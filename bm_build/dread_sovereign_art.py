"""THE DREAD SOVEREIGN (draft art): the thing that empowered the Dread - the final, final boss, met after the Malevolent Snowbeast,
the Watchful Witch and the Chomping Sawshark, on its throne at the bottom of the Undercrown (the largest dungeon in the game, hidden
in the Nether). Beaten, it is bound by its own chains and follows you: an endgame follower.

THE LOOK - the Dread armour's source, scaled up into a colossus. Cracked VOID-PLATE (near-black violet, glowing red seams), the
Dread Visage grown into a great crowned helm (a crown of black spikes, two swept horns, a single burning slit of red light for
eyes, more eyes opening on its sides), broad layered pauldrons with spikes, long arms ending in clawed gauntlets, armoured tassets
over armoured legs, talons on the sabatons. A tattered void cloak hangs from its back - it is really SIX WINGS folded down (black
membrane veined in red, the bones along the shoulders, eyes shut in it). Chains hang from it (it was bound once): a bandolier
across the breast, broken manacles at the wrists, chains from the belt. A Dread heart (a dark-red crystal) glows behind the
breastplate. It carries a jagged greatsword of void-glass veined in red.

ITS FORMS (pose key _form; every part swaps model per form - model_name):
  armored  PHASE 1. Full plate, helm closed, the wings folded into the cloak, the greatsword in hand. ~11 blocks tall at
           BOSS_SCALE: a player comes up to its knee.
  broken   PHASE 2. The plate cracked open and pieces gone (the helm's upper left broken away - red light inside - its left horn
           snapped, the left pauldron's spikes broken), the heart core exposed and blazing in a hole in the breastplate, and
           the SIX WINGS UNFURLED wide, their red eyes open.
  true     PHASE 3. The helm gone: inside, a void with a single vast red eye (small eyes opening round it) under a crown of
           floating plate shards and red motes. The body unravelling - plate fragments floating off a void core, the heart
           enormous; from the waist down it is smoke and tendrils, and it HOVERS (by design: its tendrils' tips stay some 2
           design units off the ground). The greatsword fused into its right arm as a growth of void-glass. Bigger (FORM_SCALE
           1.12) and wilder: the wings longer and more ragged, more eyes in them.
  bound    THE FOLLOWER. The armored model at follower size, the eye a dim ember, an iron collar at its throat with a broken
           leash and a chain round its waist - bound to you by its chains.
The wings follow the form (folded for armored/bound, open for broken/true); a pose can override with _wings ('fold' / 'open' -
phase 1's roar flings them open). Faces: the helm's slit (FACES: default burning, narrowed, wide, dim, closed - for armored,
broken and bound; the bound default is a dim ember) and the true form's great eye (EYE_FACES: default open, narrowed, wide,
blink; a helm face asked of the true form maps over: dim -> narrowed, closed -> blink).

SCALE (one rig, two sizes):
  RIG_SCALE = FOLLOWER_SCALE (0.85: about 2.3 blocks to the crown) - the rigpet follower's scale, used with POSES (the follower's
  poses, form 'bound').
  BOSS_SCALE (4.2: about 11 blocks to the crown) x FORM_SCALE[form] - the boss's, used with BOSS_POSES[form][name].
  scale_of(pose) gives the right one for any pose.

THE RIG (rigkit): body (the root: pelvis, belt, chains), chest (torso, breastplate and heart, collar), head (a model per form x
face), arms (upper arm with the pauldron, forearm with the gauntlet), legs (thigh with the tassets, shin with the sabaton), the
weapon (in the right fist), six wings (w1-w3 each side, rooted in the back plate) and fx (the eye's charge, beam and bolt, shown
only when a pose asks: _fx). Design units: feet at y=0, facing -z, its right is +x."""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import qs, el, seg, shrink, D, qrot

PREFIX = 'ds_'
FOLLOWER_SCALE = 0.85
RIG_SCALE = FOLLOWER_SCALE                     # (the follower's: POSES are the follower's)
BOSS_SCALE = 4.2
FORM_SCALE = {'armored': 1.0, 'broken': 1.0, 'true': 1.12}
FORMS = ('armored', 'broken', 'true', 'bound')
HOVER = 5.0                                    # (the true form's float: its root lifted this far, design units)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

PIVOT = {'body': (0, 18.0, 0), 'chest': (0, 21.0, 0), 'head': (0, 33.0, -0.5),
         'armr': (11.5, 30.0, 0), 'forer': (11.5, 21.0, 0), 'arml': (-11.5, 30.0, 0), 'forel': (-11.5, 21.0, 0),
         'legr': (4.6, 17.0, 0), 'shinr': (4.6, 9.5, 0), 'legl': (-4.6, 17.0, 0), 'shinl': (-4.6, 9.5, 0),
         'weapon': (11.5, 11.4, -0.2),
         'w1r': (3.4, 31.0, 5.2), 'w2r': (3.4, 28.0, 5.2), 'w3r': (3.4, 25.0, 5.2),
         'w1l': (-3.4, 31.0, 5.2), 'w2l': (-3.4, 28.0, 5.2), 'w3l': (-3.4, 25.0, 5.2),
         'fx': (0, 39.2, -5.6)}
PARENT = {'body': None, 'chest': 'body', 'head': 'chest', 'armr': 'chest', 'forer': 'armr', 'arml': 'chest', 'forel': 'arml',
          'legr': 'body', 'shinr': 'legr', 'legl': 'body', 'shinl': 'legl', 'weapon': 'forer',
          'w1r': 'chest', 'w2r': 'chest', 'w3r': 'chest', 'w1l': 'chest', 'w2l': 'chest', 'w3l': 'chest', 'fx': 'head'}
PARTS = tuple(PIVOT)
WINGS = ('w1r', 'w2r', 'w3r', 'w1l', 'w2l', 'w3l')
PART_K = {'weapon': 1.4, 'fx': 2.0, **{w: 1.9 for w in WINGS}}     # (built at full size, kept inside the model box)
FACES = ('narrowed', 'wide', 'dim', 'closed')
EYE_FACES = ('narrowed', 'wide', 'blink')
FX = ('charge', 'beam', 'bolt')

# the Dread armour's palette (dread_set_art), and the plate's working shades
VOID, VOID_L, RED, RED_L = (22, 16, 26), (48, 34, 54), (208, 24, 46), (255, 90, 100)
PLATE, PLATE_D, LIP, EDGE = (36, 26, 42), (15, 10, 18), (70, 52, 80), (54, 40, 62)
RED_D, EMBER, HOT = (118, 12, 28), (255, 170, 150), (255, 228, 210)


# ---------------------------------------------------------------------------------------------------- names
def _tag(p, form):
    if p in ('body', 'armr', 'arml', 'forer', 'forel', 'legr', 'legl', 'shinr', 'shinl'):
        return {'armored': 'a', 'bound': 'a', 'broken': 'b', 'true': 't'}[form]
    if p == 'chest':
        return {'armored': 'a', 'bound': 'n', 'broken': 'b', 'true': 't'}[form]
    if p == 'weapon':
        return 't' if form == 'true' else 'a'
    raise KeyError(p)


def wing_mode(pose):
    form = pose.get('_form', 'bound')
    w = pose.get('_wings') or ('open' if form in ('broken', 'true') else 'fold')
    return 'true' if (w == 'open' and form == 'true') else w


def face_of(pose):
    form, f = pose.get('_form', 'bound'), pose.get('_face')
    if form == 'true':
        f = {'dim': 'narrowed', 'closed': 'blink'}.get(f, f)
        return f if f in EYE_FACES else None
    f = {'blink': 'closed'}.get(f, f)
    return f if f in FACES else None


def HIDDEN(p, pose):
    if p == 'fx': return not pose.get('_fx')
    if p == 'weapon' and pose.get('_weapon') == 'none': return True
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    form = pose.get('_form', 'bound')
    if p == 'head':
        f = face_of(pose)
        return f'{PREFIX}head_{form}{"_x" + f if f else ""}{suffix}'
    if p in WINGS:
        return f'{PREFIX}{p}_{wing_mode(pose)}{suffix}'
    if p == 'fx':
        return f'{PREFIX}fx_{pose.get("_fx", "charge")}{suffix}'
    return f'{PREFIX}{p}_{_tag(p, form)}{suffix}'


def scale_of(pose):
    """the display scale to show a pose at: the follower's for its own poses, the boss's (by form) for BOSS_POSES"""
    form = pose.get('_form', 'bound')
    return RIG_SCALE if form == 'bound' else BOSS_SCALE * FORM_SCALE[form]


# ---------------------------------------------------------------------------------------------------- textures (2 px cells: half a design unit)
def _c(col, k=1.0, add=0):
    return tuple(max(0, min(255, int(v * k + add))) for v in col[:3]) + (255,)


def _cells(base, seed, var=0.10, size=64, cz=2, dark=0.08, light=0.05, add=5):
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im)
    for cy in range(0, size, cz):
        for cx in range(0, size, cz):
            k = 1 + rnd.uniform(-var, var); a = rnd.uniform(-add, add); q = rnd.random()
            if q < dark: k *= 0.72; a -= 3
            elif q < dark + light: k *= 1.25; a += 4
            d.rectangle((cx, cy, cx + cz - 1, cy + cz - 1), fill=_c(base, k, a))
    return im


def _sq(d, x, y, col, cz=2):
    d.rectangle((x, y, x + cz - 1, y + cz - 1), fill=_c(col))


def _crack(d, rnd, size, n=None, col=RED, hot=RED_L, x=None, y=None, branch=0.18):
    """a crack of red light, in cells: a dark lip to its left, branching as it runs down"""
    x = rnd.randrange(0, size, 2) if x is None else x; y = rnd.randrange(0, size, 2) if y is None else y
    for i in range(n or rnd.randint(5, 11)):
        _sq(d, (x - 2) % size, y, PLATE_D)
        _sq(d, x, y, hot if (i == 0 or rnd.random() < 0.18) else col)
        if rnd.random() < branch: _crack(d, rnd, size, rnd.randint(2, 4), col, hot, (x + rnd.choice((-2, 2))) % size, y, 0)
        x = (x + rnd.choice((-2, 0, 0, 2))) % size; y = (y + 2) % size


def _plate(seed, cracks=3, chips=0, voids=0, base=PLATE):
    """void-plate: banded plates (a lit lip along each band's top, a dark seam under it, staggered joints), rivets, cracks of red"""
    rnd = random.Random(seed); im = _cells(base, seed); d = ImageDraw.Draw(im)
    for by in range(0, 64, 16):
        d.rectangle((0, by, 63, by + 1), fill=_c(LIP)); d.rectangle((0, by + 14, 63, by + 15), fill=_c(PLATE_D))
        for _ in range(2):
            x0 = rnd.randrange(4, 60, 2)
            d.rectangle((x0, by + 2, x0 + 1, by + 13), fill=_c(PLATE_D)); d.rectangle((x0 + 2, by + 2, x0 + 3, by + 13), fill=_c(EDGE))
            if rnd.random() < 0.7: _sq(d, x0 + 4, by + 4, LIP); _sq(d, x0 + 4, by + 6, PLATE_D)        # (a rivet)
    for _ in range(voids):                                                                         # (holes into the void)
        x, y = rnd.randrange(0, 60, 2), rnd.randrange(0, 60, 2)
        d.rectangle((x, y, x + 5, y + 3), fill=_c((6, 3, 8))); _sq(d, x + 2, y + 2, RED_D)
    for _ in range(chips):                                                                         # (chips knocked out, red inside)
        x, y = rnd.randrange(0, 60, 2), rnd.randrange(0, 60, 2)
        d.rectangle((x, y, x + 3, y + 3), fill=_c(PLATE_D)); _sq(d, x + 1 - 1, y + 2, RED)
    for _ in range(cracks): _crack(d, rnd, 64)
    return im


def _edge(seed):
    """trim: a lighter violet, its top lit, its foot dark"""
    im = _cells(EDGE, seed, 0.08); d = ImageDraw.Draw(im)
    for by in range(0, 64, 8):
        d.rectangle((0, by, 63, by + 1), fill=_c(LIP, 1.15)); d.rectangle((0, by + 6, 63, by + 7), fill=_c(PLATE_D, 1.3))
    return im


def _dark(seed):
    """the black under-armour: ring mail"""
    im = _cells(PLATE_D, seed, 0.1, add=3); d = ImageDraw.Draw(im)
    for y in range(0, 64, 4):
        for x in range((y // 4) % 2 * 2, 64, 4):
            _sq(d, x, y, (34, 25, 40))
    return im


def _glow(base, hi, seed, p=0.22):
    rnd = random.Random(seed); im = _cells(base, seed, 0.06, dark=0.03, light=0.0, add=4); d = ImageDraw.Draw(im)
    for _ in range(int(p * 1024)):
        _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), hi)
    return im


def _heart():
    """the Dread heart's crystal: red facets, bright edges, a hot sparkle"""
    rnd = random.Random(77); im = _cells(RED, 77, 0.08, dark=0.0, light=0.0); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 12):
        d.line((k, 0, k + 64, 64), fill=_c(RED_L), width=2); d.line((k + 6, 64, k + 70, 0), fill=_c(RED_D), width=2)
    for _ in range(30): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), EMBER)
    for _ in range(8): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), HOT)
    return im


def _horn(seed, red=False):
    """black horn, ridged; red: a tip glowing from within"""
    rnd = random.Random(seed)
    if red:
        im = _cells(RED, seed, 0.1, dark=0.15, light=0.1); d = ImageDraw.Draw(im)
        for _ in range(40): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), RED_L)
        return im
    im = _cells((20, 13, 23), seed, 0.1, add=3); d = ImageDraw.Draw(im)
    for y in range(0, 64, 6):
        d.rectangle((0, y, 63, y + 1), fill=_c((46, 33, 52)))
    return im


def _membrane(seed, veins=16):
    """black membrane in folds, veined in red"""
    rnd = random.Random(seed); im = _cells((19, 11, 21), seed, 0.12, add=3); d = ImageDraw.Draw(im)
    for x in range(0, 64, 8):
        d.rectangle((x, 0, x + 1, 63), fill=_c((34, 22, 38)))
    for _ in range(veins): _crack(d, rnd, 64, rnd.randint(4, 10), RED_D, RED, branch=0.3)
    return im


def _wbone(seed):
    im = _cells((44, 31, 48), seed, 0.1); d = ImageDraw.Draw(im)
    for y in range(0, 64, 6):
        d.rectangle((0, y, 63, y + 1), fill=_c((66, 48, 72))); d.rectangle((0, y + 2, 63, y + 2), fill=_c((26, 18, 30)))
    return im


def _eye(kind='open', size=16, iris=RED):
    """a pixel eye (whole uv): a pale almond, a red iris with a slit pupil, a glint - or shut: a red seam"""
    im = Image.new('RGBA', (size, size), _c((19, 11, 21))); d = ImageDraw.Draw(im); s = size / 16
    if kind == 'shut':
        d.rectangle((2 * s, 7 * s, 14 * s - 1, 9 * s - 1), fill=_c(RED_D)); d.rectangle((4 * s, 7 * s, 12 * s - 1, 8 * s - 1), fill=_c(RED))
    else:
        d.polygon([(1 * s, 8 * s), (5 * s, 3 * s), (11 * s, 3 * s), (15 * s, 8 * s), (11 * s, 13 * s), (5 * s, 13 * s)], fill=_c((236, 226, 216)))
        d.ellipse((4 * s, 3 * s, 12 * s - 1, 13 * s - 1), fill=_c(iris))
        d.rectangle((7 * s, 4 * s, 9 * s - 1, 12 * s - 1), fill=_c((12, 2, 4)))
        d.rectangle((5 * s, 5 * s, 6 * s - 1, 6 * s - 1), fill=_c(EMBER))
    return im.resize((64, 64), Image.NEAREST)


def _red_eye():
    """the small eyes opening on the helm's sides and the void: red, a black slit"""
    im = Image.new('RGBA', (8, 8), _c(RED)); d = ImageDraw.Draw(im)
    d.rectangle((3, 1, 4, 6), fill=_c((14, 2, 4))); d.point((1, 1), fill=_c(RED_L)); d.point((2, 1), fill=_c(RED_L))
    return im.resize((64, 64), Image.NEAREST)


def _big_eye(kind=None):
    """the TRUE form's vast eye (whole uv): a dark crimson eyeball veined in red, a burning iris ringed in fire, a black slit
    pupil. narrowed: void lids over its top and bottom; wide: the pupil a needle in a smaller, hotter iris; blink: the lids shut,
    a seam of light between them"""
    N = 32; im = Image.new('RGBA', (N, N), _c((70, 6, 16))); d = ImageDraw.Draw(im); rnd = random.Random(31)
    for _ in range(9):                                                                  # (veins)
        x, y = rnd.choice((0, N - 1)), rnd.randrange(N)
        for _s in range(rnd.randint(4, 9)):
            d.point((x, y), fill=_c((150, 14, 30))); x += 1 if x < N // 2 else -1; y += rnd.choice((-1, 0, 1))
    r = 9 if kind != 'wide' else 7
    c = N // 2
    d.ellipse((c - r - 1, c - r - 1, c + r, c + r), fill=_c((40, 2, 6)))
    d.ellipse((c - r, c - r, c + r - 1, c + r - 1), fill=_c((255, 70, 30)))
    d.ellipse((c - r + 2, c - r + 2, c + r - 3, c + r - 3), fill=_c((255, 120, 60)))
    d.ellipse((c - r + 4, c - r + 4, c + r - 5, c + r - 5), fill=_c((255, 190, 120)))
    pw = 1 if kind == 'wide' else 2
    d.rectangle((c - pw, c - r + 1, c + pw - 1, c + r - 2), fill=_c((8, 0, 2)))
    d.rectangle((c - pw - 1, c - 3, c + pw, c + 2), fill=_c((8, 0, 2)))
    d.rectangle((c - 6, c - 7, c - 5, c - 6), fill=_c(HOT))
    lid = _c((8, 4, 10))
    if kind == 'narrowed':
        d.rectangle((0, 0, N - 1, 9), fill=lid); d.rectangle((0, N - 8, N - 1, N - 1), fill=lid)
        d.line((0, 10, N - 1, 10), fill=_c(RED_D)); d.line((0, N - 9, N - 1, N - 9), fill=_c(RED_D))
    if kind == 'blink':
        d.rectangle((0, 0, N - 1, N - 1), fill=lid); d.rectangle((0, c - 1, N - 1, c), fill=_c(RED_D)); d.rectangle((4, c - 1, N - 5, c - 1), fill=_c(RED))
    for x in range(N):                                                                  # (a dark rim)
        d.point((x, 0), fill=lid); d.point((x, N - 1), fill=lid); d.point((0, x), fill=lid); d.point((N - 1, x), fill=lid)
    return im.resize((64, 64), Image.NEAREST)


def _visor():
    """the helm's lower face (its top-left 32 x 16 px, at 4 px a unit): breathing slots either side of the nose guard, a lip"""
    im = _plate(901, cracks=0); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 31, 15), fill=_c(PLATE)); d.rectangle((0, 0, 31, 1), fill=_c(LIP))
    for y in (4, 8, 12):
        for x0, x1 in ((3, 12), (19, 28)):
            d.rectangle((x0, y, x1, y + 1), fill=_c((6, 2, 8))); d.rectangle((x0, y + 2, x1, y + 2), fill=_c(EDGE))
    return im


def _chain():
    """a chain link in its top-left 4 x 6 px (links are small and unshifted): a pale iron ring round a dark hole"""
    im = Image.new('RGBA', (64, 64), _c((70, 64, 78))); d = ImageDraw.Draw(im)
    for y in range(0, 64, 6):
        for x in range(0, 64, 4):
            d.rectangle((x, y, x + 3, y + 5), fill=_c((86, 78, 96))); d.rectangle((x + 1, y + 1, x + 2, y + 4), fill=_c((14, 10, 16)))
            d.point((x, y), fill=_c((120, 110, 130)))
    return im


def _iron(seed):
    rnd = random.Random(seed); im = _cells((66, 60, 74), seed, 0.08); d = ImageDraw.Draw(im)
    for y in range(0, 64, 8):
        d.rectangle((0, y, 63, y), fill=_c((96, 88, 104)))
        for x in range(2, 64, 10): _sq(d, x, y + 3, (110, 100, 118))
    for _ in range(12): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (90, 30, 34))        # (old blood-rust)
    return im


def _glass(seed):
    """void-glass: deep violet, pale streaks and fractures, a red vein here and there"""
    rnd = random.Random(seed); im = _cells((38, 18, 54), seed, 0.1); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 10):
        d.line((k, 0, k + 40, 64), fill=_c((84, 52, 112)), width=2)
    for _ in range(18): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (140, 104, 176))
    for _ in range(3): _crack(d, rnd, 64, 6, RED_D, RED, branch=0)
    return im


def _grip():
    im = _cells((40, 24, 30), 44); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 6):
        d.line((k, 0, k + 64, 64), fill=_c(RED_D), width=2)
    return im


def _smoke(seed):
    rnd = random.Random(seed); im = _cells((26, 17, 30), seed, 0.18, add=4); d = ImageDraw.Draw(im)
    for _ in range(14):
        x, y = rnd.randrange(0, 60, 2), rnd.randrange(0, 60, 2); d.rectangle((x, y, x + 5, y + 3), fill=_c((46, 32, 54)))
    for _ in range(10): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (10, 6, 12))
    for _ in range(7): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), RED)
    return im


def _void(seed):
    rnd = random.Random(seed); im = _cells((9, 5, 11), seed, 0.2, add=2); d = ImageDraw.Draw(im)
    for _ in range(26): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), (44, 26, 58))
    for _ in range(8): _sq(d, rnd.randrange(0, 64, 2), rnd.randrange(0, 64, 2), RED_D)
    return im


def textures():
    T = {'ds_plate': _plate(1101, 1), 'ds_plate_b': _plate(1102, 6, chips=3), 'ds_plate_t': _plate(1103, 9, chips=4, voids=5),
         'ds_edge': _edge(1104), 'ds_dark': _dark(1105), 'ds_red': _glow(RED, RED_L, 1106), 'ds_red_l': _glow(RED_L, EMBER, 1107, 0.3),
         'ds_red_d': _glow(RED_D, (150, 20, 36), 1108), 'ds_heart': _heart(), 'ds_horn': _horn(1109), 'ds_horn_r': _horn(1110, True),
         'ds_membrane': _membrane(1111), 'ds_membrane_t': _membrane(1112, 20), 'ds_wbone': _wbone(1113),
         'ds_eye': _eye('open'), 'ds_eye_shut': _eye('shut'), 'ds_eye_r': _red_eye(), 'ds_visor': _visor(), 'ds_chain': _chain(),
         'ds_iron': _iron(1114), 'ds_glass': _glass(1115), 'ds_grip': _grip(), 'ds_smoke': _smoke(1116), 'ds_void': _void(1117),
         'ds_beye': _big_eye()}
    for f in EYE_FACES: T[f'ds_beye_{f}'] = _big_eye(f)
    return T


# ---------------------------------------------------------------------------------------------------- building helpers
NOSHIFT = {'ds_chain', 'ds_eye', 'ds_eye_shut', 'ds_eye_r', 'ds_visor', 'ds_beye'} | {f'ds_beye_{f}' for f in EYE_FACES}
_rs = random.Random(5)


_PV = [None]


def E(fr, to, tex, pv=None, light=0, **kw):
    """an element (rigkit.el), its texture window shifted at random so neighbouring boxes don't repeat the same patch (pv: the
    part's joint - by default the part being built)"""
    pv = pv or _PV[0]
    if tex not in NOSHIFT and 'shift' not in kw and 'uv' not in kw: kw['shift'] = (_rs.random(), _rs.random())
    return el(fr, to, tex, pv, light=light, **kw)


def BX(sx, x0, x1, y0, y1, z0, z1, tex, pv, **kw):
    """a box on side sx (+1 its right, -1 its left): x given for the right side, mirrored"""
    a, b = sorted((sx * x0, sx * x1))
    return E((a, y0, z0), (b, y1, z1), tex, pv, **kw)


def CH(pts, ws, tex, pv, light=0, up=FRONT, texs=None):
    """a tapering run of boxes along a polyline (square in section): a horn, a spike, a claw, a bone"""
    n = len(pts) - 1
    if isinstance(ws, tuple): ws = [ws[0] + (ws[1] - ws[0]) * i / max(1, n - 1) for i in range(n)]
    out = []
    for i in range(n):
        t = texs[i] if texs else tex
        out.append(seg(pts[i], pts[i + 1], ws[i], ws[i], t, pv, up, 0.2, light=light if (texs is None or t in ('ds_horn_r', 'ds_red')) else 0,
                       shift=(_rs.random(), _rs.random())))
    return out


def SPIKE(base, tip, w, pv, mid=0.55, bend=(0, 0, 0), red=True):
    """a spike: thick at its root, thin, a red-hot tip"""
    m = tuple(base[i] + (tip[i] - base[i]) * mid + bend[i] for i in range(3))
    return CH([base, m, tip], [w, w * 0.55], 'ds_horn', pv, light=12, texs=['ds_horn', 'ds_horn_r' if red else 'ds_horn'])


def LINKS(pts, pv, w=0.9, L=1.5, t=0.34):
    """a chain along a polyline: links of iron, each turned a quarter from the last"""
    out, k = [], 0
    for A, B in zip(pts, pts[1:]):
        d = [B[i] - A[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in d)); u = [v / n for v in d]
        p1 = rigkit._cross(u, (0.0, 0.0, 1.0)) if abs(u[2]) < 0.9 else rigkit._cross(u, (0.0, 1.0, 0.0))
        p1 = rigkit._unit(p1); p2 = rigkit._cross(u, p1)
        steps = max(1, int(n / (L * 0.72)))
        for i in range(steps):
            a = [A[j] + u[j] * (i * n / steps) for j in range(3)]
            b = [a[j] + u[j] * L for j in range(3)]
            if i == steps - 1: b = [B[j] + u[j] * 0.2 for j in range(3)]
            out.append(seg(tuple(a), tuple(b), w, t, 'ds_chain', pv, tuple(p1 if k % 2 else p2), 0.0)); k += 1
    return out


def GEM(c, s, tex, pv, light=15, rot=(35.26, 45.0, 0.0)):
    """a cube stood on its point (a crystal)"""
    return E((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, pv, light=light, rot=(rot, c))


# ---------------------------------------------------------------------------------------------------- the parts
PL = {'armored': 'ds_plate', 'bound': 'ds_plate', 'broken': 'ds_plate_b', 'true': 'ds_plate_t'}


def _head(form, face=None):
    """(built at the old size, then grown 1.12 about the joint and lifted a unit: it stands up out of the pauldrons)"""
    return rigkit.transform(_head0(form, face), lambda v: [8 + (v[0] - 8) * 1.12, 8 + (v[1] - 8) * 1.12 + 1.0, 8 + (v[2] - 8) * 1.12])


def _head0(form, face=None):
    pv = PIVOT['head']; P = PL[form]; H = []
    if form == 'true':
        return _true_head(face)
    broken = form == 'broken'
    # ---- the hood (broken: its upper left broken away, red light inside)
    if not broken:
        H.append(E((-4.2, 33.0, -4.3), (4.2, 41.0, 3.9), P))
    else:
        H += [E((-4.2, 33.0, -4.3), (4.2, 37.6, 3.9), P), E((-0.4, 37.6, -4.3), (4.2, 41.0, 3.9), P),
              E((-4.2, 37.6, 0.8), (-0.4, 40.2, 3.9), P), E((-4.2, 37.6, -4.3), (-2.8, 38.8, 0.8), P),
              E((-1.8, 37.6, -4.3), (-0.4, 39.8, -1.0), P),
              E((-3.8, 37.6, -3.9), (-0.4, 39.9, 0.8), 'ds_red_d', light=13), GEM((-2.0, 39.0, -1.6), 1.4, 'ds_red', pv)]
    H.append(E((-0.9, 41.0, -4.0), (0.9, 41.8, 3.2) if not broken else (0.9, 41.8, 1.0), 'ds_edge'))          # (the crest)
    # ---- the face: the visor with its breathing slots, the nose guard, the dark eye band, the brow over it
    H += [E((-3.9, 33.2, -4.9), (3.9, 37.0, -4.3), 'ds_visor', pv), E((-0.5, 33.4, -5.3), (0.5, 37.0, -4.9), 'ds_edge'),
          E((-3.9, 37.0, -4.6), (3.9, 38.3, -4.3), 'ds_dark')]
    f = face
    if form == 'bound':                                       # (bound: the slit an ember - 'wide' burns as the armored default does)
        f = {None: 'ember', 'wide': None}.get(face, face)
    if f in ('narrowed', 'wide'):                             # (the brow in a hard V)
        a = 9 if f == 'narrowed' else 15; y0 = 37.9 if f == 'narrowed' else 38.4
        for sx in (1, -1):
            H.append(BX(sx, 0, 4.5, y0, y0 + 1.6, -5.3, -4.3, 'ds_edge', pv, rot=('z', a * sx, (0, y0, -4.8))))
    else:
        H.append(E((-4.4, 38.3, -5.3), (4.4, 39.9, -4.3), 'ds_edge'))
    slit = {None: [((-3.5, 37.2), (3.5, 38.1), 'ds_red', 15), ((-2.2, 37.4), (2.2, 37.9), 'ds_red_l', 15)],
            'narrowed': [((-3.0, 37.5), (3.0, 37.8), 'ds_red', 15), ((-1.0, 37.55), (1.0, 37.75), 'ds_red_l', 15)],
            'wide': [((-3.6, 37.05), (3.6, 38.25), 'ds_red', 15), ((-2.4, 37.25), (2.4, 38.05), 'ds_red_l', 15)],
            'dim': [((-2.6, 37.45), (2.6, 37.85), 'ds_red_d', 6)],
            'ember': [((-2.8, 37.4), (2.8, 37.9), 'ds_red_d', 10), ((-0.8, 37.5), (0.8, 37.8), 'ds_red', 10)],
            'closed': []}[f]
    if broken and f not in ('dim', 'closed'):
        slit = [((-3.6, slit[0][0][1] - 0.15), (3.6, slit[0][1][1] + 0.15), 'ds_red', 15)] + slit[1:]
    for i, ((x0, y0), (x1, y1), t, lt) in enumerate(slit):
        z = -4.75 - 0.05 * i
        H.append(E((x0, y0, z), (x1, y1, -4.6), t, pv, light=lt))
    if f == 'wide':                                           # (it flares past the visor's edges)
        for sx in (1, -1): H.append(BX(sx, 3.6, 4.8, 37.45, 37.85, -4.75, -4.45, 'ds_red_l', pv, light=15))
    # ---- cheek guards, the eyes opening on its sides
    for sx in (1, -1):
        H.append(BX(sx, 3.7, 4.7, 33.0, 36.8, -4.8, -1.4, P, pv))
        if f != 'closed':
            for (y, z) in ((38.8, -2.2), (35.8, 0.6)):
                H.append(BX(sx, 4.2, 4.4, y - 0.5, y + 0.5, z - 0.6, z + 0.6, 'ds_eye_r' if f != 'dim' and form != 'bound' else 'ds_red_d', pv, light=12))
    # ---- the crown of black spikes (red-hot at their tips), tallest at the front
    crown = [(-3.0, -3.6, 3.2), (-1.5, -3.6, 4.8), (0, -3.7, 7.4), (1.5, -3.6, 4.8), (3.0, -3.6, 3.2),
             (-3.8, 0.2, 3.6), (3.8, 0.2, 3.6), (0, 3.2, 3.0)]
    for x, z, h in crown:
        if broken and (x < -0.5 and z < 1.5):                 # (the broken side's spikes snapped to stubs)
            if x > -3.5 or z < 0: H += CH([(x, 40.6, z), (x * 1.05, 41.8, z - 0.2)], [1.2], 'ds_horn', pv)
            continue
        H += SPIKE((x, 40.6, z), (x * 1.3, 40.6 + h, z - 0.3 if z < 0 else z + 0.4), 1.3, pv, bend=(x * 0.05, 0, -0.3), red=(z < 0 and abs(x) < 2))
    # ---- the great horns: out of the temples, back and up (broken: its left one snapped)
    for sx in (1, -1):
        pts = [(sx * 4.0, 39.0, -0.6), (sx * 6.6, 40.4, 0.2), (sx * 8.6, 43.0, 1.6), (sx * 9.4, 46.4, 3.0), (sx * 8.8, 49.2, 4.2)]
        if broken and sx < 0:
            H += CH(pts[:3], [2.4, 2.0], 'ds_horn', pv) + [GEM(pts[2], 1.2, 'ds_red', pv)]
        else:
            H += CH(pts, [2.4, 2.0, 1.5, 1.0], 'ds_horn', pv, light=12, texs=['ds_horn', 'ds_horn', 'ds_horn', 'ds_horn_r'])
    return H


def _true_head(face=None):
    """the helm gone: a void, one vast eye framed by the shards of a socket, small eyes opening round it, a crown of floating
    shards and a ring of red motes above"""
    pv = PIVOT['head']; H = []
    H += [E((-3.6, 33.6, -3.6), (3.6, 40.8, 3.6), 'ds_void'), E((-3.1, 34.0, -4.0), (3.1, 40.3, 3.9), 'ds_void'),
          E((-4.0, 34.4, -3.0), (4.0, 40.0, 3.0), 'ds_void')]
    big = face == 'wide'
    ex, ey0, ey1 = (3.0, 34.3, 40.0) if big else (2.6, 34.8, 39.4)
    H.append(E((-ex, ey0, -4.5), (ex, ey1, -3.9), f'ds_beye{"_" + face if face else ""}', pv, light=15,
               uv={'north': [0, 0, 16, 16]}, faces=('north', 'east', 'west', 'up', 'down')))
    for (x0, x1, y0, y1) in ((-3.5, 3.5, ey1, ey1 + 0.9), (-3.1, 3.1, ey0 - 0.8, ey0), (-ex - 0.8, -ex, ey0, ey1), (ex, ex + 0.8, ey0, ey1)):
        H.append(E((x0, y0, -4.7), (x1, y1, -3.8), 'ds_plate_t'))                                     # (the socket's shards)
    for sx in (1, -1):                                                                                # (small eyes round it)
        for (y, z) in ((38.0, -1.8), (35.6, 0.8), (39.4, 1.6)):
            H.append(BX(sx, 4.0, 4.2, y - 0.55, y + 0.55, z - 0.55, z + 0.55, 'ds_eye_r', pv, light=15))
    for (x, y) in ((-3.0, 41.0), (2.6, 41.0)):
        H.append(E((x - 0.5, y - 0.5, -3.3), (x + 0.5, y + 0.5, -2.7), 'ds_eye_r', pv, light=15))
    H += [E((-1.2, 40.8, -1.0), (0.4, 42.4, 0.6), 'ds_smoke'), E((0.2, 40.8, 0.4), (1.6, 41.8, 1.8), 'ds_smoke')]
    # the crown: plate shards floating in a ring, leaning out, each with a red-hot edge - the front one tallest
    for i in range(9):
        a = 360 * i / 9; r = 5.4; cx, cz = r * math.sin(math.radians(a)), -r * math.cos(math.radians(a))
        h = 7.6 if i == 0 else (4.4 + 1.4 * (i % 2)); cy = 43.4 + h / 2 - 1.5 + (0.6 if i % 2 else 0)
        rot = ((-18.0, -a, 0.0), (cx, cy, cz))
        H.append(E((cx - 1.0, cy - h / 2, cz - 0.35), (cx + 1.0, cy + h / 2, cz + 0.35), 'ds_horn', pv, rot=rot))
        H.append(E((cx - 0.55, cy + h / 2, cz - 0.25), (cx + 0.55, cy + h / 2 + 1.6, cz + 0.25), 'ds_horn_r', pv, rot=rot, light=15))
    for i in range(14):                                                                               # (the motes)
        a = 2 * math.pi * (i + 0.5) / 14; x, z = 4.4 * math.sin(a), 4.4 * math.cos(a)
        H.append(E((x - 0.3, 42.0 + 0.4 * (i % 3), z - 0.3), (x + 0.3, 42.6 + 0.4 * (i % 3), z + 0.3), 'ds_red_l', pv, light=15))
    return H


def _bandolier(pv, z_off=0.45):
    """the chain across its breast, left shoulder to right hip, over the keel of the breastplate"""
    zf = lambda x: -5.6 + abs(x) * 0.2126 - z_off
    return LINKS([(-7.4, 31.2, zf(-7.4)), (0.0, 27.1, -6.1 - z_off), (6.0, 23.6, zf(6.0) + 0.2), (7.0, 22.9, -4.9)], pv)


def _chest(form):
    pv = PIVOT['chest']; P = PL[form]; C = []
    true = form == 'true'
    if not true:
        C += [E((-6.0, 20.0, -3.8), (6.0, 25.0, 3.8), 'ds_dark'),
              E((-6.4, 21.0, -4.3), (6.4, 22.6, -3.6), P), E((-6.8, 22.6, -4.6), (6.8, 24.6, -3.8), P),
              E((-8.6, 24.4, -3.8), (8.6, 31.6, 4.4), P), E((-8.0, 24.6, 4.4), (8.0, 31.4, 5.0), P),
              E((-6.6, 24.4, -4.75), (6.6, 24.75, -4.4), 'ds_red', pv, light=15)]
    else:                                                     # (unravelling: a void core, ribs of plate, smoke at the waist)
        C += [E((-5.0, 20.0, -3.2), (5.0, 25.0, 3.2), 'ds_smoke'), E((-4.2, 19.0, -2.6), (4.2, 21.0, 2.6), 'ds_smoke'),
              E((-8.0, 24.4, -3.6), (8.0, 31.6, 4.2), 'ds_void'), E((-7.4, 24.8, 4.2), (7.4, 31.0, 4.9), P)]
        for i, y in enumerate((25.2, 27.0, 28.8)):
            for sx in (1, -1):
                C.append(BX(sx, 3.4, 8.3, y, y + 1.1, -4.4, -3.5, P, pv, rot=('y', -sx * (8 + 4 * i), (sx * 3.4, y, -4.0))))
    # ---- the breastplate: two halves meeting in a keel, a ridge down it, the heart behind
    for sx in (1, -1):
        rot = ('y', -sx * 12, (0, 28, -5.6))
        if form in ('armored', 'bound') or (form == 'broken' and sx < 0):
            C.append(BX(sx, 0, 7.8, 24.6, 31.2, -5.6, -4.4, P, pv, rot=rot))
        elif form == 'broken':                                # (its right half smashed in: the outer part left, jagged)
            C += [BX(sx, 3.8, 7.8, 24.6, 31.2, -5.6, -4.4, P, pv, rot=rot), BX(sx, 2.4, 3.9, 24.6, 26.6, -5.6, -4.4, P, pv, rot=rot),
                  BX(sx, 2.6, 3.9, 29.6, 31.2, -5.6, -4.4, P, pv, rot=rot)]
        else:                                                 # (true: the halves torn away, floating off the core)
            C.append(BX(sx, 3.2, 8.2, 28.2, 31.6, -6.4, -5.4, P, pv, rot=('y', -sx * 20, (sx * 3.2, 30, -5.9))))
    if form in ('armored', 'bound'):
        C += [E((-0.7, 24.6, -6.1), (0.7, 31.4, -5.3), 'ds_edge'),
              GEM((0, 29.6, -6.2), 1.7, 'ds_heart', pv, light=15 if form == 'armored' else 9, rot=(0.0, 0.0, 45.0))]
        C += [E((-0.25, 25.2, -6.3), (0.25, 28.2, -6.05), 'ds_red', pv, light=15)]          # (its light leaking down the seam)
    elif form == 'broken':                                    # (the hole: red light in it, the heart blazing, cracks running off)
        C += [E((-0.7, 24.6, -6.1), (0.7, 26.0, -5.3), 'ds_edge'), E((-0.7, 30.4, -6.1), (0.7, 31.4, -5.3), 'ds_edge'),
              E((-0.6, 25.0, -5.0), (4.0, 30.8, -4.4), 'ds_red_d', pv, light=14),
              GEM((1.6, 28.0, -5.2), 2.8, 'ds_heart', pv), GEM((2.9, 29.7, -5.5), 1.1, 'ds_red_l', pv), GEM((0.5, 26.4, -5.6), 1.0, 'ds_red_l', pv)]
        zf = lambda x: -5.6 + abs(x) * 0.2126 - 0.06
        for (x0, y0, x1, y1) in ((-0.6, 28.4, -3.4, 30.6), (-0.6, 27.0, -4.6, 25.8), (-3.4, 30.6, -5.6, 30.9), (4.2, 26.0, 6.4, 24.9)):
            C.append(seg((x0, y0, zf(x0)), (x1, y1, zf(x1)), 0.35, 0.2, 'ds_red', pv, ext=0.1, light=15))
    else:                                                     # (true: the heart enormous, its light in rays)
        C += [GEM((0, 28.0, -4.6), 4.0, 'ds_heart', pv), GEM((0, 28.0, -4.6), 2.2, 'ds_red_l', pv, rot=(0.0, 45.0, 45.0))]
        for a in range(0, 360, 45):
            r0, r1 = 2.6, 4.4 + (1.4 if a % 90 == 0 else 0)
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            C.append(seg((r0 * ca, 28.0 + r0 * sa, -5.9), (r1 * ca, 28.0 + r1 * sa, -6.1), 0.4, 0.3, 'ds_red_l', pv, ext=0.0, light=15))
        for x, ln in ((-4.0, 6.0), (-1.4, 4.4), (2.0, 7.0), (4.4, 5.0)):                 # (smoke tendrils off the waist)
            C += CH([(x, 20.4, -2.6), (x * 1.15, 20.4 - ln * 0.5, -3.2), (x * 1.3, 20.4 - ln, -3.0)], (1.4, 0.7), 'ds_smoke', pv)
    # ---- the collar: the gorget, its front plate, a tall flared back collar with spikes
    C += [E((-4.8, 30.6, -3.6), (4.8, 32.6, 3.6), 'ds_dark'), E((-5.2, 30.8, -4.6), (5.2, 32.2, -3.6), 'ds_edge')]
    if not true:
        C.append(E((-5.4, 31.0, 4.2), (5.4, 36.0, 5.2), 'ds_edge', pv, rot=('x', 14, (0, 31, 4.7))))
        for sx in (1, -1): C.append(BX(sx, 4.6, 5.6, 30.8, 35.0, -2.8, 4.6, P, pv, rot=('z', -sx * 10, (sx * 4.6, 31, 0))))
        for x, h in ((-3.6, 3.4), (0, 4.6), (3.6, 3.4)):
            C += SPIKE((x, 35.0, 5.6), (x * 1.2, 35.0 + h, 7.2), 1.0, pv, red=False)
    else:
        for x0, x1, h in ((-5.4, -2.2, 4.0), (-1.2, 1.6, 5.2), (2.6, 5.4, 3.0)):
            C.append(E((x0, 31.4, 4.4), (x1, 31.4 + h, 5.2), P, pv, rot=('x', 22, (0, 31.4, 4.8))))
    # ---- the chains: the bandolier (true: snapped, trailing); bound: an iron collar with a broken leash, a chain round the waist
    if form in ('armored', 'broken', 'bound'):
        C += _bandolier(pv)
        C.append(E((-1.0, 26.4, -7.1), (1.0, 28.0, -6.3), 'ds_iron'))                    # (its broken lock)
    else:
        C += LINKS([(-7.4, 31.2, -4.5), (-4.0, 29.4, -5.0), (-2.4, 26.0, -5.4)], pv)
    if form == 'bound':
        C += [E((-5.4, 31.6, -5.1), (5.4, 33.0, 4.6), 'ds_iron'), E((-2.6, 31.2, -5.5), (-1.0, 32.8, -5.0), 'ds_iron')]
        C += LINKS([(-1.8, 31.2, -5.6), (-2.0, 28.8, -6.9), (-1.6, 26.9, -7.2)], pv)
        C += LINKS([(-6.4, 22.0, -5.0), (0, 21.8, -5.1), (6.4, 22.0, -5.0)], pv) + LINKS([(6.6, 22.0, -4.6), (6.6, 22.0, 4.4)], pv) + \
            LINKS([(-6.6, 22.0, 4.4), (-6.6, 22.0, -4.6)], pv)
    return C


def _body(form):
    pv = PIVOT['body']; P = PL[form]; B = []
    if form != 'true':
        B += [E((-6.6, 15.0, -3.8), (6.6, 20.4, 3.8), 'ds_dark'), E((-7.0, 19.6, -4.3), (7.0, 21.2, 4.3), 'ds_edge'),
              E((-6.95, 21.2, -4.25), (6.95, 21.45, 4.25), 'ds_red', pv, light=15),
              E((-2.2, 18.8, -4.9), (2.2, 22.0, -4.3), 'ds_iron'),
              E((-1.0, 19.6, -5.0), (1.0, 21.2, -4.9), 'ds_eye', pv, light=15, uv={'north': [0, 0, 16, 16]}, faces=('north',)),
              E((-1.4, 13.2, -4.6), (1.4, 18.8, -3.6), P), E((-6.8, 14.0, 3.6), (6.8, 19.6, 4.6), P)]
        for sx in (1, -1):                                    # (chains from the belt - the broken form's left one snapped)
            bot = 12.0 if (form == 'broken' and sx < 0) else 8.5
            B += LINKS([(sx * 8.0, 20.4, 0.4), (sx * 8.4, bot, 0.6)], pv)
            B.append(BX(sx, 7.0, 8.8, 19.4, 21.4, -0.6, 1.4, 'ds_iron', pv))
    else:                                                     # (the hips gone to smoke round the shards of the belt; chains trailing)
        B += [E((-5.6, 14.0, -3.4), (5.6, 20.4, 3.4), 'ds_smoke'), E((-4.6, 12.0, -2.8), (4.6, 14.0, 2.8), 'ds_smoke'),
              E((-6.8, 19.8, -4.2), (-1.4, 21.0, 4.0), 'ds_edge', pv, rot=('z', -6, (-4, 20.4, 0))),
              E((1.8, 19.4, -4.2), (7.0, 20.6, 4.0), 'ds_edge', pv, rot=('z', 9, (4, 20.0, 0))),
              E((-1.0, 19.6, -5.0), (1.0, 21.2, -4.2), 'ds_eye', pv, light=15, uv={'north': [0, 0, 16, 16]})]
        for sx in (1, -1):
            B += LINKS([(sx * 7.6, 20.0, 0.4), (sx * 8.4, 13.0, 1.0), (sx * 7.8, 7.0, 2.4)], pv)
        # the robe of smoke it hovers on: ragged strips round the hips, splaying a little and fraying out at the foot
        rnd = random.Random(404)
        for k in range(14):
            a = 2 * math.pi * (k + 0.5) / 14; ca, sa = math.sin(a), -math.cos(a)
            r0, r1 = 5.2, 6.6 + rnd.uniform(0, 1.2); ln = rnd.uniform(9.0, 13.5)
            zk = 0.75 if sa < 0 else 0.55                     # (flatter behind: clear of the wings)
            top = (r0 * ca, 16.0, r0 * sa * zk); mid = (r1 * ca, 16.0 - ln * 0.55, r1 * sa * zk); bot = ((r1 + 0.6) * ca, 16.0 - ln, (r1 + 0.6) * sa * zk)
            B += CH([top, mid, bot], [3.0, 1.8], 'ds_smoke', pv, up=UP)
            if k % 3 == 0: B.append(E((bot[0] - 0.3, bot[1] - 0.4, bot[2] - 0.3), (bot[0] + 0.3, bot[1] + 0.2, bot[2] + 0.3), 'ds_red', pv, light=15))
    return B


def _leg(sx, form):
    pv = PIVOT['legr' if sx > 0 else 'legl']; P = PL[form]
    if form == 'true':                                        # (smoke, a shard of the cuisse floating before it)
        L = [BX(sx, 2.2, 7.0, 13.0, 18.4, -2.6, 2.6, 'ds_smoke', pv), BX(sx, 2.8, 6.4, 9.0, 13.2, -2.0, 2.0, 'ds_smoke', pv),
             BX(sx, 3.2, 6.6, 12.4, 15.6, -3.8, -3.0, P, pv, rot=('x', -10, (sx * 4.8, 14, -3.4))),
             BX(sx, 4.4, 5.0, 11.6, 12.2, -3.7, -3.1, 'ds_red', pv, light=15)]
        return L
    L = [BX(sx, 2.6, 6.6, 9.8, 17.6, -2.4, 2.4, 'ds_dark', pv), BX(sx, 2.4, 6.8, 10.6, 16.0, -2.9, -2.3, P, pv),
         BX(sx, 6.6, 7.6, 11.6, 18.2, -3.4, 2.4, P, pv)]
    if not (form == 'broken' and sx < 0):                     # (the front tasset - broken off the left leg in phase 2)
        L += [BX(sx, 1.4, 7.6, 12.0, 17.6, -4.0, -2.9, P, pv), BX(sx, 1.8, 7.2, 10.6, 12.2, -3.7, -2.7, 'ds_edge', pv)]
    else:
        L += [BX(sx, 4.6, 7.6, 15.4, 18.2, -4.0, -2.9, P, pv), BX(sx, 3.0, 3.4, 11.0, 15.0, -2.95, -2.85, 'ds_red', pv, light=15)]
    return L


def _shin(sx, form):
    pv = PIVOT['shinr' if sx > 0 else 'shinl']; P = PL[form]
    if form == 'true':                                        # (tendrils fraying out of the smoke)
        S = [BX(sx, 3.0, 6.2, 5.0, 9.8, -1.6, 1.6, 'ds_smoke', pv)]
        for dx, dz, ln, tw in ((0.0, -0.6, 9.0, 1.0), (-1.0, 0.8, 7.0, -1.0), (1.2, 0.6, 6.0, 1.4)):
            x = sx * (4.6 + dx)
            S += CH([(x, 5.4, dz), (x + sx * tw * 0.8, 5.4 - ln * 0.45, dz - 0.6), (x + sx * tw * 1.4, 5.4 - ln * 0.8, dz + 0.4), (x + sx * tw, 5.4 - ln, dz + 1.2)],
                    (1.5, 0.5), 'ds_smoke', pv)
            S.append(E((x + sx * tw - 0.25, 5.0 - ln, dz + 0.95), (x + sx * tw + 0.25, 5.5 - ln, dz + 1.45), 'ds_red', pv, light=15))
        return S
    S = [BX(sx, 2.4, 6.8, 8.2, 11.0, -3.3, -1.6, 'ds_edge', pv)]                      # (the knee cop and its spike)
    S += SPIKE((sx * 4.6, 10.0, -3.2), (sx * 4.6, 12.6, -5.8), 1.2, pv, bend=(0, -0.4, -0.3), red=False)
    S += [BX(sx, 2.7, 6.5, 2.4, 9.4, -2.4, 2.2, P, pv), BX(sx, 4.1, 5.1, 2.8, 8.4, -2.8, -2.3, 'ds_edge', pv),
          BX(sx, 2.9, 6.3, 3.6, 8.6, 2.2, 2.8, P, pv),
          BX(sx, 2.3, 6.9, 0.0, 2.6, -3.8, 2.6, 'ds_dark', pv), BX(sx, 2.5, 6.7, 0.0, 1.8, -6.2, -3.8, P, pv),
          BX(sx, 2.6, 6.6, 1.8, 2.4, -5.4, -3.6, 'ds_edge', pv)]
    if form == 'broken': S.append(BX(sx, 2.65, 6.55, 5.4, 5.7, -2.5, 2.3, 'ds_red', pv, light=15))
    for x in (3.2, 4.6, 6.0):                                 # (talons; a spur at the heel)
        S += CH([(sx * x, 0.9, -6.0), (sx * x, 0.6, -7.4), (sx * x, 0.25, -8.4)], [0.8, 0.5], 'ds_horn', pv)
    S += CH([(sx * 4.6, 1.4, 2.4), (sx * 4.6, 1.0, 4.0), (sx * 4.6, 0.3, 4.8)], [0.8, 0.5], 'ds_horn', pv)
    return S


def _arm(sx, form):
    pv = PIVOT['armr' if sx > 0 else 'arml']; P = PL[form]; A = []
    true = form == 'true'
    A.append(BX(sx, 9.7, 13.3, 21.6, 28.0, -2.0, 2.0, 'ds_smoke' if true else 'ds_dark', pv))
    if true:
        A += [BX(sx, 9.5, 13.5, 23.0, 26.0, -2.4, -1.6, P, pv, rot=('x', 8, (sx * 11.5, 24.5, -2.0)))]
    else:
        A.append(BX(sx, 9.6, 13.4, 22.6, 27.4, -2.1, 2.1, P, pv))
    # ---- the pauldron: a dome, a cap, two flaring lames under it, three spikes (broken: the left one's snapped)
    if not true:
        A += [BX(sx, 8.6, 15.4, 28.0, 32.6, -4.4, 4.4, P, pv), BX(sx, 9.4, 14.6, 32.6, 33.6, -3.6, 3.6, 'ds_edge', pv),
              BX(sx, 9.8, 16.2, 26.0, 28.2, -4.0, 4.0, P, pv, rot=('z', -sx * 12, (sx * 9.8, 28.2, 0))),
              BX(sx, 10.4, 16.6, 24.4, 26.2, -3.6, 3.6, 'ds_edge', pv, rot=('z', -sx * 18, (sx * 10.4, 26.2, 0))),
              BX(sx, 9.6, 15.6, 27.85, 28.15, -4.15, 4.15, 'ds_red', pv, light=15)]
        snapped = form == 'broken' and sx < 0
        for z, h in ((-2.4, 5.0), (0.0, 7.0), (2.4, 5.0)):
            if snapped:
                A += CH([(sx * 12.4, 33.4, z), (sx * 12.9, 35.0 if z else 35.6, z)], [1.6], 'ds_horn', pv)
            else:
                A += SPIKE((sx * 12.4, 33.4, z), (sx * 14.6, 33.4 + h, z * 1.25), 1.7, pv, bend=(0, 0, 0))
        if snapped: A.append(BX(sx, 12.0, 15.4, 31.0, 32.65, -4.45, -1.2, 'ds_red_d', pv, light=12))
    else:                                                     # (true: the pauldron in floating shards, red light between)
        A += [BX(sx, 8.4, 12.0, 28.4, 33.0, -4.4, 4.4, P, pv), BX(sx, 12.6, 16.0, 27.6, 32.2, -4.0, 4.0, P, pv, rot=('z', -sx * 14, (sx * 12.6, 30, 0))),
              BX(sx, 11.9, 12.7, 28.8, 32.4, -2.0, 2.0, 'ds_red', pv, light=15)]
        A += SPIKE((sx * 11.0, 33.0, 0.0), (sx * 15.0, 41.0, 1.0), 1.8, pv)
        A += SPIKE((sx * 14.2, 31.4, -1.6), (sx * 18.4, 37.6, -2.4), 1.4, pv)
    return A


def _fore(sx, form):
    pv = PIVOT['forer' if sx > 0 else 'forel']; P = PL[form]; F = []
    true = form == 'true'
    F += [BX(sx, 9.4, 13.6, 19.4, 22.4, -2.4, 2.4, 'ds_edge', pv),
          BX(sx, 9.8, 13.2, 14.4, 19.6, -1.8, 1.8, P, pv),
          BX(sx, 9.3, 13.7, 14.8, 16.4, -2.3, 2.3, 'ds_iron', pv),                     # (the manacle)
          BX(sx, 9.4, 13.6, 13.4, 14.8, -2.2, 2.2, 'ds_edge', pv),
          BX(sx, 9.9, 13.1, 9.6, 13.4, -2.0, 1.8, 'ds_dark', pv), BX(sx, 9.7, 13.3, 10.4, 13.0, -2.5, -1.9, 'ds_edge', pv)]
    F += SPIKE((sx * 13.6, 21.0, 0.8), (sx * 16.6, 23.8, 2.0), 1.2, pv, red=False)               # (the elbow's fin)
    F += LINKS([(sx * 13.9, 15.6, 1.2), (sx * 14.3, 11.0, 1.4), (sx * 14.2, 8.6 if not true else 6.0, 1.0)], pv)
    grip = sx > 0 and form != 'true'
    for x in (10.3, 11.1, 11.9, 12.7):                        # talons: curled back under the grip (right), splayed (left; true)
        if grip:
            F += CH([(sx * x, 9.8, -1.4), (sx * x, 7.9, -1.9), (sx * x, 6.6, -1.0)], [0.7, 0.45], 'ds_horn', pv)
        else:
            ln = 1.6 if true else 1.0
            F += CH([(sx * x, 9.8, -1.8), (sx * x, 9.8 - 2.2 * ln, -3.4 - 0.4 * ln), (sx * x, 9.8 - 3.4 * ln, -3.0 - 0.6 * ln)], [0.75, 0.45], 'ds_horn', pv)
    if true and sx > 0:                                       # (void-glass creeping up the arm from the fused blade)
        for (y, z, s) in ((14.0, -2.0, 1.6), (16.6, -1.6, 1.3), (18.8, -1.9, 1.0), (12.4, 1.6, 1.4)):
            F.append(GEM((sx * 12.6, y, z), s, 'ds_glass', pv, light=0, rot=(20.0, 30.0, 40.0)))
    if form == 'broken': F.append(BX(sx, 9.75, 13.25, 17.6, 17.9, -1.85, 1.85, 'ds_red', pv, light=15))
    return F


def _weapon(form):
    """the greatsword: a jagged blade of void-glass veined in red (along -z from the fist, its edges up and down), a guard of
    black spikes with an eye in it, a wrapped grip, a pommel set with a red stone. true: fused - no hilt, the glass grown out of
    the fist"""
    pv = PIVOT['weapon']; X, Y, Z = pv; W = []
    true = form == 'true'
    if not true:
        W += [E((X - 0.6, Y - 0.6, Z - 2.2), (X + 0.6, Y + 0.6, Z + 3.0), 'ds_grip'), E((X - 0.9, Y - 0.9, Z + 3.0), (X + 0.9, Y + 0.9, Z + 4.4), 'ds_iron'),
              GEM((X, Y, Z + 4.6), 1.0, 'ds_red', pv), E((X - 0.8, Y - 4.4, Z - 3.4), (X + 0.8, Y + 4.4, Z - 2.2), 'ds_plate'),
              E((X - 0.85, Y - 0.7, Z - 3.1), (X + 0.85, Y + 0.7, Z - 2.5), 'ds_eye_r', pv, light=15)]
        for sy in (1, -1):
            W += SPIKE((X, Y + sy * 4.0, Z - 2.8), (X, Y + sy * 6.0, Z - 5.6), 1.2, pv)
        z0, L, w0 = Z - 3.4, 25.0, 4.6
    else:
        for (dy, dz, s) in ((1.6, 0.6, 2.0), (-1.4, 0.0, 1.6), (0.4, -1.8, 2.2), (1.8, -2.4, 1.2)):
            W.append(GEM((X + 0.4, Y + dy, Z + dz), s, 'ds_glass', pv, light=0, rot=(30.0 * dy, 40.0, 20.0)))
        z0, L, w0 = Z - 2.0, 28.0, 4.0
    # the blade, tapering in steps, saw-teeth on both edges, a red vein down both flats
    n = 6
    for i in range(n):
        za, zb = z0 - L * i / n, z0 - L * (i + 1) / n
        w = w0 * (1 - 0.62 * i / n)
        W.append(E((X - 0.5, Y - w / 2, zb), (X + 0.5, Y + w / 2, za + 0.05), 'ds_glass'))
    W.append(seg((X, Y, z0 - L), (X, Y - 0.6, z0 - L - 3.0), 1.0, 0.9, 'ds_glass', pv, (1, 0, 0), 0.1))
    W.append(E((X - 0.56, Y - 0.25, z0 - L + 0.6), (X + 0.56, Y + 0.25, z0 - 0.4), 'ds_red', pv, light=15))
    for i in range(1, 9):
        z = z0 - L * i / 9.5; w = w0 * (1 - 0.62 * (L * i / 9.5) / L)
        for sy in (1, -1):
            c = (X, Y + sy * (w / 2 + 0.3), z)
            W.append(E((c[0] - 0.4, c[1] - 0.5, c[2] - 0.5), (c[0] + 0.4, c[1] + 0.5, c[2] + 0.5), 'ds_glass', pv, rot=('x', 45 * sy, c)))
    if true:
        for i in (2, 4):
            z = z0 - L * i / 6
            W += CH([(X, Y + 1.2, z), (X, Y + 3.8, z - 1.6)], [0.8], 'ds_glass', pv)
    return W


def _wing_fold(name):
    """folded: a long panel of membrane hanging down its back - with its fellows, the cloak - the bone along its top, a finger
    bone down its outer edge, a clawed thumb at the shoulder, ragged at the foot, eyes shut in it"""
    i, sx = int(name[1]), (1 if name[2] == 'r' else -1)
    pv = PIVOT[name]; px, py, pz = pv
    width, bottom, z0 = {1: (9.0, 2.2, 5.9), 2: (8.0, 1.4, 5.5), 3: (6.8, 2.6, 5.1)}[i]
    rnd = random.Random(31 + i * 2 + (sx > 0)); W = []
    n = 5; top = py + 0.6
    for k in range(n):
        x0, x1 = 0.3 + width * k / n, 0.3 + width * (k + 1) / n
        b = bottom + rnd.uniform(0, 3.2) + (1.6 if k == n - 1 else 0)
        W.append(BX(sx, x0, x1 + 0.02, b, top, z0, z0 + 0.4, 'ds_membrane', pv))
        if rnd.random() < 0.6: W.append(BX(sx, x0 + 0.4, x0 + 1.0, b - rnd.uniform(1.0, 2.4), b, z0 + 0.05, z0 + 0.35, 'ds_membrane', pv))
    W += CH([(sx * 0.8, top + 0.4, z0 + 0.4), (sx * (width + 0.3), top, z0 + 0.5)], [1.2], 'ds_wbone', pv)
    W += CH([(sx * (width + 0.3), top, z0 + 0.5), (sx * (width + 0.5), bottom + 6, z0 + 0.4)], [0.9], 'ds_wbone', pv)
    W += CH([(sx * (width + 0.3), top, z0 + 0.5), (sx * (width + 1.2), top + 2.0, z0 + 0.8)], [0.8], 'ds_horn', pv)
    if i == 1:
        for (x, y) in ((3.4, py - 9.0), (6.4, py - 16.0), (2.2, py - 21.0)):
            W.append(BX(sx, x - 0.8, x + 0.8, y - 0.3, y + 0.3, z0 + 0.4, z0 + 0.5, 'ds_red', pv, light=10))
    return W


def _wing_open(name, true=False):
    """unfurled: the arm bone out from its root, fingers fanning down from it, membrane hung between in strips (the trailing
    edge scalloped and torn), eyes open in it"""
    i, sx = int(name[1]), (1 if name[2] == 'r' else -1)
    pv = PIVOT[name]; px, py, pz = pv
    L, D0 = {1: (32.0, 16.0), 2: (28.0, 13.5), 3: (22.0, 10.5)}[i]
    if true: L, D0 = L * 1.2, D0 * 1.15
    rnd = random.Random(70 + i + 10 * true + (sx > 0)); W = []
    def arm_y(x):                                             # (the arm's height at x out along it, from the root)
        t = x / L; return py + 4.0 * math.sin(math.pi * min(1.0, t * 1.15)) + 1.5 * t
    fingers = [0.34, 0.55, 0.74, 0.9, 1.0]
    def edge(x):                                              # (the trailing edge: deepest at each finger, scalloped between)
        t = x / L; dist = min(abs(t - f) for f in fingers + [0.0])
        return arm_y(x) - D0 * (1 - 0.55 * t) * (1 - 2.2 * dist)
    zm = pz + 1.3
    nstrip = int(L / 1.8)
    for k in range(nstrip):
        x0, x1 = L * k / nstrip, L * (k + 1) / nstrip; xm = (x0 + x1) / 2
        b = edge(xm) + (rnd.uniform(-0.6, 1.2) if true else 0)
        W.append(BX(sx, px * sx + x0, px * sx + x1 + 0.03, b, arm_y(xm), zm, zm + 0.4, 'ds_membrane_t' if true else 'ds_membrane', pv))
        if true and rnd.random() < 0.2:                      # (tatters, and smoke off the ragged edge)
            W.append(BX(sx, px * sx + x0 + 0.3, px * sx + x0 + 0.9, b - rnd.uniform(1.5, 3.5), b, zm + 0.1, zm + 0.3, 'ds_smoke', pv))
    a_pts = [(px + sx * L * t, arm_y(L * t), zm + 0.2 - 0.6 * (1 - t)) for t in (0.0, 0.3, 0.65, 1.0)]
    W += CH(a_pts, (1.8, 0.9), 'ds_wbone', pv)
    W += SPIKE(a_pts[2], (px + sx * (L * 0.65 + 1.0), a_pts[2][1] + 3.0, zm + 0.4), 1.0, pv)          # (the clawed thumb)
    for f in fingers:
        x = L * f; ax = px + sx * x
        W += CH([(ax, arm_y(x), zm + 0.2), (ax + sx * 0.8, edge(x) + 0.3, zm + 0.2)], [0.7], 'ds_wbone', pv)
        W += CH([(ax + sx * 0.8, edge(x) + 0.3, zm + 0.2), (ax + sx * 1.6, edge(x) - 1.0, zm + 0.2)], [0.5], 'ds_horn', pv)
    eyes = {1: [0.2, 0.45, 0.66, 0.83], 2: [0.3, 0.64], 3: [0.45, 0.8]}[i] + ([0.95] if true else [])
    for t in eyes:
        x = L * t; cy = (arm_y(x) + edge(x)) / 2 + 0.6; ex = px + sx * x; s = 1.4 if not true else 1.6
        W.append(E((ex - s, cy - s * 0.65, zm - 0.25), (ex + s, cy + s * 0.65, zm + 0.65), 'ds_eye', pv, light=15,
                   uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, faces=('north', 'south', 'east', 'west', 'up', 'down')))
    return W


def _fx(kind):
    pv = PIVOT['fx']; X, Y, Z = pv; F = []
    if kind == 'charge':                                      # (light gathering at the eye: a hot core, rays, motes)
        F += [GEM((X, Y, Z - 1.6), 1.8, 'ds_red_l', pv), GEM((X, Y, Z - 1.6), 3.0, 'ds_red', pv, rot=(0.0, 0.0, 45.0))]
        for a in range(0, 360, 30):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); r = 5.5 if a % 60 == 0 else 4.0
            F.append(seg((X + 2.2 * ca, Y + 2.2 * sa, Z - 1.6), (X + r * ca, Y + r * sa, Z - 1.4), 0.35, 0.35, 'ds_red_l', pv, ext=0, light=15))
    elif kind == 'beam':                                      # (a beam of red light, a hot core in a sheath, rings down it)
        F += [E((X - 0.7, Y - 0.7, Z - 44.0), (X + 0.7, Y + 0.7, Z - 0.5), 'ds_red_l', pv, light=15),
              E((X - 1.4, Y - 1.4, Z - 42.0), (X + 1.4, Y + 1.4, Z - 1.5), 'ds_red', pv, light=15, faces=('east', 'west', 'up', 'down')),
              GEM((X, Y, Z - 1.2), 2.6, 'ds_red_l', pv)]
        for k in range(1, 6):
            z = Z - 7.0 * k; r = 2.4 - 0.15 * k
            F.append(E((X - r, Y - r, z - 0.4), (X + r, Y + r, z + 0.4), 'ds_red', pv, light=15))
    else:                                                     # (the follower's eye bolt: a red-hot shard flying, its trail)
        F += [GEM((X, Y, Z - 7.0), 1.6, 'ds_red_l', pv, rot=(0.0, 0.0, 45.0)),
              E((X - 0.4, Y - 0.4, Z - 6.4), (X + 0.4, Y + 0.4, Z - 1.6), 'ds_red', pv, light=15)]
        for z in (-2.5, -4.2):
            F.append(E((X - 0.2 + z * 0.05, Y + 0.6, Z + z - 0.2), (X + 0.2 + z * 0.05, Y + 1.0, Z + z + 0.2), 'ds_red_l', pv, light=15))
    return F


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(5)
    def mk(part, fn, *a):
        _PV[0] = PIVOT[part]; return (part, fn(*a))
    R = {}
    for form in FORMS:
        faces = (None,) + (EYE_FACES if form == 'true' else FACES)
        for f in faces:
            R[f'{PREFIX}head_{form}{"_x" + f if f else ""}'] = mk('head', _head, form, f)
    for form, tag in (('armored', 'a'), ('broken', 'b'), ('true', 't')):
        R[f'{PREFIX}body_{tag}'] = mk('body', _body, form)
        R[f'{PREFIX}chest_{tag}'] = mk('chest', _chest, form)
        for sx, s in ((1, 'r'), (-1, 'l')):
            R[f'{PREFIX}arm{s}_{tag}'] = mk(f'arm{s}', _arm, sx, form); R[f'{PREFIX}fore{s}_{tag}'] = mk(f'fore{s}', _fore, sx, form)
            R[f'{PREFIX}leg{s}_{tag}'] = mk(f'leg{s}', _leg, sx, form); R[f'{PREFIX}shin{s}_{tag}'] = mk(f'shin{s}', _shin, sx, form)
    R[f'{PREFIX}chest_n'] = mk('chest', _chest, 'bound')
    R[f'{PREFIX}weapon_a'] = mk('weapon', _weapon, 'armored'); R[f'{PREFIX}weapon_t'] = mk('weapon', _weapon, 'true')
    for w in WINGS:
        R[f'{PREFIX}{w}_fold'] = mk(w, _wing_fold, w); R[f'{PREFIX}{w}_open'] = mk(w, _wing_open, w); R[f'{PREFIX}{w}_true'] = mk(w, _wing_open, w, True)
    for k in FX:
        R[f'{PREFIX}fx_{k}'] = mk('fx', _fx, k)
    _RAW.update(R)
    return _RAW


def models():
    M = {}
    for name, (part, els) in _build().items():
        k = PART_K.get(part, 1.0)
        els = shrink(els, k) if k != 1.0 else els
        for e in els:                                         # (every element inside the model box)
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


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
    units), as the pose stands"""
    raw = _build(); xf = rigkit.solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        if HIDDEN(p, pose): continue
        Q, t = xf[p]; pv = PIVOT[p]; dp = D(pv); W = tuple(t[i] + dp[i] for i in range(3))
        bl = []
        for e in raw[model_name(p, pose)][1]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))                     # (model -> design)
            cw = qrot(Q, tuple(D(cd)[i] - dp[i] for i in range(3)))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h)))
        out[p] = bl
    return out


def lowest(pose, parts):
    lo = 1e9
    for bl in world_boxes(pose, parts).values():
        for c, ax, h in bl:
            lo = min(lo, c[1] - sum(abs(ax[i][1]) * h[i] for i in range(3)))
    return lo


def _wq(p, w, q):
    p[w] = q


def finish(p, tip=None):
    """(after grounding) the folded wings hang as a cloak does - by the world's down, whatever the chest is doing, flared back by
    their own turn - and are swung back until their ragged foot clears the floor; the greatsword, if a tip height is asked
    (tip: design units - below 0 is planted in the ground), turned at the wrist until its point is there"""
    p = dict(p)
    if wing_mode(p) == 'fold' and not p.get('_nohang'):
        Qc = rigkit.solve(PIVOT, PARENT, p)['chest'][0]; u = qrot(Qc, (0.0, 1.0, 0.0))
        pitch = math.degrees(math.atan2(u[2], u[1]))
        for w in WINGS: p[w] = rigkit.qmul(qa_x(-pitch), p.get(w, rigkit.I))
        for _ in range(0 if p.get('_pool') else 30):     # (_pool: seated - let it pool on the floor instead)
            if lowest(p, WINGS) >= 0.6: break
            for w in WINGS: p[w] = rigkit.qmul(qa_x(4.0), p[w])
    if tip is not None and not HIDDEN('weapon', p):
        base = p.get('weapon', rigkit.I); best = None
        for a in range(-90, 91, 2):
            q = rigkit.qmul(qa_x(a), base); p['weapon'] = q
            err = abs(lowest(p, ('weapon',)) - tip) + abs(a) * 0.01
            if best is None or err < best[0]: best = (err, q)
        p['weapon'] = best[1]
    return p


def qa_x(d):
    return rigkit.qa('x', d)


GROUND_PARTS = ('body', 'legr', 'legl', 'shinr', 'shinl')


def ground(pose, parts=GROUND_PARTS):
    """set the root's height so the lowest point of these parts rests on y=0"""
    pose = dict(pose); o = pose.get('_off', (0.0, 0.0, 0.0)); pose['_off'] = (o[0], 0.0, o[2])
    lo = lowest(pose, parts); pose['_off'] = (o[0], -lo, o[2])
    return pose


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit, display frame: ('x', +a) leans a trunk forward / nods the head down; limb(fwd) swings a hanging limb forward, (out)
#  out to its own side and up; a shin bends back with knee(a); ('y', +a) on the chest turns its right shoulder forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def knee(a):
    return qs(('x', a))


def T(lean=0.0, twist=0.0, side=0.0):
    return qs(('y', twist), ('x', lean), ('z', side))


def wing(sx, up=0.0, sweep=0.0, roll=0.0):
    """an open wing: raised (up), swept forward (sweep, + toward the front), rolled"""
    return qs(('y', sweep * sx), ('z', -up * sx), ('x', roll))


def cloak(sx, back=0.0, out=0.0):
    """a folded wing (the cloak): its foot swung back (back) and out to its side (out)"""
    return qs(('x', back), ('z', -out * sx))


OPEN = {  # (name: per wing (up, sweep), w1 / w2 / w3)
    'rest': ((36, -14), (8, -18), (-20, -16)),
    'spread': ((48, -4), (16, -2), (-14, -2)),
    'high': ((64, -10), (38, -10), (10, -10)),
    'forward': ((56, 12), (28, 14), (-14, 12)),
    'back': ((38, -36), (10, -40), (-18, -38)),
    'droop': ((8, -30), (-20, -28), (-42, -24)),
    'fallen': ((-6, -40), (-28, -34), (-50, -28)),
    'tucked': ((22, -40), (-2, -44), (-26, -40)),
}
FOLD = {'rest': (4, 0), 'spread': (14, 10), 'high': (12, 4), 'forward': (0, 0), 'back': (14, 2), 'droop': (6, 0), 'fallen': (40, 6),
        'tucked': (4, 0)}


def wings(mode, form, open_=None, bump=(0.0, 0.0), cl=None):
    """the six wings' turns for a wing mode: open wings by OPEN, folded ones (the cloak) by FOLD (or cl=(back, out))"""
    w = open_ if open_ is not None else form in ('broken', 'true')
    out = {}
    for sx, s in ((1, 'r'), (-1, 'l')):
        for i in range(3):
            if w:
                up, sw = OPEN[mode][i]
                if form == 'true' and i == 2: up, sw = up + 8, sw - 8          # (its longer lower wings kept off the robe)
                out[f'w{i + 1}{s}'] = wing(sx, up + bump[0] * (1 - 0.3 * i), sw + bump[1])
            else:
                b, o = cl or FOLD[mode]; out[f'w{i + 1}{s}'] = cloak(sx, b + 1.5 * i, o + 2 * (2 - i))
    return out


def P(**kw):
    return kw


s_ = math.sin
STAND = dict(legr=limb(1, 0, 3), shinr=limb(1, 0, -3), legl=limb(-1, 0, 3), shinl=limb(-1, 0, -3))


def _boss(name, form):
    """one boss pose for a form - None where the move isn't that form's"""
    true = form == 'true'
    # the true form's tendrils (legs): trailing back and swaying, by phase t
    def tend(t=0.0, spread=6, back=10):
        return dict(legr=limb(1, -back + 6 * s_(t), spread), shinr=knee(14 + 10 * s_(t + 1)), legl=limb(-1, -back - 6 * s_(t), spread),
                    shinl=knee(14 - 10 * s_(t + 1)))
    legs = tend() if true else STAND
    hold = dict(armr=limb(1, 14, 8), forer=limb(1, 26), weapon=qs(('x', 62))) if not true else dict(armr=limb(1, 16, 12), forer=limb(1, 30), weapon=qs(('x', 48)))
    claw = dict(arml=limb(-1, 8, 12), forel=limb(-1, 22))
    face_hot = 'wide'
    if name == 'idle_a':
        p = P(chest=T(8), head=T(12), **legs, **hold, **claw, **wings('rest', form))
    elif name == 'idle_b':                                    # (breathing in: the chest up, the head turning to look round)
        p = P(_face='narrowed', chest=T(3, -6), head=T(8, 14, 4), **legs, armr=limb(1, 12, 10), forer=limb(1, 30), weapon=qs(('x', 60)),
              arml=limb(-1, 4, 16), forel=limb(-1, 34), **wings('rest', form, bump=(6, 0), cl=(6, 2)))
    elif name == 'dormant':                                   # (sealed: kneeling on its right knee, the greatsword planted, head bowed)
        if form != 'armored': return None
        p = P(_face='closed', body=T(2), chest=T(10), head=T(30), legr=limb(1, 0, 4), shinr=knee(90), legl=limb(-1, 84, 4), shinl=knee(84),
              armr=limb(1, 52, 6, 30), forer=limb(1, 40, 0, 10), weapon=qs(('x', 74), ('y', 18)), arml=limb(-1, 50, 8, 22), forel=limb(-1, 50, 0, 4),
              **wings('rest', form, cl=(34, 8)))
    elif name == 'rise':                                      # (waking: the left foot planted, the right knee coming up, the head lifting)
        if form != 'armored': return None
        p = P(_face='wide', body=T(4), chest=T(4), head=T(-6), legr=limb(1, 36, 4), shinr=knee(92), legl=limb(-1, 70, 4), shinl=knee(72),
              armr=limb(1, 30, 22), forer=limb(1, 30), weapon=qs(('x', 64)), arml=limb(-1, 20, 34), forel=limb(-1, 40), **wings('spread', form, cl=(22, 10)))
    elif name.startswith('walk_'):                            # (slow and heavy: short steps, the body rolling over them; true: drifting)
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        if true:
            p = P(_off=(0, HOVER + 0.8 * s_(ph * 2), 0), chest=T(10, 4 * sw), head=T(12), **tend(ph, 6, 18), armr=limb(1, 14 - 6 * sw, 12),
                  forer=limb(1, 30), weapon=qs(('x', 48)), arml=limb(-1, 6 + 6 * sw, 14), forel=limb(-1, 22),
                  **wings('rest', form, bump=(8 * s_(ph * 2), 0)))
        else:
            p = P(chest=T(9, 4 * sw), head=T(11, -2 * sw), legr=limb(1, 16 * sw, 3), shinr=knee(6 + 16 * max(0, -s_(ph + 0.6))),
                  legl=limb(-1, -16 * sw, 3), shinl=knee(6 + 16 * max(0, s_(ph + 0.6))),
                  armr=limb(1, 14 - 6 * sw, 8), forer=limb(1, 26), weapon=qs(('x', 62)), arml=limb(-1, 8 + 8 * sw, 12), forel=limb(-1, 22),
                  **wings('rest', form, bump=(5 * sw, 0), cl=(18, 4)))
    elif name == 'slam_up':                                   # (the greatsword up over its head, leaning back)
        p = P(_face=face_hot, chest=T(-10, -8), head=T(-10), **legs, armr=limb(1, 160, 14), forer=limb(1, 30), weapon=qs(('x', 70)),
              arml=limb(-1, 120, 18), forel=limb(-1, 40), **wings('spread', form, bump=(0, -18), cl=(16, 8)))
    elif name == 'slam':                                      # (and down into the ground before it, crouching into the blow)
        lg = dict(legr=limb(1, 30, 4), shinr=knee(40), legl=limb(-1, -12, 4), shinl=knee(18)) if not true else tend(0, 8, 0)
        p = P(_face=face_hot, chest=T(30, 8), head=T(6), **lg, armr=limb(1, 70, 6), forer=limb(1, 6), weapon=qs(('x', 40)),
              arml=limb(-1, 50, 20), forel=limb(-1, 30), **wings('high', form, bump=(0, -18), cl=(30, 10)))
    elif name == 'sweep_up':                                  # (wound round to its right, the blade out behind it)
        p = P(_face='narrowed', chest=T(8, -28), head=T(8, 22), **legs, armr=limb(1, -20, 70, -40), forer=limb(1, 20), weapon=qs(('x', 10)),
              arml=limb(-1, 60, 10), forel=limb(-1, 40), **wings('back', form, cl=(20, 6)))
    elif name == 'sweep':                                     # (the arc: round to its left, the blade flat across its front)
        p = P(_face=face_hot, chest=T(10, 30), head=T(8, -20), **legs, armr=limb(1, 84, 12, 30), forer=limb(1, 8), weapon=qs(('x', 84)),
              arml=limb(-1, -24, 30), forel=limb(-1, 20), **wings('back', form, cl=(20, 10)))
    elif name == 'stab':                                      # (a lunge, the point straight out)
        lg = dict(legr=limb(1, 34, 3), shinr=knee(34), legl=limb(-1, -22, 3), shinl=knee(10)) if not true else tend(0, 4, 20)
        p = P(_face=face_hot, chest=T(18, 22), head=T(-4, -12), **lg, armr=limb(1, 88, 0, 10), forer=limb(1, 0), weapon=qs(('x', 88)),
              arml=limb(-1, -30, 20), forel=limb(-1, 30), **wings('back', form, cl=(16, 4)))
    elif name == 'roar':                                      # (head back, arms and wings flung wide)
        p = P(_face='wide', _wings='open', chest=T(-12), head=T(-12), **legs, armr=limb(1, 34, 42), forer=limb(1, 34, -20), weapon=qs(('x', 50)),
              arml=limb(-1, 34, 42), forel=limb(-1, 34, -20), **wings('spread', form, open_=True, bump=(0, -16)))
    elif name == 'summon':                                    # (arms raised, calling its knights)
        p = P(_face='wide', chest=T(-8), head=T(-8), **legs, armr=limb(1, 150, 26), forer=limb(1, 10), weapon=qs(('x', 70)),
              arml=limb(-1, 150, 26), forel=limb(-1, 10), **wings('high', form, cl=(10, 6)))
    elif name == 'wing_gust':                                 # (the wings beaten forward; braced, arms across)
        if form == 'armored': return None
        p = P(_face='narrowed', chest=T(-6), head=T(6), **legs, armr=limb(1, 4, 16), forer=limb(1, 50), weapon=qs(('x', 70)),
              arml=limb(-1, 4, 16), forel=limb(-1, 50), **wings('forward', form))
    elif name == 'eye_beam_up':                               # (the eye charging: the head drawn back, wings raised)
        if not true: return None
        p = P(_face='wide', _fx='charge', chest=T(-6), head=T(-10), **legs, armr=limb(1, 24, 28), forer=limb(1, 40), weapon=qs(('x', 50)),
              arml=limb(-1, 24, 28), forel=limb(-1, 30), **wings('high', form))
    elif name == 'eye_beam':                                  # (and the beam, the head thrust down at you)
        if not true: return None
        p = P(_face='narrowed', _fx='beam', chest=T(14), head=T(16), **legs, armr=limb(1, 6, 30), forer=limb(1, 20), weapon=qs(('x', 50)),
              arml=limb(-1, 6, 30), forel=limb(-1, 20), **wings('back', form))
    elif name == 'heart_pulse':                               # (the chest thrust out, the arms pulled back: the heart flares)
        p = P(_face='wide', chest=T(-16), head=T(-12), **legs, armr=limb(1, -26, 34), forer=limb(1, 30), weapon=qs(('x', 60)),
              arml=limb(-1, -26, 34), forel=limb(-1, 30), **wings('spread' if not true else 'high', form, cl=(14, 12)))
    elif name == 'stagger':                                   # (between phases: down on its left knee, the sword planted, armour breaking)
        if true: return None
        p = P(_face='dim', body=T(4), chest=T(14, 8), head=T(26, -8), legr=limb(1, 80, 6), shinr=knee(86), legl=limb(-1, -2, 6), shinl=knee(92),
              armr=limb(1, 46, 16), forer=limb(1, 30), weapon=qs(('x', 92)), arml=limb(-1, 30, 20), forel=limb(-1, 50), **wings('droop', form, cl=(30, 6)))
    elif name.startswith('death_') and not true:
        return None
    elif name == 'death_0':                                   # (struck through: recoiling, the arms flung, the eye wide)
        lg = dict(legr=limb(1, 10, 6), shinr=knee(24), legl=limb(-1, -8, 6), shinl=knee(14)) if not true else tend(0, 10, 4)
        p = P(_face='wide', _weapon='none' if not true else None, chest=T(-22), head=T(-20, 10), **lg, armr=limb(1, 40, 38), forer=limb(1, 40),
              arml=limb(-1, 50, 36), forel=limb(-1, 30), weapon=qs(('x', 40)), **wings('high', form, bump=(0, -22)))
    elif name == 'death_1':                                   # (failing: sinking, the head dropping, the wings sagging)
        lg = dict(legr=limb(1, 60, 6), shinr=knee(100), legl=limb(-1, 50, 6), shinl=knee(96)) if not true else tend(0, 14, -10)
        p = P(_face='dim', _weapon='none' if not true else None, chest=T(30), head=T(30, -10), **lg, armr=limb(1, 10, 14), forer=limb(1, 10),
              arml=limb(-1, 14, 14), forel=limb(-1, 10), weapon=qs(('x', 80)), **wings('droop', form))
    elif name == 'death_2':                                   # (unravelled: slumped to the ground, the wings over it like a shroud)
        lg = dict(legr=limb(1, 84, 8), shinr=knee(120), legl=limb(-1, 80, 8), shinl=knee(118)) if not true else \
            dict(legr=limb(1, -70, 30), shinr=knee(20), legl=limb(-1, -66, 30), shinl=knee(24))
        p = P(_face='closed', _weapon='none' if not true else None, chest=T(56), head=T(26, 14, 10), **lg, armr=limb(1, 40, 14), forer=limb(1, 20),
              arml=limb(-1, 46, 10), forel=limb(-1, 20), weapon=qs(('x', 80)), **wings('fallen', form))
    else:
        raise KeyError(name)
    p = {k: v for k, v in p.items() if v is not None}
    p['_form'] = form
    tip = BOSS_TIP.get(name)
    if true and name not in ('death_2',):
        p['_off'] = p.get('_off', (0, HOVER, 0))
        if name == 'death_1': p['_off'] = (0, 2.0, 0)
        return finish(p, tip if (tip is None or tip > 0) else None)
    if name == 'death_2':
        return finish(ground(p, GROUND_PARTS + ('chest', 'head', 'forer', 'forel')), tip)
    return finish(ground(p), tip)


BOSS_TIP = {'idle_a': 1.2, 'idle_b': 2.0, 'walk_0': 2.0, 'walk_1': 2.0, 'walk_2': 2.0, 'walk_3': 2.0, 'heart_pulse': 1.5,
            'dormant': -4.0, 'stagger': -3.0, 'slam': -2.0, 'death_1': 1.0, 'death_2': 0.4}


BOSS_NAMES = ['idle_a', 'idle_b', 'dormant', 'rise', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'slam_up', 'slam', 'sweep_up', 'sweep', 'stab',
              'roar', 'summon', 'wing_gust', 'eye_beam_up', 'eye_beam', 'heart_pulse', 'stagger', 'death_0', 'death_1', 'death_2']
BOSS_POSES = {f: {n: p for n in BOSS_NAMES if (p := _boss(n, f)) is not None} for f in ('armored', 'broken', 'true')}
BOSS_DRAFT = {f: [n for n in BOSS_NAMES if n in BOSS_POSES[f] and n not in ('walk_0', 'walk_2', 'walk_3')] for f in BOSS_POSES}


# ---- the follower (form 'bound', at RIG_SCALE)
FW = lambda mode='rest', **kw: wings(mode, 'bound', **kw)
F_HOLD = dict(armr=limb(1, 14, 8), forer=limb(1, 26), weapon=qs(('x', 62)))
SWIM_FRAMES = 8


def _fol():
    G = ground
    po = {
        'idle_a': G(P(chest=T(6), head=T(6), **STAND, **F_HOLD, arml=limb(-1, 8, 12), forel=limb(-1, 22), **FW())),
        'idle_b': G(P(_face='narrowed', chest=T(2, -6), head=T(2, 18, 4), **STAND, armr=limb(1, 12, 10), forer=limb(1, 30), weapon=qs(('x', 60)),
                      arml=limb(-1, 2, 14), forel=limb(-1, 70), **FW(cl=(6, 2)))),
    }
    for k in range(4):
        ph = math.pi * k / 2; sw = s_(ph)
        po[f'walk_{k}'] = G(P(chest=T(6, 4 * sw), head=T(4), legr=limb(1, 24 * sw, 3), shinr=knee(6 + 24 * max(0, -s_(ph + 0.6))),
                              legl=limb(-1, -24 * sw, 3), shinl=knee(6 + 24 * max(0, s_(ph + 0.6))), armr=limb(1, 14 - 12 * sw, 8), forer=limb(1, 26),
                              weapon=qs(('x', 62)), arml=limb(-1, 8 + 14 * sw, 12), forel=limb(-1, 22), **FW(cl=(24, 4))))
        rl = (40, 8, -34, 8)[k]; ll = (-34, 8, 40, 8)[k]
        po[f'run_{k}'] = G(P(chest=T(13, 6 * sw), head=T(-6), legr=limb(1, rl, 3), shinr=knee((10, 70, 30, 20)[k]), legl=limb(-1, ll, 3),
                             shinl=knee((30, 20, 10, 70)[k]), armr=limb(1, 30 - 20 * sw, 14), forer=limb(1, 50), weapon=qs(('x', 30)),
                             arml=limb(-1, 10 + 30 * sw, 14), forel=limb(-1, 50), **FW(cl=(30, 6))))
        if (0.0, 2.0, 3.0, 1.0)[k]: po[f'run_{k}']['_off'] = tuple(v + (0, (0.0, 2.0, 3.0, 1.0)[k], 0)[i] for i, v in enumerate(po[f'run_{k}']['_off']))
    jump = P(_face='wide', chest=T(4), head=T(-8), legr=limb(1, 40), shinr=knee(60), legl=limb(-1, 10), shinl=knee(40), armr=limb(1, 50, 16),
             forer=limb(1, 30), weapon=qs(('x', 40)), arml=limb(-1, 40, 18), forel=limb(-1, 20), **FW(cl=(26, 10)))
    jump = G(jump); jump['_off'] = (0, jump['_off'][1] + 6.0, 0); po['jump'] = jump
    po.update({
        # seated on the ground, a knee up, its forearm on it, the greatsword laid across its lap
        'sit_a': G(P(_pool=True, body=T(-8), chest=T(8), head=T(14, -10), legr=limb(1, 74, 10), shinr=knee(100), legl=limb(-1, 84, 18), shinl=knee(40),
                     armr=limb(1, 40, 8, 20), forer=limb(1, 50), weapon=qs(('x', 20), ('y', 60)), arml=limb(-1, 26, 18), forel=limb(-1, 30),
                     **FW(cl=(26, 12))), GROUND_PARTS),
        # kneeling on one knee, the sword planted, head bowed - keeping a vigil
        'sit_b': G(P(_face='dim', body=T(2), chest=T(10), head=T(26), legr=limb(1, 0, 4), shinr=knee(90), legl=limb(-1, 84, 4), shinl=knee(84),
                     armr=limb(1, 52, 6, 30), forer=limb(1, 40, 0, 10), weapon=qs(('x', 74), ('y', 18)), arml=limb(-1, 50, 8, 22), forel=limb(-1, 50, 0, 4),
                     **FW(cl=(34, 8)))),
        # pleased (in its way): the greatsword raised in salute, the ember flaring
        'happy': G(P(_face='wide', chest=T(-4), head=T(-6), **STAND, armr=limb(1, 120, 10), forer=limb(1, 40), weapon=qs(('x', 50)),
                     arml=limb(-1, 10, 16), forel=limb(-1, 20), **FW(cl=(10, 6)))),
        'hurt': G(P(_face='dim', chest=T(-14, 8), head=T(-16, -10), legr=limb(1, 10), shinr=knee(20), legl=limb(-1, -10), shinl=knee(10),
                    armr=limb(1, 30, 18), forer=limb(1, 30), weapon=qs(('x', 60)), arml=limb(-1, 30, 20), forel=limb(-1, 40), **FW(cl=(16, 6)))),
        # spent: sat back on the ground, legs out, head hanging, arms limp
        'tired': G(P(_pool=True, _face='closed', _weapon='none', body=T(-24), chest=T(14), head=T(36), legr=limb(1, 74, 14), shinr=knee(10), legl=limb(-1, 70, 18),
                     shinl=knee(16), armr=limb(1, 10, 18), forer=limb(1, 10), arml=limb(-1, 12, 18), forel=limb(-1, 10), **FW(cl=(30, 14))),
                   GROUND_PARTS),
        # the greatsword: up over its right shoulder - and down across
        'slash_up': G(P(_face='narrowed', chest=T(-4, -24), head=T(0, 18), **STAND, armr=limb(1, 150, 30), forer=limb(1, 40), weapon=qs(('x', 20)),
                        arml=limb(-1, 40, 20), forel=limb(-1, 40), **FW(cl=(12, 4)))),
        'slash': G(P(_face='wide', chest=T(16, 26), head=T(4, -16), legr=limb(1, 22), shinr=knee(20), legl=limb(-1, -16), shinl=knee(8),
                     armr=limb(1, 64, 10, 24), forer=limb(1, 6), weapon=qs(('x', 30)), arml=limb(-1, -20, 24), forel=limb(-1, 20), **FW(cl=(22, 6)))),
        # the eye bolt: the head drawn back, the ember flaring - and the bolt loosed from the slit
        'bolt_up': G(P(_face='wide', _fx='charge', chest=T(-6), head=T(-12), **STAND, **F_HOLD, arml=limb(-1, 20, 30), forel=limb(-1, 40), **FW(cl=(8, 4)))),
        'bolt': G(P(_face='narrowed', _fx='bolt', chest=T(10), head=T(8), **STAND, **F_HOLD, arml=limb(-1, 50, 10), forel=limb(-1, 20), **FW(cl=(12, 4)))),
    })
    for i in range(SWIM_FRAMES):                              # (a heavy knight's crawl, its head up out of the water)
        ph = 2 * math.pi * i / SWIM_FRAMES
        po[f'swim_{i}'] = P(_off=(0, 12.0, 4.0), _weapon='none', _nohang=True, body=T(70), chest=T(4), head=T(-40), legr=limb(1, 26 - 14 * s_(ph)), shinr=knee(16),
                            legl=limb(-1, 26 + 14 * s_(ph)), shinl=knee(16), armr=limb(1, 150 + 40 * s_(ph), 20), forer=limb(1, 20),
                            arml=limb(-1, 150 - 40 * s_(ph), 20), forel=limb(-1, 20), **FW(cl=(8, 8)))
    tips = {'idle_a': 1.2, 'idle_b': 2.0, 'walk_0': 2.0, 'walk_1': 2.0, 'walk_2': 2.0, 'walk_3': 2.0, 'bolt_up': 1.5, 'bolt': 1.5, 'sit_b': -3.0}
    for n, p in po.items():
        p['_form'] = 'bound'; po[n] = finish(p, tips.get(n))
    return po


POSES = _fol()
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'run_2', 'jump', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired', 'slash_up', 'slash', 'bolt_up', 'bolt',
         'swim_2', 'swim_6']
