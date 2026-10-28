"""2.95e: HENRY - a black house cat, from the owner's photo. A little stockier than Nia; glossy black, with a soft sheen on
the fur where the light catches it; a small white patch on his throat; the bridge of his nose a touch silvery-grey; big
yellow-green eyes going golden at the rims; ears black outside, a dusky pink inside. The rig is the house cats'
(cat_art_base)."""
from PIL import ImageDraw
from phase57_art import hexc
import cat_art_base as B

BLACK, BLACK2, SHEEN, SHEEN2, WHITE = '#131316', '#1b1b20', '#2d2d36', '#41414e', '#f2f1ec'
IRIS, RIM = ('#aeba40', '#d8c45a'), '#6a5214'


def coat(seed, sheen=0.06, cell=2):
    """glossy black: near-black cells, a sheen running in short streaks along the fur"""
    f = B.field(seed, 5, 32)
    def c(x, y, r):
        if f[y][x] > 0.62 and r.random() < 0.55: return SHEEN if r.random() < 0.8 else SHEEN2
        if r.random() < sheen: return SHEEN
        return BLACK if r.random() < 0.7 else BLACK2
    return B.cells(c, seed, cell)


def face(kind=None):
    """the face (20 x 16 px): black, the silvery bridge starting between the eyes and running down to the muzzle, the eyes"""
    im = coat(6201, 0.04); px = im.load()
    import random
    r = random.Random(6202)
    for cy in range(4, 9):                                                               # (2-px cells, as the fur)
        for cx in (5, 6):
            if r.random() < 0.35 + 0.15 * (cy - 4):
                c = hexc(r.choice(('#55555e', '#6c6c76', '#4a4a52')))
                for y in (2 * cy, 2 * cy + 1):
                    for x in (2 * cx, 2 * cx + 1): px[x, y] = c
    B.eyes(im, kind, IRIS, RIM, cols=(2, 15), row=4, w=7, h=5, lid='#050506')
    return im


def mfront():
    """the front of the muzzle (12 x 7 px): the silvery bridge running down onto a dusky nose, black lips, the mouth"""
    im = coat(6203, 0.03); px = im.load()
    rows = ['bbbbgGGgbbbb',
            'bbbsgNNgsbbb',
            'bbbbbNNbbbbb',
            'bsbbbmmbbbsb',
            'bbmmmmmmmmbb',
            'bbbbbbbbbbbb',
            'bbsbbbbbbbbb']
    key = {'b': BLACK, 's': SHEEN, 'g': '#5c5c66', 'G': '#7a7a84', 'N': '#3a3034', 'm': '#050506'}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row): px[x, y] = hexc(key[ch])
    return im


def chest():
    """the chest (13 x 15 px at its uv, the head hiding its top rows): black, the small white patch high in the middle"""
    im = coat(6205, 0.03); d = ImageDraw.Draw(im)
    d.rectangle((5, 3, 8, 7), fill=hexc(WHITE)); d.rectangle((4, 4, 9, 6), fill=hexc(WHITE)); d.point((6, 8), fill=hexc(WHITE))
    d.point((4, 3), fill=hexc('#9a9a98')); d.point((9, 7), fill=hexc('#9a9a98'))
    return im


def look(p):
    T = {f'{p}fur': coat(6206), f'{p}back': coat(6207, 0.12), f'{p}belly': coat(6208, 0.02), f'{p}cheek': coat(6209),
         f'{p}chest': chest(), f'{p}throat': coat(6210, 0.03), f'{p}muzzle': coat(6211, 0.03), f'{p}mfront': mfront(),
         f'{p}chin': coat(6212, 0.02), f'{p}ear': coat(6213, 0.05), f'{p}ear_in': B.solid('#6a484c', 6214, ('#7e5a5c', '#4a3436'), 0.3),
         f'{p}leg': coat(6215), f'{p}paw': coat(6216, 0.02), f'{p}tail': coat(6217, 0.1), f'{p}tail_tip': coat(6218),
         f'{p}face': face(), f'{p}crown': coat(6219, 0.1)}
    for k in B.FACES: T[f'{p}face_{k}'] = face(k)
    return T


globals().update(B.make('hy_', look, dict(stock=1.12, long=1.04, tall=1.04, scale=1.0,
                                                  collar=dict(band='#c02828', band_dk='#7a1414', tag='#d8dce0', tag_dk='#8a9098', size=0.6))))
