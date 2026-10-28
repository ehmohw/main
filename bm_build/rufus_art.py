"""2.95e: RUFUS GNAW, rat for hire - his rig, so he can be a follower like the others. Until now he was one block-model figure
(rat3d_merc: the traders' wool rat in the 'merc' kit, phase29) bobbing on an invisible wolf. This keeps that look exactly - the
dark grey rat (gray wool), a paler snout, chest and belly (light grey), pink ears, paws, feet and tail, a red bandana knotted at
the back, a dark mask across his eyes, a brown leather vest with a strap across the top - and gives him joints and his kit:
a short blade (sheathed at his left hip when he isn't swinging it) and a crossbow (slung on his back when he isn't aiming it).

A rigkit rig: body (hips, haunches and vest), head (a face per expression; the bandana, ears, snout and whiskers on it), arms
bent at the elbow, two short legs, the tail, the tool in his right paw, the slung crossbow and the sheath. Design units are the
old figure's own (feet at y=0, the ears' tips at 18), centred on x and z, facing -z, his right +x. At RIG_SCALE 0.55 he stands
as tall as the old figure did (0.62 blocks to the ear-tips)."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, chain

PREFIX = 'rf_'
RIG_SCALE = 0.55
PIVOT = {'body': (0, 3.6, 0.6), 'head': (0, 11.0, 0.6),
         'armr': (3.75, 10.2, 0.75), 'forer': (3.75, 8.0, 0.75), 'arml': (-3.75, 10.2, 0.75), 'forel': (-3.75, 8.0, 0.75),
         'legr': (2.0, 3.2, 0.6), 'legl': (-2.0, 3.2, 0.6), 'footr': (2.0, 1.0, 0.6), 'footl': (-2.0, 1.0, 0.6), 'tail': (0, 2.4, 3.0),
         'tool': (3.75, 5.9, 0.75), 'slung': (0, 8.0, 3.0), 'sheath': (-3.7, 6.2, -0.2)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': 'body', 'legl': 'body', 'footr': 'legr', 'footl': 'legl', 'tail': 'body', 'tool': 'forer', 'slung': 'body', 'sheath': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
TOOLS = ('blade', 'crossbow', 'coins', 'none')
FACES = ('blink', 'grin', 'angry', 'squint', 'hurt', 'shade')
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

# the old figure's wool, sampled (gray / light gray / pink / black / white / red / brown wool, iron block, stripped oak)
GREY, GREY_D, GREY_L = '#3e4447', '#33383b', '#4b5356'
PALE, PALE_D = '#8e8e86', '#7d7d73'
PINK, PINK_D = '#ed8dac', '#d76690'
INK, MASK = '#141519', '#1f2226'
WHITE = '#e9ecec'
RED, RED_D, RED_L = '#a02722', '#7e1b18', '#b8342c'
LEATHER, LEATHER_D, LEATHER_L = '#724728', '#5a361c', '#835432'
IRON, IRON_D = '#dcdcdc', '#9a9a9a'
OAK, OAK_D = '#b19056', '#8a6d3c'
GOLD, GOLD_D = '#f2c230', '#b88a14'


def HIDDEN(p, pose):
    t = pose.get('_tool', 'blade')
    if p == 'tool': return t == 'none'
    if p == 'slung': return t == 'crossbow' or 'slung' in pose.get('_hide', ())
    if p == 'sheath': return t == 'blade'
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    if p == 'tool':
        return f'{PREFIX}tool_{pose.get("_tool", "blade")}{suffix}'
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _cells(fn, seed, cell=2):
    """a 64 px texture painted cell by cell (wool-chunky): fn(cx, cy, rnd) -> colour"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im); rnd = random.Random(seed); n = 64 // cell
    for cy in range(n):
        for cx in range(n):
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(fn(cx, cy, rnd)))
    return im


def _wool(base, var, seed, p=0.22):
    return _cells(lambda x, y, r: r.choice(var) if r.random() < p else base, seed)


def _vest(front=False):
    """brown leather: darker seams every few cells, stitching; the front open down the middle over his pale chest fur"""
    def c(x, y, r):
        if front and 10 <= x <= 13: return PALE if r.random() > 0.2 else PALE_D           # (the open front: cols 20-27 px = 1 unit each side of centre)
        if front and x in (9, 14): return LEATHER_D
        if y % 7 == 6: return LEATHER_D
        return r.choice((LEATHER, LEATHER, LEATHER, LEATHER_L, LEATHER_D))
    return _cells(c, 2901 + front)


def _bandana():
    """red cloth with darker folds and a few pale specks (the old figure's red wool, with a fold or two)"""
    def c(x, y, r):
        if y % 5 == 4: return RED_D
        if r.random() < 0.025: return '#c86a5a'
        return r.choice((RED, RED, RED, RED_L, RED_D))
    return _cells(c, 2902)


def _face(kind=None):
    """the face: 6 x 5 units (24 x 20 px from the top-left). Rows 0-3 sit under the bandana; the mask, a dark band, across rows
    4-9 with the eyes in it (cols 3-7 his right, 16-20 his left - his right is our left as we face him); a nick of a scar
    through his left brow; the snout covers cols 6-17 from row 9 down."""
    im = _wool(GREY, (GREY_D, GREY_L), 2903); d = ImageDraw.Draw(im)
    R = lambda x0, y0, x1, y1, c: d.rectangle((x0, y0, x1, y1), fill=hexc(c))
    if kind != 'shade':
        R(0, 4, 23, 9, MASK)
        for x0 in (3, 16):
            if kind in ('blink', 'shade'):
                R(x0, 6, x0 + 4, 7, INK)
            elif kind == 'grin':                                      # (pleased with himself: the eyes narrowed, curved)
                R(x0, 6, x0 + 4, 6, INK); R(x0 + 1, 5, x0 + 3, 5, INK)
            elif kind == 'squint':                                    # (down the sights: one eye shut)
                if x0 == 3: R(x0, 6, x0 + 4, 7, INK)
                else: R(x0 - 1, 4, x0 + 5, 8, '#5d6468'); R(x0, 5, x0 + 4, 7, INK); R(x0 + 1, 5, x0 + 2, 6, WHITE)
            elif kind == 'hurt':
                R(x0 - 1, 4, x0 + 5, 9, '#5d6468'); R(x0, 5, x0 + 4, 8, INK); R(x0 + 1, 6, x0 + 3, 7, '#c8c8c8')
            else:                                                     # (a pale rim round each eye, so it reads in the mask; the glint)
                R(x0 - 1, 4, x0 + 5, 9, '#5d6468'); R(x0, 5, x0 + 4, 8, INK); R(x0 + 1, 5, x0 + 2, 6, WHITE)
            if kind == 'angry':                                       # (the brows down hard)
                R(x0 - 1, 4, x0 + 5, 4, '#5d6468')
                d.line((x0, 3, x0 + 4, 5) if x0 == 3 else (x0, 5, x0 + 4, 3), fill=hexc(INK), width=2)
        if kind not in ('blink', 'grin', 'squint'):
            R(18, 2, 18, 9, '#5a5f62'); R(19, 3, 19, 4, '#5a5f62')      # (the scar through his left brow)
    else:                                                             # (the bandana pulled down over his eyes: only the snout shows)
        R(0, 0, 23, 9, RED)
        for x in range(0, 24, 3): R(x, 8, x + 1, 9, RED_D)
    return im


def _snout(kind=None):
    """the snout's front (3 x 2.4 units): pale, the mouth a dark line - a smirk to one side; a grin shows a tooth"""
    im = _wool(PALE, (PALE_D,), 2904, 0.15); d = ImageDraw.Draw(im)
    if kind == 'grin':
        d.rectangle((2, 6, 9, 6), fill=hexc(INK)); d.rectangle((4, 7, 5, 8), fill=hexc(WHITE))
    elif kind in ('angry', 'hurt'):
        d.rectangle((3, 7, 8, 7), fill=hexc(INK)); d.rectangle((3, 6, 3, 6), fill=hexc(INK)); d.rectangle((8, 6, 8, 6), fill=hexc(INK))
    else:
        d.rectangle((4, 7, 9, 7), fill=hexc(INK)); d.rectangle((9, 6, 9, 6), fill=hexc(INK))   # (the smirk)
    return im


def textures():
    T = {'rf_fur': _wool(GREY, (GREY_D, GREY_L), 2910), 'rf_pale': _wool(PALE, (PALE_D,), 2911, 0.15),
         'rf_pink': _wool(PINK, (PINK_D,), 2912, 0.15), 'rf_vest': _vest(), 'rf_vestf': _vest(True), 'rf_red': _bandana(),
         'rf_strap': _wool('#2a1c12', ('#3a2618',), 2913), 'rf_iron': _wool(IRON, ('#c4c4c4', '#f0f0f0'), 2914),
         'rf_steel': _wool('#c8ccd0', ('#e8ecee', IRON_D), 2918, 0.3),
         'rf_oak': _wool(OAK, (OAK_D, '#c2a166'), 2915), 'rf_ink': _wool(INK, ('#07090e',), 2916, 0.1),
         'rf_white': _wool(WHITE, ('#d0d6d7',), 2917, 0.1), 'rf_gold': _wool(GOLD, (GOLD_D, '#ffe070'), 2919, 0.3),
         'rf_face': _face(), 'rf_snout': _snout()}
    for k in FACES:
        T[f'rf_face_{k}'] = _face(k)
        if k in ('grin', 'angry', 'hurt'): T[f'rf_snout_{k}'] = _snout(k)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: haunches, the torso in its vest (open at the front over his chest fur), the strap, the belt and buckle
    pv = PIVOT['body']
    part('rf_body', [
        el((-3.5, 1.2, -1.5), (3.5, 6.2, 3.0), 'rf_fur', pv, shift=(0.1, 0.3)),                                  # haunches
        el((-2.0, 2.2, -1.52), (2.0, 5.9, -1.5), 'rf_pale', pv, faces=('north',)),                               # belly
        el((-3.0, 6.0, -1.0), (3.0, 11.0, 2.5), 'rf_fur', pv, shift=(0.5, 0.2)),                                 # torso
        el((-3.15, 6.4, -1.15), (3.15, 10.8, 2.65), 'rf_vest', pv, faces=('south', 'east', 'west', 'up', 'down'), shift=(0.2, 0.1)),
        el((-3.15, 6.4, -1.17), (3.15, 10.8, -1.15), 'rf_vestf', pv, faces=('north',), uv={'north': [2, 0, 8.3, 4.4]}),
        el((-3.4, 9.6, -1.35), (3.4, 10.2, 2.85), 'rf_strap', pv),                                               # (the old figure's strap)
        el((-3.6, 5.9, -1.75), (3.6, 6.7, 3.15), 'rf_strap', pv),                                                # belt
        el((-0.7, 5.75, -1.9), (0.7, 6.85, -1.75), 'rf_iron', pv),                                               # buckle
        el((-1.6, 3.8, 3.0), (1.6, 5.8, 3.4), 'rf_vest', pv, shift=(0.7, 0.7)),                                  # (a pouch at the back of his belt)
        # (the crossbow's sling, across his chest from his left shoulder to his right hip - and down his back)
        el((-0.3, 5.8, -1.45), (0.3, 11.6, -1.25), 'rf_strap', pv, rot=((0.0, 0.0, 38.0), (0.0, 8.6, -1.35))),
        el((-0.3, 5.8, 2.75), (0.3, 11.6, 2.95), 'rf_strap', pv, rot=((0.0, 0.0, -38.0), (0.0, 8.6, 2.85)))])

    # ---- the head: the skull, the face (mask and eyes painted), the snout and nose, whiskers, ears through the bandana and its knot
    pv = PIVOT['head']

    def head(face=None):
        ft = 'rf_face' if face is None else f'rf_face_{face}'
        st = f'rf_snout_{face}' if face in ('grin', 'angry', 'hurt') else 'rf_snout'
        cap_lo = 13.3 if face == 'shade' else 15.1
        h = [el((-3.0, 11.0, -2.0), (3.0, 16.0, 2.5), 'rf_fur', pv, shift=(0.3, 0.6), faces=('south', 'east', 'west', 'up', 'down')),
             el((-3.0, 11.0, -2.02), (3.0, 16.0, -2.0), ft, pv, faces=('north',), uv={'north': [0, 0, 6, 5]}),
             el((-1.5, 11.4, -4.0), (1.5, 13.8, -2.0), 'rf_pale', pv, faces=('east', 'west', 'up', 'down')),
             el((-1.5, 11.4, -4.02), (1.5, 13.8, -4.0), st, pv, faces=('north',), uv={'north': [0, 0, 3, 2.4]}),
             el((-0.7, 12.9, -4.5), (0.7, 13.9, -4.0), 'rf_pink', pv),                                           # nose
             el((-1.1, 10.7, -3.6), (1.1, 11.4, -2.0), 'rf_pale', pv),                                           # chin
             # the bandana: wrapped round, the knot at the back with its two tails
             el((-3.25, cap_lo, -2.35), (3.25, 16.5, 2.85), 'rf_red', pv, shift=(0.2, 0.2)),
             el((-1.0, 14.2, 2.8), (1.0, 15.8, 3.6), 'rf_red', pv, shift=(0.6, 0.1)),
             el((-0.2, 12.2, 3.0), (0.7, 14.6, 3.4), 'rf_red', pv, rot=((0.0, 0.0, -18.0), (0.0, 14.4, 3.2))),
             el((0.4, 12.6, 3.0), (1.3, 14.6, 3.4), 'rf_red', pv, rot=((0.0, 0.0, 24.0), (0.8, 14.4, 3.2)))]
        for sx in (-1, 1):                                                                                       # whiskers, two a side
            for dy, a in ((0.0, 8.0), (0.5, -6.0)):
                x0, x1 = sorted((sx * 1.4, sx * 4.6))
                h.append(el((x0, 12.6 + dy, -3.4), (x1, 12.68 + dy, -3.3), 'rf_white', pv, faces=('north', 'south', 'up', 'down'),
                            rot=((0.0, 0.0, a * sx), (sx * 1.4, 12.6 + dy, -3.35))))
            x0, x1 = sorted((sx * 1.8, sx * 4.3))                                                                # ears (out past the bandana)
            h.append(el((x0, 15.0, -0.2), (x1, 18.2, 0.6), 'rf_fur', pv, shift=(0.5 + 0.2 * sx, 0.3)))
            xi0, xi1 = sorted((sx * 2.2, sx * 3.9))
            h.append(el((xi0, 15.4, -0.24), (xi1, 17.8, -0.2), 'rf_pink', pv, faces=('north',)))
        return h
    part('rf_head', head())
    for fc in FACES:
        part(f'rf_head_x{fc}', head(fc))

    # ---- arms: the upper arm (a vest shoulder over it), the forearm and the pink paw
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}']
        x0, x1 = sorted((sx * 3.0, sx * 4.5))
        part(f'rf_arm{s}', [el((x0, 7.8, 0.0), (x1, 10.6, 1.5), 'rf_fur', ap, shift=(0.4, 0.5)),
                            el((x0 - 0.06, 9.3, -0.06), (x1 + 0.06, 10.66, 1.56), 'rf_vest', ap, shift=(0.3, 0.8))])
        part(f'rf_fore{s}', [el((x0 + 0.05, 6.3, 0.05), (x1 - 0.05, 8.1, 1.45), 'rf_fur', fp, shift=(0.7, 0.2)),
                             el((x0, 5.3, 0.0), (x1, 6.4, 1.5), 'rf_pink', fp)])
        # ---- legs: a short thigh under the haunches, a long pink foot
        lp = PIVOT[f'leg{s}']; lx0, lx1 = sorted((sx * 1.0, sx * 3.0))
        part(f'rf_leg{s}', [el((lx0, 0.9, -0.3), (lx1, 3.6, 1.7), 'rf_fur', lp, shift=(0.2 + 0.4 * sx, 0.6))])
        part(f'rf_foot{s}', [el((lx0, 0.0, -2.1), (lx1, 1.0, 1.4), 'rf_pink', PIVOT[f'foot{s}'])])            # (from the ankle: flat on the ground however the leg goes)

    # ---- the tail: long, pink, out behind and curving up a little at the end
    pv = PIVOT['tail']; tx, ty, tz = pv
    part('rf_tail', chain([(0, ty, tz), (0, ty - 1.0, tz + 3.0), (0, ty - 1.6, tz + 6.0), (0, ty - 1.2, tz + 9.0), (0, ty + 0.2, tz + 11.4)],
                          [0.9, 0.8, 0.7, 0.6], 0.9, 'rf_pink', pv, FRONT, ext=0.2))

    # ---- the tools, held in his right paw (the grip at the paw, the business end out ahead of him)
    tp = PIVOT['tool']; X, Y, Z = tp
    part('rf_tool_blade', [el((X - 0.3, Y - 0.35, Z - 0.9), (X + 0.3, Y + 0.25, Z + 1.0), 'rf_oak', tp),             # grip
                           el((X - 0.25, Y - 0.4, Z + 1.0), (X + 0.25, Y + 0.3, Z + 1.5), 'rf_iron', tp),            # pommel
                           el((X - 0.75, Y - 0.55, Z - 1.3), (X + 0.75, Y + 0.45, Z - 0.9), 'rf_iron', tp),          # crossguard
                           el((X - 0.2, Y - 0.3, Z - 6.4), (X + 0.2, Y + 0.2, Z - 1.3), 'rf_steel', tp),             # blade
                           el((X - 0.12, Y - 0.22, Z - 7.0), (X + 0.12, Y + 0.12, Z - 6.4), 'rf_steel', tp)])         # tip
    part('rf_tool_crossbow', [el((X - 0.35, Y - 0.4, Z - 4.4), (X + 0.35, Y + 0.35, Z + 1.6), 'rf_oak', tp),         # stock
                              el((X - 0.25, Y - 1.6, Z + 0.2), (X + 0.25, Y - 0.4, Z + 0.8), 'rf_oak', tp),          # grip
                              el((X - 3.0, Y - 0.15, Z - 4.3), (X + 3.0, Y + 0.25, Z - 3.8), 'rf_ink', tp),          # the bow
                              el((X - 3.0, Y - 0.1, Z - 3.8), (X - 2.5, Y + 0.2, Z - 3.2), 'rf_ink', tp),
                              el((X + 2.5, Y - 0.1, Z - 3.8), (X + 3.0, Y + 0.2, Z - 3.2), 'rf_ink', tp),
                              el((X - 2.7, Y + 0.0, Z - 1.9), (X + 2.7, Y + 0.08, Z - 1.8), 'rf_white', tp, faces=('up', 'down', 'north', 'south')),   # string, drawn
                              el((X - 2.7, Y + 0.0, Z - 3.6), (X - 2.55, Y + 0.08, Z - 1.85), 'rf_white', tp, faces=('up', 'down', 'east', 'west')),
                              el((X + 2.55, Y + 0.0, Z - 3.6), (X + 2.7, Y + 0.08, Z - 1.85), 'rf_white', tp, faces=('up', 'down', 'east', 'west')),
                              el((X - 0.12, Y + 0.35, Z - 5.0), (X + 0.12, Y + 0.55, Z - 1.8), 'rf_oak', tp),        # the bolt
                              el((X - 0.2, Y + 0.3, Z - 5.5), (X + 0.2, Y + 0.6, Z - 5.0), 'rf_iron', tp)])
    part('rf_tool_coins', [el((X - 0.9 + 0.1 * i, Y - 0.2 + 0.3 * i, Z - 2.1 + 0.05 * i), (X + 0.9 + 0.1 * i, Y + 0.05 + 0.3 * i, Z - 0.3 + 0.05 * i),
                              'rf_gold', tp) for i in range(3)] +                                                 # (a little stack)
                          [el((X - 0.8, Y + 1.6, Z - 2.0), (X + 0.8, Y + 1.85, Z - 0.4), 'rf_gold', tp, rot=((60.0, 0.0, 0.0), (X, Y + 1.7, Z - 1.2)))])
    part('rf_tool_none', [el((X - 0.01, Y - 0.01, Z - 0.01), (X + 0.01, Y + 0.01, Z + 0.01), 'rf_ink', tp, faces=('north',))])
    M['rf_tool'] = M['rf_tool_blade']

    # ---- the crossbow slung across his back (shown when it isn't in his paw); the scabbard at his left hip (when the blade isn't)
    pv = PIVOT['slung']; sx_, sy_, sz_ = pv; ro = ((0.0, 0.0, -38.0), pv)
    part('rf_slung', [el((sx_ - 0.35, sy_ - 4.4, sz_ + 0.1), (sx_ + 0.35, sy_ + 2.0, sz_ + 0.8), 'rf_oak', pv, rot=ro),
                      el((sx_ - 2.8, sy_ + 1.6, sz_ + 0.15), (sx_ + 2.8, sy_ + 2.0, sz_ + 0.65), 'rf_ink', pv, rot=ro),
                      el((sx_ - 2.6, sy_ + 0.4, sz_ + 0.3), (sx_ + 2.6, sy_ + 0.48, sz_ + 0.5), 'rf_white', pv, rot=ro, faces=('up', 'down', 'north', 'south'))])
    pv = PIVOT['sheath']; hx, hy, hz = pv; ro = ((-24.0, 0.0, 0.0), pv)
    part('rf_sheath', [el((hx - 0.35, hy - 5.2, hz - 0.35), (hx + 0.35, hy, hz + 0.45), 'rf_vest', pv, rot=ro, shift=(0.6, 0.4)),
                       el((hx - 0.25, hy - 5.6, hz - 0.25), (hx + 0.25, hy - 5.2, hz + 0.35), 'rf_iron', pv, rot=ro),
                       el((hx - 0.75, hy, hz - 0.45), (hx + 0.75, hy + 0.4, hz + 0.55), 'rf_iron', pv, rot=ro),
                       el((hx - 0.3, hy + 0.4, hz - 0.2), (hx + 0.3, hy + 2.0, hz + 0.4), 'rf_oak', pv, rot=ro)])
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit: ('x', -a) swings a hanging limb forward by a; ('x', +a) on the body or head leans/nods it forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


def tail(y=0.0, x=0.0):
    return dict(tail=qs(('y', y), ('x', x)))


s = math.sin
REST = dict(armr=limb(1, 8, 8), forer=limb(1, 22), arml=limb(-1, 4, 8), forel=limb(-1, 10))
POSES = {
    # standing about: blade at the ready, low; weight on one foot, tail idling
    'idle_a': P(**REST, **tail(8, -4)),
    # sizing you up: the head turned, his left fist on his hip
    'idle_b': P(_face='squint', armr=limb(1, 8, 8), forer=limb(1, 22), arml=limb(-1, -10, 42), forel=limb(-1, 0, -80), head=qs(('y', 28), ('x', -4)), **tail(-16, 6)),
    # nose up, sniffing the air; whiskers twitching
    'idle_c': P(_face='blink', **REST, head=qs(('x', -22)), body=qs(('x', -3)), **tail(20, -10)),
    **{f'walk_{i}': P(_off=(0, 0.25 * abs(s(math.pi * i / 2)), 0), legr=limb(1, 26 * s(math.pi * i / 2)), legl=limb(-1, -26 * s(math.pi * i / 2)),
                      armr=limb(1, 8 - 18 * s(math.pi * i / 2), 8), forer=limb(1, 22), arml=limb(-1, 18 * s(math.pi * i / 2), 8), forel=limb(-1, 12),
                      head=qs(('x', 3)), **tail(14 * s(math.pi * i / 2), -4)) for i in range(4)},
    **{f'run_{i}': P(_off=(0, (0.4, 1.0, 0.4, 0.0)[i], 0), body=qs(('x', 16)), head=qs(('x', -14)),
                     legr=limb(1, (46, 10, -40, 10)[i]), legl=limb(-1, (-40, 10, 46, 10)[i]),
                     armr=limb(1, (-30, 0, 40, 0)[i] + 10, 10), forer=limb(1, 40), arml=limb(-1, (40, 0, -30, 0)[i], 10), forel=limb(-1, 40),
                     **tail(10 * (1 - 2 * (i % 2)), -14)) for i in range(4)},
    'jump': P(_off=(0, 2.4, 0), _face='grin', legr=limb(1, 44), legl=limb(-1, -24), armr=limb(1, 40, 26), forer=limb(1, 30), arml=limb(-1, 30, 30), forel=limb(-1, 20),
              head=qs(('x', -6)), **tail(0, -24)),
    # the blade: up and back over his right shoulder ...
    'slash_up': P(_face='angry', body=qs(('y', 18)), armr=limb(1, 150, 24), forer=limb(1, 40), arml=limb(-1, 30, 20), forel=limb(-1, 30),
                  legr=limb(1, -12), legl=limb(-1, 16), head=qs(('y', -14)), **tail(-24, -8)),
    # ... and down across, stepping into it
    'slash': P(_face='angry', _off=(0, 0, -0.6), body=qs(('y', -22), ('x', 10)), armr=limb(1, 74, -18), forer=limb(1, 6), tool=qs(('y', 34), ('x', -10)),
               arml=limb(-1, -20, 24), forel=limb(-1, 20),
               legr=limb(1, 22), legl=limb(-1, -18), head=qs(('y', 16), ('x', -8)), **tail(28, -10)),
    # the crossbow up to his eye, his left paw under the stock
    'aim': P(_tool='crossbow', _face='squint', armr=limb(1, 84, 0, -6), forer=limb(1, 6), tool=qs(('x', 90)), arml=limb(-1, 70, -12, 28), forel=limb(-1, 34),
             head=qs(('x', 6), ('y', -6)), legr=limb(1, -10), legl=limb(-1, 12), **tail(-14, -6)),
    'shoot': P(_tool='crossbow', _face='grin', _off=(0, 0, 0.3), body=qs(('x', -5)), armr=limb(1, 98, 0, -6), forer=limb(1, 4), tool=qs(('x', 102)),
               arml=limb(-1, 82, -12, 28), forel=limb(-1, 34), head=qs(('x', -4)), legr=limb(1, -14), legl=limb(-1, 12), **tail(-10, -20)),
    # reloading: the crossbow nose-down in front of him, a foot in the stirrup, hauling the string back
    'reload': P(_tool='crossbow', _face='angry', body=qs(('x', 18)), armr=limb(1, 26, 6), forer=limb(1, 30), tool=qs(('x', -40)),
                arml=limb(-1, 50, -8, 20), forel=limb(-1, 70), legr=limb(1, 26), head=qs(('x', 18)), **tail(16, -6)),
    # sitting cross-legged on the ground (as on a crate): the legs folded in front, paws on his knees
    'sit_a': P(_off=(0, -2.4, 0), legr=limb(1, 84, 22), legl=limb(-1, 84, 22), footr=qs(('x', -84), ('y', -62)), footl=qs(('x', -84), ('y', 62)),
               armr=limb(1, 26, 10), forer=limb(1, 40),
               arml=limb(-1, 26, 10), forel=limb(-1, 40), head=qs(('x', 4)), tail=qs(('y', 70), ('x', 60))),
    # leaning back on his elbows, ankles crossed, the bandana pulled down over his eyes: off duty
    'sit_b': P(_off=(0, -2.4, 0.8), _face='shade', body=qs(('x', -34)), head=qs(('x', 14)), legr=limb(1, 62, -4), legl=limb(-1, 52, -6, -10),
               footr=qs(('x', -30)), footl=qs(('x', -20)),
               armr=limb(1, -50, 18), forer=limb(1, -20), arml=limb(-1, -50, 18), forel=limb(-1, -20), _tool='none', tail=qs(('y', 50), ('x', 70))),
    # (2.96c) riding Bender: astride, his short legs gripping either side, paws on the scruff, tail out behind for balance
    'ride': P(_face='grin', _tool='none', legr=limb(1, 40, 46), legl=limb(-1, 40, 46), footr=qs(('x', -30)), footl=qs(('x', -30)),
              armr=limb(1, 60, 6), forer=limb(1, 30), arml=limb(-1, 60, 6), forel=limb(-1, 30), head=qs(('x', 6)), tail=qs(('x', 50), ('y', 0))),
    'hurt': P(_face='hurt', _off=(0, 0, 0.4), body=qs(('x', -12)), head=qs(('x', -14)), armr=limb(1, 30, 30), forer=limb(1, 20), arml=limb(-1, 30, 30), forel=limb(-1, 20),
              legr=limb(1, 14), legl=limb(-1, -8), **tail(0, -30)),
    # worn out: hunched, the blade point down, the head hanging
    'tired': P(_face='blink', _off=(0, -0.3, 0), body=qs(('x', 14)), head=qs(('x', 24)), armr=limb(1, -4, 4), forer=limb(1, -2), tool=qs(('x', -60)),
               arml=limb(-1, 0, 4), forel=limb(-1, 0), legr=limb(1, 8), legl=limb(-1, -4), **tail(0, 30)),
    **{f'swim_{i}': P(_off=(0, 2.0, 0), _tool='none', body=qs(('x', 72)), head=qs(('x', -60)),
                      armr=limb(1, 150 + 30 * s(math.pi * i / 4), 20), forer=limb(1, 20), arml=limb(-1, 150 - 30 * s(math.pi * i / 4), 20), forel=limb(-1, 20),
                      legr=limb(1, -20 * s(math.pi * i / 4)), legl=limb(-1, 20 * s(math.pi * i / 4)), **tail(24 * s(math.pi * i / 4), -70)) for i in range(8)},
    'happy': P(_face='grin', _off=(0, 0.6, 0), armr=limb(1, 30, 50), forer=limb(1, 50), arml=limb(-1, 30, 50), forel=limb(-1, 50), head=qs(('z', 10)),
               **tail(24, -30)),
    # the salute: two fingers off the bandana's brim
    'salute': P(_face='grin', armr=limb(1, 24, 84), forer=limb(1, 20, 150), arml=limb(-1, 0, 6), forel=limb(-1, 0), _tool='none', head=qs(('x', -2)),
                **tail(10, -8)),
    # counting his pay: the coins in his right paw, held up close, his left paw picking through them
    'count_coins': P(_tool='coins', _face='grin', armr=limb(1, 40, 0, -20), forer=limb(1, 56), arml=limb(-1, 50, 0, -36), forel=limb(-1, 50),
                     head=qs(('x', 26)), **tail(12, -4)),
}
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'run_1', 'jump', 'slash_up', 'slash', 'aim', 'shoot', 'reload', 'sit_a', 'sit_b', 'hurt',
         'tired', 'swim_2', 'happy', 'salute', 'count_coins']
