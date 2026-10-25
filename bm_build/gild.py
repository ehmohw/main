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
          'ava': (4, 'cos_ava_4', 'bm.cosav'), 'pearlq': (4, 'cos_pearlq_4', 'bm.cospq'), 'bloo': (4, 'cos_bloo_4', 'bm.cosbo'), 'stalker': (4, 'cos_stalker_4', 'bm.cossv'), 'lantern': (4, 'cos_lantern_4', 'bm.cosln'), 'bender': (4, 'cos_bender_4', 'bm.cosbv'), 'bones': (4, 'cos_bones_4', 'bm.cosbj'), 'capshun': (4, 'cos_capshun_4', 'bm.cosmz'), 'pxcecil': (4, 'cos_pxcecil_4', 'bm.cosxc'), 'pxleo': (4, 'cos_pxleo_4', 'bm.cosxl'), 'pxemma': (4, 'cos_pxemma_4', 'bm.cosxm'), 'sky': (4, 'cos_sky_4', 'bm.cosyb')}   # (2.87)
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


# (2.94s) the metal looks no longer dip the whole outfit in metal (a texture overlay, the owner said - and it was): the cloth
# stays the follower's own, deepened to a richer shade for the metal it goes with, and the metal is BUILT INTO it - piping
# along every edge, the outfit's own small details (buttons, buckles, stripes, trims: its accent colours) cast in it, and a
# fine stud-work across the cloth. inlay(im, metal): cloth -> CLOTH[metal]; accents, edges and studs -> polished metal.
CLOTH = {'gold': (0.80, 1.15, 0.00), 'diamond': (0.82, 1.05, 0.12), 'netherite': (0.58, 0.70, 0.30)}   # (value, saturation, pull to the metal's own dark)


def _deepen(c, t, toward):
    import colorsys
    v_k, s_k, pull = CLOTH[t]
    h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c[:3]))
    r, g, b = colorsys.hsv_to_rgb(h, min(1.0, s * s_k), v * v_k)
    return tuple(int(255 * (a * (1 - pull)) + toward[i] * pull) for i, a in enumerate((r, g, b)))


def inlay(im, t):
    """the cloth kept (deepened), with the metal t worked into its accents - the outfit's own small details in other colours
    (buttons, buckles, stripes, trims). Its hems, cuffs and collars - the top and bottom edge of each side face, which only the
    models know - are cast in the metal too, once the pack is built (pipe)."""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    pts = [(x, y) for y in range(h) for x in range(w) if px[x, y][3] > 0]
    if not pts:
        return im.copy()
    ramp = TIERS[t]['ramp']
    q = Image.new('RGB', (len(pts), 1)); q.putdata([px[p][:3] for p in pts])
    q = q.quantize(colors=min(6, len(pts)), method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    lab = list(q.getdata())
    count = {}
    for l in lab: count[l] = count.get(l, 0) + 1
    main = max(count, key=lambda l: count[l])
    col = lambda l: pal[l * 3:l * 3 + 3]
    dist = lambda a, b: sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5
    # an accent: a shade well apart from the main cloth (not its weave), and not the bulk of the texture
    acc = {l for l in count if l != main and dist(col(l), col(main)) > 80 and count[l] < 0.10 * len(pts)}
    mask = {p for p, l in zip(pts, lab) if l in acc}
    # and its pattern - the lines drawn darker than the cloth round them (a scale's outline, a fold, a seam), traced in the metal
    lum = {p: _lum(px[p]) for p in pts}
    line = []
    for (x, y) in pts:
        nb = [lum[q] for q in ((x + dx, y + dy) for dx in (-2, -1, 0, 1, 2) for dy in (-2, -1, 0, 1, 2)) if q in lum]
        d = sum(nb) / len(nb) - lum[(x, y)]
        if d > 0.12: line.append((d, (x, y)))
    line.sort(reverse=True)
    mask |= {p for _d, p in line[:int(0.10 * len(pts))]}
    mi = Image.new('RGBA', (w, h), (0, 0, 0, 0)); mp = mi.load()
    for p in mask: mp[p] = px[p]
    shone = metal(mi, ramp=ramp, sheen=0).load()
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); o = out.load()
    dark = ramp[1][1]
    for p in pts:
        o[p] = shone[p][:3] + (px[p][3],) if p in mask else _deepen(px[p], t, dark) + (px[p][3],)
    _mark(out, t)
    return out


# ---- the hems: which saved texture is which look's (an inlaid image remembers where it was saved), then, at the end of the
#      pack's build, every model face that wears it gets its top and bottom edge in the metal (a side face's: hem and collar)
SAVED = {}                                   # png path -> metal


def _mark(im, t):
    def save(fp, *a, **k):
        SAVED[str(fp)] = t
        return Image.Image.save(im, fp, *a, **k)
    im.save = save
    for meth in ('copy', 'convert'):          # (a copy of it remembers too)
        orig = getattr(Image.Image, meth)
        def wrap(*a, _o=orig, **k):
            r = _o(im, *a, **k); _mark(r, t); return r
        setattr(im, meth, wrap)


def pipe(root):
    """(the end of gen_rp's build) the hems and collars of every inlaid texture, in its metal, from the faces that wear it"""
    import os, json
    tb = os.path.join(root, 'assets', 'bm', 'textures', 'block')
    names = {os.path.splitext(os.path.basename(f))[0]: t for f, t in SAVED.items() if os.path.dirname(os.path.abspath(f)) == os.path.abspath(tb)}
    edges = {n: set() for n in names}         # name -> {(u0, v0, u1, v1, which edges)}
    md = os.path.join(root, 'assets', 'bm', 'models')
    for dp, _d, fs in os.walk(md):
        for f in fs:
            if not f.endswith('.json'): continue
            try: m = json.load(open(os.path.join(dp, f)))
            except Exception: continue
            tex = m.get('textures', {})
            for e in m.get('elements', ()):
                for side, fc in e.get('faces', {}).items():
                    if side in ('up', 'down') or 'uv' not in fc: continue
                    ref = fc.get('texture', '')
                    v = tex.get(ref[1:], ref) if ref.startswith('#') else ref
                    for _ in range(4):
                        if isinstance(v, str) and v.startswith('#'): v = tex.get(v[1:], v)
                    n = str(v).split('/')[-1]
                    if n in edges:
                        edges[n].add((tuple(fc['uv']), fc.get('rotation', 0)))
    json.dump(names, open(os.path.join(os.path.dirname(os.path.abspath(root)), 'metal_looks.json'), 'w'))   # (for tools/preview/metals3d.py)
    # ---- the fittings: in each model wearing a metal look, its smaller pieces - belts, collars, cuffs, bands, buckles, trims -
    #      are cast whole in the metal (a texture of their own: <name>_mt, the cloth's shading through the metal's polish)
    cast, made = 0, set()
    for dp, _d, fs in os.walk(md):
        for f in fs:
            if not f.endswith('.json'): continue
            fp = os.path.join(dp, f)
            try: m = json.load(open(fp))
            except Exception: continue
            tex = m.get('textures', {}); els = m.get('elements', [])
            def name_of(ref):
                v = ref
                for _ in range(5):
                    if isinstance(v, str) and v.startswith('#'): v = tex.get(v[1:], v)
                return str(v).split('/')[-1]
            mine = [e for e in els if any(name_of(fc.get('texture', '')) in names for fc in e.get('faces', {}).values())]
            if len(mine) < 2: continue
            vol = lambda e: max(0.01, abs(e['to'][0] - e['from'][0])) * max(0.01, abs(e['to'][1] - e['from'][1])) * max(0.01, abs(e['to'][2] - e['from'][2]))
            ranked = sorted(mine, key=vol)
            big = vol(ranked[-1])
            pick = [e for e in ranked[:max(1, int(len(ranked) * 0.5))] if vol(e) < 0.4 * big]
            if not pick: continue
            for e in pick:
                for fc in e.get('faces', {}).values():
                    n = name_of(fc.get('texture', ''))
                    if n not in names: continue
                    if n not in made:
                        src = Image.open(os.path.join(tb, n + '.png')).convert('RGBA')
                        metal(src, ramp=TIERS[names[n]]['ramp']).save(os.path.join(tb, n + '_mt.png')); made.add(n)
                    tex['mt_' + n] = 'bm:block/' + n + '_mt'
                    fc['texture'] = '#mt_' + n
            m['textures'] = tex
            json.dump(m, open(fp, 'w'), indent=1); cast += 1
    print('metal fittings: %d models, %d textures' % (cast, len(made)))
    done = 0
    for n, t in names.items():
        if not edges[n]: continue
        path = os.path.join(tb, n + '.png')
        im = Image.open(path).convert('RGBA'); w, h = im.size; px = im.load()
        # (a material - a hide, scales - is worn by many faces over the same patch: hems there are a tangle. Only a texture
        #  laid out face by face, its faces apart, gets them.)
        rects = list({tuple(sorted((r[0], r[2])) + sorted((r[1], r[3]))) for r, _r in edges[n]})
        over = sum(1 for i, a in enumerate(rects) if any(min(a[1], b[1]) - max(a[0], b[0]) > 0.01 and min(a[3], b[3]) - max(a[2], b[2]) > 0.01
                                                         for j, b in enumerate(rects) if j != i))
        if over > 0.2 * len(rects): continue
        mask = set()
        for (u0, v0, u1, v1), rot in edges[n]:
            x0, x1 = sorted((int(round(u0 * w / 16)), int(round(u1 * w / 16))))
            y0, y1 = sorted((int(round(v0 * h / 16)), int(round(v1 * h / 16))))
            fw, fh = (x1 - x0, y1 - y0) if rot in (0, 180) else (y1 - y0, x1 - x0)
            if fw < 6 or fh < 8: continue                    # (a small face - a scale, a strap, one block of many: no hem, or it's stripes)
            hem = 2 if fh >= 12 else 1                       # (a long face - a skirt, a coat - a broader hem)
            if rot in (0, 180):
                bot = y1 - 1 if rot == 0 else y0
                for x in range(x0, x1):
                    mask |= {(x, bot - i if rot == 0 else bot + i) for i in range(hem)}
            else:
                side = x1 - 1 if rot == 90 else x0
                for y in range(y0, y1):
                    mask |= {(side - i if rot == 90 else side + i, y) for i in range(hem)}
        mask = {q for q in mask if 0 <= q[0] < w and 0 <= q[1] < h and px[q][3] > 0}
        if not mask: continue
        ramp = TIERS[t]['ramp']
        for q in mask:                         # (a hem's own shading: bright along it, a glint now and then)
            v = 0.70 + (0.18 if (q[0] + q[1]) % 4 == 0 else 0.0)
            px[q] = _ramp(v, ramp) + (px[q][3],)
        im.save(path); done += 1
    return done


def dress(w, k, im, **kw):
    """the texture in that look: its cloth, with the look's metal built into it (inlay)"""
    return inlay(im, LOOKS[(w, k)])


def steel(w, k):
    """the ramp for the steel worn with that look (Leo's helm and armour)"""
    return TIERS[LOOKS[(w, k)]]['steel']


def price(iid, plain):
    """a cosmetic's Goldtooth offer price (the Tailor reads it): gold 5 Gutter Trophies, diamond 8, netherite 12 (2.82t: were 20, 32, 48)"""
    return ('gutter_trophy', TIERS[TIER_OF_ITEM[iid]]['trophies']) if iid in TIER_OF_ITEM else plain
