"""2.67: the SCORCHING ARACHNO-LANTERN in the game (from the approved mockup, mockups/arachno_lantern_art.py): a jack-o'-lantern
the size of a house carried on eight long black legs, so tall it walks over the trees. Blocky, like the Gutter Gentry: square
tiers for the pumpkin, the face painted square-cut on its flat front, square legs, square flames.

The rig: every part is an item display standing at the boss itself; where it sits, how it turns and how big it is all live in
its transformation (translation, left rotation, scale), so a pose is a set of transformations and the client glides from one
to the next. The legs walk a wave gait (each leg steps a quarter cycle after the one behind it): each leg's plane swings about its
hip and the swinging ones lift - and no leg ever passes through its neighbour or the fires.
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

from phase57_art import _cloth, _el, hexc, qa, qmul

BODY_S = 2.6                      # the pumpkin: 40 units across -> 6.5 blocks
BODY_Y = 8.2                      # its centre, in blocks above the ground
FLAME_S = 2.6                     # the fires at the corners of the mouth
ORANGE, ORANGE_DK, ORANGE_LT = '#e8761c', '#a8460c', '#f8a848'
GLOW_IN, GLOW_MID, GLOW_OUT, CUT = '#fff4a8', '#ffc030', '#ff7a14', '#4a1804'
PURPLE, PURPLE_DK, PURPLE_LT = '#8a2ac8', '#561488', '#b866f2'
CHITIN, CHITIN_LT, EMBER = '#16111b', '#3a3046', '#ff5a1a'


# ---------------------------------------------------------------------------------------------------- textures
# (2.67) blocky, in the Gutter Gentry's spirit (Cobblemon's adaptations): square forms that keep the silhouette, flat colour with
# chunky shading, the face painted square-cut onto a flat front - no curves faked out of slivers.
UV = {}          # texture -> the uv window of its painted face


def _flat(c, seed, var=0.022):
    return _cloth(c, seed, var=var)


def _canvas(name, w, h, base, seed=1, var=0.022):
    """a texture for a w x h (design units) face, with the uv window that maps it unstretched; P(x, y) -> pixels"""
    im = _flat(base, seed, var)
    if w >= h: kx, win = 64 / w, [0, 0, 16, round(16 * h / w, 3)]
    else: kx, win = 64 / h, [0, 0, round(16 * w / h, 3), 16]
    UV[name] = win
    return im, ImageDraw.Draw(im), (lambda x, y: (round(x * kx), round(y * kx)))


def _skin(seed, grooves=True):
    """pumpkin rind: flat orange, a dark groove every 16 pixels with a lit strip beside it (four ribs across a face)"""
    im = _flat(ORANGE, seed); d = ImageDraw.Draw(im)
    if grooves:
        for x0 in range(0, 64, 16):
            d.rectangle((x0, 0, x0 + 1, 63), fill=hexc(ORANGE_DK)); d.rectangle((x0 + 4, 0, x0 + 6, 63), fill=hexc(ORANGE_LT))
    return im


def _skin_top():
    """the tops of the tiers: the ribs as a square-cut star, darker toward the middle"""
    im = _flat(ORANGE, 12); d = ImageDraw.Draw(im)
    for x0 in range(0, 64, 16):
        d.rectangle((x0, 0, x0 + 1, 63), fill=hexc(ORANGE_DK)); d.rectangle((0, x0, 63, x0 + 1), fill=hexc(ORANGE_DK))
    d.rectangle((22, 22, 41, 41), fill=hexc('#c05a12')); d.rectangle((28, 28, 35, 35), fill=hexc('#8a3a0a'))
    return im


def _skin_dk():
    im = _flat(ORANGE_DK, 25); d = ImageDraw.Draw(im)
    for x0 in range(0, 64, 16):
        d.rectangle((x0, 0, x0 + 1, 63), fill=hexc('#7a3008'))
    return im


FACE_W, FACE_H = 40.0, 22.0           # the face plate: the whole front of the middle tier


def _face():
    """the carved face, square-cut: big slanting triangle eyes with red crescent pupils, two square spider eyes over each, a
    triangle nose, and a wide jagged grin with square teeth (two hanging down, two standing up). The cuts are near-black, a
    dull red glow deep inside."""
    from PIL import ImageFilter
    im, d, P = _canvas('sal_face', FACE_W, FACE_H, ORANGE, 13)
    for x0 in (0, 10, 20, 30, 40):                                                            # the ribs run behind the face
        d.rectangle(P(x0 - 0.35, 0) + P(x0 + 0.35, FACE_H), fill=hexc(ORANGE_DK))
    mask = Image.new('L', im.size, 0); md = ImageDraw.Draw(mask)
    eyes = []
    for sx in (-1, 1):
        cx = 20 + sx * 10.5
        tri = [P(cx - 7.0, 10.5), P(cx + 7.0, 10.5), P(cx + sx * 4.2, 1.6)]                  # slanting in: a scowl
        md.polygon(tri, fill=255); eyes.append((cx, sx))
    for sx in (-1, 1):                                                                        # the spider eyes: two little squares over each
        for k, (ex, ey) in enumerate(((20 + sx * 11.5, 0.9), (20 + sx * 15.5, 1.9))):
            md.rectangle(P(ex - 0.9, ey - 0.6) + P(ex + 0.9, ey + 1.0), fill=255)
    md.polygon([P(18.2, 13.6), P(21.8, 13.6), P(20, 10.9)], fill=255)                          # the nose
    grin = [(1.5, 14.0), (5.5, 15.4), (9.0, 14.3), (13.0, 15.6), (16.5, 14.6), (20, 15.7), (23.5, 14.6), (27.0, 15.6), (31.0, 14.3),
            (34.5, 15.4), (38.5, 14.0), (37.2, 18.0), (33.0, 20.4), (27.5, 21.3), (20, 20.6), (12.5, 21.3), (7.0, 20.4), (2.8, 18.0)]
    md.polygon([P(x, y) for x, y in grin], fill=255)
    for x0, y0, x1, y1 in ((9.2, 14.6, 12.0, 17.4), (28.0, 14.6, 30.8, 17.4), (14.2, 18.4, 16.6, 21.2), (23.4, 18.4, 25.8, 21.2)):
        md.rectangle(P(x0, y0) + P(x1, y1), fill=0)                                            # square teeth left standing
    layers, m = [], mask
    for _ in range(4):
        layers.append(m); m = m.filter(ImageFilter.MinFilter(3))
    cols = ['#2a0c06', '#120406', '#1c0607', '#3a0c0a']                                       # (a dark wall, black, then a dull red glow)
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            dep = sum(1 for L in layers if L.getpixel((x, y)))
            if dep: px[x, y] = hexc(cols[dep - 1])
    for cx, sx in eyes:                                                                       # red crescent pupils: a wide U, horns up
        ey = 7.7
        ux = cx + sx * 4.2 * (10.5 - ey) / 8.9                                                 # (centred in the slanting eye at that height)
        cres = Image.new('L', im.size, 0); cd = ImageDraw.Draw(cres)
        cd.ellipse(P(ux - 3.1, ey - 2.3) + P(ux + 3.1, ey + 2.1), fill=255)
        cd.ellipse(P(ux - 2.6, ey - 3.6) + P(ux + 2.6, ey + 0.6), fill=0)
        for y in range(im.height):
            for x in range(im.width):
                if cres.getpixel((x, y)):
                    edge = any(not cres.getpixel((min(63, max(0, x + ox)), min(63, max(0, y + oy)))) for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    px[x, y] = hexc('#a00c0c' if edge else '#ff2a1a')
    return im


def _flame(seed):
    """fire in flat bands, bottom (row 63) to top: white-yellow, yellow, orange, red-orange, red"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im)
    for k, c in enumerate(('#e0361a', '#ff5a1a', '#ff8a1a', '#ffc030', '#fff2a8')):
        d.rectangle((0, k * 13, 63, min(63, k * 13 + 12)), fill=hexc(c))
    rnd = random.Random(seed)
    for _ in range(30):                                                                       # a few flickering squares at the band edges
        x, y = rnd.randrange(0, 64, 4), rnd.choice((12, 25, 38, 51)); d.rectangle((x, y - 1, x + 3, y + 2), fill=d.im.getpixel((x, y + 4)) if y + 4 < 64 else hexc('#fff2a8'))
    return im


def _tongue():
    im = _flat(PURPLE, 14); d = ImageDraw.Draw(im)
    d.rectangle((28, 0, 35, 63), fill=hexc(PURPLE_DK)); d.rectangle((6, 0, 11, 63), fill=hexc(PURPLE_LT))
    return im


def _stem():
    im = _flat('#5e7a2c', 16); d = ImageDraw.Draw(im)
    for x in range(0, 64, 16):
        d.rectangle((x, 0, x + 2, 63), fill=hexc('#3c5418')); d.rectangle((x + 7, 0, x + 9, 63), fill=hexc('#86a246'))
    return im


def _leaf():
    im = _flat('#3e9a30', 17); d = ImageDraw.Draw(im)
    d.rectangle((30, 0, 33, 63), fill=hexc('#2a6a20'))
    for y in range(4, 64, 14):
        d.rectangle((6, y, 57, y + 2), fill=hexc('#2a6a20'))
    return im


def _chitin(seed):
    """black chitin, flat, with one violet sheen strip and a darker edge"""
    im = _flat(CHITIN, seed, 0.03); d = ImageDraw.Draw(im)
    d.rectangle((10, 0, 17, 63), fill=hexc(CHITIN_LT)); d.rectangle((54, 0, 63, 63), fill=hexc('#0c090f'))
    return im


def textures():
    return {'sal_skin': _skin(11), 'sal_top': _skin_top(), 'sal_skin_dk': _skin_dk(), 'sal_face': _face(), 'sal_flame': _flame(22), 'sal_tongue': _tongue(),
            'sal_stem': _stem(), 'sal_leaf': _leaf(), 'sal_leg': _chitin(23)}


# ---------------------------------------------------------------------------------------------------- models
O = (0, 0, 0)


def _box(fr, to, tex, rot=None, uv=None, tex_y=None, front=None, drop=()):
    """an element around the joint (design units = model units - 8); tex_y: another texture on top and bottom; front: a painted
    texture on the north face, mapped whole; drop: faces left off (hidden inside)"""
    fs = [f for f in ('north', 'south', 'east', 'west', 'up', 'down') if f not in drop]
    u = dict(uv or {})
    if front and 'north' not in u: u['north'] = UV[front]
    e = _el(fr, to, tex, O, rot, u, fs)
    if tex_y:
        for f in ('up', 'down'):
            if f in e['faces']: e['faces'][f]['texture'] = '#' + tex_y
    if front: e['faces']['north']['texture'] = '#' + front
    return e


def _band(e, v0, v1):
    """map every face of an element onto rows v0..v1 (of 16) of its texture"""
    for f in e['faces'].values():
        u1, _a, u2, _b = f['uv']; f['uv'] = [u1, round(v0, 3), u2, round(v1, 3)]
    return e


def body(plain=False):
    """(2.75: plain - no carved face, the dormant pumpkin it hides as) the pumpkin in square tiers, like a stack of rounded crates: a broad middle tier carrying the carved face, narrower tiers
    stepping in above and below, a dark base. Wider than it is tall."""
    if 'sal_face' not in UV: _face()
    return [_box((-12, -17, -10), (12, -15, 10), 'sal_skin_dk', drop=('up',)),
            _box((-17, -15, -15), (17, -11, 15), 'sal_skin', tex_y='sal_top', drop=('up',)),
            _box((-20, -11, -18), (20, 11, 18), 'sal_skin', tex_y='sal_top', front=None if plain else 'sal_face'),
            _box((-17, 11, -15), (17, 15, 15), 'sal_skin', tex_y='sal_top', drop=('down',)),
            _box((-12, 15, -10), (12, 17, 10), 'sal_skin', tex_y='sal_top', drop=('down',)),
            # the ribs: raised square strips down the sides and the back of the middle tier (the front is the face)
            *[_box((x0, -8, z0), (x1, 8, z1), 'sal_skin', tex_y='sal_top', drop=(dr,))
              for sx in (1, -1) for zc in (-8, 8)
              for x0, x1, z0, z1, dr in [(min(sx * 20, sx * 21.2), max(sx * 20, sx * 21.2), zc - 3.5, zc + 3.5, 'west' if sx > 0 else 'east')]],
            *[_box((xc - 3.5, -8, 18), (xc + 3.5, 8, 19.2), 'sal_skin', tex_y='sal_top', drop=('north',)) for xc in (-8, 8)]]


def tongue():
    """from the grin's lower lip: out, down, and curling back up at the tip - square steps (joint = where it leaves the mouth)"""
    return [_box((-2.4, -1.6, -3.5), (2.4, 1.0, 0.5), 'sal_tongue'),
            _box((-2.6, -5.8, -6.0), (2.6, -1.4, -2.6), 'sal_tongue'),
            _box((-2.4, -9.8, -7.8), (2.4, -5.6, -4.6), 'sal_tongue'),
            _box((-2.1, -11.8, -8.0), (2.1, -9.6, -3.4), 'sal_tongue'),
            _box((-1.7, -11.4, -3.6), (1.7, -8.8, -1.4), 'sal_tongue')]


def flame(sx):
    """(2.67) a mouth fire, blocky: square licks stepping out of the corner of the grin - out, up, smaller as they go; yellow at
    the root, red at the tips (sx: which corner)"""
    steps = [((-0.6, 2.8), (-1.6, 1.6), (-1.8, 1.0), (12.8, 16.0)),                 # (root, at the corner of the grin, just in front of it)
             ((1.2, 4.6), (0.2, 3.8), (-2.0, 0.6), (9.6, 12.8)), ((3.0, 6.2), (2.4, 6.2), (-1.8, 0.4), (6.4, 9.6)),
             ((4.4, 7.0), (5.0, 8.6), (-1.5, 0.2), (3.2, 6.4)), ((5.4, 7.4), (7.8, 10.8), (-1.2, 0.0), (0.0, 3.2)),
             ((0.4, 2.6), (1.4, 4.8), (-3.0, -1.2), (6.4, 9.6)), ((0.8, 2.2), (4.4, 6.8), (-2.8, -1.4), (0.0, 3.2))]   # (and a small lick in front)
    out = []
    for (x0, x1), (y0, y1), (z0, z1), (v0, v1) in steps:
        a, b = sorted((sx * x0, sx * x1))
        out.append(_band(_box((a, y0, z0), (b, y1, z1), 'sal_flame'), v0, v1))
    return out


def stem():
    """thick and ribbed, stepping over and hooking down at the end; a flat leaf and a little square vine at its foot"""
    els = [_box((-3, 0, -3), (3, 5, 3), 'sal_stem', drop=('down',)), _box((-2.6, 5, -2.0), (2.6, 8.5, 3.2), 'sal_stem'),
           _box((-2.2, 7.5, 3.0), (2.2, 10.5, 7.2), 'sal_stem'), _box((-1.8, 6.4, 6.6), (1.8, 9.0, 9.4), 'sal_stem'),
           _box((-1.5, 5.0, 8.0), (1.5, 6.8, 9.6), 'sal_stem')]
    els.append(_box((2.5, 0.2, -5), (12, 1.0, 4), 'sal_leaf'))
    els += [_box((-6.4, 0.4, -0.8), (-4.8, 2.0, 0.8), 'sal_stem'), _box((-7.4, 1.8, -0.8), (-5.8, 3.4, 0.8), 'sal_stem'),
            _box((-6.6, 3.2, 0.4), (-5.0, 4.6, 2.0), 'sal_stem')]
    return els


SEG_LEN = 24.0                     # every leg segment is modelled 24 units long, joint at its root, along +y; scaled to fit


def segment(w0, w1, knob, tip=False, spikes=()):
    """a leg segment, square-cut: a chitin knuckle at the joint, a shaft stepping thinner (w0 -> w1 units thick), square bristles
    sticking straight out; tip: ends in a narrow point"""
    els = [_box((-knob, -knob * 0.8, -knob), (knob, knob, knob), 'sal_leg')]                        # (the knuckle: plain chitin, like the rest)
    n = 3
    for k in range(n):
        y0, y1 = SEG_LEN * k / n, SEG_LEN * (k + 1) / n
        w = (w0 + (w1 - w0) * (k + 0.5) / n) / 2
        if tip and k == n - 1:
            els += [_box((-w, y0, -w), (w, y0 + 4.0, w), 'sal_leg'), _box((-w * 0.5, y0 + 4.0, -w * 0.5), (w * 0.5, SEG_LEN, w * 0.5), 'sal_leg')]
        else:
            els.append(_box((-w, y0, -w), (w, y1, w), 'sal_leg'))
    for y, side in spikes:                                                                            # bristles: little square pegs
        w = (w0 + (w1 - w0) * y / SEG_LEN) / 2
        lo, hi = sorted((side * w, side * (w + 1.4)))
        els.append(_box((lo, y, -0.35), (hi, y + 0.7, 0.35), 'sal_leg'))
    return els


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    part('sal_body', body()); part('sal_body_plain', body(plain=True)); part('sal_tongue', tongue()); part('sal_flame_r', flame(1)); part('sal_flame_l', flame(-1))
    part('sal_stem', stem())
    part('sal_femur', segment(1.9, 1.45, 1.2, spikes=((8, 1), (14, -1), (19, 1))))
    part('sal_tibia', segment(1.75, 1.2, 1.4, spikes=((6, -1), (11, 1), (16, -1), (20, 1))))
    part('sal_tarsus', segment(1.5, 0.45, 1.15, tip=True, spikes=((7, 1), (13, -1))))
    return M


# ---------------------------------------------------------------------------------------------------- the stance (world blocks)
LEGS = [  # yaw from his front (+z), hip / knee / ankle / foot (radius, height)
    # (2.67: the hips sit up the pumpkin's sides, the front pair highest - the front legs used to rise straight through the fires
    #  at the corners of the mouth)
    (46, (2.9, 9.6), (7.9, 13.9), (11.2, 6.4), (12.8, 0)), (80, (3.0, 9.0), (8.2, 14.8), (11.0, 6.6), (12.4, 0)),
    (113, (3.0, 8.6), (8.0, 14.6), (10.8, 6.4), (12.2, 0)), (146, (2.9, 8.4), (7.6, 13.6), (10.6, 6.0), (12.4, 0))]


def q_aim(d, twist):
    """the rotation that turns +y to direction d (after a twist about y)"""
    n = math.sqrt(sum(c * c for c in d)); dx, dy, dz = (c / n for c in d)
    ax, az = dz, -dx; s = math.hypot(ax, az)
    ang = math.acos(max(-1.0, min(1.0, dy)))
    tilt = (0.0, 0.0, 0.0, 1.0) if s < 1e-9 else (ax / s * math.sin(ang / 2), 0.0, az / s * math.sin(ang / 2), math.cos(ang / 2))
    return qmul(tilt, qa('y', twist))


# ---------------------------------------------------------------------------------------------------- the rig in poses
U = BODY_S / 16
SIDES = (1, -1)
SEGS = (('f', 'sal_femur'), ('t', 'sal_tibia'), ('s', 'sal_tarsus'))
BODY_PARTS = {  # name: (model, design offset from the pumpkin's centre, scale)
    'body': ('sal_body', (0, 0, 0), BODY_S), 'stem': ('sal_stem', (0, 16.6, 0), BODY_S),         # (2.67: no collar - the legs come out of the pumpkin)
    'tongue': ('sal_tongue', (0, -8.8, -18.4), BODY_S), 'flame_r': ('sal_flame_r', (18.0, -3.4, -18.4), FLAME_S),       # (2.67: from the mouth's corners)
    'flame_l': ('sal_flame_l', (-18.0, -3.4, -18.4), FLAME_S)}
LEG_PARTS = [f'{"r" if s > 0 else "l"}{i}{k}' for s in SIDES for i in range(4) for k, _m in SEGS]
PARTS = list(BODY_PARTS) + LEG_PARTS
MODEL = {**{p: v[0] for p, v in BODY_PARTS.items()}, **{f'{"r" if s > 0 else "l"}{i}{k}': m for s in SIDES for i in range(4) for k, m in SEGS}}
# the gait: a wave, back to front (each leg steps a quarter cycle after the one behind it, the other side half a cycle
# behind) - neighbours never swing toward each other, so the legs stay clear of one another all the way round
GAIT = {(s, i): ((3 - i) * 0.25 + (0.5 if s < 0 else 0.0)) % 1.0 for s in (1, -1) for i in range(4)}
STRIDE, STEP_LIFT, WALK_FRAMES = 11.0, 2.6, 8


def _v(design):
    """design units (his right +x, front -z) -> blocks in the display frame (his left +x, front +z)"""
    x, y, z = design
    return (-x * U, y * U, -z * U)


def _qrot(q, v):
    x, y, z, w = q
    vx, vy, vz = v
    tx, ty, tz = 2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx)
    return (vx + w * tx + (y * tz - z * ty), vy + w * ty + (z * tx - x * tz), vz + w * tz + (x * ty - y * tx))


def leg_joints(side, i, swing=0.0, lift=0.0, dy=0.0, spread=0.0, kneedrop=0.0):
    """hip, knee, ankle, foot in blocks (display frame) for leg i on one side; swing: degrees toward his front"""
    yaw, hip, knee, ankle, foot = LEGS[i]
    a = math.radians((yaw - swing) * side)
    P = lambda r, h: (math.sin(a) * r, max(0.0, h), math.cos(a) * r)
    return [P(hip[0], hip[1] + dy), P(knee[0], knee[1] + dy * 0.7 + lift * 0.45 - kneedrop),
            P(ankle[0] + spread * 0.6, ankle[1] + dy * 0.3 + lift * 0.8 - kneedrop * 0.5), P(foot[0] + spread, foot[1] + lift)]


def pose(body=(0.0, 0.0, 0.0, 1.0), dy=0.0, tongue=(0.0, 0.0, 0.0, 1.0), tongue_s=1.0, flames=1.0, legs=None):
    """{part: (translation, rotation, scale)}; legs: {(side, i): dict(swing=, lift=, spread=, kneedrop=)}"""
    out = {}
    c = (0.0, BODY_Y + dy, 0.0)
    for p, (_m, off, sc) in BODY_PARTS.items():
        r = _qrot(body, _v(off))
        own = tongue if p == 'tongue' else (0.0, 0.0, 0.0, 1.0)
        s = sc * (tongue_s if p == 'tongue' else flames if p.startswith('flame') else 1.0)
        out[p] = ((c[0] + r[0], c[1] + r[1], c[2] + r[2]), qmul(body, own), s)
    for side in SIDES:
        for i in range(4):
            lp = dict((legs or {}).get((side, i), {}))
            pts = leg_joints(side, i, dy=dy, **lp)
            for (A, B), (k, _m) in zip(zip(pts, pts[1:]), SEGS):
                d = tuple(b - a_ for a_, b in zip(A, B)); L = math.sqrt(sum(v * v for v in d))
                out[f'{"r" if side > 0 else "l"}{i}{k}'] = (A, q_aim(d, LEGS[i][0] * side), L * 16 / SEG_LEN)
    return out


def _walk(ph):
    """the gait at phase ph (0..1): every leg at its own point in the wave"""
    def leg(p):
        p %= 1.0
        if p < 0.5: return dict(swing=STRIDE * (1 - 4 * p))                                   # standing: the foot sweeps back
        return dict(swing=-STRIDE + 4 * STRIDE * (p - 0.5), lift=STEP_LIFT if abs(p - 0.75) < 0.13 else 0.0)   # swinging: up and forward
    return {(s, i): leg(ph + GAIT[(s, i)]) for s in SIDES for i in range(4)}


X, Z = (lambda a: qa('x', a)), (lambda a: qa('z', a))
FRONT = lambda **kw: {(s, 0): kw for s in SIDES}
POSES = {
    'stand': pose(),
    'breathe': pose(body=X(-2), dy=0.12, tongue=Z(8), flames=1.12),
    **{f'walk{k}': pose(body=Z(2 if (k // 2) % 2 else -2), dy=(-0.12, 0.08)[(k // 2) % 2], tongue=Z((-8, 8)[(k // 2) % 2]), flames=(1.0, 1.1)[(k // 2) % 2],
                        legs=_walk(k / WALK_FRAMES)) for k in range(WALK_FRAMES)},
    # STOMP: the front pair rears up high - and comes down
    'rear': pose(body=X(-14), dy=0.9, tongue=X(-30), flames=1.3,
                 legs={**{(s, 0): dict(swing=22, lift=6.5) for s in SIDES}, **{(s, 1): dict(swing=10, lift=2.5) for s in SIDES},
                       **{(s, i): dict(swing=-5) for s in SIDES for i in (2, 3)}}),
    'stomp': pose(body=X(10), dy=-0.7, tongue=X(-10), flames=1.45, legs={**{(s, 0): dict(swing=18, spread=2.0) for s in SIDES}, **{(s, 1): dict(swing=8) for s in SIDES}}),
    # EMBER RAIN / THE GLARE: it throws its head back and the fires roar up
    'flare': pose(body=X(-10), dy=0.3, tongue=X(-20), flames=1.75),
    # TONGUE LASH
    'lash_a': pose(body=X(6), dy=-0.2, tongue=X(25), flames=1.2),
    'lash_b': pose(body=X(14), dy=-0.4, tongue=X(-58), tongue_s=2.4, flames=1.2),
    # it falls: the legs buckle out from under it and the pumpkin crashes down
    'fall': pose(body=qmul(X(16), Z(10)), dy=-5.6, tongue=X(35), flames=0.5,
                 legs={(s, i): dict(swing=(-6, 4, -3, 7)[i] * s, spread=3.5, kneedrop=7.0) for s in SIDES for i in range(4)}),
}
# (2.75) THE AWAKENING: a plain pumpkin sitting in the field (legs folded away inside, no fire); it shudders; it lights; its legs
# burst out and it hunkers low; it heaves itself up; it roars
_HALF = 17 * BODY_S / 16
def _dorm(body=(0.0, 0.0, 0.0, 1.0), flames=0.0):
    p = pose(body=body, dy=-(BODY_Y - _HALF), flames=flames, tongue_s=0.0)
    c = p['body'][0]
    for k in LEG_PARTS: p[k] = (c, (0.0, 0.0, 0.0, 1.0), 0.0)
    return p
POSES.update({'dorm': _dorm(), 'dorm_l': _dorm(body=qmul(Z(4), X(-2))), 'dorm_r': _dorm(body=qmul(Z(-4), X(2))), 'dorm_lit': _dorm(body=X(-4), flames=1.5),
              'crouch': pose(body=X(8), dy=-4.6, flames=0.9, tongue_s=0.6, legs={(s, i): dict(spread=3.0, kneedrop=-3.0) for s in SIDES for i in range(4)})})
POSES['rise'] = pose()                               # (the stand, reached slowly: it heaves itself up)
DUR = {'stand': 12, 'breathe': 30, **{f'walk{k}': 40 // WALK_FRAMES for k in range(WALK_FRAMES)}, 'rear': 12, 'stomp': 3, 'flare': 10, 'lash_a': 8, 'lash_b': 3,
       'fall': 30,
       'dorm': 1, 'dorm_l': 3, 'dorm_r': 3, 'dorm_lit': 4, 'crouch': 6, 'rise': 26}
