"""2.67: Democratus - the storm reaper, from the reference art: a broad, hooded warrior in a long, ragged dark-green cloak, dark
plate over a darker shirt (a jagged cut at the chest, a violet gem at the collar), a black belt, ragged tassets, dark trousers,
green boots and black gloves; mint-white hair under the hood, violet eyes, a dark violet beard over his mouth and jaw. His
scythe is longer than he is tall: a black shaft banded in gold, a great steel-and-teal blade, a green crystal spearhead held in
golden claws, a golden crescent at the butt.

The phase57_art kit (as Leo, a head taller and broader): one item model per part, its joint at model (8, 8, 8). Design units:
feet at y=0, facing -z, his right is +x; drawn at RIG_SCALE. The cloak is its own part (it hangs from the back of his neck and
swings out behind him); the scythe is its own part too, jointed at his left fist (as Leo's trident is at his right) - on his
shoulder at rest (his left arm bent: its own model, as Leo's salute), planted beside him when he kneels, swung wide in a fight.
His faces - the beard hides his mouth, so it's all in the eyes and brows (proud, menacing, dry): blink, smirk (one brow up,
the eyes narrowed - amused), serious (brows down hard, a glare - in a fight), hurt (one eye screwed shut), surprised,
sleepy, glare (the eyes cut to the side - when his rival Cecil is about)."""
import math
import random
from PIL import Image, ImageDraw
from phase57_art import _cloth, _hair, _el, hexc, qa, qmul, limb, torso, _qrot

RIG_SCALE = 0.92
PIVOT = {'body': (0, 14.5, 0), 'head': (0, 27, 0), 'armr': (6.1, 24.8, 0), 'arml': (-6.1, 24.8, 0), 'legr': (2.4, 14.5, 0), 'legl': (-2.4, 14.5, 0),
         'cape': (0, 25.6, 2.9)}
HEAD_K = 0.86
PARTS = ('body', 'head', 'armr', 'arml', 'legr', 'legl', 'cape', 'scythe')
GRIP = (-6.3, 11.6, -0.2)                    # his left fist (design units): the scythe's joint (he carries it left-handed, as in the art)
ELBOW = 17.2                                 # (the resting arm bends here: the forearm folds up in front, the fist at his shoulder)
KNEE = 8.6                                   # (a bent leg folds here: the shin runs straight back - a kneel, or knees up sitting)
ALT = {'arml': ('rest',), 'armr': ('rest',), 'legr': ('bent',), 'legl': ('bent',)}      # (the parts with a second model, swapped in by a pose)
SCYTHE_K = 0.75                              # (the scythe is built at 3/4 size - a model may not reach past 32 - and shown 4/3 as large)
GLOW = {'#4c2a80': '#9a5af0', '#8a5ac0': '#c890ff', '#c8a8f2': '#f2e2ff', '#1c0a2c': '#e8c8ff'}   # his irises, lit: the night glow
GRIP_REST = (-6.3, 21.4, -4.6)
SKIN, SKIN_DK, SKIN_LT = '#d0905e', '#a8704a', '#e6aa78'
HAIR = ('#a8dccc', '#bce6d8', '#cdeee4', '#dcf6ee', '#ecfcf6')
BEARD, BEARD_DK, BEARD_LT = '#3a2856', '#261a3c', '#4e3870'
HOOD, HOOD_DK, HOOD_LT = '#2c4620', '#1c3014', '#3c5a2a'
PLATE, PLATE_DK, PLATE_LT = '#3c413e', '#272b29', '#5a615c'
SHIRT = '#1c201e'
GOLD, GOLD_DK = '#f0cf4a', '#c49a28'
STEEL, TEAL, BLADE_LT = '#97a3ab', '#78c2ae', '#d6eef0'
CRYSTAL, CRYSTAL_LT, CRYSTAL_DK = '#3fbf3a', '#8af070', '#1c8428'
DEMO_EXPR = ('blink', 'smirk', 'serious', 'hurt', 'surprised', 'sleepy', 'glare')


# ---------------------------------------------------------------------------------------------------- textures
def _sheen(base, seed, var=0.02, streak=(14, 17), k_edge=0.12):
    """worn plate: a soft vertical sheen, a pale streak, a darker lower edge"""
    im = _cloth(base, seed, var=var)
    for y in range(64):
        for x in range(64):
            k = 1.0 + 0.10 * math.cos((x - 20) / 64 * math.pi * 2) - (k_edge if y > 54 else 0)
            if streak[0] <= x <= streak[1]: k += 0.16
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(max(0, min(255, p[i] * k))) for i in range(3)) + (255,))
    return im


def _chest():
    """the breastplate's front (12 x 10 texels used): dark plate, a jagged cut down the middle showing the black shirt, a pale rim"""
    P = hexc
    im = _sheen(PLATE, 301); d = ImageDraw.Draw(im)
    cut = [(3, 0), (9, 0), (8, 3), (10, 4), (7, 6), (8, 9), (6, 7), (4, 9), (5, 6), (2, 4), (4, 3)]
    d.polygon(cut, fill=P(SHIRT))
    d.line(cut + [cut[0]], fill=P(PLATE_LT))
    for x, y in ((1, 1), (11, 1), (0, 6), (12, 6)): d.point((x, y), fill=P(PLATE_LT))
    return im


def _hood(seed, base=HOOD):
    """heavy wool: the weave in faint vertical runs, darker in the folds"""
    im = _cloth(base, seed, var=0.03); rnd = random.Random(seed)
    for x in range(64):
        k = 0.86 if (x // 4 + rnd.randint(0, 1)) % 3 == 0 else 1.0
        for y in range(64):
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(p[i] * k) for i in range(3)) + (255,))
    return im


def _cape():
    """the long cloak: the weave, and a ragged, darker hem at the bottom (the art's torn edge)"""
    im = _hood(311); rnd = random.Random(312)
    edge = [44 + int(4 * math.sin(x / 2.3)) + rnd.randint(0, 3) for x in range(64)]
    for x in range(64):
        for y in range(edge[x], 64):
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(p[i] * 0.62) for i in range(3)) + (255,))
    return im


def _beard(seed):
    im = _cloth(BEARD, seed, var=0.03); rnd = random.Random(seed)
    for x in range(64):
        for y in range(64):
            if rnd.random() < 0.18: im.putpixel((x, y), hexc(rnd.choice((BEARD_DK, BEARD_LT))))
    return im


def face(expr=None):
    """32 x 32 under the hood: a spiky mint fringe, strong dark brows, violet eyes, a long nose - and from the cheekbones down,
    the dark violet beard. expr=None is the reference art's face (the right brow arched, the left set low: sizing you up)."""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(SKIN)); d = ImageDraw.Draw(im); rnd = random.Random(97)
    for x in range(32):                                                                      # the fringe: spikes of mint
        h = 6 + (3 if x % 5 in (1, 2) else 0) + (rnd.random() < 0.4)
        if x < 3 or x > 28: h += 3
        for y in range(h): im.putpixel((x, y), P(HAIR[min(4, (x + y) % 5)]))
    LID = '#1a1018'
    IRIS, IRIS_LT, IRIS_DK, PUPIL = '#8a5ac0', '#c8a8f2', '#4c2a80', '#1c0a2c'
    def eye(cx, flip, lid=0, wide=False, look=0):
        x0, y0 = cx - 4, 14
        top = y0 - (1 if wide else 0)
        d.polygon([(x0, y0 + 2), (x0 + 2, top), (x0 + 7, top), (x0 + 8, y0 + 2), (x0 + 6, y0 + 4), (x0 + 2, y0 + 4)], fill=P('#f6f2f8'))
        ix = x0 + 3 + look
        d.rectangle((ix, top, ix + 2, y0 + 4), fill=P(IRIS_DK)); d.rectangle((ix, y0 + 2, ix + 2, y0 + 4), fill=P(IRIS))
        d.point((ix + 1, y0 + 4), fill=P(IRIS_LT))
        d.rectangle((ix + 1, y0 + 1, ix + 1, y0 + 2), fill=P(PUPIL))
        d.point((ix + (2 if not flip else 0), top), fill=P('#ffffff'))
        if lid: d.rectangle((x0, top, x0 + 8, top + lid - 1), fill=P(SKIN))
        d.line((x0, top + lid, x0 + 8, top + lid), fill=P(LID))
        d.point((x0 + (8 if not flip else 0), top + lid + 1), fill=P(LID))
    def shut(cx, flip, tight=False):
        x0, y0 = cx - 4, 14
        if tight:
            d.line((x0, y0 + 1, x0 + 4, y0 + 3), fill=P(LID)); d.line((x0 + 4, y0 + 3, x0 + 8, y0 + 1), fill=P(LID))
        else:
            d.line((x0 + 1, y0 + 3, x0 + 7, y0 + 3), fill=P(LID)); d.point((x0 + (8 if not flip else 0), y0 + 2), fill=P(LID))
    # (his right eye is on the left of the plate)
    if expr in (None, 'surprised'):
        eye(9, False, lid=0 if expr else 1, wide=expr == 'surprised'); eye(23, True, wide=expr == 'surprised')
    elif expr == 'smirk':
        eye(9, False, lid=2); eye(23, True, lid=1)
    elif expr == 'serious':
        eye(9, False, lid=2); eye(23, True, lid=2)
    elif expr == 'glare':
        eye(9, False, lid=2, look=2); eye(23, True, lid=2, look=2)
    elif expr == 'sleepy':
        eye(9, False, lid=3); eye(23, True, lid=3)
    elif expr == 'blink':
        shut(9, False); shut(23, True)
    elif expr == 'hurt':
        eye(9, False, lid=2); shut(23, True, tight=True)
    BROW, BROW_LT = '#14100e', '#2a201c'
    for cx, s in ((9, 1), (23, -1)):                                                         # brows: heavy, two texels deep
        for dx in range(-4, 5):
            inner = dx * s > 0
            if expr in ('serious', 'hurt', 'glare'):                   # down hard toward the nose
                y = 11 + (1 if inner else 0) + (1 if dx * s > 2 else 0)
            elif expr == 'surprised':
                y = 9 + (1 if abs(dx) > 3 else 0)
            elif expr == 'sleepy':
                y = 12 + (1 if abs(dx) > 3 else 0)
            elif expr == 'smirk' and s < 0:                             # his left brow up, arched
                y = 9 + (1 if abs(dx) > 2 else 0)
            elif s > 0 and expr in (None, 'blink', 'smirk'):            # his right brow set low, angled in
                y = 11 + (1 if inner else 0)
            else:                                                       # the other arched (the art)
                y = 10 + (1 if abs(dx) > 2 else 0)
            x = cx + dx * s
            im.putpixel((x, y), P(BROW)); im.putpixel((x, y + 1), P(BROW_LT))
    for y in range(16, 22): im.putpixel((16, y), P(SKIN_DK))                                # the nose
    d.line((14, 22, 18, 22), fill=P(SKIN_DK)); d.point((15, 21), fill=P(SKIN_LT))
    # the beard: from the cheekbones down over the mouth and jaw, a ragged edge at the top, a point at the chin
    rb = random.Random(98)
    for x in range(32):
        top = 21 + (2 if 12 <= x <= 20 else 0) - (1 if x < 4 or x > 27 else 0) + rb.randint(0, 1)
        for y in range(top, 32): im.putpixel((x, y), P(rb.choice((BEARD, BEARD, BEARD_DK, BEARD_LT))))
    if expr in ('smirk',):                                                                   # (a smirk lifts the cheek over the beard)
        for x in range(4, 10): im.putpixel((x, 21), P(SKIN_LT))
    return im


def glow(expr=None):
    """the eyes alone, lit (everything else clear): drawn over the face as a light-emitting layer, so his violet irises glow in
    the dark like a glow squid. Made from the face itself, so it follows every expression (shut eyes: nothing lit)."""
    src = face(expr); im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    lit = {hexc(k)[:3]: hexc(v) for k, v in GLOW.items()}
    for y in range(32):
        for x in range(32):
            c = src.getpixel((x, y))[:3]
            if c in lit: im.putpixel((x, y), lit[c])
    return im


def _emblem():
    """the collar gem (4 x 4 texels): violet, faceted, a pale glint"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P('#4a2a78')); d = ImageDraw.Draw(im)
    d.polygon([(2, 0), (4, 2), (2, 4), (0, 2)], fill=P('#8a4ad0')); d.point((1, 1), fill=P('#e0c8ff')); d.point((2, 2), fill=P('#b07af0'))
    return im


def _blade():
    """the scythe's steel: grey on the back, teal toward the edge, a pale glint along it"""
    im = Image.new('RGBA', (64, 64)); a, b = hexc(STEEL), hexc(TEAL)
    rnd = random.Random(321)
    for y in range(64):
        for x in range(64):
            t = min(1.0, max(0.0, (y - 4) / 10))
            c = tuple(int((a[i] * (1 - t) + b[i] * t) * (1 + rnd.uniform(-0.02, 0.02))) for i in range(3))
            if 10 <= y <= 11: c = tuple(min(255, int(v * 1.25)) for v in c)
            im.putpixel((x, y), c + (255,))
    return im


def _crystal(seed):
    im = _cloth(CRYSTAL, seed, var=0.04); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 7): d.line((k, 0, k + 32, 64), fill=hexc(CRYSTAL_LT))
    for k in range(-60, 64, 11): d.line((k, 64, k + 30, 0), fill=hexc(CRYSTAL_DK))
    return im


def textures():
    T = {}
    T['dm_skin'] = _cloth(SKIN, 291, var=0.02)
    T['dm_hair'] = _hair(292, HAIR)
    T['dm_face'] = face()
    for e in DEMO_EXPR: T[f'dm_face_{e}'] = face(e)
    T['dm_glow'] = glow()
    for e in DEMO_EXPR: T[f'dm_glow_{e}'] = glow(e)
    T['dm_beard'] = _beard(293)
    T['dm_hood'] = _hood(294)
    T['dm_hood_dk'] = _hood(295, HOOD_DK)
    T['dm_cape'] = _cape()
    T['dm_plate'] = _sheen(PLATE, 296)
    T['dm_plate_dk'] = _sheen(PLATE_DK, 297)
    T['dm_chest'] = _chest()
    T['dm_rim'] = _cloth(PLATE_LT, 298, var=0.01)
    T['dm_shirt'] = _cloth(SHIRT, 299, var=0.03)
    T['dm_belt'] = _cloth('#121614', 300, var=0.03)
    T['dm_buckle'] = _sheen('#56605a', 302)
    T['dm_pants'] = _sheen('#3a3f3b', 303, var=0.03, streak=(30, 33), k_edge=0.0)
    T['dm_boot'] = _cloth('#2e3c22', 304, var=0.04)
    T['dm_cuff'] = _cloth('#191d17', 305, var=0.03)
    T['dm_glove'] = _cloth('#1c201e', 306, var=0.04)
    T['dm_gem'] = _emblem()
    T['dm_shaft'] = _cloth('#1c2220', 307, var=0.03, grain=(4, 0.85))
    T['dm_gold'] = _sheen(GOLD, 308, var=0.02)
    T['dm_gold_dk'] = _cloth(GOLD_DK, 309, var=0.03)
    T['dm_blade'] = _blade()
    T['dm_blade_lt'] = _cloth(BLADE_LT, 310, var=0.01)
    T['dm_crystal'] = _crystal(313)
    T['dm_crystal_lt'] = _cloth(CRYSTAL_LT, 314, var=0.03)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: thick thighs tapering to the calf, a guard over the knee, green boots with a flared black cuff, a blunt toe
    def leg_lower(x0, x1, cx):
        """the calf and boot of a straight leg (heights from the ground)"""
        return [((x0 + 0.2, 4.6, -1.7), (x1 - 0.2, 9.0, 1.7), 'dm_pants'),
                ((x0 - 0.35, 3.6, -2.2), (x1 + 0.35, 5.0, 2.2), 'dm_cuff'),                 # the cuff, flared
                ((x0 - 0.1, 0.9, -1.95), (x1 + 0.1, 3.8, 1.95), 'dm_boot'),
                ((x0 - 0.2, 0.3, -3.4), (x1 + 0.2, 1.7, 2.2), 'dm_boot'),                  # the foot
                ((cx - 1.4, 0.3, -4.6), (cx + 1.4, 1.4, -3.2), 'dm_boot'),                 # the toe, and its blunt tip
                ((cx - 0.7, 0.3, -5.3), (cx + 0.7, 1.0, -4.5), 'dm_boot'),
                ((x0 - 0.25, 0.0, -4.7), (x1 + 0.25, 0.35, 2.4), 'dm_cuff'),               # the sole
                ((x0 - 0.25, 0.3, 1.7), (x1 + 0.25, 1.2, 2.4), 'dm_cuff')]                 # the heel
    def thigh(x0, x1):
        return [((x0, 8.8, -1.95), (x1, 14.5, 1.95), 'dm_pants'),
                ((x0 - 0.1, 8.0, -2.15), (x1 + 0.1, 9.7, -1.3), 'dm_plate_dk')]             # the knee guard
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.4, 4.2) if sx > 0 else (-4.2, -0.4)
        return [_el(fr, to, t, pv) for fr, to, t in thigh(x0, x1) + leg_lower(x0, x1, (x0 + x1) / 2)]
    part('dm_legr', leg(1)); part('dm_legl', leg(-1))

    # ---- the bent leg: the thigh as before; from the knee the calf and boot run straight back (the sole facing up-back) - so a
    #      leg swung forward 90 degrees stands its shin straight down, and a leg straight down kneels on the shin
    def bent(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.4, 4.2) if sx > 0 else (-4.2, -0.4)
        k = KNEE
        # a straight-leg box (height y0..y1, depth z0..z1) folded back about the knee: it lies at height k + z, depth k - y behind
        lay = lambda fr, to, t: _el((fr[0], k + fr[2], k - to[1]), (to[0], k + to[2], k - fr[1]), t, pv)
        return [_el(fr, to, t, pv) for fr, to, t in thigh(x0, x1)] + \
               [_el((x0 - 0.05, k - 1.9, -1.9), (x1 + 0.05, k + 0.4, 1.9), 'dm_pants', pv)] + \
               [lay(fr, (to[0], min(to[1], k), to[2]), t) for fr, to, t in leg_lower(x0, x1, (x0 + x1) / 2)]
    part('dm_legr_bent', bent(1)); part('dm_legl_bent', bent(-1))

    # ---- body: a broad breastplate in two tiers (the chest wider than the waist), a raised front plate with the jagged cut, the
    #      black shirt, a heavy belt with a pouch, ragged tassets, the mantle stepped round his shoulders, a high collar, the gem
    pv = PIVOT['body']
    B = lambda fr, to, t, rot=None, uv=None: _el(fr, to, t, pv, rot, uv)
    body = [B((-4.2, 14.4, -2.5), (4.2, 17.8, 2.5), 'dm_shirt'),
            B((-4.6, 17.6, -2.65), (4.6, 21.0, 2.65), 'dm_plate'),
            B((-5.0, 20.8, -2.85), (5.0, 25.0, 2.8), 'dm_plate'),
            B((-3.9, 19.4, -3.1), (3.9, 24.6, -2.84), 'dm_chest', uv={'north': [0, 0, 12.4, 10]}),
            B((-4.65, 20.7, -2.95), (4.65, 21.1, 2.9), 'dm_rim'),
            B((-4.5, 13.6, -2.75), (4.5, 15.0, 2.75), 'dm_belt'),
            B((-1.0, 13.4, -3.05), (1.2, 15.2, -2.7), 'dm_buckle'),
            B((2.4, 12.4, -3.0), (4.2, 14.4, -2.2), 'dm_belt'), B((2.6, 13.8, -3.08), (4.0, 14.3, -2.95), 'dm_buckle'),   # a pouch at his hip
            B((-4.4, 9.4, -2.95), (-0.5, 13.8, -2.5), 'dm_plate_dk'), B((-4.0, 8.6, -2.9), (-2.4, 9.6, -2.55), 'dm_plate_dk'),   # tassets, ragged
            B((0.5, 9.8, -2.95), (4.4, 13.8, -2.5), 'dm_plate_dk'), B((2.6, 9.0, -2.9), (4.2, 10.0, -2.55), 'dm_plate_dk'),
            B((-4.6, 10.2, -2.3), (-4.15, 13.8, 2.3), 'dm_plate_dk'), B((4.15, 10.6, -2.3), (4.6, 13.8, 2.3), 'dm_plate_dk'),
            B((-4.4, 10.4, 2.35), (4.4, 13.8, 2.85), 'dm_plate_dk'),
            B((-5.3, 23.0, -3.2), (5.3, 25.4, 3.2), 'dm_hood'),                                   # the mantle, stepped round
            B((-4.4, 25.2, -2.9), (4.4, 26.4, 3.0), 'dm_hood'),
            B((-5.0, 21.4, -3.35), (-2.6, 23.2, -3.0), 'dm_hood'), B((2.6, 21.4, -3.35), (5.0, 23.2, -3.0), 'dm_hood'),   # its front edges
            B((-4.2, 20.6, -3.3), (-3.0, 21.6, -3.05), 'dm_hood_dk'), B((3.0, 20.6, -3.3), (4.2, 21.6, -3.05), 'dm_hood_dk'),
            B((-3.2, 25.8, -2.8), (3.2, 28.0, 2.9), 'dm_hood'),                                   # the high collar
            B((-0.75, 23.5, -3.5), (0.75, 25.1, -3.22), 'dm_gold'),                               # the clasp, and its gem
            B((-0.5, 23.75, -3.6), (0.5, 24.85, -3.45), 'dm_gem', uv={'north': [0, 0, 4, 4]})]
    part('dm_body', body)

    # ---- the cloak: from the back of his neck nearly to his heels, wider at the hem, folded at the sides, the hem torn in strips
    pv = PIVOT['cape']
    C = lambda fr, to, t='dm_cape', uv=None: _el(fr, to, t, pv, None, uv)
    rnd = random.Random(97)
    strips = []
    for i in range(6):
        x = -5.8 + i * 1.94
        strips.append(C((x, 2.6 + rnd.random() * 2.4, 2.75), (x + 1.98, 6.2, 3.25), uv={f: [0, 12, 2, 16] for f in ('north', 'south')}))
    cape = [C((-5.0, 14.0, 2.6), (5.0, 25.6, 3.2), uv={f: [0, 0, 10, 8] for f in ('north', 'south')}),
            C((-5.8, 6.0, 2.7), (5.8, 14.2, 3.3), uv={f: [0, 8, 11.6, 12] for f in ('north', 'south')}),
            C((-5.6, 13.0, 1.2), (-5.0, 25.2, 3.0), 'dm_hood_dk'), C((5.0, 13.0, 1.2), (5.6, 25.2, 3.0), 'dm_hood_dk'),
            C((-6.1, 5.8, 1.8), (-5.6, 13.4, 3.1), 'dm_hood_dk'), C((5.6, 5.8, 1.8), (6.1, 13.4, 3.1), 'dm_hood_dk')] + strips
    part('dm_cape', cape)

    # ---- head: the face, the hood stepped round (open at the front, a thick rim, a peak falling back into a curled tail), mint
    #      tufts at the temples, the beard in layers standing proud of the jaw, a nose - and the eyes' glowing layer
    pv = PIVOT['head']; hd = lambda fr, to, t='dm_hood', rot=None: _el(fr, to, t, pv, rot)
    head = [_el((-4.0, 27.0, -4.0), (4.0, 35.0, 4.0), 'dm_skin', pv, uv={'north': [0, 0, 8, 8]}),
            hd((-4.7, 34.2, -4.5), (4.7, 35.8, 4.7)), hd((-3.9, 35.6, -3.8), (3.9, 36.6, 4.2)),            # the crown, rounded in steps
            hd((-4.75, 27.2, -3.9), (-4.1, 34.6, 4.7)), hd((4.1, 27.2, -3.9), (4.75, 34.6, 4.7)),         # its sides
            hd((-4.7, 26.4, 4.0), (4.7, 35.0, 4.85)),                                                     # the back
            hd((-4.8, 33.4, -4.75), (4.8, 34.6, -4.0), 'dm_hood_dk'),                                     # the rim round his face
            hd((-4.85, 26.8, -4.55), (-3.85, 34.0, -3.9), 'dm_hood_dk'), hd((3.85, 26.8, -4.55), (4.85, 34.0, -3.9), 'dm_hood_dk'),
            hd((-2.2, 34.8, 3.4), (2.2, 37.0, 6.6), rot=('x', -22.5, (0, 35.8, 4.2))),                   # the peak, falling back...
            hd((-1.3, 32.6, 5.8), (1.3, 35.2, 7.8), 'dm_hood_dk', ('x', -45, (0, 34.4, 6.2))),          # ...and curling
            hd((-0.8, 31.0, 6.4), (0.8, 32.8, 7.6), 'dm_hood_dk'),
            _el((-4.05, 30.0, -4.1), (-3.5, 33.8, -1.8), 'dm_hair', pv), _el((3.5, 30.0, -4.1), (4.05, 33.8, -1.8), 'dm_hair', pv),
            _el((-3.4, 33.4, -4.35), (-2.2, 34.2, -4.05), 'dm_hair', pv), _el((1.6, 33.5, -4.35), (2.9, 34.3, -4.05), 'dm_hair', pv),
            _el((-0.45, 29.7, -4.25), (0.45, 31.5, -4.0), 'dm_skin', pv),                                 # the nose
            _el((-3.9, 26.8, -4.3), (3.9, 29.4, -4.0), 'dm_beard', pv),                                   # the beard, in layers
            _el((-3.2, 26.0, -4.25), (3.2, 27.0, -3.8), 'dm_beard', pv),
            _el((-1.4, 25.2, -4.15), (1.4, 26.2, -3.6), 'dm_beard', pv),
            _el((-4.1, 26.8, -4.0), (-3.7, 29.6, 0.6), 'dm_beard', pv), _el((3.7, 26.8, -4.0), (4.1, 29.6, 0.6), 'dm_beard', pv)]
    eyes = _el((-4.0, 27.0, -4.03), (4.0, 35.0, -4.03), 'dm_glow', pv, uv={'north': [0, 0, 8, 8]}, faces=('north',))
    eyes['shade'] = False; eyes['light_emission'] = 15
    head.append(eyes)
    kx = (HEAD_K, HEAD_K, HEAD_K)
    for e in head:                                                                         # (a little smaller than life, about the neck)
        e['from'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['from'])]; e['to'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['to'])]
        if 'rotation' in e: e['rotation']['origin'] = [round(8 + (v - 8) * kx[i], 4) for i, v in enumerate(e['rotation']['origin'])]
    head[0]['faces']['north']['texture'] = '#dm_face'
    part('dm_head', head)

    # ---- arms: a domed pauldron, the dark sleeve, a thick bare arm (the biceps standing out), black gloves with a flared cuff
    def upper(sx):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.2 * sx
        return pv, cx, [_el((cx - 2.4, 22.4, -2.4), (cx + 2.4, 25.4, 2.4), 'dm_plate', pv),               # the pauldron, domed
                        _el((cx - 1.9, 25.2, -1.9), (cx + 1.9, 26.1, 1.9), 'dm_plate', pv),
                        _el((cx - 2.45, 22.2, -2.45), (cx + 2.45, 22.7, 2.45), 'dm_rim', pv),
                        _el((cx - 2.0, 20.6, -2.0), (cx + 2.0, 22.6, 2.0), 'dm_shirt', pv),               # the sleeve
                        _el((cx - 1.95, 17.4, -1.95), (cx + 1.95, 20.8, 1.95), 'dm_skin', pv),            # the upper arm
                        _el((cx - 1.5, 18.0, -2.2), (cx + 1.5, 20.4, -1.9), 'dm_skin', pv)]               # the biceps
    hand = lambda cx: [((cx - 1.75, 13.6, -1.75), (cx + 1.75, 17.6, 1.75), 'dm_skin'),                        # the forearm
                       ((cx - 2.1, 12.6, -2.1), (cx + 2.1, 14.0, 2.1), 'dm_plate'),                           # the glove's cuff, flared
                       ((cx - 1.8, 10.4, -1.8), (cx + 1.8, 12.8, 1.8), 'dm_glove'),
                       ((cx - 1.7, 9.4, -1.8), (cx + 1.7, 10.6, 0.4), 'dm_glove')]                            # the fingers
    def arm(sx):
        pv, cx, out = upper(sx)
        return out + [_el(fr, to, t, pv) for fr, to, t in hand(cx)]
    part('dm_armr', arm(1)); part('dm_arml', arm(-1))

    # ---- the resting arm: bent at the elbow, the forearm folded up in front - the fist at his shoulder, on the shaft (his left,
    #      the scythe on his shoulder); or both, the fists together before his face (kneeling, both hands on the planted scythe)
    def rest(sx):
        pv, cx, out = upper(sx); ey = ELBOW
        fold = lambda fr, to, t: _el(fr, to, t, pv, ('x', -45, (cx, ey, 0)))
        up = lambda y0, y1: (2 * ey - y1, 2 * ey - y0)
        return out + [_el((cx - 1.8, ey - 0.4, -1.8), (cx + 1.8, ey + 0.6, 1.8), 'dm_skin', pv)] + \
            [fold((fr[0], up(fr[1], to[1])[0], fr[2]), (to[0], up(fr[1], to[1])[1], to[2]), t) for fr, to, t in hand(cx)]
    part('dm_arml_rest', rest(-1)); part('dm_armr_rest', rest(1))

    # ---- the scythe (its joint is the grip, the shaft along +y): the black shaft with its wraps, the gold band, the blade sweeping
    #      out and back toward the butt with a pale edge, its heel standing up past the shaft, the crystal in golden claws, the crescent
    g = (0.0, 0.0, 0.0)
    sc = lambda fr, to, t, rot=None: _el(fr, to, t, g, rot)
    def blade_chain():
        # each segment starts where the last one ended; directions step down 22.5 degrees at a time (the most a model element
        # can turn), so it curves out from the socket, down, and back in toward the shaft: (direction, length, thickness)
        out, (px, py) = [], (0.3, 20.4)
        for k, (ang, ln, th) in enumerate(((0, 5.2, 3.4), (-22.5, 4.8, 3.0), (-45, 4.8, 2.6), (-67.5, 5.0, 2.2), (-90, 4.6, 1.7), (-112.5, 3.4, 1.1))):
            a = math.radians(ang)
            if ang >= -45:                                         # (a box long in x, turned by ang; its lower face the edge)
                fr, to, rot = (px - 0.3, py - th / 2, -0.2), (px + ln, py + th / 2, 0.2), ang
                efr, eto = (px - 0.3, py - th / 2 - 0.05, -0.26), (px + ln, py - th / 2 + 0.45, 0.26)
            else:                                                  # (long in y, pointing down, turned by ang + 90; its outer face the edge)
                fr, to, rot = (px - th / 2, py - ln, -0.2), (px + th / 2, py + 0.3, 0.2), ang + 90
                efr, eto = (px + th / 2 - 0.45, py - ln, -0.26), (px + th / 2 + 0.05, py + 0.3, 0.26)
            r = ('z', rot, (px, py, 0)) if rot else None
            out += [sc(fr, to, 'dm_blade', r), sc(efr, eto, 'dm_blade_lt', r)]
            px, py = px + ln * math.cos(a), py + ln * math.sin(a)
        return out
    scythe = [sc((-0.5, -14.6, -0.5), (0.5, 21.0, 0.5), 'dm_shaft'),
              sc((-0.62, -2.0, -0.62), (0.62, -1.2, 0.62), 'dm_cuff'), sc((-0.62, 1.4, -0.62), (0.62, 2.2, 0.62), 'dm_cuff'),   # the grip's wraps
              sc((-0.75, -15.4, -0.75), (0.75, -14.4, 0.75), 'dm_shaft'),                                 # the butt cap
              sc((-0.3, -17.0, -0.3), (0.3, -15.2, 0.3), 'dm_gold'),                                      # the crescent
              sc((-1.9, -17.6, -0.25), (1.9, -16.8, 0.25), 'dm_gold'),
              sc((-2.2, -17.2, -0.2), (-1.6, -15.6, 0.2), 'dm_gold', ('z', -22.5, (-1.9, -16.8, 0))),
              sc((1.6, -17.2, -0.2), (2.2, -15.6, 0.2), 'dm_gold', ('z', 22.5, (1.9, -16.8, 0))),
              sc((-0.7, 13.6, -0.7), (0.7, 15.6, 0.7), 'dm_gold'), sc((-0.75, 14.2, -0.75), (0.75, 15.0, 0.75), 'dm_gold_dk'),   # the band
              sc((-0.8, 19.4, -0.8), (0.8, 21.4, 0.8), 'dm_shaft'),                                       # the socket
              *blade_chain(),
              sc((-3.0, 19.8, -0.24), (0.6, 22.2, 0.24), 'dm_blade', ('z', -22.5, (0.4, 21.0, 0))),         # the heel, past the shaft
              sc((-0.9, 21.2, -0.9), (0.9, 22.4, 0.9), 'dm_gold'),                                        # the claws...
              sc((-1.9, 21.6, -0.3), (-0.8, 24.2, 0.3), 'dm_gold', ('z', 22.5, (-1.2, 21.8, 0))),
              sc((0.8, 21.6, -0.3), (1.9, 24.2, 0.3), 'dm_gold', ('z', -22.5, (1.2, 21.8, 0))),
              sc((-0.3, 21.6, -1.9), (0.3, 24.0, -0.8), 'dm_gold_dk', ('x', -22.5, (0, 21.8, -1.2))),
              sc((-0.3, 21.6, 0.8), (0.3, 24.0, 1.9), 'dm_gold_dk', ('x', 22.5, (0, 21.8, 1.2))),
              sc((-0.8, 22.2, -0.8), (0.8, 27.4, 0.8), 'dm_crystal'),                                     # ...and the crystal
              sc((-0.5, 27.2, -0.5), (0.5, 29.6, 0.5), 'dm_crystal'),
              sc((-0.25, 29.4, -0.25), (0.25, 30.8, 0.25), 'dm_crystal_lt')]
    for e in scythe:                                                                       # (built at 3/4: see SCYTHE_K)
        e['from'] = [round(8 + (v - 8) * SCYTHE_K, 4) for v in e['from']]; e['to'] = [round(8 + (v - 8) * SCYTHE_K, 4) for v in e['to']]
        if 'rotation' in e: e['rotation']['origin'] = [round(8 + (v - 8) * SCYTHE_K, 4) for v in e['rotation']['origin']]
    part('dm_scythe', scythe)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# Display frame (as Leo's): limb(side, fwd, out) swings a limb forward / out; torso(lean, tilt, turn). The scythe has its own
# turn, at his left fist: SHOULDER - across his shoulders, the head past his right shoulder, the blade hanging (the art);
# PLANTED - stood upright at his side, the blade turned outward; LEVEL - held out flat.
# A pose may swap parts for their second model (ALT): his left arm bent to rest the scythe on his shoulder; legs bent at the
# knee to kneel or sit.
I = (0.0, 0.0, 0.0, 1.0)
U = RIG_SCALE / 16
SHOULDER = qmul(qa('z', 70), qmul(qa('x', -20), qa('y', -40)))
PLANTED = qmul(qa('y', 180), qa('z', 4))
LEVEL = qmul(qa('x', 90), qa('y', 180))
def P(dy=0.0, cape=None, alt=None, slide=0.0, **parts):
    d = {k: I for k in PARTS}; d.update(parts); d['_dy'] = dy; d['_slide'] = slide        # (slide: his grip that far up the shaft)
    d['cape'] = cape if cape is not None else qa('x', -4)
    d['_alt'] = dict(alt or {})
    if 'scythe' not in parts: d['scythe'] = SHOULDER
    return d
def R(dy=0.0, cape=None, **parts):                                   # (resting: the scythe on his shoulder, his left arm bent)
    return P(dy, cape, alt={'arml': 'rest'}, **parts)
KNEEL = {'legr': 'bent', 'legl': 'bent'}
VIGIL = dict(KNEEL, arml='rest', armr='rest')                        # (kneeling, both fists on the planted shaft)
POSES = {
    'idle_a': R(body=torso(), head=torso(), arml=limb(-1, 10, 25), armr=limb(1, -4, 12)),
    'idle_b': R(0.012, body=torso(lean=-1.5), head=torso(lean=-3), legr=limb(1, 0, 3), legl=limb(-1, 0, 3), arml=limb(-1, 8, 25), armr=limb(1, -6, 14),
                cape=qa('x', -6)),
    'idle_look': R(body=torso(turn=-6), head=qmul(qa('y', 26), qa('x', 4)), arml=limb(-1, 10, 25), armr=limb(1, -4, 12)),
    # walk: a heavy, deliberate stride, the cloak swinging, the scythe on his shoulder, his free (right) arm swinging
    'walk_a': R(body=torso(tilt=2, turn=5), head=torso(turn=-4), legr=limb(1, 22), legl=limb(-1, -22), arml=limb(-1, 8, 25), armr=limb(1, -20, 10),
                cape=qa('x', -14)),
    'walk_up': R(0.04, body=torso(), legr=limb(1, 3), legl=limb(-1, -3), arml=limb(-1, 10, 25), armr=limb(1, 0, 10), cape=qa('x', -10)),
    'walk_b': R(body=torso(tilt=-2, turn=-5), head=torso(turn=4), legr=limb(1, -22), legl=limb(-1, 22), arml=limb(-1, 12, 25), armr=limb(1, 20, 10),
                cape=qa('x', -14)),
    # run: leaning in, the scythe trailing low behind him in his left hand, the cloak flying out
    'run_a': P(0.02, body=torso(lean=12, tilt=3), head=torso(lean=-10), legr=limb(1, 44), legl=limb(-1, -42), arml=limb(-1, -34, 12), armr=limb(1, 40, 12),
               scythe=qmul(qa('x', 120), qa('y', 180)), cape=qa('x', -40)),
    'run_up': P(0.1, body=torso(lean=12), head=torso(lean=-10), legr=limb(1, 10), legl=limb(-1, -28), arml=limb(-1, -30, 12), armr=limb(1, 0, 16),
                scythe=qmul(qa('x', 116), qa('y', 180)), cape=qa('x', -46)),
    'run_b': P(0.02, body=torso(lean=12, tilt=-3), head=torso(lean=-10), legr=limb(1, -42), legl=limb(-1, 44), arml=limb(-1, -38, 12), armr=limb(1, -40, 12),
               scythe=qmul(qa('x', 124), qa('y', 180)), cape=qa('x', -40)),
    'jump': R(body=torso(lean=8), head=torso(lean=-10), legr=limb(1, 30), legl=limb(-1, -36), arml=limb(-1, 14, 30), armr=limb(1, 20, 40), cape=qa('x', -30)),
    # the vigil (the storm encounter, as the sketch): down on his left knee, the right foot planted before him, both fists high on
    # the shaft of the scythe stood upright in front of his left shoulder - the blade over his head - and his eyes straight ahead
    'kneel': P(-0.5, alt=VIGIL, slide=10.0, body=torso(lean=6), head=I, legr=limb(1, 76, 4), legl=limb(-1, -14, 3),
               arml=limb(-1, 70, 2), armr=limb(1, 74, -34), scythe=PLANTED, cape=qa('x', -26)),
    'kneel_b': P(-0.495, alt=VIGIL, slide=10.0, body=torso(lean=5), head=qa('x', -2), legr=limb(1, 76, 4), legl=limb(-1, -14, 3),
                 arml=limb(-1, 68, 2), armr=limb(1, 72, -34), scythe=PLANTED, cape=qa('x', -24)),
    # sitting (right-click him): on the ground, knees up, the scythe stood upright at his left side in his left hand
    'sit_a': P(-0.6, alt=KNEEL, body=torso(lean=-6), head=torso(lean=2), legr=limb(1, 66, 8), legl=limb(-1, 60, 8), arml=limb(-1, 14, 22), armr=limb(1, 56, 4),
               scythe=PLANTED, cape=qa('x', 22)),
    'sit_b': P(-0.59, alt=KNEEL, body=torso(lean=-8), head=qmul(qa('y', -12), qa('x', 0)), legr=limb(1, 66, 8), legl=limb(-1, 60, 8), arml=limb(-1, 12, 22),
               armr=limb(1, 54, 4), scythe=PLANTED, cape=qa('x', 22)),
    'sit_look': P(-0.6, alt=KNEEL, body=torso(lean=-6, turn=6), head=qmul(qa('y', 30), qa('x', -4)), legr=limb(1, 66, 8), legl=limb(-1, 60, 8),
                  arml=limb(-1, 14, 22), armr=limb(1, 56, 4), scythe=PLANTED, cape=qa('x', 22)),
    # arriving: the butt of the scythe slammed into the ground at his side, chin up
    'plant': P(body=torso(lean=-3), head=torso(lean=-8), legr=limb(1, 10, 4), legl=limb(-1, -8, 4), arml=limb(-1, 22, 16), armr=limb(1, -8, 14), scythe=PLANTED,
               cape=qa('x', -12)),
    # the heavy swing (slow): hauled back over his left shoulder in both hands - then round in a great flat arc
    'swing_back': P(-0.04, body=torso(lean=-8, turn=30), head=torso(turn=-20), legr=limb(1, 22, 8), legl=limb(-1, -16, 8), arml=limb(-1, 150, 40),
                    armr=limb(1, 150, -10), scythe=qmul(qa('y', 90), qa('x', -40)), cape=qa('x', -10)),
    'swing': P(-0.08, body=torso(lean=12, turn=-40), head=torso(lean=-6, turn=30), legr=limb(1, 30, 10), legl=limb(-1, -26, 10), arml=limb(-1, 84, -30),
               armr=limb(1, 84, 24), scythe=qmul(qa('y', -90), LEVEL), cape=qa('x', -22)),
    # the spin (the charged attack): both arms out, the scythe held level - the whole rig turns about him
    'spin': P(0.04, body=torso(lean=4), head=torso(lean=-4), legr=limb(1, 6, 12), legl=limb(-1, -6, 12), arml=limb(-1, 84, -40), armr=limb(1, 84, -20),
              scythe=LEVEL, cape=qa('x', -50)),
    # the slam: the scythe raised overhead in both hands - then brought down into the ground with everything he has
    'overhead': P(0.06, body=torso(lean=-12), head=torso(lean=-14), legr=limb(1, 14, 8), legl=limb(-1, -8, 8), arml=limb(-1, 170, 6), armr=limb(1, 166, -6),
                  scythe=qa('x', -20), cape=qa('x', -18)),
    'slam': P(-0.3, body=torso(lean=30), head=torso(lean=-20), legr=limb(1, 50, 8), legl=limb(-1, -30, 8), arml=limb(-1, 60, 4), armr=limb(1, 56, -4),
              scythe=qa('x', 100), cape=qa('x', -8)),
    # beaten in a duel: down on his left knee, leaning on the scythe
    'yield': P(-0.47, alt=KNEEL, body=torso(lean=22), head=torso(lean=28), legr=limb(1, 82, 2), legl=limb(-1, -6, 3), arml=limb(-1, 40, 14), armr=limb(1, 46, 2),
               scythe=qmul(qa('y', 180), qmul(qa('z', -8), qa('x', 14))), cape=qa('x', 8)),
}


def _off(a, b):
    """design offset a -> b in the display frame"""
    return (-(b[0] - a[0]) * U, (b[1] - a[1]) * U, -(b[2] - a[2]) * U)


def part_xf(pose, p):
    """(left_rotation, translation) for part p: the scythe stands at his right fist wherever the arm carries it (its own turn);
    the cloak hangs from the back of his neck and leans with his torso. Every other part stands at its own joint."""
    dy = pose['_dy']
    if p == 'scythe':
        e = _qrot(pose['arml'], _off(PIVOT['arml'], GRIP_REST if pose['_alt'].get('arml') == 'rest' else GRIP))
        sl = _qrot(pose['scythe'], (0.0, -pose['_slide'] * U, 0.0))                     # (gripped further up: the scythe slides down)
        return pose['scythe'], (e[0] + sl[0], e[1] + dy + sl[1], e[2] + sl[2])
    if p == 'cape':
        e = _qrot(pose['body'], _off(PIVOT['body'], PIVOT['cape']))
        o = _off(PIVOT['body'], PIVOT['cape'])
        return qmul(pose['body'], pose['cape']), (e[0] - o[0], e[1] - o[1] + dy, e[2] - o[2])
    return pose[p], (0.0, dy, 0.0)


def joint(p):
    return PIVOT['arml' if p == 'scythe' else p]


def seal_icon(R):
    """Democratus' Storm Seal: the green crystal of his scythe in its golden claws, a spark round it"""
    return R.grid(['................', '.......L........', '......LGL.......', '...Y..GGG..Y....', '...YY.GLG.YY....', '....YYGGGYY.....',
                   '.....YGGGY......', '.....YGDGY......', '......YDY.......', '......YYY.......', '.......K........', '.......K.....w..',
                   '.......K....w...', '...w...K...w....', '..w....K........', '.......K........'],
                  dict(L='#8af070', G='#3fbf3a', D='#1c8428', Y='#f0cf4a', K='#1c2220', w='#e8fff0'))


def scythe_icon(R):
    """the scythe in the inventory: the curved teal blade, the black shaft, the green crystal"""
    return R.grid(['............LL..', '.....bbbbbbGGL..', '...bbtttttbYG...', '..btttTTTTKY....', '.btt......KY....', '.bt......K......',
                   'bt......K.......', 'bt.....K........', 'b.....K.........', 'b....K..........', '....K...........', '...K............',
                   '..K.............', '.Y..............', 'YY..............', '................'],
                  dict(L='#8af070', G='#3fbf3a', Y='#f0cf4a', K='#1c2220', b='#97a3ab', t='#78c2ae', T='#d6eef0'))
