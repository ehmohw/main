"""Preview of the Undercrown's built template (p2/dungeons/undercrown.py): a top-down map per level band, and sections.

    python3 tools/preview/undercrown_map.py [out_dir]

Top-down: in each band the highest floor that has air over it is drawn in its block's colour (darker the lower it lies);
solid-only columns are drawn as wall; unset cells (the Nether's own rock) are the background. Sections cut the whole
template on one plane. Markers are dots coloured by kind, labelled with their puzzle number (or a short name)."""
import os, sys, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-user-main/99867ee9-8c51-5a94-9ce7-6ff9e7d41656/scratchpad/previews/undercrown'
S = 4
try:
    F = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
    F(10)
except OSError:
    F = lambda n: ImageFont.load_default()

BASE = {
    'air': None, 'lava': (255, 110, 10), 'tinted_glass': (60, 40, 70), 'black_stained_glass': (30, 26, 36), 'red_stained_glass': (190, 30, 40),
    'orange_stained_glass': (230, 120, 30), 'purple_stained_glass': (130, 60, 170), 'light_blue_stained_glass': (120, 180, 230),
    'packed_ice': (140, 180, 235), 'blue_ice': (100, 150, 235), 'snow_block': (235, 240, 250), 'crying_obsidian': (120, 40, 200),
    'obsidian': (34, 24, 48), 'polished_blackstone': (58, 52, 62), 'polished_blackstone_bricks': (52, 46, 56), 'blackstone': (44, 40, 46),
    'deepslate_tiles': (64, 64, 70), 'deepslate_bricks': (70, 70, 76), 'polished_deepslate': (72, 72, 78), 'reinforced_deepslate': (34, 36, 34),
    'red_nether_bricks': (110, 18, 22), 'nether_wart_block': (120, 10, 10), 'crimson_planks': (110, 50, 70), 'magma_block': (170, 70, 20),
    'shroomlight': (250, 160, 70), 'bone_block': (220, 215, 190), 'smooth_quartz': (235, 230, 225), 'quartz_block': (235, 230, 225),
    'gold_block': (250, 210, 60), 'raw_gold_block': (220, 170, 60), 'gilded_blackstone': (110, 85, 45), 'prismarine': (100, 160, 150),
    'dark_prismarine': (50, 95, 80), 'prismarine_bricks': (100, 170, 160), 'dark_oak_planks': (66, 43, 20), 'white_concrete': (240, 240, 240),
    'white_wool': (240, 240, 240), 'pearlescent_froglight': (240, 220, 240), 'basalt': (80, 80, 86), 'polished_basalt': (92, 92, 98),
    'netherrack': (110, 48, 48), 'bookshelf': (120, 80, 40), 'amethyst_block': (150, 100, 210), 'purpur_block': (170, 125, 170),
    'target': (230, 200, 190), 'waxed_copper_bulb': (200, 120, 60), 'iron_bars': (150, 150, 155), 'iron_chain': (90, 90, 100),
    'soul_lantern': (90, 230, 240), 'chest': (170, 120, 50), 'vault': (80, 80, 90), 'lectern': (160, 110, 60), 'bell': (240, 200, 60),
    'stripped_dark_oak_wood': (75, 55, 40), 'cracked_nether_bricks': (60, 30, 36), 'soul_soil': (75, 57, 45), 'chiseled_polished_blackstone': (70, 62, 70),
}
MK = {'gate': ((255, 60, 60), 'G'), 'pz': ((255, 220, 60), 'P'), 'sigil': ((90, 255, 220), 'S'), 'target': ((255, 140, 40), 'T'),
      'wsp': ((255, 90, 160), 'w'), 'echo': ((255, 40, 255), 'E'), 'socket': ((255, 255, 255), 'O'), 'hidden': ((190, 100, 255), 'H'),
      'relic': ((220, 160, 255), 'R'), 'voice': ((255, 120, 120), 'v'), 'eye': ((255, 30, 30), '.'), 'vault': ((80, 255, 120), 'V'),
      'zone': ((70, 70, 120), ''), 'sdoor': ((255, 255, 0), 'X'), 'other': ((180, 180, 180), ''), 'bulb': ((255, 170, 70), 'b'),
      'seq': ((120, 200, 255), 'q'), 'lo': ((200, 200, 255), 'l'), 'rift': ((120, 255, 255), 'r'), 'well': ((255, 50, 50), 'W'),
      'entr': ((60, 255, 60), 'IN')}


def colour(st):
    n = st.split(':', 1)[-1].split('[', 1)[0]
    if n in BASE: return BASE[n]
    for suf in ('_stairs', '_slab', '_wall', '_button', '_carpet', '_sign', '_wall_sign'):
        if n.endswith(suf):
            b = n[:-len(suf)]
            for c in (b, b + 's', b + '_block', b.replace('brick', 'bricks')):
                if c in BASE: return BASE[c]
            return (90, 80, 90)
    for key in ('glass', 'ice', 'candle', 'chain', 'lantern', 'copper', 'wool', 'concrete', 'terracotta', 'skull', 'head', 'banner'):
        if key in n: return {'glass': (90, 70, 110), 'ice': (140, 180, 235), 'candle': (255, 40, 40), 'chain': (90, 90, 100),
                             'lantern': (90, 230, 240), 'copper': (90, 150, 120), 'wool': (200, 200, 200), 'concrete': (60, 60, 60),
                             'terracotta': (150, 80, 60), 'skull': (230, 230, 220), 'head': (230, 230, 220), 'banner': (160, 20, 30)}[key]
    return (120, 100, 120)


def classify(tags):
    t = set(tags)
    if 'bm.gate' in t or 'bm.adoor' in t: return 'gate'
    if 'bm.pz' in t: return 'pz'
    for k in ('sigil', 'target', 'wsp', 'echo', 'socket', 'bulb', 'seq', 'lo'):
        if f'bm.pet_{k}' in t: return k
    if 'bm.pe' in t: return 'other'
    if 'bm.uhs' in t or 'bm.uhsg' in t or 'bm.uhoard' in t: return 'hidden'
    if 'bm.urelic' in t: return 'relic'
    if 'bm.uvoice' in t: return 'voice'
    if 'bm.ueye' in t: return 'eye'
    if 'bm.vaultm' in t: return 'vault'
    if 'bm.zone_d' in t: return 'zone'
    if 'bm.sdoor' in t or 'bm.sbtn' in t: return 'sdoor'
    if 'bm.urift' in t: return 'rift'
    if 'bm.uwell' in t: return 'well'
    if 'bm.entr' in t or 'bm.ugate' in t: return 'entr'
    return 'other'


def label(tags):
    for t in tags:
        if t.startswith('bm.pz') and t[5:].isdigit(): return t[5:]
        if t.startswith('bm.g') and t[4:].isdigit(): return t[4:]
    return ''


def grid(B):
    sx, sy, sz = B.size
    pal, idx = [(0, 0, 0)], {}
    A = np.zeros((sx, sy, sz), np.int16)          # 0 unset, -1 air, else palette index
    for (x, y, z), st in B.b.items():
        c = colour(st)
        if c is None: A[x, y, z] = -1; continue
        if c not in idx: idx[c] = len(pal); pal.append(c)
        A[x, y, z] = idx[c]
    return A, np.array(pal, np.int32)


def topdown(B, A, pal, y0, y1, title, path, band=-1):
    sx, sy, sz = A.shape
    sub = A[:, y0:y1 + 1, :]
    img = np.zeros((sz, sx, 3), np.uint8)
    img[:] = (22, 16, 24)
    isair = sub == -1
    solid = sub > 0
    below = np.concatenate([A[:, max(0, y0 - 1):y0, :] if y0 > 0 else np.zeros((sx, 1, sz), np.int16), sub[:, :-1, :]], axis=1)
    floor = isair & (below > 0)
    anyset = (sub != 0).any(axis=1)
    img[anyset.T] = (44, 38, 48)
    # highest floor in the band
    fy = np.where(floor, np.arange(sub.shape[1])[None, :, None], -1).max(axis=1)
    has = fy >= 0
    xs, zs = np.nonzero(has)
    for x, z in zip(xs, zs):
        yy = fy[x, z]
        c = pal[max(below[x, yy, z], 0)]
        f = 0.7 + 0.6 * (yy / max(1, sub.shape[1] - 1))
        img[z, x] = np.clip(c * f + 30, 0, 255)
    # air with nothing below in band (open drops) shown as deep shade
    drop = isair.any(axis=1) & ~has
    img[drop.T] = (12, 8, 16)
    lava = np.zeros_like(anyset)
    im = Image.fromarray(img).resize((sx * S, sz * S), Image.NEAREST)
    canvas = Image.new('RGB', (sx * S + 20, sz * S + 100), (10, 8, 12))
    canvas.paste(im, (10, 50))
    d = ImageDraw.Draw(canvas)
    d.text((10, 8), title, font=F(18), fill=(240, 220, 225))
    for gx in range(0, sx + 1, 16):
        d.line([10 + gx * S, 50, 10 + gx * S, 50 + sz * S], fill=(48, 40, 52))
        d.text((10 + gx * S + 2, 34), str(gx), font=F(10), fill=(140, 130, 140))
    for gz in range(0, sz + 1, 16):
        d.line([10, 50 + gz * S, 10 + sx * S, 50 + gz * S], fill=(48, 40, 52))
        d.text((12, 50 + gz * S + 1), str(gz), font=F(10), fill=(140, 130, 140))
    marks(B, d, lambda m: y0 <= m[1] <= y1 + 1, lambda m: (10 + m[0] * S, 50 + m[2] * S))
    for (bands, nm, x, z) in LABELS:
        if band in bands:
            d.text((10 + x * S + 1, 50 + z * S + 1), nm, font=F(13), fill=(0, 0, 0))
            d.text((10 + x * S, 50 + z * S), nm, font=F(13), fill=(255, 236, 200))
    legend(d, 10, 50 + sz * S + 4)
    canvas.save(path)


def legend(d, x, y):
    for k in ('gate', 'pz', 'sigil', 'target', 'wsp', 'echo', 'socket', 'bulb', 'seq', 'hidden', 'relic', 'sdoor', 'vault', 'voice', 'eye', 'rift', 'well', 'entr'):
        c, ch = MK[k]
        d.ellipse([x, y + 3, x + 8, y + 11], fill=c)
        t = {'pz': 'controller (P#)', 'gate': 'gate (G#)', 'wsp': 'wave spawn', 'sdoor': 'secret door/btn', 'entr': 'entrance/gate'}.get(k, k)
        d.text((x + 11, y), t, font=F(11), fill=(200, 190, 200))
        x += 22 + 7 * len(t)
        if x > 820: x, y = 10, y + 16


LABELS = [((0,), 'THE APPROACH CAVE', 196, 222), ((0,), 'the Hidden Gate', 160, 196), ((0, 1), 'tunnel', 154, 186),
          ((0,), 'rim + caged balcony', 118, 172), ((0, 1, 2, 3, 4, 5), 'HALL OF CHAINS', 92, 146), ((0,), 'secret 1', 100, 190),
          ((1,), 'Frozen landing', 70, 158), ((1,), 'P2 FROZEN FALLS', 30, 146), ((1,), 'P3 ICE BRIDGE', 28, 108),
          ((1,), 'P4 THRALLS', 30, 74), ((1,), 'P5 ECHO: SNOWBEAST', 24, 22), ((1,), 'gallery back', 68, 60), ((1,), 'NINE LIVES', 76, 92),
          ((2,), 'THE LANTERN CRAWL (pitch dark)', 92, 66), ((3,), 'Hexed landing', 132, 122), ((3,), 'P6 entry', 152, 146),
          ((3,), 'ERASED ARCHIVE', 150, 106), ((3,), 'P7 INVERTED LIBRARY', 174, 112), ((3,), 'P8 apo', 168, 96),
          ((3,), 'serpent crawl', 200, 80), ((3,), 'P9', 212, 170), ((3,), 'OSSUARY', 186, 152), ((3,), 'OSSUARY OF THE UNBOUND', 168, 186),
          ((3,), 'P10 ECHO: WITCH', 142, 192), ((4,), 'Drowned landing', 104, 170), ((4,), 'P11 ledge', 98, 186),
          ((4,), 'THE WARSHIP: P12 deck / P13 gun deck', 94, 220), ((5,), 'P14 HOLD', 106, 220), ((5,), 'P15 ECHO: SAWSHARK', 44, 222),
          ((5,), 'G15 way out', 60, 160), ((5, 6), 'FORGE', 150, 158), ((5, 6), 'P16 THRONE GATE', 120, 124),
          ((6,), 'P17 STAIR OF A THOUSAND EYES', 120, 100), ((6,), 'ANTECHAMBER', 130, 84), ((6,), 'LAST LIGHT', 60, 90),
          ((6,), 'THE THRONE OF THE DREAD', 130, 66), ((6,), 'HOARD', 128, 2), ((6,), 'throne + dais', 126, 18)]


def marks(B, d, keep, at):
    for m in B.meta['markers']:
        if not keep(m): continue
        k = classify(m[3])
        if k == 'zone':
            px, py = at(m); d.ellipse([px - 2, py - 2, px + 2, py + 2], outline=MK[k][0]); continue
        c, ch = MK[k]
        px, py = at(m)
        r = 2 if k == 'eye' else 4
        d.ellipse([px - r, py - r, px + r, py + r], fill=c, outline=(0, 0, 0))
        lb = (ch + label(m[3])) if k != 'eye' else ''
        if lb: d.text((px + 5, py - 6), lb, font=F(11), fill=c)


def section(B, A, pal, axis, at_, title, path, thick=0):
    sx, sy, sz = A.shape
    if axis == 'x':           # a N-S section at x = at_ (looking west: north on the left)
        sl = A[at_ - thick:at_ + thick + 1, :, :]
        w = sz
    else:
        sl = A[:, :, at_ - thick:at_ + thick + 1].transpose(2, 1, 0)
        w = sx
    # nearest cell to the viewer that is set
    img = np.zeros((sy, w, 3), np.uint8); img[:] = (22, 16, 24)
    for i in range(sl.shape[0]):
        layer = sl[i]                                  # (sy, w) after transpose? layer is (sy, sz) for x / (sy, sx) for z
        if axis == 'x': layer = sl[i]                  # shape (sy, sz)
        m = layer > 0
        col = pal[np.clip(layer, 0, None)]
        a = layer == -1
        img[a & (img.sum(axis=2) == 22 + 16 + 24)] = (8, 6, 10)
        img[m] = col[m]
    img = img[::-1]
    im = Image.fromarray(img).resize((w * S, sy * S), Image.NEAREST)
    canvas = Image.new('RGB', (w * S + 20, sy * S + 60), (10, 8, 12))
    canvas.paste(im, (10, 50))
    d = ImageDraw.Draw(canvas)
    d.text((10, 8), title, font=F(18), fill=(240, 220, 225))
    for gy in range(0, sy + 1, 8):
        d.text((12, 50 + (sy - gy) * S - 6), str(gy), font=F(10), fill=(140, 130, 140))
    for g in range(0, w + 1, 16):
        d.text((10 + g * S, 34), str(g), font=F(10), fill=(140, 130, 140))
    if axis == 'x':
        marks(B, d, lambda m: abs(m[0] - at_ - 0.5) <= thick + 6, lambda m: (10 + m[2] * S, 50 + (sy - m[1]) * S))
    else:
        marks(B, d, lambda m: abs(m[2] - at_ - 0.5) <= thick + 6, lambda m: (10 + m[0] * S, 50 + (sy - m[1]) * S))
    canvas.save(path)


BANDS = [('approach + tunnel + rim', 88, 108), ('frozen ward', 74, 98), ('lantern maze + north turn', 60, 72), ('hexed ward', 48, 72),
         ('drowned ward (decks)', 30, 48), ('drowned hold + echo, hub floor', 16, 30), ('throne, antechamber, eye stair', 11, 30)]


def main():
    from p2.dungeons import undercrown
    os.makedirs(OUT, exist_ok=True)
    t = time.time()
    B = undercrown.build()
    print(f'built in {time.time() - t:.1f}s: {len(B.b)} cells, {len(B.meta["markers"])} markers')
    A, pal = grid(B)
    for i, (nm, y0, y1) in enumerate(BANDS):
        topdown(B, A, pal, y0, y1, f'THE UNDERCROWN - {nm} (y {y0}..{y1}), north up', os.path.join(OUT, f'top_{i}.png'), band=i)
    section(B, A, pal, 'x', 112, 'N-S section at x=112 (north left)', os.path.join(OUT, 'sec_ns_112.png'))
    section(B, A, pal, 'z', 145, 'E-W section at z=145 (west left)', os.path.join(OUT, 'sec_ew_145.png'))
    section(B, A, pal, 'z', 42, 'E-W section at z=42: the Throne (west left)', os.path.join(OUT, 'sec_ew_42.png'))
    section(B, A, pal, 'z', 205, 'E-W section at z=205: the Drowned Ward (west left)', os.path.join(OUT, 'sec_ew_205.png'))
    section(B, A, pal, 'x', 42, 'N-S section at x=42: the Frozen Ward (north left)', os.path.join(OUT, 'sec_ns_42.png'))
    section(B, A, pal, 'x', 188, 'N-S section at x=188: the Hexed Ward (north left)', os.path.join(OUT, 'sec_ns_188.png'))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
