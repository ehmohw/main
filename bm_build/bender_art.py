"""Bender (2.88): the goodest boy - from the owner's photos. A medium dog built like a lean shepherd mix: a warm fawn coat (paler on the
chest and legs), enormous upright pointed ears (fawn outside, dusky grey-brown inside with pale fur at their edges and dark
tips), a dark charcoal mask over his eyes and down his muzzle, greying round the mouth, a white chin, a black nose, soft brown
eyes, and a darker streak down the middle of his forehead.

A rigkit rig, roughly the vanilla wolf's: body, head (a face per expression; the ears and muzzle on it), four legs and the
tail. Design units: feet at y=0, facing -z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise
from rigkit import qs, el, chain

PREFIX = 'bd_'
RIG_SCALE = 1.0
PIVOT = {'body': (0, 11.0, 0), 'head': (0, 14.0, -7.0), 'legfr': (2.2, 8.0, -5.0), 'legfl': (-2.2, 8.0, -5.0),
         'legbr': (2.2, 8.0, 6.0), 'legbl': (-2.2, 8.0, 6.0), 'tail': (0, 12.4, 8.4)}
PARENT = {'body': None, 'head': 'body', 'legfr': 'body', 'legfl': 'body', 'legbr': 'body', 'legbl': 'body', 'tail': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'blink', 'alert')
FAWN, FAWN_DK, FAWN_LT, CREAM = '#d4a066', '#b07e46', '#e6be8a', '#efdcbc'
MASK, MASK_GR = '#3a332e', '#7c766e'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _fur(seed, base=FAWN, n=90):
    im = _noise(base, seed, 6); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-1, 1), y + rnd.randint(2, 4)), fill=hexc(rnd.choice([FAWN_DK, FAWN_LT, FAWN_DK])))
    return im


def _back():
    """his back: a slightly darker saddle down the spine"""
    im = _fur(3101); d = ImageDraw.Draw(im)
    for x in range(64):
        k = abs(x - 32) / 32
        if k < 0.45:
            for y in range(64):
                if (x * 7 + y * 3) % 5 == 0: d.point((x, y), fill=hexc(FAWN_DK))
    return im


def _face(kind=None):
    """the front of his head (28 x 24 texels at uv [0, 0, 7, 6]; the muzzle box covers columns 6-21 of rows 12-23, so the eyes sit
    above it): fawn forehead with its dark streak, the charcoal mask round the eyes (fading out above them - no brows,
    grey-flecked) running down under the muzzle, and big almond brown eyes - a dark rim, a warm iris, the pupil, a white glint
    and a pale lower lid"""
    im = _fur(3102, FAWN, 40); px = im.load()
    rnd = random.Random(3103)
    P = lambda x, y, c: px.__setitem__((x, y), hexc(c)) if 0 <= x < 64 and 0 <= y < 64 else None
    for y in range(0, 7):                                                                    # the forehead streak
        for x in (13, 14):
            if rnd.random() < 0.8: P(x, y, FAWN_DK)
    for y in range(5, 24):                                                                   # the mask: round the eyes and down
        for x in range(28):
            dx = abs(x - 13.5)
            band = (6 <= y <= 13 and 3.0 <= dx <= 11.0) or (y >= 11 and dx <= 8)
            if band:
                c = MASK if rnd.random() < 0.8 else MASK_GR
                if y == 6 and rnd.random() < 0.75: continue                                  # (no hard line over the eyes: the
                if y == 7 and rnd.random() < 0.35: c = FAWN_DK                               #  mask fades into the fawn - not a brow)
                P(x, y, c)
    for sx in (-1, 1):
        x0 = 5 if sx < 0 else 18                                                             # (columns x0..x0+4)
        if kind == 'blink':
            for x in range(x0, x0 + 5): P(x, 9, '#120c08')
            for x in range(x0 + 1, x0 + 4): P(x, 10, '#8a7a6a')
        elif kind == 'happy':                                                                # (squinting up: happy arcs)
            for i, x in enumerate(range(x0, x0 + 5)): P(x, 9 - (1 if i in (1, 2, 3) else 0), '#120c08')
            for x in range(x0 + 1, x0 + 4): P(x, 10, '#8a7a6a')
        else:
            top = 6 if kind == 'alert' else 7
            for y in range(top, 11):
                for x in range(x0, x0 + 5):
                    edge = x in (x0, x0 + 4) or y == top
                    if edge and y in (top, 10) and x in (x0, x0 + 4): continue                   # (almond: the corners stay mask)
                    P(x, y, '#120c08' if edge else ('#9a6230' if y >= top + 2 else '#6e4220'))
            P(x0 + 2, top + 1, '#0a0604'); P(x0 + 3, top + 1, '#0a0604'); P(x0 + 2, top + 2, '#0a0604'); P(x0 + 3, top + 2, '#0a0604')   # the pupil
            P(x0 + 1, top + 1, '#ffffff')                                                    # the glint
            for x in range(x0 + 1, x0 + 4): P(x, 11, '#8a7a6a')                              # the pale lower lid
    return im


def _muzzle(kind=None):
    """the muzzle (4 x 3 front, uv [0, 0, 4, 3]): grey-flecked charcoal, the black nose on top, a white chin, the mouth line - and
    for happy, the pink tongue"""
    im = Image.new('RGBA', (64, 64), hexc(MASK)[:3] + (255,)); px = im.load(); rnd = random.Random(3104)
    for y in range(64):
        for x in range(64):
            if rnd.random() < 0.22: px[x, y] = hexc(MASK_GR)
    d = ImageDraw.Draw(im)
    d.rectangle((14, 0, 49, 18), fill=hexc('#121010'))                                       # the nose
    d.rectangle((20, 4, 25, 9), fill=hexc('#2a2626')); d.rectangle((38, 4, 43, 9), fill=hexc('#2a2626'))
    d.line((32, 18, 32, 30), fill=hexc('#1a1414'), width=2)
    d.line((8, 32, 56, 32), fill=hexc('#1a1414'), width=2)
    d.rectangle((10, 36, 53, 47), fill=hexc(CREAM))                                          # the white chin
    if kind == 'happy':
        d.rectangle((24, 33, 40, 47), fill=hexc('#e07a8a')); d.line((32, 34, 32, 46), fill=hexc('#b85060'))
    return im


def _ear_in():
    im = _noise('#6a5a50', 3105, 6); d = ImageDraw.Draw(im)
    for x in (0, 1, 2, 61, 62, 63):
        d.line((x, 0, x, 63), fill=hexc('#d8c4a8'))
    return im


def textures():
    T = {'bd_fur': _fur(3106), 'bd_back': _back(), 'bd_cream': _fur(3107, CREAM, 50), 'bd_fur_lt': _fur(3108, FAWN_LT, 60),
         'bd_mask': _noise(MASK, 3109, 8), 'bd_ear_in': _ear_in(), 'bd_tip': _noise('#4a3e36', 3110, 6), 'bd_paw': _noise('#e0c49a', 3111, 5),
         'bd_face': _face(), 'bd_muzzle': _muzzle()}
    for k in FACES:
        T[f'bd_face_{k}'] = _face(k)
    T['bd_muzzle_happy'] = _muzzle('happy')
    br = _noise('#9a8a78', 3112, 8); db = ImageDraw.Draw(br)                                       # the bridge: grey-fawn, a paler stripe, dark at the sides
    db.rectangle((0, 0, 9, 63), fill=hexc(MASK)); db.rectangle((54, 0, 63, 63), fill=hexc(MASK)); db.rectangle((26, 0, 37, 63), fill=hexc('#b8a890'))
    T['bd_bridge'] = br
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    # ---- the body: lean, deep-chested, the pale chest and belly, the darker saddle on top
    pv = PIVOT['body']
    body = [el((-3.4, 7.6, -7.6), (3.4, 14.6, -1.0), 'bd_fur', pv, shift=(0.2, 0.3)),          # the chest and shoulders, deep
            el((-3.0, 8.2, -1.2), (3.0, 13.8, 7.8), 'bd_fur', pv, shift=(0.6, 0.1)),           # the loins
            el((-3.42, 14.0, -7.4), (3.42, 14.62, -1.0), 'bd_back', pv, faces=('up',)),
            el((-3.02, 13.2, -1.2), (3.02, 13.82, 7.8), 'bd_back', pv, faces=('up',)),
            el((-2.8, 7.6, -7.62), (2.8, 12.6, -7.6), 'bd_cream', pv, faces=('north',)),       # the pale chest
            el((-3.0, 7.56, -7.4), (3.0, 7.6, -1.2), 'bd_cream', pv, faces=('down',)),
            el((-3.2, 13.0, -8.2), (3.2, 16.0, -5.6), 'bd_fur', pv, shift=(0.4, 0.7))]         # the neck ruff
    part('bd_body', body)
    # ---- the head: a broad skull, the muzzle long and tapering, the enormous upright ears (stepped triangles)
    pv = PIVOT['head']
    def head(face=None):
        ft = 'bd_face' if face is None else f'bd_face_{face}'
        mt = 'bd_muzzle_happy' if face == 'happy' else 'bd_muzzle'
        h = [el((-3.5, 12.6, -11.0), (3.5, 18.6, -6.0), 'bd_fur', pv, shift=(0.3, 0.2)),
             el((-3.5, 12.6, -11.02), (3.5, 18.6, -11.0), ft, pv, faces=('north',), uv={'north': [0, 0, 7, 6]}),
             el((-2.0, 12.6, -14.6), (2.0, 15.6, -10.8), 'bd_mask', pv, faces=('east', 'west', 'down', 'south'), shift=(0.5, 0.5)),   # the muzzle
             el((-2.0, 12.6, -14.62), (2.0, 15.6, -14.6), mt, pv, faces=('north',), uv={'north': [0, 0, 16, 12]}),
             el((-2.0, 15.6, -14.6), (2.0, 15.62, -10.8), 'bd_bridge', pv, faces=('up',), uv={'up': [0, 0, 16, 16]}),   # (the bridge of the nose: grey-fawn)
             el((-1.8, 12.0, -14.0), (1.8, 12.7, -10.6), 'bd_cream', pv)]                              # the white chin
        for sx in (-1, 1):                                                                             # the ears: tall, upright, pointed
            x0 = sx * 2.4
            for k, (w, y0, y1, d0) in enumerate(((4.4, 18.2, 20.0, 1.1), (3.6, 19.8, 21.6, 1.0), (2.7, 21.4, 23.0, 0.9), (1.7, 22.8, 24.2, 0.8), (0.9, 24.0, 25.0, 0.7))):
                tex = 'bd_tip' if k == 4 else 'bd_fur'
                xc = x0 + sx * 0.25 * k                                                                    # (they lean out a little)
                h.append(el((xc - w / 2, y0, -8.6), (xc + w / 2, y1, -8.6 + d0), tex, pv, rot=('z', -10 * sx, (x0, 18.2, -8.0)), shift=(0.2 * k, 0.3)))
                if k < 4:
                    h.append(el((xc - w / 2 + 0.45, y0, -8.62), (xc + w / 2 - 0.45, y1, -8.6), 'bd_ear_in', pv, faces=('north',), rot=('z', -10 * sx, (x0, 18.2, -8.0))))
        return h
    part('bd_head', head())
    for fc in FACES:
        part(f'bd_head_x{fc}', head(fc))
    # ---- the legs: fawn, paler below, cream paws
    def leg(n):
        pv = PIVOT[n]; x, y, z = pv
        return [el((x - 1.2, 2.0, z - 1.2), (x + 1.2, y + 1.4, z + 1.2), 'bd_fur', pv, shift=(0.3, 0.2)),
                el((x - 1.0, 0.8, z - 1.0), (x + 1.0, 2.4, z + 1.0), 'bd_fur_lt', pv),
                el((x - 1.2, 0.0, z - 1.6), (x + 1.2, 0.9, z + 1.1), 'bd_paw', pv)]
    for n in ('legfr', 'legfl', 'legbr', 'legbl'):
        part(f'bd_{n}', leg(n))
    # ---- the tail: a bushy fawn plume, curving up over his back (2.94: up, as a happy dog's is - it used to hang), a darker tip
    pv = PIVOT['tail']; tx, ty, tz = pv
    t = chain([(tx, ty, tz), (0, ty + 1.6, tz + 2.6), (0, ty + 4.2, tz + 3.4), (0, ty + 6.2, tz + 2.4)], (2.2, 1.6), 2.0, 'bd_fur', pv, FRONT, ext=0.3)
    t += [el((-0.8, ty + 6.0, tz + 1.0), (0.8, ty + 7.6, tz + 2.6), 'bd_tip', pv)]
    part('bd_tail', t)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def L(fwd=0.0):
    return qs(('x', -fwd))


def P(**kw):
    return kw


def wag(a):
    return dict(tail=qs(('y', a), ('x', -6)))


IDLE = dict(**wag(10), head=qs(('x', 4)))
POSES = {
    'idle_a': P(**IDLE),
    'idle_b': P(_face='alert', **dict(IDLE, head=qs(('z', 16), ('x', 2)), **wag(-10))),                  # the head tilt
    **{f'walk_{k}': P(_off=(0, 0.2 * (k % 2), 0), legfr=L(22 * math.sin(math.pi * k / 2)), legbl=L(22 * math.sin(math.pi * k / 2)),
                      legfl=L(-22 * math.sin(math.pi * k / 2)), legbr=L(-22 * math.sin(math.pi * k / 2)), head=qs(('x', 2)), **wag(16 * math.sin(math.pi * k / 2)))
       for k in range(4)},
    **{f'run_{k}': P(_off=(0, (0.4, 1.2, 0.4, 0.0)[k], 0), body=qs(('x', (4, -4, 4, 0)[k])), legfr=L((40, 10, -30, 10)[k]), legfl=L((30, 0, -40, 0)[k]),
                     legbr=L((-30, -10, 40, 10)[k]), legbl=L((-40, 0, 30, 0)[k]), head=qs(('x', -4)), tail=qs(('x', -17)))
       for k in range(4)},
    'jump': P(_off=(0, 2.0, 0), body=qs(('x', -12)), legfr=L(50), legfl=L(50), legbr=L(-40), legbl=L(-40), tail=qs(('x', -20))),
    # the bite: crouched back - then a lunge, jaws first
    'bite_up': P(_face='alert', _off=(0, -0.6, 0.6), body=qs(('x', 6)), head=qs(('x', 6)), legfr=L(-20), legfl=L(-20), legbr=L(20), legbl=L(20), tail=qs(('x', -13))),
    'bite': P(_face='alert', _off=(0, 0.4, -2.0), body=qs(('x', -6)), head=qs(('x', -12)), legfr=L(40), legfl=L(40), legbr=L(-30), legbl=L(-30), tail=qs(('x', -17))),
    # digging: nose down, front paws scrabbling, tail going like mad
    'dig_a': P(_face='happy', _off=(0, -0.8, 0), body=qs(('x', 18)), head=qs(('x', 18)), legfr=L(40), legfl=L(-10), **wag(30)),
    'dig_b': P(_face='happy', _off=(0, -0.8, 0), body=qs(('x', 18)), head=qs(('x', 22)), legfr=L(-10), legfl=L(40), **wag(-30)),
    # sniffing: nose to the ground, tail up, ears forward
    'sniff': P(_face='alert', body=qs(('x', 12)), head=qs(('x', 34), ('y', 10)), tail=qs(('x', -23))),
    'sniff_b': P(_face='alert', body=qs(('x', 12)), head=qs(('x', 34), ('y', -10)), tail=qs(('x', -23), ('y', 10))),
    # happy: the goodest boy, tongue out, tail a blur
    'happy': P(_face='happy', head=qs(('x', -8), ('z', 6)), **wag(40)),
    'wave_a': P(_face='happy', legfr=L(70), head=qs(('z', 10)), **wag(30)),
    # sitting: back legs folded under, front legs straight, chest up
    'sit_a': P(_off=(0, -3.4, 2.0), body=qs(('x', -30)), head=qs(('x', 26)), legfr=L(-30), legfl=L(-30), legbr=L(84), legbl=L(84), tail=qs(('x', 60))),
    'sit_b': P(_face='happy', _off=(0, -3.4, 2.0), body=qs(('x', -30)), head=qs(('x', 24), ('z', 14)), legfr=L(-30), legfl=L(-30), legbr=L(84), legbl=L(84), tail=qs(('x', 60), ('y', 20))),
    # lying down (the second photo): chest down, front legs out, head up and turned
    'lie': P(_off=(0, -6.8, 0), legfr=L(84), legfl=L(84), legbr=L(-84), legbl=L(-84), head=qs(('y', 30), ('x', -4)), tail=qs(('x', 20), ('y', 40))),
    'hurt': P(_face='blink', _off=(0, -0.6, 0), body=qs(('x', 6)), head=qs(('x', 18)), tail=qs(('x', 30))),
    'tired': P(_face='blink', _off=(0, -6.8, 0), legfr=L(84), legfl=L(84), legbr=L(-84), legbl=L(-84), head=qs(('x', 20)), tail=qs(('x', 20))),
}
# 2.93b RAGE: latched on a monster's head, mauling (nose down, front paws gripping, tail up and lashing); the backflip off it
# (the whole dog turned over backwards about his middle, legs tucked); the landing (a crouch to take it)
GRIP = dict(legfr=L(52), legfl=L(52), legbr=L(-24), legbl=L(-24))
POSES.update({
    'maul_a': P(_face='alert', _off=(0, 0.4, 1.6), body=qs(('x', 26)), head=qs(('x', 38)), tail=qs(('x', -24), ('y', 14)), **GRIP),
    'maul_b': P(_face='alert', _off=(0, 0.0, 1.6), body=qs(('x', 20)), head=qs(('x', 48), ('z', 14)), tail=qs(('x', -24), ('y', -14)), **GRIP),
    **{f'flip_{k}': P(_off=(0, 3.0, 0), body=qs(('x', -(62 + 68 * k))), head=qs(('x', -16)), legfr=L(74), legfl=L(74), legbr=L(-74), legbl=L(-74),
                      tail=qs(('x', 30))) for k in range(5)},
    'land': P(_face='alert', _off=(0, -1.4, 0.4), body=qs(('x', 8)), head=qs(('x', 2)), legfr=L(-26), legfl=L(-26), legbr=L(30), legbl=L(30), tail=qs(('x', -13))),
})
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (the doggy paddle)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -6.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', -14)), head=qs(('x', -10)),
                            legfr=L(40 + 30 * math.sin(_p)), legfl=L(40 - 30 * math.sin(_p)), legbr=L(-20 + 20 * math.sin(_p)), legbl=L(-20 - 20 * math.sin(_p)),
                            tail=qs(('x', -3), ('y', 20 * math.sin(_p))))
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'bite_up', 'bite', 'dig_a', 'sniff', 'happy', 'sit_a', 'lie', 'swim_2']


# (2.93e: every material with life in it - matkit)
import matkit as _mk
textures = _mk.wrapped(textures, __name__)
