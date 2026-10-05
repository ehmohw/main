"""THE HOLLOW THRONE (2.2): a black citadel on a floating rock in the crimson void of bm:hollow_throne, placed once by
command at data.HOLLOW_ORIGIN. 152 x 128 x 152. Mob griefing is switched off while anyone is in this dimension, so
the King's Wither form cannot break anything and the castle can be built from whatever looks right.

Levels (floor y / walk y): Undercroft 19/21 (lava lake at y20), L1 34/35, L2 48/49, L3 62/63.
  Arrival rock (the rift home) -> the broken bridge over the void -> gatehouse ->
  P1 THE SIEGE OF THE GATE (combat waves, north courtyard)            G1: the Ossuary door (west of the courtyard)
  -> stair down -> P2 THE CINDER CROSSING (parkour over the lava lake under the keep)   G2: foot of the keep stair
  -> stair up -> L1 P3 GALLERY OF SEALS (strike the five seals in the order the masters fell)   G3: east door
  -> east ward -> bridge -> P4 THE SHATTERED STAIR (cantilevered steps round the Spire of Ash, void below)
  -> balcony -> high bridge -> G4 -> L2 P5 THE KNIGHTS' VIGIL (combat waves)   G5: the stair to the throne
  -> L3 antechamber (spoils + victor vaults, rift home) -> battle door -> THE THRONE (arena: lava channels, pillars)
Floating islets ring the citadel, each with a dead tree, a chest of rare loot and a wayshrine back to the arrival
rock; only an elytra glide (from the bridges, balcony or towers) reaches them.
Secret: the Crown Room off the Gallery's west wall (a button low on the west wall, behind the first pillar)."""
import math
import random
from nbt import Int, Byte
from p2.kit import DBuild

SX, SY, SZ = 152, 128, 152
UF, L1, L2, L3 = 19, 34, 48, 62           # floor y of each level (walk = +1)
ROCK = [('blackstone', 5), ('basalt', 3), ('deepslate', 3), ('tuff', 1), ('cobbled_deepslate', 1)]
WALL = [('deepslate_bricks', 5), ('polished_blackstone_bricks', 4), ('deepslate_tiles', 2), ('cracked_deepslate_bricks', 1),
        ('cracked_polished_blackstone_bricks', 1)]
TRIM = [('polished_blackstone', 1)]
FLOOR = [('polished_deepslate', 3), ('deepslate_tiles', 2), ('polished_blackstone', 2), ('polished_blackstone_bricks', 1)]
ROOF = [('red_nether_bricks', 6), ('nether_wart_block', 2), ('red_terracotta', 1)]
GROUND = [('blackstone', 3), ('polished_blackstone', 2), ('tuff', 1), ('coarse_dirt', 1), ('soul_soil', 1)]
# P3: (order, x, y, z, wall-plane axis, frame) - the order the five masters fell
TARGETS = [(1, 64, 41, 60, 'z', 'white_wool'), (2, 98, 40, 82, 'x', 'packed_ice'), (3, 80, 43, 106, 'z', 'prismarine_bricks'),
           (4, 52, 42, 92, 'x', 'amethyst_block'), (5, 86, 39, 60, 'z', 'gilded_blackstone')]


def build():
    B = DBuild('hollow', SX, SY, SZ, seed=47193)
    B.meta['parkour'] = True                 # the verifier may jump 1-2 block gaps
    rnd = random.Random(2202)
    S = B.set

    def solid(x1, y1, z1, x2, y2, z2, pal):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1): S(x, y, z, B.pick(pal) if isinstance(pal, list) else pal)

    def air(x1, y1, z1, x2, y2, z2): solid(x1, y1, z1, x2, y2, z2, 'air')

    def rock_disc(cx, cz, r, top, depth, rough=1.5):
        """A floating rock: flat top at `top`, hanging cone below (deeper in the middle)."""
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            for z in range(int(cz - r - 2), int(cz + r + 3)):
                d = math.hypot(x - cx, z - cz) + rnd.uniform(-rough, rough) * 0.5
                if d > r or not (0 <= x < SX and 0 <= z < SZ): continue
                bottom = max(0, int(top - 2 - depth * (1 - d / (r + 0.5)) ** 0.8 - rnd.random() * 2))
                for y in range(bottom, top + 1): S(x, y, z, B.pick(ROCK))

    def tower(cx, cz, r, y1, y2, roof_h, wall=WALL, windows=True, glow='ochre_froglight'):
        """Round tower shell with lit slit windows and a red cone roof that overhangs by one."""
        for y in range(y1, y2 + 1):
            for x in range(cx - r, cx + r + 1):
                for z in range(cz - r, cz + r + 1):
                    d = math.hypot(x - cx, z - cz)
                    if r - 0.9 <= d <= r + 0.4:
                        win = windows and y > y1 + 4 and (y - y1) % 9 in (2, 3, 4) and (x == cx or z == cz)
                        S(x, y, z, glow if win else B.pick(wall))
        for x in range(cx - r - 1, cx + r + 2):                  # corbel ring + crenels
            for z in range(cz - r - 1, cz + r + 2):
                d = math.hypot(x - cx, z - cz)
                if r - 0.2 <= d <= r + 1.4:
                    S(x, y2 + 1, z, 'polished_blackstone_bricks')
                    if (x + z) % 2 == 0: S(x, y2 + 2, z, 'polished_blackstone_brick_wall')
        cone(cx, cz, r + 1, y2 + 2, roof_h)

    def cone(cx, cz, r, y0, h):
        for k in range(h):
            rr = (r + 0.5) * (1 - k / h)
            y = y0 + k
            for x in range(int(cx - rr - 1), int(cx + rr + 2)):
                for z in range(int(cz - rr - 1), int(cz + rr + 2)):
                    d = math.hypot(x - cx, z - cz)
                    if rr - 1.3 <= d <= rr and 0 <= y < SY:
                        S(x, y, z, B.pick(ROOF))
                        if rnd.random() < 0.08 and y + 1 < SY and B.get(x, y + 1, z) is None: S(x, y + 1, z, 'snow[layers=1]')
        top = y0 + h
        for y in range(top, min(top + 3, SY - 1)): S(cx, y, cz, 'iron_bars' if y < top + 2 else 'red_banner[rotation=4]')

    def pyramid(x1, z1, x2, z2, y0, mat=ROOF):
        k = 0
        while x1 + k <= x2 - k and z1 + k <= z2 - k and y0 + k < SY:
            for x in range(x1 + k, x2 - k + 1):
                for z in range(z1 + k, z2 - k + 1):
                    if x in (x1 + k, x2 - k) or z in (z1 + k, z2 - k): S(x, y0 + k, z, B.pick(mat))
            k += 1
        return y0 + k

    def dead_tree(x, y, z, h):
        """Scraggly dead spruce: crooked trunk, twig fences, a few rusty leaves."""
        cx, cz = x, z
        for k in range(h):
            S(cx, y + k, cz, 'spruce_log[axis=y]')
            if k > 2 and rnd.random() < 0.25:
                cx += rnd.choice((-1, 1)) if rnd.random() < 0.5 else 0
                S(cx, y + k, cz, 'spruce_log[axis=y]')
            if k >= 2 and k % 2 == 0:
                for _ in range(2):
                    dx, dz = rnd.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
                    for j in range(1, 2 + rnd.randrange(2)):
                        if B.get(cx + dx * j, y + k, cz + dz * j) is None: S(cx + dx * j, y + k, cz + dz * j, 'spruce_fence')
                    if rnd.random() < 0.4 and B.get(cx + dx * 2, y + k + 1, cz + dz * 2) is None:
                        S(cx + dx * 2, y + k + 1, cz + dz * 2, 'mangrove_leaves[distance=7,persistent=true,waterlogged=false]')
        S(cx, y + h, cz, 'spruce_fence'); S(cx, y + h + 1, cz, 'spruce_fence')

    def stair(xc, y0, z0, dz, n=14, mat='polished_deepslate', step='polished_blackstone_brick_stairs'):
        """3-wide stair rising one block per step along +z (dz=1) or -z (dz=-1); solid underneath, 3 air above."""
        face = 'south' if dz > 0 else 'north'
        for i in range(1, n + 1):
            z = z0 + dz * (i - 1)
            for x in range(xc - 1, xc + 2):
                for y in range(y0 + 1, y0 + i): S(x, y, z, mat)
                S(x, y0 + i, z, f'{step}[facing={face},half=bottom,shape=straight,waterlogged=false]' if i < n else B.pick(FLOOR))
                for y in range(y0 + i + 1, y0 + i + 4): S(x, y, z, 'air')

    def lit_window(x, y, z, h=4, mat='orange_stained_glass'):
        for k in range(h): S(x, y + k, z, mat)

    # ================================================================ the floating rock + curtain + courtyard
    rock_disc(75, 75, 44, L1 - 1, 30, rough=3)
    for x in range(36, 115):                                  # courtyard / ward ground
        for z in range(36, 115):
            S(x, L1, z, B.pick(GROUND))
            if rnd.random() < 0.05: S(x, L1 + 1, z, 'snow[layers=1]')
    # curtain wall (y35..46, crenels at 47), buttressed outside
    for i in range(35, 116):
        for (x, z) in ((i, 35), (i, 115), (35, i), (115, i)):
            for y in range(L1 - 2, 47): S(x, y, z, B.pick(WALL))
            if i % 2 == 0: S(x, 47, z, 'polished_blackstone_bricks')
            if i % 8 == 3:
                ox, oz = (0, -1) if z == 35 else (0, 1) if z == 115 else (-1, 0) if x == 35 else (1, 0)
                for y in range(L1 - 6, 44): S(x + ox, y, z + oz, 'polished_blackstone_bricks')
                S(x + ox, 44, z + oz, 'polished_blackstone_brick_wall')
    for (x1, x2) in ((36, 51), (99, 114)):                    # inner walls: the courtyard is cut off from the other wards
        for x in range(x1, x2 + 1):
            for y in range(L1 + 1, 47): S(x, y, 59, B.pick(WALL))
    for (cx, cz) in ((35, 35), (115, 35), (35, 115), (115, 115)):
        rock_disc(cx, cz, 7, L1 - 1, 18)
        tower(cx, cz, 5, L1 - 3, 62, 15)
    # gatehouse: arch x73..77, flanking towers
    air(73, L1 + 1, 35, 77, L1 + 5, 35)
    for x in range(72, 79): S(x, L1 + 6, 35, 'chiseled_polished_blackstone' if x == 75 else 'polished_blackstone_bricks')
    for x in range(73, 78): S(x, L1 + 5, 35, 'iron_bars')   # portcullis teeth
    for cx in (69, 81):
        tower(cx, 35, 3, L1 - 2, 56, 11)
    # ================================================================ arrival rock + the broken bridge (void below)
    rock_disc(75, 12, 9, L1, 16)
    for x in range(70, 81):
        for z in range(6, 19):
            if B.get(x, L1, z): S(x, L1, z, 'polished_blackstone' if abs(x - 75) <= 1 else B.pick(FLOOR))
    for (ox, oz) in ((-6, -4), (6, -4), (-6, 4), (6, 4)):
        for y in range(L1 + 1, L1 + 7): S(75 + ox, y, 12 + oz, 'polished_blackstone_bricks')
        S(75 + ox, L1 + 7, 12 + oz, 'soul_soil'); S(75 + ox, L1 + 8, 12 + oz, 'soul_fire')
    S(75, L1, 6, 'crying_obsidian'); B.mb(75, L1 + 1, 6, ['bm.rift'])
    B.mb(75, L1 + 1, 14, ['bm.isle_home'])
    B.entrance(75, L1 + 1, 16)
    B.sign(77, L1 + 1, 16, 'dark_oak_sign[rotation=8,waterlogged=false]', ['The rift behind', 'you leads home.', 'The King waits', 'beyond the gap.'], color='red', glow=True)
    for z in range(19, 35):
        if z in (25, 26, 30): continue                      # the gaps: jump, or fall forever
        for x in range(73, 78): S(x, L1, z, B.pick(FLOOR)); S(x, L1 - 1, z, B.pick(WALL))
        if z % 3: S(72, L1 + 1, z, 'polished_blackstone_wall')
        if z % 4 != 1: S(78, L1 + 1, z, 'polished_blackstone_wall')
        if z % 5 == 0:
            for k in range(2, 6 + z % 3): S(75, L1 - k, z, 'polished_blackstone_wall')
    B.fx(75, L1 + 4, 24)

    # ================================================================ P1 THE SIEGE OF THE GATE (courtyard waves)
    for (x, z) in ((44, 38), (106, 42), (58, 52), (92, 52), (66, 41), (84, 44)):
        dead_tree(x, L1 + 1, z, 7 + rnd.randrange(4))
    for (x, z) in ((54, 45), (96, 45), (75, 50)):              # lava braziers
        S(x, L1 + 1, z, 'polished_blackstone_bricks'); S(x, L1 + 2, z, 'lava_cauldron')
    B.pz(1, 'waves', 75, L1 + 1, 47)
    for (x, z) in ((46, 39), (104, 39), (48, 55), (102, 55), (75, 57), (62, 38), (88, 38)):
        B.el(1, 'wsp', x, L1 + 1, z)
    B.fx(75, L1 + 6, 47); B.zone(75, L1 + 2, 47)
    # the Ossuary (G1) - its stair dives under the courtyard to the undercroft
    for x in range(40, 49):
        for z in range(42, 55):
            edge = x in (40, 48) or z in (42, 54)
            for y in range(L1 + 1, L1 + 8): S(x, y, z, B.pick(WALL) if edge else 'air')
            S(x, L1, z, B.pick(FLOOR))
    pyramid(39, 41, 49, 55, L1 + 8)
    B.gate(48, L1 + 1, 47, 'z', 1)
    for z in (44, 50):
        S(47, L1 + 1, z, 'polished_blackstone_bricks'); S(47, L1 + 2, z, 'wither_skeleton_skull[powered=false,rotation=4]')
    stair(43, UF + 1, 62, -1, mat='blackstone')              # bottom step z62 (walk 22) .. landing z49 (floor 34)
    for z in range(50, 55):                                    # rails round the stairwell mouth
        for x in (41, 45): S(x, L1 + 1, z, 'polished_blackstone_wall')
    for x in range(42, 51):                                    # landing + corridor east to the undercroft
        for z in range(63, 66):
            S(x, UF + 1, z, B.pick(FLOOR)); air(x, UF + 2, z, x, UF + 4, z)

    # ================================================================ P2 THE CINDER CROSSING (undercroft lava lake)
    for x in range(50, 101):
        for z in range(58, 109):
            S(x, UF, z, 'blackstone'); S(x, UF + 1, z, 'lava')
            for y in range(UF + 2, L1 - 1): S(x, y, z, 'air')
            S(x, L1 - 1, z, B.pick(ROCK))
    for x in range(50, 58):                                    # start ledge (NW)
        for z in range(59, 66): S(x, UF + 1, z, B.pick(FLOOR))
    air(50, UF + 2, 62, 50, UF + 4, 64)
    for x in range(91, 100):                                   # goal ledge (SE)
        for z in range(102, 108): S(x, UF + 1, z, B.pick(FLOOR))
    # stepping pillars: each move is a straight jump over 1-2 cells of lava, sometimes up or down a block
    path = [(60, 62, 0), (63, 62, 0), (63, 64, 1), (63, 67, 1), (66, 67, 1), (66, 70, 0), (69, 70, 0), (69, 73, 0), (69, 75, 1),
            (72, 75, 1), (75, 75, 1), (75, 78, 0), (75, 81, 0)]
    rest = (78, 81)                                            # a 3x3 rest island with the archers' spawner
    path2 = [(82, 82, 0), (85, 82, 0), (85, 85, 0), (85, 87, 1), (85, 90, 1), (88, 90, 1), (88, 93, 0), (88, 96, 0), (91, 96, 0),
             (91, 99, 0)]
    for (x, z, up) in path + path2:
        top = UF + 1 + up
        for y in range(UF + 1, top + 1): S(x, y, z, 'basalt[axis=y]')
        S(x, top, z, 'polished_basalt[axis=y]' if (x + z) % 3 else 'polished_blackstone')
    for x in range(rest[0] - 1, rest[0] + 2):
        for z in range(rest[1] - 1, rest[1] + 2): S(x, UF + 1, z, 'polished_blackstone')
    B.trial_spawner(rest[0], UF + 2, rest[1] + 1, 'archers')
    for (x, z) in ((56, 80), (60, 96), (80, 66), (96, 70), (70, 100), (82, 92), (64, 86)):    # crumbling stalagmites
        for y in range(UF + 1, UF + 3 + (x * z) % 5): S(x, y, z, 'basalt[axis=y]')
    for x in range(52, 100, 6):                                # dripping ceiling teeth
        for z in range(60, 107, 6):
            for k in range(1 + (x + z) % 4): S(x, L1 - 2 - k, z, 'pointed_dripstone[thickness=tip,vertical_direction=down,waterlogged=false]' if k == (x + z) % 4 else 'basalt[axis=y]')
    B.start(2, 54, UF + 2, 62)
    B.goal(2, 95, UF + 2, 104)
    B.sign(56, UF + 3, 59, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['THE CINDER', 'CROSSING', 'Leap, or burn.', ''], color='red', glow=True)
    S(56, UF + 3, 58, 'polished_blackstone_bricks')
    B.pz(2, 'reach', 75, UF + 6, 83)
    B.fx(75, UF + 6, 83); B.zone(75, UF + 3, 83)
    # ================================================================ THE KEEP (x52..98, z60..106), three halls
    for y in range(L1, 88):
        for x in range(52, 99):
            for z in range(60, 107):
                edge = x in (52, 98) or z in (60, 106)
                if edge: S(x, y, z, B.pick(WALL))
                elif y in (L1, L2, L2 - 1, L3, L3 - 1, 87): S(x, y, z, B.pick(FLOOR) if y in (L1, L2, L3) else B.pick(WALL))
                else: S(x, y, z, 'air')
    for x in range(52, 99, 6):                                 # buttresses + lit windows
        for z in (59, 107):
            for y in range(L1 - 4, 84): S(x, y, z, 'polished_blackstone_bricks')
            S(x, 84, z, 'polished_blackstone_brick_wall')
    for z in range(60, 107, 6):
        for x in (51, 99):
            if not (x == 99 and z in (72, 84)):                # leave room for the east doors' landings
                for y in range(L1 - 4, 84): S(x, y, z, 'polished_blackstone_bricks')
    for x in range(55, 97, 6):
        for z in (60, 106):
            lit_window(x, L1 + 4, z, 5); lit_window(x, L2 + 4, z, 5)
            lit_window(x, L3 + 5, z, 12, 'red_stained_glass')
    # roof: steep red hip roof + crenellated parapet, four turrets, the Great Spire
    for x in range(51, 100):
        for z in (59, 107):
            S(x, 88, z, 'polished_blackstone_bricks')
            if x % 2 == 0: S(x, 89, z, 'polished_blackstone_brick_wall')
    for k in range(12):
        y = 88 + k
        for z in range(60, 107):
            for x in (52 + 2 * k, 53 + 2 * k, 97 - 2 * k, 98 - 2 * k): S(x, y, z, B.pick(ROOF))
        for x in range(52 + 2 * k, 99 - 2 * k):
            for z in (60, 106): S(x, y, z, B.pick(ROOF))
        for z in range(60, 107):
            if rnd.random() < 0.06: S(52 + 2 * k, y + 1, z, 'snow[layers=1]')
    for (cx, cz) in ((52, 60), (98, 60), (52, 106), (98, 106)):
        tower(cx, cz, 3, L1 - 4, 96, 10)
    for y in range(95, 114):                                   # the Great Spire, rising through the ridge
        for x in range(70, 81):
            for z in range(78, 89):
                if x in (70, 80) or z in (78, 88):
                    win = (y % 7 in (2, 3, 4)) and (x in (75,) or z in (83,))
                    S(x, y, z, 'ochre_froglight' if win else B.pick(WALL))
    for (x, z) in ((70, 78), (80, 78), (70, 88), (80, 88)):
        for y in range(108, 118): S(x, y, z, 'polished_blackstone_bricks')
        S(x, 118, z, 'polished_blackstone_brick_wall')
    pyramid(69, 77, 81, 89, 114)
    for y in range(120, 124): S(75, y, 83, 'iron_bars')
    S(75, 124, 83, 'red_banner[rotation=0]')

    # G2 + the keep stair (x94..96, z100 -> z87) in a walled shaft through the lake
    for z in range(86, 102):
        for x in range(93, 98):
            for y in range(UF, L1):
                if x in (93, 97) or z in (86, 101): S(x, y, z, B.pick(WALL))
                elif y > UF: S(x, y, z, 'air')
    stair(95, UF + 1, 100, -1)
    B.gate(95, UF + 2, 101, 'x', 2)

    # ---------------- L1 GALLERY OF SEALS (P3: ordered targets)
    for x in range(53, 98):                                    # red runner + columns + chandeliers
        S(x, L1 + 1, 83, 'red_carpet') if 56 <= x <= 92 else None
    for (x, z) in ((60, 70), (60, 96), (90, 70), (90, 96), (75, 66), (75, 100)):
        solid(x - 1, L1 + 1, z - 1, x, L2 - 2, z, WALL)
        S(x - 1, L1 + 6, z + 1, 'red_wall_banner[facing=south]'); S(x, L1 + 6, z - 2, 'red_wall_banner[facing=north]')
    for (x, z) in ((67, 76), (83, 76), (67, 90), (83, 90)):
        for y in range(L1 + 8, L2 - 1): S(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        S(x, L1 + 7, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for (x, z) in ((56, 64), (56, 102), (94, 64)):
        S(x, L1 + 1, z, 'polished_blackstone_bricks'); S(x, L1 + 2, z, 'lava_cauldron')
    for (order, x, y, z, ax, frame) in TARGETS:
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                fx, fz = (x + a, z) if ax == 'z' else (x, z + a)
                S(fx, y + b, fz, frame)
        B.target(3, x, y, z, order)
        ox, oz = {(60, 'z'): (0, -1), (106, 'z'): (0, 1)}.get((z, ax), (-1, 0) if x == 52 else (1, 0)) if ax == 'z' or x in (52, 98) else (0, 0)
        for a in (-1, 0, 1):                                   # backing outside the keep: a seal can't be shot from the yard
            for b in (-1, 0, 1):
                fx, fz = (x + a, z) if ax == 'z' else (x, z + a)
                S(fx + ox, y + b, fz + oz, 'polished_blackstone_bricks')
    for z in range(88, 102):                                   # rails round the stair from the undercroft
        for x in (93, 97): S(x, L1 + 1, z, 'polished_blackstone_wall')
    for x in range(93, 98): S(x, L1 + 1, 101, 'polished_blackstone_wall')
    for z in (84, 85):
        S(91, L1 + 1, z, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'Items': [
            {'Slot': Byte(i), 'id': 'minecraft:snowball', 'count': Int(16)} for i in range(6)]})
    B.sign(90, L1 + 1, 86, 'dark_oak_sign[rotation=4,waterlogged=false]', ['Strike the seals', 'in the order', 'their masters', 'fell.'], color='gray', glow=True)
    B.pz(3, 'targets', 75, L1 + 4, 83)
    B.trial_spawner(60, L1 + 1, 83, 'knights')
    B.trial_spawner(86, L1 + 1, 66, 'knights')
    B.fx(75, L1 + 6, 83); B.zone(75, L1 + 2, 83)
    # Crown Room (secret) in the west ward; the button hides low on the west wall behind the first column
    for x in range(40, 52):
        for z in range(72, 83):
            edge = x == 40 or z in (72, 82)
            S(x, L1, z, B.pick(WALL) if edge else 'polished_blackstone')
            for y in range(L1 + 1, L1 + 6): S(x, y, z, B.pick(WALL) if edge else 'air')
            S(x, L1 + 6, z, B.pick(WALL))
    B.sbutton(53, L1 + 1, 69, 'polished_blackstone_button[face=wall,facing=east,powered=false]', 1)
    B.sdoor(52, L1 + 1, 77, 1)
    B.chest(43, L1 + 1, 77, 'east', loot='bm:p2/hollow/hidden')
    for z in (75, 79): S(43, L1 + 1, z, 'polished_blackstone_bricks'); S(43, L1 + 2, z, 'wither_skeleton_skull[powered=false,rotation=12]')
    B.lectern(46, L1 + 1, 73, 'south', 'The Empty Crown', 'Wilfrey', [
        "Grandfather made two crowns. One he wears. The other he hid here, for an heir worthy of the Throne.",
        "If you are reading this, you are already braver than any of us. Take it. Wear it into his hall."])
    S(46, L1 + 4, 77, 'soul_lantern[hanging=true,waterlogged=false]'); S(46, L1 + 5, 77, 'iron_chain[axis=y,waterlogged=false]')

    # ================================================================ G3 -> east ward -> P4 THE SHATTERED STAIR (Spire of Ash)
    B.gate(98, L1 + 1, 72, 'z', 3)
    air(115, L1 + 1, 77, 115, L1 + 4, 79)                      # postern in the east curtain
    for x in range(116, 119):                                  # short bridge over the void
        for z in range(77, 80): S(x, L1, z, B.pick(FLOOR)); S(x, L1 - 1, z, B.pick(WALL))
    rock_disc(130, 74, 8, L1 - 1, 22, rough=2)                 # the pinnacle (its top stays under the stair line)
    for x in range(119, 125):                                  # base ledge (SW of the spire)
        for z in range(78, 83): S(x, L1, z, B.pick(FLOOR))
    for x in range(124, 137):                                  # clear the pinnacle top round the spire: void under the steps
        for z in range(66, 79):
            if not (126 <= x <= 134 and 68 <= z <= 76) and (x, z) != (124, 78):
                for y in range(L1 - 12, L1 + 1):
                    if B.get(x, y, z): S(x, y, z, 'air')
    for y in range(L1 - 12, 76):                               # the spire (square, x126..134, z68..76)
        for x in range(126, 135):
            for z in range(68, 77):
                if x in (126, 134) or z in (68, 76):
                    win = y > L1 + 2 and y % 6 in (1, 2, 3) and (x == 130 or z == 72)
                    S(x, y, z, 'ochre_froglight' if win else B.pick(WALL))
    pyramid(125, 67, 135, 77, 76)
    # steps one gap out from the spire (lines x124 / z66 / x136), one every 2 cells, each a block higher
    peri = [(124, z) for z in range(78, 66, -1)] + [(x, 66) for x in range(124, 136)] + [(136, z) for z in range(66, 79)]
    for k in range(1, 14):
        x, z = peri[2 * k]
        top = L1 + k
        S(x, top, z, 'polished_blackstone_brick_slab[type=top,waterlogged=false]' if k % 4 == 2 else 'polished_blackstone_bricks')
        S(x, top - 1, z, 'polished_blackstone_brick_wall')
        air(x, top + 1, z, x, top + 3, z)
    for x in range(125, 136):                                  # balcony ring at L2 (1 wide), broken parapet
        for z in range(67, 78):
            if x in (125, 135) or z in (67, 77):
                S(x, L2, z, B.pick(FLOOR))
    B.start(4, 121, L1 + 1, 80)
    B.goal(4, 135, L2 + 1, 70)
    B.sign(121, L1 + 1, 82, 'dark_oak_sign[rotation=8,waterlogged=false]', ['THE SHATTERED', 'STAIR', 'Climb. Do not', 'look down.'], color='red', glow=True)
    B.pz(4, 'reach', 130, L1 + 6, 74)
    B.fx(130, L1 + 8, 74)
    # the high bridge from the balcony back to the keep at L2 (over the void, then the curtain, then the east ward)
    for x in range(99, 125):
        for z in range(71, 74):
            S(x, L2, z, B.pick(FLOOR))
        if x % 3: S(x, L2 + 1, 70, 'polished_blackstone_wall')
        if x % 4 != 1: S(x, L2 + 1, 74, 'polished_blackstone_wall')
        if x % 6 == 0:
            for k in range(1, 4): S(x, L2 - k, 72, 'polished_blackstone_wall')
    B.gate(98, L2 + 1, 72, 'z', 4)

    # ================================================================ L2 P5 THE KNIGHTS' VIGIL (waves)
    for (x, z) in ((62, 68), (62, 98), (88, 68), (88, 98)):
        solid(x - 1, L2 + 1, z - 1, x, L3 - 2, z, WALL)
        S(x, L2 + 5, z + 1, 'red_wall_banner[facing=south]'); S(x - 1, L2 + 5, z - 2, 'red_wall_banner[facing=north]')
    for (x, z) in ((70, 74), (80, 74), (70, 92), (80, 92)):
        for y in range(L2 + 8, L3 - 2): S(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        S(x, L2 + 7, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for x in range(60, 96): S(x, L2 + 1, 83, 'red_carpet')
    for (x, z) in ((94, 64), (94, 102), (66, 64), (66, 102)):
        S(x, L2 + 1, z, 'polished_blackstone_bricks'); S(x, L2 + 2, z, 'lava_cauldron')
    B.pz(5, 'waves', 76, L2 + 1, 83)
    for (x, z) in ((64, 64), (90, 64), (64, 102), (90, 102), (76, 70), (76, 96)):
        B.el(5, 'wsp', x, L2 + 1, z)
    B.fx(76, L2 + 6, 83); B.zone(76, L2 + 2, 83)
    # G5 + the stair to the throne (x54..56, z72 -> z85), walled off from the hall
    for z in range(70, 87):
        for y in range(L2 + 1, L3 - 1): S(57, y, z, B.pick(WALL))
    for x in range(53, 58):
        for y in range(L2 + 1, L3 - 1): S(x, y, 70, B.pick(WALL)); S(x, y, 87, B.pick(WALL))
    stair(55, L2, 72, 1)
    B.gate(55, L2 + 1, 70, 'x', 5)
    for z in range(77, 85): S(57, L3 + 1, z, 'polished_blackstone_wall'); S(53, L3 + 1, z, 'polished_blackstone_wall')
    for x in range(53, 58): S(x, L3 + 1, 76, 'polished_blackstone_wall')

    # ================================================================ L3 antechamber -> THE THRONE (arena)
    for z in range(61, 106):
        for y in range(L3 + 1, 87): S(64, y, z, B.pick(WALL))
    B.vault(53, L3 + 1, 95, 'east', 'vkey_hollow', 'bm:p2/hollow/vault')
    B.vault(53, L3 + 1, 99, 'east', 'bkey_hollow', 'bm:p2/hollow/victor')
    for z in (93, 97, 101): S(53, L3 + 1, z, 'polished_blackstone_bricks'); S(53, L3 + 2, z, 'soul_lantern[hanging=false,waterlogged=false]')
    S(59, L3, 103, 'crying_obsidian'); B.mb(59, L3 + 1, 103, ['bm.rift'])
    B.sign(60, L3 + 1, 65, 'dark_oak_sign[rotation=0,waterlogged=false]', ['THE THRONE', 'Kneel at the', 'altar. He will', 'answer.'], color='red', glow=True)
    B.zone(59, L3 + 2, 90)
    B.gate(64, L3 + 1, 83, 'z', 0, big=True)
    # the throne room: lava channels (bridged), two rows of great columns, chandeliers, the dais
    for z in range(63, 104):
        for x in (77, 89):
            if z % 7 != 6: S(x, L3, z, 'lava')
    for (x, z) in ((71, 68), (71, 98), (83, 68), (83, 98), (95, 68), (95, 98)):
        solid(x - 1, L3 + 1, z - 1, x + 1, 86, z + 1, WALL)
        S(x, L3 + 8, z + 2, 'red_wall_banner[facing=south]'); S(x, L3 + 8, z - 2, 'red_wall_banner[facing=north]')
    for (x, z) in ((74, 76), (74, 90), (86, 76), (86, 90)):
        for y in range(L3 + 12, 87): S(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        S(x, L3 + 11, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for x in range(66, 97, 5):
        for z in range(63, 104, 5):
            for y, lv in ((84, 12), (L3 + 4, 8)):
                if B.get(x, y, z) == 'minecraft:air': S(x, y, z, f'light[level={lv},waterlogged=false]')
    for x in range(92, 98):                                    # the throne dais
        for z in range(77, 90): S(x, L3 + 1, z, 'polished_blackstone_bricks')
    for z in range(78, 89): S(91, L3 + 1, z, 'polished_blackstone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
    S(95, L3 + 2, 83, 'blackstone_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]')
    for z in (82, 84): S(95, L3 + 2, z, 'polished_blackstone_wall')
    for z in (81, 82, 83, 84, 85):
        for y in range(L3 + 2, L3 + 12): S(97, y, z, 'gilded_blackstone' if z == 83 and y < L3 + 9 else 'polished_blackstone_bricks')
    S(97, L3 + 12, 83, 'wither_skeleton_skull[powered=false,rotation=4]')
    for z in (79, 87): S(94, L3 + 2, z, 'lava_cauldron')
    for z in (80, 86): S(96, L3 + 7, z, 'red_wall_banner[facing=west]')
    B.arena(80, L3 + 1, 83)
    for (x, z) in ((67, 65), (67, 101), (93, 65), (93, 101), (80, 64), (80, 102), (86, 83)):
        B.mspawn(x, L3 + 1, z)
    B.fx(80, L3 + 8, 83); B.zone(80, L3 + 2, 83)
    # ---------------- the summoning altar: a stepped black dais, four soul-fire obelisks, skulls, lava braziers
    ax, az = 70, 83
    for dx in range(-3, 4):
        for dz in range(-3, 4):
            r = max(abs(dx), abs(dz))
            S(ax + dx, L3, az + dz, 'crying_obsidian' if r == 0 else 'polished_blackstone' if r == 1 else
              'chiseled_polished_blackstone' if r == 2 and (dx == 0 or dz == 0) else 'polished_blackstone_bricks')
    for dx, dz in ((-3, -3), (3, -3), (-3, 3), (3, 3)):
        for y in range(L3 + 1, L3 + 5): S(ax + dx, y, az + dz, 'polished_blackstone_bricks' if y < L3 + 4 else 'chiseled_polished_blackstone')
        S(ax + dx, L3 + 5, az + dz, 'soul_soil'); S(ax + dx, L3 + 6, az + dz, 'soul_fire')
    for dx, dz in ((3, 0), (0, -3), (0, 3)):
        S(ax + dx, L3 + 1, az + dz, 'wither_skeleton_skull[powered=false,rotation=%d]' % {(3, 0): 4, (0, -3): 8, (0, 3): 0}[(dx, dz)])
    for dx, dz in ((-2, -3), (2, -3), (-2, 3), (2, 3)): S(ax + dx, L3 + 1, az + dz, 'lava_cauldron')
    for y in range(L3 + 7, 87): S(ax, y, az, 'iron_chain[axis=y,waterlogged=false]')
    S(ax, L3 + 6, az, 'soul_lantern[hanging=true,waterlogged=false]')
    B.altar(ax, L3 + 1, az)

    # ================================================================ floating islets (elytra only)
    for (cx, y, cz, r) in ((10, 30, 66, 5), (14, 26, 14, 4), (62, 24, 140, 5), (138, 28, 136, 4), (140, 32, 18, 5)):
        rock_disc(cx, cz, r, y, 10 + r)
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                if B.get(x, y, z) and rnd.random() < 0.18: S(x, y + 1, z, 'snow[layers=1]')
        dead_tree(cx - 2, y + 1, cz - 1, 6 + r % 3)
        B.chest(cx + 1, y + 1, cz + 1, 'north', loot='bm:p2/hollow/isle')
        S(cx + 2, y, cz - 2, 'crying_obsidian'); S(cx + 2, y + 1, cz - 2, 'air')
        B.mb(cx + 2, y + 1, cz - 2, ['bm.isle_ret'])
        S(cx + 3, y + 1, cz - 2, 'soul_lantern[hanging=false,waterlogged=false]') if B.get(cx + 3, y, cz - 2) else None
    B.controller(75, 50, 83)
    return B
