#!/usr/bin/env python3
"""Static audit of the 2.85d fight rooms (phase184): for every room template, at every tier's materials -
  * the doorways: the entry (x=0) open, the exit (x=24) barred by build (p70/solved opens it), both 3 wide and 4 high;
  * a walkable path from the entry to the exit for a player (2 high, ladders climbable, water wadeable);
  * every foe's spawn (read off the generated wave functions): not inside a block, landing somewhere a player can reach
    (stand next to, or swing at from within reach), with room for its size.
Run from bm_build after a build: python3 tools/room_audit.py"""
import os, re, sys
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gen_dp  # noqa: F401  (every phase, in the build's order)
import phase184 as P
import phase75_rooms as R5

OUT = os.environ.get('BM_OUT', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out_p2'))
FN = os.path.join(OUT, 'BlackMarket_DP/data/bm/function/p184')

THROUGH = ('air', 'cave_air', 'water', 'ladder', 'cobweb', 'seagrass', 'carpet', 'iron_chain', 'lantern', 'end_rod', 'amethyst_cluster')
FLOAT = ('water', 'seagrass', 'sea_pickle')                       # (wade/swim: stand in it)


def name(st):
    return (st or 'minecraft:air').split('[')[0].replace('minecraft:', '')


def through(st):
    n = name(st)
    return any(n == t or n.endswith('_' + t) for t in THROUGH) or n in FLOAT


def solid(st):
    return not through(st)


def audit(k, t):
    b = P.ROOMS[k]()
    R5.retheme(b, t)
    sx, sy, sz = b.size
    g = lambda x, y, z: b.get(x, y, z) if (0 <= x < sx and 0 <= y < sy and 0 <= z < sz) else 'minecraft:stone'
    errs = []
    # ---- the doorways
    for y in range(4, 8):
        for z in (11, 12, 13):
            if name(g(0, y, z)) != 'air': errs.append(f'entry blocked at y{y} z{z}: {g(0, y, z)}')
            if name(g(24, y, z)) != 'iron_bars': errs.append(f'exit not barred at y{y} z{z}: {g(24, y, z)}')
            if not through(g(1, y, z)) or not through(g(23, y, z)): errs.append(f'doorway step blocked at y{y} z{z}')
    # ---- where a player can stand, and get to from the entry
    def stand(x, y, z):
        if not (through(g(x, y, z)) and through(g(x, y + 1, z))): return False
        below = g(x, y - 1, z)
        return solid(below) or name(g(x, y, z)) == 'ladder' or name(g(x, y, z)) in FLOAT or name(below) in FLOAT
    start = (1, 4, 12)
    seen, q = {start}, deque([start])
    while q:
        x, y, z = q.popleft()
        nxt = []
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (1 <= nx <= 23 and 1 <= nz <= 23): continue
            for ny in (y, y + 1):                                  # level, or a block up (headroom over the jump)
                if ny == y + 1 and not through(g(x, y + 2, z)): continue
                if stand(nx, ny, nz): nxt.append((nx, ny, nz))
            if through(g(nx, y, nz)) and through(g(nx, y + 1, nz)):  # off an edge: fall to where it lands
                fy = y
                while fy > 0 and not stand(nx, fy, nz): fy -= 1
                if fy > 0 and fy < y: nxt.append((nx, fy, nz))
        if name(g(x, y, z)) == 'ladder' or name(g(x, y + 1, z)) == 'ladder':
            if stand(x, y + 1, z) or name(g(x, y + 1, z)) == 'ladder': nxt.append((x, y + 1, z))
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):      # off the top of a ladder onto a floor
                if stand(x + dx, y + 1, z + dz): nxt.append((x + dx, y + 1, z + dz))
        for p in nxt:
            if p not in seen: seen.add(p); q.append(p)
    if not any(p[0] == 23 and 11 <= p[2] <= 13 and p[1] == 4 for p in seen):
        errs.append('no walkable path from the entry to the exit')
    reach = lambda x, y, z: any(abs(px - x) <= 2 and abs(pz - z) <= 2 and -2 <= y - py <= 3 for (px, py, pz) in seen)
    # ---- every foe's spawn (from the build's wave functions)
    spawns = []
    for f in sorted(os.listdir(os.path.join(FN, k))):
        if not re.fullmatch(r'w\d+\.mcfunction', f): continue
        for line in open(os.path.join(FN, k, f)):
            m = re.search(r'positioned (\S+) (\S+) (\S+) run (summon minecraft:(\w+)|function bm:p70/(guard|captain))\b', line)
            if not m: continue
            v = [0 if c == '~' else float(c[1:]) for c in m.group(1, 2, 3)]
            ty = m.group(5) or m.group(6)
            spawns.append((f, ty, int(12 + v[0]), int(4 + v[1]), int(12 + v[2])))
    big = {'spider': 1, 'hoglin': 1, 'piglin_brute': 0, 'guardian': 0, 'captain': 0}
    for f, ty, x, y, z in spawns:
        if ty == 'vex': continue                                   # (flies, through walls - kept to a short life)
        if not (through(g(x, y, z)) and through(g(x, y + 1, z))):
            errs.append(f'{f} {ty} spawns inside a block at {x},{y},{z}: {g(x, y, z)} / {g(x, y + 1, z)}'); continue
        ly = y
        while ly > 1 and not (solid(g(x, ly - 1, z)) or name(g(x, ly, z)) in FLOAT): ly -= 1
        if not reach(x, ly, z): errs.append(f'{f} {ty} lands out of reach at {x},{ly},{z}')
        r = big.get(ty, 0)
        if r and any(solid(g(x + dx, ly, z + dz)) or solid(g(x + dx, ly + 1, z + dz)) for dx in range(-r, r + 1) for dz in range(-r, r + 1)):
            errs.append(f'{f} {ty} (big) cramped at {x},{ly},{z}')
    return errs, len(spawns)


if __name__ == '__main__':
    bad = 0
    for k in P.ROOMS:
        for t in P.TIERS[k]:
            errs, n = audit(k, t)
            bad += len(errs)
            print(f'{k:10s} T{t}: {n:3d} spawns  ' + ('ok' if not errs else f'{len(errs)} problem(s)'))
            for e in dict.fromkeys(errs): print('    ' + e)
    print(f'\n{bad} problem(s)')
    sys.exit(1 if bad else 0)
