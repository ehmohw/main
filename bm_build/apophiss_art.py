"""2.76: APOPHISS - the serpent king (a draft for approval: rig, textures, poses).

From the reference art: a great green serpent-dragon, light belly from chin to tail, a huge round head and a wide maw of
dark red with cream fangs and a forked tongue, black eyes over purple bags under heavy black brows, a small black crown
(ball-tipped spikes, a great emerald, a ruby, white fur), jagged teal fins down his back, clawed hands, thick hind legs
and a long tail ending in a black spiked mace with white crescent blades. Phase 2: ETHEREAL - his scales go to a dark,
green-veined spectre and great violet wings open from his back.

Rig (rigkit): body (root) - head - jaw; arms, legs, wings off the body; tail1 - tail2 - tail3 - mace.
Design units: feet at y=0, facing -z, his right +x; drawn at BOSS_SCALE (about 5 blocks) or PET_SCALE (rideable).
    python3 apophiss_art.py <out.png>      renders the draft poses (needs the resource pack built)
"""
import math
import random
import sys
from PIL import Image, ImageDraw

from phase57_art import _el, hexc
from rigkit import qs, shrink, transform, I

PREFIX = 'apo_'
BOSS_SCALE, PET_SCALE = 2.0, 0.95
PIVOT = {'body': (0, 10, 0), 'head': (0, 30, -2), 'jaw': (0, 32, -3), 'armr': (8.6, 27, -1), 'arml': (-8.6, 27, -1),
         'legr': (5, 11, 1), 'legl': (-5, 11, 1), 'tail1': (0, 9, 6), 'tail2': (0, 6.6, 16.6), 'tail3': (0, 5.2, 26.4), 'mace': (0, 5, 34.6),
         'wingr': (4, 27, 6.5), 'wingl': (-4, 27, 6.5)}
PARENT = {'body': None, 'head': 'body', 'jaw': 'head', 'armr': 'body', 'arml': 'body', 'legr': 'body', 'legl': 'body',
          'tail1': 'body', 'tail2': 'tail1', 'tail3': 'tail2', 'mace': 'tail3', 'wingr': 'body', 'wingl': 'body'}
PARTS = tuple(PIVOT)
WING_K = 2.2                     # the wings reach past a model's box: built at full size, kept at 1/2.2, shown at 2.2x
PART_K = {'wingr': WING_K, 'wingl': WING_K}
G, G_DK, G_LT, BELLY, BELLY_DK = '#1b7d2e', '#0d5220', '#38a84c', '#b2cd68', '#90ab4a'
FIN, FIN_LT, FIN_DK = '#0e4e48', '#22907f', '#052b27'


def HIDDEN(p, pose):
    return p in ('wingr', 'wingl') and not pose.get('_eth')


def model_name(p, pose, suffix=''):
    return f'{PREFIX}{p}{"_eth" if pose.get("_eth") else ""}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _noise(base, seed, var=10, size=64):
    rnd = random.Random(seed); b = hexc(base)[:3]; im = Image.new('RGBA', (size, size))
    for y in range(size):
        for x in range(size):
            d = rnd.randint(-var, var)
            im.putpixel((x, y), tuple(max(0, min(255, v + d)) for v in b) + (255,))
    return im


def _scales(base, dark, light, seed, glow=None):
    """overlapping scale arcs, a highlight on each - the hide of the art"""
    im = _noise(base, seed, 6); d = ImageDraw.Draw(im); rnd = random.Random(seed + 1)
    for row in range(-1, 10):
        for col in range(-1, 10):
            cx = col * 8 + (4 if row % 2 else 0); cy = row * 7
            d.arc((cx - 5, cy - 4, cx + 5, cy + 6), 20, 160, fill=hexc(dark), width=1)
            if rnd.random() < 0.55: d.arc((cx - 3, cy - 2, cx + 3, cy + 3), 200, 300, fill=hexc(light), width=1)
    if glow:
        for _ in range(6):                                        # the ethereal veins
            x, y = rnd.randint(0, 63), rnd.randint(0, 63)
            for _s in range(rnd.randint(18, 40)):
                im.putpixel((x % 64, y % 64), hexc(glow)[:3] + (255,))
                x += rnd.choice((-1, 0, 1, 1)); y += rnd.choice((0, 1, 1))
    return im


def _bands(base, line, seed, glow=None):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im)
    for y in range(6, 64, 12):
        d.line((0, y, 63, y), fill=hexc(line), width=1)
        d.line((0, y + 1, 63, y + 1), fill=tuple(min(255, v + 18) for v in hexc(base)[:3]), width=1)
    if glow:
        for y in range(6, 64, 12): d.line((0, y, 63, y), fill=hexc(glow), width=1)
    return im


def _fin(base, light, dark, seed, alpha=255):
    im = _noise(base, seed, 6); rnd = random.Random(seed)
    for x in range(64):
        if rnd.random() < 0.35:
            for y in range(64): im.putpixel((x, y), tuple(min(255, int(v * 0.6 + c * 0.4)) for v, c in zip(im.getpixel((x, y))[:3], hexc(light)[:3])) + (255,))
    for y in range(64):
        for x in range(64):
            p = im.getpixel((x, y))
            if y > 56 or y < 3: p = hexc(dark)[:3] + (255,)
            im.putpixel((x, y), p[:3] + (alpha,))
    return im


def _mace(base, spike, seed):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(60):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); l = rnd.randint(2, 5)
        d.line((x, y, x + l, y - l), fill=hexc(spike), width=1)
    return im


def _bone(base, shade, seed):
    im = _noise(base, seed, 6)
    for y in range(64):
        for x in range(64):
            if (x + y) % 23 < 3:
                im.putpixel((x, y), hexc(shade)[:3] + (255,))
    return im


def _membrane(seed):
    im = Image.new('RGBA', (64, 64)); rnd = random.Random(seed)
    for y in range(64):
        for x in range(64):
            g = 1 + rnd.uniform(-0.08, 0.08)
            im.putpixel((x, y), (int(122 * g), int(60 * g), int(230 * g), 150))
    d = ImageDraw.Draw(im)
    for i in range(7):
        x0 = rnd.randint(0, 63)
        d.line((x0, 0, x0 + rnd.randint(-20, 20), 63), fill=(70, 255, 150, 210), width=1)
    return im


def textures():
    T = {'apo_scale': _scales(G, G_DK, G_LT, 701), 'apo_scale_dk': _scales(G_DK, '#073514', G, 702), 'apo_belly': _bands(BELLY, BELLY_DK, 703),
         'apo_fin': _fin(FIN, FIN_LT, FIN_DK, 704), 'apo_claw': _noise('#0b3613', 705, 6), 'apo_mouth': _noise('#5c0b16', 706, 8),
         'apo_tongue': _noise('#7c1830', 707, 6), 'apo_fang': _noise('#efe6c4', 708, 6), 'apo_eye': _noise('#0e0e12', 709, 3),
         'apo_glint': _noise('#ffffff', 710, 2), 'apo_bag': _noise('#5e2d70', 711, 6), 'apo_lash': _noise('#060606', 712, 2),
         'apo_mace': _mace('#232327', '#4a4a54', 713), 'apo_bone': _bone('#e9e4d8', '#b8b2a4', 714), 'apo_nostril': _noise('#0a2a10', 715, 3)}
    # phase 2: the ethereal spectre
    T.update({'apo_scale_eth': _scales('#0a1f14', '#05100a', '#1a4a2c', 721, glow='#3cff8a'), 'apo_scale_dk_eth': _scales('#06140c', '#020804', '#12301e', 722, glow='#2ad070'),
              'apo_belly_eth': _bands('#2e4a36', '#1c3022', 723, glow='#7affb0'), 'apo_fin_eth': _fin('#3a1a6a', '#8a4aff', '#1a0a34', 724, alpha=220),
              'apo_claw_eth': _noise('#1a0a34', 725, 6), 'apo_eye_eth': _noise('#30ff90', 726, 10), 'apo_mace_eth': _mace('#141418', '#8a4aff', 727),
              'apo_bone_eth': _bone('#c8f0ff', '#7ab0c8', 728), 'apo_wing': _membrane(729), 'apo_wingbone': _noise('#1a1030', 730, 6)})
    return T


ETH_SWAP = {'apo_scale': 'apo_scale_eth', 'apo_scale_dk': 'apo_scale_dk_eth', 'apo_belly': 'apo_belly_eth', 'apo_fin': 'apo_fin_eth',
            'apo_claw': 'apo_claw_eth', 'apo_eye': 'apo_eye_eth', 'apo_mace': 'apo_mace_eth', 'apo_bone': 'apo_bone_eth'}


# ---------------------------------------------------------------------------------------------------- models
def _crown(cx, base, cz, k):
    """the black crown (phase59's), scaled k about its band, its band's foot at (cx, base, cz)"""
    c = lambda fr, to, t, rot=None: (fr, to, t, rot)
    cr = [c((2.4, 13.6, 2.4), (13.6, 15.2, 13.6), 'f'),
          c((3, 15.0, 3), (13, 18.0, 3.8), 'k'), c((3, 15.0, 12.2), (13, 18.0, 13), 'k'),
          c((3, 15.0, 3.8), (3.8, 18.0, 12.2), 'k'), c((12.2, 15.0, 3.8), (13, 18.0, 12.2), 'k'), c((3.4, 17.6, 3.4), (12.6, 18.2, 12.6), 'k'),
          c((5.2, 17.8, 5.2), (10.8, 20.6, 10.8), 'e'), c((5.8, 20.4, 5.8), (10.2, 22.0, 10.2), 'e', ('y', 45, (8, 21, 8))),
          c((6.6, 21.8, 6.6), (9.4, 23.2, 9.4), 'v'), c((7.3, 23.0, 7.3), (8.7, 23.8, 8.7), 'v', ('y', 45, (8, 23.4, 8)))]
    for x, z, h in [(8, 3.4, 6.6), (5.0, 3.4, 4.0), (11.0, 3.4, 4.0), (3.4, 5.6, 5.0), (12.6, 5.6, 5.0), (3.4, 10.0, 3.4), (12.6, 10.0, 3.4),
                    (5.0, 12.6, 4.4), (11.0, 12.6, 4.4), (8, 12.6, 5.4)]:
        w = 1.3 if h > 6 else 1.1
        cr += [c((x - w / 2, 17.8, z - w / 2), (x + w / 2, 17.8 + h * 0.55, z + w / 2), 'k'), c((x - 0.35, 17.8 + h * 0.55, z - 0.35), (x + 0.35, 17.8 + h, z + 0.35), 'k'),
               c((x - 0.75, 17.6 + h, z - 0.75), (x + 0.75, 19.0 + h, z + 0.75), 'k')]
    cr += [c((7.0, 19.0, 2.3), (9.0, 21.0, 2.9), 'r', ('z', 45, (8, 20, 2.6))), c((7.45, 19.45, 2.05), (8.55, 20.55, 2.35), 'o', ('z', 45, (8, 20, 2.2)))]
    for x, z in ((5.0, 2.9), (11.0, 2.9)):
        cr += [c((x - 1.0, 15.6, z - 0.55), (x + 1.0, 17.6, z - 0.15), 'a'), c((x - 0.6, 15.9, z - 0.9), (x + 0.6, 17.3, z - 0.5), 'r')]
    TEX = {'k': 'ap_black', 'e': 'ap_emerald', 'v': 'ap_emerald_lt', 'r': 'ap_ruby', 'o': 'ap_ruby_lt', 'a': 'ap_gold', 'f': 'ap_fur'}
    m = lambda p: (cx + (p[0] - 8) * k, base + (p[1] - 13.6) * k, cz + (p[2] - 8) * k)
    return [(m(fr), m(to), TEX[t], (rot[0], rot[1], m(rot[2])) if rot else None) for fr, to, t, rot in cr]


def models():
    M = {}
    def part(name, els, k=1.0):
        els = shrink(els, k) if k != 1.0 else els
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
        eth = []
        for e in els:
            e2 = dict(e, faces={f: dict(v, texture='#' + ETH_SWAP.get(v['texture'][1:], v['texture'][1:])) for f, v in e['faces'].items()})
            e2['light_emission'] = max(e.get('light_emission', 0), 7)
            eth.append(e2)
        used = sorted({e['faces'][f]['texture'][1:] for e in eth for f in e['faces']})
        M[name + '_eth'] = ({t: f'bm:block/{t}' for t in used}, eth)
    E = lambda pv: (lambda fr, to, t='apo_scale', rot=None, uv=None: _el(fr, to, t, pv, rot, uv))

    # ---- the body: a deep trunk, the belly plate down its front, a hump of shoulders, fins down the spine
    b = E(PIVOT['body'])
    body = [b((-7.6, 6.6, -6.0), (7.6, 16.0, 7.0)), b((-8.0, 15.4, -6.6), (8.0, 23.2, 6.6)), b((-8.6, 22.4, -6.6), (8.6, 29.4, 6.2)),
            b((-9.2, 25.6, -5.2), (9.2, 30.0, 5.0)), b((-5.6, 28.4, -6.4), (5.6, 32.4, 3.4)),
            b((-6.0, 11.0, 6.4), (6.0, 27.0, 8.0), 'apo_scale_dk'),                                              # the back
            b((-5.0, 7.0, -6.6), (5.0, 16.0, -6.0), 'apo_belly'), b((-5.6, 15.4, -7.2), (5.6, 23.2, -6.6), 'apo_belly'),
            b((-5.2, 22.4, -7.2), (5.2, 29.4, -6.6), 'apo_belly'), b((-3.8, 28.4, -7.0), (3.8, 32.4, -6.4), 'apo_belly'),
            b((-6.6, 6.0, -5.0), (6.6, 7.0, 6.0), 'apo_belly')]                                                    # under the hips
    for y, l, a in ((26.0, 7.5, -30), (22.0, 6.5, -28), (18.0, 5.6, -26), (14.0, 4.6, -24), (10.6, 3.6, -22)):  # the spine's fins
        body += [b((-0.45, y, 7.6), (0.45, y + 1.6, 7.6 + l), 'apo_fin', ('x', a, (0, y + 0.8, 7.6))),
                 b((-0.35, y + 1.2, 7.6), (0.35, y + 2.6, 7.6 + l * 0.6), 'apo_fin', ('x', a - 14, (0, y + 1.6, 7.6)))]
    part('apo_body', body)

    # ---- the head: a great round skull over a wide snout, the maw's red roof and fangs, black eyes, purple bags, heavy
    #      brows sweeping out past his cheeks, nostrils, the crown, and a crest of fins behind
    pv = PIVOT['head']; h = E(pv)
    head = [h((-5.4, 28.6, -5.0), (5.4, 32.6, 3.0)),                                                             # the neck's top
            h((-7.0, 30.6, -4.4), (7.0, 38.6, 3.2)), h((-7.0, 32.4, -10.0), (7.0, 38.6, -4.4)),                      # skull: back, front
            h((-6.0, 32.4, -13.0), (6.0, 37.0, -10.0)), h((-5.0, 32.8, -13.6), (5.0, 36.4, -13.0)),                  # the snout
            h((-6.2, 38.6, -9.0), (6.2, 39.6, 2.2)), h((-7.6, 32.4, -8.0), (-7.0, 37.4, 1.4)), h((7.0, 32.4, -8.0), (7.6, 37.4, 1.4)),
            h((-5.8, 32.0, -12.6), (5.8, 32.4, -4.4), 'apo_mouth'),                                                  # the maw's roof
            h((-5.1, 29.6, -12.5), (-3.9, 32.1, -11.4), 'apo_fang'), h((3.9, 29.6, -12.5), (5.1, 32.1, -11.4), 'apo_fang'),   # fangs
            h((-5.4, 29.0, -12.2), (-4.5, 30.0, -11.6), 'apo_fang'), h((4.5, 29.0, -12.2), (5.4, 30.0, -11.6), 'apo_fang')]
    for x in (-2.6, -1.0, 0.6, 2.2):                                                                                  # the small teeth
        head.append(h((x, 31.0, -12.9), (x + 0.6, 32.1, -12.4), 'apo_fang'))
    for sx in (1, -1):                                                                                               # eyes and brows
        x0, x1 = (1.3, 5.5) if sx > 0 else (-5.5, -1.3)
        head += [h((x0, 34.6, -10.12), (x1, 37.8, -10.0), 'apo_eye'),
                 h((x0 + 0.3, 34.0, -10.1), (x1 - 0.2, 34.7, -10.0), 'apo_bag'),
                 h((min(sx * 2.4, sx * 3.3), 36.6, -10.2), (max(sx * 2.4, sx * 3.3), 37.4, -10.12), 'apo_glint'),
                 h((min(sx * 0.6, sx * 6.6), 37.9, -10.4), (max(sx * 0.6, sx * 6.6), 38.9, -9.4), 'apo_lash', ('z', -16 * sx, (sx * 3.6, 38.4, -9.9))),
                 h((min(sx * 6.2, sx * 9.4), 38.6, -9.2), (max(sx * 6.2, sx * 9.4), 39.3, -8.4), 'apo_lash', ('z', 30 * sx, (sx * 6.4, 38.9, -8.8))),
                 h((min(sx * 6.4, sx * 8.6), 37.2, -9.6), (max(sx * 6.4, sx * 8.6), 37.8, -9.0), 'apo_lash', ('z', -25 * sx, (sx * 6.4, 37.5, -9.3))),
                 h((min(sx * 1.2, sx * 2.2), 36.95, -12.7), (max(sx * 1.2, sx * 2.2), 37.08, -11.8), 'apo_nostril')]
    for i, (dy, l, a) in enumerate(((37.6, 9.0, -35), (35.6, 8.0, -28), (33.4, 6.4, -22))):                        # the crest of fins
        for sx in (2.2, -2.2):
            head += [h((sx - 0.45, dy, 2.6), (sx + 0.45, dy + 2.2, 2.6 + l), 'apo_fin', ('x', a, (sx, dy + 1.1, 2.6))),
                     h((sx - 0.35, dy + 1.6, 2.6), (sx + 0.35, dy + 3.0, 2.6 + l * 0.55), 'apo_fin', ('x', a - 16, (sx, dy + 2.2, 2.6)))]
    for fr, to, t, rot in _crown(0, 39.4, -3.6, 0.56):
        head.append(_el(fr, to, t, pv, rot))
    part('apo_head', head)

    # ---- the jaw: the lower maw, its red floor, fangs up, the forked tongue lolling out
    j = E(PIVOT['jaw'])
    jaw = [j((-6.2, 28.8, -12.2), (6.2, 31.9, -2.2)), j((-4.6, 28.5, -11.6), (4.6, 28.8, -3.0), 'apo_belly'),
           j((-5.4, 31.6, -11.6), (5.4, 31.95, -2.8), 'apo_mouth'),
           j((-4.7, 31.8, -11.5), (-3.9, 33.0, -10.8), 'apo_fang'), j((3.9, 31.8, -11.5), (4.7, 33.0, -10.8), 'apo_fang'),
           j((-0.7, 31.2, -14.6), (0.7, 31.7, -10.8), 'apo_tongue', ('x', -12, (0, 31.4, -10.8))),
           j((-1.5, 30.5, -16.6), (-0.4, 31.0, -14.4), 'apo_tongue', ('y', 20, (-0.6, 30.8, -14.6))),
           j((0.4, 30.5, -16.6), (1.5, 31.0, -14.4), 'apo_tongue', ('y', -20, (0.6, 30.8, -14.6)))]
    for x in (-2.4, 0.0, 2.0):
        jaw.append(j((x, 31.8, -11.9), (x + 0.5, 32.6, -11.4), 'apo_fang'))
    part('apo_jaw', jaw)

    # ---- arms: big shoulders, the forearm bent forward at the elbow, a broad hand, four hooked claws; fins on the forearm
    def arm(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; a = E(pv); cx = pv[0] + 0.6 * sx
        el = (cx, 19.0, -1.0); fa = ('x', -38, el)
        X = lambda x0, x1: (min(cx + x0 * sx, cx + x1 * sx), max(cx + x0 * sx, cx + x1 * sx))
        def F(x0, x1, y0, y1, z0, z1, t='apo_scale'):
            xa, xb = X(x0, x1); return a((xa, y0, z0), (xb, y1, z1), t, fa)
        xa, xb = X(-2.6, 2.6)
        els = [a((xa, 23.0, -3.8), (xb, 29.4, 3.0)), a(X(-2.0, 2.0)[:1] + (18.4, -3.0), X(-2.0, 2.0)[1:] + (24.0, 1.6)),
               F(-1.8, 1.8, 12.4, 19.6, -2.8, 0.8), F(-1.6, 1.6, 12.6, 18.0, -3.1, -2.7, 'apo_scale_dk'),
               F(-2.3, 2.3, 9.6, 12.8, -3.2, 1.2)]                                                               # the hand
        for i in range(4):                                                                                       # claws
            x = -1.9 + i * 1.15
            els += [F(x, x + 0.75, 7.2, 9.8, -3.4, -2.4, 'apo_claw'), F(x + 0.15, x + 0.6, 6.0, 7.4, -4.4, -3.6, 'apo_claw')]
        els += [F(2.0, 2.9, 9.8, 11.8, -3.0, -2.0, 'apo_claw')]                                                 # the thumb
        for y, l in ((17.4, 2.4), (15.6, 2.0), (13.8, 1.6)):                                                      # forearm fins
            els.append(F(1.7, 1.7 + l, y, y + 0.8, -0.6, 0.6, 'apo_fin'))
        return els
    part('apo_armr', arm(1)); part('apo_arml', arm(-1))

    # ---- legs: a huge thigh, a short shin, a broad foot, three talons
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; l = E(pv)
        X = lambda x0, x1: (min(pv[0] + x0 * sx, pv[0] + x1 * sx), max(pv[0] + x0 * sx, pv[0] + x1 * sx))
        box = lambda x0, x1, y0, y1, z0, z1, t='apo_scale', rot=None: l((X(x0, x1)[0], y0, z0), (X(x0, x1)[1], y1, z1), t, rot)
        els = [box(-3.0, 3.4, 5.4, 13.4, -3.2, 4.4), box(-2.2, 2.6, 1.6, 6.4, -2.2, 2.8), box(-2.6, 2.8, 0.0, 2.0, -5.6, 2.8),
               box(-2.0, 2.2, 5.6, 12.4, -3.4, -3.2, 'apo_scale_dk')]
        for i in range(3):
            x = -1.9 + i * 1.6
            els.append(box(x, x + 1.0, 0.0, 1.4, -7.6, -5.4, 'apo_claw'))
        return els
    part('apo_legr', leg(1)); part('apo_legl', leg(-1))

    # ---- the tail: three tapering lengths, belly underneath, little fins on top; the mace at its end
    for name, (w, y0, y1, z0, z1, n) in (('tail1', (5.0, 4.0, 12.2, 5.0, 17.4, 3)), ('tail2', (4.0, 3.0, 9.8, 16.2, 27.0, 3)),
                                         ('tail3', (3.0, 2.6, 7.6, 26.0, 35.2, 2))):
        t = E(PIVOT[name])
        els = [t((-w, y0, z0), (w, y1, z1)), t((-w * 0.65, y0 - 0.3, z0 + 0.5), (w * 0.65, y0, z1 - 0.3), 'apo_belly')]
        for i in range(n):
            z = z0 + 1.5 + i * (z1 - z0 - 2) / n
            els.append(t((-0.4, y1 - 0.2, z), (0.4, y1 + 2.4 - i * 0.4, z + 2.4), 'apo_fin', ('x', -30, (0, y1, z))))
        part(f'apo_{name}', els)
    m = E(PIVOT['mace'])
    mz = 38.4; my = 5.0
    mace = [m((-3.4, my - 3.4, mz - 3.4), (3.4, my + 3.4, mz + 3.4), 'apo_mace'), m((-1.6, my - 1.6, 34.0), (1.6, my + 1.6, mz - 3.0))]
    for ax, ang in (('x', 45), ('y', 45), ('z', 45)):                                                           # its spikes
        mace.append(m((-2.9, my - 2.9, mz - 2.9), (2.9, my + 2.9, mz + 2.9), 'apo_mace', (ax, ang, (0, my, mz))))
    for dx, dy, dz in ((0, 4.2, 0), (0, -4.2, 0), (4.2, 0, 0), (-4.2, 0, 0), (0, 0, 4.2), (2.6, 2.6, 2.6), (-2.6, 2.6, 2.6), (2.6, -2.6, 2.6), (-2.6, -2.6, 2.6)):
        mace.append(m((dx - 0.5, my + dy - 0.5, mz + dz - 0.5), (dx + 0.5, my + dy + 0.5, mz + dz + 0.5), 'apo_mace'))
    def crescent(points, plane):                                                                                   # a bone blade, a curve of pieces
        out = []
        for i in range(len(points) - 1):
            (a0, b0), (a1, b1) = points[i], points[i + 1]
            ca, cb = (a0 + a1) / 2, (b0 + b1) / 2; L = math.hypot(a1 - a0, b1 - b0) + 0.6; th = max(0.5, 1.6 - i * 0.28)
            ang = math.degrees(math.atan2(b1 - b0, a1 - a0))
            while ang > 45: ang -= 90
            while ang < -45: ang += 90
            horiz = abs(math.degrees(math.atan2(b1 - b0, a1 - a0))) % 180 < 45 or abs(math.degrees(math.atan2(b1 - b0, a1 - a0))) % 180 > 135
            la, lb = (L / 2, th / 2) if horiz else (th / 2, L / 2)
            if plane == 'xy':
                out.append(m((ca - la, cb - lb, mz - 0.4), (ca + la, cb + lb, mz + 0.4), 'apo_bone', ('z', ang, (ca, cb, mz))))
            else:                                                                                                  # 'zy': a blade off the back
                out.append(m((-0.4, cb - lb, ca - la), (0.4, cb + lb, ca + la), 'apo_bone', ('x', -ang, (0, cb, ca))))
        return out
    mace += crescent([(0, my + 3.0), (1.2, my + 6.0), (0.4, my + 9.2), (-1.6, my + 11.6), (-3.6, my + 12.6)], 'xy')       # the top blade
    mace += crescent([(3.0, my), (6.0, my + 1.0), (8.6, my + 3.0), (9.8, my + 5.8), (9.6, my + 8.2)], 'xy')              # right
    mace += crescent([(-3.0, my), (-6.0, my - 1.0), (-8.6, my - 3.0), (-9.8, my - 5.8), (-9.6, my - 8.2)], 'xy')         # left, sweeping down
    mace += crescent([(mz + 3.0, my), (mz + 5.6, my + 1.4), (mz + 7.4, my + 3.6), (mz + 8.0, my + 6.2)], 'zy')           # out the back
    part('apo_mace', mace)

    # ---- (phase 2) the wings: a bony arm from his back, three long fingers, violet membrane between (built full size)
    def wing(sx):
        pv = PIVOT['wingr' if sx > 0 else 'wingl']; w = E(pv); x0 = pv[0]
        X = lambda a, b: (min(x0 + a * sx, x0 + b * sx), max(x0 + a * sx, x0 + b * sx))
        els = []
        def bone(a0, b0, a1, b1, z, th=1.0):                                                                     # a spar in the xy plane
            ca, cb = (a0 + a1) / 2, (b0 + b1) / 2; L = math.hypot(a1 - a0, b1 - b0) + th
            ang = math.degrees(math.atan2(b1 - b0, (a1 - a0) * sx)) * sx
            xa, xb = X(ca * sx - L / 2 * sx if False else 0, 0)
            cxw = x0 + ca * sx
            if abs(ang) <= 45:
                els.append(w((cxw - L / 2, pv[1] + cb - th / 2, z - th / 2), (cxw + L / 2, pv[1] + cb + th / 2, z + th / 2), 'apo_wingbone', ('z', ang, (cxw, pv[1] + cb, z))))
            else:
                ang2 = ang - 90 if ang > 0 else ang + 90
                els.append(w((cxw - th / 2, pv[1] + cb - L / 2, z - th / 2), (cxw + th / 2, pv[1] + cb + L / 2, z + th / 2), 'apo_wingbone', ('z', ang2, (cxw, pv[1] + cb, z))))
        bone(0, 0, 10, 8, 1.0, 1.6); bone(10, 8, 20, 14, 1.6, 1.3)                                                  # the arm
        for (a1, b1) in ((34, 18), (32, 4), (26, -8)):                                                             # the fingers
            bone(20, 14, a1, b1, 2.0, 0.8)
        # membrane panels (thin, translucent) between the fingers - stacked strips
        for i in range(10):
            t = i / 9
            a = 6 + t * 26; top = 6 + t * 10; bot = -2 - t * 6
            xa, xb = X(a - 1.6, a + 1.6)
            els.append(w((xa, pv[1] + bot, 1.8), (xb, pv[1] + top, 2.2), 'apo_wing'))
        return els
    part('apo_wingr', wing(1), WING_K); part('apo_wingl', wing(-1), WING_K)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (display frame rotations: +x on the body leans him forward, a limb swings forward with -x; his right arm out with -z)
def P(**kw):
    return kw


POSES = {
    'idle_a': P(body=qs(('x', 4)), head=qs(('x', -6)), jaw=qs(('x', 10)), armr=qs(('x', -12), ('z', -10)), arml=qs(('x', -12), ('z', 10)),
                tail1=qs(('y', 12), ('x', 6)), tail2=qs(('y', 22)), tail3=qs(('y', 30)), mace=qs(('y', 20))),
    'idle_b': P(_off=(0, -0.4, 0), body=qs(('x', 6)), head=qs(('x', -2)), jaw=qs(('x', 4)), armr=qs(('x', -16), ('z', -12)), arml=qs(('x', -16), ('z', 12)),
                tail1=qs(('y', 6), ('x', 6)), tail2=qs(('y', 18)), tail3=qs(('y', 34)), mace=qs(('y', 26))),
    'battle': P(_off=(0, -1.2, -1), body=qs(('x', 16)), head=qs(('x', -12)), jaw=qs(('x', 24)), armr=qs(('x', -48), ('z', -34)), arml=qs(('x', -48), ('z', 34)),
                legr=qs(('x', -12), ('z', -8)), legl=qs(('x', -12), ('z', 8)),
                tail1=qs(('x', -12)), tail2=qs(('x', -30)), tail3=qs(('x', -40)), mace=qs(('x', -20))),
    'claw': P(_off=(0, -1.0, -1), body=qs(('x', 20), ('y', 26)), head=qs(('x', -10), ('y', -14)), jaw=qs(('x', 30)),
              armr=qs(('x', -100), ('z', 26)), arml=qs(('x', -30), ('z', 30)), legr=qs(('x', -16)), legl=qs(('x', 10)),
              tail1=qs(('y', -18)), tail2=qs(('y', -22)), tail3=qs(('y', -18))),
    'bite': P(_off=(0, -2.0, -3), body=qs(('x', 30)), head=qs(('x', 6)), jaw=qs(('x', 42)), armr=qs(('x', -30), ('z', -40)), arml=qs(('x', -30), ('z', 40)),
              legr=qs(('x', -22)), legl=qs(('x', 6)), tail1=qs(('x', -10)), tail2=qs(('x', -16)), tail3=qs(('x', -10))),
    'mace_up': P(_off=(0, 0, 1), body=qs(('x', -8)), head=qs(('x', -10)), jaw=qs(('x', 20)), armr=qs(('x', -30), ('z', -26)), arml=qs(('x', -30), ('z', 26)),
                 tail1=qs(('x', -38)), tail2=qs(('x', -44)), tail3=qs(('x', -44)), mace=qs(('x', -30))),
    'mace_slam': P(_off=(0, -1.6, -2), body=qs(('x', 26)), head=qs(('x', -16)), jaw=qs(('x', 30)), armr=qs(('x', -20), ('z', -30)), arml=qs(('x', -20), ('z', 30)),
                   legr=qs(('x', -14)), legl=qs(('x', 8)), tail1=qs(('x', -44)), tail2=qs(('x', -62)), tail3=qs(('x', -58)), mace=qs(('x', -40))),
    'cast': P(body=qs(('x', -10)), head=qs(('x', -26)), jaw=qs(('x', 34)), armr=qs(('x', -150), ('z', -24)), arml=qs(('x', -150), ('z', 24)),
              tail1=qs(('y', 20)), tail2=qs(('y', 26)), tail3=qs(('y', 20))),
    'roar': P(_off=(0, 0.4, 0), body=qs(('x', -14)), head=qs(('x', -32)), jaw=qs(('x', 48)), armr=qs(('x', -60), ('z', -70)), arml=qs(('x', -60), ('z', 70)),
              tail1=qs(('x', -20)), tail2=qs(('x', -24)), tail3=qs(('x', -30)), mace=qs(('x', -20))),
    'tired': P(_off=(0, -3.0, -1), body=qs(('x', 34)), head=qs(('x', 18), ('z', 8)), jaw=qs(('x', 28)), armr=qs(('x', -20), ('z', -4)), arml=qs(('x', -14), ('z', 6)),
               legr=qs(('x', -30)), legl=qs(('x', -26)), tail1=qs(('x', 8)), tail2=qs(('y', 10)), tail3=qs(('y', 16)), mace=qs(('y', 10))),
    'crouch': P(_off=(0, -6.2, -4), body=qs(('x', 74)), head=qs(('x', -66)), jaw=qs(('x', 12)), armr=qs(('x', -78)), arml=qs(('x', -78)),
                legr=qs(('x', -60)), legl=qs(('x', -60)), tail1=qs(('x', -60)), tail2=qs(('x', -14)), tail3=qs(('x', -6)), mace=qs(('x', 6))),
    'walk_a': P(_off=(0, -6.0, -4), body=qs(('x', 74), ('z', 3)), head=qs(('x', -66), ('y', 6)), jaw=qs(('x', 10)), armr=qs(('x', -100)), arml=qs(('x', -56)),
                legr=qs(('x', -40)), legl=qs(('x', -80)), tail1=qs(('x', -60), ('y', 10)), tail2=qs(('y', 14)), tail3=qs(('y', 16))),
    'walk_b': P(_off=(0, -6.0, -4), body=qs(('x', 74), ('z', -3)), head=qs(('x', -66), ('y', -6)), jaw=qs(('x', 10)), armr=qs(('x', -56)), arml=qs(('x', -100)),
                legr=qs(('x', -80)), legl=qs(('x', -40)), tail1=qs(('x', -60), ('y', -10)), tail2=qs(('y', -14)), tail3=qs(('y', -16))),
    'sit': P(_off=(0, -3.4, 0), body=qs(('x', -4)), head=qs(('x', 4), ('y', 12)), jaw=qs(('x', 2)), armr=qs(('x', -30), ('z', 6)), arml=qs(('x', -30), ('z', -6)),
             legr=qs(('x', -80)), legl=qs(('x', -80)), tail1=qs(('y', 60), ('x', 10)), tail2=qs(('y', 60)), tail3=qs(('y', 60)), mace=qs(('y', 40))),
    'eth_hover': P(_eth=True, _off=(0, 6, 0), body=qs(('x', 10)), head=qs(('x', -14)), jaw=qs(('x', 30)), armr=qs(('x', -40), ('z', -30)), arml=qs(('x', -40), ('z', 30)),
                   legr=qs(('x', 20)), legl=qs(('x', 26)), tail1=qs(('x', 30)), tail2=qs(('x', 20)), tail3=qs(('x', 10)), mace=qs(('x', 10)),
                   wingr=qs(('y', 10), ('z', -6)), wingl=qs(('y', -10), ('z', 6))),
    'eth_beat': P(_eth=True, _off=(0, 7, 0), body=qs(('x', 12)), head=qs(('x', -12)), jaw=qs(('x', 36)), armr=qs(('x', -60), ('z', -40)), arml=qs(('x', -60), ('z', 40)),
                  legr=qs(('x', 24)), legl=qs(('x', 30)), tail1=qs(('x', 34)), tail2=qs(('x', 22)), tail3=qs(('x', 14)), mace=qs(('x', 10)),
                  wingr=qs(('y', 30), ('z', 40)), wingl=qs(('y', -30), ('z', -40))),
}
DRAFT = ['idle_a', 'battle', 'claw', 'bite', 'mace_up', 'mace_slam', 'cast', 'roar', 'tired', 'crouch', 'walk_a', 'sit', 'eth_hover', 'eth_beat']


def rp(R):
    import sys as _s
    R.TEXTURE_MODS.append(_s.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)


if __name__ == '__main__':
    sys.path.insert(0, '/home/user/main/bm_build')
    from tools.render import Scene
    import rigkit
    from PIL import Image as _I
    out = sys.argv[1]
    rp_dir = '/home/claude/bm_build/out_p2/BlackMarket_RP'
    tiles = []
    for name in (sys.argv[2].split(',') if len(sys.argv) > 2 else DRAFT):
        s = Scene(rp_dir); rigkit.render(s, sys.modules[__name__], POSES[name], scale=1.0)
        s.player_box((2.6, 0, 0))
        im = s.render('iso', size=360, span=7.0, center=(0, 2.0, 0)); ImageDraw.Draw(im).text((8, 6), name, fill=(0, 0, 0))
        tiles.append(im)
    cols = 4; rows = (len(tiles) + cols - 1) // cols
    sheet = _I.new('RGB', (cols * 360, rows * 360), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * 360, (i // cols) * 360))
    sheet.save(out); print(out)
