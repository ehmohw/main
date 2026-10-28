"""The Doodle Dragon (draft): the first Buddy ever made by another Buddy. Kettle - the very first Buddy, the cheerful stick figure -
sat down one day with a box of crayons and drew himself a friend: a chubby little dragon. The Gem of Creativity did the rest, and the
drawing climbed off the page. He's a child's drawing and he acts like one: proud of himself (he breathes FIRE, you know - crayon fire,
a scribble of red and orange and yellow), a little clumsy on his stubby legs, and utterly devoted to Kettle, who made him.

THE LOOK - flat and drawn, like Kettle and Mr. Capshun, but in waxy crayon instead of ink: a paper cut-out of a kid's drawing, seen
front-on. A chubby pear of a green body with a big yellow belly (orange stripes across it), a round green head with three purple spikes
on top and two little cream horns, big black dot eyes (a shine in each) and a toothy grin, pink cheeks. Stubby green legs with white
toenails, short arms with little white claws, two small purple bat wings behind his shoulders, a fat curly tail out to his left with
purple spikes along the top. Every shape is coloured the way a kid colours: a thick wobbly crayon outline in a darker shade, scribbled
fill strokes you can see (paper peeking through between them, a waxy grain) - and here and there the scribble runs outside the lines.
From behind: the same cut-out, plain green, a row of purple spikes down his back. Side-on he all but vanishes, like Kettle.

He is about Kettle's height or a little shorter (1.5 blocks at Kettle's RIG_SCALE 0.78) and stands on his two stubby back legs.

THE RIG (rigkit): every part is a flat card - a crayon picture on a paper-thin plane, a front face and a back face. The cards are
layered like a paper puppet, front to back: arms (z -1.0), head (-0.5), body (0), legs (+1.1), tail (+1.5), wings (+1.9) - far enough
apart that what a pose swings out of the page can't cut through the card behind it; most moves are in the page, as a drawing moves.
Parts: body (the root, at his middle), head (a model per expression), arms, legs, wings, tail - and three effects, shown only when a
pose asks: fire, slash (_slash: three claw marks off his right hand), boom (_boom: a crayon impact under his right foot).

CRAYON FIRE - his pride and joy, and the owner's highlight. The 'fire' part (child of the head, at his mouth; hidden unless a pose
sets _fire) is drawn the way a child draws fire: waxy crayon, red round orange round a yellow heart, each colour scribbled in with
zig-zag strokes that run outside the lines, tongues licking off the edges. _fire='fire' (breathe): a big flame, 1.3 blocks long, as a
cross of two flame cards along his breath (one standing up, seen from the side; one lying flat, seen from above) with a starburst of
fire round his mouth (seen from in front). _fire='kindle' (breathe_up, the wind-up): smoke huffed out of his nose either side and
little flames licking out of his mouth. _fire='puff' (idle_c): just the smoke, a hiccup. The part is built full size and shrunk
into its model box (PART_K 2). For the datapack's own breath effect later: dd_fx_fire (a small crayon flame, standing up) and
dd_fx_smoke (a scribble of crayon smoke) - textures, each also a little flat card model of its own.
Design units: feet at y=0, facing -z, his right is +x."""
import math
import random
import sys
import zlib

from PIL import Image, ImageDraw, ImageChops

from phase57_art import hexc
from rigkit import qs, el, solve, qrot, D, shrink

PREFIX = 'dd_'
RIG_SCALE = 0.78                                   # (Kettle's own scale: a crayon line the same weight as his ink)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

# ---------------------------------------------------------------------------------------------------- the cards
ZA, ZH, ZB, ZL, ZT, ZW = -1.0, -0.5, 0.0, 1.1, 1.5, 1.9         # (the layers, front to back)
DZ = 0.05                                                       # (a card's front and back faces: its paper thickness)
MOUTH = (0.0, 19.4)
PIVOT = {'body': (0.0, 6.0, ZB), 'head': (0.0, 16.6, ZH),
         'armr': (5.0, 13.0, ZA), 'arml': (-5.0, 13.0, ZA),
         'legr': (3.05, 6.0, ZL), 'legl': (-3.05, 6.0, ZL),
         'wingr': (4.9, 14.4, ZW), 'wingl': (-4.9, 14.4, ZW),
         'tail': (-5.2, 8.6, ZT),
         'fire': (MOUTH[0], MOUTH[1], ZH), 'slash': (5.0, 13.0, ZA), 'boom': (3.05, 6.0, ZL)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'legr': 'body', 'legl': 'body',
          'wingr': 'body', 'wingl': 'body', 'tail': 'body', 'fire': 'head', 'slash': 'armr', 'boom': 'legr'}
PARTS = tuple(PIVOT)
PART_K = {'fire': 2.0}                         # (the breath is big: built full size, shrunk into its model, shown twice the scale)
FX = ('fire', 'slash', 'boom')
FIRES = ('fire', 'kindle', 'puff')
FACES = ('happy', 'surprised', 'blink', 'fierce', 'sad', 'puff', 'roar', 'dizzy')
# each card: (box x0, y0, size - a square in design units, on the page), its layer, (front texture, back texture); left parts mirror right
BOX = {'body': ((-8.0, 3.0, 16.0), ZB), 'head': ((-8.0, 16.0, 16.0), ZH), 'armr': ((2.5, 7.0, 8.0), ZA),
       'legr': ((-0.5, -0.5, 8.0), ZL), 'wingr': ((3.0, 9.0, 16.0), ZW), 'tail': ((-17.0, 2.0, 16.0), ZT)}
MIRROR = {'arml': 'armr', 'legl': 'legr', 'wingl': 'wingr'}


def HIDDEN(p, pose):
    if p == 'fire':
        return not pose.get('_fire')
    if p in ('slash', 'boom'):
        return not pose.get('_' + p)
    return False


def model_name(p, pose, suffix=''):
    if p == 'fire':
        return f'{PREFIX}fire_{pose.get("_fire") or "fire"}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- crayons
PAPER = '#fffcf0'
BLACK = '#26222c'
GREEN, GREEN_L = '#5ec43c', '#2b7d22'
BELLY, BELLY_L = '#ffd843', '#f2911a'
PURP, PURP_L = '#9b55dc', '#56289a'
WING, WING_L = '#c79df4', '#6a35b0'
HORN, HORN_L = '#ffe27a', '#d4862c'
CLAW, CLAW_L = '#ffffff', '#6f7080'
CHEEK = '#ff8db4'
MOUTH_C, TONGUE = '#7c1f30', '#ff6f8f'
RED, ORANGE, YELLOW = '#ff3d2e', '#ff8f1f', '#ffe14a'
SMOKE, SMOKE_L = '#c4c8ce', '#7d828c'
SS, DENS = 4, 8                                    # (drawn 4x over, brought down to 8 pixels a design unit - Kettle's own)
OW = 0.46                                          # (the crayon outline: thick)


def _mix(a, b, t):
    a, b = hexc(a), hexc(b)
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def _resample(pts, step, closed):
    seq = list(pts) + ([pts[0]] if closed else [])
    out = []
    for a, b in zip(seq, seq[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        out += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n)]
    if not closed:
        out.append(seq[-1])
    return out


def _area(pts):
    return sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts))) / 2


def _normals(pts, closed):
    n, out = len(pts), []
    sgn = (1 if _area(pts) < 0 else -1) if closed else 1
    for i in range(n):
        a = pts[i - 1] if (closed or i > 0) else pts[i]
        b = pts[(i + 1) % n] if (closed or i < n - 1) else pts[i]
        tx, ty = b[0] - a[0], b[1] - a[1]; L = math.hypot(tx, ty) or 1
        out.append((sgn * ty / L, -sgn * tx / L))            # (closed: pointing out of the shape)
    return out


def _noise(n, seed, ks=(2, 3, 5), amp=1.0):
    r = random.Random(seed)
    waves = [(r.uniform(0.6, 1.0) / k ** 0.5, k, r.uniform(0, 2 * math.pi)) for k in ks]
    tot = sum(a for a, _k, _p in waves)
    return [amp * sum(a * math.sin(2 * math.pi * k * i / n + p) for a, k, p in waves) / tot for i in range(n)]


def wob(pts, amp, seed, closed=True, step=0.2, ks=(2, 3, 5)):
    """a hand-drawn version of a shape: resampled, and pushed in and out along its normals by a slow wobble"""
    pts = _resample(pts, step, closed)
    nz, nm = _noise(len(pts), seed, ks, amp), _normals(pts, closed)
    return [(p[0] + n[0] * z, p[1] + n[1] * z) for p, n, z in zip(pts, nm, nz)]


def grow(pts, d):
    """a closed shape pushed out by d (a number, or one per point)"""
    nm = _normals(pts, True); d = d if isinstance(d, list) else [d] * len(pts)
    return [(p[0] + n[0] * k, p[1] + n[1] * k) for p, n, k in zip(pts, nm, d)]


def ell(cx, cy, rx, ry, n=56, a0=0.0):
    return [(cx + rx * math.cos(a0 + 2 * math.pi * i / n), cy + ry * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


def capsule(a, b, r, n=14):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    th = math.atan2(uy, ux); out = []
    for i in range(n + 1):
        t = th - math.pi / 2 + math.pi * i / n
        out.append((b[0] + r * math.cos(t), b[1] + r * math.sin(t)))
    for i in range(n + 1):
        t = th + math.pi / 2 + math.pi * i / n
        out.append((a[0] + r * math.cos(t), a[1] + r * math.sin(t)))
    return out


def spline(pts, per=10):
    """Catmull-Rom through the points"""
    P = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(per):
            t = k / per; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    out.append(pts[-1])
    return out


def tube(center, w0, w1, cap=True):
    """a tapering tube along a line: widths w0 -> w1; rounded ends"""
    n = len(center); nm = _normals(center, False)
    ws = [(w0 + (w1 - w0) * i / (n - 1)) / 2 for i in range(n)]
    left = [(p[0] + m[0] * w, p[1] + m[1] * w) for p, m, w in zip(center, nm, ws)]
    right = [(p[0] - m[0] * w, p[1] - m[1] * w) for p, m, w in zip(center, nm, ws)]
    def arc(c, a, b, k=7):
        a0, a1 = math.atan2(a[1] - c[1], a[0] - c[0]), math.atan2(b[1] - c[1], b[0] - c[0]); r = math.hypot(a[0] - c[0], a[1] - c[1])
        if a1 > a0: a1 -= 2 * math.pi
        return [(c[0] + r * math.cos(a0 + (a1 - a0) * i / k), c[1] + r * math.sin(a0 + (a1 - a0) * i / k)) for i in range(1, k)]
    return left + (arc(center[-1], left[-1], right[-1]) if cap else []) + right[::-1] + (arc(center[0], right[0], left[0]) if cap else [])


def tri(c, ang, w, h, lean=0.0):
    """a spike: its base centred on c, pointing at angle ang (degrees), w wide, h tall"""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    tip = (c[0] + ux * h + nx * lean, c[1] + uy * h + ny * lean)
    return [(c[0] + nx * w / 2, c[1] + ny * w / 2), tip, (c[0] - nx * w / 2, c[1] - ny * w / 2), (c[0] - ux * 0.6, c[1] - uy * 0.6)]


def bez(a, c, b, n=10):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0], (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1])
            for t in (i / n for i in range(n))]


class Pic:
    """a crayon picture of one card: a square box on the page (design units), drawn SS x over. Its left edge is the card's +x
    side (his right) - as a north face shows it."""
    DRY = False                                    # (dry: nothing drawn - only each shape's outer edge noted, for the floor)

    def __init__(self, box):
        self.x0, self.y0, self.sz = box; self.edges = []
        self.N = int(round(self.sz * DENS)); self.S = self.N * SS; self.k = self.S / self.sz
        self.im = Image.new('RGBA', (self.S, self.S), (0, 0, 0, 0))

    def P(self, p):
        return ((self.x0 + self.sz - p[0]) * self.k, (self.y0 + self.sz - p[1]) * self.k)

    def Ps(self, pts):
        return [self.P(p) for p in pts]

    def mask(self, pts):
        m = Image.new('L', (self.S, self.S), 0); ImageDraw.Draw(m).polygon(self.Ps(pts), fill=255); return m

    def put(self, lay, m=None):
        if m is not None:
            lay.putalpha(ImageChops.multiply(lay.getchannel('A'), m))
        self.im.alpha_composite(lay)

    def layer(self):
        return Image.new('RGBA', (self.S, self.S), (0, 0, 0, 0))

    def crayon(self, pts, col, w, seed, closed=True, passes=2, jit=0.06):
        """a waxy crayon line: gone over twice, never quite on the same track"""
        if Pic.DRY: return None
        lay = self.layer(); d = ImageDraw.Draw(lay)
        for k in range(passes):
            p = wob(pts, jit * (1 + k), seed + 101 * k, closed, step=0.12, ks=(3, 7, 13))
            if closed: p = p + p[:2]
            c = hexc(col) if k == 0 else _mix(col, BLACK, 0.12)
            ww = w * (1.0 if k == 0 else 0.62) * self.k
            pp = self.Ps(p)
            d.line(pp, fill=c, width=max(1, int(ww)), joint='curve')
            if not closed:
                for x, y in (pp[0], pp[-1]):
                    d.ellipse((x - ww / 2, y - ww / 2, x + ww / 2, y + ww / 2), fill=c)
        self.put(lay)

    def scribble(self, region, col, ang, seed, sp=0.82, w=0.24):
        """back-and-forth crayon strokes over a region (a shape), clipped to it"""
        r = random.Random(seed); a = math.radians(ang); U, V = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
        us = [p[0] * U[0] + p[1] * U[1] for p in region]; vs = [p[0] * V[0] + p[1] * V[1] for p in region]
        u0, u1, v0, v1 = min(us) - 0.6, max(us) + 0.6, min(vs) - sp, max(vs) + sp
        pts, v, i = [], v0, 0
        while v < v1:                              # (a hand going back and forth: never quite even, never quite straight)
            uu = (u0 + r.uniform(-0.4, 0.4)) if i % 2 == 0 else (u1 + r.uniform(-0.4, 0.4))
            vv = v + r.uniform(-0.35, 0.35) * sp
            pts.append((uu * U[0] + vv * V[0], uu * U[1] + vv * V[1]))
            v += sp / 2 * r.uniform(0.6, 1.45); i += 1
        lay = self.layer(); d = ImageDraw.Draw(lay)
        for j in range(len(pts) - 1):
            ww = w * r.uniform(0.75, 1.3)
            d.line(self.Ps(pts[j:j + 2]), fill=_mix(col, BLACK, r.uniform(0.0, 0.1)), width=max(1, int(ww * self.k)))
        self.put(lay, self.mask(region))

    def blob(self, poly, col, line, seed, ang=35.0, over=0.5, light=0.42, amp=0.16, ow=OW, scrib=True):
        """a shape coloured in: pale crayon all over, scribbled strokes on top (running outside the lines here and there), a
        thick wobbly outline round it. -> the shape as drawn"""
        shape = wob(poly, amp, seed)
        if Pic.DRY:
            nz = _noise(len(shape), seed + 7, (3, 5, 8))
            self.edges.append(grow(shape, [ow / 2 + 0.05 + (over * max(0.0, z * 1.6 - 0.25) if scrib else 0.0) for z in nz]))
            return shape
        lay = self.layer(); ImageDraw.Draw(lay).polygon(self.Ps(shape), fill=_mix(col, PAPER, light)); self.put(lay)
        if scrib:
            nz = _noise(len(shape), seed + 7, (3, 5, 8))
            region = grow(shape, [ow / 2 + over * max(0.0, z * 1.6 - 0.25) for z in nz]) if over else shape
            self.scribble(region, col, ang, seed + 3)
        self.crayon(shape, line, ow, seed + 5)
        return shape

    def dot(self, c, rx, ry, col, seed, line=None, ow=0.3):
        if Pic.DRY: return None
        shape = wob(ell(c[0], c[1], rx, ry, 28), min(rx, ry) * 0.06, seed, step=0.08)
        lay = self.layer(); ImageDraw.Draw(lay).polygon(self.Ps(shape), fill=hexc(col)); self.put(lay)
        if line: self.crayon(shape, line, ow, seed + 1, passes=1, jit=0.03)
        return shape

    def fill(self, poly, col, seed, line=None, ow=0.3):
        if Pic.DRY: return None
        shape = wob(poly, 0.05, seed, step=0.1)
        lay = self.layer(); ImageDraw.Draw(lay).polygon(self.Ps(shape), fill=hexc(col)); self.put(lay)
        if line: self.crayon(shape, line, ow, seed + 1, passes=1, jit=0.03)
        return shape

    def done(self, seed, alpha=None):
        """brought down to size (box filtered, the alpha kept hard), then the wax: specks of paper and a little grain"""
        S, N = self.S, self.N
        import numpy as np
        a = np.asarray(self.im).astype(np.float32) / 255.0
        a[..., :3] *= a[..., 3:4]
        a = a.reshape(N, SS, N, SS, 4).mean(axis=(1, 3))
        al = a[..., 3]
        rgb = np.where(al[..., None] > 1e-6, a[..., :3] / np.maximum(al[..., None], 1e-6), 0)
        keep = al >= 0.5 if alpha is None else alpha
        rng = np.random.default_rng(seed)
        n = rng.random((N, N))
        paper = np.array(hexc(PAPER)[:3]) / 255.0
        rgb = np.where((n < 0.11)[..., None], rgb * 0.55 + paper * 0.45, rgb)
        rgb = np.where(((n >= 0.11) & (n < 0.15))[..., None], rgb * 0.88, rgb)
        rgb = rgb * (1 + (rng.random((N, N, 1)) - 0.5) * 0.06)
        out = np.zeros((N, N, 4), np.uint8)
        out[..., :3] = np.clip(rgb * 255, 0, 255).astype(np.uint8); out[..., 3] = np.where(keep, 255, 0)
        return Image.fromarray(out, 'RGBA'), keep


# ---------------------------------------------------------------------------------------------------- the shapes
def _g_body():
    pear = [(6.4 * math.cos(t) * (1 - 0.1 * math.sin(t)), 10.9 + 7.2 * math.sin(t)) for t in (2 * math.pi * i / 64 for i in range(64))]
    return pear


def _g_head():
    c, r = (0.0, 22.6), 5.9
    on = lambda a, rr=r: (c[0] + rr * math.cos(math.radians(a)), c[1] + rr * math.sin(math.radians(a)))
    spikes = [tri(on(a, r - 0.2), a, 2.2, h) for a, h in ((90 + 27, 2.0), (90, 2.5), (90 - 27, 2.0))]
    horns = [tri(on(a, r - 0.3), a + s * 12, 1.8, 2.4, lean=s * 0.5) for a, s in ((90 + 56, 1), (90 - 56, -1))]
    return ell(c[0], c[1], r, r, 60, 0.3), spikes, horns


def _g_arm():
    A, B = (5.0, 13.0), (7.5, 9.4)
    dx, dy = B[0] - A[0], B[1] - A[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    claws = [tri((B[0] + ux * 0.75 + nx * o, B[1] + uy * 0.75 + ny * o), math.degrees(math.atan2(uy, ux)) + o * 22, 0.85, 1.35) for o in (-0.78, 0.0, 0.78)]
    return capsule(A, B, 1.15), claws


def _g_leg():
    return capsule((3.05, 5.6), (3.05, 2.3), 1.6), ell(3.3, 1.15, 2.35, 1.1, 40)


def _g_wing():
    R1, T, E1, E2, E3, R2 = (4.4, 16.4), (12.6, 23.0), (14.4, 15.4), (11.2, 13.4), (8.0, 12.8), (4.6, 12.2)
    pts = bez(R1, (7.0, 21.4), T) + bez(T, (14.6, 19.6), E1) + bez(E1, (12.4, 15.4), E2) + bez(E2, (9.4, 14.2), E3) + bez(E3, (6.2, 13.6), R2)
    bones = [((5.2, 14.4), p) for p in (T, E1, E2, E3)]
    return pts, bones


TAIL_C = [(-4.4, 9.2), (-6.8, 8.6), (-9.0, 7.8), (-11.0, 7.6), (-12.7, 8.4), (-13.6, 10.0), (-13.2, 11.6), (-11.9, 12.2), (-10.8, 11.6),
          (-10.6, 10.5), (-11.3, 10.0)]


def _g_tail():
    c = spline(TAIL_C, 8)
    body = tube(c, 3.6, 0.9)
    nm = _normals(c, False); n = len(c)
    spikes = []
    for t, h in ((0.12, 1.5), (0.24, 1.7), (0.36, 1.5)):
        i = int(t * n); p, m = c[i], nm[i]
        w = (3.6 + (0.9 - 3.6) * i / (n - 1)) / 2
        spikes.append(tri((p[0] + m[0] * (w - 0.25), p[1] + m[1] * (w - 0.25)), math.degrees(math.atan2(m[1], m[0])), 1.5, h, lean=-0.3))
    return body, spikes


GEO = {}


# ---------------------------------------------------------------------------------------------------- the pictures
def _p_body(back=False):
    pic = Pic(BOX['body'][0])
    s = pic.blob(_g_body(), GREEN, GREEN_L, 11, ang=32)
    if not back:
        b = pic.blob(ell(0.0, 10.2, 4.0, 5.5, 48), BELLY, BELLY_L, 12, ang=-24, over=0.4)
        for i, y in enumerate((6.6, 8.8, 11.0, 13.2)):
            hw = 4.0 * math.sqrt(max(0.0, 1 - ((y - 10.2) / 5.5) ** 2)) - 0.55
            pic.crayon(bez((-hw, y + 0.25), (0.0, y - 0.45), (hw, y + 0.25), 12) + [(hw, y + 0.25)], BELLY_L, 0.3, 40 + i, closed=False, passes=1)
    else:
        for i, y in enumerate((8.6, 11.2, 13.8, 16.2)):
            pic.blob(tri((0.0, y - 0.6), 90, 1.8, 1.7), PURP, PURP_L, 60 + i, ang=50, over=0.15, ow=0.3, amp=0.06)
    return pic, [s]


def _p_head(face=None, back=False):
    pic = Pic(BOX['head'][0])
    disc, spikes, horns = _g_head()
    out = []
    for i, sp in enumerate(spikes):
        out.append(pic.blob(sp, PURP, PURP_L, 20 + i, ang=60, over=0.2, amp=0.08, ow=0.38))
    for i, h in enumerate(horns):
        out.append(pic.blob(h, HORN, HORN_L, 24 + i, ang=-30, over=0.15, amp=0.06, ow=0.34))
    out.append(pic.blob(disc, GREEN, GREEN_L, 27, ang=38, over=0.45))
    if not back:
        _face(pic, face)
    return pic, out


def _face(pic, kind):
    """his face, on the head card: big black dot eyes with a shine, a toothy grin, pink cheeks - each expression redraws them"""
    K = BLACK; ex, ey = 2.3, 23.9
    def dots(rx=1.05, ry=1.38, dy=0.0):
        for i, s in enumerate((1, -1)):
            pic.dot((s * ex, ey + dy), rx, ry, K, 300 + i)
            pic.dot((s * ex - 0.32, ey + dy + 0.45), 0.36, 0.36, '#ffffff', 310 + i)
    def cheeks(r=0.95, y=20.9, x=4.1):
        for i, s in enumerate((1, -1)):
            pic.dot((s * x, y), r, r * 0.8, CHEEK, 320 + i)
    def nostrils():
        for i, s in enumerate((1, -1)):
            pic.dot((s * 0.75, 21.9), 0.24, 0.2, K, 330 + i)
    def arcs(y, h, up=True, w=0.36):                                    # (closed eyes: ^ ^ (up) or u u)
        for i, s in enumerate((1, -1)):
            x = s * ex
            pts = bez((x - 1.1, y), (x, y + (h if up else -h) * 2), (x + 1.1, y), 10) + [(x + 1.1, y)]
            pic.crayon(pts, K, w, 340 + i, closed=False, passes=1, jit=0.03)
    def brows(tilt, y=26.0, w=0.38):                                     # (tilt > 0: angry, in towards the middle; < 0: worried)
        for i, s in enumerate((1, -1)):
            x = s * ex
            pic.crayon([(x + s * 1.2, y + tilt * 0.5), (x - s * 1.0, y - tilt * 0.5)], K, w, 350 + i, closed=False, passes=1, jit=0.02)
    def grin(w=3.5, top=20.5, depth=2.6, teeth=5, tongue=True):
        low = [(w * math.cos(t), top - depth * math.sin(t)) for t in (math.pi * i / 20 for i in range(21))]
        pic.fill(low, MOUTH_C, 360, line=K, ow=0.32)
        if tongue:
            pic.dot((0.4, top - depth + 0.75), w * 0.38, 0.62, TONGUE, 361)
        tw = 2 * w * 0.86 / teeth
        for i in range(teeth):
            x = -w * 0.86 + tw * (i + 0.5)
            pic.fill([(x - tw * 0.42, top - 0.05), (x + tw * 0.42, top - 0.05), (x, top - 0.95)], '#ffffff', 370 + i, line=K, ow=0.14)
        pic.crayon([(-w, top), (w, top)], K, 0.32, 380, closed=False, passes=1, jit=0.02)
    if kind is None:
        dots(); cheeks(); nostrils(); grin()
    elif kind == 'happy':
        arcs(24.0, 0.7); cheeks(1.15); nostrils(); grin(3.8, 20.6, 3.0)
    elif kind == 'surprised':
        for i, s in enumerate((1, -1)):
            pic.dot((s * ex, ey + 0.2), 1.45, 1.7, '#ffffff', 390 + i, line=K)
            pic.dot((s * ex, ey + 0.1), 0.55, 0.62, K, 392 + i)
        nostrils(); cheeks(0.8)
        pic.dot((0.0, 19.3), 1.25, 1.5, MOUTH_C, 394, line=K)
    elif kind == 'blink':
        arcs(23.7, 0.45, up=False); cheeks(); nostrils(); grin(3.0, 20.5, 1.9, 4, tongue=False)
    elif kind == 'fierce':
        dots(1.0, 1.15, -0.25); brows(1.3, 25.7); nostrils()
        bx, top, bot = 3.3, 20.6, 18.6                                  # (a snarl: teeth clenched in a box)
        pic.fill([(-bx, top), (bx, top), (bx * 0.92, bot), (-bx * 0.92, bot)], '#ffffff', 400, line=K, ow=0.32)
        pic.crayon([(-bx * 0.96, (top + bot) / 2), (bx * 0.96, (top + bot) / 2)], K, 0.22, 401, closed=False, passes=1, jit=0.02)
        for i in range(5):
            x = -bx + 2 * bx * (i + 1) / 6
            pic.crayon([(x, top - 0.1), (x, bot + 0.1)], K, 0.16, 402 + i, closed=False, passes=1, jit=0.01)
    elif kind == 'sad':
        dots(1.0, 1.3, -0.2); brows(-1.0, 26.0); nostrils(); cheeks(0.8)
        pic.crayon(bez((-2.4, 18.6), (0.0, 20.6), (2.4, 18.6), 12) + [(2.4, 18.6)], K, 0.36, 410, closed=False, passes=1, jit=0.04)
        pic.fill([(-2.3, 22.0), (-2.75, 21.0), (-2.3, 20.5), (-1.85, 21.0)], '#5ab4ff', 411, line='#2a6fc0', ow=0.16)
    elif kind == 'puff':                                                  # (cheeks puffed full of smoke, eyes squeezed shut, lips tight)
        for i, s in enumerate((1, -1)):
            x = s * ex
            pic.crayon([(x + s * 1.0, ey + 0.8), (x - s * 0.9, ey), (x + s * 1.0, ey - 0.8)], K, 0.36, 420 + i, closed=False, passes=1, jit=0.02)
        cheeks(1.6, 20.6, 3.9); nostrils()
        pic.dot((0.0, 19.6), 0.95, 0.7, MOUTH_C, 424, line=K, ow=0.28)
    elif kind == 'roar':                                                  # (mouth wide open - the fire comes out of here)
        dots(1.0, 1.2, 0.3); brows(1.0, 26.2); nostrils()
        mouth = ell(0.0, 19.4, 3.1, 2.25, 32)
        pic.fill(mouth, MOUTH_C, 430, line=K, ow=0.34)
        for i in range(4):
            x = -2.0 + 4.0 * i / 3
            yt = 19.4 + 2.25 * math.sqrt(max(0.0, 1 - (x / 3.1) ** 2))
            pic.fill([(x - 0.42, yt - 0.15), (x + 0.42, yt - 0.15), (x, yt - 0.95)], '#ffffff', 431 + i, line=K, ow=0.12)
        for i in range(3):
            x = -1.4 + 1.4 * i
            yb = 19.4 - 2.25 * math.sqrt(max(0.0, 1 - (x / 3.1) ** 2))
            pic.fill([(x - 0.42, yb + 0.15), (x + 0.42, yb + 0.15), (x, yb + 0.9)], '#ffffff', 436 + i, line=K, ow=0.12)
    elif kind == 'dizzy':                                                 # (fainted: swirly eyes, tongue out)
        for i, s in enumerate((1, -1)):
            c = (s * ex, ey); pts = [(c[0] + 0.08 * t * math.cos(t * s), c[1] + 0.08 * t * math.sin(t * s)) for t in (j * 0.35 for j in range(40))]
            pic.crayon(pts, K, 0.3, 440 + i, closed=False, passes=1, jit=0.01)
        nostrils(); cheeks(0.8)
        pic.crayon(bez((-2.6, 19.6), (0.0, 18.4), (2.6, 19.6), 12) + [(2.6, 19.6)], K, 0.36, 444, closed=False, passes=1, jit=0.03)
        pic.fill(capsule((0.9, 19.0), (1.1, 17.9), 0.6), TONGUE, 445, line=K, ow=0.2)
    return pic


def _p_arm():
    pic = Pic(BOX['armr'][0])
    body, claws = _g_arm()
    out = [pic.blob(c, CLAW, CLAW_L, 70 + i, scrib=False, amp=0.04, ow=0.26) for i, c in enumerate(claws)]
    out.append(pic.blob(body, GREEN, GREEN_L, 74, ang=-50, over=0.35, amp=0.1))
    return pic, out


def _p_leg():
    pic = Pic(BOX['legr'][0])
    leg, foot = _g_leg()
    out = [pic.blob(leg, GREEN, GREEN_L, 80, ang=70, over=0.35, amp=0.1)]
    out.append(pic.blob(foot, GREEN, GREEN_L, 81, ang=20, over=0.0, amp=0.07))      # (no scribble past the sole: he stands on it)
    for i, x in enumerate((2.1, 3.3, 4.5)):
        pic.dot((x, 0.75 if i != 1 else 0.68), 0.46, 0.4, CLAW, 82 + i, line=CLAW_L, ow=0.16)
    return pic, out


def _p_wing():
    pic = Pic(BOX['wingr'][0])
    pts, bones = _g_wing()
    out = [pic.blob(pts, WING, WING_L, 90, ang=58, over=0.45, amp=0.12)]
    for i, (a, b) in enumerate(bones):
        pic.crayon(bez(a, ((a[0] + b[0]) / 2 + 0.3, (a[1] + b[1]) / 2 + 0.4), b, 10) + [b], WING_L, 0.3, 91 + i, closed=False, passes=1)
    return pic, out


def _p_tail():
    pic = Pic(BOX['tail'][0])
    body, spikes = _g_tail()
    out = [pic.blob(s, PURP, PURP_L, 100 + i, ang=60, over=0.15, amp=0.06, ow=0.34) for i, s in enumerate(spikes)]
    out.append(pic.blob(body, GREEN, GREEN_L, 104, ang=-35, over=0.4, amp=0.1))
    return pic, out




# the effects ----------------------------------------------------------------------------------------------------
FIRE_L, FIRE_W = 26.0, 5.6                         # (how far the breath reaches in front of his mouth - 1.3 blocks - and how fat it gets)


def _flame(pic, a0, L, w, seed, frame=lambda a, b: (-a, b)):
    """a scribbled flame from a0 out to L along its axis: three crayons, red round orange round yellow, tongues licking off it"""
    def shape(scale, start, s):
        top, bot = [], []
        for i in range(25):
            a = start + (L - start) * i / 24; t = (a - start) / (L - start)
            hw = w * scale * (0.18 + 0.82 * math.sin(min(1.0, t * 1.25) * math.pi / 2) ** 0.9) * (1 if t < 0.82 else max(0.15, 1 - (t - 0.82) / 0.2))
            lick = 0.09 * w * scale * math.sin(t * 9 + s) * t
            top.append(frame(a, hw + lick)); bot.append(frame(a, -hw + 0.6 * lick))
        return top + [frame(L + 0.6 * scale, 0.0)] + bot[::-1]
    k = L / FIRE_L
    pic.blob(shape(1.0, a0, seed), RED, '#c4161a', seed, ang=70, over=0.9 * k + 0.2, amp=0.25 * k + 0.05, light=0.3)
    pic.blob(shape(0.66, a0 + 2.0 * k, seed + 1), ORANGE, '#e0640f', seed + 1, ang=-60, over=0.6 * k + 0.15, amp=0.18 * k + 0.04, light=0.3, ow=0.4)
    pic.blob(shape(0.33, a0 + 4.5 * k, seed + 2), YELLOW, '#f0b21a', seed + 2, ang=80, over=0.4 * k + 0.1, amp=0.1 * k + 0.03, light=0.2, ow=0.32)


FIRE_BOX, BURST_BOX = (-32.0, -16.0, 32.0), (-8.0, -8.0, 16.0)


def _p_fire_side():
    pic = Pic(FIRE_BOX)                            # (a = -x on this picture: the mouth at its left edge, the flame running right)
    _flame(pic, 0.6, FIRE_L, FIRE_W, 500)
    return pic


def _burst(pic, c, r, seed, n=18):
    star = []
    for i in range(n):
        a = 2 * math.pi * i / n; rr = r * (1.0 if i % 2 == 0 else 0.6) * (1 + 0.12 * math.sin(i * 2.3))
        star.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    pic.blob(star, RED, '#c4161a', seed, ang=20, over=0.5, amp=0.15, light=0.3)
    pic.blob(ell(c[0], c[1], r * 0.52, r * 0.52, 24), ORANGE, '#e0640f', seed + 1, ang=-30, over=0.3, amp=0.12, light=0.3, ow=0.38)
    pic.blob(ell(c[0], c[1], r * 0.26, r * 0.26, 16), YELLOW, '#f0b21a', seed + 2, ang=50, over=0.15, amp=0.06, light=0.2, ow=0.28)


def _p_fire_burst():
    pic = Pic(BURST_BOX)
    _burst(pic, (0.0, 0.0), 5.2, 520)
    return pic


PUFF_BOX = (-16.0, 10.0, 32.0)
PUFFS = [((6.9, 22.6), 1.0), ((8.4, 24.9), 1.5), ((9.2, 28.2), 1.95)]


def _p_puff(kindle=False):
    """smoke huffed out of his nose, a puff either side - and (kindle) flames licking out of the corners of his mouth"""
    pic = Pic(PUFF_BOX)
    if kindle:
        for i, s in enumerate((1, -1)):
            _flame(pic, 0.1, 4.4, 1.35, 530 + 3 * i, frame=lambda a, b, s=s: (s * (0.7 + a * 0.82 + b * 0.57), 19.0 - a * 0.57 + b * 0.82))
    for s in (1, -1):
        for i, ((x, y), r) in enumerate(PUFFS):
            pic.blob(ell(s * x, y, r, r * 0.9, 24), SMOKE, SMOKE_L, 540 + i + (s > 0) * 10, ang=30, over=0.2, amp=0.12, ow=0.3)
            pic.crayon([(s * (x - r * 0.4), y + r * 0.1), (s * x, y + r * 0.45), (s * (x + r * 0.35), y + r * 0.05)], SMOKE_L, 0.2,
                       560 + i + (s > 0) * 10, closed=False, passes=1)
    return pic


SLASH_R = (6.2, 7.5, 8.8)
SLASH_BOX = (PIVOT['armr'][0] - 14.0, PIVOT['armr'][1] - 16.0, 32.0)


def _p_slash():
    """three claw marks, swept along the arc his hand comes down through (about his shoulder, behind and above the hand)"""
    A = PIVOT['armr']; pic = Pic(SLASH_BOX)
    for i, R in enumerate(SLASH_R):
        a0, a1 = -66 + 3 * i, 52 - 10 * i
        c = [(A[0] + R * math.cos(math.radians(a)), A[1] + R * math.sin(math.radians(a))) for a in (a0 + (a1 - a0) * k / 20 for k in range(21))]
        body = tube(c, 0.3, 1.25 + 0.1 * i)[::-1]
        pic.blob(body, '#fff4c2', RED, 600 + i, scrib=False, amp=0.04, ow=0.32)
    return pic


BOOM_BOX = (3.3 - 16.0, -2.0, 32.0)


def _p_boom():
    """crayon impact round his right foot as it slams down: sharp lines flying up and out, scribbled dust either side"""
    F = (3.3, 0.0); pic = Pic(BOOM_BOX)
    for i, a in enumerate((18, 42, 66, 90, 114, 138, 162)):
        r0, r1 = 3.4 + 0.5 * (i % 2), 6.6 + 1.4 * (i % 2)
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        c = [(F[0] + u[0] * (r0 + (r1 - r0) * k / 6), F[1] + 0.6 + u[1] * (r0 + (r1 - r0) * k / 6)) for k in range(7)]
        pic.blob(tube(c, 1.2, 0.25), YELLOW, ORANGE, 620 + i, scrib=False, amp=0.03, ow=0.34)
    for i, (x, y, r) in enumerate(((-1.1, 1.2, 1.25), (-3.0, 0.85, 0.85), (7.7, 1.2, 1.3), (9.6, 0.85, 0.8))):
        pic.blob(ell(x, y, r * 1.25, r, 24), '#d9c3a0', '#8c7454', 640 + i, ang=30, over=0.2, amp=0.1, ow=0.28)
    return pic


def _p_fx_fire():
    """(for the datapack: the breath's own particle, a small crayon flame standing up - a fat bottom, a point on top)"""
    pic = Pic((-4.0, 0.0, 8.0))
    _flame(pic, 0.5, 6.3, 2.5, 700, frame=lambda a, b: (b, 7.4 - a))
    return pic


def _p_fx_smoke():
    """(for the datapack: a scribble of crayon smoke)"""
    pic = Pic((-4.0, 0.0, 8.0))
    for i, (x, y, r) in enumerate(((-1.4, 2.6, 1.6), (1.3, 2.4, 1.75), (0.0, 4.6, 1.95), (1.6, 5.9, 1.05))):
        pic.blob(ell(x, y, r, r * 0.92, 28), SMOKE, SMOKE_L, 720 + i, ang=30 + 40 * i, over=0.35, amp=0.14, ow=0.34)
    pic.crayon(bez((-1.6, 4.6), (-0.2, 5.8), (1.0, 4.6), 10) + [(1.0, 4.6)], SMOKE_L, 0.24, 730, closed=False, passes=1)
    pic.crayon(bez((-2.4, 2.2), (-1.4, 3.2), (-0.4, 2.4), 10) + [(-0.4, 2.4)], SMOKE_L, 0.24, 731, closed=False, passes=1)
    return pic


# each card's outer edge, as drawn (the outline, and the scribble that runs past it) - the floor finds his lowest point on them
Pic.DRY = True
for _part, _fn in (('body', _p_body), ('head', _p_head), ('armr', _p_arm), ('legr', _p_leg), ('wingr', _p_wing), ('tail', _p_tail)):
    GEO[_part] = _fn()[0].edges
Pic.DRY = False


# ---------------------------------------------------------------------------------------------------- textures
_TEX = {}


def textures():
    if _TEX:
        return dict(_TEX)
    T = {}
    def two(name, fn):
        (pf, _), (pb, _) = fn(False), fn(True)
        f, keep = pf.done(zlib.crc32(name.encode()) & 0xffff); b, _k = pb.done((zlib.crc32(name.encode()) + 1) & 0xffff, alpha=keep)
        T[name], T[name + '_b'] = f, b
        return keep
    two('dd_body', lambda back: _p_body(back))
    pb, _ = _p_head(back=True)
    T['dd_head_b'], keep = pb.done(31)
    T['dd_face'] = _p_head(None)[0].done(32, alpha=keep)[0]
    for i, k in enumerate(FACES):
        T[f'dd_face_{k}'] = _p_head(k)[0].done(33 + i, alpha=keep)[0]
    T['dd_arm'] = _p_arm()[0].done(41)[0]
    T['dd_leg'] = _p_leg()[0].done(42)[0]
    T['dd_wing'] = _p_wing()[0].done(43)[0]
    T['dd_tail'] = _p_tail()[0].done(44)[0]
    T['dd_fire_s'] = _p_fire_side().done(45)[0]
    T['dd_fire_t'] = T['dd_fire_s'].rotate(90, expand=False)   # (the same flame for the flat card: its tip toward the image's top)
    T['dd_fire_f'] = _p_fire_burst().done(46)[0]
    T['dd_puff'] = _p_puff().done(47)[0]
    T['dd_kindle'] = _p_puff(True).done(50)[0]
    T['dd_fx_fire'] = _p_fx_fire().done(51)[0]
    T['dd_fx_smoke'] = _p_fx_smoke().done(52)[0]
    T['dd_slash'] = _p_slash().done(48)[0]
    T['dd_boom'] = _p_boom().done(49)[0]
    _TEX.update(T)
    return dict(T)


# ---------------------------------------------------------------------------------------------------- models
def card(box, z, front, back, pv, mirror=False):
    """a picture on a card in the page (an xy plane at z): its front face and its back face, the back the same shape seen from behind"""
    x0, y0, s = box
    if mirror: x0 = -(x0 + s)
    uf, ub = ([16, 0, 0, 16], [0, 0, 16, 16]) if mirror else ([0, 0, 16, 16], [16, 0, 0, 16])
    return [el((x0, y0, z - DZ), (x0 + s, y0 + s, z - DZ), front, pv, faces=('north',), uv={'north': uf}),
            el((x0, y0, z + DZ), (x0 + s, y0 + s, z + DZ), back, pv, faces=('south',), uv={'south': ub})]


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    part('dd_body', card(BOX['body'][0], ZB, 'dd_body', 'dd_body_b', PIVOT['body']))
    part('dd_head', card(BOX['head'][0], ZH, 'dd_face', 'dd_head_b', PIVOT['head']))
    for fc in FACES:
        part(f'dd_head_x{fc}', card(BOX['head'][0], ZH, f'dd_face_{fc}', 'dd_head_b', PIVOT['head']))
    for p, tex in (('armr', 'dd_arm'), ('legr', 'dd_leg'), ('wingr', 'dd_wing')):
        box, z = BOX[p]
        part(f'dd_{p}', card(box, z, tex, tex, PIVOT[p]))
        q = p[:-1] + 'l'
        part(f'dd_{q}', card(box, z, tex, tex, PIVOT[q], mirror=True))
    part('dd_tail', card(BOX['tail'][0], ZT, 'dd_tail', 'dd_tail', PIVOT['tail']))
    # the breath: a flame card standing up along it (seen from the side), the same flame lying flat across it (from above), and a
    # burst of fire at his mouth (from in front)
    # (all of it built full size and shrunk into the model's box - shown at PART_K times the scale)
    fp = PIVOT['fire']; mx, my, mz = fp; z0 = mz - 0.5; L = FIRE_BOX[2]; k = PART_K['fire']
    side = [el((mx - 0.01, my - L / 2, z0 - L), (mx + 0.01, my + L / 2, z0), 'dd_fire_s', fp, faces=('east', 'west'),
               uv={'east': [0, 0, 16, 16], 'west': [16, 0, 0, 16]})]
    flat = [el((mx - L / 2, my - 0.01, z0 - L), (mx + L / 2, my + 0.01, z0), 'dd_fire_t', fp, faces=('up', 'down'),
               uv={'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0]})]
    bx, by, bs = BURST_BOX
    burst = card((mx + bx, my + by, bs), mz - 1.1, 'dd_fire_f', 'dd_fire_f', fp)
    part('dd_fire_fire', shrink(side + flat + burst, k))
    part('dd_fire_puff', shrink(card(PUFF_BOX, mz - 0.5, 'dd_puff', 'dd_puff', fp), k))
    part('dd_fire_kindle', shrink(card(PUFF_BOX, mz - 0.5, 'dd_kindle', 'dd_kindle', fp), k))
    M['dd_fire'] = M['dd_fire_fire']
    # the breath's effect, for the datapack: a crayon flame and a scribble of smoke, each a little card to show (or to burst into)
    for k_ in ('fire', 'smoke'):
        part(f'dd_fx_{k_}', card((-4.0, 0.0, 8.0), 0.0, f'dd_fx_{k_}', f'dd_fx_{k_}', (0.0, 4.0, 0.0)))
    A = PIVOT['slash']
    part('dd_slash', card(SLASH_BOX, ZA - 0.35, 'dd_slash', 'dd_slash', A))
    part('dd_boom', card(BOOM_BOX, ZA - 0.6, 'dd_boom', 'dd_boom', PIVOT['boom']))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """fwd: swung forward (out of the page, toward whoever he faces); out: swung out to his side, in the page (negative: in)"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def roll(d):
    """leaning over to his right (d > 0) or his left, in the page"""
    return qs(('z', -d))


def P(**kw):
    return kw


def wings(up=0.0, back=0.0):
    return dict(wingr=limb(1, -back, up), wingl=limb(-1, -back, up))


def tail(wag=0.0, lift=0.0):
    return dict(tail=qs(('z', wag + lift)))


PROUD = dict(armr=limb(1, 0, 12), arml=limb(-1, 0, 12), head=roll(-4), **wings(6), **tail(-6))


def walk(k, a=16.0, lean=0.0, flap=0.0):
    """a waddle: the swinging leg goes forward, the body rolls over the leg that's down, the tail swings the other way"""
    s, c = math.sin(math.pi * k / 2), math.cos(math.pi * k / 2)
    return dict(body=qs(('x', lean), ('z', 5 * s)), head=qs(('z', -4 * s)),
                legr=limb(1, a * s, -5 * s), legl=limb(-1, -a * s, 5 * s),
                armr=limb(1, -6 * s + 4, 14), arml=limb(-1, 6 * s + 4, 14), **tail(-10 * s), **wings(8 + flap * c))


POSES = {
    # standing proud: chest out, tail up, wings spread a little - look what Kettle made!
    'idle_a': P(**PROUD),
    # a flutter of his little wings, up on his toes, beaming
    'idle_b': P(_face='happy', **dict(PROUD, **wings(34), **tail(6), armr=limb(1, 0, 40), arml=limb(-1, 0, 40), head=roll(6))),
    # a hiccup - and a puff of smoke out of his nose, which surprises him every time
    'idle_c': P(_face='surprised', _fire='puff', body=roll(-3), head=qs(('x', -6), ('z', 5)), armr=limb(1, 0, 30), arml=limb(-1, 0, 30),
                **wings(18), **tail(-14)),
    **{f'walk_{k}': P(**walk(k)) for k in range(4)},
    **{f'run_{k}': P(_face='happy', **dict(walk(k, 24, 10, 24), armr=limb(1, 22, 24), arml=limb(-1, 22, 24))) for k in range(4)},
    'jump': P(_face='surprised', _off=(0, 3.0, 0), legr=limb(1, 10, 18), legl=limb(-1, 10, 18), armr=limb(1, 0, 70), arml=limb(-1, 0, 70),
              **wings(40), **tail(14)),
    # sitting down with a bump: legs out either side, hands on his tummy, tail curled round on the floor
    'sit_a': P(legr=limb(1, 0, 66), legl=limb(-1, 0, 66), armr=limb(1, 0, -14), arml=limb(-1, 0, -14), head=roll(5), **wings(-8), **tail(-22)),
    # ...rocking on his bottom, a wave of one claw, wings fluttering
    'sit_b': P(_face='happy', body=roll(-7), head=roll(10), legr=limb(1, 0, 76), legl=limb(-1, 0, 54), armr=limb(1, 0, 118), arml=limb(-1, 0, -12),
               **wings(26), **tail(-8)),
    'happy': P(_face='happy', legr=limb(1, 0, 8), legl=limb(-1, 0, 8), armr=limb(1, 0, 120), arml=limb(-1, 0, 120), **wings(44), **tail(18)),
    'hurt': P(_face='sad', body=qs(('x', -8), ('z', 6)), head=qs(('x', -8), ('z', -8)), armr=limb(1, 0, -10), arml=limb(-1, 0, -10),
              legr=limb(1, 0, 4), legl=limb(-1, 0, -4), **wings(-20), **tail(-30)),
    # worn out: flopped over on his side, out cold, swirly-eyed
    'tired': P(_face='dizzy', body=roll(88), head=roll(10), armr=limb(1, 0, 20), arml=limb(-1, 0, 50), legr=limb(1, 0, 10), legl=limb(-1, 0, 26),
               **wings(-20), **tail(30)),
    # CRAYON FIRE: a big breath in (cheeks full of smoke, head back) - then a scribble of flame
    'breathe_up': P(_face='puff', _fire='kindle', body=qs(('x', -12)), head=roll(-5), armr=limb(1, 0, 34), arml=limb(-1, 0, 34),
                    **wings(30), **tail(10)),
    'breathe': P(_face='roar', _fire='fire', body=qs(('x', 10)), head=qs(('x', 6)), armr=limb(1, 0, 46), arml=limb(-1, 0, 46),
                 legr=limb(1, -6, 6), legl=limb(-1, 10, 4), **wings(10, 14), **tail(-16)),
    # CLAW SWIPE: his right claw up over his head - then raked down and across, three marks left in the air
    'swipe_up': P(_face='fierce', body=qs(('y', 14), ('z', 6)), head=roll(-6), armr=limb(1, 0, 150), arml=limb(-1, 0, 24), **wings(24), **tail(12)),
    'swipe': P(_face='fierce', _slash=True, body=qs(('y', -16), ('z', -8)), head=roll(4), armr=limb(1, 0, -16), arml=limb(-1, 0, 30),
               **wings(-4), **tail(-20)),
    # A HOP-FLIGHT: wings up - and down, and he's off the ground (for a moment)
    'flap_0': P(_face='happy', _off=(0, 2.4, 0), legr=limb(1, 0, 6), legl=limb(-1, 0, 6), armr=limb(1, 0, 34), arml=limb(-1, 0, 34),
                **wings(46), **tail(-8)),
    'flap_1': P(_face='happy', _off=(0, 4.6, 0), legr=limb(1, 0, 20), legl=limb(-1, 0, 20), armr=limb(1, 0, 18), arml=limb(-1, 0, 18),
                **wings(-34), **tail(10)),
    # STOMP: a sumo stomp - his right leg up and out, leaning away - then slammed down, BOOM
    'stomp_up': P(_face='fierce', body=roll(-14), head=roll(12), legr=limb(1, 0, 58), legl=limb(-1, 0, -12), armr=limb(1, 0, 60), arml=limb(-1, 0, 46),
                  **wings(30), **tail(-6)),
    'stomp': P(_face='roar', _boom=True, body=roll(4), head=roll(-4), legr=limb(1, 0, 12), legl=limb(-1, 0, 6), armr=limb(1, 0, 28), arml=limb(-1, 0, 28),
               **wings(46), **tail(16)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a doggy paddle, head up, his chin on the water: arms churning, legs kicking)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='happy' if _i % 4 else None, _off=(0, -9.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 14), ('z', 4 * math.sin(_p))),
                            head=qs(('x', -10)), armr=limb(1, 0, 40 + 34 * math.sin(_p)), arml=limb(-1, 0, 40 - 34 * math.sin(_p)),
                            legr=limb(1, 0, 14 + 12 * math.sin(2 * _p)), legl=limb(-1, 0, 14 - 12 * math.sin(2 * _p)),
                            **wings(10 + 20 * math.cos(_p)), **tail(14 * math.sin(_p)))


# ---------------------------------------------------------------------------------------------------- the floor
def _pts(p):
    """a card's outline points (design units, its own layer)"""
    src = MIRROR.get(p, p)
    if src not in GEO: return []
    z = BOX[src][1]; sx = -1 if p in MIRROR else 1
    return [(sx * x, y, z) for poly in GEO[src] for x, y in poly[::2]]


_PTS = {p: _pts(p) for p in PARTS}


def lowest(pose):
    """the lowest point of him in this pose (design units) - every card but the effects"""
    xf = solve(PIVOT, PARENT, pose); low = 1e9
    for p, pts in _PTS.items():
        if not pts or p in FX: continue
        q, t = xf[p]; pv = D(PIVOT[p]); W = tuple(t[i] + pv[i] for i in range(3))
        for x, y, z in pts:
            r = qrot(q, tuple(D((x, y, z))[i] - pv[i] for i in range(3)))
            low = min(low, W[1] + r[1])
    return low


def _ground(pose, lift=0.0):
    pose = dict(pose); pose.pop('_off', None)
    pose['_off'] = (0.0, round(lift - lowest(pose), 3), 0.0)
    return pose


AIRBORNE = ('jump', 'flap_0', 'flap_1')            # (off the ground by design - the hop-flight, the jump; the swim floats)
for _k in list(POSES):
    if _k in AIRBORNE or _k.startswith('swim_'):
        continue
    POSES[_k] = _ground(POSES[_k], lift=(0.8 if _k in ('run_1', 'run_3') else 0.0))
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'run_1', 'run_3', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired',
         'breathe_up', 'breathe', 'swipe_up', 'swipe', 'flap_0', 'flap_1', 'stomp_up', 'stomp', 'swim_0', 'swim_2', 'swim_5']
