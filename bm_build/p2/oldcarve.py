"""3.1q: the Undercrown's first site, worn back into the Nether.

When the Undercrown moved out to 2.5k (3.0), a world that had built it at its first spot (2.98 - 2.99a) had that copy taken down
(p2/oldsite): its whole box filled with netherrack - a 224 x 112 x 224 cube, flat-faced and sharp-cornered, standing in the Nether.
This wears it back into something the Nether could have made: a cavern hollowed out of it, its floor rolling (dipping under the
lava sea's level at y 31 in places), its roof high and uneven, pillars left standing, a little glowstone hung from it, and its
outer faces broken open into whatever is round it.

Only netherrack is cut (anything a player put there stays). It runs once, and only for a cube really there: when someone is
near the old site with it loaded round them, a grid of points deep in the box is tested, and only an almost all-netherrack grid
(natural Nether at those heights is half air) starts the carve. Then the box is held loaded and cut over some seconds, a step a
second; then let go. The test never loads a chunk itself: a world nobody takes there costs nothing."""

import math

X0, Y0, Z0 = 1536, 6, -1536      # (the old box - phase237's p2/oldsite call)
SX, SY, SZ = 224, 112, 224
LAVA = 31                         # the Nether's lava sea, at and under this
CELL = 2                          # columns cut in 2 x 2 cells
EDGE = 22                         # the band round the faces where the cavern closes in (irregularly)
STEP = 900                        # fills a step (a second)


def _h(ix, iz, seed):
    n = (ix * 374761393 + iz * 668265263 + seed * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 32767.5 - 1.0


def vnoise(x, z, scale, seed, oct=3):
    """value noise, about -1..1"""
    tot, amp, norm = 0.0, 1.0, 0.0
    for o in range(oct):
        s = scale / (2 ** o)
        fx, fz = x / s, z / s
        ix, iz = math.floor(fx), math.floor(fz)
        tx, tz = fx - ix, fz - iz
        tx, tz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
        a, b = _h(ix, iz, seed + o), _h(ix + 1, iz, seed + o)
        c, d = _h(ix, iz + 1, seed + o), _h(ix + 1, iz + 1, seed + o)
        tot += amp * ((a + (b - a) * tx) * (1 - tz) + (c + (d - c) * tx) * tz)
        norm += amp; amp *= 0.5
    return tot / norm


def _pillars():
    """pillar centres on a jittered 56-block grid, each with its own reach: (x, z, r)"""
    out = []
    for i in range(4):
        for j in range(4):
            if _h(i, j, 71) < -0.35: continue            # (here and there, none)
            out.append((28 + 56 * i + 16 * _h(i, j, 73), 28 + 56 * j + 16 * _h(i, j, 79), 20 + 8 * _h(i, j, 83)))
    return out


PILLARS = _pillars()


def column(x, z):
    """(floor, roof) in world y for local column x, z: air (and lava under LAVA) from floor to roof; None - left solid"""
    d = min(x, z, SX - 1 - x, SZ - 1 - z)
    fl = 35 + 14 * vnoise(x, z, 56, 11)
    rf = 92 + 14 * vnoise(x, z, 64, 23) + 5 * vnoise(x, z, 9, 37, 2)
    for px, pz, r in PILLARS:                       # the pillars: floor and roof meet there, flaring out into each
        w = 1 - math.hypot(x - px, z - pz) / (r * (1 + 0.25 * vnoise(x, z, 7, 97, 1)))
        if w > 0:
            fl += 40 * w ** 1.6; rf -= 40 * w ** 1.6
    if d < EDGE:                                    # the faces: closed in, unevenly - here a wall, there a way through
        t = 1 - d / EDGE
        k = (0.5 + 0.5 * vnoise(x, z, 14, 67, 2)) * t * t
        fl += 26 * t * t + 30 * k                   # (and the floor up out of the lava's reach: no lava runs out of the box)
        rf -= 40 * k
    fl, rf = int(round(fl)), int(round(min(rf, Y0 + SY - 6)))     # (6 of rock kept over the roof: the cube's top stays shut)
    fl = max(fl, Y0 + 8)
    if rf - fl < 3: return None
    return fl, rf


def plan():
    """the fill lines (absolute, Nether), in order: the cut, then the glowstone"""
    cut, glow = [], []
    for x in range(0, SX, CELL):
        for z in range(0, SZ, CELL):
            c = column(x + CELL // 2, z + CELL // 2)
            if not c: continue
            fl, rf = c
            ax, az = X0 + x, Z0 + z
            bx, bz = ax + CELL - 1, az + CELL - 1
            if fl <= LAVA:
                cut.append(f'fill {ax} {fl} {az} {bx} {LAVA} {bz} minecraft:lava replace minecraft:netherrack')
                cut.append(f'fill {ax} {LAVA + 1} {az} {bx} {rf} {bz} minecraft:air replace minecraft:netherrack')
            else:
                cut.append(f'fill {ax} {fl} {az} {bx} {rf} {bz} minecraft:air replace minecraft:netherrack')
            if rf - fl > 12 and _h(x, z, 89) > 0.975:      # (a glowstone cluster hung from the roof, here and there)
                glow.append(f'fill {ax} {rf - 1} {az} {bx} {rf} {bz} minecraft:glowstone replace minecraft:air')
                glow.append(f'setblock {ax} {rf - 2} {az} minecraft:glowstone keep')
    return cut + glow


def probes():
    """the test points: a 5 x 5 grid over the box's middle, at three heights - (x, y, z)"""
    return [(X0 + 32 + 40 * i, y, Z0 + 32 + 40 * j) for i in range(5) for j in range(5) for y in (40, 64, 88)]
