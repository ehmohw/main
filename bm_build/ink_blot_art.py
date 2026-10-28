"""The Ink Blot (draft): a blot that dripped off Mr. Capshun's pen while he was narrating the history of the Underwater Kingdom - a
Buddy the Gem of Creativity never meant to make, half a story and half a spill. It turns into whatever it's thinking about (or
whatever Capshun happens to be narrating). Shy but playful. Capshun is embarrassed by it.

FLAT and drawn like Mr. Capshun (the same ink, #161616, the same flat drawn page): a glossy black blot standing up - a rounded
splat with drippy edges, a few drips hanging off its base onto a little pool, splatter droplets flicked round it, a white gloss
streak on the ink - and two big white empty oval eyes, like Capshun's. About as tall as Capshun's waist-to-chest.

No limbs: it pushes out ink pseudopods when it needs them (podr/podl, hidden unless a pose asks: `_pods`), and it SHAPESHIFTS -
the body's model is chosen by the pose's `_shape`:
    blot      the default: the standing splat
    fist      a big ink fist on a wrist of ink (punch)
    shield    a round shield, rimmed, dripping onto its pool (guard)
    question  a question mark - the dot is its pool (curious, confused: wonder)
    puddle    flattened to a puddle on the ground, eyes peeking out of a little mound (sitting, sleeping, fainted)
    quill     a pointed pen nib, slit and breather hole (spike) - it dripped off a pen, after all

A rigkit rig: body (pivot at its base, on the ground: it sways and leans from there; a model per shape), head (the eyes and mouth -
a see-through panel just in front of the ink, a model per shape x expression, each shape placing the eyes on itself), the
pseudopods (two joints each, an ink ball at the tip) and the glob (an ink ball held at the right pod's tip: splash_up).
Design units: feet at y=0, facing -z, its right is +x. Nothing floats: every grounded pose puts the lowest ink just on the floor."""
import math
import sys
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg, point

PREFIX = 'ib_'
RIG_SCALE = 1.1                                   # (its crown between Capshun's waist and chest)
PIVOT = {'body': (0, 0, 0), 'head': (0, 10.4, 0),
         'podr': (4.4, 7.6, 0), 'podr2': (9.2, 7.6, 0), 'podl': (-4.4, 7.6, 0), 'podl2': (-9.2, 7.6, 0),
         'glob': (13.0, 7.6, 0)}
PARENT = {'body': None, 'head': 'body', 'podr': 'body', 'podr2': 'podr', 'podl': 'body', 'podl2': 'podl', 'glob': 'podr2'}
PARTS = tuple(PIVOT)
PART_K = {}
SHAPES = ('blot', 'fist', 'shield', 'question', 'puddle', 'quill')
FACES = ('happy', 'surprised', 'blink', 'determined', 'hurt', 'shy', 'puzzled', 'sleepy')
INK = '#161616'
GLOSS = '#f4f4f6'
SHEEN = '#2c2c32'                                 # (the ink's faint sheen, lit from the upper left - glossy, not grey)
LINE = '#46464e'                                  # (lines drawn inside the ink: the fist's fingers, the shield's rim, the nib's slit)
LD = 0.3                                          # (its depth: flat as a page)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
POD_TIP = 13.0                                    # (the pod's rest line: straight out at its sides, the ink ball at x = +-13)

# each upright shape is one square page: (its side L, its centre x, its bottom y) in design units; and where its eyes go on it:
# (centre x, centre y, the eye panel's side)
PAGE = {'blot': (16.0, 0.0, 0.0), 'fist': (16.0, 0.0, 0.0), 'shield': (16.0, 0.0, 0.0), 'question': (18.0, 0.0, 0.0),
        'quill': (22.0, 0.0, 0.0), 'puddle': (10.0, 0.0, 0.0)}
EYES = {'blot': (0.0, 10.4, 9.0), 'fist': (1.0, 10.6, 7.0), 'shield': (0.0, 10.6, 8.6), 'question': (0.6, 14.2, 6.6),
        'quill': (0.0, 6.6, 6.8), 'puddle': (0.0, 2.6, 6.4)}
PUDDLE = 20.0                                     # (the puddle lying on the floor: its side, design units)


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


def _down(im):
    im = im.resize((N, N), Image.LANCZOS); px = im.load()
    for y in range(N):
        for x in range(N):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a >= 128 else 0)
    return im


class Page:
    """an ink drawing on a 128 grid (drawn SS x over): a mask of where the ink is, then the ink laid in with its sheen and gloss"""
    def __init__(self):
        self.S = N * SS
        self.mask = Image.new('L', (self.S, self.S), 0); self.m = ImageDraw.Draw(self.mask)
        self.holes = []

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

    def stroke(self, pts, w, n=6):
        """a thick stroke along a polyline: discs swept along it (round ends, round joins)"""
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            k = max(2, int(math.hypot(x1 - x0, y1 - y0) / 1.5))
            for i in range(k + 1):
                t = i / k; self.dot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w / 2)

    def drip(self, x, y0, y1, w):
        """a drip hanging off the ink: a run of ink from y0 down to a round drop at y1"""
        self.rrect((x - w / 2, y0, x + w / 2, y1 - w * 0.4), w / 2)
        self.dot(x, y1 - w * 0.62, w * 0.62)

    def hole(self, box):
        self.holes.append(box)

    def ink(self, gloss=(), lines=(), sheen=(34, 20, 96, 92)):
        """-> the page as a texture: the ink (with a faint sheen toward the upper left), its gloss streaks, the lines drawn in it"""
        S = self.S
        for b in self.holes:
            self.m.ellipse(self.E(b), fill=0)
        im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); px = im.load(); mk = self.mask.load()
        c0, c1 = hexc(INK), hexc(SHEEN)
        sx0, sy0, sx1, sy1 = (v * SS for v in sheen); hx, hy, hr = (sx0 + sx1) / 2, (sy0 + sy1) / 2, (sx1 - sx0) / 2
        for y in range(S):
            for x in range(S):
                if mk[x, y] >= 128:
                    t = max(0.0, 1 - math.hypot(x - hx, (y - hy) * 1.1) / hr) ** 1.4
                    px[x, y] = tuple(round(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)) + (255,)
        d = ImageDraw.Draw(im)
        for kind, a, b in lines:
            if kind == 'arc':
                d.arc(self.E(a), b[0], b[1], fill=hexc(LINE), width=round(b[2] * SS))
            elif kind == 'line':
                d.line([(x * SS, y * SS) for x, y in a], fill=hexc(LINE), width=round(b * SS), joint='curve')
            elif kind == 'rrect':
                d.rounded_rectangle(self.E(a), b[0] * SS, outline=hexc(LINE), width=round(b[1] * SS))
            elif kind == 'ring':
                d.ellipse(self.E(a), outline=hexc(LINE), width=round(b * SS))
        for kind, a, b in gloss:
            if kind == 'arc':
                d.arc(self.E(a), b[0], b[1], fill=hexc(GLOSS), width=round(b[2] * SS))
            elif kind == 'dot':
                x, y, r = a; d.ellipse(self.E((x - r, y - r, x + r, y + r)), fill=hexc(GLOSS))
        # (nothing painted outside the ink - the gloss and lines are clipped to it)
        al = Image.new('L', (S, S), 0); al.paste(self.mask.point(lambda v: 255 if v >= 128 else 0))
        im.putalpha(Image.composite(im.getchannel('A'), al, al))
        return _down(im)


def _splatter(p, spots):
    for x, y, r in spots:
        p.dot(x, y, r)


def _blot():
    """the standing splat: a round body settling wider at the bottom, a few soft lumps on its crown, drips running off its sides and
    hanging off its base into the pool it stands in, droplets flicked round it"""
    p = Page()
    p.oval((22, 8, 106, 96))                                    # (the body)
    p.oval((14, 54, 114, 108))                                  # (settling wider at the bottom)
    p.oval((10, 104, 118, 127.4))                               # (the pool it stands in)
    for a, r in ((214, 9), (250, 7), (296, 8), (334, 7)):
        t = math.radians(a)
        p.dot(64 + 40 * math.cos(t), 52 + 40 * math.sin(t), r)   # (soft lumps on its crown)
    p.drip(15, 70, 100, 7); p.drip(113, 74, 96, 6); p.drip(26, 96, 114, 6)
    _splatter(p, ((6, 44, 3.2), (12, 28, 2.2), (4, 70, 2.2), (122, 40, 3.0), (116, 22, 2.0), (124, 64, 2.2)))
    return p.ink(gloss=(('arc', (20, 10, 100, 90), (200, 234, 5.5)), ('dot', (24, 60, 3.0), None)),
                 sheen=(14, 6, 92, 84))


def _fist():
    """a big ink fist, side-on (the classic cartoon punch): curled fingers to the front, the thumb wrapped over them, on a wrist
    of ink that runs down into its pool"""
    p = Page()
    p.rrect((20, 16, 106, 88), 22)                              # (the hand)
    for i, y in enumerate((18, 35, 52, 69)):                    # (four curled fingers, knuckles to the front - our right)
        p.rrect((86, y, 116, y + 19), 9)
    p.rrect((40, 60, 104, 80), 10)                              # (the thumb, across the fingers)
    p.poly([(40, 84), (88, 84), (80, 112), (48, 112)])          # (the wrist)
    p.oval((24, 106, 104, 127.4))                               # (its pool)
    p.drip(30, 104, 124, 6)
    _splatter(p, ((8, 34, 2.6), (12, 58, 2.0), (6, 84, 2.2), (122, 102, 2.2)))
    lines = [('line', [(96, 35.5), (112, 35.5)], 2.2), ('line', [(96, 52.5), (112, 52.5)], 2.2), ('line', [(96, 69.5), (112, 69.5)], 2.2),
             ('rrect', (40, 60, 104, 80), (10, 2.2)), ('line', [(88, 22), (88, 84)], 1.6)]
    return p.ink(gloss=(('arc', (24, 18, 84, 80), (190, 250, 5)), ('dot', (110, 22, 2.2), None)), lines=lines, sheen=(18, 12, 90, 76))


def _shield():
    """a round shield of ink, rimmed - dripping off its bottom edge into the pool it stands in"""
    p = Page()
    p.oval((12, 4, 116, 108))                                   # (the shield)
    p.poly([(52, 100), (76, 100), (82, 118), (46, 118)])        # (its foot of ink)
    p.oval((30, 112, 98, 127.4))
    p.drip(26, 86, 112, 7); p.drip(102, 86, 104, 6); p.drip(84, 104, 124, 5)
    _splatter(p, ((5, 30, 2.4), (122, 22, 2.6), (124, 60, 2.0), (6, 70, 2.0)))
    return p.ink(gloss=(('arc', (24, 14, 84, 74), (190, 252, 5.5)), ('dot', (100, 30, 2.4), None)),
                 lines=[('ring', (22, 14, 106, 98), 2.4)], sheen=(14, 4, 96, 86))


def _question():
    """a question mark: a heavy hook (the eyes peek out of the top of it), the stem dripping down on a thread into the dot - its pool"""
    p = Page()
    hook = [(26, 44), (28, 30), (38, 18), (52, 12), (68, 12), (84, 18), (96, 30), (98, 44), (92, 56), (80, 64), (68, 70), (64, 80), (64, 92)]
    p.stroke(hook, 22)
    p.oval((34, 6, 94, 40))                                     # (the hook's top, swollen: room for the eyes)
    p.dot(28, 42, 13)                                           # (the hook's ball end)
    p.stroke([(64, 92), (64, 106)], 7)                          # (the thread down to the dot)
    p.oval((44, 100, 84, 127.4))                                # (the dot)
    p.drip(80, 70, 86, 6)
    _splatter(p, ((10, 70, 2.4), (116, 64, 2.6), (110, 90, 2.0), (16, 92, 2.0)))
    return p.ink(gloss=(('arc', (40, 10, 92, 44), (195, 250, 4.5)), ('dot', (22, 38, 2.6), None), ('dot', (56, 108, 2.4), None)),
                 sheen=(30, 4, 96, 50))


def _quill():
    """a pen nib, pointed: shot up out of its pool into a spike - the slit down its point, the breather hole (a real hole)"""
    p = Page()
    p.poly([(64, 1), (82, 34), (96, 66), (100, 84), (28, 84), (32, 66), (46, 34)])
    p.oval((26, 64, 102, 104))                                  # (the nib's shoulders, round)
    p.poly([(44, 100), (84, 100), (92, 120), (36, 120)])
    p.oval((22, 112, 106, 127.4))
    p.drip(30, 94, 118, 6); p.drip(98, 92, 114, 6)
    p.hole((59, 40, 69, 50))
    _splatter(p, ((12, 56, 2.6), (116, 50, 2.2), (6, 90, 2.0), (122, 86, 2.4), (20, 36, 1.8)))
    return p.ink(gloss=(('arc', (40, 40, 108, 120), (200, 238, 4)), ('dot', (40, 76, 2.2), None)),
                 lines=[('line', [(64, 6), (64, 40)], 1.8)], sheen=(28, 24, 92, 100))


def _mound():
    """the puddle's mound: a low lump with the eyes peeking out of it"""
    p = Page()
    p.oval((12, 26, 116, 170))
    p.dot(10, 112, 7); p.dot(118, 110, 6)
    return p.ink(gloss=(('arc', (24, 30, 90, 120), (200, 245, 5)),), sheen=(16, 22, 90, 110))


def _puddle_top():
    """the puddle from above: a wide splat, lumpy edged, droplets flicked out round it"""
    p = Page()
    p.oval((14, 18, 114, 110))
    for a, r in ((0, 10), (35, 8), (80, 11), (128, 9), (170, 10), (210, 8), (250, 11), (300, 9), (330, 7)):
        t = math.radians(a); p.dot(64 + 48 * math.cos(t), 64 + 44 * math.sin(t), r)
    _splatter(p, ((6, 30, 3), (122, 22, 2.6), (120, 104, 3), (10, 112, 2.4), (64, 4, 2.2), (60, 124, 2.4)))
    return p.ink(gloss=(('arc', (26, 26, 90, 90), (190, 250, 5)), ('dot', (98, 88, 2.6), None)), sheen=(10, 10, 90, 90))


def _ball():
    p = Page()
    p.dot(64, 64, 60)
    return p.ink(gloss=(('arc', (22, 22, 98, 98), (195, 255, 12)),), sheen=(4, 4, 90, 90))


def _face(kind=None):
    """the eyes (his right on our left): two big white empty ovals, his left a touch bigger and higher - like Capshun's - and a small
    mouth, all in white on the ink. A see-through panel: each expression redraws them (and cuts lids back into the ink)."""
    S = N * SS; k = SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W = hexc('#fafafa'); CUT = (0, 0, 0, 0)
    E = lambda b: tuple(v * k for v in b)
    P = lambda pts: [(x * k, y * k) for x, y in pts]
    le, re = (22, 30, 56, 88), (70, 22, 106, 88)

    def eye(box):
        d.ellipse(E(box), fill=W)

    def arc(box, a0, a1, w=6):
        d.arc(E(box), a0, a1, fill=W, width=round(w * k))
    if kind == 'blink':
        arc((22, 46, 56, 70), 20, 160, 6); arc((70, 42, 106, 68), 20, 160, 6)
    elif kind == 'happy':
        arc((22, 48, 56, 82), 195, 345, 7); arc((70, 42, 106, 78), 195, 345, 7)
    elif kind == 'surprised':
        eye((18, 22, 58, 92)); eye((66, 12, 110, 92))
    elif kind == 'hurt':
        d.line(P([(26, 44), (50, 58), (26, 72)]), fill=W, width=7 * k, joint='curve')
        d.line(P([(102, 42), (76, 58), (102, 74)]), fill=W, width=7 * k, joint='curve')
    elif kind == 'shy':                                                                  # (looking away, down to our left)
        eye((14, 40, 42, 88)); eye((54, 34, 86, 88))
        for x in (20, 30, 40):
            d.line(P([(x + 4, 96), (x, 104)]), fill=W, width=round(2.4 * k))
        for x in (76, 86, 96):
            d.line(P([(x + 4, 96), (x, 104)]), fill=W, width=round(2.4 * k))
    elif kind == 'puzzled':
        eye((20, 40, 52, 86)); eye((68, 16, 108, 88))
    else:
        eye(le); eye(re)
    # lids cut back into the ink
    if kind == 'determined':
        d.polygon(P([(18, 20), (60, 20), (60, 58)]), fill=CUT); d.polygon(P([(66, 12), (110, 12), (66, 52)]), fill=CUT)
    elif kind == 'sleepy':
        d.rectangle(E((18, 18, 58, 60)), fill=CUT); d.rectangle(E((66, 10, 110, 56)), fill=CUT)
    elif kind == 'puzzled':
        d.polygon(P([(16, 30), (58, 30), (58, 60), (16, 52)]), fill=CUT)                   # (one squinting...)
    # the mouth
    if kind in (None, 'shy'):
        arc((54, 92, 76, 108), 25, 155, 4) if kind is None else arc((58, 104, 70, 114), 200, 340, 3.4)
    elif kind == 'happy':
        d.chord(E((46, 88, 84, 118)), 0, 180, fill=W)
    elif kind == 'surprised':
        d.ellipse(E((57, 98, 71, 116)), outline=W, width=round(3.6 * k))
    elif kind == 'determined':
        d.line(E((52, 106, 78, 102)), fill=W, width=round(4 * k))
    elif kind == 'hurt':
        d.line(P([(46, 110), (54, 104), (62, 110), (70, 104), (78, 110)]), fill=W, width=round(3.6 * k), joint='curve')
    elif kind == 'puzzled':
        d.line(P([(62, 108), (70, 104), (78, 108), (86, 104)]), fill=W, width=round(3.4 * k), joint='curve')
    elif kind == 'sleepy':
        arc((56, 100, 72, 110), 20, 160, 3.4)
    # blink: no mouth (asleep, or a moment's shyness)
    return _down(im)


def _solid(c):
    return Image.new('RGBA', (16, 16), hexc(c)[:3] + (255,))


DRAW = {'blot': _blot, 'fist': _fist, 'shield': _shield, 'question': _question, 'quill': _quill, 'puddle': _mound}
_CACHE = {}


def _tex(name):
    if name not in _CACHE:
        _CACHE[name] = (DRAW[name[len('ib_body_'):]] if name.startswith('ib_body_') else
                        {'ib_puddle': _puddle_top, 'ib_ball': _ball}[name])()
    return _CACHE[name]


def textures():
    T = {'ib_ink': _solid(INK), 'ib_face': _face()}
    for s in SHAPES:
        T[f'ib_body_{s}'] = _tex(f'ib_body_{s}')
    T['ib_puddle'] = _tex('ib_puddle'); T['ib_ball'] = _tex('ib_ball')
    for k in FACES:
        T[f'ib_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def page(tex, x0, y0, L, pv, z=0.0):
    """a flat picture, front and back (the back mirrored, so its outline matches) - no edges: seen side-on it's a sliver"""
    return [el((x0, y0, z - LD / 2 - 0.01), (x0 + L, y0 + L, z - LD / 2 - 0.01), tex, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((x0, y0, z + LD / 2 + 0.01), (x0 + L, y0 + L, z + LD / 2 + 0.01), tex, pv, faces=('south',), uv={'south': [16, 0, 0, 16]})]


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    bp = PIVOT['body']
    for s in SHAPES:
        L, cx, y0 = PAGE[s]
        els = page(f'ib_body_{s}', cx - L / 2, y0, L, bp)
        if s == 'puddle':                                       # (and the puddle itself, lying on the floor)
            h = PUDDLE / 2
            els += [el((-h, 0.12, -h + 1.5), (h, 0.12, h + 1.5), 'ib_puddle', bp, faces=('up', 'down'),
                       uv={'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0]})]
        part(f'ib_body_{s}', els)
    hp = PIVOT['head']
    for s in SHAPES:
        ex, ey, S = EYES[s]
        for fc in (None,) + FACES:
            ft = 'ib_face' if fc is None else f'ib_face_{fc}'
            e = el((ex - S / 2, ey - S / 2, -LD / 2 - 0.04), (ex + S / 2, ey + S / 2, -LD / 2 - 0.04), ft, hp, faces=('north',), uv={'north': [0, 0, 16, 16]})
            part(f'ib_head_{s}' + (f'_x{fc}' if fc else ''), [e])
    # the pseudopods: ink pushed out of its sides - a thick reach, a thinner one, and a round ball of ink at the end
    for s, sx in (('r', 1), ('l', -1)):
        a, b = PIVOT[f'pod{s}'], PIVOT[f'pod{s}2']
        part(f'ib_pod{s}', [seg(a, (b[0] + sx * 0.4, b[1], 0.0), 1.7, LD, 'ib_ink', a, up=(0.0, 0.0, -1.0))])
        tip = (sx * (POD_TIP - 0.6), b[1], 0.0)
        r = 1.15
        part(f'ib_pod{s}2', [seg(b, tip, 1.25, LD, 'ib_ink', b, up=(0.0, 0.0, -1.0))] +
             page('ib_ball', sx * POD_TIP - r, b[1] - r, 2 * r, b))
    gp = PIVOT['glob']; r = 2.0
    part('ib_glob', page('ib_ball', gp[0] + 0.6 - r, gp[1] - r, 2 * r, gp, z=-0.02))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def pod(sx, up=0.0, fwd=0.0, tw=0.0):
    """a pseudopod's joint: raised (up, on the page; negative droops it), swung forward out of the page (fwd; negative: back)"""
    return qs(('y', fwd * sx), ('z', -up * sx), ('x', tw))


def P(**kw):
    return kw


def lean(fwd=0.0, side=0.0, turn=0.0):
    """the body from its base: leaning forward (fwd), toward its right (side), turned (turn: its right swinging back)"""
    return qs(('y', turn), ('x', fwd), ('z', side))


def walk(k, lift=0.0):
    s = math.sin(math.pi * k / 2)
    return dict(body=lean(4, 7 * s), head=qs(('z', -3 * s)), _off=(0, lift * abs(math.cos(math.pi * k / 2)), 0))


def run(k):
    s = math.sin(math.pi * k / 2)
    return dict(_face='determined' if k % 2 else None, _pods='rl', body=lean(16, 5 * s),
                podr=pod(1, 10 + 12 * s, -50), podr2=pod(1, 16), podl=pod(-1, 10 - 12 * s, -50), podl2=pod(-1, 16),
                _off=(0, 0, 0))


POSES = {
    # standing in its pool, a little wobble - looking at you
    'idle_a': P(body=lean(0, 2)),
    # shy: it shrinks off to one side, eyes away
    'idle_b': P(_face='shy', body=lean(-3, -8, -12)),
    # playful: a pod peeks out and waggles at you
    'idle_c': P(_face='happy', _pods='l', body=lean(0, -4), podl=pod(-1, 40, 30), podl2=pod(-1, 50)),
    # thinking - and turning into what it's thinking about
    'idle_d': P(_shape='question', _face='puzzled', body=lean(0, 6)),
    # it doesn't walk: it slops along, swaying side to side, a hop in every step
    **{f'walk_{k}': P(**walk(k, lift=0.6)) for k in range(4)},
    # running: leaning hard into it, the pods streaming out behind
    **{f'run_{k}': P(**run(k)) for k in range(4)},
    'jump': P(_face='surprised', _pods='rl', _off=(0, 4.0, 0), body=lean(-4), podr=pod(1, 60), podr2=pod(1, 30), podl=pod(-1, 60), podl2=pod(-1, 30)),
    # PUNCH: it balls itself up into a fist - drawn back - and lunges
    'punch_up': P(_shape='fist', _face='determined', body=lean(-16, 0, -14), _off=(0, 0, 2.0)),
    'punch': P(_shape='fist', _face='determined', body=lean(22, 0, 10), _off=(0, 0, -4.0)),
    # SPLASH: a glob of itself wound back on a pod over its head - and flung (a splat thrown)
    'splash_up': P(_face='determined', _pods='r', _glob=True, body=lean(-8, -6, -16), podr=pod(1, 70, -55), podr2=pod(1, 50)),
    'splash': P(_face='happy', _pods='r', body=lean(12, 4, 14), podr=pod(1, 24, 50), podr2=pod(1, -6, 20)),
    # SPIKE: it gathers itself, leaning back - then shoots up into a quill, point first at the foe
    'spike_up': P(_face='determined', body=lean(-12)),
    'spike': P(_shape='quill', _face='determined', body=lean(30), _off=(0, 0, -2.0)),
    # GUARD: a round shield of ink, braced - and taking the blow
    'guard': P(_shape='shield', _face='determined', body=lean(6)),
    'guard_b': P(_shape='shield', _face='hurt', body=lean(-10, 3)),
    # WONDER: a question mark, tipping one way and the other
    'wonder': P(_shape='question', _face='puzzled', body=lean(0, 10)),
    'wonder_b': P(_shape='question', _face='surprised', body=lean(0, -8)),
    'happy': P(_face='happy', _pods='rl', _off=(0, 1.6, 0), body=lean(-4), podr=pod(1, 70), podr2=pod(1, 40), podl=pod(-1, 70), podl2=pod(-1, 40)),
    'wave_a': P(_face='happy', _pods='l', body=lean(0, -4), podl=pod(-1, 50), podl2=pod(-1, 50)),
    'wave_b': P(_face='happy', _pods='l', body=lean(0, -4), podl=pod(-1, 50), podl2=pod(-1, 10)),
    # sitting: it lets go and settles into a puddle, eyes peeking out of it...
    'sit_a': P(_shape='puddle'),
    # ...and dozes off there
    'sit_b': P(_shape='puddle', _face='blink'),
    'hurt': P(_face='hurt', _pods='rl', body=lean(-14), podr=pod(1, 10, -50), podr2=pod(1, -20), podl=pod(-1, 10, -50), podl2=pod(-1, -20)),
    # fainted: spilt flat, eyes half shut
    'tired': P(_shape='puddle', _face='sleepy'),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (it swims like a little squid: leaning into the water, its pods pulling)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_pods='rl', _off=(0, -3.0 + 0.6 * math.sin(_p), 0), body=lean(40, 4 * math.sin(_p)),
                            podr=pod(1, -10 + 40 * math.cos(_p), -30 - 20 * math.sin(_p)), podr2=pod(1, 20 + 20 * math.cos(_p)),
                            podl=pod(-1, -10 + 40 * math.cos(_p), -30 - 20 * math.sin(_p)), podl2=pod(-1, 20 + 20 * math.cos(_p)))


# every grounded pose rests its lowest ink just on the floor (a hop's high frames a little off it)
_ME = sys.modules[__name__]
_EDGE = {}


def _edge(shape):
    """points on the outline of a shape's page (design units, on the body) - the lowest ink of each column, the ends of each row"""
    if shape not in _EDGE:
        im = _tex(f'ib_body_{shape}'); a = im.getchannel('A').load(); L, cx, y0 = PAGE[shape]; pts = set()
        for x in range(N):
            ys = [y for y in range(N) if a[x, y]]
            if ys: pts.add((x, max(ys))); pts.add((x, min(ys)))
        for y in range(N):
            xs = [x for x in range(N) if a[x, y]]
            if xs: pts.add((min(xs), y)); pts.add((max(xs), y))
        des = [(cx + L / 2 - (x + 0.5) * L / N, y0 + L - (y + 1.0) * L / N) for x, y in pts]
        if shape == 'puddle':
            des += [(PUDDLE / 2 * math.cos(t), 0.12, PUDDLE / 2 * math.sin(t) + 1.5) for t in (i * math.pi / 8 for i in range(16))]
        _EDGE[shape] = [(p[0], p[1], p[2] if len(p) > 2 else 0.0) for p in des]
    return _EDGE[shape]


def _low(pose):
    low = min(point(_ME, pose, 'body', p)[1] * 16 for p in _edge(pose.get('_shape', 'blot')))
    for s in ('r', 'l'):
        if s in pose.get('_pods', ''):
            low = min(low, point(_ME, pose, f'pod{s}2', ((1 if s == 'r' else -1) * (POD_TIP + 1.15), PIVOT['podr'][1], 0.0))[1] * 16)
    return low


def _ground(pose, lift=0.0):
    pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
    pose['_off'] = (o[0], round(lift - _low(dict(pose, _off=(o[0], 0.0, o[2]))), 3), o[2])
    return pose


AIR = {'jump'}
for _k in list(POSES):
    if _k.startswith('swim_') or _k in AIR:
        continue
    POSES[_k] = _ground(POSES[_k], lift=(1.2 if _k in ('run_1', 'run_3') else 0.6 if _k in ('walk_1', 'walk_3') else 0.0))
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'idle_d', 'walk_1', 'walk_3', 'run_1', 'jump', 'punch_up', 'punch', 'splash_up', 'splash',
         'spike_up', 'spike', 'guard', 'guard_b', 'wonder', 'wonder_b', 'happy', 'wave_a', 'sit_a', 'sit_b', 'hurt', 'tired', 'swim_2']
