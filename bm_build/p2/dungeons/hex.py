"""THE HEXBOUND CATHEDRAL: a drowned-in-moss gothic cathedral in swamps, 48 x 46 x 80, ground at y5.
Nave split by rood screens (each holds a gate):
  A  Narthex & nave (trial spawners) + east Chapel of Candles: P1 Lights Out (3x3 copper candles)
  G1 -> B  Library: P2 combat waves (the Choir Militant: vindicators, pillagers, witches, an evoker)
  G2 -> C  Choir: P3 rune circle; press the runes in the rose window's clockwise order
  G3 -> D  Antechamber (spoils vault) -> battle door -> the Apse (arena, five blink pedestals)
Secret: the Forbidden Archive behind the west wall (a wooden button hidden among the bookshelves)."""
from p2.kit import DBuild
from p2.config import CODES, SEQS

WALL = [('deepslate_bricks', 4), ('cracked_deepslate_bricks', 1), ('polished_deepslate', 1), ('mossy_stone_bricks', 0.5)]
TRIM = [('polished_blackstone_bricks', 1)]
FLOOR = [('polished_deepslate', 2), ('deepslate_tiles', 2), ('polished_blackstone', 1)]
X1, X2 = 14, 34          # nave interior x range
SCREENS = {1: 23, 2: 39, 3: 53}
GY = 6                   # walkable air starts at y6 (floor y5)
ROSE = ['purple', 'red', 'lime', 'orange', 'blue', 'yellow']     # clockwise from the top = the order to press


def build():
    B = DBuild('hex', 48, 46, 80, seed=8345)
    # ---------------- foundation + shell (walls y5..24, floor y5)
    for x in range(10, 39):
        for z in range(3, 79):
            for y in range(0, 5): B.set(x, y, z, B.pick([('cobbled_deepslate', 2), ('mud_bricks', 1)]))
    for x in range(X1 - 1, X2 + 2):
        for z in range(5, 58):
            edge = x in (X1 - 1, X2 + 1) or z == 5
            for y in range(5, 25):
                B.set(x, y, z, B.pick(WALL) if (edge or y == 5) else 'air')
            B.set(x, 5, z, B.pick(FLOOR) if not edge else B.pick(WALL))
    # vaulted ceiling + gable roof
    for x in range(X1 - 1, X2 + 2):
        for z in range(5, 58):
            off = abs(x - 24)
            for y in range(25, 25 + max(1, 12 - off)):
                B.set(x, y, z, B.pick([('deepslate_tiles', 3), ('deepslate_tile_slab[type=bottom,waterlogged=false]', 0)]))
    # buttresses and tall pointed windows
    for z in range(8, 57, 5):
        for (bx, wx) in ((X1 - 2, X1 - 1), (X2 + 2, X2 + 1)):
            for y in range(5, 20): B.set(bx, y, z, B.pick(TRIM))
            for y in range(10, 19):
                for dz in (2, 3): B.set(wx, y, z + dz, 'purple_stained_glass_pane[east=false,north=false,south=false,west=false,waterlogged=false]')
    # facade + doors + bell tower (spire)
    for x in range(20, 29):
        B.set(x, 5, 4, B.pick(FLOOR))
    for x in range(22, 27):
        for y in range(6, 11): B.set(x, y, 5, 'air')
    B.entrance(24, GY, 4)
    for (x, z) in [(19, 0), (29, 0), (19, 4), (29, 4)]:        # porch pillars carrying the bell tower
        for y in range(5, 25): B.set(x, y, z, B.pick(TRIM))
    for x in range(19, 30):
        for z in range(0, 5):
            for y in range(25, 40):
                edge = x in (19, 29) or z in (0, 4)
                if edge: B.set(x, y, z, B.pick(WALL))
    for i, y in enumerate(range(40, 46)):
        for x in range(20 + i, 29 - i):
            for z in range(0 + min(i, 2), 5 - min(i, 2)):
                if x in (20 + i, 28 - i) or z in (min(i, 2), 4 - min(i, 2)): B.set(x, y, z, 'deepslate_tiles')
    B.set(24, 33, 2, 'bell[attachment=ceiling,facing=north,powered=false]'); B.set(24, 34, 2, 'deepslate_tiles')

    def screen(z, n):
        for x in range(X1, X2 + 1):
            for y in range(6, 25): B.set(x, y, z, B.pick(TRIM) if y in (6, 24) else B.pick(WALL))
        B.gate(24, GY, z, 'x', n)

    # ---------------- A: narthex + nave (combat), pews, east chapel (P1), west hidden archive
    B.trial_spawner(18, GY, 14, 'vindicators')
    B.trial_spawner(30, GY, 18, 'witches')
    for z in range(9, 21, 3):
        for x in list(range(16, 22)) + list(range(27, 33)):
            B.set(x, GY, z, 'dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for (x, z) in [(15, 8), (33, 8), (15, 21), (33, 21)]:
        B.set(x, GY, z, 'purple_candle[candles=4,lit=true,waterlogged=false]')
    B.fx(24, 10, 14); B.zone(24, 8, 14)
    # east chapel x36..43, z10..20, archway in the nave wall z13..17
    for x in range(35, 45):
        for z in range(9, 22):
            for y in range(5, 18):
                edge = x == 44 or z in (9, 21) or y in (5, 17)
                B.set(x, y, z, (B.pick(FLOOR) if y == 5 else B.pick(WALL)) if edge else 'air')
    for z in range(13, 18):
        for y in range(6, 12): B.set(X2 + 1, y, z, 'air')
    for i in range(9):
        r, c = divmod(i, 3)
        B.bulb(1, 44, 11 - r, 13 + c, i)                     # bulbs in the east wall (facing west)
        B.lo_button(1, 37 + c, 9 - r, 10, f'polished_blackstone_button[face=wall,facing=south,powered=false]', i)   # panel on the north wall
    B.sign(38, 10, 10, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['Light every', 'candle of the', 'coven. Each lights', 'its neighbours.'], color='light_purple', glow=True)
    B.pz(1, 'lights', 40, 4, 15)
    B.fx(40, 9, 15)
    # west hidden archive x5..12, z10..20 (secret door in the nave wall at z15; wooden button among the bookshelves)
    for x in range(5, 14):
        for z in range(9, 22):
            for y in range(5, 13):
                edge = x == 5 or z in (9, 21) or y in (5, 12)
                if x == X1 - 1: continue
                B.set(x, y, z, (B.pick(FLOOR) if y == 5 else B.pick(WALL)) if edge else 'air')
    for z in range(9, 22):            # no windows between the nave and the secret archive
        for y in range(10, 20): B.set(X1 - 1, y, z, B.pick(WALL))
    for z in range(17, 22):
        for y in range(6, 9): B.set(X1, y, z, 'bookshelf')
    B.sbutton(X1 + 1, 7, 19, 'oak_button[face=wall,facing=east,powered=false]', 1)
    B.set(X1, 7, 19, 'bookshelf')
    B.sdoor(X1 - 1, GY, 15, 1)
    for x in (6, 7, 8):
        for z in (10, 20): B.set(x, 6, z, 'bookshelf'); B.set(x, 7, z, 'bookshelf')
    B.chest(7, GY, 15, 'east', loot='bm:p2/hex/hidden')
    B.chest(10, GY, 11, 'south', loot='minecraft:chests/stronghold_library')
    B.lectern(10, GY, 18, 'north', 'Forbidden Index', 'The Archmage', [
        "Index of forbidden works:\n\n1. On Blinking (taken)\n2. On the Hollow Pact (taken)\n3. Rat Gang: A Field Guide (vandalised)",
        "Whoever took the Tome of Blinking: it only works OUTSIDE consecrated ground. You will look very silly trying it in here."])
    B.set(9, 11, 15, 'soul_lantern[hanging=true,waterlogged=false]')

    # ---------------- G1 -> B: Library (P2 keypad)
    screen(SCREENS[1], 1)
    for z in range(26, 38, 4):
        for x in (15, 16, 32, 33):
            for y in range(6, 10): B.set(x, y, z, 'bookshelf')
    B.pz(2, 'waves', 24, GY, 31)
    B.el(2, 'wsp', 20, GY, 28)
    B.el(2, 'wsp', 28, GY, 28)
    B.el(2, 'wsp', 20, GY, 34)
    B.el(2, 'wsp', 28, GY, 34)
    B.sign(17, 8, SCREENS[2] - 1, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['The Choir', 'Militant', 'guards these', 'books.'], color='light_purple', glow=True)
    B.fx(24, 10, 31); B.zone(24, 8, 31)

    # ---------------- G2 -> C: Choir with the rune circle (P3) and the rose window on screen 3
    screen(SCREENS[2], 2)
    screen(SCREENS[3], 3)
    zc = 46
    import math
    spots = [(round(24 + 5 * math.cos(a)), round(zc + 4 * math.sin(a))) for a in [i * math.pi / 3 + 0.4 for i in range(6)]]
    layout = ['orange', 'purple', 'blue', 'red', 'yellow', 'lime']        # where each colour stands (not the answer order)
    for (x, z), col in zip(spots, layout):
        B.set(x, GY, z, 'chiseled_deepslate'); B.set(x, GY + 1, z, f'{col}_stained_glass')
        # button on the side facing the circle centre
        dx, dz = 24 - x, zc - z
        f = ('east' if dx > 0 else 'west') if abs(dx) >= abs(dz) else ('south' if dz > 0 else 'north')
        bx, bz = x + (1 if f == 'east' else -1 if f == 'west' else 0), z + (1 if f == 'south' else -1 if f == 'north' else 0)
        B.seq_button(3, bx, GY, bz, f'stone_button[face=wall,facing={f},powered=false]', ROSE.index(col) + 1, sound=ROSE.index(col) + 1)
    SEQS.setdefault('hex', {})[3] = 6
    # rose window on the choir face of screen 3, high up: six coloured petals clockwise from the top
    rz = SCREENS[3]
    petals = [(0, 3), (3, 2), (3, -2), (0, -3), (-3, -2), (-3, 2)]      # (dx, dy) clockwise from top, viewer facing north
    for (dx, dy), col in zip(petals, ROSE):
        for ex, ey in ((0, 0), (1, 0), (0, 1)):
            B.set(24 - (dx + ex), 15 + dy + ey, rz, f'{col}_stained_glass')
    B.set(24, 15, rz, 'black_stained_glass')
    B.sign(24, GY + 1, zc, 'oak_sign[rotation=8,waterlogged=false]', ['The window', 'remembers the', 'order of the', 'summoning.'], color='light_purple', glow=True)
    B.set(24, GY, zc, 'chiseled_deepslate')
    B.pz(3, 'seq', 24, 4, zc)
    B.fx(24, 10, 46); B.zone(24, 8, 46)

    # ---------------- G3 -> D antechamber (z54..57) -> battle door z58 -> Apse arena x10..38, z59..77
    B.vault(30, GY, 55, 'west', 'vkey_hex', 'bm:p2/hex/vault')
    B.sign(18, 8, 54, 'dark_oak_wall_sign[facing=south,waterlogged=false]', ['The Apse.', 'Kneel at the', "Archmage's altar", 'with his key.'], color='light_purple', glow=True)
    for x in range(9, 40):
        for y in range(5, 26): B.set(x, y, 58, B.pick(WALL))
    B.gate(24, GY, 58, 'x', 0, big=True)
    for x in range(9, 40):
        for z in range(59, 79):
            edge = x in (9, 39) or z == 78
            for y in range(5, 26): B.set(x, y, z, (B.pick(WALL) if edge else 'air') if y > 5 else B.pick(FLOOR))
            B.set(x, 26, z, 'deepslate_tiles')
    B.arena(24, GY, 68)
    B.altar(24, GY, 61)
    B.set(24, 5, 61, 'amethyst_block')
    for x in (22, 26): B.set(x, GY, 61, 'chiseled_deepslate'); B.set(x, GY + 1, 61, 'purple_candle[candles=3,lit=true,waterlogged=false]')
    for (x, z) in [(14, 64), (34, 64), (14, 74), (34, 74), (24, 76)]:
        B.set(x, GY, z, 'amethyst_block'); B.set(x, GY + 1, z, 'chiseled_deepslate')
        B.perch(x, GY + 2, z)
    for (x, z) in [(18, 66), (30, 66), (18, 73), (30, 73)]: B.mspawn(x, GY, z)
    B.vault(10, GY, 68, 'east', 'bkey_hex', 'bm:p2/hex/victor')
    for z in range(61, 78, 4):
        for x in (11, 37): B.set(x, GY, z, 'purple_candle[candles=3,lit=true,waterlogged=false]')
    B.fx(24, 12, 68); B.zone(24, 8, 68)
    B.controller(24, 14, 40)
    return B
