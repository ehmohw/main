"""2.67: the SCORCHING ARACHNO-LANTERN in the game (from the approved mockup, mockups/arachno_lantern_art.py): a jack-o'-lantern
the size of a house carried on eight long black legs, so tall it walks over the trees.

The rig: every part is an item display standing at the boss itself; where it sits, how it turns and how big it is all live in
its transformation (translation, left rotation, scale), so a pose is a set of transformations and the client glides from one
to the next. The legs walk a tetrapod gait (four legs planted, four swinging): each leg's plane swings about its hip and the
swinging ones lift.
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
def _skin(seed, grooves=True):
    """pumpkin rind: warm orange, deep vertical grooves with a highlight beside each, a little mottling"""
    rnd = random.Random(seed); im = _cloth(ORANGE, seed, var=0.05); px = im.load()
    if grooves:
        for x in range(64):
            g = x % 16
            k = 0.62 if g in (0, 15) else 0.78 if g in (1, 14) else 1.12 if g in (3, 4) else 1.0
            for y in range(64):
                r, gg, b, a = px[x, y]; px[x, y] = (min(255, int(r * k)), min(255, int(gg * k)), min(255, int(b * k)), 255)
    d = ImageDraw.Draw(im)
    for _ in range(18):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        d.point((x, y), fill=hexc(rnd.choice((ORANGE_DK, ORANGE_LT, '#d0661a'))))
    return im


def _skin_top():
    """the top and bottom: ribs running out from the middle, darker toward the stem"""
    im = _skin(12, grooves=False); d = ImageDraw.Draw(im)
    for k in range(12):
        a = k * math.pi / 6
        d.line((32, 32, 32 + 46 * math.cos(a), 32 + 46 * math.sin(a)), fill=hexc(ORANGE_DK), width=2)
    for r, c in ((10, '#c05a12'), (5, '#8a3a0a')):
        d.ellipse((32 - r, 32 - r, 32 + r, 32 + r), fill=hexc(c))
    return im


def _carve(im, holes, teeth=()):
    """carved holes, lit from inside: a dark cut wall round each edge, then deep orange fading to pale yellow toward the middle
    (the colour follows the distance from the edge, so every shape glows evenly); teeth: rind left standing in a hole"""
    from PIL import ImageFilter
    mask = Image.new('L', im.size, 0); md = ImageDraw.Draw(mask)
    for kind, shape in holes:
        (md.polygon if kind == 'poly' else md.ellipse)(shape, fill=255)
    for box in teeth:
        md.rectangle(box, fill=0)
    layers, m = [], mask
    for _ in range(8):
        layers.append(m); m = m.filter(ImageFilter.MinFilter(3))
    # (2.67: as the original art - menacing, near-black holes with only a subtle red glow deep inside, not a cheerful yellow light)
    cols = ['#3a1206', '#1c0806', '#120406', '#170506', '#220708', '#320a0a', '#46100c', '#5c160e']
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            depth = sum(1 for L in layers if L.getpixel((x, y)))
            if depth: px[x, y] = hexc(cols[min(depth, len(cols)) - 1])
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in teeth:                                                              # (the teeth: rind, a lit edge)
        d.line((x0, y1 + 1, x1, y1 + 1), fill=hexc('#6a180c')); d.line((x0, y0, x0, y1), fill=hexc(ORANGE_DK))


def _face():
    """the carved face, 64 x 64 over a 27 x 22 unit plate: big slanting triangle eyes with red crescent pupils, two small round
    spider eyes over each, a little nose, and a wide jagged grin with two teeth hanging down and one standing up"""
    im = _skin(13, grooves=False)
    holes = []
    for sx in (-1, 1):
        cx = 32 + sx * 15
        holes.append(('poly', [(cx - 12, 30), (cx + 11, 30), (cx + sx * 7, 9)]))              # (slanting in: a scowl)
        for k, ey in ((0, 3), (1, 5)):
            ex = cx + sx * (2 + 6 * k)
            holes.append(('ellipse', (ex - 2, ey - 2, ex + 2, ey + 2)))
    holes.append(('poly', [(27, 39), (37, 39), (32, 31)]))
    holes.append(('poly', [(1, 40), (9, 44), (15, 41), (22, 45), (28, 42), (32, 45), (36, 42), (42, 45), (49, 41), (55, 44), (63, 40),
                           (61, 50), (55, 58), (47, 62), (40, 59), (32, 63), (24, 59), (17, 62), (9, 58), (3, 50)]))
    _carve(im, holes, teeth=((15, 44, 20, 50), (44, 44, 49, 50), (22, 56, 26, 61), (38, 56, 42, 61)))
    d = ImageDraw.Draw(im)
    for sx in (-1, 1):                                                                        # (2.67) red crescent pupils, horns toward the nose
        ex, ey = 32 + sx * 16.5, 23.0
        cres = Image.new('L', im.size, 0); cd = ImageDraw.Draw(cres)
        cd.ellipse((ex - 4.2, ey - 5.6, ex + 4.2, ey + 5.6), fill=255)
        cd.ellipse((ex - 3.6 - sx * 3.4, ey - 4.4, ex + 3.6 - sx * 3.4, ey + 4.4), fill=0)
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                if cres.getpixel((x, y)):
                    edge = any(not cres.getpixel((min(63, max(0, x + ox)), min(63, max(0, y + oy)))) for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    px[x, y] = hexc('#a00c0c' if edge else '#ff2a1a')
    for x in range(0, 64, 16):                                                                # faint grooves over the rind only
        for y in range(64):
            r, g, b, a = im.getpixel((x, y))
            if (r, g, b) != hexc(CUT)[:3] and g < 150: im.putpixel((x, y), (int(r * 0.8), int(g * 0.8), int(b * 0.8), 255))
    return im


def _flame(seed):
    """fire from the bottom up: a white-yellow root, orange, a red tip; ragged flicker at the sides"""
    rnd = random.Random(seed); im = Image.new('RGBA', (64, 64)); px = im.load()
    stops = [(0.0, '#e0361a'), (0.35, '#ff7a1a'), (0.65, '#ffc838'), (1.0, '#fff8c8')]
    def col(t):
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1:
                a, b = hexc(c0), hexc(c1); f = (t - t0) / (t1 - t0)
                return tuple(int(a[i] + (b[i] - a[i]) * f) for i in range(3))
        return hexc(stops[-1][1])[:3]
    for y in range(64):
        for x in range(64):
            t = y / 63 + rnd.uniform(-0.06, 0.06) - (0.12 if x in (0, 1, 62, 63) else 0)
            px[x, y] = col(max(0, min(1, t))) + (255,)
    return im


def _tongue():
    im = _cloth(PURPLE, 14, var=0.05); d = ImageDraw.Draw(im)
    d.rectangle((29, 0, 34, 63), fill=hexc(PURPLE_DK))
    for x0 in (8, 48):
        d.line((x0, 0, x0, 63), fill=hexc(PURPLE_LT), width=2)
    rnd = random.Random(15)
    for _ in range(40):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.point((x, y), fill=hexc(PURPLE_LT))
    return im


def _stem():
    im = _cloth('#5e7a2c', 16, var=0.06); d = ImageDraw.Draw(im)
    for x in range(0, 64, 6):
        d.line((x, 0, x + 2, 63), fill=hexc('#3c5418'), width=2)
    for x in range(3, 64, 12):
        d.line((x, 0, x, 63), fill=hexc('#86a246'))
    return im


def _leaf():
    im = _cloth('#3e9a30', 17, var=0.05); d = ImageDraw.Draw(im)
    d.line((32, 0, 32, 63), fill=hexc('#2a6a20'), width=2)
    for y in range(6, 60, 10):
        d.line((32, y, 6, y - 8), fill=hexc('#2a6a20')); d.line((32, y, 58, y - 8), fill=hexc('#2a6a20'))
    return im


def _chitin(seed):
    """black chitin: a faint violet sheen running along it, glints, and bristles"""
    rnd = random.Random(seed); im = _cloth(CHITIN, seed, var=0.05); d = ImageDraw.Draw(im)
    for x in (14, 15, 40):
        d.line((x, 0, x, 63), fill=hexc('#241c2e'))
    for _ in range(30):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.line((x, y, x + 1, y - 2), fill=hexc(CHITIN_LT))
    return im


def _joint():
    """the knuckles: charred black, split by glowing ember cracks"""
    im = _cloth('#1c1010', 18, var=0.05); d = ImageDraw.Draw(im)
    rnd = random.Random(19)
    for _ in range(7):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); pts = [(x, y)]
        for _k in range(5):
            x += rnd.randint(-8, 8); y += rnd.randint(-8, 8); pts.append((x, y))
        d.line(pts, fill=hexc('#9a2a0a'), width=3); d.line(pts, fill=hexc(EMBER), width=1)
    return im


def _collar():
    im = _cloth('#2a1810', 20, var=0.06); d = ImageDraw.Draw(im)
    rnd = random.Random(21)
    for _ in range(26):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.point((x, y), fill=hexc(rnd.choice((EMBER, '#c04010', '#4a2a1a'))))
    return im


def textures():
    return {'sal_skin': _skin(11), 'sal_top': _skin_top(), 'sal_face': _face(), 'sal_flame': _flame(22), 'sal_tongue': _tongue(),
            'sal_stem': _stem(), 'sal_leaf': _leaf(), 'sal_leg': _chitin(23), 'sal_joint': _joint(), 'sal_collar': _collar()}


# ---------------------------------------------------------------------------------------------------- models
O = (0, 0, 0)


def _box(fr, to, tex, rot=None, uv=None, tex_y=None):
    """an element around the joint (design units = model units - 8); tex_y: a different texture for the top/bottom faces"""
    e = _el(fr, to, tex, O, rot, uv)
    if tex_y:
        for f in ('up', 'down'): e['faces'][f]['texture'] = '#' + tex_y
    return e


def _band(e, v0, v1):
    """map every face of an element onto rows v0..v1 (of 16) of its texture"""
    for f in e['faces'].values():
        u1, _a, u2, _b = f['uv']; f['uv'] = [u1, round(v0, 3), u2, round(v1, 3)]
    return e


def body():
    """the pumpkin: eight slices, each a rough octagon (a cross and a diamond), widest at the middle, flattened top and bottom;
    the face plate on the front (-z) in three bands that follow the curve"""
    els = []
    R, H = 20.0, 17.0
    rf = lambda yc: R * max(0.0, 1 - abs(yc / (H + 0.5)) ** 2.6) ** 0.5
    for y0 in range(-16, 16, 4):
        yc = y0 + 2; r = rf(yc)
        els.append(_box((-r, y0, -0.62 * r), (r, y0 + 4, 0.62 * r), 'sal_skin', tex_y='sal_top'))
        els.append(_box((-0.7 * r, y0, -r), (0.7 * r, y0 + 4, r), 'sal_skin', tex_y='sal_top'))
        q = 0.7 * r
        els.append(_box((-q, y0, -q), (q, y0 + 4, q), 'sal_skin', ('y', 45, (0, yc, 0)), tex_y='sal_top'))
    for (y0, y1), (v0, v1) in (((4, 11), (0, 5.1)), ((-4, 4), (5.1, 10.9)), ((-11, -4), (10.9, 16))):  # (three bands down the curve)
        r = max(rf(l + 2) for l in range(-16, 16, 4) if l < y1 and l + 4 > y0)           # (in front of every slice it crosses)
        e = _box((-13.5, y0, -r - 0.45), (13.5, y1, -r + 0.6), 'sal_skin', uv={'north': [0, v0, 16, v1]})
        e['faces']['north']['texture'] = '#sal_face'
        els.append(e)
    return els


def tongue():
    """from the grin's lower lip: out, down, and curling back up at the tip (joint = where it leaves the mouth)"""
    return [_box((-2.4, -1.6, -3.5), (2.4, 1.0, 0.5), 'sal_tongue'),
            _box((-2.7, -6.0, -6.2), (2.7, -1.4, -2.6), 'sal_tongue', ('x', 22.5, (0, -3.7, -4.4))),
            _box((-2.4, -10.0, -8.0), (2.4, -5.6, -4.8), 'sal_tongue', ('x', 22.5, (0, -7.8, -6.4))),
            _box((-2.1, -12.4, -8.1), (2.1, -9.6, -5.3), 'sal_tongue', ('x', -22.5, (0, -11, -6.7))),
            _box((-1.6, -12.6, -6.0), (1.6, -10.6, -3.6), 'sal_tongue', ('x', -45, (0, -11.6, -4.8)))]


def flame(sx):
    """(2.67) a mouth fire: three tongues licking out of the corner of the grin - out to the side and a little forward,
    curling up as they go; yellow at the root, red at the tips (sx: which corner)"""
    out = []
    for dy, dz, L, rise in ((0.0, 0.0, 11.0, 0.9), (1.4, -0.6, 8.0, 1.3), (-1.2, -0.4, 7.0, 0.6)):
        n = 5
        for k in range(n):
            t0, t1 = k / n, (k + 1) / n
            x0, x1 = sx * L * t0, sx * (L * t1 + 0.4)
            y = dy + rise * L * t0 * t0 * 0.9
            w = 2.0 * (1 - k / (n + 0.6)) + 0.3
            z = dz - 0.6 * k
            out.append(_band(_box((min(x0, x1), y - w, z - w * 0.7), (max(x0, x1), y + w + rise * 1.6, z + w * 0.7), 'sal_flame'),
                             16 * (1 - (k + 1) / n), 16 * (1 - k / n)))
    return out


def stem():
    """thick and ribbed, bending over and curling at the end; a broad leaf and a corkscrew vine at its foot"""
    els = [_box((-3, 0, -3), (3, 5, 3), 'sal_stem'), _box((-2.6, 4.5, -2.2), (2.6, 9, 3.0), 'sal_stem', ('x', 22.5, (0, 4.5, 0))),
           _box((-2.2, 8, 0.5), (2.2, 11.5, 6.0), 'sal_stem', ('x', 45, (0, 8, 1.5))), _box((-1.8, 7.5, 5.0), (1.8, 10.5, 8.5), 'sal_stem'),
           _box((-1.5, 6.0, 7.2), (1.5, 8.5, 9.4), 'sal_stem')]
    els.append(_box((2.5, 0.4, -5), (12, 1.0, 4), 'sal_leaf', ('z', -22.5, (2.5, 0.7, 0))))
    for k in range(5):                                                                               # the vine: a little corkscrew
        a = k * 1.3; x, z = -4 - 2.2 * math.cos(a), 2.2 * math.sin(a)
        els.append(_box((x - 0.5, 1 + k * 1.6, z - 0.5), (x + 0.5, 2.4 + k * 1.6, z + 0.5), 'sal_stem'))
    return els


def collar():
    """the charred ring under the pumpkin the legs come out of (8 sockets)"""
    els = [_box((-14, -3, -6), (14, 3, 6), 'sal_collar'), _box((-6, -3, -14), (6, 3, 14), 'sal_collar'),
           _box((-9.5, -3, -9.5), (9.5, 3, 9.5), 'sal_collar', ('y', 45, (0, 0, 0))), _box((-8, -6, -8), (8, -3, 8), 'sal_collar')]
    return els


SEG_LEN = 24.0                     # every leg segment is modelled 24 units long, joint at its root, along +y; scaled to fit


def segment(w0, w1, knob, tip=False, spikes=()):
    """a leg segment: a knob at the joint, a tapering shaft (w0 -> w1 units thick), bristles/spikes; tip: ends in a point"""
    els = [_box((-knob, -knob * 0.7, -knob), (knob, knob * 0.9, knob), 'sal_joint')]
    n = 4
    for k in range(n):
        y0, y1 = SEG_LEN * k / n, min(SEG_LEN, SEG_LEN * (k + 1) / n + 0.3)
        w = (w0 + (w1 - w0) * (k + 0.5) / n) / 2
        if tip and k == n - 1:
            els += [_box((-w, y0, -w), (w, y0 + 3.5, w), 'sal_leg'), _box((-w * 0.55, y0 + 3.4, -w * 0.55), (w * 0.55, SEG_LEN - 0.4, w * 0.55), 'sal_leg')]
        else:
            els.append(_box((-w, y0, -w), (w, y1, w), 'sal_leg'))
    for y, side in spikes:                                                                            # bristles, raked back
        w = (w0 + (w1 - w0) * y / SEG_LEN) / 2
        lo, hi = sorted((side * w, side * (w + 1.5)))
        els.append(_box((lo, y, -0.3), (hi, y + 0.6, 0.3), 'sal_leg', ('z', 22.5 * side, (side * w, y, 0))))
    return els


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    part('sal_body', body()); part('sal_tongue', tongue()); part('sal_flame_r', flame(1)); part('sal_flame_l', flame(-1))
    part('sal_stem', stem()); part('sal_collar', collar())
    part('sal_femur', segment(1.9, 1.45, 1.2, spikes=((8, 1), (14, -1), (19, 1))))
    part('sal_tibia', segment(1.75, 1.2, 1.4, spikes=((6, -1), (11, 1), (16, -1), (20, 1))))
    part('sal_tarsus', segment(1.5, 0.45, 1.15, tip=True, spikes=((7, 1), (13, -1))))
    return M


# ---------------------------------------------------------------------------------------------------- the stance (world blocks)
LEGS = [  # yaw from his front (+z), hip / knee / ankle / foot (radius, height)
    (46, (2.9, 6.3), (7.9, 13.9), (11.2, 6.4), (12.8, 0)), (80, (3.0, 6.1), (8.2, 14.8), (11.0, 6.6), (12.4, 0)),
    (113, (3.0, 6.1), (8.0, 14.6), (10.8, 6.4), (12.2, 0)), (146, (2.9, 6.3), (7.6, 13.6), (10.6, 6.0), (12.4, 0))]


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
    'body': ('sal_body', (0, 0, 0), BODY_S), 'collar': ('sal_collar', (0, -17.0, 0), BODY_S * 0.9), 'stem': ('sal_stem', (0, 15.5, 0), BODY_S),
    'tongue': ('sal_tongue', (0, -9.4, -19.0), BODY_S), 'flame_r': ('sal_flame_r', (12.6, -4.8, -19.4), FLAME_S),       # (2.67: from the mouth's corners)
    'flame_l': ('sal_flame_l', (-12.6, -4.8, -19.4), FLAME_S)}
LEG_PARTS = [f'{"r" if s > 0 else "l"}{i}{k}' for s in SIDES for i in range(4) for k, _m in SEGS]
PARTS = list(BODY_PARTS) + LEG_PARTS
MODEL = {**{p: v[0] for p, v in BODY_PARTS.items()}, **{f'{"r" if s > 0 else "l"}{i}{k}': m for s in SIDES for i in range(4) for k, m in SEGS}}
GROUP_A = {(1, 0), (-1, 1), (1, 2), (-1, 3)}          # (the tetrapod gait: these four swing while the others stand)


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
    """the gait at phase ph (0..1) for group A; group B half a cycle behind"""
    def leg(p):
        p %= 1.0
        if p < 0.5: return dict(swing=14 * (1 - 4 * p))                           # standing: the foot sweeps back
        return dict(swing=-14 + 56 * (p - 0.5), lift=2.4 if abs(p - 0.75) < 0.01 else 0.0)   # swinging: up and forward
    return {(s, i): leg(ph if (s, i) in GROUP_A else ph + 0.5) for s in SIDES for i in range(4)}


X, Z = (lambda a: qa('x', a)), (lambda a: qa('z', a))
FRONT = lambda **kw: {(s, 0): kw for s in SIDES}
POSES = {
    'stand': pose(),
    'breathe': pose(body=X(-2), dy=0.12, tongue=Z(8), flames=1.12),
    **{f'walk{k}': pose(body=Z(2 if k % 2 else -2), dy=(-0.12, 0.08)[k % 2], tongue=Z((-8, 8)[k % 2]), flames=(1.0, 1.1)[k % 2], legs=_walk(k / 4)) for k in range(4)},
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
DUR = {'stand': 12, 'breathe': 30, 'walk0': 10, 'walk1': 10, 'walk2': 10, 'walk3': 10, 'rear': 12, 'stomp': 3, 'flare': 10, 'lash_a': 8, 'lash_b': 3,
       'fall': 30}
