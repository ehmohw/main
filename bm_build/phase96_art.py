"""2.67: Leo's rig - the knight from the approved mockup (blue tunic, open-faced silver helm, chainmail sleeves, pointed
sabatons), now with his trident and a face that moves.

One item model per part, its joint at model (8, 8, 8) (the phase57_art kit). Design units: feet at y=0, facing -z, his
right is +x; drawn at RIG_SCALE. The trident is its own part: its joint is the grip, it stands at his right fist (the
translation follows the arm) and turns on its own - upright at his side, levelled to thrust, over the shoulder to throw,
gone while it's in the air.
His faces (strong, but caring): blink, smile (warm, eyes creased), serious (brows down, jaw set - in a fight), worried (brows
up at the middle - when YOU are hurt), hurt (one eye screwed shut, teeth gritted)."""
import math
import random
from PIL import Image, ImageDraw
from phase57_art import _cloth, _hair, _el, hexc, qa, qmul, limb, torso, _qrot

RIG_SCALE = 0.82
SALUTE_FOLD = -45
PIVOT = {'body': (0, 14, 0), 'head': (0, 26, 0), 'armr': (5.4, 24.2, 0), 'arml': (-5.4, 24.2, 0), 'legr': (2.1, 14, 0), 'legl': (-2.1, 14, 0)}
HEAD_K = 0.84          # (the helmeted head, smaller than Emma's: a grown man)
HEAD_X = 0.84          # and narrower than it is tall: his eyes are small - a wide head swamped them
PARTS = ('body', 'head', 'armr', 'arml', 'legr', 'legl', 'trident')
GRIP = (5.7, 12.1, -0.2)                     # his right fist (design units): the trident's joint
SKIN, SKIN_DK = '#9a6c50', '#7e5440'
HAIR = ('#1c1816', '#24201c', '#2c2622', '#342e28', '#3e3630')
STEEL, STEEL_DK, STEEL_LT = '#b4b8c0', '#868c96', '#dfe2e8'
BLUE, BLUE_LT, BLUE_DK = '#3f8fd6', '#78bce8', '#24528c'
LEO_EXPR = ('blink', 'smile', 'serious', 'worried', 'hurt', 'surprised', 'sleepy')


# ---------------------------------------------------------------------------------------------------- textures
def _steel(seed, base=STEEL):
    """polished plate: a soft vertical sheen, a bright streak and a darker lower edge"""
    im = _cloth(base, seed, var=0.015)
    for y in range(64):
        for x in range(64):
            k = 1.0 + 0.10 * math.cos((x - 20) / 64 * math.pi * 2) - (0.12 if y > 54 else 0)
            if 14 <= x <= 17: k += 0.18
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(max(0, min(255, p[i] * k))) for i in range(3)) + (255,))
    return im


def _mail(seed):
    """chainmail: grey with a dark diamond lattice, the way the art draws it"""
    im = _cloth('#7c8188', seed, var=0.03); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 6):
        d.line((k, 0, k + 64, 64), fill=hexc('#50555c')); d.line((k + 64, 0, k, 64), fill=hexc('#50555c'))
    for y in range(0, 64, 3):
        for x in range((y // 3) % 2, 64, 3): im.putpixel((x, y), hexc('#9aa0a8'))
    return im


def face(expr=None):
    """32 x 32 (cropped at the sides by the helm): a dark fringe under the helm, straight brows (the left one a touch higher -
    he's half amused), clear green eyes, a long nose, a closed mouth with one corner lifted. expr=None is the mockup's face."""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(SKIN)); d = ImageDraw.Draw(im); rnd = random.Random(7)
    for x in range(32):                                                                      # the fringe, ragged
        for y in range(0, 9 + (rnd.random() < 0.5) + (2 if x in (5, 6, 13, 14, 22, 27, 28) else 0)):
            im.putpixel((x, y), P(rnd.choice(HAIR[:3])))
    LID = '#1a1410'
    def eye(cx, flip, lid=0, wide=False):
        x0, y0 = cx - 4, 15
        top = y0 - (1 if wide else 0)
        d.polygon([(x0, y0 + 2), (x0 + 2, top), (x0 + 7, top), (x0 + 8, y0 + 2), (x0 + 6, y0 + 4), (x0 + 2, y0 + 4)], fill=P('#f4f0e8'))
        d.rectangle((x0 + 3, top, x0 + 5, y0 + 4), fill=P('#2f8a3a')); d.rectangle((x0 + 3, y0 + 2, x0 + 5, y0 + 4), fill=P('#56c45e'))
        d.rectangle((x0 + 4, y0 + 1, x0 + 4, y0 + 2), fill=P('#0e1a10'))
        d.point((x0 + (5 if not flip else 3), top), fill=P('#ffffff'))
        if lid:                                                                              # (the upper lid lowered: narrowed)
            d.rectangle((x0, top, x0 + 8, top + lid - 1), fill=P(SKIN))
        d.line((x0, top + lid, x0 + 8, top + lid), fill=P(LID))                              # the upper lid
        d.point((x0 + (8 if not flip else 0), top + lid + 1), fill=P(LID))
    def shut(cx, flip, tight=False):
        x0, y0 = cx - 4, 15
        if tight:                                                                            # screwed shut: a bent line
            d.line((x0, y0 + 1, x0 + 4, y0 + 3), fill=P(LID)); d.line((x0 + 4, y0 + 3, x0 + 8, y0 + 1), fill=P(LID))
        else:
            d.line((x0 + 1, y0 + 3, x0 + 7, y0 + 3), fill=P(LID)); d.point((x0 + (8 if not flip else 0), y0 + 2), fill=P(LID))
    def crease(cx, flip):                                                                    # smiling: the lower lid lifts into a crescent
        x0, y0 = cx - 4, 15
        d.polygon([(x0, y0 + 2), (x0 + 2, y0), (x0 + 7, y0), (x0 + 8, y0 + 2), (x0 + 6, y0 + 3), (x0 + 2, y0 + 3)], fill=P('#f4f0e8'))
        d.rectangle((x0 + 3, y0, x0 + 5, y0 + 2), fill=P('#2f8a3a')); d.rectangle((x0 + 4, y0 + 1, x0 + 4, y0 + 1), fill=P('#0e1a10'))
        d.line((x0, y0, x0 + 8, y0), fill=P(LID))
        d.line((x0 + 2, y0 + 3, x0 + 6, y0 + 3), fill=P('#7e5440')); d.point((x0 + 1, y0 + 2), fill=P('#7e5440')); d.point((x0 + 7, y0 + 2), fill=P('#7e5440'))
    if expr in (None, 'worried', 'surprised'):
        eye(9, False, wide=expr != None); eye(23, True, wide=expr != None)
    elif expr == 'sleepy':                                                                   # (2.67) the lids half down
        eye(9, False, lid=3); eye(23, True, lid=3)
    elif expr == 'serious':
        eye(9, False, lid=1); eye(23, True, lid=1)
    elif expr == 'blink':
        shut(9, False); shut(23, True)
    elif expr == 'smile':
        crease(9, False); crease(23, True)
    elif expr == 'hurt':
        eye(9, False, lid=2); shut(23, True, tight=True)
    for cx, s, lift in ((9, 1, 0), (23, -1, 1)):                                             # brows
        for dx in range(-4, 5):
            if expr == 'serious' or expr == 'hurt':      # down hard toward the nose
                y = 12 + (1 if dx * s > 0 else 0) + (1 if dx * s > 2 else 0)
            elif expr == 'surprised':                     # both up, high
                y = 10 + (1 if abs(dx) > 3 else 0)
            elif expr == 'worried':                       # inner ends raised
                y = 12 - (1 if dx * s > 0 else 0) - (1 if dx * s > 2 else 0)
            elif expr == 'smile':                         # soft and level, both lifted a little
                y = 11 + (1 if abs(dx) > 3 else 0)
            else:
                y = 12 - lift + (1 if dx * s > 2 else 0)
            x = cx + dx * s
            im.putpixel((x, y), P('#16110e')); im.putpixel((x, y + 1), P('#241c16'))
    for y in range(16, 23): im.putpixel((16, y), P(SKIN_DK))                                # the nose
    d.line((14, 23, 18, 23), fill=P(SKIN_DK)); d.point((13, 22), fill=P(SKIN_DK)); d.point((19, 22), fill=P(SKIN_DK))
    M = '#4a2a20'
    if expr in (None, 'blink'):                                                              # closed, one corner lifted
        d.line((12, 26, 19, 26), fill=P(M)); d.line((19, 26, 21, 25), fill=P(M))
        for x in range(13, 20): im.putpixel((x, 27), P('#8a5c44'))
    elif expr == 'smile':                                                                    # a broad, warm smile, a glint of teeth
        d.line((11, 25, 13, 26), fill=P(M)); d.line((13, 26, 19, 26), fill=P(M)); d.line((19, 26, 21, 25), fill=P(M))
        d.line((13, 27, 19, 27), fill=P(M)); d.line((14, 26, 18, 26), fill=P('#f0ece4'))
        for x in range(13, 20): im.putpixel((x, 28), P('#8a5c44'))
    elif expr == 'serious':                                                                  # a flat, set line
        d.line((12, 26, 20, 26), fill=P(M))
        for x in range(13, 20): im.putpixel((x, 27), P('#8a5c44'))
    elif expr == 'worried':                                                                  # small, turned down
        d.line((13, 27, 15, 26), fill=P(M)); d.line((15, 26, 18, 26), fill=P(M)); d.line((18, 26, 20, 27), fill=P(M))
    elif expr == 'surprised':                                                                # a small round "o"
        d.ellipse((15, 25, 17, 27), fill=P(M))
    elif expr == 'sleepy':                                                                   # slack, closed
        d.line((13, 26, 19, 26), fill=P(M))
    elif expr == 'hurt':                                                                     # teeth gritted
        d.rectangle((12, 25, 20, 27), fill=P(M)); d.rectangle((13, 26, 19, 26), fill=P('#f0ece4'))
        for x in (15, 17): im.putpixel((x, 26), P('#a89a8a'))
    for cx in (6, 26): d.ellipse((cx - 2, 21, cx + 2, 23), fill=P('#a8624c' if expr == 'smile' else '#8e5e48'))   # cheeks
    for x in range(6, 27): im.putpixel((x, 31), P('#6e4a38'))                               # the jaw line
    for x in range(9, 24): im.putpixel((x, 30), P('#86593f'))
    return im


def _emblem():
    """the chest badge (10 x 11 texels): a pale water-drop in a crescent, a pink gem at its heart, three dots round it"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(BLUE)); d = ImageDraw.Draw(im)
    d.ellipse((1, 3, 9, 11), fill=P('#bfe6f6')); d.ellipse((2, 2, 8, 9), fill=P(BLUE))      # the crescent
    d.polygon([(5, 0), (7, 4), (5, 7), (3, 4)], fill=P('#d8f2fc'))                          # the drop
    d.polygon([(5, 3), (6, 4), (5, 6), (4, 4)], fill=P('#e04aa8')); d.point((5, 4), fill=P('#ff9ad8'))   # the gem
    for x, y in ((1, 2), (9, 2), (5, 10)): d.point((x, y), fill=P('#3a5ac8'))
    return im


def _cloth_hem(base, hem, seed):
    im = _cloth(base, seed, var=0.03)
    for y in range(50, 64):
        for x in range(64):
            t = (y - 50) / 14; a, b = hexc(base), hexc(hem)
            im.putpixel((x, y), tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3)) + (255,))
    return im


def _sea_steel(base, seed):
    """the trident's sea-green metal (the vanilla trident's colours), a pale glint down one side"""
    im = _cloth(base, seed, var=0.02)
    for y in range(64):
        for x in range(64):
            k = 1.14 if x < 10 else (0.86 if x > 52 else 1.0)
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(max(0, min(255, p[i] * k))) for i in range(3)) + (255,))
    return im


def textures():
    T = {}
    T['le_skin'] = _cloth(SKIN, 71, var=0.02)
    T['le_hair'] = _hair(72, HAIR)
    T['le_face'] = face()
    for e in LEO_EXPR: T[f'le_face_{e}'] = face(e)
    T['le_steel'] = _steel(73)
    T['le_steel_dk'] = _steel(74, STEEL_DK)
    T['le_rim'] = _cloth(STEEL_LT, 75, var=0.01)
    T['le_mail'] = _mail(76)
    T['le_hose'] = _cloth('#6a6e75', 77, var=0.03)
    T['le_tunic'] = _cloth(BLUE, 78, var=0.03)
    T['le_skirt'] = _cloth_hem(BLUE, BLUE_LT, 79)
    T['le_cape'] = _cloth(BLUE_DK, 80, var=0.03)
    T['le_belt'] = _cloth('#6a4a2c', 81, var=0.04)
    T['le_emblem'] = _emblem()
    T['le_tri'] = _sea_steel('#4f9a8e', 82)
    T['le_tri_lt'] = _sea_steel('#9adccc', 86)
    T['le_tri_dk'] = _sea_steel('#2c5e56', 87)
    T['le_gold'] = _cloth('#e0b048', 83, var=0.03)
    T['le_grip'] = _cloth('#4a2e1a', 84, var=0.05, grain=(3, 0.8))
    T['le_gem'] = _cloth('#e04aa8', 85, var=0.04)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: grey hose, a brown garter, a pointed knee plate, silver sabatons with long pointed toes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.5, 3.5) if sx > 0 else (-3.5, -0.5)
        cx = (x0 + x1) / 2
        return [_el((x0, 2.4, -1.4), (x1, 14.0, 1.4), 'le_hose', pv),
                _el((x0 - 0.1, 11.6, -1.5), (x1 + 0.1, 12.3, 1.5), 'le_belt', pv),                     # the garter
                _el((x0 - 0.2, 7.0, -1.9), (x1 + 0.2, 10.0, -1.3), 'le_steel', pv),                    # knee plate
                _el((cx - 0.8, 5.6, -1.85), (cx + 0.8, 7.4, -1.35), 'le_steel', pv),
                _el((x0 - 0.2, 1.6, -1.7), (x1 + 0.2, 3.0, 1.7), 'le_steel', pv),                     # the sabaton's cuff
                _el((x0 - 0.3, 0, -3.4), (x1 + 0.3, 1.8, 1.8), 'le_steel', pv),                       # the foot
                _el((cx - 1.0, 0, -4.8), (cx + 1.0, 1.2, -3.3), 'le_steel', pv),                      # the long toe
                _el((cx - 0.5, 0, -5.8), (cx + 0.5, 0.8, -4.7), 'le_steel', pv),
                _el((x0 - 0.35, 0, 1.6), (x1 + 0.35, 1.0, 2.2), 'le_steel_dk', pv)]                    # the heel
    part('le_legr', leg(1)); part('le_legl', leg(-1))

    # ---- body: tunic to the knee (paler at the hem), the badge, a broad belt and silver buckle, a mail gorget, a cape
    pv = PIVOT['body']
    body = [_el((-4.0, 17.4, -2.4), (4.0, 24.8, 2.4), 'le_tunic', pv),                                  # chest, broad
            _el((-3.8, 13.0, -2.4), (3.8, 17.6, 2.4), 'le_skirt', pv, uv={f: [0, 0, 7.6, 4.6] for f in ('north', 'south')}),
            _el((-4.3, 9.4, -2.9), (4.3, 13.2, 2.9), 'le_skirt', pv, uv={f: [0, 8, 8.6, 16] for f in ('north', 'south', 'east', 'west')}),
            _el((-4.4, 8.8, -3.0), (4.4, 9.6, 3.0), 'le_skirt', pv, uv={f: [0, 15, 8.8, 16] for f in ('north', 'south', 'east', 'west')}),
            _el((1.0, 8.0, -3.1), (4.6, 9.4, 1.0), 'le_skirt', pv, ('z', -12, (4.4, 9.4, 0)), uv={f: [0, 15, 3.6, 16] for f in ('north', 'south', 'east', 'west')}),
            _el((-3.9, 16.6, -2.6), (3.9, 18.0, 2.6), 'le_belt', pv),
            _el((-1.0, 16.2, -2.95), (1.5, 18.4, -2.55), 'le_rim', pv), _el((0.6, 16.3, -3.05), (1.2, 18.3, -2.9), 'le_steel_dk', pv),   # the buckle
            _el((-1.25, 20.4, -2.35), (1.25, 23.2, -2.2), 'le_emblem', pv, uv={'north': [0, 0, 2.5, 2.8]}),
            _el((-3.0, 22.8, -2.55), (3.0, 25.2, -2.25), 'le_mail', pv),
            _el((-3.2, 22.5, -2.6), (3.2, 22.9, -2.3), 'le_rim', pv),
            _el((-3.4, 24.6, -2.7), (3.4, 26.4, 2.7), 'le_mail', pv),
            _el((-3.6, 24.4, -2.75), (3.6, 24.8, 2.75), 'le_rim', pv),
            _el((-3.6, 10.0, 2.3), (3.6, 25.0, 2.8), 'le_cape', pv, ('x', -7.5, (0, 25.0, 2.5))),
            _el((-3.6, 10.0, 2.4), (3.6, 10.6, 3.0), 'le_rim', pv, ('x', -7.5, (0, 25.0, 2.5)))]
    part('le_body', body)

    # ---- head: an open-faced helm
    pv = PIVOT['head']; st = lambda fr, to, rot=None, t='le_steel': _el(fr, to, t, pv, rot)
    head = [_el((-4.0, 26.0, -3.8), (4.0, 34.0, 3.8), 'le_skin', pv, uv={'north': [0, 0, 8, 8]}),
            st((-4.5, 31.8, -4.3), (4.5, 34.8, 4.4)), st((-3.9, 34.6, -3.7), (3.9, 35.8, 3.8)), st((-2.6, 35.6, -2.4), (2.6, 36.3, 2.5)),
            st((-0.45, 36.0, -0.6), (0.45, 37.4, 0.3)), st((-0.3, 37.2, -0.4), (0.3, 38.0, 0.1), t='le_rim'),
            st((-4.6, 31.2, -4.5), (-1.0, 32.0, -4.25), t='le_rim'), st((1.0, 31.2, -4.5), (4.6, 32.0, -4.25), t='le_rim'),
            st((-1.2, 30.7, -4.5), (1.2, 31.8, -4.25), t='le_rim'),
            st((-0.8, 32.6, -4.45), (0.8, 33.4, -4.3), t='le_steel_dk'),
            st((3.9, 27.6, -3.4), (4.7, 31.2, 4.4)), st((-4.7, 27.6, -3.4), (-3.9, 31.2, 4.4)),
            st((3.9, 25.6, -3.2), (4.6, 27.8, -1.0), ('z', 22.5, (4.2, 27.8, -2.0))),
            st((-4.6, 25.6, -3.2), (-3.9, 27.8, -1.0), ('z', -22.5, (-4.2, 27.8, -2.0))),
            st((3.85, 27.6, -3.5), (4.75, 28.0, 0.8), t='le_rim'), st((-4.75, 27.6, -3.5), (-3.85, 28.0, 0.8), t='le_rim'),
            st((-4.5, 27.0, 3.8), (4.5, 31.2, 4.5)), st((-3.0, 25.6, 4.0), (3.0, 27.4, 4.8), ('x', -22.5, (0, 27.4, 4.2))),
            _el((-4.1, 29.0, -3.9), (-3.6, 31.0, -1.0), 'le_hair', pv), _el((3.6, 29.0, -3.9), (4.1, 31.0, -1.0), 'le_hair', pv)]
    head[0]['faces']['north']['uv'] = [round(4 - 4 * HEAD_X, 3), 0, round(4 + 4 * HEAD_X, 3), 8]       # (the face is cropped at the sides, not squeezed)
    kx = (HEAD_K * HEAD_X, HEAD_K, HEAD_K)
    for e in head:                                                                                       # shrink about the neck (narrower across)
        e['from'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['from'])]; e['to'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['to'])]
        if 'rotation' in e: e['rotation']['origin'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['rotation']['origin'])]
    head[0]['faces']['north']['texture'] = '#le_face'
    part('le_head', head)

    # ---- arms: a domed pauldron, a short blue sleeve, a bright rim, chainmail forearm, a plated gauntlet
    def arm(sx):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.3 * sx
        return [_el((cx - 2.1, 22.8, -2.2), (cx + 2.1, 25.6, 2.2), 'le_steel', pv), _el((cx - 1.6, 25.4, -1.7), (cx + 1.6, 26.3, 1.7), 'le_steel', pv),
                _el((cx - 2.15, 22.6, -2.25), (cx + 2.15, 23.0, 2.25), 'le_rim', pv),
                _el((cx - 1.5, 19.0, -1.5), (cx + 1.5, 23.0, 1.5), 'le_tunic', pv), _el((cx - 1.7, 18.8, -1.7), (cx + 1.7, 19.8, 1.7), 'le_tunic', pv),
                _el((cx - 1.45, 18.2, -1.45), (cx + 1.45, 18.9, 1.45), 'le_rim', pv),
                _el((cx - 1.3, 14.4, -1.3), (cx + 1.3, 18.4, 1.3), 'le_mail', pv),
                _el((cx - 1.5, 13.8, -1.5), (cx + 1.5, 14.6, 1.5), 'le_rim', pv),
                _el((cx - 1.25, 11.6, -1.25), (cx + 1.25, 14.0, 1.25), 'le_steel', pv),
                _el((cx - 1.0, 10.6, -1.1), (cx + 1.0, 11.8, 0.9), 'le_steel_dk', pv),
                _el((cx - 1.9, 12.4, -1.4), (cx - 1.0, 13.6, -0.4), 'le_steel', pv) if sx > 0 else _el((cx + 1.0, 12.4, -1.4), (cx + 1.9, 13.6, -0.4), 'le_steel', pv)]
    part('le_armr', arm(1)); part('le_arml', arm(-1))

    # ---- the saluting arm (his left): the same sleeve, bent hard at the elbow - the forearm folds back up toward the helm
    def salute(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; cx = pv[0] + 0.3 * sx; ey = 18.6; FA = SALUTE_FOLD * sx
        fold = lambda fr, to, t: _el(fr, to, t, pv, ('z', FA, (cx, ey, 0)))
        up = lambda y0, y1: (2 * ey - y1, 2 * ey - y0)
        box = lambda w, y0, y1, t, z0=None, z1=None: fold((cx - w, up(y0, y1)[0], -w if z0 is None else z0), (cx + w, up(y0, y1)[1], w if z1 is None else z1), t)
        return arm(sx)[:6] + [box(1.3, 14.4, 18.4, 'le_mail'), box(1.5, 13.8, 14.6, 'le_rim'), box(1.25, 11.6, 14.0, 'le_steel'),
                              box(0.5, 9.4, 11.8, 'le_steel_dk', -1.0, -0.2), box(0.5, 9.4, 11.8, 'le_steel_dk', 0.0, 0.8),
                              box(1.0, 10.8, 11.8, 'le_steel_dk', -1.1, 1.0)]
    part('le_arml_salute', salute(-1))

    # ---- the trident (its joint is the grip, the shaft along +y): a sea-green shaft, a leather grip, a gold collar with
    #      the pink gem, a crossbar and three barbed prongs
    g = (0.0, 0.0, 0.0)
    tr = lambda fr, to, t, rot=None: _el(fr, to, t, g, rot)
    trident = [tr((-0.35, -11.0, -0.35), (0.35, 15.2, 0.35), 'le_tri'),
               tr((-0.55, -11.8, -0.55), (0.55, -10.8, 0.55), 'le_tri_dk'),                          # the butt cap
               tr((-0.5, -1.8, -0.5), (0.5, 1.8, 0.5), 'le_grip'),
               tr((-0.62, 13.2, -0.62), (0.62, 14.4, 0.62), 'le_gold'), tr((-0.4, 13.5, -0.68), (0.4, 14.1, 0.68), 'le_gem'),
               tr((-2.4, 15.0, -0.4), (2.4, 15.9, 0.4), 'le_tri'),                                    # the crossbar
               tr((-2.4, 15.8, -0.3), (-1.7, 19.6, 0.3), 'le_tri'), tr((1.7, 15.8, -0.3), (2.4, 19.6, 0.3), 'le_tri'),     # the side prongs
               tr((-2.3, 19.6, -0.22), (-1.8, 20.8, 0.22), 'le_tri_lt'), tr((1.8, 19.6, -0.22), (2.3, 20.8, 0.22), 'le_tri_lt'),
               tr((-0.36, 15.8, -0.36), (0.36, 21.6, 0.36), 'le_tri'), tr((-0.22, 21.6, -0.22), (0.22, 23.0, 0.22), 'le_tri_lt'),   # the middle one
               tr((-1.7, 17.4, -0.2), (-1.2, 18.4, 0.2), 'le_tri_lt'), tr((1.2, 17.4, -0.2), (1.7, 18.4, 0.2), 'le_tri_lt'),       # barbs
               tr((-0.75, 19.4, -0.2), (-0.36, 20.2, 0.2), 'le_tri_lt'), tr((0.36, 19.4, -0.2), (0.75, 20.2, 0.2), 'le_tri_lt')]
    part('le_trident', trident)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# Display frame (as Emma's): limb(side, fwd, out) swings a limb forward / out; torso(lean, tilt, turn). The trident's turn is
# its own (as Celi's spear): UP - upright at his right side, the prongs leaning out clear of his pauldron; TIP_FWD - levelled.
I = (0.0, 0.0, 0.0, 1.0)
U = RIG_SCALE / 16
UP = qmul(qa('z', 11), qa('x', 4))
TIP_FWD = qa('x', 90)
def P(dy=0.0, **parts):
    d = {k: I for k in PARTS}; d.update(parts); d['_dy'] = dy
    if 'trident' not in parts: d['trident'] = UP
    return d
STAND = dict(armr=limb(1, 6, 9), arml=limb(-1, -2, 6))
POSES = {
    # idle: feet planted, the trident upright at his side, a slow breath; now and then he looks out to sea
    'idle_a': P(body=torso(), head=torso(), **STAND),
    'idle_b': P(0.01, body=torso(lean=-1.5), head=torso(lean=-2), legr=limb(1, 0, 2), legl=limb(-1, 0, 2), armr=limb(1, 5, 10), arml=limb(-1, -2, 8)),
    'idle_look': P(body=torso(turn=4), head=qmul(qa('y', 28), qa('x', -4)), **STAND),
    # walk: a long, steady stride, the free arm swinging, the trident carried upright like a staff
    'walk_a': P(body=torso(tilt=2, turn=4), head=torso(turn=-3), legr=limb(1, 24), legl=limb(-1, -24), armr=limb(1, 2, 9), arml=limb(-1, 22, 6)),
    'walk_up': P(0.04, body=torso(), legr=limb(1, 3), legl=limb(-1, -3), armr=limb(1, 6, 9), arml=limb(-1, 0, 6)),
    'walk_b': P(body=torso(tilt=-2, turn=-4), head=torso(turn=3), legr=limb(1, -24), legl=limb(-1, 24), armr=limb(1, 10, 9), arml=limb(-1, -22, 6)),
    # run: leaning in, the trident levelled ahead
    'run_a': P(0.02, body=torso(lean=10, tilt=3), head=torso(lean=-8), legr=limb(1, 44), legl=limb(-1, -42), armr=limb(1, 26, 8), arml=limb(-1, 40, 10), trident=qa('x', 76)),
    'run_up': P(0.1, body=torso(lean=10), head=torso(lean=-9), legr=limb(1, 10), legl=limb(-1, -28), armr=limb(1, 28, 8), arml=limb(-1, 0, 14), trident=qa('x', 78)),
    'run_b': P(0.02, body=torso(lean=10, tilt=-3), head=torso(lean=-8), legr=limb(1, -42), legl=limb(-1, 44), armr=limb(1, 30, 8), arml=limb(-1, -40, 10), trident=qa('x', 80)),
    'jump': P(body=torso(lean=6), head=torso(lean=-10), legr=limb(1, 30), legl=limb(-1, -36), armr=limb(1, 30, 12), arml=limb(-1, 20, 40), trident=qa('x', 60)),
    # sit: down on the ground, legs out (the left knee drawn up a little), leaning back on his left hand, the trident laid across
    # his knees, prongs ahead; he breathes, looks out to sea, and now and then stands the trident up beside him like a staff
    'sit_a': P(-0.6, body=torso(lean=-8), head=torso(lean=4), legr=limb(1, 84, 4), legl=limb(-1, 62, 6), armr=limb(1, 30, 8), arml=limb(-1, -28, 16), trident=qmul(qa('y', -14), qa('x', 96))),
    'sit_b': P(-0.58, body=torso(lean=-10), head=qmul(qa('y', 10), qa('x', 2)), legr=limb(1, 84, 4), legl=limb(-1, 58, 6), armr=limb(1, 28, 8), arml=limb(-1, -30, 16), trident=qmul(qa('y', -14), qa('x', 96))),
    'sit_look': P(-0.6, body=torso(lean=-8, turn=8), head=qmul(qa('y', 34), qa('x', -6)), legr=limb(1, 84, 4), legl=limb(-1, 62, 6), armr=limb(1, 30, 8), arml=limb(-1, -28, 16), trident=qmul(qa('y', -14), qa('x', 96))),
    'sit_staff': P(-0.6, body=torso(lean=-4), head=qmul(qa('y', -8), qa('x', 6)), legr=limb(1, 84, 4), legl=limb(-1, 62, 6), armr=limb(1, 74, 10), arml=limb(-1, -28, 16), trident=qmul(qa('z', 8), qa('x', -4))),
    # the salute (on arrival): mid-stride, two fingers off the helm with his left hand (the folded arm model), the trident up
    'salute': P(body=qa('y', 8), head=qmul(qa('y', -10), qa('x', 4)), arml=qmul(qa('y', 6), qmul(qa('z', 96), qa('x', -18))),
                armr=limb(1, 4, 9), legr=qa('x', 22), legl=qa('x', -20)),
    # the thrust: draw back, then drive the prongs straight ahead
    'thrust_back': P(body=torso(lean=-4, turn=-14), head=torso(turn=10), legr=limb(1, -14), legl=limb(-1, 18), armr=limb(1, 22, 10), arml=limb(-1, 24, 26), trident=TIP_FWD),
    'thrust': P(-0.02, body=torso(lean=10, turn=10), head=torso(lean=-8, turn=-8), legr=limb(1, -22), legl=limb(-1, 30), armr=limb(1, 86, 0), arml=limb(-1, -30, 20), trident=TIP_FWD),
    # the throw: the trident up over his shoulder, then the arm whips through - the trident is gone
    'throw_back': P(body=torso(lean=-8, turn=-20), head=torso(turn=16), legr=limb(1, -18), legl=limb(-1, 22), armr=limb(1, -130, 12), arml=limb(-1, 46, 20), trident=qa('x', 80)),
    'throw': P(0.01, body=torso(lean=12, turn=14), head=torso(lean=-6, turn=-10), legr=limb(1, -26), legl=limb(-1, 32), armr=limb(1, 70, 4), arml=limb(-1, -34, 24), trident=TIP_FWD),
    # on guard (covering you): feet wide, the trident held out before him, prongs up and forward
    'guard': P(-0.04, body=torso(lean=4, turn=-10), head=torso(turn=8), legr=limb(1, -14, 10), legl=limb(-1, 18, 10), armr=limb(1, 52, -6), arml=limb(-1, 34, 12), trident=qa('x', 34)),
}
# (2.67) swimming - he's at home in the water: a strong one-armed crawl with his left, the trident levelled ahead in his right like
# a lance, a long scissor kick
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(-0.6 + 0.03 * math.sin(2 * _p), body=torso(lean=6, tilt=3 * math.sin(_p), turn=4 * math.sin(_p)), head=torso(lean=2, turn=-3 * math.sin(_p)),
                            armr=limb(1, 84, 8), trident=qa('x', 90),
                            arml=limb(-1, 96 + 64 * math.sin(_p), 16 + 12 * math.cos(_p)),
                            legr=limb(1, -22 + 24 * math.sin(2 * _p)), legl=limb(-1, -22 - 24 * math.sin(2 * _p)))


def _off(a, b):
    """design offset a -> b in the display frame"""
    return (-(b[0] - a[0]) * U, (b[1] - a[1]) * U, -(b[2] - a[2]) * U)


def part_xf(pose, p):
    """(left_rotation, translation) for part p: the trident stands at his right fist wherever the arm carries it (its own
    turn). Every other part stands at its own joint."""
    dy = pose['_dy']
    if p == 'trident':
        e = _qrot(pose['armr'], _off(PIVOT['armr'], GRIP))
        return pose['trident'], (e[0], e[1] + dy, e[2])
    return pose[p], (0.0, dy, 0.0)


def joint(p):
    return PIVOT['armr' if p == 'trident' else p]


def crest_icon(R):
    """Leo's Crest: the blue shield-badge from his chest - the crescent, the drop, the pink gem - in a silver rim"""
    return R.grid(['................', '...SSSSSSSSSS...', '..SBBBBBBBBBBS..', '..SBBBBWWBBBBS..', '..SBBBLWWLBBBS..', '..SBBLBWWBLBBS..',
                   '..SBBLBPPBLBBS..', '..SBBLBPPBLBBS..', '..SBBBLBBLBBBS..', '...SBBBLLBBBS...', '...SBBBBBBBBS...', '....SBBBBBBS....',
                   '.....SBBBBS.....', '......SBBS......', '.......SS.......', '................'],
                  dict(S='#dfe2e8', B='#3f8fd6', W='#d8f2fc', L='#bfe6f6', P='#e04aa8'))
