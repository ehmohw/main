"""Bloo (2.87): the reserved woodland creature - from the owner's art. A great hulking cat-beast, taller than any man: a blue
cat's head - yellow eyes under heavy dark brows, a pink nose, whiskers, white horns in grey bands curving up out of his skull, a
tuft standing up between them, fur tufts at his cheeks - and a mouthful of sharp teeth when he snarls (his art's face). A thick
shaggy blue mane over his shoulders; a white, heavily muscled chest and belly (an old scar on his breast, a blue flame-tuft at its
top); white arms ending in huge clawed hands; blue furred legs, great clawed feet; grey bat wings; a thin white tail with a
blue flame-tuft.

A rigkit rig: body, head (a model per expression - the face painted on), arms bent at the elbow, legs, the two wings and the
tail (on the body). Design units: feet at y=0, facing -z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'bo_'
RIG_SCALE = 1.0
PIVOT = {'body': (0, 15.0, 0), 'legr': (2.6, 15.0, 0), 'legl': (-2.6, 15.0, 0), 'head': (0, 29.6, -0.8),
         'armr': (6.6, 26.4, 0), 'forer': (7.6, 20.4, 0), 'arml': (-6.6, 26.4, 0), 'forel': (-7.6, 20.4, 0),
         'wingr': (2.2, 26.0, 2.6), 'wingl': (-2.2, 26.0, 2.6), 'tail': (0, 15.4, 2.4)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'wingr': 'body', 'wingl': 'body', 'tail': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('scowl', 'roar', 'happy', 'hurt', 'blink')
FUR, FUR_DK, FUR_LT = '#5a8ed0', '#2f5aa0', '#8ab8ec'
HIDE, HIDE_DK = '#e6e8ec', '#b8bcc6'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _fur(seed, base=FUR, dk=FUR_DK, lt=FUR_LT, n=120):
    """shaggy fur: short strokes, dark and light, mostly downward"""
    im = _noise(base, seed, 6); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-2, 2), y + rnd.randint(3, 7)), fill=hexc(rnd.choice([dk, lt, dk])))
    return im


def _hide(seed):
    """his chest and arms: pale grey-white, faint muscle shading"""
    im = _noise(HIDE, seed, 4); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(6):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.arc((x - 10, y - 6, x + 10, y + 6), 200, 340, fill=hexc(HIDE_DK))
    return im


def _chest(seed):
    """the chest's front: the pecs, the abs in two columns, the old scar with its blue flame-tuft at the top, the fur's edge at
    the belt line"""
    im = _hide(seed); d = ImageDraw.Draw(im); ink = hexc('#6a7080')
    d.arc((4, 4, 32, 24), 20, 160, fill=ink, width=1); d.arc((32, 4, 60, 24), 20, 160, fill=ink, width=1)       # the pecs
    for y in (30, 39, 48):
        d.line((21, y, 30, y + 1), fill=ink); d.line((34, y + 1, 43, y), fill=ink)                                 # the abs
    d.line((32, 26, 32, 56), fill=ink)
    d.line((30, 10, 31, 22), fill=hexc('#40485a'), width=2)                                                       # the scar...
    for y in (13, 16, 19):
        d.line((27, y, 34, y), fill=hexc('#40485a'))
    d.polygon([(27, 10), (29, 2), (31, 7), (33, 0), (34, 8), (36, 4), (35, 11)], fill=hexc(FUR))                   # ...its flame-tuft
    for x in range(0, 64, 4):                                                                                      # the fur's edge below
        d.polygon([(x, 64), (x + 2, 56 + (x * 7) % 5), (x + 4, 64)], fill=hexc(FUR))
    return im


def _wing(seed):
    im = _noise('#6a6e78', seed, 5); d = ImageDraw.Draw(im)
    for x in range(0, 64, 12):
        d.line((x, 0, x + 6, 63), fill=hexc('#3c3f48'), width=2)
    return im


def _horn(seed):
    im = _noise('#ece4cc', seed, 5); d = ImageDraw.Draw(im)
    for y in range(0, 64, 9):
        d.line((0, y, 63, y), fill=hexc('#c8bea0'))
    return im


def _face(kind=None):
    """the front of his head: 40 x 27 texels on the sheet (the head's front takes uv [0, 0, 10, 6.75] - 4 texels a unit, the
    pack's own scale), drawn texel by texel. From the art: heavy navy brows slammed down toward his nose, yellow eyes under
    them (the lids cut straight across by the brows, a black slit pupil) staring straight out - vicious, not sad; a pink nose;
    whiskers; and by default (his art's face) the snarl - the mouth wide open, dark red inside, a row of sharp white teeth
    top and bottom and two great fangs. scowl: the mouth shut in a hard line, the fangs over it."""
    im = _fur(1801, n=50); d = ImageDraw.Draw(im); px = im.load()
    P = lambda x, y, c: px.__setitem__((x, y), hexc(c)) if 0 <= x < 64 and 0 <= y < 64 else None
    ink, white, yel, yel_lt, yel_dk = '#0c1020', '#ffffff', '#f4d81e', '#fff28a', '#c09a10'
    brow = '#14203e'
    for y in range(27):                                                                      # (the rim of the face, darker)
        P(0, y, FUR_DK); P(39, y, FUR_DK)
    for x in range(40):
        P(x, 0, FUR_DK)
    # the muzzle, lighter; the cheek tufts (spiky, at the sides)
    d.rectangle((9, 15, 30, 26), fill=hexc(FUR_LT))
    for sx in (-1, 1):
        x0 = 0 if sx < 0 else 39
        for i, (dx, y) in enumerate(((0, 14), (1, 15), (2, 16), (3, 17), (1, 18), (2, 19), (4, 20), (2, 21), (1, 22))):
            for k in range(dx + 1):
                P(x0 - sx * 0 + sx * (-k) if False else (x0 + (k if sx < 0 else -k)), y, FUR_LT)
    # the eyes: a wedge each - the top edge cut by the brow, sloping DOWN toward the nose; a round-ish bottom
    for flip in (False, True):
        for i in range(12):                                                                  # i = 0 at the outer corner
            x = 4 + i if not flip else 35 - i
            top = 8 + (i * 5) // 11                                                          # (lower toward the nose: anger)
            bot = 14 - (1 if i in (0, 11) else 0) - (1 if i in (1, 10) else 0)
            if kind == 'blink':
                P(x, 12, ink); continue
            if kind == 'hurt':
                P(x, 10 + (i if i < 6 else 11 - i) // 2, ink); continue
            for y in range(top, bot + 1):
                c = yel if y < bot - 1 else yel_dk
                if y == top + 1 and i in (3, 4, 5): c = yel_lt
                P(x, y, c)
            P(x, bot + 1, ink)
        if kind not in ('blink', 'hurt'):
            cx = 10 if not flip else 29                                                      # the slit, straight ahead
            for y in range(10, 15):
                P(cx, y, ink); P(cx + 1, y, ink)
            P(cx - 2 if not flip else cx + 3, 11, white)
    # the brows: heavy bars over the eyes, slammed down toward the nose (3 texels deep)
    if kind != 'happy':
        for flip in (False, True):
            for i in range(14):
                x = 2 + i if not flip else 37 - i
                top = 5 + (i * 5) // 13
                for y in range(top, top + 3):
                    P(x, y, brow)
    else:
        for flip in (False, True):
            for i in range(14):
                x = 2 + i if not flip else 37 - i
                P(x, 6, brow); P(x, 7, brow)
    # the nose (pink, a triangle), the split lip, the whiskers
    for y, (a, b) in enumerate(((17, 22), (18, 21), (19, 20))):
        for x in range(a, b + 1):
            P(x, 15 + y, '#f4a0c0')
    P(19, 18, ink); P(20, 18, ink)
    for sx in (-1, 1):
        for k, (y0, y1) in enumerate(((19, 17), (21, 21))):
            for t in range(9):
                x = 20 + sx * (6 + t) if sx > 0 else 19 + sx * (6 + t)
                P(x, round(y0 + (y1 - y0) * t / 8), '#1a2238')
    if kind in (None, 'roar'):
        top, bot = 19, 26                                                                     # wide open (roaring: wider still)
        if kind == 'roar': top = 18
        d.rectangle((10, top, 29, bot), fill=hexc('#6a1010'))
        d.rectangle((14, bot - 2, 25, bot), fill=hexc('#c84a4a'))                              # the tongue
        for x in range(10, 30, 2):                                                             # the top teeth
            P(x, top, white); P(x + 1, top, white); P(x, top + 1, white)
        for x in range(11, 29, 2):                                                             # the bottom teeth
            P(x, bot, white); P(x + 1, bot, white); P(x + 1, bot - 1, white)
        for fx in (11, 27):                                                                    # the fangs
            for y in range(top, top + 4):
                P(fx, y, white); P(fx + 1, y, white) if y < top + 3 else None
        for x in range(9, 31):
            P(x, top - 1, ink); P(x, bot + 1 if bot < 26 else bot, ink) if False else None
        for y in range(top, bot + 1):
            P(9, y, ink); P(30, y, ink)
    elif kind == 'happy':
        for t, x in enumerate(range(12, 28)):                                                  # a rare, crooked smirk
            P(x, 22 - (1 if x > 22 else 0) - (1 if x > 25 else 0), ink)
        P(24, 23, white); P(25, 23, white); P(25, 24, white)
    elif kind == 'hurt':
        for t, x in enumerate(range(12, 28)):
            P(x, 22 + (t % 4 in (1, 2)), ink)
    else:                                                                                      # scowl: a hard line, the lip curled, fangs over it
        for x in range(11, 29):
            P(x, 22, ink)
        P(10, 21, ink); P(29, 21, ink)
        for fx in (13, 25):
            P(fx, 23, white); P(fx + 1, 23, white); P(fx, 24, white)
    return im


def textures():
    T = {'bo_fur': _fur(1802), 'bo_fur_dk': _fur(1803, FUR_DK, '#1a3a70', FUR), 'bo_mane': _fur(1804, FUR_LT, FUR, '#c8e0ff', 160),
         'bo_hide': _hide(1805), 'bo_hide_dk': _noise(HIDE_DK, 1806, 4), 'bo_chest': _chest(1807), 'bo_claw': _shine('#16161c', '#5a5a66', 1808),
         'bo_wclaw': _shine('#f4f4f6', '#ffffff', 1809), 'bo_wing': _wing(1810), 'bo_bone': _noise('#5a5e68', 1811, 4), 'bo_horn': _horn(1812),
         'bo_band': _shine('#8a8e98', '#c8ccd6', 1813), 'bo_face': _face()}
    for k in FACES:
        T[f'bo_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the white chest and belly, broad at the shoulders, narrow at the waist; the shaggy blue mane over the
    #      shoulders and round the neck; the fur from the waist down
    pv = PIVOT['body']
    body = [el((-4.2, 14.6, -2.6), (4.2, 18.4, 2.6), 'bo_fur', pv, shift=(0.3, 0.2)),                     # the hips (fur)
            el((-4.4, 17.6, -2.8), (4.4, 22.0, 2.8), 'bo_hide', pv),                                       # the belly
            el((-5.8, 21.6, -3.2), (5.8, 27.2, 3.2), 'bo_hide', pv, shift=(0.5, 0.2)),                     # the chest, broad
            el((-4.4, 17.6, -2.82), (4.4, 22.0, -2.8), 'bo_chest', pv, faces=('north',), uv={'north': [4, 9, 12, 16]}),
            el((-5.8, 21.6, -3.22), (5.8, 27.2, -3.2), 'bo_chest', pv, faces=('north',), uv={'north': [0, 0, 16, 9]})]
    # the mane: shaggy layers over the shoulders, round the back of the neck, hanging spikes along its lower edge
    body += [el((-7.0, 25.4, -3.8), (7.0, 28.6, 3.8), 'bo_mane', pv, shift=(0.2, 0.3)),
             el((-5.6, 27.6, -3.0), (5.6, 30.0, 3.4), 'bo_mane', pv, shift=(0.6, 0.1))]
    for i in range(14):
        a = (i + 0.5) / 14 * 2 * math.pi; cx, cz = 6.4 * math.sin(a), -3.4 * math.cos(a)
        h = 1.6 + 0.9 * ((i * 5) % 3) / 2
        body.append(el((cx - 0.8, 25.4 - h, cz - 0.6), (cx + 0.8, 25.6, cz + 0.6), 'bo_mane', pv, shift=(0.13 * i, 0.4)))
    part('bo_body', body)

    # ---- the head: a cat's head - broad, a little muzzle; the face painted on; the horns (white, grey-banded at the root)
    #      curving up and out; the tuft between them; cat ears behind the horns
    pv = PIVOT['head']
    HW, HB, HT, HZ = 5.0, 29.2, 35.95, 4.0
    def head(face=None):
        tex = 'bo_face' if face is None else f'bo_face_{face}'
        h = [el((-HW, HB, -HZ + 0.2), (HW, HT, HZ), 'bo_fur', pv, shift=(0.2, 0.3)),
             el((-HW, HB, -HZ + 0.18), (HW, HT, -HZ + 0.2), tex, pv, faces=('north',), uv={'north': [0, 0, 10, 6.75]})]
        for sx in (-1, 1):                                                                   # the cheek tufts, standing out from the jaw
            h += [el((sx * HW - (0.0 if sx > 0 else 1.4), HB + 0.6, -HZ + 0.6), (sx * HW + (1.4 if sx > 0 else 0.0), HB + 3.2, -HZ + 3.0), 'bo_mane', pv,
                     rot=('z', 22.5 * sx, (sx * HW, HB + 1.8, 0)), shift=(0.3, 0.3))]
        for sx in (-1, 1):
            # the horns: a grey band at the root, then white, sweeping up and out and back
            h += [el((sx * 3.2 - 0.9, HT - 1.6, -0.4), (sx * 3.2 + 0.9, HT + 0.2, 1.4), 'bo_band', pv)]
            h += chain([(sx * 3.4, HT, 0.5), (sx * 4.6, HT + 2.2, 0.9), (sx * 5.0, HT + 4.4, 1.8), (sx * 4.6, HT + 6.0, 3.0)], [(1.4, 0.5)][0], 1.3, 'bo_horn', pv, FRONT, ext=0.1)
            # the ears (cat's, tufted), set behind the horns
            h += [el((sx * 3.0 - 0.9, HT - 0.2, 1.6), (sx * 3.0 + 0.9, HT + 2.0, 2.6), 'bo_fur_dk', pv, rot=('z', -18 * sx, (sx * 3.0, HT, 2.0))),
                  el((sx * 3.3 - 0.4, HT + 1.6, 1.8), (sx * 3.3 + 0.4, HT + 3.0, 2.4), 'bo_mane', pv, rot=('z', -30 * sx, (sx * 3.3, HT + 1.8, 2.0)))]
        # the tuft between the horns: a curved spike standing up and back
        h += chain([(0.2, HT, -0.8), (0.4, HT + 2.2, 0.2), (1.0, HT + 3.8, 1.8)], [1.2, 0.5], 1.1, 'bo_fur', pv, FRONT, ext=0.1)
        return h
    part('bo_head', head())
    for fc in FACES:
        part(f'bo_head_x{fc}', head(fc))

    # ---- the arms: thick white upper arms, white forearms, the huge clawed hands (long pale claws)
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        return [el((x0 - 2.0, y0 - 1.8, -2.1), (x0 + 2.0, y0 + 1.6, 2.1), 'bo_hide', pv)] + \
            chain([(x0, y0, 0), (sx * 7.6, 20.4, 0)], [(3.4, 3.0)][0], 3.2, 'bo_hide', pv, FRONT, ext=0.4)
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 8.2, 15.4
        a = chain([(ex, ey, 0), (wx, wy, 0)], [(3.0, 2.6)][0], 2.8, 'bo_hide', pv, FRONT, ext=0.3)
        a += [el((wx - 2.0, wy - 3.4, -2.2), (wx + 2.0, wy + 0.4, 2.0), 'bo_hide', pv, shift=(0.4, 0.4)),        # the great hand
              el((wx - 2.05, wy - 0.4, -2.25), (wx + 2.05, wy + 0.4, 2.05), 'bo_hide_dk', pv)]
        for i, dx in enumerate((-1.4, -0.45, 0.45, 1.4)):                                                       # the claws, long and pale
            a += chain([(wx + dx, wy - 3.0, -1.6), (wx + dx * 1.15, wy - 5.0, -2.4), (wx + dx * 1.2, wy - 6.2, -2.0)], [0.6, 0.35], 0.6, 'bo_wclaw', pv, FRONT, ext=0.05)
        a += chain([(wx - sx * 1.8, wy - 1.6, -1.4), (wx - sx * 2.6, wy - 3.2, -2.4)], [0.6], 0.6, 'bo_wclaw', pv, FRONT, ext=0.05)   # the thumb claw
        return a
    part('bo_armr', upper(1)); part('bo_arml', upper(-1)); part('bo_forer', lower(1)); part('bo_forel', lower(-1))

    # ---- the legs: long, thick, shaggy blue fur; the great clawed feet (black claws)
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        L = [el((cx - 2.2, 8.0, -2.2), (cx + 2.2, 15.4, 2.2), 'bo_fur', pv, shift=(0.3 if sx > 0 else 0.6, 0.2)),
             el((cx - 1.9, 1.6, -1.9), (cx + 1.9, 8.4, 1.9), 'bo_fur', pv, shift=(0.6, 0.5)),
             el((cx - 2.3, 1.8, -2.3), (cx + 2.3, 2.8, 2.3), 'bo_fur_dk', pv),                                  # (the shag at the ankle)
             el((cx - 2.3, 0.0, -3.6), (cx + 2.3, 1.9, 1.8), 'bo_fur_dk', pv)]                                   # the foot
        for dx in (-1.6, -0.55, 0.55, 1.6):
            L += [el((cx + dx - 0.35, 0.0, -4.6), (cx + dx + 0.35, 0.7, -3.5), 'bo_claw', pv)]
        return L
    part('bo_legr', leg(1)); part('bo_legl', leg(-1))

    # ---- the wings: grey bat wings - the arm bone up and out from his shoulder blade, three finger bones fanning down from its
    #      tip, the membrane between them (boxes, stepped)
    def wing(sx):
        pv = PIVOT['wingr' if sx > 0 else 'wingl']
        w = chain([(sx * 2.2, 26.0, 2.8), (sx * 8.0, 30.0, 3.4), (sx * 14.0, 33.0, 3.8)], [0.9, 0.7], 0.8, 'bo_bone', pv, FRONT, ext=0.2)
        tip = (sx * 14.0, 33.0, 3.8)
        for k, (ex, ey) in enumerate(((sx * 15.6, 24.0), (sx * 11.6, 21.0), (sx * 7.2, 21.6))):
            w += chain([tip, (ex, ey, 3.8)], [0.5], 0.5, 'bo_bone', pv, FRONT, ext=0.1)
        # the membrane: vertical strips stepping down from the arm bone to the fingers' tips
        for i in range(8):
            x0 = sx * (2.6 + i * 1.6); x1 = sx * (2.6 + (i + 1) * 1.6)
            lo, hi = min(x0, x1), max(x0, x1)
            xm = (i + 0.5) / 8
            top = 26.4 + 6.4 * xm
            bot = 23.0 - 2.4 * math.sin(xm * math.pi * 3) * 0.6 - (1.6 if i in (2, 5) else 0)
            w.append(el((lo, bot, 3.6), (hi, top, 3.85), 'bo_wing', pv, shift=(0.11 * i, 0.3)))
        return w
    part('bo_wingr', wing(1)); part('bo_wingl', wing(-1))

    # ---- the tail: thin and white, a long curve down and out to the side; the blue flame-tuft at its end
    pv = PIVOT['tail']
    tl = chain([(0, 15.4, 2.6), (-2.0, 12.0, 5.4), (-5.6, 8.6, 7.0), (-9.6, 7.6, 6.4), (-12.6, 9.4, 4.8)], [0.7, 0.6, 0.55, 0.5], 0.6, 'bo_hide', pv, FRONT, ext=0.15)
    tl += [el((-13.6, 9.0, 4.0), (-12.0, 11.6, 5.6), 'bo_mane', pv, rot=('z', 20, (-12.8, 10, 4.8))),
           el((-13.2, 11.0, 4.4), (-12.4, 12.6, 5.2), 'bo_fur', pv, rot=('z', 30, (-12.8, 11.6, 4.8)))]
    part('bo_tail', tl)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def flap(sx, up=0.0, back=0.0):
    return qs(('y', back * sx), ('z', -up * sx))


def P(**kw):
    return kw


WINGS = dict(wingr=flap(1, 6, 18), wingl=flap(-1, 6, 18))                    # half spread, ready
# idle (the art's stance): legs planted wide, a forward hunch, the head low and glaring, arms out and bent, claws spread
IDLE = dict(WINGS, body=qs(('x', 8)), legr=limb(1, -6, 9), legl=limb(-1, -6, 9), armr=limb(1, 18, 26), forer=limb(1, 34, -14), arml=limb(-1, 18, 26),
            forel=limb(-1, 34, -14), head=qs(('x', -2)), tail=qs(('y', 18), ('x', -10)))
POSES = {
    # idle: arms hanging heavy, claws flexing, watching you sidelong (head turned, eyes straight - he just looks away)
    'idle_a': P(**IDLE),                                                            # (his art's face: the snarl)
    'idle_b': P(_face='scowl', _off=(0, -0.2, 0), **dict(IDLE, armr=limb(1, 22, 30), forer=limb(1, 40, -18), arml=limb(-1, 22, 30), forel=limb(-1, 40, -18),
                                                         head=qs(('x', 2), ('y', 14)), tail=qs(('y', -18), ('x', -10)), wingr=flap(1, 12, 12), wingl=flap(-1, 12, 12))),
    # walk: a heavy, rolling prowl
    'walk_a': P(_off=(0, 0.2, 0), body=qs(('x', 6), ('y', 4)), legr=limb(1, 24), legl=limb(-1, -22), armr=limb(1, -16, 10), forer=limb(1, 24),
                arml=limb(-1, 22, 10), forel=limb(-1, 24), head=qs(('x', -4)), tail=qs(('y', 16)), **WINGS),
    'walk_up': P(_off=(0, 0.6, 0), body=qs(('x', 6)), legr=limb(1, 4), legl=limb(-1, -4), armr=limb(1, 2, 10), forer=limb(1, 24), arml=limb(-1, 2, 10), forel=limb(-1, 24),
                 head=qs(('x', -4)), **WINGS),
    'walk_b': P(_off=(0, 0.2, 0), body=qs(('x', 6), ('y', -4)), legr=limb(1, -22), legl=limb(-1, 24), armr=limb(1, 22, 10), forer=limb(1, 24),
                arml=limb(-1, -16, 10), forel=limb(-1, 24), head=qs(('x', -4)), tail=qs(('y', -16)), **WINGS),
    # run: low and loping, the wings half open for balance
    'run_a': P(_off=(0, 0.4, 0), body=qs(('x', 22)), head=qs(('x', -18)), legr=limb(1, 48), legl=limb(-1, -40), armr=limb(1, -40, 14), forer=limb(1, 50),
               arml=limb(-1, 50, 14), forel=limb(-1, 50), wingr=flap(1, 10, 10), wingl=flap(-1, 10, 10), tail=qs(('x', -20))),
    'run_up': P(_off=(0, 1.1, 0), body=qs(('x', 22)), head=qs(('x', -18)), legr=limb(1, 16), legl=limb(-1, -20), armr=limb(1, 4, 16), forer=limb(1, 60),
                arml=limb(-1, 4, 16), forel=limb(-1, 60), wingr=flap(1, 20, 4), wingl=flap(-1, 20, 4), tail=qs(('x', -26))),
    'run_b': P(_off=(0, 0.4, 0), body=qs(('x', 22)), head=qs(('x', -18)), legr=limb(1, -40), legl=limb(-1, 48), armr=limb(1, 50, 14), forer=limb(1, 50),
               arml=limb(-1, -40, 14), forel=limb(-1, 50), wingr=flap(1, 10, 10), wingl=flap(-1, 10, 10), tail=qs(('x', -20))),
    'jump': P(_off=(0, 1.8, 0), body=qs(('x', 10)), legr=limb(1, 40), legl=limb(-1, 20), armr=limb(1, 60, 30), forer=limb(1, 30), arml=limb(-1, 60, 30),
              forel=limb(-1, 30), wingr=flap(1, 30, -6), wingl=flap(-1, 30, -6)),
    # the swipe (his attack): a claw drawn back, then raked across
    'swipe_up': P(body=qs(('y', -20)), armr=limb(1, 60, 60), forer=limb(1, 50), arml=limb(-1, 20, 14), forel=limb(-1, 30), wingr=flap(1, 10, 10), wingl=flap(-1, 10, 10)),
    'swipe': P(_off=(0, -0.2, 0), body=qs(('y', 24), ('x', 10)), head=qs(('x', -6)), armr=limb(1, 80, -20, 30), forer=limb(1, 20), arml=limb(-1, -10, 20),
               forel=limb(-1, 30), wingr=flap(1, -6, 30), wingl=flap(-1, -6, 30)),
    # the pounce: crouched, then a leap with both claws out
    'crouch': P(_off=(0, -2.0, 0), body=qs(('x', 30)), head=qs(('x', -26)), legr=limb(1, 60), legl=limb(-1, 60), armr=limb(1, 40, 20), forer=limb(1, 50),
                arml=limb(-1, 40, 20), forel=limb(-1, 50), wingr=flap(1, 4, 40), wingl=flap(-1, 4, 40)),
    'pounce': P(_off=(0, 2.0, 0), body=qs(('x', 34)), head=qs(('x', -24)), legr=limb(1, -30), legl=limb(-1, -20), armr=limb(1, 150, 20), forer=limb(1, 10),
                arml=limb(-1, 150, 20), forel=limb(-1, 10), wingr=flap(1, 40, -10), wingl=flap(-1, 40, -10)),
    # the roar (his great move): head thrown back, wings flung wide, arms out and claws spread
    'roar': P(_face='roar', _off=(0, 0.4, 0), body=qs(('x', -12)), head=qs(('x', -24)), armr=limb(1, 40, 70), forer=limb(1, 30), arml=limb(-1, 40, 70), forel=limb(-1, 30),
              wingr=flap(1, 36, -14), wingl=flap(-1, 36, -14), tail=qs(('x', -30))),
    # arms folded, looking away (his "hmph")
    'hmph': P(_face='scowl', head=qs(('y', -40), ('x', -6)), armr=limb(1, 30, -6), forer=limb(1, 84, 0, 60), arml=limb(-1, 30, -6), forel=limb(-1, 80, 0, 60), **dict(WINGS, tail=qs(('y', 24)))),
    'wave_a': P(**dict(IDLE, arml=limb(-1, 10, 80), forel=limb(-1, 40), head=qs(('y', -20)))),
    # sitting: cross-legged on the ground, arms on his knees, wings folded
    'sit_a': P(_face='scowl', _off=(0, -7.4, 0), legr=limb(1, 84, 30, -20), legl=limb(-1, 84, 30, -20), armr=limb(1, 20, 10), forer=limb(1, 40), arml=limb(-1, 20, 10), forel=limb(-1, 40),
               head=qs(('y', -16), ('x', 6)), wingr=flap(1, -16, 36), wingl=flap(-1, -16, 36), tail=qs(('x', 30), ('y', 30))),
    'sit_b': P(_face='blink', _off=(0, -7.5, 0), body=qs(('x', 6)), legr=limb(1, 84, 30, -20), legl=limb(-1, 84, 30, -20), armr=limb(1, 26, 12), forer=limb(1, 40),
               arml=limb(-1, 26, 12), forel=limb(-1, 40), head=qs(('x', 18), ('z', 6)), wingr=flap(1, -18, 38), wingl=flap(-1, -18, 38), tail=qs(('x', 30), ('y', 34))),
    'hurt': P(_face='hurt', body=qs(('x', -8)), head=qs(('x', -14)), armr=limb(1, 30, 40), forer=limb(1, 50), arml=limb(-1, 30, 40), forel=limb(-1, 50),
              wingr=flap(1, 24, -6), wingl=flap(-1, 24, -6)),
    'tired': P(_face='hurt', _off=(0, -1.0, 0), body=qs(('x', 18)), head=qs(('x', 18)), armr=limb(1, 4, 6), arml=limb(-1, 4, 6), forer=limb(1, 6), forel=limb(-1, 6),
               legr=limb(1, 10), legl=limb(-1, -6), wingr=flap(1, -30, 30), wingl=flap(-1, -30, 30)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (he hates it: a furious dog-paddle, the wings beating)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -9.0 + 0.5 * math.sin(2 * _p), 0), body=qs(('x', 40)), head=qs(('x', -40)),
                            armr=limb(1, 90 + 40 * math.sin(_p), 20), forer=limb(1, 40 + 20 * math.cos(_p)),
                            arml=limb(-1, 90 - 40 * math.sin(_p), 20), forel=limb(-1, 40 - 20 * math.cos(_p)),
                            legr=limb(1, -10 + 26 * math.sin(2 * _p)), legl=limb(-1, -10 - 26 * math.sin(2 * _p)),
                            wingr=flap(1, 14 * math.sin(_p), 30), wingl=flap(-1, 14 * math.sin(_p), 30), tail=qs(('x', -30)))
DRAFT = ['idle_a', 'idle_b', 'walk_a', 'run_a', 'swipe_up', 'swipe', 'crouch', 'pounce', 'roar', 'hmph', 'sit_a', 'hurt', 'swim_2']
