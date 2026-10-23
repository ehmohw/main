"""2.94: THE SKY BUDDIES - Sunny, Snooze, Twinkle and Nimbus, cut from the owner's painting (ref/sky_buddies.png) and kept
as painted: smooth, not pixelated. Each part is a flat 2D sprite on its own item display, billboarded (it always faces you),
floating.

THE PARTS   head (Sunny's disc: the shades, the smirk), rays (his rays, a part of their own so they can spin), moon (Snooze,
            asleep), cap (Snooze's nightcap - a texture of its own, so the wardrobe can recolour it), star (Twinkle, grumpy),
            body (Nimbus, the front cloud: ":3") and back (the darker cloud behind him).
ONE JOINT   every part shares one joint - the middle of Sunny's disc - and the layout is in the models (each sprite's quad sits
            where it belongs round that joint). A part moves on its own with rigkit's '_o_<part>' offsets (a pose's per-part
            shift, carried to its children: the cap rides the moon).
FACES       each face is the owner's own face, untouched; every other expression is the painting with its features painted
            out (the skin under them refilled from the shading round them) and new ones drawn in the same hand: bold black
            strokes, tapered at the ends.
BILLBOARD   a display with billboard "center" turns its whole frame to the camera, so a model's north face (rigkit's front, -z)
            is always toward you and its +x on your left - rigkit's design frame as is. The translation a pose solves is in that
            frame too, so the layout and every offset hold from any side.
Design units: 1 = 1/8 block at RIG_SCALE 2 (built half size, shown at twice the scale: the models keep inside their box)."""
import math
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from rigkit import qs, el, I

PREFIX = 'yb_'
RIG_SCALE = 2.0
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'ref', 'sky_buddies.png')
PPB = 440.0                                     # (art pixels to a block)
DU = 16.0 / RIG_SCALE / PPB                     # (design units per art pixel)
WIN = 512                                       # (a part's window on the painting: 512 square - its texture 512 - or, for the small ones, 128 at twice the size)
WINS = {'star': 128, 'cap': 128, 'body': 640}
CS = {'star': 8, 'cap': 8}                      # (canvas pixels per painting pixel - 4, the small ones 8)
TEXS = {'body': 512, 'head': 512, 'rays': 512, 'moon': 512, 'back': 512, 'star': 256, 'cap': 256}
SUN_C = (271.0, 270.0)                          # (the middle of Sunny's disc in the painting: the joint)
DISC_R = 168.0
FACED = ('head', 'moon', 'star', 'body')
# a part: its anchor in the painting (the middle of its window), where that anchor sits round the joint (on screen, in painting
# pixels: +x your right, +y down), and its depth (+ toward you)
LAYOUT = {'back': ((700, 660), None, -3.0), 'rays': (SUN_C, (0.0, 0.0), -2.0), 'head': (SUN_C, (0.0, 0.0), -1.0),
          'moon': ((857, 400), (+420.0, +10.0), 0.0), 'cap': ((965, 222), None, 0.6), 'star': ((809, 381), None, 1.2),
          'body': ((460, 690), (+190.0, +300.0), 2.0)}
FOLLOW = {'back': 'body', 'cap': 'moon', 'star': 'moon'}          # (placed as the painting has them, round their partner)
PARTS = ('body', 'head', 'rays', 'moon', 'cap', 'star', 'back')
PARENT = {'body': None, 'head': None, 'rays': 'head', 'moon': None, 'cap': 'moon', 'star': None, 'back': 'body'}
JOINT = (0.0, 14.0, 0.0)                        # (design units: the joint, over the host's feet - Sunny about head height)
PIVOT = {p: JOINT for p in PARTS}
PART_K = {}
EXPR = {'head': ('grin', 'surprised', 'hurt', 'sleepy', 'blink', 'fierce'),
        'moon': ('drowsy', 'surprised', 'hurt', 'yawn', 'happy', 'awake'),
        'star': ('smug', 'surprised', 'hurt', 'blink', 'angry', 'happy'),
        'body': ('happy', 'surprised', 'hurt', 'blink', 'angry', 'sing')}
INK = (22, 18, 16, 255)


def HIDDEN(p, pose):
    return pose.get('_hide') is not None and p in pose['_hide']


def model_name(p, pose, suffix=''):
    face = pose.get('_face_' + p) if p in FACED else None
    return f'{PREFIX}{p}{"_x" + face if face else ""}{suffix}'


def place_of(p):
    """a part's anchor round the joint, on screen (painting pixels, +x right, +y down)"""
    a, off, _z = LAYOUT[p]
    if off is not None:
        return off
    q = FOLLOW.get(p, 'moon')
    qa, qo = LAYOUT[q][0], place_of(q)
    return (qo[0] + a[0] - qa[0], qo[1] + a[1] - qa[1])


# ---------------------------------------------------------------------------------------------------- the painting, cut
_CACHE = {}


def _src():
    if 'src' not in _CACHE:
        _CACHE['src'] = np.asarray(Image.open(SRC).convert('RGBA')).astype(np.float32)
    return _CACHE['src']


def _label(mask):
    """connected regions of a boolean mask (4-neighbour): -> (labels, count)"""
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32); n = 0
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n
        while st:
            y, x = st.pop()
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n; st.append((ny, nx))
    return lab, n


def _fill(mask, seed):
    """flood from seed over True cells -> the reached mask"""
    H, W = mask.shape
    out = np.zeros_like(mask); st = [seed]; out[seed] = True
    while st:
        y, x = st.pop()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not out[ny, nx]:
                out[ny, nx] = True; st.append((ny, nx))
    return out


def _holes(mask):
    """a mask with its enclosed holes filled"""
    H, W = mask.shape
    pad = np.ones((H + 2, W + 2), bool); pad[1:-1, 1:-1] = ~mask
    outside = _fill(pad, (0, 0))[1:-1, 1:-1]
    return ~outside


def _dilate(mask, r):
    im = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * r + 1))
    return np.asarray(im) > 127


def _erode(mask, r):
    return ~_dilate(~mask, r)


def _masks():
    """every part's mask in the painting"""
    if 'masks' in _CACHE:
        return _CACHE['masks']
    S = _src(); a = S[..., 3] > 20
    lab, n = _label(a)
    at = lambda x, y: lab[y, x]
    M = {}
    sun = at(int(SUN_C[0]), int(SUN_C[1])); M['head'] = lab == sun
    cy, cx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    rays = np.zeros_like(a)
    for k in range(1, n + 1):
        if k == sun:
            continue
        ys, xs = np.nonzero(lab == k)
        if len(ys) > 400 and math.hypot(xs.mean() - SUN_C[0], ys.mean() - SUN_C[1]) < 290:
            rays |= lab == k
    M['rays'] = rays
    moon = lab == at(985, 420)
    M['cap'] = moon & (cy < 263)
    M['moon'] = moon & (cy >= 263)
    M['star'] = lab == at(809, 390)
    cloud = lab == at(460, 700)
    cloud[727:760, 730:815] &= S[727:760, 730:815, :3].mean(axis=2) > 90          # (the owner's signature, "MOW", left on the page)
    lum = S[..., :3].mean(axis=2)
    light = cloud & (lum > 90)
    inner = _fill(light, (700, 460))                                # (the front cloud's own grey, inside its outline)
    front = _holes(_dilate(inner, 7) & cloud) & cloud
    M['body'] = front
    M['back'] = cloud & ~_erode(front, 1)
    _CACHE['masks'] = M
    return M


def _window(p, img=None):
    """a part's square of the painting (its own pixels only) -> float RGBA array, and the window's corner"""
    (ax, ay), _o, _z = LAYOUT[p]
    N = WINS.get(p, WIN)
    x0, y0 = int(round(ax - N / 2)), int(round(ay - N / 2))
    S = _src() if img is None else img
    m = _masks()[p]
    out = np.zeros((N, N, 4), np.float32)
    H, W = m.shape
    sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(W, x0 + N), min(H, y0 + N)
    sub = S[sy0:sy1, sx0:sx1].copy(); sub[~m[sy0:sy1, sx0:sx1]] = 0
    out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = sub
    return out, (x0, y0)


# ---------------------------------------------------------------------------------------------------- redrawn clean
# The painting is the reference, not the texture: each part is traced into its colour regions (the black ink, the whites, the
# skin - and the moon's crater, the cap's trim), every region's edge smoothed at four times the texture's size, then repainted
# flat: an even outline, a clean gradient for the skin fitted to the painting's own light, flat whites, and the face's ink
# drawn back as clean shapes. The other expressions are drawn on the same clean skin.
SSC = 4                                          # (the canvas: four times the texture)


def C_of(p):
    """canvas pixels per painting pixel"""
    return CS.get(p, SSC)


def _blur(m, s):
    im = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), 'L')
    return np.asarray(im.filter(ImageFilter.GaussianBlur(s)) if s else im).astype(np.float32) / 255


def _up(m, C, s=1.0, level=0.5):
    """a painting-size mask (bool or 0..1) -> the canvas, smoothed: blurred s painting pixels, enlarged, cut at level"""
    im = Image.fromarray((_blur(m, s) * 255).astype(np.uint8), 'L')
    im = im.resize((im.width * C, im.height * C), Image.BICUBIC)
    return np.asarray(im) > level * 255


def _fit(W0, m):
    """the painting's light over a region: a quadratic per channel -> coefficients"""
    ys, xs = np.nonzero(m)
    if len(xs) > 40000:
        k = np.random.RandomState(7).choice(len(xs), 40000, replace=False); ys, xs = ys[k], xs[k]
    A = np.stack([np.ones_like(xs), xs, ys, xs * xs, xs * ys, ys * ys], 1).astype(np.float64)
    return [np.linalg.lstsq(A, W0[ys, xs, c].astype(np.float64), rcond=None)[0] for c in range(3)]


def _field(coef, n, C):
    """a fitted gradient over the whole canvas (n x n)"""
    g = (np.arange(n, dtype=np.float64) + 0.5) / C
    X, Y = np.meshgrid(g, g)
    return np.stack([np.clip(c[0] + c[1] * X + c[2] * Y + c[3] * X * X + c[4] * X * Y + c[5] * Y * Y, 0, 255) for c in coef], -1).astype(np.float32)


class Canvas:
    def __init__(self, p):
        self.p, self.C = p, C_of(p)
        self.n = WINS.get(p, WIN) * self.C
        self.rgba = np.zeros((self.n, self.n, 4), np.float32)

    def paint(self, mask, col):
        c = col if isinstance(col, np.ndarray) else np.array(col[:3], np.float32)
        self.rgba[mask, :3] = c[mask] if c.ndim == 3 else c
        self.rgba[mask, 3] = 255

    def over(self, layer):
        self.rgba = _over(self.rgba, layer)

    def copy(self):
        c = Canvas.__new__(Canvas); c.p, c.C, c.n, c.rgba = self.p, self.C, self.n, self.rgba.copy()
        return c

    def tex(self):
        im = Image.fromarray(np.clip(self.rgba, 0, 255).astype(np.uint8), 'RGBA').resize((TEXS[self.p],) * 2, Image.LANCZOS)
        a = np.asarray(im).copy()
        a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)                 # (a cutout edge: no sorting trouble between the parts)
        return Image.fromarray(a, 'RGBA')


def _classes(W0, sil, white_lum=None, crater=False, trim=None, ink_lum=95):
    rgb = W0[..., :3]; lum = rgb.mean(axis=2)
    mx, mn = rgb.max(axis=2), rgb.min(axis=2); sat = (mx - mn) / np.maximum(mx, 1)
    ink = sil & (lum < ink_lum)
    white = sil & ~ink & (sat < 0.13) & (lum > white_lum) if white_lum else np.zeros_like(sil)
    crat = sil & ~ink & (lum < 175) & (rgb[..., 1] - rgb[..., 2] > 20) & (rgb[..., 0] < 200) if crater else np.zeros_like(sil)
    if trim is not None:
        white &= trim
    return ink, white, crat


def _clean(p, skip=(), white_lum=None, crater=False, line=3.6, sil=None, W0=None, trim=None, dark=1.0, ink_lum=95, edge=1.0, ring=False):
    """a part redrawn clean -> (canvas, its painting-size silhouette, window corner); skip: boxes (window coords) whose
    interior ink and whites are left off (for the faces drawn fresh)"""
    if W0 is None:
        W0, (x0, y0) = _window(p)
    else:
        (x0, y0) = _window(p)[1]
    if sil is None:
        sil = _holes(W0[..., 3] > 128)
    C = C_of(p); cv = Canvas(p)
    ink, white, crat = _classes(W0, sil, white_lum, crater, trim, ink_lum)
    iink = ink & _erode(sil, int(line * 2 + 3))                          # (the face's ink: well inside the outline)
    keep = np.ones_like(sil)
    for b in skip:
        bx0, by0, bx1, by1 = (int(v) for v in b)
        keep[by0:by1, bx0:bx1] = False
    fill = sil & ~_dilate(ink | white | crat, 2) & _erode(sil, 3)
    if fill.sum() < 50:
        fill = sil & ~ink
    field = _field(_fit(W0, fill), cv.n, C) * dark
    rim = _blur(sil.astype(np.float32), 12)                             # (a soft shade in from the edge: it rounds the shape)
    rim = np.asarray(Image.fromarray((rim * 255).astype(np.uint8), 'L').resize((cv.n, cv.n), Image.BICUBIC)).astype(np.float32) / 255
    field *= (0.86 + 0.14 * np.clip((rim - 0.5) / 0.5, 0, 1))[..., None]
    cv.paint(_up(sil, C, edge), INK)
    inner = _up(sil, C, line * edge, 0.84)
    cv.paint(inner, field)
    for m, dk in ((white & keep, 1.0), (crat & keep, 1.0)):
        if m.sum() > 8:
            if ring:                                                        # (a white shape outlined in its own ink: the cap's fur)
                cv.paint(_up(_dilate(m, 2), C, 1.2) & inner, INK)
                m = _holes(m)
            cv.paint(_up(m, C, 0.9) & inner, _field(_fit(W0, m & _erode(m, 1) if (m & _erode(m, 1)).sum() > 20 else m), cv.n, C) * dk)
    if crater and (crat & keep).sum():
        cl = iink & keep & _dilate(crat, 4)
        cv.paint(_up(cl, C, 0.8) & inner, (92, 88, 34))
        iink = iink & ~cl
    if not ring:
        cv.paint(_up(iink & keep, C, 0.8) & inner, INK)
    return cv, sil, (x0, y0)


class Pen:
    """strokes on a part's canvas, in the window's painting coordinates"""
    def __init__(self, p):
        self.C = C_of(p); n = WINS.get(p, WIN) * self.C
        self.im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.im)

    def stroke(self, pts, w=5.0, col=INK, taper=0.35, n=60):
        """a tapered stroke through pts (a Catmull-Rom curve): full width in the middle, thinner at the ends"""
        P = _spline(pts, n * 2); C = self.C
        for i, (x, y) in enumerate(P):
            t = i / max(1, len(P) - 1)
            k = 1.0 - taper * (abs(2 * t - 1) ** 2.2)
            r = w * k * C / 2
            self.d.ellipse((x * C - r, y * C - r, x * C + r, y * C + r), fill=col)

    def blob(self, box, col=INK):
        self.d.ellipse(tuple(v * self.C for v in box), fill=col)

    def poly(self, pts, col):
        self.d.polygon([(x * self.C, y * self.C) for x, y in pts], fill=col)

    def layer(self):
        return np.asarray(self.im).astype(np.float32)


def _spline(pts, n=60):
    if len(pts) == 2:
        (x0, y0), (x1, y1) = pts
        return [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        m = max(4, n // (len(pts) - 1))
        for j in range(m + (1 if i == len(P) - 3 else 0)):
            t = j / m; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 +
                                    (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    return out


def _over(base, top):
    """top over base (float RGBA arrays)"""
    a = top[..., 3:4] / 255.0
    out = base.copy()
    out[..., :3] = top[..., :3] * a + base[..., :3] * (1 - a)
    out[..., 3:4] = np.maximum(base[..., 3:4], top[..., 3:4])
    return out


def _clip(top, mask):
    out = top.copy(); out[..., 3] *= mask
    return out


def _shift_layer(L, dx, dy, ang=0.0, c=None):
    """move (and turn, about c) a layer (canvas pixels)"""
    im = Image.fromarray(np.clip(L, 0, 255).astype(np.uint8), 'RGBA')
    if ang:
        im = im.rotate(ang, resample=Image.BICUBIC, center=c)
    im = im.transform(im.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), resample=Image.BICUBIC)
    return np.asarray(im).astype(np.float32)


# ---------------------------------------------------------------------------------------------------- the faces
def _sun_faces():
    W0, (x0, y0) = _window('head')
    C = C_of('head')
    sx, sy = SUN_C[0] - x0, SUN_C[1] - y0
    w = lambda x, y: (x - x0, y - y0)                                   # (painting -> window)
    gy, gx = np.mgrid[0:WIN, 0:WIN]
    rr = np.hypot(gx - sx, gy - sy)
    full = _holes(W0[..., 3] > 128)
    disc = full & (rr < DISC_R + 4)                                     # (the disc alone: the shades' arm off it is the shades')
    GB = (*w(88, 214), *w(442, 310))
    feats = [(*w(180, 160), *w(276, 226)), (*w(320, 163), *w(410, 226)), GB, (*w(156, 298), *w(314, 402))]
    plain, _s, _o = _clean('head', skip=feats, white_lum=200, sil=disc, W0=W0, line=4.2, ink_lum=125)
    asis, _s, _o = _clean('head', skip=[GB], white_lum=200, sil=disc, W0=W0, line=4.2, ink_lum=125)
    # the shades, redrawn: the lenses' ink (with the bridge, the frame and the arm past the disc) and their glints
    gl = np.zeros((WIN, WIN), bool); gl[int(GB[1]):int(GB[3]), int(GB[0]):int(GB[2])] = True
    ink, white, _c = _classes(W0, full, 200)
    ink &= gl; white &= gl
    ring = (rr > DISC_R - 7) & (rr < DISC_R + 3) & ~((gx < sx) & (np.abs(gy - sy + 10) < 30))     # (not the disc's own rim, bar the arm's crossing)
    ink &= ~ring
    shades = Canvas('head')
    shades.paint(_up(ink, C, 0.7), (16, 14, 16))
    shades.paint(_up(white, C, 0.8) & _up(ink | white, C, 0.7), (244, 244, 240))
    shades = shades.rgba
    discC = _up(disc, C, 1.0)
    L1, L2 = w(234, 262), w(372, 258)

    def face(kind):
        if kind is None:
            cv = asis.copy(); cv.over(shades); return cv
        pen = Pen('head')
        cv = plain.copy(); ang, dx, dy = 0.0, 0.0, 0.0
        b1, b2 = w(232, 190), w(366, 192)
        if kind == 'grin':
            pen.stroke([(b1[0] - 34, b1[1] + 6), (b1[0], b1[1] - 16), (b1[0] + 34, b1[1] + 4)], 9)
            pen.stroke([(b2[0] - 34, b2[1] + 4), (b2[0], b2[1] - 18), (b2[0] + 34, b2[1] + 6)], 9)
            m0 = w(196, 322); m1 = w(318, 318)
            pen.poly(_spline([m0, w(220, 360), w(258, 380), w(296, 358), m1], 40) + [w(258, 326)], (255, 255, 255, 255))
            pen.poly(_spline([w(212, 352), w(258, 378), w(300, 350)], 30) + [w(258, 362)], (196, 64, 60, 255))
            pen.stroke([m0, w(256, 328), m1], 6)
            pen.stroke([m0, w(220, 360), w(258, 380), w(296, 358), m1], 7)
            pen.stroke([w(208, 340), w(258, 348), w(306, 336)], 4)
        elif kind == 'fierce':
            pen.stroke([(b1[0] - 36, b1[1] - 14), (b1[0], b1[1] - 2), (b1[0] + 32, b1[1] + 14)], 11, taper=0.5)
            pen.stroke([(b2[0] - 32, b2[1] + 14), (b2[0], b2[1] - 2), (b2[0] + 36, b2[1] - 14)], 11, taper=0.5)
            m0, m1 = w(190, 334), w(322, 328)
            pen.poly(_spline([m0, w(256, 346), m1], 30) + _spline([m1, w(256, 384), m0], 30), (255, 255, 255, 255))
            pen.stroke([m0, w(256, 346), m1], 7); pen.stroke([m1, w(256, 384), m0], 7)
            pen.stroke([w(194, 352), w(256, 362), w(318, 348)], 4)
            for x in (220, 246, 272, 296):
                pen.stroke([w(x, 340), w(x, 378)], 3.4, taper=0.1)
        elif kind == 'surprised':
            dy = 34
            for c in (L1, L2):
                pen.blob((c[0] - 26, c[1] - 52, c[0] + 26, c[1] + 6), INK)
                pen.blob((c[0] - 21, c[1] - 47, c[0] + 21, c[1] + 1), (255, 255, 255, 255))
                pen.blob((c[0] - 9, c[1] - 30, c[0] + 9, c[1] - 6), INK)
            pen.stroke([(b1[0] - 30, b1[1] - 14), (b1[0], b1[1] - 30), (b1[0] + 30, b1[1] - 16)], 8)
            pen.stroke([(b2[0] - 30, b2[1] - 16), (b2[0], b2[1] - 32), (b2[0] + 30, b2[1] - 14)], 8)
            mc = w(258, 362)
            pen.blob((mc[0] - 17, mc[1] - 13, mc[0] + 17, mc[1] + 23), INK)
            pen.blob((mc[0] - 11, mc[1] - 7, mc[0] + 11, mc[1] + 17), (150, 40, 40, 255))
        elif kind == 'hurt':
            ang, dy, dx = -9.0, 8, -4
            pen.stroke([(b1[0] - 34, b1[1] + 8), (b1[0], b1[1] - 4), (b1[0] + 30, b1[1] - 22)], 9)
            pen.stroke([(b2[0] - 30, b2[1] - 22), (b2[0], b2[1] - 4), (b2[0] + 34, b2[1] + 8)], 9)
            m0, m1 = w(200, 350), w(316, 350)
            pen.poly(_spline([m0, w(230, 334), w(258, 350), w(288, 334), m1], 40) + _spline([m1, w(288, 372), w(258, 360), w(230, 372), m0], 40), (255, 255, 255, 255))
            pen.stroke([m0, w(230, 334), w(258, 350), w(288, 334), m1], 6)
            pen.stroke([m1, w(288, 372), w(258, 360), w(230, 372), m0], 6)
            pen.stroke([w(204, 352), w(258, 354), w(312, 352)], 3.5)
            pen.stroke([w(424, 214), w(430, 232), w(424, 248), w(418, 232), w(424, 214)], 3, col=(120, 200, 255, 255))
        elif kind == 'sleepy':
            dy = 30
            for c in (L1, L2):
                pen.stroke([(c[0] - 22, c[1] - 26), (c[0], c[1] - 16), (c[0] + 22, c[1] - 26)], 6)
            pen.stroke([(b1[0] - 30, b1[1] + 4), (b1[0], b1[1] - 6), (b1[0] + 30, b1[1] + 4)], 7)
            pen.stroke([(b2[0] - 30, b2[1] + 4), (b2[0], b2[1] - 6), (b2[0] + 30, b2[1] + 4)], 7)
            pen.stroke([w(222, 356), w(258, 366), w(292, 352)], 6)
        elif kind == 'blink':                                           # (behind the shades: the glints go out a moment)
            cv = asis.copy(); cv.over(shades)
            for c, (rx, ry) in ((L1, (40, 34)), (L2, (40, 32))):
                pen.blob((c[0] - rx * 0.62, c[1] - ry * 0.7, c[0] + rx * 0.62, c[1] + ry * 0.75), (16, 14, 16, 255))
            pen.stroke([w(214, 246), w(226, 242)], 4, col=(244, 244, 240, 255))
            pen.stroke([w(352, 242), w(364, 238)], 4, col=(244, 244, 240, 255))
            cv.over(pen.layer())
            return cv
        cv.over(pen.layer())
        sh = _shift_layer(shades, dx * C, dy * C, ang, (sx * C, sy * C))
        side = (np.arange(cv.n)[None, :] < (sx - DISC_R + 20) * C) & (np.arange(cv.n)[:, None] < (sy + 60) * C)
        cv.over(_clip(sh, (discC | side).astype(np.float32)))
        return cv
    return face


def _moon_faces():
    W0, (x0, y0) = _window('moon')
    w = lambda x, y: (x - x0, y - y0)
    EB = (*w(940, 334), *w(992, 368))
    plain, _s, _o = _clean('moon', skip=[EB], crater=True, line=4.0)
    asis, _s, _o = _clean('moon', crater=True, line=4.0)
    E = w(964, 349)

    def face(kind):
        if kind is None:
            return asis.copy()
        cv = plain.copy(); pen = Pen('moon'); ex, ey = E
        if kind in ('drowsy', 'awake', 'surprised'):
            op = {'drowsy': 7, 'awake': 12, 'surprised': 17}[kind]
            pen.blob((ex - 16, ey - op, ex + 16, ey + op * 0.9), INK)
            pen.blob((ex - 12.5, ey - op + 3.5, ex + 12.5, ey + op * 0.9 - 3.5), (255, 255, 255, 255))
            pr = 6.5 if kind != 'surprised' else 5.0
            pen.blob((ex - pr + 1, ey - pr * 0.9 + (2 if kind == 'drowsy' else 0), ex + pr + 1, ey + pr * 1.1), INK)
            if kind == 'drowsy':
                pen.poly([(ex - 17, ey - 9), (ex + 17, ey - 9), (ex + 17, ey - 1), (ex - 17, ey - 1)], (240, 232, 178, 255))
                pen.stroke([(ex - 17, ey - 1), (ex, ey - 3), (ex + 17, ey - 1)], 4.5)
            if kind == 'surprised':
                pen.stroke([(ex - 14, ey - 30), (ex + 2, ey - 36), (ex + 16, ey - 31)], 4.5)
                pen.blob((ex + 3, ey + 24, ex + 15, ey + 40), INK)
            if kind == 'awake':
                pen.stroke([(ex - 14, ey - 22), (ex, ey - 24), (ex + 15, ey - 20)], 4.5)
        elif kind == 'hurt':
            pen.stroke([(ex - 16, ey - 9), (ex + 12, ey), (ex - 16, ey + 9)], 5.5, taper=0.2)
            pen.stroke([(ex - 2, ey + 26), (ex + 6, ey + 22), (ex + 15, ey + 27)], 4.5)
        elif kind == 'yawn':
            pen.stroke([(ex - 16, ey - 2), (ex, ey + 5), (ex + 16, ey - 2)], 5)
            pen.blob((ex - 3, ey + 18, ex + 15, ey + 40), INK)
            pen.blob((ex, ey + 22, ex + 12, ey + 37), (170, 60, 70, 255))
        elif kind == 'happy':
            pen.stroke([(ex - 16, ey + 4), (ex, ey - 5), (ex + 16, ey + 4)], 5)
            pen.stroke([(ex - 2, ey + 22), (ex + 7, ey + 28), (ex + 16, ey + 22)], 4.5)
        cv.over(pen.layer())
        return cv
    return face


def _star_faces():
    W0, (x0, y0) = _window('star')
    w = lambda x, y: (x - x0, y - y0)
    FB = (*w(784, 369), *w(840, 404))
    plain, _s, _o = _clean('star', skip=[FB], line=1.5, edge=2.4, ink_lum=120)
    asis, _s, _o = _clean('star', line=1.5, edge=2.4, ink_lum=120)
    L, R, M = w(799, 382), w(825, 382), w(811, 398)

    def face(kind):
        if kind is None:
            return asis.copy()
        cv = plain.copy(); pen = Pen('star')
        if kind == 'angry':
            pen.stroke([(L[0] - 9, L[1] - 9), (L[0] + 8, L[1] - 3)], 3.4, taper=0.2); pen.stroke([(R[0] - 8, R[1] - 3), (R[0] + 9, R[1] - 9)], 3.4, taper=0.2)
            for c in (L, R):
                pen.blob((c[0] - 2.4, c[1] - 1, c[0] + 2.4, c[1] + 4.5))
            pen.stroke([(M[0] - 8, M[1] + 3), (M[0], M[1] - 2), (M[0] + 8, M[1] + 3)], 3)
        elif kind == 'surprised':
            for c in (L, R):
                pen.blob((c[0] - 4, c[1] - 4, c[0] + 4, c[1] + 5))
                pen.blob((c[0] - 1.2, c[1] - 2, c[0] + 1.4, c[1] + 0.4), (255, 255, 255, 255))
            pen.blob((M[0] - 3.5, M[1] - 3, M[0] + 3.5, M[1] + 5))
        elif kind == 'hurt':
            pen.stroke([(L[0] - 5, L[1] - 4), (L[0] + 4, L[1]), (L[0] - 5, L[1] + 4)], 2.8, taper=0.1)
            pen.stroke([(R[0] + 5, R[1] - 4), (R[0] - 4, R[1]), (R[0] + 5, R[1] + 4)], 2.8, taper=0.1)
            pen.stroke([(M[0] - 8, M[1] + 1), (M[0] - 4, M[1] - 2), (M[0], M[1] + 1), (M[0] + 4, M[1] - 2), (M[0] + 8, M[1] + 1)], 2.6, taper=0.1)
        elif kind == 'blink':
            pen.stroke([(L[0] - 8, L[1] - 4), (L[0] + 8, L[1] - 4)], 3, taper=0.2); pen.stroke([(R[0] - 8, R[1] - 4), (R[0] + 8, R[1] - 4)], 3, taper=0.2)
            pen.stroke([(L[0] - 5, L[1] + 1), (L[0] + 5, L[1] + 1)], 2.6); pen.stroke([(R[0] - 5, R[1] + 1), (R[0] + 5, R[1] + 1)], 2.6)
            pen.stroke([(M[0] - 7, M[1]), (M[0] + 7, M[1])], 2.8)
        elif kind == 'smug':
            pen.stroke([(L[0] - 8, L[1] - 4), (L[0] + 8, L[1] - 4)], 3, taper=0.2); pen.stroke([(R[0] - 8, R[1] - 6), (R[0], R[1] - 10), (R[0] + 8, R[1] - 7)], 3, taper=0.2)
            for c in (L, R):
                pen.blob((c[0] - 2.4, c[1] - 2, c[0] + 2.4, c[1] + 4))
            pen.stroke([(M[0] - 7, M[1]), (M[0] + 3, M[1] - 0.5), (M[0] + 8, M[1] - 4)], 2.8)
        elif kind == 'happy':
            pen.stroke([(L[0] - 5, L[1] + 1), (L[0], L[1] - 4), (L[0] + 5, L[1] + 1)], 2.8); pen.stroke([(R[0] - 5, R[1] + 1), (R[0], R[1] - 4), (R[0] + 5, R[1] + 1)], 2.8)
            pen.stroke([(M[0] - 7, M[1] - 2), (M[0], M[1] + 3), (M[0] + 7, M[1] - 2)], 2.8)
        cv.over(pen.layer())
        return cv
    return face


def _cloud_faces():
    W0, (x0, y0) = _window('body')
    w = lambda x, y: (x - x0, y - y0)
    FB = (*w(388, 668), *w(496, 752))
    plain, _s, _o = _clean('body', skip=[FB], line=3.8)
    asis, _s, _o = _clean('body', line=3.8)
    L, R, M = w(404, 688), w(479, 688), w(441, 724)

    def face(kind):
        if kind is None:
            return asis.copy()
        cv = plain.copy(); pen = Pen('body')
        cat = lambda: (pen.stroke([(M[0] - 22, M[1] - 8), (M[0] - 18, M[1] + 2), (M[0] - 8, M[1] + 8), (M[0], M[1] - 1)], 4),
                       pen.stroke([(M[0], M[1] - 1), (M[0] + 8, M[1] + 8), (M[0] + 18, M[1] + 2), (M[0] + 22, M[1] - 8)], 4))
        if kind == 'happy':
            for c in (L, R):
                pen.stroke([(c[0] - 10, c[1] + 4), (c[0], c[1] - 8), (c[0] + 10, c[1] + 4)], 5)
            cat()
        elif kind == 'sing':
            for c in (L, R):
                pen.stroke([(c[0] - 10, c[1] + 4), (c[0], c[1] - 8), (c[0] + 10, c[1] + 4)], 5)
            pen.blob((M[0] - 9, M[1] - 6, M[0] + 9, M[1] + 14)); pen.blob((M[0] - 5, M[1] - 1, M[0] + 5, M[1] + 10), (170, 70, 80, 255))
        elif kind == 'surprised':
            for c in (L, R):
                pen.blob((c[0] - 9, c[1] - 13, c[0] + 9, c[1] + 13))
                pen.blob((c[0] - 4, c[1] - 9, c[0] + 1, c[1] - 3), (255, 255, 255, 255))
            pen.blob((M[0] - 8, M[1] - 4, M[0] + 8, M[1] + 14)); pen.blob((M[0] - 4.5, M[1], M[0] + 4.5, M[1] + 10), (120, 120, 124, 255))
        elif kind == 'hurt':
            pen.stroke([(L[0] - 10, L[1] - 8), (L[0] + 8, L[1]), (L[0] - 10, L[1] + 8)], 4.5, taper=0.15)
            pen.stroke([(R[0] + 10, R[1] - 8), (R[0] - 8, R[1]), (R[0] + 10, R[1] + 8)], 4.5, taper=0.15)
            pen.stroke([(M[0] - 18, M[1] + 4), (M[0] - 9, M[1] - 2), (M[0], M[1] + 4), (M[0] + 9, M[1] - 2), (M[0] + 18, M[1] + 4)], 4, taper=0.1)
        elif kind == 'blink':
            for c in (L, R):
                pen.stroke([(c[0] - 10, c[1] + 2), (c[0], c[1] + 5), (c[0] + 10, c[1] + 2)], 5)
            cat()
        elif kind == 'angry':
            for c, s in ((L, 1), (R, -1)):
                pen.blob((c[0] - 7, c[1] - 9, c[0] + 7, c[1] + 11))
                pen.stroke([(c[0] - 14 * s, c[1] - 24), (c[0] + 10 * s, c[1] - 14)], 5, taper=0.25)
            pen.stroke([(M[0] - 16, M[1] + 8), (M[0], M[1] - 2), (M[0] + 16, M[1] + 8)], 4.5)
        cv.over(pen.layer())
        return cv
    return face


def _hull(pts):
    """the convex hull of (x, y) points (monotone chain)"""
    pts = sorted(set(pts))
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0: hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def _back_tex():
    """the cloud behind, redrawn clean and a little darker: its own outline, and what the front one hid filled in within
    its outline's hull (so a puff of Nimbus's never shows a hole behind him)"""
    W0, (x0, y0) = _window('back')
    m = W0[..., 3] > 20
    ys, xs = np.nonzero(m)
    hull = Image.new('L', (WIN, WIN), 0)
    ImageDraw.Draw(hull).polygon(_hull(list(zip(xs.tolist(), ys.tolist()))), fill=255)
    hull = np.asarray(hull) > 127
    fa = _masks()['body']
    fm = np.zeros(m.shape, bool)
    H, W = fa.shape
    sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(W, x0 + WIN), min(H, y0 + WIN)
    fm[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = fa[sy0:sy1, sx0:sx1]
    sil = _holes(m | (hull & _erode(fm, 3)))
    W1 = W0.copy()
    W1[sil & ~m] = np.array([176, 176, 180, 255], np.float32)
    cv, _s, _o = _clean('back', sil=sil, W0=W1, line=3.6, dark=0.82)
    return cv


def _cap_tex():
    """the nightcap: its cloth redrawn clean (the wardrobe recolours it), and its fur trim and bobble drawn fresh where the
    painting has them - a band of soft white scallops, and a round bobble, each in its own outline"""
    W0, (x0, y0) = _window('cap')
    sil = _holes(W0[..., 3] > 128)
    cv, _s, _o = _clean('cap', skip=[(0, 0, 128, 128)], white_lum=165, line=2.0, edge=1.4, sil=sil, W0=W0)
    rgb = W0[..., :3]; lum = rgb.mean(axis=2); sat = (rgb.max(axis=2) - rgb.min(axis=2)) / np.maximum(rgb.max(axis=2), 1)
    wh = _dilate(sil & (lum > 165) & (sat < 0.13), 2) & sil
    lab, n = _label(wh)
    boxes = sorted((tuple(int(v) for v in (xs.min(), ys.min(), xs.max(), ys.max())) for k in range(1, n + 1)
                    for ys, xs in [np.nonzero(lab == k)] if len(xs) > 12), key=lambda b: -(b[2] - b[0]) * (b[3] - b[1]))
    trim = max(boxes[:2], key=lambda b: b[3]); bob = min(boxes[:2], key=lambda b: b[3])
    pen = Pen('cap')
    fur, shade = (246, 246, 242, 255), (214, 216, 222, 255)
    tx0, ty0, tx1, ty1 = trim
    k = 5; puffs = [(tx0 + (tx1 - tx0) * (i + 0.5) / k, (ty0 + ty1) / 2 + (1.2 if i % 2 else -1.2)) for i in range(k)]
    rx, ry = (tx1 - tx0) / k * 0.72, (ty1 - ty0) / 2 + 0.6
    for x, y in puffs:
        pen.blob((x - rx - 1.3, y - ry - 1.3, x + rx + 1.3, y + ry + 1.3), INK)
    for x, y in puffs:
        pen.blob((x - rx, y - ry, x + rx, y + ry), fur)
    for x, y in puffs:
        pen.blob((x - rx * 0.7, y + ry * 0.1, x + rx * 0.8, y + ry * 0.85), shade)
    for x, y in puffs:
        pen.blob((x - rx * 0.85, y - ry * 0.85, x + rx * 0.6, y + ry * 0.3), fur)
    bx0, by0, bx1, by1 = bob
    cx, cy, r = (bx0 + bx1) / 2, (by0 + by1) / 2, max(bx1 - bx0, by1 - by0) / 2 + 0.5
    pen.blob((cx - r - 1.3, cy - r - 1.3, cx + r + 1.3, cy + r + 1.3), INK)
    pen.blob((cx - r, cy - r, cx + r, cy + r), shade)
    pen.blob((cx - r, cy - r, cx + r * 0.5, cy + r * 0.5), fur)
    cv.over(pen.layer())
    return cv


def textures():
    if 'tex' in _CACHE:
        return _CACHE['tex']
    T = {}
    faces = {'head': _sun_faces(), 'moon': _moon_faces(), 'star': _star_faces(), 'body': _cloud_faces()}
    for p, f in faces.items():
        T[f'{PREFIX}{p}'] = f(None).tex()
        for e in EXPR[p]:
            T[f'{PREFIX}{p}_{e}'] = f(e).tex()
    T[f'{PREFIX}rays'] = _clean('rays', line=3.4)[0].tex()
    T[f'{PREFIX}cap'] = _cap_tex().tex()
    T[f'{PREFIX}back'] = _back_tex().tex()
    _CACHE['tex'] = T
    return T


# ---------------------------------------------------------------------------------------------------- models
def _quad(p, tex):
    """a part's sprite: one flat quad, its anchor where the layout puts it round the joint (front: north; a back face too)"""
    (ax, ay), _o, z = LAYOUT[p]
    ox, oy = place_of(p)
    half = WINS.get(p, WIN) / 2 * DU
    cx, cy = -ox * DU, -oy * DU                                         # (design: +x is his right - your left)
    jx, jy, jz = JOINT
    fr = (jx + cx - half, jy + cy - half, jz - z * 0.25 - 0.002)
    to = (jx + cx + half, jy + cy + half, jz - z * 0.25 + 0.002)
    e = el(fr, to, tex, JOINT, faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]})
    e['shade'] = False
    return [e]


def models():
    M = {}

    def part(name, tex, p):
        M[name] = ({tex: f'bm:block/{tex}'}, _quad(p, tex))
    for p in PARTS:
        part(f'{PREFIX}{p}', f'{PREFIX}{p}', p)
        for e in EXPR.get(p, ()):
            part(f'{PREFIX}{p}_x{e}', f'{PREFIX}{p}_{e}', p)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def o(dx=0.0, dy=0.0):
    """a screen shift (painting pixels: +x your right, +y up) -> a design shift"""
    return (-dx * DU, dy * DU, 0.0)


def _turned(p, deg):
    """the shift that keeps a part turning about its own middle, not the shared joint: the part's middle, carried round by
    the turn, put back where it was (rigkit: a model point v is drawn at W + Q.D(v - joint))"""
    from rigkit import D, qrot
    ox, oy = place_of(p)
    c = D((-ox * DU, -oy * DU, 0.0))
    r = qrot(qs(('z', deg)), c)
    return D(tuple(c[i] - r[i] for i in range(3)))


def Q(lift=0.0, **spec):
    """a pose: lift (design units, the whole trio), then per part a face (a string) or dict(r=turn in degrees - about the
    part's own middle, on the screen's plane; o=(dx, dy) screen shift in painting pixels; f=face)"""
    out = {'_off': (0.0, lift, 0.0)}
    for p, sp in spec.items():
        if isinstance(sp, str):
            sp = {'f': sp}
        if sp.get('f'):
            out[f'_face_{p}'] = sp['f']
        sh = o(*sp.get('o', (0.0, 0.0)))
        if sp.get('r'):
            out[p] = qs(('z', sp['r']))
            if PARENT[p] is None and p != 'head':
                t = _turned(p, sp['r']); sh = tuple(sh[i] + t[i] for i in range(3))
        if any(abs(v) > 1e-9 for v in sh):
            out[f'_o_{p}'] = sh
    return out


def bob(k, n, amp=10.0, phase=0.0):
    return amp * math.sin(2 * math.pi * k / n + phase)


def drift(k, n=4, faces=None, lift=0.0, lean=0.0, trail=0.0, amp=1.0):
    """their float: each on its own beat (and leaning into a move, the small ones trailing behind)"""
    f = faces or {}
    return Q(lift + bob(k, n, 0.45 * amp),
             head=dict(o=(0, bob(k, n, 6 * amp, 0.9)), r=lean * 0.6, f=f.get('head')),
             moon=dict(o=(-trail * 0.6, bob(k, n, 9 * amp, 1.6)), r=lean + bob(k, n, 3 * amp, 2.2), f=f.get('moon')),
             star=dict(o=(bob(k, n, 5 * amp, 0.6) - trail, bob(k, n, 7 * amp, 2.6)), r=bob(k, n, 8 * amp, 1.1) + lean * 1.5, f=f.get('star')),
             body=dict(o=(bob(k, n, 6 * amp, 3.1) - trail * 0.4, bob(k, n, 5 * amp, 0.3)), r=lean * 0.4, f=f.get('body')))


POSES = {}
for _k in range(4):
    POSES[f'idle_{_k}'] = drift(_k)
POSES['idle_a'] = POSES['idle_0']
POSES['idle_b'] = drift(2, faces=dict(moon='awake', star='blink', body='happy'))            # (Snooze opens an eye; Nimbus beams)
POSES['idle_c'] = drift(1, faces=dict(head='grin', star='smug'))                            # (Sunny shows off; Twinkle unimpressed)
for _k in range(4):                                                                         # moving: leaning into it, the small ones trailing
    POSES[f'walk_{_k}'] = drift(_k, lean=-5, trail=10)
    POSES[f'run_{_k}'] = drift(_k, lean=-11, trail=34, amp=1.3, faces=dict(head='grin', star='angry'))
POSES['jump'] = Q(2.0, head='surprised', body='surprised', star='surprised', moon='surprised')
# sitting: they settle low - Nimbus a bed, Snooze curled up asleep on him, Twinkle tucked by her, Sunny dozing behind
POSES['sit_a'] = Q(-6.0, moon=dict(o=(-60, -170), r=-72), star=dict(o=(-150, -150), r=-20, f='blink'), head=dict(o=(-30, -50), f='sleepy'))
POSES['sit_b'] = Q(-6.2, moon=dict(o=(-58, -166), r=-76), star=dict(o=(-146, -146), r=-26, f='blink'), head=dict(o=(-30, -56), f='sleepy'), body='blink')
# SUNBEAM: Sunny rises, swells, glares - then the beam
POSES['beam_up'] = Q(0.5, head=dict(o=(-10, 40), r=-6, f='fierce'), star='smug')
POSES['beam'] = Q(0.5, head=dict(o=(-20, 54), r=4, f='fierce'), body='surprised', star='smug')
# STAR SHOT: Twinkle winds back - and hurls herself forward (a star of light leaves her)
POSES['shot_up'] = Q(star=dict(o=(40, 40), r=40, f='angry'))
POSES['shot'] = Q(star=dict(o=(-90, -10), r=-60, f='angry'), head='grin')
# ZAP: Nimbus puffs up, glowering - then the bolt
POSES['zap_up'] = Q(body=dict(o=(0, 26), r=-3, f='angry'))
POSES['zap'] = Q(body=dict(o=(0, -12), r=3, f='angry'), head='surprised')
# LULLABY: Snooze rocks and sings (Nimbus hums along; the others nod off)
POSES['lull_a'] = Q(moon=dict(o=(-10, 10), r=-14, f='yawn'), body='sing', star='blink', head='sleepy')
POSES['lull_b'] = Q(moon=dict(o=(10, 14), r=14, f='happy'), body='happy', star='blink', head='sleepy')
# DRIZZLE: Nimbus drifts over you, raining - the rest cheer
POSES['drizzle'] = Q(body=dict(o=(-60, 70), f='happy'), head='grin', star='happy', moon='happy')
# THE FORECAST (charged): all three rise and let everything go at once
POSES['forecast_a'] = Q(1.5, head=dict(o=(-40, 30), f='fierce'), moon=dict(o=(30, 50), f='awake'), star=dict(o=(30, 60), f='angry'), body=dict(o=(0, 40), f='angry'))
POSES['forecast_b'] = Q(2.0, head=dict(o=(-60, 60), r=8, f='fierce'), moon=dict(o=(50, 70), r=-10, f='surprised'), star=dict(o=(50, 90), r=30, f='angry'),
                        body=dict(o=(0, 70), f='angry'))
POSES['happy'] = Q(1.5, head='grin', moon='happy', star='happy', body='happy')
POSES['wave_a'] = Q(1.0, head=dict(r=10, f='grin'), moon=dict(r=-12, f='happy'), star=dict(r=20, f='smug'), body=dict(r=-3, f='happy'))
POSES['wave_b'] = Q(1.3, head=dict(r=-10, f='grin'), moon=dict(r=12, f='happy'), star=dict(r=-20, f='smug'), body=dict(r=3, f='happy'))
POSES['hurt'] = Q(-1.0, moon=dict(o=(10, 0), r=8, f='hurt'), star=dict(o=(-10, 6), r=-15, f='hurt'), head='hurt', body='hurt')
POSES['tired'] = Q(-3.0, head='sleepy', moon=dict(r=-10, f='yawn'), star='blink', body='blink')
SWIM_FRAMES = 4
for _k in range(SWIM_FRAMES):                      # (over water they bob along above it)
    POSES[f'swim_{_k}'] = drift(_k, SWIM_FRAMES, lift=2.0, faces=dict(head='surprised', body='surprised'))
# the rays' own clock: a step at a time on right_rotation (under any pose's left_rotation, so the two never fight)
SPIN = 12
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'run_1', 'sit_a', 'beam_up', 'beam', 'shot_up', 'shot', 'zap', 'lull_a', 'drizzle', 'forecast_b', 'happy', 'hurt']


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sky_tex'
    os.makedirs(out, exist_ok=True)
    for k, im in textures().items():
        im.save(os.path.join(out, k + '.png'))
    print(len(textures()), 'textures')
