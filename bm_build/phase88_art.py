"""2.67: THE GUTTER GENTRY - the art, blocky (in the spirit of Cobblemon's adaptations: square forms that keep the
reference's silhouette and its faces - no curves faked out of slivers).

BATTY: a big square navy head with stepped pointed ears and a little grey pipe-cap between them; heavy-lidded sleepy
  yellow eyes; a square muzzle with a pink nose over a wide, gritted, toothy grin; a spiky collar; a grey belly with
  black bands; brown wings - flat membranes with tan panels on blocky finger bones; dangling clawed feet, a tan tail web.
  He roosts upside down.
EGGBERT: a stacked egg - grey-white shell with slate spots, split by a jagged crack: the halves' toothed edges are cut
  out, so the black ooze core shows between them, with two pale glowing eyes in it (lit on their own); ooze drips over
  the lower shell; black dripping arms with three talons; stubby black legs with clawed feet; a broken pipe on top.
THE COUNT: a pale blue gumdrop of a blob in tiers - grumpy: furrowed brows, round empty white eyes, a frown with two
  little fangs; drooping side lobes; a blocky black top hat with a red band; stick legs in pointed shoes; a cane.

Front = -z (north). Design units: each part's joint is at 0 (model = design + 8). Rigs are flat: every part hangs off
the body joint (its offset turns with the body). Animation: gaits (idle, walk, run, jump - looped) and acts (attacks -
one-shot). Each keyframe is blended over its whole duration, so the motion reads as continuous.
"""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import _cloth, _el, hexc, qa, qmul

FUR, FUR_LT, FUR_DK, INK = '#2e2b4a', '#454170', '#1c1a31', '#0d0c17'
BELLY, BELLY_DK, STRIPE = '#a9adad', '#8c9090', '#262626'
WING, WING_LT = '#8b5a3a', '#c4a57a'
EYE, EYE_DK, PUPIL, NOSE = '#e4d42c', '#a8980e', '#17150c', '#e8a6b8'
TEETH, TEETH_SH, GUM = '#ecebe6', '#a8a8a4', '#141418'
SHELL, SHELL_HL, SHELL_DK, SPOT = '#d6d2ca', '#ebe8e2', '#b2aea6', '#56626e'
GOO, GOO_HL, EGG_EYE, EGG_EYE_HL = '#121214', '#3a3a42', '#e4f09a', '#fbffe0'
PIPE, PIPE_DK = '#9a9da2', '#696c72'
BLOB, BLOB_DK, BLOB_LN = '#c9dcf0', '#a3bcda', '#2b3b58'
HAT, BAND, BLACK = '#1d1d20', '#c43a3a', '#151517'
SPEC, WHITE = '#7c8698', '#f6f8fa'


# ---------------------------------------------------------------------------------------------------- textures
def _noise(c, seed, var=0.05):
    return _cloth(c, seed, var=var)


UV = {}          # texture -> the uv window of its painted face (filled as the textures are made)


def _canvas(name, w, h, base, seed=1, var=0.04):
    """a texture for a w x h (design units) face, with the uv window that maps it unstretched; k = pixels per unit"""
    im = _noise(base, seed, var)
    if w >= h: k, win = 64 / w, [0, 0, 16, round(16 * h / w, 3)]
    else: k, win = 64 / h, [0, 0, round(16 * w / h, 3), 16]
    UV[name] = win
    return im, ImageDraw.Draw(im), (lambda x, y: (round(x * k), round(y * k)))


def _fur(seed=1, base=FUR):
    im = _noise(base, seed, 0.06); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(90):
        x, y = rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2)
        d.rectangle((x, y, x + 1, y + 3), fill=hexc(rnd.choice((FUR_LT, FUR_DK))))
    return im


def _bat_face():
    """the head's front (12 x 10): small dark brows, heavy-lidded yellow eyes looking down and in, lighter fur tufts at
    the cheeks (the muzzle box covers the lower middle)"""
    im, d, P = _canvas('gnt_bat_face', 12, 10, FUR, 3, 0.05)
    rnd = random.Random(4)
    for _ in range(40):
        x, y = rnd.uniform(0, 12), rnd.uniform(0, 10)
        d.rectangle(P(x, y) + P(x + 0.2, y + 0.6), fill=hexc(rnd.choice((FUR_LT, FUR_DK))))
    for cx, s in ((3.4, 1), (8.6, -1)):
        x0, x1, y0, y1 = cx - 1.8, cx + 1.8, 2.3, 4.9
        d.rectangle(P(x0 - 0.2, y0 - 0.2) + P(x1 + 0.2, y1 + 0.2), fill=hexc(INK))             # the eye, square-cut
        d.rectangle(P(x0, y0) + P(x1, y1), fill=hexc(EYE))
        d.rectangle(P(x0, y1 - 0.5) + P(x1, y1), fill=hexc(EYE_DK))
        px = cx + 0.4 * s                                                                     # pupil: low and inward (sleepy)
        d.rectangle(P(px - 0.7, y0 + 1.1) + P(px + 0.7, y1 - 0.15), fill=hexc(PUPIL))
        d.rectangle(P(px - 0.5 - 0.15, y0 + 1.3) + P(px - 0.5 + 0.15, y0 + 1.7), fill=hexc('#ffffff'))   # (the glint: the same side in both)
        d.rectangle(P(x0 - 0.3, y0 - 0.3) + P(x1 + 0.3, y0 + 1.0), fill=hexc(FUR_DK))          # the heavy lid, half shut
        d.rectangle(P(x0 - 0.3, y0 + 0.9) + P(x1 + 0.3, y0 + 1.2), fill=hexc(INK))
        d.rectangle(P(cx - 1.3 * s - 0.6, 1.0) + P(cx - 1.3 * s + 0.6, 1.45), fill=hexc(INK))  # a little brow at the inner end
    for x0, s in ((0.1, 1), (11.0, -1)):                                                       # cheek tufts
        for i in range(3):
            x = x0 + s * i * 0.4
            d.rectangle(P(min(x, x + 0.9 * s), 6.4 + i * 0.6) + P(max(x, x + 0.9 * s), 6.8 + i * 0.6), fill=hexc(FUR_LT))
    return im


def _bat_grin():
    """the muzzle's front (8.4 x 4.2): a pink nose, then the wide gritted grin - two rows of square teeth, a fang at each
    upper corner, outlined in black"""
    im, d, P = _canvas('gnt_bat_grin', 8.4, 4.2, FUR, 5, 0.05)
    d.rectangle(P(3.5, 0.2) + P(4.9, 0.8), fill=hexc(NOSE)); d.rectangle(P(3.9, 0.8) + P(4.5, 1.1), fill=hexc(NOSE))
    d.rectangle(P(3.7, 0.25) + P(4.0, 0.45), fill=hexc('#ffd6e2'))
    x0, x1, y0, y1 = 0.45, 7.95, 1.35, 3.95
    d.rectangle(P(x0, y0) + P(x1, y1), fill=hexc(GUM))
    d.rectangle(P(x0 + 0.2, y0 + 0.2) + P(x1 - 0.2, y1 - 0.2), fill=hexc(TEETH))
    ym = (y0 + y1) / 2
    d.rectangle(P(x0 + 0.2, ym - 0.5) + P(x1 - 0.2, ym - 0.12), fill=hexc('#d0d0cc'))
    d.rectangle(P(x0 + 0.2, y1 - 0.55) + P(x1 - 0.2, y1 - 0.2), fill=hexc(TEETH_SH))
    d.rectangle(P(x0 + 0.2, ym - 0.12) + P(x1 - 0.2, ym + 0.12), fill=hexc(GUM))                 # the gritted line
    n = 7
    for i in range(1, n):
        x = x0 + 0.2 + i * (x1 - x0 - 0.4) / n
        d.rectangle(P(x - 0.08, y0 + 0.2) + P(x + 0.08, y1 - 0.2), fill=hexc(TEETH_SH))
    for fx in (x0 + 0.6, x1 - 1.1):                                                                # fangs over the lower row
        d.rectangle(P(fx, ym) + P(fx + 0.5, ym + 0.75), fill=hexc('#ffffff'))
        d.rectangle(P(fx + 0.1, ym + 0.75) + P(fx + 0.4, ym + 1.0), fill=hexc('#ffffff'))
    return im


def _bat_chest():
    """the torso's front (8 x 11): grey belly in bands - grey, black, grey, black, grey - edged with fur, collar fur on top"""
    im, d, P = _canvas('gnt_bat_chest', 8, 11, BELLY, 6, 0.03)
    for y0, y1 in ((3.0, 4.6), (6.6, 8.2)):
        d.rectangle(P(0, y0) + P(8, y1), fill=hexc(STRIPE))
    for y0 in (1.2, 4.8, 8.4):
        d.rectangle(P(0, y0 + 1.4) + P(8, y0 + 1.8), fill=hexc(BELLY_DK))
    d.rectangle(P(0, 0) + P(0.7, 11), fill=hexc(FUR)); d.rectangle(P(7.3, 0) + P(8, 11), fill=hexc(FUR))
    for i in range(8):
        x = i + 0.5
        d.polygon([P(x - 0.5, 0), P(x + 0.5, 0), P(x, 1.4 + 0.4 * (i % 2))], fill=hexc(FUR_DK))
    return im


WRIST = (8.0, 1.0)
TIPS = [(18.0, 0.9), (15.8, 8.8), (12.8, 12.55), (8.0, 13.5), (0.0, 11.5)]       # (texture units: x out, y down from the arm)


def _wing():
    """the right wing's membrane (18 x 14 from the shoulder): brown with tan panels, navy finger bones from the wrist to
    each point, a scalloped trailing edge; clear outside"""
    W, H = 18, 14
    k = 64 / W; UV['gnt_wing'] = [0, 0, 16, round(16 * H / W, 3)]
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    P = lambda x, y: (round(x * k), round(y * k))
    d.polygon([P(0, 0), P(18, 0)] + [P(*t) for t in TIPS], fill=hexc(WING))
    for t0, t1 in zip(TIPS[:-1], TIPS[1:]):                                                          # tan along each bone's lee
        a = (WRIST[0] + (t0[0] - WRIST[0]) * 0.35, WRIST[1] + (t0[1] - WRIST[1]) * 0.35)
        d.polygon([P(*a), P(*t0), P((t0[0] * 2 + t1[0]) / 3, (t0[1] * 2 + t1[1]) / 3)], fill=hexc(WING_LT))
    for a, b in zip(TIPS, TIPS[1:]):                                                                 # scallops: bite out the edge
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        nx, ny = -(b[1] - a[1]) / ln, (b[0] - a[0]) / ln
        if nx * (mx - WRIST[0]) + ny * (my - WRIST[1]) < 0: nx, ny = -nx, -ny                       # (pointing away from the wrist)
        r = ln * 0.4
        cx, cy = mx + nx * r * 0.6, my + ny * r * 0.6                                                 # the bite sits outside the edge, eating in
        d.ellipse(P(cx - r, cy - r) + P(cx + r, cy + r), fill=(0, 0, 0, 0))
    for t in TIPS[:-1]:
        d.line(P(*WRIST) + P(*t), fill=hexc(FUR), width=max(2, round(0.45 * k)))
    d.rectangle(P(0, 0) + P(18, 1.4), fill=hexc(FUR))
    return im


def _tail():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (63, 0), (32, 63)], fill=hexc(WING_LT)); d.line((32, 0, 32, 50), fill=hexc(WING), width=2)
    return im


CRACK_P, CRACK_X0, CRACK_A = 16 / 3, 2.9, 3.5          # the crack's zigzag: period, a low point (under the big eye), height (units)


def crack_z(xu):
    """0 at the crack's low points, 1 at its high points (xu: design x across the front)"""
    t = ((xu - CRACK_X0) % CRACK_P) / CRACK_P
    return 1 - abs(t * 2 - 1)


def _shell(seed=11, spots=((14, 18, 9), (44, 40, 11), (52, 10, 6), (22, 50, 7)), crack=None):
    """grey-white shell with slate spots (squared off); crack: ('lo', top) / ('hi', top) - the face's top in units, and
    which half: the lower half's edge runs 12.5 + 3.5z, the upper's 17.5 + 3.5z, so the two interlock like jaws around a
    black band 5 units deep; beyond the edge, clear"""
    im = _noise(SHELL, seed, 0.03); d = ImageDraw.Draw(im)
    for x, y, r in spots:
        d.rectangle((x - r, y - r + 2, x + r, y + r - 2), fill=hexc(SPOT)); d.rectangle((x - r + 2, y - r, x + r - 2, y + r), fill=hexc(SPOT))
    d.rectangle((6, 4, 12, 7), fill=hexc(SHELL_HL)); d.rectangle((40, 30, 43, 32), fill=hexc(SHELL_HL))
    if crack:
        half, top = crack
        for x in range(64):
            z = crack_z(x / 4 - 8 + 0.125)
            edge = (12.5 if half == 'lo' else 17.5) + CRACK_A * z
            row = (top - edge) * 4
            for y in range(64):
                if (half == 'lo' and y < row) or (half == 'hi' and y > row): im.putpixel((x, y), (0, 0, 0, 0))
            e = math.ceil(row) if half == 'lo' else math.floor(row)                                   # a darker rim on the broken edge
            if 0 <= e < 64: im.putpixel((x, e), hexc(SHELL_DK))
    return im


def _egg_eye():
    im = Image.new('RGBA', (64, 64), hexc(INK)); d = ImageDraw.Draw(im)
    d.rectangle((4, 4, 59, 59), fill=hexc('#9aa86a')); d.rectangle((8, 8, 55, 55), fill=hexc(EGG_EYE))
    d.rectangle((18, 18, 45, 45), fill=hexc(EGG_EYE_HL)); d.rectangle((12, 12, 22, 20), fill=hexc('#ffffff'))
    return im


def _goo():
    im = _noise(GOO, 19, 0.06); d = ImageDraw.Draw(im); rnd = random.Random(19)
    for _ in range(16):
        x, y = rnd.randrange(0, 60, 2), rnd.randrange(0, 60, 2)
        d.rectangle((x, y, x + 3, y + 1), fill=hexc(GOO_HL))
    return im


def _claw():
    im = _noise('#1e1e22', 23, 0.05); d = ImageDraw.Draw(im)
    d.rectangle((0, 44, 63, 63), fill=hexc('#4a4a52'))
    return im


def _count_face():
    """the blob's front (18 x 7): an angry furrowed brow, round spectacle eyes (grey rims, empty white - no pupils), a
    knobbly nose line, a frown with two little fangs pointing up"""
    im, d, P = _canvas('gnt_count_face', 18, 7, BLOB, 41, 0.025)
    ln = hexc(BLOB_LN)
    d.rectangle(P(0, 6.3) + P(18, 7), fill=hexc(BLOB_DK))
    for (x0, y0), (x1, y1) in (((3.2, 0.9), (7.8, 1.9)), ((14.8, 0.9), (10.2, 1.9))):
        for i in range(13):
            x = x0 + (x1 - x0) * i / 12; y = y0 + (y1 - y0) * i / 12
            d.rectangle(P(x - 0.25, y - 0.2) + P(x + 0.25, y + 0.25), fill=ln)
    for x in (8.6, 9.4):
        d.rectangle(P(x - 0.12, 0.5) + P(x + 0.12, 1.5), fill=ln)
    d.rectangle(P(5.6, 0.25) + P(12.4, 0.45), fill=hexc(BLOB_DK))                                   # the forehead crease
    for cx in (6.4, 11.6):                                                                           # the spectacle eyes
        cy, r = 3.3, 1.35
        d.ellipse(P(cx - r - 0.25, cy - r - 0.25) + P(cx + r + 0.25, cy + r + 0.25), fill=hexc(SPEC))
        d.ellipse(P(cx - r, cy - r) + P(cx + r, cy + r), fill=hexc(WHITE))                      # (empty white: no pupils)
    for x, y in ((8.2, 4.95), (9.0, 4.75), (9.8, 4.95)):                                             # a knobbly nose line
        d.rectangle(P(x - 0.3, y) + P(x + 0.3, y + 0.25), fill=ln)
    pts = [(4.4, 6.3), (5.6, 5.85), (7.4, 5.55), (9.0, 5.45), (10.6, 5.55), (12.4, 5.85), (13.6, 6.3)]   # the frown
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        for i in range(9):
            x = xa + (xb - xa) * i / 8; y = ya + (yb - ya) * i / 8
            d.rectangle(P(x - 0.15, y - 0.12) + P(x + 0.15, y + 0.12), fill=ln)
    for fx, fy in ((5.7, 5.9), (12.3, 5.9)):                                                         # two fangs, pointing up
        d.polygon([P(fx - 0.45, fy), P(fx + 0.45, fy), P(fx, fy - 0.9)], fill=hexc('#ffffff'), outline=ln)
    return im


def _band():
    im = _noise(BAND, 37, 0.04); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 3), fill=hexc('#e05a5a')); d.rectangle((0, 60, 63, 63), fill=hexc('#8a2424'))
    return im


def textures():
    return {'gnt_fur': _fur(1), 'gnt_fur_dk': _fur(2, FUR_DK), 'gnt_fur_lt': _fur(7, FUR_LT), 'gnt_bat_face': _bat_face(), 'gnt_bat_grin': _bat_grin(),
            'gnt_bat_chest': _bat_chest(), 'gnt_wing': _wing(), 'gnt_tail': _tail(),
            'gnt_shell': _shell(), 'gnt_shell_b': _shell(13, ((40, 20, 10), (12, 44, 8), (54, 52, 6))),
            'gnt_shell_lo': _shell(17, ((20, 26, 6), (50, 27, 5), (6, 29, 3)), crack=('lo', 16.2)),
            'gnt_shell_hi': _shell(21, ((16, 6, 5), (46, 4, 5)), crack=('hi', 24.5)),
            'gnt_egg_eye': _egg_eye(), 'gnt_goo': _goo(), 'gnt_pipe': _noise(PIPE, 23, 0.06), 'gnt_pipe_dk': _noise(PIPE_DK, 24, 0.06), 'gnt_claw': _claw(),
            'gnt_blob': _noise(BLOB, 27, 0.025), 'gnt_blob_dk': _noise(BLOB_DK, 28, 0.03), 'gnt_count_face': _count_face(),
            'gnt_black': _noise(BLACK, 29, 0.05), 'gnt_hat': _noise(HAT, 31, 0.04), 'gnt_band': _band()}


# ---------------------------------------------------------------------------------------------------- models
O = (0, 0, 0)


def _box(fr, to, tex, rot=None, uv=None, front=None, faces=None, drop=(), other=None):
    """a box; front: a painted texture on its north face, mapped whole; drop: faces left off (hidden or open);
    other: {face: texture} for faces in another texture"""
    fs = [f for f in (faces or ('north', 'south', 'east', 'west', 'up', 'down')) if f not in drop]
    u = dict(uv or {})
    if front and 'north' not in u and front in UV: u['north'] = UV[front]
    e = _el(fr, to, tex, O, rot, u, fs)
    if front: e['faces']['north']['texture'] = '#' + front
    for f, t in (other or {}).items():
        if f in e['faces']: e['faces'][f]['texture'] = '#' + t
    return e


def _mirror(els):
    """the left side from the right: x flipped (rotations about y and z reversed, east and west swapped, uvs flipped)"""
    out = []
    for e in els:
        f, t = e['from'], e['to']
        n = {'from': [round(16 - t[0], 4), f[1], f[2]], 'to': [round(16 - f[0], 4), t[1], t[2]], 'faces': {}}
        for k, v in e['faces'].items():
            k2 = {'east': 'west', 'west': 'east'}.get(k, k)
            u = list(v['uv']); n['faces'][k2] = {'uv': [u[2], u[1], u[0], u[3]], 'texture': v['texture']}
        if 'rotation' in e:
            r = e['rotation']; o = r['origin']
            n['rotation'] = {'origin': [round(16 - o[0], 4), o[1], o[2]], 'axis': r['axis'], 'angle': -r['angle'] if r['axis'] in ('y', 'z') else r['angle']}
        out.append(n)
    return out


def _shift(els, dy):
    for e in els:
        e['from'][1] = round(e['from'][1] - dy, 4); e['to'][1] = round(e['to'][1] - dy, 4)
        if 'rotation' in e: e['rotation']['origin'][1] = round(e['rotation']['origin'][1] - dy, 4)
    return els


# ---- Batty (joint at the neck: the torso hangs below it, the head sits on it)
def bat_body():
    els = [_box((-4, -11, -3.2), (4, 0, 3.2), 'gnt_fur', front='gnt_bat_chest')]
    for sx in (1, -1):
        x0, x1 = sorted((sx * 1.8, sx * 3.4))
        els.append(_box((x0, -15, -0.8), (x1, -10.6, 0.8), 'gnt_fur_dk', drop=('up',)))                   # a leg
        for dx in (-0.55, 0.0, 0.55):                                                                     # three toe claws, curled
            cx = (x0 + x1) / 2 + dx
            els.append(_box((cx - 0.22, -16.2, -1.5), (cx + 0.22, -14.9, 0.0), 'gnt_claw'))
    els.append(_box((-1.9, -14.6, -0.15), (1.9, -10.7, 0.15), 'gnt_tail', faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [16, 0, 0, 16]}))
    for x, z, ang in ((-2.6, -3.0, -22.5), (0.0, -3.2, -22.5), (2.6, -3.0, -22.5), (-2.6, 3.0, 22.5), (0.0, 3.2, 22.5), (2.6, 3.0, 22.5)):
        els.append(_box((x - 0.8, -1.0, z - 0.5), (x + 0.8, 2.0, z + 0.5), 'gnt_fur_dk', ('x', ang, (x, -1.0, z))))   # the spiky collar
    for sx in (1, -1):
        x = sx * 4.0
        els.append(_box((x - 0.5, -1.2, -1.6), (x + 0.5, 1.8, 1.6), 'gnt_fur_dk', ('z', -22.5 * sx, (x, -1.2, 0))))
    return els


def bat_head():
    els = [_box((-6, 0, -5), (6, 10, 5), 'gnt_fur', front='gnt_bat_face'),
           _box((-4.2, 0.6, -5.7), (4.2, 4.8, -4.8), 'gnt_fur', front='gnt_bat_grin', drop=('south',)),            # the muzzle: nose and grin
           _box((-1.8, 9.8, -1.8), (1.8, 12.2, 1.8), 'gnt_pipe', drop=('down',)), _box((-2.1, 12.0, -2.1), (2.1, 12.7, 2.1), 'gnt_pipe_dk')]
    for sx in (1, -1):
        def ex(a, b): return sorted((sx * a, sx * b))
        (a0, a1), (b0, b1), (c0, c1) = ex(2.4, 5.6), ex(3.0, 5.2), ex(3.6, 4.7)
        els += [_box((a0, 9.6, -1.3), (a1, 12.8, 1.3), 'gnt_fur', front='gnt_fur_lt'),                         # stepped pointed ears
                _box((b0, 12.6, -1.0), (b1, 15.0, 1.0), 'gnt_fur'), _box((c0, 14.8, -0.6), (c1, 16.8, 0.6), 'gnt_fur_dk')]
        tx0, tx1 = ex(5.8, 7.4)                                                                         # cheek tufts
        els.append(_box((tx0, 1.2, -2.6), (tx1, 2.8, -0.4), 'gnt_fur_dk', ('z', -22.5 * sx, (sx * 5.8, 2.0, -1.5))))
        tx0, tx1 = ex(5.6, 7.0)
        els.append(_box((tx0, 4.0, -1.8), (tx1, 5.4, 0.2), 'gnt_fur', ('z', -22.5 * sx, (sx * 5.6, 4.7, -0.8))))
    return els


def bat_wing():
    """the right wing; joint at the shoulder; +x outward (texture point (x, y) -> model (0.5 + x, 2.5 - y))"""
    w = UV['gnt_wing']
    els = [_box((0.5, -11.5, -0.12), (18.5, 2.5, 0.12), 'gnt_wing', faces=('north', 'south'), uv={'north': w, 'south': [w[2], 0, 0, w[3]]}),
           _box((-0.5, 0.9, -0.65), (8.9, 2.2, 0.65), 'gnt_fur'),                                         # the arm
           _box((8.4, 1.1, -0.5), (18.6, 2.3, 0.5), 'gnt_fur'),                                           # the forearm, out to the tip
           _box((8.1, 2.1, -0.4), (9.1, 3.6, 0.4), 'gnt_claw')]                                            # the thumb claw
    wx, wy = 0.5 + WRIST[0], 2.5 - WRIST[1]
    for tx, ty in TIPS[1:4]:                                                                                # the finger bones, along the painted ones
        mx, my = 0.5 + tx, 2.5 - ty
        L = math.hypot(mx - wx, my - wy); ang = math.degrees(math.atan2(mx - wx, wy - my))
        ang = min((45, 22.5, 0, -22.5), key=lambda a: abs(a - ang))
        # (an element's z rotation turns a hanging box's foot toward -x for a positive angle: so outward is negative here)
        els.append(_box((wx - 0.4, wy - L, -0.42), (wx + 0.4, wy, 0.42), 'gnt_fur_dk', ('z', -ang, (wx, wy, 0))))
    return els


# ---- Eggbert (body joint 10 units up, at the lower shell)
EGG_J = 10.0


def egg_body():
    els = [_box((-6, 5, -5), (6, 8.2, 5), 'gnt_shell_b', drop=('up',)),
           _box((-8, 8, -6.5), (8, 16.2, 6.5), 'gnt_shell_lo', drop=('up',), other={'down': 'gnt_shell'},
                uv={'north': [0, 0, 16, 8.2], 'south': [0, 0, 16, 8.2], 'east': [1.5, 0, 14.5, 8.2], 'west': [1.5, 0, 14.5, 8.2]}),
           _box((-7.4, 8.4, -5.9), (7.4, 24.4, 5.9), 'gnt_goo'),                                          # the ooze core
           _box((-7.5, 17.4, -6.0), (7.5, 24.5, 6.0), 'gnt_shell_hi', drop=('down',), other={'up': 'gnt_shell'},
                uv={'north': [0.5, 0, 15.5, 7.1], 'south': [0.5, 0, 15.5, 7.1], 'east': [2, 0, 14, 7.1], 'west': [2, 0, 14, 7.1]}),
           _box((-6, 24.3, -4.8), (6, 27.3, 4.8), 'gnt_shell', drop=('down',)), _box((-4, 27.1, -3.2), (4, 29.2, 3.2), 'gnt_shell_b', drop=('down',)),
           _box((-2.2, 29.0, -2.2), (2.2, 32.3, 2.2), 'gnt_pipe', drop=('down',)), _box((-2.5, 32.1, -2.5), (2.5, 32.8, 2.5), 'gnt_pipe_dk')]
    for x, ln in ((-5.6, 2.6), (-0.6, 3.4), (5.6, 2.4)):                                                  # ooze drips from the lower edge
        top = 12.5 + CRACK_A * crack_z(x) + 0.3
        els.append(_box((x - 0.45, top - ln, -6.75), (x + 0.45, top, -6.4), 'gnt_goo', drop=('south',)))
    for x, ln in ((-4.0, 2.2), (3.4, 2.8)):
        top = 13.5
        els.append(_box((x - 0.45, top - ln, 6.4), (x + 0.45, top, 6.75), 'gnt_goo', drop=('north',)))
    return _shift(els, EGG_J)


def egg_eyes():
    xs = CRACK_X0 - CRACK_P                                                                                # (each sits at a low point of the crack)
    return _shift([_box((CRACK_X0 - 1.8, 12.9, -6.3), (CRACK_X0 + 1.8, 16.6, -5.8), 'gnt_egg_eye', drop=('south',)),
                   _box((xs - 1.1, 13.3, -6.25), (xs + 1.1, 15.5, -5.8), 'gnt_egg_eye', drop=('south',))], EGG_J)


def egg_arm():
    """the right arm; joint at the shoulder; out to the side, then down to a three-talon hand"""
    els = [_box((-0.6, -1.2, -1.2), (5.6, 1.2, 1.2), 'gnt_goo'), _box((4.2, -6.4, -1.05), (6.6, 0.6, 1.05), 'gnt_goo'),
           _box((1.8, -2.8, -0.4), (2.7, -1.1, 0.4), 'gnt_goo')]                                           # a drip
    for cx, ang in ((6.3, 22.5), (5.4, 0), (4.5, -22.5)):
        els.append(_box((cx - 0.32, -10.0, -0.32), (cx + 0.32, -6.2, 0.32), 'gnt_claw', ('z', ang, (cx, -6.2, 0))))
    els.append(_box((5.0, -7.2, -2.8), (5.7, -6.5, -0.9), 'gnt_claw'))                                     # the thumb talon, forward
    return els


def egg_leg():
    els = [_box((-1.7, -4.6, -1.7), (1.7, 1.2, 1.7), 'gnt_goo'), _box((-1.3, -7.0, -1.3), (1.3, -4.4, 1.3), 'gnt_goo'),
           _box((-0.4, -7.5, 1.0), (0.4, -6.7, 2.4), 'gnt_claw')]
    for dx in (-1.2, 0.0, 1.2):
        els.append(_box((dx - 0.4, -7.5, -4.2), (dx + 0.4, -6.6, -1.0), 'gnt_claw'))
    return els


# ---- The Count (body joint 9 units up)
CNT_J = 9.0


def count_body():
    els = [_box((-8, 7, -5.6), (8, 9.2, 5.6), 'gnt_blob_dk', drop=('up',)),
           _box((-9, 9, -6.5), (9, 16, 6.5), 'gnt_blob', front='gnt_count_face'),
           _box((-7.6, 15.8, -5.6), (7.6, 18.5, 5.6), 'gnt_blob', drop=('down',)),
           _box((-5.6, 18.3, -4.2), (5.6, 19.6, 4.2), 'gnt_blob', drop=('down',))]
    for sx in (1, -1):                                                                                   # drooping side lobes
        x0, x1 = sorted((sx * 8.6, sx * 11.6))
        els.append(_box((x0, 10.4, -2.2), (x1, 14.4, 2.2), 'gnt_blob', ('z', 22.5 * sx, (sx * 8.6, 14.4, 0))))
    return _shift(els, CNT_J)


def count_hat():
    els = [_box((-7, 0, -5.4), (7, 1, 5.4), 'gnt_hat'), _box((-4.2, 0.9, -3.8), (4.2, 8, 3.8), 'gnt_hat', drop=('down',)),
           _box((-4.35, 1.5, -3.95), (4.35, 3.0, 3.95), 'gnt_band', drop=('up', 'down'))]
    for sx in (1, -1):                                                                                    # the brim curls up at the sides
        x0, x1 = sorted((sx * 5.8, sx * 7.3))
        els.append(_box((x0, 0.8, -4.6), (x1, 1.8, 4.6), 'gnt_hat', drop=('down',)))
    return els


def count_cane():
    return [_box((-0.4, -11.0, -0.4), (0.4, 0.6, 0.4), 'gnt_black'), _box((-0.45, -11.0, -0.45), (0.45, -10.2, 0.45), 'gnt_pipe'),
            _box((-2.2, 0.0, -0.4), (0.1, 0.9, 0.4), 'gnt_black'), _box((-2.2, -1.2, -0.4), (-1.4, 0.2, 0.4), 'gnt_black')]


def count_leg():
    return [_box((-0.55, -7.6, -0.55), (0.55, 1.2, 0.55), 'gnt_black'), _box((-1.0, -8.5, -2.8), (1.0, -7.5, 0.9), 'gnt_black'),
            _box((-0.55, -8.5, -3.9), (0.55, -7.9, -2.8), 'gnt_black')]


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        for e in els:
            for c in e['from'] + e['to']:
                assert -16 <= c <= 32, (name, e['from'], e['to'])
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    part('gnt_bat_body', bat_body()); part('gnt_bat_head', bat_head())
    part('gnt_bat_wing_r', bat_wing()); part('gnt_bat_wing_l', _mirror(bat_wing()))
    part('gnt_egg_body', egg_body()); part('gnt_egg_eyes', egg_eyes())
    part('gnt_egg_arm_r', egg_arm()); part('gnt_egg_arm_l', _mirror(egg_arm()))
    part('gnt_egg_leg_r', egg_leg()); part('gnt_egg_leg_l', _mirror(egg_leg()))
    part('gnt_blob_body', count_body()); part('gnt_blob_hat', count_hat()); part('gnt_blob_cane', count_cane())
    part('gnt_blob_leg_r', count_leg()); part('gnt_blob_leg_l', _mirror(count_leg()))
    return M


# ---------------------------------------------------------------------------------------------------- poses
# a pose: {part: (translation in blocks, left rotation, scale)} at the boss's feet, facing the boss's way
S_BAT, S_EGG, S_BLOB = 1.1, 1.2, 1.15
U = lambda s: s / 16
I = (0.0, 0.0, 0.0, 1.0)


def _qrot(q, v):
    x, y, z, w = q; vx, vy, vz = v
    t = (2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx))
    return (vx + w * t[0] + y * t[2] - z * t[1], vy + w * t[1] + z * t[0] - x * t[2], vz + w * t[2] + x * t[1] - y * t[0])


def _conv(q):
    """a rotation in the model's frame -> the display's (an item display shows its model turned half round: x and z flip)"""
    return (-q[0], q[1], -q[2], q[3])


def _place(root, body_q, offs, s, scales=None):
    """parts hung off the body: design offsets (units) turned with the body; root = the body's joint above the feet (blocks);
    rotations are given in the model's frame"""
    out = {}
    bq = _conv(body_q)
    for part, (off, q) in offs.items():
        v = _qrot(bq, (-off[0] * U(s), off[1] * U(s), -off[2] * U(s)))
        sc = (scales or {}).get(part, s)
        out[part] = ((round(root[0] + v[0], 4), round(root[1] + v[1], 4), round(root[2] + v[2], 4)), qmul(bq, _conv(q)), sc)
    return out


fwd = lambda deg: qa('x', -deg)              # a lean forward (front = -z)
swing = lambda deg: qa('x', deg)             # a hanging limb swings its end forward


def bat_pose(pitch=10.0, flap=0.0, sweep=0.0, head=0.0, roost=False, bob=0.0, roll=0.0):
    """pitch: body tilted forward; flap: wings up (+) / down (-); sweep: wings swept back; head: nods down (+) / up (-)"""
    if roost:
        body_q, root, hq = qa('z', 180), (0, 2.3, 0), qa('x', head)
    else:
        body_q, root, hq = qmul(qa('z', roll), fwd(pitch)), (0, 0.95 + bob * U(S_BAT), 0), fwd(-pitch * 0.6 + head)
    wing = lambda sx: qmul(qa('z', sx * flap), qa('y', -sx * sweep))
    return _place(root, body_q, {'body': ((0, 0, 0), I), 'head': ((0, 0.2, 0), hq),
                                 'wing_r': ((3.6, -1.6, 0.6), wing(1)), 'wing_l': ((-3.6, -1.6, 0.6), wing(-1))}, S_BAT)


def egg_pose(lean=0.0, sway=0.0, bob=0.0, arm_r=0.0, arm_l=0.0, up_r=0.0, up_l=0.0, leg_r=0.0, leg_l=0.0, turn=0.0, squash=1.0):
    s = S_EGG
    body_q = qmul(qa('y', turn), qmul(qa('z', sway), fwd(lean)))
    out = _place((0, (EGG_J + bob) * U(s), 0), body_q, {'body': ((0, 0, 0), I), 'eyes': ((0, 0, 0), I),
                                                         'arm_r': ((7.6, 7.5, -0.5), qmul(qa('z', up_r), swing(arm_r))),
                                                         'arm_l': ((-7.6, 7.5, -0.5), qmul(qa('z', -up_l), swing(arm_l)))}, s,
                 {'body': (s * (2 - squash) ** 0.5, s * squash, s * (2 - squash) ** 0.5)})
    # (the legs stand on the ground: they turn with him but don't lean or bob with the shell)
    out.update(_place((0, (EGG_J - 2.5) * U(s), 0), qa('y', turn), {'leg_r': ((3.6, 0, 0), swing(leg_r)), 'leg_l': ((-3.6, 0, 0), swing(leg_l))}, s))
    return out


def count_pose(lean=0.0, sway=0.0, bob=0.0, squash=1.0, leg_r=0.0, leg_l=0.0, hat_up=0.0, hat_tilt=0.0, cane=0.0, cane_out=0.0, turn=0.0):
    s = S_BLOB
    body_q = qmul(qa('y', turn), qmul(qa('z', sway), fwd(lean)))
    wide = (s * (2 - squash) ** 0.5, s * squash, s * (2 - squash) ** 0.5)
    out = _place((0, (CNT_J + bob) * U(s), 0), body_q, {'body': ((0, 0, 0), I), 'hat': ((0, 10.5 * squash + hat_up, -0.3), qa('z', hat_tilt)),
                                                         'cane': ((-11.3, 2.0 * squash, -1.0), qmul(qa('z', -cane_out), swing(cane)))}, s, {'body': wide})
    out.update(_place((0, (CNT_J - 0.5) * U(s), 0), qa('y', turn), {'leg_r': ((3.4, 0, 0), swing(leg_r)), 'leg_l': ((-3.4, 0, 0), swing(leg_l))}, s))
    return out


# the gaits (looped: (period in ticks, keyframes)) and the acts (one-shot: [(ticks, keyframe)])
ANIMS = {
    'bat': {'idle': (5, [bat_pose(pitch=12, flap=38, bob=0.6), bat_pose(pitch=12, flap=-30, bob=-0.6)]),
            'walk': (4, [bat_pose(pitch=30, flap=44), bat_pose(pitch=30, flap=-40)]),
            'run': (3, [bat_pose(pitch=55, flap=48, head=-14), bat_pose(pitch=55, flap=-46, head=-14)]),
            'jump': (4, [bat_pose(pitch=70, flap=12, sweep=40, head=-22), bat_pose(pitch=72, flap=4, sweep=46, head=-24)])},
    'egg': {'idle': (10, [egg_pose(up_r=6, up_l=6), egg_pose(bob=0.4, up_r=10, up_l=10, squash=0.98)]),
            'walk': (5, [egg_pose(sway=3, leg_r=24, leg_l=-24, arm_r=-14, arm_l=14, up_r=6, up_l=6),
                         egg_pose(bob=0.8, up_r=10, up_l=10),
                         egg_pose(sway=-3, leg_r=-24, leg_l=24, arm_r=14, arm_l=-14, up_r=6, up_l=6),
                         egg_pose(bob=0.8, up_r=10, up_l=10)]),
            'run': (3, [egg_pose(lean=14, sway=4, leg_r=44, leg_l=-40, arm_r=-30, arm_l=30, up_r=28, up_l=28),
                        egg_pose(lean=14, bob=1.5, up_r=34, up_l=34),
                        egg_pose(lean=14, sway=-4, leg_r=-40, leg_l=44, arm_r=30, arm_l=-30, up_r=28, up_l=28),
                        egg_pose(lean=14, bob=1.5, up_r=34, up_l=34)]),
            'jump': (4, [egg_pose(lean=-6, bob=1.0, leg_r=34, leg_l=18, up_r=55, up_l=55, squash=1.05)])},
    'blob': {'idle': (12, [count_pose(), count_pose(squash=0.97, hat_up=0.3)]),
             'walk': (5, [count_pose(sway=3, leg_r=22, leg_l=-22, cane=14, lean=3),
                          count_pose(bob=0.6, squash=1.02, lean=3, cane=4),
                          count_pose(sway=-3, leg_r=-22, leg_l=22, cane=-8, lean=3),
                          count_pose(bob=0.6, squash=1.02, lean=3, cane=4)]),
             'run': (3, [count_pose(lean=10, leg_r=38, leg_l=-38, cane=-26, cane_out=10),
                         count_pose(lean=10, bob=1.2, squash=1.05, hat_up=1.2, cane=-30, cane_out=12),
                         count_pose(lean=10, leg_r=-38, leg_l=38, cane=-26, cane_out=10),
                         count_pose(lean=10, bob=1.2, squash=1.05, hat_up=1.2, cane=-30, cane_out=12)]),
             'jump': (4, [count_pose(bob=1.0, squash=1.1, leg_r=30, leg_l=26, hat_up=2.0, cane=-20, cane_out=20)])}}
ACTS = {
    'bat': {'bite': [(4, bat_pose(pitch=18, flap=52, head=-26)), (3, bat_pose(pitch=42, flap=-42, head=26)), (5, bat_pose(pitch=25, flap=10))],
            'screech': [(5, bat_pose(pitch=-8, flap=20, sweep=-26, head=-34)), (14, bat_pose(pitch=-12, flap=8, sweep=-30, head=-38)), (6, bat_pose(pitch=12, flap=30))]},
    'egg': {'swipe': [(5, egg_pose(lean=-8, turn=-14, arm_r=-62, up_r=44, arm_l=10, up_l=12, leg_r=-10, leg_l=12)),
                      (3, egg_pose(lean=16, turn=16, arm_r=86, up_r=12, arm_l=-20, up_l=20, leg_r=14, leg_l=-10, squash=0.96)),
                      (6, egg_pose(lean=6, arm_r=20, up_r=10, up_l=10))],
            'ooze': [(6, egg_pose(lean=-10, bob=1.0, up_r=62, up_l=62, arm_r=-10, arm_l=-10, squash=1.04)),
                     (10, egg_pose(lean=-12, bob=1.2, up_r=68, up_l=68, arm_r=-14, arm_l=-14, squash=1.05)),
                     (6, egg_pose(up_r=8, up_l=8))]},
    'blob': {'swat': [(5, count_pose(turn=16, lean=-4, cane=-46, cane_out=26, squash=1.03)),
                      (3, count_pose(turn=-18, lean=8, cane=96, cane_out=6, squash=0.93)),
                      (6, count_pose(cane=10))],
             'tip': [(6, count_pose(hat_up=4.5, hat_tilt=-26, lean=6)), (12, count_pose(hat_up=5.0, hat_tilt=-30, lean=8, squash=0.98)),
                     (6, count_pose())]}}
POSES = {k: {} for k in ANIMS}
for _k, _st in ANIMS.items():
    for _s, (_p, _fr) in _st.items():
        for _i, _f in enumerate(_fr): POSES[_k][f'{_s}{_i}'] = _f
for _k, _st in ACTS.items():
    for _s, _steps in _st.items():
        for _i, (_t, _f) in enumerate(_steps): POSES[_k][f'{_s}{_i}'] = _f
POSES['bat']['roost'] = bat_pose(roost=True, flap=30, head=-10)
PARTS = {'bat': {'body': 'gnt_bat_body', 'head': 'gnt_bat_head', 'wing_r': 'gnt_bat_wing_r', 'wing_l': 'gnt_bat_wing_l'},
         'egg': {'body': 'gnt_egg_body', 'eyes': 'gnt_egg_eyes', 'arm_r': 'gnt_egg_arm_r', 'arm_l': 'gnt_egg_arm_l', 'leg_r': 'gnt_egg_leg_r', 'leg_l': 'gnt_egg_leg_l'},
         'blob': {'body': 'gnt_blob_body', 'hat': 'gnt_blob_hat', 'cane': 'gnt_blob_cane', 'leg_r': 'gnt_blob_leg_r', 'leg_l': 'gnt_blob_leg_l'}}
LIT = {('egg', 'eyes')}                       # (parts shown at full brightness: Eggbert's eyes glow)
