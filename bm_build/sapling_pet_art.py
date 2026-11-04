"""(3.1 draft, stage 1: art only - not wired) THE SAPLING (3rd pass: a full rework to the quality bar - see fol5_kit's notes).

Hand the Pale Dryad a Golden Apple by day while Kettle is out: she bites it, finds the golden pip, and plants it at your feet
("Kettle, water it - no, with the WATERING can"). A mound of earth with a golden pip in it stands where she planted it; it grows
over a few in-game days (as the Mireling does), and each stage follows you further than the last:

  STAGE 0  THE PLANTED PIP  (day 0)   a soft mound of dark earth, the golden pip half in it, a curled shoot with two baby leaves
                                      (a prop: right-click says "it's growing" and the day it'll be ready)
  STAGE 1  SPROUT           (day 1)   ankle-high (~0.5 blocks): a plump bean of a seed with a sweet face - big glossy amber eyes,
                                      a blush, a tiny smile - its golden seed-husk still on its head like a tipped beret, two fat
                                      cotyledon leaves sprouting up like ears, a new leaf-bud between them, leaf-nub hands, root
                                      toes. It hops.
  STAGE 2  SAPLING          (day 3)   knee-high (~0.85): a round burl head - its face set into a smooth heartwood plate under a
                                      carved bark brow - crowned by a rosette of curling leaves; a slender ridged trunk with the
                                      pip glowing gold in a knot on its chest; twig arms with three-leaf hands; root feet.
  STAGE 3  TREE SPIRIT      (day 5)   waist-high (~1.35): a big round heartwood face under a terraced canopy of leaves (a
                                      scalloped fringe over its brow, leaf tufts round the brim, the stage-1 sprout curl still
                                      on top), a GOLDEN APPLE hanging at its cheek like an earring; a tiered, ridged trunk with a
                                      moss collar, the glowing pip-knot and a shelf of the Dryad's blue glow-mushrooms; branch
                                      arms with forked twig fingers and leaf clusters; splayed, clawed, mossy roots.

RIG   each stage its own Rig with the same part names: body (the root), head (the face part - for the Sprout the bean is the
      head), crown (the cotyledons / leaf rosette / canopy: sways on its own), armr/arml + handr/handl (twig arms bend at the
      elbow), legr/legl (root feet); fx (opt, shown by _show): roots (Rootsnare), seeds (Seed Shot), sap (Golden Sap),
      aura (the rare Golden Bloom aura), mound (stage 0, on the Sprout's rig).
SKINS '_sh' the SHINY "Cherry Blossom" (pink blossom, dark cherry bark, a blush-pink heartwood, the apple ripened into a cherry);
      '_aut' the cosmetic "Autumn Crown" (amber, scarlet and gold leaves; per stage)."""
import math
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, bark, leaves, blade, glaze, glow, eye, blush, mouth, put,
                      slab, stack, ball, leaf, cleaf, chain, ring)

STAGES = (1, 2, 3)
FACES = ('happy', 'blink', 'focus', 'hurt', 'sleepy', 'surprised')
SKIN_NAMES = {'_sh': 'SHINY: Cherry Blossom', '_aut': 'cosmetic: Autumn Crown'}

C = dict(
    bark=('#5e5247', '#85776a', '#a99c8c', '#c7bba9'),          # pale oak: deep, dark, base, light
    root=('#56443a', '#76604f', '#937b66', '#ad977f'),
    heart=('#f3e5c9', '#fbf2df', '#e3cfac'),                      # heartwood: base, light, dark
    seed=('#ead3a4', '#f6e7c4', '#d9bd8a'),                       # the sprout's seed-coat
    leaf=('#3f7a3e', '#5f9e4c', '#82bf62', '#b7e08a'),            # rows: dark, base, light, tip
    blade=('#3d743a', '#62a24e', '#86c466'),                      # one leaf: dark, base, light (vein lighter)
    coty=('#5d9a4a', '#86c25e', '#a6d877'),                       # the cotyledons: plumper, paler
    gold=('#b8800e', '#efbd2c', '#ffdf6e', '#fff6cc'),            # the pip / apple: dark, base, light, shine
    husk=('#9c6c12', '#c99424', '#e6b843', '#f6d878'),
    moss=('#5b8a3e', '#79a94e', '#4c7534'),
    mush=('#4cb6ee', '#78d8ff', '#c9f4ff'), stem=('#f4ead6', '#fffaf0', '#e6d8bc'),
    earth=('#4a3628', '#5e4634', '#38281d'), pebble=('#8f8a80', '#a8a398', '#76726a'),
    iris=('#2e1a06', '#4e300c', '#7a4e12', '#b07e1e', '#dcae36', '#f4d670'),
    lash='#3a2412', mouth='#5a2c16', tongue='#e8847a', blush='#f2a08c', brow='#7a6050')
SKINS = {
    '_sh': dict(bark=('#3e1f22', '#5a2c30', '#76393c', '#94504f'), root=('#3a1e20', '#52292a', '#6a3634', '#844842'),
                heart=('#fde4e2', '#fff3f2', '#f2c8c6'), seed=('#f7d6d4', '#ffeaea', '#e8b8b8'),
                leaf=('#d0628e', '#f08ab0', '#ffb6d0', '#fff0f6'), blade=('#d0628e', '#f592b6', '#ffc0d8'),
                coty=('#e07aa0', '#ffa0c2', '#ffc8dc'), gold=('#8a0e24', '#d4243e', '#f45a6a', '#ffd0d4'),
                husk=('#8c3a52', '#b85674', '#d87896', '#f4b0c4'), moss=('#8aa04e', '#a8bc64', '#6e843c'),
                iris=('#3a0818', '#5e1028', '#8e1c40', '#c0365c', '#e8648a', '#ffa8c0'), blush='#ff8aa8'),
    '_aut': dict(leaf=('#8a2a12', '#c8501e', '#ee8a2a', '#ffc85a'), blade=('#9a3014', '#d8601e', '#f49a34'),
                 coty=('#b04a1a', '#e07c28', '#f8aa44'), moss=('#8a7a3a', '#a89448', '#6e602c'))}


# ---------------------------------------------------------------------------------------------------- textures
def _earth(c):
    deep, base, dark = c['earth']
    pt = [[(i * 7 + j * 3) % 5 for i in range(8)] for j in range(8)]
    def f(x, y, r):
        if (x * 5 + y * 3) % 23 == 0: return mix(base, '#8a6a4a', 0.5)          # (a lighter clod)
        if (x * 5 + y * 3) % 23 == 1: return dark
        k = pt[y // 4][x // 4]
        return deep if k == 0 else (dark if k == 1 and r.random() < 0.5 else base)
    return cells(f, 71)


def _seedcoat(c):
    base, light, dark = c['seed']
    def f(x, y, r):                                                               # (faint long grain, a soft sheen band)
        if x % 7 == 3 and r.random() < 0.75: return dark
        if 3 <= y <= 4 and x % 7 not in (3,): return light
        return light if r.random() < 0.05 else base
    return lit(cells(f, 72), 1.08, 0.93, 10)


def _heart(c):
    base, light, dark = c['heart']
    im = soft(base, light, dark, 73, 0.07)
    return lit(im, 1.04, 0.95, 10)


def _pip_knot(c):
    """the knot's rim: dark bark rings round a hollow"""
    deep, dark, base, light = c['bark']
    return cells(lambda x, y, r: deep if (x + y) % 5 == 0 else (dark if (x * 3 + y) % 4 else light), 74)


def _face(kind, c, stage):
    """the face plate: heartwood (the Sprout: its seed-coat), the blush, the mouth, brows when it frowns. The eyes are the
    overlay (_eyes). Layout per stage (texels from the top-left, 4 a unit): see EYES"""
    W, H, (lx, rx), ey, ew, eh = EYES[stage]
    base = _seedcoat(c) if stage == 1 else _heart(c)
    im = base.copy()
    by = ey + eh + 1; mx = int(W * 4) // 2
    if kind != 'hurt':
        blush(im, lx - ew // 2 - 0, by, 6 if stage > 1 else 5, c['blush'])
        blush(im, rx + ew // 2 + 0, by, 6 if stage > 1 else 5, c['blush'])
    if kind == 'focus':
        for x0, s in ((lx, 1), (rx, -1)):
            for i in range(4): put(im, x0 - s * 1 + s * i, ey - 2 + (i // 2), c['brow'])
    if kind == 'sad' or kind == 'hurt':
        for x0, s in ((lx, 1), (rx, -1)):
            for i in range(3): put(im, x0 + s * i, ey - 1 - (i // 2), c['brow'])
    my = by + (1 if stage == 1 else 2)
    mouth(im, mx, my, {None: 'smile', 'happy': 'open', 'blink': 'smile', 'focus': 'flat', 'hurt': 'wobble', 'sleepy': 'cat',
                       'surprised': 'o'}[kind], c['mouth'], c['tongue'], 4 if stage < 3 else 6)
    return im


def _eyes(kind, c, stage):
    """the eye overlay: glossy all-iris creature eyes (the stage-3 spirit gets a lash flick and a lid), amber like the pip"""
    W, H, (lx, rx), ey, ew, eh = EYES[stage]
    from PIL import Image
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    k = {'focus': 'fierce'}.get(kind, kind)
    for cx, fl in ((lx, False), (rx, True)):
        eye(im, cx, ey, ew, eh, fl, k, iris=c['iris'], lash=c['lash'], pupil='#1a0e04', sclera=False, irk=0.8)
    return im


# (W, H units of the face plate; eye centres; eye top row; eye w, h texels) - 4 texels a unit
EYES = {1: (6.0, 3.8, (7, 17), 2, 7, 8), 2: (6.0, 4.4, (7, 17), 3, 8, 9), 3: (7.2, 5.4, (8, 21), 4, 9, 10)}


def _textures(c, stage):
    t = {'bark': bark(c['bark'], 81, 4), 'barkf': bark(c['bark'], 82, 3, 1), 'root': bark(c['root'], 83, 3, 0),
         'heart': _heart(c), 'seed': _seedcoat(c),
         'leaf': leaves(c['leaf'], 84), 'leaft': lit(leaves(tuple(mix(v, '#ffffff', 0.12) for v in c['leaf']), 85), 1.06, 1.0, 6),
         'blade': blade(c['blade'], 86, rim='sides'), 'coty': blade(c['coty'], 87, rim='sides'),
         'gold': glaze(c['gold'], 88, 4), 'husk': leaves((c['husk'][0], c['husk'][1], c['husk'][2], c['husk'][3]), 89),
         'moss': soft(c['moss'][1], c['moss'][0], c['moss'][2], 90, 0.22), 'stem': soft(*c['stem'], 91, 0.1),
         'mush': soft(c['mush'][0], c['mush'][1], mix(c['mush'][0], '#2a7ab8', 0.4), 92, 0.2),
         'mushlt': soft(c['mush'][1], c['mush'][2], c['mush'][0], 93, 0.2), 'knot': _pip_knot(c),
         'green': soft(c['blade'][1], c['blade'][2], c['blade'][0], 94, 0.12),
         'earth': _earth(c), 'pebble': soft(*c['pebble'], 95, 0.2),
         'pipglow': glow((c['gold'][3], c['gold'][2], c['gold'][1]), 16),
         'sap': glow(('#fff6cc', '#ffe070', '#f4bc2c', '#d89a14'), 16), 'sapa': glow(('#fff6cc', '#ffe070', '#f8c84a'), 16, alpha=(200, 150, 90)),
         'petal': soft('#ffe58a', '#fff6cc', '#f2c040', 96, 0.25)}
    t['face'] = _face(None, c, stage); t['eyes'] = _eyes(None, c, stage)
    for f in FACES:
        t[f'face_{f}'] = _face(f, c, stage); t[f'eyes_{f}'] = _eyes(f, c, stage)
    return t


# ---------------------------------------------------------------------------------------------------- shared pieces
def _face_plate(R, stage, y0, z, x0=None):
    """the face plate and its eye overlay on the head's front at z (the slab's front face)"""
    W, H = EYES[stage][:2]; x0 = -W / 2 if x0 is None else x0
    R.box('head', (x0, y0, z - 0.02), (x0 + W, y0 + H, z), 'FACE', faces=('north',), uv={'north': [0, 0, W, H]})
    R.box('head', (x0, y0, z - 0.05), (x0 + W, y0 + H, z - 0.03), 'EYES', faces=('north',), uv={'north': [0, 0, W, H]}, light=5)


def _roots_fx(R, z0=-9.0, n=7, r=4.2, h=7.5):
    """ROOTSNARE: a ring of roots bursting out of the ground round the foe (in front), curling up and in over it"""
    for i in range(n):
        a = math.radians(i * 360 / n + 10); x, z = r * math.cos(a), z0 + r * math.sin(a)
        hh = h * (0.8 + 0.25 * ((i * 3) % 4) / 3)
        pts = [(x, 0.0, z), (x * 0.95, hh * 0.45, z0 + (z - z0) * 0.95), (x * 0.6, hh * 0.85, z0 + (z - z0) * 0.6), (x * 0.25, hh, z0 + (z - z0) * 0.25)]
        chain(R, 'roots', pts, [1.5, 1.1, 0.75, 0.35], 'root')
        R.box('roots', (x - 1.1, 0.0, z - 1.1), (x + 1.1, 0.35, z + 1.1), 'earth')                       # (the earth it tore up)
    for i in range(5):                                                                                       # (clods flung out)
        a = math.radians(i * 72 + 30); x, z = (r + 2.2) * math.cos(a), z0 + (r + 2.2) * math.sin(a)
        R.box('roots', (x - 0.4, 0.8 + i % 2, z - 0.4), (x + 0.4, 1.5 + i % 2, z + 0.4), 'earth')


def _aura(R, cy, r=7.0):
    """the rare GOLDEN BLOOM aura: gold petals and motes spiralling up round it (light 12)"""
    for i in range(12):
        a = math.radians(i * 47); y = cy * (0.15 + 0.07 * i)
        x, z = r * math.cos(a) * (0.9 + 0.1 * (i % 3)), r * math.sin(a) * (0.9 + 0.1 * (i % 3))
        R.box('aura', (x - 0.55, y, z - 0.3), (x + 0.55, y + 0.22, z + 0.3), 'petal', rot=('y', (i * 37) % 90 - 45, (x, y, z)), light=12)
        if i % 2: R.box('aura', (x * 0.8 - 0.2, y + 1.5, z * 0.8 - 0.2), (x * 0.8 + 0.2, y + 1.9, z * 0.8 + 0.2), 'sap', light=14, full=True)


# ---------------------------------------------------------------------------------------------------- the stages
def _rig(stage, pivot, parent):
    R = Rig(f'sp{stage}_', 0.8, pivot, parent, FACES, opt=('roots', 'seeds', 'sap', 'aura', 'mound'))
    base = _textures(C, stage)
    for n, im in base.items(): R.tex(n, im)
    for sfx, ch in SKINS.items():
        sk = _textures(dict(C, **ch), stage)
        for n, im in sk.items(): R.tex(n + sfx, im)
        R.skin(sfx, {n: n + sfx for n in base})
    return R


def sprout():
    """STAGE 1: a plump seed-bean, ~0.5 blocks to the tips of its cotyledons"""
    PIV = {'body': (0, 1.2, 0), 'head': (0, 1.2, 0), 'crown': (0, 7.6, -0.4), 'armr': (3.9, 4.6, -0.2), 'handr': (3.9, 4.6, -0.2),
           'arml': (-3.9, 4.6, -0.2), 'handl': (-3.9, 4.6, -0.2), 'legr': (1.6, 1.4, 0), 'legl': (-1.6, 1.4, 0),
           'roots': (0, 0, -9), 'seeds': (0, 6, -4), 'sap': (0, 10, -7), 'aura': (0, 0, 0), 'mound': (0, 0, 0)}
    PAR = {'body': None, 'head': 'body', 'crown': 'head', 'armr': 'head', 'handr': 'armr', 'arml': 'head', 'handl': 'arml',
           'legr': 'body', 'legl': 'body', 'roots': None, 'seeds': 'head', 'sap': None, 'aura': None, 'mound': None}
    R = _rig(1, PIV, PAR)
    # the bean: a plump capsule of slabs, its face on the flat of the wide band
    rows = [(1.0, 1.7, 2.9, 2.5), (1.7, 2.5, 3.8, 3.2), (2.5, 6.4, 4.2, 3.5), (6.4, 7.1, 3.8, 3.2), (7.1, 7.7, 2.9, 2.5)]
    stack(R, 'head', rows, 'seed', shift=False)
    _face_plate(R, 1, 2.6, -3.5)
    # the seed-husk: a golden cup tipped back on its head like a beret, a scalloped rim, a little stalk
    rot = ('x', 22, (0, 7.6, 0.6))
    for (y0, y1, w) in ((7.2, 7.9, 3.3), (7.9, 8.5, 3.0), (8.5, 9.0, 2.3), (9.0, 9.3, 1.3)):
        slab(R, 'head', y0, y1, w, 'husk', w * 0.92, c=(0, 0.9), rot=rot)
    for i in range(10):
        a = math.radians(i * 36 + 18); x, z = 3.15 * math.cos(a), 0.9 + 2.9 * math.sin(a)
        R.box('head', (x - 0.45, 6.85, z - 0.45), (x + 0.45, 7.3, z + 0.45), 'husk', rot=rot)
    R.box('head', (-0.25, 9.3, 0.7), (0.25, 10.0, 1.2), 'root', rot=rot)
    # the shoot: a green stem out of the front of the husk, two fat cotyledons like ears, a new leaf-bud between them
    R.seg('crown', (0, 7.4, -0.5), (0.15, 9.6, -0.8), 0.7, 0.7, 'green')
    for sx in (1, -1):
        cleaf(R, 'crown', (0.15 * sx, 9.5, -0.8), (sx * 1.0, 0.42, 0.05), 5.0, 3.0, 'coty', droop=0.16, t=0.55, tipw=0.62, base=0.35)
    cleaf(R, 'crown', (0.1, 9.6, -0.8), (0.25, 1.0, -0.25), 2.2, 1.1, 'blade', droop=0.05, t=0.25)
    cleaf(R, 'crown', (0.1, 9.6, -0.8), (-0.35, 1.0, 0.2), 1.7, 0.9, 'blade', droop=0.08, t=0.25)
    # leaf-nub hands
    for sx, p in ((1, 'armr'), (-1, 'arml')):
        x = PIV[p][0]
        cleaf(R, p, (x, 4.6, -0.2), (sx * 0.7, -0.5, -0.5), 2.0, 1.5, 'blade', droop=0.1, t=0.35, tipw=0.4)
    # root feet: a nub, three root toes
    for sx, p in ((1, 'legr'), (-1, 'legl')):
        x = PIV[p][0]
        R.box(p, (x - 0.9, 0.3, -0.9), (x + 0.9, 1.5, 0.9), 'root')
        R.box(p, (x - 0.65, 0.0, -0.65), (x + 0.65, 0.3, 0.65), 'root')
        for dx, dz in ((0.2, -2.1), (1.6, -1.2), (0.9, 1.3)):
            chain(R, p, [(x, 0.45, 0), (x + sx * dx * 0.6, 0.3, dz * 0.6), (x + sx * dx, 0.12, dz)], [0.8, 0.55, 0.3], 'root', hs=[0.6, 0.4, 0.24])
    # fx
    _roots_fx(R, -9.0, 6, 3.4, 5.5)
    for i, (x, y, z) in enumerate(((0.4, 6.4, -5.2), (-0.6, 6.8, -8.0), (0.2, 6.2, -11.0))):
        R.box('seeds', (x - 0.55 + i * 0.1, y - 0.45, z - 0.6), (x + 0.55 - i * 0.1, y + 0.45, z + 0.6), 'gold', light=10)
        R.box('seeds', (x - 0.2, y - 0.15, z + 0.6), (x + 0.2, y + 0.15, z + 2.2 - i * 0.3), 'sapa', light=12, full=True)    # (a streak)
    _sap_fx(R, PIV['sap'], 0.8)
    _aura(R, 10.0, 6.0)
    # STAGE 0: the planted pip in its mound
    stack(R, 'mound', [(0.0, 0.7, 4.6, 4.1), (0.7, 1.4, 3.9, 3.4), (1.4, 1.9, 2.8, 2.4), (1.9, 2.2, 1.6, 1.4)], 'earth')
    ball(R, 'mound', (0.5, 2.2, -0.3), 0.95, 'gold', 3, ry=0.8, light=10)
    R.seg('mound', (0.2, 2.0, -0.2), (-0.1, 3.4, -0.4), 0.42, 0.42, 'green')
    R.seg('mound', (-0.1, 3.4, -0.4), (0.4, 4.0, -0.6), 0.38, 0.38, 'green')
    cleaf(R, 'mound', (0.4, 3.9, -0.6), (1.0, 0.35, -0.1), 1.6, 1.1, 'coty', droop=0.1, t=0.3, tipw=0.6)
    cleaf(R, 'mound', (0.4, 3.9, -0.6), (-1.0, 0.45, 0.1), 1.4, 1.0, 'coty', droop=0.1, t=0.3, tipw=0.6)
    for x, z, s in ((-3.2, -2.0, 0.55), (2.9, 2.2, 0.45), (-2.4, 2.8, 0.35)):
        ball(R, 'mound', (x, 0.9 + s * 0.4, z), s, 'pebble', 2)
    for x, z in ((3.4, -1.6), (-3.7, 0.8)):                                                                # (tufts of grass)
        for j in range(3): R.seg('mound', (x, 0.5, z), (x + (j - 1) * 0.45, 1.8 + 0.3 * (j % 2), z - 0.3), 0.22, 0.22, 'green')
    return R, PIV


def _sap_fx(R, c, k=1.0):
    """GOLDEN SAP: a fat golden drop over a friend, a glow round it, two drips falling"""
    x, y, z = c
    ball(R, 'sap', (x, y, z), 1.5 * k, 'gold', 4, light=14)
    R.box('sap', (x - 0.45 * k, y + 1.3 * k, z - 0.45 * k), (x + 0.45 * k, y + 2.4 * k, z + 0.45 * k), 'gold', light=14)
    R.box('sap', (x - 0.2, y + 2.3 * k, z - 0.2), (x + 0.2, y + 2.8 * k, z + 0.2), 'gold', light=14)
    R.box('sap', (x - 2.6 * k, y - 2.6 * k, z), (x + 2.6 * k, y + 2.6 * k, z + 0.02), 'sapa', faces=('north', 'south'), full=True, light=15)
    for dx, dy in ((-0.7, -3.0), (0.8, -4.6)):
        R.box('sap', (x + dx - 0.3, y + dy * k - 0.5, z - 0.3), (x + dx + 0.3, y + dy * k + 0.3, z + 0.3), 'gold', light=14)


def sapling():
    """STAGE 2: ~0.85 blocks - a burl head with a leaf rosette, a slender ridged trunk, twig arms, root feet"""
    PIV = {'body': (0, 3.4, 0), 'head': (0, 8.7, 0), 'crown': (0, 15.0, 0.2), 'armr': (1.9, 7.9, 0), 'handr': (3.5, 6.1, -0.3),
           'arml': (-1.9, 7.9, 0), 'handl': (-3.5, 6.1, -0.3), 'legr': (1.2, 3.5, 0), 'legl': (-1.2, 3.5, 0),
           'roots': (0, 0, -9), 'seeds': (0, 15.5, -3), 'sap': (0, 16, -8), 'aura': (0, 0, 0), 'mound': (0, 0, 0)}
    PAR = {'body': None, 'head': 'body', 'crown': 'head', 'armr': 'body', 'handr': 'armr', 'arml': 'body', 'handl': 'arml',
           'legr': 'body', 'legl': 'body', 'roots': None, 'seeds': 'crown', 'sap': None, 'aura': None, 'mound': None}
    R = _rig(2, PIV, PAR)
    # legs: short root stumps, three root toes splayed on the ground
    for sx, p in ((1, 'legr'), (-1, 'legl')):
        x = PIV[p][0]
        stack(R, p, [(0.0, 0.5, 1.25, 1.15), (0.5, 2.2, 0.95, 0.9), (2.2, 3.7, 0.8, 0.75)], 'root', c=(x, 0))
        for dx, dz in ((0.1, -2.3), (1.9, -0.9), (0.7, 1.7)):
            chain(R, p, [(x, 0.7, 0), (x + sx * dx * 0.55, 0.42, dz * 0.55), (x + sx * dx, 0.14, dz)], [0.95, 0.65, 0.3], 'root', hs=[0.7, 0.45, 0.26])
    # the trunk: a slender taper, flared at the foot; raised ridges; the pip glowing in a knot on its chest
    stack(R, 'body', [(3.2, 4.0, 2.4, 2.0), (4.0, 4.9, 2.0, 1.7), (4.9, 6.9, 1.7, 1.45), (6.9, 8.3, 1.95, 1.6), (8.3, 8.9, 1.55, 1.3)], 'barkf')
    for x, z, y0, y1 in ((-1.05, -1.5, 3.4, 7.6), (1.15, -1.5, 3.6, 6.2), (1.85, 0.0, 3.5, 8.0), (-1.85, 0.3, 3.3, 7.2), (0.2, 1.6, 3.4, 8.1)):
        if abs(z) > 1: R.box('body', (x - 0.22, y0, z - 0.12 * (1 if z < 0 else -1)), (x + 0.22, y1, z), 'bark')
        else: R.box('body', (x - 0.12 * (1 if x > 0 else -1), y0, z - 0.22), (x, y1, z + 0.22), 'bark')
    _knot(R, 'body', 6.6, -1.6, 1.35, 9)
    # the head: a round burl; the face on a heartwood plate under a carved bark brow
    stack(R, 'head', [(8.6, 9.3, 3.3, 2.8), (9.3, 13.9, 4.2, 3.5), (13.9, 14.6, 3.6, 3.0), (14.6, 15.2, 2.6, 2.2)], 'bark')
    _face_plate(R, 2, 9.4, -3.5)
    _brow(R, 3.05, 13.55, -3.5, 0.55)
    R.box('head', (-3.05, 9.0, -3.62), (3.05, 9.4, -3.5), 'bark')                                             # (the chin lip)
    # a side twig off its head (its left) with one leaf - a little asymmetry
    R.seg('head', (-3.9, 12.6, 0.4), (-5.4, 13.9, 0.6), 0.45, 0.45, 'bark')
    cleaf(R, 'head', (-5.4, 13.9, 0.6), (-0.6, 0.6, -0.4), 2.2, 1.4, 'blade', droop=0.2, t=0.25)
    # the crown: a rosette of curling leaves - six round the rim, two tall in the middle, two dipping over the brow
    for i in range(6):
        a = math.radians(i * 60 + 30); d = (math.cos(a), 0.85, math.sin(a))
        cleaf(R, 'crown', (0.4 * math.cos(a), 15.0, 0.2 + 0.4 * math.sin(a)), d, 4.4, 2.0, 'blade', droop=0.32, t=0.3)
    cleaf(R, 'crown', (0.1, 15.1, 0.2), (0.25, 1.0, 0.15), 4.2, 1.8, 'blade', droop=0.14, t=0.3)
    cleaf(R, 'crown', (-0.1, 15.1, 0.3), (-0.35, 1.0, 0.35), 3.4, 1.6, 'blade', droop=0.18, t=0.3)
    for sx in (1, -1):
        cleaf(R, 'crown', (sx * 0.8, 15.0, -1.2), (sx * 0.55, 0.4, -1.0), 3.0, 1.5, 'blade', droop=0.45, t=0.28)
    R.seg('crown', (0, 14.7, 0.2), (0, 15.4, 0.2), 0.8, 0.8, 'green')
    # twig arms: an upper twig, a forearm twig, three leaves for fingers
    for sx, a, h in ((1, 'armr', 'handr'), (-1, 'arml', 'handl')):
        ax, ay, az = PIV[a]; hx, hy, hz = PIV[h]
        R.seg(a, (ax, ay, az), (hx, hy, hz), 0.75, 0.75, 'bark', ext=0.2)
        e = (hx + sx * 0.9, hy - 1.5, hz - 0.4)
        R.seg(h, (hx, hy, hz), e, 0.6, 0.6, 'bark', ext=0.1)
        for d in ((sx * 0.5, -1.0, -0.3), (sx * 1.0, -0.4, -0.1), (sx * 0.2, -0.8, -0.9)):
            cleaf(R, h, e, d, 1.6, 0.9, 'blade', droop=0.12, t=0.22)
    # fx
    _roots_fx(R, -9.0, 7, 4.0, 7.0)
    for i, (x, y, z) in enumerate(((0.4, 16.2, -4.5), (-0.5, 16.6, -7.5), (0.3, 16.0, -10.5))):
        R.box('seeds', (x - 0.6, y - 0.5, z - 0.65), (x + 0.6, y + 0.5, z + 0.65), 'gold', light=10)
        R.box('seeds', (x - 0.22, y - 0.18, z + 0.65), (x + 0.22, y + 0.18, z + 2.6), 'sapa', light=12, full=True)
    _sap_fx(R, PIV['sap'], 1.0)
    _aura(R, 17.0, 7.0)
    return R, PIV


def _knot(R, part, y, z, r, light):
    """a knot in the bark on the front at height y: a dark rim of four boxes a hair proud, the golden pip glowing in it"""
    R.box(part, (-r, y - r, z - 0.2), (r, y - r + 0.45, z + 0.1), 'knot')
    R.box(part, (-r, y + r - 0.45, z - 0.2), (r, y + r, z + 0.1), 'knot')
    R.box(part, (-r, y - r + 0.45, z - 0.2), (-r + 0.45, y + r - 0.45, z + 0.1), 'knot')
    R.box(part, (r - 0.45, y - r + 0.45, z - 0.2), (r, y + r - 0.45, z + 0.1), 'knot')
    R.box(part, (-r + 0.45, y - r + 0.45, z + 0.05), (r - 0.45, y + r - 0.45, z + 0.12), 'knot', faces=('north',))
    R.box(part, (-r * 0.45, y - r * 0.45, z - 0.05), (r * 0.45, y + r * 0.45, z + 0.12), 'gold', light=light)
    R.box(part, (-r * 0.6, y - r * 0.6, z - 0.03), (r * 0.6, y + r * 0.6, z - 0.02), 'pipglow', faces=('north',), full=True, light=light)


def _brow(R, w, y, z, h):
    """a carved bark brow over the face plate: a ledge a little proud, its ends stepping down the sides of the face"""
    R.box('head', (-w, y, z - 0.18), (w, y + h, z), 'bark')
    for sx in (1, -1):
        a, b = sorted((sx * w, sx * (w - 0.45)))
        R.box('head', (a, y - 1.6, z - 0.12), (b, y, z), 'bark')


def spirit():
    """STAGE 3: the Tree Spirit, ~1.35 blocks to the top of its canopy"""
    PIV = {'body': (0, 4.6, 0), 'head': (0, 12.2, 0), 'crown': (0, 19.4, 0.5), 'armr': (2.9, 11.1, 0), 'handr': (5.3, 8.7, -0.4),
           'arml': (-2.9, 11.1, 0), 'handl': (-5.3, 8.7, -0.4), 'legr': (1.9, 4.7, 0), 'legl': (-1.9, 4.7, 0),
           'roots': (0, 0, -10), 'seeds': (0, 18, -5), 'sap': (0, 22, -9), 'aura': (0, 0, 0), 'mound': (0, 0, 0)}
    PAR = {'body': None, 'head': 'body', 'crown': 'head', 'armr': 'body', 'handr': 'armr', 'arml': 'body', 'handl': 'arml',
           'legr': 'body', 'legl': 'body', 'roots': None, 'seeds': 'head', 'sap': None, 'aura': None, 'mound': None}
    R = _rig(3, PIV, PAR)
    # roots: a mossy stump on each side, four clawed roots arching to the ground
    for sx, p in ((1, 'legr'), (-1, 'legl')):
        x = PIV[p][0]
        stack(R, p, [(0.6, 1.6, 1.7, 1.55), (1.6, 3.4, 1.4, 1.3), (3.4, 5.0, 1.25, 1.15)], 'root', c=(x, 0))
        slab(R, p, 1.55, 1.95, 1.55, 'moss', 1.42, c=(x, 0))
        for dx, dz, L in ((0.2, -3.0, 1.0), (2.4, -1.9, 0.9), (3.0, 0.6, 0.85), (1.0, 2.6, 0.8)):
            pts = [(x + sx * dx * 0.15, 1.6, dz * 0.15), (x + sx * dx * 0.55, 1.25, dz * 0.55), (x + sx * dx * 0.88, 0.55, dz * 0.88), (x + sx * dx * 1.0, 0.0, dz * 1.0)]
            chain(R, p, pts, [1.25 * L, 0.95 * L, 0.6 * L, 0.3], 'root', hs=[1.0 * L, 0.75 * L, 0.5 * L, 0.25])
        R.box(p, (x + sx * 1.0 - 0.5, 1.4, -1.9), (x + sx * 1.0 + 0.5, 1.75, -1.2), 'moss')
    # the trunk: tiered - a flared foot, a waist, the chest; raised ridges, a moss collar, the pip-knot, glow-mushrooms
    stack(R, 'body', [(4.3, 5.4, 3.4, 2.9), (5.4, 6.9, 2.9, 2.5), (6.9, 10.0, 2.6, 2.25), (10.0, 11.6, 3.0, 2.55), (11.6, 12.4, 2.5, 2.1)], 'barkf')
    for x, z, y0, y1 in ((-1.35, -2.3, 4.6, 9.6), (1.5, -2.3, 4.8, 8.2), (2.7, 0.0, 4.5, 11.0), (-2.7, 0.4, 4.4, 10.4), (0.3, 2.3, 4.5, 11.2), (-1.4, 2.3, 4.8, 9.0)):
        if abs(z) > 1: R.box('body', (x - 0.25, y0, min(z, z - 0.14 * (1 if z < 0 else -1))), (x + 0.25, y1, max(z, z - 0.14 * (1 if z < 0 else -1))), 'bark')
        else:
            a, b = sorted((x, x + 0.14 * (1 if x > 0 else -1))); R.box('body', (a, y0, z - 0.25), (b, y1, z + 0.25), 'bark')
    slab(R, 'body', 11.3, 12.15, 3.25, 'moss', 2.8)
    for i in range(8):                                                                                       # (moss tufts hanging off the collar)
        a = math.radians(i * 45 + 20); x, z = 3.0 * math.cos(a), 2.6 * math.sin(a)
        R.box('body', (x - 0.45, 10.6 + 0.3 * (i % 2), z - 0.45), (x + 0.45, 11.4, z + 0.45), 'moss')
    _knot(R, 'body', 8.4, -2.25, 1.45, 10)
    for y, w, d in ((6.6, 2.1, 1.7), (7.9, 1.6, 1.3), (9.0, 1.0, 0.8)):                                       # (the Dryad's glow-mushrooms, a shelf)
        R.box('body', (-2.6 - w, y, -0.6 - d * 0.5), (-2.5, y + 0.42, -0.6 + d * 0.5), 'mush', light=8)
        R.box('body', (-2.6 - w * 0.72, y + 0.42, -0.6 - d * 0.35), (-2.5, y + 0.62, -0.6 + d * 0.35), 'mushlt', light=8)
        R.box('body', (-2.6 - w + 0.2, y - 0.12, -0.6 - d * 0.42), (-2.5, y, -0.6 + d * 0.42), 'stem')
    # the head: big and round; the heartwood face under a carved brow
    stack(R, 'head', [(12.2, 12.9, 4.0, 3.4), (12.9, 18.7, 5.0, 4.2), (18.7, 19.4, 4.4, 3.7), (19.4, 19.9, 3.4, 2.9)], 'bark')
    _face_plate(R, 3, 13.1, -4.2)
    _brow(R, 3.6, 18.35, -4.2, 0.55)
    R.box('head', (-3.6, 12.7, -4.34), (3.6, 13.1, -4.2), 'bark')
    for sx in (1, -1):                                                                                       # (knobbly cheeks: a burl each side)
        slab(R, 'head', 13.8, 16.6, 0.9, 'bark', 1.3, c=(sx * 4.75, -0.6))
    # the canopy: a terraced dome of leaves, set back a little; lighter leaves on each terrace's top
    rows = [(18.8, 20.0, 6.6, 5.9), (20.0, 21.4, 7.3, 6.5), (21.4, 22.7, 7.0, 6.2), (22.7, 23.8, 6.1, 5.4), (23.8, 24.7, 4.8, 4.2), (24.7, 25.3, 3.2, 2.8)]
    stack(R, 'crown', rows, 'leaf', c=(0, 0.6), top='leaft')
    # bumps on the dome (leaf clumps a little proud), so the outline isn't a stepped cake
    for x, y, z, r in ((4.6, 22.6, -3.2, 1.6), (-4.8, 22.2, -2.6, 1.7), (5.6, 21.6, 2.6, 1.6), (-5.4, 21.8, 3.0, 1.7), (2.0, 24.6, -2.2, 1.5),
                       (-2.6, 24.4, 2.4, 1.5), (0.3, 22.6, 6.4, 1.6), (-1.2, 23.4, -4.4, 1.4)):
        ball(R, 'crown', (x, y, z), r, 'leaf', 3, ry=r * 0.8, top='leaft')
    # the fringe over its brow: leaf tips hanging, alternating lengths; tufts all round the brim
    for i in range(8):
        x = -5.2 + i * 1.48; ln = 1.5 if i % 2 else 2.3
        cleaf(R, 'crown', (x, 19.4, -5.6), (0.1 * (x / 5), -1.0, -0.35), ln, 1.55, 'blade', droop=0.0, t=0.3, tipw=0.35)
    for i in range(14):
        a = math.radians(i * 360 / 14 + 8)
        if -0.9 < math.sin(a) < -0.45 and abs(math.cos(a)) < 0.6: continue                                 # (not in front of the face)
        x, z = 6.9 * math.cos(a), 0.6 + 6.2 * math.sin(a)
        cleaf(R, 'crown', (x, 19.6, z), (math.cos(a), -0.55, math.sin(a)), 2.6, 1.7, 'blade', droop=0.25, t=0.3)
    # on top: the sprout's curl, still there
    R.seg('crown', (0.2, 25.2, 0.6), (0.5, 26.6, 0.3), 0.5, 0.5, 'green')
    for sx in (1, -1):
        cleaf(R, 'crown', (0.5, 26.5, 0.3), (sx * 1.0, 0.45, 0.0), 2.2, 1.4, 'coty', droop=0.15, t=0.35, tipw=0.6)
    # the golden apple, hanging at its cheek: a twig from the brim, a stem, a leaf, the apple (glowing)
    R.seg('crown', (5.4, 19.4, -3.3), (5.8, 18.1, -3.7), 0.4, 0.4, 'bark')
    ball(R, 'crown', (5.85, 16.6, -3.75), 1.45, 'gold', 4, ry=1.35, light=10)
    R.box('crown', (5.6, 17.85, -4.0), (6.1, 18.2, -3.5), 'root')
    cleaf(R, 'crown', (5.85, 18.1, -3.75), (-0.8, 0.5, -0.4), 1.6, 1.0, 'blade', droop=0.1, t=0.22)
    # branch arms: an upper branch, the forearm, three forked twig fingers; leaf clusters at the elbow and the hand
    for sx, a, h in ((1, 'armr', 'handr'), (-1, 'arml', 'handl')):
        ax, ay, az = PIV[a]; hx, hy, hz = PIV[h]
        chain(R, a, [(ax - sx * 0.3, ay + 0.3, az), (hx, hy, hz)], [1.35, 1.0], 'bark')
        slab(R, a, ay - 0.1, ay + 0.75, 1.3, 'moss', 1.1, c=(ax - sx * 0.3, az))                         # (a moss pad on the shoulder)
        e = (hx + sx * 1.1, hy - 2.0, hz - 0.5)
        chain(R, h, [(hx, hy, hz), e], [0.95, 0.75], 'bark')
        for d, L in (((sx * 0.4, -1.0, -0.5), 1.6), ((sx * 1.0, -0.5, 0.0), 1.5), ((sx * 0.0, -0.9, -1.0), 1.3)):
            m = math.sqrt(sum(v * v for v in d)); tip = tuple(e[i] + d[i] / m * L for i in range(3))
            chain(R, h, [e, tip], [0.5, 0.26], 'bark')
        ball(R, h, (hx + sx * 0.2, hy - 0.3, hz + 0.5), 0.9, 'leaf', 3, top='leaft')
        cleaf(R, h, (hx + sx * 0.2, hy - 0.1, hz + 0.4), (sx * 0.6, 0.3, 0.8), 1.8, 1.1, 'blade', droop=0.2, t=0.25)
        ball(R, a, (ax + sx * 1.3, ay - 1.0, az + 0.7), 0.8, 'leaf', 3, top='leaft')
    # fx
    _roots_fx(R, -10.0, 8, 4.8, 9.0)
    for i, (x, y, z) in enumerate(((0.5, 19.0, -7.0), (-0.6, 19.6, -10.0), (0.4, 18.8, -13.0))):
        R.box('seeds', (x - 0.65, y - 0.55, z - 0.7), (x + 0.65, y + 0.55, z + 0.7), 'gold', light=10)
        R.box('seeds', (x - 0.24, y - 0.2, z + 0.7), (x + 0.24, y + 0.2, z + 3.0), 'sapa', light=12, full=True)
    _sap_fx(R, PIV['sap'], 1.2)
    _aura(R, 24.0, 8.5)
    return R, PIV


# ---------------------------------------------------------------------------------------------------- poses
def _poses(R, stage):
    k = {1: 1.0, 2: 1.0, 3: 0.85}[stage]
    def P(lift=0.0, **kw):
        return R.ground(kw, lift)
    hop = stage == 1
    def W(s):
        if hop:                                                                                              # (the Sprout hops: squash and lift)
            return dict(head=T(6 * s, 0, 4 * s), legr=limb(1, 20 * s), legl=limb(-1, 20 * s), armr=limb(1, 0, 30), arml=limb(-1, 0, 30),
                        crown=T(-14 * s, 0, 6 * s))
        return dict(legr=limb(1, 24 * s * k), legl=limb(-1, -24 * s * k), armr=limb(1, -26 * s, 4), arml=limb(-1, 26 * s, 4),
                    handr=limb(1, -10), handl=limb(-1, -10), body=T(4, 7 * s), head=T(-2, -5 * s), crown=T(0, 0, 4 * s))
    up = lambda a: dict(armr=limb(1, 0, a), arml=limb(-1, 0, a))
    R.POSES.update({
        'idle_a': P(head=T(0, 0, 4), crown=T(0, 0, -3), **up(6)),
        'idle_b': P(_face='happy', head=T(-8, 0, -5), crown=T(-6, 0, 4), armr=limb(1, 0, 70), arml=limb(-1, 0, 70),
                    handr=limb(1, 0, 20), handl=limb(-1, 0, 20)),                                              # (basking in the sun)
        'idle_c': P(_face='blink', head=T(6, 0, 9), body=T(0, 0, 4), crown=T(0, 0, -10), **up(10)),          # (swaying in a breeze)
        'walk_0': P(lift=1.2 if hop else 0.0, **W(1)), 'walk_1': P(**W(-1)),
        'sit_a': P(_face='happy', _o_body=(0, -1.2 if stage > 1 else -0.6, 0), legr=limb(1, 80, 14), legl=limb(-1, 80, 14),
                   armr=limb(1, 35, 8), arml=limb(-1, 35, 8), handr=limb(1, 20), handl=limb(-1, 20), head=T(-6, 0, 6)),
        # (taking root: it settles, eyes shut, roots in the soil, the crown droops and it sleeps the night through)
        'sit_b': P(_face='sleepy', _o_body=(0, -1.4 if stage > 1 else -0.7, 0), legr=limb(1, 0, 34), legl=limb(-1, 0, 34),
                   head=T(14, 0, 9), crown=T(10, 0, 8), armr=limb(1, 6, 2), arml=limb(-1, 6, 2), handr=limb(1, 10), handl=limb(-1, 10)),
        # ROOTSNARE: it stamps and sweeps both arms down; roots burst up round the foe and hold it
        'snare': P(_face='focus', _show=('roots',), body=T(12), head=T(-8), armr=limb(1, 55, 20), arml=limb(-1, 55, 20),
                   handr=limb(1, 30), handl=limb(-1, 30), legr=limb(1, -8), legl=limb(-1, 14), crown=T(12)),
        # SEED SHOT: a flick of the crown - golden pips shot from its leaves
        'seeds': P(_face='focus', _show=('seeds',), head=T(-6 if stage == 3 else 18), body=T(-4), crown=T(28 if stage < 3 else 8),
                   armr=limb(1, -30, 24), arml=limb(-1, -30, 24)),
        # GOLDEN SAP: arms up, a drop of golden sap over a friend (a heal)
        'sap': P(_face='happy', _show=('sap',), armr=limb(1, 10, 140), arml=limb(-1, 10, 140), handr=limb(1, 0, 20), handl=limb(-1, 0, 20),
                 head=T(-14), crown=T(-6)),
        'hurt': P(_face='hurt', body=T(-12, 0, 8), head=T(-8, 0, -6), armr=limb(1, 20, 50), arml=limb(-1, 20, 50), crown=T(-10, 0, 12)),
        'aura': P(_face='happy', _show=('aura',), head=T(-4, 0, 4), **up(16)),
    })
    R.DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'sit_a', 'sit_b', 'snare', 'seeds', 'sap', 'hurt', 'aura']
    if stage == 1:
        R.POSES['planted'] = R.ground({'_show': ('mound',), '_hide': tuple(p for p in R.PARTS if p != 'mound')})


def make(stage):
    R, _ = {1: sprout, 2: sapling, 3: spirit}[stage]()
    _poses(R, stage)
    return R


RIGS = {s: make(s) for s in STAGES}
R = RIGS[3]                                                 # (the grown Tree Spirit: the doll, the figurine, the frame)
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'crown': 'head'}
SHINY = 'Shiny Cherry Blossom'
