"""2.82: OMEGA PALACE - King Omega's haunted castle (a structure template; the datapack side is phase169).

From the owner's comics: a grey stone-brick castle on a rise in a dark wood - black pointed spires, yellow windows, a tall
central tower over the door with two round windows crossed like a cross-hairs, cracked walls and creepers of vine, a dead tree
and a dirt path up to the door; soul wisps drifting round the towers.
INSIDE (the reference panel): a tall white hall - white pillars down both sides, dark arched doorways between them, a pale
tiled floor, a round purple rug, and at the back two flights of purple stairs up to a landing with a railing, a great arched
wooden door, and three banners over it - purple, gold-edged, the Omega sign. Beyond the door, raised: the THRONE ROOM and
his TOMB - a black sarcophagus ringed by six socketed pedestals (one for each Conquest Emblem), his throne behind it.
The wings: the west is the library (ground) and Cecil's room (up the stair - "I'll show them to their rooms"); the east,
the dining hall and Pistachio's kitchen (ground) and the guest rooms (up).

Template coordinates: x 0..SX-1, y 0..SY-1, z 0..SZ-1; the door faces north (-z) - you come up the path from z=0. The floor
is y=FY everywhere outside (walk FY+1); the throne room's floor is TY (walk TY+1), up the stairs. Everything above the
floor in the box is set (air where empty), so the wood it lands in is cleared; below it, the foundation."""
import math
import random

from structures import Build
from nbt import Int, Float, Double

SX, SY, SZ = 66, 52, 78
FY = 5                                   # the floor (walk FY+1)
TY = FY + 7                              # the throne room's floor (walk TY+1)
HALL = (20, 45, 12, 44)                  # the hall's walls: x0, x1, z0, z1 (inside x21..44, z13..43)
THRONE = (16, 49, 45, 72)                # the throne room's walls (inside x17..48, z46..71)
TOMB = (32.5, TY + 1, 58.5)              # the sarcophagus's middle (walk height)
SPAWN = (32.5, TY + 1, 65.0)             # where he crawls up out of the floor (between the tomb and his throne)
THRONE_AT = (32.5, TY + 1, 67.5)         # where the King holds court, once he is at peace
ARRIVE = (32.5, TY + 1, 48.5)            # just inside the great door
CENTER = (32.5, FY + 1, 28.5)            # the hall's middle (the palace's marker)
EMBLEMS = ('brood', 'frost', 'tide', 'hex', 'keep', 'hollow')
SOCKET_R = 5.0


def socket_pos(i):
    """the six pedestals round the tomb (i = 0..5, in EMBLEMS order): a ring, the first due north (toward the door)"""
    a = math.radians(180 + 60 * i)
    return (TOMB[0] + SOCKET_R * math.sin(a), TY + 2, TOMB[2] + SOCKET_R * math.cos(a))


STAIR = lambda m, f, half='bottom': f'{m}_stairs[facing={f},half={half},shape=straight,waterlogged=false]'
LANT = lambda hang=True, soul=False: f'{"soul_" if soul else ""}lantern[hanging={"true" if hang else "false"},waterlogged=false]'
CHAIN = 'iron_chain[axis=y,waterlogged=false]'


def build():
    B = Build(SX, SY, SZ)
    rnd = random.Random(8200)
    S = B.set
    get = B.get
    WALL = [('stone_bricks', 10), ('cracked_stone_bricks', 3), ('mossy_stone_bricks', 2), ('andesite', 1), ('polished_andesite', 1)]
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]

    # ---------------------------------------------------------------- the ground: foundation below, the floor, air above
    for x in range(SX):
        for z in range(SZ):
            for y in range(0, FY):
                S(x, y, z, 'stone' if y < FY - 2 else 'dirt')
            S(x, FY, z, rnd.choice(['grass_block[snowy=false]'] * 5 + ['podzol[snowy=false]', 'coarse_dirt']))
            for y in range(FY + 1, SY):
                S(x, y, z, 'air')

    def wall_box(x0, x1, z0, z1, y0, y1, fill_inside='air', floor=None):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = x in (x0, x1) or z in (z0, z1)
                for y in range(y0, y1 + 1):
                    S(x, y, z, pick(WALL) if edge else fill_inside)
                if floor and not edge: S(x, y0, z, floor)

    def round_tower(cx, cz, r, y0, y1, spire_h):
        S = lambda x, y, z, st: B.set(x, y, z, st) if 0 <= x < SX and 0 <= z < SZ else None
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
                if d <= r:
                    for y in range(y0, y1 + 1):
                        S(x, y, z, pick(WALL) if d > r - 1.2 else 'air')
                    S(x, y0, z, 'polished_andesite')
                    S(x, y1, z, 'stone_bricks')
                    if d <= r - 1.2: S(x, FY + 7, z, 'spruce_planks')            # (its upper floor, level with the wings')
        # windows: glowing yellow slits up the tower
        for k, a in enumerate(range(0, 360, 90)):
            wx, wz = int(round(cx - 0.5 + (r - 0.4) * math.cos(math.radians(a + 45)))), int(round(cz - 0.5 + (r - 0.4) * math.sin(math.radians(a + 45))))
            for y in range(y0 + 4, y1 - 2, 6):
                if get(wx, y, wz) not in (None, 'minecraft:air'):
                    S(wx, y, wz, 'ochre_froglight[axis=y]'); S(wx, y + 1, wz, 'ochre_froglight[axis=y]')
        # the spire: a black cone, a stair rim, a dark tip
        for h in range(spire_h):
            rr = (r + 0.8) * (1 - h / spire_h)
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                for z in range(int(cz - r - 2), int(cz + r + 3)):
                    d = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
                    if d <= rr and (d > rr - 1.5 or h == 0):
                        S(x, y1 + 1 + h, z, 'deepslate_tiles' if (x + z + h) % 5 else 'blackstone')
        S(int(cx), y1 + 1 + spire_h, int(cz), 'polished_blackstone_wall')

    # ---------------------------------------------------------------- the wings (two storeys, battlements)
    for (x0, x1) in ((4, 19), (46, 61)):
        wall_box(x0, x1, 12, 44, FY, FY + 14, floor='spruce_planks')
        for x in range(x0 + 1, x1):
            for z in range(13, 44):
                S(x, FY + 7, z, 'spruce_planks')                       # the upper floor
                S(x, FY + 14, z, 'stone_bricks')                      # the roof
        for x in range(x0, x1 + 1):                                   # battlements
            for z in range(12, 45):
                if x in (x0, x1) or z in (12, 44):
                    S(x, FY + 15, z, 'stone_brick_wall' if (x + z) % 2 else 'stone_bricks')
        # windows (yellow glass below, glowing above), on the outer and front walls
        for z in range(16, 43, 4):
            for (wx, y) in ((x0 if x0 == 4 else x1, FY + 3), (x0 if x0 == 4 else x1, FY + 10)):
                for dy in (0, 1):
                    S(wx, y + dy, z, 'yellow_stained_glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]' if y < FY + 6 else 'ochre_froglight[axis=y]')
        for x in range(x0 + 3, x1 - 1, 4):
            for y in (FY + 3, FY + 10):
                for dy in (0, 1):
                    S(x, y + dy, 12, 'yellow_stained_glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]' if y < FY + 6 else 'ochre_froglight[axis=y]')
    # ---------------------------------------------------------------- the great hall
    hx0, hx1, hz0, hz1 = HALL
    wall_box(hx0, hx1, hz0, hz1, FY, FY + 20)
    for x in range(hx0 + 1, hx1):
        for z in range(hz0 + 1, hz1):
            S(x, FY, z, 'smooth_quartz' if (x % 4 == 0 or z % 4 == 0) else 'polished_diorite')     # pale tiles, grout lines
            S(x, FY + 20, z, 'stone_bricks')
    # the gable roof over the hall: black tiles
    for h in range(0, 9):
        for z in range(hz0 - 1, hz1 + 2):
            for x in (hx0 - 1 + h, hx1 + 1 - h):
                if hx0 - 1 + h <= hx1 + 1 - h:
                    S(x, FY + 21 + h, z, STAIR('deepslate_tile', 'east' if x < 33 else 'west'))
            if hx0 + h < hx1 - h:
                for x in range(hx0 + h, hx1 - h + 1):
                    if get(x, FY + 21 + h, z) == 'minecraft:air' and h < 8: S(x, FY + 20 + h, z, 'deepslate_tiles')
    # the white pillars down both sides
    for px in (23, 42):
        for pz in (16, 21, 26, 31, 36):
            for y in range(FY + 1, FY + 20):
                S(px, y, pz, 'quartz_pillar[axis=y]')
            S(px, FY + 19, pz, 'chiseled_quartz_block')
            S(px, FY + 1, pz, 'smooth_quartz')
    # dark arched doorways into the wings, between the pillars
    for wx, step in ((hx0, 1), (hx1, -1), (hx0 - 1, 1), (hx1 + 1, -1)):          # (the hall's wall and the wing's own, side by side)
        for (za, zb) in ((18, 19), (28, 29)):
            for z in range(za - 1, zb + 2):
                for y in range(FY + 1, FY + 6):
                    inside = za <= z <= zb and y <= FY + 4
                    S(wx, y, z, 'air' if inside else ('polished_blackstone_bricks' if y <= FY + 5 else get(wx, y, z)))
            S(wx, FY + 5, za, 'polished_blackstone_brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]')
            S(wx, FY + 5, zb, 'polished_blackstone_brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]')
    # the round purple rug, and a runner from the door to the stairs
    for x in range(hx0 + 1, hx1):
        for z in range(hz0 + 1, hz1):
            if math.hypot(x + 0.5 - 32.5, z + 0.5 - 26.5) <= 5.3:
                S(x, FY + 1, z, 'purple_carpet')
    for x in (32, 33):
        for z in range(hz0 + 1, 34):
            S(x, FY + 1, z, 'purple_carpet')
    # ---- the stairs: a landing at the back (TY), a flight up each side; a railing; the great door
    for x in range(22, 44):
        for z in range(40, 44):
            for y in range(FY + 1, TY):
                S(x, y, z, 'polished_andesite')
            S(x, TY, z, 'polished_andesite' if (x + z) % 3 else 'smooth_stone')
    for fx in ((22, 23, 24), (41, 42, 43)):
        for k in range(7):                                   # 7 steps up from z 33 to the landing at z 40
            z = 33 + k
            for x in fx:
                for y in range(FY + 1, FY + 1 + k):
                    S(x, y, z, 'polished_andesite')
                S(x, FY + 1 + k, z, 'purpur_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]')
    for x in range(25, 41):                                   # the railing along the landing's front
        S(x, TY + 1, 40, 'iron_bars')
    for z in range(40, 44):
        S(21, TY + 1, z, 'iron_bars') if get(21, TY + 1, z) == 'minecraft:air' else None
    # (an arch under the landing - the pantry door, Pistachio's)
    for x in (32, 33):
        for y in (FY + 1, FY + 2):
            S(x, y, 40, 'air')
    S(32, FY + 1, 40, 'dark_oak_door[facing=north,half=lower,hinge=left,open=false,powered=false]')
    S(32, FY + 2, 40, 'dark_oak_door[facing=north,half=upper,hinge=left,open=false,powered=false]')
    S(33, FY + 1, 40, 'dark_oak_door[facing=north,half=lower,hinge=right,open=false,powered=false]')
    S(33, FY + 2, 40, 'dark_oak_door[facing=north,half=upper,hinge=right,open=false,powered=false]')
    for x in range(30, 36):
        for z in range(41, 44):
            for y in (FY + 1, FY + 2):
                S(x, y, z, 'air')
    S(30, FY + 1, 43, 'barrel[facing=up,open=false]'); S(35, FY + 1, 43, 'barrel[facing=up,open=false]'); S(34, FY + 1, 43, 'smoker[facing=north,lit=false]')
    S(31, FY + 1, 43, 'barrel[facing=up,open=false]'); S(30, FY + 2, 43, 'candle[candles=3,lit=true,waterlogged=false]')
    # the great door (an arch of dark wood through the back wall, onto the throne room)
    # (2.82c) the arch is cut to the doors - two wide, two high, a lintel over them; it was 4 x 4, and the 2 x 2 doors stood in it loose
    for x in range(30, 36):
        for y in range(TY + 1, TY + 7):
            S(x, y, hz1, 'spruce_planks' if not (32 <= x <= 33 and y <= TY + 2) else 'air')
    for x in range(31, 35):
        S(x, TY + 3, hz1, 'stripped_spruce_log[axis=x]')
    S(32, TY + 1, hz1, 'spruce_door[facing=south,half=lower,hinge=left,open=true,powered=false]')
    S(32, TY + 2, hz1, 'spruce_door[facing=south,half=upper,hinge=left,open=true,powered=false]')
    S(33, TY + 1, hz1, 'spruce_door[facing=south,half=lower,hinge=right,open=true,powered=false]')
    S(33, TY + 2, hz1, 'spruce_door[facing=south,half=upper,hinge=right,open=true,powered=false]')
    # light in the hall: chandeliers, lanterns on the pillars
    for (cx, cz) in ((32, 20), (32, 32)):
        for y in range(FY + 14, FY + 20): S(cx, y, cz, CHAIN)
        for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            S(cx + dx, FY + 13, cz + dz, 'polished_blackstone_wall' if (dx or dz) else 'gold_block')
            if dx or dz: S(cx + dx, FY + 12, cz + dz, LANT(True))
    for z in range(15, 42, 5):
        for x in (hx0 + 1, hx1 - 1):
            S(x, FY + 8, z, 'light[level=12,waterlogged=false]')
            S(x, FY + 3, z, 'light[level=10,waterlogged=false]')
    for x in range(24, 42, 4):
        for z in range(15, 40, 6):
            S(x, FY + 15, z, 'light[level=11,waterlogged=false]')
    # high windows in the hall's side walls (glowing)
    for wx in (hx0, hx1):
        for z in range(15, 43, 5):
            for y in range(FY + 10, FY + 15):
                if get(wx, y, z) not in ('minecraft:air',):
                    S(wx, y, z, 'ochre_froglight[axis=y]' if y in (FY + 11, FY + 12, FY + 13) else get(wx, y, z))

    # ---------------------------------------------------------------- the central tower over the door, with its round windows
    for x in range(26, 40):
        for z in range(7, 18):
            edge = x in (26, 39) or z in (7, 17)
            for y in range(FY, FY + 30):
                if edge: S(x, y, z, pick(WALL))
                elif y > FY: S(x, y, z, 'air' if y < FY + 29 else 'stone_bricks')
            if not edge: S(x, FY, z, 'smooth_quartz' if (x + z) % 2 else 'polished_diorite')
    for x in range(27, 39):                                  # the tower opens into the hall
        for y in range(FY + 1, FY + 10):
            S(x, y, 12, 'air') if 28 <= x <= 37 else None
            S(x, y, 17, 'air') if 28 <= x <= 37 else None
    # the door: an arch in the tower's front, and the path's end
    for x in range(30, 36):
        for y in range(FY + 1, FY + 7):
            arch = (x in (30, 35) and y >= FY + 5) or y == FY + 6
            S(x, y, 7, 'polished_blackstone_bricks' if arch else 'air')
    for (y0, cx) in ((FY + 14, 32.5), (FY + 23, 32.5)):         # the two round windows, crossed
        for x in range(28, 38):
            for y in range(y0 - 3, y0 + 4):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - (y0 + 0.5))
                if d <= 3.3:
                    cross = abs(x + 0.5 - cx) < 0.6 or abs(y + 0.5 - (y0 + 0.5)) < 0.6
                    S(x, y, 7, 'polished_andesite' if (cross or d > 2.7) else 'ochre_froglight[axis=y]')
    # the tower's spire
    for h in range(14):
        rr = 8.5 * (1 - h / 14)
        for x in range(24, 42):
            for z in range(5, 20):
                dx_, dz_ = abs(x + 0.5 - 33.0), abs(z + 0.5 - 12.5)
                d = max(dx_, dz_)
                if d <= rr and (d > rr - 1.5 or h == 0):
                    S(x, FY + 30 + h, z, 'deepslate_tiles' if (x + z + h) % 6 else 'blackstone')
    S(33, FY + 44, 12, 'polished_blackstone_wall')
    # the corner towers and their spires
    for (cx, cz) in ((4.5, 12.5), (61.5, 12.5), (4.5, 44.5), (61.5, 44.5)):        # (on the wings' outer corners)
        round_tower(cx, cz, 4.2, FY, FY + 22, 10)

    # ---------------------------------------------------------------- the throne room and the tomb (raised: up the stairs, through the door)
    tx0, tx1, tz0, tz1 = THRONE
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            edge = x in (tx0, tx1) or z in (tz0, tz1)
            for y in range(FY, TY):
                S(x, y, z, 'stone_bricks' if edge else 'cobbled_deepslate')
            for y in range(TY, TY + 18):
                S(x, y, z, pick(WALL) if edge else 'air')
            if not edge:
                S(x, TY, z, 'polished_deepslate' if (x + z) % 2 else 'deepslate_tiles')
                S(x, TY + 17, z, 'deepslate_bricks')
    for x in range(30, 36):                                  # the back wall of the hall is its front: the door through
        for y in range(TY + 1, TY + 3):
            if 32 <= x <= 33: S(x, y, tz0, 'air')
    # its roof: a dark gable
    for h in range(0, 10):
        for z in range(tz0 - 1, tz1 + 2):
            for x in (tx0 - 1 + h, tx1 + 1 - h):
                S(x, TY + 18 + h, z, STAIR('deepslate_tile', 'east' if x < 33 else 'west'))
            for x in range(tx0 + h, tx1 - h + 1):
                if get(x, TY + 18 + h, z) == 'minecraft:air' and h < 9: S(x, TY + 17 + h, z, 'deepslate_tiles')
    # the runner, dark pillars, tall windows
    for x in (32, 33):
        for z in range(tz0 + 1, 52):
            S(x, TY + 1, z, 'purple_carpet')
    for px in (20, 45):
        for pz in range(49, 71, 5):
            for y in range(TY + 1, TY + 17):
                S(px, y, pz, 'polished_basalt[axis=y]')
            S(px, TY + 16, pz, 'polished_blackstone_bricks')
    for wx in (tx0, tx1):
        for z in range(50, 70, 5):
            for y in range(TY + 4, TY + 12):
                S(wx, y, z + 2, 'ochre_froglight[axis=y]' if y in range(TY + 5, TY + 11) else 'polished_blackstone_bricks')
    # the tomb: a black sarcophagus, gold-banded, on a low dais
    tcx, ty, tcz = TOMB
    for x in range(int(tcx) - 3, int(tcx) + 4):
        for z in range(int(tcz) - 4, int(tcz) + 5):
            S(x, TY + 1, z, 'polished_blackstone_bricks' if abs(x - 32) == 3 or abs(z - 58) == 4 else 'polished_blackstone')
    for x in range(int(tcx) - 1, int(tcx) + 2):
        for z in range(int(tcz) - 2, int(tcz) + 3):
            S(x, TY + 2, z, 'polished_deepslate' if x != 32 else 'gold_block')
            S(x, TY + 3, z, 'chiseled_polished_blackstone' if x == 32 and z == 58 else 'polished_blackstone_slab[type=bottom,waterlogged=false]')
    # the six pedestals round it (the sockets sit on them)
    for i in range(6):
        sx_, _sy, sz_ = socket_pos(i)
        x, z = int(math.floor(sx_)), int(math.floor(sz_))
        S(x, TY + 1, z, 'chiseled_polished_blackstone')
        S(x, TY + 2, z, 'polished_blackstone_brick_wall')
    # his throne at the back: huge, black and purple, gold-topped (he is nine blocks tall)
    for x in range(27, 39):
        for z in range(68, 71):
            for y in range(TY + 1, TY + 3):
                S(x, y, z, 'polished_blackstone_bricks')
            if z == 68: S(x, TY + 3, z, 'purple_wool' if 28 <= x <= 37 else 'polished_blackstone_bricks')
    for x in range(27, 39):
        for y in range(TY + 3, TY + 13):
            if abs(x - 32.5) + (y - TY - 3) * 0.5 <= 6.2:
                S(x, y, 71, 'polished_blackstone_bricks' if abs(x - 32.5) > 4.5 else 'purple_wool')
    S(32, TY + 13, 71, 'gold_block'); S(33, TY + 13, 71, 'gold_block'); S(32, TY + 14, 71, 'gold_block')
    for x in (27, 38):
        for y in range(TY + 3, TY + 7): S(x, y, 68, 'polished_blackstone_brick_wall')
    # soul fire: braziers down the room, lanterns on chains
    for (bx, bz) in ((23, 50), (42, 50), (23, 62), (42, 62)):
        S(bx, TY + 1, bz, 'polished_blackstone_bricks'); S(bx, TY + 2, bz, 'soul_campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]')
    for (cx, cz) in ((26, 54), (39, 54), (26, 64), (39, 64)):
        for y in range(TY + 11, TY + 17): S(cx, y, cz, CHAIN)
        S(cx, TY + 10, cz, LANT(True, soul=True))
    for x in range(19, 47, 5):
        for z in range(48, 71, 6):
            S(x, TY + 8, z, 'light[level=9,waterlogged=false]')
    for (x, z) in ((18, 47), (47, 47), (18, 70), (47, 70)):
        S(x, TY + 1, z, 'candle[candles=4,lit=true,waterlogged=false]')

    # ---------------------------------------------------------------- the wings' rooms
    # WEST (x 5..18): the library below; Cecil's room above (a stair in the corner)
    for z in range(13, 44):
        for x in (5, 18):
            if z % 6 != 0:
                for y in range(FY + 1, FY + 5): S(x, y, z, 'bookshelf') if get(x, y, z) == 'minecraft:air' else None
    for z in range(16, 41, 6):
        for x in range(8, 16): S(x, FY + 1, z, 'dark_oak_planks') if x not in (8, 15) else S(x, FY + 1, z, 'dark_oak_fence')
        S(11, FY + 2, z, 'candle[candles=2,lit=true,waterlogged=false]')
    S(12, FY + 1, 14, 'lectern[facing=south,has_book=false,powered=false]')
    for z in range(15, 43, 7):
        S(11, FY + 6, z, LANT(True))
    for k in range(7):                                   # the stair up (west wing, at the back): seven steps to the floor above
        S(8 + k, FY + 1 + k, 37, STAIR('spruce', 'east'))
        for y in (FY + 2 + k, FY + 3 + k, FY + 4 + k): S(8 + k, y, 37, 'air') if k < 6 else None
    # Cecil's room (upstairs, west): purple, a crystal ball, a staff on the wall
    for x in range(5, 19):
        for z in range(13, 35):
            if (x + z) % 2: S(x, FY + 8, z, 'purple_carpet') if get(x, FY + 8, z) == 'minecraft:air' else None
    S(8, FY + 8, 15, 'purple_bed[facing=north,occupied=false,part=head]'); S(8, FY + 8, 16, 'purple_bed[facing=north,occupied=false,part=foot]')
    S(14, FY + 8, 15, 'polished_blackstone_wall'); S(14, FY + 9, 15, 'purple_stained_glass')
    S(16, FY + 8, 20, 'brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]')
    S(6, FY + 8, 24, 'bookshelf'); S(6, FY + 9, 24, 'bookshelf')
    S(11, FY + 13, 20, LANT(True, soul=True)); S(11, FY + 13, 32, LANT(True))
    for z in range(13, 41, 9):
        S(16, FY + 10, z, 'light[level=11,waterlogged=false]')
    # EAST (x 47..60): the dining hall below (Pistachio's), the guest rooms above
    for z in range(17, 39):
        S(53, FY + 1, z, 'dark_oak_planks')
        if z % 3 == 0: S(53, FY + 2, z, 'candle[candles=3,lit=true,waterlogged=false]')
    for z in range(18, 38, 2):
        S(51, FY + 1, z, STAIR('dark_oak', 'east')); S(55, FY + 1, z, STAIR('dark_oak', 'west'))
    S(53, FY + 2, 27, 'cake[bites=1]')
    for z in (14, 15, 16):
        S(59, FY + 1, z, 'smoker[facing=west,lit=true]' if z == 15 else 'barrel[facing=up,open=false]')
    S(59, FY + 1, 41, 'cauldron'); S(58, FY + 1, 42, 'barrel[facing=up,open=false]')
    for (cx, cz) in ((53, 22), (53, 33)):
        for y in range(FY + 4, FY + 7): S(cx, y, cz, CHAIN)
        S(cx, FY + 3, cz, LANT(True))
    for k in range(7):                                   # the stair up (east wing, at the back)
        S(57 - k, FY + 1 + k, 37, STAIR('spruce', 'west'))
        for y in (FY + 2 + k, FY + 3 + k, FY + 4 + k): S(57 - k, y, 37, 'air') if k < 6 else None
    for (bx, bz) in ((50, 16), (57, 16), (50, 30), (57, 30)):
        f = 'south'
        S(bx, FY + 8, bz, f'red_bed[facing={f},occupied=false,part=head]'); S(bx, FY + 8, bz - 1, f'red_bed[facing={f},occupied=false,part=foot]')
        S(bx + (1 if bx == 50 else -1), FY + 8, bz, 'candle[candles=1,lit=true,waterlogged=false]')
    for z in range(15, 42, 8):
        S(53, FY + 13, z, LANT(True))
        S(53, FY + 10, z, 'light[level=11,waterlogged=false]')
    # (the wings' ground floors lit softly)
    for (x0, x1) in ((5, 18), (47, 60)):
        for z in range(15, 43, 6):
            S((x0 + x1) // 2 + 2, FY + 4, z, 'light[level=11,waterlogged=false]')

    # ---------------------------------------------------------------- outside: the path, the dead tree, lanterns on posts
    for z in range(0, 8):
        for x in range(30, 36):
            S(x, FY, z, 'dirt_path' if x in (31, 32, 33, 34) else rnd.choice(['coarse_dirt', 'gravel', 'podzol[snowy=false]']))
    for z in (2, 5):
        for x in (29, 36):
            S(x, FY + 1, z, 'dark_oak_fence'); S(x, FY + 2, z, 'dark_oak_fence'); S(x, FY + 3, z, LANT(False))
    # the dead tree (east of the path), bare and crooked
    tx, tz = 44, 4
    for y in range(FY + 1, FY + 8): S(tx, y, tz, 'stripped_dark_oak_log[axis=y]')
    for (dx, dy, dz, ax) in ((1, 6, 0, 'x'), (2, 7, 0, 'x'), (-1, 5, 0, 'x'), (-2, 6, 1, 'x'), (0, 7, 1, 'z'), (0, 8, 2, 'z'), (1, 8, -1, 'z')):
        S(tx + dx, FY + dy, tz + dz, f'stripped_dark_oak_log[axis={ax}]')
    S(20, FY + 1, 3, 'dead_bush'); S(41, FY + 1, 6, 'dead_bush'); S(14, FY + 1, 5, 'dead_bush')
    S(24, FY + 1, 2, 'cobblestone_wall'); S(24, FY + 2, 2, 'skeleton_skull[rotation=4]')
    # vines on the walls (a few, hanging from the battlements)
    for _ in range(40):
        x, z = rnd.choice([(3, rnd.randint(13, 43)), (62, rnd.randint(13, 43)), (rnd.randint(5, 60), 11)])
        face = 'east' if x == 3 else 'west' if x == 62 else 'south'
        top = FY + rnd.randint(8, 14)
        for y in range(top - rnd.randint(2, 6), top):
            nb = {'east': (x + 1, z), 'west': (x - 1, z), 'south': (x, z + 1)}[face]
            if get(nb[0], y, nb[1]) not in (None, 'minecraft:air') and get(x, y, z) == 'minecraft:air':
                S(x, y, z, f'vine[east={"true" if face == "east" else "false"},north=false,south={"true" if face == "south" else "false"},up=false,'
                           f'west={"true" if face == "west" else "false"}]')

    # ---------------------------------------------------------------- markers and the banners
    B.marker(*CENTER, ['bm.ompal', 'bm.omnew'])
    B.marker(*TOMB, ['bm.omtomb'])
    B.marker(*SPAWN, ['bm.omspawn'], 180.0)
    B.marker(*THRONE_AT, ['bm.omthrone'], 180.0)
    B.marker(*ARRIVE, ['bm.omarrive'], 0.0)
    for i, d in enumerate(EMBLEMS):
        B.marker(*socket_pos(i), ['bm.omsockm', f'bm.omsk_{d}'])
    for (x, y, z, tag) in ((32.5, FY + 3, 26.5, 'hall'), (11.5, FY + 3, 28.5, 'library'), (53.5, FY + 3, 28.5, 'dining'), (32.5, TY + 4, 58.5, 'tomb'),
                           (32.5, FY + 3, 3.5, 'gate'), (11.5, FY + 10, 28.5, 'cecil'), (53.5, FY + 10, 28.5, 'guest')):
        B.marker(x, y, z, ['bm.omamb', f'bm.omamb_{tag}'])
    def banner(x, y, z, yaw, s=3.0):
        B.ents.append({'pos': [Double(x), Double(y), Double(z)], 'blockPos': [Int(int(x // 1)), Int(int(y // 1)), Int(int(z // 1))],
                       'nbt': {'id': 'minecraft:item_display', 'Tags': ['bm.omban'], 'Rotation': [Float(yaw), Float(0.0)],
                               'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:om_banner'}},
                               'item_display': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(12)},
                               'transformation': {'left_rotation': [Float(0), Float(0), Float(0), Float(1)], 'right_rotation': [Float(0), Float(0), Float(0), Float(1)],
                                                  'translation': [Float(0), Float(0), Float(0)], 'scale': [Float(s), Float(s), Float(s)]}}})
    # (the three over the great door, facing into the hall; one over the gate; two in the throne room either side of his throne)
    banner(32.5, TY + 9.5, HALL[3] - 0.45, 0.0, 4.2)
    banner(26.5, TY + 8.0, HALL[3] - 0.45, 0.0, 2.8)
    banner(38.5, TY + 8.0, HALL[3] - 0.45, 0.0, 2.8)
    banner(32.5, FY + 9.5, 6.55, 180.0, 3.0)
    banner(25.5, TY + 9.0, THRONE[3] - 0.45, 0.0, 3.4)
    banner(39.5, TY + 9.0, THRONE[3] - 0.45, 0.0, 3.4)
    return B


def check(B):
    """Static proofs (run at build): the door to the throne room on foot, every room and socket reachable, nothing hanging
    from air, the tomb and the throne clear for a nine-block king."""
    import p2.verify as V
    from p2.verify import Grid
    errs = []
    G = Grid(B, outside='solid')
    V.GRID = G
    seen = G.bfs([(32, FY + 1, 1)], margin=0)
    want = {'the hall': (32, FY + 1, 26), 'the landing': (32, TY + 1, 42), 'the throne room': (32, TY + 1, 48), 'the throne': (32, TY + 1, 66),
            'the library': (11, FY + 1, 28), 'the dining hall': (50, FY + 1, 28), "Cecil's room": (11, FY + 8, 28), 'the guest rooms': (53, FY + 8, 28)}
    for nm, p in want.items():
        if not any(abs(a - p[0]) <= 1 and abs(c - p[2]) <= 1 and b == p[1] for (a, b, c) in seen):
            errs.append(f'{nm} {p} not reachable on foot from the path')
    for i in range(6):
        x, y, z = socket_pos(i)
        if not any(math.hypot(a + 0.5 - x, c + 0.5 - z) <= 2.2 and b == TY + 1 for (a, b, c) in seen):
            errs.append(f'socket {EMBLEMS[i]} out of reach')
    # the space he rises in and holds court in: clear, nine blocks up
    for (x, y, z) in (SPAWN, THRONE_AT):
        for dy in range(0, 12):
            for dx in (-2, 0, 2):
                st = B.b.get((int(x + dx), int(y + dy), int(z)), 'minecraft:air')
                if st not in ('minecraft:air', 'minecraft:light') and not st.startswith('minecraft:light['):
                    errs.append(f'{(int(x + dx), int(y + dy), int(z))} blocks his space: {st}'); break
    # lanterns, candles, chains: something under or over them
    for (x, y, z), st in B.b.items():
        nm = st.split('[')[0].split(':')[1]
        if nm in ('lantern', 'soul_lantern'):
            hang = 'hanging=true' in st
            n = B.b.get((x, y + (1 if hang else -1), z), 'minecraft:air')
            if n == 'minecraft:air' or n.startswith('minecraft:light'): errs.append(f'{nm} {(x, y, z)} hangs from air')
        if nm in ('candle', 'dead_bush', 'cake', 'brewing_stand'):
            n = B.b.get((x, y - 1, z), 'minecraft:air')
            if n == 'minecraft:air' or n.startswith('minecraft:light'): errs.append(f'{nm} {(x, y, z)} stands on air')
    return sorted(set(errs))
