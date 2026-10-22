"""2.87: the royal family's faces - Queen Ava and Queen Pearl - drawn as Emma's is (phase57_art._face): crisp pixel art, 36 x 32
on a 64 x 64 sheet, the head's front taking uv [0, 0, 9, 8] (4 texels a unit, Emma's own scale, so the three read as family).

Each face: big anime eyes (a dark lash line over the top, a lash flick at the outer corner, the iris graded dark to light down
it, a big dark pupil, two white glints), soft brows, a blush with freckles, a small nose and mouth - and the bangs painted
across the top rows (the 3D hair sits over and around them). The expressions change as little as they need to."""
import math
import random
from PIL import Image

from phase57_art import hexc, _sh

LASH = '#2a1610'


def _put(im, x, y, c):
    if 0 <= x < 64 and 0 <= y < 64:
        im.putpixel((x, y), hexc(c) if isinstance(c, str) else c)


def _eye(im, cx, y0, iris, flip, kind=None, lash=LASH, h=13):
    """one eye: (cx, y0) its top-centre. iris = (dark, mid, light, pupil). flip: the left-hand eye on the sheet (her right eye)
    is drawn as is; the other mirrored (glint and lash flick to the outside)."""
    dark, mid, light, pupil = iris
    w = 10
    x0 = cx - w // 2
    if kind == 'happy':                                                                  # closed, curved up: ^
        for i, dy in enumerate((5, 3, 2, 1, 1, 1, 1, 2, 3, 5)):
            _put(im, x0 + i, y0 + 4 + dy, lash); _put(im, x0 + i, y0 + 5 + dy, lash)
        return
    if kind in ('blink', 'wink'):                                                        # closed, curved down (lashes)
        for i, dy in enumerate((0, 1, 2, 2, 3, 3, 2, 2, 1, 0)):
            _put(im, x0 + i, y0 + 7 + dy, lash)
        _put(im, (x0 - 1) if not flip else (x0 + w), y0 + 6, lash)
        return
    if kind == 'hurt':                                                                   # squeezed shut: > <
        for i in range(5):
            xa = x0 + 2 + i if not flip else x0 + 7 - i
            _put(im, xa, y0 + 5 + i, lash); _put(im, xa, y0 + 13 - i, lash)
        return
    top = y0 + (1 if kind == 'pout' else 0)                                               # (pouting: the lid lowered a touch)
    hh = h + (1 if kind == 'shout' else 0)
    # the white, then the iris graded down it, the pupil, the glints
    for y in range(top, y0 + hh):
        t = (y - y0) / (hh - 1)
        half = round((w / 2) * math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2 * 0.9)))
        for x in range(cx - half, cx + half):
            _put(im, x, y, '#ffffff')
            if abs(x - cx + 0.5) < half - 1 and top < y < y0 + hh - 1:
                c = dark if t < 0.45 else (mid if t < 0.75 else light)
                _put(im, x, y, c)
    for y in range(y0 + 4, y0 + 10):
        for x in range(cx - 2, cx + 2):
            if not ((y in (y0 + 4, y0 + 9)) and x in (cx - 2, cx + 1)):
                _put(im, x, y, pupil)
    gx = cx - 3 if not flip else cx + 1
    for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (1, 2)):
        _put(im, gx + dx, y0 + 2 + dy, '#ffffff')
    _put(im, cx + (1 if not flip else -2), y0 + hh - 4, '#ffffff')
    # the lash line over the top, thick; the flick at the outer corner; a soft lower lash
    for x in range(cx - 5, cx + 5):
        _put(im, x, top - 1, lash); _put(im, x, top, lash)
    _put(im, cx - 6, top, lash); _put(im, cx + 5, top, lash)
    ox = cx - 6 if not flip else cx + 5
    sx = -1 if not flip else 1
    _put(im, ox + sx, top - 1, lash); _put(im, ox + 2 * sx, top - 2, lash)
    for x in range(cx - 3, cx + 3):
        _put(im, x, y0 + hh, _sh(hexc('#c08a70'), 1.0) + (255,))


def _brow(im, cx, y, col, flip, angle=0):
    xs = range(cx - 3, cx + 3)
    for i, x in enumerate(xs):
        t = i if not flip else 5 - i
        _put(im, x, y + (1 if t == 0 else 0) - (angle * t // 5), col)


def _blush(im, cx, y, col='#f6aaa6', dots='#c8705c', freckles=True):
    for x in range(cx - 4, cx + 4):
        for yy in (y, y + 1, y + 2):
            if not (yy != y + 1 and x in (cx - 4, cx + 3)):
                _put(im, x, yy, col)
    if freckles:
        for fx, fy in ((-2, 1), (0, 2), (2, 1)):
            _put(im, cx + fx, y + fy, dots)


def _mouth(im, kind, x, y, ink='#8a3428', smile='soft'):
    if kind == 'shout':
        for dy, row in enumerate(('.mmmm.', 'mrrrrm', 'mrppm.', '.mmm..')[:4]):
            for dx, ch in enumerate(row):
                if ch != '.':
                    _put(im, x + dx, y + dy, {'m': ink, 'r': '#5a1a1a', 'p': '#e07a7a'}[ch])
    elif kind == 'happy':
        for dy, row in enumerate(('mmmmmm', 'mwwwwm', '.mppm.')):
            for dx, ch in enumerate(row):
                if ch != '.':
                    _put(im, x + dx, y + dy, {'m': ink, 'w': '#ffffff', 'p': '#e07a7a'}[ch])
    elif kind == 'hurt':
        for dx, dy in ((0, 1), (1, 0), (2, 1), (3, 0), (4, 1), (5, 0)):
            _put(im, x + dx, y + dy, ink)
    elif kind == 'pout':
        for dx, dy in ((1, 1), (2, 0), (3, 0), (4, 1)):
            _put(im, x + dx, y + dy, ink)
    elif smile == 'sly':                                                                  # a crooked, knowing smile - up at one end
        for dx, dy in ((0, 0), (1, 1), (2, 1), (3, 1), (4, 0), (5, -1)):
            _put(im, x + dx, y + dy, ink)
    else:                                                                                 # a soft, closed smile
        for dx, dy in ((0, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 0)):
            _put(im, x + dx, y + dy, ink)


def _nose(im, x, y, col):
    _put(im, x, y, col); _put(im, x + 1, y + 1, col)


# ------------------------------------------------------------------------------------------------ Ava
AVA_SKIN, AVA_SKIN_DK = '#f6d2b8', '#e8b898'
AVA_IRIS = ('#0e5662', '#16a0aa', '#6ae2dc', '#082e36')
AVA_HAIR = ('#4e2a12', '#6a3c1c', '#86522a', '#a06a3a')


def ava_face(kind=None):
    """Ava: Emma's face grown up - the same big teal eyes (a touch longer lashes), freckles across her nose, a shy, gentle
    smile; her brown bangs swept across her brow from a parting over her right eye, longer on her left (the viewer's right)"""
    im = Image.new('RGBA', (64, 64), hexc(AVA_SKIN))
    for y in range(9):
        for x in range(36): _put(im, x, y, AVA_SKIN_DK)
    hk = (kind if kind != 'shout' else None)
    _eye(im, 9, 13, AVA_IRIS, False, kind, h=13)
    _eye(im, 27, 13, AVA_IRIS, True, kind, h=13)
    if kind != 'happy':
        _brow(im, 9, 10, '#6e3a18', False, angle=(2 if kind == 'hurt' else 0)); _brow(im, 27, 10, '#6e3a18', True, angle=(2 if kind == 'hurt' else 0))
    _blush(im, 6, 26); _blush(im, 30, 26)
    rnd = random.Random(1620)
    for _ in range(6):                                                                     # freckles across the nose
        _put(im, 15 + rnd.randint(0, 6), 24 + rnd.randint(0, 2), '#d08a68')
    _nose(im, 17, 24, '#d89a7a')
    _mouth(im, kind, 15, 28)
    # the bangs: a heavy sweep - high at her right (the sheet's left), down over the brow to her left, in clumps
    hd, hm, hl, hs = (hexc(c)[:3] for c in AVA_HAIR)
    for x in range(36):
        edge = int(4 + 7 * (x / 35) ** 1.3 + 1.2 * math.sin(x / 2.1))
        if x < 4: edge = 9 - x                                                             # (the parting: a lock down her right temple)
        for y in range(min(edge, 12)):
            j = (x + y // 2) % 5
            c = hm if j else hd
            if y in (2, 3) and j in (2, 3): c = hl
            if y == edge - 1: c = hd
            _put(im, x, y, c + (255,))
    for y in range(9, 16):                                                                 # the sweep's end at her left cheek
        for x in range(33 - (y - 9) // 3, 36):
            _put(im, x, y, (hm if (x + y) % 4 else hd) + (255,))
    return im


# ------------------------------------------------------------------------------------------------ Pearl
PEARL_SKIN, PEARL_SKIN_DK = '#f2cbb0', '#e2b090'
PEARL_IRIS = ('#14287a', '#2860d8', '#7ab8ff', '#0a1238')
MINT = ('#5aa29c', '#8ad0c8', '#b4ece4', '#e0fffa')
PEARL_HAIR = ('#4e2c12', '#6e4420')


def pearl_face(kind=None):
    """Pearl: big blue eyes - the open one starry, a sparkle in it - the right one under the mint swoop that falls across her right
    eye (the sheet's left) from a parting high on her left; rosy cheeks; a sly, crooked smile"""
    im = Image.new('RGBA', (64, 64), hexc(PEARL_SKIN))
    for y in range(8):
        for x in range(36): _put(im, x, y, PEARL_SKIN_DK)
    wk = kind if kind in ('happy', 'blink', 'hurt', 'wink') else None                    # (2.88: both eyes open - she winks only for her Wink)
    _eye(im, 9, 13, PEARL_IRIS, False, wk, h=13)
    _eye(im, 27, 13, PEARL_IRIS, True, kind if kind != 'wink' else None, h=13)
    if kind not in ('happy', 'blink', 'hurt', 'wink'):                                    # the star in her open eye
        for dx, dy in ((0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)):
            _put(im, 29 + dx, 22 + dy, '#cfe6ff')
    if kind != 'happy':
        _brow(im, 27, 9, '#7a4a28', True, angle=(-2 if kind == 'pout' else 1))
    _blush(im, 6, 26, '#f4a0aa', freckles=False); _blush(im, 30, 26, '#f4a0aa', freckles=False)
    _nose(im, 17, 24, '#d49a80')
    _mouth(im, kind, 15, 28, smile='sly')
    # the brown hair at the top, parted high on her left; the mint swoop sweeping down across her right eye from it
    for y in range(6):
        for x in range(36): _put(im, x, y, PEARL_HAIR[(x // 3 + y) % 2])
    md, mm, ml, mw = (hexc(c)[:3] for c in MINT)
    for x in range(36):
        # the swoop's lower edge: low over her right eye (it covers the top of the wink), rising toward her left
        edge = int(21 - 15 * (x / 30) ** 0.9) if x <= 30 else 5
        for y in range(edge):
            j = (2 * x + y) // 3 % 5                                                      # (strands, following the sweep)
            c = (md, mm, mm, ml, mm)[j]
            if j == 3 and (x + y) % 7 == 0: c = mw
            if y == edge - 1 or y == edge - 2 and j == 0: c = md
            _put(im, x, y, c + (255,))
    return im
