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
Design units: feet at y=0, facing -z, his right is +x.

3.0a: THE DOODLE ENDER DRAGON (the owner's: "recreate the doodle dragon as the doodle ender dragon so it fits the Minecraft
theme"). Kettle drew him again - this time Minecraft's own Ender Dragon, the way a kid draws the final boss: the same chubby
paper puppet, but in black crayon pressed hard (charcoal scribble, paper flecks showing through, a near-black wobbly outline),
a flat boxy Ender head with its snout in front (two raised nostril bumps on top, a fang either side of a grin), two bony grey
horns and a ridge of grey spines on top of it, glowing PURPLE eyes (Minecraft's magenta slits, made big and cute) with a few
purple "ender particles" doodled round his head, a short ribbed neck, a grey-plated belly, grey spines down his back and along
a long ribbed tail, and big bat wings: a near-black membrane, greyer inside, on light-grey bone fingers with a hooked claw at
each wrist. (His long neck reaches back, away from you - on a front-on puppet it reads as the ribbed collar under his chin and
the spines running up his back.) The eyes and the particles are a card of their own in front of the face (dd_eyes_*,
light_emission 15): they glow at night and keep their purple in every wardrobe look (phase138 recolours the rest).

THE OG GREEN DRAGON - "Crayon Green", his costume: the first drawing, kept exactly as it was (the same rig, pivots, poses and
faces), as a twin set of models: OG_SFX ('_og') on every part of OG_PARTS (dd_body_og, dd_head_og, dd_head_x<face>_og, ...),
its textures the old ones with a '_g' suffix (so phase138 recolours them as a set of their own, as Ava's ghost). rigpet's FORM
puts it on: FORM_SPEC below is what phase235's Dragon needs. The effects (fire, slash, boom) are shared by both drawings.
Previews: a pose with '_og' set shows the costume (model_name).

THE DOODLE CREEPER - his second costume (draft; not wired into the game yet): Kettle draws him as a plain Minecraft creeper in
green crayon - a tall boxy body, a big boxy head with the creeper's face in black crayon (square eyes with a shine, the frown-
mouth, pink cheeks; every FACES expression has its creeper version), four stubby block feet (each leg card a front foot and a
back one beside it), scribbled lighter/darker green blotches. No arms, wings or tail: CR_GONE, hidden (HIDDEN). Models CR_SFX
('_cr') on CR_PARTS, textures CR_TEX ('_cp'; LOOK_CR, recoloured by phase138 as a set of their own); '_crw'/'_cpw' his white
flash. His effects (CR_SFX on fire/slash/boom): the spark breath (fire), the hiss (kindle), a hiccup of smoke (puff), the
KABOOM (fire 'kaboom', round all of him), a POP (slash), stomp dust (boom). A pose with '_cr' shows him, '_crw' flashing;
CR_POSES: his swell (swell_0, swell_1), kaboom, reform - and his own 'tired' (grounded on him: no arm or wing to lie on)."""
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
    if p in CR_GONE and _cr(pose):                     # (the Doodle Creeper: no arms, no wings, no tail)
        return True
    return False


def _cr(pose):
    return bool(pose.get('_cr') or pose.get('_crw'))


def model_name(p, pose, suffix=''):
    cr = CR_SFX if _cr(pose) else ''                                   # (_cr: the Doodle Creeper - his effects too: sparks, a hiss, a pop)
    if p == 'fire':
        return f'{PREFIX}fire_{pose.get("_fire") or "fire"}{cr}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    if cr and p in CR_PARTS:                                            # (_crw: his white flash, swelling up to go boom)
        form = CR_SFX + ('w' if pose.get('_crw') else '')
    elif cr and p in CR_GONE:                                           # (an empty model: what a creeper hasn't got)
        form = CR_SFX
    elif cr and p in ('slash', 'boom'):
        form = CR_SFX
    else:
        form = OG_SFX if pose.get('_og') and p in OG_PARTS else ''    # (_og: the OG green costume - previews; in the game rigpet's FORM)
    return f'{PREFIX}{p}{face}{form}{suffix}'


# (3.0a) the OG green drawing: a costume (rigpet's FORM) - these parts' OG_SFX models; the effects are shared
OG_SFX, OG_TEX = '_og', '_g'
OG_PARTS = ('body', 'head', 'armr', 'arml', 'legr', 'legl', 'wingr', 'wingl', 'tail')
# (3.0?) the Doodle Creeper: Kettle draws him as a plain Minecraft creeper - a second costume. CR_SFX on CR_PARTS (his body, his
# boxy head and every face, his feet: each leg card a pair of stubby block feet, four in all) and on his effects; the parts a
# creeper hasn't got (CR_GONE) are hidden. Textures: CR_TEX on their names ('_cp'; '_cpw': the white flash, never recoloured)
CR_SFX, CR_TEX = '_cr', '_cp'
CR_PARTS = ('body', 'head', 'legr', 'legl')
CR_GONE = ('armr', 'arml', 'wingr', 'wingl', 'tail')


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


# ==================================================================================================== (3.0a) THE DOODLE ENDER DRAGON
# black crayon pressed hard, grey bone, magenta-purple eyes - the same cards, boxes and pivots as the OG drawing
INK = '#16121b'                                    # (his outline: near-black, a hint of violet)
COAL = '#2c2833'                                   # (the black crayon he's scribbled in)
PLATE, PLATE_L = '#5a5566', '#9a95a8'              # (his belly plates, the ribs of his neck and tail)
SPINE, SPINE_L = '#a8a3b6', '#4e4a5a'              # (grey spines: his back, his tail, the ridge on his head)
BONE, BONE_L = '#d6d2de', '#5e5a6c'                # (horns, wing bones, claws)
MEMB, MEMB_IN = '#34303d', '#6f6a80'               # (the wing membrane: near-black, greyer inside)
EYE, EYE_M, EYE_C, EYE_L = '#b62ff0', '#e27cff', '#ffe4ff', '#5c138a'   # (Minecraft's ender magenta: rim, glow, heart; its line)
EMOUTH, ETONGUE = '#2a0c30', '#c45ad8'
TOOTH = '#f4f1f8'
GRIN = '#bcb6ca'                                   # (his grin: a line of pale grey crayon across the black)
DARK = 0.16                                        # (black crayon: hardly any paper under the scribble)


def sq(cx, cy, a, b, e=3.0, n=60):
    """a rounded box (a superellipse): Minecraft-ish, as a kid draws a block"""
    out = []
    for i in range(n):
        t = 2 * math.pi * i / n; c, s = math.cos(t), math.sin(t)
        out.append((cx + a * math.copysign(abs(c) ** (2 / e), c), cy + b * math.copysign(abs(s) ** (2 / e), s)))
    return out


def _e_head():
    skull, snout = sq(0.0, 24.5, 5.7, 3.55, 3.2), sq(0.0, 19.75, 3.95, 2.45, 3.0)
    neck = [(-2.5, 16.25), (2.5, 16.25), (2.1, 18.6), (-2.1, 18.6)]
    horns = [tri((s * 3.7, 27.4), 90 - s * 24, 1.9, 3.4, lean=-s * 0.55) for s in (1, -1)]
    spikes = [tri((x, 27.6), 90 - x * 9, 1.45, h) for x, h in ((-1.35, 1.35), (0.0, 1.75), (1.35, 1.35))]
    nostrils = [sq(s * 2.25, 21.55, 0.8, 0.5, 2.6, 28) for s in (1, -1)]
    return skull, snout, neck, horns, spikes, nostrils


ESPOTS = [(6.75, 28.0, 0.55, 12), (7.5, 25.7, 0.38, -8), (-7.05, 29.15, 0.5, 20), (-7.45, 26.4, 0.36, 4), (5.5, 30.7, 0.32, 30)]


def _e_picture_head(face=None, back=False):
    """the head card (front: the face drawn on; back: his head from behind) - and the eyes, a card of their own"""
    pic = Pic(BOX['head'][0])
    skull, snout, neck, horns, spikes, nostrils = _e_head()
    out = [pic.blob(neck, COAL, INK, 210, ang=10, over=0.2, amp=0.06, ow=0.4, light=DARK)]
    if not back:
        for i, y in enumerate((16.9, 17.75)):
            pic.crayon([(-2.2 + 0.1 * i, y), (2.2 - 0.1 * i, y)], PLATE_L, 0.26, 212 + i, closed=False, passes=1)
    for i, sp in enumerate(spikes):
        out.append(pic.blob(sp, SPINE, SPINE_L, 214 + i, ang=60, over=0.15, amp=0.06, ow=0.32))
    for i, h in enumerate(horns):
        out.append(pic.blob(h, BONE, BONE_L, 218 + i, ang=-30, over=0.15, amp=0.05, ow=0.34))
    out.append(pic.blob(skull, COAL, INK, 220, ang=36, over=0.4, amp=0.12, light=DARK))
    out.append(pic.blob(snout, COAL, INK, 221, ang=-28, over=0.25, amp=0.08, light=DARK))
    if not back:
        for i, n in enumerate(nostrils):
            pic.blob(n, PLATE, INK, 222 + i, ang=20, over=0.0, amp=0.03, ow=0.26)
            pic.dot(((1, -1)[i] * 2.25, 21.45), 0.24, 0.17, INK, 224 + i)
        _e_face(pic, face)
    return pic, out


def _eye(eyes, cx, cy, hw, hh, seed, tilt=0.0):
    """a glowing ender eye: a magenta box, a pinker glow inside, a white-hot heart and a shine"""
    box = sq(cx, cy, hw, hh, 3.2, 36)
    if tilt:
        box = [(x, y + (x - cx) * tilt) for x, y in box]
    eyes.fill(box, EYE, seed, line=EYE_L, ow=0.24)
    eyes.fill([(cx + (x - cx) * 0.62, cy + (y - cy) * 0.55) for x, y in box], EYE_M, seed + 1)
    eyes.fill([(cx + (x - cx) * 0.3, cy + (y - cy) * 0.28) for x, y in box], EYE_C, seed + 2)
    eyes.dot((cx - hw * 0.45, cy + hh * 0.35), 0.24, 0.24, '#ffffff', seed + 3)


def _e_eyes(kind=None):
    """the eye card: his eyes in this expression - and the ender particles round his head (every face)"""
    eyes = Pic(BOX['head'][0]); ex, ey = 2.95, 24.55
    for i, (x, y, r, a) in enumerate(ESPOTS):                    # (little purple squares drifting off him, as the real one sheds)
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        q = [(x + r * (u * c - v * s_), y + r * (u * s_ + v * c)) for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        eyes.fill(q, EYE if i % 2 else EYE_M, 260 + i, line=EYE_L, ow=0.14)
    def arc(y, h, up=True, w=0.5):
        for i, s in enumerate((1, -1)):
            x = s * ex
            pts = bez((x - 1.3, y), (x, y + (h if up else -h) * 2), (x + 1.3, y), 10) + [(x + 1.3, y)]
            eyes.crayon(pts, EYE_L, w + 0.2, 270 + i, closed=False, passes=1, jit=0.02)
            eyes.crayon(pts, EYE, w, 272 + i, closed=False, passes=1, jit=0.02)
    if kind in (None, 'roar'):
        for i, s in enumerate((1, -1)): _eye(eyes, s * ex, ey + (0.15 if kind == 'roar' else 0.0), 1.45, 0.95, 280 + 4 * i)
    elif kind == 'happy':
        arc(24.3, 0.75)
    elif kind == 'blink':
        arc(24.6, 0.4, up=False)
    elif kind == 'surprised':
        for i, s in enumerate((1, -1)):
            eyes.dot((s * ex, ey + 0.1), 1.45, 1.55, EYE, 290 + i, line=EYE_L, ow=0.24)
            eyes.dot((s * ex, ey + 0.1), 0.95, 1.0, EYE_M, 292 + i)
            eyes.dot((s * ex, ey + 0.1), 0.45, 0.48, EYE_C, 294 + i)
    elif kind == 'fierce':                                           # (narrowed: slanting down to the middle)
        for i, s in enumerate((1, -1)): _eye(eyes, s * ex, ey - 0.2, 1.35, 0.62, 300 + 4 * i, tilt=s * 0.3)
    elif kind == 'sad':                                              # (drooping: down at the outside)
        for i, s in enumerate((1, -1)): _eye(eyes, s * ex, ey - 0.25, 1.3, 0.78, 310 + 4 * i, tilt=-s * 0.22)
    elif kind == 'puff':                                             # (squeezed shut: > <)
        for i, s in enumerate((1, -1)):
            x = s * ex; pts = [(x + s * 1.1, ey + 0.85), (x - s * 0.95, ey), (x + s * 1.1, ey - 0.85)]
            eyes.crayon(pts, EYE_L, 0.62, 320 + i, closed=False, passes=1, jit=0.02)
            eyes.crayon(pts, EYE, 0.42, 322 + i, closed=False, passes=1, jit=0.02)
    elif kind == 'dizzy':
        for i, s in enumerate((1, -1)):
            c = (s * ex, ey); pts = [(c[0] + 0.085 * t * math.cos(t * s), c[1] + 0.07 * t * math.sin(t * s)) for t in (j * 0.35 for j in range(40))]
            eyes.crayon(pts, EYE, 0.36, 330 + i, closed=False, passes=1, jit=0.01)
    return eyes


def _e_face(pic, kind):
    """what of his face is on the head card itself (and so takes the wardrobe's colour): mouth, fangs, brows, a tear"""
    K = INK
    def fangs(y=19.0, x=1.75, h=0.95):
        for i, s in enumerate((1, -1)):
            pic.fill([(s * x - 0.42, y + 0.05), (s * x + 0.42, y + 0.05), (s * x + 0.05 * s, y - h)], TOOTH, 400 + i, line=K, ow=0.13)
    def grin(y=19.05, w=2.9, d=0.62):
        pic.crayon(bez((-w, y + 0.35), (0.0, y - d * 2), (w, y + 0.35), 14) + [(w, y + 0.35)], GRIN, 0.4, 404, closed=False, passes=1, jit=0.03)
    def brows(tilt, y=26.35):
        for i, s in enumerate((1, -1)):
            x = s * 2.95
            pic.crayon([(x + s * 1.45, y + tilt * 0.5), (x - s * 1.25, y - tilt * 0.5)], PLATE_L, 0.42, 406 + i, closed=False, passes=1, jit=0.02)
    def open_mouth(cy=18.95, rx=2.75, ry=1.4, tongue=True, teeth=True):
        m = sq(0.0, cy, rx, ry, 2.4, 36)
        pic.fill(m, EMOUTH, 410, line=K, ow=0.3)
        if tongue: pic.dot((0.35, cy - ry * 0.45), rx * 0.42, ry * 0.4, ETONGUE, 411)
        if teeth:
            for i, x in enumerate((-1.7, 1.7)):
                pic.fill([(x - 0.4, cy + ry - 0.1), (x + 0.4, cy + ry - 0.1), (x, cy + ry - 0.95)], TOOTH, 412 + i, line=K, ow=0.12)
            for i, x in enumerate((-0.9, 0.9)):
                pic.fill([(x - 0.35, cy - ry + 0.12), (x + 0.35, cy - ry + 0.12), (x, cy - ry + 0.82)], TOOTH, 414 + i, line=K, ow=0.12)
    if kind is None:
        grin(); fangs()
    elif kind == 'happy':
        open_mouth(18.9, 2.6, 1.15, teeth=False); fangs(19.95, 1.7, 0.75)
    elif kind == 'blink':
        grin(19.1, 2.6, 0.35); fangs(19.0, 1.6, 0.8)
    elif kind == 'surprised':
        pic.dot((0.0, 18.85), 1.05, 1.1, EMOUTH, 420, line=K, ow=0.28)
    elif kind == 'fierce':
        brows(1.35)
        bx, top, bot = 2.9, 19.85, 18.15                                  # (a snarl: teeth clenched)
        pic.fill([(-bx, top), (bx, top), (bx * 0.9, bot), (-bx * 0.9, bot)], TOOTH, 422, line=K, ow=0.3)
        pic.crayon([(-bx * 0.95, (top + bot) / 2), (bx * 0.95, (top + bot) / 2)], K, 0.2, 423, closed=False, passes=1, jit=0.02)
        for i in range(4):
            x = -bx + 2 * bx * (i + 1) / 5
            pic.crayon([(x, top - 0.1), (x, bot + 0.1)], K, 0.15, 424 + i, closed=False, passes=1, jit=0.01)
    elif kind == 'sad':
        brows(-1.0)
        pic.crayon(bez((-2.2, 18.4), (0.0, 20.0), (2.2, 18.4), 12) + [(2.2, 18.4)], GRIN, 0.38, 430, closed=False, passes=1, jit=0.04)
        pic.fill([(-4.3, 23.1), (-4.75, 22.1), (-4.3, 21.6), (-3.85, 22.1)], '#5ab4ff', 431, line='#2a6fc0', ow=0.16)
    elif kind == 'puff':                                                  # (cheeks full of smoke: his snout bulging, lips pressed)
        for i, s in enumerate((1, -1)):
            pic.crayon(bez((s * 3.4, 21.0), (s * 4.9, 19.6), (s * 3.4, 18.0), 10) + [(s * 3.4, 18.0)], PLATE_L, 0.3, 434 + i, closed=False, passes=1)
        pic.dot((0.0, 18.95), 0.8, 0.5, EMOUTH, 436, line=PLATE_L, ow=0.24)
    elif kind == 'roar':
        brows(1.0); open_mouth(18.85, 3.0, 1.55)
    elif kind == 'dizzy':
        pic.crayon(bez((-2.5, 19.3), (0.0, 18.2), (2.5, 19.3), 12) + [(2.5, 19.3)], GRIN, 0.38, 440, closed=False, passes=1, jit=0.03)
        pic.fill(capsule((0.9, 18.8), (1.05, 17.6), 0.55), ETONGUE, 441, line=K, ow=0.2)
    return pic


def _e_body(back=False):
    pic = Pic(BOX['body'][0])
    s = pic.blob(_g_body(), COAL, INK, 11, ang=32, light=DARK)      # (the OG's seeds: the same silhouette, to the pixel)
    if not back:                                                      # (the plates of his belly: grey, ribbed)
        pic.blob(ell(0.0, 10.2, 3.7, 5.3, 48), PLATE, INK, 212, ang=-24, over=0.3, light=0.25, ow=0.36)
        for i, y in enumerate((6.6, 8.6, 10.6, 12.6, 14.4)):
            hw = 3.7 * math.sqrt(max(0.0, 1 - ((y - 10.2) / 5.3) ** 2)) - 0.5
            pic.crayon(bez((-hw, y + 0.2), (0.0, y - 0.4), (hw, y + 0.2), 12) + [(hw, y + 0.2)], PLATE_L, 0.28, 240 + i, closed=False, passes=1)
    else:                                                             # (grey spines down his back, up into his neck)
        for i, (y, h) in enumerate(((6.6, 1.5), (8.8, 1.8), (11.1, 2.0), (13.5, 2.0), (15.8, 1.8))):
            pic.blob(tri((0.0, y - 0.6), 90, 1.8, h), SPINE, SPINE_L, 260 + i, ang=50, over=0.15, ow=0.3, amp=0.06)
    return pic, [s]


def _e_arm():
    pic = Pic(BOX['armr'][0])
    body, claws = _g_arm()
    out = [pic.blob(c, BONE, BONE_L, 70 + i, scrib=False, amp=0.04, ow=0.26) for i, c in enumerate(claws)]
    out.append(pic.blob(body, COAL, INK, 74, ang=-50, over=0.35, amp=0.1, light=DARK))
    return pic, out


def _e_leg():
    pic = Pic(BOX['legr'][0])
    leg, foot = _g_leg()
    out = [pic.blob(leg, COAL, INK, 80, ang=70, over=0.35, amp=0.1, light=DARK)]
    out.append(pic.blob(foot, COAL, INK, 81, ang=20, over=0.0, amp=0.07, light=DARK))
    for i, x in enumerate((2.1, 3.3, 4.5)):
        pic.dot((x, 0.75 if i != 1 else 0.68), 0.46, 0.4, BONE, 282 + i, line=BONE_L, ow=0.16)
    return pic, out


WING_E = dict(R1=(4.4, 17.0), W=(10.4, 22.2), T=(17.6, 23.4), F=[(18.3, 16.0), (15.4, 11.9), (11.0, 10.5)], R2=(4.7, 12.0))


def _e_g_wing():
    """his wing: the arm bone up and out to the wrist and on to a hooked tip; three fingers fanning down from the wrist; the
    membrane between them scalloped in toward his shoulder"""
    R1, W, T, F, R2 = WING_E['R1'], WING_E['W'], WING_E['T'], WING_E['F'], WING_E['R2']
    pts = bez(R1, (6.4, 21.4), W) + bez(W, (14.0, 24.4), T)
    ends = [T] + F
    for a, b in zip(ends, ends[1:]):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        pts += bez(a, (m[0] + (W[0] - m[0]) * 0.28, m[1] + (W[1] - m[1]) * 0.28), b)
    pts += bez(F[-1], (7.6, 12.6), R2)
    return pts


def _e_wing():
    pic = Pic(BOX['wingr'][0])
    R1, W, T, F = WING_E['R1'], WING_E['W'], WING_E['T'], WING_E['F']
    shape = pic.blob(_e_g_wing(), MEMB, INK, 290, ang=58, over=0.35, amp=0.12, light=DARK)
    if not Pic.DRY:                                                    # (greyer inside: the membrane catching the light)
        pic.scribble(grow(shape, -1.1), MEMB_IN, -40, 291, sp=0.9, w=0.22)
    bones = [spline([R1, (7.2, 20.4), W], 6), spline([W, (14.0, 23.6), T], 6)] + [spline([W, ((W[0] + f[0]) / 2 + 0.3, (W[1] + f[1]) / 2 + 0.2), f], 6) for f in F]
    out = [shape]
    for i, c in enumerate(bones):
        w0 = 1.05 if i < 2 else 0.78
        out.append(pic.blob(tube(c, w0, w0 * 0.55), BONE, BONE_L, 292 + i, scrib=False, amp=0.03, ow=0.24))
    out.append(pic.blob(tri((W[0] + 0.2, W[1] + 0.3), 104, 1.1, 1.7), BONE, BONE_L, 299, scrib=False, amp=0.03, ow=0.24))   # (the hook at his wrist)
    return pic, out


TAIL_E = [(-4.4, 9.2), (-6.8, 8.6), (-9.1, 7.75), (-11.6, 7.0), (-13.8, 7.1), (-15.3, 8.3), (-15.7, 10.0), (-15.0, 11.3), (-14.0, 11.4)]


def _e_tail():
    pic = Pic(BOX['tail'][0])
    c = spline(TAIL_E, 8); n = len(c)
    body = tube(c, 3.7, 0.95)
    nm = _normals(c, False); out = []
    wid = lambda i: (3.7 + (0.95 - 3.7) * i / (n - 1)) / 2
    for k, (t, h) in enumerate(((0.15, 1.55), (0.27, 1.6), (0.39, 1.45), (0.5, 1.25), (0.61, 1.0))):
        i = int(t * n); p, m = c[i], nm[i]
        out.append(pic.blob(tri((p[0] + m[0] * (wid(i) - 0.25), p[1] + m[1] * (wid(i) - 0.25)), math.degrees(math.atan2(m[1], m[0])), 1.4, h, lean=-0.25),
                            SPINE, SPINE_L, 300 + k, ang=60, over=0.15, amp=0.05, ow=0.3))
    out.append(pic.blob(body, COAL, INK, 310, ang=-35, over=0.35, amp=0.1, light=DARK))
    for k, t in enumerate((0.12, 0.23, 0.34, 0.45, 0.56, 0.67, 0.78)):  # (ribbed: bands across it, as the real one's segments)
        i = int(t * n); p, m = c[i], nm[i]; w = wid(i) - 0.3
        if not Pic.DRY:
            pic.crayon([(p[0] + m[0] * w, p[1] + m[1] * w), (p[0] - m[0] * w, p[1] - m[1] * w)], PLATE_L, 0.22, 320 + k, closed=False, passes=1)
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


# ==================================================================================================== THE DOODLE CREEPER
# Kettle draws him as a creeper: a plain Minecraft creeper, the way a kid draws one in green crayon - a tall boxy body, a big
# boxy head with the creeper's face in black crayon (square eyes, each with a shine; the frown-mouth), pink cheeks, and four
# stubby block feet (each leg card a pair: the front foot and the back one peeking out beside it, a little higher). Scribbled
# lighter and darker green blotches all over, as the real one's mottled skin. No arms, no wings, no tail (CR_GONE: hidden).
CRG, CRG_L = '#58b844', '#22601d'                  # (creeper green; its outline)
CRG_LT, CRG_DK, CRG_PALE = '#a8e48c', '#2e8a2a', '#d4ecc6'   # (the blotches: light, dark - and a few near-white)
CRG_FOOT = '#4aa53a'                               # (the back feet: a shade further away)
CK, CK_L = '#1e1b22', '#0c0b0e'                    # (his face: black crayon pressed hard)
CMOUTH = '#4a1626'                                 # (inside his mouth, open)
WHITE = '#ffffff'
# the effects: gunpowder grey-green smoke, yellow-white sparks, black specks of powder
PUFF_C, PUFF_L, PUFF_D = '#e2e9d8', '#7f8f72', '#c3cfb3'
SPARK, SPARK_L = '#fff27a', '#e09a14'
POWDER = '#3a3a3c'

CR_BODY = (0.0, 11.0, 4.7, 7.0)                     # (centre, half-width, half-height: y 4.0 .. 18.0 - no lower than the pear he shares the poses with)
CR_HEAD = (0.0, 22.9, 6.2, 6.1)                     # (y 16.8 .. 29.0: big, as a chibi's)
CR_EYE = (2.85, 24.55, 1.45)                        # (x either side, y, half-size)
CR_FEET = ((4.05, 2.3, 1.5, 2.3, 0.0), (1.8, 2.6, 1.28, 2.0, 1.0))   # (front foot, back foot: centre x, y, half w, half h, shade)


def _mottle(pic, shape, seed, n=14, avoid=None, size=(0.55, 1.2)):
    """a creeper's blotches: little squarish patches scribbled over him in lighter and darker green, kept inside his outline"""
    if Pic.DRY: return
    poly = grow(shape, -OW * 0.9); r = random.Random(seed)
    def inside(pt):                                    # (even-odd ray test)
        x, y = pt; c = False
        for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
        return c
    xs, ys = [p[0] for p in shape], [p[1] for p in shape]; k = 0; tries = 0
    while k < n and tries < 600:
        tries += 1
        s_ = r.uniform(*size); cx, cy = r.uniform(min(xs), max(xs)), r.uniform(min(ys), max(ys))
        q = sq(cx, cy, s_ * r.uniform(0.8, 1.25), s_ * r.uniform(0.8, 1.2), 3.5, 20)
        if not all(inside(p) for p in q[::3]): continue
        if avoid and any(a[0] <= cx <= a[2] and a[1] <= cy <= a[3] for a in avoid): continue
        col = (CRG_LT, CRG_DK, CRG_LT, CRG_DK, CRG_PALE)[k % 5]
        pic.scribble(wob(q, 0.08, seed + 7 * k), col, r.uniform(-60, 60), seed + 13 * k, sp=0.42, w=0.3)
        k += 1


def _cr_body(back=False):
    pic = Pic(BOX['body'][0])
    s = pic.blob(sq(*CR_BODY, 3.6, 64), CRG, CRG_L, 1011, ang=30, over=0.45)
    _mottle(pic, s, 1020 + back, 12)
    if not Pic.DRY: pic.crayon(s, CRG_L, OW, 1016)                  # (the outline gone over again, on top of the blotches)
    return pic, [s]


CR_FACE_ZONE = [(-4.6, 17.4, 4.6, 26.5)]           # (no blotch where his face is drawn - it stays easy to read)


def _cr_picture_head(face=None, back=False):
    pic = Pic(BOX['head'][0])
    s = pic.blob(sq(*CR_HEAD, 4.2, 64), CRG, CRG_L, 1031, ang=36, over=0.45)
    _mottle(pic, s, 1040 + back, 13 if back else 10, None if back else CR_FACE_ZONE)
    if not Pic.DRY: pic.crayon(s, CRG_L, OW, 1036)
    if not back:
        _cr_face(pic, face)
    return pic, [s]


def _cmouth(sc=1.0, flip=False, cy=20.45):
    """the creeper's mouth: the bar under his eyes, the wide middle, the two legs down at its corners"""
    pts = [(-1.15, 22.75), (1.15, 22.75), (1.15, 21.7), (2.35, 21.7), (2.35, 17.95), (1.25, 17.95), (1.25, 19.0), (-1.25, 19.0),
           (-1.25, 17.95), (-2.35, 17.95), (-2.35, 21.7), (-1.15, 21.7)]
    return [(x * sc, cy + (y - cy) * sc * (-1 if flip else 1)) for x, y in pts]


def _cr_face(pic, kind):
    """his creeper face, on the head card (and so in the wardrobe's colours, as the OG's): black crayon - each expression
    redraws it"""
    ex, ey, eh = CR_EYE
    def black(poly, seed, ow=0.3):
        return pic.blob(poly, CK, CK_L, seed, ang=50, over=0.08, light=0.12, amp=0.035, ow=ow)
    def eyes(hw=eh, hh=eh, dy=0.0, tilt=0.0, shine=True):
        for i, s in enumerate((1, -1)):
            q = sq(s * ex, ey + dy, hw, hh, 4.5, 36)
            if tilt: q = [(x, y + (x - s * ex) * tilt * s) for x, y in q]
            black(q, 1100 + i)
            if shine:
                pic.fill(sq(s * ex - hw * 0.42, ey + dy + hh * 0.36, 0.36, 0.36, 3.0, 16), WHITE, 1104 + i)
    def cheeks(r=0.95, y=21.2, x=4.6):
        for i, s in enumerate((1, -1)):
            pic.dot((s * x, y), r, r * 0.72, CHEEK, 1110 + i)
    def chevron(up=True, y=ey, w=0.62):                                 # (^ ^ - or, up=False, v v)
        for i, s in enumerate((1, -1)):
            x = s * ex; h = 0.75 if up else -0.6
            pic.crayon([(x - 1.35, y - h), (x, y + h), (x + 1.35, y - h)], CK, w, 1120 + i, closed=False, passes=2, jit=0.025)
    def brows(tilt, y=26.9):
        for i, s in enumerate((1, -1)):
            x = s * ex
            pic.crayon([(x + s * 1.5, y + tilt * 0.5), (x - s * 1.3, y - tilt * 0.5)], CK, 0.5, 1130 + i, closed=False, passes=2, jit=0.02)
    if kind is None:
        eyes(); cheeks(); black(_cmouth(), 1140)
    elif kind == 'happy':                                               # (eyes squeezed into ^ ^, the creeper's mouth turned up into a smile)
        chevron(True, ey - 0.1); cheeks(1.15, 21.6)
        m = black(_cmouth(0.95, flip=True, cy=20.2), 1141)
        pic.dot((0.0, 18.95), 0.62, 0.42, TONGUE, 1142)
    elif kind == 'surprised':                                           # (big white eyes, little black pupils, an 'o' of a mouth)
        for i, s in enumerate((1, -1)):
            pic.blob(sq(s * ex, ey + 0.15, 1.6, 1.7, 4.5, 36), WHITE, CK, 1150 + i, scrib=False, amp=0.03, ow=0.32)
            black(sq(s * ex, ey + 0.05, 0.62, 0.68, 4.0, 24), 1152 + i, ow=0.2)
            pic.fill(sq(s * ex - 0.22, ey + 0.32, 0.18, 0.18, 3.0, 12), WHITE, 1154 + i)
        cheeks(0.8, 20.9)
        black(sq(0.0, 19.9, 1.05, 1.3, 4.0, 32), 1156)
    elif kind == 'blink':                                               # (eyes shut: two thick crayon lines, curving down)
        for i, s in enumerate((1, -1)):
            x = s * ex
            pic.crayon(bez((x - 1.4, ey + 0.1), (x, ey - 0.85), (x + 1.4, ey + 0.1), 10) + [(x + 1.4, ey + 0.1)], CK, 0.55, 1160 + i,
                       closed=False, passes=2, jit=0.02)
        cheeks(); black(_cmouth(0.9), 1162)
    elif kind == 'fierce':                                              # (narrowed eyes slanting in, brows down, the mouth wide - two little fangs)
        eyes(1.45, 1.05, -0.25, 0.32, shine=True); brows(1.3)
        m = _cmouth(1.1, cy=20.3); black(m, 1170)
        for i, s in enumerate((1, -1)):
            pic.fill([(s * 1.55, 21.55), (s * 2.25, 21.55), (s * 1.9, 20.55)], WHITE, 1172 + i, line=CK, ow=0.12)
    elif kind == 'sad':                                                 # (eyes drooping at the outside, worried brows, a little frown - and a tear)
        eyes(1.35, 1.2, -0.2, -0.26); brows(-1.0, 26.9); cheeks(0.8, 21.0)
        black(_cmouth(0.82, cy=20.0), 1180)
        pic.fill([(-4.6, 22.9), (-5.05, 21.9), (-4.6, 21.4), (-4.15, 21.9)], '#5ab4ff', 1181, line='#2a6fc0', ow=0.16)
    elif kind == 'puff':                                                # (cheeks puffed right out, eyes squeezed > <, lips pressed tight - swelling)
        for i, s in enumerate((1, -1)):
            x = s * ex
            pic.crayon([(x + s * 1.2, ey + 0.9), (x - s * 1.05, ey), (x + s * 1.2, ey - 0.9)], CK, 0.6, 1190 + i, closed=False, passes=2, jit=0.02)
        cheeks(1.55, 20.8, 4.3)
        black(sq(0.0, 20.0, 1.25, 0.55, 4.0, 28), 1192)
    elif kind == 'roar':                                                # (the creeper mouth opened wide: dark inside, a tongue - the hiss comes out of here)
        eyes(1.45, 1.15, 0.15, 0.18); brows(0.9, 27.1)
        m = _cmouth(1.22, cy=20.15); black(m, 1200, ow=0.34)
        if not Pic.DRY:
            pic.fill([(x * 0.78, 20.15 + (y - 20.15) * 0.72) for x, y in _cmouth(1.22, cy=20.15)], CMOUTH, 1201)
            pic.dot((0.0, 19.25), 1.1, 0.55, TONGUE, 1202)
    elif kind == 'dizzy':                                               # (fainted: swirly eyes, a wobbly mouth, tongue out)
        for i, s in enumerate((1, -1)):
            c = (s * ex, ey); pts = [(c[0] + 0.09 * t * math.cos(t * s), c[1] + 0.09 * t * math.sin(t * s)) for t in (j * 0.35 for j in range(42))]
            pic.crayon(pts, CK, 0.42, 1210 + i, closed=False, passes=1, jit=0.01)
        cheeks(0.8, 20.9)
        pic.crayon([(-2.4, 20.2), (-1.2, 19.5), (0.0, 20.2), (1.2, 19.5), (2.4, 20.2)], CK, 0.48, 1212, closed=False, passes=2, jit=0.03)
        pic.fill(capsule((1.2, 19.4), (1.35, 18.3), 0.55), TONGUE, 1213, line=CK, ow=0.2)
    return pic


def _cr_leg():
    """a pair of stubby block feet on each leg card: the front one, and the back one beside it (a little higher - further back);
    a stub of leg up to the hip, hidden behind his body until a pose swings it out"""
    pic = Pic(BOX['legr'][0]); out = []
    out.append(pic.blob(sq(3.05, 4.9, 1.75, 1.9, 3.0, 40), CRG, CRG_L, 1301, ang=60, over=0.2, amp=0.06))
    (fx, fy, fw, fh, _), (bx, by, bw, bh, _) = CR_FEET
    b = pic.blob(sq(bx, by, bw, bh, 3.4, 40), CRG_FOOT, CRG_L, 1302, ang=70, over=0.0, amp=0.06, light=0.35)
    _mottle(pic, b, 1303, 2, size=(0.4, 0.7))
    f = pic.blob(sq(fx, fy, fw, fh, 3.4, 40), CRG, CRG_L, 1304, ang=20, over=0.0, amp=0.06)   # (no scribble past the sole: he stands on it)
    _mottle(pic, f, 1305, 3, size=(0.4, 0.75))
    if not Pic.DRY:
        pic.crayon(f, CRG_L, OW, 1306)
    return pic, out + [b, f]


# the effects, creeper-style ------------------------------------------------------------------------------------
STROKES = {                                         # (a kid's capitals, in a box 0.7 wide and 1 tall: crayon strokes)
    'K': [[(0, 0), (0, 1)], [(0.7, 1), (0.05, 0.45), (0.7, 0)]],
    'A': [[(0, 0), (0.35, 1), (0.7, 0)], [(0.14, 0.38), (0.56, 0.38)]],
    'B': [[(0, 0), (0, 1), (0.42, 1), (0.6, 0.9), (0.6, 0.64), (0.42, 0.53), (0, 0.53)], [(0.42, 0.53), (0.7, 0.4), (0.7, 0.12), (0.5, 0), (0, 0)]],
    'O': [[(0.35 + 0.36 * math.cos(t), 0.5 + 0.5 * math.sin(t)) for t in (2 * math.pi * i / 20 + 1.6 for i in range(21))]],
    'M': [[(0, 0), (0, 1), (0.35, 0.45), (0.7, 1), (0.7, 0)]],
    'P': [[(0, 0), (0, 1), (0.48, 1), (0.7, 0.86), (0.7, 0.62), (0.48, 0.5), (0, 0.5)]],
    'S': [[(0.68, 0.86), (0.5, 1), (0.16, 1), (0.0, 0.83), (0.08, 0.6), (0.62, 0.42), (0.7, 0.18), (0.54, 0.0), (0.16, 0.0), (0.0, 0.14)]],
    's': [[(0.5, 0.6), (0.36, 0.68), (0.12, 0.66), (0.04, 0.52), (0.14, 0.4), (0.46, 0.3), (0.52, 0.14), (0.38, 0.0), (0.1, 0.0), (0.0, 0.08)]],
    'h': [[(0, 0), (0, 1)], [(0, 0.38), (0.15, 0.6), (0.38, 0.66), (0.52, 0.52), (0.52, 0)]],
    '!': [[(0.2, 1), (0.2, 0.32)], [(0.2, 0.08), (0.21, 0.04)]],
}


def _letters(pic, text, at, h, seed, col=WHITE, line=CK, w=0.55, ang=0.0, adv=0.92, bounce=0.12):
    """crayon writing: each letter gone over thick in the dark crayon, then in its colour on top - wobbly, bouncing on its line.
    at: where the first letter starts - as the viewer reads it, on the left (the card's +x)"""
    if Pic.DRY: return
    r = random.Random(seed); a = math.radians(ang); c, s_ = math.cos(a), math.sin(a)
    x = 0.0; strokes = []
    for ch in text:
        if ch == ' ': x += 0.5 * h; continue
        dy, rot = r.uniform(-bounce, bounce) * h, math.radians(r.uniform(-9, 9))
        cr, sr = math.cos(rot), math.sin(rot)
        for st in STROKES[ch]:
            pts = []
            for u, v in st:
                u, v = (u - 0.35) * h, (v - 0.5) * h
                u, v = u * cr - v * sr + x + 0.35 * h, u * sr + v * cr + 0.5 * h + dy
                pts.append((at[0] - (u * c - v * s_), at[1] + u * s_ + v * c))   # (the card's +x is the viewer's left: written leftward)
            strokes.append(_resample(pts, 0.25, False) if len(pts) > 2 else pts)
        x += adv * h * (0.62 if ch in 'sh!' else 0.8)
    for i, st in enumerate(strokes):
        pic.crayon(st, line, w + 0.34, seed + 3 * i, closed=False, passes=1, jit=0.02)
    for i, st in enumerate(strokes):
        pic.crayon(st, col, w, seed + 3 * i + 1, closed=False, passes=1, jit=0.02)


def _spark(pic, c, r, seed, col=SPARK, line=SPARK_L):
    """a little crayon spark: a four-pointed star"""
    pts = []
    for i in range(8):
        a = math.pi / 4 * i + 0.3; rr = r if i % 2 == 0 else r * 0.38
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    pic.blob(pts, col, line, seed, scrib=False, amp=0.02, ow=0.22)


def _puffball(pic, c, r, seed, col=PUFF_C, line=PUFF_L, ow=0.32):
    """a lumpy crayon puff of smoke"""
    pic.blob(ell(c[0], c[1], r, r * 0.9, 28), col, line, seed, ang=30 + seed % 60, over=0.2, amp=0.1, ow=ow)
    if not Pic.DRY:
        pic.crayon(bez((c[0] - r * 0.45, c[1] + r * 0.05), (c[0] - r * 0.05, c[1] + r * 0.5), (c[0] + r * 0.35, c[1] + r * 0.1), 8) +
                   [(c[0] + r * 0.35, c[1] + r * 0.1)], line, 0.2, seed + 1, closed=False, passes=1)


def _powder(pic, pts, seed):
    if Pic.DRY: return
    r = random.Random(seed)
    for i, (x, y) in enumerate(pts):
        pic.dot((x, y), r.uniform(0.16, 0.28), r.uniform(0.14, 0.24), POWDER, seed + i)


def _p_cr_cone(frame=lambda a, b: (-a, b)):
    """THE SPARK BREATH (his crayon fire, creeper-style): a cone of gunpowder smoke out of his mouth, puffs growing as it goes,
    sparks fizzing all through it, specks of powder - it pops a beat later"""
    pic = Pic(FIRE_BOX); r = random.Random(1400)
    for i, (a, rad) in enumerate(((3.0, 1.3), (6.6, 1.9), (10.6, 2.5), (15.0, 2.9), (19.6, 3.2), (23.6, 2.6))):
        for j, off in enumerate((-0.55, 0.55) if i >= 2 else (0.0,)):
            _puffball(pic, frame(a + j * 0.9, off * rad), rad * (0.9 if j else 1.0), 1402 + 10 * i + j, col=PUFF_C if (i + j) % 2 else PUFF_D)
    for k in range(16):
        a = r.uniform(2.0, 25.0); b = r.uniform(-1, 1) * (0.9 + a * 0.13)
        _spark(pic, frame(a, b), r.uniform(0.55, 1.05) * (0.7 + a / 40), 1480 + k)
    _powder(pic, [frame(r.uniform(2, 26), r.uniform(-1, 1) * (1 + r.uniform(0, 26) * 0.12)) for _ in range(22)], 1500)
    return pic


def _p_cr_burst():
    """(the spark breath, from in front: a ring of smoke round his mouth, sparks flying out of it)"""
    pic = Pic(BURST_BOX); r = random.Random(1520)
    for i in range(7):
        a = 2 * math.pi * i / 7 + 0.4
        _puffball(pic, (3.3 * math.cos(a), 3.3 * math.sin(a)), 1.7, 1521 + 3 * i, col=PUFF_C if i % 2 else PUFF_D, ow=0.28)
    _spark(pic, (0.0, 0.0), 2.2, 1550)
    for k in range(6):
        a = 2 * math.pi * k / 6; _spark(pic, (5.4 * math.cos(a), 5.4 * math.sin(a)), 0.9, 1551 + k)
    return pic


def _p_cr_hiss():
    """THE HISS (his wind-up): 'hsss' scribbled up beside his head, sparks fizzing off the corners of his mouth"""
    pic = Pic(PUFF_BOX)
    for i, s in enumerate((1, -1)):
        _spark(pic, (s * 3.6, 18.4), 0.85, 1600 + i); _spark(pic, (s * 4.4, 17.0), 0.55, 1602 + i)
        for j in range(3):                                              # (little fizz lines)
            pic.crayon([(s * (6.9 + 0.2 * j), 26.0 - 1.6 * j), (s * (8.6 + 0.4 * j), 26.4 - 1.5 * j)], CK, 0.26, 1604 + 3 * i + j, closed=False, passes=1)
    _letters(pic, 'hsss', (-6.6, 28.6), 3.2, 1620, col='#c6f0b0', line=CRG_L, w=0.6, ang=10)
    return pic


def _p_cr_puff():
    """(the hiccup: a little pop of grey-green smoke off either corner of his head - and a spark)"""
    pic = Pic(PUFF_BOX)
    for s in (1, -1):
        for i, ((x, y), r) in enumerate((((7.3, 28.4), 0.85), ((8.7, 30.3), 1.2))):
            _puffball(pic, (s * x, y), r, 1700 + i + (s > 0) * 10, col=PUFF_C if i % 2 else PUFF_D, ow=0.28)
    _spark(pic, (-10.8, 28.4), 0.8, 1730)
    return pic


KABOOM_BOX = (-16.0, -5.0, 32.0)                    # (round his whole body, from his mouth (the fire part's joint))


def _p_cr_kaboom():
    """THE KABOOM: he swells, flashes white - and goes off. A big scribbled cloud of grey-green smoke round all of him, a jagged
    yellow-white flash in the middle, sparks and powder flying, KABOOM! written across it in fat crayon. (No crater: a
    drawing's explosion. He scribbles himself back together after.)"""
    pic = Pic(KABOOM_BOX); c = (0.0, 12.0); r = random.Random(1800)
    for i in range(11):                                                  # (the cloud: a ring of lumpy puffs)
        a = 2 * math.pi * i / 11 + 0.2
        _puffball(pic, (c[0] + 10.4 * math.cos(a), c[1] + 9.6 * math.sin(a)), 4.0 + 0.6 * math.sin(i * 1.9), 1801 + 5 * i,
                  col=PUFF_C if i % 2 else PUFF_D, ow=0.42)
    _puffball(pic, c, 9.6, 1870, col='#cbd5bd', line=PUFF_L, ow=0.4)
    star = []
    for i in range(22):                                                  # (the flash: a jagged star)
        a = 2 * math.pi * i / 22; rr = (8.2 if i % 2 == 0 else 4.6) * (1 + 0.14 * math.sin(i * 2.3))
        star.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a) * 0.92))
    pic.blob(star, SPARK, SPARK_L, 1880, ang=20, over=0.4, amp=0.15, light=0.25, ow=0.42)
    pic.blob(ell(c[0], c[1], 3.6, 3.3, 28), '#fffbe0', '#f0c030', 1881, ang=-30, over=0.2, amp=0.1, light=0.1, ow=0.32)
    for k in range(12):
        a = 2 * math.pi * k / 12 + 0.15; rr = r.uniform(12.6, 14.4)
        _spark(pic, (c[0] + rr * math.cos(a), c[1] + rr * math.sin(a) * 0.95), r.uniform(0.8, 1.3), 1890 + k)
    _powder(pic, [(c[0] + r.uniform(-14, 14), c[1] + r.uniform(-13, 14)) for _ in range(26)], 1910)
    _letters(pic, 'KABOOM!', (13.2, 9.4), 4.4, 1940, col=WHITE, line=CK, w=0.85, ang=6, adv=0.98)
    return pic


def _p_cr_pop():
    """THE POP (his claw, creeper-style): a hiss and a little scribbled blast beside him - a white-yellow star in a puff, POP!"""
    pic = Pic(SLASH_BOX); c = (10.2, 12.6)
    for i in range(6):
        a = 2 * math.pi * i / 6 + 0.5
        _puffball(pic, (c[0] + 3.1 * math.cos(a), c[1] + 3.0 * math.sin(a)), 1.8, 2001 + 3 * i, col=PUFF_C if i % 2 else PUFF_D, ow=0.3)
    star = []
    for i in range(14):
        a = 2 * math.pi * i / 14; rr = (3.6 if i % 2 == 0 else 1.9)
        star.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    pic.blob(star, SPARK, SPARK_L, 2030, ang=20, over=0.25, amp=0.08, light=0.2, ow=0.34)
    for k, (dx, dy) in enumerate(((6.2, 3.8), (6.6, -2.8), (-0.4, 6.0), (2.8, -5.6), (8.4, 0.6))):
        _spark(pic, (c[0] + dx, c[1] + dy), 0.75, 2040 + k)
    _letters(pic, 'POP!', (c[0] + 3.0, c[1] + 4.6), 2.6, 2050, col=WHITE, line=CK, w=0.5, ang=6)
    return pic


def _p_cr_boom():
    """(the stomp, creeper-style: grey-green dust puffing out either side of his foot, sparks flying up)"""
    F = (3.3, 0.0); pic = Pic(BOOM_BOX)
    for i, (x, y, r) in enumerate(((-1.6, 1.4, 1.6), (-4.0, 1.0, 1.1), (-6.0, 0.8, 0.75), (8.4, 1.4, 1.6), (10.8, 1.0, 1.1), (12.8, 0.8, 0.75))):
        _puffball(pic, (x, y), r, 2101 + 3 * i, col=PUFF_C if i % 2 else PUFF_D, ow=0.3)
    for k, a in enumerate((30, 60, 90, 120, 150)):
        rr = 6.0 + 1.2 * (k % 2); u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        _spark(pic, (F[0] + u[0] * rr, F[1] + 0.8 + u[1] * rr), 0.95, 2130 + k)
    _powder(pic, [(F[0] + x, y) for x, y in ((-3.0, 4.2), (4.6, 5.0), (-5.4, 2.8), (7.0, 3.0), (0.4, 7.6), (6.2, 7.0))], 2140)
    return pic


def charged(im):
    """(3.0b) THE SHINY DOODLE CREEPER - a charged creeper, as a kid draws one: his own green crayon under a crackle of light-blue
    crayon swirls (the real one's electric shell), scribbled on in waves, his black face showing through"""
    import numpy as np
    a = np.asarray(im.convert('RGBA')).astype(np.float32); h, w = a.shape[:2]
    y, x = np.mgrid[0:h, 0:w].astype(np.float32) / max(h, w)
    ph = (x + y) * 26.0 + 2.2 * np.sin(y * 17.0) + 1.6 * np.sin(x * 11.0 + 1.3)
    band = np.sin(ph)                                                   # (diagonal swirling stripes)
    lum = a[..., :3].mean(axis=2) / 255.0
    rng = np.random.default_rng(7)
    core = (band > 0.55) & (rng.random((h, w)) > 0.12)                 # (a waxy stripe: paper flecks through it)
    edge = (band > 0.3) & ~core
    k = np.clip((lum - 0.14) / 0.2, 0, 1)[..., None]                   # (his face and outlines stay black under it)
    blue, deep = np.array([150, 225, 255], np.float32), np.array([60, 140, 230], np.float32)
    rgb = a[..., :3]
    rgb = np.where(core[..., None], rgb + (blue - rgb) * 0.78 * k, rgb)
    rgb = np.where(edge[..., None], rgb + (deep - rgb) * 0.45 * k, rgb)
    a[..., :3] = rgb
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def _flash(im):
    """the white flash (_cpw): his crayon picture gone most of the way to white, the lines still showing through"""
    import numpy as np
    a = np.asarray(im).astype(np.float32)
    lum = a[..., :3].mean(axis=2, keepdims=True) / 255.0
    k = 0.34 + 0.5 * np.clip((lum - 0.12) / 0.3, 0, 1)                 # (his black face and outlines whiten least: still him)
    a[..., :3] = a[..., :3] + (255 - a[..., :3]) * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


# each card's outer edge, as drawn (the outline, and the scribble that runs past it) - the floor finds his lowest point on them
# (3.0a: the Ender drawing's - he stands on them; GEO_OG: the OG green drawing's, for its own check)
GEO_OG = {}
Pic.DRY = True
for _part, _fn in (('body', _e_body), ('head', _e_picture_head), ('armr', _e_arm), ('legr', _e_leg), ('wingr', _e_wing), ('tail', _e_tail)):
    GEO[_part] = _fn()[0].edges
for _part, _fn in (('body', _p_body), ('head', _p_head), ('armr', _p_arm), ('legr', _p_leg), ('wingr', _p_wing), ('tail', _p_tail)):
    GEO_OG[_part] = _fn()[0].edges
GEO_CR = {}                                         # (the Doodle Creeper's: his body, his head, his feet)
for _part, _fn in (('body', _cr_body), ('head', _cr_picture_head), ('legr', _cr_leg)):
    GEO_CR[_part] = _fn()[0].edges
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
    # (3.0a) the Doodle Ender Dragon - the default drawing, under the names the OG had (the wardrobe's recolours, phase138)
    two('dd_body', lambda back: _e_body(back))
    pb, _ = _e_picture_head(back=True)
    T['dd_head_b'], keep = pb.done(231)
    T['dd_face'] = _e_picture_head(None)[0].done(232, alpha=keep)[0]
    for i, k in enumerate(FACES):
        T[f'dd_face_{k}'] = _e_picture_head(k)[0].done(233 + i, alpha=keep)[0]
    T['dd_eyes'] = _e_eyes(None).done(250)[0]                  # (the glowing eyes and the ender particles: never recoloured)
    for i, k in enumerate(FACES):
        T[f'dd_eyes_{k}'] = _e_eyes(k).done(251 + i)[0]
    T['dd_arm'] = _e_arm()[0].done(241)[0]
    T['dd_leg'] = _e_leg()[0].done(242)[0]
    T['dd_wing'] = _e_wing()[0].done(243)[0]
    T['dd_tail'] = _e_tail()[0].done(244)[0]
    # the OG green drawing ('Crayon Green', a costume): the very same pictures as before, '_g' on their names
    G_ = {}
    pf, _ = _p_body(False); pb, _ = _p_body(True)
    G_['dd_body'], keep = pf.done(zlib.crc32(b'dd_body') & 0xffff)
    G_['dd_body_b'] = pb.done((zlib.crc32(b'dd_body') + 1) & 0xffff, alpha=keep)[0]
    pb, _ = _p_head(back=True)
    G_['dd_head_b'], keep = pb.done(31)
    G_['dd_face'] = _p_head(None)[0].done(32, alpha=keep)[0]
    for i, k in enumerate(FACES):
        G_[f'dd_face_{k}'] = _p_head(k)[0].done(33 + i, alpha=keep)[0]
    G_['dd_arm'] = _p_arm()[0].done(41)[0]
    G_['dd_leg'] = _p_leg()[0].done(42)[0]
    G_['dd_wing'] = _p_wing()[0].done(43)[0]
    G_['dd_tail'] = _p_tail()[0].done(44)[0]
    T.update({k + OG_TEX: v for k, v in G_.items()})
    # the Doodle Creeper (a costume): '_cp' on the names (phase138 recolours them as a set of their own) - and '_cpw', the same
    # pictures in his white flash (swelling up to go off; never recoloured)
    C_ = {}
    pf, _ = _cr_body(False); pb, _ = _cr_body(True)
    C_['dd_body'], keep = pf.done(1051)
    C_['dd_body_b'] = pb.done(1052, alpha=keep)[0]
    pb, _ = _cr_picture_head(back=True)
    C_['dd_head_b'], keep = pb.done(1053)
    C_['dd_face'] = _cr_picture_head(None)[0].done(1054, alpha=keep)[0]
    for i, k in enumerate(FACES):
        C_[f'dd_face_{k}'] = _cr_picture_head(k)[0].done(1055 + i, alpha=keep)[0]
    C_['dd_leg'] = _cr_leg()[0].done(1070)[0]
    T.update({k + CR_TEX: v for k, v in C_.items()})
    T.update({k + CR_TEX + 'w': _flash(v) for k, v in C_.items()})
    # the effects - shared by both drawings
    T['dd_fire_s'] = _p_fire_side().done(45)[0]
    T['dd_fire_t'] = T['dd_fire_s'].rotate(90, expand=False)   # (the same flame for the flat card: its tip toward the image's top)
    T['dd_fire_f'] = _p_fire_burst().done(46)[0]
    T['dd_puff'] = _p_puff().done(47)[0]
    T['dd_kindle'] = _p_puff(True).done(50)[0]
    T['dd_fx_fire'] = _p_fx_fire().done(51)[0]
    T['dd_fx_smoke'] = _p_fx_smoke().done(52)[0]
    T['dd_slash'] = _p_slash().done(48)[0]
    T['dd_boom'] = _p_boom().done(49)[0]
    # the Doodle Creeper's effects: the spark breath, the hiss, the hiccup puff, the KABOOM, the pop, the stomp's dust
    T['dd_fire_s_cp'] = _p_cr_cone().done(1071)[0]
    T['dd_fire_t_cp'] = T['dd_fire_s_cp'].rotate(90, expand=False)
    T['dd_fire_f_cp'] = _p_cr_burst().done(1072)[0]
    T['dd_kindle_cp'] = _p_cr_hiss().done(1073)[0]
    T['dd_puff_cp'] = _p_cr_puff().done(1074)[0]
    T['dd_kaboom_cp'] = _p_cr_kaboom().done(1075)[0]
    T['dd_slash_cp'] = _p_cr_pop().done(1076)[0]
    T['dd_boom_cp'] = _p_cr_boom().done(1077)[0]
    _TEX.update(T)
    return dict(T)


# (3.0a) the wardrobe's recolours (phase138.RECOL's list): every drawn texture of his but the eyes (they keep their purple glow)
# and the effects; the OG's '_g' set recoloured as a set of its own (phase138: a name ending '_g', as Ava's ghost)
_LOOK = ('dd_body', 'dd_body_b', 'dd_head_b', 'dd_arm', 'dd_leg', 'dd_wing', 'dd_tail', 'dd_face') + tuple(f'dd_face_{k}' for k in FACES)
_LOOK_CR = ('dd_body', 'dd_body_b', 'dd_head_b', 'dd_leg', 'dd_face') + tuple(f'dd_face_{k}' for k in FACES)
LOOK_CR = tuple(n + CR_TEX for n in _LOOK_CR)      # (the Doodle Creeper's: phase138.OWN_SETS, a set of its own; never his flash)
LOOK_TEX = _LOOK + tuple(n + OG_TEX for n in _LOOK) + LOOK_CR
SHINY_SETS = {'dd_cp': charged}                    # (3.0b, phase138: his shiny look, the creeper's set - a charged creeper, not a recolour)
EYES_LIGHT = 15


# ---------------------------------------------------------------------------------------------------- models
def card(box, z, front, back, pv, mirror=False):
    """a picture on a card in the page (an xy plane at z): its front face and its back face, the back the same shape seen from behind"""
    x0, y0, s = box
    if mirror: x0 = -(x0 + s)
    uf, ub = ([16, 0, 0, 16], [0, 0, 16, 16]) if mirror else ([0, 0, 16, 16], [16, 0, 0, 16])
    return [el((x0, y0, z - DZ), (x0 + s, y0 + s, z - DZ), front, pv, faces=('north',), uv={'north': uf}),
            el((x0, y0, z + DZ), (x0 + s, y0 + s, z + DZ), back, pv, faces=('south',), uv={'south': ub})]


EYE_DZ = 0.12                                      # (the eye card: this far in front of the face - well clear of z-fighting)


def eyecard(box, z, tex, pv):
    """the eyes, aglow: toward whoever he faces - and its back too, so the ender particles drifting off him show from behind
    (his eyes there are behind his head)"""
    x0, y0, s = box
    return el((x0, y0, z), (x0 + s, y0 + s, z), tex, pv, faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]}, light=EYES_LIGHT)


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    for sfx, tx in (('', ''), (OG_SFX, OG_TEX)):              # (3.0a: the Ender drawing; the OG green one, its costume)
        part('dd_body' + sfx, card(BOX['body'][0], ZB, 'dd_body' + tx, 'dd_body_b' + tx, PIVOT['body']))
        for fc in (None,) + FACES:
            nm, face = (f'dd_head_x{fc}', f'dd_face_{fc}') if fc else ('dd_head', 'dd_face')
            els = card(BOX['head'][0], ZH, face + tx, 'dd_head_b' + tx, PIVOT['head'])
            if not sfx:                                       # (his eyes: a glowing card just in front of his face)
                els.append(eyecard(BOX['head'][0], ZH - DZ - EYE_DZ, 'dd_eyes' + (f'_{fc}' if fc else ''), PIVOT['head']))
            part(nm + sfx, els)
        for p, tex in (('armr', 'dd_arm'), ('legr', 'dd_leg'), ('wingr', 'dd_wing')):
            box, z = BOX[p]
            part(f'dd_{p}{sfx}', card(box, z, tex + tx, tex + tx, PIVOT[p]))
            q = p[:-1] + 'l'
            part(f'dd_{q}{sfx}', card(box, z, tex + tx, tex + tx, PIVOT[q], mirror=True))
        part('dd_tail' + sfx, card(BOX['tail'][0], ZT, 'dd_tail' + tx, 'dd_tail' + tx, PIVOT['tail']))
    for sfx, tx in ((CR_SFX, CR_TEX), (CR_SFX + 'w', CR_TEX + 'w')):   # the Doodle Creeper - and his white flash
        part('dd_body' + sfx, card(BOX['body'][0], ZB, 'dd_body' + tx, 'dd_body_b' + tx, PIVOT['body']))
        for fc in (None,) + FACES:
            nm, face = (f'dd_head_x{fc}', f'dd_face_{fc}') if fc else ('dd_head', 'dd_face')
            part(nm + sfx, card(BOX['head'][0], ZH, face + tx, 'dd_head_b' + tx, PIVOT['head']))
        box, z = BOX['legr']
        part('dd_legr' + sfx, card(box, z, 'dd_leg' + tx, 'dd_leg' + tx, PIVOT['legr']))
        part('dd_legl' + sfx, card(box, z, 'dd_leg' + tx, 'dd_leg' + tx, PIVOT['legl'], mirror=True))
    for p in CR_GONE:                                                 # (3.0b: the parts a creeper hasn't got - nothing at all; in the game the
        M['dd_' + p + CR_SFX] = ({'dd_body_cp': 'bm:block/dd_body_cp'}, [])   #  form puts these on, so no pose's scale brings a wing back;
                                                                        #  a texture named all the same: its particle)
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
    # the Doodle Creeper's: the spark breath (the same cross of cards and a burst), the hiss, the hiccup, and the KABOOM round all of him
    side_c = [dict(e, faces={f: dict(v, texture='#dd_fire_s_cp') for f, v in e['faces'].items()}) for e in side]
    flat_c = [dict(e, faces={f: dict(v, texture='#dd_fire_t_cp') for f, v in e['faces'].items()}) for e in flat]
    part('dd_fire_fire' + CR_SFX, shrink(side_c + flat_c + card((mx + bx, my + by, bs), mz - 1.1, 'dd_fire_f_cp', 'dd_fire_f_cp', fp), k))
    part('dd_fire_kindle' + CR_SFX, shrink(card(PUFF_BOX, mz - 0.5, 'dd_kindle_cp', 'dd_kindle_cp', fp), k))
    part('dd_fire_puff' + CR_SFX, shrink(card(PUFF_BOX, mz - 0.5, 'dd_puff_cp', 'dd_puff_cp', fp), k))
    part('dd_fire_kaboom' + CR_SFX, shrink(card(KABOOM_BOX, ZA - 1.4, 'dd_kaboom_cp', 'dd_kaboom_cp', fp), k))
    M['dd_fire'] = M['dd_fire_fire']
    # the breath's effect, for the datapack: a crayon flame and a scribble of smoke, each a little card to show (or to burst into)
    for k_ in ('fire', 'smoke'):
        part(f'dd_fx_{k_}', card((-4.0, 0.0, 8.0), 0.0, f'dd_fx_{k_}', f'dd_fx_{k_}', (0.0, 4.0, 0.0)))
    A = PIVOT['slash']
    part('dd_slash', card(SLASH_BOX, ZA - 0.35, 'dd_slash', 'dd_slash', A))
    part('dd_boom', card(BOOM_BOX, ZA - 0.6, 'dd_boom', 'dd_boom', PIVOT['boom']))
    part('dd_slash' + CR_SFX, card(SLASH_BOX, ZA - 0.35, 'dd_slash_cp', 'dd_slash_cp', A))
    part('dd_boom' + CR_SFX, card(BOOM_BOX, ZA - 0.6, 'dd_boom_cp', 'dd_boom_cp', PIVOT['boom']))
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
    # (3.0a: the wing under him folded up along his back and his tail curled up off the floor - he lies on his arm, in both drawings)
    'tired': P(_face='dizzy', body=roll(88), head=roll(10), armr=limb(1, 0, 20), arml=limb(-1, 0, 50), legr=limb(1, 0, 10), legl=limb(-1, 0, 26),
               wingr=limb(1, 0, -20), wingl=limb(-1, 0, 80), **tail(70)),
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
def _pts(p, geo=GEO):
    """a card's outline points (design units, its own layer)"""
    src = MIRROR.get(p, p)
    if src not in geo: return []
    z = BOX[src][1]; sx = -1 if p in MIRROR else 1
    return [(sx * x, y, z) for poly in geo[src] for x, y in poly[::2]]


_PTS = {p: _pts(p) for p in PARTS}
_PTS_CR = {p: _pts(p, GEO_CR) for p in PARTS}      # (the Doodle Creeper: his own outlines - and nothing of the parts he hasn't got)


def lowest(pose):
    """the lowest point of him in this pose (design units) - every card but the effects"""
    xf = solve(PIVOT, PARENT, pose); low = 1e9
    for p, pts in (_PTS_CR if _cr(pose) else _PTS).items():
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

# (the Doodle Creeper) his own moves, on the same rig: the creeper's swell - a crouch, cheeks puffed (swell_0), then puffed up
# and flashing white (swell_1, '_crw'; '_swell': the whole rig shown this much bigger - in the game the displays' scale, as
# rigpet's grow) - KABOOM (the cloud round all of him: the fire part's 'kaboom') - and scribbling himself back together
CR_POSES = {
    'swell_0': P(_cr=True, _face='puff', body=qs(('x', -6)), head=qs(('x', -4)), legr=limb(1, 0, 10), legl=limb(-1, 0, 10)),
    'swell_1': P(_crw=True, _swell=1.16, _face='puff', head=qs(('x', 4)), legr=limb(1, 0, 14), legl=limb(-1, 0, 14)),
    'kaboom': P(_crw=True, _swell=1.2, _face='roar', _fire='kaboom', legr=limb(1, 0, 18), legl=limb(-1, 0, 18)),
    'reform': P(_cr=True, _face='dizzy', _fire='puff', body=roll(-6), head=roll(10), legr=limb(1, 0, 8), legl=limb(-1, 0, -4)),
}
# (a shared pose he'd float in - he has no arm or wing to lie on: 'tired' - his own, grounded on him; the game picks it in this form)
CR_POSES['tired'] = dict(POSES['tired'], _cr=True)
for _k in CR_POSES:
    CR_POSES[_k] = _ground(CR_POSES[_k])
CR_DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired', 'flap_0', 'swim_0']
