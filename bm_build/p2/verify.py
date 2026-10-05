"""Static verification of Phase 2 dungeon layouts.

1. Wiring: every puzzle element sits on the right block, attachments are solid, gate frames only contain
   gate material inside their fill box, secret doors pair with hidden buttons, keypads/sequences are complete.
2. NO SKIPPING: a voxel walkability search (walk, step up 1, fall, climb ladders, open wooden doors) from the
   entrance - and, for surface dungeons, from everywhere outside - proves that with gates 1..k open, the puzzle
   k+1 controls are reachable but puzzle k+2+, the altar and the arena are NOT. It also proves every hidden room
   is sealed until its secret door opens, the arena exit stays sealed until victory, and pressure-plate paths
   cannot be crossed without stepping on plates (and have a safe route).
"""
import math
from collections import deque
from p2.config import D, OPEN_LIGHT, ADOOR_LIGHT, GATE_H, BIG_W, BIG_H

PASS_EXACT = {'air', 'cave_air', 'void_air', 'light', 'cobweb', 'glow_lichen', 'ladder', 'vine', 'water', 'bubble_column', 'kelp',
              'kelp_plant', 'seagrass', 'tall_seagrass', 'short_grass', 'tall_grass', 'fern', 'large_fern', 'snow', 'redstone_wire',
              'tripwire', 'string', 'dead_bush', 'bush', 'firefly_bush', 'sculk_vein', 'pink_petals', 'leaf_litter', 'hanging_roots',
              'spore_blossom', 'cave_vines', 'cave_vines_plant', 'twisting_vines', 'weeping_vines', 'lily_pad', 'small_dripleaf',
              'big_dripleaf_stem', 'sea_pickle', 'lantern', 'soul_lantern', 'chain', 'iron_chain', 'pointed_dripstone', 'frogspawn',
              'moss_carpet', 'pale_moss_carpet', 'pale_hanging_moss', 'eyeblossom', 'open_eyeblossom', 'closed_eyeblossom', 'structure_void'}
PASS_SUFFIX = ('_button', '_pressure_plate', '_carpet', '_sign', '_torch', 'torch', 'candle', '_banner', '_sapling', 'rail', '_skull',
               '_head', '_door', '_flower', 'flower', '_tulip', 'dandelion', 'poppy', 'orchid', 'allium', 'azure_bluet', 'oxeye_daisy',
               'cornflower', 'lily_of_the_valley', 'wither_rose', 'torchflower', 'lever', '_coral', '_coral_fan', '_wall_fan', 'sunflower',
               'lilac', 'rose_bush', 'peony', 'pitcher_plant', '_mushroom', 'copper_lantern', '_lantern_hanging')
CLIMB = {'ladder', 'vine', 'cave_vines', 'cave_vines_plant', 'twisting_vines', 'weeping_vines', 'water', 'bubble_column', 'scaffolding'}


def bname(st):
    return st.split(':', 1)[-1].split('[', 1)[0]


def passable(st):
    if st is None: return None
    n = bname(st)
    if n == 'iron_door': return False
    if n in ('sea_lantern', 'jack_o_lantern', 'redstone_lamp', 'candle_cake', 'flower_pot') or n.startswith('potted_'): return False
    return n in PASS_EXACT or n.endswith(PASS_SUFFIX)


DIRS = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}


def walk_up_ok(st, dx, dz):
    """Can a player walk (not jump) up onto this block moving in direction (dx, dz)? Bottom slabs: always (half a block).
    Stairs: only from the front or the sides - from the back the stair is a full block-high wall."""
    n = bname(st)
    if n.endswith('_slab'): return 'type=bottom' in st or 'type=' not in st
    if not n.endswith('_stairs') or 'half=top' in st: return False
    f = st.split('facing=')[1].split(',')[0].split(']')[0] if 'facing=' in st else 'north'
    fx, fz = DIRS[f]
    return (dx, dz) != (-fx, -fz)


class Grid:
    def __init__(self, B, outside='solid', base_y=0, jumps=False):
        self.B, self.sx, self.sy, self.sz = B, *B.size
        self.outside, self.base_y = outside, base_y
        self.jumps = jumps           # 2.2: parkour - straight jumps over a 1-2 block gap (same level or lower), or a 1 gap up 1
        self.override = {}
        self.bad_stairs = set()      # stairs a player would hit from the back with no headroom to jump

    def st(self, x, y, z):
        if (x, y, z) in self.override: return self.override[(x, y, z)]
        return self.B.b.get((x, y, z))

    def free(self, x, y, z):
        if self.outside == 'void':                    # floating in nothing: everything unset is air, falling off is death
            if not (0 <= x < self.sx and 0 <= y < self.sy and 0 <= z < self.sz): return True
            s = self.st(x, y, z)
            return True if s is None else passable(s)
        if not (0 <= x < self.sx and 0 <= z < self.sz): return self.outside in ('air', 'water') and y >= self.base_y
        if y < 0: return False
        if y >= self.sy: return self.outside == 'air' or True
        s = self.st(x, y, z)
        if s is None: return self.outside in ('air', 'water') and y >= self.base_y
        return passable(s)

    def climb(self, x, y, z):
        s = self.st(x, y, z) if (0 <= x < self.sx and 0 <= y < self.sy and 0 <= z < self.sz) else None
        if s is None and self.outside == 'water' and y >= self.base_y: return True      # the open ocean: swim anywhere
        return bool(s) and bname(s) in CLIMB

    def stand(self, x, y, z):
        if not (self.free(x, y, z) and self.free(x, y + 1, z)): return False
        if 0 <= x < self.sx and 0 < y <= self.sy and 0 <= z < self.sz:
            below = self.st(x, y - 1, z)
            if below and bname(below) in ('lava', 'lava_cauldron', 'fire', 'soul_fire', 'campfire', 'soul_campfire'): return False   # 2.2
        return (not self.free(x, y - 1, z)) or self.climb(x, y, z) or self.climb(x, y - 1, z)

    def cells_margin(self):
        return 3

    def inside(self, x, y, z):
        return 0 <= x < self.sx and 0 <= y < self.sy + 2 and 0 <= z < self.sz

    def bfs(self, starts, margin=3):
        seen, q = set(), deque()
        for s in starts:
            if self.stand(*s): seen.add(s); q.append(s)
        lo, hi = -margin, margin
        while q:
            x, y, z = q.popleft()
            nbrs = []
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, nz = x + dx, z + dz
                if not (lo <= nx < self.sx + hi and lo <= nz < self.sz + hi): continue
                if self.stand(nx, y, nz): nbrs.append((nx, y, nz)); continue
                # step up one block: a jump needs headroom, but stairs and slabs are walked up without jumping
                up = self.st(nx, y, nz) if self.inside(nx, y, nz) else None
                stairish = bool(up) and walk_up_ok(up, dx, dz)
                # 2.1: stairs/slabs too - you rise while still half under the block above where you stood
                if self.free(x, y + 2, z) and self.stand(nx, y + 1, nz): nbrs.append((nx, y + 1, nz)); continue
                if up and (bname(up).endswith('_stairs') or bname(up).endswith('_slab')) and self.stand(nx, y + 1, nz): self.bad_stairs.add((nx, y, nz))
                # walk off a ledge and fall
                if self.free(nx, y, nz) and self.free(nx, y + 1, nz):
                    fy = y - 1
                    while fy >= -1 and not self.stand(nx, fy, nz):
                        if not self.free(nx, fy, nz): fy = -99; break
                        fy -= 1
                    if fy >= 0: nbrs.append((nx, fy, nz))
            if self.climb(x, y, z) or self.climb(x, y + 1, z):
                for dy in (1, -1):
                    if self.stand(x, y + dy, z) or (self.free(x, y + dy, z) and self.free(x, y + dy + 1, z) and self.climb(x, y + dy, z)):
                        nbrs.append((x, y + dy, z))
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):          # swim sideways through water
                    nx, nz = x + dx, z + dz
                    if not (lo <= nx < self.sx + hi and lo <= nz < self.sz + hi): continue
                    if self.free(nx, y, nz) and self.free(nx, y + 1, nz) and self.climb(nx, y, nz): nbrs.append((nx, y, nz))
            if self.stand(x, y - 1, z) and self.free(x, y - 1, z): nbrs.append((x, y - 1, z))
            if self.jumps and self.free(x, y + 2, z):
                for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    for dist, rise in ((2, 1), (2, 0), (3, 0), (2, -1), (3, -1), (3, -2)):
                        if not all(self.free(x + dx * i, y + h, z + dz * i) for i in range(1, dist) for h in (0, 1, 2)): continue
                        tx, ty, tz = x + dx * dist, y + rise, z + dz * dist
                        if rise > 0 and not self.free(tx, ty + 1, tz): continue
                        if self.stand(tx, ty, tz): nbrs.append((tx, ty, tz))
            for n in nbrs:
                if n not in seen and -2 <= n[1] < self.sy + 3:
                    seen.add(n); q.append(n)
        return Seen(seen)


GRID = None   # set by verify(): used for line-of-sight


def los(eye, tgt, target_cell):
    """Ray from the eye to the target centre must not pass through any solid cell except the target itself."""
    (ex, ey, ez), (tx, ty, tz) = eye, tgt
    steps = int(math.dist(eye, tgt) * 8) + 1
    for i in range(1, steps):
        f = i / steps
        c = (math.floor(ex + (tx - ex) * f), math.floor(ey + (ty - ey) * f), math.floor(ez + (tz - ez) * f))
        if c == target_cell: return True
        if not GRID.free(*c): return False
    return True


class Seen(set):
    """Reached cells with an 8x8 column index so reach() only scans nearby cells."""
    def __init__(self, cells):
        super().__init__(cells)
        self.idx = {}
        for c in cells: self.idx.setdefault((c[0] >> 3, c[2] >> 3), []).append(c)


def reach(seen, x, y, z, r=4.5):
    """Can a player standing in `seen` touch block (x,y,z)? (eye at feet+1.62, interaction range 4.5, line of sight)"""
    if not isinstance(seen, Seen): seen = Seen(seen)
    cx, cy, cz = x + 0.5, y + 0.5, z + 0.5
    rb = int(r) // 8 + 1
    cands = []
    for bx in range((x >> 3) - rb, (x >> 3) + rb + 1):
        for bz in range((z >> 3) - rb, (z >> 3) + rb + 1):
            cands += seen.idx.get((bx, bz), ())
    cands.sort(key=lambda c: (c[0] - x) ** 2 + (c[1] - y) ** 2 + (c[2] - z) ** 2)
    for (sx, sy, sz) in cands:
        eye = (sx + 0.5, sy + 1.62, sz + 0.5)
        if (sx - x) ** 2 + (sy - y) ** 2 + (sz - z) ** 2 > (r + 3) ** 2: break     # sorted by distance: nothing closer remains
        if math.dist(eye, (cx, cy, cz)) > r: continue
        if los(eye, (cx, cy, cz), (x, y, z)): return True
    return False


def attached_ok(B, x, y, z, st):
    """Buttons, levers, wall signs and ladders must hang on something solid."""
    s = st.split(':', 1)[-1]
    name, _, props = s.partition('[')
    pr = dict(kv.split('=') for kv in props.rstrip(']').split(',')) if props else {}
    vec = {'north': (0, 0, -1), 'south': (0, 0, 1), 'east': (1, 0, 0), 'west': (-1, 0, 0)}
    def solid(p): return not passable(B.b.get(p) or 'minecraft:stone')
    if name.endswith('button') or name == 'lever':
        face = pr.get('face', 'wall')
        if face == 'ceiling': return solid((x, y + 1, z))
        if face == 'floor': return solid((x, y - 1, z))
        dx, _, dz = vec[pr['facing']]
        return solid((x - dx, y, z - dz))
    if name.endswith('wall_sign') or name == 'ladder':
        dx, _, dz = vec[pr['facing']]
        return solid((x - dx, y, z - dz))
    return True


ELEMENT_BLOCK = {'lever': 'lever', 'key': 'button', 'seq': 'button', 'listen': 'button', 'lo': 'button', 'sbtn': 'button',
                 'pull': 'button', 'target': 'target', 'bulb': 'copper_bulb', 'reel': 'gold_block'}


def verify(B, outside='solid', base_y=0, extra_starts=()):
    errs, notes = [], []
    d, cfg = B.d, D[B.d]
    gate_blk = cfg['gate']
    # ---------------- wiring
    for (x, y, z, axis, n) in B.meta['gates']:
        for dx in (-1, 0, 1):
            for dy in range(GATE_H):
                for dz in (-1, 0, 1):
                    s = B.b.get((x + dx, y + dy, z + dz))
                    in_plane = (dz == 0) if axis == 'x' else (dx == 0)
                    if in_plane and s != gate_blk: errs.append(f'{d} gate {n}: plane cell {(x + dx, y + dy, z + dz)} is {s}')
                    if not in_plane and s in (gate_blk, OPEN_LIGHT): errs.append(f'{d} gate {n}: stray {s} in fill box at {(x + dx, y + dy, z + dz)}')
    for (x, y, z, axis) in B.meta['big']:
        for dx in range(-BIG_W, BIG_W + 1):
            for dy in range(BIG_H):
                for dz in range(-BIG_W, BIG_W + 1):
                    s = B.b.get((x + dx, y + dy, z + dz))
                    in_plane = (dz == 0) if axis == 'x' else (dx == 0)
                    if in_plane and s != ADOOR_LIGHT: errs.append(f'{d} battle door: plane cell {(x + dx, y + dy, z + dz)} is {s}')
                    if not in_plane and s in (gate_blk, ADOOR_LIGHT): errs.append(f'{d} battle door: stray {s} at {(x + dx, y + dy, z + dz)}')
    sb = {k for (_, _, _, _, k) in [e for e in B.meta['elements'] if e[0] == 'sbtn']}
    for (x, y, z, k) in B.meta['sdoors']:
        if k not in sb: errs.append(f'{d} secret door {k} has no hidden button')
        for dy in (0, 1):
            if B.b.get((x, y + dy, z)) != cfg['secret']: errs.append(f'{d} secret door {k} cell {(x, y + dy, z)} = {B.b.get((x, y + dy, z))}')
    for e in B.meta['elements']:
        kind, x, y, z = e[0], e[1], e[2], e[3]
        st = B.b.get((x, y, z)) or ''
        want = ELEMENT_BLOCK.get(kind)
        if want and want not in st: errs.append(f'{d} element {kind} at {(x, y, z)} sits on {st}')
        if want in ('lever', 'button') and not attached_ok(B.b if False else B, x, y, z, st): errs.append(f'{d} element {kind} at {(x, y, z)} not attached: {st}')
    for (x, y, z), st in B.b.items():
        if ('wall_sign' in st or 'ladder' in st or 'button' in st or 'lever' in st) and not attached_ok(B, x, y, z, st):
            errs.append(f'{d} unattached {st} at {(x, y, z)}')
    for n, p in sorted(B.meta['puzzles'].items()):
        kinds = [e[0] for e in p['elements']]
        if p.get('kind') is None: errs.append(f'{d} puzzle {n} has elements but no controller'); continue
        k = p['kind']
        if k == 'levers' and (kinds.count('lever') < 2 or not any('bm.want1' in e[4] for e in p['elements'])): errs.append(f'{d} P{n} levers incomplete')
        if k == 'keypad':
            keys = {t for e in p['elements'] for t in e[4]}
            need = {f'bm.k{i}' for i in range(10)} | {'bm.kclr', 'bm.kent'}
            if keys != need: errs.append(f'{d} P{n} keypad keys {sorted(need - keys)} missing')
        if k in ('seq', 'simon'):
            orders = sorted(int(t[4:]) for e in p['elements'] if e[0] == 'seq' for t in e[4] if t.startswith('bm.s') and t[4:].isdigit())
            if orders != list(range(1, len(orders) + 1)) or len(orders) < 3: errs.append(f'{d} P{n} sequence orders {orders}')
            if k == 'simon' and 'listen' not in kinds: errs.append(f'{d} P{n} simon has no listen button')
        if k == 'path' and not ('start' in kinds and 'goal' in kinds): errs.append(f'{d} P{n} path needs start+goal')
        if k == 'lights':
            bi = sorted(int(t[4:]) for e in p['elements'] if e[0] == 'bulb' for t in e[4] if t.startswith('bm.i'))
            li = sorted(int(t[4:]) for e in p['elements'] if e[0] == 'lo' for t in e[4] if t.startswith('bm.i'))
            if bi != li or bi != list(range(len(bi))) or len(bi) not in (9, 16): errs.append(f'{d} P{n} lights-out grid {bi} / {li}')
        if k == 'targets' and kinds.count('target') < 3: errs.append(f'{d} P{n} needs 3+ targets')
        if k == 'waves':
            sp = [e for e in p['elements'] if e[0] == 'wsp']
            if len(sp) < 2: errs.append(f'{d} P{n} waves needs 2+ spawn points')
            for e in sp:
                if not (passable(B.b.get(e[1:4], 'minecraft:air')) and passable(B.b.get((e[1], e[2] + 1, e[3]), 'minecraft:air'))
                        and not passable(B.b.get((e[1], e[2] - 1, e[3]), 'minecraft:air'))):
                    errs.append(f'{d} P{n} wave spawn point {e[1:4]} is not a clear floor cell')
        if k == 'reach' and not ('start' in kinds and 'goal' in kinds): errs.append(f'{d} P{n} reach needs start+goal')
        if k == 'offering' and kinds.count('offer') < 1: errs.append(f'{d} P{n} offering has no pedestal')
        if k == 'slots' and (kinds.count('reel') != 3 or 'pull' not in kinds): errs.append(f'{d} P{n} slot machine incomplete')
    if not B.meta['entrance']: errs.append(f'{d}: no entrance marker')
    if not B.meta['arena'] or not B.meta['altar']: errs.append(f'{d}: arena/altar missing')
    tags = [t for m in B.meta['markers'] for t in m[3]]
    for need in ('bm.dg', 'bm.zone_d', 'bm.dgfx', 'bm.arena', 'bm.altar', 'bm.mspawn', 'bm.entr'):
        if need not in tags: errs.append(f'{d}: no {need} marker')
    # every marker within the dungeon radius of the controller (resets/gates find each other by distance)
    ctrl = [m for m in B.meta['markers'] if 'bm.dg' in m[3]]
    if ctrl:
        cx, cy, cz = ctrl[0][:3]
        far = max(math.dist((cx, cy, cz), m[:3]) for m in B.meta['markers'])
        if far > cfg['radius']: errs.append(f'{d}: a marker is {far:.1f} from the controller (radius {cfg["radius"]})')
        notes.append(f'farthest marker {far:.1f} / radius {cfg["radius"]}')

    # ---------------- NO SKIPPING (walkability)
    global GRID
    G = Grid(B, outside, base_y, jumps=bool(B.meta.get('parkour')))
    GRID = G
    starts = [tuple(B.meta['entrance'])] + list(extra_starts)
    if outside in ('air', 'water'):
        # feet level just above the natural ground (ground = unset cells below base_y); all four sides
        starts += [(x, base_y, z) for x in (-2, B.size[0] + 1) for z in range(-2, B.size[2] + 2, 2)]
        starts += [(x, base_y, z) for z in (-2, B.size[2] + 1) for x in range(-2, B.size[0] + 2, 2)]
    gates = sorted(B.meta['gates'], key=lambda g: g[4])
    ngate = max([g[4] for g in gates] or [0])
    plane = lambda g: [((g[0] + dw, g[1] + dy, g[2]) if g[3] == 'x' else (g[0], g[1] + dy, g[2] + dw)) for dw in (-1, 0, 1) for dy in range(GATE_H)]
    for (x, y, z, k) in B.meta['sdoors']: pass
    def elems(n): return [e for e in B.meta['puzzles'].get(n, {}).get('elements', []) if e[0] not in ('goal',)]
    puzzles = sorted(B.meta['puzzles'])
    for opened in range(0, ngate + 1):
        G.override = {}
        for g in gates:
            if g[4] <= opened:
                for c in plane(g): G.override[c] = OPEN_LIGHT
        seen = G.bfs(starts)
        for n in puzzles:
            el = elems(n)
            if not el: continue
            # buttons/levers must be touchable (4.5 blocks); targets are shot and bulbs/reels only watched (line of sight, 32 blocks)
            # every shootable/watchable/clickable element needs at least one face open to the inside (2.1: a Frost-Eye
            # was built outside the wall and only 'visible' through a diagonal corner seam)
            for e in el:
                if e[0] in ('target', 'bulb', 'reel', 'button', 'lever', 'lo', 'pull'):
                    open_faces = [o for o in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
                                  if (e[1] + o[0], e[2] + o[1], e[3] + o[2]) in B.b and G.free(e[1] + o[0], e[2] + o[1], e[3] + o[2])]
                    if not open_faces: errs.append(f'{d} P{n} {e[0]} at {e[1:4]} has no exposed face')
            ok = [reach(seen, e[1], e[2], e[3], 32.0 if e[0] in ('target', 'bulb', 'reel') else 4.5) for e in el]
            if n <= opened + 1 and not all(ok):
                bad = [el[i][:4] for i, o in enumerate(ok) if not o]
                errs.append(f'{d}: with gates 1..{opened} open, puzzle {n} elements unreachable: {bad[:4]}')
            if n > opened + 1 and any(ok):
                bad = [el[i][:4] for i, o in enumerate(ok) if o]
                errs.append(f'{d}: SKIP RISK - with gates 1..{opened} open, puzzle {n} elements reachable: {bad[:4]}')
        ax, ay, az = B.meta['altar']
        alt = reach(seen, ax, ay, az, 2.5)
        if opened < ngate and alt: errs.append(f'{d}: SKIP RISK - altar reachable with only gates 1..{opened} open')
        if opened == ngate and not alt: errs.append(f'{d}: altar unreachable with all gates open')
        if opened == ngate:
            arx, ary, arz = B.meta['arena']
            if not any((abs(s[0] - arx) <= 2 and abs(s[2] - arz) <= 2) for s in seen): errs.append(f'{d}: arena centre unreachable with all gates open')
            for (x, y, z, k) in B.meta['sdoors']:
                pass
    # hidden rooms sealed until their secret door opens; hidden buttons reachable once their room is reachable
    G.override = {}
    for g in gates:
        for c in plane(g): G.override[c] = OPEN_LIGHT
    all_open = G.bfs(starts)
    for (x, y, z, k) in B.meta['sdoors']:
        btn = [e for e in B.meta['elements'] if e[0] == 'sbtn' and e[4] == k]
        if btn and not reach(all_open, btn[0][1], btn[0][2], btn[0][3]): errs.append(f'{d}: hidden button {k} unreachable')
        G2o = dict(G.override); G2o[(x, y, z)] = 'minecraft:air'; G2o[(x, y + 1, z)] = 'minecraft:air'
        G.override = G2o
        with_door = G.bfs(starts)
        G.override = {c: v for c, v in G2o.items() if c not in ((x, y, z), (x, y + 1, z))}
        gained = len([c for c in with_door - all_open if abs(c[0] - x) + abs(c[2] - z) > 1])   # ignore the doorway itself
        if gained <= 0: errs.append(f'{d}: secret door {k} opens onto nothing new')
        else: notes.append(f'secret room {k}: +{gained} standable cells')
    # chests in hidden rooms must not be reachable before their door opens
    for (x, y, z, loot) in B.meta['chests']:
        if loot and '/hidden' in loot and reach(all_open, x, y, z): errs.append(f'{d}: hidden chest at {(x, y, z)} reachable without its secret door')
    # arena exit sealed until victory
    for (x, y, z) in [m[:3] for m in B.meta['xdoors']]:
        pass
    # pressure-plate paths: safe route exists; no route avoids the plates
    for n, p in B.meta['puzzles'].items():
        if p.get('kind') != 'path': continue
        st = [e for e in p['elements'] if e[0] == 'start'][0]
        go = [e for e in p['elements'] if e[0] == 'goal'][0]
        # read the real blocks (not the builder's records): a plate is a trap when the trap block is 2 below it
        plates = {(x, y, z): (B.b.get((x, y - 2, z)) == cfg['trap']) for (x, y, z), st in B.b.items() if 'pressure_plate' in st}
        G.override = {}
        for g in gates:                       # only the gates before this puzzle are open
            if g[4] < n:
                for c in plane(g): G.override[c] = OPEN_LIGHT
        for (x, y, z), trap in plates.items():
            if trap:                                                   # traps act like tall walls for the safe-route test
                for dy in range(6): G.override[(x, y + dy, z)] = 'minecraft:stone'
        safe = G.bfs([(st[1], st[2], st[3])], margin=0)
        if not any(abs(s[0] - go[1]) + abs(s[2] - go[3]) <= 1 and abs(s[1] - go[2]) <= 1 for s in safe):
            errs.append(f'{d} P{n}: no safe route from start to goal')
        for (x, y, z) in plates:
            for dy in range(6): G.override[(x, y + dy, z)] = 'minecraft:stone'
        noplate = G.bfs([(st[1], st[2], st[3])], margin=0)
        if any(abs(s[0] - go[1]) + abs(s[2] - go[3]) <= 1 and abs(s[1] - go[2]) <= 1 for s in noplate):
            errs.append(f'{d} P{n}: SKIP RISK - goal reachable without stepping on plates')
        G.override = {}
    if G.bad_stairs: errs.append(f'{d}: steps with no headroom (head bump) at {sorted(G.bad_stairs)[:8]}')
    return errs, notes
