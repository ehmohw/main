"""THE VORN ARMADA (2.99): the Vorn's hive-fleet, circling the Hive-Star in the End's void (240 x 96 x 240 at armadacfg.ORIGIN;
an unset cell is the void). p2/armadacfg.py is the contract (the star, the ships' centres, the bridge arena, the trials' order,
the hidden rooms); phase241 runs it, phase242 is the Admiral's fight on the bridge.

North is -z. Walk y in brackets. Every ship sails ANTICLOCKWISE round the star (seen from above, its prow forward on the orbit),
so the chain of trials runs out of each ship's prow and into the next one's flank. Each ship is its rooms, carved first (walls
two thick), then a hull wrapped round them (ABuild-agnostic: K.hull, a bevelled section swept along the ship's axis, the rooms'
envelope always inside it), then its outside: engines with glowing exhausts, antenna masts, fins, war-red stripes, green
running lights. Every ship's way on is a docking collar sealed by its last trial's gate (G1, G5, G9, G13, G14, G16) with a
hard-light bridge beyond it (ABuild.bridge, the same n), a landing pad (ABuild.pad) inside each collar.

  THE HIVE-STAR      (120, 48, 120) r 22: a hollow burning shell - granulation, latitude bands, sunspots - with prominence loops
                     and spicules out to r 28 (burn radius 30). B.star(); the dungeon's controller sits at its heart.
  THE DOCK  (50)     the arrival frigate, x 86..160, z 194..224, prow east. ARRIVAL HALL x104..128 z200..212: B.dock/the entrance
                     facing the Fleet Map projector (bm.amap); the Starforge bench; the beam-out pad (B.home) in the stern alcove;
                     the 'dock' lectern and voice. THE LIFT ROOM x133..143 z201..211 - P1 levers (the gravity lifts: up, down,
                     up, down, up). G1 in the prow collar; BRIDGE 1 east along z205..207 to the Brood-Carrier.
      THE HULL GARDEN (hidden: the Sky Buddies) - their sigil in the hall; a door in its south wall out to a ledge on the hull.
  THE BROOD-CARRIER (46)  x 175..211, z 128..224, prow north. P2 simon: the specimen-tank lab x178..192 z190..208 (four tanks,
                     the pulse console; BOOKS['brood']) -> G2 -> P3 waves: the bio-bay x196..208 z176..208 -> G3 -> P4 lights: the
                     quarantine grid x178..192 z174..186 (4x4 bulbs, the button plinth) -> G4 -> P5 vboss: THE HATCHERY, round, r15,
                     17 tall, centre (192, 46, 152); a ward vault. G5 in the prow collar; BRIDGE 5 north along x197..199.
      THE SPECIMEN KENNEL (hidden: Donado) - a floor vent in the lab's south wall.
  THE STAR-FORGE (48) x 189..228, z 48..124, prow north. P6 seq: the conduit room x192..212 z102..114 (five conduit pillars, the
                     wiring schematic on the north wall; BOOKS['forge']) -> G6 -> P7 waves: the slag bay x192..206 z84..98 -> G7 ->
                     P8 xsock: the furnace hall x210..218 z84..98 (green, violet, cyan) -> G8 -> P9 vboss: THE FOUNDRY FLOOR
                     x191..216 z55..80 (26 across, lava under glass); a ward vault. G9 in the prow collar; BRIDGE 9 north, then west.
      SECRET 1 - a button behind a barrel in the furnace hall; the door in its east wall.
  THE NAVIGATOR (52) x 86..186, z 0..44, prow west. P10 targets: the star-dome x160..176 z22..38 (five constellations on its walls;
                     BOOKS['nav']) -> G10 -> P11 path: THE ZERO-G CROSSING x134..157 z24..36, plates over the open void (the
                     ceiling's stars mark the safe tiles) -> G11 -> P12 waves: the squadron bay x128..148 z4..20 -> G12 -> P13
                     vboss: THE OBSERVATORY, round, r15, under a glass dome, centre (110, 52, 18); a ward vault. G13 in the prow
                     collar; BRIDGE 13 west.
      THE MAINFRAME CORE (hidden: the Cursor) - a door in the star-dome's north wall.
  DREADNOUGHT A (48) x 34..86, z 4..46, prow west. The lobby x70..78 z18..26 ('dread' voice) -> P14 reactor: the reactor hall
                     x46..66 z15..35 (core (56, 52, 25), four conduits, four spawn points) -> G14: its armoury (north) and the
                     south collar; BRIDGE 14 south, then west.
      ZIB'S LOST SQUAD (hidden: Zib) - a Donadian-coded door (teal) in the lobby's south wall.
  DREADNOUGHT B (52) x 0..46, z 58..126, prow south. The lobby x30..38 z64..74 -> P15 waves: the hangar x12..38 z78..98 -> G15 ->
                     P16 reactor: the reactor hall x14..36 z102..118 (core (25, 56, 110)) -> G16: its armoury (east) and the
                     prow collar; BRIDGE 16 south.
      SECRET 2 - a button on a crate stack in the hangar; the door in its west wall.
  THE FLAGSHIP (55)  the Hive-Throne, round its bridge, x 0..100, z 124..238. THE COMMAND LOCK x8..32 z140..150 - P17 xsock (the
                     three Ciphers), the 'flag' voice -> G17 (the sealed bulkhead) -> P18 THE GAUNTLET x6..10 z154..214, 61 long,
                     sentries every 6 blocks alternating walls, the goal at its end -> G18 -> THE ANTECHAMBER x14..25 z192..216
                     (the spoils vault, a rift) -> the battle door (27, 55, 199) -> THE BRIDGE exactly per armadacfg.ARENA: floor
                     r30 (top y54), the wall to y66, the dome to y84; on the star's arc (window +-55 deg) the wall is one vast
                     window; four shield pylons; the helm. Behind the helm, the console housing and THE HIVE VAULT's door; a stair
                     down to the Hive Vault x81..92 z158..172 (47): the victor's vault, the hoard, a rift, BOOKS['helm']."""
import math
import random
import numpy as np
from scipy import ndimage
from nbt import Int, Byte
import armada_lore as L
from p2 import armadacfg as A
from p2.config import SEQS
from p2.kit import VEC

SX, SY, SZ = A.SIZE
STAR = A.STAR
AR = A.ARENA
AC = AR['c']
WIN = AR['window']

# ---- palettes
HULL = [('polished_deepslate', 5), ('deepslate_tiles', 3), ('gray_concrete', 2), ('black_concrete', 2), ('cracked_deepslate_tiles', 0.4)]
HULL_DARK = [('black_concrete', 4), ('polished_blackstone', 3), ('polished_deepslate', 2), ('deepslate_tiles', 1)]
WAR = [('polished_blackstone', 3), ('black_concrete', 3), ('polished_deepslate', 3), ('deepslate_tiles', 2), ('red_terracotta', 0.6)]
WALL = [('polished_deepslate', 4), ('deepslate_tiles', 2), ('gray_concrete', 1)]
FLOOR = [('polished_blackstone', 3), ('black_concrete', 1), ('deepslate_tiles', 1)]
BIO_WALL = [('polished_deepslate', 3), ('moss_block', 1), ('green_terracotta', 1), ('deepslate_tiles', 1)]
BIO_FLOOR = [('moss_block', 2), ('polished_deepslate', 2), ('sculk', 1), ('green_terracotta', 1)]
LAB_WALL = [('white_concrete', 3), ('light_gray_concrete', 2), ('polished_diorite', 1)]
LAB_FLOOR = [('light_gray_concrete', 2), ('white_concrete', 1), ('polished_andesite', 1)]
FORGE_WALL = [('polished_blackstone_bricks', 3), ('waxed_cut_copper', 1), ('waxed_weathered_cut_copper', 1), ('polished_deepslate', 2)]
FORGE_FLOOR = [('polished_blackstone', 3), ('waxed_cut_copper', 1), ('blackstone', 1)]
NAV_WALL = [('purpur_block', 2), ('polished_deepslate', 3), ('deepslate_tiles', 1)]
NAV_FLOOR = [('polished_deepslate', 2), ('purpur_block', 1), ('black_concrete', 1)]
DREAD_WALL = [('polished_blackstone_bricks', 3), ('red_terracotta', 1), ('polished_deepslate', 2), ('black_concrete', 1)]
DREAD_FLOOR = [('polished_blackstone', 3), ('black_concrete', 2), ('red_terracotta', 0.4)]
FLAG_WALL = [('black_concrete', 3), ('polished_blackstone', 3), ('polished_deepslate', 1)]
FLAG_FLOOR = [('polished_blackstone', 3), ('black_concrete', 2)]

GL = 'verdant_froglight'                     # the Vorn's green light
CHAIN_Y = 'iron_chain[axis=y,waterlogged=false]'
LAMP = 'lantern[hanging=true,waterlogged=false]'


def polar(x, z, cx, cz):
    dx, dz = x - cx, z - cz
    return math.hypot(dx, dz), math.degrees(math.atan2(dz, dx))


def angdiff(a, b):
    return (a - b + 180) % 360 - 180


class K:
    """the builder's toolkit, bound to one ABuild"""

    def __init__(self, B):
        self.B = B
        self.rnd = random.Random(29901)
        self.rooms = {}                                   # ship -> [outer boxes] (the hull's envelope)
        self.hm = np.zeros(A.SIZE, bool)                  # every hull's inside (an unset cell in here is a sealed void)
        self.ship_mask = {}
        self.decor_cells = {}

    def s(self, x, y, z, st, nbt=None):
        self.B.set(x, y, z, st, nbt)

    def get(self, x, y, z):
        return self.B.b.get((x, y, z))

    def pick(self, pal):
        return self.B.pick(pal)

    def inb(self, x, y, z):
        return 0 <= x < SX and 0 <= y < SY and 0 <= z < SZ

    def fill(self, x1, y1, z1, x2, y2, z2, pal, soft=False):
        B = self.B
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    if soft and (x, y, z) in B.b: continue
                    B.set(x, y, z, B.pick(pal))

    def air(self, x1, y1, z1, x2, y2, z2):
        self.fill(x1, y1, z1, x2, y2, z2, 'air')

    def is_air(self, x, y, z):
        st = self.B.b.get((x, y, z))
        return st is not None and st.endswith(':air')

    def exterior(self, x, y, z):
        return self.inb(x, y, z) and (x, y, z) not in self.B.b and not self.hm[x, y, z]

    def room(self, ship, x1, y1, z1, x2, y2, z2, wall=WALL, floor=FLOOR, ceil=None, t=2):
        """an air box x1..x2, y1 (walk)..y2, z1..z2; floor at y1-1 (and one under it), ceiling, walls t thick - walls only where
        nothing is set yet, so a room never closes off what was cut before it. Recorded for the ship's hull."""
        ceil = ceil or wall
        self.fill(x1 - t, y1 - 2, z1 - t, x2 + t, y2 + t, z2 + t, wall, soft=True)
        self.fill(x1, y1 - 1, z1, x2, y1 - 1, z2, floor)
        self.fill(x1, y2 + 1, z1, x2, y2 + 1, z2, ceil)
        self.air(x1, y1, z1, x2, y2, z2)
        self.rooms.setdefault(ship, []).append((x1 - t, y1 - 2, z1 - t, x2 + t, y2 + t, z2 + t))
        return self.rooms[ship][-1]

    def round_room(self, ship, cx, cz, r, w, top, wall, floor, t=2, wall_h=None):
        """a round hall: floor r (at w-1), its ceiling a dome from w+wall_h up to `top` at the centre"""
        wall_h = wall_h or (top - w) // 2
        R = r + t
        for x in range(int(cx - R) - 1, int(cx + R) + 2):
            for z in range(int(cz - R) - 1, int(cz + R) + 2):
                d = math.hypot(x - cx, z - cz)
                if d > R + 0.5: continue
                if d <= r + 0.5:
                    ceil = w + wall_h + int((top - w - wall_h) * math.sqrt(max(0.0, 1 - (d / (r + 0.8)) ** 2)))
                    self.fill(x, w - 2, z, x, w - 2, z, wall, soft=True)
                    self.s(x, w - 1, z, self.pick(floor))
                    for y in range(w, ceil + 1): self.s(x, y, z, 'air')
                    self.fill(x, ceil + 1, z, x, ceil + t, z, wall, soft=True)
                else:
                    self.fill(x, w - 2, z, x, w + wall_h + t + 3, z, wall, soft=True)
        self.rooms.setdefault(ship, []).append((int(cx - R), w - 2, int(cz - R), int(cx + R), top + t, int(cz + R)))

    def sign(self, x, y, z, facing, lines, color='lime', wall=True):
        st = f'warped_wall_sign[facing={facing},waterlogged=false]' if wall else f'warped_sign[rotation={facing},waterlogged=false]'
        self.B.sign(x, y, z, st, lines, color=color, glow=True)

    def hang(self, x, y, z, length, lamp=LAMP):
        for k in range(length): self.s(x, y + 1 + k, z, CHAIN_Y)
        self.s(x, y, z, lamp)

    def lectern(self, key, x, y, z, facing):
        self.B.lectern(x, y, z, facing, L.BOOKS[key][0], L.VX if key == 'helm' else 'The Hive', L.BOOKS[key][1])
        self.B.meta['armada']['lecterns'].append((key, x, y, z))

    # ------------------------------------------------------------------------------------------------ hulls
    def hull(self, ship, axis, keys, pal, skin=2, chamfer=4, env=True, pad=1, panel=(5, 3, 5), boxes=None):
        """a hull: a bevelled section swept along `axis` ('x' or 'z'). keys [(u, vlo, vhi, ylo, yhi)] (u along the axis, v across
        it), linear between keys; with env, every room of the ship's envelope (+pad) is always inside. Only its outer `skin`
        layers are set (where nothing is set yet): inside, the rooms; between them, a sealed void."""
        boxes = (boxes if boxes is not None else self.rooms.get(ship, [])) if env else []
        keys = sorted(keys)
        def bu(b): return (b[0], b[3]) if axis == 'x' else (b[2], b[5])
        def bv(b): return (b[2], b[5]) if axis == 'x' else (b[0], b[3])
        u0 = min([keys[0][0]] + [bu(b)[0] - pad for b in boxes])
        u1 = max([keys[-1][0]] + [bu(b)[1] + pad for b in boxes])
        mask = np.zeros(A.SIZE, bool)
        for u in range(u0, u1 + 1):
            sec = None
            for (ua, *a), (ub, *b) in zip(keys, keys[1:]):
                if ua <= u <= ub:
                    f = (u - ua) / (ub - ua) if ub > ua else 0
                    sec = [round(a[i] + (b[i] - a[i]) * f) for i in range(4)]
                    break
            if sec is None and len(keys) == 1 and u == keys[0][0]: sec = list(keys[0][1:])
            ev = [b for b in boxes if bu(b)[0] - pad <= u <= bu(b)[1] + pad]
            if ev:
                e = [min(bv(b)[0] for b in ev) - pad, max(bv(b)[1] for b in ev) + pad, min(b[1] for b in ev) - pad, max(b[4] for b in ev) + pad]
                sec = e if sec is None else [min(sec[0], e[0]), max(sec[1], e[1]), min(sec[2], e[2]), max(sec[3], e[3])]
            if sec is None: continue
            vlo, vhi, ylo, yhi = sec
            c = max(0, min(chamfer, (yhi - ylo) // 3, (vhi - vlo) // 3))
            for v in range(vlo, vhi + 1):
                dv = min(v - vlo, vhi - v)
                for y in range(max(0, ylo), min(SY - 1, yhi) + 1):
                    dy = min(y - ylo, yhi - y)
                    if dv + dy < c: continue
                    x, z = (u, v) if axis == 'x' else (v, u)
                    if 0 <= x < SX and 0 <= z < SZ: mask[x, y, z] = True
        self.paint(ship, mask, pal, skin, axis, panel)
        return mask

    def paint(self, ship, mask, pal, skin=2, axis='x', panel=(5, 3, 5)):
        """set a mask's outer `skin` layers (only unset cells), in panels of one block each"""
        nz = np.nonzero(mask)
        if not len(nz[0]): return
        lo = [max(0, int(a.min()) - 2) for a in nz]; hi = [int(a.max()) + 3 for a in nz]
        sub = mask[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
        shell = np.zeros_like(mask)
        shell[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] = sub & ~ndimage.binary_erosion(sub, iterations=skin, border_value=0)
        tot = sum(w for _, w in pal)
        cum = []
        acc = 0
        for b, w in pal:
            acc += w; cum.append((acc, b))
        pu, py, pv = panel
        B = self.B
        for (x, y, z) in zip(*np.nonzero(shell)):
            x, y, z = int(x), int(y), int(z)
            if (x, y, z) in B.b: continue
            u, v = (x, z) if axis == 'x' else (z, x)
            h = ((u // pu) * 73856093 ^ (y // py) * 19349663 ^ (v // pv) * 83492791) & 0xffffff
            r = (h / 0xffffff) * tot
            for a, b in cum:
                if r <= a: break
            B.set(x, y, z, b)
        self.hm |= mask
        self.ship_mask[ship] = self.ship_mask.get(ship, np.zeros(A.SIZE, bool)) | mask

    def skin_cells(self, ship):
        """the ship's outside skin: its set cells with the open void beside them"""
        m = self.ship_mask[ship]
        out = []
        B = self.B
        for (x, y, z) in zip(*np.nonzero(m)):
            x, y, z = int(x), int(y), int(z)
            st = B.b.get((x, y, z))
            if st is None or st.endswith(':air') or 'glass' in st: continue
            for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0)):
                if self.exterior(x + dx, y + dy, z + dz):
                    out.append((x, y, z, dx, dy, dz)); break
        return out

    def window(self, x, y, z, dx, dz, glass='glass', maxd=8):
        """punch a window from the room cell (x, y, z) outward through (dx, dz) until the open void"""
        cells = []
        cx, cz = x + dx, z + dz
        for _ in range(maxd):
            if not self.inb(cx, y, cz): return False
            if self.exterior(cx, y, cz): break
            st = self.get(cx, y, cz)
            if st is not None and (st.endswith(':air') or 'light[' in st): return False
            cells.append((cx, y, cz)); cx += dx; cz += dz
        else:
            return False
        for c in cells: self.s(*c, glass)
        return True

    def windows(self, x1, x2, z1, z2, y1, y2, dx, dz, glass='glass', every=None):
        """a band of windows on a room's wall: the room cells x1..x2 / z1..z2 (one of them a line) at y1..y2, out through (dx, dz);
        every=(n, gap): n panes then a gap mullion"""
        n = 0
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                n += 1
                if every and (n - 1) % (every[0] + every[1]) >= every[0]: continue
                for y in range(y1, y2 + 1): self.window(x, y, z, dx, dz, glass)

    def tube(self, axis, a1, a2, c, w, pal, ring=True, frame=GL):
        """a docking collar: 3 wide, 4 tall (walk w), from a1 to a2 along `axis` at cross coordinate c; walls a ring round it.
        Cut through whatever is there; returns the mouth (the far end's centre, walk level)."""
        lo, hi = min(a1, a2), max(a1, a2)
        for a in range(lo, hi + 1):
            for dc in range(-2, 3):
                for y in range(w - 1, w + 5):
                    x, z = (a, c + dc) if axis == 'x' else (c + dc, a)
                    inner = abs(dc) <= 1 and w <= y <= w + 3
                    if inner: self.s(x, y, z, 'air')
                    elif y == w - 1 and abs(dc) <= 1: self.s(x, y, z, 'polished_blackstone' if (a % 3) else 'gray_concrete')
                    elif ring and not self.is_air(x, y, z): self.s(x, y, z, self.pick(pal) if (a - lo) % 4 else 'iron_block')
        # a lit frame round the mouth
        a = a2
        for dc in range(-2, 3):
            for y in range(w - 1, w + 5):
                x, z = (a, c + dc) if axis == 'x' else (c + dc, a)
                if abs(dc) == 2 or y in (w - 1, w + 4):
                    self.s(x, y, z, frame if (abs(dc) == 2 and y in (w + 1, w + 2)) or (dc == 0 and y == w + 4) else 'black_concrete')
        return (a2, w, c) if axis == 'x' else (c, w, a2)


# ===================================================================================================== bridges
def span(k, n, legs):
    """a hard-light bridge in legs [(x1, z1, x2, z2, ya, yb)]: each an axis-aligned deck 3 wide (one of its extents), its deck y
    from ya at (x1, z1) to yb at (x2, z2) in even steps (several boxes, the same n)"""
    B = k.B
    for (x1, z1, x2, z2, ya, yb) in legs:
        along_x = abs(x2 - x1) > abs(z2 - z1)
        a1, a2 = (x1, x2) if along_x else (z1, z2)
        c1, c2 = (min(z1, z2), max(z1, z2)) if along_x else (min(x1, x2), max(x1, x2))
        sgn = 1 if a2 >= a1 else -1
        L_ = abs(a2 - a1) + 1
        steps = abs(yb - ya)
        segs = steps + 1
        assert L_ >= segs, f'bridge {n}: a leg of {L_} cannot climb {steps}'
        for i in range(segs):
            s0 = a1 + sgn * (L_ * i // segs)
            s1 = a1 + sgn * (L_ * (i + 1) // segs - 1)
            y = ya + (1 if yb > ya else -1) * i
            if along_x: B.bridge(n, s0, y, c1, s1, y, c2)
            else: B.bridge(n, c1, y, s0, c2, y, s1)


# ===================================================================================================== THE HIVE-STAR
def vnoise(rng, shape, cells):
    g = rng.random(tuple(int(math.ceil(s / cells)) + 2 for s in shape))
    z = ndimage.zoom(g, cells, order=1)
    return z[:shape[0], :shape[1], :shape[2]]


def hive_star(k):
    B = k.B
    cx, cy, cz = STAR['c']
    r = STAR['r']
    rng = np.random.default_rng(4242)
    R = r + 8
    sh = (2 * R + 1,) * 3
    n1 = vnoise(rng, sh, 4) * 0.6 + vnoise(rng, sh, 2) * 0.4          # granulation
    n2 = vnoise(rng, sh, 9)                                            # the surface's swell
    n3 = vnoise(rng, sh, 6)
    I = np.indices(sh) - R
    D = np.sqrt((I ** 2).sum(0))
    rs = r + (n2 - 0.5) * 2.4
    lat = np.degrees(np.arcsin(np.clip(I[1] / np.maximum(D, 1e-6), -1, 1)))
    lon = np.degrees(np.arctan2(I[2], I[0]))
    band = np.sin(np.radians(lat * 4.2 + (n3 - 0.5) * 70 + lon * 0.25))
    for (i, j, l) in zip(*np.nonzero((D <= rs) & (D > rs - 3.2))):
        x, y, z = cx + i - R, cy + j - R, cz + l - R
        if not k.inb(x, y, z): continue
        g = n1[i, j, l]; b = band[i, j, l]; d = rs[i, j, l] - D[i, j, l]
        if d > 1.2:
            st = 'magma_block' if g < 0.45 else 'shroomlight'
        elif g > 0.8 and b > 0.2: st = 'pearlescent_froglight'
        elif g > 0.66: st = 'shroomlight' if b > -0.3 else 'ochre_froglight'
        elif g > 0.5: st = 'orange_concrete' if b > 0.35 else ('ochre_froglight' if b > -0.2 else 'orange_glazed_terracotta')
        elif g > 0.36: st = 'magma_block' if b > 0 else 'red_glazed_terracotta'
        elif g > 0.25: st = 'red_concrete' if b > -0.4 else 'magma_block'
        else: st = 'red_glazed_terracotta' if b > 0 else 'red_concrete'
        B.set(x, y, z, st)
    # sunspots: dark cores (crying obsidian) with a penumbra of glowstone
    srng = random.Random(77)
    for _ in range(9):
        th, ph = srng.uniform(0, 2 * math.pi), srng.uniform(-0.9, 0.9)
        ux, uy, uz = math.cos(ph) * math.cos(th), math.sin(ph), math.cos(ph) * math.sin(th)
        sr = srng.uniform(1.4, 3.0)
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                for dz in range(-5, 6):
                    px, py, pz = round(cx + ux * r) + dx, round(cy + uy * r) + dy, round(cz + uz * r) + dz
                    if (px, py, pz) not in B.b: continue
                    dd = math.dist((px, py, pz), (cx + ux * r, cy + uy * r, cz + uz * r))
                    if dd <= sr: B.set(px, py, pz, 'crying_obsidian')
                    elif dd <= sr + 1.3: B.set(px, py, pz, 'glowstone')
    # prominences: burning loops from the surface out to r 28; spicules
    prng = random.Random(9)
    for _ in range(14):
        th, ph = prng.uniform(0, 2 * math.pi), prng.uniform(-1.1, 1.1)
        a = np.array([math.cos(ph) * math.cos(th), math.sin(ph), math.cos(ph) * math.sin(th)])
        t = np.cross(a, [0, 1, 0]); t = t / (np.linalg.norm(t) + 1e-9)
        t = t * math.cos(prng.uniform(0, 6.28)) + np.cross(a, t) * math.sin(prng.uniform(0, 6.28))
        span_ = prng.uniform(0.18, 0.4)
        h = prng.uniform(3.5, 6.5)
        for i in range(0, 61):
            f = i / 60
            ang = (f - 0.5) * span_
            dirv = a * math.cos(ang) + t * math.sin(ang)
            rr = r + 0.5 + h * math.sin(math.pi * f)
            p = np.array([cx, cy, cz]) + dirv * rr
            for q in ((0, 0, 0), (1, 0, 0), (0, 1, 0)) if 0.15 < f < 0.85 else ((0, 0, 0),):
                x, y, z = (int(round(p[0])) + q[0], int(round(p[1])) + q[1], int(round(p[2])) + q[2])
                if k.inb(x, y, z) and (x, y, z) not in B.b:
                    B.set(x, y, z, prng.choice(('shroomlight', 'magma_block', 'orange_stained_glass', 'shroomlight', 'ochre_froglight')))
    for _ in range(60):
        th, ph = prng.uniform(0, 2 * math.pi), prng.uniform(-1.4, 1.4)
        a = (math.cos(ph) * math.cos(th), math.sin(ph), math.cos(ph) * math.sin(th))
        ln = prng.randint(2, 4)
        for i in range(ln):
            rr = r + 1 + i
            x, y, z = round(cx + a[0] * rr), round(cy + a[1] * rr), round(cz + a[2] * rr)
            if k.inb(x, y, z) and (x, y, z) not in B.b:
                B.set(x, y, z, 'orange_stained_glass' if i else 'magma_block')
    B.star()
    B.controller(cx, cy, cz)


# ===================================================================================================== outside dressing
def engine(k, axis, sgn, u_face, v, y, rad, length, core=GL, rim='lime_stained_glass', plume=('lime_stained_glass', 'green_stained_glass'),
           shell=HULL_DARK, plen=4):
    """an engine nacelle along `axis`: a cylinder of radius rad from u_face (its glowing exhaust face) `length` toward -sgn...
    sgn is the way the exhaust points (away from the prow). A plume of stained glass trails out behind."""
    B = k.B
    for i in range(length):
        u = u_face - sgn * i
        for dv in range(-rad - 1, rad + 2):
            for dy in range(-rad - 1, rad + 2):
                d = math.hypot(dv, dy)
                if d > rad + 0.5: continue
                x, z = (u, v + dv) if axis == 'x' else (v + dv, u)
                yy = y + dy
                if not k.inb(x, yy, z) or k.is_air(x, yy, z): continue
                if i == 0:
                    st = core if d <= rad - 1.2 else rim if d <= rad - 0.4 else 'black_concrete'
                elif i == 1 and d <= rad - 1:
                    st = 'shroomlight' if core == 'shroomlight' else core
                else:
                    st = 'iron_block' if (i % 4 == 2 and d > rad - 0.8) else k.pick(shell)
                if i == 0 or (x, yy, z) not in B.b or d > rad - 0.8: B.set(x, yy, z, st)
    for j in range(1, plen + 1):                                       # the plume
        u = u_face + sgn * j
        pr = max(0.6, rad - 0.6 - j * 0.45)
        for dv in range(-rad, rad + 1):
            for dy in range(-rad, rad + 1):
                if math.hypot(dv, dy) > pr: continue
                x, z = (u, v + dv) if axis == 'x' else (v + dv, u)
                if k.inb(x, y + dy, z) and (x, y + dy, z) not in B.b:
                    B.set(x, y + dy, z, plume[0] if j <= 2 else plume[1])


def col_top(k, x, z, lo=0, hi=SY - 1):
    """the first free cell over the highest set cell of a column"""
    ys = [y for y in range(lo, hi + 1) if (x, y, z) in k.B.b and not k.is_air(x, y, z)]
    return (max(ys) + 1) if ys else None


def mast(k, x, y, z, h, tip=GL, arms=()):
    """an antenna mast: a lightning-rod spine, chain crossbars, a light at its tip (y None: on the column's top)"""
    if y is None: y = col_top(k, x, z)
    h = min(h, SY - 3 - y)
    for i in range(h):
        if k.inb(x, y + i, z) and (x, y + i, z) not in k.B.b:
            k.s(x, y + i, z, 'lightning_rod[facing=up,powered=false,waterlogged=false]' if i % 5 else 'polished_blackstone_wall')
    k.s(x, y + h, z, tip)
    k.s(x, y + h + 1, z, 'end_rod[facing=up]')
    for (ay, ax_, ln) in arms:                                         # crossbars (axis 'x' or 'z')
        if ay >= h: continue
        for d in range(1, ln + 1):
            for sg in (1, -1):
                px, pz = (x + sg * d, z) if ax_ == 'x' else (x, z + sg * d)
                if k.inb(px, y + ay, pz) and (px, y + ay, pz) not in k.B.b:
                    k.s(px, y + ay, pz, f'iron_chain[axis={ax_},waterlogged=false]')
        for sg in (1, -1):
            px, pz = (x + sg * ln, z) if ax_ == 'x' else (x, z + sg * ln)
            if k.inb(px, y + ay - 1, pz) and (px, y + ay - 1, pz) not in k.B.b: k.s(px, y + ay - 1, pz, 'red_stained_glass' if ay % 2 else GL)


def fin(k, axis, u1, u2, v, y1, y2, sweep, pal, side=0):
    """a thin fin (one block thick) in the plane v (axis 'x': the plane z=v), swept back: its top edge leans by `sweep`"""
    for u in range(min(u1, u2), max(u1, u2) + 1):
        f = (u - u1) / ((u2 - u1) or 1)
        top = round(y1 + (y2 - y1) * (1 - abs(f - 0.3) ** 1.2 * 1.3)) if sweep else y2
        for y in range(y1, max(y1, top) + 1):
            x, z = (u, v) if axis == 'x' else (v, u)
            if k.inb(x, y, z) and (x, y, z) not in k.B.b: k.s(x, y, z, k.pick(pal) if y < top else 'red_concrete')


def wing(k, axis, u1, u2, vroot, vtip, y, pal, light=GL):
    """a flat wing (one layer) from the hull side (vroot) out to vtip, its leading edge swept"""
    sg = 1 if vtip > vroot else -1
    n = abs(vtip - vroot)
    for i in range(n + 1):
        v = vroot + sg * i
        cut = round(i * (u2 - u1) / max(1, n) * 0.7)
        for u in range(min(u1, u2) + cut, max(u1, u2) + 1):
            x, z = (u, v) if axis == 'x' else (v, u)
            if k.inb(x, y, z) and (x, y, z) not in k.B.b:
                k.s(x, y, z, light if i == n and (u % 3 == 0) else ('red_concrete' if i == n else k.pick(pal)))


def dress(k, ship, stripe=None, stripe_pal=('red_concrete', 'red_terracotta'), light=GL, every=7):
    """the outside skin: war-red stripe band(s) (y values) on the hull's flanks, running lights over them and on its back"""
    B = k.B
    keep = ('glass', 'froglight', 'lantern', 'iron_block', 'shroomlight', 'magma', 'copper', 'lightning', 'wall', 'rod', 'chain',
            'observer', 'campfire', 'gold', 'sea_lantern', 'amethyst', 'terracotta', 'concrete_powder')
    cells = k.skin_cells(ship)
    top = max(stripe) + 3 if stripe else None
    for (x, y, z, dx, dy, dz) in cells:
        st = B.b[(x, y, z)]
        if any(t in st for t in keep): continue
        if dy == 0 and stripe and y in stripe:
            B.set(x, y, z, stripe_pal[((x + z) // 3) % len(stripe_pal)])
        elif dy == 0 and top and y == top and (x + z) % every == 0:
            B.set(x, y, z, light)
        elif dy == 1 and (x * 5 + z * 3) % (every * 3) == 0:
            B.set(x, y, z, light)
    return cells


def lava_slot(k, cells, glass='orange_stained_glass'):
    """lava behind glass: `cells` [(x, y, z)] become lava; every neighbour that isn't lava and isn't already solid becomes
    blackstone (never air or the void), and the faces we want seen are glass - set those first"""
    S = set(cells)
    for c in cells: k.s(*c, 'lava')
    for (x, y, z) in cells:
        for q in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1), (x, y - 1, z), (x, y + 1, z)):
            if q in S: continue
            st = k.get(*q)
            if st is None or st.endswith(':air') or 'light[' in st: k.s(*q, 'blackstone')


# ===================================================================================================== THE DOCK
def dock(k):
    B, s = k.B, k.s
    W = 50
    sh = 'dock'
    k.room(sh, 104, W, 200, 128, W + 7, 212, wall=WALL, floor=FLOOR)              # the arrival hall
    k.room(sh, 97, W, 204, 101, W + 4, 208, wall=WALL, floor=FLOOR)               # the beam-out alcove
    k.air(102, W, 205, 103, W + 3, 207)
    k.room(sh, 133, W, 201, 143, W + 6, 211, wall=WALL, floor=FLOOR)              # the lift room
    k.air(129, W, 204, 132, W + 4, 208)
    # the hull: a long frigate, a raised bridge tower over the hall, the prow a docking spar
    k.hull(sh, 'x', [(88, 200, 212, 44, 58), (96, 196, 216, 42, 60), (130, 196, 216, 42, 61), (146, 200, 212, 45, 57), (156, 203, 209, 47, 55)], HULL)
    k.hull(sh, 'x', [(106, 202, 210, 58, 64), (122, 203, 209, 58, 64), (126, 205, 207, 58, 61)], HULL_DARK, env=False, chamfer=2)
    k.hull(sh, 'x', [(98, 204, 208, 38, 44), (138, 205, 207, 40, 44)], HULL_DARK, env=False, chamfer=1)                  # the keel
    mouth = k.tube('x', 144, 157, 206, W, HULL_DARK)                          # the prow collar: G1, bridge 1
    # -------- the arrival hall: green light strips in the floor, ceiling panels, the Fleet Map projector, windows on the star
    for x in range(104, 129):
        for z in (203, 209):
            s(x, W - 1, z, GL if x % 2 else 'black_concrete')
    for x in range(106, 128, 4):
        for z in (202, 206, 210):
            s(x, W + 8, z, GL)
    for x in (105, 115, 121, 127):
        for z in (200, 212):
            for y in range(W, W + 8): s(x, y, z, 'polished_blackstone' if y % 4 else 'iron_block')
    for (x, z) in ((117, 205), (118, 205), (119, 205), (117, 206), (119, 206), (117, 207), (118, 207), (119, 207)):
        s(x, W, z, 'chiseled_polished_blackstone')
    s(118, W, 206, GL)
    for (x, z) in ((116, 204), (120, 204), (116, 208), (120, 208)):
        s(x, W, z, 'polished_blackstone_wall'); s(x, W + 1, z, 'end_rod[facing=up]')
    B.mb(118, W + 2, 206, ['bm.amap'])
    k.windows(106, 126, 200, 200, W + 2, W + 5, 0, -1, every=(4, 1))          # the star, through the north wall
    B.dock(107, W, 206, 'east')
    B.entrance(107, W, 206)
    s(107, W - 1, 206, GL)
    B.bench(110, W + 1, 211)
    for (x, z) in ((109, 211), (111, 211)): s(x, W, z, 'anvil[facing=east]')
    k.lectern('dock', 124, W, 202, 'south')
    B.voice('dock', 112, W, 206, r=6)
    k.sign(106, W + 2, 212, 'north', ['WELCOME,', 'SPECIMEN.', 'PLEASE REMAIN', 'CALM.'], color='lime')
    # the beam-out alcove
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            s(99 + dx, W - 1, 206 + dz, 'lime_concrete' if dx or dz else GL)
    B.home(99, W, 206)
    k.sign(101, W + 2, 208, 'north', ['BEAM-OUT PAD', 'Step on it to', 'go back where', 'you came from.'], color='aqua')
    s(99, W + 4, 206, 'end_rod[facing=down]')
    # -------- THE LIFT ROOM (P1 levers): five gravity lifts on the south wall, up, down, up, down, up
    for x in range(133, 144):
        s(x, W - 1, 206, GL if x % 2 else 'black_concrete')
    for i, x in enumerate((134, 136, 138, 140, 142)):
        s(x, W + 1, 212, 'iron_block'); s(x, W + 3, 212, 'redstone_lamp[lit=false]')
        B.lever(1, x, W + 1, 211, 'north', want=(i % 2 == 0))
        k.sign(x, W + 2, 211, 'north', [f'LIFT {i + 1}', '', 'UP / DOWN', ''], color='lime')
    k.sign(138, W + 4, 211, 'north', ['GRAVITY LIFTS', 'Set them as the', 'manifest says.', ''], color='yellow')
    B.pz(1, 'levers', 138, W + 3, 206)
    B.pad(141, W, 206)
    k.windows(134, 142, 201, 201, W + 2, W + 4, 0, -1, every=(2, 1))
    B.gate(146, W, 206, 'z', 1)
    B.fx(118, W + 4, 206); B.fx(138, W + 3, 206)
    # -------- THE HULL GARDEN (the Sky Buddies): their sigil by the hall's south wall; the door out to a ledge on the hull
    for x in range(113, 122):
        for y in range(W, W + 5): s(x, y, 213, 'polished_deepslate')
    k.air(116, W, 214, 118, W + 2, 218)
    k.fill(116, W - 1, 214, 118, W - 1, 218, 'polished_blackstone')
    for x in (115, 119):
        for z in range(214, 219):
            for y in range(W - 1, W + 4):
                if (x, y, z) not in B.b or not k.is_air(x, y, z): s(x, y, z, k.pick(HULL_DARK))
    k.fill(115, W + 3, 214, 119, W + 3, 218, HULL_DARK)
    B.hidden('garden', 117, W, 213, 'x', 1, 3, 'polished_deepslate', [('sky', 117, W, 210)])
    k.sign(114, W + 2, 212, 'north', ['THE SKY IS', 'RIGHT THERE.', 'SOMEONE WHO', 'FLIES KNOWS.'], color='aqua')
    for x in range(106, 129):
        for z in range(219, 224):
            s(x, W - 1, z, 'moss_block' if (x * 3 + z) % 5 else 'grass_block[snowy=false]')
            s(x, W - 2, z, k.pick(HULL_DARK))
            for y in range(W, W + 6): s(x, y, z, 'air') if (x, y, z) in B.b else None
    for x in range(106, 129):
        s(x, W - 1, 218, 'moss_block') if x not in (116, 117, 118) else None
    for x in range(105, 130):
        s(x, W, 224, 'polished_blackstone_wall'); s(x, W - 1, 224, k.pick(HULL_DARK))
    for z in range(218, 225):
        s(105, W, z, 'polished_blackstone_wall'); s(129, W, z, 'polished_blackstone_wall')
        s(105, W - 1, z, k.pick(HULL_DARK)); s(129, W - 1, z, k.pick(HULL_DARK))
    grng = random.Random(5)
    for x in range(107, 128):
        for z in range(219, 224):
            if (x, z) in ((126, 221), (107, 221), (117, 219)): continue
            r_ = grng.random()
            if r_ < 0.12: s(x, W, z, grng.choice(('azalea', 'flowering_azalea')))
            elif r_ < 0.3: s(x, W, z, grng.choice(('cornflower', 'allium', 'blue_orchid', 'oxeye_daisy', 'short_grass', 'fern', 'lily_of_the_valley')))
    for (x, z) in ((110, 222), (122, 220)):
        for y in range(W, W + 4): s(x, y, z, 'birch_log[axis=y]')
        k.fill(x - 2, W + 3, z - 2, x + 2, W + 4, z + 2, [('azalea_leaves[distance=1,persistent=true,waterlogged=false]', 2),
                                                         ('flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]', 1)], soft=True)
    s(126, W - 1, 221, 'gold_block'); B.relic('garden', 126, W, 221)
    B.chest(107, W, 221, 'east', loot='bm:p2/armada/hidden')
    # -------- outside: engines, masts, fins, stripes
    for (z, y, r) in ((200, 48, 3), (212, 48, 3), (206, 55, 2), (206, 43, 2)):
        engine(k, 'x', -1, 86, z, y, r, 7)
    mast(k, 112, None, 206, 10, arms=((4, 'z', 3), (7, 'z', 2)))
    mast(k, 118, None, 206, 14, arms=((5, 'z', 4), (9, 'z', 2)))
    mast(k, 136, None, 206, 7, arms=((3, 'z', 2),))
    fin(k, 'x', 92, 108, 206, 61, 69, True, HULL_DARK)
    wing(k, 'x', 92, 104, 196, 189, 49, HULL)
    wing(k, 'x', 90, 102, 216, 223, 47, HULL)
    dress(k, sh, stripe=(52, 53))
    return mouth


# ===================================================================================================== THE BROOD-CARRIER
def brood(k):
    B, s = k.B, k.s
    W = 46
    sh = 'brood'
    rng = random.Random(46)
    k.room(sh, 178, W, 190, 192, W + 7, 208, wall=LAB_WALL, floor=LAB_FLOOR)       # P2 the specimen lab
    k.room(sh, 196, W, 176, 208, W + 10, 208, wall=BIO_WALL, floor=BIO_FLOOR)     # P3 the bio-bay
    k.room(sh, 178, W, 174, 192, W + 11, 186, wall=LAB_WALL, floor=LAB_FLOOR)     # P4 quarantine
    k.room(sh, 184, W, 212, 192, W + 3, 217, wall=BIO_WALL, floor=[('moss_block', 1)])  # the kennel (hidden)
    k.round_room(sh, 192, 152, 15, W, W + 17, BIO_WALL, BIO_FLOOR, wall_h=9)      # P5 THE HATCHERY
    k.room(sh, 184, W, 166, 186, W + 3, 173, wall=BIO_WALL, floor=BIO_FLOOR)      # the corridor to the hatchery (G4)
    k.hull(sh, 'z', [(224, 182, 202, 38, 54), (214, 176, 208, 36, 58), (170, 174, 210, 35, 62), (140, 178, 206, 37, 60), (130, 193, 203, 43, 52)],
           HULL, chamfer=5)
    k.hull(sh, 'z', [(206, 186, 198, 58, 62), (180, 188, 196, 58, 63)], HULL_DARK, env=False, chamfer=2)       # the spine
    k.hull(sh, 'z', [(212, 189, 195, 30, 36), (150, 190, 194, 31, 36)], HULL_DARK, env=False, chamfer=1)       # the keel
    arr = k.tube('x', 177, 171, 206, W, HULL_DARK)                                 # arrival (bridge 1)
    dep = k.tube('z', 138, 128, 198, W, HULL_DARK)                                 # the prow collar (G5, bridge 5)
    # ---------------- P2 THE SPECIMEN LAB (simon): four tanks pulse; the pulse console; BOOKS['brood']
    for x in range(178, 193):
        s(x, W - 1, 199, 'lime_concrete' if x % 2 else 'white_concrete')
    order = {1: 1, 4: 2, 2: 3, 3: 4}                                              # tank label -> its place in the pulse (the book)
    tanks = [(1, 181, 194, 'east'), (2, 189, 194, 'west'), (3, 181, 202, 'east'), (4, 189, 202, 'west')]
    for (lab, tx, tz, f) in tanks:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                s(tx + dx, W, tz + dz, 'polished_deepslate')
                for y in range(W + 1, W + 6):
                    s(tx + dx, y, tz + dz, 'glass' if dx or dz else ('slime_block' if y in (W + 2, W + 4) else GL if y == W + 1 else 'green_stained_glass'))
                s(tx + dx, W + 6, tz + dz, 'iron_block' if dx or dz else GL)
                s(tx + dx, W + 7, tz + dz, 'polished_deepslate')
        fx_, fz_ = VEC[f]
        bx = tx + 2 * fx_
        B.seq_button(2, bx, W, tz, f'polished_blackstone_button[face=wall,facing={f},powered=false]', order[lab], sound=lab)
        k.sign(bx, W + 1, tz, f, [f'TANK {lab}', '', 'SUBJECT', f'#{110 + lab * 2}'], color='green')
    s(185, W, 190, 'polished_deepslate'); s(185, W + 1, 190, GL)
    B.listen_button(2, 185, W, 191, 'stone_button[face=wall,facing=south,powered=false]')
    k.sign(185, W + 1, 191, 'south', ['PULSE CONSOLE', 'Press: the tanks', 'pulse. Press', 'them back.'], color='lime')
    k.lectern('brood', 183, W, 206, 'east')
    B.pz(2, 'simon', 185, W + 4, 198)
    SEQS.setdefault(A.d, {})[2] = 4
    B.voice('brood', 182, W, 206, r=6)
    B.pad(180, W, 206)
    for x in range(180, 192, 3):
        for z in (192, 198, 204):
            s(x, W + 8, z, 'sea_lantern')
    k.windows(178, 178, 192, 202, W + 2, W + 4, -1, 0, every=(3, 2))
    # THE SPECIMEN KENNEL (Donado): a vent in the lab's south wall; his sigil before it
    for x in range(185, 192):
        for y in range(W, W + 3): s(x, y, 209, 'white_concrete')
    k.air(188, W, 210, 188, W + 1, 211)
    B.hidden('kennel', 188, W, 209, 'x', 0, 2, 'waxed_copper_grate', [('don', 188, W, 206)])
    k.sign(186, W + 1, 208, 'north', ['SUBJECT 117', '(CANINE) LOST', 'IN THE VENTS.', 'DO NOT FOLLOW.'], color='red')
    for x in range(184, 193):
        for z in range(212, 218):
            if (x + z) % 3 == 0: s(x, W, z, rng.choice(('brown_carpet', 'red_carpet', 'white_carpet')))
    for (x, z) in ((185, 213), (191, 216)): s(x, W, z, 'bone_block[axis=x]')
    s(190, W - 1, 213, 'gold_block'); s(190, W, 213, 'air'); B.relic('kennel', 190, W, 213)
    B.chest(185, W, 216, 'east', loot='bm:p2/armada/hidden')
    s(188, W + 4, 215, GL)
    # ---------------- P3 THE BIO-BAY (waves)
    k.air(193, W, 199, 195, W + 3, 201)
    B.gate(194, W, 200, 'z', 2)
    B.pz(3, 'waves', 202, W, 192)
    for (x, z) in ((198, 180), (206, 180), (198, 204), (206, 204), (202, 185), (202, 199)):
        B.el(3, 'wsp', x, W, z)
    for z in range(178, 208, 5):                                             # bio-vats along the east wall
        for y in range(W, W + 6):
            s(209, y, z, 'green_stained_glass' if 0 < y - W < 5 else 'polished_deepslate')
            s(210, y, z, GL if y == W + 1 else 'slime_block')
    for x in range(197, 208):
        for z in range(177, 208):
            if rng.random() < 0.08: s(x, W - 1, z, 'sculk')
            if rng.random() < 0.03 and k.is_air(x, W, z) and abs(x - 202) >= 2: s(x, W, z, 'moss_carpet')
    for x in range(198, 208, 4):
        for z in range(178, 208, 5): s(x, W + 11, z, GL)
    k.windows(208, 208, 179, 206, W + 3, W + 6, 1, 0, every=(4, 1))
    # ---------------- P4 THE QUARANTINE GRID (lights-out): 4x4 bulbs in the west wall, the buttons on a plinth before them
    k.air(193, W, 179, 195, W + 3, 181)
    B.gate(194, W, 180, 'z', 3)
    for z in range(176, 186):
        for y in range(W + 7, W + 11): s(177, y, z, 'black_concrete' if (z + y) % 2 else 'yellow_concrete')
    for i in range(16):
        r_, c = divmod(i, 4)
        B.bulb(4, 177, W + 10 - 2 * r_, 177 + 2 * c, i)
    for z in range(177, 183):
        for y in range(W, W + 4): s(179, y, z, 'polished_deepslate')
        s(179, W + 4, z, 'polished_deepslate_slab[type=bottom,waterlogged=false]')
    for i in range(16):
        r_, c = divmod(i, 4)
        B.lo_button(4, 180, W + 3 - r_, 178 + c, 'polished_blackstone_button[face=wall,facing=east,powered=false]', i)
    k.sign(180, W + 3, 177, 'east', ['QUARANTINE', 'Light every cell', 'to seal the', 'grid.'], color='yellow')
    B.pz(4, 'lights', 184, W + 5, 180)
    for x in range(182, 192, 3):
        for z in range(175, 186, 3): s(x, W + 12, z, 'sea_lantern')
    for z in (175, 185):
        for x in range(185, 192): s(x, W, z, 'iron_bars')
    # ---------------- P5 THE HATCHERY (vboss: the Brood-Warden): egg pods, a green glass skylight; a ward vault
    B.gate(185, W, 172, 'x', 4)
    cx, cz = 192, 152
    for a in range(0, 360, 30):
        ex, ez = round(cx + 12.5 * math.cos(math.radians(a))), round(cz + 12.5 * math.sin(math.radians(a)))
        if abs(ex - 185) <= 2 and ez > 160: continue
        if abs(ex - 198) <= 2 and ez < 145: continue
        if abs(ex - 192) <= 2 and ez < 142: continue
        for dy in range(0, 4):
            rr = 1.4 if dy in (1, 2) else 0.8
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if math.hypot(dx, dz) <= rr: s(ex + dx, W + dy, ez + dz, 'slime_block' if dy % 2 else 'ochre_froglight' if (dx, dz) == (0, 0) else 'lime_terracotta')
    for x in range(cx - 15, cx + 16):
        for z in range(cz - 15, cz + 16):
            d = math.hypot(x - cx, z - cz)
            if d <= 15 and rng.random() < 0.12: s(x, W - 1, z, 'sculk')
            if d <= 4.5: s(x, W - 1, z, 'verdant_froglight' if d <= 1.5 else 'sculk_catalyst' if int(d) == 3 else 'moss_block')
    for y in range(W + 14, W + 19):                                      # the skylight
        for x in range(cx - 6, cx + 7):
            for z in range(cz - 6, cz + 7):
                if math.hypot(x - cx, z - cz) <= 5.5 and not k.is_air(x, y, z) and (x, y, z) in B.b and k.is_air(x, y - 1, z):
                    s(x, y, z, 'green_stained_glass')
    for a in range(15, 360, 45):
        hx, hz = round(cx + 9 * math.cos(math.radians(a))), round(cz + 9 * math.sin(math.radians(a)))
        top = max([y for y in range(W, W + 20) if k.is_air(hx, y, hz)] or [W])
        for y in range(top - 4, top + 1): s(hx, y, hz, 'weeping_vines_plant' if y < top else 'weeping_vines_plant')
        s(hx, top - 5, hz, 'weeping_vines[age=20]')
    B.vboss(5, cx, W, cz, 'brood', r=14)
    B.vault(cx, W, 139, 'south', 'akey', 'bm:p2/armada/ward')
    s(cx - 1, W, 139, 'polished_deepslate'); s(cx + 1, W, 139, 'polished_deepslate')
    B.fx(cx, W + 8, cz)
    for a in range(-60, 61, 20):                                          # windows on the star (west, round the hatchery)
        t = math.radians(180 + a)
        wx, wz = round(cx + 15 * math.cos(t)), round(cz + 15 * math.sin(t))
        if k.is_air(wx, W + 4, wz):
            for y in range(W + 3, W + 7):
                k.window(wx, y, wz, -1, 0, glass='green_stained_glass')
    B.gate(198, W, 135, 'x', 5)
    B.pad(198, W, 141)
    B.fx(185, W + 4, 199); B.fx(202, W + 5, 192); B.fx(185, W + 5, 180)
    # ---------------- outside
    for (x, y, r) in ((184, 42, 3), (200, 42, 3), (186, 53, 3), (198, 53, 3)):
        engine(k, 'z', 1, 224, x, y, r, 6)
    for (x, z, h) in ((190, 196, 12), (194, 184, 16), (190, 176, 9)):
        mast(k, x, None, z, h, arms=((4, 'x', 3), (8, 'x', 2)))
    wing(k, 'z', 140, 166, 174, 164, 42, HULL)
    wing(k, 'z', 140, 166, 210, 220, 42, HULL)
    fin(k, 'z', 196, 220, 192, 63, 72, True, HULL_DARK)
    dress(k, sh, stripe=(48, 49), stripe_pal=('red_concrete', 'red_terracotta', 'lime_terracotta'))
    return arr, dep


# ===================================================================================================== THE STAR-FORGE
def forge(k):
    B, s = k.B, k.s
    W = 48
    sh = 'forge'
    rng = random.Random(48)
    k.room(sh, 192, W, 102, 212, W + 7, 114, wall=FORGE_WALL, floor=FORGE_FLOOR)   # P6 the conduit room
    k.room(sh, 192, W, 84, 206, W + 9, 98, wall=FORGE_WALL, floor=FORGE_FLOOR)     # P7 the slag bay
    k.room(sh, 210, W, 84, 218, W + 7, 98, wall=FORGE_WALL, floor=FORGE_FLOOR)     # P8 the furnace hall
    k.room(sh, 222, W, 93, 226, W + 3, 99, wall=WALL, floor=FLOOR)                 # secret 1
    k.room(sh, 191, W, 55, 216, W + 12, 80, wall=FORGE_WALL, floor=FORGE_FLOOR)    # P9 THE FOUNDRY FLOOR
    k.hull(sh, 'z', [(117, 195, 213, 42, 57), (111, 190, 216, 40, 60), (84, 189, 221, 40, 62), (58, 190, 217, 41, 64), (50, 199, 209, 45, 56)],
           HULL, chamfer=5)
    k.hull(sh, 'z', [(110, 196, 210, 58, 63), (90, 194, 206, 58, 63)], HULL_DARK, env=False, chamfer=2)
    k.hull(sh, 'z', [(116, 201, 207, 34, 40), (60, 201, 207, 35, 40)], HULL_DARK, env=False, chamfer=1)
    arr = k.tube('z', 115, 119, 198, W, HULL_DARK)
    dep = k.tube('z', 54, 48, 204, W, HULL_DARK)
    # ---------------- P6 THE CONDUIT ROOM (seq): five conduit pillars; the schematic over the door shows the order
    colours = [('orange_concrete', 'ORANGE'), ('lime_concrete', 'LIME'), ('cyan_concrete', 'CYAN'), ('yellow_concrete', 'YELLOW'), ('magenta_concrete', 'MAGENTA')]
    press = {0: 2, 1: 5, 2: 1, 3: 3, 4: 4}                                    # pillar (west to east) -> its place in the order
    for i, x in enumerate((195, 199, 203, 207, 211)):
        for y in range(W, W + 6):
            s(x, y, 107, 'waxed_cut_copper' if y < W + 3 else colours[i][0] if y == W + 3 else 'waxed_copper_block' if y < W + 6 else 'copper_bulb')
        s(x, W + 6, 107, 'waxed_copper_bulb[lit=true,powered=false]')
        s(x, W + 7, 107, CHAIN_Y)
        B.seq_button(6, x, W + 1, 108, 'stone_button[face=wall,facing=south,powered=false]', press[i], sound=i + 1)
        # the schematic, over the door on the north wall: the same five in the same places, numbered
        s(x, W + 6, 101, colours[i][0])
        k.sign(x, W + 5, 102, 'south', [f'{press[i]}', colours[i][1], '', ''], color='orange')
    for x in range(195, 212):
        if x not in (195, 199, 203, 207, 211): s(x, W + 6, 101, 'waxed_copper_block' if x % 2 else 'redstone_lamp[lit=false]')
    k.sign(203, W + 7, 102, 'south', ['REROUTE THE', 'CONDUITS IN', 'THIS ORDER', ''], color='yellow')
    k.lectern('forge', 194, W, 112, 'east')
    B.pz(6, 'seq', 203, W + 4, 109)
    SEQS.setdefault(A.d, {})[6] = 5
    B.voice('forge', 198, W, 111, r=6)
    B.pad(198, W, 112)
    for x in range(193, 212, 3):
        s(x, W - 1, 110, 'magma_block'); s(x, W + 8, 110, 'shroomlight')
    k.windows(212, 212, 104, 112, W + 2, W + 4, 1, 0, every=(2, 1))
    # ---------------- P7 THE SLAG BAY (waves): lava behind glass in its walls, blast furnaces burning
    k.air(201, W, 99, 203, W + 3, 101)
    B.gate(202, W, 100, 'x', 6)
    B.pz(7, 'waves', 199, W, 91)
    for (x, z) in ((194, 86), (204, 86), (194, 96), (204, 96), (199, 86)):
        B.el(7, 'wsp', x, W, z)
    slots = []
    for z in range(85, 98, 4):
        for y in range(W + 1, W + 7):
            s(191, y, z, 'orange_stained_glass'); slots.append((190, y, z))
    lava_slot(k, slots)
    for (x, z) in ((193, 85), (205, 85), (193, 97), (205, 97)):
        for y in range(W, W + 3): s(x, y, z, 'blast_furnace[facing=south,lit=true]' if y == W else 'polished_blackstone_bricks')
    for x in range(194, 206, 3):
        for z in range(86, 98, 4): s(x, W + 10, z, 'shroomlight')
    for x in range(195, 205, 4):
        k.hang(x, W + 6, 91, 3, lamp='lantern[hanging=true,waterlogged=false]')
    # ---------------- P8 THE FURNACE HALL (xsock): green, violet, cyan - over three furnaces, their glass burning behind
    k.air(207, W, 90, 209, W + 3, 92)
    B.gate(208, W, 91, 'z', 7)
    for (z, key, glass, name) in ((88, 'green', 'lime_stained_glass', 'GREEN'), (91, 'violet', 'purple_stained_glass', 'VIOLET'), (94, 'cyan', 'cyan_stained_glass', 'CYAN')):
        B.sock(8, 216, W + 1, z, key)
        for y in range(W, W + 5):
            s(219, y, z, glass); s(220, y, z, 'shroomlight' if y % 2 else 'ochre_froglight')
        k.sign(218, W + 3, z, 'west', [name, 'XENITE', '(drop it on', 'the furnace)'], color={'green': 'lime', 'violet': 'magenta', 'cyan': 'aqua'}[key])
    B.pz(8, 'xsock', 214, W + 3, 91)
    for z in range(85, 98, 3): s(214, W + 8, z, 'shroomlight')
    # SECRET 1: a button behind a barrel in the north-east corner; the door in the east wall
    s(216, W, 84, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel'})
    s(217, W, 84, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel'})
    s(216, W + 1, 84, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel'})
    B.sbutton(218, W, 84, 'polished_blackstone_button[face=wall,facing=south,powered=false]', 1)
    for z in range(95, 99):
        for y in range(W, W + 4): s(219, y, z, 'polished_deepslate')
    k.air(220, W, 96, 221, W + 1, 96)
    B.sdoor(219, W, 96, 1)
    s(224, W - 1, 96, 'gilded_blackstone'); B.relic('secret1', 224, W, 96)
    B.chest(222, W, 98, 'east', loot='bm:p2/armada/hidden')
    s(225, W + 3, 94, 'shroomlight')
    # ---------------- P9 THE FOUNDRY FLOOR (vboss: the Forgemaster): lava running under glass in the floor; a ward vault
    k.air(213, W, 81, 215, W + 3, 83)
    B.gate(214, W, 82, 'x', 8)
    cx, cz = 203, 67
    slots = []
    for x in range(192, 216):
        for z in range(56, 80):
            if (x - cx) % 6 == 0 or (z - cz) % 6 == 0:
                if abs(x - cx) <= 1 and abs(z - cz) <= 1: continue
                s(x, W - 1, z, 'orange_stained_glass'); slots.append((x, W - 2, z))
    lava_slot(k, slots)
    for (x, z) in ((194, 58), (212, 58), (194, 77), (212, 77)):                   # crucibles
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for y in range(W, W + 3): s(x + dx, y, z + dz, 'blast_furnace[facing=south,lit=true]' if y == W + 2 and dx == dz == 0 else 'polished_blackstone_bricks')
        s(x, W + 3, z, 'campfire[facing=north,lit=true,signal_fire=true,waterlogged=false]')
    for x in range(193, 215, 4):
        for z in range(57, 80, 4): s(x, W + 13, z, 'shroomlight')
    for (x, z) in ((197, 62), (209, 62), (197, 73), (209, 73)):
        k.hang(x, W + 7, z, 6, lamp='lantern[hanging=true,waterlogged=false]')
    B.vboss(9, cx, W, cz, 'forge', r=14)
    B.vault(196, W, 57, 'south', 'akey', 'bm:p2/armada/ward')
    B.fx(cx, W + 8, cz)
    k.windows(191, 191, 58, 78, W + 3, W + 7, -1, 0, glass='orange_stained_glass', every=(3, 2))
    B.gate(204, W, 51, 'x', 9)
    B.pad(204, W, 57)
    B.fx(203, W + 4, 108); B.fx(199, W + 5, 91); B.fx(214, W + 4, 91)
    # ---------------- outside: chimneys, engines
    for (x, z) in ((196, 66), (210, 66), (196, 76), (210, 76), (203, 94)):
        top = max(y for y in range(40, 80) if (x, y, z) in B.b) + 1
        for y in range(top, top + 7):
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    s(x + dx, y, z + dz, 'magma_block' if (dx, dz) == (0, 0) else 'polished_blackstone_bricks' if y % 3 else 'waxed_copper_block')
        s(x, top + 7, z, 'campfire[facing=north,lit=true,signal_fire=true,waterlogged=false]')
    for (x, y, r) in ((206, 44, 3), (212, 50, 2), (206, 55, 3)):
        engine(k, 'z', 1, 117, x, y, r, 5, core='ochre_froglight', rim='orange_stained_glass', plume=('orange_stained_glass', 'red_stained_glass'))
    mast(k, 200, None, 104, 10, arms=((4, 'x', 3),))
    mast(k, 216, None, 90, 8, arms=((3, 'z', 2),), tip='shroomlight')
    wing(k, 'z', 100, 118, 189, 181, 46, HULL)
    wing(k, 'z', 100, 118, 221, 229, 46, HULL)
    dress(k, sh, stripe=(50, 51), stripe_pal=('red_concrete', 'orange_terracotta', 'red_terracotta'), light='shroomlight')
    return arr, dep


# ===================================================================================================== THE NAVIGATOR
EYE = ['  ***  ', ' *   * ', '*  T  *', ' *   * ', '  ***  ']
CROWN = ['*  *  *', '** * **', '*** ***', '*  T  *', '*******']
SERPENT = [' **    ', '*  *   ', '   T  *', '    ** ', '       ']
HAND = ['* * * *', '* * * *', '*******', ' **T** ', '  ***  ']
STARP = ['   *   ', '  ***  ', '***T***', ' ** ** ', '*     *']


def constellation(k, n, mask, cx, cy, cz, ax, order, name, sign_dir):
    """a constellation on a dome wall plane: '*' bright stars set into the wall, 'T' the target at its heart; its name below"""
    for row, line in enumerate(mask):
        for col, ch in enumerate(line):
            if ch == ' ': continue
            u = col - 3
            y = cy + 2 - row
            x, z = (cx + u, cz) if ax == 'x' else (cx, cz + u)
            if ch == 'T':
                k.B.target(n, x, y, z, order=order)
            else:
                k.s(x, y, z, 'pearlescent_froglight')
    k.sign(*((cx, cy - 4, cz + sign_dir[1]) if ax == 'x' else (cx + sign_dir[0], cy - 4, cz)), sign_dir[2], [name, '', '', ''], color='magenta')


def nav(k):
    B, s = k.B, k.s
    W = 52
    sh = 'nav'
    rng = random.Random(52)
    k.room(sh, 160, W, 22, 176, W + 12, 38, wall=[('black_concrete', 1)], floor=NAV_FLOOR)   # P10 the star-dome
    k.room(sh, 163, W, 12, 173, W + 4, 18, wall=WALL, floor=FLOOR)                            # the mainframe (hidden)
    k.room(sh, 134, 44, 24, 157, W + 11, 36, wall=NAV_WALL, floor=[('air', 1)])               # P11 THE ZERO-G CROSSING
    k.room(sh, 128, W, 4, 148, W + 10, 20, wall=NAV_WALL, floor=NAV_FLOOR)                     # P12 the squadron bay
    k.round_room(sh, 110, 18, 15, W, W + 17, NAV_WALL, NAV_FLOOR, wall_h=5)                  # P13 THE OBSERVATORY
    k.hull(sh, 'x', [(92, 19, 25, 50, 57), (98, 4, 34, 44, 62), (128, 1, 40, 42, 66), (152, 2, 41, 40, 66), (176, 17, 41, 44, 68), (180, 21, 39, 46, 64)],
           HULL, chamfer=5)
    k.hull(sh, 'x', [(132, 18, 26, 66, 70), (170, 24, 36, 66, 72)], HULL_DARK, env=False, chamfer=2)
    k.hull(sh, 'x', [(120, 17, 23, 34, 41), (170, 27, 33, 36, 42)], HULL_DARK, env=False, chamfer=1)
    arr = k.tube('x', 177, 183, 30, W, HULL_DARK)
    dep = k.tube('x', 95, 90, 22, W, HULL_DARK)
    # ---------------- P10 THE STAR-DOME (targets): its walls a night sky; five constellations, struck in the chart's order
    for x in range(160, 177):
        for z in range(22, 39):
            dd = max(abs(x - 168) / 8.5, abs(z - 30) / 8.5)
            top = W + 12 - int(max(0, dd - 0.7) * 10)
            for y in range(top + 1, W + 13): s(x, y, z, 'black_concrete')
    for (x, y, z), st in list(B.b.items()):
        if 158 <= x <= 178 and 20 <= z <= 40 and W <= y <= W + 14 and st == 'minecraft:black_concrete' and rng.random() < 0.035:
            if any(k.is_air(x + a, y + b, z + c) for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0))):
                s(x, y, z, rng.choice(('sea_lantern', 'end_stone', 'white_concrete', 'sea_lantern')))
    constellation(k, 10, EYE, 165, W + 6, 21, 'x', 1, 'THE EYE', (0, 1, 'south'))
    constellation(k, 10, CROWN, 172, W + 7, 21, 'x', 2, 'THE CROWN', (0, 1, 'south'))
    constellation(k, 10, SERPENT, 165, W + 6, 39, 'x', 3, 'THE SERPENT', (0, -1, 'north'))
    constellation(k, 10, HAND, 172, W + 7, 39, 'x', 4, 'THE HAND', (0, -1, 'north'))
    constellation(k, 10, STARP, 159, W + 8, 30, 'z', 5, 'THE STAR', (1, 0, 'east'))
    k.lectern('nav', 170, W, 34, 'west')
    s(170, W, 35, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'Items': [{'Slot': Byte(i), 'id': 'minecraft:arrow', 'count': Int(32)} for i in range(4)]})
    s(170, W, 36, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'Items': [{'Slot': Byte(0), 'id': 'minecraft:bow', 'count': Int(1)}]})
    B.pz(10, 'targets', 168, W + 5, 30)
    B.voice('nav', 172, W, 30, r=6)
    B.pad(174, W, 30)
    for (x, z) in ((164, 26), (172, 26), (164, 34), (172, 34)):
        s(x, W - 1, z, 'amethyst_block')
    s(168, W - 1, 30, 'pearlescent_froglight')
    for x in range(161, 176):
        s(x, W - 1, 30, 'purpur_block' if x % 2 else 'black_concrete') if x != 168 else None
    # THE MAINFRAME CORE (the Cursor): a door in the star-dome's north wall; its sigil before it
    for x in range(166, 171):
        for y in range(W, W + 3): s(x, y, 21, 'black_concrete')
    k.air(167, W, 19, 169, W + 2, 20)
    B.hidden('mainframe', 168, W, 21, 'x', 1, 3, 'black_concrete', [('cursor', 168, W, 24)])
    k.sign(166, W + 1, 22, 'south', ['ACCESS: DENIED', 'ACCESS: DENIED', 'ACCESS: ...', '...a cursor?'], color='lime')
    for x in range(163, 174, 2):
        for z in (12, 18):
            for y in range(W, W + 4):
                s(x, y, z, rng.choice(('observer[facing=north,powered=false]', 'redstone_lamp[lit=true]', 'crafter[crafting=false,orientation=north_up,triggered=false]',
                                       'green_stained_glass', 'redstone_lamp[lit=true]', 'dispenser[facing=north,triggered=false]')))
    for x in range(163, 174):
        s(x, W - 1, 15, GL if x % 2 else 'black_concrete')
    s(165, W - 1, 15, 'gold_block'); B.relic('mainframe', 165, W, 15)
    B.chest(172, W, 15, 'west', loot='bm:p2/armada/hidden')
    # ---------------- P11 THE ZERO-G CROSSING (path): plates over the open void; the stars in the ceiling mark the way
    k.air(158, W, 29, 159, W + 3, 31)
    B.gate(158, W, 30, 'z', 10)
    k.fill(132, 34, 22, 159, 43, 38, NAV_WALL, soft=True)                     # the void under it: a shaft out through the hull
    for x in range(134, 158):
        for z in range(24, 37):
            for y in range(28, 46): B.b.pop((x, y, z), None)
    for x in range(153, 158):                                               # the start platform
        for z in range(26, 35):
            s(x, W - 1, z, k.pick(NAV_FLOOR)); s(x, W - 2, z, 'polished_deepslate'); s(x, W - 3, z, 'purpur_pillar[axis=y]') if (x + z) % 4 == 0 else None
    for x in range(134, 140):                                               # the goal platform (to the north wall: G11)
        for z in range(24, 35):
            s(x, W - 1, z, k.pick(NAV_FLOOR)); s(x, W - 2, z, 'polished_deepslate')
    safe = [(152, 30), (151, 30), (150, 30), (150, 29), (150, 28), (149, 28), (148, 28), (147, 28), (147, 29), (147, 30), (147, 31), (147, 32),
            (146, 32), (145, 32), (144, 32), (144, 31), (144, 30), (143, 30), (142, 30), (142, 29), (142, 28), (141, 28), (140, 28)]
    for x in range(140, 153):
        for z in range(28, 33):
            s(x, W - 3, z, 'polished_deepslate')
            B.plate(x, W, z, (x, z) not in safe, plate='minecraft:polished_blackstone_pressure_plate', safe_under='minecraft:red_nether_bricks')
            s(x, W - 1, z, 'purpur_block' if (x + z) % 2 else 'polished_deepslate')
    for (x, z) in safe:
        s(x, W + 12, z, 'pearlescent_froglight')
    B.start(11, 155, W, 30)
    B.goal(11, 136, W, 30)
    B.pz(11, 'path', 146, W + 5, 30)
    k.sign(157, W, 26, 8, ['ZERO-G CROSSING', 'Step only where', 'the stars above', 'point.'], color='magenta', wall=False)
    k.windows(135, 156, 36, 36, W + 1, W + 9, 0, 1, glass='glass', every=(3, 1))
    drng = random.Random(11)
    for _ in range(9):                                                      # drifting debris (well clear of the plates)
        x, y, z = drng.randint(136, 155), drng.randint(W + 5, W + 10), drng.choice((25, 35))
        for dx in (0, 1):
            if k.is_air(x + dx, y, z): s(x + dx, y, z, drng.choice(('purpur_block', 'polished_deepslate', 'amethyst_block')))
    # ---------------- P12 THE SQUADRON BAY (waves): saucers on their cradles
    k.air(135, W, 21, 137, W + 3, 23)
    B.gate(136, W, 22, 'x', 11)
    B.pz(12, 'waves', 138, W, 12)
    for (x, z) in ((130, 6), (146, 6), (130, 18), (146, 18), (138, 6)):
        B.el(12, 'wsp', x, W, z)
    for (sx_, sz_) in ((132, 12), (144, 12)):
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                d = math.hypot(dx, dz)
                if d <= 3.3: s(sx_ + dx, W + 6, sz_ + dz, 'iron_block' if d > 2.3 else 'black_concrete')
                if d <= 1.5: s(sx_ + dx, W + 7, sz_ + dz, 'green_stained_glass')
        s(sx_, W + 5, sz_, GL)
        for y in range(W + 8, W + 11): s(sx_, y, sz_, CHAIN_Y)
    for x in range(130, 148, 4):
        for z in (5, 19): s(x, W + 11, z, 'sea_lantern')
    # ---------------- P13 THE OBSERVATORY (vboss: the Star-Seer): a glass dome, amethyst ribs; a ward vault
    k.air(124, W, 11, 127, W + 3, 13)
    k.fill(124, W - 1, 11, 127, W - 1, 13, NAV_FLOOR)
    B.gate(126, W, 12, 'z', 12)
    cx, cz = 110, 18
    for (x, y, z), st in list(B.b.items()):
        if abs(x - cx) <= 18 and abs(z - cz) <= 18 and y >= W + 6 and not st.endswith(':air'):
            d = math.hypot(x - cx, z - cz)
            ang = math.degrees(math.atan2(z - cz, x - cx)) % 30
            if d <= 17.5 and any(k.is_air(x + a, y + b, z + c) for a, b, c in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, -1, 0))):
                s(x, y, z, 'amethyst_block' if ang < 3 or y % 6 == 0 else 'purple_stained_glass' if (x + y + z) % 5 == 0 else 'light_blue_stained_glass')
    for x in range(cx - 15, cx + 16):
        for z in range(cz - 15, cz + 16):
            d = math.hypot(x - cx, z - cz)
            if d <= 15:
                if abs(d - 6) < 0.6 or abs(d - 12) < 0.6: s(x, W - 1, z, 'amethyst_block')
                elif d < 1.6: s(x, W - 1, z, 'pearlescent_froglight')
    for a in range(0, 360, 60):                                              # an orrery: little worlds hung from the dome
        px, pz = round(cx + 8 * math.cos(math.radians(a))), round(cz + 8 * math.sin(math.radians(a)))
        top = max(y for y in range(W, W + 20) if k.is_air(px, y, pz))
        for y in range(W + 11, top + 1): s(px, y, pz, CHAIN_Y)
        s(px, W + 10, pz, rng.choice(('amethyst_block', 'ochre_froglight', 'prismarine', 'crying_obsidian', 'pearlescent_froglight', 'purpur_block')))
    B.vboss(13, cx, W, cz, 'nav', r=14)
    B.vault(cx, W, 5, 'south', 'akey', 'bm:p2/armada/ward')
    B.fx(cx, W + 8, cz)
    B.gate(93, W, 22, 'z', 13)
    B.pad(98, W, 22)
    B.fx(168, W + 6, 30); B.fx(146, W + 6, 30); B.fx(138, W + 5, 12)
    # ---------------- outside
    for (z, y, r) in ((23, 50, 3), (37, 50, 3), (30, 61, 2)):
        engine(k, 'x', 1, 180, z, y, r, 4, core='pearlescent_froglight', rim='light_blue_stained_glass', plume=('light_blue_stained_glass', 'purple_stained_glass'))
    for (x, z, h) in ((150, 30, 14), (140, 20, 9), (165, 30, 9)):
        mast(k, x, None, z, h, arms=((4, 'z', 3), (8, 'z', 2)), tip='amethyst_block')
    wing(k, 'x', 150, 172, 42, 50, 48, HULL)
    fin(k, 'x', 166, 180, 30, 69, 76, True, HULL_DARK)
    dress(k, sh, stripe=(55, 56), stripe_pal=('purple_concrete', 'red_concrete', 'magenta_terracotta'), light='sea_lantern')
    return arr, dep


# ===================================================================================================== THE TWIN DREADNOUGHTS
def reactor(k, n, cx, w, cz, wsp, armoury_gate=None):
    """a reactor: the core (its controller inside it), four conduit cells on plinths round it (5 out), four spawn points"""
    B, s = k.B, k.s
    for y in range(w, w + 11):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                edge = abs(dx) + abs(dz) == 2
                s(cx + dx, y, cz + dz, 'polished_blackstone' if edge else 'red_stained_glass' if (dx or dz) else 'shroomlight')
        if y % 3 == 0:
            for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)): s(cx + dx, y, cz + dz, 'iron_bars')
    B.pz(n, 'reactor', cx, w + 4, cz)
    for i, (dx, dz) in enumerate(((5, 0), (-5, 0), (0, 5), (0, -5))):
        x, z = cx + dx, cz + dz
        s(x, w, z, 'chiseled_polished_blackstone')
        s(x, w + 1, z, 'air')
        B.conduit(n, i, x, w + 1, z)
        for t in range(1, 5):                                             # power lines in the floor to the core
            px, pz = cx + dx * t // 5, cz + dz * t // 5
            s(px, w - 1, pz, 'shroomlight')
    for (x, z) in wsp:
        B.el(n, 'wsp', x, w, z)
        s(x, w - 1, z, 'red_concrete')
    ring = []
    for x in range(cx - 8, cx + 9):
        for z in range(cz - 8, cz + 9):
            if abs(math.hypot(x - cx, z - cz) - 7.5) < 0.5: ring.append((x, z))
    for (x, z) in ring: s(x, w - 1, z, 'red_terracotta' if (x + z) % 2 else 'polished_blackstone')


def dread_a(k):
    B, s = k.B, k.s
    W = 48
    sh = 'dread_a'
    k.room(sh, 70, W, 18, 78, W + 6, 26, wall=DREAD_WALL, floor=DREAD_FLOOR)       # the lobby
    k.room(sh, 46, W, 15, 66, W + 12, 35, wall=DREAD_WALL, floor=DREAD_FLOOR)      # P14 the reactor hall
    k.room(sh, 50, W, 7, 62, W + 4, 11, wall=DREAD_WALL, floor=DREAD_FLOOR)        # the armoury
    k.room(sh, 70, W, 30, 78, W + 4, 35, wall=WALL, floor=[('cyan_terracotta', 1), ('polished_deepslate', 2)])   # Zib's lost squad
    k.air(67, W, 21, 69, W + 3, 23)
    k.hull(sh, 'x', [(34, 23, 29, 44, 54), (44, 10, 40, 40, 62), (70, 12, 40, 40, 62), (77, 14, 38, 42, 58), (80, 17, 33, 44, 56)], WAR, chamfer=5)
    k.hull(sh, 'x', [(48, 18, 32, 62, 66), (62, 20, 30, 62, 67)], HULL_DARK, env=False, chamfer=2)
    k.hull(sh, 'x', [(40, 22, 28, 32, 40), (80, 23, 27, 34, 42)], HULL_DARK, env=False, chamfer=1)
    arr = k.tube('x', 79, 82, 22, W, HULL_DARK, frame='shroomlight')
    dep = k.tube('z', 36, 44, 56, W, HULL_DARK, frame='shroomlight')
    # lobby
    for z in (17, 27):
        for x in range(70, 79):
            s(x, W + 3, z, 'cyan_terracotta' if x % 3 == 0 else 'red_terracotta')
    B.voice('dread', 74, W, 22, r=6)
    B.pad(76, W, 22)
    for x in range(71, 78, 3): s(x, W + 7, 22, 'shroomlight')
    k.sign(77, W + 2, 18, 'south', ['DREADNOUGHT', 'XV-A', 'IT HAS NEVER', 'LOST.'], color='red')
    # ZIB'S LOST SQUAD: a Donadian-coded door (teal panels) in the lobby's south wall
    for x in range(72, 77):
        for y in range(W, W + 3): s(x, y, 27, 'cyan_terracotta')
    k.air(73, W, 28, 75, W + 2, 29)
    B.hidden('squad', 74, W, 27, 'x', 1, 3, 'cyan_terracotta', [('zib', 74, W, 24)])
    k.sign(71, W + 1, 26, 'north', ['A DOOR IN THE', 'OLD CODE.', 'Only a Donadian', 'could read it.'], color='aqua')
    for x in (71, 77):
        for z in (31, 34): s(x, W, z, 'cyan_carpet')
    for x in range(70, 79, 2): s(x, W + 5, 32, 'prismarine_bricks')
    s(74, W + 4, 32, 'sea_lantern')
    s(77, W - 1, 33, 'gold_block'); B.relic('squad', 77, W, 33)
    B.chest(71, W, 33, 'east', loot='bm:p2/armada/hidden')
    k.sign(74, W + 1, 35, 'north', ["ZIB'S SQUAD", 'WE WAITED.', 'WE KNEW YOU', 'WOULD COME.'], color='aqua')
    # P14 THE REACTOR
    reactor(k, 14, 56, W, 25, ((49, 18), (63, 18), (49, 32), (63, 32)))
    for x in range(48, 66, 4):
        for z in (16, 34): s(x, W + 13, z, 'shroomlight')
    for (x1, x2) in ((47, 52), (60, 65)):
        k.windows(x1, x2, 35, 35, W + 3, W + 7, 0, 1, glass='red_stained_glass', every=(1, 1))
    for (x1, x2) in ((47, 48), (64, 65)):
        k.windows(x1, x2, 15, 15, W + 3, W + 7, 0, -1, glass='red_stained_glass', every=(1, 1))
    B.fx(56, W + 6, 25)
    # the armoury (G14)
    k.air(55, W, 12, 57, W + 3, 14)
    B.gate(56, W, 13, 'x', 14)
    for x in (51, 54, 58, 61):
        B.chest(x, W, 7, 'south', loot='bm:p2/armada/ward')
    for x in range(50, 63, 3): s(x, W + 4, 9, 'shroomlight')
    # the south collar (G14, bridge 14)
    B.gate(56, W, 40, 'x', 14)
    B.pad(59, W, 33)
    # outside: the war look - turrets, red slits
    for (z, y, r) in ((30, 46, 3), (30, 54, 3), (16, 52, 2)):
        engine(k, 'x', 1, 80, z, y, r, 5, core='shroomlight', rim='red_stained_glass', plume=('red_stained_glass', 'orange_stained_glass'))
    turrets(k, [(52, 25), (64, 25)], 'x', -1)
    mast(k, 58, None, 21, 9, tip='shroomlight', arms=((4, 'z', 2),))
    wing(k, 'x', 50, 70, 12, 4, 46, WAR, light='shroomlight')
    dress(k, sh, stripe=(51, 52, 58), stripe_pal=('red_concrete', 'red_terracotta'), light='shroomlight')
    return arr, dep


def turrets(k, spots, axis, sgn):
    """dorsal gun turrets: a domed base on the hull's back, two long barrels toward the prow"""
    B, s = k.B, k.s
    for (x, z) in spots:
        y = col_top(k, x, z)
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if abs(dx) + abs(dz) <= 3:
                    s(x + dx, y, z + dz, 'polished_blackstone')
                    if abs(dx) + abs(dz) <= 1: s(x + dx, y + 1, z + dz, 'black_concrete')
        s(x, y + 2, z, 'red_stained_glass')
        for i in range(1, 8):
            for o in (-1, 1):
                px, pz = (x + sgn * (i + 1), z + o) if axis == 'x' else (x + o, z + sgn * (i + 1))
                if (px, y + 1, pz) not in B.b: s(px, y + 1, pz, 'polished_blackstone_wall' if i < 7 else 'shroomlight')


def dread_b(k):
    B, s = k.B, k.s
    W = 52
    sh = 'dread_b'
    k.room(sh, 30, W, 64, 38, W + 6, 74, wall=DREAD_WALL, floor=DREAD_FLOOR)       # the lobby
    k.room(sh, 12, W, 78, 38, W + 10, 98, wall=DREAD_WALL, floor=DREAD_FLOOR)      # P15 the hangar
    k.room(sh, 14, W, 102, 36, W + 12, 118, wall=DREAD_WALL, floor=DREAD_FLOOR)    # P16 the reactor hall
    k.room(sh, 40, W, 106, 44, W + 4, 114, wall=DREAD_WALL, floor=DREAD_FLOOR)     # the armoury
    k.room(sh, 3, W, 87, 7, W + 3, 93, wall=WALL, floor=FLOOR)                     # secret 2
    k.air(33, W, 75, 35, W + 3, 77)
    k.hull(sh, 'z', [(58, 22, 34, 46, 58), (66, 10, 42, 44, 62), (110, 10, 40, 44, 64), (118, 18, 32, 46, 60), (121, 22, 28, 50, 57)], WAR, chamfer=5)
    k.hull(sh, 'z', [(70, 20, 30, 64, 69), (94, 20, 30, 64, 70)], HULL_DARK, env=False, chamfer=2)
    k.hull(sh, 'z', [(70, 23, 27, 36, 44), (114, 23, 27, 37, 44)], HULL_DARK, env=False, chamfer=1)
    arr = k.tube('x', 39, 44, 70, W, HULL_DARK, frame='shroomlight')
    dep = k.tube('z', 119, 124, 25, W, HULL_DARK, frame='shroomlight')
    B.pad(36, W, 70)
    k.sign(31, W + 2, 64, 'south', ['DREADNOUGHT', 'XV-B', '', ''], color='red')
    for x in range(31, 38, 3): s(x, W + 7, 69, 'shroomlight')
    # P15 THE HANGAR (waves): parked saucers, crates
    B.pz(15, 'waves', 25, W, 88)
    for (x, z) in ((14, 80), (36, 80), (14, 96), (36, 96), (25, 80)):
        B.el(15, 'wsp', x, W, z)
    for (sx_, sz_) in ((19, 92), (31, 92)):
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                d = math.hypot(dx, dz)
                if d <= 3.3: s(sx_ + dx, W + 1, sz_ + dz, 'iron_block' if d > 2.3 else 'black_concrete')
                if d <= 1.5: s(sx_ + dx, W + 2, sz_ + dz, 'red_stained_glass')
        s(sx_, W, sz_, 'polished_blackstone')
    for x in range(14, 38, 4):
        for z in (79, 97): s(x, W + 11, z, 'shroomlight')
    for x in range(13, 38):
        s(x, W - 1, 88, 'yellow_concrete' if x % 2 else 'black_concrete')
    # SECRET 2: a button on the side of a crate stack in the north-west corner; the door in the west wall
    for (x, z, h) in ((13, 79, 3), (14, 79, 2), (13, 80, 2)):
        for y in range(W, W + h): s(x, y, z, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel'})
    B.sbutton(15, W, 79, 'polished_blackstone_button[face=wall,facing=east,powered=false]', 2)
    for z in range(87, 94):
        for y in range(W, W + 4): s(11, y, z, 'polished_deepslate')
    k.air(8, W, 90, 10, W + 1, 90)
    B.sdoor(11, W, 90, 2)
    s(5, W - 1, 90, 'gilded_blackstone'); B.relic('secret2', 5, W, 90)
    B.chest(4, W, 92, 'east', loot='bm:p2/armada/hidden')
    s(5, W + 3, 88, 'shroomlight')
    # P16 THE REACTOR (G15 before it)
    k.air(24, W, 99, 26, W + 3, 101)
    B.gate(25, W, 100, 'x', 15)
    reactor(k, 16, 25, W, 110, ((17, 104), (33, 104), (17, 116), (33, 116)))
    for x in range(16, 36, 4):
        for z in (103, 117): s(x, W + 13, z, 'shroomlight')
    B.fx(25, W + 6, 110); B.fx(25, W + 5, 88)
    # the armoury (G16)
    k.air(37, W, 109, 39, W + 3, 111)
    B.gate(38, W, 110, 'z', 16)
    for z in (107, 113): B.chest(43, W, z, 'west', loot='bm:p2/armada/ward')
    s(42, W + 4, 110, 'shroomlight')
    # the prow collar (G16, bridge 16)
    B.gate(25, W, 121, 'x', 16)
    B.pad(28, W, 117)
    k.windows(12, 12, 80, 96, W + 3, W + 6, -1, 0, glass='red_stained_glass', every=(2, 3))
    for (x, y, r) in ((20, 50, 3), (30, 50, 3), (25, 59, 3)):
        engine(k, 'z', -1, 58, x, y, r, 5, core='shroomlight', rim='red_stained_glass', plume=('red_stained_glass', 'orange_stained_glass'))
    turrets(k, [(25, 78), (25, 92)], 'z', 1)
    mast(k, 21, None, 84, 9, tip='shroomlight', arms=((4, 'x', 2),))
    wing(k, 'z', 96, 116, 42, 50, 50, WAR, light='shroomlight')
    dress(k, sh, stripe=(55, 56, 62), stripe_pal=('red_concrete', 'red_terracotta'), light='shroomlight')
    return arr, dep


# ===================================================================================================== THE FLAGSHIP
def bearing_cell(r, deg, y=None):
    a = math.radians(deg)
    return round(AC[0] + r * math.cos(a)), round(AC[2] + r * math.sin(a))


PYLONS = []
for _i, _off in enumerate((45, 135, 225, 315)):
    _a = math.radians(WIN + _off)
    _px, _pz = round(AC[0] + AR['pylon_r'] * math.cos(_a)), round(AC[2] + AR['pylon_r'] * math.sin(_a))
    _ix, _iz = -math.cos(_a), -math.sin(_a)                    # toward the centre: the crystal's side
    _f = (round(_ix) if abs(_ix) >= abs(_iz) else 0, 0 if abs(_ix) >= abs(_iz) else round(_iz))
    PYLONS.append((_i, _px, _pz, (_px + 2 * _f[0], AR['pylon_y'][1], _pz + 2 * _f[1])))


def arena_ceil(r):
    """the bridge's inside top over radius r (the wall to y66, the dome to y84 - its top layer)"""
    return 66 + int(round(17 * math.sqrt(max(0.0, 1 - (r / 30.8) ** 2))))


def flag(k):
    B, s = k.B, k.s
    W = 55
    sh = 'flag'
    rng = random.Random(55)
    cx, fy, cz = AC                                         # (52, 54, 180): the floor's top layer
    R = AR['r']
    # ---------------- THE BRIDGE: floor r30 (y53..54), wall r30..32.5, the dome; the window on the star's arc
    for x in range(cx - 34, cx + 35):
        for z in range(cz - 34, cz + 35):
            d, ang = polar(x, z, cx, cz)
            if d > 33: continue
            win = abs(angdiff(ang, WIN)) <= 55
            if d <= R + 0.5:
                s(x, fy - 1, z, 'polished_blackstone')
                ring = int(d) % 6
                s(x, fy, z, 'gold_block' if abs(d - 10) < 0.5 or abs(d - 20) < 0.5 else GL if abs(d - 25) < 0.5 else
                  'black_concrete' if ring in (0, 1) else 'polished_blackstone' if ring in (2, 3) else 'polished_deepslate')
                top = arena_ceil(d)
                for y in range(W, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 3): s(x, y, z, 'black_concrete' if (x + z) % 7 else 'polished_blackstone')
            else:
                top = arena_ceil(max(0, d - 2.5)) + 2
                for y in range(fy - 2, top + 1):
                    if win and W <= y <= 79: st = 'glass'
                    else: st = 'black_concrete' if (y + int(ang // 8)) % 5 else 'polished_blackstone'
                    s(x, y, z, st)
    # the window's mullions (every 11 degrees) and transoms
    for x in range(cx - 34, cx + 35):
        for z in range(cz - 34, cz + 35):
            d, ang = polar(x, z, cx, cz)
            if not (R + 0.5 < d <= 33): continue
            a = angdiff(ang, WIN)
            if abs(a) > 55: continue
            for y in range(W, 80):
                if B.b.get((x, y, z)) != 'minecraft:glass': continue
                if abs(abs(a) - 55) < 1.2 or abs(a - 11 * round(a / 11)) < 0.9 or y in (W + 9, W + 18):
                    s(x, y, z, 'polished_blackstone' if y not in (W + 9, W + 18) else 'gold_block' if (x + z) % 3 == 0 else 'black_concrete')
    # the dome: ribs of gold and black, a ring of green command lights; the glass climbs into it on the star's side
    for x in range(cx - 33, cx + 34):
        for z in range(cz - 33, cz + 34):
            d, ang = polar(x, z, cx, cz)
            if d > R + 0.5: continue
            top = arena_ceil(d)
            a = angdiff(ang, WIN)
            if abs(a) <= 55 and d >= 19 and top < 80:
                s(x, top + 1, z, 'glass'); s(x, top + 2, z, 'glass')
            elif int(ang) % 30 == 0 and d > 4: s(x, top + 1, z, 'gold_block')
            elif abs(d - 14) < 0.5 or abs(d - 24) < 0.5: s(x, top + 1, z, GL)
            elif d < 2.5: s(x, top + 1, z, 'gold_block' if d > 1.5 else GL)
    # buttresses round the solid part of the wall, with gold caps and green lamps
    for a in range(0, 360, 15):
        if abs(angdiff(a, WIN)) <= 62: continue
        bx, bz = bearing_cell(R - 0.2, a)
        if abs(bx - 29) <= 3 and abs(bz - 199) <= 4: continue                     # (the battle door)
        for y in range(W, 66):
            s(bx, y, bz, 'polished_blackstone' if y % 5 else 'gold_block')
        s(bx, W + 6, bz, GL)
    # the four shield pylons, 3x3, y55..61, each with its crystal cell on its inward face
    for (i, px, pz, cell) in PYLONS:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for y in range(AR['pylon_y'][0], AR['pylon_y'][1] + 1):
                    edge = abs(dx) + abs(dz) == 2
                    s(px + dx, y, pz + dz, 'gold_block' if y == AR['pylon_y'][1] and not edge else 'polished_blackstone' if edge else
                      'black_concrete' if (y - W) % 3 else GL)
        for dx in (-2, -1, 0, 1, 2):
            for dz in (-2, -1, 0, 1, 2):
                if max(abs(dx), abs(dz)) == 2 and (dx, dz) != (cell[0] - px, cell[2] - pz):
                    s(px + dx, fy, pz + dz, 'gold_block')
        s(px, AR['pylon_y'][1] + 1, pz, 'end_rod[facing=up]')
        B.pylon(i, *cell)
    # the helm: a gold-ringed platform, flush, a console arc behind it; the housing over the Hive Vault's stair
    hx, _, hz = AR['helm']
    for x in range(hx - 3, hx + 4):
        for z in range(hz - 3, hz + 4):
            d = math.hypot(x - hx, z - hz)
            if d <= 3.2: s(x, fy, z, 'gold_block' if d > 2.4 else GL if d < 0.8 else 'chiseled_polished_blackstone')
    B.helm(hx, W, hz)
    B.voice('helm', hx - 6, W, hz + 5, r=8)
    # the housing: x71..77 z160..170, y55..61, hollow; the vault door on its west face; a stair down inside it
    for x in range(71, 78):
        for z in range(160, 171):
            for y in range(W, 62):
                edge = x in (71, 77) or z in (160, 170) or y == 61
                s(x, y, z, ('black_concrete' if (y + z) % 4 else 'gold_block') if edge else 'air')
    for z in range(160, 171): s(70, W, z, 'polished_blackstone_slab[type=bottom,waterlogged=false]') if z not in range(163, 168) else None
    for y in range(W + 1, W + 4):
        for z in (161, 169): s(70, y, z, GL) if y == W + 2 else None
    # the stair: from (72, 55) down one a block east to walk 47 at x80, then the Hive Vault
    for i, x in enumerate(range(72, 81)):
        w = W - i
        for z in range(164, 167):
            s(x, w - 1, z, 'polished_blackstone' if i == 0 else 'polished_blackstone_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
            s(x, w - 2, z, 'polished_blackstone')
            top = 60 if x <= 76 else w + 3
            for y in range(w, top + 1): s(x, y, z, 'air')
            if x > 76: s(x, w + 4, z, 'black_concrete')
        for z in (163, 167):
            for y in range(w - 2, (61 if x <= 76 else w + 5)):
                if not (x <= 77 and y >= W) : s(x, y, z, 'polished_blackstone')
    k.room(sh, 81, 47, 158, 92, 51, 172, wall=FLAG_WALL, floor=FLAG_FLOOR)
    k.air(80, 47, 164, 80, 50, 166)
    B.hive_vault(71, W, 165, 'z', 1, 4, 'gilded_blackstone')
    k.sign(70, W + 2, 162, 'west', ['THE HIVE VAULT', 'Six sigils of', 'forgotten rooms', 'open it.'], color='lime')
    # the Hive Vault: gold, green, the victor's vault, the hoard, a rift, the Admiral's last log
    for x in range(81, 93):
        for z in range(158, 173):
            if (x + z) % 4 == 0: s(x, 46, z, 'gold_block')
    B.vault(91, 47, 165, 'west', 'akey_victor', 'bm:p2/armada/victor')
    for (x, z) in ((84, 159), (88, 159), (84, 171), (88, 171)):
        B.chest(x, 47, z, 'south' if z == 159 else 'north', loot='bm:p2/armada/hoard')
    for (x, z) in ((83, 161), (86, 170), (90, 160)):
        s(x, 47, z, 'gold_block'); s(x, 48, z, 'raw_gold_block') if x == 83 else None
    s(89, 46, 168, 'crying_obsidian'); B.rift(89, 47, 168)
    k.lectern('helm', 86, 47, 165, 'west')
    for x in range(82, 92, 3):
        for z in (161, 169): s(x, 52, z, GL)
    s(86, 52, 165, 'gold_block')
    # ---------------- the hull: a great saucer round the bridge, its keel, the prow (south); the command spine (west)
    sm = np.zeros(A.SIZE, bool)
    for x in range(cx - 46, cx + 47):
        for z in range(cz - 46, cz + 47):
            d = math.hypot(x - cx, z - cz)
            if d > 46 or not (0 <= x < SX and 0 <= z < SZ): continue
            f = d / 46.0
            yb = round(53 - 13 * math.sqrt(max(0.0, 1 - f ** 2)))
            yt = 57 if d <= 36 else round(57 - (d - 36) * 0.45)
            for y in range(yb, yt + 1): sm[x, y, z] = True
    k.paint(sh, sm, FLAG_WALL, skin=2, axis='z', panel=(6, 3, 6))
    spine = [k.room(sh, 8, W, 140, 32, W + 7, 150, wall=FLAG_WALL, floor=FLAG_FLOOR),     # P17 THE COMMAND LOCK
             k.room(sh, 6, W, 154, 10, W + 5, 214, wall=FLAG_WALL, floor=FLAG_FLOOR),     # P18 THE GAUNTLET
             k.room(sh, 14, W, 192, 25, W + 7, 216, wall=FLAG_WALL, floor=FLAG_FLOOR)]    # the antechamber
    k.air(26, W, 197, 29, W + 5, 201)                                             # the battle door's vestibule
    k.fill(26, fy, 197, 29, fy, 201, 'polished_blackstone')
    k.fill(26, fy - 1, 197, 29, fy - 1, 201, 'polished_blackstone')
    for z in (196, 202):
        for x in range(25, 30):
            for y in range(W, W + 7): s(x, y, z, 'black_concrete' if y < W + 6 else 'gold_block')
    k.fill(25, W + 6, 197, 29, W + 6, 201, 'black_concrete')
    k.hull(sh, 'z', [(134, 2, 16, 50, 64), (214, 2, 16, 50, 64), (220, 6, 14, 51, 62)], HULL_DARK, chamfer=4, boxes=spine)
    k.hull(sh, 'z', [(212, 30, 74, 46, 58), (226, 40, 64, 48, 56), (236, 50, 54, 51, 54)], HULL_DARK, env=False, chamfer=4)      # the prow
    arr = k.tube('z', 139, 132, 25, W, HULL_DARK)
    # ---------------- P17 THE COMMAND LOCK: three Cipher slots before the sealed bulkhead
    for x in range(9, 32):
        for y in range(W + 1, W + 6):
            if (x, y, 151) in B.b and not k.is_air(x, y, 151): s(x, y, 151, 'gold_block' if y == W + 5 else 'black_concrete')
    for (x, key, nm) in ((14, 'c1', 'CIPHER I'), (20, 'c2', 'CIPHER II'), (26, 'c3', 'CIPHER III')):
        B.sock(17, x, W + 1, 146, key)
        for dx in (-1, 1): s(x + dx, W, 146, 'gold_block')
        s(x, W, 147, 'gold_block')
        s(x, W + 4, 151, GL)
        k.sign(x, W + 2, 150, 'north', [nm, '', 'Drop it on', 'its slot.'], color='lime')
    B.pz(17, 'xsock', 20, W + 3, 146)
    B.voice('flag', 24, W, 142, r=6)
    B.pad(25, W, 142)
    for x in range(10, 32, 4): s(x, W + 8, 145, GL)
    k.windows(9, 31, 140, 140, W + 2, W + 5, 0, -1, every=(3, 1))
    k.sign(31, W + 2, 141, 'west', ['THE COMMAND', 'LOCK', 'THREE CIPHERS,', 'THREE GUARDIANS.'], color='lime')
    # ---------------- G17 the bulkhead -> P18 THE GAUNTLET
    k.air(7, W, 151, 9, W + 3, 153)
    B.gate(8, W, 152, 'x', 17)
    B.start(18, 8, W, 155)
    B.goal(18, 8, W, 213)
    B.pz(18, 'gauntlet', 8, W + 3, 184)
    B.voice('gauntlet', 8, W, 157, r=5)
    for z in range(154, 215):
        s(8, fy, z, 'iron_block' if z % 2 else 'black_concrete')
        if z % 3 == 0:
            s(8, W + 6, z, 'shroomlight')
            for x in (6, 10): s(x, W + 6, z, 'red_stained_glass')
    n_ = 0
    for i, z in enumerate(range(159, 212, 6)):
        if i % 2 == 0: ex, cx_, f = 5, 6, 'east'
        else: ex, cx_, f = 11, 10, 'west'
        s(ex, W + 1, z, f'observer[facing={f},powered=false]')
        for dy in (0, 2):
            s(ex, W + dy, z, 'red_stained_glass')
        B.sentry(18, cx_, W + 1, z, f, 5)
        n_ += 1
    k.sign(10, W + 2, 154, 'south', ['THE GAUNTLET', 'Move between', 'the sweeps.', ''], color='red')
    # the Command Lock's key vault (at the gauntlet's head)
    k.air(11, W, 156, 11, W + 2, 156)
    B.vault(12, W, 156, 'west', 'akey', 'bm:p2/armada/ward')
    # ---------------- G18 -> THE ANTECHAMBER: the spoils vault, a rift, the battle door
    k.air(11, W, 211, 13, W + 3, 213)
    B.gate(12, W, 212, 'z', 18)
    B.vault(16, W, 194, 'east', 'akey', 'bm:p2/armada/vault')
    s(23, W - 1, 214, 'crying_obsidian'); B.rift(23, W, 214)
    for z in range(194, 216, 4): s(20, W + 8, z, GL)
    for x in (15, 24):
        for z in range(193, 216, 5):
            for y in range(W, W + 8): s(x, y, z, 'black_concrete' if y % 4 else 'gold_block')
    k.sign(23, W + 1, 216, 'north', ['A WAY HOME,', 'FOR AFTER.', '', ''], color='gray')
    B.gate(27, W, 199, 'z', 0, big=True)
    B.arena(cx, W, cz)
    for j in range(6):
        a = math.radians(WIN + 30 + 60 * j)
        B.mspawn(round(cx + 11 * math.cos(a)), W, round(cz + 11 * math.sin(a)))
    B.fx(cx, W + 10, cz); B.fx(cx + 15, W + 6, cz); B.fx(cx - 15, W + 6, cz); B.fx(8, W + 3, 184); B.fx(20, W + 3, 145)
    # ---------------- outside: the antenna crown on the dome, engines (north), the prow's lights
    for a in range(0, 360, 40):
        if abs(angdiff(a, WIN)) < 40: continue
        mx, mz = bearing_cell(31.5, a)
        top = max(y for y in range(50, 95) if (mx, y, mz) in B.b and not k.is_air(mx, y, mz)) + 1
        if top < 90: mast(k, mx, top, mz, min(8, 92 - top), tip=GL)
    mast(k, cx, 86, cz, 6, tip='gold_block')
    for (x, y, r) in ((44, 50, 3), (60, 50, 3), (52, 46, 3)):
        engine(k, 'z', -1, 134, x, y, r, 6)
    dress(k, sh, stripe=(52,), stripe_pal=('red_concrete', 'black_concrete'), light=GL)
    return arr


# ===================================================================================================== finishing passes
def zones(k, reach=26):
    """a zone marker within `reach` of every floor a player can stand on"""
    B = k.B
    from p2.verify import passable
    zs, idx = [], {}
    def near(p):
        bx, by, bz = p[0] // 24, p[1] // 24, p[2] // 24
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for q in idx.get((bx + a, by + b, bz + c), ()):
                        if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2 <= reach * reach: return True
        return False
    cells = sorted(c for c, st in B.b.items() if st.endswith(':air') and passable(B.b.get((c[0], c[1] + 1, c[2])) or 'minecraft:air')
                   and (c[0], c[1] - 1, c[2]) in B.b and not passable(B.b[(c[0], c[1] - 1, c[2])]))
    for c in cells:
        if not near(c):
            zs.append(c); idx.setdefault((c[0] // 24, c[1] // 24, c[2] // 24), []).append(c); B.zone(*c)
    return len(zs)


def tidy(k):
    """keep the gates' fill boxes clean (their open/close fills replace any gate glass or light in the box), and prove the
    lava can't go anywhere: every lava cell has only lava or solid blocks beside and under it"""
    from p2.config import OPEN_LIGHT, ADOOR_LIGHT, GATE_H, BIG_W, BIG_H
    from p2.verify import passable
    B = k.B
    bad = ('minecraft:' + A.CFG['gate'].split(':')[1], OPEN_LIGHT, ADOOR_LIGHT)
    for (x, y, z, ax, n) in B.meta['gates']:
        for dx in (-1, 0, 1):
            for dy in range(GATE_H):
                for dz in (-1, 0, 1):
                    if (dz == 0 if ax == 'x' else dx == 0): continue
                    if B.b.get((x + dx, y + dy, z + dz)) in bad: B.set(x + dx, y + dy, z + dz, 'polished_blackstone')
    for (x, y, z, ax) in B.meta['big']:
        for dx in range(-BIG_W, BIG_W + 1):
            for dy in range(BIG_H):
                for dz in range(-BIG_W, BIG_W + 1):
                    if (dz == 0 if ax == 'x' else dx == 0): continue
                    if B.b.get((x + dx, y + dy, z + dz)) in bad: B.set(x + dx, y + dy, z + dz, 'polished_blackstone')
    loose = []
    for (x, y, z), st in list(B.b.items()):
        if st.endswith(':water') or 'waterlogged=true' in st: loose.append(((x, y, z), st))
        if not st.startswith('minecraft:lava'): continue
        for q in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1), (x, y - 1, z)):
            n = B.b.get(q)
            if n is None or (not n.startswith('minecraft:lava') and passable(n) is not False): loose.append((q, n))
    if loose: raise ValueError(f'armada: lava (or water) loose at {loose[:6]}')


def build():
    B = A.ABuild(seed=29901)
    k = K(B)
    hive_star(k)
    d_mouth = dock(k)
    b_arr, b_dep = brood(k)
    f_arr, f_dep = forge(k)
    n_arr, n_dep = nav(k)
    a_arr, a_dep = dread_a(k)
    bb_arr, bb_dep = dread_b(k)
    fl_arr = flag(k)
    # ---------------- THE HARD-LIGHT BRIDGES (deck y = walk - 1), in the order the trials switch them on
    span(k, 1, [(d_mouth[0] + 1, 205, b_arr[0] - 1, 207, 49, 45)])                                # the Dock -> the Brood-Carrier
    span(k, 5, [(197, b_dep[2] - 1, 199, f_arr[2] + 1, 45, 47)])                                 # the Brood-Carrier -> the Star-Forge
    span(k, 9, [(203, f_dep[2] - 1, 205, 29, 47, 47), (202, 29, n_arr[0] + 1, 31, 47, 51)])     # the Star-Forge -> the Navigator
    span(k, 13, [(n_dep[0] - 1, 21, a_arr[0] + 1, 23, 51, 47)])                                  # the Navigator -> Dreadnought A
    span(k, 14, [(55, a_dep[2] + 1, 57, 71, 47, 51), (54, 69, bb_arr[0] + 1, 71, 51, 51)])       # Dreadnought A -> Dreadnought B
    span(k, 16, [(24, bb_dep[2] + 1, 26, fl_arr[2] - 1, 51, 54)])                                # Dreadnought B -> the Flagship
    def bounds(m):
        xs, ys, zs = (np.nonzero(m.any(axis=ax))[0] for ax in ((1, 2), (0, 2), (0, 1)))
        return (int(xs[0]), int(ys[0]), int(zs[0]), int(xs[-1]), int(ys[-1]), int(zs[-1]))
    B.meta['armada']['ships'] = {nm: bounds(m) for nm, m in k.ship_mask.items()}
    zones(k)
    tidy(k)
    return B
