"""Trade / item-NBT integrity audit (1.13). Run on a built pack:  BM_OUT=out python3 check_trades.py

Villager trade costs match items EXACTLY on the components they list, so a trade breaks the moment the item a player
holds differs from the price tag in any of those components. This audit proves, for the generated pack, that:
  1. every Black Market item anywhere in the pack (functions, loot tables, item modifiers, advancements, structure
     NBT) carries the current item version stamp (bmv) - a stale stamp is exactly the 1.12 Lucky Whiskers bug;
  2. every trade COST of a Black Market item lists components identical to the item's real definition, and keeps
     max_stack_size for stack-limited bases (else the game clamps the price);
  3. every trade RESULT is the item exactly as defined, so what a trader sells is accepted by every other trader;
  4. every loot table that drops a Black Market item drops it exactly as defined;
  5. each trader's spawn offers are identical to the offers its refresh writes (no trader can be "downgraded");
  6. every NPC marker in every structure has a spawner, and every trader has a refresh with a checksum;
  7. every Black Market item used as a price can actually be obtained somewhere in the pack.
Runtime drift (items and traders already in a world) is handled in-game: items are restamped when held
(phase18) and traders re-sync whenever their offer checksum changes (phase17)."""
import glob, json, os, re, sys
import check262 as C
from nbt import read_nbt_gz

ROOT = C.ROOT_DP
errs, notes = [], []
COST_KEYS = ('minecraft:custom_data', 'minecraft:item_model', 'minecraft:item_name', 'minecraft:max_stack_size')   # 1.16: no glint override (Xenite trades refused real shards)


def E(m): errs.append(m)


def norm(v):
    """SNBT-parsed and JSON values -> comparable plain Python."""
    if isinstance(v, bool): return int(v)
    if isinstance(v, dict): return {str(k): norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [norm(x) for x in v]
    if isinstance(v, float) and v.is_integer(): return int(v)
    if isinstance(v, int): return int(v)
    if isinstance(v, str):
        if v.startswith('{') and v.endswith('}'):          # an SNBT string inside JSON (custom_data in some tables)
            try: return norm(C.parse_snbt(v, 0)[1])
            except Exception: return v
        return v
    return v


# ---------------- the canonical definition of every item: bm:items/<iid> loot tables are written from ITEMS
CANON = {}
for f in glob.glob(f'{ROOT}/bm/loot_table/items/*.json'):
    iid = os.path.basename(f)[:-5]
    e = C.jload(f)['pools'][0]['entries'][0]
    comps = next(fn['components'] for fn in e['functions'] if fn['function'] == 'minecraft:set_components')
    CANON[iid] = {'base': e['name'], 'comps': norm(comps)}
VERSIONS = {c['comps']['minecraft:custom_data'].get('bmv') for c in CANON.values()}
if len(VERSIONS) != 1: E(f'item definitions disagree on the version stamp: {VERSIONS}')
VER = next(iter(VERSIONS))


def iid_of(comps):
    cd = comps.get('minecraft:custom_data') if isinstance(comps, dict) else None
    return cd.get('bm') if isinstance(cd, dict) and isinstance(cd.get('bm'), str) else None


# ---------------- 1. version stamps everywhere
STAMP = re.compile(r'bm:"([a-z0-9_]+)",bmv:(\d+)|"bm":\s*"([a-z0-9_]+)",\s*"bmv":\s*(\d+)')
files = glob.glob(f'{ROOT}/**/*.mcfunction', recursive=True) + glob.glob(f'{ROOT}/**/*.json', recursive=True)
for f in files:
    rel = f[len(ROOT) + 1:]
    for ln, line in enumerate(open(f, encoding='utf-8'), 1):
        for m in STAMP.finditer(line):
            iid, v = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
            if int(v) != VER: E(f'{rel}:{ln}: {iid} stamped bmv:{v}, current is {VER}')


def walk_nbt(o, path, out):
    if isinstance(o, dict):
        if 'minecraft:custom_data' in o or 'custom_data' in o: out.append((path, o))
        for k, v in o.items(): walk_nbt(v, f'{path}.{k}', out)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk_nbt(v, f'{path}[{i}]', out)


MARKERS = {}
for f in glob.glob(f'{ROOT}/bm/structure/*.nbt'):
    d = read_nbt_gz(f); name = os.path.basename(f)
    found = []
    walk_nbt(d.get('blocks', []), name, found)
    for path, comps in found:
        cd = comps.get('minecraft:custom_data') or comps.get('custom_data')
        cd = norm(cd)
        if isinstance(cd, dict) and 'bm' in cd and cd.get('bmv') != VER: E(f'{path}: {cd.get("bm")} stamped bmv:{cd.get("bmv")}, current is {VER}')
    for e in d.get('entities', []):
        for t in e['nbt'].get('Tags', []):
            if t.startswith('bm.npc.'): MARKERS.setdefault(t[7:], set()).add(name)

# ---------------- trades: parse every Offers list the pack writes
SPAWN, REFRESH, OTHER = {}, {}, {}
OFFERS = re.compile(r'Offers:\{Recipes:(\[.*?\])\}[,}]')
for f in glob.glob(f'{ROOT}/bm/function/**/*.mcfunction', recursive=True):
    rel = f[len(ROOT) + 13:-11]
    for ln, line in enumerate(open(f, encoding='utf-8'), 1):
        if 'Recipes' not in line: continue
        if line.startswith('$'): line = re.sub(r'\$\((\w+)\)', '0', line[1:])
        if 'Offers.Recipes set value ' in line:
            recs = C.parse_snbt(line.split('Offers.Recipes set value ', 1)[1].strip(), 0)[1]
            key = rel.split('/')[-1]
            (REFRESH if rel.startswith('p17/npc/') else OTHER)[rel if not rel.startswith('p17/npc/') else key] = recs
            continue
        i = line.find('Offers:{Recipes:')
        if i >= 0:
            j = line.find('{', line.find(' ', line.find('summon ') + 7))
            nbt = C.parse_snbt(line[line.index('{', line.index('summon minecraft:')):].strip(), 0)[1]
            recs = nbt['Offers']['Recipes']
            if rel.startswith('npc/'): SPAWN[rel[4:]] = recs
            else: OTHER[f'{rel}:{ln}'] = recs

ALL_TRADES = [(k, r) for k, rs in list(SPAWN.items()) + list(REFRESH.items()) + list(OTHER.items()) for r in rs]
used_as_price = set()
for who, r in ALL_TRADES:
    for slot in ('buy', 'buyB'):
        st = r.get(slot)
        if not st: continue
        comps = norm(st.get('components', {}))
        iid = iid_of(comps)
        if not iid: continue
        used_as_price.add(iid)
        can = CANON.get(iid)
        if not can: E(f'{who}: price {iid} has no item definition'); continue
        if st['id'] != can['base']: E(f'{who}: price {iid} is a {st["id"]}, the item is a {can["base"]}')
        for k, v in comps.items():
            if k not in can['comps']: E(f'{who}: price {iid} asks for component {k} the item never has')
            elif can['comps'][k] != v: E(f'{who}: price {iid} component {k} differs from the item: {v} vs {can["comps"][k]}')
        if 'minecraft:custom_data' not in comps: E(f'{who}: price {iid} lacks custom_data')
        if 'minecraft:max_stack_size' in can['comps'] and 'minecraft:max_stack_size' not in comps:
            E(f'{who}: price {iid} omits max_stack_size - the game would clamp the price')
    st = r['sell']
    comps = norm(st.get('components', {}))
    iid = iid_of(comps)
    if iid and iid in CANON:
        can = CANON[iid]
        if st['id'] != can['base'] or comps != can['comps']:
            diff = sorted(set(k for k in set(comps) | set(can['comps']) if comps.get(k) != can['comps'].get(k)))
            E(f'{who}: sells {iid} different from its definition ({diff})')

# ---------------- 5. spawn offers == refresh offers; 6. markers have spawners
for k, recs in SPAWN.items():
    if k in ('deco_rat', 'deco_key'): continue
    if k not in REFRESH: E(f'trader {k}: no checksum refresh (old copies would never update)'); continue
    if norm(recs) != norm(REFRESH[k]): E(f'trader {k}: spawn offers differ from refresh offers')
dispatch = open(f'{ROOT}/bm/function/npc/spawn.mcfunction').read()
for k, where in MARKERS.items():
    if f'tag=bm.npc.{k}]' not in dispatch: E(f'marker bm.npc.{k} ({", ".join(sorted(where))}) has no spawner in npc/spawn')
    if not os.path.exists(f'{ROOT}/bm/function/npc/{k}.mcfunction'): E(f'marker bm.npc.{k}: npc/{k} function missing')
second = open(f'{ROOT}/bm/function/loop/second.mcfunction').read()
# 2.15: optimize.py moves the market's once-a-second chores into opt/market_second, called from loop/second_b while a
# player is near a market - follow that call
for extra in ('loop/second_b', 'opt/market_second'):
    pth = f'{ROOT}/bm/function/{extra}.mcfunction'
    if os.path.exists(pth) and (extra == 'loop/second_b' or 'function bm:opt/market_second' in second): second += '\n' + open(pth).read()
for k in REFRESH:
    if f'tag=bm.npc_{k}] unless score @s bm.ofv' not in second: E(f'trader {k}: refresh not wired into the second loop')

# ---------------- 4. loot tables drop items exactly as defined; 7. every price is obtainable
produced = set()
for f in glob.glob(f'{ROOT}/**/loot_table/**/*.json', recursive=True):
    rel = f[len(ROOT) + 1:]
    def scan(o):
        if isinstance(o, dict):
            for fn_ in o.get('functions', []) if isinstance(o.get('functions'), list) else []:
                if fn_.get('function') == 'minecraft:set_components':
                    comps = norm(fn_['components'])
                    iid = iid_of(comps)
                    if iid and iid in CANON:
                        produced.add(iid)
                        if comps != CANON[iid]['comps'] and not rel.startswith('bm/loot_table/items/'):
                            diff = sorted(k for k in set(comps) | set(CANON[iid]['comps']) if comps.get(k) != CANON[iid]['comps'].get(k))
                            E(f'{rel}: drops {iid} different from its definition ({diff})')
            for v in o.values(): scan(v)
        elif isinstance(o, list):
            for v in o: scan(v)
    if not rel.startswith('bm/loot_table/items/'): scan(C.jload(f))
for f in glob.glob(f'{ROOT}/bm/function/**/*.mcfunction', recursive=True):
    for line in open(f, encoding='utf-8'):
        if re.search(r'(^|run )(give |item replace .* with )', line):
            produced.update(m.group(1) for m in re.finditer(r'custom_data=\{bm:"([a-z0-9_]+)"', line))
        produced.update(m.group(1) for m in re.finditer(r'loot bm:items/([a-z0-9_]+)', line))
for who, r in ALL_TRADES:
    iid = iid_of(norm(r['sell'].get('components', {})))
    if iid: produced.add(iid)
for iid in sorted(used_as_price - produced):
    E(f'{iid} is used as a price but nothing in the pack gives, drops or sells it')

# ---------------- 8. load order: no scoreboard line uses an objective before load creates it
made = set()
for ln, line in enumerate(open(f'{ROOT}/bm/function/load.mcfunction', encoding='utf-8'), 1):
    m = re.match(r'scoreboard objectives add (\S+)', line)
    if m: made.add(m.group(1)); continue
    m = re.match(r'scoreboard players \S+ \S+ (bm\.\S+)', line)
    if m and m.group(1) not in made: E(f'load.mcfunction:{ln}: uses {m.group(1)} before it is created')

for e in errs: print('✗', e)
print(f'{len(ALL_TRADES)} trades, {len(CANON)} items, {len(MARKERS)} NPC marker kinds audited (item version {VER}): {len(errs)} errors')
sys.exit(1 if errs else 0)
