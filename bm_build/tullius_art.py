"""2.76: TULLIUS - the drowned captain, Leo's rival (a draft for approval: rig, textures, faces, poses).

From the reference art: a vengeful undead soldier of the sunken kingdom - a skull of icy blue bone under a cracked brow,
hollow black sockets with a cold light deep in them, frost-white hair spiking out under a tall, battered top hat (a torn
green band, a cluster of ice crystals at his left), an emerald earring in his left ear; a torn teal frock coat with a
high, spiky collar and great dark cuffs, a ragged green shirt, a green sash knotted at his left hip and an icy buckle on a
strap at his right; black gloves, green stockings, big dark teal shoes; and in his LEFT hand a long barbed harpoon with a
rope tied at its head. His element is ice: for his charged attacks the harpoon frosts over (tu_harpoon_ice).

Rig (rigkit): the legs stand on their own; body (the hips) - head, arms, coat tails; the harpoon rides in his left fist.
Design units: feet at y=0, facing -z, his right +x; shown at RIG_SCALE (the follower - Leo's size) or BOSS_SCALE.
Faces: the head has a model per expression (tu_head_x<face>): sneer, fury, hurt, shock, tired, blink - the default is
his cold stare.
"""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc, _hair
from rigkit import qs, shrink, el, seg, chain, _add, _mul, _sub, _unit, I

PREFIX = 'tu_'
RIG_SCALE, BOSS_SCALE = 0.96, 1.4
PIVOT0 = {'body': (0, 13.4, 0), 'legr': (2.2, 13.4, 0), 'legl': (-2.2, 13.4, 0), 'tails': (0, 14.6, 0), 'head': (0, 26.0, 0),
          'armr': (5.9, 24.4, 0), 'arml': (-5.9, 24.4, 0), 'harpoon': (-6.3, 9.6, -0.3)}       # (the frame the parts are drawn in)
LIFT = 1.8                      # his legs are long (the art): everything above the hips stands LIFT higher, the stockings stretched to meet it
PIVOT = {k: (v[0], v[1] + LIFT, v[2]) for k, v in PIVOT0.items()}
LEG_TOP, SHOE = 13.6, 3.4
leg_y = lambda y: y if y <= SHOE else SHOE + (y - SHOE) * (LEG_TOP + LIFT - SHOE) / (LEG_TOP - SHOE)
PARENT = {'body': None, 'legr': None, 'legl': None, 'tails': 'body', 'head': 'body', 'armr': 'body', 'arml': 'body', 'harpoon': 'arml'}
PARTS = tuple(PIVOT)
HARPOON_K = 1.3                 # (the harpoon reaches past a model's box: built at full size, kept at 1/1.3, shown at 1.3x)
PART_K = {'harpoon': HARPOON_K}
FACES = ('sneer', 'fury', 'hurt', 'shock', 'tired', 'blink')
COAT, COAT_DK, COAT_LT = '#4c8a8f', '#2f5f63', '#7fbcbf'
BONE, BONE_DK, BONE_LT = '#8fc4cc', '#5a8f9a', '#c4e8ec'
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)


def HIDDEN(p, pose):
    return p == 'harpoon' and pose.get('_thrown')


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    ice = '_ice' if p == 'harpoon' and pose.get('_ice') else ''
    bent = '_bent' if p == 'armr' and pose.get('_bent') else ''
    return f'{PREFIX}{p}{face}{ice}{bent}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _noise(base, seed, var=8):
    rnd = random.Random(seed); b = hexc(base)[:3]; im = Image.new('RGBA', (64, 64))
    for y in range(64):
        for x in range(64):
            d = rnd.randint(-var, var)
            im.putpixel((x, y), tuple(max(0, min(255, v + d)) for v in b) + (255,))
    return im


def _folds(base, dark, light, seed, torn=None):
    """cloth: long folds (dark creases, a light edge beside each), grime; torn: darker ragged patches"""
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed + 1)
    for _ in range(4):
        x = rnd.randint(0, 63); x2 = x + rnd.randint(-5, 5)
        d.line((x, 0, x2, 63), fill=hexc(dark), width=1)
        d.line((x + 1, 0, x2 + 1, 63), fill=hexc(light), width=1)
    if torn:
        for _ in range(5):
            cx, cy = rnd.randint(4, 59), rnd.randint(4, 59); r = rnd.randint(2, 4)
            d.polygon([(cx - r, cy), (cx, cy - r - 1), (cx + r, cy + 1), (cx + 1, cy + r)], fill=hexc(torn))
    return im


def _shine(base, light, seed):
    """leather / stockings: a soft highlight streak down it"""
    im = _noise(base, seed, 4)
    for y in range(64):
        for x in range(18, 28):
            k = 1 - abs(x - 23) / 5
            p = im.getpixel((x, y))[:3]; L = hexc(light)[:3]
            im.putpixel((x, y), tuple(int(p[i] * (1 - 0.6 * k) + L[i] * 0.6 * k) for i in range(3)) + (255,))
    return im


def _bone(seed):
    """icy bone: pale blue, frost cracks"""
    im = _noise(BONE, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(5):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63)
        for _s in range(rnd.randint(6, 14)):
            nx, ny = x + rnd.choice((-2, -1, 1, 2)), y + rnd.randint(1, 3)
            d.line((x, y, nx, ny), fill=hexc(BONE_DK), width=1); x, y = nx, ny
    for _ in range(40):
        im.putpixel((rnd.randint(0, 63), rnd.randint(0, 63)), hexc(BONE_LT))
    return im


def _teeth(seed):
    im = _noise('#d8eef0', seed, 4); d = ImageDraw.Draw(im)
    for x in range(0, 64, 6): d.line((x, 0, x, 63), fill=hexc('#3a5a64'), width=1)
    d.line((0, 31, 63, 31), fill=hexc('#2a3a44'), width=2)
    return im


def _rope(seed):
    im = _noise('#7a5632', seed, 6); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 6): d.line((k, 0, k + 64, 64), fill=hexc('#4e3418'), width=2)
    return im


def _ice(seed, alpha=225):
    im = _noise('#bfeeff', seed, 10); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(6):
        x = rnd.randint(0, 63); d.line((x, 0, x + rnd.randint(-10, 10), 63), fill=(255, 255, 255, 255), width=1)
    px = im.load()
    for y in range(64):
        for x in range(64): px[x, y] = px[x, y][:3] + (alpha,)
    return im


def textures():
    return {'tu_coat': _folds(COAT, COAT_DK, COAT_LT, 801, torn='#3a6e72'), 'tu_coat_dk': _folds('#22484b', '#14302f', '#33605f', 802),
            'tu_cuff': _shine('#2b4749', '#5f8a8c', 803), 'tu_shirt': _folds('#2e5a2c', '#1c3a1a', '#467a40', 804, torn='#1a3018'),
            'tu_sash': _folds('#4f8f3f', '#356a2a', '#76b25e', 805), 'tu_stock': _shine('#4a8a3a', '#8cc870', 806),
            'tu_shoe': _shine('#1e4644', '#3f7470', 807), 'tu_sole': _noise('#0f2423', 808, 3), 'tu_glove': _shine('#16191b', '#3c4246', 809),
            'tu_bone': _bone(810), 'tu_bone_dk': _noise(BONE_DK, 811, 5), 'tu_socket': _noise('#070b0e', 812, 2), 'tu_pupil': _noise('#8af4ff', 813, 8),
            'tu_teeth': _teeth(814), 'tu_hair': _hair(815, ('#a8d4dc', '#c4e4ea', '#dcf2f6', '#eefafc', '#ffffff')),
            'tu_hat': _folds('#123a36', '#0a2422', '#1e5450', 816), 'tu_band': _folds('#3f8a3a', '#2a6026', '#5aa850', 817, torn='#24501f'),
            'tu_ice': _ice(818), 'tu_steel': _shine('#8a90b2', '#d6dcf4', 819), 'tu_shaft': _shine('#3a3d5a', '#6c709a', 820),
            'tu_rope': _rope(821), 'tu_gold': _noise('#e0b030', 822, 12), 'tu_emerald': _noise('#22c060', 823, 12),
            'tu_buckle': _shine('#bfe4f0', '#ffffff', 824), 'tu_strap': _noise('#6a8a94', 825, 6), 'tu_frost': _ice(826, 255)}


# ---------------------------------------------------------------------------------------------------- models
def _jag(x0, x1, y, z0, z1, n, h, tex, pv, seed):
    """a torn hem: n ragged teeth hanging below y"""
    rnd = random.Random(seed); out = []; w = (x1 - x0) / n
    for i in range(n):
        d = h * rnd.uniform(0.4, 1.0)
        out.append(el((x0 + i * w, y - d, z0), (x0 + (i + 1) * w + 0.05, y + 0.1, z1), tex, pv, shift=(0.3 * i, 0.6)))
    return out


def models():
    M = {}
    PIVOT = PIVOT0                                                                     # (drawn in the unlifted frame)
    def part(name, els, k=1.0):
        els = shrink(els, k) if k != 1.0 else els
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- legs: green stockings to the knee and on up under the coat, big rounded dark teal shoes
    def leg(sx):
        pv = globals()['PIVOT']['legr' if sx > 0 else 'legl']                          # (the lifted joint; the stocking stretched up to it)
        X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
        E = lambda a, b, y0, y1, z0, z1, t, sh=None: el((X(a, b)[0], leg_y(y0), z0), (X(a, b)[1], leg_y(y1), z1), t, pv, shift=sh)
        return [E(0.6, 3.8, 2.4, 13.6, -1.6, 1.6, 'tu_stock'), E(0.5, 3.9, 6.6, 8.0, -1.75, 1.7, 'tu_stock', (0.4, 0.2)),   # (the knee)
                E(0.3, 4.1, 0.4, 2.9, -3.1, 2.0, 'tu_shoe'), E(0.5, 3.9, 0.4, 2.4, -4.7, -3.0, 'tu_shoe', (0.5, 0.1)),        # shoe, round toe
                E(0.8, 3.6, 2.2, 3.2, -4.2, -3.0, 'tu_shoe', (0.2, 0.5)), E(0.2, 4.2, 0.0, 0.45, -4.8, 2.1, 'tu_sole'),
                E(0.4, 4.0, 2.7, 3.4, -1.9, 1.9, 'tu_shoe', (0.7, 0.7))]                                                   # (the cuff of it)
    part('tu_legr', leg(1)); part('tu_legl', leg(-1))

    # ---- body: a broad coat over a V-shaped chest, open at the throat on the torn green shirt; the lapels; the sash round
    #      his waist knotted at his left hip, its ends hanging; the icy buckle on its strap at his right; the high, spiky collar
    pv = PIVOT['body']; E = lambda fr, to, t='tu_coat', rot=None, sh=None: el(fr, to, t, pv, rot, shift=sh)
    body = [E((-4.2, 13.6, -2.5), (4.2, 19.6, 2.5), sh=(0.1, 0.2)), E((-4.9, 19.2, -2.7), (4.9, 25.4, 2.7), sh=(0.5, 0.4)),
            E((-5.5, 22.6, -2.6), (5.5, 26.0, 2.6), sh=(0.8, 0.1)),                                                          # the shoulders
            E((-2.2, 17.8, -2.85), (2.2, 25.0, -2.65), 'tu_shirt'),                                                          # the shirt in the V
            E((-1.3, 16.4, -2.85), (1.3, 17.9, -2.65), 'tu_shirt', None, (0.5, 0.5))]
    for sx in (1, -1):                                                                                                        # lapels, the V
        body.append(seg((sx * 2.4, 25.4, -2.9), (sx * 1.0, 16.8, -2.9), 1.5, 0.35, 'tu_coat_dk', pv, FRONT))
        body.append(seg((sx * 3.2, 25.2, -2.95), (sx * 1.9, 18.6, -2.95), 0.8, 0.3, 'tu_coat', pv, FRONT))
    body += _jag(-2.1, 2.1, 17.9, -2.95, -2.8, 6, 1.6, 'tu_shirt', pv, 830)                                                 # the shirt's torn edge
    body += [E((-4.45, 14.4, -2.85), (4.45, 16.9, 2.85), 'tu_sash'),                                                          # the sash
             E((-3.4, 14.0, -3.25), (-0.9, 17.3, -2.75), 'tu_sash', None, (0.4, 0.3))]                                       # its knot (his left)
    body += chain([(-2.6, 14.6, -3.2), (-2.9, 11.6, -3.3), (-2.5, 9.0, -3.25)], [1.5, 1.2], 0.35, 'tu_sash', pv, FRONT)       # the hanging ends
    body += chain([(-1.6, 14.6, -3.1), (-1.3, 12.2, -3.2), (-1.5, 10.2, -3.15)], [1.2, 0.9], 0.35, 'tu_sash', pv, FRONT)
    body += [seg((4.5, 13.4, -1.0), (2.2, 17.4, -2.95), 0.9, 0.3, 'tu_strap', pv, FRONT),                                    # the strap, the icy buckle
             E((2.6, 13.6, -3.15), (4.2, 15.4, -2.8), 'tu_buckle'), E((3.0, 14.0, -3.25), (3.8, 15.0, -3.1), 'tu_ice'),
             E((4.4, 12.4, -1.8), (5.2, 15.2, 1.2), 'tu_buckle', None, (0.6, 0.2))]                                          # (the pouch on his hip)
    # the collar: high round the back and sides of his neck, flaring out, ragged points along its top
    for sx in (1, -1):
        body += [seg((sx * 3.0, 25.6, 1.2), (sx * 4.4, 30.0, 2.2), 2.8, 0.5, 'tu_coat_dk', pv, (sx * 1.0, 0.0, 0.0)),
                 seg((sx * 3.2, 25.6, -1.6), (sx * 4.6, 29.0, -2.0), 2.6, 0.5, 'tu_coat_dk', pv, (sx * 1.0, 0.0, 0.0)),
                 seg((sx * 4.0, 29.6, 1.8), (sx * 5.4, 31.6, 2.6), 0.9, 0.45, 'tu_coat_dk', pv, (sx * 1.0, 0.0, 0.0)),       # its points
                 seg((sx * 4.3, 28.8, -1.9), (sx * 5.8, 30.4, -2.6), 0.9, 0.45, 'tu_coat_dk', pv, (sx * 1.0, 0.0, 0.0))]
    body += [seg((-3.0, 25.6, 2.6), (3.0, 25.6, 2.6), 4.4, 0.5, 'tu_coat_dk', pv, (0.0, 0.3, 1.0)),
             seg((0, 25.4, 2.7), (0, 30.4, 3.4), 6.2, 0.5, 'tu_coat_dk', pv, (0.0, 0.0, 1.0)),
             seg((-1.8, 30.0, 3.3), (-2.6, 31.8, 3.8), 0.9, 0.45, 'tu_coat_dk', pv, (0.0, 0.0, 1.0)),
             seg((1.8, 30.0, 3.3), (2.6, 31.8, 3.8), 0.9, 0.45, 'tu_coat_dk', pv, (0.0, 0.0, 1.0))]
    part('tu_body', body)

    # ---- the coat tails: the long skirt of the coat, open at the front, flaring to a torn hem above the knee
    pv = PIVOT['tails']; E = lambda fr, to, t='tu_coat', rot=None, sh=None: el(fr, to, t, pv, rot, shift=sh)
    tails = []
    for sx in (1, -1):                                                                                                        # front panels, splayed
        X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
        tails += [el((X(1.0, 4.6)[0], 7.8, -3.0), (X(1.0, 4.6)[1], 14.6, -2.55), 'tu_coat', pv, ('z', -6 * sx, (sx * 2.8, 14.6, -2.8)), shift=(0.2, 0.4)),
                  el((X(4.2, 4.8)[0], 7.8, -2.9), (X(4.2, 4.8)[1], 14.6, 2.9), 'tu_coat', pv, ('z', -9 * sx, (sx * 4.5, 14.6, 0)), shift=(0.6, 0.1))]
        tails += [el((X(4.1, 4.9)[0], 7.8, -2.9), (X(4.1, 4.9)[1], 8.4, 2.9), 'tu_coat_dk', pv, ('z', -9 * sx, (sx * 4.5, 14.6, 0)))]
    tails += [E((-4.7, 7.6, 2.5), (4.7, 14.6, 3.0), sh=(0.4, 0.6))]                                                         # the back
    for i, (x0, x1) in enumerate(((1.0, 4.6), (-4.6, -1.0))):
        tails += _jag(x0, x1, 7.85, -3.0, -2.6, 4, 1.8, 'tu_coat', pv, 840 + i)
    tails += _jag(-4.7, 4.7, 7.65, 2.5, 3.0, 8, 2.2, 'tu_coat', pv, 842)
    part('tu_tails', tails)

    # ---- arms: bulky sleeves, great dark cuffs, black gloves. (bent: the forearm folded up at the elbow - a hand to his hat brim)
    def arm(sx, fold=0.0):
        pv = PIVOT['armr' if sx > 0 else 'arml']; cx = 6.2
        X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
        fr = ((fold, 0.0, 0.0), (sx * cx, 18.8, 0.0)) if fold else None
        E = lambda a, b, y0, y1, z0, z1, t='tu_coat', sh=None, rot=None: el((X(a, b)[0], y0, z0), (X(a, b)[1], y1, z1), t, pv, rot, shift=sh)
        els = [E(cx - 2.4, cx + 2.4, 18.6, 26.4, -2.4, 2.4, sh=(0.2, 0.3)), E(cx - 2.6, cx + 2.2, 23.4, 26.6, -2.6, 2.6, sh=(0.7, 0.2)),   # sleeve, shoulder
               E(cx - 2.1, cx + 2.1, 14.0, 19.6 if fold else 18.8, -2.1, 2.1, sh=(0.5, 0.7), rot=fr),
               E(cx - 2.7, cx + 2.7, 11.2, 14.6, -2.7, 2.7, 'tu_cuff', rot=fr), E(cx - 2.8, cx + 2.8, 14.2, 14.8, -2.8, 2.8, 'tu_cuff', (0.5, 0.2), fr),
               E(cx - 1.8, cx + 1.8, 8.6, 11.4, -1.9, 1.7, 'tu_glove', rot=fr),                                             # the hand
               E(cx - 1.7, cx + 1.7, 7.6, 8.8, -1.9, 0.6, 'tu_glove', (0.3, 0.6), fr),                                       # fingers
               E(cx - 2.6, cx - 1.6, 9.0, 10.8, -1.6, -0.2, 'tu_glove', (0.7, 0.4), fr)]                                      # the thumb (inside)
        if fold: els.append(E(cx - 2.3, cx + 2.3, 16.8, 20.2, -2.3, 2.3, sh=(0.4, 0.4)))                                    # (the elbow, filled)
        return els
    part('tu_armr', arm(1)); part('tu_arml', arm(-1)); part('tu_armr_bent', arm(1, 128))

    # ---- the head (per face): a skull of icy bone, the jaw narrower; hollow sockets with a cold light deep in each; the
    #      nose's hole; teeth; frost-white hair spiking out under the hat; the emerald earring; the battered top hat
    def head(face=None):
        pv = PIVOT['head']; E = lambda fr, to, t='tu_bone', rot=None, sh=None: el(fr, to, t, pv, rot, shift=sh)
        h = [E((-1.4, 25.6, -1.4), (1.4, 27.4, 1.4), 'tu_bone_dk'),                                                         # the neck
             E((-3.6, 29.0, -3.5), (3.6, 34.4, 3.4), sh=(0.2, 0.2)), E((-2.9, 27.0, -3.2), (2.9, 29.2, 2.6), sh=(0.6, 0.5)),   # skull, jaw
             E((-3.2, 28.4, -3.3), (3.2, 29.2, 2.8), sh=(0.4, 0.8)),
             E((-1.8, 27.5, -3.62), (1.8, 28.7, -3.45), 'tu_teeth'),
             E((-0.55, 29.6, -3.66), (0.55, 30.3, -3.45), 'tu_socket'), E((-0.3, 30.3, -3.66), (0.3, 30.8, -3.45), 'tu_socket')]   # the nose
        for sx in (1, -1):
            X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
            h.append(E((X(2.2, 3.7)[0], 29.4, -3.8), (X(2.2, 3.7)[1], 30.5, -2.4), sh=(0.3, 0.3)))                           # cheekbones
        # the sockets and their light: per face, per side (brow tilt, brow height, socket top, pupil (dx, dy, size) or None)
        F = {None: ((10, 0.0, 32.0, (0.1, -0.1, 0.55)), (10, 0.0, 32.0, (0.1, -0.1, 0.55))),
             'sneer': ((-8, 0.5, 32.3, (0.3, 0.0, 0.5)), (16, -0.2, 31.5, (0.3, -0.2, 0.5))),
             'fury': ((24, -0.2, 31.7, (0.0, -0.2, 0.75)), (24, -0.2, 31.7, (0.0, -0.2, 0.75))),
             'hurt': ((16, 0.0, 31.8, (0.0, 0.0, 0.5)), (26, -0.4, 30.6, None)),
             'shock': ((-6, 0.6, 32.6, (0.0, 0.1, 0.35)), (-6, 0.6, 32.6, (0.0, 0.1, 0.35))),
             'tired': ((-4, -0.3, 31.2, (0.0, -0.3, 0.45)), (-4, -0.3, 31.2, (0.0, -0.3, 0.45))),
             'blink': ((6, 0.0, 30.6, None), (6, 0.0, 30.6, None))}[face]
        for sx in (1, -1):
            X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
            tilt, bh, top, pup = F[0 if sx > 0 else 1]
            t2 = max(30.75, top + 0.3)
            h += [E((X(0.45, 3.05)[0], 30.6, -3.62), (X(0.45, 3.05)[1], t2, -3.45), 'tu_socket'),                          # the hollow socket, rounded below
                  E((X(0.8, 2.7)[0], 30.0, -3.62), (X(0.8, 2.7)[1], 30.7, -3.45), 'tu_socket'),
                  E((X(1.2, 2.3)[0], 29.75, -3.62), (X(1.2, 2.3)[1], 30.1, -3.45), 'tu_socket')]
            if top < 30.8: h.append(E((X(0.5, 3.0)[0], 30.5, -3.72), (X(0.5, 3.0)[1], t2 + 0.1, -3.6), 'tu_bone', None, (0.3, 0.6)))   # (shut: bone over it)
            if top < 30.8: h.append(E((X(0.7, 2.8)[0], 30.25, -3.74), (X(0.7, 2.8)[1], 30.5, -3.62), 'tu_bone_dk'))       # (and a seam)
            h.append(E((X(2.0, 3.55)[0], 28.5, -3.5), (X(2.0, 3.55)[1], 29.4, -3.3), 'tu_bone_dk'))                         # the hollow under his cheekbone
            if pup:
                dx, dy, sz = pup; px, py = sx * (1.7 + dx * sx), 31.0 + dy
                h.append(el((px - sz / 2, py - sz / 2, -3.68), (px + sz / 2, py + sz / 2, -3.6), 'tu_pupil', pv, light=12))
            h.append(E((X(0.2, 3.4)[0], 32.0 + bh, -3.85), (X(0.2, 3.4)[1], 33.0 + bh, -3.4), 'tu_bone', ('z', tilt * sx, (sx * 1.8, 32.0 + bh, -3.6)), (0.5, 0.4)))   # the brow ridge
        # hair: frost-white spikes out under the hat, at the sides and behind
        for sx in (1, -1):
            for (y, z, dx, dy, dz, w) in ((33.2, -1.6, 1.8, 0.4, 0.6, 1.4), (32.4, 0.4, 2.2, -0.4, 1.0, 1.6), (33.4, 2.0, 1.6, 0.2, 1.8, 1.4),
                                         (31.4, 1.6, 1.4, -1.2, 1.4, 1.2)):
                b0 = (sx * 3.4, y, z)
                h += chain([b0, (b0[0] + sx * dx * 0.6, y + dy * 0.6, z + dz * 0.6), (b0[0] + sx * dx, y + dy, z + dz)], [w, w * 0.5], w * 0.8, 'tu_hair', pv, UP, 0.2)
        for (x, y, dy, dz) in ((-2.0, 32.4, -1.6, 2.2), (0.0, 32.8, -2.0, 2.6), (2.0, 32.4, -1.4, 2.0), (-1.0, 30.8, -2.2, 1.6), (1.2, 30.6, -2.0, 1.8)):
            b0 = (x, y, 3.3)
            h += chain([b0, (x, y + dy * 0.5, 3.3 + dz * 0.6), (x * 1.1, y + dy, 3.3 + dz)], [1.5, 0.7], 1.1, 'tu_hair', pv, FRONT, 0.2)
        # the emerald earring (his left ear)
        h += [E((-3.85, 30.0, 0.2), (-3.55, 30.6, 0.8), 'tu_gold'), E((-4.0, 28.7, 0.25), (-3.6, 30.0, 0.75), 'tu_emerald'),
              E((-3.95, 28.4, 0.35), (-3.65, 28.75, 0.65), 'tu_gold')]
        # the hat: tipped a little to his right and back (as the art) - brim with its sides curled up, the tall crown flaring
        # at the top, the torn green band, the cluster of ice crystals at his left. Built upright, then the whole of it turned
        hc = (0.0, 34.0, 0.2); ca, sa = math.cos(math.radians(4)), math.sin(math.radians(4)); cb, sb = math.cos(math.radians(-6)), math.sin(math.radians(-6))
        def R(v):                                                                       # (Rz(-6) Rx(+4))
            x, y, z = v; y, z = y * ca - z * sa, y * sa + z * ca
            return (x * cb - y * sb, x * sb + y * cb, z)
        tilt = lambda q: _add(hc, R(_sub(q, hc)))
        HS = lambda A, B, w, hh, t, up, sh=None, light=0: seg(tilt(A), tilt(B), w, hh, t, pv, R(up), 0.0, light=light, shift=sh)
        out = [HS((0, 34.05, -5.6), (0, 34.05, 5.6), 11.0, 0.7, 'tu_hat', UP),                                         # the brim
               HS((0, 34.2, 0), (0, 42.6, 0), 7.8, 7.6, 'tu_hat', FRONT, (0.3, 0.4)),                                     # the crown
               HS((0, 42.0, 0), (0, 43.6, 0), 8.5, 8.3, 'tu_hat', FRONT, (0.7, 0.2)),                                     # its flared top
               HS((0, 34.3, 0), (0, 36.2, 0), 8.0, 7.8, 'tu_band', FRONT),                                               # the band
               HS((2.0, 34.3, -3.94), (2.0, 36.1, -3.94), 1.2, 0.1, 'tu_hat', FRONT)]                                    # (the tear in it)
        c28, s28 = math.cos(math.radians(28)), math.sin(math.radians(28))
        out += [HS((5.5 + 0.6 * c28, 34.05 + 0.6 * s28, -5.0), (5.5 + 0.6 * c28, 34.05 + 0.6 * s28, 5.0), 1.3, 0.7, 'tu_hat', (-s28, c28, 0.0), (0.5, 0.5)),
                HS((-5.5 - 0.6 * c28, 34.05 + 0.6 * s28, 5.0), (-5.5 - 0.6 * c28, 34.05 + 0.6 * s28, -5.0), 1.3, 0.7, 'tu_hat', (s28, c28, 0.0), (0.5, 0.5))]
        for (y0, dx, dy, dz, w) in ((35.2, -2.6, 3.6, -0.6, 1.0), (35.0, -3.0, 2.2, 0.8, 0.9), (35.4, -1.8, 4.4, 0.6, 0.8), (34.8, -2.4, 1.2, -1.4, 0.8)):
            b0 = (-3.9, y0, -0.4)                                                                                         # ice crystals, out of the band
            out.append(HS(b0, (b0[0] + dx, b0[1] + dy, b0[2] + dz), w, w, 'tu_ice', FRONT, None, 6))
        h += out
        return h
    part('tu_head', head())
    for f in FACES:
        part(f'tu_head_x{f}', head(f))

    # ---- the harpoon (its joint is his grip; the head points along -z): a long shaft of dark sea-iron, a grip wrapped in
    #      rope, a collar, a long barbed head; the rope tied at the collar, wound down the shaft and hanging in a loop
    def harpoon(ice=False):
        g = (0.0, 0.0, 0.0); S = lambda A, B, w, h, t, up=UP, ext=0.1, light=0: seg(A, B, w, h, t, g, up, ext, light=light)
        els = [S((0, 0, 9.4), (0, 0, -20.0), 0.85, 0.85, 'tu_shaft'), S((0, 0, 10.2), (0, 0, 9.2), 1.2, 1.2, 'tu_shaft'),      # shaft, butt cap
               S((0, 0, 2.2), (0, 0, -2.2), 1.15, 1.15, 'tu_rope'),                                                           # the grip
               S((0, 0, -19.6), (0, 0, -21.2), 1.5, 1.5, 'tu_steel'), S((0, 0, -21.0), (0, 0, -22.4), 1.0, 1.0, 'tu_steel')]    # the collar, socket
        els += [S((0, 0, -22.2), (0, 0, -27.6), 1.9, 0.5, 'tu_steel'), S((0, 0, -27.4), (0, 0, -29.6), 1.1, 0.45, 'tu_steel'),   # the blade
                S((0, 0, -29.4), (0, 0, -30.4), 0.5, 0.4, 'tu_steel')]
        for sx in (1, -1):                                                                                                    # barbs, swept back
            els += [S((sx * 0.6, 0, -25.6), (sx * 2.4, 0, -23.2), 0.7, 0.45, 'tu_steel', UP), S((sx * 2.4, 0, -23.2), (sx * 2.9, 0, -22.0), 0.4, 0.4, 'tu_steel', UP),
                    S((sx * 0.5, 0, -22.6), (sx * 1.6, 0, -21.0), 0.5, 0.4, 'tu_steel', UP)]
        for z in (-18.8, -15.6, -12.4, -9.2):                                                                                 # the rope, wound on the shaft
            els.append(S((0, 0, z + 0.3), (0, 0, z - 0.3), 1.2, 1.2, 'tu_rope'))
        els += chain([(0.4, -0.3, -19.0), (1.6, -1.6, -16.0), (2.2, -2.6, -11.0), (1.8, -2.4, -5.0), (0.8, -0.8, 1.6)], [0.5, 0.5, 0.5, 0.5], 0.5, 'tu_rope', g, UP)   # its loose run
        els += chain([(0.0, -0.4, 9.6), (0.6, -2.6, 10.6), (0.4, -4.4, 9.4), (-0.4, -4.0, 7.2), (-0.2, -1.6, 6.6)], [0.5, 0.5, 0.5, 0.5], 0.5, 'tu_rope', g, UP)  # the loop off the end
        if ice:                                                                                                               # charged: frost on the head and shaft
            rnd = random.Random(860)
            for _ in range(12):
                z = rnd.uniform(-29.0, -12.0); a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.4, 0.9)
                b0 = (math.cos(a) * r, math.sin(a) * r, z); tip = (math.cos(a) * (r + rnd.uniform(1.2, 2.6)), math.sin(a) * (r + rnd.uniform(1.2, 2.6)), z + rnd.uniform(0.4, 1.6))
                els.append(S(b0, tip, rnd.uniform(0.5, 0.9), rnd.uniform(0.5, 0.9), 'tu_ice', UP, 0.2, light=9))
            els.append(S((0, 0, -21.0), (0, 0, -31.6), 2.6, 1.2, 'tu_ice', UP, 0.0, light=9))                               # (the blade sheathed in ice)
        return els
    part('tu_harpoon', harpoon(), HARPOON_K); part('tu_harpoon_ice', harpoon(True), HARPOON_K)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# Display-frame rotations, as Apophiss's: body +x leans forward, +y turns to his left, +z rolls to his right; a limb (arm or
# leg) swings forward with -x, out to his side with -z (right) / +z (left); head +x nods. The harpoon's own turn is from
# pointing straight ahead out of his fist: -y swings its head toward his right, +x dips it, -x raises it.
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


# The harpoon's turn is given as where it points in the world (_hw: from straight ahead of him); its turn in his fist is
# worked out from his body and left arm, so the harpoon holds its aim whatever the arm does.
CARRY = qs(('y', -62), ('x', 14))                       # (the art: held low across his body, the head toward his right foot)
UPRIGHT = qs(('x', -84))                                # (stood on its butt like a staff, head up)
AHEAD = qs(('x', -3))                                   # (levelled at you)
POSES = {
    # idle: chin up, contemptuous; the harpoon held low across him; his free hand flexing
    'idle_a': P(body=qs(('y', 6)), head=qs(('x', -12), ('z', -4)), armr=limb(1, 2, 8), arml=limb(-1, 18, 6), _hw=CARRY, legr=limb(1, -2, 3), legl=limb(-1, 3, 3)),
    'idle_b': P(_off=(0, -0.1, 0), body=qs(('y', 4), ('x', 2)), head=qs(('x', -8), ('z', -2), ('y', -6)), armr=limb(1, 6, 10), arml=limb(-1, 20, 6), _hw=CARRY,
                legr=limb(1, -2, 3), legl=limb(-1, 3, 3), tails=qs(('x', -2))),
    # walk: a long stride, the harpoon carried at his side, coat tails swinging
    'walk_a': P(body=qs(('y', 6), ('z', 2)), head=qs(('x', -8), ('y', -4)), legr=limb(1, 26), legl=limb(-1, -24), armr=limb(1, -22, 6), arml=limb(-1, 14, 6),
                _hw=qs(('y', -12), ('x', 10)), tails=qs(('x', -8))),
    'walk_b': P(body=qs(('y', -6), ('z', -2)), head=qs(('x', -8), ('y', 4)), legr=limb(1, -24), legl=limb(-1, 26), armr=limb(1, 24, 6), arml=limb(-1, -8, 6),
                _hw=qs(('y', -12), ('x', 14)), tails=qs(('x', -8))),
    # on guard: feet wide, side-on (left shoulder to you), the harpoon levelled at you, his right hand forward on the shaft
    'guard': P(_off=(0, -0.6, 0), body=qs(('y', 34), ('x', 6)), head=qs(('y', -30), ('x', -4)), legr=limb(1, -22, 10), legl=limb(-1, 24, 8),
               armr=limb(1, 64, -24), arml=limb(-1, 42, 14), _hw=AHEAD, tails=qs(('x', -6))),
    # the thrust: drawn back, then driven straight in
    'thrust_back': P(_off=(0, -0.4, 0), body=qs(('y', 44), ('x', -4)), head=qs(('y', -40)), legr=limb(1, -26, 10), legl=limb(-1, 26, 8),
                     armr=limb(1, 30, 30), arml=limb(-1, -10, 24), _hw=AHEAD, tails=qs(('x', 4))),
    'thrust': P(_off=(0, -0.9, -1.0), body=qs(('y', 16), ('x', 14)), head=qs(('y', -14), ('x', -10)), legr=limb(1, -34, 8), legl=limb(-1, 40, 6),
                armr=limb(1, -30, 30), arml=limb(-1, 84, 2), _hw=qs(('x', 2)), tails=qs(('x', -16))),
    # the throw: the harpoon raised back over his left shoulder, aimed - then hurled (the rope pays out after it)
    'throw_back': P(body=qs(('y', 30), ('x', -10)), head=qs(('y', -26), ('x', -6)), legr=limb(1, 22, 8), legl=limb(-1, -20, 6), armr=limb(1, 50, -10),
                    arml=limb(-1, 160, 14), _hw=qs(('x', -18)), tails=qs(('x', 6))),
    'throw': P(_off=(0, -0.5, 0), body=qs(('y', -20), ('x', 16)), head=qs(('y', 16), ('x', -10)), legr=limb(1, 30, 8), legl=limb(-1, -26, 6),
               armr=limb(1, -30, 20), arml=limb(-1, 70, -6), _thrown=True, tails=qs(('x', -14))),
    # ice: frost gathered in his right hand, the harpoon stood beside him
    'ice_cast': P(_face='fury', body=qs(('y', -14), ('x', -4)), head=qs(('y', 10), ('x', -6)), legr=limb(1, 14, 8), legl=limb(-1, -10, 6),
                  armr=limb(1, 96, -4), arml=limb(-1, 10, 12), _hw=qs(('x', -84), ('z', 8))),
    # the charged strike (the harpoon frosts over): raised high in both hands, then driven down into the ground before him
    'slam_up': P(_ice=True, _face='fury', body=qs(('x', -12)), head=qs(('x', -14)), legr=limb(1, -10, 10), legl=limb(-1, 14, 10),
                 armr=limb(1, 160, -12), arml=limb(-1, 166, -16), _hw=qs(('x', -130)), tails=qs(('x', 6))),
    'slam_mid': P(_ice=True, _face='fury', _off=(0, -1.0, -0.4), body=qs(('x', 12)), head=qs(('x', -18)), legr=limb(1, -20, 11), legl=limb(-1, 32, 10),
                  armr=limb(1, 118, -16), arml=limb(-1, 122, -16), _hw=qs(('x', -34)), tails=qs(('x', -8))),
    'slam': P(_ice=True, _face='fury', _off=(0, -2.6, -1.0), body=qs(('x', 36)), head=qs(('x', -26)), legr=limb(1, -30, 12), legl=limb(-1, 50, 10),
              armr=limb(1, 66, -18), arml=limb(-1, 70, -16), _hw=qs(('x', 62)), tails=qs(('x', -24))),
    # tired: hunched, leaning his weight on the harpoon stood beside him
    'tired': P(_face='tired', _off=(0, -0.6, 0), body=qs(('x', 18), ('z', -6)), head=qs(('x', -8), ('z', 8)), legr=limb(1, 10, 6), legl=limb(-1, -6, 4),
               armr=limb(1, -4, 4), arml=limb(-1, 26, 14), _hw=qs(('x', -80), ('z', -10)), tails=qs(('x', -6))),
    # the taunt: a tip of the hat with his free hand (the bent arm), the sneer
    'taunt': P(_face='sneer', _bent=True, body=qs(('y', 10), ('x', -2)), head=qs(('x', -6), ('z', -8)), legr=limb(1, 6, 4), legl=limb(-1, -4, 4),
               armr=qs(('z', -40), ('x', -40), ('y', -40)), arml=limb(-1, 18, 6), _hw=CARRY),
    # sit (a follower at rest): on the ground, one knee up, the harpoon leant against his shoulder
    'sit': P(_off=(0, -13.0, 0), body=qs(('x', -12)), head=qs(('x', -2), ('y', 16)), legr=limb(1, 88, 6), legl=limb(-1, 60, 8), armr=limb(1, 40, 14),
             arml=limb(-1, 10, 22), _hw=qs(('x', -66), ('z', 16)), tails=qs(('x', -72))),
    # beaten: slumped where he fell, head bowed, the harpoon fallen beside him - the moment you can offer him a place
    'defeated': P(_face='hurt', _off=(0, -13.0, 0), body=qs(('x', 26), ('z', 6)), head=qs(('x', 30), ('z', 10)), legr=limb(1, 84, 10), legl=limb(-1, 80, 12),
                  armr=limb(1, 6, 10), arml=limb(-1, 34, 26), _hw=qs(('y', -30), ('x', 4)), tails=qs(('x', -70))),
}
from rigkit import qmul as _qm
_conj = lambda q: (-q[0], -q[1], -q[2], q[3])
for _p in POSES.values():                      # (the harpoon's world aim -> its turn in his left fist)
    if '_hw' in _p:
        _p['harpoon'] = _qm(_conj(_qm(_p.get('body', I), _p.get('arml', I))), _p['_hw'])
DRAFT = ['idle_a', 'walk_a', 'guard', 'thrust_back', 'thrust', 'throw_back', 'throw', 'ice_cast', 'slam_up', 'slam', 'tired', 'taunt', 'sit', 'defeated']
ANIMS = {'idle': [('idle_a', 30), ('idle_b', 30)], 'walk': [('walk_a', 8), ('walk_b', 8)], 'thrust': [('guard', 8), ('thrust_back', 8), ('thrust', 4), ('guard', 10)],
         'throw': [('guard', 8), ('throw_back', 10), ('throw', 4), ('guard', 12)], 'slam': [('guard', 8), ('slam_up', 14), ('slam_mid', 3), ('slam', 3), ('slam', 8), ('guard', 12)],
         'taunt': [('idle_a', 8), ('taunt', 10), ('taunt', 12), ('idle_a', 10)]}


def rp(R):
    import sys as _s
    R.TEXTURE_MODS.append(_s.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
