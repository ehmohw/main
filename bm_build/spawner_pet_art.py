"""(3.1 draft, stage 1: art only - not wired) THE SPAWNER - a small caged mob spawner that never fights itself: the pilot light of
a dungeon spawner that got bored of making monsters, and now makes FRIENDS - tiny ghostly minions that swarm your foes.

LOOK  Shin-high (~0.6 blocks), a vanilla-style spawner cage in miniature: a dark iron frame (corner posts with rivet caps,
      top and bottom rings), a grid of bars on every face, a solid base plate, four stubby iron feet. Inside, floating in the
      middle, its PILOT LIGHT - a round ember with a sweet face (big glowing eyes, a tiny smile, a blush), little flame wisps
      licking up off it and out between the bars. The ember's colour is what it was last fed:
        default   warm ember orange                  (minions: whatever it fancies - a mix)
        '_z'      rotten flesh -> sickly zombie green (ZOMBIE minions)
        '_s'      string -> violet with red sparks    (SPIDER minions)
        '_b'      a blaze rod -> blaze yellow-white   (BLAZE minions)
RIG   body (the root: the cage) - core (the ember, its face; bobs and spins) - flame (the wisps above it) - fl fr bl br (feet);
      fx: 'puff' (the spawn puff out of its top), 'feed' (the food going in: a flesh / a string / a rod, shown by _show with
      the skin), 'aura' (the rare Ring of Souls).
MINIONS  three small ghost rigs (MINIONS['zombie' | 'spider' | 'blaze']), translucent and softly glowing, dissolving to a wisp
      below - each with poses 'idle_a', 'rush', 'grab' / 'web' / 'shoot', and 'pop' (bursting into soul puffs).
SKINS '_z' '_s' '_b' (fed: the ember and the bar glints), '_sh' SHINY "Gilded Cage" (gold bars, a white-gold ember),
      '_cop' cosmetic "Oxidised" (copper bars gone verdigris), '_am' cosmetic "Amethyst" (amethyst bars, a lilac ember)."""
import math
import random
from PIL import Image
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, metal, glaze, glow, eye, blush, mouth, put, alpha, slab, stack, ball,
                      chain, ring, leaf)

PIVOT = {'body': (0, 2.0, 0), 'core': (0, 7.0, 0), 'flame': (0, 9.4, 0), 'fl': (-4.0, 2.0, -4.0), 'fr': (4.0, 2.0, -4.0),
         'bl': (-4.0, 2.0, 4.0), 'br': (4.0, 2.0, 4.0), 'puff': (0, 13.0, 0), 'feed': (0, 13.0, -4.0), 'aura': (0, 0, 0)}
PARENT = {'body': None, 'core': 'body', 'flame': 'core', 'fl': 'body', 'fr': 'body', 'bl': 'body', 'br': 'body', 'puff': 'body',
          'feed': 'body', 'aura': None}
FACES = ('happy', 'blink', 'focus', 'hurt', 'sleepy', 'wow', 'chew')
R = Rig('sw_', 0.8, PIVOT, PARENT, FACES, face_part='core', opt=('puff', 'feed', 'aura'))
FEET = ('fl', 'fr', 'bl', 'br')
SKIN_NAMES = {'_z': 'fed rotten flesh: ZOMBIES', '_s': 'fed string: SPIDERS', '_b': 'fed a blaze rod: BLAZES', '_sh': 'SHINY: Gilded Cage',
              '_cop': 'cosmetic: Oxidised', '_am': 'cosmetic: Amethyst'}

C = dict(bar=('#16181e', '#2a2e38', '#464c5a', '#7a8294'), plate=('#1a1c22', '#30343e', '#4a505c', '#6a7080'),
         ember=('#ff6a10', '#ff9a30', '#ffd060', '#fff0b0'), ember_dk='#c03a08', flame=('#ffb030', '#ffe080', '#ff7a20'),
         iris=('#6a1a00', '#a83a00', '#e06a10', '#ffa030', '#ffe080'), eye_white='#fff6e0', lash='#5a1400', blush='#ff5a3a', mouth='#7a2000')
FED = {'_z': dict(ember=('#3a9a2a', '#5ac83a', '#9ae86a', '#e0ffc0'), ember_dk='#1a5a14', flame=('#7ae04a', '#c8ff9a', '#3aa02a'),
                  iris=('#0a3a0a', '#1a6a1a', '#3aa02a', '#7ad04a', '#c8ff9a'), lash='#0a3a0a', blush='#9ae06a', mouth='#0a3a0a'),
       '_s': dict(ember=('#6a1a8a', '#9a2ab0', '#d04ae0', '#ffb0ff'), ember_dk='#3a0a5a', flame=('#d04ae0', '#ffa0ff', '#8a1aa0'),
                  iris=('#5a0000', '#a00010', '#e02030', '#ff6060', '#ffc0c0'), lash='#2a0030', blush='#ff60a0', mouth='#2a0030'),
       '_b': dict(ember=('#f0a000', '#ffd020', '#fff070', '#ffffe0'), ember_dk='#c07000', flame=('#ffe040', '#ffffc0', '#ffa000'),
                  iris=('#6a3a00', '#a86a00', '#e8a800', '#ffe040', '#fffbc0'), lash='#6a3a00', blush='#ffa040', mouth='#6a3a00'),
       '_sh': dict(bar=('#5a3a08', '#a8781a', '#e0b040', '#fff0a0'), plate=('#4a3008', '#8a6014', '#c8962a', '#f0d070'),
                   ember=('#ffe0a0', '#fff0c8', '#fffbe8', '#ffffff'), ember_dk='#e0b060', flame=('#fff4c0', '#ffffff', '#ffd880'),
                   iris=('#5a3a00', '#a87a10', '#e8b840', '#ffe890', '#fffbe0'), lash='#5a3a00', blush='#ffc090'),
       '_cop': dict(bar=('#1a4a40', '#2e7a66', '#4aa88a', '#8ad8b8'), plate=('#1a3a34', '#2a5a50', '#3a7a6a', '#5a9a8a')),
       '_am': dict(bar=('#2a1050', '#4a2a80', '#7a4ab8', '#b090f0'), plate=('#200c40', '#38206a', '#5a3a98', '#8a6ac8'),
                   ember=('#b070ff', '#d0a0ff', '#f0d8ff', '#ffffff'), ember_dk='#7040c0', flame=('#d0a0ff', '#ffffff', '#a070f0'),
                   iris=('#3a1060', '#6a2aa0', '#a060e0', '#d0a0ff', '#f8e8ff'), lash='#3a1060', blush='#ff90e0')}

CF = 4.4          # (the ember's front face: 4.4 x 4.4 units = 18 x 18 texels)


# ---------------------------------------------------------------------------------------------------- textures
def _ember(c, seed):
    e = c['ember']
    return lit(soft(e[1], e[2], e[0], seed, 0.12), 1.12, 0.86, 12)


def _face(kind, c):
    im = _ember(c, 31)
    if kind not in ('hurt',):
        blush(im, 3, 12, 4, c['blush']); blush(im, 15, 12, 4, c['blush'])
    mouth(im, 9, 13, {None: 'smile', 'happy': 'open', 'blink': 'smile', 'focus': 'flat', 'hurt': 'wobble', 'sleepy': 'flat', 'wow': 'o',
                      'chew': 'cat'}[kind], c['mouth'], '#ff8a8a', 4)
    return im


def _eyes(kind, c):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    k = {'focus': 'fierce', 'wow': 'wide', 'chew': 'happy'}.get(kind, kind)
    for cx, fl in ((5, False), (13, True)):
        eye(im, cx, 3, 7, 9, fl, k, iris=c['iris'], lash=c['lash'], pupil='#1a0600', sclera=False, irk=0.7)
    return im


def textures(c):
    t = {'bar': metal(c['bar'], 1), 'bar2': metal(c['bar'], 2), 'plate': lit(metal(c['plate'], 3, rivets=True), 1.08, 0.9, 6),
         'rivet': metal((c['bar'][1], c['bar'][2], c['bar'][3], '#ffffff'), 4),
         'ember': _ember(c, 5), 'emberdk': soft(c['ember'][0], c['ember'][1], c['ember_dk'], 6, 0.2),
         'flame': lit(soft(c['flame'][0], c['flame'][1], c['flame'][2], 7, 0.2), 1.25, 0.8, 14), 'flamec': soft(c['flame'][1], '#ffffff', c['flame'][0], 8, 0.15),
         'smoke': glow(('#ffffff', '#e0e0e8', '#b0b0c0', '#b0b0c0'), 16, alpha=(200, 150, 90, 0)),
         'inner': glow((c['ember'][2], c['ember'][1], c['ember'][0], c['ember'][0]), 16, alpha=(150, 100, 50, 0)),
         'flesh': soft('#8a5a3a', '#b07a4a', '#5a3a20', 9, 0.3), 'string': soft('#f0f0f0', '#ffffff', '#c8c8c8', 10, 0.1),
         'rod': lit(soft('#ffd020', '#fff080', '#c08000', 11, 0.2), 1.2, 0.8, 10),
         'face': _face(None, c), 'eyes': _eyes(None, c)}
    for f in FACES: t[f'face_{f}'] = _face(f, c); t[f'eyes_{f}'] = _eyes(f, c)
    return t


TEX = textures(C)
for k, v in TEX.items(): R.tex(k, v)
for sfx, ch in FED.items():
    for k, v in textures(dict(C, **ch)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in TEX})

# ---------------------------------------------------------------------------------------------------- the spawner
B = R.box
H, Y0, Y1 = 5.0, 2.0, 12.0          # (half width; the cage's bottom and top)
bw = 0.7                            # (a frame member's width)
# the base plate and the top ring; the four corner posts with rivet caps
B('body', (-H - 0.2, Y0, -H - 0.2), (H + 0.2, Y0 + 1.1, H + 0.2), 'plate', shift=False)
B('body', (-H + 0.6, Y0 + 1.1, -H + 0.6), (H - 0.6, Y0 + 1.3, H - 0.6), 'emberdk', light=6)   # (the hearth, glowing)
for a, b in (((-H - 0.1, Y1 - bw, -H - 0.1), (H + 0.1, Y1, -H + bw)), ((-H - 0.1, Y1 - bw, H - bw), (H + 0.1, Y1, H + 0.1)),
             ((-H - 0.1, Y1 - bw, -H + bw), (-H + bw, Y1, H - bw)), ((H - bw, Y1 - bw, -H + bw), (H + 0.1, Y1, H - bw))):
    B('body', a, b, 'bar', shift=False)
for sx in (-1, 1):
    for sz in (-1, 1):
        x0, z0 = sorted((sx * H, sx * (H - bw))), sorted((sz * H, sz * (H - bw)))
        B('body', (x0[0] - 0.05, Y0 + 1.1, z0[0] - 0.05), (x0[1] + 0.05, Y1 - bw, z0[1] + 0.05), 'bar2')
        cx, cz = sx * (H - bw / 2), sz * (H - bw / 2)
        B('body', (cx - 0.55, Y1, cz - 0.55), (cx + 0.55, Y1 + 0.45, cz + 0.55), 'rivet')                     # (rivet caps on top)
        B('body', (cx - 0.5, Y0 + 1.1, cz - 0.5), (cx + 0.5, Y0 + 1.5, cz + 0.5), 'rivet')
# the bars: on every face two uprights and a cross bar (the vanilla spawner's grid), a hair inside the frame
for i, (ax, s) in enumerate((('z', -1), ('z', 1), ('x', -1), ('x', 1))):
    d = s * (H - 0.25)
    front = ax == 'z' and s < 0                                                          # (the front: a wider gap, so its face shows)
    for u in ((-2.9, 2.9) if front else (-1.7, 1.7)):
        if ax == 'z': B('body', (u - 0.22, Y0 + 1.1, d - 0.22), (u + 0.22, Y1 - bw, d + 0.22), 'bar')
        else: B('body', (d - 0.22, Y0 + 1.1, u - 0.22), (d + 0.22, Y1 - bw, u + 0.22), 'bar')
    for yy in ((4.1,) if front else (5.2, 8.6)):
        if ax == 'z': B('body', (-H + bw, yy - 0.2, d - 0.2), (H - bw, yy + 0.2, d + 0.2), 'bar2')
        else: B('body', (d - 0.2, yy - 0.2, -H + bw), (d + 0.2, yy + 0.2, H - bw), 'bar2')
# the top: a grid too, and a little ring handle on it
for u in (-1.7, 1.7):
    B('body', (u - 0.22, Y1 - 0.5, -H + bw), (u + 0.22, Y1 - 0.1, H - bw), 'bar')
    B('body', (-H + bw, Y1 - 0.5, u - 0.22), (H - bw, Y1 - 0.1, u + 0.22), 'bar')
ring(R, 'body', (0, Y1 + 1.0, 0), 1.0, 8, 0.32, 0.32, 'bar', plane='xy')
# the glow inside (a soft light plate, front and back)
B('body', (-3.6, 3.8, -0.02), (3.6, 11.0, 0.02), 'inner', faces=('north', 'south'), full=True, light=10)
B('body', (-0.02, 3.8, -3.6), (0.02, 11.0, 3.6), 'inner', faces=('east', 'west'), full=True, light=10)
# ---- the pilot light: a round ember (slabs), its face on the flat front, flame wisps above it
cy = PIVOT['core'][1]
stack(R, 'core', [(cy - 2.6, cy - 2.0, 1.6), (cy - 2.0, cy - 1.2, 2.3), (cy - 1.2, cy + 1.4, 2.6), (cy + 1.4, cy + 2.2, 2.3), (cy + 2.2, cy + 2.8, 1.5)],
      'ember', shift=False, light=8)
fy0 = cy - CF / 2 + 0.05
B('core', (-CF / 2, fy0, -2.62), (CF / 2, fy0 + CF, -2.6), 'FACE', faces=('north',), uv={'north': [0, 0, CF, CF]}, light=8)
B('core', (-CF / 2, fy0, -2.66), (CF / 2, fy0 + CF, -2.64), 'EYES', faces=('north',), uv={'north': [0, 0, CF, CF]}, light=12)
fx_, fy_, fz_ = PIVOT['flame']
stack(R, 'flame', [(fy_, fy_ + 0.6, 1.1), (fy_ + 0.6, fy_ + 1.5, 1.2), (fy_ + 1.5, fy_ + 2.2, 0.8), (fy_ + 2.2, fy_ + 2.7, 0.45)], 'flame', light=14)
R.seg('flame', (0, fy_ + 2.6, 0), (-0.5, fy_ + 3.3, 0.3), 0.36, 0.36, 'flame', light=14)
stack(R, 'flame', [(fy_ + 0.1, fy_ + 0.8, 0.6), (fy_ + 0.8, fy_ + 1.3, 0.45)], 'flamec', c=(0, -0.4), light=15)
for sx in (-1, 1):                                                                    # (two side licks escaping between the bars)
    R.seg('flame', (sx * 1.6, fy_ - 0.6, 0.4), (sx * 2.6, fy_ + 1.4, 0.6), 0.5, 0.5, 'flame', light=14)
    R.seg('flame', (sx * 2.6, fy_ + 1.4, 0.6), (sx * 2.9, fy_ + 2.4, 0.6), 0.32, 0.32, 'flame', light=14)
# ---- the feet: stubby iron, out of the base corners
for p in FEET:
    x, y, z = PIVOT[p]
    stack(R, p, [(0.0, 0.5, 1.1), (0.5, 1.6, 0.85), (1.6, 2.1, 0.95)], 'plate', c=(x, z))
# ---- fx: the spawn puff, the food going in, the Ring of Souls
px_, py_, pz_ = PIVOT['puff']
for i in range(7):
    a = math.radians(i * 51); r = 1.6 + (i % 3) * 0.8
    x, z = r * math.cos(a), r * math.sin(a); y = py_ + (i % 4) * 0.9
    B('puff', (x - 1.2, y - 1.2, z), (x + 1.2, y + 1.2, z + 0.02), 'smoke', faces=('north', 'south'), full=True, light=6)
    B('puff', (x, y - 1.2, z - 1.2), (x + 0.02, y + 1.2, z + 1.2), 'smoke', faces=('east', 'west'), full=True, light=6)
B('feed', (-0.9, 12.8, -4.4), (0.9, 13.6, -3.6), 'flesh', rot=('z', 20, (0, 13.2, -4)))                             # (rotten flesh)
R.seg('feed', (-1.6, 14.4, -4.0), (1.4, 12.6, -4.0), 0.24, 0.24, 'string')                                          # (a string)
R.seg('feed', (1.2, 15.4, -4.0), (-0.4, 12.4, -4.0), 0.5, 0.5, 'rod', light=8)                                      # (a blaze rod)
for i in range(6):
    a = math.radians(i * 60); x, z = 10 * math.cos(a), 10 * math.sin(a); y = 7 + 2.2 * math.sin(a * 3)
    ball(R, 'aura', (x, y, z), 0.9, 'ember', 3, light=12)
    B('aura', (x - 0.9, y - 2.0, z - 0.02), (x + 0.9, y - 0.4, z + 0.02), 'inner', faces=('north', 'south'), full=True, light=10)


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


POSES = R.POSES
POSES.update({
    'idle_a': P(core=T(0, 10, 0)),
    'idle_b': P(_face='happy', core=T(-8, -16, 6), flame=T(0, 0, 10), _o_core=(0, 0.6, 0)),
    'walk_0': P(lift=0.8, body=T(6, 0, 6), fl=T(-24), br=T(-24), fr=T(16), bl=T(16), core=T(-6), flame=T(-14)),
    'walk_1': P(body=T(-2, 0, -6), fl=T(16), br=T(16), fr=T(-24), bl=T(-24), core=T(4), flame=T(8)),
    # sitting: it settles, feet tucked, the ember low and dim; a doze, the flame down to a pilot light
    'sit_a': P(_face='happy', _hide=FEET, _o_core=(0, -0.8, 0)),
    'sit_b': P(_face='sleepy', _hide=FEET, _o_core=(0, -1.6, 0), flame=T(30)),
    # SPAWN: the ember flares up into the top of the cage - a puff - a minion pops out
    'spawn': P(_face='wow', _show=('puff',), _o_core=(0, 1.6, 0), flame=T(0, 0, 0), body=T(-4)),
    # FEED: lid... it looks up, mouth open - the food dropped in through the top - it chews (and its colour changes)
    'feed': P(_face='wow', _show=('feed',), core=T(-24), _o_core=(0, 1.0, 0)),
    'chew': P(_face='chew', core=T(8, 0, 8), _o_core=(0, -0.4, 0)),
    # COMMAND: it leans after the foe, the ember pressed to the front bars - the swarm goes
    'command': P(_face='focus', body=T(14), core=T(10), _o_core=(0, 0, -1.2), flame=T(-30)),
    'hurt': P(_face='hurt', body=T(-12, 0, 10), core=T(0, 0, -14), _o_core=(0.6, -0.4, 0)),
    'aura': P(_face='happy', _show=('aura',)),
})
R.DRAFT = ['idle_a', 'idle_b', 'walk_0', 'walk_1', 'sit_a', 'sit_b', 'spawn', 'feed', 'chew', 'command', 'hurt', 'aura']
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'body': 'head', 'core': 'head', 'flame': 'head', 'fl': 'legs', 'fr': 'legs', 'bl': 'legs', 'br': 'legs'}
SHINY = 'Shiny Gilded Cage'


# ---------------------------------------------------------------------------------------------------- the minions
MA = 135            # (their alpha: ghostly)


def _gface(c, kind):
    """a minion's face (full uv): its own pack-style pixel face, soft-glowing"""
    def f(x, y, r):
        if kind == 'zombie':
            if 9 <= y <= 14 and (6 <= x <= 11 or 20 <= x <= 25): return c['eye']
            if 20 <= y <= 22 and 10 <= x <= 21: return c['dark']
            if y < 6: return c['hair']
        if kind == 'blaze':
            if 11 <= y <= 15 and (6 <= x <= 12 or 19 <= x <= 25): return c['dark']
            if 11 <= y <= 12 and (8 <= x <= 9 or 21 <= x <= 22): return c['eye']
            if 20 <= y <= 22 and 10 <= x <= 21: return c['dark']
        if kind == 'spider':
            for ex, ey, s in ((9, 12, 3), (20, 12, 3), (5, 8, 2), (24, 8, 2), (13, 7, 1), (17, 7, 1)):
                if ex <= x < ex + s * 2 - 0 and ey <= y < ey + s * 2 - 1: return c['eye']
        return c['skin'] if (x + y) % 7 else c['skin2']
    return alpha(cells(f, 40), 185)


def _minion(kind):
    pal = {'zombie': dict(skin='#6ab84a', skin2='#5aa03a', hair='#3a6a2a', shirt='#3aa8b0', pants='#4a4ab0', eye='#e8ffd0', dark='#1a3a1a', wisp='#a8f0c0'),
           'spider': dict(skin='#3a2a4a', skin2='#2a1a3a', hair='#2a1a3a', shirt='#4a3a5a', pants='#2a1a3a', eye='#ff3040', dark='#100818', wisp='#c0a0e0'),
           'blaze': dict(skin='#ffd040', skin2='#f0b020', hair='#ffe080', shirt='#ffb020', pants='#ff9010', eye='#fff8c0', dark='#7a3a00', wisp='#fff0a0')}[kind]
    pv = {'body': (0, 6.0, 0), 'head': (0, 10.0, 0), 'armr': (2.6, 9.4, 0), 'arml': (-2.6, 9.4, 0), 'wisp': (0, 5.0, 0), 'pop': (0, 8, 0),
          'legs': (0, 6.0, 0), 'rods': (0, 7.0, 0)}
    par = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'wisp': 'body', 'pop': 'body', 'legs': 'body', 'rods': 'body'}
    M = Rig(f'sm{kind[0]}_', 0.6, pv, par, ('grin',), opt=('pop',))
    t = {'skin': alpha(soft(pal['skin'], mix(pal['skin'], '#ffffff', 0.3), pal['skin2'], 41, 0.1), MA),
         'shirt': alpha(soft(pal['shirt'], mix(pal['shirt'], '#ffffff', 0.3), mix(pal['shirt'], '#000000', 0.2), 42, 0.1), MA),
         'pants': alpha(soft(pal['pants'], mix(pal['pants'], '#ffffff', 0.25), mix(pal['pants'], '#000000', 0.2), 43, 0.1), MA - 30),
         'wisp': glow((pal['wisp'], pal['wisp'], pal['wisp'], pal['wisp']), 16, alpha=(150, 110, 70, 0)),
         'eye': soft(pal['eye'], '#ffffff', pal['eye'], 44, 0.1), 'face': _gface(pal, kind), 'face_grin': _gface(pal, kind),
         'puff': glow(('#ffffff', pal['wisp'], pal['wisp'], pal['wisp']), 16, alpha=(220, 160, 90, 0))}
    for k, v in t.items(): M.tex(k, v)
    MB = M.box
    if kind in ('zombie', 'blaze'):
        hs = 2.4 if kind == 'zombie' else 2.6
        MB('head', (-hs, 10.0, -hs), (hs, 10.0 + 2 * hs, hs), 'skin', shift=False, light=5)
        MB('head', (-hs, 10.0, -hs - 0.02), (hs, 10.0 + 2 * hs, -hs), 'FACE', faces=('north',), full=True, light=8)
    if kind == 'zombie':
        MB('body', (-2.2, 5.6, -1.2), (2.2, 10.0, 1.2), 'shirt', light=4)
        MB('body', (-2.0, 4.0, -1.1), (2.0, 5.6, 1.1), 'pants', light=4)
        for p, sx in (('armr', 1), ('arml', -1)):                                             # (arms out in front, zombie-wise)
            x, y, z = pv[p]
            M.seg(p, (x, y, z), (x + sx * 0.2, y - 0.2, z - 5.0), 1.5, 1.5, 'skin', light=5)
    if kind == 'blaze':
        for i in range(4):                                                                     # (the rods round it, two tiers)
            a = math.radians(i * 90 + 45)
            for ty, r in ((8.6, 2.8), (5.6, 2.2)):
                x, z = r * math.cos(a + ty), r * math.sin(a + ty)
                MB('rods', (x - 0.45, ty - 1.4, z - 0.45), (x + 0.45, ty + 1.4, z + 0.45), 'skin', light=10)
        for i in range(3):
            MB('wisp', (-1.6 + i * 1.6 - 0.8, 3.0 - i, -0.02), (-1.6 + i * 1.6 + 0.8, 6.4 - i, 0.02), 'wisp', faces=('north', 'south'), full=True, light=8)
    if kind == 'spider':
        ball(M, 'body', (0, 6.4, 1.6), 2.8, 'skin', 4, ry=2.2, light=4)                         # (the abdomen)
        ball(M, 'head', (0, 6.6, -2.4), 1.8, 'skin', 3, ry=1.5, light=4)
        MB('head', (-1.5, 5.6, -4.1), (1.5, 7.8, -4.08), 'FACE', faces=('north',), full=True, light=10)
        for sx in (-1, 1):                                                                     # (eight legs, bent: a knee up, a foot down)
            for j, dz in enumerate((-2.6, -1.0, 0.6, 2.2)):
                k = (sx * 3.6, 9.0 - abs(dz) * 0.3, dz * 1.3); f = (sx * 6.0, 2.4, dz * 1.7)
                chain(M, 'legs', [(sx * 1.2, 6.4, dz * 0.6), k, f], [0.6, 0.5, 0.25], 'skin', )
    if kind == 'zombie':
        MB('wisp', (-1.8, 1.0, -0.02), (1.8, 4.6, 0.02), 'wisp', faces=('north', 'south'), full=True, light=8)
        MB('wisp', (-0.02, 1.0, -1.4), (0.02, 4.6, 1.4), 'wisp', faces=('east', 'west'), full=True, light=8)
    for i in range(6):                                                                         # (POP: the burst of soul puffs)
        a = math.radians(i * 60); x, y = 3.5 * math.cos(a), 8 + 3.5 * math.sin(a)
        MB('pop', (x - 1.4, y - 1.4, -0.02), (x + 1.4, y + 1.4, 0.02), 'puff', faces=('north', 'south'), full=True, light=12)
        MB('pop', (x - 0.02, y - 1.4, -1.4), (x + 0.02, y + 1.4, 1.4), 'puff', faces=('east', 'west'), full=True, light=12)
    lift = 2.0 if kind != 'spider' else 0.0
    def MP(**kw): return M.ground(kw, lift)
    M.POSES.update({
        'idle_a': MP(),
        'rush': MP(body=T(24 if kind != 'spider' else 6), head=T(-14)),
        'grab': MP(body=T(10), armr=limb(1, 20, -10), arml=limb(-1, 20, -10)) if kind == 'zombie' else
                (MP(body=T(-20), head=T(-10)) if kind == 'spider' else MP(body=T(-10), head=T(-8), rods=T(0, 45))),
        'pop': dict(MP(), _show=('pop',), _hide=('head', 'armr', 'arml', 'legs', 'rods')),
    })
    M.DRAFT = ['idle_a', 'rush', 'grab', 'pop']
    return M


MINIONS = {k: _minion(k) for k in ('zombie', 'spider', 'blaze')}
UNLOCK = ('Light a Soul Lantern beside a dungeon\'s monster spawner and hold the room through three waves without breaking it. On '
          'the third wave the spawner\'s pilot light "gets bored of making monsters" and hops out of it as the Spawner - which only '
          'ever makes friends. The real spawner block is never touched (it keeps spawning, as vanilla).')
