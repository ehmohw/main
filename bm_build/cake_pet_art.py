"""(3.1 draft, stage 1: art only - not wired) THE CAKE - Queen Pearl's cake, finished at last. Hand Queen Pearl a cake while the
Chef is out, and she remembers what she always said ("I am cake" - and "I want someone to finish the cake"): the Chef finishes it,
and it gets up off the plate. Small, bouncy, and slightly unhinged - a living two-tier birthday cake that is VERY happy to be here.

LOOK  Knee-high (~0.8 blocks to the tip of its candle flame). A rounded-square bottom tier of golden sponge with a jam-and-cream
      seam, its FACE on the front (mismatched big eyes - its left bigger, tiny pupils - a wide jam-red grin with cream teeth,
      sprinkle freckles); pink strawberry frosting poured over the top and dripping down the sides in fat drips; a smaller top
      tier with its own frosting, a ring of piped rosettes, a cherry on a springy stem and a single striped candle with a lit
      flame. Two stubby ladyfinger legs, two thin wafer-stick arms, and a big silver cake FORK in its right hand (its weapon).
      The top tier is a LID: hinged at the back, it flips open like a mouth (the chomp) to show the jam inside, ringed with
      cream teeth.

RIG   base (the root: the bottom tier and its face) - lid (the top tier, frosting, rosettes, candle; hinged at the back) - cherry
      (on the lid, springs) - armr / arml (wafer sticks) - fork (in the right hand) - legr / legl; effects: 'splat' (a ring of
      frosting on the floor, the slam), 'spr' (a fountain of sprinkles over it), 'crumbs'.

SKINS '_sh' the SHINY, a frosting palette - "Midnight Velvet": blue-violet velvet sponge, silver-white frosting, a sugared
      blue cherry, gold sprinkles. Cosmetic flavours (per form): '_mint' (mint frosting, chocolate sponge), '_lem' (lemon
      frosting, white sponge), '_choc' (chocolate ganache, a vanilla sponge)."""
import math
import random
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, blob

PIVOT = {'base': (0, 4.0, 0), 'lid': (0, 7.6, 3.2), 'cherry': (0, 14.2, 0), 'armr': (5.8, 5.6, 0), 'arml': (-5.8, 5.6, 0),
         'fork': (9.2, 3.0, -1.0), 'legr': (2.6, 2.2, 0), 'legl': (-2.6, 2.2, 0), 'splat': (0, 0, 0), 'spr': (0, 16, 0), 'crumbs': (0, 0, -4)}
PARENT = {'base': None, 'lid': 'base', 'cherry': 'lid', 'armr': 'base', 'arml': 'base', 'fork': 'armr', 'legr': None, 'legl': None,
          'splat': None, 'spr': 'base', 'crumbs': None}
FACES = ('happy', 'blink', 'manic', 'hurt', 'sleepy', 'chomp')
R = Rig('ck_', 0.8, PIVOT, PARENT, FACES, face_part='base', opt=('splat', 'spr', 'crumbs'))

COL = {'sponge': '#efbe6a', 'crumb': '#c8893a', 'frost': '#ff8fc4', 'frost_hi': '#ffc4e0', 'frost_dk': '#e0609e', 'jam': '#cc1a3c',
       'cream': '#fff6ec', 'cherry': '#e01030', 'wafer': '#e9b062', 'stick': '#c98a3c'}
FLAVOURS = {'_sh': {'sponge': '#3a2a8a', 'crumb': '#1e1450', 'frost': '#e8ecff', 'frost_hi': '#ffffff', 'frost_dk': '#aab4e0',
                    'jam': '#2a3ac0', 'cream': '#fff8e0', 'cherry': '#3a7aff', 'sprk': ('#ffd23a', '#ffffff', '#ffe890')},
            '_mint': {'sponge': '#6a3e22', 'crumb': '#3e2210', 'frost': '#8ee8c0', 'frost_hi': '#c8ffe8', 'frost_dk': '#4cbc90'},
            '_lem': {'sponge': '#fff0c8', 'crumb': '#e0c890', 'frost': '#ffe24a', 'frost_hi': '#fff6a8', 'frost_dk': '#e8b820'},
            '_choc': {'sponge': '#f6dca0', 'crumb': '#d0a860', 'frost': '#6a3a1e', 'frost_hi': '#9a5a30', 'frost_dk': '#3e200e'}}
SPRK = ('#ff3a5a', '#3ac0ff', '#ffe03a', '#6aff6a', '#ffffff', '#b06aff')


def _tex(c, sprk=SPRK):
    sp = c['sponge']; fr = c['frost']
    t = {'sponge': coat(sp, 1, 16, 0.07, 1, spots=[(c['crumb'], 14), ('#ffffff', 2)]),
         'frost': coat(fr, 2, 16, 0.05, 1, spots=[(c['frost_hi'], 10)] + [(s, 2) for s in sprk]),
         'frost_plain': coat(fr, 3, 16, 0.05, 1, spots=[(c['frost_hi'], 8), (c['frost_dk'], 6)]),
         'jam': coat(c['jam'], 4, 16, 0.08, 1, spots=[('#ffffff', 2)]), 'cream': coat(c['cream'], 5, 16, 0.03, 1),
         'cherry': coat(c['cherry'], 6, 16, 0.06, 1, spots=[('#ffffff', 3)]), 'wafer': _wafer(c.get('wafer', '#e9b062')),
         'stick': coat(c.get('stick', '#c98a3c'), 7, 16, 0.08, 1)}
    t['face'] = _face(None, c)
    for f in FACES: t[f'face_{f}'] = _face(f, c)
    return t


def _wafer(col):
    im = coat(col, 8, 16, 0.05, 1); px = im.load(); dk = hexc('#b8803a')
    for i in range(16):
        for j in range(0, 16, 4): px[i, j] = dk; px[j, i] = dk
    return im


def _face(kind, c):
    """the front of the bottom tier: sponge, a jam-and-cream seam low across it, and its face over the top"""
    im, d = canvas(32); base = coat(c['sponge'], 9, 32, 0.07, 2, spots=[(c['crumb'], 30)]); im.paste(base)
    d.rectangle((0, 24, 31, 25), fill=hexc(c['cream'])); d.rectangle((0, 26, 31, 27), fill=hexc(c['jam'])); d.rectangle((0, 28, 31, 28), fill=hexc(c['cream']))
    K, W = hexc('#2a1218'), hexc('#ffffff')
    # eyes: its right small (x 6..12), its left BIG (x 18..27) - unhinged
    if kind in (None, 'manic', 'chomp'):
        big = kind == 'manic'
        d.ellipse((6, 6, 13, 14), fill=W, outline=K); d.ellipse((17, 3, 28, 15) if not big else (16, 2, 29, 16), fill=W, outline=K)
        if big: d.rectangle((9, 9, 10, 10), fill=K); d.rectangle((22, 8, 23, 9), fill=K)          # (pinpoint pupils)
        else: d.rectangle((9, 9, 11, 12), fill=K); d.rectangle((21, 7, 24, 11), fill=K); d.point((10, 9), fill=W); d.point((22, 8), fill=W)
    elif kind == 'happy':
        d.arc((6, 7, 13, 15), 200, 340, fill=K, width=2); d.arc((17, 4, 28, 16), 200, 340, fill=K, width=2)
    elif kind in ('blink', 'sleepy'):
        d.line((6, 11, 13, 11), fill=K, width=2); d.line((17, 10, 28, 10), fill=K, width=2)
        if kind == 'sleepy': d.text((26, 0), 'z', fill=K)
    elif kind == 'hurt':
        d.line((6, 8, 13, 13), fill=K, width=2); d.line((6, 13, 13, 8), fill=K, width=2)
        d.line((17, 6, 27, 14), fill=K, width=2); d.line((17, 14, 27, 6), fill=K, width=2)
    # the mouth
    if kind in (None, 'happy', 'manic'):
        w = 2 if kind != 'manic' else 0
        d.chord((7 - w, 12, 25 + w, 23 + w), 0, 180, fill=hexc(c['jam']), outline=K)
        for x in range(9 - w, 24 + w, 3): d.rectangle((x, 17, x + 1, 18), fill=W)                  # (cream teeth)
    elif kind == 'chomp':
        d.ellipse((10, 14, 22, 23), fill=hexc('#5a0a1a'), outline=K)
    elif kind == 'hurt':
        d.line((10, 20, 13, 18, 16, 20, 19, 18, 22, 20), fill=K, width=2)
    else:
        d.arc((11, 15, 21, 21), 20, 160, fill=K, width=1)
    # sprinkle freckles
    for (x, y), s in zip(((4, 17), (27, 18), (29, 20), (3, 20)), SPRK): d.rectangle((x, y, x + 1, y), fill=hexc(s))
    return im


for k, v in _tex(COL).items(): R.tex(k, v)
R.tex('silver', coat('#d8dce4', 10, 16, 0.05, 1, spots=[('#ffffff', 4), ('#9aa0ac', 4)])); R.tex('flame', flat('#ffd23a'))
R.tex('candle', _wafer('#ffffff')); R.tex('stem', flat('#3a7a2a'))
for sfx, ch in FLAVOURS.items():
    c = dict(COL, **ch)
    for k, v in _tex(c, ch.get('sprk', SPRK)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in _tex(c)})


def tier(part, y0, h, r, tex, front=None):
    """a rounded-square tier: two crossed boxes; the front plate carries the face"""
    R.box(part, (-r, y0, -r * 0.78), (r, y0 + h, r * 0.78), tex)
    R.box(part, (-r * 0.78, y0, -r), (r * 0.78, y0 + h, r), tex)
    if front:
        R.box(part, (-r * 0.78, y0, -r - 0.05), (r * 0.78, y0 + h, -r), front, faces=('north',), uv={'north': [0, 0, 16, 16]})


# ---- the bottom tier, its frosting and drips
tier('base', 2.0, 5.6, 6.0, 'sponge', 'FACE')
tier('base', 7.4, 0.8, 6.3, 'frost_plain')
for i, (a, L) in enumerate(((20, 2.6), (70, 1.6), (115, 3.0), (160, 1.8), (205, 2.4), (250, 1.4), (295, 2.8), (340, 1.7))):
    x, z = 6.05 * math.sin(math.radians(a)), -6.05 * math.cos(math.radians(a))
    if -7 < x < 7 and z < -5 and abs(x) < 3.4: continue                                    # (keep the face clear)
    R.box('base', (x - 0.8, 7.4 - L, z - 0.5), (x + 0.8, 7.6, z + 0.5), 'frost_plain', rot=('y', -a, (x, 7, z)))
# ---- the lid: the top tier, frosting, rosettes, the candle
tier('lid', 7.8, 3.6, 4.2, 'sponge')
tier('lid', 11.2, 0.9, 4.5, 'frost')
for i in range(8):
    a = math.radians(i * 45 + 22.5); x, z = 4.6 * math.sin(a), 4.6 * math.cos(a)
    R.box('lid', (x - 0.7, 7.4, z - 0.7), (x + 0.7, 8.4, z + 0.7), 'frost_plain')               # (rosettes round the base of the top tier)
R.box('lid', (1.6, 12.1, 0.6), (2.6, 15.6, 1.6), 'candle')
R.box('lid', (1.75, 15.6, 0.75), (2.45, 17.0, 1.45), 'flame', light=14)
# (inside: when the lid lifts, the jam mouth on top of the bottom tier, ringed with cream teeth)
R.box('base', (-4.6, 7.62, -4.6), (4.6, 8.3, 4.6), 'jam')
for i in range(10):
    a = math.radians(i * 36); x, z = 4.1 * math.sin(a), 4.1 * math.cos(a)
    R.box('base', (x - 0.5, 8.2, z - 0.5), (x + 0.5, 9.3, z + 0.5), 'cream')
# ---- the cherry on its springy stem
blob(R, 'cherry', (0, 13.6, 0), 1.5, 'cherry')
R.seg('cherry', (0, 15.0, 0), (0.6, 17.0, 0.4), 0.35, 0.35, 'stem')
# ---- arms, fork, legs
for p, sx in (('armr', 1), ('arml', -1)):
    x, y, z = PIVOT[p]
    R.seg(p, (x, y, z), (x + sx * 3.4, y - 2.6, z - 1.0), 0.9, 0.9, 'wafer')
    blob(R, p, (x + sx * 3.5, y - 2.7, z - 1.0), 0.8, 'frost_plain')                                   # (a frosting mitten)
fx, fy, fz = PIVOT['fork']
R.box('fork', (fx - 0.35, fy - 3.0, fz - 0.35), (fx + 0.35, fy + 1.0, fz + 0.35), 'silver')
R.box('fork', (fx - 1.1, fy + 1.0, fz - 0.3), (fx + 1.1, fy + 1.8, fz + 0.3), 'silver')
for dx in (-1.0, -0.33, 0.33, 1.0):
    R.box('fork', (fx + dx - 0.18, fy + 1.8, fz - 0.2), (fx + dx + 0.18, fy + 4.4, fz + 0.2), 'silver')
for p, sx in (('legr', 1), ('legl', -1)):
    x, y, z = PIVOT[p]
    R.box(p, (x - 0.9, 0, z - 1.6), (x + 0.9, y + 0.4, z + 0.9), 'wafer')
# ---- effects
for i in range(12):
    a = math.radians(i * 30); x, z = 9 * math.sin(a), 9 * math.cos(a); s = 1.4 + (i % 3) * 0.5
    R.box('splat', (x - s, 0.0, z - s), (x + s, 0.7 + (i % 2) * 0.4, z + s), 'frost_plain')
rr = random.Random(5)
for i in range(16):
    x, y, z = rr.uniform(-6, 6), 16 + rr.uniform(0, 7), rr.uniform(-6, 6)
    R.box('spr', (x - 0.25, y - 0.6, z - 0.25), (x + 0.25, y + 0.6, z + 0.25), 'frost', rot=('z', rr.uniform(-60, 60), (x, y, z)))
for i in range(6):
    x, z = rr.uniform(-3, 3), -4 + rr.uniform(-2, 2)
    R.box('crumbs', (x - 0.5, 0, z - 0.5), (x + 0.5, 0.8, z + 0.5), 'sponge')


# ---- poses (bouncy: every step a little hop)
def P(lift=0.0, **kw):
    kw.setdefault('legr', limb(1)); kw.setdefault('legl', limb(-1))
    return R.ground(kw, lift)


ARMS = dict(armr=limb(1, 10, 10), arml=limb(-1, 10, 10))
POSES = R.POSES
POSES.update({
    'idle_a': P(**ARMS, cherry=T(0, 0, -8)),
    'idle_b': P(lift=1.2, _face='happy', armr=limb(1, 0, 50), arml=limb(-1, 0, 50), cherry=T(0, 0, 14)),       # (a happy little hop)
    'idle_c': P(_face='manic', base=T(0, 0, 8), lid=T(-6, 0, -6), cherry=T(0, 0, 20), **ARMS),                    # (the twitch)
    'walk_0': P(lift=1.6, base=T(8), legr=limb(1, 30), legl=limb(-1, -20), armr=limb(1, -20, 20), arml=limb(-1, 30, 20), cherry=T(-14)),
    'walk_1': P(lift=0.0, base=T(-4), legr=limb(1, -10), legl=limb(-1, 20), armr=limb(1, 20, 20), arml=limb(-1, -10, 20), cherry=T(12)),
    'run_0': P(lift=2.6, _face='manic', base=T(16), legr=limb(1, 50), legl=limb(-1, -40), armr=limb(1, -40, 40), arml=limb(-1, -40, 40), cherry=T(-26)),
    # sitting: plonked down on its plate, legs straight out, the fork across its lap; then a doze (the candle still lit)
    'sit_a': P(_face='happy', legr=limb(1, 88), legl=limb(-1, 88), armr=limb(1, 40, 0, -40), arml=limb(-1, 20, 30)),
    'sit_b': P(_face='sleepy', base=T(-6, 0, 6), legr=limb(1, 88, 10), legl=limb(-1, 88, 10), armr=limb(1, 0, 6), arml=limb(-1, 0, 6), lid=T(-4)),
    # FORK! - wound up over its head, then a stab
    'fork_up': P(_face='manic', base=T(-8, -16), armr=limb(1, 160, 10), arml=limb(-1, 20, 30), cherry=T(10)),
    'fork': P(_face='happy', base=T(14, 18), armr=limb(1, 90, -6), fork=T(80), arml=limb(-1, -20, 30), legr=limb(1, -20), legl=limb(-1, 24), cherry=T(-20)),
    # I AM CAKE (the chomp): the lid flips open - the jam mouth, cream teeth - and snaps shut on a foe
    'chomp': P(_face='chomp', base=T(10), lid=T(-70), armr=limb(1, 40, 40), arml=limb(-1, 40, 40)),
    # LAYER SLAM (charged): a huge bounce, tucked - then down flat, frosting splashing out in a ring
    'slam_up': P(lift=10.0, _face='manic', legr=limb(1, 70), legl=limb(-1, 70), armr=limb(1, 0, 150), arml=limb(-1, 0, 150), cherry=T(30)),
    'slam': P(_face='happy', _show=('splat', 'crumbs'), legr=limb(1, 0, 40), legl=limb(-1, 0, 40), armr=limb(1, 0, 80), arml=limb(-1, 0, 80), lid=T(-14), cherry=T(-30)),
    # SPRINKLE SHOWER: the lid tipped, sprinkles fountaining out of it over its friends (a heal, a sugar rush)
    'sprinkle': P(_face='happy', _show=('spr',), lid=T(-30), armr=limb(1, 0, 120), arml=limb(-1, 0, 120)),
    'happy': P(lift=2.0, _face='happy', armr=limb(1, 0, 140), arml=limb(-1, 0, 140), legr=limb(1, 30), legl=limb(-1, 30), cherry=T(0, 0, 25)),
    'hurt': P(_face='hurt', _show=('crumbs',), base=T(-14, 0, 10), lid=T(10, 0, -10), armr=limb(1, 20, 60), arml=limb(-1, 20, 60)),
    'tired': P(_face='blink', base=T(-80), legr=limb(1, 60), legl=limb(-1, 60), armr=limb(1, 0, 70), arml=limb(-1, 0, 70)),
})
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'sit_a', 'sit_b', 'fork_up', 'fork', 'chomp', 'slam_up', 'slam', 'sprinkle', 'happy', 'hurt', 'tired']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'lid': 'head', 'cherry': 'head', 'base': 'head', 'armr': 'body', 'arml': 'body', 'fork': 'body'}   # (a cake is all head: kb on its arms)
SHINY = 'Shiny Midnight Velvet'
