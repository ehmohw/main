"""2.95e: THE GEM'S BUDDIES - the ten the Gem of Creativity conjures for a moment to fight beside it, each a small 3D rig in the
pack's blocky follower style (the owner's drawings are the design reference only - shapes, colours and FACES - never the textures):

  GRACE      a hummingbird: yellow-green, a pink crest and a pink throat stripe, a long dark beak; small white eyes, tall pupils.
                                                                                             flap / DIVE-PECK
  ROBO       a boxy grey robot: a red dot of a nose and a crooked cream grin; his eyes on STALKS (a big one, a little one) and a
             curly antenna with a red bulb; a trapezoid chest with a panel; long arms with C-clamp hands; jet boots.
                                                                                             STOMP / ROCKET PUNCH
  ZAPPER     an unevenly rounded little body with jagged lightning spikes all the way round (2.96c - not a bolt; the long bolt
             in the drawing is an arm he stretches out to light Dessa up), pale blue glints between the spikes; round white eyes
             glancing sideways under a raised brow, a green gem of a nose, a wavy unsure little mouth.   curious bob / ZAP
  DESSA      a light bulb, eyes closed in two happy arches, a wavy little smile; arms of light; a screw base.
                                                                                             flicker / FLASH-BURST
  BUBBLES    a PAIR of bubbles: the big one with two tall dark eyes and a great round open mouth, its little one beside it.
                                                                                             bounce in tandem / POP-SPLASH
  CHASE      a glossy green gummy: three round lobes on top of him, big hollow white eyes - no pupils -
             no nose, one eye a little the bigger, a wide toothy grin; his lower half is his head upside down - three lobes on
             top and three below, round his middle like an octopus's tentacles (those below his arms, too); he floats.
                                                                                             squash-and-stretch hop / TACKLE
  LIMER      the round fellow - a pale ball with sleepy lidded eyes, a big curl of a nose and a little "o" of a mouth - in his
             loopy green covering, on stick legs.                                            roll / BODY SLAM
  CHICO      a drumstick: worried brows, shiny black eyes, an open fretful mouth; crispy at the bottom, the bone his body.
                                                                                             wobble / SWING-WHACK
  SPIKE      a circular saw: a ring of hooked steel teeth round a glossy black hub with an angry face - heavy brows, a jagged
             fanged grin.                                                                    spin up / BUZZ-SAW DASH
  CHEFERONI  a whole pizza: crust, cheese, slices and pepperoni; angry brows, a great curly moustache over an open mouth, a
             curl of hair, a tilted chef's hat; thin black arms, long yellow legs.           toss the dough / SLICE THROW

Each is a rigkit rig (an object with PREFIX, PIVOT, PARENT, PARTS, POSES, HIDDEN, model_name, models, textures, RIG_SCALE): RIGS
below, by name. Design units: feet at y=0, facing -z, its right is +x. Every one has the poses appear (popping out of a sparkle),
idle_a, idle_b, its wind-up and strike, happy and vanish; GROW gives the display scale through appear/vanish (they pop in small and
pop out small). Faces are a model per expression on the part with the face (pose key _face); some parts have a variant shape (pose
key _v: {part: variant} - Chase's squash and stretch, Bubbles' pop, Dessa's lit glass).

(2.95e, reworked after the owner's look: every face is that Buddy's own, drawn from the owner's art - no shared eye or mouth -
painted at 16 px a unit and smoothed (drawn 4x over and brought down), so the lines stay clean; the coats are smooth, softly lit
colour, not 2-px noise. Zapper, Spike and Chase were rebuilt to the drawings' shapes.)"""
import math
import random
from types import SimpleNamespace
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg, chain, euler

GROW = {'appear': (0.15, 1.15, 1.0), 'vanish': (1.0, 1.2, 0.0)}     # (the display's scale, keyframe by keyframe)
def T(*r):
    """a trunk's turn (body, head, core...): ('x', -a) leans it FORWARD (nose down), ('x', +a) back"""
    return qs(*[(a, -d if a == 'x' else d) for a, d in r])


def L(*r):
    """a limb's turn (arms, legs, wings, lobes): ('z', +a) swings it OUT and up on its own side (the right one; the left mirrors with -a)"""
    return qs(*[(a, -d if a == 'z' else d) for a, d in r])


FACES = ('blink', 'happy', 'fierce', 'wow', 'look')
DRAFT = ['appear', 'idle_a', 'idle_b', 'wind', 'strike', 'happy', 'vanish']
PPU, SS = 16, 4                    # (face textures: 16 px a unit, 256 px over 16 units; drawn SS times over, then brought down)


# ==================================================================================================== painting
def _field(seed, n, size):
    rnd = random.Random(seed); g = [[rnd.random() for _ in range(n + 1)] for _ in range(n + 1)]
    out = [[0.0] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            fx, fy = x / size * n, y / size * n; ix, iy = int(fx), int(fy); tx, ty = fx - ix, fy - iy
            tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
            a = g[iy][ix] * (1 - tx) + g[iy][ix + 1] * tx; b = g[iy + 1][ix] * (1 - tx) + g[iy + 1][ix + 1] * tx
            out[y][x] = a * (1 - ty) + b * ty
    return out


def tex(col, seed, var=0.04, cell=None, size=64, spots=None, n=5, pix=True):
    """a coat: one colour, varied over broad areas. (2.96d, the owner's ask - the blocky, cobblestone look of the pack's other
    models:) pix - painted in square cells half a design unit across, each its own shade, a few darker and lighter (as a vanilla
    block is); pix=False - smooth, as Robo keeps. spots: [(colour, p)] - flecks"""
    im = Image.new('RGBA', (size, size)); px = im.load(); c = hexc(col); f = _field(seed, n, size)
    if pix:
        cz = cell or max(2, size // 32); r = random.Random(seed * 31 + 5); v2 = max(var, 0.05)
        for cy in range(0, size, cz):
            for cx in range(0, size, cz):
                k = 1 + (f[cy][cx] - 0.5) * 2 * var + r.uniform(-1, 1) * v2 * 0.9
                q = r.random()
                if q < 0.07: k *= 0.88
                elif q < 0.11: k *= 1.08
                col_ = tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
                for y in range(cy, min(size, cy + cz)):
                    for x in range(cx, min(size, cx + cz)):
                        px[x, y] = col_
    else:
        for y in range(size):
            for x in range(size):
                k = 1 + (f[y][x] - 0.5) * 2 * var
                px[x, y] = tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
    if spots:
        d = ImageDraw.Draw(im); r = random.Random(seed + 7)
        for sc, p in spots:
            for _ in range(int(p * size * size / 14)):
                x, y, s = r.uniform(0, size), r.uniform(0, size), r.uniform(size / 64, size / 30)
                if pix:                                       # (square flecks, on the cells)
                    cz = cell or max(2, size // 32); x, y = int(x) // cz * cz, int(y) // cz * cz; k = max(1, int(s * 2 / cz + 0.5)) * cz
                    d.rectangle((x, y, x + k - 1, y + k - 1), fill=hexc(sc))
                else:
                    d.ellipse((x - s, y - s * 0.8, x + s, y + s * 0.8), fill=hexc(sc))
    return im


def lit(im, w, h, ppu=4, hi='#ffffff', a=110, rim=None, rim_a=150, pix=True):
    """light from the upper left over the (w x h unit) window at the top left of a texture, a darker rim at the lower right
    (pix: worked out cell by cell and in a few steps - pixel-art shading; pix=False smooth, as Robo keeps)"""
    px = im.load(); W, H = int(w * ppu), int(h * ppu)
    cz = max(1, im.width // 32) if pix else 1
    for y in range(min(H, im.height)):
        for x in range(min(W, im.width)):
            sx, sy = (x // cz * cz + cz / 2, y // cz * cz + cz / 2) if pix else (x + 0.5, y + 0.5)
            u, v = sx / W - 0.32, sy / H - 0.28
            g = max(0.0, 1 - math.hypot(u * 1.6, v * 1.6) * 1.6)
            if pix: g = round(g * 4) / 4
            c = px[x, y]
            if g > 0:
                t = hexc(hi); k = g * a / 255
                c = tuple(int(c[i] * (1 - k) + t[i] * k) for i in range(3)) + (255,)
            if rim:
                e = max(0.0, sx / W + sy / H - 1.45) * 2.2
                if pix: e = round(min(1.0, e) * 3) / 3
                if e > 0:
                    t = hexc(rim); k = min(1.0, e) * rim_a / 255
                    c = tuple(int(c[i] * (1 - k) + t[i] * k) for i in range(3)) + (255,)
            px[x, y] = c
    return im


# ---- drawing (on the 4x canvas: every size is a fraction of the face box, so each face scales cleanly)
def E(d, cx, cy, rx, ry, fill=None, outline=None, w=0):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=hexc(fill) if fill else None, outline=hexc(outline) if outline else None, width=int(w))


def ln(d, pts, col, w):
    """a stroke with round ends and joints"""
    w = max(1, int(w)); d.line(pts, fill=hexc(col), width=w, joint='curve')
    for x, y in (pts[0], pts[-1]): d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=hexc(col))


def clip(cx, cy, rx, ry, keep, n=96):
    """the part of an ellipse where keep(x, y) holds, as a polygon (a lid, an eye cut by a brow)"""
    pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return [p_ for p_ in pts if keep(*p_)]


def bez(*p, n=24):
    """a Bezier curve's points (3 or 4 control points)"""
    out = []
    for i in range(n + 1):
        t = i / n
        if len(p) == 3:
            out.append(tuple((1 - t) ** 2 * p[0][k] + 2 * (1 - t) * t * p[1][k] + t * t * p[2][k] for k in range(2)))
        else:
            out.append(tuple((1 - t) ** 3 * p[0][k] + 3 * (1 - t) ** 2 * t * p[1][k] + 3 * (1 - t) * t * t * p[2][k] + t ** 3 * p[3][k] for k in range(2)))
    return out


def arc(cx, cy, rx, ry, a0, a1, n=24):
    """points round an ellipse from a0 to a1 degrees (0 = right, 90 = down - image coordinates)"""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def face_tex(base, w, h, paint, seed=1, var=0.03, hi=110, rim=None, rim_a=150, under=None, rot=0.0, pix=True):
    """a face texture (256 px, 16 px a unit): the base colour softly lit over the w x h unit window at its top left (a ball's
    whole front, say), then paint(draw, W, H) draws the face over that same window on a canvas SS times the size - brought down
    smoothly. under(draw, W, H): painted on the base before the light (a pizza's toppings, a robot's panel)"""
    size = 256
    im = tex(base, seed, var, size=size, n=4, pix=pix)
    W, H = int(w * PPU * SS), int(h * PPU * SS)
    if under:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); under(ImageDraw.Draw(lay), W, H)
        im.alpha_composite(lay.resize((int(w * PPU), int(h * PPU)), Image.LANCZOS), (0, 0))
    lit(im, w, h, PPU, a=hi, rim=rim, rim_a=rim_a, pix=pix)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); paint(ImageDraw.Draw(lay), W, H)
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC)          # (a face kept upright on a part that leans)
    im.alpha_composite(lay.resize((int(w * PPU), int(h * PPU)), Image.LANCZOS), (0, 0))
    return im


# ==================================================================================================== the rig builder
class Rig:
    """collects one Buddy's parts: rig.part(name, pivot, parent, builder) where builder(variant, face) -> elements;
    variants and faces are listed per part. rig.ns() -> the rigkit rig object."""

    def __init__(self, prefix, scale=1.0):
        self.prefix, self.scale = prefix, scale
        self.PIVOT, self.PARENT, self.B, self.VARS, self.FACED, self.T, self.POSES = {}, {}, {}, {}, set(), {}, {}

    def part(self, name, pivot, parent, builder, variants=(), faced=False):
        self.PIVOT[name], self.PARENT[name], self.B[name], self.VARS[name] = pivot, parent, builder, tuple(variants)
        if faced: self.FACED.add(name)

    def t(self, key, im):
        self.T[self.prefix + key] = im
        return self.prefix + key

    def fk(self, f, key='face'):
        """the texture name of a face: face, face_<expr>"""
        return self.prefix + key + (f'_{f}' if f else '')

    def ns(self):
        P, prefix = self, self.prefix

        def HIDDEN(p, pose):
            return p in pose.get('_hide', ())

        def model_name(p, pose, suffix=''):
            v = pose.get('_v', {}).get(p)
            v = f'_v{v}' if v and v in P.VARS[p] else ''
            f = f'_x{pose["_face"]}' if p in P.FACED and pose.get('_face') else ''
            return f'{prefix}{p}{v}{f}{suffix}'

        def models():
            M = {}
            for p in P.PIVOT:
                for v in (None,) + P.VARS[p]:
                    for f in ((None,) + FACES if p in P.FACED else (None,)):
                        els = P.B[p](v, f)
                        used = sorted({e['faces'][k]['texture'][1:] for e in els for k in e['faces']})
                        M[f'{prefix}{p}' + (f'_v{v}' if v else '') + (f'_x{f}' if f else '')] = ({t: f'bm:block/{t}' for t in used}, els)
            return M
        return SimpleNamespace(PREFIX=prefix, PIVOT=dict(P.PIVOT), PARENT=dict(P.PARENT), PARTS=tuple(P.PIVOT), PART_K={},
                               POSES=P.POSES, DRAFT=DRAFT, FACES=FACES, HIDDEN=HIDDEN, model_name=model_name, models=models,
                               textures=lambda: (models(), dict(P.T))[1],          # (some textures are made as the models are)
                               RIG_SCALE=P.scale, GROW=GROW, UP=(0.0, 1.0, 0.0), FRONT=(0.0, 0.0, -1.0))


def ball(c, r, tex_, pv, yr=None, zr=None, shift=(0.0, 0.0), light=0, face=None, n=7, smooth=False):
    """a round ball, sliced: layers, each a cross of two boxes as wide as the sphere is there - round from every side.
    face: a texture painted over the whole front (the window 2r x 2yr at the top left of it) - laid over the front of every
    slice at its own depth, so the face sits ON the ball. (2.96d, the blocky look: a block - a vanilla mob's head, a slime -
    its face over the whole front; smooth=True, the n fine slices Robo keeps)"""
    x, y, z = c; ry, rz = yr or r, zr or r
    if not smooth:                                    # (2.96d, the owner's word: round Buddies needn't be round - a block, its face on the front)
        k = 0.9
        e = el((x - r * k, y - ry * k, z - rz * k), (x + r * k, y + ry * k, z + rz * k), tex_, pv, shift=shift, light=light)
        if face:
            e['faces']['north'] = {'uv': [0, 0, round(2 * r, 4), round(2 * ry, 4)], 'texture': '#' + face}
        return [e]
    out = []
    for i in range(n):
        y0 = y - ry + i * 2 * ry / n; y1 = y0 + 2 * ry / n
        near = 0.0 if y0 < y < y1 else min(abs(y0 - y), abs(y1 - y))
        if smooth:
            f = max(0.38, math.sqrt(max(0.0, 1 - (near / ry) ** 2)))
        else:
            mid = abs((y0 + y1) / 2 - y)
            f = max(0.5, round(math.sqrt(max(0.0, 1 - (mid / ry) ** 2)) * 8) / 8)
        for j, (kx, kz) in enumerate(((f, f * 0.74), (f * 0.74, f))):
            e = el((x - r * kx, y0, z - rz * kz), (x + r * kx, y1, z + rz * kz), tex_, pv, shift=(shift[0] + 0.13 * i + 0.4 * j, shift[1] + 0.29 * i), light=light)
            if face:
                x0, x1 = x - r * kx, x + r * kx
                e['faces']['north'] = {'uv': [round((x + r) - x1, 4), round((y + ry) - y1, 4), round((x + r) - x0, 4), round((y + ry) - y0, 4)], 'texture': '#' + face}
            out.append(e)
    return out


def pear(y0, h, radii, tex_, pv, zk=0.8, n=9, light=0):
    """(2.96c) a pear standing on its base at y0, h tall, sliced as a ball is (a cross of two boxes a layer): radii = (at the
    base, at the widest - a quarter of the way up - and at the top), the sides easing between them"""
    rb, rm, rt = radii
    out = []
    for i in range(n):
        a, b = y0 + i * h / n, y0 + (i + 1) * h / n
        t = (i + 0.5) / n
        if t < 0.25:
            r = rb + (rm - rb) * math.sin(t / 0.25 * math.pi / 2)
        else:
            u = (t - 0.25) / 0.75
            r = rt + (rm - rt) * (0.5 + 0.5 * math.cos(u * math.pi))
        for j, (kx, kz) in enumerate(((1.0, 0.74), (0.74, 1.0))):
            out.append(el((-r * kx, a, -r * zk * kz), (r * kx, b, r * zk * kz), tex_, pv, shift=(0.13 * i + 0.4 * j, 0.29 * i), light=light))
    return out


def disc(c, r, th, tex_, pv, face=None, n=9, light=0, smooth=False):
    """a flat round disc standing up, facing front (a pizza, a saw's hub): strips across, the face over the front of all of them
    (2.96d: five chunky strips - the blocky look; smooth=True, n fine ones)"""
    x, y, z = c; out = []
    if not smooth:                                    # (2.96d: a square slab - the blocky look)
        k = 0.9
        e = el((x - r * k, y - r * k, z - th), (x + r * k, y + r * k, z + th), tex_, pv, light=light)
        if face:
            e['faces']['north'] = {'uv': [0, 0, round(2 * r, 4), round(2 * r, 4)], 'texture': '#' + face}
        return [e]
    for i in range(n):
        y0 = y - r + i * 2 * r / n; y1 = y0 + 2 * r / n
        near = 0.0 if y0 < y < y1 else min(abs(y0 - y), abs(y1 - y))
        f = max(0.3, math.sqrt(max(0.0, 1 - (near / r) ** 2)))
        e = el((x - r * f, y0, z - th), (x + r * f, y1, z + th), tex_, pv, shift=(0.11 * i, 0.23 * i), light=light)
        if face:
            e['faces']['north'] = {'uv': [round(r - r * f, 4), round((y + r) - y1, 4), round(r + r * f, 4), round((y + r) - y0, 4)], 'texture': '#' + face}
        out.append(e)
    return out


def plate(fr, to, tex_, pv, w, h, light=0, rot=None):
    """a face plate on the front (north) of a box: the window w x h units at the top left of the face texture"""
    return el(fr, to, tex_, pv, faces=('north',), uv={'north': [0, 0, w, h]}, light=light, rot=rot)


def _rm(ax, ay, az):
    """Rz Ry Rx (degrees) as rows"""
    a, b, c = (math.radians(v) for v in (ax, ay, az))
    Rx = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    Ry = [[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]
    Rz = [[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(Rz, mm(Ry, Rx))


def turn(els, ang, origin):
    """turn a group of elements (model units out of el()) by Euler angles ang=(x, y, z) about a design-unit origin - each
    element's own turn composed with it (a baked tilt: a cocked hat, a leaning bolt)"""
    R = _rm(*ang); out = []
    for e in els:
        e = dict(e); fr, to = e['from'], e['to']
        if 'rotation' in e:
            r0 = e['rotation']; o = r0['origin']
            R0 = _rm(r0.get('x', 0), r0.get('y', 0), r0.get('z', 0)) if 'axis' not in r0 else _rm(*[r0['angle'] if r0['axis'] == k else 0 for k in 'xyz'])
        else:
            o = [(fr[i] + to[i]) / 2 for i in range(3)]; R0 = _rm(0, 0, 0)
        O = origin                                          # (model units, as mo() gives it)
        v = [o[i] - O[i] for i in range(3)]
        o2 = [sum(R[i][k] * v[k] for k in range(3)) + O[i] for i in range(3)]
        dlt = [o2[i] - o[i] for i in range(3)]
        e['from'] = [round(fr[i] + dlt[i], 4) for i in range(3)]; e['to'] = [round(to[i] + dlt[i], 4) for i in range(3)]
        Rn = [[sum(R[i][k] * R0[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        ax, ay, az = euler(Rn)
        e['rotation'] = {'origin': [round(v_, 4) for v_ in o2], 'x': ax, 'y': ay, 'z': az}
        out.append(e)
    return out


def mo(p, pv):
    """a design point -> model units for the part with joint pv (what el() does to a point)"""
    return [p[i] + 8 - pv[i] for i in range(3)]


# ==================================================================================================== GRACE - the hummingbird
def grace():
    R = Rig('gz_grace_', 1.0)
    G, GD, HEAD, PINK, PINKL, BEAK, INK = '#4e9a24', '#2c6a14', '#8cc63a', '#de5cb4', '#f2a0dc', '#3e3a34', '#162410'
    body = R.t('body', lit(tex(G, 11, 0.06), 6, 6, 4, a=70, rim=GD))
    headc = R.t('head', lit(tex(HEAD, 12, 0.05), 4.4, 4.0, 4, a=90, rim='#5a9a24', rim_a=90))
    throat = R.t('throat', tex(PINK, 18, 0.05, spots=[(PINKL, 0.08)]))
    wing, wing2 = R.t('wing', tex(G, 13, 0.06, spots=[('#6ab634', 0.1)])), R.t('wing_d', tex(GD, 14, 0.05))
    crest = R.t('crest', tex(PINK, 15, 0.06, spots=[(PINKL, 0.25)]))
    beak = R.t('beak', lit(tex(BEAK, 16, 0.04), 2, 8, 4, hi='#9a968a', a=120))

    def eye(d, W, H, cx, cy, s, f, side):
        """her eye: black, with a bit of white shine; startled ('wow') as drawn - a white oval, a tall dark pupil set toward the
        beak, a crease behind it"""
        lw = s * 0.16
        if f == 'blink':
            ln(d, arc(cx, cy - s * 0.2, s * 0.6, s * 0.55, 20, 160), INK, lw); return
        if f == 'happy':
            ln(d, arc(cx, cy + s * 0.5, s * 0.6, s * 0.75, 200, 340), INK, lw); return
        if f != 'wow':                     # (2.96d, the owner's word: her eyes are just black, with a bit of white shine - the
            rx, ry = s * 0.42, s * (0.5 if f == 'fierce' else 0.6)          #  drawing's wide white eye is her startled one)
            lx = {'look': -side * 0.12}.get(f, 0.0) * s
            E(d, cx + lx, cy, rx, ry, '#120e08')
            E(d, cx + lx - rx * 0.35, cy - ry * 0.4, rx * 0.32, rx * 0.32, '#ffffff'); E(d, cx + lx + rx * 0.3, cy + ry * 0.35, rx * 0.13, rx * 0.13, '#ffffff')
            if f == 'fierce':
                ln(d, [(cx - side * s * 0.9, cy - s * 0.95), (cx + side * s * 0.7, cy - s * 0.45)], INK, s * 0.26)
            return
        rx, ry = s * 0.62, s * 0.95
        E(d, cx, cy, rx, ry, '#fafaf2', INK, lw)
        lx = {'look': -side * 0.22}.get(f, side * 0.14) * s
        pr = (s * 0.14, s * 0.24) if f == 'wow' else (s * 0.2, s * 0.5 if f != 'fierce' else s * 0.38)
        E(d, cx + lx, cy + s * 0.06, pr[0], pr[1], '#141008')
        E(d, cx + lx - pr[0] * 0.3, cy - pr[1] * 0.45, pr[0] * 0.4, pr[0] * 0.4, '#ffffff')
        a0 = 125 if side > 0 else -55
        ln(d, arc(cx, cy, rx + s * 0.4, ry + s * 0.18, a0, a0 + 90, n=12), INK, s * 0.09)                       # (the crease behind)
        if f == 'fierce':
            ln(d, [(cx - side * s * 1.0, cy - s * 1.15), (cx + side * s * 0.8, cy - s * 0.55)], INK, s * 0.26)

    def face(f):
        def p(d, W, H):
            s = W * 0.11
            eye(d, W, H, W * 0.22, H * 0.4, s, f, 1)
            eye(d, W, H, W * 0.78, H * 0.4, s, f, -1)
        return R.t(f'face{"_" + f if f else ""}', face_tex(HEAD, 4.4, 4.0, p, seed=17, hi=90, rim='#5a9a24', rim_a=90))
    for f in (None,) + FACES: face(f)
    HY = 13.0
    R.part('body', (0, 9.0, 0), None, lambda v, f: [
        *ball((0, 9.0, 0.6), 2.4, body, (0, 9.0, 0), yr=2.6, zr=3.0),
        el((-0.7, 7.4, -2.62), (0.7, 10.9, -2.2), throat, (0, 9.0, 0), faces=('north', 'east', 'west', 'up', 'down'))])     # (the pink stripe)
    R.part('head', (0, 11.4, -1.4), 'body', lambda v, f: [
        *ball((0, HY, -2.0), 2.2, headc, (0, 11.4, -1.4), yr=2.0, zr=2.0, shift=(0.4, 0.1), face=R.fk(f)),
        *chain([(0, HY - 0.4, -3.8), (0, HY - 1.0, -6.6), (0, HY - 2.1, -9.2), (0, HY - 3.3, -10.8)], [0.75, 0.6, 0.42], 0.6, beak, (0, 11.4, -1.4)),   # (long, curving down, as drawn)
        el((-0.7, HY - 2.0, -3.6), (0.7, HY - 1.2, -2.6), throat, (0, 11.4, -1.4)),                                  # (pink under the chin)
        *chain([(0, HY + 1.8, -1.6), (0, HY + 4.6, 0.4), (0, HY + 5.4, 3.4)], [1.8, 1.0], 0.7, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0)),       # (the crest: a fan
        *chain([(0.8, HY + 1.6, -1.0), (1.7, HY + 4.0, 0.8), (2.2, HY + 4.4, 3.2)], [1.4, 0.8], 0.6, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0)),       #  of feathers swept
        *chain([(-0.8, HY + 1.6, -1.0), (-1.7, HY + 4.0, 0.8), (-2.2, HY + 4.4, 3.2)], [1.4, 0.8], 0.6, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0)),    #  back off her head)
        *chain([(0, HY + 1.2, 0.4), (0, HY + 2.6, 3.2), (0, HY + 2.2, 5.6)], [1.3, 0.7], 0.6, crest, (0, 11.4, -1.4), (0.0, 1.0, 0.0))],
        faced=True)
    for s, n in ((1, 'wingr'), (-1, 'wingl')):
        pv = (s * 2.0, 10.4, 0.2)
        # (2.96d: a broad wing swept back, as drawn - tapering in blocky steps out to its tip, a darker band of coverts at the root)
        WG = ((0.0, 3.2, -1.8, 2.4), (3.2, 5.8, -1.2, 3.1), (5.8, 7.9, -0.3, 3.6))
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: [
            *[el((pv[0] + (x0 if s > 0 else -x1), pv[1] - 0.2, pv[2] + z0), (pv[0] + (x1 if s > 0 else -x0), pv[1] + 0.2, pv[2] + z1), wing, pv, shift=(0.3 * i, 0.2 * i))
              for i, (x0, x1, z0, z1) in enumerate(WG)],
            el((pv[0] + (0 if s > 0 else -4.2), pv[1] - 0.3, pv[2] - 2.0), (pv[0] + (4.2 if s > 0 else 0), pv[1] + 0.3, pv[2] + 0.4), wing2, pv)])(pv, s))
    R.part('tail', (0, 8.2, 3.2), 'body', lambda v, f: [
        *chain([(0.4, 8.2, 3.2), (1.6, 6.8, 6.8)], [1.6], 0.35, wing, (0, 8.2, 3.2), (0.0, 1.0, 0.0)),
        *chain([(-0.4, 8.2, 3.2), (-1.6, 6.8, 6.8)], [1.6], 0.35, wing2, (0, 8.2, 3.2), (0.0, 1.0, 0.0))])
    W = lambda a: dict(wingr=L(('z', a)), wingl=L(('z', -a)))        # (+a: both up)
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 1.0, 0), body=T(('y', 30)), **W(60), head=T(('x', -12))),
        'idle_a': dict(_off=(0, 1.0, 0), **W(55), tail=T(('x', 10))),
        'idle_b': dict(_face='look', _off=(0, 1.6, 0), **W(-35), head=T(('y', -24), ('z', 12)), tail=T(('x', -10))),
        'flap_0': dict(_off=(0, 1.2, 0), **W(60)), 'flap_1': dict(_off=(0, 0.8, 0), **W(-40)),
        'wind': dict(_face='fierce', _off=(0, 3.4, 1.6), body=T(('x', 30)), head=T(('x', -12)), **W(80), tail=T(('x', 20))),
        'strike': dict(_face='fierce', _off=(0, -0.6, -5.0), body=T(('x', -52)), head=T(('x', -10)), **W(-70), tail=T(('x', -30))),
        'happy': dict(_face='happy', _off=(0, 1.8, 0), body=T(('z', 14)), **W(70), head=T(('z', -10)), tail=T(('x', 18))),
        'vanish': dict(_face='happy', _off=(0, 3.0, 0), body=T(('y', -160)), **W(80)),
    })
    return R.ns()


# ==================================================================================================== ROBO - the robot
def robo():
    R = Rig('gz_robo_', 1.0)
    GREY, GREYD, GREYL, LINE, RED = '#9a9c9e', '#5e6062', '#c6c8ca', '#3c3e40', '#d42a1e'
    metal = R.t('metal', lit(tex(GREY, 21, 0.04, pix=False), 8, 8, 4, a=70, rim='#4a4c4e', pix=False))
    dark, light_ = R.t('dark', tex(GREYD, 22, 0.04, pix=False)), R.t('light', lit(tex(GREYL, 23, 0.03, pix=False), 4, 8, 4, a=60, pix=False))
    flame = R.t('flame', tex('#ffcc30', 25, 0.1, spots=[('#ff4a1a', 0.3), ('#fff8c0', 0.2)], pix=False))
    eyew = R.t('eyew', lit(tex('#eeeeec', 26, 0.02, pix=False), 2, 2, 4, a=60, rim='#a0a0a0', pix=False))
    stalk = R.t('stalk', tex('#4c4e50', 27, 0.03, pix=False))
    redb = R.t('red', lit(tex(RED, 28, 0.05, pix=False), 2, 2, 4, a=120, pix=False))

    def head_face(f):
        """his face, as drawn: a grey plate with a dark outline and a glint, a red dot of a nose, a crooked cream grin of
        squared teeth (the grin changes with his mood; his eyes are on the stalks)"""
        def p(d, W, H):
            lw = W * 0.025
            d.rounded_rectangle((lw, lw, W - lw, H - lw), radius=int(W * 0.06), outline=hexc(LINE), width=int(lw * 1.6))
            E(d, W * 0.2, H * 0.2, W * 0.07, H * 0.045, '#e8eaec'); E(d, W * 0.12, H * 0.3, W * 0.025, H * 0.025, '#e8eaec')    # (the shine)
            nr = W * (0.05 if f != 'fierce' else 0.065)
            E(d, W * 0.58, H * 0.36, nr, nr, RED if f != 'fierce' else '#ff3a1a', '#7a1410', lw * 0.7)
            E(d, W * 0.565, H * 0.345, nr * 0.35, nr * 0.35, '#ffb0a0')
            T_, S_ = '#e2daa0', '#b8ae6c'
            if f == 'wow':                                          # (his jaw dropped: a dark mouth, the teeth along its top)
                d.rectangle((W * 0.24, H * 0.52, W * 0.86, H * 0.9), fill=hexc('#2a2a2a'), outline=hexc(LINE), width=int(lw))
                d.rectangle((W * 0.26, H * 0.54, W * 0.84, H * 0.62), fill=hexc(T_))
                return
            if f == 'fierce':                                       # (clenched: a flat top, teeth set edge to edge)
                pts = [(0.22, 0.58), (0.88, 0.58), (0.88, 0.9), (0.22, 0.9)]
            elif f == 'happy':                                      # (the grin opened up wide)
                pts = [(0.2, 0.5), (0.46, 0.46), (0.44, 0.66), (0.66, 0.6), (0.64, 0.44), (0.9, 0.42), (0.9, 0.92), (0.2, 0.92)]
            else:                                                   # (the crooked grin: up on the left, a dip, up on the right)
                pts = [(0.22, 0.56), (0.46, 0.52), (0.44, 0.72), (0.66, 0.66), (0.64, 0.5), (0.88, 0.48), (0.88, 0.9), (0.22, 0.9)]
            P = [(x * W, y * H) for x, y in pts]
            d.polygon(P, fill=hexc(T_), outline=hexc(LINE), width=int(lw))
            d.rectangle((W * 0.235, H * 0.82, W * 0.865, H * 0.885), fill=hexc(S_))
            for x in (0.36, 0.54, 0.74):
                ln(d, [(W * x, H * 0.7), (W * x, H * 0.88)], '#c8be80', lw * 0.6)
            if f == 'fierce':
                for i in range(7):
                    x = 0.24 + i * 0.09; ln(d, [(W * x, H * 0.6), (W * (x + 0.045), H * 0.66), (W * (x + 0.09), H * 0.6)], LINE, lw * 0.6)
        return R.t(f'face{"_" + f if f else ""}', face_tex(GREY, 6.4, 4.8, p, seed=29, hi=60, pix=False))

    def eyeball(f, big):
        """an eye on a stalk: white, shaded low; a black pupil with a glint (or a grey lid coming down)"""
        def p(d, W, H):
            E(d, W * 0.5, H * 0.62, W * 0.42, H * 0.3, '#c8c8c4')                               # (shade)
            lx = {'look': 0.2, 'happy': 0.0}.get(f, 0.06) * W; ly = {'happy': -0.12, 'wow': 0.0}.get(f, 0.04) * H
            pr = W * (0.12 if f == 'wow' else 0.18)
            if f != 'blink':
                E(d, W * 0.5 + lx, H * 0.5 + ly, pr, pr, '#141414'); E(d, W * 0.44 + lx, H * 0.43 + ly, pr * 0.4, pr * 0.4, '#ffffff')
            if f in ('blink', 'fierce'):                             # (the lid: all the way down, or half and slanting)
                lid = [(0, 0), (W, 0), (W, H * (0.62 if f == 'blink' else (0.3 if big else 0.5))), (0, H * (0.62 if f == 'blink' else (0.5 if big else 0.3)))]
                d.polygon(lid, fill=hexc('#8a8c8e'))
                ln(d, [lid[3], lid[2]], LINE, W * 0.06)
        return R.t(f'eye{"_b" if big else "_s"}{"_" + f if f else ""}', face_tex('#eeeeec', 2.2 if big else 1.2, 2.2 if big else 1.2, p, seed=31, hi=70, rim='#9a9a9a', rim_a=90, pix=False))
    for f in (None,) + FACES:
        head_face(f); eyeball(f, True); eyeball(f, False)
    by = 9.0
    panel = R.t('panel', face_tex(GREY, 5.0, 5.4, lambda d, W, H: (
        d.polygon([(W * 0.08, H * 0.06), (W * 0.92, H * 0.06), (W * 0.82, H * 0.94), (W * 0.18, H * 0.94)], fill=hexc(GREYL), outline=hexc(LINE), width=int(W * 0.04)),
        ln(d, [(W * 0.56, H * 0.3), (W * 0.56, H * 0.7)], LINE, W * 0.05)), seed=24, hi=50, pix=False))

    def body(v, f):
        return [el((-3.8, by + 1.2, -2.4), (3.8, by + 3.6, 2.4), metal, (0, by, 0)),               # (the chest, wide at the top...)
                el((-3.3, by - 1.0, -2.2), (3.3, by + 1.2, 2.2), metal, (0, by, 0), shift=(0.3, 0.2)),
                el((-2.8, by - 3.0, -2.0), (2.8, by - 1.0, 2.0), metal, (0, by, 0), shift=(0.6, 0.5)),   # (...narrow at the waist)
                plate((-2.5, by - 2.6, -2.62), (2.5, by + 2.8, -2.6), panel, (0, by, 0), 5.0, 5.4),
                el((-2.4, by - 4.2, -1.8), (2.4, by - 3.0, 1.8), dark, (0, by, 0)),
                el((-1.5, by + 3.6, -1.4), (1.5, by + 4.6, 1.4), dark, (0, by, 0))]                 # (the neck)
    R.part('body', (0, by, 0), None, body)
    hy = by + 4.6

    def head(v, f):
        pv = (0, hy, 0)
        Lh = [el((-3.2, hy, -2.4), (3.2, hy + 4.8, 2.4), metal, pv, shift=(0.3, 0.5)),
              plate((-3.2, hy, -2.43), (3.2, hy + 4.8, -2.4), R.fk(f), pv, 6.4, 4.8)]
        # the eyes on stalks: the big one on his right, the little one on his left; the curly antenna between
        Lh += [el((1.75, hy + 4.8, -0.25), (2.25, hy + 7.0, 0.25), stalk, pv), *ball((2.0, hy + 8.0, -0.2), 1.1, eyew, pv, face=R.fk(f, 'eye_b'), n=5, smooth=True),
               el((-2.35, hy + 4.8, -0.2), (-1.95, hy + 6.0, 0.2), stalk, pv), *ball((-2.15, hy + 6.55, -0.2), 0.6, eyew, pv, face=R.fk(f, 'eye_s'), n=4, smooth=True)]
        Lh += chain([(0.2, hy + 4.8, 0), (0.0, hy + 6.0, 0), (0.9, hy + 6.8, 0), (0.5, hy + 7.6, 0), (-0.2, hy + 7.0, 0), (0.3, hy + 8.6, 0)],
                    [0.3] * 5, 0.3, stalk, pv, (0.0, 0.0, -1.0), ext=0.1)
        Lh += ball((0.3, hy + 9.1, 0), 0.55, redb, pv, n=3, smooth=True)
        return Lh
    R.part('head', (0, hy, 0), 'body', head, faced=True)

    def clamp(cx, cy, cz, pv, r=1.1):
        """a C-clamp hand, open at the top, in the plane facing front"""
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)), cz) for a in range(120, 421, 50)]
        return chain(pts, [0.65] * (len(pts) - 1), 0.7, metal, pv, (0.0, 0.0, -1.0), ext=0.15)
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 4.0, by + 3.0, 0)
        def arm(v, f, pv=pv, s=s):
            x = pv[0]; y = pv[1]
            A = [el((x - 0.9, y - 0.9, -0.9), (x + 0.9, y + 0.9, 0.9), dark, pv),
                 *chain([(x, y, 0), (x + s * 1.4, y - 3.6, 0), (x + s * 1.0, y - 7.4, 0)], [0.9, 0.85], 0.9, light_, pv)]
            A += clamp(x + s * 1.0, y - 8.6, 0, pv)
            if v == 'rocket':
                A.append(el((x + s * 1.0 - 0.7, y - 0.5, -0.7), (x + s * 1.0 + 0.7, y + 0.7, 0.7), flame, pv, light=15))
            return A
        R.part(n, pv, 'body', arm, variants=('rocket',))
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.7, by - 4.0, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: [
            seg((pv[0], pv[1], 0), (pv[0] + s * 0.3, 2.2, 0), 1.6, 1.6, light_, pv),
            el((pv[0] + s * 0.3 - 1.5, 0.6, -2.2), (pv[0] + s * 0.3 + 1.5, 2.4, 1.4), metal, pv),            # (the boot)
            el((pv[0] + s * 0.3 - 1.4, 0.0, -2.0), (pv[0] + s * 0.3 + 1.4, 0.6, 1.2), dark, pv)] +
            ([el((pv[0] + s * 0.3 - 0.9, -1.8, -1.0), (pv[0] + s * 0.3 + 0.9, 0.0, 0.6), flame, pv, light=15)] if v == 'jet' else []))(pv, s), variants=('jet',))
    arms = lambda r, l: dict(armr=L(('x', r[0]), ('z', r[1])), arml=L(('x', l[0]), ('z', l[1])))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'legr': 'jet', 'legl': 'jet'}, _off=(0, 3.0, 0), **arms((0, 60), (0, -60))),
        'idle_a': dict(**arms((4, 6), (-4, -6)), head=T(('x', 3))),
        'idle_b': dict(_face='look', **arms((0, 10), (0, 130)), head=T(('y', -22), ('z', 6)), body=T(('y', 6))),        # (a wave, as drawn)
        'stomp_up': dict(_face='fierce', _off=(0, 1.4, 0), legr=L(('x', -60)), **arms((0, 30), (0, -30)), body=T(('z', -6))),
        'stomp': dict(_face='fierce', _off=(0, -0.8, 0), **arms((-10, 40), (-10, -40)), body=T(('x', 6))),
        'wind': dict(_face='fierce', body=T(('y', 28)), **arms((50, 0), (-30, -14)), head=T(('y', -18))),
        'strike': dict(_face='fierce', _v={'armr': 'rocket'}, _o_armr=(0, 2.0, -9.0), body=T(('y', -18)), armr=L(('x', -90)), arml=L(('x', 30)), head=T(('y', 8))),
        'happy': dict(_face='happy', _off=(0, 0.6, 0), **arms((0, 150), (0, -150)), head=T(('z', 8))),
        'vanish': dict(_face='happy', _v={'legr': 'jet', 'legl': 'jet'}, _off=(0, 4.0, 0), arml=L(('z', -150)), armr=L(('x', 0), ('z', 20))),
    })
    return R.ns()


# ==================================================================================================== ZAPPER - the lightning bolt
def zapper():
    R = Rig('gz_zapper_', 1.0)
    Y, YL, YD, INK = '#ffe11a', '#fff38a', '#e0a800', '#7a5a08'
    gold = R.t('bolt', lit(tex(Y, 31, 0.04), 6, 6, 4, a=110, rim=YD))
    hot = R.t('hot', lit(tex('#fff27a', 32, 0.03), 6, 6, 4, a=60))
    blue = R.t('arc', tex('#a8e4ff', 33, 0.04))

    def face(f):
        """his face as drawn: round white eyes, grey low down, small black pupils glancing aside; one brow way up, the other
        down and in (curious); a green gem of a nose; a wavy, unsure little mouth"""
        def p(d, W, H):
            lw = W * 0.018
            ex, ey, er = (W * 0.28, H * 0.38), (W * 0.7, H * 0.38), W * (0.14 if f != 'wow' else 0.16)
            for (cx, cy), side in ((ex, 1), (ey, -1)):
                if f in ('blink', 'happy'):
                    ln(d, arc(cx, cy + (er * 0.6 if f == 'happy' else -er * 0.2), er * 0.9, er * (0.8 if f == 'happy' else 0.5), 200 if f == 'happy' else 20, 340 if f == 'happy' else 160), '#3a2a06', lw * 1.6)
                    continue
                E(d, cx, cy, er, er * 1.05, '#ffffff', INK, lw)
                d.chord((cx - er, cy - er * 1.05, cx + er, cy + er * 1.05), 20, 160, fill=hexc('#cfcfd4'))          # (grey shade low in the eye)
                E(d, cx, cy, er, er * 1.05, None, INK, lw)
                lx = {'look': -0.45, 'fierce': 0.0, 'wow': 0.0}.get(f, 0.42) * er; ly = {'fierce': 0.0}.get(f, 0.1) * er
                pr = er * (0.22 if f == 'wow' else 0.36)
                E(d, cx + lx, cy + ly, pr, pr * 1.1, '#101010'); E(d, cx + lx - pr * 0.35, cy + ly - pr * 0.4, pr * 0.35, pr * 0.35, '#ffffff')
            # brows: curious - his right one arched high, the left low and slanting in; level and high when amazed; both down in a fight
            bw = lw * 1.7; BR = '#6a4a0a'
            if f == 'fierce':
                ln(d, [(ex[0] - er, ex[1] - er * 1.25), (ex[0] + er * 0.9, ex[1] - er * 0.7)], BR, bw * 1.5)
                ln(d, [(ey[0] + er, ey[1] - er * 1.25), (ey[0] - er * 0.9, ey[1] - er * 0.7)], BR, bw * 1.5)
            elif f == 'wow':
                ln(d, arc(ex[0], ex[1] - er * 1.0, er * 0.9, er * 0.5, 200, 340), BR, bw); ln(d, arc(ey[0], ey[1] - er * 1.0, er * 0.9, er * 0.5, 200, 340), BR, bw)
            elif f == 'look':
                ln(d, arc(ey[0], ey[1] - er * 1.0, er * 0.9, er * 0.6, 200, 340), BR, bw)
                ln(d, [(ex[0] - er * 0.9, ex[1] - er * 1.15), (ex[0] + er * 0.8, ex[1] - er * 1.2)], BR, bw)
            else:
                ln(d, arc(ex[0], ex[1] - er * 1.05, er * 0.9, er * 0.6, 200, 340), BR, bw)
                ln(d, [(ey[0] - er * 0.9, ey[1] - er * 1.05), (ey[0] + er * 0.9, ey[1] - er * 1.35)], BR, bw)
            # the nose: an emerald - a dark rim, a lighter facet, a glint
            nx, ny = W * 0.49, H * 0.62
            E(d, nx, ny, W * 0.1, H * 0.07, '#139a48', '#08542a', lw * 1.2)
            d.polygon([(nx - W * 0.04, ny - H * 0.035), (nx + W * 0.02, ny - H * 0.045), (nx + W * 0.005, ny + H * 0.005)], fill=hexc('#5ad890'))
            E(d, nx - W * 0.03, ny - H * 0.03, W * 0.014, H * 0.012, '#ffffff')
            mx, my = W * 0.47, H * 0.79
            if f == 'happy':
                ln(d, arc(mx, my - H * 0.03, W * 0.07, H * 0.05, 20, 160), '#3a2a06', lw * 1.5)
            elif f == 'wow':
                E(d, mx, my, W * 0.035, H * 0.045, '#5a2a10', '#3a2a06', lw)
            elif f == 'fierce':
                ln(d, [(mx - W * 0.08, my), (mx - W * 0.04, my - H * 0.025), (mx, my), (mx + W * 0.04, my - H * 0.025), (mx + W * 0.08, my)], '#3a2a06', lw * 1.4)
            else:                                                     # (the wavy, unsure little mouth: a dip and a wobble)
                ln(d, bez((mx - W * 0.075, my + H * 0.01), (mx - W * 0.035, my - H * 0.045), (mx + W * 0.01, my + H * 0.02), (mx + W * 0.07, my - H * 0.02)), '#3a2a06', lw * 1.4)
                ln(d, [(mx + W * 0.07, my - H * 0.02), (mx + W * 0.085, my + H * 0.012)], '#3a2a06', lw * 1.2)
        return R.t(f'face{"_" + f if f else ""}', face_tex(Y, 6.6, 6.6, p, seed=34, hi=120, rim=YD, rim_a=80))
    for f in (None,) + FACES: face(f)
    # (2.96c, the owner's art (ref/owner/buddies/zapper.png): not a lightning bolt - an unevenly rounded little body, his face on
    #  it, with jagged lightning spikes all the way round. The long bolt in the drawing is one of them stretched out: an arm,
    #  reaching to touch the light bulb (Dessa) and light her up - so his arms are two of the spikes, and the left one reaches
    #  out, a long zigzag of a bolt, when he zaps.)
    cy = 9.0
    R0 = 2.7                                                           # (where a spike grows out of him)

    def spike(a, L, t, pv, w=1.5, kink=0.7, th=1.0):
        """one jagged lightning spike in the plane of his face, at a degrees (0: his right, 90: up), L long"""
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        P = lambda r, k: (c * r - s_ * k, cy + s_ * r + c * k, 0.0)
        return chain([P(R0, 0), P(R0 + 0.45 * L, kink), P(R0 + 0.62 * L, -kink * 0.5), P(R0 + L, 0)], [w, w * 0.68, w * 0.4], th, t, pv, (0.0, 0.0, -1.0), ext=0.2)
    SPIKES = [(4, 4.0, 3.0), (40, 5.2, 3.4), (78, 4.4, 3.2), (108, 5.6, 3.0), (142, 4.0, 3.4), (176, 4.8, 3.0), (268, 4.6, 3.2), (296, 3.4, 2.6), (350, 3.0, 2.4)]
    ARMS = {'armr': 324, 'arml': 222}

    def core(v, f):
        t = hot if v == 'charged' else gold; pv = (0, cy, 0); lt = 10 if v else 5
        B = ball((0, cy, 0), 3.3, t, pv, yr=3.3, zr=2.4, face=R.fk(f), n=9, light=lt)
        B += ball((1.3, cy + 1.5, 0.5), 2.4, t, pv, yr=2.2, zr=1.7, n=5, light=lt) + ball((-1.5, cy - 1.3, 0.4), 2.5, t, pv, yr=2.3, zr=1.7, n=5, light=lt)
        for i, (a, L, w) in enumerate(SPIKES):                          # (broad jagged blades, every one its own size)
            B += spike(a, L, t, pv, w=w, kink=0.9 if i % 2 else -0.9)
        for a in (22, 58):                                             # (the pale blue glints between his spikes, as drawn)
            B += spike(a, 2.6, blue, pv, w=1.6, kink=0.3, th=0.5)
        if v == 'charged':
            B += [seg((2.8, cy + 3.2, -1.0), (5.8, cy + 5.4, -2.0), 0.3, 0.3, blue, pv, light=15),
                  seg((-4.0, cy - 2.0, -1.0), (-7.0, cy - 0.4, -2.2), 0.3, 0.3, blue, pv, light=15)]
        return B
    R.part('core', (0, cy, 0), None, core, variants=('charged',), faced=True)
    for n, a in ARMS.items():                                          # (his arms: two of the spikes - the left one reaches)
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
        pv = (c * R0, cy + s_ * R0, 0.0)

        def arm(v, f, a=a, pv=pv, c=c, s_=s_):
            if v != 'reach':
                return spike(a, 4.2, gold, pv, w=2.8, kink=0.8)
            # reaching: a long bolt - out and forward, zigzagging, to a point
            pts, k = [pv], 1
            for i in range(1, 7):
                r = i * 1.6
                side = (0.9 if i % 2 else -0.9) if i < 6 else 0.0
                pts.append((pv[0] + c * r * 0.6 - s_ * side, pv[1] + s_ * r * 0.4 + c * side, -r * 0.8))
            return chain(pts, [1.3, 1.1, 0.95, 0.8, 0.6, 0.35], 0.9, hot, pv, (0.0, 1.0, 0.0), ext=0.2) + [
                seg(pts[-1], (pts[-1][0], pts[-1][1], pts[-1][2] - 1.0), 0.25, 0.25, blue, pv, light=15)]
        R.part(n, pv, 'core', arm, variants=('reach',))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'core': 'charged'}, _off=(0, 1.4, 0), core=T(('z', 12))),
        'idle_a': dict(_off=(0, 0.8, 0), core=T(('z', -4)), armr=L(('z', 10)), arml=L(('z', -10))),
        'idle_b': dict(_face='look', _off=(0, 1.4, 0), core=T(('z', 12), ('y', -18)), armr=L(('z', -20))),     # (head cocked - curious)
        'bob_0': dict(_face='look', _off=(0, 2.0, 0), core=T(('z', 16), ('x', -10)), armr=L(('z', 30)), arml=L(('z', -10))),
        'bob_1': dict(_face='wow', _off=(0, 0.4, 0), core=T(('z', -14), ('y', 20)), armr=L(('z', -10)), arml=L(('z', 30))),
        'wind': dict(_face='fierce', _v={'core': 'charged'}, _off=(0, 2.4, 1.6), core=T(('x', 18)), armr=L(('z', 40)), arml=L(('z', -40))),
        'strike': dict(_face='fierce', _v={'core': 'charged', 'arml': 'reach'}, _off=(0, 1.0, -2.0), core=T(('x', -12), ('y', -20))),
        'happy': dict(_face='happy', _off=(0, 2.0, 0), core=T(('z', -12)), armr=L(('z', 50)), arml=L(('z', -50))),
        'vanish': dict(_face='blink', _v={'core': 'charged'}, _off=(0, 3.0, 0), core=T(('y', 180))),
    })
    return R.ns()


# ==================================================================================================== DESSA - the light bulb
def dessa():
    R = Rig('gz_dessa_', 1.0)
    GL, GLD, INK = '#f6ec48', '#d8c41a', '#4a3c0a'
    glass = {None: R.t('glass', lit(tex(GL, 41, 0.03), 8, 8, 4, a=150, rim=GLD, rim_a=110)),
             'dim': R.t('glass_dim', lit(tex('#b8ac3a', 42, 0.03), 8, 8, 4, a=60)),
             'flash': R.t('glass_flash', tex('#fffcea', 43, 0.02))}
    base, ring = R.t('base', lit(tex('#8e9294', 44, 0.04), 4, 4, 4, a=80)), R.t('ring', tex('#5a5e62', 45, 0.04))
    glow = R.t('glow', tex('#fff6a0', 46, 0.03))
    fil = R.t('filament', tex('#e8a030', 47, 0.06))

    def face(f, v):
        col = {None: GL, 'dim': '#b8ac3a', 'flash': '#fffcea'}[v]
        def p(d, W, H):          # (as drawn: her eyes shut in two happy pointed arches, a wavy little smile with a curl at its end)
            lw = W * 0.022; ex, ey = (W * 0.32, H * 0.42), (W * 0.68, H * 0.42); er = W * 0.1
            E(d, W * 0.24, H * 0.2, W * 0.08, H * 0.05, '#fffff0'); E(d, W * 0.17, H * 0.3, W * 0.025, H * 0.04, '#fffff0')   # (the glass's shine)
            for cx, cy in (ex, ey):
                if f in (None, 'happy'):                     # (^ : a peak, its two sides bowing out a little)
                    k = 1.25 if f == 'happy' else 1.0
                    ln(d, bez((cx - er, cy + er * 0.55 * k), (cx - er * 0.55, cy - er * 0.2 * k), (cx - er * 0.08, cy - er * 0.75 * k)), INK, lw)
                    ln(d, bez((cx - er * 0.08, cy - er * 0.75 * k), (cx + er * 0.45, cy - er * 0.25 * k), (cx + er, cy + er * 0.5 * k)), INK, lw)
                elif f == 'blink':                            # (drowsing: two soft dashes)
                    ln(d, arc(cx, cy - er * 0.2, er * 0.85, er * 0.35, 30, 150), INK, lw)
                elif f == 'fierce':                           # (determined: two slanted strokes)
                    s = 1 if cx < W / 2 else -1
                    ln(d, [(cx - s * er, cy - er * 0.5), (cx + s * er * 0.8, cy + er * 0.15)], INK, lw * 1.3)
                else:                                          # (wide awake: two round dark eyes with a glint)
                    lx = er * (0.25 if f == 'look' else 0)
                    E(d, cx + lx, cy, er * 0.42, er * 0.5, '#2a2008'); E(d, cx + lx - er * 0.14, cy - er * 0.18, er * 0.15, er * 0.15, '#ffffff')
            mx, my = W * 0.52, H * 0.66
            if f == 'happy':
                d.chord((mx - W * 0.1, my - H * 0.06, mx + W * 0.1, my + H * 0.1), 0, 180, fill=hexc('#8a5a14'), outline=hexc(INK), width=int(lw))
            elif f == 'wow':
                E(d, mx, my + H * 0.02, W * 0.04, H * 0.05, '#8a5a14', INK, lw)
            elif f == 'fierce':
                ln(d, [(mx - W * 0.08, my + H * 0.02), (mx + W * 0.08, my - H * 0.005)], INK, lw)
            else:                                              # (the wavy smile, curling up at its end)
                ln(d, bez((mx - W * 0.1, my - H * 0.02), (mx - W * 0.06, my + H * 0.05), (mx - W * 0.02, my + H * 0.05), (mx + W * 0.01, my)), INK, lw)
                ln(d, bez((mx + W * 0.01, my), (mx + W * 0.04, my + H * 0.05), (mx + W * 0.09, my + H * 0.04), (mx + W * 0.1, my - H * 0.03)), INK, lw)
                ln(d, arc(mx + W * 0.115, my - H * 0.035, W * 0.018, H * 0.02, 180, 360, n=8), INK, lw * 0.8)
        return R.t(f'face{"_" + v if v else ""}{"_" + f if f else ""}', face_tex(col, 7.2, 7.6, p, seed=48, hi=130 if v != 'dim' else 50, rim=None if v == 'flash' else '#c8b010', rim_a=80))
    for v in (None, 'dim', 'flash'):
        for f in (None,) + FACES: face(f, v)
    gy = 10.4
    def bulb(v, f):
        lt = {None: 11, 'dim': 3, 'flash': 15}[v]
        Lb = ball((0, gy, 0), 3.6, glass[v], (0, gy, 0), yr=3.8, zr=3.4, light=lt, face=R.prefix + 'face' + (f'_{v}' if v else '') + (f'_{f}' if f else ''), n=8)
        Lb += [el((-1.9, gy - 5.0, -1.9), (1.9, gy - 3.0, 1.9), glass[v], (0, gy, 0), light=lt),                  # (the neck)
               *chain([(-0.6, gy - 4.6, 0), (-0.3, gy - 3.4, -0.2), (0.2, gy - 2.8, -0.4), (0.0, gy - 2.2, -0.6)], [0.18] * 3, 0.18, fil, (0, gy, 0), (0.0, 0.0, -1.0))]
        return Lb
    R.part('bulb', (0, gy, 0), None, bulb, variants=('dim', 'flash'), faced=True)
    R.part('base', (0, gy - 5.0, 0), 'bulb', lambda v, f: [
        el((-2.0, 1.2 + i * 1.0, -2.0), (2.0, 2.0 + i * 1.0, 2.0), base if i % 2 else ring, (0, gy - 5.0, 0)) for i in range(4)] + [
        el((-1.2, 0.0, -1.2), (1.2, 1.2, 1.2), ring, (0, gy - 5.0, 0))])
    for s, n in ((1, 'armr'), (-1, 'arml')):                         # (arms of light: wavy glowing lines, as drawn)
        pv = (s * 3.2, gy - 2.2, 0)
        R.part(n, pv, 'bulb', (lambda pv, s: lambda v, f: [
            *[dict(e, light_emission=12) for e in chain([(pv[0], pv[1], 0), (pv[0] + s * 1.2, pv[1] - 1.2, -0.2), (pv[0] + s * 2.4, pv[1] - 0.6, -0.4), (pv[0] + s * 3.0, pv[1] + 0.6, -0.6)],
                                                         [0.3, 0.3, 0.3], 0.3, glow, pv, (0.0, 0.0, -1.0))],
            *[dict(e, light_emission=12) for e in chain([(pv[0] + s * 3.0, pv[1] + 0.6, -0.6), (pv[0] + s * 2.7, pv[1] + 1.3, -0.6)], [0.25], 0.25, glow, pv, (0.0, 0.0, -1.0))]])(pv, s))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'bulb': 'flash'}, _off=(0, 1.0, 0), armr=L(('z', 50)), arml=L(('z', -50))),
        'idle_a': dict(bulb=T(('z', -5)), armr=L(('z', -10)), arml=L(('z', 10))),
        'idle_b': dict(_face='look', _v={'bulb': 'dim'}, bulb=T(('z', 10), ('y', -14)), armr=L(('z', 30))),     # (a flicker - and a look round)
        'flicker': dict(_face='blink', _v={'bulb': 'dim'}),
        'wind': dict(_face='fierce', _off=(0, -0.6, 0), bulb=T(('x', 14)), armr=L(('x', 40), ('z', 40)), arml=L(('x', 40), ('z', -40))),
        'strike': dict(_face='wow', _v={'bulb': 'flash'}, _off=(0, 1.2, 0), bulb=T(('x', -10)), armr=L(('z', 110)), arml=L(('z', -110))),
        'happy': dict(_face='happy', _off=(0, 0.8, 0), bulb=T(('z', 12)), armr=L(('z', 90)), arml=L(('z', -40))),
        'vanish': dict(_face='blink', _v={'bulb': 'dim'}, bulb=T(('z', -20)), armr=L(('z', 120))),
    })
    return R.ns()


# ==================================================================================================== BUBBLES - a pair of bubbles
def bubbles():
    R = Rig('gz_bubbles_', 1.0)
    B, BL, BD, INK = '#90d6ee', '#d0f2fc', '#4aa4c4', '#2e5a68'
    skin = R.t('skin', lit(tex(B, 51, 0.03), 9.2, 8.4, 4, a=170, rim=BD))
    skin2 = R.t('skin2', lit(tex(B, 52, 0.03), 5.2, 5.2, 4, a=170, rim=BD))
    shine = R.t('shine', tex('#ffffff', 53, 0.01))
    drop = R.t('drop', tex(BL, 54, 0.04))

    def face(f):
        """as drawn: two tall dark teal eyes, close together, each with a big glint - and the great round open mouth off to one
        side: a thick teal rim, dark inside, a red tongue at the bottom"""
        def p(d, W, H):
            lw = W * 0.02
            E(d, W * 0.22, H * 0.2, W * 0.07, H * 0.05, '#ffffff'); E(d, W * 0.14, H * 0.3, W * 0.02, H * 0.03, '#ffffff')       # (the bubble's shine)
            for cx in (W * 0.3, W * 0.47):
                cy = H * 0.36
                if f == 'blink': ln(d, arc(cx, cy, W * 0.055, H * 0.035, 20, 160), INK, lw * 1.6); continue
                if f == 'happy': ln(d, arc(cx, cy + H * 0.04, W * 0.055, H * 0.07, 200, 340), INK, lw * 1.8); continue
                rx, ry = (W * 0.055, H * 0.12) if f == 'wow' else (W * 0.048, H * 0.1)
                lx = W * (0.018 if f == 'look' else 0)
                if f == 'fierce':                                       # (the top cut off on a slant, sloping in toward the middle)
                    s = 1 if cx < W * 0.4 else -1
                    y0, y1 = cy - ry * (0.6 if s > 0 else 0.0), cy - ry * (0.0 if s > 0 else 0.6)
                    cut = lambda x, y, cx=cx, y0=y0, y1=y1, rx=rx: y > y0 + (y1 - y0) * (x - cx + rx) / (2 * rx)
                    d.polygon(clip(cx, cy, rx, ry, cut), fill=hexc(INK))
                    ln(d, [(cx - rx * 1.5, y0 - (y1 - y0) * 0.25), (cx + rx * 1.5, y1 + (y1 - y0) * 0.25)], INK, lw * 1.3)
                    continue
                E(d, cx + lx, cy, rx, ry, INK)
                E(d, cx + lx - rx * 0.25, cy - ry * 0.4, rx * 0.45, rx * 0.45, '#ffffff'); E(d, cx + lx + rx * 0.3, cy + ry * 0.45, rx * 0.2, rx * 0.2, '#e0f4fa')
            mx, my, mr = W * 0.68, H * 0.66, W * (0.15 if f != 'wow' else 0.18)
            if f == 'fierce': mr *= 0.8
            E(d, mx, my, mr, mr * 1.05, '#3e7482', INK, lw)                                   # (the rim)
            E(d, mx + mr * 0.05, my + mr * 0.08, mr * 0.68, mr * 0.75, '#173a46')              # (inside)
            d.chord((mx - mr * 0.55, my + mr * 0.1, mx + mr * 0.65, my + mr * 0.85), 0, 180, fill=hexc('#8a2a18'))   # (the tongue)
            d.chord((mx - mr * 0.35, my + mr * 0.25, mx + mr * 0.4, my + mr * 0.7), 0, 180, fill=hexc('#b84a2e'))
        return R.t(f'face{"_" + f if f else ""}', face_tex(B, 9.2, 8.4, p, seed=55, hi=170, rim=BD, rim_a=110))
    for f in (None,) + FACES: face(f)
    cy = 5.2
    def big(v, f):
        if v == 'pop':                                   # (popped: a splash of droplets where it was)
            return [el((x - 0.7, cy + y - 0.7, z - 0.7), (x + 0.7, cy + y + 0.7, z + 0.7), drop, (0, cy, 0), light=6)
                    for x, y, z in ((-4, 1, 0), (4, 2, -1), (0, 5, 0), (-3, -3, 1), (3, -3, -2), (0, -1, -4), (5, -1, 2), (-5, 3, -2))]
        return ball((0, cy, 0), 4.6, skin, (0, cy, 0), yr=4.2, zr=4.0, face=R.fk(f), n=9) + [
            el((2.6, cy + 2.0, -3.4), (3.6, cy + 3.0, -2.8), shine, (0, cy, 0), light=10)]
    R.part('big', (0, cy, 0), None, big, variants=('pop',), faced=True)
    sc = (-6.2, 3.4, 1.4)                                  # (its little one, beside it - no face of its own, as drawn)
    R.part('small', sc, 'big', lambda v, f: [el((sc[0] + x - 0.5, sc[1] + y - 0.5, sc[2] + z - 0.5), (sc[0] + x + 0.5, sc[1] + y + 0.5, sc[2] + z + 0.5), drop, sc, light=6)
                                             for x, y, z in ((-1.5, 1, 0), (1.8, 0.5, -1), (0, -1.6, 1), (1, 2.2, 0.5))] if v == 'pop' else ball(sc, 2.6, skin2, sc, yr=2.4, zr=2.4) + [
        el((sc[0] + 0.8, sc[1] + 1.0, sc[2] - 2.0), (sc[0] + 1.6, sc[1] + 1.8, sc[2] - 1.6), shine, sc, light=10)], variants=('pop',))
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 2.0, 0), _o_small=(-1.0, 2.0, 0)),
        'idle_a': dict(_off=(0, 0.8, 0), _o_small=(0, -0.6, 0), big=T(('z', -4))),
        'idle_b': dict(_face='look', _off=(0, 0.2, 0), _o_small=(0, 1.0, -0.6), big=T(('y', 16)), small=T(('y', -20))),
        'bounce_0': dict(_off=(0, 2.4, 0), _o_small=(0, -1.6, 0)), 'bounce_1': dict(_off=(0, 0.0, 0), _o_small=(0, 2.0, 0)),
        'wind': dict(_face='fierce', _off=(0, 3.6, 1.6), _o_small=(1.0, 1.2, 1.0), big=T(('x', 14))),
        'strike': dict(_face='wow', _v={'big': 'pop', 'small': 'pop'}, _off=(0, 0.0, -4.0)),
        'happy': dict(_face='happy', _off=(0, 1.6, 0), _o_small=(0, 1.8, 0), big=T(('z', -10)), small=T(('z', 16))),
        'vanish': dict(_face='happy', _off=(0, 4.0, 0), _o_small=(2.0, 2.0, 0)),
    })
    return R.ns()


# ==================================================================================================== CHASE - the green gummy
def chase():
    R = Rig('gz_chase_', 1.0)
    G, GL, GD, INK = '#1ed23a', '#8af08a', '#0c8a22', '#0a1a0a'
    goo = R.t('goo', lit(tex(G, 61, 0.03), 6, 6, 4, a=150, rim=GD, rim_a=130))
    gloss = R.t('gloss', tex('#d8ffd8', 63, 0.02))

    def face(f):
        """as drawn: big hollow white eyes (no pupils) in thick dark rims, a short brow line over each; a wide toothy grin,
        and a little dark moustache tuft just above it"""
        def p(d, W, H):
            lw = W * 0.03
            E(d, W * 0.2, H * 0.16, W * 0.06, H * 0.04, '#e8ffe8'); E(d, W * 0.12, H * 0.26, W * 0.02, H * 0.03, '#e8ffe8')      # (the gloss)
            eyes = ((W * 0.33, H * 0.37, -1), (W * 0.67, H * 0.39, 1))       # (2.96c, as drawn: the eye on his right a little the bigger)
            for cx, cy, s in eyes:
                rx, ry = W * 0.11 * (1.0 if s < 0 else 0.86), H * 0.17 * (1.0 if s < 0 else 0.86)
                if f == 'wow': rx, ry = W * 0.125, H * 0.2
                if f == 'blink':
                    ln(d, arc(cx, cy - ry * 0.1, rx, ry * 0.45, 25, 155), INK, lw); continue
                if f == 'happy':                      # (still hollow and white - just squeezed up into crescents by the grin)
                    d.chord((cx - rx, cy - ry * 0.9, cx + rx, cy + ry * 0.9), 180, 360, fill=hexc('#ffffff'), outline=hexc(INK), width=int(lw))
                    ln(d, [(cx - rx, cy), (cx + rx, cy)], INK, lw)
                    continue
                lx = (s * 0.0 if f != 'look' else 0.25 * rx)
                if f == 'fierce':                     # (a heavy brow cutting down across the top of the eye, sloping in)
                    yo, yi = cy - ry * 0.75, cy - ry * 0.1            # (outer end higher, inner lower)
                    x_o, x_i = cx - s * rx, cx + s * rx
                    cut = lambda x, y, x_o=x_o, x_i=x_i, yo=yo, yi=yi: y > yo + (yi - yo) * (x - x_o) / (x_i - x_o)
                    P = clip(cx, cy, rx, ry, cut)
                    d.polygon(P, fill=hexc('#ffffff'), outline=hexc(INK), width=int(lw))
                    ln(d, [(x_o - s * rx * 0.3, yo - (yi - yo) * 0.15), (x_i + s * rx * 0.2, yi + (yi - yo) * 0.1)], INK, lw * 1.5)
                    continue
                E(d, cx + lx, cy, rx, ry, '#ffffff', INK, lw)
            if f not in ('fierce',):                   # (the little brow lines)
                for cx, cy, s in eyes:
                    by = cy - H * (0.24 if f != 'wow' else 0.28)
                    ln(d, arc(cx + s * W * 0.01, by, W * 0.05, H * 0.025, 200, 340, n=10), INK, lw * 0.7)
            mx, my = W * 0.46, H * 0.74                 # (as drawn: the grin a touch to his right)
            # (2.96d: no moustache tuft - at his size it read as a mole; the owner had it taken off)
            if f == 'wow':
                E(d, mx, my + H * 0.04, W * 0.07, H * 0.08, '#2a0a0a', INK, lw)
                d.chord((mx - W * 0.06, my - H * 0.03, mx + W * 0.06, my + H * 0.03), 0, 180, fill=hexc('#ffffff'))
                return
            if f == 'fierce':                         # (gritted: a box of teeth)
                d.rounded_rectangle((mx - W * 0.16, my - H * 0.03, mx + W * 0.16, my + H * 0.07), radius=int(W * 0.03), fill=hexc('#ffffff'), outline=hexc(INK), width=int(lw))
                ln(d, [(mx - W * 0.15, my + H * 0.02), (mx + W * 0.15, my + H * 0.02)], INK, lw * 0.6)
                for i in range(1, 6):
                    x = mx - W * 0.16 + i * W * 0.32 / 6; ln(d, [(x, my - H * 0.025), (x, my + H * 0.065)], INK, lw * 0.5)
                return
            k = 1.45 if f == 'happy' else 1.25
            # the grin: a wide smile - white teeth across the top, a dark line under them, curling up at the corners
            top = bez((mx - W * 0.19 * k, my - H * 0.03), (mx, my + H * 0.015), (mx + W * 0.19 * k, my - H * 0.03))
            bot = bez((mx + W * 0.19 * k, my - H * 0.03), (mx + W * 0.02, my + H * 0.15 * k), (mx - W * 0.19 * k, my - H * 0.03))
            d.polygon(top + bot, fill=hexc('#ffffff'), outline=hexc(INK), width=int(lw))
            ln(d, bez((mx - W * 0.17 * k, my - H * 0.015), (mx, my + H * 0.075 * k), (mx + W * 0.17 * k, my - H * 0.015)), INK, lw * 0.6)
            for x in (-0.09, -0.03, 0.03, 0.09):
                ln(d, [(mx + W * x * k, my + H * 0.0), (mx + W * x * k, my + H * 0.035 * k)], '#7a8a7a', lw * 0.4)
            for s in (-1, 1):                         # (the corners, pulled up)
                ln(d, [(mx + s * W * 0.19 * k, my - H * 0.03), (mx + s * W * 0.22 * k, my - H * 0.06)], INK, lw * 0.8)
        return R.t(f'face{"_" + f if f else ""}', face_tex(G, 5.6, 4.8, p, seed=62, hi=150, rim=GD, rim_a=120))
    for f in (None,) + FACES: face(f)
    # (2.96c, the owner's art (ref/owner/buddies/chase.png): one gummy, no neck, no feet - his lower half is his head turned
    #  upside down: the same round shape under the face, its three lobes hanging down where the top's stand up (the middle one
    #  shortest). He floats a little over the ground. No nose; the eye on his right (the viewer's left) a little the bigger)
    SH = {None: (1.0, 1.0), 'squash': (1.12, 0.85), 'stretch': (0.9, 1.15)}            # (squash and stretch: width, height)
    lo = 6.0                                                                          # (the middle of the lower half)

    def body(v, f):
        kw, kh = SH[v]; pv = (0, lo, 0)
        return ball((0, lo, 0), 2.8 * kw, goo, pv, yr=2.4 * kh, zr=2.1 * kw, n=7) + [
            el((-1.6 * kw, lo - 0.2, -1.95 * kw), (-1.15 * kw, lo + 0.9, -1.9 * kw), gloss, pv, faces=('north',), light=4)]
    R.part('body', (0, lo, 0), None, body, variants=('squash', 'stretch'))
    hy = 9.4
    R.part('head', (0, 7.7, 0), 'body', lambda v, f: [
        *ball((0, hy, 0), 2.8, goo, (0, 7.7, 0), yr=2.4, zr=2.1, face=R.fk(f), n=7)], faced=True)
    # (2.96d, the owner's word: the lobes go round his middle like an octopus's tentacles - three on top, three below, spaced
    #  evenly round him (two to the front corners, one behind), each splaying out away from the middle; none left hanging
    #  limp in front. Each is built standing straight, then tilted out on its own line: (x, z) where it grows, its tilt)
    TENT = {'r': (1.8, -0.9, (-8.0, 0.0, -20.0)), 'l': (-1.8, -0.9, (-8.0, 0.0, 20.0)), 'm': (0.0, 1.5, (22.0, 0.0, 0.0))}

    def lobe(x, z, base, top, ang, pv, down=False, shine=True):
        k = -1 if down else 1
        els = ball((x, base + k * top / 2, z), 0.85, goo, pv, yr=top / 2 + 0.55, zr=0.85, n=10)
        if shine and not down:
            els += [el((x + 0.2, base + top - 1.1, z - 0.92), (x + 0.5, base + top - 0.4, z - 0.88), gloss, pv, faces=('north',), light=4)]
        a_ = ang if not down else (-ang[0], ang[1], -ang[2])
        return turn(els, a_, mo((x, base, z), pv))
    for key, (x, z, ang) in TENT.items():
        top = 3.4 if key != 'm' else 3.0
        pv = (x, hy + 1.4, z)
        R.part('lobe' + key, pv, 'head', (lambda x, z, top, ang, pv: lambda v, f: lobe(x, z, hy + 1.3, top, ang, pv))(x, z, top, ang, pv))
        pv2 = (x, lo - 1.4, z)
        R.part('leg' + key, pv2, 'body', (lambda x, z, top, ang, pv: lambda v, f: lobe(x, z, lo - 1.3, top, ang, pv, down=True))(x, z, top, ang, pv2))
    # (no arms of his own: the lobes hanging under him do for arms - the owner's word - swung out, up, forward)
    R.POSES.update({
        'appear': dict(_face='wow', _v={'body': 'stretch'}, _off=(0, 1.6, 0), legr=L(('z', 50)), legl=L(('z', -50))),
        'idle_a': dict(_off=(0, 1.0, 0), lober=L(('z', -6)), lobel=L(('z', 6)), legr=L(('z', 4)), legl=L(('z', -4))),
        'idle_b': dict(_face='look', _off=(0, 1.5, 0), head=T(('y', -14), ('z', 6)), lober=L(('z', 16)), lobel=L(('z', 10)), lobem=L(('x', 10)),
                       legr=L(('z', 40)), legl=L(('z', 6))),
        'hop_0': dict(_v={'body': 'squash'}, _off=(0, 0.3, 0), lober=L(('z', -20)), lobel=L(('z', 20)), lobem=L(('x', -10)), legr=L(('z', 14)), legl=L(('z', -14))),
        'hop_1': dict(_v={'body': 'stretch'}, _off=(0, 3.4, 0), lober=L(('z', 10)), lobel=L(('z', -10)), legr=L(('z', 40)), legl=L(('z', -40)), legm=L(('x', -14))),
        'wind': dict(_face='fierce', _v={'body': 'squash'}, _off=(0, 0.6, 1.0), body=T(('x', 14)), legr=L(('x', -50)), legl=L(('x', -50))),
        'strike': dict(_face='fierce', _v={'body': 'stretch'}, _off=(0, 1.2, -5.0), body=T(('x', -46)), lober=L(('x', 30)), lobel=L(('x', 30)),
                       lobem=L(('x', 30)), legr=L(('x', 80)), legl=L(('x', 80)), legm=L(('x', 40))),
        'happy': dict(_face='happy', _v={'body': 'stretch'}, _off=(0, 2.0, 0), lober=L(('z', -16)), lobel=L(('z', 16)), legr=L(('z', 120)), legl=L(('z', -120))),
        'vanish': dict(_face='happy', _v={'body': 'squash'}, _off=(0, 1.0, 0), legr=L(('z', 90))),
    })
    return R.ns()


# ==================================================================================================== LIMER - the round fellow in his green covering
def limer():
    R = Rig('gz_limer_', 1.0)
    S, SD, INK = '#cbbfb0', '#968a7c', '#16120e'
    skin = R.t('skin', lit(tex(S, 71, 0.04), 8.4, 8.8, 4, a=110, rim=SD))

    def loops(seed, base, cols):
        """his covering, as drawn: a tangle of little dark green loops"""
        im = tex(base, seed, 0.03, size=128); d = ImageDraw.Draw(im); r = random.Random(seed)
        for _ in range(150):
            x, y, s = r.uniform(-4, 132), r.uniform(-4, 132), r.uniform(4.0, 8.0)
            d.ellipse((x - s, y - s * 0.85, x + s, y + s * 0.85), outline=hexc(r.choice(cols)), width=2)
        return im
    leaf, leaf2 = R.t('leaf', loops(72, '#1e5a16', ('#3a9a2a', '#0e3a0c', '#2c7a20'))), R.t('leaf2', loops(73, '#246a1a', ('#46a834', '#0e3a0c')))
    stick = R.t('stick', tex('#1a1a1a', 74, 0.03))

    def face(f):
        """as drawn: two sleepy eyes - heavy black lids over a sliver of white, a dark pupil peeping out - a big curl of a nose,
        and a little round "o" of a mouth down low"""
        def p(d, W, H):
            lw = W * 0.02
            for cx, cy, s in ((W * 0.34, H * 0.3, -1), (W * 0.64, H * 0.27, 1)):
                rx, ry = W * 0.085, H * 0.042
                tilt = s * H * 0.012
                if f == 'blink':
                    ln(d, [(cx - rx, cy - tilt), (cx, cy + ry * 0.4), (cx + rx, cy + tilt)], INK, lw * 1.4); continue
                if f == 'happy':
                    ln(d, arc(cx, cy + ry * 1.2, rx, ry * 1.6, 200, 340), INK, lw * 1.5); continue
                if f == 'wow': ry *= 1.9
                E(d, cx, cy, rx, ry, '#f4f0ea', INK, lw)
                lx = rx * {'look': 0.45}.get(f, 0.1)
                E(d, cx + lx, cy + ry * 0.2, rx * 0.3, ry * 0.7, INK); E(d, cx + lx - rx * 0.1, cy, rx * 0.1, rx * 0.1, '#ffffff')
                lid = 0.62 if f is None or f == 'look' else 0.3                      # (how far the heavy lid comes down)
                if f == 'fierce':                                                      # (a slanting lid, low at the middle)
                    yo, yi = cy - ry * 0.3, cy + ry * 0.35
                    x_o, x_i = cx + s * rx, cx - s * rx
                    lidcut = lambda x, y, x_o=x_o, x_i=x_i, yo=yo, yi=yi: y < yo + (yi - yo) * (x - x_o) / (x_i - x_o)
                else:
                    yl = cy - ry + 2 * ry * lid
                    lidcut = lambda x, y, yl=yl: y < yl
                d.polygon(clip(cx, cy, rx * 1.04, ry * 1.06, lidcut), fill=hexc(INK))
            # the nose: a big round curl, open on the left - a soft shadow inside it
            nx, ny, nr = W * 0.62, H * 0.42, W * 0.085
            d.ellipse((nx - nr * 0.9, ny - nr * 0.7, nx + nr * 0.9, ny + nr * 0.8), fill=hexc('#bcae9c'))
            ln(d, arc(nx, ny, nr, nr * 0.85, -150, 150, n=28), INK, lw * 1.2)
            mx, my = W * 0.42, H * 0.6
            mr = W * {'wow': 0.04, 'happy': 0.03, 'fierce': 0.028}.get(f, 0.024)
            if f == 'happy':
                ln(d, arc(mx, my - H * 0.01, mr * 1.4, mr * 0.9, 20, 160), INK, lw * 1.2)
            elif f == 'fierce':
                ln(d, arc(mx, my + H * 0.02, mr * 1.3, mr * 0.8, 200, 340), INK, lw * 1.2)
            else:
                E(d, mx, my, mr, mr * 1.2, '#2a1a12', INK, lw * 0.8); E(d, mx + mr * 0.2, my + mr * 0.3, mr * 0.4, mr * 0.4, '#7a3a2a')
        return R.t(f'face{"_" + f if f else ""}', face_tex(S, 8.4, 8.8, p, seed=75, hi=110, rim=SD, rim_a=110))
    for f in (None,) + FACES: face(f)
    cy = 9.0
    def body(v, f):
        Lb = ball((0, cy, 0), 4.2, skin, (0, cy, 0), yr=4.4, zr=4.0, face=R.fk(f), n=8)
        for i in range(16):                                               # (the covering: a ring of loopy tufts round his lower half)
            a = math.radians(i * 360 / 16); x, z = math.sin(a) * 4.1, -math.cos(a) * 3.9
            Lb.append(el((x - 1.2, cy - 3.8 + (i % 3) * 0.15, z - 1.2), (x + 1.2, cy - 1.6 + (i % 2) * 0.2, z + 1.2), leaf if i % 2 else leaf2, (0, cy, 0), shift=(0.17 * i, 0.31 * i)))
        Lb.append(el((-3.4, cy - 4.4, -3.4), (3.4, cy - 3.2, 3.4), leaf2, (0, cy, 0)))
        Lb += chain([(0, cy + 4.3, 0), (0.4, cy + 5.6, 0), (1.2, cy + 6.0, 0), (1.4, cy + 5.2, 0), (0.8, cy + 5.0, 0)], [0.25] * 4, 0.25, stick, (0, cy, 0), (0.0, 0.0, -1.0))
        return Lb
    R.part('body', (0, cy, 0), None, body, faced=True)
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.6, cy - 4.2, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 0.8, 2.2, 0), (pv[0] + s * 0.6, 0.2, 0)], [0.3, 0.3], 0.3, stick, pv) +
                                                         [el((pv[0] + s * 0.6 - 0.5, 0.0, -1.2), (pv[0] + s * 0.6 + 0.5, 0.35, 0.3), stick, pv)])(pv, s))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 4.0, cy - 0.6, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.6, pv[1] - 2.4, -0.2), (pv[0] + s * 1.8, pv[1] - 4.6, -0.6)],
                                                                [0.3, 0.3], 0.3, stick, pv))(pv, s))
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 1.6, 0), armr=L(('z', 60)), arml=L(('z', -60))),
        'idle_a': dict(body=T(('z', -4)), armr=L(('z', 6)), arml=L(('z', -6))),
        'idle_b': dict(_face='look', body=T(('y', -18), ('z', 8)), armr=L(('x', -30), ('z', 20))),
        'roll_0': dict(_face='blink', _hide=('legr', 'legl', 'armr', 'arml'), _off=(0, -4.0, 0), body=T(('x', -90))),
        'roll_1': dict(_face='blink', _hide=('legr', 'legl', 'armr', 'arml'), _off=(0, -4.0, -2.0), body=T(('x', -180))),
        'wind': dict(_face='fierce', _off=(0, 4.0, 0), body=T(('x', 18)), legr=L(('x', 50)), legl=L(('x', 50)), armr=L(('z', 80)), arml=L(('z', -80))),
        'strike': dict(_face='fierce', _off=(0, -2.6, -3.0), body=T(('x', -10)), legr=L(('z', 60)), legl=L(('z', -60)), armr=L(('z', 100)), arml=L(('z', -100))),
        'happy': dict(_face='happy', _off=(0, 1.0, 0), body=T(('z', 10)), armr=L(('z', 130)), arml=L(('z', -130)), legr=L(('x', 30))),
        'vanish': dict(_face='happy', body=T(('y', 90)), arml=L(('z', -140))),
    })
    return R.ns()


# ==================================================================================================== CHICO - the drumstick
def chico():
    R = Rig('gz_chico_', 1.0)
    M, ML, MD, INK = '#9c6a30', '#c8a448', '#5a3410', '#120a04'
    meat = R.t('meat', lit(tex(M, 81, 0.05), 8, 8, 4, a=100, hi='#e8cc6a', rim=MD))
    crisp = R.t('crisp', tex('#5e3612', 85, 0.05, spots=[('#7a4a1a', 0.1)]))
    bone, stick = R.t('bone', lit(tex('#f2ead8', 82, 0.03), 4, 4, 4, a=60)), R.t('stick', tex('#1a1a1a', 83, 0.03))

    def face(f):
        """as drawn: shiny black eyes (no whites) with a big glint, thin worried brows lifted in the middle, an open fretful
        mouth - red inside, a row of top teeth - and crispy freckles"""
        def p(d, W, H):
            lw = W * 0.018
            r = random.Random(86)
            for _ in range(26):                                   # (freckles)
                x, y = r.uniform(0.08, 0.92), r.uniform(0.08, 0.92)
                if 0.22 < y < 0.5 and 0.2 < x < 0.8: continue
                E(d, W * x, H * y, W * 0.006, H * 0.005, '#5a3410')
            eyes = ((W * 0.36, H * 0.38, -1), (W * 0.64, H * 0.36, 1))
            for cx, cy, s in eyes:
                rx, ry = W * 0.06, H * 0.075
                if f == 'wow': rx, ry = rx * 1.2, ry * 1.25
                if f == 'blink': ln(d, arc(cx, cy, rx, ry * 0.5, 20, 160), INK, lw * 1.5); continue
                if f == 'happy': ln(d, arc(cx, cy + ry * 0.5, rx, ry * 0.8, 200, 340), INK, lw * 2.2); continue
                if f == 'fierce': ry *= 0.7
                lx = rx * (0.4 if f == 'look' else 0)
                E(d, cx + lx, cy, rx, ry, INK)
                E(d, cx + lx + rx * 0.3, cy - ry * 0.4, rx * 0.32, rx * 0.32, '#ffffff'); E(d, cx + lx - rx * 0.35, cy + ry * 0.45, rx * 0.12, rx * 0.12, '#ffffff')
            # brows: worried (inner ends up), relaxed when happy, down and in when fierce, way up when amazed
            for cx, cy, s in eyes:
                by = cy - H * 0.12
                if f == 'fierce':
                    ln(d, [(cx + s * W * 0.07, by - H * 0.02), (cx - s * W * 0.06, by + H * 0.035)], '#2a1606', lw * 1.6)
                elif f == 'happy':
                    ln(d, arc(cx, by + H * 0.02, W * 0.06, H * 0.025, 200, 340), '#2a1606', lw)
                else:
                    up = 0.05 if f == 'wow' else 0.0
                    ln(d, bez((cx + s * W * 0.07, by + H * 0.01 - H * up), (cx, by - H * 0.035 - H * up), (cx - s * W * 0.06, by - H * 0.045 - H * up)), '#2a1606', lw)
            mx, my = W * 0.42, H * 0.66
            if f == 'happy':
                d.chord((mx - W * 0.09, my - H * 0.05, mx + W * 0.09, my + H * 0.09), 0, 180, fill=hexc('#b8402a'), outline=hexc(INK), width=int(lw))
                d.rectangle((mx - W * 0.08, my - H * 0.01, mx + W * 0.08, my + H * 0.012), fill=hexc('#f4ece0'))
                return
            k = {'wow': 2.0, 'fierce': 1.3}.get(f, 1.6)
            # the fretful mouth: a lopsided open shape, a row of top teeth along it
            pts = bez((mx - W * 0.085 * k, my - H * 0.01), (mx - W * 0.02, my - H * 0.045 * k), (mx + W * 0.07 * k, my - H * 0.02), (mx + W * 0.075 * k, my + H * 0.01)) + \
                bez((mx + W * 0.075 * k, my + H * 0.01), (mx + W * 0.07 * k, my + H * 0.06 * k), (mx - W * 0.03, my + H * 0.07 * k), (mx - W * 0.085 * k, my - H * 0.01))
            d.polygon(pts, fill=hexc('#b8402a'), outline=hexc(INK), width=int(lw))
            d.polygon(bez((mx - W * 0.075 * k, my - H * 0.008), (mx - W * 0.02, my - H * 0.04 * k), (mx + W * 0.065 * k, my - H * 0.018)) +
                      bez((mx + W * 0.065 * k, my - H * 0.002), (mx - W * 0.02, my - H * 0.01 * k), (mx - W * 0.075 * k, my + H * 0.01)), fill=hexc('#f6eee2'))
            if f == 'fierce':
                for x in (-0.04, 0.0, 0.04): ln(d, [(mx + W * x, my - H * 0.03), (mx + W * x, my + H * 0.01)], '#7a6a5a', lw * 0.5)
        return R.t(f'face{"_" + f if f else ""}', face_tex(M, 6.8, 8.4, p, seed=84, hi=100, rim=MD, rim_a=110))
    for f in (None,) + FACES: face(f)
    my = 11.6
    R.part('meat', (0, 8.4, 0), None, lambda v, f: ball((0, my, 0), 3.4, meat, (0, 8.4, 0), yr=4.2, zr=3.2, face=R.fk(f), n=8) + [
        el((-2.2, my - 6.0, -2.0), (2.2, my - 3.6, 2.0), crisp, (0, 8.4, 0), shift=(0.4, 0.6)),                     # (crispy, tapering to the bone)
        ], faced=True)
    R.part('bone', (0, 5.6, 0), 'meat', lambda v, f: [el((-0.7, 3.0, -0.7), (0.7, 5.8, 0.7), bone, (0, 5.6, 0)),
                                                       el((-1.5, 2.2, -0.8), (-0.1, 3.4, 0.8), bone, (0, 5.6, 0)), el((0.1, 2.2, -0.8), (1.5, 3.4, 0.8), bone, (0, 5.6, 0))])
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 0.8, 2.4, 0)
        R.part(n, pv, 'bone', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.2, 0.2, 0)], [0.25], 0.25, stick, pv) +
                                                        [el((pv[0] + s * 1.2 - 0.5, 0.0, -1.0), (pv[0] + s * 1.2 + 0.5, 0.3, 0.3), stick, pv)])(pv, s))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 2.8, 9.0, 0)
        R.part(n, pv, 'meat', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.8, pv[1] - 1.6, -0.2), (pv[0] + s * 2.4, pv[1] - 3.4, -0.4)],
                                                               [0.25, 0.25], 0.25, stick, pv))(pv, s))
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 1.2, 0), armr=L(('z', 70)), arml=L(('z', -70))),
        'idle_a': dict(meat=T(('z', -6)), armr=L(('z', 10)), arml=L(('z', -4))),
        'idle_b': dict(_face='look', meat=T(('z', 9), ('y', -16)), armr=L(('z', -20)), arml=L(('z', 30))),
        'wobble_0': dict(meat=T(('z', -14)), armr=L(('z', 30)), arml=L(('z', -10))), 'wobble_1': dict(meat=T(('z', 14)), armr=L(('z', 10)), arml=L(('z', -30))),
        'wind': dict(_face='fierce', meat=T(('x', 26)), armr=L(('x', 60)), arml=L(('x', 60)), legr=L(('x', -20))),           # (leaning way back...)
        'strike': dict(_face='fierce', _off=(0, 0, -2.4), meat=T(('x', -38)), armr=L(('x', -40)), arml=L(('x', -40)), legl=L(('x', 30))),   # (...and WHACK - the meaty end first)
        'happy': dict(_face='happy', _off=(0, 1.0, 0), meat=T(('z', 10)), armr=L(('z', 120)), arml=L(('z', -120))),
        'vanish': dict(_face='happy', meat=T(('y', 120)), armr=L(('z', 100))),
    })
    return R.ns()


# ==================================================================================================== SPIKE - the circular saw
def spike():
    R = Rig('gz_spike_', 1.0)
    BK, INK = '#2e3034', '#000000'
    hub = R.t('hub', lit(tex(BK, 91, 0.04), 7.6, 7.6, 4, a=80, rim='#0e0e10'))
    steel, steeld, steelr = R.t('steel', lit(tex('#e8e6e8', 92, 0.02), 4, 4, 4, a=60, rim='#a0a0a8')), R.t('steeld', tex('#bebdc4', 93, 0.03)), R.t('ring', tex('#8c8c94', 97, 0.03))

    def face(f):
        """as drawn: a glossy black hub; heavy angry brows; dark eyes with a glint; a jagged fanged grin off to his left
        (2.96c: the green goo at its corner gone - the owner's ask)"""
        def p(d, W, H):
            lw = W * 0.02
            E(d, W * 0.36, H * 0.24, W * 0.18, H * 0.1, '#5c5e64'); E(d, W * 0.3, H * 0.2, W * 0.08, H * 0.04, '#8a8c92')       # (the gloss)
            eyes = ((W * 0.36, H * 0.48, -1, 0.07), (W * 0.62, H * 0.44, 1, 0.08))
            for cx, cy, s, r_ in eyes:
                rx, ry = W * r_ * 0.8, H * r_
                if f == 'wow': rx, ry = rx * 1.1, ry * 1.2
                if f == 'blink':
                    ln(d, [(cx - rx, cy), (cx + rx, cy + s * H * 0.01)], '#d8d8dc', lw * 1.2); continue
                if f == 'happy':                               # (a nasty glee: eyes squeezed into upturned crescents)
                    ln(d, arc(cx, cy + ry * 0.5, rx, ry * 0.7, 200, 340), '#d8d8dc', lw * 1.8); continue
                lx = rx * (0.45 if f == 'look' else 0)
                E(d, cx + lx, cy, rx, ry, '#050505', '#c8c8cc', lw * 0.6)
                E(d, cx + lx - rx * 0.3, cy - ry * 0.35, rx * 0.3, rx * 0.3, '#ffffff'); E(d, cx + lx + rx * 0.35, cy + ry * 0.4, rx * 0.12, rx * 0.12, '#ffffff')
            # the brows: heavy wedges sloping down to the middle (up and apart when amazed)
            for cx, cy, s, r_ in eyes:
                if f == 'wow':
                    ln(d, arc(cx, cy - H * 0.13, W * 0.07, H * 0.03, 200, 340), '#000000', lw * 2); continue
                lo = 0.06 if f == 'fierce' else 0.08
                d.polygon([(cx + s * W * 0.1, cy - H * 0.16), (cx - s * W * 0.09, cy - H * lo), (cx - s * W * 0.08, cy - H * (lo - 0.03)), (cx + s * W * 0.1, cy - H * 0.11)], fill=hexc('#000000'))
            # the mouth: a jagged grin on his left, two white fangs
            mx, my = W * 0.62, H * 0.7
            k = {'happy': 1.25, 'fierce': 1.2, 'wow': 0.7}.get(f, 1.0)
            if f == 'wow':
                d.polygon([(mx - W * 0.06, my - H * 0.04), (mx + W * 0.04, my - H * 0.06), (mx + W * 0.07, my + H * 0.03), (mx - W * 0.03, my + H * 0.05)], fill=hexc('#111111'), outline=hexc('#d8d8dc'))
            else:
                zz = [(mx - W * 0.16 * k, my + H * 0.02), (mx - W * 0.08 * k, my - H * 0.04 * k), (mx - W * 0.02, my + H * 0.02), (mx + W * 0.06 * k, my - H * 0.06 * k), (mx + W * 0.15 * k, my - H * 0.12 * k)]
                if f in ('fierce', 'happy'):                    # (open: the dark of his mouth under the jag)
                    d.polygon(zz + [(mx + W * 0.13 * k, my + H * 0.02), (mx - W * 0.04, my + H * 0.1 * k), (mx - W * 0.14 * k, my + H * 0.06)], fill=hexc('#0a0a0a'))
                ln(d, zz, '#d8d8dc', lw * 1.1)
                for fx, fy, up in ((-0.08, -0.04, False), (0.06, -0.06, False), (0.12, -0.1, True)):
                    x, y = mx + W * fx * k, my + H * fy * k
                    if up: d.polygon([(x - W * 0.02, y + H * 0.03), (x + W * 0.02, y + H * 0.03), (x, y - H * 0.04)], fill=hexc('#ffffff'))
                    else: d.polygon([(x - W * 0.025, y), (x + W * 0.025, y), (x + W * 0.005, y + H * 0.07)], fill=hexc('#ffffff'))
        return R.t(f'face{"_" + f if f else ""}', face_tex(BK, 7.6, 7.6, p, seed=95, hi=40, rim='#08080a', rim_a=120))
    for f in (None,) + FACES: face(f)
    cy = 7.6
    R.part('core', (0, cy, 0), None, lambda v, f: disc((0, cy, 0), 3.8, 1.0, hub, (0, cy, 0), face=R.fk(f), n=11), faced=True)

    def blade(v, f):
        pv = (0, cy, 0.0); B = []
        B += disc((0, cy, 0.1), 5.1, 0.25, steelr, pv, n=11)                                  # (the steel disc behind the hub)
        n = 16
        P_ = lambda r_, a_: (math.cos(a_) * r_, cy + math.sin(a_) * r_, 0.0)
        for i in range(n):                    # (the teeth: broad blades, hooked and swept round the same way, in the saw's plane)
            a = math.radians(i * 360 / n)
            t = steel if i % 2 else steeld
            B += chain([P_(4.0, a), P_(5.5, a + 0.1), P_(6.6, a + 0.3), P_(7.2, a + 0.55)], [2.1, 1.5, 0.7], 0.45, t, pv, (0.0, 0.0, -1.0), ext=0.25)
        if v == 'spin':
            B += [seg((math.cos(math.radians(a)) * 6.6, cy + math.sin(math.radians(a)) * 6.6, -0.5),
                      (math.cos(math.radians(a + 50)) * 6.6, cy + math.sin(math.radians(a + 50)) * 6.6, -0.5), 0.2, 0.2, R.t('spark', tex('#fff0a0', 96, 0.05)), pv, light=15)
                  for a in (0, 120, 240)]
        return B
    R.part('blade', (0, cy, 0.0), 'core', blade, variants=('spin',))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'blade': 'spin'}, _off=(0, 1.4, 0), blade=T(('z', 40))),
        'idle_a': dict(_off=(0, 0.4, 0), blade=T(('z', 10))),
        'idle_b': dict(_face='look', _off=(0, 0.6, 0), core=T(('y', -20), ('z', 8)), blade=T(('z', -10))),
        'spin_0': dict(_face='fierce', _v={'blade': 'spin'}, blade=T(('z', 0))), 'spin_1': dict(_face='fierce', _v={'blade': 'spin'}, blade=T(('z', 10))),
        'wind': dict(_face='fierce', _v={'blade': 'spin'}, _off=(0, 0.0, 1.6), core=T(('x', 20)), blade=T(('z', 20))),
        'strike': dict(_face='fierce', _v={'blade': 'spin'}, _off=(0, -0.6, -6.0), core=T(('x', -24)), blade=T(('z', 5))),
        'happy': dict(_face='happy', _off=(0, 1.2, 0), core=T(('z', 12)), blade=T(('z', -20))),
        'vanish': dict(_face='blink', _v={'blade': 'spin'}, core=T(('y', 90))),
    })
    return R.ns()


# ==================================================================================================== CHEFERONI - the pizza chef
def cheferoni():
    R = Rig('gz_cheferoni_', 1.0)
    CR, CRD, CH, INK = '#c8ab8e', '#a08468', '#f2e8b2', '#101010'
    crust = R.t('crust', lit(tex(CR, 101, 0.04), 4, 4, 4, a=60, rim=CRD))
    cheese = R.t('cheese', tex(CH, 102, 0.04, spots=[('#e8d68a', 0.15)]))
    hat, hatb = R.t('hat', lit(tex('#f8f8f8', 103, 0.02), 6, 6, 4, a=40, rim='#c4c4c4')), R.t('hatband', tex('#e2e2e2', 104, 0.02))
    yel, dough = R.t('limb', lit(tex('#f4e06a', 105, 0.03), 2, 8, 4, a=60, rim='#c8b040')), R.t('dough', lit(tex('#f4e6c4', 106, 0.03), 6, 6, 4, a=70))
    blk = R.t('arm', tex('#141414', 108, 0.02))
    pep = R.t('pep', tex('#b8362a', 107, 0.05, spots=[('#8a1a16', 0.15)]))

    def pizza_under(d, W, H):
        """the pizza: a crust rim, the cheese, eight slice cuts, pepperoni scattered all over (as drawn) - (2.96d) square, filling
        his square slab: the blocky look"""
        cx, cy, r = W / 2, H / 2, W * 0.5
        d.rectangle((0, 0, W - 1, H - 1), fill=hexc(CR), outline=hexc(CRD), width=int(W * 0.024))
        hs = r * 0.8
        d.rectangle((cx - hs, cy - hs, cx + hs, cy + hs), fill=hexc(CH), outline=hexc('#b89a72'), width=int(W * 0.01))
        rr = random.Random(110)
        for _ in range(48):                                   # (the cheese, melted unevenly)
            x, y = rr.uniform(cx - hs * 0.9, cx + hs * 0.9), rr.uniform(cy - hs * 0.9, cy + hs * 0.9)
            E(d, x, y, W * rr.uniform(0.02, 0.05), H * rr.uniform(0.015, 0.03), '#ead98e')
        for i in range(8):                                    # (the slice cuts, out to the crust)
            a = math.radians(i * 45 + 8); t = hs / max(abs(math.cos(a)), abs(math.sin(a)))
            ln(d, [(cx + math.cos(a) * r * 0.05, cy + math.sin(a) * r * 0.05), (cx + math.cos(a) * t, cy + math.sin(a) * t)], '#3e3020', W * 0.006)
        for _ in range(30):                                   # (pepperoni)
            x, y, s = rr.uniform(cx - hs * 0.85, cx + hs * 0.85), rr.uniform(cy - hs * 0.85, cy + hs * 0.85), W * rr.uniform(0.022, 0.042)
            if abs(x - cx) < W * 0.2 and H * 0.36 < y < H * 0.78: continue          # (not over his face)
            E(d, x, y, s, s, '#b8362a', '#7a1a12', W * 0.006); E(d, x - s * 0.3, y - s * 0.3, s * 0.25, s * 0.25, '#d86a5a')

    def face(f):
        """as drawn: angry slanted brows, small black eyes with a glint, a great black curly moustache over an open mouth
        with a red tongue, and a curl of hair over the crust at the top"""
        def p(d, W, H):
            lw = W * 0.012
            for i in range(4):                                # (the curly "wow" hair on top of the crust)
                x = W * (0.4 + i * 0.05)
                ln(d, arc(x, H * 0.035, W * 0.022, H * 0.022, 150, 520, n=20), INK, lw * 0.8)
            eyes = ((W * 0.41, H * 0.45, -1), (W * 0.59, H * 0.45, 1))
            for cx, cy, s in eyes:
                r = W * (0.022 if f != 'wow' else 0.03)
                if f == 'blink': ln(d, arc(cx, cy, r * 1.4, r * 0.6, 20, 160), INK, lw * 1.6); continue
                if f == 'happy': ln(d, arc(cx, cy + r * 0.6, r * 1.4, r * 1.1, 200, 340), INK, lw * 1.8); continue
                lx = r * (0.6 if f == 'look' else 0)
                E(d, cx + lx, cy, r, r * 1.15, INK); E(d, cx + lx - r * 0.35, cy - r * 0.4, r * 0.32, r * 0.32, '#ffffff')
            for cx, cy, s in eyes:                            # (the brows: angry, slanting down to the middle; up when happy or amazed)
                by = cy - H * 0.07
                if f in ('happy', 'wow'):
                    ln(d, arc(cx, by - H * 0.01, W * 0.04, H * 0.02, 200, 340), INK, lw * 2.2)
                else:
                    lo = 0.03 if f == 'fierce' else 0.02
                    ln(d, [(cx + s * W * 0.05, by - H * 0.025), (cx - s * W * 0.04, by + H * lo)], INK, lw * (3.2 if f == 'fierce' else 2.6))
            # the mouth, open below the moustache, a red tongue in it
            mx, my = W * 0.5, H * 0.63
            k = {'wow': 1.3, 'fierce': 1.25, 'happy': 1.15, 'blink': 0.8}.get(f, 1.0)
            d.chord((mx - W * 0.05 * k, my - H * 0.04 * k, mx + W * 0.05 * k, my + H * 0.075 * k), 0, 360 if f == 'wow' else 180, fill=hexc('#5a1410'), outline=hexc(INK), width=int(lw))
            E(d, mx, my + H * 0.045 * k, W * 0.03 * k, H * 0.022 * k, '#d84a4a')
            # the moustache: two great black curls
            for s in (-1, 1):
                pts = bez((mx, my - H * 0.03), (mx + s * W * 0.06, my - H * 0.08), (mx + s * W * 0.13, my - H * 0.05), (mx + s * W * 0.13, my - H * 0.1))
                ln(d, pts, INK, W * 0.032)
                ln(d, arc(mx + s * W * 0.115, my - H * 0.11, W * 0.022, H * 0.022, (0 if s > 0 else 180) - 90, (0 if s > 0 else 180) + 160 * s, n=12), INK, W * 0.016)
        return R.t(f'face{"_" + f if f else ""}', face_tex(CR, 10.8, 10.8, p, seed=108, hi=50, under=pizza_under))
    for f in (None,) + FACES: face(f)
    cy = 11.0
    R.part('pizza', (0, cy, 0), None, lambda v, f: disc((0, cy, 0), 5.4, 0.8, crust, (0, cy, 0), face=R.fk(f), n=11), faced=True)
    hpv = (-1.2, cy + 4.8, 0)                                  # (the hat, cocked over to his left - the viewer's right)
    R.part('hat', hpv, 'pizza', lambda v, f: turn([
        el((-3.0, cy + 4.4, -1.2), (0.6, cy + 6.2, 1.2), hatb, hpv),
        *ball((-1.2, cy + 7.4, 0), 2.3, hat, hpv, yr=1.6, zr=2.0),
        *ball((-2.4, cy + 7.8, 0), 1.25, hat, hpv, yr=1.2, zr=1.5, n=4), *ball((0.0, cy + 7.9, 0), 1.25, hat, hpv, yr=1.2, zr=1.5, n=4)],
        (0.0, 0.0, 18.0), mo(hpv, hpv)))
    for s, n in ((1, 'armr'), (-1, 'arml')):                  # (thin black arms)
        pv = (s * 5.0, cy - 1.0, 0)
        R.part(n, pv, 'pizza', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 2.0, pv[1] - 2.6, -0.4), (pv[0] + s * 2.4, pv[1] - 5.2, -0.8)],
                                                                [0.28, 0.28], 0.28, blk, pv) + [el((pv[0] + s * 2.4 - 0.35, pv[1] - 5.6, -1.1), (pv[0] + s * 2.4 + 0.35, pv[1] - 5.0, -0.5), blk, pv)])(pv, s))
    for s, n in ((1, 'legr'), (-1, 'legl')):                  # (long yellow legs, round yellow feet)
        pv = (s * 1.8, cy - 5.0, 0)
        R.part(n, pv, 'pizza', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 0.4, 0.8, 0)], [0.6], 0.6, yel, pv) +
                                                         ball((pv[0] + s * 0.4, 0.55, -0.6), 0.95, yel, pv, yr=0.55, zr=1.3, n=3))(pv, s))
    hand = (5.0 + 2.4, cy - 6.0, -0.8)
    def round_dough():                       # (a round flat sheet of dough, sliced across like the pizza)
        n, r = 9, 3.4
        out = []
        for i in range(n):
            z0 = hand[2] - r + i * 2 * r / n; z1 = z0 + 2 * r / n; zc = (z0 + z1) / 2 - hand[2]
            near = 0.0 if z0 < hand[2] < z1 else min(abs(z0 - hand[2]), abs(z1 - hand[2]))
            w = r * max(0.3, math.sqrt(max(0.0, 1 - (near / r) ** 2)))
            out.append(el((hand[0] - w, hand[1] - 0.25 - (0.12 if abs(zc) < 1 else 0), z0), (hand[0] + w, hand[1] + 0.25, z1), dough, hand, shift=(0.1 * i, 0.2 * i)))
        return out
    R.part('dough', hand, 'armr', lambda v, f: (round_dough()
                                                if v != 'slice' else
                                                [seg((hand[0], hand[1], hand[2] - 3.0), (hand[0], hand[1], hand[2] + 2.0), 0.6, 0.5, crust, hand),
                                                 *[seg((hand[0] - k, hand[1], hand[2] - 2.4 + k * 1.6), (hand[0] + k, hand[1], hand[2] - 2.4 + k * 1.6), 0.9, 0.3, cheese, hand)
                                                   for k in (2.4, 1.8, 1.2, 0.6)],
                                                 el((hand[0] - 0.7, hand[1] + 0.15, hand[2] - 1.0), (hand[0] + 0.7, hand[1] + 0.4, hand[2] + 0.4), pep, hand)]),
           variants=('slice',))
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 1.0, 0), _hide=('dough',), armr=L(('z', 70)), arml=L(('z', -70))),
        'idle_a': dict(_hide=('dough',), armr=L(('z', -6)), arml=L(('x', 20), ('z', 30)), pizza=T(('z', -3))),       # (a hand on his hip... roughly)
        'idle_b': dict(_face='look', _hide=('dough',), pizza=T(('y', -16), ('z', 6)), armr=L(('x', -40), ('z', 30)), hat=T(('z', -8))),
        'toss_0': dict(_face='happy', armr=L(('x', -70)), arml=L(('z', -20))),
        'toss_1': dict(_face='wow', _o_dough=(0, 9.0, 0), armr=L(('x', -150)), arml=L(('z', -60)), dough=T(('y', 60))),     # (the dough spinning up overhead)
        'wind': dict(_face='fierce', _v={'dough': 'slice'}, pizza=T(('y', 24)), armr=L(('x', 70), ('z', 20)), arml=L(('x', -30))),
        'strike': dict(_face='fierce', _v={'dough': 'slice'}, _o_dough=(0, 2.0, -12.0), pizza=T(('y', -20)), armr=L(('x', -100)), arml=L(('x', 30)), dough=T(('x', 90))),
        'happy': dict(_face='happy', _off=(0, 0.6, 0), _hide=('dough',), armr=L(('z', 140)), arml=L(('z', -140)), hat=T(('z', 12))),
        'vanish': dict(_face='happy', _hide=('dough',), pizza=T(('y', 60)), armr=L(('x', -90), ('z', 40)), hat=T(('x', -20))),       # (a bow)
    })
    return R.ns()


RIGS = {}
for _n, _f in (('grace', grace), ('robo', robo), ('zapper', zapper), ('dessa', dessa), ('bubbles', bubbles), ('chase', chase),
               ('limer', limer), ('chico', chico), ('spike', spike), ('cheferoni', cheferoni)):
    RIGS[_n] = _f()
# (each Buddy's own moves, past the shared ones: the attack names its wind-up and strike)
MOVES = {'grace': ('flap_0', 'flap_1', 'DIVE-PECK'), 'robo': ('stomp_up', 'stomp', 'ROCKET PUNCH'), 'zapper': ('bob_0', 'bob_1', 'ZAP'),
         'dessa': ('flicker', 'idle_a', 'FLASH-BURST'), 'bubbles': ('bounce_0', 'bounce_1', 'POP-SPLASH'), 'chase': ('hop_0', 'hop_1', 'TACKLE'),
         'limer': ('roll_0', 'roll_1', 'BODY SLAM'), 'chico': ('wobble_0', 'wobble_1', 'SWING-WHACK'), 'spike': ('spin_0', 'spin_1', 'BUZZ-SAW DASH'),
         'cheferoni': ('toss_0', 'toss_1', 'SLICE THROW')}
