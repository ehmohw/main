"""(draft) THE PALE DRYAD - a spirit of the Pale Garden, the eerie pale-oak woods (Wilfrey's Keep stands in pale gardens and
dark forests). Gentle, odd, sleepy and as old as the woods: a healer and a binder - roots that hold monsters fast, spores that
heal, mushrooms that glow. She glows softly at night: her small blue mushrooms, the faint spots on her orange ones and her eyes
give off a soft light (light_emission, moderate - never neon) while her bark stays unlit, so the glow reads as coming from the
mushrooms. (The night-only part - extra glow particles after dark - is wiring for later.)

The look, in the pack's blocky follower style: a dryad woman a little shorter than a player (her cap's crown tops out about
where a player's head does). Her body is pale-oak bark - grey-white, with darker grain running down it; her face is the same
bark worn smooth, with gentle glowing blue eyes and a few glowing freckles. Her hat and hair is one great BLUE mushroom cap with
ORANGE spots and orange gills underneath, a downturned rim, and a couple of tiny glowing mushrooms sprouting from its crown;
mycelium hangs from under it as pale, faintly blue strands (a fringe at the back, locks either side of her face). Clusters of
small blue (glowing) and orange mushrooms grow from her shoulders and the backs of her forearms, and orange shelf fungi and
blue caps climb her back. A bodice of moss, a moss sash at the waist, and a skirt of pale moss over pale-oak leaves with a
jagged leafy hem. Twig fingers; root feet, with roots splaying from the toes and heel.

The rig (rigkit): hips (the root: the sash), body (torso, bodice, back fungi; bends at the waist), head (a face per
expression; the cap, gills, hair and the eyes' glowing overlay on it), arms bent at the elbow, legs bent at the knee, root
feet. The skirt is carried in two halves by the thighs (each leg swings its own half, so a stride or a seat never pushes a leg
through it). Design units: feet at y=0, facing -z, her right is +x; RIG_SCALE 0.9 (about 1.73 blocks to the cap's crown).

Pose keys: _face (an expression), _glow (True: every mushroom flares - the healing and bloom poses; a '_lit' model per mushroomed
part), _off (the root's shift - worked out for every grounded pose so the lowest root-toe, or her seat, rests on y=0)."""
import math
import random
import sys
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, qa, qmul, qrot, el, seg, solve, D

PREFIX = 'pd_'
RIG_SCALE = 0.9
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
PIVOT = {'hips': (0, 12.5, 0), 'body': (0, 12.6, 0), 'head': (0, 20.9, 0.0),
         'armr': (4.45, 20.3, 0), 'forer': (4.45, 15.2, 0), 'arml': (-4.45, 20.3, 0), 'forel': (-4.45, 15.2, 0),
         'legr': (1.7, 12.5, 0), 'shinr': (1.7, 6.0, 0), 'footr': (1.7, 1.5, 0),
         'legl': (-1.7, 12.5, 0), 'shinl': (-1.7, 6.0, 0), 'footl': (-1.7, 1.5, 0)}
PARENT = {'hips': None, 'body': 'hips', 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': 'hips', 'shinr': 'legr', 'footr': 'shinr', 'legl': 'hips', 'shinl': 'legl', 'footl': 'shinl'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'sleepy', 'blink', 'fierce', 'surprised', 'sad')
GLOWS = ('head', 'body', 'armr', 'arml', 'forer', 'forel')         # (the parts with mushrooms: a '_lit' model each, for _glow)

# light_emission (0-15): a soft glow at rest, a flare when she heals or blooms
L_BLUE, L_SPOT, L_EYES, L_FLARE = 8, 4, 6, 15

# ---- colours
BARK, BARK_L, BARK_D, GRAIN, GRAIN_D = '#d8d3ca', '#e5e1d9', '#c6bfb4', '#a39b90', '#80786d'
SKIN, SKIN_D = '#e4e0d8', '#d4cec4'
MOSS, MOSS_D, MOSS_L = '#9aa688', '#7f8c6f', '#b4bea0'
LEAF, LEAF_D, LEAF_L = '#7f8b74', '#66725c', '#98a48a'
BLUE, BLUE_D, BLUE_L, BLUE_H = '#2a5fc4', '#1e4796', '#3c78dc', '#5f98ee'
ORANGE, ORANGE_D, ORANGE_L = '#ee7d1f', '#c05a12', '#ffa244'
STEM, STEM_D = '#eee8da', '#d5ccba'
GLOW, GLOW_L, GLOW_D = '#6fd6ff', '#c6f5ff', '#3aa6e6'
HAIR, HAIR_D, HAIR_B = '#ebeae2', '#d0d3cb', '#bfd9e3'
EYE, EYE_L, EYE_D, LASH = '#58d2ff', '#d2faff', '#2a8fd0', '#5a534b'


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


def _mottle(base, var, seed, p=0.25):
    return _cells(lambda x, y, r: r.choice(var) if r.random() < p else base, seed)


def _bark(seed, base=BARK, lines=4, light=(BARK_L, BARK_D)):
    """pale-oak bark: grey-white cells, darker grain lines running down it, wandering and broken, the odd knot"""
    rnd = random.Random(seed)
    g = [[base if rnd.random() > 0.25 else rnd.choice(light) for _ in range(32)] for _ in range(32)]
    for _ in range(lines):
        x, y = rnd.randrange(32), 0
        while y < 32:
            g[y][x % 32] = GRAIN if rnd.random() > 0.15 else GRAIN_D
            y += 1
            if rnd.random() < 0.18: x += rnd.choice((-1, 1))
            if rnd.random() < 0.07: y += rnd.randint(2, 4)
    for _ in range(2):                                                         # (knots)
        x, y = rnd.randrange(1, 31), rnd.randrange(1, 31)
        g[y][x] = GRAIN_D; g[y - 1][x] = GRAIN; g[y + 1][x] = GRAIN
    return _cells(lambda x, y, r: g[y][x], seed)


def _cap(seed, lit=False):
    """the great cap: blue, lighter in patches, with round orange spots (2-3 cells across, the corners off)"""
    base, var = (BLUE, (BLUE_D, BLUE_L)) if not lit else (BLUE_L, (BLUE, BLUE_H))
    rnd = random.Random(seed)
    g = [[base if rnd.random() > 0.3 else rnd.choice(var) for _ in range(32)] for _ in range(32)]
    spots = []
    while len(spots) < 11:                                                    # (well apart, so each reads as a spot)
        x, y, s = rnd.randrange(32), rnd.randrange(32), rnd.choice((3, 4, 4))
        if all(min(abs(x - a), 32 - abs(x - a)) + min(abs(y - b), 32 - abs(y - b)) > 9 for a, b, _ in spots): spots.append((x, y, s))
    for x, y, s in spots:
        for dy in range(s):
            for dx in range(s):
                if dx in (0, s - 1) and dy in (0, s - 1): continue          # (the corners off: round-ish)
                hi = dx <= 1 and dy <= 1 and not (dx == 0 or dy == 0) or (s == 3 and dx == 1 and dy == 1)
                g[(y + dy) % 32][(x + dx) % 32] = (ORANGE_L if hi else ORANGE) if not lit else ('#ffe39a' if hi else '#ffc35a')
            g[(y + s - 1) % 32][(x + 1) % 32] = ORANGE_D if not lit else '#ffb24e'
    return _cells(lambda x, y, r: g[y][x], seed)


def _gills(lit=False):
    """orange gills: darker lines every other cell (they run in toward the stem)"""
    a, b, c = (ORANGE, ORANGE_D, ORANGE_L) if not lit else ('#ffb24e', '#e88a22', '#ffd890')
    return _cells(lambda x, y, r: b if x % 2 == 0 else (c if r.random() < 0.2 else a), 4410)


def _hair():
    """mycelium: pale strands, faintly blue, a darker line between them"""
    return _cells(lambda x, y, r: HAIR_D if x % 3 == 0 else (HAIR_B if r.random() < 0.22 else HAIR), 4420)


def _leaves():
    """pale-oak leaves: overlapping dull grey-green leaves, each a lighter top and a darker lower edge"""
    def c(x, y, r):
        k = (y + (x // 3) * 2) % 4
        if k == 3: return LEAF_D
        if k == 0: return LEAF_L if r.random() < 0.6 else LEAF
        return LEAF if r.random() > 0.15 else LEAF_D
    return _cells(c, 4430)


def _face(kind=None):
    """the face: 6 x 6 units (24 x 24 px from the top-left; the cap's gills hide rows 0-6). Smooth pale bark, a whisper of grain
    at the edges, the brows and mouth (the eyes are their own glowing overlay, _eyes). Her right eye is our left: cols 4-8,
    her left cols 15-19; the eyes on rows 13-16, the mouth round row 20."""
    rnd = random.Random(4440)
    im = _cells(lambda x, y, r: SKIN if r.random() > 0.18 else SKIN_D, 4441)
    d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=hexc(c))
    for x in (0, 1, 22, 23):                                                  # (grain at the temples)
        for y in range(6, 24):
            if rnd.random() < 0.35: R(x, y, x, y, GRAIN)
    R(11, 17, 12, 17, SKIN_D); R(11, 18, 12, 18, BARK_D)                     # (a knot of a nose)
    if kind == 'fierce':                                                      # brows: down hard toward the middle
        for i in range(5):
            R(4 + i, 10 + i // 2, 4 + i, 11 + i // 2, GRAIN_D); R(19 - i, 10 + i // 2, 19 - i, 11 + i // 2, GRAIN_D)
    elif kind == 'sad':                                                       # (up in the middle)
        for i in range(5):
            R(4 + i, 12 - i // 2, 4 + i, 12 - i // 2, GRAIN); R(19 - i, 12 - i // 2, 19 - i, 12 - i // 2, GRAIN)
    elif kind == 'surprised':
        R(4, 9, 8, 9, GRAIN); R(15, 9, 19, 9, GRAIN)
    elif kind in ('sleepy', 'blink'):
        R(4, 12, 8, 12, GRAIN); R(15, 12, 19, 12, GRAIN)
    else:
        R(5, 11, 8, 11, GRAIN); R(15, 11, 18, 11, GRAIN); R(4, 12, 4, 12, GRAIN); R(19, 12, 19, 12, GRAIN)
    M = '#7a5a52'                                                             # (the mouth: a dark rosy brown)
    if kind == 'happy':
        R(9, 20, 9, 20, M); R(10, 21, 13, 21, M); R(14, 20, 14, 20, M)
    elif kind == 'surprised':
        R(10, 20, 13, 22, M); R(11, 21, 12, 21, '#4a3632')
    elif kind == 'sad':
        R(10, 21, 13, 21, M); R(9, 22, 9, 22, M); R(14, 22, 14, 22, M)
    elif kind == 'fierce':
        R(9, 21, 14, 21, M); R(9, 20, 9, 20, M); R(14, 20, 14, 20, M)
    elif kind == 'sleepy':
        R(11, 21, 12, 21, M)
    else:                                                                     # (a soft little smile)
        R(10, 21, 13, 21, M); R(9, 20, 9, 20, M); R(14, 20, 14, 20, M)
    return im


def _eyes(kind=None):
    """the eyes' overlay (transparent but for the eyes, lashes and freckles; light_emission on its element): glowing blue"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=hexc(c))
    for x0 in (4, 15):
        m = x0 == 4                                                           # (her right eye: the glint on its outer side)
        if kind == 'blink':                                                   # (shut: a soft downward curve of lashes)
            R(x0, 14, x0, 14, LASH); R(x0 + 1, 15, x0 + 3, 15, LASH); R(x0 + 4, 14, x0 + 4, 14, LASH)
        elif kind == 'happy':                                                 # (smiling arches)
            R(x0, 15, x0, 15, EYE_D); R(x0 + 1, 14, x0 + 3, 14, EYE); R(x0 + 4, 15, x0 + 4, 15, EYE_D); R(x0 + 2, 14, x0 + 2, 14, EYE_L)
            R(x0 + 1, 13, x0 + 3, 13, LASH)
        elif kind == 'sleepy':                                                # (heavy lids: the lower half glows)
            R(x0, 14, x0 + 4, 14, LASH); R(x0, 15, x0 + 4, 15, EYE); R(x0 + 1, 16, x0 + 3, 16, EYE_D); R(x0 + 2, 15, x0 + 2, 15, EYE_L)
        elif kind == 'fierce':                                                # (narrowed, brighter)
            R(x0, 14, x0 + 4, 15, EYE); R(x0 + 1, 14, x0 + 3, 14, EYE_L)
            if m: R(x0 + 3, 13, x0 + 4, 13, LASH)
            else: R(x0, 13, x0 + 1, 13, LASH)
        elif kind == 'surprised':                                             # (wide and round)
            R(x0 + 1, 12, x0 + 3, 12, EYE_D); R(x0, 13, x0 + 4, 16, EYE); R(x0 + 1, 17, x0 + 3, 17, EYE_D)
            R(x0 + 1, 14, x0 + 3, 15, EYE_L); R(x0 + 2, 14, x0 + 2, 15, '#ffffff')
        else:                                                                 # default / sad: a soft almond, lash on top, a glint
            R(x0, 13, x0 + 4, 13, LASH); R(x0, 14, x0 + 4, 15, EYE); R(x0 + 1, 16, x0 + 3, 16, EYE_D)
            R(x0 + 1, 14, x0 + 3, 14, EYE_L); R(x0 + (1 if m else 3), 14, x0 + (1 if m else 3), 14, '#ffffff')
            if kind == 'sad':                                                 # (the outer corners droop; a glowing tear)
                R(x0 + (0 if m else 4), 16, x0 + (0 if m else 4), 16, EYE_D)
                if not m: R(x0 + 3, 18, x0 + 3, 19, GLOW)
    for x, y in ((3, 18), (5, 19), (2, 19), (20, 18), (18, 19), (21, 19)):     # (glowing freckles on her cheeks)
        R(x, y, x, y, GLOW_D)
    return im


def textures():
    T = {'pd_bark': _bark(4401), 'pd_bark2': _bark(4402, lines=9), 'pd_barkl': _bark(4403, base=BARK_L, lines=5),
         'pd_moss': _mottle(MOSS, (MOSS_D, MOSS_L), 4404), 'pd_leaf': _leaves(),
         'pd_cap': _cap(4405), 'pd_cap_lit': _cap(4405, True), 'pd_gill': _gills(), 'pd_gill_lit': _gills(True),
         'pd_hair': _hair(), 'pd_stem': _mottle(STEM, (STEM_D,), 4406, 0.2),
         'pd_mblue': _mottle(GLOW_D, (GLOW, BLUE_L), 4407, 0.35), 'pd_mblue_lit': _mottle(GLOW_L, (GLOW, '#ffffff'), 4408, 0.35),
         'pd_morange': _mottle(ORANGE, (ORANGE_D, ORANGE_L), 4409, 0.3), 'pd_morange_lit': _mottle('#ffb24e', ('#ffd890', ORANGE_L), 4411, 0.3),
         'pd_mspot': _mottle('#ffe6a8', ('#fff4d0',), 4412, 0.3), 'pd_mspot_lit': _mottle('#fff6dc', ('#ffffff',), 4413, 0.3),
         'pd_root': _bark(4414, base=BARK_D, lines=10, light=(BARK, GRAIN)),
         'pd_face': _face(), 'pd_eyes': _eyes()}
    for k in FACES:
        T[f'pd_face_{k}'] = _face(k); T[f'pd_eyes_{k}'] = _eyes(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def B(sx, x0, x1, y0, y1, z0, z1, tex, piv, **kw):
    """a box on one side (sx = 1 her right, -1 her left: x mirrored)"""
    a, b = sorted((sx * x0, sx * x1))
    return el((a, y0, z0), (b, y1, z1), tex, piv, **kw)


def mush(A, d, piv, kind='blue', lit=False, size=1.0, up=(0.0, 1.0, 0.0)):
    """a small mushroom growing from A along d (design units: its length). Blue ones glow; orange ones carry a faint glowing
    spot on top. lit: the flare (_glow) - all of it bright and at full light"""
    L = math.sqrt(sum(v * v for v in d)); u = tuple(v / L for v in d)
    Bt = tuple(A[i] + d[i] for i in range(3))
    tip = tuple(Bt[i] + u[i] * 0.55 * size for i in range(3))
    cw = 1.8 * size
    sfx = '_lit' if lit else ''
    lc = (L_FLARE if lit else L_BLUE) if kind == 'blue' else (L_FLARE if lit else 0)
    out = [seg(A, Bt, 0.6 * size, 0.6 * size, 'pd_stem', piv, up=up),
           seg(tuple(Bt[i] - u[i] * 0.15 * size for i in range(3)), tip, cw, cw, f'pd_m{kind}{sfx}', piv, up=up, light=lc),
           seg(tip, tuple(tip[i] + u[i] * 0.35 * size for i in range(3)), cw * 0.6, cw * 0.6, f'pd_m{kind}{sfx}', piv, up=up, light=lc)]
    if kind == 'orange':                                                       # (the glowing spot on its crown)
        top = tuple(tip[i] + u[i] * 0.35 * size for i in range(3))
        out.append(seg(top, tuple(top[i] + u[i] * 0.06 for i in range(3)), cw * 0.34, cw * 0.34, f'pd_mspot{sfx}', piv, up=up,
                       light=L_FLARE if lit else L_SPOT))
    return out


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the hips: the moss sash, knotted at her left hip, its ends hanging
    pv = PIVOT['hips']
    part('pd_hips', [el((-3.3, 11.0, -2.45), (3.3, 13.4, 2.45), 'pd_moss', pv, shift=(0.2, 0.4)),
                     el((-3.0, 12.6, -2.5), (3.0, 13.0, 2.5), 'pd_leaf', pv, shift=(0.5, 0.2)),               # (a band of leaves)
                     el((-3.48, 11.6, -1.0), (-3.3, 13.0, 0.4), 'pd_moss', pv, shift=(0.6, 0.1)),             # (the knot)
                     el((-3.46, 10.0, -0.6), (-3.3, 11.6, 0.0), 'pd_leaf', pv)])

    # ---- the body: waist, chest (bark), the moss bodice, a leaf collar, the neck; fungi up her back
    pv = PIVOT['body']

    def body(lit):
        b = [el((-2.75, 12.6, -1.6), (2.75, 15.4, 1.6), 'pd_bark', pv, shift=(0.1, 0.5)),                  # waist
             el((-3.25, 15.2, -1.75), (3.25, 20.9, 1.75), 'pd_bark2', pv, shift=(0.3, 0.2)),                # chest
             el((-3.3, 17.2, -2.15), (3.3, 19.9, 1.85), 'pd_moss', pv, shift=(0.4, 0.3)),                 # the bodice
             el((-2.0, 16.6, -2.1), (2.0, 17.2, -1.75), 'pd_moss', pv, shift=(0.7, 0.6)),
             el((-1.2, 20.9, -1.1), (1.2, 21.3, 1.1), 'pd_barkl', pv),                                      # neck
             # the leaf collar over the shoulders
             el((-3.2, 20.6, -1.9), (3.2, 21.2, -1.2), 'pd_leaf', pv, shift=(0.2, 0.1)),
             el((-3.2, 20.6, 1.2), (3.2, 21.2, 1.9), 'pd_leaf', pv, shift=(0.5, 0.3))]
        # fungi up her back: orange shelves low, blue caps by the shoulder blades
        for (x0, x1, y, w) in ((-1.9, 0.3, 13.6, 1.4), (-0.3, 2.1, 15.6, 1.3), (-1.6, 0.2, 17.6, 1.1)):
            b += [el((x0, y, 1.6 if y < 15 else 1.75), (x1, y + 0.55, 1.6 + w + (0 if y < 15 else 0.15)), 'pd_morange' + ('_lit' if lit else ''), pv,
                     light=L_FLARE if lit else 0),
                  el(((x0 + x1) / 2 - 0.25, y + 0.55, 1.9 + w * 0.4), ((x0 + x1) / 2 + 0.25, y + 0.6, 2.4 + w * 0.4), 'pd_mspot' + ('_lit' if lit else ''), pv,
                     light=L_FLARE if lit else L_SPOT)]
        b += mush((1.2, 18.6, 1.75), (0.3, 0.7, 1.0), pv, 'blue', lit, 0.9)
        b += mush((0.3, 19.8, 1.75), (-0.2, 0.4, 1.0), pv, 'blue', lit, 0.7)
        b += mush((-1.0, 15.0, 1.6), (-0.4, 0.5, 0.9), pv, 'blue', lit, 0.65)
        return b
    part('pd_body', body(False)); part('pd_body_lit', body(True))

    # ---- the head: smooth bark, the face, the eyes' glow; the great cap (stepped, a downturned rim), gills; mycelium hair
    pv = PIVOT['head']

    def head(face=None, lit=False):
        ft, et = ('pd_face', 'pd_eyes') if face is None else (f'pd_face_{face}', f'pd_eyes_{face}')
        cp, gl = ('pd_cap_lit', 'pd_gill_lit') if lit else ('pd_cap', 'pd_gill')
        h = [el((-3.0, 21.0, -3.0), (3.0, 27.0, 3.0), 'pd_barkl', pv, faces=('south', 'east', 'west', 'up', 'down'), shift=(0.3, 0.6)),
             el((-3.0, 21.0, -3.02), (3.0, 27.0, -3.0), ft, pv, faces=('north',), uv={'north': [0, 0, 6, 6]}),
             el((-3.0, 21.0, -3.06), (3.0, 27.0, -3.04), et, pv, faces=('north',), uv={'north': [0, 0, 6, 6]}, light=L_FLARE if lit else L_EYES),
             # the cap: gills under the brim, the brim, two steps up and the crown
             el((-6.0, 25.2, -5.7), (6.0, 25.6, 5.7), gl, pv, shift=(0.1, 0.1)),
             el((-6.5, 25.6, -6.2), (6.5, 26.8, 6.2), cp, pv, shift=(0.0, 0.2)),
             el((-5.3, 26.8, -5.0), (5.3, 28.6, 5.0), cp, pv, shift=(0.4, 0.5)),
             el((-3.9, 28.6, -3.7), (3.9, 30.0, 3.7), cp, pv, shift=(0.7, 0.1)),
             el((-2.3, 30.0, -2.1), (2.3, 30.8, 2.1), cp, pv, shift=(0.2, 0.8)),
             # the downturned rim (blue outside; its inside shows the gills' orange)
             el((-6.5, 24.8, -6.2), (6.5, 25.6, -5.7), cp, pv, shift=(0.5, 0.3)),
             el((-6.5, 24.8, 5.7), (6.5, 25.6, 6.2), cp, pv, shift=(0.3, 0.9)),
             el((-6.5, 24.8, -5.7), (-6.0, 25.6, 5.7), cp, pv, shift=(0.8, 0.4)),
             el((6.0, 24.8, -5.7), (6.5, 25.6, 5.7), cp, pv, shift=(0.6, 0.7))]
        # mycelium hair: a fringe at the back and sides under the cap, strands of uneven length; locks beside her face
        h += [el((-3.4, 22.6, 3.0), (3.4, 25.2, 3.5), 'pd_hair', pv),
              el((-3.4, 22.6, -2.6), (-3.0, 25.2, 3.0), 'pd_hair', pv, shift=(0.3, 0.0)),
              el((3.0, 22.6, -2.6), (3.4, 25.2, 3.0), 'pd_hair', pv, shift=(0.6, 0.0))]
        rnd = random.Random(4450)
        for i in range(7):                                                     # (back strands)
            x = -3.4 + i * 6.8 / 7
            h.append(el((x + 0.05, 22.6 - rnd.choice((0.6, 1.0, 1.2, 0.8)), 3.05), (x + 6.8 / 7 - 0.1, 22.6, 3.45), 'pd_hair', pv, shift=(0.1 * i, 0.3)))
        for sx in (-1, 1):
            for i, ln in enumerate((1.4, 0.8, 1.1, 0.6, 1.2)):                 # (side strands)
                z = -2.6 + i * 5.6 / 5
                h.append(B(sx, 3.02, 3.38, 22.6 - ln, 22.6, z + 0.05, z + 5.6 / 5 - 0.1, 'pd_hair', pv, shift=(0.2 * i, 0.5)))
            h.append(B(sx, 2.5, 3.4, 20.7, 25.2, -3.35, -3.05, 'pd_hair', pv, shift=(0.5, 0.2)))  # (a lock framing her face)
            h.append(B(sx, 2.75, 3.25, 20.1, 20.7, -3.32, -3.08, 'pd_hair', pv, shift=(0.1, 0.7)))
        # tiny glowing mushrooms sprouting from the crown
        h += mush((1.6, 30.0, -0.9), (0.2, 0.9, -0.1), pv, 'blue', lit, 0.55)
        h += mush((-0.9, 30.8, 0.6), (-0.15, 0.7, 0.1), pv, 'blue', lit, 0.45)
        h += mush((-3.0, 28.6, -1.6), (-0.4, 0.8, -0.2), pv, 'orange', lit, 0.5)
        return h
    for lit in (False, True):
        s = '_lit' if lit else ''
        part(f'pd_head{s}', head(None, lit))
        for fc in FACES:
            part(f'pd_head_x{fc}{s}', head(fc, lit))

    # ---- arms: bark, mushrooms on the outer side of the shoulder and the back of the forearm; twig fingers
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']
        X = ap[0]

        def arm(lit):
            a = [B(sx, 3.55, 5.35, 15.2, 20.9, -0.95, 0.95, 'pd_bark', ap, shift=(0.4 + 0.2 * sx, 0.5)),
                 B(sx, 3.5, 5.4, 19.6, 20.95, -1.0, 1.0, 'pd_leaf', ap, shift=(0.2, 0.6))]          # (leaves over the shoulder)
            a += mush((X + sx * 0.9, 20.0, -0.3), (sx * 1.25, 0.65, -0.1), ap, 'blue', lit, 1.15)
            a += mush((X + sx * 0.9, 18.8, 0.45), (sx * 1.2, 0.6, 0.25), ap, 'orange', lit, 0.95)
            a += mush((X + sx * 0.9, 17.6, -0.5), (sx * 0.9, 0.35, -0.35), ap, 'blue', lit, 0.75)
            return a

        def fore(lit):
            f = [B(sx, 3.6, 5.3, 10.9, 15.25, -0.9, 0.9, 'pd_bark2', fp, shift=(0.6, 0.3 + 0.2 * sx)),
                 B(sx, 3.62, 5.28, 9.8, 10.9, -0.95, 0.85, 'pd_barkl', fp, shift=(0.3, 0.1))]            # the hand
            for i, z in enumerate((-0.7, -0.05, 0.6)):                                                    # twig fingers
                f.append(B(sx, 3.85 + 0.15 * i, 4.3 + 0.15 * i, 9.0 + 0.2 * (i == 1) - 0.2, 9.8, z - 0.2, z + 0.2, 'pd_root', fp, shift=(0.1 * i, 0.4)))
            f.append(B(sx, 3.3, 3.62, 9.6, 10.6, -0.9, -0.4, 'pd_root', fp))                              # (the thumb)
            f += mush((X + sx * 0.6, 13.6, 0.9), (sx * 0.5, 0.4, 1.0), fp, 'orange', lit, 0.6)          # (on the back of the forearm)
            f += mush((X + sx * 0.9, 12.6, 0.3), (sx * 1.0, 0.4, 0.3), fp, 'blue', lit, 0.6)
            return f
        part(f'pd_arm{s}', arm(False)); part(f'pd_arm{s}_lit', arm(True))
        part(f'pd_fore{s}', fore(False)); part(f'pd_fore{s}_lit', fore(True))

        # ---- legs: the thigh (bark) carrying her half of the skirt - pale moss over pale-oak leaves, a jagged leafy hem
        lp, kp, fp2 = PIVOT[f'leg{s}'], PIVOT[f'shin{s}'], PIVOT[f'foot{s}']
        sk = [B(sx, 0.6, 2.8, 6.0, 10.6, -1.1, 1.1, 'pd_bark', lp),
              B(sx, 0.04, 3.25, 9.4, 11.0, -2.3, 2.3, 'pd_moss', lp, shift=(0.3 + 0.3 * sx, 0.2)),
              B(sx, 0.04, 3.75, 5.9, 9.4, -2.7, 0.6, 'pd_leaf', lp, shift=(0.1, 0.3 + 0.2 * sx)),
              B(sx, 0.04, 3.75, 6.9, 9.4, 0.6, 2.7, 'pd_leaf', lp, shift=(0.6, 0.3)),             # (a little shorter behind: room for a bent knee)
              B(sx, 0.04, 3.32, 9.2, 9.6, -2.36, 2.36, 'pd_leaf', lp, shift=(0.5, 0.1))]
        for i in range(4):                                                     # (the hem: leaf tips at the front and side - none at
            x0 = 0.15 + i * 0.9                                                #  the back, so a knee bent hard never meets them)
            sk.append(B(sx, x0, x0 + 0.6, 5.0 + 0.4 * (i % 2), 5.9, -2.7, -2.0, 'pd_leaf', lp, shift=(0.2 * i, 0.7)))
        for z in (-2.2, -1.0, 0.2):
            sk.append(B(sx, 3.05, 3.75, 5.0 + 0.4 * (z > -1 and z < 0), 5.9, z, z + 0.8, 'pd_leaf', lp, shift=(0.4, 0.8)))
        part(f'pd_leg{s}', sk)
        part(f'pd_shin{s}', [B(sx, 0.7, 2.7, 1.4, 6.1, -1.0, 1.0, 'pd_bark2', kp, shift=(0.5, 0.1 + 0.3 * sx)),
                             B(sx, 0.62, 2.78, 3.2, 3.8, -1.08, 1.08, 'pd_root', kp),                      # (a root wound round)
                             B(sx, 0.62, 2.78, 4.4, 4.8, -1.08, 1.08, 'pd_root', kp, shift=(0.5, 0.5))])
        # ---- the root foot: a broad base, roots splaying from the toes and the heel (from the ankle, so a pose sets it flat)
        X = abs(fp2[0])
        ft = [B(sx, 0.35, 3.05, 0.0, 1.5, -2.2, 1.3, 'pd_root', fp2),
              B(sx, 0.7, 2.7, 1.4, 1.9, -1.0, 1.0, 'pd_root', fp2, shift=(0.3, 0.3))]
        for dx, dz, w in ((-0.75, -0.1, 0.5), (0.0, 0.25, 0.6), (0.8, 0.7, 0.55)):    # (three toes, splayed)
            x0 = sx * (X + dx * 1.0)
            ft.append(seg((x0, 0.5, -2.0), (x0 + sx * dz * 1.4, 0.25, -3.6), w, 0.5, 'pd_root', fp2))
        ft.append(seg((sx * (X + 1.1), 0.4, 0.3), (sx * (X + 2.0), 0.25, 0.9), 0.5, 0.45, 'pd_root', fp2))   # (one out to the side)
        ft.append(seg((sx * X, 0.4, 1.2), (sx * (X - 0.3), 0.25, 2.4), 0.55, 0.5, 'pd_root', fp2))            # (and the heel's)
        part(f'pd_foot{s}', ft)
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
REST = dict(armr=limb(1, 4, 7), forer=limb(1, 14), arml=limb(-1, 4, 7), forel=limb(-1, 14))
STAND = dict(legr=limb(1, 0, 2), legl=limb(-1, 0, 2))
POSES = {
    # serene: a gentle tilt of the head, arms soft at her sides
    'idle_a': P(**REST, **STAND, head=qs(('z', 5))),
    # sleepy: the head drooping to one side, a little sway, arms hanging loose
    'idle_b': P(_face='sleepy', body=qs(('z', 3), ('x', 3)), head=qs(('z', -11), ('x', 9)),
                armr=limb(1, 0, 5), forer=limb(1, 6), arml=limb(-1, 0, 5), forel=limb(-1, 6), legr=limb(1, 4, 2), shinr=knee(8), legl=limb(-1, -2, 2)),
    # a glowing mushroom cupped in her right palm, admired
    'idle_c': P(_face='happy', head=qs(('x', 20), ('y', -10)), armr=limb(1, 26, 4, -10), forer=limb(1, 62), arml=limb(-1, 2, 7), forel=limb(-1, 12), **STAND),
    **{f'walk_{k}': P(head=qs(('z', 3 * s(math.pi * k / 2))), body=qs(('y', -4 * s(math.pi * k / 2))),
                      legr=limb(1, 22 * s(math.pi * k / 2)), shinr=knee(34 * max(0.0, -s(math.pi * k / 2)) + 6),
                      legl=limb(-1, -22 * s(math.pi * k / 2)), shinl=knee(34 * max(0.0, s(math.pi * k / 2)) + 6),
                      armr=limb(1, -18 * s(math.pi * k / 2), 7), forer=limb(1, 16), arml=limb(-1, 18 * s(math.pi * k / 2), 7), forel=limb(-1, 16))
       for k in range(4)},
    **{f'run_{k}': P(body=qs(('x', 12)), head=qs(('x', -10)),
                     legr=limb(1, (40, 8, -30, 8)[k]), shinr=knee((14, 70, 40, 20)[k]), legl=limb(-1, (-30, 8, 40, 8)[k]), shinl=knee((40, 20, 14, 70)[k]),
                     armr=limb(1, (-30, 0, 34, 0)[k], 9), forer=limb(1, 60), arml=limb(-1, (34, 0, -30, 0)[k], 9), forel=limb(-1, 60))
       for k in range(4)},
    'jump': P(_face='happy', legr=limb(1, 40), shinr=knee(70), legl=limb(-1, 14), shinl=knee(40),
              armr=limb(1, 10, 62), forer=limb(1, 20), arml=limb(-1, 10, 62), forel=limb(-1, 20), head=qs(('x', -8))),
    # sitting on the ground, legs out before her, hands resting on her lap
    'sit_a': P(body=qs(('x', -4)), head=qs(('z', 5)), legr=limb(1, 84, 4), shinr=knee(10), legl=limb(-1, 84, 4), shinl=knee(10),
               footr=qs(('x', -10)), footl=qs(('x', -10)),
               armr=limb(1, 28, 6, -16), forer=limb(1, 46), arml=limb(-1, 28, 6, -16), forel=limb(-1, 46)),
    # (the seated idle's other beat) leaning back on her hands, one knee up, nodding off
    'sit_b': P(_face='sleepy', body=qs(('x', -22)), head=qs(('z', -12), ('x', 10)),
               legr=limb(1, 92, 4), shinr=knee(6), legl=limb(-1, 100, 2), shinl=knee(80), footl=qs(('x', -14)), footr=qs(('x', -12)),
               armr=limb(1, -26, 16), forer=limb(1, 0), arml=limb(-1, -26, 16), forel=limb(-1, 0)),
    'happy': P(_face='happy', head=qs(('z', 8), ('x', -6)), armr=limb(1, 130, 46), forer=limb(1, 0, 10), arml=limb(-1, 130, 46), forel=limb(-1, 0, 10),
               legr=limb(1, 10), shinr=knee(30), legl=limb(-1, 0, 2)),
    # struck: rocked back, arms flung out
    'hurt': P(_face='surprised', body=qs(('x', -12)), head=qs(('x', -10), ('z', 6)), armr=limb(1, 26, 34), forer=limb(1, 30), arml=limb(-1, 26, 34), forel=limb(-1, 30),
              legr=limb(1, 16), shinr=knee(20), legl=limb(-1, -10), shinl=knee(6)),
    # fainted: lying on her side, curled a little, the cap's rim on the ground under her cheek
    'tired': P(_face='blink', hips=qs(('x', -90)), head=qs(('x', 62), ('z', 10)),
               legr=limb(1, 6, 4), shinr=knee(4), legl=limb(-1, 30, 6), shinl=knee(56),
               armr=limb(1, 0, 64), forer=limb(1, 0, 20), arml=limb(-1, 10, 40), forel=limb(-1, 30)),
    # ROOTS: the hand raised high - then down on her knees, the hand plunged into the ground (roots burst up round the foe)
    'root_up': P(_face='fierce', body=qs(('x', -6), ('y', 8)), head=qs(('x', 16)), armr=limb(1, 150, 42), forer=limb(1, 16), arml=limb(-1, 20, 36), forel=limb(-1, 24),
                 legr=limb(1, 6, 8), legl=limb(-1, 0, 8)),
    'root': P(_face='fierce', body=qs(('x', 50)), head=qs(('x', -26)), armr=limb(1, 65, 6), forer=limb(1, 0), arml=limb(-1, 0, 30), forel=limb(-1, 10),
              legr=limb(1, -40, 8), shinr=knee(75), legl=limb(-1, -40, 8), shinl=knee(75), footr=knee(30), footl=knee(30)),
    # (holding them fast: both hands pressed to the earth)
    'root_hold': P(_face='fierce', body=qs(('x', 50)), head=qs(('x', -30)), armr=limb(1, 58, 2, -6), forer=limb(1, 0), arml=limb(-1, 58, 2, -6), forel=limb(-1, 0),
                   legr=limb(1, -40, 8), shinr=knee(75), legl=limb(-1, -40, 8), shinl=knee(75), footr=knee(30), footl=knee(30)),
    # SPORES: a breath in, the cap tipped back - then a deep bow, a puff of healing spores off the cap
    'spore_up': P(_face='surprised', body=qs(('x', -8)), head=qs(('x', -20)), armr=limb(1, -16, 24), forer=limb(1, 20), arml=limb(-1, -16, 24), forel=limb(-1, 20),
                  legr=limb(1, 0, 3), legl=limb(-1, 0, 3)),
    'spore': P(_face='blink', _glow=True, body=qs(('x', 16)), head=qs(('x', 24)), armr=limb(1, -34, 20), forer=limb(1, 10), arml=limb(-1, -34, 20), forel=limb(-1, 10),
               legr=limb(1, -8, 2), shinr=knee(12), legl=limb(-1, 4, 2)),
    # HEAL: hands cupped at her heart - then opened wide, every mushroom glowing
    'heal_up': P(_face='blink', _glow=True, head=qs(('x', 12)), armr=limb(1, 30, 8, -14), forer=limb(1, 100, -14), arml=limb(-1, 30, 8, -14), forel=limb(-1, 100, -14),
                 **STAND),
    'heal': P(_face='happy', _glow=True, head=qs(('x', -12)), body=qs(('x', -4)), armr=limb(1, 26, 70), forer=limb(1, 16), arml=limb(-1, 26, 70), forel=limb(-1, 16),
              **STAND),
    # SWIPE: the bark arm drawn up and back - then raked across
    'swipe_up': P(_face='fierce', body=qs(('y', 24)), head=qs(('y', -14)), armr=limb(1, 128, 40), forer=limb(1, 36), arml=limb(-1, 34, 22), forel=limb(-1, 40),
                  legr=limb(1, -14, 4), shinr=knee(16), legl=limb(-1, 18, 4)),
    'swipe': P(_face='fierce', body=qs(('y', -30), ('x', 10)), head=qs(('y', 18), ('x', -6)), armr=limb(1, 82, -4, -30), forer=limb(1, 6),
               arml=limb(-1, -24, 26), forel=limb(-1, 20), legr=limb(1, 26), shinr=knee(26), legl=limb(-1, -16), shinl=knee(18)),
    # BLOOM (charged): gathering low, then arms flung up and out - every mushroom on her flaring
    'bloom_up': P(_face='fierce', _glow=True, body=qs(('x', 16)), head=qs(('x', 12)), armr=limb(1, -26, 30), forer=limb(1, 30), arml=limb(-1, -26, 30), forel=limb(-1, 30),
                  legr=limb(1, 40, 8), shinr=knee(64), legl=limb(-1, 40, 8), shinl=knee(64)),
    'bloom': P(_face='happy', _glow=True, body=qs(('x', -6)), head=qs(('x', -18)), armr=limb(1, 140, 44), forer=limb(1, 0, 12), arml=limb(-1, 140, 44), forel=limb(-1, 0, 12),
               legr=limb(1, 0, 6), legl=limb(-1, 0, 6)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a slow breaststroke, low in the water, the cap riding on top)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='sleepy' if _i in (3, 4) else None, hips=qs(('x', 72)), head=qs(('x', -58)),
                            armr=limb(1, 140 + 30 * s(_p), 30 + 30 * s(_p)), forer=limb(1, 20 + 20 * s(_p)),
                            arml=limb(-1, 140 + 30 * s(_p), 30 + 30 * s(_p)), forel=limb(-1, 20 + 20 * s(_p)),
                            legr=limb(1, -10 + 16 * s(2 * _p), 6), shinr=knee(30 + 20 * s(_p)), legl=limb(-1, -10 - 16 * s(2 * _p), 6), shinl=knee(30 + 20 * s(_p)))
    if POSES[f'swim_{_i}']['_face'] is None: del POSES[f'swim_{_i}']['_face']


# ---- ground every pose: the feet set flat (standing poses), then the lowest point of the feet - or of her whole body, seated
#      or lying - put on y=0
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


def _ground(pose, parts, lift=0.0):
    pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
    low = min(p[1] for pts in world_points(pose, parts).values() for p in pts)
    pose['_off'] = (o[0], round(lift - low, 3), o[2])
    return pose


_FEET = ('footr', 'footl', 'shinr', 'shinl')
for _k in list(POSES):
    _pz = POSES[_k]
    if _k.startswith('swim_'):
        POSES[_k] = _ground(_pz, PARTS, -4.0)                                  # (low in the water: the waterline about her shoulders)
        continue
    if not (_k.startswith(('walk_', 'run_', 'sit_')) or _k in ('jump', 'tired') ):
        _pz = _flat_feet(_pz)
    if _k.startswith('sit_') or _k == 'tired':
        POSES[_k] = _ground(_pz, PARTS)
    else:
        POSES[_k] = _ground(_pz, _FEET, {'jump': 4.0, 'happy': 1.0, 'run_1': 1.2, 'run_3': 1.2}.get(_k, 0.0))

DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'run_1', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired',
         'swim_0', 'swim_2', 'root_up', 'root', 'root_hold', 'spore_up', 'spore', 'heal_up', 'heal', 'swipe_up', 'swipe', 'bloom_up', 'bloom']
