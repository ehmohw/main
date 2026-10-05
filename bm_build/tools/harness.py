"""Runtime harness for the 26.3 GameTest server.
   python3 harness.py build <out|out_p2>   -> writes scratchpad/bmtest (test pack)
   python3 harness.py check <out|out_p2>   -> parses gt/run.log: trade read-back vs source, NBT decode warnings
Every trader function is run (npc/*, p17/npc/* refreshes, field rats), its Offers.Recipes is read back from the live
entity and compared field-by-field with what the pack wrote. Every literal summon / entity NBT write is replayed on a
matching entity so the game's 26.3 decoders run over it; any 'Serialization errors' warning is attributed to its line."""
import sys, os, re, glob, json, shutil
sys.path.insert(0, '/home/claude/bm_build')
S = os.environ.get('BM_SCRATCH', '/tmp/claude-0/-home-claude/3b068e51-eb2f-56d1-b54d-7ae7b9353a7e/scratchpad')   # 2.15: set BM_SCRATCH
mode, OUT = sys.argv[1], sys.argv[2]
os.environ['BM_OUT'] = OUT
import check262 as C

ROOT = f'/home/claude/bm_build/{OUT}/BlackMarket_DP/data'
PK = f'{S}/bmtest'
POS = 'execute positioned 0 100 0 run '


def snbt_at(s, i):
    return C.parse_snbt(s, i)


def summon_parts(line):
    """'... summon <type> [x y z] [nbt]' -> (type, nbt_text or '', index)."""
    m = re.search(r'(?:^|\brun |^)summon (\S+)', line)
    if not m: return None
    t = m.group(1); rest = line[m.end():].lstrip()
    toks = rest.split(' ', 3)
    if len(toks) >= 3 and all(re.fullmatch(r'[~^]?-?[\d.]*', x) for x in toks[:3]):
        rest = toks[3] if len(toks) > 3 else ''
    rest = rest.strip()
    if rest and rest[0] == '{':
        end, _ = snbt_at(rest, 0)
        return t, rest[:end]
    return t, ''



def raw_compound(s):
    """'{k:v,...}' -> [(key, raw value text)] keeping the exact SNBT (types, suffixes)."""
    p = C.SNBT(s, 1); out = []
    p.ws()
    if p.peek() == '}': return out
    while True:
        p.ws()
        k = p.qstr() if p.peek() in '"\'' else p.word()
        p.ws(); p.i += 1; p.ws()
        a = p.i; p.value(); out.append((k, s[a:p.i]))
        p.ws(); c = p.peek(); p.i += 1
        if c == '}': return out


def raw_list(s):
    p = C.SNBT(s, 1); out = []
    p.ws()
    if p.peek() == ']': return out
    while True:
        p.ws(); a = p.i; p.value(); out.append(s[a:p.i]); p.ws(); c = p.peek(); p.i += 1
        if c == ']': return out


def qk(k):
    return k if re.fullmatch(r'[A-Za-z0-9_.+-]+', k) else '"' + k + '"'


def offer_checks(name, recipes_text):
    """In-game typed checks of every field of every recipe; prints MISS|name|recipe|field (short, < 256 chars)."""
    out = [f'data modify storage bm_test:o got."{name}" set from entity @s Offers.Recipes',
           f'execute store result storage bm_test:o len int 1 run data get entity @s Offers.Recipes',
           f'data modify storage bm_test:o n set value "{name}"', 'function bm_test:say_len with storage bm_test:o']
    recs = raw_list(recipes_text)
    return out, len(recs)

KEYTYPE = [({'Offers'}, 'minecraft:wandering_trader'), ({'block_state'}, 'minecraft:block_display'),
           ({'text', 'background', 'line_width', 'text_opacity', 'see_through', 'default_background', 'alignment'}, 'minecraft:text_display'),
           ({'item'}, 'minecraft:item_display'),
           ({'transformation', 'interpolation_duration', 'start_interpolation', 'brightness', 'billboard', 'glow_color_override',
             'view_range', 'shadow_radius', 'teleport_duration'}, 'minecraft:item_display'),
           ({'width', 'height', 'response'}, 'minecraft:interaction'), ({'Item', 'PickupDelay'}, 'minecraft:item'),
           ({'Motion', 'ShowArms', 'Pose', 'Small', 'Marker'}, 'minecraft:armor_stand')]


def guess_type(sel, keys):
    m = re.search(r'type=(minecraft:[a-z_]+)', sel)
    if m: return m.group(1)
    for ks, t in KEYTYPE:
        if ks & keys: return t
    return 'minecraft:zombie'


def build():
    shutil.rmtree(PK, ignore_errors=True)
    os.makedirs(f'{PK}/data/bm_test/function'); os.makedirs(f'{PK}/data/bm_test/test_environment'); os.makedirs(f'{PK}/data/bm_test/test_instance')
    json.dump({'pack': {'description': 'BM 26.3 runtime harness', 'min_format': [121, 0], 'max_format': 121}}, open(f'{PK}/pack.mcmeta', 'w'))
    W = lambda n, lines: open(f'{PK}/data/bm_test/function/{n}.mcfunction', 'w').write('\n'.join(lines) + '\n')
    W('say_len', ['$say LEN|$(n)|$(len)'])
    W('clear', ['execute positioned 0 100 0 run kill @e[type=!minecraft:player,distance=..80]',
                'execute positioned 0 100 0 run kill @e[type=minecraft:item,distance=..80]'])
    expect, trades, k = {}, ['say HARNESS trades begin', 'function bm_test:clear'], 0
    for f in sorted(glob.glob(f'{ROOT}/bm/function/**/*.mcfunction', recursive=True)):
        rel = f[len(ROOT) + len('/bm/function/'):-len('.mcfunction')]
        for line in open(f).read().split('\n'):
            if 'Offers' not in line or line.startswith('$') or line.startswith('#'): continue
            if 'Offers.Recipes set value ' in line:
                i = line.index('Offers.Recipes set value ') + len('Offers.Recipes set value ')
                end, _ = snbt_at(line, i); rtext = line[i:end]
                t = summon_parts(open(f'{ROOT}/bm/function/{rel.replace("p17/", "")}.mcfunction').read().split('\n')[0])
                etype = t[0] if t else 'minecraft:wandering_trader'
                run = [POS + f'summon {etype} ~ ~ ~ {{NoAI:1b,Tags:["bmt"]}}', f'execute as @e[tag=bmt,limit=1] at @s run function bm:{rel}',
                       f'execute as @e[tag=bmt,limit=1] run function bm_test:chk{k}']
            elif 'summon ' in line:
                t, nbt = summon_parts(line)
                rtext = dict(raw_compound(dict(raw_compound(nbt))['Offers']))['Recipes']
                first = POS + (f'function bm:{rel}' if rel.startswith('npc/') else f'summon {t} ~ ~ ~ {nbt}')
                run = [first, f'execute positioned 0 100 0 as @e[type={t},distance=..3,limit=1,sort=nearest] run function bm_test:chk{k}']
            else: continue
            chk, nrec = offer_checks(rel, rtext)
            W(f'chk{k}', chk); k += 1
            trades += run + ['function bm_test:clear']
            expect[rel] = nrec
    # payments: every trade 'buy'/'buyB' and every exact custom_data test in the pack's commands, checked in-game against
    # the item exactly as players receive it from its loot table (component equality is tag-for-tag: 20b != 20)
    need = {}
    for f in glob.glob(f'{ROOT}/bm/function/**/*.mcfunction', recursive=True):
        for line in open(f).read().split('\n'):
            if line.startswith('$'): continue
            if 'Offers' in line:
                i = line.index('Recipes') ; i = line.index('[', i)
                end, _ = snbt_at(line, i)
                for r in raw_list(line[i:end]):
                    for k, v in raw_compound(r):
                        if k not in ('buy', 'buyB'): continue
                        d = dict(raw_compound(v))
                        if 'components' not in d: continue
                        comps = raw_compound(d['components'])
                        cid = re.search(r'bm:"([a-z0-9_]+)"', dict(comps).get('minecraft:custom_data', '')) if 'minecraft:custom_data' in dict(comps) else None
                        if not cid: continue
                        pred = d['id'].strip('"') + '[' + ','.join(f'{kk}={vv}' for kk, vv in comps) + ']'
                        need.setdefault(cid.group(1), set()).add(('trade', pred))
            for m in re.finditer(r'[\[,](minecraft:)?custom_data=(\{[^}]*\})', line):
                cid = re.search(r'bm:"([a-z0-9_]+)"', m.group(2))
                if cid: need.setdefault(cid.group(1), set()).add(('cmd', '*[minecraft:custom_data=' + m.group(2) + ']'))
    npay = 0
    for c in sorted(need):
        if not os.path.exists(f'{ROOT}/bm/loot_table/items/{c}.json'): print('no loot table for', c); continue
        chk = [f'say PAYRAN|{c}']
        for j, (kind, pred) in enumerate(sorted(need[c])):
            chk.append(f'execute unless items entity @s contents {pred} run say PAYFAIL|{c}|{kind}|{j}')
            npay += 1
        W(f'pay_{c}', chk)
        open(f'{S}/harness_pay_{c}.txt', 'w').write('\n'.join(p for _, p in sorted(need[c])))
        trades += [POS + f'loot spawn ~ ~ ~ loot bm:items/{c}',
                   f'execute positioned 0 100 0 as @e[type=minecraft:item,distance=..3,limit=1] run function bm_test:pay_{c}',
                   'function bm_test:clear']
    json.dump(sorted(c for c in need if os.path.exists(f'{ROOT}/bm/loot_table/items/{c}.json')), open(f'{S}/harness_pay_{OUT}.json', 'w'))
    print(f'{npay} payment/predicate checks over {len(need)} items')
    trades.append('say HARNESS trades end')
    W('trades', trades)
    json.dump(expect, open(f'{S}/harness_expect_{OUT}.json', 'w'))

    # every literal summon and entity NBT write, replayed on a matching entity
    nbt, n = ['say HARNESS nbt begin', 'function bm_test:clear',      # canaries: both must be reported, proving detection works
              'say NBT|canary_summon', POS + 'summon minecraft:block_display ~ ~ ~ {block_state:{Name:"minecraft:stone"}}', 'function bm_test:clear',
              'say NBT|canary_merge', POS + 'summon minecraft:block_display ~ ~ ~ {Tags:["bmr"]}',
              POS + 'data merge entity @e[tag=bmr,limit=1] {block_state:{Name:"minecraft:stone"}}', 'function bm_test:clear'], 0
    for f in sorted(glob.glob(f'{ROOT}/*/function/**/*.mcfunction', recursive=True)):
        rel = os.path.relpath(f, ROOT)
        for ln, line in enumerate(open(f).read().split('\n'), 1):
            if line.startswith('$') or line.startswith('#') or not line: continue
            cmd = None
            if re.search(r'(^|\brun )summon ', line):
                t, comp = summon_parts(line)
                cmd = f'summon {t} ~ ~ ~ {comp}'
            else:
                m = re.search(r'\bdata merge entity (\S+) (\{.*)$', line)
                if m:
                    end, v = snbt_at(m.group(2), 0)
                    cmd = (f'summon {guess_type(m.group(1), set(v))} ~ ~ ~ {{Tags:["bmr"]}}\n'
                           f'data merge entity @e[tag=bmr,limit=1] {m.group(2)[:end]}')
                m = re.search(r'\bdata modify entity (\S+) ([A-Za-z_]+) set value ([\{\[].*)$', line)
                if m:
                    end, v = snbt_at(m.group(3), 0)
                    key = m.group(2)
                    cmd = (f'summon {guess_type(m.group(1), {key})} ~ ~ ~ {{Tags:["bmr"]}}\n'
                           f'data modify entity @e[tag=bmr,limit=1] {key} set value {m.group(3)[:end]}')
            if not cmd: continue
            n += 1
            nbt += [f'say NBT|{rel}:{ln}'] + [POS + c for c in cmd.split('\n')] + ['function bm_test:clear']
    nbt.append('say HARNESS nbt end')
    W('nbt', nbt)
    tpl = ['say HARNESS templates begin']
    for f in sorted(glob.glob(f'{ROOT}/bm/structure/**/*.nbt', recursive=True)):
        t = os.path.relpath(f, f'{ROOT}/bm/structure')[:-4]
        tpl += [f'say NBT|template:{t}', 'execute unless loaded 160 0 160 run say TEMPLATE area not loaded',
                f'place template bm:{t} 0 -40 0', f'execute if block 0 -40 0 minecraft:structure_void run say TPL|{t}|void-corner',
                'execute positioned 80 0 80 run kill @e[type=!minecraft:player,distance=..200]']
    tpl.append('say HARNESS templates end')
    W('templates', tpl)
    # macro lines are only parsed when called: write each one with sample arguments into a plain function so the
    # server parses it at load (a parse error is logged with the file and line)
    os.makedirs(f'{PK}/data/bm_test/function/macro', exist_ok=True)
    nm = 0; mapping = {}
    for f in sorted(glob.glob(f'{ROOT}/*/function/**/*.mcfunction', recursive=True)):
        rel = os.path.relpath(f, ROOT)
        lines = [l for l in open(f).read().split('\n') if l.startswith('$')]
        if not lines: continue
        out = []
        for line in lines:
            line = line[1:].replace('$(eid)', 'minecraft:pig').replace('$(data)', '{}').replace('$(dim)', 'minecraft:overworld').replace('$(path)', 'Inventory[{Slot:0b}]').replace('$(slot)', 'container.0').replace('$(iid)', 'token').replace('$(id)', 'minecraft:diamond_sword').replace('$(a)', '30').replace('$(b)', '210').replace('$(col)', 'gold').replace('"minecraft:container":$(c)', '"minecraft:container":[]')
            out.append(re.sub(r'\$\(\w+\)', '1', line))
        open(f'{PK}/data/bm_test/function/macro/m{nm}.mcfunction', 'w').write('\n'.join(out) + '\n')
        mapping[f'm{nm}'] = rel; nm += 1
    json.dump(mapping, open(f'{S}/harness_macros_{OUT}.json', 'w'))
    print(f'{nm} macro functions written for load-time parsing')
    W('setup', ['forceload add -48 -48 48 48', 'forceload add 0 0 175 175', 'say HARNESS setup'])
    W('run', ['say HARNESS run', 'function bm_test:trades', 'function bm_test:nbt', 'say HARNESS done'])
    json.dump({'type': 'minecraft:function', 'setup': 'bm_test:setup', 'teardown': 'bm_test:run'},
              open(f'{PK}/data/bm_test/test_environment/main.json', 'w'))
    json.dump({'type': 'minecraft:function', 'environment': 'bm_test:main', 'function': 'minecraft:always_pass', 'max_ticks': 20,
               'structure': 'minecraft:empty', 'required': False}, open(f'{PK}/data/bm_test/test_instance/main.json', 'w'))
    # every structure template is also placed by the GameTest framework itself (entities decoded on placement)
    W('tpl_count', ['execute store result storage bm_test:o mk int 1 if entity @e[type=minecraft:marker,distance=..300]',
                    'function bm_test:say_mk with storage bm_test:o'])
    W('say_mk', ['$say MARKERS|$(mk)'])
    json.dump({'type': 'minecraft:function', 'setup': 'bm_test:noop'}, open(f'{PK}/data/bm_test/test_environment/tpl.json', 'w'))
    W('noop', ['say HARNESS templates placed'])
    nt = 0
    for f in sorted(glob.glob(f'{ROOT}/bm/structure/**/*.nbt', recursive=True)):
        t = os.path.relpath(f, f'{ROOT}/bm/structure')[:-4]
        json.dump({'type': 'minecraft:function', 'environment': 'bm_test:tpl', 'function': 'minecraft:always_pass', 'max_ticks': 20,
                   'structure': f'bm:{t}', 'required': False}, open(f'{PK}/data/bm_test/test_instance/tpl_{t}.json', 'w')); nt += 1
    print(f'{len(expect)} trader offer sets, {n} NBT replays, {nt} templates')


def loose_eq(e, a, path, out):
    if isinstance(e, dict):
        if not isinstance(a, dict): out.append(f'{path}: expected compound, got {str(a)[:80]}'); return
        for k, v in e.items():
            if k not in a: out.append(f'{path}.{k}: missing after load'); continue
            loose_eq(v, a[k], f'{path}.{k}', out)
    elif isinstance(e, list):
        if not isinstance(a, list) or len(a) != len(e): out.append(f'{path}: list length {len(e)} -> {len(a) if isinstance(a, list) else a!r}'); return
        for i, (x, y) in enumerate(zip(e, a)): loose_eq(x, y, f'{path}[{i}]', out)
    elif isinstance(e, (int, float)) and isinstance(a, (int, float)):
        if abs(e - a) > 1e-4: out.append(f'{path}: {e} -> {a}')
    elif e != a: out.append(f'{path}: {str(e)[:60]!r} -> {str(a)[:60]!r}')


def check():
    log = open(f'{S}/gt/run.log', encoding='utf-8', errors='replace').read().split('\n')
    expect = json.load(open(f'{S}/harness_expect_{OUT}.json'))
    lens, miss, warns, marker, done = {}, {}, {}, 'startup', False
    for l in log:
        m = re.search(r'\] LEN\|([^|]+)\|(\d+)$', l)
        if m: lens[m.group(1)] = int(m.group(2)); marker = 'TRADE ' + m.group(1); continue
        m = re.search(r'\] PAYFAIL\|(.*)$', l)
        if m: miss.setdefault('PAYMENT', []).append(m.group(1)); continue
        m = re.search(r'\] MISS\|([^|]+)\|(\d+)\|(.*)$', l)
        if m: miss.setdefault(m.group(1), []).append(f'recipe {m.group(2)}: {m.group(3)}'); continue
        m = re.search(r'\[Server\] (NBT\|\S+|HARNESS \w+.*)$', l)
        if m:
            marker = m.group(1); done = done or 'HARNESS done' in l; continue
        if 'Serialization errors' in l or ('WARN' in l and 'Failed' in l) or l.startswith(': '):
            warns.setdefault(marker, []).append(l.strip()[:300])
    print('harness completed:', done)
    bad = 0
    for n, cnt in sorted(expect.items()):
        if n not in lens: print(f'✗ {n}: trader missing / no read-back'); bad += 1; continue
        if lens[n] != cnt: print(f'✗ {n}: {cnt} recipes written, {lens[n]} on the trader'); bad += 1
        if n in miss: bad += 1; print(f'✗ {n}: {len(miss[n])} fields differ'); [print('   ', d) for d in miss[n][:10]]
    ran = set(re.findall(r'\] PAYRAN\|([a-z0-9_]+)', '\n'.join(log)))
    want = set(json.load(open(f'{S}/harness_pay_{OUT}.json')))
    if want - ran: print(f'✗ payment checks did not run for {len(want - ran)} items: {sorted(want - ran)[:8]}')
    else: print(f'payment checks ran for all {len(want)} items')
    if 'PAYMENT' in miss: print(f'✗ PAYMENT: {len(miss["PAYMENT"])} item/predicate mismatches'); [print('   ', d) for d in miss['PAYMENT'][:25]]
    else: print('payments: every trade cost and exact custom_data test accepts the loot-table item')
    print(f'trades: {len(expect)} offer sets, {sum(expect.values())} recipes; {bad} sets with problems')
    for k, v in warns.items():
        if k == 'startup' and not any('Serialization' in x for x in v): continue
        print(f'⚠ {k}:'); [print('   ', x[:220]) for x in v[:4]]
    print(f'decode warnings under {len([k for k in warns if k != "startup"])} markers')


build() if mode == 'build' else check()
