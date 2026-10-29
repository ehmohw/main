"""2.99 (v299): THE DREADBORNE, redrawn - the dark mirror of the Seraph's Raiment (seraph_art.py). The Dread bosses' armour
(phase206) and the Dread monsters' own (phase176, through dread_armor.py, which draws its helm and plate from here).

THE WORN LAYERS (64 x 32, the pack's armour resolution)
  humanoid  bm:dread   cracked void-plate, red light in the cracks. The breast a RIBCAGE: a bone sternum with a slit-pupilled eye
            at its top, ribs arching out over black, the gaps between them glowing red; a bone gorget; a chain belt; a
            tattered fauld, its hem smouldering. On the back a spine of vertebrae and two bone sockets with eyes (where the 3D
            wings root). SPINED pauldrons (bone spikes, an eye on each), vambraces chained and clawed at the wrist. The
            Treads: chains at the ankle, a bone spur at the heel, bone CLAWS for toes.
  humanoid_leggings  bm:dread   a chain belt with a bone clasp, tattered tassets; void cuisses with red cracks, a bone spur
            down each outer thigh, a bone knee-cap with an eye in it.
  wings     bm:dread_wings   (the Carapace's elytra mesh) cut back like the Seraph's to a mantle over the shoulder blades - black
            membrane on a bone spar, red veins, two eyes, a torn edge: the 3D wings (seraph_wings / dread_wings) own the
            silhouette.
THE DREAD VISAGE (3D, item model bm:dread_helm - the Dread monsters wear the same one): a bevelled hood of black chitin cracked
  with red; an ARC OF SEVEN EYES across the brow (slit pupils, lit); a maw - a slit of red light behind bone teeth - and two
  bone mandibles curving down to fangs; two great horns sweeping out, back and up, ringed bone darkening to black tips; a
  crown of spines along the crest; tendrils of flesh down the back, embers at their ends; and, the Seraph's halo turned: a
  BROKEN HALO OF THORNS - a ring of black iron, three gaps in it, bone thorns pointing out, embers and two eyes on it.
  Model space as before: a head filling 3..13 (shown x1.28 on the head), front north.
THE SPRITES  dread_carapace / greaves / treads, drawn on vanilla's silhouettes (the Dread Heart's is dread_set_art's).
Block textures (dk_*) 32 x 32, as seraph_art's."""
import math
import random
from PIL import Image

import rigkit
import seraph_art as SA
from seraph_art import Layer, FULL

# ---------------------------------------------------------------------------------------------------- the palette
BLACK, VOID, VOID2, VOID_L, VOID_LL, GLINT = (8, 6, 10), (22, 16, 26), (34, 24, 40), (48, 34, 54), (72, 54, 80), (104, 84, 112)
RED_D, RED, RED_L, HOT = (98, 6, 18), (208, 24, 46), (255, 90, 100), (255, 196, 170)
BONE_L, BONE, BONE_S, BONE_D = (244, 236, 216), (216, 204, 176), (154, 140, 112), (96, 84, 64)
IRON_D, IRON, IRON_L = (64, 62, 74), (118, 116, 130), (168, 166, 180)
FLESH, FLESH_L, FLESH_D = (90, 20, 32), (134, 40, 58), (48, 8, 14)
PAL = {'k': BLACK, 'v': VOID, 'V': VOID2, 'l': VOID_L, 'L': VOID_LL, 'q': GLINT, 'd': RED_D, 'r': RED, 'R': RED_L, 'w': HOT,
       'B': BONE_L, 'b': BONE, 'c': BONE_S, 'C': BONE_D, 'i': IRON_D, 'I': IRON, 'J': IRON_L}
_c, _mix = SA._c, SA._mix


class DLayer(Layer):
    def art(self, box, face, x, y, rows):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.': self.f(box, face, x + i, y + j, PAL[ch])

    def top(self, box, which, rows):
        Layer.top(self, box, which, lambda x, y, w, h: PAL[rows[y][x]] if rows[y][x] != '.' else None)


# every face by hand. Strips: right/outer, front, left/inner, back; rows from v 20. Light from above and the viewer's left.
BODY = {
    'right': ['CccC', 'vlLv', 'lvVv', 'vvcb', 'vkdv', 'vvcb', 'lVkv', 'kvvc', 'iIiI', 'vlLk', 'lVvk', 'dk.d'],
    'front': ['CcBccBcC',
              'vcRkkRcv',
              'LkcbbckV',
              'bccbBccb',
              'vkdbBdkv',
              'cbcbBcbc',
              'vVkbBkVk',
              'kcbbbbck',
              'iIiJJiIi',
              'vlLvlLlk',
              'lvvVlrvk',
              'd.vkd.vk'],
    'left': ['CccC', 'vLlv', 'vVvk', 'bcvv', 'vdkk', 'bcvv', 'vkVk', 'cvvk', 'IiIi', 'lLvk', 'vVlk', 'd.dk'],
    'back': ['CcbBBbcC',
             'cRcBBcRc',
             'kckccckk',
             'vlvbBvlv',
             'lvVccVvk',
             'vlvbBvlk',
             'vVkccdvk',
             'kvvbBvvk',
             'iIiJJiIi',
             'vlLvlLlk',
             'lvVvlrvk',
             'dkv.dk.d']}
BODY_TOP = ['BcBccBcB', 'cvvkkvvc', 'vlLvvlLv', 'CccCCccC']
ARM = {
    'outer': ['BkBk', 'bcbc', 'cRkR', 'vlLv', 'lvdv', 'kdkd', '....', '....', 'iIiI', 'vlLv', 'lvdv', 'BcBc'],
    'front': ['kBkB', 'cbcb', 'vlLv', 'lVvv', 'vdlv', 'kdkd', '....', '....', 'IiIi', 'vLlv', 'lvVv', 'cBcB'],
    'inner': ['kckc', 'cvcv', 'vlvv', 'vVvk', 'lvvk', 'kdkk', '....', '....', 'iIiI', 'vlvk', 'vVvk', 'CcCc'],
    'back': ['BkBk', 'bcbc', 'vlvv', 'vVlk', 'lvdk', 'kdkd', '....', '....', 'IiIi', 'vlvk', 'lvVk', 'cCcC']}
ARM_TOP = ['BkBk', 'kBkB', 'BcBc', 'cCcC']
FEET = {
    'outer': ['iIiI', 'vlLv', 'lvdv', 'cbvv', 'lvvk', 'CcCk'],
    'front': ['IiJi', 'vlLv', 'lVvv', 'vdVv', 'bcbc', 'BkBk'],
    'inner': ['iIiI', 'vlvk', 'vVvk', 'lvvk', 'vvvk', 'CcCk'],
    'back': ['IiIi', 'vlvk', 'lVvk', 'vbck', 'kBck', 'kCck']}
SOLE = ['kCCk', 'CvvC', 'CvvC', 'kCCk']
HIPS = {
    'right': ['iIiI', 'vlLk', 'lVvk', 'dvlk', 'k.dk'],
    'front': ['iIcBBcIi', 'vlLvlLlk', 'lvVvlrvk', 'dvlvVvlk', 'k.dkk.dk'],
    'left': ['IiIi', 'lLvk', 'vVlk', 'vldk', 'kd.k'],
    'back': ['iIiIiIiI', 'vlvlvlvk', 'lVvvlVvk', 'vdvlvdvk', 'kk.dk.dk']}
THIGH = {
    'outer': ['iIiI', 'vcLv', 'lcVv', 'vbdv', 'lcvv', 'vbVv', 'lcdv', 'vvvk', 'kCCk'],
    'front': ['IiIi', 'vlLv', 'lVvv', 'cbbc', 'bRkb', 'cbbc', 'vlVv', 'lvdv', 'kvvk'],
    'inner': ['iIiI', 'vlvk', 'vVvk', 'lvvk', 'vdvk', 'vVvk', 'lvvk', 'vvkk', 'kkkk'],
    'back': ['IiIi', 'vlvk', 'lVvk', 'vdvk', 'lvvk', 'vVlk', 'vdvk', 'vvkk', 'kkkk']}
THIGH_TOP = ['iIIi', 'IvlI', 'IlvI', 'iIIi']


def humanoid():
    """bm:dread humanoid: the Carapace's plate (body, arms) and the Treads (the legs' feet)"""
    L = DLayer()
    for face, rows in BODY.items(): L.art('body', face, 0, 0, rows)
    L.top('body', 0, BODY_TOP)
    for face, rows in ARM.items(): L.art('arm', face, 0, 0, rows)
    L.top('arm', 0, ARM_TOP)
    for face, rows in FEET.items(): L.art('leg', face, 0, 6, rows)
    L.top('leg', 1, SOLE)
    return L.im


def leggings():
    """bm:dread humanoid_leggings: the chain belt and tattered tassets, the cuisses with an eye in each knee-cap"""
    L = DLayer()
    for face, rows in HIPS.items(): L.art('body', face, 0, 7, rows)
    for face, rows in THIGH.items(): L.art('leg', face, 0, 0, rows)
    L.top('leg', 0, THIGH_TOP)
    return L.im


def wings_layer():
    """bm:dread_wings: the elytra mesh's wing cut back to a mantle over the shoulder blades (7 of its 20 rows, as the Seraph's):
    a bone spar on the leading edge, black membrane with red veins, two eyes, a torn edge; its sides left clear"""
    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); px = im.load()
    X0, Y0, LEN = 36, 2, 7
    rows = ['BcvlvVvlrv',
            'bclvrvVvdv',
            'bcvRkRvlvr',
            'cCvlvdvrVv',
            'cCdvVvlRkR',
            'CCvrvlvdvl',
            'C.d.v.d.r.']
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != '.': px[X0 + c, Y0 + r] = PAL[ch] + (255,)
    return im


# ---------------------------------------------------------------------------------------------------- the 3D pieces' textures (32 x 32)
_paint = SA._paint


def _crack(px, rnd, n, size=32, col=RED, hot=RED_L, lip=RED_D):
    for _ in range(n):
        x, y = rnd.randrange(size), rnd.randrange(size)
        for i in range(rnd.randint(4, 10)):
            if 0 <= x < size and 0 <= y < size:
                px[x, y] = _c(hot if i == 0 or rnd.random() < 0.15 else col)
                if x > 0: px[x - 1, y] = _c(lip)
            x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1, 1))


def _chitin(seed, k=1.0, cracks=5):
    """black chitin: plates (a lit lip, a dark seam every 8 rows, staggered joints), a dull violet sheen, red cracks"""
    def c(x, y, r):
        b = VOID if r.random() > 0.3 else (VOID2 if r.random() > 0.4 else BLACK)
        if y % 8 == 0: b = VOID_LL if r.random() > 0.3 else VOID_L
        if y % 8 == 7: b = BLACK
        if (x + (y // 8) * 11) % 16 == 0 and y % 8 not in (0, 7): b = BLACK
        if r.random() < 0.03: b = GLINT
        return _c(b, k)
    im = _paint(c, seed); px = im.load(); _crack(px, random.Random(seed), cracks)
    return im


def _bone(seed, dark=False):
    base, lit, sh = (BONE_S, BONE, BONE_D) if dark else (BONE, BONE_L, BONE_S)
    def c(x, y, r):
        if y % 6 == 0: return _c(sh)
        if y % 6 == 1: return _c(lit)
        return _c(base if r.random() > 0.15 else sh)
    return _paint(c, seed)


def _horn(seed):
    """a horn, a spar, a claw (whole uv, along v): ringed bone at the root darkening through brown to a black point"""
    def c(x, y, r):
        t = y / 31
        b = _mix(BONE, BONE_D, min(1, t * 1.4)) if t < 0.7 else _mix(BONE_D, BLACK, (t - 0.7) / 0.3)
        if y % 5 == 0: b = _mix(b, BLACK, 0.45)
        if x in (0, 1, 30, 31): b = _mix(b, BLACK, 0.35)
        if r.random() < 0.08: b = _mix(b, BONE_L, 0.3)
        return _c(b)
    return _paint(c, seed)


def _eye(seed=0, lid=VOID):
    """a Dread eye (whole uv): an almond of red in black lids, a slit pupil, a hot glint"""
    def c(x, y, r):
        dx, dy = (x - 15.5) / 15.0, (y - 15.5) / 9.0
        a = abs(dy) + dx * dx * 0.9
        if a > 1.15: return _c(lid if r.random() > 0.3 else BLACK)
        if a > 0.95: return _c(RED_D)
        if abs(x - 15.5) < 1.6 and abs(dy) < 0.85: return _c(BLACK)                 # (the slit)
        d = math.hypot(x - 15.5, (y - 15.5) * 1.5)
        return _c(_mix(HOT, RED, min(1, d / 6)) if d < 6 else _mix(RED, RED_D, min(1, (d - 6) / 10)))
    im = _paint(c, seed); px = im.load()
    for (x, y) in ((11, 11), (12, 11), (11, 12)): px[x, y] = _c(HOT)
    return im


def _membrane(seed):
    """a membrane (along v from the bone it hangs from to its torn end - each strip shows its own window across): black-violet
    skin, mottled, a few veins of dark red running down it with a thread of light in them, its end torn (cut out) and
    smouldering, a hole or two"""
    rnd = random.Random(seed)
    tear = [25 + int(4 * abs(math.sin(x * 0.9 + seed))) + rnd.randint(0, 2) for x in range(32)]
    def c(x, y, r):
        if y > tear[x]: return (0, 0, 0, 0)
        q = r.random()
        b = VOID2 if q > 0.4 else (VOID if q > 0.08 else VOID_L)
        if y < 2: b = BONE_D
        if y > tear[x] - 2: b = _mix(b, RED_D, 0.7)
        return _c(b)
    im = _paint(c, seed); px = im.load()
    for v0 in (6, 19, 28):                                                              # veins down it, a branch or two
        x, y = v0, 2
        while y < 30:
            x = max(0, min(31, x))
            if px[x, y][3]: px[x, y] = _c(RED if (y % 7 == 3) else RED_D)
            if rnd.random() < 0.08:
                bx, by = x, y
                for _ in range(rnd.randint(2, 4)):
                    bx += rnd.choice((-1, 1)); by += 1
                    if 0 <= bx < 32 and by < 32 and px[bx, by][3]: px[bx, by] = _c(RED_D)
            x += rnd.choice((-1, 0, 0, 0, 1)); y += 1
    for _ in range(2):
        hx, hy = rnd.randrange(4, 28), rnd.randrange(10, 20)
        for dx in (0, 1):
            for dy in (0, 1): px[hx + dx, hy + dy] = (0, 0, 0, 0)
    return im


def _flesh(seed):
    def c(x, y, r):
        if y % 4 == 0: return _c(FLESH_D)
        return _c(FLESH if r.random() > 0.2 else FLESH_L)
    return _paint(c, seed)


def _ember(seed):
    return _paint(lambda x, y, r: _c(r.choice((RED, RED_L, RED_L, HOT, (255, 120, 60)))), seed)


def _chain(seed):
    """chain (whole uv, along v): iron links, the gaps between cut out"""
    def c(x, y, r):
        ly = y % 8; link = (y // 8) % 2
        if link == 0:                                      # (a link face on: an oval ring)
            if 9 <= x <= 22 and ly in (0, 7): return _c(IRON)
            if (x in (9, 10) or x in (21, 22)) and 0 < ly < 7: return _c(IRON_L if x < 16 else IRON_D)
            return (0, 0, 0, 0)
        if 14 <= x <= 17: return _c(IRON_L if x == 14 else (IRON if x < 17 else IRON_D))   # (a link edge on)
        return (0, 0, 0, 0)
    return _paint(c, seed)


def _iron(seed):
    def c(x, y, r):
        b = IRON_D if r.random() > 0.25 else (IRON if r.random() > 0.5 else BLACK)
        if r.random() < 0.05: b = RED_D
        return _c(b)
    return _paint(c, seed)


def textures():
    return {'dk_chitin': _chitin(4101, 1.0, 2), 'dk_chitin_d': _chitin(4102, 0.8, 1), 'dk_bone': _bone(4103), 'dk_bone_d': _bone(4104, True),
            'dk_horn': _horn(4105), 'dk_eye': _eye(4106), 'dk_membrane': _membrane(4107), 'dk_membrane_b': _membrane(4108),
            'dk_flesh': _flesh(4109), 'dk_ember': _ember(4110), 'dk_chain': _chain(4111), 'dk_iron': _iron(4112)}


# ---------------------------------------------------------------------------------------------------- building
NOSHIFT = {'dk_eye', 'dk_horn', 'dk_membrane', 'dk_membrane_b', 'dk_chain'}
SA.NOSHIFT |= NOSHIFT                                     # (seraph_art's builders: these are whole-uv textures too)
E, SEG, GEM = SA.E, SA.SEG, SA.GEM
UP, FRONT, BACK = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (0.0, 0.0, 1.0)


def EYE(c, w, h, n, pv, d=0.3, light=12):
    """a Dread eye set in a surface facing n, a black rim round it"""
    n = rigkit._unit(n)
    side = rigkit._unit(rigkit._cross(n, (0.0, 1.0, 0.0) if abs(n[1]) < 0.9 else (1.0, 0.0, 0.0)))
    A_ = lambda w_, dn: (tuple(c[i] - side[i] * w_ / 2 + n[i] * dn for i in range(3)), tuple(c[i] + side[i] * w_ / 2 + n[i] * dn for i in range(3)))
    uv = {'up': [0, 16, 16, 0], 'down': [0, 0, 16, 16], 'north': [0, 0, 1, 1], 'south': [0, 0, 1, 1], 'east': [0, 0, 1, 1], 'west': [0, 0, 1, 1]}
    return [SEG(*A_(w + 0.45, -0.12), h + 0.45, d, 'dk_chitin_d', pv, n), SEG(*A_(w, 0.0), h, d + 0.06, 'dk_eye', pv, n, light=light, uv=uv)]


def CHAIN(pts, w, tex, pv, up, light=0):
    """a tapering run along a polyline (horns, spars, tendrils); w: (start, end)"""
    n = len(pts) - 1; out = []
    for i in range(n):
        ww = w[0] + (w[1] - w[0]) * i / max(1, n - 1)
        out.append(SEG(pts[i], pts[i + 1], ww, ww, tex, pv, up, ext=0.15, light=light, uv=FULL() if tex in NOSHIFT else None))
    return out


def helm_model():
    """the Dread Visage: drawn for a head filling 3..13 (front north, -z)"""
    pv = (8.0, 8.0, 8.0); SA._rs.seed(4100)
    H = []
    H.append(E((3.0, 2.8, 3.2), (13.0, 12.4, 13.0), 'dk_chitin', pv))                       # the hood
    for (x0, x1, z0, z1) in ((2.7, 13.3, 3.6, 12.6), (3.4, 12.6, 2.9, 13.3)):              # (bevelled)
        H.append(E((x0, 3.2, z0), (x1, 12.0, z1), 'dk_chitin', pv))
    H.append(E((3.6, 12.4, 3.8), (12.4, 13.6, 12.4), 'dk_chitin', pv))                      # its crown, stepped
    H.append(E((4.8, 13.6, 5.0), (11.2, 14.3, 11.4), 'dk_chitin_d', pv))
    H.append(E((7.3, 12.6, 3.0), (8.7, 14.8, 13.1), 'dk_bone_d', pv))                       # a ridge of bone, brow to nape
    H.append(E((2.6, 2.5, 10.6), (13.4, 6.0, 13.6), 'dk_chitin_d', pv))                     # the nape guard
    H.append(E((7.4, 2.9, 13.3), (8.6, 10.6, 13.7), 'dk_bone', pv))                         # vertebrae down the back
    for k in range(4): H.append(E((6.9, 3.6 + 1.9 * k, 13.5), (9.1, 4.4 + 1.9 * k, 13.9), 'dk_bone_d', pv))
    H.append(E((3.1, 2.6, 2.75), (12.9, 12.0, 3.1), 'dk_chitin_d', pv))                     # the face plate
    H.append(E((6.0, 10.4, 2.5), (10.0, 11.6, 2.9), 'dk_bone_d', pv))                       # a brow of bone
    for sx in (-1, 1):                                                                       # cheek plates, bone-edged
        x0, x1 = (2.3, 3.1) if sx < 0 else (12.9, 13.7)
        H.append(E((x0, 3.0, 3.0), (x1, 10.4, 8.6), 'dk_chitin', pv))
        H.append(E((x0 - 0.05, 3.0, 8.4), (x1 + 0.05, 10.4, 8.9), 'dk_bone_d', pv))
    # eyes on its sides and back
    for (x, y, z, n) in ((2.2, 6.4, 10.6, (-1, 0, 0)), (13.8, 6.8, 10.4, (1, 0, 0)), (2.2, 9.0, 5.8, (-1, 0, 0)), (13.8, 8.6, 6.0, (1, 0, 0)),
                         (5.4, 8.0, 13.25, (0, 0, 1)), (10.6, 8.0, 13.25, (0, 0, 1))):
        H += EYE((x, y, z), 1.9, 1.1, n, pv)
    H = rigkit.transform(H, lambda v: [8 + (v[0] - 8) * 1.1, 7.6 + (v[1] - 7.6) * 1.1, 8 + (v[2] - 8) * 1.1])   # (clear of the hat layer)
    # THE ARC OF SEVEN EYES across the brow
    for (x, y, w, h) in ((8.0, 9.3, 3.2, 1.9), (5.1, 8.9, 2.3, 1.35), (10.9, 8.9, 2.3, 1.35), (3.2, 7.6, 1.5, 1.0), (12.8, 7.6, 1.5, 1.0),
                         (6.3, 11.3, 1.4, 0.85), (9.7, 11.3, 1.4, 0.85)):
        H += EYE((x, y, 2.05), w, h, FRONT, pv, d=0.35, light=13)
    # the maw: a slit of red light behind bone teeth
    H.append(E((7.0, 2.6, 2.0), (9.0, 7.2, 2.2), 'dk_ember', pv, light=12, shade=False))
    for k in range(5):
        y = 3.0 + 0.85 * k
        H.append(E((6.6, y, 1.8), (7.6, y + 0.45, 2.15), 'dk_bone', pv)); H.append(E((8.4, y + 0.4, 1.8), (9.4, y + 0.85, 2.15), 'dk_bone', pv))
    for sx in (-1, 1):
        X = lambda x: 8 + sx * (x - 8)
        # mandibles from the jaw, curving down and in to fangs
        H += CHAIN([(X(3.4), 4.6, 2.6), (X(3.0), 2.6, 1.6), (X(4.0), 0.8, 0.6), (X(5.6), -0.4, 0.2)], (1.3, 0.55), 'dk_horn', pv, FRONT)
        # the horns: out from the temples, back and up, ringed bone to black points
        H += CHAIN([(X(3.4), 11.4, 7.0), (X(0.9), 12.3, 7.6), (X(-1.3), 14.4, 8.9), (X(-2.0), 17.4, 10.5), (X(-1.3), 20.2, 11.8), (X(0.1), 22.2, 12.3)],
                   (2.4, 0.55), 'dk_horn', pv, FRONT)
        # tendrils down the back, embers at their ends
        for j, (x, sway) in enumerate(((4.6, -0.5), (7.0, 0.4) if sx > 0 else (6.4, -0.3))):
            pts = [(X(x), 4.0, 13.8), (X(x + sway), 1.6, 14.6), (X(x + 2 * sway), -0.6, 15.0), (X(x + 2.6 * sway), -2.6, 14.8)]
            H += CHAIN(pts, (1.3, 0.6), 'dk_flesh', pv, BACK)
            H.append(GEM(pts[-1], 0.6, 'dk_ember', pv, light=13))
    # a crown of spines along the crest, raked back
    for x, h in ((4.8, 2.0), (6.4, 3.2), (8.0, 4.2), (9.6, 3.2), (11.2, 2.0)):
        H += CHAIN([(x, 14.6, 7.6), (x, 14.6 + h * 0.6, 8.6), (x, 14.6 + h, 10.2)], (0.9, 0.3), 'dk_horn', pv, FRONT)
    # THE BROKEN HALO OF THORNS: black iron, three gaps, thorns out, embers and two eyes on it
    c, R, n = (8.0, 16.6, 10.6), 5.3, 22
    tilt = math.radians(24)
    def hp(a, r=R, dy=0.0):
        x, z = r * math.cos(a), r * math.sin(a)
        return (c[0] + x, c[1] + dy - z * math.sin(tilt), c[2] + z * math.cos(tilt))
    up_t = (0.0, math.cos(tilt), math.sin(tilt))
    for i in range(n):
        if i in (3, 10, 17): continue                                                         # (the breaks)
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        H.append(SEG(hp(a0), hp(a1), 0.85, 0.6, 'dk_iron', pv, up_t, ext=0.1))
        if i % 2 == 0:
            a = (a0 + a1) / 2
            H.append(SEG(hp(a), hp(a, R + 1.6 + 0.6 * (i % 4 == 0)), 0.45, 0.45, 'dk_horn', pv, up_t, uv=FULL()))   # thorns
        if i % 5 == 1:
            H.append(GEM(hp((a0 + a1) / 2, dy=0.35), 0.55, 'dk_ember', pv, light=14))
    for a in (math.pi * 0.25, math.pi * 0.75):
        p = hp(a, dy=0.1)
        H += EYE(p, 1.3, 0.8, (math.cos(a) * 0.3, 0.2, -1.0), pv, d=0.5, light=13)
    return H


def helm_json(display):
    els = helm_model()
    for e in els:
        for v in e['from'] + e['to']: assert -16 <= v <= 32, e
        for fc in e['faces'].values(): fc['uv'] = [max(0.0, min(16.0, u)) for u in fc['uv']]
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    return {'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/dk_chitin'), 'elements': els, 'display': display}


# ---------------------------------------------------------------------------------------------------- the sprites
ICON_ROWS = {   # (vanilla's silhouettes, drawn over: the dark mirror of the Seraph's sprites)
    'dread_carapace': [             # the Carapace: a ribcage of bone, an eye at its top, black membrane wings behind it
        'Bk............kB',
        'cvl..........lvc',
        'vkkkkk....kkkkkv',
        'lkBcBk....kBcBkl',
        'dkvlLkk..kkLlvkd',
        'vkvlrkcRRckrlvkv',
        'rklvdcbkkbcdvlkr',
        'dkkLcbccccbcLkkd',
        'r..kbcrBBrcbk..r',
        '...kvcbccbcvk...',
        '...kiIiJJiIik...',
        '...kvlLvlLlvk...',
        '...klrvlrvlvk...',
        '....kkdkdkkk....',
        '.....kkkkkk.....',
        '................'],
    'dread_greaves': [              # the Greaves: a chain belt and bone clasp, tattered tassets, an eye in each bone knee
        '................',
        '................',
        '....kkkkkkkk....',
        '...kiIcBBcIik...',
        '...kvlLvlLlvk...',
        '...klrvdlrdvk...',
        '...kvlLkkLlvk...',
        '...klrk..kvrk...',
        '...kcbk..kbck...',
        '...kRkk..kkRk...',
        '...kcbk..kbck...',
        '...kvdk..kdvk...',
        '...klvk..kvlk...',
        '...kkkk..kkkk...',
        '................',
        '................'],
    'dread_treads': [               # the Treads: chained ankles, bone spurs, bone claws for toes
        '................',
        '................',
        '................',
        '...ik......ki...',
        '...kIk....kIk...',
        '...kvk....kvk...',
        '...kiIk..kIik...',
        '...klrk..krlk...',
        '...kvdk..kdvk...',
        '..kvlrk..krlvk..',
        '.kBlvdk..kdvlBk.',
        '.BcbvCk..kCvbcB.',
        '.kBkBk....kBkBk.',
        '................',
        '................',
        '................'],
}


def icons():
    out = {}
    for k, rows in ICON_ROWS.items():
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != '.': px[x, y] = PAL[ch] + (255,)
        out[k] = im
    return out
