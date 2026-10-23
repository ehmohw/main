"""Isometric preview of a structures.Build (flat block colours, shaded faces) - for checking a structure against its art.

    from tools.preview.structiso import render
    render(B, 'out.png', hide=('glass',), yaw=45)"""
import math
from PIL import Image, ImageDraw

COL = {
    'stone_bricks': (128, 128, 128), 'cracked_stone_bricks': (112, 112, 112), 'mossy_stone_bricks': (108, 122, 96), 'chiseled_stone_bricks': (120, 120, 120),
    'andesite': (136, 136, 136), 'polished_andesite': (142, 144, 144), 'stone': (125, 125, 125), 'cobblestone': (115, 115, 115), 'gravel': (130, 124, 122),
    'blue_terracotta': (74, 60, 112), 'blue_concrete': (45, 47, 143), 'light_blue_concrete': (90, 170, 220), 'magenta_wool': (190, 70, 180),
    'grass_block': (95, 160, 60), 'dirt': (134, 96, 67), 'sand': (219, 207, 163), 'glass': (200, 230, 240), 'light_blue_stained_glass': (110, 170, 220),
    'prismarine_bricks': (99, 171, 158), 'prismarine_brick_slab': (99, 171, 158), 'dark_prismarine': (51, 91, 75), 'prismarine': (99, 156, 151),
    'sea_lantern': (210, 230, 225), 'water': (60, 90, 200), 'polished_diorite': (200, 200, 200), 'quartz_stairs': (235, 230, 225), 'gold_block': (245, 210, 60),
    'end_rod': (240, 240, 230), 'campfire': (230, 120, 30), 'blackstone': (40, 36, 42), 'coal_block': (20, 20, 20), 'black_concrete': (10, 10, 14),
    'polished_blackstone': (50, 46, 54), 'polished_blackstone_bricks': (48, 42, 50), 'pink_tulip': (240, 140, 190), 'pink_petals': (240, 160, 200),
    'peony': (230, 160, 210), 'allium': (190, 110, 220), 'short_grass': (110, 170, 70), 'lantern': (240, 190, 90), 'soul_lantern': (90, 220, 230),
    'nether_bricks': (60, 30, 36), 'red_nether_bricks': (100, 20, 20), 'blackstone_bricks': (40, 36, 42), 'magma_block': (160, 70, 20), 'lava': (240, 110, 20),
    'netherrack': (110, 50, 50), 'basalt': (80, 80, 86), 'polished_basalt': (90, 90, 96), 'obsidian': (25, 18, 40), 'crying_obsidian': (60, 20, 100),
    'purpur_block': (170, 125, 170), 'purpur_pillar': (175, 130, 175), 'end_stone': (220, 222, 160), 'end_stone_bricks': (215, 218, 155),
    'amethyst_block': (140, 100, 200), 'shroomlight': (240, 150, 70), 'glowstone': (250, 210, 120), 'gilded_blackstone': (90, 70, 40),
    'chest': (160, 110, 50), 'barrel': (130, 95, 55), 'iron_bars': (150, 150, 150), 'chain': (70, 70, 80), 'iron_chain': (70, 70, 80),
    'cauldron': (70, 70, 74), 'water_cauldron': (70, 90, 200), 'lava_cauldron': (220, 100, 30), 'anvil': (60, 60, 64), 'smithing_table': (60, 50, 50),
}


def color(st):
    n = st.split(':', 1)[-1].split('[', 1)[0]
    if n in COL: return COL[n]
    for suf in ('_stairs', '_slab', '_wall', '_fence'):
        if n.endswith(suf):
            b = n[:-len(suf)]
            for k in (b, b + 's', b + '_block', b.replace('brick', 'bricks')):
                if k in COL: return COL[k]
    if 'banner' in n: return COL['magenta_wool']
    if 'glass' in n: return COL['glass']
    return (200, 0, 200)


def render(B, path, hide=(), yaw=45, scale=6, cut=None, bg=(24, 30, 44)):
    """yaw: 45 looks from the low-x/low-z corner (the north-west), 135 from the north-east, ... ; cut(x,y,z)->True hides a cell"""
    sx, sy, sz = B.size
    a = math.radians(yaw)
    ca, sa = math.cos(a), math.sin(a)
    cells = {p: st for p, st in B.b.items() if not st.endswith(':air') and st.split(':', 1)[-1].split('[', 1)[0] not in hide and not (cut and cut(*p))}

    def proj(x, y, z):
        u = (x - sx / 2) * ca - (z - sz / 2) * sa
        v = (x - sx / 2) * sa + (z - sz / 2) * ca
        return u * scale, (-y * 1.15 + v * 0.5) * scale, v

    pts = [proj(x, y, z) for x in (0, sx) for y in (0, sy) for z in (0, sz)]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    W, H = int(maxx - minx) + 20, int(maxy - miny) + 20
    im = Image.new('RGB', (W, H), bg)
    d = ImageDraw.Draw(im)
    off = lambda p: (p[0] - minx + 10, p[1] - miny + 10)
    # faces seen from the camera: +y, and the two side faces toward it
    vx, vz = sa, ca              # direction toward the viewer in xz (v grows toward the viewer: lower on the screen)
    faces = []
    for (x, y, z), st in cells.items():
        c = color(st)
        def solid(p):
            s = cells.get(p)
            return s is not None and 'glass' not in s.split(':')[-1] if 'glass' not in st else s is not None
        if not solid((x, y + 1, z)):
            q = [proj(x, y + 1, z), proj(x + 1, y + 1, z), proj(x + 1, y + 1, z + 1), proj(x, y + 1, z + 1)]
            faces.append((sum(p[2] for p in q) / 4 + y * 0.001 + 0.5, q, c, 1.0))
        for (dx, dz, quad) in ((1, 0, [(1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 1, 0)]), (-1, 0, [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)]),
                               (0, 1, [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]), (0, -1, [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])):
            if dx * vx + dz * vz <= 0: continue
            if solid((x + dx, y, z + dz)): continue
            q = [proj(x + ox, y + oy, z + oz) for ox, oy, oz in quad]
            shade = 0.78 if dx else 0.62
            faces.append((sum(p[2] for p in q) / 4 + y * 0.001, q, c, shade))
    faces.sort(key=lambda f: f[0])
    for _dep, q, c, sh in faces:
        col = tuple(int(v * sh) for v in c)
        d.polygon([off(p) for p in q], fill=col)
    im.save(path)
    return im
