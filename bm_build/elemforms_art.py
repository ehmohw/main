"""3.0g (redo): THE ETHEREAL AND WRAITHFIRE FORMS' ART for elemforms.py's ten - real new shapes per character, not a palette swap.

The owner, of the first pass: "way too generic - just retextures instead of properly new forms". So each of the ten gets its own
DESIGN per form: new parts built onto its own bones (crowns, halos, horns, wings, crystal weapons, flame manes, soul-fire tails,
floating shards...), some of its own pieces taken away and redrawn (a scythe's blade, a pencil, a stem), its own textures recoloured
to a palette chosen for it, and a few painted outright. Everything stays CLEAN: a few bold shapes, smooth colour, no speckle.

HOW IT RIDES (elemforms.Twins, unchanged in spirit): every item definition of theirs chooses by its display's custom_model_data float
(0 itself, 1 Ethereal, 2 Wraithfire) between the model and its twin. A twin is now the model's own elements, recoloured, MINUS what
the design drops, PLUS the design's new parts for that bone - built in that bone's own model space from its measured bounds, so
every new part is parented to the rig's joint it sits on (a halo turns with the head, a tail-flame wags with the tail, a crystal
blade swings with the scythe), in every pose, face and look. Nothing new for the datapack: the same float, the same parts.

  DESIGNS[k][form] = dict(pal=..., parts={bone: builder(B) -> elements}, drop={bone: textures to remove}, retex={texture: painter})
    bone: the part's model-name stem after the prefix ('head' matches bd_head, bd_head_xhappy, bd_head_c3...; 'w1r' ds_w1r_open)
    B: the bone's measured model (B.lo, B.hi, B.c - its bounds and centre; B.of(tex) - the bounds of its elements with a texture)
Model space: the bone's joint at (8, 8, 8), its front toward -z (north), his right +x. Every element stays inside -16..32.
"""
import math
import colorsys

import numpy as np
from PIL import Image

import rigkit as RK

ETH, WR = 'e', 'w'
SUB = 'elf'
FULL = {d: [0, 0, 16, 16] for d in ('north', 'south', 'east', 'west', 'up', 'down')}


# ==================================================================================================== textures (16 px, clean)
def _rgb(h):
    if isinstance(h, tuple): return h
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _img(fn, n=16):
    im = Image.new('RGBA', (n, n)); px = im.load()
    for y in range(n):
        for x in range(n):
            c = fn(x, y)
            px[x, y] = tuple(max(0, min(255, int(v))) for v in c) + ((255,) if len(c) == 3 else ())
    return im


def crystal_t(hi, lo):
    """a cut crystal's face: lit along one side, a bright facet line, darker toward the far edge, one white glint"""
    hi, lo = _rgb(hi), _rgb(lo)
    def f(x, y):
        d = abs(x - 6.5) / 9.5
        c = _mix(hi, lo, min(1, d * 1.1 + (0.18 if x > 6 else 0)))
        if x in (5, 6): c = _mix(c, (255, 255, 255), 0.55)
        if x in (0, 15): c = _mix(c, lo, 0.5)
        if (x, y) in ((5, 3), (6, 3), (10, 11)): c = (255, 255, 255)
        return c
    return _img(f)


def grad_t(top, bottom, line=None, edge=None):
    """a vertical gradient (top -> bottom), a lit line down its middle, a darker rim"""
    top, bottom = _rgb(top), _rgb(bottom)
    def f(x, y):
        c = _mix(top, bottom, y / 15)
        if line and x in (7, 8): c = _rgb(line)
        if edge and (x in (0, 15)): c = _mix(c, _rgb(edge), 0.6)
        return c
    return _img(f)


def flat_t(c, rim=None):
    c = _rgb(c)
    return _img(lambda x, y: _rgb(rim) if rim and (x in (0, 15) or y in (0, 15)) else c)


def flame_t(base='#0a6fa8', mid='#2fd2f2', tip='#e8ffff'):
    """soul fire: deep blue at the root, cyan, white at the tip (the tongues are built tip-up: v 0 is the top)"""
    base, mid, tip = _rgb(base), _rgb(mid), _rgb(tip)
    def f(x, y):
        t = y / 15
        c = _mix(tip, mid, t * 2) if t < 0.5 else _mix(mid, base, (t - 0.5) * 2)
        core = 1 - abs(x - 7.5) / 8
        return _mix(c, tip, max(0, core - 0.55) * 0.9)
    return _img(f)


def rainbow_t(l=0.82, s=0.75, off=0.0):
    """prismatic light, every colour across the face, a white line down the middle"""
    def f(x, y):
        r, g, b = colorsys.hls_to_rgb((x / 16 + off) % 1.0, l, s)
        c = (r * 255, g * 255, b * 255)
        return _mix(c, (255, 255, 255), 0.6) if x in (7, 8) else c
    return _img(f)


def outline_t(line, fill=None, dash=True):
    """a ghost's outline: a dashed border, its middle see-through (or a faint fill)"""
    line = _rgb(line)
    def f(x, y):
        edge = x in (0, 1, 14, 15) or y in (0, 1, 14, 15)
        if edge and (not dash or ((x + y) // 3) % 2 == 0): return line + (255,)
        if fill: return _rgb(fill) + (255,)
        return (0, 0, 0, 0)
    return _img(f)


# the shared textures of the new parts (name -> painter); a design's own are added in its 'tex'
TEXLIB = {
    # ETHEREAL
    'x_cwhite': lambda: crystal_t('#ffffff', '#a8d8f8'),
    'x_cice': lambda: crystal_t('#e8fcff', '#58b8f0'),
    'x_caqua': lambda: crystal_t('#d8fff6', '#2cc0c0'),
    'x_crose': lambda: crystal_t('#fff0f8', '#f080c0'),
    'x_clilac': lambda: crystal_t('#f4ecff', '#9a78f0'),
    'x_camber': lambda: crystal_t('#fff8d8', '#f0a838'),
    'x_cgold': lambda: crystal_t('#fffbe0', '#e0b040'),
    'x_cmint': lambda: crystal_t('#eafff0', '#50d890'),
    'x_cruby': lambda: crystal_t('#ffd8e0', '#d8204a'),
    'x_csapph': lambda: crystal_t('#dce8ff', '#2a58d8'),
    'x_gold': lambda: grad_t('#fff6c8', '#e8b84a', line='#ffffff'),
    'x_light': lambda: grad_t('#ffffff', '#fff0b8'),
    'x_prism': lambda: rainbow_t(),
    'x_pearl': lambda: grad_t('#ffffff', '#e4dcf4'),
    # WRAITHFIRE
    'x_flame': lambda: flame_t(),
    'x_f0': lambda: grad_t('#1a8cc8', '#0a4a80'), 'x_f1': lambda: grad_t('#3ad4f4', '#1a9cd0'),
    'x_f2': lambda: grad_t('#a8f6ff', '#4ad8f4'), 'x_f3': lambda: grad_t('#ffffff', '#b8f8ff'),
    'x_flame_hot': lambda: flame_t('#1aa8d8', '#8af4ff', '#ffffff'),
    'x_soul': lambda: grad_t('#c8fcff', '#38d0f0', line='#ffffff'),
    'x_smoke': lambda: grad_t('#1e3440', '#0a1218', edge='#38d0f0'),
    'x_obsid': lambda: crystal_t('#3a5868', '#0a141c'),
    'x_scrys': lambda: crystal_t('#b8fbff', '#127890'),
    'x_iron': lambda: grad_t('#3a4048', '#16181e', line='#5ae0ff'),
}


# ==================================================================================================== recolouring a bone's own textures
def _hexf(h):
    return np.array(_rgb(h), float) / 255


def _ramp(stops, t):
    S = np.array([_hexf(s) for s in stops])
    t = np.clip(np.nan_to_num(np.asarray(t, float)), 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = (t - i)[..., None]
    return S[i] * (1 - f) + S[i + 1] * f


def _lum(rgb):
    return 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]


def recolour(im, ramp, keep=0.0, ink=None, sheen=0.0, lift=0.0, alpha=None, flatten=0.0, ink_at=None):
    """a texture remapped clean: its own light and shade kept (luminance, stretched over the texture's own range) onto `ramp`;
    keep: how much of its own hue stays (each texel's hue, pastel-lifted); ink: its darkest marks (eyes, lines) drawn in this
    colour instead (ink_at: every texel darker than this share of its range); sheen: a soft diagonal band of light across it (a
    crystal's face); lift: lighter overall; flatten: its texel-to-texel speckle smoothed away (a share), its shapes kept"""
    a = np.asarray(im.convert('RGBA')).astype(float) / 255
    rgb, al = a[..., :3], a[..., 3]
    L = _lum(rgb)
    vis = al > 0
    lo, hi = (np.percentile(L[vis], 3), np.percentile(L[vis], 97)) if vis.any() else (0, 1)
    t = np.clip((L - lo) / max(0.06, hi - lo), 0, 1) if hi - lo > 0.03 else np.full(L.shape, 0.6)
    t0 = t
    if flatten:
        H, W = t.shape
        c = max(1, W // 16)
        tp = np.pad(t, c, mode='edge')
        bl = sum(tp[c + dy * c:c + dy * c + H, c + dx * c:c + dx * c + W] for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9
        t = t * (1 - flatten) + bl * flatten
    t = np.clip(t * (1 - lift) + lift, 0, 1)
    out = _ramp(ramp, t)
    if keep:
        mx, mn = rgb.max(-1), rgb.min(-1)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
        hsv = np.vectorize(lambda r, g, b: colorsys.rgb_to_hsv(r, g, b)[0])(rgb[..., 0], rgb[..., 1], rgb[..., 2]) if sat.max() > 0.05 else np.zeros(L.shape)
        pastel = np.stack(np.vectorize(lambda h, s, l: colorsys.hls_to_rgb(h, l, s))(hsv, np.clip(sat * 0.9, 0, 0.9), 0.42 + 0.5 * t), -1)
        k = (keep * np.clip(sat * 2.2, 0, 1))[..., None]
        out = out * (1 - k) + pastel * k
    if sheen:
        H, W = L.shape
        yy, xx = np.mgrid[0:H, 0:W]
        d = ((xx + yy) / max(1, (H + W) / 2)) % 1.0
        band = np.clip(1 - np.abs(d - 0.32) * 7, 0, 1) * sheen
        out = out * (1 - band[..., None]) + band[..., None]
    if ink is not None:
        dark = (t0 < ink_at) if ink_at is not None else ((L < 0.16) & (t0 < 0.22))
        out = np.where(dark[..., None], _hexf(ink), out)
    if alpha is not None:
        al = al * alpha
    o = np.concatenate([np.clip(out, 0, 1), al[..., None]], -1)
    return Image.fromarray((o * 255 + 0.5).astype('uint8'), 'RGBA')


# each form's default palettes (a design overrides them): base - the body; accent - its brightest pieces; glow - eyes and fires
PAL = {
    ETH: dict(base=dict(ramp=['#6a7cc8', '#a8c4f0', '#dceaff', '#ffffff'], keep=0.35, ink='#24306e', sheen=0.35, flatten=0.5),
              accent=dict(ramp=['#c08a2a', '#f0cc60', '#fff4c4', '#ffffff'], sheen=0.4),
              glow=dict(ramp=['#bdf4ff', '#ffffff'], lift=0.3), light=dict(base=8, accent=12, glow=15)),
    WR: dict(base=dict(ramp=['#05090d', '#0e1c26', '#1a3442', '#2e6274'], ink='#03060a', flatten=0.6),
             accent=dict(ramp=['#0a5a78', '#1eb4d8', '#8af4ff', '#ffffff']),
             glow=dict(ramp=['#5ae6ff', '#e8ffff'], lift=0.4), light=dict(base=3, accent=13, glow=15)),
}


# ==================================================================================================== shapes (model space)
def _d(p):                       # (model -> the gem kit's design space: rigkit.el adds 8)
    return tuple(c - 8 for c in p)


def _u(v):
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / n for c in v)


def box(fr, to, tex, light=0, rot=None):
    """an axis-aligned box, every face the whole texture. rot: (axis, angle, origin) - a turn on one axis"""
    e = {'from': [round(v, 3) for v in fr], 'to': [round(v, 3) for v in to], 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#' + tex} for f in FULL}}
    if rot: e['rotation'] = {'axis': rot[0], 'angle': rot[1], 'origin': [round(v, 3) for v in rot[2]]}
    if light: e['light_emission'] = light
    return e


def beam(A, B, w, tex, light=0, t=None, up=(0.0, 1.0, 0.0), diamond=False, ext=0.0):
    """a box from A to B (w across, t thick: its cross-section turned so t lies along `up`'s side), or a diamond in section"""
    d = tuple(B[i] - A[i] for i in range(3))
    x, y, z = RK.frame(d, up)
    if diamond:
        x, y, z = RK.frame(d, _u(tuple(x[i] + y[i] for i in range(3))))
    t = w if t is None else t
    L = math.sqrt(sum(c * c for c in d)) / 2 + ext
    m = tuple((A[i] + B[i]) / 2 for i in range(3))
    ang = RK.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    md = _d(m)
    fr, to = (md[0] - w / 2, md[1] - t / 2, md[2] - L), (md[0] + w / 2, md[1] + t / 2, md[2] + L)
    return RK.el(fr, to, tex, (0.0, 0.0, 0.0), None if max(abs(v) for v in ang) < 1e-3 else (ang, md), uv=FULL, light=light)


def crystal(A, B, w, tex, light=10, tip=None):
    """a tapered crystal from its root A to its point B: four diamond-cut boxes narrowing to a sharp tip"""
    P = lambda f: tuple(A[i] + (B[i] - A[i]) * f for i in range(3))
    steps = ((0.0, 0.45, 1.0), (0.4, 0.72, 0.72), (0.68, 0.9, 0.44), (0.86, 1.0, 0.2))
    return [beam(P(a), P(b), w * k, tex, light if b < 1 else (tip or light), diamond=True, ext=0.1) for a, b, k in steps]


def tongue(A, h, w, lean=(0.0, 0.0, 0.0), tex='x_flame', tip='x_flame_hot', light=15, down=False):
    """a tongue of fire from A: wide at its root, curling to a point h above it (lean: where its tip drifts, per unit up)"""
    s = -1 if down else 1
    pts = []
    for f in (0.0, 0.3, 0.58, 0.82, 1.0):
        pts.append((A[0] + lean[0] * h * f * f, A[1] + s * h * f, A[2] + lean[2] * h * f * f))
    ws = (1.0, 0.82, 0.58, 0.3)
    return [beam(pts[i], pts[i + 1], w * ws[i], _shade(tex, tip, i), light, diamond=True, ext=0.15) for i in range(4)]


def _shade(tex, tip, i):
    """a tongue's segment's texture: soul fire in four clean steps, deep blue at the root to white at the tip"""
    if tex == 'x_flame': return ('x_f0', 'x_f1', 'x_f2', 'x_f3')[i]
    return tex if i < 2 else tip


def flick(A, d, h, w, tex='x_flame', tip='x_flame_hot', light=15, curl=(0.0, 0.35, 0.0)):
    """a tongue of fire from A along direction d (streaming back, out sideways...), its tip curling toward `curl`"""
    d = _u(d)
    pts = [tuple(A[i] + d[i] * h * f + curl[i] * h * f * f for i in range(3)) for f in (0.0, 0.3, 0.58, 0.82, 1.0)]
    ws = (1.0, 0.82, 0.58, 0.3)
    return [beam(pts[i], pts[i + 1], w * ws[i], _shade(tex, tip, i), light, diamond=True, ext=0.15) for i in range(4)]


def crescent(c, r, a0, a1, wmax, tex, light=13, n=10, plane='xy', t=0.6):
    """a crescent moon (or a glaive's blade): an arc of r round c from a0 to a1 degrees, thickest in its middle, sharp at both horns"""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]) if plane == 'xy' else (c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)))
    out = []
    for i in range(n):
        f = (i + 0.5) / n
        w = 0.25 + (wmax - 0.25) * math.sin(math.pi * f)
        out.append(beam(pts[i], pts[i + 1], w, tex, light, t=t, up=(0.0, 0.0, 1.0) if plane == 'xy' else (0.0, 1.0, 0.0), ext=0.12))
    return out


def zigzag(c, r0, r1, n, w, tex, light=14, arc=(0.0, 360.0), z=0.0):
    """a jagged ring (a storm's halo, a scribbled sun) in the xy plane: its points alternating between r0 and r1"""
    pts = []
    full = abs(arc[1] - arc[0]) >= 359.9
    for i in range(n + (0 if full else 1)):
        a = math.radians(arc[0] + (arc[1] - arc[0]) * i / n)
        r = r1 if i % 2 else r0
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2] + z))
    if full: pts.append(pts[0])
    return [beam(pts[i], pts[i + 1], w, tex, light, t=0.5, up=(0.0, 0.0, 1.0), ext=0.15) for i in range(len(pts) - 1)]


def ring(c, r, n, w, tex, light=12, plane='xz', tilt=0.0, t=None, arc=(0.0, 360.0), diamond=False):
    """a ring (or an arc of one) of n beams round c: in the xz plane (a halo over a head) or xy (a disc behind one), tilted on x"""
    pts = []
    a0, a1 = arc
    full = abs(a1 - a0) >= 359.9
    for i in range(n + (0 if full else 1)):
        a = math.radians(a0 + (a1 - a0) * i / n)
        u, v = r * math.cos(a), r * math.sin(a)
        if plane == 'xz': p = (u, 0.0, v)
        else: p = (u, v, 0.0)
        tl = math.radians(tilt)
        p = (p[0], p[1] * math.cos(tl) - p[2] * math.sin(tl), p[1] * math.sin(tl) + p[2] * math.cos(tl))
        pts.append((c[0] + p[0], c[1] + p[1], c[2] + p[2]))
    if full: pts.append(pts[0])
    up = (0.0, 1.0, 0.0) if plane == 'xz' else (0.0, 0.0, 1.0)
    return [beam(pts[i], pts[i + 1], w, tex, light, t=t, up=up, diamond=diamond, ext=0.08) for i in range(len(pts) - 1)]


def rays(c, r0, r1, n, w, tex, light=14, arc=(0.0, 360.0), plane='xy', zs=0.0):
    """a sunburst: n spikes radiating from r0 to r1 round c, in the xy plane (behind a head) - each a crystal"""
    out = []
    for i in range(n):
        a = math.radians(arc[0] + (arc[1] - arc[0]) * (i + 0.5) / n)
        d = (math.cos(a), math.sin(a), 0.0) if plane == 'xy' else (math.cos(a), 0.0, math.sin(a))
        L = r1 if i % 2 == 0 else r0 + (r1 - r0) * 0.62
        A = (c[0] + d[0] * r0, c[1] + d[1] * r0, c[2] + d[2] * r0 + zs)
        B = (c[0] + d[0] * L, c[1] + d[1] * L, c[2] + d[2] * L + zs)
        out += crystal(A, B, w, tex, light)
    return out


# the wing: a bird's, in its own plane (u out from the root and swept back, v up) - an arm along the leading edge, and long blades
ARM = ((0.0, 0.0), (4.0, 3.6), (7.5, 6.5))
FEATHERS = (((7.0, 6.2), (15.5, 11.0), 5.0), ((7.2, 5.6), (16.6, 3.8), 5.4), ((5.4, 4.6), (13.2, -2.8), 5.4),
            ((3.2, 2.8), (9.2, -5.8), 4.8), ((1.2, 1.0), (4.8, -6.4), 3.8))


def wing(root, side, s, texs, arm_tex, light=9, tip_light=12, sweep=0.55, curl=0.0, n=5, t=0.45, spread=1.0):
    """a wing from root (his right: side 1, +x), s its size (1: the Gem's - about a block across at full scale), texs the blades'
    textures from the top down (cycled), curl: each blade's tip curling up (a flame's feather)"""
    o = _u((side * 1.0, 0.0, sweep)); up = (0.0, 1.0, 0.0)
    nrm = _u((o[1] * up[2] - o[2] * up[1], o[2] * up[0] - o[0] * up[2], o[0] * up[1] - o[1] * up[0]))
    W3 = lambda uv, lift=0.0: tuple(root[i] + (o[i] * uv[0] * spread + up[i] * uv[1]) * s + nrm[i] * lift for i in range(3))
    els = []
    for j, (a, b, w) in enumerate(FEATHERS[:n]):
        pts = []
        for f in (0.0, 0.35, 0.65, 0.86, 1.0):
            uv = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f + curl * f * f)
            pts.append(W3(uv, (-0.15 - 0.12 * j) * s))
        tex = texs[j % len(texs)]
        k = len(pts) - 1
        for i in range(k):
            ff = 1 - 0.7 * i / max(1, k - 1)
            els.append(beam(pts[i], pts[i + 1], w * ff * s, tex, light if i < k - 1 else tip_light, t=t * s, up=nrm, ext=0.14 * s))
    arm = [W3(p, 0.2 * s) for p in ARM]
    for i in range(len(arm) - 1):
        els.append(beam(arm[i], arm[i + 1], (1.7 - 0.4 * i) * s, arm_tex, tip_light, diamond=True, ext=0.3 * s))
    els.append(beam(W3((-0.4, -0.6), 0.2 * s), W3((0.9, 0.7), 0.2 * s), 2.2 * s, arm_tex, tip_light, diamond=True))
    return els


def line_wing(root, side, s, tex, light=14, sweep=0.5, n=5):
    """a drawn wing (Mr. Capshun's): its outline in lines of light - a leading edge, feather strokes fanning down from it, their
    tips joined in scallops"""
    o = _u((side * 1.0, 0.0, sweep)); up = (0.0, 1.0, 0.0)
    W3 = lambda u, v: tuple(root[i] + (o[i] * u + up[i] * v) * s for i in range(3))
    edge = [W3(0, 0), W3(4, 3.4), W3(8, 5.4), W3(12, 5.6), W3(15, 4.2)]
    els = [beam(edge[i], edge[i + 1], 0.55 * s, tex, light, ext=0.2 * s) for i in range(len(edge) - 1)]
    tips = [W3(15, 4.2), W3(13.6, -0.6), W3(11, -4.4), W3(7.6, -6.6), W3(4.2, -6.4), W3(1.2, -3.6), W3(0, 0)]
    roots = [W3(12.4, 5.4), W3(9.6, 5.4), W3(6.6, 4.8), W3(3.6, 3.0), W3(1.6, 1.4)]
    for i in range(len(tips) - 1):
        mid = tuple((tips[i][j] + tips[i + 1][j]) / 2 + (o[j] * 0.9 + up[j] * -0.9) * s * (0 if i == len(tips) - 2 else 1) for j in range(3))
        els += [beam(tips[i], mid, 0.5 * s, tex, light, ext=0.15 * s), beam(mid, tips[i + 1], 0.5 * s, tex, light, ext=0.15 * s)]
    for r_, t_ in list(zip(roots, tips[1:6]))[1::2]:               # (two feather strokes inside it - more and it reads as a cage)
        els.append(beam(r_, t_, 0.4 * s, tex, light - 2, ext=0.1 * s))
    return els


def plume(A, n, h, w, spread, tex='x_flame', tip='x_flame_hot', back=0.0, lean_x=0.0, light=15):
    """a crest of n fire tongues in a row from A along x (spread apart), the middle tallest, all leaning back"""
    out = []
    for i in range(n):
        f = (i - (n - 1) / 2) / max(1, (n - 1) / 2) if n > 1 else 0.0
        hh = h * (1 - 0.38 * abs(f))
        out += tongue((A[0] + f * spread, A[1], A[2]), hh, w * (1 - 0.25 * abs(f)), (lean_x * f, 0.0, back), tex, tip, light)
    return out


# ==================================================================================================== a bone, measured
class Bone:
    def __init__(self, els, textures):
        self.els = els
        self.tex = textures
        bb = [_aabb(e) for e in els] or [[(7.5, 8.5)] * 3]
        self.lo = tuple(min(b[i][0] for b in bb) for i in range(3))
        self.hi = tuple(max(b[i][1] for b in bb) for i in range(3))
        self.c = tuple((self.lo[i] + self.hi[i]) / 2 for i in range(3))
        self._bb = bb

    def of(self, *stems):
        """the bounds of the elements textured with any of these (texture names, or stems of them) - None if none"""
        hit = []
        for e, b in zip(self.els, self._bb):
            names = {self.tex.get(f.get('texture', '#')[1:], '').split('/')[-1] for f in e.get('faces', {}).values()}
            if any(n.startswith(s) for n in names for s in stems): hit.append(b)
        if not hit: return None
        lo = tuple(min(b[i][0] for b in hit) for i in range(3)); hi = tuple(max(b[i][1] for b in hit) for i in range(3))
        return lo, hi, tuple((lo[i] + hi[i]) / 2 for i in range(3)), [(tuple(a for a, _b in b), tuple(b_ for _a, b_ in b)) for b in hit]

    def lowest(self):
        """the bottom of the lowest element: (x, y, z) - a leg's foot"""
        b = min(self._bb, key=lambda b: b[1][0])
        return ((b[0][0] + b[0][1]) / 2, b[1][0], (b[2][0] + b[2][1]) / 2)

    def highest(self):
        b = max(self._bb, key=lambda b: b[1][1])
        return ((b[0][0] + b[0][1]) / 2, b[1][1], (b[2][0] + b[2][1]) / 2)


def _aabb(e):
    pts = [[x, y, z] for x in (e['from'][0], e['to'][0]) for y in (e['from'][1], e['to'][1]) for z in (e['from'][2], e['to'][2])]
    r = e.get('rotation')
    if r:
        o = r.get('origin', [8, 8, 8])
        turns = [(r['axis'], r['angle'])] if 'axis' in r else [(a, r.get(a, 0)) for a in ('x', 'y', 'z')]
        for axis, ang in turns:
            if not ang: continue
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            i, k = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}[axis]
            for p in pts:
                a, b = p[i] - o[i], p[k] - o[k]
                p[i], p[k] = o[i] + a * c - b * s_, o[k] + a * s_ + b * c
    return [(min(p[i] for p in pts), max(p[i] for p in pts)) for i in range(3)]


def mirror(els):
    """elements on his right, mirrored to his left as well (model x about 8)"""
    out = list(els)
    for e in els:
        e2 = dict(e); e2['from'] = [16 - e['to'][0], e['from'][1], e['from'][2]]; e2['to'] = [16 - e['from'][0], e['to'][1], e['to'][2]]
        if 'rotation' in e:
            r = dict(e['rotation']); r['origin'] = [16 - r['origin'][0], r['origin'][1], r['origin'][2]]
            if 'axis' in r:
                if r['axis'] in ('y', 'z'): r['angle'] = -r['angle']
            else:
                r['y'] = -r.get('y', 0); r['z'] = -r.get('z', 0)
            e2['rotation'] = r
        e2['faces'] = {({'east': 'west', 'west': 'east'}.get(k, k)): v for k, v in e['faces'].items()}
        out.append(e2)
    return out


from elemforms_designs import DESIGNS  # noqa: E402  (the ten, each form - below this kit)


# ==================================================================================================== used by elemforms.Twins
def bone_of(k, model):
    """the design's bone for a model name: the longest stem in its form's parts/drop that the name starts (stem, then '_' or end)"""
    D = DESIGNS.get(k)
    if not D: return None
    pre = D['pre']
    if not model.startswith(pre): return None
    rest = model[len(pre):]
    stems = sorted({s for f in (ETH, WR) for s in list(D[f].get('parts', {})) + list(D[f].get('drop', {})) + list(D[f].get('keep_only', {}))},
                   key=len, reverse=True)
    for s in stems:
        if rest == s or rest.startswith(s + '_'): return s
    return None


def palette(k, el, tex_name, kind):
    """the recolour settings for one of a follower's own textures in a form"""
    D = DESIGNS[k][el]
    base = dict(PAL[el][kind])
    base.update(D.get('pal', {}).get(kind, {}))
    for stem, over in D.get('tex', {}).items():
        if tex_name.startswith(stem):
            if callable(over): return over
            b = dict(base); b.update(over); return b
    return base


def light_of(k, el, kind):
    L = dict(PAL[el]['light']); L.update(DESIGNS[k][el].get('light', {}))
    return L[kind]


def own_tex(k, el):
    """the textures a form paints for itself (its new parts' and its painted replacements): name -> PIL image"""
    out = {}
    for n, fn in TEXLIB.items(): out[n] = fn
    for n, fn in DESIGNS[k][el].get('paint', {}).items(): out[n] = fn
    return out


def build(k, el, model, els, textures):
    """a bone's twin: (elements kept and recoloured by the caller, + the new ones, the texture keys the new ones use)"""
    b = bone_of(k, model)
    D = DESIGNS[k][el]
    if b is None: return els, set()
    drop = D.get('drop', {}).get(b, ())
    def gone(e):
        names = [textures.get(f.get('texture', '#')[1:], '').split('/')[-1] for f in e.get('faces', {}).values()]
        for d in drop:                                              # (a stem, or (stem, y): only those of its elements from y up)
            stem, y = (d, None) if isinstance(d, str) else d
            if any(n.startswith(stem) for n in names) and (y is None or min(e['from'][1], e['to'][1]) >= y): return True
        return False
    keep = [e for e in els if not gone(e)]
    if b in D.get('keep_only', {}):
        keep = []
    fn = D.get('parts', {}).get(b)
    new = fn(Bone(els, textures)) if fn else []
    used = {f['texture'][1:] for e in new for f in e['faces'].values()}
    return keep + new, used


def _corners(e):
    """what the game checks of an element against the model box: its from and to"""
    return [e['from'], e['to']]
