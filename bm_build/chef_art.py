"""The Chef (2.86): from the owner's art. Short and stocky - a head shorter than a player, broad in the middle: a tall white
toque, pleated at the band and puffed on top; an orange face with big round eyes and a great black curled moustache; a red
bow tie; a white double-breasted jacket (two rows of black buttons) over a round belly; black-and-white check trousers and
black shoes. His ladle rides in his right hand.

A rigkit rig like Dennis's: body, head (a model per expression - its face painted on), the arms bent at the elbow, the legs,
and the ladle (on his right forearm). Design units: feet at y=0, facing -z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain, I

PREFIX = 'cf_'
RIG_SCALE = 0.82
PIVOT = {'body': (0, 6.4, 0), 'legr': (2.1, 6.4, 0), 'legl': (-2.1, 6.4, 0), 'head': (0, 14.6, 0),
         'armr': (5.0, 13.4, 0), 'forer': (5.5, 9.8, 0), 'arml': (-5.0, 13.4, 0), 'forel': (-5.5, 9.8, 0),
         'ladle': (5.7, 6.8, -0.4)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'ladle': 'forer'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'shout', 'hurt', 'blink')
SKIN, SKIN_DK = '#f08a3a', '#c86a24'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return p == 'ladle' and pose.get('_noladle', False)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _face(kind=None):
    """the front of his head, 64 x 64, from the owner's art: two huge round eyes spread across his face (small pupils glancing up
    and to the side, the lower half of each eye a shade greyer), thin brows - his left one raised; red freckled cheeks; a small
    round "o" of a mouth under the moustache (that's 3D) and a little chin line. No nose shows."""
    im = _noise(SKIN, 1401, 5).resize((64, 64)); d = ImageDraw.Draw(im)
    ink, white, grey = hexc('#141010'), hexc('#ffffff'), hexc('#d4d4d6')
    for cx in (9, 55):                                        # the cheeks: red, a couple of white freckles
        d.ellipse((cx - 8, 34, cx + 8, 44), fill=hexc('#e2502a')[:3] + (150,))
        d.point((cx - 2, 37), fill=white); d.point((cx + 3, 39), fill=white); d.point((cx, 41), fill=hexc('#ffd0c0'))
    E = ((17, 21), (47, 21)); r = 12                          # the eyes: big, wide-set, nearly touching
    for i, (cx, cy) in enumerate(E):
        if kind == 'happy':
            d.arc((cx - 11, cy - 6, cx + 11, cy + 12), 200, 340, fill=ink, width=3)
            continue
        if kind == 'blink':
            d.line((cx - 11, cy + 2, cx + 11, cy + 2), fill=ink, width=3)
            continue
        if kind == 'hurt':
            d.line((cx - 8, cy - 6, cx + 8, cy + 6), fill=ink, width=3); d.line((cx - 8, cy + 6, cx + 8, cy - 6), fill=ink, width=3)
            continue
        rr = r + (1 if kind == 'shout' else 0)
        d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=white, outline=ink, width=2)
        d.chord((cx - rr + 2, cy - rr + 2, cx + rr - 2, cy + rr - 2), 8, 172, fill=grey)          # (the lower half, greyer)
        d.line((cx - rr + 3, cy + 2, cx + rr - 3, cy), fill=hexc('#bdbdc0'))
        if kind == 'shout':
            px, py, pr = cx, cy, 2                                                          # (pinpricks, dead centre)
        else:
            px, py, pr = cx + 3, cy - 1, 4                                                  # (glancing up and to his left)
        d.ellipse((px - pr, py - pr, px + pr, py + pr), fill=ink)
        d.ellipse((px - pr + 1, py - pr + 1, px - pr + 2, py - pr + 2), fill=white)
        d.point((px + 1, py + 1), fill=white)
        d.ellipse((cx - rr + 5, cy - rr + 5, cx - rr + 7, cy - rr + 7), fill=white)           # the glint
    # brows: thin, as drawn - his right flat, his left raised in a worried curve (a shout: both up; hurt: knitted)
    if kind == 'shout':
        d.arc((5, 2, 29, 12), 200, 340, fill=ink, width=3); d.arc((35, 2, 59, 12), 200, 340, fill=ink, width=3)
    elif kind == 'hurt':
        d.line((6, 7, 26, 10), fill=ink, width=3); d.line((38, 10, 58, 7), fill=ink, width=3)
    elif kind == 'happy':
        d.arc((6, 4, 28, 14), 200, 340, fill=ink, width=3); d.arc((36, 4, 58, 14), 200, 340, fill=ink, width=3)
    else:
        d.line((7, 8, 25, 7), fill=ink, width=3)
        d.arc((37, 3, 59, 13), 200, 330, fill=ink, width=3)
    # the mouth, under the moustache (which covers rows ~40-48)
    if kind == 'shout':
        d.ellipse((26, 49, 38, 61), fill=hexc('#5a0e10'), outline=ink); d.ellipse((29, 55, 35, 60), fill=hexc('#c0303a'))
    elif kind == 'happy':
        d.chord((24, 46, 40, 60), 0, 180, fill=hexc('#5a0e10'), outline=ink); d.chord((27, 53, 37, 59), 0, 180, fill=hexc('#c0303a'))
    elif kind == 'hurt':
        d.line((26, 55, 30, 52), fill=ink, width=2); d.line((30, 52, 34, 55), fill=ink, width=2); d.line((34, 55, 38, 52), fill=ink, width=2)
    else:
        d.ellipse((28, 50, 36, 57), fill=hexc('#6a1014'), outline=ink); d.ellipse((30, 51, 33, 54), fill=hexc('#a02028'))
        d.arc((28, 57, 36, 62), 30, 150, fill=ink)                                          # (the little chin line)
    return im


def _hair(seed):
    im = _noise('#2a1a12', seed, 6); rnd = random.Random(seed)
    for x in range(0, 64, 3):
        for y in range(rnd.randrange(3), 64, 5):
            im.putpixel((x, y), hexc(rnd.choice(['#3e281c', '#1a100a', '#4a3020'])))
    return im


def _whites(seed, base='#fbfaf6', sh='#e2e0da'):
    im = _noise(base, seed, 4); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(10):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-6, 6), y + rnd.randint(4, 12)), fill=hexc(sh))
    return im


def _pleats(seed):
    im = _whites(seed); d = ImageDraw.Draw(im)
    for x in range(0, 64, 6):
        d.line((x, 0, x, 63), fill=hexc('#d0cec8'), width=2); d.line((x + 2, 0, x + 2, 63), fill=hexc('#ffffff'))
    return im


def _check(seed):
    im = Image.new('RGBA', (64, 64), hexc('#f2f2f2')); d = ImageDraw.Draw(im)
    for y in range(0, 64, 4):
        for x in range(0, 64, 4):
            if (x // 4 + y // 4) % 2 == 0:
                d.rectangle((x, y, x + 3, y + 3), fill=hexc('#1c1c1e'))
    return im


def _jacket(seed):
    im = _whites(seed); d = ImageDraw.Draw(im)
    d.line((32, 0, 50, 63), fill=hexc('#cfcdc6'), width=2)    # the double-breasted flap
    return im


def _bow(seed):
    im = _shine('#c81e24', '#ff6a5a', seed); d = ImageDraw.Draw(im)
    d.rectangle((26, 20, 38, 44), fill=hexc('#8a1014'))
    return im


def textures():
    T = {'cf_skin': _noise(SKIN, 1402, 6), 'cf_skin_dk': _noise(SKIN_DK, 1403, 5), 'cf_white': _whites(1404), 'cf_toque': _whites(1417), 'cf_white_dk': _whites(1405, '#dcd9d0', '#bebab0'),
         'cf_pleat': _pleats(1406), 'cf_jacket': _jacket(1407), 'cf_check': _check(1408), 'cf_shoe': _shine('#1a1a1c', '#4a4a52', 1409),
         'cf_stache': _shine('#121214', '#3a3a40', 1410), 'cf_bow': _bow(1411), 'cf_steel': _shine('#9aa2b4', '#eef2f8', 1412),
         'cf_steel_dk': _shine('#5e6476', '#9aa2b4', 1413), 'cf_wood': _shine('#8a5a2e', '#c08a52', 1414), 'cf_button': _noise('#1c1c1e', 1415, 2),
         'cf_face': _face(), 'cf_hair': _hair(1416)}
    for k in FACES:
        T[f'cf_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the round belly in the white double-breasted jacket, its hem over the check trousers; the red bow tie
    pv = PIVOT['body']
    body = [el((-3.9, 5.8, -2.4), (3.9, 7.6, 2.4), 'cf_check', pv),
            el((-4.3, 7.0, -2.9), (4.3, 14.4, 2.8), 'cf_white', pv, shift=(0.1, 0.5)),
            el((-4.3, 7.0, -2.92), (4.3, 14.4, -2.9), 'cf_jacket', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((-3.8, 7.6, -3.7), (3.8, 12.6, -2.6), 'cf_white', pv, shift=(0.3, 0.4)),         # the belly, round out front
            el((-3.0, 8.2, -4.2), (3.0, 12.0, -3.5), 'cf_white', pv, shift=(0.6, 0.1)),
            el((-4.5, 6.8, -3.0), (4.5, 7.4, 2.95), 'cf_white_dk', pv),                       # the hem
            el((-3.2, 13.6, -3.0), (3.2, 14.9, 2.6), 'cf_white_dk', pv),                      # the collar
            el((-0.5, 13.4, -3.25), (0.5, 14.4, -3.0), 'cf_bow', pv),                         # the bow tie's knot ...
            el((-2.3, 13.0, -3.2), (-0.4, 14.8, -2.95), 'cf_bow', pv, shift=(0.2, 0.3)),      # ... and its wings
            el((0.4, 13.0, -3.2), (2.3, 14.8, -2.95), 'cf_bow', pv, shift=(0.7, 0.3))]
    for x in (-1.3, 1.3):                                                                     # two rows of buttons, standing proud
        for y in (8.6, 10.2, 11.8):
            body.append(el((x - 0.35, y - 0.35, -4.3 if y < 12 else -3.0), (x + 0.35, y + 0.35, -4.15 if y < 12 else -2.85), 'cf_button', pv))
    part('cf_body', body)

    # ---- the head: big and round-cheeked, its face painted (a head per expression), the great curled moustache, a button
    #      nose, ears; the toque: a pleated band, then the puff, wider, rounded on top
    pv = PIVOT['head']
    def head(face=None):
        tex = 'cf_face' if face is None else f'cf_face_{face}'
        h = [el((-1.6, 14.2, -1.5), (1.6, 15.2, 1.5), 'cf_skin_dk', pv),                       # the neck
             el((-4.1, 15.0, -3.7), (4.1, 22.4, 3.5), 'cf_skin', pv, shift=(0.3, 0.2)),
             el((-4.1, 15.0, -3.72), (4.1, 22.4, -3.70), tex, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-4.9, 16.6, -0.9), (-4.05, 19.9, 0.7), 'cf_skin', pv), el((4.05, 16.6, -0.9), (4.9, 19.9, 0.7), 'cf_skin', pv),   # big ears
             el((-4.95, 17.2, -0.5), (-4.85, 19.3, 0.3), 'cf_skin_dk', pv), el((4.85, 17.2, -0.5), (4.95, 19.3, 0.3), 'cf_skin_dk', pv)]
        # the moustache, as drawn: a broad black zigzag from cheek to cheek - its ends down and pointed, two peaks either side of
        # a dip in the middle, its lower edge straight over the little mouth
        h += chain([(-4.15, 16.55, -3.85), (-2.6, 17.2, -3.95), (-1.25, 17.75, -4.0), (0.0, 17.15, -4.05), (1.25, 17.75, -4.0), (2.6, 17.2, -3.95), (4.15, 16.55, -3.85)],
                   [0.5, 0.9, 0.95, 0.95, 0.9, 0.5], 0.5, 'cf_stache', pv, FRONT, ext=0.12)
        h.append(el((-3.3, 16.7, -4.02), (3.3, 17.2, -3.72), 'cf_stache', pv))
        # his hair: dark and thick under the toque - full at the back, down past his ears at the sides (the band hides his brow)
        h += [el((-4.25, 16.6, 1.0), (4.25, 22.6, 3.75), 'cf_hair', pv, shift=(0.2, 0.3)),
              el((-4.3, 17.6, -2.6), (-3.95, 22.6, 1.4), 'cf_hair', pv), el((3.95, 17.6, -2.6), (4.3, 22.6, 1.4), 'cf_hair', pv),
              el((-4.35, 16.4, -2.4), (-4.0, 18.2, -1.0), 'cf_hair', pv), el((4.0, 16.4, -2.4), (4.35, 18.2, -1.0), 'cf_hair', pv)]   # sideburns
        # (owner's note: a little of it showing from the front - tufts at the temples and a ragged edge under the band)
        for sx in (-1, 1):
            h += [el((sx * 4.15 - 0.55, 20.0, -3.85), (sx * 4.15 + 0.55, 22.2, -3.5), 'cf_hair', pv, shift=(0.3, 0.6)),
                  el((sx * 3.2 - 0.6, 21.3, -3.82), (sx * 3.2 + 0.6, 22.2, -3.68), 'cf_hair', pv, shift=(0.7, 0.2))]
        for x in (-1.6, 0.0, 1.6):
            h.append(el((x - 0.5, 21.75, -3.8), (x + 0.5, 22.2, -3.68), 'cf_hair', pv, shift=(x * 0.1 + 0.4, 0.5)))
        # the toque
        h += [el((-3.9, 22.0, -3.5), (3.9, 24.6, 3.3), 'cf_pleat', pv),
              el((-4.7, 24.4, -4.3), (4.7, 28.6, 4.1), 'cf_toque', pv, shift=(0.2, 0.3)),
              el((-4.2, 28.4, -3.8), (4.2, 29.6, 3.6), 'cf_toque', pv, shift=(0.7, 0.1)),
              el((-3.2, 29.4, -2.8), (3.2, 30.2, 2.6), 'cf_toque', pv, shift=(0.4, 0.6))]
        for x, z in ((-2.6, -2.4), (2.4, -2.0), (0.0, 2.2)):                                  # its puffs
            h.append(el((x - 1.7, 27.6, z - 1.7), (x + 1.7, 30.0, z + 1.7), 'cf_toque', pv, shift=(x * 0.1, z * 0.1)))
        return h
    part('cf_head', head())
    for fc in FACES:
        part(f'cf_head_x{fc}', head(fc))

    # ---- the arms: white sleeves, rolled cuffs, orange hands
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        a = [el((x0 - 1.6, y0 - 1.5, -1.7), (x0 + 1.6, y0 + 1.2, 1.7), 'cf_white', pv, shift=(0.4, 0.2))]
        a += chain([(x0, y0, 0), (sx * 5.5, 9.8, 0)], [3.0], 3.0, 'cf_white', pv, FRONT, ext=0.3)
        return a
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 5.7, 7.2
        a = chain([(ex, ey, 0), (wx, wy, 0)], [2.8], 2.8, 'cf_white', pv, FRONT, ext=0.25)
        a += [el((wx - 1.6, wy - 0.2, -1.6), (wx + 1.6, wy + 0.8, 1.6), 'cf_white_dk', pv),          # the rolled cuff
              el((wx - 1.25, wy - 2.2, -1.3), (wx + 1.25, wy - 0.1, 1.2), 'cf_skin', pv),
              el((wx - 1.0, wy - 2.45, -1.4), (wx + 1.0, wy - 1.8, -0.9), 'cf_skin_dk', pv)]
        return a
    part('cf_armr', upper(1)); part('cf_arml', upper(-1)); part('cf_forer', lower(1)); part('cf_forel', lower(-1))

    # ---- the legs: check trousers, black shoes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 1.8, 1.4, -1.6), (cx + 1.8, 6.8, 1.6), 'cf_check', pv, shift=(0.3 if sx > 0 else 0.6, 0.2)),
                el((cx - 1.85, 0.0, -2.9), (cx + 1.85, 1.6, 1.8), 'cf_shoe', pv),
                el((cx - 1.6, 0.0, -3.5), (cx + 1.6, 1.3, -2.6), 'cf_shoe', pv, shift=(0.5, 0.5))]
    part('cf_legr', leg(1)); part('cf_legl', leg(-1))

    # ---- the ladle: a wooden handle in his fist, its steel bowl hanging below
    pv = PIVOT['ladle']; x = 5.7
    lad = [el((x - 0.35, 4.6, -0.75), (x + 0.35, 8.4, -0.05), 'cf_wood', pv),
           el((x - 0.3, 3.0, -0.7), (x + 0.3, 4.8, -0.1), 'cf_steel_dk', pv),
           el((x - 1.2, 1.6, -1.5), (x + 1.2, 3.1, 0.7), 'cf_steel', pv),
           el((x - 0.95, 3.05, -1.25), (x + 0.95, 3.15, 0.45), 'cf_steel_dk', pv)]
    part('cf_ladle', lad)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


IDLE = dict(armr=limb(1, 6, 8), forer=limb(1, 14), arml=limb(-1, -4, 10), forel=limb(-1, 20), head=qs(('y', 6)))
POSES = {
    'idle_a': P(**IDLE),
    'idle_b': P(_off=(0, -0.15, 0), **dict(IDLE, armr=limb(1, 4, 9), forer=limb(1, 18), head=qs(('y', -6), ('x', 3)))),
    # walk: a busy waddle - he rocks side to side
    'walk_a': P(_off=(0, 0.25, 0), body=qs(('z', 5)), legr=limb(1, 26), legl=limb(-1, -24), armr=limb(1, -14, 8), arml=limb(-1, 20, 8),
                forer=limb(1, 14), forel=limb(-1, 24), head=qs(('z', -3))),
    'walk_up': P(_off=(0, 0.5, 0), legr=limb(1, 4), legl=limb(-1, -4), armr=limb(1, 2, 8), arml=limb(-1, 2, 8), forer=limb(1, 16), forel=limb(-1, 18)),
    'walk_b': P(_off=(0, 0.25, 0), body=qs(('z', -5)), legr=limb(1, -24), legl=limb(-1, 26), armr=limb(1, 16, 8), arml=limb(-1, -18, 8),
                forer=limb(1, 18), forel=limb(-1, 18), head=qs(('z', 3))),
    'run_a': P(_off=(0, 0.4, 0), body=qs(('x', 12), ('z', 6)), head=qs(('x', -10)), legr=limb(1, 44), legl=limb(-1, -38), armr=limb(1, -34, 14), arml=limb(-1, 36, 14),
               forer=limb(1, 50), forel=limb(-1, 50)),
    'run_up': P(_off=(0, 1.0, 0), body=qs(('x', 12)), head=qs(('x', -10)), legr=limb(1, 14), legl=limb(-1, -20), armr=limb(1, 4, 16), arml=limb(-1, 4, 16),
                forer=limb(1, 60), forel=limb(-1, 60)),
    'run_b': P(_off=(0, 0.4, 0), body=qs(('x', 12), ('z', -6)), head=qs(('x', -10)), legr=limb(1, -38), legl=limb(-1, 44), armr=limb(1, 36, 14), arml=limb(-1, -34, 14),
               forer=limb(1, 50), forel=limb(-1, 50)),
    'jump': P(_face='shout', _off=(0, 1.2, 0), legr=limb(1, 50), legl=limb(-1, 20), armr=limb(1, 120, 30), forer=limb(1, 20), arml=limb(-1, 120, 30), forel=limb(-1, 20)),
    # his whack: the ladle up, then down on the foe's head
    'whack_up': P(_face='shout', body=qs(('x', -6), ('y', -10)), armr=limb(1, 160, 10), forer=limb(1, 30), arml=limb(-1, 10, 20), forel=limb(-1, 40)),
    'whack': P(_face='shout', _off=(0, -0.3, 0), body=qs(('x', 14), ('y', 8)), head=qs(('x', -8)), armr=limb(1, 70, 4), forer=limb(1, 0),
               arml=limb(-1, -10, 20), forel=limb(-1, 30)),
    # a throw (the food attacks): the left hand back past his ear, then flung - overarm
    'throw_back': P(body=qs(('y', 20), ('x', -4)), head=qs(('y', -14)), arml=limb(-1, 150, -10), forel=limb(-1, 70), armr=limb(1, 20, 20), forer=limb(1, 30),
                    legr=limb(1, 14), legl=limb(-1, -10)),
    'throw': P(_face='shout', body=qs(('y', -18), ('x', 10)), head=qs(('y', 10), ('x', -6)), arml=limb(-1, 80, 4), forel=limb(-1, 0), armr=limb(1, -10, 20),
               forer=limb(1, 30), legr=limb(1, -16), legl=limb(-1, 20)),
    # stirring (cooking up a buff), and tasting
    'stir_a': P(_face='happy', armr=limb(1, 50, -10), forer=limb(1, 40), arml=limb(-1, 40, 14), forel=limb(-1, 60), head=qs(('x', 14))),
    'stir_b': P(_face='happy', armr=limb(1, 50, 10), forer=limb(1, 60), arml=limb(-1, 40, 14), forel=limb(-1, 60), head=qs(('x', 14), ('y', 6))),
    'taste': P(_face='happy', _off=(0, 0.2, 0), armr=limb(1, 4, 8), forer=limb(1, 14), arml=limb(-1, 60, -16), forel=limb(-1, 110), head=qs(('x', -12))),
    # the Feast (his great move): the ladle raised high, the other arm wide
    'feast': P(_face='happy', _off=(0, 0.6, 0), body=qs(('x', -8)), head=qs(('x', -16)), armr=limb(1, 170, 10), forer=limb(1, 0), arml=limb(-1, 30, 80),
               forel=limb(-1, 10)),
    'wave_a': P(_face='happy', armr=limb(1, 4, 8), forer=limb(1, 14), arml=limb(-1, 10, 120), forel=limb(-1, 40), head=qs(('y', -8))),
    'sit_a': P(_off=(0, -4.2, 0), legr=limb(1, 84, 10), legl=limb(-1, 84, 10), armr=limb(1, 24, 12), forer=limb(1, 50), arml=limb(-1, 24, 12),
               forel=limb(-1, 54), head=qs(('y', 8))),
    'sit_b': P(_face='blink', _off=(0, -4.35, 0), body=qs(('x', 4)), legr=limb(1, 80, 10), legl=limb(-1, 86, 10), armr=limb(1, 26, 12), forer=limb(1, 54),
               arml=limb(-1, 26, 12), forel=limb(-1, 56), head=qs(('x', 12), ('y', -4))),
    'hurt': P(_face='hurt', body=qs(('x', -8)), head=qs(('x', -12)), armr=limb(1, 30, 30), forer=limb(1, 60), arml=limb(-1, 30, 30), forel=limb(-1, 60)),
    'tired': P(_face='hurt', _off=(0, -0.8, 0), body=qs(('x', 12), ('z', -4)), head=qs(('x', 16)), armr=limb(1, 0, 6), arml=limb(-1, 0, 6),
               forer=limb(1, 6), forel=limb(-1, 6), legr=limb(1, 6, 4), legl=limb(-1, -4, 4)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (a doggy paddle, toque well clear of the water)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='shout', _off=(0, -5.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 20)), head=qs(('x', -22)),
                            armr=limb(1, 90 + 30 * math.sin(_p), 20), forer=limb(1, 30 + 20 * math.cos(_p)),
                            arml=limb(-1, 90 - 30 * math.sin(_p), 20), forel=limb(-1, 30 - 20 * math.cos(_p)),
                            legr=limb(1, -10 + 20 * math.sin(2 * _p)), legl=limb(-1, -10 - 20 * math.sin(2 * _p)))
DRAFT = ['idle_a', 'walk_a', 'run_a', 'jump', 'whack_up', 'whack', 'throw_back', 'throw', 'stir_a', 'taste', 'feast', 'sit_a', 'hurt', 'tired']


# (2.93e: every material with life in it - matkit)
import matkit as _mk
textures = _mk.wrapped(textures, __name__)
