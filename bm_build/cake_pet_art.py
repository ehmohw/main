"""(3.1 draft, stage 1: art only - not wired) THE CAKE - Queen Pearl's cake, finished at last. Hand Queen Pearl a cake while the
Chef is out, and she remembers what she always said ("I am cake" - and "I want someone to finish the cake"): the Chef finishes it,
and it hops up off the plate. Small, round, bouncy and adorable - a living birthday cake that is very happy to be here.

(3rd pass: the quality bar. The owner liked the 2nd pass's direction ("looking better") - matching big shiny eyes set low, a
blush, a tiny smile, a plump round shape, the cherry, the candle-flame tuft, the tiny fork - so this keeps all of it and rebuilds
how it's made: a round tier of octagon slabs instead of crossed boxes, a proud jam-and-cream seam, a pillowy glazed frosting
dome with real drips (a rounded bead at each tip), sprinkles in the geometry, piped rosettes round the hat, crumb painted as
air pits instead of speckle, and the eyes built the Dryad's way - a separate overlay, graded dark to light, two shines.)

LOOK  Knee-high (~0.75 blocks to the flame's tip). ONE PLUMP ROUND TIER of golden sponge, the jam-and-cream seam low round it;
      pink strawberry frosting poured over the top - a soft pillowy dome, a rolled rim, fat drips down the sides with a bead at
      each tip, sprinkles. Its FACE on the front, low: two big round matching glossy eyes (plum-dark at the top to rosy at the
      bottom, a big white shine and a small one), rosy cheeks, a tiny smile. A SMALL TOP TIER worn like a hat, a touch askew,
      piped rosettes round its foot and rim, the CHERRY on top (a stem and a leaf) and a striped CANDLE whose flame is a little
      flickering tuft. Two round nub feet, two frosting nub arms, a tiny silver four-tined FORK in its right nub.

RIG   base (the root: the tier and its face) - hat (the top tier, rosettes, candle) - flame (flickers) - cherry - armr / arml
      (nubs) - fork (right) - legr / legl (nub feet); effects: 'splat' (a ring of frosting on the floor, the slam), 'spr'
      (a fountain of sprinkles), 'dollop' (a frosting dollop on its nub - the boop), 'aura' (the rare Birthday Wish aura).

SKINS '_sh' the SHINY "Midnight Velvet": blue-violet velvet sponge, silver-white frosting, a sugared blue cherry, gold
      sprinkles. Cosmetic flavours (per form): '_mint' (mint frosting, chocolate sponge), '_lem' (lemon frosting, white
      sponge), '_choc' (chocolate ganache, a vanilla sponge)."""
import math
import random
from PIL import Image
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, glaze, sponge, glow, stripes, metal, eye, blush, mouth, put,
                      slab, stack, ball, chain, ring, cleaf, blade, bead, icing_dots)

PIVOT = {'base': (0, 5.0, 0), 'hat': (0, 10.4, 0.5), 'flame': (1.6, 16.4, 1.4), 'cherry': (-0.6, 14.4, 0.2), 'armr': (7.4, 5.0, -1.2),
         'arml': (-7.4, 5.0, -1.2), 'fork': (8.6, 3.6, -2.4), 'legr': (3.0, 1.3, -3.4), 'legl': (-3.0, 1.3, -3.4),
         'splat': (0, 0, 0), 'spr': (0, 16, 0), 'dollop': (-8.4, 4.4, -3.0), 'aura': (0, 0, 0)}
PARENT = {'base': None, 'hat': 'base', 'flame': 'hat', 'cherry': 'hat', 'armr': 'base', 'arml': 'base', 'fork': 'armr', 'legr': None,
          'legl': None, 'splat': None, 'spr': 'base', 'dollop': 'arml', 'aura': None}
FACES = ('happy', 'blink', 'wow', 'hurt', 'sleepy', 'boop')
R = Rig('ck_', 0.8, PIVOT, PARENT, FACES, face_part='base', opt=('splat', 'spr', 'dollop', 'aura'))

COL = {'sponge': '#f2c477', 'crumb': '#d8994a', 'sponge_l': '#fbd99a', 'frost': '#ff9ccb', 'frost_hi': '#ffd0e6', 'frost_dk': '#ec74b0',
       'jam': '#e0405e', 'cream': '#fff6ec', 'cherry': '#ee2244', 'cheek': '#ff7eb6', 'sprk': ('#ff5a7a', '#5ac8ff', '#ffe05a', '#7aff7a', '#ffffff', '#c08aff'),
       'iris': ('#1e0e1a', '#2e1628', '#43223e', '#5e3458', '#7e4a76', '#a8709e'), 'lash': '#2a1620', 'mouth': '#5a2236',
       'chip': ('#140804', '#22110a', '#321b10', '#472816'), 'chip_rim': '#7c4e30', 'chip_shine': '#fff6ec'}
FLAVOURS = {'_sh': {'sponge': '#3e2e90', 'crumb': '#241a5a', 'sponge_l': '#5a48b8', 'frost': '#e8ecff', 'frost_hi': '#ffffff', 'frost_dk': '#b0bae4',
                    'jam': '#3a4ad0', 'cream': '#fff8e0', 'cherry': '#3a7aff', 'cheek': '#c8d0ff', 'sprk': ('#ffd23a', '#ffffff', '#ffe890', '#c8d0ff', '#ffd23a', '#e8ecff'),
                    'iris': ('#0e0e2a', '#16184a', '#22286a', '#34408e', '#4a5cb4', '#7a90e0'),
                    'chip': ('#6a3e06', '#9a6610', '#c89424', '#e8b83a'), 'chip_rim': '#fff0a0', 'chip_shine': '#ffffff'},   # (gold dragees)
            '_mint': {'sponge': '#7a4a2a', 'crumb': '#4a2a14', 'sponge_l': '#94603a', 'frost': '#9aecc8', 'frost_hi': '#d0fff0', 'frost_dk': '#5ac49a', 'cheek': '#7ad8b0'},
            '_lem': {'sponge': '#fff2cc', 'crumb': '#e8d098', 'sponge_l': '#fffae6', 'frost': '#ffe45a', 'frost_hi': '#fff8b0', 'frost_dk': '#ecc02a', 'cheek': '#ffb070'},
            '_choc': {'sponge': '#f6dca0', 'crumb': '#d8b068', 'sponge_l': '#fff0c8', 'frost': '#7a4424', 'frost_hi': '#a86a3c', 'frost_dk': '#4a2812', 'cheek': '#ff9a9a'}}
SKIN_NAMES = {'_sh': 'SHINY Midnight Velvet', '_mint': 'Mint', '_lem': 'Lemon', '_choc': 'Chocolate'}

# the face plate: 9.2 x 5.8 units on the tier's front flat (37 x 23 texels). (EYE_*: the 3rd pass's big anime eyes, kept as names.)
FW, FH = 9.2, 5.8
EYE_C, EYE_Y, EYE_W, EYE_H = (10, 27), 1, 12, 13
# (4th pass, the eye art pass: its OWN eyes - two small glossy CHOCOLATE CHIPS set wide apart, one tiny shine each, a chip's
#  little curled peak on top, piped-icing dots for cheeks. Chips 6 x 7 at 9 and 28, their top row 7; the mouth between, low.)
CHIP_C, CHIP_Y, CHIP_W, CHIP_H = (9, 28), 7, 6, 7


# ---------------------------------------------------------------------------------------------------- textures
def _face(kind, c):
    """the face plate: smooth sponge (a lit top, the crumb only faint here), the cheeks, the mouth; 'z' when it sleeps"""
    im = lit(soft(c['sponge'], c['sponge_l'], c['crumb'], 9, 0.05), 1.06, 0.95, 8)
    by = CHIP_Y + CHIP_H
    if kind != 'hurt':                                                          # (piped icing dots, under and outside each chip)
        for cx in (CHIP_C[0] - 5, CHIP_C[1] + 5):
            icing_dots(im, cx, by, c['cheek'], mix(c['cheek'], '#ffffff', 0.6))
    mouth(im, 19, by, {None: 'smile', 'happy': 'cat', 'blink': 'smile', 'wow': 'o', 'hurt': 'wobble', 'sleepy': 'flat', 'boop': 'o'}[kind],
          c['mouth'], '#ff6a8a', 4)
    if kind == 'sleepy':
        for x, y in ((31, 1), (32, 1), (33, 1), (32, 2), (31, 3), (32, 3), (33, 3)): put(im, x, y, c['lash'])
    return im


def _eyes(kind, c):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for i, cx in enumerate(CHIP_C):
        k = {'wow': 'wide', 'boop': ('wide' if i == 0 else 'happy')}.get(kind, kind)
        bead(im, cx, CHIP_Y, CHIP_W, CHIP_H, i == 1, k, ramp=c['chip'], rim=c['chip_rim'], shine=c['chip_shine'])
    return im


def _side(c, seed):
    """the tier's sides: crumb as air pits with lit lips (the sponge pattern), light from above"""
    return lit(sponge((c['crumb'], mix(c['crumb'], c['sponge'], 0.5), c['sponge'], c['sponge_l']), seed), 1.06, 0.94, 10)


def _frost(c, seed, sprinkle=False):
    im = glaze((c['frost_dk'], c['frost'], c['frost_hi'], mix(c['frost_hi'], '#ffffff', 0.6)), seed, 3)
    return im


def _tex(c):
    t = {'side': _side(c, 1), 'side2': _side(c, 2), 'frost': _frost(c, 3), 'frost2': _frost(c, 4),
         'frosth': lit(soft(c['frost_hi'], mix(c['frost_hi'], '#ffffff', 0.5), c['frost'], 5, 0.12), 1.04, 0.96, 6),
         'cream': soft(c['cream'], '#ffffff', mix(c['cream'], c['sponge'], 0.3), 6, 0.1),
         'jam': glaze((mix(c['jam'], '#000000', 0.25), c['jam'], mix(c['jam'], '#ffffff', 0.25), mix(c['jam'], '#ffffff', 0.55)), 7, 2),
         'cherry': lit(glaze((mix(c['cherry'], '#000000', 0.3), c['cherry'], mix(c['cherry'], '#ffffff', 0.2), mix(c['cherry'], '#ffffff', 0.5)), 8, 3), 1.08, 0.82, 14),
         'foot': lit(soft(c['sponge'], c['sponge_l'], c['crumb'], 10, 0.12), 1.08, 0.86, 14),
         'face': _face(None, c), 'eyes': _eyes(None, c)}
    for i, s in enumerate(c['sprk']): t[f'sp{i}'] = soft(s, mix(s, '#ffffff', 0.4), mix(s, '#000000', 0.15), 20 + i, 0.2)
    for f in FACES: t[f'face_{f}'] = _face(f, c); t[f'eyes_{f}'] = _eyes(f, c)
    return t


BASE_T = _tex(COL)
for k, v in BASE_T.items(): R.tex(k, v)
R.tex('silver', metal(('#8a90a0', '#c8ccd8', '#e8ecf4', '#ffffff'), 11))
R.tex('candle', stripes(('#ffffff', '#ffffff', '#7ac8ff', '#7ac8ff'), 1, vertical=False))
R.tex('wick', soft('#3a2a20', '#5a4030', '#2a1a14', 12, 0.2)); R.tex('stem', soft('#4a8a2a', '#6aaa3a', '#3a6a20', 13, 0.2))
R.tex('leaf', blade(('#3a7a2a', '#5aa03a', '#78c050'), 14, rim='sides'))
R.tex('flame', lit(soft('#ffc444', '#ffe890', '#ff9a30', 15, 0.2), 1.25, 0.8, 14)); R.tex('flamec', soft('#fff8d0', '#ffffff', '#ffe890', 16, 0.2))
R.tex('wish', glow(('#ffffff', '#fff2a8', '#ffc8e0', '#ffc8e0'), 16, alpha=(230, 190, 120, 0)))
for sfx, ch in FLAVOURS.items():
    c = dict(COL, **ch)
    for k, v in _tex(c).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in BASE_T})

# ---------------------------------------------------------------------------------------------------- the model
B = R.box
NSP = len(COL['sprk'])
# ---- the plump tier: a round drum of slabs, a little fuller at the middle
TIER = [(1.2, 1.8, 5.5), (1.8, 2.6, 6.2), (2.6, 8.4, 6.6), (8.4, 9.1, 6.35)]
stack(R, 'base', TIER, 'side', shift=False)
fz = -6.6
B('base', (-FW / 2, 2.7, fz - 0.02), (FW / 2, 2.7 + FH, fz), 'FACE', faces=('north',), uv={'north': [0, 0, FW, FH]})
B('base', (-FW / 2, 2.7, fz - 0.05), (FW / 2, 2.7 + FH, fz - 0.03), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]})
# the jam-and-cream seam, low round it, a hair proud
for y0, y1, t, w in ((2.0, 2.3, 'cream', 6.72), (2.3, 2.75, 'jam', 6.76), (2.75, 2.95, 'cream', 6.72)):
    slab(R, 'base', y0, y1, w, t)
# the frosting: a rolled rim, a pillowy dome, drips with a bead at each tip (short ones over the face), sprinkles on top
slab(R, 'base', 8.9, 9.7, 6.85, 'frost')
stack(R, 'base', [(9.7, 10.2, 6.4), (10.2, 10.5, 5.4), (10.5, 10.7, 4.0)], 'frost2', top='frosth')
for i, (a, L) in enumerate(((0, 0.5), (24, 0.9), (45, 2.2), (70, 3.4), (95, 2.0), (120, 3.0), (145, 1.8), (170, 2.8), (195, 2.2),
                            (220, 3.2), (245, 1.8), (270, 2.9), (295, 2.0), (318, 0.9), (338, 0.5))):
    ra = math.radians(a); k = 0.72 if (a % 90) > 22 and (a % 90) < 68 else 1.0
    rr = 6.85 * (0.92 if k < 1 else 1.0)
    x, z = rr * math.sin(ra), -rr * math.cos(ra)
    nx, nz = math.sin(ra), -math.cos(ra)
    top, bot = (x, 9.2, z), (x + nx * 0.05, 9.2 - L, z + nz * 0.05)
    R.seg('base', top, bot, 1.15 - 0.1 * (i % 2), 0.35, 'frost', up=(nx, 0.0, nz), ext=0.1)
    if L > 0.8:
        slab(R, 'base', 9.2 - L - 0.55, 9.2 - L + 0.25, 0.68, 'frost', 0.4, c=(x + nx * 0.12, z + nz * 0.12))
rs = random.Random(5)
for i in range(18):                                                                    # (sprinkles, a hair proud on the dome)
    a = rs.uniform(0, 6.28); d = rs.uniform(1.2, 5.6)
    x, z = d * math.cos(a), d * math.sin(a); y = 10.2 if d > 5.2 else (10.5 if d > 4.0 else 10.7)
    if d > 5.5: y = 9.7
    B('base', (x - 0.42, y, z - 0.14), (x + 0.42, y + 0.18, z + 0.14), f'sp{i % NSP}', rot=('y', rs.uniform(-80, 80), (x, y, z)))

# ---- the little top tier, worn like a hat: a smaller drum, its own frosting cap, piped rosettes, the cherry, the candle
hy = 10.4; hz = 0.5
stack(R, 'hat', [(hy, hy + 0.5, 3.1), (hy + 0.5, hy + 3.0, 3.45)], 'side2', c=(0, hz), shift=False)
slab(R, 'hat', hy + 1.0, hy + 1.3, 3.52, 'jam', c=(0, hz))
slab(R, 'hat', hy + 2.9, hy + 3.5, 3.62, 'frost', c=(0, hz))
stack(R, 'hat', [(hy + 3.5, hy + 3.8, 3.2), (hy + 3.8, hy + 4.0, 2.4)], 'frost2', c=(0, hz), top='frosth')
for ring_y, rr, n, s in ((hy + 0.15, 3.65, 10, 0.62), (hy + 3.55, 3.15, 8, 0.5)):
    for i in range(n):
        a = math.radians(i * 360 / n + 18); x, z = rr * math.sin(a), hz + rr * math.cos(a)
        ball(R, 'hat', (x, ring_y + s * 0.6, z), s, 'frosth', 2, ry=s * 0.7)              # (a rosette: a soft swirl...)
        B('hat', (x - s * 0.35, ring_y + s * 1.15, z - s * 0.35), (x + s * 0.35, ring_y + s * 1.55, z + s * 0.35), 'frosth')   # (...and its peak)
# the cherry: glossy, a shine, a stem and a leaf
cx, cy, cz = -0.6, 15.6, 0.2
ball(R, 'cherry', (cx, cy, cz), 1.55, 'cherry', 4, ry=1.45, shift=False)
B('cherry', (cx - 1.0, cy + 0.2, cz - 1.62), (cx - 0.4, cy + 0.75, cz - 1.56), 'frosth', faces=('north',), light=6)
R.seg('cherry', (cx, cy + 1.3, cz), (cx + 0.5, cy + 2.4, cz + 0.3), 0.32, 0.32, 'stem')
R.seg('cherry', (cx + 0.5, cy + 2.4, cz + 0.3), (cx + 1.1, cy + 3.0, cz + 0.4), 0.28, 0.28, 'stem')
cleaf(R, 'cherry', (cx + 0.9, cy + 2.85, cz + 0.4), (0.8, 0.2, -0.5), 1.5, 1.0, 'leaf', droop=0.2, t=0.18)
# the candle: striped, a wick
R.seg('hat', (1.6, hy + 3.8, 1.4), (1.6, 16.2, 1.4), 1.0, 1.0, 'candle', shift=False)
R.seg('hat', (1.6, 16.1, 1.4), (1.6, 16.5, 1.4), 0.22, 0.22, 'wick')
# the flame: a little tuft - three licks, curling over like a cowlick, a bright core
fx, fy, fz2 = PIVOT['flame']
stack(R, 'flame', [(fy, fy + 0.5, 0.55), (fy + 0.5, fy + 1.3, 0.72), (fy + 1.3, fy + 1.9, 0.55), (fy + 1.9, fy + 2.4, 0.36)], 'flame',
      c=(fx, fz2), light=14)
R.seg('flame', (fx, fy + 2.3, fz2), (fx - 0.55, fy + 3.1, fz2 + 0.1), 0.42, 0.42, 'flame', light=14)          # (its tip curls over: a cowlick)
R.seg('flame', (fx - 0.55, fy + 3.1, fz2 + 0.1), (fx - 1.05, fy + 3.0, fz2 + 0.1), 0.3, 0.3, 'flame', light=14)
stack(R, 'flame', [(fy + 0.15, fy + 0.6, 0.36), (fy + 0.6, fy + 1.25, 0.44), (fy + 1.25, fy + 1.6, 0.28)], 'flamec', c=(fx, fz2 - 0.42), light=15)
# ---- nub arms (round frosting nubs with a swirl), the tiny fork, nub feet
for p, sx in (('armr', 1), ('arml', -1)):
    x, y, z = PIVOT[p]
    ball(R, p, (x, y, z), 1.35, 'frost', 3, ry=1.25)
    B(p, (x - 0.4, y + 1.05, z - 0.4), (x + 0.4, y + 1.45, z + 0.4), 'frosth')
fx, fy, fz3 = PIVOT['fork']
R.seg('fork', (fx, fy - 1.7, fz3), (fx, fy + 0.6, fz3), 0.42, 0.3, 'silver')
B('fork', (fx - 0.55, fy + 0.6, fz3 - 0.15), (fx + 0.55, fy + 1.1, fz3 + 0.15), 'silver')
B('fork', (fx - 0.75, fy + 1.1, fz3 - 0.13), (fx + 0.75, fy + 1.35, fz3 + 0.13), 'silver')
for dx in (-0.62, -0.21, 0.21, 0.62):
    B('fork', (fx + dx - 0.1, fy + 1.35, fz3 - 0.1), (fx + dx + 0.1, fy + 2.7, fz3 + 0.1), 'silver')
for p in ('legr', 'legl'):
    x, y, z = PIVOT[p]
    ball(R, p, (x, y, z - 0.2), 1.5, 'foot', 3, ry=1.3, d=1.15, shift=False)
# ---- effects
for i in range(12):                                                                    # (the splat: a ring of frosting puddles)
    a = math.radians(i * 30); x, z = 9 * math.sin(a), 9 * math.cos(a); s = 1.3 + (i % 3) * 0.4
    stack(R, 'splat', [(0.0, 0.35, s), (0.35, 0.6, s * 0.65)], 'frost', c=(x, z), top='frosth')
    if i % 2: B('splat', (x * 1.25 - 0.3, 1.2 + i % 3, z * 1.25 - 0.3), (x * 1.25 + 0.3, 1.8 + i % 3, z * 1.25 + 0.3), 'frost')
rr = random.Random(5)
for i in range(22):                                                                    # (the sprinkle shower)
    x, y, z = rr.uniform(-6, 6), 16 + rr.uniform(0, 8), rr.uniform(-6, 6)
    B('spr', (x - 0.2, y - 0.55, z - 0.2), (x + 0.2, y + 0.55, z + 0.2), f'sp{i % NSP}', rot=('z', rr.uniform(-70, 70), (x, y, z)), light=6)
dx, dy, dz = PIVOT['dollop']
ball(R, 'dollop', (dx - 0.4, dy + 0.3, dz - 0.6), 1.3, 'frost', 3, ry=1.0)
ball(R, 'dollop', (dx - 0.4, dy + 1.3, dz - 0.6), 0.85, 'frosth', 2, ry=0.6)
B('dollop', (dx - 0.65, dy + 1.8, dz - 0.85), (dx - 0.15, dy + 2.3, dz - 0.35), 'frosth')
# the rare BIRTHDAY WISH aura: a ring of tiny candle flames and wish-sparkles floating round it
for i in range(8):
    a = math.radians(i * 45); x, z = 9.5 * math.cos(a), 9.5 * math.sin(a); y = 9 + 2.0 * math.sin(a * 2)
    R.seg('aura', (x, y, z), (x, y + 1.3, z), 0.7, 0.7, 'flame', light=14, full=True)
    B('aura', (x - 1.2, y - 0.4, z), (x + 1.2, y + 2.0, z + 0.02), 'wish', faces=('north', 'south'), full=True, light=12)


# ---------------------------------------------------------------------------------------------------- poses (bouncy)
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
    'aura': P(_face='happy', _show=('aura',), **NUBS, hat=T(0, 0, -4)),
})
POSES['sit_a'] = R.ground(POSES['sit_a'])
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'sit_a', 'sit_b', 'fork_up', 'fork', 'hop', 'boop', 'slam_up', 'slam',
         'sprinkle', 'happy', 'hurt', 'tired', 'aura']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'hat': 'head', 'cherry': 'head', 'flame': 'head', 'base': 'head', 'armr': 'body', 'arml': 'body', 'fork': 'body'}   # (a cake is all head)
SHINY = 'Shiny Midnight Velvet'
