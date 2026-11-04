"""(3.1 draft, stage 1: art only - not wired) THE GILDED ELDRITCH - the Golden Doodle's second phase, and its second form as a
follower (goldendoodle_pet_art.py is the goose; the design: scratchpad/design_goldendoodle.md).

The owner: "in the second phase, a piece of the dread sovereign accidentally attaches to it and it morphes into the gilded
eldritch. As a follower, you can switch it between both forms."

THE STORY IN THE ART  A shard of the Dread Sovereign's crown (the Bound Sovereign's - it was standing right there) lodges in the
       goose's head. Everything here grows from that point: the crown on its head is the shard, grown; red cracks of the Dread's
       light run out of it - densest on the head and the neck (void-dark, the gold nearly gone), thinning over the body, and the
       tail plumes are still nearly all gold. It is still the goose: the S of the neck, the beak, the paunch, the webbed feet,
       the folded-wing shoulders. Only all of it is WRONG.
LOOK   ~2.9 blocks to the crown as a follower (RIG_SCALE 0.9, its own size; the Rat King's companion rules apply - see the doc) and
       ~5.2 blocks as the boss (BOSS_SCALE 1.6): a player comes up to its breast.
         - THE BODY: the goose's egg grown huge and REARING (the breast high, the way a swan threatens), gold feathers cracked with
           void seams and red light; Dread void-plate grafted over its shoulders and back (the Sovereign's own plate texture,
           ds_plate, red-seamed); a ridge of void-glass spines down its back, tallest at the shoulders; on each flank the
           feathers have fallen away from a RIB CAGE of gilded bone over a dark cavity with an ember in it.
         - THE NECK: three times as long, in three parts, a void-dark core ringed by gilded vertebrae (every ~2.5 units) with
           dorsal spikes; small red eyes open along its sides. Two thirds of the way up IT SPLITS: a second, smaller neck
           branches off to its left, ending in a head with no beak at all - a four-petal mandible lined with teeth, a cluster
           of red eyes where a face should be.
         - THE HEAD: the goose's long head, its beak grown long and hooked, the goose's serrated tomia now FANGS along both
           bills; its beady eyes gone red and slit (the Dread's eye), and TOO MANY: three more down each side and a vertical
           third eye in the brow under the crown. THE CROWN: the Sovereign's spikes (ds_horn, red-hot tips) round a heart-crystal
           (ds_heart) set where the emerald used to be.
         - THE WINGS: GILDED BONE - a gold humerus and forearm, four long finger bones, and between them tattered Dread
           membrane (black, veined red, holes torn in it) with eyes in it, like the Sovereign's wings; a few gold blade-feathers
           still hanging from the forearm (the rest fell off).
         - THE LEGS AND FEET: thick thighs, tall scaled shanks, and the goose's paddles grown into claws: three long toes ending
           in black void-glass talons, the webbing between them torn.
         - THE TAIL: long ragged plumes, still mostly gold, a few blackened, drooping.
RIG    body (root) - tail - neck1 - neck2 - neck3 - head (face part) - jaw - neckb - headb (the second head) - wr / wl (arm) -
       wr2 / wl2 (hand) - legr / legl - footr / footl; fx: 'beam' (the brow-eye's DREAD BEAM), 'shriek' (the honk, gone wrong:
       jagged red rings), 'eggs' (dread eggs: black, red-cracked, one hatched into grasping void hands), 'curse' (THE UNLUCKY:
       an inverted Lucky sigil on the ground - a black four-leaf clover in a ring of broken coins), 'shard' (the defeat: the shard
       tumbling out of its head), 'aura' (the rare aura of this form: a halo of watching eyes and gold motes).
SKINS  '_rg' ROSE GOLD and '_pt' PLATINUM (each the goose's cosmetic, carried into this form), '_sh' SHINY FOUR-LEAF (emerald,
       its cracks glowing green instead of red - the shiny keeps its luck).
"""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import Rig, hexc, mix, limb, T, cells, soft, lit, glow, put, slab, stack, profile, ring, leaf, cleaf, _ell, hue, recolor
import rigkit
import goldendoodle_pet_art as GQ
import dread_sovereign_art as DSA

PIVOT = {'body': (0, 21.0, 3.0), 'tail': (0, 20.0, 15.0), 'neck1': (0, 27.0, -6.5), 'neck2': (0, 34.0, -10.5), 'neck3': (0, 41.0, -12.0),
         'head': (0, 46.5, -13.0), 'jaw': (0, 47.0, -18.5), 'neckb': (-1.6, 38.5, -11.6), 'headb': (-7.4, 44.6, -15.2),
         'wr': (8.0, 28.0, -1.0), 'wl': (-8.0, 28.0, -1.0), 'wr2': (27.0, 36.0, 3.0), 'wl2': (-27.0, 36.0, 3.0),
         'legr': (5.6, 15.0, 3.0), 'legl': (-5.6, 15.0, 3.0), 'footr': (6.2, 2.6, 1.6), 'footl': (-6.2, 2.6, 1.6),
         'beam': (0, 51.0, -20.0), 'shriek': (0, 47.0, -26.0), 'eggs': (0, 0, 0), 'curse': (0, 0, 0), 'shard': (0, 52.0, -17.0), 'aura': (0, 30.0, 0)}
PARENT = {'body': None, 'tail': 'body', 'neck1': 'body', 'neck2': 'neck1', 'neck3': 'neck2', 'head': 'neck3', 'jaw': 'head',
          'neckb': 'neck2', 'headb': 'neckb', 'wr': 'body', 'wl': 'body', 'wr2': 'wr', 'wl2': 'wl', 'legr': 'body', 'legl': 'body',
          'footr': 'legr', 'footl': 'legl', 'beam': 'head', 'shriek': 'head', 'eggs': None, 'curse': None, 'shard': 'head', 'aura': None}
FACES = ('narrowed', 'wide', 'blink', 'hurt', 'dim')
OPT = ('beam', 'shriek', 'eggs', 'curse', 'shard', 'aura')
R = Rig('gk_', 0.9, PIVOT, PARENT, FACES, face_part='head', opt=OPT, companion=0.55)
COMPANION = 0.55                 # (its menu's Companion Size: ~1.95 blocks - compsize twins the rig at COMPANION / RIG_SCALE, as the Rat King's)
BOSS_SCALE = 1.6
SKIN_NAMES = {'_rg': 'cosmetic: Rose Gold', '_pt': 'cosmetic: Platinum', '_sh': 'SHINY: Four-Leaf'}

# ---------------------------------------------------------------------------------------------------- palette and textures
VOID, VOID2, VEIN = '#120a14', '#22142a', '#3a1a2a'
RED, RED_L, RED_D = '#d0182e', '#ff5a64', '#76101e'
DG = dict(deep='#3a2404', dark='#6e4a0c', base='#a87a18', light='#d8a836', shine='#ffe890', white='#fff8e0')     # (dimmed gold)
BONE = dict(deep='#4a3410', dark='#9a7a3a', base='#d8bc78', light='#f2dea8', shine='#fff6d8')
_DS = DSA.textures()


def crack(im, rnd, n, col=RED, hot=RED_L, dark=VOID, wide=False):
    """a crack of the Dread's light through the gold, in 2-px cells: a void-dark lip, a red core, a hot fleck now and then; it
    wanders down and branches (wide: a two-cell void seam either side - the heavy cracks of the head and neck)"""
    d = ImageDraw.Draw(im)
    sq = lambda x, y, c: d.rectangle((x % 64, y % 64, x % 64 + 1, y % 64 + 1), fill=hexc(c))
    for _ in range(n):
        x, y = rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2)
        for i in range(rnd.randint(6, 14)):
            sq(x - 2, y, dark); sq(x + 2, y, dark) if wide else None
            if wide: sq(x - 4, y, VOID2)
            sq(x, y, hot if (i == 0 or rnd.random() < 0.15) else col)
            if rnd.random() < 0.16:
                bx, by = x, y
                for _k in range(rnd.randint(2, 4)):
                    bx += rnd.choice((-2, 2)); by += 2; sq(bx, by, col); sq(bx - 2, by, dark)
            x += rnd.choice((-2, 0, 0, 2)); y += 2
    return im


def cracked(P, seed, n, wide=False, w=4, darken=0.0):
    im = GQ.feathers(P, seed, w=w, sparks=0)
    if darken:
        px = im.load()
        for y in range(64):
            for x in range(64):
                r, g, b, a = px[x, y]
                px[x, y] = (int(r * (1 - darken) + 18 * darken), int(g * (1 - darken) + 10 * darken), int(b * (1 - darken) + 22 * darken), a)
    return crack(im, random.Random(seed), n, wide=wide)


def flesh(seed):
    """the neck's void-dark core: deep violet-black, veined red, a faint wet sheen in rows"""
    rnd = random.Random(seed)
    im = soft(VOID, VOID2, '#08040a', seed, p=0.2)
    d = ImageDraw.Draw(im)
    for y in range(0, 64, 10): d.rectangle((0, y, 63, y + 1), fill=hexc(VOID2))
    return crack(im, rnd, 5, RED_D, RED, '#050206')


def bone(P, seed):
    """gilded bone: ivory-gold, ridged along its length, a lit edge, a crack or two of red"""
    def c(x, y, r):
        k = x % 6
        if k == 0: return P['dark']
        if k == 1: return P['light']
        if k == 2 and y % 9 == 0: return P['shine']
        if y % 13 == 12: return mix(P['base'], P['dark'], 0.4)
        return P['base']
    return crack(cells(c, seed), random.Random(seed), 2)


def membrane(seed):
    """tattered Dread membrane: the Sovereign's (black, folded, red-veined) with holes torn in it near its edges (see-through)"""
    im = _DS['ds_membrane'].copy(); rnd = random.Random(seed); px = im.load()
    holes = [(rnd.randrange(64), rnd.randrange(40, 64), rnd.uniform(2, 6)) for _ in range(7)] + [(rnd.randrange(64), rnd.randrange(64), rnd.uniform(1.5, 3.5)) for _ in range(4)]
    for y in range(64):
        for x in range(64):
            for hx, hy, hr in holes:
                dd = math.hypot(x - hx, y - hy)
                if dd < hr: px[x, y] = (0, 0, 0, 0); break
                if dd < hr + 1.6: px[x, y] = hexc('#3a0a14')
    return im


def slit_eye(kind=None, size=16, iris=RED):
    """a Dread eye (whole uv), the Sovereign's: a pale almond, a red iris with a slit; narrowed: lids over it; blink / dim"""
    im = Image.new('RGBA', (size, size), hexc('#140a16')); d = ImageDraw.Draw(im)
    if kind in ('blink', 'dim'):
        d.rectangle((2, 7, 13, 8), fill=hexc(RED_D if kind == 'blink' else '#4a0c18'))
        if kind == 'blink': d.rectangle((4, 7, 11, 7), fill=hexc(RED))
        return im.resize((64, 64), Image.NEAREST)
    top, bot = (5, 11) if kind == 'narrowed' else (2, 14) if kind == 'wide' else (3, 13)
    d.polygon([(1, 8), (5, top), (11, top), (15, 8), (11, bot), (5, bot)], fill=hexc('#f0e2cc'))
    r = 4 if kind != 'wide' else 3
    d.ellipse((8 - r, 8 - r, 8 + r - 1, 8 + r - 1), fill=hexc(iris if kind != 'hurt' else '#ff9a5a'))
    d.rectangle((7, 8 - r + 1, 8, 8 + r - 2), fill=hexc('#0a0204'))
    d.rectangle((5, 5, 5, 5), fill=hexc('#ffc8b8'))
    if kind == 'narrowed':
        d.rectangle((0, 0, 15, top), fill=hexc('#140a16')); d.rectangle((0, bot, 15, 15), fill=hexc('#140a16'))
    return im.resize((64, 64), Image.NEAREST)


def eyes_sheet(kind=None):
    """its EYES overlay: the face part's eyes, one window per eye group (u 0-3: the main pair's big eye; u 3-6: the small ones;
    u 6-9: the brow's vertical third eye) - each a slit eye, all closing / narrowing / widening together"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    big = slit_eye(kind).resize((12, 12), Image.NEAREST)
    small = slit_eye(kind).resize((8, 8), Image.NEAREST)
    im.paste(big, (0, 0)); im.paste(small, (12, 0)); im.paste(small.rotate(90), (24, 0))
    return im


def _tex(P=DG, B_=BONE, emer=GQ.EMER, red=(RED, RED_L, RED_D), suffix=''):
    t = {'gcr': cracked(P, 31, 5, wide=True, darken=0.45), 'gcr2': cracked(P, 32, 3, darken=0.15), 'gcr3': cracked(P, 33, 1, w=5),
         'prim': GQ.primaries(P, 34), 'down': GQ.down(GQ.CREAM if not suffix else {'dark': B_['dark'], 'base': B_['base'], 'light': B_['light'], 'shine': B_['shine']}, 35),
         'flesh': flesh(36), 'bone': bone(B_, 37), 'memb': membrane(38),
         'plate': _DS['ds_plate_b'], 'edge': _DS['ds_edge'], 'glass': _DS['ds_glass'], 'horn': _DS['ds_horn'], 'horn_r': _DS['ds_horn_r'],
         'red': _DS['ds_red'], 'red_l': _DS['ds_red_l'], 'red_d': _DS['ds_red_d'], 'heart': _DS['ds_heart'], 'void': _DS['ds_void'],
         'smoke': _DS['ds_smoke'], 'eye': slit_eye(), 'eye_s': slit_eye('narrowed'), 'tooth': cells(lambda x, y, r: '#f4ead8' if y > 6 else '#ffffff', 0),
         'beak': GQ.orange(dict(deep='#2a0a04', dark='#5a1a08', base='#9a3a10', light='#d06a20', hot='#ffa040'), 39),
         'talon': cells(lambda x, y, r: '#140a1a' if x < 20 else '#3a2a4a', 0), 'scute': GQ.orange(dict(deep='#2a1a08', dark='#4a3010', base='#7a5420', light='#a87a3a', hot='#d8a860'), 40, scutes=True),
         'mouth': cells(lambda x, y, r: '#3a0610' if y % 6 else '#5a0a18', 0),
         'beamc': glow(['#ffffff', '#ffb0a0', '#ff4a50', '#c0102a'], alpha=[255, 240, 200, 120]),
         'ring': GQ.ring_tex('#ff4a5a', 200), 'egg': crack(lit(cells(lambda x, y, r: VOID2 if (x + y) % 11 else '#3a2a44', 41), 1.4, 0.8, 10), random.Random(42), 6),
         'sigil': _sigil(), 'coin': GQ.coin_tex(), 'aura': glow(['#ffffff', '#ffd040', '#d0182e', '#40081a'], alpha=[230, 200, 140, 0]),
         'spark': GQ.spark_tex(), 'eyes': eyes_sheet()}
    for f in FACES: t[f'eyes_{f}'] = eyes_sheet(f)
    return t


def _sigil():
    """THE UNLUCKY: the Lucky Night's clover inverted - a black four-leaf clover, red-rimmed, in a ring of broken coins (full uv,
    see-through, on the ground)"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 61, 61), outline=hexc(RED), width=2); d.ellipse((7, 7, 56, 56), outline=hexc(RED_D), width=1)
    for i in range(12):
        a = math.radians(i * 30); x, y = 32 + 27 * math.cos(a), 32 + 27 * math.sin(a)
        if i % 3: d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=hexc('#a87a18')); d.line((x - 3, y + 2, x + 3, y - 2), fill=hexc(VOID), width=1)
    for ang in (45, 135, 225, 315):
        a = math.radians(ang); cx, cy = 32 + 9 * math.cos(a), 32 + 9 * math.sin(a)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=hexc(RED)); d.ellipse((cx - 7, cy - 7, cx + 7, cy + 7), fill=hexc('#0a0406'))
    d.line((32, 36, 26, 52), fill=hexc(RED), width=2)
    return im


TEX = _tex()
for k, v in TEX.items(): R.tex(k, v)


# ---------------------------------------------------------------------------------------------------- helpers (on this rig)
B = R.box


def zslab(part, z0, z1, hw, hh, tex, c=(0.0, 0.0), k=0.7, light=0):
    x, y = c
    return [B(part, (x - hw, y - hh * k, z0), (x + hw, y + hh * k, z1), tex, light=light),
            B(part, (x - hw * k, y + hh * k, z0), (x + hw * k, y + hh, z1), tex, light=light),
            B(part, (x - hw * k, y - hh, z0), (x + hw * k, y - hh * k, z1), tex, light=light)]


def zegg(part, z0, z1, r, tex, yc, n=9, sq=0.84, blunt=1.35, power=1.2, under=None, top=None):
    out = []
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n; t = (t0 + t1) / 2
        u = (t - 0.36) / (0.64 if t > 0.36 else 0.36)
        w = max(0.6, r * max(0.0, 1 - abs(u) ** (blunt if u < 0 else 1.6)) ** (0.5 / power))
        es = zslab(part, z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1, w, w * sq, tex(t) if callable(tex) else tex, c=(0.0, yc(t)), k=0.7)
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


def spike(part, base, tip, w, tex='horn', tip_tex='horn_r', light=0):
    """a tapered spike from base to tip: three spans narrowing, the last one red-hot"""
    P = lambda s: tuple(base[i] + (tip[i] - base[i]) * s for i in range(3))
    up = (0.0, 0.0, -1.0) if abs(tip[1] - base[1]) > abs(tip[2] - base[2]) else (0.0, 1.0, 0.0)
    R.seg(part, P(0.0), P(0.45), w, w, tex, up, ext=0.1)
    R.seg(part, P(0.42), P(0.8), w * 0.6, w * 0.6, tex, up, ext=0.05)
    R.seg(part, P(0.78), P(1.0), w * 0.3, w * 0.3, tip_tex, up, light=light or 10)


def eye_plate(part, c, s, facing, kind='eye', light=12, window=None):
    """a small eye set in the surface (whole uv, or a window of the EYES sheet): facing 'east'/'west'/'north'"""
    x, y, z = c; h = s / 2
    if facing in ('east', 'west'):
        fr, to = (x, y - h, z - h), (x + (0.02 if facing == 'east' else -0.02), y + h, z + h)
    else:
        fr, to = (x - h, y - h, z), (x + h, y + h, z + 0.02)
    fr, to = tuple(min(a, b) for a, b in zip(fr, to)), tuple(max(a, b) for a, b in zip(fr, to))
    return B(part, fr, to, kind, faces=(facing,), uv={facing: window or [0, 0, 16, 16]}, light=light)


def panel(part, O, P1, P2, tex, n=3, t=0.3, light=0):
    """a membrane triangle O-P1-P2: n thin boxes from O out toward the edge P1-P2, each as wide as the triangle is there"""
    M = tuple((P1[i] + P2[i]) / 2 for i in range(3))
    e1 = [P1[i] - O[i] for i in range(3)]; e2 = [P2[i] - O[i] for i in range(3)]
    nrm = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
    L = math.sqrt(sum(v * v for v in nrm)) or 1.0; nrm = tuple(v / L for v in nrm)
    W = math.dist(P1, P2)
    out = []
    for i in range(n):
        a, b = i / n, (i + 1) / n
        A_ = tuple(O[k] + (M[k] - O[k]) * a for k in range(3)); B_ = tuple(O[k] + (M[k] - O[k]) * b for k in range(3))
        out.append(R.seg(part, A_, B_, max(0.4, W * (a + b) / 2 * 0.98), t, tex, nrm, ext=0.0, light=light, full=True))
    return out


# ---------------------------------------------------------------------------------------------------- the body: rearing, cracked
def btex(t):
    return 'gcr' if t < 0.22 else 'gcr2' if t < 0.62 else 'gcr3'


zegg('body', -11.0, 15.4, 9.6, btex, lambda t: 23.4 - 6.0 * t, n=11, sq=0.8, under='down')     # (rearing: the breast high)
zegg('body', -12.0, -2.0, 7.0, 'gcr', lambda t: 22.4 - 1.0 * t, n=5, sq=0.86, blunt=0.9, power=1.0)     # (the breast)
zegg('body', 0.0, 13.0, 6.2, 'down', lambda t: 14.2 - 0.8 * t, n=5, sq=0.62)                             # (the paunch, gone gaunt)
# the breast's rift: a red crack down its front, glowing
for i, (y0, y1, x) in enumerate(((26.5, 28.5, 0.3), (24.5, 26.6, -0.4), (22.4, 24.6, 0.4), (20.6, 22.5, -0.2))):
    B('body', (x - 0.45, y0, -12.05), (x + 0.45, y1, -11.9), 'red_l', light=13)
    B('body', (x - 0.9, y0, -12.0), (x + 0.9, y1, -11.85), 'red_d', light=8)
# Dread void-plate grafted over its shoulders and back (each a tilted plate with a lit edge, red-seamed)
for sx in (1, -1):
    for (x, y, z, w, d, a) in ((5.6, 30.2, -3.0, 6.0, 7.0, 24), (4.0, 29.6, 4.6, 5.2, 6.0, 14)):
        R.box('body', (sx * x - w / 2, y - 0.6, z - d / 2), (sx * x + w / 2, y + 0.6, z + d / 2), 'plate', rot=('z', -a * sx, (sx * x, y, z)))
        R.box('body', (sx * x - w / 2, y + 0.55, z - d / 2 - 0.2), (sx * x + w / 2, y + 0.85, z - d / 2 + 0.6), 'edge', rot=('z', -a * sx, (sx * x, y, z)))
# the spines: void-glass, down the back, tallest at the shoulders
for i, (z, h) in enumerate(((-6.0, 6.5), (-2.6, 8.0), (1.0, 7.0), (4.4, 5.6), (7.6, 4.2), (10.6, 3.0))):
    y = 31.0 - i * 1.1
    spike('body', (0, y - 1.0, z), (0, y + h, z + 1.8 + i * 0.3), 1.8 - i * 0.15, 'glass', 'red_l')
# the flank's rib cage: the feathers fallen away from gilded bone, a dark cavity behind, an ember inside it
for sx in (1, -1):
    X = sx * 9.0
    X0, X1 = (X - 0.7, X + 0.3) if sx > 0 else (X - 0.3, X + 0.7)
    B('body', (X0, 17.0, -1.6), (X1, 22.0, 4.4), 'smoke')
    B('body', (X0 - 0.05 * sx, 18.4, 0.2), (X1 - 0.05 * sx, 20.4, 2.6), 'red_d', light=8)
    for k in range(3):
        z = -0.9 + k * 2.2
        R.seg('body', (X + 0.1 * sx, 22.8, z), (X + 0.9 * sx, 19.6, z + 0.5), 0.75, 0.75, 'bone', up=(float(sx), 0, 0))
        R.seg('body', (X + 0.9 * sx, 19.6, z + 0.5), (X + 0.3 * sx, 16.6, z + 1.0), 0.65, 0.65, 'bone', up=(float(sx), 0, 0))

# ---- the tail: long ragged plumes, still mostly gold, a few blackened, drooping
for i, (sx, L, dy) in enumerate(((0, 15.0, -4.0), (0.55, 13.0, -2.6), (-0.55, 13.4, -3.0), (1.0, 10.6, -1.0), (-1.0, 11.0, -1.6))):
    x0, y0, z0 = sx * 2.2, 21.0, 13.6
    tex = 'prim' if i not in (2, 4) else 'gcr'
    cleaf(R, 'tail', (x0, y0, z0), (sx * 0.35, 0.18, 1.0), L, 2.6 - abs(sx) * 0.4, tex, droop=0.16 - dy * 0.0, t=0.5, n=4, full=False)
R.seg('tail', (0, 21.0, 12.0), (0, 21.6, 16.4), 5.4, 3.4, 'gcr3', ext=0.3)

# ---------------------------------------------------------------------------------------------------- the neck: long, split
def neck(part, pts, ws, rings=True):
    rod(part, pts, ws, 'flesh')
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    for i in range(len(pts) - 1):                     # (gilded vertebrae, every ~2.5 units, a dorsal spike on each)
        n = max(1, int(L[i] / 2.5))
        for k in range(n):
            s = (k + 0.5) / n; c = tuple(pts[i][j] + (pts[i + 1][j] - pts[i][j]) * s for j in range(3))
            w = ws[i] + (ws[i + 1] - ws[i]) * s
            a = tuple(pts[i][j] + (pts[i + 1][j] - pts[i][j]) * (s - 0.08) for j in range(3))
            b = tuple(pts[i][j] + (pts[i + 1][j] - pts[i][j]) * (s + 0.08) for j in range(3))
            if rings:
                R.seg(part, a, b, w * 1.16, w * 1.16, 'gcr2', (0.0, 0.0, -1.0), ext=0.05)
                R.seg(part, a, b, w * 1.04, w * 1.04, 'gcr2', (0.7, 0.0, -0.7), ext=0.0)
            back = (c[0], c[1] + 0.2, c[2] + w * 0.55)
            spike(part, back, (c[0], c[1] + 1.4, c[2] + w * 0.55 + 2.4), 0.8, 'glass', 'red_l')


N1 = [(0, 25.6, -7.4), (0, 29.4, -10.6), (0, 33.2, -11.8), (0, 34.6, -11.6)]
N2 = [(0, 34.2, -11.6), (0, 37.6, -11.2), (0, 40.8, -11.4), (0, 41.6, -11.8)]
N3 = [(0, 41.2, -11.8), (0, 44.0, -12.6), (0, 46.6, -13.4)]
zslab('neck1', -12.0, -4.0, 5.2, 4.0, 'gcr', c=(0, 26.0), k=0.66)                   # (the neck's root, flaring into the breast)
neck('neck1', N1, [5.2, 4.2, 3.7, 3.6])
neck('neck2', N2, [3.6, 3.3, 3.2, 3.1])
neck('neck3', N3, [3.1, 3.0, 3.1])
for part, pts, sx in (('neck1', N1, 1), ('neck2', N2, -1), ('neck2', N2, 1), ('neck1', N1, -1)):     # (red eyes opening along its sides)
    for k, s in enumerate((0.3, 0.62)):
        i = 1 if part == 'neck1' else 0
        c = tuple(pts[i][j] + (pts[i + 1][j] - pts[i][j]) * s for j in range(3))
        w = 2.0 if part == 'neck1' else 1.75
        eye_plate(part, (c[0] + sx * w, c[1], c[2] - 0.2), 1.0 + 0.2 * k, 'east' if sx > 0 else 'west', 'eye')
# THE SPLIT: a second neck branching to its left, ending in a head with no beak - a four-petal mandible, a cluster of eyes
NB = [(-1.6, 38.5, -11.6), (-4.4, 41.0, -13.2), (-6.6, 43.4, -14.6), (-7.4, 44.6, -15.2)]
neck('neckb', NB, [3.0, 2.7, 2.6, 2.6])
hx, hy, hz = PIVOT['headb']
zegg('headb', hz - 5.2, hz + 1.6, 3.3, lambda t: 'gcr' if t < 0.6 else 'flesh', lambda t: hy + 0.6, n=5, sq=0.95, blunt=1.0)
for k, (dx, dy) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):                         # (the four petals, splayed open, toothed)
    base = (hx + dx * 1.1, hy + 0.6 + dy * 1.1, hz - 4.8)
    mid = (hx + dx * 3.0, hy + 0.6 + dy * 2.8, hz - 7.4)
    tip = (hx + dx * 3.0, hy + 0.6 + dy * 2.6, hz - 10.0)                           # (each petal curls back in at its tip: a hooked mandible)
    for A_, B2, w in ((base, mid, 2.2), (mid, tip, 1.4)):
        R.seg('headb', A_, B2, w, 0.7, 'gcr', up=(dx * 0.7, dy * 0.7, 0.3), ext=0.12)
    R.seg('headb', tip, (tip[0] - dx * 0.8, tip[1] - dy * 0.8, tip[2] - 1.2), 0.6, 0.6, 'horn_r', light=8)
    for j in range(4):
        s = 0.15 + j * 0.22; c = tuple(base[i] + (mid[i] - base[i]) * s * 1.6 for i in range(3)) if j < 3 else tuple(mid[i] + (tip[i] - mid[i]) * 0.5 for i in range(3))
        R.seg('headb', c, (c[0] - dx * 0.75, c[1] - dy * 0.75, c[2] - 0.2), 0.3, 0.3, 'tooth')
B('headb', (hx - 1.6, hy - 1.0, hz - 5.35), (hx + 1.6, hy + 2.2, hz - 5.15), 'mouth', light=3)
for (dx, dy, s) in ((0, 1.6, 1.0), (-1.3, 2.4, 0.7), (1.2, 2.5, 0.75), (-2.0, 1.2, 0.6), (2.0, 0.9, 0.6), (0.2, 3.1, 0.55)):     # (eyes where its face should be)
    eye_plate('headb', (hx + dx * 0.75, hy + 0.6 + dy * 0.9, hz - 5.45), s * 1.2, 'north', 'eye')

# ---------------------------------------------------------------------------------------------------- the head: the goose's, wrong
HX, HY, HZ = 0.0, 47.2, -14.6
zegg('head', -20.2, -10.8, 3.9, lambda t: 'gcr' if t < 0.7 else 'flesh', lambda t: HY + 0.4 * t, n=6, sq=0.86, blunt=1.0, power=1.1)
for sx in (1, -1):                                                                     # (gaunt cheekbones of gilded bone)
    R.seg('head', (sx * 3.4, 45.8, -18.8), (sx * 3.6, 46.4, -12.2), 0.9, 1.0, 'bone', up=(float(sx), 0.3, 0))
R.seg('head', (0, 51.0, -15.0), (0, 50.0, -19.4), 4.2, 1.2, 'gcr')                  # (the brow, heavy)
# the beak: long and hooked, black-red, the tomia grown into FANGS along it; its nail a void-glass hook
R.seg('head', (0, 47.6, -19.6), (0, 47.0, -24.0), 3.6, 2.0, 'beak', ext=0.1)
R.seg('head', (0, 46.9, -23.9), (0, 46.2, -27.4), 2.6, 1.5, 'beak', ext=0.05)
R.seg('head', (0, 46.2, -27.2), (0, 44.6, -28.6), 1.4, 1.2, 'glass')                # (the hooked nail)
for i in range(8):                                                                     # (fangs down both sides of the upper bill)
    z = -20.2 - i * 0.9
    for sx in (1, -1):
        L = 1.4 - abs(i - 3) * 0.12
        R.seg('head', (sx * (1.35 - i * 0.06), 46.2, z), (sx * (1.25 - i * 0.06), 46.2 - L, z - 0.2), 0.36, 0.36, 'tooth')
B('head', (-1.4, 46.0, -26.0), (1.4, 46.3, -19.8), 'mouth')
# the eyes: the goose's own pair, now the Dread's slit eyes, big; three more down each side; a third eye, upright, in the brow
for sx in (1, -1):
    x = sx * 3.85
    eye_plate('head', (x, 48.3, -17.4), 3.4, 'east' if sx > 0 else 'west', 'EYES', light=15, window=[0, 0, 3, 3] if sx > 0 else [3, 0, 0, 3])
    for k, (dy, dz) in enumerate(((-1.4, -14.6), (0.6, -13.4), (-0.8, -12.2))):
        eye_plate('head', (x * (0.98 - k * 0.04), 48.0 + dy, dz), 1.6 - k * 0.2, 'east' if sx > 0 else 'west', 'EYES', light=14,
                  window=[3, 0, 5, 2] if sx > 0 else [5, 0, 3, 2])
eye_plate('head', (0, 49.4, -20.25), 1.8, 'north', 'EYES', light=15, window=[6, 0, 8, 2])
B('head', (-0.6, 48.2, -20.3), (0.6, 50.6, -20.24), 'EYES', faces=('north',), uv={'north': [6, 0, 8, 2]}, light=15)
# THE CROWN: the Sovereign's shard, grown - black spikes, red-hot tips, tallest at the front, a heart-crystal where the emerald was
crown = [(0, -18.4, 7.0), (-1.8, -18.0, 4.8), (1.8, -18.0, 4.8), (-3.0, -16.4, 3.8), (3.0, -16.4, 3.8), (-2.6, -13.8, 3.0), (2.6, -13.8, 3.0), (0, -12.6, 2.6)]
for x, z, h in crown:
    spike('head', (x, 50.4, z), (x * 1.35, 50.4 + h, z - (0.6 if z < -16 else -0.5)), 1.3)
R.box('head', (-1.2, 51.0, -20.6), (1.2, 53.4, -18.2), 'heart', rot=((35.26, 45.0, 0.0), (0, 52.2, -19.4)), light=15)
for sx in (1, -1):                                                                     # (the cracks it spreads, glowing)
    for k in range(3):
        R.seg('head', (sx * 0.8, 51.0, -18.6 + k * 1.6), (sx * (3.2 + k * 0.3), 47.6 - k * 0.8, -17.0 + k * 2.0), 0.35, 0.25, 'red_l', light=12, up=(0, 0, -1))

# ---- the jaw: the lower bill, fanged
R.seg('jaw', (0, 46.0, -19.4), (0, 45.4, -23.6), 3.0, 1.2, 'beak', ext=0.1)
R.seg('jaw', (0, 45.4, -23.5), (0, 45.0, -26.6), 2.0, 1.0, 'beak')
B('jaw', (-1.1, 46.4, -25.6), (1.1, 46.6, -19.8), 'mouth')
for i in range(6):
    z = -20.4 - i * 0.95
    for sx in (1, -1): R.seg('jaw', (sx * 1.0, 46.4, z), (sx * 0.95, 47.6 - abs(i - 2) * 0.1, z - 0.15), 0.32, 0.32, 'tooth')

# ---------------------------------------------------------------------------------------------------- the wings: gilded bone
for a, h, sx in (('wr', 'wr2', 1), ('wl', 'wl2', -1)):
    S = lambda v: (sx * v[0], v[1], v[2])
    SH, EL, WR = S((8.0, 28.0, -1.0)), S((18.0, 33.4, 1.0)), S((27.0, 36.0, 3.0))
    rod(a, [SH, EL], [3.0, 2.4], 'bone'); rod(a, [EL, WR], [2.4, 1.9], 'bone')
    for c in (EL, WR): stack(R, a, [(c[1] - 1.5, c[1] + 1.5, 1.6)], 'bone', c=(c[0], c[2]), k=0.62)     # (knuckles)
    panel(a, SH, WR, S((11.0, 17.0, 7.0)), 'memb', n=3, t=0.25)                        # (the inner membrane, down to its flank)
    for k, (z0, L) in enumerate(((0.0, 9.0), (2.6, 11.0), (5.2, 8.0))):                 # (the last gold blade-feathers hanging off it)
        base = S((14.0 + k * 4.4, 32.0 + k * 1.2, 1.6 + k * 0.6))
        leaf(R, a, base, (base[0] + sx * 1.6, base[1] - L, base[2] + 2.6), 2.2, 'prim', up=(0.0, 0.0, -1.0), t=0.4)
    FT = [S((44.0, 44.0, 6.0)), S((45.0, 34.0, 9.0)), S((40.0, 22.0, 11.0)), S((31.0, 15.0, 10.0))]
    for i, tip in enumerate(FT):
        mid = tuple(WR[j] + (tip[j] - WR[j]) * 0.55 + (0.0, 1.2, 0.0)[j] for j in range(3))
        rod(h, [WR, mid, tip], [1.7, 1.2, 0.6], 'bone', ext=0.1)
        spike(h, tip, tuple(tip[j] + (tip[j] - mid[j]) * 0.22 for j in range(3)), 0.6, 'horn', 'horn_r')      # (a black claw on each)
    for i in range(3):
        panel(h, WR, FT[i], FT[i + 1], 'memb', n=3, t=0.22)
    for (p, q, s) in ((0, 1, 1.5), (1, 2, 1.7), (2, 3, 1.3)):                           # (an eye in each membrane, like the Sovereign's)
        c = tuple(WR[j] * 0.45 + (FT[p][j] + FT[q][j]) * 0.275 for j in range(3))
        eye_plate(h, (c[0], c[1], c[2] - 0.2), s, 'north', 'eye')
        eye_plate(h, (c[0], c[1], c[2] + 0.2), s, 'south', 'eye')
    B(a, (SH[0] - 2.5, SH[1] - 1.2, SH[2] - 3.0), (SH[0] + 2.5, SH[1] + 2.0, SH[2] + 3.0), 'plate')       # (a plate over the shoulder joint)

# ---------------------------------------------------------------------------------------------------- the legs and the clawed feet
for p, f, sx in (('legr', 'footr', 1), ('legl', 'footl', -1)):
    x, y, z = PIVOT[p]
    for (y0, y1, hw) in ((11.0, 17.0, 3.0), (17.0, 19.0, 2.4)):
        slab(R, p, y0, y1, hw, 'gcr3', 2.8, c=(x, z), k=0.66)                          # (the thigh: feathered, cracked)
    rod(p, [(x, 11.4, z), (x + 0.2 * sx, 7.0, z + 0.6), (x + 0.6 * sx, 2.8, z - 1.2)], [2.2, 1.9, 1.7], 'scute')
    spike(p, (x, 7.6, z + 1.2), (x, 6.6, z + 4.0), 0.9, 'horn', 'horn_r')              # (a spur, backward)
    fx_, fy, fz = PIVOT[f]
    for dx, dz, L in ((0.0, -1.0, 8.4), (0.65, -0.75, 7.0), (-0.65, -0.75, 7.0)):
        tip = (fx_ + dx * L, 0.9, fz + dz * L)
        rod(f, [(fx_, 2.2, fz), tip], [1.5, 1.0], 'scute', ext=0.1)
        spike(f, tip, (tip[0] + dx * 1.8, 0.0, tip[2] + dz * 1.8 - 0.2), 0.9, 'glass', 'red_l')
    panel(f, (fx_, 1.4, fz), (fx_ + 0.65 * 6.0, 1.0, fz - 0.75 * 6.0), (fx_, 1.0, fz - 7.0), 'memb', n=2, t=0.25)    # (torn webbing)
    panel(f, (fx_, 1.4, fz), (fx_ - 0.65 * 4.4, 1.0, fz - 0.75 * 4.4), (fx_, 1.0, fz - 5.0), 'memb', n=2, t=0.25)

# ---------------------------------------------------------------------------------------------------- fx
# THE DREAD BEAM: out of the brow's eye - a hot core, a red sheath, rings along it
bx, by, bz = PIVOT['beam']
BL = 46.0                                                     # (built full length, then kept inside the model box: PART_K 2.2)
end = (0, 49.4 - BL * 0.34, -21.0 - BL * 0.94)
R.seg('beam', (0, 49.4, -21.0), end, 1.4, 1.4, 'beamc', light=15, full=True)
R.seg('beam', (0, 49.4, -21.0), end, 2.8, 2.8, 'beamc', light=15, full=True, up=(0.7, 0.0, -0.7))
for k in range(6):
    s_ = 0.08 + k * 0.17; c = tuple(PIVOT['beam'][j] * 0 + (0, 49.4, -21.0)[j] + (end[j] - (0, 49.4, -21.0)[j]) * s_ for j in range(3))
    ring(R, 'beam', c, 2.4 + k * 0.35, 8, 0.5, 0.5, 'ring', plane='xy', light=14)
for k in range(5):                                            # (where it strikes: a splash of red sparks)
    a_ = math.radians(k * 72); B('beam', (end[0] + 2.2 * math.cos(a_) - 0.6, end[1] + 2.2 * math.sin(a_) - 0.6, end[2]), (end[0] + 2.2 * math.cos(a_) + 0.6, end[1] + 2.2 * math.sin(a_) + 0.6, end[2] + 0.02), 'spark', faces=('north', 'south'), full=True, light=15)

# THE SHRIEK: the honk, gone wrong - jagged red rings (each ring's segments kinked out of true)
for i, (r, z) in enumerate(((3.0, -27.5), (5.0, -31.0), (7.4, -35.5))):
    for k in range(12):
        a0, a1 = math.radians(k * 30), math.radians(k * 30 + 30); jag = 1.0 + (0.18 if k % 2 else -0.12)
        p0 = (r * math.cos(a0), 47.0 + r * math.sin(a0), z); p1 = (r * jag * math.cos((a0 + a1) / 2), 47.0 + r * jag * math.sin((a0 + a1) / 2), z - 0.4)
        R.seg('shriek', p0, p1, 0.6, 0.35, 'ring', up=(0.0, 0.0, -1.0), light=13)
# DREAD EGGS: black, red-cracked eggs round it; one hatched - grasping void hands
for (x, z, r) in ((14.0, -10.0, 3.2), (-15.0, -4.0, 3.0), (6.0, 16.0, 3.0)):
    stack(R, 'eggs', [(0.0, r * 0.4, r * 0.62), (r * 0.4, r * 1.1, r * 0.92), (r * 1.1, r * 1.7, r * 0.86), (r * 1.7, r * 2.2, r * 0.6), (r * 2.2, r * 2.5, r * 0.3)],
          'egg', c=(x, z), k=0.66)
stack(R, 'eggs', [(0.0, 1.2, 2.4), (1.2, 2.0, 2.8)], 'egg', c=(-6.0, 14.0), k=0.66)
for k, (dx, dz) in enumerate(((-1.0, 0.4), (0.8, -0.6), (0.2, 1.0))):
    b = (-6.0 + dx, 1.6, 14.0 + dz); t = (-6.0 + dx * 3.2, 6.8 + k, 14.0 + dz * 3.0)
    rod('eggs', [b, t], [0.9, 0.6], 'flesh')
    for j in range(3): spike('eggs', t, (t[0] + dx * 0.8 + (j - 1) * 0.6, t[1] + 1.6, t[2] + dz * 0.8), 0.35, 'horn', 'horn_r')
# THE UNLUCKY: the inverted Lucky sigil on the ground, and four broken coins standing at its edge
B('curse', (-18, 0.05, -18), (18, 0.12, 18), 'sigil', faces=('up',), uv={'up': [0, 0, 16, 16]}, light=11)
for i in range(4):
    a = math.radians(i * 90 + 45); x, z = 15.0 * math.cos(a), 15.0 * math.sin(a)
    R.box('curse', (x - 1.4, 0.1, z - 0.25), (x + 1.4, 2.9, z + 0.25), 'coin', rot=('y', -i * 90 - 45, (x, 1.5, z)), uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]})
    spike('curse', (x, 0.0, z), (x * 1.08, 6.0, z * 1.08), 0.9, 'glass', 'red_l')
# THE SHARD: falling out of its head (the defeat) - void-glass, the heart-crystal, a trail of red motes
sx0, sy0, sz0 = PIVOT['shard']
R.seg('shard', (sx0 + 0.4, sy0 - 1.2, sz0 + 0.8), (sx0 + 2.0, sy0 + 5.6, sz0 + 2.6), 2.0, 1.6, 'glass', ext=0.1)
R.seg('shard', (sx0 - 1.0, sy0 - 0.8, sz0 + 0.2), (sx0 - 2.4, sy0 + 3.4, sz0 - 0.8), 1.2, 1.0, 'glass')
R.box('shard', (sx0 - 0.8, sy0 - 0.2, sz0 - 0.4), (sx0 + 0.9, sy0 + 1.5, sz0 + 1.3), 'heart', rot=((35.26, 45.0, 0.0), (sx0, sy0 + 0.6, sz0 + 0.4)), light=15)
for k in range(5): B('shard', (sx0 - 0.3 + k * 0.4, sy0 - 2.0 - k * 1.3, sz0 + 0.1 * k), (sx0 + 0.1 + k * 0.4, sy0 - 1.6 - k * 1.3, sz0 + 0.1 * k + 0.4), 'red_l', light=14)
# THE AURA (rare, this form's): a halo of watching eyes and gold motes, two rings
for i in range(10):
    a = math.radians(i * 36); x, z = 20.0 * math.cos(a), 20.0 * math.sin(a); y = 34.0 + 4.0 * math.sin(a * 2)
    B('aura', (x - 1.0, y - 1.0, z), (x + 1.0, y + 1.0, z + 0.02), 'eye', faces=('north', 'south'), uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, light=14)
    B('aura', (x * 0.8 - 0.5, y - 10 - 0.5, z * 0.8), (x * 0.8 + 0.5, y - 10 + 0.5, z * 0.8 + 0.02), 'spark', faces=('north', 'south'), full=True, light=15)


R.PART_K['beam'] = 2.2
R._els['beam'] = rigkit.shrink(R._els['beam'], 2.2)       # (the beam: built at full length, shown at 2.2x)


# ---------------------------------------------------------------------------------------------------- skins
def _skin(sfx, P, B_, red):
    swap = {}
    t = _tex(P, B_, suffix=sfx)
    # (the cracks' colour: recolor the red of the fresh cracks)
    for k in ('gcr', 'gcr2', 'gcr3', 'prim', 'down', 'bone', 'flesh'):
        im = t[k]
        if red:
            im = recolor(im, {RED: red[0], RED_L: red[1], RED_D: red[2]})
        R.tex(k + sfx, im); swap[k] = k + sfx
    if red:
        for k in ('red', 'red_l', 'red_d', 'heart', 'horn_r', 'eye', 'memb', 'beamc', 'ring'):
            src = R._tex[k]
            g = lambda c: (c[1] * 0.4, min(255, c[0] * 0.9 + 30), c[2] * 0.5 + 20) if c[0] > c[1] + 40 else c
            R.tex(k + sfx, hue(src, g)); swap[k] = k + sfx
        for f in [None] + list(FACES):
            k = 'eyes' if f is None else f'eyes_{f}'
            R.tex(k + sfx, __import__('fol5_kit').hue(R._tex[k], lambda c: (c[1] * 0.4, min(255, c[0] * 0.9 + 30), c[2] * 0.5 + 20) if c[0] > c[1] + 40 else c))
            swap[k] = k + sfx
    R.skin(sfx, swap)


_skin('_rg', dict(deep='#4a2020', dark='#7a4038', base='#b47064', light='#dc9a8a', shine='#ffd8cc', white='#fff0ec'),
      dict(deep='#4a3030', dark='#a07a74', base='#e0beb4', light='#f4dcd4', shine='#fff4f0'), None)
_skin('_pt', dict(deep='#2a2e34', dark='#5a626e', base='#9aa2ae', light='#c8d0da', shine='#ffffff', white='#ffffff'),
      dict(deep='#3a3e44', dark='#8a9098', base='#c8ccd4', light='#e4e8ee', shine='#ffffff'), None)
_skin('_sh', dict(deep='#04200e', dark='#0a4422', base='#17783a', light='#3eb05a', shine='#d8ff9a', white='#f0ffe0'),
      dict(deep='#1a3a10', dark='#6a9a50', base='#a8d890', light='#d0f0b8', shine='#f4ffe8'), ('#2ad850', '#a0ff8a', '#0e6a2a'))


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


from rigkit import qs
FOLD = dict(wr=limb(1, 0, -10, -70), wr2=qs(('y', -100)), wl=limb(-1, 0, -10, -70), wl2=qs(('y', 100)))   # (folded low along its back)
MANTLE = dict(wr=limb(1, 0, 30, -80), wr2=qs(('y', -150)), wl=limb(-1, 0, 30, -80), wl2=qs(('y', 150)))  # (folded, raised behind it like a mantle)
HALF = dict(wr=limb(1, -10, -14, 20), wr2=T(0, 50, 0), wl=limb(-1, -10, -14, 20), wl2=T(0, -50, 0))
POSES = R.POSES
POSES.update({
    'idle_a': P(_face='narrowed', **FOLD, neck1=T(-4), neck2=T(4), neck3=T(4), head=T(6), neckb=T(4, 0, 12), headb=T(10, 30, 0)),
    # (the boss's idle: the wings half open)
    'menace': P(_face='narrowed', **HALF, neck1=T(-4), neck2=T(4), neck3=T(4), head=T(6), neckb=T(4, 0, 12), headb=T(10, 30, 0)),
    'idle_b': P(**MANTLE, neck1=T(-2, -10), neck2=T(6, -12), head=T(10, -20, 10), neckb=T(-10, 20, 20), headb=T(20, 50, 10), jaw=T(10)),
    # THE STALK (4 frames, 24 ticks): heavy, the goose's waddle grown slow and deliberate - a roll of 6 deg, the necks low and level,
    # swaying against each step (the goose's neck-bend, gone predatory)
    'walk_0': P(_face='narrowed', **FOLD, body=T(6, 4, 6), legr=limb(1, -18, -6), legl=limb(-1, 22, -6), footl=limb(-1, -24),
                neck1=T(12, -4), neck2=T(8), neck3=T(4), head=T(-10), neckb=T(0, 10, 16), headb=T(10, 30, 0)),
    'walk_1': P(_face='narrowed', **FOLD, body=T(8), legr=limb(1, 4), legl=limb(-1, 4), neck1=T(16), neck2=T(6), head=T(-12), neckb=T(4, 0, 14)),
    'walk_2': P(_face='narrowed', **FOLD, body=T(6, -4, -6), legl=limb(-1, -18, 6), legr=limb(1, 22, 6), footr=limb(1, -24),
                neck1=T(12, 4), neck2=T(8), neck3=T(4), head=T(-10), neckb=T(0, -6, 10), headb=T(10, 10, 0)),
    'walk_3': P(_face='narrowed', **FOLD, body=T(8), legr=limb(1, 4), legl=limb(-1, 4), neck1=T(16), neck2=T(6), head=T(-12), neckb=T(4, 0, 14)),
    # THE ROAR (its entrance, and the turn's last beat): reared up, both heads high, every jaw open, the wings flung wide
    'roar': P(_face='wide', _show=('shriek',), body=T(-10), neck1=T(-16), neck2=T(-8), neck3=T(-6), head=T(-24), jaw=T(38),
              neckb=T(-20, 10, 28), headb=T(-30, 30, 0), wr=limb(1, 10, 18, -10), wl=limb(-1, 10, 18, -10)),
    # DREAD BEAM: it draws its head back (the brow-eye kindling, 20 ticks) - then the beam (40 ticks, sweeping 60 deg)
    'beam_up': P(_face='narrowed', **HALF, neck1=T(-18), neck2=T(-14), neck3=T(-10), head=T(10), neckb=T(-10, 0, 30), headb=T(0, 40)),
    'beam': P(_face='wide', _show=('beam',), **HALF, body=T(4), neck1=T(8), neck2=T(4), neck3=T(0), head=T(6), neckb=T(-6, 0, 30), headb=T(-10, 50)),
    # THE SHRIEK: the honk, gone wrong (wind-up 10, the shriek 4, held 10)
    'shriek': P(_face='wide', _show=('shriek',), body=T(4), neck1=T(20), neck2=T(-4), neck3=T(-6), head=T(-16), jaw=T(40),
                neckb=T(10, 0, 20), headb=T(-10, 20), wr=limb(1, 0, 10, -10), wl=limb(-1, 0, 10, -10)),
    # WING SLAM: wings raised high (12) - and brought down on the ground either side of it (3): a shockwave
    'slam_up': P(_face='wide', body=T(-12), neck1=T(-10), neck2=T(-4), head=T(-8), wr=limb(1, 0, 60, -20), wl=limb(-1, 0, 60, -20), wr2=T(0, 0, 30), wl2=T(0, 0, -30)),
    'slam': P(_face='narrowed', body=T(16), neck1=T(26), neck2=T(10), head=T(-20), jaw=T(20), wr=limb(1, 20, -36, -30), wl=limb(-1, 20, -36, -30), wr2=T(0, 30, -30), wl2=T(0, -30, 30)),
    # THE LUNGE: the long neck strikes like a snake (wind-up 8, strike 3, recover 10) - the second head hissing the other way
    'bite_up': P(_face='narrowed', **HALF, neck1=T(-24), neck2=T(-20), neck3=T(-10), head=T(20), jaw=T(10), neckb=T(10, 0, 30), headb=T(0, 60)),
    'bite': P(_face='wide', **HALF, body=T(12), neck1=T(46), neck2=T(16), neck3=T(4), head=T(-30), jaw=T(42), neckb=T(-10, 0, 34), headb=T(-10, 70)),
    # DREAD EGGS (its parody of phase 1's egg drop): it rears, and the eggs are round it
    'eggs': P(_face='narrowed', _show=('eggs',), **HALF, body=T(-6), neck1=T(-8), head=T(-6)),
    # THE UNLUCKY: it spreads its wings over you and the sigil burns under everyone (luck inverted - see the doc)
    'curse': P(_face='wide', _show=('curse',), body=T(-8), neck1=T(-12), neck2=T(-6), head=T(16), wr=limb(1, 0, 30, -30), wl=limb(-1, 0, 30, -30), wr2=T(0, -20), wl2=T(0, 20)),
    'hurt': P(_face='hurt', **HALF, body=T(-14, 0, 8), neck1=T(-20, 0, -14), neck2=T(-10), head=T(-14), jaw=T(30), neckb=T(-20, 0, 30)),
    # TIRED / THE DEFEAT: down on its breast, wings fallen open, the heads low - and the shard tumbling out of its crown
    'tired': P(_face='dim', body=T(14), legr=limb(1, 60), legl=limb(-1, 60), neck1=T(40), neck2=T(20), neck3=T(10), head=T(-10),
               neckb=T(30, 0, 30), headb=T(20), wr=limb(1, 10, -20, 10), wl=limb(-1, 10, -20, 10), wr2=T(0, 20, -20), wl2=T(0, -20, 20)),
    'defeat': P(_face='blink', _show=('shard',), _o_shard=(3.0, 3.0, -2.0), body=T(18, 0, 6), legr=limb(1, 70), legl=limb(-1, 70), neck1=T(52), neck2=T(24), neck3=T(16), head=T(-4),
                neckb=T(40, 0, 40), headb=T(30), wr=limb(1, 10, -30, 10), wl=limb(-1, 10, -30, 10), wr2=T(0, 30, -30), wl2=T(0, -30, 30)),
    # SITTING (right-click): crouched like a gargoyle, wings folded round it, the heads watching; (sneak) coiled, the heads tucked
    'sit_a': P(_face='narrowed', **FOLD, body=T(-4), legr=limb(1, 70, 8), legl=limb(-1, 70, 8), footr=limb(1, -60), footl=limb(-1, -60),
               neck1=T(-6), neck2=T(4), head=T(8), neckb=T(0, 0, 18), headb=T(20, 40, 0)),
    'sit_b': P(_face='blink', **FOLD, body=T(6), legr=limb(1, 80), legl=limb(-1, 80), footr=limb(1, -70), footl=limb(-1, -70),
               neck1=T(-50, 0, 0), neck2=T(-56, 0, 10), neck3=T(-30), head=T(-30, 0, 20), neckb=T(-40, 40, 30), headb=T(-30, 60, 0)),
    'aura': P(_face='narrowed', _show=('aura',), **MANTLE, neck1=T(-4), neck2=T(4), head=T(6)),
    'doll': P(_face='narrowed', **FOLD, neck1=T(-4), neck2=T(4), head=T(6)),
})
DRAFT = list(POSES)
R.DRAFT = DRAFT
DOLL_GROUPS = {'head': 'head', 'jaw': 'head', 'neck3': 'body', 'neckb': 'body', 'headb': 'head', 'body': 'body', 'neck1': 'body', 'neck2': 'body',
               'tail': 'body', 'wr': 'body', 'wl': 'body', 'wr2': 'body', 'wl2': 'body', 'legr': 'legs', 'legl': 'legs', 'footr': 'legs', 'footl': 'legs'}

# ATTACKS of the boss's phase 2 (ticks; see the design doc)
ATTACKS = {
    'beam': dict(poses=('beam_up', 'beam'), windup=20, hit=21, hold=40, sweep=60, dmg=6, per=10, cd=14, dread=True,
                 fx='the brow-eye beam sweeps 60 deg across the arena; get behind something solid, or hold a Lucky Token up (it reflects ONCE, the token used up)'),
    'shriek': dict(poses=('shriek',), windup=10, hit=11, hold=10, recover=10, dmg=8, radius=10.0, cd=12, dread=True,
                   fx='three jagged rings out to 10 blocks; Darkness 3 s and Weakness 5 s (the honk, gone wrong); jump the rings as they pass'),
    'slam': dict(poses=('slam_up', 'slam'), windup=12, hit=13, hold=4, recover=12, dmg=10, radius=6.0, cd=10, dread=True,
                 fx='both wings down: a shockwave ring along the floor out to 6 blocks (jump it), the floor cracks'),
    'bite': dict(poses=('bite_up', 'bite'), windup=8, hit=9, hold=3, recover=10, dmg=12, reach=7.0, cd=6, dread=True,
                 fx='a snake-strike along a line 7 blocks; the second head bites the other way 1 s later'),
    'eggs': dict(poses=('eggs',), windup=12, hit=14, fuse=60, n=4, cd=20,
                 fx='four dread eggs; each hatches in 3 s into a GRASPING HAND that roots whoever stands near (2 s) - break them first'),
    'curse': dict(poses=('curse',), windup=16, hit=17, hold=100, cd=30,
                  fx='THE UNLUCKY: the inverted Lucky sigil under everyone for 5 s: Unluck, and every Lucky-Night buff and charm you hold is DRAINED into it (it heals 4 per charm) - unless you step off the sigil'),
}
