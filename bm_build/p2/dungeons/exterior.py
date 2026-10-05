"""2.13: dressing for the dungeon exteriors (the Hollow Throne keeps its own). Every helper here only fills cells the dungeon
left UNSET (open world) or re-skins the outermost layer of a shell wall, so no room, passage, puzzle or marker changes -
the verifier's walk/lighting proofs still run on the result.

  FROSTBOUND SPIRE   banded ice-and-slate courses, eight stepped buttresses with ice pinnacles, a corbelled parapet hung with
                     icicles, four ice needles on the crown, banners and lamps at the door
  SUNKEN THRONE      dark-prismarine pilasters with sea-lantern capitals, a lantern band, a ruined colonnade and conduit on the
                     roof, sea pickles on the terraces, a coral reef, kelp and seagrass round the base
  HEXBOUND CATHEDRAL a hipped slate roof over the Apse, flying-buttress pinnacles with skulls, tall violet windows in the Apse,
                     a ceiled porch with hanging lanterns, vines and moss creeping over everything
  WILFREY'S KEEP     the usurper's black banners and Wilfrey's white ones on the curtain walls, lamps on every buttress"""
import math


def unset(B, x, y, z):
    sx, sy, sz = B.size
    return 0 <= x < sx and 0 <= y < sy and 0 <= z < sz and B.get(x, y, z) is None


def put(B, x, y, z, st):
    """Place only into open world."""
    if unset(B, x, y, z): B.set(x, y, z, st)


def face_cells(B, palette_names):
    """Shell cells (in the given palette) with open world beside them, and the outward directions."""
    out = {}
    for (x, y, z), st in list(B.b.items()):
        if not st: continue
        n = st.split(':', 1)[-1].split('[')[0]
        if n not in palette_names: continue
        dirs = [(dx, dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if unset(B, x + dx, y, z + dz)]
        if dirs: out[(x, y, z)] = dirs
    return out


VINE_SIDE = {(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north', (0, -1): 'south'}     # vine placed at wall+d hangs on its <side>
STAIR_IN = {(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north', (0, -1): 'south'}


def vine(side):
    return 'vine[' + ','.join(f'{s}={"true" if s == side else "false"}' for s in ('east', 'north', 'south', 'up', 'west')) + ']'


# ================================================================ THE FROSTBOUND SPIRE
def frost(B):
    from p2.dungeons.frost import CX, CZ, inside
    r = B.rnd
    WALLN = {'deepslate_tiles', 'cracked_deepslate_tiles', 'packed_ice', 'polished_deepslate'}
    faces = face_cells(B, WALLN)
    FY = (6, 15, 24, 33, 42)
    streak = {}
    for (x, y, z) in faces:
        dx, dz = abs(x - CX), abs(z - CZ)
        vert = (dx, dz) in ((13, 6), (6, 13))
        if vert: st = 'polished_deepslate'                                   # pilasters at the octagon's corners
        elif y in FY or y == 44: st = 'deepslate_bricks'                     # string courses at every floor
        elif y <= 7: st = 'cobbled_deepslate'
        else:
            k = streak.setdefault((x, z), (r.random() < 0.22, 44 - r.randrange(6, 26)))
            st = ('blue_ice' if r.random() < 0.15 else 'packed_ice') if k[0] and y >= k[1] else \
                 ('cracked_deepslate_tiles' if r.random() < 0.12 else 'deepslate_tiles')
        B.set(x, y, z, st)
    # eight buttresses, stepping in as they rise, each capped by an ice pinnacle
    verts = [(CX + sx * a, CZ + sz * b) for sx in (1, -1) for sz in (1, -1) for (a, b) in ((13, 6), (6, 13))]
    for (vx, vz) in verts:
        ox, oz = (1 if vx > CX else -1), (1 if vz > CZ else -1)
        for k, top in ((1, 34), (2, 26), (3, 18)):
            cells = [(vx + ox * k, vz), (vx, vz + oz * k), (vx + ox * k, vz + oz * k)] if k < 3 else [(vx + ox * (k - 1), vz + oz * (k - 1))]
            for (bx, bz) in cells:
                if inside(bx, bz): continue
                for y in range(0, top + 1): put(B, bx, y, bz, 'polished_deepslate' if y % 9 == 6 else 'deepslate_bricks')
                put(B, bx, top + 1, bz, 'snow[layers=2]')
        px, pz = vx + ox, vz + oz
        for y in range(35, 40): put(B, px, y, pz, 'packed_ice')
        put(B, px, 40, pz, 'blue_ice'); put(B, px, 41, pz, 'end_rod[facing=up]')
    # corbelled parapet one block out at y44, hung with icicles
    for x in range(B.size[0]):
        for z in range(B.size[2]):
            if inside(x, z, -1) and not inside(x, z):
                put(B, x, 44, z, 'deepslate_brick_slab[type=top,waterlogged=false]')
                if r.random() < 0.35:
                    for y in range(43, 43 - r.randrange(1, 4), -1): put(B, x, y, z, 'ice' if y < 43 else 'packed_ice')
    # four ice needles on the crown (on the diagonal faces of the ring)
    for (sx, sz) in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        nx, nz = CX + sx * 10, CZ + sz * 9
        if not inside(nx, nz) or inside(nx, nz, 1): continue
        for y in range(46, 52): put(B, nx, y, nz, 'packed_ice' if y < 50 else 'blue_ice')
        put(B, nx, 52, nz, 'sea_lantern'); put(B, nx, 53, nz, 'end_rod[facing=up]')
    # the door: lamps on the porch walls, frost-blue banners either side
    for x in (19, 25):
        put(B, x, 12, 36, 'soul_lantern[hanging=false,waterlogged=false]')
    for x in (18, 26):
        put(B, x, 10, 36, 'light_blue_wall_banner[facing=south]')


# ================================================================ THE SUNKEN THRONE
def tide(B):
    r = B.rnd
    BODYN = {'prismarine_bricks', 'dark_prismarine', 'prismarine', 'cracked_stone_bricks'}
    faces = face_cells(B, BODYN)
    for (x, y, z), dirs in faces.items():
        if y > 22: continue
        along = z if dirs[0][0] else x
        if along % 8 in (0, 1): st = 'sea_lantern' if y == 20 else 'dark_prismarine'      # pilasters with lit capitals
        elif y <= 2: st = 'dark_prismarine'
        elif y == 12: st = 'sea_lantern' if along % 8 == 4 else 'dark_prismarine'       # a lantern band half way up
        elif y == 21: st = 'dark_prismarine'
        else: st = 'prismarine_bricks' if r.random() < 0.75 else 'prismarine'
        B.set(x, y, z, st)
    # the roof: a ruined colonnade round the top terrace, a conduit at its heart, pickles on every step
    top = 25
    for (x, z) in [(x, z) for x in range(14, 42, 3) for z in (14, 41)] + [(x, z) for z in range(17, 41, 3) for x in (14, 41)]:
        h = 2 + (x * 7 + z * 3) % 4
        for y in range(top + 1, top + 1 + h): put(B, x, y, z, 'prismarine_wall' if y < top + h else 'dark_prismarine')
    put(B, 27, top + 1, 27, 'dark_prismarine'); put(B, 27, top + 2, 27, 'conduit[waterlogged=true]')
    for i in range(0, 4):
        lo, hi, y = 4 + i * 3, 51 - i * 3, 23 + i
        for x in range(lo, hi + 1):
            for z in (lo, hi):
                if r.random() < 0.08: put(B, x, y, z, f'sea_pickle[pickles={r.randrange(1, 5)},waterlogged=true]')
        for z in range(lo, hi + 1):
            for x in (lo, hi):
                if r.random() < 0.08: put(B, x, y, z, f'sea_pickle[pickles={r.randrange(1, 5)},waterlogged=true]')
    # the tower: lantern bands and a crown of walls
    for y in (26, 32):
        for (x, z) in ((5, 5), (9, 5), (5, 9), (9, 9)):
            if B.get(x, y, z) and 'prismarine' in B.get(x, y, z): B.set(x, y, z, 'sea_lantern')
    for x in range(5, 10):
        for z in range(5, 10):
            if x in (5, 9) or z in (5, 9):
                if (x + z) % 2 == 0: put(B, x, 39, z, 'prismarine_wall')
    # the reef round the base (template y3 is the sea floor)
    corals = ['tube', 'brain', 'bubble', 'fire', 'horn']
    for x in range(0, 56):
        for z in range(0, 56):
            if 4 <= x <= 51 and 4 <= z <= 51: continue
            v = r.random()
            if v < 0.10:
                c = r.choice(corals)
                put(B, x, 3, z, f'{c}_coral_block')
                put(B, x, 4, z, f'{r.choice(corals)}_coral[waterlogged=true]' if r.random() < 0.6 else f'{c}_coral_fan[waterlogged=true]')
            elif v < 0.17:
                h = r.randrange(3, 12)
                for y in range(3, 3 + h): put(B, x, y, z, 'kelp_plant')
                put(B, x, 3 + h, z, 'kelp[age=25]')
            elif v < 0.30:
                put(B, x, 3, z, 'seagrass')
            elif v < 0.33:
                put(B, x, 3, z, 'tall_seagrass[half=lower]'); put(B, x, 4, z, 'tall_seagrass[half=upper]')


# ================================================================ THE HEXBOUND CATHEDRAL
def hex(B):
    r = B.rnd
    TRIM = 'polished_blackstone_bricks'
    # a hipped slate roof over the Apse (x9..39, z59..78; ceiling y26), its ridge running on from the nave's
    for x in range(9, 40):
        for z in range(59, 79):
            h = min(15 - abs(x - 24), 79 - z, 14)
            for y in range(27, 27 + max(1, h)):
                put(B, x, y, z, 'deepslate_tiles' if (y - z) % 5 else 'deepslate_bricks')
    # corner pinnacles on the Apse, buttresses with skull-capped pinnacles along its walls
    for (x, z) in ((8, 58), (40, 58), (8, 79), (40, 79)):
        for y in range(5, 30): put(B, x, y, z, TRIM)
        put(B, x, 30, z, 'polished_blackstone_wall'); put(B, x, 31, z, 'soul_lantern[hanging=false,waterlogged=false]')
    for z in range(62, 78, 5):
        for (bx, wx) in ((8, 9), (40, 39)):
            for y in range(5, 21): put(B, bx, y, z, TRIM)
            put(B, bx, 21, z, 'wither_skeleton_skull[powered=false,rotation=%d]' % (4 if bx == 40 else 12))
            for y in range(11, 19):
                for dz in (2, 3):
                    if B.get(wx, y, z + dz) and 'deepslate' in B.get(wx, y, z + dz):
                        B.set(wx, y, z + dz, 'magenta_stained_glass_pane[east=false,north=false,south=false,west=false,waterlogged=false]')
    for x in range(12, 38, 6):
        for y in range(5, 21): put(B, x, y, 79, TRIM)
        put(B, x, 21, 79, 'wither_skeleton_skull[powered=false,rotation=0]')
    # pinnacles on top of the nave's buttresses (x12 / x36 every 5)
    for z in range(8, 57, 5):
        for bx in (12, 36):
            if B.get(bx, 19, z):
                put(B, bx, 20, z, 'polished_blackstone_wall'); put(B, bx, 21, z, 'polished_blackstone_wall')
                put(B, bx, 22, z, 'skeleton_skull[powered=false,rotation=%d]' % (12 if bx == 12 else 4))
    # the porch under the bell tower: a ceiling (the tower was open above) and hanging lanterns
    for x in range(20, 29):
        for z in range(1, 4): put(B, x, 25, z, 'deepslate_tiles')
    for (x, z) in ((21, 2), (27, 2)):
        put(B, x, 24, z, 'iron_chain[axis=y,waterlogged=false]'); put(B, x, 23, z, 'soul_lantern[hanging=true,waterlogged=false]')
    # the swamp creeps up: vines down the walls, moss on the ledges
    WALLN = {'deepslate_bricks', 'cracked_deepslate_bricks', 'polished_deepslate', 'mossy_stone_bricks', 'deepslate_tiles'}
    for (x, y, z), dirs in face_cells(B, WALLN).items():
        if y < 14 or y > 26 or r.random() > 0.05: continue
        dx, dz = dirs[0]
        for yy in range(y, max(6, y - r.randrange(3, 10)), -1):
            if not unset(B, x + dx, yy, z + dz): break
            B.set(x + dx, yy, z + dz, vine(VINE_SIDE[(dx, dz)]))
    for (x, y, z), st in list(B.b.items()):
        if st and 'polished_blackstone_bricks' in st and unset(B, x, y + 1, z) and r.random() < 0.25 and y > 6:
            put(B, x, y + 1, z, 'moss_carpet')


# ================================================================ WILFREY'S KEEP
def keep(B):
    # banners on the curtain walls between the buttresses: Bobbery's black, with Wilfrey's old white here and there
    for i, z in enumerate(range(16, 70, 8)):
        col = 'white' if i % 3 == 1 else 'black'
        put(B, 3, 15, z, f'{col}_wall_banner[facing=west]'); put(B, 68, 15, z, f'{col}_wall_banner[facing=east]')
    for i, x in enumerate(range(16, 62, 8)):
        put(B, x, 15, 74, f'{"white" if i % 3 == 1 else "black"}_wall_banner[facing=south]')
    # a lamp on every buttress
    for z in range(12, 70, 8):
        for x in (3, 68):
            put(B, x, 18, z, 'polished_blackstone_wall'); put(B, x, 19, z, 'soul_lantern[hanging=false,waterlogged=false]')
    for x in range(12, 64, 8):
        put(B, x, 18, 74, 'polished_blackstone_wall'); put(B, x, 19, 74, 'soul_lantern[hanging=false,waterlogged=false]')
