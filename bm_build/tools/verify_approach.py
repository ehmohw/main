"""3.0a: prove the way to the Undercrown's Maw is open (p2/underroad), offline: the built template set into sample Nether
terrain, then the very commands of p237/build/roads run on it by a small interpreter (fill / setblock / execute positioned,
store, if score, if block / function / return / scoreboard / summon / kill - just what the approach uses), then a walk search
(p2/verify's Grid: walk, step up one, fall, climb vines).

For each terrain it checks:
  - from open Nether air (a floor in the terrain's own cave) the walk reaches the Hidden Gate's landing, the court (OUTER, where
    the Summons points) on the way;
  - every road's end (its marker) is walkable, and the road broke into open air (#ubopen) - except where the terrain has none;
  - no lava touches anything the approach cut (beside or above an air cell it made), and none of the template was changed.

    python3 tools/verify_approach.py            # every terrain
    python3 tools/verify_approach.py lava open  # some
"""
import math, os, random, re, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import p2.undercfg as U
import p2.underroad as R
from p2.dungeons import undercrown as UC
import p2.verify as PV
from p2.verify import Grid, passable
PV.PASS_EXACT |= {'twisting_vines_plant'}                 # (the vines' stem climbs as its tip does: p2/verify only knew the tip)
PV.CLIMB |= {'twisting_vines_plant'}

OX, OY, OZ = U.ORIGIN
SX, SY, SZ = U.SIZE
TOP = 121                                     # (local: the Nether's bedrock roof is at world 127)
REPL = {'air', 'water', 'lava', 'short_grass', 'fern', 'dead_bush', 'fire', 'soul_fire', 'snow', 'vine', 'glow_lichen', 'light', 'structure_void',
        'void_air', 'cave_air', 'bubble_column', 'warped_roots', 'nether_sprouts', 'crimson_roots', 'hanging_roots', 'tall_grass', 'seagrass'}
TAGS = {'bm:grap_pass': REPL, 'minecraft:replaceable': REPL, 'minecraft:air': {'air', 'void_air', 'cave_air'}, 'bm:u_contain': {'lava', 'gravel'}}
bn = lambda st: st.split(':', 1)[-1].split('[', 1)[0]


# ------------------------------------------------------------------ terrains: local (x, y, z) -> block, outside the template
def blobs(seed, boxes, n, r=(2, 4)):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x1, y1, z1, x2, y2, z2 = rnd.choice(boxes)
        out.append((rnd.uniform(x1, x2), rnd.uniform(y1, y2), rnd.uniform(z1, z2), rnd.uniform(*r)))
    return out


def in_blobs(bl, x, y, z):
    return any((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 <= rr * rr for a, b, c, rr in bl)


def T_solid(x, y, z):
    return 'minecraft:netherrack'


_PK = blobs(1, [(216, 64, 166, 272, 112, 222), (186, 64, 216, 242, 112, 272), (264, 70, 186, 330, 92, 202), (205, 70, 264, 222, 92, 330)], 220)
_PK_CAVES = [(306, 82, 194, 16), (213, 82, 306, 16)]


def T_pockets(x, y, z):
    """solid rock, lava pockets all through where the forecourts and roads go; a cave out east and one out south"""
    for a, b, c, r in _PK_CAVES:
        d = (x - a) ** 2 + ((y - b) * 1.6) ** 2 + (z - c) ** 2
        if d <= r * r: return 'minecraft:air'
    return 'minecraft:lava' if in_blobs(_PK, x, y, z) else 'minecraft:netherrack'


def T_lake(x, y, z):
    """a lava lake under and round the east forecourt, a lava ceiling-pool over the south one; caves far out"""
    if 230 <= x <= 300 and 58 <= y <= 78 and 160 <= z <= 232: return 'minecraft:lava'
    if 186 <= x <= 245 and 104 <= y <= 112 and 226 <= z <= 270: return 'minecraft:lava'
    for a, b, c, r in ((356, 84, 194, 14), (213, 84, 356, 14)):
        if (x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 <= r * r: return 'minecraft:air'
    return 'minecraft:netherrack'


def T_open(x, y, z):
    """one vast open cavern: the lava sea below (world y 31), nothing above it"""
    if y <= 20: return 'minecraft:netherrack'
    if y <= 25: return 'minecraft:lava'
    return 'minecraft:air'


def T_noise(x, y, z):
    v = (math.sin(x * 0.11) + math.sin(z * 0.13 + 1.3) + math.sin(y * 0.17 + x * 0.05) + 0.6 * math.sin((x + z) * 0.07)) / 3.6
    if v > 0.18: return 'minecraft:lava' if y <= 25 else 'minecraft:air'
    if v < -0.55 and y > 40: return 'minecraft:lava'                          # lava seams in the rock
    return 'minecraft:netherrack'


def T_falls(x, y, z):
    """an open cave in front of the east mouth with lava falls pouring from its roof onto where the forecourt goes"""
    if 226 <= x <= 300 and 74 <= y <= 100 and 150 <= z <= 240:
        if (x % 11 == 3 and z % 9 == 4) and y >= 90: return 'minecraft:lava'
        return 'minecraft:air'
    if y > 100 and 220 <= x <= 300 and 150 <= z <= 240 and (x + z) % 7 == 0: return 'minecraft:lava'
    return 'minecraft:netherrack'


def T_deep(x, y, z):
    """great caves out east and south whose floors lie 20 and more under the roads: the landings' climbs"""
    for a, b, c, r in ((308, 66, 194, 20), (213, 66, 308, 20)):
        if (x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 <= r * r: return 'minecraft:air'
    return 'minecraft:netherrack'


TERRAINS = {'pockets': (T_pockets, [(306, 82, 194), (213, 82, 306)]), 'lake': (T_lake, [(356, 84, 194), (213, 84, 356)]),
            'open': (T_open, [(300, 26, 300)]), 'noise': (T_noise, None), 'falls': (T_falls, [(260, 74, 230)]),
            'deep': (T_deep, [(300, 60, 194), (213, 60, 300)]), 'solid': (T_solid, None)}


# ------------------------------------------------------------------ the world and the interpreter
class World:
    def __init__(self, tmpl, terrain):
        self.t, self.ter, self.set_, self.carved, self.markers, self.score = tmpl, terrain, {}, set(), [], {}

    def get(self, p):
        if p in self.set_: return self.set_[p]
        x, y, z = p
        if y < 0 or y > TOP: return 'minecraft:bedrock'
        if 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ and p in self.t: return self.t[p]
        return self.ter(x, y, z)

    def put(self, p, st):
        if self.get(p) == st: return False
        self.set_[p] = st
        return True


def match(st, flt):
    if flt.startswith('#'): return bn(st) in TAGS[flt[1:]]
    return bn(st) == bn(flt) and ('[' not in flt or st == flt)


def norm(b):
    return b if ':' in b.split('[')[0] else 'minecraft:' + b


class Interp:
    def __init__(self, W, funcs):
        self.W, self.F, self.n = W, funcs, 0

    def coord(self, tok, base):
        if tok.startswith('~'): return base + (float(tok[1:]) if len(tok) > 1 else 0.0)
        return float(tok)

    def pos(self, toks, ctx):
        return tuple(self.coord(t, c) for t, c in zip(toks, ctx))

    def blk(self, p):                               # world -> local block cell
        return (math.floor(p[0]) - OX, math.floor(p[1]) - OY, math.floor(p[2]) - OZ)

    def fn(self, name, ctx):
        for line in self.F[name]:
            r = self.line(line, ctx)
            if r is not None: return r
        return None

    def line(self, line, ctx):
        """None, or ('ret', value) when a return was hit"""
        self.n += 1
        toks = line.split(' ')
        res = self.cmd(toks, ctx)
        return res if isinstance(res, tuple) else None

    def cmd(self, t, ctx):
        """runs; returns an int result, or ('ret', v) for a return"""
        k = t[0]
        if k == 'execute': return self.execute(t[1:], ctx)
        if k == 'return':
            if t[1] == 'run':
                r = self.cmd(t[2:], ctx)
                return ('ret', r[1] if isinstance(r, tuple) else r)
            return ('ret', int(t[1]))
        if k == 'function':
            r = self.fn(t[1].split(':', 1)[1], ctx)
            return r[1] if r else 0
        if k == 'fill': return self.fill(t[1:], ctx)
        if k == 'setblock':
            p = self.blk(self.pos(t[1:4], ctx)); return int(self.W.put(p, norm(t[4])))
        if k == 'scoreboard':
            op, who, obj = t[2:5]
            key = (who, obj); S = self.W.score
            if op == 'set': S[key] = int(t[5])
            elif op == 'add': S[key] = S.get(key, 0) + int(t[5])
            elif op == 'remove': S[key] = S.get(key, 0) - int(t[5])
            elif op == 'operation':
                o, src = t[5], (t[6], t[7]); a, b = S.get(key, 0), S.get(src, 0)
                S[key] = {'=': b, '+=': a + b, '-=': a - b, '%=': a % b if b else a, '*=': a * b}[o]
            return 1
        if k == 'summon':
            p = self.pos(t[2:5], ctx); self.W.markers.append((p, ' '.join(t[5:]))); return 1
        if k == 'kill': return 1
        raise ValueError('interp: no ' + ' '.join(t)[:120])

    def execute(self, t, ctx):
        i, store = 0, None
        while i < len(t):
            s = t[i]
            if s == 'in': i += 2
            elif s == 'positioned': ctx = self.pos(t[i + 1:i + 4], ctx); i += 4
            elif s == 'store':
                store = (t[i + 1], t[i + 3], t[i + 4]); i += 5
            elif s in ('if', 'unless'):
                want = s == 'if'
                if t[i + 1] == 'score':
                    v = self.W.score.get((t[i + 2], t[i + 3]), None)
                    m = t[i + 5]; lo, _, hi = m.partition('..') if '..' in m else (m, '', m)
                    ok = v is not None and (lo == '' or v >= int(lo)) and (hi == '' or v <= int(hi))
                    i += 6
                elif t[i + 1] == 'block':
                    p = self.blk(self.pos(t[i + 2:i + 5], ctx)); ok = match(self.W.get(p), t[i + 5]); i += 6
                else: raise ValueError('interp: if ' + t[i + 1])
                if ok != want: return 0 if store is None else self.store(store, 0)
            elif s == 'run':
                r = self.cmd(t[i + 1:], ctx)
                if isinstance(r, tuple): return r
                return r if store is None else self.store(store, r)
            else: raise ValueError('interp: execute ' + s)
        return 1

    def store(self, st, v):
        kind, who, obj = st
        self.W.score[(who, obj)] = (v if kind == 'result' else int(bool(v)))
        return v

    def fill(self, t, ctx):
        a, b = self.blk(self.pos(t[0:3], ctx)), self.blk(self.pos(t[3:6], ctx))
        block = norm(t[6]); rest = t[7:]
        flt = rest[1] if rest[:1] == ['replace'] else None
        vol = (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1) * (abs(a[2] - b[2]) + 1)
        if vol > R.LIMIT: raise ValueError(f'fill over the block limit ({vol}): {" ".join(t)}')
        n = 0
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                    p = (x, y, z)
                    if flt and not match(self.W.get(p), flt): continue
                    if self.W.put(p, block):
                        n += 1
                        if block == 'minecraft:air' and flt is None: self.W.carved.add(p)
        return n


# ------------------------------------------------------------------ the checks
class Walk(Grid):
    """the Grid on the world, out to the roads' reach (never in through the shut Hidden Gate: it is crying obsidian)"""
    def __init__(self, Wd):
        class FB: pass
        fb = FB(); fb.b = Wd; fb.size = (SX + R.MAXB + 200, TOP, SZ + R.MAXB + 200)
        super().__init__(fb, outside='solid')

    def st(self, x, y, z):
        return self.B.b.get((x, y, z))

    def stand(self, x, y, z):
        if x < 150 or z < 140: return False
        return super().stand(x, y, z)


def floor_under(Wd, x, y, z):
    for yy in range(y, 0, -1):
        if passable(Wd.get((x, yy, z))) and passable(Wd.get((x, yy + 1, z))) and not passable(Wd.get((x, yy - 1, z))) and bn(Wd.get((x, yy - 1, z))) != 'lava':
            return (x, yy, z)
    return None


def run(name, tmpl):
    ter, caves = TERRAINS[name]
    Wd = World(tmpl, ter)
    funcs = {}
    roads = R.lines(lambda n, l: funcs.__setitem__(n, l))
    funcs['_roads'] = [re.sub(r'^execute in minecraft:the_nether run ', '', l) for l in roads]
    I = Interp(Wd, funcs)
    t0 = time.time()
    I.fn('_roads', (0.0, 0.0, 0.0))
    errs, notes = [], []
    changed = [p for p in Wd.set_ if 0 <= p[0] < SX and 0 <= p[1] < SY and 0 <= p[2] < SZ and p in tmpl]
    if changed: errs.append(f'the approach changed {len(changed)} of the template\'s own cells, e.g. {changed[:3]}')
    sc = Wd.score
    ends = [(p, tg) for p, tg in Wd.markers if 'bm.uroadend' in tg]
    for k in R.WAYS:
        notes.append(f'{k} road: {sc.get(("#ubore_" + k, "bm.p2"))} slices, open air: {sc.get(("#ubopen_" + k, "bm.p2"))}')
    G = Walk(Wd)
    gate = (UC.SEAM[0] + 5, UC.SEAM[1], UC.SEAM[2])                               # (the landing before the gate)
    reach = G.bfs([gate])
    if UC.OUTER not in reach: errs.append(f'the court (OUTER {UC.OUTER}, where the Summons points) is not walkable from the gate')
    for p, tg in ends:
        c = (math.floor(p[0]) - OX, math.floor(p[1]) - OY, math.floor(p[2]) - OZ)
        if c not in reach: errs.append(f'a road end {c} ({tg}) cannot be walked to from the gate')
    opened = [k for k in R.WAYS if sc.get(('#ubopen_' + k, 'bm.p2')) in (1, 2)]
    if caves is not None or name != 'solid':
        if not opened: errs.append('neither road broke into open air')
    # from the terrain's own open air, to the gate
    starts = []
    for c in (caves or []):
        f = floor_under(Wd, *c)
        if f: starts.append(f)
    if name == 'noise':                                  # (a floor in open air beyond each road's end)
        for p, tg in ends:
            c = (math.floor(p[0]) - OX, math.floor(p[1]) - OY, math.floor(p[2]) - OZ)
            k = tg.split('bm.uroad_')[1][0]
            d = (1, 0) if R.WAYS[k]['ax'] == 'x' else (0, 1)
            f = floor_under(Wd, c[0] + d[0] * 8, c[1] + 4, c[2] + d[1] * 8)
            if f: starts.append(f)
    for s_ in starts:
        back = G.bfs([s_])
        if gate not in back and (gate[0], gate[1], gate[2]) not in back:
            errs.append(f'from open air at {s_} the walk does not reach the Hidden Gate')
        else: notes.append(f'from open air at {s_}: the gate is reached')
    if name in ('pockets', 'lake', 'falls') and not starts: errs.append('no open-air start found in the terrain')
    # lava touching what was cut
    leak = []
    for p in Wd.carved:
        if not passable(Wd.get(p)): continue
        for q in ((p[0] + 1, p[1], p[2]), (p[0] - 1, p[1], p[2]), (p[0], p[1], p[2] + 1), (p[0], p[1], p[2] - 1), (p[0], p[1] + 1, p[2])):
            if bn(Wd.get(q)) == 'lava' and not (0 <= q[0] < SX and 0 <= q[2] < SZ and q in tmpl): leak.append(q)
    if leak: errs.append(f'lava beside or above {len(set(leak))} cut cells, e.g. {sorted(set(leak))[:4]}')
    notes.append(f'{len(Wd.carved)} cells cut, {I.n} commands, {len(reach)} cells walkable from the gate ({time.time() - t0:.0f}s)')
    return errs, notes


def static(B):
    """what holds whatever the terrain: the court's air never borders a cell the template leaves to the Nether (lava there could
    pour in), and no lava or gravel of the template's own lies in a forecourt's shell (its fill turns them to blackstone)"""
    errs = []
    N = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1))
    v = {q for p in B.outside if B.b.get(p, '').endswith(':air') for d in N for q in [(p[0] + d[0], p[1] + d[1], p[2] + d[2])]
         if q not in B.b and 0 <= q[0] < SX and 0 <= q[1] < SY and 0 <= q[2] < SZ}
    if v: errs.append(f'the court\'s air borders {len(v)} cells left to the Nether, e.g. {sorted(v)[:3]}')
    for k, c in R.WAYS.items():
        x1, y1, z1, x2, y2, z2 = c['box']; S = R.SHELL
        own = [p for p, st in B.b.items() if x1 - S <= p[0] <= x2 + S and y1 - S - 1 <= p[1] <= y2 + S and z1 - S <= p[2] <= z2 + S and bn(st) in TAGS[R.CONTAIN]]
        if own: errs.append(f'{k} forecourt: its shell would turn {len(own)} of the template\'s own lava/gravel to blackstone, e.g. {own[:3]}')
    return errs


if __name__ == '__main__':
    want = [a for a in sys.argv[1:] if not a.startswith('-')] or list(TERRAINS)
    B = UC.build()
    tmpl = B.b
    bad = 0
    se = static(B)
    print(f'static: {len(se)} errors'); [print('    ', e) for e in se]; bad += len(se)
    for name in want:
        errs, notes = run(name, tmpl)
        exp = name == 'solid'
        if exp:          # (solid rock all round: nowhere open to reach - the roads run their length; that is the report, not a failure)
            errs = [e for e in errs if 'open air' not in e]
        print(f'{name}: {len(errs)} errors')
        for e in errs: print('    ', e)
        for n_ in notes: print('    .', n_)
        bad += len(errs)
    sys.exit(1 if bad else 0)
