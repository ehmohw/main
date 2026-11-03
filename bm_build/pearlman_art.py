"""3.0g: PEARLMAN, THE FOLLOWER, AS A RIG - the trader's own penguin (phase60's model, every box where it was) cut into parts, so
he waddles, runs, hops, sits, swims, tips his hat and swings his briefcase like everyone else; and drawn at the trader's size
(phase60 PS 0.76 - he was 0.55, a head shorter than the penguin who sells you gems).

PARTS   body (the egg of him: belly, globe-gem, bow tie - his root, at his feet), head (beak, grin, eyes; parented to the body),
        hat (its own part on the head: it TIPS - lifted off his head by his flipper), armr (the right flipper - it rests at his
        side now, as the left; the trader holds it up at his brim, which is his 'tip' pose), arml (the left flipper and the
        briefcase he carries in it), legr / legl (his feet).
        Every season (phase60's pearlman_<season>: the same penguin in the season's colours, its bow tie and trim) is a set
        of part models of its own: pmr_<part>_<season>. The wardrobe's looks ride on the base set (phase138's '_c<k>').
HIS JOKE FORMS (phase128): '_e' ETHEREAL - Pearlman, Gem Appraiser of the Cosmos: a gaudy crystal-encrusted suit of starry
        violet, an opal shirt-front, a diamond bow tie, crystal epaulettes and cufflinks, a monocle, an amethyst top hat crowned
        in crystal and a briefcase studded with gems - and the Ethereal Gem itself on his chest.
        '_w' WRAITHFIRE - Pearlman, Soul Broker: a charcoal pinstripe suit, a ghost-pale shirt, a soul-fire tie and hat band,
        soul flames licking off his hat, eyes lit cyan, a contract scroll in his flipper and a black ledger-case.
        (A form outranks a season and a look, as the Gem's do.)

Design units: feet at y=0, facing -z, his right is +x (rigkit). phase60 drew him in model units on a 16-wide box: design =
model - (8, 0, 8)."""
import math
import random

from PIL import Image

from rigkit import qs, qa, I

PREFIX = 'pmr_'
RIG_SCALE = 0.76                          # (the trader's: phase60 PS)
PIVOT = {'body': (0, 1.5, 0), 'head': (0, 17.0, 0), 'hat': (0, 24.0, 0), 'armr': (5.6, 14.0, -0.5), 'arml': (-5.6, 14.0, -0.5),
         'legr': (3.0, 1.5, -1.5), 'legl': (-3.0, 1.5, -1.5)}
PARENT = {'body': None, 'head': 'body', 'hat': 'head', 'armr': 'body', 'arml': 'body', 'legr': None, 'legl': None}
PARTS = tuple(PIVOT)
SEASONS = ('fall', 'xmas', 'easter', 'summer')
FORMS = ('_e', '_w')
SWIM_FRAMES = 4

# phase60's texture keys (his own) - and each form's: key -> texture
TEX = {'k': 'pm_black', 'w': 'pm_white', 'o': 'pm_orange', 'y': 'pm_yellow', 'b': 'pm_blue', 'd': 'pm_dblue', 'g': 'pm_gold',
       'e': 'pm_eye', 't': 'pm_teeth', 'c': 'pm_case', 'r': 'gm_earth', 'H': 'pm_hat'}
SEASON_TEX = lambda sk: dict(TEX, k=f'pm_{sk}_body', w=f'pm_{sk}_belly', b=f'pm_{sk}_band', y=f'pm_{sk}_feet', h=f'pm_{sk}_hat',
                             v=f'pm_{sk}_tie', q=f'pm_{sk}_trim', l=f'pm_{sk}_leaf')
FORM_TEX = {'_e': dict(TEX, k='pmx_e_suit', w='pmx_e_opal', b='pmx_e_band', d='pmx_e_tie', g='pmx_e_gold', r='gm_eth', c='pmx_e_case',
                       H='pmx_e_hat', y='pmx_e_gold', q='pmx_e_crys', Q='gm_eth_lt', m='pmx_e_glass'),
            '_w': dict(TEX, k='pmx_w_suit', w='pmx_w_shirt', b='pmx_w_band', d='pmx_w_tie', g='pmx_w_chain', r='pmx_w_gem', c='pmx_w_case',
                       H='pmx_w_hat', y='pmx_w_feet', e='pmx_w_eye', f='pmx_w_flame', F='pmx_w_flame_tip', p='pmx_w_scroll', o='pmx_w_beak')}
# (the boxes that glow: their texture keys, a light level)
LIGHT = {'_e': {'q': 12, 'Q': 14, 'r': 13, 'd': 10}, '_w': {'f': 15, 'F': 15, 'e': 13, 'b': 13, 'd': 12, 'r': 14}}


# ---------------------------------------------------------------------------------------------------- the penguin, in parts
def _c(fr, to, t, rot=None):
    return (tuple(fr), tuple(to), t, rot)


def penguin(H='H', tie=True, crown=31.5, brim=0):
    """phase60's penguin (model units), each box given to its part. The right flipper hangs at his side, the left's twin."""
    P = {p: [] for p in PARTS}
    P['legr'] += [_c((9, 0, 0.5), (13, 1.5, 6.5), 'y')]
    P['legl'] += [_c((3, 0, 0.5), (7, 1.5, 6.5), 'y')]
    P['body'] += [_c((2.5, 1.5, 3.5), (13.5, 14, 12.5), 'k'), _c((3.5, 14, 4.5), (12.5, 17, 11.5), 'k'),
                  _c((4, 2.5, 3.1), (12, 13.2, 3.5), 'w'), _c((5, 13, 4.1), (11, 14.6, 4.5), 'w'),
                  _c((6.2, 5.5, 2.7), (9.8, 9.1, 3.15), 'g'), _c((6.7, 6.0, 2.45), (9.3, 8.6, 2.8), 'r')]
    if tie:
        P['body'] += [_c((5, 14.6, 3.8), (7.6, 16.4, 4.5), 'b'), _c((8.4, 14.6, 3.8), (11, 16.4, 4.5), 'b'), _c((7.4, 14.9, 3.6), (8.6, 16.1, 4.3), 'd')]
    P['head'] += [_c((3.5, 17, 4.5), (12.5, 19, 11.5), 'k'), _c((4.5, 19, 5), (11.5, 24, 11), 'k'),
                  _c((6.3, 18.6, 2.4), (9.7, 20.4, 5.1), 'o'), _c((6.6, 17.9, 2.8), (9.4, 18.6, 5.0), 't'), _c((6.8, 17.2, 3.2), (9.2, 17.9, 5.0), 'o'),
                  _c((4.7, 20.3, 4.75), (7.2, 23.6, 5.05), 'e'), _c((8.8, 20.3, 4.75), (11.3, 23.6, 5.05), 'e'),
                  _c((5.1, 22.3, 4.7), (6.1, 23.2, 4.76), 't'), _c((9.2, 22.3, 4.7), (10.2, 23.2, 4.76), 't'),
                  _c((6.3, 20.7, 4.7), (6.7, 21.1, 4.76), 't'), _c((10.4, 20.7, 4.7), (10.8, 21.1, 4.76), 't')]
    P['hat'] += [_c((2.5 - brim, 24, 3 - brim), (13.5 + brim, 24.8, 13 + brim), H), _c((4.5, 24.8, 5), (11.5, crown, 11), H),
                 _c((4.4, 24.8, 4.9), (11.6, 26.2, 11.1), 'b')]
    P['armr'] += [_c((12.8, 6, 6.2), (14.4, 14, 8.8), 'k', ('z', 22.5, (13.6, 14, 7.5)))]
    P['arml'] += [_c((1.6, 6, 6.2), (3.2, 14, 8.8), 'k', ('z', -22.5, (2.4, 14, 7.5))),
                  _c((-3.6, 0.4, 5.2), (1.4, 5.6, 9.8), 'c'), _c((-2.2, 5.6, 7.1), (0.0, 6.8, 7.9), 'c')]
    return P


def _where(fr, to):
    """an extra (a season's or a form's) by where it sits: on the hat, the head or the body"""
    y = (fr[1] + to[1]) / 2
    return 'hat' if y >= 24.0 else ('head' if y >= 17.2 else 'body')


def _mirror(els):
    out = []
    for fr, to, t, *r in els:
        out.append(_c(fr, to, t, *r))
        rr = [(r[0][0], -r[0][1], (16 - r[0][2][0], r[0][2][1], r[0][2][2]))] if r and r[0] else []
        out.append(_c((16 - to[0], fr[1], fr[2]), (16 - fr[0], to[1], to[2]), t, *rr))
    return out


# phase60's seasons, as there: (hat key, the hat's shape, the extras)
def _seasons():
    octa = [_c((6.4, 5.7, 2.6), (9.6, 8.9, 3.1), 'g', ('z', 45, (8, 7.3, 2.85)))]
    S = {
        'fall': ('H', {}, _mirror([((4.6, 15.0, 3.7), (7.4, 16.8, 4.4), 'v'), ((4.0, 16.2, 3.75), (4.8, 17.0, 4.35), 'v'),
                                  ((4.6, 14.3, 3.75), (5.4, 15.0, 4.35), 'v'), ((6.0, 14.5, 3.75), (6.8, 15.0, 4.35), 'v')]) +
                 [_c((7.1, 14.6, 3.35), (8.9, 16.3, 4.3), 'q'), _c((7.5, 14.5, 3.25), (8.5, 16.4, 3.4), 'q'), _c((7.8, 16.3, 3.6), (8.2, 16.9, 4.0), 'l')]),
        'xmas': ('H', {}, _mirror([((5, 14.6, 3.8), (7.6, 16.4, 4.5), 'v')]) +
                 [_c((7.3, 14.5, 3.4), (8.7, 16.2, 4.3), 'g'), _c((7.6, 14.2, 3.3), (8.4, 14.6, 4.2), 'g'),
                  _c((4.6, 25.0, 4.5), (7.0, 26.0, 4.75), 'l', ('z', 22.5, (5.8, 25.5, 4.6))), _c((6.2, 25.6, 4.5), (8.4, 26.6, 4.75), 'l', ('z', -22.5, (7.3, 26.1, 4.6))),
                  _c((6.3, 25.2, 4.25), (6.9, 25.8, 4.6), 'q'), _c((6.9, 25.6, 4.25), (7.5, 26.2, 4.6), 'q'), _c((5.9, 25.8, 4.25), (6.5, 26.4, 4.6), 'q')]),
        'easter': ('h', {}, _mirror([((5, 14.6, 3.8), (7.6, 16.4, 4.5), 'v')]) +
                   [_c((7.2, 14.3, 3.35), (8.8, 16.5, 4.3), 'q'), _c((7.5, 14.1, 3.45), (8.5, 16.8, 4.2), 'q'),
                    _c((5.0, 24.7, 4.6), (7.4, 26.5, 4.75), 'l'), _c((5.6, 24.2, 4.6), (6.8, 27.0, 4.75), 'l'), _c((5.7, 25.1, 4.45), (6.7, 26.1, 4.6), 'y')]),
        'summer': ('h', {'crown': 27.6, 'brim': 1.2}, _mirror([((5, 14.6, 3.8), (7.6, 16.4, 4.5), 'v'), ((4.4, 20.4, 4.45), (7.4, 22.9, 4.7), 'q'),
                                                             ((3.9, 22.2, 4.6), (4.5, 22.6, 8.5), 'q')]) +
                   [_c((7.4, 14.9, 3.6), (8.6, 16.1, 4.3), 'y'), _c((7.4, 22.0, 4.5), (8.6, 22.5, 4.7), 'q'),
                    _c((5.0, 22.2, 4.4), (5.8, 22.6, 4.45), 'l'), _c((9.4, 22.2, 4.4), (10.2, 22.6, 4.45), 'l')]),
    }
    return octa, S


def _form_extras(f):
    """each joke form's finery (model units)"""
    if f == '_e':
        X = [  # the monocle on his right eye: a gold rim, a glass, a chain down to his chest
            _c((8.5, 20.0, 4.55), (11.6, 20.3, 4.7), 'g'), _c((8.5, 23.6, 4.55), (11.6, 23.9, 4.7), 'g'),
            _c((8.5, 20.0, 4.55), (8.8, 23.9, 4.7), 'g'), _c((11.3, 20.0, 4.55), (11.6, 23.9, 4.7), 'g'), _c((8.8, 20.3, 4.5), (11.3, 23.6, 4.56), 'm'),
            _c((11.4, 17.4, 4.5), (11.7, 20.0, 4.7), 'g'),
            # the crown of crystal on his hat, a great cut gem at its band
            _c((7.0, 31.4, 7.0), (9.0, 34.6, 9.0), 'Q', ('y', 45, (8, 33, 8))), _c((5.4, 31.3, 7.4), (6.8, 33.4, 8.6), 'q', ('z', 22.5, (6.1, 31.4, 8))),
            _c((9.2, 31.3, 7.4), (10.6, 33.4, 8.6), 'q', ('z', -22.5, (9.9, 31.4, 8))), _c((7.4, 31.3, 5.3), (8.6, 33.0, 6.6), 'q', ('x', 22.5, (8, 31.4, 6))),
            _c((6.9, 24.6, 4.5), (9.1, 26.6, 4.9), 'Q', ('z', 45, (8, 25.6, 4.7))),
            # studs on the suit: down both lapels and round the hem
            *[_c((x, y, 3.3), (x + 0.8, y + 0.8, 3.55), 'q') for x, y in ((3.2, 12.0), (3.4, 9.0), (3.3, 6.0), (3.2, 3.0), (12.0, 12.0), (11.8, 9.0), (11.9, 6.0), (12.0, 3.0))],
            *[_c((x, 1.6, 3.3), (x + 0.9, 2.4, 3.55), 'q') for x in (5.0, 7.55, 10.1)],
        ]
        # crystal epaulettes on both shoulders
        X += _mirror([((2.6, 16.3, 5.8), (4.4, 18.0, 9.6), 'q', ('z', 22.5, (3.5, 16.3, 7.7))), ((2.2, 15.6, 6.3), (3.4, 17.0, 9.0), 'Q')])
        return X, {'armr': [_c((13.0, 6.4, 6.4), (14.2, 7.6, 8.6), 'q')],                 # (a crystal cufflink)
                   'arml': [_c((1.8, 6.4, 6.4), (3.0, 7.6, 8.6), 'q'),
                            _c((-3.4, 5.6, 5.6), (-2.2, 7.2, 6.8), 'Q', ('y', 45, (-2.8, 6.4, 6.2))), _c((0.0, 5.6, 8.4), (1.2, 7.0, 9.6), 'q', ('y', 45, (0.6, 6.3, 9.0))),
                            _c((-3.8, 1.6, 6.6), (-3.55, 4.4, 8.4), 'Q'), _c((1.35, 1.6, 6.6), (1.6, 4.4, 8.4), 'Q')]}
    # (3.0g redo - the owner: "looked messy". A few bold shapes in black, white and one cyan: a matte black suit and tall hat,
    # a crisp white front, ONE long soul-fire necktie pinned with his soul gem, ONE tall flame rising off the hat over a lit band,
    # a sealed contract in one flipper and a plain black case with a lit clasp in the other.)
    X = [  # the flame on his hat: one tall tongue over two short licks leaning out - wide at the crown, drawn to a point
        _c((5.9, 31.4, 5.9), (10.1, 33.8, 10.1), 'f', ('y', 45, (8, 32.6, 8))), _c((6.5, 33.6, 6.5), (9.5, 36.2, 9.5), 'f', ('y', 45, (8, 34.9, 8))),
        _c((7.1, 36.0, 7.1), (8.9, 38.6, 8.9), 'F', ('y', 45, (8, 37.3, 8))), _c((7.6, 38.4, 7.6), (8.4, 40.2, 8.4), 'F', ('y', 45, (8, 39.3, 8))),
        _c((4.4, 31.2, 7.0), (6.4, 35.0, 9.0), 'f', ('z', 22.5, (5.4, 31.4, 8))), _c((9.6, 31.2, 7.0), (11.6, 35.0, 9.0), 'f', ('z', -22.5, (10.6, 31.4, 8))),
        # the necktie: a knot under his chin and a long blade down his front to the soul gem, which pins it
        _c((7.1, 14.5, 3.5), (8.9, 16.2, 4.3), 'd'), _c((7.3, 9.4, 2.75), (8.7, 14.8, 3.15), 'd'),
        _c((7.2, 8.7, 2.75), (8.8, 10.3, 3.15), 'd', ('z', 45, (8, 9.5, 2.95))),
        # a white collar's two points either side of the knot
        _c((5.6, 15.0, 3.7), (7.1, 16.4, 4.4), 'w', ('z', -30, (7.1, 16.4, 4))), _c((8.9, 15.0, 3.7), (10.4, 16.4, 4.4), 'w', ('z', 30, (8.9, 16.4, 4))),
    ]
    return X, {'armr': [_c((12.7, 4.4, 5.9), (14.5, 6.2, 10.3), 'p'), _c((13.1, 4.0, 7.6), (14.1, 6.6, 8.6), 'b')],      # (the contract, its seal)
               'arml': [_c((-0.4, 2.2, 5.0), (0.9, 3.8, 5.25), 'b')]}                                                   # (the case's clasp, lit)


def _part_els(p, boxes, tex_keys, light):
    """model-unit boxes -> the part's elements (its joint at model 8, 8, 8), textured as phase60's cube (uv from the box)"""
    piv = PIVOT[p]
    off = (-piv[0], 8 - piv[1], -piv[2])          # (model = design + (8, 0, 8); the part's joint to 8, 8, 8)
    out = []
    for fr, to, t, rot in boxes:
        x1, y1, z1 = fr; x2, y2, z2 = to
        cl = lambda v: max(0.0, min(16.0, v % 16 if v > 16 else v))
        uv = {'north': [x1, 16 - y2, x2, 16 - y1], 'south': [x1, 16 - y2, x2, 16 - y1], 'east': [z1, 16 - y2, z2, 16 - y1],
              'west': [z1, 16 - y2, z2, 16 - y1], 'up': [x1, z1, x2, z2], 'down': [x1, z1, x2, z2]}
        faces = {}
        for f, u in uv.items():
            u = [cl(v) for v in u]
            if u[0] == u[2]: u[2] = min(16, u[0] + 1)
            if u[1] == u[3]: u[3] = min(16, u[1] + 1)
            faces[f] = {'uv': [round(v, 4) for v in u], 'texture': '#' + t}
        e = {'from': [round(fr[i] + off[i], 4) for i in range(3)], 'to': [round(to[i] + off[i], 4) for i in range(3)], 'faces': faces}
        if rot:
            e['rotation'] = {'origin': [round(rot[2][i] + off[i], 4) for i in range(3)], 'axis': rot[0], 'angle': rot[1]}
        if light.get(t): e['light_emission'] = light[t]
        out.append(e)
        tex_keys.add(t)
    return out


def models():
    M = {}
    def put(name, p, boxes, texmap, light={}):
        keys = set()
        els = _part_els(p, boxes, keys, light)
        M[name] = ({k: f'bm:block/{texmap[k]}' for k in sorted(keys)}, els)
    base = penguin()
    for p in PARTS:
        put(f'{PREFIX}{p}', p, base[p], TEX)
    octa, SEAS = _seasons()
    for sk, (H, hat, extra) in SEAS.items():
        P = penguin(H if H == 'h' else 'H', tie=False, **hat)
        for b in octa + extra:
            P[_where(b[0], b[1])].append(b)
        for p in PARTS:
            put(f'{PREFIX}{p}_{sk}', p, P[p], SEASON_TEX(sk))
    for f in FORMS:
        P = penguin(tie=f != '_w')
        X, per = _form_extras(f)
        for b in X:
            P[_where(b[0], b[1])].append(b)
        for p, bs in per.items():
            P[p] += bs
        for p in PARTS:
            put(f'{PREFIX}{p}{f}', p, P[p], FORM_TEX[f], LIGHT[f])
    return M


def model_name(p, pose, suffix=''):
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures: the two forms
def _px(base, var, seed, fn=None):
    rnd = random.Random(seed)
    im = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            c = fn(x, y) if fn else base
            d = rnd.randint(-var, var)
            im.putpixel((x, y), tuple(max(0, min(255, c[i] + d)) for i in range(3)) + (255,))
    return im


def _lerp(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def textures():
    T = {}
    # ETHEREAL: starry violet velvet, its stars and facets; an opal front; platinum-gold; crystal
    def suit(x, y):
        c = _lerp((44, 20, 92), (86, 40, 150), (math.sin(x * 0.9 + y * 0.4) + 1) / 2)
        if (x * 7 + y * 3) % 11 == 0: c = (232, 220, 255)
        elif (x + 2 * y) % 9 == 0: c = _lerp(c, (160, 230, 255), 0.6)
        return c
    T['pmx_e_suit'] = _px(None, 4, 301, suit)
    hues = [(255, 200, 230), (200, 240, 255), (220, 255, 220), (255, 240, 200), (230, 210, 255)]
    T['pmx_e_opal'] = _px(None, 3, 302, lambda x, y: _lerp(hues[(x + y) // 4 % 5], hues[((x + y) // 4 + 1) % 5], ((x + y) % 4) / 4))
    T['pmx_e_gold'] = _px(None, 6, 303, lambda x, y: (255, 244, 170) if (x - y) % 7 == 0 else (236, 200, 84))
    T['pmx_e_band'] = _px(None, 3, 304, lambda x, y: [(214, 30, 66), (255, 172, 34), (34, 206, 108), (40, 98, 232), (164, 70, 232)][x // 3 % 5])
    T['pmx_e_tie'] = _px(None, 4, 305, lambda x, y: (255, 255, 255) if (x + y) % 5 == 0 else (178, 236, 255))
    T['pmx_e_hat'] = _px(None, 4, 306, lambda x, y: _lerp((70, 24, 120), (150, 70, 220), ((x + (15 - y)) % 8) / 8))
    T['pmx_e_case'] = _px(None, 4, 307, lambda x, y: (230, 200, 90) if x in (0, 15) or y in (0, 15) else _lerp((40, 16, 70), (90, 40, 140), y / 15))
    T['pmx_e_crys'] = _px(None, 3, 308, lambda x, y: (255, 255, 255) if (x, y) in ((3, 3), (4, 3), (11, 9)) else _lerp((150, 90, 255), (220, 200, 255), ((x + y) % 8) / 8))
    T['pmx_e_glass'] = _px((200, 240, 255), 3, 309)
    # WRAITHFIRE (3.0g redo): matte black, crisp white, one cyan - no pinstripes, no busy speckle
    T['pmx_w_suit'] = _px(None, 2, 311, lambda x, y: _lerp((30, 32, 40), (18, 19, 25), y / 15))
    T['pmx_w_shirt'] = _px(None, 2, 312, lambda x, y: _lerp((246, 250, 252), (212, 226, 234), y / 15))
    T['pmx_w_band'] = _px(None, 2, 313, lambda x, y: (190, 252, 255) if y in (7, 8) else (60, 214, 240))
    T['pmx_w_tie'] = _px(None, 2, 314, lambda x, y: (150, 246, 255) if x in (7, 8) else _lerp((40, 190, 228), (24, 130, 176), y / 15))
    T['pmx_w_chain'] = _px((44, 48, 58), 2, 315)
    T['pmx_w_gem'] = _px(None, 2, 316, lambda x, y: (230, 255, 255) if abs(x - 7.5) + abs(y - 7.5) < 3 else (30, 200, 240))
    T['pmx_w_case'] = _px(None, 2, 317, lambda x, y: (40, 42, 52) if x in (0, 15) or y in (0, 15) else (20, 21, 27))
    T['pmx_w_hat'] = _px(None, 2, 318, lambda x, y: _lerp((28, 30, 38), (14, 15, 20), y / 15))
    T['pmx_w_feet'] = _px((52, 56, 66), 2, 319)
    T['pmx_w_beak'] = _px((122, 128, 140), 3, 323)
    T['pmx_w_eye'] = _px(None, 2, 320, lambda x, y: (236, 255, 255) if 5 <= x <= 10 and 5 <= y <= 10 else (70, 226, 255))
    T['pmx_w_flame'] = _px(None, 3, 321, lambda x, y: _lerp((16, 140, 204), (110, 236, 255), (15 - y) / 15))
    T['pmx_w_flame_tip'] = _px(None, 2, 324, lambda x, y: _lerp((120, 240, 255), (235, 255, 255), (15 - y) / 15))
    T['pmx_w_scroll'] = _px(None, 2, 322, lambda x, y: (200, 190, 160) if x in (0, 15) else (236, 228, 204))
    return T


# ---------------------------------------------------------------------------------------------------- poses (rigkit: display frame -
# his front is +z, his right -x; a limb swings forward with negative x; his right flipper goes out with negative z, his left
# with positive; the body leans forward with positive x)
def P(**kw):
    d = {}
    for k, v in kw.items():
        if k.startswith('o_'): d['_o_' + k[2:]] = v
        elif k == 'off': d['_off'] = v
        else: d[k] = v if isinstance(v, tuple) and len(v) == 4 else qs(*v)
    return d


def flip(r, l): return {'armr': qs(('z', -r)), 'arml': qs(('z', l))}


POSES = {
    'idle_a': P(**flip(5, 5)),
    'idle_b': P(off=(0, -0.15, 0), head=(('z', 4), ('x', 3)), **flip(9, 8)),
    'look_l': P(head=(('y', 28),), **flip(6, 4)), 'look_r': P(head=(('y', -28),), **flip(4, 6)),
    # the waddle: he rolls from foot to foot, the lifted foot shuffled forward, the flippers out for balance
    'walk_a': P(body=(('z', 8),), head=(('z', -4),), o_legr=(0, 0.9, -1.0), legr=(('x', -14),), **flip(20, 9)),
    'walk_up': P(off=(0, 0.25, 0), **flip(12, 12)),
    'walk_b': P(body=(('z', -8),), head=(('z', 4),), o_legl=(0, 0.9, -1.0), legl=(('x', -14),), **flip(9, 20)),
    # running: leant into it, rolling hard, both flippers flung back and out
    'run_a': P(body=(('x', 14), ('z', 11)), head=(('x', -10),), o_legr=(0, 1.4, -1.6), legr=(('x', -22),),
               armr=(('x', 30), ('z', -55)), arml=(('x', 30), ('z', 40))),
    'run_up': P(off=(0, 0.5, 0), body=(('x', 14),), head=(('x', -10),), armr=(('x', 25), ('z', -48)), arml=(('x', 25), ('z', 48))),
    'run_b': P(body=(('x', 14), ('z', -11)), head=(('x', -10),), o_legl=(0, 1.4, -1.6), legl=(('x', -22),),
               armr=(('x', 30), ('z', -40)), arml=(('x', 30), ('z', 55))),
    'jump': P(off=(0, 0.6, 0), body=(('x', -6),), head=(('x', -8),), legr=(('x', 18),), legl=(('x', 18),), **flip(70, 70)),
    # sitting: down on his tail, his feet stuck out in front, flippers resting on his belly - and a little foot-swing
    'sit_a': P(o_body=(0, -1.5, 0.6), body=(('x', -12),), head=(('x', 8),), o_legr=(0, 0.1, -1.4), legr=(('x', -38),),
               o_legl=(0, 0.1, -1.4), legl=(('x', -38),), armr=(('x', -30), ('z', -8)), arml=(('x', -30), ('z', 8))),
    'sit_b': P(o_body=(0, -1.5, 0.6), body=(('x', -12),), head=(('x', 3), ('z', 7)), o_legr=(0, 0.4, -1.4), legr=(('x', -55),),
               o_legl=(0, 0.1, -1.4), legl=(('x', -30),), armr=(('x', -30), ('z', -8)), arml=(('x', -30), ('z', 8))),
    # tipping his hat: the flipper up to the brim - the hat lifted and tilted - and a little bow under it
    'tip_up': P(head=(('z', -4),), armr=(('z', -150), ('x', -6)), arml=(('z', 6),)),
    'tip': P(body=(('x', 8),), head=(('x', 12),), hat=(('z', -14), ('x', -6)), o_hat=(0.8, 1.6, 0.2), armr=(('z', -142), ('x', -12)), arml=(('z', 6),)),
    # the briefcase swung: back, and round into whatever's in front of him
    'swing_back': P(body=(('y', -22),), head=(('y', 14),), arml=(('x', 60), ('z', 30)), armr=(('z', -18),)),
    'swing': P(body=(('y', 26), ('x', 8)), head=(('y', -10),), arml=(('x', -95), ('z', -10)), armr=(('z', -30),)),
    # appraising (his forms' strike): both flippers out at it, leaning in, the case held up
    'appraise': P(body=(('x', 10),), head=(('x', -6),), armr=(('x', -80), ('z', -10)), arml=(('x', -70), ('z', 14))),
    'happy': P(off=(0, 0.8, 0), head=(('x', -10),), **flip(60, 60)),
    'hurt': P(body=(('x', -14),), head=(('x', -12), ('z', 6)), **flip(35, 35)),
}
# swimming: flat out like a torpedo, the flippers beating, the feet trailing
for _i in range(SWIM_FRAMES):
    _a = 25 + 40 * (0.5 + 0.5 * math.sin(2 * math.pi * _i / SWIM_FRAMES))
    POSES[f'swim_{_i}'] = P(off=(0, 3.0, 0), body=(('x', 80),), head=(('x', -55),), legr=(('x', 40 + 8 * math.sin(2 * math.pi * _i / SWIM_FRAMES)),),
                            legl=(('x', 40 - 8 * math.sin(2 * math.pi * _i / SWIM_FRAMES)),), **flip(_a, _a))
DUR = {'idle_a': 30, 'idle_b': 30, 'look_l': 12, 'look_r': 12, 'walk_a': 3, 'walk_up': 3, 'walk_b': 3, 'run_a': 2, 'run_up': 2, 'run_b': 2,
       'jump': 4, 'sit_a': 20, 'sit_b': 20, 'tip_up': 6, 'tip': 6, 'swing_back': 5, 'swing': 2, 'appraise': 5, 'happy': 4, 'hurt': 3,
       **{f'swim_{i}': 4 for i in range(SWIM_FRAMES)}}
