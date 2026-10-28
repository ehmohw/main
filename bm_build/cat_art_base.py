"""2.95e: the house cats' shared rig (Nia, Henry) - from the owner's photos. Not the vanilla cat, but built on its proportions
(a long low body, a small round head with a short muzzle, thin legs, a long tail), with more character: tall pointed ears with
pink insides, a real little muzzle and chin, big painted eyes with lids and a glint.

A rigkit rig: body, head (a face per expression; the ears and muzzle on it), four legs and the tail. Design units: feet at
y=0, facing -z, the cat's right is +x. Textures 64 px over 16 units (4 px a unit, as the other followers'), painted in
2-px cells so the fur keeps a chunky, vanilla-adjacent look.

make(prefix, look, build) returns the module-level names a rigkit art module has (PREFIX, PIVOT, PARENT, PARTS, FACES, POSES,
DRAFT, HIDDEN, model_name, models, textures, RIG_SCALE): `look` paints the textures, `build` sizes the frame."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, chain

FACES = ('blink', 'happy', 'alert')
FRONT = (0.0, 0.0, -1.0)


# ---------------------------------------------------------------------------------------------------- painting helpers
def field(seed, n=6, size=64):
    """smooth value noise in 0..1 (an n x n lattice, bilinear) - for coat patches"""
    rnd = random.Random(seed); g = [[rnd.random() for _ in range(n + 1)] for _ in range(n + 1)]
    out = [[0.0] * size for _ in range(size)]
    for y in range(size):
        for x in range(size):
            fx, fy = x / size * n, y / size * n; ix, iy = int(fx), int(fy); tx, ty = fx - ix, fy - iy
            tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
            a = g[iy][ix] * (1 - tx) + g[iy][ix + 1] * tx; b = g[iy + 1][ix] * (1 - tx) + g[iy + 1][ix + 1] * tx
            out[y][x] = a * (1 - ty) + b * ty
    return out


def cells(fn, seed, cell=2):
    """a 64 px texture painted cell by cell: fn(cx, cy, rnd) -> colour (cx, cy in cells)"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im); rnd = random.Random(seed); n = 64 // cell
    for cy in range(n):
        for cx in range(n):
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(fn(cx, cy, rnd)))
    return im


def solid(col, seed, var=(), p=0.0, cell=2):
    """a plain coat: one colour, flecked with `var` colours (chance p a cell)"""
    return cells(lambda x, y, r: r.choice(var) if var and r.random() < p else col, seed, cell)


def eyes(im, kind, iris, rim, pupil='#0c0a08', lid='#2a2420', glint='#ffffff', cols=(1, 14), row=4, w=7, h=5):
    """two eyes on a face texture (pixels): almond, dark rim, iris shading lighter at the bottom, an oval pupil, a glint"""
    px = im.load()
    P = lambda x, y, c: px.__setitem__((x, y), hexc(c)) if 0 <= x < 64 and 0 <= y < 64 else None
    for x0 in cols:
        if kind == 'blink':
            for x in range(x0, x0 + w): P(x, row + h // 2, lid)
            continue
        if kind == 'happy':                                                     # (content: closed, curved up)
            for i, x in enumerate(range(x0, x0 + w)): P(x, row + h // 2 - (1 if 0 < i < w - 1 else 0), lid)
            continue
        top = row - (1 if kind == 'alert' else 0)
        for y in range(top, row + h):
            for x in range(x0, x0 + w):
                corner = (x in (x0, x0 + w - 1)) and (y in (top, row + h - 1))
                if corner: continue
                edge = x in (x0, x0 + w - 1) or y in (top, row + h - 1)
                P(x, y, rim if edge else (iris[1] if y >= row + h // 2 else iris[0]))
        mid = x0 + w // 2
        for y in range(top + 1, row + h - 1):                                    # the pupil (rounder when alert)
            P(mid, y, pupil)
            if kind == 'alert': P(mid - 1, y, pupil)
        P(mid - 1 if kind != 'alert' else mid - 2, top + 1, glint)
        for x in range(x0 + 1, x0 + w - 1): P(x, top - 1, lid)                   # the upper lid line


# ---------------------------------------------------------------------------------------------------- the rig
def make(prefix, look, build):
    """look(prefix) -> {texture name: image} with the keys below; build: dict(stock=1.0 (width), long=1.0, tall=1.0, scale=..)"""
    k, L_, hgt = build.get('stock', 1.0), build.get('long', 1.0), build.get('tall', 1.0)      # (head_tex: the head's own coat, if not 'fur')
    bw = 2.2 * k                                                                 # (half the body's width)
    by0, by1 = 3.8 * hgt, 8.4 * hgt
    zf, zb = -6.0 * L_, 6.4 * L_
    PIVOT = {'body': (0, 6.1 * hgt, 0), 'head': (0, 8.9 * hgt, zf), 'legfr': (1.3 * k, 5.0 * hgt, zf + 1.8), 'legfl': (-1.3 * k, 5.0 * hgt, zf + 1.8),
             'legbr': (1.4 * k, 5.2 * hgt, zb - 1.6), 'legbl': (-1.4 * k, 5.2 * hgt, zb - 1.6), 'tail': (0, by1 - 0.6, zb)}
    PARENT = {'body': None, 'head': 'body', 'legfr': 'body', 'legfl': 'body', 'legbr': 'body', 'legbl': 'body', 'tail': 'body'}
    T = lambda n: f'{prefix}{n}'

    def HIDDEN(p, pose):
        return p in pose.get('_hide', ())

    def model_name(p, pose, suffix=''):
        face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
        return f'{prefix}{p}{face}{suffix}'

    def textures():
        return look(prefix)

    def models():
        M = {}

        def part(name, els):
            used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
            M[name] = ({t: f'bm:block/{t}' for t in used}, els)
        # ---- the body: long and low, the chest a little deeper, a short neck; a paler belly; the chest patch
        pv = PIVOT['body']
        body = [el((-bw, by0, zf + 2.4), (bw, by1, zb), T('fur'), pv, shift=(0.1, 0.2)),
                el((-bw - 0.2, by0 - 0.3, zf), (bw + 0.2, by1 + 0.1, zf + 2.6), T('fur'), pv, shift=(0.55, 0.4)),       # the chest, deeper
                el((-bw + 0.02, by1, zf + 2.4), (bw - 0.02, by1 + 0.02, zb), T('back'), pv, faces=('up',)),
                el((-bw + 0.3, by0 - 0.02, zf + 1.0), (bw - 0.3, by0, zb - 1.0), T('belly'), pv, faces=('down',)),
                el((-1.7 * k, by1 - 1.6, zf - 1.0), (1.7 * k, by1 + 0.9, zf + 1.2), T('fur'), pv, shift=(0.3, 0.7)),     # the neck
                el((-1.5 * k, by0 + 0.6, zf - 0.22), (1.5 * k, by1 - 0.4, zf - 0.2), T('chest'), pv, faces=('north',),
                   uv={'north': [0, 0, 3.0 * k, by1 - by0 - 1.0]}),
                el((-1.5 * k, by1 - 1.5, zf - 1.02), (1.5 * k, by1 + 0.6, zf - 1.0), T('throat'), pv, faces=('north',),
                   uv={'north': [0, 0, 3.0 * k, 2.1]})]
        part(T('body'), body)
        # ---- the head: a round skull, cheeks, the short muzzle and chin, tall pointed ears (stepped), the face painted on
        pv = PIVOT['head']; hy = PIVOT['head'][1]; hz = zf
        hw = 2.8 * (1 + (k - 1) * 0.5)

        def head(face=None):
            ft = T('face') if face is None else T(f'face_{face}')
            h = [el((-hw, hy - 0.8, hz - 4.6), (hw, hy + 3.4, hz), T(build.get('head_tex', 'fur')), pv, shift=(0.3, 0.6)),
                 el((-hw, hy - 0.8, hz - 4.62), (hw, hy + 3.4, hz - 4.6), ft, pv, faces=('north',), uv={'north': [0, 0, 2 * hw, 4.2]}),
                 el((-hw, hy + 3.4, hz - 4.6), (hw, hy + 3.42, hz), T('crown'), pv, faces=('up',), uv={'up': [0, 0, 2 * hw, 4.6]}),
                 el((-hw - 0.35, hy - 0.4, hz - 3.6), (hw + 0.35, hy + 1.4, hz - 0.8), T('cheek'), pv, faces=('east', 'west', 'down', 'south'), shift=(0.2, 0.1)),
                 el((-1.5, hy - 0.8, hz - 5.6), (1.5, hy + 0.9, hz - 4.6), T('muzzle'), pv, faces=('east', 'west', 'down', 'up'), shift=(0.4, 0.4)),
                 el((-1.5, hy - 0.8, hz - 5.62), (1.5, hy + 0.9, hz - 5.6), T('mfront'), pv, faces=('north',), uv={'north': [0, 0, 3, 1.7]}),
                 el((-1.0, hy - 1.15, hz - 5.3), (1.0, hy - 0.8, hz - 4.0), T('chin'), pv)]
            for sx in (-1, 1):                                                   # the ears: two blades meeting at the tip (an A, a clean
                x0, ap, z0 = sx * (hw - 1.2), hy + 5.6, hz - 2.6                 #  point), leaning out a little; pink inside
                for b in (-1, 1):
                    rot = ((0.0, 0.0, b * 17.0 - 11 * sx), (x0, ap, z0))
                    h.append(el((x0 - 0.5, ap - 2.9, z0 - 0.4), (x0 + 0.5, ap, z0 + 0.4), T('ear'), pv, rot=rot, shift=(0.3 + 0.2 * b, 0.2)))
                h.append(el((x0 - 0.42, ap - 2.3, z0 - 0.42), (x0 + 0.42, ap - 1.0, z0 - 0.4), T('ear_in'), pv, faces=('north',),
                            rot=((0.0, 0.0, -11.0 * sx), (x0, ap, z0))))
            return h
        part(T('head'), head())
        for fc in FACES:
            part(T(f'head_x{fc}'), head(fc))

        # ---- the legs: slim; the hind ones with a thigh; small round paws
        def leg(n, hind):
            pv = PIVOT[n]; x, y, z = pv; r = 0.75 * (1 + (k - 1) * 0.6)
            L = [el((x - r, 0.7, z - r), (x + r, y + 0.6, z + r), T('leg'), pv, shift=(0.3 if hind else 0.7, 0.2)),
                 el((x - r - 0.1, 0.0, z - r - 0.5), (x + r + 0.1, 0.8, z + r), T('paw'), pv)]
            if hind: L.insert(0, el((x - r - 0.25, y - 3.2, z - r - 0.6), (x + r + 0.25, y + 1.0, z + r + 0.7), T('fur'), pv, shift=(0.8, 0.5)))
            return L
        for n in ('legfr', 'legfl'): part(T(n), leg(n, False))
        for n in ('legbr', 'legbl'): part(T(n), leg(n, True))
        # ---- the tail: long, out behind and curling up at the tip
        pv = PIVOT['tail']; tx, ty, tz = pv
        t = chain([(tx, ty, tz), (0, ty - 1.6, tz + 3.0), (0, ty - 2.4, tz + 6.4), (0, ty - 1.2, tz + 9.4), (0, ty + 1.2, tz + 11.0)],
                  [1.2 * k, 1.1 * k, 1.0 * k, 1.0 * k], 1.1 * k, T('tail'), pv, FRONT, ext=0.3)
        t += [el((-0.55 * k, ty + 0.9, tz + 10.5), (0.55 * k, ty + 2.2, tz + 11.5), T('tail_tip'), pv)]
        part(T('tail'), t)
        return M

    # ------------------------------------------------------------------------------------------------ poses
    def L(fwd=0.0):
        return qs(('x', -fwd))

    def P(**kw):
        return kw

    def tail(x=0.0, y=0.0):
        return dict(tail=qs(('y', y), ('x', x)))
    s = math.sin
    POSES = {
        'idle_a': P(head=qs(('x', 2)), **tail(-8, 6)),
        'idle_b': P(_face='alert', head=qs(('z', 14), ('y', -12)), **tail(-20, -14)),                       # the head tilt, tail up
        **{f'walk_{i}': P(_off=(0, 0.15 * (i % 2), 0), legfr=L(20 * s(math.pi * i / 2)), legbl=L(20 * s(math.pi * i / 2)),
                          legfl=L(-20 * s(math.pi * i / 2)), legbr=L(-20 * s(math.pi * i / 2)), head=qs(('x', 4)), **tail(-14, 12 * s(math.pi * i / 2)))
           for i in range(4)},
        **{f'run_{i}': P(_off=(0, (0.4, 1.4, 0.4, 0.0)[i], 0), body=qs(('x', (5, -5, 5, 0)[i])), legfr=L((44, 10, -34, 10)[i]), legfl=L((34, 0, -44, 0)[i]),
                         legbr=L((-34, -10, 44, 10)[i]), legbl=L((-44, 0, 34, 0)[i]), head=qs(('x', -3)), **tail(-4, 0))
           for i in range(4)},
        'jump': P(_off=(0, 3.0, 0), body=qs(('x', -18)), legfr=L(56), legfl=L(56), legbr=L(-46), legbl=L(-46), head=qs(('x', 14)), **tail(-10, 0)),
        # the swipe: up on the haunches, a front paw raised and batting
        'swipe_up': P(_face='alert', _off=(0, -0.4, 0.6), body=qs(('x', -14)), head=qs(('x', 10)), legfr=L(96), legfl=L(10), legbr=L(10), legbl=L(10), **tail(-24, 10)),
        'swipe': P(_face='alert', _off=(0, -0.2, -0.6), body=qs(('x', -6)), head=qs(('x', 4)), legfr=L(36), legfl=L(14), legbr=L(-8), legbl=L(-8), **tail(-24, -10)),
        # sitting: haunches down, front legs straight, chest up, the tail curled round the side
        'sit_a': P(_off=(0, -2.4, 3.2), body=qs(('x', -40)), head=qs(('x', 38)), legfr=L(-40), legfl=L(-40), legbr=L(88), legbl=L(88), tail=qs(('x', 74), ('y', 40))),
        # the loaf: tucked up - legs folded out of sight under her - tail wrapped along the side
        'sit_b': P(_face='happy', _off=(0, -5.0, 0), _hide=('legfr', 'legfl', 'legbr', 'legbl'), head=qs(('x', -2)), tail=qs(('y', 118), ('x', 26))),
        # lying: chest down, front paws out ahead, hind legs tucked, head up
        'lie': P(_off=(0, -5.0, 0), _hide=('legbr', 'legbl'), legfr=L(84), legfl=L(84), head=qs(('y', 20), ('x', -2)), tail=qs(('y', 70), ('x', 22))),
        # grooming: sitting, a front paw raised to the mouth, the head bent down to it
        'groom': P(_face='blink', _off=(0, -2.4, 3.2), body=qs(('x', -40)), head=qs(('x', 62), ('y', 14)), legfr=L(30), legfl=L(-40), legbr=L(88), legbl=L(88),
                   tail=qs(('x', 74), ('y', 40))),
        'happy': P(_face='happy', head=qs(('z', 10)), **tail(-30, 8)),
        'hurt': P(_face='blink', _off=(0, -0.6, 0), body=qs(('x', 6)), head=qs(('x', 18)), **tail(10, 0)),
    }
    DRAFT = ['idle_a', 'idle_b', 'walk_1', 'walk_3', 'run_1', 'jump', 'swipe_up', 'swipe', 'sit_a', 'sit_b', 'lie', 'groom']
    return dict(PREFIX=prefix, PIVOT=PIVOT, PARENT=PARENT, PARTS=tuple(PIVOT), PART_K={}, FACES=FACES, POSES=POSES, DRAFT=DRAFT,
                HIDDEN=HIDDEN, model_name=model_name, models=models, textures=textures, RIG_SCALE=build.get('scale', 1.0), UP=(0.0, 1.0, 0.0), FRONT=FRONT)
