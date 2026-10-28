"""THE UNDERCROWN (2.98): the final dungeon - the Dread Sovereign's hall, cut into the Nether's rock (224 x 112 x 224 at
undercfg.ORIGIN; only what is set here is placed, so the Nether's own rock stays round it; UBuild.seal wraps it all in reinforced
deepslate). p2/undercfg.py holds the arena, the trials' order, the sigils and the hidden rooms; phase237 runs it.

Walk y in brackets. North is -z. The Hall of Chains' axis is (112, 145).
  THE APPROACH (outside: B.outside, never sealed) - an ash cave x191..223 z190..223 (99), open to the template's east and south
      edges by rough tunnels. Its west wall is a sheer basalt cliff (x191) with a seam of crying obsidian (z206..208, 5 high): THE
      HIDDEN GATE. Three token hollows at chest height, each with one red candle: snow z197, shark z202, witch z212.
  THE TUNNEL - from the seam (entrance marker, the 'gate' voice) 5 wide and 7 tall, ribbed, chained, west along z207 (99 -> 95),
      north along x152 (-> 92), west along z166 to the Hall's rim. Red glass lavafalls glow at the end of each leg.
  THE HALL OF CHAINS (hub, controller) - a shaft r27.5 from a lava pool (y14..16, under a tinted glass floor at y17) to a dome at
      y104; twelve ribbed piers (the two by the Throne Gate are statues instead), five giant chains of 5x7 links, iron chains
      with soul lanterns. Tinted glass floors span the shaft at every ward (y77, 51, 35). THE STAIR is a 3-wide, 5-tall corridor
      inside the wall (r29.5..32.5) winding down one and a half turns: the rim (92: the warden's lectern, the 'hall' voice, a
      caged balcony over the shaft) -> FROZEN LANDING (78, west) -> G5 -> the north turn (64) -> HEXED LANDING (52, east) -> G10
      -> DROWNED LANDING (36, south) -> G15 -> the HUB FLOOR RING (18). Its windows onto the shaft are barred low, open above.
  THE FROZEN WARD (78, x8..72 z29..170)
      P1  sigil: Pistachio, on the landing, before the hat-lock door (a top hat of packed ice)          -> G1
      P2  targets: THE FROZEN FALLS x28..55 z128..168 - icicles hang from its vault, snow drifts against its walls; seven-wide
          frozen lavafalls (two silent ones), each with a target in a framed sign: claw (4) and
          hat (1) on the west wall, empty frame (5) and snowflake (2) on the south, icicle (3) on the north. The verse
          (BOOKS['frozen']) is on the lectern; a barrel of arrows beside it                                -> G2
      P3  sigil: Celi (32,78,121) + Tullius (52,78,121) on the near shore of a lava lake (z101..117) -> bridge 3 (packed ice,
          x41..43) and G3 on the far shore
      P4  waves: THE FROSTBOUND THRALLS x26..58 z62..93 (six spawn points)                               -> G4
      P5  echo (snow): a round frozen arena, centre (42,78,44), r15; a ward vault                         -> G5: a frozen gallery
          (x63..65) back south to the vestibule - and the stair's own G5 below the landing
  THE LANTERN CRAWL (hidden: lantern) - a 12x11-cell maze x92..132 z68..105 (64), 2-wide 3-tall corridors, no light at all;
      bm.udark at its centre (r24, short of the stair). Its door is in the stair's outer wall at the north turn (112,64,111).
  THE HEXED WARD (52, x152..218 z84..186)
      P6  sigil: Cecil, in the entry hall x154..169 z126..142 before the library doors                  -> G6
      P7  lights: THE INVERTED LIBRARY x172..204 z110..154, bookshelves hanging from a purple ceiling; the 4x4 hex board in the
          east wall (bulbs) with its 4x4 buttons on a plinth before it (same layout); BOOKS['witch']   -> G7
      P8  sigil: Apophiss, in the serpent's room x180..196 z97..107                                      -> G8: THE SERPENT CRAWL,
          2 wide, 3 tall, scale-tiled, meandering north and then south down the east side to
      P9  sigil: King Omega, in the bone room x202..216 z158..168                                       -> G9: THE OSSUARY x184..200
      P10 echo (witch): a round hex arena, centre (163,52,170), r15; a ward vault                         -> G10: a corridor north to
          the entry hall - and the stair's own G10 below the landing
  THE DROWNED WARD (x44..154 z177..222) - a great lava cavern (lava y7..9, its vault rising to ~y78 over the ship) with the
      Kingdom's warship hung in it by colossal chains, a dozen blocks over the drop, its bow rammed into the cavern's west rock. Hull x93..146 z195..216: hold (24), gun deck (33), main deck (38).
      P11 sigil: Queen Pearl, on the ledge (36) before the gangway's gatehouse                          -> G11
      P12 simon: THE KINGDOM'S SONG - five bells on the main deck, a button on each bell's plinth; the conch (listen button) on
          the mainmast; BOOKS['drowned']                                                                 -> G12: the companionway down
      P13 sigil: Emma (112,33,200) + Bones (124,33,211) on the gun deck                                  -> G13: the keel stair down
      P14 waves: THE DRIED DROWNED in the hold x105..140 z196..215                                      -> G14: the bow, a breach into
          the rock, a tunnel west and down to
      P15 echo (shark): the dried sea-bed, centre (66,22,200), r16, dome to 40; a ward vault             -> G15: a tunnel north and
          east into the Hall's floor ring (and the stair's own G15 below the landing)
  THE HUB FLOOR RING (18)
      P16 shards: THE THRONE GATE (north) - six G16 gates make one door 9 wide and 8 tall, framed; the Snowbeast and the Witch
          stand either side of it in blackstone, the Sawshark over it. Three sockets on pedestals (snow, witch, shark), the
          trial's controller over the middle one, the 'shards' voice                                      -> G16
      P17 reach: THE STAIR OF A THOUSAND EYES x109..115 z90..115 - a ribbed gallery 7 wide, ~15 tall, down from 18 to 13; 42
          eyes (shut lids) on its walls, 8 knight spawns; start at the top, goal at the foot             -> G17
  THE ANTECHAMBER x96..128 z80..88 (13) - BOOKS['ante'], the spoils vault (ukey), the victor's vault (ukey_victor), a rift
      home, the 'ante' voice; the battle door (big, open) north into
  THE THRONE OF THE DREAD - exactly undercfg.ARENA: the floor (y11..12) over air (7..10) over the lava sea (2..6), the dome
      to 64; six pillars (r26, on islands r6, on rock cones), each with its Wellspring's air cell at y16 on its inward face and
      chains wound round it; obsidian slabs on three islands; the outer floor is void-glass with red cracks (it falls in phase
      3). THE THRONE (112,13,11): a colossus' seat of red nether brick and gilded blackstone edged in crying obsidian, its spikes
      tipped with light, standing in a black apse cut into the north wall and dome, a great red rose window burning behind it
      and chains radiating from its crown into the dome. It stands on its dais: meta['under']['dais'] lists the dais' columns - its own island, solid down to the
      sea floor and joined to the two northern pillars' islands; the fight must leave it standing. Chains run from the
      throne to the six pillars. A rift by the throne, for after. Behind the throne's arch: THE HOARD's door (z7) and the Hoard,
      a crescent behind the north wall (gold, three chests, the 'hoard' voice).
HIDDEN ROOMS (undercfg.HIDDEN: each a door that looks like its wall, its followers' sigils beside it, a sign, a relic, a chest)
  last_light  the Lightbringer's sigil in the antechamber (99,13,84); the door in its west wall -> a white chapel under a coved
              quartz vault: pews, a gold-trimmed altar under a stained-glass sun lit from behind, candles, banners, BOOKS['vigil'],
              the 'last_light' voice
  lantern     the Arachno-Lantern's sigil on the stair at the north turn (112,64,114); the door in the outer wall -> the maze
  archive     the Eraser's sigil in the Hexed entry hall (161,52,129); the door is a white_concrete patch in the north wall,
              "painted over" -> the Erased Archive, BOOKS['unwritten']
  forge       Bender's sigil on the hub floor ring (135,18,145); the door is one of the ring's iron-bar grilles (east) -> the
              Chainmaker's Forge (anvils, a lava quench, chain racks), BOOKS['chains']
  nine        Henry (64,78,97) and Nia (64,78,103) in the Frozen gallery; a 1x2 cat-flap in a timbered panel of its east wall ->
              Nine Lives, a 2-high room
  ossuary     Wilfrey's sigil in the Hexed ossuary (192,52,168); the door in its bone south wall -> the Unbound Knights' tomb
SECRETS (the classic kind: cracked nether brick doors, a hidden button each, a chest behind)
  1  THE CHAIN: on the stair just past the rim, due south (walk 88), chains hang against the outer wall; behind the middle
     one, low at its foot, a button (112,88,177). The door opens two blocks east (114,88,178): a small room.
  2  LOOK UP: in the inverted library, one shelf stack hangs low (x188 z120, its foot at y55); a button on its underside
     (188,54,120). The door is in the north-east closet's wall (201,52,115)."""
import math
import random
from nbt import Int, Byte
import undercrown_lore as L
from p2 import undercfg as U
from p2.config import SEQS

SX, SY, SZ = U.SIZE
HX, HZ = 112, 145                          # the Hall of Chains' axis
SHAFT_R, IN_R, COR_R, OUT_R = 27.5, 29.5, 32.5, 35.5     # shaft air / inner wall / stair corridor / outer wall (radii)
# the spiral stair: (Theta, walk y) knots; Theta is the angle (x=cos, z=sin, degrees) unwound - it goes round more than once
KNOTS = [(30, 92), (62, 92), (84, 88), (96, 88), (166, 78), (196, 78), (262, 64), (278, 64), (326, 52), (362, 52),
         (430, 36), (460, 36), (560, 18), (566, 18)]
T0, T1 = KNOTS[0][0], KNOTS[-1][0]
FROZEN_Y, HEXED_Y, DROWNED_Y, FLOOR_Y, RIM_Y = 78, 52, 36, 18, 92

VOID = [('polished_blackstone_bricks', 5), ('deepslate_tiles', 3), ('deepslate_bricks', 2), ('cracked_polished_blackstone_bricks', 1),
        ('blackstone', 1)]
FLOOR = [('polished_blackstone', 3), ('deepslate_tiles', 2), ('polished_deepslate', 2), ('polished_blackstone_bricks', 1)]
RED = [('red_nether_bricks', 5), ('nether_wart_block', 1), ('crimson_planks', 1)]
ROCK = [('blackstone', 4), ('basalt[axis=y]', 2), ('netherrack', 2), ('deepslate', 1)]
ICE = [('packed_ice', 6), ('blue_ice', 2)]                    # (black veins are drawn through it afterwards: ice_veins)
ICE_FLOOR = [('packed_ice', 6), ('blue_ice', 2), ('snow_block', 0.5)]
HEX = [('polished_blackstone_bricks', 6), ('deepslate_tiles', 2), ('obsidian', 1), ('cracked_polished_blackstone_bricks', 1)]
BONE = [('bone_block[axis=y]', 4), ('bone_block[axis=x]', 1), ('smooth_quartz', 1), ('calcite', 1)]
HULL = [('prismarine', 3), ('dark_prismarine', 3), ('prismarine_bricks', 2), ('weathered_copper', 1), ('oxidized_copper', 1)]

CHAIN_Y = 'iron_chain[axis=y,waterlogged=false]'
SOUL = 'soul_lantern[hanging=true,waterlogged=false]'
SOUL_F = 'soul_lantern[hanging=false,waterlogged=false]'
CANDLE = 'red_candle[candles=%d,lit=true,waterlogged=false]'


def walk_at(T):
    """the spiral's walk y at unwound angle T (linear between knots)"""
    for (a, ya), (b, yb) in zip(KNOTS, KNOTS[1:]):
        if a <= T <= b:
            return ya + (yb - ya) * (T - a) / (b - a) if b > a else ya
    return None


def polar(x, z, cx=HX, cz=HZ):
    dx, dz = x - cx, z - cz
    return math.hypot(dx, dz), math.degrees(math.atan2(dz, dx)) % 360


class K:
    """the builder's toolkit, bound to one UBuild"""

    def __init__(self, B):
        self.B = B
        self.rnd = random.Random(29801)

    def s(self, x, y, z, st, nbt=None):
        self.B.set(x, y, z, st, nbt)

    def get(self, x, y, z):
        return self.B.b.get((x, y, z))

    def pick(self, pal):
        return self.B.pick(pal)

    def fill(self, x1, y1, z1, x2, y2, z2, pal, soft=False):
        B = self.B
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    if soft and (x, y, z) in B.b: continue
                    B.set(x, y, z, B.pick(pal))

    def air(self, x1, y1, z1, x2, y2, z2):
        self.fill(x1, y1, z1, x2, y2, z2, 'air')

    def room(self, x1, y1, z1, x2, y2, z2, wall=VOID, floor=FLOOR, ceil=None, t=2):
        """an interior air box x1..x2, y1..y2 (y1 = walk level), z1..z2; floor (y1-1, and one more under it), ceiling and walls
        t thick - walls and the under-floor only where nothing is set yet (so a room never closes off what was cut before it)"""
        ceil = ceil or wall
        self.fill(x1 - t, y1 - 2, z1 - t, x2 + t, y2 + t, z2 + t, wall, soft=True)
        self.fill(x1, y1 - 1, z1, x2, y1 - 1, z2, floor)
        self.fill(x1, y2 + 1, z1, x2, y2 + 1, z2, ceil)
        self.air(x1, y1, z1, x2, y2, z2)

    def is_air(self, x, y, z):
        st = self.B.b.get((x, y, z))
        return st is not None and st.endswith(':air')

    def sign(self, x, y, z, facing, lines, color='red', wall=True):
        st = f'dark_oak_wall_sign[facing={facing},waterlogged=false]' if wall else f'dark_oak_sign[rotation={facing},waterlogged=false]'
        self.B.sign(x, y, z, st, lines, color=color, glow=True)

    def hang(self, x, y, z, length, lamp=SOUL):
        """a lamp hanging on a chain of `length` below the solid block above (x, y+length, z)"""
        for k in range(length): self.s(x, y + 1 + k, z, CHAIN_Y)
        self.s(x, y, z, lamp)

    def chain_run(self, x, y1, y2, z):
        for y in range(min(y1, y2), max(y1, y2) + 1): self.s(x, y, z, CHAIN_Y)


# ===================================================================================================== THE HALL OF CHAINS
def stair_facing(phi):
    """the way UP the spiral at angle phi (decreasing Theta): tangent (sin, -cos) -> nearest cardinal"""
    tx, tz = math.sin(math.radians(phi)), -math.cos(math.radians(phi))
    if abs(tx) >= abs(tz): return 'east' if tx > 0 else 'west'
    return 'south' if tz > 0 else 'north'


def hub(k):
    B, s = k.B, k.s
    cells = {}                                         # (x, z) -> [walk y of each turn of the stair through this column]
    ring = []
    for x in range(int(HX - OUT_R) - 1, int(HX + OUT_R) + 2):
        for z in range(int(HZ - OUT_R) - 1, int(HZ + OUT_R) + 2):
            r, phi = polar(x, z)
            if r > OUT_R: continue
            ring.append((x, z, r, phi))
    # ---- the wall mass (inner wall, the stair's rock, outer wall), the shaft, the pool, the floor ring
    for (x, z, r, phi) in ring:
        if r > SHAFT_R:
            for y in range(10, 108): s(x, y, z, k.pick(VOID))
        else:
            for y in range(10, 14): s(x, y, z, k.pick(VOID))
            if r <= 20:
                for y in range(14, 17): s(x, y, z, 'lava')
                s(x, 17, z, 'tinted_glass')
            else:
                for y in range(14, 17): s(x, y, z, k.pick(VOID))
                s(x, 17, z, 'polished_blackstone_bricks' if int(r) % 4 == 0 else k.pick(FLOOR))
            top = 96 + 8 * math.sqrt(max(0.0, 1 - (r / 28.0) ** 2))
            for y in range(18, 108):
                s(x, y, z, 'air' if y <= top else k.pick(VOID))
            for gy in (FROZEN_Y - 1, HEXED_Y - 1, DROWNED_Y - 1):        # the tinted glass floors across the shaft at every ward
                s(x, gy, z, 'tinted_glass')
    # ---- ribbed piers (two are the Throne Gate's statues instead)
    for a in range(15, 360, 30):
        if a in (255, 285): continue
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        for (x, z, r, phi) in ring:
            if not (24.6 < r <= SHAFT_R + 0.3): continue
            dx, dz = x - HX, z - HZ
            if abs(-sa * dx + ca * dz) > 1.5 or (dx * ca + dz * sa) < 0: continue
            for y in range(18, 100):
                if B.b.get((x, y, z), '').endswith(':air') or y in (FROZEN_Y - 1, HEXED_Y - 1, DROWNED_Y - 1):
                    s(x, y, z, 'polished_blackstone_bricks' if y % 9 else 'chiseled_polished_blackstone')
    # ---- the spiral stair inside the wall
    for (x, z, r, phi) in ring:
        if not (IN_R < r <= COR_R): continue
        for kk in range(3):
            T = phi + 360 * kk
            if T0 <= T <= T1:
                cells.setdefault((x, z), []).append((round(walk_at(T)), T))
    for (x, z), lst in cells.items():
        for (w, T) in lst:
            s(x, w - 1, z, k.pick(FLOOR))
            s(x, w - 2, z, k.pick(VOID))
            for y in range(w, w + 5): s(x, y, z, 'air')
            s(x, w + 5, z, k.pick(VOID))
    for (x, z), lst in cells.items():                  # stairs where the next column down is a block lower
        for (w, T) in lst:
            f = stair_facing(T % 360)
            dx, dz = {'east': (1, 0), 'west': (-1, 0), 'south': (0, 1), 'north': (0, -1)}[f]
            low = [w2 for (w2, T2) in cells.get((x - dx, z - dz), []) if abs(T2 - T) < 20]
            if low and low[0] == w - 1:
                s(x, w - 1, z, f'polished_blackstone_brick_stairs[facing={f},half=bottom,shape=straight,waterlogged=false]')
    k.stair_cells = cells
    return ring


def spiral_at(k, T):
    """the corridor column nearest the centre line at unwound angle T, and its walk y"""
    a = math.radians(T % 360)
    return round(HX + 31 * math.cos(a)), round(walk_at(T)), round(HZ + 31 * math.sin(a))


# ----------------------------------------------------------------------------------------------- silhouettes (statues)
SNOWBEAST = ['   #####   ', '   #####   ', '   #####   ', ' ######### ', '   #####   ', '  #######  ', '  #r###r#  ', '  #######  ',
             '   #####   ', ' ######### ', '###########', '###########', '###########', ' ######### ', '  #######  ', ' ######### ',
             '###########', '###########', '###########', ' ######### ']
WITCH = ['     #     ', '    ##     ', '    ###    ', '   ####    ', '   #####   ', '  #######  ', '###########', '   #####   ',
         '   #r#r#   ', '   #####   ', '    ###    ', '  #######  ', ' ######### ', '## ##### ##', '#  #####  #', '  #######  ',
         ' ######### ', ' ######### ', '###########', '###########']
SAWSHARK = ['           ##           ', '          ####          ', '     ###############   #', '=t=t=###############r####',
            '     ################# ##', '       ###   ####      #', '        #     ##        ']


def relief(k, mask, x0, ytop, z, mat=('blackstone', 'polished_blackstone'), thick=2, dz=1):
    """a pixel silhouette standing in the plane z (and `thick` deep toward +dz): '#' stone, 'r' a dim red eye, '=' bone, 't' teeth"""
    for row, line in enumerate(mask):
        for col, ch in enumerate(line):
            if ch == ' ': continue
            st = {'#': None, 'r': 'magma_block', '=': 'bone_block[axis=x]', 't': 'smooth_quartz'}[ch]
            for t in range(thick):
                k.s(x0 + col, ytop - row, z + dz * t, st or (mat[0] if (row + col) % 5 else mat[1]))


def inner_cells(phi, half, r0=SHAFT_R, r1=IN_R + 0.01):
    """wall cells (x, z) with r0 < r <= r1 within `half` (tangentially) of the radial line at angle phi"""
    ca, sa = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    out = []
    for x in range(int(HX + r1 * ca) - 5, int(HX + r1 * ca) + 6):
        for z in range(int(HZ + r1 * sa) - 5, int(HZ + r1 * sa) + 6):
            dx, dz = x - HX, z - HZ
            r = math.hypot(dx, dz)
            if r0 < r <= r1 and abs(-sa * dx + ca * dz) <= half and dx * ca + dz * sa > 0: out.append((x, z))
    return out


def hub_features(k):
    B, s = k.B, k.s
    rnd = k.rnd
    # ---------------- the rim (the tunnel arrives here): a wide gallery and a caged balcony out over the shaft
    for x in range(HX, HX + 40):
        for z in range(HZ, HZ + 40):
            r, phi = polar(x, z)
            if 29.5 < r <= 37.5 and 33 <= phi <= 59:
                k.fill(x, RIM_Y - 2, z, x, RIM_Y - 1, z, FLOOR)
                for y in range(RIM_Y, RIM_Y + 7): s(x, y, z, 'air')
            elif 37.5 < r <= 39.5 and 31 <= phi <= 61:
                k.fill(x, RIM_Y - 2, z, x, RIM_Y + 8, z, VOID, soft=True)
    k.fill(HX, RIM_Y + 7, HZ, HX + 39, RIM_Y + 7, HZ + 39, 'air', soft=True) if False else None
    for x in range(HX, HX + 40):                           # its ceiling (over the widened part)
        for z in range(HZ, HZ + 40):
            r, phi = polar(x, z)
            if 29.5 < r <= 39.5 and 31 <= phi <= 61 and B.b.get((x, RIM_Y + 7, z), '').endswith(':air'):
                s(x, RIM_Y + 7, z, k.pick(VOID))
    bal = {(x, z) for x in range(HX, HX + 32) for z in range(HZ, HZ + 32)
           if 19 < polar(x, z)[0] <= IN_R and abs(-math.sin(math.radians(45)) * (x - HX) + math.cos(math.radians(45)) * (z - HZ)) <= 3.2}
    for (x, z) in bal:
        s(x, RIM_Y - 1, z, 'polished_blackstone_bricks' if (x + z) % 3 else 'gilded_blackstone')
        s(x, RIM_Y - 2, z, k.pick(VOID))
        for y in range(RIM_Y, RIM_Y + 5): s(x, y, z, 'air')
    for (x, z) in bal:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, z + dz)
            if n not in bal and polar(*n)[0] <= SHAFT_R:
                for y in range(RIM_Y, RIM_Y + 3): s(x, y, z, 'iron_bars')
                break
    for (x, z) in list(bal)[::7]:                            # chains up to the dome hold it
        if B.b.get((x, RIM_Y, z), '').endswith('iron_bars'):
            for y in range(RIM_Y + 3, 100):
                if B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, CHAIN_Y)
    lx, _, lz = spiral_at(k, 52)
    k.B.lectern(lx + 3, RIM_Y, lz + 3, 'west', *L.BOOKS['warden'])
    B.voice('hall', lx, RIM_Y, lz, r=6)
    k.sign(lx + 2, RIM_Y, lz + 4, 6, ['THE HALL OF', 'CHAINS', 'Down is the', 'only way.'], wall=False)
    # ---------------- windows onto the shaft (barred low, open above), every 30 degrees of the stair
    skip = [45, 90, 180, 187, 270, 340, 360, 450, 457, 562]
    for T in range(T0 + 15, T1 - 3, 30):
        if any(abs(T - f) < 12 for f in skip): continue
        w = round(walk_at(T))
        for (x, z) in inner_cells(T % 360, 1.6):
            for y in (w, w + 1): s(x, y, z, 'iron_bars')
            for y in (w + 2, w + 3, w + 4): s(x, y, z, 'air')
    # ---------------- the giant chains: links 5 wide, 7 tall, in alternating planes, from the dome into the pool
    for i in range(5):
        a = math.radians(18 + 72 * i)
        cx, cz = round(HX + 15 * math.cos(a)), round(HZ + 15 * math.sin(a))
        yt, j = 104, 0
        while yt - 6 >= 12:
            for dy in range(7):
                for dw in range(-2, 3):
                    edge = dy in (0, 6) or dw in (-2, 2)
                    corner = dy in (0, 6) and dw in (-2, 2)
                    if not edge or corner: continue
                    x, z = (cx + dw, cz) if j % 2 == 0 else (cx, cz + dw)
                    y = yt - dy
                    if y < 14: continue
                    s(x, y, z, 'polished_deepslate' if dw in (-2, 2) else 'deepslate_tiles')
            yt -= 5; j += 1
    # ---------------- long iron chains hanging from the dome, some with a soul lantern
    for _ in range(46):
        a, r = rnd.uniform(0, 360), rnd.uniform(4, 26)
        x, z = round(HX + r * math.cos(math.radians(a))), round(HZ + r * math.sin(math.radians(a)))
        top = max(y for y in range(18, 108) if B.b.get((x, y, z), '').endswith(':air')) if B.b.get((x, 60, z), '').endswith(':air') else None
        if top is None: continue
        ln = rnd.randint(8, 34)
        ok = all(B.b.get((x, y, z), '').endswith(':air') for y in range(top - ln, top + 1))
        if not ok: continue
        for y in range(top - ln + 1, top + 1): s(x, y, z, CHAIN_Y)
        if rnd.random() < 0.35: s(x, top - ln, z, SOUL)
    # dim red on the piers: a magma band every 18 blocks
    for a in range(15, 360, 30):
        if a in (255, 285): continue
        for (x, z) in inner_cells(a, 0.6, 24.6, 25.6):
            for y in (30, 48, 66, 84):
                if 'blackstone' in B.b.get((x, y, z), ''): s(x, y, z, 'magma_block')
    B.fx(HX, 60, HZ); B.fx(HX, 30, HZ); B.fx(HX, 88, HZ)
    B.controller(HX, 46, HZ)


def landings(k):
    B, s = k.B, k.s
    # ---- the Frozen landing (west, walk 78): Pistachio's sigil in front of the hat-lock door (G1)
    k.room(72, FROZEN_Y, 143, 79, FROZEN_Y + 7, 153, wall=VOID)
    k.air(70, FROZEN_Y, 147, 70, FROZEN_Y + 3, 149)
    for z in range(144, 153):
        if z % 2: s(73, FROZEN_Y, z, 'air')
    # ---- the Hexed landing (east, walk 52)
    k.room(143, HEXED_Y, 127, 151, HEXED_Y + 7, 140, wall=VOID)
    k.air(153, HEXED_Y, 133, 153, HEXED_Y + 3, 135)
    # ---- the Drowned landing (south, walk 36)
    k.room(110, DROWNED_Y, 177, 124, DROWNED_Y + 7, 186, wall=VOID)
    k.air(116, DROWNED_Y, 188, 118, DROWNED_Y + 3, 188)


def stair_gates(k):
    """the stair's own gates: G5 below the Frozen landing, G10 below the Hexed one, G15 below the Drowned one"""
    B, s = k.B, k.s
    for (x, y, z, ax, n) in ((81, FROZEN_Y, 141, 'x', 5), (143, HEXED_Y, 145, 'x', 10), (108, DROWNED_Y, 176, 'z', 15)):
        for dw in range(-4, 5):                              # the plane is exactly three wide: wall anything else in the way
            gx, gz = (x + dw, z) if ax == 'x' else (x, z + dw)
            for dy in range(0, 6):
                if abs(dw) > 1 or dy >= 4:
                    s(gx, y + dy, gz, 'chiseled_polished_blackstone' if dy == 4 and abs(dw) <= 1 else 'polished_blackstone_bricks')
            if abs(dw) <= 1: s(gx, y - 1, gz, 'polished_blackstone')
        B.gate(x, y, z, ax, n)


def floor_ring(k):
    B, s = k.B, k.s
    y = FLOOR_Y
    # ---- the Throne Gate (north): six G16 gates make one door 9 wide and 8 tall, framed and flanked by the Dread's three
    k.air(108, y, 117, 116, y + 7, 118)
    k.fill(108, y - 1, 117, 116, y - 1, 118, 'polished_blackstone')
    for x in range(103, 122):                                   # the frame: pilasters, a lintel, a crest of spikes
        for yy in range(y, y + 13):
            for z in (117, 118, 119):
                pil = x <= 107 or x >= 117
                if (pil or yy >= y + 8) and not (108 <= x <= 116 and yy < y + 8):
                    if z == 119 and not (pil or yy >= y + 8): continue
                    s(x, yy, z, 'gilded_blackstone' if (yy == y + 9 and x % 2 == 0) or (z == 119 and pil and yy % 4 == 0)
                      else 'chiseled_polished_blackstone' if yy == y + 12 else 'polished_blackstone_bricks')
        if x % 3 == 0:
            for yy in range(y + 13, y + 13 + (3 if x % 6 == 0 else 1)): s(x, yy, 119, 'polished_blackstone_wall')
    relief(k, SNOWBEAST, 93, y + 19, 125, dz=-1)               # the Snowbeast and the Witch stand either side, the Sawshark over
    relief(k, WITCH, 121, y + 19, 125, dz=-1)
    relief(k, SAWSHARK, 100, y + 18 + 7, 121, thick=3, dz=-1)
    for x in range(93, 104): s(x, y - 1, 124, 'polished_blackstone'); s(x, y - 1, 125, 'polished_blackstone')
    for x in range(121, 132): s(x, y - 1, 124, 'polished_blackstone'); s(x, y - 1, 125, 'polished_blackstone')
    for gx in (109, 112, 115):
        for gy in (y, y + 4):
            B.gate(gx, gy, 116, 'x', 16)
    # ---- the three sockets on their pedestals, the trial's controller over the middle one
    for x, kk in ((106, 'snow'), (112, 'witch'), (118, 'shark')):
        B.socket(16, x, y + 1, 122, kk)
        s(x, y - 1, 122, 'polished_blackstone_bricks')
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            s(x + dx, y - 1, 122 + dz, 'gilded_blackstone')
    B.pz(16, 'shards', 112, y + 3, 122)
    k.sign(112, y, 125, 0, ['THE THRONE GATE', 'Lay the three', 'Crown Shards', 'on their stones.'], wall=False)
    B.voice('shards', 112, y, 124, r=7)
    # braziers of soul fire on the ring
    for a in (0, 60, 120, 180, 240, 300):
        x, z = round(HX + 22.5 * math.cos(math.radians(a + 30))), round(HZ + 22.5 * math.sin(math.radians(a + 30)))
        if B.b.get((x, y, z), '').endswith(':air'):
            s(x, y, z, 'polished_blackstone_bricks'); s(x, y + 1, z, 'soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    # ---- the stair's last arch onto the ring (west-north-west)
    for a in range(199, 208):
        for (x, z) in inner_cells(a, 1.0):
            for yy in range(y, y + 4): s(x, yy, z, 'air')
            s(x, y - 1, z, 'polished_blackstone')
    # ---- grilles round the ring (one of them is the Forge's door)
    for a in (40, 160, 230, 320):
        for (x, z) in inner_cells(a, 1.4, SHAFT_R, IN_R - 1.0):
            for yy in range(y, y + 3): s(x, yy, z, 'iron_bars')
    B.zone(HX, y + 1, HZ + 22); B.zone(HX, y + 1, HZ - 22)


def secret_chain(k):
    """SECRET 1: a button low on the stair's outer wall, behind a hanging chain (south, walk 88); a room behind the wall"""
    B, s = k.B, k.s
    w = 88
    for x in (108, 112, 116):
        for y in range(w + 1, w + 5): s(x, y, 177, CHAIN_Y)
    B.sbutton(112, w, 177, 'polished_blackstone_button[face=wall,facing=north,powered=false]', 1)
    k.room(110, w, 181, 118, w + 3, 186, wall=VOID)
    k.air(114, w, 179, 114, w + 1, 180)
    B.sdoor(114, w, 178, 1)
    B.chest(117, w, 183, 'west', loot='bm:p2/under/hidden')
    s(111, w, 184, 'polished_blackstone_bricks'); s(111, w + 1, 184, 'wither_skeleton_skull[powered=false,rotation=12]')
    s(114, w + 3, 184, 'soul_lantern[hanging=true,waterlogged=false]')


# ===================================================================================================== THE APPROACH, THE GATE
CAVE = [('blackstone', 4), ('basalt[axis=y]', 3), ('netherrack', 3), ('magma_block', 0.25), ('polished_basalt[axis=y]', 1)]
SEAM = (191, 99, 207)


def approach(k):
    """the ash cave before the Hidden Gate: every cell of it (air and rough walls) is B.outside - the seal leaves it be"""
    B, s, rnd = k.B, k.s, k.rnd
    out = B.outside
    sx_, sy_, sz_ = B.size
    air = set()
    for x in range(192, 224):
        for y in range(99, 110):
            for z in range(188, 224):
                v = ((x - 206) / 16) ** 2 + ((y - 99) / 9) ** 2 + ((z - 207) / 14) ** 2
                if v <= 1 - rnd.random() * 0.18: air.add((x, y, z))
    for x in range(192, 198):                              # the apron in front of the cliff
        for z in range(194, 221):
            for y in range(99, 105 + (z * 7 + x) % 3): air.add((x, y, z))
    for x in range(212, 224):                              # a rough tunnel east, to the template's edge
        for y in range(99, 106):
            for z in range(202, 213):
                if ((y - 102) / 3.6) ** 2 + ((z - 207) / 4.2) ** 2 <= 1 - rnd.random() * 0.2: air.add((x, y, z))
    for z in range(214, 224):                              # and one south
        for y in range(99, 106):
            for x in range(200, 213):
                if ((y - 102) / 3.6) ** 2 + ((x - 206) / 4.4) ** 2 <= 1 - rnd.random() * 0.2: air.add((x, y, z))
    shell = set()
    for (x, y, z) in air:
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                for dz in (-2, -1, 0, 1, 2):
                    q = (x + dx, y + dy, z + dz)
                    if q not in air and 0 <= q[0] < sx_ and 0 <= q[1] < sy_ and 0 <= q[2] < sz_ and q[0] >= 191: shell.add(q)
    for q in shell:
        s(*q, k.pick(CAVE)); out.add(q)
    for q in air:
        s(*q, 'air'); out.add(q)
    # floor: rough, with ash-grey basalt and a few magma cracks
    for (x, y, z) in air:
        if (x, y - 1, z) in shell:
            s(x, y - 1, z, 'magma_block' if rnd.random() < 0.03 else 'smooth_basalt' if rnd.random() < 0.3 else k.pick(CAVE[:3]))
    # the sheer cliff (x 191): basalt columns, with the seam and three token hollows
    for z in range(190, 224):
        for y in range(95, 111):
            q = (191, y, z)
            s(*q, 'polished_basalt[axis=y]' if (z + y // 4) % 3 else 'basalt[axis=y]'); out.add(q)
    hol = {'snow': 197, 'shark': 202, 'witch': 212}
    for kk, z in hol.items():
        s(191, 100, z, CANDLE % 1); out.add((191, 100, z))
        s(191, 101, z, 'polished_blackstone'); s(191, 99, z, 'chiseled_polished_blackstone')
    for (x, y, z) in list(air):                            # a few basalt stalagmites and hanging ash
        if rnd.random() < 0.004 and (x, y - 1, z) in shell and x > 199:
            for dy in range(rnd.randint(2, 5)):
                if (x, y + dy, z) in air: s(x, y + dy, z, 'basalt[axis=y]')
    sx, sy, sz = SEAM
    B.hidden_gate(sx, sy, sz, 'z', 1, 5, {kk: (192, 99, z) for kk, z in hol.items()}, (197, 99, sz))
    for z in range(sz - 2, sz + 3):                        # a crack that runs up the cliff over the seam
        s(191, sy + 5 + abs(z - sz), z, 'crying_obsidian' if z == sz else 'obsidian')
    s(191, sy + 9, sz, 'obsidian')


def tube(k, path, w=5, h=7, wall=VOID, rib=4, ribmat='polished_blackstone'):
    """an axis-aligned tunnel along `path` [(x, z, walk)...] (consecutive points share x or z); w wide, h tall, walls 2 thick,
    ribs (arches) every `rib` blocks; one step of walk per cell at most (a stair where it drops)"""
    B, s = k.B, k.s
    hw = w // 2
    cells = []
    for (x1, z1, y1), (x2, z2, y2) in zip(path, path[1:]):
        n = max(abs(x2 - x1), abs(z2 - z1))
        dx, dz = (x2 > x1) - (x2 < x1), (z2 > z1) - (z2 < z1)
        for i in range(n + 1):
            yy = round(y1 + (y2 - y1) * i / n)
            cells.append((x1 + dx * i, z1 + dz * i, yy, dx, dz))
    for (x, z, y, dx, dz) in cells:
        px, pz = (0, 1) if dx else (1, 0)
        for o in range(-hw - 2, hw + 3):
            cx, cz = x + px * o, z + pz * o
            for yy in range(y - 2, y + h + 2):
                if (cx, yy, cz) not in B.b: s(cx, yy, cz, k.pick(wall))
    for i, (x, z, y, dx, dz) in enumerate(cells):
        px, pz = (0, 1) if dx else (1, 0)
        for o in range(-hw, hw + 1):
            cx, cz = x + px * o, z + pz * o
            s(cx, y - 1, cz, k.pick(FLOOR))
            for yy in range(y, y + h): s(cx, yy, cz, 'air')
            s(cx, y + h, cz, k.pick(wall))
    # stairs where the walk drops (facing the way up)
    for i in range(1, len(cells)):
        (x0, z0, y0, _, _), (x, z, y, dx, dz) = cells[i - 1], cells[i]
        if abs(y - y0) == 1:
            hi = cells[i - 1] if y0 > y else cells[i]
            lo = cells[i] if y0 > y else cells[i - 1]
            fx, fz = hi[0] - lo[0], hi[1] - lo[1]
            f = {(1, 0): 'east', (-1, 0): 'west', (0, 1): 'south', (0, -1): 'north'}[(fx, fz)]
            px, pz = (0, 1) if fx else (1, 0)
            for o in range(-hw, hw + 1):
                s(hi[0] + px * o, hi[2] - 1, hi[1] + pz * o, f'polished_blackstone_brick_stairs[facing={f},half=bottom,shape=straight,waterlogged=false]')
    # ribs: arches that pinch the top corners, every `rib` cells
    for i, (x, z, y, dx, dz) in enumerate(cells):
        if i % rib or i == 0: continue
        px, pz = (0, 1) if dx else (1, 0)
        for o in (-hw, hw):
            for yy in range(y + h - 2, y + h):
                s(x + px * o, yy, z + pz * o, ribmat)
        s(x, y + h, z, 'chiseled_polished_blackstone')
    return cells


def tunnel(k):
    """from the seam, a long descending tunnel west then north-west to the Hall's rim"""
    B, s, rnd = k.B, k.s, k.rnd
    sx, sy, sz = SEAM
    k.air(sx - 2, sy, sz - 1, sx - 1, sy + 4, sz + 1)
    k.fill(sx - 2, sy - 1, sz - 1, sx - 1, sy - 1, sz + 1, 'polished_blackstone')
    a = tube(k, [(sx - 3, sz, 99), (176, sz, 99), (164, sz, 95), (152, sz, 95)])
    b = tube(k, [(152, sz, 95), (152, 196, 95), (152, 178, 92), (152, 166, 92)])
    c = tube(k, [(152, 166, 92), (140, 166, 92)])
    # the far ends glow red: a lavafall of glass behind the wall where each leg turns
    for z in range(sz - 1, sz + 2):
        for y in range(97, 104):
            s(148, y, z, 'red_stained_glass'); s(147, y, z, 'shroomlight' if y % 3 == 0 else 'magma_block')
    for x in range(151, 154):
        for y in range(94, 100):
            s(x, y, 162, 'red_stained_glass'); s(x, y, 161, 'shroomlight' if y % 3 == 0 else 'magma_block')
    # chains hang between the ribs; dim red candles in the ribs' feet
    for i, (x, z, y, dx, dz) in enumerate(a + b + c):
        px, pz = (0, 1) if dx else (1, 0)
        if i % 4 == 2:
            for o in (-1, 1):
                ln = 2 + (i * 7 + o) % 3
                for yy in range(y + 7 - ln, y + 7): s(x + px * o, yy, z + pz * o, CHAIN_Y)
        if i % 12 == 6:
            o = 2 if i % 24 == 6 else -2
            s(x + px * o, y, z + pz * o, CANDLE % 3)
    B.entrance(sx - 3, sy, sz)
    B.voice('gate', sx - 5, sy, sz, r=6)
    k.sign(sx - 4, sy + 2, sz - 2, 'south', ['', 'You broke', 'my three.', ''])


# ===================================================================================================== THE FROZEN WARD
def lavafall(k, x, z, y0, y1, ax, back, w=3):
    """a frozen 'lavafall' on a wall face: a glass core (orange/red, magma glowing dimly behind it) sheathed in ice, w wide
    (the core is w-2 wide). ax: the wall plane's axis ('x' - the fall spans x; 'z' - spans z); back = (dx, dz) into the wall"""
    s = k.s
    h = w // 2
    for y in range(y0, y1 + 1):
        for o in range(-h, h + 1):
            cx, cz = (x + o, z) if ax == 'x' else (x, z + o)
            if abs(o) < h:
                s(cx, y, cz, 'orange_stained_glass' if (y * 3 + x + z + o * 5) % 4 else 'red_stained_glass')
                s(cx + back[0], y, cz + back[1], 'shroomlight' if (y + o) % 7 == 0 and abs(o) == 0 else 'magma_block')
            else:
                s(cx, y, cz, 'blue_ice' if (y + o) % 3 == 0 else 'packed_ice')


def frame_deco(k, kind, x, y, z, ax, front):
    """the decoration round a Frozen Falls target at (x, y, z) in a wall plane; front = (dx, dz) out of the wall"""
    s = k.s
    def at(u, v):                                   # u along the wall, v up
        return (x + u, y + v, z) if ax == 'x' else (x, y + v, z + u)
    ring = [(u, v) for u in (-1, 0, 1) for v in (-1, 0, 1) if (u, v) != (0, 0)]
    if kind == 'hat':
        for (u, v) in ring: s(*at(u, v), 'black_concrete')
        for u in range(-2, 3): s(*at(u, 2), 'black_wool')
        for u in (-1, 0, 1):
            for v in (3, 4, 5): s(*at(u, v), 'black_wool')
        for u in (-1, 0, 1): s(*at(u, 3), 'red_wool')
    elif kind == 'flake':
        for (u, v) in ring: s(*at(u, v), 'white_concrete' if u == 0 or v == 0 else 'packed_ice')
        for d in (2, 3):
            for (u, v) in ((d, 0), (-d, 0), (0, d), (0, -d)): s(*at(u, v), 'white_concrete')
        for (u, v) in ((2, 2), (-2, 2), (2, -2), (-2, -2)): s(*at(u, v), 'white_concrete')
    elif kind == 'icicle':
        for (u, v) in ring: s(*at(u, v), 'packed_ice')
        for v in range(2, 6): s(*at(0, v), 'blue_ice')
        for (u, v) in ((-1, 2), (1, 2), (-1, 3), (1, 3)): s(*at(u, v), 'blue_ice')
        fx, fz = front
        for v, ln in ((-2, 1), (-3, 1)):
            s(at(0, v)[0], at(0, v)[1], at(0, v)[2], 'blue_ice')
    elif kind == 'claw':
        for (u, v) in ring: s(*at(u, v), 'bone_block[axis=y]')
        for u in (-2, 0, 2):
            for v in (2, 3, 4): s(*at(u + (v - 2) * (1 if u > 0 else -1 if u < 0 else 0), v), 'bone_block[axis=y]')
    elif kind == 'empty':
        for (u, v) in ring: s(*at(u, v), 'polished_blackstone')


def ice_veins(k, box, n=160):
    """black ice-veins: crooked lines of blackstone wandering over the Frozen Ward's ice faces (not random specks)"""
    B, rnd = k.B, random.Random(4411)
    (x0, y0, z0), (x1, y1, z1) = box
    ice = lambda q: B.b.get(q, '').split(':')[-1].split('[')[0] in ('packed_ice', 'blue_ice')
    def face(q):
        return ice(q) and any(B.b.get((q[0] + a, q[1] + b, q[2] + c), '').endswith(':air') for a, b, c in
                              ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
    seeds = [q for q in B.b if x0 <= q[0] <= x1 and y0 <= q[1] <= y1 and z0 <= q[2] <= z1 and face(q)]
    seeds.sort()
    for _ in range(n):
        q = seeds[rnd.randrange(len(seeds))]
        d = rnd.choice(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
        for _ in range(rnd.randint(5, 14)):
            if not face(q): break
            B.set(*q, 'blackstone')
            if rnd.random() < 0.35: d = rnd.choice(((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)))
            q = (q[0] + d[0], q[1] + d[1], q[2] + d[2])


def frozen_cavern(k, x1, z1, x2, z2, W):
    """the Frozen Falls' drama: icicle clusters hanging from the vault, ice teeth rising from the floor, snow drifted against
    the walls (nothing within reach of the doors, and no icicle lower than ten blocks over the floor)"""
    B, s, rnd = k.B, k.s, random.Random(5150)
    air = lambda q: B.b.get(q, '').endswith(':air')
    keep_clear = lambda x, z: (36 <= x <= 40 and z <= 131) or (x >= 52 and 143 <= z <= 153) or (37 <= x <= 45 and 146 <= z <= 153)
    for _ in range(46):                                         # icicles: a long blue spike, shorter ones round it
        cx, cz = rnd.randint(x1 + 1, x2 - 1), rnd.randint(z1 + 1, z2 - 1)
        for (dx, dz, f) in ((0, 0, 1.0), (1, 0, 0.55), (-1, 0, 0.45), (0, 1, 0.6), (0, -1, 0.4), (1, 1, 0.3)):
            x, z = cx + dx, cz + dz
            y = W + 1
            while y < W + 30 and air((x, y, z)): y += 1
            if y >= W + 30 or not air((x, y - 1, z)): continue
            ln = max(1, int(rnd.randint(3, 9) * f))
            bottom = max(W + 10, y - ln)
            for yy in range(bottom, y): s(x, yy, z, 'blue_ice' if yy < bottom + 2 or (dx, dz) == (0, 0) else 'packed_ice')
    for x in range(x1, x2 + 1):                                 # drifts: snow banked against every wall, deeper in the corners
        for z in range(z1, z2 + 1):
            if keep_clear(x, z) or not air((x, W, z)): continue
            walls = sum(not air((x + a, W, z + b)) and B.b.get((x + a, W, z + b), '').split(':')[-1].split('[')[0] in
                        ('packed_ice', 'blue_ice', 'blackstone') for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if walls and rnd.random() < 0.75:
                s(x, W, z, 'snow_block')
                if walls >= 2 and air((x, W + 1, z)): s(x, W + 1, z, 'snow_block')
            elif not walls and rnd.random() < 0.011 and air((x, W + 1, z)):
                for yy in range(W, W + rnd.randint(2, 4)): s(x, yy, z, 'blue_ice' if yy == W else 'packed_ice')


def frozen(k):
    B, s, rnd = k.B, k.s, k.rnd
    W = FROZEN_Y
    # ---------------- G1: the hat-lock door (a top hat of packed ice round the gate), Pistachio's sigil before it
    for z in range(145, 152):
        for y in range(W, W + 10):
            pass
    for z in (146, 150):
        for y in range(W, W + 4): s(71, y, z, 'packed_ice'); s(72, y, z, 'packed_ice')
    for z in range(144, 153): s(71, W + 4, z, 'packed_ice'); s(72, W + 4, z, 'packed_ice')
    for z in range(146, 151):
        for y in range(W + 5, W + 9): s(71, y, z, 'black_wool' if y == W + 5 else 'packed_ice')
    k.sign(72, W + 2, 145, 'east', ['A HAT MAY', 'ENTER.', 'ITS HEAD MAY', 'FOLLOW.'], color='aqua')
    B.sigil(1, 75, W, 148, 'pistachio')
    B.pz(1, 'sigil', 75, W + 3, 150)
    k.hang(76, W + 5, 151, 2)
    # ---------------- the vestibule
    k.room(58, W, 143, 69, W + 8, 153, wall=ICE, floor=ICE_FLOOR)
    B.voice('frozen', 66, W, 148, r=6)
    k.hang(63, W + 6, 148, 2)
    for z in (144, 152):
        for y in range(W, W + 8): s(60, y, z, 'blackstone' if y % 3 else 'packed_ice')
    # ---------------- P2 THE FROZEN FALLS (targets, in the verse's order)
    k.room(28, W, 128, 55, W + 21, 168, wall=ICE, floor=ICE_FLOOR)
    for x in range(28, 56):                                 # a vaulted ceiling: the corners stay rock
        for z in range(128, 169):
            dd = max(abs(x - 41.5) / 14, abs(z - 148) / 20.5)
            top = W + 21 - int(max(0, dd - 0.55) * 22)
            for y in range(top + 1, W + 22): s(x, y, z, k.pick(ICE))
    k.air(56, W, 145, 57, W + 4, 151)
    for z in range(145, 152): s(56, W - 1, z, 'packed_ice'); s(57, W - 1, z, 'packed_ice')
    FALLS = [('claw', 4, 27, 136, 'z', (-1, 0)), ('hat', 1, 27, 160, 'z', (-1, 0)), ('empty', 5, 36, 169, 'x', (0, 1)),
             ('flake', 2, 48, 169, 'x', (0, 1)), ('icicle', 3, 50, 127, 'x', (0, -1))]
    for kind, order, x, z, ax, back in FALLS:
        lavafall(k, x, z, W, W + 17, ax, back, w=7)
        frame_deco(k, kind, x, W + 6, z, ax, (-back[0], -back[1]))
        B.target(2, x, W + 6, z, order=order)
        ox, oz = back
        for u in range(-3, 4):                               # where it froze as it hit the floor: a pool of blue ice, a frozen splash
            for v in (1, 2, 3):
                if abs(u) == 3 and v == 3: continue
                cx, cz = (x + u - ox * v, z - oz * v) if ax == 'x' else (x - ox * v, z + u - oz * v)
                s(cx, W - 1, cz, 'blue_ice' if (u + v) % 3 else 'orange_stained_glass')
                if v == 1 and abs(u) >= 2: s(cx, W, cz, 'packed_ice')
    lavafall(k, 27, 147, W, W + 14, 'z', (-1, 0), w=5)        # the silent falls, with nothing in them
    lavafall(k, 42, 169, W, W + 14, 'x', (0, 1), w=5)
    frozen_cavern(k, 28, 128, 55, 168, W)
    B.lectern(41, W, 150, 'south', *L.BOOKS['frozen'])
    s(41, W - 1, 150, 'chiseled_polished_blackstone')
    k.sign(43, W, 151, 0, ['THE FROZEN', 'FALLS', 'Read the verse.', 'Strike in order.'], color='aqua', wall=False)
    s(39, W, 151, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'Items': [
        {'Slot': Byte(i), 'id': 'minecraft:arrow', 'count': Int(32)} for i in range(4)]})
    B.pz(2, 'targets', 41, W + 4, 148)
    for (x, z) in ((34, 140), (49, 140), (34, 158), (49, 158)):
        for y in range(W, W + 21):
            if B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, 'packed_ice' if y % 5 else 'blackstone')
    for (x, z) in ((41, 138), (41, 160), (35, 149), (48, 149)):
        k.hang(x, W + 9, z, 6)
    B.fx(41, W + 8, 148)
    # ---------------- G2 -> P3 THE ICE BRIDGE (Celi + Tullius, a lava lake)
    k.room(24, W, 96, 60, W + 16, 125, wall=ICE, floor=ICE_FLOOR)
    k.air(37, W, 126, 39, W + 3, 126)
    for x in range(24, 61):
        for z in range(101, 118):
            s(x, W - 1, z, 'air'); s(x, W - 2, z, 'lava'); s(x, W - 3, z, 'lava'); s(x, W - 4, z, k.pick(VOID)); s(x, W - 5, z, k.pick(VOID))
    for z in range(99, 120):
        for x in (22, 23, 61, 62):
            for y in range(W - 6, W - 1): s(x, y, z, k.pick(VOID))
    for x in range(22, 63):
        for z in (100, 118):
            for y in range(W - 6, W - 1):
                if not (B.b.get((x, y, z), '').endswith('lava')): s(x, y, z, k.pick(VOID))
    for x in range(24, 61):                                 # the shores' edges: ice teeth
        if x % 3 == 0: s(x, W, 118, 'packed_ice'); s(x, W, 100, 'packed_ice')
    for x in (40, 44):
        s(x, W, 118, 'polished_blackstone_brick_wall'); s(x, W, 100, 'polished_blackstone_brick_wall')
    for x in range(40, 45):
        if x in (41, 42, 43): s(x, W, 118, 'air'); s(x, W, 100, 'air')
    B.bridge(3, 41, W - 1, 101, 43, W - 1, 117, 'packed_ice')
    B.sigil(3, 32, W, 121, 'celi')
    B.sigil(3, 52, W, 121, 'tul')
    B.pz(3, 'sigil', 42, W + 3, 122)
    k.sign(42, W, 123, 0, ['THE SNOW FALLS.', 'THE ICE HOLDS.', 'BOTH,', 'OR NEITHER.'], color='aqua', wall=False)
    for x, z in ((26, 98), (58, 98), (26, 123), (58, 123)):
        lavafall(k, x, 95 if z == 98 else 126, W, W + 16, 'x', (0, -1) if z == 98 else (0, 1))
    for (x, z) in ((32, 124), (52, 124)):
        k.hang(x, W + 7, z, 9)
    B.fx(42, W + 8, 109)
    # ---------------- G3 (far shore) -> P4 THE FROSTBOUND THRALLS (waves)
    k.room(26, W, 62, 58, W + 10, 93, wall=ICE, floor=ICE_FLOOR)
    k.air(41, W, 94, 43, W + 3, 94)
    for (x, z) in ((32, 70), (52, 70), (32, 85), (52, 85), (42, 77)):
        if (x, z) == (42, 77): continue
        for y in range(W, W + 11): s(x, y, z, 'packed_ice' if (y - W) % 4 else 'blackstone')
        s(x + 1, W, z, 'blue_ice'); s(x - 1, W, z, 'blue_ice')
    B.pz(4, 'waves', 42, W, 78)
    for (x, z) in ((29, 65), (55, 65), (29, 90), (55, 90), (42, 66), (42, 89)):
        B.el(4, 'wsp', x, W, z)
    for (x, z) in ((36, 77), (48, 77)):
        k.hang(x, W + 6, z, 4)
    k.sign(42, W, 92, 8, ['THE FROSTBOUND', 'THRALLS', 'They were', 'afraid too.'], color='aqua', wall=False)
    B.fx(42, W + 5, 77)
    # ---------------- G4 -> P5 THE ECHO OF THE SNOWBEAST (a round frozen arena)
    cx, cz = 42, 44
    for x in range(cx - 19, cx + 20):
        for z in range(cz - 19, cz + 20):
            r = math.hypot(x - cx, z - cz)
            if r > 18.5: continue
            top = W + 6 + int(12 * math.sqrt(max(0.0, 1 - (r / 16.0) ** 2)))
            if r <= 15.2:
                s(x, W - 1, z, 'packed_ice' if int(r) % 5 else 'blue_ice'); s(x, W - 2, z, k.pick(VOID))
                for y in range(W, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 3): s(x, y, z, k.pick(ICE))
            else:
                for y in range(W - 2, W + 22):
                    if (x, y, z) not in B.b: s(x, y, z, k.pick(ICE))
    for a in range(0, 360, 60):
        px, pz = round(cx + 12 * math.cos(math.radians(a + 30))), round(cz + 12 * math.sin(math.radians(a + 30)))
        for y in range(W, W + 25):
            if B.b.get((px, y, pz), '').endswith(':air'): s(px, y, pz, 'packed_ice' if y % 6 else 'blackstone')
    for a in range(15, 360, 45):
        fx, fz = round(cx + 16 * math.cos(math.radians(a))), round(cz + 16 * math.sin(math.radians(a)))
        if abs(fx - 58) <= 2 and abs(fz - 44) <= 3: continue
        for y in range(W, W + 8):
            if (fx, y, fz) in B.b and not B.b[(fx, y, fz)].endswith(':air'): s(fx, y, fz, 'orange_stained_glass' if y % 3 else 'blue_ice')
    k.air(41, W, 59, 43, W + 3, 60)
    B.echo(5, cx, W, cz, 'snow', r=14)
    B.vault(42, W, 30, 'south', 'ukey', 'bm:p2/under/ward')
    s(41, W, 30, 'packed_ice'); s(43, W, 30, 'packed_ice')
    k.hang(cx, W + 10, cz + 8, 6); k.hang(cx, W + 10, cz - 8, 6)
    B.fx(cx, W + 8, cz)
    # ---------------- G5 out of the arena, and the long frozen gallery back to the vestibule
    corr = tube(k, [(59, 44, W), (64, 44, W), (64, 140, W)], w=3, h=5, wall=ICE, ribmat='packed_ice')
    k.air(63, W, 141, 65, W + 3, 142)
    for i, (x, z, y, dx, dz) in enumerate(corr):
        if dz and i % 9 == 4:
            s(x - 1, y, z, CANDLE % 1) if (x - 1, y, z) and i % 18 == 4 else None
        if dz and i % 16 == 8:
            for yy in range(y, y + 5): s(x + 2, yy, z, 'orange_stained_glass' if yy % 2 else 'packed_ice')
    # ---------------- NINE LIVES (Henry + Nia): a cat-flap in a timbered panel of the gallery's east wall
    for z in list(range(96, 105)) + list(range(70, 76)) + list(range(120, 126)):
        for y in range(W, W + 4): s(66, y, z, 'stripped_dark_oak_wood')
    k.room(68, W, 97, 73, W + 1, 103, wall=VOID, floor=[('spruce_planks', 1)], ceil=[('stripped_dark_oak_wood', 1)])
    s(67, W, 100, 'air'); s(67, W + 1, 100, 'air')
    B.hidden('nine', 66, W, 100, 'z', 0, 2, 'stripped_dark_oak_wood', [('henry', 64, W, 97), ('nia', 64, W, 103)])
    k.sign(65, W + 2, 101, 'west', ['TWO CATS', 'KNOW A', 'LITTLE DOOR.', ''], color='gold')
    for x in range(68, 74):
        for z in range(97, 104):
            if (x + z) % 2 == 0: s(x, W, z, 'red_carpet')
    s(73, W - 1, 100, 'gold_block'); s(73, W, 100, 'air'); B.relic('nine', 73, W, 100)
    B.chest(70, W, 103, 'north', loot='bm:p2/under/hidden')
    s(68, W, 97, 'white_carpet'); s(69, W, 97, 'white_carpet')
    s(72, W + 1, 97, 'soul_lantern[hanging=true,waterlogged=false]')
    # ---------------- the gates (last, over whatever was cut)
    B.gate(71, W, 148, 'z', 1)
    B.gate(38, W, 127, 'x', 2)
    B.gate(42, W, 95, 'x', 3)
    B.gate(42, W, 61, 'x', 4)
    B.gate(58, W, 44, 'z', 5)
    ice_veins(k, ((8, W - 2, 20), (70, W + 26, 170)))


# ===================================================================================================== THE HEXED WARD
SCALES = [('deepslate_tiles', 3), ('oxidized_cut_copper', 1), ('polished_blackstone', 2), ('weathered_cut_copper', 1)]
CRAWL = [(188, 94), (188, 87), (196, 87), (196, 92), (204, 92), (204, 86), (212, 86), (212, 98), (209, 98), (209, 110), (213, 110),
         (213, 122), (209, 122), (209, 134), (213, 134), (213, 146), (210, 146), (210, 157)]


def crawl(k, pts, y):
    """the serpent crawl: 2 wide, 3 tall, tiled like scales (diamonds of copper on black), walls 2 thick"""
    B, s = k.B, k.s
    cells = set()
    for (x1, z1), (x2, z2) in zip(pts, pts[1:]):
        for x in range(min(x1, x2), max(x1, x2) + 2):
            for z in range(min(z1, z2), max(z1, z2) + 2):
                cells.add((x, z))
    scale = lambda x, yy, z: 'oxidized_cut_copper' if (x + z + 2 * yy) % 4 == 0 else 'deepslate_tiles' if (x - z) % 2 else 'polished_blackstone'
    for (x, z) in cells:
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for yy in range(y - 2, y + 5):
                    q = (x + dx, yy, z + dz)
                    if q not in B.b: s(*q, scale(*q))
    for (x, z) in cells:
        s(x, y - 1, z, scale(x, y - 1, z))
        for yy in range(y, y + 3): s(x, yy, z, 'air')
        s(x, y + 3, z, scale(x, y + 3, z))
    for i, (x, z) in enumerate(sorted(cells)):
        if i % 23 == 5:
            for dx, dz, f in ((1, 0, 'west'), (-1, 0, 'east'), (0, 1, 'north'), (0, -1, 'south')):
                if (x + dx, z + dz) not in cells:
                    s(x, y + 2, z, f'glow_lichen[{",".join(f"{d}={str(d == {"west": "east", "east": "west", "north": "south", "south": "north"}[f]).lower()}" for d in ("down", "east", "north", "south", "up", "west"))},waterlogged=false]')
                    break
    return cells


def hexed(k):
    B, s, rnd = k.B, k.s, k.rnd
    W = HEXED_Y
    # ---------------- the entry hall: Cecil's sigil before the library doors (G6); the painted-over wall (the Erased Archive)
    k.room(154, W, 126, 169, W + 9, 142, wall=HEX, floor=[('dark_oak_planks', 3), ('polished_blackstone', 1)])
    B.voice('hexed', 156, W, 134, r=6)
    for z in range(127, 142):
        if z % 4 == 1: s(155, W, z, 'purple_candle[candles=3,lit=true,waterlogged=false]')
    for x in range(156, 169): s(x, W, 134, 'purple_carpet')
    for (x, z) in ((158, 128), (158, 140), (166, 128), (166, 140)):
        for y in range(W, W + 10): s(x, y, z, 'polished_blackstone_bricks' if y % 4 else 'chiseled_polished_blackstone')
    for y in range(W, W + 5):
        s(170, y, 132, 'dark_oak_log[axis=y]'); s(170, y, 136, 'dark_oak_log[axis=y]')
    for z in range(132, 137): s(170, W + 4, z, 'dark_oak_log[axis=z]')
    s(171, W, 133, 'air')
    k.air(171, W, 133, 171, W + 3, 135)
    B.sigil(6, 164, W, 134, 'cecil')
    B.pz(6, 'sigil', 164, W + 3, 131)
    k.sign(169, W + 2, 131, 'west', ['HER OLD', 'FRIEND', 'MAY KNOCK.', ''], color='light_purple')
    k.hang(162, W + 7, 134, 2)
    # the painted-over patch: a door of white concrete in a whitewashed wall
    for x in range(157, 166):
        for y in range(W, W + 6): s(x, y, 125, 'white_concrete')
    k.room(154, W, 112, 168, W + 6, 123, wall=HEX, floor=[('dark_oak_planks', 1)])
    k.air(160, W, 124, 162, W + 2, 124)
    B.hidden('archive', 161, W, 125, 'x', 1, 3, 'white_concrete', [('eraser', 161, W, 129)])
    k.sign(157, W + 1, 126, 'south', ['SOMEONE', 'PAINTED OVER', 'THIS WALL.', 'RUB IT OUT.'], color='gray')
    # the Erased Archive: dusty shelves, every name rubbed white, the Unwritten History
    for x in range(155, 168):
        for y in range(W, W + 5):
            s(x, y, 112, 'bookshelf' if (x + y) % 3 else 'white_concrete')
    for z in range(113, 123):
        for y in range(W, W + 5):
            s(154, y, z, 'bookshelf' if (z + y) % 3 else 'white_concrete'); s(168, y, z, 'bookshelf' if (z + y) % 4 else 'white_wool')
    for x in range(156, 167):
        for z in range(114, 122):
            if (x * 3 + z) % 5 == 0: s(x, W, z, 'white_carpet')
    B.lectern(161, W, 116, 'south', *L.BOOKS['unwritten'])
    s(158, W - 1, 119, 'gold_block'); B.relic('archive', 158, W, 119)
    B.chest(165, W, 119, 'west', loot='bm:p2/under/hidden')
    s(161, W + 5, 119, SOUL); s(161, W + 6, 119, CHAIN_Y)
    # ---------------- G6 -> P7 THE INVERTED LIBRARY (lights-out: the hex sigils)
    k.room(172, W, 110, 204, W + 19, 154, wall=HEX, floor=[('dark_oak_planks', 3), ('stripped_dark_oak_wood', 1)],
           ceil=[('purple_wool', 2), ('black_wool', 1), ('purpur_block', 1)])
    stacks = []
    for x in range(176, 202, 6):
        for z in range(114, 152, 6):
            if 196 <= x and 124 <= z <= 138: continue          # (the board's wall stays clear)
            if x >= 196 and z <= 116: continue                  # (the closet)
            stacks.append((x, z))
    for (x, z) in stacks:
        low = W + 3 if (x, z) == (188, 120) else W + 8 + (x * 7 + z * 3) % 6
        for y in range(low, W + 20):
            for dx in (0, 1):
                for dz in (0, 1):
                    s(x + dx, y, z + dz, 'bookshelf' if y > low else 'purpur_block')
        for dx, dz in ((-1, 0), (2, 0), (0, -1), (0, 2), (-1, 1), (2, 1), (1, -1), (1, 2)):
            if B.b.get((x + dx, low, z + dz), '').endswith(':air') and (x * dx + z) % 3 == 0:
                s(x + dx, W + 18, z + dz, 'amethyst_cluster[facing=down,waterlogged=false]')
    for x in range(174, 203, 4):                                  # chandeliers standing up off the floor (upside down)
        for z in (118, 146):
            if B.b.get((x, W, z), '').endswith(':air') and B.b.get((x, W + 3, z), '').endswith(':air'):
                s(x, W, z, CHAIN_Y); s(x, W + 1, z, CHAIN_Y); s(x, W + 2, z, 'purple_candle[candles=4,lit=true,waterlogged=false]')
    for x in range(174, 203):
        s(x, W - 1, 132, 'purple_wool')
    for x in range(176, 202, 8):
        for z in range(112, 154, 10):
            s(x, W + 19, z, 'crying_obsidian')
    # the board: 4x4 copper bulbs in the east wall, the 4x4 buttons on a plinth before it (same layout, row 0 at the top)
    for z in range(126, 138):
        for y in range(W + 4, W + 16):
            s(205, y, z, 'amethyst_block' if z in (126, 137) or y in (W + 4, W + 15) else 'purpur_block')
    for z in range(127, 136):
        for y in range(W, W + 5): s(201, y, z, 'polished_blackstone_bricks')
        s(201, W + 5, z, 'purpur_slab[type=bottom,waterlogged=false]')
    for i in range(16):
        r, c = divmod(i, 4)
        B.bulb(7, 205, W + 13 - 2 * r, 128 + 2 * c, i)
        B.lo_button(7, 200, W + 3 - r, 129 + c, 'polished_blackstone_button[face=wall,facing=west,powered=false]', i)
    k.sign(200, W + 4, 131, 'west', ['Light every', 'sigil of the', 'hex. Each one', 'wakes its kin.'], color='light_purple')
    B.lectern(197, W, 124, 'west', *L.BOOKS['witch'])
    B.pz(7, 'lights', 199, W + 6, 131)
    B.fx(188, W + 8, 132)
    # SECRET 2 (look up): a button on the underside of the one shelf that hangs low; the closet in the north-east corner
    B.sbutton(188, W + 2, 120, 'polished_blackstone_button[face=ceiling,facing=north,powered=false]', 2)
    for x in range(198, 205):
        for y in range(W, W + 6): s(x, y, 115, k.pick(HEX))
    for z in range(110, 116):
        for y in range(W, W + 6): s(198, y, z, k.pick(HEX))
    k.fill(199, W + 4, 110, 204, W + 5, 114, HEX)
    B.sdoor(201, W, 115, 2)
    B.chest(203, W, 111, 'west', loot='bm:p2/under/hidden')
    s(199, W, 111, 'purple_candle[candles=2,lit=true,waterlogged=false]')
    # ---------------- G7 -> the Serpent's door: Apophiss's sigil (P8)
    k.room(180, W, 97, 196, W + 8, 107, wall=HEX)
    k.air(187, W, 109, 189, W + 3, 109)
    B.sigil(8, 188, W, 101, 'apo')
    B.pz(8, 'sigil', 188, W + 3, 104)
    k.sign(185, W + 1, 97, 'south', ['ONE THAT', 'CRAWLS', 'OPENS THE', 'CRAWL.'], color='green')
    for x in (181, 195):
        for z in range(98, 107, 2): s(x, W, z, 'purple_candle[candles=1,lit=true,waterlogged=false]')
    # ---------------- G8 -> the serpent crawl -> King Omega's door (P9)
    k.air(188, W, 95, 189, W + 2, 95)
    crawl(k, CRAWL, W)
    k.room(202, W, 158, 216, W + 7, 168, wall=BONE)
    B.sigil(9, 209, W, 163, 'omega')
    B.pz(9, 'sigil', 212, W + 3, 165)
    k.sign(209, W + 1, 168, 'north', ['THE DEAD', 'STEP ASIDE', 'FOR THEIR', 'KING.'], color='white')
    for x in (204, 214):
        s(x, W, 160, 'bone_block[axis=y]'); s(x, W + 1, 160, 'skeleton_skull[powered=false,rotation=0]')
        s(x, W, 166, 'bone_block[axis=y]'); s(x, W + 1, 166, 'skeleton_skull[powered=false,rotation=8]')
    k.hang(209, W + 5, 163, 2)
    # ---------------- G9 -> the ossuary; the Ossuary of the Unbound off its south wall (Wilfrey)
    k.room(184, W, 158, 200, W + 8, 170, wall=BONE, floor=[('bone_block[axis=x]', 1), ('polished_blackstone', 2)])
    for x in range(185, 200, 2):
        for z in (158, 170):
            for y in (W + 2, W + 5):
                if B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, 'skeleton_skull[powered=false,rotation=%d]' % (0 if z == 158 else 8))
    for z in range(160, 170, 3):
        s(185, W + 3, z, 'wither_skeleton_skull[powered=false,rotation=4]')
    for x in range(186, 199, 4):
        s(x, W, 164, 'bone_block[axis=y]'); s(x, W + 1, 164, 'bone_block[axis=y]'); s(x, W + 2, 164, 'skeleton_skull[powered=false,rotation=0]')
    k.hang(192, W + 6, 161, 2); k.hang(192, W + 6, 167, 2)
    k.room(186, W, 174, 198, W + 6, 182, wall=BONE, floor=[('polished_blackstone_bricks', 1)])
    k.air(191, W, 171, 193, W + 2, 171)
    k.air(191, W, 173, 193, W + 2, 173)
    B.hidden('ossuary', 192, W, 172, 'x', 1, 3, 'bone_block[axis=y]', [('wil', 192, W, 168)])
    k.sign(195, W + 1, 170, 'north', ['THE UNBOUND', 'KNIGHTS WAIT', 'FOR THEIR', 'OLD FRIEND.'], color='white')
    for x in range(187, 198, 3):                               # the Unbound Knights' tombs: banners over sarcophagi
        s(x, W, 181, 'polished_blackstone_bricks'); s(x, W + 1, 181, 'wither_skeleton_skull[powered=false,rotation=0]')
        s(x, W + 3, 182, 'black_wall_banner[facing=north]')
        s(x, W, 175, 'polished_blackstone_bricks'); s(x, W + 1, 175, 'skeleton_skull[powered=false,rotation=8]')
    s(192, W - 1, 178, 'chiseled_polished_blackstone'); B.relic('ossuary', 192, W, 178)
    B.chest(197, W, 178, 'west', loot='bm:p2/under/hidden')
    s(189, W + 5, 178, SOUL)
    # ---------------- P10 THE ECHO OF THE WITCH (a round hex arena) -> G10 back to the entry hall
    cx, cz = 163, 170
    for x in range(cx - 19, cx + 20):
        for z in range(cz - 19, cz + 20):
            r = math.hypot(x - cx, z - cz)
            if r > 18.5: continue
            top = W + 7 + int(11 * math.sqrt(max(0.0, 1 - (r / 16.0) ** 2)))
            if r <= 15.2:
                s(x, W - 1, z, 'amethyst_block' if int(r) in (5, 11) else 'obsidian' if (x + z) % 2 else 'purpur_block')
                s(x, W - 2, z, k.pick(VOID))
                for y in range(W, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 3): s(x, y, z, k.pick(HEX))
            else:
                for y in range(W - 2, W + 21):
                    if (x, y, z) not in B.b: s(x, y, z, k.pick(HEX))
    for a in range(0, 360, 45):
        px, pz = round(cx + 13 * math.cos(math.radians(a + 22))), round(cz + 13 * math.sin(math.radians(a + 22)))
        for y in range(W, W + 7): s(px, y, pz, 'purpur_pillar[axis=y]')
        s(px, W + 7, pz, 'amethyst_block'); s(px, W + 8, pz, 'amethyst_cluster[facing=up,waterlogged=false]')
    k.air(177, W, 168, 183, W + 3, 170)
    k.fill(177, W - 1, 168, 183, W - 1, 170, 'polished_blackstone_bricks')
    B.echo(10, cx, W, cz, 'witch', r=14)
    B.vault(cx, W, 184, 'north', 'ukey', 'bm:p2/under/ward')
    k.hang(cx, W + 12, cz, 5)
    B.fx(cx, W + 8, cz)
    tube(k, [(163, 154, W), (163, 143, W)], w=3, h=5, wall=HEX)
    # ---------------- the gates
    B.gate(152, W, 134, 'z', 5)
    B.gate(170, W, 134, 'z', 6)
    B.gate(188, W, 108, 'x', 7)
    B.gate(188, W, 96, 'x', 8)
    B.gate(201, W, 163, 'z', 9)
    B.gate(163, W, 147, 'x', 10)


# ===================================================================================================== THE DROWNED WARD
SHIP_X0, SHIP_X1, SHIP_ZC = 93, 146, 205.5
KEEL, HOLD, GUN, DECK = 22, 24, 33, 38                     # keel plate y; walk y of the hold, the gun deck, the main deck
DECK_W = [('dark_oak_planks', 4), ('stripped_dark_oak_wood', 1), ('dark_oak_slab[type=double,waterlogged=false]', 1)]


def hw_at(x):
    """the ship's half-beam at x (the bow tapers into the rock it rammed)"""
    if x < 106: return max(2.6, 10.5 * (x - SHIP_X0 + 2) / 15)
    if x > 143: return 10.5 - (x - 143) * 0.8
    return 10.5


def drowned(k):
    B, s, rnd = k.B, k.s, k.rnd
    W = DROWNED_Y
    # ---------------- the cavern (lava below everything), the ledge, the ship's gangway (G11)
    for x in range(86, 155):
        for z in range(183, 224):
            e = ((x - 120) / 29.0) ** 4 + ((z - 204.3) / 16.2) ** 4
            if e > 1.6: continue
            hi = 20 * min(1.0, max(0.0, (144 - x) / 8.0))            # the vault rises to ~78 over the ship (not by the Hexed arena)
            top = 58 + int(hi) + int(4 * math.sin(x / 5.0) * math.cos(z / 4.0)) - int(max(0.0, e - 0.6) * (18 + hi))
            if e <= 1.0 - rnd.random() * 0.05:
                for y in range(4, 7): s(x, y, z, k.pick(ROCK))
                for y in range(7, 10): s(x, y, z, 'lava')
                for y in range(10, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 4): s(x, y, z, k.pick(ROCK))
            else:
                for y in range(3, 84):
                    if (x, y, z) not in B.b: s(x, y, z, k.pick(ROCK))
    for x in range(86, 155):                                 # make sure every lava cell is held: rock round the lake's rim
        for z in range(183, 224):
            for y in range(7, 10):
                if B.b.get((x, y, z), '').endswith('lava'):
                    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (x + dx, y, z + dz)
                        if q not in B.b or B.b[q].endswith(':air'): s(*q, k.pick(ROCK))
    for x in range(102, 133):
        for z in range(188, 192):
            for y in range(4, W): s(x, y, z, k.pick(ROCK) if y < W - 1 else k.pick(FLOOR))
            for y in range(W, W + 6): s(x, y, z, 'air')
    for x in range(102, 133): s(x, W, 191, 'polished_blackstone_wall') if x % 3 == 0 and not 113 <= x <= 121 else None
    B.voice('drowned', 117, W, 189, r=6)
    for x in (114, 115, 119, 120):                           # the gatehouse over the gangway
        for z in range(191, 195):
            for y in range(W - 1, W + 6): s(x, y, z, 'dark_prismarine' if (y + z) % 3 else 'prismarine_bricks')
    for x in range(116, 119):
        for z in range(191, 195):
            for y in (W + 4, W + 5): s(x, y, z, 'dark_prismarine')
            s(x, W - 1, z, 'dark_oak_planks')
            for y in range(W, W + 4): s(x, y, z, 'air')
        s(x, W, 194, 'dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    B.sigil(11, 117, W, 189, 'pearlq')
    B.pz(11, 'sigil', 121, W + 3, 189)
    k.sign(115, W + 2, 190, 'north', ["THE QUEEN'S", 'SHIP KNOWS', 'HER STEP.', ''], color='aqua')
    k.hang(110, W + 4, 189, 1); k.hang(125, W + 4, 189, 1)
    # ---------------- the rock the ship's bow is rammed into
    k.fill(84, 4, 197, 95, 34, 214, ROCK)
    # ---------------- THE WARSHIP: hull, keel, three decks
    for x in range(SHIP_X0, SHIP_X1 + 1):
        hw = hw_at(x)
        for z in range(int(SHIP_ZC - hw) - 1, int(SHIP_ZC + hw) + 2):
            dd = abs(z + 0.5 - SHIP_ZC - 0.5)
            if dd > hw: continue
            shell = dd > hw - 1
            for y in range(KEEL - 2, DECK + 2):
                if y < KEEL:
                    if dd <= 1.5: s(x, y, z, 'dark_prismarine')
                    continue
                if y == KEEL:
                    if dd <= hw - 1.5: s(x, y, z, k.pick(HULL))
                    elif dd <= hw: s(x, y, z, 'prismarine_bricks')
                    continue
                if shell:
                    s(x, y, z, k.pick(HULL) if y < DECK - 1 else 'dark_prismarine' if y < DECK + 1 else 'prismarine_brick_wall')
                    continue
                if y in (HOLD - 1, GUN - 1, DECK - 1): s(x, y, z, k.pick(DECK_W))
                elif y < DECK: s(x, y, z, 'air')
                else: s(x, y, z, 'air')
            if shell:
                for y in range(DECK + 2, DECK + 2): pass
        if x in (SHIP_X0, SHIP_X1):
            for z in range(int(SHIP_ZC - hw), int(SHIP_ZC + hw) + 1):
                for y in range(KEEL, DECK + 1): s(x, y, z, k.pick(HULL))
    for x in range(SHIP_X0, SHIP_X1 + 1):                     # the bulwark is the shell's top (2 high), weathered copper rail
        hw = hw_at(x)
        for z in range(int(SHIP_ZC - hw) - 1, int(SHIP_ZC + hw) + 2):
            dd = abs(z + 0.5 - SHIP_ZC - 0.5)
            if hw - 1 < dd <= hw or x in (SHIP_X0, SHIP_X1):
                if dd <= hw:
                    s(x, DECK, z, 'dark_prismarine'); s(x, DECK + 1, z, 'weathered_cut_copper')
    for x in range(SHIP_X0 + 1, SHIP_X1, 5):                  # ribs inside the hold, and cracks in the hull
        hw = hw_at(x)
        for z in range(int(SHIP_ZC - hw), int(SHIP_ZC + hw) + 1):
            dd = abs(z + 0.5 - SHIP_ZC - 0.5)
            if hw - 2 < dd <= hw - 1:
                for y in range(HOLD, GUN - 1): s(x, y, z, 'dark_oak_log[axis=y]')
    for _ in range(140):
        x, y = rnd.randint(SHIP_X0 + 3, SHIP_X1 - 1), rnd.randint(KEEL + 1, DECK - 2)
        z = round(SHIP_ZC - 0.5 + rnd.choice((-1, 1)) * hw_at(x))
        if B.b.get((x, y, z), '').split(':')[-1].startswith(('prism', 'dark_prism', 'weathered', 'oxidized')):
            s(x, y, z, rnd.choice(('dead_tube_coral_block', 'dead_brain_coral_block', 'cracked_deepslate_tiles', 'oxidized_copper')))
    # the gangway port through the bulwark
    for x in range(116, 119):
        s(x, W + 1, 195, 'dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
        for y in range(W + 2, W + 6): s(x, y, 195, 'air')
        s(x, W, 195, 'dark_prismarine')
    # masts (broken), torn sails, and the chains it hangs by
    for mx, top in ((108, 52), (122, 58), (136, 50)):
        for y in range(HOLD, top): s(mx, y, 205, 'dark_oak_log[axis=y]')
        for y in range(HOLD, top): s(mx + 1, y, 205, 'dark_oak_log[axis=y]') if y > DECK + 6 else None
        for z in range(199, 213): s(mx, top - 4, z, 'dark_oak_log[axis=z]')
        for z in range(200, 212):
            for y in range(top - 12, top - 4):
                if rnd.random() < 0.55 and (z + y) % 4: s(mx + 1, y, z, rnd.choice(('gray_wool', 'black_wool', 'light_gray_wool')))
        for y in range(HOLD, DECK + 7): s(mx + 1, y, 205, 'air') if y >= DECK else None
    for (x, z) in ((98, 201), (98, 210), (110, 195), (110, 216), (126, 195), (126, 216), (142, 197), (142, 214)):
        for y in range(DECK + 2, 84):
            if B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, CHAIN_Y)
            elif y > DECK + 4: break
    for (x, z) in ((104, 193), (134, 193), (104, 218), (134, 218)):          # four colossal links, from the hull up into the vault
        for y0 in range(DECK - 6, 84, 5):
            j = (y0 // 5) % 2
            for dy in range(7):
                for dw in range(-2, 3):
                    if (dy in (0, 6) or dw in (-2, 2)) and not (dy in (0, 6) and dw in (-2, 2)):
                        q = (x + dw, y0 + dy, z) if j == 0 else (x, y0 + dy, z + dw)
                        if B.b.get(q, '').endswith(':air'): s(*q, 'polished_deepslate')
    # ---------------- P12 THE KINGDOM'S SONG: five bells on the deck, the listening conch at the mainmast
    order = {0: 3, 1: 1, 2: 5, 3: 2, 4: 4}
    bells = [(112, 199, 'south'), (118, 199, 'south'), (128, 199, 'south'), (114, 212, 'north'), (126, 212, 'north')]
    for i, (x, z, f) in enumerate(bells):
        s(x, DECK, z, 'dark_prismarine'); s(x, DECK + 1, z, 'bell[attachment=floor,facing=north,powered=false]')
        bz = z + (1 if f == 'south' else -1)
        B.seq_button(12, x, DECK, bz, f'stone_button[face=wall,facing={f},powered=false]', order[i], sound=i + 1)
    B.listen_button(12, 123, DECK + 1, 205, 'polished_blackstone_button[face=wall,facing=east,powered=false]')
    k.sign(123, DECK + 2, 205, 'east', ['Press the conch', 'to hear the', "Kingdom's Song.", 'Ring it back.'], color='aqua')
    s(122, DECK + 2, 204, 'dark_oak_log[axis=y]') if False else None
    B.lectern(116, DECK, 205, 'east', *L.BOOKS['drowned'])
    B.pz(12, 'simon', 118, DECK + 3, 205)
    SEQS.setdefault(U.d, {})[12] = 5
    for (x, z) in ((104, 205), (132, 200), (132, 211)):
        s(x, DECK, z, 'dark_oak_fence'); s(x, DECK + 1, z, 'soul_lantern[hanging=false,waterlogged=false]')
    B.fx(120, DECK + 6, 205)
    # ---------------- G12: the companionway down to the gun deck
    for x in range(100, 108):
        for z in range(203, 209):
            for y in range(DECK, DECK + 5):
                if x in (100, 107) or z in (203, 208) or y == DECK + 4: s(x, y, z, 'dark_oak_planks' if y < DECK + 4 else 'dark_prismarine')
                else: s(x, y, z, 'air')
    for i, x in enumerate(range(106, 100, -1)):
        w = DECK - i                                          # x106 walk 38 .. x101 walk 33
        for z in range(204, 207):
            for y in range(GUN - 1, w - 1): s(x, y, z, 'dark_oak_planks')
            s(x, w - 1, z, 'dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]' if 0 < i else 'dark_oak_planks')
            for y in range(w, DECK + 4): s(x, y, z, 'air')
    # ---------------- P13 EMMA + BONES on the gun deck (the keel's door, G13)
    for x in range(108, 141, 6):                              # cannons: dark barrels at the gun ports
        for z, f in ((197, 'north'), (214, 'south')):
            if B.b.get((x, GUN, z), '').endswith(':air'): s(x, GUN, z, 'black_concrete'); s(x, GUN, z + (1 if f == 'south' else -1), 'polished_blackstone')
    B.sigil(13, 112, GUN, 200, 'emma')
    B.sigil(13, 124, GUN, 211, 'bones')
    B.pz(13, 'sigil', 118, GUN + 2, 205)
    k.sign(129, GUN + 1, 202, 'north', ['THE KEEL', 'OPENS FOR', 'TWO OLD', 'FRIENDS.'], color='aqua')
    k.hang(110, GUN + 2, 205, 1); k.hang(130, GUN + 2, 199, 1)
    for x in range(128, 141):                                 # the keel stair (behind G13), down into the hold
        for z in range(203, 208):
            for y in range(GUN, DECK - 1):
                if z in (203, 207) or x == 140: s(x, y, z, 'dark_oak_planks')
    for i, x in enumerate(range(129, 138)):
        w = GUN - 1 - i                                       # x129 walk 32 .. x137 walk 24
        for z in range(204, 207):
            for y in range(HOLD - 1, w - 1): s(x, y, z, 'dark_oak_planks')
            s(x, w - 1, z, 'dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
            for y in range(w, GUN + 4): s(x, y, z, 'air')
    for x in (138, 139):
        for z in range(204, 207):
            for y in range(HOLD, GUN + 4): s(x, y, z, 'air')
    # ---------------- P14 THE DRIED DROWNED in the hold
    B.pz(14, 'waves', 118, HOLD, 205)
    for (x, z) in ((108, 199), (108, 212), (118, 198), (118, 213), (128, 199), (128, 212)):
        B.el(14, 'wsp', x, HOLD, z)
    for (x, z) in ((112, 205), (124, 205)):
        k.hang(x, HOLD + 5, z, 2)
    for (x, z) in ((106, 197), (106, 214), (139, 197), (139, 214), (134, 198)):
        s(x, HOLD, z, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel'})
    k.sign(105, HOLD + 1, 208, 'east', ['THE DRIED', 'DROWNED', 'They still', 'serve the ship.'], color='aqua')
    B.fx(120, HOLD + 4, 205)
    # bulkhead before the bow (G14), the bow compartment, and the breach into the rock
    for z in range(195, 217):
        for y in range(HOLD, GUN - 1):
            if B.b.get((104, y, z), '').endswith(':air'): s(104, y, z, 'dark_oak_planks')
    k.air(86, HOLD, 204, 103, HOLD + 3, 206)
    k.fill(86, HOLD - 1, 204, 103, HOLD - 1, 206, 'dark_oak_planks')
    for x in range(86, 93):
        for z in (203, 207):
            for y in range(HOLD - 1, HOLD + 5): s(x, y, z, k.pick(ROCK))
        for z in range(204, 207): s(x, HOLD + 4, z, k.pick(ROCK))
    tube(k, [(85, 205, HOLD), (82, 205, 22)], w=3, h=5, wall=ROCK)
    # ---------------- P15 THE ECHO OF THE SAWSHARK: the dried sea-bed under the cavern (out of the ship)
    cx, cz, Y = 66, 200, 22
    for x in range(cx - 20, cx + 21):
        for z in range(cz - 20, cz + 21):
            r = math.hypot(x - cx, z - cz)
            if r > 19.5 or not (0 <= z < SZ - 2): continue
            top = Y + 7 + int(11 * math.sqrt(max(0.0, 1 - (r / 17.0) ** 2)))
            if r <= 16.2:
                s(x, Y - 1, z, rnd.choice(('sandstone', 'smooth_sandstone', 'dead_brain_coral_block', 'prismarine', 'sandstone')))
                s(x, Y - 2, z, k.pick(ROCK))
                for y in range(Y, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 3): s(x, y, z, k.pick(ROCK))
            else:
                for y in range(Y - 2, Y + 21):
                    if (x, y, z) not in B.b: s(x, y, z, k.pick(ROCK))
    for a in range(0, 360, 40):                                # bleached ribs of something enormous
        px, pz = round(cx + 14 * math.cos(math.radians(a))), round(cz + 14 * math.sin(math.radians(a)))
        for y in range(Y, Y + 9):
            if B.b.get((px, y, pz), '').endswith(':air'): s(px, y, pz, 'bone_block[axis=y]')
    for (x, z) in ((58, 192), (74, 208), (60, 208)):
        s(x, Y, z, 'dead_fire_coral_block'); s(x, Y + 1, z, 'dead_horn_coral')
    k.air(80, Y, 204, 82, Y + 3, 206)
    B.echo(15, cx, Y, cz, 'shark', r=14)
    B.vault(cx, Y, 215, 'north', 'ukey', 'bm:p2/under/ward')
    k.hang(cx, Y + 12, cz, 5)
    B.fx(cx, Y + 8, cz)
    # ---------------- G15 out: the way to the Hall's floor
    tube(k, [(66, 183, Y), (66, 168, 20), (96, 168, FLOOR_Y)], w=3, h=5, wall=VOID)
    # ---------------- the gates
    B.gate(117, W, 187, 'x', 10)
    B.gate(117, W, 192, 'x', 11)
    B.gate(107, DECK, 205, 'z', 12)
    B.gate(128, GUN, 205, 'z', 13)
    B.gate(104, HOLD, 205, 'z', 14)
    B.gate(66, Y, 182, 'x', 15)


# ===================================================================================================== THE CHAINMAKER'S FORGE
def forge(k):
    B, s = k.B, k.s
    y = FLOOR_Y
    k.room(148, y, 136, 164, y + 8, 154, wall=VOID, floor=[('polished_blackstone', 2), ('blackstone', 1)])
    k.air(140, y, 144, 140, y + 2, 146)
    k.air(142, y, 144, 147, y + 2, 146)
    k.fill(140, y - 1, 144, 147, y - 1, 146, 'polished_blackstone')
    for z in range(143, 148):
        for yy in range(y, y + 3):
            if z in (143, 147): s(141, yy, z, 'iron_bars')
    B.hidden('forge', 141, y, 145, 'z', 1, 3, 'iron_bars', [('bender', 135, y, 145)])
    k.sign(137, y, 148, 12, ['A CHAIN GATE.', 'SOMETHING WITH', 'GOOD TEETH', 'COULD CHEW IT.'], color='gold', wall=False)
    for x in range(155, 159):                                  # the quench: a lava basin in the floor
        for z in range(139, 143):
            s(x, y - 1, z, 'lava' if 156 <= x <= 157 and 140 <= z <= 141 else 'polished_blackstone_bricks')
            s(x, y - 2, z, 'polished_blackstone_bricks')
    for (x, z) in ((152, 139), (152, 151), (160, 147)):
        s(x, y, z, 'anvil[facing=north]')
    s(161, y, 139, 'blast_furnace[facing=west,lit=true]'); s(162, y, 139, 'smithing_table'); s(163, y, 140, 'magma_block')
    for z in range(138, 153, 2):                               # chain racks along the east wall
        for yy in range(y + 1, y + 7): s(163, yy, z, CHAIN_Y)
        s(163, y + 7, z, 'polished_blackstone_bricks')
    for x in range(150, 162, 3):
        for yy in range(y + 3, y + 8): s(x, yy, 153, CHAIN_Y)
    B.lectern(150, y, 145, 'east', *L.BOOKS['chains'])
    s(158, y - 1, 148, 'gilded_blackstone'); B.relic('forge', 158, y, 148)
    B.chest(163, y, 151, 'west', loot='bm:p2/under/hidden')
    k.hang(156, y + 6, 145, 2)


# ===================================================================================================== THE THRONE OF THE DREAD
A = U.ARENA
ACX, AFY, ACZ = A['c']                                        # (112, 12, 42): the floor's top layer
AR = A['r']


def dome_top(r):
    """the arena's ceiling over radius r: a sheer wall to y 30, then a dome to ARENA['dome']"""
    if r >= AR: return 30
    return 30 + (A['dome'] - 30) * math.sqrt(max(0.0, 1 - (r / AR) ** 2))


def pillars():
    out = []
    for i in range(A['pil_n']):
        a = math.radians(60 * i)
        out.append((i + 1, ACX + A['pil_r'] * math.cos(a), ACZ + A['pil_r'] * math.sin(a)))
    return out


def chain_line(k, p, q):
    """a line of iron chain from p to q (each link turned along the way it runs)"""
    (x1, y1, z1), (x2, y2, z2) = p, q
    n = int(max(abs(x2 - x1), abs(y2 - y1), abs(z2 - z1))) + 1
    for i in range(n + 1):
        t = i / n
        c = (round(x1 + (x2 - x1) * t), round(y1 + (y2 - y1) * t), round(z1 + (z2 - z1) * t))
        dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
        ax = 'x' if dx >= max(dy, dz) else 'z' if dz >= dy else 'y'
        if k.B.b.get(c, '').endswith(':air'): k.s(*c, f'iron_chain[axis={ax},waterlogged=false]')


def throne_room(k):
    B, s, rnd = k.B, k.s, k.rnd
    PIL = pillars()
    near_pil = lambda x, z, rr: any(math.hypot(x - px, z - pz) <= rr for (_, px, pz) in PIL)
    dais = set()
    for x in range(ACX - 40, ACX + 41):
        for z in range(0, ACZ + 41):
            r = math.hypot(x - ACX, z - ACZ)
            if r > 38.6: continue
            if r <= AR and z <= 17 and abs(x - ACX) <= 13: dais.add((x, z))
            s(x, 0, z, 'blackstone'); s(x, 1, z, 'obsidian' if (x + z) % 3 else 'blackstone')
            if r <= AR:
                for y in range(2, 7): s(x, y, z, 'lava')
                for y in range(7, 11): s(x, y, z, 'air')
                top = int(dome_top(r))
                for y in range(13, top + 1): s(x, y, z, 'air')
                for y in range(top + 1, top + 4): s(x, y, z, k.pick(VOID))
            else:
                for y in range(2, 35): s(x, y, z, k.pick(VOID))
    # ---- the floor: an inner ring that never falls, six islands, the throne's dais; the rest void-glass with red cracks
    cracks = set()
    for c in range(14):
        a = math.radians(c * 360 / 14 + rnd.uniform(-8, 8))
        r, ang = 14.5, a
        while r < AR:
            x, z = round(ACX + r * math.cos(ang)), round(ACZ + r * math.sin(ang))
            cracks.add((x, z))
            if rnd.random() < 0.25: cracks.add((x + rnd.choice((-1, 1)), z))
            r += 0.7; ang += rnd.uniform(-0.05, 0.05)
    for x in range(ACX - AR - 1, ACX + AR + 2):
        for z in range(max(0, ACZ - AR - 1), ACZ + AR + 2):
            r = math.hypot(x - ACX, z - ACZ)
            if r > AR: continue
            isl = near_pil(x, z, A['isl_r'])
            if r <= A['inner']:
                top = ('gilded_blackstone' if 4.0 <= r < 4.8 or 9.0 <= r < 9.8 else 'chiseled_polished_blackstone' if r >= 13.2
                       else 'red_nether_bricks' if r < 2.2 else 'polished_blackstone' if (x + z) % 2 else 'polished_blackstone_bricks')
                s(x, 11, z, 'polished_blackstone'); s(x, 12, z, top)
            elif isl or (x, z) in dais:
                rim = isl and any(5.2 <= math.hypot(x - px, z - pz) <= 6.0 for (_, px, pz) in PIL)
                s(x, 11, z, 'polished_blackstone')
                s(x, 12, z, 'gilded_blackstone' if rim and (x + z) % 2 else 'chiseled_polished_blackstone' if rim else
                  'polished_blackstone_bricks' if (x * 3 + z) % 5 else 'polished_blackstone')
            elif (x, z) in cracks:
                s(x, 11, z, 'magma_block'); s(x, 12, z, 'red_stained_glass')
            else:
                u = rnd.random()
                if u < 0.42: s(x, 11, z, 'obsidian'); s(x, 12, z, 'black_stained_glass')
                elif u < 0.47: s(x, 11, z, 'crying_obsidian'); s(x, 12, z, 'purple_stained_glass')
                elif u < 0.75: s(x, 11, z, 'obsidian'); s(x, 12, z, 'black_concrete')
                else: s(x, 11, z, 'blackstone'); s(x, 12, z, 'obsidian')
            if r <= 5:                                           # the inner ring's own column, down to the sea floor
                for y in range(2, 11): s(x, y, z, k.pick(VOID))
            if (x, z) in dais:
                for y in range(2, 11): s(x, y, z, 'polished_blackstone_bricks' if y > 7 else 'blackstone')
    B.meta['under']['dais'] = sorted(dais)
    # ---- the six pillars (on cones of rock under their islands), their Wellsprings, a few obsidian slabs to hide behind
    for (i, px, pz) in PIL:
        for x in range(int(px) - 7, int(px) + 8):
            for z in range(int(pz) - 7, int(pz) + 8):
                d = math.hypot(x - px, z - pz)
                if d <= A['pil_w']:
                    for y in range(2, 70):
                        st = B.b.get((x, y, z))
                        if y > 12 and st and not st.endswith(':air'): break
                        band = (y - 13) % 12
                        s(x, y, z, 'chiseled_polished_blackstone' if band == 0 else 'deepslate_tiles' if band in (5, 6) else 'polished_blackstone_bricks')
                elif d <= 3 + (2 if True else 0):
                    pass
                for y in range(7, 11):
                    if d <= 3 + (y - 6) * 0.75 and B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, k.pick(ROCK))
        ux, uz = (ACX - px) / A['pil_r'], (ACZ - pz) / A['pil_r']
        inpil = lambda x, z: math.hypot(x - px, z - pz) <= A['pil_w']
        for t in [3 + j * 0.1 for j in range(16)]:               # the first cell along the inward ray that touches the pillar's face
            wx, wz = round(px + ux * t), round(pz + uz * t)
            if not inpil(wx, wz) and any(inpil(wx + a_, wz + b_) for a_, b_ in ((1, 0), (-1, 0), (0, 1), (0, -1))): break
        s(wx, A['well_y'] - 1, wz, 'chiseled_polished_blackstone')
        s(wx, A['well_y'], wz, 'air')
        B.well(i, wx, A['well_y'], wz)
        for y in range(18, 60, 7):                               # chains wound round the pillar
            for a in range(0, 360, 30):
                cx_, cz_ = round(px + 3.6 * math.cos(math.radians(a + y * 9))), round(pz + 3.6 * math.sin(math.radians(a + y * 9)))
                if B.b.get((cx_, y, cz_), '').endswith(':air') and (cx_, cz_) != (wx, wz): s(cx_, y, cz_, 'iron_chain[axis=y,waterlogged=false]')
        if i in (1, 3, 5):
            ox, oz = round(px - uz * 4.5), round(pz + ux * 4.5)
            for y in range(13, 18):
                for o in (-1, 0, 1):
                    q = (ox + round(ux * o), y, oz + round(uz * o))
                    if B.b.get(q, '').endswith(':air'): s(*q, 'obsidian' if y < 17 else 'crying_obsidian')
    # ---- the wall: piers every 15 degrees, deep niches between with red windows; chains hang the height of the dome
    for x in range(ACX - 40, ACX + 41):
        for z in range(0, ACZ + 41):
            r = math.hypot(x - ACX, z - ACZ)
            if not (AR < r <= 37.6): continue
            ang = math.degrees(math.atan2(z - ACZ, x - ACX)) % 360
            off = (ang % 15) - 7.5
            if abs(off) * math.pi / 180 * r < 3.2 and not (60 <= ang <= 120) and not (240 <= ang <= 300):
                if r <= 35.6:
                    for y in range(14, 29): s(x, y, z, 'air')
                elif r <= 36.6:
                    for y in range(17, 27): s(x, y, z, 'red_stained_glass')
                else:
                    for y in range(17, 27): s(x, y, z, 'magma_block')
    for a in range(0, 360, 15):
        x, z = round(ACX + 33.5 * math.cos(math.radians(a))), round(ACZ + 33.5 * math.sin(math.radians(a)))
        top = int(dome_top(33.5))
        if 70 <= a <= 110: continue
        for y in range(18, top):
            if B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, CHAIN_Y)
    # ---- the throne: a colossus' seat. An apse is cut into the north wall and dome behind it (black, with a great red rose window
    #      burning at its back); the throne stands before it in red nether brick and gilded blackstone, edged in crying obsidian,
    #      its spikes tipped with shroomlight; its back arches over the Hoard's door; chains radiate from it into the dome
    k.fill(ACX - 16, 21, 0, ACX + 16, 70, 30, VOID, soft=True)
    def apse_hw(y):
        return 13.0 if y <= 50 else 13.0 * math.sqrt(max(0.0, 1 - ((y - 50) / 14.0) ** 2))
    for x in range(ACX - 14, ACX + 15):
        for y in range(23, 65):
            if abs(x - ACX) > apse_hw(y): continue
            for z in range(4, 31 if y > 30 else 9):
                st = B.b.get((x, y, z), '')
                if st.endswith(':air') and y > 30: break           # reached the arena's own air
                if any(math.hypot(x - px, z - pz) <= A['pil_w'] + 0.6 for (_, px, pz) in PIL): break
                s(x, y, z, 'air')
            s(x, y, 3, 'black_concrete'); s(x, y, 2, 'obsidian'); s(x, y, 1, k.pick(VOID))
        s(x, 23, 4, 'obsidian')
    for x in range(ACX - 15, ACX + 16):                            # the apse's floor over the Hoard's ceiling
        for z in range(3, 8):
            if B.b.get((x, 23, z), '').endswith(':air') or (x, 23, z) not in B.b: s(x, 23, z, 'obsidian')
            if B.b.get((x, 22, z), '').endswith(':air') and z < 9: s(x, 22, z, k.pick(VOID))
    RX, RY, RR = ACX, 46, 12.0                                      # the rose window: red glass over fire, black tracery
    for x in range(ACX - 13, ACX + 14):
        for y in range(RY - 13, RY + 14):
            d = math.hypot(x - RX, y - RY)
            if d > RR: continue
            ang = math.degrees(math.atan2(y - RY, x - RX)) % 45
            tracery = d < 1.6 or abs(d - 5.5) < 0.55 or abs(d - 9) < 0.5 or (d > 2 and min(ang, 45 - ang) * math.pi / 180 * d < 0.5)
            s(x, y, 3, 'black_concrete' if tracery else 'red_stained_glass')
            if not tracery: s(x, y, 2, 'shroomlight' if (x + y) % 3 == 0 or d < 4 else 'magma_block')
            if d > RR - 1.2: s(x, y, 3, 'gilded_blackstone')
    for x in range(ACX - 11, ACX + 12):
        dx = abs(x - ACX)
        top = 46 - int(dx * 1.2) + (6 if dx == 0 else 3 if dx in (4, 8) else 0)
        for z in (8, 9):
            for y in range(13, top + 1):
                arch = dx <= 3 and y <= 13 + 8 - (1 if dx == 3 else 0)
                if arch: s(x, y, z, 'air'); continue
                st = 'red_nether_bricks' if (dx + y) % 9 else 'nether_wart_block'
                if dx in (3, 6, 9) or y in (24, 32): st = 'gilded_blackstone'
                if dx <= 3 and y in (22, 23): st = 'gilded_blackstone'
                s(x, y, z, st)
        if dx in (0, 4, 8): s(x, top + 1, 9, 'shroomlight')
    sil = {(x, y) for x in range(ACX - 11, ACX + 12) for y in range(13, 60) if B.b.get((x, y, 9), '').split(':')[-1].startswith(
        ('red_nether', 'nether_wart', 'gilded'))}
    for (x, y) in sil:                                             # the lit outline: every edge of the silhouette
        if any((x + a, y + b) not in sil for a, b in ((1, 0), (-1, 0), (0, 1))):
            if not (abs(x - ACX) <= 4 and y <= 22): s(x, y, 9, 'crying_obsidian')
    for side in (-1, 1):                                           # the arms: great blocks, gilded, edged and tipped with light
        for x in range(ACX + side * 7, ACX + side * 13, side):
            for z in range(10, 18):
                for y in range(13, 22 + (2 if z < 12 else 0)):
                    edge = x == ACX + side * 7 or z == 17 or y == 21 + (2 if z < 12 else 0)
                    s(x, y, z, 'gilded_blackstone' if y >= 21 + (2 if z < 12 else 0) else 'crying_obsidian' if edge and (y + z) % 4 == 0
                      else 'red_nether_bricks' if edge else 'polished_blackstone_bricks')
        fx = ACX + side * 8
        for y in range(22, 28): s(fx, y, 16, 'gilded_blackstone' if y < 27 else 'shroomlight')
        for y in range(13, 30): s(ACX + side * 12, y, 9, 'gilded_blackstone' if y % 4 else 'crying_obsidian')
        s(ACX + side * 12, 30, 9, 'shroomlight')
    for x in range(ACX - 3, ACX + 4):                              # the arch's floor
        s(x, 12, 8, 'polished_blackstone'); s(x, 12, 9, 'polished_blackstone')
    for z in range(10, 18): s(ACX, 13, z, 'red_carpet')
    for i in range(12):                                            # chains radiating from the throne's crown into the dome
        a = math.radians(200 + i * 140 / 11)
        tx, tz = ACX + 26 * math.cos(a), ACZ + 26 * math.sin(a)
        chain_line(k, (ACX, 50, 10), (round(tx), int(dome_top(26)) - 1, round(tz)))
    B.throne(*A['throne'])
    for (i, px, pz) in PIL:
        chain_line(k, (ACX, 34, 10), (round(px), 40, round(pz)))
    # ---- the Hoard behind the throne
    hoard_cells = []
    for x in range(ACX - 14, ACX + 15):
        for z in range(0, 14):
            r = math.hypot(x - ACX, z - ACZ)
            dx = abs(x - ACX)
            if dx <= 12 and 36.0 <= r <= 39.6:
                hoard_cells.append((x, z))
                s(x, 12, z, 'gold_block' if (x + z) % 4 == 0 else 'polished_blackstone_bricks')
                s(x, 11, z, k.pick(VOID))
                for y in range(13, 21): s(x, y, z, 'air')
                s(x, 21, z, k.pick(VOID)); s(x, 22, z, k.pick(VOID))
            elif dx <= 14 and 34.0 < r <= 41.6:
                for y in range(11, 23):
                    if not B.b.get((x, y, z), '').endswith(':air'): s(x, y, z, k.pick(VOID))
    B.hoard(ACX, 13, 7, 'x', 1, 4, 'polished_blackstone_bricks')
    for (x, z) in hoard_cells:
        if rnd.random() < 0.18 and abs(x - ACX) > 2: s(x, 13, z, rnd.choice(('gold_block', 'raw_gold_block', 'gold_block')))
    for x in (ACX - 9, ACX, ACX + 9):
        zc = max(z for (xx, z) in hoard_cells if xx == x) - (1 if x == ACX else 0)
        zc = min(z for (xx, z) in hoard_cells if xx == x) + 1
        s(x, 13, zc, 'air')
        B.chest(x, 13, zc, 'south', loot='bm:p2/under/hoard')
    B.voice('hoard', ACX, 13, 5, r=4)
    s(ACX - 6, 20, 5, SOUL); s(ACX + 6, 20, 5, SOUL)
    # ---- the battle door, the markers
    k.air(ACX - 2, 13, 76, ACX + 2, 17, 79)
    k.fill(ACX - 2, 12, 76, ACX + 2, 12, 79, 'polished_blackstone')
    B.gate(ACX, 13, 77, 'x', 0, big=True)
    B.arena(ACX, 13, ACZ)
    for j in range(6):
        a = math.radians(30 + 60 * j)
        B.mspawn(round(ACX + 9 * math.cos(a)), 13, round(ACZ + 9 * math.sin(a)))
    s(ACX - 6, 12, 15, 'crying_obsidian'); B.rift(ACX - 6, 13, 15)
    B.fx(ACX, 30, ACZ); B.fx(ACX, 20, ACZ + 20); B.fx(ACX, 20, ACZ - 20)
    k.sign(ACX - 5, 13, 16, 0, ['A WAY HOME,', 'FOR AFTER.', '', ''], color='gray', wall=False)


def antechamber(k):
    B, s = k.B, k.s
    k.room(96, 13, 80, 128, 22, 88, wall=VOID)
    for x in range(97, 128):
        s(x, 12, 84, 'red_nether_bricks')
    for x in (100, 106, 118, 124):
        for z in (81, 87):
            for y in range(13, 23): s(x, y, z, 'polished_blackstone_bricks' if y % 5 else 'chiseled_polished_blackstone')
    B.lectern(109, 13, 81, 'south', *L.BOOKS['ante'])
    B.vault(102, 13, 87, 'north', 'ukey', 'bm:p2/under/vault')
    B.vault(122, 13, 87, 'north', 'ukey_victor', 'bm:p2/under/victor')
    for x in (101, 103, 121, 123): s(x, 13, 87, 'polished_blackstone_wall')
    s(126, 12, 82, 'crying_obsidian'); B.rift(126, 13, 82)
    k.sign(126, 13, 84, 8, ['A WAY HOME.', 'There is no', 'shame in it.', ''], color='gray', wall=False)
    B.voice('ante', 112, 13, 85, r=6)
    for x in (104, 120):
        k.hang(x, 18, 84, 4)
    B.fx(112, 18, 84)
    # ---- THE LAST LIGHT (the Lightbringer): a white chapel behind the west wall - a holy place hidden in the dark. A coved
    #      quartz vault, pews, a gold-trimmed altar under a stained-glass sun (white and yellow glass over froglight), banners,
    #      candles, a chandelier of light
    k.room(82, 13, 79, 93, 24, 91, wall=[('white_wool', 1)], floor=[('smooth_quartz', 3), ('white_concrete', 1)], ceil=[('smooth_quartz', 1)])
    k.fill(79, 11, 77, 95, 26, 93, VOID, soft=True)
    k.air(94, 13, 83, 94, 15, 85)
    B.hidden('last_light', 95, 13, 84, 'z', 1, 3, 'polished_blackstone_bricks', [('lightbringer', 99, 13, 84)])
    for z in range(79, 92):                                    # (the chapel's side of the shared wall is white too)
        for y in range(13, 25):
            if not B.b.get((94, y, z), '').endswith(':air'): s(94, y, z, 'white_wool')
    k.sign(98, 13, 81, 8, ['THE LAST LIGHT', 'IS KEPT FOR', 'ONE WHO KNOWS', 'THE WAY.'], color='yellow', wall=False)
    for x in range(82, 94):                                    # the coved vault, a gold rib every third bay
        for z in range(79, 92):
            cap = 24 - max(0, abs(z - 85) - 3) // 2
            for y in range(cap + 1, 25): s(x, y, z, 'gold_block' if x % 3 == 0 and y == cap + 1 else 'smooth_quartz')
    for z in range(79, 92):
        for x in range(82, 94):
            if x % 3 == 0: s(x, 25, z, 'smooth_quartz')
    for (x, z) in ((84, 81), (84, 89), (91, 81), (91, 89)):
        for y in range(13, 21): s(x, y, z, 'quartz_pillar[axis=y]')
        s(x, 21, z, 'pearlescent_froglight[axis=y]'); s(x, 22, z, 'gold_block')
    # the stained-glass sun in the west wall, lit from behind
    for z in range(81, 90):
        for y in range(14, 24):
            d = math.hypot(z - 85, (y - 18.5) * 0.9)
            if d > 4.6:
                if d <= 5.4: s(81, y, z, 'gold_block')
                continue
            ang = math.degrees(math.atan2(y - 18.5, z - 85)) % 30
            s(81, y, z, 'yellow_stained_glass' if d < 1.8 or ang < 12 else 'white_stained_glass')
            s(80, y, z, 'pearlescent_froglight[axis=y]')
    # the altar: quartz and gold, a little sun on it, candles
    for z in range(83, 88):
        s(82, 13, z, 'gold_block' if z in (83, 87) else 'chiseled_quartz_block')
        s(83, 13, z, 'gold_block' if z in (83, 87) else 'smooth_quartz')
    s(82, 14, 85, 'gold_block'); s(82, 15, 85, 'pearlescent_froglight[axis=y]')
    for z in (84, 86): s(83, 14, z, 'candle[candles=4,lit=true,waterlogged=false]')
    for z in (83, 87): s(82, 14, z, 'candle[candles=3,lit=true,waterlogged=false]')
    s(84, 12, 85, 'gold_block'); s(85, 12, 85, 'gold_block')
    s(86, 13, 85, 'air'); s(86, 12, 85, 'gold_block'); B.relic('last_light', 86, 13, 85)
    B.lectern(89, 13, 85, 'west', *L.BOOKS['vigil'])
    B.chest(83, 13, 80, 'east', loot='bm:p2/under/hidden')
    # pews either side of the aisle, a runner up it, candle stands, banners of the heralds
    for x in (88, 90, 92):
        for z in list(range(80, 84)) + list(range(87, 91)):
            if (x, z) in ((91, 81), (91, 89)): continue
            s(x, 13, z, 'birch_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
    for x in range(84, 94):
        if x not in (86, 89): s(x, 13, 85, 'yellow_carpet')
    for (x, z) in ((93, 80), (93, 90), (86, 80), (86, 90)):
        s(x, 13, z, 'quartz_pillar[axis=y]'); s(x, 14, z, 'candle[candles=4,lit=true,waterlogged=false]')
    for x in (85, 88, 91):
        s(x, 18, 79, 'white_wall_banner[facing=south]'); s(x, 18, 91, 'white_wall_banner[facing=north]')
    for y in range(20, 24): s(88, y, 85, 'iron_chain[axis=y,waterlogged=false]')
    s(88, 19, 85, 'pearlescent_froglight[axis=y]')
    B.voice('last_light', 88, 13, 85, r=5)


def eye_stair(k):
    """THE STAIR OF A THOUSAND EYES (P17, reach): a tall ribbed gallery, its walls full of shut lids, from the Throne Gate down
    to the antechamber; G17 at its foot"""
    B, s = k.B, k.s
    walk = lambda z: 18 if z >= 112 else 17 if z >= 108 else 16 if z >= 104 else 15 if z >= 100 else 14 if z >= 96 else 13
    for z in range(90, 116):
        w = walk(z)
        for x in range(107, 118):
            for y in range(9, 36):
                inner = 109 <= x <= 115
                if inner and w <= y <= 32: s(x, y, z, 'air')
                elif inner and y == w - 1: s(x, y, z, k.pick(FLOOR))
                else: s(x, y, z, k.pick(VOID) if (x + y + z) % 7 else 'deepslate_bricks')
        if walk(z - 1) == w - 1 and z > 90:
            for x in range(109, 116): s(x, w - 1, z, 'polished_blackstone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for z in range(92, 116, 4):                                   # ribs: pilasters and arches
        w = walk(z)
        for y in range(w, 33):
            s(109, y, z, 'polished_blackstone_bricks' if y % 6 else 'magma_block')
            s(115, y, z, 'polished_blackstone_bricks' if y % 6 else 'magma_block')
        for x in range(110, 115):
            for y in range(29, 33):
                if y >= 32 - min(abs(x - 112), 2) + (0 if abs(x - 112) < 2 else 0) or y == 32: s(x, y, z, 'polished_blackstone_bricks')
        s(110, w, z, CANDLE % 2); s(114, w, z, CANDLE % 2)
    n = 0
    for z2 in range(90, 116, 4):                                    # (the ribs stand at 92, 96 .. 112: the eyes between them)
        w = walk(z2)
        for (x, f) in ((109, 'east'), (115, 'west')):
            for h in (3, 6, 10):
                s(x, w + h, z2, 'air')
                B.eye(x, w + h, z2, f)
                n += 1
    for (x, z) in ((110, 93), (114, 97), (110, 101), (114, 105), (110, 109), (114, 113), (110, 113), (114, 91)):
        B.eyesp(x, walk(z), z)
    B.start(17, 112, 18, 114)
    B.goal(17, 112, 13, 91)
    B.pz(17, 'reach', 112, 22, 102)
    B.voice('eyes', 112, 18, 113, r=5)
    k.sign(112, 18, 115, 0, ['THE STAIR OF A', 'THOUSAND EYES', 'Move while', 'they sleep.'], color='red', wall=False) if False else None
    B.fx(112, 26, 102)
    B.gate(112, 13, 89, 'x', 17)


def lantern_maze(k):
    """THE LANTERN CRAWL (the Arachno-Lantern): a pitch-dark maze off the Hall's stair (north), no light at all"""
    B, s, rnd = k.B, k.s, random.Random(7712)
    y = 64
    NI, NJ, X0, Z0 = 12, 11, 95, 71
    k.fill(X0 - 3, y - 2, Z0 - 3, X0 + 3 * NI + 1, y + 4, Z0 + 3 * NJ + 1, [('blackstone', 3), ('polished_blackstone_bricks', 2), ('deepslate_tiles', 1)])
    seen, stack, open_ = {(0, 0)}, [(0, 0)], set()
    while stack:
        i, j = stack[-1]
        nb = [(i + a, j + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= i + a < NI and 0 <= j + b < NJ and (i + a, j + b) not in seen]
        if not nb: stack.pop(); continue
        n = rnd.choice(nb)
        open_.add(((i, j), n)); open_.add((n, (i, j)))
        seen.add(n); stack.append(n)
    for _ in range(10):                                           # a few loops, so it isn't a tree
        i, j = rnd.randrange(NI - 1), rnd.randrange(NJ)
        open_.add(((i, j), (i + 1, j))); open_.add(((i + 1, j), (i, j)))
    cell = lambda i, j: (X0 + 3 * i, Z0 + 3 * j)
    for i in range(NI):
        for j in range(NJ):
            x, z = cell(i, j)
            k.fill(x, y - 1, z, x + 1, y - 1, z + 1, [('polished_blackstone', 2), ('blackstone', 1)])
            k.air(x, y, z, x + 1, y + 2, z + 1)
            if ((i, j), (i + 1, j)) in open_: k.air(x + 2, y, z, x + 2, y + 2, z + 1); s(x + 2, y - 1, z, 'blackstone'); s(x + 2, y - 1, z + 1, 'blackstone')
            if ((i, j), (i, j + 1)) in open_: k.air(x, y, z + 2, x + 1, y + 2, z + 2); s(x, y - 1, z + 2, 'blackstone'); s(x + 1, y - 1, z + 2, 'blackstone')
    # the way in (from the south): the door in the stair's outer wall, a passage north to the maze's last row
    k.air(111, y, 104, 113, y + 2, 112)
    k.fill(111, y - 1, 104, 113, y - 1, 112, 'polished_blackstone')
    k.air(110, y, 103, 111, y + 2, 103)
    B.hidden('lantern', 112, y, 111, 'x', 1, 3, 'polished_blackstone_bricks', [('lantern', 112, y, 114)])
    k.sign(110, y + 1, 113, 'south', ['THE DARK HERE', 'WANTS A LIGHT', 'OF ITS OWN.', ''], color='yellow')
    hx, hz = cell(6, 5)
    s(hx, y - 1, hz, 'gilded_blackstone'); B.relic('lantern', hx, y, hz)
    B.chest(hx + 1, y, hz + 1, 'west', loot='bm:p2/under/hidden')
    B.mb(112, y + 1, Z0 + 3 * NJ // 2, ['bm.udark'], data={'r': Int(24)})
    for i in range(0, NI, 3):                                     # bones of the lost
        x, z = cell(i, (i * 7) % NJ)
        if B.b.get((x, y, z), '').endswith(':air') and (x, z) != (hx, hz): s(x, y, z, 'skeleton_skull[powered=false,rotation=3]')


# ===================================================================================================== finishing passes
def zones(k, reach=26):
    """a zone marker within `reach` of every floor a player can stand on (adventure mode inside) - but none within 36 of the
    Hidden Gate's outer face, so nobody in the approach cave counts as inside (the gate would open for them)"""
    from p2.verify import passable
    B = k.B
    gx, gy, gz = SEAM[0] + 1.5, SEAM[1] + 0.5, SEAM[2] + 0.5
    zs, idx = [], {}
    def near(p):
        bx, by, bz = p[0] // 24, p[1] // 24, p[2] // 24
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for q in idx.get((bx + a, by + b, bz + c), ()):
                        if (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2 + (q[2] - p[2]) ** 2 <= reach * reach: return True
        return False
    def add(p):
        zs.append(p); idx.setdefault((p[0] // 24, p[1] // 24, p[2] // 24), []).append(p); B.zone(*p)
    add((SEAM[0] - 34, SEAM[1], SEAM[2]))
    cells = sorted(c for c, st in B.b.items() if st.endswith(':air') and c not in B.outside and passable(B.b.get((c[0], c[1] + 1, c[2])) or 'minecraft:stone')
                   and not passable(B.b.get((c[0], c[1] - 1, c[2])) or 'minecraft:air'))
    for c in cells:
        if (c[0] - gx) ** 2 + (c[1] - gy) ** 2 + (c[2] - gz) ** 2 < 37 ** 2: continue
        if not near(c): add(c)
    return len(zs)


def tidy(k):
    """keep the gates' fill boxes clean (their open/close fills replace every crying obsidian/light in the box), and prove
    the lava can't go anywhere: every lava cell sits on lava or rock and has only lava or rock beside it"""
    from p2.config import OPEN_LIGHT, ADOOR_LIGHT, GATE_H, BIG_W, BIG_H
    from p2.verify import passable
    B = k.B
    bad = ('minecraft:crying_obsidian', OPEN_LIGHT, ADOOR_LIGHT)
    for (x, y, z, ax, n) in B.meta['gates']:
        for dx in (-1, 0, 1):
            for dy in range(GATE_H):
                for dz in (-1, 0, 1):
                    if (dz == 0 if ax == 'x' else dx == 0): continue
                    if B.b.get((x + dx, y + dy, z + dz)) in bad: B.set(x + dx, y + dy, z + dz, 'obsidian')
    for (x, y, z, ax) in B.meta['big']:
        for dx in range(-BIG_W, BIG_W + 1):
            for dy in range(BIG_H):
                for dz in range(-BIG_W, BIG_W + 1):
                    if (dz == 0 if ax == 'x' else dx == 0): continue
                    if B.b.get((x + dx, y + dy, z + dz)) in bad: B.set(x + dx, y + dy, z + dz, 'obsidian')
    loose = []
    for (x, y, z), st in list(B.b.items()):
        if st.endswith(':water') or st == 'minecraft:ice' or 'waterlogged=true' in st: loose.append(((x, y, z), st))
        if not st.startswith('minecraft:lava'): continue
        for q in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1), (x, y - 1, z)):
            n = B.b.get(q)
            if n is None: B.set(*q, 'blackstone')
            elif not n.startswith('minecraft:lava') and passable(n) is not False: loose.append((q, n))
    if loose: raise ValueError(f'undercrown: lava (or water/ice) loose at {loose[:6]}')


def build():
    B = U.UBuild(seed=29801)
    k = K(B)
    approach(k)
    hub(k)
    hub_features(k)
    tunnel(k)
    landings(k)
    floor_ring(k)
    secret_chain(k)
    frozen(k)
    hexed(k)
    drowned(k)
    forge(k)
    throne_room(k)
    antechamber(k)
    eye_stair(k)
    lantern_maze(k)
    stair_gates(k)
    zones(k)
    tidy(k)
    B.seal()
    return B
