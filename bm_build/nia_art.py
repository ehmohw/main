"""2.95e: NIA - a tortoiseshell house cat, from the owner's photo. Slim; a coat mottled black, chestnut and bright orange all
over (brindled, no two patches alike); a black blaze straight down the middle of her face from forehead to nose, one cheek
bright orange and the other darker; a cream chin under the mouth; a black nose; big yellow-green eyes; dark ears, pink
inside. The rig is the house cats' (cat_art_base)."""
from PIL import ImageDraw
from phase57_art import hexc
import cat_art_base as B

BLACK, DKBR, BROWN, ORANGE, ORANGE_LT, CREAM = '#17120e', '#3a2416', '#6e4424', '#c47a38', '#df9e58', '#eedcb8'
IRIS, RIM = ('#b6c454', '#d6e07e'), '#3a4618'


def tortie(seed, bias=0.0, cell=2):
    """the tortoiseshell: broad patches from a smooth field (black / chestnut / orange), brindled with flecks of the others"""
    f = B.field(seed, 4, 32)
    def c(x, y, r):
        v = f[y][x] + bias + (r.random() - 0.5) * 0.08
        base = BLACK if v < 0.42 else (DKBR if v < 0.49 else (BROWN if v < 0.55 else (ORANGE if v < 0.74 else ORANGE_LT)))
        if r.random() < 0.13: base = r.choice((BLACK, DKBR, BROWN, ORANGE))          # (brindle)
        return base
    return B.cells(c, seed, cell)


def face(kind=None):
    """the face (21 x 17 px at its uv; the muzzle covers the middle of rows 10-16): the black blaze down the middle (cols 9-12,
    wider on the forehead), bright orange on one cheek, darker brindle on the other, the eyes either side"""
    im = tortie(5201, 0.05); px = im.load()
    import random
    r = random.Random(5202)
    for y in range(17):
        for x in range(22):
            if x <= 8 and y >= 2:                                                         # her right cheek: bright orange
                px[x, y] = hexc(r.choice((ORANGE, ORANGE, ORANGE_LT, ORANGE, BROWN)) if r.random() < 0.9 else BLACK)
            elif x >= 13 and y >= 2:                                                      # the other: darker
                px[x, y] = hexc(r.choice((DKBR, BLACK, BROWN, ORANGE, DKBR)))
            elif y < 2:
                px[x, y] = hexc(r.choice((BLACK, DKBR, ORANGE)))
    for y in range(17):                                                                   # the blaze
        w0, w1 = (8, 13) if y < 4 else (9, 12)
        for x in range(w0, w1 + 1):
            if r.random() < 0.95: px[x, y] = hexc(BLACK)
    B.eyes(im, kind, IRIS, RIM, cols=(1, 14), row=4, w=7, h=5, lid='#0d0907')
    return im


def mfront():
    """the front of the muzzle (12 x 7 px): an orange whisker pad one side and a dark one the other, the blaze running down into
    the black nose, the mouth, the cream chin below"""
    im = tortie(5203, 0.1); px = im.load()
    rows = ['OOOOkkkkDDDD',
            'OOoOkNNkDdDD',
            'OOOOkNNkDDdD',
            'oOOOOmmDDDDd',
            'OOmmmmmmmmDD',
            'CCCCCCCCCCCC',
            'CCcCCCCCCcCC']
    key = {'O': ORANGE, 'o': ORANGE_LT, 'D': DKBR, 'd': BLACK, 'k': BLACK, 'N': '#2a1c1a', 'm': '#0a0706', 'C': CREAM, 'c': '#e0caa2'}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row): px[x, y] = hexc(key[ch])
    return im


def crown():
    im = tortie(5204); d = ImageDraw.Draw(im)
    d.rectangle((8, 0, 13, 63), fill=hexc(BLACK))                                         # the blaze over the top of her head
    return im


def look(p):
    from tullius_art import _noise
    ear = tortie(5205, -0.25)
    ear_in = B.solid('#c88a86', 5206, ('#a86a66', '#e0aaa4', DKBR), 0.3)
    T = {f'{p}fur': tortie(5207), f'{p}back': tortie(5208, -0.08), f'{p}belly': tortie(5209, 0.12), f'{p}cheek': tortie(5210, 0.08),
         f'{p}chest': tortie(5211, 0.05), f'{p}throat': tortie(5212, -0.05), f'{p}muzzle': tortie(5213, 0.1), f'{p}mfront': mfront(),
         f'{p}chin': B.solid(CREAM, 5214, ('#e2cca4',), 0.2), f'{p}ear': ear, f'{p}ear_in': ear_in, f'{p}leg': tortie(5215, 0.02),
         f'{p}paw': tortie(5216, -0.1), f'{p}tail': tortie(5217, -0.05), f'{p}tail_tip': B.solid(BLACK, 5218, (DKBR,), 0.2),
         f'{p}face': face(), f'{p}crown': crown()}
    for k in B.FACES: T[f'{p}face_{k}'] = face(k)
    return T


globals().update(B.make('ni_', look, dict(stock=0.92, long=1.0, tall=1.0, scale=1.0)))
