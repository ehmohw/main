"""(3.1 draft, stage 1: art only) A small rig-builder shared by the five new followers' art modules - The Glitch, The Blank Page,
The Cake, The Fixer and The Sapling (glitch_pet_art, blankpage_pet_art, cake_pet_art, fixer_pet_art, sapling_pet_art).

A Rig is a rigkit rig as rigpet / rigfol / draftkit / phase134 / dolls_bake take one - PREFIX, RIG_SCALE, PIVOT, PARENT, PARTS,
PART_K, HIDDEN(p, pose), model_name(p, pose, suffix), textures(), models(), POSES - built box by box in design units (feet at
y=0, facing -z, its right +x), so each follower module says only what it looks like and how it moves.

  box(part, from, to, tex, ...)   an element (rigkit.el) on a part; tex 'FACE' is the part's face (face_<expression> per _face)
  seg(part, A, B, w, h, tex)      a box along a line (rigkit.seg)
  skin(suffix, {tex: tex2})       a model set with some textures swapped - a palette, a shiny, a stage, an afterimage ('_g')
  opt                             parts hidden unless a pose's '_show' names them (a held prop, a burst of shards)
  ground(pose)                    the pose's '_off' set so its lowest point stands on y=0 (lift: off the floor by that much)
  fit(pose)                       phase134.FIT: (lowest y, height, x0, x1, z0, z1) in blocks at RIG_SCALE

Textures: pixel coats painted in square cells (the pack's blocky look, as gem_buddies_art.tex), faces drawn on a 32 grid."""
import math
import random
from PIL import Image, ImageDraw

from rigkit import qs, el, seg as _seg, solve, qrot, D, I

FACESIDES = ('north', 'south', 'east', 'west', 'up', 'down')


def hexc(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """a limb's turn (as kettle_art): swung forward, out to its own side, twisted"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def T(x=0.0, y=0.0, z=0.0):
    """a trunk's turn: leaned forward (x), turned (y), tipped to its left (z)"""
    return qs(('x', x), ('y', y), ('z', z))


# ---------------------------------------------------------------------------------------------------- textures
def coat(col, seed, size=32, var=0.06, cell=2, spots=None, alpha=255):
    """one colour in square cells, each its own shade, a few darker and lighter (a vanilla block's look)"""
    im = Image.new('RGBA', (size, size)); px = im.load(); c = hexc(col); r = random.Random(seed * 7919 + 13)
    for cy in range(0, size, cell):
        for cx in range(0, size, cell):
            k = 1 + r.uniform(-1, 1) * var; q = r.random()
            if q < 0.08: k *= 0.88
            elif q < 0.12: k *= 1.08
            v = tuple(max(0, min(255, int(c[i] * k))) for i in range(3)) + (alpha,)
            for y in range(cy, min(size, cy + cell)):
                for x in range(cx, min(size, cx + cell)): px[x, y] = v
    if spots:
        d = ImageDraw.Draw(im)
        for sc, n in spots:
            for _ in range(n):
                x, y = r.randrange(0, size, cell), r.randrange(0, size, cell)
                d.rectangle((x, y, x + cell - 1, y + cell - 1), fill=hexc(sc, alpha))
    return im


def flat(col, size=16, alpha=255):
    return Image.new('RGBA', (size, size), hexc(col, alpha))


def shade(im, top=1.12, bot=0.82):
    """lit from above: a vertical ramp over the texture (pixel steps)"""
    im = im.copy(); px = im.load(); n = im.height
    for y in range(n):
        k = top + (bot - top) * (y // max(1, n // 8) * max(1, n // 8)) / max(1, n - 1)
        for x in range(im.width):
            r, g, b, a = px[x, y]; px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a)
    return im


def ghost(im, tint, a=120):
    """an afterimage: the texture washed toward a tint, see-through (rendered blended)"""
    im = im.convert('RGBA').copy(); px = im.load(); t = hexc(tint)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, al = px[x, y]
            if al < 10: continue
            v = (r + g + b) / 765
            px[x, y] = (int(t[0] * (0.5 + 0.5 * v)), int(t[1] * (0.5 + 0.5 * v)), int(t[2] * (0.5 + 0.5 * v)), a)
    return im


def remap(im, pal):
    """recolour by luminance through a list of hex colours, dark to light (a palette swap)"""
    im = im.convert('RGBA').copy(); px = im.load(); cols = [hexc(c) for c in pal]; n = len(cols)
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 10: continue
            v = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            px[x, y] = cols[min(n - 1, int(v * n))][:3] + (a,)
    return im


def canvas(n=32, fill=None):
    im = Image.new('RGBA', (n, n), hexc(fill) if fill else (0, 0, 0, 0)); return im, ImageDraw.Draw(im)


def up(im, n):
    return im.resize((n, n), Image.NEAREST)


# ---------------------------------------------------------------------------------------------------- the rig
def _rotm(rot):
    """an element's rotation (rigkit.el's rot) -> (3x3 rows, origin) in design space"""
    if not rot: return None, None
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if isinstance(rot[0], str):
        M = {'x': rx, 'y': ry, 'z': rz}[rot[0]](math.radians(rot[1]))
    else:
        ax, ay, az = rot[0]; M = mm(rz(math.radians(az)), mm(ry(math.radians(ay)), rx(math.radians(ax))))
    return M, rot[-1]


class Rig:
    def __init__(self, prefix, scale, pivot, parent, faces=(), face_part='head', opt=(), companion=None):
        self.PREFIX = prefix; self.RIG_SCALE = scale; self.COMPANION = companion or scale
        self.PIVOT = dict(pivot); self.PARENT = dict(parent); self.PARTS = tuple(pivot); self.PART_K = {}
        self.FACES = tuple(faces); self.FACE_PART = face_part; self.OPT = set(opt)
        self._els = {p: [] for p in pivot}; self._pts = {p: [] for p in pivot}
        self._tex = {}; self._skins = {}; self.POSES = {}; self.DRAFT = []
        self._n = 0

    # ---- building
    def tex(self, name, im):
        self._tex[name] = im

    def box(self, part, fr, to, tex, rot=None, uv=None, faces=None, light=0, full=False):
        pv = self.PIVOT[part]
        if full: uv = dict({f: [0, 0, 16, 16] for f in FACESIDES}, **(uv or {}))
        self._n += 1
        e = el(fr, to, tex, pv, rot, uv, faces, light, shift=None if full or uv else ((self._n * 0.37) % 1, (self._n * 0.61) % 1))
        self._els[part].append(e)
        M, o = _rotm(rot)
        for x in (fr[0], to[0]):
            for y in (fr[1], to[1]):
                for z in (fr[2], to[2]):
                    v = (x, y, z)
                    if M:
                        d = [v[i] - o[i] for i in range(3)]
                        v = tuple(sum(M[i][k] * d[k] for k in range(3)) + o[i] for i in range(3))
                    self._pts[part].append(v)
        return e

    def seg(self, part, A, B, w, h, tex, up=(0.0, 1.0, 0.0), ext=0.0, light=0):
        e = _seg(A, B, w, h, tex, self.PIVOT[part], up, ext, light)
        self._els[part].append(e)
        for v in (A, B): self._pts[part].append(tuple(v))
        return e

    def skin(self, suffix, swap):
        """a model set named <part><suffix>: these textures swapped for others (names without the prefix)"""
        self._skins[suffix] = dict(swap)

    # ---- what rigkit / draftkit / phase134 read
    def HIDDEN(self, p, pose):
        if not self._els[p] or p in pose.get('_hide', ()): return True          # (a bare joint - the root of the slices - has no model)
        return p in self.OPT and p not in pose.get('_show', ())

    def model_name(self, p, pose=None, suffix=''):
        face = f'_x{pose["_face"]}' if pose and p == self.FACE_PART and pose.get('_face') else ''
        return f'{self.PREFIX}{p}{face}{suffix}'

    def textures(self):
        return {f'{self.PREFIX}{k}': (v() if callable(v) else v) for k, v in self._tex.items()}

    def models(self):
        out = {}
        for suffix, swap in [('', {})] + list(self._skins.items()):
            for p in self.PARTS:
                variants = [('', None)] + ([(f'_x{f}', f) for f in self.FACES] if p == self.FACE_PART else [])
                for vs, face in variants:
                    els = []
                    for e in self._els[p]:
                        fcs = {}
                        for k, fc in e['faces'].items():
                            t = fc['texture'][1:]
                            if t == 'FACE': t = 'face' if face is None else f'face_{face}'
                            t = swap.get(t, t)
                            fcs[k] = dict(fc, texture='#' + self.PREFIX + t)
                        els.append(dict(e, faces=fcs))
                    for e in els:
                        for v in e['from'] + e['to']: assert -16 <= v <= 32, (self.PREFIX, p, e['from'], e['to'])
                    used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
                    if not els: continue
                    out[f'{self.PREFIX}{p}{vs}{suffix}'] = ({t: f'bm:block/{t}' for t in used}, els)
        return out

    # ---- poses
    def world_pts(self, pose):
        xf = solve(self.PIVOT, self.PARENT, pose)
        out = []
        for p in self.PARTS:
            if self.HIDDEN(p, pose): continue
            q, t = xf[p]; pv = D(self.PIVOT[p])
            for v in self._pts[p]:
                r = qrot(q, tuple(D(v)[i] - pv[i] for i in range(3)))
                w = tuple(pv[i] + t[i] + r[i] for i in range(3))
                out.append((-w[0], w[1], -w[2]))           # (back to design axes)
        return out

    def ground(self, pose, lift=0.0, dx=0.0, dz=0.0):
        pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
        low = min(v[1] for v in self.world_pts(pose))
        pose['_off'] = (o[0] + dx, round(lift - low, 3), o[2] + dz)
        return pose

    def fit(self, pose=None):
        pts = self.world_pts(pose or self.POSES['idle_a']); U = self.RIG_SCALE / 16
        lo = [min(p[i] for p in pts) * U for i in range(3)]; hi = [max(p[i] for p in pts) * U for i in range(3)]
        return (round(lo[1], 3), round(hi[1] - lo[1], 3), round(lo[0], 3), round(hi[0], 3), round(lo[2], 3), round(hi[2], 3))


# ---------------------------------------------------------------------------------------------------- shapes
def rounded(rig, part, c, r, h, tex, n=3, top_tex=None, light=0):
    """a squat round drum (a cake tier, a pot): n boxes turned about y, crossed, so it reads round from every side"""
    x, y, z = c
    for i in range(n):
        a = 90.0 / n * i
        e = rig.box(part, (x - r, y, z - r * 0.42), (x + r, y + h, z + r * 0.42), tex, rot=('y', a, c) if a else None, light=light)
        e2 = rig.box(part, (x - r * 0.42, y, z - r), (x + r * 0.42, y + h, z + r), tex, rot=('y', a, c) if a else None, light=light)
        if top_tex:
            for ee in (e, e2): ee['faces']['up']['texture'] = '#' + top_tex
    return rig


def blob(rig, part, c, r, tex, k=(1.0, 1.0, 1.0), light=0):
    """a rounded lump: three crossed boxes (a ball read blocky)"""
    x, y, z = c; a, b, d = r * k[0], r * k[1], r * k[2]
    rig.box(part, (x - a, y - b * 0.62, z - d * 0.62), (x + a, y + b * 0.62, z + d * 0.62), tex, light=light)
    rig.box(part, (x - a * 0.62, y - b, z - d * 0.62), (x + a * 0.62, y + b, z + d * 0.62), tex, light=light)
    rig.box(part, (x - a * 0.62, y - b * 0.62, z - d), (x + a * 0.62, y + b * 0.62, z + d), tex, light=light)
    return rig
