"""THE DIVINE ONE (draft art): the god the Lightbringer and Aurel served. He is never fought and never follows: He appears ONCE, in
the cinematic at the Dread Sovereign's defeat (the bottom of the Undercrown, phase238's fall), and eradicates what His first herald
became. He has to read at a glance as divine, vast and overwhelming beside the Sovereign - a colossus of light twice its height.

THE LOOK - a robed figure of light, hooded, faceless, hovering.
  - THE ROBE: radiant ivory silk in deep pleats (every panel a facet turned to the light, so the folds read in light and shadow),
    stitched with SEAMS OF GOLD that glow: down the pleats, round the hem, a broad embroidered orphrey (gold, a lattice of
    white-gold suns) down the front from the throat to the dissolving hem. A gold girdle at the waist with a sun-gem clasp.
    A cope over the shoulders and back, its gold-banded edges meeting at a great MORSE on the breast: a sunburst round a core
    of pure light (the brightest thing on Him after His face).
  - BELOW THE WAIST THE ROBE DISSOLVES INTO LIGHT: its lower tier brightens to white-gold, then frays into ribbons of light that
    fade out (translucent, lit), motes falling below them; inside the skirt, a floor of light - from beneath (where a player
    stands) He is lit from within. He HOVERS: nothing of Him comes near the ground.
  - THE HEAD: a deep hood, its lining in warm shadow, and in it a FACE OF PURE LIGHT - no features, only a radiant oval with a
    white core (never a cartoon face). A glowing gold frame round the hood's opening, a sun-gem on the brow. Faces (_face):
        default  the radiant visage
        blaze    the light flaring out of the hood in rays (raise, smite)
        veiled   a veil of translucent silk over it, the light showing through (descend)
  - THE HALO: three concentric rings standing behind His head, each its own part so they can turn independently - halo_a the
    inner ring of gold set with studs of light, halo_b the middle ring of white light set with eight diamonds, halo_c the outer
    ring and its SUNBURST of rays (long and short). _halo 'dim' hides the sunburst (He arrives dimmed and blazes in the reveal).
  - LONG BELL SLEEVES with glowing gold cuffs, the cloth over each shoulder; the HANDS ARE LIGHT (open, the fingers apart),
    each in a faint aura. The right hand is its own part (handr) so it can be raised to smite.
  - FOUR WINGS OF FEATHERED LIGHT (not the Sovereign's six black membranes): a great upper pair and a lower pair, each a
    leading edge of glowing gold, two rows of coverts and long white flight feathers whose gold tips burn (lit, unshaded).
    One model per wing - opened, raised, folded back only by turning at the root, so every pose interpolates.
  Palette: ivory/white silk, pale shadows of warm grey-gold in the folds, gold and white-gold light. No other colour.

SCALE   BOSS_SCALE 6.8 (RIG_SCALE the same - there is no follower): the hood's tip ~26 blocks over the floor (the root hovers
        HOVER design units up: the ribbons' ends ~0.5 above the floor), the halo's rays to ~31, the wingspan ~38 blocks open
        (~5 folded). The Sovereign is ~11 to its crown (true form ~14): it comes up to His breast. scale_of(pose) gives the
        scale; PART_K the parts built bigger than the model box (the wings 2.2, the beam 3), shown at k x the scale (rigfol /
        rigkit do this). Every element stays inside -16..32 and every uv inside 0..16 (models() asserts / clamps it).

THE RIG (rigkit; one item_display per part - 18):
  body     the root: hips, the gold girdle
  skirt    the robe below the hips: pleats, the dissolving tier, the ribbons and motes of light, the light within
  chest    torso, the cope (back), the morse and its core of light, the orphrey
  head     the hood and the face of light (a model per face)
  halo_a / halo_b / halo_c    the three rings (on the chest, behind the head) - spun about their own z by the poses
  armr / arml    upper sleeve and the cloth over the shoulder
  forer / forel  the bell sleeve and its gold cuff
  handr / handl  the hands of light
  w1r / w1l / w2r / w2l    the upper (great) and lower wings, rooted in the back
  fx       on the right hand, shown only when a pose asks (_fx): 'gather' (an orb of light gathering in the palm, rays round
           it) or 'beam' (the smiting beam: a column of light ~25 blocks long out of the hand along the fingers - in 'smite' it
           comes down through a Sovereign standing ~20 blocks before Him)
Not a rig part: PILLAR (model dvn_pillar) - a vertical pillar of light for the cinematic to drop on the Sovereign where the beam
strikes (its foot at the model's joint; show it at scale BOSS_SCALE * PILLAR_K: ~39 blocks tall, a white core ~2 across in
sheaths of light ~5.6 across, rings up it, a flare ~17 across on the ground). An extra item_display when it's used.
Design units: the ribbons' ends at y~-5.5 (the root lifted HOVER), facing -z, His right is +x. PIVOT is the rig's joints; the
parts from the waist up are built round BP and stand RISE higher in PIVOT (a long robe) - the models don't see the difference.

POSES (BOSS_POSES[name]; each a full rig pose - every part named - and every one hovering):
  descend  arriving from above: the head bowed, the arms folded before the breast (the hands in the sleeves), the wings folded
           back and down like a mantle, veiled, the halo dimmed (no sunburst)
  reveal   the wings and arms opening wide, the head lifting, the veil gone, the halo ablaze
  gaze     looking down at the Sovereign: leaning over it, the head tilted down, wings open
  raise    the right hand raised high, light gathering in it (fx gather), the face blazing, the wings lifted
  smite    the hand thrust down and forward at it, the beam on (fx beam), the wings swept forward
  rest     after: arms lowered, calm, the head a little bowed, the wings eased down
  ascend   rising away: lifted higher, the head up, the arms out and down, palms down, the wings raised for the beat
SEQUENCE: the order and the ticks to reach each, for the cinematic. Consecutive poses never turn a joint more than 150 deg and
the halo's spin steps are 20-50 deg (so the game's slerp turns them the right way, and on); between(a, b) (rigkit.mid) gives an
in-between key where a long chain (the raised arm) should keep to its arc. Model swaps ride the keys: the face (veiled ->
default -> blaze -> default), the sunburst (hidden in descend), the fx (gather in raise, beam in smite)."""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import qs, el, shrink, D, qrot

PREFIX = 'dvn_'
BOSS_SCALE = 6.8
RIG_SCALE = BOSS_SCALE                         # (no follower: one scale)
HOVER = 7.0                                    # (design units: the root lifted this far in every pose - the ribbons' ends clear the floor)
PILLAR_K = 4.0
HEAD_K = 0.88                                  # (the head built, then made this much smaller about the neck)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

BP = {'body': (0, 22.0, 0), 'skirt': (0, 15.0, 0), 'chest': (0, 24.0, 0), 'head': (0, 36.6, -0.4),
         'halo_a': (0, 43.6, 9.6), 'halo_b': (0, 43.6, 10.3), 'halo_c': (0, 43.6, 11.0),
         'armr': (8.2, 34.2, 0), 'forer': (9.0, 26.8, 0), 'handr': (9.2, 19.4, -0.2),
         'arml': (-8.2, 34.2, 0), 'forel': (-9.0, 26.8, 0), 'handl': (-9.2, 19.4, -0.2),
         'w1r': (3.4, 33.0, 4.9), 'w2r': (3.0, 28.4, 5.6), 'w1l': (-3.4, 33.0, 4.9), 'w2l': (-3.0, 28.4, 5.6),
         'fx': (9.2, 15.0, -0.2)}
RISE = 5.0                                     # (the parts from the waist up are built at BP and stand RISE higher: a long robe)
UPPER = ('chest', 'head', 'halo_a', 'halo_b', 'halo_c', 'armr', 'forer', 'handr', 'arml', 'forel', 'handl', 'w1r', 'w2r', 'w1l', 'w2l', 'fx')
PIVOT = {p: (x, y + (RISE if p in UPPER else 0.0), z) for p, (x, y, z) in BP.items()}
PARENT = {'body': None, 'skirt': 'body', 'chest': 'body', 'head': 'chest', 'halo_a': 'chest', 'halo_b': 'chest', 'halo_c': 'chest',
          'armr': 'chest', 'forer': 'armr', 'handr': 'forer', 'arml': 'chest', 'forel': 'arml', 'handl': 'forel',
          'w1r': 'chest', 'w2r': 'chest', 'w1l': 'chest', 'w2l': 'chest', 'fx': 'handr'}
PARTS = tuple(PIVOT)
WINGS = ('w1r', 'w2r', 'w1l', 'w2l')
HALOS = ('halo_a', 'halo_b', 'halo_c')
PART_K = {'fx': 3.0, **{w: 2.2 for w in WINGS}}       # (built at full size, kept inside the model box)
FACES = ('blaze', 'veiled')
FX = ('gather', 'beam')

# ivory silk, its fold shadows (warm grey-gold), gold, white-gold light
IVORY, IVORY_L, IVORY_D, IVORY_S = (244, 238, 224), (255, 253, 246), (212, 200, 176), (178, 162, 132)
GOLD, GOLD_L, GOLD_W, GOLD_D = (234, 184, 58), (255, 222, 118), (255, 245, 200), (170, 116, 28)
LIGHT, WHITE = (255, 250, 232), (255, 255, 255)
HOOD, HOOD_D = (150, 110, 58), (98, 68, 34)
FEATH, FEATH_D, FEATH_S = (248, 246, 240), (226, 221, 230), (196, 189, 206)


# ---------------------------------------------------------------------------------------------------- names
def face_of(pose):
    f = pose.get('_face')
    return f if f in FACES else None


def HIDDEN(p, pose):
    if p == 'fx': return not pose.get('_fx')
    if p == 'halo_c' and pose.get('_halo') == 'dim': return True
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    if p == 'head':
        f = face_of(pose)
        return f'{PREFIX}head{"_x" + f if f else ""}{suffix}'
    if p == 'fx':
        return f'{PREFIX}fx_{pose.get("_fx", "gather")}{suffix}'
    return f'{PREFIX}{p}{suffix}'


def scale_of(pose):
    return BOSS_SCALE


# ---------------------------------------------------------------------------------------------------- textures (2 px cells: half a design unit)
def _c(col, k=1.0, add=0, a=255):
    return tuple(max(0, min(255, int(v * k + add))) for v in col[:3]) + (a,)


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _paint(fn, seed, size=64, cz=2):
    """a texture painted in square cells: fn(cx, cy, rnd) -> an RGB or RGBA tuple (cx, cy in cells, 0..31)"""
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im)
    for cy in range(size // cz):
        for cx in range(size // cz):
            c = fn(cx, cy, rnd); c = c if len(c) == 4 else tuple(c) + (255,)
            d.rectangle((cx * cz, cy * cz, cx * cz + cz - 1, cy * cz + cz - 1), fill=tuple(max(0, min(255, int(v))) for v in c))
    return im


def _robe(seed, k=1.0):
    """ivory silk in long folds: a lit crest, the body of the fold, a shaded crease (8 cells a fold), faint streaks down it"""
    prof = [IVORY_L, IVORY_L, IVORY, IVORY, IVORY, _mix(IVORY, IVORY_D, 0.45), IVORY_D, _mix(IVORY_D, IVORY_S, 0.5)]
    def c(x, y, r):
        b = prof[(x + (y // 11) % 2) % 8]
        b = _mix(b, IVORY_L, 0.35) if r.random() < 0.08 else b
        return _c(b, k * (1 + r.uniform(-0.025, 0.025)))
    return _paint(c, seed)


def _robe_lo(seed):
    """the robe's lower tier, brightening as it goes down (v: the full height of the panel) into white-gold light"""
    prof = [IVORY_L, IVORY, IVORY, IVORY, _mix(IVORY, IVORY_D, 0.4), IVORY_D, IVORY, IVORY_L]
    def c(x, y, r):
        t = y / 31
        b = _mix(prof[x % 8], LIGHT, min(1.0, t * 1.25))
        if t > 0.55 and r.random() < 0.25 * t: b = _mix(b, GOLD_L, 0.5)
        if t > 0.7 and r.random() < 0.18: b = WHITE
        return _c(b)
    return _paint(c, seed)


def _fade(seed):
    """a ribbon of light (v: its length): white-gold at the root, fading out to nothing at its end, sparks in it"""
    def c(x, y, r):
        t = y / 31
        b = _mix(LIGHT, GOLD_L, 0.25 + 0.4 * t) if r.random() > 0.15 else WHITE
        a = 236 if t < 0.25 else int(236 - (t - 0.25) / 0.75 * 210)
        if r.random() < 0.06: b, a = WHITE, max(a, 200)
        if x in (0, 31): a = int(a * 0.6)
        return _c(b, a=max(24, a))
    return _paint(c, seed)


def _gold(seed):
    def c(x, y, r):
        if (x + y) % 7 == 0: return _c(GOLD_W)
        if (x - y) % 9 == 0: return _c(GOLD_D)
        return _c(r.choice((GOLD, GOLD, GOLD, GOLD_L, _mix(GOLD, GOLD_D, 0.4))))
    return _paint(c, seed)


def _seam(seed):
    """a glowing gold seam: bright gold, white-hot flecks"""
    return _paint(lambda x, y, r: _c(WHITE if r.random() < 0.12 else r.choice((GOLD_L, GOLD_L, GOLD_W, GOLD))), seed)


def _emb(seed):
    """the orphrey's embroidery: deep gold, a lattice of white-gold suns (a diamond every 4 cells), dark gold stitching between"""
    def c(x, y, r):
        dx, dy = (x % 4) - 1.5, (y % 4) - 1.5
        m = abs(dx) + abs(dy)
        if m <= 1.0: return _c(GOLD_W if (x // 4 + y // 4) % 2 else WHITE)
        if m <= 2.0: return _c(GOLD_L)
        if m >= 2.9: return _c(GOLD_D)
        return _c(GOLD, 1 + r.uniform(-0.05, 0.05))
    return _paint(c, seed)


def _light(seed, base=LIGHT, hi=WHITE, gold=0.12):
    return _paint(lambda x, y, r: _c(hi if r.random() < 0.3 else (_mix(base, GOLD_L, 0.6) if r.random() < gold else base)), seed)


def _aura(seed, a=70):
    return _paint(lambda x, y, r: _c(_mix(LIGHT, GOLD_L, r.uniform(0, 0.5)), a=a + r.randint(-14, 14)), seed)


def _hood_in(seed):
    """the hood's lining: warm shadow, darker deeper in"""
    return _paint(lambda x, y, r: _c(_mix(HOOD_D, HOOD, r.uniform(0.2, 1.0))), seed)


def _face(kind=None):
    """the face of pure light (whole uv, 64 px): no features - a radiant oval, a white core, white-gold, gold at its rim, the
    hood's warm shadow round it. blaze: brighter and wider, rays of light out of the core"""
    N = 32; rnd = random.Random(61)
    def c(x, y, r):
        dx, dy = (x + 0.5 - N / 2) / (N / 2), (y + 0.5 - N / 2 + 1) / (N / 2)
        q = math.sqrt((dx / (0.82 if kind != 'blaze' else 0.96)) ** 2 + (dy / 0.96) ** 2)
        if kind == 'blaze':
            ang = math.atan2(dy, dx); ray = 0.5 + 0.5 * math.cos(ang * 8)
            q = q * (1 - 0.18 * ray)
        if q < 0.32: return _c(WHITE)
        if q < 0.55: return _c(_mix(WHITE, LIGHT, (q - 0.32) / 0.23))
        if q < 0.78: return _c(_mix(LIGHT, GOLD_L, (q - 0.55) / 0.23))
        if q < 0.98: return _c(_mix(GOLD_L, GOLD, (q - 0.78) / 0.2))
        return _c(_mix(GOLD_D, HOOD, min(1.0, (q - 0.98) * 2.5)))
    return _paint(c, 61 if kind is None else 62, size=64, cz=2)


def _veil(seed):
    """translucent silk: pale, a gold edge, the light behind it showing through"""
    def c(x, y, r):
        if y >= 29: return _c(GOLD_L, a=230)
        return _c(_mix(IVORY_L, IVORY, r.uniform(0, 0.5)), a=150 if x % 6 else 175)
    return _paint(c, seed)


def _feather(dark=False):
    """a flight feather (whole uv, the length down v): the white vane in barbs slanting off a gold-white shaft, its edges shaded
    (so feathers side by side read apart), the root tucked in shadow"""
    base = FEATH_D if dark else FEATH; edge = FEATH_S if dark else FEATH_D
    def c(x, y, r):
        if x in (15, 16): return _c(_mix(GOLD_L, WHITE, 0.4))
        if x <= 1 or x >= 30: return _c(edge)
        side = x < 15
        if (y + (x if side else 31 - x) // 2) % 5 == 0: return _c(_mix(base, edge, 0.6))
        b = base if r.random() > 0.15 else _mix(base, WHITE, 0.6)
        if y < 4: b = _mix(b, edge, 0.6)
        return _c(b)
    return _paint(c, 81 if not dark else 82)


def _ftip(seed):
    """a feather's burning tip: gold running to white-gold light, the shaft white"""
    def c(x, y, r):
        if x in (15, 16): return _c(WHITE)
        t = y / 31
        return _c(_mix(GOLD, GOLD_W, t)) if r.random() > 0.15 else _c(WHITE)
    return _paint(c, seed)


def _covert(seed, dark=False):
    """the coverts: small rounded feathers in rows, each lit along its top and shaded at its foot"""
    base = FEATH_D if dark else FEATH
    def c(x, y, r):
        sx = (x + (y // 4 % 2) * 2) % 4
        if y % 4 == 3: return _c(_mix(base, FEATH_S, 0.7) if sx else base)
        if y % 4 == 0 and sx in (1, 2): return _c(_mix(WHITE, GOLD_L, 0.3))
        return _c(base if r.random() > 0.2 else WHITE)
    return _paint(c, seed)


def _gem(seed):
    """a sun-diamond: white facets, pale gold and a touch of sky in them, a white sparkle"""
    def c(x, y, r):
        if (x + y) % 6 == 0: return _c(WHITE)
        if (x - y) % 6 == 0: return _c((226, 236, 255))
        return _c(r.choice((GOLD_W, LIGHT, GOLD_L, WHITE)))
    return _paint(c, seed)


def textures():
    T = {'dvn_robe': _robe(5101), 'dvn_robe_d': _robe(5102, 0.86), 'dvn_robe_lo': _robe_lo(5103), 'dvn_fade': _fade(5104),
         'dvn_gold': _gold(5105), 'dvn_seam': _seam(5106), 'dvn_emb': _emb(5107), 'dvn_light': _light(5108),
         'dvn_light_g': _light(5109, GOLD_W, WHITE, 0.4), 'dvn_aura': _aura(5110), 'dvn_aura_g': _aura(5111, 120),
         'dvn_hood_in': _hood_in(5112), 'dvn_face': _face(), 'dvn_face_blaze': _face('blaze'), 'dvn_veil': _veil(5113),
         'dvn_feather': _feather(), 'dvn_feather_d': _feather(True), 'dvn_ftip': _ftip(5114),
         'dvn_covert': _covert(5115), 'dvn_covert_d': _covert(5116, True), 'dvn_gem': _gem(5117),
         'dvn_halo': _paint(lambda x, y, r: _c(r.choice((GOLD_L, GOLD_W, GOLD_W, GOLD))), 5118),
         'dvn_halo_w': _light(5119, GOLD_W, WHITE, 0.2)}
    return T


# ---------------------------------------------------------------------------------------------------- building helpers
NOSHIFT = {'dvn_face', 'dvn_face_blaze', 'dvn_feather', 'dvn_feather_d', 'dvn_ftip', 'dvn_fade', 'dvn_robe_lo', 'dvn_veil'}
_rs = random.Random(9)
_PV = [None]


def E(fr, to, tex, pv=None, light=0, shade=True, **kw):
    """an element (rigkit.el), its texture window shifted at random so neighbouring boxes don't repeat the same patch; shade
    False: drawn as lit as it's painted (light itself - the face, the hands' auras, the halo, the beam)"""
    pv = pv or _PV[0]
    if tex not in NOSHIFT and 'shift' not in kw and 'uv' not in kw: kw['shift'] = (_rs.random(), _rs.random())
    e = el(fr, to, tex, pv, light=light, **kw)
    if not shade: e['shade'] = False
    return e


def BX(sx, x0, x1, y0, y1, z0, z1, tex, pv=None, **kw):
    """a box on side sx (+1 His right, -1 His left): x given for the right side, mirrored"""
    a, b = sorted((sx * x0, sx * x1))
    return E((a, y0, z0), (b, y1, z1), tex, pv, **kw)


def SEG(A, B, w, h, tex, pv=None, up=UP, ext=0.0, light=0, shade=True, uv=None, faces=None):
    """a box w (across) by h (toward `up`) from A to B (rigkit.seg, with uvs and shade): its 'up' face is the broad one facing
    `up`, its uv's v running from A to B"""
    pv = pv or _PV[0]
    S = lambda a, b: tuple(a[i] - b[i] for i in range(3))
    x, y, z = rigkit.frame(S(B, A), up)
    L = math.sqrt(sum(v * v for v in S(B, A))) / 2 + ext; m = tuple((A[i] + B[i]) / 2 for i in range(3))
    ang = rigkit.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    fr, to = (m[0] - w / 2, m[1] - h / 2, m[2] - L), (m[0] + w / 2, m[1] + h / 2, m[2] + L)
    kw = {}
    if uv is None and tex not in NOSHIFT: kw['shift'] = (_rs.random(), _rs.random())
    return E(fr, to, tex, pv, light=light, shade=shade, uv=uv, faces=faces,
             rot=None if max(abs(v) for v in ang) < 1e-3 else (ang, m), **kw)


def FULL(w=16, h=16):
    """the whole texture down a SEG's length on its broad faces (the 'down' face flipped so it runs the same way)"""
    w = min(16, w)
    return {'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0], 'east': [0, 0, 2, 16], 'west': [0, 0, 2, 16], 'north': [0, 0, 16, 2], 'south': [0, 0, 16, 2]}


def PANELS(c, y0, y1, r0, r1, n, tex, pv=None, zk=1.0, h=0.5, a0=0.0, a1=360.0, pleat=0.0, wk=1.14, light=0, shade=True, uv=None,
           out=0.0):
    """a ring of panels round an upright axis at c (x, z) - a cone from radius r0 at y0 to r1 at y1, squashed front to back by zk:
    the robe's skirt, a sleeve's bell, a cope. Every panel is a facet turned its own way (the folds read by the light), the
    alternate ones stood in or out by `pleat` (deep pleats); a=0 is His front (-z), a=90 His right"""
    P = []
    for k in range(n):
        a = math.radians(a0 + (a1 - a0) * (k + 0.5) / n); sa, ca = math.sin(a), math.cos(a)
        pk = 1 + (pleat if k % 2 else -pleat)
        top = (c[0] + r0 * pk * sa, y0, c[1] - r0 * pk * ca * zk)
        bot = (c[0] + r1 * pk * sa, y1, c[1] - r1 * pk * ca * zk)
        nrm = (zk * sa, 0.0, -ca); nn = math.hypot(nrm[0], nrm[2]); nrm = (nrm[0] / nn, out, nrm[2] / nn)
        w = r1 * math.sqrt(ca * ca + (zk * sa) ** 2) * math.radians(a1 - a0) / n * wk
        P.append(SEG(top, bot, min(w, 16.0), h, tex, pv, nrm, light=light, shade=shade, uv=uv))
    return P


def SEAMS(c, y0, y1, r0, r1, angles, pv=None, zk=1.0, w=0.32, dr=0.3):
    """glowing gold seams down a PANELS cone, at these angles (deg)"""
    S = []
    for ad in angles:
        a = math.radians(ad); sa, ca = math.sin(a), math.cos(a)
        top = (c[0] + (r0 + dr) * sa, y0, c[1] - (r0 + dr) * ca * zk); bot = (c[0] + (r1 + dr) * sa, y1, c[1] - (r1 + dr) * ca * zk)
        S.append(SEG(top, bot, w, 0.2, 'dvn_seam', pv, (zk * sa, 0, -ca), light=15, shade=False))
    return S


def GEM(c, s, tex, pv=None, light=15, rot=(35.26, 45.0, 0.0), shade=True):
    """a cube stood on its point (a diamond)"""
    return E((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, pv, light=light, rot=(rot, c), shade=shade)


def RING(c, r, n, w, h, tex, pv=None, light=15, shade=False, start=0.0):
    """an upright ring (a halo) of n boxes round c, in the xy plane: w its radial thickness, h its depth"""
    pts = [(c[0] + r * math.cos(start + 2 * math.pi * k / n), c[1] + r * math.sin(start + 2 * math.pi * k / n), c[2]) for k in range(n + 1)]
    return [SEG(pts[k], pts[k + 1], w, h, tex, pv, FRONT, ext=0.12 * r / n * 2, light=light, shade=shade) for k in range(n)]


# ---------------------------------------------------------------------------------------------------- the parts
def _body():
    """the hips under the girdle: pleats, the girdle of gold, its sun-gem clasp"""
    pv = BP['body']; B = []
    B.append(E((-5.2, 15.6, -3.4), (5.2, 28.8, 3.4), 'dvn_robe_d'))
    B += PANELS((0, 0), 28.6, 15.2, 5.9, 6.9, 14, 'dvn_robe', zk=0.72, pleat=0.025)
    B += PANELS((0, 0), 29.4, 27.4, 6.35, 6.5, 14, 'dvn_gold', zk=0.72, h=0.6, light=12, wk=1.18)
    B += PANELS((0, 0), 27.55, 27.25, 6.6, 6.6, 14, 'dvn_seam', zk=0.72, h=0.3, light=15, shade=False, wk=1.18)
    B += [GEM((0, 28.4, -5.2), 1.7, 'dvn_gem', rot=(0.0, 0.0, 45.0)),
          E((-1.5, 27.2, -5.1), (1.5, 29.6, -4.6), 'dvn_gold', light=12)]
    B.append(SEG((0, 27.2, -4.75), (0, 16.6, -5.05), 2.8, 0.3, 'dvn_emb', pv, FRONT, light=10))          # (the orphrey on down)
    for sx in (1, -1):
        B.append(SEG((sx * 1.4, 27.2, -4.9), (sx * 1.4, 16.6, -5.2), 0.3, 0.2, 'dvn_seam', pv, FRONT, light=15, shade=False))
    return B


def _skirt():
    """the robe below the hips: deep pleats with gold seams down them, the front orphrey, a gold hem - then the lower tier
    brightening into light, ribbons of light fraying off it and fading, motes below; inside, a floor of light"""
    pv = BP['skirt']; S = []; zk = 0.74
    S += PANELS((0, 0), 16.6, 8.6, 6.8, 9.6, 16, 'dvn_robe', zk=zk, pleat=0.035, h=0.6)
    S += SEAMS((0, 0), 16.4, 8.8, 6.8, 9.6, (45, 90, 135, 180, 225, 270, 315), zk=zk)
    S += PANELS((0, 0), 9.0, 8.1, 9.75, 9.85, 16, 'dvn_seam', zk=zk, h=0.35, light=15, shade=False, wk=1.2)      # (the hem)
    S += PANELS((0, 0), 8.4, 3.0, 9.5, 10.9, 16, 'dvn_robe_lo', zk=zk, pleat=0.03, h=0.5, light=12, uv=FULL())
    rnd = random.Random(808)
    for k in range(22):                                       # (the ribbons of light: fraying off the lower tier, fading out)
        a = math.radians(360 * (k + 0.5) / 22 + rnd.uniform(-4, 4)); sa, ca = math.sin(a), math.cos(a)
        r0, r1 = 10.7, 11.2 + rnd.uniform(-0.4, 1.0); y1 = rnd.uniform(-5.4, -0.6)
        top = (r0 * sa, 3.6, -r0 * ca * zk); bot = (r1 * sa, y1, -r1 * ca * zk)
        S.append(SEG(top, bot, rnd.uniform(1.4, 2.6), 0.3, 'dvn_fade', pv, (zk * sa, 0, -ca), light=15, shade=False, uv=FULL()))
    for k in range(9):                                        # (and inside them, nearer the middle, more - so it's light right through)
        a = math.radians(360 * k / 9 + 20); r = 6.2
        top = (r * math.sin(a), 5.0, -r * math.cos(a) * zk); bot = (r * 1.05 * math.sin(a), rnd.uniform(-4.6, -1.5), -r * 1.05 * math.cos(a) * zk)
        S.append(SEG(top, bot, 2.4, 0.3, 'dvn_fade', pv, (math.sin(a), 0, -math.cos(a)), light=15, shade=False, uv=FULL()))
    for k in range(16):                                       # (motes falling off it)
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(3.0, 11.5); y = rnd.uniform(-6.6, -1.6); s = rnd.uniform(0.45, 0.9)
        S.append(E((r * math.sin(a) - s / 2, y - s / 2, -r * math.cos(a) * zk - s / 2), (r * math.sin(a) + s / 2, y + s / 2, -r * math.cos(a) * zk + s / 2),
                   'dvn_light', light=15, shade=False))
    S += [E((-9.0, 5.6, -5.4), (9.0, 6.0, 5.4), 'dvn_light', light=15, shade=False, faces=('up', 'down')),         # (the light within)
          E((-6.4, 5.6, -7.4), (6.4, 6.0, 7.4), 'dvn_light', light=15, shade=False, faces=('up', 'down'))]
    # the front orphrey (gold embroidery, glowing seams either side), down the front panel
    for (y0, r0, y1, r1, w) in ((16.6, 6.8, 8.6, 9.6, 3.0), (8.6, 9.6, 3.4, 10.9, 3.4)):
        A, B = (0, y0, -r0 * zk - 0.45), (0, y1, -r1 * zk - 0.45)
        S.append(SEG(A, B, w, 0.3, 'dvn_emb', pv, FRONT, light=10))
        for sx in (1, -1):
            S.append(SEG((sx * w / 2, A[1], A[2] - 0.12), (sx * w / 2, B[1], B[2] - 0.12), 0.35, 0.2, 'dvn_seam', pv, FRONT, light=15, shade=False))
    return S


def _chest():
    """the torso (faceted, a little wider at the shoulders), the cope over the back, its gold-banded edges meeting at the morse
    on the breast - a sunburst round a core of pure light - and the orphrey down from it to the girdle"""
    pv = BP['chest']; C = []; zk = 0.64
    C += PANELS((0, 0), 35.6, 23.2, 7.0, 6.2, 12, 'dvn_robe', zk=zk, h=0.6)
    C.append(E((-6.4, 34.4, -4.0), (6.4, 35.8, 4.0), 'dvn_robe'))
    C += PANELS((0, 0.6), 37.6, 25.4, 5.6, 10.4, 9, 'dvn_robe', zk=0.66, a0=104, a1=256, pleat=0.03, h=0.6)          # (the cope)
    C += PANELS((0, 0.6), 25.9, 25.1, 10.4, 10.5, 9, 'dvn_seam', zk=0.66, a0=104, a1=256, h=0.3, light=15, shade=False, wk=1.2)
    C += SEAMS((0, 0.6), 37.4, 25.6, 5.6, 10.4, (140, 180, 220), zk=0.66)
    # the morse: a sunburst of gold rays round a core of light, its aura
    m = (0, 30.8, -4.9)
    C += [GEM((m[0], m[1], m[2] - 0.5), 2.4, 'dvn_light', shade=False, rot=(0.0, 0.0, 45.0)),
          GEM((m[0], m[1], m[2] - 0.9), 1.4, 'dvn_gem', rot=(0.0, 0.0, 45.0)),
          E((m[0] - 2.4, m[1] - 2.4, m[2] - 0.2), (m[0] + 2.4, m[1] + 2.4, m[2] + 0.3), 'dvn_gold', light=12)]
    C += RING((m[0], m[1], m[2] - 0.35), 2.6, 12, 0.5, 0.5, 'dvn_halo', light=15)
    for k in range(12):
        a = 2 * math.pi * k / 12 + math.pi / 12; L = 5.2 if k % 2 else 3.8
        C.append(SEG((m[0] + 2.9 * math.cos(a), m[1] + 2.9 * math.sin(a), m[2] - 0.3), (m[0] + L * math.cos(a), m[1] + L * math.sin(a), m[2] - 0.2),
                     0.55, 0.3, 'dvn_halo', pv, FRONT, light=15, shade=False))
    C.append(E((m[0] - 3.4, m[1] - 3.4, m[2] - 1.6), (m[0] + 3.4, m[1] + 3.4, m[2] - 0.7), 'dvn_aura', light=15, shade=False))
    # the cope's edges (gold bands) from the shoulders to the morse; the orphrey from the morse to the girdle
    for sx in (1, -1):
        A, B = (sx * 6.0, 36.4, -2.4), (sx * 2.0, 31.6, -4.8)
        C.append(SEG(A, B, 2.0, 0.4, 'dvn_emb', pv, (sx * 0.3, 0.2, -1.0), light=10))
        C.append(SEG((A[0] + sx * 1.0, A[1], A[2] - 0.1), (B[0] + sx * 1.0, B[1], B[2] - 0.15), 0.3, 0.2, 'dvn_seam', pv, (sx * 0.3, 0.2, -1.0), light=15, shade=False))
    C.append(SEG((0, 27.4, -4.55), (0, 23.4, -4.25), 2.8, 0.3, 'dvn_emb', pv, FRONT, light=10))
    for sx in (1, -1):
        C.append(SEG((sx * 1.4, 27.4, -4.7), (sx * 1.4, 23.4, -4.4), 0.3, 0.2, 'dvn_seam', pv, FRONT, light=15, shade=False))
    return C


def _head(face=None):
    """the hood (a tall pointed cowl in folds, a gothic arch for its opening, rolled at the rim, its lining in warm shadow,
    draping onto the shoulders) and in its hollow the face of pure light; a glowing gold seam round the arch, a sun-gem at
    its peak"""
    pv = BP['head']; H = []; c = (0, 0.8)
    H += PANELS(c, 49.6, 44.2, 0.9, 4.5, 9, 'dvn_robe', zk=0.95, h=0.6, wk=0.9)                     # (the peak)
    H += PANELS(c, 44.6, 35.4, 4.5, 5.9, 12, 'dvn_robe', zk=0.95, a0=42, a1=318, pleat=0.03, h=0.6)  # (the sides and back)
    H += PANELS(c, 44.4, 36.0, 3.9, 5.2, 10, 'dvn_hood_in', zk=0.95, a0=46, a1=314, h=0.3)          # (the lining)
    H += PANELS(c, 46.4, 44.0, 0.8, 3.9, 8, 'dvn_hood_in', zk=0.95, h=0.3, wk=0.9)
    H.append(E((-3.6, 35.4, -1.0), (3.6, 44.6, 3.8), 'dvn_hood_in'))
    # the rolled rim round the opening: a pointed arch, gold-seamed
    arch = [(-4.0, 35.2, -3.9), (-3.9, 40.0, -4.1), (-3.3, 43.4, -4.3), (-1.8, 45.4, -4.4), (0.0, 46.6, -4.5),
            (1.8, 45.4, -4.4), (3.3, 43.4, -4.3), (3.9, 40.0, -4.1), (4.0, 35.2, -3.9)]
    for a, b in zip(arch, arch[1:]):
        H.append(SEG(a, b, 1.3, 1.0, 'dvn_robe', pv, FRONT, ext=0.35))
        H.append(SEG((a[0] * 0.86, a[1] - 0.1, a[2] - 0.55), (b[0] * 0.86, b[1] - 0.1, b[2] - 0.55), 0.32, 0.2, 'dvn_seam', pv, FRONT, ext=0.15, light=15, shade=False))
    # the cowl: the hood's folds lying on the shoulders round the throat
    H += PANELS((0, 0.4), 37.4, 33.6, 5.2, 7.8, 12, 'dvn_robe', zk=0.84, pleat=0.04, h=0.6, out=0.25)
    H += PANELS((0, 0.4), 34.1, 33.3, 7.8, 7.9, 12, 'dvn_seam', zk=0.84, h=0.3, light=15, shade=False, wk=1.2, out=0.25)
    # the face of light: a radiant oval deep in the hollow, a brighter core standing out of it, its glow filling the opening
    ft = 'dvn_face_blaze' if face == 'blaze' else 'dvn_face'
    H.append(E((-3.4, 35.6, -1.6), (3.4, 44.4, -1.0), ft, light=15, shade=False, uv={'north': [0, 0, 16, 16]}, faces=('north',)))
    H += [E((-1.8, 37.8, -2.2), (1.8, 42.2, -1.6), 'dvn_light', light=15, shade=False),
          E((-1.2, 37.0, -2.0), (1.2, 43.0, -1.6), 'dvn_light', light=15, shade=False),
          E((-3.0, 35.8, -3.6), (3.0, 43.8, -2.4), 'dvn_aura', light=15, shade=False, faces=('north',))]
    H += [GEM((0, 47.4, -4.6), 1.6, 'dvn_gem'), E((-0.3, 48.0, -4.55), (0.3, 50.4, -4.25), 'dvn_seam', light=15, shade=False)]
    for sx in (1, -1):
        H.append(SEG((sx * 0.8, 47.6, -4.5), (sx * 2.6, 49.0, -4.0), 0.3, 0.2, 'dvn_seam', pv, FRONT, light=15, shade=False))
    if face == 'blaze':                                       # (rays of His light streaming out of the hood)
        for k in range(11):
            a = math.radians(200 + 140 * k / 10); ca, sa = math.cos(a), math.sin(a)
            L = 5.5 if k % 2 else 8.5; c0 = (0, 40.0, -5.2)
            H.append(SEG((c0[0] + 3.2 * ca, c0[1] - 4.2 * sa, c0[2]), (c0[0] + (3.2 + L) * ca, c0[1] - (4.2 + L) * sa, c0[2] - 1.2),
                         0.5, 0.25, 'dvn_light_g', pv, FRONT, light=15, shade=False))
        H.append(E((-3.4, 35.4, -4.6), (3.4, 44.6, -3.8), 'dvn_aura_g', light=15, shade=False, faces=('north', 'south')))
    if face == 'veiled':                                      # (a veil of silk over it, the light behind showing through)
        H.append(E((-3.8, 34.4, -4.9), (3.8, 45.0, -4.75), 'dvn_veil', light=8, uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, faces=('north', 'south')))
    return H


def _halo(which):
    """three rings standing behind His head, in the xy plane (each turns about its own z)"""
    pv = BP[which]; X, Y, Z = pv; H = []
    if which == 'halo_a':                                     # (the inner ring of gold, studs of light)
        H += RING(pv, 7.2, 24, 1.1, 0.8, 'dvn_halo')
        H += RING((X, Y, Z - 0.2), 6.2, 20, 0.35, 0.5, 'dvn_halo_w')
        for k in range(12):
            a = 2 * math.pi * k / 12
            H.append(GEM((X + 8.2 * math.cos(a), Y + 8.2 * math.sin(a), Z), 0.8, 'dvn_halo_w', rot=(0.0, 0.0, 45.0), shade=False))
    elif which == 'halo_b':                                   # (the middle ring of white light, eight diamonds)
        H += RING(pv, 10.6, 32, 0.6, 0.5, 'dvn_halo_w')
        for k in range(8):
            a = 2 * math.pi * (k + 0.5) / 8
            H.append(GEM((X + 10.6 * math.cos(a), Y + 10.6 * math.sin(a), Z), 1.6, 'dvn_gem', rot=(0.0, 0.0, 45.0)))
            b = 2 * math.pi * k / 8
            H.append(SEG((X + 9.4 * math.cos(b), Y + 9.4 * math.sin(b), Z), (X + 11.8 * math.cos(b), Y + 11.8 * math.sin(b), Z), 0.35, 0.3,
                         'dvn_halo', pv, FRONT, light=15, shade=False))
    else:                                                     # (the outer ring and its sunburst)
        H += RING(pv, 13.0, 36, 0.4, 0.4, 'dvn_halo')
        for k in range(24):
            a = 2 * math.pi * k / 24; ca, sa = math.cos(a), math.sin(a)
            L = 18.6 if k % 3 == 0 else (15.6 if k % 3 == 1 else 16.4)
            w = 0.9 if k % 3 == 0 else 0.6
            mid = 13.6 + (L - 13.6) * 0.55
            H.append(SEG((X + 13.6 * ca, Y + 13.6 * sa, Z), (X + mid * ca, Y + mid * sa, Z), w, 0.3, 'dvn_halo', pv, FRONT, light=15, shade=False))
            H.append(SEG((X + mid * ca, Y + mid * sa, Z), (X + L * ca, Y + L * sa, Z), w * 0.55, 0.25, 'dvn_halo_w', pv, FRONT, light=15, shade=False))
    return H


def _arm(sx):
    """the upper sleeve, and the cloth over the shoulder (the cope's shoulder, moving with the arm), a gold seam at its edge"""
    pv = BP['armr' if sx > 0 else 'arml']; A = []; x = sx * 8.6
    A.append(BX(sx, 6.6, 10.8, 26.4, 34.6, -2.3, 2.3, 'dvn_robe'))
    A += PANELS((x, 0), 36.4, 29.6, 2.4, 4.4, 8, 'dvn_robe', a0=-150 * sx, a1=150 * sx, pleat=0.04, h=0.5, out=0.3)
    A += PANELS((x, 0), 30.1, 29.3, 4.4, 4.5, 8, 'dvn_seam', a0=-150 * sx, a1=150 * sx, h=0.3, light=15, shade=False, wk=1.2, out=0.3)
    return A


def _fore(sx):
    """the bell sleeve, widening to the wrist, its lower lip hanging longer; the mouth in shadow; a glowing gold cuff"""
    pv = BP['forer' if sx > 0 else 'forel']; F = []; x = sx * 9.0
    F += PANELS((x, 0.2), 27.4, 19.2, 2.6, 4.3, 10, 'dvn_robe', pleat=0.05, h=0.45)
    F += PANELS((x, 0.6), 22.0, 16.8, 3.4, 4.0, 4, 'dvn_robe', a0=135, a1=225, h=0.45)          # (the lip, hanging behind)
    F += PANELS((x, 0.2), 19.9, 19.0, 4.35, 4.45, 10, 'dvn_seam', h=0.35, light=15, shade=False, wk=1.2)
    F += PANELS((x, 0.6), 17.4, 16.6, 4.05, 4.1, 4, 'dvn_seam', a0=135, a1=225, h=0.3, light=15, shade=False, wk=1.2)
    F.append(E((x - 3.6, 19.5, -3.4), (x + 3.6, 19.9, 3.8), 'dvn_hood_in', faces=('down',)))
    return F


def _hand(sx):
    """an open hand of light (built, then grown 1.35 about the wrist): the palm turned in, four long fingers a little apart, the
    thumb forward - unshaded, white running to pale gold, in a faint aura"""
    pv = BP['handr' if sx > 0 else 'handl']; Hd = []; x = sx * 9.2
    Hd.append(BX(sx, 8.65, 9.85, 15.9, 19.8, -1.6, 1.3, 'dvn_light', light=15, shade=False))
    for i, ln in enumerate((3.4, 4.0, 3.8, 3.1)):
        z0 = -1.6 + 0.82 * i
        Hd.append(BX(sx, 8.8, 9.7, 16.1 - ln, 16.2, z0, z0 + 0.52, 'dvn_light' if i % 2 else 'dvn_light_g', light=15, shade=False,
                     rot=('x', (i - 1.5) * -10.0, (x, 16.2, z0 + 0.26))))
    Hd.append(SEG((x, 17.8, -1.3), (x - sx * 0.4, 15.6, -3.0), 0.62, 0.62, 'dvn_light_g', pv, (sx * 1.0, 0, 0), light=15, shade=False))
    Hd.append(BX(sx, 8.1, 10.4, 11.4, 20.0, -2.6, 1.7, 'dvn_aura', light=15, shade=False))
    return rigkit.transform(Hd, lambda v: [8 + (c - 8) * 1.35 for c in v])


# ---- the wings: drawn flat (u outward from the root, v up) in a plane swept back by WSWEEP; n its back
WSWEEP = 24.0
WING = {1: dict(lead=[(0, 0), (3, 3.2), (7, 7.4), (12, 11.0), (18, 13.6), (24, 14.6), (29, 13.4), (32, 11.0)],
                sec=[(1.6 + 2.15 * i, 10.0 + 0.75 * i, 0.04 + 0.012 * i) for i in range(8)],
                prim=[(19.0 + 2.2 * i, 21.0 + 1.2 * i - (0.9 * (i - 4) ** 2 if i > 4 else 0), 0.14 + 0.07 * i) for i in range(7)],
                arm=(2.4, 1.0), fw=2.6),
        2: dict(lead=[(0, 0), (4, 0.6), (9, 0.2), (14, -1.2), (19, -3.4), (22, -5.6)],
                sec=[(1.4 + 2.1 * i, 6.5 + 0.5 * i, 0.08 + 0.02 * i) for i in range(5)],
                prim=[(12.0 + 2.1 * i, 10.0 + 0.9 * i - (0.8 * (i - 3) ** 2 if i > 3 else 0), 0.2 + 0.08 * i) for i in range(5)],
                arm=(1.8, 0.8), fw=2.2)}


def _lead_v(lead, u):
    for (u0, v0), (u1, v1) in zip(lead, lead[1:]):
        if u <= u1: return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return lead[-1][1]


def _wing(name):
    """a wing of feathered light: a leading edge of glowing gold, two rows of coverts under it, then the flight feathers in one
    layer - white vanes, gold-white shafts, burning gold tips - the secondaries near the root, the long primaries at the end"""
    i, sx = int(name[1]), (1 if name[2] == 'r' else -1)
    pv = BP[name]; G = WING[i]; lead = G['lead']
    a = math.radians(WSWEEP)
    du, n = (sx * math.cos(a), 0.0, math.sin(a)), (-sx * math.sin(a), 0.0, math.cos(a))
    P = lambda u, v, w=0.0: (pv[0] + u * du[0] + w * n[0], pv[1] + v, pv[2] + u * du[2] + w * n[2])
    W = []
    # the leading edge: tapering gold
    m = len(lead) - 1; w0, w1 = G['arm']
    for k in range(m):
        w = w0 + (w1 - w0) * k / max(1, m - 1)
        W.append(SEG(P(*lead[k], -0.2), P(*lead[k + 1], -0.2), w, w * 0.8, 'dvn_gold', pv, n, ext=0.3, light=13))
    # the coverts: two rows under it (the lower row shaded, so the rows read apart)
    for row, (dv, ln, tex) in enumerate(((0.8, 4.0, 'dvn_covert'), (3.0, 5.0, 'dvn_covert_d'))):
        us = [lead[0][0] + 0.6 + 2.0 * k for k in range(int((lead[-1][0] - 1.0) / 2.0))]
        for k, u in enumerate(us):
            v = _lead_v(lead, u) - dv
            A = P(u, v, 0.15 + 0.12 * row); B = P(u + 0.5 + 0.08 * u, v - ln, 0.15 + 0.12 * row)
            W.append(SEG(A, B, 2.6, 0.35, tex, pv, n, ext=0.2))
    # the flight feathers
    for k, (u, L, lean) in enumerate(G['sec'] + G['prim']):
        v0 = _lead_v(lead, u) - 5.6 if i == 1 else _lead_v(lead, u) - 4.6
        dx, dy = lean, -1.0; mm = math.hypot(dx, dy); dx, dy = dx / mm, dy / mm
        lay = 0.5 + 0.22 * (k % 2)
        A = P(u, v0, lay); C = P(u + dx * L * 0.8, v0 + dy * L * 0.8, lay); B = P(u + dx * L, v0 + dy * L, lay); T = P(u + dx * (L + 1.4), v0 + dy * (L + 1.4), lay)
        tex = 'dvn_feather' if k % 2 == 0 else 'dvn_feather_d'
        W.append(SEG(A, C, G['fw'], 0.4, tex, pv, n, uv=FULL()))
        W.append(SEG(C, B, G['fw'], 0.4, 'dvn_ftip', pv, n, light=15, shade=False, uv=FULL()))
        W.append(SEG(B, T, G['fw'] * 0.5, 0.36, 'dvn_ftip', pv, n, light=15, shade=False, uv=FULL()))
    return W


def _fx(kind):
    """on the right hand: 'gather' an orb of light gathering at the palm, rays and motes round it; 'beam' the smiting column of
    light out of the hand along the fingers - a white core in a sheath of gold light, rings down it, a flare at the hand"""
    pv = BP['fx']; X, Y, Z = pv; F = []
    c = (X - 1.6, Y, Z - 0.4)
    if kind == 'gather':
        F += [GEM(c, 2.6, 'dvn_light', shade=False), GEM(c, 3.6, 'dvn_light_g', rot=(0.0, 45.0, 45.0), shade=False),
              E((c[0] - 3.2, c[1] - 3.2, c[2] - 3.2), (c[0] + 3.2, c[1] + 3.2, c[2] + 3.2), 'dvn_aura_g', light=15, shade=False)]
        for k in range(14):
            a = 2 * math.pi * k / 14; b = (k % 3 - 1) * 0.6
            d = (math.cos(a) * math.cos(b), math.sin(a) * math.cos(b), math.sin(b))
            r0, r1 = 3.4, 6.0 if k % 2 else 8.0
            F.append(SEG(tuple(c[j] + d[j] * r0 for j in range(3)), tuple(c[j] + d[j] * r1 for j in range(3)), 0.4, 0.4, 'dvn_light_g', pv,
                         (0.3, 0.2, 1.0) if abs(d[2]) < 0.9 else (1, 0, 0), light=15, shade=False))
        rnd = random.Random(17)
        for k in range(10):
            a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(5, 9); y = rnd.uniform(-4, 4); s = rnd.uniform(0.4, 0.8)
            p = (c[0] + r * math.cos(a), c[1] + y, c[2] + r * math.sin(a))
            F.append(E(tuple(v - s / 2 for v in p), tuple(v + s / 2 for v in p), 'dvn_light', light=15, shade=False))
    else:
        top, L = Y - 1.0, 60.0
        F += [E((X - 0.9, top - L, Z - 0.9), (X + 0.9, top, Z + 0.9), 'dvn_light', light=15, shade=False),
              E((X - 2.0, top - L + 2, Z - 2.0), (X + 2.0, top - 1.0, Z + 2.0), 'dvn_aura_g', light=15, shade=False, faces=('north', 'south', 'east', 'west')),
              E((X - 3.2, top - L + 4, Z - 3.2), (X + 3.2, top - 3.0, Z + 3.2), 'dvn_aura', light=15, shade=False, faces=('north', 'south', 'east', 'west')),
              GEM((X, Y - 0.4, Z), 3.4, 'dvn_light', shade=False), GEM((X, Y - 0.4, Z), 4.6, 'dvn_aura_g', rot=(0.0, 45.0, 45.0), shade=False)]
        for k in range(1, 9):
            y = top - 7.5 * k; r = 3.0 - 0.12 * k
            F.append(E((X - r, y - 0.3, Z - r), (X + r, y + 0.3, Z + r), 'dvn_aura_g', light=15, shade=False))
        for k in range(8):                                    # (the flare at the hand: rays round the root of the beam)
            a = 2 * math.pi * k / 8; ca, sa = math.cos(a), math.sin(a)
            F.append(SEG((X + 1.6 * ca, Y - 1.0, Z + 1.6 * sa), (X + 5.0 * ca, Y - 3.4, Z + 5.0 * sa), 0.5, 0.4, 'dvn_light_g', pv, UP, light=15, shade=False))
    return F


def _pillar():
    """the pillar of light dropped where the beam strikes (not a rig part: its foot at the joint): a white core in two sheaths
    of gold light, rings rising up it, a flare on the ground round its foot"""
    pv = (0.0, 0.0, 0.0); F = []; H = 92.0
    F += [E((-2.4, 0, -2.4), (2.4, H, 2.4), 'dvn_light', pv, light=15, shade=False),
          E((-4.4, 0, -4.4), (4.4, H - 2, 4.4), 'dvn_aura_g', pv, light=15, shade=False, faces=('north', 'south', 'east', 'west')),
          E((-6.6, 0, -6.6), (6.6, H - 6, 6.6), 'dvn_aura', pv, light=15, shade=False, faces=('north', 'south', 'east', 'west'))]
    for k in range(10):
        y = 3 + 9.0 * k; r = 7.4 - 0.25 * k
        F.append(E((-r, y, -r), (r, y + 0.6, r), 'dvn_aura_g', pv, light=15, shade=False))
    F += [E((-12.0, 0.0, -12.0), (12.0, 0.4, 12.0), 'dvn_aura_g', pv, light=15, shade=False, faces=('up', 'down')),
          E((-8.0, 0.0, -8.0), (8.0, 0.6, 8.0), 'dvn_light', pv, light=15, shade=False, faces=('up', 'down'))]
    for k in range(12):
        a = 2 * math.pi * k / 12; ca, sa = math.cos(a), math.sin(a); L = 20.0 if k % 2 else 15.0
        F.append(SEG((7.0 * ca, 0.5, 7.0 * sa), (L * ca, 0.5, L * sa), 1.2 if k % 2 else 0.8, 0.3, 'dvn_light_g', pv, UP, light=15, shade=False))
    return F


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    if _RAW: return _RAW
    _rs.seed(9)
    def mk(part, fn, *a):
        _PV[0] = BP[part]; return (part, fn(*a))
    R = {}
    R[f'{PREFIX}body'] = mk('body', _body); R[f'{PREFIX}skirt'] = mk('skirt', _skirt); R[f'{PREFIX}chest'] = mk('chest', _chest)
    for f in (None,) + FACES:
        part, els = mk('head', _head, f)
        R[f'{PREFIX}head{"_x" + f if f else ""}'] = (part, rigkit.transform(els, lambda v: [8 + (c - 8) * HEAD_K for c in v]))
    for h in HALOS:
        R[f'{PREFIX}{h}'] = mk(h, _halo, h)
    for sx, s in ((1, 'r'), (-1, 'l')):
        R[f'{PREFIX}arm{s}'] = mk(f'arm{s}', _arm, sx); R[f'{PREFIX}fore{s}'] = mk(f'fore{s}', _fore, sx); R[f'{PREFIX}hand{s}'] = mk(f'hand{s}', _hand, sx)
    for w in WINGS:
        R[f'{PREFIX}{w}'] = mk(w, _wing, w)
    for k in FX:
        R[f'{PREFIX}fx_{k}'] = mk('fx', _fx, k)
    _PV[0] = (0.0, 0.0, 0.0); R[f'{PREFIX}pillar'] = ('pillar', _pillar())
    _RAW.update(R)
    return _RAW


def models():
    M = {}
    for name, (part, els) in _build().items():
        k = PILLAR_K if part == 'pillar' else PART_K.get(part, 1.0)
        els = shrink(els, k) if k != 1.0 else els
        for e in els:                                         # (every element inside the model box, every uv on the texture)
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
            for fc in e['faces'].values():
                u1, v1, u2, v2 = fc['uv']
                fc['uv'] = [max(0.0, min(16.0, c)) for c in (u1, v1, u2, v2)]
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    return M


def rp(R):
    """register the models (as phase238 does the Sovereign's) and the textures (TEXTURE_MODS reads textures())"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)


# ---------------------------------------------------------------------------------------------------- poses
# (rigkit, display frame: ('x', +a) leans a trunk forward / nods the head down; limb(fwd) swings a hanging limb forward, (out)
#  out to its own side and up, (turn) about its own length; ('y', +a) on the chest turns His right shoulder forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def T(lean=0.0, twist=0.0, side=0.0):
    return qs(('y', twist), ('x', lean), ('z', side))


def wing(sx, up=0.0, sweep=0.0, roll=0.0):
    """a wing: raised (up, out to its side and up about the root), swept (sweep, + toward the front, - back), rolled"""
    return qs(('y', sweep * sx), ('z', -up * sx), ('x', roll))


def wings(up1, sw1, up2, sw2, roll=0.0):
    return dict(w1r=wing(1, up1, sw1, roll), w1l=wing(-1, up1, sw1, roll), w2r=wing(1, up2, sw2, roll), w2l=wing(-1, up2, sw2, roll))


def halo(spin, tilt=0.0):
    """the three rings' turns: spin (deg) - the inner one with it, the middle one against it, the sunburst at half speed"""
    t = ('x', tilt)
    return dict(halo_a=qs(t, ('z', spin)), halo_b=qs(t, ('z', -spin)), halo_c=qs(t, ('z', spin * 0.5)))


def P(**kw):
    return kw


def full(p):
    """every part named (a full rig pose: the cinematic can set each display from it alone)"""
    p = dict(p)
    for k in PARTS:
        p.setdefault(k, rigkit.I)
    p.setdefault('_off', (0.0, HOVER, 0.0))
    return p


BOSS_POSES = {
    # arriving out of the light above: the head bowed, the hands together before the breast, the wings folded back, veiled
    'descend': full(P(_face='veiled', _halo='dim', _off=(0, HOVER + 2.0, 0), body=T(4), skirt=T(-6), chest=T(6), head=T(26),
                      armr=limb(1, 26, -6, 30), forer=limb(1, 74, 0, 64), handr=limb(1, 0, -10),
                      arml=limb(-1, 26, -6, 30), forel=limb(-1, 74, 0, 64), handl=limb(-1, 0, -10),
                      **wings(-45, -70, -30, -80, -25), **halo(0, 0))),
    # the reveal: the wings flung open and high, the arms opening wide, the head lifting, the halo ablaze
    'reveal': full(P(_off=(0, HOVER + 1.0, 0), body=T(-2), skirt=T(-3), chest=T(-6), head=T(-8),
                     armr=limb(1, 10, 60), forer=limb(1, 14), handr=limb(1, 0, 10, -90),
                     arml=limb(-1, 10, 60), forel=limb(-1, 14), handl=limb(-1, 0, 10, -90),
                     **wings(12, -6, 2, -4), **halo(40, 0))),
    # looking down at the Sovereign: leaning over it, the head tilted down, the left hand open toward it
    'gaze': full(P(_off=(0, HOVER, 0), body=T(6), skirt=T(-4), chest=T(10), head=T(26, 0, 4),
                   armr=limb(1, 12, 16), forer=limb(1, 18), handr=limb(1, 0, 6),
                   arml=limb(-1, 40, 24, -10), forel=limb(-1, 26, 0, -30), handl=limb(-1, 10, 10),
                   **wings(6, -12, -6, -10), **halo(80, -4))),
    # the right hand raised high over the halo, light gathering in it; the face blazing; the wings lifted
    'raise': full(P(_face='blaze', _fx='gather', _off=(0, HOVER + 1.2, 0), body=T(-2), skirt=T(-3), chest=T(-6, -12), head=T(6, 6),
                    armr=limb(1, 26, 150), forer=limb(1, 14, 0, -40), handr=limb(1, 12, -30),
                    arml=limb(-1, 50, 30, -10), forel=limb(-1, 30, 0, -30), handl=limb(-1, 10, 10),
                    **wings(24, -10, 10, -8), **halo(130, 0))),
    # and down: the hand thrust down and forward at it, the beam loosed; leaning into it, the wings swept forward
    'smite': full(P(_face='blaze', _fx='beam', _off=(0, HOVER, -1.0), body=T(8), skirt=T(-6), chest=T(14, 14), head=T(20, -4),
                    armr=limb(1, 66, 6), forer=limb(1, 6), handr=limb(1, 0, 0),
                    arml=limb(-1, -10, 42), forel=limb(-1, 20, 0, -20), handl=limb(-1, 0, 10),
                    **wings(8, 22, -8, 18), **halo(170, -6))),
    # after: arms lowered, calm, the head a little bowed, the wings eased down
    'rest': full(P(_off=(0, HOVER + 0.6, 0), body=T(2), skirt=T(-2), chest=T(4), head=T(12),
                   armr=limb(1, 10, 16), forer=limb(1, 18, 0, -10), handr=limb(1, 0, 4),
                   arml=limb(-1, 10, 16), forel=limb(-1, 18, 0, -10), handl=limb(-1, 0, 4),
                   **wings(-4, -16, -14, -14), **halo(210, 0))),
    # rising away: lifted, the head up toward the light, the arms out and low (palms down), the wings raised for the beat
    'ascend': full(P(_off=(0, HOVER + 6.0, 0), body=T(-4), skirt=T(10), chest=T(-6), head=T(-22),
                     armr=limb(1, -8, 40), forer=limb(1, 4, 0, -20), handr=limb(1, -6, 14),
                     arml=limb(-1, -8, 40), forel=limb(-1, 4, 0, -20), handl=limb(-1, -6, 14),
                     **wings(30, -14, 14, -10), **halo(250, 0))),
}
POSES = BOSS_POSES
BOSS_NAMES = list(BOSS_POSES)
SEQUENCE = [('descend', 0), ('reveal', 40), ('gaze', 40), ('raise', 30), ('smite', 6), ('rest', 50), ('ascend', 60)]


def between(a, b, t=0.5):
    """an in-between key (each joint bent part way - rigkit.mid): keeps a long chain, the raised arm, on its arc"""
    return rigkit.mid(a, b, t)


def world_boxes(pose, parts=None):
    """{part: [(centre, (axis, axis, axis), half extents)]} - each shown element as a box in the world (display frame, design
    units), as the pose stands (for a clip check)"""
    import dread_sovereign_art as _DS
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
                R = _DS._rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))
            cw = qrot(Q, tuple(D(cd)[i] - dp[i] for i in range(3)))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h)))
        out[p] = bl
    return out
