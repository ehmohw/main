"""Live access audit (2.14): place a structure in real terrain on the local test server and prove a player can WALK
(step up one block, fall up to 20, climb ladders/vines, swim) from the surrounding surface to its entrance - no digging,
no block placing (inside a dungeon's zone you couldn't). Uses tools/rcon.py and tools/scan.py.

    python3 tools/access.py brood 5000 5000          # place bm:p2_brood near (5000, 5000) and test it
    python3 tools/access.py all                       # every dungeon at its built-in test sites
"""
import os, re, sys, time
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from rcon import Rcon
from scan import scan
from p2.verify import passable as vpass, bname, CLIMB

R = Rcon()
SITES = {   # (x, z) test spots in varied terrain on the test seed; tide needs open ocean
    'brood': [(5000, 5000), (-3000, 4200), (7400, -2600)], 'lucky': [(5200, -4800), (-6000, -1500), (2600, 7400)],
    'frost': [(5600, 2600), (-4400, -4400), (8800, 800)], 'hex': [(-2200, 6600), (4400, -7000), (-7600, 3000)],
    'keep': [(3000, 9000), (-9000, -6000), (9600, 6400)], 'tide': [(6000, 6000), (-6128, -6128), (288, -960)]}
FALL = 20


def cmd(c): return R.cmd(c)


def wait_loaded(x, z):
    for _ in range(90):
        if 'passed' in cmd(f'execute if loaded {x} 0 {z}'): return True
        time.sleep(1)
    return False


def marker_pos(tag, d, x, z, r=160):
    dt = f',tag=bm.d_{d}' if d else ''
    out = cmd(f'execute as @e[type=minecraft:marker,tag={tag}{dt},x={x - r},y=-64,z={z - r},dx={2 * r},dy=400,dz={2 * r},limit=1] run data get entity @s Pos')
    m = re.search(r'\[(-?[\d.]+)d, (-?[\d.]+)d, (-?[\d.]+)d\]', out)
    return tuple(float(v) for v in m.groups()) if m else None


def solid(st): return st is not None and not vpass(st) and 'water' not in st and 'lava' not in st


def walkable_model(B):
    def st(c): return B.get(c)          # None = air (scan drops air)
    def free(c):
        s = st(c)
        return s is None or vpass(s) or 'water' in s
    def liquid(c):
        s = st(c); return s is not None and ('water' in s or 'bubble_column' in s)
    def climb(c):
        s = st(c); return s is not None and bname(s) in CLIMB
    def node(c):
        x, y, z = c
        if not (free(c) and free((x, y + 1, z))): return False
        below = st((x, y - 1, z))
        return solid(below) or liquid(c) or climb(c) or (below is not None and bname(below).endswith(('_slab', '_stairs')))
    return st, free, liquid, climb, node


def bfs(B, starts, goal, box):
    st, free, liquid, climb, node = walkable_model(B)
    (x1, y1, z1), (x2, y2, z2) = box
    seen = set(s for s in starts if node(s)); q = deque(seen)
    while q:
        c = q.popleft()
        if abs(c[0] - goal[0]) <= 1 and abs(c[2] - goal[2]) <= 1 and abs(c[1] - goal[1]) <= 1: return True, len(seen)
        x, y, z = c
        nxt = []
        if climb(c) or liquid(c):
            nxt += [(x, y + 1, z), (x, y - 1, z)]
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (x1 <= nx <= x2 and z1 <= nz <= z2): continue
            if node((nx, y, nz)): nxt.append((nx, y, nz)); continue
            if free((x, y + 2, z)) and node((nx, y + 1, nz)): nxt.append((nx, y + 1, nz)); continue      # step / jump up 1
            if liquid(c) and free((x, y + 2, z)) and free((x, y + 3, z)) and node((nx, y + 2, nz)): nxt.append((nx, y + 2, nz)); continue   # climb out of water onto a ledge one above the surface
            if free((nx, y, nz)) and free((nx, y + 1, nz)):                                             # walk off an edge
                for k in range(1, FALL + 1):
                    if y - k < y1: break
                    if node((nx, y - k, nz)): nxt.append((nx, y - k, nz)); break
                    if not free((nx, y - k, nz)): break
        for n in nxt:
            if n not in seen and y1 <= n[1] <= y2 and node(n): seen.add(n); q.append(n)
    return False, len(seen)


OTHER = {'graveyard': ('bm:graveyard', 'bm.key_altar')}     # non-dungeon structures: (structure id, the marker to reach)


def test(d, x, z, wait_shaft=True, place=True):
    sid, tag, dd = (OTHER[d][0], OTHER[d][1], None) if d in OTHER else (f'bm:p2_{d}', 'bm.entr', d)
    cmd(f'forceload add {x - 112} {z - 112} {x + 112} {z + 112}')
    if not wait_loaded(x, z): return f'{d} @{x},{z}: chunks never loaded'
    out = cmd(f'place structure {sid} {x} 0 {z}') if place else 'Generated (already placed)'
    if 'Generated' not in out: cmd(f'forceload remove {x - 112} {z - 112} {x + 112} {z + 112}'); return f'{d} @{x},{z}: {out.strip()}'
    time.sleep(8 if wait_shaft else 3)           # markers tick: the runtime shaft (brood, lucky) is built within a couple of seconds
    e = marker_pos(tag, dd, x, z)
    if not e: return f'{d} @{x},{z}: no entrance marker found'
    ex, ey, ez = int(e[0] // 1), int(e[1] // 1), int(e[2] // 1)
    cmd('save-all flush'); time.sleep(2)
    r = 70
    box = ((ex - r, max(-64, ey - 40), ez - r), (ex + r, min(319, ey + 140), ez + r))
    B = scan(*box[0], *box[1], save=False)
    if isinstance(B, tuple): B = B[0]
    # start on the surface all round the edge of the box (the top walkable cell of each edge column)
    st, free, liquid, climb, node = walkable_model(B)
    starts = []
    for (cx, cz) in [(cx, box[0][2]) for cx in range(box[0][0], box[1][0] + 1, 3)] + [(cx, box[1][2]) for cx in range(box[0][0], box[1][0] + 1, 3)] + \
                    [(box[0][0], cz) for cz in range(box[0][2], box[1][2] + 1, 3)] + [(box[1][0], cz) for cz in range(box[0][2], box[1][2] + 1, 3)]:
        for y in range(box[1][1], box[0][1], -1):
            if node((cx, y, cz)): starts.append((cx, y, cz)); break
    ok, n = bfs(B, starts, (ex, ey, ez), box)
    cmd(f'forceload remove {x - 112} {z - 112} {x + 112} {z + 112}')
    return f'{d} @{x},{z}: entrance {ex},{ey},{ez} ' + ('REACHABLE' if ok else 'NOT REACHABLE') + f' ({n} cells searched, {len(starts)} edge starts)'


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'all':
        for d, sites in SITES.items():
            for (x, z) in sites: print(test(d, x, z), flush=True)
    elif a and a[0] == 'recheck':
        print(test(a[1], int(a[2]), int(a[3]), place=False))
    else:
        print(test(a[0], int(a[1]), int(a[2])))
