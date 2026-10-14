"""2.76: APOPHISS - the serpent king (a draft for approval: rig, textures, faces, poses).

From the reference art: a great green serpent with arms and no legs - he rears up out of his own coils like a cobra, his
light belly running from chin to coil; a huge round head with a maw of dark red, cream fangs (the lower ones jutting past
his lip) and a long forked tongue; glossy black eyes with white slit pupils under heavy lids, purple bags, black brushstroke brows, freckles on one cheek and
the honeycomb marks on the other; the small black crown (ball-tipped spikes, the great emerald, a ruby, white fur); jagged
teal fins from the back of his head down his spine; thick arms, webbed forearms, hooked claws; and a long tail that ends
in a black spiked mace with white crescent blades.
Phase 2, ETHEREAL: his scales go to a dark, green-veined spectre, his eyes burn green and violet wings open from his back.

Rig (rigkit): coil (the root: his coils on the ground) - body - chest - head - jaw; arms and wings off the chest;
tail1 - tail2 - tail3 - tail4 - mace out of the back of the coil (a long tail: it reaches over his head). Design units: the coil on y=0, facing -z, his right +x; shown at
BOSS_SCALE (about nine blocks to the tip of his crest) or PET_SCALE (the follower he becomes - since 2.77b just as big: no\none shrinks the Serpent King; you ride him).
Faces: the head model has a variant per expression (apo_head_x<face>): smug, shock, hurt, tired, blink - the default is
his scowl.
"""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, shrink, el, seg, chain, frame, transform, _add, _mul, _sub, _unit, I, mid

PREFIX = 'apo_'
BOSS_SCALE, PET_SCALE = 2.8, 2.8
PIVOT = {'coil': (0, 3, 5), 'body': (0, 5, -3.4), 'chest': (0, 19.4, -2.6), 'head': (0, 31.0, -0.8), 'jaw': (0, 31.8, 0.4),
         'armr': (8.4, 26.0, -3.0), 'arml': (-8.4, 26.0, -3.0),
         'tail1': (2.0, 3.0, 13.4), 'tail2': (2.4, 3.0, 24.6), 'tail3': (2.6, 3.0, 35.4), 'tail4': (2.7, 3.0, 45.2), 'mace': (2.75, 3.0, 54.0),
         'wingr': (5.0, 24.4, 2.8), 'wingl': (-5.0, 24.4, 2.8)}
PARENT = {'coil': None, 'body': 'coil', 'chest': 'body', 'head': 'chest', 'jaw': 'head', 'armr': 'chest', 'arml': 'chest',
          'tail1': 'coil', 'tail2': 'tail1', 'tail3': 'tail2', 'tail4': 'tail3', 'mace': 'tail4', 'wingr': 'chest', 'wingl': 'chest'}
PARTS = tuple(PIVOT)
WING_K = 1.7                    # the wings reach past a model's box: built at full size, kept at 1/1.7, shown at 1.7x
PART_K = {'wingr': WING_K, 'wingl': WING_K}
FACES = ('smug', 'shock', 'hurt', 'tired', 'blink')
G, G_DK, G_LT, BELLY, BELLY_DK = '#177a2c', '#0c5420', '#35a64a', '#b0cc66', '#8ea84a'
FIN, FIN_LT, FIN_DK = '#0d4c47', '#23917f', '#052a26'
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)
# (2.77d: a serpent's head - his eyes up and back on a taller brow, a long snout under them. The eyes are built where they
#  always were and moved by this much; the crown sits higher on the dome)
EYE_UP, EYE_BACK = 2.4, 3.2
CROWN_AT, CROWN_K = (0.0, 43.8, -4.6), 0.56          # (2.78: on the new dome, a little smaller - as the art)


def HIDDEN(p, pose):
    return p in ('wingr', 'wingl') and not pose.get('_eth')


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    sad = '_saddle' if p in ('body', 'chest') and pose.get('_saddle') else ''
    return f'{PREFIX}{p}{face}{sad}{"_eth" if pose.get("_eth") else ""}{suffix}'


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
        for _ in range(7):                                        # the ethereal veins
            x, y = rnd.randint(0, 63), rnd.randint(0, 63)
            for _s in range(rnd.randint(18, 40)):
                im.putpixel((x % 64, y % 64), hexc(glow)[:3] + (255,))
                x += rnd.choice((-1, 0, 1, 1)); y += rnd.choice((0, 1, 1))
    return im


def _bands(base, line, seed, glow=None):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im)
    for y in range(6, 64, 12):
        d.line((0, y, 63, y), fill=hexc(glow or line), width=1)
        d.line((0, y + 1, 63, y + 1), fill=tuple(min(255, v + 18) for v in hexc(base)[:3]), width=1)
    return im


def _fin(base, light, dark, seed, alpha=255):
    im = _noise(base, seed, 6); rnd = random.Random(seed)
    for x in range(64):                                          # streaks along the fin, a dark rim
        if rnd.random() < 0.35:
            for y in range(64): im.putpixel((x, y), tuple(min(255, int(v * 0.55 + c * 0.45)) for v, c in zip(im.getpixel((x, y))[:3], hexc(light)[:3])) + (255,))
    for y in range(64):
        for x in range(64):
            p = im.getpixel((x, y))
            if x < 3 or x > 60: p = hexc(dark)[:3] + (255,)
            im.putpixel((x, y), p[:3] + (alpha,))
    return im


def _mace(base, spike, seed):
    im = _noise(base, seed, 5); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(70):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); l = rnd.randint(2, 5)
        d.line((x, y, x + l, y - l), fill=hexc(spike), width=1)
    return im


def _bone(base, shade, seed):
    im = _noise(base, seed, 6)
    for y in range(64):
        for x in range(64):
            if (x + 2 * y) % 29 < 3: im.putpixel((x, y), hexc(shade)[:3] + (255,))
    return im


def _eye(base, glint, seed):
    """glossy: near-black, a soft sheen across the top, the bright glint drawn as its own box"""
    im = _noise(base, seed, 3)
    for y in range(64):
        for x in range(64):
            if y < 22: im.putpixel((x, y), tuple(min(255, v + 14 - y // 2) for v in im.getpixel((x, y))[:3]) + (255,))
    return im


def _hex(seed):
    """the honeycomb marks on his cheek: thin dark lines, the rest clear"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def hexagon(cx, cy, r):
        pts = [(cx + r * math.cos(math.radians(60 * i)), cy + r * math.sin(math.radians(60 * i))) for i in range(7)]
        d.line(pts, fill=hexc('#0a4a1a'), width=2)
    for cx, cy in ((20, 18), (38, 28), (20, 38), (38, 48), (56, 18)):
        hexagon(cx, cy, 10.5)
    return im


def _brush(base, streak, seed):
    """a brushstroke: near-black, fine lighter streaks running along it"""
    im = _noise(base, seed, 4); rnd = random.Random(seed)
    for y in range(64):
        if rnd.random() < 0.3:
            for x in range(64):
                if rnd.random() < 0.8: im.putpixel((x, y), hexc(streak))
    return im


def _leather(base, stitch, seed):
    im = _noise(base, seed, 7); d = ImageDraw.Draw(im)
    for y in (3, 60):
        for x in range(2, 62, 4): d.line((x, y, x + 1, y), fill=hexc(stitch))
    return im


def _membrane(seed):
    im = Image.new('RGBA', (64, 64)); rnd = random.Random(seed)
    for y in range(64):
        for x in range(64):
            g = 1 + rnd.uniform(-0.08, 0.08)
            im.putpixel((x, y), (int(118 * g), int(56 * g), int(226 * g), 150))
    d = ImageDraw.Draw(im)
    for _ in range(6):
        x0 = rnd.randint(0, 63)
        d.line((x0, 0, x0 + rnd.randint(-18, 18), 63), fill=(80, 255, 160, 210), width=1)
    return im


def textures():
    T = {'apo_scale': _scales(G, G_DK, G_LT, 701), 'apo_scale_dk': _scales(G_DK, '#073514', G, 702), 'apo_belly': _bands(BELLY, BELLY_DK, 703),
         'apo_fin': _fin(FIN, FIN_LT, FIN_DK, 704), 'apo_claw': _noise('#163b14', 705, 6), 'apo_mouth': _noise('#5a0b16', 706, 8),
         'apo_tongue': _noise('#7a1830', 707, 6), 'apo_fang': _noise('#efe6c4', 708, 6), 'apo_eye': _eye('#0c0c10', '#ffffff', 709),
         'apo_glint': _noise('#ffffff', 710, 2), 'apo_bag': _noise('#5e2d70', 711, 6), 'apo_lash': _noise('#060606', 712, 2),
         'apo_mace': _mace('#222226', '#4a4a54', 713), 'apo_bone': _bone('#ebe6da', '#b8b2a4', 714), 'apo_dot': _noise('#08200c', 715, 3),
         'apo_hex': _hex(716), 'apo_lid': _scales('#13702a', G_DK, G, 717), 'apo_saddle': _leather('#5a3218', '#3e200e', 718),
         'apo_strap': _leather('#3a2012', '#24120a', 719), 'apo_gold': _noise('#e2b236', 720, 14), 'apo_brow': _brush('#121214', '#202024', 741), 'apo_pupil': _noise('#f6f6f0', 743, 4)}
    # phase 2: the ethereal spectre
    T.update({'apo_scale_eth': _scales('#0a1f14', '#05100a', '#1a4a2c', 721, glow='#3cff8a'), 'apo_scale_dk_eth': _scales('#06140c', '#020804', '#12301e', 722, glow='#2ad070'),
              'apo_belly_eth': _bands('#2e4a36', '#1c3022', 723, glow='#7affb0'), 'apo_fin_eth': _fin('#3a1a6a', '#8a4aff', '#1a0a34', 724, alpha=225),
              'apo_claw_eth': _noise('#1a0a34', 725, 6), 'apo_eye_eth': _noise('#34ff94', 726, 12), 'apo_mace_eth': _mace('#141418', '#8a4aff', 727),
              'apo_bone_eth': _bone('#c8f0ff', '#7ab0c8', 728), 'apo_lid_eth': _scales('#0c2418', '#05100a', '#1a4a2c', 729, glow='#3cff8a'),
              'apo_brow_eth': _brush('#0a0a10', '#3a2a6a', 742), 'apo_pupil_eth': _noise('#06140a', 744, 3), 'apo_wing': _membrane(731), 'apo_wingbone': _noise('#1a1030', 732, 6)})
    return T


ETH_SWAP = {'apo_scale': 'apo_scale_eth', 'apo_scale_dk': 'apo_scale_dk_eth', 'apo_belly': 'apo_belly_eth', 'apo_fin': 'apo_fin_eth',
            'apo_claw': 'apo_claw_eth', 'apo_eye': 'apo_eye_eth', 'apo_mace': 'apo_mace_eth', 'apo_bone': 'apo_bone_eth', 'apo_lid': 'apo_lid_eth', 'apo_brow': 'apo_brow_eth', 'apo_pupil': 'apo_pupil_eth'}


# ---------------------------------------------------------------------------------------------------- models
def _crown(cx, base, cz, k, piv):
    """the black crown (phase59's apophiss_crown, his drop), scaled k about its band, the band's foot at (cx, base, cz)"""
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
    return [el(m(fr), m(to), TEX[t], piv, (rot[0], rot[1], m(rot[2])) if rot else None) for fr, to, t, rot in cr]


def _spike(base, tip, w0, th, tex, piv, up=SIDE, bend=(0.0, 0.0, 0.0), n=3):
    """a jagged fin spike: n tapering plates from base to tip (th thick, toward `up`), bowed by `bend` at its middle"""
    pts = []
    for i in range(n + 1):
        t = i / n; b = 4 * t * (1 - t)
        pts.append(tuple(base[k] + (tip[k] - base[k]) * t + bend[k] * b for k in range(3)))
    return chain(pts, [w0 * (1 - 0.72 * i / max(1, n - 1)) for i in range(n)], th, tex, piv, up, ext=0.35)


def _sail(a, b, tip, th, tex, piv, n=4, up=SIDE, ragged=0.18):
    """a broad fin: a triangle (base a-b, point at tip) filled with n strips fanned from the tip, its back edge ragged"""
    out = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n; tm = (t0 + t1) / 2
        q = tuple(a[k] + (b[k] - a[k]) * tm for k in range(3))
        q = tuple(q[k] + (tip[k] - q[k]) * (ragged if i % 2 else 0.0) for k in range(3))
        w = math.dist(tuple(a[k] + (b[k] - a[k]) * t0 for k in range(3)), tuple(a[k] + (b[k] - a[k]) * t1 for k in range(3)))
        L = math.dist(q, tip)
        m = tuple(q[k] + (tip[k] - q[k]) * 0.5 for k in range(3))
        out += [seg(q, m, w * 1.1, th, tex, piv, up, 0.2, shift=(0.3 * i, 0.5 * i)), seg(m, tip, w * 0.62, th, tex, piv, up, 0.2, shift=(0.6 * i, 0.2 * i))]
    return out


def _saddle(A, B, w, d, piv):
    """a leather saddle on the back of the span A-B (w wide, d deep): pad, cantle, pommel, gold trim, girth straps, stirrups"""
    z = _unit(_sub(B, A)); n = _unit((0.0, -z[2], z[1]))               # (n: out of his back)
    x = (1.0, 0.0, 0.0)
    c = _add(_mul(_add(A, B), 0.5), _mul(n, d / 2))
    L = lambda u, v, t: _add(c, _add(_mul(x, u), _add(_mul(n, v), _mul(z, t))))
    S = lambda p0, p1, ww, hh, t, up=None: seg(p0, p1, ww, hh, t, piv, up or n, 0.0)
    els = [S(L(0, 0.3, -3.4), L(0, 0.3, 3.4), 7.4, 0.8, 'apo_saddle'),                               # the seat
           S(L(0, 0.32, -3.6), L(0, 0.32, 3.6), 8.0, 0.5, 'apo_gold'),                                # (its gold edge, under)
           S(L(0, 1.2, -3.9), L(0, 1.2, -2.9), 6.6, 2.2, 'apo_saddle'), S(L(0, 2.35, -3.95), L(0, 2.35, -2.85), 6.0, 0.3, 'apo_gold'),   # the cantle
           S(L(0, 1.0, 2.9), L(0, 1.0, 3.9), 3.2, 1.8, 'apo_saddle'), S(L(0, 2.0, 3.0), L(0, 2.0, 3.8), 2.4, 0.3, 'apo_gold')]           # the pommel
    for t in (-1.8, 1.8):                                                                               # girth straps, right round him
        for side in (1, -1):
            els.append(S(L(side * (w / 2 + 0.15), -d / 2, t), L(side * (w / 2 + 0.15), 0.2, t), 0.8, 0.3, 'apo_strap', x))
        els.append(S(L(0, -d - 0.05, t - 0.4), L(0, -d - 0.05, t + 0.4), w + 0.6, 0.3, 'apo_strap'))
    for side in (1, -1):                                                                                # stirrups
        els += [S(L(side * (w / 2 + 0.35), 0.0, 0.2), L(side * (w / 2 + 0.35), -3.8, 0.2), 0.7, 0.25, 'apo_strap', x),
                S(L(side * (w / 2 + 0.6), -3.9, -0.6), L(side * (w / 2 + 0.6), -3.9, 1.0), 0.5, 0.5, 'apo_gold', x)]
    return els


def _eye_parts(sx, f, pv):
    """one eye (sx +1: his right): glossy black, rounded below, a white snake's slit for a pupil (set toward his nose, as the
    art), the purple crescent under it, the heavy upper lid edged in black, and the brow - one black brushstroke from over
    the inner corner sweeping out past the side of his head to a fine point.
    f: (lid inner y, lid outer y, brow inner y, brow outer y) or ('shut' | 'pain', brow inner y, brow outer y)"""
    X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
    E = lambda x0, y0, z0, x1, y1, z1, t, rot=None, sh=None: el((X(x0, x1)[0], y0, z0), (X(x0, x1)[1], y1, z1), t, pv, rot, shift=sh)
    out = [E(1.4, 35.4, -12.62, 6.8, 38.6, -12.3, 'apo_eye'), E(1.8, 34.95, -12.62, 6.5, 35.4, -12.3, 'apo_eye'),       # the eye, rounded below
           E(2.5, 34.6, -12.62, 5.9, 34.95, -12.3, 'apo_eye'),
           E(1.5, 34.05, -12.66, 6.8, 34.6, -12.36, 'apo_bag'), E(1.4, 34.6, -12.66, 1.8, 35.4, -12.36, 'apo_bag'),       # the purple crescent
           E(6.5, 34.6, -12.66, 6.8, 35.4, -12.36, 'apo_bag'), E(1.8, 34.6, -12.66, 2.5, 34.95, -12.36, 'apo_bag'),
           E(5.9, 34.6, -12.66, 6.5, 34.95, -12.36, 'apo_bag')]
    shut = isinstance(f[0], str)
    if shut:
        kind, bi, bo = f; yi = yo = 34.75
    else:
        yi, yo, bi, bo = f
    ang = math.degrees(math.atan2(yo - yi, 6.2)); ym = (yi + yo) / 2
    rot = lambda y: ('z', ang * sx, (sx * 4.1, y, -12.5))
    out.append(E(1.0, ym, -12.8, 7.2, ym + max(2.0, 40.0 - min(yi, yo)), -12.26, 'apo_lid', rot(ym), (0.3, 0.6)))         # the upper lid
    if shut:                                                                                                       # shut: a line across
        mid = 35.0 if kind == 'shut' else 35.7
        out += chain([(sx * 1.3, 35.45, -12.84), (sx * 4.1, mid, -12.84), (sx * 7.0, 35.45 if kind == 'shut' else 35.0, -12.84)], [0.5, 0.5], 0.3, 'apo_lash', pv, FRONT, 0.15)
        if kind == 'pain':
            out.append(seg((sx * 2.0, 36.4, -12.86), (sx * 4.4, 36.0, -12.86), 0.35, 0.25, 'apo_lash', pv, FRONT))
    else:
        out.append(E(1.0, ym - 0.45, -12.84, 7.3, ym + 0.05, -12.28, 'apo_lash', rot(ym)))                           # the lid's black line
        slim = 0.55 if yi > 38 else 0.75                                                                            # (shocked: the slit narrows)
        px = 3.3
        out += [E(px - slim / 2, 35.7, -12.68, px + slim / 2, 37.6, -12.6, 'apo_pupil'),                            # the white slit
                E(px - slim / 4, 37.6, -12.68, px + slim / 4, 38.4, -12.6, 'apo_pupil'),
                E(px - slim / 4, 35.0, -12.68, px + slim / 4, 35.7, -12.6, 'apo_pupil')]
    # the brow: thick over the inner corner, sweeping out and up past the side of his head, thinning to a point
    mid_y = (bi + bo) / 2 + 0.25
    pts = [(sx * 0.9, bi, -12.98), (sx * 4.0, mid_y, -12.98), (sx * 7.0, bo, -12.92), (sx * 8.9, bo + 0.55, -12.3), (sx * 9.7, bo + 0.95, -11.4)]
    out += chain(pts, [1.45, 1.25, 0.8, 0.42], 0.55, 'apo_brow', pv, FRONT, 0.2)
    return out


# (2.78) the skull, from the art's side view: the forehead rises behind his lids and brows and rounds over a low dome (the
# crown on top), then runs a long way back - the round back of his head - and curls under into his neck: an egg laid along
# him, longer than it is tall. Built in slices front to back: the middle one has the whole profile, the outer ones a lower
# dome and a back pulled in - so it rounds off across as well as along. Each slice: plates laid along its profile (the
# smooth outline) over blocks that fill it.
SKULL_EGG = (-3.0, 37.6, 12.6, 6.6)                                                   # (its middle (z, y), half its length, half its height)


def _egg(phis):
    """points round the egg where its surface faces angle phi (0: straight back, 90: up), so the plates turn evenly"""
    zc, yc, a, b = SKULL_EGG
    out = []
    for p in phis:
        c, s = math.cos(math.radians(p)), math.sin(math.radians(p)); d = math.hypot(a * c, b * s)
        out.append((round(zc + a * a * c / d, 3), round(yc + b * b * s / d, 3)))
    return out


SKULL = [(-9.2, 42.6), (-9.1, 43.1), (-8.85, 43.4)] + _egg([104 - 172 * i / 15 for i in range(16)])   # (z, y): from his brow to his nape
SKULL_SLICES = [(2.8, 1.0, 1.0), (4.8, 0.985, 0.975), (6.2, 0.955, 0.93), (7.4, 0.91, 0.87), (8.4, 0.84, 0.8)]   # (out to |x|, how far back, how high)


def skull(pv, z_front=-9.2):
    out = []
    x0 = 0.0
    cz, y_mid = SKULL_EGG[:2]                                                                   # (inside: for the plates' outward side)
    for si, (x1, kz, ky) in enumerate(SKULL_SLICES):
        prof = [(z_front + (z - z_front) * kz, y_mid + (y - y_mid) * ky) if y > y_mid or z > 1.6 else (z_front + (z - z_front) * kz, y) for z, y in SKULL]
        prof = [(z, max(y, 32.4)) for z, y in prof]
        if si >= 2: prof = prof[::2] + ([prof[-1]] if len(prof) % 2 == 0 else [])      # (the outer slices: half the plates)
        sides = [(1,)] if si == 0 else [(1,), (-1,)]
        for (sx,) in sides:
            xa, xb = (-x1, x1) if si == 0 else ((x0, x1) if sx > 0 else (-x1, -x0))
            xm, w = (xa + xb) / 2, xb - xa
            for i in range(len(prof) - 1):
                (za, ya), (zb, yb) = prof[i], prof[i + 1]
                dz, dy = zb - za, yb - ya
                n = _unit((0.0, -dz, dy)) if (-dz * (ya + yb - 2 * y_mid) / 2 + dy * ((za + zb) / 2 - cz)) > 0 else _unit((0.0, dz, -dy))
                A = (xm, ya - n[1] * 0.75, za - n[2] * 0.75); B = (xm, yb - n[1] * 0.75, zb - n[2] * 0.75)
                out.append(seg(A, B, w + (0.02 if si else 0.0), 1.5, 'apo_scale', pv, n, 0.3, shift=(0.13 * i + 0.3 * si, 0.21 * i + 0.17 * sx)))
            # (the fill: blocks behind the cranium's core, under the plates - each band reaching back as far as the profile
            #  does all the way up it, so no corner pokes through)
            back = lambda y: max([z for z, _ in _crossings(prof, y)] or [-99.0])
            y = round(min(yy for zz, yy in prof if zz > 1.6), 2)
            top = max(yy for zz, yy in prof)
            while y < top - 1.0:
                y1 = min(y + 1.8, top - 1.0)
                zb = min(back(y + 0.01), back((y + y1) / 2), back(y1)) - 0.25
                if zb > 1.8:
                    out.append(el((xa + (0.05 if si else 0), y, 1.4), (xb - (0.05 if si else 0), y1, zb), 'apo_scale', pv, shift=(0.6, 0.2 + 0.1 * si)))
                y = y1
        x0 = x1
    return out


def _crossings(prof, y):
    """where the profile crosses height y: [(z, y)]"""
    out = []
    for (za, ya), (zb, yb) in zip(prof, prof[1:]):
        if (ya - y) * (yb - y) <= 0 and ya != yb:
            t = (y - ya) / (yb - ya); out.append((za + (zb - za) * t, y))
    return out


def _ring(cx, cy, cz, R, w, h, a0, a1, n, tex, piv, ext=0.9, dy=None):
    """a coil: n boxes round a circle (angle 0 = his front, +90 = his right), dy(t) lifting it along the way"""
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n); y = cy + (dy(i / n) if dy else 0.0)
        pts.append((cx + R * math.sin(a), y, cz - R * math.cos(a)))
    return [seg(pts[i], pts[i + 1], w, h, tex, piv, UP, ext, shift=(0.29 * i, 0.53 * i)) for i in range(n)], pts


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

    # ---- the coil: one rounded loop on the ground, open in the middle - his light belly round its inside, fins along its top.
    #      The body comes down into its front; the right half rides up over the left at the back, where it runs on into the tail
    pv = PIVOT['coil']; cz = 5.4; R = 9.4
    lift = lambda t: 0.9 * math.sin(math.pi * min(1.0, t) / 2)
    rt, rp_ = _ring(0, 3.1, cz, R, 6.8, 6.2, 0, 180, 8, 'apo_scale', pv, dy=lift)                # (his right half: rising to the back)
    lt, lp_ = _ring(0, 2.8, cz, R - 0.3, 6.6, 5.6, 180, 360, 8, 'apo_scale', pv)                  # (the left half: lower, passing under)
    coil = rt + lt
    caps, _ = _ring(0, 6.5, cz, R, 4.6, 1.4, 0, 180, 8, 'apo_scale_dk', pv, dy=lift)              # rounding over the top
    caps2, _ = _ring(0, 5.9, cz, R - 0.3, 4.4, 1.2, 180, 360, 8, 'apo_scale_dk', pv)
    coil += caps + caps2
    for half, (a0, r0, y0, hh) in enumerate(((0, R, 3.1, 6.2), (180, R - 0.3, 2.8, 5.6))):        # the belly, round the inside
        for i in range(8):
            t0, t1 = math.radians(a0 + 22.5 * i), math.radians(a0 + 22.5 * (i + 1)); ri = r0 - 3.45
            yy = y0 + (lift((i + 0.5) / 8) if half == 0 else 0.0)
            A = (ri * math.sin(t0), yy - 0.5, cz - ri * math.cos(t0)); B = (ri * math.sin(t1), yy - 0.5, cz - ri * math.cos(t1))
            coil.append(seg(A, B, 0.3, hh - 1.6, 'apo_belly', pv, UP, 0.6))
    for a in (120, 150, 180):                                                                     # fins along the top of the right half
        sn, cs = math.sin(math.radians(a)), math.cos(math.radians(a)); y = 7.0 + lift(a / 180)
        b0 = (R * sn, y, cz - R * cs); d = (cs, 0.0, sn)                                         # (d: along the coil)
        coil += _sail(_add(b0, _mul(d, -1.6)), _add(b0, _mul(d, 1.6)), (b0[0] + 0.6 * sn, y + 3.4, b0[2] - 0.6 * cs + 1.2), 0.7, 'apo_fin', pv, 3, up=(sn, 0.0, -cs))
    part('apo_coil', coil)

    # ---- the body: rearing up out of the coil in an S, thick; the light belly plate down its front, sails down its back.
    #      Saddled (the follower, ridden): the saddle sits on the middle of it and the sails there are gone
    pv = PIVOT['body']
    spine = [(0, 3.4, -3.2), (0, 8.4, -5.6), (0, 13.2, -5.3), (0, 17.2, -3.2), (0, 21.0, -2.4)]
    ws, ds = [11.6, 11.0, 10.6, 10.6], [9.8, 9.4, 9.2, 9.2]
    def body(saddle=False):
        els = []
        for i in range(4):
            A, B = spine[i], spine[i + 1]
            els.append(seg(A, B, ws[i], ds[i], 'apo_scale', pv, FRONT, 0.6, shift=(0.3 * i, 0.7 * i)))
            n = _unit((0.0, B[2] - A[2], -(B[1] - A[1])))             # (the front of this span)
            els.append(seg(_add(A, _mul(n, ds[i] / 2)), _add(B, _mul(n, ds[i] / 2)), 6.6, 0.4, 'apo_belly', pv, FRONT, 0.45))
            if i and not (saddle and i >= 2):                            # a sail off the back of each upper span
                ba, bb = _add(A, _mul(n, -ds[i] / 2 + 0.3)), _add(B, _mul(n, -ds[i] / 2 + 0.3))
                els += _sail(ba, bb, (0, bb[1] + 1.4 + 0.6 * i, bb[2] + 4.0 + 0.9 * i), 0.8, 'apo_fin', pv, 3)
        if saddle:
            els += _saddle(spine[2], spine[3], ws[2], ds[2], pv)
        return els
    part('apo_body', body()); part('apo_body_saddle', body(True))

    # ---- the chest: broad, the shoulders' bulk, the belly plate up to the chin, a fin over the back
    pv = PIVOT['chest']
    # (2.78: the neck sets back as it rises - its throat slopes in under his jaw - so the jaw can drop open in front of it
    #  instead of sinking into it: the art's big head held out over a slimmer throat)
    TH = _unit((0.0, 0.62, -0.78))                                                                    # (the throat's slope, facing out)
    chest = [seg((0, 18.8, -2.6), (0, 24.8, -2.4), 12.6, 9.6, 'apo_scale', pv, FRONT, 0.4),
             el((-7.8, 23.6, -7.3), (7.8, 26.4, 2.3), 'apo_scale', pv, shift=(0.2, 0.4)),            # the shoulders' bulk
             el((-7.8, 26.2, -3.9), (7.8, 29.6, 2.3), 'apo_scale', pv, shift=(0.5, 0.3)),            # the neck, set back
             seg((0, 25.3, -6.5), (0, 29.0, -3.55), 15.4, 2.4, 'apo_scale', pv, TH, 0.3),           # its throat, sloping in
             el((-6.6, 29.4, -3.4), (6.6, 30.8, 1.4), 'apo_scale', pv, shift=(0.6, 0.1)),
             el((-4.6, 19.4, -7.75), (4.6, 25.9, -7.25), 'apo_belly', pv),                           # the belly plate, and up the throat
             seg((0, 25.75, -7.62), (0, 29.65, -4.52), 9.2, 0.5, 'apo_belly', pv, TH, 0.25)]
    part('apo_chest_saddle', chest + [el((-2.0, 22.0, 2.2), (2.0, 27.0, 2.6), 'apo_strap', pv), el((-1.2, 22.6, 2.5), (1.2, 26.4, 2.8), 'apo_gold', pv)])   # (a breastplate strap)
    for y0, y1, l in ((19.4, 23.4, 5.0), (23.0, 27.4, 6.2), (26.6, 30.4, 7.0)):
        chest += _sail((0, y0, 2.0), (0, y1, 2.0), (0, y1 + 1.6, 2.0 + l), 0.8, 'apo_fin', pv, 3)
    part('apo_chest', chest)

    # ---- the head (and its faces): the art's - a great round head, his eyes up on a high brow, and under them a short, broad
    #      muzzle (about an eye's width out) with a blunt rounded nose: two small nostrils at its tip, scowl creases on its
    #      bridge, the upper lip dipping to a lobe between the two great fangs. The jaw muscles bulge at the back
    def head(face=None):
        pv = PIVOT['head']; E = lambda fr, to, t='apo_scale', rot=None, sh=None: el(fr, to, t, pv, rot, shift=sh)
        h = [E((-8.4, 32.4, -9.2), (8.4, 42.6, 1.6), sh=(0.1, 0.3)),                                                      # the cranium's core
             E((8.2, 32.8, -8.8), (9.2, 40.6, 0.4), sh=(0.3, 0.9)), E((-9.2, 32.8, -8.8), (-8.2, 40.6, 0.4), sh=(0.7, 0.4))]   # the jaw muscles
        h += skull(pv)
        # the muzzle (the art's): a broad mound under the eyes - narrow over the bridge, its cheeks sloping out and down to a
        # wide lip - rounding in to a blunt nose about an eye's width out; blocks inside, a skin of plates over them
        Z = (-9.2, -12.4, -14.4, -15.3)                                                                 # (from the face to the nose)
        BW, BY = (3.0, 2.8, 2.5, 2.2), (36.05, 35.8, 35.3, 34.7)                                       # the bridge: half-width, top
        LW, LY = (7.6, 7.0, 6.0, 4.7), (34.0, 33.9, 33.7, 33.4)                                        # the lip: half-width, its top
        def ip(vals, z):
            z = min(Z[0], max(Z[-1], z)); i = next(i for i in range(3) if Z[i + 1] <= z <= Z[i])
            return vals[i] + (vals[i + 1] - vals[i]) * (Z[i] - z) / (Z[i] - Z[i + 1])
        def surf(x, z):                                                                                  # (the skin's height there)
            bw, by, lw, ly = ip(BW, z), ip(BY, z), ip(LW, z), ip(LY, z)
            return by if abs(x) <= bw else by - (abs(x) - bw) / (lw - bw) * (by - ly)
        MZ = [(7.6, -12.4, -9.0), (7.0, -14.0, -12.2), (6.0, -15.0, -13.8), (4.7, -15.5, -14.8)]        # the lip, all round: (half-width, front, back)
        h += [E((-w, 32.4, z0), (w, ip(LY, z0) + 0.1, z1), sh=(0.2 + 0.3 * i, 0.7 - 0.15 * i)) for i, (w, z0, z1) in enumerate(MZ)]
        for i in range(3):                                                                              # the core, under the skin
            for xw in (BW[i + 1], (BW[i + 1] + LW[i + 1]) / 2):
                h.append(E((-xw, 33.3, Z[i + 1]), (xw, surf(xw, Z[i + 1]) - 0.3, Z[i] + 0.2), sh=(0.3 * i, 0.4)))
        for i in range(3):                                                                              # the cheeks: a plate each side
            for sx in (1, -1):
                P0, P1 = (sx * BW[i], BY[i], Z[i]), (sx * BW[i + 1], BY[i + 1], Z[i + 1])
                Q0, Q1 = (sx * LW[i], LY[i], Z[i]), (sx * LW[i + 1], LY[i + 1], Z[i + 1])
                a_, b_ = _sub(Q0, P0), _sub(P1, P0)
                n = _unit((a_[1] * b_[2] - a_[2] * b_[1], a_[2] * b_[0] - a_[0] * b_[2], a_[0] * b_[1] - a_[1] * b_[0]))
                n = n if n[1] > 0 else _mul(n, -1)
                M0, M1 = _sub(_mul(_add(P0, Q0), 0.5), _mul(n, 0.25)), _sub(_mul(_add(P1, Q1), 0.5), _mul(n, 0.25))
                w = (math.dist(P0, Q0) + math.dist(P1, Q1)) / 2 + 0.3
                h.append(seg(M0, M1, w, 0.5, 'apo_scale', pv, n, 0.15, shift=(0.2 + 0.3 * i, 0.5 + 0.2 * sx)))
        SK = [(0, BY[0] - 0.25, Z[0]), (0, BY[1] - 0.25, Z[1]), (0, BY[2] - 0.25, Z[2]), (0, BY[3] - 0.25, Z[3]),      # the bridge, over the
              (0, 34.0, -15.55), (0, 33.45, -15.72), (0, 32.85, -15.78)]                                                # nose and down its front
        h += chain(SK, [6.6, 6.2, 5.6, 6.4, 7.8, 9.2], 0.5, 'apo_scale', pv, UP)
        for sx in (1, -1):                                                                              # (rounding the nose's corners)
            h.append(seg((sx * 3.5, 34.0, -15.12), (sx * 4.25, 33.35, -15.55), 2.2, 0.5, 'apo_scale', pv, _unit((0.55 * sx, 0.55, -0.62)), 0.2))
        for w, z0, z1 in MZ:                                                                            # the dark edge of his upper lip
            h += [E((w - 0.05, 32.4, z0), (w + 0.1, 33.0, z1), 'apo_scale_dk'), E((-w - 0.1, 32.4, z0), (-w + 0.05, 33.0, z1), 'apo_scale_dk')]
        h += [E((-4.6, 32.4, -15.62), (4.6, 33.0, -15.5), 'apo_scale_dk'),
              E((-2.3, 31.75, -16.0), (2.3, 33.1, -14.9), sh=(0.3, 0.1)), E((-2.35, 31.7, -16.05), (2.35, 32.1, -15.9), 'apo_scale_dk')]   # the lobe of his lip
        for sx in (1, -1):                                                                              # two small nostrils, low on the nose
            X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
            h.append(E((X(0.75, 1.85)[0], 33.5, -16.06), (X(0.75, 1.85)[1], 33.92, -15.9), 'apo_dot', ('z', 16 * sx, (sx * 1.3, 33.7, -16.0))))
        # the frown: one dark crease arching over the top of the muzzle just under his eyes, and a little knot of scales under it
        for sx in (1, -1):
            h.append(seg((sx * 6.9, surf(6.9, -9.55) + 0.05, -9.55), (sx * 2.9, surf(2.9, -9.55) + 0.05, -9.55), 0.34, 0.14, 'apo_scale_dk', pv, (0.45 * sx, 0.89, 0.0), 0.1))
        h.append(E((-2.95, BY[0] - 0.01, -9.72), (2.95, BY[0] + 0.12, -9.38), 'apo_scale_dk'))
        for x, z, k in ((0.0, -10.3, 1.0), (-0.95, -10.9, 0.8), (0.95, -10.9, 0.8), (0.0, -11.5, 0.7)):
            y = surf(x, z)
            h.append(E((x - 0.5 * k, y - 0.1, z - 0.4 * k), (x + 0.5 * k, y + 0.16, z + 0.4 * k), 'apo_scale_dk'))
        # the eyes (the art's), up on his brow over the snout: glossy black with white slit pupils, a purple crescent under each,
        # a heavy upper lid edged in black sloping down to his nose (the scowl), and over each a black brushstroke brow. Per face,
        # per side:
        F = {None: ((36.5, 37.9, 37.5, 39.7), (36.5, 37.9, 37.5, 39.7)),                 # (lid in, lid out, brow in, brow out)
             'smug': ((36.4, 36.5, 38.7, 39.5), (36.9, 37.6, 37.9, 39.4)),
             'shock': ((38.8, 38.8, 39.8, 40.0), (38.8, 38.8, 39.8, 40.0)),
             'hurt': ((36.2, 37.9, 37.2, 39.9), ('pain', 37.3, 38.9)),
             'tired': ((36.1, 35.8, 37.5, 37.1), (36.1, 35.8, 37.5, 37.1)),
             'blink': (('shut', 37.7, 38.4), ('shut', 37.7, 38.4))}[face]
        for sx in (1, -1):
            h += transform(_eye_parts(sx, F[0 if sx > 0 else 1], pv), lambda p: (p[0], p[1] + EYE_UP, p[2] + EYE_BACK))
        for x, y in ((6.3, 35.25), (6.95, 35.75), (7.3, 34.95)):                                       # the freckles on his right cheek
            h.append(E((x, y, -9.27), (x + 0.45, y + 0.45, -9.19), 'apo_dot'))
        h.append(el((-9.32, 33.8, -8.0), (-9.24, 39.6, -2.0), 'apo_hex', pv, faces=('west',)))         # the honeycomb on his left
        h += [E((-7.0, 32.25, -12.2), (7.0, 32.45, 0.8), 'apo_mouth'), E((-6.4, 32.25, -13.8), (6.4, 32.45, -12.0), 'apo_mouth'),   # the roof of his maw
              E((-5.4, 32.25, -14.8), (5.4, 32.45, -13.6), 'apo_mouth'), E((-4.0, 32.25, -15.3), (4.0, 32.45, -14.6), 'apo_mouth')]
        # the teeth: the two great fangs hanging either side of the lobe, in front of his chin, and a row down each side
        # hanging just outside the lower jaw
        for sx in (1, -1):
            X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
            h += [E((X(2.45, 3.35)[0], 30.9, -15.85), (X(2.45, 3.35)[1], 32.6, -15.05), 'apo_fang'), E((X(2.6, 3.2)[0], 30.0, -15.75), (X(2.6, 3.2)[1], 31.0, -15.15), 'apo_fang'),
                  E((X(2.72, 3.08)[0], 29.3, -15.65), (X(2.72, 3.08)[1], 30.1, -15.25), 'apo_fang')]
            for w, z in ((6.45, -13.1), (7.05, -11.4), (7.05, -9.8), (8.05, -7.4)):
                h.append(E((X(w, w + 0.38)[0], 31.5, z), (X(w, w + 0.38)[1], 32.45, z + 0.55), 'apo_fang'))
        h += _crown(*CROWN_AT, CROWN_K, pv)
        # the crest: great layered sails swept back off the back of his head, the tallest from just behind the crown
        h += _sail((0, 43.5, 0.0), (0, 39.0, 8.6), (0, 50.6, 13.6), 0.9, 'apo_fin', pv, 5)
        h += _sail((0, 42.2, 5.2), (0, 37.4, 9.3), (0, 46.8, 16.2), 0.9, 'apo_fin', pv, 4)
        h += _sail((0, 38.6, 9.2), (0, 34.6, 8.8), (0, 41.2, 16.6), 0.9, 'apo_fin', pv, 3)
        for sx in (1, -1):
            h += _sail((sx * 4.4, 43.2, 1.6), (sx * 4.8, 39.0, 7.4), (sx * 7.4, 48.8, 11.8), 0.8, 'apo_fin', pv, 4)
            h += _sail((sx * 6.0, 40.6, 5.0), (sx * 6.2, 36.4, 6.6), (sx * 9.2, 43.6, 13.2), 0.8, 'apo_fin', pv, 3)
        return h
    part('apo_head', head())
    for f in FACES:
        part(f'apo_head_x{f}', head(f))

    # ---- the jaw: heavy and round under the muzzle, its chin tucked just behind the great fangs; the light throat, the red
    #      floor, the lower fangs (standing inside his lip), and the forked tongue lolling out of the corner of his mouth
    pv = PIVOT['jaw']; E = lambda fr, to, t='apo_scale', sh=None: el(fr, to, t, pv, shift=sh)
    JW = [(8.0, 28.4, -9.0, -3.6), (7.0, 28.6, -12.0, -8.8), (6.2, 28.9, -13.6, -11.8), (5.0, 29.3, -14.4, -13.4), (3.4, 29.7, -15.0, -14.2)]   # (half-width, bottom, front, back)
    jaw = [E((-w, y0, z0), (w, 32.2, z1), sh=(0.2 + 0.2 * i, 0.2 + 0.17 * i)) for i, (w, y0, z0, z1) in enumerate(JW)]
    # (2.78: the back of his jaw rounds up to the hinge - no corner hanging under it to swing back into his neck as he opens
    #  wide, and a round jaw from the side, as the art)
    JB = [(-3.9, 28.35), (-2.5, 28.65), (-1.2, 29.3), (-0.15, 30.25), (0.55, 31.4), (0.75, 32.15)]                        # (z, y): its underside, up to the hinge
    for i in range(len(JB) - 1):
        (za, ya), (zb, yb) = JB[i], JB[i + 1]
        n = _unit((0.0, -(zb - za), (yb - ya)))
        n = n if n[1] < 0 or n[2] > 0 else _mul(n, -1)
        jaw.append(seg((0.0, ya - n[1] * 0.6, za - n[2] * 0.6), (0.0, yb - n[1] * 0.6, zb - n[2] * 0.6), 15.6 - 0.5 * i, 1.2, 'apo_scale', pv, n, 0.25,
                       shift=(0.3 * i, 0.2)))
    jaw += [E((-7.8, 29.0, -3.8), (7.8, 32.2, -1.0), sh=(0.5, 0.3)), E((-7.6, 30.0, -1.2), (7.6, 32.2, 0.4), sh=(0.7, 0.6))]   # (filling it)
    jaw += [E((7.9, 29.6, -5.8), (8.6, 32.1, -0.2), sh=(0.1, 0.8)), E((-8.6, 29.6, -5.8), (-7.9, 32.1, -0.2), sh=(0.9, 0.3)),
            E((-6.8, 27.8, -8.6), (6.8, 28.5, -3.8), sh=(0.6, 0.5))]
    jaw += [E((-w + 1.0, y0 - 0.15, z0 + 0.3), (w - 1.0, y0 + 0.05, z1 - 0.3), 'apo_belly') for w, y0, z0, z1 in JW[1:]] + \
           [E((-5.6, 27.65, -8.4), (5.6, 27.85, -3.9), 'apo_belly')]
    jaw += [E((-w + 0.6, 32.1, z0 + 0.3), (w - 0.6, 32.25, z1 if z1 < 0 else 0.4), 'apo_mouth') for w, y0, z0, z1 in JW]
    for sx in (1, -1):
        X = lambda a, b: (min(a * sx, b * sx), max(a * sx, b * sx))
        jaw += [E((X(2.3, 3.0)[0], 32.1, -14.85), (X(2.3, 3.0)[1], 33.4, -14.25), 'apo_fang'), E((X(2.45, 2.85)[0], 33.3, -14.75), (X(2.45, 2.85)[1], 34.0, -14.35), 'apo_fang'),
                E((X(4.3, 4.8)[0], 32.1, -13.6), (X(4.3, 4.8)[1], 33.0, -13.1), 'apo_fang'),
                E((X(5.6, 6.0)[0], 32.1, -11.6), (X(5.6, 6.0)[1], 32.9, -11.1), 'apo_fang'), E((X(6.4, 6.8)[0], 32.1, -8.4), (X(6.4, 6.8)[1], 32.9, -7.9), 'apo_fang')]
    # (the tongue: along the floor of his mouth and out over the corner of his lip on his left, hanging there, forked)
    jaw += chain([(-1.0, 32.28, -8.0), (-2.4, 32.3, -12.4), (-4.3, 32.32, -14.7), (-4.7, 31.1, -15.2), (-4.85, 29.7, -15.3)], [1.7, 1.6, 1.4, 1.25], 0.5, 'apo_tongue', pv, UP)
    jaw += chain([(-4.85, 29.9, -15.3), (-4.3, 28.6, -15.35)], [0.55], 0.4, 'apo_tongue', pv, UP) + chain([(-4.85, 29.9, -15.3), (-5.6, 28.7, -15.3)], [0.55], 0.4, 'apo_tongue', pv, UP)
    part('apo_jaw', jaw)

    # ---- arms: a great shoulder, the upper arm, the forearm bent forward at the elbow with its jagged web, a broad hand and
    #      four hooked claws (and a thumb)
    def arm(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']
        Mx = lambda p: (p[0] * sx, p[1], p[2])
        S = lambda A, B, w, h, t='apo_scale', up=FRONT, ext=0.3, sh=None: seg(Mx(A), Mx(B), w, h, t, pv, Mx(up), ext, shift=sh)
        E = lambda fr, to, t='apo_scale', sh=None: el((min(fr[0] * sx, to[0] * sx), fr[1], fr[2]), (max(fr[0] * sx, to[0] * sx), to[1], to[2]), t, pv, shift=sh)
        els = [E((6.2, 22.2, -6.8), (12.2, 29.0, 0.6), sh=(0.3, 0.2)), E((6.8, 28.8, -6.0), (11.6, 29.8, -0.2), sh=(0.6, 0.7)),
               S((9.9, 24.0, -3.0), (10.6, 17.6, -3.4), 5.8, 5.6, sh=(0.2, 0.5)),
               E((8.0, 16.0, -6.0), (13.0, 20.0, -1.0), sh=(0.8, 0.1))]
        el_, wr = (10.5, 18.0, -3.6), (10.8, 13.2, -10.6)
        mid = _mul(_add(el_, wr), 0.5)
        els += [S(el_, mid, 5.2, 5.0, sh=(0.1, 0.9)), S(mid, wr, 4.4, 4.2, sh=(0.7, 0.3))]
        for t, l in ((0.25, 3.6), (0.55, 3.0), (0.85, 2.2)):                                     # the web: jagged, off the outer forearm
            b = tuple(el_[k] + (wr[k] - el_[k]) * t for k in range(3)); b = (b[0] + 2.0, b[1], b[2])
            els += [S(b, (b[0] + l * 0.75, b[1] + l * 0.45, b[2] + l * 0.55), 1.8, 0.6, 'apo_scale_dk', FRONT, 0.4),
                    S((b[0] + l * 0.6, b[1] + l * 0.36, b[2] + l * 0.44), (b[0] + l * 1.05, b[1] + l * 0.5, b[2] + l * 0.95), 0.9, 0.5, 'apo_scale_dk', FRONT, 0.3)]
        d = _unit(_sub(wr, el_)); x, y, z = frame(d, UP)                                          # the hand, in its own frame
        L = lambda u, v, w: _add(wr, _add(_mul(x, u), _add(_mul(y, v), _mul(z, w))))
        els.append(S(L(0, 0, -0.4), L(0, 0, 2.8), 5.2, 2.8, 'apo_scale', y, 0.2))
        for i in range(4):
            u = -1.95 + 1.3 * i
            els += [S(L(u, 0.2, 2.6), L(u * 1.1, -0.2, 4.8), 0.95, 0.95, 'apo_claw', y, 0.2),
                    S(L(u * 1.1, -0.2, 4.8), L(u * 1.15, -1.8, 6.2), 0.75, 0.7, 'apo_claw', y, 0.2),
                    S(L(u * 1.15, -1.8, 6.2), L(u * 1.15, -3.2, 6.4), 0.5, 0.5, 'apo_claw', y, 0.15)]
        els += [S(L(-2.6, 0.0, 0.6), L(-3.8, -0.6, 2.4), 0.9, 0.9, 'apo_claw', y, 0.2), S(L(-3.8, -0.6, 2.4), L(-4.2, -1.8, 3.4), 0.6, 0.6, 'apo_claw', y, 0.15)]
        return els
    part('apo_armr', arm(1)); part('apo_arml', arm(-1))

    # ---- the tail: three tapering lengths out of the coil's back - belly under, small fins over; the mace at its end
    for name, (A, B, w0, w1, h0, h1, nf) in (('tail1', ((2.0, 3.0, 12.8), (2.4, 3.0, 24.6), 7.0, 6.4, 6.2, 5.8, 2)),
                                            ('tail2', ((2.4, 3.0, 24.6), (2.6, 3.0, 35.4), 6.2, 5.4, 5.6, 5.0, 2)),
                                            ('tail3', ((2.6, 3.0, 35.4), (2.7, 3.0, 45.2), 5.2, 4.4, 4.8, 4.2, 2)),
                                            ('tail4', ((2.7, 3.0, 45.2), (2.75, 3.0, 54.0), 4.2, 3.4, 4.0, 3.2, 1))):
        pv = PIVOT[name]; m = _mul(_add(A, B), 0.5)
        els = [seg(A, m, w0, h0, 'apo_scale', pv, UP, 0.5, shift=(0.2, 0.3)), seg(m, B, w1, h1, 'apo_scale', pv, UP, 0.5, shift=(0.7, 0.6)),
               seg((A[0], A[1] - h0 / 2 + 0.05, A[2]), (B[0], B[1] - h1 / 2 + 0.05, B[2]), w1 * 0.62, 0.3, 'apo_belly', pv, UP, 0.2)]
        for i in range(nf):
            t = (i + 0.5) / nf; b = tuple(A[k] + (B[k] - A[k]) * t for k in range(3)); b = (b[0], b[1] + (h0 + (h1 - h0) * t) / 2 - 0.2, b[2])
            els += _spike(b, (b[0], b[1] + 2.6 - 0.4 * i, b[2] + 2.8), 2.6, 0.6, 'apo_fin', pv)
        part(f'apo_{name}', els)
    pv = PIVOT['mace']; c = (2.75, 3.0, 58.2)
    mace = [seg((2.75, 3.0, 53.6), (2.75, 3.0, 55.4), 3.2, 3.2, 'apo_scale_dk', pv, UP),
            el(_sub(c, (3.5, 3.5, 3.5)), _add(c, (3.5, 3.5, 3.5)), 'apo_mace', pv)]
    for ax in ('x', 'y', 'z'):                                                                       # the spiky bulk
        mace.append(el(_sub(c, (3.0, 3.0, 3.0)), _add(c, (3.0, 3.0, 3.0)), 'apo_mace', pv, (ax, 45, c), shift=(0.3, 0.5)))
    dirs = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)] + [(a, b, cc) for a in (1, -1) for b in (1, -1) for cc in (1, -0.4)]
    for dv in dirs:                                                                                  # spikes, every way
        dv = _unit(dv)
        mace += chain([_add(c, _mul(dv, 3.2)), _add(c, _mul(dv, 5.0)), _add(c, _mul(dv, 6.0))], [1.3, 0.6], 1.3, 'apo_mace', pv, UP if abs(dv[1]) < 0.9 else FRONT)
    for k in range(2):                                                                               # white crescents: two across the tail...
        pts = []
        for i in range(6):
            t = i / 5; r = 3.0 + 8.6 * t; a = math.radians(180 * k + 20 + 80 * t)
            pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2] + 0.4 * t))
        mace += chain(pts, [2.8, 2.6, 2.1, 1.5, 0.7], 0.8, 'apo_bone', pv, (0.0, 0.0, 1.0), ext=0.3)
    for k in (1, -1):                                                                                # ...and two hooked along it, up and down
        pts = []
        for i in range(6):
            t = i / 5; r = 3.0 + 7.8 * t; a = math.radians(70 * t)
            pts.append((c[0], c[1] + k * r * math.cos(a) * 0.95, c[2] + r * math.sin(a) * 0.9 - 0.6))
        mace += chain(pts, [2.6, 2.4, 1.9, 1.3, 0.6], 0.8, 'apo_bone', pv, (1.0, 0.0, 0.0), ext=0.3)
    part('apo_mace', mace)

    # ---- (phase 2) the wings: a bony arm from his back, four long fingers, the violet membrane strung between them in fans
    def wing(sx):
        pv = PIVOT['wingr' if sx > 0 else 'wingl']; K = 0.82
        P = lambda p: (pv[0] + sx * (p[0] - 4.4) * K, pv[1] + (p[1] - 26.4) * K, pv[2] + (p[2] - 2.0) * K)          # (drawn about the old root, (4.4, 26.4, 2.0))
        S0, E0, W0 = P((4.4, 26.4, 2.0)), P((13.0, 32.4, 4.6)), P((22.0, 36.4, 6.0))
        F = [P((37.0, 39.0, 7.4)), P((35.0, 27.0, 8.0)), P((29.0, 17.4, 7.4)), P((19.4, 12.6, 6.0))]
        T0 = P((6.4, 15.6, 3.2))
        n = (0.0, 0.0, 1.0)                                                                          # (the wing's plane faces back)
        els = [seg(S0, E0, 1.9, 1.9, 'apo_wingbone', pv, n, 0.4), seg(E0, W0, 1.6, 1.6, 'apo_wingbone', pv, n, 0.4),
               seg(W0, _add(W0, (sx * 0.6, 2.4, 0.2)), 0.9, 0.9, 'apo_wingbone', pv, n, 0.2)]                 # the thumb's hook
        for f in F:
            m = _mul(_add(W0, f), 0.5)
            els += [seg(W0, m, 1.1, 1.1, 'apo_wingbone', pv, n, 0.3), seg(m, f, 0.7, 0.7, 'apo_wingbone', pv, n, 0.3)]
        def fan(cen, a, b, k):                                                                        # membrane strips from cen to the edge a-b
            out = []
            for i in range(k):
                t0, t1 = i / k, (i + 1) / k; tm = (t0 + t1) / 2
                q = tuple(a[j] + (b[j] - a[j]) * tm for j in range(3))
                q = tuple(q[j] + (cen[j] - q[j]) * 0.12 * math.sin(math.pi * tm) for j in range(3))       # (scalloped between the fingers)
                wid = math.dist(tuple(a[j] + (b[j] - a[j]) * t0 for j in range(3)), tuple(a[j] + (b[j] - a[j]) * t1 for j in range(3)))
                out.append(seg(cen, q, wid * 1.05, 0.3, 'apo_wing', pv, n, 0.0))
            return out
        els += fan(W0, F[0], F[1], 5) + fan(W0, F[1], F[2], 5) + fan(W0, F[2], F[3], 4) + fan(E0, F[3], T0, 4) + fan(S0, E0, T0, 2)
        return els
    part('apo_wingr', wing(1), WING_K); part('apo_wingl', wing(-1), WING_K)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# Display-frame rotations (a pose names each joint's own bend; children ride along):
#   body/chest/head: +x leans forward (head: nods down), -x rears back; +y turns to his left; +z rolls to his right
#   jaw: +x opens.   arms: -x swings forward/up, -z (right arm) / +z (left arm) out to the side
#   tail (it trails behind): +x lifts it, +y swings it to his right.  coil: +y turns all of him to his left
def P(**kw):
    return kw


TAIL_HIGH = dict(tail1=qs(('x', 26), ('y', 8)), tail2=qs(('x', 34)), tail3=qs(('x', 36)), mace=qs(('x', 24)))        # curled up behind him, the mace high
POSES = {
    # (2.77d: with the snout his head is tipped a little further down in the standing and fighting poses - glaring down at you,
    #  his eyes clear of the muzzle from the ground)
    # idle: reared up, regal, claws half raised, the mace swaying high behind; a slow breath (a/b)
    'idle_a': P(body=qs(('x', -3)), chest=qs(('x', 5)), head=qs(('x', 6)), jaw=qs(('x', 12)), armr=qs(('x', -26), ('z', -16)), arml=qs(('x', -22), ('z', 14)), **TAIL_HIGH),
    'idle_b': P(_off=(0, -0.3, 0), body=qs(('x', -1)), chest=qs(('x', 7)), head=qs(('x', 10), ('y', 6)), jaw=qs(('x', 8)), armr=qs(('x', -22), ('z', -14)), arml=qs(('x', -18), ('z', 12)),
                tail1=qs(('x', 24), ('y', 14)), tail2=qs(('x', 34), ('y', 6)), tail3=qs(('x', 36)), mace=qs(('x', 30))),
    # slither: low and forward, the tail swinging side to side behind (a/b)
    'slither_a': P(coil=qs(('y', 8)), body=qs(('x', 22), ('y', -6)), chest=qs(('x', 12)), head=qs(('x', -28), ('y', -4)), jaw=qs(('x', 8)),
                   armr=qs(('x', -50), ('z', -10)), arml=qs(('x', -30), ('z', 10)), tail1=qs(('x', 6), ('y', -26)), tail2=qs(('y', 30)), tail3=qs(('y', 28), ('x', 8)), mace=qs(('x', 10))),
    'slither_b': P(coil=qs(('y', -8)), body=qs(('x', 22), ('y', 6)), chest=qs(('x', 12)), head=qs(('x', -28), ('y', 4)), jaw=qs(('x', 8)),
                   armr=qs(('x', -30), ('z', -10)), arml=qs(('x', -50), ('z', 10)), tail1=qs(('x', 6), ('y', 26)), tail2=qs(('y', -30)), tail3=qs(('y', -28), ('x', 8)), mace=qs(('x', 10))),
    # battle: hunched in, claws out wide, maw open, the mace poised over his head like a scorpion's sting
    'battle': P(_off=(0, -0.4, 0), body=qs(('x', 12)), chest=qs(('x', 10)), head=qs(('x', -10)), jaw=qs(('x', 26)), armr=qs(('x', -50), ('z', -40)), arml=qs(('x', -50), ('z', 40)),
                tail1=qs(('x', 80)), tail2=qs(('x', 30)), tail3=I, tail4=I, mace=I),
    # the claw: a raking swipe - wound up to his right, then across
    'claw_up': P(body=qs(('x', 6), ('y', -14)), chest=qs(('y', -16), ('x', 4)), head=qs(('y', 8)), jaw=qs(('x', 16)), armr=qs(('x', -120), ('z', -50)), arml=qs(('x', -30), ('z', 40)), **TAIL_HIGH),
    'claw': P(body=qs(('x', 16), ('y', 18)), chest=qs(('y', 20), ('x', 8)), head=qs(('y', -14), ('x', -20)), jaw=qs(('x', 14)), armr=qs(('x', -80), ('z', 14)), arml=qs(('x', -40), ('z', 40)),
              tail1=qs(('x', 20), ('y', -20)), tail2=qs(('x', 26), ('y', -10)), tail3=qs(('x', 30)), mace=qs(('x', 20))),
    # the bite: a lunge, the maw gaping
    'bite': P(_off=(0, -0.6, -2), body=qs(('x', 30)), chest=qs(('x', 22)), head=qs(('x', -30)), jaw=qs(('x', 48)), armr=qs(('x', -70), ('z', -30)), arml=qs(('x', -70), ('z', 30)),
              tail1=qs(('x', 14)), tail2=qs(('x', 20)), tail3=qs(('x', 24)), mace=qs(('x', 10))),
    # the mace: raised high overhead and over (the wind-up), then brought crashing down beside him
    'mace_up': P(body=qs(('x', -12)), chest=qs(('x', -4)), head=qs(('x', -6)), jaw=qs(('x', 20)), armr=qs(('x', -130), ('z', -14)), arml=qs(('x', -40), ('z', 30)),
                 tail1=qs(('x', 56), ('y', 24)), tail2=qs(('x', 40)), tail3=qs(('x', 10)), tail4=I, mace=I),
    'mace_slam': P(_off=(0, -0.6, 0), body=qs(('x', 18), ('y', -10)), chest=qs(('x', 14), ('y', -8)), head=qs(('x', -12), ('y', 8)), jaw=qs(('x', 26)),
                   armr=qs(('x', -130), ('z', -14)), arml=qs(('x', -50), ('z', 36)), tail1=qs(('x', 64), ('y', 34)), tail2=qs(('x', 44), ('y', 30)), tail3=qs(('x', 58)), tail4=qs(('x', 40)), mace=qs(('x', 30))),
    # dark magic: reared to his full height, both claws high, green fire in them (the game adds the particles)
    'cast': P(body=qs(('x', -10)), chest=qs(('x', -6)), head=qs(('x', -20)), jaw=qs(('x', 30)), armr=qs(('x', -160), ('z', -26)), arml=qs(('x', -160), ('z', 26)),
              tail1=qs(('x', 26), ('y', 20)), tail2=qs(('x', 34)), tail3=qs(('x', 30)), tail4=qs(('x', 24)), mace=qs(('x', 16))),
    'cast_point': P(body=qs(('x', 6), ('y', -10)), chest=qs(('x', 4), ('y', -10)), head=qs(('x', 2), ('y', 6)), jaw=qs(('x', 18)), armr=qs(('x', -96), ('z', -4)), arml=qs(('x', -26), ('z', 32)), **TAIL_HIGH),
    # the roar: head flung back, maw wide, claws out
    'roar': P(body=qs(('x', -10)), chest=qs(('x', -12)), head=qs(('x', -30)), jaw=qs(('x', 50)), armr=qs(('x', -70), ('z', -70)), arml=qs(('x', -70), ('z', 70)),
              tail1=qs(('x', 30), ('y', 24)), tail2=qs(('x', 30), ('y', 10)), tail3=qs(('x', 26)), tail4=qs(('x', 20)), mace=qs(('x', 14))),
    # tired (his health low): slumped over his coils, head hanging, arms limp, tongue lolling, the tail down
    'tired': P(_face='tired', _off=(0, -0.8, 0), body=qs(('x', 16)), chest=qs(('x', 14), ('z', 4)), head=qs(('x', -12), ('z', 10)), jaw=qs(('x', 22)), armr=qs(('x', 4), ('z', -2)), arml=qs(('x', 8), ('z', 4)),
               tail1=qs(('y', 16)), tail2=qs(('y', 20)), tail3=qs(('y', 24)), mace=qs(('y', 10))),
    # the crouch (the art): down low on his claws, coiled to spring, the mace raised behind
    'crouch': P(_off=(0, -0.6, 0), body=qs(('x', 40)), chest=qs(('x', 26)), head=qs(('x', -50)), jaw=qs(('x', 24)), armr=qs(('x', -18), ('z', -30)), arml=qs(('x', -18), ('z', 30)),
                tail1=qs(('x', 44)), tail2=qs(('x', 40)), tail3=qs(('x', 34)), mace=qs(('x', 20))),
    # sit (a follower at rest): sunk into his coils, arms folded, the tail wrapped round in front
    'sit': P(_face='smug', _off=(0, -1.6, 0), body=qs(('x', -4)), chest=qs(('x', 4)), head=qs(('x', 6), ('y', 14)), jaw=qs(('x', 2)), armr=qs(('x', -56), ('z', 14)), arml=qs(('x', -50), ('z', -14)),
             tail1=qs(('x', 2), ('y', 54)), tail2=qs(('y', 56)), tail3=qs(('y', 50)), mace=qs(('y', 30))),
    # ridden (saddled): low and long like a mount - you sit astride the middle of his back, his head up in front of you
    'ride': P(_saddle=True, body=qs(('x', 56)), chest=qs(('x', -14)), head=qs(('x', -34)), jaw=qs(('x', 10)), armr=qs(('x', -6), ('z', -12)), arml=qs(('x', -6), ('z', 12)),
              tail1=qs(('x', 14)), tail2=qs(('x', 18)), tail3=qs(('x', 22)), mace=qs(('x', 14))),
    # beaten: down on his coils, crown askew, head on the ground - the moment you can offer him a place
    'defeated': P(_face='hurt', _off=(0, -1.8, 0), body=qs(('x', 26), ('z', 6)), chest=qs(('x', 18), ('z', 6)), head=qs(('x', -8), ('z', 12)), jaw=qs(('x', 12)), armr=qs(('x', 20), ('z', -8)), arml=qs(('x', 28), ('z', 10)),
                  tail1=qs(('y', -20)), tail2=qs(('y', -24)), tail3=qs(('y', -18)), mace=qs(('y', -10))),
    # phase 2 - ETHEREAL: risen off the ground on violet wings
    'eth_hover': P(_eth=True, _off=(0, 11, 0), coil=qs(('x', -8)), body=qs(('x', 4)), chest=qs(('x', 8)), head=qs(('x', -6)), jaw=qs(('x', 26)), armr=qs(('x', -50), ('z', -30)), arml=qs(('x', -50), ('z', 30)),
                   tail1=qs(('x', 4)), tail2=qs(('x', 10)), tail3=qs(('x', 18)), mace=qs(('x', 10)), wingr=qs(('y', 14), ('z', 8)), wingl=qs(('y', -14), ('z', -8))),
    'eth_beat': P(_eth=True, _off=(0, 12.5, 0), coil=qs(('x', -8)), body=qs(('x', 6)), chest=qs(('x', 10)), head=qs(('x', -8)), jaw=qs(('x', 28)), armr=qs(('x', -60), ('z', -36)), arml=qs(('x', -60), ('z', 36)),
                  tail1=qs(('x', 2)), tail2=qs(('x', 6)), tail3=qs(('x', 14)), mace=qs(('x', 8)), wingr=qs(('y', 30), ('z', -40)), wingl=qs(('y', -30), ('z', 40))),
    'eth_cast': P(_eth=True, _off=(0, 11, 0), coil=qs(('x', -10)), body=qs(('x', -8)), chest=qs(('x', -6)), head=qs(('x', -22)), jaw=qs(('x', 44)), armr=qs(('x', -150), ('z', -40)), arml=qs(('x', -150), ('z', 40)),
                  tail1=qs(('x', 8)), tail2=qs(('x', 16)), tail3=qs(('x', 22)), mace=qs(('x', 14)), wingr=qs(('y', -6), ('z', 18)), wingl=qs(('y', 6), ('z', -18))),
}
for _p in POSES.values():                       # (a pose that doesn't name tail4 carries tail3's bend on into it)
    if 'tail4' not in _p and 'tail3' in _p: _p['tail4'] = _p['tail3']
# the game's own poses: asleep (before the Serpent's Den wakes him), a glance from his seat, ridden on the move, swimming,
# the ethereal king's dive and landing
POSES['sleep'] = dict(POSES['sit'], head=qs(('x', 16), ('y', 10), ('z', 8)), jaw=qs(('x', 2)), armr=qs(('x', -34), ('z', 12)), arml=qs(('x', -30), ('z', -12)))
POSES['sit_b'] = dict(POSES['sit'], head=qs(('x', 2), ('y', -18)), jaw=qs(('x', 6)))
POSES['ride_b'] = dict(POSES['ride'], tail1=qs(('x', 14), ('y', -14)), tail2=qs(('x', 18), ('y', 12)), tail3=qs(('x', 22), ('y', 10)), tail4=qs(('x', 22), ('y', 6)),
                       head=qs(('x', -30), ('y', 6)))
POSES['ride_c'] = dict(POSES['ride'], tail1=qs(('x', 14), ('y', 14)), tail2=qs(('x', 18), ('y', -12)), tail3=qs(('x', 22), ('y', -10)), tail4=qs(('x', 22), ('y', -6)),
                       head=qs(('x', -30), ('y', -6)))
POSES['swim_a'] = dict(POSES['slither_a'], _off=(0, -2.0, 0), body=qs(('x', 50), ('y', -6)), chest=qs(('x', 20)), head=qs(('x', -50), ('y', -4)))
POSES['swim_b'] = dict(POSES['slither_b'], _off=(0, -2.4, 0), body=qs(('x', 50), ('y', 6)), chest=qs(('x', 20)), head=qs(('x', -50), ('y', 4)))
POSES['eth_dive'] = P(_eth=True, _off=(0, 6, 0), coil=qs(('x', 34)), body=qs(('x', 26)), chest=qs(('x', 8)), head=qs(('x', -34)), jaw=qs(('x', 46)),
                      armr=qs(('x', -96), ('z', -20)), arml=qs(('x', -96), ('z', 20)), tail1=qs(('x', -20)), tail2=qs(('x', -8)), tail3=qs(('x', -6)), tail4=qs(('x', -6)),
                      mace=I, wingr=qs(('y', 54), ('z', -14)), wingl=qs(('y', -54), ('z', 14)))
POSES['eth_land'] = P(_eth=True, _off=(0, 1, 0), body=qs(('x', 14)), chest=qs(('x', 10)), head=qs(('x', -20)), jaw=qs(('x', 40)),
                      armr=qs(('x', -150), ('z', -40)), arml=qs(('x', -150), ('z', 40)), tail1=qs(('x', 30)), tail2=qs(('x', 30)), tail3=qs(('x', 30)), tail4=qs(('x', 30)),
                      mace=qs(('x', 20)), wingr=qs(('y', -10), ('z', 40)), wingl=qs(('y', 10), ('z', -40)))
# tired, a breath later: low on his coils he stays low (he no longer snaps back up to a regal idle between slumps)
POSES['tired_b'] = dict(POSES['tired'], _off=(0, -0.95, 0), chest=qs(('x', 15), ('z', 3)), head=qs(('x', -14), ('z', 12)), jaw=qs(('x', 16)),
                        armr=qs(('x', 6), ('z', -3)), arml=qs(('x', 10), ('z', 5)))
# (2.78) the in-between keyframes: when a long chain - his tail and the mace on it - swings a long way, each display would
# slide straight to its end and cut the corner (the mace through his arm and chest, the tail through itself); a keyframe
# with every joint bent half way keeps it on its arc
POSES['slither_m'] = mid(POSES['slither_a'], POSES['slither_b'])
POSES['swim_m'] = mid(POSES['swim_a'], POSES['swim_b'])
# (the mace: his right claw held high out of its way the whole time - over, out wide at his side, down; then swung back out
#  wide and low behind him before it rises over his head again for the fight)
POSES['mace_swing'] = dict(mid(POSES['mace_up'], POSES['mace_slam']), tail1=qs(('x', 60), ('y', 40)), armr=qs(('x', -150), ('z', -10)))
POSES['mace_back'] = dict(POSES['mace_slam'], armr=qs(('x', -110), ('z', -20)), tail1=qs(('x', 44), ('y', 30)), tail2=qs(('x', 30)), tail3=qs(('x', 10)), tail4=I, mace=I)
POSES['mace_rec'] = mid(POSES['mace_slam'], POSES['mace_back'])
POSES['eth_dland'] = mid(POSES['eth_dive'], POSES['eth_land'])                 # (the ethereal king pulling out of his dive to land,
POSES['eth_lift'] = mid(POSES['eth_land'], POSES['eth_beat'])                  #  and rising off the ground again)
for _p in POSES.values():
    if 'tail4' not in _p and 'tail3' in _p: _p['tail4'] = _p['tail3']
DRAFT = ['idle_a', 'slither_a', 'battle', 'claw_up', 'claw', 'bite', 'mace_up', 'mace_slam', 'cast', 'cast_point', 'roar', 'tired', 'crouch', 'sit', 'ride', 'defeated',
         'eth_hover', 'eth_beat', 'eth_cast']
# animation loops (pose, ticks to it): the moves the game makes (phase131's attacks and idles - previews, and the clipping
# audit checks the frames between them as well as the poses: each display turns and slides on its own between keyframes)
ANIMS = {'idle': [('idle_a', 30), ('idle_b', 30), ('idle_a', 30)],
         'slither': [('slither_a', 5), ('slither_m', 5), ('slither_b', 5), ('slither_m', 5), ('slither_a', 5)],
         'claw': [('battle', 6), ('claw_up', 7), ('claw', 3), ('battle', 6)], 'bite': [('battle', 6), ('crouch', 6), ('bite', 3), ('battle', 6)],
         'mace': [('battle', 6), ('mace_up', 12), ('mace_swing', 2), ('mace_slam', 2), ('mace_rec', 4), ('mace_back', 4), ('battle', 6)],
         'roar': [('idle_a', 8), ('roar', 8), ('roar', 14), ('idle_a', 10)],
         'cast': [('battle', 6), ('cast', 10), ('cast', 10), ('cast_point', 5), ('idle_a', 10)], 'venom': [('battle', 6), ('cast_point', 5), ('battle', 6)],
         'tired': [('idle_a', 20), ('tired', 20), ('tired_b', 30), ('tired', 30)], 'down': [('tired', 20), ('defeated', 14)],
         'moves': [('idle_a', 10), ('slither_a', 10), ('battle', 6), ('slither_b', 10), ('idle_b', 10)],
         'wake': [('sleep', 16), ('idle_a', 16)], 'rest': [('idle_a', 20), ('sit', 20), ('sit_b', 20), ('sit', 20)],
         'ride': [('ride', 8), ('ride_b', 8), ('ride_c', 8), ('ride_b', 8)],
         'swim': [('swim_a', 5), ('swim_m', 5), ('swim_b', 5), ('swim_m', 5), ('swim_a', 5)],
         'wings': [('eth_hover', 8), ('eth_beat', 8), ('eth_hover', 8), ('eth_cast', 8), ('eth_hover', 8)],
         'swoop': [('eth_beat', 8), ('eth_dive', 5), ('eth_beat', 8)],
         'grand': [('eth_hover', 8), ('eth_dive', 5), ('eth_dland', 3), ('eth_land', 3), ('eth_lift', 4), ('eth_beat', 4)]}


def rp(R):
    import sys as _s
    R.TEXTURE_MODS.append(_s.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
