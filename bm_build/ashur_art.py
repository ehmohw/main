"""Ashur (2.86): the fire follower - from the owner's sketches. A fierce little fire-mage in the Emma/Celi style: a big head,
a painted anime face (sharp violet eyes with slit pupils, angled brows, a set little mouth, a smudge of ash on one cheek),
a red-orange bob that flares up into flame at the crown and curls out in two hooks at her jaw, and a golden flame tiara with
a red hexagonal gem on her brow. Her dress is magma: dark red rock, cracked through with glowing orange, yellow and red, the
bodice plated in cooled hexagons with a jagged neckline, the skirt flared to the knee with a jagged, glowing hem. Bare
shoulders and arms. Barefoot, a gold anklet on her left ankle. Fire blooms in her palms when
she fights (the 'firer' / 'firel' parts, shown by a pose's _fire).

One item model per part, its joint at model (8, 8, 8) (the phase57_art kit, as Celi). Design units: feet at y=0, facing -z,
her right is +x; drawn at RIG_SCALE. A face texture per expression ('as_face', 'as_face_<x>')."""
import math
import random
from PIL import Image, ImageDraw
from phase57_art import _cloth, _hair2, _el, hexc, qa, qmul, limb, torso, _qrot, _sh

RIG_SCALE = 0.85
PREFIX = 'as_'
PIVOT = {'body': (0, 13, 0), 'head': (0, 25, 0), 'armr': (4.5, 23.0, 0), 'arml': (-4.5, 23.0, 0), 'legr': (1.7, 13, 0), 'legl': (-1.7, 13, 0),
         'forer': (4.7, 18.8, 0), 'forel': (-4.7, 18.8, 0)}
PARTS = ('body', 'head', 'armr', 'arml', 'forer', 'forel', 'legr', 'legl', 'firer', 'firel')
PALMR, PALML = (4.8, 13.0, -0.3), (-4.8, 13.0, -0.3)        # her palms (design units): where the fire sits
SKIN, SKIN_DK, SKIN_LT = '#f2b48a', '#d8916a', '#ffd0ae'
HAIR = ('#a8260c', '#c8340e', '#e04a14', '#f06a1c', '#ff9a3a')
EXPR = ('fierce', 'grin', 'shout', 'hurt', 'blink')
GLOW = ('#ff3a10', '#ff7a14', '#ffb21a', '#ffe060')


# ---------------------------------------------------------------------------------------------------- textures
def _magma(seed, base='#3a0806', cell=10.0, glow=1.0, plates=False):
    """dark red rock, cracked through with light: every pixel near the border of a jittered cell glows - deep red at the edge
    of a crack, orange, then a yellow-white core. (Sampled from the top-left at 4 px a unit, so the cracks are fine.)
    plates: the cells are cooled hexagons (the bodice) - thin dark seams, a few glowing."""
    rnd = random.Random(seed); b = hexc(base)[:3]
    pts = []
    for gy in range(-1, int(64 / cell) + 2):
        for gx in range(-1, int(64 / cell) + 2):
            ox = (cell / 2) if (plates and gy % 2) else 0
            j = 0.15 if plates else 0.42
            pts.append((gx * cell + ox + rnd.uniform(-j, j) * cell, gy * cell * (0.87 if plates else 1) + rnd.uniform(-j, j) * cell, rnd.random()))
    im = Image.new('RGBA', (64, 64)); px = im.load()
    for y in range(64):
        for x in range(64):
            d1 = d2 = 1e9; hot = 0
            for (cx, cy, h) in pts:
                d = (cx - x) ** 2 + (cy - y) ** 2
                if d < d1: d2 = d1; d1 = d; hot = h
                elif d < d2: d2 = d
            e = math.sqrt(d2) - math.sqrt(d1)                     # distance to the cell border
            k = 1 + rnd.uniform(-0.06, 0.06) - 0.12 * (1 - min(1, e / cell))
            c = _sh(b, k)
            if plates:
                if e < 0.6 and hot > 0.3: c = hexc(GLOW[2])[:3]
                elif e < 1.1: c = hexc(GLOW[1] if hot > 0.3 else '#2a0504')[:3]
                elif e < 1.8 and hot > 0.3: c = hexc(GLOW[0])[:3]
                elif e < 2.4 and hot > 0.3: c = _sh(hexc('#8a1a0c'), 1.0)
            else:
                w = glow * (0.5 + 0.7 * hot)                              # (thin cracks: a hot core, a soft red edge)
                if e < 0.35 * w: c = hexc(GLOW[3])[:3]
                elif e < 0.7 * w: c = hexc(GLOW[2])[:3]
                elif e < 1.05 * w: c = hexc(GLOW[1])[:3]
                elif e < 1.5 * w: c = hexc(GLOW[0])[:3]
                elif e < 2.1 * w: c = _sh(hexc('#8a1a0c'), 1 + rnd.uniform(-0.05, 0.05))
            px[x, y] = c + (255,)
    return im


def _hem(seed):
    """the skirt's lowest band: hotter - the magma glows more where it hangs"""
    return _magma(seed, '#5a0c08', cell=7.0, glow=1.5)


def _skin(seed, ash=0):
    im = _cloth(SKIN, seed, var=0.02); rnd = random.Random(seed)
    for _ in range(ash):                                          # a few smudges of ash
        x, y = rnd.randint(0, 40), rnd.randint(0, 40)
        for dx, dy in ((0, 0), (1, 0), (0, 1)): im.putpixel((x + dx, y + dy), hexc('#5a3a30'))
    return im


def _gold(seed):
    im = _cloth('#e0b030', seed, var=0.05); px = im.load()
    for y in range(64):
        for x in range(64):
            if (x + y) % 9 == 0: px[x, y] = hexc('#fff0a0')
            elif (x - y) % 13 == 0: px[x, y] = hexc('#a07010')
    return im


def _gem():
    im = Image.new('RGBA', (64, 64), hexc('#b0101c')); d = ImageDraw.Draw(im)
    d.polygon([(8, 1), (14, 4), (14, 12), (8, 15), (2, 12), (2, 4)], fill=hexc('#e01a2c'), outline=hexc('#6a0008'))
    d.polygon([(8, 4), (11, 6), (11, 10), (8, 12), (5, 10), (5, 6)], fill=hexc('#ff4a5a'))
    d.ellipse((6, 5, 9, 8), fill=hexc('#ffd0d8'))
    return im


def _fire(seed):
    im = Image.new('RGBA', (64, 64)); px = im.load(); rnd = random.Random(seed)
    for y in range(64):
        for x in range(64):
            t = y / 63
            c = GLOW[3] if t > 0.75 else GLOW[2] if t > 0.45 else GLOW[1] if t > 0.2 else GLOW[0]
            px[x, y] = _sh(hexc(c), 1 + rnd.uniform(-0.08, 0.08)) + (255,)
    return im


def _face(kind=None):
    """36 x 32 on a 64 x 64 sheet (the head's front face takes uv [0, 0, 9, 8]). The sketch's eyes, small and angry: an
    almond with a rounded bottom and a heavy upper lid that slants down toward her nose, a violet iris with a slit pupil and
    one glint, a lash flick at the outer corner; brows slanting down hard over them. The expressions change as little as
    they need to."""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(SKIN)); px = im.load(); d = ImageDraw.Draw(im)
    for y in range(4):                                                       # the bangs' shadow along the top
        for x in range(36): px[x, y] = P(SKIN_DK)
    LINE, BROW, WHITE = P('#2a0e10'), P('#7a1608'), P('#fff8f0')
    IR, IR_LT, PUP = P('#5a2aa0'), P('#9a6ae0'), P('#14081e')
    W, BOT = 9, 25                                                           # eye width; the row of the lowest point
    slope = {'fierce': 0.42, 'shout': 0.3, 'hurt': -0.15, 'grin': 0.32}.get(kind, 0.36)
    for flip in (False, True):
        x0 = 5 if not flip else 22                                           # the eye's outer-left pixel (her right eye on the left)
        cols = []
        for i in range(W):
            t = i / (W - 1)                                                  # 0 outer corner .. 1 inner corner (mirrored for her left)
            u = t if not flip else 1 - t
            top = 16 + round(u * slope * 6)                                  # the lid: higher at the outside, down toward the nose
            bot = BOT - round(4.0 * (2 * t - 1) ** 2)                         # the rounded bottom
            cols.append((x0 + i, top, bot))
        if kind == 'blink':
            for x, top, bot in cols: px[x, (top + bot) // 2] = LINE; px[x, (top + bot) // 2 + 1] = LINE
        else:
            cx = x0 + W // 2
            for x, top, bot in cols:
                for y in range(top, bot + 1):
                    px[x, y] = WHITE
                    edge = abs(x - cx) == 2 and (y >= bot or y <= top + 1)              # (round the iris's corners)
                    if abs(x - cx) <= 2 and not edge: px[x, y] = IR_LT if y >= bot - 2 else IR
                px[x, top] = LINE; px[x, top - 1] = LINE                          # the heavy lid
            px[cx, cols[cx - x0][1] + 1] = PUP
            for y in range(cols[cx - x0][1] + 1, BOT - 1): px[cx, y] = PUP       # the slit pupil
            gx = cx - 1 if not flip else cx + 1
            px[gx, cols[gx - x0][1] + 2] = WHITE                                   # one glint
            ox, oy = (cols[0][0] - 1, cols[0][1] - 1) if not flip else (cols[-1][0] + 1, cols[-1][1] - 1)
            px[ox, oy] = LINE; px[ox + (-1 if not flip else 1), oy - 1] = LINE     # the lash flick
            for x, top, bot in cols[1:-1]: px[x, bot + 1] = P(SKIN_DK)             # the lower lid, soft
        # the brow: slanting down to the nose (fierce harder), lifted inside when hurt
        for i in range(W + 1):
            t = i / W; u = t if not flip else 1 - t
            x = x0 - 1 + i
            y = 12 + round(u * (slope + 0.18) * 7) if kind != 'hurt' else 13 - round(u * 3)
            px[x, y] = BROW; px[x, y + 1] = BROW
    px[18, 26] = P(SKIN_DK); px[18, 27] = P(SKIN_DK)                                # the nose
    for x, y in ((31, 28), (32, 29)): px[x, y] = P('#6a4a40')                       # a smudge of ash
    M = P('#5a1010')
    if kind == 'grin':                                                              # a hard smirk, one corner up
        d.line((16, 29, 20, 29), fill=M); px[21, 28] = M
    elif kind == 'shout':                                                           # a snarl: a small open mouth, teeth top and bottom
        d.rectangle((15, 28, 21, 30), fill=M); d.line((15, 28, 21, 28), fill=P('#f4e8e0')); d.line((16, 30, 20, 30), fill=P('#f4e8e0'))
    elif kind == 'hurt':
        d.line((16, 29, 20, 29), fill=M); px[15, 30] = M; px[21, 30] = M
    else:                                                                           # set, a corner turned down
        d.line((16, 29, 20, 29), fill=M); px[15, 30] = M
    return im


def textures():
    T = {'as_skin': _skin(1402), 'as_skin_ash': _skin(1403, ash=6), 'as_skin_dk': _cloth(SKIN_DK, 1404, var=0.02),
         'as_hair': _hair2(1405, HAIR, shine=(6, 9)), 'as_magma': _magma(1406), 'as_plates': _magma(1407, '#4a0a08', cell=7.0, plates=True),
         'as_hem': _hem(1408), 'as_rock': _cloth('#2a0605', 1409, var=0.05), 'as_gold': _gold(1410), 'as_gem': _gem(), 'as_fire': _fire(1411),
         'as_ember': _cloth(GLOW[2], 1412, var=0.06)}
    T['as_face'] = _face()
    for k in EXPR: T[f'as_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: bare - skin from the hem down, bare feet; a gold anklet (and its little flame charm) on her left
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.55, 2.85) if sx > 0 else (-2.85, -0.55)
        L = [_el((x0, 0.9, -1.1), (x1, 13.2, 1.1), 'as_skin', pv),
             _el((x0 + 0.15, 0.0, -2.0), (x1 - 0.15, 0.95, 0.9), 'as_skin', pv),                     # the foot, slim
             _el((x0 + 0.2, 0.0, -2.75), (x1 - 0.2, 0.55, -1.95), 'as_skin', pv),                     # the toes, low
             _el((x0 + 0.2, 0.0, -2.78), (x1 - 0.2, 0.06, -1.95), 'as_skin_dk', pv)]                  # (their underside)
        if sx < 0:
            L += [_el((x0 - 0.25, 1.6, -1.35), (x1 + 0.25, 2.1, 1.35), 'as_gold', pv),
                  _el((-1.9, 1.05, -1.38), (-1.45, 1.5, -1.26), 'as_gem', pv, uv={'north': [0, 0, 4, 4]})]  # the charm
        return L
    part('as_legr', leg(1)); part('as_legl', leg(-1))

    # ---- body: the magma dress - a flared skirt in tiers to the knee, its hem jagged and hotter; a dark rock waist; the
    #      plated bodice with a jagged neckline; bare shoulders and collarbones above it
    pv = PIVOT['body']
    mg = lambda fr, to, t='as_magma', rot=None: _el(fr, to, t, pv, rot)
    body = [mg((-3.4, 14.6, -2.5), (3.4, 16.0, 2.5)), mg((-4.1, 13.0, -3.0), (4.1, 14.8, 3.0)), mg((-4.8, 11.4, -3.6), (4.8, 13.2, 3.6)),
            mg((-5.4, 9.8, -4.1), (5.4, 11.6, 4.1)), mg((-5.8, 8.8, -4.4), (5.8, 10.0, 4.4), 'as_hem')]
    for i in range(16):                                                  # the jagged hem: shards hanging below it all the way round
        a = (i + 0.5) / 16 * 2 * math.pi; r = 5.2; cx, cz = r * math.sin(a), -r * math.cos(a) * 0.78
        h = 1.1 + 0.6 * ((i * 7) % 3) / 2
        body.append(mg((cx - 0.75, 8.8 - h, cz - 0.55), (cx + 0.75, 8.9, cz + 0.55), 'as_hem'))
    body += [mg((-3.3, 15.8, -2.4), (3.3, 16.8, 2.4), 'as_rock'),                                    # the waist: cooled rock
             mg((-3.0, 16.6, -2.1), (3.0, 21.2, 2.2), 'as_plates'),                                  # the bodice
             mg((-3.15, 19.2, -2.35), (3.15, 21.6, 2.3), 'as_plates')]                               # (the bust, a little fuller)
    for i, x in enumerate((-2.7, -1.6, -0.5, 0.5, 1.6, 2.7)):                                        # the jagged neckline
        hgt = 0.9 if i % 2 == 0 else 0.5
        body.append(mg((x - 0.55, 21.5, -2.4), (x + 0.55, 21.6 + hgt, 2.3), 'as_plates'))
    body += [_el((-2.9, 21.4, -1.9), (2.9, 23.8, 1.9), 'as_skin', pv),                               # bare shoulders, collarbones
             _el((-1.1, 23.6, -1.1), (1.1, 25.3, 1.1), 'as_skin', pv),                               # the neck
             _el((-0.6, 22.4, -2.0), (0.6, 22.6, -1.92), 'as_skin_dk', pv)]                          # (the dip of the collarbones)
    part('as_body', body)

    # ---- head: the face; the bob - flame spikes up through the tiara at the crown, a hook curling out at each jaw; the tiara
    pv = PIVOT['head']; hr = lambda fr, to, rot=None: _el(fr, to, 'as_hair', pv, rot)
    head = [_el((-4.4, 25.0, -3.9), (4.4, 33.0, 3.9), 'as_skin', pv, uv={'north': [0, 0, 9, 8]}),
            hr((-4.8, 31.0, -4.4), (4.8, 33.8, 4.5)), hr((-4.3, 33.6, -3.6), (4.3, 34.8, 3.9)),     # the top
            hr((-4.8, 25.6, 3.2), (4.8, 31.2, 4.6)),                                               # the back, to the jaw
            hr((4.4, 26.6, -2.6), (5.0, 31.2, 4.4)), hr((-5.0, 26.6, -2.6), (-4.4, 31.2, 4.4)),     # the sides
            hr((-4.8, 30.4, -4.6), (-0.6, 31.4, -3.9)), hr((0.6, 30.0, -4.6), (4.8, 31.4, -3.9)),   # the bangs, parted a touch
            hr((-1.0, 29.8, -4.7), (0.4, 31.0, -4.0), ('z', -14, (0, 30.4, -4.3)))]                 # a lock between the brows
    for sx in (1, -1):                                                   # the hooks curling out at her jaw (the sketch's crescents)
        x = sx * 4.7
        head += [hr((x - 0.6, 25.0, -1.8), (x + 0.6, 27.4, 1.6)),
                 hr((x + sx * 0.2 - 0.7, 24.2, -1.6), (x + sx * 0.2 + 0.7, 25.4, 1.4), ('z', -35 * sx, (x, 25.0, 0))),
                 hr((x + sx * 1.0 - 0.6, 24.4, -1.4), (x + sx * 1.0 + 0.6, 25.8, 1.2), ('z', -70 * sx, (x + sx * 0.8, 25.0, 0)))]
    for x, h, lean in ((-3.2, 2.4, 22), (-1.4, 3.2, 8), (0.6, 3.6, -6), (2.4, 2.8, -18), (3.8, 1.8, -30), (-0.4, 2.6, 30)):   # flame spikes at the crown
        head.append(hr((x - 0.8, 34.4, -1.8), (x + 0.8, 34.6 + h, 0.6), ('z', lean, (x, 34.6, 0))))
    # the tiara: a gold band at the hairline, flame points rising off it, the red hexagonal gem in a gold setting on her brow
    head += [_el((-4.95, 31.6, -4.75), (4.95, 32.4, 4.6), 'as_gold', pv)]
    for x, h, lean in ((-3.6, 1.2, 20), (-2.2, 1.7, 10), (2.2, 1.7, -10), (3.6, 1.2, -20)):
        head.append(_el((x - 0.45, 32.3, -4.85), (x + 0.45, 32.3 + h, -4.6), 'as_gold', pv, ('z', lean, (x, 32.4, -4.7))))
    head += [_el((-1.25, 31.8, -4.95), (1.25, 34.4, -4.65), 'as_gold', pv),                         # the setting
             _el((-0.95, 32.1, -5.05), (0.95, 34.1, -4.8), 'as_gem', pv, uv={'north': [0, 0, 4, 4]}),  # the gem
             _el((-0.4, 34.2, -4.85), (0.4, 35.4, -4.65), 'as_gold', pv)]                           # its flame tip
    head[0]['faces']['north']['texture'] = '#as_face'
    part('as_head', head)
    for k in EXPR:                                                       # (a head per expression: only the face differs)
        h2 = [dict(e, faces={f: dict(v) for f, v in e['faces'].items()}) for e in head]
        h2[0]['faces']['north']['texture'] = f'#as_face_{k}'
        part(f'as_head_x{k}', h2)

    # ---- arms: bare, slim; ash on the forearms; hands open (the fire sits in her palms)
    def arm(sx):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.1 * sx
        return [_el((cx - 1.2, 18.6, -1.2), (cx + 1.2, 23.6, 1.2), 'as_skin', pv),
                _el((cx - 1.35, 22.0, -1.35), (cx + 1.35, 23.8, 1.35), 'as_skin', pv)]                  # the shoulder
    def fore(sx):
        nm = 'forer' if sx > 0 else 'forel'; pv = PIVOT[nm]; cx = pv[0]
        return [_el((cx - 1.05, 14.2, -1.05), (cx + 1.05, 19.0, 1.05), 'as_skin_ash', pv),
                _el((cx - 1.2, 15.0, -1.2), (cx + 1.2, 15.6, 1.2), 'as_ember', pv),                      # a glowing band at the wrist
                _el((cx - 1.15, 12.0, -1.3), (cx + 1.15, 14.4, 1.0), 'as_skin', pv),                     # the hand
                _el((cx + (0.9 if sx > 0 else -1.6), 12.6, -1.4), (cx + (1.6 if sx > 0 else -0.9), 13.8, -0.4), 'as_skin_dk', pv)]   # the thumb
    part('as_armr', arm(1)); part('as_arml', arm(-1)); part('as_forer', fore(1)); part('as_forel', fore(-1))

    # ---- the fire in her palms (joint: the palm): a flame of nested boxes, yellow-white at the heart
    g = (0.0, 0.0, 0.0)
    FU = {f: [0, 0, 16, 16] for f in ('north', 'south', 'east', 'west', 'up', 'down')}
    fl = lambda fr, to, rot=None: _el(fr, to, 'as_fire', g, rot, uv=FU)
    fire = [fl((-1.3, -0.4, -1.3), (1.3, 1.4, 1.3)), fl((-0.9, 1.2, -0.9), (0.9, 2.8, 0.9), ('y', 45, (0, 2, 0))),
            fl((-0.5, 2.6, -0.5), (0.5, 4.0, 0.5)), fl((0.6, 1.0, -0.3), (1.2, 2.4, 0.3), ('z', -20, (0.9, 1.0, 0))),
            fl((-1.2, 0.8, -0.3), (-0.6, 2.0, 0.3), ('z', 20, (-0.9, 0.8, 0))), _el((-0.6, -0.1, -0.6), (0.6, 1.2, 0.6), 'as_ember', g)]
    part('as_firer', fire); part('as_firel', fire)
    return M


# ---------------------------------------------------------------------------------------------------- poses
I = (0.0, 0.0, 0.0, 1.0)
U = RIG_SCALE / 16
BENT = qa('x', -24)
def P(dy=0.0, face=None, fire=(), **parts):
    d = {k: I for k in PARTS}; d.update(parts); d['_dy'] = dy; d['_face'] = face; d['_fire'] = tuple(fire)
    return d
# (her idle: a fighter's stance - weight on her left, right hand up and open with a flame in it, left fist at her side)
IDLE = dict(body=torso(tilt=-3, turn=8), head=qmul(qa('y', -10), qa('x', 4)), armr=limb(1, 44, 10), forer=qa('x', -70), arml=limb(-1, -4, 10), forel=BENT,
            legr=limb(1, 6, 4), legl=limb(-1, -4, 2))
POSES = {
    'idle': P(face='fierce', fire=('r',), **IDLE),
    'idle_b': P(0.01, face='fierce', fire=('r',), **dict(IDLE, armr=limb(1, 50, 12), forer=qa('x', -64), head=qmul(qa('y', -4), qa('x', 2)))),
    'blink': P(face='blink', fire=('r',), **IDLE),
    # walk: a quick, stamping stride - she's barefoot and it doesn't slow her at all
    'walk_a': P(body=torso(tilt=3), head=torso(tilt=-3), legr=limb(1, 26), legl=limb(-1, -26), arml=limb(-1, 22, 8), forel=BENT, armr=limb(1, -18, 8), forer=BENT),
    'walk_up': P(0.04, legr=limb(1, 4), legl=limb(-1, -4), arml=limb(-1, 0, 8), forel=BENT, armr=limb(1, 0, 8), forer=BENT),
    'walk_b': P(body=torso(tilt=-3), head=torso(tilt=3), legr=limb(1, -26), legl=limb(-1, 26), arml=limb(-1, -22, 8), forel=BENT, armr=limb(1, 18, 8), forer=BENT),
    # run: leaning hard, both hands trailing fire
    'run_a': P(0.02, face='fierce', fire=('r', 'l'), body=torso(lean=14, tilt=4), head=torso(lean=-12), legr=limb(1, 46), legl=limb(-1, -42),
               arml=limb(-1, -40, 16), forel=qa('x', -30), armr=limb(1, 22, 12), forer=qa('x', -24)),
    'run_up': P(0.1, face='fierce', fire=('r', 'l'), body=torso(lean=14), head=torso(lean=-12), legr=limb(1, 12), legl=limb(-1, -30),
                arml=limb(-1, 0, 20), forel=qa('x', -40), armr=limb(1, 10, 18), forer=qa('x', -50)),
    'run_b': P(0.02, face='fierce', fire=('r', 'l'), body=torso(lean=14, tilt=-4), head=torso(lean=-12), legr=limb(1, -42), legl=limb(-1, 46),
               arml=limb(-1, 22, 12), forel=qa('x', -24), armr=limb(1, -40, 16), forer=qa('x', -30)),
    # jump: the sketch's leap - knees up, both hands high and burning
    'jump': P(face='shout', fire=('r', 'l'), body=torso(lean=4), head=torso(lean=-10), legr=limb(1, 70), legl=limb(-1, -30),
              armr=limb(1, 150, 30), forer=qa('x', -30), arml=limb(-1, 150, 30), forel=qa('x', -30)),
    # the fireball: drawn back past her hip, then flung from the shoulder
    'cast_back': P(face='fierce', fire=('r',), body=torso(lean=-6, turn=-24), head=torso(turn=18), legr=limb(1, -16), legl=limb(-1, 20),
                   arml=limb(-1, 40, 20), forel=qa('x', -40), armr=limb(1, -50, 24), forer=qa('x', -40)),
    'cast': P(0.01, face='shout', body=torso(lean=12, turn=16), head=torso(lean=-6, turn=-10), legr=limb(1, -26), legl=limb(-1, 32),
              arml=limb(-1, -30, 24), forel=BENT, armr=limb(1, 90, 2), forer=I),
    # the flamethrower: both hands thrust ahead, palms together
    'blast': P(-0.02, face='shout', fire=('r', 'l'), body=torso(lean=8), head=torso(lean=-6), legr=limb(1, -18), legl=limb(-1, 24),
               armr=limb(1, 88, -14), forer=I, arml=limb(-1, 88, -14), forel=I),
    # the eruption (her great blow): crouched, then up with both arms flung wide
    'crouch': P(-0.12, face='fierce', fire=('r', 'l'), body=torso(lean=18), head=torso(lean=-14), legr=limb(1, 40), legl=limb(-1, 40),
                armr=limb(1, 30, 30), forer=qa('x', -80), arml=limb(-1, 30, 30), forel=qa('x', -80)),
    'erupt': P(0.06, face='shout', fire=('r', 'l'), body=torso(lean=-10), head=torso(lean=-16), legr=limb(1, -6, 8), legl=limb(-1, -6, 8),
               armr=limb(1, 160, 40), forer=I, arml=limb(-1, 160, 40), forel=I),
    # sit: cross-legged-ish, leaning back on her hands, toes wriggling
    'sit_a': P(-0.58, face='grin', body=torso(lean=-10), head=qmul(qa('y', 12), qa('z', -6)), legr=limb(1, 84, 10), legl=limb(-1, 80, 10),
               arml=limb(-1, -30, 16), forel=qa('x', 10), armr=limb(1, -30, 16), forer=qa('x', 10)),
    'sit_b': P(-0.58, face='grin', body=torso(lean=-10), head=qmul(qa('y', 4), qa('z', -2)), legr=limb(1, 74, 10), legl=limb(-1, 86, 10),
               arml=limb(-1, -30, 16), forel=qa('x', 10), armr=limb(1, -30, 16), forer=qa('x', 10)),
    'wave': P(face='grin', armr=limb(1, 10, 140), forer=qa('x', -30), arml=limb(-1, -4, 10), forel=BENT, head=qa('y', -10)),
    'hurt': P(face='hurt', body=torso(lean=-8), head=torso(lean=-12), armr=limb(1, 30, 20), forer=qa('x', -60), arml=limb(-1, 30, 20), forel=qa('x', -60)),
    'tired': P(-0.1, face='hurt', body=torso(lean=16, tilt=-4), head=torso(lean=18), armr=limb(1, 0, 4), arml=limb(-1, 0, 4), forer=BENT, forel=BENT,
               legr=limb(1, 10, 4), legl=limb(-1, -6, 4)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (she hates water: head well up, a frantic paddle)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(-0.66 + 0.03 * math.sin(2 * _p), face='hurt', body=torso(lean=10), head=qa('x', -14),
                            armr=limb(1, 80 + 30 * math.sin(_p), 18), forer=qa('x', -30 - 18 * math.cos(_p)),
                            arml=limb(-1, 80 - 30 * math.sin(_p), 18), forel=qa('x', -30 + 18 * math.cos(_p)),
                            legr=limb(1, -16 + 18 * math.sin(2 * _p)), legl=limb(-1, -16 - 18 * math.sin(2 * _p)))
DRAFT = ['idle', 'walk_a', 'run_a', 'jump', 'cast_back', 'cast', 'blast', 'erupt', 'sit_a', 'wave', 'hurt', 'tired']


def HIDDEN(p, pose):
    return (p == 'firer' and 'r' not in pose.get('_fire', ())) or (p == 'firel' and 'l' not in pose.get('_fire', ()))


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


def _off(a, b):
    return (-(b[0] - a[0]) * U, (b[1] - a[1]) * U, -(b[2] - a[2]) * U)


def part_xf(pose, p):
    """(left_rotation, translation): forearms hang from their elbows, the fires sit in her palms wherever the arms carry them"""
    dy = pose['_dy']
    if p in ('forer', 'forel', 'firer', 'firel'):
        r = p in ('forer', 'firer')
        up, fo = ('armr', 'forer') if r else ('arml', 'forel')
        e = _qrot(pose[up], _off(PIVOT[up], PIVOT[fo]))
        fq = qmul(pose[up], pose[fo])
        if p.startswith('fire'):
            g = _qrot(fq, _off(PIVOT[fo], PALMR if r else PALML))
            return I, (e[0] + g[0], e[1] + g[1] + dy, e[2] + g[2])                # (the flame stays upright)
        return fq, (e[0], e[1] + dy, e[2])
    return pose[p], (0.0, dy, 0.0)


def joint(p):
    return PIVOT[{'firer': 'armr', 'forer': 'armr', 'firel': 'arml', 'forel': 'arml'}.get(p, p)]
