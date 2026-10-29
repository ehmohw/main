"""(3.0 draft) THE KEEPER OF BONDS - the 50th follower, and the last: a spirit woven from the threads of every bond you've made.
Earned by having all 49 others; a compass (bond_compass) shows the way to the Loom Sanctuary in the Overworld sky (keeper_sanctuary),
where it waits by its great loom. It is not the Divine One and not a herald: no halo, no wings - a quiet, gentle keeper of threads.

LOOK  A calm, cosy figure (3.0c: 2.14 blocks to the hood's crown as it floats - shorter and a little broader than 3.0's 2.45), robed in woven threads: cream and gold cloth, the
      rainbow of the bonds woven through it. Every follower's own colour (phase125.WHO's) is in it, once:
      - the ROBE from the belt to the hem is a tapestry of 24 woven rows, two followers' colours to a row (the row's colour and
        a twill stitch every fourth cell), running round the colour wheel from gold at the belt, through green, blue, violet
        and rose, to amber at the gold hem; a fringe of loose threads hangs from the hem in all their colours;
      - the 49th colour (the bonds' first: Emma's pink) is the spindle at its heart.
      - Pearl cloth above (a soft vertical warp line), a gold belt and a mantle over the shoulders with a woven border of colour
        blocks; long bell sleeves, the same border at the cuffs, their short drape trailing loose drifting threads (threadr / threadl).
        (3.0b) The cloth is MOTHER-OF-PEARL: kb_robe (and kb_hood, in golds) are animated strips (FRAMES frames, interpolated) - a pastel
        sheen (PEARL: rose, peach, cream, mint, sky, lilac) running diagonally over a warm pearl base and flowing along over
        the frames, a pale highlight band sweeping across once a cycle; every frame keeps each cell's luminance, so the
        wardrobe's luminance recolours (phase138 -> phase99._recolour / gild.metal) come out as clean cloth in the look's
        colours with the highlight passing over them (gen_rp copies the .mcmeta to their _cN copies). The gold trim (kb_gold,
        kb_rim, kb_brd) glints the same way, in rose and champagne golds; the wings are tuned to the same pastels.
      - (3.0c, cheerful) A soft pearl hood, opened wide (gold rim, a deep dusky-rose lining), rounding to a low crown - no
        point; inside it no face of flesh, only the original's warm amber glow (kb_face) with its EYES OF LIGHT smiling in it: crescents of
        light, a soft pink blush glowing under them, a tiny smile of light (kb_eyes / kb_eyes_<face>, at full light). Every
        mood a friendly one. Short, round sleeves; out of each cuff a soft mitten of light (a little thumb), not long fingers.
      - At its heart a small glowing LOOM (its own part): a gold frame strung with rainbow warp threads, a spindle of light at
        its centre (light 15).
      - Round it, slowly orbiting, the 49 BONDS: tiny glowing motes, each a follower's colour - two tilted rings on their own
        root parts (motes: 25 of them, motesb: 24), centred on the rig at chest height, so the runtime can spin them (a left
        rotation about y on those two displays; nothing hangs from them). Every pose already turns them a little.
      - SIX WINGS of woven light (3.0, the owner's addition): three pairs on its back like a seraph's - the upper rising, a
        short middle pair (inside the motes' inner ring), the lower falling - each a fan of feathers in three lengths, gold and
        rose at the root, violet and blue, green and pale at the tip. Their textures (kb_wing0-2) are ANIMATED strips (16 frames,
        interpolated: pastels flowing over each length of feather); rp must write their .png.mcmeta (mcmeta() / ANIMATED,
        as mire_art's post pass does). Parts wing_ur/ul, wing_mr/ml, wing_lr/ll on the body; every pose sets them (WING_POSE):
        a slow flap through the idles, folded round it sitting, spread in happy and the weave, drooped in the faint.
      Simplified, readable textures: 2-px square cells on 64-px textures (a half unit), no speckle.

MOTION  It hovers (_off y HOVER, a slow bob), the hem's fringe clear of the ground; it glides rather than walks. Sitting, praying
      and fainting set it down kneeling on its robe spread on the floor (the 'pool', shown instead of the skirt).

RIG (rigkit)  body (root: torso, belt, mantle, the robe's upper two tiers), skirt (the lower four tiers, hem and fringe; swings
      on its own joint), head (a model per face; the hood is on it), armr/forer, arml/forel (sleeves, bent at the elbow),
      threadr/threadl (the loose threads off each sleeve's drape), loom (on the chest), motes/motesb (the orbit, roots),
      pool (root; kneeling), web (the weave's spread of threads between its hands - only in the weave poses), and the six
      wings (wing_ur, wing_ul, wing_mr, wing_ml, wing_lr, wing_ll: on the body).
      Design units: the hem at y=0.6 at rest, facing -z, its right is +x. RIG_SCALE 1.0 (16 units a block).

POSE KEYS  _face, _pool (kneeling: the pool shows, the skirt hides), _web (the weave: the web shows), _hide, _off, _o_pool.

FOR THE WIRING  (phase-to-be, like phase236)  A = RF2.art(keeper_art); SWAP = RF2.swapping(...) (= (): only the head's face
      changes); RF2.setup(C, 'head'); FACE = FACE_MAP below; SCALE ~1.0 and HIT (0.9, 2.2) for the host; ENC_POSES from
      'tend_a'/'tend_b'/'bow'; the abilities' poses: weave_up/weave/weave_hold/weave_end (charged: hands spreading threads),
      tug_up/tug (a thread cast at a foe), mend_a/mend (support), gift (kind), rise (getting up from a faint).
      P134.FIT[ITEM] = FIT; P141.DOLL_FROM['doll_keeper'] = (ITEM, DOLL); the wardrobe's recolour textures: LOOK_TEX."""
import colorsys
import math
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg

PREFIX = 'kb_'
RIG_SCALE = 1.0
HOVER = 1.6                                   # (design units off the ground while it floats)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
MOTE_Y = 17.3
# (3.0c: cosier - the robe's tiers 1.6 tall, not 2; the torso 0.8 shorter; a little broader; shorter sleeves and mitten hands:
#  2.4 lower at the belt, 3.2 lower from the shoulders up)
ARM_X = 5.65
PIVOT = {'body': (0, 11.6, 0), 'skirt': (0, 7.6, 0), 'head': (0, 23.6, 0),
         'armr': (ARM_X, 23.0, 0.2), 'forer': (ARM_X, 17.8, 0.2), 'arml': (-ARM_X, 23.0, 0.2), 'forel': (-ARM_X, 17.8, 0.2),
         'threadr': (ARM_X, 10.6, 1.3), 'threadl': (-ARM_X, 10.6, 1.3),
         'loom': (0, 17.4, -3.0), 'motes': (0, MOTE_Y, 0), 'motesb': (0, MOTE_Y, 0), 'pool': (0, 0.0, 0), 'web': (0, 17.3, -9.0),
         # the six wings (3.0 owner's addition): three pairs on its back - upper, middle, lower
         'wing_ur': (2.3, 20.8, 3.3), 'wing_ul': (-2.3, 20.8, 3.3), 'wing_mr': (1.7, 17.4, 2.75), 'wing_ml': (-1.7, 17.4, 2.75),
         'wing_lr': (1.5, 14.2, 2.75), 'wing_ll': (-1.5, 14.2, 2.75)}       # (3.0c: all 3.2 lower, as the head and the motes)
PARENT = {'body': None, 'skirt': 'body', 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'threadr': 'forer', 'threadl': 'forel', 'loom': 'body', 'motes': None, 'motesb': None, 'pool': None, 'web': 'body'}
PARENT.update({w: 'body' for w in ('wing_ur', 'wing_ul', 'wing_mr', 'wing_ml', 'wing_lr', 'wing_ll')})
PARTS = tuple(PIVOT)
PART_K = {}
JOINTS = {}
FACES = ('happy', 'blink', 'sleepy', 'surprised', 'sad', 'focus', 'hurt')
FACE_MAP = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'}
LOOK_TEX = ('kb_robe', 'kb_hood', 'kb_hair')  # (the cream cloth - and the hood down's pearl hair: what a wardrobe recolour tints)
HOOD_PARTS, HOOD_SFX = ('head', 'body'), '_h'  # (3.0d: the hood down - 'Sunlit': these parts' '_h' models; rigpet's FORM)
ITEM, COMPASS = 'bond_thread', 'bond_compass'

# ---- the 49 bonds: every other follower's colour, as phase125.WHO has them (its order: the motes' and the atlas's order)
BONDS = [('emma', '#ff8ad8'), ('celi', '#9ad8ff'), ('zib', '#3ad8c8'), ('cecil', '#b48cff'), ('kw', '#ffe040'), ('leo', '#5ab8e0'),
         ('demo', '#7ad06a'), ('apo', '#3ad06a'), ('tul', '#7ad8ff'), ('frog', '#6ac850'), ('don', '#e8d29a'), ('pearl', '#5ac8ff'),
         ('wil', '#f4f4f4'), ('fishy', '#ffa040'), ('dennis', '#e0a040'), ('pistachio', '#7ae890'), ('omega', '#9fb4ff'), ('ashur', '#ff7a2a'),
         ('chef', '#ffd07a'), ('neighbor', '#7ab8ff'), ('ava', '#6ad8e8'), ('pearlq', '#5ae0d8'), ('bloo', '#5a9ae8'), ('stalker', '#a8ac70'),
         ('lantern', '#ff8a2a'), ('bender', '#e0a860'), ('bones', '#8ab0c8'), ('capshun', '#f0f0f0'), ('kettle', '#8ad8ff'), ('rufus', '#c0392b'),
         ('henry', '#9a9ab8'), ('nia', '#e0a050'), ('gem', '#5ae0a0'), ('batty', '#8a8ad8'), ('eggbert', '#d8d4c0'), ('count', '#a8c8f0'),
         ('dragon', '#5ac048'), ('eraser', '#f08aa0'), ('cursor', '#cfe8ff'), ('inkblot', '#7a7aaa'), ('speech', '#ffd060'), ('lightbringer', '#ffe08a'),
         ('dryad', '#6aa8f0'), ('sovereign', '#d0182e'), ('vexis', '#7aff6a'), ('pxcecil', '#b070ff'), ('pxleo', '#4ab0ff'), ('pxemma', '#ff6ac8'),
         ('sky', '#ffd04a'), ('mireling', '#ff6a1a')]

# ---- the palette (3.0b: friendlier, and mother-of-pearl): pearl cloth with a pastel sheen running over it, gold trim, a soft
#      dusky-rose lining, and a warm round face under the hood - peach skin, rosy cheeks, starlight-lilac hair
CREAM, CREAM_D, CREAM_L = '#f6ece4', '#e6d8d0', '#fcf6f0'     # (the pearl's base: its cloth, the warp line, the paler weft row)
HOODC, HOODC_D = '#f0e6e2', '#e0d0cc'
GOLD, GOLD_D, GOLD_L, GOLD_W = '#e8b648', '#c08a2c', '#ffd878', '#fff2c0'
LINING, LINING_D = '#8a5a78', '#74486a'                       # (deep dusky rose: the hood's inside - shadowy but warm - and the robe's underside)
GLOW_C, GLOW_E, GLOW_D = '#ffd88a', '#f4bc5e', '#e2a04a'       # (the sleeves' insides: warm with the light of the hands)
EYE, EYE_H, EYE_R = '#5a3418', '#fff8e0', '#8a5428'          # (3.0c: on the amber glow) the eyes: warm dark brown, a bright shine, a softer edge
BLUSH, BLUSH_L, SMILE, TEAR = '#ff8ec4', '#ffb8dc', '#7a4422', '#7fc8ff'   # (3.0c) a glowing blush, a tiny smile of light, a tear
HAND, HAND_L = '#ffeec6', '#fff8e4'                           # (the mittens of light)
L_CLOTH, L_BAND, L_FACE, L_EYES, L_CORE, L_THREAD, L_HAND = 7, 9, 12, 15, 15, 12, 8     # (modest cloth; the face's amber glow, its eyes full)
L_WING = (9, 11, 13)                                          # (the wings' three lengths, root to tip)
# (3.0d) THE HOOD DOWN ('Sunlit', a wardrobe costume - the '_h' models of HOOD_PARTS): pearl hair, a sunburst of gold light
HAIR, HAIR_D, HAIR_L = '#f6ecf2', '#e6d8e2', '#fcf4f6'       # (the hair's pearl: inside the cloth's luminance range - see _hair)
RAY = ['#ffc860', '#ffd878', '#ffe8a0', '#ffd070']           # (the rays: warm golds, root ...)
RAY_TIP = ['#fff2c0', '#fffbe8', '#ffffff', '#fff4d0']       # (... to white-gold tips)
L_HAIR, L_RAY, L_RAY_TIP = 8, 13, 15

# ---- the iridescence (3.0b): the pearl cloth, its trim and the wings are ANIMATED strips (FRAMES frames, interpolated); in each
#      frame a pastel sheen (PEARL's tones, round and round) runs diagonally over the cloth, and with time it flows along - a
#      slow mother-of-pearl shimmer. Every frame keeps each cell's luminance (the sheen changes hue, not brightness), so the
#      wardrobe's luminance recolours (phase99._recolour / gild.metal) still come out as clean cloth in the look's colours -
#      with only the soft highlight band (SWEEP) passing over them, the look's own shimmer.
PEARL = ['#ffbcdc', '#ffd0a8', '#fff0a8', '#b8f0d4', '#b4d8ff', '#d4bcff']    # rose, peach, cream, mint, sky, lilac
FRAMES = 16


def _hsv(c):
    r, g, b, *_ = hexc(c)
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def _mix(a, b, t):
    a, b = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def _soft(c, t=0.14):
    """a bond colour as it's woven into the robe: a touch of the cream thread through it, so the rainbow sits in the cloth"""
    return _mix(c, CREAM, t)


# the colour wheel: from gold round through green, blue, violet and rose to amber (the hem's gold closes it)
def _wheel(c):
    h, s, v = _hsv(c)
    return ((h - 0.135) % 1.0, -s)


SPECTRUM = sorted(range(len(BONDS)), key=lambda i: _wheel(BONDS[i][1]))
HEART = 0                                     # (Emma, the first bond: the spindle's colour)
_ROWS = [i for i in SPECTRUM if i != HEART]   # the 48 others, two to a row of the robe
ROBE_Y = [10.8, 9.2, 7.6, 6.0, 4.4, 2.8, 1.2]  # the robe's six tiers, belt to hem (7.6: the skirt's joint; 3.0c: 1.6 each, were 2)


def HIDDEN(p, pose):
    if p == 'pool': return not pose.get('_pool')
    if p == 'skirt': return bool(pose.get('_pool'))
    if p == 'web': return not pose.get('_web')
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    form = HOOD_SFX if pose.get('_h') and p in HOOD_PARTS else ''    # (_h: the hood down - previews; in the game rigpet's FORM)
    return f'{PREFIX}{p}{face}{form}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _cells(fn, cell=2):
    """a 64 px texture painted in square cells half a unit across (fn(cx, cy) -> colour)"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im); n = 64 // cell
    for cy in range(n):
        for cx in range(n):
            c = fn(cx, cy)
            if c is None: continue
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(c) if isinstance(c, str) else c)
    return im


def _inner():
    """the inside of the sleeves: warm with the light of the hands in them"""
    return _cells(lambda x, y: GLOW_E if (x // 2 + y // 2) % 2 else GLOW_D)


def _lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _at_lum(c, L):
    """colour c (rgb) moved to luminance L, keeping its hue as far as it can (what clamps at 255 goes to the other channels)"""
    c = [float(v) for v in c[:3]]
    for _ in range(4):
        d = L - _lum(c)
        if abs(d) < 0.3: break
        free = [i for i in range(3) if (c[i] < 255 if d > 0 else c[i] > 0)]
        if not free: break
        w = sum((0.299, 0.587, 0.114)[i] for i in free)
        for i in free: c[i] = max(0.0, min(255.0, c[i] + d / w * (1 if len(free) < 3 else w)))
    return tuple(int(round(v)) for v in c)


def _sheen_at(t, tints=None):
    """the sheen at t (0..1, round PEARL's tones - or `tints` - and back to the first), smoothly"""
    P_ = tints or PEARL
    n = len(P_); k = (t % 1.0) * n; i = int(k); f = k - i
    f = f * f * (3 - 2 * f)
    return hexc(_mix(P_[i % n], P_[(i + 1) % n], f))


SWEEP = 0.07                                  # (the highlight band's width, as a share of the diagonal; it crosses once a cycle)


def _strip(frame):
    """FRAMES frames of 64 px (frame(f) -> a 64 px image), stacked: an animated strip (its .png.mcmeta: ANIMATED)"""
    im = Image.new('RGBA', (64, 64 * FRAMES))
    for f in range(FRAMES):
        im.paste(frame(f), (0, 64 * f))
    return im


def _pearl(base, line, light=None, phase=0.0, scale=1.8, tints=None, wash=(0.66, 0.3), lum_at=None):
    """mother-of-pearl cloth: the woven grid of before (a warp line every two units, a paler weft row every four) at the
    luminance of `base`/`line`/`light`, washed with a pastel sheen - hue running diagonally over it (scale: how much of the
    round fits across the texture), how much of it varying in soft waves the other way - and flowing along over the frames;
    a pale highlight band sweeps across once a cycle"""
    Lb, Ll, Lh = _lum(hexc(base)), _lum(hexc(line)), _lum(hexc(light or base))
    bc = hexc(base)

    def frame(f):
        tf = f / FRAMES

        def c(x, y):
            L = lum_at(x, y) if lum_at else Ll if x % 4 == 3 else Lh if light and y % 8 == 0 else Lb
            t = (x + y) / 62 * scale + tf + phase
            amt = wash[0] + wash[1] * math.sin(2 * math.pi * ((x - y) / 22 + phase))
            s = _sheen_at(t, tints)
            col = tuple(bc[i] + (s[i] - bc[i]) * amt for i in range(3))
            d = ((x + y) / 62 - tf - phase * 0.5) % 1.0
            if d < SWEEP:                                                     # (the highlight: paler, a touch brighter)
                k = 1 - abs(d / SWEEP * 2 - 1)
                col = tuple(v + (255 - v) * 0.45 * k for v in col); L = L + 7 * k
            return _at_lum(col, L) + (255,)
        return _cells(c)
    return _strip(frame)


GOLDS = ['#e8b648', '#f0b060', '#e8bc58', '#dcc060']          # (the gold's own sheen: yellow, rose, warm, a greenish champagne)


def _gold_at(f, x, y, c):
    """gold tone c in frame f, at cell x, y: tinted toward the gold sheen there (luminance kept), the glint band passing"""
    t = (x + y) / 62 * 0.6 + f / FRAMES
    n = len(GOLDS); k = (t % 1.0) * n; i = int(k)
    g = hexc(_mix(GOLDS[i % n], GOLDS[(i + 1) % n], k - i))
    cc = hexc(c)
    col = tuple(cc[j] + (g[j] - hexc(GOLD)[j]) * 0.8 for j in range(3))
    L = _lum(cc)
    d = ((x + y) / 62 - f / FRAMES) % 1.0
    if d < SWEEP:
        L += 14 * (1 - abs(d / SWEEP * 2 - 1))
    return _at_lum(col, L) + (255,)


def _gold():
    """gold thread: bright, a running diagonal glint, a darker twill - with a slow rose-and-champagne sheen and a glint band
    running over it (animated)"""
    def base(x, y):
        if (x + y) % 8 == 0: return GOLD_W
        if (x - y) % 8 == 4: return GOLD_D
        return GOLD if (x + 2 * y) % 5 else GOLD_L
    return _strip(lambda f: _cells(lambda x, y: _gold_at(f, x, y, base(x, y))))


def _tier(k):
    """one tier of the tapestry: four woven rows (rows 0-3, the top two units), each two bonds' colours - the row's own and,
    every fourth cell (stepped one along each row: a twill), its neighbour on the wheel; below them, cream"""
    rows = [(_soft(BONDS[_ROWS[2 * r]][1]), _soft(BONDS[_ROWS[2 * r + 1]][1])) for r in range(4 * k, 4 * k + 4)]

    def c(x, y):
        if y >= 4: return CREAM
        a, b = rows[y]
        return b if (x + y) % 4 == 0 else a
    return _cells(c)


def _border():
    """the woven border (cuffs, the mantle's edge): a gold row, a row of colour blocks (two cells of a bond, one of gold) going
    round the wheel, a gold row - 1.5 units"""
    order = [BONDS[i][1] for i in SPECTRUM]

    def c(f, x, y):
        if y % 3 != 1: return _gold_at(f, x, y, GOLD if (x + y) % 6 else GOLD_L)
        if x % 3 == 2: return _gold_at(f, x, y, GOLD_D)
        return _soft(order[((x // 3) + 5 * (y // 3)) % len(order)], 0.08)
    return _strip(lambda f: _cells(lambda x, y: c(f, x, y)))


def _rim():
    """the hood's rim and the belt: gold, a row of small colour squares down its middle (the gold shimmering, as _gold's)"""
    order = [BONDS[i][1] for i in SPECTRUM]

    def c(f, x, y):
        if y % 3 == 1 and x % 2 == 0: return _soft(order[(x // 2 + 7 * (y // 3)) % len(order)], 0.05)
        return _gold_at(f, x, y, GOLD if (x + y) % 7 else GOLD_L)
    return _strip(lambda f: _cells(lambda x, y: c(f, x, y)))


def _hair():
    """(the hood down) her hair: mother-of-pearl as the cloth is - the same pastel sheen flowing over it, but stronger, and in
    fine combed strands, not a weave: a pale strand of sheen every third cell, a darker one every seventh. Its luminance stays
    inside the cloth's (HAIR_D..HAIR_L within CREAM_D/HOODC_D..CREAM_L), so a look recolours it with the cloth and the cloth's
    own recolour range is unchanged"""
    Lb, Ls, Ld = _lum(hexc(HAIR)), _lum(hexc(HAIR_L)), _lum(hexc(HAIR_D))
    return _pearl(HAIR, HAIR_D, phase=0.61, scale=2.4, wash=(0.86, 0.14),
                  lum_at=lambda x, y: Ls if x % 3 == 1 else Ld if x % 7 == 0 else Lb)


def _rays(tip=False):
    """the sunburst behind her head (the hood down): warm gold rays (tip: white-gold, their ends) - a slow glint flowing out
    along them, an animated strip like the gold trim's, but all light"""
    cols = RAY_TIP if tip else RAY

    def frame(f):
        def c(x, y):
            k = ((y / 62 * 0.7 - f / FRAMES) % 1.0) * len(cols); i = int(k)
            col = _mix(cols[i % len(cols)], cols[(i + 1) % len(cols)], k - i)
            d = (y / 62 - f / FRAMES) % 1.0
            if d < SWEEP * 1.6: col = _mix(col, '#ffffff', 0.55 * (1 - abs(d / (SWEEP * 1.6) * 2 - 1)))
            return col
        return _cells(c)
    return _strip(frame)


def _atlas():
    """kb_bonds: 8 x 8 swatches (2 units each) - swatch i is bond i (WHO's order): its colour, a paler square at its heart;
    57-59 gold, cream, white light"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [c for _k, c in BONDS] + ['#000000'] * (57 - len(BONDS)) + [GOLD, CREAM, '#fffdf2']
    for i, c in enumerate(cols):
        if i >= len(BONDS) and i < 57: continue
        x0, y0 = (i % 8) * 8, (i // 8) * 8
        d.rectangle((x0, y0, x0 + 7, y0 + 7), fill=hexc(c))
        d.rectangle((x0 + 2, y0 + 2, x0 + 5, y0 + 5), fill=hexc(_mix(c, '#ffffff', 0.5)))
    return im


def swatch(i, inner=False):
    """the uv window of bond i's swatch in kb_bonds (inner: just its pale heart)"""
    u, v = (i % 8) * 2, (i // 8) * 2
    return [u + 0.5, v + 0.5, u + 1.5, v + 1.5] if inner else [u, v, u + 2, v + 2]


GOLD_I, CREAM_I, WHITE_I = 57, 58, 59


# the face (3.0c: cloaked, and cheerful): no face of flesh - the hood's hollow aglow (kb_face: the original's warm amber, stepping
# down to its rim) with the eyes of light in it, smiling: each mood's overlay (kb_eyes / kb_eyes_<face>, at full light) holds the
# eyes, a soft pink blush glowing under each, and a tiny glowing smile. Its window FACE_W x FACE_H px (6.5 x 6 units) from
# the top left; the eyes 5 px wide (its right eye on our left, mirrored for the other), drawn a pixel (a quarter unit) at a time
FACE_W, FACE_H = 26, 24


def _face():
    def c(x, y):
        d = max(abs(x - 6.25) / 6.6, abs(y - 5.5) / 6.1)              # (in 2-px cells: square rings, stepping darker to the rim)
        return GLOW_C if d < 0.6 else GLOW_E if d < 0.86 else GLOW_D      # (3.0c: the original's warm amber glow, not shadow)
    return _cells(c)


EYE_X, EYE_Y = 3, 6                                                  # (its right eye's left column, top row; 3.0c: big eyes, 8 px)
_EYES = {
    None: ['..EEEE..', '.EEEEEE.', 'EEE..EEE', 'EE....EE'],           # cheerful: two big crescents of light, smiling
    'happy': ['...EE...', '..EEEE..', '.EEHHEE.', 'EEE..EEE', 'EE....EE'],     # beaming: ^ ^
    'blink': ['........', 'EE....EE', '.EE..EE.', '..EEEE..'],         # closed, content
    'sleepy': ['........', '........', 'EEEEEEEE', '.EEEEEE.', '..RRRR..'],    # low, drowsy arcs
    'surprised': ['..EEEE..', '.EHHEEE.', 'EEHEEEEE', 'EEEEEEEE', '.EEEEEE.', '..EEEE..'],   # round
    'sad': ['.....EEE', '...EEE..', '.EEE....', 'EE......'],           # drooping arcs (a tear of light below)
    'focus': ['........', 'REEEEEER', '.EEEEEE.', '..RRRR..'],         # flattened - still kindly
    'hurt': ['EEE.....', '..EEE...', '....EEE.', '..EEE...', 'EEE.....'],      # squeezed: > <
}
_BLUSH = [(3, 13, 'B'), (4, 13, 'L'), (5, 13, 'L'), (6, 13, 'B'), (4, 14, 'B'), (5, 14, 'B')]     # (under its right eye; mirrored)
_SMILE = [(11, 16), (14, 16), (12, 17), (13, 17)]
_MOUTH = {
    None: _SMILE,
    'happy': [(10, 15), (15, 15), (11, 16), (12, 16), (13, 16), (14, 16)],
    'blink': _SMILE,
    'sleepy': [(12, 17), (13, 17)],
    'surprised': [(12, 16), (13, 16), (12, 17), (13, 17)],            # a little 'o'
    'sad': [(11, 17), (14, 17), (12, 16), (13, 16)],                  # a small wobble down
    'focus': _SMILE,
    'hurt': [(11, 17), (12, 16), (13, 17), (14, 16)],
}


def _eyes(kind=None):
    """the face's lights (transparent but for them; its element just in front of the hollow, at full light): the eyes, the
    blush and the smile - every mood a friendly one"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    pal = {'E': EYE, 'H': EYE_H, 'R': EYE_R, 'B': BLUSH, 'L': BLUSH_L, 'S': SMILE, 'T': TEAR}
    put = lambda x, y, k: im.putpixel((x, y), hexc(pal[k]))
    for r, row in enumerate(_EYES[kind]):
        n, x0 = len(row), FACE_W - EYE_X - len(row)                 # (its left eye: the right one mirrored - x0 its first column)
        for cx, ch in enumerate(row):
            if ch == '.': continue
            put(EYE_X + cx, EYE_Y + r, ch); put(FACE_W - 1 - EYE_X - cx, EYE_Y + r, 'E' if ch == 'H' else ch)
        for cx, ch in enumerate(row):                               # (3.0c fix: the shine is NOT mirrored - one light, the same side
            if ch == 'H' and row[n - 1 - cx] != '.':                #  of both eyes: at the right eye's own offset within the left)
                put(x0 + cx, EYE_Y + r, 'H')
    for x, y, k in _BLUSH:
        put(x, y, k); put(FACE_W - 1 - x, y, k)
    if kind == 'sad':                                                # (a tear of light under each eye's outer corner)
        for y in (EYE_Y + 4, EYE_Y + 5):
            put(EYE_X, y, 'T'); put(FACE_W - 1 - EYE_X, y, 'T')
    for x, y in _MOUTH[kind]:
        put(x, y, 'S')
    return im


def _hand():
    def c(x, y):
        return HAND_L if 1 <= x % 4 <= 2 and 1 <= y % 4 <= 2 else HAND
    return _cells(c)


def _light():
    def c(x, y):
        return '#ffffff' if (x // 2 + y // 2) % 2 == 0 else '#fff4c8'
    return _cells(c)


# ---- the wings' feathers: woven light, iridescent - three animated strips (FRAMES frames: the pearl's sheen, deeper - each
#      length of feather a run of pastels flowing diagonally over it, a fine sheen every four units, the robe's highlight band
#      sweeping across), root to tip: champagne, peach and rose; rose, lilac and periwinkle; sky, mint and pearl
WING_BANDS = {'kb_wing0': ['#ffd27a', '#ffb89a', '#ffa8cc', '#ffd896'],
              'kb_wing1': ['#ee98d8', '#c4a0ff', '#a0b8ff', '#dca8f6'],
              'kb_wing2': ['#8ccfff', '#94eac4', '#d8fff0', '#b8d4ff']}
WING_FRAMES = FRAMES
ANIMATED = {k: {'animation': {'frametime': 4, 'interpolate': True}} for k in WING_BANDS}     # {texture: its .png.mcmeta}
CLOTH_ANIM = ('kb_robe', 'kb_hood', 'kb_gold', 'kb_rim', 'kb_brd', 'kb_hair', 'kb_ray', 'kb_rayt')   # (the pearl cloth, its gold trim; the hair, the rays)
ANIMATED.update({k: {'animation': {'frametime': 5, 'interpolate': True}} for k in CLOTH_ANIM})


def _wing_strip(cols):
    """one feather texture: FRAMES frames stacked - its colours running diagonally over it and flowing along with the frames
    (interpolated: a slow shimmer), a fine sheen every four units, a pale highlight band crossing once a cycle"""
    n = len(cols)

    def frame(f):
        def c(x, y):
            k = (((x + y) / 62 * 0.5 + f / FRAMES) % 1.0) * n; i = int(k)
            col = hexc(_mix(cols[i % n], cols[(i + 1) % n], k - i))
            if (x + y) % 8 == 0: col = hexc(_mix('#%02x%02x%02x' % col[:3], '#ffffff', 0.35))
            d = ((x + y) / 62 - f / FRAMES) % 1.0
            if d < SWEEP: col = hexc(_mix('#%02x%02x%02x' % col[:3], '#ffffff', 0.4 * (1 - abs(d / SWEEP * 2 - 1))))
            return col[:3] + (255,)
        return _cells(c)
    return _strip(frame)


def mcmeta():
    """(for the rp post pass, as mire_art does it) {path: json} of the animated textures' .png.mcmeta"""
    return {f'assets/bm/textures/block/{k}.png.mcmeta': v for k, v in ANIMATED.items()}


def textures():
    T = {'kb_robe': _pearl(CREAM, CREAM_D, CREAM_L), 'kb_hood': _pearl(HOODC, HOODC_D, phase=0.37, scale=1.5), 'kb_gold': _gold(), 'kb_brd': _border(), 'kb_rim': _rim(),
         'kb_lining': _cells(lambda x, y: LINING_D if (x + y) % 6 == 0 else LINING), 'kb_bonds': _atlas(), 'kb_hand': _hand(), 'kb_light': _light(), 'kb_inner': _inner(),
         'kb_face': _face(), 'kb_eyes': _eyes(), 'kb_hair': _hair(), 'kb_ray': _rays(), 'kb_rayt': _rays(True)}
    for k in range(6):
        T[f'kb_tier{k}'] = _tier(k)
    for k in FACES:
        T[f'kb_eyes_{k}'] = _eyes(k)
    for k, cols in WING_BANDS.items():
        T[k] = _wing_strip(cols)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _faces_but(*drop):
    return tuple(f for f in ('north', 'south', 'east', 'west', 'up', 'down') if f not in drop)


def bx(fr, to, tex, pv, faces=None, ftex=None, light=0, shift=None, uv=None):
    """a box; ftex: {face: texture} for faces in another texture (a tier's gold top, a hood's lining)"""
    e = el(fr, to, tex, pv, faces=faces, light=light, shift=shift, uv=uv)
    for f, t in (ftex or {}).items():
        if f in e['faces']: e['faces'][f]['texture'] = '#' + t
    return e


def paint(e, i, inner=False):
    """an element in one bond's colour: every face from its swatch in kb_bonds"""
    for f in e['faces'].values():
        f['texture'] = '#kb_bonds'; f['uv'] = swatch(i, inner)
    return e


def B(sx, x0, x1, y0, y1, z0, z1, tex, pv, **kw):
    """a box on one side (sx 1: its right, +x; -1: mirrored)"""
    a, b = sorted((sx * x0, sx * x1))
    return bx((a, y0, z0), (b, y1, z1), tex, pv, **kw)


def _robe_w(k):
    """tier k's half width and half depth: a slim robe, flaring to the hem"""
    t = k / 5
    return 4.1 + 2.45 * t ** 1.1, 2.9 + 1.65 * t              # (3.0c: a little broader)


def _tier_el(k, pv):
    y1, y0 = ROBE_Y[k], ROBE_Y[k + 1]
    w, dd = _robe_w(k)
    e = bx((-w, y0, -dd), (w, y1, dd), f'kb_tier{k}', pv, faces=_faces_but('down') if k < 5 else None,
           ftex={'down': 'kb_lining'}, light=L_BAND, shift=(0.13 * k, 0.0))
    e['faces']['up']['uv'] = [0, 0, round(min(16, 2 * w), 3), 0.5]          # (its ledge: the tier's own top row, drawn out - no hard line)
    for f in ('north', 'south', 'east', 'west'):                              # (3.0c: its four woven rows, two units of them, fitted to its 1.6)
        if f in e['faces']: e['faces'][f]['uv'][3] = round(e['faces'][f]['uv'][1] + 2.0, 4)
    return e


def _ring(c, r, n, w, h, tex, pv, light=0):
    """n boxes round a circle (radius r, centre c) in the xy plane - the spindle's whorl"""
    pts = [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n), c[2]) for k in range(n + 1)]
    return [seg(pts[k], pts[k + 1], w, h, tex, pv, FRONT, ext=0.12, light=light) for k in range(n)]


def _strand(pts, w, i, pv, light=L_THREAD):
    """a loose thread down a polyline, in bond i's colour"""
    return [paint(seg(pts[k], pts[k + 1], w, w, 'kb_bonds', pv, FRONT, ext=0.03, light=light), i) for k in range(len(pts) - 1)]


def _motes(ring):
    """the bonds' orbit: ring 0 (25 motes, radius 11, tilted one way), ring 1 (24, radius 13.6, tilted the other); each mote
    a little cube of its follower's colour, at full light, a smaller pale one beside it on every fifth"""
    pv = PIVOT['motes']
    idx = [i for i in range(len(BONDS)) if i % 2 == ring]
    n, r, tilt, ph, s = len(idx), (11.0, 13.6)[ring], (2.6, -3.4)[ring], (0.0, 0.9)[ring], (0.9, 0.75)[ring]
    out = []
    for j, i in enumerate(idx):
        a = 2 * math.pi * j / n
        x, z = r * math.cos(a), r * math.sin(a)
        y = MOTE_Y + tilt * math.sin(a + ph) + 0.8 * math.sin(3 * a)
        out.append(paint(bx((x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), 'kb_bonds', pv, light=15), i))
    return out


# the six wings: (feathers as (elevation degrees above the horizontal, length)) - the upper pair rising, the middle pair short
# (it stays inside the motes' inner ring, which its tips would cross), the lower pair falling; all swept back by WING_SWEEP
WING_SWEEP = 24.0
WING_BACK = {'u': 2.1, 'm': 0.3, 'l': 0.3}           # (how far behind its root each wing's plane stands: the upper clears the hood)
WINGS = {'u': [(75, 10.0), (66, 12.5), (57, 14.5), (48, 15.5), (39, 15.0), (30, 13.5), (22, 11.0)],
         'm': [(20, 5.6), (8, 6.6), (-4, 6.6), (-16, 5.8)],
         'l': [(-26, 8.1), (-36, 9.4), (-46, 9.8), (-56, 9.4), (-66, 7.7)]}      # (3.0c: the lower pair 0.85 as long - the robe is shorter)


def _wing(sx, tier):
    """one wing: a gold covert at its root on the back, then its feathers fanned in one plane (swept back), each in three
    lengths of woven light - gold/rose at the root, violet/blue, green/pale at the tip - narrowing; neighbours a hair apart in
    depth where they overlap"""
    pv = PIVOT[f'wing_{tier}{"r" if sx > 0 else "l"}']
    a = math.radians(WING_SWEEP)
    n = (-sx * math.sin(a), 0.0, math.cos(a))                                  # (the wing's back, away from it)
    def P(u, v, w=0.0):                                                        # (u outward in its plane, v up, w back)
        return (pv[0] + sx * u * math.cos(a) + w * n[0], pv[1] + v, pv[2] + u * math.sin(a) + w * n[2])
    bk = WING_BACK[tier]
    els = [seg(P(-0.4, 0.0, -0.3), P(1.4, 0.0, bk + 0.1), 2.2, 1.0, 'kb_gold', pv, (0.0, 1.0, 0.0), ext=0.0, light=10)]     # (the root, out of its back)
    for k, (e, L) in enumerate(WINGS[tier]):
        c, s_ = math.cos(math.radians(e)), math.sin(math.radians(e))
        lay = 0.36 * (k % 2) + 0.05 + bk + 0.04 * (k // 2)         # (3.0b: and every other one a hair further back - no two in one plane)
        pts = [P(0.9 + c * L * f, s_ * L * f, lay) for f in (0.0, 0.36, 0.7, 1.0)]
        for j, (tex, w, light) in enumerate((('kb_wing0', 2.6, L_WING[0]), ('kb_wing1', 2.2, L_WING[1]), ('kb_wing2', 1.8, L_WING[2]))):
            els.append(seg(pts[j], pts[j + 1], w, 0.34, tex, pv, n, ext=0.0, light=light, shift=(0.17 * k + 0.3 * j, 0.23 * k)))   # (3.0b: end to end - no overlap to z-fight)
    return els


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the robe's two upper tiers, the gold belt and its knot, the torso (cream, a soft warp line), the mantle
    #      over its shoulders (a woven border at its edge), and the glowing hollow at its heart where the loom sits
    pv = PIVOT['body']
    body = [_tier_el(0, pv), _tier_el(1, pv),
            bx((-3.9, 10.6, -2.75), (3.9, 15.2, 2.75), 'kb_robe', pv, faces=_faces_but('down'), light=L_CLOTH, shift=(0.1, 0.2)),         # the waist
            bx((-4.3, 10.7, -3.07), (4.3, 12.1, 3.07), 'kb_rim', pv, faces=_faces_but('down'), ftex={'up': 'kb_gold'}, light=L_BAND),     # the belt
            bx((-0.7, 10.0, -3.3), (0.7, 12.5, -3.07), 'kb_gold', pv, light=L_BAND),                                                          # its knot
            bx((-4.4, 15.2, -2.85), (4.4, 21.4, 2.85), 'kb_robe', pv, faces=_faces_but('down', 'up'), light=L_CLOTH, shift=(0.4, 0.5)),      # the chest
            bx((-2.45, 14.4, -2.95), (2.45, 20.4, -2.87), 'kb_light', pv, faces=('north',), light=L_CORE),                                    # the heart's glow
            bx((-5.25, 20.6, -3.6), (5.25, 21.4, 3.6), 'kb_brd', pv, faces=_faces_but('up'), light=L_BAND),                                # the mantle's border
            bx((-5.1, 21.4, -3.45), (5.1, 23.8, 3.45), 'kb_hood', pv, ftex={'down': 'kb_lining'}, light=L_CLOTH, shift=(0.2, 0.6))]          # the mantle
    part('kb_body', body)
    # (3.0d) the hood down ('Sunlit'): the hood lies bunched round its neck and shoulders - a soft pearl roll, lower at the front
    #      (under the smile), higher at the sides and the back, its dusky lining turned out on top; the hood's gold rim along
    #      the back of it, and its crown hanging a little way down the back, between the wings' roots
    lin = {'up': 'kb_lining'}
    cowl = [bx((-4.0, 23.4, -4.0), (4.0, 24.5, -2.7), 'kb_hood', pv, faces=_faces_but('down', 'south'), ftex=lin, light=L_CLOTH, shift=(0.15, 0.8)),     # the front
            B(1, 3.95, 5.4, 23.4, 25.3, -3.8, 4.2, 'kb_hood', pv, faces=_faces_but('down'), ftex=lin, light=L_CLOTH, shift=(0.55, 0.3)),               # its sides
            B(-1, 3.95, 5.4, 23.4, 25.3, -3.8, 4.2, 'kb_hood', pv, faces=_faces_but('down'), ftex=lin, light=L_CLOTH, shift=(0.75, 0.5)),
            bx((-5.3, 23.4, 3.8), (5.3, 25.9, 5.2), 'kb_hood', pv, faces=_faces_but('down', 'north'), ftex=lin, light=L_CLOTH, shift=(0.35, 0.1)),    # the back
            bx((-4.6, 25.9, 4.6), (4.6, 26.3, 5.3), 'kb_rim', pv, faces=_faces_but('down'), light=L_BAND),                                       # the rim
            bx((-2.3, 22.0, 3.6), (2.3, 23.4, 4.6), 'kb_hood', pv, faces=_faces_but('north', 'up'), light=L_CLOTH, shift=(0.6, 0.6)),             # its crown
            bx((-2.4, 21.7, 3.55), (2.4, 22.0, 4.65), 'kb_gold', pv, faces=_faces_but('north', 'up'), light=L_BAND)]
    part('kb_body' + HOOD_SFX, body + cowl)

    # ---- the skirt: the lower four tiers of the tapestry, the gold hem, and a fringe of loose threads round it - every bond's colour
    pv = PIVOT['skirt']
    sk = [_tier_el(k, pv) for k in range(2, 6)]
    w5, d5 = _robe_w(5)
    sk.append(bx((-w5 - 0.15, 0.8, -d5 - 0.15), (w5 + 0.15, 1.3, d5 + 0.15), 'kb_gold', pv, ftex={'down': 'kb_lining'}, light=L_BAND))   # the hem
    per, k = [], 0
    for side, n in (('n', 13), ('e', 9), ('s', 13), ('w', 9)):                # (the fringe: threads round the hem, a bond each)
        for j in range(n):
            t = (j + 0.5) / n
            if side in 'ns':
                x, z = -w5 + 2 * w5 * t, (-d5 if side == 'n' else d5) + (0.05 if side == 's' else -0.05)
            else:
                x, z = (w5 if side == 'e' else -w5) + (0.05 if side == 'e' else -0.05), -d5 + 2 * d5 * t
            per.append((x, z))
    for j, (x, z) in enumerate(per):
        i = SPECTRUM[(j * 49 // len(per)) % 49]
        L = 1.0 + 0.35 * ((j * 7) % 3)
        sk.append(paint(bx((x - 0.22, 0.85 - L, z - 0.22), (x + 0.22, 0.85, z + 0.22), 'kb_bonds', pv, faces=_faces_but('up'), light=L_THREAD), i, True))
    part('kb_skirt', sk)

    # ---- the pool: the robe spread round it on the floor when it kneels (the tapestry's last tiers, the gold hem at its edge)
    pv = PIVOT['pool']
    part('kb_pool', [bx((-8.2, 0.0, -7.4), (8.2, 0.9, 6.8), 'kb_tier5', pv, faces=_faces_but('down'), ftex={'up': 'kb_robe'}, light=L_BAND),
                     bx((-7.0, 0.9, -6.3), (7.0, 1.8, 5.8), 'kb_tier4', pv, faces=_faces_but('down'), ftex={'up': 'kb_robe'}, light=L_BAND, shift=(0.3, 0)),
                     bx((-5.8, 1.8, -5.2), (5.8, 2.7, 4.8), 'kb_tier3', pv, faces=_faces_but('down'), ftex={'up': 'kb_robe'}, light=L_BAND, shift=(0.6, 0)),
                     bx((-8.35, 0.0, -7.55), (8.35, 0.35, 6.95), 'kb_gold', pv, faces=_faces_but('up', 'down'), light=L_BAND)])

    # ---- the head (3.0c): the hood, cloaked again - its hollow in shadow, the eyes of light smiling in it, a glowing blush;
    #      the opening wide (6.5), gold at the rim, lined inside, rounding over the top to a low soft crown (no point), a short
    #      flap behind. (Its design y's as the 3.0b head's, 3.2 lower: HY.)
    pv = PIVOT['head']; HY = -3.2

    def head(face=None):
        et = 'kb_eyes' if face is None else f'kb_eyes_{face}'
        lin = 'kb_lining'
        F, O, W, BK = -3.9, 3.25, 4.3, 4.3                       # (the hood's front edge, the opening's half width, its outside, back)
        y = lambda v: round(v + HY, 4)
        TOP = y(33.0)
        h = [# the hollow: shadow (unlit, unshaded) a hand's depth in, and the eyes' lights just in front of it
             dict(bx((-O, y(27.0), -2.62), (O, TOP, -2.6), 'kb_face', pv, faces=('north',), uv={'north': [0, 0, 6.5, 6.0]}, light=L_FACE), shade=False),
             dict(bx((-O, y(27.0), -2.68), (O, TOP, -2.66), et, pv, faces=('north',), uv={'north': [0, 0, 6.5, 6.0]}, light=L_EYES), shade=False),
             # the hood: its sides round the hollow, the back, the cap over it, rounding to a low crown
             bx((O, y(26.4), F), (W, TOP, BK), 'kb_hood', pv, faces=_faces_but('down'), ftex={'west': lin}, light=L_CLOTH, shift=(0.5, 0.2)),
             bx((-W, y(26.4), F), (-O, TOP, BK), 'kb_hood', pv, faces=_faces_but('down'), ftex={'east': lin}, light=L_CLOTH, shift=(0.7, 0.2)),
             bx((-O, y(26.4), -2.6), (O, TOP, BK), 'kb_hood', pv, faces=('south',), light=L_CLOTH, shift=(0.3, 0.2)),
             bx((-4.05, TOP, F), (4.05, y(34.5), BK), 'kb_hood', pv, ftex={'down': lin}, light=L_CLOTH, shift=(0.6, 0.1)),
             bx((-3.3, y(34.5), -3.1), (3.3, y(35.3), 3.6), 'kb_hood', pv, faces=_faces_but('down'), light=L_CLOTH, shift=(0.1, 0.7)),
             bx((-2.1, y(35.3), -2.0), (2.1, y(35.8), 2.6), 'kb_hood', pv, faces=_faces_but('down'), light=L_CLOTH, shift=(0.4, 0.4)),
             # its gold rim round the opening, a little proud of the front edge
             bx((O, y(26.4), -4.1), (O + 0.6, y(33.6), F), 'kb_gold', pv, faces=_faces_but('south'), light=L_BAND),
             bx((-O - 0.6, y(26.4), -4.1), (-O, y(33.6), F), 'kb_gold', pv, faces=_faces_but('south'), light=L_BAND),
             bx((-O, TOP, -4.1), (O, y(33.6), F), 'kb_gold', pv, faces=('north', 'up', 'down'), light=L_BAND),
             # a short soft flap down its back
             bx((-1.7, y(30.2), BK), (1.7, y(33.6), 5.0), 'kb_hood', pv, faces=_faces_but('north'), light=L_CLOTH, shift=(0.4, 0.3))]
        return h
    part('kb_head', head())
    for fc in FACES:
        part(f'kb_head_x{fc}', head(fc))

    # ---- (3.0d) the hood down ('Sunlit'): her head revealed - the same glowing face and eyes of light, now the front of a head
    #      whose sides, top and back are her HAIR (pearl, combed back sleek and tight) - a high ponytail gathered at the crown in
    #      a gold band, falling behind; and round it, from behind, a SUNBURST: rays of gold light, long and short by turns, in an
    #      arch over the head and shoulders (none straight up: the ponytail; none below the shoulders: the cowl and the wings)
    RAYC, RAYZ = (0.0, 27.4), 4.0                                # (the sunburst's centre, its plane behind the head)
    RAYS = [(90 + sx * (24 + 16 * k), (8.2, 6.6)[k % 2]) for sx in (1, -1) for k in range(5)]     # (degrees from +x, tip radius)
    RAY_R0 = 4.2

    def head_down(face=None):
        et = 'kb_eyes' if face is None else f'kb_eyes_{face}'
        hr = 'kb_hair'
        h = [dict(bx((-3.25, 23.8, -2.62), (3.25, 29.8, -2.6), 'kb_face', pv, faces=('north',), uv={'north': [0, 0, 6.5, 6.0]}, light=L_FACE), shade=False),
             dict(bx((-3.25, 23.8, -2.68), (3.25, 29.8, -2.66), et, pv, faces=('north',), uv={'north': [0, 0, 6.5, 6.0]}, light=L_EYES), shade=False),
             # the glow behind it (its jaw, under the hair at the sides): the face's own amber rim
             dict(bx((-3.2, 23.8, -2.6), (3.2, 29.8, 3.1), 'kb_face', pv, faces=('east', 'west', 'down'),
                     uv={f: [0, 0, 0.5, 0.5] for f in ('east', 'west', 'down')}, light=L_FACE), shade=False),
             # the hair: combed back over the top (a hairline just proud of the face), the sides from the temples, the back, a low crown
             bx((-3.85, 29.8, -2.95), (3.85, 30.7, 3.7), hr, pv, light=L_HAIR, shift=(0.2, 0.1)),
             B(1, 3.25, 3.85, 24.2, 29.8, -2.75, 3.1, hr, pv, faces=_faces_but('west', 'up'), light=L_HAIR, shift=(0.5, 0.3)),
             B(-1, 3.25, 3.85, 24.2, 29.8, -2.75, 3.1, hr, pv, faces=_faces_but('east', 'up'), light=L_HAIR, shift=(0.7, 0.4)),
             bx((-3.85, 24.0, 3.1), (3.85, 29.8, 3.7), hr, pv, faces=_faces_but('north', 'up'), light=L_HAIR, shift=(0.3, 0.6)),
             bx((-2.9, 30.7, -1.9), (2.9, 31.3, 3.5), hr, pv, faces=_faces_but('down'), light=L_HAIR, shift=(0.6, 0.2)),
             # the ponytail: gathered high at the back of the crown, a gold band round it, then a sleek tail arching back and falling
             bx((-1.0, 30.7, 2.6), (1.0, 31.9, 4.4), hr, pv, faces=_faces_but('down'), light=L_HAIR, shift=(0.1, 0.5)),
             bx((-0.92, 30.9, 4.4), (0.92, 32.3, 5.0), 'kb_gold', pv, light=L_BAND)]
        tail = [(0.0, 31.6, 4.6), (0.0, 31.5, 5.9), (0.0, 29.4, 6.7), (0.0, 26.8, 6.9), (0.0, 24.6, 6.6)]
        for k, (wd, th) in enumerate(((1.6, 1.2), (1.45, 1.1), (1.25, 1.0), (0.95, 0.8))):
            h.append(seg(tail[k], tail[k + 1], th, wd, hr, pv, (1.0, 0.0, 0.0), ext=0.12, light=L_HAIR, shift=(0.3 * k, 0.2 * k)))
        # the sunburst: each ray a root of warm gold and a white-gold tip, end to end, in one plane behind the head
        for a, r1 in RAYS:
            c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
            P_ = lambda r: (RAYC[0] + c * r, RAYC[1] + s_ * r, RAYZ)
            long_ = r1 > 7
            rm = RAY_R0 + (r1 - RAY_R0) * 0.45
            h.append(seg(P_(RAY_R0), P_(rm), 0.9 if long_ else 0.7, 0.3, 'kb_ray', pv, (0.0, 0.0, 1.0), light=L_RAY, shift=(0.1 * a % 1, 0.3)))
            h.append(seg(P_(rm), P_(r1), 0.5 if long_ else 0.4, 0.3, 'kb_rayt', pv, (0.0, 0.0, 1.0), light=L_RAY_TIP, shift=(0.07 * a % 1, 0.6)))
        return h
    part('kb_head' + HOOD_SFX, head_down())
    for fc in FACES:
        part(f'kb_head_x{fc}{HOOD_SFX}', head_down(fc))

    # ---- the arms (3.0c: shorter, rounder sleeves): pearl upper sleeves; a bell from the elbow to a woven cuff, a soft mitten
    #      of light peeping out of it (a little thumb on its inner side), and the sleeve's short drape hanging behind (the loose
    #      threads hang from its tip: threadr / threadl)
    for s, sx in (('r', 1), ('l', -1)):
        ap, fp, tp = PIVOT[f'arm{s}'], PIVOT[f'fore{s}'], PIVOT[f'thread{s}']
        cx = ARM_X
        part(f'kb_arm{s}', [B(sx, cx - 1.35, cx + 1.35, 17.6, 23.0, -1.35, 1.75, 'kb_robe', ap, light=L_CLOTH, shift=(0.3 + 0.2 * sx, 0.4))])
        fore = [B(sx, cx - 1.45, cx + 1.45, 15.4, 17.9, -1.45, 1.85, 'kb_robe', fp, faces=_faces_but('up'), light=L_CLOTH, shift=(0.6, 0.2)),
                B(sx, cx - 1.9, cx + 1.9, 13.6, 15.4, -1.9, 2.3, 'kb_robe', fp, faces=_faces_but('up'), ftex={'down': 'kb_inner'}, light=L_CLOTH, shift=(0.2, 0.7)),
                B(sx, cx - 2.0, cx + 2.0, 12.6, 13.6, -2.0, 2.4, 'kb_brd', fp, ftex={'down': 'kb_inner', 'up': 'kb_gold'}, light=L_BAND),  # the cuff
                B(sx, cx - 1.7, cx + 1.7, 11.0, 12.6, 0.45, 2.3, 'kb_robe', fp, faces=_faces_but('up'), light=L_CLOTH, shift=(0.8, 0.4)),       # the drape
                B(sx, cx - 1.8, cx + 1.8, 10.6, 11.2, 0.35, 2.4, 'kb_brd', fp, faces=_faces_but('up'), light=L_BAND, shift=(0.5, 0)),
                # the mitten of light: round and soft, just out of the cuff; a little thumb; its rounded tip
                B(sx, cx - 0.95, cx + 0.95, 11.3, 12.9, -1.55, 0.25, 'kb_hand', fp, faces=_faces_but('up'), light=L_HAND),
                B(sx, cx - 1.3, cx - 0.95, 11.9, 12.6, -1.35, -0.55, 'kb_hand', fp, faces=_faces_but('east' if sx > 0 else 'west'), light=L_HAND),
                B(sx, cx - 0.7, cx + 0.7, 11.0, 11.3, -1.3, 0.0, 'kb_hand', fp, faces=_faces_but('up'), light=L_HAND)]
        part(f'kb_fore{s}', fore)
        # the loose threads: five, from the drape's tip, drifting apart as they fall
        th = []
        X, Y, Z = tp
        for j, (dx, dz, L, bend) in enumerate(((-1.1, -0.3, 3.4, 0.7), (-0.5, 0.4, 4.4, -0.6), (0.1, -0.2, 3.8, 0.9), (0.7, 0.5, 4.8, -0.8), (1.2, 0.0, 3.0, 0.5))):
            i = SPECTRUM[(j * 10 + (0 if sx > 0 else 5)) % 49]
            x0, z0 = X + sx * dx, Z + dz
            pts = [(x0, Y + 0.1, z0), (x0 + sx * bend * 0.4, Y - L * 0.5, z0 + 0.3), (x0 + sx * bend, Y - L, z0 + 0.8)]
            th += _strand(pts, 0.28, i, tp)
            th.append(paint(bx((pts[-1][0] - 0.35, pts[-1][1] - 0.7, pts[-1][2] - 0.35), (pts[-1][0] + 0.35, pts[-1][1], pts[-1][2] + 0.35),
                               'kb_bonds', tp, light=15), i))                                                        # (a bead of light at its end)
        part(f'kb_thread{s}', th)

    # ---- the loom at its heart: a little gold frame strung with rainbow warp threads, a beam at the top and the foot, and in
    #      the middle a spindle of light, wound with the first bond's thread
    pv = PIVOT['loom']; X, Y, Z = pv
    lm = [bx((X - 2.6, Y - 2.9, Z - 0.7), (X - 2.0, Y + 2.9, Z + 0.1), 'kb_gold', pv, light=L_BAND),      # (3.0b: their backs 0.05 off the
          bx((X + 2.0, Y - 2.9, Z - 0.7), (X + 2.6, Y + 2.9, Z + 0.1), 'kb_gold', pv, light=L_BAND),      #  beams': no z-fighting)
          bx((X - 2.9, Y + 2.3, Z - 0.8), (X + 2.9, Y + 2.95, Z + 0.15), 'kb_gold', pv, light=L_BAND),
          bx((X - 2.9, Y - 2.95, Z - 0.8), (X + 2.9, Y - 2.3, Z + 0.15), 'kb_gold', pv, light=L_BAND)]
    for j in range(6):                                                         # (the warp: six threads, six bonds)
        x = X - 1.6 + 0.64 * j
        lm.append(paint(bx((x - 0.13, Y - 2.2, Z - 0.35), (x + 0.13, Y + 2.2, Z - 0.1), 'kb_bonds', pv, light=L_THREAD), SPECTRUM[j * 8 + 3], True))
    # the spindle: a shaft of light, a whorl, the wound thread swelling at its middle
    lm += [bx((X - 0.2, Y - 2.3, Z - 1.25), (X + 0.2, Y + 2.3, Z - 0.85), 'kb_light', pv, light=L_CORE),
           paint(bx((X - 0.65, Y - 1.1, Z - 1.5), (X + 0.65, Y + 1.1, Z - 0.65), 'kb_bonds', pv, light=L_CORE), HEART),
           paint(bx((X - 1.0, Y - 0.55, Z - 1.7), (X + 1.0, Y + 0.55, Z - 0.55), 'kb_bonds', pv, light=L_CORE), HEART, True),
           bx((X - 1.1, Y - 1.9, Z - 1.4), (X + 1.1, Y - 1.5, Z - 0.75), 'kb_gold', pv, light=L_CORE)]
    part('kb_loom', lm)

    # ---- the bonds' orbit (two rings, roots: the runtime may spin them)
    part('kb_motes', _motes(0)); part('kb_motesb', _motes(1))
    for tier in 'uml':
        part(f'kb_wing_{tier}r', _wing(1, tier)); part(f'kb_wing_{tier}l', _wing(-1, tier))

    # ---- the web: the weave's spread of threads between its hands - rainbow wefts across gold warps, at full glow
    pv = PIVOT['web']; X, Y, Z = pv
    wb = []
    for j in range(7):                                                         # (the wefts: seven rows across, the wheel's colours)
        y = Y - 4.5 + 1.5 * j
        wb.append(paint(bx((X - 10.5, y - 0.18, Z - 0.1), (X + 10.5, y + 0.18, Z + 0.1), 'kb_bonds', pv, light=15), SPECTRUM[j * 7 + 2], True))
    for j in range(8):                                                         # (the warps: gold, between them)
        x = X - 9.1 + 2.6 * j
        wb.append(bx((x - 0.14, Y - 5.4, Z - 0.16), (x + 0.14, Y + 5.4, Z + 0.16), 'kb_gold', pv, light=15))
    for j in range(5):                                                         # (and motes caught in it)
        x, y = X - 7.0 + 3.5 * j, Y - 3.0 + 1.5 * ((j * 3) % 5)
        wb.append(paint(bx((x - 0.4, y - 0.4, Z - 0.4), (x + 0.4, y + 0.4, Z + 0.4), 'kb_bonds', pv, light=15), SPECTRUM[j * 10 + 5]))
    part('kb_web', wb)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit: ('x', -a) swings a hanging limb forward by a; ('x', +a) on the body or head leans/nods it forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


def orbit(a, b=None):
    """the two rings turned a and b degrees about y (the second turns the other way by default)"""
    return dict(motes=qs(('y', a)), motesb=qs(('y', -a * 0.75 if b is None else b)))


def drift(r, l=None, side=0.0):
    """the loose threads swung back (r: degrees, ahead if negative) and out a little"""
    l = r if l is None else l
    return dict(threadr=qs(('x', r), ('z', -side)), threadl=qs(('x', l), ('z', side)))


s = math.sin
REST = dict(armr=limb(1, 6, 7), forer=limb(1, 22, 0, -6), arml=limb(-1, 6, 7), forel=limb(-1, 22, 0, -6))
POSES = {
    # floating at rest, hands low before it, its head a little bowed, the threads hanging still
    'idle_a': P(_off=(0, HOVER, 0), **REST, head=qs(('x', 6)), **drift(6, 4), **orbit(0)),
    # looking up, its right hand raised palm-up as if a mote had settled in it; the threads drift
    'idle_b': P(_off=(0, HOVER + 0.5, 0), armr=limb(1, 34, 14, -10), forer=limb(1, 62, 0, -30), arml=limb(-1, 6, 8), forel=limb(-1, 24, 0, -6),
                head=qs(('x', -10), ('y', 10)), body=qs(('x', -2)), **drift(-14, 8, 6), **orbit(120)),
    # a quiet moment: eyes closed, both hands drawn up to the loom at its heart, tending it
    'idle_c': P(_face='blink', _off=(0, HOVER - 0.2, 0), armr=limb(1, 36, 10), forer=limb(1, 70, 0, 15), arml=limb(-1, 36, 10), forel=limb(-1, 70, 0, 15),
                head=qs(('x', 14)), body=qs(('x', 3)), **drift(-20, -20, -4), **orbit(240)),
    # gliding: no steps - a slow bob, the skirt and the threads trailing
    **{f'walk_{i}': P(_off=(0, HOVER + 0.4 + 0.35 * s(math.pi * i / 2), 0), body=qs(('x', 4), ('z', 1.5 * s(math.pi * i / 2))), skirt=qs(('x', -8)),
                      armr=limb(1, 4 - 8 * s(math.pi * i / 2), 9), forer=limb(1, 20), arml=limb(-1, 4 + 8 * s(math.pi * i / 2), 9), forel=limb(-1, 20),
                      head=qs(('x', 2)), **drift(24 + 6 * s(math.pi * i / 2), 24 - 6 * s(math.pi * i / 2), 4), **orbit(20 * i))
      for i in range(4)},
    # gliding fast: leaning into it, the arms drawn back, everything streaming behind
    **{f'run_{i}': P(_off=(0, HOVER + 2.0 + (0.4, 0.8, 0.4, 0.0)[i], 0), body=qs(('x', 16)), head=qs(('x', -12)), skirt=qs(('x', -22)),
                     armr=limb(1, 2, 20), forer=limb(1, 16), arml=limb(-1, 2, 20), forel=limb(-1, 16),
                     **drift(32 + (0, 6, 0, -6)[i], 32 - (0, 6, 0, -6)[i], 8), **orbit(15 * i))
      for i in range(4)},
    'jump': P(_face='happy', _off=(0, HOVER + 4.0, 0), armr=limb(1, 20, 40), forer=limb(1, 20), arml=limb(-1, 20, 40), forel=limb(-1, 20),
              skirt=qs(('x', 6)), head=qs(('x', -8)), **drift(-10, -10, 10), **orbit(40)),
    # sitting: kneeling back on its robe spread on the floor, hands folded in its lap
    'sit_a': P(_pool=True, _off=(0, -6.8, 0), body=qs(('x', 2)), armr=limb(1, 26, 10, -4), forer=limb(1, 56, 0, 22), arml=limb(-1, 26, 10, -4), forel=limb(-1, 56, 0, 22),
               head=qs(('x', 8), ('z', 4)), **drift(-30, -30), **orbit(60)),
    # (the seated idle's other beat) looking up at the motes going round, a hand lifted to one, smiling
    'sit_b': P(_pool=True, _face='happy', _off=(0, -6.8, 0), body=qs(('x', -4)), armr=limb(1, 60, 18, -10), forer=limb(1, 40, 0, -20),
               arml=limb(-1, 26, 10, -4), forel=limb(-1, 56, 0, 22), head=qs(('x', -14), ('y', 5), ('z', -4)), **drift(-10, -30, 6), **orbit(180)),
    'happy': P(_face='happy', _off=(0, HOVER + 1.0, 0), armr=limb(1, 22, 40), forer=limb(1, 24, 0, -20), arml=limb(-1, 22, 40), forel=limb(-1, 24, 0, -20),
               head=qs(('z', 8), ('x', -6)), body=qs(('x', -3)), **drift(-6, -6, 12), **orbit(90)),
    # struck: rocked back, the sleeves flung
    'hurt': P(_face='hurt', _off=(0, HOVER - 0.4, 0.6), body=qs(('x', -12)), head=qs(('x', -12), ('z', 6)), skirt=qs(('x', 8)),
              armr=limb(1, 30, 30), forer=limb(1, 30), arml=limb(-1, 30, 30), forel=limb(-1, 30), **drift(-24, -24, 10), **orbit(-20)),
    # fainted: sunk to the floor on its robe, slumped forward, the hood bowed, the hands fallen in its lap
    'tired': P(_pool=True, _face='blink', _off=(0, -7.6, 0), body=qs(('x', 22)), head=qs(('x', 22), ('z', -6)),
               armr=limb(1, 4, 16), forer=limb(1, 24), arml=limb(-1, 10, 16), forel=limb(-1, 28), **drift(-80, -80, 30), **orbit(10)),
    # getting up again: straightening on its knees, one hand pressed to the floor, the other to the loom
    'rise': P(_pool=True, _face='sleepy', _off=(0, -4.6, 0), body=qs(('x', 10)), head=qs(('x', 4)),
              armr=limb(1, 24, 16), forer=limb(1, 6), arml=limb(-1, 36, 10), forel=limb(-1, 70, 0, 15), **drift(-50, -20), **orbit(30)),
    # THE WEAVE (charged): its hands brought together before the loom, gathering the threads ...
    'weave_up': P(_face='focus', _off=(0, HOVER + 0.4, 0), body=qs(('x', 6)), head=qs(('x', 10)),
                  armr=limb(1, 44, 10), forer=limb(1, 52, 0, 18), arml=limb(-1, 44, 10), forel=limb(-1, 52, 0, 18), **drift(-30, -30, -6), **orbit(60)),
    # ... then spread wide, and the threads stream out between them: the web of every bond hangs in the air before it
    'weave': P(_web=True, _face='happy', _off=(0, HOVER + 1.4, 0), body=qs(('x', -6)), head=qs(('x', -8)),
               armr=limb(1, 40, 68), forer=limb(1, 20, 0, -40), arml=limb(-1, 40, 68), forel=limb(-1, 20, 0, -40), skirt=qs(('x', 6)),
               **drift(-40, -40, 30), **orbit(150)),
    # (holding it: the web taut, its arms a little lower)
    'weave_hold': P(_web=True, _face='focus', _off=(0, HOVER + 1.0, 0), body=qs(('x', -3)), head=qs(('x', 2)),
                    armr=limb(1, 36, 62), forer=limb(1, 18, 0, -40), arml=limb(-1, 36, 62), forel=limb(-1, 18, 0, -40), **drift(-30, -30, 24), **orbit(210)),
    # (letting it go: the hands sweeping down and round, the web gone into the foes)
    'weave_end': P(_face='blink', _off=(0, HOVER + 0.4, 0), body=qs(('x', 4)), head=qs(('x', 8)),
                   armr=limb(1, 18, 30), forer=limb(1, 20), arml=limb(-1, 18, 30), forel=limb(-1, 20), **drift(20, 20, 14), **orbit(260)),
    # A THREAD CAST at a foe: drawn back ... and flung forward, the threads streaming out ahead
    'tug_up': P(_face='focus', _off=(0, HOVER + 0.4, 0), body=qs(('y', 18), ('x', -2)), head=qs(('y', -14)),
                armr=limb(1, -24, 20), forer=limb(1, 40), arml=limb(-1, 20, 16), forel=limb(-1, 40, 0, 20), **drift(30, 0), **orbit(30)),
    'tug': P(_face='focus', _off=(0, HOVER + 0.2, -0.6), body=qs(('y', -16), ('x', 8)), head=qs(('y', 12), ('x', -6)),
             armr=limb(1, 92, 6), forer=limb(1, 6), arml=limb(-1, -10, 18), forel=limb(-1, 24), **drift(-96, 20, 0), **orbit(70)),
    # MENDING (support): its hands cupped at its heart ... then opened toward you, a glowing thread offered
    'mend_a': P(_face='blink', _off=(0, HOVER, 0), head=qs(('x', 12)), body=qs(('x', 4)),
                armr=limb(1, 36, 10), forer=limb(1, 70, 0, 15), arml=limb(-1, 36, 10), forel=limb(-1, 70, 0, 15), **drift(-20, -20, -4), **orbit(90)),
    'mend': P(_face='happy', _off=(0, HOVER + 0.6, -0.4), body=qs(('x', 8)), head=qs(('x', 4)),
              armr=limb(1, 66, 12, -6), forer=limb(1, 20, 0, -30), arml=limb(-1, 66, 12, -6), forel=limb(-1, 20, 0, -30), **drift(-70, -70, 6), **orbit(130)),
    # A GIFT (out of a fight): a deep, slow bow, both hands open low before it
    'gift': P(_face='happy', _off=(0, HOVER, -0.6), body=qs(('x', 22)), head=qs(('x', 12)),
              armr=limb(1, 40, 10, -6), forer=limb(1, 30, 0, -20), arml=limb(-1, 40, 10, -6), forel=limb(-1, 30, 0, -20), skirt=qs(('x', -14)),
              **drift(-30, -30, 4), **orbit(160)),
    # BY ITS LOOM (the sanctuary; the encounter): working the great loom, its hands forward, one beat and the next
    'tend_a': P(_off=(0, HOVER, 0), body=qs(('x', 6)), head=qs(('x', 14), ('y', -8)),
                armr=limb(1, 52, 10, -6), forer=limb(1, 30, 0, 10), arml=limb(-1, 40, 10, -6), forel=limb(-1, 44, 0, 20), **drift(-40, -30), **orbit(40)),
    'tend_b': P(_off=(0, HOVER + 0.3, 0), body=qs(('x', 6)), head=qs(('x', 14), ('y', 8)),
                armr=limb(1, 40, 10, -6), forer=limb(1, 44, 0, 20), arml=limb(-1, 52, 10, -6), forel=limb(-1, 30, 0, 10), **drift(-30, -40), **orbit(80)),
    # a greeting: a gentle bow, a hand at its heart
    'bow': P(_face='blink', _off=(0, HOVER, 0), body=qs(('x', 16)), head=qs(('x', 14)), skirt=qs(('x', -10)),
             armr=limb(1, 36, 10), forer=limb(1, 70, 0, 15), arml=limb(-1, 6, 10), forel=limb(-1, 20), **drift(-10, 10), **orbit(20)),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                  # (gliding through the water: laid forward, a slow sweep of the sleeves)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, 6.0 + 0.4 * s(2 * _p), 0), body=qs(('x', 66)), head=qs(('x', -12)), skirt=qs(('x', -10)),
                            armr=limb(1, 110 + 24 * s(_p), 40 + 16 * math.cos(_p)), forer=limb(1, 16),
                            arml=limb(-1, 110 + 24 * s(_p), 40 + 16 * math.cos(_p)), forel=limb(-1, 16),
                            **drift(70 + 10 * s(_p), 70 - 10 * s(_p), 6), **orbit(10 * _i))
def wings(raise_=0.0, spread=0.0, fold=0.0, droop=0.0, beat=0.0):
    """the six wings' turns at their roots: raise_ lifts every wing up and out (negative lowers it), spread fans the three pairs
    apart (the upper higher, the lower lower), fold sweeps them further back (negative: forward, round it), droop lets them fall
    (the upper most), beat lifts the upper pair and lowers the lower (a flap's two beats)"""
    out = {}
    for t, (sp, dr, bt) in (('u', (0.3, 1.0, 1.0)), ('m', (0.0, 0.7, 0.4)), ('l', (-1.0, 0.4, -0.6))):
        r = raise_ + spread * sp - droop * dr + beat * bt
        for side, sx in (('r', 1), ('l', -1)):
            out[f'wing_{t}{side}'] = qs(('y', fold * sx), ('z', -r * sx))
    return out


# each pose's wings: a slow gentle flap through the idles, swept back when it glides fast, folded softly round it sitting,
# spread wide when it's happy and when it weaves, drooped when it faints
WING_POSE = {'idle_a': dict(), 'idle_b': dict(beat=6, raise_=2), 'idle_c': dict(beat=-6, fold=6),
             'walk_0': dict(beat=4), 'walk_1': dict(beat=10), 'walk_2': dict(beat=4), 'walk_3': dict(beat=-4),
             'run_0': dict(fold=20, beat=4), 'run_1': dict(fold=20, beat=10), 'run_2': dict(fold=20, beat=2), 'run_3': dict(fold=20, beat=-2),
             'jump': dict(spread=12, fold=-10, beat=6), 'sit_a': dict(fold=-14, spread=-22), 'sit_b': dict(fold=-10, spread=-28, beat=2),
             'happy': dict(spread=14, fold=-16, beat=2), 'hurt': dict(fold=18, beat=10, spread=-16), 'tired': dict(droop=24, fold=10, spread=-24), 'rise': dict(droop=10, beat=8),
             'weave_up': dict(fold=10, beat=-8), 'weave': dict(spread=16, fold=-8, beat=2), 'weave_hold': dict(spread=14, fold=-10, beat=0),
             'weave_end': dict(beat=-6, fold=6), 'tug_up': dict(fold=10, beat=8), 'tug': dict(fold=-6, beat=-6), 'mend_a': dict(fold=-6),
             'mend': dict(spread=8, fold=-10, beat=4), 'gift': dict(fold=-12, droop=6), 'tend_a': dict(beat=3), 'tend_b': dict(beat=-3),
             'bow': dict(fold=-10, droop=6)}
for _k, _v in POSES.items():
    _v.update(wings(**WING_POSE.get(_k, dict(fold=30, spread=-8, beat=-10 + 4 * math.sin(int(_k[-1]) if _k[-1].isdigit() else 0)))))   # (swimming: laid back)
for _k, _v in POSES.items():                                   # (kneeling: the pool stays on the floor however low it sinks)
    if _v.get('_pool'): _v['_o_pool'] = (0.0, -_v['_off'][1], 0.0)

DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'run_2', 'jump', 'swim_0', 'swim_2', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired', 'rise',
         'weave_up', 'weave', 'weave_hold', 'weave_end', 'tug_up', 'tug', 'mend_a', 'mend', 'gift', 'tend_a', 'tend_b', 'bow']

# ---- the display case and the doll (measured from the built rig with tools/preview/keeper.py 'fit'; phase134.FIT's form:
#      (lowest y, height, x0, x1, z0, z1) in blocks, idle_a at RIG_SCALE)
FIT = (0.047, 2.144, -0.873, 0.867, -0.872, 0.872)     # (the width is the outer ring of motes; 3.0c: re-measured - 0.2 shorter)
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, 'groups': {'bm:kb_skirt': 'legs'}}     # (no legs: the skirt is shortened as legs would be)


# ---------------------------------------------------------------------------------------------------- icons
def icon_bond_thread():
    """the Thread of Bonds: a spool of golden thread wound in bands of the bonds' colours - gold-capped flanges, a loose gold
    thread curling off it to a bead of light - 16 x 16 in sprites280's kit, lit from the top left"""
    from sprites280 import S, GOLD as G
    from sprites299 import strings
    s = S()
    for y0, sh in ((1, 0), (13, -1)):                                   # the flanges: gold rims, the top one catching the light
        s.g(['.GGGGGGGGGGG.', 'GgggggggggggG'] if y0 == 1 else ['GgggggggggggG', '.GGGGGGGGGGG.'],
            {'G': G[2 + sh], 'g': G[4 + sh]}, 1, y0)
    bands = [('#ff6a9a', '#ffb0c8', '#c03a6a'), ('#ff9a2a', '#ffc880', '#c0640a'), ('#ffe040', '#fff4a0', '#c0a010'),
             ('#58d060', '#a8f0a0', '#2a8a30'), ('#40b8ff', '#a0e0ff', '#1a70c0'), ('#9a6aff', '#d0b8ff', '#5a2ac0'),
             ('#ffd0e8', '#fff4fa', '#d090b0'), ('#e8b648', '#fff0b0', '#a07018'), ('#ff6a9a', '#ffb0c8', '#c03a6a'), ('#ffe040', '#fff4a0', '#c0a010')]
    for k, y in enumerate(range(3, 13)):                               # the thread wound round it, a band to a row
        mid, hi, lo = bands[k]
        for x in range(2, 13):
            s.px(x, y, hi if x <= 3 else lo if x >= 11 else mid)
        if k % 2: s.px(7 + (k % 3), y, hi)                             # (a glint of the twist)
    for x, y, c in ((13, 9, G[3]), (14, 8, G[4]), (14, 7, G[3]), (14, 6, G[4])): s.px(x, y, c)      # the loose end, off its side ...
    im = s.render()
    return strings(im, [(15, 5, '#fffbe0'), (15, 4, G[4])])                                        # ... to a bead of light


def icon_bond_compass():
    """the Compass of Bonds: a gold compass, its face pale cream, its needle a woven rainbow thread pointing up and right,
    a gold bead at its pivot - 16 x 16"""
    from sprites280 import S, GOLD as G
    s = S()
    s.ring(8.0, 8.5, 7.0, 7.0, 1.9, G, light=(-0.6, -0.8))
    FACE_ = ['#d8ccaa', '#efe6cc', '#fffbee']
    for y in range(16):
        for x in range(16):
            d = math.hypot(x + 0.5 - 8.0, y + 0.5 - 8.5)
            if d < 5.15: s.px(x, y, FACE_[2] if x + y < 12 else FACE_[1] if x + y < 19 else FACE_[0])
    for x, y in ((8, 4), (12, 8), (3, 8), (8, 12)): s.px(x, y, G[1])       # the four marks
    s.g(['.G.', 'GgG'], {'G': G[2], 'g': G[4]}, 7, 0)                       # the bow at its top
    # the needle: a woven thread two pixels wide, lower left to upper right, round the colour wheel; its tip bright
    cols = ['#7a4ad8', '#3a8ae8', '#2ab0c8', '#3ab848', '#e8c020', '#f08a20', '#e8487a']
    for k, (x, y) in enumerate(((4, 12), (5, 11), (6, 10), (8, 8), (9, 7), (10, 6), (11, 5))):
        s.px(x, y, cols[k]); s.px(x + 1, y, cols[k]) if k < 6 else None
    s.px(12, 4, '#ff9ab8'); s.px(12, 5, cols[6])
    s.px(7, 9, G[4]); s.px(8, 9, G[3]); s.px(7, 8, G[3])                   # the pivot: a gold bead
    return s.render()


ICONS = {ITEM: icon_bond_thread, COMPASS: icon_bond_compass}
