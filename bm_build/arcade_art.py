"""2.94d: THE ARCADE's art (phase216) - its four armour sets' layers, painted here in 8-bit style on the standard 64 x 32 armour
layout (a box's faces: top, bottom, then right, front, left, back round its sides), and the icons and props from PixelLab
(ref/pixellab/arcade/icons: an item's icon as is; a prop a voxel model of its icon, so it stands in the world as pixel art you can
walk round).

THE SETS (homages): the BOUNTY HUNTER's power suit (orange-red, a green visor, great round pauldrons), the BLUE BOMBER's armour
(blue and light blue, an open helm with ear discs), the PLUMBER's outfit (a red cap and shirt, blue overalls with yellow buttons,
brown boots) and the VAMPIRE HUNTER's garb (a red headband, brown leather, a red sash, a silver cross). A face left open (the
Bomber's helm, the Plumber's cap, the Hunter's headband) is drawn clear, so your own face shows through."""
import os
from PIL import Image

from phase57_art import hexc

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, 'ref', 'pixellab', 'arcade', 'icons')

# the standard layout: a box (u, v, w, h, d) - its faces' rectangles
BOXES = {'head': (0, 0, 8, 8, 8), 'body': (16, 16, 8, 12, 4), 'arm': (40, 16, 4, 12, 4), 'leg': (0, 16, 4, 12, 4)}


def faces(u, v, w, h, d):
    return {'top': (u + d, v, u + d + w, v + d), 'bottom': (u + d + w, v, u + d + 2 * w, v + d),
            'right': (u, v + d, u + d, v + d + h), 'front': (u + d, v + d, u + d + w, v + d + h),
            'left': (u + d + w, v + d, u + 2 * d + w, v + d + h), 'back': (u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h)}


class Layer:
    def __init__(self):
        self.im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); self.px = self.im.load()

    def put(self, x, y, c):
        if 0 <= x < 64 and 0 <= y < 32:
            self.px[x, y] = hexc(c) if c else (0, 0, 0, 0)

    def box(self, part, col, dark, light, rows=None, sides=('top', 'bottom', 'right', 'front', 'left', 'back')):
        """a box's faces filled, 8-bit shaded: a light top row and left edge, a dark bottom row and right edge (rows: only
        those rows of its sides, from the top - a boot's or a belt's band)"""
        F = faces(*BOXES[part])
        for s in sides:
            x0, y0, x1, y1 = F[s]
            for y in range(y0, y1):
                if rows and s not in ('top', 'bottom') and not (rows[0] <= y - y0 < rows[1]):
                    continue
                for x in range(x0, x1):
                    c = col
                    if y == y1 - 1 or x == x1 - 1:
                        c = dark
                    elif y == y0 or x == x0:
                        c = light
                    self.put(x, y, c)

    def face(self, part, side):
        return faces(*BOXES[part])[side]


def _helm_open(L, rows, frame=1):
    """the front of the head left clear below `rows` (your own face shows) - inside a frame `frame` wide (0: a cap, open across)"""
    x0, y0, x1, y1 = L.face('head', 'front')
    for y in range(y0 + rows, y1):
        for x in range(x0 + frame, x1 - frame):
            L.put(x, y, None)


def paint(which):
    """-> (humanoid layer, humanoid_leggings layer)"""
    H, Lg = Layer(), Layer()
    if which == 'hunter':                              # the bounty hunter's power suit
        O, OD, OL, Y, YD, G, GL = '#e0601c', '#8a2a0c', '#ff9a50', '#f0c020', '#a07010', '#30d050', '#b0ff90'
        H.box('head', O, OD, OL)
        x0, y0, x1, y1 = H.face('head', 'front')        # the visor
        for y in range(y0 + 3, y0 + 6):
            for x in range(x0 + 1, x1 - 1):
                H.put(x, y, GL if y == y0 + 3 and x < x0 + 4 else G)
        H.box('body', O, OD, OL)
        x0, y0, x1, y1 = H.face('body', 'front')        # the chest light, a dark band at the waist
        for x in range(x0 + 3, x0 + 5):
            H.put(x, y0 + 3, G); H.put(x, y0 + 4, G)
        for x in range(x0, x1):
            H.put(x, y0 + 9, OD)
        H.box('arm', O, OD, OL)
        H.box('arm', Y, YD, '#fff080', rows=(0, 4))     # the great pauldrons
        H.box('leg', O, OD, OL, rows=(6, 12))           # the boots
        x0, y0, x1, y1 = H.face('leg', 'front')
        for x in range(x0, x1):
            H.put(x, y0 + 6, Y)
        Lg.box('leg', O, OD, OL)
        x0, y0, x1, y1 = Lg.face('leg', 'front')        # yellow knees
        for y in range(y0 + 4, y0 + 7):
            for x in range(x0, x1):
                Lg.put(x, y, Y if y != y0 + 6 else YD)
        Lg.box('body', OD, '#5a1a08', O, rows=(9, 12))
    elif which == 'bomber':                            # the blue bomber
        B, BD, BL, C, CD = '#2060e0', '#103080', '#60a0ff', '#40d0ff', '#1080b0'
        H.box('head', B, BD, BL)
        _helm_open(H, 3)
        for s in ('right', 'left'):                    # the ear discs
            x0, y0, x1, y1 = H.face('head', s)
            for y in range(y0 + 3, y0 + 6):
                for x in range(x0 + 2, x0 + 6):
                    H.put(x, y, C if (y, x) != (y0 + 3, x0 + 2) else '#c0f4ff')
        x0, y0, x1, y1 = H.face('head', 'front')        # a light blue brow stripe
        for x in range(x0 + 2, x1 - 2):
            H.put(x, y0 + 1, C)
        H.box('body', C, CD, '#a0f0ff')
        H.box('arm', B, BD, BL)
        H.box('arm', C, CD, '#a0f0ff', rows=(0, 3))
        H.box('leg', B, BD, BL, rows=(5, 12))           # the big boots
        x0, y0, x1, y1 = H.face('leg', 'front')
        for x in range(x0, x1):
            H.put(x, y0 + 5, C)
        Lg.box('leg', C, CD, '#a0f0ff')
        Lg.box('body', B, BD, BL, rows=(9, 12))
    elif which == 'plumber':                           # the plumber's outfit
        R, RD, RL, U, UD, UL, Yb, Br, BrD = '#e02020', '#801010', '#ff6060', '#2040c0', '#102070', '#5070ff', '#ffe040', '#7a4a20', '#4a2a10'
        H.box('head', R, RD, RL, sides=('top', 'right', 'left', 'back', 'front'))
        _helm_open(H, 3, frame=0)
        x0, y0, x1, y1 = H.face('head', 'front')        # the cap's white badge
        H.put(x0 + 3, y0 + 1, '#ffffff'); H.put(x0 + 4, y0 + 1, '#ffffff'); H.put(x0 + 3, y0 + 2, '#ffffff'); H.put(x0 + 4, y0 + 2, '#ffffff')
        for s in ('right', 'left', 'back'):            # a cap: only the top of the head's sides
            x0, y0, x1, y1 = H.face('head', s)
            for y in range(y0 + 3, y1):
                for x in range(x0, x1):
                    H.put(x, y, None)
        H.box('body', R, RD, RL)
        x0, y0, x1, y1 = H.face('body', 'front')        # the overalls' straps and buttons
        for y in range(y0, y1):
            H.put(x0 + 1, y, U); H.put(x1 - 2, y, U)
        for y in range(y0 + 7, y1):
            for x in range(x0, x1):
                H.put(x, y, U if y < y1 - 1 else UD)
        H.put(x0 + 1, y0 + 6, Yb); H.put(x1 - 2, y0 + 6, Yb)
        H.box('arm', R, RD, RL)
        H.box('leg', Br, BrD, '#a06a30', rows=(8, 12))
        Lg.box('leg', U, UD, UL)
        Lg.box('body', U, UD, UL, rows=(7, 12))
    elif which == 'vhunter':                           # the vampire hunter's garb
        L_, LD, LL, R, RD, S = '#7a4a24', '#40220c', '#a8743c', '#c01818', '#6a0808', '#d8d8e0'
        for s in ('front', 'right', 'left', 'back'):   # the headband: one band round the brow, its tails at the back
            x0, y0, x1, y1 = H.face('head', s)
            for x in range(x0, x1):
                H.put(x, y0 + 1, R); H.put(x, y0 + 2, RD)
        x0, y0, x1, y1 = H.face('head', 'back')
        for y in range(y0 + 3, y0 + 7):
            H.put(x0 + 3, y, R); H.put(x0 + 5, y + 1 if y < y1 - 1 else y, RD)
        H.box('body', L_, LD, LL)
        x0, y0, x1, y1 = H.face('body', 'front')        # the red sash, the silver cross
        for i in range(8):
            H.put(x0 + i, y0 + 2 + i, R); H.put(x0 + i, y0 + 3 + i, RD)
        for y in range(y0 + 1, y0 + 6):
            H.put(x0 + 4, y, S)
        for x in range(x0 + 3, x0 + 6):
            H.put(x, y0 + 2, S)
        H.box('arm', L_, LD, LL)
        H.box('arm', LD, '#2a1406', L_, rows=(9, 12))   # bracers
        H.box('leg', L_, LD, LL, rows=(4, 12))          # tall boots, silver buckles
        x0, y0, x1, y1 = H.face('leg', 'front')
        H.put(x0 + 1, y0 + 7, S); H.put(x0 + 2, y0 + 7, S)
        Lg.box('leg', '#5a3418', '#2a1406', L_)
        Lg.box('body', R, RD, '#ff5050', rows=(9, 12))
    return H.im, Lg.im


def icon(k):
    return Image.open(os.path.join(ICONS, f'{k}.png')).convert('RGBA')
