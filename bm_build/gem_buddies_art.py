"""2.95e: THE GEM'S BUDDIES - the ten the Gem of Creativity conjures for a moment to fight beside it, each a small 3D rig in the
pack's blocky follower style (the owner's drawings are the design reference only - shapes and colours - never the textures):

  GRACE      a hummingbird: green, a pink crest and pink-edged wings, a long dark beak.     flap / DIVE-PECK
  ROBO       a boxy grey robot: a screen face, long arms with claws, thruster feet.          STOMP / ROCKET PUNCH
  ZAPPER     a curious little lightning bolt, all spikes, a green button nose.               curious bob / ZAP
  DESSA      a light bulb with a sleepy happy face, a screw base, wiry arms.                 flicker / FLASH-BURST
  BUBBLES    a PAIR of bubbles (a big one and its little one), blue and shiny.               bounce in tandem / POP-SPLASH
  CHASE      a green gummy blob with two lobes on top, stubby arms and legs.                 squash-and-stretch hop / TACKLE
  LIMER      the round fellow - a pale ball wearing a green leafy covering - on stick legs.  roll / BODY SLAM
  CHICO      a drumstick: the meat is his head, the bone his body.                           wobble / SWING-WHACK
  SPIKE      a saw blade round a black ball with an angry face.                              spin up / BUZZ-SAW DASH
  CHEFERONI  a pizza in a chef's hat, a big moustache, on yellow stick legs.                 toss the dough / SLICE THROW

Each is a rigkit rig (an object with PREFIX, PIVOT, PARENT, PARTS, POSES, HIDDEN, model_name, models, textures, RIG_SCALE): RIGS
below, by name. Design units: feet at y=0, facing -z, its right is +x. Every one has the poses appear (popping out of a sparkle),
idle_a, idle_b, its wind-up and strike, happy and vanish; GROW gives the display scale through appear/vanish (they pop in small and
pop out small). Faces are a model per expression on the part with the face (pose key _face); some parts have a variant shape (pose
key _v: {part: variant} - Chase's squash and stretch, Bubbles' pop, Dessa's lit glass)."""
import math
import random
from types import SimpleNamespace
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg, chain

GROW = {'appear': (0.15, 1.15, 1.0), 'vanish': (1.0, 1.2, 0.0)}     # (the display's scale, keyframe by keyframe)
def T(*r):
    """a trunk's turn (body, head, core...): ('x', -a) leans it FORWARD (nose down), ('x', +a) back"""
    return qs(*[(a, -d if a == 'x' else d) for a, d in r])


def L(*r):
    """a limb's turn (arms, legs, wings, lobes): ('z', +a) swings it OUT and up on its own side (the right one; the left mirrors with -a)"""
    return qs(*[(a, -d if a == 'z' else d) for a, d in r])


FACES = ('blink', 'happy', 'fierce', 'wow', 'look')
DRAFT = ['appear', 'idle_a', 'idle_b', 'wind', 'strike', 'happy', 'vanish']


# ==================================================================================================== painting
def tex(col, seed, var=0.05, cell=2, size=64, spots=None):
    """a hand-painted coat: one colour in 2-px cells, each a touch lighter or darker (a little life in it); spots: [(colour, p)]"""
    im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im); r = random.Random(seed); c = hexc(col)
    for y in range(0, size, cell):
        for x in range(0, size, cell):
            k = 1 + (r.random() - 0.5) * 2 * var
            cc = tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)
            for sc, p in (spots or ()):
                if r.random() < p: cc = hexc(sc)
            d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=cc)
    return im


def lit(im, w, h, ppu=8, hi='#ffffff', a=110, rim=None, rim_a=150):
    """light from the upper left over the (w x h unit) window at the top left of a texture, a darker rim at the lower right"""
    px = im.load(); W, H = int(w * ppu), int(h * ppu)
    for y in range(H):
        for x in range(W):
            u, v = (x + 0.5) / W - 0.32, (y + 0.5) / H - 0.28
            g = max(0.0, 1 - math.hypot(u * 1.6, v * 1.6) * 1.6)
            c = px[x, y]
            if g > 0:
                t = hexc(hi); k = g * a / 255
                c = tuple(int(c[i] * (1 - k) + t[i] * k) for i in range(3)) + (255,)
            if rim:
                e = max(0.0, (x + 0.5) / W + (y + 0.5) / H - 1.45) * 2.2
                if e > 0:
                    t = hexc(rim); k = min(1.0, e) * rim_a / 255
                    c = tuple(int(c[i] * (1 - k) + t[i] * k) for i in range(3)) + (255,)
            px[x, y] = c
    return im


def oval(d, cx, cy, rx, ry, fill, outline=None, width=1):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=fill, outline=outline, width=width)


def eye(d, cx, cy, rx, ry, kind=None, iris='#2a2a2a', white='#ffffff', ink='#141414', look=(0, 0), lid=None, angry=0):
    """a big cartoon eye: a white, a dark pupil looking `look`, two glints; blink: a curved closed line; happy: an upturned arc;
    fierce: a brow slanting in (angry: +1 for the right eye, -1 the left); wow: wide, the pupil small"""
    if kind == 'blink':
        d.arc((cx - rx, cy - ry * 0.6, cx + rx, cy + ry * 0.9), 20, 160, fill=ink, width=max(2, int(rx / 2.5))); return
    if kind == 'happy':
        d.arc((cx - rx, cy - ry * 0.3, cx + rx, cy + ry * 1.5), 200, 340, fill=ink, width=max(2, int(rx / 2.5))); return
    ry2 = ry * (1.15 if kind == 'wow' else 1.0)
    oval(d, cx, cy, rx, ry2, hexc(white), hexc(ink), max(1, int(rx / 4)))
    pr = rx * (0.38 if kind == 'wow' else 0.55)
    lx, ly = look
    oval(d, cx + lx * rx * 0.35, cy + ly * ry * 0.3 + ry * 0.12, pr, pr * 1.2, hexc(iris))
    oval(d, cx + lx * rx * 0.35 - pr * 0.35, cy + ly * ry * 0.3 - pr * 0.3, pr * 0.32, pr * 0.32, hexc('#ffffff'))
    oval(d, cx + lx * rx * 0.35 + pr * 0.4, cy + ly * ry * 0.3 + pr * 0.55, pr * 0.15, pr * 0.15, hexc('#ffffff'))
    if kind == 'fierce':                                     # (the brow, cutting across the top of the eye)
        s = angry or 1
        d.polygon([(cx - rx * 1.2, cy - ry * (1.25 if s > 0 else 0.35)), (cx + rx * 1.2, cy - ry * (0.35 if s > 0 else 1.25)),
                   (cx + rx * 1.2, cy - ry * (1.55 if s > 0 else 1.55)), (cx - rx * 1.2, cy - ry * 1.55)], fill=lid or hexc(ink))


def mouth(d, cx, cy, w, kind, ink='#141414', inner='#7a1c26', tongue='#e0607a'):
    """smile / grin (open, a tongue) / o (surprised) / wavy / frown / fangs (a jagged angry grin)"""
    I = hexc(ink); lw = max(2, int(w / 6))
    if kind == 'smile':
        d.arc((cx - w, cy - w * 0.7, cx + w, cy + w * 0.6), 25, 155, fill=I, width=lw)
    elif kind == 'grin':
        d.chord((cx - w, cy - w * 0.5, cx + w, cy + w * 0.9), 0, 180, fill=hexc(inner), outline=I, width=lw)
        oval(d, cx, cy + w * 0.55, w * 0.45, w * 0.22, hexc(tongue))
    elif kind == 'o':
        oval(d, cx, cy + w * 0.2, w * 0.45, w * 0.55, hexc(inner), I, lw)
    elif kind == 'wavy':
        pts = [(cx - w + i * w / 4, cy + (2 if i % 2 else -2) * w / 10) for i in range(9)]
        d.line(pts, fill=I, width=lw)
    elif kind == 'frown':
        d.arc((cx - w * 0.8, cy, cx + w * 0.8, cy + w), 205, 335, fill=I, width=lw)
    elif kind == 'fangs':
        d.chord((cx - w, cy - w * 0.4, cx + w, cy + w * 0.8), 0, 180, fill=hexc(inner), outline=I, width=lw)
        for i in range(4):
            x = cx - w * 0.75 + i * w * 0.5
            d.polygon([(x - w * 0.2, cy + w * 0.08), (x + w * 0.2, cy + w * 0.08), (x, cy + w * 0.4)], fill=hexc('#ffffff'))


FACE_MOUTH = {None: 'smile', 'blink': 'smile', 'happy': 'grin', 'fierce': 'fangs', 'wow': 'o', 'look': 'smile'}


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


def ball(c, r, tex_, pv, yr=None, zr=None, shift=(0.0, 0.0), light=0, face=None, n=7):
    """a round ball, sliced: n layers, each a cross of two boxes as wide as the sphere is there - round from every side.
    face: a texture painted over the whole front (the window 2r x 2yr at the top left of it) - laid over the front of every
    slice at its own depth, so the face sits ON the ball"""
    x, y, z = c; ry, rz = yr or r, zr or r
    L = []
    for i in range(n):
        y0 = y - ry + i * 2 * ry / n; y1 = y0 + 2 * ry / n
        near = 0.0 if y0 < y < y1 else min(abs(y0 - y), abs(y1 - y))
        f = max(0.38, math.sqrt(max(0.0, 1 - (near / ry) ** 2)))
        for j, (kx, kz) in enumerate(((f, f * 0.74), (f * 0.74, f))):
            e = el((x - r * kx, y0, z - rz * kz), (x + r * kx, y1, z + rz * kz), tex_, pv, shift=(shift[0] + 0.13 * i + 0.4 * j, shift[1] + 0.29 * i), light=light)
            if face:
                x0, x1 = x - r * kx, x + r * kx
                e['faces']['north'] = {'uv': [round((x + r) - x1, 4), round((y + ry) - y1, 4), round((x + r) - x0, 4), round((y + ry) - y0, 4)], 'texture': '#' + face}
            L.append(e)
    return L


def disc(c, r, th, tex_, pv, face=None, n=9, light=0):
    """a flat round disc standing up, facing front (a pizza): n strips across, the face over the front of all of them"""
    x, y, z = c; L = []
    for i in range(n):
        y0 = y - r + i * 2 * r / n; y1 = y0 + 2 * r / n
        near = 0.0 if y0 < y < y1 else min(abs(y0 - y), abs(y1 - y))
        f = max(0.3, math.sqrt(max(0.0, 1 - (near / r) ** 2)))
        e = el((x - r * f, y0, z - th), (x + r * f, y1, z + th), tex_, pv, shift=(0.11 * i, 0.23 * i), light=light)
        if face:
            e['faces']['north'] = {'uv': [round(r - r * f, 4), round((y + r) - y1, 4), round(r + r * f, 4), round((y + r) - y0, 4)], 'texture': '#' + face}
        L.append(e)
    return L


def plate(fr, to, tex_, pv, w, h, light=0):
    """a face plate on the front (north) of a box: the window w x h units at the top left of the face texture"""
    return el(fr, to, tex_, pv, faces=('north',), uv={'north': [0, 0, w, h]}, light=light)


def face_tex(base, w, h, paint, ppu=8, seed=1, var=0.03, hi=110, rim=None, fw=None, fh=None, fy=0.5, rim_a=150):
    """a face texture: the base colour painted and lit over the w x h window (a whole ball's front), then paint(draw, W, H) draws
    the face (pixels) in an fw x fh box within it, centred across and fy of the way down"""
    size = 128
    im = lit(tex(base, seed, var, 2, size), w, h, ppu, a=hi, rim=rim, rim_a=rim_a)
    fw, fh = fw or w, fh or h
    lay = Image.new('RGBA', (int(fw * ppu), int(fh * ppu)), (0, 0, 0, 0)); paint(ImageDraw.Draw(lay), fw * ppu, fh * ppu)
    im.alpha_composite(lay, (int((w - fw) / 2 * ppu), int(max(0, fy * h - fh / 2) * ppu)))
    return im


def looks(face):
    return {'look': (1, -0.2)}.get(face, (0, 0))


# ==================================================================================================== GRACE - the hummingbird
def grace():
    R = Rig('gb_grace_', 1.0)
    G, GL, PINK, PINKL, BEAK = '#5cae2e', '#8ed34a', '#d8409a', '#f07cc4', '#3a3530'
    body, belly = R.t('body', lit(tex(G, 11, 0.07), 6, 6, 4, a=70)), R.t('belly', tex('#cfe9a0', 12, 0.05))
    wing, wing2 = R.t('wing', tex(PINK, 13, 0.08, spots=[(GL, 0.12)])), R.t('wing_g', tex(G, 14, 0.08, spots=[(PINK, 0.1)]))
    crest, beak = R.t('crest', tex(PINK, 15, 0.1, spots=[(PINKL, 0.25)])), R.t('beak', tex(BEAK, 16, 0.05))

    def face(f):
        def p(d, W, H):
            eye(d, W * 0.24, H * 0.42, W * 0.16, H * 0.2, f, iris='#1c1410', look=looks(f), angry=1)
            eye(d, W * 0.76, H * 0.42, W * 0.16, H * 0.2, f, iris='#1c1410', look=looks(f), angry=-1)
            oval(d, W * 0.12, H * 0.78, W * 0.09, H * 0.06, hexc('#f08cb4'))         # (rosy cheeks)
            oval(d, W * 0.88, H * 0.78, W * 0.09, H * 0.06, hexc('#f08cb4'))
        return R.t(f'face{"_" + f if f else ""}', face_tex(G, 4.4, 4.0, p, seed=17, hi=90, rim='#3a7a1c', rim_a=110, fw=4.2, fh=3.0, fy=0.52))
    for f in (None,) + FACES: face(f)
    HY = 13.0
    R.part('body', (0, 9.0, 0), None, lambda v, f: [
        *ball((0, 9.0, 0.6), 2.4, body, (0, 9.0, 0), yr=2.6, zr=3.0),
        el((-1.6, 6.8, -2.0), (1.6, 9.6, -1.6), belly, (0, 9.0, 0), faces=('north', 'down'))])
    R.part('head', (0, 11.4, -1.4), 'body', lambda v, f: [
        *ball((0, HY, -2.0), 2.2, body, (0, 11.4, -1.4), yr=2.0, zr=2.0, shift=(0.4, 0.1), face=R.prefix + 'face' + (f'_{f}' if f else '')),
        seg((0, HY - 0.6, -4.0), (0, HY - 2.2, -10.5), 0.55, 0.55, beak, (0, 11.4, -1.4)),
        *chain([(0, HY + 1.8, -1.6), (0, HY + 4.0, 0.2), (0, HY + 4.6, 2.4)], [1.0, 0.7], 0.5, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0)),
        *chain([(0.7, HY + 1.6, -1.0), (1.4, HY + 3.6, 0.6), (1.6, HY + 3.8, 2.2)], [0.8, 0.5], 0.4, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0)),
        *chain([(-0.7, HY + 1.6, -1.0), (-1.4, HY + 3.6, 0.6), (-1.6, HY + 3.8, 2.2)], [0.8, 0.5], 0.4, crest, (0, 11.4, -1.4), (0.0, 0.0, -1.0))],
        faced=True)
    for s, n in ((1, 'wingr'), (-1, 'wingl')):
        pv = (s * 2.0, 10.4, 0.2)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: [
            el((pv[0] + (0 if s > 0 else -7.5), pv[1] - 0.2, pv[2] - 1.6), (pv[0] + (7.5 if s > 0 else 0), pv[1] + 0.2, pv[2] + 2.0), wing, pv),
            el((pv[0] + (0 if s > 0 else -4.5), pv[1] - 0.25, pv[2] - 1.8), (pv[0] + (4.5 if s > 0 else 0), pv[1] + 0.25, pv[2] + 0.6), wing2, pv)])(pv, s))
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
    R = Rig('gb_robo_', 1.0)
    GREY, GREYD, GREYL, RED = '#8a9096', '#5c6268', '#b8bec4', '#d83a2a'
    metal = R.t('metal', lit(tex(GREY, 21, 0.06, spots=[('#7a8086', 0.08)]), 8, 8, 4, a=60, rim='#3a3e44'))
    dark, light_ = R.t('dark', tex(GREYD, 22, 0.05)), R.t('light', tex(GREYL, 23, 0.04))
    rust, flame = R.t('panel', tex('#c8a432', 24, 0.06)), R.t('flame', tex('#ffb030', 25, 0.15, spots=[('#ff6a20', 0.3), ('#fff2a0', 0.2)]))

    def face(f):
        def p(d, W, H):                                   # (a screen: two glowing eyes that change, a mouth of dots)
            d.rounded_rectangle((W * 0.06, H * 0.08, W * 0.94, H * 0.92), radius=int(W * 0.1), fill=hexc('#14202a'), outline=hexc('#2c3a46'), width=3)
            E = '#7ff0ff' if f != 'fierce' else '#ff5040'
            for cx, s in ((0.32, 1), (0.68, -1)):
                x, y = W * cx, H * 0.42
                if f == 'blink': d.rectangle((x - W * 0.1, y, x + W * 0.1, y + H * 0.04), fill=hexc(E))
                elif f == 'happy': d.arc((x - W * 0.1, y - H * 0.06, x + W * 0.1, y + H * 0.16), 200, 340, fill=hexc(E), width=4)
                elif f == 'fierce':
                    d.polygon([(x - W * 0.11, y - H * 0.1 * s), (x + W * 0.11, y + H * 0.1 * s), (x + W * 0.11, y + H * 0.14), (x - W * 0.11, y + H * 0.14)], fill=hexc(E))
                else:
                    r = W * (0.13 if f == 'wow' else 0.1); lx = looks(f)[0] * W * 0.04
                    d.ellipse((x - r + lx, y - r, x + r + lx, y + r), fill=hexc(E))
                    d.ellipse((x - r * 0.4 + lx, y - r * 0.6, x - r * 0.05 + lx, y - r * 0.25), fill=hexc('#ffffff'))
            k = {None: 'smile', 'blink': 'smile', 'look': 'smile', 'happy': 'grin', 'fierce': 'flat', 'wow': 'o'}[f]
            y = H * 0.74
            if k == 'o': d.ellipse((W * 0.44, y - H * 0.06, W * 0.56, y + H * 0.08), outline=hexc(E), width=3)
            else:
                for i in range(5):
                    x = W * (0.3 + i * 0.1); dy = {'smile': (1 - ((i - 2) / 2) ** 2) * H * 0.05, 'grin': (1 - ((i - 2) / 2) ** 2) * H * 0.09, 'flat': 0}[k]
                    d.rectangle((x - 3, y + dy - 3, x + 3, y + dy + 3), fill=hexc(E))
        return R.t(f'face{"_" + f if f else ""}', face_tex(GREY, 6.0, 4.6, p, seed=26, hi=40))
    for f in (None,) + FACES: face(f)
    by = 9.0
    R.part('body', (0, by, 0), None, lambda v, f: [
        el((-3.6, by - 3.0, -2.4), (3.6, by + 3.6, 2.4), metal, (0, by, 0)),
        el((-2.4, by - 1.8, -2.62), (2.4, by + 1.6, -2.4), rust, (0, by, 0), faces=('north',)),           # (the chest panel)
        el((-0.8, by - 0.8, -2.8), (0.8, by + 0.6, -2.6), R.t('lamp', tex(RED, 27, 0.05)), (0, by, 0), faces=('north', 'east', 'west', 'up', 'down'), light=12),
        el((-2.8, by - 4.2, -1.8), (2.8, by - 3.0, 1.8), dark, (0, by, 0))])
    hy = by + 3.6
    R.part('head', (0, hy, 0), 'body', lambda v, f: [
        el((-3.2, hy + 0.2, -2.6), (3.2, hy + 5.0, 2.4), metal, (0, hy, 0), shift=(0.3, 0.5)),
        plate((-3.0, hy + 0.3, -2.63), (3.0, hy + 4.9, -2.6), R.prefix + 'face' + (f'_{f}' if f else ''), (0, hy, 0), 6.0, 4.6, light=6),
        el((-0.25, hy + 5.0, -0.25), (0.25, hy + 7.0, 0.25), dark, (0, hy, 0)),                            # (the antenna)
        el((-0.6, hy + 7.0, -0.6), (0.6, hy + 8.2, 0.6), R.t('bulb', tex(RED, 28, 0.08)), (0, hy, 0), light=14),
        el((-3.8, hy + 1.6, -1.0), (-3.2, hy + 3.4, 1.0), dark, (0, hy, 0)), el((3.2, hy + 1.6, -1.0), (3.8, hy + 3.4, 1.0), dark, (0, hy, 0))],
        faced=True)
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 4.2, by + 2.6, 0)
        def arm(v, f, pv=pv, s=s):
            x = pv[0]; y = pv[1]
            L = [el((x - 0.9, y - 1.0, -1.0), (x + 0.9, y + 1.0, 1.0), dark, pv),                              # (the shoulder)
                 seg((x + s * 0.4, y, 0), (x + s * 0.9, y - 7.0, 0), 0.9, 0.9, light_, pv),
                 el((x + s * 0.9 - 1.3, y - 8.4, -1.3), (x + s * 0.9 + 1.3, y - 6.8, 1.3), dark, pv)]
            for c in (-1, 1):                                                                                 # (the claw)
                L.append(seg((x + s * 0.9, y - 8.4, c * 0.7), (x + s * 0.9, y - 10.6, c * 1.4), 0.6, 0.5, metal, pv))
            if v == 'rocket':
                L.append(el((x + s * 0.9 - 0.7, y - 0.5, -0.7), (x + s * 0.9 + 0.7, y + 0.7, 0.7), flame, pv, light=15))
            return L
        R.part(n, pv, 'body', arm, variants=('rocket',))
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.8, by - 4.0, 0)
        R.part(n, pv, None if False else 'body', (lambda pv: lambda v, f: [
            seg((pv[0], pv[1], 0), (pv[0], 2.4, 0), 1.0, 1.0, light_, pv),
            el((pv[0] - 1.4, 0.4, -1.8), (pv[0] + 1.4, 2.6, 1.6), metal, pv),                                   # (the thruster foot)
            el((pv[0] - 1.0, 0.0, -1.2), (pv[0] + 1.0, 0.4, 1.0), dark, pv)] +
            ([el((pv[0] - 0.8, -1.6, -0.8), (pv[0] + 0.8, 0.0, 0.8), flame, pv, light=15)] if v == 'jet' else []))(pv), variants=('jet',))
    arms = lambda r, l: dict(armr=L(('x', r[0]), ('z', r[1])), arml=L(('x', l[0]), ('z', l[1])))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'legr': 'jet', 'legl': 'jet'}, _off=(0, 3.0, 0), **arms((0, 60), (0, -60))),
        'idle_a': dict(**arms((4, 6), (-4, -6)), head=T(('x', 3))),
        'idle_b': dict(_face='look', **arms((0, 10), (20, -8)), head=T(('y', -22), ('z', 6)), body=T(('y', 6))),
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
    R = Rig('gb_zapper_', 1.0)
    Y, YL, YD = '#f6d21e', '#fff27a', '#d8a40c'
    gold = R.t('bolt', lit(tex(Y, 31, 0.05, spots=[(YL, 0.08)]), 6, 6, 4, a=90, rim=YD))
    hot = R.t('hot', tex('#fffbe0', 32, 0.04, spots=[(YL, 0.3)]))
    blue = R.t('ice', tex('#9ad8f4', 33, 0.05))

    def face(f):
        def p(d, W, H):
            eye(d, W * 0.3, H * 0.4, W * 0.16, H * 0.2, f, iris='#3a2a0a', look=looks(f) if f else (0.5, -0.3), angry=1)
            eye(d, W * 0.7, H * 0.36, W * 0.14, H * 0.18, f, iris='#3a2a0a', look=looks(f) if f else (0.5, -0.3), angry=-1)
            oval(d, W * 0.52, H * 0.62, W * 0.08, H * 0.07, hexc('#2ca850'), hexc('#1a6a30'), 2)       # (the green button nose)
            mouth(d, W * 0.52, H * 0.78, W * 0.1, {None: 'wavy', 'look': 'o', 'blink': 'smile'}.get(f, FACE_MOUTH[f]))
        return R.t(f'face{"_" + f if f else ""}', face_tex(Y, 5.0, 4.6, p, seed=34, hi=120))
    for f in (None,) + FACES: face(f)
    cy = 9.0
    def core(v, f):
        t = hot if v == 'charged' else gold
        L = [el((-2.5, cy - 2.2, -1.6), (2.5, cy + 2.4, 1.6), t, (0, cy, 0), light=10 if v else 6),
             plate((-2.5, cy - 2.2, -1.63), (2.5, cy + 2.4, -1.6), R.prefix + 'face' + (f'_{f}' if f else ''), (0, cy, 0), 5.0, 4.6, light=10)]
        for a, ln in ((90, 3.6), (40, 4.4), (140, 3.0), (-15, 3.2), (195, 2.8), (65, 2.4)):            # (spikes all round the edge)
            r = math.radians(a); A = (math.cos(r) * 2.0, cy + math.sin(r) * 1.9, 0.0); B = (math.cos(r) * (2.0 + ln), cy + math.sin(r) * (1.9 + ln), 0.0)
            L.append(seg(A, B, 1.1, 1.0, t, (0, cy, 0), (0.0, 0.0, -1.0), light=8))
        if v == 'charged':
            L += [seg((-2.6, cy + 1.0, -1.0), (-5.6, cy + 3.4, -2.0), 0.3, 0.3, blue, (0, cy, 0), light=15),
                  seg((2.6, cy - 1.0, -1.0), (5.8, cy - 2.6, -2.2), 0.3, 0.3, blue, (0, cy, 0), light=15)]
        return L
    R.part('core', (0, cy, 0), None, core, variants=('charged',), faced=True)
    R.part('tail', (0, cy - 2.0, 0), 'core', lambda v, f: chain([(0.6, cy - 2.0, 0.4), (-1.8, cy - 4.6, 0.6), (1.2, cy - 6.2, 0.8), (-0.6, cy - 8.4, 1.0)],
                                                              [1.8, 1.4, 1.0], 1.2, gold, (0, cy - 2.0, 0), (0.0, 0.0, -1.0)))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 2.4, cy - 0.4, 0)
        R.part(n, pv, 'core', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.6, pv[1] - 1.2, -0.2), (pv[0] + s * 2.6, pv[1] - 0.2, -0.4)],
                                                                [0.7, 0.55], 0.6, gold, pv, (0.0, 0.0, -1.0)))(pv, s))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'core': 'charged'}, _off=(0, 1.4, 0), core=T(('z', 18))),
        'idle_a': dict(_off=(0, 0.8, 0), core=T(('z', -10)), tail=T(('z', 8)), armr=L(('z', 10)), arml=L(('z', -20))),
        'idle_b': dict(_face='look', _off=(0, 1.4, 0), core=T(('z', 24), ('y', -18)), tail=T(('z', -12)), armr=L(('z', -30))),     # (head cocked - curious)
        'bob_0': dict(_face='look', _off=(0, 2.0, 0), core=T(('z', 30), ('x', -10)), tail=T(('z', -20)), armr=L(('z', 40)), arml=L(('z', -10))),
        'bob_1': dict(_face='wow', _off=(0, 0.4, 0), core=T(('z', -26), ('y', 20)), tail=T(('z', 18)), armr=L(('z', -10)), arml=L(('z', 40))),
        'wind': dict(_face='fierce', _v={'core': 'charged'}, _off=(0, 2.4, 1.6), core=T(('x', 18)), armr=L(('z', 60)), arml=L(('z', -60)), tail=T(('x', -20))),
        'strike': dict(_face='fierce', _v={'core': 'charged'}, _off=(0, 0.0, -5.0), core=T(('x', -36)), armr=L(('z', -20)), arml=L(('z', 20)), tail=T(('x', 30))),
        'happy': dict(_face='happy', _off=(0, 2.0, 0), core=T(('z', -16)), armr=L(('z', 70)), arml=L(('z', -70)), tail=T(('z', 16))),
        'vanish': dict(_face='blink', _v={'core': 'charged'}, _off=(0, 3.0, 0), core=T(('y', 180))),
    })
    return R.ns()


# ==================================================================================================== DESSA - the light bulb
def dessa():
    R = Rig('gb_dessa_', 1.0)
    GL, GLD = '#f8e64a', '#e0c020'
    glass = {None: R.t('glass', lit(tex(GL, 41, 0.04), 8, 8, 4, a=130, rim=GLD, rim_a=110)),
             'dim': R.t('glass_dim', lit(tex('#b8a838', 42, 0.04), 8, 8, 4, a=60)),
             'flash': R.t('glass_flash', tex('#fffce8', 43, 0.03))}
    base, ring = R.t('base', tex('#8c9094', 44, 0.06)), R.t('ring', tex('#5e6266', 45, 0.05))
    wire = R.t('wire', tex('#3a3a3a', 46, 0.04))
    fil = R.t('filament', tex('#ff9a30', 47, 0.1))

    def face(f, v):
        col = {None: GL, 'dim': '#b8a838', 'flash': '#fffce8'}[v]
        def p(d, W, H):          # (her look: eyes closed in two happy curves, a little wavy smile - sleepy and sweet)
            k = {None: 'happy', 'happy': 'happy', 'blink': 'blink', 'look': None, 'wow': 'wow', 'fierce': 'fierce'}[f]
            eye(d, W * 0.3, H * 0.42, W * 0.14, H * 0.17, k, iris='#4a3a10', look=looks(f), angry=1)
            eye(d, W * 0.7, H * 0.42, W * 0.14, H * 0.17, k, iris='#4a3a10', look=looks(f), angry=-1)
            mouth(d, W * 0.5, H * 0.7, W * 0.13, {None: 'wavy', 'happy': 'grin', 'blink': 'wavy', 'look': 'smile', 'wow': 'o', 'fierce': 'fangs'}[f])
            oval(d, W * 0.16, H * 0.66, W * 0.07, H * 0.05, hexc('#f4a040'))
            oval(d, W * 0.84, H * 0.66, W * 0.07, H * 0.05, hexc('#f4a040'))
        return R.t(f'face{"_" + v if v else ""}{"_" + f if f else ""}', face_tex(col, 7.2, 7.6, p, seed=48, hi=120 if v != 'dim' else 50, rim=None if v == 'flash' else '#c8a010', rim_a=90, fw=5.6, fh=4.8, fy=0.52))
    for v in (None, 'dim', 'flash'):
        for f in (None,) + FACES: face(f, v)
    gy = 10.4
    def bulb(v, f):
        lt = {None: 11, 'dim': 3, 'flash': 15}[v]
        L = ball((0, gy, 0), 3.6, glass[v], (0, gy, 0), yr=3.8, zr=3.4, light=lt, face=R.prefix + 'face' + (f'_{v}' if v else '') + (f'_{f}' if f else ''), n=8)
        L += [el((-1.9, gy - 5.0, -1.9), (1.9, gy - 3.0, 1.9), glass[v], (0, gy, 0), light=lt),                  # (the neck)
              seg((-0.8, gy - 3.0, 0.6), (0.8, gy - 3.0, 0.6), 0.25, 0.25, fil, (0, gy, 0), light=15)]
        return L
    R.part('bulb', (0, gy, 0), None, bulb, variants=('dim', 'flash'), faced=True)
    R.part('base', (0, gy - 5.0, 0), 'bulb', lambda v, f: [
        el((-2.0, 1.2 + i * 1.0, -2.0), (2.0, 2.0 + i * 1.0, 2.0), base if i % 2 else ring, (0, gy - 5.0, 0)) for i in range(4)] + [
        el((-1.2, 0.0, -1.2), (1.2, 1.2, 1.2), ring, (0, gy - 5.0, 0))])
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 3.4, gy - 1.6, 0)
        R.part(n, pv, 'bulb', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 2.0, pv[1] - 1.6, -0.4), (pv[0] + s * 3.0, pv[1] - 0.6, -0.8)],
                                                                [0.35, 0.3], 0.35, wire, pv, (0.0, 0.0, -1.0)) +
                                                          [el((pv[0] + s * 3.0 - 0.45, pv[1] - 1.05, -1.25), (pv[0] + s * 3.0 + 0.45, pv[1] - 0.15, -0.35), wire, pv)])(pv, s))
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
    R = Rig('gb_bubbles_', 1.0)
    B, BL, BD = '#8ed2f2', '#d4f1ff', '#4a9cc8'
    skin = R.t('skin', lit(tex(B, 51, 0.03), 8, 8, 4, a=160, rim=BD))
    skin2 = R.t('skin2', lit(tex(B, 52, 0.03), 6, 6, 4, a=160, rim=BD))
    shine = R.t('shine', tex('#ffffff', 53, 0.01))
    drop = R.t('drop', tex(BL, 54, 0.04))

    def face(f, small=False):
        def p(d, W, H):
            r = 0.15 if not small else 0.17
            eye(d, W * 0.3, H * 0.38, W * r, H * 0.2, f, iris='#163a5a', look=looks(f), angry=1)
            eye(d, W * 0.68, H * 0.38, W * r, H * 0.2, f, iris='#163a5a', look=looks(f), angry=-1)
            mouth(d, W * 0.5, H * 0.72, W * 0.14, {None: 'o', 'look': 'o'}.get(f, FACE_MOUTH[f]), inner='#3a2030')
            oval(d, W * 0.12, H * 0.14, W * 0.08, H * 0.06, hexc('#ffffff'))          # (the bubble's glint)
        return R.t(f'face{"_s" if small else ""}{"_" + f if f else ""}', (face_tex(B, 8.8, 8.8, p, seed=55, hi=170, rim=BD, rim_a=120, fw=5.6, fh=4.8, fy=0.54) if not small else face_tex(B, 5.2, 5.2, p, seed=56, hi=170, rim=BD, rim_a=120, fw=3.6, fh=3.2, fy=0.54)))
    for f in (None,) + FACES:
        face(f); face(f, True)
    cy = 5.6
    def big(v, f):
        if v == 'pop':                                   # (popped: a splash of droplets where it was)
            return [el((x - 0.7, cy + y - 0.7, z - 0.7), (x + 0.7, cy + y + 0.7, z + 0.7), drop, (0, cy, 0), light=6)
                    for x, y, z in ((-4, 1, 0), (4, 2, -1), (0, 5, 0), (-3, -3, 1), (3, -3, -2), (0, -1, -4), (5, -1, 2), (-5, 3, -2))]
        return ball((0, cy, 0), 4.4, skin, (0, cy, 0), yr=4.4, zr=4.2, face=R.prefix + 'face' + (f'_{f}' if f else ''), n=9) + [
            el((-3.4, cy + 2.2, -3.4), (-2.2, cy + 3.4, -2.8), shine, (0, cy, 0), light=10)]
    R.part('big', (0, cy, 0), None, big, variants=('pop',), faced=True)
    sc = (6.4, 3.2, 1.6)
    R.part('small', sc, 'big', lambda v, f: [el((sc[0] + x - 0.5, sc[1] + y - 0.5, sc[2] + z - 0.5), (sc[0] + x + 0.5, sc[1] + y + 0.5, sc[2] + z + 0.5), drop, sc, light=6)
                                             for x, y, z in ((-1.5, 1, 0), (1.8, 0.5, -1), (0, -1.6, 1), (1, 2.2, 0.5))] if v == 'pop' else ball(sc, 2.6, skin2, sc, yr=2.6, zr=2.4, face=R.prefix + 'face_s' + (f'_{f}' if f else '')) + [
        el((sc[0] - 2.0, sc[1] + 1.2, sc[2] - 2.0), (sc[0] - 1.2, sc[1] + 2.0, sc[2] - 1.6), shine, sc, light=10)], variants=('pop',), faced=True)
    R.POSES.update({
        'appear': dict(_face='wow', _off=(0, 2.0, 0), _o_small=(1.0, 2.0, 0)),
        'idle_a': dict(_off=(0, 0.8, 0), _o_small=(0, -0.6, 0), big=T(('z', -4))),
        'idle_b': dict(_face='look', _off=(0, 0.2, 0), _o_small=(0, 1.0, -0.6), big=T(('y', -16)), small=T(('y', 20))),
        'bounce_0': dict(_off=(0, 2.4, 0), _o_small=(0, -1.6, 0)), 'bounce_1': dict(_off=(0, 0.0, 0), _o_small=(0, 2.0, 0)),
        'wind': dict(_face='fierce', _off=(0, 3.6, 1.6), _o_small=(-1.0, 1.2, 1.0), big=T(('x', 14))),
        'strike': dict(_face='wow', _v={'big': 'pop', 'small': 'pop'}, _off=(0, 0.0, -4.0)),
        'happy': dict(_face='happy', _off=(0, 1.6, 0), _o_small=(0, 1.8, 0), big=T(('z', 10)), small=T(('z', -16))),
        'vanish': dict(_face='happy', _off=(0, 4.0, 0), _o_small=(-2.0, 2.0, 0)),
    })
    return R.ns()


# ==================================================================================================== CHASE - the green blob
def chase():
    R = Rig('gb_chase_', 1.0)
    G, GL, GD = '#34c83a', '#7ef06a', '#1c8a24'
    goo = R.t('goo', lit(tex(G, 61, 0.04, spots=[(GL, 0.05)]), 8, 8, 4, a=150, rim=GD))

    def face(f):
        def p(d, W, H):
            eye(d, W * 0.32, H * 0.36, W * 0.12, H * 0.2, f, iris='#0c2a10', look=looks(f), angry=1)
            eye(d, W * 0.68, H * 0.36, W * 0.12, H * 0.2, f, iris='#0c2a10', look=looks(f), angry=-1)
            mouth(d, W * 0.48, H * 0.66, W * 0.16, FACE_MOUTH[f] if f else 'grin', inner='#145018')
        for v, (w, h) in SH.items():            # (a face for each shape he takes - squashed wide, stretched tall)
            R.t(f'face{"_" + v if v else ""}{"_" + f if f else ""}',
                face_tex(G, 2 * w, 2 * h, p, seed=62, hi=170, rim=GD, rim_a=110, fw=min(5.6, 2 * w * 0.86), fh=min(5.2, 2 * h * 0.62), fy=0.44))
    SH = {None: (3.4, 4.2), 'squash': (4.4, 3.0), 'stretch': (2.7, 5.4)}             # (half width, half height)
    for f in (None,) + FACES: face(f)
    def body(v, f):
        w, h = SH[v]; cy = 3.2 + h
        return ball((0, cy, 0), w, goo, (0, 7.4, 0), yr=h, zr=w * 0.85, face=R.prefix + 'face' + (f'_{v}' if v else '') + (f'_{f}' if f else ''), n=8)
    R.part('body', (0, 7.4, 0), None, body, variants=('squash', 'stretch'), faced=True)
    for s, n in ((1, 'lober'), (-1, 'lobel')):
        pv = (s * 1.6, 11.2, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1] - 0.6, 0), (pv[0] + s * 0.6, pv[1] + 2.0, 0), (pv[0] + s * 0.3, pv[1] + 3.6, 0)],
                                                                [1.9, 1.5], 1.7, goo, pv, (0.0, 0.0, -1.0), ext=0.5))(pv, s))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 3.4, 7.0, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: [seg((pv[0], pv[1], 0), (pv[0] + s * 2.2, pv[1] - 1.8, -0.4), 1.4, 1.4, goo, pv, ext=0.4)])(pv, s))
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.6, 3.6, 0)
        R.part(n, pv, 'body', (lambda pv: lambda v, f: [el((pv[0] - 1.0, 0.0, -1.4), (pv[0] + 1.0, pv[1] + 0.4, 1.0), goo, pv)])(pv))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'body': 'stretch'}, _off=(0, 1.6, 0), armr=L(('z', 70)), arml=L(('z', -70))),
        'idle_a': dict(armr=L(('z', -10)), arml=L(('z', 10)), lober=L(('z', -8)), lobel=L(('z', 8))),
        'idle_b': dict(_face='look', body=T(('y', -14), ('z', 6)), lober=L(('z', 20)), lobel=L(('z', 14)), armr=L(('z', 30))),
        'hop_0': dict(_v={'body': 'squash'}, _off=(0, -0.4, 0), lober=L(('z', -24)), lobel=L(('z', 24))),
        'hop_1': dict(_v={'body': 'stretch'}, _off=(0, 3.0, 0), lober=L(('z', 10)), lobel=L(('z', -10)), armr=L(('z', 40)), arml=L(('z', -40))),
        'wind': dict(_face='fierce', _v={'body': 'squash'}, _off=(0, -0.4, 1.0), body=T(('x', 14)), armr=L(('x', 50)), arml=L(('x', 50))),
        'strike': dict(_face='fierce', _v={'body': 'stretch'}, _off=(0, 0.4, -5.0), body=T(('x', -46)), armr=L(('x', -80)), arml=L(('x', -80)), lober=L(('x', 30)), lobel=L(('x', 30))),
        'happy': dict(_face='happy', _v={'body': 'stretch'}, _off=(0, 1.2, 0), armr=L(('z', 120)), arml=L(('z', -120)), lober=L(('z', -20)), lobel=L(('z', 20))),
        'vanish': dict(_face='happy', _v={'body': 'squash'}, armr=L(('z', 90))),
    })
    return R.ns()


# ==================================================================================================== LIMER - the round fellow in his green covering
def limer():
    R = Rig('gb_limer_', 1.0)
    S, SD = '#c8c0b0', '#8c8474'
    skin = R.t('skin', lit(tex(S, 71, 0.05, spots=[('#b4ac9c', 0.08)]), 8, 8, 4, a=110, rim=SD))
    leaf, leaf2 = R.t('leaf', tex('#2e8a2a', 72, 0.12, spots=[('#46b03c', 0.2), ('#1c5a1a', 0.15)])), R.t('leaf2', tex('#3ca236', 73, 0.12, spots=[('#1c5a1a', 0.2)]))
    stick = R.t('stick', tex('#2a2a2a', 74, 0.05))

    def face(f):
        def p(d, W, H):
            eye(d, W * 0.32, H * 0.36, W * 0.11, H * 0.16, f, iris='#1a1a1a', look=looks(f) if f else (0.3, 0), angry=1)
            eye(d, W * 0.66, H * 0.34, W * 0.11, H * 0.16, f, iris='#1a1a1a', look=looks(f) if f else (0.3, 0), angry=-1)
            d.arc((W * 0.5, H * 0.38, W * 0.66, H * 0.6), 270, 120, fill=hexc('#3a3630'), width=3)        # (his nose - the curl the owner drew)
            mouth(d, W * 0.42, H * 0.74, W * 0.1, {None: 'o', 'look': 'o'}.get(f, FACE_MOUTH[f]), inner='#4a2a20')
        return R.t(f'face{"_" + f if f else ""}', face_tex(S, 8.4, 8.8, p, seed=75, hi=110, rim=SD, rim_a=110, fw=5.6, fh=4.6, fy=0.36))
    for f in (None,) + FACES: face(f)
    cy = 9.0
    def body(v, f):
        L = ball((0, cy, 0), 4.2, skin, (0, cy, 0), yr=4.4, zr=4.0, face=R.prefix + 'face' + (f'_{f}' if f else ''), n=8)
        for i in range(14):                                               # (the covering: a ring of leafy tufts round his lower half)
            a = math.radians(i * 360 / 14); x, z = math.sin(a) * 4.1, -math.cos(a) * 3.9
            L.append(el((x - 1.2, cy - 3.6, z - 1.2), (x + 1.2, cy - 1.6, z + 1.2), leaf if i % 2 else leaf2, (0, cy, 0), shift=(0.17 * i, 0.31 * i)))
        L.append(el((-3.4, cy - 4.4, -3.4), (3.4, cy - 3.2, 3.4), leaf2, (0, cy, 0)))
        L += chain([(0, cy + 4.3, 0), (0.4, cy + 5.6, 0), (1.2, cy + 6.0, 0), (1.4, cy + 5.2, 0)], [0.3, 0.3, 0.3], 0.3, stick, (0, cy, 0), (0.0, 0.0, -1.0))
        return L
    R.part('body', (0, cy, 0), None, body, faced=True)
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.6, cy - 4.2, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 0.8, 2.2, 0), (pv[0] + s * 0.6, 0.2, 0)], [0.35, 0.35], 0.35, stick, pv) +
                                                         [el((pv[0] + s * 0.6 - 0.5, 0.0, -1.2), (pv[0] + s * 0.6 + 0.5, 0.4, 0.3), stick, pv)])(pv, s))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 4.0, cy - 0.6, 0)
        R.part(n, pv, 'body', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.6, pv[1] - 2.4, -0.2), (pv[0] + s * 1.8, pv[1] - 4.6, -0.6)],
                                                                [0.35, 0.35], 0.35, stick, pv))(pv, s))
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
    R = Rig('gb_chico_', 1.0)
    M, ML, MD = '#9a5a2a', '#c48040', '#5e3214'
    meat = R.t('meat', lit(tex(M, 81, 0.07, spots=[(ML, 0.1), (MD, 0.08)]), 8, 8, 4, a=100, rim=MD))
    bone, stick = R.t('bone', lit(tex('#f2ead8', 82, 0.03), 6, 6, 4, a=60)), R.t('stick', tex('#2a2a2a', 83, 0.05))

    def face(f):
        def p(d, W, H):
            eye(d, W * 0.3, H * 0.34, W * 0.13, H * 0.18, f, iris='#1a0e06', look=looks(f), angry=1)
            eye(d, W * 0.68, H * 0.32, W * 0.13, H * 0.18, f, iris='#1a0e06', look=looks(f), angry=-1)
            mouth(d, W * 0.48, H * 0.68, W * 0.14, {None: 'o', 'look': 'o'}.get(f, FACE_MOUTH[f]), inner='#5a1a14')
            for x, y in ((0.18, 0.86), (0.82, 0.8), (0.6, 0.12), (0.12, 0.12)):                   # (crispy freckles)
                oval(d, W * x, H * y, 3, 3, hexc(MD))
        return R.t(f'face{"_" + f if f else ""}', face_tex(M, 6.8, 8.4, p, seed=84, hi=100, rim=MD, rim_a=110, fw=5.2, fh=4.8, fy=0.46))
    for f in (None,) + FACES: face(f)
    my = 11.6
    R.part('meat', (0, 8.4, 0), None, lambda v, f: ball((0, my, 0), 3.4, meat, (0, 8.4, 0), yr=4.2, zr=3.2, face=R.prefix + 'face' + (f'_{f}' if f else ''), n=8) + [
        el((-2.2, my - 6.0, -2.0), (2.2, my - 3.2, 2.0), meat, (0, 8.4, 0), shift=(0.4, 0.6)),                     # (tapering to the bone)
        ], faced=True)
    R.part('bone', (0, 5.6, 0), 'meat', lambda v, f: [el((-0.7, 3.0, -0.7), (0.7, 5.8, 0.7), bone, (0, 5.6, 0)),
                                                       el((-1.5, 2.2, -0.8), (-0.1, 3.4, 0.8), bone, (0, 5.6, 0)), el((0.1, 2.2, -0.8), (1.5, 3.4, 0.8), bone, (0, 5.6, 0))])
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 0.8, 2.4, 0)
        R.part(n, pv, 'bone', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.2, 0.2, 0)], [0.3], 0.3, stick, pv) +
                                                        [el((pv[0] + s * 1.2 - 0.5, 0.0, -1.0), (pv[0] + s * 1.2 + 0.5, 0.35, 0.3), stick, pv)])(pv, s))
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 2.8, 9.0, 0)
        R.part(n, pv, 'meat', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 1.8, pv[1] - 1.6, -0.2), (pv[0] + s * 2.4, pv[1] - 3.4, -0.4)],
                                                               [0.3, 0.3], 0.3, stick, pv))(pv, s))
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


# ==================================================================================================== SPIKE - the saw blade
def spike():
    R = Rig('gb_spike_', 1.0)
    BK = '#2a2c30'
    core = R.t('core', lit(tex(BK, 91, 0.06), 8, 8, 4, a=70, rim='#101012'))
    steel, steeld = R.t('steel', lit(tex('#d4d8dc', 92, 0.04), 6, 6, 4, a=80)), R.t('steeld', tex('#8a8e94', 93, 0.05))
    green = R.t('green', tex('#3ac850', 94, 0.05))

    def face(f):
        def p(d, W, H):                       # (his default is a scowl - the owner drew him angry - with a green mouth)
            k = 'fierce' if f in (None, 'look') else f
            eye(d, W * 0.32, H * 0.4, W * 0.14, H * 0.17, k, iris='#0a0a0a', white='#e8eaec', ink='#000000', look=looks(f), angry=1, lid=hexc('#000000'))
            eye(d, W * 0.7, H * 0.4, W * 0.14, H * 0.17, k, iris='#0a0a0a', white='#e8eaec', ink='#000000', look=looks(f), angry=-1, lid=hexc('#000000'))
            mouth(d, W * 0.5, H * 0.74, W * 0.18, {None: 'fangs', 'look': 'frown', 'happy': 'grin', 'blink': 'frown'}.get(f, FACE_MOUTH[f]), ink='#0e3a14', inner='#3ac850')
        return R.t(f'face{"_" + f if f else ""}', face_tex(BK, 7.2, 7.2, p, seed=95, hi=60, rim='#08080a', rim_a=120, fw=5.6, fh=4.8, fy=0.5))
    for f in (None,) + FACES: face(f)
    cy = 7.4
    R.part('core', (0, cy, 0), None, lambda v, f: ball((0, cy, 0), 3.6, core, (0, cy, 0), yr=3.6, zr=2.6, face=R.prefix + 'face' + (f'_{f}' if f else '')), faced=True)
    def blade(v, f):
        L = []
        n = 16
        for i in range(n):                    # (the teeth: a ring of hooked blades round him, in the plane facing front)
            a = math.radians(i * 360 / n); b = math.radians(i * 360 / n + 26)
            A = (math.cos(a) * 4.0, cy + math.sin(a) * 4.0, 0.0); B = (math.cos(b) * 6.6, cy + math.sin(b) * 6.6, 0.0)
            L.append(seg(A, B, 1.5, 0.5, steel if i % 2 else steeld, (0, cy, 0), (0.0, 0.0, -1.0)))
        L.append(el((-4.4, cy - 4.4, -0.3), (4.4, cy + 4.4, 0.3), steeld, (0, cy, 0)))
        if v == 'spin':
            L += [seg((math.cos(math.radians(a)) * 5.0, cy + math.sin(math.radians(a)) * 5.0, -0.5),
                      (math.cos(math.radians(a + 60)) * 5.0, cy + math.sin(math.radians(a + 60)) * 5.0, -0.5), 0.2, 0.2, R.t('spark', tex('#fff0a0', 96, 0.1)), (0, cy, 0), light=15)
                  for a in (0, 120, 240)]
        return L
    R.part('blade', (0, cy, 0.4), 'core', blade, variants=('spin',))
    R.POSES.update({
        'appear': dict(_face='wow', _v={'blade': 'spin'}, _off=(0, 1.4, 0), blade=T(('z', 40))),
        'idle_a': dict(_off=(0, 0.4, 0), blade=T(('z', 11))),
        'idle_b': dict(_face='look', _off=(0, 0.6, 0), core=T(('y', -20), ('z', 8)), blade=T(('z', -11))),
        'spin_0': dict(_face='fierce', _v={'blade': 'spin'}, blade=T(('z', 0))), 'spin_1': dict(_face='fierce', _v={'blade': 'spin'}, blade=T(('z', 11.25))),
        'wind': dict(_face='fierce', _v={'blade': 'spin'}, _off=(0, 0.0, 1.6), core=T(('x', 20)), blade=T(('z', 22))),
        'strike': dict(_face='fierce', _v={'blade': 'spin'}, _off=(0, -0.6, -6.0), core=T(('x', -24)), blade=T(('z', 5))),
        'happy': dict(_face='happy', _off=(0, 1.2, 0), core=T(('z', 12)), blade=T(('z', -20))),
        'vanish': dict(_face='blink', _v={'blade': 'spin'}, core=T(('y', 90))),
    })
    return R.ns()


# ==================================================================================================== CHEFERONI - the pizza chef
def cheferoni():
    R = Rig('gb_cheferoni_', 1.0)
    CR, CH = '#d8a058', '#f6e2a0'
    crust = R.t('crust', lit(tex(CR, 101, 0.07, spots=[('#b07a3a', 0.1)]), 8, 8, 4, a=80))
    cheese = R.t('cheese', tex(CH, 102, 0.05, spots=[('#f0c860', 0.15)]))
    hat, hatb = R.t('hat', lit(tex('#fafafa', 103, 0.03), 6, 6, 4, a=40, rim='#c8c8c8')), R.t('hatband', tex('#e4e4e4', 104, 0.03))
    yel, dough = R.t('limb', tex('#f2d44a', 105, 0.05)), R.t('dough', lit(tex('#f4e6c4', 106, 0.04), 6, 6, 4, a=70))
    pep = R.t('pep', tex('#c0302a', 107, 0.08, spots=[('#8a1a16', 0.15)]))

    def face(f):
        def p(d, W, H):                      # (the pizza face: cheese, pepperoni round the edge, two eyes and a great black moustache)
            oval(d, W / 2, H / 2, W * 0.42, H * 0.42, hexc(CH), hexc('#c8902a'), 3)
            r_ = random.Random(110)
            for _ in range(60):              # (melted cheese - a little darker here and there)
                x, y = W / 2 + (r_.random() - 0.5) * W * 0.7, H / 2 + (r_.random() - 0.5) * H * 0.7
                if math.hypot(x - W / 2, y - H / 2) < W * 0.38: d.rectangle((x, y, x + 3, y + 3), fill=hexc('#f0c860'))
            for a in range(0, 360, 60):     # (the slice cuts)
                r = math.radians(a); d.line((W / 2, H / 2, W / 2 + math.cos(r) * W * 0.41, H / 2 + math.sin(r) * H * 0.41), fill=hexc('#d8a850'), width=2)
            for a in range(20, 380, 52):    # (pepperoni round the edge)
                r = math.radians(a); x, y = W / 2 + math.cos(r) * W * 0.31, H / 2 + math.sin(r) * H * 0.31
                oval(d, x, y, W * 0.055, H * 0.055, hexc('#c0302a'), hexc('#8a1a16'), 2)
                oval(d, x - W * 0.015, y - H * 0.015, W * 0.012, H * 0.012, hexc('#e06a5a'))
            eye(d, W * 0.4, H * 0.42, W * 0.075, H * 0.09, f, iris='#1a1208', look=looks(f), angry=1)
            eye(d, W * 0.6, H * 0.42, W * 0.075, H * 0.09, f, iris='#1a1208', look=looks(f), angry=-1)
            W, H = W * 0.75, H * 0.75; mx, my = W * 0.5 / 0.75, H * 0.58 / 0.75                                                          # (the moustache: two curls)
            for s in (-1, 1):
                d.ellipse((mx + s * W * 0.02 - (W * 0.16 if s < 0 else 0), my - H * 0.06, mx + s * W * 0.02 + (W * 0.16 if s > 0 else 0), my + H * 0.07), fill=hexc('#141414'))
                d.ellipse((mx + s * W * 0.17 - W * 0.04, my - H * 0.1, mx + s * W * 0.17 + W * 0.04, my - H * 0.02), fill=hexc('#141414'))
            if f in ('happy', 'wow', 'fierce'): mouth(d, mx, my + H * 0.14, W * 0.08, {'happy': 'grin', 'wow': 'o', 'fierce': 'fangs'}[f])
        return R.t(f'face{"_" + f if f else ""}', face_tex(CR, 10.8, 10.8, p, seed=108, hi=60, fw=10.8, fh=10.8))
    for f in (None,) + FACES: face(f)
    cy = 11.0
    def pizza(v, f):
        return disc((0, cy, 0), 5.4, 0.8, crust, (0, cy, 0), face=R.prefix + 'face' + (f'_{f}' if f else ''), n=11)
    R.part('pizza', (0, cy, 0), None, pizza, faced=True)
    R.part('hat', (0, cy + 4.6, 0), 'pizza', lambda v, f: [
        el((-2.4, cy + 4.0, -1.4), (2.4, cy + 5.6, 1.4), hatb, (0, cy + 4.6, 0)),
        *ball((0, cy + 7.6, 0), 3.0, hat, (0, cy + 4.6, 0), yr=2.2, zr=2.6)])
    for s, n in ((1, 'armr'), (-1, 'arml')):
        pv = (s * 4.6, cy - 1.0, 0)
        R.part(n, pv, 'pizza', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 2.4, pv[1] - 2.4, -0.4), (pv[0] + s * 2.8, pv[1] - 5.0, -0.8)],
                                                                [0.5, 0.45], 0.5, yel, pv) + [el((pv[0] + s * 2.8 - 0.7, pv[1] - 5.8, -1.5), (pv[0] + s * 2.8 + 0.7, pv[1] - 4.6, -0.1), yel, pv)])(pv, s))
    for s, n in ((1, 'legr'), (-1, 'legl')):
        pv = (s * 1.8, cy - 5.0, 0)
        R.part(n, pv, 'pizza', (lambda pv, s: lambda v, f: chain([(pv[0], pv[1], 0), (pv[0] + s * 0.4, 0.4, 0)], [0.55], 0.55, yel, pv) +
                                                         [el((pv[0] + s * 0.4 - 0.7, 0.0, -1.6), (pv[0] + s * 0.4 + 0.7, 0.6, 0.4), R.t('shoe', tex('#3a2a20', 109, 0.05)), pv)])(pv, s))
    hand = (4.6 + 2.8, cy - 6.0, -0.8)
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
