"""The Eraser (draft, for approval - not in the pack yet): the Gem of Creativity's one mistake. It made the Eraser when it tried to
take a Buddy back, and what came out was a thing that can UNMAKE - rub anything out of the world as if it had never been drawn.
Which is exactly why it is so nervous: timid, gentle, guilty and very, very polite - it says sorry to the things it rubs out.
Mr. Capshun (who knows he is in a video game, and is made of pencil) is terrified of it.

The look: it IS a block - a chunky, classic pink rubber eraser standing on end, in the pack's blocky style. Its top end is cut at a
slant like the old wedge-ended pink erasers, and the low corner (the end it rubs with) is worn: greyed with graphite, crumbs still
clinging to it. A worried face on its front - big tall anxious eyes, brows up in the middle, a small wobbly mouth, a little blush -
and a maker's stamp pressed into its back. Small chunky rose-pink arms (a stubby upper arm and a mitten), short legs with big flat
feet. About knee-to-waist height on a player.

It leaves pink crumbs behind when it attacks: rubbing a foe out sheds tiny crumb cubes off its worn corner and its base as it
scrubs (the shed part, shown when a pose says _shed), and leaves a little heap of rolled eraser crumbs on the ground (the crumbs
part, when a pose says _crumbs). er_crumb_bit is a small 16 px sprite of loose pink crumbs (transparent round them) for the
datapack to use later as a particle or a little item model.

A rigkit rig: body (the block - a model per expression, the face painted on its front), arms bent at the elbow (arm, fore), legs
(each its own root, so the block can lean and rock over its planted feet), the shed crumbs (carried by the block) and the crumbs on
the floor in front of it. Every pose is
set on the ground by its lowest point (_ground below) - the feet, or the block itself when it sits or faints - except the airborne
ones (jump, happy, hop) and the swim, which sinks it to the eyes. Design units: feet at y=0, facing -z, its right is +x."""
import math
import random
import sys
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg, point, qrot
from gem_buddies_art import tex, lit, face_tex, E, ln, arc, bez

PREFIX = 'er_'
RIG_SCALE = 1.0
BW, BD = 4.0, 2.2                                  # (the block's half-width and half-depth)
BY0, BY1 = 2.2, 9.8                                # (its bottom, and the top of its straight sides - the slanted end rises above)
SLANT = 11.3                                       # (the wedge end's slope, degrees: down towards its right, the worn corner)
PIVOT = {'body': (0, 2.6, 0), 'armr': (4.72, 7.0, -0.6), 'forer': (4.72, 4.8, -0.6), 'arml': (-4.72, 7.0, -0.6), 'forel': (-4.72, 4.8, -0.6),
         'legr': (2.0, 2.5, 0), 'legl': (-2.0, 2.5, 0), 'shed': (0, 2.6, 0), 'crumbs': (0, 0, -6.4)}
PARENT = {'body': None, 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml', 'legr': None, 'legl': None, 'shed': 'body', 'crumbs': None}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('blink', 'happy', 'scared', 'sad', 'focus', 'wince')
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

PINK, PINK_D, PINK_L = '#ffa0b6', '#e07a92', '#ffc8d4'
ROSE, ROSE_D = '#f27494', '#bc4f6e'                # (its arms and legs: the same rubber, a deeper pink)
GRAPHITE = '#7d7378'
INK, WHITE = '#2a171e', '#fbf7f3'
BLUSH, SWEAT = '#f47a92', '#8fd0f2'


def HIDDEN(p, pose):
    if p == 'crumbs': return not pose.get('_crumbs')
    if p == 'shed': return not pose.get('_shed')
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'body' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
FW, FH = 2 * BW, BY1 - BY0                         # (the front: the face's window, 8 x 7.6 units)


def _face(kind=None):
    """the worried face (drawn smooth over the pixel-celled pink, as the Gem's Buddies are): two big tall eyes - white, a dark rim,
    a big pupil looking up a little and a glint - brows lifted in the middle, a small wobbly mouth, a blush on each cheek.
    Every expression keeps the brows worried; it is never quite at ease."""
    def p(d, W, H):
        lw = W * 0.016
        eyes = ((W * 0.30, H * 0.42, -1), (W * 0.70, H * 0.42, 1))         # (viewer's left, viewer's right; s = which side)
        rx, ry = W * 0.12, H * 0.165
        for cx, cy, s in eyes:                                               # (the blush first - the rest is drawn over it)
            E(d, cx + s * W * 0.06, H * 0.655, W * 0.075, H * 0.035, BLUSH)
        for cx, cy, s in eyes:
            if kind == 'blink':                                              # (shut, the lids sagging - still worried)
                ln(d, arc(cx, cy - ry * 0.1, rx * 0.9, ry * 0.45, 20, 160), INK, lw * 1.8); continue
            if kind == 'happy':                                              # (relieved: two soft upturned arcs)
                ln(d, arc(cx, cy + ry * 0.35, rx * 0.95, ry * 0.6, 200, 340), INK, lw * 2.0); continue
            if kind == 'wince':                                              # (squeezed shut: > <)
                k = -s
                ln(d, [(cx - k * rx * 0.8, cy - ry * 0.5), (cx + k * rx * 0.7, cy), (cx - k * rx * 0.8, cy + ry * 0.5)], INK, lw * 2.0); continue
            ex, ey = (rx * 1.15, ry * 1.12) if kind == 'scared' else (rx, ry)
            E(d, cx, cy, ex, ey, WHITE, INK, lw)
            if kind == 'scared':                                             # (tiny pupils in huge eyes)
                pr, px_, py_ = rx * 0.32, cx - s * rx * 0.05, cy + ry * 0.05
            elif kind == 'sad':                                              # (looking down and away)
                pr, px_, py_ = rx * 0.52, cx + s * rx * 0.12, cy + ry * 0.35
            else:                                                            # (big pupils, glancing up)
                pr, px_, py_ = rx * 0.56, cx - s * rx * 0.08, cy - ry * 0.12
            E(d, px_, py_, pr, pr * 1.25, INK)
            E(d, px_ - pr * 0.35, py_ - pr * 0.5, pr * 0.32, pr * 0.32, WHITE)
            E(d, px_ + pr * 0.35, py_ + pr * 0.45, pr * 0.13, pr * 0.13, WHITE)
            if kind in ('sad', 'focus'):                                     # (a heavy lid over the top of the eye)
                cut = cy - ry * (0.2 if kind == 'sad' else 0.05)
                d.polygon([(x, y) for x, y in arc(cx, cy, ex + lw, ey + lw, 180, 360, n=40) if y <= cut] +
                          [(cx + ex + lw, cut), (cx - ex - lw, cut)], fill=hexc(PINK))
                ln(d, [(cx - ex * 0.98, cut), (cx + ex * 0.98, cut + s * H * 0.01)], INK, lw * 1.4)
        # the brows: lifted in the middle - worried (higher when scared, pinched when wincing or trying hard)
        lift = {'scared': 0.05, 'wince': -0.01, 'focus': -0.005, 'sad': 0.02}.get(kind, 0.0)
        for cx, cy, s in eyes:
            o, i = (cx + s * W * 0.10, H * (0.19 - lift * 0.4)), (cx - s * W * 0.07, H * (0.09 - lift))
            ln(d, bez(o, (cx + s * W * 0.02, H * (0.115 - lift * 0.7)), i), INK, lw * 2.4)
        # the mouth: small and wobbly, under the eyes and between them
        mx, my = W * 0.5, H * 0.69
        if kind == 'scared':                                                 # (open: a wobbly little "o")
            pts = [(mx + W * 0.055 * math.cos(t) * (1 + 0.08 * math.sin(5 * t)), my + H * 0.05 * math.sin(t) * (1 + 0.08 * math.cos(4 * t)))
                   for t in [2 * math.pi * k / 48 for k in range(48)]]
            d.polygon(pts, fill=hexc('#6a2a38'), outline=hexc(INK)); ln(d, pts + pts[:1], INK, lw * 1.3)
        elif kind == 'happy':                                                # (a small shy smile, wobbling at the ends)
            ln(d, [(mx + W * 0.09 * t, my - H * 0.01 + H * 0.035 * (1 - t * t) + H * 0.006 * math.sin(9 * t)) for t in [k / 20 - 1 for k in range(41)]], INK, lw * 1.6)
        elif kind == 'wince':                                                # (gritted: a tight zigzag)
            ln(d, [(mx - W * 0.09 + W * 0.03 * k, my + (H * 0.018 if k % 2 else -H * 0.012)) for k in range(7)], INK, lw * 1.5)
        else:                                                                # (a wobbly line, turned down at the ends; more so when sad)
            down = 0.035 if kind == 'sad' else 0.018
            ln(d, [(mx + W * 0.1 * t, my + H * 0.013 * math.sin(3 * math.pi * t) + H * down * t * t) for t in [k / 20 - 1 for k in range(41)]], INK, lw * 1.5)
        if kind in ('scared', 'focus', 'sad'):                               # (a bead of sweat - or, sad, a tear)
            if kind == 'sad':
                sx, sy, r = W * 0.27, H * 0.6, W * 0.022
            else:
                sx, sy, r = W * 0.88, H * 0.24, W * 0.03
            d.polygon([(sx, sy - r * 2.4), (sx - r * 0.95, sy - r * 0.3), (sx + r * 0.95, sy - r * 0.3)], fill=hexc(SWEAT))
            E(d, sx, sy, r, r, SWEAT); E(d, sx - r * 0.35, sy - r * 0.3, r * 0.28, r * 0.28, WHITE)
    return face_tex(PINK, FW, FH, p, seed=4101, var=0.03, hi=45, rim=PINK_D, rim_a=80)


GLYPH = {'E': ('111', '100', '110', '100', '111'), 'R': ('110', '101', '110', '101', '101'), 'A': ('010', '101', '111', '101', '101'),
         'S': ('111', '100', '111', '001', '111')}


def _back():
    """its back: the maker's stamp pressed into the rubber - a frame and ERASER in blocky letters"""
    im = lit(tex(PINK, 4111, 0.035), 2 * BW, FH, 4, a=50, rim=PINK_D, rim_a=80); d = ImageDraw.Draw(im)
    deep, edge = hexc('#d88796'), hexc('#fbd0d7')
    x0, y0, x1, y1 = 3, 9, 28, 20
    for (a, b, c, e_) in ((x0, y0, x1, y0), (x0, y1, x1, y1), (x0, y0, x0, y1), (x1, y0, x1, y1)):
        d.line((a, b, c, e_), fill=deep)
    d.line((x0 + 1, y1 + 1, x1 + 1, y1 + 1), fill=edge); d.line((x1 + 1, y0 + 1, x1 + 1, y1 + 1), fill=edge)    # (the lip of the press)
    for i, ch in enumerate('ERASER'):
        for r, row in enumerate(GLYPH[ch]):
            for c, on in enumerate(row):
                if on == '1': d.point((5 + i * 4 + c, 12 + r), fill=deep)
    return im


def _worn(seed, end_u):
    """the slanted top end: pink, rubbed grey with graphite towards the worn corner (end_u: that end, in pixels across)"""
    im = tex(PINK, seed, 0.04); px = im.load(); rnd = random.Random(seed + 1); g = hexc(GRAPHITE)
    for y in range(0, 64, 2):
        for x in range(0, 64, 2):
            k = max(0.0, 1 - abs(x - end_u) / 18.0) ** 1.5 * 0.85 * rnd.uniform(0.55, 1.1)
            if k <= 0.04: continue
            c = px[x, y]; c = tuple(int(c[i] * (1 - k) + g[i] * k) for i in range(3)) + (255,)
            for dy in (0, 1):
                for dx in (0, 1): px[x + dx, y + dy] = c
    return im


def _crumb_bit():
    """loose pink rubber crumbs, a few pixels each, on transparent (16 px): a particle sprite or a tiny item model for the pack"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for (x0, y0, x1, y1), c, sh in (((2, 3, 6, 5), '#f2a3b1', '#c9707f'), ((9, 2, 11, 5), '#e99aa8', '#b8606f'), ((6, 8, 10, 10), '#f6b4c0', '#c9707f'),
                                    ((11, 9, 13, 13), '#d98c9a', '#a9526a'), ((2, 11, 5, 13), '#c4a2a8', '#8a7a80'), ((8, 13, 9, 14), '#f2a3b1', '#c9707f')):
        d.rectangle((x0, y0, x1, y1), fill=hexc(c))
        d.line((x0, y1, x1, y1), fill=hexc(sh)); d.line((x1, y0, x1, y1), fill=hexc(sh))           # (shaded below and to the right)
        d.point((x0, y0), fill=hexc('#fde0e5'))                                                        # (a glint)
    return im


def textures():
    T = {'er_crumb_bit': _crumb_bit(), 'er_face': _face(), 'er_back': _back(),
         'er_rub': lit(tex(PINK, 4121, 0.035), 4.4, 7.6, 4, a=40, rim=PINK_D, rim_a=70),
         'er_slab': lit(tex(PINK, 4122, 0.035), 8.2, 3.0, 4, a=50, rim=PINK_D, rim_a=40),
         'er_under': tex('#d98c9a', 4123, 0.04),
         'er_worn': _worn(4124, 30), 'er_worn_end': _worn(4125, 8),
         'er_limb': lit(tex(ROSE, 4126, 0.04), 1.5, 2.6, 4, a=50, rim=ROSE_D, rim_a=80),
         'er_sole': tex(ROSE_D, 4127, 0.04),
         'er_crumb': tex('#e9a2ae', 4128, 0.06, spots=[('#b48a92', 0.4)]),
         'er_crumb_g': tex('#c4a2a8', 4129, 0.06, spots=[('#8a7a80', 0.4)])}
    for k in FACES:
        T[f'er_face_{k}'] = _face(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _body(face=None):
    pv = PIVOT['body']; ft = 'er_face' if face is None else f'er_face_{face}'
    main = el((-BW, BY0, -BD), (BW, BY1, BD), 'er_rub', pv, uv={'north': [0, 0, FW, FH], 'south': [0, 0, FW, FH]})
    main['faces']['north']['texture'] = '#' + ft
    main['faces']['south']['texture'] = '#er_back'
    main['faces']['down']['texture'] = '#er_under'
    # the slanted end: a slab laid along the slope, its bottom buried in the block (its ends cut so nothing pokes out of the sides:
    # the high end is bevelled a little, as a wedge eraser's is). Its top is the worn face, graphite-grey towards the low corner.
    org = (0.0, BY1, 0.0)
    slab = el((-3.76, BY1 - 1.6, -BD + 0.02), (3.8, BY1 + 1.4, BD - 0.02), 'er_slab', pv, rot=((0.0, 0.0, -SLANT), org), shift=(0.3, 0.2))
    slab['faces']['up']['texture'] = '#er_worn'
    slab['faces']['east']['texture'] = '#er_worn_end'
    # crumbs still clinging to the worn corner
    nubs = [el((2.9, 10.15, -1.5), (3.5, 10.65, -0.9), 'er_crumb', pv), el((3.85, 9.75, 0.5), (4.35, 10.2, 1.05), 'er_crumb_g', pv),
            el((1.9, 10.45, 0.9), (2.35, 10.85, 1.35), 'er_crumb', pv)]
    return [main, slab] + nubs


def _arm(sx):
    s = 'r' if sx > 0 else 'l'; ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']
    x0, x1 = sorted((sx * 4.02, sx * 5.42)); h0, h1 = sorted((sx * 4.0, sx * 5.46))
    z = ap[2]
    arm = [el((x0, 4.6, z - 0.7), (x1, 7.6, z + 0.7), 'er_limb', ap, shift=(0.2, 0.1))]
    fore = [el((h0, 2.9, z - 0.76), (h1, 5.0, z + 0.76), 'er_limb', fp, shift=(0.6, 0.5))]                      # (a chunky mitten)
    return arm, fore


def _leg(sx):
    lp = PIVOT['legr' if sx > 0 else 'legl']
    x0, x1 = sorted((sx * 1.2, sx * 2.8)); f0, f1 = sorted((sx * 1.0, sx * 3.0))
    foot = el((f0, 0.0, -2.1), (f1, 1.1, 1.0), 'er_limb', lp, shift=(0.5, 0.7))
    foot['faces']['down']['texture'] = '#er_sole'
    return [el((x0, 0.9, -0.8), (x1, 2.8, 0.8), 'er_limb', lp, shift=(0.1, 0.3)), foot]


def _crumbs():
    """the heap it leaves: little rolled worms of rubber, pink and grey, scattered on the floor"""
    pv = PIVOT['crumbs']; cx, _, cz = pv; rnd = random.Random(4131); out = []
    for i in range(11):
        a = rnd.uniform(0, math.pi); L = rnd.uniform(0.5, 0.85); r = rnd.uniform(0.0, 2.6) ** 0.9; b = rnd.uniform(0, 2 * math.pi)
        x, z = cx + r * math.cos(b) * 1.2, cz + r * math.sin(b) * 0.8
        h = rnd.choice((0.38, 0.42, 0.46))
        y = h / 2 + (0.36 if i in (3, 7) else 0.0)                                           # (two lying on top of the others)
        out.append(seg((x - L * math.cos(a), y, z - L * math.sin(a)), (x + L * math.cos(a), y, z + L * math.sin(a)), h, h,
                       'er_crumb_g' if i % 3 == 0 else 'er_crumb', pv))
    return out


def _shed():
    """crumbs coming off it as it scrubs: bits breaking from the worn corner and the front edge, more dropping by its base"""
    pv = PIVOT['shed']
    bits = [((4.35, 9.3, -1.2), 0.7), ((4.75, 8.1, 0.4), 0.55), ((4.5, 6.6, -1.4), 0.6), ((3.4, 11.0, -2.3), 0.55), ((5.0, 5.2, -0.4), 0.5),   # (off the worn corner)
            ((-1.6, 2.5, -2.75), 0.6), ((0.6, 2.1, -3.1), 0.55), ((2.7, 2.4, -2.8), 0.65), ((-3.3, 2.0, -2.9), 0.55), ((1.6, 1.7, -3.5), 0.5),  # (dropping off its front edge)
            ((1.6, 9.6, -2.75), 0.5), ((-2.5, 3.3, -2.7), 0.45)]
    return [el((x - r / 2, y - r / 2, z - r / 2), (x + r / 2, y + r / 2, z + r / 2), 'er_crumb_g' if i % 4 == 3 else 'er_crumb', pv, shift=(0.17 * i, 0.31 * i))
            for i, ((x, y, z), r) in enumerate(bits)]


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    part('er_body', _body())
    for fc in FACES:
        part(f'er_body_x{fc}', _body(fc))
    for sx, s in ((1, 'r'), (-1, 'l')):
        a, f = _arm(sx)
        part(f'er_arm{s}', a); part(f'er_fore{s}', f); part(f'er_leg{s}', _leg(sx))
    part('er_shed', _shed())
    part('er_crumbs', _crumbs())
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    """a limb's turn: fwd swings it forward, out lifts it out to its own side, turn twists it (+ inwards)"""
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def B(lean=0.0, yaw=0.0, roll=0.0):
    """the block's turn: lean tips it forward (-: back), yaw turns it to its left (-: its right), roll tips it to its right"""
    return qs(('y', yaw), ('x', lean), ('z', -roll))


def P(**kw):
    return kw


SITLEGS = {'_o_legr': (0.0, 0.5, -2.4), '_o_legl': (0.0, 0.5, -2.4)}
REST = dict(armr=limb(1, 6, 6), forer=limb(1, 14), arml=limb(-1, 6, 6), forel=limb(-1, 14))
POSES = {
    # standing, fidgeting: its little hands drawn up in front of it
    'idle_a': P(armr=limb(1, 26, -4), forer=limb(1, 44, 0, 20), arml=limb(-1, 22, -4), forel=limb(-1, 48, 0, 20)),
    # a nervous glance over its shoulder, one mitten raised to its mouth
    'idle_b': P(_face='scared', body=B(yaw=-16, roll=-3), armr=limb(1, 48, -6), forer=limb(1, 84, 0, 30), arml=limb(-1, 8, 10), forel=limb(-1, 16)),
    # "sorry!": a little apologetic bow
    'idle_c': P(_face='sad', body=B(lean=20), armr=limb(1, 14, -2), forer=limb(1, 20), arml=limb(-1, 14, -2), forel=limb(-1, 20)),
    'happy': P(_face='happy', _off=(0, 1.4, 0), body=B(roll=5), armr=limb(1, 10, 74), forer=limb(1, 0, 30), arml=limb(-1, 10, 74), forel=limb(-1, 0, 30),
               legr=limb(1, 10, 6), legl=limb(-1, -6, 6)),
    'hurt': P(_face='wince', body=B(lean=-14, roll=4), armr=limb(1, 40, 36), forer=limb(1, 50), arml=limb(-1, 40, 36), forel=limb(-1, 50),
              legr=limb(1, 10), legl=limb(-1, -8)),
    # fainted: flat on its back, its stubby legs sticking out, arms flopped
    'tired': P(_face='blink', body=B(lean=-90), legr=limb(1, 72, 4), legl=limb(-1, 66, 4), armr=limb(1, 0, 40), forer=limb(1, 10), arml=limb(-1, 0, 40), forel=limb(-1, 10)),
    # sitting: on its bottom, short legs out in front, mittens in its lap
    # (its legs are too short to clear the block, so they slide out from under its front edge: _o_ shifts)
    'sit_a': P(body=B(lean=-6), legr=limb(1, 86, 6), legl=limb(-1, 86, 6), **SITLEGS, armr=limb(1, 34, -4), forer=limb(1, 40, 0, 16), arml=limb(-1, 34, -4), forel=limb(-1, 40, 0, 16)),
    # ...and the seated idle: swinging its feet, rocking a little, a shy smile
    'sit_b': P(_face='happy', body=B(lean=-8, roll=-4), legr=limb(1, 104, 4), legl=limb(-1, 74, 10), **SITLEGS, armr=limb(1, 10, 22), forer=limb(1, 10), arml=limb(-1, 10, 22),
               forel=limb(-1, 10)),
    'jump': P(_face='scared', body=B(lean=-4), legr=limb(1, 30, 8), legl=limb(-1, 18, 8), armr=limb(1, 10, 120), forer=limb(1, 0, 20), arml=limb(-1, 10, 120), forel=limb(-1, 0, 20)),
    # RUB OUT: it leans right in, mittens braced on the foe, and scrubs side to side - crumbs flying - trying very hard not to look
    'rub_0': P(_face='focus', _crumbs=1, _shed=1, _off=(0.7, 0, -0.8), body=B(lean=30, yaw=10, roll=8), armr=limb(1, 78, 6), forer=limb(1, 20), arml=limb(-1, 88, 6),
               forel=limb(-1, 20), legr=limb(1, -26), legl=limb(-1, 0)),
    'rub_1': P(_face='focus', _crumbs=1, _shed=1, _off=(-0.7, 0, -0.8), body=B(lean=30, yaw=-10, roll=-8), armr=limb(1, 88, 6), forer=limb(1, 20), arml=limb(-1, 78, 6),
               forel=limb(-1, 20), legr=limb(1, 0), legl=limb(-1, -26)),
    # ...and afterwards it winces at what it's done, backing off from the crumbs
    'wince': P(_face='wince', _crumbs=1, _off=(0, 0, 0.8), body=B(lean=-10, roll=-6), armr=limb(1, 62, -8), forer=limb(1, 70, 0, 26), arml=limb(-1, 62, -8),
               forel=limb(-1, 70, 0, 26), legr=limb(1, -10), legl=limb(-1, 12)),
    # BOUNCE: a crouch on splayed feet, arms back - up - and down flat on the foe (it's rubber: it bounces)
    'hop_up': P(_face='focus', body=B(lean=10), legr=limb(1, 0, 26), legl=limb(-1, 0, 26), armr=limb(1, -36, 24), forer=limb(1, 10), arml=limb(-1, -36, 24), forel=limb(-1, 10)),
    'hop': P(_face='scared', body=B(lean=-8), legr=limb(1, 36, 8), legl=limb(-1, 36, 8), armr=limb(1, 10, 136), forer=limb(1, 0, 20), arml=limb(-1, 10, 136), forel=limb(-1, 0, 20)),
    'slam': P(_face='wince', _crumbs=1, _shed=1, body=B(lean=6), legr=limb(1, 0, 30), legl=limb(-1, 0, 30), armr=limb(1, 10, 76), forer=limb(1, 0, -10), arml=limb(-1, 10, 76), forel=limb(-1, 0, -10)),
    # HIDE: scared - it cowers on splayed feet, ducks its face and turns half away, mittens pressed over its eyes (as far as its
    # little arms reach)
    'hide': P(_face='wince', body=B(lean=16, yaw=28), legr=limb(1, 0, 20), legl=limb(-1, 0, 20), armr=limb(1, 90, 0, 10), forer=limb(1, 15, -60),
              arml=limb(-1, 90, 0, 10), forel=limb(-1, 15, -60)),
}


def _walk(k, a=24.0, arm=20.0, waddle=5.0):
    s = math.sin(math.pi * k / 2)
    return dict(legr=limb(1, a * s), legl=limb(-1, -a * s), armr=limb(1, -arm * s + 6, 6), forer=limb(1, 16), arml=limb(-1, arm * s + 6, 6), forel=limb(-1, 16),
                body=B(roll=waddle * s, yaw=-4 * s))


for _k in range(4):
    POSES[f'walk_{_k}'] = P(**_walk(_k))                                                # (a waddle - the block rocks over each foot)
    _r = _walk(_k, 40, 34, 4)
    _s = math.sin(math.pi * _k / 2)
    _r.update(body=B(lean=12, roll=4 * _s), armr=limb(1, -30 * _s + 20, 46), arml=limb(-1, 30 * _s + 20, 46), forer=limb(1, 30), forel=limb(-1, 30))
    POSES[f'run_{_k}'] = P(_face='scared', **_r)                                        # (running for it, arms flapping)
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                              # (a frantic little paddle, sunk to the eyes - rubber doesn't float)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_face='scared', _off=(0, -6.2 + 0.4 * math.sin(2 * _p), 0), body=B(lean=14),
                            armr=limb(1, 96 + 36 * math.sin(_p), 14), forer=limb(1, 20), arml=limb(-1, 96 - 36 * math.sin(_p), 14), forel=limb(-1, 20),
                            legr=limb(1, -10 + 26 * math.sin(_p)), legl=limb(-1, -10 - 26 * math.sin(_p)))


# ---- every pose set on the ground by its lowest corner
_ME = sys.modules[__name__]
_CORNERS = {}


def _corners():
    if _CORNERS: return _CORNERS
    M = models()
    for p in PARTS:
        if p in ('crumbs', 'shed'): continue
        pts = []
        for e in M[f'{PREFIX}{p}'][1]:
            off = [PIVOT[p][i] - 8 for i in range(3)]
            fr, to = e['from'], e['to']
            q = None
            if 'rotation' in e:
                r = e['rotation']
                q = qs(('z', r.get('z', 0.0)), ('y', r.get('y', 0.0)), ('x', r.get('x', 0.0))) if 'axis' not in r else qs((r['axis'], r['angle']))
                o = r['origin']
            for c in [(a, b, cc) for a in (fr[0], to[0]) for b in (fr[1], to[1]) for cc in (fr[2], to[2])]:
                if q:
                    v = qrot(q, tuple(c[i] - o[i] for i in range(3))); c = tuple(v[i] + o[i] for i in range(3))
                pts.append(tuple(c[i] + off[i] for i in range(3)))
        _CORNERS[p] = pts
    return _CORNERS


def low(pose):
    """the lowest point of the posed figure (design units above the floor)"""
    return min(point(_ME, pose, p, c)[1] * 16 for p, cs in _corners().items() for c in cs)


def _ground(pose, lift=0.0):
    pose = dict(pose); o = pose.pop('_off', (0.0, 0.0, 0.0))
    pose['_off'] = (o[0], 0.0, o[2])
    pose['_off'] = (o[0], round(lift - low(pose), 3), o[2])
    return pose


_LIFT = {'jump': 3.2, 'happy': 1.2, 'hop': 6.0, 'walk_1': 0.3, 'walk_3': 0.3, 'run_1': 1.0, 'run_3': 1.0}
for _k in list(POSES):
    if not _k.startswith('swim_'):
        POSES[_k] = _ground(POSES[_k], _LIFT.get(_k, 0.0))

DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'run_1', 'jump', 'happy', 'hurt', 'sit_a', 'sit_b', 'tired', 'swim_2',
         'rub_0', 'rub_1', 'wince', 'hop_up', 'hop', 'slam', 'hide']
