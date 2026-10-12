"""2.60: the Gilded Gutter Vault's rooms, as structure templates (built here, placed at runtime by phase70).

Every room is a 25 x 16 x 25 vault chamber: a blackstone-and-gold shell, the floor at y 3 (the stand height is 4), an
entry doorway in the west wall and an exit in the east wall (x 24, z 11-13, y 4-7) - closed with iron bars until the
room is beaten. Each holds one controller marker at (12.5, 4, 12.5) (tags bm.gvr, bm.gvr_<kind>, bm.gvnew); the
puzzle's movable parts (item frames, coffers, signs as text displays) are summoned around it when the run starts.
The vault room is longer (37): the guardian's hall, then the treasury behind a gold door."""
from structures import Build

W, H, D = 25, 16, 25
FY = 3                                       # floor block layer; players stand at y 4
CTRL = (12.5, 4, 12.5)
WALL, TRIM, PILLAR, FLOOR, CEIL = ('minecraft:polished_blackstone_bricks', 'minecraft:gilded_blackstone', 'minecraft:chiseled_polished_blackstone',
                                   'minecraft:polished_blackstone', 'minecraft:blackstone')
KINDS = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'guards', 'coffers']
NAMES = {'levers': 'The Combination Room', 'plates': 'The Weighing Room', 'lasers': 'The Gauntlet', 'tiles': 'The Tile Floor',
         'dial': 'The Dial Lock', 'guards': 'The Counting House', 'coffers': 'The Three Coffers', 'lobby': 'The Fixer\'s Den',
         'vault': 'The Vault', 'cache': 'The Clockwork Cache'}


def rel(x, y, z):
    """a block (local coords) relative to the controller marker - '~dx ~dy ~dz' (the block's centre for summons, its own cell for setblock)"""
    def f(v):
        return '~' if v == 0 else f'~{v:g}'
    return f'{f(x - 12)} {f(y - 4)} {f(z - 12)}'


def shell(length=W, exit_closed=True):
    b = Build(length, H, D)
    b.fill(0, 0, 0, length - 1, FY - 1, D - 1, 'minecraft:blackstone')
    b.room(0, FY, 0, length - 1, H - 1, D - 1, WALL, floor=FLOOR, ceil=CEIL)
    for x in range(1, length - 1):                       # a gilded band and a dark skirting round the walls
        for z in (0, D - 1):
            b.set(x, 9, z, TRIM); b.set(x, 4, z, 'minecraft:polished_blackstone')
    for z in range(1, D - 1):
        for x in (0, length - 1):
            b.set(x, 9, z, TRIM); b.set(x, 4, z, 'minecraft:polished_blackstone')
    for (x, z) in ((1, 1), (length - 2, 1), (1, D - 2), (length - 2, D - 2)):     # corner pillars, lanterns on chains
        b.fill(x, 4, z, x, 14, z, PILLAR)
    for x in range(4, length - 3, 6):
        for z in (6, 18):
            b.set(x, 14, z, 'minecraft:iron_chain'); b.set(x, 13, z, 'minecraft:lantern[hanging=true]')
    for x in range(1, length - 1):                       # a gold-edged floor runner from door to door
        b.set(x, FY, 10, 'minecraft:gilded_blackstone'); b.set(x, FY, 14, 'minecraft:gilded_blackstone')
        for z in (11, 12, 13):
            b.set(x, FY, z, 'minecraft:polished_blackstone_bricks')
    for y in range(4, 8):                                # doorways
        for z in (11, 12, 13):
            b.set(0, y, z, 'minecraft:air')
            b.set(length - 1, y, z, 'minecraft:iron_bars' if exit_closed else 'minecraft:air')
    for y in (4, 5, 6, 7, 8):                             # gold door frames
        for x in (0, length - 1):
            b.set(x, y, 10, 'minecraft:gold_block'); b.set(x, y, 14, 'minecraft:gold_block')
    for z in range(10, 15):
        b.set(0, 8, z, 'minecraft:gold_block'); b.set(length - 1, 8, z, 'minecraft:gold_block')
    for (x, z) in ((3, 3), (length - 4, 3), (3, D - 4), (length - 4, D - 4)):      # loot piles for the look of it
        b.set(x, 4, z, 'minecraft:raw_gold_block'); b.set(x + 1, 4, z, 'minecraft:gold_block'); b.set(x, 5, z, 'minecraft:yellow_carpet')
    return b


def ctrl(b, kind):
    b.marker(*CTRL, ['bm.gvr', f'bm.gvr_{kind}', 'bm.gvnew'])


def lobby():
    b = shell()
    for x in range(2, 8):                                # Goldtooth's counter
        b.set(x, 4, 19, 'minecraft:dark_oak_planks'); b.set(x, 5, 19, 'minecraft:dark_oak_slab')
    b.fill(9, 4, 2, 15, 4, 2, 'minecraft:dark_oak_planks')          # under the board
    b.set(23, 5, 15, 'minecraft:pale_oak_button[face=wall,facing=west]')   # "begin the heist"
    b.set(23, 5, 9, 'minecraft:pale_oak_button[face=wall,facing=west]')    # (and its twin, on the other side)
    for y in range(4, 7):                                # (2.67d) the Fixer's Door - the way out (phase103 fills the arch)
        b.set(1, y, 3, 'minecraft:gold_block'); b.set(1, y, 5, 'minecraft:gold_block')
    for z in (3, 4, 5):
        b.set(1, 7, z, 'minecraft:gold_block')
    for y in range(4, 7):                                # the clockwork door (to the secret cache, north)
        for x in (11, 12, 13):
            b.set(x, y, 0, 'minecraft:waxed_oxidized_copper')
    b.set(10, 5, 1, 'minecraft:waxed_copper_bulb[lit=true]'); b.set(14, 5, 1, 'minecraft:waxed_copper_bulb[lit=true]')
    ctrl(b, 'lobby')
    return b


def levers():
    b = shell()
    for x in (8, 10, 12, 14, 16):
        b.set(x, 5, 23, 'minecraft:lever[face=wall,facing=north,powered=false]')
        b.set(x, 4, 23, 'minecraft:gold_block')
    b.set(12, 7, 23, 'minecraft:pale_oak_button[face=wall,facing=north]')
    for x in range(7, 18):                               # the ledger wall
        b.set(x, 5, 1, 'minecraft:dark_oak_planks'); b.set(x, 7, 1, 'minecraft:dark_oak_planks')
    ctrl(b, 'levers'); return b


def plates():
    b = shell()
    for (x, z) in ((5, 5), (19, 5), (5, 19), (19, 19)):
        b.set(x, 3, z, 'minecraft:gold_block'); b.set(x, 4, z, 'minecraft:light_weighted_pressure_plate')
        for (dx, dz) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            b.set(x + dx, 3, z + dz, 'minecraft:gilded_blackstone')
    ctrl(b, 'plates'); return b


def lasers():
    b = shell()
    for x in range(1, 24):                               # a corridor, z 6..18, between laser emitters
        for y in range(4, 15):
            for z in list(range(1, 6)) + list(range(19, 24)):
                b.set(x, y, z, WALL)
    for x in (5, 9, 13, 17, 21):
        for y in (4, 5, 6):
            b.set(x, y, 5, 'minecraft:redstone_lamp[lit=true]'); b.set(x, y, 19, 'minecraft:redstone_lamp[lit=true]')
    b.set(22, 3, 12, 'minecraft:gold_block'); b.set(22, 4, 12, 'minecraft:light_weighted_pressure_plate')
    for x in range(4, 22, 4):
        b.set(x, 14, 12, 'minecraft:iron_chain'); b.set(x, 13, 12, 'minecraft:lantern[hanging=true]')
    ctrl(b, 'lasers'); return b


def tiles():
    b = shell()
    for x in range(3, 21):                               # the grid over a coin pit
        for z in range(5, 20):
            c, r = (x - 3) // 3, (z - 5) // 3
            b.set(x, FY, z, 'minecraft:polished_blackstone' if (c + r) % 2 == 0 else 'minecraft:gilded_blackstone')
            b.set(x, 2, z, 'minecraft:air'); b.set(x, 1, z, 'minecraft:air'); b.set(x, 0, z, 'minecraft:hay_block')
    for z in range(5, 20):
        b.set(1, FY, z, 'minecraft:gold_block'); b.set(2, FY, z, 'minecraft:gold_block')
        b.set(21, FY, z, 'minecraft:gold_block'); b.set(22, FY, z, 'minecraft:gold_block'); b.set(23, FY, z, 'minecraft:gold_block')
    b.set(1, 5, 9, 'minecraft:pale_oak_button[face=wall,facing=east]')     # peek
    ctrl(b, 'tiles'); return b


def dial():
    b = shell()
    for x in range(8, 17):
        for y in range(4, 10):
            b.set(x, y, 23, 'minecraft:dark_oak_planks')
    for x in (10, 12, 14):
        b.set(x, 5, 23, 'minecraft:gold_block')
    ctrl(b, 'dial'); return b


def guards():
    b = shell()
    for x in range(6, 19, 4):                            # counting tables
        for z in (6, 18):
            b.set(x, 4, z, 'minecraft:dark_oak_fence'); b.set(x, 5, z, 'minecraft:dark_oak_pressure_plate')
            b.set(x + 1, 4, z, 'minecraft:gold_block')
    ctrl(b, 'guards'); return b


def coffers():
    b = shell()
    for z in (6, 10, 14, 18):
        b.set(19, 4, z, 'minecraft:chiseled_polished_blackstone')
        b.set(19, 3, z, 'minecraft:gold_block')
    for x in range(3, 8):
        for y in range(4, 9):
            b.set(x, y, 23, 'minecraft:dark_oak_planks')
    ctrl(b, 'coffers'); return b


VAULT_LEN = 37


def vault():
    b = shell(VAULT_LEN, exit_closed=False)
    for z in range(1, D - 1):                            # the gold door between the hall and the treasury (x 24)
        for y in range(4, 15):
            b.set(24, y, z, WALL)
    for z in range(9, 16):
        for y in range(4, 9):
            b.set(24, y, z, 'minecraft:gold_block')
    for y in range(4, 8):                                # (the far wall is solid: the way out is the Fixer's Door)
        for z in (11, 12, 13):
            b.set(VAULT_LEN - 1, y, z, WALL)
    for x in range(26, VAULT_LEN - 1):                   # the treasury: gold underfoot, piles everywhere
        for z in range(1, D - 1):
            b.set(x, FY, z, 'minecraft:gold_block' if (x + z) % 3 else 'minecraft:raw_gold_block')
    for (x, z) in ((27, 3), (33, 3), (27, 21), (33, 21), (35, 8), (35, 16)):
        b.fill(x, 4, z, x + 1, 5, z + 1, 'minecraft:gold_block'); b.set(x, 6, z, 'minecraft:raw_gold_block')
    for z in range(7, 18, 2):                            # the strongbox ring: six gold plates round the grand strongbox
        pass
    ring = [(28, 9), (28, 15), (30, 7), (30, 17), (32, 9), (32, 15)]
    for (x, z) in ring:
        b.set(x, 4, z, 'minecraft:light_weighted_pressure_plate')
    b.set(30, 4, 12, 'minecraft:gold_block')
    for y in range(4, 7):                                # (2.67d) the Fixer's Door against the far wall - the way out, once the vault opens
        b.set(35, y, 11, 'minecraft:gold_block'); b.set(35, y, 13, 'minecraft:gold_block')
    for z in (11, 12, 13):
        b.set(35, 7, z, 'minecraft:gold_block')
    b.marker(*CTRL, ['bm.gvr', 'bm.gvr_vault', 'bm.gvnew'])
    return b


RING = [(28, 9), (28, 15), (30, 7), (30, 17), (32, 9), (32, 15)]


def cache():
    b = shell(exit_closed=False)
    for y in range(4, 8):                                # (its way in is the south wall, z 24 - from the lobby's north door)
        for z in (11, 12, 13):
            b.set(0, y, z, WALL); b.set(W - 1, y, z, WALL)
    for y in range(4, 7):
        for x in (11, 12, 13):
            b.set(x, y, D - 1, 'minecraft:air')
    for x in range(4, 21, 2):
        b.set(x, 4, 4, 'minecraft:waxed_copper_bulb[lit=true]')
    for (x, z) in ((6, 10), (18, 10), (6, 16), (18, 16)):
        b.set(x, 4, z, 'minecraft:chiseled_copper')
    b.marker(*CTRL, ['bm.gvr', 'bm.gvr_cache', 'bm.gvnew'])
    return b


BUILDERS = {'lobby': lobby, 'levers': levers, 'plates': plates, 'lasers': lasers, 'tiles': tiles, 'dial': dial, 'guards': guards,
            'coffers': coffers, 'vault': vault, 'cache': cache}


def export_all(path):
    out = {}
    for nm, f in BUILDERS.items():
        out[nm] = f().export(path(nm))
    return out
