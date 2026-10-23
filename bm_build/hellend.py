"""2.91: the Nether and the End's new places (structure templates; the datapack side is phase200).

THE EMBER RAT'S OUTPOST - a Black Market branch in the Nether: a little nether-brick fort, red battlements and corner towers,
  the Ember Rat's stall under a crimson awning, a lava font, a charged respawn anchor. A shelter in an Eruption.
THE COLOSSUS'S FORGE - a lava temple: a gate hall (blaze cages in its alcoves), a bridge over a lava moat, and the round Forge
  Heart - a ring of basalt pillars veined with magma round the dais of the Great Anvil, where the Magma Colossus is woken.
THE VOID RAT'S OUTPOST - a purpur-and-obsidian stall on its own island of end stone, floating; an ender chest, end rods.
THE VOIDWALKER'S OBSERVATORY - a shattered observatory adrift in the void: a round floor of obsidian and purpur, its dome
  broken open, a great telescope still trained on the stars, and on a pedestal of crying obsidian, his Starless Eye.

Each template's floor is FLOOR (walk FLOOR+1); its core marker stands at the middle of that floor. Everything in each box is set
(air included), so a template carves its own space out of whatever it lands in."""
import math
import random

from structures import Build

STAIR = lambda m, f, half='bottom': f'{m}_stairs[facing={f},half={half},shape=straight,waterlogged=false]'
LANT = lambda soul=False, hang=False: f'{"soul_" if soul else ""}lantern[hanging={"true" if hang else "false"},waterlogged=false]'


def _air(B):
    sx, sy, sz = B.size
    B.fill(0, 0, 0, sx - 1, sy - 1, sz - 1, 'air')


# ------------------------------------------------------------------------------------------------ the Ember Rat's Outpost
EO = dict(SX=23, SY=14, SZ=23, FLOOR=2)


def ember_outpost():
    SX, SY, SZ, FL = EO['SX'], EO['SY'], EO['SZ'], EO['FLOOR']
    B = Build(SX, SY, SZ); _air(B)
    rnd = random.Random(2911)
    S = B.set
    brick = lambda: rnd.choice(['nether_bricks'] * 6 + ['cracked_nether_bricks', 'chiseled_nether_bricks'])
    for x in range(SX):
        for z in range(SZ):
            for y in range(FL):
                S(x, y, z, 'blackstone' if y else 'basalt[axis=y]')
            S(x, FL, z, 'red_nether_bricks' if x in (1, SX - 2) or z in (1, SZ - 2) else 'polished_blackstone_bricks')
    # the walls (a gate in the south), battlements, corner towers with lanterns on top
    for x in range(1, SX - 1):
        for z in range(1, SZ - 1):
            if not (x in (1, SX - 2) or z in (1, SZ - 2)): continue
            for y in range(FL + 1, FL + 6):
                S(x, y, z, brick())
            if (x + z) % 2 == 0: S(x, FL + 6, z, 'nether_brick_wall')
    for x in (10, 11, 12):
        for y in range(FL + 1, FL + 4):
            S(x, y, SZ - 2, 'air')
    S(10, FL + 4, SZ - 2, STAIR('nether_brick', 'east', 'top')); S(12, FL + 4, SZ - 2, STAIR('nether_brick', 'west', 'top'))
    for (cx, cz) in ((1, 1), (SX - 4, 1), (1, SZ - 4), (SX - 4, SZ - 4)):
        for x in range(cx, cx + 3):
            for z in range(cz, cz + 3):
                for y in range(FL + 1, FL + 9):
                    S(x, y, z, 'red_nether_bricks' if y in (FL + 7,) else brick())
                S(x, FL + 9, z, 'nether_brick_fence' if (x + z) % 2 else 'nether_bricks')
        S(cx + 1, FL + 10, cz + 1, 'shroomlight')
    # the stall: a red counter under a crimson awning, the rat behind it; barrels of stock; a sign
    for x in range(7, 16):
        S(x, FL + 1, 8, 'red_nether_brick_slab[type=top,waterlogged=false]' if x not in (7, 15) else 'red_nether_bricks')
        S(x, FL + 4, 6, 'crimson_planks'); S(x, FL + 4, 7, 'crimson_slab[type=bottom,waterlogged=false]'); S(x, FL + 4, 8, 'crimson_slab[type=bottom,waterlogged=false]')
    for x in (7, 15):
        for y in range(FL + 1, FL + 4):
            S(x, y, 6, 'crimson_stem[axis=y]')
    for x in (8, 9, 13, 14):
        S(x, FL + 1, 5, 'barrel[facing=up,open=false]')
    S(12, FL + 1, 5, 'chest[facing=south,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p200_outpost'})
    B.sign(11, FL + 2, 9, 'crimson_wall_sign[facing=south,waterlogged=false]' if False else 'crimson_sign[rotation=0,waterlogged=false]',
           ['BLACK MARKET', '- Ember Branch -', 'scales welcome', 'no refunds'], color='orange')
    S(11, FL + 1, 9, 'red_nether_bricks')
    S(10, FL + 3, 7, LANT(hang=True) if False else 'air'); S(9, FL + 3, 6, 'air')
    S(9, FL + 3, 7, 'lantern[hanging=true,waterlogged=false]'); S(13, FL + 3, 7, 'lantern[hanging=true,waterlogged=false]')
    # the yard: a lava font, a charged respawn anchor (a safe place to wake up in the Nether), lamps
    S(5, FL + 1, 15, 'polished_blackstone'); S(5, FL + 2, 15, 'lava_cauldron')
    S(17, FL + 1, 15, 'respawn_anchor[charges=4]')
    for (x, z) in ((4, 10), (18, 10), (6, 18), (16, 18)):
        S(x, FL + 1, z, 'nether_brick_fence'); S(x, FL + 2, z, 'nether_brick_fence'); S(x, FL + 3, z, 'lantern[hanging=false,waterlogged=false]')
    B.marker(11.5, FL + 1, 7.5, ['bm.onew', 'bm.ocore', 'bm.oember'], 0)                 # the rat's spot behind the counter (faces south)
    return B


# ------------------------------------------------------------------------------------------------ the Colossus's Forge
CF = dict(SX=41, SY=24, SZ=47, FLOOR=2)
CF_HEART = (20, 27)              # the Forge Heart's middle (x, z): the Great Anvil


def colossus_forge():
    SX, SY, SZ, FL = CF['SX'], CF['SY'], CF['SZ'], CF['FLOOR']
    B = Build(SX, SY, SZ); _air(B)
    rnd = random.Random(2912)
    S = B.set
    hx, hz = CF_HEART
    wall = lambda: rnd.choice(['blackstone'] * 4 + ['polished_blackstone_bricks', 'cracked_polished_blackstone_bricks', 'basalt[axis=y]', 'gilded_blackstone' if rnd.random() < 0.08 else 'blackstone'])
    # the whole box: a shell of blackstone; the floor; the ceiling
    for x in range(SX):
        for z in range(SZ):
            for y in range(FL + 1):
                S(x, y, z, 'blackstone' if y < FL else 'polished_blackstone')
            S(x, SY - 1, z, wall())
    for y in range(FL + 1, SY - 1):
        for x in range(SX):
            S(x, y, 0, wall()); S(x, y, SZ - 1, wall())
        for z in range(SZ):
            S(0, y, z, wall()); S(SX - 1, y, z, wall())
    # the Forge Heart: a round hall (radius 18), the lava moat (radius 14..16) and its island
    for x in range(1, SX - 1):
        for z in range(9, SZ - 1):
            r = math.hypot(x - hx, z - hz)
            if r > 18.5:
                for y in range(FL + 1, SY - 1): S(x, y, z, wall())
                continue
            if 14 <= r <= 16.2 and not (abs(x - hx) <= 2 and z < hz):
                S(x, FL, z, 'lava'); S(x, FL - 1, z, 'magma_block')
            elif r < 14:
                S(x, FL, z, 'polished_blackstone_bricks' if (x + z) % 2 else 'polished_blackstone')
    # the bridge (north) and the gate hall (z 0..9), with blaze cages in its alcoves and chests in its side rooms
    for z in range(1, 12):
        for x in range(hx - 2, hx + 3):
            S(x, FL, z, 'polished_blackstone_bricks')
            for y in range(FL + 1, FL + 6): S(x, y, z, 'air')
        for x in (hx - 3, hx + 3):
            for y in range(FL + 1, FL + 6): S(x, y, z, wall())
        for x in range(hx - 3, hx + 4):
            S(x, FL + 6, z, wall())
    for x in range(hx - 1, hx + 2):                                       # the gate (north face)
        for y in range(FL + 1, FL + 4): S(x, y, 0, 'air')
    S(hx, FL + 4, 0, 'air')
    for (ax, side) in ((hx - 4, -1), (hx + 4, 1)):                       # alcoves with blaze cages
        for z in (4, 7):
            S(ax, FL + 1, z, 'spawner', {'id': 'minecraft:mob_spawner', 'SpawnData': {'entity': {'id': 'minecraft:blaze'}},
                                          'SpawnCount': 2, 'MaxNearbyEntities': 4, 'RequiredPlayerRange': 12, 'Delay': 40})
            S(ax - side * 0, FL + 2, z, 'iron_bars')
            S(hx + side * 3, FL + 1, z, 'air'); S(hx + side * 3, FL + 2, z, 'iron_bars')
    for (cx, face) in ((hx - 5, 'east'), (hx + 5, 'west')):              # side vaults with a chest each
        S(cx, FL + 1, 10, 'chest[facing=%s,type=single,waterlogged=false]' % face, {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p200_forge'})
        S(cx + (1 if face == 'east' else -1), FL + 1, 10, 'air'); S(cx + (1 if face == 'east' else -1), FL + 2, 10, 'air')
        S(hx + (-3 if face == 'east' else 3), FL + 1, 10, 'air'); S(hx + (-3 if face == 'east' else 3), FL + 2, 10, 'air')
    # the pillars: eight, basalt veined with magma, round the island
    for i in range(8):
        a = 2 * math.pi * i / 8 + math.pi / 8
        px, pz = round(hx + 10 * math.sin(a)), round(hz + 10 * math.cos(a))
        for y in range(FL + 1, SY - 1):
            for dx in (0, 1):
                for dz in (0, 1):
                    S(px + dx, y, pz + dz, 'magma_block' if (y + i) % 5 == 0 else 'polished_basalt[axis=y]')
        S(px, FL + 4, pz - 1, 'soul_lantern[hanging=false,waterlogged=false]' if False else 'air')
    # the dais and the Great Anvil: steps, an anvil, blast furnaces glowing, a ring of lava cauldrons
    for x in range(hx - 4, hx + 5):
        for z in range(hz - 4, hz + 5):
            r = math.hypot(x - hx, z - hz)
            if r <= 4.5: S(x, FL + 1, z, 'polished_blackstone_bricks' if r > 3.2 else 'gilded_blackstone')
            if r <= 2.4: S(x, FL + 2, z, 'polished_blackstone')
    S(hx, FL + 3, hz, 'anvil[facing=north]'); S(hx - 1, FL + 3, hz + 1, 'blast_furnace[facing=north,lit=true]'); S(hx + 1, FL + 3, hz + 1, 'blast_furnace[facing=north,lit=true]')
    S(hx - 1, FL + 3, hz - 1, 'smithing_table'); S(hx + 1, FL + 3, hz - 1, 'lava_cauldron')
    for (x, z) in ((hx - 4, hz), (hx + 4, hz), (hx, hz + 4)):
        S(x, FL + 2, z, 'lava_cauldron')
    # light: shroomlight veins in the ceiling, soul lanterns hung on chains
    for x in range(4, SX - 4, 6):
        for z in range(12, SZ - 3, 6):
            if math.hypot(x - hx, z - hz) < 17:
                S(x, SY - 1, z, 'shroomlight')
                S(x, SY - 2, z, 'iron_chain[axis=y,waterlogged=false]'); S(x, SY - 3, z, LANT(soul=True, hang=True))
    B.marker(hx + 0.5, FL + 3, hz - 2.5, ['bm.cfnew', 'bm.fcore'], 180)                   # in front of the anvil
    return B


# ------------------------------------------------------------------------------------------------ the Void Rat's Outpost
VO = dict(SX=25, SY=20, SZ=25, FLOOR=9)


def void_outpost():
    SX, SY, SZ, FL = VO['SX'], VO['SY'], VO['SZ'], VO['FLOOR']
    B = Build(SX, SY, SZ)
    rnd = random.Random(2913)
    S = B.set
    cx, cz = 12, 12
    # the island under it: a rough cone of end stone hanging below the floor
    for x in range(SX):
        for z in range(SZ):
            r = math.hypot(x - cx, z - cz)
            if r > 11.8: continue
            depth = int((11.8 - r) * 0.8 + rnd.random() * 1.5)
            for y in range(max(0, FL - depth), FL):
                S(x, y, z, 'end_stone')
            S(x, FL, z, 'purpur_block' if r < 8.5 else 'end_stone_bricks' if r < 10.5 else 'end_stone')
            for y in range(FL + 1, SY): S(x, y, z, 'air')
    # the stall: purpur pillars, an obsidian back wall, a purpur-slab roof; end rods for light
    for x in range(7, 18):
        S(x, FL + 1, 9, 'purpur_slab[type=top,waterlogged=false]' if x not in (7, 17) else 'purpur_pillar[axis=y]')
        for y in range(FL + 1, FL + 5): S(x, y, 6, 'obsidian' if (x + y) % 3 else 'crying_obsidian')
        S(x, FL + 5, 6, 'purpur_block')
        for z in (7, 8, 9): S(x, FL + 5, z, 'purpur_slab[type=bottom,waterlogged=false]')
    for (x, z) in ((7, 9), (17, 9), (7, 6), (17, 6)):
        for y in range(FL + 1, FL + 5): S(x, y, z, 'purpur_pillar[axis=y]')
    S(10, FL + 4, 8, 'end_rod[facing=down]'); S(14, FL + 4, 8, 'end_rod[facing=down]')
    S(9, FL + 1, 7, 'ender_chest[facing=south,waterlogged=false]')
    S(15, FL + 1, 7, 'chest[facing=south,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p200_void'})
    S(12, FL + 1, 10, 'purpur_block')
    B.sign(12, FL + 2, 10, 'birch_sign[rotation=0,waterlogged=false]', ['BLACK MARKET', '- Void Branch -', 'shards welcome', 'mind the edge'], color='purple')
    # a ring of end rods round the rim (a beacon to find it by), a little rift-anchor pillar
    for i in range(10):
        a = 2 * math.pi * i / 10
        x, z = round(cx + 9.5 * math.sin(a)), round(cz + 9.5 * math.cos(a))
        S(x, FL + 1, z, 'end_rod[facing=up]')
    for y in range(FL + 1, FL + 4): S(cx, y, 17, 'purpur_pillar[axis=y]')
    S(cx, FL + 4, 17, 'crying_obsidian')
    B.marker(12.5, FL + 1, 7.5, ['bm.onew', 'bm.ocore', 'bm.ovoid'], 0)
    return B


# ------------------------------------------------------------------------------------------------ the Voidwalker's Observatory
OB = dict(SX=31, SY=26, SZ=31, FLOOR=6)


def observatory():
    SX, SY, SZ, FL = OB['SX'], OB['SY'], OB['SZ'], OB['FLOOR']
    B = Build(SX, SY, SZ)
    rnd = random.Random(2914)
    S = B.set
    cx, cz = 15, 15
    R = 11
    # the floor: a round slab of obsidian and purpur, broken at the edges, a little rock under it
    for x in range(SX):
        for z in range(SZ):
            r = math.hypot(x - cx, z - cz)
            if r > R + 0.5: continue
            if r > R - 1.5 and rnd.random() < 0.35: continue                  # the broken rim
            S(x, FL, z, 'obsidian' if (int(r) % 3 == 0) else 'purpur_block')
            for y in range(max(0, FL - int((R - r) * 0.5) - 1), FL): S(x, y, z, 'end_stone')
            for y in range(FL + 1, SY): S(x, y, z, 'air')
    # the shattered dome: a shell of purpur and obsidian ribs, most of it fallen away
    for x in range(SX):
        for z in range(SZ):
            for y in range(FL + 1, SY - 1):
                d = math.sqrt((x - cx) ** 2 + ((y - FL) * 1.1) ** 2 + (z - cz) ** 2)
                if R - 0.6 <= d <= R + 0.4:
                    ang = math.atan2(z - cz, x - cx)
                    rib = abs(math.sin(ang * 4)) < 0.18
                    keep = (rib and rnd.random() < 0.8) or (y < FL + 4 and rnd.random() < 0.4) or (ang > 1.2 and ang < 2.4 and y < FL + 8 and rnd.random() < 0.5)
                    if keep: S(x, y, z, 'obsidian' if rib else 'purpur_block')
    # the telescope: a tube of polished blackstone and copper, trained up through the hole, on a tripod
    tx, tz = cx + 3, cz - 2
    for (dx, dz) in ((-1, -1), (1, -1), (0, 1)):
        S(tx + dx, FL + 1, tz + dz, 'polished_blackstone_wall')
    S(tx, FL + 2, tz, 'polished_blackstone')
    for i in range(6):
        S(tx + (i // 2), FL + 3 + i, tz - (i // 3), 'waxed_copper_block' if i in (0, 5) else 'polished_blackstone_bricks')
    S(tx + 3, FL + 9, tz - 2, 'end_rod[facing=up]')
    # the pedestal (his Starless Eye), crying obsidian and end stone bricks; scattered books and broken glass
    px, pz = cx - 3, cz + 3
    S(px, FL + 1, pz, 'end_stone_bricks'); S(px, FL + 2, pz, 'crying_obsidian')
    for (x, z) in ((px - 1, pz), (px + 1, pz), (px, pz - 1), (px, pz + 1)):
        S(x, FL + 1, z, 'end_stone_brick_stairs[facing=%s,half=bottom,shape=straight,waterlogged=false]' % (
            'east' if x < px else 'west' if x > px else 'south' if z < pz else 'north'))
    S(cx, FL + 1, cz - 6, 'lectern[facing=south,has_book=false,powered=false]')
    S(cx - 5, FL + 1, cz - 3, 'chest[facing=east,type=single,waterlogged=false]', {'id': 'minecraft:chest', 'LootTable': 'bm:chests/p200_observatory'})
    for (x, z) in ((cx + 6, cz + 3), (cx - 2, cz - 7), (cx + 1, cz + 7)):
        S(x, FL + 1, z, 'purple_stained_glass_pane')
    for (x, z) in ((cx - 7, cz), (cx + 7, cz), (cx, cz + 8)):
        S(x, FL + 1, z, 'end_rod[facing=up]')
    # debris adrift round it: lumps of purpur and obsidian hanging in the void
    for _ in range(9):
        a = rnd.random() * 2 * math.pi
        r = rnd.uniform(12.5, 14.5)
        x, z = int(cx + r * math.cos(a)), int(cz + r * math.sin(a))
        y = FL + rnd.randint(-3, 10)
        if 0 <= x < SX and 0 <= z < SZ and 0 <= y < SY:
            for dx, dy, dz in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)):
                if rnd.random() < 0.75 and 0 <= x + dx < SX and 0 <= y + dy < SY and 0 <= z + dz < SZ:
                    S(x + dx, y + dy, z + dz, rnd.choice(['purpur_block', 'obsidian', 'end_stone', 'purpur_pillar[axis=y]']))
    B.marker(cx + 0.5, FL + 1, cz + 0.5, ['bm.obnew', 'bm.vcore'], 0)
    B.marker(px + 0.5, FL + 3, pz + 0.5, ['bm.vspot', 'bm.vspot_eye'], 0)
    B.marker(tx + 0.5, FL + 1, tz + 0.5, ['bm.vspot', 'bm.vspot_scope'], 0)
    return B


if __name__ == '__main__':
    for f in (ember_outpost, colossus_forge, void_outpost, observatory):
        B = f()
        print(f.__name__, B.size, len(B.b))
