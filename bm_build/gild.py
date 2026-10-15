"""2.79a: GILDED - a follower's gilded look is polished gold, not yellow cloth.

metal(im) turns any texture into shiny gold: its shading (luminance, stretched over the image's own range) through a
six-stop gold ramp - umber shadow, ochre, gold, bright gold, pale gold, a white-gold glint - with the contrast pushed so the
folds read as burnished metal; then light catches it: a bright rim along each upper and left edge (where the pixel above or
to the left is darker or empty), a thin diagonal sheen every few pixels, and a white glint on the brightest pixels.
Transparency is kept as it is. Every gilded outfit's textures go through it (and the game adds the sparkles)."""
from PIL import Image

RAMP = [(0.00, (0x3a, 0x22, 0x04)), (0.22, (0x78, 0x4c, 0x0a)), (0.45, (0xc0, 0x88, 0x1c)), (0.66, (0xea, 0xb8, 0x38)),
        (0.84, (0xff, 0xe0, 0x7a)), (1.00, (0xff, 0xfa, 0xe0))]
GOLD = '#ffcf40'


def _ramp(t):
    t = max(0.0, min(1.0, t))
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if t <= b:
            f = (t - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * f) for i in range(3))
    return RAMP[-1][1]


def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def metal(im, sheen=11):
    """the texture in polished gold (see the module's note); sheen: the diagonal streaks' spacing, in pixels (0: none)"""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    raw = {(x, y): _lum(px[x, y]) for y in range(h) for x in range(w) if px[x, y][3] > 0}
    if not raw:
        return im.copy()
    # (its shading, softened: a cloth's weave mustn't turn to glitter)
    soft = {}
    for (x, y) in raw:
        nb = [raw[q] for q in ((x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)) if q in raw]
        soft[(x, y)] = sum(nb) / len(nb)
    vals = sorted(soft.values())
    mean = sum(vals) / len(vals)
    spread = max(vals[int(len(vals) * 0.95)] - vals[int(len(vals) * 0.05)], 0.12)
    L = {}
    for q, v in soft.items():
        t = 0.56 + 0.62 * (v - mean) / spread + 0.35 * (raw[q] - v)       # (centred on bright gold; a little of the fine grain kept)
        L[q] = max(0.12, min(0.90, t))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    o = out.load()
    for (x, y), t0 in L.items():
        t = t0
        up, down = soft.get((x, y - 1)), soft.get((x, y + 1))
        if up is None or up < soft[(x, y)] - 0.10: t += 0.18            # (light along the upper edges of its shapes)
        if down is None or down < soft[(x, y)] - 0.10: t -= 0.14        # (and shade under them)
        if sheen and (x + y) % sheen in (0, 1): t += 0.10               # (a sheen across it)
        if t0 >= 0.86 and (x * 7 + y * 13) % 5 == 0: t = 1.0            # (a glint here and there on the brightest)
        o[x, y] = _ramp(t) + (px[x, y][3],)
    return out


def sheet(path, ims):
    """a preview: each texture beside its gilded self, 8x"""
    tiles = [(im, metal(im)) for im in ims]
    W = sum(a.width * 16 + 24 for a, _b in tiles) + 8; H = max(a.height for a, _b in tiles) * 8 + 16
    s = Image.new('RGBA', (W, H), (40, 44, 52, 255)); x = 8
    for a, b in tiles:
        s.alpha_composite(a.resize((a.width * 8, a.height * 8), Image.NEAREST), (x, 8))
        s.alpha_composite(b.resize((b.width * 8, b.height * 8), Image.NEAREST), (x + a.width * 8, 8))
        x += a.width * 16 + 24
    s.save(path)


# ---------------------------------------------------------------- which look is each follower's gilded one (2.79a)
# follower: (its look's number, its item, its score - the current look, on the owner); emma's is a dress, Celi's an outfit, Zib's a uniform
GILDED = {'emma': (6, 'cos_dress_6', 'bm.cosd'), 'celi': (5, 'cos_celi_5', 'bm.cosc'), 'zib': (3, 'cos_zib_3', 'bm.cosz'),
          'cecil': (4, 'cos_cecil_4', 'bm.cosce'), 'kw': (4, 'cos_kw_4', 'bm.cosk'), 'leo': (4, 'cos_leo_4', 'bm.cosl'),
          'demo': (4, 'cos_demo_4', 'bm.cosm'), 'apo': (4, 'cos_apo_4', 'bm.cosap'), 'tul': (4, 'cos_tul_4', 'bm.costu'),
          'frog': (4, 'cos_frog_4', 'bm.cosfg'), 'don': (5, 'cos_don_5', 'bm.cosdn'), 'pearl': (4, 'cos_pearl_4', 'bm.cospm'),
          'wil': (4, 'cos_wil_4', 'bm.coswl'), 'fishy': (4, 'cos_fishy_4', 'bm.cosfy')}
ITEMS = {g[1] for g in GILDED.values()}
TROPHIES = 20                                # its price: 20 Gutter Trophies - 2,560 coins at the Tailor (an aura is 1,280)


def is_gilded(w, k):
    return w in GILDED and GILDED[w][0] == k


def price(iid, plain):
    """a cosmetic's Goldtooth offer price (the Tailor reads it): the gilded ones 20 Gutter Trophies"""
    return ('gutter_trophy', TROPHIES) if iid in ITEMS else plain
