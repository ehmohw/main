"""Floor-plan previews of the Phase 2 dungeons (developer aid): for each dungeon, slices at its walk levels with
gates, battle doors, secret doors, puzzle elements, the altar and markers highlighted."""
import sys
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/bm_build')

COL = [('air', None), ('tuff', (110, 110, 100)), ('podzol', (90, 65, 40)), ('coarse_dirt', (110, 80, 55)), ('leaf_litter', (130, 100, 60)),
       ('dead_bush', (140, 105, 60)), ('gray_banner', (120, 120, 120)), ('gray_candle', (130, 130, 130)), ('mud', (60, 55, 60)), ('cherry_leaves', (240, 170, 200)), ('pink_petals', (250, 180, 210)), ('pale_oak_leaves', (200, 205, 190)),
       ('pale_moss', (190, 195, 175)), ('pale_hanging', (200, 205, 190)), ('cherry_log', (90, 50, 60)), ('pale_oak_log', (210, 205, 200)),
       ('moss_block', (95, 130, 55)), ('rooted', (140, 105, 80)), ('lily_of', (250, 250, 250)), ('white_tulip', (250, 250, 240)),
       ('azure', (200, 220, 255)), ('oxeye', (250, 250, 220)), ('short_grass', (110, 150, 70)), ('firefly', (120, 140, 60)),
       ('dripstone', (140, 110, 90)), ('white_banner', (250, 250, 250)), ('white_candle', (255, 250, 230)), ('red_nether', (150, 25, 30)), ('nether_wart', (120, 15, 20)), ('red_terracotta', (140, 50, 40)),
       ('red_', (170, 30, 35)), ('froglight', (250, 200, 90)), ('orange_stained', (230, 140, 40)), ('basalt', (70, 70, 75)),
       ('crying_obsidian', (80, 20, 120)), ('soul_fire', (90, 220, 230)), ('lava_cauldron', (230, 90, 20)), ('light', (255, 230, 140)), ('water', (40, 90, 200)), ('lava', (230, 90, 20)),
       ('reinforced_deepslate', (40, 60, 70)), ('iron_block', (200, 200, 205)), ('raw_gold', (220, 170, 60)),
       ('gold', (240, 200, 40)), ('quartz', (235, 230, 220)), ('calcite', (225, 225, 220)), ('smooth_quartz', (235, 230, 220)),
       ('white_wool', (245, 245, 245)), ('cobweb', (220, 220, 230)), ('blue_ice', (120, 170, 250)), ('ice', (160, 200, 250)),
       ('snow', (240, 250, 255)), ('copper', (90, 160, 140)), ('prismarine', (90, 170, 150)), ('purple', (150, 80, 200)),
       ('amethyst', (160, 110, 210)), ('blackstone', (45, 40, 45)), ('deepslate', (75, 75, 80)), ('tuff', (110, 110, 100)),
       ('mud', (110, 85, 65)), ('dirt', (120, 85, 55)), ('moss', (120, 140, 90)), ('log', (190, 180, 170)), ('plank', (160, 120, 80)),
       ('glass', (60, 60, 80)), ('bars', (130, 130, 140)), ('pressure_plate', (210, 90, 90)), ('button', (255, 255, 0)),
       ('lever', (255, 255, 0)), ('target', (255, 60, 60)), ('bulb', (230, 140, 60)), ('vault', (40, 200, 200)),
       ('trial_spawner', (200, 40, 160)), ('chest', (180, 120, 40)), ('barrel', (150, 100, 50)), ('lectern', (180, 140, 90)),
       ('stairs', (130, 120, 120)), ('slab', (120, 120, 120)), ('sign', (220, 200, 150)), ('lantern', (120, 220, 255)),
       ('candle', (255, 240, 200)), ('bell', (240, 210, 60)), ('hay', (220, 190, 60)), ('terracotta', (200, 160, 60)),
       ('glowstone', (255, 230, 120)), ('stone', (130, 130, 130))]


def color(st):
    if st is None: return None
    n = st.split(':', 1)[-1].split('[', 1)[0]
    for k, c in COL:
        if k in n: return c
    return (150, 150, 150)


def render(B, levels, path, scale=6):
    sx, sy, sz = B.size
    W = len(levels) * (sx * scale + 12)
    im = Image.new('RGB', (W, sz * scale + 26), (18, 18, 22))
    d = ImageDraw.Draw(im)
    gate_cells, sdoor_cells = set(), set()
    for (x, y, z, axis, n) in B.meta['gates']:
        for dw in (-1, 0, 1):
            gate_cells.add((x + dw, z) if axis == 'x' else (x, z + dw))
    for (x, y, z, k) in B.meta['sdoors']: sdoor_cells.add((x, z))
    for i, y in enumerate(levels):
        ox = i * (sx * scale + 12)
        d.text((ox + 2, 2), f'{B.d}  y={y}', fill=(230, 230, 230))
        for x in range(sx):
            for z in range(sz):
                st = B.b.get((x, y, z))
                c = color(st)
                if c is None:                                 # look down: show the floor dimmed
                    fl = B.b.get((x, y - 1, z))
                    fc = color(fl)
                    c = tuple(int(v * 0.45) for v in fc) if fc else (18, 18, 22)
                if (x, z) in gate_cells and st and ('light' in st or B.cfg['gate'] in st): c = (255, 40, 40)
                if (x, z) in sdoor_cells and st and B.cfg['secret'] in st: c = (255, 0, 255)
                d.rectangle([ox + x * scale, 20 + z * scale, ox + x * scale + scale - 1, 20 + z * scale + scale - 1], fill=c)
        ax, ay, az = B.meta['altar']
        if abs(ay - y) <= 1:
            d.ellipse([ox + ax * scale - 3, 20 + az * scale - 3, ox + ax * scale + scale + 2, 20 + az * scale + scale + 2], outline=(0, 255, 0), width=2)
        ex, ey, ez = B.meta['entrance']
        if abs(ey - y) <= 1:
            d.ellipse([ox + ex * scale - 3, 20 + ez * scale - 3, ox + ex * scale + scale + 2, 20 + ez * scale + scale + 2], outline=(0, 200, 255), width=2)
    im.save(path)


if __name__ == '__main__':
    import items, p2.p2items  # noqa
    from p2.dungeons import brood, frost, tide, hex, keep, hollow, lucky
    L = {brood: [3, 15], frost: [7, 16, 25, 34, 43], tide: [5, 36], hex: [6], keep: [1, 7], hollow: [21], lucky: [5]}
    for mod, lv in L.items():
        B = mod.build()
        render(B, lv, f'/home/claude/bm_build/preview/p2_{B.d}.png', scale=5 if B.size[0] > 70 else 6)
        print(B.d, 'ok')


def iso(B, path, s=4, cut=None):
    """Isometric exterior render (surface voxels only, painter's order)."""
    sx, sy, sz = B.size
    W, H = (sx + sz) * s * 2 + 40, (sx + sz) * s + sy * s * 2 + 40
    im = Image.new('RGB', (W, H), (16, 16, 20))
    d = ImageDraw.Draw(im)
    def solid(x, y, z):
        st = B.b.get((x, y, z))
        if not st: return False
        n = st.split(':', 1)[-1].split('[')[0]
        return not (n in ('air', 'light', 'cobweb') or n.endswith(('button', 'sign', 'lantern', 'carpet', 'plate', 'chain')))
    ox, oy = sz * s * 2 + 20, sy * s * 2 + 20
    for y in range(sy):
        if cut is not None and y > cut: break
        for t in range(sx + sz):
            for x in range(max(0, t - sz + 1), min(sx, t + 1)):
                z = t - x
                if not solid(x, y, z): continue
                if solid(x, y + 1, z) and solid(x + 1, y, z) and solid(x, y, z + 1): continue
                c = color(B.b[(x, y, z)]) or (150, 150, 150)
                px, py = ox + (x - z) * s * 2, oy + (x + z) * s - y * s * 2
                top = [(px, py), (px + 2 * s, py + s), (px, py + 2 * s), (px - 2 * s, py + s)]
                left = [(px - 2 * s, py + s), (px, py + 2 * s), (px, py + 4 * s), (px - 2 * s, py + 3 * s)]
                right = [(px, py + 2 * s), (px + 2 * s, py + s), (px + 2 * s, py + 3 * s), (px, py + 4 * s)]
                d.polygon(left, fill=tuple(int(v * 0.6) for v in c))
                d.polygon(right, fill=tuple(int(v * 0.8) for v in c))
                d.polygon(top, fill=c)
    im = im.crop(im.getbbox())
    im.save(path)


if __name__ == '__main__':
    for mod, cut in ((keep, None), (lucky, None), (hollow, None), (keep, 12)):
        B = mod.build()
        iso(B, f'/home/claude/bm_build/preview/p2_{B.d}_iso{"_cut" if cut else ""}.png', s=3, cut=cut)
        print('iso', B.d)
