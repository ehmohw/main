"""(draft) THE PALE DRYAD - a little forest sprite of the Pale Garden, the pale-oak woods (Wilfrey's Keep stands in pale gardens
and dark forests). Gentle, a bit odd, often sleepy, and far older than she looks: a healer and a binder - roots that hold monsters
fast, spores that heal, mushrooms that glow. She glows softly at night: her small blue mushrooms, the faint orange spots on her
cap and the dot on her orange mushroom, and her eyes give off a soft light (light_emission, moderate - never neon) while the rest
of her stays unlit, so the glow reads as coming from the mushrooms. (The night-only part - extra glow particles after dark - is
wiring for later.)

The look (2nd pass, after the owner's note "more polished, not as creepy, smaller"): a sweet, slightly chibi girl about chest
high on a player (her cap's crown at ~1.15 blocks) - a big head under a big mushroom hat, a small body, short limbs. Warm
pale-cream skin with a peach blush; big anime-style glowing-blue eyes (a dark lash line, a dark-to-light iris, a dark pupil, a big shine); a small smile. Her hat is a
soft, rounded BLUE mushroom dome with raised ORANGE spots (faintly glowing), orange gills underneath and a slightly turned-down
rim, a tiny glowing mushroom sprouting from its crown. A neat pale silver-mint bob, two soft locks framing her face. A moss-green
dress: the bodice, a darker leaf sash, puffed moss sleeves, and a full flared skirt of moss over pale-oak leaves with a leafy
hem. Rounded hands; little orange mushroom shoes with cream spots and a tiny root curl at the heel. A few deliberate mushrooms:
one cluster on her left shoulder (two blue, one orange), one on her back, the tiny one on the cap.

The rig (rigkit): hips (the root: the sash), body (bodice, back cluster; bends at the waist), head (a face per expression; the
cap, gills, hair and the eyes' glowing overlay on it), arms bent at the elbow, legs bent at the knee, feet (shoes), and the skirt
as two panels on the hips, front and back, meeting at her sides - each swings on the hip line with the thigh that leads it, so
the skirt is whole from the front (no split down the middle) and a stride or a seat never pushes a leg through it. Design
units: feet at y=0, facing -z, her right is +x; RIG_SCALE 0.8 (the cap's crown at ~1.15 blocks, 1.2 to the tip of its tiny mushroom).

Pose keys: _face (an expression), _glow (True: every mushroom flares - the healing and bloom poses; a '_lit' model per mushroomed
part), skirtf / skirtb (worked out from the thighs unless a pose sets them), _off (the root's shift - worked out for every
grounded pose so her shoes, or her seat, rest on y=0)."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, qa, qmul, qrot, el, seg, solve, D

PREFIX = 'pd_'
RIG_SCALE = 0.8
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
PIVOT = {'hips': (0, 8.0, 0), 'body': (0, 8.2, 0), 'head': (0, 13.6, 0),
         'armr': (3.35, 12.0, 0), 'forer': (3.35, 9.6, 0), 'arml': (-3.35, 12.0, 0), 'forel': (-3.35, 9.6, 0),
         'legr': (1.1, 8.0, 0), 'shinr': (1.1, 4.2, 0), 'footr': (1.1, 1.2, 0),
         'legl': (-1.1, 8.0, 0), 'shinl': (-1.1, 4.2, 0), 'footl': (-1.1, 1.2, 0),
         'skirtf': (0, 8.0, 0), 'skirtb': (0, 8.0, 0)}
PARENT = {'hips': None, 'body': 'hips', 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': 'hips', 'shinr': 'legr', 'footr': 'shinr', 'legl': 'hips', 'shinl': 'legl', 'footl': 'shinl',
          'skirtf': 'hips', 'skirtb': 'hips'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'sleepy', 'blink', 'fierce', 'surprised', 'sad')
GLOWS = ('head', 'body', 'arml')                                  # (the parts with mushrooms: a '_lit' model each, for _glow)
# the cap: (bottom, top, half-width) of each rounded slab, brim to crown - a soft dome, set a little back on her head (CZ)
CAP = [(18.2, 19.0, 5.6), (19.0, 19.9, 5.4), (19.9, 20.7, 5.0), (20.7, 21.5, 4.4), (21.5, 22.2, 3.6), (22.2, 22.7, 2.6), (22.7, 23.0, 1.5)]
CZ = 0.3

# light_emission (0-15): a soft glow at rest, a flare when she heals or blooms
L_BLUE, L_SPOT, L_EYES, L_CAP, L_FLARE = 8, 4, 6, 3, 15

# ---- colours: pale cream, soft moss green, blue cap with orange spots, a little orange
SKIN, SKIN_D, SKIN_L, BLUSH = '#f4e5d2', '#ebd7c0', '#f8ede0', '#f2b3a2'
MOSS, MOSS_D, MOSS_L = '#9fb88b', '#8ea97a', '#b0c79c'
LEAF, LEAF_D, LEAF_L = '#86a170', '#76905f', '#97b281'
SASH, SASH_D = '#6f8c5b', '#64804f'
BLUE, BLUE_D, BLUE_L, BLUE_H = '#3a6fd0', '#3262bd', '#4a80de', '#6e9ff0'
ORANGE, ORANGE_D, ORANGE_L = '#f0913a', '#dc7c2a', '#ffad5c'
CREAM, CREAM_D = '#fbf3e4', '#efe3cd'
GLOW, GLOW_L, GLOW_D = '#78d8ff', '#c9f4ff', '#4cb6ee'
HAIR, HAIR_D, HAIR_L = '#e2f4ec', '#cde8dd', '#f1fbf7'
EYE_T, EYE, EYE_B, PUPIL, LASH = '#2f86d2', '#4fc4fb', '#a4ebff', '#1c3a72', '#5b4743'
BROW, MOUTH = '#b49a89', '#b65d57'
ROOT, ROOT_D = '#a58b72', '#8f765f'


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    lit = '_lit' if pose.get('_glow') and p in GLOWS else ''
    return f'{PREFIX}{p}{face}{lit}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _cells(fn, seed, cell=2):
    """a 64 px texture painted cell by cell (2-px cells: half a design unit) - fn(cx, cy, rnd) -> colour"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im); rnd = random.Random(seed); n = 64 // cell
    for cy in range(n):
        for cx in range(n):
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(fn(cx, cy, rnd)))
    return im


def _soft(base, light, dark, seed, p=0.16):
    """gentle cell shading: mostly the base, a few cells a shade lighter or darker, in soft patches (never speckle-gritty)"""
    rnd = random.Random(seed * 7 + 1)
    patch = [[rnd.random() for _ in range(5)] for _ in range(5)]
    def c(x, y, r):
        k = patch[y * 4 // 32][x * 4 // 32]
        q = r.random()
        if q < p * (0.4 + k): return light
        if q > 1 - p * (1.4 - k) * 0.6: return dark
        return base
    return _cells(c, seed)


def _leaves():
    """pale-oak leaves, tidy: rows of overlapping leaves - a lighter tip, a darker edge below"""
    def c(x, y, r):
        k = (y + (x // 3) % 2 * 2) % 4
        if k == 3: return LEAF_D
        if k == 0: return LEAF_L
        return LEAF
    return _cells(c, 4430)


def _hair():
    """the bob: pale silver-mint, a faint strand line every few cells, a soft sheen band"""
    def c(x, y, r):
        if x % 4 == 3: return HAIR_D
        if 5 <= y <= 6: return HAIR_L
        return HAIR
    return _cells(c, 4420)


def _gills(lit=False):
    a, b = (ORANGE_L, ORANGE) if not lit else ('#ffd08a', '#ffb860')
    return _cells(lambda x, y, r: b if x % 2 == 0 else a, 4410)


def _shoe():
    """a little orange mushroom shoe: orange, two cream spots on each side"""
    im = _soft(ORANGE, ORANGE_L, ORANGE_D, 4440, 0.12); d = ImageDraw.Draw(im)
    for x, y in ((2, 2), (8, 1), (13, 3)):
        d.rectangle((x, y, x + 1, y + 1), fill=hexc(CREAM))
    return im


def _face(kind=None):
    """the face: 7 x 6.6 units (28 x 26 px from the top-left; the cap's rim hides rows 0-9). Warm cream; a peach blush low on
    each cheek (rows 21-22, out toward the edges), the mouth small (rows 23-24). The eyes are their own glowing overlay (_eyes):
    big, anime-style - her right eye (our left) cols 5-10, her left cols 17-22, rows 11-20. No brows at rest (the cap's rim
    shades her forehead); fierce, sad and surprised show a short brow on row 10."""
    im = _soft(SKIN, SKIN_L, SKIN_D, 4441, 0.08); d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=hexc(c))
    for x0 in (2, 22):                                                        # (blush)
        R(x0, 21, x0 + 3, 21, BLUSH); R(x0 + 1, 22, x0 + 2, 22, '#f6c7b8')
    for x0, inner in ((5, 1), (17, -1)):                                      # (inner: +1 if the eye's inner side is to the right)
        if kind == 'fierce':                                                  # (short, set low at the middle)
            R(x0 + 3, 10, x0 + 5, 10, BROW) if inner > 0 else R(x0, 10, x0 + 2, 10, BROW)
        elif kind == 'sad':                                                   # (raised at the middle: only the inner end shows)
            R(x0 + 4, 10, x0 + 5, 10, BROW) if inner > 0 else R(x0, 10, x0 + 1, 10, BROW)
        elif kind == 'surprised':
            R(x0 + 1, 10, x0 + 4, 10, BROW)
    if kind == 'happy':                                                       # (a small open smile)
        R(12, 23, 15, 23, '#8f4643'); R(13, 24, 14, 24, '#e58f8a')
    elif kind == 'surprised':
        R(13, 23, 14, 24, '#8f4643')
    elif kind == 'sad':
        R(13, 23, 14, 23, MOUTH); R(12, 24, 12, 24, MOUTH); R(15, 24, 15, 24, MOUTH)
    elif kind == 'fierce':
        R(12, 23, 15, 23, MOUTH)
    elif kind == 'sleepy':
        R(13, 24, 14, 24, MOUTH)
    else:                                                                     # (a small smile)
        R(12, 23, 12, 23, MOUTH); R(13, 24, 14, 24, MOUTH); R(15, 23, 15, 23, MOUTH)
    return im


def _eyes(kind=None):
    """the eyes' overlay (transparent but for the eyes, freckles and a tear; light_emission on its element): big anime eyes -
    a dark upper lash line with a flick at the outer corner, the glowing iris dark at the top and light at the bottom, a dark
    pupil, one big white shine and a small second highlight. The closed shapes (happy, blink, sleepy) are drawn to match."""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=hexc(c))
    MID = '#3aa5e8'
    grad = {13: EYE_T, 14: EYE_T, 15: MID, 16: MID, 17: EYE, 18: EYE, 19: EYE_B, 20: EYE_B}
    for x0, outer in ((5, -1), (17, 1)):
        ox, ix = (x0, x0 + 5) if outer < 0 else (x0 + 5, x0)                  # (outer / inner columns)
        if kind == 'blink':                                                   # (shut: a soft, contented curve, a lash flick)
            R(x0, 16, x0, 16, LASH); R(x0 + 1, 17, x0 + 4, 17, LASH); R(x0 + 5, 16, x0 + 5, 16, LASH)
            R(ox + outer, 15, ox + outer, 15, LASH)
        elif kind == 'happy':                                                 # (smiling arches, thick)
            R(x0, 17, x0, 18, LASH); R(x0 + 5, 17, x0 + 5, 18, LASH); R(x0 + 1, 15, x0 + 1, 16, LASH); R(x0 + 4, 15, x0 + 4, 16, LASH)
            R(x0 + 2, 14, x0 + 3, 15, LASH); R(x0 + 2, 16, x0 + 3, 16, EYE_B); R(x0 + 1, 17, x0 + 1, 17, EYE); R(x0 + 4, 17, x0 + 4, 17, EYE)
        elif kind == 'sleepy':                                                # (heavy lids: the lower half of the eye)
            R(x0, 15, x0 + 5, 16, LASH); R(ox + outer, 15, ox + outer, 15, LASH)
            for y in range(17, 21):
                a, b = (x0 + 1, x0 + 4) if y == 20 else (x0, x0 + 5)
                R(a, y, b, y, grad[y])
            R(x0 + 2, 17, x0 + 3, 19, PUPIL); R(x0 + 1, 17, x0 + 1, 17, '#ffffff'); R(x0 + 4, 19, x0 + 4, 19, '#dff8ff')
        else:
            top = 12 if kind == 'surprised' else 13
            R(x0, top - 2, x0 + 5, top - 1, LASH)                             # (the upper lash line, two pixels thick)
            if kind not in ('surprised', 'sad'): R(ox + outer, top - 2, ox + outer, top - 2, LASH)  # (the flick)
            for y in range(top, 21):
                c = grad.get(y, EYE_T)
                a, b = (x0 + 1, x0 + 4) if y == 20 else (x0, x0 + 5)          # (rounded at the bottom)
                R(a, y, b, y, c)
            if kind == 'sad': R(ox + outer, top, ox + outer, top, LASH)
            if kind == 'fierce':                                              # (the lid slants down to the middle)
                R(ix, top, ix, top, LASH); R(x0 + 2, top, x0 + 3, top, EYE_T)
            if kind == 'surprised':                                           # (a small pupil, wide eyes)
                R(x0 + 2, 15, x0 + 3, 17, PUPIL); R(x0 + 1, 13, x0 + 2, 14, '#ffffff'); R(x0 + 4, 18, x0 + 4, 18, '#dff8ff')
            else:
                R(x0 + 2, top + 1, x0 + 3, 19, PUPIL); R(x0 + 1, top + 1, x0 + 2, top + 2, '#ffffff'); R(x0 + 4, 18, x0 + 4, 18, '#dff8ff')
            if kind == 'sad' and outer > 0: R(x0 + 5, 21, x0 + 5, 22, GLOW)    # (a glowing tear)
    for x, y in ((3, 23), (5, 23), (22, 23), (24, 23)):                       # (a few soft glowing freckles)
        R(x, y, x, y, GLOW_D)
    return im


def textures():
    T = {'pd_skin': _soft(SKIN, SKIN_L, SKIN_D, 4401, 0.08), 'pd_skinb': _soft(SKIN_D, SKIN, '#e0c9b0', 4402, 0.12),
         'pd_moss': _soft(MOSS, MOSS_L, MOSS_D, 4404), 'pd_leaf': _leaves(), 'pd_sash': _soft(SASH, MOSS_D, SASH_D, 4403),
         'pd_cap': _soft(BLUE, BLUE_L, BLUE_D, 4405), 'pd_cap_lit': _soft(BLUE_L, BLUE_H, BLUE, 4405),
         'pd_gill': _gills(), 'pd_gill_lit': _gills(True), 'pd_hair': _hair(),
         'pd_cspot': _soft(ORANGE, ORANGE_L, ORANGE_D, 4415, 0.2), 'pd_cspot_lit': _soft('#ffd27a', '#ffe9b0', '#ffc35a', 4416, 0.2),
         'pd_stem': _soft(CREAM, '#fffaf0', CREAM_D, 4406, 0.12),
         'pd_mblue': _soft(GLOW_D, GLOW, '#3f9fd8', 4407, 0.2), 'pd_mblue_lit': _soft(GLOW_L, '#ffffff', GLOW, 4408, 0.2),
         'pd_morange': _soft(ORANGE, ORANGE_L, ORANGE_D, 4409, 0.15), 'pd_morange_lit': _soft('#ffb860', '#ffd890', ORANGE_L, 4411, 0.15),
         'pd_mspot': _soft('#ffe6a8', '#fff4d0', '#ffdc90', 4412, 0.2), 'pd_mspot_lit': _soft('#fff6dc', '#ffffff', '#fff0c8', 4413, 0.2),
         'pd_shoe': _shoe(), 'pd_sole': _soft(CREAM_D, CREAM, '#e2d3b8', 4417, 0.1), 'pd_root': _soft(ROOT, '#b39a80', ROOT_D, 4414, 0.15),
         'pd_face': _face(), 'pd_eyes': _eyes()}
    for k in FACES:
        T[f'pd_face_{k}'] = _face(k); T[f'pd_eyes_{k}'] = _eyes(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def B(sx, x0, x1, y0, y1, z0, z1, tex, piv, **kw):
    """a box on one side (sx = 1 her right, -1 her left: x mirrored)"""
    a, b = sorted((sx * x0, sx * x1))
    return el((a, y0, z0), (b, y1, z1), tex, piv, **kw)


def mush(A, d, piv, kind='blue', lit=False, size=1.0):
    """a small mushroom growing from A along d: a cream stem, a two-step cap. Blue ones glow; an orange one carries a faintly
    glowing dot on its crown. lit: the flare (_glow) - all of it bright and at full light"""
    L = math.sqrt(sum(v * v for v in d)); u = tuple(v / L for v in d)
    Bt = tuple(A[i] + d[i] for i in range(3))
    tip = tuple(Bt[i] + u[i] * 0.5 * size for i in range(3))
    cw = 1.5 * size; sfx = '_lit' if lit else ''
    lc = (L_FLARE if lit else L_BLUE) if kind == 'blue' else (L_FLARE if lit else 0)
    out = [seg(A, Bt, 0.5 * size, 0.5 * size, 'pd_stem', piv),
           seg(tuple(Bt[i] - u[i] * 0.15 * size for i in range(3)), tip, cw, cw, f'pd_m{kind}{sfx}', piv, light=lc),
           seg(tip, tuple(tip[i] + u[i] * 0.32 * size for i in range(3)), cw * 0.6, cw * 0.6, f'pd_m{kind}{sfx}', piv, light=lc)]
    if kind == 'orange':
        top = tuple(tip[i] + u[i] * 0.32 * size for i in range(3))
        out.append(seg(top, tuple(top[i] + u[i] * 0.06 for i in range(3)), cw * 0.3, cw * 0.3, f'pd_mspot{sfx}', piv,
                       light=L_FLARE if lit else L_SPOT))
    return out


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the hips: the leaf sash, a little bow at her left hip
    pv = PIVOT['hips']
    part('pd_hips', [el((-2.3, 7.6, -1.65), (2.3, 9.0, 1.65), 'pd_sash', pv, shift=(0.2, 0.4)),
                     el((-2.4, 6.5, -1.75), (2.4, 7.6, 1.75), 'pd_moss', pv, shift=(0.5, 0.6)),              # (the skirt's yoke)
                     el((-2.75, 8.0, -0.7), (-2.3, 8.9, 0.3), 'pd_sash', pv, shift=(0.6, 0.1)),              # (the bow)
                     el((-2.7, 7.0, -0.45), (-2.4, 8.0, -0.05), 'pd_sash', pv, shift=(0.3, 0.3))])

    # ---- the body: the moss bodice (a darker band at its top), and the back cluster
    pv = PIVOT['body']

    def body(lit):
        b = [el((-1.95, 8.2, -1.4), (1.95, 10.4, 1.4), 'pd_moss', pv, shift=(0.1, 0.5)),                   # waist
             el((-2.3, 10.2, -1.5), (2.3, 13.6, 1.5), 'pd_moss', pv, shift=(0.3, 0.2)),                     # chest
             el((-2.35, 12.9, -1.55), (2.35, 13.4, 1.55), 'pd_sash', pv, shift=(0.5, 0.1)),                 # (a band at the neckline)
             el((-0.9, 13.4, -0.9), (0.9, 13.65, 0.9), 'pd_skin', pv)]                                      # neck
        # the back cluster: an orange shelf, two blue caps above it
        sf = '_lit' if lit else ''
        b += [el((-1.3, 10.8, 1.5), (0.5, 11.25, 2.5), f'pd_morange{sf}', pv, light=L_FLARE if lit else 0),
              el((-0.65, 11.25, 1.85), (-0.15, 11.32, 2.25), f'pd_mspot{sf}', pv, light=L_FLARE if lit else L_SPOT)]
        b += mush((0.6, 11.8, 1.5), (0.3, 0.4, 0.9), pv, 'blue', lit, 0.75)
        b += mush((-0.8, 12.4, 1.5), (-0.3, 0.25, 0.8), pv, 'blue', lit, 0.6)
        return b
    part('pd_body', body(False)); part('pd_body_lit', body(True))

    # ---- the head: cream, the face, the eyes' glow; the cap (a soft dome, a slightly turned-down rim), gills; the bob
    pv = PIVOT['head']

    def layer(y0, y1, w, tex, sh, k=0.72):
        """one rounded slab of the cap: a box with its four corners cut (three boxes, none overlapping) - an octagon from above"""
        return [el((-w, y0, CZ - w * k), (w, y1, CZ + w * k), tex, pv, shift=sh),
                el((-w * k, y0, CZ - w), (w * k, y1, CZ - w * k), tex, pv, shift=(sh[0] + 0.3, sh[1])),
                el((-w * k, y0, CZ + w * k), (w * k, y1, CZ + w), tex, pv, shift=(sh[0] + 0.6, sh[1]))]

    def cap(lit):
        cp, gl, st = ('pd_cap_lit', 'pd_gill_lit', 'pd_cspot_lit') if lit else ('pd_cap', 'pd_gill', 'pd_cspot')
        lc = L_FLARE if lit else L_CAP
        y0b = CAP[0][0]; w0, k = CAP[0][2], 0.72
        c = layer(y0b - 0.3, y0b, w0 - 0.45, gl, (0.1, 0.1))                    # (the gills, under the brim)
        for i, (y0, y1, w) in enumerate(CAP):
            c += layer(y0, y1, w, cp, (0.17 * i, 0.23 * i))
        c += [el((-w0 * k, y0b - 0.4, CZ - w0), (w0 * k, y0b, CZ - w0 + 0.35), cp, pv, shift=(0.5, 0.3)),     # (the rim, turned down)
              el((-w0 * k, y0b - 0.4, CZ + w0 - 0.35), (w0 * k, y0b, CZ + w0), cp, pv, shift=(0.3, 0.9)),
              el((-w0, y0b - 0.4, CZ - w0 * k), (-w0 + 0.35, y0b, CZ + w0 * k), cp, pv, shift=(0.8, 0.4)),
              el((w0 - 0.35, y0b - 0.4, CZ - w0 * k), (w0, y0b, CZ + w0 * k), cp, pv, shift=(0.6, 0.7))]
        # the orange spots: raised a hair proud of the cap, glowing faintly - on the steps' ledges, the crown and the brim's edge
        for i, (y0, y1, w) in enumerate(CAP):
            wn = CAP[i + 1][2] if i + 1 < len(CAP) else 0.0
            ring = w - wn
            s = min(1.0, ring - 0.2) if wn else 0.8
            if s < 0.35: continue
            r = (w + wn) / 2 if wn else 0.0
            pts = [(0.45, -0.5), (-0.5, 0.4)] if not wn else \
                  [(r, -0.3 + 0.5 * (i % 2)), (-r, 0.4 - 0.6 * (i % 2)), (0.4 - 0.7 * (i % 2), -r), (-0.9 + 0.8 * (i % 2), r)]
            for j, (px, pz) in enumerate(pts):
                c.append(el((px - s / 2, y1, CZ + pz - s / 2), (px + s / 2, y1 + 0.12, CZ + pz + s / 2), st, pv, light=lc, shift=(0.2 * j, 0.1)))
        for x, zz, ax in ((-1.9, -w0, 'z'), (1.5, -w0, 'z'), (w0, -1.2, 'x'), (-w0, 0.8, 'x'), (w0, 1.9, 'x'), (0.4, w0, 'z')):
            d = -1 if (zz if ax == 'z' else x) < 0 else 1                      # (and on the brim's edge)
            if ax == 'z':
                a0, a1 = sorted((zz, zz + 0.1 * d))
                c.append(el((x - 0.4, y0b + 0.15, CZ + a0), (x + 0.4, CAP[0][1] - 0.1, CZ + a1), st, pv, light=lc))
            else:
                a0, a1 = sorted((x, x + 0.1 * d))
                c.append(el((a0, y0b + 0.15, CZ + zz - 0.4), (a1, CAP[0][1] - 0.1, CZ + zz + 0.4), st, pv, light=lc))
        c += mush((0.6, CAP[-1][1], CZ - 0.4), (0.15, 0.7, -0.1), pv, 'blue', lit, 0.5)     # (the tiny one on the crown)
        return c

    def head(face=None, lit=False):
        ft, et = ('pd_face', 'pd_eyes') if face is None else (f'pd_face_{face}', f'pd_eyes_{face}')
        h = [el((-3.5, 13.6, -3.3), (3.5, 20.2, 3.3), 'pd_skin', pv, faces=('south', 'east', 'west', 'up', 'down'), shift=(0.3, 0.6)),
             el((-3.5, 13.6, -3.32), (3.5, 20.2, -3.3), ft, pv, faces=('north',), uv={'north': [0, 0, 7, 6.6]}),
             el((-3.5, 13.6, -3.36), (3.5, 20.2, -3.34), et, pv, faces=('north',), uv={'north': [0, 0, 7, 6.6]}, light=L_FLARE if lit else L_EYES),
             # the bob: round the sides and back, to her jaw; two soft locks framing her face
             el((-3.9, 14.6, 3.3), (3.9, 18.0, 3.75), 'pd_hair', pv, shift=(0.2, 0.1)),
             el((-3.9, 14.0, -2.6), (-3.5, 18.0, 3.3), 'pd_hair', pv, shift=(0.4, 0.1)),
             el((3.5, 14.0, -2.6), (3.9, 18.0, 3.3), 'pd_hair', pv, shift=(0.6, 0.1)),
             el((-3.95, 13.75, -3.6), (-2.95, 18.0, -2.6), 'pd_hair', pv, shift=(0.1, 0.4)),
             el((2.95, 13.75, -3.6), (3.95, 18.0, -2.6), 'pd_hair', pv, shift=(0.3, 0.4))]
        for i in range(5):                                                     # (the bob's hem at the back, softly scalloped)
            x0 = -3.9 + i * 1.56
            h.append(el((x0 + 0.04, 14.0 if i % 2 else 14.2, 3.3), (x0 + 1.52, 14.6, 3.75), 'pd_hair', pv, shift=(0.15 * i, 0.5)))
        return h + cap(lit)
    for lit in (False, True):
        s = '_lit' if lit else ''
        part(f'pd_head{s}', head(None, lit))
        for fc in FACES:
            part(f'pd_head_x{fc}{s}', head(fc, lit))

    # ---- arms: puffed moss sleeves, cream arms, rounded hands; the shoulder cluster on her left
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']

        def arm(lit):
            a = [B(sx, 2.72, 3.98, 9.6, 11.7, -0.63, 0.63, 'pd_skin', ap, shift=(0.4, 0.5)),
                 B(sx, 2.65, 4.05, 10.9, 12.6, -0.78, 0.78, 'pd_moss', ap, shift=(0.2, 0.6))]              # (the puffed sleeve)
            if sx < 0:                                                         # (the shoulder cluster: on her left, out the side)
                a += mush((-3.7, 11.2, 0.63), (-0.55, 0.15, 0.75), ap, 'blue', lit, 0.85)
                a += mush((-3.98, 10.1, 0.3), (-0.8, -0.05, 0.2), ap, 'orange', lit, 0.65)
                a += mush((-4.05, 11.6, 0.5), (-0.6, 0.1, 0.25), ap, 'blue', lit, 0.5)
            return a
        part(f'pd_arm{s}', arm(False))
        if sx < 0: part(f'pd_arm{s}_lit', arm(True))
        part(f'pd_fore{s}', [B(sx, 2.75, 3.95, 7.5, 9.65, -0.6, 0.6, 'pd_skin', fp, shift=(0.6, 0.3)),
                             B(sx, 2.66, 4.04, 6.6, 7.6, -0.7, 0.7, 'pd_skin', fp, shift=(0.3, 0.1)),        # the hand, rounded
                             B(sx, 2.8, 3.9, 6.35, 6.6, -0.56, 0.56, 'pd_skin', fp, shift=(0.5, 0.2)),
                             B(sx, 2.58, 2.66, 6.85, 7.45, -0.55, -0.05, 'pd_skin', fp)])                  # (the thumb)

        # ---- legs: cream, a faint bark hint on the shins; little orange mushroom shoes, a root curl at the heel
        lp, kp, fp2 = PIVOT[f'leg{s}'], PIVOT[f'shin{s}'], PIVOT[f'foot{s}']
        part(f'pd_leg{s}', [B(sx, 0.35, 1.85, 4.2, 6.6, -0.75, 0.75, 'pd_skin', lp)])
        part(f'pd_shin{s}', [B(sx, 0.4, 1.8, 1.1, 4.3, -0.7, 0.7, 'pd_skinb', kp, shift=(0.5, 0.1))])
        part(f'pd_foot{s}', [B(sx, 0.2, 2.0, 0.0, 0.35, -1.75, 0.85, 'pd_sole', fp2),                          # the sole
                             B(sx, 0.2, 2.0, 0.35, 1.25, -1.45, 0.85, 'pd_shoe', fp2, shift=(0.2, 0.1)),      # the shoe
                             B(sx, 0.35, 1.85, 0.35, 0.95, -1.75, -1.45, 'pd_shoe', fp2, shift=(0.6, 0.3)),   # (its rounded toe)
                             B(sx, 0.45, 1.75, 1.25, 1.55, -1.1, 0.6, 'pd_shoe', fp2, shift=(0.4, 0.6)),
                             B(sx, 0.9, 1.3, 0.1, 0.55, 0.85, 1.25, 'pd_root', fp2),                          # (a root curl at the heel)
                             B(sx, 0.9, 1.3, 0.55, 0.85, 1.05, 1.4, 'pd_root', fp2)])

    # ---- the skirt: moss over pale-oak leaves, flaring to a leafy hem just above her knees. Two panels on the hips, front and
    #      back, meeting at her sides; each swings on the hip line with the thigh that leads it (the front with the more forward
    #      leg, the back with the one further back). Its top tucks up under the sash.
    for nm, sz in (('skirtf', -1), ('skirtb', 1)):
        pv = PIVOT[nm]
        z = lambda a, b: sorted((sz * a, sz * b))
        sk = [el((-2.6, 6.3, z(0, 1.95)[0]), (2.6, 6.6, z(0, 1.95)[1]), 'pd_moss', pv, shift=(0.2 + 0.3 * sz, 0.3)),
              el((-2.72, 6.05, z(0, 2.08)[0]), (2.72, 6.4, z(0, 2.08)[1]), 'pd_sash', pv, shift=(0.5, 0.1)),    # (a band)
              el((-3.0, 5.4, z(0, 2.3)[0]), (3.0, 6.1, z(0, 2.3)[1]), 'pd_leaf', pv, shift=(0.1, 0.4 + 0.2 * sz)),
              el((-3.35, 4.7, z(0, 2.55)[0]), (3.35, 5.4, z(0, 2.55)[1]), 'pd_leaf', pv, shift=(0.4, 0.2 + 0.2 * sz))]   # (flaring)
        for i in range(7):                                                     # (the hem: leaf points along the front / back)
            x0 = -3.3 + i * 0.95
            lo = 4.25 + 0.2 * (i % 2)
            sk.append(el((x0, lo, z(2.0, 2.55)[0]), (x0 + 0.65, 4.7, z(2.0, 2.55)[1]), 'pd_leaf', pv, shift=(0.11 * i, 0.7)))
        for sxx in (-1, 1):                                                    # (and at the sides)
            for j, zz in enumerate((0.1, 1.05)):
                a0, a1 = sorted((sxx * 2.8, sxx * 3.35))
                sk.append(el((a0, 4.3 + 0.2 * j, z(zz, zz + 0.7)[0]), (a1, 4.7, z(zz, zz + 0.7)[1]), 'pd_leaf', pv, shift=(0.3 * j, 0.8)))
        part(f'pd_{nm}', sk)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit: ('x', -a) swings a hanging limb forward; ('x', +a) on a trunk or head leans/nods it forward; a knee bends back with
#  ('x', +a) on the shin)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def knee(b):
    return qs(('x', b))


def P(**kw):
    return kw


s = math.sin
REST = dict(armr=limb(1, 4, 9), forer=limb(1, 12), arml=limb(-1, 4, 9), forel=limb(-1, 12))
STAND = dict(legr=limb(1, 0, 1), legl=limb(-1, 0, 1))
POSES = {
    # sweet and still: a little tilt of the head, hands soft at her sides
    'idle_a': P(**REST, **STAND, head=qs(('z', 5))),
    # sleepy: the head nodding to one side, a little sway
    'idle_b': P(_face='sleepy', body=qs(('z', 3), ('x', 3)), head=qs(('z', -10), ('x', 8)),
                armr=limb(1, 0, 7), forer=limb(1, 6), arml=limb(-1, 0, 7), forel=limb(-1, 6), legr=limb(1, 4, 1), shinr=knee(8), legl=limb(-1, -2, 1)),
    # holding up her hand to look at something in her palm, pleased
    'idle_c': P(_face='happy', head=qs(('x', 16), ('y', -10)), armr=limb(1, 20, 8, -10), forer=limb(1, 70), arml=limb(-1, 2, 9), forel=limb(-1, 12), **STAND),
    **{f'walk_{k}': P(head=qs(('z', 3 * s(math.pi * k / 2))), body=qs(('y', -4 * s(math.pi * k / 2))),
                      legr=limb(1, 22 * s(math.pi * k / 2)), shinr=knee(30 * max(0.0, -s(math.pi * k / 2)) + 4),
                      legl=limb(-1, -22 * s(math.pi * k / 2)), shinl=knee(30 * max(0.0, s(math.pi * k / 2)) + 4),
                      armr=limb(1, -20 * s(math.pi * k / 2), 9), forer=limb(1, 14), arml=limb(-1, 20 * s(math.pi * k / 2), 9), forel=limb(-1, 14))
       for k in range(4)},
    **{f'run_{k}': P(body=qs(('x', 10)), head=qs(('x', -8)),
                     legr=limb(1, (38, 8, -28, 8)[k]), shinr=knee((14, 64, 40, 20)[k]), legl=limb(-1, (-28, 8, 38, 8)[k]), shinl=knee((40, 20, 14, 64)[k]),
                     armr=limb(1, (-30, 0, 34, 0)[k], 12), forer=limb(1, 56), arml=limb(-1, (34, 0, -30, 0)[k], 12), forel=limb(-1, 56))
       for k in range(4)},
    'jump': P(_face='happy', legr=limb(1, 36), shinr=knee(60), legl=limb(-1, 12), shinl=knee(36),
              armr=limb(1, 10, 60), forer=limb(1, 20), arml=limb(-1, 10, 60), forel=limb(-1, 20), head=qs(('x', -6))),
    # sitting on the ground, legs out before her, hands in her lap; the back of the skirt spread on the ground behind
    'sit_a': P(skirtb=qs(('x', 78)), body=qs(('x', -4)), head=qs(('z', 6)), legr=limb(1, 84, 3), shinr=knee(8), legl=limb(-1, 84, 3), shinl=knee(8),
               footr=qs(('x', -8)), footl=qs(('x', -8)),
               armr=limb(1, 30, 8, -14), forer=limb(1, 40), arml=limb(-1, 30, 8, -14), forel=limb(-1, 40)),
    # (the seated idle's other beat) leaning back on her hands, one knee up, nodding off
    'sit_b': P(skirtb=qs(('x', 70)), _face='sleepy', body=qs(('x', -16)), head=qs(('z', -12), ('x', 10)),
               legr=limb(1, 90, 3), shinr=knee(6), legl=limb(-1, 96, 4), shinl=knee(72), footl=qs(('x', -14)), footr=qs(('x', -12)),
               armr=limb(1, -30, 14), forer=limb(1, 0), arml=limb(-1, -30, 14), forel=limb(-1, 0)),
    'happy': P(_face='happy', head=qs(('z', 8), ('x', -4)), armr=limb(1, 20, 96), forer=limb(1, 0, 50), arml=limb(-1, 20, 96), forel=limb(-1, 0, 50),
               legr=limb(1, 10), shinr=knee(30), legl=limb(-1, 0, 1)),
    # struck: rocked back, arms flung out
    'hurt': P(_face='surprised', body=qs(('x', -10)), head=qs(('x', -8), ('z', 6)), armr=limb(1, 26, 34), forer=limb(1, 30), arml=limb(-1, 26, 34), forel=limb(-1, 30),
              legr=limb(1, 14), shinr=knee(20), legl=limb(-1, -8), shinl=knee(6)),
    # fainted: on her back, the head tipped so the cap rests on the ground, one knee drawn up
    'tired': P(_face='blink', hips=qs(('x', -90)), head=qs(('x', 50)), skirtb=qs(('x', -6)),
               legr=limb(1, 6, 3), shinr=knee(4), legl=limb(-1, 34, 4), shinl=knee(60),
               armr=limb(1, 0, 40), forer=limb(1, 0, 20), arml=limb(-1, 10, 40), forel=limb(-1, 30)),
    # ROOTS: the hand raised high - then down on her knees, a hand plunged into the ground (roots burst up round the foe)
    'root_up': P(_face='fierce', body=qs(('x', -6), ('y', 8)), head=qs(('x', 12)), armr=limb(1, 40, 100), forer=limb(1, 0, 40), arml=limb(-1, 20, 34), forel=limb(-1, 24),
                 legr=limb(1, 6, 4), legl=limb(-1, 0, 4)),
    'root': P(_face='fierce', skirtb=qs(('x', 52)), body=qs(('x', 50)), head=qs(('x', -30)), armr=limb(1, 60, 6), forer=limb(1, 0), arml=limb(-1, 0, 30), forel=limb(-1, 10),
              legr=limb(1, -40, 4), shinr=knee(75), legl=limb(-1, -40, 4), shinl=knee(75), footr=knee(30), footl=knee(30)),
    # (holding them fast: both hands pressed to the earth)
    'root_hold': P(_face='fierce', skirtb=qs(('x', 52)), body=qs(('x', 50)), head=qs(('x', -32)), armr=limb(1, 54, 2, -6), forer=limb(1, 0), arml=limb(-1, 54, 2, -6), forel=limb(-1, 0),
                   legr=limb(1, -40, 4), shinr=knee(75), legl=limb(-1, -40, 4), shinl=knee(75), footr=knee(30), footl=knee(30)),
    # SPORES: a breath in, the cap tipped back - then a little bow, a puff of healing spores off the cap
    'spore_up': P(_face='surprised', body=qs(('x', -8)), head=qs(('x', -16)), armr=limb(1, -16, 26), forer=limb(1, 20), arml=limb(-1, -16, 26), forel=limb(-1, 20),
                  legr=limb(1, 0, 2), legl=limb(-1, 0, 2)),
    'spore': P(_face='blink', _glow=True, body=qs(('x', 14)), head=qs(('x', 20)), armr=limb(1, -30, 20), forer=limb(1, 10), arml=limb(-1, -30, 20), forel=limb(-1, 10),
               legr=limb(1, -8, 1), shinr=knee(12), legl=limb(-1, 4, 1)),
    # HEAL: hands cupped at her heart - then opened wide, every mushroom glowing
    'heal_up': P(_face='blink', _glow=True, head=qs(('x', 10)), armr=limb(1, 26, 8, -10), forer=limb(1, 96, -18), arml=limb(-1, 26, 8, -10), forel=limb(-1, 96, -18),
                 **STAND),
    'heal': P(_face='happy', _glow=True, head=qs(('x', -10)), body=qs(('x', -4)), armr=limb(1, 26, 74), forer=limb(1, 14), arml=limb(-1, 26, 74), forel=limb(-1, 14),
              **STAND),
    # SWIPE: the arm drawn up and back - then swept across
    'swipe_up': P(_face='fierce', body=qs(('y', 24)), head=qs(('y', -12)), armr=limb(1, 60, 86), forer=limb(1, 50), arml=limb(-1, 34, 22), forel=limb(-1, 40),
                  legr=limb(1, -14, 2), shinr=knee(16), legl=limb(-1, 18, 2)),
    'swipe': P(_face='fierce', body=qs(('y', -30), ('x', 8)), head=qs(('y', 18), ('x', -4)), armr=limb(1, 80, -4, -30), forer=limb(1, 6),
               arml=limb(-1, -24, 26), forel=limb(-1, 20), legr=limb(1, 24), shinr=knee(24), legl=limb(-1, -16), shinl=knee(16)),
    # BLOOM (charged): gathering low - then arms flung up and out, every mushroom on her flaring
    'bloom_up': P(_face='fierce', _glow=True, body=qs(('x', 14)), head=qs(('x', 10)), armr=limb(1, -24, 30), forer=limb(1, 30), arml=limb(-1, -24, 30), forel=limb(-1, 30),
                  legr=limb(1, 36, 4), shinr=knee(58), legl=limb(-1, 36, 4), shinl=knee(58)),
    'bloom': P(_face='happy', _glow=True, body=qs(('x', -6)), head=qs(('x', -14)), armr=limb(1, 30, 96), forer=limb(1, 0, 50), arml=limb(-1, 30, 96), forel=limb(-1, 0, 50),
               legr=limb(1, 0, 4), legl=limb(-1, 0, 4)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a little breaststroke, low in the water, the cap riding on top)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(hips=qs(('x', 70)), head=qs(('x', -56)),
                            armr=limb(1, 130 + 30 * s(_p), 30 + 30 * s(_p)), forer=limb(1, 20 + 20 * s(_p)),
                            arml=limb(-1, 130 + 30 * s(_p), 30 + 30 * s(_p)), forel=limb(-1, 20 + 20 * s(_p)),
                            legr=limb(1, -10 + 16 * s(2 * _p), 3), shinr=knee(30 + 20 * s(_p)), legl=limb(-1, -10 - 16 * s(2 * _p), 3), shinl=knee(30 + 20 * s(_p)))
    if _i in (3, 4): POSES[f'swim_{_i}']['_face'] = 'sleepy'


# ---- the skirt follows the thighs; the feet set flat (standing poses); then every pose grounded: the lowest point of her shoes -
#      or of her whole body, seated or lying - put on y=0
_GEO = {}


def _geo():
    if not _GEO:
        M = models()
        for p in PARTS: _GEO[p] = M[f'{PREFIX}{p}'][1]
    return _GEO


def _corners(e):
    (x0, y0, z0), (x1, y1, z1) = e['from'], e['to']
    pts = [(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]
    r = e.get('rotation')
    if not r: return pts
    o = r['origin']
    if 'axis' in r: ang = {'x': 0, 'y': 0, 'z': 0}; ang[r['axis']] = r['angle']
    else: ang = r
    q = qs(('z', ang.get('z', 0)), ('y', ang.get('y', 0)), ('x', ang.get('x', 0)))      # (Rz Ry Rx)
    return [tuple(o[i] + v for i, v in enumerate(qrot(q, tuple(p[i] - o[i] for i in range(3))))) for p in pts]


def world_points(pose, parts=None):
    """every element corner of the posed rig, in design units ({part: [(x, y, z)]})"""
    xf = solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        Q, t = xf[p]; pv = PIVOT[p]; W = tuple(t[i] + D(pv)[i] for i in range(3)); pts = []
        for e in _geo()[p]:
            for c in _corners(e):
                d = tuple(c[i] - 8 + pv[i] for i in range(3))                  # (model units -> design)
                r = qrot(Q, tuple(D(d)[i] - D(pv)[i] for i in range(3)))
                pts.append(D(tuple(W[i] + r[i] for i in range(3))))
        out[p] = pts
    return out


def _flat_feet(pose):
    pose = dict(pose)
    xf = solve(PIVOT, PARENT, pose)
    f = qrot(xf['hips'][0], (0.0, 0.0, 1.0)); yaw = qa('y', math.degrees(math.atan2(f[0], f[2])))
    for s_ in 'rl':
        if f'foot{s_}' in pose: continue                                     # (a foot the pose sets itself)
        Qs = xf[f'shin{s_}'][0]
        pose[f'foot{s_}'] = qmul((-Qs[0], -Qs[1], -Qs[2], Qs[3]), yaw)
    return pose


def _thigh(pose, s_):
    """how far forward (degrees) a thigh swings, in the hips' frame"""
    v = qrot(pose.get(f'leg{s_}', (0.0, 0.0, 0.0, 1.0)), (0.0, -1.0, 0.0))
    return math.degrees(math.atan2(v[2], -v[1]))


def _skirt(pose):
    """the skirt's front panel rides with the leading thigh, the back panel with the trailing one (unless the pose says)"""
    pose = dict(pose); a = [_thigh(pose, 'r'), _thigh(pose, 'l')]
    pose.setdefault('skirtf', qs(('x', -max(0.0, max(a)))))
    pose.setdefault('skirtb', qs(('x', -min(0.0, min(a)))))
    return pose


def _ground(pose, parts, lift=0.0):
    pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
    low = min(p[1] for pts in world_points(pose, parts).values() for p in pts)
    pose['_off'] = (o[0], round(lift - low, 3), o[2])
    return pose


_FEET = ('footr', 'footl', 'shinr', 'shinl')
for _k in list(POSES):
    _pz = POSES[_k] = _skirt(POSES[_k])
    if _k.startswith('swim_'):
        POSES[_k] = _ground(_pz, PARTS, -3.0)                                  # (low in the water: the waterline about her chest)
        continue
    if not (_k.startswith(('walk_', 'run_', 'sit_')) or _k in ('jump', 'tired')):
        _pz = _flat_feet(_pz)
    if _k.startswith('sit_') or _k == 'tired':
        POSES[_k] = _ground(_pz, PARTS)
    else:
        POSES[_k] = _ground(_pz, _FEET, {'jump': 3.0, 'happy': 0.8, 'run_1': 1.0, 'run_3': 1.0}.get(_k, 0.0))

DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'run_1', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired',
         'swim_0', 'swim_2', 'root_up', 'root', 'root_hold', 'spore_up', 'spore', 'heal_up', 'heal', 'swipe_up', 'swipe', 'bloom_up', 'bloom']
