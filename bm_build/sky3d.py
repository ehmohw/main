"""2.94e: THE SKY BUDDIES, MODELLED - new blocky 3D models, designed from the owner's painting rather than cut from it (the owner:
"scrap using my art and do entirely new 3D models based off of it"). Each part is built of boxes, like Emma, and painted in
pixel art at 4 texels a design unit (32 to the block at the rig's scale 2):

SUNNY      a stepped ball of a sun (rows of boxes, round from the front and the side), his shades a 3D pair of black lenses on
           a frame, the arms running back along his sides; brows and a smirk painted on. His RAYS: twelve stepped wedges round
           him, a part of their own so they can spin.
SNOOZE     a chunky crescent (rows of boxes between two circles), asleep, her crater on her; her NIGHTCAP a cone of boxes that
           flops over at the tip, a fur band round its brim and a bobble at the end (a texture of its own - the wardrobe
           recolours it).
TWINKLE    a fat little five-point star, pixel-cut and puffed, scowling.
NIMBUS     a cloud of stepped puffs on a flat base, ":3" on his biggest; behind him a second, darker cloud.

The layout, the joint, the parts, the faces and the poses are sky_art's (each part sits at its place round the joint, as in
the painting); this module only builds the geometry and the textures. Coordinates here are the viewer's: X to your right, Y
up, Z toward you (rigkit's design frame has +x on your left and its front at -z)."""
import math
from PIL import Image

from rigkit import el

RES = 4                                             # (texels a design unit)
Q = 1.0 / RES


def hexc(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3)) + (255,)


def shade(c, k):
    return tuple(max(0, min(255, int(round(v * k)))) for v in c[:3]) + (255,)


def noise(i, j, seed=0):
    h = (i * 73856093) ^ (j * 19349663) ^ (seed * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    return ((h ^ (h >> 16)) & 1023) / 1023.0


def snap(v):
    return round(v * RES) / RES


INK = hexc('#1c1816')
WHITE = hexc('#f8f8f4')


# ---------------------------------------------------------------------------------------------------- a part: boxes, painted
class Part:
    """boxes in the viewer's frame round the part's own middle; each painted by `paint(side, X, Y, Z, box)` -> RGBA, side one
    of front / back / left / right / top / bottom (as the viewer sees it)"""

    def __init__(self, paint):
        self.boxes, self.paint = [], paint

    def box(self, lo, hi, tag='', rot=None, paint=None):
        """lo, hi: (X, Y, Z) corners; rot: degrees about the viewer's Z (toward you), round `rot_at`"""
        lo = tuple(snap(v) for v in lo); hi = tuple(snap(v) for v in hi)
        if any(hi[i] - lo[i] < Q * 0.99 for i in range(3)):
            return
        self.boxes.append(dict(lo=lo, hi=hi, tag=tag, rot=rot, paint=paint or self.paint))


# the face quads (rigkit's design frame, as the game draws them: corner i takes uv corner (u0,v0) (u1,v0) (u1,v1) (u0,v1))
def _quads(f, t):
    x1, y1, z1 = f; x2, y2, z2 = t
    return {'north': [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)],
            'south': [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
            'east': [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)],
            'west': [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
            'up': [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)],
            'down': [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)]}


SIDE = {'north': 'front', 'south': 'back', 'east': 'left', 'west': 'right', 'up': 'top', 'down': 'bottom'}


def build(part, tex, at, piv):
    """-> (elements in rigkit's design frame - the part's middle at `at` (design units), round the joint `piv` - and its
    texture: an atlas of every face, each painted)"""
    ax, ay, az = at
    faces = []                                                          # (box, face, w, h, quad in viewer coords)
    for b in part.boxes:
        (X0, Y0, Z0), (X1, Y1, Z1) = b['lo'], b['hi']
        f, t = (-X1, Y0, -Z1), (-X0, Y1, -Z0)                         # (viewer -> design, part-local)
        for fc, q in _quads(f, t).items():
            P = [(-x, y, -z) for x, y, z in q]                          # (back to the viewer's frame, for the painter)
            w = round(math.dist(q[0], q[1]) * RES); h = round(math.dist(q[0], q[3]) * RES)
            faces.append((b, fc, max(1, w), max(1, h), P, f, t))
    # shelf-pack the faces into the smallest square that holds them, a texel apart (each face's edge carried into the gap: no
    # neighbour's colour bleeds onto it, at a distance or at a seam)
    N = 32
    while True:
        x = y = row = 0; place = []
        ok = True
        for b, fc, w, h, P, f, t in sorted(faces, key=lambda r: -r[3]):
            if x + w + 2 > N:
                x, y, row = 0, y + row, 0
            if y + h + 2 > N or w + 2 > N:
                ok = False; break
            place.append((b, fc, w, h, P, f, t, x + 1, y + 1)); x += w + 2; row = max(row, h + 2)
        if ok:
            break
        N *= 2
    im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); px = im.load()
    k = 16.0 / N
    els = {}
    for b, fc, w, h, P, f, t, x0, y0 in place:
        for j in range(h):
            for i in range(w):
                s, v = (i + 0.5) / w, (j + 0.5) / h
                p = [P[0][c] * (1 - s) * (1 - v) + P[1][c] * s * (1 - v) + P[2][c] * s * v + P[3][c] * (1 - s) * v for c in range(3)]
                px[x0 + i, y0 + j] = b['paint'](SIDE[fc], p[0], p[1], p[2], b)
        for j in range(-1, h + 1):
            for i in range(-1, w + 1):
                if 0 <= i < w and 0 <= j < h:
                    continue
                px[x0 + i, y0 + j] = px[x0 + min(w - 1, max(0, i)), y0 + min(h - 1, max(0, j))]
        els.setdefault(id(b), (b, f, t, {}))[3][fc] = {'uv': [round(x0 * k, 4), round(y0 * k, 4), round((x0 + w) * k, 4), round((y0 + h) * k, 4)],
                                                       'texture': '#' + tex}
    out = []
    for b, f, t, fcs in els.values():
        fr = (f[0] + ax, f[1] + ay, f[2] + az); to = (t[0] + ax, t[1] + ay, t[2] + az)
        rot = None
        if b['rot']:
            ang, (cx, cy) = b['rot']
            rot = ((0.0, 0.0, -ang), (-cx + ax, cy + ay, az))          # (about the viewer's Z: the design's -z, so the angle flips)
        e = el(fr, to, tex, piv, rot=rot)
        e['faces'] = fcs
        out.append(e)
    return out, im


# ---------------------------------------------------------------------------------------------------- pixel faces
class Face:
    """pixels on the front, in texels round the part's middle (i to your right, j up)"""

    def __init__(self):
        self.px = {}

    def put(self, i, j, c):
        self.px[(i, j)] = c

    def rect(self, i0, j0, i1, j1, c):
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                self.px[(i, j)] = c

    def pts(self, pts, c):
        for i, j in pts:
            self.px[(i, j)] = c

    def at(self, X, Y):
        return self.px.get((math.floor(X * RES), math.floor(Y * RES)))


def rows_ball(part, cx, cy, R, depth=0.8, zc=0.0, step=0.5, tag='', paint=None, flat_bottom=None):
    """a stepped ball: rows `step` high, each a box as wide as the circle there and `depth` of that deep"""
    n = int(math.ceil(R / step))
    for k in range(-n, n):
        y0, y1 = k * step, (k + 1) * step
        if flat_bottom is not None and cy + y1 <= flat_bottom:
            continue
        ym = (y0 + y1) / 2
        if abs(ym) >= R:
            continue
        hw = snap(math.sqrt(R * R - ym * ym))
        if hw < Q:
            continue
        hd = snap(hw * depth)
        part.box((cx - hw, cy + max(y0, (flat_bottom - cy) if flat_bottom is not None else y0), zc - hd), (cx + hw, cy + y1, zc + hd), tag=tag, paint=paint)


# ---------------------------------------------------------------------------------------------------- SUNNY
SUN = dict(base=hexc('#f7c325'), hi=hexc('#ffe36a'), lo=hexc('#e39a12'), rim=hexc('#c97a0e'))
RAY = dict(base=hexc('#f59a2c'), hi=hexc('#ffc060'), lo=hexc('#d06d14'), rim=hexc('#a44e0a'))
SR = 3.25                                           # (his radius)


def _sun_face(expr):
    F = Face(); B = INK
    up = {'surprised': -2, 'sleepy': 4}.get(expr, 0)                 # (where the shades sit: down his nose, or pushed up)
    # brows
    if expr in (None, 'blink'):
        F.pts([(-9, 9), (-8, 10), (-7, 10), (-6, 11), (-5, 11), (-4, 11), (-3, 10), (-2, 10), (-9, 10), (-8, 11), (-7, 11), (-3, 11)], B)   # (an arch)
        F.pts([(2, 10), (3, 10), (4, 11), (5, 11), (6, 11), (7, 12), (8, 12), (9, 11), (3, 11), (4, 12), (5, 12), (6, 12), (7, 13), (8, 13)], B)   # (cocked)
    elif expr == 'grin':
        for s in (-1, 1):
            F.pts([(s * a, b) for a, b in ((2, 11), (3, 12), (4, 12), (5, 13), (6, 13), (7, 13), (8, 12), (9, 11), (3, 13), (4, 13), (8, 13))], B)
    elif expr == 'fierce':
        for s in (-1, 1):
            F.pts([(s * a, b) for a, b in ((2, 9), (3, 9), (4, 10), (5, 10), (6, 11), (7, 11), (8, 12), (9, 12), (2, 10), (3, 10), (4, 11), (5, 11), (6, 12), (7, 12))], B)
    elif expr == 'surprised':
        for s in (-1, 1):
            F.pts([(s * a, b) for a, b in ((2, 10), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 10), (4, 12), (5, 12), (6, 12))], B)
        for s in (-1, 1):                                              # (wide eyes over the dropped shades)
            F.rect(s * 6 - 2 if s > 0 else -8, 4, s * 6 + 2 if s > 0 else -4, 8, B)
            F.rect(s * 6 - 1 if s > 0 else -7, 5, s * 6 + 1 if s > 0 else -5, 7, WHITE)
            F.put(s * 6, 6, B)
    elif expr == 'hurt':
        for s in (-1, 1):
            F.pts([(s * a, b) for a, b in ((2, 12), (3, 12), (4, 11), (5, 11), (6, 10), (7, 10), (8, 9), (3, 11), (4, 10))], B)
        F.pts([(11, 7), (11, 6), (12, 6), (11, 5), (12, 5), (10, 5), (11, 4)], hexc('#7ac8ff'))
    elif expr == 'sleepy':
        for s in (-1, 1):                                              # (eyes shut under the shades on his brow)
            F.pts([(s * a, b) for a, b in ((3, 1), (4, 0), (5, 0), (6, 0), (7, 0), (8, 1))], B)
    # mouths
    if expr in (None, 'blink'):                                        # (the smirk: teeth, up at your left)
        F.rect(-8, -7, -1, -5, WHITE)
        F.pts([(-9, -4), (-8, -4), (-7, -4), (-6, -4), (-5, -4), (-4, -4), (-3, -4), (-2, -4), (-1, -4), (0, -4), (1, -3),
               (-9, -5), (-9, -6), (-8, -7), (-8, -8), (-7, -8), (-6, -8), (-5, -8), (-4, -8), (-3, -8), (-2, -7), (-1, -7), (0, -6), (0, -5), (1, -4)], B)
        F.pts([(-7, -6), (-6, -6), (-5, -6), (-4, -6), (-3, -6), (-2, -6)], hexc('#d8d4cc'))
    elif expr == 'grin':
        F.rect(-6, -8, 6, -4, WHITE); F.rect(-4, -9, 4, -9, hexc('#c8443c')); F.rect(-3, -10, 3, -10, hexc('#c8443c'))
        for i in range(-7, 8):
            F.put(i, -3, B)
        F.pts([(-7, -4), (-7, -5), (-7, -6), (-6, -7), (-6, -8), (-5, -9), (-4, -10), (-3, -11), (-2, -11), (-1, -11), (0, -11), (1, -11), (2, -11), (3, -11),
               (4, -10), (5, -9), (6, -8), (6, -7), (7, -6), (7, -5), (7, -4)], B)
        F.rect(-5, -6, 5, -6, hexc('#d8d4cc'))
    elif expr == 'fierce':
        F.rect(-6, -8, 6, -5, WHITE)
        F.rect(-7, -4, 7, -4, B); F.rect(-7, -9, 7, -9, B); F.rect(-7, -8, -7, -5, B); F.rect(7, -8, 7, -5, B)
        for i in (-4, -1, 2, 5):
            F.rect(i, -8, i, -5, B)
    elif expr == 'surprised':
        F.rect(-2, -9, 2, -5, B); F.rect(-1, -8, 1, -6, hexc('#9a2a2a'))
    elif expr == 'hurt':
        F.rect(-6, -7, 6, -5, WHITE)
        F.pts([(i, -4 if i % 4 in (0, 1) else -5) for i in range(-7, 8)] + [(i, -8 if i % 4 in (2, 3) else -7) for i in range(-7, 8)], B)
    elif expr == 'sleepy':
        F.pts([(-3, -6), (-2, -7), (-1, -7), (0, -7), (1, -7), (2, -6)], B)
    return F, up


def sunny(expr=None):
    F, up = _sun_face(expr)

    def paint(side, X, Y, Z, b):
        i, j = math.floor(X * RES), math.floor(Y * RES)
        r = math.hypot(X, Y) / SR
        n = noise(i, j, 7 if side in ('front', 'back') else 11) - 0.5
        if side == 'top':
            return shade(SUN['hi'], 1.0 + 0.04 * n)
        if side == 'bottom':
            return shade(SUN['lo'], 0.92 + 0.04 * n)
        if side in ('left', 'right'):
            t = 0.5 + 0.5 * Y / SR
            return shade(mix(SUN['lo'], SUN['base'], t), 1.0 + 0.04 * n)
        c = mix(SUN['hi'], SUN['base'], min(1.0, max(0.0, (math.hypot(X + 1.0, Y - 1.2) / (SR * 1.4)))))
        if r > 0.86:
            c = mix(c, SUN['lo'], 0.6)
        if side == 'front':
            f = F.at(X, Y)
            if f:
                return f
        return shade(c, 1.0 + 0.05 * n)
    P = Part(paint)
    rows_ball(P, 0.0, 0.0, SR, depth=0.78)

    # the shades: two black lenses, a bridge, the bar across the top, the arms back along his sides
    def lens_paint(side, X, Y, Z, b):
        if side != 'front' or expr == 'blink':
            return shade(INK, 1.0 + 0.3 * (side == 'top'))
        cx = -1.5 if X < 0 else 1.5
        i, j = math.floor((X - cx) * RES), math.floor((Y - b['lo'][1]) * RES) - 1
        if (i, j) in ((-2, 4), (-1, 4), (-1, 3), (-1, 2), (-2, 1), (1, 4), (1, 3), (2, 4), (-2, 3)):  # (the glints: a comma and a fleck)
            return WHITE
        return shade(INK, 1.0)
    frame = lambda side, X, Y, Z, b: hexc('#2a2624') if side in ('top', 'front') else INK
    y0 = up * Q                                                         # (no face of theirs on a row's edge: those are on the half units)
    zf = snap(math.sqrt(SR * SR - (y0 + 0.5) ** 2) * 0.78)             # (his face's front, at the shades' height)
    lw = 2.5 if expr == 'sleepy' else 2.75                            # (the lenses' outer edge - never on a row's side)
    P.box((-lw, y0 - 0.25, zf - 0.25), (-0.5, y0 + 1.25, zf + 0.5), 'shades', paint=lens_paint)       # (lenses, the bar on top: nothing shares a face)
    P.box((0.5, y0 - 0.25, zf - 0.25), (lw, y0 + 1.25, zf + 0.5), 'shades', paint=lens_paint)
    P.box((-0.5, y0 + 0.75, zf), (0.5, y0 + 1.25, zf + 0.5), 'shades', paint=frame)
    row_hw = lambda y: snap(math.sqrt(max(0.0, SR * SR - ((math.floor(y / 0.5) + 0.5) * 0.5) ** 2)))     # (the ball's row at y: its half width)
    hw = max(row_hw(y0 + 1.0), row_hw(y0 + 1.45))                       # (the arms and the bar's ends just outside the widest row they pass)
    P.box((-hw - 0.25, y0 + 1.25, zf - (0.0 if expr == 'surprised' else 0.25)), (hw + 0.25, y0 + 1.5, zf + 0.5), 'shades', paint=frame)
    for s in (-1, 1):                                                  # (the arms, back along his sides to his ears)
        P.box((hw if s > 0 else -hw - 0.25, y0 + 1.0, -0.5), (hw + 0.25 if s > 0 else -hw, y0 + 1.5, zf - 0.25), 'shades', paint=frame)
    return P


def rays():
    def paint(side, X, Y, Z, b):
        n = noise(math.floor(X * RES * 3), math.floor(Y * RES * 3), 3) - 0.5
        if side in ('top', 'left'):
            return shade(RAY['hi'], 1.0 + 0.04 * n)
        if side in ('bottom', 'right'):
            return shade(RAY['lo'], 1.0 + 0.04 * n)
        return shade(RAY['base'], 1.0 + 0.05 * n)

    def rim(side, X, Y, Z, b):
        return shade(RAY['rim'], 1.0)
    P = Part(paint)
    for k in range(12):
        ang = 15.0 + 30.0 * k
        r0 = SR + 0.5
        for w, l, d in ((1.75, 0.75, 0.75), (1.25, 0.5, 0.75), (0.75, 0.5, 0.5), (0.25, 0.25, 0.5)):
            P.box((-w / 2, r0, -d / 2), (w / 2, r0 + l, d / 2), rot=(ang, (0.0, 0.0)))
            r0 += l
    return P


# ---------------------------------------------------------------------------------------------------- SNOOZE, her cap
MOON = dict(base=hexc('#f4eab0'), hi=hexc('#fffbe0'), lo=hexc('#d8cc84'), crater=hexc('#8f8a3a'), crater_d=hexc('#6c6a28'))
# her outline, traced off the painting round her middle (design units, X to your right): the top horn (under the cap), down
# her back, the long lower horn sweeping to your left - and back up her inner curve
MOON_OUT = [(1.69, 2.51), (2.15, 2.45), (2.42, 1.82), (2.6, 0.91), (2.56, 0.0), (2.33, -0.91), (1.87, -1.64), (1.15, -2.18), (0.24, -2.45),
            (-1.04, -2.42), (-2.13, -2.09), (-2.75, -1.64)]
MOON_IN = [(-1.75, -1.4), (-0.6, -1.2), (0.1, -0.95), (0.55, -0.45), (0.8, 0.0), (0.88, 0.91), (1.05, 1.82)]   # (her inner curve set in a little from the painting's: chunkier, for a blocky moon)
MO_C, MO_R = (0.3, 0.0), 2.6                        # (for her shading: her middle, her size)


def _crescent_rows():
    """her rows, a texel high: (y0, y1, x0, x1) for each run inside her outline"""
    poly = MOON_OUT + MOON_IN
    out = []
    for k in range(-12, 12):
        y0, y1 = k * Q, (k + 1) * Q; ym = (y0 + y1) / 2
        xs = []
        for n in range(len(poly)):
            (xa, ya), (xb, yb) = poly[n], poly[(n + 1) % len(poly)]
            if (ya > ym) != (yb > ym):
                xs.append(xa + (xb - xa) * (ym - ya) / (yb - ya))
        xs.sort()
        for a, b in zip(xs[0::2], xs[1::2]):
            a, b = snap(a), snap(b)
            if b - a >= Q:
                out.append((y0, y1, a, b))
    return out


def _moon_face(expr):
    F = Face(); B = INK
    ex, ey = 7, 4                                    # (her eye: high on her, as the painting has it)
    if expr in (None, 'drowsy') or expr is None:
        F.pts([(ex - 2, ey), (ex - 1, ey - 1), (ex, ey - 1), (ex + 1, ey - 1), (ex + 2, ey), (ex - 3, ey + 1), (ex + 3, ey + 1)], B)    # (shut, a sleepy curve)
        if expr == 'drowsy':
            F.pts([(ex - 1, ey), (ex, ey), (ex + 1, ey)], WHITE)
    elif expr in ('awake', 'surprised'):
        h = 2 if expr == 'awake' else 3
        F.rect(ex - 2, ey - h, ex + 2, ey + h, B); F.rect(ex - 1, ey - h + 1, ex + 1, ey + h - 1, WHITE); F.put(ex, ey, B)
        if expr == 'surprised':
            F.pts([(ex - 2, ey + 5), (ex - 1, ey + 6), (ex, ey + 6), (ex + 1, ey + 6), (ex + 2, ey + 5)], B)
    elif expr == 'hurt':
        F.pts([(ex - 2, ey + 2), (ex - 1, ey + 1), (ex, ey), (ex - 1, ey - 1), (ex - 2, ey - 2)], B)
    elif expr == 'yawn':
        F.pts([(ex - 2, ey), (ex - 1, ey - 1), (ex, ey - 1), (ex + 1, ey - 1), (ex + 2, ey)], B)
    elif expr == 'happy':
        F.pts([(ex - 2, ey - 1), (ex - 1, ey), (ex, ey + 1), (ex + 1, ey), (ex + 2, ey - 1)], B)
    mx, my = 8, 1                                    # (her mouth, below)
    if expr == 'yawn':
        F.rect(mx - 1, my - 3, mx + 2, my, B); F.rect(mx, my - 2, mx + 1, my - 1, hexc('#b04050'))
    elif expr == 'surprised':
        F.rect(mx, my - 2, mx + 1, my, B)
    elif expr == 'hurt':
        F.pts([(mx - 1, my), (mx, my - 1), (mx + 1, my), (mx + 2, my - 1)], B)
    else:
        F.pts([(mx - 1, my), (mx, my - 1), (mx + 1, my - 1), (mx + 2, my)], B)      # (a small smile)
    return F


def snooze(expr=None):
    F = _moon_face(expr)

    def crater(X, Y):
        for cx, cy, r in ((1.1, -1.55, 0.55), (1.65, -1.15, 0.38)):
            if math.hypot(X - cx, Y - cy) < r:
                return math.hypot(X - cx, Y - cy) > r - 0.3
        return None

    def paint(side, X, Y, Z, b):
        i, j = math.floor(X * RES), math.floor(Y * RES)
        n = noise(i, j, 21) - 0.5
        if side == 'top':
            return shade(MOON['hi'], 1.0 + 0.03 * n)
        if side == 'bottom':
            return shade(MOON['lo'], 0.95 + 0.03 * n)
        if side in ('left', 'right'):
            return shade(mix(MOON['lo'], MOON['base'], 0.5 + 0.5 * (Y - MO_C[1]) / MO_R), 1.0 + 0.04 * n)
        if side == 'front':
            f = F.at(X, Y)
            if f:
                return f
            c = crater(X, Y)
            if c is not None:
                return MOON['crater_d'] if c else MOON['crater']
        c = mix(MOON['hi'], MOON['base'], min(1.0, math.hypot(X - 0.6, Y - 1.2) / 3.0))
        if side == 'back':
            c = shade(c, 0.95)
        return shade(c, 1.0 + 0.04 * n)
    P = Part(paint)
    for y0, y1, x0, x1 in _crescent_rows():
        hd = 0.75 if x1 - x0 >= 1.0 else 0.5 if x1 - x0 >= 0.5 else 0.25      # (a flat front where her face is; the horns thinner)
        P.box((x0, y0, -hd), (x1, y1, hd))
    return P


CAP = dict(base=hexc('#9cc4dc'), hi=hexc('#c4e0f0'), lo=hexc('#6f9cbc'))
FUR = dict(base=hexc('#f6f6f2'), lo=hexc('#d4d6dc'))


def cap():
    def cloth(side, X, Y, Z, b):
        n = noise(math.floor(X * RES), math.floor(Y * RES), 31) - 0.5
        c = CAP['hi'] if side == 'top' else CAP['lo'] if side in ('bottom', 'right') else CAP['base']
        if side == 'front' and (math.floor(X * RES) + math.floor(Y * RES)) % 5 == 0:
            c = mix(c, CAP['lo'], 0.35)                                 # (a knit's slant)
        return shade(c, 1.0 + 0.05 * n)

    def fur(side, X, Y, Z, b):
        i, j = math.floor(X * RES), math.floor(Y * RES)
        c = FUR['lo'] if side == 'bottom' or (noise(i, j, 41) > 0.72) else FUR['base']
        return c
    P = Part(cloth)
    # (on her top horn: the fur band round the brim, then the cone leaning over to your right, its bobble hanging at the tip)
    o = (-0.25, 0.0)
    bx = lambda lo, hi, paint=None: P.box((lo[0] + o[0], lo[1] + o[1], lo[2]), (hi[0] + o[0], hi[1] + o[1], hi[2]), paint=paint)
    bx((-0.75, -0.75, -0.75), (0.75, -0.25, 0.75), fur)
    bx((-0.625, -0.25, -0.625), (0.625, 0.25, 0.625))
    bx((-0.375, 0.25, -0.5), (0.625, 0.75, 0.5))
    bx((0.0, 0.75, -0.375), (0.875, 1.125, 0.375))
    bx((0.625, 0.5, -0.25), (1.25, 0.875, 0.25))
    bx((0.875, 0.0, -0.375), (1.5, 0.625, 0.375), fur)
    return P


# ---------------------------------------------------------------------------------------------------- TWINKLE
STAR = dict(base=hexc('#ffe94a'), hi=hexc('#fff8a8'), lo=hexc('#e2b818'), rim=hexc('#b88a0c'))
ST_R, ST_r = 1.3, 0.56


def _star_mask():
    """her shape, a texel at a time: a five-point star (point up)"""
    cells = set()
    pts = []
    for k in range(10):
        a = math.pi / 2 + k * math.pi / 5
        r = ST_R if k % 2 == 0 else ST_r
        pts.append((r * math.cos(a), r * math.sin(a)))

    def inside(x, y):
        c = False
        for k in range(10):
            (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % 10]
            if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                c = not c
        return c
    n = int(ST_R * RES) + 1
    for i in range(-n, n):
        for j in range(-n, n):
            if inside((i + 0.5) * Q, (j + 0.5) * Q):
                cells.add((i, j))
    return cells


def _star_face(expr):
    F = Face(); B = INK
    L, R = (-2, 0), (1, 0)
    if expr in (None, 'angry', 'smug'):
        F.pts([(-3, 1), (-2, 1), (1, 1), (2, 1)] if expr is None else [(-3, 2), (-2, 1), (1, 1), (2, 2)], B)      # (flat, grumpy lids - or slanted)
        F.pts([L, R], B)
        F.pts([(-1, -2), (0, -2)] if expr != 'smug' else [(-1, -2), (0, -2), (1, -1)], B)
    elif expr == 'surprised':
        F.pts([L, R, (L[0], L[1] + 1), (R[0], R[1] + 1)], B); F.pts([(-1, -2), (0, -2), (-1, -3), (0, -3)], B)
    elif expr == 'hurt':
        F.pts([(-3, 1), (-2, 0), (-3, -1), (2, 1), (1, 0), (2, -1)], B); F.pts([(-2, -2), (-1, -3), (0, -2), (1, -3)], B)
    elif expr == 'blink':
        F.pts([(-3, 0), (-2, 0), (1, 0), (2, 0)], B); F.pts([(-1, -2), (0, -2)], B)
    elif expr == 'happy':
        F.pts([(-3, 0), (-2, 1), (1, 1), (2, 0)], B); F.pts([(-2, -2), (-1, -3), (0, -3), (1, -2)], B)
    return F


def twinkle(expr=None):
    F = _star_face(expr)
    cells = _star_mask()

    def paint(side, X, Y, Z, b):
        i, j = math.floor(X * RES), math.floor(Y * RES)
        n = noise(i, j, 51) - 0.5
        if side == 'top':
            return shade(STAR['hi'], 1.0)
        if side in ('bottom', 'right'):
            return shade(STAR['lo'], 0.96)
        if side == 'left':
            return shade(STAR['base'], 0.98)
        if side == 'front':
            f = F.at(X, Y)
            if f:
                return f
        return shade(mix(STAR['hi'], STAR['base'], min(1.0, math.hypot(X + 0.3, Y - 0.3) / 1.2)), 1.0 + 0.04 * n)
    P = Part(paint)
    # each row's runs, deeper in the middle
    rows = {}
    for i, j in cells:
        rows.setdefault(j, []).append(i)
    for j, xs in rows.items():
        xs.sort(); run = [xs[0]]
        for x in xs[1:] + [None]:
            if x is not None and x == run[-1] + 1:
                run.append(x); continue
            mid = (run[0] + run[-1] + 1) / 2 * Q
            d = snap(0.5 + 0.25 * max(0.0, 1.0 - math.hypot(mid, (j + 0.5) * Q) / ST_R) * 2)
            P.box((run[0] * Q, j * Q, -d / 2), ((run[-1] + 1) * Q, (j + 1) * Q, d / 2))
            if x is not None:
                run = [x]
    return P


# ---------------------------------------------------------------------------------------------------- NIMBUS and the cloud behind
CLOUD = dict(base=hexc('#d6d6da'), hi=hexc('#f0f0f2'), lo=hexc('#a8a8b0'), under=hexc('#8e8e98'))
BACK = dict(base=hexc('#b0b0b8'), hi=hexc('#c8c8ce'), lo=hexc('#8a8a94'), under=hexc('#74747e'))
PUFFS = [(0.0, 0.5, 2.0), (-2.6, -0.15, 1.45), (2.45, 0.0, 1.5), (-4.1, -0.75, 0.9), (4.0, -0.7, 0.85)]
BACK_PUFFS = [(0.4, 0.7, 1.6), (2.3, 1.2, 1.55), (-1.4, 0.1, 1.2), (3.8, 0.3, 1.1)]
CB = -1.25                                          # (his flat underside)


def _cloud_face(expr):
    """Nimbus: two round black eyes and his ":3" (texels round his middle; his big puff's middle is at j 2; the mouth drawn
    round j 0, then set 3 texels down with the eyes)"""
    D = -3
    F = Face(); B = INK
    eyes = ((-5, 1), (4, 1))                         # (each eye's lower-left: 2.94f lower on him, not at the top of his head)
    if expr is None:
        for x, y in eyes:
            F.rect(x, y, x + 1, y + 3, B); F.put(x, y + 3, hexc('#6a6a72'))
    elif expr in ('happy', 'sing'):
        for x, y in eyes:
            F.pts([(x - 1, y + 1), (x, y + 2), (x + 1, y + 2), (x + 2, y + 1)], B)
    elif expr == 'blink':
        for x, y in eyes:
            F.pts([(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)], B)
    elif expr == 'surprised':
        for x, y in eyes:
            F.rect(x - 1, y, x + 2, y + 4, B); F.rect(x, y + 1, x + 1, y + 3, WHITE); F.put(x + 1, y + 2, B)
    elif expr == 'hurt':
        for (x, y), s_ in zip(eyes, (1, -1)):
            F.pts([(x - 1 if s_ > 0 else x + 2, y + 3), (x, y + 2) if s_ > 0 else (x + 1, y + 2), (x + 1, y + 1) if s_ > 0 else (x, y + 1),
                   (x, y) if s_ > 0 else (x + 1, y), (x - 1 if s_ > 0 else x + 2, y - 1)], B)
    elif expr == 'angry':
        for (x, y), s_ in zip(eyes, (1, -1)):
            F.rect(x, y, x + 1, y + 2, B)
            F.pts([(x - 1, y + 4), (x, y + 3), (x + 1, y + 3)] if s_ > 0 else [(x + 2, y + 4), (x + 1, y + 3), (x, y + 3)], B)
    # the mouth
    E_, F = F, Face()
    if expr == 'surprised':
        F.rect(-1, -2, 1, 1, B); F.rect(0, -1, 0, 0, hexc('#6a6a72'))
    elif expr == 'sing':
        F.rect(-1, -2, 1, 1, B); F.rect(0, -1, 0, 0, hexc('#b04858'))
    elif expr == 'hurt':
        F.pts([(-4, -1), (-3, 0), (-2, -1), (-1, 0), (0, -1), (1, 0), (2, -1), (3, 0), (4, -1)], B)
    elif expr == 'angry':
        F.pts([(-3, -1), (-2, 0), (-1, 1), (0, 1), (1, 1), (2, 0), (3, -1)], B)
    else:                                            # (":3")
        F.pts([(-4, 1), (-4, 0), (-3, -1), (-2, -1), (-1, 0), (0, 1), (1, 0), (2, -1), (3, -1), (4, 0), (4, 1)], B)
    for (x, y), c in F.px.items():
        E_.put(x, y + D, c)
    return E_


def _cloud(puffs, pal, F=None, seed=61, depth=0.62, flat=None):
    def paint(side, X, Y, Z, b):
        i, j = math.floor(X * RES), math.floor(Y * RES)
        n = noise(i, j, seed) - 0.5
        if side == 'bottom':
            return shade(pal['under'], 1.0 + 0.04 * n)
        if side == 'top':
            return shade(pal['hi'], 1.0 + 0.03 * n)
        if side == 'front' and F is not None:
            f = F.at(X, Y)
            if f:
                return f
        t = min(1.0, max(0.0, (Y - CB) / 3.2))
        c = mix(pal['lo'], pal['base'], t ** 0.7)
        c = mix(c, pal['hi'], max(0.0, 1.0 - math.hypot(X + 0.6, Y - 1.4) / 2.2) * 0.6)
        if side in ('left', 'right'):
            c = shade(c, 0.94)
        if side == 'back':
            c = shade(c, 0.9)
        return shade(c, 1.0 + 0.04 * n)
    P = Part(paint)
    # one surface, not puffs laid over each other (their faces would share planes and flicker): each row (a texel high, from
    # his flat underside up) cut into texel cells, each as deep as the deepest puff there (a puff's row: one flat front, as deep as it is wide) - the
    # flat base the puffs sit on among them - and each row's runs of one depth made a box
    xs = [cx - r for cx, cy, r in puffs] + [cx + r for cx, cy, r in puffs]
    lo, hi = math.floor(min(xs) * 4) / 4, math.ceil(max(xs) * 4) / 4
    base = (min(xs) + 0.5, max(xs) - 0.5)
    st, cw = 0.5, 0.25                                                  # (rows half a unit, cells a texel)
    rows = []
    y = CB
    while y < max(cy + r for cx, cy, r in puffs):
        ym = y + st / 2
        cells = []
        x = lo
        while x < hi:
            xm = x + cw / 2; d = 0.0
            for cx, cy, r in puffs:
                if abs(ym - cy) < r:
                    hw = math.sqrt(r * r - (ym - cy) ** 2)
                    if abs(xm - cx) < hw:
                        d = max(d, snap(hw * depth))
            if ym < CB + 1.0 and base[0] <= xm <= base[1]:
                d = max(d, 1.0)
            cells.append([x, d]); x += cw
        rows.append((y, cells))
        y += st
    if flat:                                                            # (his face: one flat panel, eyes and smile on the same plane)
        fx0, fx1, fy0, fy1 = flat
        zone = [c for y, cells in rows if y < fy1 and y + st > fy0 for c in cells if c[1] > 0 and fx0 <= c[0] + cw / 2 <= fx1]
        fd = max(c[1] for c in zone)
        for c in zone:
            c[1] = fd
    for y, cells in rows:
        k = 0
        while k < len(cells):
            x0, d = cells[k]; k2 = k
            while k2 + 1 < len(cells) and cells[k2 + 1][1] == d:
                k2 += 1
            if d > 0:
                P.box((x0, y, -d), (cells[k2][0] + cw, y + st, d))
            k = k2 + 1
    return P


def nimbus(expr=None):
    return _cloud(PUFFS, CLOUD, _cloud_face(expr), flat=(-1.75, 2.0, -1.0, 1.25))      # (the panel round his eyes and smile)


def back():
    return _cloud(BACK_PUFFS, BACK, None, seed=71, depth=0.55)


BUILD = {'head': sunny, 'rays': rays, 'moon': snooze, 'cap': cap, 'star': twinkle, 'body': nimbus, 'back': back}
