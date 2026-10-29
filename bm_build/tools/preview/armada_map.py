"""Top-down maps of the Vorn Armada's built template (p2/dungeons/armada.py).

    python3 tools/preview/armada_map.py [out_dir]

plan.png    the fleet from above: each column's top block in its colour (shaded by height), the hard-light bridges drawn in, the
            ships named. floors.png: every floor a player walks (the highest one in each column), the trial controllers (P#), the
            gates (G#), the elements, the hidden rooms, the pads and the rest as dots, labelled. Both north up."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
import undercrown_map as UM

OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/user/main/previews/v299_armada/ship'
S = 4
F = UM.F
UM.BASE.update({
    'verdant_froglight': (190, 240, 170), 'ochre_froglight': (250, 225, 150), 'orange_concrete': (240, 110, 20), 'red_concrete': (160, 35, 35),
    'orange_glazed_terracotta': (220, 140, 60), 'red_glazed_terracotta': (180, 50, 40), 'glowstone': (250, 210, 120), 'gray_concrete': (60, 64, 70),
    'black_concrete': (14, 16, 20), 'iron_block': (210, 210, 215), 'lime_concrete': (100, 200, 30), 'red_terracotta': (145, 60, 45),
    'moss_block': (90, 110, 45), 'sculk': (20, 40, 50), 'slime_block': (120, 200, 90), 'glass': (180, 220, 230), 'lime_stained_glass': (130, 220, 60),
    'green_stained_glass': (90, 130, 40), 'light_blue_stained_glass': (110, 160, 220), 'cyan_terracotta': (90, 95, 95), 'white_concrete': (220, 225, 228),
    'light_gray_concrete': (130, 130, 125), 'sea_lantern': (200, 230, 225), 'purpur_block': (170, 125, 170), 'waxed_cut_copper': (190, 110, 80),
    'waxed_copper_block': (195, 105, 75), 'blast_furnace': (100, 100, 105), 'green_terracotta': (75, 85, 40), 'redstone_block': (180, 20, 10),
    'red_nether_bricks': (110, 18, 22), 'cyan_concrete': (20, 120, 135), 'yellow_concrete': (240, 175, 20), 'magenta_concrete': (170, 50, 160),
    'grass_block': (100, 150, 60), 'lime_terracotta': (105, 120, 50), 'end_stone': (220, 220, 160), 'polished_diorite': (200, 200, 200)})
MK = {'gate': ((255, 60, 60), 'G'), 'pz': ((255, 220, 60), 'P'), 'target': ((255, 140, 40), 'T'), 'wsp': ((255, 90, 160), 'w'),
      'vboss': ((255, 40, 255), 'B'), 'sock': ((255, 255, 255), 'O'), 'conduit': ((255, 80, 80), 'C'), 'hidden': ((190, 100, 255), 'H'),
      'relic': ((220, 160, 255), 'R'), 'voice': ((255, 120, 120), 'v'), 'vault': ((80, 255, 120), 'V'), 'sdoor': ((255, 255, 0), 'X'),
      'bulb': ((255, 170, 70), 'b'), 'seq': ((120, 200, 255), 'q'), 'lo': ((200, 200, 255), 'l'), 'lever': ((255, 200, 120), 'L'),
      'rift': ((120, 255, 255), 'r'), 'pad': ((160, 255, 160), 'p'), 'entr': ((60, 255, 60), 'IN'), 'sentry': ((255, 30, 30), 's'),
      'pylon': ((255, 230, 120), 'Y'), 'helm': ((255, 255, 120), 'HELM'), 'misc': ((200, 200, 200), ''), 'zone': ((70, 70, 120), '')}
NAMES = {'dock': 'THE DOCK', 'brood': 'THE BROOD-CARRIER', 'forge': 'THE STAR-FORGE', 'nav': 'THE NAVIGATOR', 'dread_a': 'DREADNOUGHT A',
         'dread_b': 'DREADNOUGHT B', 'flag': 'THE FLAGSHIP'}


def classify(tags):
    t = set(tags)
    if 'bm.gate' in t or 'bm.adoor' in t: return 'gate'
    if 'bm.pz' in t: return 'pz'
    for k in ('target', 'wsp', 'vboss', 'sock', 'conduit', 'bulb', 'seq', 'lo', 'lever'):
        if f'bm.pet_{k}' in t: return k
    if 'bm.pe' in t: return 'misc'
    if 'bm.ahs' in t or 'bm.ahsg' in t or 'bm.avault' in t: return 'hidden'
    if 'bm.arelic' in t: return 'relic'
    if 'bm.avoice' in t: return 'voice'
    if 'bm.vaultm' in t: return 'vault'
    if 'bm.zone_d' in t: return 'zone'
    if 'bm.sdoor' in t or 'bm.sbtn' in t: return 'sdoor'
    if 'bm.arift' in t or 'bm.ahome' in t: return 'rift'
    if 'bm.apad' in t: return 'pad'
    if 'bm.entr' in t: return 'entr'
    if 'bm.asentry' in t: return 'sentry'
    if 'bm.apylon' in t: return 'pylon'
    if 'bm.ahelm' in t: return 'helm'
    return 'misc'


def label(tags):
    for t in tags:
        if t.startswith('bm.pz') and t[5:].isdigit(): return t[5:]
        if t.startswith('bm.g') and t[4:].isdigit(): return t[4:]
    return ''


def canvas_for(img, title):
    sz, sx = img.shape[:2]
    im = Image.fromarray(img).resize((sx * S, sz * S), Image.NEAREST)
    cv = Image.new('RGB', (sx * S + 20, sz * S + 96), (6, 6, 10))
    cv.paste(im, (10, 50))
    d = ImageDraw.Draw(cv)
    d.text((10, 8), title, font=F(18), fill=(220, 255, 210))
    for g in range(0, sx + 1, 16):
        d.text((10 + g * S + 2, 34), str(g), font=F(10), fill=(120, 140, 120))
    for g in range(0, sz + 1, 16):
        d.text((12, 50 + g * S + 1), str(g), font=F(10), fill=(120, 140, 120))
    return cv, d


def bridges(B, d, every=1):
    for (n, x1, y1, z1, x2, y2, z2, blk) in B.meta['armada']['bridges']:
        d.rectangle([10 + x1 * S, 50 + z1 * S, 10 + (x2 + 1) * S - 1, 50 + (z2 + 1) * S - 1], fill=(120, 255, 90), outline=(30, 90, 20))
    seen = set()
    for (n, x1, y1, z1, x2, y2, z2, blk) in B.meta['armada']['bridges']:
        if n in seen: continue
        seen.add(n)
        d.text((10 + x1 * S + 4, 50 + z1 * S - 14), f'bridge {n}', font=F(12), fill=(160, 255, 120))


def ship_labels(B, d):
    for nm, (x1, y1, z1, x2, y2, z2) in B.meta['armada']['ships'].items():
        cx, cz = (x1 + x2) / 2, (z1 + z2) / 2
        t = NAMES[nm]
        d.text((10 + cx * S - len(t) * 4 + 1, 50 + cz * S + 1), t, font=F(14), fill=(0, 0, 0))
        d.text((10 + cx * S - len(t) * 4, 50 + cz * S), t, font=F(14), fill=(255, 240, 200))


def plan(B, path):
    sx, sy, sz = B.size
    top = np.full((sx, sz), -1, np.int32)
    col = np.zeros((sx, sz, 3), np.float32)
    for (x, y, z), st in B.b.items():
        if st.endswith(':air') or 'light[' in st: continue
        if y > top[x, z]:
            c = UM.colour(st)
            if c is None: continue
            top[x, z] = y; col[x, z] = c
    img = np.zeros((sz, sx, 3), np.uint8); img[:] = (4, 4, 8)
    rng = np.random.default_rng(1)
    st_ = rng.random((sz, sx)) < 0.004
    img[st_] = (150, 150, 170)
    has = top >= 0
    f = 0.55 + 0.75 * (np.clip(top, 30, 95) - 30) / 65.0
    shaded = np.clip(col * f[..., None], 0, 255).astype(np.uint8)
    img[has.T] = shaded.transpose(1, 0, 2)[has.T]
    cv, d = canvas_for(img, 'THE VORN ARMADA - the fleet from above (top blocks, brighter = higher), the hard-light bridges in green; north up')
    bridges(B, d)
    ship_labels(B, d)
    cx, cy, cz = B.meta['armada']['star']
    d.text((10 + cx * S - 40, 50 + cz * S - 6), 'THE HIVE-STAR', font=F(14), fill=(40, 10, 0))
    cv.save(path)


def floors(B, path):
    sx, sy, sz = B.size
    img = np.zeros((sz, sx, 3), np.uint8); img[:] = (6, 6, 10)
    best = np.full((sx, sz), -1, np.int32)
    colr = np.zeros((sx, sz, 3), np.float32)
    for (x, y, z), st in B.b.items():
        if not st.endswith(':air'): continue
        b = B.b.get((x, y - 1, z))
        if not b or b.endswith(':air') or 'light[' in b: continue
        if not B.b.get((x, y + 1, z), 'minecraft:air').endswith(':air'): continue
        if y > best[x, z]:
            c = UM.colour(b)
            if c is None: continue
            best[x, z] = y; colr[x, z] = c
    anyset = np.zeros((sx, sz), bool)
    for (x, y, z) in B.b: anyset[x, z] = True
    img[anyset.T] = (34, 36, 40)
    has = best >= 0
    f = 0.6 + 0.5 * (np.clip(best, 40, 60) - 40) / 20.0
    sh = np.clip(colr * f[..., None] + 25, 0, 255).astype(np.uint8)
    img[has.T] = sh.transpose(1, 0, 2)[has.T]
    cv, d = canvas_for(img, 'THE VORN ARMADA - the floors (highest walkable in each column) and every marker; north up')
    bridges(B, d)
    for m in B.meta['markers']:
        k = classify(m[3])
        px, py = 10 + m[0] * S, 50 + m[2] * S
        c, ch = MK[k]
        if k == 'zone':
            d.ellipse([px - 2, py - 2, px + 2, py + 2], outline=c); continue
        r = 2 if k in ('sentry', 'misc') else 4
        d.ellipse([px - r, py - r, px + r, py + r], fill=c, outline=(0, 0, 0))
        lb = ch + label(m[3])
        if lb and k not in ('sentry',): d.text((px + 5, py - 6), lb, font=F(11), fill=c)
    ship_labels(B, d)
    x, y = 10, 50 + sz * S + 6
    for k in ('gate', 'pz', 'lever', 'seq', 'bulb', 'lo', 'target', 'wsp', 'vboss', 'sock', 'conduit', 'sentry', 'pylon', 'helm', 'hidden',
              'relic', 'sdoor', 'vault', 'voice', 'rift', 'pad', 'entr'):
        c, ch = MK[k]
        d.ellipse([x, y + 3, x + 8, y + 11], fill=c)
        t = {'pz': 'controller P#', 'gate': 'gate G#', 'wsp': 'spawn', 'sdoor': 'secret', 'entr': 'arrival', 'rift': 'rift/home',
             'hidden': 'hidden door/sigil'}.get(k, k)
        d.text((x + 11, y), t, font=F(11), fill=(200, 210, 200))
        x += 22 + 7 * len(t)
        if x > sx * S - 80: x, y = 10, y + 16
    cv.save(path)


def main():
    from p2.dungeons import armada
    os.makedirs(OUT, exist_ok=True)
    B = armada.build()
    plan(B, os.path.join(OUT, 'map_plan.png'))
    floors(B, os.path.join(OUT, 'map_floors.png'))
    print('wrote', OUT)


if __name__ == '__main__':
    main()
