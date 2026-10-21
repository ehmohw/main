"""The Neighbor (2.86): from the owner's art. A cheerful musician of a lad with a big head: a black beret slumped to one side, an
orange button on its crown; spiky reddish-brown hair; a white mime's mask over his eyes, thick black rectangular glasses on it and
big blue eyes behind them; freckles and a lopsided smile below. A white sailor's shirt - the black square collar and a black
neckerchief knotted at the throat - with a black octopus (or is it a moustache?) on the chest; white trousers; big black shoes;
black wristbands. A conductor's baton in his right hand, and on his back two great black eighth notes for wings.

A rigkit rig like the Chef's: body, head (a model per expression - the face painted on), arms bent at the elbow, legs, the baton
(on his right forearm) and the two note wings (on the body). Design units: feet at y=0, facing -z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, chain

PREFIX = 'nb_'
RIG_SCALE = 0.95
PIVOT = {'body': (0, 7.4, 0), 'legr': (1.9, 7.4, 0), 'legl': (-1.9, 7.4, 0), 'head': (0, 14.6, 0),
         'armr': (4.4, 13.6, 0), 'forer': (5.2, 10.2, 0), 'arml': (-4.4, 13.6, 0), 'forel': (-5.2, 10.2, 0),
         'baton': (5.5, 7.0, -0.4), 'wingr': (1.4, 12.6, 2.3), 'wingl': (-1.4, 12.6, 2.3)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'baton': 'forer', 'wingr': 'body', 'wingl': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'shout', 'hurt', 'blink')
SKIN, SKIN_DK = '#f2b583', '#d08a5a'
HAIR = '#6a2216'
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return p == 'baton' and pose.get('_nobaton', False)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _face(kind=None):
    """the front of his head, 64 x 64, from the owner's art: a ragged fringe of red-brown hair across the brow; the white mime mask
    from brow to cheekbone, thick black glasses on it, big blue eyes behind them; below, freckles across a button nose and a
    lopsided smile, higher on his left."""
    im = _noise(SKIN, 1501, 5).resize((64, 64)); d = ImageDraw.Draw(im)
    ink, white, mask_sh = hexc('#141418'), hexc('#ffffff'), hexc('#dfe8ee')
    # the mask: wide over the brow, narrowing to the cheekbones
    d.polygon([(2, 10), (62, 10), (62, 33), (56, 40), (40, 41), (32, 38), (24, 41), (8, 40), (2, 33)], fill=white)
    d.line([(2, 33), (8, 40), (24, 41), (32, 38), (40, 41), (56, 40), (62, 33)], fill=mask_sh, width=1)
    d.line([(3, 12), (3, 32)], fill=mask_sh, width=2); d.line([(61, 12), (61, 32)], fill=mask_sh, width=2)
    # the eyes (behind the glasses): big, white with a blue iris and a dark pupil, a glint top-left
    E = ((19, 26), (45, 26))
    for cx, cy in E:
        if kind == 'happy':
            d.arc((cx - 8, cy - 3, cx + 8, cy + 9), 200, 340, fill=ink, width=3); continue
        if kind == 'blink':
            d.line((cx - 8, cy + 2, cx + 8, cy + 2), fill=ink, width=3); continue
        if kind == 'hurt':
            d.line((cx - 7, cy - 3, cx + 7, cy + 1), fill=ink, width=3) if cx < 32 else d.line((cx - 7, cy + 1, cx + 7, cy - 3), fill=ink, width=3)
            d.line((cx - 6, cy + 4, cx + 6, cy + 4), fill=ink, width=2); continue
        # (owner's note, from the art: tall solid ovals, near-black navy - a faint blue glow low in the middle, a big white
        #  shine top-left and a small white dot bottom-right; no white of the eye, the mask round them)
        rx, ry = (5, 7) if kind == 'shout' else (5, 6)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=hexc('#0b111e'))
        d.ellipse((cx - rx + 2, cy - 1, cx + rx - 2, cy + ry - 1), fill=hexc('#172a4c'))
        d.ellipse((cx - rx + 3, cy + 1, cx + rx - 3, cy + ry - 2), fill=hexc('#24426f'))
        d.ellipse((cx - 3, cy - 4, cx, cy - 1), fill=white)                                    # the big shine
        d.rectangle((cx + 1, cy + ry - 4, cx + 2, cy + ry - 3), fill=white)                      # the small dot
    # the glasses: thick black rectangular frames, the bridge, the arms off to the sides
    for x0 in (7, 34):
        d.rounded_rectangle((x0, 17, x0 + 23, 35), radius=3, outline=ink, width=3)
    d.rectangle((29, 21, 35, 24), fill=ink)
    d.rectangle((0, 19, 8, 21), fill=ink); d.rectangle((56, 19, 63, 21), fill=ink)
    # the fringe: ragged red-brown spikes over the top of the mask, a big lock over his right eye
    hair, hair_dk, hair_lt = hexc(HAIR), hexc('#3e120c'), hexc('#8e3a24')
    d.rectangle((0, 0, 63, 9), fill=hair)
    d.polygon([(0, 8), (4, 18), (9, 9), (14, 20), (20, 8), (26, 15), (30, 8)], fill=hair)
    d.polygon([(34, 8), (40, 13), (44, 8), (52, 16), (56, 8), (61, 13), (63, 8)], fill=hair)
    for x in range(1, 63, 5):
        d.line((x, 0, x + 2, 8), fill=hair_dk if x % 2 else hair_lt)
    # freckles across the nose and cheeks, the nose, the smile
    rnd = random.Random(1502)
    for cx in (16, 48):
        for _ in range(9):
            d.point((cx + rnd.randint(-6, 6), 44 + rnd.randint(-2, 3)), fill=hexc('#c8642e'))
    d.arc((27, 39, 37, 48), 20, 160, fill=hexc(SKIN_DK), width=2)                 # the button nose
    d.point((30, 46), fill=hexc('#b06a3e')); d.point((34, 46), fill=hexc('#b06a3e'))
    if kind == 'shout':
        d.ellipse((27, 50, 37, 60), fill=hexc('#5a1416'), outline=ink); d.ellipse((29, 55, 35, 59), fill=hexc('#d0484c'))
    elif kind == 'happy':
        d.chord((22, 46, 44, 60), 0, 180, fill=hexc('#5a1416'), outline=ink)
        d.rectangle((25, 53, 41, 54), fill=white); d.chord((27, 54, 39, 59), 0, 180, fill=hexc('#d0484c'))
    elif kind == 'hurt':
        d.line((24, 55, 28, 52, 32, 55, 36, 52, 40, 55), fill=ink, width=2)
    else:
        d.arc((22, 44, 46, 56), 30, 120, fill=ink, width=2)                           # the lopsided smile, up on his left
        d.line((44, 51, 46, 49), fill=ink, width=2)
    return im


def _hair(seed):
    im = _noise(HAIR, seed, 7); rnd = random.Random(seed)
    for x in range(0, 64, 2):
        for y in range(rnd.randrange(4), 64, 6):
            im.putpixel((x, y), hexc(rnd.choice(['#8e3a24', '#3e120c', '#7a2c1a'])))
    return im


def _whites(seed, base='#f6f8fa', sh='#cddbe4'):
    im = _noise(base, seed, 3); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(9):
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-8, 8), y + rnd.randint(4, 14)), fill=hexc(sh), width=2)
    return im


def _shirt_front(seed):
    """the shirt front: the black sailor collar's V from the shoulders to the knot, and the octopus - a round black head with
    two white eyes and a smile, its tentacles curling out either side like a great moustache"""
    im = _whites(seed); d = ImageDraw.Draw(im)
    ink, white = hexc('#121216'), hexc('#ffffff')
    d.polygon([(0, 0), (12, 0), (32, 22), (52, 0), (63, 0), (63, 6), (32, 30), (0, 6)], fill=ink)
    d.ellipse((21, 29, 43, 47), fill=ink)                                           # its head
    d.ellipse((25, 34, 29, 39), fill=white); d.ellipse((35, 34, 39, 39), fill=white)
    d.arc((27, 37, 37, 44), 20, 160, fill=white, width=2)
    for sx in (-1, 1):                                                              # the tentacles, curled up at the tips
        pts = [(32 + sx * 7, 46), (32 + sx * 14, 50), (32 + sx * 22, 50), (32 + sx * 27, 45), (32 + sx * 25, 41)]
        d.line(pts, fill=ink, width=5, joint='curve')
        pts2 = [(32 + sx * 4, 49), (32 + sx * 10, 57), (32 + sx * 19, 59), (32 + sx * 25, 56)]
        d.line(pts2, fill=ink, width=5, joint='curve')
    d.line((0, 63, 63, 63), fill=hexc('#9fb0bc'), width=2)
    return im


def _collar(seed):
    im = _noise('#121216', seed, 3); d = ImageDraw.Draw(im)
    for i in (5, 58):
        d.rectangle((i, 0, i + 1, 63), fill=hexc('#ffffff'))                        # the white piping
        d.rectangle((0, i, 63, i + 1), fill=hexc('#ffffff'))
    return im


def _band(seed):
    im = _shine('#141416', '#3c3c44', seed)
    return im


def textures():
    T = {'nb_skin': _noise(SKIN, 1503, 6), 'nb_skin_dk': _noise(SKIN_DK, 1504, 5), 'nb_white': _whites(1505), 'nb_white_dk': _whites(1506, '#d8e2ea', '#aebfcc'),
         'nb_shirt': _shirt_front(1507), 'nb_collar': _collar(1508), 'nb_black': _shine('#151518', '#40404a', 1509), 'nb_shoe': _shine('#16161a', '#4a4a54', 1510),
         'nb_band': _band(1511), 'nb_beret': _shine('#1a1a1e', '#46464e', 1512), 'nb_button': _shine('#d07a3a', '#ffc080', 1513),
         'nb_hair': _hair(1514), 'nb_note': _shine('#0e0e10', '#3a3a42', 1515), 'nb_baton': _shine('#1c1c20', '#5a5a64', 1516),
         'nb_tip': _noise('#e8e8ee', 1517, 3), 'nb_face': _face()}
    for k in FACES:
        T[f'nb_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the white sailor shirt (the octopus on its front), the square black collar on his back, the knot and its tails
    pv = PIVOT['body']
    body = [el((-3.6, 6.8, -2.1), (3.6, 7.8, 2.1), 'nb_white_dk', pv),                       # the waistband
            el((-3.8, 7.6, -2.3), (3.8, 14.4, 2.3), 'nb_white', pv, shift=(0.2, 0.4)),
            el((-3.8, 7.6, -2.32), (3.8, 14.4, -2.3), 'nb_shirt', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
            el((-3.85, 7.5, -2.4), (3.85, 7.9, 2.4), 'nb_white_dk', pv),                      # the hem
            el((-3.9, 10.6, 2.3), (3.9, 14.5, 2.55), 'nb_collar', pv, uv={'south': [0, 0, 16, 16]}),   # the square collar on his back
            el((-3.9, 14.2, -2.4), (-2.0, 14.55, 2.5), 'nb_collar', pv), el((2.0, 14.2, -2.4), (3.9, 14.55, 2.5), 'nb_collar', pv),
            el((-0.7, 12.4, -2.85), (0.7, 13.6, -2.3), 'nb_black', pv),                       # the neckerchief's knot ...
            el((-0.9, 11.5, -2.6), (-0.2, 12.5, -2.35), 'nb_black', pv, shift=(0.2, 0.3)),   # ... and its tails
            el((0.15, 11.2, -2.6), (0.85, 12.5, -2.35), 'nb_black', pv, shift=(0.7, 0.3))]
    part('nb_body', body)

    # ---- the head: big, the face painted (a head per expression); the spiky hair, the ears; the beret slumped to his right
    pv = PIVOT['head']
    HW, HT, HZ = 3.7, 24.6, 3.6                    # (2.86 owner's note: a taller, slimmer head than the first draft's 8.8 x 8.4)
    def head(face=None):
        tex = 'nb_face' if face is None else f'nb_face_{face}'
        h = [el((-1.3, 14.2, -1.2), (1.3, 15.2, 1.2), 'nb_skin_dk', pv),                       # the neck
             el((-HW, 15.0, -HZ), (HW, HT, HZ - 0.2), 'nb_skin', pv, shift=(0.3, 0.2)),
             el((-HW, 15.0, -HZ - 0.02), (HW, HT, -HZ), tex, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
             el((-HW - 0.6, 18.2, -0.6), (-HW + 0.05, 20.6, 0.8), 'nb_skin', pv), el((HW - 0.05, 18.2, -0.6), (HW + 0.6, 20.6, 0.8), 'nb_skin', pv)]
        # the hair: thick at the back and sides, the mask's band hidden under it; spikes sticking out over the ears and behind
        h += [el((-HW - 0.2, 16.4, 0.6), (HW + 0.2, HT + 0.2, HZ + 0.3), 'nb_hair', pv, shift=(0.2, 0.3)),
              el((-HW - 0.25, 19.4, -HZ + 0.2), (-HW + 0.05, HT + 0.2, 0.8), 'nb_hair', pv), el((HW - 0.05, 19.4, -HZ + 0.2), (HW + 0.25, HT + 0.2, 0.8), 'nb_hair', pv),
              el((-HW - 0.2, HT - 1.8, -HZ - 0.25), (HW + 0.2, HT + 0.2, -HZ + 0.1), 'nb_hair', pv, shift=(0.6, 0.1))]      # the fringe, standing proud
        for sx in (-1, 1):                                                                    # spikes over the ears, swept back
            h += chain([(sx * (HW + 0.1), 21.8, -1.4), (sx * (HW + 1.4), 20.6, 0.2), (sx * (HW + 2.1), 19.4, 1.6)], [1.6, 0.25], 0.9, 'nb_hair', pv, UP, ext=0.1)
            h += chain([(sx * HW, 19.0, 0.6), (sx * (HW + 1.2), 17.8, 2.0), (sx * (HW + 1.6), 16.8, 3.2)], [1.2, 0.2], 0.8, 'nb_hair', pv, UP, ext=0.1)
        for x in (-2.2, 0.2, 2.4):                                                            # and out the back
            h += chain([(x, 20.0, HZ + 0.1), (x * 1.1, 19.2, HZ + 1.4), (x * 1.2, 18.2, HZ + 2.2)], [1.6, 0.25], 1.0, 'nb_hair', pv, UP, ext=0.1)
        for x, top in ((-2.9, HT - 2.4), (-1.0, HT - 2.8), (1.2, HT - 2.2), (3.0, HT - 2.6)):    # the fringe's spikes over the mask
            h.append(el((x - 0.7, top, -HZ - 0.3), (x + 0.7, HT - 1.4, -HZ), 'nb_hair', pv, shift=(x * 0.1, 0.4)))
        # the beret: a soft black disc, wider than his head, slumped down over his right ear; the orange button on its crown
        bt = HT - 0.4
        h += [el((-HW - 0.4, bt, -HZ - 0.4), (HW + 0.4, bt + 1.2, HZ + 0.4), 'nb_beret', pv),
              el((-HW, bt + 0.6, -HZ - 1.4), (HW + 2.2, bt + 2.0, HZ + 0.8), 'nb_beret', pv, rot=('z', -22.5, (0.0, bt + 1.0, 0.0)), shift=(0.3, 0.2)),
              el((-HW + 0.8, bt + 1.8, -HZ - 0.6), (HW + 1.0, bt + 2.8, HZ - 0.2), 'nb_beret', pv, rot=('z', -22.5, (0.0, bt + 1.0, 0.0)), shift=(0.6, 0.5)),
              el((-0.6, bt + 2.7, -1.0), (0.6, bt + 3.5, 0.2), 'nb_button', pv, rot=('z', -22.5, (0.0, bt + 1.0, 0.0)))]
        return h
    part('nb_head', head())
    for fc in FACES:
        part(f'nb_head_x{fc}', head(fc))

    # ---- the arms: short white sleeves, bare arms, black wristbands, big hands
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        a = [el((x0 - 1.5, y0 - 2.6, -1.6), (x0 + 1.5, y0 + 1.0, 1.6), 'nb_white', pv, shift=(0.4, 0.2)),        # the sleeve
             el((x0 - 1.55, y0 - 2.7, -1.65), (x0 + 1.55, y0 - 2.3, 1.65), 'nb_white_dk', pv)]
        a += chain([(x0, y0 - 2.4, 0), (sx * 5.2, 10.2, 0)], [2.2], 2.2, 'nb_skin', pv, FRONT, ext=0.3)
        return a
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 5.5, 7.8
        a = chain([(ex, ey, 0), (wx, wy, 0)], [2.1], 2.1, 'nb_skin', pv, FRONT, ext=0.25)
        a += [el((wx - 1.2, wy + 0.2, -1.2), (wx + 1.2, wy + 1.3, 1.2), 'nb_band', pv),          # the wristband
              el((wx - 1.3, wy - 1.9, -1.3), (wx + 1.3, wy + 0.3, 1.2), 'nb_skin', pv),         # the hand: big, as drawn
              el((wx - 1.0, wy - 2.2, -1.45), (wx + 1.0, wy - 1.5, -0.9), 'nb_skin_dk', pv)]
        return a
    part('nb_armr', upper(1)); part('nb_arml', upper(-1)); part('nb_forer', lower(1)); part('nb_forel', lower(-1))

    # ---- the legs: loose white trousers, big black shoes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 1.75, 1.6, -1.7), (cx + 1.75, 7.6, 1.7), 'nb_white', pv, shift=(0.3 if sx > 0 else 0.6, 0.2)),
                el((cx - 1.8, 1.4, -1.75), (cx + 1.8, 2.0, 1.75), 'nb_white_dk', pv),
                el((cx - 1.9, 0.0, -2.6), (cx + 1.9, 1.8, 2.0), 'nb_shoe', pv),
                el((cx - 1.7, 0.0, -3.4), (cx + 1.7, 1.4, -2.5), 'nb_shoe', pv, shift=(0.5, 0.5))]
    part('nb_legr', leg(1)); part('nb_legl', leg(-1))

    # ---- the baton: thin and black, out ahead of his fist, a pale tip
    pv = PIVOT['baton']; x = 5.5
    part('nb_baton', [el((x - 0.4, 6.0, -1.0), (x + 0.4, 7.4, -0.2), 'nb_baton', pv),
                      el((x - 0.17, 6.55, -7.2), (x + 0.17, 6.89, -1.0), 'nb_baton', pv),
                      el((x - 0.12, 6.6, -8.0), (x + 0.12, 6.84, -7.2), 'nb_tip', pv)])

    # ---- the wings: a great black eighth note on each side - the beam out from his shoulder blade, the stem down at its tip,
    #      the round note head at its foot (turned in), a little flag at the very end of the beam
    def wing(sx):
        pv = PIVOT['wingr' if sx > 0 else 'wingl']
        w = [el((sx * 1.0 - 0.6, 11.8, 2.3), (sx * 1.0 + 0.6, 13.4, 2.9), 'nb_note', pv)]       # the root on his back
        w += chain([(sx * 1.2, 12.8, 2.6), (sx * 7.0, 14.4, 3.0), (sx * 12.4, 15.8, 3.3)], [1.3, 1.1], 0.5, 'nb_note', pv, FRONT, ext=0.2)
        w += chain([(sx * 11.9, 15.6, 3.3), (sx * 11.9, 9.6, 3.3)], [0.7], 0.5, 'nb_note', pv, FRONT, ext=0.1)   # the stem
        hx = sx * 11.9
        lo, hi = (hx - 2.9, hx + 0.35) if sx > 0 else (hx - 0.35, hx + 2.9)
        w += [el((lo, 8.2, 2.95), (hi, 10.2, 3.65), 'nb_note', pv),                             # the note head, an oval
              el((lo + 0.4, 7.8, 3.0), (hi - 0.4, 10.6, 3.6), 'nb_note', pv, shift=(0.5, 0.5))]
        fx = sx * 12.4
        w += chain([(fx, 15.8, 3.3), (fx + sx * 0.8, 14.6, 3.3), (fx + sx * 0.6, 13.6, 3.3)], [0.8, 0.5], 0.45, 'nb_note', pv, FRONT, ext=0.1)
        return w
    part('nb_wingr', wing(1)); part('nb_wingl', wing(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def flap(sx, up=0.0, back=0.0):
    """a wing: raised (up) about his spine and swept back (back)"""
    return qs(('y', back * sx), ('z', -up * sx))


def P(**kw):
    return kw


WINGS = dict(wingr=flap(1, 0, 10), wingl=flap(-1, 0, 10))
IDLE = dict(WINGS, armr=limb(1, 30, 8), forer=limb(1, 40), arml=limb(-1, -4, 8), forel=limb(-1, 14), head=qs(('y', -6)))
POSES = {
    # idle: humming along, the baton keeping time; the wings drift
    'idle_a': P(**IDLE),
    'idle_b': P(_off=(0, -0.12, 0), **dict(IDLE, armr=limb(1, 40, 14), forer=limb(1, 30), head=qs(('y', 6), ('z', 4)),
                                           wingr=flap(1, 6, 6), wingl=flap(-1, 6, 6))),
    # walk: a jaunty bounce, the baton swinging like a metronome
    'walk_a': P(_off=(0, 0.2, 0), legr=limb(1, 28), legl=limb(-1, -26), armr=limb(1, 10, 8), arml=limb(-1, 24, 8),
                forer=limb(1, 30), forel=limb(-1, 20), head=qs(('z', -4)), **dict(WINGS, wingr=flap(1, -4, 14), wingl=flap(-1, -4, 14))),
    'walk_up': P(_off=(0, 0.55, 0), legr=limb(1, 4), legl=limb(-1, -4), armr=limb(1, 24, 8), arml=limb(-1, 4, 8), forer=limb(1, 34), forel=limb(-1, 16),
                 **dict(WINGS, wingr=flap(1, 8, 10), wingl=flap(-1, 8, 10))),
    'walk_b': P(_off=(0, 0.2, 0), legr=limb(1, -26), legl=limb(-1, 28), armr=limb(1, 40, 8), arml=limb(-1, -20, 8),
                forer=limb(1, 40), forel=limb(-1, 14), head=qs(('z', 4)), **dict(WINGS, wingr=flap(1, -4, 14), wingl=flap(-1, -4, 14))),
    'run_a': P(_off=(0, 0.4, 0), body=qs(('x', 12)), head=qs(('x', -10)), legr=limb(1, 46), legl=limb(-1, -40), armr=limb(1, -30, 12), arml=limb(-1, 40, 12),
               forer=limb(1, 50), forel=limb(-1, 50), wingr=flap(1, 14, 26), wingl=flap(-1, 14, 26)),
    'run_up': P(_off=(0, 1.0, 0), body=qs(('x', 12)), head=qs(('x', -10)), legr=limb(1, 14), legl=limb(-1, -20), armr=limb(1, 6, 14), arml=limb(-1, 6, 14),
                forer=limb(1, 60), forel=limb(-1, 60), wingr=flap(1, -10, 30), wingl=flap(-1, -10, 30)),
    'run_b': P(_off=(0, 0.4, 0), body=qs(('x', 12)), head=qs(('x', -10)), legr=limb(1, -40), legl=limb(-1, 46), armr=limb(1, 40, 12), arml=limb(-1, -30, 12),
               forer=limb(1, 50), forel=limb(-1, 50), wingr=flap(1, 14, 26), wingl=flap(-1, 14, 26)),
    'jump': P(_face='happy', _off=(0, 1.4, 0), legr=limb(1, 40), legl=limb(-1, 10), armr=limb(1, 130, 30), forer=limb(1, 20), arml=limb(-1, 110, 40), forel=limb(-1, 20),
              wingr=flap(1, 30, 0), wingl=flap(-1, 30, 0)),
    # conducting (his healing song): the baton up and across, then down - the left hand shaping the phrase
    'conduct_a': P(_face='happy', body=qs(('y', -8)), head=qs(('x', -8), ('y', 6)), armr=limb(1, 120, 20), forer=limb(1, 30), arml=limb(-1, 60, 30), forel=limb(-1, 40),
                   wingr=flap(1, 16, 4), wingl=flap(-1, 16, 4)),
    'conduct_b': P(_face='happy', _off=(0, -0.2, 0), body=qs(('y', 8)), head=qs(('x', 4), ('y', -6)), armr=limb(1, 60, -6), forer=limb(1, 50), arml=limb(-1, 70, 10),
                   forel=limb(-1, 20), wingr=flap(1, -6, 12), wingl=flap(-1, -6, 12)),
    # a sharp note (his attack): the baton drawn back, then a hard downbeat flung at the foe
    'strike_up': P(_face='shout', body=qs(('y', -16), ('x', -4)), armr=limb(1, 150, 30), forer=limb(1, 20), arml=limb(-1, 10, 24), forel=limb(-1, 30),
                   wingr=flap(1, 24, 0), wingl=flap(-1, 24, 0)),
    'strike': P(_face='shout', _off=(0, -0.3, 0), body=qs(('y', 14), ('x', 12)), head=qs(('x', -8)), armr=limb(1, 80, -4), forer=limb(1, 0), arml=limb(-1, -20, 24),
                forel=limb(-1, 20), wingr=flap(1, -14, 20), wingl=flap(-1, -14, 20)),
    # the Crescendo (his great move): both arms flung high, wings spread wide, head back
    'crescendo': P(_face='shout', _off=(0, 0.8, 0), body=qs(('x', -10)), head=qs(('x', -18)), armr=limb(1, 160, 30), forer=limb(1, 10), arml=limb(-1, 160, 30),
                   forel=limb(-1, 10), wingr=flap(1, 30, -8), wingl=flap(-1, 30, -8)),
    # a bow for the audience
    'bow': P(_face='happy', body=qs(('x', 34)), head=qs(('x', 10)), armr=limb(1, -10, -40), forer=limb(1, 60), arml=limb(-1, 0, 50), forel=limb(-1, 10),
             legr=limb(1, -30), legl=limb(-1, -30), wingr=flap(1, 10, 20), wingl=flap(-1, 10, 20)),
    'wave_a': P(_face='happy', **dict(IDLE, arml=limb(-1, 10, 130), forel=limb(-1, 40), head=qs(('y', 8)))),
    'sit_a': P(_off=(0, -4.6, 0), legr=limb(1, 84, 8), legl=limb(-1, 84, 8), armr=limb(1, 30, 10), forer=limb(1, 50), arml=limb(-1, 24, 10),
               forel=limb(-1, 54), head=qs(('y', -8)), wingr=flap(1, -16, 16), wingl=flap(-1, -16, 16)),
    'sit_b': P(_face='blink', _off=(0, -4.7, 0), body=qs(('x', 4)), legr=limb(1, 80, 8), legl=limb(-1, 86, 8), armr=limb(1, 40, 16), forer=limb(1, 40),
               arml=limb(-1, 26, 10), forel=limb(-1, 56), head=qs(('x', 10), ('z', 8)), wingr=flap(1, -10, 12), wingl=flap(-1, -10, 12)),
    'hurt': P(_face='hurt', body=qs(('x', -8)), head=qs(('x', -12)), armr=limb(1, 30, 30), forer=limb(1, 60), arml=limb(-1, 30, 30), forel=limb(-1, 60),
              wingr=flap(1, 24, -6), wingl=flap(-1, 24, -6)),
    'tired': P(_face='hurt', _off=(0, -0.8, 0), body=qs(('x', 14), ('z', -4)), head=qs(('x', 16)), armr=limb(1, 0, 6), arml=limb(-1, 0, 6),
               forer=limb(1, 6), forel=limb(-1, 6), legr=limb(1, 6, 4), legl=limb(-1, -4, 4), wingr=flap(1, -30, 20), wingl=flap(-1, -30, 20)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (a breaststroke, the wings sculling)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='shout', _off=(0, -5.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 24)), head=qs(('x', -24)),
                            armr=limb(1, 100 + 30 * math.sin(_p), 30), forer=limb(1, 30 + 20 * math.cos(_p)),
                            arml=limb(-1, 100 + 30 * math.sin(_p), 30), forel=limb(-1, 30 + 20 * math.cos(_p)),
                            legr=limb(1, -10 + 22 * math.sin(2 * _p)), legl=limb(-1, -10 - 22 * math.sin(2 * _p)),
                            wingr=flap(1, 10 * math.sin(_p), 30), wingl=flap(-1, 10 * math.sin(_p), 30))
DRAFT = ['idle_a', 'walk_a', 'run_a', 'jump', 'conduct_a', 'conduct_b', 'strike_up', 'strike', 'crescendo', 'bow', 'sit_a', 'hurt', 'tired']
