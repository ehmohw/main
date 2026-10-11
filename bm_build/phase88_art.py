"""2.67: THE GUTTER GENTRY - the art (from the reference sheet): BATTY, a navy bat with a grey-and-black striped
body, brown wings, sleepy yellow eyes and a toothy grin, who roosts upside down; EGGBERT, a spotted egg cracked
open across the middle with black ooze and two pale glowing eyes inside, black dripping arms and talons, a broken pipe
on top; THE COUNT, a pale blue grumpy blob with a black top hat (red band), little stick legs and a cane.

Front = -z (north), like the Arachno-Lantern. Design units with the joint at 0 (model = design + 8).
"""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import _cloth, _el, hexc, qa, qmul

FUR, FUR_LT, FUR_DK = '#2c2c4c', '#40406a', '#1a1a30'
BELLY, STRIPE = '#a8acac', '#262626'
WING, WING_LT = '#8a5a38', '#c0a070'
EYE, PUPIL, NOSE, TEETH = '#e8dc2a', '#1a1a10', '#e8a0b0', '#dcdcdc'
SHELL, SHELL_DK, SPOT = '#d4d0c8', '#b0aca4', '#56606c'
GOO, GOO_HL, EGG_EYE = '#121214', '#3a3a40', '#eef6b0'
PIPE = '#9a9ca0'
BLOB, BLOB_DK, BLOB_LN = '#c8dcf2', '#9ab4d6', '#2a3a56'
HAT, BAND, BLACK = '#1c1c1e', '#c83434', '#141416'


# ---------------------------------------------------------------------------------------------------- textures
def _noise(c, seed, var=0.05):
    return _cloth(c, seed, var=var)


def _fur(seed=1):
    im = _noise(FUR, seed, 0.07); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(120):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        d.line((x, y, x + rnd.choice((-1, 0, 1)), y + 2), fill=hexc(rnd.choice((FUR_LT, FUR_DK))))
    return im


def _bat_face():
    """(laid across the five front plates of his round head) heavy-lidded yellow eyes looking down and aside, a small pink
    nose, and under it a wide grey mouth-plate - a closed grin with a fang at each corner"""
    im = _fur(3); d = ImageDraw.Draw(im)
    for cx, look in ((21, 2), (43, -2)):
        d.ellipse((cx - 10, 13, cx + 10, 33), fill=hexc('#0c0c16'))                        # dark rims
        d.ellipse((cx - 8, 15, cx + 8, 31), fill=hexc(EYE))
        d.ellipse((cx - 4 + look, 22, cx + 3 + look, 30), fill=hexc(PUPIL))
        d.point((cx - 1 + look, 24), fill=hexc('#ffffff')); d.point((cx + look, 24), fill=hexc('#ffffff'))
        d.chord((cx - 11, 6, cx + 11, 28), 180, 360, fill=hexc(FUR_DK))                     # heavy lids, half shut
        d.arc((cx - 11, 6, cx + 11, 28), 180, 360, fill=hexc('#06060c'), width=2)
        d.line((cx - 9, 17 + (2 if cx < 32 else -2), cx + 9, 17 - (2 if cx < 32 else -2)), fill=hexc('#06060c'), width=2)
    d.polygon([(29, 33), (35, 33), (32, 37)], fill=hexc(NOSE)); d.point((32, 34), fill=hexc('#ffd0e0'))
    d.rounded_rectangle((15, 39, 49, 55), radius=7, fill=hexc(TEETH), outline=hexc('#141418'), width=2)
    d.arc((19, 36, 45, 52), 20, 160, fill=hexc('#2a2a30'), width=2)                           # the grin line
    d.polygon([(16, 46), (20, 46), (18, 51)], fill=hexc('#ffffff')); d.polygon([(44, 46), (48, 46), (46, 51)], fill=hexc('#ffffff'))
    for cx in (10, 54): d.ellipse((cx - 3, 34, cx + 3, 38), fill=hexc('#3c3256'))
    return im


def _belly():
    """grey with two broad black bands (it runs down his body: v 0 = his chest, 16 = his hips)"""
    im = _noise(BELLY, 5, 0.04); d = ImageDraw.Draw(im)
    for y0 in (14, 34): d.rectangle((0, y0, 63, y0 + 10), fill=hexc(STRIPE))
    for y in (0, 63): d.line((0, y, 63, y), fill=hexc('#8a8e8e'))
    return im


def _wing():
    """the right wing in its own square (x 0..24 out from the shoulder, y +6 at the top .. -18 at the hip): the arm along the
    top out to the wrist, four fingers fanning back from the wrist to a scalloped trailing edge, tan panels by each finger;
    everything outside the membrane is clear"""
    S = 64 / 24.0
    P = lambda x, y: (x * S, (6 - y) * S)
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    wrist = (21.5, 5.0)
    tips = [(23.8, -1.0), (21.5, -9.5), (14.5, -15.5), (6.5, -17.8)]
    edge = [(0.0, 5.2), (11, 5.8), wrist, tips[0]]
    for i in range(len(tips)):                                                               # scallops between the finger tips
        a, b2 = tips[i], tips[i + 1] if i + 1 < len(tips) else (0.0, -16.5)
        mid = ((a[0] + b2[0]) / 2 + 1.6, (a[1] + b2[1]) / 2 + 2.2)
        edge += [mid, b2]
    d.polygon([P(*p) for p in edge], fill=hexc(WING))
    for t in tips:                                                                           # the tan panel along each finger
        d.polygon([P(*wrist), P(*t), P(wrist[0] + (t[0] - wrist[0]) * 0.55 - 2.6, wrist[1] + (t[1] - wrist[1]) * 0.55 + 0.8)], fill=hexc(WING_LT))
    d.polygon([P(0, 4.6), P(*wrist), P(10, -2), P(0, -6)], fill=hexc(WING_LT))
    for t in tips: d.line([P(*wrist), P(*t)], fill=hexc(FUR), width=3)
    d.line([P(0, 5.2), P(11, 5.8), P(*wrist)], fill=hexc(FUR), width=5)                      # the arm
    d.ellipse([P(wrist[0] - 0.9, wrist[1] + 0.9), P(wrist[0] + 0.9, wrist[1] - 0.9)], fill=hexc(FUR_DK))
    d.polygon([P(wrist[0] - 0.4, wrist[1] + 0.6), P(wrist[0] + 1.6, wrist[1] + 2.6), P(wrist[0] + 1.0, wrist[1] + 0.2)], fill=hexc(FUR))   # a thumb claw
    return im


def _tail():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(4, 0), (60, 0), (32, 62)], fill=hexc(WING)); d.polygon([(18, 0), (46, 0), (32, 40)], fill=hexc(WING_LT))
    return im


def _shell(seed=11):
    rnd = random.Random(seed); im = _noise(SHELL, seed, 0.03); d = ImageDraw.Draw(im)
    for _ in range(9):
        x, y, r = rnd.randint(0, 63), rnd.randint(0, 63), rnd.randint(3, 8)
        d.ellipse((x - r, y - r, x + r, y + r), fill=hexc('#8a929c'))
    for _ in range(4):                                                                       # ooze stains
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=hexc(GOO)); d.rectangle((x - 1, y, x, y + 4), fill=hexc(GOO))
    for _ in range(14):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=hexc('#eeeae2'))
    return im


def _shell_plain():
    return _noise(SHELL, 41, 0.025)


def _spot():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 6, 60, 58), fill=hexc(SPOT)); d.ellipse((14, 14, 30, 26), fill=hexc('#6c7682'))
    return im


def _egg_face():
    """(laid across the five front plates) the crack: jagged top and bottom edges right across, glossy black ooze inside with
    two pale glowing eyes - the big one on his right (your left) - and drips over the lower shell"""
    im = _shell(13); d = ImageDraw.Draw(im)
    top = [(0, 26), (5, 18), (9, 27), (15, 13), (20, 26), (26, 12), (31, 25), (37, 14), (42, 26), (48, 15), (53, 27), (58, 18), (64, 24)]
    bot = [(64, 40), (59, 48), (54, 39), (49, 50), (44, 40), (38, 52), (33, 41), (27, 51), (22, 40), (16, 49), (11, 39), (5, 47), (0, 41)]
    d.polygon(top + bot, fill=hexc(GOO))
    for pts in (top, bot):
        for i in range(len(pts) - 1): d.line(pts[i] + pts[i + 1], fill=hexc('#6a6a70'), width=1)
    for (x, y, h) in ((9, 44, 9), (24, 46, 15), (36, 50, 8), (47, 47, 13), (57, 45, 6)):
        d.rectangle((x - 1, y, x + 1, min(63, y + h)), fill=hexc(GOO)); d.ellipse((x - 2, min(61, y + h - 1), x + 2, min(63, y + h + 2)), fill=hexc(GOO))
    for (cx, cy, r) in ((24, 31, 7), (41, 35, 4)):
        d.ellipse((cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2), fill=hexc('#4a5034'))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hexc(EGG_EYE))
        d.ellipse((cx - r + 1, cy - r + 1, cx - r // 3, cy - r // 3), fill=hexc('#ffffff'))
    for (x, y) in ((14, 22), (31, 44), (52, 31), (47, 20)): d.line((x, y, x + 3, y), fill=hexc(GOO_HL))
    return im


def _goo():
    im = _noise(GOO, 17, 0.08); d = ImageDraw.Draw(im); rnd = random.Random(17)
    for _ in range(26):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); d.line((x, y, x + 2, y), fill=hexc(GOO_HL))
    return im


def _blob():
    im = _noise(BLOB, 19, 0.02)
    for y in range(64):
        k = 1.04 - 0.16 * (y / 63)
        for x in range(64):
            r, g, b, a = im.getpixel((x, y)); im.putpixel((x, y), (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), 255))
    return im


def _blob_face():
    """(laid across the five front plates) small round eyes with dot pupils under a furrowed brow, two creases for a nose, and
    a flat frown with two little fangs pointing up"""
    im = _blob(); d = ImageDraw.Draw(im)
    for cx in (23, 41):
        d.ellipse((cx - 5, 24, cx + 5, 34), fill=hexc('#f6f9ff'), outline=hexc(BLOB_LN), width=2)
        d.ellipse((cx - 2, 27, cx + 1, 30), fill=hexc('#0e0e0e'))
    d.line((15, 19, 22, 23), fill=hexc(BLOB_LN), width=2); d.line((22, 23, 30, 20), fill=hexc(BLOB_LN), width=2)     # the furrowed brow: a W
    d.line((34, 20, 42, 23), fill=hexc(BLOB_LN), width=2); d.line((42, 23, 49, 19), fill=hexc(BLOB_LN), width=2)
    d.arc((24, 10, 40, 22), 200, 340, fill=hexc(BLOB_DK), width=2)
    d.arc((26, 34, 31, 40), 300, 80, fill=hexc(BLOB_DK), width=2); d.arc((33, 34, 38, 40), 100, 240, fill=hexc(BLOB_DK), width=2)
    d.line((18, 47, 46, 47), fill=hexc(BLOB_LN), width=2); d.arc((14, 45, 22, 53), 180, 270, fill=hexc(BLOB_LN), width=2)
    d.arc((42, 45, 50, 53), 270, 360, fill=hexc(BLOB_LN), width=2)
    for x in (23, 41): d.polygon([(x - 2, 47), (x + 2, 47), (x, 43)], fill=hexc('#ffffff'))
    return im


def _claw():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(20, 0), (44, 0), (36, 50), (30, 63)], fill=hexc(GOO)); d.line((26, 4, 31, 40), fill=hexc(GOO_HL))
    return im


def textures():
    return {'gnt_fur': _fur(1), 'gnt_bat_face': _bat_face(), 'gnt_belly': _belly(), 'gnt_wing': _wing(), 'gnt_tail': _tail(),
            'gnt_shell': _shell_plain(), 'gnt_spot': _spot(), 'gnt_egg_face': _egg_face(), 'gnt_goo': _goo(), 'gnt_pipe': _noise(PIPE, 23, 0.06), 'gnt_claw': _claw(),
            'gnt_blob': _blob(), 'gnt_blob_face': _blob_face(), 'gnt_black': _noise(BLACK, 29, 0.05),
            'gnt_hat': _noise(HAT, 31, 0.04), 'gnt_band': _noise(BAND, 37, 0.04)}


# ---------------------------------------------------------------------------------------------------- models
O = (0, 0, 0)
T11 = math.tan(math.radians(11.25))


def _box(fr, to, tex, rot=None, uv=None, front=None, rest=None, faces=None):
    e = _el(fr, to, tex, O, rot, uv, faces)
    if front: e['faces']['north']['texture'] = '#' + front
    if rest:
        for f in ('south', 'east', 'west', 'up', 'down'):
            if f in e['faces']: e['faces'][f]['texture'] = '#' + rest
    return e


def _round(y0, y1, step, rf, tex, band=None, cx=0.0, cz=0.0):
    """a round solid in slices: each slice the union of six boxes whose corners all sit on the circle - two long ones and
    their crosswise twins at 0 and 45 degrees, two squares at +-22.5 - so nothing pokes out past radius rf(y); band: map
    each slice onto its own rows of the texture (top of the solid = row 0)"""
    out = []
    y = y0
    A, B, C = math.cos(math.radians(22.5)), math.sin(math.radians(22.5)), math.sqrt(0.5)
    while y < y1 - 1e-6:
        y2 = min(y1, y + step); r = rf((y + y2) / 2)
        if r > 0.35:
            uv = None
            if band:
                v0 = 16 * (y1 - y2) / (y1 - y0); v1 = 16 * (y1 - y) / (y1 - y0)
                uv = {f: [0, round(v0, 3), 16, round(v1, 3)] for f in ('north', 'south', 'east', 'west')}
            for (hx, hz), ang in (((A, B), 0), ((B, A), 0), ((A, B), 45), ((B, A), 45), ((C, C), 22.5), ((C, C), -22.5)):
                out.append(_box((cx - hx * r, y, cz - hz * r), (cx + hx * r, y2, cz + hz * r), tex, ('y', ang, (cx, y, cz)) if ang else None, uv))
        y = y2
    return out


def _face(y0, y1, rf, tex, base, cols=5, lift=0.35):
    """a face laid round a round solid's front: cols plates (0, +-22.5, +-45 degrees) in three bands, each a slice of the
    face texture - so it follows the curve"""
    out = []
    angs = {3: (-22.5, 0, 22.5), 5: (-45, -22.5, 0, 22.5, 45)}[cols]
    bands = 3
    for bi in range(bands):
        ya, yb = y0 + (y1 - y0) * bi / bands, y0 + (y1 - y0) * (bi + 1) / bands
        r = max(rf(ya), rf((ya + yb) / 2), rf(yb - 0.01)) + lift
        w = r * T11 * 1.04
        v0, v1 = 16 * (1 - (bi + 1) / bands), 16 * (1 - bi / bands)
        for ci, ang in enumerate(angs):
            u0, u1 = 16 * ci / cols, 16 * (ci + 1) / cols
            e = _box((-w, ya, -r - 0.3), (w, yb, -r + 0.4), base, ('y', ang, (0, ya, 0)) if ang else None,
                     uv={'north': [round(u0, 3), round(v0, 3), round(u1, 3), round(v1, 3)]})
            e['faces']['north']['texture'] = '#' + tex
            out.append(e)
    return out


def _decal(y, ang, size, rf, tex, base):
    """a round spot laid on a round solid's surface at height y, turned ang degrees round from the front"""
    r = rf(y) + 0.25
    e = _box((-size, y - size, -r - 0.2), (size, y + size, -r + 0.3), base, ('y', ang, (0, y, 0)) if ang else None,
             uv={'north': [0, 0, 16, 16]}, faces=('north',))
    e['faces']['north']['texture'] = '#' + tex
    return e


def bat_body():
    head = lambda y: 9.6 * max(0.0, 1 - ((y - 13.5) / 8.6) ** 2) ** 0.5
    body = lambda y: 5.6 - 1.0 * max(0.0, (-y - 4) / 10)
    els = _round(5, 22, 2, head, 'gnt_fur') + _face(7, 19.5, head, 'gnt_bat_face', 'gnt_fur')
    els += _round(-14, 5, 2, body, 'gnt_belly', band=True)
    for zz, ang in ((-1, 0), (-1, 45), (-1, -45), (1, 0), (1, 45), (1, -45)):              # the ruff: tufts all round
        els.append(_box((-1.3, 2.4, -9.4) if zz < 0 else (-1.3, 2.4, 6.6), (1.3, 5.6, -6.6) if zz < 0 else (1.3, 5.6, 9.4), 'gnt_fur',
                        ('y', ang, (0, 4, 0)) if ang else None))
    for sx in (1, -1):
        lo, hi = sorted((sx * 6.6, sx * 9.4))
        els.append(_box((lo, 2.4, -1.3), (hi, 5.6, 1.3), 'gnt_fur'))
    els += _round(3, 6.5, 1.75, lambda y: 7.6, 'gnt_fur')
    for sx in (1, -1):
        lo, hi = sorted((sx * 3.6, sx * 7.2))
        els.append(_box((lo, 18.5, -1.4), (hi, 23.6, 1.4), 'gnt_fur', ('z', -22.5 * sx, (sx * 5.5, 19, 0))))     # the ears
        lo, hi = sorted((sx * 1.4, sx * 3.4))
        els.append(_box((lo, -18.5, -1.1), (hi, -13, 1.1), 'gnt_fur', ('z', 22.5 * sx, (sx * 2.4, -14, 0))))     # the legs, splayed
        lo, hi = sorted((sx * 3.0, sx * 5.4))
        els.append(_box((lo, -21.5, -1.0), (hi, -18.2, 1.0), 'gnt_fur'))
        for k in (-1, 0, 1):                                                                 # the toes
            x = sx * 4.2 + k * 0.9
            els.append(_box((x - 0.4, -23.6, -0.4 + k * 0.6), (x + 0.4, -21.3, 0.4 + k * 0.6), 'gnt_fur'))
    els += _round(21, 23.6, 1.3, lambda y: 1.5, 'gnt_pipe')                                  # the little grey cap
    t = _box((-3.4, -21, 1.6), (3.4, -13.6, 2.0), 'gnt_tail', faces=('north', 'south'))       # the tail membrane
    els.append(t)
    return els


def bat_wing(sx):
    """one quad, the wing drawn on it (clear outside the membrane); seen from both sides"""
    lo, hi = sorted((0, sx * 24))
    uv = [0, 0, 16, 16] if sx < 0 else [16, 0, 0, 16]
    return [_box((lo, -18, -0.15), (hi, 6, 0.15), 'gnt_wing', uv={'north': uv, 'south': [uv[2], 0, uv[0], 16]}, faces=('north', 'south'))]


def egg_body():
    rf = lambda y: 11.2 * max(0.0, 1 - ((y + 2.5) / 12.2) ** 2) ** 0.5 if y < -2.5 else 11.2 * max(0.0, 1 - ((y + 2.5) / 19.5) ** 2) ** 0.5
    els = _round(-14, 16.5, 2, rf, 'gnt_shell') + _face(-3, 10, rf, 'gnt_egg_face', 'gnt_shell')
    for (y, ang, sz) in ((12.5, -22.5, 2.6), (13.5, 22.5, 1.8), (-7.5, 45, 3.0), (-9.5, -22.5, 2.2), (-5.5, -45, 1.6), (5, 45, 1.8)):   # big blue-grey spots
        els.append(_decal(y, ang, sz, rf, 'gnt_spot', 'gnt_shell'))
    els += _round(14.6, 19, 1.5, lambda y: 2.1, 'gnt_pipe', cx=1.2)                          # the broken pipe on top
    els.append(_box((-1.3, 18.6, -2.6), (3.7, 19.6, 2.6), 'gnt_pipe', ('z', -22.5, (1.2, 18.6, 0))))
    for sx in (1, -1):
        els += _round(-21, -12, 3, lambda y: 2.6, 'gnt_goo', cx=sx * 4.4)                    # the legs
        for k in (-1, 0, 1):                                                                 # three talons forward, one back
            x = sx * 4.4 + k * 2.2
            els.append(_box((x - 0.7, -22.6, -6.6), (x + 0.7, -21.0, -1.6), 'gnt_goo', ('y', 22.5 * k, (x, -22, -1.6))))
            els.append(_box((x - 0.35, -23.4, -7.4), (x + 0.35, -22.2, -6.0), 'gnt_goo'))
        els.append(_box((sx * 4.4 - 0.6, -22.6, 1.4), (sx * 4.4 + 0.6, -21.2, 4.2), 'gnt_goo'))
    return els


def egg_arm(sx):
    def bx(x0, x1, y0, y1, z0, z1, rot=None, tex='gnt_goo', faces=None):
        lo, hi = sorted((sx * x0, sx * x1))
        return _box((lo, y0, z0), (hi, y1, z1), tex, rot, faces=faces)
    els = [bx(0, 10.5, -1.5, 1.5, -1.5, 1.5), bx(9.0, 11.8, -9.5, 0.4, -1.3, 1.3), bx(8.6, 12.4, -11.2, -8.8, -1.8, 1.8)]
    for k in (-1.5, -0.5, 0.5, 1.5):                                                         # four long claws
        x = 10.5 + k * 1.15
        lo, hi = sorted((sx * (x - 0.9), sx * (x + 0.9)))
        els.append(_box((lo, -19.5, -0.05), (hi, -10.8, 0.05), 'gnt_claw', ('z', 11.25 * sx * k if abs(k) < 1 else 22.5 * sx * (1 if k > 0 else -1), (sx * x, -11, 0)),
                        faces=('north', 'south')))
    for x, h in ((3, 3.2), (6.5, 2.0)):
        lo, hi = sorted((sx * (x - 0.5), sx * (x + 0.5)))
        els.append(_box((lo, -1.5 - h, -0.5), (hi, -1.5, 0.5), 'gnt_goo'))
    return els


def blob_body():
    rf = lambda y: 13.2 * max(0.0, 1 - ((y + 2.0) / 14.2) ** 2) ** 0.5 if y > -2 else 13.2 * max(0.0, 1 - ((y + 2.0) / 7.6) ** 2) ** 0.5
    els = _round(-8, 12, 2, rf, 'gnt_blob') + _face(-5, 8, rf, 'gnt_blob_face', 'gnt_blob')
    for sx in (1, -1):                                                                       # the drooping shoulders
        els += _round(-6.5, 0, 1.6, lambda y: 3.3 * max(0.0, 1 - ((y + 3.2) / 3.6) ** 2) ** 0.5, 'gnt_blob', cx=sx * 12.6)
        els += _round(-7.6, -2.5, 1.7, lambda y: 2.4 * max(0.0, 1 - ((y + 5) / 2.8) ** 2) ** 0.5, 'gnt_blob', cx=sx * 14.8)
        lo, hi = sorted((sx * 3.2, sx * 4.0))
        els.append(_box((lo, -20.5, -0.4), (hi, -7.5, 0.4), 'gnt_black'))                    # stick legs
        lo, hi = sorted((sx * 2.0, sx * 5.0))
        els.append(_box((lo, -21.6, -4.2), (hi, -20.2, 1.2), 'gnt_black'))                   # pointed shoes
        lo, hi = sorted((sx * 2.8, sx * 4.2))
        els.append(_box((lo, -21.4, -5.6), (hi, -20.6, -4.0), 'gnt_black'))
    return els


def blob_hat():
    return _round(0, 1.2, 1.2, lambda y: 9.0, 'gnt_hat') + _round(1.2, 13.5, 2.05, lambda y: 5.8, 'gnt_hat') + \
        _round(1.6, 3.8, 2.2, lambda y: 6.05, 'gnt_band') + _round(13.2, 13.8, 0.6, lambda y: 5.9, 'gnt_hat')


def blob_cane():
    return [_box((-0.5, -21.5, -0.5), (0.5, 3.0, 0.5), 'gnt_black'), _box((-0.5, 2.2, -0.5), (3.9, 3.3, 0.5), 'gnt_black'),
            _box((3.0, 0.0, -0.5), (4.1, 3.2, 0.5), 'gnt_black'), _box((-0.75, -22.2, -0.75), (0.75, -21.2, 0.75), 'gnt_pipe')]


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    part('gnt_bat_body', bat_body()); part('gnt_bat_wing_r', bat_wing(1)); part('gnt_bat_wing_l', bat_wing(-1))
    part('gnt_egg_body', egg_body()); part('gnt_egg_arm_r', egg_arm(1)); part('gnt_egg_arm_l', egg_arm(-1))
    part('gnt_blob_body', blob_body()); part('gnt_blob_hat', blob_hat()); part('gnt_blob_cane', blob_cane())
    return M


# ---------------------------------------------------------------------------------------------------- poses
# a pose: {part: (translation in blocks, left rotation, scale)} at the boss's feet, facing the boss's way
S_BAT, S_EGG, S_BLOB = 1.05, 1.35, 1.05
U = lambda s: s / 16
I = (0.0, 0.0, 0.0, 1.0)


def _qrot(q, v):
    x, y, z, w = q; vx, vy, vz = v
    t = (2 * (y * vz - z * vy), 2 * (z * vx - x * vz), 2 * (x * vy - y * vx))
    return (vx + w * t[0] + y * t[2] - z * t[1], vy + w * t[1] + z * t[0] - x * t[2], vz + w * t[2] + x * t[1] - y * t[0])


def _conv(q):
    """a rotation in the model's frame -> the display's (an item display shows its model turned half round: x and z flip)"""
    return (-q[0], q[1], -q[2], q[3])


def _place(root, body_q, offs, s, body_scale=None):
    """parts hung off the body: design offsets (units) turned with the body; root = the body's joint above the feet (blocks);
    rotations are given in the model's frame"""
    out = {}
    bq = _conv(body_q)
    for part, (off, q) in offs.items():
        v = _qrot(bq, (-off[0] * U(s), off[1] * U(s), -off[2] * U(s)))
        sc = body_scale if (part == 'body' and body_scale) else s
        out[part] = ((round(root[0] + v[0], 4), round(root[1] + v[1], 4), round(root[2] + v[2], 4)), qmul(bq, _conv(q)), sc)
    return out


def bat_pose(flap=0.0, roost=False, lean=0.0, fold=0.0):
    body_q = qa('z', 180) if roost else qa('x', lean)
    root = (0, 2.4, 0) if roost else (0, 23.6 * U(S_BAT), 0)
    return _place(root, body_q, {'body': ((0, 0, 0), I),
                                 'wing_r': ((5.0, 4.2, 0.8), qmul(qa('z', -flap), qa('y', fold))),
                                 'wing_l': ((-5.0, 4.2, 0.8), qmul(qa('z', flap), qa('y', -fold)))}, S_BAT)


def egg_pose(lean=0.0, sway=0.0, arm_r=0.0, arm_l=0.0, up=0.0):
    body_q = qmul(qa('z', sway), qa('x', lean))
    return _place((0, 23.4 * U(S_EGG), 0), body_q, {'body': ((0, 0, 0), I),
                                                    'arm_r': ((10.0, 4.0, -2.0), qmul(qa('x', -arm_r), qa('z', -up))),
                                                    'arm_l': ((-10.0, 4.0, -2.0), qmul(qa('x', -arm_l), qa('z', up)))}, S_EGG)


def blob_pose(sq=1.0, hat_up=0.0, hat_tilt=-8.0, cane=0.0):
    s = S_BLOB
    wide = (s * (2 - sq) ** 0.5, s * sq, s * (2 - sq) ** 0.5)
    root = (0, 21.6 * U(s), 0)
    out = _place(root, I, {'body': ((0, 0, 0), I), 'hat': ((0, (11.2 * sq) + hat_up, -0.5), qa('z', hat_tilt)),
                           'cane': ((-16.0, 0.6, -1.4), qa('x', -cane))}, s, body_scale=wide)
    return out


POSES = {
    'bat': {'roost': bat_pose(roost=True, flap=-8), 'fly_a': bat_pose(flap=24, lean=8), 'fly_b': bat_pose(flap=-26, lean=8),
            'screech': bat_pose(flap=6, lean=-22, fold=-20)},
    'egg': {'idle': egg_pose(), 'walk_a': egg_pose(sway=6, arm_r=12, arm_l=-12), 'walk_b': egg_pose(sway=-6, arm_r=-12, arm_l=12),
            'swipe': egg_pose(lean=12, arm_r=95, arm_l=20), 'ooze': egg_pose(lean=-8, up=45, arm_r=30, arm_l=30)},
    'blob': {'idle': blob_pose(), 'squish': blob_pose(sq=0.82), 'hop': blob_pose(sq=1.12, hat_up=3), 'swat': blob_pose(cane=80),
             'tip': blob_pose(hat_up=5, hat_tilt=-25)}}
PARTS = {'bat': {'body': 'gnt_bat_body', 'wing_r': 'gnt_bat_wing_r', 'wing_l': 'gnt_bat_wing_l'},
         'egg': {'body': 'gnt_egg_body', 'arm_r': 'gnt_egg_arm_r', 'arm_l': 'gnt_egg_arm_l'},
         'blob': {'body': 'gnt_blob_body', 'hat': 'gnt_blob_hat', 'cane': 'gnt_blob_cane'}}
