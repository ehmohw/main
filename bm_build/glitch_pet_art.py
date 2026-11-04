"""(3.1 draft, stage 1: art only - not wired) THE GLITCH - what came through when 8-Bit Cecil, 8-Bit Leo and 8-Bit Emma were all
out at once and someone used a Glitched Cartridge anyway: three sprites on one screen was more than the old cartridge could draw,
and the leftover pixels tore out of the screen as a creature of their own. It speaks in corrupted text ("H3LL0 PL4YER 0NE",
"%%THANK Y0U%%"), shifts palette at random, and is very, very friendly.

LOOK  An original glitch-sprite in the visual language of the pack's MissingNo. Chip (a scrambled block of random pixels) - and
      nothing else of anyone's: a little floating figure about knee-to-waist high on a player (~1 block to the top of its screen).
      Its HEAD is a chunky old screen - a dark bezel round a black CRT face, two tall pixel eyes and a jagged scan-line mouth
      (faces: happy ^ ^, blink, ERR in pixel letters, focus, hurt X X, surprised) - with one corner torn off it and that chunk
      floating loose beside it. Its BODY is three SCANLINE SLICES of scrambled pixels stacked like a torn sprite, each one free
      to slide sideways (the tear: '_o_sl1..3'), with dead pixels sticking out of their edges. No arms: two floating 2x2 PIXEL
      FISTS hover at its sides. No legs: below the slices it dissolves into a TRAIL of falling pixels. Four loose SHARDS orbit
      its head. The screen and the eyes glow (light_emission).

PALETTE SHIFT  every so often it flickers to another palette, at random: skins '_p1' (DMG green), '_p2' (Virtual Red), '_p3'
      (INVERTED: white noise, an orange screen). Its shiny, '_sh' "CLEAN SIGNAL": a gold-and-pearl holographic ROM chip - the one
      glitch that came out perfect. Its afterimages, '_g': a translucent cyan copy (the duplicating afterimages).

RIG   core (the root; the slices hang off it) - sl1 sl2 sl3 (the scanline slices, bottom to top) - head (a model per face;
      the torn corner 'chunk' its child) - fistr fistl - trail - shards; 'err' (a burst of ERROR glyph-cubes round a
      corrupted foe, shown by _show). Design units: the floor at y=0, facing -z, its right +x; it floats 2 units up."""
from fol5_kit import Rig, coat, flat, canvas, up, hexc, remap, ghost, limb, T
import random
from PIL import ImageDraw

PIVOT = {'core': (0, 9.0, 0), 'sl1': (0, 5.0, 0), 'sl2': (0, 8.0, 0), 'sl3': (0, 11.0, 0), 'head': (0, 14.0, 0), 'chunk': (4.5, 21.0, -1),
         'fistr': (7.0, 9.5, -1), 'fistl': (-7.0, 9.5, -1), 'trail': (0, 4.0, 0), 'shards': (0, 18.0, 0), 'err': (0, 10.0, -10)}
PARENT = {'core': None, 'sl1': 'core', 'sl2': 'core', 'sl3': 'core', 'head': 'core', 'chunk': 'head', 'fistr': 'core', 'fistl': 'core',
          'trail': 'sl1', 'shards': 'head', 'err': 'core'}
FACES = ('happy', 'blink', 'err', 'focus', 'hurt', 'surprised')
R = Rig('gl_', 0.78, PIVOT, PARENT, FACES, opt=('err',), companion=0.78)

BASE = ['#0e0b16', '#3a1a6a', '#ff3cc8', '#3cf0ff', '#ffffff', '#7a2cff', '#18ff9c']
PALS = {'_p1': ['#0f380f', '#306230', '#8bac0f', '#9bbc0f'], '_p2': ['#100000', '#5a0008', '#c0001a', '#ff3040'],
        '_p3': ['#ff8a1a', '#ffd8a0', '#ffffff', '#fffbe8'], '_sh': ['#5a3a10', '#c8962a', '#ffe08a', '#fff8e8', '#bfe8ff']}


def _noise(seed, pal=BASE, n=16, w=(3, 2, 2, 2, 1, 1, 1)):
    """scrambled pixels: runs of a colour along a scan-line, the odd line shifted - a block of broken sprite"""
    im, d = canvas(n); r = random.Random(seed); px = im.load()
    for y in range(n):
        x = 0; shift = r.choice((0, 0, 0, 3, -2))
        while x < n:
            c = hexc(r.choices(pal, w[:len(pal)])[0]); L = r.choice((1, 1, 2, 3, 4))
            for i in range(L):
                px[(x + i + shift) % n, y] = c
            x += L
    return im


def _screen(face=None):
    """the CRT: black glass with faint scan-lines, a glow in the corner, its eyes and mouth in pixel cyan-white"""
    im, d = canvas(32, '#0a0a14'); px = im.load()
    for y in range(0, 32, 2):
        for x in range(32): px[x, y] = (18, 16, 34, 255)
    for x in range(0, 6):
        for y in range(0, 6 - x): px[x + 2, y + 2] = (60, 70, 110, 255)     # (the glare)
    E, W, M = hexc('#9ffcff'), hexc('#ffffff'), hexc('#ff3cc8')
    def r(x0, y0, x1, y1, c): d.rectangle((x0, y0, x1, y1), fill=c)
    if face in (None, 'focus', 'surprised'):
        h = {'focus': (12, 16), 'surprised': (6, 18)}.get(face, (8, 18))
        for x in (8, 20):
            r(x, h[0], x + 3, h[1], E); r(x, h[0], x + 1, h[0] + 1, W)
        if face == 'focus':
            r(7, 9, 12, 10, M); r(19, 10, 24, 9, M); d.line((7, 9, 12, 11), fill=M); d.line((24, 9, 19, 11), fill=M)
    elif face == 'happy':
        for x in (8, 20):
            d.line((x, 16, x + 2, 12), fill=E, width=2); d.line((x + 2, 12, x + 4, 16), fill=E, width=2)
    elif face == 'blink':
        for x in (8, 20): r(x, 14, x + 4, 15, E)
    elif face == 'hurt':
        for x in (8, 20):
            d.line((x, 10, x + 4, 16), fill=M, width=2); d.line((x + 4, 10, x, 16), fill=M, width=2)
    elif face == 'err':                                    # E R R in a 3x5 pixel font, red on the glass
        G = {'E': ['###', '#..', '##.', '#..', '###'], 'R': ['##.', '#.#', '##.', '#.#', '#.#']}
        for i, ch in enumerate('ERR'):
            for yy, row in enumerate(G[ch]):
                for xx, c in enumerate(row):
                    if c == '#': r(6 + i * 7 + xx * 2, 9 + yy * 2, 7 + i * 7 + xx * 2, 10 + yy * 2, hexc('#ff3040'))
    # the mouth: a jagged scan-line (a grin on most faces, a flat buzz on focus, an O surprised)
    if face == 'surprised':
        d.rectangle((14, 22, 17, 26), outline=E)
    elif face != 'err':
        pts = [(9, 23), (12, 25), (15, 23), (18, 25), (21, 23), (23, 24)] if face != 'focus' else [(10, 24), (13, 23), (16, 24), (19, 23), (22, 24)]
        d.line(pts, fill=E if face != 'hurt' else M, width=2)
    return im


def _bezel():
    im = coat('#2c2a3a', 3, 16, 0.08, 1, spots=[('#46445a', 10), ('#1a1824', 8)]); return im


for k, s in (('n1', 11), ('n2', 12), ('n3', 13), ('n4', 14)): R.tex(k, _noise(s))
R.tex('bezel', _bezel()); R.tex('face', _screen())
for f in FACES: R.tex(f'face_{f}', _screen(f))
R.tex('glow', flat('#9ffcff')); R.tex('mag', flat('#ff3cc8')); R.tex('dark', flat('#0e0b16')); R.tex('errred', _noise(21, ['#ff3040', '#ffffff', '#2a0008'], 16, (3, 1, 2)))

# ---- the model
# the slices: torn scan-lines of pixels, each a little narrower or wider, with dead pixels proud of the edges
for p, y0, w, t, bits in (('sl1', 4.0, 3.4, 'n1', ((-4.4, 5.0), (3.9, 6.0))), ('sl2', 7.0, 4.2, 'n2', ((4.7, 8.0), (-5.2, 9.0), (-4.7, 7.5))),
                          ('sl3', 10.0, 3.8, 'n3', ((-4.4, 11.5), (4.3, 10.4)))):
    R.box(p, (-w, y0, -2.8), (w, y0 + 3.0, 2.8), t)
    for (bx, by) in bits:
        R.box(p, (bx - 0.5, by, -1.5), (bx + 0.5, by + 1.0, -0.5), 'n4')
R.box('sl2', (-1.5, 7.8, -3.4), (1.5, 9.2, -2.8), 'glow', light=12)                     # (a bright scan-line on its chest: its 'heart')
# the head: the screen in its bezel, a corner torn off (the chunk floats beside it)
R.box('head', (-5.5, 13.0, -3.6), (5.5, 21.0, 3.6), 'bezel')
R.box('head', (-4.6, 13.8, -3.75), (4.6, 20.2, -3.6), 'FACE', uv={'north': [0, 0, 16, 16]}, faces=('north',), light=10)
R.box('head', (-3.0, 21.0, -1.5), (-1.0, 22.0, 1.5), 'bezel')                             # (a stub of antenna, the other one broken off)
R.box('head', (-2.4, 22.0, -0.5), (-1.6, 24.5, 0.5), 'dark')
R.box('head', (-2.6, 24.5, -0.7), (-1.4, 25.7, 0.7), 'mag', light=10)
R.box('chunk', (3.6, 19.6, -3.2), (6.3, 22.3, 0.6), 'bezel', rot=('z', 18, (4.9, 21.0, -1)))
R.box('chunk', (3.9, 19.9, -3.35), (6.0, 22.0, -3.2), 'n4', faces=('north',), rot=('z', 18, (4.9, 21.0, -1)), light=8)
# the fists: 2 x 2 pixel blocks, a knuckle row of lighter pixels
for p, sx in (('fistr', 1), ('fistl', -1)):
    x, y, z = PIVOT[p]
    R.box(p, (x - 1.6, y - 1.6, z - 1.6), (x + 1.6, y + 1.6, z + 1.6), 'n2')
    R.box(p, (x - 1.7, y + 0.2, z - 1.75), (x + 1.7, y + 1.0, z - 1.55), 'glow', faces=('north',), light=8)
# the trail: pixels falling off its bottom, smaller as they go
for i, (x, y, s) in enumerate(((0.6, 3.0, 1.4), (-1.6, 1.8, 1.0), (1.4, 0.6, 0.8), (-0.4, -0.6, 0.6))):
    R.box('trail', (x - s / 2, y - s / 2, -s / 2), (x + s / 2, y + s / 2, s / 2), ('n1', 'n3', 'n4', 'n2')[i])
# the shards: loose pixels orbiting the head
for i, (x, y, z, s) in enumerate(((-8.0, 18.5, 1.0, 1.0), (7.6, 15.5, 2.0, 0.8), (-6.4, 23.0, -2.0, 0.7), (2.0, 26.0, 2.6, 0.9))):
    R.box('shards', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), ('mag', 'glow', 'n4', 'mag')[i], light=10)
# the corruption: a cage of ERROR cubes round a foe (in front of it)
for i in range(10):
    import math
    a = i * 36; x, z = 6 * math.cos(math.radians(a)), -10 + 6 * math.sin(math.radians(a)); y = 6 + (i % 4) * 3.5; s = 1.6 - (i % 3) * 0.3
    R.box('err', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), 'errred', light=12)

# ---- the skins: the palette shifts, the shiny, the afterimage
_NOISE = ('n1', 'n2', 'n3', 'n4')
for sfx, pal in PALS.items():
    for k, s in zip(_NOISE, (11, 12, 13, 14)): R.tex(f'{k}{sfx}', _noise(s, pal, 16, (3, 2, 2, 2, 1)))
    R.tex(f'glow{sfx}', flat(pal[-1])); R.tex(f'mag{sfx}', flat(pal[2])); R.tex(f'bezel{sfx}', remap(_bezel(), [pal[0], pal[1]]))
    for f in ('face',) + tuple(f'face_{x}' for x in FACES):
        R.tex(f'{f}{sfx}', remap(_screen(None if f == 'face' else f[5:]), [pal[0], pal[1], pal[-2], pal[-1]]))
    R.skin(sfx, {**{k: k + sfx for k in _NOISE}, 'glow': 'glow' + sfx, 'mag': 'mag' + sfx, 'bezel': 'bezel' + sfx,
                 'face': 'face' + sfx, **{f'face_{x}': f'face_{x}{sfx}' for x in FACES}})
_ALL = list(_NOISE) + ['glow', 'mag', 'bezel', 'dark', 'face'] + [f'face_{x}' for x in FACES]
for k in _ALL:
    R.tex(f'{k}_g', lambda k=k: ghost(R._tex[k] if not callable(R._tex[k]) else R._tex[k](), '#3cf0ff', 110))
R.skin('_g', {k: k + '_g' for k in _ALL})


# ---- poses (it floats: every pose is set 2 units off the floor unless it says otherwise)
def P(lift=2.0, **kw):
    return R.ground(kw, lift)


def tear(a=0.0, b=0.0, c=0.0, dz=0.0):
    return {'_o_sl1': (a, 0, dz), '_o_sl2': (b, 0, -dz), '_o_sl3': (c, 0, dz)}


POSES = R.POSES
POSES.update({
    'idle_a': P(**tear(0.4, -0.3, 0.2), head=T(0, 0, 2)),
    'idle_b': P(lift=2.8, **tear(-0.6, 0.5, -0.2), head=T(-4, 8, -4), _face='happy', _o_fistr=(0, 0.8, 0)),
    'idle_c': P(**tear(1.6, -1.4, 0.8), head=T(0, -12, 8), _face='blink', _o_chunk=(1.0, 1.0, 0)),    # (a flicker: the tear opens)
    'walk_0': P(core=T(14), head=T(-10), **tear(-0.8, 0.0, 0.8, 0.6), _o_fistr=(0, 0, 2.0), _o_fistl=(0, 0, 2.0)),
    'walk_1': P(lift=2.6, core=T(14), head=T(-10, 4), **tear(0.8, 0.0, -0.8, -0.6), _o_fistr=(0, 0.6, 2.4), _o_fistl=(0, 0.6, 2.4)),
    'run_0': P(core=T(28), head=T(-22), **tear(-2.0, 0.6, 1.8, 1.4), _o_fistr=(0, 1, 4.0), _o_fistl=(0, 1, 4.0), _o_trail=(0, 1, 3)),
    # sitting: settled on the floor, the slices squashed down into a heap of pixels, the fists resting either side, content
    'sit_a': P(lift=0.0, _face='happy', **{'_o_sl3': (0.5, -1.2, 0), '_o_sl2': (-0.4, -0.6, 0), '_o_head': (0, -1.8, 0)},
               _o_fistr=(0.5, -6.0, 0), _o_fistl=(-0.5, -6.0, 0), _hide=('trail',)),
    'sit_b': P(lift=0.0, _face='blink', head=T(6, 0, 10), **{'_o_sl3': (-0.5, -1.2, 0), '_o_sl2': (0.6, -0.6, 0), '_o_head': (0, -1.8, 0)},
               _o_fistr=(0.5, -6.0, 0), _o_fistl=(-0.5, -6.0, 0), _hide=('trail',)),
    # TELEPORT-STUTTER: three jittered blinks to a foe - each frame the slices land out of step
    'stutter_0': P(_face='focus', core=T(10), **tear(3.0, -2.5, 1.5)),
    'stutter_1': P(_face='focus', core=T(18, 10), **tear(-3.5, 2.0, -3.0, 1.0), _off=(0, 0, -6)),
    # the strike: both fists forward, the head buzzing
    'strike': P(_face='focus', core=T(20), head=T(-14), **tear(0.6, -0.6, 0.6), _o_fistr=(-2.5, 1.0, -6.0), _o_fistl=(2.5, 1.0, -6.0)),
    # CORRUPT: hands held out over a foe, ERR on its screen, the error cubes caging the foe
    'corrupt': P(_face='err', _show=('err',), core=T(-6), head=T(8), **tear(1.0, -1.2, 1.0), _o_fistr=(-2.0, 3.0, -4.0), _o_fistl=(2.0, 3.0, -4.0)),
    # SEGFAULT (charged): torn wide apart - every slice flung out, the head jerked up, then it snaps back together
    'segfault': P(lift=4.0, _face='surprised', **{'_o_sl1': (-5.0, -1.0, 1.0), '_o_sl2': (5.5, 0.5, -1.0), '_o_sl3': (-4.0, 2.5, 0.0),
                                               '_o_head': (2.0, 5.0, 0)}, head=T(-10, 0, -14), _o_fistr=(5, 4, 0), _o_fistl=(-5, -2, 0), _o_shards=(0, 3, 0)),
    'happy': P(lift=3.4, _face='happy', head=T(-8, 0, -6), _o_fistr=(1, 5, 0), _o_fistl=(-1, 5, 0), **tear(0.8, -0.8, 0.8)),
    'hurt': P(_face='hurt', core=T(-16), head=T(10, 0, 14), **tear(-2.0, 2.0, -1.0)),
    'tired': P(lift=0.0, _face='blink', core=T(0, 0, 70), head=T(0, 0, 10), **tear(1.0, -0.5, 1.5), _hide=('shards', 'trail')),
})
POSES['sit_a'] = R.ground(POSES['sit_a']); POSES['sit_b'] = R.ground(POSES['sit_b'])
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'run_0', 'sit_a', 'sit_b', 'stutter_0', 'stutter_1', 'strike', 'corrupt', 'segfault', 'happy', 'hurt', 'tired']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'chunk': 'head', 'shards': 'head', 'trail': 'legs', 'sl1': 'legs'}   # (no head by name: its screen is; no legs: the trail)
SHINY = ('Shiny Clean Signal', PALS['_sh'])
COSMETIC = 'CRT Bezel Skins: the screen\'s frame in Beige 1989, Clear Purple, Atomic Teal - one bezel per palette form'
