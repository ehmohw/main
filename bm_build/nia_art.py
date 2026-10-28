"""2.95e: NIA - a tortoiseshell house cat, from the owner's photo. Slim. Her coat is a soft tortoiseshell: ginger and black
finely brindled and BLENDED (a lot of amber and brown between them), darker zones over the back and the top of the head,
lighter ginger on the shoulders, chest and legs. A crisp black blaze runs down the middle of her face from forehead to nose;
the cheek on her left (the viewer's right) is bright ginger, the other darker and brindled; a cream chin under the mouth; a
black nose; big yellow-green eyes; ears dark outside, pink inside. The rig is the house cats' (cat_art_base).

(2.95e, reworked after the owner's look: painted a pixel at a time, not in 2-px cells - a 7-tone ramp blended across smooth
zones, then short directional fur strokes one tone either side of the zone, so the brindle reads as fur and never as single
specks; every part painted from the same ramp, so the seams between boxes don't show.)"""
import math
import random
from PIL import Image, ImageDraw
from phase57_art import hexc
import cat_art_base as B

RAMP = ['#120d0a', '#2a1b12', '#4a2e1a', '#734522', '#a0632e', '#c6843e', '#dea35c', '#ebbd7c']     # black .. light ginger
CREAM, CREAM_D = '#efe2c4', '#d9c49e'
NOSE = '#1a1210'
IRIS_T, IRIS_B, EYE_RIM, PUPIL = '#a3b23c', '#dbe47c', '#1c1c0c', '#0a0807'


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


_RAMP = [hexc(c) for c in RAMP]


def ramp(v):
    """0..1 -> the coat's colour, blended between the ramp's tones (so there's always a mid-tone between ginger and black)"""
    v = min(0.999, max(0.0, v)) * (len(_RAMP) - 1); i = int(v)
    return _mix(_RAMP[i], _RAMP[i + 1], v - i)


def _field(seed, nx, ny, w=64, h=64):
    """smooth value noise (nx by ny lattice - more cells one way than the other stretches it into streaks)"""
    rnd = random.Random(seed); g = [[rnd.random() for _ in range(nx + 1)] for _ in range(ny + 1)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            fx, fy = x / w * nx, y / h * ny; ix, iy = int(fx), int(fy); tx, ty = fx - ix, fy - iy
            tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
            a = g[iy][ix] * (1 - tx) + g[iy][ix + 1] * tx; b = g[iy + 1][ix] * (1 - tx) + g[iy + 1][ix + 1] * tx
            out[y][x] = a * (1 - ty) + b * ty
    return out


def tortie(seed, bias=-0.06, angle=0.0, strokes=420, contrast=1.3):
    """the coat: broad zones (black ... ginger) from a smooth field, blended through the ramp; then short fur strokes along
    `angle` (degrees; 0 = across the texture), each one or two tones off the zone under it - brindle, in the fur's direction"""
    big, mid = _field(seed, 4, 4), _field(seed + 1, 9, 7)
    im = Image.new('RGBA', (64, 64)); px = im.load()
    val = [[0.0] * 64 for _ in range(64)]
    for y in range(64):
        for x in range(64):
            v = 0.5 + ((big[y][x] - 0.5) * 1.5 + (mid[y][x] - 0.5) * 0.7) * contrast + bias
            v = 0.5 + math.tanh((v - 0.5) * 3.0) / 2.1                             # (zones that hold their colour, soft edges)
            val[y][x] = v; px[x, y] = ramp(v)
    d = ImageDraw.Draw(im); r = random.Random(seed + 2)
    for _ in range(strokes):                                                      # (fur: short strokes, the way it lies)
        x, y = r.uniform(0, 64), r.uniform(0, 64); v = val[int(y)][int(x)]
        a = math.radians(angle + r.uniform(-30, 30)); ln = r.uniform(1.8, 3.6)
        dv = r.choice((-0.16, -0.1, 0.1, 0.16)) if v > 0.3 else r.choice((0.1, 0.16, 0.22))  # (dark zones get amber flecks)
        d.line((x, y, x + math.cos(a) * ln, y + math.sin(a) * ln), fill=ramp(v + dv), width=1)
    for _ in range(strokes // 5):                                                 # (brindle dabs: a few pixels, never one alone)
        x, y = r.randrange(0, 63), r.randrange(0, 63); v = val[y][x]
        c = ramp(v - 0.32) if v > 0.5 else ramp(v + 0.3)
        d.rectangle((x, y, x + r.choice((1, 2)), y + r.choice((0, 1))), fill=c)
    return im


def solid_soft(col, col2, seed, n=4):
    """a plain soft colour (cream, pink), gently shaded between two tones - no specks"""
    f = _field(seed, n, n); im = Image.new('RGBA', (64, 64)); px = im.load(); a, b = hexc(col), hexc(col2)
    for y in range(64):
        for x in range(64): px[x, y] = _mix(a, b, f[y][x] * 0.8)
    return im


def eye(px, x0, y0, kind, w=7, h=5):
    """one eye on the face (pixels): an almond with a dark rim, the iris yellow-green, brighter low down, a dark pupil and a glint"""
    P = lambda x, y, c: px.__setitem__((x, y), c if isinstance(c, tuple) else hexc(c)) if 0 <= x < 64 and 0 <= y < 64 else None
    if kind in ('blink', 'happy'):
        for i in range(w):
            dy = 0 if kind == 'blink' else (-1 if 0 < i < w - 1 else 0)
            P(x0 + i, y0 + h // 2 + dy + (1 if kind == 'blink' and i in (0, w - 1) else 0), EYE_RIM)
        P(x0 + w - 1, y0 + h // 2 - 1, EYE_RIM)                                   # (a lash flick at the outer corner)
        return
    top = y0 - (1 if kind == 'alert' else 0); bot = y0 + h - 1
    for y in range(top, bot + 1):
        for x in range(x0, x0 + w):
            if (x in (x0, x0 + w - 1)) and (y in (top, bot)): continue                # (the almond's corners)
            edge = x in (x0, x0 + w - 1) or y in (top, bot)
            t = (y - top) / max(1, bot - top)
            P(x, y, EYE_RIM if edge else _mix(hexc(IRIS_T), hexc(IRIS_B), t))
    mid = x0 + w // 2
    pw = 2 if kind == 'alert' else 1                                              # (rounder when alert)
    for y in range(top + 1, bot):
        for dx in range(pw): P(mid - dx, y, PUPIL)
    P(mid - pw - 1 if kind != 'alert' else mid - 3, top + 1, '#ffffff')           # (the glint)
    P(mid + 1, bot - 1, '#eef4c8')


def face(kind=None):
    """the face (22 x 17 px at its uv; the muzzle covers the middle of rows 10-16): the dark brindled forehead, the crisp black
    blaze down the middle, the cheek on the viewer's left darker and brindled, the other bright ginger, the eyes either side"""
    im = Image.new('RGBA', (64, 64)); px = im.load()
    dark, warm, bright = tortie(5201, -0.2, 90), tortie(5221, 0.05, 20), tortie(5222, 0.32, 160, contrast=0.6)
    dk, wm, br = dark.load(), warm.load(), bright.load()
    for y in range(64):
        for x in range(64):
            # forehead dark at the top, fading into the cheeks; left cheek mixed, right cheek bright
            t = min(1.0, max(0.0, (y - 2) / 5.0))
            side = br[x, y] if x >= 12 else wm[x, y]
            if 10 <= x <= 12: side = _mix(wm[x, y], br[x, y], (x - 10) / 2)
            px[x, y] = _mix(dk[x, y], side, t)
    for y in range(17):                                                           # the blaze: crisp black, wide on the forehead
        hw = 3.2 if y < 3 else (2.2 if y < 7 else 1.6)
        for x in range(22):
            dd = abs(x + 0.5 - 11.0) - hw
            if dd < 0: px[x, y] = hexc(RAMP[0])
            elif dd < 1: px[x, y] = _mix(hexc(RAMP[0]), px[x, y], 0.55)
    eye(px, 1, 5, kind); eye(px, 14, 5, kind)
    return im


def mfront():
    """the front of the muzzle (12 x 7 px): the blaze running down into the black nose; a darker whisker pad on the viewer's
    left, a ginger one on the right; the mouth; the cream chin below (soft edged)"""
    im = Image.new('RGBA', (64, 64)); px = im.load()
    L, R_ = tortie(5203, -0.05, 0, 200).load(), tortie(5223, 0.3, 0, 200, 0.6).load()
    for y in range(64):
        for x in range(64): px[x, y] = L[x, y] if x < 6 else R_[x, y]
    for y in range(3):                                                            # the blaze into the nose
        for x in range(4, 8): px[x, y] = hexc(RAMP[0])
    for x, y in ((5, 1), (6, 1), (5, 2), (6, 2), (4, 2), (7, 2)): px[x, y] = hexc(NOSE)
    px[5, 3] = px[6, 3] = hexc('#0a0706')                                         # (the philtrum)
    for x in range(2, 10): px[x, 4] = hexc('#0a0706') if x in (3, 4, 5, 6, 7, 8) else px[x, 4]
    for y in range(5, 7):
        for x in range(12): px[x, y] = _mix(hexc(CREAM), hexc(CREAM_D), 0.3 if (x + y) % 3 == 0 else 0.0)
    for x in range(12): px[x, 4] = _mix(px[x, 4], hexc(CREAM), 0.35) if px[x, 4][:3] != hexc('#0a0706')[:3] else px[x, 4]
    return im


def crown():
    """the top of the head: dark, the blaze running back over it (crisp edged)"""
    im = tortie(5204, -0.22, 90); px = im.load()
    for y in range(64):
        for x in range(22):
            dd = abs(x + 0.5 - 11.0) - 3.0
            if dd < 0: px[x, y] = hexc(RAMP[0])
            elif dd < 1: px[x, y] = _mix(hexc(RAMP[0]), px[x, y], 0.5)
    return im


def look(p):
    T = {f'{p}fur': tortie(5207, 0.0, 0), f'{p}back': tortie(5208, -0.2, 0), f'{p}belly': tortie(5209, 0.18, 0, contrast=0.7),
         f'{p}cheek': tortie(5210, 0.12, 90), f'{p}chest': tortie(5211, 0.22, 90, contrast=0.7), f'{p}throat': tortie(5212, 0.08, 90),
         f'{p}muzzle': tortie(5213, 0.1, 0), f'{p}mfront': mfront(), f'{p}chin': solid_soft(CREAM, CREAM_D, 5214),
         f'{p}ear': tortie(5205, -0.3, 90, contrast=0.6), f'{p}ear_in': solid_soft('#c98a86', '#e6b0aa', 5206),
         f'{p}leg': tortie(5215, 0.14, 90), f'{p}paw': tortie(5216, 0.04, 90), f'{p}tail': tortie(5217, -0.08, 90),
         f'{p}tail_tip': tortie(5218, -0.4, 90, contrast=0.4), f'{p}face': face(), f'{p}crown': crown(),
         f'{p}headfur': tortie(5219, -0.2, 90)}
    for k in B.FACES: T[f'{p}face_{k}'] = face(k)
    return T


globals().update(B.make('ni_', look, dict(stock=0.92, long=1.0, tall=1.0, scale=1.0, head_tex='headfur')))
