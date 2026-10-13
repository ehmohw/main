"""2.71 puzzle data, every piece checked here: the Spire's ladder and switch routes (each jump makeable, none that skips a
step), colour squares and picture grids with exactly one answer, minefields a careful digger can cross without guessing,
carving models that can be carved, banners whose layers all overlap (so the order shows)."""
import itertools
import math
import random

# ===================================================================== THE SPIRE (tops = the height you stand at)
GOAL = {(x, z): 14 for x in range(10, 15) for z in range(10, 15)}
GOAL.update({(x, 12): 14 for x in range(15, 21)})
GOAL.update({(x, z): 14 for x in range(21, 24) for z in range(10, 15)})
START = [(x, z, 4) for x in range(1, 4) for z in range(10, 15)]


def reach_gen(a, b):
    """generous - could a good jumper get from a to b at all?"""
    d = math.hypot(a[0] - b[0], a[1] - b[1]); dy = b[2] - a[2]
    if dy >= 2: return False
    if dy == 1: return d <= 4.4
    if dy == 0: return d <= 5.4
    return d <= 6 + 0.7 * (-dy - 1)


def intended(a, b, kind='jump'):
    d = math.hypot(a[0] - b[0], a[1] - b[1]); dy = b[2] - a[2]
    if kind == 'grab': return d <= 3.01 and -1 <= dy <= 1
    return dy <= 1 and (d <= 3.01 if dy == 1 else d <= 4.01)


def low_ceiling_ok(tops, name):
    for a in tops:
        for b in tops:
            if a != b and abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1 and b[2] > a[2]:
                assert b[2] - a[2] >= 4, (name, 'a block hangs low over another', a, b)


# ---- B: THE LADDER SPIRE - posts with ladders up their sides; level jumps between
LADDERS = [  # (ladder x, z, facing, lowest feet y, highest ladder block y, the post (x, z, top))
    (5, 9, 'south', 5, 6, (5, 8, 7)),
    (13, 4, 'south', 7, 9, (13, 3, 10)),
    (19, 9, 'west', 10, 12, (20, 9, 13))]
LJUMPS = [[(7, 5, 7), (10, 4, 7)], [(16, 4, 10), (19, 6, 10)]]       # the blocks between ladders 1-2 and 2-3
BCHECK = LADDERS[1][5]                                              # the checkpoint: the second post's top


def _ladder_route():
    r = [('jump', START)]
    for k, (x, z, f, y0, y1, post) in enumerate(LADDERS):
        r.append(('grab', [(x, z, y) for y in range(y0, y1 + 2)] + [post]))
        if k < len(LJUMPS): r += [('jump', [n]) for n in LJUMPS[k]]
    return r


def check_route(route, name):
    idx = {}
    for i, (_k, nodes) in enumerate(route):
        for n in nodes: idx.setdefault(n, i)
    for i in range(1, len(route)):
        kind, nodes = route[i]
        assert any(intended(p, nodes[0], kind) for p in route[i - 1][1]), (name, 'move', i, nodes[0])
    assert any(intended(n, (x, z, t)) for n in route[-1][1] for (x, z), t in GOAL.items()), (name, 'no way off the last step')
    for a in idx:
        for b in idx:
            assert not (idx[b] > idx[a] + 1 and reach_gen(a, b)), (name, 'a shortcut', a, b)
        if idx[a] < len(route) - 1:
            assert not any(reach_gen(a, (x, z, t)) for (x, z), t in GOAL.items()), (name, 'off early', a)
    for s in START:
        assert not any(idx[b] > 1 and reach_gen(s, b) for b in idx), (name, 'from the start')


LROUTE = _ladder_route()
check_route(LROUTE, 'ladder spire')
low_ceiling_ok([n for k in LJUMPS for n in k] + [L[5] for L in LADDERS], 'ladder spire')


# ---- C: THE SWITCH SPIRE - red and blue blocks; a switch post's button swaps which colour is solid
def _ring():
    return [(8, z) for z in range(8, 17)] + [(x, 16) for x in range(9, 17)] + [(16, z) for z in range(15, 7, -1)] + [(x, 8) for x in range(15, 8, -1)]


SPLAN = [('r', [(0, 1), (3, 0), (3, 1)]), ('p', [(2, 1)]), ('b', [(3, 0), (3, 1), (2, 0)]), ('p', [(3, 1)]),
         ('r', [(3, 0), (2, 1), (3, 0)]), ('p', [(3, 1)]), ('b', [(3, 0), (2, 1)])]


def _switch_route():
    R = _ring()
    nodes = [(5, 12, 5, 'p')]
    i, top = R.index((8, 12)), 5
    for col, steps in SPLAN:
        for st, dy in steps:
            i += st; top += dy
            nodes.append((*R[i % len(R)], top, col))
    return nodes


SROUTE_C = _switch_route()
CCHECK = [n for n in SROUTE_C if n[3] == 'p'][2]          # the checkpoint: the middle switch post


def _check_switch():
    rc = SROUTE_C
    prev = START
    for n in rc:
        assert any(intended(p, n[:3]) for p in prev), ('switch spire move', n)
        prev = [n[:3]]
    assert any(intended(prev[0], (x, z, t)) for (x, z), t in GOAL.items()), 'switch spire: no way off'
    for state in 'rb':
        keep = [(k, n[:3]) for k, n in enumerate(rc) if n[3] in ('p', state)]
        for ka, a in keep:
            for kb, b in keep:
                if kb > ka + 1 and reach_gen(a, b):
                    assert all(x[3] == state for x in rc[ka + 1:kb]), ('switch spire: a jump past a switch or the other colour', state, a, b)
            if ka < len(rc) - 1:
                assert not any(reach_gen(a, (x, z, t)) for (x, z), t in GOAL.items()), ('switch spire: off early', a)
        for s in START:
            assert not any(kb > 1 and reach_gen(s, b) for kb, b in keep), ('switch spire: from the start', state)
    low_ceiling_ok([n[:3] for n in rc], 'switch spire')


_check_switch()


# ===================================================================== THE MASON: colour squares (4x4, one of each colour in every row and column)
def latin_squares(n=4):
    out = []
    for perm_rows in itertools.permutations(itertools.permutations(range(n)), n):
        if all(len({r[c] for r in perm_rows}) == n for c in range(n)):
            out.append(perm_rows)
    return out


ALL_LS = latin_squares()


def squares(seed=7101):
    rng = random.Random(seed)
    GIVENS = {1: 8, 2: 7, 3: 6, 4: 6, 5: 5}
    out = {}
    for t, ng in GIVENS.items():
        L = []
        while len(L) < 4:
            sol = rng.choice(ALL_LS)
            cells = [(r, c) for r in range(4) for c in range(4)]
            rng.shuffle(cells)
            giv = sorted(cells[:ng])
            fits = [s for s in ALL_LS if all(s[r][c] == sol[r][c] for r, c in giv)]
            if len(fits) == 1: L.append((sol, giv))
        out[t] = L
    return out


SQUARES = squares()


# ===================================================================== THE MASON: picture grids (5x5, a clue per row and column)
def runs(line):
    out, n = [], 0
    for v in line:
        if v: n += 1
        elif n: out.append(n); n = 0
    if n: out.append(n)
    return out or [0]


def nonograms(seed=7102, k=8):
    rng = random.Random(seed)
    rows_by_clue = {}
    for bits in itertools.product((0, 1), repeat=5):
        rows_by_clue.setdefault(tuple(runs(bits)), []).append(bits)
    out = []
    while len(out) < k:
        g = [tuple(1 if rng.random() < 0.52 else 0 for _ in range(5)) for _ in range(5)]
        n = sum(map(sum, g))
        if not 10 <= n <= 16: continue
        rc = [tuple(runs(r)) for r in g]; cc = [tuple(runs([g[r][c] for r in range(5)])) for c in range(5)]
        if sum(1 for c in rc + cc if c == (0,)) > 1: continue
        sols = 0
        for rows in itertools.product(*(rows_by_clue[c] for c in rc)):
            if all(tuple(runs([rows[r][c] for r in range(5)])) == cc[c] for c in range(5)):
                sols += 1
                if sols > 1: break
        if sols == 1 and g not in [o[0] for o in out]:
            out.append((g, rc, cc))
    return out


PICTURES = nonograms()


# ===================================================================== THE DIG: minefields (x 9..15, z 2..22; the first column is dug already)
FX, FZ = range(9, 16), range(2, 23)


def _nbrs(x, z):
    return [(x + a, z + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if (a or b) and (x + a) in FX and (z + b) in FZ]


def _solve(mines):
    """what a careful digger can know: start with column 9 open; reveal what must be safe, mark what must be mines"""
    num = {c: sum(n in mines for n in _nbrs(*c)) for c in itertools.product(FX, FZ)}
    rev = {(9, z) for z in FZ}; mk = set()
    changed = True
    while changed:
        changed = False
        cons = []
        for c in rev:
            U = [n for n in _nbrs(*c) if n not in rev and n not in mk]
            m = num[c] - sum(n in mk for n in _nbrs(*c))
            if U: cons.append((frozenset(U), m))
        for U, m in cons:
            if m == 0:
                rev |= U; changed = True
            elif m == len(U):
                mk |= U; changed = True
        if changed: continue
        for (U1, m1), (U2, m2) in itertools.permutations(cons, 2):
            if U1 < U2:
                D = U2 - U1
                if m2 - m1 == 0: rev |= D; changed = True
                elif m2 - m1 == len(D): mk |= D; changed = True
        assert not (rev & mines), 'the solver dug a mine'
    return rev, num


def _crossable(rev):
    seen = {(9, z) for z in FZ}; todo = list(seen)
    while todo:
        x, z = todo.pop()
        if x == 15: return True
        for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
            if n in rev and n not in seen: seen.add(n); todo.append(n)
    return False


def minefields(seed=7103, k=6, density=0.2):
    rng = random.Random(seed)
    out = []
    while len(out) < k:
        cells = [(x, z) for x in FX if x > 9 for z in FZ]
        mines = {c for c in cells if rng.random() < density}
        if not 20 <= len(mines) <= 30: continue
        rev, num = _solve(mines)
        if not _crossable(rev): continue
        if len(rev) > 0.75 * len(list(itertools.product(FX, FZ))): continue      # (not a walkover)
        out.append((sorted(mines), num))
    return out


MINEFIELDS = minefields()


# ===================================================================== THE DIG: carving models (3x3x3 - what stays)
def models(seed=7104, k=8):
    rng = random.Random(seed)
    cube = list(itertools.product(range(3), range(3), range(3)))       # (x, y, z)
    def nb(c): return [(c[0] + a, c[1] + b, c[2] + d) for a, b, d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    out = []
    while len(out) < k:
        keep = {c for c in cube if rng.random() < 0.55}
        if not 11 <= len(keep) <= 17: continue
        if not any(c[1] == 0 for c in keep): continue
        start = next(iter(keep)); seen = {start}; todo = [start]
        while todo:
            for n in nb(todo.pop()):
                if n in keep and n not in seen: seen.add(n); todo.append(n)
        if seen != keep: continue
        gone = set(cube) - keep
        out_ = {c for c in gone if any(not all(0 <= v <= 2 for v in n) for n in nb(c))}       # (on the outside)
        todo = list(out_)
        while todo:
            for n in nb(todo.pop()):
                if n in gone and n not in out_: out_.add(n); todo.append(n)
        if out_ != gone: continue          # (every block carved away can be reached from outside)
        if sorted(keep) in [o for o in out]: continue
        out.append(sorted(keep))
    return out


MODELS = models()


# ===================================================================== THE BENCH: banners (every two layers overlap, so the order shows)
BPATS = ['stripe_left', 'stripe_right', 'stripe_top', 'stripe_bottom', 'stripe_center', 'stripe_middle', 'stripe_downright', 'stripe_downleft', 'border']
APART = {frozenset(p) for p in [('stripe_left', 'stripe_right'), ('stripe_top', 'stripe_bottom'), ('stripe_center', 'stripe_left'), ('stripe_center', 'stripe_right'),
                                 ('stripe_middle', 'stripe_top'), ('stripe_middle', 'stripe_bottom')]}
BCOLS = ['red', 'blue', 'yellow', 'black', 'lime', 'orange', 'purple', 'light_blue']


def banners(seed=7105):
    rng = random.Random(seed)
    layers = {1: 1, 2: 2, 3: 2, 4: 3, 5: 3}
    out = {}
    for t, n in layers.items():
        L = []
        while len(L) < 4:
            pats = rng.sample(BPATS, n); cols = rng.sample(BCOLS, n)
            if any(frozenset((a, b)) in APART for a, b in itertools.combinations(pats, 2)): continue
            d = list(zip(pats, cols))
            if d not in L: L.append(d)
        out[t] = L
    return out


BANNERS = banners()
