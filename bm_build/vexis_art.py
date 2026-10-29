"""ADMIRAL VEXIS, VOICE OF THE HIVE (draft art): the boss of the Vorn Armada (previews/v299_armada/PLAN.md) - once a single Vorn,
one of the first the hive "improved"; now the voice every ship and trooper answers. It waits at the helm of the Hive-Throne
inside its warframe, the red star filling the window behind it. Beaten, the hive-link is cut, and it follows you: an endgame
follower (phase242 the fight, phase243 the follower; armada_lore the words).

THE LOOK - A VORN, an elder and an admiral: the pack's own Vorn (phase32/phase45's troopers, phase25.donado_parts in Vorn colours)
grown tall and regal, in their textures' style and colours (phase32.textures: vorn_skin (122,110,140), vorn_dark (40,34,52),
vorn_eye (60,255,80) with its pale glint, vorn_armor (34,36,40) with the green stripe, the warlord's vorn_armor_red (40,22,24)
with the (255,70,60) stripe) - each a flat colour, every texel nudged (_vorn). The troopers' SQUARE HEAD: the dark muzzle with
its green nose and smile (an elder's beard under it), square glowing-green eyes with the dark pupil at their outer top, long dark
ears hanging past the jaw, and THE VORN'S TWO ANTENNAE (dark stalks, froglight tips) standing tall out of an admiral's circlet
with a crown of lesser ones; the troopers' black armour for a long tunic (the green stripe round the waist, the ragged hem), dark
gloves and boots; the warlord's red armour for the epaulets, the tabard and the ragged command mantle (#ff463c stripe at the hem).
The hive's work on it in gunmetal (sprites280e's VORN ramp) and green light: the gorget, the node in its breast, the bracers, the
ports in its skull and spine with cables between. The WARFRAME is Vorn tech in the same language: gunmetal plate in panels and
rivets, warplate-red stripes (#d83030) in chevrons and bands, the warlord's red armour on its pauldrons, the troopers' black-and-
green band for a belt, the Vorn's two froglight-tipped antennae on its head (and on its masts), dark ear-plates - and a Vorn at
the helm in its cockpit. Donadian teal is the OTHER aliens' colour: it appears only as the patches the follower's mantle was
mended with.

ITS FORMS (pose key _form; every part swaps model per form - model_name):
  warframe  PHASE 1. A colossal battle-mech, ~12 blocks to its hull's top (~13.5 to its masts) at BOSS_SCALE - a little under
            the armored Sovereign: a top-heavy armoured hull, a glass cockpit dome in the chest (a Vorn at the helm inside,
            lit green from behind), a low sensor head with one green visor bar, a heavy plasma cannon for a right arm (green
            coils, a glowing bore), a three-claw manipulator for a left, missile pods on its shoulders (_pods 'open': hatches
            up, warheads out), a reactor glowing in its abdomen, a backpack with thrusters and comms masts, and DIGITIGRADE legs
            (thigh forward, shin back, a metatarsus and a big three-toed foot). _power 0..3 lights it section by section for
            the entrance (0: dark; 1: the reactor; 2: the hull and cockpit; 3: the cannon and the backpack - the default).
  hivelink  PHASE 2. Vexis, out of the torn warframe: ~8 blocks to the skull (~9.3 to the antennae' tips), HOVERING (its toes
            HOVER design units off the deck), tall, long-armed, legs atrophied in cybernetic braces, the mantle hanging by the
            world's down, TWO GRAVITY RINGS orbiting it (ring1, ring2: green energy bands with gunmetal nodes - each pose
            turns them, so they orbit as it moves).
  starfire  PHASE 3. The star's fire in it (1.15 x the hive-link: ~9 blocks to the skull): the skin cracked with star-fire, the
            eyes blazing white-gold, the rings burning, a halo of solar flare behind the skull, the mantle's hem burning.
  unlinked  THE FOLLOWER (~2.3 blocks at FOLLOWER_SCALE): the hive-link cut - the skull cables severed (frayed ends, bare
            wire), the implants dark, the eyes a calm green, the mantle mended with Donadian patches, ONE small gravity ring.
EVERY BOSS FORM IS ALSO A FOLLOWER, at two sizes: COMPANION (COMPANION_SCALE[form], in place of BOSS_SCALE * FORM_SCALE) and FULL
(BOSS_SCALE * FORM_SCALE). The follower drives it with BOSS_POSES[form] alone: FOLLOW_KEYS - idle_a, idle_b, walk_0..3, sit_a and
sit_b (resting and its breath: the warframe down on one knee, idling, its visor lit; Vexis floating cross-legged, the rings
slowed), happy and hurt.

ONE RIG, TWO SKELETONS. Every form has the same PARTS, but the warframe and the alien have different joints (JOINTS): PIVOT is
the warframe's (where every display stands at rest); an alien pose carries '_o_<part>' shifts (rigkit) that put each joint where
the alien's skeleton has it - fit() solves them from the pose's turns, so rigfol.place/pose/cycles and rigpet drive both
unchanged (an alien part's model is built about its own joint). The parts a form doesn't use are HIDDEN (scale 0): the pods
for Vexis, the rings for the warframe, ring2 for the follower.

FACES (_face): narrowed, wide, dim, closed, soft. The warframe's visor bar (soft -> default; closed = powered down); Vexis's
eyes (the hive's green, the star's white-gold, the follower's calm green). A copy of phase239 maps the moods:
FACE = {'happy': 'soft', 'surprised': 'wide', 'hurt': 'dim', 'sleepy': 'closed', 'blink': 'closed', 'squint': 'narrowed',
'serious': 'narrowed'}.
FX (_fx; shown only when a pose asks): on the head (fx) - charge, beam (the improvement beam, from the eyes), bolt (the
follower's), scan (the warframe's targeting fan), sparks (the link burning out); in the right hand / at the cannon's muzzle
(fxh) - plasma_c, plasma (the cannon's sweep), well (a gravity well), sun (a star gathered in the palm), lance (the solar
lance), flare (the star-flare's fan), deflect (the follower's deflector).

SCALE (one rig, three sizes):
  RIG_SCALE = FOLLOWER_SCALE (0.86: about 2.3 blocks to the antennae' tips, 1.9 to the skull) - rigpet's, with POSES (form
  'unlinked').
  BOSS_SCALE (4.0) x FORM_SCALE[form] (warframe 1.0, hivelink 0.85, starfire 0.98) - the boss's, with BOSS_POSES[form][name].
  COMPANION_SCALE[form] (warframe 1.14, hivelink 1.31, starfire 1.4) - a boss form as a companion, with BOSS_POSES[form].
  scale_of(pose) gives the boss's or the follower's; companion_scale(form) the companion's.

THE RIG (rigkit): body (the root: the pelvis - the reactor; Vexis's hips and tabard), chest (the hull and cockpit; the torso),
head (a model per form x face), arms (armr/arml: the pauldron and upper arm; forer: the cannon / a forearm and hand; forel:
the claw / a forearm and hand), legs (thigh, shin, foot each side), podr/podl (the missile pods), back (the backpack; the
mantle), ring1/ring2 (the gravity rings, on the body), fx (on the head) and fxh (on the right forearm): 20 displays. Design
units: feet at y=0, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import qs, el, seg, shrink, D, qrot

PREFIX = 'vx_'
FOLLOWER_SCALE = 0.86
RIG_SCALE = FOLLOWER_SCALE                     # (the follower's: POSES are the follower's)
BOSS_SCALE = 4.0
FORM_SCALE = {'warframe': 1.0, 'hivelink': 0.85, 'starfire': 0.98}    # (starfire: the hive-link's x 1.15)
# a boss form as a COMPANION follower: the whole rig's scale (in place of BOSS_SCALE * FORM_SCALE[form]) for its own BOSS_POSES -
# the warframe ~3.5 blocks to the top of its hull (~3.85 to its masts), the hive-link ~3 to its skull (~3.6 to the antennae'
# tips), starfire ~3.2 (~4.1 to its halo); the FULL size is BOSS_SCALE * FORM_SCALE
COMPANION_SCALE = {'warframe': 1.14, 'hivelink': 1.31, 'starfire': 1.4}
FORMS = ('warframe', 'hivelink', 'starfire', 'unlinked')
ALIEN = ('hivelink', 'starfire', 'unlinked')
HOVER = 4.0                                    # (the boss's float: its toes this far off the deck, design units)
F_HOVER = 2.4                                  # (the follower's)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

# the warframe's joints (PIVOT: where every display stands at rest)
PIVOT = {'body': (0, 20.0, 0), 'chest': (0, 25.0, 0.5), 'head': (0, 42.0, -2.0),
         'armr': (13.5, 37.5, 0.5), 'forer': (14.5, 27.0, 0.5), 'arml': (-13.5, 37.5, 0.5), 'forel': (-14.5, 27.0, 0.5),
         'legr': (6.5, 19.0, 0.5), 'shinr': (7.0, 11.5, -4.0), 'footr': (7.0, 5.5, 3.5),
         'legl': (-6.5, 19.0, 0.5), 'shinl': (-7.0, 11.5, -4.0), 'footl': (-7.0, 5.5, 3.5),
         'podr': (9.2, 43.3, 3.5), 'podl': (-9.2, 43.3, 3.5), 'back': (0, 34.0, 7.0),
         'ring1': (0, 22.0, 0), 'ring2': (0, 22.0, 0), 'fx': (0, 44.9, -9.2), 'fxh': (14.5, 5.4, 0.5)}
PARENT = {'body': None, 'chest': 'body', 'head': 'chest', 'armr': 'chest', 'forer': 'armr', 'arml': 'chest', 'forel': 'arml',
          'legr': 'body', 'shinr': 'legr', 'footr': 'shinr', 'legl': 'body', 'shinl': 'legl', 'footl': 'shinl',
          'podr': 'chest', 'podl': 'chest', 'back': 'chest', 'ring1': 'body', 'ring2': 'body', 'fx': 'head', 'fxh': 'forer'}
PARTS = tuple(PIVOT)
# Vexis's own skeleton (hivelink, starfire, unlinked)
JA = {'body': (0, 13.0, 0), 'chest': (0, 14.5, 0), 'head': (0, 24.6, -0.4),
      'armr': (5.0, 22.4, 0.2), 'forer': (5.5, 13.6, 0.2), 'arml': (-5.0, 22.4, 0.2), 'forel': (-5.5, 13.6, 0.2),
      'legr': (2.0, 12.2, 0.2), 'shinr': (2.3, 7.4, -0.6), 'footr': (2.3, 3.0, 0.4),
      'legl': (-2.0, 12.2, 0.2), 'shinl': (-2.3, 7.4, -0.6), 'footl': (-2.3, 3.0, 0.4),
      'podr': (3.0, 22.0, 1.5), 'podl': (-3.0, 22.0, 1.5), 'back': (0, 23.0, 2.2),
      'ring1': (0, 16.0, 0), 'ring2': (0, 16.0, 0), 'fx': (0, 30.0, -3.6), 'fxh': (5.8, 3.2, -0.3)}
JOINTS = {'warframe': PIVOT, 'hivelink': JA, 'starfire': JA, 'unlinked': JA}
PODS = ('podr', 'podl')
RINGS = ('ring1', 'ring2')
FXP = ('fx', 'fxh')
PART_K = {'fx': 2.0, 'fxh': 2.0}               # (built at full size, kept inside the model box)
FACES = ('narrowed', 'wide', 'dim', 'closed', 'soft')
FX_HEAD = ('charge', 'beam', 'bolt', 'scan', 'sparks')
FX_HAND = ('plasma_c', 'plasma', 'well', 'sun', 'lance', 'flare', 'deflect')
POWER = {'body': 1, 'chest': 2, 'back': 3, 'forer': 3}          # (the warframe: the _power each part needs to be lit)

# ---- the palette (sprites280e's Vorn ramps; the Vorn skin; the star)
VORN = [(42, 46, 54), (68, 74, 86), (100, 108, 122), (138, 148, 162), (180, 188, 200)]
XEN = [(14, 90, 30), (30, 138, 46), (58, 200, 74), (122, 255, 106), (216, 255, 200)]
SKIN, SKIN_M, SKIN_D = (122, 110, 140), (100, 88, 118), (40, 30, 52)
RED, RED_H, RED_D, RED_A = (216, 48, 48), (255, 70, 60), (130, 22, 26), (40, 22, 24)
TEAL = (58, 216, 200)
FIRE, FIRE_L, FIRE_D, HOT, GOLD = (255, 106, 40), (255, 190, 80), (176, 34, 20), (255, 244, 206), (255, 214, 110)


# ---------------------------------------------------------------------------------------------------- names
def joints(form):
    return JOINTS.get(form, JA)


def _tag(p, form):
    if form == 'warframe': return 'w'
    if form == 'starfire': return 's'
    if form == 'unlinked' and p in ('chest', 'back', 'ring1'): return 'u'
    return 'h'


def face_of(pose):
    form, f = pose.get('_form', 'unlinked'), pose.get('_face')
    f = {'blink': 'closed'}.get(f, f)
    if form == 'warframe' and f == 'soft': f = None
    return f if f in FACES else None


def HIDDEN(p, pose):
    form = pose.get('_form', 'unlinked')
    if p == 'fx': return pose.get('_fx') not in FX_HEAD
    if p == 'fxh': return pose.get('_fx') not in FX_HAND
    if p in PODS: return form != 'warframe'
    if p in RINGS: return form == 'warframe' or (form == 'unlinked' and p == 'ring2') or p in pose.get('_hide', ())
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    form = pose.get('_form', 'unlinked')
    if p == 'head':
        f = face_of(pose)
        if form == 'warframe' and pose.get('_power', 3) < 1: f = 'closed'
        return f'{PREFIX}head_{form}{"_x" + f if f else ""}{suffix}'
    if p in FXP:
        k = pose.get('_fx'); ks = FX_HEAD if p == 'fx' else FX_HAND
        return f'{PREFIX}{p}_{k if k in ks else ks[0]}{suffix}'
    if p in PODS:
        return f'{PREFIX}{p}_{"open" if pose.get("_pods") == "open" and form == "warframe" else "shut"}{suffix}'
    dark = '_off' if form == 'warframe' and pose.get('_power', 3) < POWER.get(p, 0) else ''
    return f'{PREFIX}{p}_{_tag(p, form)}{dark}{suffix}'


def companion_scale(form):
    """the whole rig's display scale for a boss form as a companion follower"""
    return COMPANION_SCALE[form]


def scale_of(pose):
    """the display scale to show a pose at: the follower's for its own poses, the boss's (by form) for BOSS_POSES"""
    form = pose.get('_form', 'unlinked')
    return RIG_SCALE if form == 'unlinked' else BOSS_SCALE * FORM_SCALE[form]


# ---------------------------------------------------------------------------------------------------- textures (2 px cells: half a design unit)
def _c(col, k=1.0, add=0, a=255):
    return tuple(max(0, min(255, int(v * k + add))) for v in col[:3]) + (a,)


def _cells(base, seed, var=0.10, size=64, cz=2, dark=0.08, light=0.05, add=5):
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im)
    for cy in range(0, size, cz):
        for cx in range(0, size, cz):
            k = 1 + rnd.uniform(-var, var); a = rnd.uniform(-add, add); q = rnd.random()
            if q < dark: k *= 0.78; a -= 3
            elif q < dark + light: k *= 1.18; a += 4
            d.rectangle((cx, cy, cx + cz - 1, cy + cz - 1), fill=_c(base, k, a))
    return im


def _sq(d, x, y, col, cz=2):
    d.rectangle((x, y, x + cz - 1, y + cz - 1), fill=_c(col))


def _crack(d, rnd, size, n=None, col=FIRE, hot=FIRE_L, lip=SKIN_D, x=None, y=None, branch=0.2):
    """a crack of light, in cells: a dark lip to its left, branching as it runs down"""
    x = rnd.randrange(0, size, 2) if x is None else x; y = rnd.randrange(0, size, 2) if y is None else y
    for i in range(n or rnd.randint(5, 11)):
        _sq(d, (x - 2) % size, y, lip)
        _sq(d, x, y, hot if (i == 0 or rnd.random() < 0.2) else col)
        if rnd.random() < branch: _crack(d, rnd, size, rnd.randint(2, 4), col, hot, lip, (x + rnd.choice((-2, 2))) % size, y, 0)
        x = (x + rnd.choice((-2, 0, 0, 2))) % size; y = (y + 2) % size


def _hull(seed, base=VORN[1], lip=VORN[2], seam=VORN[0], scuff=VORN[3]):
    """gunmetal plate: panels (a lit lip on top, a dark seam under, staggered joints), rivets in pairs, scuffs and grime"""
    rnd = random.Random(seed); im = _cells(base, seed, 0.06, dark=0.06, light=0.04, add=3); d = ImageDraw.Draw(im)
    for by in range(0, 64, 16):
        d.rectangle((0, by, 63, by + 1), fill=_c(lip)); d.rectangle((0, by + 14, 63, by + 15), fill=_c(seam))
        x0 = rnd.randrange(6, 26, 2)
        for x in (x0, x0 + rnd.randrange(18, 30, 2)):
            if x < 62: d.rectangle((x, by + 2, x + 1, by + 13), fill=_c(seam)); d.rectangle((x + 2, by + 2, x + 2, by + 13), fill=_c(lip))
        for x in (rnd.randrange(2, 60, 2),):
            _sq(d, x, by + 4, scuff); _sq(d, x, by + 10, scuff)                                   # (rivets)
    for _ in range(5):                                                                             # (scuffs)
        x, y = rnd.randrange(0, 56, 2), rnd.randrange(0, 62, 2)
        d.rectangle((x, y, x + rnd.choice((4, 6, 8)), y), fill=_c(scuff, 0.92))
    for _ in range(6): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), _c(seam, 0.85)[:3])  # (grime)
    return im


def _red(seed):
    """warplate red: the hive's stripes - lit along the top, a darker seam, a hex-cell grain"""
    rnd = random.Random(seed); im = _cells(RED, seed, 0.07, dark=0.05, light=0.05, add=4); d = ImageDraw.Draw(im)
    for by in range(0, 64, 8):
        d.rectangle((0, by, 63, by), fill=_c(RED_H)); d.rectangle((0, by + 7, 63, by + 7), fill=_c(RED_D))
    for _ in range(10): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (240, 90, 80))
    return im


def _glow(base, hi, seed, p=0.22, var=0.06):
    rnd = random.Random(seed); im = _cells(base, seed, var, dark=0.03, light=0.0, add=4); d = ImageDraw.Draw(im)
    for _ in range(int(p * 1024)):
        _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), hi)
    return im


def _visor():
    """the visor bar: a hot core line along it, scan ticks"""
    im = _cells(XEN[3], 301, 0.05, dark=0.0, light=0.0); d = ImageDraw.Draw(im)
    for y in range(0, 64, 4):
        d.rectangle((0, y + 1, 63, y + 2), fill=_c(XEN[4]))
    for x in range(0, 64, 10): d.rectangle((x, 0, x + 1, 63), fill=_c(XEN[2]))
    return im


def _vent(seed):
    im = _cells(VORN[0], seed, 0.05, add=2); d = ImageDraw.Draw(im)
    for y in range(0, 64, 4):
        d.rectangle((0, y, 63, y + 1), fill=_c((14, 16, 20))); d.rectangle((0, y + 2, 63, y + 2), fill=_c(VORN[2]))
    return im


def _glass(dark=False):
    """the cockpit's glass: green-tinted, see-through, a streak of light across it"""
    im = Image.new('RGBA', (64, 64), (60, 170, 90, 40) if not dark else (20, 40, 30, 120)); d = ImageDraw.Draw(im)
    for k, w in ((-30, 5), (-18, 2)):
        d.line((k, 64, k + 64, 0), fill=(200, 255, 210, 110) if not dark else (60, 80, 70, 140), width=w)
    d.rectangle((0, 0, 63, 1), fill=(150, 220, 160, 170)); d.rectangle((0, 62, 63, 63), fill=(20, 60, 30, 170))
    return im


def _cockpit(lit=True):
    """the cockpit's back wall: the green light behind the pilot (its silhouette stands against it)"""
    if not lit: return _cells((22, 30, 26), 311, 0.05, add=2)
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im)
    for y in range(64):
        t = abs(y - 28) / 36
        col = tuple(int(XEN[4][i] * (1 - t) + XEN[2][i] * t) for i in range(3))
        d.line((0, y, 63, y), fill=col + (255,))
    rnd = random.Random(312)
    for _ in range(60): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), XEN[4] if rnd.random() < 0.3 else XEN[2])
    for y in range(6, 64, 12): d.rectangle((0, y, 63, y), fill=_c(XEN[1]))
    return im


def _disc(cols, size=32, ring=None, crack=False):
    """a round light (whole uv): bands from outside in; ring: a gunmetal rim"""
    im = Image.new('RGBA', (size, size), _c(ring or cols[0])); d = ImageDraw.Draw(im); c = size / 2
    n = len(cols)
    for i, col in enumerate(cols):
        r = (c - 1) * (1 - i / (n + 0.4))
        d.ellipse((c - r, c - r, c + r - 1, c + r - 1), fill=_c(col))
    if crack:
        d.line((4, 6, 14, 15, 12, 22, 26, 28), fill=_c((10, 8, 12)), width=2)
    return im.resize((64, 64), Image.NEAREST)


def _implant(seed, lit=True):
    rnd = random.Random(seed); im = _hull(seed, VORN[2], VORN[3], VORN[0], VORN[4]); d = ImageDraw.Draw(im)
    for _ in range(10):
        _sq(d, rnd.randrange(0, 64, 4), rnd.randrange(0, 64, 4), XEN[3] if lit else (40, 52, 46))
    return im


def _cable(seed, glow=XEN[2], base=(30, 26, 38)):
    im = _cells(base, seed, 0.08); d = ImageDraw.Draw(im)
    for y in range(0, 64, 4):
        d.rectangle((0, y, 63, y), fill=_c(VORN[1]))
    for y in range(2, 64, 12):
        for x in range(0, 64, 8): _sq(d, x, y, glow)
    return im


def _wire():
    im = _cells((150, 92, 52), 331, 0.12); d = ImageDraw.Draw(im)
    for x in range(0, 64, 6): d.rectangle((x, 0, x + 1, 63), fill=_c((70, 70, 82)))
    return im


def _mantle(seed, embers=0):
    """the command mantle: Vorn red-black cloth in vertical folds; star: embers in it"""
    rnd = random.Random(seed); im = _cells(RED_A, seed, 0.08, dark=0.06, light=0.03, add=3); d = ImageDraw.Draw(im)
    for x in range(0, 64, 8):
        d.rectangle((x, 0, x + 1, 63), fill=_c((62, 34, 38))); d.rectangle((x + 2, 0, x + 3, 63), fill=_c((22, 11, 13)))
    for _ in range(embers): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), FIRE if rnd.random() < 0.7 else FIRE_L)
    return im


def _mantle_trim(seed):
    """the mantle's trim: the hive's red stripe (#ff463c) on the red-black"""
    im = _mantle(seed); d = ImageDraw.Draw(im)
    d.rectangle((0, 20, 63, 43), fill=_c(RED_H)); d.rectangle((0, 20, 63, 21), fill=_c((255, 130, 110)))
    d.rectangle((0, 42, 63, 43), fill=_c((150, 30, 30)))
    return im


def _patch():
    """the Donadian patch the follower's mantle was mended with: teal, a pale stitched border, their circle sign"""
    im = _cells(TEAL, 341, 0.06, dark=0.05, light=0.03, add=3); d = ImageDraw.Draw(im)
    for x in range(4, 60, 6):
        d.rectangle((x, 3, x + 2, 4), fill=_c((232, 244, 236))); d.rectangle((x, 59, x + 2, 60), fill=_c((232, 244, 236)))
    for y in range(4, 60, 6):
        d.rectangle((3, y, 4, y + 2), fill=_c((232, 244, 236))); d.rectangle((59, y, 60, y + 2), fill=_c((232, 244, 236)))
    d.ellipse((20, 20, 43, 43), outline=_c((26, 140, 130)), width=3); d.ellipse((29, 29, 34, 34), fill=_c((26, 140, 130)))
    return im


def _vorn(base, var, seed, cz=2, size=64):
    """the Vorn's own texture style (phase32.textures: vorn_skin, vorn_dark, vorn_armor): a flat colour, every texel nudged by
    +-var - here in half-unit cells"""
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im)
    for y in range(0, size, cz):
        for x in range(0, size, cz):
            n = rnd.randrange(-var, var + 1)
            d.rectangle((x, y, x + cz - 1, y + cz - 1), fill=tuple(max(0, min(255, c + n)) for c in base) + (255,))
    return im


VSKIN, VDARK, VEYE, VARM, VARM_R = (122, 110, 140), (40, 34, 52), (60, 255, 80), (34, 36, 40), (40, 22, 24)
VSTRIPE, VSTRIPE_R, FROG = (90, 255, 110), (255, 70, 60), (215, 238, 213)


def _vstar_skin(seed, base=VSKIN, cracks=8):
    """starfire: the Vorn skin, cracked with the star's fire"""
    rnd = random.Random(seed); im = _vorn(base, 10, seed); d = ImageDraw.Draw(im)
    for _ in range(cracks): _crack(d, rnd, 64, rnd.randint(9, 16), FIRE_L, HOT, (40, 16, 22), branch=0.35)
    return im


def _frog():
    """the antennae's tips: the Vorn troopers' verdant froglight - pale mint, greener at the edge"""
    im = _vorn((228, 246, 228), 8, 2141, 4); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 3), fill=_c((160, 211, 155))); d.rectangle((0, 60, 63, 63), fill=_c((160, 211, 155)))
    d.rectangle((0, 0, 3, 63), fill=_c((189, 225, 183))); d.rectangle((60, 0, 63, 63), fill=_c((189, 225, 183)))
    return im


def _eye(kind=None, pal='hive'):
    """a Vorn eye (whole uv): the troopers' glowing square (phase32 vorn_eye: (60,255,80), +-18, a pale glint at its top-left),
    a texel to a quarter of it. pal: hive (the Vorn green), star (blazing white-gold), calm (the follower: the same green,
    softer); dim: gone dark"""
    base, var, gl = {'hive': (VEYE, 18, (230, 255, 230)), 'star': ((255, 226, 140), 14, (255, 255, 240)), 'calm': ((88, 236, 108), 14, (226, 255, 226))}[pal]
    if kind == 'dim': base, gl = ({'hive': (20, 96, 30), 'star': (150, 60, 24), 'calm': (24, 90, 34)}[pal], None)
    im = _vorn(base, var, 2150 + len(pal), 8)
    if pal == 'star' and kind != 'dim':
        d = ImageDraw.Draw(im); d.rectangle((16, 16, 47, 47), fill=_c(HOT)); d.rectangle((24, 24, 39, 39), fill=_c((255, 255, 255)))
    if gl:
        d = ImageDraw.Draw(im)
        for (x, y) in ((8, 8), (16, 8), (8, 16)): d.rectangle((x, y, x + 7, y + 7), fill=_c(gl))
    return im


def _missile():
    im = _cells(RED, 351, 0.06); d = ImageDraw.Draw(im)
    d.rectangle((0, 40, 63, 47), fill=_c((220, 224, 230))); d.rectangle((20, 0, 43, 12), fill=_c(RED_H))
    return im


def _void(seed):
    rnd = random.Random(seed); im = _cells((8, 10, 12), seed, 0.2, add=2); d = ImageDraw.Draw(im)
    for _ in range(26): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (20, 60, 30))
    return im


def _shield():
    im = Image.new('RGBA', (64, 64), (60, 220, 90, 80)); d = ImageDraw.Draw(im)
    for k in range(0, 64, 12):
        d.line((k, 0, k, 63), fill=(170, 255, 180, 170), width=1); d.line((0, k, 63, k), fill=(170, 255, 180, 170), width=1)
    return im


def textures():
    T = {'vx_hull': _hull(2101), 'vx_hull_l': _hull(2102, VORN[2], VORN[3], VORN[1], VORN[4]), 'vx_hull_d': _hull(2103, VORN[0], VORN[1], (22, 24, 30), VORN[2]),
         'vx_red': _red(2104), 'vx_vent': _vent(2105), 'vx_visor': _visor(),
         'vx_glow': _glow(XEN[2], XEN[3], 2106), 'vx_glow_l': _glow(XEN[3], XEN[4], 2107, 0.3), 'vx_glow_d': _glow(XEN[0], XEN[1], 2108),
         'vx_off': _glow((30, 38, 34), (40, 52, 46), 2109), 'vx_glass': _glass(), 'vx_glass_off': _glass(True),
         'vx_cockpit': _cockpit(), 'vx_cockpit_off': _cockpit(False), 'vx_pilot': _cells((20, 16, 28), 2110, 0.06),
         'vx_reactor': _disc([XEN[1], XEN[2], XEN[3], XEN[4], (255, 255, 255)], ring=VORN[0]),
         'vx_reactor_off': _disc([(24, 30, 28), (34, 44, 38), (30, 40, 34)], ring=VORN[0]),
         'vx_missile': _missile(),
         'vx_skin': _vorn(VSKIN, 10, 2111), 'vx_skin_d': _vorn(VDARK, 5, 2112), 'vx_skin_s': _vstar_skin(2113, cracks=4),
         'vx_skin_sd': _vstar_skin(2114, (52, 36, 54), 6),
         'vx_varmor': _vorn(VARM, 6, 2142), 'vx_varmor_r': _vorn(VARM_R, 6, 2143), 'vx_vstripe': _vorn(VSTRIPE, 8, 2144, 4),
         'vx_vstripe_r': _vorn(VSTRIPE_R, 8, 2145, 4), 'vx_frog': _frog(),
         'vx_implant': _implant(2115), 'vx_implant_off': _implant(2116, False),
         'vx_cable': _cable(2117), 'vx_cable_s': _cable(2118, FIRE_L, (70, 24, 14)), 'vx_cable_u': _cable(2119, (52, 60, 56)), 'vx_wire': _wire(),
         'vx_mantle': _mantle(2120), 'vx_mantle_r': _mantle_trim(2121), 'vx_mantle_s': _mantle(2122, 70), 'vx_patch': _patch(),
         'vx_ring': _glow(XEN[2], XEN[4], 2123, 0.18), 'vx_ring2': _glow(XEN[3], XEN[4], 2124, 0.3),
         'vx_fire': _glow(FIRE, FIRE_L, 2125, 0.3, 0.1), 'vx_fire_l': _glow(FIRE_L, HOT, 2126, 0.3), 'vx_fire_d': _glow(FIRE_D, FIRE, 2127, 0.2, 0.1),
         'vx_hot': _glow(HOT, (255, 255, 255), 2128, 0.3),
         'vx_node': _disc([VORN[2], XEN[1], XEN[3], XEN[4]], ring=VORN[0]), 'vx_node_s': _disc([FIRE_D, FIRE, FIRE_L, HOT], ring=(60, 30, 20)),
         'vx_node_u': _disc([VORN[1], (40, 52, 46), (52, 66, 58)], ring=VORN[0], crack=True),
         'vx_void': _void(2129), 'vx_shield': _shield()}
    for pal in ('hive', 'star', 'calm'):
        T[f'vx_eye_{pal}'] = _eye(None, pal); T[f'vx_eye_{pal}_dim'] = _eye('dim', pal)
    return T


# ---------------------------------------------------------------------------------------------------- building helpers
NOSHIFT = {'vx_reactor', 'vx_reactor_off', 'vx_node', 'vx_node_s', 'vx_node_u', 'vx_patch'}
_rs = random.Random(5)
_PV = [None]


def E(fr, to, tex, pv=None, light=0, **kw):
    """an element (rigkit.el), its texture window shifted at random so neighbouring boxes don't repeat the same patch (pv: the
    part's joint - by default the part being built, in its form's skeleton)"""
    pv = pv or _PV[0]
    if tex not in NOSHIFT and not tex.startswith('vx_eye') and 'shift' not in kw and 'uv' not in kw: kw['shift'] = (_rs.random(), _rs.random())
    return el(fr, to, tex, pv, light=light, **kw)


def BX(sx, x0, x1, y0, y1, z0, z1, tex, pv=None, **kw):
    """a box on side sx (+1 its right, -1 its left): x given for the right side, mirrored (a z turn mirrored with it)"""
    a, b = sorted((sx * x0, sx * x1))
    return E((a, y0, z0), (b, y1, z1), tex, pv, **kw)


def SEG(A, B, w, h, tex, light=0, up=UP, ext=0.15):
    return seg(A, B, w, h, tex, _PV[0], up, ext, light=light, shift=(_rs.random(), _rs.random()))


def CH(pts, ws, tex, light=0, up=FRONT, texs=None, lights=None, ext=0.2):
    """a tapering run of boxes along a polyline (square in section): a claw, a finger, an antenna, a cable"""
    n = len(pts) - 1
    if isinstance(ws, tuple): ws = [ws[0] + (ws[1] - ws[0]) * i / max(1, n - 1) for i in range(n)]
    out = []
    for i in range(n):
        t = texs[i] if texs else tex
        lt = lights[i] if lights else light
        out.append(seg(pts[i], pts[i + 1], ws[i], ws[i], t, _PV[0], up, ext, light=lt, shift=(_rs.random(), _rs.random())))
    return out


def GEM(c, s, tex, light=15, rot=(35.26, 45.0, 0.0)):
    """a cube stood on its point (a core, a spark)"""
    return E((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, light=light, rot=(rot, c))


def RING(c, r, n, w, h, tex, light=15, plane='xz', phase=0.0, ext=0.12):
    """a ring of boxes round c, radius r (plane 'xz': flat; 'xy': standing, facing front)"""
    out = []
    for i in range(n):
        a0, a1 = 2 * math.pi * (i + phase) / n, 2 * math.pi * (i + 1 + phase) / n
        if plane == 'xz':
            A = (c[0] + r * math.cos(a0), c[1], c[2] + r * math.sin(a0)); B = (c[0] + r * math.cos(a1), c[1], c[2] + r * math.sin(a1)); up = UP
        else:
            A = (c[0] + r * math.cos(a0), c[1] + r * math.sin(a0), c[2]); B = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1), c[2]); up = FRONT
        out.append(seg(A, B, w, h, tex, _PV[0], up, ext, light=light, shift=(_rs.random(), _rs.random())))
    return out


def _lit(tex, lit):
    return tex if lit else {'vx_glow': 'vx_off', 'vx_glow_l': 'vx_off', 'vx_visor': 'vx_off', 'vx_cockpit': 'vx_cockpit_off',
                            'vx_glass': 'vx_glass_off', 'vx_reactor': 'vx_reactor_off'}.get(tex, tex)


def _lt(lit, v=15):
    return v if lit else 0


# ==================================================================================================== THE WARFRAME
def _w_body(lit=True):
    """the pelvis, hip housings, a red belt - and the reactor in the abdomen above it, caged"""
    B = [E((-6.0, 16.5, -4.2), (6.0, 22.0, 4.2), 'vx_hull_d'), E((-5.2, 15.4, -5.2), (5.2, 21.4, -4.2), 'vx_hull'),
         E((-2.4, 13.2, -5.0), (2.4, 15.6, -3.4), 'vx_hull'), E((-5.6, 16.0, 4.2), (5.6, 21.4, 5.2), 'vx_hull'),
         E((-6.1, 20.6, -4.35), (6.1, 22.0, 4.35), 'vx_varmor'), E((-6.15, 21.1, -4.4), (6.15, 21.5, 4.4), _lit('vx_vstripe', lit), light=_lt(lit, 10)),
         E((-0.7, 15.6, -5.45), (0.7, 20.6, -5.2), 'vx_red')]
    for sx in (1, -1):
        B += [BX(sx, 5.6, 9.2, 16.4, 21.6, -2.8, 3.6, 'vx_hull'), BX(sx, 9.2, 9.9, 17.4, 20.6, -1.8, 2.6, 'vx_hull_l'),
              BX(sx, 4.6, 5.2, 22.6, 25.6, -2.2, 2.2, _lit('vx_glow', lit), light=_lt(lit))]
    # the reactor: a housing, the core's face (whole uv), a cage of bars over it
    B += [E((-4.6, 21.6, -3.4), (4.6, 26.6, 3.4), 'vx_hull_d'),
          E((-3.2, 22.0, -4.4), (3.2, 26.4, -3.3), _lit('vx_reactor', lit), light=_lt(lit), uv={'north': [0, 0, 16, 16]})]
    for x in (-1.6, 0.0, 1.6):
        B.append(E((x - 0.3, 21.8, -4.85), (x + 0.3, 26.6, -4.35), 'vx_hull_d'))
    B.append(E((-3.6, 23.9, -4.8), (3.6, 24.5, -4.4), 'vx_hull_d'))
    return B


def _w_chest(lit=True):
    """the hull: top-heavy, chamfered, red chevrons over the cockpit - a glass dome, Vexis inside against a green-lit wall"""
    C = [E((-4.2, 24.6, -3.0), (4.2, 27.6, 3.4), 'vx_hull_d'),
         E((-8.5, 26.6, -6.0), (8.5, 31.6, 6.0), 'vx_hull'), E((-11.0, 30.6, -7.2), (11.0, 41.6, 7.5), 'vx_hull'),
         E((-10.4, 41.4, -6.4), (10.4, 42.4, 7.0), 'vx_hull_l'),
         E((-0.7, 26.8, -6.4), (0.7, 30.8, -6.0), 'vx_red')]
    for sx in (1, -1):
        C += [BX(sx, 5.2, 7.2, 27.4, 30.6, -6.35, -6.0, 'vx_vent'),
              BX(sx, 7.6, 11.6, 30.6, 41.4, -8.4, -6.8, 'vx_hull_l', rot=('y', sx * 24, (sx * 7.6, 36, -7.6))),     # (the chamfers)
              BX(sx, 5.8, 7.4, 33.0, 40.6, -7.45, -7.2, 'vx_red'),                                            # (red flanking the cockpit)
              BX(sx, 9.6, 11.4, 26.8, 32.0, -5.0, 5.0, 'vx_hull_l'),
              BX(sx, 7.0, 9.4, 32.6, 33.2, -7.45, -7.2, _lit('vx_glow', lit), light=_lt(lit, 12)),
              BX(sx, 4.4, 6.0, 41.4, 43.6, -4.0, 2.0, 'vx_hull'), BX(sx, 6.0, 9.8, 26.8, 27.6, -6.3, -6.0, 'vx_hull_d')]
    C.append(E((-5.6, 41.4, 1.4), (5.6, 44.4, 4.4), 'vx_hull'))                                 # (the collar behind the head)
    # ---- the cockpit: a heavy brow over it, a sill, posts; the glass; inside, Vexis at the helm
    C += [E((-4.6, 31.4, -7.4), (4.6, 38.8, -7.2), _lit('vx_cockpit', lit), light=_lt(lit)),
          E((-5.0, 30.8, -10.8), (5.0, 31.6, -7.2), 'vx_hull_l'), E((-5.4, 38.6, -10.6), (5.4, 39.8, -7.2), 'vx_hull'),
          E((-1.0, 39.8, -10.2), (1.0, 41.4, -7.2), 'vx_hull_l')]
    for sx in (1, -1):
        C += [BX(sx, 4.2, 5.2, 31.4, 38.8, -10.8, -9.8, 'vx_hull_d'), BX(sx, 4.4, 4.6, 31.6, 38.6, -9.8, -7.3, _lit('vx_glass', lit), faces=('east', 'west'))]
    C.append(E((-4.2, 31.6, -10.5), (4.2, 38.6, -10.3), _lit('vx_glass', lit), faces=('north',)))
    # (the pilot: a Vorn - black armour with the green stripe, the square head, the dark muzzle, green eyes, dark ears, the two antennae)
    C += [E((-2.6, 31.6, -8.2), (2.6, 32.8, -7.45), 'vx_hull_d'),                                # (the seat)
          E((-1.8, 31.6, -9.3), (1.8, 34.4, -8.0), 'vx_varmor'), E((-1.85, 32.8, -9.35), (1.85, 33.2, -7.95), _lit('vx_vstripe', lit), light=_lt(lit, 10)),
          E((-1.4, 34.4, -9.8), (1.4, 36.8, -8.0), 'vx_skin'), E((-0.75, 34.5, -10.25), (0.75, 35.4, -9.75), 'vx_skin_d'),
          E((-0.3, 35.2, -10.32), (0.3, 35.55, -10.22), 'vx_eye_hive' if lit else 'vx_eye_hive_dim', light=_lt(lit), uv={'north': [0, 0, 16, 16]})]
    for sx in (1, -1):
        C += [BX(sx, 0.3, 1.0, 35.75, 36.45, -9.86, -9.78, 'vx_eye_hive' if lit else 'vx_eye_hive_dim', light=_lt(lit), uv={'north': [0, 0, 16, 16]}, faces=('north',)),
              BX(sx, 1.35, 1.75, 34.2, 36.4, -9.5, -8.3, 'vx_skin_d'),
              BX(sx, 0.48, 0.72, 36.8, 37.9, -9.0, -8.76, 'vx_skin_d'), BX(sx, 0.35, 0.85, 37.8, 38.3, -9.13, -8.63, 'vx_frog', light=_lt(lit)),
              BX(sx, 1.8, 2.5, 32.2, 34.2, -9.6, -8.2, 'vx_varmor'), BX(sx, 1.85, 2.45, 31.6, 32.3, -9.9, -9.0, 'vx_skin_d'),
              BX(sx, 1.6, 3.8, 31.6, 32.4, -10.2, -9.2, _lit('vx_glow', lit), light=_lt(lit, 12))]
    return C


def _w_head(face=None):
    """a low sensor head, wedge-browed, one green visor bar; jaw plates; side sensors; two antennae (the left one taller)"""
    H = [E((-2.2, 40.8, -3.6), (2.2, 43.0, 0.6), 'vx_hull_d'),
         E((-3.8, 42.4, -6.2), (3.8, 46.4, 1.6), 'vx_hull'), E((-3.4, 46.2, -5.4), (3.4, 47.2, 1.0), 'vx_hull_l'),
         E((-0.6, 46.6, -5.8), (0.6, 47.4, 1.2), 'vx_red'),
         E((-3.5, 43.2, -6.5), (3.5, 45.2, -6.2), 'vx_hull_d')]
    f = face
    a = {'narrowed': 12, 'wide': 2}.get(f, 7)
    for sx in (1, -1):                                        # (the brow: a V, harder when narrowed)
        H.append(BX(sx, 0, 4.3, 45.1, 46.5, -7.4, -6.0, 'vx_hull', rot=('z', -sx * a, (0, 45.8, -6.7))))
        H += [BX(sx, 0.6, 3.6, 41.6, 43.4, -7.0, -5.2, 'vx_hull_d', rot=('y', -sx * 16, (sx * 0.6, 42.5, -6.1))),
              BX(sx, 3.8, 4.8, 43.0, 45.4, -4.6, -1.4, 'vx_hull_l'),
              BX(sx, 4.8, 5.0, 43.6, 44.6, -4.0, -2.6, 'vx_glow' if f not in ('dim', 'closed') else ('vx_glow_d' if f == 'dim' else 'vx_off'), light=0 if f == 'closed' else 12)]
    bar = {None: (43.7, 44.7, 'vx_visor', 15), 'narrowed': (44.0, 44.45, 'vx_visor', 15), 'wide': (43.4, 45.0, 'vx_visor', 15),
           'dim': (43.8, 44.6, 'vx_glow_d', 6), 'closed': (43.8, 44.6, 'vx_off', 0)}[f]
    H.append(E((-3.1, bar[0], -6.62), (3.1, bar[1], -6.45), bar[2], light=bar[3]))
    if f == 'wide':                                           # (it flares past the slot)
        for sx in (1, -1): H.append(BX(sx, 3.1, 4.4, 43.9, 44.5, -6.7, -6.4, 'vx_glow_l', light=15))
    for sx in (1, -1):                                        # (the Vorn's two antennae: dark stalks, froglight tips - and its ear-plates)
        H += [E((sx * 2.2 - 0.32, 46.9, -1.0), (sx * 2.2 + 0.32, 51.6, -0.36), 'vx_skin_d'),
              E((sx * 2.2 - 0.62, 51.4, -1.3), (sx * 2.2 + 0.62, 52.6, -0.06), 'vx_frog' if f != 'closed' else 'vx_off', light=0 if f == 'closed' else 15),
              BX(sx, 3.8, 4.8, 40.6, 46.2, -1.4, 1.6, 'vx_varmor', rot=('z', sx * 7, (sx * 3.8, 46.2, 0))),
              BX(sx, 4.75, 4.85, 41.6, 42.2, -1.2, 1.4, 'vx_vstripe_r', rot=('z', sx * 7, (sx * 3.8, 46.2, 0)))]
    return H


def _w_arm(sx):
    """the shoulder: a great pauldron (a red band and stripe), the upper arm, a piston, the elbow"""
    A = [BX(sx, 11.0, 15.6, 34.8, 39.4, -2.2, 3.2, 'vx_hull_d'),
         BX(sx, 10.8, 18.2, 37.6, 42.4, -5.2, 6.0, 'vx_hull'),
         BX(sx, 11.4, 18.6, 42.2, 43.2, -4.6, 5.4, 'vx_hull_l', rot=('z', -sx * 10, (sx * 11.4, 42.7, 0))),
         BX(sx, 12.0, 18.8, 35.6, 37.8, -4.6, 5.4, 'vx_hull', rot=('z', -sx * 8, (sx * 12.0, 37.8, 0))),
         BX(sx, 18.2, 18.55, 37.9, 42.1, -4.6, 5.4, 'vx_varmor_r'), BX(sx, 18.5, 18.7, 39.6, 40.5, -4.6, 5.4, 'vx_vstripe_r', light=8),
         BX(sx, 12.0, 16.4, 28.2, 35.6, -2.4, 3.2, 'vx_hull'), BX(sx, 12.6, 13.4, 28.6, 35.0, 3.2, 4.0, 'vx_hull_l'),
         BX(sx, 12.2, 16.8, 25.8, 28.6, -2.6, 3.4, 'vx_hull_d')]
    for z in (-3.0, 0.4, 3.8):                                # (vents on the pauldron's top)
        A.append(BX(sx, 13.0, 16.6, 42.55, 42.75, z - 0.5, z + 0.5, 'vx_hull_d', rot=('z', -sx * 10, (sx * 11.4, 42.7, 0))))
    return A


def _w_cannon(lit=True):
    """the plasma cannon (right forearm): a housing (a red stripe, vents), three green coils round the barrel, a muzzle brake,
    the bore glowing at its foot (the beam goes down -y from fxh), a feed cable"""
    G, GL = _lit('vx_glow', lit), _lit('vx_glow_l', lit)
    C = [E((11.4, 17.0, -3.6), (17.8, 27.0, 4.6), 'vx_hull'), E((11.0, 21.6, -4.2), (18.2, 26.2, 5.2), 'vx_hull_l'),
         E((18.2, 22.4, -3.0), (18.45, 25.4, 4.0), 'vx_red'),
         E((11.1, 17.6, -2.4), (11.4, 21.2, 3.4), 'vx_vent'),
         E((12.9, 7.0, -1.1), (16.1, 17.2, 2.1), 'vx_hull_d')]
    for y in (15.6, 13.0, 10.4):
        C.append(E((12.3, y - 0.7, -1.7), (16.7, y + 0.7, 2.7), G, light=_lt(lit)))
    C += [E((14.2, 8.0, -1.25), (14.8, 16.6, -1.1), GL, light=_lt(lit)),
          E((12.1, 5.6, -2.0), (16.9, 8.0, 3.0), 'vx_hull'), E((12.4, 6.2, -2.15), (16.6, 6.8, 3.15), 'vx_red'),
          E((13.3, 5.45, -0.7), (15.7, 5.7, 1.7), GL, light=_lt(lit))]
    C += CH([(14.5, 24.0, 4.8), (14.6, 19.4, 6.2), (14.5, 14.2, 2.4)], [1.1, 0.9], 'vx_cable')
    return C


def _w_claw():
    """the manipulator (left forearm): an armoured forearm, a wrist, a hub - three long claws, curling in"""
    sx = -1
    F = [BX(sx, 11.6, 17.4, 18.0, 27.0, -3.0, 4.0, 'vx_hull'), BX(sx, 17.4, 18.0, 19.0, 26.0, -2.4, 3.4, 'vx_hull_l'),
         BX(sx, 18.0, 18.25, 20.0, 25.0, -1.6, 2.6, 'vx_red'), BX(sx, 11.2, 18.2, 22.4, 23.4, -3.4, 4.4, 'vx_red'),
         BX(sx, 12.4, 16.6, 15.6, 18.2, -2.2, 3.2, 'vx_hull_d'), BX(sx, 12.0, 17.0, 13.4, 15.8, -2.6, 3.6, 'vx_hull')]
    cx, cy, cz = -14.5, 14.0, 0.5
    for th in (-55.0, 55.0, 180.0):
        dx, dz = math.sin(math.radians(th)), -math.cos(math.radians(th))
        b = (cx + 2.0 * dx, cy, cz + 2.0 * dz); m = (cx + 3.6 * dx, cy - 3.8, cz + 3.6 * dz); t = (cx + 1.6 * dx, cy - 8.0, cz + 1.6 * dz)
        F += CH([b, m, t], [1.5, 1.0], 'vx_hull_l', texs=['vx_hull_l', 'vx_hull_d'])
    return F


def _w_leg(sx):
    """the thigh: forward and down from the hip to the knee, plated, a red stripe on its outer plate"""
    return [BX(sx, 4.8, 8.6, 17.0, 21.0, -1.8, 2.8, 'vx_hull_d'),
            SEG((sx * 6.8, 18.6, 0.3), (sx * 7.0, 12.0, -3.6), 4.6, 5.0, 'vx_hull', up=FRONT),
            SEG((sx * 9.4, 18.0, -0.1), (sx * 9.6, 13.0, -3.0), 0.8, 5.4, 'vx_hull_l', up=FRONT),
            SEG((sx * 9.85, 17.6, -0.6), (sx * 9.95, 13.6, -2.9), 0.3, 1.2, 'vx_red', up=FRONT),
            SEG((sx * 6.9, 17.2, -2.4), (sx * 7.0, 12.8, -5.2), 4.0, 0.8, 'vx_hull_l', up=FRONT),
            SEG((sx * 6.8, 18.0, 3.0), (sx * 7.0, 12.8, -0.8), 1.0, 1.0, 'vx_hull_l', up=FRONT)]


def _w_shin(sx):
    """the shin: back and down from the knee (a great knee cap, red-striped) to the hock, a piston behind"""
    return [BX(sx, 4.8, 9.2, 9.8, 13.2, -6.0, -2.4, 'vx_hull_d'),
            BX(sx, 4.4, 9.6, 10.0, 14.6, -7.6, -5.6, 'vx_hull'), BX(sx, 6.4, 7.6, 10.4, 14.2, -7.85, -7.6, 'vx_red'),
            BX(sx, 4.6, 9.4, 14.4, 15.2, -7.2, -5.8, 'vx_hull_l'),
            SEG((sx * 7.0, 11.0, -3.6), (sx * 7.0, 5.8, 3.0), 3.8, 4.0, 'vx_hull'),
            SEG((sx * 7.0, 10.4, -5.2), (sx * 7.0, 6.6, 1.4), 2.8, 0.8, 'vx_hull_l'),
            SEG((sx * 7.0, 10.6, -1.0), (sx * 7.0, 6.4, 4.4), 1.0, 1.0, 'vx_hull_l')]


def _w_foot(sx):
    """the hock, the metatarsus down to a big three-toed foot, a heel spur"""
    F = [BX(sx, 5.2, 8.8, 4.2, 6.8, 2.0, 5.2, 'vx_hull_d'),
         SEG((sx * 7.0, 5.2, 3.2), (sx * 7.0, 2.0, 0.4), 3.0, 3.0, 'vx_hull', up=FRONT),
         BX(sx, 3.6, 10.4, 0.0, 2.6, -4.4, 2.6, 'vx_hull'), BX(sx, 4.6, 9.4, 2.6, 3.2, -3.6, 1.8, 'vx_hull_l'),
         BX(sx, 6.4, 7.6, 2.6, 2.8, -4.2, 0.4, 'vx_red'),
         BX(sx, 5.8, 8.2, 0.0, 1.6, 2.6, 6.0, 'vx_hull_d')]
    for (x0, x1, a) in ((3.6, 5.6, 14), (6.0, 8.0, 0), (8.4, 10.4, -14)):
        r = ('y', sx * a, (sx * (x0 + x1) / 2, 1.0, -4.4))
        F += [BX(sx, x0, x1, 0.0, 2.1, -7.6, -4.2, 'vx_hull', rot=r), BX(sx, x0 + 0.3, x1 - 0.3, 0.0, 1.3, -8.8, -7.6, 'vx_hull_d', rot=r)]
    return F


def _w_pod(sx, open_=False):
    """a missile pod on the shoulder: a box of six tubes; shut, an armoured hatch (a red chevron) over its face; open, the hatch
    swung up and the warheads out"""
    P = [BX(sx, 7.0, 11.0, 41.2, 42.6, 1.0, 6.0, 'vx_hull_d'),
         BX(sx, 5.6, 12.6, 42.4, 47.6, -0.6, 7.4, 'vx_hull'), BX(sx, 12.6, 12.85, 43.0, 47.0, 0.0, 6.8, 'vx_red'),
         BX(sx, 5.8, 12.4, 47.6, 48.0, 0.0, 7.0, 'vx_hull_l')]
    hinge = (0.0, 47.4, -1.2)
    if not open_:
        P += [BX(sx, 5.8, 12.4, 42.6, 47.4, -1.2, -0.6, 'vx_hull_l'),
              BX(sx, 7.0, 11.2, 44.4, 45.2, -1.4, -1.2, 'vx_red', rot=('z', sx * 20, (sx * 9.1, 44.8, -1.3)))]
    else:
        r = ('x', 67.5, (sx * 9.1, 47.4, -1.2))
        P += [BX(sx, 5.8, 12.4, 47.4, 48.0, -6.0, -1.2, 'vx_hull_l', rot=r)]
        for x in (6.9, 9.1, 11.3):
            for y in (43.7, 46.1):
                P += [BX(sx, x - 0.7, x + 0.7, y - 0.7, y + 0.7, -2.0, -0.6, 'vx_missile'),
                      BX(sx, x - 0.3, x + 0.3, y - 0.3, y + 0.3, -2.3, -2.0, 'vx_glow_l', light=15)]
    del hinge
    P = rigkit.transform(P, lambda v: [v[0] + sx * 0.2, v[1] + 1.8, v[2]])     # (raised clear of the pauldrons and the head)
    return P + [BX(sx, 6.8, 10.6, 42.2, 44.6, 1.4, 6.4, 'vx_hull_d')]


def _w_back(lit=True):
    """the backpack: thrusters underneath, vents, a red spine stripe; comms masts (a dish on the left), a centre antenna"""
    B = [E((-7.2, 28.0, 7.2), (7.2, 40.4, 11.2), 'vx_hull'), E((-6.6, 40.2, 7.2), (6.6, 41.4, 10.2), 'vx_hull_l'),
         E((-0.8, 29.0, 11.2), (0.8, 40.0, 11.45), 'vx_red')]
    for sx in (1, -1):
        B += [BX(sx, 2.0, 5.6, 25.6, 28.4, 7.6, 11.0, 'vx_hull_d'),
              BX(sx, 2.6, 5.0, 25.45, 25.7, 8.2, 10.4, _lit('vx_glow_l', lit), light=_lt(lit)),
              BX(sx, 2.4, 6.4, 31.0, 38.0, 11.2, 11.45, 'vx_vent'),
              BX(sx, 7.2, 7.5, 30.0, 39.0, 8.0, 10.6, 'vx_red'),
              BX(sx, 6.4, 7.0, 39.4, 40.0, 10.6, 11.2, _lit('vx_glow', lit), light=_lt(lit, 12))]
    B += CH([(-4.6, 40.2, 9.0), (-5.4, 46.0, 11.0), (-6.0, 51.6, 12.4)], [0.9, 0.6], 'vx_hull_l')
    B += [E((-8.4, 45.6, 10.2), (-5.6, 48.6, 10.7), 'vx_hull_l', rot=('y', 30, (-7.0, 47.0, 10.4))),
          E((-7.3, 46.8, 10.0), (-6.7, 47.4, 10.25), _lit('vx_glow_l', lit), light=_lt(lit), rot=('y', 30, (-7.0, 47.0, 10.4))),
          E((-6.7, 51.4, 11.7), (-5.3, 52.8, 13.1), 'vx_frog' if lit else 'vx_off', light=_lt(lit))]
    B += CH([(4.6, 40.2, 9.0), (5.2, 44.6, 10.6), (5.6, 47.6, 11.6)], [0.8, 0.55], 'vx_hull_l')
    B += [E((4.9, 47.3, 10.9), (6.3, 48.7, 12.3), 'vx_frog' if lit else 'vx_off', light=_lt(lit)),
          E((-0.4, 40.6, 9.2), (0.4, 45.6, 10.0), 'vx_hull_d')]
    for y in (42.0, 43.6):
        B.append(E((-1.4, y, 9.3), (1.4, y + 0.4, 9.9), 'vx_hull_l'))
    return B


# ==================================================================================================== VEXIS
def _sk(form):
    return ('vx_skin_s', 'vx_skin_sd') if form == 'starfire' else ('vx_skin', 'vx_skin_d')


def _gl(form, dim=False):
    """its light: the hive's green; the star's fire; the follower's, dimmer"""
    if form == 'starfire': return 'vx_fire_l'
    return 'vx_glow' if (form == 'unlinked' or dim) else 'vx_glow_l'


def _grow(els, k, shift=(0.0, 0.0, 0.0)):
    """a part's elements grown k about its joint (and shifted, design units)"""
    return rigkit.transform(els, lambda v: [8 + (v[0] - 8) * k + shift[0], 8 + (v[1] - 8) * k + shift[1], 8 + (v[2] - 8) * k + shift[2]])


W_HEAD_K = 1.3                                 # (the warframe's head, grown about its neck and brought forward a unit)
HEAD_K = 1.0                                   # (Vexis's head: built at its own size)


def _a_head(form, face=None):
    return _grow(_a_head0(form, face), HEAD_K)


def _a_head0(form, face=None):
    """a VORN's head, an elder's: the troopers' square skull (phase25.donado_parts, in Vorn colours) grown regal - the dark
    muzzle with its green nose and smile and an elder's beard under it, the square green eyes with a dark pupil at their outer top,
    long dark ears hanging past the jaw, the Vorn's two antennae (dark stalks, froglight tips) standing tall out of an admiral's
    circlet with a crown of lesser ones; the hive's port and cables at the back of the skull (cut, for the follower); starfire:
    a halo of solar flare behind it"""
    S, SD = _sk(form); H = []
    MZ = 'vx_skin_sd' if form == 'starfire' else 'vx_skin_d'
    H += [E((-1.1, 22.6, -0.9), (1.1, 25.8, 1.5), S),                                              # (the neck)
          E((-4.2, 25.4, -3.2), (4.2, 32.4, 3.2), S),                                               # (the skull)
          E((-2.3, 25.6, -5.0), (2.3, 28.6, -3.15), MZ),                                            # (the muzzle)
          E((-0.9, 24.6, -4.6), (0.9, 25.7, -3.4), MZ)]                                             # (an elder's beard)
    nose = 'vx_eye_star' if form == 'starfire' else ('vx_eye_calm' if form == 'unlinked' else 'vx_eye_hive')
    H += [E((-0.95, 27.9, -5.15), (0.95, 28.9, -4.95), nose, light=12, uv={'north': [0, 0, 16, 16]}),       # (the nose)
          E((-1.35, 26.55, -5.1), (1.35, 26.85, -4.98), nose, light=12, faces=('north',), uv={'north': [0, 0, 16, 16]})]   # (the smile)
    for sx in (1, -1):                                        # (the ears: long, dark, hanging past the jaw, a hive clip on each)
        r = ('z', sx * 6, (sx * 4.2, 31.6, 0))
        H += [BX(sx, 4.15, 5.45, 23.6, 31.6, -1.4, 2.6, MZ, rot=r),
              BX(sx, 5.4, 5.75, 26.2, 27.4, -0.2, 1.4, 'vx_implant_off' if form == 'unlinked' else 'vx_implant', rot=r)]
    # ---- the eyes (FACES)
    pal = {'starfire': 'star', 'unlinked': 'calm'}.get(form, 'hive')
    et = f'vx_eye_{pal}{"_dim" if face == "dim" else ""}'
    lt = 0 if face in ('closed', 'dim') else 15
    ez = -3.2
    for sx in (1, -1):
        if face == 'closed':
            H.append(BX(sx, 0.8, 2.8, 29.6, 30.0, ez - 0.12, ez + 0.05, 'vx_skin_d', faces=('north',)))
            continue
        if face == 'soft':                                    # (the eyes smiling: an arch of light)
            H += [BX(sx, 0.75, 1.85, 29.7, 30.25, ez - 0.12, ez + 0.05, et, light=lt, faces=('north',), uv={'north': [0, 0, 16, 16]}, rot=('z', sx * 28, (sx * 1.8, 30.2, ez))),
                  BX(sx, 1.75, 2.85, 29.7, 30.25, ez - 0.12, ez + 0.05, et, light=lt, faces=('north',), uv={'north': [0, 0, 16, 16]}, rot=('z', -sx * 28, (sx * 1.8, 30.2, ez)))]
            continue
        x0, x1, y0, y1 = {'wide': (0.55, 3.0, 28.7, 31.3), 'narrowed': (0.8, 2.8, 29.3, 30.4)}.get(face, (0.8, 2.8, 29.0, 31.0))
        H.append(BX(sx, x0, x1, y0, y1, ez - 0.12, ez + 0.05, et, light=lt, faces=('north',), uv={'north': [0, 0, 16, 16]}))
        if face != 'dim':                                     # (the dark pupil at the top of each eye, on its right side - as the troopers have it)
            pw = 0.45 if face == 'wide' else 0.55
            a0 = x1 - 0.25 - pw if sx > 0 else x0 + 0.25
            H.append(BX(sx, a0, a0 + pw, y1 - 0.25 - pw, y1 - 0.25, ez - 0.16, ez - 0.1, 'vx_skin_d', faces=('north',)))
        if face == 'narrowed':                                # (the brow drawn down hard toward the muzzle)
            H.append(BX(sx, 0.4, 3.4, 30.3, 31.1, -3.5, -3.1, MZ, rot=('z', -sx * 14, (sx * 0.4, 30.7, -3.3))))
    # ---- the admiral's circlet, a crown of lesser antennae - and the Vorn pair, tall
    tip = {'hivelink': 15, 'starfire': 15, 'unlinked': 11}[form]
    H += [E((-4.35, 31.6, -3.35), (4.35, 32.5, 3.35), 'vx_hull_l'), E((-0.6, 31.7, -3.5), (0.6, 32.4, -3.3), _gl(form), light=tip)]
    for x, z, h in ((-3.3, -2.0, 2.0), (3.3, -2.0, 2.0), (-3.3, 2.2, 2.6), (3.3, 2.2, 2.6), (0.0, 2.6, 3.0)):
        H += [E((x - 0.22, 32.4, z - 0.22), (x + 0.22, 32.4 + h, z + 0.22), MZ),
              E((x - 0.4, 32.4 + h, z - 0.4), (x + 0.4, 33.2 + h, z + 0.4), 'vx_frog', light=tip)]
    for sx in (1, -1):
        H += [E((sx * 1.7 - 0.4, 32.4, -0.4), (sx * 1.7 + 0.4, 38.6, 0.4), MZ, rot=('z', -sx * 4, (sx * 1.7, 32.4, 0))),
              E((sx * 2.13 - 0.75, 38.4, -0.75), (sx * 2.13 + 0.75, 39.9, 0.75), 'vx_frog', light=tip, rot=('z', -sx * 4, (sx * 1.7, 32.4, 0)))]
    # ---- the hive's port at the back of the skull, its cables
    imp = 'vx_implant_off' if form == 'unlinked' else 'vx_implant'
    H.append(E((-1.4, 28.6, 3.15), (1.4, 31.0, 3.8), imp))
    if form != 'unlinked':
        cab = 'vx_cable_s' if form == 'starfire' else 'vx_cable'
        for sx in (1, -1):
            H += CH([(sx * 0.8, 29.4, 3.7), (sx * 1.6, 27.6, 4.6), (sx * 2.0, 25.6, 4.2), (sx * 1.8, 24.2, 3.0)], [0.8, 0.7, 0.6], cab,
                    light=12 if form == 'starfire' else 0)
    else:                                                     # (cut: a stub each, bare wire fraying out of it)
        for sx in (1, -1):
            end = (sx * 1.4, 28.0, 4.8)
            H += CH([(sx * 0.8, 29.4, 3.7), end], [0.8], 'vx_cable_u')
            for dx, dy, dz in ((0.5, -0.9, 0.5), (-0.3, -1.0, 0.6), (0.1, -0.6, 0.9)):
                H.append(seg(end, (end[0] + sx * dx, end[1] + dy, end[2] + dz), 0.18, 0.18, 'vx_wire', _PV[0], FRONT, 0.05))
    # ---- starfire: the halo - a burning ring behind the skull, flares off it
    if form == 'starfire':
        c = (0.0, 31.0, 5.6)
        H += RING(c, 6.6, 20, 0.7, 0.6, 'vx_fire', plane='xy')
        rnd = random.Random(808)
        for i in range(14):
            a = 2 * math.pi * (i + 0.5) / 14; ln = rnd.uniform(1.6, 3.6) * (1.4 if i % 3 == 0 else 1.0)
            A = (c[0] + 6.8 * math.cos(a), c[1] + 6.8 * math.sin(a), c[2]); B = (c[0] + (6.8 + ln) * math.cos(a), c[1] + (6.8 + ln) * math.sin(a), c[2] + 0.3)
            H.append(seg(A, B, 0.9, 0.5, 'vx_fire_l' if i % 2 else 'vx_fire', _PV[0], FRONT, 0.1, light=15))
        H += RING(c, 5.0, 16, 0.4, 0.4, 'vx_hot', plane='xy', phase=0.5)
    return H


def _a_chest(form):
    """the Vorn's black armour (phase32 vorn_armor), an admiral's long tunic of it: the troopers' green stripe round the waist, a
    ragged hem; the hive-link's gorget round the neck; the hive's node in its breast; implant ports down the spine with cables up
    into the gorget (cut stubs for the follower)"""
    S, SD = _sk(form); C = []
    A_, ST = 'vx_varmor', ('vx_fire_l' if form == 'starfire' else 'vx_vstripe')
    C += [E((-2.3, 14.2, -1.6), (2.3, 17.6, 1.7), A_), E((-2.36, 15.4, -1.66), (2.36, 16.0, 1.76), ST, light=0 if form == 'unlinked' else 12),
          E((-3.9, 17.2, -2.4), (3.9, 22.0, 2.3), A_), E((-4.1, 17.6, -2.2), (4.1, 19.4, 2.1), A_),
          E((-5.0, 21.0, -1.9), (5.0, 23.0, 2.0), A_), E((-1.6, 22.8, -1.0), (1.6, 23.8, 1.4), S)]
    for sx in (1, -1):
        C += [BX(sx, 3.8, 5.6, 21.2, 23.3, -1.5, 1.8, A_), BX(sx, 2.4, 4.0, 19.2, 21.6, -2.5, -2.35, 'vx_hull_l')]     # (the admiral's chest plates)
    imp = 'vx_implant_off' if form == 'unlinked' else 'vx_implant'
    node = {'hivelink': 'vx_node', 'starfire': 'vx_node_s', 'unlinked': 'vx_node_u'}[form]
    C += [E((-1.3, 19.0, -2.8), (1.3, 21.6, -2.4), node, light=0 if form == 'unlinked' else 15, uv={'north': [0, 0, 16, 16]}),
          E((-1.6, 18.7, -2.6), (1.6, 21.9, -2.35), imp),
          E((-2.6, 22.9, -2.2), (2.6, 24.0, 2.4), imp)]                                            # (the gorget)
    gl = {'hivelink': 'vx_glow_l', 'starfire': 'vx_fire_l', 'unlinked': 'vx_off'}[form]
    for sx in (1, -1):
        C.append(BX(sx, 0.8, 1.8, 23.1, 23.8, -2.35, -2.2, gl, light=0 if form == 'unlinked' else 15))
    for y in (15.4, 17.2, 19.0, 20.8):
        C.append(E((-0.8, y, 2.2), (0.8, y + 0.9, 2.75), imp))
    if form != 'unlinked':
        cab = 'vx_cable_s' if form == 'starfire' else 'vx_cable'
        for sx in (1, -1):
            C += CH([(sx * 0.5, 19.4, 2.7), (sx * 1.4, 21.2, 3.1), (sx * 1.6, 23.0, 2.9), (sx * 1.4, 23.6, 2.3)], [0.6, 0.55, 0.5], cab, light=12 if form == 'starfire' else 0)
    else:
        for sx in (1, -1):
            C += CH([(sx * 0.5, 19.4, 2.7), (sx * 1.2, 20.8, 3.1)], [0.6], 'vx_cable_u')
            C.append(seg((sx * 1.2, 20.8, 3.1), (sx * 1.7, 21.5, 3.4), 0.15, 0.15, 'vx_wire', _PV[0], FRONT, 0.05))
    return C


def _a_body(form):
    """the hips in the tunic's black armour (its ragged hem, as the troopers' is), a belt with the hive's sigil, a tabard of the
    warlord's red armour front and back (the red stripe at its foot)"""
    S, SD = _sk(form)
    B = [E((-2.8, 11.2, -1.6), (2.8, 14.6, 1.8), 'vx_varmor'), E((-3.0, 12.6, -1.8), (3.0, 13.6, 2.0), 'vx_implant'),
         E((-0.7, 12.7, -1.95), (0.7, 13.5, -1.8), _gl(form), light=0 if form == 'unlinked' else 15),
         E((-1.3, 7.6, -2.1), (1.3, 12.6, -1.7), 'vx_mantle'), E((-1.35, 8.2, -2.15), (1.35, 9.2, -2.05), 'vx_mantle_r'),
         E((-1.5, 8.0, 1.8), (1.5, 12.6, 2.2), 'vx_mantle'), E((-1.55, 8.6, 2.15), (1.55, 9.6, 2.25), 'vx_mantle_r')]
    for sx in (1, -1):
        B += [BX(sx, 2.0, 3.3, 11.4, 13.4, -1.2, 1.4, 'vx_varmor'),
              BX(sx, 1.4, 2.6, 10.4, 11.4, -1.5, 1.7, 'vx_varmor'), BX(sx, 2.8, 3.4, 10.8, 11.4, -1.4, 1.6, 'vx_varmor')]    # (the ragged hem)
    if form == 'starfire':
        B += [E((-1.1, 7.2, -2.15), (1.1, 7.8, -1.8), 'vx_fire', light=15), E((-1.3, 7.6, 1.9), (1.3, 8.2, 2.2), 'vx_fire', light=15)]
    return B


def _a_arm(sx, form):
    """a long upper arm sleeved in the black armour; the epaulet over the shoulder (the warlord's red armour, its red stripe, a
    fringe of cable); an implant band; the elbow"""
    S, SD = _sk(form)
    r = ('z', -sx * 14, (sx * 2.8, 23.6, 0))
    A = [BX(sx, 3.9, 6.5, 20.6, 23.6, -1.4, 1.8, 'vx_varmor'),
         SEG((sx * 5.1, 21.4, 0.2), (sx * 5.5, 14.0, 0.2), 2.0, 2.1, 'vx_varmor', up=FRONT),
         BX(sx, 4.2, 6.6, 18.0, 19.1, -1.0, 1.4, 'vx_implant_off' if form == 'unlinked' else 'vx_implant'),
         BX(sx, 4.4, 6.6, 12.9, 14.7, -0.8, 1.2, 'vx_varmor'),
         BX(sx, 2.8, 7.6, 23.1, 24.2, -2.2, 2.9, 'vx_varmor_r', rot=r),
         BX(sx, 2.8, 7.6, 23.45, 23.85, -2.35, 3.05, 'vx_vstripe_r', rot=r, light=0 if form == 'unlinked' else 10),
         BX(sx, 3.6, 7.2, 24.2, 24.5, -1.2, 2.0, 'vx_hull_l', rot=r)]
    for z in (-1.6, 0.4, 2.4):                                # (the epaulet's fringe of cable)
        A += CH([(sx * 7.5, 22.6, z), (sx * 7.9, 20.4, z)], [0.4], 'vx_cable_u' if form == 'unlinked' else ('vx_cable_s' if form == 'starfire' else 'vx_cable'))
    return A


def _a_fore(sx, form):
    """a long Vorn forearm, a cybernetic bracer at the wrist (a light in it), the dark glove the troopers wear - three long
    gloved fingers (two and a thumb)"""
    S, SD = _sk(form); gl = _gl(form)
    G = 'vx_skin_sd' if form == 'starfire' else 'vx_skin_d'
    F = [SEG((sx * 5.5, 13.4, 0.2), (sx * 5.8, 6.2, 0.0), 1.8, 1.9, S, up=FRONT),
         BX(sx, 4.6, 7.0, 6.2, 9.8, -1.1, 1.3, 'vx_implant_off' if form == 'unlinked' else 'vx_implant'),
         BX(sx, 5.2, 6.4, 6.8, 9.2, -1.22, -1.1, gl, light=0 if form == 'unlinked' else 15),
         BX(sx, 4.7, 6.9, 3.9, 6.5, -1.1, 1.1, G)]
    tip = 'vx_fire_l' if form == 'starfire' else G
    for (x, z, ln, cu) in ((5.2, -0.5, 5.0, 1.0), (6.4, -0.4, 4.6, 0.9), (4.7, 0.6, 3.6, 0.6)):
        b = (sx * x, 4.2, z)
        F += CH([b, (b[0], 4.2 - ln * 0.55, z - 0.5 * cu), (b[0], 4.2 - ln, z - 0.1 * cu)], [0.7, 0.55], G, texs=[G, tip],
                lights=[0, 15 if form == 'starfire' else 0])
    return F


def _a_leg(sx, form):
    S, SD = _sk(form)
    return [SEG((sx * 2.0, 12.0, 0.2), (sx * 2.3, 7.6, -0.5), 1.2, 1.3, S, up=FRONT),
            SEG((sx * 2.95, 11.4, 0.2), (sx * 3.0, 8.0, -0.4), 0.35, 0.8, 'vx_implant', up=FRONT),
            BX(sx, 1.5, 3.15, 6.8, 8.2, -1.2, 0.0, 'vx_implant')]


def _a_shin(sx, form):
    S, SD = _sk(form)
    return [SEG((sx * 2.3, 7.2, -0.6), (sx * 2.3, 3.2, 0.3), 0.95, 1.0, S, up=FRONT),
            SEG((sx * 2.85, 6.8, -0.4), (sx * 2.9, 3.6, 0.3), 0.3, 0.7, 'vx_implant', up=FRONT),
            BX(sx, 1.7, 2.9, 4.2, 5.0, -0.7, 0.6, 'vx_implant')]


def _a_foot(sx, form):
    """a small foot in the troopers' dark boot, pointed down (it never stands on them), three little claws"""
    S, SD = _sk(form); G = 'vx_skin_sd' if form == 'starfire' else 'vx_skin_d'
    F = [SEG((sx * 2.3, 3.2, 0.4), (sx * 2.3, 0.9, -0.8), 1.25, 1.35, G, up=FRONT)]
    for dx in (-0.35, 0.0, 0.35):
        F += CH([(sx * 2.3 + dx, 1.0, -0.8), (sx * 2.3 + dx * 1.4, 0.0, -1.4)], [0.3], G)
    return F


def _a_back(form):
    """the command mantle: a stiff collar standing behind the skull, then ragged strips to the shins, wrapping its flanks, the
    red stripe above the hem. starfire: the hem burning; unlinked: mended with Donadian patches"""
    MT = 'vx_mantle_s' if form == 'starfire' else 'vx_mantle'
    rc = ('x', -18, (0, 22.6, 3.2))
    M = [E((-4.8, 22.6, 3.0), (4.8, 29.0, 3.7), MT, rot=rc), E((-4.9, 28.6, 2.95), (4.9, 29.4, 3.75), 'vx_mantle_r', rot=rc)]
    for x, h in ((-3.8, 2.4), (0.0, 3.4), (3.8, 2.4)):        # (the collar's points)
        M += CH([(x, 29.0, 5.0), (x * 1.15, 29.0 + h, 5.8)], [0.75], 'vx_mantle_r')
    rnd = random.Random(611); n = 10; W0 = 5.6
    def strip(xt, ang, bot, w, z0, z1, k, side=0):
        r = ('z', ang, (xt, 23.2, z1)) if not side else (('z', ang, (xt, 23.2, z1)))
        out = [E((xt - w / 2, bot, z0), (xt + w / 2, 23.4, z1), MT, rot=r),
               E((xt - w / 2 - 0.02, bot + 2.2, z1 - 0.02), (xt + w / 2 + 0.02, bot + 3.4, z1 + 0.08), 'vx_mantle_r', rot=r)]
        if rnd.random() < 0.6: out.append(E((xt - w / 2 + 0.2, bot - rnd.uniform(0.8, 2.0), z0 + 0.05), (xt - w / 2 + 0.7, bot, z1 - 0.05), MT, rot=r))
        if form == 'starfire':
            out.append(E((xt - w / 2 + 0.1, bot - 0.5, z0 - 0.1), (xt + w / 2 - 0.1, bot + 0.6, z1 + 0.1), 'vx_fire', light=15, rot=r))
            if k % 2: out += CH([(xt, bot, (z0 + z1) / 2), (xt + 0.3, bot - 1.8, z1)], [0.45], 'vx_fire_l', light=15)
        return out
    for k in range(n):
        xt = -W0 + 2 * W0 * (k + 0.5) / n; ang = -(xt / W0) * 7.0      # (each strip fanned out a little from the shoulders)
        bot = 3.6 + rnd.uniform(0, 3.0) + (1.4 if k in (0, n - 1) else 0)
        M += strip(xt, ang, bot, 2 * W0 / n + 0.05, 3.2, 3.6, k)
    for sx in (1, -1):                                        # (wrapping the flanks: strips turned to its sides)
        for j, (z, bot) in enumerate(((3.0, 6.6), (2.4, 8.2))):
            r = ('z', -sx * 9, (sx * 5.6, 21.4, z))
            M += [BX(sx, 5.45, 5.75, bot, 21.4, z - 0.4, z + 0.4, MT, rot=r), BX(sx, 5.42, 5.78, bot + 2.0, bot + 3.2, z - 0.42, z + 0.42, 'vx_mantle_r', rot=r)]
            if form == 'starfire': M.append(BX(sx, 5.4, 5.8, bot - 0.4, bot + 0.5, z - 0.55, z + 0.55, 'vx_fire', light=15, rot=r))
    if form == 'unlinked':
        M += [E((0.9, 12.4, 3.62), (3.6, 15.2, 3.78), 'vx_patch', uv={'south': [0, 0, 16, 16], 'north': [0, 0, 16, 16]}),
              E((-3.4, 7.2, 3.62), (-1.6, 9.0, 3.78), 'vx_patch', uv={'south': [0, 0, 16, 16], 'north': [0, 0, 16, 16]})]
    return M


def _a_ring(i, form):
    """a gravity ring: an energy band with gunmetal nodes (starfire: burning, flames licking off it; unlinked: one small ring)"""
    c = JA['ring1']; R = []
    if form == 'unlinked':
        R += RING(c, 7.0, 18, 0.4, 0.55, 'vx_ring', light=12)
        for k in range(2):
            a = math.pi * k; R.append(GEM((c[0] + 7.0 * math.cos(a), c[1], c[2] + 7.0 * math.sin(a)), 0.9, 'vx_hull_l', light=0, rot=(0.0, 45.0, 0.0)))
        return R
    star = form == 'starfire'
    if i == 1:
        r, n = 9.6, 24
        R += RING(c, r, n, 0.55, 0.9, 'vx_fire' if star else 'vx_ring')
        for k in range(3):
            a = 2 * math.pi * k / 3
            R.append(GEM((c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), 1.5, 'vx_fire_l' if star else 'vx_hull_l', light=15 if star else 0, rot=(0.0, 45.0, 0.0)))
    else:
        r, n = 12.4, 28
        R += RING((c[0], c[1] + 0.45, c[2]), r, n, 0.35, 0.4, 'vx_fire' if star else 'vx_ring2') + \
             RING((c[0], c[1] - 0.45, c[2]), r, n, 0.35, 0.4, 'vx_fire' if star else 'vx_ring2', phase=0.5)
        for k in range(3):
            a = 2 * math.pi * (k + 0.25) / 3
            R.append(E((c[0] + r * math.cos(a) - 0.5, c[1] - 0.9, c[2] + r * math.sin(a) - 0.5), (c[0] + r * math.cos(a) + 0.5, c[1] + 0.9, c[2] + r * math.sin(a) + 0.5),
                       'vx_fire_l' if star else 'vx_hull', light=15 if star else 0))
    if star:                                                  # (flames licking up off it)
        rnd = random.Random(90 + i)
        for k in range(0, n, 2):
            a = 2 * math.pi * (k + 0.5) / n; ca, sa = math.cos(a), math.sin(a); h = rnd.uniform(0.8, 2.2)
            R.append(seg((c[0] + r * ca, c[1] + 0.3, c[2] + r * sa), (c[0] + (r + 0.4) * ca, c[1] + 0.3 + h, c[2] + (r + 0.4) * sa), 0.5, 0.4, 'vx_fire_l', _PV[0], FRONT, 0.05, light=15))
    return R


# ==================================================================================================== FX
def _fx(kind):
    """(on the head) the warframe's scan and Vexis's eye fx"""
    X, Y, Z = _PV[0]; F = []
    if kind == 'charge':                                      # (light gathering at both eyes, motes drawn in)
        for sx in (1, -1):
            F += [GEM((X + sx * 1.6, Y, Z - 0.6), 1.2, 'vx_glow_l'), GEM((X + sx * 1.6, Y, Z - 0.6), 2.0, 'vx_glow', rot=(0.0, 0.0, 45.0))]
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); r = 5.5 if a % 60 == 0 else 4.0
            F.append(seg((X + 2.6 * ca, Y + 2.6 * sa, Z - 0.8), (X + r * ca, Y + r * sa, Z - 0.6), 0.3, 0.3, 'vx_glow_l', _PV[0], ext=0, light=15))
    elif kind == 'beam':                                      # (two beams from the eyes, braiding into one, rings down it)
        for sx in (1, -1):
            F.append(seg((X + sx * 1.6, Y, Z - 0.4), (X, Y - 0.6, Z - 9.0), 0.8, 0.8, 'vx_glow_l', _PV[0], ext=0.2, light=15))
        F += [E((X - 0.8, Y - 1.4, Z - 44.0), (X + 0.8, Y + 0.2, Z - 8.6), 'vx_glow_l', light=15),
              E((X - 1.6, Y - 2.2, Z - 42.0), (X + 1.6, Y + 1.0, Z - 9.0), 'vx_glow', light=15, faces=('east', 'west', 'up', 'down'))]
        for k in range(2, 7):
            z = Z - 6.4 * k; r = 2.4 - 0.12 * k
            F.append(E((X - r, Y - 0.6 - r, z - 0.35), (X + r, Y - 0.6 + r, z + 0.35), 'vx_glow', light=15))
    elif kind == 'bolt':                                      # (the follower's: a green shard flying, its trail)
        F += [GEM((X, Y, Z - 7.0), 1.4, 'vx_glow_l', rot=(0.0, 0.0, 45.0)),
              E((X - 0.35, Y - 0.35, Z - 6.4), (X + 0.35, Y + 0.35, Z - 1.6), 'vx_glow', light=15)]
        for sx in (1, -1):
            F.append(seg((X + sx * 1.6, Y, Z - 0.3), (X + sx * 0.5, Y, Z - 2.2), 0.35, 0.35, 'vx_glow_l', _PV[0], ext=0, light=15))
    elif kind == 'scan':                                      # (the warframe's targeting fan, down ahead of it; a reticle at each end)
        for k in range(-3, 4):
            a = math.radians(k * 11); L = 30.0
            B = (X + L * math.sin(a), Y - 20.0, Z - L * math.cos(a))
            F.append(seg((X, Y, Z - 0.3), B, 0.25, 0.25, 'vx_glow_l', _PV[0], ext=0, light=15))
            F += [E((B[0] - 1.4, B[1] - 0.15, B[2] - 1.4), (B[0] + 1.4, B[1] + 0.15, B[2] + 1.4), 'vx_red', light=15, faces=('up', 'down'),
                    rot=((0.0, 45.0, 0.0), B))]
    else:                                                     # sparks: the link burning out - arcs and sparks round the skull
        rnd = random.Random(55)
        for i in range(10):
            a = 2 * math.pi * i / 10 + rnd.uniform(-0.2, 0.2); r = rnd.uniform(3.6, 5.2)
            p0 = (X + r * math.cos(a), Y + 1.5 + r * math.sin(a) * 0.9, Z + 5.0 + rnd.uniform(-2, 2))
            p1 = (p0[0] + rnd.uniform(-1.2, 1.2), p0[1] + rnd.uniform(-1.4, 1.4), p0[2] + rnd.uniform(-1, 1))
            p2 = (p1[0] + rnd.uniform(-1.0, 1.0), p1[1] + rnd.uniform(-1.2, 1.2), p1[2] + rnd.uniform(-1, 1))
            t = 'vx_glow_l' if i % 2 else 'vx_hot'
            F += [seg(p0, p1, 0.22, 0.22, t, _PV[0], FRONT, 0.05, light=15), seg(p1, p2, 0.2, 0.2, t, _PV[0], FRONT, 0.05, light=15),
                  GEM(p2, 0.5, 'vx_hot')]
    return F


def _fxh(kind):
    """(in the right hand / at the cannon's muzzle; its 'forward' is the forearm's -y)"""
    X, Y, Z = _PV[0]; F = []
    if kind == 'plasma_c':                                    # (the cannon charging: a ball of plasma at the bore, rays, motes drawn in)
        F += [GEM((X, Y - 1.4, Z), 2.4, 'vx_glow_l'), GEM((X, Y - 1.4, Z), 3.8, 'vx_glow', rot=(45.0, 0.0, 45.0))]
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); r = 7.0 if a % 60 == 0 else 5.0
            F.append(seg((X + 2.6 * ca, Y - 1.4, Z + 2.6 * sa), (X + r * ca, Y - 1.0, Z + r * sa), 0.35, 0.35, 'vx_glow_l', _PV[0], ext=0, light=15))
    elif kind == 'plasma':                                    # (the beam: a white-green core in a sheath, rings down it, a flash at the bore)
        F += [E((X - 1.0, Y - 46.0, Z - 1.0), (X + 1.0, Y - 0.4, Z + 1.0), 'vx_hot', light=15),
              E((X - 2.0, Y - 44.0, Z - 2.0), (X + 2.0, Y - 1.0, Z + 2.0), 'vx_glow_l', light=15, faces=('north', 'south', 'east', 'west')),
              GEM((X, Y - 1.0, Z), 3.4, 'vx_glow_l')]
        for k in range(1, 7):
            y = Y - 6.6 * k; r = 3.0 - 0.15 * k
            F.append(E((X - r, y - 0.35, Z - r), (X + r, y + 0.35, Z + r), 'vx_glow', light=15))
    elif kind == 'well':                                      # (a gravity well held below the palm: a black core, a green accretion ring, streaks in)
        c = (X, Y - 3.4, Z - 0.6)
        F += [GEM(c, 2.6, 'vx_void', light=0)] + RING(c, 2.8, 14, 0.35, 0.3, 'vx_glow_l')
        for a in range(0, 360, 45):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            F.append(seg((c[0] + 5.2 * ca, c[1] + 1.2 * sa, c[2] + 5.2 * sa), (c[0] + 3.4 * ca, c[1] + 0.6 * sa, c[2] + 3.4 * sa), 0.25, 0.25, 'vx_glow', _PV[0], ext=0, light=15))
    elif kind == 'sun':                                       # (a star gathered in the palm: white-gold, fire round it, rays)
        c = (X, Y - 2.2, Z)
        F += [GEM(c, 2.2, 'vx_hot'), GEM(c, 3.4, 'vx_fire_l', rot=(45.0, 0.0, 45.0)), GEM(c, 4.4, 'vx_fire', rot=(0.0, 45.0, 0.0))]
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); r = 6.8 if a % 60 == 0 else 5.0
            F.append(seg((c[0] + 2.4 * ca, c[1] + 2.4 * sa, c[2]), (c[0] + r * ca, c[1] + r * sa, c[2]), 0.4, 0.4, 'vx_fire_l', _PV[0], ext=0, light=15))
    elif kind == 'lance':                                     # (the solar lance: a white-gold core, fire round it, from the fingertips)
        F += [E((X - 0.9, Y - 46.0, Z - 0.9), (X + 0.9, Y - 1.0, Z + 0.9), 'vx_hot', light=15),
              E((X - 1.8, Y - 44.0, Z - 1.8), (X + 1.8, Y - 1.6, Z + 1.8), 'vx_fire_l', light=15, faces=('north', 'south', 'east', 'west')),
              GEM((X, Y - 1.4, Z), 3.0, 'vx_hot')]
        for k in range(1, 7):
            y = Y - 6.4 * k; r = 2.8 - 0.12 * k
            F.append(E((X - r, y - 0.3, Z - r), (X + r, y + 0.3, Z + r), 'vx_fire', light=15, rot=('y', 45, (X, y, Z))))
    elif kind == 'flare':                                     # (the star-flare: a fan of fire thrown out of the hand)
        rnd = random.Random(77)
        for k in range(-4, 5):
            a = math.radians(k * 10); L = rnd.uniform(15, 22)
            B = (X + L * math.sin(a), Y - L * math.cos(a), Z + rnd.uniform(-1.5, 1.5))
            M = (X + L * 0.5 * math.sin(a), Y - L * 0.5 * math.cos(a), Z)
            F += [seg((X, Y - 0.6, Z), M, 1.6, 1.0, 'vx_fire_l', _PV[0], FRONT, 0.1, light=15), seg(M, B, 1.1, 0.7, 'vx_fire', _PV[0], FRONT, 0.1, light=15)]
        F.append(GEM((X, Y - 1.0, Z), 2.8, 'vx_hot'))
    else:                                                     # deflect: a shield of hard light held out (a grid, an edge of light)
        c = (X, Y - 3.0, Z)
        F.append(E((c[0] - 4.4, c[1] - 0.15, c[2] - 4.4), (c[0] + 4.4, c[1] + 0.15, c[2] + 4.4), 'vx_shield', light=15))
        for sx in (1, -1):
            F += [E((c[0] + sx * 4.4 - 0.25, c[1] - 0.3, c[2] - 4.4), (c[0] + sx * 4.4 + 0.25, c[1] + 0.3, c[2] + 4.4), 'vx_glow_l', light=15),
                  E((c[0] - 4.4, c[1] - 0.3, c[2] + sx * 4.4 - 0.25), (c[0] + 4.4, c[1] + 0.3, c[2] + sx * 4.4 + 0.25), 'vx_glow_l', light=15)]
    return F


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(5)
    def mk(part, form, fn, *a):
        _PV[0] = joints(form)[part]; return (part, fn(*a))
    R = {}
    for form in FORMS:
        for f in (None,) + (FACES[:4] if form == 'warframe' else FACES):
            R[f'{PREFIX}head_{form}{"_x" + f if f else ""}'] = (('head', _grow(mk('head', form, _w_head, f)[1], W_HEAD_K, (0.0, 0.0, -1.0))) if form == 'warframe'
                                                                 else mk('head', form, _a_head, form, f))
    W = 'warframe'
    for lit, d in ((True, ''), (False, '_off')):
        R[f'{PREFIX}body_w{d}'] = mk('body', W, _w_body, lit); R[f'{PREFIX}chest_w{d}'] = mk('chest', W, _w_chest, lit)
        R[f'{PREFIX}back_w{d}'] = mk('back', W, _w_back, lit); R[f'{PREFIX}forer_w{d}'] = mk('forer', W, _w_cannon, lit)
    R[f'{PREFIX}forel_w'] = mk('forel', W, _w_claw)
    for sx, s in ((1, 'r'), (-1, 'l')):
        R[f'{PREFIX}arm{s}_w'] = mk(f'arm{s}', W, _w_arm, sx)
        R[f'{PREFIX}leg{s}_w'] = mk(f'leg{s}', W, _w_leg, sx); R[f'{PREFIX}shin{s}_w'] = mk(f'shin{s}', W, _w_shin, sx)
        R[f'{PREFIX}foot{s}_w'] = mk(f'foot{s}', W, _w_foot, sx)
        R[f'{PREFIX}pod{s}_shut'] = mk(f'pod{s}', W, _w_pod, sx, False); R[f'{PREFIX}pod{s}_open'] = mk(f'pod{s}', W, _w_pod, sx, True)
    for form, tag in (('hivelink', 'h'), ('starfire', 's')):
        R[f'{PREFIX}body_{tag}'] = mk('body', form, _a_body, form)
        for sx, s in ((1, 'r'), (-1, 'l')):
            R[f'{PREFIX}arm{s}_{tag}'] = mk(f'arm{s}', form, _a_arm, sx, form); R[f'{PREFIX}fore{s}_{tag}'] = mk(f'fore{s}', form, _a_fore, sx, form)
            R[f'{PREFIX}leg{s}_{tag}'] = mk(f'leg{s}', form, _a_leg, sx, form); R[f'{PREFIX}shin{s}_{tag}'] = mk(f'shin{s}', form, _a_shin, sx, form)
            R[f'{PREFIX}foot{s}_{tag}'] = mk(f'foot{s}', form, _a_foot, sx, form)
        R[f'{PREFIX}ring2_{tag}'] = mk('ring2', form, _a_ring, 2, form)
    for form, tag in (('hivelink', 'h'), ('starfire', 's'), ('unlinked', 'u')):
        R[f'{PREFIX}chest_{tag}'] = mk('chest', form, _a_chest, form); R[f'{PREFIX}back_{tag}'] = mk('back', form, _a_back, form)
        R[f'{PREFIX}ring1_{tag}'] = mk('ring1', form, _a_ring, 1, form)
    R[f'{PREFIX}ring1_w'] = R[f'{PREFIX}ring1_h']; R[f'{PREFIX}ring2_w'] = R[f'{PREFIX}ring2_h']      # (hidden on the warframe)
    for k in FX_HEAD: R[f'{PREFIX}fx_{k}'] = mk('fx', 'warframe' if k == 'scan' else 'hivelink', _fx, k)
    for k in FX_HAND: R[f'{PREFIX}fxh_{k}'] = mk('fxh', 'warframe' if k.startswith('plasma') else 'hivelink', _fxh, k)
    _RAW.update(R)
    return _RAW


def models():
    M = {}
    for name, (part, els) in _build().items():
        k = PART_K.get(part, 1.0)
        els = shrink(els, k) if k != 1.0 else els
        for e in els:                                         # (every element inside the model box, every uv on the texture)
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
            for fc in e['faces'].values():
                u1, v1, u2, v2 = fc['uv']
                assert all(0.0 <= t <= 16.0 for t in (u1, v1, u2, v2)), (name, fc['uv'])
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


def rp(R):
    """gen_rp (as phase238 does for the Sovereign): the vx_ textures through TEXTURE_MODS, every part's model as a 3D model"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)


# ---------------------------------------------------------------------------------------------------- world boxes (grounding, clip checks)
def _rotm(r):
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if 'axis' in r: return {'x': rx, 'y': ry, 'z': rz}[r['axis']](math.radians(r['angle']))
    return mm(mm(rz(math.radians(r.get('z', 0))), ry(math.radians(r.get('y', 0)))), rx(math.radians(r.get('x', 0))))


def world_boxes(pose, parts=None):
    """{part: [(centre, (axis, axis, axis), half extents)]} - each shown element as a box in the world (display frame, design
    units), as the pose stands (an alien part's model is built about its own joint: the pose's _o_ shifts carry it there)"""
    raw = _build(); xf = rigkit.solve(PIVOT, PARENT, pose); out = {}
    jt = joints(pose.get('_form', 'unlinked'))
    for p in (parts or PARTS):
        if HIDDEN(p, pose): continue
        Q, t = xf[p]; dp = D(PIVOT[p]); W = tuple(t[i] + dp[i] for i in range(3)); jp = jt[p]
        bl = []
        for e in raw[model_name(p, pose)][1]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 for i in range(3))                             # (model -> design, about its joint)
            cw = qrot(Q, D(cd))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h)))
        out[p] = bl
    return out


def lowest(pose, parts):
    lo = 1e9
    for bl in world_boxes(pose, parts).values():
        for c, ax, h in bl:
            lo = min(lo, c[1] - sum(abs(ax[i][1]) * h[i] for i in range(3)))
    return lo


def fit(pose):
    """an alien pose's '_o_' shifts: solved from its turns so every joint stands where the alien's skeleton (JA) has it, though
    the displays stand at the warframe's (PIVOT). The warframe's poses need none."""
    pose = {k: v for k, v in pose.items() if not k.startswith('_o_')}
    J = joints(pose.get('_form', 'unlinked'))
    if J is PIVOT: return pose
    xt = rigkit.solve(J, PARENT, pose)
    Wt = {p: tuple(xt[p][1][i] + D(J[p])[i] for i in range(3)) for p in PARTS}
    for p in rigkit.order(PARENT):
        par = PARENT[p]
        if par is None:
            o = tuple(D(J[p])[i] - D(PIVOT[p])[i] for i in range(3))
        else:
            r = qrot(xt[par][0], tuple(D(PIVOT[p])[i] - D(PIVOT[par])[i] for i in range(3)))
            o = tuple(Wt[p][i] - Wt[par][i] - r[i] for i in range(3))
        if max(abs(v) for v in o) > 1e-6: pose['_o_' + p] = tuple(round(v, 5) for v in D(o))
    return pose


def qa_x(d):
    return rigkit.qa('x', d)


GROUND_PARTS = ('body', 'legr', 'legl', 'shinr', 'shinl', 'footr', 'footl')
LEGS = GROUND_PARTS[1:]                        # (seated: the tabard and the mantle fold away into the deck)


def ground(pose, parts=GROUND_PARTS, lift=0.0):
    """set the root's height so the lowest point of these parts rests on y=0 (lift: that far above it - a hover)"""
    pose = dict(pose); o = pose.get('_off', (0.0, 0.0, 0.0)); pose['_off'] = (o[0], 0.0, o[2])
    lo = lowest(pose, parts); pose['_off'] = (o[0], round(-lo + lift, 4), o[2])
    return pose


def hang(p, flow=0.0):
    """the mantle hangs by the world's down, whatever the chest is doing (flow: swept back by its going), and is swung back until
    its hem clears the floor (unless _pool: seated, let it pool)"""
    p = dict(p)
    Qc = rigkit.solve(PIVOT, PARENT, p)['chest'][0]; u = qrot(Qc, (0.0, 1.0, 0.0))
    pitch = math.degrees(math.atan2(u[2], u[1]))
    p['back'] = rigkit.qmul(qa_x(-pitch + flow), p.get('back', rigkit.I))
    for _ in range(0 if p.get('_pool') else 20):
        if lowest(p, ('back',)) >= 0.4: break
        p['back'] = rigkit.qmul(qa_x(4.0), p['back'])
    return p


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit, display frame: ('x', +a) leans a trunk forward / nods the head down; limb(fwd) swings a hanging limb forward, (out)
#  out to its own side and up; a shin bends back with knee(a); ('y', +a) on the chest turns its right shoulder forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def knee(a):
    return qs(('x', a))


def T(lean=0.0, twist=0.0, side=0.0):
    return qs(('y', twist), ('x', lean), ('z', side))


def P(**kw):
    return kw


s_ = math.sin


def mleg(sx, hip=0.0, kn=0.0, out=2.0, bx=0.0, toe=0.0):
    """a digitigrade leg (the warframe's): the thigh swung forward (hip), the shin back (kn) - the foot kept level (bx: the
    pelvis's own lean), or tipped toe-down by toe"""
    s = 'r' if sx > 0 else 'l'
    return {f'leg{s}': limb(sx, hip, out), f'shin{s}': knee(kn), f'foot{s}': qa_x(hip - kn - bx + toe)}


def mlegs(hip=8.0, kn=14.0, out=2.0, bx=0.0):
    return dict(**mleg(1, hip, kn, out, bx), **mleg(-1, hip, kn, out, bx))


def dangle(swing=0.0, spread=5.0, bend=18.0, point=10.0, sway=0.0):
    """Vexis's legs, hanging under it as it floats (swing: trailed back if negative)"""
    return dict(legr=limb(1, swing + sway, spread), shinr=knee(bend), footr=qa_x(point), legl=limb(-1, swing - sway, spread), shinl=knee(bend), footl=qa_x(point))


def rings(spin=0.0, t1=(8.0, 22.0), t2=(-26.0, -10.0)):
    """the gravity rings: each tilted (z, x), spun about its own axis (they orbit as the poses go by)"""
    return dict(ring1=qs(('z', t1[0]), ('x', t1[1]), ('y', spin)), ring2=qs(('z', t2[0]), ('x', t2[1]), ('y', -spin)))


def _wf(name):
    """the warframe's boss poses"""
    face_hot = 'wide'
    IDLE_ARMS = dict(armr=limb(1, 10, 6), forer=limb(1, 34), arml=limb(-1, 8, 10), forel=limb(-1, 26))
    lowall = False
    if name == 'idle_a':
        p = P(chest=T(6), head=T(6), **mlegs(8, 14), **IDLE_ARMS)
    elif name == 'idle_b':                                    # (scanning the room: the head turning, the claw flexing)
        p = P(_face='narrowed', chest=T(3, -10), head=T(0, 22, 2), **mlegs(8, 14), armr=limb(1, 16, 8), forer=limb(1, 44),
              arml=limb(-1, 4, 14), forel=limb(-1, 52))
    elif name.startswith('walk_'):                            # (heavy: a stomping stride, the hull rolling over it)
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = P(chest=T(9, 5 * sw), head=T(6, -3 * sw), **mleg(1, 8 + 18 * sw, 14 + 26 * max(0, -s_(ph + 0.6))),
              **mleg(-1, 8 - 18 * sw, 14 + 26 * max(0, s_(ph + 0.6))),
              armr=limb(1, 10 - 8 * sw, 6), forer=limb(1, 34), arml=limb(-1, 8 + 8 * sw, 10), forel=limb(-1, 26))
    elif name == 'roar':                                      # (rearing back, the arms flung out, the pods open, the visor blazing)
        p = P(_face='wide', _pods='open', chest=T(-14), head=T(-18), **mlegs(12, 22, 6), armr=limb(1, 30, 48), forer=limb(1, 40),
              arml=limb(-1, 30, 48), forel=limb(-1, 40))
    elif name == 'stagger':                                   # (between phases: down on its right knee, the cannon dark and braced on the deck)
        p = P(_face='dim', _power=2, chest=T(22, 12, -6), head=T(18, -16, 8), **mleg(1, 58, 112, 4), **mleg(-1, 26, 46, 4),
              armr=limb(1, 26, 14), forer=limb(1, 6), arml=limb(-1, 34, 18), forel=limb(-1, 72))
        lowall = True
    elif name == 'cannon_up':                                 # (the cannon swung out to its right and raised, charging)
        p = P(_face='narrowed', _fx='plasma_c', chest=T(4, -24), head=T(2, 16), **mleg(1, 4, 12, 5), **mleg(-1, 18, 28, 5),
              armr=limb(1, 70, 30, -10), forer=limb(1, 24), arml=limb(-1, 24, 26), forel=limb(-1, 30))
    elif name == 'cannon':                                    # (and the sweep: the plasma beam carved across the deck, right to left)
        p = P(_face=face_hot, _fx='plasma', chest=T(8, 24), head=T(4, -14), **mleg(1, 18, 28, 5), **mleg(-1, 4, 12, 5),
              armr=limb(1, 62, 20, 14), forer=limb(1, 22), arml=limb(-1, -10, 30), forel=limb(-1, 30))
    elif name == 'missiles':                                  # (the pods open and tipped up, the claw marking targets, the visor scanning)
        p = P(_face='narrowed', _pods='open', _fx='scan', chest=T(-6), head=T(-4), **mlegs(12, 20, 5), podr=qa_x(-28), podl=qa_x(-28),
              armr=limb(1, 4, 20), forer=limb(1, 36), arml=limb(-1, 74, 12), forel=limb(-1, 12))
    elif name == 'stomp_up':                                  # (the right foot raised high)
        p = P(_face='narrowed', chest=T(-8, 8), head=T(6), **mleg(1, 58, 52, 3), **mleg(-1, 14, 26, 4),
              armr=limb(1, 20, 34), forer=limb(1, 30), arml=limb(-1, 20, 34), forel=limb(-1, 30))
    elif name == 'stomp':                                     # (and down: the shockwave, the hull thrown forward over it)
        p = P(_face=face_hot, chest=T(18), head=T(8), **mleg(1, 28, 36, 3), **mleg(-1, 4, 40, 4),
              armr=limb(1, 30, 18), forer=limb(1, 30), arml=limb(-1, 30, 18), forel=limb(-1, 34))
    elif name == 'deploy':                                    # (drop-pods: the pods open, the claw raised high - the order given)
        p = P(_face=face_hot, _pods='open', chest=T(-10, -8), head=T(-8, 12), **mlegs(8, 14, 4), podr=qa_x(-12), podl=qa_x(-12),
              armr=limb(1, 6, 16), forer=limb(1, 24), arml=limb(-1, 136, 12), forel=limb(-1, 16))
    elif name == 'dormant':                                   # (powered down at the helm: folded on its legs, slumped, the arms on the deck)
        p = P(_face='closed', _power=0, chest=T(28), head=T(26), **mlegs(62, 118, 4),
              armr=limb(1, 22, 6), forer=limb(1, 18), arml=limb(-1, 26, 8), forel=limb(-1, 22))
        lowall = True
    elif name == 'wake_0':                                    # (the reactor lights; the visor glimmers; the head lifts)
        p = P(_face='dim', _power=1, chest=T(26), head=T(14), **mlegs(62, 118, 4),
              armr=limb(1, 22, 6), forer=limb(1, 18), arml=limb(-1, 26, 8), forel=limb(-1, 22))
        lowall = True
    elif name == 'wake_1':                                    # (the hull and the cockpit light; the claw pushes off the deck)
        p = P(_face='dim', _power=2, chest=T(20, -6), head=T(4, 6), **mleg(1, 56, 106, 4), **mleg(-1, 50, 96, 4),
              armr=limb(1, 22, 8), forer=limb(1, 18), arml=limb(-1, 10, 20), forel=limb(-1, 0))
        lowall = True
    elif name == 'rise':                                      # (rising off its haunches)
        p = P(_face='narrowed', _power=2, chest=T(14), head=T(2), **mleg(1, 34, 64, 3), **mleg(-1, 28, 54, 3),
              armr=limb(1, 24, 10), forer=limb(1, 30), arml=limb(-1, 20, 20), forel=limb(-1, 30))
    elif name == 'wake_2':                                    # (standing: the cannon and the backpack light, the cannon lifted)
        p = P(_face='narrowed', _power=3, chest=T(4), head=T(-4), **mlegs(8, 14), armr=limb(1, 42, 10), forer=limb(1, 40),
              arml=limb(-1, 30, 24), forel=limb(-1, 60))
    elif name == 'wake_3':                                    # (every system up: the arms spread, the pods open, the visor wide)
        p = P(_face='wide', _pods='open', chest=T(-8), head=T(-10), **mlegs(10, 18, 4), armr=limb(1, 30, 40), forer=limb(1, 50),
              arml=limb(-1, 30, 40), forel=limb(-1, 50))
    # ---- as a follower (the companion and full-size warframe): resting, glad, hurt
    elif name == 'sit_a':                                     # (resting: down on one knee, systems idling - the visor still lit, the cannon grounded)
        p = P(_power=1, chest=T(12, -4), head=T(6, 8), **mleg(1, 50, 104, 4), **mleg(-1, 22, 40, 4),
              armr=limb(1, 18, 10), forer=limb(1, 10), arml=limb(-1, 34, 14), forel=limb(-1, 56))
        lowall = True
    elif name == 'sit_b':                                     # (its idle breath: the hull settling, the head turning to you)
        p = P(_power=1, _face='narrowed', chest=T(14, 2), head=T(8, -14, -3), **mleg(1, 52, 106, 4), **mleg(-1, 23, 42, 4),
              armr=limb(1, 18, 10), forer=limb(1, 10), arml=limb(-1, 32, 16), forel=limb(-1, 62))
        lowall = True
    elif name == 'happy':                                     # (pleased: the claw raised in a wave, the head cocked, the pods popping open)
        p = P(_face='wide', _pods='open', chest=T(-4, -6), head=T(-6, 10, 10), **mlegs(10, 18, 3),
              armr=limb(1, 16, 14), forer=limb(1, 40), arml=limb(-1, 118, 26), forel=limb(-1, 34))
    elif name == 'hurt':                                      # (a flinch: rocked back, the claw up to guard the cockpit, the visor flickering)
        p = P(_face='dim', chest=T(-12, 12), head=T(-14, -14), **mleg(1, 2, 12, 4), **mleg(-1, 22, 40, 4),
              armr=limb(1, 24, 24), forer=limb(1, 36), arml=limb(-1, 60, -6, 30), forel=limb(-1, 86))
    else:
        raise KeyError(name)
    p['_form'] = 'warframe'
    return ground(p, PARTS if lowall else GROUND_PARTS)


def _alien(name, form):
    """Vexis's boss poses (hivelink, starfire) - None where the move isn't that form's"""
    star = form == 'starfire'
    H = HOVER; lift, flow = H, 0.0
    if name == 'idle_a':
        p = P(chest=T(6), head=T(8), armr=limb(1, 8, 12), forer=limb(1, 18), arml=limb(-1, 8, 12), forel=limb(-1, 18), **dangle(), **rings(0))
        if star: p.update(armr=limb(1, 14, 22), forer=limb(1, 30), arml=limb(-1, 14, 22), forel=limb(-1, 30))
    elif name == 'idle_b':                                    # (the head cocked - studying you - one hand lifted, the fingers moving)
        p = P(_face='narrowed', chest=T(2, -8), head=T(-2, 20, 12), armr=limb(1, 26, 14), forer=limb(1, 56), arml=limb(-1, 4, 16), forel=limb(-1, 14),
              **dangle(-4, 5, 22, 14, 3), **rings(60))
        lift = H + 1.0
    elif name.startswith('walk_'):                            # (drifting: leaning into it, the arms and legs trailing, the rings turning)
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = P(chest=T(14, 4 * sw), head=T(2, -3 * sw), armr=limb(1, -14 + 6 * sw, 14), forer=limb(1, 12), arml=limb(-1, -14 - 6 * sw, 14), forel=limb(-1, 12),
              **dangle(-18, 5, 26, 20, 6 * sw), **rings(90 * k))
        lift, flow = H + 0.8 * s_(2 * ph), 10.0
    elif name == 'roar':                                      # (head back, arms flung up and wide, the rings flared)
        p = P(_face='wide', chest=T(-16), head=T(-22), armr=limb(1, 50, 72), forer=limb(1, 24), arml=limb(-1, 50, 72), forel=limb(-1, 24),
              **dangle(-6, 12, 12, 0), **rings(30, (16, 34), (-40, -20)))
        lift = H + 2.0
    elif name == 'stagger':                                   # (struck: doubled over, a hand to the breast, sinking, the rings slipping)
        p = P(_face='dim', chest=T(24, 10), head=T(24, -12, 8), armr=limb(1, 30, 6), forer=limb(1, 92), arml=limb(-1, -10, 26), forel=limb(-1, 22),
              **dangle(10, 6, 10, 4), **rings(20, (24, 44), (-10, 30)))
        lift = H - 2.0
    elif name == 'rise':                                      # (climbing out of the torn warframe: hunched low, reaching up, glaring)
        if star: return None
        p = P(_face='narrowed', chest=T(34), head=T(-30), armr=limb(1, 120, 18), forer=limb(1, 6), arml=limb(-1, 44, 28), forel=limb(-1, 56),
              **dangle(60, 10, 100, -10), **rings(0, (10, 60), (-30, 50)))
        lift = 0.6
    elif name == 'gravity':                                   # (the arms out, the palms turned in, pulling - the rings stood up round it)
        if star: return None
        p = P(_face='wide', _fx='well', chest=T(-4), head=T(6), armr=limb(1, 46, 64), forer=limb(1, 56), arml=limb(-1, 46, 64), forel=limb(-1, 56),
              **dangle(-4, 8, 14, 6), ring1=qs(('x', 90)), ring2=qs(('z', 90), ('x', 20)))
        lift = H + 1.0
    elif name == 'beam_up':                                   # (the hands to its temples, the head drawn back: the eyes charging)
        if star: return None
        p = P(_face='wide', _fx='charge', chest=T(-8), head=T(-12), armr=limb(1, 70, 34, 30), forer=limb(1, 112), arml=limb(-1, 70, 34, 30), forel=limb(-1, 112),
              **dangle(-2, 6, 18, 10), **rings(45, (18, 30), (-36, -16)))
    elif name == 'beam':                                      # (the improvement beam: the head thrust at you, the arms flung back)
        if star: return None
        p = P(_face='narrowed', _fx='beam', chest=T(12), head=T(10), armr=limb(1, -34, 40), forer=limb(1, 12), arml=limb(-1, -34, 40), forel=limb(-1, 12),
              **dangle(-14, 6, 22, 16), **rings(90, (4, 14), (-20, -6)))
    elif name == 'clone':                                     # (splitting: the arms spread level, the head bowed, the eyes shut, the rings stood on edge)
        if star: return None
        p = P(_face='closed', chest=T(4), head=T(20), armr=limb(1, 14, 78), forer=limb(1, 34, 0, -20), arml=limb(-1, 14, 78), forel=limb(-1, 34, 0, -20),
              **dangle(0, 3, 22, 14), ring1=qs(('z', 60), ('x', 80)), ring2=qs(('z', -60), ('x', 80)))
    elif name == 'summon':                                    # (the arms raised high: calling the swarm)
        if star: return None
        p = P(_face='wide', chest=T(-10), head=T(-16), armr=limb(1, 150, 28), forer=limb(1, 12), arml=limb(-1, 150, 28), forel=limb(-1, 12),
              **dangle(-4, 8, 14, 6), **rings(120, (10, 40), (-30, -40)))
        lift = H + 2.0
    elif name == 'flare_up':                                  # (the right hand drawn across to its left, a star gathering in it)
        if not star: return None
        p = P(_face='narrowed', _fx='sun', chest=T(6, 30), head=T(4, -24), armr=limb(1, 58, -10, 50), forer=limb(1, 60), arml=limb(-1, -10, 40), forel=limb(-1, 30),
              **dangle(-6, 6, 18, 10), **rings(30, (14, 30), (-30, -18)))
    elif name == 'flare':                                     # (and flung out to its right: the star-flare thrown across the deck)
        if not star: return None
        p = P(_face='wide', _fx='flare', chest=T(8, -28), head=T(2, 18), armr=limb(1, 74, 50, -16), forer=limb(1, 10), arml=limb(-1, 20, 50), forel=limb(-1, 30),
              **dangle(-10, 8, 14, 10), **rings(90, (4, 18), (-20, -6)))
    elif name == 'lance_up':                                  # (the right hand raised high: a star in it)
        if not star: return None
        p = P(_face='wide', _fx='sun', chest=T(-10, -10), head=T(-18), armr=limb(1, 166, 14), forer=limb(1, 8), arml=limb(-1, 30, 40), forel=limb(-1, 50),
              **dangle(-4, 6, 16, 8), **rings(60, (12, 36), (-34, -24)))
        lift = H + 1.5
    elif name == 'lance':                                     # (thrust out: the solar lance from its fingertips)
        if not star: return None
        p = P(_face='narrowed', _fx='lance', chest=T(10, 18), head=T(4, -12), armr=limb(1, 84, 4, 6), forer=limb(1, 4), arml=limb(-1, -24, 36), forel=limb(-1, 20),
              **dangle(-16, 6, 22, 16), **rings(120, (4, 12), (-20, -4)))
    elif name == 'frenzy':                                    # (IMPROVE. IMPROVE. IMPROVE: thrashing, the rings wild)
        if not star: return None
        p = P(_face='wide', chest=T(-6, -22, 12), head=T(-22, 26, -16), armr=limb(1, 126, 60), forer=limb(1, 46), arml=limb(-1, 70, 82), forel=limb(-1, 64),
              **dangle(-10, 14, 30, 0, 12), ring1=qs(('z', 40), ('x', 60), ('y', 30)), ring2=qs(('z', -70), ('x', -20), ('y', 80)))
        lift = H + 3.0
    elif name == 'death_0':                                   # (the link severed: convulsing, arched back, arms rigid, the implants sparking)
        if not star: return None
        p = P(_face='wide', _fx='sparks', chest=T(-26, 8), head=T(-30, 14), armr=limb(1, 20, 76), forer=limb(1, 4), arml=limb(-1, 34, 70), forel=limb(-1, 4),
              **dangle(-12, 14, 6, -4), **rings(40, (30, 50), (-50, -30)))
        lift = H + 1.0
    elif name == 'death_1':                                   # (the hands to its skull, sinking, the rings slack and falling)
        if not star: return None
        p = P(_face='dim', _fx='sparks', chest=T(28), head=T(30), armr=limb(1, 104, 34, 20), forer=limb(1, 118), arml=limb(-1, 104, 34, 20), forel=limb(-1, 118),
              **dangle(10, 6, 30, 6), **rings(60, (40, 60), (-60, 50)))
        lift = 1.2
    elif name == 'death_2':                                   # (down: kneeling on the deck, the hands on its thighs, the head bowed - "...one.")
        if not star: return None
        p = P(_face='dim', body=T(-6), chest=T(16), head=T(28), legr=limb(1, 84, 8), shinr=knee(140), footr=qa_x(-40), legl=limb(-1, 84, 8), shinl=knee(140), footl=qa_x(-40),
              armr=limb(1, 32, 4), forer=limb(1, 34), arml=limb(-1, 32, 4), forel=limb(-1, 34), ring1=qs(('x', 2)), ring2=qs(('x', -3)))
        lift = None
    # ---- as a follower: meditating cross-legged in the air (and its breath), glad, hurt
    elif name in ('sit_a', 'sit_b'):
        b = name == 'sit_b'
        p = P(_face='closed' if not star else 'narrowed', body=T(-2), chest=T(4 if not b else 1), head=T(12 if not b else 6, 0, 0 if not b else 4),
              legr=limb(1, 64, 52, 20), shinr=knee(128), footr=qa_x(-20), legl=limb(-1, 64, 52, 20), shinl=knee(128), footl=qa_x(-20),
              armr=limb(1, 30 if not b else 34, 4), forer=limb(1, 62, 0, 14), arml=limb(-1, 30 if not b else 34, 4), forel=limb(-1, 62, 0, 14),
              ring1=qs(('z', 2), ('x', 6), ('y', 0 if not b else 20)), ring2=qs(('z', -4), ('x', -6), ('y', 0 if not b else -20)))
        lift = H * 0.5 + (0.4 if b else 0.0)
    elif name == 'happy':                                     # (pleased: the long hands opened, the head on one side, the eyes smiling)
        p = P(_face='soft', chest=T(-6), head=T(-4, 0, -14), armr=limb(1, 34, 46), forer=limb(1, 36), arml=limb(-1, 34, 46), forel=limb(-1, 36),
              **dangle(-6, 8, 16, 8), **rings(120, (14, 30), (-34, -16)))
        lift = H + 1.0
    elif name == 'hurt':                                      # (a flinch: thrown back, an arm across its face, the rings jolted)
        p = P(_face='dim', chest=T(-16, 10), head=T(-14, -12), armr=limb(1, 70, 4, 30), forer=limb(1, 96, 0, 20), arml=limb(-1, 20, 34), forel=limb(-1, 40),
              **dangle(14, 8, 12, 4), **rings(20, (22, 40), (-40, 10)))
        lift = H - 0.6
    else:
        raise KeyError(name)
    p['_form'] = form
    p = fit(p)
    if lift is None:
        p = ground(p, GROUND_PARTS + ('forer', 'forel', 'back'))
        p['_pool'] = True
    else:
        p = ground(p, GROUND_PARTS, lift)
    p = hang(p, flow)
    p.pop('_pool', None)
    return p


BOSS_NAMES = {
    'warframe': ['idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'dormant', 'wake_0', 'wake_1', 'rise', 'wake_2', 'wake_3', 'roar',
                 'cannon_up', 'cannon', 'missiles', 'stomp_up', 'stomp', 'deploy', 'stagger', 'sit_a', 'sit_b', 'happy', 'hurt'],
    'hivelink': ['idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'rise', 'roar', 'gravity', 'beam_up', 'beam', 'clone', 'summon', 'stagger',
                 'sit_a', 'sit_b', 'happy', 'hurt'],
    'starfire': ['idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'roar', 'flare_up', 'flare', 'lance_up', 'lance', 'frenzy', 'stagger',
                 'death_0', 'death_1', 'death_2', 'sit_a', 'sit_b', 'happy', 'hurt']}
FOLLOW_KEYS = ('idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'sit_a', 'sit_b', 'happy', 'hurt')   # (what the follower drives a boss form with)
BOSS_POSES = {'warframe': {n: _wf(n) for n in BOSS_NAMES['warframe']},
              **{f: {n: p for n in BOSS_NAMES[f] if (p := _alien(n, f)) is not None} for f in ('hivelink', 'starfire')}}
ENTRANCE = ['dormant', 'wake_0', 'wake_1', 'rise', 'wake_2', 'wake_3', 'roar']           # (the coming, keyframe by keyframe)
BOSS_DRAFT = {f: [n for n in BOSS_NAMES[f] if n not in ('walk_0', 'walk_2', 'walk_3')] for f in BOSS_NAMES}


# ---- the follower (form 'unlinked', at RIG_SCALE)
SWIM_FRAMES = 8


def _fol():
    po = {}
    def F(lift=F_HOVER, flow=0.0, grounded=False, gparts=GROUND_PARTS, **kw):
        p = dict(kw); p['_form'] = 'unlinked'
        p = fit(p)
        p = ground(p, gparts) if grounded else ground(p, GROUND_PARTS, lift)
        p = hang(p, flow); p.pop('_pool', None)
        return p
    R1 = lambda sp=0.0, t=(6.0, 18.0): dict(ring1=qs(('z', t[0]), ('x', t[1]), ('y', sp)))
    po['idle_a'] = F(chest=T(4), head=T(6), armr=limb(1, 12, 8), forer=limb(1, 30), arml=limb(-1, 12, 8), forel=limb(-1, 30), **dangle(), **R1(0))
    # (curious: the head tilted right over, a long finger to its chin)
    po['idle_b'] = F(lift=F_HOVER + 0.6, _face='soft', chest=T(0, -6), head=T(-4, 16, 18), armr=limb(1, 26, 4, 30), forer=limb(1, 118), arml=limb(-1, 6, 12), forel=limb(-1, 40),
                     **dangle(-4, 4, 22, 14, 3), **R1(70))
    for k in range(4):
        ph = math.pi * k / 2; sw = s_(ph)
        po[f'walk_{k}'] = F(lift=F_HOVER + 0.5 * s_(2 * ph), flow=8.0, chest=T(10, 4 * sw), head=T(2, -3 * sw), armr=limb(1, -6 + 8 * sw, 10), forer=limb(1, 20),
                            arml=limb(-1, -6 - 8 * sw, 10), forel=limb(-1, 20), **dangle(-14, 5, 24, 18, 8 * sw), **R1(90 * k))
        po[f'run_{k}'] = F(lift=F_HOVER + 1.0 + 0.6 * s_(2 * ph), flow=22.0, chest=T(26, 5 * sw), head=T(-14), armr=limb(1, -30 + 6 * sw, 16), forer=limb(1, 8),
                           arml=limb(-1, -30 - 6 * sw, 16), forel=limb(-1, 8), **dangle(-40, 6, 20, 30, 6 * sw), **R1(90 * k, (2, 34)))
    po['jump'] = F(lift=F_HOVER + 6.0, _face='wide', chest=T(-4), head=T(-10), armr=limb(1, 40, 30), forer=limb(1, 20), arml=limb(-1, 40, 30), forel=limb(-1, 20),
                   **dangle(20, 8, 50, 10), **R1(40, (0, 4)))
    # sat on the deck, its thin legs out before it, its long hands on its knees, looking about; the ring settled round it
    po['sit_a'] = F(grounded=True, _pool=True, body=T(-10), chest=T(14), head=T(8, -12, 6), legr=limb(1, 84, 12), shinr=knee(16), footr=qa_x(-50),
                    legl=limb(-1, 80, 14), shinl=knee(24), footl=qa_x(-50), armr=limb(1, 24, 16), forer=limb(1, 78), arml=limb(-1, 24, 16),
                    forel=limb(-1, 78), ring1=qs(('x', 2)), gparts=LEGS + ('forer', 'forel'))
    # meditating, floating a little off the deck: legs crossed under it, hands together, eyes shut, the ring turning slowly
    po['sit_b'] = F(lift=1.2, _face='closed', body=T(-2), chest=T(4), head=T(12), legr=limb(1, 64, 52, 20), shinr=knee(128), footr=qa_x(-20),
                    legl=limb(-1, 64, 52, 20), shinl=knee(128), footl=qa_x(-20), armr=limb(1, 34, -2, 20), forer=limb(1, 70, 0, 18), arml=limb(-1, 34, -2, 20),
                    forel=limb(-1, 70, 0, 18), ring1=qs(('x', 4), ('y', 45)))
    # glad (in its quiet way): the arms opening, the head on one side, the eyes smiling, the ring spun up
    po['happy'] = F(lift=F_HOVER + 1.0, _face='soft', chest=T(-4), head=T(-6, 0, -14), armr=limb(1, 30, 44), forer=limb(1, 30), arml=limb(-1, 30, 44), forel=limb(-1, 30),
                    **dangle(-6, 8, 16, 8), **R1(120, (14, 30)))
    po['hurt'] = F(lift=F_HOVER - 0.6, _face='dim', chest=T(-14, 10), head=T(-16, -12), armr=limb(1, 30, 24), forer=limb(1, 40), arml=limb(-1, 20, 30), forel=limb(-1, 50),
                   **dangle(10, 6, 12, 4), **R1(20, (20, 40)))
    # spent: sunk to the deck, legs out, slumped forward over them, the ring lying round it
    po['tired'] = F(grounded=True, _pool=True, _face='closed', body=T(-16), chest=T(34), head=T(30), legr=limb(1, 82, 16), shinr=knee(8), footr=qa_x(-40),
                    legl=limb(-1, 78, 20), shinl=knee(14), footl=qa_x(-40), armr=limb(1, 4, 8), forer=limb(1, 96, 0, 10), arml=limb(-1, 4, 8), forel=limb(-1, 96, 0, 10),
                    ring1=qs(('x', 6), ('z', 4)), gparts=LEGS + ('forer', 'forel'))
    # a gravity swipe: the long hand drawn up and back - and swept down across, the ring flaring
    po['slash_up'] = F(_face='narrowed', chest=T(-4, -24), head=T(0, 18), armr=limb(1, 140, 34), forer=limb(1, 40), arml=limb(-1, 30, 20), forel=limb(-1, 40),
                       **dangle(-6, 5, 20, 12), **R1(30, (10, 26)))
    po['slash'] = F(_face='wide', flow=10.0, chest=T(16, 26), head=T(4, -16), armr=limb(1, 60, 6, 30), forer=limb(1, 10), arml=limb(-1, -20, 24), forel=limb(-1, 20),
                    **dangle(-14, 5, 20, 16), **R1(110, (4, 10)))
    # the eye bolt: the head drawn back, the eyes charging - and the bolt loosed
    po['bolt_up'] = F(_face='wide', _fx='charge', chest=T(-6), head=T(-12), armr=limb(1, 20, 30), forer=limb(1, 50), arml=limb(-1, 20, 30), forel=limb(-1, 50),
                      **dangle(-4, 5, 18, 10), **R1(30))
    po['bolt'] = F(_face='narrowed', _fx='bolt', chest=T(10), head=T(8), armr=limb(1, -10, 24), forer=limb(1, 20), arml=limb(-1, -10, 24), forel=limb(-1, 20),
                   **dangle(-10, 5, 20, 14), **R1(80))
    # its powers: a gravity well held out (palm down), the deflector raised
    po['well'] = F(_face='narrowed', _fx='well', chest=T(4, 10), head=T(6, -8), armr=limb(1, 70, 10, 10), forer=limb(1, 20), arml=limb(-1, 10, 24), forel=limb(-1, 30),
                   **dangle(-6, 5, 18, 12), **R1(60, (16, 30)))
    po['deflect'] = F(_face='wide', _fx='deflect', chest=T(-2, 14), head=T(2, -10), armr=limb(1, 92, 4), forer=limb(1, 0), arml=limb(-1, 10, 28), forel=limb(-1, 40),
                      **dangle(-6, 5, 18, 12), **R1(90, (0, 70)))
    for i in range(SWIM_FRAMES):                              # (gliding through the water like a ray, the arms sweeping, the mantle streaming)
        ph = 2 * math.pi * i / SWIM_FRAMES
        p = dict(_form='unlinked', _off=(0, 10.0, 4.0), body=T(70), chest=T(4), head=T(-44), legr=limb(1, -6 - 10 * s_(ph), 6), shinr=knee(16), footr=qa_x(30),
                 legl=limb(-1, -6 + 10 * s_(ph), 6), shinl=knee(16), footl=qa_x(30), armr=limb(1, 100 + 50 * s_(ph), 30), forer=limb(1, 10),
                 arml=limb(-1, 100 + 50 * s_(ph), 30), forel=limb(-1, 10), **R1(45 * i, (0, 60)))
        po[f'swim_{i}'] = fit(p)
        po[f'swim_{i}']['back'] = qa_x(8 + 6 * s_(ph))           # (streaming back along it)
    return po


POSES = _fol()
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired', 'slash_up', 'slash', 'bolt_up', 'bolt',
         'well', 'deflect', 'swim_2', 'swim_6']
