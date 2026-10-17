"""Fishy (draft, for approval - not in the pack yet): a gentleman goldfish in a top hat and monocle, swimming about inside a fishbowl
that walks on long robot legs and waves its jointed robot arms. From the owner's art: the round bowl with its lip and a metal
collar under it, sand on the bottom, a ribbon of seaweed on his right and a little blue castle on his left, bubbles rising;
grey-steel limbs banded at the joints, three-clawed hands, big rounded boots.

The fish is a part of his own (he swims laps round the bowl, bobs, bows and tips his hat while the bowl walks); the seaweed is
one too (it sways). The arms bend at the elbow (an upper and a lower part each). A rigkit rig, like Tullius and Apophiss.
Design units: feet at y=0, facing -z, his right is +x. The glass is translucent; everything inside shows through it."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, seg, chain, I

PREFIX = 'fy_'
RIG_SCALE = 1.0
BOWL_LO, BOWL_HI = 13.6, 27.0                  # (2.80d: a square glass tank - no longer a round bowl built of turned slabs)
TANK_W = 6.4                                   # (its half-width)
WATER = 25.0                                   # (2.82: the water line - the tank is full, a hand's breadth from the rim)
PIVOT = {'body': (0, 12.2, 0), 'legr': (3.4, 12.2, 0), 'legl': (-3.4, 12.2, 0),
         'armr': (8.2, 20.4, 0), 'forer': (9.9, 15.4, 0), 'arml': (-8.2, 20.4, 0), 'forel': (-9.9, 15.4, 0),
         'fish': (0, 20.0, 0.0), 'weed': (3.3, 15.6, 0.6)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml', 'fish': 'body', 'weed': 'body'}
PARTS = tuple(PIVOT)
PART_K = {'fish': 1.5}                      # (the fish built small, shown half as big again - as big in his bowl as in the art)
FACES = ('blink', 'happy', 'shock', 'squint')
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'fish' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _glass(seed, alpha=40, streak=150):
    im = Image.new('RGBA', (16, 16), (176, 218, 242, alpha)); px = im.load(); rnd = random.Random(seed)
    for x in range(16):
        for y in range(16):
            r, g, b, a = px[x, y]; v = rnd.randint(-6, 6)
            px[x, y] = (min(255, r + v), min(255, g + v), min(255, b + v), a)
    for y in range(3, 12):                                  # (a soft glint down one side, like the art's highlights; 2.82: fainter, no lone dots)
        px[4, y] = (236, 248, 255, streak // 2)
    return im


def _rim(seed):
    im = Image.new('RGBA', (16, 16), (196, 226, 244, 160)); px = im.load(); rnd = random.Random(seed)   # (2.82: even - no white row for thin faces to catch)
    for x in range(16):
        for y in range(16):
            v = rnd.randint(-5, 5); r, g, b, a = px[x, y]; px[x, y] = (r + v, g + v, min(255, b + v), a)
    return im


def _water(seed, alpha=44):
    """(2.82) the water in his tank: a clear blue, faint light ripples"""
    im = Image.new('RGBA', (16, 16), (70, 150, 214, alpha)); px = im.load(); rnd = random.Random(seed)
    for x in range(16):
        for y in range(16):
            v = rnd.randint(-6, 6); r, g, b, a = px[x, y]; px[x, y] = (r + v, g + v, min(255, b + v), a)
    for _ in range(4):
        x, y = rnd.randrange(1, 14), rnd.randrange(16)
        for k in range(3):
            px[x + k, y] = (150, 210, 240, alpha + 16)
    return im


def _surface(seed):
    """the water's top: lighter, with ripple rings"""
    im = _water(seed, 64); d = ImageDraw.Draw(im)
    d.arc((2, 2, 9, 7), 0, 360, fill=(190, 230, 250, 110)); d.arc((8, 8, 14, 13), 0, 360, fill=(190, 230, 250, 96))
    return im


def _sand(seed):
    im = _noise('#e4d6bb', seed, 7); px = im.load(); rnd = random.Random(seed)
    for _ in range(26):
        x, y = rnd.randrange(16), rnd.randrange(16); px[x, y] = hexc(rnd.choice(['#c9b896', '#f4ead6', '#b8a684']))
    return im


def _weed(seed):
    im = _noise('#3f8a3e', seed, 6); d = ImageDraw.Draw(im)
    d.line((7, 0, 7, 15), fill=hexc('#2a6a2c')); d.line((4, 0, 4, 15), fill=hexc('#5aa95a')); d.line((11, 0, 11, 15), fill=hexc('#5aa95a'))
    return im


def _stone(seed):
    im = _noise('#8a94bc', seed, 6); d = ImageDraw.Draw(im)
    for y in (3, 7, 11, 15):
        d.line((0, y, 15, y), fill=hexc('#6c76a2'))
    for i, y in enumerate((0, 4, 8, 12)):
        for x in ((3, 11) if i % 2 else (7, 15)):
            d.line((x, y, x, y + 2), fill=hexc('#6c76a2'))
    return im


def _roof(seed):
    im = _noise('#4f7299', seed, 6); d = ImageDraw.Draw(im)
    for y in (2, 6, 10, 14):
        d.line((0, y, 15, y), fill=hexc('#3b5a7e'))
    return im


def _scales(seed, base='#f6a11e', hi='#ffd048', dk='#e0841a'):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im)
    for row, y in enumerate(range(1, 16, 3)):
        for x in range(-2 + (row % 2) * 2, 16, 4):
            d.arc((x, y - 1, x + 4, y + 3), 0, 180, fill=hexc(hi))
    d.line((0, 15, 15, 15), fill=hexc(dk))
    return im


def _fin(seed):
    im = _noise('#f39220', seed, 5); d = ImageDraw.Draw(im)
    for x in range(1, 16, 3):
        d.line((x, 0, x + 2, 15), fill=hexc('#ffd060'))
    return im


def _eye(seed, look=0, shut=False, happy=False, wide=False):
    """an eye: white with a black pupil; shut (a line), happy (an arch), wide (a small pupil)"""
    im = Image.new('RGBA', (16, 16), hexc('#fbfbf6')); d = ImageDraw.Draw(im)
    if shut:
        im = Image.new('RGBA', (16, 16), hexc('#f6a11e')); d = ImageDraw.Draw(im); d.rectangle((1, 7, 14, 9), fill=hexc('#2a1606')); return im
    if happy:
        im = Image.new('RGBA', (16, 16), hexc('#f6a11e')); d = ImageDraw.Draw(im); d.arc((2, 5, 13, 16), 200, 340, fill=hexc('#2a1606'), width=3); return im
    r = 2 if wide else 4
    d.ellipse((8 - r + look, 8 - r, 8 + r + look, 8 + r), fill=hexc('#121212'))
    d.rectangle((9 + look, 5, 10 + look, 6), fill=hexc('#ffffff'))
    return im


def textures():
    T = {'fy_glass': _glass(901), 'fy_glass_b': _glass(902, 30, 90), 'fy_rim': _rim(903), 'fy_water': _water(929), 'fy_water_top': _surface(930), 'fy_bubble': _glass(904, 120, 220),
         'fy_metal': _shine('#6f8c9c', '#a8c4d0', 905), 'fy_band': _shine('#8db2be', '#c8e2ea', 906), 'fy_dark': _shine('#3d5464', '#6f8c9c', 907),
         'fy_joint': _shine('#9cc2ce', '#e0f2f6', 908), 'fy_sand': _sand(909), 'fy_weed': _weed(910), 'fy_stone': _stone(911), 'fy_roof': _roof(912),
         'fy_door': _noise('#4a3f72', 913, 4), 'fy_fish': _scales(914), 'fy_belly': _scales(915, '#ffc04c', '#ffe08a', '#f0a030'), 'fy_fin': _fin(916),
         'fy_eye': _eye(917), 'fy_eye_l': _eye(918, look=-1), 'fy_eye_shut': _eye(919, shut=True), 'fy_eye_happy': _eye(920, happy=True),
         'fy_eye_wide': _eye(921, wide=True), 'fy_pupil': _noise('#121212', 922, 2), 'fy_gold': _shine('#e2b42c', '#fff0a0', 923),
         'fy_lens': _glass(924, 90, 200), 'fy_hat': _shine('#1c1c22', '#46464e', 925), 'fy_hatband': _noise('#c6435a', 926, 6),
         'fy_stache': _noise('#9a4c12', 927, 6), 'fy_mouth': _noise('#5a2a08', 928, 3)}
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the tank (body), 2.80d: square and blocky, as Minecraft builds things - a stepped metal collar and its mount; the
    #      sand, the castle, the bubbles; then the glass round it all, one pane a side (each a thin pane with only its two broad
    #      faces, so no inner edges show through the glass), a frame of rim along the top and a band along the bottom
    pv = PIVOT['body']
    body = []
    def slab(y0, y1, a, tex, sh=(0, 0)):
        return el((-a, y0, -a), (a, y1, a), tex, pv, shift=sh)
    body += [slab(11.4, 12.4, 3.2, 'fy_dark'), slab(12.4, 13.6, 4.6, 'fy_metal'), slab(13.6, 14.1, TANK_W + 0.3, 'fy_band', (0.4, 0.2))]
    body += [slab(14.1, 15.6, TANK_W - 0.1, 'fy_sand'), el((-3.0, 15.6, -3.0), (3.0, 16.2, 2.0), 'fy_sand', pv, shift=(0.5, 0.5))]   # (a low mound)
    # the castle (his left, toward the back): a stone tower, a stepped slate roof, an arched dark door
    cx, cz = -3.3, 1.4
    body += [el((cx - 1.3, 15.6, cz - 1.3), (cx + 1.3, 19.6, cz + 1.3), 'fy_stone', pv),
             el((cx - 1.55, 19.6, cz - 1.55), (cx + 1.55, 20.1, cz + 1.55), 'fy_stone', pv, shift=(0.3, 0.6))]
    for i, (y0, h) in enumerate(((20.1, 1.6), (21.0, 1.1), (21.9, 0.6))):
        body.append(el((cx - h, y0, cz - h), (cx + h, y0 + 0.9, cz + h), 'fy_roof', pv, shift=(0.2 * i, 0.3 * i)))
    body += [el((cx - 0.55, 15.6, cz - 1.36), (cx + 0.55, 17.6, cz - 1.31), 'fy_door', pv), el((cx - 0.35, 17.6, cz - 1.36), (cx + 0.35, 17.95, cz - 1.31), 'fy_door', pv)]
    # bubbles rising on his right, in front of the fish
    for (x, y, sz) in ((1.9, 21.4, 0.55), (2.5, 22.7, 0.7), (1.7, 23.9, 0.45)):
        body.append(el((x - sz / 2, y - sz / 2, -1.6 - sz / 2), (x + sz / 2, y + sz / 2, -1.6 + sz / 2), 'fy_bubble', pv))
    # the glass: four panes (front and back span the width, the sides fit between them)
    W = TANK_W
    body += [el((-W, BOWL_LO, -W - 0.12), (W, BOWL_HI, -W), 'fy_glass', pv, faces=('north', 'south')),
             el((-W, BOWL_LO, W), (W, BOWL_HI, W + 0.12), 'fy_glass_b', pv, faces=('north', 'south'), shift=(0.4, 0.2)),
             el((W, BOWL_LO, -W), (W + 0.12, BOWL_HI, W), 'fy_glass_b', pv, faces=('east', 'west'), shift=(0.2, 0.5)),
             el((-W - 0.12, BOWL_LO, -W), (-W, BOWL_HI, W), 'fy_glass', pv, faces=('east', 'west'), shift=(0.6, 0.1))]
    # (2.82) the water: a blue sheet just inside each pane up to the water line, and its rippled surface (seen from above
    #  and from below), so the tank reads as full - the fish swims in it, his hat just breaking the surface
    w = W - 0.06
    body += [el((-w, 15.6, -w), (w, WATER, -w + 0.02), 'fy_water', pv, faces=('north', 'south')),
             el((-w, 15.6, w - 0.02), (w, WATER, w), 'fy_water', pv, faces=('north', 'south'), shift=(0.5, 0.3)),
             el((w - 0.02, 15.6, -w), (w, WATER, w), 'fy_water', pv, faces=('east', 'west'), shift=(0.3, 0.6)),
             el((-w, 15.6, -w), (-w + 0.02, WATER, w), 'fy_water', pv, faces=('east', 'west'), shift=(0.7, 0.2)),
             el((-w, WATER - 0.02, -w), (w, WATER, w), 'fy_water_top', pv, faces=('up', 'down'))]
    # the rim: a square frame round the opening; the band round the glass floor
    for (y0, y1, t, o) in ((BOWL_HI - 0.2, BOWL_HI + 0.5, 'fy_rim', 0.45), (BOWL_LO - 0.1, BOWL_LO + 0.3, 'fy_band', 0.25)):
        body += [el((-W - o, y0, -W - o), (W + o, y1, -W + 0.1), t, pv), el((-W - o, y0, W - 0.1), (W + o, y1, W + o), t, pv),
                 el((-W - o, y0, -W + 0.1), (-W + 0.1, y1, W - 0.1), t, pv), el((W - 0.1, y0, -W + 0.1), (W + o, y1, W - 0.1), t, pv)]
    part('fy_body', body)

    # ---- the seaweed: two ribbons waving up from the sand
    pv = PIVOT['weed']
    weed = chain([(3.3, 15.6, 0.6), (3.9, 17.6, 0.5), (3.1, 19.8, 0.7), (3.9, 22.0, 0.6), (3.4, 23.6, 0.6)], (1.0, 0.6), 0.25, 'fy_weed', pv, FRONT)
    weed += chain([(2.6, 15.6, 1.2), (2.1, 17.4, 1.3), (2.7, 19.2, 1.2), (2.2, 20.6, 1.3)], (0.85, 0.5), 0.25, 'fy_weed', pv, FRONT)
    part('fy_weed', weed)

    # ---- the fish: a round orange body facing you, a lighter belly, a fan of a tail swept round to his left, a side fin; big
    #      eyes, a gold monocle on his right one (its chain looping down), a curled moustache; the top hat with its red band
    pv = PIVOT['fish']; fx, fy, fz = pv
    E = lambda fr, to, t, rot=None, sh=None, faces=None: el(fr, to, t, pv, rot, shift=sh, faces=faces)
    def fish(face=None):
        f = [E((fx - 1.6, fy - 1.5, fz - 1.1), (fx + 1.6, fy + 1.4, fz + 1.1), 'fy_fish'),               # (2.80d: one block of a fish)
             E((fx - 1.0, fy - 1.4, fz - 1.18), (fx + 1.0, fy - 0.45, fz - 1.1), 'fy_belly', faces=('north',))]
        # the tail: swept back and round to his left, a forked fan
        # (2.82: tucked in closer - the old fan reached out through the glass as he swam his laps)
        f += chain([(fx - 1.2, fy - 0.2, fz + 0.6), (fx - 1.9, fy - 0.4, fz + 1.0), (fx - 2.3, fy - 0.3, fz + 1.1)], (1.1, 0.8), 0.65, 'fy_fish', pv, UP)
        f += [seg((fx - 2.2, fy - 0.3, fz + 1.1), (fx - 3.0, fy + 1.1, fz + 1.0), 0.9, 0.25, 'fy_fin', pv, FRONT),
              seg((fx - 2.2, fy - 0.3, fz + 1.1), (fx - 2.9, fy - 1.5, fz + 0.9), 0.9, 0.25, 'fy_fin', pv, FRONT),
              seg((fx + 1.3, fy - 0.6, fz - 0.6), (fx + 2.0, fy - 1.2, fz - 0.8), 0.8, 0.2, 'fy_fin', pv, FRONT),               # his right fin
              seg((fx - 1.3, fy - 0.6, fz - 0.4), (fx - 2.1, fy - 1.2, fz - 0.2), 0.7, 0.2, 'fy_fin', pv, FRONT),
              seg((fx - 0.2, fy + 1.4, fz + 0.4), (fx - 0.6, fy + 1.9, fz + 1.2), 0.25, 0.7, 'fy_fin', pv, SIDE)]                # the dorsal fin, behind the hat
        # eyes: a little apart, high on the face
        tex = {None: ('fy_eye', 'fy_eye'), 'blink': ('fy_eye_shut', 'fy_eye_shut'), 'happy': ('fy_eye_happy', 'fy_eye_happy'),
               'shock': ('fy_eye_wide', 'fy_eye_wide'), 'squint': ('fy_eye_shut', 'fy_eye_l')}[face]
        for sx, t in ((1, tex[0]), (-1, tex[1])):
            f.append(E((fx + sx * 0.25 - 0.45 + sx * 0.3, fy + 0.15, fz - 1.24), (fx + sx * 0.25 + 0.45 + sx * 0.3, fy + 1.05, fz - 1.12), t, faces=('north',)))
        # the monocle, on his right eye (popped off and swinging on its chain when he's shocked)
        mx, my, mz = fx + 0.85, fy + 0.6, fz - 1.3
        if face == 'shock':
            mx, my = fx + 1.25, fy - 0.9
        ring = [((mx - 0.6, my - 0.6), (mx + 0.6, my - 0.45)), ((mx - 0.6, my + 0.45), (mx + 0.6, my + 0.6)),
                ((mx - 0.6, my - 0.45), (mx - 0.45, my + 0.45)), ((mx + 0.45, my - 0.45), (mx + 0.6, my + 0.45))]
        f += [E((a[0], a[1], mz - 0.08), (b[0], b[1], mz + 0.04), 'fy_gold') for a, b in ring]
        f.append(E((mx - 0.45, my - 0.45, mz - 0.04), (mx + 0.45, my + 0.45, mz), 'fy_lens', faces=('north',)))
        f += chain([(mx + 0.5, my - 0.5, mz), (fx + 1.25, fy - 1.0, fz - 1.15), (fx + 0.9, fy - 1.5, fz - 1.15)], [0.12, 0.12], 0.08, 'fy_gold', pv, FRONT, ext=0.04)
        # the moustache: two curls under his eyes, and a small mouth
        if face != 'shock':
            for sx in (1, -1):
                f += chain([(fx + sx * 0.1, fy - 0.15, fz - 1.24), (fx + sx * 0.55, fy - 0.35, fz - 1.27), (fx + sx * 0.85, fy - 0.15, fz - 1.27),
                            (fx + sx * 0.8, fy + 0.1, fz - 1.27)], [0.3, 0.26, 0.2], 0.12, 'fy_stache', pv, FRONT, ext=0.06)
        f.append(E((fx - 0.25, fy - 0.6 - (0.2 if face == 'shock' else 0), fz - 1.22), (fx + 0.25, fy - 0.45, fz - 1.18), 'fy_mouth', faces=('north',)))
        # the top hat, cocked a touch toward his right
        hat = (('z', -6.0), (fx, fy + 1.6, fz))
        f += [E((fx - 1.55, fy + 1.4, fz - 1.4), (fx + 1.55, fy + 1.7, fz + 1.4), 'fy_hat', ((0.0, 0.0, -6.0), (fx, fy + 1.6, fz))),
              E((fx - 1.0, fy + 1.65, fz - 0.95), (fx + 1.0, fy + 4.0, fz + 0.95), 'fy_hat', ((0.0, 0.0, -6.0), (fx, fy + 1.6, fz)), (0.3, 0.2)),
              E((fx - 1.04, fy + 1.7, fz - 0.99), (fx + 1.04, fy + 2.15, fz + 0.99), 'fy_hatband', ((0.0, 0.0, -6.0), (fx, fy + 1.6, fz)))]
        return f
    part('fy_fish', fish())
    for fc in FACES:
        part(f'fy_fish_x{fc}', fish(fc))

    # ---- the arms: a round shoulder plate on the bowl's side, a banded upper arm, a banded forearm (its own part, from the
    #      elbow) and a three-clawed hand
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        ex, ey = sx * 9.9, 15.4
        a = [el((x0 - (0.7 if sx > 0 else -0.7) - 0.6, y0 - 2.0, -2.0), (x0 - (0.7 if sx > 0 else -0.7) + 0.6, y0 + 2.0, 2.0), 'fy_joint', pv)]  # the shoulder plate: square
        a += chain([(x0, y0, 0), (ex, ey, 0)], [2.1], 2.1, 'fy_metal', pv, FRONT, ext=0.2)
        for t in (0.3, 0.62):                                                        # its bands
            p = (x0 + (ex - x0) * t, y0 + (ey - y0) * t, 0)
            q = (x0 + (ex - x0) * (t + 0.08), y0 + (ey - y0) * (t + 0.08), 0)
            a.append(seg(p, q, 2.45, 2.45, 'fy_band', pv, FRONT))
        a.append(el((ex - 1.3, ey - 1.3, -1.3), (ex + 1.3, ey + 1.3, 1.3), 'fy_joint', pv))   # the elbow
        return a
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 10.9, 10.4
        a = chain([(ex, ey, 0), (wx, wy, 0)], [1.95], 1.95, 'fy_metal', pv, FRONT, ext=0.1)
        for t in (0.35, 0.7):
            p = (ex + (wx - ex) * t, ey + (wy - ey) * t, 0); q = (ex + (wx - ex) * (t + 0.08), ey + (wy - ey) * (t + 0.08), 0)
            a.append(seg(p, q, 2.3, 2.3, 'fy_band', pv, FRONT))
        # the hand: a broad palm, two long claws and a thumb, slightly open
        a += [el((wx - 1.4, wy - 2.6, -1.3), (wx + 1.4, wy + 0.1, 1.2), 'fy_dark', pv),
              seg((wx - 0.55 * sx, wy - 2.3, -0.6), (wx - 0.9 * sx, wy - 4.9, -1.3), 0.95, 0.85, 'fy_dark', pv, SIDE),
              seg((wx + 0.6 * sx, wy - 2.3, -0.2), (wx + 1.05 * sx, wy - 5.0, -0.5), 0.95, 0.85, 'fy_dark', pv, SIDE),
              seg((wx - 0.2 * sx, wy - 1.6, -1.2), (wx - 0.7 * sx, wy - 3.4, -2.8), 0.85, 0.8, 'fy_dark', pv, SIDE),
              el((wx - 1.5, wy - 0.3, -1.35), (wx + 1.5, wy + 0.5, 1.25), 'fy_band', pv)]                     # the cuff
        return a
    part('fy_armr', upper(1)); part('fy_arml', upper(-1)); part('fy_forer', lower(1)); part('fy_forel', lower(-1))

    # ---- the legs: long and a little splayed, banded thigh and shin, a knee joint, big rounded boots
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; hx, hy, _ = pv
        kx, ky, ax, ay = sx * 4.3, 6.6, sx * 4.7, 2.8
        a = [el((hx - 1.2, hy - 0.9, -1.2), (hx + 1.2, hy + 0.5, 1.2), 'fy_joint', pv)]                        # the hip
        a += chain([(hx, hy, 0), (kx, ky, 0)], [2.4], 2.4, 'fy_metal', pv, FRONT, ext=0.1)
        a += chain([(kx, ky, 0), (ax, ay, 0)], [2.2], 2.2, 'fy_metal', pv, FRONT, ext=0.1)
        for (p, q) in (((hx + (kx - hx) * 0.45, hy + (ky - hy) * 0.45, 0), (hx + (kx - hx) * 0.55, hy + (ky - hy) * 0.55, 0)),
                       ((kx + (ax - kx) * 0.45, ky + (ay - ky) * 0.45, 0), (kx + (ax - kx) * 0.56, ky + (ay - ky) * 0.56, 0))):
            a.append(seg(p, q, 2.75, 2.75, 'fy_band', pv, FRONT))
        a.append(el((kx - 1.45, ky - 1.4, -1.45), (kx + 1.45, ky + 1.4, 1.45), 'fy_joint', pv))                 # the knee
        a += [el((ax - 2.3, 0.0, -2.9), (ax + 2.3, 2.8, 2.2), 'fy_dark', pv),                                     # the boot: rounded
              el((ax - 2.0, 0.0, -4.1), (ax + 2.0, 2.2, -2.8), 'fy_dark', pv, shift=(0.4, 0.3)),
              el((ax - 1.8, 2.6, -2.2), (ax + 1.8, 3.8, 1.7), 'fy_dark', pv, shift=(0.6, 0.6)),
              el((ax - 2.4, 0.0, -3.4), (ax + 2.4, 0.45, 2.3), 'fy_metal', pv)]
        return a
    part('fy_legr', leg(1)); part('fy_legl', leg(-1))
    return M


# ---------------------------------------------------------------------------------------------------- poses
# limbs: -x swings forward, z out to the side; the forearm bends at the elbow (+x folds it forward); the fish turns freely
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


POSES = {
    'idle_a': P(armr=limb(1, 4, 4), arml=limb(-1, 2, 6), forer=limb(1, 10), forel=limb(-1, 8), fish=qs(('y', 8)), weed=qs(('z', 6))),
    'idle_b': P(_off=(0, -0.15, 0), armr=limb(1, 0, 6), arml=limb(-1, 6, 4), forer=limb(1, 14), forel=limb(-1, 12), fish=qs(('y', -10), ('x', -4)), weed=qs(('z', -6))),
    'walk_a': P(_off=(0, 0.2, 0), body=qs(('z', 3)), legr=limb(1, 22), legl=limb(-1, -20), armr=limb(1, -18, 4), arml=limb(-1, 18, 4),
                forer=limb(1, 16), forel=limb(-1, 24), fish=qs(('z', -6)), weed=qs(('z', 10))),
    'walk_b': P(_off=(0, 0.2, 0), body=qs(('z', -3)), legr=limb(1, -20), legl=limb(-1, 22), armr=limb(1, 18, 4), arml=limb(-1, -18, 4),
                forer=limb(1, 24), forel=limb(-1, 16), fish=qs(('z', 6)), weed=qs(('z', -10))),
    # the art: his left arm up in a wave, the fish beaming
    'wave_a': P(_face='happy', armr=limb(1, 8, 12), forer=limb(1, 18), arml=limb(-1, 10, 112), forel=limb(-1, 40), fish=qs(('y', 10))),
    'wave_b': P(_face='happy', armr=limb(1, 8, 12), forer=limb(1, 18), arml=limb(-1, 10, 126), forel=limb(-1, 12), fish=qs(('y', 14), ('z', 4))),
    # a gentleman's bow: the bowl dips, one arm across, the fish lifts his hat
    'bow': P(_off=(0, -0.6, 0), body=qs(('x', 14)), legr=limb(1, -12), legl=limb(-1, -12), armr=limb(1, 34, -14), forer=limb(1, 70),
             arml=limb(-1, -14, 10), forel=limb(-1, 10), fish=qs(('x', 26))),
    'point': P(armr=limb(1, 84, 4), forer=limb(1, 4), arml=limb(-1, 4, 6), forel=limb(-1, 10), fish=qs(('y', 24)), _face='squint'),
    'shock': P(_face='shock', _off=(0, 0.4, 0), armr=limb(1, 30, 40), forer=limb(1, 60), arml=limb(-1, 30, 40), forel=limb(-1, 60), fish=qs(('x', -10))),
    'sit': P(_off=(0, -7.6, 0), legr=limb(1, 86, 6), legl=limb(-1, 86, 6), armr=limb(1, 10, 10), forer=limb(1, 30), arml=limb(-1, 10, 10), forel=limb(-1, 30),
             fish=qs(('y', -14))),
    'tired': P(_face='squint', _off=(0, -1.0, 0), body=qs(('x', 8), ('z', -4)), armr=limb(1, 0, 2), arml=limb(-1, 0, 2), forer=limb(1, 4), forel=limb(-1, 4),
               legr=limb(1, 6, 4), legl=limb(-1, -4, 4), fish=qs(('x', 20)))}
# the fish's laps of his bowl: round the inside, facing the way he swims (and the seaweed swaying behind him)
LAP = 8
for _i in range(LAP):
    _a = 2 * math.pi * _i / LAP
    _x, _z = 1.0 * math.sin(_a), -0.76 * math.cos(_a)          # (2.82: a smaller lap, round the tank's middle - tail and all inside the glass)
    POSES[f'swim_{_i}'] = P(armr=limb(1, 4, 4), arml=limb(-1, 2, 6), forer=limb(1, 10), forel=limb(-1, 8),
                            fish=qs(('y', -math.degrees(_a) - 90)), _fish_at=(_x, 0.5 * math.sin(2 * _a), _z), weed=qs(('z', 8 * math.sin(_a))))
DRAFT = ['idle_a', 'walk_a', 'wave_a', 'bow', 'point', 'shock', 'sit', 'tired', 'swim_2', 'swim_6']
ANIMS = {'idle': [(f'swim_{i}', 6) for i in range(LAP)], 'walk': [('walk_a', 8), ('walk_b', 8)], 'wave': [('idle_a', 8), ('wave_a', 6), ('wave_b', 6), ('wave_a', 6), ('wave_b', 6), ('idle_a', 8)],
         'bow': [('idle_a', 8), ('bow', 12), ('bow', 10), ('idle_a', 10)], 'shock': [('idle_a', 8), ('shock', 4), ('shock', 14), ('idle_a', 10)]}
