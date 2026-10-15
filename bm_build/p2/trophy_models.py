"""2.79a: the dungeon bosses' trophies - each boss in miniature, the way the follower dolls are the followers.

Every boss is a vanilla mob in its own gear, so each trophy is built from that mob's real shape (the game's own boxes, part for
part) wearing the game's own skin - the spider's, the stray's with its ragged overlay, the drowned's with its kelp layer, the
evoker's robe, the wither skeleton's, the warm chicken's - pulled into the block atlas, not copied. On it goes the boss's real
gear: the Frost Marksman's diamond helm and chainmail, the Tyrant's gold helm, Bobbery's netherite, the Hollow King's
netherite and crown; and in its hands the boss's weapon, the item's own sprite (bow, trident, axe, sword). Then it's pushed
into the dolls' chibi proportions (the head bigger about the neck, the body smaller about the hips, the legs shorter) and set
in a pose that is that boss's moment, on a trophy plinth: a stepped base in the dungeon's stone, a gold rim, a gold plaque on
the front. So it's the boss, small - and still plainly a trophy.

Front = model north (the trophy is turned to face whoever sets it down). Built in mob units (one texel of the mob's skin, y up
from the feet, the mob facing -z, its right side +x), then fitted onto the plinth."""
import math
import numpy as np

SKIN = {'spider': 'minecraft:entity/spider/spider', 'stray': 'minecraft:entity/skeleton/stray',
        'stray_o': 'minecraft:entity/skeleton/stray_overlay', 'wither': 'minecraft:entity/skeleton/wither_skeleton',
        'drowned': 'minecraft:entity/zombie/drowned', 'drowned_o': 'minecraft:entity/zombie/drowned_outer_layer',
        'evoker': 'minecraft:entity/illager/evoker', 'chicken': 'minecraft:entity/chicken/chicken_warm',
        'a_diamond': 'minecraft:entity/equipment/humanoid/diamond', 'a_gold': 'minecraft:entity/equipment/humanoid/gold',
        'a_chain': 'minecraft:entity/equipment/humanoid/chainmail', 'a_neth': 'minecraft:entity/equipment/humanoid/netherite',
        'l_neth': 'minecraft:entity/equipment/humanoid_leggings/netherite',
        'i_bow': 'minecraft:item/bow', 'i_trident': 'minecraft:item/trident', 'i_axe': 'minecraft:item/netherite_axe',
        'i_sword': 'minecraft:item/netherite_sword', 'i_bone': 'minecraft:item/bone'}
SIZE = {'drowned': (64, 64), 'drowned_o': (64, 64), 'evoker': (64, 64)}            # (the rest are 64 x 32)
BLOCK = {'mc': 'minecraft:block/mossy_cobblestone', 'mo': 'minecraft:block/moss_block', 'pi': 'minecraft:block/packed_ice',
         'sn': 'minecraft:block/snow', 'dp': 'minecraft:block/dark_prismarine', 'pr': 'minecraft:block/prismarine',
         'pb': 'minecraft:block/polished_blackstone', 'pu': 'minecraft:block/purpur_block', 'nb': 'minecraft:block/nether_bricks',
         'pd': 'minecraft:block/polished_deepslate', 'gc': 'minecraft:block/green_concrete', 'em': 'minecraft:block/emerald_block',
         'y': 'minecraft:block/gold_block', 'cw': 'minecraft:block/cobweb', 'wr': 'minecraft:block/wither_rose',
         'am': 'minecraft:block/amethyst_cluster', 'go': 'minecraft:block/raw_gold_block', 'tc': 'minecraft:block/tube_coral'}
ATLAS = [v for k, v in SKIN.items()]                  # (the entity skins and the item sprites the block atlas must carry)


def Rx(a):
    a = math.radians(a); c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    a = math.radians(a); c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def Rz(a):
    a = math.radians(a); c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _euler(R):
    """R = Rz Ry Rx -> (x, y, z) degrees (the element rotation's order)"""
    b = math.asin(max(-1.0, min(1.0, -R[2][0])))
    if abs(math.cos(b)) > 1e-6:
        a = math.atan2(R[2][1], R[2][2]); c = math.atan2(R[1][0], R[0][0])
    else:
        a = math.atan2(-R[1][2], R[1][1]); c = 0.0
    return math.degrees(a), math.degrees(b), math.degrees(c)


def uv(skin, u, v, w, h, d, mirror=False):
    """a box's faces on its skin (the game's box layout) -> item-model uvs (0..16 across the sheet)"""
    tw, th = SIZE.get(skin, (64, 32))
    U = lambda a, b, c, e: [a * 16 / tw, b * 16 / th, c * 16 / tw, e * 16 / th]
    f = {'north': U(u + d, v + d, u + d + w, v + d + h), 'south': U(u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h),
         'east': U(u, v + d, u + d, v + d + h), 'west': U(u + d + w, v + d, u + 2 * d + w, v + d + h),
         'up': U(u + d, v, u + d + w, v + d), 'down': U(u + d + w, v + d, u + d + 2 * w, v)}
    if mirror:
        f['east'], f['west'] = f['west'], f['east']
        for k in f: a, b, c, e = f[k]; f[k] = [c, b, a, e]
    return f


class Fig:
    """a boss's parts: boxes on its skin (or block-textured), each with a group for the chibi warp and a turn about a pivot"""
    def __init__(self):
        self.parts = []

    def box(self, skin, lo, hi, uvs, group, R=None, pivot=None, grow=0.0):
        lo, hi = np.array(lo, float) - grow, np.array(hi, float) + grow
        faces = {k: {'uv': [round(x, 4) for x in v], 'texture': '#' + skin} for k, v in uvs.items()}
        self.parts.append(dict(lo=lo, hi=hi, faces=faces, group=group, R=np.eye(3) if R is None else R,
                               pivot=(lo + hi) / 2 if pivot is None else np.array(pivot, float), item=False))

    def sprite(self, tex, center, size, group, R=None, flip=False, item=True):
        """an item's own sprite, flat (no depth), facing north and south; R turns it about its centre"""
        c = np.array(center, float); h = size / 2
        n, s = ([16, 0, 0, 16], [0, 0, 16, 16]) if flip else ([0, 0, 16, 16], [16, 0, 0, 16])
        faces = {'north': {'uv': n, 'texture': '#' + tex}, 'south': {'uv': s, 'texture': '#' + tex}}
        self.parts.append(dict(lo=c - [h, h, 0], hi=c + [h, h, 0], faces=faces, group=group, R=np.eye(3) if R is None else R,
                               pivot=c, item=item))

    def cross(self, tex, center, size, group, item=False):
        """a plant's two crossed planes (a cobweb, a rose, a crystal)"""
        for a in (45, -45):
            self.sprite(tex, center, size, group, Ry(a), item=item)

    @staticmethod
    def at(local, R, pivot):
        """where a point of a turned part ends up"""
        p = np.array(pivot, float)
        return p + R @ (np.array(local, float) - p)


def humanoid(f, skin, *, arms=4, wide=True, left64=False, hat=False, poses=None, over=None, over_grow=0.25):
    """the game's humanoid (zombie / skeleton) at rest - legs, body, arms, head - its arms turned by poses {'r': R, 'l': R}.
    arms: their width (4 a zombie's, 2 a skeleton's); left64: a 64x64 skin with its own left limbs; over: an outer-layer skin."""
    poses = poses or {}
    lw = 4 if wide else 2
    for sk, g in ((skin, 0.0),) + (((over, over_grow),) if over else ()):
        f.box(sk, (0, 0, -lw / 2), (lw, 12, lw / 2), uv(sk, 0, 16, lw, 12, lw), 'legs', grow=g) if wide else \
            f.box(sk, (1, 0, -1), (3, 12, 1), uv(sk, 0, 16, 2, 12, 2), 'legs', grow=g)
        lu = (uv(sk, 16, 48, 4, 12, 4) if left64 else uv(sk, 0, 16, lw, 12, lw, True))
        f.box(sk, (-lw, 0, -lw / 2), (0, 12, lw / 2), lu, 'legs', grow=g) if wide else \
            f.box(sk, (-3, 0, -1), (-1, 12, 1), uv(sk, 0, 16, 2, 12, 2, True), 'legs', grow=g)
        f.box(sk, (-4, 12, -2), (4, 24, 2), uv(sk, 16, 16, 8, 12, 4), 'body', grow=g)
        sx = 4 + arms / 2 if arms == 4 else 5
        f.box(sk, (4, 12, -arms / 2), (4 + arms, 24, arms / 2), uv(sk, 40, 16, arms, 12, arms), 'body',
              poses.get('r'), (sx, 22, 0), grow=g)
        la = uv(sk, 32, 48, 4, 12, 4) if left64 else uv(sk, 40, 16, arms, 12, arms, True)
        f.box(sk, (-4 - arms, 12, -arms / 2), (-4, 24, arms / 2), la, 'body', poses.get('l'), (-sx, 22, 0), grow=g)
        f.box(sk, (-4, 24, -4), (4, 32, 4), uv(sk, 0, 0, 8, 8, 8), 'head', grow=g)
        if hat:
            f.box(sk, (-4, 24, -4), (4, 32, 4), uv(sk, 32, 0, 8, 8, 8), 'head', grow=g + 0.5)


def armour(f, *, helm=None, chest=None, legs=None, boots=None, poses=None, skinny=True):
    """the game's armour layer: the helmet and chestplate (and boots) grown 1 about the head, body and arms; the leggings 0.5"""
    poses = poses or {}
    sx = 5 if skinny else 6
    if helm:
        f.box(helm, (-4, 24, -4), (4, 32, 4), uv(helm, 0, 0, 8, 8, 8), 'head', grow=1.0)
    if chest:
        f.box(chest, (-4, 12, -2), (4, 24, 2), uv(chest, 16, 16, 8, 12, 4), 'body', grow=1.0)
        f.box(chest, (4, 12, -2), (8, 24, 2), uv(chest, 40, 16, 4, 12, 4), 'body', poses.get('r'), (sx, 22, 0), grow=1.0)
        f.box(chest, (-8, 12, -2), (-4, 24, 2), uv(chest, 40, 16, 4, 12, 4, True), 'body', poses.get('l'), (-sx, 22, 0), grow=1.0)
    if legs:
        f.box(legs, (-4, 12, -2), (4, 24, 2), uv(legs, 16, 16, 8, 12, 4), 'body', grow=0.5)
        f.box(legs, (0, 0, -2), (4, 12, 2), uv(legs, 0, 16, 4, 12, 4), 'legs', grow=0.5)
        f.box(legs, (-4, 0, -2), (0, 12, 2), uv(legs, 0, 16, 4, 12, 4, True), 'legs', grow=0.5)
    if boots:
        f.box(boots, (0, 0, -2), (4, 12, 2), uv(boots, 0, 16, 4, 12, 4), 'legs', grow=1.0)
        f.box(boots, (-4, 0, -2), (0, 12, 2), uv(boots, 0, 16, 4, 12, 4, True), 'legs', grow=1.0)


def hand(R, pivot, x):
    """the fist of an arm hanging from (x, 22) - where it ends up turned by R"""
    return Fig.at((x, 12.5, 0), R, pivot)


def bake(f, warp, height=12.5, width=11.0, base=3.5, turn=0.0):
    """the parts warped (chibi), turned on the plinth by turn (degrees about the upright), fitted on it (feet at base, centred
    on 8 8), as item-model elements"""
    T = Ry(turn)
    def W(g, p):
        k, c0, c1 = warp.get(g, (1.0, np.zeros(3), np.zeros(3)))
        return T @ (np.array(c1) + k * (np.array(p) - np.array(c0)))
    pts, figpts = [], []
    for e in f.parts:
        for x in (e['lo'][0], e['hi'][0]):
            for y in (e['lo'][1], e['hi'][1]):
                for z in (e['lo'][2], e['hi'][2]):
                    q = W(e['group'], Fig.at((x, y, z), e['R'], e['pivot']))
                    pts.append(q)
                    if not e['item']: figpts.append(q)
    pts, figpts = np.array(pts), np.array(figpts)
    lo, hi = figpts.min(0), figpts.max(0)
    alo, ahi = pts.min(0), pts.max(0)
    S = min(height / (hi[1] - lo[1]), width / max(ahi[0] - alo[0], ahi[2] - alo[2]))
    cx, cz = (alo[0] + ahi[0]) / 2, (alo[2] + ahi[2]) / 2
    fit = lambda w: np.array([8 + (w[0] - cx) * S, base + (w[1] - lo[1]) * S, 8 + (w[2] - cz) * S])
    els = []
    for e in f.parts:
        k = warp.get(e['group'], (1.0,))[0]
        qm = fit(W(e['group'], e['pivot']))
        a, b = (e['lo'] - e['pivot']) * k * S, (e['hi'] - e['pivot']) * k * S
        el = {'from': [round(float(v), 4) for v in qm + a], 'to': [round(float(v), 4) for v in qm + b], 'faces': e['faces']}
        x, y, z = _euler(T @ e['R'])
        if max(abs(x), abs(y), abs(z)) > 1e-3:
            el['rotation'] = {'origin': [round(float(v), 4) for v in qm], 'x': round(x, 3), 'y': round(y, 3), 'z': round(z, 3)}
        els.append(el)
    top = max(max(el['from'][1], el['to'][1]) for el in els)
    assert top < 32 and min(min(el['from'][1], el['to'][1]) for el in els) > -16, top
    return els


def chibi(neck=24.0, hip=12.0, kh=1.5, kb=0.82, kl=0.62):
    """the dolls' proportions: the head grown about the neck, the body shrunk about the hips, the legs shortened from the ground"""
    hip1 = hip * kl
    neck1 = hip1 + (neck - hip) * kb
    return {'legs': (kl, (0, 0, 0), (0, 0, 0)), 'body': (kb, (0, hip, 0), (0, hip1, 0)), 'head': (kh, (0, neck, 0), (0, neck1, 0))}


def plinth(base, top):
    """the trophy's stand: a stepped base in the dungeon's stone, a gold rim, its top, and a gold plaque on the front"""
    def blk(lo, hi, t):
        (x1, y1, z1), (x2, y2, z2) = lo, hi
        uv = {'north': [16 - x2, 16 - y2, 16 - x1, 16 - y1], 'south': [x1, 16 - y2, x2, 16 - y1], 'east': [16 - z2, 16 - y2, 16 - z1, 16 - y1],
              'west': [z1, 16 - y2, z2, 16 - y1], 'up': [x1, z1, x2, z2], 'down': [x1, 16 - z2, x2, 16 - z1]}       # (as the game would give them)
        return {'from': list(lo), 'to': list(hi), 'faces': {k: {'uv': v, 'texture': '#' + t} for k, v in uv.items()}}
    return [blk((1.5, 0, 1.5), (14.5, 1.5, 14.5), base), blk((2.5, 1.5, 2.5), (13.5, 2.0, 13.5), 'y'),
            blk((3, 2.0, 3), (13, 3.5, 13), top), blk((5, 0.35, 1.4), (11, 1.15, 1.5), 'y')]


# ---------------------------------------------------------------------------------------------------------- the bosses
def brood():
    """The Broodmother: the spider herself, head reared, every leg planted; webs at her back, a gnawed bone at her feet"""
    f = Fig()
    f.box('spider', (-3, 6, -3), (3, 12, 3), uv('spider', 0, 0, 6, 6, 6), 'body')                                  # (her neck)
    f.box('spider', (-5, 5, 3), (5, 13, 15), uv('spider', 0, 12, 10, 8, 12), 'body', Rx(-12), (0, 9, 3))            # abdomen
    f.box('spider', (-4, 5, -11), (4, 13, -3), uv('spider', 32, 4, 8, 8, 8), 'head', Rx(10), (0, 9, -3))            # head (reared)
    for zp, phi, th in ((2, -45, 38), (1, -20, 30), (0, 20, 30), (-1, 45, 38)):
        f.box('spider', (3, 8, zp - 1), (19, 10, zp + 1), uv('spider', 18, 0, 16, 2, 2), 'body', Ry(phi) @ Rz(-th), (4, 9, zp))
        f.box('spider', (-19, 8, zp - 1), (-3, 10, zp + 1), uv('spider', 18, 0, 16, 2, 2, True), 'body', Ry(-phi) @ Rz(th), (-4, 9, zp))
    f.cross('cw', (-11, 7, 15), 14, 'body')
    f.cross('cw', (11, 6, 14), 12, 'body')
    f.sprite('i_bone', (6, 2.5, -14), 10, 'body', Rx(-55) @ Rz(30), item=False)
    return bake(f, {'head': (1.3, (0, 9, -3), (0, 9, -3))}, height=8.5, width=12.0), ('mc', 'mo')


def frost():
    """The Frost Marksman: the stray, ragged, in his diamond helm and chainmail, his longbow upright at his side - the
    huntsman who never missed, standing his watch"""
    f = Fig()
    P = {'r': Rx(-10) @ Rz(8), 'l': Rx(-25) @ Rz(-20)}
    humanoid(f, 'stray', arms=2, wide=False, poses=P, over='stray_o')
    armour(f, helm='a_diamond', chest='a_chain', poses=P)
    hl = hand(P['l'], (-5, 22, 0), -5)
    f.sprite('i_bow', hl + [-1.2, 1.5, -0.6], 17, 'body', Rz(-45))                                                 # (the bow, upright in his fist)
    return bake(f, chibi(kh=1.4)), ('pi', 'sn')


def tide():
    """The Drowned Tyrant: the drowned in his gold helm, his trident held high to throw, the other hand reaching"""
    f = Fig()
    P = {'r': Rx(15) @ Rz(125), 'l': Rx(70) @ Rz(-10)}
    humanoid(f, 'drowned', left64=True, hat=True, poses=P, over='drowned_o')
    armour(f, helm='a_gold', skinny=False)
    hr = hand(P['r'], (6, 22, 0), 6)
    f.sprite('i_trident', hr + [0.8, 2.5, -0.6], 20, 'body', Rz(-45))                                              # (upright, tines high)
    f.cross('tc', (-7, 2.5, -6), 6, 'legs')
    return bake(f, chibi()), ('dp', 'pr')


def hex_():
    """The Archmage: the evoker mid-spell, both arms flung up, a shard of amethyst crackling between his hands"""
    f = Fig()
    s = 'evoker'
    f.box(s, (0, 0, -2), (4, 12, 2), uv(s, 0, 22, 4, 12, 4), 'legs')
    f.box(s, (-4, 0, -2), (0, 12, 2), uv(s, 0, 22, 4, 12, 4, True), 'legs')
    f.box(s, (-4, 12, -3), (4, 24, 3), uv(s, 16, 20, 8, 12, 6), 'body')
    f.box(s, (-4, 4, -3), (4, 24, 3), uv(s, 0, 38, 8, 20, 6), 'body', grow=0.5)                                     # (his robe)
    P = {'r': Rx(-15) @ Rz(140), 'l': Rx(-15) @ Rz(-140)}
    f.box(s, (4, 12, -2), (8, 24, 2), uv(s, 40, 46, 4, 12, 4), 'body', P['r'], (5, 22, 0))
    f.box(s, (-8, 12, -2), (-4, 24, 2), uv(s, 40, 46, 4, 12, 4, True), 'body', P['l'], (-5, 22, 0))
    f.box(s, (-4, 24, -4), (4, 34, 4), uv(s, 0, 0, 8, 10, 8), 'head')
    f.box(s, (-1, 23, -6), (1, 27, -4), uv(s, 24, 0, 2, 4, 2), 'head')                                              # (his nose)
    f.cross('am', (0, 46, -1), 15, 'body', item=True)
    return bake(f, chibi(), height=12.5), ('pb', 'pu')


def keep():
    """Bobbery: the wither skeleton in his gold-trimmed netherite, his axe swung up over his head"""
    f = Fig()
    P = {'r': Rx(20) @ Rz(118), 'l': Rx(30) @ Rz(-15)}
    humanoid(f, 'wither', arms=2, wide=False, poses=P)
    armour(f, helm='a_neth', chest='a_neth', legs='l_neth', boots='a_neth', poses=P)
    hr = hand(P['r'], (5, 22, 0), 5)
    f.sprite('i_axe', hr + [0.5, 5.0, -0.8], 16, 'body', Rz(-45))                                                  # (raised high, head up)
    f.box('y', (-10, 0, -9), (-6, 1.6, -5), {k: [0, 0, 16, 16] for k in ('north', 'south', 'east', 'west', 'up', 'down')}, 'legs')   # (a spill of his gold)
    f.box('y', (6, 0, -10), (9, 1.2, -7), {k: [0, 0, 16, 16] for k in ('north', 'south', 'east', 'west', 'up', 'down')}, 'legs')
    for e in f.parts[-2:]:
        for fc in e['faces'].values(): fc['texture'] = '#y'
    return bake(f, chibi()), ('nb', 'pd')


def hollow(crown):
    """The Hollow King: the wither skeleton crowned, in his netherite, his sword planted point-down before him, both hands on
    the hilt; wither roses at his feet"""
    f = Fig()
    P = {'r': Rx(38) @ Rz(22), 'l': Rx(38) @ Rz(-22)}
    humanoid(f, 'wither', arms=2, wide=False, poses=P)
    armour(f, chest='a_neth', legs='l_neth', boots='a_neth', poses=P)
    mid = (hand(P['r'], (5, 22, 0), 5) + hand(P['l'], (-5, 22, 0), -5)) / 2
    f.sprite('i_sword', mid + [0, -6.5, -0.8], 16, 'body', Rz(135))                                                # (point down)
    for el in crown:                                                                                                # the King's own crown
        f.parts.append(el)
    f.cross('wr', (-8, 4.5, -6), 9, 'legs')
    f.cross('wr', (8, 4, -5), 8, 'legs')
    return bake(f, chibi()), ('pd', 'pb')


def lucky():
    """The Golden Goose: the warm chicken herself, wings up, on her golden egg's nest"""
    f = Fig()
    s = 'chicken'
    f.box(s, (-3, 0, -2), (0, 5, 1), uv(s, 26, 0, 3, 5, 3), 'legs')
    f.box(s, (0, 0, -2), (3, 5, 1), uv(s, 26, 0, 3, 5, 3, True), 'legs')
    f.box(s, (-3, 4, -3), (3, 12, 3), uv(s, 0, 9, 6, 8, 6), 'body', Rx(90), (0, 8, 0))                            # body (laid along her)
    f.box(s, (-4, 7, -3), (-3, 11, 3), uv(s, 24, 13, 1, 4, 6), 'body', Rz(-14), (-4, 11, 0))                       # wings, a little raised
    f.box(s, (3, 7, -3), (4, 11, 3), uv(s, 24, 13, 1, 4, 6, True), 'body', Rz(14), (4, 11, 0))
    f.box(s, (-2, 9, -6), (2, 15, -3), uv(s, 0, 0, 4, 6, 3), 'head')
    f.box(s, (-2, 11, -8), (2, 13, -6), uv(s, 14, 0, 4, 2, 2), 'head')
    f.box(s, (-1, 9, -7), (1, 11, -5), uv(s, 14, 4, 2, 2, 2), 'head')
    full = {k: [0, 0, 16, 16] for k in ('north', 'south', 'east', 'west', 'up', 'down')}
    for lo, hi in (((5, 0, -8), (9, 1, -4)), ((5.5, 1, -7.5), (8.5, 4.5, -4.5)), ((6, 4.5, -7), (8, 5.5, -5))):    # her golden egg
        f.box('y', lo, hi, full, 'legs')
    for lo, hi in (((-9, 0, -7), (-6, 0.8, -4)), ((-8, 0, 4), (-5, 1, 7)), ((5, 0, 5), (8, 0.7, 8))):              # nuggets of raw gold
        f.box('go', lo, hi, full, 'legs')
    return bake(f, {'head': (1.35, (0, 9, -4), (0, 9, -4))}, height=9.5, width=11.0), ('gc', 'em')


def _crown(crown):
    """the Hollow King's crown (bm:crown, as he wears it: gen_rp's HATS['crown']) - its elements, sized to sit on his skull"""
    m = {'textures': crown[0], 'elements': crown[1]}
    els = m['elements']
    lo = np.min([e['from'] for e in els] + [e['to'] for e in els], 0)
    hi = np.max([e['from'] for e in els] + [e['to'] for e in els], 0)
    k = 9.6 / max(hi[0] - lo[0], hi[2] - lo[2])
    c = (lo + hi) / 2
    out = []
    for e in els:
        a, b = np.array(e['from'], float), np.array(e['to'], float)
        p = lambda v: np.array([(v[0] - c[0]) * k, 31.2 + (v[1] - lo[1]) * k, (v[2] - c[2]) * k])
        R, piv = np.eye(3), (p(a) + p(b)) / 2
        r = e.get('rotation')
        if r:
            R = {'x': Rx, 'y': Ry, 'z': Rz}[r['axis']](r['angle']) if 'axis' in r else Rz(r.get('z', 0)) @ Ry(r.get('y', 0)) @ Rx(r.get('x', 0))
            piv = p(np.array(r['origin'], float))
        faces = {}
        for fn, fc in e['faces'].items():
            t = m['textures'].get(fc['texture'].lstrip('#'), fc['texture'])
            faces[fn] = dict(fc, texture='#k_' + t.split('/')[-1])
            faces[fn].pop('cullface', None)
            CROWN_TEX['k_' + t.split('/')[-1]] = t
        out.append(dict(lo=p(a), hi=p(b), faces=faces, group='head', R=R, pivot=piv, item=False))
    return out


CROWN_TEX = {}


def models(crown):
    """{dungeon: (textures, elements)} - the trophy, plinth and boss (crown: the King's crown model, (textures, elements))"""
    crown = _crown(crown)
    M = {}
    for d, (els, (b, t)) in (('brood', brood()), ('frost', frost()), ('tide', tide()), ('hex', hex_()), ('keep', keep()),
                             ('hollow', hollow(crown)), ('lucky', lucky())):
        els = plinth(b, t) + els
        used = {fc['texture'][1:] for e in els for fc in e['faces'].values()}
        tex = {b: BLOCK[b]}
        tex.update({k: SKIN.get(k) or BLOCK.get(k) or CROWN_TEX[k] for k in sorted(used) if k != b})
        M[d] = (tex, els)
    return M
