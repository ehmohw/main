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


# ===================================================================== 2.25b: vanilla sprites as bases (keys, bottles, boots, the maul, emblems)
def ramp(base, n=7, mid=None):
    """an n-step vanilla-style ramp around a base colour: darker steps cooler and more saturated, lighter steps warmer"""
    b = _hex(base) if isinstance(base, str) else base
    mid = n // 2 if mid is None else mid
    return [shade(b, (i - mid) * 0.9) for i in range(n)]


TRIAL_SHAFT = ['54281a', '6d3421', '84432d', '9a5038', 'c15a36', 'd67b5b', 'fc9982']
OMINOUS_SHAFT = ['2f4a42', '36594d', '396e59', '3e816b', '55a386', '69c09c', '7bdbb0']
KEY_HEAD = ['292828', '373b35', '454a42', '525a51', '6c716b', '85837a', 'a19e94']


def _swap(im, src_hexes, dst):
    m = {_hex('#' + h)[:3]: dst[i] for i, h in enumerate(src_hexes)}
    out = im.copy()
    out.putdata([m.get(c[:3], c) if c[3] else c for c in im.getdata()])
    return out


def key(shaft, eyes=None, head=None, ominous=False):
    """a trial key (or ominous trial key) with its shaft in another colour - a dungeon key variant"""
    im = _load(V + ('ominous_trial_key.png' if ominous else 'trial_key.png'))
    im = _swap(im, OMINOUS_SHAFT if ominous else TRIAL_SHAFT, ramp(shaft, 7, 4))
    if head: im = _swap(im, KEY_HEAD, ramp(head, 7, 4))
    if eyes:
        e = ramp(eyes, 3, 1)
        im = _swap(im, ['de4058', '9a1e33'] if ominous else ['ff9951'], [e[2], e[0]] if ominous else [e[2]])
    return im


def bottle(liquid, extra=()):
    """the vanilla potion bottle, its liquid (the grey overlay) tinted like a vanilla potion"""
    im = _load(V + 'potion.png'); ov = _load(V + 'potion_overlay.png')
    t = _hex(liquid)
    for y in range(16):
        for x in range(16):
            c = ov.getpixel((x, y))
            if c[3]: im.putpixel((x, y), tuple(min(255, round(t[i] * c[i] / 255 * 1.08)) for i in range(3)) + (255,))
    for (x, y), colr in extra: im.putpixel((x, y), _hex(colr))
    return im


def boots(base, sole=None, trim=None):
    """vanilla iron boots, recoloured; an optional sole/blade line under them and a trim at the cuffs"""
    im = _recolor(_load(V + 'iron_boots.png'), ramp(base, 6, 3))
    if trim:
        for x in (4, 5, 6, 9, 10, 11): im.putpixel((x, 3), _hex(trim))
    if sole:
        kind, colr = sole
        c, d = _hex(colr), shade(_hex(colr), -1.5)
        if kind == 'blade':                                   # skate blades with a curled toe
            for x in list(range(1, 6)) + list(range(10, 15)): im.putpixel((x, 13), c)
            im.putpixel((0, 12), c); im.putpixel((15, 12), c)
            for x in list(range(1, 6)) + list(range(10, 15)): im.putpixel((x, 14), d) if x in (2, 4, 11, 13) else None
        elif kind == 'glow':                                  # glowing soles
            for x in list(range(1, 7)) + list(range(9, 15)): im.putpixel((x, 13), c)
            for x in (2, 4, 11, 13): im.putpixel((x, 14), d)
        elif kind == 'spring':                                # coiled springs under the heels
            for x0 in (2, 11):
                for dy, xs in ((13, (x0, x0 + 2)), (14, (x0 + 1,)), (15, (x0, x0 + 2))):
                    for x in xs: im.putpixel((x, dy), c if dy != 14 else d)
        elif kind == 'wave':                                  # a curl of water under each boot
            for x in (1, 3, 5, 10, 12, 14): im.putpixel((x, 13), c)
            for x in (2, 4, 11, 13): im.putpixel((x, 14), d)
    return im


def quake_maul():
    """the vanilla mace, its head in Vorn red, the haft in dark iron"""
    im = _load(V + 'mace.png')
    head = [p for p in ((x, y) for y in range(16) for x in range(16)) if im.getpixel(p)[3] and not (p[0] < 7 and p[1] > 6)]
    red = ramp('#c42a22', 6, 3); iron = ramp('#4a4e58', 5, 2)
    hsrc = sorted({im.getpixel(p) for p in head}, key=_lum)
    hand = [p for p in ((x, y) for y in range(16) for x in range(16)) if im.getpixel(p)[3] and p not in head]
    asrc = sorted({im.getpixel(p) for p in hand}, key=_lum)
    out = im.copy()
    for p in head: out.putpixel(p, red[round(hsrc.index(im.getpixel(p)) / max(1, len(hsrc) - 1) * 5)])
    for p in hand: out.putpixel(p, iron[round(asrc.index(im.getpixel(p)) / max(1, len(asrc) - 1) * 4)])
    return out


EMBLEM_SIGN = {   # 6 x 6 symbols (x = light, o = shadow)
    'brood': ['x....x', '.x..x.', 'x.oo.x', '.xxxx.', 'x.xx.x', '.x..x.'],          # a spider
    'frost': ['..x...', 'x.x.x.', '.xxx..', 'xxxxx.', '.xxx..', 'x.x.x.'],          # a snowflake
    'hex':   ['.xxxx.', 'x....x', 'x.oo.x', 'x.oo.x', 'x....x', '.xxxx.'],          # an eye
    'hollow': ['......', 'x.x.x.', 'xxxxx.', 'xoxox.', 'xxxxx.', '......'],         # a crown
    'keep':  ['x.x.x.', 'xxxxx.', '.xxx..', '.xox..', '.xox..', 'xxxxx.'],          # a tower
    'tide':  ['x.x.x.', 'x.x.x.', 'xxxxx.', '..x...', '..x...', '..x...'],          # a trident
}


def emblem(d):
    """a gold medal (gold-ingot ramp), the dungeon's colour inside, its sign in relief"""
    from p2.config import D
    g = ramp('#e8b830', 6, 3); inner = ramp(D[d]['color'], 5, 2)
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            dx, dy = x - 7.5, y - 7.5
            r = (dx * dx + dy * dy) ** 0.5
            lit = -(dx + dy) / 10.6                                 # light from the top-left: +1 .. -1
            if r <= 7.3:
                if r > 6.4: im.putpixel((x, y), g[0] if lit < 0.2 else g[1])                    # the rim's dark edge
                elif r > 5.0: im.putpixel((x, y), g[min(5, max(1, round(3 + lit * 2.4)))])      # the gold band
                elif r > 4.3: im.putpixel((x, y), g[1] if lit > 0 else g[4])                    # the band's inner lip (sunk)
                else: im.putpixel((x, y), inner[min(4, max(0, round(2 + lit * 1.6)))])
    sign = EMBLEM_SIGN[d]
    hi, lo = shade(inner[4], 1.5), inner[0]
    for y, row in enumerate(sign):
        for x, ch in enumerate(row):
            if ch == 'x': im.putpixel((5 + x, 5 + y), hi)
            elif ch == 'o': im.putpixel((5 + x, 5 + y), lo)
    return im


def _register_b():
    from p2.config import D
    for d in ('brood', 'frost', 'hex', 'hollow', 'keep', 'tide', 'lucky'):
        col = {'hollow': '#7a8a9c', 'keep': '#9a4a3a'}.get(d, D[d]['color'])      # (the darkest dungeon colours, lifted so the shaft reads)
        OVERRIDES[f'key_{d}'] = (lambda c=col: key(c, eyes=c))
        OVERRIDES[f'vkey_{d}'] = (lambda c=col: key(c, eyes='#ffffff', head='#c89a2a'))
        OVERRIDES[f'bkey_{d}'] = (lambda c=col: key(c, ominous=True))
        if d != 'lucky': OVERRIDES[f'emblem_{d}'] = (lambda d_=d: emblem(d_))
    OVERRIDES.update({
        'gold_key': lambda: key('#e8b830', eyes='#fff2a0', head='#c89a2a'), 'silver_key': lambda: key('#c8ccd2', eyes='#a8ecff'),
        'mail_key': lambda: key('#c8a050', eyes='#ffd23f'), 'renewal_key': lambda: key('#a8e8f0', eyes='#ffffff', head='#d8dee6'),
        'market_key': lambda: key('#7a3aa8', eyes='#ffd23f', head='#c89a2a'),
        'vial_clear': lambda: bottle('#9ad8ff', [((8, 10), '#ffffff')]), 'vial_rain': lambda: bottle('#3a6ad8', [((7, 11), '#a8c8ff'), ((9, 12), '#a8c8ff')]),
        'vial_storm': lambda: bottle('#3a2a6a', [((8, 9), '#ffe85a'), ((7, 10), '#ffe85a'), ((8, 11), '#ffe85a'), ((7, 12), '#fff6b0')]),
        'soul_vial_zombie': lambda: bottle('#4a9a3a', [((8, 10), '#b8ffb0')]), 'soul_vial_skeleton': lambda: bottle('#d8d8c8', [((8, 10), '#ffffff')]),
        'soul_vial_spider': lambda: bottle('#9a1e1e', [((8, 10), '#ff8a8a'), ((9, 11), '#ff3a3a')]),
        'sanguine_tonic': lambda: bottle('#8a0a1a', [((8, 10), '#ff6a7a')]), 'xp_flask': lambda: bottle('#7dff3a', [((8, 10), '#f4ffb0'), ((9, 12), '#d8ff6a')]),
        'ice_skates': lambda: boots('#7a4a2a', ('blade', '#d8e6f0'), '#f0f0f0'),
        'gravity_boots': lambda: boots('#4a3a6a', ('glow', '#b48cff'), '#c8a0ff'),
        'spring_boots': lambda: boots('#2a8a96', ('spring', '#c8ccd2'), '#7ae8f0'),
        'triple_boots': lambda: boots('#b8302a', ('glow', '#7dff6a'), '#ff8a7a'),
        'water_walking_boots': lambda: boots('#2a5ab8', ('wave', '#9ad8ff'), '#d8f0ff'),
        'quake_maul': quake_maul,
    })


_register_b()
