"""(3.1 draft, stage 1: art only - not wired) THE CAKE - Queen Pearl's cake, finished at last. Hand Queen Pearl a cake while the
Chef is out, and she remembers what she always said ("I am cake" - and "I want someone to finish the cake"): the Chef finishes it,
and it hops up off the plate. Small, round, bouncy and adorable - a living birthday cake that is very happy to be here.

(2nd pass, the owner: "make the cake cuter and not so weird" - matching big round shiny eyes, set low; a small smile; rosy
frosting-pink cheeks; one plump round tier with a little top tier worn like a hat; nub feet and nub arms; the candle flame a
little flickering hair tuft. No mismatched eyes, no toothy grin, no opening lid.)

LOOK  Knee-high (~0.75 blocks to the flame's tip). ONE PLUMP ROUND TIER of golden sponge (rounded on every side - three
      crossed boxes and a rounded crown), a jam-and-cream seam low round its middle; pink strawberry frosting poured over its
      top in a soft rim with fat round drips down the sides. Its FACE on the front, low: two big round matching eyes (dark,
      a big white shine and a small one in each), rosy frosting-pink cheeks, a tiny smile (happy: a cat-mouth; wow: a little
      'o'). A SMALL TOP TIER worn like a hat, a touch askew, ringed with piped rosettes, with the CHERRY on top and a striped
      CANDLE whose flame flickers like a tuft of hair. Two round nub feet, two round frosting nub arms, and a tiny silver
      FORK in its right nub.

RIG   base (the root: the tier and its face) - hat (the top tier, rosettes, candle) - flame (flickers) - cherry - armr / arml
      (nubs) - fork (right) - legr / legl (nub feet); effects: 'splat' (a ring of frosting on the floor, the slam), 'spr'
      (a fountain of sprinkles), 'dollop' (a frosting dollop on its nub - the boop).

SKINS '_sh' the SHINY, a frosting palette - "Midnight Velvet": blue-violet velvet sponge, silver-white frosting, a sugared
      blue cherry, gold sprinkles. Cosmetic flavours (per form): '_mint' (mint frosting, chocolate sponge), '_lem' (lemon
      frosting, white sponge), '_choc' (chocolate ganache, a vanilla sponge)."""
import math
import random
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, blob

PIVOT = {'base': (0, 5.0, 0), 'hat': (0, 10.4, 0.5), 'flame': (1.6, 16.0, 1.4), 'cherry': (-0.6, 14.4, 0.2), 'armr': (7.6, 5.0, -1.2),
         'arml': (-7.6, 5.0, -1.2), 'fork': (8.8, 3.6, -2.4), 'legr': (3.0, 1.3, -3.6), 'legl': (-3.0, 1.3, -3.6),
         'splat': (0, 0, 0), 'spr': (0, 16, 0), 'dollop': (-8.6, 4.4, -3.0)}
PARENT = {'base': None, 'hat': 'base', 'flame': 'hat', 'cherry': 'hat', 'armr': 'base', 'arml': 'base', 'fork': 'armr', 'legr': None,
          'legl': None, 'splat': None, 'spr': 'base', 'dollop': 'arml'}
FACES = ('happy', 'blink', 'wow', 'hurt', 'sleepy', 'boop')
R = Rig('ck_', 0.8, PIVOT, PARENT, FACES, face_part='base', opt=('splat', 'spr', 'dollop'))

COL = {'sponge': '#f2c477', 'crumb': '#d8994a', 'frost': '#ff9ccb', 'frost_hi': '#ffd0e6', 'frost_dk': '#ec74b0', 'jam': '#e0405e',
       'cream': '#fff6ec', 'cherry': '#ee2244', 'cheek': '#ff7eb6'}
FLAVOURS = {'_sh': {'sponge': '#3e2e90', 'crumb': '#241a5a', 'frost': '#e8ecff', 'frost_hi': '#ffffff', 'frost_dk': '#b0bae4',
                    'jam': '#3a4ad0', 'cream': '#fff8e0', 'cherry': '#3a7aff', 'cheek': '#c8d0ff', 'sprk': ('#ffd23a', '#ffffff', '#ffe890')},
            '_mint': {'sponge': '#7a4a2a', 'crumb': '#4a2a14', 'frost': '#9aecc8', 'frost_hi': '#d0fff0', 'frost_dk': '#5ac49a', 'cheek': '#7ad8b0'},
            '_lem': {'sponge': '#fff2cc', 'crumb': '#e8d098', 'frost': '#ffe45a', 'frost_hi': '#fff8b0', 'frost_dk': '#ecc02a', 'cheek': '#ffb070'},
            '_choc': {'sponge': '#f6dca0', 'crumb': '#d8b068', 'frost': '#7a4424', 'frost_hi': '#a86a3c', 'frost_dk': '#4a2812', 'cheek': '#ff9a9a'}}
SPRK = ('#ff5a7a', '#5ac8ff', '#ffe05a', '#7aff7a', '#ffffff', '#c08aff')


def _face(kind, c):
    """the front of the tier: sponge, the jam-and-cream seam low across it, and its face - big round matching shiny eyes set
    low, rosy cheeks, a tiny smile"""
    im, d = canvas(32); im.paste(coat(c['sponge'], 9, 32, 0.05, 2, spots=[(c['crumb'], 18)]))
    d.rectangle((0, 27, 31, 27), fill=hexc(c['cream'])); d.rectangle((0, 28, 31, 29), fill=hexc(c['jam'])); d.rectangle((0, 30, 31, 30), fill=hexc(c['cream']))
    K, W, B2 = hexc('#2a1620'), hexc('#ffffff'), hexc('#5a3a5a')
    ey = 10
    for x0 in (5, 19):
        if kind in (None, 'wow', 'boop' if False else None):
            d.ellipse((x0, ey, x0 + 8, ey + 9), fill=K)
            d.ellipse((x0 + 1, ey + 5, x0 + 7, ey + 9), fill=B2)                 # (a soft lower glow in the eye)
            d.ellipse((x0 + 1, ey + 1, x0 + 4, ey + 4), fill=W); d.rectangle((x0 + 5, ey + 6, x0 + 6, ey + 7), fill=W)
        elif kind == 'boop' and x0 == 19:                                         # (a wink: its left eye shut)
            d.arc((x0, ey + 2, x0 + 8, ey + 9), 200, 340, fill=K, width=2)
        elif kind == 'boop':
            d.ellipse((x0, ey, x0 + 8, ey + 9), fill=K); d.ellipse((x0 + 1, ey + 1, x0 + 4, ey + 4), fill=W); d.rectangle((x0 + 5, ey + 6, x0 + 6, ey + 7), fill=W)
        elif kind == 'happy':
            d.arc((x0, ey + 2, x0 + 8, ey + 10), 200, 340, fill=K, width=2)
        elif kind in ('blink', 'sleepy'):
            d.arc((x0, ey - 2, x0 + 8, ey + 7), 20, 160, fill=K, width=2)
        elif kind == 'hurt':
            d.line((x0 + 1, ey + 2, x0 + 7, ey + 5), fill=K, width=2); d.line((x0 + 7, ey + 5, x0 + 1, ey + 8), fill=K, width=2) if x0 == 5 else None
            if x0 == 19: d.line((x0 + 7, ey + 2, x0 + 1, ey + 5), fill=K, width=2); d.line((x0 + 1, ey + 5, x0 + 7, ey + 8), fill=K, width=2)
    if kind == 'sleepy': d.text((26, 0), 'z', fill=K)
    # cheeks: rosy frosting-pink
    for x0 in (2, 24):
        d.ellipse((x0, ey + 9, x0 + 6, ey + 13), fill=hexc(c['cheek']))
        d.point((x0 + 2, ey + 10), fill=W)
    # the mouth: a tiny smile; a cat-mouth when happy; a little 'o' for wow / boop
    if kind in ('wow', 'boop'):
        d.ellipse((14, ey + 11, 17, ey + 14), fill=K); d.point((15, ey + 13), fill=hexc('#ff6a8a'))
    elif kind == 'happy':
        d.arc((11, ey + 9, 16, ey + 13), 0, 180, fill=K, width=1); d.arc((15, ey + 9, 20, ey + 13), 0, 180, fill=K, width=1)
    elif kind == 'hurt':
        d.line((13, ey + 13, 15, ey + 12, 17, ey + 13), fill=K)
    else:
        d.arc((12, ey + 8, 19, ey + 13), 30, 150, fill=K, width=1)
    return im


def _tex(c, sprk=SPRK):
    t = {'sponge': coat(c['sponge'], 1, 16, 0.05, 1, spots=[(c['crumb'], 10)]),
         'frost': coat(c['frost'], 2, 16, 0.04, 1, spots=[(c['frost_hi'], 10)] + [(s, 2) for s in sprk]),
         'frost_plain': coat(c['frost'], 3, 16, 0.04, 1, spots=[(c['frost_hi'], 8), (c['frost_dk'], 4)]),
         'cream': coat(c['cream'], 5, 16, 0.03, 1), 'jam': coat(c['jam'], 4, 16, 0.05, 1),
         'cherry': coat(c['cherry'], 6, 16, 0.05, 1, spots=[('#ffffff', 3)]), 'sidecake': _side(c)}
    t['face'] = _face(None, c)
    for f in FACES: t[f'face_{f}'] = _face(f, c)
    return t


def _side(c):
    """the tier's sides: sponge with the seam at the same height as on the face"""
    im = coat(c['sponge'], 11, 16, 0.05, 1, spots=[(c['crumb'], 8)]); d = canvas(16)[1]
    from PIL import ImageDraw
    d = ImageDraw.Draw(im); d.rectangle((0, 12, 15, 12), fill=hexc(c['cream'])); d.rectangle((0, 13, 15, 13), fill=hexc(c['jam']))
    return im


for k, v in _tex(COL).items(): R.tex(k, v)
R.tex('silver', coat('#d8dce4', 10, 16, 0.05, 1, spots=[('#ffffff', 4), ('#9aa0ac', 4)])); R.tex('flame', flat('#ffd23a')); R.tex('flame2', flat('#ff8a2a'))
R.tex('candle', coat('#ffffff', 12, 16, 0.02, 1, spots=[('#7ac8ff', 30)])); R.tex('stem', flat('#3a8a2a'))
for sfx, ch in FLAVOURS.items():
    c = dict(COL, **ch)
    for k, v in _tex(c, ch.get('sprk', SPRK)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in _tex(c)})

B = R.box
# ---- the plump tier: rounded on every side, its face on the front
r, y0, y1 = 6.4, 1.2, 9.4
B('base', (-r, y0 + 0.8, -r * 0.8), (r, y1 - 0.4, r * 0.8), 'sidecake')
B('base', (-r * 0.8, y0 + 0.8, -r), (r * 0.8, y1 - 0.4, r), 'sidecake')
B('base', (-r * 0.86, y0, -r * 0.86), (r * 0.86, y1, r * 0.86), 'sidecake')
B('base', (-r * 0.8, y0 + 0.8, -r - 0.05), (r * 0.8, y1 - 0.4, -r), 'FACE', faces=('north',), uv={'north': [0, 0, 16, 16]})
# the frosting: a soft rim over the top, fat round drips down the sides (none over the face's eyes)
B('base', (-r * 0.9, y1, -r * 0.9), (r * 0.9, y1 + 0.9, r * 0.9), 'frost')
B('base', (-r - 0.2, y1 - 0.6, -r * 0.72), (r + 0.2, y1 + 0.4, r * 0.72), 'frost_plain')
B('base', (-r * 0.72, y1 - 0.6, -r - 0.2), (r * 0.72, y1 + 0.4, r + 0.2), 'frost_plain')
for a, L in ((35, 1.8), (75, 2.6), (120, 1.6), (160, 2.4), (200, 2.0), (245, 2.8), (285, 1.7), (325, 2.2)):
    x, z = (r + 0.1) * math.sin(math.radians(a)), -(r + 0.1) * math.cos(math.radians(a))
    B('base', (x - 0.9, y1 - 0.6 - L, z - 0.6), (x + 0.9, y1, z + 0.6), 'frost_plain', rot=('y', -a, (x, y1, z)))
    blob(R, 'base', (x * 1.0, y1 - 0.6 - L, z * 1.0), 0.9, 'frost_plain')
# ---- the little top tier, worn like a hat (a touch askew), rosettes, the cherry, the candle
hy = 10.4
B('hat', (-3.4, hy, -2.9), (3.4, hy + 3.0, 3.9), 'sidecake')
B('hat', (-3.6, hy + 3.0, -3.1), (3.6, hy + 3.7, 4.1), 'frost')
for i in range(8):
    a = math.radians(i * 45 + 22.5); x, z = 3.7 * math.sin(a), 0.5 + 3.7 * math.cos(a)
    blob(R, 'hat', (x, hy + 0.3, z), 0.7, 'frost_plain')
blob(R, 'cherry', (-0.6, 15.2, 0.2), 1.5, 'cherry')
R.seg('cherry', (-0.6, 16.5, 0.2), (0.2, 18.2, 0.6), 0.35, 0.35, 'stem')
B('hat', (1.1, hy + 3.6, 0.9), (2.1, hy + 6.2, 1.9), 'candle')
# the flame: a little tuft - three licks, curling over like a cowlick
fx, fy, fz = PIVOT['flame']
B('flame', (fx - 0.7, fy, fz - 0.5), (fx + 0.7, fy + 2.2, fz + 0.5), 'flame', light=14)
B('flame', (fx - 0.45, fy + 1.4, fz - 0.4), (fx + 0.45, fy + 3.4, fz + 0.4), 'flame', rot=('z', -34, (fx, fy + 1.4, fz)), light=14)
B('flame', (fx - 0.4, fy + 0.8, fz - 0.35), (fx + 0.4, fy + 2.4, fz + 0.35), 'flame2', rot=('z', 38, (fx, fy + 0.8, fz)), light=14)
B('flame', (fx - 0.3, fy - 0.2, fz - 0.55), (fx + 0.3, fy + 0.8, fz - 0.5), 'flame2', faces=('north',), light=14)
# ---- nub arms (round frosting nubs), the tiny fork, nub feet
for p in ('armr', 'arml'):
    blob(R, p, PIVOT[p], 1.3, 'frost_plain')
fx, fy, fz = PIVOT['fork']
B('fork', (fx - 0.25, fy - 1.6, fz - 0.25), (fx + 0.25, fy + 1.0, fz + 0.25), 'silver')
B('fork', (fx - 0.8, fy + 1.0, fz - 0.2), (fx + 0.8, fy + 1.5, fz + 0.2), 'silver')
for dx in (-0.65, 0.0, 0.65):
    B('fork', (fx + dx - 0.14, fy + 1.5, fz - 0.14), (fx + dx + 0.14, fy + 3.0, fz + 0.14), 'silver')
for p in ('legr', 'legl'):
    x, y, z = PIVOT[p]
    blob(R, p, (x, y, z - 0.2), 1.45, 'sponge', k=(1.0, 0.95, 1.15))
# ---- effects
for i in range(12):
    a = math.radians(i * 30); x, z = 9 * math.sin(a), 9 * math.cos(a); s = 1.3 + (i % 3) * 0.4
    blob(R, 'splat', (x, 0.4, z), s, 'frost_plain', k=(1.0, 0.4, 1.0))
rr = random.Random(5)
for i in range(16):
    x, y, z = rr.uniform(-6, 6), 16 + rr.uniform(0, 7), rr.uniform(-6, 6)
    B('spr', (x - 0.25, y - 0.6, z - 0.25), (x + 0.25, y + 0.6, z + 0.25), 'frost', rot=('z', rr.uniform(-60, 60), (x, y, z)))
dx, dy, dz = PIVOT['dollop']
blob(R, 'dollop', (dx - 0.4, dy, dz - 0.6), 1.3, 'frost'); blob(R, 'dollop', (dx - 0.4, dy + 1.1, dz - 0.6), 0.8, 'frost_plain')


# ---- poses (bouncy: every step a little hop)
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


NUBS = dict(armr=limb(1, 6, 8), arml=limb(-1, 6, 8))
POSES = R.POSES
POSES.update({
    'idle_a': P(**NUBS, hat=T(0, 0, -4), flame=T(0, 0, -10)),
    'idle_b': P(lift=1.4, _face='happy', armr=limb(1, 0, 40), arml=limb(-1, 0, 40), hat=T(0, 0, 4), flame=T(0, 0, 14), cherry=T(0, 0, 10)),   # (a happy little hop)
    'idle_c': P(_face='wow', base=T(-4, 0, 8), hat=T(0, 0, -6), flame=T(0, 0, -20), **NUBS),                                          # (curious: a tilt)
    'walk_0': P(lift=1.4, base=T(6, 0, 4), hat=T(0, 0, -4), flame=T(-16), legr=limb(1, 30), legl=limb(-1, -20), armr=limb(1, -20, 20), arml=limb(-1, 24, 20)),
    'walk_1': P(lift=0.0, base=T(-2, 0, -4), hat=T(0, 0, 4), flame=T(10), legr=limb(1, -14), legl=limb(-1, 24), armr=limb(1, 20, 20), arml=limb(-1, -14, 20)),
    'run_0': P(lift=2.4, _face='happy', base=T(12), flame=T(-34), legr=limb(1, 40), legl=limb(-1, -34), armr=limb(1, -30, 40), arml=limb(-1, -30, 40)),
    # sitting: plonked down on its plate, nub feet out front; then a doze, the hat slipped, the flame drooping
    'sit_a': P(_face='happy', legr=limb(1, 70), legl=limb(-1, 70), _off=(0, -1.0, 0), armr=limb(1, 20, 0), arml=limb(-1, 20, 0)),
    'sit_b': P(_face='sleepy', base=T(-4, 0, 6), hat=T(0, 0, 14), flame=T(30), legr=limb(1, 70, 10), legl=limb(-1, 70, 10), armr=limb(1, 0, 4), arml=limb(-1, 0, 4)),
    # TINY FORK: wound up - then a poke
    'fork_up': P(_face='wow', base=T(-6, -14), armr=limb(1, 150, 10), arml=limb(-1, 10, 30), flame=T(10)),
    'fork': P(_face='happy', base=T(10, 16), armr=limb(1, 90, -6), fork=T(80), arml=limb(-1, -10, 30), flame=T(-20)),
    # I AM CAKE: a happy little hop ... and a frosting BOOP on the foe's nose (it's sweetened: slowed, and it drops what it held)
    'hop': P(lift=4.0, _face='happy', legr=limb(1, 40), legl=limb(-1, 40), armr=limb(1, 0, 110), arml=limb(-1, 0, 110), flame=T(0, 0, 20), cherry=T(0, 0, 14)),
    'boop': P(_face='boop', _show=('dollop',), base=T(10, 18), arml=limb(-1, 92, -4), armr=limb(1, -10, 30), flame=T(-10), hat=T(0, 0, -8)),
    # LAYER SLAM (charged): a big bounce, nubs up - then a plop, frosting splashing out in a ring
    'slam_up': P(lift=9.0, _face='wow', legr=limb(1, 50), legl=limb(-1, 50), armr=limb(1, 0, 150), arml=limb(-1, 0, 150), flame=T(30)),
    'slam': P(_face='happy', _show=('splat',), legr=limb(1, 0, 40), legl=limb(-1, 0, 40), armr=limb(1, 0, 70), arml=limb(-1, 0, 70), hat=T(-10), flame=T(-30)),
    # SPRINKLE SHOWER: hat tipped, sprinkles fountaining over its friends (a heal - a sugar rush)
    'sprinkle': P(_face='happy', _show=('spr',), hat=T(-24, 0, 10), armr=limb(1, 0, 120), arml=limb(-1, 0, 120)),
    'happy': P(lift=2.0, _face='happy', armr=limb(1, 0, 140), arml=limb(-1, 0, 140), legr=limb(1, 30), legl=limb(-1, 30), flame=T(0, 0, 25)),
    'hurt': P(_face='hurt', base=T(-12, 0, 10), hat=T(10, 0, -12), armr=limb(1, 20, 50), arml=limb(-1, 20, 50), flame=T(0, 0, -40)),
    'tired': P(_face='blink', base=T(0, 0, 80), legr=limb(1, 0, 50), legl=limb(-1, 0, 50), hat=T(0, 0, 10), flame=T(60)),
})
POSES['sit_a'] = R.ground(POSES['sit_a'])
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'sit_a', 'sit_b', 'fork_up', 'fork', 'hop', 'boop', 'slam_up', 'slam', 'sprinkle', 'happy', 'hurt', 'tired']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'hat': 'head', 'cherry': 'head', 'flame': 'head', 'base': 'head', 'armr': 'body', 'arml': 'body', 'fork': 'body'}   # (a cake is all head)
SHINY = 'Shiny Midnight Velvet'
SKIN_NAMES = {'_sh': 'SHINY Midnight Velvet', '_mint': 'Mint', '_lem': 'Lemon', '_choc': 'Chocolate'}
