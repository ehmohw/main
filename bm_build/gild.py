"""2.79a: GILDED - a follower's gilded look is polished gold, not yellow cloth. (2.80c: and a diamond look and a netherite
look beside it - the same polish through another metal's ramp: TIERS, LOOKS.)

metal(im) turns any texture into shiny gold: its shading (luminance, stretched over the image's own range) through a
six-stop gold ramp - umber shadow, ochre, gold, bright gold, pale gold, a white-gold glint - with the contrast pushed so the
folds read as burnished metal; then light catches it: a bright rim along each upper and left edge (where the pixel above or
to the left is darker or empty), a thin diagonal sheen every few pixels, and a white glint on the brightest pixels.
Transparency is kept as it is. Every gilded outfit's textures go through it (and the game adds the sparkles)."""
from PIL import Image

RAMP = [(0.00, (0x3a, 0x22, 0x04)), (0.22, (0x78, 0x4c, 0x0a)), (0.45, (0xc0, 0x88, 0x1c)), (0.66, (0xea, 0xb8, 0x38)),
        (0.84, (0xff, 0xe0, 0x7a)), (1.00, (0xff, 0xfa, 0xe0))]
# (2.79b: a diamond ramp - Leo's steel with his Diamond Champion; 2.80c: and the diamond looks themselves)
DIAMOND = [(0.00, (0x06, 0x2c, 0x32)), (0.22, (0x0c, 0x5c, 0x62)), (0.45, (0x18, 0x9c, 0xa0)), (0.66, (0x34, 0xd2, 0xcf)),
           (0.84, (0x8a, 0xf2, 0xea)), (1.00, (0xe6, 0xff, 0xfc))]
# (2.80c: netherite - dark, faintly purple-brown steel; the polish still catches its edges)
NETHERITE = [(0.00, (0x0c, 0x0a, 0x0c)), (0.22, (0x22, 0x1c, 0x20)), (0.45, (0x3c, 0x33, 0x38)), (0.66, (0x5c, 0x50, 0x56)),
             (0.84, (0x8c, 0x7e, 0x85)), (1.00, (0xd8, 0xcc, 0xd2))]
GOLD = '#ffcf40'


def _ramp(t, ramp=RAMP):
    t = max(0.0, min(1.0, t))
    for (a, ca), (b, cb) in zip(ramp, ramp[1:]):
        if t <= b:
            f = (t - a) / (b - a)
            return tuple(int(ca[i] + (cb[i] - ca[i]) * f) for i in range(3))
    return ramp[-1][1]


def _lum(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def metal(im, sheen=11, ramp=RAMP, soften=True):
    """the texture in polished gold (see the module's note); sheen: the diagonal streaks' spacing, in pixels (0: none);
    ramp: another metal's (DIAMOND); soften=False keeps every pixel's own shade (a mail's links)"""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    raw = {(x, y): _lum(px[x, y]) for y in range(h) for x in range(w) if px[x, y][3] > 0}
    if not raw:
        return im.copy()
    # (its shading, softened: a cloth's weave mustn't turn to glitter)
    soft = {}
    for (x, y) in raw:
        nb = [raw[q] for q in (((x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)) if soften else ((x, y),)) if q in raw]
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
        o[x, y] = _ramp(t, ramp) + (px[x, y][3],)
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
          'wil': (4, 'cos_wil_4', 'bm.coswl'), 'fishy': (4, 'cos_fishy_4', 'bm.cosfy'),
          'dennis': (4, 'cos_dennis_4', 'bm.cosdw'), 'pistachio': (4, 'cos_pistachio_4', 'bm.cospi'),
          'omega': (4, 'cos_omega_4', 'bm.cosom'),
          'ashur': (4, 'cos_ashur_4', 'bm.cosas'),
          'chef': (4, 'cos_chef_4', 'bm.coskk'),
          'neighbor': (4, 'cos_neighbor_4', 'bm.cosnb'),
          'ava': (4, 'cos_ava_4', 'bm.cosav'), 'pearlq': (4, 'cos_pearlq_4', 'bm.cospq'), 'bloo': (4, 'cos_bloo_4', 'bm.cosbo'), 'stalker': (4, 'cos_stalker_4', 'bm.cossv'), 'lantern': (4, 'cos_lantern_4', 'bm.cosln')}   # (2.87)
# (2.80c) the diamond and the netherite looks: the next two numbers in each follower's set
_ITEM = {'emma': 'cos_dress_{}', 'celi': 'cos_celi_{}', 'zib': 'cos_zib_{}'}
_K2 = {'emma': 7, 'celi': 6, 'zib': 4, 'don': 6}
DIAMOND_LOOKS = {w: (_K2.get(w, 5), _ITEM.get(w, f'cos_{w}_{{}}').format(_K2.get(w, 5)), sc) for w, (k, i, sc) in GILDED.items()}
NETHERITE_LOOKS = {w: (_K2.get(w, 5) + 1, _ITEM.get(w, f'cos_{w}_{{}}').format(_K2.get(w, 5) + 1), sc) for w, (k, i, sc) in GILDED.items()}
# each metal: its ramp, the steel beside it (Leo's helm and armour - 2.80c: gold with the gold, no longer diamond), its colour, its word, its lore, its price (Gutter Trophies), Wilfrey's armour
TIERS = {'gold': {'ramp': RAMP, 'steel': RAMP, 'col': GOLD, 'word': 'Gilded', 'trophies': 5, 'armour': 'gold',
                  'lore': 'Gilded: polished gold - and it sparkles.', 'looks': GILDED},
         'diamond': {'ramp': DIAMOND, 'steel': DIAMOND, 'col': '#5ee8e0', 'word': 'Diamond', 'trophies': 8, 'armour': 'diamond',
                     'lore': 'Diamond: cut and polished - and it glitters.', 'looks': DIAMOND_LOOKS},
         'netherite': {'ramp': NETHERITE, 'steel': NETHERITE, 'col': '#9a8a92', 'word': 'Netherite', 'trophies': 12, 'armour': 'netherite',
                       'lore': 'Netherite: forged in the deep Nether - and it smoulders.', 'looks': NETHERITE_LOOKS}}
LOOKS = {(w, k): t for t, d in TIERS.items() for w, (k, i, sc) in d['looks'].items()}
ITEMS = {g[1] for g in GILDED.values()}
TIER_OF_ITEM = {i: t for t, d in TIERS.items() for (k, i, sc) in d['looks'].values()}
TROPHIES = 20                                # its price: 20 Gutter Trophies - 2,560 coins at the Tailor (an aura is 1,280)


def tier(w, k):
    """the metal of a follower's look (gold, diamond, netherite) - or None for a cloth one"""
    return LOOKS.get((w, k))


def is_gilded(w, k):
    """(any of the metal looks - gold, diamond, netherite: polished through gild.metal)"""
    return (w, k) in LOOKS


def dress(w, k, im, **kw):
    """the texture in that look's metal"""
    return metal(im, ramp=TIERS[LOOKS[(w, k)]]['ramp'], **kw)


def steel(w, k):
    """the ramp for the steel worn with that look (Leo's helm and armour)"""
    return TIERS[LOOKS[(w, k)]]['steel']


def price(iid, plain):
    """a cosmetic's Goldtooth offer price (the Tailor reads it): gold 5 Gutter Trophies, diamond 8, netherite 12 (2.82t: were 20, 32, 48)"""
    return ('gutter_trophy', TIERS[TIER_OF_ITEM[iid]]['trophies']) if iid in TIER_OF_ITEM else plain
