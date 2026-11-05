"""(3.x draft, stage 1: art only - not wired) THE GUIDE - a little non-combat companion you switch on from the Black Market
Handbook (phase260). It follows like the Pixel Creeper (phase256): no fights, no buffs, not counted as a follower; right-click
it and the Handbook opens. The player picks one of FOUR forms, each its own small rig (all ~0.45-0.55 blocks, a handful of parts,
every one well under 60 elements):

  WISP       (guiw_)  a ball of warm-white light (the CORE: the only thing that glows - light_emission 15, shade off) inside a
                      soft see-through halo shell, two little feathered wings (one cut-out panel each, drawn feather by feather).
                      No face: it is a light.
  BUTTERFLY  (guib_)  vector-art: four flat wing panels in clean concentric rainbow bands (violet at the body out to red), a bold
                      indigo outline with white edge-dots, a small indigo body, curled antennae with gold tips. No noise at all.
  SUITCASE   (guis_)  a mini caramel-leather travel case on stubby little legs: rounded corners with dark corner caps, a stitched
                      front, two brass latches, a leather handle on top, a luggage tag that swings off the handle, a travel
                      sticker on its side. ITS EYES (its own eye language): rubber-hose cartoon eyes - tall white ovals, an
                      ink outline, a big black pupil with a pie-cut shine; an open smile, rosy cheeks.
  BOOK       (guik_)  the Handbook itself, awake: dark purple leather boards with a gold-foil frame and corners, a gilt-banded
                      spine, cream pages fanned a little open, a crimson ribbon bookmark tail. ITS EYES: gold-foil STAR EYES -
                      deep violet ovals ringed in gold, a four-point star sparkle in each; a tiny gold cat mouth, a pink blush.

Design units as every rig: feet / the bottom at y=0, facing -z, its right +x. The floaters (wisp, butterfly, book) are built
sitting low; HOVER[form] is how high above the ground the follow code should carry them (blocks, added to the display's
translation); the suitcase walks on the ground (HOVER 0) and hops.

POSES (every form): idle_a / idle_b (the float bob - stage 2 tweens between them, ~30 ticks a cycle; wing flutter for the wisp and
the butterfly, the cover and pages flapping for the book, a sway with the handle and tag swinging for the suitcase), move_0 /
move_1 (following: a lean forward, a faster flutter / beat; the suitcase hops), happy / happy_b (right-clicked: a bounce and a
twirl - two keys, played happy -> happy_b -> idle_a), frame (the item-frame / display-case pose, grounded, faced front), and on
the two faces a 'blink' pose (idle_a with the blink face). FACES: blink, happy, wow (the suitcase and the book)."""
import math
from PIL import Image, ImageDraw
from fol5_kit import Rig, hexc, mix, mul, limb, T, cells, soft, lit, put, slab, stack, ball, blush, mouth, _ell, _curve, _thick, stroke

HOVER = {'wisp': 1.30, 'butterfly': 1.40, 'book': 1.15, 'suitcase': 0.0}
FORMS = ('wisp', 'butterfly', 'suitcase', 'book')
NAMES = {'wisp': 'Wisp', 'butterfly': 'Rainbow Butterfly', 'suitcase': 'Suitcase', 'book': 'Little Handbook'}


def up2(fn, n=32):
    """a texture drawn on a 32 grid (one cell = 2 px of the 64 texture: the kit's cell size), transparent where fn gives None"""
    im = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    for y in range(n):
        for x in range(n):
            c = fn(x, y)
            if c is not None: im.putpixel((x, y), hexc(c) if isinstance(c, str) else c)
    return im.resize((n * 2, n * 2), Image.NEAREST)


def _mask(poly, n=32):
    m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    px = m.load(); return {(x, y) for y in range(n) for x in range(n) if px[x, y]}


def _edge(S):
    return {(x, y) for x, y in S if any((x + dx, y + dy) not in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}


def vpanel(R, part, x0, x1, y0, y1, z, tex, sx, rot=None, t=0.1, vflip=False):
    """a flat upright cut-out panel (a wing) in the x-y plane, its texture drawn as seen from the front with its ROOT at the
    image's right: mirrored per side and per face so the drawing sits the same way on both wings, front and back (vflip: the
    drawing upside down - a lower wing, fanned downward)"""
    e = R.box(part, (x0, y0, z - t / 2), (x1, y1, z + t / 2), tex, faces=('north', 'south'), rot=rot, full=True)
    a, b = ([0, 0, 16, 16], [16, 0, 0, 16]) if sx > 0 else ([16, 0, 0, 16], [0, 0, 16, 16])
    if vflip: a, b = [a[0], 16, a[2], 0], [b[0], 16, b[2], 0]
    e['faces']['north']['uv'] = a; e['faces']['south']['uv'] = b
    return e


def hpanel(R, part, x0, x1, z0, z1, y, tex, sx, rot=None, t=0.1):
    """a flat lying cut-out panel (a butterfly's wing) in the x-z plane: drawn as seen from above, the ROOT at the image's left
    and the front edge at its top; the underside the same drawing in the same place"""
    e = R.box(part, (x0, y - t / 2, z0), (x1, y + t / 2, z1), tex, faces=('up', 'down'), rot=rot, full=True)
    a, b = ([0, 0, 16, 16], [0, 16, 16, 0]) if sx > 0 else ([16, 0, 0, 16], [16, 16, 0, 0])
    e['faces']['up']['uv'] = a; e['faces']['down']['uv'] = b
    return e


def unshaded(els):
    """shade off (a face lit as painted, from every side): the wisp's light, its halo and its white wings - not a glow (only
    the core has light_emission)"""
    for e in els: e['shade'] = False
    return els


# ==================================================================================================== 1. THE WISP
WP = {'body': (0, 5.0, 0), 'wr': (1.9, 5.9, 0.9), 'wl': (-1.9, 5.9, 0.9), 'wr2': (1.8, 4.3, 0.9), 'wl2': (-1.8, 4.3, 0.9)}
WPAR = {'body': None, 'wr': 'body', 'wl': 'body', 'wr2': 'body', 'wl2': 'body'}
WISP = Rig('guiw_', 0.75, WP, WPAR, (), face_part='body')
CORE = dict(white='#ffffff', base='#fff7e0', warm='#ffeab0')
HALO = '#fff0b8'
FEATHER = dict(tip='#ffffff', base='#fffaf0', root='#ffefc8', line='#e2bd72', deep='#c99a4a')


def _blade(ox, oy, ang, L, W):
    """one feather on the 32 grid: from (ox, oy) along ang (image degrees, y down) for L cells, W wide, a round tip ->
    {cell: how far along it (0..1)}"""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); S = {}
    for y in range(32):
        for x in range(32):
            dx, dy = x + 0.5 - ox, y + 0.5 - oy; s = dx * ux + dy * uy; q = -dx * uy + dy * ux
            if -1 <= s <= L:
                hw = W / 2 if s < L - W / 2 else math.sqrt(max(0, (W / 2) ** 2 - (s - (L - W / 2)) ** 2))
                if abs(q) <= hw: S[(x, y)] = max(0.0, s) / L
    return S


def wisp_wing():
    """a little cartoon wing (its root at the image's right, low): a short arm rising up and out to the wrist, five long
    rounded feathers hung from it and fanned (the primaries off the wrist pointing out, the secondaries down), each white at
    its tip, cream at its root, a faint shaft, a pale-gold outline - drawn outer to inner so they overlap like real ones - and
    the coverts, a soft cream band along the arm over their roots"""
    R0, Wr = (29.5, 22.0), (19.0, 5.0)
    fe = [(1.00, 192, 17.0, 6.4), (0.80, 176, 18.5, 6.6), (0.58, 160, 17.0, 6.6), (0.36, 145, 14.5, 6.4), (0.14, 130, 11.0, 6.0)]
    out = {}
    for t, ang, L, W in fe:
        ox, oy = R0[0] + (Wr[0] - R0[0]) * t, R0[1] + (Wr[1] - R0[1]) * t
        S = _blade(ox, oy, ang, L, W); E = _edge(set(S)); sa, ca = math.sin(math.radians(ang)), math.cos(math.radians(ang))
        for p, s in S.items():
            c = FEATHER['line'] if p in E else (FEATHER['tip'] if s > 0.55 else FEATHER['base'])
            if p not in E and abs(-(p[0] + 0.5 - ox) * sa + (p[1] + 0.5 - oy) * ca) < 0.5 and 0.15 < s < 0.7:
                c = mix(FEATHER['line'], FEATHER['base'], 0.55)                                   # (the shaft)
            out[p] = c
    vx, vy = Wr[0] - R0[0], Wr[1] - R0[1]; cov = set()
    for y in range(32):
        for x in range(32):
            t = max(0.0, min(1.0, ((x + .5 - R0[0]) * vx + (y + .5 - R0[1]) * vy) / (vx * vx + vy * vy)))
            if math.hypot(x + .5 - R0[0] - vx * t, y + .5 - R0[1] - vy * t) <= 4.2 - 1.4 * t: cov.add((x, y))
    E = _edge(cov)
    for p in cov: out[p] = FEATHER['line'] if p in E else FEATHER['root'] if p[0] > 24 else FEATHER['base']
    SIL = _edge(set(out)); part = mix(FEATHER['line'], FEATHER['root'], 0.45)
    for p, c in out.items():
        if c == FEATHER['line'] and p not in SIL: out[p] = part          # (inside the wing the feathers part in a softer line)
    return up2(lambda x, y: out.get((x, y)))


def halo_tex():
    def c(x, y, r):
        return (*hexc(HALO)[:3], 44 if (x + y) % 7 else 56)
    return cells(c, 3)


WISP.tex('core', soft(CORE['base'], CORE['white'], CORE['warm'], 1, 0.03))
WISP.tex('corec', soft(CORE['white'], CORE['white'], CORE['base'], 2, 0.1))
WISP.tex('halo', halo_tex())
WISP.tex('wing', wisp_wing())
# the core: a ball of light (the only glow), a brighter heart a hair in front of it; the halo: a soft shell round it
from fol5_kit import profile
unshaded(stack(WISP, 'body', [r + ('core' if i in (0, 4) else 'corec',) for i, r in enumerate(profile(2.7, 4.6, 2.3, 5))], 'core', light=15))
unshaded(ball(WISP, 'body', (0, 5.0, 0), 3.15, 'halo', 5))
for sx, p in ((1, 'wr'), (-1, 'wl')):
    x0 = 1.9 * sx
    unshaded([vpanel(WISP, p, min(x0, x0 + 6.2 * sx), max(x0, x0 + 6.2 * sx), 3.6, 9.8, 0.9, 'wing', sx, rot=('y', -22 * sx, (x0, 6.0, 0.9)))])
for sx, p in ((1, 'wr2'), (-1, 'wl2')):                         # (the lower pair: smaller, fanned down and out, a touch further back)
    x0 = 1.8 * sx
    unshaded([vpanel(WISP, p, min(x0, x0 + 4.3 * sx), max(x0, x0 + 4.3 * sx), 0.6, 4.9, 1.1, 'wing', sx, rot=('y', -30 * sx, (x0, 4.3, 1.1)), vflip=True)])


def wing(sx, raise_=0.0, back=0.0):
    """a wing's turn: raised (about the body's front-back axis), swept back (about the upright)"""
    return limb(sx, 0.0, -raise_, back)


def WPOSE(off=0.0, body=None, r=0.0, b=0.0, r2=0.0, b2=0.0, **kw):
    """r / b: the upper pair raised / swept back; r2 / b2: the lower pair's (out of step with the upper: one flutters while the
    other settles)"""
    p = {'_off': (0.0, off, 0.0), 'wr': wing(1, r, b), 'wl': wing(-1, r, b), 'wr2': wing(1, r2, b2), 'wl2': wing(-1, r2, b2)}
    if body: p['body'] = body
    p.update(kw); return p


WISP.POSES.update({
    'idle_a': WPOSE(0.0, r=6, b=0, r2=-12, b2=8),
    'idle_b': WPOSE(0.7, r=-14, b=10, r2=6, b2=0),
    'move_0': WPOSE(0.3, T(16), r=22, b=-6, r2=-22, b2=14),
    'move_1': WPOSE(0.0, T(12), r=-24, b=14, r2=14, b2=-4),
    'happy': WPOSE(2.0, T(-8, 0, 14), r=34, b=-10, r2=-26, b2=10),
    'happy_b': WPOSE(1.0, T(-4, 0, -14), r=-20, b=12, r2=18, b2=-6),
    'frame': WISP.ground(WPOSE(0.0, r=10, b=-4, r2=-6, b2=0), 0.6),
})
WISP.DRAFT = ['idle_a', 'idle_b', 'move_0', 'move_1', 'happy', 'happy_b', 'frame']


# ==================================================================================================== 2. THE BUTTERFLY
BY = 3.0
BP = {'body': (0, BY, 0), 'wr': (0.45, BY + 0.35, -0.5), 'wl': (-0.45, BY + 0.35, -0.5), 'ant': (0, BY + 0.5, -2.2)}
BPAR = {'body': None, 'wr': 'body', 'wl': 'body', 'ant': 'body'}
FLY = Rig('guib_', 0.6, BP, BPAR, (), face_part='body')
RAINBOW = ('#8a5cff', '#3a9cff', '#3fd07a', '#ffe03a', '#ff9a2a', '#ff4a62')       # (root out: violet, blue, green, yellow, orange, red)
INK, DOT, INK_L = '#2a1d52', '#ffffff', '#5a4a9e'


def rainbow_wing(poly, root, rmax, dots=True, edge_w=1.0):
    """a flat vector wing: the silhouette's cells in concentric bands from the root (crisp: one colour per band, no shading), a
    bold ink outline and an outer ink border carrying white dots (the edge band) - drawn on the 32 grid"""
    S = _mask(poly); E = _edge(S)
    E2 = _edge(S - E)
    n = len(RAINBOW)
    out = {}
    for (x, y) in S:
        d = math.hypot(x + 0.5 - root[0], y + 0.5 - root[1]) / rmax
        if (x, y) in E: out[(x, y)] = INK; continue
        if d > 0.86 and (x, y) in E2: out[(x, y)] = INK; continue
        if d > 0.9: out[(x, y)] = INK; continue
        out[(x, y)] = RAINBOW[min(n - 1, int(d / 0.9 * n))]
    if dots:
        for (x, y) in list(out):
            d = math.hypot(x + 0.5 - root[0], y + 0.5 - root[1]) / rmax
            if out[(x, y)] == INK and d > 0.9 and (x, y) not in E and (x * 3 + y * 5) % 7 == 0: out[(x, y)] = DOT
    return up2(lambda x, y: out.get((x, y)))


FORE = [(0, 9), (5, 5), (14, 2), (24, 0), (30, 1), (31, 6), (29, 13), (25, 21), (19, 28), (12, 31), (5, 30), (0, 26)]
HIND = [(0, 0), (10, 0), (20, 3), (27, 8), (31, 15), (29, 23), (23, 29), (14, 31), (6, 29), (1, 22), (0, 12)]
FLY.tex('fore', rainbow_wing(FORE, (0, 18), 34))
FLY.tex('hind', rainbow_wing(HIND, (0, 4), 32))
FLY.tex('ink', cells(lambda x, y, r: INK_L if y < 3 else INK, 4))
FLY.tex('inkh', cells(lambda x, y, r: INK_L if (y < 4 or x % 8 == 3) else INK, 5))
FLY.tex('gold', cells(lambda x, y, r: '#fff2a0' if y < 3 else '#ffd23a', 6))
# the body: a little thorax, a tapered abdomen, a round head; the antennae curl forward and out with gold tips
FLY.box('body', (-0.8, BY - 0.75, -1.5), (0.8, BY + 0.85, 0.5), 'inkh', shift=False)
FLY.seg('body', (0, BY - 0.05, 0.3), (0, BY - 0.35, 3.0), 1.2, 1.2, 'ink', shift=False)
FLY.seg('body', (0, BY - 0.35, 2.9), (0, BY - 0.6, 4.6), 0.75, 0.75, 'ink', shift=False)
FLY.box('body', (-0.7, BY - 0.5, -2.7), (0.7, BY + 0.8, -1.4), 'inkh', shift=False)
for sx in (1, -1):
    a, b, c = (0.3 * sx, BY + 0.7, -2.3), (0.9 * sx, BY + 2.4, -3.6), (1.7 * sx, BY + 3.2, -4.0)
    FLY.seg('ant', a, b, 0.22, 0.22, 'ink'); FLY.seg('ant', b, c, 0.22, 0.22, 'ink')
    FLY.box('ant', (c[0] - 0.32, c[1] - 0.32, c[2] - 0.32), (c[0] + 0.32, c[1] + 0.32, c[2] + 0.32), 'gold', shift=False)
# the wings: a forewing and a hindwing a side, flat (hinged along the body)
for sx, p in ((1, 'wr'), (-1, 'wl')):
    x0, x1 = 0.45 * sx, 0.45 * sx + 7.6 * sx
    hpanel(FLY, p, min(x0, x1), max(x0, x1), -6.6, 0.4, BY + 0.4, 'fore', sx)
    x1 = 0.45 * sx + 6.0 * sx
    hpanel(FLY, p, min(x0, x1), max(x0, x1), -0.3, 5.3, BY + 0.32, 'hind', sx)


def bwing(sx, up):
    """a butterfly wing's turn: raised `up` degrees about the body's long axis"""
    return limb(sx, 0.0, up)


def BPOSE(off=0.0, body=T(-18), up=30, up2=None, ant=None, **kw):
    p = {'_off': (0.0, off, 0.0), 'body': body, 'wr': bwing(1, up), 'wl': bwing(-1, up if up2 is None else up2)}
    if ant: p['ant'] = ant
    p.update(kw); return p


FLY.POSES.update({
    'idle_a': BPOSE(0.0, up=34, ant=T(4)),
    'idle_b': BPOSE(0.6, up=8, ant=T(-6)),
    'move_0': BPOSE(0.4, T(-4), up=62, ant=T(14)),
    'move_1': BPOSE(0.0, T(-6), up=-10, ant=T(6)),
    'happy': BPOSE(2.2, T(-40, 0, 20), up=70, ant=T(-14)),
    'happy_b': BPOSE(1.0, T(-30, 0, -20), up=4, ant=T(10)),
    'frame': FLY.ground(BPOSE(0.0, T(-62), up=22, ant=T(-10)), 0.3),
})
FLY.DRAFT = ['idle_a', 'idle_b', 'move_0', 'move_1', 'happy', 'happy_b', 'frame']


# ==================================================================================================== 3. THE SUITCASE
SP = {'body': (0, 4.4, 0), 'handle': (0, 8.5, 0), 'tag': (1.6, 9.5, -0.1), 'legr': (2.3, 2.0, 0), 'legl': (-2.3, 2.0, 0)}
SPAR = {'body': None, 'handle': 'body', 'tag': 'handle', 'legr': None, 'legl': None}
SFACES = ('blink', 'happy', 'wow')
CASE = Rig('guis_', 0.8, SP, SPAR, SFACES, face_part='body')
LEATHER = dict(base='#d6955a', light='#e8ae72', dark='#bd7d46', deep='#8a5228', stitch='#f4cf9a')
CAP, CAP_L = '#6a3a1e', '#8a5230'
BRASS = ('#8a5a10', '#c8901e', '#f0c040', '#fff0a0')
SINK, SPUP, SWHITE = '#2a1408', '#140804', '#fffdf6'
SCHEEK, SMOUTH, STONGUE = '#f2846a', '#4a1a0c', '#ff7a8a'
SFW, SFH = 9.0, 5.7                      # (the front plate: x -4.5..4.5, y 2.4..8.1 -> 36 x 23 texels)
SEYE = (11, 25)                          # (the eyes' centre columns, the plate's 36 texels)


def toon_eye(im, cx, y0, kind=None, flip=False):
    """the Suitcase's eyes - rubber-hose cartoon eyes: a tall white oval (6 x 8), an ink outline, a big black pupil low in it
    looking up at you, a PIE-CUT shine (a wedge of white cut out of the pupil, top-right on both: one light). Kinds: None,
    'blink' (a closed smile-line, two lash flicks), 'happy' (thick ^ arches), 'wow' (the pupil shrunk to a startled dot)"""
    w, h = 6, 8
    if kind == 'blink':
        S = _curve(cx, y0 + 5, w + 1, -2) | _curve(cx, y0 + 6, w - 1, -2)
        stroke(im, S, SINK); o = 1 if flip else -1
        put(im, cx + o * 4, y0 + 4, SINK); put(im, cx + o * 4 + o, y0 + 3, SINK)
        return
    if kind == 'happy':
        stroke(im, _thick(_curve(cx, y0 + 5, w + 1, 3), 2), SINK); return
    S = _ell(cx, y0 + h / 2, w / 2, h / 2)
    stroke(im, S, SWHITE, rim=SINK)
    if kind == 'wow':
        P = _ell(cx, y0 + h / 2 + 0.5, 1.2, 1.6)
    else:
        P = _ell(cx, y0 + h / 2 + 0.8, 2.0, 2.7)
    P &= S
    for x, y in P: put(im, x, y, SPUP)
    if kind != 'wow':
        top = min(y for _, y in P); right = max(x for x, _ in P)
        for x, y in ((right - 1, top + 1), (right, top + 1), (right - 1, top + 2), (right, top + 2)):      # (the pie-cut: a notch of
            if (x, y) in S: put(im, x, y, SWHITE)                                                         #  white out of the pupil)


def case_face(kind=None):
    """the front plate: caramel leather (soft cells, light from above), a stitched seam just inside its edge, rosy cheeks and
    an open smile; the eyes are their own overlay"""
    im = lit(soft(LEATHER['base'], LEATHER['light'], LEATHER['dark'], 11, 0.05), 1.06, 0.94, 6)
    W, H = int(SFW * 4), int(SFH * 4)
    for x in range(2, W - 2):
        if x % 3 != 0: put(im, x, 1, LEATHER['stitch']); put(im, x, H - 2, LEATHER['stitch'])
    for y in range(2, H - 2):
        if y % 3 != 0: put(im, 1, y, LEATHER['stitch']); put(im, W - 2, y, LEATHER['stitch'])
    for cx in (SEYE[0] - 4, SEYE[1] + 4):
        blush(im, cx, 15, 4, SCHEEK, mix(SCHEEK, LEATHER['base'], 0.5))
    mk = {None: 'open', 'blink': 'open', 'happy': 'open', 'wow': 'o'}[kind]
    mouth(im, 18, 14, mk, SMOUTH, STONGUE, 8 if kind != 'happy' else 10)
    return im


def case_eyes(kind=None):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for i, cx in enumerate(SEYE): toon_eye(im, cx, 4, kind, i == 1)
    return im


def sticker():
    """the side: leather, and a round travel sticker - a cream disc, a teal ring, a gold star"""
    im = lit(soft(LEATHER['base'], LEATHER['light'], LEATHER['dark'], 12, 0.05), 1.06, 0.94, 6)
    d = ImageDraw.Draw(im); cx, cy = 8, 12
    d.ellipse((cx - 6, cy - 6, cx + 5, cy + 5), fill=hexc('#2a8a8a')); d.ellipse((cx - 4, cy - 4, cx + 3, cy + 3), fill=hexc('#fff4dc'))
    for x, y in ((0, -2), (-1, -1), (0, -1), (1, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (-1, 1), (1, 1)):
        put(im, cx + x - 0.5, cy + y, BRASS[2])
    return im


def back_tex():
    """the back: leather and an old hotel label, tilted - a purple oval, a gold rim and a gold star (the Black Market's own)"""
    im = lit(soft(LEATHER['base'], LEATHER['light'], LEATHER['dark'], 13, 0.05), 1.06, 0.94, 6)
    S = {(x, y) for x, y in _ell(24, 12, 7, 5)}
    for x, y in _ell(24, 12, 8, 6) - S: put(im, x, y, BRASS[2])
    for x, y in S: put(im, x, y, '#4a2272' if y > 9 else '#5e2e8c')
    for x, y in ((0, -2), (-1, -1), (0, -1), (1, -1), (-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0), (-1, 1), (0, 1), (1, 1), (-2, 2), (2, 2)):
        put(im, 24 + x, 12 + y, BRASS[2])
    return im


def tag_tex():
    im = cells(lambda x, y, r: '#fff4dc' if y > 1 else '#ffe8b8', 13)
    d = ImageDraw.Draw(im)
    for x in range(2, 7): put(im, x, 8, '#c84a3a'); put(im, x, 10, '#c8a070')
    put(im, 4, 3, '#8a6a4a'); put(im, 5, 3, '#8a6a4a')
    return im


CASE.tex('leather', lit(soft(LEATHER['base'], LEATHER['light'], LEATHER['dark'], 10, 0.05), 1.06, 0.94, 6))
CASE.tex('leathert', soft(LEATHER['light'], mix(LEATHER['light'], '#ffffff', 0.2), LEATHER['base'], 14, 0.05))
CASE.tex('side', sticker()); CASE.tex('back', back_tex())
CASE.tex('cap', lit(soft(CAP, CAP_L, mul(CAP, 0.85), 15, 0.1), 1.12, 0.92, 4))
CASE.tex('latch', cells(lambda x, y, r: BRASS[0] if (x == 1 and 2 <= y <= 3) else BRASS[3] if y == 0 else BRASS[1] if y >= 5 else BRASS[2], 20))
CASE.tex('brass', lit(cells(lambda x, y, r: BRASS[3] if y == 0 else BRASS[2] if y < 3 else BRASS[1], 16), 1.0, 0.86, 4))
CASE.tex('strap', lit(soft('#5a3018', '#764222', '#4a2612', 17, 0.08), 1.1, 0.9, 3))
CASE.tex('seam', cells(lambda x, y, r: LEATHER['deep'], 18))
CASE.tex('shoe', lit(soft('#3a2418', '#54362a', '#2a1810', 19, 0.08), 1.15, 0.85, 3))
CASE.tex('tagt', tag_tex())
CASE.tex('face', case_face()); CASE.tex('eyes', case_eyes())
for f in SFACES:
    CASE.tex(f'face_{f}', case_face(f)); CASE.tex(f'eyes_{f}', case_eyes(f))
B = CASE.box
# the case: a fat rounded box (front view: the corners cut), the lid seam round its middle, dark corner caps
e = B('body', (-4.5, 2.4, -2.0), (4.5, 8.1, 2.0), 'leather', shift=False)
e['faces']['west']['texture'] = '#side'; e['faces']['south']['texture'] = '#back'
e['faces']['up']['texture'] = '#leathert'
B('body', (-4.0, 2.0, -1.8), (4.0, 2.4, 1.8), 'leather', shift=False)
B('body', (-4.0, 8.1, -1.8), (4.0, 8.5, 1.8), 'leathert', shift=False)
B('body', (-4.6, 2.5, -0.12), (4.6, 8.0, 0.12), 'seam')
B('body', (-SFW / 2, 2.4, -2.02), (SFW / 2, 2.4 + SFH, -2.0), 'FACE', faces=('north',), uv={'north': [0, 0, SFW, SFH]})
B('body', (-SFW / 2, 2.4, -2.05), (SFW / 2, 2.4 + SFH, -2.03), 'EYES', faces=('north',), uv={'north': [0, 0, SFW, SFH]})
for sx in (1, -1):
    for sy, yy in ((1, 8.5), (-1, 2.0)):
        x0, x1 = sorted((4.62 * sx, 3.5 * sx)); y0, y1 = sorted((yy + 0.08 * sy, yy - 1.2 * sy))
        B('body', (x0, y0, -2.12), (x1, y1, 2.12), 'cap', shift=False)
    B('body', (2.0 * sx - 0.45, 7.25, -2.16), (2.0 * sx + 0.45, 8.62, -1.9), 'latch', shift=False)          # (the brass latches)
# the handle: two brass mounts and a rounded leather grip
for sx in (1, -1): B('handle', (1.7 * sx - 0.45, 8.5, -0.45), (1.7 * sx + 0.45, 8.9, 0.45), 'brass', shift=False)
for a, b in (((-1.75, 8.8, 0), (-1.3, 10.0, 0)), ((-1.35, 10.0, 0), (1.35, 10.0, 0)), ((1.3, 10.0, 0), (1.75, 8.8, 0))):
    CASE.seg('handle', a, b, 0.8, 0.75, 'strap', up=(0, 0, -1), ext=0.18, shift=False)
# the luggage tag: a string off the handle and a little card on it
CASE.seg('tag', (1.6, 9.5, -0.1), (4.78, 8.55, -0.1), 0.16, 0.16, 'seam')
CASE.box('tag', (4.66, 6.3, -0.9), (4.78, 8.6, 0.7), 'tagt', faces=('east', 'west'), full=True)
# stubby legs: a short leg, a round little shoe
for p, sx in (('legr', 1), ('legl', -1)):
    x = SP[p][0]
    B(p, (x - 0.65, 0.7, -0.65), (x + 0.65, 2.2, 0.65), 'strap', shift=False)
    B(p, (x - 0.9, 0.0, -1.4), (x + 0.9, 0.9, 0.8), 'shoe', shift=False)
    B(p, (x - 0.65, 0.0, -1.8), (x + 0.65, 0.75, -1.3), 'shoe', shift=False)


def SPOSE(lift=0.0, **kw):
    return CASE.ground(kw, lift)


CASE.POSES.update({
    'idle_a': SPOSE(0.0, tag=T(0, 0, 4)),
    'idle_b': SPOSE(0.0, body=T(0, 0, 6), handle=T(0, 0, -16), tag=T(6, 0, -10), legr=limb(1, 0, -6), legl=limb(-1, 0, 6)),
    'move_0': SPOSE(1.6, body=T(10), handle=T(-34), tag=T(-30), legr=limb(1, -30), legl=limb(-1, 24)),
    'move_1': SPOSE(0.0, body=T(-4), handle=T(12), tag=T(14), legr=limb(1, 22), legl=limb(-1, -26)),
    'happy': SPOSE(3.0, _face='happy', body=T(-6, 24, 0), handle=T(30), tag=T(30, 0, 30), legr=limb(1, 40, 20), legl=limb(-1, 40, 20)),
    'happy_b': SPOSE(1.2, _face='happy', body=T(0, -24, 8), handle=T(-20, 0, 20), tag=T(-10, 0, -30), legr=limb(1, 0, 30), legl=limb(-1, 0, 30)),
    'frame': SPOSE(0.0, tag=T(0, 0, 4)),
})
CASE.POSES['blink'] = dict(CASE.POSES['idle_a'], _face='blink')
CASE.DRAFT = ['idle_a', 'idle_b', 'blink', 'move_0', 'move_1', 'happy', 'happy_b', 'frame']


# ==================================================================================================== 4. THE BOOK
KP = {'body': (0, 5.0, 0), 'cover': (3.7, 5.0, -1.25), 'pg1': (3.4, 5.0, -1.0), 'pg2': (3.4, 5.0, -0.95), 'ribbon': (0.6, 0.4, 0.2)}
KPAR = {'body': None, 'cover': 'body', 'pg1': 'body', 'pg2': 'body', 'ribbon': 'body'}
KFACES = ('blink', 'happy', 'wow')
BOOK = Rig('guik_', 0.75, KP, KPAR, KFACES, face_part='cover')
PURPLE = dict(base='#4a2272', light='#5e2e8c', dark='#3a1a5c', deep='#26103e')
GOLD = ('#7a5208', '#c8901e', '#f0c040', '#fff0a0')
PAGE = ('#fff6e0', '#efe0c0', '#d8c49a')
RIBBON = ('#8a1426', '#c8243c', '#ee5064')
KFW, KFH = 7.4, 10.0                      # (the cover: 30 x 40 texels)
KEYE = (9, 21)
KBLUSH = '#ff7ab0'
STAR_IRIS = ('#140828', '#24103e', '#3a1e62', '#5a3490', '#8a62c8')


def star_eye(im, cx, y0, kind=None, flip=False):
    """the Book's eyes - gold-foil STAR EYES: a deep violet oval (7 x 9) shaded dark at the top to lavender at the bottom, ringed
    in gold foil (a darker gold under it, as stamped foil), a four-point STAR sparkle up and toward its left, a small dot low on
    the other side. Kinds: None, 'blink' (a gold closed curve, an outer lash), 'happy' (gold ^ arches), 'wow' (round, the
    star bigger)"""
    w, h = 7, 9
    o = 1 if flip else -1
    if kind == 'blink':
        S = _curve(cx, y0 + 6, w + 1, -2)
        stroke(im, _thick(S, 2), GOLD[2]); put(im, cx + o * 4, y0 + 5, GOLD[2]); put(im, cx + o * 5, y0 + 4, GOLD[2])
        return
    if kind == 'happy':
        stroke(im, _thick(_curve(cx, y0 + 6, w + 1, 3), 2), GOLD[2]); return
    if kind == 'wow': w, h = 8, 9
    S = _ell(cx, y0 + h / 2, w / 2, h / 2)
    top, bot = min(y for _, y in S), max(y for _, y in S)
    for x, y in _ell(cx, y0 + h / 2, w / 2 + 1, h / 2 + 1) - S: put(im, x, y, GOLD[2] if y < y0 + h - 1 else GOLD[1])
    for x, y in S:
        t = (y - top) / max(1, bot - top); put(im, x, y, STAR_IRIS[min(4, int(t * 5))])
    sx, sy = cx - 1 - (1 if kind == 'wow' else 0), top + 2 + (0 if kind != 'wow' else 1)
    arms = 2 if kind == 'wow' else 1
    for k in range(1, arms + 1):
        for dx, dy in ((k, 0), (-k, 0), (0, k), (0, -k)): put(im, sx + dx, sy + dy, GOLD[3])
    put(im, sx, sy, '#ffffff')
    put(im, cx + 2, bot - 1, '#ffffff' if kind != 'wow' else GOLD[3])


def cover_face(kind=None):
    """the front board: purple leather, a gold-foil frame (a fine double rule) with filled corner pieces, a small gold diamond
    crest at the top; a pink blush and a tiny gold cat-mouth (the eyes are their own overlay)"""
    im = lit(soft(PURPLE['base'], PURPLE['light'], PURPLE['dark'], 21, 0.05), 1.1, 0.92, 8)
    W, H = int(KFW * 4), int(KFH * 4)
    for x in range(W):
        for y in range(H):
            dx, dy = min(x, W - 1 - x), min(y, H - 1 - y)
            if (dx == 1 and dy >= 1) or (dy == 1 and dx >= 1): put(im, x, y, GOLD[2])
            if dx + dy <= 5 and dx >= 1 and dy >= 1: put(im, x, y, GOLD[2] if dx + dy < 5 else GOLD[1])
            if (dx == 3 and dy >= 3) or (dy == 3 and dx >= 3): put(im, x, y, GOLD[1])
    cx = W // 2
    for dy, hw in ((5, 0), (6, 1), (7, 2), (8, 1), (9, 0)):
        for x in range(cx - hw - 1, cx + hw): put(im, x, dy, GOLD[2] if dy < 7 else GOLD[1])
    put(im, cx - 1, 6, GOLD[3])
    by = 25
    if kind == '_back': return im
    if True:
        for c in KEYE:
            blush(im, c + (-1 if c < cx else 1), by, 5, KBLUSH, mix(KBLUSH, PURPLE['base'], 0.45))
    mouth(im, cx, by + 1, 'o' if kind == 'wow' else 'cat', GOLD[2], '#ff8ab8', 4)
    return im


def back_board():
    im = cover_face('_back'); return im


def cover_eyes(kind=None):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for i, cx in enumerate(KEYE): star_eye(im, cx, 14, kind, i == 1)
    return im


def pages(vertical):
    return cells(lambda x, y, r: (PAGE[1] if (x if vertical else y) % 2 else PAGE[0]) if (x if vertical else y) % 5 else PAGE[2], 22)


BOOK.tex('board', lit(soft(PURPLE['base'], PURPLE['light'], PURPLE['dark'], 23, 0.05), 1.1, 0.92, 8))
BOOK.tex('boardb', back_board())
BOOK.tex('pagev', pages(True)); BOOK.tex('pageh', pages(False))
BOOK.tex('sheet', soft(PAGE[0], '#ffffff', PAGE[1], 25, 0.08))
BOOK.tex('gilt', lit(cells(lambda x, y, r: GOLD[3] if y == 0 else GOLD[2] if y < 2 else GOLD[1], 26), 1.0, 0.9, 2))
BOOK.tex('ribbon', lit(cells(lambda x, y, r: RIBBON[2] if x % 4 == 0 else RIBBON[1], 27), 1.1, 0.85, 4))
BOOK.tex('face', cover_face()); BOOK.tex('eyes', cover_eyes())
for f in KFACES:
    BOOK.tex(f'face_{f}', cover_face(f)); BOOK.tex(f'eyes_{f}', cover_eyes(f))
B = BOOK.box
# the back board, the page block (its edges ruled as pages), the round spine with two gilt bands
B('body', (-3.7, 0.0, 1.0), (3.7, 10.0, 1.5), 'boardb', shift=False)
e = B('body', (-3.4, 0.35, -1.0), (3.4, 9.65, 1.0), 'pagev', shift=False)
for k in ('up', 'down'): e['faces'][k]['texture'] = '#pageh'
B('body', (3.4, 0.0, -1.5), (3.95, 10.0, 1.5), 'board', shift=False)
B('body', (3.95, 0.0, -1.1), (4.3, 10.0, 1.1), 'board', shift=False)
for y in (1.6, 8.0):
    B('body', (3.93, y, -1.2), (4.38, y + 0.5, 1.2), 'gilt', shift=False)
# the front board (the face), hinged at the spine
B('cover', (-3.7, 0.0, -1.5), (3.7, 10.0, -1.0), 'board', shift=False)
B('cover', (-KFW / 2, 0.0, -1.52), (KFW / 2, KFH, -1.5), 'FACE', faces=('north',), uv={'north': [0, 0, KFW, KFH]})
B('cover', (-KFW / 2, 0.0, -1.55), (KFW / 2, KFH, -1.53), 'EYES', faces=('north',), uv={'north': [0, 0, KFW, KFH]})
# two loose pages that flutter, and the ribbon bookmark (a tail with a notched end)
B('pg1', (-3.25, 0.5, -1.06), (3.4, 9.5, -0.98), 'sheet', faces=('north', 'south', 'west'))
B('pg2', (-3.25, 0.5, -1.0), (3.4, 9.5, -0.92), 'sheet', faces=('north', 'south', 'west'))
BOOK.seg('ribbon', (0.6, 0.6, 0.2), (0.75, -1.6, 0.1), 0.9, 0.12, 'ribbon', up=(0, 0, -1))
BOOK.seg('ribbon', (0.75, -1.55, 0.1), (0.55, -3.0, 0.0), 0.9, 0.12, 'ribbon', up=(0, 0, -1))
for dx in (-0.28, 0.28):
    BOOK.seg('ribbon', (0.55 + dx, -2.95, 0.0), (0.55 + dx * 1.4, -3.6, 0.0), 0.36, 0.12, 'ribbon', up=(0, 0, -1))


def KPOSE(off=0.0, body=None, cover=22, p1=7, p2=14, rib=None, **kw):
    p = {'_off': (0.0, off, 0.0), 'cover': T(0, -cover, 0), 'pg1': T(0, -p1, 0), 'pg2': T(0, -p2, 0)}
    if body: p['body'] = body
    if rib: p['ribbon'] = rib
    p.update(kw); return p


BOOK.POSES.update({
    'idle_a': KPOSE(0.0, T(0, 0, 2), 18, 5, 11, T(0, 0, -4)),
    'idle_b': KPOSE(0.6, T(0, 0, -2), 28, 9, 19, T(0, 0, 6)),
    'move_0': KPOSE(0.3, T(14), 16, 4, 9, T(-26)),
    'move_1': KPOSE(0.0, T(10), 30, 10, 22, T(-14)),
    'happy': KPOSE(2.2, T(-14, 0, 10), 56, 24, 40, T(24, 0, 10), _face='happy'),
    'happy_b': KPOSE(1.0, T(-6, 0, -10), 44, 16, 32, T(-12, 0, -10), _face='happy'),
    'frame': BOOK.ground(KPOSE(0.0, None, 16, 4, 9, None), 0.0),
})
BOOK.POSES['blink'] = dict(BOOK.POSES['idle_a'], _face='blink')
BOOK.DRAFT = ['idle_a', 'idle_b', 'blink', 'move_0', 'move_1', 'happy', 'happy_b', 'frame']

RIGS = {'wisp': WISP, 'butterfly': FLY, 'suitcase': CASE, 'book': BOOK}
POSE_NAMES = ('idle_a', 'idle_b', 'move_0', 'move_1', 'happy', 'happy_b', 'frame')
