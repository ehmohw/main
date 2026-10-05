"""WILFREY'S KEEP: a Gothic blackstone castle in pale gardens and dark forests. 72 x 48 x 78, ground at y6
(floors at y6, walkable air from y7). Bobbery stole it when his cousin Wilfrey died.
Flow: drawbridge -> gatehouse -> Outer Bailey (open courtyard, trial spawners, gravestones)
  P1 Heraldry: six banners on the keep facade, a lever under each; raise only the rightful lord's (white) colours
  G1 (facade door) -> Great Hall (spawner): P2 combat waves (Bobbery's Bonecrew). Formerly a keypad: the
     hall's tally: skulls on the mantle (3), the usurper's black banners (5), candles at the high table (7), bells (2)
  G2 (west wall) -> the Lord's Stair down -> Crypt of the Fallen (under the hall): P3 six tombs, pressed in the
     order the knights fell (told by the chronicle lectern)
  G3 (crypt south wall) -> stair up -> Antechamber (spoils vault) -> battle door -> Throne Room (arena)
Secrets: Bobbery's Stash in the west gatehouse tower (button on a gravestone);
         Wilfrey's Tomb behind the crypt's east wall (a blackstone button on the crypt ceiling: "look up").
The throne room holds nothing flammable (Bobbery brings blazes)."""
from p2.kit import DBuild
from p2.config import CODES, SEQS

WALL = [('polished_blackstone_bricks', 5), ('cracked_polished_blackstone_bricks', 1.5), ('blackstone', 2), ('gilded_blackstone', 0.06)]
MASS = [('blackstone', 3), ('polished_blackstone_bricks', 3), ('basalt[axis=y]', 1)]
FLOOR = [('polished_blackstone', 4), ('polished_blackstone_bricks', 2), ('chiseled_polished_blackstone', 0.3)]
CRYPT = [('deepslate_bricks', 4), ('cracked_deepslate_bricks', 2), ('polished_deepslate', 1), ('sculk', 0.3)]
YARD = [('cobbled_deepslate', 3), ('polished_blackstone', 2), ('pale_moss_block', 1.2), ('coarse_dirt', 1), ('mud_bricks', 0.6)]
GY = 7
WANT = [1, 0, 0, 1, 1, 0]                 # banners west -> east: white (Wilfrey) = raise, black (Bobbery) = leave down
BANNER_X = [13, 20, 27, 45, 52, 59]
# crypt tombs: (x centre, row) -> (name, order fallen)
TOMBS = {(22, 'N'): ('Sir Aldric', 5), (36, 'N'): ('Dame Isolde', 2), (50, 'N'): ('Sir Cedric', 6),
         (22, 'S'): ('Sir Edmund', 3), (36, 'S'): ('Sir Bertram', 1), (50, 'S'): ('Dame Rowena', 4)}
CODE = '3572'


def build():
    B = DBuild('keep', 72, 48, 78, seed=5572)
    st = lambda f, half='bottom': f'polished_blackstone_brick_stairs[facing={f},half={half},shape=straight,waterlogged=false]'

    # ================================================================ ground works
    # courtyard: foundation, paving, and clear air (removes trees/terrain inside the walls)
    B.fillp(6, 0, 8, 65, 5, 31, MASS)
    B.fillp(6, 6, 8, 65, 6, 31, YARD)
    B.carve(6, 7, 8, 65, 47, 31)
    # keep mass: x6..65, z32..71, y0..24 (rooms are carved out of it), roof parapet
    B.fillp(6, 0, 32, 65, 24, 71, MASS)
    for x in range(6, 66):
        for z in range(32, 72):
            B.set(x, 24, z, B.pick(WALL))
            if x in (6, 65) or z in (32, 71):
                B.set(x, 25, z, B.pick(WALL))
                if (x + z) % 2 == 0: B.set(x, 26, z, B.pick(WALL))
    # outer faces of the keep in proper brick
    for y in range(6, 25):
        for x in range(6, 66):
            B.set(x, y, 32, B.pick(WALL))
        for z in range(32, 72):
            B.set(6, y, z, B.pick(WALL)); B.set(65, y, z, B.pick(WALL))
    # curtain walls (2 thick, y0..20, crenellated)
    def curtain(x1, z1, x2, z2):
        B.fillp(x1, 0, z1, x2, 20, z2, WALL)
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                if (x + z) % 2 == 0: B.set(x, 21, z, B.pick(WALL))
    curtain(4, 6, 5, 73); curtain(66, 6, 67, 73); curtain(4, 6, 67, 7); curtain(4, 72, 67, 73)
    # buttresses on the outer faces
    for z in range(12, 70, 8):
        for x in (3, 68):
            for y in range(6, 17): B.set(x, y, z, B.pick(WALL))
            B.set(x, 17, z, st('east' if x == 3 else 'west'))
    for x in range(12, 64, 8):
        for z in (74,):
            for y in range(6, 17): B.set(x, y, z, B.pick(WALL))
            B.set(x, 17, z, st('north'))
    # corner towers with spires
    for (cx, cz) in [(5, 7), (66, 7), (5, 72), (66, 72)]:
        for x in range(cx - 4, cx + 5):
            for z in range(cz - 4, cz + 5):
                if (x - cx) ** 2 + (z - cz) ** 2 > 18: continue
                for y in range(0, 31): B.set(x, y, z, B.pick(WALL))
                if (x - cx) ** 2 + (z - cz) ** 2 >= 12 and (x + z) % 2 == 0: B.set(x, 31, z, B.pick(WALL))
        for i, y in enumerate(range(32, 40)):
            r = 3.6 - i * 0.45
            for x in range(cx - 4, cx + 5):
                for z in range(cz - 4, cz + 5):
                    if (x - cx) ** 2 + (z - cz) ** 2 <= r * r: B.set(x, y, z, 'deepslate_tiles' if i % 3 else 'polished_blackstone_bricks')
        B.set(cx, 40, cz, 'polished_blackstone_wall'); B.set(cx, 41, cz, 'soul_lantern[hanging=false,waterlogged=false]')
        for (dx, dz) in ((4, 0), (-4, 0), (0, 4), (0, -4)):
            for y in (12, 13, 22, 23):
                B.set(cx + dx, y, cz + dz, 'iron_bars')
    # donjon (great tower over the hall), sealed, with a spire
    for x in range(26, 47):
        for z in range(36, 47):
            for y in range(25, 39):
                if x in (26, 46) or z in (36, 46) or y == 38: B.set(x, y, z, B.pick(WALL))
                else: B.set(x, y, z, 'blackstone')
    for i, y in enumerate(range(39, 48)):
        for x in range(27 + i, 46 - i):
            for z in range(37 + min(i, 4), 46 - min(i, 4)):
                if x in (27 + i, 45 - i) or z in (37 + min(i, 4), 45 - min(i, 4)): B.set(x, y, z, 'deepslate_tiles')
    for x in (30, 36, 42):
        for y in range(28, 35): B.set(x, y, 36, 'black_stained_glass_pane')
    for (x, z) in [(26, 36), (46, 36), (26, 46), (46, 46)]:
        for y in range(39, 44): B.set(x, y, z, 'polished_blackstone_wall')

    # gothic dressing: pinnacles along the keep roof, a steep slate roof over the throne room, false lancet windows
    for x in range(6, 66, 6):
        for z in (32, 71):
            for y in range(25, 29): B.set(x, y, z, 'polished_blackstone_bricks')
            B.set(x, 29, z, 'polished_blackstone_wall')
    for z in range(32, 72, 6):
        for x in (6, 65):
            for y in range(25, 29): B.set(x, y, z, 'polished_blackstone_bricks')
            B.set(x, 29, z, 'polished_blackstone_wall')
    for i in range(0, 9):
        for x in range(14, 58):
            B.set(x, 25 + i, 56 + i, 'deepslate_tiles'); B.set(x, 25 + i, 71 - i, 'deepslate_tiles')
            for z in range(56 + i + 1, 71 - i): B.set(x, 25 + i, z, 'blackstone')
        for z in range(56 + i, 72 - i):
            B.set(14, 25 + i, z, B.pick(WALL)); B.set(57, 25 + i, z, B.pick(WALL))
    for x in range(16, 57, 4):
        B.set(x, 34, 63, 'polished_blackstone_wall'); B.set(x, 34, 64, 'polished_blackstone_wall')
    for (x, z) in [(14, 56), (57, 56), (14, 71), (57, 71)]:
        for y in range(25, 38): B.set(x, y, z, 'polished_blackstone_bricks')
        B.set(x, 38, z, 'polished_blackstone_wall'); B.set(x, 39, z, 'soul_lantern[hanging=false,waterlogged=false]')
    for z in range(36, 70, 5):
        for x in (6, 65):
            for y in range(9, 20): B.set(x, y, z, 'black_stained_glass' if y < 19 else 'chiseled_polished_blackstone')
    for x in range(10, 64, 5):
        for y in range(9, 18): B.set(x, y, 73, 'black_stained_glass' if y < 17 else 'chiseled_polished_blackstone')

    # ================================================================ gatehouse + drawbridge
    B.fillp(29, 0, 2, 43, 26, 10, WALL)
    for x in range(29, 44):
        if (x % 2): B.set(x, 27, 2, B.pick(WALL)); B.set(x, 27, 10, B.pick(WALL))
    B.carve(34, 7, 2, 38, 12, 10)
    B.fillp(34, 6, 2, 38, 6, 10, FLOOR)
    for x in range(34, 39):
        B.set(x, 12, 4, 'iron_bars'); B.set(x, 11, 4, 'iron_bars')          # raised portcullis teeth
        B.set(x, 12, 8, 'iron_bars')
        B.set(x, 6, 0, st('south')); B.set(x, 6, 1, 'polished_blackstone_bricks')
    for x in (33, 39):
        B.set(x, 7, 0, 'polished_blackstone_wall'); B.set(x, 8, 0, 'soul_lantern[hanging=false,waterlogged=false]')
        for y in range(6, 9): B.set(x, y, 1, B.pick(WALL))
    for (x, z) in [(29, 2), (43, 2)]:
        for y in range(27, 33): B.set(x, y, z, 'polished_blackstone_wall')
    for y in (15, 16, 20, 21):
        for x in (31, 41): B.set(x, y, 2, 'iron_bars')
    B.sign(36, 13, 2, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ["WILFREY'S KEEP", '', '(not his', 'anymore)'], color='red', glow=True)
    B.entrance(36, GY, 1)
    # Bobbery's Stash: west gatehouse tower interior (secret door to the courtyard; button on a gravestone)
    B.carve(30, 7, 3, 32, 10, 8)
    B.fillp(30, 6, 3, 32, 6, 8, FLOOR)
    B.sdoor(31, GY, 10, 1)
    B.carve(31, 7, 9, 31, 8, 9)
    B.chest(30, GY, 4, 'east', loot='minecraft:chests/bastion_other')
    B.chest(32, GY, 4, 'west', loot='minecraft:chests/nether_bridge')
    B.set(31, GY, 3, 'barrel[facing=up,open=false]', {'id': 'minecraft:barrel', 'LootTable': 'bm:p2/keep/spawner'})
    B.set(31, 10, 6, 'soul_lantern[hanging=true,waterlogged=false]'); B.set(31, 11, 6, 'polished_blackstone_bricks')
    B.sign(32, 8, 8, 'dark_oak_wall_sign[facing=west,waterlogged=false]', ['PROPERTY OF', 'BOBBERY', 'touch it and', "you're bones"], color='red')

    # ================================================================ OUTER BAILEY (courtyard) + P1 heraldry
    B.fx(36, 10, 20); B.zone(36, 8, 20); B.zone(16, 8, 24); B.zone(56, 8, 24)
    B.trial_spawner(16, GY, 18, 'wither_knights')
    B.trial_spawner(56, GY, 18, 'wither_knights')
    # gravestones (one hides the stash button), dead pale oaks, soul braziers, eyeblossoms
    graves = [(20, 13), (25, 15), (14, 26), (18, 28), (52, 13), (58, 26), (54, 28), (48, 15)]
    for (x, z) in graves:
        B.set(x, GY, z, 'polished_blackstone'); B.set(x, GY + 1, z, 'polished_blackstone_brick_slab[type=bottom,waterlogged=false]')
        B.set(x, GY, z - 1, 'pale_moss_carpet[bottom=true,east=none,north=none,south=none,west=none]')
    B.sbutton(25, GY, 14, 'polished_blackstone_button[face=wall,facing=north,powered=false]', 1)   # replaces that grave's carpet
    for (tx, tz) in [(10, 12), (62, 12), (30, 22), (42, 22)]:
        for y in range(GY, GY + 7): B.set(tx, y, tz, 'pale_oak_log[axis=y]')
        for dx, dz, ax in ((1, 0, 'x'), (-1, 0, 'x'), (0, 1, 'z')):
            B.set(tx + dx, GY + 5, tz + dz, f'pale_oak_log[axis={ax}]')
            B.set(tx + dx, GY + 4, tz + dz, 'pale_hanging_moss[tip=true]')
        B.set(tx + 2, GY + 6, tz, 'pale_oak_log[axis=x]')
    for (x, z) in [(22, 20), (50, 20), (36, 16)]:
        B.set(x, GY, z, 'polished_blackstone_bricks'); B.set(x, GY + 1, z, 'soul_campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    B.scatter(8, GY, 11, 63, 30, 'closed_eyeblossom', 0.02, soil='minecraft:pale_moss_block',
              soil_on=('minecraft:cobbled_deepslate', 'minecraft:mud_bricks'))
    B.scatter(8, GY, 11, 63, 30, 'pale_moss_carpet[bottom=true,east=none,north=none,south=none,west=none]', 0.04)
    # keep it clear in front of the levers and the door
    B.carve(8, GY, 29, 63, GY + 3, 31)
    B.lectern(40, GY, 12, 'north', "A Herald's Note", 'Unknown', [
        "This keep was built by Wilfrey the Kind, who stood with the Overworld in the War of the Withered Host.",
        "His colours were WHITE and GOLD. When he died, his cousin Bobbery took the keep and hung his own BLACK banners beside them.",
        "The great door answers only to the rightful lord. Pull the lever beneath each of his banners. Leave the usurper's levers be.",
        "(Bobbery hides his takings behind a grave near the gate. Everyone knows. Nobody says.)"])
    for i, (x, w) in enumerate(zip(BANNER_X, WANT)):
        B.set(x, 11, 31, f'{"white" if w else "black"}_wall_banner[facing=north]')
        if w: B.set(x, 13, 31, 'gold_block')
        B.lever(1, x, 8, 31, 'north', w)
    B.sign(33, 9, 31, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['Pull the lever', 'under each of', "the lord's", 'colours.'], color='white', glow=True)
    B.sign(39, 9, 31, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['Leave the', "usurper's", 'levers be.', ''], color='red', glow=True)
    B.pz(1, 'levers', 36, 4, 30)
    for x in (18, 24, 48, 54):                  # tall hall windows in the facade
        for y in range(12, 20):
            B.set(x, y, 32, 'black_stained_glass_pane'); B.set(x, y, 33, 'air')

    # ================================================================ G1 -> GREAT HALL
    B.gate(36, GY, 32, 'x', 1)
    B.carve(35, GY, 33, 37, GY + 3, 33)
    B.carve(15, GY, 34, 56, 22, 48)
    B.fillp(15, 6, 34, 56, 6, 48, FLOOR)
    for x in range(15, 57):                     # ribbed ceiling
        for z in range(34, 49):
            if z % 4 == 2: B.set(x, 22, z, 'polished_blackstone_bricks')
    for x in (21, 28, 44, 51):
        for z in (38, 44):
            for y in range(GY, 22): B.set(x, y, z, 'polished_blackstone_bricks' if y % 5 else 'chiseled_polished_blackstone')
    for (x, z) in [(24, 42), (48, 42), (36, 38)]:            # soul chandeliers (from the ribs)
        for y in range(18, 22): B.set(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        B.set(x, 17, z, 'soul_lantern[hanging=true,waterlogged=false]')
    # THE TALLY (each counted thing appears nowhere else in the hall)
    B.set(32, 21, 42, 'bell[attachment=ceiling,facing=north,powered=false]')            # bells: 2 (hung from a ceiling rib)
    B.set(40, 21, 42, 'bell[attachment=ceiling,facing=north,powered=false]')
    for x in range(30, 43): B.set(x, GY, 46, 'polished_blackstone_brick_slab[type=top,waterlogged=false]')     # high table
    for x in range(30, 43, 2): B.set(x, GY + 1, 46, 'candle[candles=1,lit=true,waterlogged=false]')            # candles: 7
    B.set(36, GY, 47, 'blackstone_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for x in (34, 38): B.set(x, GY, 47, 'polished_blackstone_brick_slab[type=bottom,waterlogged=false]')
    B.set(57, GY, 41, 'soul_campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]')               # fireplace
    B.set(57, GY + 1, 41, 'air')
    for z in range(39, 44): B.set(56, 10, z, 'polished_blackstone_brick_slab[type=top,waterlogged=false]')    # mantle
    for z in (40, 41, 42): B.set(56, 11, z, 'wither_skeleton_skull[powered=false,rotation=4]')                # skulls: 3
    for z in (35, 37, 41, 45, 47): B.set(56, 15, z, 'black_wall_banner[facing=west]')                         # black banners: 5
    B.lectern(33, GY, 35, 'north', "Steward's Ledger", 'The Steward', [
        "Bobbery's crew has taken the hall. They drink, they brawl, and they bar the Lord's Stair.",
        "Clear them out - every last one - and the stair will open."])
    B.trial_spawner(25, GY, 41, 'wither_knights')
    B.fx(36, 12, 41); B.zone(36, 8, 41); B.zone(20, 8, 41); B.zone(52, 8, 41)
    # P2 keypad on the west wall, beside the Lord's Stair (G2)
    B.pz(2, 'waves', 36, GY, 41)
    B.el(2, 'wsp', 20, GY, 36)
    B.el(2, 'wsp', 52, GY, 36)
    B.el(2, 'wsp', 20, GY, 46)
    B.el(2, 'wsp', 52, GY, 46)
    B.el(2, 'wsp', 36, GY, 44)
    B.sign(15, 11, 44, 'dark_oak_wall_sign[facing=east,waterlogged=false]', ["The Lord's", 'Stair', '', ''], color='white', glow=True)

    # ================================================================ G2 -> the Lord's Stair -> CRYPT
    B.gate(14, GY, 44, 'z', 2)
    B.carve(8, GY, 43, 13, GY + 3, 47)
    B.fillp(8, 6, 43, 13, 6, 47, FLOOR)
    for k, z in enumerate(range(42, 37, -1)):        # z42 walk 6 ... z38 walk 2
        walk = 6 - k
        for x in range(8, 11):
            B.set(x, walk - 1, z, 'polished_blackstone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
            for y in range(walk, walk + 4): B.set(x, y, z, 'air')
    B.carve(8, 1, 35, 15, 4, 37)
    B.fillp(8, 0, 35, 15, 0, 37, CRYPT)
    B.set(9, 10, 45, 'soul_lantern[hanging=true,waterlogged=false]')
    # the crypt (under the hall)
    B.carve(16, 1, 35, 55, 5, 47)
    B.fillp(16, 0, 35, 55, 0, 47, [('deepslate_tiles', 3), ('cracked_deepslate_tiles', 1)])
    for x in range(16, 56):
        for z in (35, 47):
            for y in range(1, 6):
                if x % 6 == 1 and not 33 <= x <= 39: B.set(x, y, z, 'polished_deepslate')
    for (xc, row), (name, order) in TOMBS.items():
        zs, zb, f = ((37, 38), 39, 'south') if row == 'N' else ((44, 45), 43, 'north')
        for x in range(xc - 1, xc + 2):
            for z in zs:
                B.set(x, 1, z, 'polished_blackstone_bricks'); B.set(x, 2, z, 'polished_blackstone_bricks')
                B.set(x, 3, z, 'polished_blackstone_brick_slab[type=top,waterlogged=false]')
        B.seq_button(3, xc, 1, zb, f'polished_blackstone_button[face=wall,facing={f},powered=false]', order, sound=order)
        B.sign(xc, 2, zb, f'dark_oak_wall_sign[facing={f},waterlogged=false]', ['Here lies', name, '', ''], color='white', glow=True)
        B.set(xc - 1, 4, zs[0], 'skeleton_skull[powered=false,rotation=0]')
        B.set(xc + 1, 4, zs[1], 'white_candle[candles=2,lit=true,waterlogged=false]')
    SEQS.setdefault('keep', {})[3] = 6
    B.lectern(18, 1, 41, 'east', 'The Six Who Fell', 'Wilfrey', [
        "I buried my knights here, beneath the hall where we feasted. They rest in the order they were laid down. Honour them in that order, and the stair to the throne will open.",
        "Sir Bertram fell first, holding the river ford on the first night of the war.\n\nDame Isolde went back for him at dawn. She did not come back either.",
        "Sir Edmund fell third, at the burning mill.\n\nWhen the Withered Host reached our walls, Dame Rowena held the gate until it broke.",
        "Sir Aldric died on the stair, and bought us the night.\n\nLast of all, Sir Cedric fell at my side, on the final day.",
        "I am not among them. I asked to lie apart from them, behind these walls, where the war cannot follow. If you seek me, look up."])
    B.pz(3, 'seq', 36, 0, 41)
    B.trial_spawner(53, 1, 41, 'wither_knights')
    for (x, z) in [(29, 41), (43, 41)]:
        B.set(x, 5, z, 'soul_lantern[hanging=true,waterlogged=false]')
    B.ceiling_scatter(16, 5, 35, 55, 47, 'cobweb', 0.05)
    B.fx(36, 3, 41); B.zone(36, 2, 41); B.zone(18, 2, 36)
    # hidden: ceiling button above the aisle ("look up") -> Wilfrey's Tomb behind the east wall
    B.set(36, 6, 41, 'polished_blackstone')
    B.set(37, 5, 41, 'air'); B.set(35, 5, 41, 'air')
    B.sbutton(36, 5, 41, 'polished_blackstone_button[face=ceiling,facing=north,powered=false]', 2)
    B.carve(58, 1, 38, 64, 4, 44)
    B.fillp(58, 0, 38, 64, 0, 44, [('calcite', 2), ('polished_diorite', 1)])
    for x in range(58, 65):
        for z in (38, 44):
            for y in range(1, 5): B.set(x, y, z, 'polished_diorite' if y % 2 else 'calcite')
    B.sdoor(56, 1, 41, 2)
    B.carve(57, 1, 41, 57, 2, 41)
    for x in range(61, 64):
        B.set(x, 1, 41, 'quartz_pillar[axis=x]'); B.set(x, 2, 41, 'smooth_quartz_slab[type=bottom,waterlogged=false]')
    for (x, z) in [(60, 40), (60, 42), (64, 40), (64, 42)]:
        B.set(x, 1, z, 'white_candle[candles=3,lit=true,waterlogged=false]')
    B.chest(63, 1, 43, 'north', loot='bm:p2/keep/hidden')
    B.chest(59, 1, 43, 'north', loot='minecraft:chests/bastion_treasure')
    B.lectern(59, 1, 39, 'east', 'Epitaph', 'Bobbery', [
        "WILFREY\nLord of this Keep\nShield of the Overworld\n\nHe was kind to everyone.\nEven me.",
        "I kept his sword and his shield here. I could never lift the shield. It would not let me.\n\n- B."])

    # ================================================================ G3 -> stair up -> ANTECHAMBER -> THRONE ROOM
    B.gate(36, 1, 48, 'x', 3)
    B.carve(33, 1, 49, 39, 4, 52)
    B.fillp(33, 0, 49, 39, 0, 52, CRYPT)
    for k, x in enumerate(range(40, 46)):        # x40 walk 2 ... x45 walk 7
        walk = 2 + k
        for z in range(50, 53):
            B.set(x, walk - 1, z, 'polished_blackstone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
            for y in range(walk, 14): B.set(x, y, z, 'air')
    B.carve(28, GY, 50, 50, 13, 55)
    for x in range(28, 51):
        for z in range(50, 56):
            if not (40 <= x <= 45 and 50 <= z <= 52): B.set(x, 6, z, B.pick(FLOOR))
    for x in range(40, 45): B.set(x, GY, 53, 'polished_blackstone_wall')
    for z in range(50, 53): B.set(39, GY, z, 'polished_blackstone_wall')
    B.vault(30, GY, 53, 'east', 'vkey_keep', 'bm:p2/keep/vault')
    B.sign(32, 10, 55, 'dark_oak_wall_sign[facing=north,waterlogged=false]', ['THE THRONE', 'Kneel at the altar', "with Wilfrey's", 'Signet.'], color='red', glow=True)
    for x in (29, 49):
        B.set(x, 12, 52, 'soul_lantern[hanging=true,waterlogged=false]'); B.set(x, 13, 52, 'iron_chain[axis=y,waterlogged=false]')
    B.zone(36, 8, 52)
    B.trial_spawner(47, GY, 54, 'blazes')                  # the throne's guard: nothing flammable in here
    # battle door + throne room (arena): nothing flammable in here
    B.gate(36, GY, 56, 'x', 0, big=True)
    B.carve(16, GY, 57, 55, 22, 71)
    for x in range(16, 56):
        for z in range(57, 72):
            B.set(x, 6, z, B.pick([('polished_blackstone', 3), ('polished_blackstone_bricks', 2), ('gilded_blackstone', 0.1)]))
    for x in range(31, 42):                      # dais
        for z in range(68, 72): B.set(x, GY, z, 'polished_blackstone_bricks')
    B.set(36, GY + 1, 70, 'blackstone_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for x in (35, 37): B.set(x, GY + 1, 70, 'polished_blackstone_wall')
    for x in (35, 36, 37):
        for y in range(GY + 1, GY + 7): B.set(x, y, 71, 'gilded_blackstone' if x == 36 or y > GY + 4 else 'polished_blackstone_bricks')
    for (x, z) in [(24, 61), (48, 61), (24, 67), (48, 67)]:
        for y in range(GY, 22): B.set(x, y, z, 'polished_blackstone_bricks' if y % 4 else 'chiseled_polished_blackstone')
    for (x, z) in [(30, 63), (42, 63), (30, 69), (42, 69), (36, 65)]:
        for y in range(19, 23): B.set(x, y, z, 'iron_chain[axis=y,waterlogged=false]')
        B.set(x, 18, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for z in range(58, 71, 4):
        for x in (15, 56): B.set(x, 12, z, 'shroomlight')
    for x in range(17, 55, 6):
        B.set(x, 12, 72, 'shroomlight')
    B.arena(36, GY, 64)
    B.altar(36, GY, 59)
    B.set(36, 6, 59, 'gilded_blackstone')
    for x in (34, 38): B.set(x, GY, 59, 'chiseled_polished_blackstone'); B.set(x, GY + 1, 59, 'soul_lantern[hanging=false,waterlogged=false]')
    for (x, z) in [(22, 64), (50, 64), (26, 69), (46, 69)]: B.mspawn(x, GY, z)
    B.vault(17, GY, 64, 'east', 'bkey_keep', 'bm:p2/keep/victor')
    B.xdoor(48, GY, 72)
    B.carve(48, GY, 73, 48, GY + 1, 73)
    B.fx(36, 12, 64); B.zone(36, 8, 64)
    B.controller(36, 12, 40)
    from p2.dungeons import exterior
    exterior.keep(B)                          # 2.13: exterior dressing (open-world cells and the outer skin only)
    return B
