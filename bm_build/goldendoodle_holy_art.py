"""(3.1 draft, stage 1: art only - not wired) THE GOLDEN DOODLE, LIGHTBRINGER FORM - her third form: the Gilded Eldritch's holy
mirror (goldendoodle_pet_art.py is the goose, goldendoodle_boss_art.py the Eldritch; the design: scratchpad/design_goldendoodle.md).

The owner: "once she's recruited, the Golden Doodle also gets an ANGELIC 'Lightbringer' form, a holy counterpart to the Gilded
Eldritch. Tie it into the phase-2 defeat: the Lightbringer cures her of the dread with her light."

THE STORY IN THE ART  The Lightbringer's light burned the Dread's shard out of her - and what it left is the Eldritch made whole:
       where the shard's crown was, a HALO (two rings: her gold one, and a tilted second ring beaded with sapphires - the Ophanim's
       wheel, echoed); where every crack ran, white-gold; where its many eyes were, two calm, kind gold eyes; its split neck one
       neck again, long and pure; its bone wings SIX FEATHERED WINGS OF LIGHT (a seraph's: two raised over her, two at her sides,
       two folded round her breast), in the Lightbringer's own feathers. The clover on her breast is a gold sun now - the
       Lightbringer's sun, off her stole - with the clover still at its heart.
LOOK   As big as the Eldritch (RIG_SCALE 0.9: ~3.3 blocks to her halo; COMPANION 0.55: ~2 blocks), but a SWAN's poise where the Eldritch
       rears: the breast high and smooth, the long neck in one serene S, a small refined head, a gold bill with a pearl nail.
         - Her feathers: pearl-white leaf in soft scalloped rows (the goose's feather rows, repainted), gold at every edge that
           catches the light; the belly pearl down; the neck's soft furrows white-gold.
         - THE WINGS are the Lightbringer's: her translucent pearl feathers (lb_feather) and coverts (lb_covert) with glowing gold
           tips (lb_tip), the primaries' ends royal blue (lb_tip_blue) - so the two of them read as one light.
         - THE TAIL: a lyre of long pearl plumes with gold tips, flowing, never ragged.
         - THE FEET: gold paddles with pearl webbing, whole again.
         - GLOW, soft and placed: the halo (15), the wing tips (12), the sun on her breast (10), the eyes (6). (THE GLOW RULE, for the
           wiring: a Glowing outline goes on her displays, never her invisible host.)
RIG    body (root) - tail - neck1 - neck2 - neck3 (one neck, the Eldritch's three joints: the forms tween part for part) - head (face
       part) - jaw - halo (on the head) - wr / wl + wr2 / wl2 (the upper pair: arm and hand, so they fold) - wmr / wml (the middle
       pair) - wlr / wll (the lower pair) - legr / legl - footr / footl; fx: 'beam' (THE HOLY BEAM: a pillar of light called down
       on a foe), 'gust' (THE WING GUST: arcs of wind and loose feathers), 'cure' (the cure's light: a sunburst ring round her
       feet), 'aura' (the rare aura of this form: a slow wheel of light).
SKINS  '_rg' ROSE GOLD, '_pt' PLATINUM (the goose's cosmetics, in this form too), '_sh' SHINY FOUR-LEAF (pale emerald light, gold).
"""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import Rig, hexc, mix, limb, T, cells, lit, glow, put, slab, stack, profile, ring, leaf, cleaf, eye, blush, hue, recolor
from rigkit import qs
import rigkit
import goldendoodle_pet_art as GQ
import lightbringer_art as LBA

PIVOT = {'body': (0, 21.0, 3.0), 'tail': (0, 21.0, 15.0), 'neck1': (0, 27.0, -6.5), 'neck2': (0, 34.0, -10.5), 'neck3': (0, 41.0, -12.0),
         'head': (0, 46.5, -13.0), 'jaw': (0, 47.0, -18.0), 'halo': (0, 53.5, -14.0),
         'wr': (7.0, 29.0, 0.0), 'wl': (-7.0, 29.0, 0.0), 'wr2': (24.0, 37.0, 2.0), 'wl2': (-24.0, 37.0, 2.0),
         'wmr': (8.6, 24.0, 2.0), 'wml': (-8.6, 24.0, 2.0), 'wlr': (6.0, 19.0, -6.0), 'wll': (-6.0, 19.0, -6.0),
         'legr': (5.4, 15.0, 3.0), 'legl': (-5.4, 15.0, 3.0), 'footr': (6.0, 2.6, 1.6), 'footl': (-6.0, 2.6, 1.6),
         'beam': (0, 0, -30.0), 'gust': (0, 24.0, -26.0), 'cure': (0, 0, 0), 'aura': (0, 30.0, 0)}
PARENT = {'body': None, 'tail': 'body', 'neck1': 'body', 'neck2': 'neck1', 'neck3': 'neck2', 'head': 'neck3', 'jaw': 'head', 'halo': 'head',
          'wr': 'body', 'wl': 'body', 'wr2': 'wr', 'wl2': 'wl', 'wmr': 'body', 'wml': 'body', 'wlr': 'body', 'wll': 'body',
          'legr': 'body', 'legl': 'body', 'footr': 'legr', 'footl': 'legl', 'beam': None, 'gust': 'body', 'cure': None, 'aura': None}
FACES = ('happy', 'blink', 'fierce', 'surprised', 'sad')
OPT = ('beam', 'gust', 'cure', 'aura')
R = Rig('gh_', 0.9, PIVOT, PARENT, FACES, face_part='head', opt=OPT, companion=0.55)
COMPANION = 0.55                 # (its menu's Companion Size: ~2 blocks - compsize twins the rig at COMPANION / RIG_SCALE)
SKIN_NAMES = {'_rg': 'cosmetic: Rose Gold', '_pt': 'cosmetic: Platinum', '_sh': 'SHINY: Four-Leaf'}

# ---------------------------------------------------------------------------------------------------- palette and textures
PW = dict(deep='#b09050', dark='#e8d8b0', base='#fff8e8', light='#ffffff', shine='#ffffff', white='#ffffff')       # (pearl-white leaf, warm)
PG = dict(deep='#7a5410', dark='#b8862a', base='#ecc456', light='#ffe48a', shine='#fff8d0', white='#ffffff')       # (her gold)
PDOWN = dict(dark='#ecdcbc', base='#fffaee', light='#ffffff', shine='#ffffff')
BILL = dict(deep='#6a4a08', dark='#b8841a', base='#eab838', light='#ffe07a', hot='#fff4c0')
_LB = LBA.textures()


def edged(P, G, seed, w=6, rows=4):
    """pearl feathers whose tips catch the light in GOLD: the goose's feather rows, repainted; the tip row gold, its corners pearl"""
    im = GQ.feathers(P, seed, w=w, rows=rows, sparks=0)
    px = im.load(); tip = hexc(mix(P['light'], G['base'], 0.7))
    for y in range(64):
        cy = (y // 2) % rows
        if cy != rows - 1: continue
        for x in range(64):
            cx = x // 2; lx = (cx + ((y // 2) // rows % 2) * (w // 2)) % w
            if 0 < lx < w - 1: px[x, y] = tip
    return im


def sun_tex():
    """the sun on her breast (full uv): the Lightbringer's gold sun - twelve rays round a disc - with the clover at its heart"""
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(12):
        a = math.radians(i * 30); L = 15 if i % 2 == 0 else 11.5
        d.line((16, 16, 16 + L * math.cos(a), 16 + L * math.sin(a)), fill=hexc(PG['light'] if i % 2 == 0 else PG['base']), width=2)
    d.ellipse((8, 8, 24, 24), fill=hexc(PG['base'])); d.ellipse((9, 9, 23, 23), fill=hexc(PG['light']))
    for ang in (45, 135, 225, 315):
        a = math.radians(ang); cx, cy = 16 + 3.2 * math.cos(a), 16 + 3.2 * math.sin(a)
        d.ellipse((cx - 2.8, cy - 2.8, cx + 2.8, cy + 2.8), fill=hexc(GQ.EMER[2]))
    d.ellipse((14.5, 14.5, 17.5, 17.5), fill=hexc('#ffffff'))
    return im


KIND_IRIS = ('#8a4a06', '#b8700e', '#dc9a1e', '#f4c03a', '#fcde6a', '#fff4b0')   # (the Lightbringer's amber-to-pale-gold, a touch warmer)


def kind_eye(im, x0, y0, kind=None, flip=False, W=16):
    """one calm, kind gold eye in a W x W window (window x 0 = the back of the head, before flip): an amber-to-pale-gold oval,
    a soft dark pupil, one big shine up toward the front, a warm brown upper lid that sits a little low (serene), a blush below.
    kinds: None (serene), happy (^, gold), blink, fierce (the lid slanting down to the front), surprised (round, the lid up),
    sad (the lid slanting down to the back, a tear)"""
    from fol5_kit import _ell
    fx = (lambda x: x0 + (W - 1 - x)) if flip else (lambda x: x0 + x)
    P = lambda x, y, c: put(im, fx(x), y0 + y, c)
    for x, y in ((3, 13), (4, 13), (5, 13), (6, 13), (4, 14), (5, 14)): P(x, y, '#f6c4b4')
    lid = '#7a4a1a'
    if kind == 'happy':
        for x in range(4, 14):
            y = 6 if 6 < x < 11 else 7 if x in (5, 6, 11, 12) else 8
            P(x, y, '#c88a20'); P(x, y + 1, lid)
        return
    if kind == 'blink':
        for x in range(4, 14): P(x, 8 if x in (4, 13) else 9, lid); P(x, 10, lid) if 6 < x < 11 else None
        return
    cx, cy, rx, ry = 8.8, 7.4, 3.6, (4.4 if kind == 'surprised' else 4.0)
    S = _ell(cx, cy, rx, ry)
    top, bot = min(y for _, y in S), max(y for _, y in S)
    for x, y in S:
        t = (y - top) / max(1, bot - top); P(x, y, KIND_IRIS[min(5, int(t * 6))])
    for x, y in _ell(cx + 0.2, cy + 0.4, 1.4, 1.8): P(x, y, '#4a2408')
    sx = max(x for x, _ in S) - 3
    for dx in range(2):
        for dy in range(2): P(sx + dx, top + 1 + dy, '#ffffff')
    P(min(x for x, _ in S) + 2, bot - 1, '#fff6d8')
    xs = range(min(x for x, _ in S) - 1, max(x for x, _ in S) + 2)
    for x in xs:
        if kind == 'fierce': y = top + 1 + round((x - 4) * 0.45)
        elif kind == 'sad': y = top + 1 + round((13 - x) * 0.45)
        elif kind == 'surprised': y = top - 1
        else: y = top + 1
        for yy in range(top - 1, y):
            if (x, yy) in S: P(x, yy, '#f6ead2')
        P(x, y, lid); P(x, y - 1, lid) if kind in (None, 'fierce', 'sad') and 0.25 < (x - xs[0]) / len(xs) < 0.8 else None
    if kind == 'sad':
        for dy, c in ((0, '#bfe6ff'), (1, '#e8f8ff'), (2, '#bfe6ff')): P(4, bot + 1 + dy, c)


def eyes(kind=None):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    kind_eye(im, 0, 0, kind); kind_eye(im, 16, 0, kind, flip=True)
    return im


def _tex(P=PW, G=PG, D=PDOWN, Bl=BILL, emer=GQ.EMER):
    t = {'hf': edged(P, G, 51), 'hf2': edged(P, G, 52, w=7), 'hdown': GQ.down(D, 53), 'hneck': GQ.furrows({**P, 'light': G['light']}, 54),
         'hprim': GQ.primaries({**P, 'shine': G['shine'], 'light': G['light']}, 55), 'hgold': GQ.feathers(G, 56, sparks=0),
         'hlip': lit(edged(P, G, 57), 1.15, 1.0, 4), 'hbill': GQ.orange(Bl, 58), 'hbill_d': GQ.orange({**Bl, 'base': Bl['dark'], 'light': Bl['base']}, 59),
         'hleg': GQ.orange(Bl, 60, scutes=True), 'hweb': cells(lambda x, y, r: PDOWN['base'] if x % 6 else PDOWN['dark'], 61),
         'hnail': cells(lambda x, y, r: '#fffaf0', 0), 'hgrin': cells(lambda x, y, r: '#7a5410', 0), 'hmouth': cells(lambda x, y, r: '#e89aa0', 0),
         'sun': sun_tex(), 'spark': GQ.spark_tex(), 'ring': GQ.ring_tex('#fff4c0', 190),
         'pillar': cells(lambda x, y, r: (*hexc(mix('#ffffff', '#ffd040', abs(x - 15.5) / 16))[:3], int(250 - 150 * abs(x - 15.5) / 16)), 0),
         'gem': GQ.gemtex(emer), 'eyes': eyes()}
    for f in FACES: t[f'eyes_{f}'] = eyes(f)
    for k in ('lb_feather', 'lb_covert', 'lb_tip', 'lb_tip_blue', 'lb_gold', 'lb_halo', 'lb_light', 'lb_sapph'): t[k[3:]] = _LB[k]
    return t


TEX = _tex()
for k, v in TEX.items(): R.tex(k, v)

# ---------------------------------------------------------------------------------------------------- helpers (on this rig)
B = R.box


def zslab(part, z0, z1, hw, hh, tex, c=(0.0, 0.0), k=0.7, light=0):
    x, y = c
    return [B(part, (x - hw, y - hh * k, z0), (x + hw, y + hh * k, z1), tex, light=light),
            B(part, (x - hw * k, y + hh * k, z0), (x + hw * k, y + hh, z1), tex, light=light),
            B(part, (x - hw * k, y - hh, z0), (x + hw * k, y - hh * k, z1), tex, light=light)]


def zegg(part, z0, z1, r, tex, yc, n=9, sq=0.84, blunt=1.35, power=1.2, under=None, light=3):
    out = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n; t = (t0 + t1) / 2
        u = (t - 0.36) / (0.64 if t > 0.36 else 0.36)
        w = max(0.6, r * max(0.0, 1 - abs(u) ** (blunt if u < 0 else 1.6)) ** (0.5 / power))
        es = zslab(part, z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1, w, w * sq, tex(t) if callable(tex) else tex, c=(0.0, yc(t)), k=0.7, light=light)
        if under:
            for f in es[2]['faces'].values(): f['texture'] = '#' + under
        out += es
    return out


def rod(part, pts, ws, tex, front=(0.0, 0.0, -1.0), k=0.8, ext=0.15):
    f2 = (front[0] + (0.7 if abs(front[0]) < 0.5 else 0.0), front[1], front[2] * 0.7 + (0.0 if abs(front[0]) < 0.5 else 0.7))
    out = []
    for i in range(len(pts) - 1):
        w = (ws[i] + ws[i + 1]) / 2
        out.append(R.seg(part, pts[i], pts[i + 1], w, w, tex, front, ext=ext))
        out.append(R.seg(part, pts[i], pts[i + 1], w * k * 1.12, w * k * 1.12, tex, f2, ext=ext * 0.3))
    return out


def sparkle3d(part, c, s, light=15):
    x, y, z = c
    B(part, (x - s, y - s, z), (x + s, y + s, z + 0.01), 'spark', faces=('north', 'south'), full=True, light=light)
    B(part, (x, y - s, z - s), (x + 0.01, y + s, z + s), 'spark', faces=('east', 'west'), full=True, light=light)


def feather_wing(part, root, sx, span, rise, back, n, flen, fw=2.4, hand=None, hand_at=0.62, lean=0.25, cov=True):
    """a feathered wing of light, the Lightbringer's way: a leading edge (coverts, lb_covert) from the root out along an arc, and n
    feathers hanging back from it (lb_feather, translucent pearl), each with a glowing gold tip (lb_tip; the outermost royal blue).
    flen(u): a feather's length at u (0 root .. 1 tip). hand: the part the outer half (u > hand_at) is built on (so the wing folds)"""
    x0, y0, z0 = root
    L = lambda u: (x0 + sx * span * u, y0 + rise * math.sin(math.pi * u * 0.75), z0 + back * u)
    pts = [L(u / 6) for u in range(7)]
    for i in range(6):
        u = (i + 0.5) / 6; p = hand if (hand and u > hand_at) else part
        w = 2.6 - 1.4 * u
        R.seg(p, pts[i], pts[i + 1], w, w * 0.6, 'covert', up=(0.0, 1.0, 0.0), ext=0.25, light=6)
        if cov: R.seg(p, pts[i], pts[i + 1], w * 0.7, w * 0.4, 'gold', up=(0.0, 1.0, 0.0), ext=0.1)
    for k in range(n):
        u = 0.08 + 0.92 * k / max(1, n - 1); p = hand if (hand and u > hand_at) else part
        A = L(u); Lf = flen(u)
        d = (sx * lean * u, -1.0, 0.45 + 0.35 * u)
        m = math.sqrt(sum(v * v for v in d)); d = tuple(v / m for v in d)
        Bp = tuple(A[i] + d[i] * Lf * 0.82 for i in range(3)); Tp = tuple(A[i] + d[i] * Lf for i in range(3))
        R.seg(p, A, Bp, fw, 0.3, 'feather', up=(0.0, 0.0, -1.0), ext=0.1, light=7)
        R.seg(p, Bp, Tp, fw * 0.7, 0.32, 'tip_blue' if k >= n - 2 and Lf > 8 else 'tip', up=(0.0, 0.0, -1.0), ext=0.05, light=12)


# ---------------------------------------------------------------------------------------------------- the body: a swan's poise
zegg('body', -11.0, 15.0, 9.2, 'hf', lambda t: 22.6 - 4.0 * t, n=11, sq=0.8, under='hdown')
zegg('body', -12.0, -2.0, 6.8, 'hf2', lambda t: 22.0 - 0.8 * t, n=5, sq=0.86, blunt=0.9, power=1.0)
zegg('body', 0.0, 12.0, 5.6, 'hdown', lambda t: 14.6 - 0.6 * t, n=5, sq=0.6)                          # (the paunch, tidy now)
R.seg('body', (0, 29.4, -6.0), (0, 30.2, 8.0), 7.0, 0.7, 'hlip', shift=False)                          # (the back's lit covert run)
B('body', (-2.6, 19.8, -12.95), (2.6, 25.0, -12.93), 'sun', faces=('north',), full=True, light=10)       # (the sun, the clover at its heart)
for c, s in (((-3.0, 31.4, 2.0), 1.2), ((-4.2, 32.6, 3.4), 0.8), ((2.4, 31.8, 6.0), 0.6)): sparkle3d('body', c, s)

# ---- the tail: a lyre of long pearl plumes, gold-tipped, flowing
for i, (sx, L, up_) in enumerate(((0, 14.0, 0.34), (0.5, 12.6, 0.42), (-0.5, 12.6, 0.42), (0.95, 10.4, 0.55), (-0.95, 10.4, 0.55))):
    cleaf(R, 'tail', (sx * 2.0, 21.4, 13.4), (sx * 0.38, up_, 1.0), L, 2.6 - abs(sx) * 0.5, 'hprim', droop=-0.12, t=0.45, n=4, full=False)
    tip = (sx * 2.0 + sx * 0.38 * L * 0.9, 21.4 + up_ * L * 0.8, 13.4 + L * 0.9)
    R.seg('tail', tip, (tip[0] + sx * 0.3, tip[1] + 0.8, tip[2] + 1.8), 1.4, 0.4, 'tip', light=12)
R.seg('tail', (0, 21.4, 11.0), (0, 22.4, 15.6), 5.0, 3.0, 'hf2', ext=0.3)

# ---------------------------------------------------------------------------------------------------- the neck: one, pure, serene
N1 = [(0, 25.6, -7.6), (0, 29.6, -10.4), (0, 33.4, -11.4), (0, 34.6, -11.2)]
N2 = [(0, 34.2, -11.2), (0, 37.8, -10.6), (0, 40.8, -10.8), (0, 41.6, -11.4)]
N3 = [(0, 41.2, -11.4), (0, 44.0, -12.2), (0, 46.6, -13.0)]
zslab('neck1', -12.0, -4.0, 4.8, 3.8, 'hf', c=(0, 26.0), k=0.66)
for _p, _pts, _ws in (('neck1', N1, [4.6, 3.6, 3.2, 3.1]), ('neck2', N2, [3.1, 2.9, 2.8, 2.8]), ('neck3', N3, [2.8, 2.7, 2.8])):
    for _e in rod(_p, _pts, _ws, 'hneck'): _e['light_emission'] = 3
for part, pts in (('neck1', N1), ('neck2', N2), ('neck3', N3)):                  # (a fine gold line down the front of the neck)
    R.seg(part, (0, pts[0][1], pts[0][2] - 1.45), (0, pts[-1][1], pts[-1][2] - 1.35), 0.5, 0.2, 'gold', up=(0.0, 0.0, -1.0), light=4)

# ---------------------------------------------------------------------------------------------------- the head: refined, kind
HY = 47.4
zegg('head', -19.0, -11.0, 3.2, 'hf', lambda t: HY + 0.3 * t, n=6, sq=0.9, blunt=1.0, power=1.1)
slab(R, 'head', HY + 2.6, HY + 3.2, 1.8, 'hf', 2.6, c=(0, -14.8), k=0.66)
R.seg('head', (0, HY + 2.4, -15.6), (0, HY + 1.6, -18.6), 2.8, 0.9, 'hlip', ext=0.1)
R.seg('head', (0, HY - 0.2, -18.8), (0, HY - 0.5, -21.6), 3.0, 1.6, 'hbill', ext=0.1)
R.seg('head', (0, HY - 0.55, -21.5), (0, HY - 0.75, -23.6), 2.1, 1.25, 'hbill', ext=0.05)
R.seg('head', (0, HY - 0.8, -23.5), (0, HY - 0.95, -24.0), 1.3, 0.9, 'hnail')
for sx in (1, -1):
    R.seg('head', (sx * 1.4, HY - 0.8, -19.0), (sx * 1.0, HY - 1.0, -23.4), 0.22, 0.38, 'hgrin', up=(0, 1, 0))
stack(R, 'head', [(HY + 0.4, HY + 1.0, 1.4, 1.0), (HY + 1.0, HY + 1.9, 1.6, 1.2)], 'hbill', c=(0, -19.0), k=0.62)   # (the knob, gold)
R.box('head', (-0.65, HY + 0.6, -20.3), (0.65, HY + 1.9, -19.95), 'gem', rot=('z', 45.0, (0, HY + 1.25, -20.1)), light=8)   # (the emerald, back)
for sx in (1, -1):                                                                      # (the eyes, on soft bumps, turned forward)
    xc, yc, zc, a = sx * 2.85, HY + 0.6, -16.6, 24.0 * sx
    B('head', (xc - 0.6, yc - 2.0, zc - 2.0), (xc + 0.6, yc + 2.0, zc + 2.0), 'hf2', rot=('y', a, (xc, yc, zc)))
    x = xc + 0.61 * sx
    B('head', (min(x, x + 0.02 * sx), yc - 2.0, zc - 2.0), (max(x, x + 0.02 * sx), yc + 2.0, zc + 2.0), 'EYES', faces=('east' if sx > 0 else 'west',),
      uv={'east' if sx > 0 else 'west': [0, 0, 4, 4] if sx > 0 else [4, 0, 8, 4]}, light=6, rot=('y', a, (xc, yc, zc)))
# ---- the jaw
R.seg('jaw', (0, HY - 1.3, -18.8), (0, HY - 1.55, -22.4), 2.6, 0.8, 'hbill_d', ext=0.1)
B('jaw', (-0.9, HY - 1.0, -21.8), (0.9, HY - 0.85, -19.2), 'hmouth')
# ---- THE HALO: her gold ring over the head, and a tilted second ring beaded with sapphires (the Ophanim's wheel, echoed)
ring(R, 'halo', (0, 53.5, -14.0), 4.4, 14, 0.8, 0.5, 'halo', light=15)
ring(R, 'halo', (0, 53.5, -14.0), 3.8, 14, 0.35, 0.25, 'light', light=15)
for k in range(12):
    a = math.radians(k * 30); x, y = 5.6 * math.cos(a), 50.0 + 5.6 * math.sin(a)
    R.seg('halo', (x, y, -8.6), (5.6 * math.cos(a + math.radians(30)), 50.0 + 5.6 * math.sin(a + math.radians(30)), -8.6), 0.45, 0.45, 'gold', up=(0.0, 0.0, -1.0), light=12)
    if k % 3 == 0: R.box('halo', (x - 0.5, y - 0.5, -9.1), (x + 0.5, y + 0.5, -8.1), 'sapph', rot=((35.26, 45.0, 0.0), (x, y, -8.6)), light=10)

# ---------------------------------------------------------------------------------------------------- THE SIX WINGS (the Lightbringer's feathers)
for sx, a, h, m, lo in ((1, 'wr', 'wr2', 'wmr', 'wlr'), (-1, 'wl', 'wl2', 'wml', 'wll')):
    # the upper pair: the great wings, built spread (folded / raised by the poses); the outer half on the hand
    feather_wing(a, PIVOT[a], sx, 30.0, 9.0, 3.0, 12, lambda u: 6.0 + 13.0 * u ** 0.8, fw=2.6, hand=h, hand_at=0.55)
    # the middle pair: at her sides, a little smaller, hanging lower
    feather_wing(m, PIVOT[m], sx, 16.0, 3.0, 4.0, 8, lambda u: 5.0 + 8.0 * u, fw=2.2, lean=0.15)
    # the lower pair: small, folded forward round her breast (a seraph's covering wings)
    x0, y0, z0 = PIVOT[lo]
    for k in range(6):
        u = k / 5.0
        A = (x0 + sx * (1.2 + 1.6 * u), y0 + 2.0 - 1.0 * u, z0 + 1.0 - 3.6 * u)
        Tp = (A[0] + sx * (0.8 + 0.8 * u), A[1] - 6.0 - 3.0 * u, A[2] - 2.6 - 1.2 * u)
        Mp = tuple(A[i] + (Tp[i] - A[i]) * 0.8 for i in range(3))
        R.seg(lo, A, Mp, 2.0, 0.3, 'feather', up=(float(sx), 0.0, -0.4), ext=0.1, light=7)
        R.seg(lo, Mp, Tp, 1.4, 0.32, 'tip', up=(float(sx), 0.0, -0.4), ext=0.05, light=12)
    R.seg(lo, (x0, y0 + 2.4, z0 + 1.4), (x0 + sx * 3.2, y0 + 1.0, z0 - 2.6), 2.2, 1.0, 'covert', up=(float(sx), 0.0, 0.0), ext=0.2)

# ---------------------------------------------------------------------------------------------------- the legs and feet: whole, golden
for p, f, sx in (('legr', 'footr', 1), ('legl', 'footl', -1)):
    x, y, z = PIVOT[p]
    slab(R, p, 11.0, 17.0, 2.8, 'hdown', 2.6, c=(x, z), k=0.66)
    rod(p, [(x, 11.4, z), (x + 0.1 * sx, 7.0, z + 0.4), (x + 0.3 * sx, 2.8, z - 0.6)], [1.9, 1.6, 1.5], 'hleg')
    fx_, fy, fz = PIVOT[f]
    B(f, (fx_ - 1.4, 0.0, fz - 2.4), (fx_ + 1.4, 0.8, fz + 1.6), 'hweb')
    B(f, (fx_ - 2.8, 0.0, fz - 5.0), (fx_ + 2.8, 0.7, fz - 2.3), 'hweb')
    B(f, (fx_ - 3.8, 0.0, fz - 6.4), (fx_ + 3.8, 0.6, fz - 4.9), 'hweb')
    for dx, dz in ((0.0, -8.0), (4.0, -7.0), (-4.0, -7.0)):
        R.seg(f, (fx_, 0.8, fz - 0.6), (fx_ + dx, 0.6, fz + dz), 1.1, 1.0, 'hleg', ext=0.1)
        B(f, (fx_ + dx * 1.06 - 0.45, 0.1, fz + dz - 0.9), (fx_ + dx * 1.06 + 0.45, 0.8, fz + dz + 0.2), 'hnail')

# ---------------------------------------------------------------------------------------------------- fx
# THE HOLY BEAM: a pillar of light called down on a foe (in front of her), rings round it, a sunburst where it lands
bx, by, bz = PIVOT['beam']
R.seg('beam', (bx, 0.2, bz), (bx, 90.0, bz), 6.0, 6.0, 'pillar', light=15, full=True)
R.seg('beam', (bx, 0.2, bz), (bx, 90.0, bz), 11.0, 11.0, 'pillar', light=15, full=True, up=(0.7, 0.0, -0.7))
for k in range(5): ring(R, 'beam', (bx, 2.0 + k * 18.0, bz), 7.0 + (k % 2) * 1.6, 12, 0.8, 0.8, 'ring', light=14)
for k in range(8):
    a = math.radians(k * 45); B('beam', (bx + 8 * math.cos(a) - 0.8, 0.1, bz + 8 * math.sin(a) - 0.8), (bx + 8 * math.cos(a) + 0.8, 0.2, bz + 8 * math.sin(a) + 0.8), 'spark', faces=('up',), full=True, light=15)
R.PART_K['beam'] = 4.0
# THE WING GUST: three arcs of wind out in front, loose feathers tumbling in them
gx, gy, gz = PIVOT['gust']
for i, (r, z) in enumerate(((7.0, gz + 2.0), (10.0, gz - 3.0), (13.0, gz - 8.0))):
    ring(R, 'gust', (gx, gy, z), r, 10, 0.5, 0.35, 'ring', plane='xy', light=10, a0=200, arc=140)
for k in range(9):
    x, y, z = gx + (k - 4) * 2.6, gy + 2.0 + (k % 3) * 2.4, gz - 4.0 - (k % 4) * 2.0
    R.seg('gust', (x, y, z), (x + 1.2, y - 2.2, z - 0.6), 0.9, 0.2, 'feather', up=(0.3, 0.0, -1.0)); R.seg('gust', (x + 1.2, y - 2.2, z - 0.6), (x + 1.5, y - 2.9, z - 0.8), 0.6, 0.2, 'tip', light=10)
# THE CURE: the light's sunburst round her feet (the cure's last beat; also her arrival), rays on the ground
for k in range(16):
    a = math.radians(k * 22.5); L = 20.0 if k % 2 == 0 else 14.0
    R.seg('cure', (math.cos(a) * 6.0, 0.15, math.sin(a) * 6.0), (math.cos(a) * L, 0.15, math.sin(a) * L), 1.2 if k % 2 == 0 else 0.8, 0.1, 'pillar', up=(0, 1, 0), light=15, full=True)
ring(R, 'cure', (0, 0.3, 0), 6.0, 16, 0.9, 0.3, 'halo', light=15)
for k in range(10): sparkle3d('cure', (9 * math.cos(k * 0.63), 3 + (k % 4) * 4, 9 * math.sin(k * 0.63)), 0.8 + (k % 3) * 0.3)
# THE AURA (rare, this form's): a slow wheel of light round her - a gold ring of twelve feathers and sparks
for k in range(12):
    a = math.radians(k * 30); x, z = 20.0 * math.cos(a), 20.0 * math.sin(a); y = 34.0 + 3.0 * math.sin(a * 2)
    R.seg('aura', (x, y, z), (x + 2.4 * math.cos(a + 1.57), y - 2.2, z + 2.4 * math.sin(a + 1.57)), 1.4, 0.2, 'feather', light=12)
    sparkle3d('aura', (x * 0.85, y - 6.0, z * 0.85), 0.7)
ring(R, 'aura', (0, 30.0, 0), 22.0, 24, 0.5, 0.5, 'halo', light=14)

R.PART_K.update({'cure': 1.4, 'aura': 1.5})
for p in ('beam', 'cure', 'aura'):
    R._els[p] = rigkit.shrink(R._els[p], R.PART_K[p])                                   # (fx built at full size, kept inside the model box)


# ---------------------------------------------------------------------------------------------------- skins
def _skin(sfx, P, G, D, Bl, feather_fn):
    t = _tex(P, G, D, Bl)
    swap = {}
    for k in ('hf', 'hf2', 'hdown', 'hneck', 'hprim', 'hgold', 'hlip', 'hbill', 'hbill_d', 'hleg', 'hweb'):
        R.tex(k + sfx, t[k]); swap[k] = k + sfx
    for k in ('feather', 'covert', 'tip', 'tip_blue', 'halo'):
        R.tex(k + sfx, hue(R._tex[k], feather_fn)); swap[k] = k + sfx
    R.skin(sfx, swap)


_skin('_rg', dict(deep='#7a4a44', dark='#d0a49a', base='#f6dcd4', light='#fff0ea', shine='#ffffff', white='#ffffff'),
      dict(deep='#6a2a20', dark='#b06a58', base='#e4a08a', light='#ffcab4', shine='#fff0e8', white='#ffffff'),
      dict(dark='#e0c4bc', base='#f8e6e0', light='#fff6f2', shine='#ffffff'), dict(deep='#6a2a20', dark='#b06a58', base='#e49a84', light='#ffc4ae', hot='#fff0e8'),
      lambda c: (min(255, c[0] * 1.02 + 6), c[1] * 0.86, c[2] * 0.84))
_skin('_pt', dict(deep='#5a606a', dark='#b8c0ca', base='#eef2f6', light='#ffffff', shine='#ffffff', white='#ffffff'),
      dict(deep='#3a4048', dark='#8a929e', base='#c4ccd6', light='#e8eef4', shine='#ffffff', white='#ffffff'),
      dict(dark='#d0d6de', base='#f2f4f8', light='#ffffff', shine='#ffffff'), dict(deep='#3a4048', dark='#8a929e', base='#c4ccd6', light='#e8eef4', hot='#ffffff'),
      lambda c: ((c[0] + c[1] + c[2]) / 3 * 0.98, (c[0] + c[1] + c[2]) / 3 * 1.0, min(255, (c[0] + c[1] + c[2]) / 3 * 1.06)))
_skin('_sh', dict(deep='#2a5a30', dark='#a8dcae', base='#e4f8e4', light='#f6fff4', shine='#ffffff', white='#ffffff'),
      PG, dict(dark='#c4e4c4', base='#eefaec', light='#fbfff8', shine='#ffffff'), BILL,
      lambda c: (c[0] * 0.78, min(255, c[1] * 1.0 + 10), c[2] * 0.8))


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


# the wings: REST (the great pair raised in a gentle V behind her, folded at the wrist; the middle pair folded along her flanks;
# the lower pair round her breast), SPREAD (all six open: glory), BEAT (a downstroke)
REST = dict(wr=limb(1, 0, 34, -46), wr2=qs(('y', -70)), wl=limb(-1, 0, 34, -46), wl2=qs(('y', 70)),
            wmr=limb(1, 0, -24, -70), wml=limb(-1, 0, -24, -70))
SPREAD = dict(wr=limb(1, 0, 18, -8), wr2=qs(('z', 0)), wl=limb(-1, 0, 18, -8), wl2=qs(('z', 0)),
              wmr=limb(1, 0, -6, -10), wml=limb(-1, 0, -6, -10), wlr=limb(1, 0, 10, 24), wll=limb(-1, 0, 10, 24))
BEAT = dict(wr=limb(1, 0, -14, -14), wr2=qs(('z', -16)), wl=limb(-1, 0, -14, -14), wl2=qs(('z', 16)),
            wmr=limb(1, 0, -30, -30), wml=limb(-1, 0, -30, -30))
NECK = dict(neck1=T(-4), neck2=T(4), neck3=T(4), head=T(4))
POSES = R.POSES
POSES.update({
    'idle_a': P(**REST, **NECK),
    # (idle: her head bowed - a moment's prayer, the halo dipping with it)
    'idle_b': P(_face='blink', **REST, neck1=T(6), neck2=T(14), neck3=T(16), head=T(24)),
    # THE GRACEFUL WADDLE (4 frames, 24 ticks): the goose's own walk, gentled - a roll of 5 deg, the neck held up and bending back
    # a little with each step (neck1 back 10 deg, the head kept level), the toes curling as each paddle lifts
    'walk_0': P(**REST, body=T(2, 3, 5), legr=limb(1, -12, -5), legl=limb(-1, 16, -5), footl=limb(-1, -20),
                neck1=T(-10, -3, -3), neck2=T(-2), neck3=T(2), head=T(12)),
    'walk_1': P(**REST, body=T(3), legr=limb(1, 4), legl=limb(-1, 4), neck1=T(-6), neck2=T(2), neck3=T(2), head=T(6)),
    'walk_2': P(**REST, body=T(2, -3, -5), legl=limb(-1, -12, 5), legr=limb(1, 16, 5), footr=limb(1, -20),
                neck1=T(-10, 3, 3), neck2=T(-2), neck3=T(2), head=T(12)),
    'walk_3': P(**REST, body=T(3), legr=limb(1, 4), legl=limb(-1, 4), neck1=T(-6), neck2=T(2), neck3=T(2), head=T(6)),
    # THE RUN (2 frames, 8 ticks): a swan's take-off run - leaning forward, the neck stretched out ahead (no flapping behind: she is
    # all grace now), the great wings beating (spread, then the downstroke), the paddles pattering
    'run_0': P(**SPREAD, body=T(14), legr=limb(1, -30), legl=limb(-1, 34), footl=limb(-1, -30), neck1=T(30), neck2=T(14), neck3=T(4), head=T(-30)),
    'run_1': P(**BEAT, body=T(18), legl=limb(-1, -30), legr=limb(1, 34), footr=limb(1, -30), neck1=T(34), neck2=T(12), neck3=T(4), head=T(-32)),
    # THE HOLY BEAM: her head raised, the great wings lifted, light gathering in the halo (14 ticks) - then the pillar falls on the
    # foe in front of her (the hit, 2 ticks), held 20, fading 10
    'beam_up': P(_face='fierce', **SPREAD, body=T(-6), neck1=T(-14), neck2=T(-10), neck3=T(-8), head=T(-20)),
    'beam': P(_face='fierce', _show=('beam',), **SPREAD, body=T(-2), neck1=T(4), neck2=T(4), neck3=T(2), head=T(10)),
    # THE WING GUST: all six wings drawn back (10 ticks) - and swept forward together (3): a gust that throws foes back
    'gust_up': P(_face='fierce', wr=limb(1, -20, 30, -60), wl=limb(-1, -20, 30, -60), wr2=qs(('y', -30)), wl2=qs(('y', 30)),
                 wmr=limb(1, -20, 0, -60), wml=limb(-1, -20, 0, -60), body=T(-8), **NECK),
    'gust': P(_face='fierce', _show=('gust',), wr=limb(1, 30, 10, 30), wl=limb(-1, 30, 10, 30), wr2=qs(('y', 20)), wl2=qs(('y', -20)),
              wmr=limb(1, 20, -10, 30), wml=limb(-1, 20, -10, 30), body=T(8), neck1=T(10), neck2=T(4), head=T(-6)),
    # THE CURE's last beat (and her arrival in this form): all six open, the sunburst at her feet
    'cure': P(_face='happy', _show=('cure',), **SPREAD, body=T(-6), neck1=T(-8), neck2=T(-4), head=T(-12)),
    'happy': P(_face='happy', **SPREAD, neck1=T(-6), head=T(-10)),
    'hurt': P(_face='sad', **REST, body=T(-10, 0, 6), neck1=T(-14, 0, -10), neck2=T(-6), head=T(-8)),
    # SITTING (right-click): settled as a swan sits on still water - the feet tucked, the wings folded, the neck in its S
    'sit_a': P(_face='happy', **REST, _hide=('legr', 'legl', 'footr', 'footl'), body=T(-4), neck1=T(-4), neck2=T(6), neck3=T(6), head=T(4)),
    # SNEAK + RIGHT-CLICK: asleep - the neck laid back along her back, her head under the great wing, the halo low
    'sit_b': P(_face='blink', wr=limb(1, 0, 14, -60), wl=limb(-1, 0, 14, -60), wr2=qs(('y', -100)), wl2=qs(('y', 100)), wmr=limb(1, 0, -24, -70), wml=limb(-1, 0, -24, -70),
               _hide=('legr', 'legl', 'footr', 'footl'), neck1=T(-40), neck2=T(-56), neck3=T(-40), head=T(-30, 0, 18)),
    'aura': P(_face='happy', _show=('aura',), **REST, **NECK),
    'doll': P(**dict(REST, wmr=limb(1, 0, -30, -80), wml=limb(-1, 0, -30, -80)), **NECK),
})
DRAFT = list(POSES)
R.DRAFT = DRAFT
DOLL_GROUPS = {'head': 'head', 'jaw': 'head', 'halo': 'head', 'neck3': 'body', 'neck2': 'body', 'neck1': 'body', 'body': 'body', 'tail': 'body',
               'wr': 'body', 'wl': 'body', 'wr2': 'body', 'wl2': 'body', 'wmr': 'body', 'wml': 'body', 'wlr': 'body', 'wll': 'body',
               'legr': 'legs', 'legl': 'legs', 'footr': 'legs', 'footl': 'legs'}

# HER MOVES in this form (ticks; for the wiring stage)
ATTACKS = {
    'beam': dict(poses=('beam_up', 'beam'), windup=14, hit=15, hold=20, recover=10, dmg=8, undead=14, cd=8,
                 fx='a pillar of light called down on the foe (r 1.5 blocks): 8, 14 to the undead and the Dread; it lights them up (Glowing, on the MOB)'),
    'gust': dict(poses=('gust_up', 'gust'), windup=10, hit=11, hold=3, recover=8, dmg=3, push=2.2, cone=70, cd=10,
                 fx='all six wings swept forward: every foe in a 70-deg cone 6 blocks deep thrown back 2.2 and slowed; projectiles in it knocked aside'),
    'bless': dict(poses=('cure',), windup=12, hold=20, cd=60, fx='out of a fight, every minute: the sunburst at her feet - Regeneration II 5 s for you and every follower within 8'),
}
