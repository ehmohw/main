"""EMMA'S 2D COSTUME (mockup - not in the pack): a 2D cartoon puppet of Emma, drawn fresh in her design.

Her painting is the model sheet, not the material: proportions, palette and details come from it (big teal eyes with lilac
lids and lashes, freckles and blush, swept bangs, the curl at her cheek, the high ponytail with its pink bow, the stud in her
ear; the white collar, cyan scarf, flower brooch with its gold gem, lace band, woven belt with its white flower buckle; the
full blue skirt, white knee socks and chunky mary-janes), but every part is drawn clean, cel-shaded, outlined, and built to
move:
  HEAD       face and hair; one model per expression, with eyes and mouths drawn for each (not painted over);
  PONYTAIL   hinged at the bow, so it swings;
  TORSO      neck to belt;
  SKIRT      hinged at the belt, drawn in four cuts (still, swished left / right, flared) so it flows with her steps and twirls;
  ARMS       upper arm and forearm, round at the elbow so a bend has no corner; the forearm has a relaxed hand and an open
             (waving) hand;
  LEGS       one leg drawn, mirrored for the other.
Design units: canvas pixels, her feet at FEET_Y, the top of her hair at TOP_Y, her middle at CX; facing you, her right is
image-left. Rig: rigkit, flat planes, torso (root) > head > ponytail; torso > skirt; torso > arm > forearm; legs as roots."""
import math
import types
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

from rigkit import qs, el

SS = 3                                                  # (drawn at 3x, then scaled down: smooth edges)
TEX = 512
FEET_Y, TOP_Y, HEIGHT_BLOCKS = 1940, 236, 1.82
CX = 497.5
PREFIX = 'pe_'

# her palette (picked from the painting)
LINE = (58, 24, 34)
SKIN, SKIN_SH, SKIN_DK, BLUSH = (246, 214, 194), (226, 168, 146), (176, 104, 92), (238, 150, 150)
HAIR, HAIR_SH, HAIR_HI, HAIR_DK = (171, 89, 39), (122, 58, 26), (208, 130, 66), (86, 38, 20)
IRIS, IRIS_DK, IRIS_LT, PUPIL = (70, 196, 194), (30, 134, 148), (156, 240, 226), (16, 66, 78)
LASH, LID = (62, 26, 52), (204, 160, 214)
TOP, TOP_SH, TOP_HI = (54, 136, 200), (36, 98, 164), (110, 182, 232)
SCARF, SCARF_SH, SCARF_HI = (118, 210, 226), (60, 156, 184), (186, 240, 246)
SKIRT, SKIRT_SH, SKIRT_LT, SKIRT_IN = (66, 112, 164), (40, 72, 120), (98, 148, 196), (22, 40, 74)
BELT, BELT_DK, BELT_HI = (112, 72, 38), (66, 40, 18), (150, 104, 60)
WHITE, WHITE_SH = (244, 244, 248), (196, 202, 220)
SHOE, SHOE_SH, SHOE_HI = (70, 88, 136), (38, 48, 90), (118, 138, 186)
PINK, PINK_DK, PINK_HI, GOLD = (218, 92, 186), (150, 44, 120), (246, 168, 228), (240, 196, 70)
BOW, BOW_DK, BOW_HI = (190, 96, 196), (128, 50, 140), (232, 160, 236)
MOUTH, TONGUE = (112, 36, 48), (226, 112, 122)


# ---------------------------------------------------------------------------------------------------- drawing kit
def cr(pts, closed=True, n=10):
    """a smooth curve through the points (Catmull-Rom); a point given twice in a row is a sharp tip"""
    P = [tuple(map(float, p)) for p in pts]
    m, out = len(P), []
    for i in (range(m) if closed else range(m - 1)):
        p0 = P[i - 1] if (closed or i > 0) else P[0]
        p1, p2 = P[i], P[(i + 1) % m]
        p3 = P[(i + 2) % m] if (closed or i + 2 < m) else P[-1]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    if not closed: out.append(P[-1])
    return out


def ribbon(path, w0, w1=None, n=10, smooth=True):
    """a tapered strand along a path: width w0 at its start, w1 at its end"""
    c = cr(path, closed=False, n=n) if smooth else [tuple(map(float, p)) for p in path]
    w1 = w0 if w1 is None else w1
    L, R = [], []
    for i, (x, y) in enumerate(c):
        a, b = c[max(i - 1, 0)], c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = (w0 + (w1 - w0) * i / (len(c) - 1)) / 2
        L.append((x + nx * w, y + ny * w)); R.append((x - nx * w, y - ny * w))
    return L + R[::-1]


def ell(cx, cy, rx, ry, a0=0, a1=360, n=48, rot=0):
    r = math.radians(rot)
    out = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    return out


def mirror_pts(pts, ax=CX):
    return [(2 * ax - x, y) for x, y in pts]


class Part:
    """one flat piece, drawn in canvas coordinates inside its box"""
    def __init__(self, box):
        self.box = box
        self.x0, self.y0 = box[0], box[1]
        self.W, self.H = int((box[2] - box[0]) * SS), int((box[3] - box[1]) * SS)
        self.rgb = np.zeros((self.H, self.W, 3), float)
        self.a = np.zeros((self.H, self.W), float)

    def _xy(self, pts):
        return [((x - self.x0) * SS, (y - self.y0) * SS) for x, y in pts]

    def mask(self, pts):
        m = Image.new('L', (self.W, self.H), 0); ImageDraw.Draw(m).polygon(self._xy(pts), fill=255)
        return np.asarray(m) > 0

    def line_mask(self, pts, w, closed=False):
        m = Image.new('L', (self.W, self.H), 0); d = ImageDraw.Draw(m)
        xy = self._xy(pts + ([pts[0]] if closed else []))
        d.line(xy, fill=255, width=max(1, int(w * SS)), joint='curve')
        r = w * SS / 2
        for x, y in (xy[0], xy[-1]):
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
        return np.asarray(m) > 0

    def paint(self, m, col, clip=None, alpha=1.0):
        if clip is not None: m = m & clip
        k = m.astype(float) * alpha
        self.rgb = self.rgb * (1 - k[..., None]) + np.array(col, float) * k[..., None]
        self.a = np.maximum(self.a, k)
        return m

    def poly(self, pts, col, clip=None, alpha=1.0):
        return self.paint(self.mask(pts), col, clip, alpha)

    def stroke(self, pts, col, w, clip=None, closed=False, alpha=1.0):
        return self.paint(self.line_mask(pts, w, closed), col, clip, alpha)

    def soft(self, pts, col, clip=None, alpha=0.5, blur=6):
        m = ndimage.gaussian_filter(self.mask(pts).astype(float), blur * SS / 3)
        if clip is not None: m = m * clip
        self.rgb = self.rgb * (1 - m[..., None] * alpha) + np.array(col, float) * m[..., None] * alpha

    def shift(self, m, dx, dy):
        return ndimage.shift(m.astype(float), (dy * SS, dx * SS), order=0) > 0.5

    def outline(self, w=5.0, col=LINE):
        """the cartoon outline around the whole piece"""
        solid = self.a > 0.5
        ring = (ndimage.distance_transform_edt(~solid) <= w * SS) & ~solid
        self.rgb[ring] = col; self.a[ring] = 1.0

    def image(self):
        a = np.dstack([np.clip(self.rgb, 0, 255), np.clip(self.a, 0, 1) * 255]).astype(np.uint8)
        return Image.fromarray(a, 'RGBA').resize((int(self.W / SS), int(self.H / SS)), Image.LANCZOS)

    def mirrored(self, ax=CX):
        q = Part((2 * ax - self.box[2], self.box[1], 2 * ax - self.box[0], self.box[3]))
        q.rgb, q.a = self.rgb[:, ::-1].copy(), self.a[:, ::-1].copy()
        return q


# ---------------------------------------------------------------------------------------------------- the head
EYE_FAR, EYE_NEAR = (424, 492, 35, 45), (539, 486, 41, 51)     # (cx, cy, rx, ry): she looks a little to your left
MOUTH_C = (478, 579)


def _eye_open(p, e, near, lid=0.0, wide=False, look=(0, 0)):
    cx, cy, rx, ry = e
    sc = p.poly(ell(cx, cy, rx, ry), WHITE)
    p.poly(ell(cx, cy + ry * 0.45, rx, ry * 0.7), WHITE_SH, clip=sc & ~p.mask(ell(cx, cy - ry * 0.25, rx * 1.2, ry * 0.95)))
    k = 0.6 if wide else 0.84
    ix, iy = cx + look[0] + (3 if near else -2), cy + 4 + look[1]
    ir = p.poly(ell(ix, iy, rx * k, ry * k * 0.98), IRIS, clip=sc)
    p.poly(ell(ix, iy - ry * k * 0.55, rx * k * 1.2, ry * k * 0.65), IRIS_DK, clip=ir)
    p.poly(ell(ix, iy + ry * k * 0.6, rx * k * 0.7, ry * k * 0.35), IRIS_LT, clip=ir)
    p.stroke(ell(ix, iy, rx * k, ry * k * 0.98), IRIS_DK, 2.6, clip=sc)
    p.poly(ell(ix, iy + 2, rx * k * 0.36, ry * k * 0.4), PUPIL, clip=sc)
    p.poly(ell(ix - rx * k * 0.34, iy - ry * k * 0.36, rx * k * 0.26, ry * k * 0.24), WHITE, clip=sc)
    p.poly(ell(ix + rx * k * 0.34, iy + ry * k * 0.36, rx * k * 0.12, ry * k * 0.11), WHITE, clip=sc)
    below = None
    if lid > 0:                                                           # (lowered lids: determined, sleepy)
        top = cy - ry + 2 * ry * lid
        tilt = (1 if near else -1) * ry * 0.25 * lid
        above = p.mask([(cx - rx - 8, cy - ry - 12), (cx + rx + 8, cy - ry - 12), (cx + rx + 8, top - tilt), (cx - rx - 8, top + tilt)])
        p.paint(above, SKIN, clip=p.mask(ell(cx, cy, rx + 4, ry + 4)))
        below = ~above
    else:
        p.stroke(ell(cx, cy, rx * 1.02, ry * 1.02, 196, 344, 24), LID, 9, alpha=0.9)   # (lilac lid)
        p.stroke(ell(cx, cy, rx, ry, 192, 348, 24), LASH, 6.5)
    p.stroke(ell(cx, cy, rx * 0.98, ry, 40, 140, 16), LASH, 2.6)
    p.stroke(ell(cx, cy, rx, ry, 0, 360), LASH, 2.2, clip=below)
    if lid > 0:
        p.stroke([(cx - rx * 1.04, top + tilt), (cx + rx * 1.04, top - tilt)], LASH, 7)
    # lashes at the outer corner
    s = 1 if near else -1
    ox, oy = cx + s * rx * 0.92, cy - ry * (0.42 if lid == 0 else 0.1)
    for i, (dx, dy) in enumerate(((13, -9), (15, 2))):
        p.poly([(ox, oy - 4 + i * 8), (ox + s * dx, oy + dy - 2 + i * 6), (ox + s * dx * 0.3, oy + 5 + i * 8)], LASH)


def _eye_closed(p, e, near, kind):
    cx, cy, rx, ry = e
    s = 1 if near else -1
    if kind == 'squeeze':                                               # > <
        tip = (cx - s * rx * 0.55, cy + 2)
        p.stroke([(cx + s * rx * 0.7, cy - ry * 0.35), tip, (cx + s * rx * 0.7, cy + ry * 0.35)], LASH, 6.5)
        return
    k = 1 if kind == 'happy' else -1                                    # happy: an arch; blink: a resting curve
    pts = [(cx - rx * 0.95 + 1.9 * rx * i / 16, cy + ry * 0.12 - k * ry * 0.36 * math.sin(math.pi * i / 16)) for i in range(17)]
    p.stroke(pts, LASH, 6.5)
    ex, ey = pts[-1] if near else pts[0]
    p.stroke([(ex, ey), (ex + s * 11, ey - 7)], LASH, 4)
    p.stroke([(ex - s * 3, ey + 1), (ex + s * 9, ey + 4)], LASH, 3.4)


def _brows(p, kind):
    for (cx, cy, rx, ry), near in ((EYE_FAR, False), (EYE_NEAR, True)):
        s = 1 if near else -1
        y = cy - ry - 14
        if kind == 'angry':
            pts = [(cx - s * rx * 0.75, y + 10), (cx + s * rx * 0.8, y - 6)]
        elif kind == 'worried':
            pts = [(cx - s * rx * 0.75, y - 8), (cx + s * rx * 0.8, y + 4)]
        elif kind == 'up':
            pts = [(cx - rx * 0.8, y - 10), (cx, y - 17), (cx + rx * 0.8, y - 10)]
        else:
            continue
        p.stroke(cr(pts, closed=False) if len(pts) > 2 else pts, HAIR_DK, 5.5)


def _mouth(p, kind):
    mx, my = MOUTH_C
    if kind in ('grin', 'open'):
        big = kind == 'grin'
        w, d = (40, 32) if big else (28, 22)
        shape = cr([(mx - w, my - 10), (mx, my - 6), (mx + w, my - 14), (mx + w * 0.7, my + d * 0.55), (mx + 4, my + d),
                    (mx - w * 0.65, my + d * 0.6)])
        m = p.poly(shape, MOUTH)
        p.poly([(mx - w - 5, my - 30), (mx + w + 5, my - 30), (mx + w + 5, my - 1), (mx - w - 5, my + 3)], WHITE, clip=m)
        p.poly(ell(mx + 4, my + d - 2, w * 0.55, d * 0.42), TONGUE, clip=m)
        p.stroke(shape, LINE, 3.5, closed=True)
        p.stroke([(mx - w * 0.8, my + 1), (mx + w * 0.8, my - 3)], (210, 200, 205), 1.6, clip=m)
        p.stroke([(mx - w - 4, my - 6), (mx - w - 9, my - 13)], SKIN_DK, 3)
    elif kind == 'smile':
        p.stroke(cr([(mx - 32, my - 6), (mx - 6, my + 9), (mx + 28, my - 10)], closed=False), MOUTH, 4.5)
        p.stroke([(mx + 28, my - 10), (mx + 33, my - 15)], MOUTH, 3)
    elif kind == 'o':
        m = p.poly(ell(mx, my + 4, 11, 14), MOUTH)
        p.poly(ell(mx, my + 12, 7, 5), TONGUE, clip=m)
        p.stroke(ell(mx, my + 4, 11, 14), LINE, 3)
    elif kind == 'set':
        p.stroke(cr([(mx - 22, my + 4), (mx, my + 2), (mx + 24, my - 4)], closed=False), MOUTH, 4.5)
    elif kind == 'pout':
        p.stroke(cr([(mx - 16, my + 7), (mx, my), (mx + 16, my + 6)], closed=False), MOUTH, 4.5)
    elif kind == 'grimace':
        shape = cr([(mx - 26, my), (mx, my - 6), (mx + 26, my - 2), (mx + 20, my + 12), (mx, my + 10), (mx - 20, my + 12)])
        m = p.poly(shape, WHITE)
        p.stroke([(mx - 22, my + 4), (mx + 22, my + 3)], WHITE_SH, 2, clip=m)
        for x in (-10, 2, 13):
            p.stroke([(mx + x, my - 4), (mx + x, my + 11)], WHITE_SH, 1.8, clip=m)
        p.stroke(shape, LINE, 3.5, closed=True)


FACES = {   # name: (eyes, mouth, brows)
    'cheer': ('open', 'grin', None), 'smile': ('open', 'smile', None), 'blink': ('blink', 'smile', None),
    'joy': ('happy', 'grin', None), 'surprised': ('wide', 'o', 'up'), 'determined': ('lidded', 'set', 'angry'),
    'hurt': ('squeeze', 'grimace', 'worried'), 'pout': ('open', 'pout', 'worried'), 'talk': ('open', 'open', None),
}
HEAD_BOX = (280, 200, 720, 680)


def head(face):
    p = Part(HEAD_BOX)
    # hair behind the face
    back = cr([(492, 218), (596, 232), (664, 286), (700, 370), (702, 455), (678, 538), (612, 566), (480, 572), (350, 556),
               (310, 480), (312, 370), (370, 270), (420, 236)])
    hb = p.poly(back, HAIR)
    p.poly(cr([(640, 330), (690, 420), (680, 520), (640, 560), (620, 470)]), HAIR_SH, clip=hb)
    # the face
    face_pts = cr([(366, 398), (500, 368), (618, 398), (626, 468), (613, 530), (578, 576), (520, 607), (473, 617), (432, 602),
                   (393, 566), (367, 516), (358, 455)])
    fm = p.poly(face_pts, SKIN)
    # ear, with its stud
    ear = cr([(610, 462), (633, 450), (650, 470), (647, 506), (632, 529), (612, 524)])
    p.poly(ear, SKIN); p.stroke(ear, LINE, 3.5, closed=True)
    p.stroke(cr([(624, 470), (638, 478), (634, 500), (624, 510)], closed=False), SKIN_DK, 3)
    p.poly(ell(631, 521, 4.5, 4.5), (230, 230, 240)); p.stroke(ell(631, 521, 4.5, 4.5), LINE, 1.8)
    # cheeks: shade on the far side, blush and freckles
    p.poly(cr([(366, 470), (380, 540), (420, 590), (472, 616), (432, 602), (393, 566), (365, 515)]), SKIN_SH, clip=fm)
    p.soft(ell(398, 552, 28, 14), BLUSH, clip=fm, alpha=0.75)
    p.soft(ell(582, 546, 30, 15), BLUSH, clip=fm, alpha=0.75)
    for x, y in ((386, 548), (398, 556), (410, 548), (403, 541), (392, 561), (571, 541), (584, 549), (596, 541), (590, 534),
                 (578, 556), (600, 553)):
        p.poly(ell(x, y, 2.2, 2.2), SKIN_DK, alpha=0.8)
    # nose
    p.stroke(cr([(470, 535), (465, 548), (474, 553)], closed=False), SKIN_DK, 3)
    p.stroke([(476, 541), (479, 545)], WHITE, 2.4, alpha=0.8)
    # eyes, mouth
    eyes, mouth, brows = FACES[face]
    for e, near in ((EYE_FAR, False), (EYE_NEAR, True)):
        if eyes in ('open', 'wide', 'lidded'):
            _eye_open(p, e, near, lid=0.42 if eyes == 'lidded' else 0.0, wide=eyes == 'wide')
        else:
            _eye_closed(p, e, near, eyes)
    _mouth(p, mouth)
    # the curl at her cheek, the lock before her ear
    curl = ribbon([(360, 405), (366, 470), (373, 540), (364, 598), (340, 626), (316, 616), (318, 592), (334, 590)], 36, 9)
    cm = p.poly(curl, HAIR)
    p.stroke(cr([(368, 430), (372, 520), (360, 590), (336, 612)], closed=False), HAIR_SH, 5, clip=cm)
    p.stroke(curl, LINE, 3.5, closed=True)
    lock = ribbon([(608, 412), (618, 462), (610, 520)], 24, 8)
    p.poly(lock, HAIR); p.stroke(lock, LINE, 3.5, closed=True)
    # bangs, swept from the part at the bow to her right (image-left)
    bangs = cr([(600, 256), (556, 232), (494, 226), (430, 240), (378, 270), (340, 312), (318, 360), (302, 410), (270, 452),
                (270, 452), (318, 436), (336, 462), (336, 462), (362, 428), (396, 420), (430, 430), (456, 448), (456, 448),
                (472, 412), (520, 404), (556, 420), (556, 420), (576, 392), (606, 396), (632, 424), (632, 424), (644, 376),
                (652, 318), (636, 276)])
    bm = p.poly(bangs, HAIR)
    p.paint(p.shift(bm, 0, 14) & fm & ~bm, SKIN_SH)                                       # (their shadow on her brow)
    for path, w in ((((598, 270), (520, 290), (440, 330), (360, 400), (290, 450)), 9), (((520, 300), (440, 360), (400, 420)), 6),
                    (((610, 300), (540, 340), (480, 380), (450, 440)), 7), (((628, 320), (600, 360), (565, 415)), 6),
                    (((560, 262), (470, 290), (400, 340), (360, 440)), 6)):
        p.stroke(cr(path, closed=False), HAIR_SH, w, clip=bm)
    p.stroke(cr([(560, 268), (500, 280), (440, 306), (400, 340)], closed=False), HAIR_HI, 7, clip=bm)
    p.stroke(cr([(600, 300), (585, 330)], closed=False), HAIR_HI, 5, clip=bm)
    p.stroke(bangs, LINE, 3.5, closed=True)
    _brows(p, brows)
    # the bow
    for lp in (cr([(596, 258), (566, 228), (540, 236), (546, 266), (596, 266)]), cr([(600, 258), (634, 226), (660, 240), (650, 270), (602, 268)])):
        m = p.poly(lp, BOW); p.poly(cr([lp[0], lp[len(lp) // 3], lp[len(lp) // 2]]), BOW_HI, clip=m, alpha=0.8)
        p.stroke(lp, LINE, 3.5, closed=True)
    for tail in (((590, 270), (578, 298), (570, 290)), ((606, 270), (622, 296), (630, 286))):
        p.poly(cr(tail), BOW_DK); p.stroke(cr(tail), LINE, 3, closed=True)
    p.poly(ell(598, 261, 12, 11), BOW_DK); p.stroke(ell(598, 261, 12, 11), LINE, 3.5)
    p.outline(5)
    return p


def pony():
    p = Part((560, 200, 930, 700))
    tail = cr([(590, 258), (660, 232), (750, 236), (830, 268), (884, 330), (904, 410), (890, 490), (896, 560), (896, 560),
               (862, 520), (850, 600), (850, 600), (826, 540), (796, 618), (796, 618), (790, 530), (800, 450), (790, 380),
               (740, 330), (670, 312), (604, 296)])
    m = p.poly(tail, HAIR)
    p.poly(cr([(760, 300), (850, 330), (870, 430), (850, 540), (820, 480), (800, 380), (740, 320)]), HAIR_SH, clip=m)
    p.stroke(cr([(620, 262), (720, 254), (810, 290), (860, 360), (870, 440)], closed=False), HAIR_HI, 10, clip=m)
    for path in (((640, 290), (740, 290), (820, 340), (840, 440), (836, 540)), ((700, 300), (790, 360), (812, 470), (812, 580))):
        p.stroke(cr(path, closed=False), HAIR_DK, 4, clip=m)
    p.outline(5)
    return p


# ---------------------------------------------------------------------------------------------------- torso, arms, skirt, legs
def torso():
    p = Part((360, 590, 640, 960))
    neck = p.poly([(452, 590), (506, 590), (510, 660), (450, 660)], SKIN)
    p.poly(cr([(450, 600), (506, 600), (506, 628), (478, 640), (450, 628)]), SKIN_SH, clip=neck)
    body = cr([(445, 654), (515, 654), (562, 668), (600, 690), (612, 724), (600, 784), (586, 842), (574, 902), (580, 950),
               (414, 950), (420, 902), (408, 842), (393, 784), (381, 724), (393, 690), (430, 668)])
    bm = p.poly(body, TOP)
    p.poly(cr([(381, 724), (410, 700), (430, 760), (440, 840), (436, 902), (420, 902), (408, 842), (393, 784)]), TOP_SH, clip=bm)
    p.stroke(cr([(560, 720), (575, 780), (566, 840)], closed=False), TOP_HI, 8, clip=bm, alpha=0.8)
    p.stroke(cr([(430, 812), (470, 826), (530, 826), (566, 810)], closed=False), TOP_SH, 4, clip=bm)
    # lace band
    lace = p.poly([(418, 858), (578, 858), (574, 902), (420, 902)], TOP_SH, clip=bm)
    for i in range(9):
        x = 424 + i * 18.5
        p.stroke(ell(x + 9, 866, 9, 8, 0, 180, 10), TOP_HI, 2.4, clip=lace)
        p.poly(ell(x + 9, 884, 3, 3), TOP_HI, clip=lace, alpha=0.8)
    p.stroke([(418, 858), (578, 858)], LINE, 2.4)
    # belt and buckle
    belt = p.poly(cr([(412, 900), (497, 906), (582, 900), (586, 950), (497, 956), (410, 950)]), BELT)
    for i in range(-12, 14):
        x = 497 + i * 14
        p.stroke([(x - 20, 902), (x + 20, 954)], BELT_DK, 2.2, clip=belt)
        p.stroke([(x + 20, 902), (x - 20, 954)], BELT_HI, 1.6, clip=belt, alpha=0.6)
    p.stroke(cr([(412, 900), (497, 906), (582, 900)], closed=False), LINE, 2.6)
    bk = ell(497, 928, 38, 32)
    p.poly(bk, WHITE); p.poly(ell(503, 936, 32, 24), WHITE_SH, clip=p.mask(bk) & ~p.mask(ell(493, 922, 34, 28)))
    for k in range(5):
        a = math.radians(-90 + 72 * k)
        p.stroke(ell(497 + 11 * math.cos(a), 928 + 11 * math.sin(a), 8, 8), (150, 150, 168), 2.2)
    p.poly(ell(497, 928, 4, 4), (150, 150, 168))
    p.stroke(bk, LINE, 3.5, closed=True)
    # scarf (cowl over the shoulders, its tails over her right breast) and collar
    sc = cr([(386, 694), (440, 668), (482, 682), (526, 668), (604, 690), (610, 716), (560, 708), (484, 726), (424, 716), (390, 722)])
    sm = p.poly(sc, SCARF)
    p.poly(cr([(390, 712), (430, 704), (484, 716), (560, 700), (608, 708), (560, 712), (484, 728), (424, 718)]), SCARF_SH, clip=sm)
    p.stroke(cr([(420, 690), (470, 698), (520, 690)], closed=False), SCARF_HI, 4, clip=sm)
    p.stroke(sc, LINE, 3.2, closed=True)
    for tl in (cr([(424, 708), (406, 744), (402, 780), (402, 780), (420, 768), (430, 784), (430, 784), (440, 744), (446, 714)]),
               cr([(440, 712), (452, 750), (466, 772), (466, 772), (470, 750), (460, 712)])):
        m = p.poly(tl, SCARF); p.stroke(cr([tl[2], tl[len(tl) // 2]], closed=False), SCARF_SH, 4, clip=m)
        p.stroke(tl, LINE, 3.2, closed=True)
    p.poly(ell(440, 712, 14, 11), SCARF_SH); p.stroke(ell(440, 712, 14, 11), LINE, 3)
    col = cr([(452, 640), (510, 640), (520, 666), (482, 680), (442, 666)])
    p.poly(col, WHITE); p.stroke(col, LINE, 3.2, closed=True)
    p.stroke([(481, 652), (481, 678)], WHITE_SH, 2.4)
    p.poly(ell(481, 668, 4.5, 4.5), WHITE); p.stroke(ell(481, 668, 4.5, 4.5), LINE, 2)
    # the flower brooch
    for k in range(5):
        a = -90 + 72 * k
        pet = ell(500 + 17 * math.cos(math.radians(a)), 772 + 17 * math.sin(math.radians(a)), 17, 9.5, rot=a)
        m = p.poly(pet, PINK); p.poly(ell(500 + 12 * math.cos(math.radians(a)), 772 + 12 * math.sin(math.radians(a)), 8, 3, rot=a), PINK_HI, clip=m)
        p.stroke(pet, PINK_DK, 2.6, closed=True)
    gem = [(500, 760), (507, 772), (500, 784), (493, 772)]
    p.poly(gem, GOLD); p.poly([(500, 760), (507, 772), (500, 772)], (255, 236, 150)); p.stroke(gem, LINE, 2, closed=True)
    p.outline(5)
    return p


SH_L, SH_R = (591, 710), (404, 710)                    # (her left shoulder - image-right - and her right)
ELBOW_Y, WRIST_Y = 856, 994


def upper_arm():
    x = SH_L[0]
    p = Part((x - 40, 680, x + 40, 880))
    arm = cr([(x - 26, 704), (x, 688), (x + 26, 702), (x + 27, 770), (x + 24, 846), (x, 870), (x - 23, 846), (x - 26, 770)])
    m = p.poly(arm, TOP)
    p.poly(cr([(x - 26, 704), (x - 12, 720), (x - 8, 800), (x - 10, 860), (x - 23, 846), (x - 26, 770)]), TOP_SH, clip=m)
    p.stroke(cr([(x + 14, 716), (x + 16, 790)], closed=False), TOP_HI, 6, clip=m, alpha=0.8)
    p.stroke(cr([(x - 14, 830), (x + 4, 840), (x + 18, 832)], closed=False), TOP_SH, 3, clip=m)
    p.outline(5)
    return p


def forearm(hand='rest'):
    x = SH_L[0]
    p = Part((x - 70, 830, x + 70, 1140))
    fa = cr([(x - 23, 852), (x, 840), (x + 23, 852), (x + 21, 930), (x + 18, 996), (x - 18, 996), (x - 21, 930)])
    m = p.poly(fa, TOP)
    p.poly(cr([(x - 23, 852), (x - 10, 862), (x - 6, 940), (x - 8, 996), (x - 18, 996), (x - 21, 930)]), TOP_SH, clip=m)
    p.stroke(cr([(x + 12, 870), (x + 12, 950)], closed=False), TOP_HI, 5, clip=m, alpha=0.8)
    if hand == 'rest':
        palm = cr([(x - 18, 1018), (x + 18, 1018), (x + 24, 1050), (x + 18, 1086), (x + 2, 1100), (x - 12, 1094), (x - 20, 1066)])
        pm = p.poly(palm, SKIN)
        p.poly(cr([(x - 20, 1030), (x - 6, 1040), (x - 4, 1090), (x - 12, 1094), (x - 20, 1066)]), SKIN_SH, clip=pm)
        for dx in (-3, 7):
            p.stroke([(x + dx, 1078), (x + dx + 1, 1094)], SKIN_DK, 2.2, clip=pm)
        p.stroke(palm, LINE, 3.4, closed=True)
        th = cr([(x - 17, 1030), (x - 30, 1056), (x - 26, 1072), (x - 14, 1062)])
        p.poly(th, SKIN); p.stroke(th, LINE, 3.2, closed=True)
    else:                                                                  # (open, palm out: her wave)
        palm = cr([(x - 22, 1016), (x + 22, 1016), (x + 26, 1050), (x + 22, 1072), (x - 22, 1072), (x - 26, 1048)])
        p.poly(palm, SKIN)
        for i, (dx, ang, ln) in enumerate(((-18, 12, 44), (-6, 4, 52), (7, -3, 50), (19, -12, 42))):
            a = math.radians(90 + ang)
            x0, y0 = x + dx, 1066
            f = ribbon([(x0, y0), (x0 + ln * math.cos(a), y0 + ln * math.sin(a))], 12, 10, smooth=False)
            p.poly(f, SKIN); p.stroke(f, LINE, 3, closed=True)
            p.poly(ell(x0 + (ln - 4) * math.cos(a), y0 + (ln - 4) * math.sin(a), 3.5, 4.5), (240, 170, 200))
        p.poly(palm, SKIN); p.stroke(cr([(x - 22, 1072), (x - 26, 1048), (x - 22, 1016)], closed=False), LINE, 3.4)
        p.stroke(cr([(x + 22, 1016), (x + 26, 1050), (x + 22, 1072)], closed=False), LINE, 3.4)
        p.stroke(cr([(x - 10, 1036), (x + 2, 1050), (x + 12, 1040)], closed=False), SKIN_SH, 2.4)
        th = ribbon([(x - 22, 1036), (x - 44, 1050), (x - 52, 1068)], 16, 11)
        p.poly(th, SKIN); p.stroke(th, LINE, 3, closed=True)
    cuff = cr([(x - 21, 990), (x + 21, 990), (x + 22, 1022), (x - 22, 1022)])
    cm = p.poly(cuff, WHITE); p.poly([(x - 30, 1012), (x + 30, 1012), (x + 30, 1030), (x - 30, 1030)], WHITE_SH, clip=cm)
    p.stroke(cuff, LINE, 3.2, closed=True)
    p.poly(ell(x + 12, 1006, 4, 4), WHITE); p.stroke(ell(x + 12, 1006, 4, 4), LINE, 1.8)
    p.outline(5)
    return p


WAIST_Y = 936
SKIRTS = ('still', 'swish_l', 'swish_r', 'flare')


def skirt(cut='still'):
    p = Part((110, 900, 890, 1500))
    flare = 1.12 if cut == 'flare' else 1.0
    lift = 34 if cut == 'flare' else 0
    sw = {'swish_l': -52, 'swish_r': 52}.get(cut, 0)
    def at(x, y):                                               # (the cut's sway and flare, growing toward the hem)
        t = max(0.0, (y - WAIST_Y) / 470)
        return (CX + (x - CX) * (1 + (flare - 1) * t) + sw * t ** 1.6, y - lift * t ** 1.3)
    # the hem: big soft waves - bumps fall toward you, hollows lift and show the skirt's inside
    hem = [(200, 1384), (236, 1416), (286, 1404), (322, 1370), (366, 1406), (424, 1432), (474, 1400), (502, 1378), (550, 1420),
           (612, 1438), (662, 1402), (692, 1378), (734, 1412), (776, 1420), (802, 1390)]
    hollows = (322, 502, 692)
    if cut == 'swish_l': hem = [(x, y + 10 * math.sin(x / 40)) for x, y in hem]
    left = [(418, WAIST_Y), (372, 1030), (292, 1180), (218, 1330)]
    right = [(782, 1330), (704, 1180), (624, 1030), (578, WAIST_Y)]
    out = cr([at(*q) for q in left + hem + right], n=8)
    back = cr([at(*q) for q in [(214, 1350), (320, 1394), (500, 1404), (690, 1400), (790, 1352), (700, 1200), (300, 1200)]], n=8)
    p.poly(back, SKIRT_IN)
    m = p.poly(out, SKIRT)
    # folds: broad valleys down to each hollow, soft light ridges between
    for hx in hollows:
        top = at(CX + (hx - CX) * 0.25, WAIST_Y + 10)
        p.poly(cr([top, at(CX + (hx - CX) * 0.7 - 14, 1200), at(hx - 30, 1396), at(hx + 30, 1396), at(CX + (hx - CX) * 0.7 + 14, 1200)]),
               SKIRT_SH, clip=m)
    for bx, w in ((236, 22), (424, 26), (612, 28), (776, 18)):
        p.stroke(cr([at(CX + (bx - CX) * 0.3, WAIST_Y + 20), at(CX + (bx - CX) * 0.75, 1210), at(bx, 1400)], closed=False),
                 SKIRT_LT, w, clip=m, alpha=0.55)
    p.poly(cr([at(418, WAIST_Y), at(372, 1030), at(292, 1180), at(218, 1330), at(200, 1384), at(250, 1400), at(330, 1200),
               at(400, 1040), at(444, WAIST_Y)]), SKIRT_SH, clip=m)
    p.stroke(out, LINE, 3.5, closed=True)
    p.outline(5)
    return p


LEG_X = 540


def leg():
    x = LEG_X
    p = Part((x - 90, 1300, x + 90, 1960))
    th = cr([(x - 40, 1320), (x + 42, 1320), (x + 39, 1420), (x + 31, 1496), (x - 29, 1496), (x - 38, 1420)])
    tm = p.poly(th, SKIN)
    p.poly(cr([(x - 38, 1330), (x - 22, 1340), (x - 16, 1470), (x - 29, 1496), (x - 38, 1420)]), SKIN_SH, clip=tm)
    p.stroke(cr([(x - 9, 1468), (x + 2, 1476), (x + 13, 1471)], closed=False), SKIN_DK, 2.4)
    sock = cr([(x - 33, 1500), (x + 35, 1500), (x + 42, 1590), (x + 34, 1690), (x + 24, 1790), (x - 22, 1790), (x - 30, 1690),
               (x - 40, 1590)])
    sm = p.poly(sock, WHITE)
    p.poly(cr([(x - 40, 1590), (x - 26, 1560), (x - 18, 1660), (x - 12, 1790), (x - 22, 1790), (x - 30, 1690)]), WHITE_SH, clip=sm, alpha=0.7)
    for i in range(6):
        p.stroke(ell(x - 33 + i * 12.5 + 6, 1528, 6, 6, 0, 180, 8), WHITE_SH, 2, clip=sm)
    p.stroke([(x - 36, 1530), (x + 38, 1530)], WHITE_SH, 2)
    p.stroke(sock, LINE, 3.2, closed=True)
    sh = cr([(x - 26, 1786), (x + 28, 1786), (x + 48, 1830), (x + 54, 1892), (x + 44, 1926), (x - 38, 1928), (x - 50, 1892),
             (x - 44, 1830)])
    shm = p.poly(sh, SHOE)
    p.poly([(x - 70, 1900), (x + 70, 1900), (x + 70, 1950), (x - 70, 1950)], SHOE_SH, clip=shm)
    p.poly(ell(x + 14, 1860, 20, 13, rot=-20), SHOE_HI, clip=shm, alpha=0.8)
    p.stroke([(x - 52, 1900), (x + 54, 1900)], LINE, 2.6, clip=shm)
    p.poly([(x - 40, 1812), (x + 42, 1812), (x + 44, 1828), (x - 42, 1828)], WHITE, clip=shm)
    p.stroke([(x - 40, 1812), (x + 42, 1812)], LINE, 2); p.stroke([(x - 42, 1828), (x + 44, 1828)], LINE, 2)
    p.poly(ell(x + 26, 1820, 4.5, 4.5), (200, 200, 216)); p.stroke(ell(x + 26, 1820, 4.5, 4.5), LINE, 1.6)
    p.stroke(sh, LINE, 3.4, closed=True)
    p.outline(5)
    return p


# ---------------------------------------------------------------------------------------------------- the rig
def build():
    P = {'pony': pony(), 'torso': torso(), 'arm': upper_arm(), 'leg': leg()}
    for f in FACES: P[f'head_x{f}'] = head(f)
    for c in SKIRTS: P[f'skirt_x{c}'] = skirt(c)
    for h in ('rest', 'open'): P[f'fore_x{h}'] = forearm(h)
    return P


def flat(P, faces='cheer', cut='still', hand='rest'):
    """the puppet in its rest pose as one picture (to look at the drawing)"""
    im = Image.new('RGBA', (1000, 2000), (0, 0, 0, 0))
    def put(q):
        img = q.image(); im.alpha_composite(img, (int(round(q.box[0])), int(round(q.box[1]))))
    put(P['pony'])
    for q in (P['arm'], P[f'fore_x{hand}']): put(q)
    for q in (P['leg'].mirrored(), P['leg']): put(q)
    put(P[f'skirt_x{cut}']); put(P['torso']); put(P[f'head_x{faces}'])
    for q in (P['arm'].mirrored(SH_L[0] / 2 + SH_R[0] / 2), P[f'fore_x{hand}'].mirrored(SH_L[0] / 2 + SH_R[0] / 2)): put(q)
    return im


def make():
    P = build()
    k = HEIGHT_BLOCKS * 16 / (FEET_Y - TOP_Y)
    D = lambda x, y: ((CX - x) * k, (FEET_Y - y) * k)
    AX = (SH_L[0] + SH_R[0]) / 2                         # (the arms' mirror line)
    LX = CX                                              # (the legs')

    pieces = {}                                          # name -> {variant: Part}, hinge, parent, z (+ is further back)
    def add(n, var, hinge, parent, z):
        pieces[n] = (var, hinge, parent, z)
    add('torso', {'': P['torso']}, (CX, WAIST_Y), None, 0.0)
    add('skirt', {c: P[f'skirt_x{c}'] for c in SKIRTS}, (CX, WAIST_Y), 'torso', 0.9)
    add('head', {f: P[f'head_x{f}'] for f in FACES}, (480, 640), 'torso', -0.3)
    add('pony', {'': P['pony']}, (598, 262), 'head', 0.8)
    add('arml', {'': P['arm']}, SH_L, 'torso', 0.6)
    add('forel', {h: P[f'fore_x{h}'] for h in ('rest', 'open')}, (SH_L[0], ELBOW_Y), 'arml', 0.55)
    add('armr', {'': P['arm'].mirrored(AX)}, SH_R, 'torso', -0.6)
    add('forer', {h: P[f'fore_x{h}'].mirrored(AX) for h in ('rest', 'open')}, (SH_R[0], ELBOW_Y), 'armr', -0.7)
    add('legl', {'': P['leg']}, (LEG_X, 1330), None, 1.4)
    add('legr', {'': P['leg'].mirrored(LX)}, (2 * LX - LEG_X, 1330), None, 1.45)

    def square(q):                                       # (each texture square: the piece padded about its middle)
        x0, y0, x1, y1 = q.box
        s = max(x1 - x0, y1 - y0) + 6
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        box = (mx - s / 2, my - s / 2, mx + s / 2, my + s / 2)
        canvas = Image.new('RGBA', (int(round(s * 2)), int(round(s * 2))), (0, 0, 0, 0))
        img = q.image(); img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
        canvas.alpha_composite(img, (int(round((x0 - box[0]) * 2)), int(round((y0 - box[1]) * 2))))
        return canvas.resize((TEX, TEX), Image.LANCZOS), box

    tex = {}
    for n, (var, *_r) in pieces.items():
        for v, q in var.items():
            tex[f'{PREFIX}{n}' + (f'_x{v}' if v else '')] = square(q)

    PIVOT = {n: (round(D(*h)[0], 3), round(D(*h)[1], 3), 0.0) for n, (_v, h, _p, _z) in pieces.items()}
    PARENT = {n: par for n, (_v, _h, par, _z) in pieces.items()}

    def textures():
        return {t: im for t, (im, _b) in tex.items()}

    def models():
        M = {}
        for n, (var, _h, _p, z) in pieces.items():
            for v in var:
                t = f'{PREFIX}{n}' + (f'_x{v}' if v else '')
                box = tex[t][1]
                ax, ay = D(box[0], box[3]); bx, by = D(box[2], box[1])
                zz = z * 0.08
                e = el((min(ax, bx), ay, zz - 0.02), (max(ax, bx), by, zz + 0.02), t, PIVOT[n], faces=('north', 'south'),
                       uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]})
                M[t] = ({t: f'bm:block/{t}'}, [e])
        return M

    DEF = {'head': ('_face', 'smile'), 'skirt': ('_skirt', 'still'), 'forel': ('_handl', 'rest'), 'forer': ('_handr', 'rest')}

    def model_name(p, pose, suffix=''):
        if p in DEF:
            key, d = DEF[p]
            return f'{PREFIX}{p}_x{pose.get(key, d)}{suffix}'
        return f'{PREFIX}{p}{suffix}'

    return types.SimpleNamespace(KEY='emma', PREFIX=PREFIX, RIG_SCALE=1.0, PIVOT=PIVOT, PARENT=PARENT, PARTS=tuple(pieces), PART_K={},
                                 HIDDEN=lambda p, pose: False, model_name=model_name, textures=textures, models=models,
                                 POSES=POSES, FACES=tuple(FACES), P=P)


Z = lambda d: qs(('z', d))
# (in the picture's plane: + turns counter-clockwise as she faces you; her right arm is image-left)
POSES = {
    'idle': {'_face': 'smile', 'armr': Z(-5), 'forer': Z(-4), 'arml': Z(5), 'forel': Z(4)},
    'idle_b': {'_face': 'blink', 'armr': Z(-7), 'forer': Z(-6), 'arml': Z(7), 'forel': Z(6), 'head': Z(3), 'pony': Z(-5)},
    'walk_a': {'_face': 'smile', '_skirt': 'swish_r', 'legr': Z(-10), 'legl': Z(6), 'armr': Z(14), 'forer': Z(-10), 'arml': Z(14),
               'forel': Z(10), 'torso': Z(-2), 'pony': Z(7), 'head': Z(-2)},
    'walk_b': {'_face': 'smile', '_skirt': 'swish_l', 'legr': Z(-6), 'legl': Z(10), 'armr': Z(-14), 'forer': Z(-10), 'arml': Z(-14),
               'forel': Z(10), 'torso': Z(2), 'pony': Z(-7), 'head': Z(2)},
    'wave': {'_face': 'cheer', '_handl': 'open', 'arml': Z(150), 'forel': Z(-12), 'armr': Z(-6), 'forer': Z(-4), 'head': Z(5),
             'pony': Z(-8)},
    'talk': {'_face': 'talk', 'armr': Z(-24), 'forer': Z(-70), 'arml': Z(6), 'forel': Z(4), 'head': Z(-3)},
    'cast': {'_face': 'determined', '_handr': 'open', '_skirt': 'swish_l', 'armr': Z(-95), 'forer': Z(-8), 'arml': Z(30),
             'forel': Z(40), 'head': Z(-3), 'pony': Z(12)},
    'joy': {'_face': 'joy', '_skirt': 'flare', '_handl': 'open', '_handr': 'open', 'armr': Z(-150), 'forer': Z(-20), 'arml': Z(150),
            'forel': Z(20), 'pony': Z(-12)},
    'hurt': {'_face': 'hurt', 'armr': Z(20), 'forer': Z(70), 'arml': Z(-20), 'forel': Z(-70), 'head': Z(-6), 'torso': Z(-3),
             'pony': Z(10)},
    'surprised': {'_face': 'surprised', '_handl': 'open', '_handr': 'open', 'armr': Z(-30), 'forer': Z(-60), 'arml': Z(30),
                  'forel': Z(60), 'head': Z(-2)},
    'pout': {'_face': 'pout', 'armr': Z(28), 'forer': Z(95), 'arml': Z(-28), 'forel': Z(-95), 'head': Z(4)},
}

EMMA = None


def get():
    global EMMA
    if EMMA is None: EMMA = make()
    return EMMA
