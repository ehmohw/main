"""2.72 puzzle data, every piece checked here: library shelves (each riddle and sum has exactly one answer), pipe grids
(solvable, and not solved to begin with), grapple chasms (the hook count is exactly enough - no jump-only way, no cheaper
way), minecart tracks (every rail joined to the next)."""
import itertools
import math
import random

# ===================================================================== THE LIBRARY: 36 books on the north wall, three shelves of twelve
LCOLS = [3.75 + 1.5 * i for i in range(12)]    # x of each book (12 a shelf)
LROWS = [7, 6, 5]                              # y of each shelf, top first (2.82: three, all within reach with no jump - Leaden)
PER = len(LCOLS)
LSLOTS = [(x, y) for y in LROWS for x in LCOLS]
WORDS = ['Ledgers', 'Moths', 'Tides', 'Brass', 'Owls', 'Ashes', 'Lanterns', 'Ravens', 'Wax', 'Thorns', 'Ciphers', 'Bones', 'Salt', 'Echoes',
         'Glass', 'Embers', 'Saints', 'Rust', 'Silk', 'Comets', 'Wolves', 'Velvet', 'Mirrors', 'Dust', 'Hymns', 'Orchids', 'Coins', 'Riddles',
         'Storms', 'Ink', 'Keys', 'Masks', 'Pearls', 'Shadows', 'Locks', 'Sparrows', 'Ivory', 'Clocks', 'Hollows', 'Gold', 'Maps', 'Candles',
         'Herons', 'Smoke', 'Tin', 'Rubies', 'Crowns', 'Frost', 'Rivers', 'Beetles']
RIDDLES = [('I have a face and two hands, but no arms or legs.', 'CLOCK'), ('The more you take, the more you leave behind.', 'STEPS'),
           ('I have many teeth, but I never bite.', 'COMB'), ('The more I dry, the wetter I get.', 'TOWEL'),
           ('I have keys, but I open no locks.', 'PIANO'), ('I run and run, but I never walk.', 'RIVER'),
           ('You can catch me, but you can\'t throw me.', 'COLD'), ('I go up and down, but I never move.', 'STAIR')]
LETTERS = 'ABCDEFGHIJKLMNOPRSTUVWY'


def library(seed=7201):
    rng = random.Random(seed)
    A, B, C = [], [], []
    for _ in range(8):                         # A: the catalogue - find the books by their titles
        w = rng.sample(WORDS, 36)
        A.append((w, rng.sample(range(36), 4)))
    for riddle, ans in RIDDLES:                # B: the acrostic - pull the books that spell the answer, in order
        letters = list(ans) + [rng.choice(LETTERS) for _ in range(36 - len(ans))]
        rng.shuffle(letters)
        assert all(letters.count(ch) >= ans.count(ch) for ch in ans)
        B.append((riddle, ans, letters))
    while len(C) < 8:                          # C: the sum - three numbered books, one from each of three shelves, add up to N
        slots = rng.sample(range(36), 12)
        nums = {s: rng.randint(1, 19) for s in slots}
        triples = [t for t in itertools.combinations(slots, 3) if len({s // PER for s in t}) == 3]
        sums = {}
        for t in triples: sums.setdefault(sum(nums[s] for s in t), []).append(t)
        ok = [n for n, ts in sums.items() if len(ts) == 1 and 20 <= n <= 45]
        if not ok: continue
        n = rng.choice(ok)
        C.append((nums, n, sums[n][0]))
    return A, B, C


LIB_A, LIB_B, LIB_C = library()


# ===================================================================== THE PIPES: a 5x5 grid of pieces, water in at the west, out at the east
N_, E_, S_, W_ = 1, 2, 4, 8
DIRS = {N_: (-1, 0), E_: (0, 1), S_: (1, 0), W_: (0, -1)}         # (row, col) steps; row = z (north is -), col = x
OPP = {N_: S_, S_: N_, E_: W_, W_: E_}


def rot_mask(m, r):
    for _ in range(r % 4):
        m = ((m << 1) | (m >> 3)) & 15                          # N->E->S->W
    return m


BASE = {0: N_ | S_, 1: N_ | E_}                                 # 0 straight, 1 corner


def mask(t, r): return rot_mask(BASE[t], r)


def wet(grid, rs):
    """the cells the water reaches (grid: {(r, c): (type, rot)}); it comes in at (rs, 0) from the west"""
    if not mask(*grid[(rs, 0)]) & W_: return set()
    seen = {(rs, 0)}; todo = [(rs, 0)]
    while todo:
        r, c = todo.pop(); m = mask(*grid[(r, c)])
        for d, (dr, dc) in DIRS.items():
            n = (r + dr, c + dc)
            if m & d and n in grid and n not in seen and mask(*grid[n]) & OPP[d]:
                seen.add(n); todo.append(n)
    return seen


def solved(grid, rs, rd, gauges=()):
    w = wet(grid, rs)
    return (rd, 4) in w and mask(*grid[(rd, 4)]) & E_ and all(g in w for g in gauges)


def _path(rng):
    while True:
        rs, rd = rng.randrange(5), rng.randrange(5)
        p = [(rs, 0)]
        for _ in range(60):
            r, c = p[-1]
            if c == 4 and r == rd: return rs, rd, p
            opts = [(r + dr, c + dc) for dr, dc in ((0, 1), (0, 1), (1, 0), (-1, 0)) if 0 <= r + dr < 5 and 0 <= c + dc < 5 and (r + dr, c + dc) not in p]
            if not opts: break
            p.append(rng.choice(opts))


def _pieces(p):
    out = {}
    for i, (r, c) in enumerate(p):
        a = W_ if i == 0 else next(d for d, (dr, dc) in DIRS.items() if (r + dr, c + dc) == p[i - 1])
        b = E_ if i == len(p) - 1 else next(d for d, (dr, dc) in DIRS.items() if (r + dr, c + dc) == p[i + 1])
        want = a | b
        out[(r, c)] = next((t, k) for t in (0, 1) for k in range(4) if mask(t, k) == want)
    return out


def pipes(seed=7202, k=6):
    rng = random.Random(seed)
    A, B, C = [], [], []
    while len(A) < k or len(B) < k or len(C) < k:
        rs, rd, p = _path(rng)
        if not 7 <= len(p) <= 13: continue
        sol = _pieces(p)
        full = {(r, c): sol.get((r, c), (rng.randrange(2), rng.randrange(4))) for r in range(5) for c in range(5)}
        assert solved(full, rs, rd)
        scr = {cell: (t, rng.randrange(4)) for cell, (t, _r) in full.items()}
        if solved(scr, rs, rd): continue
        if len(A) < k: A.append((rs, rd, scr, full))
        if len(C) < k:
            g = rng.sample(p[2:-2], 2) if len(p) > 6 else []
            if len(g) == 2: C.append((rs, rd, scr, full, g))
        if len(B) < k:
            cells = list(full); vals = [full[c] for c in cells]; rng.shuffle(vals)
            sh = dict(zip(cells, vals))
            if not solved(sh, rs, rd): B.append((rs, rd, sh, full))
    return A, B, C


PIPE_A, PIPE_B, PIPE_C = pipes()


# ===================================================================== THE GRAPPLE: a chasm of islands; the hook pulls you to a lamp, you drop to what's under it
EYE = 1.62
ISL_TOP = 4                                    # islands stand at y 4 (feet)
LAMP_Y = 9                                     # the lamps (target blocks) hang at y 9
HOOK_REACH = 8.0                               # (the room's hook reaches 9 blocks: a margin both ways)
HOOK_FAR = 9.6


def box(cx, cz, h=1.0):
    """an island as its footprint (x0, x1, z0, z1) in world units; a 2x2 island of blocks c-1, c spans c-1 .. c+1"""
    return (cx - h, cx + h, cz - h, cz + h)


START_BOX = (1.0, 4.0, 10.0, 15.0)             # the start ledge (blocks x 1..3, z 10..14)
GOAL_BOX = (23.0, 24.0, 10.0, 15.0)            # the far ledge (blocks x 23, z 10..14)


def _gap(a, b):
    dx = max(0.0, max(a[0], b[0]) - min(a[1], b[1])); dz = max(0.0, max(a[2], b[2]) - min(a[3], b[3]))
    return math.hypot(dx, dz)


def _jump(a, b, far=False):
    """intended: a gap of 3 or less; generous (could anyone at all): under 4.7"""
    return _gap(a, b) <= (4.7 if far else 3.0)


def _hook(a, b, reach=HOOK_REACH):
    """from the near edge of a, can the hook reach the lamp over the middle of b?"""
    cx, cz = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
    dx = max(0.0, a[0] - cx, cx - a[1]); dz = max(0.0, a[2] - cz, cz - a[3])
    return math.sqrt(dx * dx + dz * dz + (LAMP_Y + 0.5 - ISL_TOP - EYE) ** 2) <= reach


def min_hooks(nodes, start, goal, far=False):
    reach = HOOK_FAR if far else HOOK_REACH
    best = {start: 0}; todo = [(0, start)]
    while todo:
        todo.sort(key=lambda e: e[0]); c, n = todo.pop(0)
        if n == goal: return c
        for m in nodes:
            if m == n or m == 'start': continue
            for cost, ok in ((0, _jump(nodes[n], nodes[m], far)), (1, _hook(nodes[n], nodes[m], reach))):
                if ok and best.get(m, 99) > c + cost:
                    best[m] = c + cost; todo.append((c + cost, m))
    return 99


def chasms(seed=7203, k=4):
    """2x2 islands in the pit (blocks x 5..20, z 2..22): the fewest hooks across is the hook count you get - and no cheaper way
    even for a jumper who clears more than anyone can"""
    rng = random.Random(seed)
    out = []
    while len(out) < k:
        n = rng.randint(6, 8)
        isl = []
        while len(isl) < n:
            p = (rng.randint(6, 20), rng.randint(3, 22))
            if all(abs(p[0] - q[0]) >= 4 or abs(p[1] - q[1]) >= 4 for q in isl): isl.append(p)
        nodes = {'start': START_BOX, 'goal': GOAL_BOX}
        nodes.update({i: box(*p) for i, p in enumerate(isl)})
        h = min_hooks(nodes, 'start', 'goal')
        if h not in (2, 3) or min_hooks(nodes, 'start', 'goal', True) != h: continue
        out.append((isl, h))
    return out


CHASMS = chasms()
LANES = [10, 17]                               # B: the swinging lamps - two islands (centres) across the room; the lamps swing along z
SWING = [-3, 0, 3]


def _check_lanes():
    nodes = {'start': START_BOX, 'goal': GOAL_BOX}
    nodes.update({i: box(x, 12) for i, x in enumerate(LANES)})
    order = ['start', 0, 1, 'goal']
    for a, b in zip(order, order[1:]):
        assert not _jump(nodes[a], nodes[b], True), ('lanes: a gap you could jump', a, b)
        assert _hook(nodes[a], nodes[b]), ('lanes: a lamp out of reach', a, b)
    for a in order:
        for b in order:
            if order.index(b) > order.index(a) + 1: assert not _hook(nodes[a], nodes[b], HOOK_FAR), ('lanes: a skip', a, b)


_check_lanes()
BELLS = [(16, 6, 6), (16, 9, 9), (16, 5, 15), (16, 8, 18)]     # C: (x, y, z) of the four bells across the gap
BELL_COLS = ['red', 'blue', 'yellow', 'lime']


# ===================================================================== THE MINECART RUN: rails (x, z) from the start station to the end
def _line(*pts):
    out = []
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        dx = (x1 > x0) - (x1 < x0); dz = (z1 > z0) - (z1 < z0)
        x, z = x0, z0
        while (x, z) != (x1, z1):
            out.append((x, z)); x += dx; z += dz
    out.append(pts[-1])
    return out


def shape(prev, cur, nxt):
    ds = set()
    for o in (prev, nxt):
        if o is None: continue
        ds.add({(0, -1): 'north', (0, 1): 'south', (1, 0): 'east', (-1, 0): 'west'}[(o[0] - cur[0], o[1] - cur[1])])
    if len(ds) == 1: ds |= {{'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}[next(iter(ds))]}
    if ds == {'north', 'south'}: return 'north_south'
    if ds == {'east', 'west'}: return 'east_west'
    return '_'.join(sorted(ds, key=lambda d: ('north', 'south').index(d) if d in ('north', 'south') else 2 + ('east', 'west').index(d)))


def rails(path):
    out = []
    for i, c in enumerate(path):
        out.append((c, shape(path[i - 1] if i else None, c, path[i + 1] if i + 1 < len(path) else None)))
    return out


# A: the rail shooter - one long winding run past the targets
RUN_A = _line((3, 12), (6, 12), (6, 4), (12, 4), (12, 20), (18, 20), (18, 12), (21, 12))
TARGETS_A = [(4, 6, 9), (9, 6, 2), (14, 6, 7), (10, 7, 12), (14, 6, 17), (16, 7, 22), (20, 6, 17), (16, 6, 10)]
# B: the switch yard - three sets of points; one way through, the rest end in buffers
RUN_B_MAIN = _line((3, 12), (16, 12))          # (the main line: J1 at x 7, J2 at x 12; it ends at a buffer at 16)
RUN_B_SOUTH = _line((12, 13), (12, 18), (20, 18), (20, 13), (21, 13))      # (from J2, south and round to the end)
SPUR_J1 = _line((7, 11), (7, 6))               # (from J1, north to a dead end)
SPUR_J3 = _line((16, 19), (16, 22))            # (from J3 on the south loop, south to a dead end)
JUNCTIONS = {1: ((7, 12), 'east_west', 'north_west'), 2: ((12, 12), 'east_west', 'south_west'), 3: ((16, 18), 'east_west', 'south_west')}
B_RIGHT = {1: 0, 2: 1, 3: 0}                   # (lever up = the second shape)
B_ENDS = [(16, 12), (7, 6), (16, 22)]          # the buffers (dead ends)
# C: the drawbridges - three gaps; a button by the track closes each one for a moment
RUN_C = _line((3, 12), (14, 12), (14, 5), (20, 5), (20, 12), (21, 12))
GAPS_C = [[(9, 12), (10, 12)], [(14, 8), (14, 7)], [(20, 9), (20, 10)]]
BUTTONS_C = [(6, 5, 11), (13, 5, 11), (21, 5, 7)]  # (x, y, z) - beside the track, before each gap (on a post)


def _check_track(path, name):
    for a, b in zip(path, path[1:]):
        assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1, (name, 'rails not joined', a, b)
    assert len(set(path)) == len(path), (name, 'rails cross')


for _p, _n in ((RUN_A, 'A'), (RUN_B_MAIN, 'B main'), (RUN_B_SOUTH, 'B south'), (SPUR_J1, 'J1 spur'), (SPUR_J3, 'J3 spur'), (RUN_C, 'C')):
    _check_track(_p, _n)
for _g in GAPS_C:
    assert all(c in RUN_C for c in _g)


# ===================================================================== the Apothecary's brews: (what to call it, the item, the potion id, riddle)
BREW_A = {2: [('a Potion of Swiftness', 'potion', 'swiftness'), ('a Potion of Fire Resistance', 'potion', 'fire_resistance'), ('a Potion of Night Vision', 'potion', 'night_vision')],
          3: [('a Potion of Strength', 'potion', 'strength'), ('a Potion of Leaping', 'potion', 'leaping'), ('a Potion of Water Breathing', 'potion', 'water_breathing')],
          4: [('a Potion of Regeneration', 'potion', 'regeneration'), ('a Potion of Healing', 'potion', 'healing'), ('a Potion of Slow Falling', 'potion', 'slow_falling')],
          5: [('a Potion of Poison', 'potion', 'poison'), ('a Potion of Strength', 'potion', 'strength'), ('a Potion of Regeneration', 'potion', 'regeneration')]}
RIDDLE_B = {'swiftness': 'Drink me and you\'ll outrun the wind.', 'fire_resistance': 'Drink me and walk through flame unburnt.',
            'night_vision': 'Drink me and the dark has no secrets.', 'water_breathing': 'Drink me and breathe where the fish do.',
            'leaping': 'Drink me and the walls are no higher than steps.', 'strength': 'Drink me and hit like a falling anvil.',
            'regeneration': 'Drink me and your wounds close themselves.', 'slow_falling': 'Drink me and drift down like a feather.',
            'healing': 'Drink me and be mended at once.', 'poison': 'Give me to your enemy, not your friend.'}
BREW_B = {2: ['swiftness', 'fire_resistance', 'night_vision'], 3: ['water_breathing', 'leaping', 'strength'], 4: ['regeneration', 'slow_falling', 'healing'],
          5: ['poison', 'water_breathing', 'leaping']}
BREW_C = {2: [('a long Potion of Fire Resistance', 'potion', 'long_fire_resistance'), ('a Splash Potion of Swiftness', 'splash_potion', 'swiftness')],
          3: [('a Potion of Invisibility', 'potion', 'invisibility'), ('a strong Potion of Strength', 'potion', 'strong_strength')],
          4: [('a Splash Potion of Healing II', 'splash_potion', 'strong_healing'), ('a Potion of Slowness', 'potion', 'slowness')],
          5: [('a long Splash Potion of Invisibility', 'splash_potion', 'long_invisibility'), ('a Splash Potion of Harming II', 'splash_potion', 'strong_harming')]}
INGR = {'swiftness': ['sugar'], 'fire_resistance': ['magma_cream'], 'night_vision': ['golden_carrot'], 'strength': ['blaze_powder'],
        'leaping': ['rabbit_foot'], 'water_breathing': ['pufferfish'], 'regeneration': ['ghast_tear'], 'healing': ['glistering_melon_slice'],
        'slow_falling': ['phantom_membrane'], 'poison': ['spider_eye'],
        'long_fire_resistance': ['magma_cream', 'redstone'], 'invisibility': ['golden_carrot', 'fermented_spider_eye'],
        'strong_strength': ['blaze_powder', 'glowstone_dust'], 'strong_healing': ['glistering_melon_slice', 'glowstone_dust'],
        'slowness': ['sugar', 'fermented_spider_eye'], 'long_invisibility': ['golden_carrot', 'fermented_spider_eye', 'redstone'],
        'strong_harming': ['glistering_melon_slice', 'fermented_spider_eye', 'glowstone_dust']}
DECOY = ['sugar', 'magma_cream', 'golden_carrot', 'rabbit_foot', 'pufferfish', 'ghast_tear', 'spider_eye', 'phantom_membrane', 'glistering_melon_slice']


