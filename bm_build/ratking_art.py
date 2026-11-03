"""3.0g: THE RAT KING (art) - the heist's rarest champion (phase76's pit), redrawn as a rigkit rig (heist3g runs it).

The owner: "The rat king boss in heists looks unimpressive and has no animations." He was the pack's little 3D rat
(bm:rat3d_lord) blown up 1.7 times on an invisible zombie. Now he is a king: a great, fat, upright rat ~2.8 blocks tall in
the pack's rat look (the grey-brown fur, the pink snout, ears, paws and tail of the market's rats), with a tall gold crown
(its points, a ruby at the brow, a velvet cap and an orb), a crimson royal cape with an ermine collar, a blue sash and a
belt with a gold buckle, red eyes that glow under a scowl, long buck teeth, whiskers, and in his right paw a gold sceptre
crowned with a wheel of golden cheese (the Rat King's prize - the cabinet's Golden Cheese Wheel). His tail is three
segments, ringed in gold, and it sways.

THE RIG (rigkit, as knight_art / mire_art). Design units: feet at y=0, facing -z, his right is +x; one unit is 1/16 block
at display scale 1 (RIG_SCALE 0.9: ~2.8 blocks to the crown's points). Parts (13): body (the root: belly, chest, sash,
belt), head, jaw (hinged under the snout), crown, armr, arml, sceptre (in the right paw), legr, legl (haunch and long hind
foot), cape, tail1, tail2, tail3 (a chain).

POSES (heist3g's state machine and the staging kit's timelines play them): idle_a / idle_b (a proud stance, the sceptre
upright; the breath in, the tail swinging the other way), walk_0..3 (a heavy waddle: the body rolls, the legs and arms
swing, the tail sways), atk_0 / atk_1 (the sceptre hauled back over his shoulder, then brought down in front of him),
sp_0 / sp_1 (THE ROYAL DECREE: rearing up, both paws high, jaws wide in a screech - then the sceptre slammed into the
floor, crouched over it), hurt (a flinch back, jaw open), death_0 / death_1 (he staggers, then topples onto his back,
the crown knocked askew), arrive_0 / arrive_1 (crouched low out of the dark, then rearing up to roar).
Every pose is grounded (his feet on y=0; death_1 his back)."""
import math
import random
from PIL import Image, ImageDraw

import rigkit as RK
from rigkit import qs, el, seg, shrink, D, qrot

PREFIX = 'rk_'
RIG_SCALE = 0.9
SCALE = RIG_SCALE
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

PIVOT = {'body': (0, 15.0, 1.0), 'head': (0, 33.0, -1.5), 'jaw': (0, 34.4, -7.5), 'crown': (0, 44.0, -1.5),
         'armr': (10.0, 30.0, 0.0), 'arml': (-10.0, 30.0, 0.0), 'sceptre': (12.3, 13.6, -6.6),
         'legr': (5.5, 14.0, 2.0), 'legl': (-5.5, 14.0, 2.0), 'cape': (0, 32.5, 8.0),
         'tail1': (0, 7.0, 9.5), 'tail2': (0, 4.0, 17.0), 'tail3': (0, 2.6, 24.5)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'crown': 'head', 'armr': 'body', 'arml': 'body', 'sceptre': 'armr',
          'legr': 'body', 'legl': 'body', 'cape': 'body', 'tail1': 'body', 'tail2': 'tail1', 'tail3': 'tail2'}
PARTS = tuple(PIVOT)
PART_K = {'cape': 1.6, 'sceptre': 1.4}           # (built at full size, kept inside the model box: shown at k times)
GLOW = ('eye', 'ruby')                            # (lit textures: light_emission on their faces' elements)


def HIDDEN(p, pose):
    return False


def model_name(p, pose=None, suffix=''):
    return f'{PREFIX}{p}{suffix}'


def model_id(p):
    return model_name(p)


# ---------------------------------------------------------------------------------------------------- textures (16 x 16)
def _rgb(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a, b, k):
    return tuple(int(a[i] * (1 - k) + b[i] * k) for i in range(3))


def _base(col, seed, grain=10):
    rnd = random.Random(seed); im = Image.new('RGBA', (16, 16)); px = im.load(); c = _rgb(col)
    for y in range(16):
        for x in range(16):
            d = rnd.randint(-grain, grain)
            px[x, y] = tuple(max(0, min(255, v + d)) for v in c) + (255,)
    return im


def _fur(col, seed, dark, light):
    """fur: little strokes, darker tufts, a lit tip here and there (top-left light)"""
    rnd = random.Random(seed); im = _base(col, seed, 7); px = im.load(); dk, lt = _rgb(dark), _rgb(light)
    for _ in range(22):
        x, y = rnd.randrange(16), rnd.randrange(16)
        for k in range(rnd.randint(2, 3)):
            if 0 <= y + k < 16: px[x, (y + k) % 16] = dk + (255,)
        if y - 1 >= 0 and rnd.random() < 0.5: px[x, y - 1] = lt + (255,)
    return im


def _velvet(seed):
    """crimson velvet: soft vertical folds, a sheen down each fold's crest"""
    im = Image.new('RGBA', (16, 16)); px = im.load(); a, b, c = _rgb('#7a0f1e'), _rgb('#a81c2c'), _rgb('#c8384a')
    for x in range(16):
        k = 0.5 + 0.5 * math.sin(x / 16 * 2 * math.pi * 2)
        for y in range(16):
            col = _mix(a, b, k) if k < 0.85 else _mix(b, c, (k - 0.85) / 0.15)
            px[x, y] = col + (255,)
    return im


def _ermine():
    """ermine: white fur, the little black tails in rows"""
    im = _base('#f0ece4', 41, 6); d = ImageDraw.Draw(im); k = _rgb('#1a1a1e') + (255,)
    for y0, xs in ((2, (2, 9)), (8, (5, 12)), (13, (1, 8, 14))):
        for x in xs:
            d.line((x, y0, x, y0 + 2), fill=k); d.point((x - 1, y0 + 2), fill=k); d.point((x + 1, y0 + 2), fill=k)
    return im


def _gold(seed, dark='#9a6a10', mid='#e8b020', hi='#fff2a0'):
    """polished gold: a bright band across the top, a dark lower edge, a glint"""
    im = Image.new('RGBA', (16, 16)); px = im.load(); a, b, c = _rgb(dark), _rgb(mid), _rgb(hi)
    for y in range(16):
        for x in range(16):
            k = y / 15
            col = _mix(c, b, min(1, k * 3)) if k < 0.33 else _mix(b, a, (k - 0.33) / 0.67)
            px[x, y] = col + (255,)
    rnd = random.Random(seed)
    for _ in range(3):
        x, y = rnd.randrange(1, 15), rnd.randrange(1, 8); px[x, y] = (255, 255, 230, 255)
    return im


def _cheese():
    """a wheel of golden cheese: warm gold, the holes darker, a rind round the edge"""
    im = _base('#f2c43a', 77, 6); d = ImageDraw.Draw(im); h = _rgb('#b8861e') + (255,); rind = _rgb('#c88a1a') + (255,)
    for (x, y, r) in ((4, 4, 2), (11, 6, 1), (6, 11, 2), (12, 12, 1), (9, 2, 1)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=h)
    d.rectangle((0, 0, 15, 0), fill=rind); d.rectangle((0, 15, 15, 15), fill=rind)
    return im


def _eye():
    im = _base('#ff2a1a', 9, 4); px = im.load()
    for x in range(16):
        for y in range(16):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 4: px[x, y] = (255, 210, 120, 255)
    for (x, y) in ((4, 4), (5, 4), (4, 5)): px[x, y] = (255, 255, 255, 255)
    return im


def _flat(col, seed, grain=5):
    return _base(col, seed, grain)


def _sash():
    im = _base('#2a3a9a', 61, 5); d = ImageDraw.Draw(im); g = _rgb('#e8b020') + (255,)
    d.line((0, 1, 15, 1), fill=g); d.line((0, 14, 15, 14), fill=g)
    return im


def _leather():
    im = _base('#5a3418', 51, 6); d = ImageDraw.Draw(im); s = _rgb('#3a200c') + (255,)
    for x in range(0, 16, 3): d.point((x, 2), fill=s); d.point((x + 1, 13), fill=s)
    return im


def _ruby():
    im = _base('#d01030', 33, 6); px = im.load()
    for (x, y) in ((4, 4), (5, 4), (4, 5), (5, 5), (6, 6)): px[x, y] = (255, 190, 200, 255)
    return im


def _mouth():
    im = _base('#4a1018', 21, 5); d = ImageDraw.Draw(im); d.rectangle((3, 8, 12, 14), fill=_rgb('#c84a5a') + (255,))       # (the tongue)
    return im


TEX = {'fur': lambda: _fur('#6a5e56', 1, '#4a403a', '#8a7e74'), 'furdk': lambda: _fur('#4e4440', 2, '#3a302c', '#6a5e56'),
       'furlt': lambda: _fur('#9a8c80', 3, '#7a6c62', '#b8aa9c'), 'belly': lambda: _fur('#bfae9c', 4, '#a09080', '#d8c8b8'),
       'skin': lambda: _flat('#dc9696', 5), 'nose': lambda: _flat('#e0707e', 6, 4), 'eye': _eye, 'tooth': lambda: _flat('#f2ead0', 7, 3),
       'mouth': _mouth, 'whisker': lambda: _flat('#ece4d6', 8, 2), 'claw': lambda: _flat('#2e2628', 10, 4),
       'gold': lambda: _gold(11), 'golddk': lambda: _gold(12, '#6a4a08', '#b88a18', '#e8c860'), 'ruby': _ruby,
       'velvet': lambda: _velvet(13), 'ermine': _ermine, 'sash': _sash, 'leather': _leather, 'cheese': _cheese,
       'brow': lambda: _flat('#2e2624', 14, 3)}


def tex_name(m):
    return f'{PREFIX}{m}'


def textures():
    """{name: 16 x 16 RGBA} (assets/bm/textures/block)"""
    return {tex_name(m): f() for m, f in TEX.items()}


# ---------------------------------------------------------------------------------------------------- geometry
_rs = random.Random(31)
_PV = [None]


def E(fr, to, mat, **kw):
    if 'shift' not in kw and 'uv' not in kw and mat not in ('eye', 'ruby'): kw['shift'] = (_rs.random(), _rs.random())
    e = el(fr, to, mat, _PV[0], **kw)
    if mat in GLOW: e['light_emission'] = 15
    return e


def M(sx, x0, x1, y0, y1, z0, z1, mat, rot=None, **kw):
    """a box on side sx (+1 his right, -1 his left): x given for the right side, mirrored"""
    a, b = sorted((sx * x0, sx * x1))
    if rot and isinstance(rot[0], str):
        ax, ang, o = rot
        rot = (ax, ang if ax == 'x' else ang * sx, (sx * o[0], o[1], o[2]))
    return E((a, y0, z0), (b, y1, z1), mat, rot=rot, **kw)


def S(A, B, w, h, mat, up=UP, ext=0.2):
    e = seg(A, B, w, h, mat, _PV[0], up, ext, shift=(_rs.random(), _rs.random()))
    return e


def _body():
    B = [E((-10, 12, -6.5), (10, 26, 9), 'fur'),                                   # the great belly and haunches
         E((-7.5, 13, -7.1), (7.5, 25, -6.5), 'belly'),                            # the pale belly fur
         E((-9, 26, -5), (9, 33.5, 8), 'fur'),                                     # the chest and shoulders
         E((-6, 26, -5.5), (6, 32.5, -5), 'belly'),
         E((-10.4, 15.5, -7.4), (10.4, 17.5, 9.4), 'leather'),                     # the belt
         E((-1.8, 14.8, -7.9), (1.8, 18.2, -7.3), 'gold'), E((-0.8, 15.8, -8.1), (0.8, 17.2, -7.8), 'ruby')]     # its buckle
    # the sash, from his right shoulder down across the belly to his left hip
    B += [S((7.8, 33.4, -5.7), (-6.5, 18.0, -7.7), 3.2, 0.5, 'sash', FRONT)]
    B += [E((-3.5, 33, -4.5), (3.5, 35, 5.5), 'fur')]                               # the neck, under the collar
    return B


def _head():
    H = [E((-7, 33.5, -8), (7, 44, 5), 'fur'),                                     # the skull
         E((-4.6, 34.4, -15), (4.6, 40.2, -8), 'furlt'),                          # the snout
         E((-5.5, 40, -12), (5.5, 42.5, -7.5), 'fur'),                             # the brow over it
         E((-1.6, 37.4, -16.3), (1.6, 40.2, -15), 'nose'),                         # the nose
         E((-1.7, 32.8, -14.6), (-0.15, 34.6, -14.1), 'tooth'), E((0.15, 32.8, -14.6), (1.7, 34.6, -14.1), 'tooth'),     # buck teeth
         E((-6.2, 39.2, -8.35), (-2.6, 41.6, -8.0), 'eye'), E((2.6, 39.2, -8.35), (6.2, 41.6, -8.0), 'eye')]
    for sx in (1, -1):
        H += [M(sx, 2.0, 7.0, 41.6, 42.6, -8.7, -8.1, 'brow', rot=('z', 14, (4.5, 42.1, -8.4))),                  # the scowl
              M(sx, 4.5, 12.0, 46.5, 47.5, -1.6, 1.4, 'fur'),                                                       # (the ears: a round cup)
              M(sx, 5.0, 11.5, 40.5, 47.0, -1.6, 1.4, 'fur'), M(sx, 6.0, 10.5, 41.5, 46.2, -1.9, -1.6, 'skin'),
              M(sx, 11.5, 12.5, 41.5, 46.5, -1.6, 1.4, 'fur'),
              M(sx, 4.6, 11.0, 36.4, 36.7, -12.0, -11.7, 'whisker', rot=('z', 8, (4.6, 36.5, -11.8))),             # whiskers
              M(sx, 4.6, 10.4, 37.4, 37.7, -11.6, -11.3, 'whisker', rot=('z', -6, (4.6, 37.5, -11.4))),
              M(sx, 4.6, 9.6, 35.4, 35.7, -11.2, -10.9, 'whisker', rot=('z', 20, (4.6, 35.5, -11.0)))]
    return H


def _jaw():
    return [E((-4.0, 31.6, -14.2), (4.0, 34.2, -7.5), 'furlt'), E((-3.4, 34.2, -13.6), (3.4, 34.45, -7.9), 'mouth'),
            E((-1.2, 34.2, -14.0), (1.2, 35.0, -13.4), 'tooth')]


def _crown():
    C = [E((-5.2, 44, -6.4), (5.2, 48.6, 3.4), 'velvet'),                          # the velvet cap inside
         E((-6, 44, -7.2), (6, 47, -6.2), 'gold'), E((-6, 44, 3.4), (6, 47, 4.4), 'gold'),                            # the band
         E((-6, 44, -6.2), (-5, 47, 3.4), 'gold'), E((5, 44, -6.2), (6, 47, 3.4), 'gold'),
         E((-6.2, 43.6, -7.4), (6.2, 44.4, 4.6), 'golddk'),                         # its rim
         E((-1.2, 44.8, -7.7), (1.2, 46.8, -7.15), 'ruby'),                         # the ruby at the brow
         E((-0.9, 48.6, -2.3), (0.9, 50.4, -0.5), 'gold'), E((-0.35, 50.4, -1.75), (0.35, 52.2, -1.05), 'gold'),     # the orb and its cross
         E((-1.0, 51.2, -1.75), (1.0, 51.8, -1.05), 'gold')]
    for (x, z) in ((0, -6.9), (-4.2, -6.9), (4.2, -6.9), (0, 4.1), (-4.2, 4.1), (4.2, 4.1), (-5.7, -1.4), (5.7, -1.4)):     # the points
        tall = 3.6 if x == 0 or abs(x) > 5 else 2.6
        C += [E((x - 0.9, 47, z - 0.4), (x + 0.9, 47 + tall * 0.6, z + 0.4), 'gold'), E((x - 0.45, 47 + tall * 0.6, z - 0.35), (x + 0.45, 47 + tall, z + 0.35), 'gold')]
    for x in (-3.0, 3.0):
        C.append(E((x - 0.6, 45.0, -7.55), (x + 0.6, 46.2, -7.15), 'ruby'))
    return C


def _arm(sx):
    A = [S((sx * 10.6, 31.5, 0.5), (sx * 12.6, 21.5, -1.5), 5.6, 5.6, 'fur'),          # the upper arm (a fat one)
         S((sx * 12.6, 21.5, -1.5), (sx * 12.4, 15.2, -5.6), 4.4, 4.4, 'fur'),         # the forearm, forward
         M(sx, 10.6, 14.2, 12.4, 15.6, -8.4, -4.6, 'skin')]                            # the paw
    for k in range(3):                                                                # its claws
        A.append(M(sx, 10.8 + k * 1.2, 11.6 + k * 1.2, 11.6, 12.6, -9.0, -8.2, 'claw'))
    if sx == 1:
        A.append(M(sx, 9.8, 10.6, 13.0, 15.0, -7.6, -5.6, 'skin'))                   # (the thumb round the haft)
    return A


def _sceptre():
    x, z = 12.3, -6.6
    P = [E((x - 0.7, 3.5, z - 0.7), (x + 0.7, 33.5, z + 0.7), 'gold'),               # the haft
         E((x - 0.9, 11.6, z - 0.9), (x + 0.9, 16.0, z + 0.9), 'golddk'),            # the grip
         E((x - 1.3, 2.2, z - 1.3), (x + 1.3, 3.8, z + 1.3), 'golddk'),              # the foot
         E((x - 1.6, 33.0, z - 1.6), (x + 1.6, 34.4, z + 1.6), 'golddk'),            # the collar under the wheel
         # the wheel of golden cheese, edge-on to his sides (a round of three crossed boxes)
         E((x - 1.6, 34.2, z - 3.6), (x + 1.6, 41.4, z + 3.6), 'cheese'), E((x - 1.6, 35.2, z - 4.6), (x + 1.6, 40.4, z + 4.6), 'cheese'),
         E((x - 1.6, 33.6, z - 2.4), (x + 1.6, 42.0, z + 2.4), 'cheese'),
         E((x - 1.75, 37.1, z - 0.9), (x + 1.75, 38.5, z + 0.9), 'ruby')]             # a ruby set in it
    return P


def _leg(sx):
    return [M(sx, 1.5, 10.5, 6.0, 17.0, -3.0, 7.5, 'fur'),                          # the haunch
            M(sx, 3.2, 8.4, 1.4, 7.0, 1.0, 6.4, 'fur'),                              # the hock
            M(sx, 3.0, 8.6, 0.0, 1.8, -7.0, 3.6, 'skin'),                            # the long hind foot
            M(sx, 3.2, 4.6, 0.0, 1.2, -8.4, -7.0, 'claw'), M(sx, 5.1, 6.5, 0.0, 1.2, -8.6, -7.0, 'claw'),
            M(sx, 7.0, 8.4, 0.0, 1.2, -8.4, -7.0, 'claw')]


def _cape():
    C = [E((-10.6, 9.0, 8.0), (10.6, 32.5, 9.4), 'velvet'),                          # the back
         E((-12.0, 3.0, 9.0), (12.0, 14.0, 10.6), 'velvet'),                          # the hem, flaring
         E((-11.4, 12.0, 8.4), (11.4, 22.0, 10.0), 'velvet'),
         E((-11.2, 10.0, 2.0), (-10.4, 31.0, 8.6), 'velvet'), E((10.4, 10.0, 2.0), (11.2, 31.0, 8.6), 'velvet'),    # its sides
         E((-12.1, 3.0, 10.6), (12.1, 4.2, 10.9), 'ermine'),                          # an ermine hem
         # the ermine collar round his shoulders
         E((-10.2, 31.0, -5.8), (-4.0, 35.0, -4.6), 'ermine'), E((4.0, 31.0, -5.8), (10.2, 35.0, -4.6), 'ermine'),
         E((-10.8, 31.0, -5.0), (-9.4, 35.4, 9.0), 'ermine'), E((9.4, 31.0, -5.0), (10.8, 35.4, 9.0), 'ermine'),
         E((-10.2, 31.0, 8.0), (10.2, 36.2, 10.2), 'ermine')]
    return C


def _tail(i):
    a, b = PIVOT[f'tail{i}'], (PIVOT[f'tail{i + 1}'] if i < 3 else (0, 3.6, 32.0))
    w = (3.0, 2.3, 1.6)[i - 1]
    T = [S(a, b, w, w, 'skin', UP, 0.3)]
    if i == 2:
        m = tuple((a[j] + b[j]) / 2 for j in range(3))
        T.append(S((m[0], m[1] + 0.3, m[2] - 0.8), (m[0], m[1] - 0.3, m[2] + 0.8), 3.2, 3.2, 'gold', FRONT, 0.0))     # a gold ring on it
    return T


_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(31)
    def mk(part, f, *a):
        _PV[0] = PIVOT[part]; return f(*a)
    _RAW.update(body=mk('body', _body), head=mk('head', _head), jaw=mk('jaw', _jaw), crown=mk('crown', _crown),
                armr=mk('armr', _arm, 1), arml=mk('arml', _arm, -1), sceptre=mk('sceptre', _sceptre),
                legr=mk('legr', _leg, 1), legl=mk('legl', _leg, -1), cape=mk('cape', _cape),
                tail1=mk('tail1', _tail, 1), tail2=mk('tail2', _tail, 2), tail3=mk('tail3', _tail, 3))
    return _RAW


def models():
    """{model id: (textures, elements)} - one per part, as gen_rp's HATS take them"""
    out = {}
    for part, els in _build().items():
        k = PART_K.get(part, 1.0)
        els = shrink(els, k) if k != 1.0 else els
        fe = []
        for e in els:
            e = dict(e, faces={f: dict(fc, texture='#' + tex_name(fc['texture'][1:])) for f, fc in e['faces'].items()})
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (part, e['from'], e['to'])
            fe.append(e)
        used = sorted({fc['texture'][1:] for e in fe for fc in e['faces'].values()})
        out[model_id(part)] = ({t: f'bm:block/{t}' for t in used}, fe)
    return out


# ---------------------------------------------------------------------------------------------------- posing
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """a hanging limb: fwd swings it forward (up, past 90), out away from his side, turn about its own length"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def T(lean=0.0, twist=0.0, side=0.0):
    """a trunk (or the head): lean forward (+) / back (-), twist to his left (+), tip to his right side (+)"""
    return qs(('y', twist), ('x', lean), ('z', side))


def _corners(part):
    """a part's element corners, design units (an element's own turn ignored - near enough for grounding)"""
    pv = PIVOT[part]; out = []
    for e in _build()[part]:
        f, t = e['from'], e['to']
        for x in (f[0], t[0]):
            for y in (f[1], t[1]):
                for z in (f[2], t[2]):
                    out.append((x - 8 + pv[0], y - 8 + pv[1], z - 8 + pv[2]))
    return out


def lowest(pose, parts):
    xf = RK.solve(PIVOT, PARENT, pose); lo = 1e9
    for p in parts:
        q, t = xf[p]; pv = D(PIVOT[p]); W = tuple(t[i] + pv[i] for i in range(3))
        for c in _corners(p):
            r = qrot(q, tuple(D(c)[i] - pv[i] for i in range(3)))
            lo = min(lo, W[1] + r[1])
    return lo


def ground(pose, parts=('legr', 'legl')):
    pose = dict(pose); o = pose.get('_off', (0.0, 0.0, 0.0)); pose['_off'] = (o[0], 0.0, o[2])
    lo = lowest(pose, parts); pose['_off'] = (o[0], round(-lo, 4), o[2])
    return pose


def _tail_pose(sway=0.0, lift=0.0):
    return dict(tail1=T(-10 + lift, sway), tail2=T(8 + lift * 0.5, sway * 1.2), tail3=T(-14 + lift * 0.3, sway * 1.4))


CROWN = T(0, 0, -6)                     # (worn at a jaunty tilt)


def _pose(name):
    s_ = math.sin
    if name in ('idle_a', 'idle_b'):                          # (proud: chest out, the sceptre upright, the left paw at his belly)
        b = name == 'idle_b'
        p = dict(body=T(-2 if b else 0, 0, 0), head=T(-4 if b else 2, 6 if b else -4, 2 if b else 0), jaw=T(4 if b else 0), crown=CROWN,
                 armr=limb(1, 6, 4), arml=limb(-1, 22, 8, -10), sceptre=T(-6), legr=limb(1, 2, 2), legl=limb(-1, -2, 2),
                 cape=T(-2 if b else -3), **_tail_pose(14 if b else -14))
        p['_off'] = (0.0, 0.5 if b else 0.0, 0.0)
        return ground(p)
    if name.startswith('walk_'):                              # (a heavy, rolling waddle)
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = dict(body=T(6, 6 * sw, 5 * sw), head=T(-4, -6 * sw, -4 * sw), jaw=T(0), crown=CROWN,
                 armr=limb(1, 10 - 16 * sw, 6), arml=limb(-1, 18 + 22 * sw, 10), sceptre=T(-8 + 6 * sw),
                 legr=limb(1, 24 * sw, 3), legl=limb(-1, -24 * sw, 3), cape=T(-8 - 4 * abs(sw), 0, -4 * sw), **_tail_pose(22 * sw, 4))
        p = ground(p)
        p['_off'] = (p['_off'][0], p['_off'][1] + 0.7 * abs(math.cos(ph)), p['_off'][2])
        return p
    if name == 'atk_0':                                       # (the wind-up: the sceptre hauled back over his right shoulder)
        p = dict(body=T(-10, -26, -4), head=T(-6, 18), jaw=T(10), crown=CROWN, armr=limb(1, 168, 16), arml=limb(-1, 46, 28),
                 sceptre=T(170), legr=limb(1, -14, 4), legl=limb(-1, 18, 4), cape=T(-6), **_tail_pose(-26, 10))
        return ground(p)
    if name == 'atk_1':                                       # (the blow: brought down in front of him, leaning into it)
        p = dict(body=T(22, 18, 4), head=T(-10, -12), jaw=T(24), crown=CROWN, armr=limb(1, 72, 4, -10), arml=limb(-1, -16, 30),
                 sceptre=T(-160), legr=limb(1, 26, 4), legl=limb(-1, -22, 4), cape=T(-18), **_tail_pose(24, 14))
        return ground(p)
    if name == 'sp_0':                                        # (THE ROYAL DECREE: rearing up, paws high, a screech)
        p = dict(body=T(-16), head=T(-24), jaw=T(38), crown=CROWN, armr=limb(1, 160, 26), arml=limb(-1, 150, 34),
                 sceptre=T(175), legr=limb(1, 6, 8), legl=limb(-1, 6, 8), cape=T(10), **_tail_pose(0, 28))
        return ground(p)
    if name == 'sp_1':                                        # (the sceptre slammed down into the floor, crouched over it)
        p = dict(body=T(30, 6), head=T(-20, -4), jaw=T(26), crown=CROWN, armr=limb(1, 52, 6), arml=limb(-1, 40, 30),
                 sceptre=T(70), legr=limb(1, 44, 10), legl=limb(-1, 30, 12), cape=T(-26), **_tail_pose(-10, -4))
        return ground(p)
    if name == 'hurt':                                        # (a flinch: back, jaw open, paws out)
        p = dict(body=T(-12, 8, -6), head=T(-18, -10, 8), jaw=T(22), crown=T(0, 0, -14), armr=limb(1, 20, 30), arml=limb(-1, 30, 40),
                 sceptre=T(-14), legr=limb(1, -8, 4), legl=limb(-1, 10, 4), cape=T(6), **_tail_pose(18, 16))
        return ground(p)
    if name == 'death_0':                                     # (he staggers: knees going, the crown slipping)
        p = dict(body=T(-14, 14, 12), head=T(-20, 16, 14), jaw=T(30), crown=T(-10, 0, -26), armr=limb(1, 40, 46), arml=limb(-1, 50, 56),
                 sceptre=T(-30), legr=limb(1, 26, 8), legl=limb(-1, -6, 12), cape=T(8), **_tail_pose(-20, -8))
        p['_o_crown'] = (2.0, -1.0, 1.0)
        return ground(p)
    if name == 'death_1':                                     # (toppled onto his back, paws in the air, the crown knocked off his head)
        p = dict(body=T(-86, 6), head=T(-8, 18), jaw=T(36), crown=T(-30, 0, -70), armr=limb(1, 96, 50), arml=limb(-1, 110, 40),
                 sceptre=T(-60), legr=limb(1, 80, 18), legl=limb(-1, 64, 24), cape=T(0), **_tail_pose(30, -30))
        p['_o_crown'] = (6.0, -4.0, -6.0)
        return ground(p, PARTS)
    if name == 'arrive_0':                                    # (crouched low, out of the dark)
        p = dict(body=T(38), head=T(-26, 10), jaw=T(6), crown=CROWN, armr=limb(1, 38, 10), arml=limb(-1, 44, 14),
                 sceptre=T(44), legr=limb(1, 58, 10), legl=limb(-1, 50, 10), cape=T(-30), **_tail_pose(-30, -10))
        return ground(p)
    if name == 'arrive_1':                                    # (risen: the sceptre up, jaws wide - a roar)
        p = dict(body=T(-12, -10), head=T(-22, 8), jaw=T(40), crown=CROWN, armr=limb(1, 150, 10), arml=limb(-1, 30, 44),
                 sceptre=T(170), legr=limb(1, -10, 8), legl=limb(-1, 12, 8), cape=T(8), **_tail_pose(26, 24))
        return ground(p)
    raise KeyError(name)


POSE_NAMES = ('idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'atk_0', 'atk_1', 'sp_0', 'sp_1', 'hurt',
              'death_0', 'death_1', 'arrive_0', 'arrive_1')
def _tail_clear(p, k=0.3):
    """the tail lifted (its root turned up, a little at a time) until it clears the floor"""
    for _ in range(40):
        if lowest(p, ('tail1', 'tail2', 'tail3')) >= k: break
        p['tail1'] = RK.qmul(p['tail1'], RK.qa('x', 2.0))
    return p


POSES = {n: (_pose(n) if n == 'death_1' else _tail_clear(_pose(n))) for n in POSE_NAMES}


def rp(R):
    """gen_rp: the rk_ block textures (TEXTURE_MODS) and every part as a 3D model at display scale (HATS, DISPLAY_3D_EXTRA)"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
