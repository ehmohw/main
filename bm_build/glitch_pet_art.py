"""(3.1 draft, stage 1: art only - not wired) THE GLITCH (2nd pass: the owner's "looks good overall - his animations and movement
should be glitchy". The model is kept; it's rebuilt to the quality bar, and it gets glitchy motion: see MOTION at the bottom, and
the design doc's timing tables).

What came through when 8-Bit Cecil, 8-Bit Leo and 8-Bit Emma were all out at once and someone used a Glitched Cartridge anyway:
three sprites on one screen was more than the old cartridge could draw, and the leftover pixels tore out of the screen as a
creature of their own. It speaks in corrupted text ("H3LL0 PL4YER 0NE", "%%THANK Y0U%%"), shifts palette at random, and is very,
very friendly.

LOOK  a little floating figure about knee-to-waist high on a player (~1 block to the top of its screen).
      HEAD   a chunky old CRT: a rounded plastic bezel, the screen recessed in it (scan-lines, a vignette, a glare streak), the
             tube's tapered housing behind it (so side-on it's a real old telly), two knobs, a speaker grille and a magenta
             power LED on its chin, rabbit-ear antennae (one whole with a glowing bead, one snapped off and sparking). Its top
             corner is TORN OFF - a stair-stepped bite out of the bezel and the screen, the guts glowing in the tear - and that
             chunk floats loose above it.
      FACE   pixel eyes with an RGB fringe (a magenta column one side, a teal one the other - a misaligned colour gun), a
             jagged scan-line mouth; faces: happy ^ ^, blink, ERR, focus, hurt X X, surprised, SNOW (static), REW (<<).
      BODY   three SCANLINE SLICES of torn sprite - rows of pixel runs from the three 8-bit heroes' palettes - stacked with a
             hairline gap, each torn ragged at its ends and lit along its top edge, each free to slide on its own.
      FISTS  two 2x2x2 voxel fists, a lit knuckle row and a thumb pixel. TRAIL: pixels falling off its bottom. SHARDS: four
             loose pixels orbiting the head. The screen, eyes, LED, bead and the tear glow (light_emission).

SKINS '_p1' DMG green, '_p2' Virtual Red, '_p3' INVERTED (palette shifts at random); '_sh' the SHINY "CLEAN SIGNAL" (a gold-and-
      pearl holographic ROM chip - the one glitch that came out perfect); '_g' a cyan afterimage; '_gr' / '_gc' the RGB-SPLIT
      pair (a red copy and a cyan copy, drawn a hair to either side for 2-3 ticks when it teleports, snaps or gets hit).

RIG   core (the root; the slices hang off it) - sl1 sl2 sl3 (bottom to top) - head (a model per face; the torn 'chunk' its
      child; 'shards' on it) - fistr fistl - trail; 'err' (the ERROR cage round a foe, shown by _show). Design units: the
      floor at y=0, facing -z, its right +x; it floats 2 units up."""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import Rig, hexc, mix, canvas, cells, soft, lit, ghost, limb, T, put, ring

PIVOT = {'core': (0, 9.0, 0), 'sl1': (0, 5.0, 0), 'sl2': (0, 8.0, 0), 'sl3': (0, 11.0, 0), 'head': (0, 14.0, 0), 'chunk': (6.2, 22.2, -1.6),
         'fistr': (7.0, 9.5, -1), 'fistl': (-7.0, 9.5, -1), 'trail': (0, 4.0, 0), 'shards': (0, 18.0, 0), 'err': (0, 10.0, -10)}
PARENT = {'core': None, 'sl1': 'core', 'sl2': 'core', 'sl3': 'core', 'head': 'core', 'chunk': 'head', 'fistr': 'core', 'fistl': 'core',
          'trail': 'sl1', 'shards': 'head', 'err': 'core'}
FACES = ('happy', 'blink', 'err', 'focus', 'hurt', 'surprised', 'snow', 'rew')
R = Rig('gl_', 0.78, PIVOT, PARENT, FACES, opt=('err',), companion=0.78)
SKIN_NAMES = {'_p1': 'palette shift: DMG green', '_p2': 'palette shift: Virtual Red', '_p3': 'palette shift: INVERTED',
              '_sh': 'SHINY: Clean Signal', '_g': 'afterimage', '_gr': 'RGB split: red', '_gc': 'RGB split: cyan'}

# the palette: glass, the case, the three heroes' sprite colours, the signal colours
BASE = dict(glass='#0a0a14', scan='#141228', case='#2e2b3e', case_l='#433f5a', case_d='#1e1c2a', guts='#7a2cff',
            mag='#ff3cc8', cyan='#3cf0ff', eye='#9ffcff', white='#ffffff', purple='#7a2cff', green='#18ff9c', deep='#0e0b16',
            red='#ff3040', sprites=(('#ff6ac8', '#ffd0ea', '#3a6fd0', '#f7d7bf'),      # (8-bit Emma: pink, blue, skin)
                                    ('#e8b830', '#fff0a0', '#c03020', '#f0c090'),      # (8-bit Leo: gold, red)
                                    ('#3cf0ff', '#7a2cff', '#18ff9c', '#ffffff')))     # (8-bit Cecil / the signal)
PALS = {
    '_p1': dict(glass='#0f380f', scan='#173f17', case='#306230', case_l='#3e7a3e', case_d='#204a20', guts='#8bac0f', mag='#8bac0f',
                cyan='#9bbc0f', eye='#c8e070', purple='#306230', green='#9bbc0f', red='#8bac0f',
                sprites=(('#0f380f', '#306230', '#8bac0f', '#9bbc0f'),) * 3),
    '_p2': dict(glass='#100000', scan='#1e0004', case='#3a0008', case_l='#5a0010', case_d='#240004', guts='#ff3040', mag='#ff3040',
                cyan='#ff6070', eye='#ff9aa0', purple='#8a0018', green='#c0001a', sprites=(('#5a0008', '#c0001a', '#ff3040', '#ff9aa0'),) * 3),
    '_p3': dict(glass='#fffbe8', scan='#f0e8d0', case='#e8e0f0', case_l='#ffffff', case_d='#c8c0d8', guts='#ff8a1a', mag='#ff8a1a',
                cyan='#1a6aff', eye='#ff6a00', purple='#ffd8a0', green='#e000c0', white='#3a2000', deep='#fff0d8',
                sprites=(('#ffffff', '#ffd8a0', '#ff8a1a', '#1a6aff'),) * 3),
    '_sh': dict(glass='#1a1206', scan='#2a1e0a', case='#c8962a', case_l='#ffe08a', case_d='#8a6216', guts='#bfe8ff', mag='#ffe08a',
                cyan='#bfe8ff', eye='#fff8e8', purple='#c8962a', green='#bfe8ff', red='#ffe08a',
                sprites=(('#fff8e8', '#ffe08a', '#c8962a', '#bfe8ff'), ('#bfe8ff', '#fff8e8', '#e8c060', '#ffffff'), ('#ffe08a', '#fff8e8', '#bfe8ff', '#c8962a'))),
}


# ---------------------------------------------------------------------------------------------------- textures
def _scan(seed, c, which, alpha=255):
    """a torn slice of sprite: rows of pixel RUNS (2-6 cells of one colour) from one hero's palette with the odd signal pixel,
    each row shifted - read as scan-lines of a broken sprite, not confetti. Row 0 lit (the slice's top edge), row 1 a dark
    hairline; anchored boxes (shift=False) show it"""
    rnd = random.Random(seed); pal = c['sprites'][which]; sig = (c['cyan'], c['mag'], c['green'])
    rows = []
    for y in range(32):
        row = []; x = 0
        while x < 32:
            L = rnd.choice((2, 3, 3, 4, 5, 6)); col = rnd.choice(pal) if rnd.random() > 0.12 else rnd.choice(sig)
            if rnd.random() < 0.18: col = c['deep']
            row += [col] * L; x += L
        sh = rnd.choice((0, 0, 0, 1, -2)); rows.append(row[-sh:] + row[:-sh] if sh else row)
    def f(x, y, r):
        if y == 0: return mix(rows[0][x], '#ffffff', 0.45)
        if y == 1: return mix(rows[1][x], c['deep'], 0.55)
        return rows[y][x]
    return cells(f, seed, alpha=alpha)


def _case(c, seed):
    """the bezel's plastic: soft patches, lit from the top, a sheen row"""
    return lit(soft(c['case'], c['case_l'], c['case_d'], seed, 0.04), 1.16, 0.86, 10)


def _vent(c):
    """vent slots across the tube's housing: dark slots with a lit lip under each"""
    return cells(lambda x, y, r: c['case_d'] if y % 4 == 1 and 2 < x % 16 < 14 else (c['case_l'] if y % 4 == 2 and 2 < x % 16 < 14 else c['case']), 3)


def _grille(c):
    return cells(lambda x, y, r: c['case_d'] if x % 2 else c['case'], 4)


def _guts(c):
    """the torn edge's insides: glowing pixel shreds, wires (lines of the signal colours)"""
    return cells(lambda x, y, r: (c['guts'], c['mag'], c['cyan'], c['deep'])[(x * 3 + y * 5 + (x // 3)) % 4], 5)


def _pixel(col, seed, c):
    """one voxel of a fist: a flat pixel colour, a lit top row and a darker bottom row (a cleanly shaded block)"""
    def f(x, y, r):
        if y < 2: return mix(col, '#ffffff', 0.35)
        if y > 27: return mix(col, c['deep'], 0.35)
        return col
    return cells(f, seed)


# the screen: 9.4 x 5.2 units = 38 x 21 texels (from the top-left; the sheet's left is its right - the torn corner's side)
SW, SH = 38, 21
TORN = [(0, 6), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2)]          # (row, last torn col): the stair the tear leaves in the glass


def _screen(c, face=None):
    im = Image.new('RGBA', (64, 64), hexc(c['glass'])); px = im.load()
    G, S = hexc(c['glass']), hexc(c['scan'])
    for y in range(SH):
        for x in range(SW):
            v = S if y % 2 == 0 else G
            d = max(abs(x - SW / 2) / (SW / 2), abs(y - SH / 2) / (SH / 2))
            if d > 0.86: v = tuple(int(q * 0.7) for q in v[:3]) + (255,)                 # (the vignette)
            px[x, y] = v
    for i in range(7):                                                                     # (the glare: a diagonal streak, top right)
        put(im, SW - 10 + i, 1 + i // 2, mix(c['glass'], '#5a6a9a', 0.6)); put(im, SW - 9 + i, 1 + i // 2, mix(c['glass'], '#8a9ac8', 0.5))
    E, W, M, Tl = c['eye'], c['white'], c['mag'], c['green']
    halo = mix(c['glass'], c['eye'], 0.3)
    def r(x0, y0, x1, y1, col):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): put(im, x, y, col)
    def eye(x, y0, y1, shine=True):
        r(x - 1, y0 - 1, x + 4, y1 + 1, halo)                                               # (phosphor halo)
        r(x - 1, y0, x - 1, y1, M); r(x + 4, y0, x + 4, y1, Tl)                             # (the RGB fringe)
        r(x, y0, x + 3, y1, E)
        if shine: r(x, y0, x + 1, y0 + 1, W)
    L, Rr = 10, 24                                                                          # (eye columns)
    if face in (None, 'focus', 'surprised'):
        y0, y1 = {'focus': (7, 11), 'surprised': (3, 12)}.get(face, (4, 12))
        eye(L, y0, y1); eye(Rr, y0, y1)
        if face == 'focus':
            for i in range(5): put(im, L - 1 + i, 4 + i // 2, M); put(im, Rr + 4 - i, 4 + i // 2, M)
    elif face == 'happy':
        for x in (L, Rr):
            for i in range(3): r(x + i, 8 - i, x + i, 9 - i, E); r(x + 5 - i, 8 - i, x + 5 - i, 9 - i, E)
            r(x - 1, 9, x - 1, 9, M); r(x + 6, 9, x + 6, 9, Tl)
    elif face == 'blink':
        for x in (L, Rr): r(x - 1, 8, x + 4, 9, halo); r(x, 8, x + 3, 8, E); r(x - 1, 8, x - 1, 8, M); r(x + 4, 8, x + 4, 8, Tl)
    elif face == 'hurt':
        for x in (L, Rr):
            for i in range(6): put(im, x - 1 + i, 4 + int(i * 1.6), M); put(im, x + 4 - i, 4 + int(i * 1.6), M)
    elif face == 'err':
        F = {'E': ['###', '#..', '##.', '#..', '###'], 'R': ['##.', '#.#', '##.', '#.#', '#.#']}
        for i, ch in enumerate('ERR'):
            for yy, row in enumerate(F[ch]):
                for xx, q in enumerate(row):
                    if q == '#': r(8 + i * 8 + xx * 2, 4 + yy * 2, 9 + i * 8 + xx * 2, 5 + yy * 2, c['red'])
    elif face == 'snow':                                                                    # (static: the signal lost)
        rnd = random.Random(7)
        for y in range(SH):
            for x in range(SW):
                v = rnd.random()
                if v > 0.55: put(im, x, y, mix(c['glass'], '#ffffff', 0.2 + 0.7 * rnd.random()))
        r(0, 9, SW - 1, 10, mix(c['glass'], '#ffffff', 0.55))                               # (a rolling bar)
    elif face == 'rew':                                                                     # (<< REW, and a timecode bar)
        for x0 in (12, 19):                                                                  # (two left-pointing triangles)
            for i in range(6): r(x0 + 5 - i, 4 + i, x0 + 5 - i, 14 - i, E)
        r(6, 17, 31, 17, mix(c['glass'], c['eye'], 0.4)); r(6, 17, 14, 17, E)
    # the mouth: a jagged scan-line (a grin, a buzz on focus, an O surprised)
    if face == 'surprised':
        r(17, 14, 20, 14, E); r(17, 18, 20, 18, E); r(16, 15, 16, 17, E); r(21, 15, 21, 17, E)
    elif face not in ('err', 'snow', 'rew'):
        pts = [(11, 15), (14, 17), (17, 15), (20, 17), (23, 15), (26, 16)] if face not in ('focus', 'blink') else [(12, 16), (15, 15), (18, 16), (21, 15), (24, 16)]
        col = M if face == 'hurt' else E
        for (a, b), (cc, dd) in zip(pts, pts[1:]):
            n = max(abs(cc - a), abs(dd - b))
            for i in range(n + 1):
                x = a + (cc - a) * i // n; y = b + (dd - b) * i // n
                put(im, x, y, col); put(im, x, y + 1, mix(col, c['glass'], 0.5))
    for y, last in TORN:                                                                    # (the torn corner: the glass is gone)
        for x in range(0, last + 1): px[x, y] = (0, 0, 0, 0)
        put(im, last + 1, y, c['guts'])
    return im


def _errglyph(c):
    """an ERROR cube: red, a white '!' on it"""
    def f(x, y, r):
        if 14 <= x <= 17 and (6 <= y <= 18 or 22 <= y <= 25): return '#ffffff'
        if x in (0, 31) or y in (0, 31): return mix(c['red'], c['deep'], 0.5)
        return c['red']
    return cells(f, 6)


def textures(c):
    t = {'s1': _scan(11, c, 0), 's2': _scan(12, c, 1), 's3': _scan(13, c, 2), 's4': _scan(14, c, 2),
         'case': _case(c, 21), 'case2': _case(c, 22), 'vent': _vent(c), 'grille': _grille(c), 'guts': _guts(c),
         'knob': lit(soft('#8a8aa0', '#b8b8cc', '#5a5a70', 23, 0.1), 1.2, 0.8, 8),
         'rod': soft('#a0a0b8', '#d0d0e0', '#70708a', 24, 0.1), 'deep': soft(c['deep'], c['case_d'], c['deep'], 25, 0.1),
         'glow': soft(c['eye'], c['white'], c['cyan'], 26, 0.15), 'mag': soft(c['mag'], mix(c['mag'], '#ffffff', 0.4), c['mag'], 27, 0.15),
         'pxa': _pixel(c['mag'], 31, c), 'pxb': _pixel(c['purple'], 32, c), 'pxc': _pixel(c['cyan'], 33, c), 'pxd': _pixel(c['green'], 34, c),
         'errred': _errglyph(c), 'face': _screen(c)}
    for f in FACES: t[f'face_{f}'] = _screen(c, f)
    return t


TEX = textures(BASE)
for k, im in TEX.items(): R.tex(k, im)
for sfx, ch in PALS.items():
    for k, im in textures(dict(BASE, **ch)).items(): R.tex(k + sfx, im)
    R.skin(sfx, {k: k + sfx for k in TEX})
for sfx, tint, a in (('_g', '#3cf0ff', 110), ('_gr', '#ff2040', 80), ('_gc', '#20e0ff', 80)):
    for k in TEX: R.tex(k + sfx, ghost(TEX[k], tint, a))
    R.skin(sfx, {k: k + sfx for k in TEX})

# ---------------------------------------------------------------------------------------------------- the model
B = R.box
# ---- the slices: torn sprite scan-lines, a hairline gap between them, torn ragged ends, lit top edges, dead pixels
for p, y0, w, t, ends, bits in (('sl1', 4.0, 3.4, 's1', ((1, 0.9, 1.0), (-1, 0.6, 2.0)), ((-4.6, 5.2), (4.4, 6.0))),
                                ('sl2', 7.0, 4.2, 's2', ((1, 0.7, 0.4), (-1, 1.0, 1.6), (-1, 0.5, 0.2)), ((5.4, 8.2), (-5.6, 9.2))),
                                ('sl3', 10.0, 3.8, 's3', ((1, 0.6, 1.8), (-1, 0.8, 0.6)), ((-4.8, 11.8), (4.9, 10.6)))):
    B(p, (-w, y0 + 0.08, -2.8), (w, y0 + 2.92, 2.8), t, shift=False)
    for sx, L, dy in ends:                                                                 # (torn: a step of the row sticking out)
        a, b = sorted((sx * w, sx * (w + L)))
        B(p, (a, y0 + dy, -2.2), (b, y0 + dy + 0.9, 2.0), t, shift=(0.3 * L, 0.5))
    B(p, (-w + 0.2, y0 + 2.72, -2.92), (w - 0.5, y0 + 2.92, -2.8), 'glow', light=9)          # (the lit scan-line along its top)
    for (bx, by) in bits:                                                                  # (dead pixels stuck to its edges)
        B(p, (bx - 0.45, by, -1.4), (bx + 0.45, by + 0.9, -0.5), 'pxc' if bx > 0 else 'pxa', light=6)
B('sl2', (-1.5, 7.9, -3.05), (1.5, 8.9, -2.8), 'glow', light=12)                           # (its 'heart': a bright scan-line)
B('sl2', (-0.9, 9.0, -3.0), (0.9, 9.3, -2.8), 'mag', light=10)

# ---- the head: the bezel (rounded, the corner torn off in a stair), the recessed screen, the tube's housing, the controls
cs = 'case'
B('head', (-5.5, 13.4, -3.4), (2.6, 20.6, 0.0), cs, shift=False)                          # (the bezel's body, left of the tear)
B('head', (2.6, 13.4, -3.4), (5.5, 18.4, 0.0), cs, shift=False)
B('head', (2.6, 18.4, -3.4), (3.8, 19.5, 0.0), 'case2', shift=False)                      # (the stair of the tear)
B('head', (-5.1, 13.0, -3.4), (5.1, 13.4, 0.0), 'case2')                                  # (rounded: caps top and bottom)
B('head', (-5.1, 20.6, -3.4), (2.6, 21.0, 0.0), 'case2', shift=False)
for a, b in (((-5.5, 19.8, -3.62), (2.6, 20.6, -3.4)), ((-5.5, 13.4, -3.62), (5.5, 14.6, -3.4)), ((-5.5, 14.6, -3.62), (-4.7, 19.8, -3.4)),
             ((4.7, 14.6, -3.62), (5.5, 18.4, -3.4)), ((2.6, 18.4, -3.62), (3.8, 19.8, -3.4))):
    B('head', a, b, cs, shift=False)                                                       # (the front frame round the screen)
B('head', (-4.7, 14.6, -3.42), (4.7, 19.8, -3.4), 'FACE', faces=('north',), uv={'north': [0, 0, 9.4, 5.2]}, light=10)
for a, b in (((3.8, 18.4, -3.3), (4.7, 18.5, 0.0)), ((2.6, 19.5, -3.3), (3.8, 19.6, 0.0)), ((3.7, 18.5, -3.3), (3.8, 19.5, 0.0)),
             ((2.5, 19.6, -3.3), (2.6, 20.6, 0.0))):
    B('head', a, b, 'guts', light=13)                                                      # (the guts glowing along the tear)
# the tube's housing: tapered back, vent slots, the neck
B('head', (-4.6, 14.0, 0.0), (4.6, 20.0, 2.4), 'case2', shift=False)
B('head', (-3.4, 14.8, 2.4), (3.4, 19.2, 4.2), 'vent', shift=False)
B('head', (-1.8, 15.8, 4.2), (1.8, 18.2, 5.2), 'case2', shift=False)
B('head', (-1.0, 16.4, 5.2), (1.0, 17.6, 5.5), 'deep')
# the chin: two knobs, a speaker grille, the power LED
for x in (-4.3, -3.2):
    B('head', (x - 0.4, 13.65, -3.9), (x + 0.4, 14.35, -3.62), 'knob')
    B('head', (x - 0.08, 14.05, -3.95), (x + 0.08, 14.35, -3.9), 'deep')
B('head', (0.6, 13.75, -3.64), (3.4, 14.3, -3.62), 'grille', faces=('north',))
B('head', (4.0, 13.85, -3.72), (4.5, 14.2, -3.62), 'mag', light=12)
# antennae: a base, one whole rabbit-ear with a glowing bead, one snapped off and sparking
B('head', (-1.2, 21.0, -0.8), (1.2, 21.6, 0.8), 'deep')
R.seg('head', (-0.4, 21.4, 0.0), (-1.6, 23.6, 0.2), 0.36, 0.36, 'rod')
R.seg('head', (-1.6, 23.6, 0.2), (-2.9, 25.6, 0.5), 0.32, 0.32, 'rod')
B('head', (-3.4, 25.5, 0.0), (-2.4, 26.5, 1.0), 'mag', light=12)
R.seg('head', (0.4, 21.4, 0.0), (1.3, 22.9, -0.3), 0.36, 0.36, 'rod')
for x, y, s in ((1.55, 23.2, 0.32), (1.95, 23.75, 0.24), (1.25, 23.8, 0.2)):
    B('head', (x - s, y - s, -0.3 - s), (x + s, y + s, -0.3 + s), 'glow', light=15)
# the torn chunk: the stair-shaped piece of bezel and glass, floating free above the tear
cx, cy, cz = PIVOT['chunk']; rot = ('z', 18, (cx, cy, cz))
B('chunk', (cx - 1.3, cy - 1.0, -3.6), (cx + 1.4, cy + 0.9, -0.2), 'case', rot=rot, shift=False)
B('chunk', (cx - 1.3, cy - 1.6, -3.6), (cx + 0.1, cy - 1.0, -0.2), 'case2', rot=rot)
B('chunk', (cx - 1.0, cy - 1.4, -3.75), (cx + 0.9, cy + 0.4, -3.6), 'guts', faces=('north',), rot=rot, light=9)
B('chunk', (cx + 1.4, cy - 1.0, -3.0), (cx + 1.5, cy + 0.9, -0.6), 'guts', rot=rot, light=9)

# ---- the fists: 2x2x2 voxels, the front-top row lit (knuckles), a thumb pixel on the inside
for p, sx in (('fistr', 1), ('fistl', -1)):
    x, y, z = PIVOT[p]; s = 1.5
    for i, (dx, dy, dz) in enumerate([(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]):
        t = ('pxa' if dz == 0 else 'pxb') if dy == 1 else ('pxb' if dz == 0 else 'pxb')
        if dx == (1 if sx > 0 else 0) and dy == 0 and dz == 1: t = 'pxc'
        B(p, (x - s + dx * s, y - s + dy * s, z - s + dz * s), (x + dx * s, y + dy * s, z + dz * s), t, shift=False)
    B(p, (x - s * 0.95, y + 0.25, z - s - 0.12), (x + s * 0.95, y + 0.75, z - s), 'glow', faces=('north',), light=8)
    a, b = sorted((-sx * s, -sx * (s + 0.6)))
    B(p, (x + a, y + 0.2, z - s + 0.2), (x + b, y + 1.1, z - 0.2), 'pxa', shift=False)

# ---- the trail: pixels falling off its bottom, smaller as they go, out of line
for i, (x, y, z, s, t) in enumerate(((0.8, 3.0, 0.2, 1.3, 'pxb'), (-1.7, 1.9, -0.4, 1.0, 'pxa'), (1.6, 0.9, 0.6, 0.8, 'pxc'),
                                      (-0.4, -0.3, 0.0, 0.6, 'pxd'), (0.9, -1.3, -0.5, 0.45, 'pxa'))):
    B('trail', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), t, light=4, shift=False)
# ---- the shards: loose pixels orbiting the head
for i, (x, y, z, s) in enumerate(((-8.0, 18.5, 1.0, 1.0), (7.9, 15.0, 2.0, 0.8), (-6.6, 23.0, -2.0, 0.7), (3.2, 26.8, 2.6, 0.9))):
    B('shards', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), ('pxa', 'pxc', 'pxd', 'pxa')[i], light=10, shift=False)
# ---- the corruption: a cage of ERROR cubes round a foe (in front of it), and a scan-line ring
for i in range(10):
    a = i * 36; x, z = 6 * math.cos(math.radians(a)), -10 + 6 * math.sin(math.radians(a)); y = 6 + (i % 4) * 3.5; s = 1.6 - (i % 3) * 0.3
    B('err', (x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), 'errred', light=12, full=True)
ring(R, 'err', (0, 4.0, -10), 6.6, 12, 0.3, 0.3, 'glow', light=12)
ring(R, 'err', (0, 13.0, -10), 5.0, 10, 0.3, 0.3, 'mag', light=12)


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=2.0, **kw):
    return R.ground(kw, lift)


def tear(a=0.0, b=0.0, c=0.0, dz=0.0):
    return {'_o_sl1': (a, 0, dz), '_o_sl2': (b, 0, -dz), '_o_sl3': (c, 0, dz)}


POSES = R.POSES
POSES.update({
    'idle_a': P(**tear(0.4, -0.3, 0.2), head=T(0, 0, 2)),
    'idle_b': P(lift=2.8, **tear(-0.6, 0.5, -0.2), head=T(-4, 8, -4), _face='happy', _o_fistr=(0, 0.8, 0)),
    'idle_c': P(**tear(1.6, -1.4, 0.8), head=T(0, -12, 8), _face='blink', _o_chunk=(1.0, 1.0, 0)),    # (a flicker: the tear opens)
    # (the idle JITTER frames: held 1 tick each, at random, between idle_a holds - see MOTION)
    'jit_1': P(**tear(-1.1, 0.7, 0.3), head=T(0, 3, -3), _o_head=(0.5, 0, 0), _o_fistr=(0.3, -0.4, 0), _o_chunk=(0.6, -0.3, 0)),
    'jit_2': P(lift=2.5, **tear(0.9, 0.2, -1.2), head=T(2, -4, 4), _o_head=(-0.4, 0.2, 0), _o_fistl=(-0.4, 0.5, 0), _face='snow'),
    # (a HARD SNAP: the head turns 30 degrees in one tick, no easing - it looks at you; then snaps back)
    'snap_l': P(**tear(0.4, -0.3, 0.2), head=T(0, 30, 0)), 'snap_r': P(**tear(0.4, -0.3, 0.2), head=T(-6, -30, 6), _face='surprised'),
    # (the stutter-step walk: 4 keyframes; MOTION drops and doubles them)
    'walk_0': P(core=T(14), head=T(-10), **tear(-0.8, 0.0, 0.8, 0.6), _o_fistr=(0, 0, 2.0), _o_fistl=(0, 0, 2.0)),
    'walk_1': P(lift=2.6, core=T(14), head=T(-10, 4), **tear(0.8, 0.0, -0.8, -0.6), _o_fistr=(0, 0.6, 2.4), _o_fistl=(0, 0.6, 2.4)),
    'walk_2': P(lift=2.3, core=T(16), head=T(-8, -6), **tear(-1.6, 0.8, 1.4, 0.4), _o_fistr=(0, 0.2, 1.0), _o_fistl=(0, 0.2, 3.0)),
    'walk_3': P(lift=2.0, core=T(10), head=T(-12, 6), **tear(1.4, -1.0, -0.2, -0.8), _o_fistr=(0, 0.4, 3.0), _o_fistl=(0, 0.4, 1.0), _face='blink'),
    'run_0': P(core=T(28), head=T(-22), **tear(-2.0, 0.6, 1.8, 1.4), _o_fistr=(0, 1, 4.0), _o_fistl=(0, 1, 4.0), _o_trail=(0, 1, 3)),
    # (REWIND: the frames run backwards - REW on the screen, the slices dragged the other way)
    'rew': P(_face='rew', core=T(-8), head=T(6, -8), **tear(1.8, -2.2, 2.6, -0.8), _o_fistr=(0, 0, -1.5), _o_fistl=(0, 0, -1.5)),
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
    'segfault': P(lift=4.0, _face='snow', **{'_o_sl1': (-5.0, -1.0, 1.0), '_o_sl2': (5.5, 0.5, -1.0), '_o_sl3': (-4.0, 2.5, 0.0),
                                            '_o_head': (2.0, 5.0, 0)}, head=T(-10, 0, -14), _o_fistr=(5, 4, 0), _o_fistl=(-5, -2, 0), _o_shards=(0, 3, 0)),
    'happy': P(lift=3.4, _face='happy', head=T(-8, 0, -6), _o_fistr=(1, 5, 0), _o_fistl=(-1, 5, 0), **tear(0.8, -0.8, 0.8)),
    'hurt': P(_face='hurt', core=T(-16), head=T(10, 0, 14), **tear(-2.0, 2.0, -1.0)),
    'tired': P(lift=0.0, _face='blink', core=T(0, 0, 70), head=T(0, 0, 10), **tear(1.0, -0.5, 1.5), _hide=('shards', 'trail')),
})
POSES['sit_a'] = R.ground(POSES['sit_a']); POSES['sit_b'] = R.ground(POSES['sit_b'])
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'jit_1', 'jit_2', 'snap_r', 'walk_0', 'walk_2', 'run_0', 'rew', 'sit_a', 'sit_b', 'stutter_0',
         'stutter_1', 'strike', 'corrupt', 'segfault', 'happy', 'hurt', 'tired']
R.DRAFT = DRAFT

# ---------------------------------------------------------------------------------------------------- MOTION (for the wiring stage)
# Glitchy, never smooth. Each clip is a list of (pose, ticks, how[, extras]):
#   how  'snap'  set the transformation with interpolation_duration 0 (a hard cut - the default for this follower)
#        'ease'  interpolation_duration = ticks (the rare smooth move, on purpose - a sit, a sigh)
#        'hold'  the same frame again (a stutter: the sprite 'sticks')
#        'skip'  advance the clock without showing the frame (a dropped frame: the pose after it lands early)
#   extras  'rgb'  show the RGB-split pair ('_gr' at -0.05 blocks x, '_gc' at +0.05) on the head and slices for 2 ticks
#           'ghost' leave a '_g' afterimage where it was, fading over 4 ticks
#           'lag'   the slices take this pose late by SLICE_LAG ticks each (the desync), while the head and fists take it now
# The runtime adds JITTER on top: every tick, with chance JIT_P, offset one random slice by +-JIT_X units (x only) for 1 tick.
SLICE_LAG = {'head': 0, 'fistr': 0, 'fistl': 0, 'sl3': 1, 'sl2': 2, 'sl1': 3, 'trail': 3}
JIT_P, JIT_X = 0.18, (0.4, 1.2)
MOTION = {
    # idle: mostly still; a jitter frame now and then; a look-at-you snap every 6-10 s
    'idle':   [('idle_a', 14, 'snap'), ('jit_1', 1, 'snap'), ('idle_a', 9, 'snap'), ('jit_2', 1, 'snap', 'rgb'), ('idle_a', 18, 'snap'),
               ('snap_l', 6, 'snap'), ('idle_a', 1, 'snap'), ('idle_c', 2, 'snap'), ('idle_a', 10, 'snap')],
    # walk: a stutter-step - frames doubled and dropped, never evenly spaced (8 frames shown over 12 ticks)
    'walk':   [('walk_0', 2, 'snap', 'lag'), ('walk_0', 1, 'hold'), ('walk_1', 0, 'skip'), ('walk_2', 2, 'snap', 'lag'),
               ('walk_3', 1, 'snap'), ('walk_3', 1, 'hold'), ('walk_1', 2, 'snap', 'lag'), ('walk_2', 1, 'snap'), ('walk_0', 2, 'snap', 'rgb')],
    # run: a teleport-stride - it vanishes for a tick every few steps and lands a block on, an afterimage left behind
    'run':    [('run_0', 2, 'snap', 'lag'), ('walk_1', 1, 'snap'), ('run_0', 1, 'snap', 'ghost'), ('run_0', 0, 'skip'), ('walk_2', 2, 'snap', 'rgb')],
    # rewind: the last 3 keyframes replayed backwards at 1 tick each with REW on the screen, then the clip resumes
    'rewind': [('rew', 1, 'snap', 'rgb'), ('<prev-2>', 1, 'snap'), ('<prev-3>', 1, 'snap'), ('rew', 1, 'snap'), ('<resume>', 0, 'snap')],
    # teleport-stutter (an attack's approach): three blinks, each landing with the slices out of step
    'stutter': [('stutter_0', 2, 'snap', 'rgb'), ('stutter_0', 0, 'skip'), ('stutter_1', 2, 'snap', 'ghost'), ('stutter_0', 1, 'snap', 'lag'),
                ('strike', 3, 'snap', 'rgb')],
    'corrupt': [('jit_1', 1, 'snap'), ('corrupt', 2, 'snap', 'rgb'), ('corrupt', 16, 'hold'), ('idle_a', 1, 'snap', 'lag')],
    'segfault': [('jit_2', 1, 'snap'), ('jit_1', 1, 'snap'), ('jit_2', 1, 'snap'), ('segfault', 4, 'snap', 'rgb'), ('segfault', 6, 'hold'),
                 ('rew', 1, 'snap'), ('idle_a', 1, 'snap', 'lag')],
    'hurt':   [('hurt', 2, 'snap', 'rgb'), ('jit_2', 1, 'snap'), ('hurt', 2, 'hold'), ('idle_a', 1, 'snap', 'lag')],
    # sitting is the one smooth thing it does - it 'settles' like a sigh (ease), then the slices fizz now and then
    'sit':    [('sit_a', 6, 'ease'), ('sit_a', 40, 'hold')],
}
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'chunk': 'head', 'shards': 'head', 'trail': 'legs', 'sl1': 'legs'}   # (no head by name: its screen is; no legs: the trail)
SHINY = ('Shiny Clean Signal', PALS['_sh'])
COSMETIC = 'CRT Bezel Skins: the screen\'s frame in Beige 1989, Clear Purple, Atomic Teal - one bezel per palette form'
