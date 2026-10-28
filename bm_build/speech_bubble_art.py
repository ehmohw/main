"""The Speech Bubble (draft): Mr. Capshun narrated so loudly, near the Gem of Creativity, that his words came alive. One of the
Buddies, the strange folk born of pure imagination - and the loudest of them. Its body is its words: it fights by SHOUTING comic-book
sound effects that physically hit things (BAM! POW! ZAP! KRAK!) - and when it isn't fighting, its words still show: ZZZ when it
sleeps, ? when it's confused, ! when it's alarmed, ... when things get awkward. Loud, dramatic, theatrical; a show-off.

THE LOOK: drawn like Mr. Capshun - flat, a page come to life, a bold black outline. A white comic speech bubble (a rounded oval,
shaded off at one side like pencil on paper) with its little pointed tail at the bottom - the tail is its one "foot", and it hops
on it. A face drawn on the bubble: big black eyes with a glint, thick expressive brows, a big mouth. About Mr. Capshun's chest height.

  _shape (the bubble's outline, and the tail that goes with it):
    'speech'  - the rounded oval (the default)
    'shout'   - a spiky starburst outline with a jagged lightning tail (when it attacks)
    'thought' - a cloud of bumps, its tail a trail of three little circles (idle / thinking; it hops on the smallest)
    'puff'    - swollen big and round, a breath held in (the wind-up of its big blast)
  _tail: 'none' tucks the tail away (sitting, sleeping: it has sat down on it); otherwise the tail follows _shape.
  _word (a separate flat model it shows, floating just in front of it - 'none' or absent: hidden):
    'bam', 'pow', 'zap', 'krak'  - bold comic lettering (yellow / red, a heavy black outline) on a bursting starburst
    'zzz' (asleep), 'q' (?, confused), 'bang' (!, alarmed), 'dots' (..., awkward)

FLAT: every part is a pair of planes (front and back) with no edges - side-on it all but vanishes, like Capshun.

A rigkit rig: body (the bubble - root, its joint at the bubble's middle; a model per _shape), face (a decal just in front of the
bubble, a model per FACE; '_o_face' slides it a little - a look to one side), tail (its joint at the bubble's bottom, a model per
shape; it swings a little as it hops), word (a root of its own, floating above and just in front; '_o_word' throws it about).
Design units: the tail's tip at y=0, facing -z, its right is +x. It floats only when hopping (walk/run/jump frames are airborne)."""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, point

PREFIX = 'sbb_'
RIG_SCALE = 1.0                                    # (the bubble's top at ~1.07 blocks: Mr. Capshun's chest)
PIVOT = {'body': (0, 11.2, 0), 'face': (0, 11.2, 0), 'tail': (1.0, 5.8, 0), 'word': (0, 22.6, -1.2)}
PARENT = {'body': None, 'face': 'body', 'tail': 'body', 'word': None}
PARTS = tuple(PIVOT)
PART_K = {}
SHAPES = ('speech', 'shout', 'thought', 'puff')
WORDS = ('bam', 'pow', 'zap', 'krak', 'zzz', 'q', 'bang', 'dots')
FACES = ('happy', 'surprised', 'blink', 'fierce', 'shout', 'hurt', 'smug', 'puzzled', 'puff', 'dizzy')
INK = '#161616'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
OW = 0.62                                          # (the outline's width, design units - bold, like Capshun's head)
LD = 0.32                                          # (the gap between front and back planes - it's flat)

# the squares the textures are painted on (design units: centre, half side)
BODY_C, BODY_H, BODY_N = (0.0, 11.4), 10.0, 256
TAIL_C, TAIL_H, TAIL_N = (0.5, 3.8), 4.2, 128
FACE_C, FACE_H, FACE_N = (0.0, 11.6), 6.0, 128
WORD_H, WORD_N = 6.0, 256
SS = 4


def HIDDEN(p, pose):
    if p == 'word':
        return pose.get('_word', 'none') in (None, 'none')
    if p == 'tail':
        return pose.get('_tail') == 'none'
    return False


def model_name(p, pose, suffix=''):
    shape = pose.get('_shape', 'speech')
    if p == 'body':
        return f'{PREFIX}body_{shape}{suffix}'
    if p == 'tail':
        t = pose.get('_tail') or shape
        return f'{PREFIX}tail_{shape if t == "none" else t}{suffix}'
    if p == 'word':
        return f'{PREFIX}word_{pose.get("_word") or "bam"}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'face' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- the shapes (design units)
def _ellipse(c, rx, ry, n=160):
    return [(c[0] + rx * math.cos(2 * math.pi * i / n), c[1] + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _burst(c, rx, ry, spikes, outer, inner, seed, phase=0.0):
    rnd = random.Random(seed); pts = []
    for i in range(2 * spikes):
        a = phase + math.pi * i / spikes + rnd.uniform(-0.06, 0.06)
        f = outer * rnd.uniform(0.9, 1.0) if i % 2 == 0 else inner * rnd.uniform(0.96, 1.04)
        pts.append((c[0] + rx * f * math.cos(a), c[1] + ry * f * math.sin(a)))
    return pts


SPEECH = dict(c=(0.0, 11.2), rx=7.2, ry=5.6)
PUFF = dict(c=(0.0, 12.0), rx=8.4, ry=6.5)
# (the starburst: a valley at the very bottom, where the jagged tail comes out)
SHOUT_POLY = _burst((0.0, 11.4), 7.4, 5.9, 15, 1.24, 0.9, 'sbb-shout', phase=-math.pi / 2 + math.pi / 15)
# (the cloud: bumps round an ellipse, a little bigger and smaller by turns)
CLOUD = [((0.0 + 5.7 * math.cos(2 * math.pi * i / 11 + 0.3), 11.5 + 3.9 * math.sin(2 * math.pi * i / 11 + 0.3)), 2.55 + 0.35 * ((i * 7) % 3 - 1))
         for i in range(11)]
CLOUD_CORE = _ellipse((0.0, 11.5), 5.7, 3.9)
THOUGHT_TAIL = [((0.9, 3.5), 1.1), ((1.75, 1.55), 0.75), ((2.25, 0.46), 0.46)]       # (it hops on the smallest)


def outline(shape):
    """the bubble's outline as points (design units) - for grounding a pose on whatever part of it is lowest"""
    if shape == 'speech': return _ellipse(SPEECH['c'], SPEECH['rx'] + OW / 2, SPEECH['ry'] + OW / 2, 48)
    if shape == 'puff': return _ellipse(PUFF['c'], PUFF['rx'] + OW / 2, PUFF['ry'] + OW / 2, 48)
    if shape == 'shout': return SHOUT_POLY
    return [(x + (r + OW / 2) * math.cos(a * math.pi / 8), y + (r + OW / 2) * math.sin(a * math.pi / 8)) for (x, y), r in CLOUD for a in range(16)]


def _poly(shape):
    if shape == 'speech': return _ellipse(SPEECH['c'], SPEECH['rx'], SPEECH['ry'], 360)
    if shape == 'puff': return _ellipse(PUFF['c'], PUFF['rx'], PUFF['ry'], 360)
    return SHOUT_POLY


def _hit(pts, poly):
    """walk a polyline (from the tail's tip, up) to where it first crosses the bubble's outline -> the cut polyline"""
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        best = None
        for i in range(len(poly)):
            c, d = poly[i], poly[(i + 1) % len(poly)]
            r = (b[0] - a[0], b[1] - a[1]); s = (d[0] - c[0], d[1] - c[1])
            den = r[0] * s[1] - r[1] * s[0]
            if abs(den) < 1e-12: continue
            t = ((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0]) / den
            u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
            if 0 <= t <= 1 and 0 <= u <= 1 and (best is None or t < best): best = t
        if best is not None:
            out.append((a[0] + (b[0] - a[0]) * best, a[1] + (b[1] - a[1]) * best)); return out
        out.append(b)
    return out


# the tails: each side a line from the tip up into the bubble (cut where it meets the outline)
# (a comic tail: a wedge, wide where it leaves the bubble, its point off to its right - one side nearly straight, one curved)
_WEDGE = ((2.2, 0.3), [(2.9, 2.2), (3.4, 4.4), (3.5, 8.0)], [(1.4, 2.1), (0.2, 4.2), (-1.6, 8.0)])
TAILS = {'speech': _WEDGE, 'puff': _WEDGE,
         'shout': ((1.1, 0.3), [(2.9, 2.6), (1.8, 3.1), (3.1, 5.6), (3.1, 8.0)], [(-0.2, 3.3), (0.8, 3.5), (-1.4, 6.0), (-1.6, 8.0)])}


def tail_sides(shape):
    tip, r, l = TAILS[shape]
    return _hit([tip] + r, _poly(shape)), _hit([tip] + l, _poly(shape))


def tail_tip(shape):
    if shape == 'thought':
        (x, y), r = THOUGHT_TAIL[-1]; return (x, y - r - OW / 2)
    return TAILS[shape][0]


# ---------------------------------------------------------------------------------------------------- textures
def _down(rgb, a, n):
    """SS x over -> n: colour and coverage averaged apart (a box filter - no ringing at the edges), the alpha kept hard. Colour
    is everywhere (paper under the transparent part too), so a cut edge never darkens or lightens"""
    c = np.asarray(Image.fromarray(np.asarray(rgb, np.uint8), 'RGB').resize((n, n), Image.BOX))
    m = np.asarray(Image.fromarray(np.asarray(a, np.uint8), 'L').resize((n, n), Image.BOX))
    return Image.fromarray(np.dstack([c, np.where(m >= 128, 255, 0).astype(np.uint8)]), 'RGBA')


class _Page:
    """a texture square over design space (c, half side h): its own design-to-pixel map (drawn SS x over). The texture is drawn
    as you see the character from the front - its right (+x) on your left"""
    def __init__(self, c, h, n, ss=SS):
        self.c, self.h, self.n, self.ss = c, h, n, ss; self.S = n * ss
        self.fill = Image.new('L', (self.S, self.S), 0); self.ink = Image.new('L', (self.S, self.S), 0)
        self.shine = Image.new('L', (self.S, self.S), 0)
        self.f, self.i, self.s = ImageDraw.Draw(self.fill), ImageDraw.Draw(self.ink), ImageDraw.Draw(self.shine)

    def p(self, x, y):
        k = self.S / (2 * self.h)
        return ((self.c[0] + self.h - x) * k, (self.c[1] + self.h - y) * k)

    def P(self, pts): return [self.p(x, y) for x, y in pts]
    def w(self, d): return max(1, round(d * self.S / (2 * self.h)))

    def circle(self, dr, x, y, r, v=255):
        (cx, cy), k = self.p(x, y), self.S / (2 * self.h)
        dr.ellipse((cx - r * k, cy - r * k, cx + r * k, cy + r * k), fill=v)

    def stroke(self, pts, d, v=255, end_cap=True):
        self.i.line(self.P(pts), fill=v, width=self.w(d), joint='curve')
        for x, y in (pts[0], pts[-1]) if end_cap else (pts[0],): self.circle(self.i, x, y, d / 2, v)

    def image(self):
        """shaded paper where it's filled, ink over it -> the texture (brought down smooth, its alpha kept hard)"""
        S, k = self.S, 2 * self.h / self.S
        xs = self.c[0] + self.h - (np.arange(S) + 0.5) * k; ys = self.c[1] + self.h - (np.arange(S) + 0.5) * k
        X, Y = np.meshgrid(xs, ys)
        t = np.clip(np.hypot(X - 3.6, Y - 15.4) / 15.0, 0, 1) ** 1.6                   # (lit from its upper right - our upper left)
        v = 253 - t * 38
        f = np.asarray(self.fill) > 127; i = np.asarray(self.ink) > 127
        rgb = np.stack([v, v, v], -1); rgb[(np.asarray(self.shine) > 127) & f] = 255; rgb[i] = hexc(INK)[:3]
        a = (f | i).astype(np.uint8) * 255
        return _down(rgb, a, self.n)


def _bubble(shape):
    g = _Page(BODY_C, BODY_H, BODY_N)
    if shape == 'thought':
        for (x, y), r in CLOUD: g.circle(g.i, x, y, r + OW / 2)
        for (x, y), r in CLOUD: g.circle(g.i, x, y, r - OW / 2, 0); g.circle(g.f, x, y, r - OW / 2)
        g.i.polygon(g.P(CLOUD_CORE), fill=0); g.f.polygon(g.P(CLOUD_CORE), fill=255)
    else:
        pts = _poly(shape)
        g.f.polygon(g.P(pts), fill=255)
        g.i.line(g.P(pts + pts[:2]), fill=255, width=g.w(OW), joint='curve')
    if shape == 'puff':                                                             # (blown up tight: a shine on it, like a balloon)
        c, rx, ry = PUFF['c'], PUFF['rx'] * 0.74, PUFF['ry'] * 0.74
        arc = [(c[0] + rx * math.cos(a), c[1] + ry * math.sin(a)) for a in np.linspace(math.radians(30), math.radians(70), 12)]
        g.s.line(g.P(arc), fill=255, width=g.w(0.75), joint='curve')
        for x, y in (arc[0], arc[-1]): g.circle(g.s, x, y, 0.375)
        g.circle(g.s, c[0] + rx * math.cos(math.radians(14)), c[1] + ry * math.sin(math.radians(14)), 0.42)
    return g.image()


def _tail(shape):
    g = _Page(TAIL_C, TAIL_H, TAIL_N)
    if shape == 'thought':
        for (x, y), r in THOUGHT_TAIL:
            g.circle(g.i, x, y, r + OW / 2); g.circle(g.i, x, y, r - OW / 2, 0); g.circle(g.f, x, y, r - OW / 2)
        return g.image()
    rs, ls = tail_sides(shape)
    R, L = rs[-1], ls[-1]; top = max(R[1], L[1]) + 1.1
    g.f.polygon(g.P(rs + [(R[0] * 0.8, top), (L[0] * 0.8, top)] + ls[::-1]), fill=255)
    g.stroke(rs, OW, end_cap=False); g.stroke(ls, OW, end_cap=False)                 # (no round end where it meets the bubble)
    return g.image()


# ---- the face (a decal over the bubble: transparent but for the features)
def _face(kind=None):
    S = FACE_N * SS
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); k = SS
    ink, white, red, pink = hexc(INK), (255, 255, 255, 255), hexc('#e0485a'), hexc('#f59aa8')
    E = lambda b: tuple(v * k for v in b)

    def line(pts, w=6):
        d.line([(x * k, y * k) for x, y in pts], fill=ink, width=w * k, joint='curve')
        for x, y in (pts[0], pts[-1]): d.ellipse(E((x - w / 2, y - w / 2, x + w / 2, y + w / 2)), fill=ink)

    def arc(box, a0, a1, w=6):
        d.arc(E(box), a0, a1, fill=ink, width=w * k)

    def eye(cx, cy, rx=11, ry=15, lid=None, look=(0, 0)):
        """a big black eye with a white glint; lid: how far down the top is cut off (0..1)"""
        d.ellipse(E((cx - rx, cy - ry, cx + rx, cy + ry)), fill=ink)
        gx, gy = cx - rx * 0.35 + look[0], cy - ry * 0.4 + look[1]
        d.ellipse(E((gx - rx * 0.32, gy - ry * 0.26, gx + rx * 0.32, gy + ry * 0.26)), fill=white)
        if lid:
            cut = cy - ry + 2 * ry * lid
            d.rectangle(E((cx - rx - 1, cy - ry - 2, cx + rx + 1, cut)), fill=(0, 0, 0, 0))
            d.line(E((cx - rx - 2, cut, cx + rx + 2, cut)), fill=ink, width=5 * k)

    L, R = (38, 50), (90, 50)                          # (its right eye on our left)
    # ---- eyes
    if kind == 'blink':
        arc((L[0] - 11, L[1] - 6, L[0] + 11, L[1] + 10), 15, 165); arc((R[0] - 11, R[1] - 6, R[0] + 11, R[1] + 10), 15, 165)
    elif kind == 'happy':
        arc((L[0] - 11, L[1] - 6, L[0] + 11, L[1] + 14), 195, 345, 7); arc((R[0] - 11, R[1] - 6, R[0] + 11, R[1] + 14), 195, 345, 7)
    elif kind == 'surprised':
        for cx, cy in (L, R):
            d.ellipse(E((cx - 11, cy - 16, cx + 11, cy + 16)), fill=white, outline=ink, width=5 * k)
            d.ellipse(E((cx - 4, cy - 5, cx + 4, cy + 5)), fill=ink)
    elif kind in ('fierce', 'shout'):
        eye(*L, lid=0.38, look=(3, 4)); eye(*R, lid=0.38, look=(3, 4))
    elif kind == 'hurt':
        line([(L[0] - 10, L[1] - 9), (L[0] + 8, L[1]), (L[0] - 10, L[1] + 9)]); line([(R[0] + 10, R[1] - 9), (R[0] - 8, R[1]), (R[0] + 10, R[1] + 9)])
    elif kind == 'smug':
        eye(*L, lid=0.5); eye(*R, lid=0.42)
    elif kind == 'puzzled':
        eye(L[0], L[1] + 2, 8, 11); eye(R[0], R[1] - 1, 10, 14)
    elif kind == 'puff':
        line([(L[0] - 10, L[1] - 7), (L[0] + 8, L[1]), (L[0] - 10, L[1] + 7)], 5); line([(R[0] + 10, R[1] - 7), (R[0] - 8, R[1]), (R[0] + 10, R[1] + 7)], 5)
    elif kind == 'dizzy':
        for cx, cy in (L, R):                                                       # (spirals)
            pts = [(cx + (1 + 1.25 * a) * math.cos(a), cy + (1 + 1.25 * a) * math.sin(a)) for a in np.linspace(0, 3.4 * math.pi, 40)]
            line(pts, 4)
    else:
        eye(*L); eye(*R)
    # ---- brows (thick, and they do most of the acting)
    if kind in ('fierce', 'shout'):
        line([(26, 26), (50, 36)], 8); line([(102, 26), (78, 36)], 8)
    elif kind in ('surprised',):
        arc((26, 16, 54, 34), 200, 340, 7); arc((74, 16, 102, 34), 200, 340, 7)
    elif kind == 'hurt':
        line([(28, 34), (50, 28)], 7); line([(100, 34), (78, 28)], 7)
    elif kind == 'smug':
        arc((26, 18, 54, 36), 200, 340, 7); line([(76, 32), (102, 32)], 7)               # (one brow arched high, one flat)
    elif kind == 'puzzled':
        line([(28, 34), (52, 32)], 7); arc((74, 12, 104, 32), 200, 340, 7)
    elif kind == 'puff':
        line([(28, 28), (50, 34)], 7); line([(100, 28), (78, 34)], 7)
    elif kind in ('blink', 'dizzy'):
        arc((28, 24, 54, 38), 205, 335, 6); arc((74, 24, 100, 38), 205, 335, 6)
    else:                                                                           # (default and happy: high and theatrical - its right one a touch higher)
        arc((26, 18, 54, 34), 200, 340, 7); arc((74, 22, 102, 38), 200, 340, 7)
    # ---- mouth
    if kind in (None, 'happy'):
        h = 30 if kind == 'happy' else 24
        d.chord(E((36, 72, 92, 72 + h)), 0, 180, fill=ink)
        d.chord(E((50, 72 + h * 0.45, 78, 72 + h - 3)), 0, 180, fill=red)
    elif kind == 'surprised':
        d.ellipse(E((56, 74, 72, 94)), fill=ink)
    elif kind == 'blink':
        arc((50, 72, 78, 86), 20, 160)
    elif kind == 'fierce':
        d.rounded_rectangle(E((42, 76, 86, 92)), radius=5 * k, fill=white, outline=ink, width=5 * k)
        for x in (53, 64, 75): d.line(E((x, 77, x, 91)), fill=ink, width=3 * k)
        d.line(E((43, 84, 85, 84)), fill=ink, width=3 * k)
    elif kind == 'shout':
        d.ellipse(E((38, 66, 90, 110)), fill=ink)
        d.chord(E((50, 88, 78, 108)), 180, 360, fill=red)
        d.rectangle(E((48, 68, 80, 74)), fill=white)                                 # (teeth along the top)
    elif kind == 'hurt':
        line([(44, 86), (52, 80), (60, 86), (68, 80), (76, 86), (84, 80)], 5)
    elif kind == 'smug':
        line([(48, 84), (64, 86), (80, 80), (86, 74)], 6)
    elif kind == 'puzzled':
        line([(50, 84), (58, 80), (66, 84), (74, 82)], 5)
    elif kind == 'puff':
        d.ellipse(E((58, 80, 70, 90)), fill=None, outline=ink, width=5 * k)
        for cx in (26, 102): d.ellipse(E((cx - 9, 66, cx + 9, 78)), fill=pink)         # (cheeks puffed, flushed)
    elif kind == 'dizzy':
        line([(46, 84), (56, 80), (66, 86), (76, 80), (84, 84)], 5)
    im = im.resize((FACE_N, FACE_N), Image.BOX); a = np.asarray(im).copy(); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    return Image.fromarray(a, 'RGBA')


# ---- the words: hand-lettered (strokes on a cell 1 wide, 1.4 tall, y down) - no fonts, so the build never depends on one
_O = [(0.5 + 0.5 * math.cos(a), 0.7 + 0.7 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 28)]
GLYPH = {
    'B': (0.92, [[(0, 0), (0, 1.4)], [(0, 0.02), (0.52, 0.02), (0.78, 0.14), (0.8, 0.46), (0.55, 0.66), (0, 0.66)],
                 [(0, 0.66), (0.6, 0.66), (0.9, 0.86), (0.9, 1.2), (0.6, 1.38), (0, 1.38)]], []),
    'A': (1.05, [[(0, 1.4), (0.52, 0), (1.04, 1.4)], [(0.22, 0.9), (0.82, 0.9)]], []),
    'M': (1.15, [[(0, 1.4), (0.05, 0), (0.57, 0.8), (1.1, 0), (1.15, 1.4)]], []),
    'P': (0.88, [[(0, 1.4), (0, 0.02), (0.55, 0.02), (0.86, 0.2), (0.86, 0.56), (0.55, 0.76), (0, 0.76)]], []),
    'O': (1.0, [_O], []),
    'W': (1.35, [[(0, 0), (0.3, 1.4), (0.67, 0.5), (1.05, 1.4), (1.35, 0)]], []),
    'Z': (0.95, [[(0.02, 0.02), (0.93, 0.02), (0.02, 1.38), (0.95, 1.38)]], []),
    'K': (0.95, [[(0, 0), (0, 1.4)], [(0.92, 0), (0.05, 0.82)], [(0.32, 0.56), (0.95, 1.4)]], []),
    'R': (0.92, [[(0, 1.4), (0, 0.02), (0.55, 0.02), (0.86, 0.2), (0.86, 0.56), (0.55, 0.76), (0, 0.76)], [(0.4, 0.76), (0.92, 1.4)]], []),
    '!': (0.3, [[(0.15, 0), (0.15, 0.92)]], [(0.15, 1.3)]),
    '?': (0.85, [[(0.04, 0.32), (0.18, 0.08), (0.45, 0), (0.74, 0.08), (0.84, 0.32), (0.72, 0.56), (0.45, 0.72), (0.43, 0.96)]], [(0.43, 1.3)]),
    '.': (0.75, [], [(0.37, 1.0)]),
}
# per word: (text, burst colours (outer, inner) or None, letter fill (top, bottom), spikes, layout)
WORD_STYLE = {
    'bam': ('BAM!', ('#e8322a', '#ff8f1f'), ('#fff15a', '#ffb21c'), 15),
    'pow': ('POW!', ('#ffd21f', '#fff6b0'), ('#ff4a2e', '#c4141a'), 13),
    'zap': ('ZAP!', ('#2aa8ff', '#cdf2ff'), ('#fff15a', '#ff9e1c'), 21),
    'krak': ('KRAK!', ('#ff7414', '#ffd23a'), ('#fff7c8', '#ffd21f'), 17),
    'zzz': ('ZZZ', None, ('#ffffff', '#9fd0ff'), 0),
    'q': ('?', None, ('#ffffff', '#d8ecff'), 0),
    'bang': ('!', None, ('#ff5a3a', '#d01818'), 0),
    'dots': ('...', None, ('#3a3a44', '#161616'), 0),
}


def _grad(size, top, bot):
    a, b = np.array(hexc(top)[:3], float), np.array(hexc(bot)[:3], float)
    t = np.linspace(0, 1, size)[:, None, None]
    return Image.fromarray(np.broadcast_to(a + (b - a) * t, (size, size, 3)).astype(np.uint8), 'RGB')


def _word(key):
    text, burst, (ft, fb), spikes = WORD_STYLE[key]
    S = WORD_N * 2; im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = hexc(INK); rnd = random.Random('sbb-' + key)
    if burst:                                                                       # (the starburst it bursts out of)
        c = (S / 2, S / 2)
        def star(rx, ry, o, i_):
            pts = []
            for j in range(2 * spikes):
                a = math.pi * j / spikes + rnd.uniform(-0.07, 0.07)
                f = o * rnd.uniform(0.84, 1.0) if j % 2 == 0 else i_ * rnd.uniform(0.9, 1.08)
                pts.append((c[0] + rx * f * math.cos(a), c[1] + ry * f * math.sin(a)))
            return pts
        outer = star(S * 0.49, S * 0.42, 1.0, 0.66)
        d.polygon(outer, fill=hexc(burst[0])); d.line(outer + outer[:2], fill=ink, width=10, joint='curve')
        inner = star(S * 0.36, S * 0.3, 1.0, 0.72)
        d.polygon(inner, fill=hexc(burst[1]))
        if key == 'krak':                                                           # (cracks running out of it)
            for a0 in (0.5, 2.1, 3.7, 5.2):
                pts = [c]; r = 0
                for _ in range(4):
                    r += S * 0.1; a = a0 + rnd.uniform(-0.25, 0.25); pts.append((c[0] + r * math.cos(a), c[1] + r * 0.85 * math.sin(a)))
                d.line(pts, fill=ink, width=7, joint='curve')
    # ---- the letters: laid out along a slight rising wave, each tipped a little - a heavy shadow, a black outline, then the fill
    gl = [GLYPH[ch] for ch in text]
    gap = 0.16; tw = sum(g[0] for g in gl) + gap * (len(gl) - 1)
    if key == 'zzz':
        H = S * 0.3
    elif key in ('q', 'bang'):
        H = S * 0.62
    elif key == 'dots':
        H = S * 0.36
    else:
        H = min(S * 0.4, S * 0.82 / tw * 1.4)                                    # (the word fills ~82% of the width)
    unit = H / 1.4; sw = unit * (0.3 if key not in ('q', 'bang') else 0.26); ow = unit * 0.13
    strokes, dots = [], []
    x = S / 2 - tw * unit / 2
    for n, (w, ss, ds) in enumerate(gl):
        ang = math.radians((-7, 6, -4, 8, -5)[n % 5]) if key not in ('q', 'bang', 'dots') else 0.0
        sc = 1.0 + (0.14 if n == 0 and key not in ('zzz', 'dots') else 0.0)
        if key == 'zzz': sc = 0.62 + 0.3 * n
        yb = S / 2 - H / 2 - (n - (len(gl) - 1) / 2) * unit * 0.16
        cx, cy = x + w * unit / 2, yb + H / 2
        if key == 'zzz':                                                            # (three Z's climbing up and away, each bigger)
            cx, cy = S * (0.24 + 0.25 * n), S * (0.72 - 0.22 * n); x, yb = cx - w * unit / 2, cy - H / 2
        def T(p, w=w, cx=cx, cy=cy, ang=ang, sc=sc, yb=yb, x0=x):
            px, py = x0 + p[0] * unit, yb + p[1] * unit
            dx, dy = (px - cx) * sc, (py - cy) * sc
            return (cx + dx * math.cos(ang) - dy * math.sin(ang), cy + dx * math.sin(ang) + dy * math.cos(ang))
        strokes += [[T(p) for p in s] for s in ss]; dots += [(T(p), sc) for p in ds]
        x += (w + gap) * unit * (sc if key == 'zzz' else 1.0)
    if key == 'zzz':                                                                # (re-centre the climbing Z's)
        xs = [p[0] for s in strokes for p in s]; ys = [p[1] for s in strokes for p in s]
        mx, my = S / 2 - (min(xs) + max(xs)) / 2, S / 2 - (min(ys) + max(ys)) / 2
        strokes = [[(p[0] + mx, p[1] + my) for p in s] for s in strokes]

    def draw(dr, off, wid, col, dot_r):
        for s in strokes:
            q = [(p[0] + off, p[1] + off) for p in s]
            dr.line(q, fill=col, width=round(wid), joint='curve')
            for p in (q[0], q[-1]): dr.ellipse((p[0] - wid / 2, p[1] - wid / 2, p[0] + wid / 2, p[1] + wid / 2), fill=col)
        for (p, sc) in dots:
            r = dot_r * sc; dr.ellipse((p[0] + off - r, p[1] + off - r, p[0] + off + r, p[1] + off + r), fill=col)
    halo = key in ('q', 'bang', 'dots', 'zzz')                                       # (the loose symbols get a white halo - they float on anything)
    if halo: draw(d, 0, sw + 4 * ow, (255, 255, 255, 255), sw * 0.55 + 2 * ow)
    draw(d, ow * 0.9, sw + 2 * ow, ink, sw * 0.55 + ow)                              # (the drop shadow, down and to the right)
    draw(d, 0, sw + 2 * ow, ink, sw * 0.55 + ow)
    m = Image.new('L', (S, S), 0); draw(ImageDraw.Draw(m), 0, sw, 255, sw * 0.55)
    ys = [p[1] for s in strokes for p in s] + [p[1] for p, _ in dots]
    g = _grad(S, ft, fb)
    if ys:                                                                          # (the fill's gradient runs over the letters' own height)
        y0, y1 = int(max(0, min(ys) - sw)), int(min(S, max(ys) + sw))
        g = _grad(max(2, y1 - y0), ft, fb).resize((S, max(2, y1 - y0)))
        full = Image.new('RGB', (S, S), hexc(fb)[:3]); full.paste(Image.new('RGB', (S, y0), hexc(ft)[:3]), (0, 0)); full.paste(g, (0, y0)); g = full
    im.paste(g, (0, 0), m)
    im = im.resize((WORD_N, WORD_N), Image.BOX); a = np.asarray(im).copy(); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    return Image.fromarray(a, 'RGBA')


def _solid(c):
    return Image.new('RGBA', (16, 16), hexc(c)[:3] + (255,))


def textures():
    T = {f'{PREFIX}ink': _solid(INK), f'{PREFIX}face': _face()}
    for s in SHAPES:
        T[f'{PREFIX}bub_{s}'] = _bubble(s)
        T[f'{PREFIX}tail_{s}'] = _tail(s)
    for k in FACES:
        T[f'{PREFIX}face_{k}'] = _face(k)
    for w in WORDS:
        T[f'{PREFIX}w_{w}'] = _word(w)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _sheet(c, h, z, tex, pv, both=True, back_reads=False, zc=0.0):
    """a picture on the page: a front plane at z - and, a hair behind the bubble, its back (mirrored like the back of the paper -
    or, back_reads, reading right way round from behind too: the words)"""
    (x, y) = c
    e = [el((x - h, y - h, zc - z), (x + h, y + h, zc - z), tex, pv, faces=('north',), uv={'north': [0, 0, 16, 16]})]
    if both:
        e.append(el((x - h, y - h, zc + z), (x + h, y + h, zc + z), tex, pv, faces=('south',), uv={'south': [0, 0, 16, 16] if back_reads else [16, 0, 0, 16]}))
    return e


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    for s in SHAPES:
        part(f'{PREFIX}body_{s}', _sheet(BODY_C, BODY_H, LD / 2, f'{PREFIX}bub_{s}', PIVOT['body']))
        part(f'{PREFIX}tail_{s}', _sheet(TAIL_C, TAIL_H, LD / 2 + 0.04, f'{PREFIX}tail_{s}', PIVOT['tail']))
    part(f'{PREFIX}face', _sheet(FACE_C, FACE_H, LD / 2 + 0.08, f'{PREFIX}face', PIVOT['face'], both=False))
    for k in FACES:
        part(f'{PREFIX}face_x{k}', _sheet(FACE_C, FACE_H, LD / 2 + 0.08, f'{PREFIX}face_{k}', PIVOT['face'], both=False))
    wp = PIVOT['word']
    for w in WORDS:
        part(f'{PREFIX}word_{w}', _sheet((wp[0], wp[1]), WORD_H, 0.02, f'{PREFIX}w_{w}', wp, back_reads=True, zc=wp[2]))
    M[f'{PREFIX}body'] = M[f'{PREFIX}body_speech']; M[f'{PREFIX}tail'] = M[f'{PREFIX}tail_speech']; M[f'{PREFIX}word'] = M[f'{PREFIX}word_bam']
    return M


# ---------------------------------------------------------------------------------------------------- poses
def P(**kw):
    return kw


def lean(fwd=0.0, side=0.0, turn=0.0):
    """the bubble's lean: fwd tips its top toward where it faces, side tips its top over to its right (our left), turn turns it"""
    return qs(('y', turn), ('x', fwd), ('z', side))


def swing(a):
    """the tail swung (on the page): its tip kicked back toward its left (our right) by a degrees - never past 6: the tail's
    lines meet the bubble's outline at its joint, and a bigger swing pokes their ends into the white"""
    return qs(('z', -max(-6.0, min(6.0, a))))


def hop(k, h, fwd, wob, face=None):
    """a hop cycle on its tail: 0 lands, 1 up, 2 lands, 3 up (the tail trails behind it in the air)"""
    air = k % 2 == 1
    side = wob * (1 if k == 1 else -1 if k == 3 else 0)
    p = P(body=lean(fwd + (4 if air else -2), side), tail=swing(10 if air else -4), _lift=h if air else 0.0)
    if face: p['_face'] = face
    return p


SHOW = dict(_word='bam', _o_word=(0, 0, 0))

POSES = {
    # standing on its tail, chest out - pleased with itself
    'idle_a': P(body=lean(-3, 3)),
    # the show-off: tips over to one side, a sly look - one brow up
    'idle_b': P(_face='smug', body=lean(0, -8, 12), _o_face=(-0.7, 0.2, 0), tail=swing(-6)),
    # lost in thought: a thought bubble now, a ? over its head
    'idle_c': P(_shape='thought', _face='puzzled', _word='q', body=lean(0, 5), _o_face=(0.6, 0.5, 0), _o_word=(-3.2, 0.4, 0), word=qs(('z', -12))),
    # a slow blink, sagging a touch
    'idle_d': P(_face='blink', body=lean(2, -2)),
    **{f'walk_{k}': hop(k, 1.6, 6, 5) for k in range(4)},
    **{f'run_{k}': hop(k, 3.4, 16, 8, 'fierce') for k in range(4)},
    'jump': P(_face='surprised', _word='bang', body=lean(-6, 0), tail=swing(14), _lift=5.0, _o_word=(-4.5, -1.0, 0), word=qs(('z', -14))),
    # SHOUT (its quick attack): it rears back, fierce - then lunges, and the word bursts out of it, straight at the foe
    'shout_up': P(_face='fierce', body=lean(-14, 4, -10), tail=swing(-8)),
    'shout': P(_shape='shout', _face='shout', _word='bam', body=lean(12, -3, 6), tail=swing(8), _o_word=(0, -2.4, -7.0), word=qs(('x', 8), ('z', 8))),
    'shout_b': P(_shape='shout', _face='shout', _word='pow', body=lean(10, 5, -6), tail=swing(6), _o_word=(1.0, -2.0, -7.5), word=qs(('x', 8), ('z', -10))),
    # THE BIG ONE (charged): it breathes in - swelling, cheeks puffed - and then BLASTS it out, recoiling on its tail
    'puff_up': P(_shape='puff', _face='puff', body=lean(-6, 0), tail=swing(-3)),
    'puff_b': P(_shape='puff', _face='puff', body=lean(-12, -3), tail=swing(-6), _lift=0.0),
    'blast': P(_shape='shout', _face='shout', _word='krak', body=lean(-16, 0), tail=swing(-12), _o_word=(0, -1.0, -8.5), word=qs(('x', 4))),
    'blast_b': P(_shape='shout', _face='fierce', _word='zap', body=lean(-8, 6, 8), tail=swing(-6), _o_word=(-1.5, -0.6, -10.0), word=qs(('z', 12))),
    # thinking: a thought bubble, the dots trailing out of it, its eyes off to one side
    'think': P(_shape='thought', _face='puzzled', _word='dots', body=lean(0, -4), _o_face=(-0.8, 0.6, 0), _o_word=(0, -0.4, 0)),
    # asleep: sat down on its tail, tipped over a little, ZZZ
    'sleep': P(_face='blink', _word='zzz', _tail='none', body=lean(4, -14), _o_face=(0, -0.4, 0), _o_word=(-3.4, -1.2, 0), word=qs(('z', 10))),
    'happy': P(_face='happy', body=lean(-6, 0), tail=swing(10), _lift=2.2),
    # (alarm, for whatever needs it: ! and wide eyes)
    'alarm': P(_face='surprised', _word='bang', body=lean(-8, 0), _o_word=(-3.0, -0.6, 0), word=qs(('z', -10))),
    # awkward: ... and a sideways look
    'awkward': P(_face='puzzled', _word='dots', body=lean(0, 4, -10), _o_face=(0.9, -0.2, 0), _o_word=(0, -0.6, 0)),
    # sitting: sat down on its tail, settled - and, seated idle, rocking back to look up at the sky
    'sit_a': P(_face='happy', _tail='none', body=lean(-4, 0)),
    'sit_b': P(_tail='none', _face='blink', body=lean(-10, 8), _o_face=(0.4, 0.6, 0)),
    'hurt': P(_face='hurt', body=lean(-14, -8), tail=swing(-10)),
    # tired: keeled over on its side on the ground, dizzy
    'tired': P(_face='dizzy', body=lean(0, 80), tail=swing(6)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                       # (a paper boat: afloat, tipped forward, paddling with its tail)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='happy' if _i % 4 else None, _off=(0, -5.0 + 0.4 * math.sin(2 * _p), 0),
                            body=lean(34 + 4 * math.sin(_p), 8 * math.sin(_p)), tail=swing(14 * math.sin(2 * _p)))
    if POSES[f'swim_{_i}']['_face'] is None: POSES[f'swim_{_i}'].pop('_face')


# every pose stands on its tail's tip (or, sat down, on its bubble) - just on the floor; hops lifted by _lift
_ME = sys.modules[__name__]


def lowest(pose):
    pose = dict(pose)
    shape = pose.get('_shape', 'speech'); refs = []
    for x, y in outline(shape): refs += [('body', (x, y, z)) for z in (-LD / 2, LD / 2)]
    if pose.get('_tail') != 'none':
        t = pose.get('_tail') or shape; x, y = tail_tip(t)
        refs += [('tail', (x + dx, y, z)) for dx in (-0.25, 0.25) for z in (-LD / 2, LD / 2)]
        if t == 'thought':
            refs += [('tail', (x + (r + OW / 2) * math.cos(a), y0 + (r + OW / 2) * math.sin(a), 0.0)) for (x, y0), r in THOUGHT_TAIL for a in np.linspace(0, 2 * math.pi, 16)]
    return min(point(_ME, pose, p, v)[1] * 16 for p, v in refs)


def _ground(pose):
    pose = dict(pose); lift = pose.pop('_lift', 0.0); pose.pop('_off', None)
    pose['_off'] = (0.0, round(lift - lowest(pose) + 0.08, 3), 0.0)
    return pose


for _k in list(POSES):
    if not _k.startswith('swim_'):
        POSES[_k] = _ground(POSES[_k])
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'idle_d', 'walk_0', 'walk_1', 'run_1', 'jump', 'shout_up', 'shout', 'shout_b', 'puff_up', 'puff_b', 'blast', 'blast_b',
         'think', 'sleep', 'alarm', 'awkward', 'happy', 'sit_a', 'sit_b', 'hurt', 'tired', 'swim_2']
