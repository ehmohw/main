"""3.0g (redo): each of elemforms.py's ten followers, designed for each form (the kit and how it rides: elemforms_art.py).

Per follower: pre (its models' prefix) and, per form ('e' Ethereal, 'w' Wraithfire):
  pal    its own palettes for the recolour (base / accent / glow; elemforms_art.PAL is the default)
  tex    per texture stem: a palette of its own (dict; 'L' its light), or a painter (im -> im)
  parts  per bone: the new parts built onto it (builder(B) -> elements, in the bone's model space)
  drop   per bone: textures whose elements go (redrawn by the parts)
  keep_only  per bone: nothing of the bone's own stays (the parts replace it whole)
  paint  its own textures for the new parts (name -> painter())
Model space: the joint at (8, 8, 8), front -z, his right +x; y up. Every point inside -16..32."""
import math

import elemforms_art as A
from elemforms_art import (crystal, tongue, flick, ring, rays, wing, line_wing, plume, crescent, zigzag, box, beam, mirror,
                           recolour, outline_t, crystal_t, grad_t, flame_t)
import numpy as np
from PIL import Image

E, W = 'e', 'w'
CRYS = ('x_cwhite', 'x_cice', 'x_clilac', 'x_crose', 'x_caqua')


def _side(B):
    """a limb bone's side: +1 his right (its bounds lie to +x of the joint), -1 his left"""
    return 1 if B.c[0] >= 8 else -1


# ---------------------------------------------------------------------------------------------------- the ghost (the Eraser's)
def ghost(line='#7af0ff', keep_dark=False, keep_light=False, fill='#0b161e'):
    """a texture turned to an ERASED ghost's: its outline dashed in soul light, its middle gone - but its darkest marks (eyes)
    or its lightest (the sleeve's letters) kept, lit"""
    def paint(im):
        a = np.asarray(im.convert('RGBA')).astype(float) / 255
        H, Wd = a.shape[:2]
        n = max(1, Wd // 16)
        yy, xx = np.mgrid[0:H, 0:Wd]
        gx, gy = xx // n, yy // n
        edge = (gx == 0) | (gx == 15) | (gy == 0) | (gy == 15)
        dash = ((gx + gy) // 2) % 2 == 0
        out = np.zeros((H, Wd, 4)); out[..., :3] = np.array(A._rgb(fill)) / 255; out[..., 3] = a[..., 3]
        on = edge & dash & (a[..., 3] > 0)
        out[on, :3] = np.array(A._rgb(line)) / 255
        L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
        vis = a[..., 3] > 0
        if vis.any() and (keep_dark or keep_light):
            lo, hi = np.percentile(L[vis], 5), np.percentile(L[vis], 95)
            m = (L < lo + 0.12 * (hi - lo)) if keep_dark else (L > lo + 0.72 * (hi - lo))
            m &= vis
            c = np.array([0.88, 1.0, 1.0]) if keep_dark else np.array([0.48, 0.94, 1.0])
            out[m, :3] = c; out[m, 3] = 1.0
        return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype('uint8'), 'RGBA')
    return paint


def hotrod(im):
    """Donado's shirt, Wraithfire: charcoal, with hot-rod flames of soul fire licking up from its hem"""
    a = np.asarray(im.convert('RGBA')).astype(float) / 255
    H, Wd = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:Wd]
    u, v = xx / Wd, 1 - yy / H                                      # (v 0 at the hem)
    edge = 0.42 + 0.16 * np.sin(u * math.pi * 6) + 0.06 * np.sin(u * math.pi * 14 + 1)
    base = np.array([0.08, 0.1, 0.13])
    f = np.clip((edge - v) / 0.42, 0, 1)[..., None]
    fire = np.array([0.04, 0.42, 0.66]) * (1 - f) + np.array([0.7, 0.98, 1.0]) * f
    rgb = np.where((v < edge)[..., None], fire, base)
    rim = (np.abs(v - edge) < 0.05)[..., None]
    rgb = np.where(rim, np.array([0.85, 1.0, 1.0]), rgb)
    o = np.concatenate([rgb, a[..., 3:4]], -1)
    return Image.fromarray((np.clip(o, 0, 1) * 255 + 0.5).astype('uint8'), 'RGBA')


def holo(im):
    """Donado's shirt, Ethereal: a holographic tee - its folds kept, every colour sliding across it"""
    base = recolour(im, ['#c8c0f0', '#f4f0ff', '#ffffff'], sheen=0.25)
    a = np.asarray(base).astype(float) / 255
    H, Wd = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:Wd]
    import colorsys
    h = ((xx + yy * 0.6) / (Wd * 1.1)) % 1.0
    rb = np.stack(np.vectorize(lambda q: colorsys.hls_to_rgb(q, 0.74, 0.85))(h), -1)
    a[..., :3] = a[..., :3] * 0.45 + rb * 0.55
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype('uint8'), 'RGBA')


def prism(ramp=('#6a5aa8', '#c8b8ff', '#ffffff'), k=0.55):
    """a texture as stained glass: its own shading, every colour across it"""
    def paint(im):
        base = recolour(im, list(ramp), sheen=0.2)
        a = np.asarray(base).astype(float) / 255
        H, Wd = a.shape[:2]
        yy, xx = np.mgrid[0:H, 0:Wd]
        import colorsys
        h = ((xx * 1.0 + yy * 0.5) / (Wd * 1.2)) % 1.0
        rb = np.stack(np.vectorize(lambda q: colorsys.hls_to_rgb(q, 0.6, 0.9))(h), -1)
        a[..., :3] = a[..., :3] * (1 - k) + rb * k * (0.5 + 0.5 * a[..., :3].mean(-1, keepdims=True))
        return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype('uint8'), 'RGBA')
    return paint


# ==================================================================================================== BENDER - the dog
def _bender_e_body(B):
    out = []
    for sd, x in ((1, B.hi[0] - 0.3), (-1, B.lo[0] + 0.3)):          # (little seraph wings at his shoulders)
        out += wing((x, B.hi[1] - 1.0, 4.2), sd, 0.5, ('x_cwhite', 'x_cice', 'x_clilac', 'x_crose', 'x_caqua'), 'x_cwhite', 10, 13)
    return out


def _bender_e_head(B):
    out = ring((8.0, B.hi[1] + 3.0, 6.8), 2.8, 12, 0.6, 'x_gold', 14)
    tips = B.of('bd_tip')
    if tips:
        for lo, hi in tips[3]:
            x = (lo[0] + hi[0]) / 2
            out += crystal((x, hi[1] - 0.6, 6.75), (x + (0.5 if x > 8 else -0.5), hi[1] + 2.6, 7.0), 1.2, 'x_cice', 12, 14)
    return out


def _bender_e_tail(B):
    t = B.highest()
    return (crystal((t[0], t[1] - 0.8, t[2] - 0.3), (t[0], t[1] + 4.2, t[2] + 3.0), 1.6, 'x_clilac', 11, 14) +
            crystal((t[0], t[1] - 0.8, t[2] - 0.3), (t[0] + 2.0, t[1] + 3.2, t[2] + 3.4), 1.3, 'x_caqua', 11, 14) +
            crystal((t[0], t[1] - 0.8, t[2] - 0.3), (t[0] - 2.0, t[1] + 3.2, t[2] + 3.4), 1.3, 'x_crose', 11, 14))


def _bender_e_leg(B):
    (x0, x1), (z0, z1) = (B.lo[0], B.hi[0]), (B.lo[2], B.hi[2])
    return [box((x0 - 0.25, 1.7, z0 - 0.25), (x1 + 0.25, 2.5, z1 + 0.25), 'x_gold', 13)]


def _bender_w_body(B):
    out = []
    for z, h in zip((0.8, 3.4, 6.0, 8.6, 11.2), (5.2, 6.0, 5.4, 4.4, 3.4)):
        out += tongue((8.0, B.hi[1] - 0.6, z), h, 2.6, (0.0, 0.0, 0.55))
    return out


def _bender_w_head(B):
    out = []
    tips = B.of('bd_tip')
    if tips:
        for lo, hi in tips[3]:
            x = (lo[0] + hi[0]) / 2
            out += tongue((x, hi[1] - 1.4, 6.75), 4.2, 1.6, (0.25 if x > 8 else -0.25, 0.0, 0.45))
    return out


def _bender_w_tail(B):
    t = B.highest()
    return tongue((t[0], t[1] - 1.2, t[2] - 0.2), 7.5, 3.0, (0.0, 0.0, 0.5))


def _bender_w_leg(B):
    c = ((B.lo[0] + B.hi[0]) / 2, 0.4, B.hi[2] - 0.6)
    return tongue(c, 3.2, 2.0, (0.0, 0.0, 0.9))


BENDER = dict(pre='bd_', **{
    E: dict(pal=dict(base=dict(ramp=['#8c86c8', '#cbc6ef', '#f4f0ff', '#ffffff'], keep=0.3, ink='#2a2c6e', sheen=0.3)),
            tex={'bd_tip': dict(ramp=['#7ad8f0', '#ffffff'], L=13), 'bd_ear_in': dict(ramp=['#f0a8d8', '#ffe8f8'], L=11)},
            parts={'body': _bender_e_body, 'head': _bender_e_head, 'tail': _bender_e_tail,
                   **{l: _bender_e_leg for l in ('legfr', 'legfl', 'legbr', 'legbl')}}),
    W: dict(tex={'bd_face': dict(ramp=['#05090d', '#0e1c26', '#1a3442', '#2e6274'], ink='#8af4ff', ink_at=0.3, L=12), 'bd_tip': dict(ramp=['#1aa8d8', '#c8fcff'], L=15), 'bd_ear_in': dict(ramp=['#0a5a78', '#3ad0ea'], L=10),
                 'bd_back': dict(ramp=['#05090d', '#0e1c26', '#1e4a5a', '#3ad0ea'])},
            parts={'body': _bender_w_body, 'head': _bender_w_head, 'tail': _bender_w_tail,
                   **{l: _bender_w_leg for l in ('legfr', 'legfl', 'legbr', 'legbl')}}),
})


# ==================================================================================================== MR. CAPSHUN - the stick figure
def _cap_quill(B, flame=False):
    b, a = (B.lo[0] + 0.4, B.lo[1] + 0.4, 8.0), (B.hi[0] - 0.4, B.hi[1] - 0.4, 8.0)
    d = tuple(b[i] - a[i] for i in range(3))
    P = lambda f: tuple(a[i] + d[i] * f for i in range(3))
    if flame:
        return []
    out = [beam(P(0.0), P(0.16), 0.55, 'x_gold', 14, diamond=True), beam(P(0.12), P(1.02), 0.45, 'x_gold', 13)]
    n = (-d[1], d[0], 0.0); L = math.hypot(*n[:2]); n = (n[0] / L, n[1] / L, 0.0)
    for i in range(6):                                              # (the vane: barbs either side of the shaft, longest mid-way)
        f = 0.34 + 0.11 * i
        w = 2.4 * math.sin(math.pi * (f - 0.3) / 0.75) + 0.4
        for sd in (1, -1):
            p = P(f); q = tuple(p[j] + n[j] * w * sd + d[j] * 0.12 for j in range(3))
            out.append(beam(p, q, 0.9, ('x_cwhite', 'x_cice')[i % 2], 12, t=0.3, up=(0.0, 0.0, 1.0)))
    return out


def _cap_e_body(B):
    out = []
    for sd in (1, -1):
        out += line_wing((8.0 + 0.5 * sd, B.hi[1] - 1.4, 8.6), sd, 0.62, 'x_gold', 14)
    return out


def _cap_w_head(B):
    top = (B.c[0], B.hi[1] - 0.8, 8.0)
    out = plume(top, 3, 6.0, 2.6, 2.8, back=0.15, lean_x=0.5)
    out += zigzag((B.c[0], B.c[1], 8.9), 5.6, 7.2, 18, 0.55, 'x_soul', 14)
    return out


def _cap_w_tool(B):
    t = (B.lo[0] + 0.9, B.lo[1] + 0.9, 8.0)
    return flick(t, (-0.7, -0.5, 0.0), 4.5, 1.9, curl=(0.0, 0.9, 0.0))


def _cap_w_shin(B):
    f = B.lowest()
    return flick((f[0], f[1] + 0.6, f[2] + 0.2), (0.0, 0.25, 1.0), 3.4, 1.4, curl=(0.0, 0.5, 0.0))


CAPSHUN = dict(pre='mz_', **{
    E: dict(tex={'mz_ink': dict(ramp=['#d8a838', '#fff0b0', '#ffffff'], L=13), 'mz_face': dict(ramp=['#e8e2ff', '#ffffff'], ink='#30307a', ink_at=0.45),
                 'mz_back': dict(ramp=['#ece6ff', '#ffffff']), 'mz_sk_': dict(ramp=['#d8a838', '#fff0b0', '#ffffff'], L=13)},
            parts={'head': lambda B: ring((B.c[0], B.hi[1] + 1.9, 8.2), 3.4, 14, 0.6, 'x_gold', 15, tilt=-14),
                   'body': _cap_e_body, 'tool': _cap_quill},
            drop={'tool': ('mz_t_',)}),
    W: dict(tex={'mz_ink': dict(ramp=['#0a6fa8', '#2fd2f2', '#c8fcff'], L=15), 'mz_face': dict(ramp=['#0e1c26', '#1a3442'], ink='#7af0ff', ink_at=0.45, L=8),
                 'mz_back': dict(ramp=['#0a141c', '#1a3442']), 'mz_t_': dict(ramp=['#05090d', '#1a3442', '#3ad0ea'], L=10),
                 'mz_sk_': dict(ramp=['#0a6fa8', '#2fd2f2', '#c8fcff'], L=15)},
            parts={'head': _cap_w_head, 'tool': _cap_w_tool, 'shinr': _cap_w_shin, 'shinl': _cap_w_shin}),
})


# ==================================================================================================== THE BOUND SOVEREIGN
def _sov_e_head(B):
    c = (8.0, (B.lo[1] + B.hi[1]) / 2 + 1.0, min(31.0, B.hi[2] + 1.6))
    out = rays(c, 7.0, 12.4, 11, 1.4, 'x_cgold', 14, arc=(-20, 200))
    out += ring(c, 7.0, 18, 0.8, 'x_gold', 15, plane='xy', t=0.6)
    return out


def _sov_e_chest(B):
    out = []
    for sd, x in ((1, B.hi[0] - 2.2), (-1, B.lo[0] + 2.2)):
        out += crystal((x, B.hi[1] - 2.0, 8.6), (x + 2.2 * sd, B.hi[1] + 4.6, 9.6), 2.4, 'x_cwhite', 12, 14)
        out += crystal((x - 1.3 * sd, B.hi[1] - 2.2, 10.2), (x + 0.4 * sd, B.hi[1] + 2.8, 12.2), 1.7, 'x_cice', 12, 14)
    return out


def _sov_w_head(B):
    top = (8.0, B.hi[1] - 3.0, (B.lo[2] + B.hi[2]) / 2 + 1.0)
    return plume(top, 5, 11.0, 3.4, 4.2, back=0.3, lean_x=0.5)


def _sov_w_chest(B):
    out = []
    for sd, x in ((1, B.hi[0] - 2.4), (-1, B.lo[0] + 2.4)):        # (soul fire pouring up off his pauldrons)
        out += tongue((x, B.hi[1] - 2.2, 9.0), 9.0, 3.6, (0.35 * sd, 0.0, 0.35))
        out += tongue((x - 2.6 * sd, B.hi[1] - 2.4, 10.4), 6.4, 2.6, (0.2 * sd, 0.0, 0.5))
    return out


SOVEREIGN = dict(pre='ds_', **{
    E: dict(pal=dict(base=dict(ramp=['#9aa0c4', '#d0d6ee', '#f0f3ff', '#ffffff'], keep=0.0, sheen=0.3, flatten=0.85, ink=None)),
            tex={'ds_red': dict(ramp=['#f0b840', '#fff4c0', '#ffffff'], L=14), 'ds_eye': dict(ramp=['#9af4ff', '#ffffff'], L=15),
                 'ds_beye': dict(ramp=['#9af4ff', '#ffffff'], L=15), 'ds_heart': dict(ramp=['#ff9ad8', '#ffffff'], L=15),
                 'ds_horn': dict(ramp=['#5a9ad8', '#a8e0ff', '#ffffff'], sheen=0.5, flatten=0.8, L=12), 'ds_membrane': prism(('#8a84c8', '#d8d0ff', '#ffffff'), 0.35),
                 'ds_chain': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=11), 'ds_glass': dict(ramp=['#9ae4ff', '#ffffff'], L=13),
                 'ds_wbone': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=11), 'ds_edge': dict(ramp=['#b8c0e0', '#f4f6ff'], flatten=0.9, L=9),
                 'ds_dark': dict(ramp=['#8088b8', '#b8c0e4', '#e4e8ff'], flatten=0.9), 'ds_iron': dict(ramp=['#b8c0e0', '#f4f6ff'], flatten=0.9)},
            parts={'head': _sov_e_head, 'chest': _sov_e_chest}),
    W: dict(tex={'ds_red': dict(ramp=['#1aa8d8', '#8af4ff', '#ffffff'], L=14), 'ds_eye': dict(ramp=['#5ae6ff', '#ffffff'], L=15),
                 'ds_beye': dict(ramp=['#5ae6ff', '#ffffff'], L=15), 'ds_heart': dict(ramp=['#5ae6ff', '#ffffff'], L=15),
                 'ds_membrane': dict(ramp=['#03070b', '#0c2836', '#1a6a84'], L=6), 'ds_horn': dict(ramp=['#05090d', '#14303c', '#3ad0ea'], L=8),
                 'ds_chain': dict(ramp=['#0a5a78', '#3ad0ea', '#c8fcff'], L=12), 'ds_glass': dict(ramp=['#1aa8d8', '#c8fcff'], L=14),
                 'ds_edge': dict(ramp=['#0a141c', '#1a3442'], flatten=0.9)},
            parts={'head': _sov_w_head, 'chest': _sov_w_chest}),
})


# ==================================================================================================== THE KEEPER OF BONDS
def _kb_e_head(B):
    out = []
    zf = B.lo[2] + 2.0
    for x, h in zip((5.6, 6.8, 8.0, 9.2, 10.4), (2.0, 3.0, 4.4, 3.0, 2.0)):
        out += crystal((x, B.hi[1] - 0.8, zf), (x + (x - 8) * 0.25, B.hi[1] - 0.8 + h, zf + 0.4), 1.1, 'x_cwhite' if x == 8 else 'x_crose', 12, 14)
    c = (8.0, (B.lo[1] + B.hi[1]) / 2 + 1.0, B.hi[2] + 1.0)
    out += ring(c, 6.4, 18, 1.0, 'x_gold', 15, plane='xy')
    for i in range(6):                                              # (six spindles of crystal set round the halo)
        a = math.radians(i * 60 + 90)
        p = (c[0] + 6.4 * math.cos(a), c[1] + 6.4 * math.sin(a), c[2])
        q = (c[0] + 8.6 * math.cos(a), c[1] + 8.6 * math.sin(a), c[2])
        out += crystal(p, q, 1.5, CRYS[i % 5], 13, 15)
    return out


def _kb_e_body(B):
    out = []
    for i in range(6):                                              # (prisms hanging round her in the air)
        a = math.radians(30 + 60 * i)
        x, z = 8 + 10.5 * math.cos(a), 8 + 10.5 * math.sin(a)
        y = 10.5 + (1.2 if i % 2 else -0.6)
        out += crystal((x, y, z), (x, y + 3.6, z), 2.2, CRYS[i % 5], 13, 15) + crystal((x, y, z), (x, y - 2.8, z), 2.2, CRYS[i % 5], 13, 15)
    return out


def _kb_w_head(B):
    c = (8.0, (B.lo[1] + B.hi[1]) / 2 + 1.0, B.hi[2] + 1.0)
    out = ring(c, 6.4, 18, 0.7, 'x_soul', 15, plane='xy')
    for i in range(7):
        a = math.radians(10 + 160 * i / 6)
        d = (math.cos(a), math.sin(a), 0.25)
        p = (c[0] + 6.4 * math.cos(a), c[1] + 6.4 * math.sin(a), c[2])
        out += flick(p, d, 3.6 if i % 2 == 0 else 2.6, 1.7, curl=(0.0, 0.5, 0.0))
    return out


def _kb_w_skirt(B):
    out = []
    for i in range(8):
        a = math.radians(22.5 + 45 * i)
        rx, rz = (B.hi[0] - B.lo[0]) / 2 + 0.4, (B.hi[2] - B.lo[2]) / 2 + 0.4
        p = (B.c[0] + rx * math.cos(a), B.lo[1] + 0.4, B.c[2] + rz * math.sin(a))
        out += tongue(p, 5.4 if i % 2 else 4.2, 2.2, (0.3 * math.cos(a), 0.0, 0.3 * math.sin(a)))
    return out


KEEPER = dict(pre='kb_', **{
    E: dict(pal=dict(base=dict(ramp=['#8a84c0', '#d0ccf0', '#f6f4ff', '#ffffff'], keep=0.7, ink='#2a2c6e', sheen=0.3)),
            tex={'kb_wing': prism(('#7a70c0', '#d8d0ff', '#ffffff'), 0.5), 'kb_tier': dict(ramp=['#b0a8e0', '#f0ecff', '#ffffff'], keep=0.9, sheen=0.3),
                 'kb_brd': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12), 'kb_rim': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12), 'kb_gold': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12),
                 'kb_bonds': dict(ramp=['#f0c0ff', '#ffffff'], keep=0.8, L=14), 'kb_light': dict(ramp=['#fff8d8', '#ffffff'], L=15),
                 'kb_eyes': dict(ramp=['#2a3a9a', '#9ae4ff'], L=12)},
            parts={'head': _kb_e_head, 'body': _kb_e_body}),
    W: dict(tex={'kb_wing': dict(ramp=['#03070b', '#0c2836', '#1e6e88', '#5ae6ff'], L=7), 'kb_gold': dict(ramp=['#0a5a78', '#3ad0ea', '#c8fcff'], L=12),
                 'kb_bonds': dict(ramp=['#1aa8d8', '#c8fcff'], L=15), 'kb_light': dict(ramp=['#5ae6ff', '#ffffff'], L=15),
                 'kb_eyes': dict(ramp=['#5ae6ff', '#ffffff'], L=15), 'kb_face': dict(ramp=['#2a4450', '#5a8494'], ink='#8af4ff', ink_at=0.35, L=8),
                 'kb_hair': dict(ramp=['#0a3a4c', '#2fb8d8', '#c8fcff'], L=11)},
            parts={'head': _kb_w_head, 'skirt': _kb_w_skirt}),
})


# ==================================================================================================== THE ARACHNO-LANTERN
def _ln_e_head(B):
    st = B.of('ln_stem')
    c = st[2] if st else (8.0, B.hi[1], 7.7)
    y0 = (st[0][1] if st else B.hi[1] - 1.0)
    out = crystal((c[0], y0, c[2]), (c[0], y0 + 12.0, c[2]), 3.6, 'x_cwhite', 13, 15)
    for i in range(6):                                              # (a crown of crystals round it, leaning out like petals)
        a = math.radians(i * 60 + 30)
        d = (math.cos(a), 0.0, math.sin(a))
        p = (c[0] + d[0] * 2.4, y0 - 0.4, c[2] + d[2] * 2.4)
        out += crystal(p, (p[0] + d[0] * 6.0, y0 + 7.0, p[2] + d[2] * 6.0), 2.6, ('x_cice', 'x_cwhite')[i % 2], 12, 14)
    for x in (-11.0, 27.0):                                         # (a crystal seed floating at either side)
        out += crystal((x, 18.0, 7.7), (x, 22.5, 7.7), 2.0, 'x_camber', 13, 15) + crystal((x, 18.0, 7.7), (x, 14.5, 7.7), 2.0, 'x_camber', 13, 15)
    return out


def _ln_e_leg(B):
    f = B.lowest()
    return crystal((f[0], f[1] + 1.4, f[2]), (f[0], max(-15.9, f[1] - 2.4), f[2]), 1.6, 'x_cice', 12, 14)


def _ln_w_head(B):
    st = B.of('ln_stem')
    c = st[2] if st else (8.0, B.hi[1], 7.7)
    y0 = (st[0][1] if st else B.hi[1] - 1.0)
    out = []
    for i, (dx, L, w) in enumerate(((0.0, 16.0, 4.6), (-4.6, 12.5, 3.4), (4.6, 12.5, 3.4), (-8.4, 8.5, 2.6), (8.4, 8.5, 2.6))):
        out += flick((c[0] + dx, y0 - 1.0, c[2] - 1.5), (dx * 0.05, 1.0, 0.55), L * 0.9, w * 1.2, curl=(0.0, 0.1, 0.25))
    return out


def _ln_w_leg(B):
    k = B.highest()
    return tongue((k[0], k[1] - 1.0, k[2]), 4.6, 2.2, (0.0, 0.0, 0.2))


LANTERN = dict(pre='ln_', **{
    E: dict(pal=dict(base=dict(ramp=['#9a3a6a', '#d06a94', '#f4a8c0', '#ffe4ec'], keep=0.0, ink='#fffbe8', sheen=0.45, flatten=0.7)),
            tex={'ln_face': dict(ramp=['#9a3a6a', '#d06a94', '#f4a8c0', '#ffe4ec'], ink='#fff6c8', ink_at=0.38, sheen=0.4, flatten=0.5, L=12),
                 'ln_flame': dict(ramp=['#fff0b0', '#ffffff'], L=15), 'ln_tongue': dict(ramp=['#ff9ad8', '#ffe8f8'], L=12),
                 'ln_leg': dict(ramp=['#8a84c0', '#d4d0f0', '#ffffff'], sheen=0.3, flatten=0.9)},
            parts={'head': _ln_e_head, **{f'leg{s}{i}': _ln_e_leg for s in 'lr' for i in range(4)}},
            drop={'head': ('ln_stem', 'ln_leaf')}),
    W: dict(tex={'ln_face': dict(ramp=['#05090d', '#0e1c26', '#1a3442'], ink='#8af4ff', L=12), 'ln_rind': dict(ramp=['#05090d', '#0e1c26', '#1a3442', '#2a5464']),
                 'ln_flame': dict(ramp=['#3ad0ea', '#ffffff'], L=15), 'ln_tongue': dict(ramp=['#1aa8d8', '#c8fcff'], L=15),
                 'ln_leg': dict(ramp=['#05090d', '#101c24', '#2a4450'])},
            parts={'head': _ln_w_head, **{f'leg{s}{i}': _ln_w_leg for s in 'lr' for i in range(4)}},
            drop={'head': ('ln_stem', 'ln_leaf')}),
})


# ==================================================================================================== LEO - the knight
def _leo_e_head(B):
    out = []
    for z, h in zip((B.lo[2] + 1.2, B.lo[2] + 3.4, B.lo[2] + 5.6, B.lo[2] + 7.8), (3.0, 4.6, 4.2, 3.0)):
        out += crystal((8.0, B.hi[1] - 0.5, z), (8.0, B.hi[1] - 0.5 + h, z + h * 0.7), 1.3, 'x_caqua', 12, 14)
    return out


def _leo_shoulder(B, tex, flame=False):
    sd = _side(B)
    x = B.hi[0] - 0.8 if sd > 0 else B.lo[0] + 0.8
    p = (x, B.hi[1] - 0.8, B.c[2])
    if flame:
        return tongue(p, 4.4, 2.4, (0.35 * sd, 0.0, 0.3))
    out = []
    for dz, up, L in ((0.0, 1.0, 4.6), (-2.2, 0.7, 3.4), (2.2, 0.7, 3.4)):
        out += crystal((p[0] - sd * 1.2, p[1] - 0.6, p[2] + dz * 0.5), (p[0] + sd * L * 0.75, p[1] + L * up, p[2] + dz), 1.8, tex, 12, 14)
    return out


TINE_Y = 22.9


def _leo_e_tri(B):
    y0 = TINE_Y
    out = crystal((8.0, y0 - 0.5, 8.0), (8.0, y0 + 11.5, 8.0), 2.0, 'x_caqua', 13, 15)
    for sd in (1, -1):
        out.append(beam((8.0, y0 + 0.4, 8.0), (8.0 + 3.4 * sd, y0 + 2.2, 8.0), 1.1, 'x_gold', 13, diamond=True))
        out += crystal((8.0 + 3.4 * sd, y0 + 1.6, 8.0), (8.0 + 4.6 * sd, y0 + 9.0, 8.0), 1.6, 'x_cice', 13, 15)
    return out


def _leo_w_head(B):
    out = []
    for z, h in zip((B.lo[2] + 2.0, B.lo[2] + 4.4, B.lo[2] + 6.8), (5.0, 6.2, 5.0)):
        out += tongue((8.0, B.hi[1] - 0.6, z), h, 2.6, (0.0, 0.0, 0.7))
    return out


def _leo_w_tri(B):
    y0 = TINE_Y
    out = tongue((8.0, y0 - 0.4, 8.0), 11.0, 2.6, (0.0, 0.0, 0.0))
    for sd in (1, -1):
        out.append(beam((8.0, y0 + 0.4, 8.0), (8.0 + 3.4 * sd, y0 + 2.0, 8.0), 1.1, 'x_iron', 12, diamond=True))
        out += tongue((8.0 + 3.4 * sd, y0 + 1.4, 8.0), 8.0, 2.0, (0.14 * sd, 0.0, 0.0))
    return out


LEO = dict(pre='le_', **{
    E: dict(pal=dict(base=dict(ramp=['#6a84b0', '#b4cce8', '#eaf4ff', '#ffffff'], keep=0.45, ink='#22306a', sheen=0.4)),
            tex={'le_tunic': dict(ramp=['#2a9ab0', '#7ae0e0', '#d8fff8'], sheen=0.3), 'le_cape': dict(ramp=['#2a9ab0', '#7ae0e0', '#d8fff8']),
                 'le_emblem': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=13), 'le_gem': dict(ramp=['#7ae0ff', '#ffffff'], L=15),
                 'le_gold': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12)},
            parts={'head': _leo_e_head, 'armr': lambda B: _leo_shoulder(B, 'x_caqua'), 'arml': lambda B: _leo_shoulder(B, 'x_caqua'),
                   'trident': _leo_e_tri},
            drop={'trident': (('le_tri', 22.9),)}),
    W: dict(tex={'le_face': dict(ramp=['#a8c8d0', '#e0f4f8'], ink='#5ae6ff', L=6), 'le_skin': dict(ramp=['#8aa8b4', '#d0e8f0']),
                 'le_tunic': dict(ramp=['#05090d', '#0c2836', '#1e6e88']), 'le_emblem': dict(ramp=['#1aa8d8', '#c8fcff'], L=15),
                 'le_gem': dict(ramp=['#5ae6ff', '#ffffff'], L=15), 'le_gold': dict(ramp=['#0a5a78', '#3ad0ea', '#c8fcff'], L=12),
                 'le_rim': dict(ramp=['#0a5a78', '#3ad0ea'], L=10)},
            parts={'head': _leo_w_head, 'armr': lambda B: _leo_shoulder(B, None, True), 'arml': lambda B: _leo_shoulder(B, None, True),
                   'trident': _leo_w_tri},
            drop={'trident': (('le_tri', 22.9),)}),
})


# ==================================================================================================== CELI - the ice girl
def _celi_e_head(B):
    out = []
    zf = B.lo[2] + 2.6
    for x, h in zip((5.0, 6.5, 8.0, 9.5, 11.0), (3.0, 4.6, 6.6, 4.6, 3.0)):
        out += crystal((x, B.hi[1] - 1.0, zf), (x + (x - 8) * 0.35, B.hi[1] - 1.0 + h, zf - 0.2), 1.4, 'x_cice' if x != 8 else 'x_cwhite', 13, 15)
    out += crescent((8.0, B.hi[1] + 10.5, B.c[2] + 1.0), 4.2, 200, 340, 2.2, 'x_cgold', 15, n=10)          # (a little moon, floating over her crown)
    return out


def _celi_e_body(B):
    out = []
    for sd in (1, -1):
        out += wing((8.0 + 2.0 * sd, B.hi[1] - 5.0, B.hi[2] - 1.2), sd, 0.85, ('x_cice', 'x_cwhite', 'x_cice', 'x_clilac', 'x_cwhite'), 'x_cwhite', 11, 14, sweep=0.8)
    return out


def _celi_e_spear(B):
    t = B.of('ce_ice')
    y0 = t[0][1] if t else 26.0
    out = crystal((8.0, y0 - 0.4, 8.0), (8.0, 31.9, 8.0), 1.6, 'x_cwhite', 13, 15)
    out += crescent((8.0, y0 + 0.2, 8.0), 4.6, 200, 340, 2.0, 'x_cice', 14, n=8, plane='xy')
    return out


def _celi_w_head(B):
    out = []
    for i, x in enumerate((3.0, 5.4, 8.0, 10.6, 13.0)):
        out += tongue((x, B.hi[1] - 2.2, B.c[2] + 1.6), (5.2, 6.8, 8.0, 6.8, 5.2)[i], 3.0, ((x - 8) * 0.05, 0.0, 0.8))
    return out


def _celi_w_body(B):
    out = []
    for p, h in (((B.lo[0] - 5.0, B.hi[1] - 2.0, B.hi[2] + 1.0), 4.4), ((B.hi[0] + 5.0, B.hi[1] - 2.0, B.hi[2] + 1.0), 4.4),
                 ((B.lo[0] - 3.0, B.lo[1] + 2.0, B.hi[2] + 2.0), 3.0), ((B.hi[0] + 3.0, B.lo[1] + 2.0, B.hi[2] + 2.0), 3.0)):
        out += crystal(p, (p[0], p[1] + h, p[2]), 1.8, 'x_scrys', 14, 15) + crystal(p, (p[0], p[1] - h * 0.7, p[2]), 1.8, 'x_scrys', 14, 15)
    return out


def _celi_w_spear(B):
    t = B.of('ce_ice')
    y0 = t[0][1] if t else 26.0
    return tongue((8.0, y0 - 0.6, 8.0), 31.9 - y0, 2.6, (0.0, 0.0, 0.0))


CELI = dict(pre='ce_', **{
    E: dict(pal=dict(base=dict(ramp=['#6a7cc8', '#a8c4f0', '#dceaff', '#ffffff'], keep=0.5, ink='#24306e', sheen=0.35)),
            tex={'ce_hair': dict(ramp=['#8a7ac8', '#c8c0f0', '#f0eeff', '#ffffff'], keep=0.0, sheen=0.4), 'ce_moon': dict(ramp=['#fff0b0', '#ffffff'], L=15),
                 'ce_star': dict(ramp=['#fff0b0', '#ffffff'], L=15), 'ce_band': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12)},
            parts={'head': _celi_e_head, 'body': _celi_e_body, 'spear': _celi_e_spear},
            drop={'spear': ('ce_ice',)}),
    W: dict(tex={'ce_hair': dict(ramp=['#0a6fa8', '#2fd2f2', '#c8fcff'], L=14), 'ce_face': dict(ramp=['#a8c8d0', '#e0f4f8'], ink='#3ad0ea'),
                 'ce_skin': dict(ramp=['#8aa8b4', '#d0e8f0']), 'ce_moon': dict(ramp=['#3ad0ea', '#ffffff'], L=15), 'ce_star': dict(ramp=['#3ad0ea', '#ffffff'], L=15),
                 'ce_band': dict(ramp=['#0a5a78', '#3ad0ea'], L=12)},
            parts={'head': _celi_w_head, 'body': _celi_w_body, 'spear': _celi_w_spear},
            drop={'spear': ('ce_ice',)}),
})


# ==================================================================================================== DEMOCRATUS - the storm's reaper
BLADE = ((8.6, 23.4), (13.0, 25.4), (17.6, 24.8), (21.4, 22.2), (24.0, 18.2), (25.0, 13.6), (24.4, 9.4))


def _demo_blade(flame):
    out = []
    n = len(BLADE) - 1
    for i in range(n):
        a, b = (BLADE[i][0], BLADE[i][1], 8.0), (BLADE[i + 1][0], BLADE[i + 1][1], 8.0)
        w = 3.4 * (1 - i / n) + 0.5
        tex = ('x_flame' if i < 3 else 'x_flame_hot') if flame else ('x_cice' if i % 2 else 'x_cwhite')
        out.append(beam(a, b, w, tex, 15 if flame else 13, t=0.5, up=(0.0, 0.0, 1.0), ext=0.3))
        if not flame:                                               # (its cutting edge: a bright line along the inside)
            ia = (a[0] - 0.4, a[1] - w / 2 + 0.2, 8.0); ib = (b[0] - 0.4, b[1] - w / 2 + 0.6, 8.0)
            out.append(beam(ia, ib, 0.45, 'x_light', 15, t=0.7, up=(0.0, 0.0, 1.0)))
    if flame:
        for i in (1, 2, 3):
            out += tongue((BLADE[i][0], BLADE[i][1] + 0.6, 8.0), min(5.0, 31.5 - BLADE[i][1]), 1.8, (0.25, 0.0, 0.0))
    return out


def _demo_e_head(B):
    return zigzag((8.0, (B.lo[1] + B.hi[1]) / 2 + 1.0, B.hi[2] + 1.0), 5.8, 8.6, 16, 1.2, 'x_cgold', 15, arc=(-30, 210))


def _demo_e_body(B):
    out = []
    for sd, x in ((1, B.hi[0] - 1.0), (-1, B.lo[0] + 1.0)):
        out += crystal((x, B.hi[1] - 1.4, 8.0), (x + 3.6 * sd, B.hi[1] + 3.4, 8.4), 2.0, 'x_cwhite', 12, 14)
        out += crystal((x - 0.8 * sd, B.hi[1] - 1.6, 9.6), (x + 1.8 * sd, B.hi[1] + 2.2, 11.6), 1.5, 'x_cice', 12, 14)
    return out


def _demo_w_body(B):
    out = []
    for sd, x in ((1, B.hi[0] - 1.4), (-1, B.lo[0] + 1.4)):
        out += tongue((x, B.hi[1] - 1.2, 8.6), 4.6, 2.4, (0.3 * sd, 0.0, 0.5))
    return out


def _demo_w_cape(B):
    out = []
    for i, x in enumerate((2.4, 5.2, 8.0, 10.8, 13.6)):
        out += tongue((x, B.lo[1] + 0.4, B.hi[2] + 0.3), (5.0, 6.6, 7.6, 6.6, 5.0)[i], 2.6, (0.0, 0.0, 0.3))
    return out


DEMO = dict(pre='dm_', **{
    E: dict(pal=dict(base=dict(ramp=['#7a80a8', '#c0c8e4', '#eef2ff', '#ffffff'], keep=0.35, ink='#2a3070', sheen=0.35)),
            tex={'dm_hood': dict(ramp=['#9aa4d0', '#e4e8ff', '#ffffff']), 'dm_beard': dict(ramp=['#b8c0e0', '#f4f6ff'], flatten=0.9),
                 'dm_face': dict(ramp=['#c8cce8', '#f4f6ff'], ink='#2a3070', ink_at=0.25, flatten=0.6), 'dm_cape': dict(ramp=['#9aa4d0', '#e4e8ff', '#ffffff']),
                 'dm_crystal': dict(ramp=['#9ae4ff', '#ffffff'], L=15), 'dm_gem': dict(ramp=['#9ae4ff', '#ffffff'], L=15),
                 'dm_gold': dict(ramp=['#c89a30', '#ffe890', '#ffffff'], L=12), 'dm_glow': dict(ramp=['#9ae4ff', '#ffffff'], L=15)},
            parts={'scythe': lambda B: _demo_blade(False), 'head': _demo_e_head, 'body': _demo_e_body},
            drop={'scythe': ('dm_blade',)}),
    W: dict(tex={'dm_face': dict(ramp=['#05090d', '#101c24'], ink='#7af0ff', L=8), 'dm_skin': dict(ramp=['#05090d', '#101c24']),
                 'dm_beard': dict(ramp=['#05090d', '#101c24']), 'dm_glow': dict(ramp=['#5ae6ff', '#ffffff'], L=15),
                 'dm_crystal': dict(ramp=['#1aa8d8', '#c8fcff'], L=15), 'dm_gem': dict(ramp=['#1aa8d8', '#c8fcff'], L=15),
                 'dm_gold': dict(ramp=['#0a5a78', '#3ad0ea'], L=11), 'dm_rim': dict(ramp=['#0a5a78', '#3ad0ea', '#c8fcff'], L=12),
                 'dm_buckle': dict(ramp=['#1aa8d8', '#c8fcff'], L=14)},
            parts={'scythe': lambda B: _demo_blade(True), 'body': _demo_w_body, 'cape': _demo_w_cape},
            drop={'scythe': ('dm_blade',)}),
})


# ==================================================================================================== THE ERASER (joke)
def _er_e_body(B):
    out = []
    c = (8.0, B.hi[1] + 3.6, (B.lo[2] + B.hi[2]) / 2)
    out += ring(c, 5.4, 14, 0.45, 'x_gold', 15)
    for i in range(10):                                             # (the halo of crumbs, glittering)
        a = math.radians(i * 36 + 8)
        x, z = c[0] + 5.4 * math.cos(a), c[2] + 5.4 * math.sin(a)
        s = 0.55 + 0.25 * (i % 3)
        out.append(box((x - s, c[1] - s * 0.8, z - s), (x + s, c[1] + s * 0.8, z + s), 'e_crumb', 15, rot=('y', 22.5 * (i % 2), (x, c[1], z))))
    for sd, x in ((1, B.hi[0] - 1.0), (-1, B.lo[0] + 1.0)):
        out += wing((x, B.hi[1] - 2.2, B.hi[2] - 0.2), sd, 0.78, ('x_cwhite', 'e_pinkf', 'x_cwhite', 'e_pinkf', 'x_cwhite'), 'x_gold', 12, 14)
    return out


def marquee(lo, hi, tex='x_soul', dash=1.3, gap=0.9, w=0.32, pad=0.35, light=15):
    """a dashed outline round a box - a selection's marching ants: dashes along its twelve edges, just outside it"""
    lo = tuple(v - pad for v in lo); hi = tuple(v + pad for v in hi)
    out = []
    for ax in range(3):
        o = [i for i in range(3) if i != ax]
        for a in (lo[o[0]], hi[o[0]]):
            for b in (lo[o[1]], hi[o[1]]):
                t = lo[ax]
                while t < hi[ax] - 0.2:
                    t1 = min(hi[ax], t + dash)
                    p, q = [0.0] * 3, [0.0] * 3
                    p[o[0]] = q[o[0]] = a; p[o[1]] = q[o[1]] = b; p[ax], q[ax] = t, t1
                    fr = [p[i] - (w / 2 if i != ax else 0) for i in range(3)]; to = [q[i] + (w / 2 if i != ax else 0) for i in range(3)]
                    out.append(box(fr, to, tex, light))
                    t = t1 + gap
    return out


def _er_w_body(B):
    top = (8.0, B.hi[1] - 0.4, (B.lo[2] + B.hi[2]) / 2)
    sl = B.of('er_slab', 'er_rub', 'er_back')
    lo, hi = (sl[0], sl[1]) if sl else (B.lo, B.hi)
    return plume(top, 3, 6.4, 2.8, 2.8, back=0.2, lean_x=0.4) + marquee(lo, hi)


def _er_w_leg(B):
    f = B.lowest()                                                  # (soul fire trailing off its heels)
    return flick((f[0], f[1] + 0.5, B.hi[2] - 0.2), (0.0, 0.25, 1.0), 3.0, 1.5, curl=(0.0, 0.5, 0.0))


ERASER = dict(pre='er_', **{
    E: dict(pal=dict(base=dict(ramp=['#d87aa8', '#f4b8d4', '#ffe8f4', '#ffffff'], keep=0.0, ink='#5a2050', sheen=0.4)),
            tex={'er_sleeve': dict(ramp=['#c8962a', '#ffe680', '#fffbe8'], L=12), 'er_crumb': dict(ramp=['#e8b840', '#fff4c0'], L=13),
                 'er_face': dict(ramp=['#d87aa8', '#f4b8d4', '#ffe8f4', '#ffffff'], ink='#3a1040', sheen=0.3)},
            paint={'e_crumb': lambda: crystal_t('#fff4c8', '#f08ab8'), 'e_pinkf': lambda: crystal_t('#fff0f8', '#f090c0')},
            parts={'body': _er_e_body}),
    W: dict(tex={'er_sleeve_front': dict(ramp=['#05090d', '#0e1c26', '#3ad0ea', '#c8fcff'], L=13), 'er_sleeve': dict(ramp=['#05090d', '#0e1c26', '#1e6e88'], L=6),
                 'er_crumb': dict(ramp=['#3ad0ea', '#ffffff'], L=15)},
            parts={'body': _er_w_body, 'legl': _er_w_leg, 'legr': _er_w_leg}),
})


# ==================================================================================================== DONADO (joke)
def _don_e_head(B):
    y = B.hi[1] + 3.2
    c = (8.0, y, (B.lo[2] + B.hi[2]) / 2)
    out = [box((c[0] - 4.6, y, c[2] - 4.6), (c[0] + 4.6, y + 0.8, c[2] + 4.6), 'x_pearl', 12),
           box((c[0] - 4.6, y + 0.05, c[2] - 4.6), (c[0] + 4.6, y + 0.75, c[2] + 4.6), 'x_pearl', 12, rot=('y', 45, c)),
           box((c[0] - 3.2, y - 0.5, c[2] - 3.2), (c[0] + 3.2, y + 0.1, c[2] + 3.2), 'x_iron_e', 10, rot=('y', 22.5, c)),
           box((c[0] - 1.9, y + 0.7, c[2] - 1.9), (c[0] + 1.9, y + 2.5, c[2] + 1.9), 'x_caqua', 13, rot=('y', 45, c))]
    for i in range(8):
        a = math.radians(i * 45 + 22.5)
        x, z = c[0] + 5.2 * math.cos(a), c[2] + 5.2 * math.sin(a)
        out.append(box((x - 0.45, y + 0.1, z - 0.45), (x + 0.45, y + 0.7, z + 0.45), ('x_cgold', 'x_caqua')[i % 2], 15))
    # (the tractor beam, a faint cone down onto his head)
    for i in range(4):
        a = math.radians(i * 90 + 45)
        out.append(beam((c[0] + 2.6 * math.cos(a), y - 0.4, c[2] + 2.6 * math.sin(a)), (c[0] + 4.0 * math.cos(a), y - 2.8, c[2] + 4.0 * math.sin(a)), 0.35, 'x_light', 15))
    return out


def _don_w_head(B):
    out = []
    ears = B.of('don_ear')
    if ears:
        for lo, hi in ears[3]:
            x = (lo[0] + hi[0]) / 2
            out += tongue((x, hi[1] - 0.8, (lo[2] + hi[2]) / 2), 4.0, 1.8, (0.3 if x > 8 else -0.3, 0.0, 0.7))
    return out


def _don_w_torso(B):
    out = []
    for sd, x in ((1, B.hi[0] + 0.6), (-1, B.lo[0] - 0.6)):        # (speed lines streaming off him)
        for dy, L in ((0.0, 13.0), (-2.6, 9.5), (2.4, 8.0)):
            y = B.c[1] + dy
            out.append(beam((x, y, B.c[2]), (x + 0.6 * sd, y + 0.4, min(31.5, B.c[2] + L)), 0.4, 'x_soul', 15))
    return out


def _don_w_tail(B):
    return flick((8.0, 8.0, B.hi[2] - 0.6), (0.0, 0.35, 1.0), 6.0, 2.2, curl=(0.0, 0.4, 0.0))


def _don_w_leg(B):
    f = B.lowest()
    return flick((f[0], f[1] + 0.8, f[2] + 0.4), (0.0, 0.2, 1.0), 4.0, 1.8, curl=(0.0, 0.5, 0.0))


DONADO = dict(pre='dnr_', **{
    E: dict(pal=dict(base=dict(ramp=['#c8a868', '#f0dcae', '#fff6e4', '#ffffff'], keep=0.2, ink='#3a2a5a', sheen=0.3)),
            tex={'don_shirt': holo, 'don_dark': dict(ramp=['#2a2a6a', '#5a5aa8'])},
            paint={'x_iron_e': lambda: grad_t('#c8d0e8', '#7a84a8', line='#9af4ff')},
            parts={'head': _don_e_head}),
    W: dict(tex={'don_shirt': hotrod, 'don_dark': dict(ramp=['#5ae6ff', '#e0ffff'], L=14), 'don_fur': dict(ramp=['#2a2620', '#5a5040', '#8a7a60']),
                 'don_muzzle': dict(ramp=['#3a362e', '#6a6050']), 'don_patch': dict(ramp=['#1a1812', '#2a2620'])},
            parts={'head': _don_w_head, 'torso': _don_w_torso, 'tail': _don_w_tail, 'legl': _don_w_leg, 'legr': _don_w_leg}),
})


# ---------------------------------------------------------------------------------------------------- (3.0g) what changes: the owner's rule
# Only the OUTFIT (clothes, armour, weapon, accessories) takes the form's colours; the EYES glow (Ethereal violet, as Emma's;
# Wraithfire cyan); skin, fur, hair, face and the rest of their natural colours stay exactly as they are. The new parts come on top.
def _collar(gold):
    def f(B):
        x0, x1, y0, y1 = B.lo[0] - 0.35, B.hi[0] + 0.35, B.hi[1] - 3.4, B.hi[1] + 0.35
        out = [box((x0, y0, -0.6), (x1, y1, 1.6), 'x_gold' if gold else 'x_iron', 12 if gold else 10)]
        if gold:
            out += crystal((8.0, y0 + 0.2, -0.9), (8.0, y0 - 2.6, -0.9), 1.6, 'x_clilac', 13, 15)              # (a crystal tag)
        else:
            for x in (x0 + 0.8, 8.0, x1 - 0.8):                                                                    # (spikes, lit)
                out += crystal((x, y1 - 1.0, -0.6), (x, y1 - 1.0, -2.8), 0.9, 'x_scrys', 13, 15)
            for y in (y1 + 0.1,):
                out += crystal((x0, y - 1.4, 0.4), (x0 - 2.0, y - 1.0, 0.4), 0.9, 'x_scrys', 13, 15) + crystal((x1, y - 1.4, 0.4), (x1 + 2.0, y - 1.0, 0.4), 0.9, 'x_scrys', 13, 15)
        return out
    return f


def _plus(fn, extra):
    return lambda B: fn(B) + extra(B)


for _f, _g in ((E, True), (W, False)):
    BENDER[_f]['parts']['body'] = _plus(BENDER[_f]['parts']['body'], _collar(_g))
    BENDER[_f].update(outfit=(), eyes={'bd_face': dict(sel='dark', thr=0.28, box=(0.0, 0.0, 0.5, 0.45))})
    CAPSHUN[_f].update(outfit=('mz_t_', 'mz_sk_'), eyes={'mz_face': dict(sel='fill', fill=((0.37, 0.36), (0.63, 0.36)))})
    SOVEREIGN[_f].update(outfit=('ds_plate', 'ds_edge', 'ds_dark', 'ds_iron', 'ds_chain', 'ds_red', 'ds_horn', 'ds_glass', 'ds_grip', 'ds_heart', 'ds_visor')
                         if _g else ('ds_red', 'ds_chain', 'ds_glass', 'ds_heart'),
                         eyes={'ds_eye': dict(sel='hue', hue=(0.92, 0.08), L=14), 'ds_beye': dict(sel='hue', hue=(0.92, 0.12), L=14)})
    KEEPER[_f].update(outfit=('kb_robe', 'kb_hood', 'kb_lining', 'kb_brd', 'kb_gold', 'kb_rim', 'kb_tier', 'kb_wing', 'kb_bonds', 'kb_inner', 'kb_light', 'kb_ray'),
                      eyes={'kb_eyes': dict(sel='hue', hue=(0.15, 0.6), L=12)})
    LANTERN[_f].update(outfit=('ln_flame',), eyes={'ln_face': dict(sel='hue', hue=(0.9, 0.04), L=0)})
    LEO[_f].update(outfit=('le_steel', 'le_mail', 'le_tunic', 'le_cape', 'le_rim', 'le_belt', 'le_skirt', 'le_emblem', 'le_hose', 'le_gold', 'le_gem', 'le_tri', 'le_grip'),
                   eyes={'le_face': dict(sel='hue', hue=(0.2, 0.45))})
    CELI[_f].update(outfit=('ce_tunic', 'ce_skirt', 'ce_fur', 'ce_stripe', 'ce_belt', 'ce_moon', 'ce_star', 'ce_band', 'ce_mitt', 'ce_boot', 'ce_shoe', 'ce_shorts', 'ce_steel', 'ce_ice'),
                    eyes={'ce_face': dict(sel='hue', hue=(0.08, 0.2))})
    DEMO[_f].update(outfit=('dm_hood', 'dm_cape', 'dm_plate', 'dm_rim', 'dm_shirt', 'dm_glove', 'dm_belt', 'dm_buckle', 'dm_gold', 'dm_gem', 'dm_chest',
                            'dm_pants', 'dm_boot', 'dm_cuff', 'dm_shaft', 'dm_crystal', 'dm_blade', 'dm_emblem'),
                    eyes={'dm_face': dict(sel='hue', hue=(0.68, 0.85), box=(0.0, 0.1, 1.0, 0.45)), 'dm_glow': dict(sel='all', L=13)})
    ERASER[_f].update(outfit=('er_sleeve', 'er_crumb'), eyes={'er_face': dict(sel='dark', thr=0.3)})
    DONADO[_f].update(outfit=('don_shirt',), eyes={'don_dark': dict(sel='all', L=12)})


DESIGNS = {'bender': BENDER, 'capshun': CAPSHUN, 'sovereign': SOVEREIGN, 'keeper': KEEPER, 'lantern': LANTERN, 'leo': LEO, 'celi': CELI,
           'demo': DEMO, 'eraser': ERASER, 'don': DONADO}
