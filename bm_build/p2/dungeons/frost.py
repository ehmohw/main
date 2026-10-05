"""THE FROSTBOUND SPIRE: an octagonal ice tower in frozen biomes, 44 x 58 x 44, ground level at y6.
F0 Hall of the Watch (trial spawners) -> open stair -> F1 Frost-Eyes (targets) -> G1 stairwell -> F2 Rime Archive
(keypad; four winter tallies) -> G2 stairwell -> F3 Thin Ice (sliding plate bridge) -> G3 stairwell -> roof stair-house
(spoils vault) -> battle door -> the Frozen Crown (roof arena, four sniper perches).
Secrets: Huntsman's Cache (F2 storeroom, button under a table)."""
from p2.kit import DBuild, is_solid
from nbt import Byte, Int
from p2.config import CODES

CX = CZ = 22
WALL = [('deepslate_tiles', 3), ('cracked_deepslate_tiles', 1), ('packed_ice', 2), ('polished_deepslate', 1)]
FLOORP = [('packed_ice', 3), ('deepslate_tiles', 2), ('polished_diorite', 1)]
STAIR = 'deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]'
FY = [6, 15, 24, 33, 42]       # floor levels F0..F3 and the roof
# F3 thin-ice bridge: plates x17..23 (c 0..6), z16..28 (r 0..12); safe path enters from the west and leaves east
PATH = [(0, 6), (1, 6), (1, 5), (1, 4), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 8), (5, 8), (5, 7), (5, 6), (6, 6)]


def inside(x, z, shrink=0):
    dx, dz = abs(x - CX), abs(z - CZ)
    r = 13 - shrink
    return dx <= r and dz <= r and dx + dz <= 19 - shrink


def build():
    B = DBuild('frost', 44, 58, 44, seed=7041)
    # ---------------- foundation + shell
    for x in range(44):
        for z in range(44):
            if not inside(x, z): continue
            for y in range(0, 6): B.set(x, y, z, B.pick([('stone_bricks', 2), ('packed_ice', 2), ('deepslate', 1)]))
            ring = not inside(x, z, 1)
            for y in range(6, 45):
                if ring: B.set(x, y, z, B.pick(WALL))
                elif y in FY: B.set(x, y, z, B.pick(FLOORP))
                else: B.set(x, y, z, 'air')
            if ring and (x + z) % 2 == 0: B.set(x, 45, z, B.pick(WALL))            # crenellations
    # arrow-slit windows
    for y0 in (10, 19, 28, 37):
        for x in range(44):
            for z in range(44):
                if inside(x, z) and not inside(x, z, 1) and (abs(x - CX) == 13 or abs(z - CZ) == 13) and (x + z) % 6 == 1:
                    B.set(x, y0, z, 'light_blue_stained_glass_pane[east=false,north=false,south=false,west=false,waterlogged=false]')
                    B.set(x, y0 + 1, z, 'light_blue_stained_glass_pane[east=false,north=false,south=false,west=false,waterlogged=false]')
    # ---------------- entrance (south) + porch
    for x in range(20, 25):
        for y in range(7, 11): B.set(x, y, 35, 'air')
    for x in range(19, 26):
        for z in range(36, 41): B.set(x, 5, z, B.pick([('snow_block', 2), ('stone_bricks', 1)]))
    for x in (19, 25):
        for y in range(6, 12): B.set(x, y, 36, 'deepslate_tile_wall')
    B.entrance(22, 6, 38)

    def stair(xc, f, z0=28):
        """3-wide stair rising north from floor FY[f] to FY[f+1]; solid underneath; slab holes for headroom."""
        y0 = FY[f]
        for i in range(1, 10):
            z = z0 - i + 1
            for x in range(xc - 1, xc + 2):
                for y in range(y0 + 1, y0 + i): B.set(x, y, z, 'polished_deepslate')
                B.set(x, y0 + i, z, STAIR if i < 9 else B.pick(FLOORP))
                for y in range(y0 + i + 1, y0 + i + 4): B.set(x, y, z, 'air')
        return y0

    def enclosure(xc, f):
        y0 = FY[f]
        for z in range(19, 30):
            for y in range(y0 + 1, FY[f + 1]):
                B.set(xc - 2, y, z, B.pick(WALL)); B.set(xc + 2, y, z, B.pick(WALL))
        for x in range(xc - 2, xc + 3):
            for y in range(y0 + 1, FY[f + 1]): B.set(x, y, 19, B.pick(WALL)); B.set(x, y, 29, B.pick(WALL))

    # ---------------- F0: Hall of the Watch (combat) + open stair to F1 (x13..15)
    stair(14, 0)
    B.trial_spawner(18, 7, 14, 'strays')
    B.trial_spawner(28, 7, 26, 'frozen')
    for (x, z) in [(10, 14), (34, 30), (30, 10), (12, 30)]:
        B.set(x, 7, z, 'powder_snow'); B.set(x + 1, 7, z, 'snow[layers=3]')
    for (x, z) in [(17, 10), (27, 10), (22, 30), (33, 18)]:
        B.set(x, 7, z, 'packed_ice'); B.set(x, 8, z, 'skeleton_skull[rotation=%d]' % B.rnd.randrange(16))
    for y in range(7, 15): B.set(CX, y, CZ, 'polished_deepslate')          # central pillar
    B.set(CX, 11, CZ - 1, 'soul_lantern[hanging=false,waterlogged=false]'); B.set(CX, 11, CZ + 1, 'soul_lantern[hanging=false,waterlogged=false]')
    B.fx(22, 9, 22); B.zone(22, 8, 22)

    # ---------------- F1: Frost-Eyes (targets). Stair S1 to F2 behind G1 (x29..31)
    enclosure(30, 1); stair(30, 1)
    B.gate(30, 16, 29, 'x', 1)
    for (x, y, z) in [(22, 20, 9), (9, 18, 22), (33, 21, 14), (16, 22, 35)]:   # 4th was (35,21,14): outside the wall (fixed 2.1)
        B.target(1, x, y, z)
    B.pz(1, 'targets', 22, 14, 22)
    B.set(20, 16, 30, 'barrel[facing=up,open=false]',
          {'id': 'minecraft:barrel', 'Items': [{'Slot': Byte(i), 'id': 'minecraft:snowball', 'count': Int(16)} for i in range(4)]})
    B.set(21, 16, 31, 'deepslate_tiles'); B.set(21, 17, 31, 'deepslate_tiles')
    B.sign(21, 17, 30, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['Strike all four', 'frost-eyes before', 'the cold takes', 'your hands.'], color='light_blue', glow=True)
    for (x, z) in [(12, 12), (32, 32), (12, 32)]:
        B.set(x, 16, z, 'snow[layers=2]')
    B.fx(22, 18, 22)

    # ---------------- F2: Rime Archive (keypad). Stair S2 to F3 behind G2 (x13..15)
    enclosure(14, 2); stair(14, 2)
    B.gate(14, 25, 29, 'x', 2)
    code = '7041'
    CODES.setdefault('frost', {})[2] = code
    # keypad on the north side of a built plaque wall at z=12, facing south
    for x in range(19, 26):
        for y in range(25, 31): B.set(x, y, 11, B.pick(WALL))
    B.keypad(2, 21, 29, 12, 'south', code)
    # four tallies in alcoves (each says which winter and its count)
    tallies = [((10, 26, 26), 'east', 'The first', 'winter: seven', 'stray-hunts.'),
               ((34, 27, 26), 'west', 'The second', 'winter: none', 'came home.'),
               ((26, 28, 12), 'south', 'The third', 'winter: four', 'hunters lost.'),
               ((18, 26, 33), 'north', 'The fourth', 'winter: one', 'oath kept.')]
    vec = {'east': (-1, 0), 'west': (1, 0), 'south': (0, -1), 'north': (0, 1)}
    for (x, y, z), f, a, b2, c in tallies:
        dx, dz = vec[f]
        B.set(x + dx, y, z + dz, 'packed_ice')
        B.sign(x, y, z, f'spruce_wall_sign[facing={f},waterlogged=false]', [a, b2, c, ''], color='light_blue', glow=True)
    B.sign(19, 28, 12, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Speak the four', 'winters of the', 'oath, in order.', ''], color='white', glow=True)
    # Huntsman's Cache: storeroom x26..32, z30..34 (south-east), secret door in its north wall, button under a table
    for x in range(25, 34):
        for z in range(29, 35):
            if not inside(x, z, 1): continue
            for y in range(25, 33): B.set(x, y, z, B.pick(WALL) if (x in (25, 33) or z in (29,)) else 'air')
    B.sdoor(28, 25, 29, 1)
    B.chest(30, 25, 32, 'north', loot='bm:p2/frost/hidden')
    B.set(31, 25, 32, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'LootTable': 'minecraft:chests/igloo_chest'})
    B.sign(29, 26, 33, 'spruce_wall_sign[facing=north,waterlogged=false]', ["Huntsman's", 'Cache', '', 'Keep it quiet.'], color='light_blue', glow=True)
    B.set(29, 26, 34, 'packed_ice')
    # the table (button underneath) in the main room
    B.set(18, 25, 22, 'spruce_fence'); B.set(20, 25, 22, 'spruce_fence')
    for x in (18, 19, 20): B.set(x, 26, 22, 'spruce_slab[type=bottom,waterlogged=false]')
    B.sbutton(19, 25, 22, 'spruce_button[face=ceiling,facing=north,powered=false]', 1)
    B.fx(22, 27, 22); B.zone(22, 26, 22)

    # ---------------- F3: Thin Ice (plate bridge between two halves). Stair S3 to roof behind G3 (x29..31)
    enclosure(30, 3); stair(30, 3, z0=27)     # 2.1: was z0=28 - step 6 sat under the roof floor at z23 (head bump)
    B.gate(30, 34, 29, 'x', 3)
    # walls split F3 into west (arrival from S2) and east (G3) halves except the bridge x17..23, z16..28
    for x in range(17, 24):
        for z in range(9, 36):
            if not inside(x, z, 1) or 16 <= z <= 28: continue
            for y in range(34, 42): B.set(x, y, z, B.pick(WALL))
    for x in range(17, 24):            # double floor under the bridge so F2 cannot read the tell blocks from below
        for z in range(16, 29): B.set(x, 31, z, B.pick(WALL))
    safe = set(PATH)
    for c in range(7):
        for r in range(13):
            x, z = 17 + c, 16 + r
            B.set(x, 33, z, 'packed_ice')
            B.plate(x, 34, z, (c, r) not in safe, plate='minecraft:polished_blackstone_pressure_plate', safe_under='minecraft:packed_ice')
            if (c, r) in safe: B.set(x, 42, z, 'sea_lantern')
    B.pz(3, 'path', 20, 32, 22)
    B.start(3, 14, 34, 17)
    B.goal(3, 26, 34, 22)
    B.sign(16, 35, 15, 'dark_oak_wall_sign[facing=west,waterlogged=false]', ['Thin ice. The', 'old lights above', 'mark where it', 'still holds.'], color='light_blue', glow=True)
    B.set(17, 35, 15, 'deepslate_tiles')
    B.fx(22, 36, 22)

    # ---------------- roof: stair-house x25..33, z14..23 (spoils vault) with the battle door in its south wall
    for x in range(25, 34):
        for z in range(14, 24):
            for y in range(43, 50):
                edge = x in (25, 33) or z in (14, 23)
                B.set(x, y, z, B.pick(WALL) if edge else 'air')
            B.set(x, 50, z, B.pick([('deepslate_tile_slab[type=bottom,waterlogged=false]', 1)]))
            if (x, z) not in [(xx, zz) for xx in range(29, 32) for zz in range(20, 23)]: B.set(x, 42, z, B.pick(FLOORP))
    B.vault(27, 43, 15, 'south', 'vkey_frost', 'bm:p2/frost/vault')
    B.set(31, 46, 15, 'soul_lantern[hanging=false,waterlogged=false]')
    B.gate(29, 43, 23, 'x', 0, big=True)
    B.altar(29, 43, 26)
    B.set(28, 43, 27, 'packed_ice'); B.set(30, 43, 27, 'packed_ice')
    B.arena(22, 43, 28)
    for (x, z) in [(13, 13), (31, 31), (13, 31), (16, 22)]:
        B.pillar(x, z, 43, 45, [('packed_ice', 2), ('polished_deepslate', 1)])
        B.perch(x + 0.0, 46, z)
    for (x, z) in [(18, 30), (26, 32), (14, 26), (20, 16)]: B.mspawn(x, 43, z)
    B.vault(16, 43, 33, 'north', 'bkey_frost', 'bm:p2/frost/victor')
    B.fx(22, 46, 28); B.zone(22, 44, 28)
    B.controller(22, 26, 22)
    return B
