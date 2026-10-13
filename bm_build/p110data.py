"""2.69: puzzle data for the vault's room variants, worked out at build time (fixed seeds, so every build is the same).
Every generator checks its puzzles have exactly one answer (asserts) - the rooms only show what's here."""
import itertools
import random

ROMAN = ['I', 'II', 'III', 'IV', 'V']


# ===================================================================== THE COMBINATION ROOM (C): the logic ledger
# levers I..V left to right as you face them; a pattern is a 5-bit mask, bit k = lever (k+1) pulled
def _lever_clues(rng):
    C = []
    for n in range(1, 5):
        C.append((f'Exactly {n} lever{"s are" if n > 1 else " is"} pulled.', lambda p, n=n: bin(p).count('1') == n, 'count'))
    for a, b in itertools.combinations(range(5), 2):
        A, Bn = ROMAN[a], ROMAN[b]
        C.append((f'Levers {A} and {Bn} are set the same way.', lambda p, a=a, b=b: ((p >> a) & 1) == ((p >> b) & 1), 'pair'))
        C.append((f'Levers {A} and {Bn} are set differently.', lambda p, a=a, b=b: ((p >> a) & 1) != ((p >> b) & 1), 'pair'))
        C.append((f'Lever {A} or lever {Bn} is pulled - or both.', lambda p, a=a, b=b: bool((p >> a) & 1) or bool((p >> b) & 1), 'or'))
    for a, b in itertools.permutations(range(5), 2):
        C.append((f'If lever {ROMAN[a]} is pulled, so is lever {ROMAN[b]}.', lambda p, a=a, b=b: not ((p >> a) & 1) or bool((p >> b) & 1), 'if'))
    for a in range(5):
        C.append((f'Lever {ROMAN[a]} is pulled.', lambda p, a=a: bool((p >> a) & 1), 'direct'))
        C.append((f'Lever {ROMAN[a]} is left alone.', lambda p, a=a: not ((p >> a) & 1), 'direct'))
    adj = lambda p: any(((p >> k) & 3) == 3 for k in range(4))
    C.append(('No two pulled levers stand side by side.', lambda p: not adj(p), 'adj'))
    C.append(('At least two pulled levers stand side by side.', lambda p: adj(p), 'adj'))
    left = lambda p: bin(p & 0b00011).count('1'); right = lambda p: bin(p & 0b11000).count('1')
    C.append(('More are pulled left of III than right of it.', lambda p: left(p) > right(p), 'side'))
    C.append(('More are pulled right of III than left of it.', lambda p: right(p) > left(p), 'side'))
    C.append(('As many are pulled left of III as right of it.', lambda p: right(p) == left(p), 'side'))
    for a, b, c in itertools.combinations(range(5), 3):
        C.append((f'At most one of levers {ROMAN[a]}, {ROMAN[b]} and {ROMAN[c]} is pulled.',
                  lambda p, a=a, b=b, c=c: ((p >> a) & 1) + ((p >> b) & 1) + ((p >> c) & 1) <= 1, 'most'))
    return C


def lever_puzzles(n=32, seed=6901):
    rng = random.Random(seed)
    C = _lever_clues(rng)
    out = []
    pats = list(range(1, 32))
    while len(out) < n:
        p = rng.choice(pats)
        for _attempt in range(200):
            cand = set(range(32)); chosen = []; direct = 0
            true = [c for c in C if c[1](p)]
            rng.shuffle(true)
            for c in true:
                if c[2] == 'direct' and direct >= 1: continue
                new = {q for q in cand if c[1](q)}
                if len(new) < len(cand):
                    chosen.append(c); cand = new
                    direct += c[2] == 'direct'
                if len(cand) == 1: break
            if cand == {p} and 3 <= len(chosen) <= 5:
                # (drop any clue the others make redundant)
                for c in list(chosen):
                    rest = [d for d in chosen if d is not c]
                    if len(rest) >= 3 and {q for q in range(32) if all(d[1](q) for d in rest)} == {p}: chosen = rest
                assert {q for q in range(32) if all(d[1](q) for d in chosen)} == {p}
                out.append((p, [c[0] for c in chosen])); break
    return out


# ===================================================================== THE WEIGHING ROOM (B): the order of the scales
SYMS = ['crown', 'key', 'coin', 'skull']


def _order_clues():
    C = []
    pos = lambda o, s: o.index(s)
    for a, b in itertools.permutations(range(4), 2):
        A, Bn = SYMS[a], SYMS[b]
        C.append((f'The {A} comes before the {Bn}.', lambda o, a=a, b=b: pos(o, a) < pos(o, b), 'before'))
        C.append((f'The {A} comes straight after the {Bn}.', lambda o, a=a, b=b: pos(o, a) == pos(o, b) + 1, 'after'))
    for a, b in itertools.combinations(range(4), 2):
        C.append((f'The {SYMS[a]} and the {SYMS[b]} are not one after the other.', lambda o, a=a, b=b: abs(pos(o, a) - pos(o, b)) != 1, 'apart'))
    for a in range(4):
        C.append((f'The {SYMS[a]} is not first.', lambda o, a=a: pos(o, a) != 0, 'not'))
        C.append((f'The {SYMS[a]} is not last.', lambda o, a=a: pos(o, a) != 3, 'not'))
        C.append((f'The {SYMS[a]} is first.', lambda o, a=a: pos(o, a) == 0, 'direct'))
        C.append((f'The {SYMS[a]} is last.', lambda o, a=a: pos(o, a) == 3, 'direct'))
    return C


def order_puzzles(seed=6902):
    rng = random.Random(seed)
    C = _order_clues()
    orders = list(itertools.permutations(range(4)))
    out = []
    for o in orders:
        best = None
        for _attempt in range(300):
            cand = set(orders); chosen = []; direct = 0
            true = [c for c in C if c[1](o)]
            rng.shuffle(true)
            for c in true:
                if c[2] == 'direct' and direct >= 1: continue
                new = {q for q in cand if c[1](q)}
                if len(new) < len(cand):
                    chosen.append(c); cand = new; direct += c[2] == 'direct'
                if len(cand) == 1: break
            if cand == {o} and (best is None or len(chosen) < len(best)) and len(chosen) >= 3:
                best = list(chosen)
        assert best and {q for q in orders if all(c[1](q) for c in best)} == {o}
        out.append((o, [c[0] for c in best]))
    return out


# ===================================================================== THE GAUNTLET (C): the mirror gauntlet
# sockets: 5 columns (x 5,9,13,17,21) by 3 rows (z 8,12,16); the beam enters column 0 from the north wall, going south
DIRS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
REFLECT = {1: {'E': 'N', 'N': 'E', 'W': 'S', 'S': 'W'}, 2: {'E': 'S', 'S': 'E', 'W': 'N', 'N': 'W'}}
NC, NR = 5, 3


def exit_of(c, r, d):
    """the exit (a wall spot) a beam leaving cell (c, r) heading d reaches"""
    if d == 'S': return f'S{c}'
    if d == 'N': return f'N{c}'
    if d == 'E': return f'E{r}'
    return f'W{r}'


def trace(grid):
    """grid[(c, r)] = 0/1/2 -> (cells passed through, the exit)"""
    c, r, d = 0, 0, 'S'
    path = []
    for _ in range(64):
        path.append((c, r))
        m = grid.get((c, r), 0)
        if m: d = REFLECT[m][d]
        dc, dr = DIRS[d]
        if not (0 <= c + dc < NC and 0 <= r + dr < NR): return path, exit_of(c, r, d)
        c, r = c + dc, r + dr
    raise AssertionError('beam loop')


RECEIVERS = [f'S{c}' for c in range(5)] + [f'N{c}' for c in range(1, 5)] + ['E0', 'E1', 'E2']


def mirror_puzzles(k, n, seed):
    """n puzzles with k turnable mirrors (and a few fixed ones): exactly one setting of the turnable mirrors lights the receiver,
    and that setting turns the beam at least four times"""
    rng = random.Random(seed)
    cells = [(c, r) for c in range(NC) for r in range(NR)]
    out = []
    while len(out) < n:
        rot = rng.sample(cells, k)
        rest = [x for x in cells if x not in rot]
        fixed = {x: rng.choice((1, 2)) for x in rng.sample(rest, rng.randint(1, 3))}
        recv = rng.choice(RECEIVERS)
        sols = []
        for bits in range(2 ** k):
            g = dict(fixed); g.update({x: 1 + ((bits >> i) & 1) for i, x in enumerate(rot)})
            path, ex = trace(g)
            if ex == recv: sols.append((bits, path))
        if len(sols) != 1: continue
        bits, path = sols[0]
        g = dict(fixed); g.update({x: 1 + ((bits >> i) & 1) for i, x in enumerate(rot)})
        turns = sum(1 for x in path if g.get(x, 0))
        used_rot = sum(1 for x in path if x in rot)
        if turns < 4 or used_rot < min(k, 3): continue
        start = [b for b in range(2 ** k) if b != bits and trace({**fixed, **{x: 1 + ((b >> i) & 1) for i, x in enumerate(rot)}})[1] != recv]
        st = rng.choice(start)
        if bin(st ^ bits).count('1') < 2: continue
        out.append({'rot': rot, 'fixed': fixed, 'recv': recv, 'sol': bits, 'start': st})
    return out


# ===================================================================== THE TILE FLOOR (B, C): a path across 6 x 5 tiles
TC, TR = 6, 5


def tile_path(rng):
    """a path from column 0 to column 5 that never turns back: a run up or down each column, then one step on; it stops at
    the first tile of column 5 (you step off onto the gold from there)"""
    r = rng.randrange(TR); path = []
    for c in range(TC):
        if c == TC - 1:
            path.append((c, r)); break
        r2 = max(0, min(TR - 1, r + rng.choice((-2, -1, -1, 0, 1, 1, 2))))
        step = 1 if r2 >= r else -1
        for rr in range(r, r2 + step, step): path.append((c, rr))
        r = r2
    return path


COLS = ['red', 'blue', 'lime', 'yellow']


def colour_puzzles(n=16, seed=6903):
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        path = tile_path(rng)
        if len(path) < 9: continue
        cyc = list(range(4)); rng.shuffle(cyc)
        col = {}
        for i, t in enumerate(path): col[t] = cyc[i % 4]
        for c in range(TC):
            for r in range(TR):
                if (c, r) not in col: col[(c, r)] = rng.randrange(4)
        # every trail that follows the colours from column 0 to column 5 (any way but back over itself)
        found = []
        def dfs(t, i, seen):
            if len(found) > 1: return
            if t[0] == TC - 1: found.append(list(seen)); return
            for dc, dr in ((1, 0), (0, 1), (0, -1), (-1, 0)):
                u = (t[0] + dc, t[1] + dr)
                if u in col and u not in seen and col[u] == cyc[(i + 1) % 4]:
                    seen.append(u); dfs(u, i + 1, seen); seen.pop()
        starts = [(0, r) for r in range(TR) if col[(0, r)] == cyc[0]]
        if len(starts) < 2: continue
        for s in starts: dfs(s, 0, [s])
        if len(found) != 1 or found[0] != path: continue
        # (decoys: at least three tiles that fit the next colour beside the trail, but lead nowhere)
        decoys = sum(1 for i, t in enumerate(path) for dc, dr in ((1, 0), (0, 1), (0, -1)) if (t[0] + dc, t[1] + dr) in col
                     and (t[0] + dc, t[1] + dr) not in path and col[(t[0] + dc, t[1] + dr)] == cyc[(i + 1) % 4])
        if decoys < 3: continue
        out.append({'path': path, 'cyc': cyc, 'col': col})
    return out


def _all_paths():
    res = []
    def rec(c, r, acc):
        if c == TC - 1: res.append(acc + [(c, r)]); return
        for r2 in range(TR):
            if abs(r2 - r) > 2: continue
            step = 1 if r2 >= r else -1
            rec(c + 1, r2, acc + [(c, rr) for rr in range(r, r2 + step, step)])
    for r in range(TR): rec(0, r, [])
    return res


def count_puzzles(n=16, seed=6904):
    rng = random.Random(seed)
    allp = _all_paths()
    sig = lambda p: (tuple(sum(1 for t in p if t[1] == r) for r in range(TR)), tuple(sum(1 for t in p if t[0] == c) for c in range(TC)))
    out = []
    while len(out) < n:
        path = tile_path(rng)
        if len(path) < 8: continue
        s = sig(path)
        cands = [p for p in allp if sig(p) == s]
        shown = []
        while len(cands) > 1 and len(shown) < 2:
            best = min((t for t in path if t not in shown), key=lambda t: sum(1 for p in cands if t in p))
            shown.append(best); cands = [p for p in cands if best in p]
        if len(cands) != 1 or cands[0] != path: continue
        out.append({'path': path, 'rows': s[0], 'cols': s[1], 'shown': shown})
    return out


# ===================================================================== THE DIAL LOCK (B): the numbered dials
DNAME = ['left', 'middle', 'right']


def dial_puzzles(n=24, seed=6906):
    """three dials, each 0-7; three or four clues pin them down"""
    rng = random.Random(seed)
    def clues(v):
        C = []
        for i, j in itertools.permutations(range(3), 2):
            A, Bn = DNAME[i].capitalize(), DNAME[j]
            C.append((f'{A} + {Bn} = {v[i] + v[j]}', lambda w, i=i, j=j, s=v[i] + v[j]: w[i] + w[j] == s))
            if v[i] - v[j] > 0: C.append((f'{A} - {Bn} = {v[i] - v[j]}', lambda w, i=i, j=j, s=v[i] - v[j]: w[i] - w[j] == s))
            if v[i] == 2 * v[j]: C.append((f'{A} is twice the {Bn}', lambda w, i=i, j=j: w[i] == 2 * w[j]))
            if v[i] > v[j]: C.append((f'{A} is more than the {Bn}', lambda w, i=i, j=j: w[i] > w[j]))
        C.append((f'All three add up to {sum(v)}', lambda w, s=sum(v): sum(w) == s))
        for i in range(3):
            C.append((f'{DNAME[i].capitalize()} is {"odd" if v[i] % 2 else "even"}', lambda w, i=i, p=v[i] % 2: w[i] % 2 == p))
        return C
    allv = list(itertools.product(range(8), repeat=3))
    out = []
    while len(out) < n:
        v = tuple(rng.randrange(8) for _ in range(3))
        if len(set(v)) < 2: continue
        C = clues(v); rng.shuffle(C)
        cand = allv; chosen = []
        for c in C:
            new = [w for w in cand if c[1](w)]
            if len(new) < len(cand): chosen.append(c); cand = new
            if len(cand) == 1: break
        if len(cand) == 1 and 3 <= len(chosen) <= 4:
            out.append((v, [c[0] for c in chosen]))
    return out


# ===================================================================== THE THREE COFFERS (B): the lying coffers
CKINDS = ['oak chest', 'copper chest', 'ender chest', 'barrel']


def liar_puzzles(n=24, seed=6907):
    """four coffers (left to right as you face them), each saying where the honest one is; exactly one of them tells the
    truth - and only one place for the honest coffer makes that so"""
    rng = random.Random(seed)
    perms = list(itertools.permutations(range(4)))
    out = []
    while len(out) < n:
        perm = rng.choice(perms)                      # perm[i] = the kind of chest at place i
        pos = {perm[i]: i for i in range(4)}
        def stmts(me):
            S = [('The honest one is me.', lambda h: h == me), ('It isn\'t me.', lambda h: h != me),
                 ('It stands right beside me.', lambda h: abs(h - me) == 1), ('It sits at one end of the row.', lambda h: h in (0, 3)),
                 ('It is somewhere to my left.', lambda h: h < me), ('It is somewhere to my right.', lambda h: h > me)]
            for k in range(4):
                if pos[k] != me:
                    S.append((f'It is the {CKINDS[k]}.', lambda h, p=pos[k]: h == p))
                    S.append((f'It isn\'t the {CKINDS[k]}.', lambda h, p=pos[k]: h != p))
            return S
        pick = [rng.choice(stmts(i)) for i in range(4)]
        good = [h for h in range(4) if sum(1 for s in pick if s[1](h)) == 1]
        if len(good) != 1: continue
        # (no giveaways: the true line isn't 'the honest one is me')
        h = good[0]
        if any(s[0] == 'The honest one is me.' and s[1](h) for s in pick): continue
        out.append({'perm': perm, 'h': h, 'say': [s[0] for s in pick]})
    return out


# ===================================================================== THE CRUMBLING RAFTERS (C): the ghost beams
def ghost_paths(n=4, seed=6908):
    """a winding path of single beams (x 3..21, z 4..20) - orthogonal steps, never touching itself sideways"""
    rng = random.Random(seed)
    out = []
    while len(out) < n:
        x, z = 3, rng.randrange(8, 17); path = [(x, z)]
        ok = True
        while x < 21:
            moves = [(1, 0), (1, 0), (0, 1), (0, -1)]
            rng.shuffle(moves)
            for dx, dz in moves:
                nx, nz = x + dx, z + dz
                if not (4 <= nz <= 20) or (nx, nz) in path: continue
                nb = [(nx + a, nz + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                if sum(1 for t in nb if t in path) != 1: continue
                if dz and len(path) >= 2 and path[-2][1] != z and abs(path[-2][1] - nz) == 2: continue
                x, z = nx, nz; path.append((x, z)); break
            else:
                ok = False; break
        turns = sum(1 for i in range(1, len(path) - 1) if (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]) != (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1]))
        if ok and turns >= 10 and 28 <= len(path) <= 44: out.append(path)
    return out
