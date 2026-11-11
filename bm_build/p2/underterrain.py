"""3.1i: THE UNDERCROWN'S GROUND - the owner: "the undercrown's placement is really sloppy, resulting in major cut offs where the
Netherrack is super flat and jarring looking ... the underground generates with needless netherrack surrounding it, resulting in
large blocky placements of it" - "No sharp cut offs or large flat walls from terrain suddenly being cut off for the lava lake. It
should generate and transition smoothly, with the dungeon having no loose terrain attached all over it."

What it was: the lake cut every column straight from the lava (world y 31) to a flat roof (~104) - shores that were sheer walls
seventy blocks high, a ceiling like a lid - and the dungeon's box (224 x 112 x 224) was left as whatever the Nether had there,
its outer six blocks filled solid: a giant cube of netherrack standing in the lava, its faces flat, caves and crags of the
Nether's own clinging to it.

What it is now, column by column over the box and the lake (local coordinates; phase237 stages it a chunk column a second):
THE MASSIF   round the dungeon, rock shaped as a mountain: its height over every column the highest of (a dungeon column's top +
             COVER) less SLOPE a block of distance - so every room keeps COVER blocks of rock over it and the mountain falls away
             on every side, into the lava, with a little noise on it. Above it: open air (nothing loose left on it). Below it:
             whole rock (the caves the Nether ran through the box filled - the template puts the dungeon's own cells back after).
THE SHORES   from the lake's outer edge the floor rises as a beach (BEACH blocks over the lava at the edge, down 1:1 into it), and
             the roof comes down to meet it - a great cavern, its ceiling a slow dome with a little roll to it, never a lid.
KEPT OPEN    the forecourts, the causeways and the roads' first stretch: the mountain slopes down to them (never cut), the roof
             lifted over the roads and eased back down. Over the whole roof a few blocks of lava are made rock: no lava falls.
"""
import math

from p2 import underroad as UR
from p2 import undercfg as UC

SX, SY, SZ = UC.SIZE if hasattr(UC, 'SIZE') else (224, 112, 224)
COVER = 5            # rock kept over every dungeon column
SLOPE = 1.9          # the massif's fall, blocks down per block out (steep enough to leave the lake open)
BEACH = 12           # the shore's rise over the lava at the lake's edge
ROOF_MIN, ROOF_MAX = 92 - 6, 112 - 6     # (local) the cavern roof over the lake's middle: world y 92..112
Q = 1                # heights snapped to this (1: no terraces)
SEAL = 6             # rock over the roof (3.1j: 6, air too - no lava falls out of the ceiling)
LAVA_TOP = 122 - 6   # (local) and any lava up to world 122 above that, made rock


def noise(x, z, s=1.0):
    return s * (math.sin(x * 0.071 + 0.4) * 1.3 + math.sin(z * 0.063 + 1.9) * 1.2 + math.sin((x + z) * 0.041 + 0.8) * 1.6
                + math.sin((x - z) * 0.113 + 2.6) * 0.7) / 4.8


def _q(v): return int(Q * round(v / Q))


INF0 = 10 ** 6


def _chamfer_min(g, W, D):
    """in place: each cell the least of itself and its neighbours' + step (a chamfer distance transform)"""
    for _ in range(2):
        for i in range(W):
            for j in range(D):
                v = g[i][j]
                if i: v = min(v, g[i - 1][j] + 1)
                if j: v = min(v, g[i][j - 1] + 1)
                if i and j: v = min(v, g[i - 1][j - 1] + 1.414)
                if i and j + 1 < D: v = min(v, g[i - 1][j + 1] + 1.414)
                g[i][j] = v
        for i in range(W - 1, -1, -1):
            for j in range(D - 1, -1, -1):
                v = g[i][j]
                if i + 1 < W: v = min(v, g[i + 1][j] + 1)
                if j + 1 < D: v = min(v, g[i][j + 1] + 1)
                if i + 1 < W and j + 1 < D: v = min(v, g[i + 1][j + 1] + 1.414)
                if i + 1 < W and j: v = min(v, g[i + 1][j - 1] + 1.414)
                g[i][j] = v


def plan(B):
    """[(cx, [commands])] - one step per chunk column (x), in local coords turned to world by the caller's w()"""
    sea, bed = UR.LAKE_SEA, UR.LAKE_BED
    # ---- the dungeon's columns: the top of what it sets in each (air too: its rooms' insides want rock over them)
    top = {}
    for (x, y, z) in B.b:
        if 0 <= x < SX and 0 <= z < SZ and y > top.get((x, z), -1): top[(x, z)] = y
    lx1, lz1, lx2, lz2 = UR.lake_extent()
    X1, Z1, X2, Z2 = min(lx1, 0), min(lz1, 0), max(lx2, SX - 1), max(lz2, SZ - 1)
    W, D = X2 - X1 + 1, Z2 - Z1 + 1
    inbox = lambda x, z: 0 <= x < SX and 0 <= z < SZ
    dom = lambda x, z: inbox(x, z) or UR.in_lake(x, z)
    # ---- kept open: the forecourts (and 3 round), the causeways' bands (and 4 round) to the lake's edge
    keep = set()
    for k, c in UR.WAYS.items():
        x1, _y1, z1, x2, _y2, z2 = c['box']
        keep |= {(x, z) for x in range(x1 - 3, x2 + 4) for z in range(z1 - 3, z2 + 4)}
        a1, a2 = c['road']; e = UR.lake_edge(k)
        for u in range(c['start'], e + 1):
            for v in range(a1 - 4, a2 + 5):
                keep.add((u, v) if c['ax'] == 'x' else (v, u))
    road_top = UR.Y + UR.H + 3
    # ---- each column's distance from the kept-open ground: the massif comes down to it as a slope, never a cut
    kd = [[INF0] * D for _ in range(W)]
    for (x, z) in keep:
        if X1 <= x <= X2 and Z1 <= z <= Z2: kd[x - X1][z - Z1] = 0
    _chamfer_min(kd, W, D)
    # ---- the massif: H = max over dungeon columns of (top + COVER - SLOPE * distance) - a two-pass chamfer max-propagation
    NEG = -10 ** 6
    H = [[NEG] * D for _ in range(W)]
    for (x, z), t in top.items(): H[x - X1][z - Z1] = t + COVER
    r2 = math.sqrt(2) * SLOPE
    for _ in range(2):
        for i in range(W):
            for j in range(D):
                v = H[i][j]
                if i: v = max(v, H[i - 1][j] - SLOPE)
                if j: v = max(v, H[i][j - 1] - SLOPE)
                if i and j: v = max(v, H[i - 1][j - 1] - r2)
                if i and j + 1 < D: v = max(v, H[i - 1][j + 1] - r2)
                H[i][j] = v
        for i in range(W - 1, -1, -1):
            for j in range(D - 1, -1, -1):
                v = H[i][j]
                if i + 1 < W: v = max(v, H[i + 1][j] - SLOPE)
                if j + 1 < D: v = max(v, H[i][j + 1] - SLOPE)
                if i + 1 < W and j + 1 < D: v = max(v, H[i + 1][j + 1] - r2)
                if i + 1 < W and j: v = max(v, H[i + 1][j - 1] - r2)
                H[i][j] = v
    # ---- the shore: each lake column's distance in from the lake's outer edge (the box counts as lake: no beach against it)
    dist = [[INF0] * D for _ in range(W)]
    for i in range(W):
        for j in range(D):
            if not dom(X1 + i, Z1 + j): dist[i][j] = 0
    _chamfer_min(dist, W, D)
    # ---- each column's profile: rock to lo-1, air lo..hi, (lake: old cut above hi given back to rock)
    def col(x, z):
        i, j = x - X1, z - Z1
        d = dist[i][j]
        n = noise(x, z)
        roof = ROOF_MIN + (ROOF_MAX - ROOF_MIN) * (0.5 + 0.5 * math.sin(x * 0.027 + 0.3) * math.cos(z * 0.031 + 1.1)) + 3 * n
        floor_ = sea + 1 + max(0.0, BEACH - d) + (2 * n if d < BEACH + 4 else 0)       # (the beach, 1:1 down into the lava)
        roof = min(roof, floor_ + 1 + 1.6 * d)                                            # (the roof comes down to meet it, closing)
        k = kd[i][j]
        # (down to the forecourts and roads as a slope - in the box from the court's own floor (3.1j: from the lava it left the Maw
        #  court on a two-block shell over a forty-block void), out on the lake from the lava, where the causeways run)
        base = (UR.Y - 2) if inbox(x, z) else (sea + 1 + 2 * n)
        m = min(H[i][j] + 3 * n, base + SLOPE * max(0.0, k - 1))
        roof = max(roof, road_top - 1.2 * k) if k < 40 else roof                          # (the roof lifted over the roads, smoothly)
        lo = max(floor_, m + 1)
        if inbox(x, z):
            lo = max(m + 1, sea + 1)      # (no beach in the box: the massif meets the lava)
        lo, hi = _q(lo), _q(min(roof, SY - 1))
        return lo, hi
    steps = {}
    xs = range(X1, X2 + 1)
    for x in xs:
        runs, cur = [], None
        for z in range(Z1, Z2 + 1):
            p = (col(x, z), inbox(x, z)) if dom(x, z) else None
            if cur and p == cur[2] and z == cur[1] + 1: cur[1] = z
            else:
                if cur and cur[2]: runs.append(tuple(cur))
                cur = [z, z, p]
        if cur and cur[2]: runs.append(tuple(cur))
        out = steps.setdefault((UC.ORIGIN[0] + x) // 16, [])
        for za, zb, ((lo, hi), boxcol) in runs:
            if boxcol:
                # the box: whole rock below the massif (the place puts the dungeon back after), open air above it
                out.append(('fill', x, bed, za, x, max(bed, lo - 1), zb, 'minecraft:netherrack', 'replace #bm:u_hollow'))
                if hi >= lo: out.append(('fill', x, lo, za, x, hi, zb, 'minecraft:air', ''))
                out.append(('fill', x, hi + 1, za, x, hi + SEAL, zb, 'minecraft:netherrack', 'replace #bm:u_hollow'))
                if hi + SEAL < LAVA_TOP: out.append(('fill', x, hi + SEAL + 1, za, x, LAVA_TOP, zb, 'minecraft:netherrack', 'replace minecraft:lava'))
            else:
                out.append(('fill', x, bed, za, x, sea, zb, 'minecraft:lava', ''))
                if lo > sea + 1: out.append(('fill', x, sea + 1, za, x, lo - 1, zb, 'minecraft:netherrack', ''))
                if hi >= lo: out.append(('fill', x, lo, za, x, hi, zb, 'minecraft:air', ''))
                old = UR.lake_air_top(x)
                if old > hi: out.append(('fill', x, hi + 1, za, x, old, zb, 'minecraft:netherrack', 'replace #bm:u_hollow'))
                t_ = max(hi, old)
                out.append(('fill', x, t_ + 1, za, x, t_ + SEAL, zb, 'minecraft:netherrack', 'replace #bm:u_hollow'))
                if t_ + SEAL < LAVA_TOP: out.append(('fill', x, t_ + SEAL + 1, za, x, LAVA_TOP, zb, 'minecraft:netherrack', 'replace minecraft:lava'))
    return [(cx, steps[cx]) for cx in sorted(steps)], (X1, Z1, X2, Z2)
