"""(3.1 draft, stage 1: art only - not wired) THE SAPLING - hand the Pale Dryad a Golden Apple by day while Kettle is out: she bites
it, finds the golden pip, and plants it at your feet with a little song ("Kettle, water it - no, with the WATERING can"). A mound
of earth with a golden sprout in it stands where she planted it; it grows over a few in-game days, as the Mireling does, and
each stage follows you further than the last:

  STAGE 0  THE PLANTED PIP  (day 0)   a mound of dark earth, a golden pip half in it, one green shoot (a block-like prop; not a
                                      follower yet - right-click: "it's growing", the day it'll be ready)
  STAGE 1  SPROUT           (day 1)   ankle-high (~0.45 blocks): a round pale-wood seed-body with a sweet dot-eyed face, two big
                                      cotyledon leaves on its head like ears, two little root feet, leaf-nub hands. It hops.
  STAGE 2  SAPLING          (day 3)   knee-high (~0.8): a slender pale-oak trunk, its head a rounded burl with the face, a tuft
                                      of five mint leaves for hair, twig arms with leaf hands, root legs; the pip glows gold in
                                      its chest through a knot in the bark.
  STAGE 3  TREE SPIRIT      (day 5)   waist-high (~1.2): pale-oak bark body and a big bark head, its face a pair of hollow
                                      knot-eyes with warm gold light in them and a little smile; a canopy of mint-and-silver
                                      pale-oak leaves over its head like a mop of hair, a GOLDEN APPLE hanging in it (glowing);
                                      a small blue glow-mushroom on its shoulder (the Dryad's), moss on its feet, branch arms
                                      with leafy twig fingers, splayed root legs.

RIG   (each stage its own Rig, the same parts): body (root), head (faces), armr/arml, legr/legl, canopy (stage 3: on the head),
      fx: roots (a ring of roots out of the ground before it), sap (a drop of golden sap over a friend), seeds (a burst of pips).
Skins: '_sh' the SHINY "Cherry Blossom" (stage 2-3: pink blossom, dark cherry bark, a silver apple); '_aut' the cosmetic
"Autumn Crown" (amber and red leaves; per stage)."""
import math
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, blob

STAGES = (1, 2, 3)
C = {'bark': '#d6cfc0', 'barkdk': '#8c7c68', 'leaf': '#8fd0a0', 'leafdk': '#5a9c70', 'leaflt': '#d0f0dc', 'gold': '#ffd23a',
     'root': '#a8916f', 'moss': '#6aa04a', 'mush': '#4aa8ff', 'earth': '#4a3626', 'eye': '#ffc84a'}
SKINS = {'_sh': {'bark': '#6a3a32', 'barkdk': '#40201c', 'leaf': '#ffb0d0', 'leafdk': '#e07aa8', 'leaflt': '#fff0f6', 'gold': '#e8ecf4', 'eye': '#ff8ac8'},
         '_aut': {'leaf': '#f0a030', 'leafdk': '#c04a1a', 'leaflt': '#ffd890'}}
FACES = ('happy', 'blink', 'focus', 'hurt', 'sleepy')


def _face(kind, c, stage):
    """stage 1-2: big dark dot eyes with a shine, a tiny smile, blush; stage 3: hollow knot-eyes with gold light in them"""
    im, d = canvas(32); im.paste(coat(c['bark'], 40 + stage, 32, 0.05, 2, spots=[(c['barkdk'], 20)]))
    for x in range(0, 32, 7):
        d.line((x, 0, x + 1, 31), fill=hexc(c['barkdk']))                                          # (bark grain)
    K = hexc('#2a1a10'); G = hexc(c['eye']); W = hexc('#ffffff')
    ey = 12 if stage < 3 else 11
    if kind in (None, 'focus'):
        for x in (8, 19):
            if stage < 3:
                d.ellipse((x, ey, x + 5, ey + 7), fill=K); d.rectangle((x + 1, ey + 1, x + 2, ey + 2), fill=W)
            else:
                d.ellipse((x - 1, ey - 1, x + 6, ey + 8), fill=hexc('#3a2614')); d.ellipse((x + 1, ey + 2, x + 4, ey + 6), fill=G)
        if kind == 'focus':
            d.line((7, ey - 3, 13, ey - 1), fill=K, width=2); d.line((25, ey - 3, 19, ey - 1), fill=K, width=2)
    elif kind == 'happy':
        for x in (8, 19): d.arc((x, ey, x + 6, ey + 7), 190, 350, fill=K if stage < 3 else G, width=2)
    elif kind in ('blink', 'sleepy'):
        for x in (8, 19): d.line((x, ey + 4, x + 5, ey + 4), fill=K, width=2)
    elif kind == 'hurt':
        for x in (8, 19): d.line((x, ey + 1, x + 5, ey + 6), fill=K, width=2); d.line((x, ey + 6, x + 5, ey + 1), fill=K, width=2)
    if kind == 'hurt':
        d.line((12, 25, 16, 23, 20, 25), fill=K)
    elif kind == 'focus':
        d.line((12, 24, 20, 24), fill=K)
    else:
        d.arc((12, 20, 20, 26), 20, 160, fill=K, width=1)
    for x in (4, 25): d.rectangle((x, 21, x + 3, 22), fill=hexc('#ff9aa0'))                          # (blush)
    return im


def _tex(c, stage):
    t = {'bark': coat(c['bark'], 1, 16, 0.07, 1, spots=[(c['barkdk'], 22)]), 'barkdk': coat(c['barkdk'], 2, 16, 0.08, 1),
         'leaf': coat(c['leaf'], 3, 16, 0.08, 1, spots=[(c['leafdk'], 26), (c['leaflt'], 12)]), 'leaflt': coat(c['leaflt'], 4, 16, 0.05, 1, spots=[(c['leaf'], 20)]),
         'gold': coat(c['gold'], 5, 16, 0.06, 1, spots=[('#ffffff', 6)]), 'root': coat(c['root'], 6, 16, 0.08, 1, spots=[(c['barkdk'], 12)]),
         'moss': coat(c['moss'], 7, 16, 0.1, 1), 'mush': coat(c['mush'], 8, 16, 0.06, 1, spots=[('#c8ecff', 8)]), 'stem': flat('#e8e4d8'),
         'earth': coat(c['earth'], 9, 16, 0.1, 1, spots=[('#2e2018', 20), ('#6a5040', 10)])}
    t['face'] = _face(None, c, stage)
    for f in FACES: t[f'face_{f}'] = _face(f, c, stage)
    return t


def make(stage):
    """the Sapling at one stage of its growth"""
    k = {1: 0.55, 2: 0.8, 3: 1.0}[stage]                     # (how far it's grown)
    hh = {1: 6.0, 2: 7.0, 3: 9.0}[stage]                     # (the head's size)
    by = {1: 2.0, 2: 6.0, 3: 8.0}[stage]                     # (the body's top: the neck)
    PIVOT = {'body': (0, by * 0.5 + 1, 0), 'head': (0, by, 0), 'armr': (2.0 * k + 0.6, by - 0.8, 0), 'arml': (-2.0 * k - 0.6, by - 0.8, 0),
             'legr': (1.2 * k + 0.2, 1.6 * k, 0), 'legl': (-1.2 * k - 0.2, 1.6 * k, 0), 'canopy': (0, by + hh, 0),
             'roots': (0, 0, -8), 'sap': (0, by + hh + 4, -6), 'seeds': (0, by + hh * 0.4, -6), 'mound': (0, 0, 0)}
    PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'legr': None, 'legl': None, 'canopy': 'head',
              'roots': None, 'sap': None, 'seeds': 'head', 'mound': None}
    R = Rig(f'sp{stage}_', 0.8, PIVOT, PARENT, FACES, opt=('roots', 'sap', 'seeds', 'mound'))
    for n, im in _tex(C, stage).items(): R.tex(n, im)
    for sfx, ch in SKINS.items():
        for n, im in _tex(dict(C, **ch), stage).items(): R.tex(n + sfx, im)
        R.skin(sfx, {n: n + sfx for n in _tex(C, stage)})
    B = R.box
    # body: a trunk, flaring at the foot (stage 1: hardly any - it's all seed-head)
    bw = {1: 1.6, 2: 1.5, 3: 2.6}[stage]
    B('body', (-bw, 1.2 * k, -bw * 0.85), (bw, by, bw * 0.85), 'bark')
    if stage >= 2:
        B('body', (-0.7, by - 3.2, -bw * 0.85 - 0.15), (0.7, by - 1.8, -bw * 0.85), 'gold', faces=('north',), light=10)   # (the pip, through a knot)
    if stage == 3:
        B('body', (-bw - 0.6, 1.0, -bw - 0.4), (bw + 0.6, 2.8, bw + 0.4), 'bark')                      # (the flare at the foot)
        B('body', (bw - 0.4, by - 0.4, -1.0), (bw + 1.4, by + 0.4, 1.0), 'stem')                          # (the Dryad's glow-mushroom, on its shoulder)
        B('body', (bw - 1.0, by + 0.4, -1.6), (bw + 2.0, by + 1.4, 1.6), 'mush', light=8)
    # head: a rounded burl with the face
    hw = hh * 0.58
    B('head', (-hw, by, -hw * 0.9), (hw, by + hh, hw * 0.9), 'bark')
    B('head', (-hw * 0.8, by + 0.4, -hw * 0.9 - 0.06), (hw * 0.8, by + hh - 0.4, -hw * 0.9), 'FACE', faces=('north',), uv={'north': [0, 0, 16, 16]})
    B('head', (-hw - 0.4, by + hh * 0.2, -hw * 0.7), (hw + 0.4, by + hh * 0.85, hw * 0.7), 'bark')
    top = by + hh
    if stage == 1:                                                                                          # two big cotyledon leaves, like ears
        for sx in (1, -1):
            R.box('head', (sx * 0.3 if sx > 0 else -4.6, top - 0.2, -1.6), (4.6 if sx > 0 else -0.3, top + 0.6, 1.6), 'leaf',
                  rot=('z', -sx * 28, (0, top, 0)))
        R.box('head', (-0.3, top - 0.5, -0.3), (0.3, top + 1.0, 0.3), 'leafdk' if False else 'leaf')
    elif stage == 2:                                                                                        # a tuft of five leaves
        for i, a in enumerate((-50, -25, 0, 25, 50)):
            R.box('head', (-0.9, top - 0.3, -0.4 + (i % 2) * 0.6), (0.9, top + 3.6 - abs(a) / 40, 0.4 + (i % 2) * 0.6), 'leaf', rot=('z', a, (0, top - 0.3, 0)))
    else:                                                                                                   # the canopy: a mop of leaves, an apple in it
        cy = top + 1.6
        blob(R, 'canopy', (0, cy, 0.4), 6.4, 'leaf', k=(1.15, 0.62, 1.0))
        blob(R, 'canopy', (-3.8, cy - 1.0, 1.4), 3.0, 'leaflt')
        blob(R, 'canopy', (3.6, cy + 0.6, 1.6), 3.2, 'leaf')
        for x in (-5.4, -2.2, 1.6, 5.0):                                                                    # (leaves hanging over the brow)
            B('canopy', (x - 1.0, top - 1.2, -6.3), (x + 1.0, top + 1.2, -4.8), 'leaf')
        B('canopy', (5.0, top - 2.6, -3.4), (5.3, top - 1.4, -3.1), 'barkdk')
        blob(R, 'canopy', (5.15, top - 3.7, -3.25), 1.25, 'gold', light=12)                              # (the golden apple, hanging)
    # arms: stage 1 leaf nubs; 2 twigs with leaf hands; 3 branches with twig fingers and leaf tufts
    for p, sx in (('armr', 1), ('arml', -1)):
        x, y, z = PIVOT[p]
        if stage == 1:
            R.box(p, (x - 0.5, y - 1.6, z - 0.4), (x + 0.5, y + 0.2, z + 0.4), 'leaf', rot=('z', sx * 30, (x, y, z)))
            continue
        L = 3.6 * k + (1.4 if stage == 3 else 0)
        e = (x + sx * L * 0.55, y - L * 0.85, z - 0.6)
        R.seg(p, (x, y, z), e, 0.8 * k + 0.2, 0.8 * k + 0.2, 'bark')
        if stage == 2:
            R.box(p, (e[0] - 0.9, e[1] - 1.6, e[2] - 0.3), (e[0] + 0.9, e[1] + 0.2, e[2] + 0.3), 'leaf')
        else:
            for a in (-30, 0, 30):
                R.seg(p, e, (e[0] + sx * 1.4 * math.sin(math.radians(a + 20)), e[1] - 1.6 * math.cos(math.radians(a)), e[2] - 0.6), 0.45, 0.45, 'barkdk')
            blob(R, p, (x + sx * L * 0.3, y - L * 0.4, z - 0.2), 1.0, 'leaf')
    # legs: roots - stage 1 two nubs; 2-3 splayed roots
    for p, sx in (('legr', 1), ('legl', -1)):
        x, y, z = PIVOT[p]
        R.box(p, (x - 0.7 * k - 0.2, 0, z - 0.8 * k - 0.4), (x + 0.7 * k + 0.2, y + 0.4, z + 0.8 * k + 0.2), 'root')
        if stage >= 2:
            for dx, dz in ((sx * 1.4, -1.6), (sx * 1.8, 0.6)):
                R.seg(p, (x, 0.6, z), (x + dx * k, 0.25, z + dz * k), 0.6, 0.5, 'root')
        if stage == 3:
            R.box(p, (x - 1.2, 0, z - 1.4), (x + 1.2, 0.7, z + 1.2), 'moss')
    # fx: the roots out of the ground (a ring, spiking up and in), the sap drop, the burst of pips; the planted mound
    for i in range(7):
        a = math.radians(i * 360 / 7); x, z = 4.6 * math.cos(a), -8 + 4.6 * math.sin(a)
        R.seg('roots', (x, -0.5, z), (x * 0.4, 7.0 + (i % 3), -8 + (z + 8) * 0.4), 1.2, 1.2, 'root')
    sx_, sy_, sz_ = PIVOT['sap']
    blob(R, 'sap', (sx_, sy_, sz_), 1.4, 'gold', light=14); B('sap', (sx_ - 0.5, sy_ + 1.2, sz_ - 0.5), (sx_ + 0.5, sy_ + 2.6, sz_ + 0.5), 'gold', light=14)
    for i in range(6):
        a = math.radians(i * 60); x, y = 3.0 * math.cos(a), PIVOT['seeds'][1] + 3.0 * math.sin(a)
        B('seeds', (x - 0.5, y - 0.5, -7.0), (x + 0.5, y + 0.5, -6.0), 'gold', light=10)
    B('mound', (-4.5, 0, -4.5), (4.5, 1.6, 4.5), 'earth'); B('mound', (-3.0, 1.6, -3.0), (3.0, 2.4, 3.0), 'earth')
    blob(R, 'mound', (0.6, 2.6, 0), 1.0, 'gold', light=10); B('mound', (-0.2, 2.4, -0.2), (0.2, 5.0, 0.2), 'leaf')
    B('mound', (-1.6, 4.6, -0.6), (0.0, 5.2, 0.6), 'leaf'); B('mound', (0.0, 4.2, -0.6), (1.4, 4.8, 0.6), 'leaf')

    # ---- poses
    def P(lift=0.0, **kw):
        return R.ground(kw, lift)
    W = lambda s: dict(legr=limb(1, 26 * s), legl=limb(-1, -26 * s), armr=limb(1, -22 * s, 14), arml=limb(-1, 22 * s, 14), body=T(4, 6 * s))
    R.POSES.update({
        'idle_a': P(armr=limb(1, 0, 14), arml=limb(-1, 0, 14), head=T(0, 0, 4)),
        'idle_b': P(_face='happy', armr=limb(1, 0, 60), arml=limb(-1, 0, 60), head=T(-6, 0, -6), lift=0.8 if stage == 1 else 0.0),   # (basking)
        'idle_c': P(_face='blink', armr=limb(1, 0, 10), arml=limb(-1, 0, 10), head=T(12, 0, 8), body=T(0, 0, 4)),                     # (swaying in a breeze)
        'walk_0': P(lift=1.0 if stage == 1 else 0.2, **W(1)), 'walk_1': P(**W(-1)),
        'sit_a': P(_face='happy', legr=limb(1, 85, 12), legl=limb(-1, 85, 12), armr=limb(1, 30, 10), arml=limb(-1, 30, 10)),
        'sit_b': P(_face='sleepy', _show=('roots',) if False else (), legr=limb(1, 85, 20), legl=limb(-1, 85, 20), head=T(16, 0, 10),
                   armr=limb(1, 10, 4), arml=limb(-1, 10, 4)),                                                                     # (dozing in the sun: it 'takes root')
        # ROOTSNARE: both arms swept down - roots burst up round the foe and hold it
        'snare': P(_face='focus', _show=('roots',), body=T(14), armr=limb(1, 60, -10), arml=limb(-1, 60, -10), legr=limb(1, -10), legl=limb(-1, 14)),
        # SEED SHOT: a little puff - golden pips from its leaves
        'seeds': P(_face='focus', _show=('seeds',), head=T(-14), body=T(-6), armr=limb(1, -20, 30), arml=limb(-1, -20, 30)),
        # GOLDEN SAP (heal): arms raised, a drop of golden sap over a friend
        'sap': P(_face='happy', _show=('sap',), armr=limb(1, 0, 150), arml=limb(-1, 0, 150), head=T(-16)),
        'hurt': P(_face='hurt', body=T(-14, 0, 8), head=T(-10), armr=limb(1, 20, 50), arml=limb(-1, 20, 50)),
    })
    R.POSES['planted'] = R.ground({'_show': ('mound',), '_hide': R.PARTS})
    R.DRAFT = ['idle_a', 'idle_b', 'walk_0', 'sit_a', 'sit_b', 'snare', 'seeds', 'sap', 'hurt']
    return R


RIGS = {s: make(s) for s in STAGES}
R = RIGS[3]                                                 # (the grown Tree Spirit: the doll, the figurine, the frame)
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'canopy': 'head'}
SHINY = 'Shiny Cherry Blossom'
