"""2.25: a vanilla-style finishing pass for the pack's 2D item textures.

Every icon keeps its exact silhouette and design; only the colouring changes, the way Mojang's item art is coloured:
  - light falls from the top-left: the top/left edge of each colour region steps up a shade, the bottom/right edge
    steps down one, and the outermost bottom/right pixels down two;
  - shades shift hue as they change brightness (highlights a little warmer, shadows a little cooler and more
    saturated) instead of just going lighter/darker;
  - black outlines become a dark shade of the colour they wrap (vanilla items almost never use pure black);
  - pinholes (1-2 transparent pixels enclosed by the sprite) are filled.
Hand-made replacements (built from vanilla sprites and colour ramps) are in OVERRIDES."""
import colorsys
from PIL import Image

SKIP = {'rat_chef', 'rat_lucky', 'rat_pirate', 'rat_prof', 'rat_soldier', 'rat_familiar', 'blue_marlin', 'bloomheart_gem', 'cecil_gem'}
V = '/home/claude/mc263/client/assets/minecraft/textures/item/'


def _lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def shade(c, step):
    """step > 0: lighter and warmer; step < 0: darker, cooler, a touch more saturated"""
    r, g, b = (v / 255 for v in c[:3])
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08:                                  # greys: plain lightness steps (vanilla iron, stone)
        l = min(0.97, max(0.04, l + 0.11 * step))
    else:
        warm, cool = 1 / 6, 2 / 3                 # yellow / blue
        target = warm if step > 0 else cool
        d = ((target - h + 0.5) % 1) - 0.5
        h = (h + d * 0.06 * abs(step)) % 1
        l = min(0.95, max(0.05, l + (0.10 if step > 0 else 0.11) * step))
        s = min(1, max(0, s + (-0.04 if step > 0 else 0.05) * abs(step)))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (round(r * 255), round(g * 255), round(b * 255), c[3] if len(c) > 3 else 255)


def _fill_pinholes(im):
    w, h = im.size
    px = im.load()
    seen = set()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] or (x, y) in seen: continue
            comp, stack, edge = [], [(x, y)], False
            seen.add((x, y))
            while stack:
                cx, cy = stack.pop(); comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if not (0 <= nx < w and 0 <= ny < h): edge = True; continue
                    if px[nx, ny][3] == 0 and (nx, ny) not in seen:
                        seen.add((nx, ny)); stack.append((nx, ny))
            if not edge and len(comp) <= 2:
                for cx, cy in comp:
                    ns = [px[nx, ny] for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)) if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3]]
                    ns.sort(key=_lum)
                    px[cx, cy] = ns[len(ns) // 2]


def process(name, im):
    if name in SKIP: return im
    if name in OVERRIDES: return OVERRIDES[name]()
    im = im.convert('RGBA').copy()
    w, h = im.size
    if w != 16 or h != 16: return im                # paintings, maps and other big art keep their own look
    _fill_pinholes(im)
    src = im.load()
    out = im.copy(); px = out.load()
    alpha = lambda x, y: 0 <= x < w and 0 <= y < h and src[x, y][3] > 0
    col = lambda x, y: src[x, y] if alpha(x, y) else None
    dark = lambda c: c is not None and _lum(c) < 40
    for y in range(h):
        for x in range(w):
            c = src[x, y]
            if not c[3]: continue
            if dark(c) and any(not alpha(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                # a black OUTER outline pixel: a deep shade of the colour it wraps (interior detail lines stay as drawn)
                ns = [col(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))]
                ns = [n for n in ns if n is not None and not dark(n)]
                if ns:
                    base = max(ns, key=lambda n: colorsys.rgb_to_hls(*(v / 255 for v in n[:3]))[2])
                    hh, ll, ss = colorsys.rgb_to_hls(*(v / 255 for v in base[:3]))
                    r, g, b = colorsys.hls_to_rgb(hh, max(0.07, min(0.16, ll * 0.3)), min(1, ss * 0.9))
                    px[x, y] = (round(r * 255), round(g * 255), round(b * 255), 255)
                continue
            if dark(c): continue
            # lit as one object: only the sprite's outer edge (transparency or its outline) catches light or falls into shadow
            edge = lambda dx, dy: not alpha(x + dx, y + dy) or dark(col(x + dx, y + dy))
            step = 0
            if edge(0, -1) or edge(-1, 0): step += 1
            if edge(0, 1) or edge(1, 0): step -= 1
            if not alpha(x, y + 1) and not alpha(x + 1, y): step -= 1     # the outer bottom-right corner
            if step: px[x, y] = shade(c, step)
    return out


# ===================================================================== hand-made replacements
def _load(p):
    im = Image.open(p).convert('RGBA'); return im.crop((0, 0, im.width, im.width))


def _ramp(p):
    return sorted({c for c in _load(p).getdata() if c[3] > 0}, key=_lum)


def _recolor(im, r):
    src = sorted({c for c in im.getdata() if c[3] > 0}, key=_lum)
    m = {c: tuple(r[round(i / max(1, len(src) - 1) * (len(r) - 1))][:3]) + (255,) for i, c in enumerate(src)}
    out = im.copy(); out.putdata([m[c] if c[3] else c for c in im.getdata()]); return out


H = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def _paint(im, rows, pal, x0=0, y0=0):
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': im.putpixel((x0 + x, y0 + y), pal[ch])
    return im


def staff_of_sparks():
    st = _recolor(_load(V + 'breeze_rod.png'), _ramp(V + 'copper_ingot.png'))
    for y in range(0, 5):
        for x in range(11, 16): st.putpixel((x, y), (0, 0, 0, 0))
    return _paint(st, ['..W..', '.1L2.', '012L.', '.012.', '..0..'],
                  {'W': H('#ffffff'), 'L': H('#a8ecff'), '2': H('#5ec3ea'), '1': H('#2e86b5'), '0': H('#1b4b6b')}, 11, 0)


def gravewell_staff():
    gw = _recolor(_load(V + 'blaze_rod.png'), [H('#100914'), H('#1e1428'), H('#3b2a4f'), H('#5d4880'), H('#8a72b0')])
    for y in range(0, 6):
        for x in range(10, 16): gw.putpixel((x, y), (0, 0, 0, 0))
    return _paint(gw, ['..vvv.', '.vkkkv', 'vkpkkv', 'vkkkkd', '.vkkd.', '..dd..'],
                  {'v': H('#8a5ad0'), 'd': H('#5a2e96'), 'k': H('#0a0410'), 'p': H('#d6b8ff')}, 10, 0)


def crescent_staff():
    g = [c[:3] + (255,) for c in _ramp(V + 'gold_ingot.png')]
    cs = _recolor(_load(V + 'stick.png'), [H('#1e120c'), H('#3a2418'), H('#5a3a28'), H('#7a5238')])
    for y in range(0, 9):
        for x in range(6, 16): cs.putpixel((x, y), (0, 0, 0, 0))
    rows = ['........3.......',
            '.......32....p4.',
            '.......21...pPp4',
            '.......21..pPPp.',
            '..33222110.mPp..',
            '...1111100m.....',
            '........0011111.',
            '.......w012222.3',
            '.........11.....',
            '.........12.....',
            '..........2.....']
    return _paint(cs, rows, {'P': H('#ec7ab8'), 'p': H('#c04a8a'), '4': H('#ffd0ea'), 'm': H('#8a2a5e'), '0': g[1], '1': g[3], '2': g[5], '3': g[-1], 'w': H('#5a3a28')})


def _bowl(soup):
    """the vanilla stew bowl with its soup recoloured onto a 5-step ramp (dark to light), plus any flecks"""
    ch = _load(V + 'mushroom_stew.png'); bowl = _load(V + 'bowl.png')
    ramp, flecks = soup
    for y in range(16):
        for x in range(16):
            c, b = ch.getpixel((x, y)), bowl.getpixel((x, y))
            if c[3] and c != b: ch.putpixel((x, y), ramp[min(4, int(_lum(c) / 256 * 5))])
    for (x, y), colr in flecks: ch.putpixel((x, y), colr)
    return ch


def dish_chili():
    return _bowl(([H('#5a0e08'), H('#8a1a0c'), H('#b8321a'), H('#e0582a'), H('#ff8a3a')], [((6, 6), H('#ffd23f')), ((9, 7), H('#ffd23f')), ((8, 6), H('#3a6a1a'))]))


def dish_chowder():
    return _bowl(([H('#8a8270'), H('#b8ae96'), H('#d8d0b8'), H('#efe8d4'), H('#ffffff')], [((6, 6), H('#e8a050')), ((9, 6), H('#3ad8d0')), ((8, 7), H('#e8a050'))]))


def ocarina():
    oca = Image.new('RGBA', (16, 16))
    return _paint(oca, ['................', '................', '................', '.............kk.', '......kkkkk.kBbk', '....kkbBBbbkkbbk',
                        '...kbBWBbbbbbbk.', '..kbBBhbbBhbbbk.', '..kbBbbbbbbbbdk.', '..kbbbhbbhbbdk..', '...kbbbbbbddk...', '....kkdddddk....', '......kkkk......',
                        '................', '................', '................'],
                  {'k': H('#1c2a4a'), 'b': H('#3a5aa0'), 'B': H('#6a92d8'), 'W': H('#a8c8ff'), 'd': H('#2a4280'), 'h': H('#0e1426')})


def skiff_key():
    """the saucer-headed key, coloured like vanilla iron with a green core"""
    k = Image.new('RGBA', (16, 16))
    rows = ['................',
            '................',
            '......4444......',
            '....43332222....',
            '..433gG3g2221...',
            '.43333333322211.',
            '..1111111111....',
            '.......32.......',
            '.......3e.......',
            '.......32.......',
            '.......3211.....',
            '.......32.......',
            '.......3211.....',
            '.......321......',
            '.......00.......',
            '................']
    return _paint(k, rows, {'4': H('#e6ebf0'), '3': H('#c2c9d2'), '2': H('#8e97a4'), '1': H('#5a626e'), '0': H('#33383f'),
                            'g': H('#7dff6a'), 'G': H('#d8ffd0'), 'e': H('#3ad040')})


OVERRIDES = {'staff_of_sparks': staff_of_sparks, 'gravewell_staff': gravewell_staff, 'crescent_staff': crescent_staff,
             'dish_chili': dish_chili, 'dish_chowder': dish_chowder, 'ocarina': ocarina, 'skiff_key': skiff_key}


# ===================================================================== the Vorn Skiff's own textures (the model is unchanged)
SKIFF_PAINT = {'green': ('#c4c9d0', '#a4acb6'), 'crimson': ('#b3352c', '#8e2620'), 'gold': ('#e3b23c', '#c08e22'),
               'midnight': ('#3a3256', '#2a2440'), 'ocean': ('#3f9196', '#2c7378'), 'rose': ('#e483b0', '#c8608e')}


def _hex(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) + (255,)


def _plates(base, seed):
    """riveted hull plates: a staggered seam pattern, a highlight under each seam, rivets at the plate corners"""
    import random
    rnd = random.Random(seed)
    b = _hex(base)
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            n = rnd.randint(-3, 3)
            im.putpixel((x, y), tuple(max(0, min(255, v + n)) for v in b[:3]) + (255,))
    seam, lit, rivet = shade(b, -1), shade(b, 0.5), shade(b, 1.5)
    for x in range(16):
        im.putpixel((x, 0), seam); im.putpixel((x, 8), seam); im.putpixel((x, 1), lit); im.putpixel((x, 9), lit)
    for y in range(1, 8): im.putpixel((0, y), seam); im.putpixel((1, y), lit) if y > 1 else None
    for y in range(9, 16): im.putpixel((8, y), seam); im.putpixel((9, y), lit) if y > 9 else None
    for (x, y) in ((3, 3), (13, 3), (3, 6), (13, 6), (5, 11), (11, 11), (5, 14), (11, 14)): im.putpixel((x, y), rivet)
    return im


def _belly(seed):
    """the underside: dark gunmetal with two rows of cooling vents"""
    im = _plates('#4a4e56', seed)
    v, vl = _hex('#202328'), _hex('#6a707a')
    for y in (4, 12):
        for x in range(2, 15):
            if x % 3 != 1: im.putpixel((x, y), v); im.putpixel((x, y + 1), vl)
    return im


def textures():
    T = {}
    for i, (k, (hull, deck)) in enumerate(SKIFF_PAINT.items()):
        T[f'skiff_{k}_hull'] = _plates(hull, 100 + i)
        T[f'skiff_{k}_deck'] = _plates(deck, 200 + i)
    T['skiff_belly'] = _belly(5)
    return T
