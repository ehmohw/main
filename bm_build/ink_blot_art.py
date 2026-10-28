"""The Ink Blot: a drop of ink that fell off Mr. Capshun's pen while he was narrating the history of the Underwater Kingdom - a
Buddy the Gem of Creativity never meant to make, half a story and half a spill. It turns into whatever it's thinking about (or
whatever Capshun happens to be narrating). Shy but playful. Capshun is embarrassed by it.

(2.97b - the owner: "it's not clear what it is"; it read as a soot blob) Now unmistakably INK, fresh off a pen:
  - fountain-pen ink, not soot: a deep blue-black, a darker core, a lighter blue rim light round its edge, and WET - bright white
    specular streaks across the top (on a layer of their own, ib_shine_*, so a recoloured ink keeps its white shine);
  - the shape of liquid: a big ink DROP (a round bottom, a soft peak), drips running down its sides and off its pods, standing in
    its own splat on the floor (the classic splat outline, satellite drops flicked round it);
  - the pen: a little gold fountain-pen nib stuck in the top of its head like a cowlick, its tip still inky;
  - big WHITE eyes with a shine (unshaded, so they stay white), a small mouth.
FLAT, drawn like Mr. Capshun: every shape is one picture, front and back - side-on it all but vanishes.

It SHAPESHIFTS - the body's model is the pose's `_shape`:
    blot      the default: the ink drop, standing in its splat (the splat lies on the floor, part of the body)
    drop      the same drop OFF the floor - a hop, a lunge, a run, a swim - its splat left behind (the same textures as blot)
    fist      a big ink fist on a wrist of ink (punch)
    shield    a round shield, rimmed, dripping into its splat (guard)
    question  a question mark - its dot stands in its splat (curious, confused: wonder)
    puddle    spilt flat on the floor, eyes peeking out of a little mound (sitting, sleeping, fainted)
    quill     a pointed pen nib of ink, slit and breather hole (spike)

A rigkit rig: body (pivot at its base, on the floor; a model per shape), head (the eyes and mouth - a see-through panel just in front
of the ink, a model per shape x expression; each shape puts the eyes on itself), the pseudopods (two joints each, an ink ball at the
tip with a drop hanging off it; hidden unless a pose asks: `_pods`) and the glob (an ink ball at the right pod's tip: `_glob`).
A shape that stands in its splat only leans a few degrees (the splat must stay flat on the floor); the big leans are the drop's.
Design units: feet at y=0, facing -z, its right is +x."""
import math
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from phase57_art import hexc
from rigkit import qs, el, seg, point, qrot, D

PREFIX = 'ib_'
RIG_SCALE = 1.05                                  # (the drop's peak between Capshun's waist and chest; the nib a little above)
PIVOT = {'body': (0, 0, 0), 'head': (0, 7.4, 0),
         'podr': (4.4, 7.0, 0), 'podr2': (9.0, 7.0, 0), 'podl': (-4.4, 7.0, 0), 'podl2': (-9.0, 7.0, 0),
         'glob': (12.6, 7.0, 0)}
PARENT = {'body': None, 'head': 'body', 'podr': 'body', 'podr2': 'podr', 'podl': 'body', 'podl2': 'podl', 'glob': 'podr2'}
PARTS = tuple(PIVOT)
PART_K = {}
SHAPES = ('blot', 'drop', 'fist', 'shield', 'question', 'puddle', 'quill')
FACES = ('happy', 'surprised', 'blink', 'determined', 'hurt', 'shy', 'puzzled', 'sleepy')
# fountain-pen ink: (the wardrobe recolours the ink by its brightness, dark - mid - light; the white shine is a layer of its own)
CORE, BASE, MID, RIM = '#04061a', '#0a1242', '#1a2c86', '#4f7cf0'
LINE = '#3d5cc8'                                  # (lines drawn into the ink: the fist's fingers, the shield's rim, the nib's slit)
INK = BASE
LD = 0.3                                          # (its depth: flat as a page)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
POD_TIP = 12.6                                    # (the pod's rest line: straight out at its sides, the ink ball at x = +-12.6)

# each upright shape is one square page: (its side L, its centre x, its bottom y) in design units; where its eyes go on it
# (centre x, centre y, the eye panel's side); whether it stands in a splat on the floor; where its nib is stuck in (x, y, tilt)
PAGE = {'blot': (17.0, 0.0, 0.0), 'drop': (17.0, 0.0, 0.0), 'fist': (16.0, 0.0, 0.0), 'shield': (16.0, 0.0, 0.0),
        'question': (18.0, 0.0, 0.0), 'quill': (22.0, 0.0, 0.0), 'puddle': (10.0, 0.0, 0.0)}
EYES = {'blot': (0.0, 7.4, 8.4), 'drop': (0.0, 7.4, 8.4), 'fist': (1.0, 10.6, 7.0), 'shield': (0.0, 10.0, 8.6),
        'question': (0.6, 14.4, 6.6), 'quill': (0.0, 6.4, 6.8), 'puddle': (0.0, 2.6, 6.4)}
SPLAT = {'blot': 19.0, 'shield': 19.0, 'question': 17.0, 'puddle': 22.0}         # (the splat on the floor: its side)
NIB = {'blot': (0.5, 15.6, -22.5), 'drop': (0.5, 15.6, -22.5), 'question': (-1.6, 16.6, 22.5), 'puddle': (0.6, 5.4, -22.5),
       'shield': (0.0, 14.8, 0.0)}
NIB_S = 4.6
PUDDLE = SPLAT['puddle']


def HIDDEN(p, pose):
    if p in ('podr', 'podr2'):
        return 'r' not in pose.get('_pods', '')
    if p in ('podl', 'podl2'):
        return 'l' not in pose.get('_pods', '')
    if p == 'glob':
        return not pose.get('_glob')
    return False


def model_name(p, pose, suffix=''):
    shape = pose.get('_shape', 'blot')
    if p == 'body':
        return f'{PREFIX}body_{shape}{suffix}'
    if p == 'head':
        face = f'_x{pose["_face"]}' if pose.get('_face') else ''
        return f'{PREFIX}head_{shape}{face}{suffix}'
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
SS = 4                                            # (drawn 4x over, brought down smooth; the edge kept hard)
N = 128


def _down(im, n=N):
    im = im.resize((n, n), Image.LANCZOS)
    a = np.asarray(im).copy(); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    return Image.fromarray(a, 'RGBA')


def _c(h):
    return np.array(hexc(h)[:3], np.float32)


class Page:
    """an ink drawing on a 128 grid (drawn SS x over): a mask of where the ink is, then the ink laid in - its dark core, its
    blue rim light - and, on a layer of its own, its wet white shine"""
    def __init__(self, light=(0.3, 0.25)):
        self.S = N * SS
        self.mask = Image.new('L', (self.S, self.S), 0); self.m = ImageDraw.Draw(self.mask)
        self.holes = []; self.light = light

    def E(self, b):
        return tuple(v * SS for v in b)

    def oval(self, box):
        self.m.ellipse(self.E(box), fill=255)

    def dot(self, x, y, r):
        self.oval((x - r, y - r, x + r, y + r))

    def poly(self, pts):
        self.m.polygon([(x * SS, y * SS) for x, y in pts], fill=255)

    def rrect(self, box, r):
        self.m.rounded_rectangle(self.E(box), r * SS, fill=255)

    def stroke(self, pts, w):
        """a thick stroke along a polyline: discs swept along it (round ends, round joins)"""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            k = max(2, int(math.hypot(x1 - x0, y1 - y0) / 1.5))
            for i in range(k + 1):
                t = i / k; self.dot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w / 2)

    def drip(self, x, y0, y1, w):
        """a drip running down: a run of ink from y0, narrowing a little, to a round drop at y1"""
        self.poly([(x - w / 2, y0), (x + w / 2, y0), (x + w * 0.36, y1 - w * 0.7), (x - w * 0.36, y1 - w * 0.7)])
        self.dot(x, y1 - w * 0.6, w * 0.6)

    def drop(self, cx, cy, r, peak, curl=0.0):
        """a teardrop: a round bottom (centre, radius) and a soft peak, its tip curling over a little"""
        px, py = peak
        d = math.hypot(px - cx, py - cy); a = math.asin(min(0.99, r / d)); base = math.atan2(cy - py, cx - px)
        pts = [(px, py)]
        for s in (-1, 1):
            t = base + s * a
            L = math.sqrt(max(0.0, d * d - r * r))
            pts.append((px + L * math.cos(t), py + L * math.sin(t)))
        self.poly([pts[1], pts[0], pts[2], (cx, cy)])
        self.dot(cx, cy, r)
        self.dot(px + curl, py + 2.2, 3.4)                     # (the soft tip)

    def hole(self, box):
        self.holes.append(box)

    def ink(self, shine=(), lines=(), rim=1.0):
        """-> (the ink texture, its shine texture). The ink: dark at the core and at the bottom, a sheen toward the upper left, a blue
        rim light round the edge (strongest down its right side); lines drawn in it. The shine: white streaks and glints - only on
        the ink."""
        S = self.S
        for b in self.holes:
            self.m.ellipse(self.E(b), fill=0)
        mk = np.asarray(self.mask).astype(np.float32) / 255.0
        ins = mk >= 0.5
        blur = np.asarray(self.mask.filter(ImageFilter.GaussianBlur(5 * SS))).astype(np.float32) / 255.0
        ys, xs = np.mgrid[0:S, 0:S].astype(np.float32) / S
        if ins.any():
            yy, xx = np.nonzero(ins); x0, x1, y0, y1 = xx.min() / S, xx.max() / S, yy.min() / S, yy.max() / S
        else:
            x0, x1, y0, y1 = 0, 1, 0, 1
        u = (xs - x0) / max(1e-3, x1 - x0); v = (ys - y0) / max(1e-3, y1 - y0)
        lx, ly = self.light
        sheen = np.clip(1 - np.hypot(u - lx, (v - ly) * 1.2) / 0.62, 0, 1) ** 1.3
        col = _c(BASE)[None, None] + (_c(CORE) - _c(BASE))[None, None] * np.clip(v * 0.9 - 0.15, 0, 1)[..., None]
        col = col + (_c(MID) - col) * (sheen * 0.85)[..., None]
        edge = np.clip((1 - blur) * 2.6 - 0.25, 0, 1)                          # (0 deep inside, 1 at the very edge)
        side = np.clip(0.35 + 0.9 * (u - 0.35), 0.2, 1.0) * np.clip(0.6 + 0.6 * v, 0, 1)
        col = col + (_c(RIM) - col) * (edge * side * rim * 0.9)[..., None]
        a = np.zeros((S, S, 4), np.uint8); a[..., :3] = np.clip(col, 0, 255).astype(np.uint8); a[..., 3] = np.where(ins, 255, 0)
        im = Image.fromarray(a, 'RGBA'); d = ImageDraw.Draw(im)
        for kind, p, q in lines:
            self._draw(d, kind, p, q, hexc(LINE))
        sh = Image.new('RGBA', (S, S), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        for kind, p, q, *c in shine:
            self._draw(ds, kind, p, q, hexc(c[0] if c else '#ffffff'))
        sa = np.asarray(sh).copy(); sa[..., 3] = np.where(ins, sa[..., 3], 0)
        return _down(im), _down(Image.fromarray(sa, 'RGBA'))

    def _draw(self, d, kind, a, b, col):
        if kind == 'arc':
            d.arc(self.E(a), b[0], b[1], fill=col, width=round(b[2] * SS))
        elif kind == 'line':
            d.line([(x * SS, y * SS) for x, y in a], fill=col, width=round(b * SS), joint='curve')
        elif kind == 'ring':
            d.ellipse(self.E(a), outline=col, width=round(b * SS))
        elif kind == 'rrect':
            d.rounded_rectangle(self.E(a), b[0] * SS, outline=col, width=round(b[1] * SS))
        elif kind == 'dot':
            x, y, r = a; d.ellipse(self.E((x - r, y - r, x + r, y + r)), fill=col)
        elif kind == 'oval':
            d.ellipse(self.E(a), fill=col)


def _sat(p, spots):
    for x, y, r in spots:
        p.dot(x, y, r)


SOFT = '#bcd0ff'                                  # (a softer glint, the rim's wet edge)


def _blot():
    """the ink drop: a round bottom on the floor, a soft peak curling over, drips running down its sides (hanging off it in drops),
    droplets flicked round it"""
    p = Page(light=(0.3, 0.3))
    p.drop(64, 86, 41.5, (60, 6), curl=-1.0)
    p.drip(26, 70, 112, 9); p.drip(103, 80, 106, 7); p.drip(36, 98, 124, 6.4); p.drip(92, 104, 126, 5.6)
    _sat(p, ((8, 58, 3.2), (14, 42, 2.0), (6, 84, 2.2), (120, 52, 2.8), (115, 36, 1.8), (123, 76, 2.2)))
    return p.ink(shine=(('arc', (30, 34, 98, 122), (196, 246, 6.0)),            # (the big wet streak across its upper left)
                        ('dot', (31, 96, 3.2), None), ('line', [(55, 16), (51, 26)], 3.4),
                        ('arc', (24, 46, 104, 128), (300, 352, 3.0), SOFT), ('dot', (26, 104, 2.0), None)))


def _fist():
    """a big ink fist, side-on (the classic cartoon punch): curled fingers to the front, the thumb wrapped over them, on a wrist
    of ink that drips down into a little pool"""
    p = Page(light=(0.25, 0.2))
    p.rrect((20, 16, 106, 88), 22)
    for y in (18, 35, 52, 69):
        p.rrect((86, y, 116, y + 19), 9)
    p.rrect((40, 60, 104, 80), 10)
    p.poly([(40, 84), (88, 84), (80, 112), (48, 112)])
    p.oval((26, 108, 102, 127.4))
    p.drip(28, 80, 112, 7); p.drip(108, 86, 104, 5)
    _sat(p, ((8, 34, 2.6), (12, 58, 2.0), (6, 84, 2.2), (122, 108, 2.2), (118, 118, 1.6)))
    lines = [('line', [(96, 35.5), (112, 35.5)], 2.2), ('line', [(96, 52.5), (112, 52.5)], 2.2), ('line', [(96, 69.5), (112, 69.5)], 2.2),
             ('rrect', (40, 60, 104, 80), (10, 2.2)), ('line', [(88, 22), (88, 84)], 1.6)]
    return p.ink(shine=(('arc', (24, 18, 84, 80), (190, 252, 5.5)), ('dot', (110, 23, 2.4), None), ('dot', (110, 40, 1.8), None),
                        ('line', [(42, 66), (60, 64)], 2.2, SOFT)), lines=lines)


def _shield():
    """a round shield of ink, rimmed - dripping off its bottom edge into the splat it stands in"""
    p = Page(light=(0.3, 0.25))
    p.oval((12, 4, 116, 108))
    p.poly([(50, 100), (78, 100), (86, 127.4), (42, 127.4)])
    p.drip(24, 84, 114, 7); p.drip(104, 84, 106, 6); p.drip(70, 104, 127, 5)
    _sat(p, ((5, 30, 2.4), (122, 22, 2.6), (124, 60, 2.0), (6, 70, 2.0)))
    return p.ink(shine=(('arc', (24, 14, 90, 80), (192, 252, 6)), ('dot', (30, 66, 2.8), None), ('dot', (100, 28, 2.2), None),
                        ('arc', (18, 10, 110, 102), (330, 360, 2.4), SOFT)),
                 lines=[('ring', (22, 14, 106, 98), 2.4)])


def _question():
    """a question mark: a heavy hook (the eyes peek out of the top of it), the stem dripping down on a thread into its dot"""
    p = Page(light=(0.3, 0.15))
    hook = [(26, 44), (28, 30), (38, 18), (52, 12), (68, 12), (84, 18), (96, 30), (98, 44), (92, 56), (80, 64), (68, 70), (64, 80), (64, 92)]
    p.stroke(hook, 22)
    p.oval((34, 6, 94, 40))
    p.dot(28, 42, 13)
    p.stroke([(64, 92), (64, 106)], 7)
    p.oval((44, 100, 84, 127.4))
    p.drip(82, 66, 88, 6); p.drip(24, 50, 66, 5)
    _sat(p, ((10, 74, 2.4), (116, 64, 2.6), (110, 92, 2.0), (16, 94, 2.0)))
    return p.ink(shine=(('arc', (40, 10, 92, 44), (195, 252, 4.6)), ('dot', (22, 37, 2.8), None), ('dot', (55, 108, 2.4), None),
                        ('line', [(88, 26), (92, 36)], 2.2, SOFT)))


def _quill():
    """a pen nib of ink, pointed: shot up out of its pool into a spike - the slit down its point, the breather hole (a real hole)"""
    p = Page(light=(0.35, 0.4))
    p.poly([(64, 1), (82, 34), (96, 66), (100, 84), (28, 84), (32, 66), (46, 34)])
    p.oval((26, 64, 102, 104))
    p.poly([(44, 100), (84, 100), (92, 120), (36, 120)])
    p.oval((22, 112, 106, 127.4))
    p.drip(30, 92, 118, 6); p.drip(98, 90, 112, 6)
    p.hole((59, 40, 69, 50))
    _sat(p, ((12, 56, 2.6), (116, 50, 2.2), (6, 90, 2.0), (122, 86, 2.4), (20, 36, 1.8)))
    return p.ink(shine=(('line', [(54, 30), (40, 66), (36, 82)], 3.6), ('dot', (42, 94, 2.4), None),
                        ('line', [(74, 30), (84, 52)], 2.0, SOFT)),
                 lines=[('line', [(64, 6), (64, 40)], 1.8)])


def _mound():
    """the puddle's mound: a low lump of ink with the eyes peeking out of it"""
    p = Page(light=(0.3, 0.35))
    p.oval((12, 30, 116, 172))
    p.dot(10, 116, 6); p.dot(118, 112, 5)
    return p.ink(shine=(('arc', (24, 36, 92, 124), (198, 248, 6)), ('dot', (30, 98, 2.6), None), ('arc', (20, 32, 108, 150), (300, 340, 3), SOFT)))


def _splat():
    """the splat on the floor, from above: the classic ink-splat outline - a round pool, lobes and spikes flung out of it, satellite
    drops round it"""
    p = Page(light=(0.4, 0.4))
    p.oval((26, 26, 102, 102))
    for a, r, L in ((0, 9, 40), (28, 6, 46), (62, 10, 40), (100, 5, 50), (130, 9, 42), (168, 7, 46), (205, 10, 40), (240, 6, 50),
                    (272, 8, 44), (310, 6, 48), (338, 8, 42)):
        t = math.radians(a)
        p.stroke([(64 + 30 * math.cos(t), 64 + 30 * math.sin(t)), (64 + L * math.cos(t), 64 + L * math.sin(t))], r * 1.2)
        p.dot(64 + (L + r * 0.3) * math.cos(t), 64 + (L + r * 0.3) * math.sin(t), r * 0.75)
    for a, d_, r in ((15, 58, 3.4), (80, 60, 2.6), (150, 58, 3.0), (190, 61, 2.2), (255, 59, 3.2), (295, 61, 2.0), (350, 60, 2.4), (115, 61, 2.0)):
        t = math.radians(a); p.dot(64 + d_ * math.cos(t), 64 + d_ * math.sin(t), r)
    return p.ink(shine=(('arc', (34, 34, 94, 94), (205, 245, 3.6)), ('dot', (40, 50, 2.0), None)), rim=0.8)


def _ball():
    p = Page(light=(0.3, 0.3))
    p.dot(64, 64, 60)
    return p.ink(shine=(('arc', (22, 22, 98, 98), (195, 255, 13)), ('dot', (90, 92, 7), None, SOFT)))


def _nib():
    """a little gold fountain-pen nib, tip down (stuck into the ink): the shoulders, the slit up from the tip to the breather hole,
    the tip still wet with ink"""
    S = 64 * SS; k = SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    out, gold, lt, hi, dk = hexc('#5a3608'), hexc('#d8a032'), hexc('#f4d06a'), hexc('#fff4c0'), hexc('#a8701c')
    body = [(32, 62), (20, 36), (18, 22), (22, 10), (42, 10), (46, 22), (44, 36)]
    d.polygon(P(body), fill=out)
    inner = [(32, 57), (23, 35), (21.5, 22.5), (24.5, 13), (39.5, 13), (42.5, 22.5), (41, 35)]
    d.polygon(P(inner), fill=gold)
    d.polygon(P([(24.5, 13), (31, 13), (29, 36), (32, 55), (23, 35), (21.5, 22.5)]), fill=lt)      # (lit down its left)
    d.polygon(P([(39.5, 13), (42.5, 22.5), (41, 35), (34, 52)]), fill=dk)
    d.rectangle((19 * k, 4 * k, 45 * k, 12 * k), fill=out); d.rectangle((21 * k, 5.5 * k, 43 * k, 10.5 * k), fill=hexc('#2a2a34'))   # (the collar)
    d.line(P([(24, 7), (40, 7)]), fill=hexc('#6a6a7a'), width=round(1.4 * k))
    d.ellipse((29 * k, 27 * k, 35 * k, 33 * k), fill=out)                             # (the breather hole)
    d.line(P([(32, 33), (32, 61)]), fill=out, width=round(1.6 * k))                                  # (the slit)
    d.polygon(P([(32, 62), (25.5, 48), (38.5, 48)]), fill=hexc(BASE))                                 # (the tip, wet with ink)
    d.line(P([(26, 18), (27, 28)]), fill=hi, width=round(1.6 * k))
    return _down(im, 64)


def _face(kind=None):
    """the eyes (his right on our left): two big white ovals, its left a touch bigger and higher - like Capshun's - shaded a
    little blue along the bottom and each with a bright glint; a small mouth. A see-through panel: each expression redraws them
    (and cuts lids back into the ink)."""
    S = N * SS; k = SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W = hexc('#ffffff'); SH = hexc('#c2d2fa'); CUT = (0, 0, 0, 0)
    E = lambda b: tuple(v * k for v in b)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    le, re = (20, 28, 56, 90), (70, 20, 108, 90)

    def eye(box, glint=True):
        x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
        d.ellipse(E(box), fill=SH)
        d.ellipse(E((x0, y0, x1, y1 - h * 0.16)), fill=W)                       # (white, a blue crescent of shade along the bottom)
        if glint:
            d.ellipse(E((x0 + w * 0.44, y0 + h * 0.1, x0 + w * 0.86, y0 + h * 0.38)), fill=hexc('#8ea8e8'))
            d.ellipse(E((x0 + w * 0.51, y0 + h * 0.14, x0 + w * 0.79, y0 + h * 0.33)), fill=W)  # (its glint, ringed in blue)
            d.ellipse(E((x0 + w * 0.22, y1 - h * 0.2, x0 + w * 0.36, y1 - h * 0.09)), fill=W)

    def arc(box, a0, a1, w=6):
        d.arc(E(box), a0, a1, fill=W, width=round(w * k))
    if kind == 'blink':
        arc((20, 46, 56, 72), 20, 160, 6.4); arc((70, 42, 108, 70), 20, 160, 6.4)
    elif kind == 'happy':
        arc((20, 48, 56, 84), 195, 345, 7.4); arc((70, 42, 108, 80), 195, 345, 7.4)
    elif kind == 'surprised':
        eye((16, 20, 60, 96)); eye((64, 10, 112, 96))
    elif kind == 'hurt':
        d.line(P([(24, 44), (50, 59), (24, 74)]), fill=W, width=7 * k, joint='curve')
        d.line(P([(104, 42), (76, 58), (104, 74)]), fill=W, width=7 * k, joint='curve')
    elif kind == 'shy':                                                                  # (looking away, down to our left)
        eye((12, 40, 42, 90)); eye((52, 34, 86, 90))
        for x in (18, 28, 38):
            d.line(P([(x + 4, 98), (x, 106)]), fill=hexc('#ff9ab8'), width=round(2.6 * k))
        for x in (78, 88, 98):
            d.line(P([(x + 4, 98), (x, 106)]), fill=hexc('#ff9ab8'), width=round(2.6 * k))
    elif kind == 'puzzled':
        eye((18, 40, 52, 88)); eye((68, 14, 110, 90))
    else:
        eye(le); eye(re)
    if kind == 'determined':
        d.polygon(P([(16, 18), (60, 18), (60, 58)]), fill=CUT); d.polygon(P([(66, 8), (112, 8), (66, 52)]), fill=CUT)
    elif kind == 'sleepy':
        d.rectangle(E((16, 16, 60, 60)), fill=CUT); d.rectangle(E((66, 8, 112, 56)), fill=CUT)
    elif kind == 'puzzled':
        d.polygon(P([(14, 30), (58, 30), (58, 60), (14, 52)]), fill=CUT)
    if kind is None:
        arc((54, 94, 76, 110), 25, 155, 4.4)
    elif kind == 'shy':
        arc((58, 104, 70, 114), 200, 340, 3.6)
    elif kind == 'happy':
        d.chord(E((46, 90, 84, 120)), 0, 180, fill=W); d.chord(E((56, 104, 74, 118)), 0, 180, fill=hexc('#ff7a98'))
    elif kind == 'surprised':
        d.ellipse(E((57, 100, 71, 118)), outline=W, width=round(3.8 * k))
    elif kind == 'determined':
        d.line(E((52, 108, 78, 104)), fill=W, width=round(4.2 * k))
    elif kind == 'hurt':
        d.line(P([(46, 112), (54, 106), (62, 112), (70, 106), (78, 112)]), fill=W, width=round(3.8 * k), joint='curve')
    elif kind == 'puzzled':
        d.line(P([(62, 110), (70, 106), (78, 110), (86, 106)]), fill=W, width=round(3.6 * k), joint='curve')
    elif kind == 'sleepy':
        arc((56, 102, 72, 112), 20, 160, 3.6)
    return _down(im)


def _solid_ink():
    """the pseudopods' ink: the body's blue-black, a touch lighter on top"""
    im = Image.new('RGBA', (16, 16)); a = _c(MID) * 0.7 + _c(BASE) * 0.3; b = _c(BASE)
    for y in range(16):
        c = a + (b - a) * min(1.0, y / 10)
        for x in range(16):
            im.putpixel((x, y), tuple(int(v) for v in c) + (255,))
    return im


DRAW = {'blot': _blot, 'fist': _fist, 'shield': _shield, 'question': _question, 'quill': _quill, 'puddle': _mound}
_CACHE = {}


def _art(name):
    """name: a shape, 'splat' or 'ball' -> (ink, shine)"""
    if name not in _CACHE:
        _CACHE[name] = (DRAW.get(name) or {'splat': _splat, 'ball': _ball}[name])()
    return _CACHE[name]


def _tex(name):
    """(kept for callers) a shape's ink texture"""
    return _art(name[len('ib_body_'):] if name.startswith('ib_body_') else name)[0]


def textures():
    T = {'ib_ink': _solid_ink(), 'ib_face': _face(), 'ib_nib': _nib()}
    for s in DRAW:
        T[f'ib_body_{s}'], T[f'ib_shine_{s}'] = _art(s)
    T['ib_puddle'], T['ib_puddle_shine'] = _art('splat')
    T['ib_ball'], T['ib_ball_shine'] = _art('ball')
    for k in FACES:
        T[f'ib_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def page(tex, x0, y0, L, pv, z=0.0, shine=None, w=None):
    """a flat picture, front and back (the back mirrored, so its outline matches) - no edges: seen side-on it's a sliver. With its
    wet shine a hair in front of it, front and back."""
    w = w or L
    els = [el((x0, y0, z - LD / 2 - 0.01), (x0 + w, y0 + L, z - LD / 2 - 0.01), tex, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
           el((x0, y0, z + LD / 2 + 0.01), (x0 + w, y0 + L, z + LD / 2 + 0.01), tex, pv, faces=('south',), uv={'south': [16, 0, 0, 16]})]
    if shine:                                                    # (unshaded: a wet glint is as bright as light, whichever way it faces)
        els += [dict(el((x0, y0, z - LD / 2 - 0.025), (x0 + w, y0 + L, z - LD / 2 - 0.025), shine, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}), shade=False),
                dict(el((x0, y0, z + LD / 2 + 0.025), (x0 + w, y0 + L, z + LD / 2 + 0.025), shine, pv, faces=('south',), uv={'south': [16, 0, 0, 16]}), shade=False)]
    return els


def splat(side, pv, cz=0.6):
    """the splat it stands in, lying on the floor (its wet shine a hair above it)"""
    h = side / 2
    return [el((-h, 0.1, cz - h), (h, 0.1, cz + h), 'ib_puddle', pv, faces=('up', 'down'), uv={'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0]}),
            dict(el((-h, 0.13, cz - h), (h, 0.13, cz + h), 'ib_puddle_shine', pv, faces=('up',), uv={'up': [0, 0, 16, 16]}), shade=False)]


def nib(x, y, tilt, pv):
    """the gold nib stuck in its head: in the middle of the page, so the ink's own faces cover the part pushed into it"""
    s = NIB_S; x0, y0 = x - s / 2, y - 0.4
    rot = (('z', tilt, (x, y, 0.0)) if tilt else None)
    return [el((x0, y0, -0.02), (x0 + s, y0 + s, -0.02), 'ib_nib', pv, rot=rot, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((x0, y0, 0.02), (x0 + s, y0 + s, 0.02), 'ib_nib', pv, rot=rot, faces=('south',), uv={'south': [16, 0, 0, 16]})]


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    bp = PIVOT['body']
    for s in SHAPES:
        L, cx, y0 = PAGE[s]
        art = 'blot' if s == 'drop' else s
        els = page(f'ib_body_{art}', cx - L / 2, y0, L, bp, shine=f'ib_shine_{art}')
        if s in SPLAT:
            els += splat(SPLAT[s], bp, 1.5 if s == 'puddle' else 0.6)
        if s in NIB:
            els += nib(*NIB[s], bp)
        part(f'ib_body_{s}', els)
    hp = PIVOT['head']
    for s in SHAPES:
        ex, ey, S = EYES[s]
        for fc in (None,) + FACES:
            ft = 'ib_face' if fc is None else f'ib_face_{fc}'
            e = el((ex - S / 2, ey - S / 2, -LD / 2 - 0.06), (ex + S / 2, ey + S / 2, -LD / 2 - 0.06), ft, hp, faces=('north',), uv={'north': [0, 0, 16, 16]})
            e['shade'] = False                                   # (white eyes stay white, whichever way it faces)
            part(f'ib_head_{s}' + (f'_x{fc}' if fc else ''), [e])
    # the pseudopods: ink pushed out of its sides - a thick reach, a thinner one, a round ball of ink at the end and a drop
    # hanging off it on a thread
    for s, sx in (('r', 1), ('l', -1)):
        a, b = PIVOT[f'pod{s}'], PIVOT[f'pod{s}2']
        part(f'ib_pod{s}', [seg(a, (b[0] + sx * 0.4, b[1], 0.0), 1.8, LD, 'ib_ink', a, up=(0.0, 0.0, -1.0))])
        tip = (sx * (POD_TIP - 0.6), b[1], 0.0)
        r = 1.25; dx = sx * (POD_TIP - 0.3)
        # (the drop gathering under the ball - about to fall)
        part(f'ib_pod{s}2', [seg(b, tip, 1.3, LD, 'ib_ink', b, up=(0.0, 0.0, -1.0))] +
             page('ib_ball', sx * POD_TIP - r, b[1] - r, 2 * r, b, shine='ib_ball_shine') +
             page('ib_ball', dx - 0.75, b[1] - 2.05, 1.5, b, z=0.005) + page('ib_ball', dx - 0.45, b[1] - 2.75, 0.9, b, z=0.01))
    gp = PIVOT['glob']; r = 2.0
    part('ib_glob', page('ib_ball', gp[0] + 0.6 - r, gp[1] - r, 2 * r, gp, z=-0.02, shine='ib_ball_shine'))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def pod(sx, up=0.0, fwd=0.0, tw=0.0):
    """a pseudopod's joint: raised (up, on the page; negative droops it), swung forward out of the page (fwd; negative: back)"""
    return qs(('y', fwd * sx), ('z', -up * sx), ('x', tw))


def P(**kw):
    return kw


def lean(fwd=0.0, side=0.0, turn=0.0):
    """the body from its base: leaning forward (fwd), toward its right (side), turned (turn: its right swinging back).
    (A shape standing in its splat leans no more than a few degrees: the splat must stay flat on the floor.)"""
    return qs(('y', turn), ('x', fwd), ('z', side))


def on_body(body, v):
    """a head shift (design units) as seen on the body's page: turned with the body, so the eyes slide over the ink, never into it
    (a pose's own shift, _o_head, is in the world's frame)"""
    return tuple(round(c, 4) for c in D(qrot(body, D(v))))


def walk(k):
    """it slides along in its splat, swaying and twisting, its eyes bobbing"""
    s, c = math.sin(math.pi * k / 2), abs(math.cos(math.pi * k / 2))
    b = lean(2, 3.5 * s, 8 * s)
    return dict(body=b, head=qs(('z', -4 * s)), _o_head=on_body(b, (0.3 * s, 0.35 * c, 0)))


def run(k):
    s = math.sin(math.pi * k / 2)
    return dict(_shape='drop', _face='determined' if k % 2 else None, _pods='rl', body=lean(16, 5 * s),
                podr=pod(1, 10 + 12 * s, -50), podr2=pod(1, 16), podl=pod(-1, 10 - 12 * s, -50), podl2=pod(-1, 16))


POSES = {
    # standing in its splat - looking at you
    'idle_a': P(body=lean(0, 1.5)),
    # shy: it turns half away, eyes down and away
    'idle_b': P(_face='shy', body=lean(0, -3, -18), head=qs(('z', 5)), _o_head=on_body(lean(0, -3, -18), (-0.4, -0.3, 0))),
    # playful: a pod peeks out and waggles at you
    'idle_c': P(_face='happy', _pods='l', body=lean(0, -3), podl=pod(-1, 40, 30), podl2=pod(-1, 50)),
    # thinking - and turning into what it's thinking about
    'idle_d': P(_shape='question', _face='puzzled', body=lean(0, 3, 10)),
    **{f'walk_{k}': P(**walk(k)) for k in range(4)},
    # running: off the floor, leaning hard into it, the pods streaming out behind
    **{f'run_{k}': P(**run(k)) for k in range(4)},
    'jump': P(_shape='drop', _face='surprised', _pods='rl', _off=(0, 4.0, 0), body=lean(-4), podr=pod(1, 60), podr2=pod(1, 30), podl=pod(-1, 60), podl2=pod(-1, 30)),
    # PUNCH: it balls itself up into a fist - drawn back - and lunges
    'punch_up': P(_shape='fist', _face='determined', body=lean(-16, 0, -14), _off=(0, 0, 2.0)),
    'punch': P(_shape='fist', _face='determined', body=lean(22, 0, 10), _off=(0, 0, -4.0)),
    # SPLASH: it rears up out of its splat, a glob of itself wound back on a pod - and flung
    'splash_up': P(_shape='drop', _face='determined', _pods='r', _glob=True, body=lean(-8, -6, -16), podr=pod(1, 70, -55), podr2=pod(1, 50)),
    'splash': P(_shape='drop', _face='happy', _pods='r', body=lean(12, 4, 14), podr=pod(1, 24, 50), podr2=pod(1, -6, 20)),
    # SPIKE: it gathers itself, turning side-on - then shoots up into a quill, point first at the foe
    'spike_up': P(_face='determined', body=lean(-3, 0, -20), _o_head=on_body(lean(-3, 0, -20), (0, -0.5, 0))),
    'spike': P(_shape='quill', _face='determined', body=lean(30), _off=(0, 0, -2.0)),
    # GUARD: a round shield of ink, braced - and taking the blow
    'guard': P(_shape='shield', _face='determined', body=lean(3)),
    'guard_b': P(_shape='shield', _face='hurt', body=lean(-4, 2, -12)),
    # WONDER: a question mark, tipping one way and the other
    'wonder': P(_shape='question', _face='puzzled', body=lean(0, 4, 12)),
    'wonder_b': P(_shape='question', _face='surprised', body=lean(0, -4, -12)),
    'happy': P(_face='happy', _pods='rl', body=lean(-2), podr=pod(1, 70), podr2=pod(1, 40), podl=pod(-1, 70), podl2=pod(-1, 40)),
    'wave_a': P(_face='happy', _pods='l', body=lean(0, -3), podl=pod(-1, 50), podl2=pod(-1, 50)),
    'wave_b': P(_face='happy', _pods='l', body=lean(0, -3), podl=pod(-1, 50), podl2=pod(-1, 10)),
    # sitting: it lets go and settles into a puddle, eyes peeking out of it...
    'sit_a': P(_shape='puddle'),
    # ...and there, its eyes drift off to one side and droop - dozing (the head moves: not the same as sit_a)
    'sit_b': P(_shape='puddle', _face='blink', head=qs(('z', -9)), _o_head=(-0.9, -0.45, 0)),
    'hurt': P(_shape='drop', _face='hurt', _pods='rl', body=lean(-14), podr=pod(1, 10, -50), podr2=pod(1, -20), podl=pod(-1, 10, -50), podl2=pod(-1, -20)),
    # fainted: spilt flat, eyes half shut and sunk low
    'tired': P(_shape='puddle', _face='sleepy', head=qs(('z', 6)), _o_head=(0.5, -0.7, 0)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (it swims like a little squid: leaning into the water, its pods pulling)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_shape='drop', _pods='rl', _off=(0, -3.0 + 0.6 * math.sin(_p), 0), body=lean(40, 4 * math.sin(_p)),
                            podr=pod(1, -10 + 40 * math.cos(_p), -30 - 20 * math.sin(_p)), podr2=pod(1, 20 + 20 * math.cos(_p)),
                            podl=pod(-1, -10 + 40 * math.cos(_p), -30 - 20 * math.sin(_p)), podl2=pod(-1, 20 + 20 * math.cos(_p)))


# every grounded pose rests on the floor: a shape in its splat stands with its base on it (the splat flat on the floor); the
# others put their lowest ink just on it (a run's high frames a little off it)
_ME = sys.modules[__name__]
_EDGE = {}


def _edge(shape):
    """points on the outline of a shape's page (design units, on the body) - the lowest ink of each column, the ends of each row"""
    if shape not in _EDGE:
        im = _tex(f'ib_body_{"blot" if shape == "drop" else shape}'); a = np.asarray(im.getchannel('A')) > 0
        L, cx, y0 = PAGE[shape]; pts = set()
        for x in range(N):
            ys = np.nonzero(a[:, x])[0]
            if len(ys): pts.add((x, ys.max())); pts.add((x, ys.min()))
        for y in range(N):
            xs = np.nonzero(a[y])[0]
            if len(xs): pts.add((xs.min(), y)); pts.add((xs.max(), y))
        _EDGE[shape] = [(cx + L / 2 - (x + 0.5) * L / N, y0 + L - (y + 1.0) * L / N, 0.0) for x, y in pts]
    return _EDGE[shape]


def _low(pose):
    low = min(point(_ME, pose, 'body', p)[1] * 16 for p in _edge(pose.get('_shape', 'blot')))
    for s in ('r', 'l'):
        if s in pose.get('_pods', ''):
            sx = 1 if s == 'r' else -1
            for q in ((sx * (POD_TIP + 1.25), PIVOT['podr'][1], 0.0), (sx * (POD_TIP - 0.3), PIVOT['podr'][1] - 3.3, 0.0)):
                low = min(low, point(_ME, pose, f'pod{s}2', q)[1] * 16)
    return low


def _ground(pose, lift=0.0):
    pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
    if pose.get('_shape', 'blot') in SPLAT:
        pose['_off'] = (o[0], 0.0, o[2])
    else:
        pose['_off'] = (o[0], round(lift - _low(dict(pose, _off=(o[0], 0.0, o[2]))), 3), o[2])
    return pose


AIR = {'jump'}
for _k in list(POSES):
    if _k.startswith('swim_') or _k in AIR:
        continue
    POSES[_k] = _ground(POSES[_k], lift=(1.2 if _k in ('run_1', 'run_3') else 0.0))
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'idle_d', 'walk_1', 'walk_3', 'run_1', 'jump', 'punch_up', 'punch', 'splash_up', 'splash',
         'spike_up', 'spike', 'guard', 'guard_b', 'wonder', 'wonder_b', 'happy', 'wave_a', 'sit_a', 'sit_b', 'hurt', 'tired', 'swim_2']
