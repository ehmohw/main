"""1.18: market geometry for the runtime install (ledgers, gates, the auction hall, the Gilded Gutter).

Every entity 1.18 adds to a market is spawned at runtime relative to the market's `bm.mkt` marker, so markets already
in worlds get exactly what a freshly generated one gets. The positions are TEMPLATE coordinates; this module checks
them against the built template (open air to stand in, a real floor, reachable by walking) and turns them into the
local ^ offsets the install function uses (the marker turns with the structure, so ^ follows any rotation)."""
import collections, math

import market2

MKT = (38.5, market2.W + 2, 46.5)          # the bm.mkt marker (template coordinates, yaw 0)
_MB = None


def MB():
    global _MB
    if _MB is None: _MB = market2.build()
    return _MB


def st(c):
    return MB().b.get(c, 'minecraft:air')


def passable(c):
    s = st(c)
    return (s.endswith(':air') or 'carpet' in s or s.endswith(':light') or 'light[' in s or '_sign' in s or 'lichen' in s
            or 'candle' in s or 'button' in s)


def standable(c):
    s = st(c).split('[')[0]
    return not passable(c) and not any(k in s for k in ('water', 'lava', 'fence', '_wall', 'iron_bars', 'campfire'))


def walk(c):
    x, y, z = c
    return passable(c) and passable((x, y + 1, z)) and standable((x, y - 1, z))


def flood(start):
    """Cells a player can walk to from `start` (steps of one block up or down: slabs, stairs and terraces)."""
    if not walk(start): raise ValueError(f'flood start {start} is not a walkable cell ({st(start)} over {st((start[0], start[1] - 1, start[2]))})')
    seen = {start}; q = collections.deque([start])
    while q:
        x, y, z = q.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (0, 1, -1):
                n = (x + dx, y + dy, z + dz)
                if n in seen or not (0 <= n[0] < market2.SX and 0 <= n[2] < market2.SZ and 0 < n[1] < market2.SY - 1): continue
                if walk(n): seen.add(n); q.append(n)
    return seen


_REACH = {}


def reach(name):
    """Named walkable regions: the public market, the auction hall, the Gilded Gutter, the Captain's den."""
    starts = {'public': (38, market2.W, 40), 'hall': (37, market2.W, 11), 'gutter': (55, market2.BF + 1, 9),
              'den': (3, market2.W, 15)}
    if name not in _REACH: _REACH[name] = flood(starts[name])
    return _REACH[name]


def cell(p):
    return (int(math.floor(p[0])), int(math.floor(p[1])), int(math.floor(p[2])))


def need_floor(p, region, what):
    """p: a standing position (feet). It must be a walkable cell inside the named region."""
    c = cell(p)
    if c not in reach(region):
        raise SystemExit(f'1.18 placement: {what} at {p} is not walkable in the {region} '
                         f'({st(c)} / {st((c[0], c[1] + 1, c[2]))} over {st((c[0], c[1] - 1, c[2]))})')


def need_air(p, what):
    c = cell(p)
    if not passable(c): raise SystemExit(f'1.18 placement: {what} at {p} is inside {st(c)}')


def rel(p):
    """Template position -> '^left ^up ^forward' from the bm.mkt marker (yaw 0: left = +x, forward = +z)."""
    dx, dy, dz = p[0] - MKT[0], p[1] - MKT[1], p[2] - MKT[2]
    f = lambda v: ('%.3f' % v).rstrip('0').rstrip('.') if abs(v) > 1e-9 else ''
    return f'^{f(dx)} ^{f(dy)} ^{f(dz)}'


def top_of(x, z, y0, y1):
    """Height of the walkable surface on top of the column (x, z) between y0..y1 (a bottom slab is half a block)."""
    for y in range(y1, y0 - 1, -1):
        s = st((x, y, z))
        if not passable((x, y, z)):
            return y + (0.5 if 'type=bottom' in s else 1.0)
    return None


def npc_markers():
    """{trader: ((x, y, z), yaw)} from the template's spawn markers."""
    out = {}
    for e in MB().ents:
        t = e['nbt']['Tags']
        k = [x for x in t if x.startswith('bm.npc.')]
        if 'bm.npc_spawn' in t and k:
            out.setdefault(k[0][7:], (e['pos'], float(e['nbt']['Rotation'][0])))
    return out


def counter_spot(trader):
    """A ledger spot on the trader's own counter (one block to the side of him), or None.
    -> (position of the ledger's base on the counter top, yaw the ledger faces = the trader's yaw)."""
    (x, y, z), yaw = npc_markers()[trader]
    fx, fz = round(-math.sin(math.radians(yaw))), round(math.cos(math.radians(yaw)))
    sx, sz = fz, -fx
    for df in (1, 2, 3, -1):
        for ds in (1, -1):
            cx, cz = int(math.floor(x + fx * df + sx * ds)), int(math.floor(z + fz * df + sz * ds))
            cy = int(y)
            s = st((cx, cy, cz))
            if passable((cx, cy, cz)) or 'stairs' in s or 'fence' in s: continue
            top = top_of(cx, cz, cy, cy + 2)
            if top is None or top > y + 2.2: continue
            if not passable((cx, int(top), cz)) or not passable((cx, int(top) + 1, cz)): continue
            return (cx + 0.5, top, cz + 0.5), yaw
    return None
