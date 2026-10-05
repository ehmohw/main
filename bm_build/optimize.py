"""2.15: a final pass over every generated function, run just before they are written. It only changes HOW often or HOW
cheaply a command finds its entities - never what it does - and every change is provably equivalent:

1. TYPED SELECTORS. `@e[tag=bm.x]` makes the game test every loaded entity; `@e[type=minecraft:husk,tag=bm.x]` only
   tests husks. For each tag the pack ever puts on an entity, the pass collects the entity types it is put on - from every
   `summon` (passengers included) and every structure template's entities. A tag that is also added any other way (`tag ...
   add`, `data merge/modify ... Tags`) is left alone, since then any entity could carry it. Mob conversions (a husk drowning
   into a zombie, a villager struck into a witch...) are followed so a converted mob is still found.
2. QUIET DUNGEONS. Each Phase 2 dungeon runs ~6 entity scans every tick (puzzles, secret buttons, gates, the arena) and more
   every 5 ticks (effects, the altar). They only matter with someone nearby, so they move into one function per dungeon,
   called only while a player is within its radius (+24) of its controller - checked once a second.
3. QUIET MARKETS. Likewise the market's door, bouncers, fountain and effects, neon signs, walkers, busker, vents, ledgers,
   trader offer syncs and chatter, crowd and ambience run only while someone is within 100 blocks of a market."""
import gzip, io, json, os, re, struct
from collections import defaultdict

CONVERT = {'husk': {'zombie', 'drowned'}, 'zombie': {'drowned'}, 'villager': {'zombie_villager', 'witch'}, 'zombie_villager': {'villager'},
           'pig': {'zombified_piglin'}, 'piglin': {'zombified_piglin'}, 'piglin_brute': {'zombified_piglin'}, 'hoglin': {'zoglin'},
           'skeleton': {'stray'}, 'mooshroom': {'cow'}, 'cow': {'mooshroom'}, 'tadpole': {'frog'}, 'creaking': set()}
MARKET_TAGS = ('bm.market_door', 'bm.market_hall', 'bm.mfx', 'bm.mfx2', 'bm.nflk', 'bm.neon_', 'bm.walker', 'bm.busker', 'bm.vent', 'bm.ledger')


# ---------------------------------------------------------------- a small SNBT reader (summon NBT)
class _P:
    def __init__(self, s): self.s, self.i = s, 0
    def ws(self):
        while self.i < len(self.s) and self.s[self.i] in ' \t': self.i += 1
    def val(self):
        self.ws(); c = self.s[self.i]
        if c == '{': return self.comp()
        if c == '[': return self.lst()
        if c in '"\'': return self.string()
        j = self.i
        while self.i < len(self.s) and self.s[self.i] not in ',]}': self.i += 1
        return self.s[j:self.i].strip()
    def string(self):
        q = self.s[self.i]; self.i += 1; out = []
        while self.s[self.i] != q:
            if self.s[self.i] == '\\': self.i += 1
            out.append(self.s[self.i]); self.i += 1
        self.i += 1
        return ''.join(out)
    def comp(self):
        self.i += 1; d = {}
        while True:
            self.ws()
            if self.s[self.i] == '}': self.i += 1; return d
            if self.s[self.i] in '"\'': k = self.string()
            else:
                j = self.i
                while self.s[self.i] not in ':': self.i += 1
                k = self.s[j:self.i].strip()
            self.ws(); self.i += 1
            d[k] = self.val(); self.ws()
            if self.s[self.i] == ',': self.i += 1
    def lst(self):
        self.i += 1; self.ws(); out = []
        if self.s[self.i:self.i + 2] in ('I;', 'B;', 'L;'): self.i += 2
        while True:
            self.ws()
            if self.s[self.i] == ']': self.i += 1; return out
            out.append(self.val()); self.ws()
            if self.s[self.i] == ',': self.i += 1


def _ents(kind, nbt, out):
    """(type, tags) for an entity and its passengers."""
    tags = nbt.get('Tags', []) if isinstance(nbt, dict) else []
    out.append((kind, [t for t in tags if isinstance(t, str)]))
    for p in (nbt.get('Passengers', []) if isinstance(nbt, dict) else []):
        if isinstance(p, dict) and isinstance(p.get('id'), str): _ents(p['id'].split(':')[-1], p, out)


# ---------------------------------------------------------------- a small binary NBT reader (structure templates)
def _read_nbt(raw):
    f = io.BytesIO(raw)
    def r(fmt): return struct.unpack('>' + fmt, f.read(struct.calcsize('>' + fmt)))[0]
    def rstr(): n = r('H'); return f.read(n).decode('utf-8', 'replace')
    def payload(t):
        if t == 1: return r('b')
        if t == 2: return r('h')
        if t == 3: return r('i')
        if t == 4: return r('q')
        if t == 5: return r('f')
        if t == 6: return r('d')
        if t == 7: n = r('i'); return f.read(n)
        if t == 8: return rstr()
        if t == 9:
            et, n = r('b'), r('i'); return [payload(et) for _ in range(n)]
        if t == 10:
            d = {}
            while True:
                tt = r('b')
                if tt == 0: return d
                k = rstr(); d[k] = payload(tt)
        if t == 11: n = r('i'); return [r('i') for _ in range(n)]
        if t == 12: n = r('i'); return [r('q') for _ in range(n)]
        raise ValueError(t)
    t = r('b'); rstr()
    return payload(t)


def collect(funcs, structure_dir):
    types, unsafe = defaultdict(set), set()
    summon = re.compile(r'summon (minecraft:[a-z0-9_]+)(?: +[~^\-\d.]*[~^\-\d.]+ +[~^\-\d.]*[~^\-\d.]+ +[~^\-\d.]*[~^\-\d.]+)?(?: +(\{.*))?$')
    for name, lines in funcs.items():
        for l in lines:
            body = l.lstrip('$')
            for m in re.finditer(r'\btag @\w(?:\[[^\]]*\])? add ([\w.\-$()]+)', body): unsafe.add(m.group(1))
            if re.search(r'data (merge|modify) (entity|storage)', body) and 'Tags' in body:
                unsafe.update(re.findall(r'"(bm\.[\w.\-]+)"', body))
            i = body.find('summon minecraft:')
            if i < 0: continue
            m = summon.match(body[i:])
            if not m: unsafe.update(re.findall(r'"(bm\.[\w.\-]+)"', body)); continue
            kind = m.group(1).split(':')[-1]
            if not m.group(2): continue
            try:
                nbt = _P(m.group(2)).val()
            except Exception:
                unsafe.update(re.findall(r'"(bm\.[\w.\-]+)"', body)); continue
            if '$(' in m.group(2): unsafe.update(re.findall(r'"(bm\.[\w.\-]+)"', body))
            out = []; _ents(kind, nbt, out)
            for k, tags in out:
                for t in tags: types[t].add(k)
    def walk(o):
        """Any compound with a Tags list: an entity (spawner/trial spawner data, template entities). With an id we know its
        type; without one the tag is treated as unsafe."""
        if isinstance(o, dict):
            tg = o.get('Tags')
            if isinstance(tg, list) and all(isinstance(t, str) for t in tg):
                if isinstance(o.get('id'), str):
                    for t in tg: types[t].add(o['id'].split(':')[-1])
                else: unsafe.update(tg)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    if os.path.isdir(structure_dir):
        for fn in os.listdir(structure_dir):
            if fn.endswith('.nbt'): walk(_read_nbt(gzip.decompress(open(os.path.join(structure_dir, fn), 'rb').read())))
    data_dir = os.path.dirname(os.path.dirname(structure_dir))          # .../data
    for base, dirs, files in os.walk(data_dir):
        for fn in files:
            if fn.endswith('.json'):
                try: walk(json.load(open(os.path.join(base, fn))))
                except Exception: pass
    for t in list(types):                       # follow conversions
        extra = set()
        for k in types[t]: extra |= CONVERT.get(k, set())
        types[t] |= extra
    return {t: ks for t, ks in types.items() if t not in unsafe}


def split_args(inner):
    out, depth, cur, q = [], 0, [], None
    for ch in inner:
        if q:
            cur.append(ch)
            if ch == q: q = None
            continue
        if ch in '"\'': q = ch
        elif ch in '{[': depth += 1
        elif ch in '}]': depth -= 1
        if ch == ',' and depth == 0: out.append(''.join(cur)); cur = []
        else: cur.append(ch)
    if cur: out.append(''.join(cur))
    return out


def type_selectors(funcs, safe, wjson):
    autotags, n = {}, 0
    def fix(m):
        nonlocal n
        inner = m.group(1)
        args = [a.strip() for a in split_args(inner)]
        if any(a.startswith('type=') for a in args): return m.group(0)
        cands = [safe[a[4:]] for a in args if a.startswith('tag=') and not a.startswith('tag=!') and a[4:] in safe]
        if not cands: return m.group(0)
        ks = tuple(sorted(min(cands, key=len)))
        if len(ks) == 1: t = 'minecraft:' + ks[0]
        else:
            if ks not in autotags: autotags[ks] = f'auto{len(autotags)}'
            t = f'#bm:{autotags[ks]}'
        n += 1
        return f'@e[type={t},{inner}]'
    sel = re.compile(r'@e\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]')
    for name, lines in funcs.items():
        funcs[name] = [sel.sub(fix, l) for l in lines]
    for ks, tag in autotags.items():
        wjson(f'bm/tags/entity_type/{tag}.json', {'values': [f'minecraft:{k}' for k in ks]})
    return n, len(autotags)


def gate(funcs, name, pred, fn_name):
    """Move the lines of funcs[name] that match pred into funcs[fn_name]; a single call line takes the first one's place."""
    lines = funcs[name]
    moved = [l for l in lines if pred(l)]
    if not moved: return 0
    k = next(i for i, l in enumerate(lines) if pred(l))
    rest = [l for l in lines if not pred(l)]
    funcs[fn_name] = moved
    return moved, k - sum(1 for l in lines[:k] if pred(l)), rest


def optimize(G):
    funcs = G.FUNCS
    safe = collect(funcs, G.path('data', 'bm', 'structure'))
    report = []
    # 2 + 3: quiet dungeons and markets (before typing, so the moved lines get typed too)
    pre = ['scoreboard players set #opt_mn bm.rng 0',
           'execute as @e[type=minecraft:marker,tag=bm.market_hall] at @s if entity @a[distance=..100] run scoreboard players set #opt_mn bm.rng 1',
           'execute as @e[type=minecraft:marker,tag=bm.mkt] at @s if entity @a[distance=..100] run scoreboard players set #opt_mn bm.rng 1']
    if G.PHASE2:
        from p2.config import D
        for d, cfg in D.items():
            mine = lambda l, d=d: f'tag=bm.d_{d}' in l and 'bm.eshaft' not in l and 'bm.entr' not in l
            for loop, short in (('tick', 'tick'), ('loop/fast', 'fast')):
                r = gate(funcs, loop, mine, f'opt/{d}_{short}')
                if not r: continue
                moved, k, rest = r
                funcs[loop] = rest[:k] + [f'execute if score #opt_dn_{d} bm.rng matches 1 run function bm:opt/{d}_{short}'] + rest[k:]
                report.append(f'{d}: {len(moved)} {short} lines gated')
            pre += [f'scoreboard players set #opt_dn_{d} bm.rng 0',
                    f'execute as @e[type=minecraft:marker,tag=bm.dg,tag=bm.d_{d}] at @s if entity @a[distance=..{cfg["radius"] + 24}] run scoreboard players set #opt_dn_{d} bm.rng 1']
    first_sel = lambda l: re.match(r'execute as @e\[([^\]]*)\]', l)
    def market_line(l):
        m = first_sel(l)
        if not m: return False
        tags = [a.split('=', 1)[1] for a in split_args(m.group(1)) if a.startswith('tag=') and not a.startswith('tag=!')]
        return any(t == mt or (mt.endswith('_') and t.startswith(mt)) for t in tags for mt in MARKET_TAGS)
    r = gate(funcs, 'loop/fast', market_line, 'opt/market_fast')
    if r:
        moved, k, rest = r
        funcs['loop/fast'] = rest[:k] + ['execute if score #opt_mn bm.rng matches 1 run function bm:opt/market_fast'] + rest[k:]
        report.append(f'market: {len(moved)} fast lines gated')
    # the once-a-second market chores too: trader offer syncs and chatter, the crowd, ambience, signs/portraits, the bouncers
    msec = ('bm.market_hall', 'bm.mkt', 'bm.crowd', 'bm.amb_', 'bm.walker') + tuple(f'bm.npc_{k}' for k in G.NPCS)
    def market_second(l):
        if 'bm.say=1..' in l: return True                     # only market traders ever carry bm.say
        m = first_sel(l)
        if not m: return False
        tags = [a.split('=', 1)[1] for a in split_args(m.group(1)) if a.startswith('tag=') and not a.startswith('tag=!')]
        return any(t == mt or (mt.endswith('_') and t.startswith(mt)) for t in tags for mt in msec)
    # 4. HALF-SECOND OFFSET: these self-contained groups (market chores, each dungeon's once-a-second work) run in their own
    # loop half a second after loop/second, so the two halves don't land in the same tick
    later = []
    r = gate(funcs, 'loop/second', market_second, 'opt/market_second')
    if r:
        moved, k, rest = r
        funcs['loop/second'] = rest
        later.append('execute if score #opt_mn bm.rng matches 1 run function bm:opt/market_second')
        report.append(f'market: {len(moved)} second lines gated (half a second later)')
    if G.PHASE2:
        for d, cfg in D.items():
            mine = lambda l, d=d: f'tag=bm.d_{d}' in l and 'bm.eshaft' not in l and 'bm.entr' not in l
            r = gate(funcs, 'loop/second', mine, f'opt/{d}_second')
            if r:
                moved, k, rest = r
                funcs['loop/second'] = rest
                later.append(f'execute if score #opt_dn_{d} bm.rng matches 1 run function bm:opt/{d}_second')
                report.append(f'{d}: {len(moved)} second lines gated (half a second later)')
    funcs['loop/second_b'] = later + ['schedule function bm:loop/second_b 20t replace']
    for fname in ('load',):
        ld = funcs[fname]
        k = next(i for i, l in enumerate(ld) if l == 'schedule function bm:loop/second 20t replace')
        ld.insert(k + 1, 'schedule function bm:loop/second_b 30t replace')
    funcs['admin/uninstall'].insert(0, 'schedule clear bm:loop/second_b')
    funcs['loop/second'][0:0] = pre
    # 1: typed selectors everywhere
    n, na = type_selectors(funcs, safe, G.wjson)
    report.append(f'{n} entity selectors typed ({na} multi-type tags), from {len(safe)} provably-typed tags')
    return report
