"""2.65: the vault's new rooms, as templates (their logic is phase76). Same plan as every room: 25 wide and deep, entry in
the west wall and exit in the east (x 24, z 11-13, y 4-7, barred until beaten), the controller marker at (12.5, 4, 12.5).
The bell tower is taller (26) and its exit is ten blocks up.

PUZZLES  lamps (the Signal Lamps: repeat the sequence), lightsout (the Lamp Floor: light every lamp), tumbler (the
         Tumbler Lock: catch the running light on the gate)
PARKOUR  climb (the Bell Tower), rafters (the Crumbling Rafters)
COMBAT   ambush (the Arcane Study: casters spring a trap), pit (the Champion's Pit: a champion, sometimes the Rat King)
EVENTS   rave (the Rat Rave), rest (the Rats' Rest), storm (the Storm Vault), ufo (the Vorn Landing), grove (the
         Enchanted Grove)"""
import random
from structures import Build
import phase70_rooms as RM
from phase75_rooms import BASE, wall_glow

W, D = 25, 25
FY = 3

# ---------------------------------------------------------------- shared positions (phase76 reads these)
LAMPS_X = [8, 11, 14, 17]                     # signal lamps (north wall, y 7) and their buttons (y 5, z 1)
LAMP_COL = ['red', 'blue', 'lime', 'yellow']
LO_BTN = lambda i, j: (5 + i, 5, 11 + j)      # the Lamp Floor's desk buttons (on the desk at y 4)
LO_CELL = lambda i, j: (9 + 3 * i, 8 + 3 * j)  # its 3x3 lamp cells (floor, y 3): x..x+2, z..z+2
TUMB_X = list(range(8, 17))                   # the tumbler's running lights (north wall, y 7); the gate is the middle one
CLIMB_H, CLIMB_EXIT = 26, 14                  # the bell tower: height, the exit door's floor level
RAFT = [(4, 12), (5, 12), (7, 11), (8, 11), (10, 12), (12, 13), (13, 13), (15, 12), (17, 11), (18, 11), (20, 12)]
STORM_LEVERS = [(6, 5, 7, 'south'), (18, 5, 7, 'south'), (12, 5, 19, 'north')]   # (lever cell, the face it's on)
STORM_PILLARS = [(6, 6), (18, 6), (12, 20)]
UFO_CORES = [(9, 12), (15, 12), (12, 15)]
GROVE_WISPS = [(4, 6, 4), (20, 7, 5), (5, 6, 20), (19, 8, 19), (12, 9, 3), (12, 6, 21)]
RAVE = ['red', 'blue', 'lime', 'yellow', 'magenta']
SECRET_SPOTS = [(0, 5, 5), (0, 6, 19), (24, 5, 5), (24, 6, 19), (5, 5, 0), (19, 6, 0), (5, 6, 24), (19, 5, 24)]


def shell(exit_closed=True):
    return RM.shell(W, exit_closed)


def ctrl(b, kind):
    b.marker(*RM.CTRL, ['bm.gvr', f'bm.gvr_{kind}', 'bm.gvnew'])


def label_wall(b, x1, x2, y, z, block='minecraft:dark_oak_planks'):
    for x in range(x1, x2 + 1): b.set(x, y, z, block)


# ===================================================================== PUZZLES
def lamps():
    b = shell()
    for i, x in enumerate(LAMPS_X):
        c = LAMP_COL[i]
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                b.set(x + dx, 7 + dy, 0, f'minecraft:{c}_concrete')
        b.set(x, 7, 0, 'minecraft:redstone_lamp[lit=false]')
        b.set(x, 5, 0, BASE['metal'])
    label_wall(b, 7, 18, 9, 0)
    ctrl(b, 'lamps'); return wall_glow(b)


def lightsout():
    b = shell()
    for i in range(3):
        for j in range(3):
            x0, z0 = LO_CELL(i, j)
            for dx in range(3):
                for dz in range(3):
                    b.set(x0 + dx, FY, z0 + dz, 'minecraft:redstone_lamp[lit=true]')
            bx, by, bz = LO_BTN(i, j)
            b.set(bx, 4, bz, BASE['pillar'])
    for x in range(8, 19):                                   # a gold frame round the lamp floor
        for z in (7, 17): b.set(x, FY, z, BASE['metal'])
    for z in range(7, 18):
        for x in (8, 18): b.set(x, FY, z, BASE['metal'])
    b.set(5, 4, 9, BASE['pillar'])                           # (the reset button's post)
    ctrl(b, 'lightsout'); return wall_glow(b)


def tumbler():
    b = shell()
    for x in TUMB_X:
        b.set(x, 7, 0, 'minecraft:redstone_lamp[lit=false]')
        b.set(x, 8, 0, BASE['trim']); b.set(x, 6, 0, BASE['trim'])
    gx = TUMB_X[4]
    for dy in (5, 6, 7, 8, 9):
        b.set(gx - 1, dy, 0, BASE['metal']); b.set(gx + 1, dy, 0, BASE['metal'])
    b.set(gx, 9, 0, BASE['metal']); b.set(gx, 6, 0, BASE['metal'])
    for x in range(gx - 1, gx + 2):                          # a plinth for the big button
        b.set(x, 4, 2, BASE['pillar'])
    ctrl(b, 'tumbler'); return wall_glow(b)


# ===================================================================== PARKOUR
def climb():
    """the Bell Tower: platforms spiral up the walls round a bell column to a landing by the high exit"""
    H = CLIMB_H
    b = Build(W, H, D)
    b.fill(0, 0, 0, W - 1, FY - 1, D - 1, 'minecraft:blackstone')
    b.room(0, FY, 0, W - 1, H - 1, D - 1, BASE['wall'], floor='minecraft:hay_block', ceil=BASE['ceil'])
    for y in range(4, 8):                                    # entry (west, the usual place), the high exit (east, barred)
        for z in (11, 12, 13): b.set(0, y, z, 'minecraft:air')
    for y in range(CLIMB_EXIT, CLIMB_EXIT + 4):
        for z in (11, 12, 13): b.set(W - 1, y, z, 'minecraft:iron_bars')
    for y in range(CLIMB_EXIT, CLIMB_EXIT + 5):
        b.set(W - 1, y, 10, BASE['metal']); b.set(W - 1, y, 14, BASE['metal'])
    for z in range(10, 15): b.set(W - 1, CLIMB_EXIT + 4, z, BASE['metal'])
    for y in (4, 5, 6, 7, 8):
        b.set(0, y, 10, BASE['metal']); b.set(0, y, 14, BASE['metal'])
    for z in range(10, 15): b.set(0, 8, z, BASE['metal'])
    for y in range(4, H - 2):                                # the bell column
        for x in (11, 12, 13):
            for z in (11, 12, 13):
                b.set(x, y, z, BASE['pillar'] if (x, z) != (12, 12) else BASE['wall'])
    b.set(12, H - 3, 12, 'minecraft:iron_chain'); b.set(12, H - 4, 12, 'minecraft:bell[attachment=ceiling,facing=north]')
    for y in (8, 13, 18):
        for (x, z) in ((10, 12), (14, 12), (12, 10), (12, 14)): b.set(x, y, z, BASE['glow'])
    # the climb: 2x2 steps, one block higher each, along the north wall then the east, to the landing
    path = [(3, 7), (3, 4), (6, 3), (9, 3), (12, 3), (15, 3), (18, 3), (21, 4), (21, 7)]
    for k, (x, z) in enumerate(path):
        top = 4 + k                                           # the step's top block (stand on top+1)
        for dx in (0, 1):
            for dz in (0, 1):
                b.set(x + dx, top, z + dz, BASE['trim'] if k % 2 else BASE['floor'])
        b.set(x, top - 1, z, 'minecraft:iron_chain')
    land_top = CLIMB_EXIT - 1
    for x in range(19, 24):                                  # the landing (stand at the exit's level)
        for z in range(9, 16):
            b.set(x, land_top, z, BASE['floor'])
    for z in range(10, 16): b.set(19, land_top + 1, z, 'minecraft:polished_blackstone_wall')     # (a rail on the pit side; the last step comes in from the north)
    b.set(21, land_top + 1, 12, 'minecraft:light_weighted_pressure_plate')
    for x in range(4, W - 3, 6):
        for z in (6, 18):
            if not (11 <= x <= 13): b.set(x, H - 2, z, 'minecraft:iron_chain'); b.set(x, H - 3, z, 'minecraft:lantern[hanging=true]')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_climb', 'bm.gvnew'])
    for x in (6, 18):
        for z in (0, D - 1):
            b.set(x, 6, z, BASE['glow']); b.set(x, 15, z, BASE['glow'])
    return b


def rafters():
    b = shell()
    for x in range(3, 22):                                   # the pit under the rafters
        for z in range(4, 21):
            b.set(x, FY, z, 'minecraft:air'); b.set(x, 2, z, 'minecraft:air'); b.set(x, 1, z, 'minecraft:air')
            b.set(x, 0, z, 'minecraft:hay_block')
    for (x, z) in RAFT:
        b.set(x, FY, z, BASE['trim'])
    for z in range(4, 21):                                   # the ends stand firm
        b.set(2, FY, z, BASE['floor']); b.set(22, FY, z, BASE['floor'])
    b.set(22, FY, 12, BASE['metal']); b.set(22, 4, 12, 'minecraft:light_weighted_pressure_plate')
    for x in range(4, 22, 3):                                # old beams overhead, for the look of it
        for z in range(4, 21): b.set(x, 13, z, 'minecraft:stripped_dark_oak_log[axis=z]')
    for x in range(3, 22, 6):
        b.set(x, 12, 12, 'minecraft:iron_chain'); b.set(x, 11, 12, 'minecraft:lantern[hanging=true]')
    ctrl(b, 'rafters'); return wall_glow(b)


# ===================================================================== COMBAT
def ambush():
    b = shell()
    for z in list(range(2, 10)) + list(range(15, 23)):       # an arcane study: bookshelves, lecterns, candles, amethyst
        for y in (4, 5, 6):
            b.set(1, y, z, 'minecraft:bookshelf'); b.set(23, y, z, 'minecraft:bookshelf')
    for x in range(2, 23):
        if 10 <= x <= 14: continue
        for y in (4, 5, 6):
            b.set(x, y, 1, 'minecraft:bookshelf'); b.set(x, y, 23, 'minecraft:bookshelf')
    for (x, z) in ((6, 6), (18, 6), (6, 18), (18, 18)):
        b.set(x, 4, z, 'minecraft:enchanting_table'); b.set(x, 3, z, 'minecraft:crying_obsidian')
        b.set(x + 1, 4, z, 'minecraft:amethyst_block'); b.set(x + 1, 5, z, 'minecraft:amethyst_cluster[facing=up]')
    for (x, z) in ((9, 6), (15, 6), (9, 18), (15, 18)):
        b.set(x, 4, z, 'minecraft:lectern[facing=south]')
    for (x, z) in ((3, 3), (21, 3), (3, 21), (21, 21)):
        b.set(x, 5, z, 'minecraft:purple_candle[candles=4,lit=true]')
    for x in range(2, 23):                                   # a violet runner
        for z in (11, 12, 13): b.set(x, FY, z, 'minecraft:purple_glazed_terracotta' if z == 12 else BASE['floor'])
    ctrl(b, 'ambush'); return wall_glow(b)


def pit():
    b = shell()
    for x in range(6, 19):                                   # a sunken sand ring, banners at the corners
        for z in range(6, 19):
            if (x - 12) ** 2 + (z - 12) ** 2 <= 40: b.set(x, FY, z, 'minecraft:smooth_sandstone' if (x + z) % 2 else 'minecraft:sandstone')
    for (x, z) in ((5, 5), (19, 5), (5, 19), (19, 19)):
        for y in range(4, 9): b.set(x, y, z, BASE['pillar'])
        b.set(x, 9, z, 'minecraft:soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=north]')
    for x in range(8, 17, 2):
        b.set(x, 4, 1, 'minecraft:red_wool'); b.set(x, 4, 23, 'minecraft:red_wool')
    ctrl(b, 'pit'); return wall_glow(b)


# ===================================================================== EVENTS (their own look - the theming passes them by)
def rave():
    b = Build(W, 16, D)
    b.fill(0, 0, 0, W - 1, FY - 1, D - 1, 'minecraft:glowstone')
    b.room(0, FY, 0, W - 1, 15, D - 1, 'minecraft:black_concrete', floor='minecraft:black_concrete', ceil='minecraft:black_concrete')
    rnd = random.Random(7)
    for x in range(2, 23):                                   # the dance floor: coloured glass over light (phase76 reshuffles it)
        for z in range(2, 23):
            c = RAVE[((x - 2) // 3 + (z - 2) // 3) % len(RAVE)]
            b.set(x, FY, z, f'minecraft:{c}_stained_glass')
    for y in range(4, 8):
        for z in (11, 12, 13):
            b.set(0, y, z, 'minecraft:air'); b.set(W - 1, y, z, 'minecraft:iron_bars')
    for y in (4, 5, 6, 7, 8):
        for x in (0, W - 1): b.set(x, y, 10, 'minecraft:gold_block'); b.set(x, y, 14, 'minecraft:gold_block')
    for z in range(10, 15): b.set(0, 8, z, 'minecraft:gold_block'); b.set(W - 1, 8, z, 'minecraft:gold_block')
    for x in range(9, 16):                                   # the DJ booth (north)
        b.set(x, 4, 2, 'minecraft:note_block'); b.set(x, 4, 1, 'minecraft:black_concrete')
    b.set(12, 4, 2, 'minecraft:jukebox'); b.set(10, 5, 2, 'minecraft:sea_lantern'); b.set(14, 5, 2, 'minecraft:sea_lantern')
    for x in range(2, 23, 4):                                # stage lights round the walls
        for z in (0, D - 1): b.set(x, 10, z, 'minecraft:sea_lantern'); b.set(x, 6, z, f'minecraft:{RAVE[x % 5]}_stained_glass')
    for z in range(2, 23, 4):
        for x in (0, W - 1):
            if not 10 <= z <= 14: b.set(x, 10, z, 'minecraft:sea_lantern')
    b.set(12, 14, 12, 'minecraft:iron_chain'); b.set(12, 13, 12, 'minecraft:iron_chain')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_rave', 'bm.gvnew'])
    return b


def rest():
    b = Build(W, 16, D)
    b.fill(0, 0, 0, W - 1, FY - 1, D - 1, 'minecraft:dirt')
    b.room(0, FY, 0, W - 1, 15, D - 1, 'minecraft:spruce_planks', floor='minecraft:oak_planks', ceil='minecraft:dark_oak_planks')
    for x in range(1, W - 1):
        for z in (0, D - 1): b.set(x, 4, z, 'minecraft:stripped_spruce_log[axis=x]'); b.set(x, 9, z, 'minecraft:stripped_spruce_log[axis=x]')
    for z in range(1, D - 1):
        for x in (0, W - 1): b.set(x, 4, z, 'minecraft:stripped_spruce_log[axis=z]'); b.set(x, 9, z, 'minecraft:stripped_spruce_log[axis=z]')
    for y in range(4, 8):
        for z in (11, 12, 13):
            b.set(0, y, z, 'minecraft:air'); b.set(W - 1, y, z, 'minecraft:air')        # (the way on is open at once)
    for x in range(3, 22, 6):                                # ceiling beams, lanterns
        for z in range(1, D - 1): b.set(x, 14, z, 'minecraft:stripped_dark_oak_log[axis=z]')
        for z in (6, 18): b.set(x, 13, z, 'minecraft:lantern[hanging=true]')
    for x in range(9, 16):                                   # the hearth (north wall)
        for y in range(4, 10): b.set(x, y, 1, 'minecraft:bricks')
    for x in range(10, 15):
        for y in range(4, 7): b.set(x, y, 1, 'minecraft:air')
        b.set(x, 4, 1, 'minecraft:campfire[lit=true,signal_fire=false,waterlogged=false,facing=south]')
    for x in range(9, 16): b.set(x, 7, 2, 'minecraft:spruce_slab[type=bottom]')
    for (x, z) in ((5, 7), (5, 17), (19, 7), (19, 17)):     # tables and stools
        b.set(x, 4, z, 'minecraft:spruce_fence'); b.set(x, 5, z, 'minecraft:spruce_pressure_plate')
        for (dx, dz) in ((-1, 0), (1, 0)): b.set(x + dx, 4, z + dz, 'minecraft:spruce_trapdoor[half=top,facing=north,open=false]')
    for (x, z) in ((2, 2), (2, 3), (3, 2), (22, 2), (22, 22), (21, 22), (2, 22)):
        b.set(x, 4, z, 'minecraft:barrel[facing=up]')
    b.set(2, 5, 2, 'minecraft:barrel[facing=up]'); b.set(22, 5, 22, 'minecraft:barrel[facing=up]')
    for x in range(8, 17):
        for z in range(8, 17): b.set(x, 4, z, 'minecraft:red_carpet' if (x + z) % 5 else 'minecraft:orange_carpet')
    for z in (11, 12, 13):
        for x in range(1, 8): b.set(x, 4, z, 'minecraft:air')
        for x in range(17, 24): b.set(x, 4, z, 'minecraft:air')
    for (x, z) in ((20, 3), (21, 3), (20, 4)):               # the peddler's counter
        b.set(x, 4, z, 'minecraft:chiseled_bookshelf[facing=south]')
    b.set(12, 4, 21, 'minecraft:heavy_weighted_pressure_plate'); b.set(12, 3, 21, 'minecraft:emerald_block')   # (the Endless Vault's cash-out)
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_rest', 'bm.gvnew'])
    return b


def storm():
    b = shell()
    for (x, z) in STORM_PILLARS:                             # copper pillars with a lightning rod each, a lever on one face
        for y in range(4, 9): b.set(x, y, z, 'minecraft:waxed_copper_block')
        b.set(x, 9, z, 'minecraft:lightning_rod[facing=up]')
    for (x, y, z, face) in STORM_LEVERS:
        b.set(x, y, z, f'minecraft:lever[face=wall,facing={face},powered=false]')
    for x in range(1, W - 1):                                # puddles
        for z in range(1, D - 1):
            if (x * 7 + z * 13) % 11 == 0 and not 10 <= z <= 14: b.set(x, FY, z, 'minecraft:mud')
    for x in range(2, 23, 5):
        for z in range(2, 23, 5): b.set(x, 14, z, 'minecraft:tinted_glass')
    ctrl(b, 'storm'); return b


def ufo():
    b = shell()
    cx, cz = 12, 12
    for x in range(4, 21):                                   # the saucer's hull on stilts (y 8), a glass dome, a green underlight
        for z in range(4, 21):
            r2 = (x - cx) ** 2 + (z - cz) ** 2
            if r2 <= 64:
                b.set(x, 8, z, 'minecraft:light_gray_concrete' if r2 > 36 else 'minecraft:iron_block')
                if 36 < r2 <= 64 and (x + z) % 3 == 0: b.set(x, 7, z, 'minecraft:sea_lantern')
            if r2 <= 16: b.set(x, 9, z, 'minecraft:light_blue_stained_glass'); b.set(x, 7, z, 'minecraft:lime_stained_glass')
            if r2 <= 4: b.set(x, 10, z, 'minecraft:light_blue_stained_glass')
    for (x, z) in ((7, 7), (17, 7), (7, 17), (17, 17)):
        for y in range(4, 8): b.set(x, y, z, 'minecraft:iron_bars')
    for (x, z) in ((3, 20), (4, 21), (21, 3)):              # wreckage
        b.set(x, 4, z, 'minecraft:iron_trapdoor[half=bottom,facing=north,open=false]')
    for x in range(2, 23):
        for z in range(2, 23):
            if (x * 5 + z * 3) % 17 == 0: b.set(x, FY, z, 'minecraft:black_concrete_powder')
    ctrl(b, 'ufo'); return b


def grove():
    b = shell()
    rnd = random.Random(11)
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            b.set(x, FY, z, 'minecraft:moss_block' if (x + z) % 4 else 'minecraft:grass_block')
            if 10 <= z <= 14: continue
            r = rnd.random()
            if r < 0.10: b.set(x, 4, z, 'minecraft:firefly_bush')
            elif r < 0.25: b.set(x, 4, z, 'minecraft:moss_carpet')
            elif r < 0.32: b.set(x, 4, z, 'minecraft:pink_petals[facing=north,flower_amount=3]')
            elif r < 0.36: b.set(x, 4, z, 'minecraft:fern')
    for (tx, tz) in ((5, 5), (19, 6), (6, 19), (18, 18)):    # four old trees
        for y in range(4, 10): b.set(tx, y, tz, 'minecraft:oak_log[axis=y]')
        for dx in range(-3, 4):
            for dz in range(-3, 4):
                for y in (9, 10, 11):
                    if dx * dx + dz * dz + (y - 10) ** 2 * 2 <= 10 and 1 <= tx + dx <= 23 and 1 <= tz + dz <= 23 and (tx + dx, tz + dz) != (tx, tz):
                        b.set(tx + dx, y, tz + dz, 'minecraft:flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]' if rnd.random() < 0.4
                              else 'minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]')
    for x in range(9, 16):                                   # a moonlit pond
        for z in range(16, 21):
            if (x - 12) ** 2 / 9 + (z - 18) ** 2 / 4 <= 1: b.set(x, FY, z, 'minecraft:water'); b.set(x, 2, z, 'minecraft:sea_lantern')
    b.set(11, 4, 18, 'minecraft:lily_pad'); b.set(13, 4, 17, 'minecraft:lily_pad')
    ctrl(b, 'grove'); return b


BUILDERS = {'lamps': lamps, 'lightsout': lightsout, 'tumbler': tumbler, 'climb': climb, 'rafters': rafters,
            'ambush': ambush, 'pit': pit, 'rave': rave, 'rest': rest, 'storm': storm, 'ufo': ufo, 'grove': grove}
NAMES = {'lamps': 'The Signal Lamps', 'lightsout': 'The Lamp Floor', 'tumbler': 'The Tumbler Lock', 'climb': 'The Bell Tower',
         'rafters': 'The Crumbling Rafters', 'ambush': 'The Arcane Study', 'pit': "The Champion's Pit", 'rave': 'The Rat Rave',
         'rest': "The Rats' Rest", 'storm': 'The Storm Vault', 'ufo': 'The Vorn Landing', 'grove': 'The Enchanted Grove'}
