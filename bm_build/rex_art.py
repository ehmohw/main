"""2.99a: THE REX MOUNTS (art) - two hidden mounts, not followers: summoned with an item, ridden, and kept on the Partner
Wheel. The runtime (riding, the breath, the unlock quests, the wheel) is the main session's; this module is the art.

TWO KINDS (KINDS)
  atomic  THE ATOMIC REX: an upright kaiju in the classic stance - torso held near-vertical, thick column legs, a heavy tail
          dragging behind, a smallish head on a thick neck with a blunt snout, a strong brow and a powerful jaw. Charcoal to
          stone-grey craggy hide in clean square scales (no speckle). THREE ROWS of big jagged maple-leaf DORSAL PLATES from
          the neck to the tail tip, the largest between the shoulders, glowing nuclear blue: a cyan-white core inside a deep
          blue rim (two nested layers, both light_emission 15). Blue glowing eyes, a blue glow in the mouth and throat.
          A dark leather saddle with steel fittings on the shoulders, behind the neck - the biggest plates are its backrest.
  mecha   THE MECHA REX: the same skeleton and silhouette rebuilt as a war machine - gunmetal and steel-grey armour panels with
          seams and rivets, a visor band with two blue eyes, a blue chest reactor, the dorsal plates as steel blade-fins with
          blue-lit cores, blue thruster ports on the back and the heels, a mechanical jaw with steel fangs and a blue emitter
          in the throat, a cockpit seat (backrest, armrests, a console with a blue screen), shoulder missile pods (closed
          panels), and one small Vorn-green light on the console and on each pod: it was hidden in the Armada.

THE RIG (rigkit, as knight_art / mire_art). Design units: feet at y=0, facing -z, its right is +x; a design unit is one texel
of the 16 px textures. PARTS (25 displays per rex):
  body                      the hips (root)
  chest                     the barrel chest and shoulders (child of body)
  neck, head, jaw           neck (chest), head (neck), lower jaw (head) - JAW(a) opens it a degrees
  armr, forer, arml, forel  upper arm (chest) and forearm with the claws / fist (armr / arml)
  thighr shinr footr        the legs (thigh: body; shin: thigh; foot: shin)
  thighl shinl footl
  tail1..tail4              the tail, base to tip, each the child of the one before (tail1: body); each joint has a knuckle
                            (an octagonal collar of the child) so the tail stays one continuous tail through any bend
  plates                    the big dorsal plates on the chest's back - the largest, between the shoulders (child of chest);
                            the smaller ones ride on neck, body and the tail segments
  saddle                    the saddle / cockpit on the shoulders (child of chest)
  podr, podl                mecha: the shoulder missile pods; atomic: craggy shoulder scutes (each kind has every part,
                            so nothing is hidden by kind - HIDDEN only honours a pose's '_hide')

SCALE: RIG_SCALE = SCALE = 2.5 - a design unit is 2.5/16 block. At that size the idle rex stands ~7.4 blocks to the top of
its head (~7.7 to the tip of the highest plate), ~11 blocks nose to tail tip, ~3 blocks across the shoulders. The runtime
passes SCALE to all three, as phase245 does with the knights:
    RF.part_nbt(A, p, tags, SCALE, model=A.model_id(p, kind))
    RF.place(A, SCALE / 16, sel)
    RF.pose(A, A.posed(name, kind), SCALE, dur, sel)            (posed() adds the kind, so swap= finds the right models)
(No PART_K: every part fits its model box at k 1.) A different SCALE scales the whole rex (2.0: ~6 blocks).

SEAT = (0.0, y, z) blocks - from the rig's origin (between the feet, on the ground) to the saddle's seat surface at the
rider's middle, in idle_a: +y up, +z toward the rex's FRONT (display frame, yaw 0 facing south; negative z is behind the
origin). Put the host's passenger attachment there: a vanilla player rides with its feet 0.6 below the attachment point
(hips 0.15 above it), which seats it on the saddle. SEATS[pose] gives every pose's seat (it moves a little as the rex
walks and drops in sit); SEAT_SIT = SEATS['sit'] is where to mount and dismount.

POSES (POSES[name], shared by both kinds; every pose has its feet on y=0 and its tail on or above the ground):
  idle_a, idle_b        breathing (the chest rises in b), the tail swaying
  walk_0..walk_3        a heavy stomping walk: the body rolls over the planted foot, the tail swings against it
  run_0..run_3          a faster run, leaning forward, the tail raised level behind for balance
  roar                  head up, jaw wide, arms out
  breath_0              the charge: plates flaring back (and charged - see CHARGED), head drawn back, mouth opening
  breath_1              the breath / beam: head thrust forward and level, jaw wide, firing straight ahead
  stomp_0, stomp_1      rearing up on the left leg, the right raised - then slammed down, crouched on the impact
  tailswipe             hips and chest twisted, the tail swung round to its right
  sit                   crouched low on its haunches, tail on the ground, parked - for mounting
  mecha_fist            mecha: the right arm punched straight forward (the rocket fist); on atomic it is roar's dict
posed(name, kind[, charged]) adds '_kind' (and '_charge') for rigfol / rigkit.

CHARGED (breath_0's "plates light up from the tail upward"): every part that carries plates (PLATED) has a second model,
model_name(part, kind, 'charged') -> 'bm:rx_atomic_tail3_charged': the plates (atomic: rim and core both near-white blue;
mecha: the whole fin lit blue) blazing. Swap them in CHARGE_ORDER (tail tip first, up to the neck) a tick or two apart:
    execute as <tail4> run data modify entity @s item.components."minecraft:item_model" set value "bm:rx_<kind>_tail4_charged"
and back to model_name(part, kind) when the breath ends. (RF.pose(A, A.posed('breath_0', kind, charged=True), SCALE, d, sel,
swap=A.PLATED) swaps them all at once.)

GLOW = () - no brightness override needed: every blue highlight (plates/fins' cores, eyes, mouth and throat, the mecha's
reactor, visor, thrusters, screen, the Vorn lights, the atomic saddle's studs) is light_emission 15 in its model, so it
glows in the dark whatever the light; the grey hide shades with the world as it should. (LIGHT[kind] lists the materials.)

POINTS (design units, on the part named; rigkit.point(A, pose, part, pt, scale=SCALE) -> blocks from the host at yaw 0):
  MOUTH = ('head', pt)      between the jaws at the front of the mouth - where the breath / beam starts
  BREATH = (origin, dir)    for breath_1: the mouth in blocks (display frame) and the beam's unit direction (level, ahead)
  FIST = ('forer', pt)      the right fist (mecha_fist: where the rocket fist leaves)
  STOMP = ('footr', pt)     the right foot's sole (stomp_1: where the shockwave starts)

NAMES: model_id(part, kind[, variant]) -> 'rx_atomic_head' / 'rx_atomic_tail3_charged' (RF.part_nbt's model=);
model_name(part, kind[, variant]) -> the same with 'bm:'. rigfol / rigkit call model_name(part, pose[, suffix]) with a pose
dict: it reads '_kind' / '_charge' and answers without 'bm:', as theirs do.

ITEMS (ICONS, raw 16x16 outlined - gen_rp's ICONS loop finishes them with vanilla.process): atomic_whistle (a fossil claw
whistle, a steel mouthpiece, a blue glowing core and veins), mecha_remote (a chunky grey remote: blue screen, antenna, a
Vorn-green button), rex_fossil, rex_egg, mecha_blueprint_1/2/3 (head, body, legs), mecha_core.

gen_rp hook (PHASE2 block, beside knight_art / phase246):   import rex_art; rex_art.rp(sys.modules[__name__])
"""
import math
from PIL import Image

import rigkit
from rigkit import qs, el, seg, D, qrot, qmul

PREFIX = 'rx_'
KINDS = ('atomic', 'mecha')
RIG_SCALE = 2.5                                 # (a design unit = 2.5/16 block: ~7.4 blocks to the head standing)
SCALE = RIG_SCALE                               # (what the runtime passes to RF.part_nbt / RF.place (SCALE / 16) / RF.pose)
UP, FRONT, BACK = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (0.0, 0.0, 1.0)

TAILPTS = [(0.0, 17.0, 8.0), (0.0, 13.6, 19.5), (0.0, 10.0, 30.0), (0.0, 6.6, 40.0), (0.0, 3.8, 51.0)]   # (the tail's spine, joint to joint, the tip last)
PIVOT = {'body': (0.0, 17.0, 2.0), 'chest': (0.0, 24.0, 2.0), 'neck': (0.0, 36.0, 0.0), 'head': (0.0, 42.0, -3.0),
         'jaw': (0.0, 41.6, -2.0),
         'armr': (8.6, 33.0, -1.5), 'forer': (10.4, 27.6, -3.2), 'arml': (-8.6, 33.0, -1.5), 'forel': (-10.4, 27.6, -3.2),
         'thighr': (6.6, 17.5, 2.0), 'shinr': (7.6, 8.8, 3.0), 'footr': (7.6, 2.6, 1.6),
         'thighl': (-6.6, 17.5, 2.0), 'shinl': (-7.6, 8.8, 3.0), 'footl': (-7.6, 2.6, 1.6),
         'tail1': TAILPTS[0], 'tail2': TAILPTS[1], 'tail3': TAILPTS[2], 'tail4': TAILPTS[3],
         'plates': (0.0, 30.0, 8.0), 'saddle': (0.0, 38.5, 4.0), 'podr': (10.0, 36.0, 2.0), 'podl': (-10.0, 36.0, 2.0)}
PARENT = {'body': None, 'chest': 'body', 'neck': 'chest', 'head': 'neck', 'jaw': 'head',
          'armr': 'chest', 'forer': 'armr', 'arml': 'chest', 'forel': 'arml',
          'thighr': 'body', 'shinr': 'thighr', 'footr': 'shinr', 'thighl': 'body', 'shinl': 'thighl', 'footl': 'shinl',
          'tail1': 'body', 'tail2': 'tail1', 'tail3': 'tail2', 'tail4': 'tail3',
          'plates': 'chest', 'saddle': 'chest', 'podr': 'chest', 'podl': 'chest'}
PARTS = tuple(PIVOT)
PART_K = {}                                     # (every part fits its model box at its own size)
GLOW = ()                                       # (no brightness override: the highlights are light_emission 15 - see the docstring)
PLATED = ('neck', 'plates', 'body', 'tail1', 'tail2', 'tail3', 'tail4')
CHARGE_ORDER = ('tail4', 'tail3', 'tail2', 'tail1', 'body', 'plates', 'neck')
SEAT_PT = (0.0, 40.3, 4.4)                      # (the seat's surface at the rider's middle, on the saddle, rest design units)
MOUTH = ('head', (0.0, 41.4, -13.0))
FIST = ('forer', (10.4, 24.6, -11.2))
STOMP = ('footr', (7.6, 0.0, -1.0))


# ---------------------------------------------------------------------------------------------------- names
def model_id(part, kind, variant=None):
    """the model's id without the namespace: rx_<kind>_<part>[_charged] (RF.part_nbt's model=)"""
    assert kind in KINDS and part in PIVOT, (part, kind)
    if variant == 'charged' and part in PLATED:
        return f'{PREFIX}{kind}_{part}_charged'
    return f'{PREFIX}{kind}_{part}'


def model_name(part, kind, variant=None):
    """model_name(part, kind[, 'charged']) -> 'bm:rx_atomic_head'. (rigfol / rigkit's call, model_name(part, pose[, suffix]):
    the pose's _kind / _charge, answered without 'bm:' and with the suffix)"""
    if isinstance(kind, dict):
        return model_id(part, kind.get('_kind', 'atomic'), 'charged' if kind.get('_charge') else None) + (variant or '')
    return 'bm:' + model_id(part, kind, variant)


def posed(name, kind, charged=None):
    """a pose with its kind set (and '_charge' - breath_0 and breath_1 charge by default)"""
    p = dict(POSES[name], _kind=kind)
    if charged is not None: p['_charge'] = charged
    return p


def scale_of(pose=None):
    return RIG_SCALE


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


# ---------------------------------------------------------------------------------------------------- textures (16 px)
def _rgb(c):
    if isinstance(c, str): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(c[:3])


def _new(c):
    return Image.new('RGBA', (16, 16), _rgb(c) + (255,))


def _put(im, x, y, c):
    im.putpixel((x % 16, y % 16), _rgb(c) + (255,))


def _pebble(base, base2, lit, hi, gap):
    """square scales, 4 px, rows staggered by 2: a lit top-left edge, a dark gap below and right (no speckle)"""
    im = _new(gap)
    for r in range(4):
        off = 2 * (r % 2)
        for c in range(4):
            b = base2 if (c * 7 + r * 3) % 5 in (1, 3) else base
            for j in range(3):
                for i in range(3):
                    col = hi if (i == 0 and j == 0) else lit if (i == 0 or j == 0) else b
                    _put(im, off + 4 * c + i, 4 * r + j, col)
    return im


_SLABS = [(0, 0, 6, 5), (6, 0, 16, 4), (0, 5, 4, 11), (4, 5, 11, 10), (11, 4, 16, 9), (4, 10, 9, 16), (0, 11, 4, 16),
          (9, 10, 16, 16), (11, 9, 16, 10)]


def _crag(base, base2, lit, gap):
    """craggy slabs, 4-10 px: rough plates of hide, each lit along its top and left, a dark crack below and right"""
    im = _new(gap)
    for k, (x0, y0, x1, y1) in enumerate(_SLABS):
        b = base2 if k % 3 == 1 else base
        for y in range(y0, y1 - 1):
            for x in range(x0, x1 - 1):
                _put(im, x, y, lit if (y == y0 or x == x0) else b)
    return im


def _bands(base, lit, dark, split=True, h=4):
    """horizontal bands (belly scutes / tail rings / padding): a lit top row, a dark bottom one, split every 8 px, staggered"""
    im = _new(base)
    for r in range(16 // h):
        for x in range(16):
            _put(im, x, r * h, lit); _put(im, x, r * h + h - 1, dark)
        if split:
            sx = (4 * (r % 2)) + 2
            for y in range(r * h, r * h + h - 1):
                _put(im, sx, y, dark); _put(im, sx + 8, y, dark); _put(im, sx + 1, y, lit); _put(im, sx + 9, y, lit)
    return im


def _flat(base, lit=None, dark=None, glint=None):
    im = _new(base)
    for x in range(16):
        if lit: _put(im, x, 0, lit)
        if dark: _put(im, x, 15, dark)
    if glint:
        for y in range(1, 4):
            for x in range(1, 4): _put(im, x, y, glint)
    return im


def _frame(base, rim, dot=None):
    """a glow texture: a rim colour round the edge, the base inside, square highlights (dot) in a sparse grid"""
    im = _new(base)
    for i in range(16):
        for (x, y) in ((i, 0), (i, 15), (0, i), (15, i)): _put(im, x, y, rim)
    if dot:
        for y in (3, 11):
            for x in ((3, 11) if y == 3 else (7,)):
                for j in range(2):
                    for i in range(2): _put(im, x + i, y + j, dot)
    return im


def _panel(base, lit, seam, rivet, sx=(5, 12)):
    """armour panels: seams in a staggered brick of 8 px rows, a lit lip under each seam, rivets at the panels' corners"""
    im = _new(base)
    for r in range(2):
        y0 = 8 * r
        for x in range(16):
            _put(im, x, y0, seam); _put(im, x, y0 + 1, lit)
        v = sx[r]
        for y in range(y0 + 1, y0 + 8):
            _put(im, v, y, seam); _put(im, v + 1, y, lit)
        for x in (v + 3, v - 2):
            _put(im, x, y0 + 3, rivet)
        for x in (v + 3, v - 2):
            _put(im, x, y0 + 6, seam)
    return im


def _plate(base, lit, seam, rivet):
    """a steel plate: a lit lip, a dark seam at the foot, four rivets"""
    im = _flat(base, lit, seam)
    for x in range(16): _put(im, x, 1, lit)
    for (x, y) in ((2, 3), (13, 3), (2, 12), (13, 12)): _put(im, x, y, rivet)
    return im


def _grille(dark, light, k=2):
    im = _new(dark)
    for y in range(0, 16, k * 2):
        for x in range(16):
            for j in range(k): _put(im, x, y + j, light)
    return im


def _stripes(a, b, w=2):
    im = _new(a)
    for x in range(0, 16, w * 2):
        for y in range(16):
            for i in range(w): _put(im, x + i, y, b)
    return im


def _teeth(base, gap):
    im = _new(base)
    for x in range(3, 16, 4):
        for y in range(16): _put(im, x, y, gap)
    return im


def _stitch(base, lit, dark, st):
    """leather: lit top, dark foot, a line of stitches two px in from each edge"""
    im = _flat(base, lit, dark)
    for x in range(1, 16, 3):
        _put(im, x, 2, st); _put(im, x, 13, st)
    return im


# materials per kind: {mat: image}. Atomic: hide, crag, belly, claw, tooth, dark, eye, maw (mouth / throat glow), pedge /
# pcore (the plates' rim and core, glowing), pedge_c / pcore_c (charged), leather, strap, steel, stud (glowing blue studs).
# Mecha: armor, steel, dark, vent, joint, light (blue glow), core (cyan-white), visor, green (the Vorn light), fin (the steel
# blades), fin_c / light_c (charged), tooth (steel fangs), seat (padding), screen.
BLUE = dict(deep=(22, 64, 200), mid=(52, 120, 245), lt=(110, 200, 255), core=(196, 244, 255), white=(236, 252, 255))


def textures_of(kind):
    if kind == 'atomic':
        return {
            'hide': _pebble((54, 54, 60), (48, 48, 53), (68, 68, 75), (84, 84, 92), (30, 30, 34)),
            'crag': _crag((44, 44, 49), (52, 52, 58), (62, 62, 69), (24, 24, 28)),
            'belly': _bands((78, 78, 84), (96, 96, 103), (50, 50, 56)),
            'claw': _bands((150, 146, 136), (184, 180, 168), (100, 96, 90), split=False, h=4),
            'tooth': _teeth((224, 222, 212), (150, 146, 136)),
            'dark': _flat((20, 22, 28)),
            'eye': _flat(BLUE['lt'], glint=BLUE['white']),
            'maw': _frame(BLUE['mid'], BLUE['deep'], BLUE['lt']),
            'pedge': _frame(BLUE['deep'], (14, 40, 150), BLUE['mid']),
            'pcore': _frame(BLUE['core'], BLUE['lt'], BLUE['white']),
            'pedge_c': _frame(BLUE['lt'], BLUE['mid'], BLUE['core']),
            'pcore_c': _frame(BLUE['white'], BLUE['core'], (255, 255, 255)),
            'leather': _stitch((56, 60, 72), (74, 78, 92), (34, 36, 44), (110, 116, 130)),
            'strap': _flat((38, 40, 48), (52, 54, 64), (22, 24, 30)),
            'steel': _plate((120, 126, 138), (150, 156, 168), (78, 82, 92), (176, 182, 194)),
            'stud': _flat(BLUE['lt'], glint=BLUE['white']),
        }
    return {
        'armor': _panel((70, 74, 86), (96, 102, 116), (34, 36, 44), (130, 136, 150)),
        'steel': _plate((118, 124, 138), (146, 152, 166), (76, 80, 92), (174, 180, 194)),
        'dark': _flat((30, 32, 38), (40, 42, 50), (20, 21, 26)),
        'vent': _grille((20, 22, 27), (58, 62, 72)),
        'joint': _stripes((92, 98, 110), (150, 156, 170)),
        'light': _frame(BLUE['mid'], BLUE['deep'], BLUE['lt']),
        'core': _frame(BLUE['core'], BLUE['lt'], BLUE['white']),
        'visor': _flat(BLUE['lt'], BLUE['core'], BLUE['mid'], glint=BLUE['white']),
        'green': _flat((58, 200, 74), (122, 255, 106), (30, 138, 46)),
        'fin': _plate((104, 110, 124), (140, 146, 160), (60, 64, 74), (160, 166, 180)),
        'fin_c': _frame(BLUE['lt'], BLUE['mid'], BLUE['core']),
        'light_c': _frame(BLUE['white'], BLUE['core'], (255, 255, 255)),
        'tooth': _teeth((178, 184, 196), (90, 96, 108)),
        'seat': _bands((46, 48, 58), (62, 64, 76), (28, 30, 36), split=False, h=4),
        'screen': _grille((36, 110, 220), (90, 180, 255), 1),
    }


LIGHT = {'atomic': {'eye': 15, 'maw': 15, 'pedge': 15, 'pcore': 15, 'pedge_c': 15, 'pcore_c': 15, 'stud': 15},
         'mecha': {'light': 15, 'core': 15, 'visor': 15, 'green': 15, 'fin_c': 15, 'light_c': 15, 'screen': 15}}
CHARGE = {'atomic': {'pedge': 'pedge_c', 'pcore': 'pcore_c'}, 'mecha': {'fin': 'fin_c', 'light': 'light_c'}}
FULLUV = {'eye', 'stud', 'visor', 'green'}                      # (the whole texture on each face: a glint in the corner)
_TAG = {'atomic': 'a', 'mecha': 'm'}


def tex_name(mat, kind):
    return f'{PREFIX}{_TAG[kind]}_{mat}'


def textures():
    """{name: 16 x 16 RGBA} - every material of both kinds (assets/bm/textures/block)"""
    return {tex_name(m, k): im for k in KINDS for m, im in textures_of(k).items()}


# ---------------------------------------------------------------------------------------------------- building helpers
class _R:
    """a tiny deterministic random (uv shifts), reseeded per kind"""
    def __init__(self): self.s = 1
    def seed(self, s): self.s = s * 2654435761 % 4294967296 or 1
    def random(self):
        self.s = (self.s * 1103515245 + 12345) % 2147483648; return self.s / 2147483648


_rs = _R()
_PV = [None]
_KIND = ['atomic']


def E(fr, to, mat, rot=None, faces=None):
    """an element of a material about the current part's joint, its texture window shifted so boxes don't repeat"""
    fr, to = tuple(min(a, b) for a, b in zip(fr, to)), tuple(max(a, b) for a, b in zip(fr, to))
    uv = {f: [0, 0, 16, 16] for f in ('north', 'south', 'east', 'west', 'up', 'down')} if mat in FULLUV else None
    return el(fr, to, mat, _PV[0], rot=rot, uv=uv, faces=faces, shift=None if uv else (_rs.random(), _rs.random()))


def BX(sx, x0, x1, y0, y1, z0, z1, mat, rot=None):
    """a box on side sx (+1 its right, -1 its left): x given for the right side, mirrored"""
    a, b = sorted((sx * x0, sx * x1))
    if rot:
        ax, ang, o = rot
        rot = (ax, ang if ax == 'x' else -ang, (sx * o[0], o[1], o[2]))
    return E((a, y0, z0), (b, y1, z1), mat, rot=rot)


def SG(a, b, w, h, mat, up=FRONT, ext=0.0):
    """a box w across, h toward `up`, along a -> b"""
    if mat in FULLUV:
        e = seg(a, b, w, h, mat, _PV[0], up, ext)
        for fc in e['faces'].values(): fc['uv'] = [0, 0, 16, 16]
        return e
    return seg(a, b, w, h, mat, _PV[0], up, ext, shift=(_rs.random(), _rs.random()))


def OCT(c, r, h, mat, axis='y', k=0.7):
    """an octagonal collar: two crossed boxes about centre c, radius r, length h along the axis"""
    x, y, z = c
    if axis == 'y':
        return [E((x - r, y - h / 2, z - r * k), (x + r, y + h / 2, z + r * k), mat), E((x - r * k, y - h / 2 + 0.05, z - r), (x + r * k, y + h / 2 - 0.05, z + r), mat)]
    return [E((x - r, y - r * k, z - h / 2), (x + r, y + r * k, z + h / 2), mat), E((x - r * k, y - r, z - h / 2 + 0.05), (x + r * k, y + r, z + h / 2 - 0.05), mat)]


def _norm(v):
    n = math.sqrt(sum(c * c for c in v)); return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# the plates' outlines, the tip row first (side view: columns run along the spine, rows out from the back). '#' solid.
MASKS = {
    'big': ['....#....',
            '...###...',
            '#..###..#',
            '##.###.##',
            '.#######.',
            '..#####..',
            '#.#####.#',
            '#########',
            '.#######.',
            '.#######.'],
    'mid': ['...#...',
            '..###..',
            '#.###.#',
            '#######',
            '.#####.',
            '#.###.#',
            '#######',
            '.#####.'],
    'small': ['..#..',
              '.###.',
              '#####',
              '.###.',
              '#####',
              '.###.'],
    # (mecha: swept-back saw blades - the tip leans toward the tail, column 0)
    'fbig': ['##.......',
             '.##......',
             '.###.....',
             '..###..#.',
             '..####.##',
             '..#######',
             '.########',
             '#########',
             '.#######.',
             '.#######.'],
    'fmid': ['##.....',
             '.##....',
             '.###.#.',
             '..#####',
             '.######',
             '#######',
             '.#####.',
             '.#####.'],
    'fsmall': ['##...',
               '.##..',
               '.####',
               '#####',
               '.###.',
               '.###.'],
}


def _rects(mask):
    """the mask's solid cells as rectangles (c0, r0, c1, r1), inclusive: runs per row merged down the rows"""
    H = len(mask); runs = []
    for r, row in enumerate(mask):
        c = 0
        while c < len(row):
            if row[c] == '#':
                c1 = c
                while c1 + 1 < len(row) and row[c1 + 1] == '#': c1 += 1
                runs.append((c, r, c1)); c = c1 + 1
            else: c += 1
    out = []; open_ = {}
    for r in range(H):
        cur = {(c0, c1) for (c0, rr, c1) in runs if rr == r}
        for key in list(open_):
            if key not in cur: out.append(open_.pop(key))
        for key in cur:
            if key in open_: open_[key] = (key[0], open_[key][1], key[1], r)
            else: open_[key] = (key[0], r, key[1], r)
    out += open_.values()
    return out


def _erode(mask):
    H, W = len(mask), len(mask[0]); g = lambda r, c: 0 <= r < H and 0 <= c < W and mask[r][c] == '#'
    return [''.join('#' if g(r, c) and g(r - 1, c) and g(r + 1, c) and g(r, c - 1) and g(r, c + 1) else '.' for c in range(W))
            for r in range(H)]


def PLATE(base, spine, out, cell, mask, mats, t=1.2, sink=0.8):
    """a jagged dorsal plate standing on a back: its base centred at `base`, its columns along `spine`, its rows out along
    `out` (the tip furthest out), `cell` design units a cell, `t` thick. mats = (rim, core): the whole outline in the rim,
    the outline shrunk a cell in the core, a little thicker so it shows on both faces"""
    sp = _norm(spine); ou = _norm(out); ou = _norm(tuple(ou[i] - sum(ou[j] * sp[j] for j in range(3)) * sp[i] for i in range(3)))
    side = _cross(ou, sp)
    R = [[side[0], ou[0], sp[0]], [side[1], ou[1], sp[1]], [side[2], ou[2], sp[2]]]
    ang = rigkit.euler(R)
    rot = None if max(abs(v) for v in ang) < 1e-3 else (ang, tuple(base))
    m = MASKS[mask]; H, W = len(m), len(m[0]); out_ = []
    for layer, (mk, th) in enumerate(((m, t), (_erode(m), t + 0.36))):
        for (c0, r0, c1, r1) in _rects(mk):
            lo = (base[0] - th / 2, base[1] + (H - 1 - r1) * cell - sink, base[2] + (c0 - W / 2) * cell)
            hi = (base[0] + th / 2, base[1] + (H - r0) * cell - sink, base[2] + (c1 + 1 - W / 2) * cell)
            if layer: lo = (lo[0], lo[1] + 0.05, lo[2] + 0.05); hi = (hi[0], hi[1] - 0.05, hi[2] - 0.05)
            out_.append(E(lo, hi, mats[layer], rot=rot))
    return out_


def _tilt(v, sx, deg, axis):
    """turn a direction v about an axis by deg*sx (the side rows splay out)"""
    a = math.radians(deg * sx); ax = _norm(axis); c, s = math.cos(a), math.sin(a)
    d = sum(v[i] * ax[i] for i in range(3)); cr = _cross(ax, v)
    return tuple(v[i] * c + cr[i] * s + ax[i] * d * (1 - c) for i in range(3))


def ROW3(base, spine, out, sizes, side_dx, splay=24.0, side_at=0.0, side_sizes=None, center=True, side=True):
    """a stretch of the three rows: the centre plate at base, and a side pair offset side_dx to either side (shifted
    side_at along the spine, splayed out)"""
    kind = _KIND[0]; atomic = kind == 'atomic'
    mats = ('pedge', 'pcore') if atomic else ('fin', 'light')
    pre = '' if atomic else 'f'
    els = []
    mask, cell = sizes
    if center: els += PLATE(base, spine, out, cell, pre + mask, mats, t=1.25 if atomic else 1.0)
    if side:
        smask, scell = side_sizes or sizes
        for sx in (1, -1):
            b = tuple(base[i] + (side_dx * sx if i == 0 else 0) + _norm(spine)[i] * side_at for i in range(3))
            els += PLATE(b, spine, _tilt(out, sx, -splay, spine), scell, pre + smask, mats, t=1.05 if atomic else 0.9)
    return els


# ---------------------------------------------------------------------------------------------------- the parts (design units)
def _atomic():
    return _KIND[0] == 'atomic'


def _M(a, m):
    """a material by kind: (atomic, mecha)"""
    return a if _atomic() else m


def _body():
    at = _atomic(); S, C, B = _M('hide', 'armor'), _M('crag', 'steel'), _M('belly', 'dark')
    L = [E((-9.0, 13.0, -5.0), (9.0, 24.5, 8.0), S),
         E((-7.0, 14.0, -6.0), (7.0, 24.0, -5.0), _M('belly', 'steel')),
         E((-7.5, 13.5, 8.0), (7.5, 23.0, 10.0), C),
         E((-6.0, 12.2, -3.0), (6.0, 13.2, 6.0), _M('hide', 'dark'))]
    for sx in (1, -1):
        L.append(BX(sx, 8.6, 10.0, 14.5, 22.0, -2.5, 6.5, C))                     # (the hips' outer swell)
    if at:
        L += ROW3((0.0, 19.5, 9.6), UP, BACK, ('mid', 0.82), 2.6, side_at=0.8, side_sizes=('mid', 0.7))
    else:
        L += [E((-7.1, 16.0, -6.25), (7.1, 16.6, -5.9), 'light'), E((-7.1, 20.0, -6.25), (7.1, 20.6, -5.9), 'light'),   # (lit belly seams)
              E((-9.15, 20.5, -1.0), (9.15, 21.2, 5.0), 'light')]
        for y in (14.5, 18.0, 21.5):
            L.append(E((-6.6, y, -6.3), (6.6, y + 2.6, -5.8), 'armor'))
        L += ROW3((0.0, 19.5, 9.6), UP, BACK, ('mid', 0.82), 2.6, side_at=0.8, side_sizes=('mid', 0.7))
    return L


def _chest():
    at = _atomic(); S, C = _M('hide', 'armor'), _M('crag', 'steel')
    L = [E((-8.6, 23.0, -5.0), (8.6, 33.5, 7.5), S),
         E((-8.1, 33.0, -3.6), (8.1, 37.0, 7.0), C),
         E((-6.2, 36.5, -0.5), (6.2, 38.6, 7.2), C),
         E((-6.6, 23.5, -6.0), (6.6, 33.0, -5.0), _M('belly', 'steel'))]
    for sx in (1, -1):
        L += [BX(sx, 1.2, 7.8, 29.0, 35.2, -5.7, -3.2, S),                         # (the chest's two great slabs)
              BX(sx, 8.3, 9.3, 24.5, 32.5, -3.0, 6.0, C),                          # (flanks)
              BX(sx, 1.0, 7.4, 24.5, 34.0, 7.2, 8.4, C)]                           # (the back's muscle, the plates stand on it)
    if not at:
        L += [E((-2.4, 29.8, -6.5), (2.4, 34.2, -5.6), 'steel'),                   # (the reactor's housing)
              E((-1.7, 30.5, -6.9), (1.7, 33.5, -6.3), 'core'),                    # (THE REACTOR CORE)
              E((-2.8, 31.7, -6.6), (2.8, 32.3, -6.2), 'light'), E((-0.3, 29.4, -6.6), (0.3, 34.6, -6.2), 'light'),   # (its cross of light)
              E((-6.7, 26.0, -6.3), (6.7, 26.6, -5.9), 'light')]
        for sx in (1, -1):
            L += [BX(sx, 2.8, 7.4, 28.6, 29.2, -5.9, -5.6, 'light'),               # (lit seams under the pectoral plates)
                  BX(sx, 2.0, 5.6, 24.5, 27.5, 8.3, 9.4, 'steel'),                 # (BACK THRUSTERS: a housing, its port glowing)
                  BX(sx, 2.6, 5.0, 25.1, 26.9, 9.3, 9.7, 'light'),
                  BX(sx, 8.9, 9.5, 26.0, 31.0, -1.5, 4.5, 'vent')]                 # (flank vents)
    return L


def _plates():
    """the largest plates, between the shoulders - the saddle's backrest"""
    L = ROW3((0.0, 33.0, 8.3), UP, BACK, ('big', 1.08), 3.0, side_at=-2.4, side_sizes=('mid', 1.05), splay=26)
    L += ROW3((0.0, 25.4, 8.3), UP, BACK, ('mid', 0.86), 3.0, side_at=-1.2, side_sizes=('mid', 0.76), splay=26)
    return L


def _neck():
    at = _atomic(); S = _M('hide', 'armor')
    L = [E((-5.6, 34.5, -5.0), (5.6, 41.0, 4.0), S), E((-4.8, 40.0, -5.4), (4.8, 44.0, 2.6), S),
         E((-3.6, 35.0, -5.7), (3.6, 42.5, -5.0), _M('belly', 'joint'))]
    if at:
        for sx in (1, -1): L.append(BX(sx, 5.0, 6.0, 36.0, 40.0, -3.5, 2.5, 'crag'))
    else:
        L += [E((-5.8, 37.0, -4.6), (5.8, 38.0, 4.2), 'steel'), E((-5.0, 41.0, -5.0), (5.0, 41.8, 2.8), 'steel'),
              E((-3.7, 38.4, -5.85), (3.7, 39.0, -5.5), 'light')]
    L += ROW3((0.0, 38.3, 3.8), UP, BACK, ('small', 0.78), 2.2, side_at=-1.0, side_sizes=('small', 0.62), splay=22)
    L += ROW3((0.0, 42.0, 2.4), UP, BACK, ('small', 0.62), 1.8, side_at=-0.8, side_sizes=('small', 0.5), splay=20)
    return L


def _head():
    at = _atomic()
    if at:
        L = [E((-4.0, 42.0, -8.0), (4.0, 47.0, 1.0), 'hide'),                      # (the cranium)
             E((-3.3, 41.9, -14.0), (3.3, 45.3, -7.8), 'hide'),                    # (the snout)
             E((-2.9, 42.2, -14.6), (2.9, 44.8, -13.9), 'crag'),                   # (its blunt tip)
             E((-4.5, 45.1, -9.4), (4.5, 46.7, -6.4), 'crag'),                     # (the brow ridge)
             E((-3.6, 45.2, -12.0), (3.6, 46.0, -9.2), 'crag'),                    # (the ridge down the nose)
             E((-3.8, 41.0, 1.0), (3.8, 46.0, 3.0), 'hide'),                       # (the back of the skull)
             E((-2.7, 41.55, -13.6), (2.7, 41.95, -2.5), 'maw'),                   # (the roof of the mouth, glowing)
             E((-2.3, 41.2, -3.4), (2.3, 42.0, -1.2), 'maw')]                     # (the throat's glow)
        for sx in (1, -1):
            L += [BX(sx, 2.9, 4.2, 43.7, 44.9, -8.4, -6.7, 'eye'),                 # (blue glowing eyes, under the brow)
                  BX(sx, 3.6, 4.5, 40.6, 43.8, -7.0, -0.8, 'crag'),                # (the jaw's muscle)
                  BX(sx, 0.8, 1.8, 44.6, 45.2, -14.75, -13.9, 'dark'),             # (nostrils)
                  BX(sx, 4.0, 4.6, 45.8, 47.2, -1.0, 1.4, 'crag')]                 # (the ear nubs)
            for i, z in enumerate((-13.6, -12.0, -10.4, -8.8, -7.2)):              # (the upper teeth)
                L.append(BX(sx, 2.0 if i else 0.4, 3.0, 40.9, 42.0, z, z + 0.9, 'tooth'))
        L += [E((-0.6, 40.9, -13.9), (0.6, 42.0, -13.0), 'tooth')]
        L += ROW3((0.0, 44.0, 2.6), UP, BACK, ('small', 0.48), 1.6, side=False)
        return L
    L = [E((-4.1, 42.0, -8.0), (4.1, 47.2, 1.0), 'armor'), E((-3.4, 41.9, -14.0), (3.4, 45.0, -7.8), 'armor'),
         E((-3.0, 42.2, -14.8), (3.0, 44.6, -13.9), 'steel'),                      # (the nose cap)
         E((-4.6, 45.0, -9.4), (4.6, 46.4, -6.6), 'steel'),                        # (the brow plate)
         E((-4.35, 43.6, -8.6), (4.35, 45.0, -7.4), 'dark'),                       # (the visor's slot)
         E((-3.5, 45.0, -13.0), (3.5, 45.8, -9.2), 'steel'),                       # (the nose ridge)
         E((-3.9, 41.0, 1.0), (3.9, 46.4, 3.2), 'armor'),
         E((-1.0, 46.4, -6.0), (1.0, 48.6, 2.0), 'steel'),                         # (a crest)
         E((-0.4, 47.0, -4.0), (0.4, 47.6, 1.0), 'light'),
         E((-2.7, 41.55, -13.6), (2.7, 41.95, -2.5), 'dark'),
         E((-1.8, 41.3, -3.4), (1.8, 42.0, -1.2), 'core')]                         # (the throat's emitter)
    for sx in (1, -1):
        L += [BX(sx, 1.4, 4.3, 43.85, 44.75, -8.75, -7.3, 'visor'),                # (the visor's two blue eyes)
              BX(sx, 3.6, 4.5, 40.6, 43.6, -7.0, -0.8, 'steel'),                   # (the jaw's hydraulics)
              BX(sx, 4.1, 4.7, 41.6, 42.6, -5.6, -2.0, 'joint'),
              BX(sx, 0.9, 1.7, 44.1, 44.6, -14.9, -14.75, 'light'),                # (nose lights)
              BX(sx, 3.8, 5.6, 45.6, 47.4, -1.4, 1.6, 'steel'),                    # (the antenna fins)
              BX(sx, 4.6, 5.2, 47.0, 49.2, -0.6, 1.4, 'fin')]
        for i, z in enumerate((-13.6, -11.9, -10.2, -8.5)):                        # (steel fangs)
            L.append(BX(sx, 2.0 if i else 0.3, 3.0, 40.8, 42.0, z, z + 1.1, 'tooth'))
    return L


def _jaw():
    at = _atomic()
    L = [E((-3.0, 38.8, -13.6), (3.0, 41.5, -1.5), _M('hide', 'armor')),
         E((-2.4, 41.2, -12.6), (2.4, 41.6, -2.0), _M('maw', 'light')),             # (the mouth's floor, glowing)
         E((-2.2, 38.4, -11.0), (2.2, 38.9, -2.5), _M('belly', 'steel'))]
    for sx in (1, -1):
        for i, z in enumerate((-13.1, -11.5, -9.9, -8.3)):
            L.append(BX(sx, 1.9 if i else 0.4, 2.8, 41.4, 42.3, z, z + 0.85, 'tooth'))
    if not at:
        L += [E((-3.15, 39.6, -13.0), (3.15, 40.2, -2.0), 'steel')]
    return L


def _arm(sx):
    at = _atomic(); S = _M('hide', 'armor')
    sh = (sx * 9.6, 32.0, -1.6); el_ = (sx * 10.4, 27.6, -3.2)
    L = [SG(sh, el_, 4.0, 4.0, S, up=FRONT, ext=0.8)]
    if at:
        L += [BX(sx, 7.6, 12.0, 30.4, 35.0, -4.4, 0.8, 'crag')]
    else:
        L += [BX(sx, 7.4, 12.6, 31.0, 35.6, -4.6, 1.2, 'steel'), BX(sx, 12.5, 12.8, 32.0, 34.4, -3.4, 0.0, 'light'),   # (the pauldron)
              BX(sx, 9.4, 11.4, 27.0, 29.0, -4.4, -2.0, 'joint')]
    return L


def _fore(sx):
    at = _atomic(); S = _M('hide', 'armor')
    el_ = (sx * 10.4, 27.6, -3.2); wr = (sx * 10.4, 25.6, -8.6)
    L = [SG(el_, wr, 3.4, 3.4, S, up=UP, ext=0.6), BX(sx, 8.9, 11.9, 23.8, 27.0, -10.8, -8.2, S)]
    if at:
        for dx in (-1.1, 0.0, 1.1):
            L.append(SG((sx * (10.4 + dx), 24.8, -10.4), (sx * (10.4 + dx * 1.2), 23.4, -12.6), 0.8, 0.8, 'claw', up=UP, ext=0.2))
        L.append(SG((sx * 9.0, 25.4, -9.6), (sx * 8.4, 24.2, -11.4), 0.8, 0.8, 'claw', up=UP, ext=0.2))   # (the thumb)
    else:
        L += [BX(sx, 8.8, 12.0, 25.9, 26.6, -8.8, -7.8, 'light'),                  # (the wrist's ring: the rocket fist's thruster)
              BX(sx, 9.0, 11.8, 23.6, 26.6, -11.6, -10.6, 'steel')]                # (the knuckle plate)
        for dx in (-0.9, 0.0, 0.9):
            L.append(SG((sx * (10.4 + dx), 24.4, -11.4), (sx * (10.4 + dx), 23.4, -12.8), 0.8, 0.8, 'tooth', up=UP, ext=0.1))
    return L


def _thigh(sx):
    at = _atomic(); S, C = _M('hide', 'armor'), _M('crag', 'steel')
    L = [BX(sx, 2.8, 12.0, 9.0, 20.0, -4.2, 7.0, S), BX(sx, 11.6, 12.8, 11.0, 18.0, -2.0, 5.0, C),
         BX(sx, 3.6, 11.2, 10.0, 18.5, -4.9, -4.0, C)]
    if not at:
        L += [BX(sx, 12.7, 13.0, 12.5, 16.5, -1.0, 4.0, 'light'), BX(sx, 3.5, 11.3, 9.4, 10.2, -4.6, 6.6, 'joint')]
    return L


def _shin(sx):
    at = _atomic(); S, C = _M('hide', 'armor'), _M('crag', 'steel')
    L = [BX(sx, 3.8, 11.4, 2.2, 10.0, -1.6, 6.4, S), BX(sx, 4.6, 10.6, 6.0, 10.6, -2.4, -1.4, C),     # (the knee)
         BX(sx, 4.4, 10.8, 2.6, 7.0, 6.2, 7.0, C)]
    if not at:
        L += [BX(sx, 6.8, 8.4, 3.0, 8.0, -1.85, -1.55, 'light')]                   # (a blue strip down the shin)
    return L


def _foot(sx):
    at = _atomic(); S = _M('hide', 'armor')
    L = [BX(sx, 3.4, 11.8, 0.0, 3.4, -5.4, 5.6, S), BX(sx, 4.4, 10.8, 3.0, 4.4, -3.0, 5.0, S)]
    for i, (x0, x1) in enumerate(((3.6, 6.0), (6.4, 8.8), (9.2, 11.6))):
        L.append(BX(sx, x0, x1, 0.0, 2.5, -7.8, -5.2, S))
        L.append(BX(sx, x0 + 0.4, x1 - 0.4, 0.0, 1.6, -9.3, -7.6, _M('claw', 'tooth')))
    if at:
        L.append(BX(sx, 6.6, 8.6, 0.0, 1.4, 5.4, 7.2, 'claw'))                       # (the heel spur)
    else:
        L += [BX(sx, 5.4, 9.8, 0.4, 3.0, 5.5, 6.6, 'steel'), BX(sx, 6.0, 9.2, 0.9, 2.5, 6.5, 6.9, 'light')]   # (HEEL THRUSTER)
    return L


def _taildir(i):
    a, b = TAILPTS[i], TAILPTS[i + 1]
    return _norm(tuple(b[k] - a[k] for k in range(3)))


TAILW = [(13.0, 12.0, 11.6, 10.8), (11.0, 10.2, 9.0, 8.4), (8.6, 8.0, 6.6, 6.2), (6.2, 5.8, 2.6, 2.6)]   # (each segment's width / height at its root and end)
TAILPL = [(('mid', 0.86), ('mid', 0.72), 2.4), (('mid', 0.74), ('small', 0.8), 2.1), (('small', 0.86), ('small', 0.7), 1.6),
          (('small', 0.66), ('small', 0.52), 1.1)]


def _tail(i):
    at = _atomic(); S = _M('hide', 'armor')
    a, b = TAILPTS[i], TAILPTS[i + 1]
    w0, h0, w1, h1 = TAILW[i]
    m = tuple((a[k] + b[k]) / 2 for k in range(3))
    L = []
    if i:                                                                         # (the knuckle: a collar round the joint, so the bend never opens)
        pw = TAILW[i - 1][2]; ph = TAILW[i - 1][3]
        d = _taildir(i)
        L.append(SG(tuple(a[k] - d[k] * 1.6 for k in range(3)), tuple(a[k] + d[k] * 1.6 for k in range(3)), pw * 0.94, ph * 0.94, S, up=UP))
        L.append(SG(tuple(a[k] - d[k] * 1.2 for k in range(3)), tuple(a[k] + d[k] * 1.2 for k in range(3)), pw * 0.7, ph * 1.02, S, up=UP))
    L.append(SG(a, m, w0, h0, S, up=UP, ext=0.3))
    L.append(SG(m, b, (w0 + w1) / 2 * 0.98, (h0 + h1) / 2 * 0.98, S, up=UP, ext=0.3 if i < 3 else 0.0))
    if i == 3:
        L.append(SG(tuple(b[k] - _taildir(i)[k] * 1.5 for k in range(3)), tuple(b[k] + _taildir(i)[k] * 2.4 for k in range(3)), w1, h1, _M('crag', 'steel'), up=UP))
    d = _taildir(i); up = _norm((0.0, d[2], -d[1]))
    belly = _M('belly', 'steel')
    L.append(SG(tuple(a[k] - up[k] * (h0 / 2 - 0.2) for k in range(3)), tuple(b[k] - up[k] * (h1 / 2 - 0.4) for k in range(3)), w0 * 0.62, 0.9, belly, up=UP))
    if not at:                                                                    # (armour rings round the segment, lit seams)
        for t in (0.3, 0.75):
            c = tuple(a[k] + (b[k] - a[k]) * t for k in range(3)); w = w0 + (w1 - w0) * t; h = h0 + (h1 - h0) * t
            L.append(SG(tuple(c[k] - d[k] * 0.7 for k in range(3)), tuple(c[k] + d[k] * 0.7 for k in range(3)), w + 0.5, h + 0.5, 'steel', up=UP))
        c = tuple(a[k] + (b[k] - a[k]) * 0.52 for k in range(3)); w = w0 + (w1 - w0) * 0.52
        for sx in (1, -1):
            L.append(SG(tuple(c[k] - d[k] * 2.5 + (sx * (w / 2 + 0.05) if k == 0 else 0) for k in range(3)),
                        tuple(c[k] + d[k] * 2.5 + (sx * (w / 2 + 0.05) if k == 0 else 0) for k in range(3)), 0.4, 0.8, 'light', up=UP))
    # the plates down its top: two stretches per segment (the centre row), the side pairs between them
    (cm, sm, dx) = TAILPL[i]
    for t, cmask in ((0.25, cm), (0.72, (cm[0], cm[1] * 0.92))):
        c = tuple(a[k] + (b[k] - a[k]) * t for k in range(3)); h = h0 + (h1 - h0) * t
        base = tuple(c[k] + up[k] * (h / 2 - 0.1) for k in range(3))
        L += ROW3(base, tuple(-v for v in d), up, cmask, dx, side_at=-0.24 * (len(MASKS[cmask[0]][0]) * cmask[1]),
                  side_sizes=sm, splay=28)
    return L


def _saddle():
    at = _atomic()
    tilt = ('x', -16.0, (0.0, 38.5, 4.0))                                         # (the seat built level for the idle lean)
    if at:
        L = [E((-5.2, 38.2, -0.2), (5.2, 39.2, 8.6), 'leather', rot=tilt),         # (the pad)
             E((-3.0, 39.0, 1.0), (3.0, 40.3, 7.4), 'leather', rot=tilt),          # (the seat)
             E((-3.2, 39.8, 6.8), (3.2, 43.0, 8.2), 'leather', rot=tilt),          # (the cantle)
             E((-1.3, 39.8, 0.4), (1.3, 41.8, 1.6), 'steel', rot=tilt),            # (the pommel)
             E((-0.5, 41.8, 0.5), (0.5, 42.3, 1.5), 'stud', rot=tilt),
             E((-8.75, 34.6, 1.2), (8.75, 35.4, 2.6), 'strap'),                    # (the girth, round the shoulders)
             E((-6.3, 37.6, 1.2), (6.3, 38.8, 2.6), 'strap')]
        for sx in (1, -1):
            L += [BX(sx, 5.0, 6.4, 34.0, 38.8, -0.2, 8.0, 'leather', rot=tilt),    # (the flaps down its flanks)
                  BX(sx, 5.8, 6.6, 31.0, 34.2, 3.4, 4.4, 'strap', rot=tilt),       # (stirrup leathers)
                  BX(sx, 5.6, 7.0, 30.4, 31.2, 2.8, 5.0, 'steel', rot=tilt),       # (the stirrups)
                  BX(sx, 2.0, 2.8, 40.6, 41.6, 7.6, 8.4, 'stud', rot=tilt),
                  BX(sx, 8.6, 8.9, 34.4, 35.6, 1.4, 2.4, 'stud')]
        return L
    L = [E((-5.2, 38.2, -0.2), (5.2, 39.2, 8.6), 'armor', rot=tilt),               # (the cockpit's deck)
         E((-3.0, 39.0, 1.0), (3.0, 40.3, 7.4), 'seat', rot=tilt),                 # (the seat)
         E((-3.2, 39.8, 6.6), (3.2, 44.4, 8.2), 'seat', rot=tilt),                 # (the high backrest)
         E((-3.6, 43.6, 6.4), (3.6, 44.8, 8.6), 'steel', rot=tilt),
         E((-4.6, 38.8, -1.6), (4.6, 41.6, 0.6), 'armor', rot=tilt),               # (the console before the seat)
         E((-3.4, 41.6, -1.2), (3.4, 42.0, 0.3), 'steel', rot=tilt),
         E((-2.4, 40.0, 0.62), (2.4, 41.4, 0.82), 'screen', rot=tilt),             # (its blue screen, facing the rider)
         E((2.8, 41.2, 0.62), (3.6, 42.0, 0.85), 'green', rot=tilt),               # (a small Vorn-green light)
         E((-3.6, 41.2, 0.62), (-2.8, 42.0, 0.85), 'light', rot=tilt)]
    for sx in (1, -1):
        L += [BX(sx, 3.0, 4.4, 40.0, 41.6, 1.6, 7.0, 'steel', rot=tilt),           # (armrests)
              BX(sx, 4.6, 6.2, 34.0, 39.2, -0.6, 8.4, 'armor', rot=tilt),          # (side panels)
              BX(sx, 6.15, 6.4, 35.0, 35.6, 0.4, 7.4, 'light', rot=tilt)]
    return L


def _pod(sx):
    if _atomic():                                                                 # (the shoulder's craggy scutes)
        return [BX(sx, 8.0, 11.4, 34.6, 37.0, -2.6, 3.2, 'crag'), BX(sx, 8.6, 10.6, 36.4, 37.8, -1.6, 2.2, 'crag')]
    L = [BX(sx, 9.0, 14.8, 36.0, 40.4, -3.4, 4.6, 'armor'),                         # (the pod)
         BX(sx, 9.4, 14.4, 40.2, 40.8, -3.0, 4.2, 'steel'),
         BX(sx, 9.4, 14.4, 36.4, 40.0, -3.8, -3.3, 'steel'),                       # (its closed front panel)
         BX(sx, 11.85, 12.0, 36.4, 40.0, -3.95, -3.75, 'dark'), BX(sx, 9.4, 14.4, 38.15, 38.3, -3.95, -3.75, 'dark'),   # (the hatches' seams)
         BX(sx, 13.4, 14.0, 39.2, 39.8, -3.95, -3.75, 'green' if sx < 0 else 'light'),
         BX(sx, 8.4, 9.4, 35.0, 38.0, -1.0, 2.0, 'joint'),                         # (its mount)
         BX(sx, 14.8, 15.1, 37.0, 39.4, -2.0, 3.6, 'vent')]
    return L


_RAW = {}


def _build():
    """{kind: {part: [elements (material keys)]}} - geometry"""
    if _RAW: return _RAW
    for kind in KINDS:
        _KIND[0] = kind; _rs.seed(5 if kind == 'atomic' else 6)

        def mk(part, fn, *a):
            _PV[0] = PIVOT[part]; return fn(*a)
        R = {'body': mk('body', _body), 'chest': mk('chest', _chest), 'neck': mk('neck', _neck), 'head': mk('head', _head),
             'jaw': mk('jaw', _jaw), 'plates': mk('plates', _plates), 'saddle': mk('saddle', _saddle)}
        for sx, s in ((1, 'r'), (-1, 'l')):
            R['arm' + s] = mk('arm' + s, _arm, sx); R['fore' + s] = mk('fore' + s, _fore, sx)
            R['thigh' + s] = mk('thigh' + s, _thigh, sx); R['shin' + s] = mk('shin' + s, _shin, sx)
            R['foot' + s] = mk('foot' + s, _foot, sx); R['pod' + s] = mk('pod' + s, _pod, sx)
        for i in range(4):
            R[f'tail{i + 1}'] = mk(f'tail{i + 1}', _tail, i)
        _RAW[kind] = {p: R[p] for p in PARTS}
    _KIND[0] = 'atomic'
    return _RAW


def _finish(els, kind, charged=False):
    """the geometry's materials as the kind's textures; light_emission where the material glows"""
    lt = LIGHT[kind]; ch = CHARGE[kind] if charged else {}
    out = []
    for e in els:
        faces = {}
        for f, fc in e['faces'].items():
            m = ch.get(fc['texture'][1:], fc['texture'][1:])
            faces[f] = dict(fc, texture='#' + tex_name(m, kind))
        e = dict(e, faces=faces); e.pop('light_emission', None)
        m = next(iter(e['faces'].values()))['texture'][1:].split('_', 2)[-1]
        L = lt.get(m, 0)
        if L: e['light_emission'] = L
        out.append(e)
    return out


def models():
    """{model id: (textures, elements)} - every part x kind (and the PLATED parts' charged models), as gen_rp's HATS take them"""
    M = {}
    for kind, parts in _build().items():
        for part, els in parts.items():
            for variant in ((None, 'charged') if part in PLATED else (None,)):
                fe = _finish(els, kind, variant == 'charged')
                for e in fe:
                    for v in e['from'] + e['to']:
                        assert -16 <= v <= 32, (kind, part, e['from'], e['to'])
                    for fc in e['faces'].values():
                        assert all(0.0 <= t <= 16.0 for t in fc['uv']), (kind, part, fc['uv'])
                used = sorted({fc['texture'][1:] for e in fe for fc in e['faces'].values()})
                M[model_id(part, kind, variant)] = ({t: f'bm:block/{t}' for t in used}, fe)
    return M


# ---------------------------------------------------------------------------------------------------- world geometry (grounding, checks)
def _rotm(r):
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if 'axis' in r: return {'x': rx, 'y': ry, 'z': rz}[r['axis']](math.radians(r['angle']))
    return mm(mm(rz(math.radians(r.get('z', 0))), ry(math.radians(r.get('y', 0)))), rx(math.radians(r.get('x', 0))))


def world_boxes(pose, parts=None, kind='atomic', xf=None):
    """{part: [(centre, axes, half extents)]} - each element as an oriented box in the world (display frame, design units)"""
    raw = _build()[kind]; xf = xf or rigkit.solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        Q, t = xf[p]; pv = PIVOT[p]; dp = D(pv); W = tuple(t[i] + dp[i] for i in range(3)); bl = []
        for e in raw[p]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))
            cw = qrot(Q, tuple(D(cd)[i] - dp[i] for i in range(3)))
            bl.append((tuple(W[i] + cw[i] for i in range(3)), tuple(qrot(Q, D(a)) for a in ax), tuple(h)))
        out[p] = bl
    return out


def lowest(pose, parts, xf=None):
    lo = 1e9
    for bl in world_boxes(pose, parts, xf=xf).values():
        for c, ax, h in bl:
            lo = min(lo, c[1] - sum(abs(ax[i][1]) * h[i] for i in range(3)))
    return lo


def extent(pose, kind='atomic'):
    """(lowest y, highest y, min z, max z) of the whole rex, design units (display frame: +z its front)"""
    lo, hi, zl, zh = 1e9, -1e9, 1e9, -1e9
    for bl in world_boxes(pose, kind=kind).values():
        for c, ax, h in bl:
            ey = sum(abs(ax[i][1]) * h[i] for i in range(3)); ez = sum(abs(ax[i][2]) * h[i] for i in range(3))
            lo, hi = min(lo, c[1] - ey), max(hi, c[1] + ey); zl, zh = min(zl, c[2] - ez), max(zh, c[2] + ez)
    return lo, hi, zl, zh


def top_of(pose, part, kind='atomic'):
    return max(c[1] + sum(abs(ax[i][1]) * h[i] for i in range(3)) for c, ax, h in world_boxes(pose, (part,), kind)[part])


def at(pose, part, p, xf=None):
    """where a design point carried by `part` stands in the world (design units, design frame)"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); Q, t = xf[part]; pv = D(PIVOT[part])
    r = qrot(Q, tuple(D(p)[i] - pv[i] for i in range(3)))
    return D(tuple(t[i] + pv[i] + r[i] for i in range(3)))


# ---------------------------------------------------------------------------------------------------- posing kit
# (rigkit's display frame: ('x', +a) leans a trunk forward / nods the head down / opens the jaw / raises the tail; limb(fwd)
#  swings a limb forward, (out) out to its side; knee(a) bends a shin back; ('y', +a) on the trunk turns its right shoulder
#  forward, on the tail swings it to its right)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def knee(a):
    return qs(('x', a))


def T(lean=0.0, twist=0.0, side=0.0):
    return qs(('y', twist), ('x', lean), ('z', side))


def JAW(a):
    return qs(('x', a))


def TL(raise_=0.0, swing=0.0):
    return qs(('y', swing), ('x', raise_))


def _conj(q):
    return (-q[0], -q[1], -q[2], q[3])


def flat(p, yaw=0.0, pitch=0.0):
    """both feet set flat on the ground (their world turn only the given yaw), whatever the legs are doing"""
    p = dict(p)
    for s in 'rl':
        Qs = rigkit.solve(PIVOT, PARENT, p)['shin' + s][0]
        p['foot' + s] = qmul(_conj(Qs), qs(('y', yaw), ('x', pitch)))
    return p


def ground(p, parts=('footr', 'footl', 'shinr', 'shinl')):
    """set the root's height so the lowest point of these parts rests on y=0"""
    p = dict(p); o = p.get('_off', (0.0, 0.0, 0.0)); p['_off'] = (o[0], 0.0, o[2])
    lo = lowest(p, parts); p['_off'] = (o[0], round(-lo, 4), o[2])
    return p


TAIL = ('tail1', 'tail2', 'tail3', 'tail4')


def settle_tail(p, floor=0.25, drag=None):
    """keep the tail on or above the ground (raise tail1 until clear); drag: lower tail2/3 until the tip lies within it"""
    p = dict(p)
    for _ in range(60):
        if lowest(p, TAIL) >= floor: break
        p['tail1'] = qmul(p.get('tail1', rigkit.I), qs(('x', 1.5)))
    if drag:
        for _ in range(30):
            lo = lowest(p, ('tail4',))
            if lo <= drag: break
            for t in ('tail2', 'tail3', 'tail4'):
                p[t] = qmul(p.get(t, rigkit.I), qs(('x', -1.0)))
            if lowest(p, TAIL) < floor:
                for t in ('tail2', 'tail3', 'tail4'):
                    p[t] = qmul(p.get(t, rigkit.I), qs(('x', 1.0)))
                break
    return p


def level_head(p, pitch=0.0):
    """turn the head so its snout points level (pitch: + up)"""
    p = dict(p)
    for _ in range(40):
        a = at(p, 'head', (0.0, 43.0, -14.0)); b = at(p, 'head', (0.0, 43.0, -4.0))
        cur = math.degrees(math.atan2(a[1] - b[1], math.hypot(a[0] - b[0], a[2] - b[2])))
        if abs(cur - pitch) < 0.3: break
        p['head'] = qmul(p.get('head', rigkit.I), qs(('x', (cur - pitch) * 0.9)))
    return p


def _done(p, floor=0.25, drag=None, feet=True, yaw=0.0):
    if feet: p = flat(p, yaw)
    p = ground(p)
    return settle_tail(p, floor, drag)


def _pose(name):
    s_ = math.sin
    if name in ('idle_a', 'idle_b'):
        b = name == 'idle_b'; sw = -1 if b else 1
        p = dict(body=T(8), chest=T(9 if b else 11), neck=T(17 if b else 19), head=T(-32 if b else -33), jaw=JAW(5 if b else 3),
                 armr=limb(1, 12, 6), forer=limb(1, 4), arml=limb(-1, 14, 6), forel=limb(-1, 2),
                 thighr=limb(1, 10, 3), shinr=knee(4), thighl=limb(-1, 6, 3), shinl=knee(4),
                 tail1=TL(-6, 3 * sw), tail2=TL(-4, 5 * sw), tail3=TL(-2, 6 * sw), tail4=TL(2, 7 * sw))
        return _done(p, drag=1.0)
    if name.startswith('walk_'):
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = dict(body=T(9, 5 * sw, 3 * sw), chest=T(10, -4 * sw, -2 * sw), neck=T(18, -2 * sw), head=T(-32, 3 * sw), jaw=JAW(4),
                 armr=limb(1, 14 - 8 * sw, 6), forer=limb(1, 6), arml=limb(-1, 14 + 8 * sw, 6), forel=limb(-1, 6),
                 thighr=limb(1, 9 + 22 * sw), shinr=knee(6 + 34 * max(0.0, -s_(ph + 0.6))),
                 thighl=limb(-1, 9 - 22 * sw), shinl=knee(6 + 34 * max(0.0, s_(ph + 0.6))),
                 tail1=TL(-4, -5 * sw), tail2=TL(-3, -6 * sw), tail3=TL(-2, -7 * sw), tail4=TL(2, -8 * sw))
        p = _done(p)
        o = p['_off']; p['_off'] = (o[0], o[1] - 0.6 * abs(math.cos(ph)), o[2])    # (the stomp: down on the planted foot)
        return settle_tail(p)
    if name.startswith('run_'):
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = dict(body=T(18, 4 * sw, 2 * sw), chest=T(16, -3 * sw), neck=T(8), head=T(-38, 2 * sw), jaw=JAW(8),
                 armr=limb(1, 30 - 10 * sw, 8), forer=limb(1, 10), arml=limb(-1, 30 + 10 * sw, 8), forel=limb(-1, 10),
                 thighr=limb(1, 22 + 32 * sw), shinr=knee(10 + 50 * max(0.0, -s_(ph + 0.5))),
                 thighl=limb(-1, 22 - 32 * sw), shinl=knee(10 + 50 * max(0.0, s_(ph + 0.5))),
                 tail1=TL(-8, -4 * sw), tail2=TL(4, -5 * sw), tail3=TL(4, -6 * sw), tail4=TL(4, -6 * sw))
        p = _done(p, floor=1.0)
        o = p['_off']; p['_off'] = (o[0], o[1] + 1.2 * abs(s_(ph)), o[2])
        return p
    if name in ('roar', 'mecha_fist_atomic'):
        p = dict(body=T(2), chest=T(-4), neck=T(-2), head=T(-22), jaw=JAW(38),
                 armr=limb(1, 38, 30), forer=limb(1, -10), arml=limb(-1, 38, 30), forel=limb(-1, -10),
                 thighr=limb(1, 14, 6), shinr=knee(8), thighl=limb(-1, -6, 6), shinl=knee(6),
                 tail1=TL(-2, 8), tail2=TL(2, 10), tail3=TL(4, 12), tail4=TL(6, 12))
        return _done(p)
    if name == 'breath_0':
        p = dict(body=T(4), chest=T(-2), neck=T(-10), head=T(-6), jaw=JAW(14), plates=qs(('x', -7)),
                 armr=limb(1, 24, 18), forer=limb(1, 12), arml=limb(-1, 24, 18), forel=limb(-1, 12),
                 thighr=limb(1, 18, 6), shinr=knee(14), thighl=limb(-1, -6, 6), shinl=knee(10),
                 tail1=TL(4, 10), tail2=TL(4, 14), tail3=TL(4, 18), tail4=TL(6, 22))
        p = _done(p); p['_charge'] = True
        return p
    if name == 'breath_1':
        p = dict(body=T(12), chest=T(16), neck=T(36), jaw=JAW(30), plates=qs(('x', -3)),
                 armr=limb(1, 10, 12), forer=limb(1, 0), arml=limb(-1, 10, 12), forel=limb(-1, 0),
                 thighr=limb(1, 32, 6), shinr=knee(22), thighl=limb(-1, -10, 6), shinl=knee(8),
                 tail1=TL(-4, -4), tail2=TL(2, -6), tail3=TL(4, -8), tail4=TL(4, -8))
        p = level_head(p, 0.0)
        p = _done(p); p['_charge'] = True
        return p
    if name == 'stomp_0':
        p = dict(body=T(-4, -6, -5), chest=T(-6, 4), neck=T(10), head=T(-24), jaw=JAW(24),
                 armr=limb(1, 50, 30), forer=limb(1, 10), arml=limb(-1, 40, 34), forel=limb(-1, 10),
                 thighr=limb(1, 62, 8), shinr=knee(70), thighl=limb(-1, -2, 2), shinl=knee(4),
                 tail1=TL(6, 4), tail2=TL(4, 6), tail3=TL(2, 6), tail4=TL(2, 6))
        p = flat(p)
        p['footr'] = qmul(p['footr'], qs(('x', 10)))
        return settle_tail(ground(p))
    if name == 'stomp_1':
        p = dict(body=T(18, 4, 3), chest=T(14), neck=T(14), head=T(-38), jaw=JAW(30),
                 armr=limb(1, 30, 22), forer=limb(1, 16), arml=limb(-1, 26, 22), forel=limb(-1, 16),
                 thighr=limb(1, 52, 8), shinr=knee(44), thighl=limb(-1, 4, 6), shinl=knee(40),
                 tail1=TL(-10, -4), tail2=TL(-4, -6), tail3=TL(-2, -6), tail4=TL(2, -6))
        return _done(p)
    if name == 'tailswipe':
        p = dict(body=T(10, 30, 0), chest=T(10, 14), neck=T(18, -16), head=T(-30, -26), jaw=JAW(16),
                 armr=limb(1, 20, 24), forer=limb(1, 10), arml=limb(-1, 30, 20), forel=limb(-1, 10),
                 thighr=limb(1, 14, 6, -30), shinr=knee(16), thighl=limb(-1, 0, 8, 30), shinl=knee(14),
                 tail1=TL(4, 26), tail2=TL(2, 28), tail3=TL(2, 30), tail4=TL(2, 30))
        return _done(p, floor=1.2)
    if name == 'sit':
        p = dict(body=T(18), chest=T(-4), neck=T(20), head=T(-30), jaw=JAW(2),
                 armr=limb(1, 22, 6), forer=limb(1, 6), arml=limb(-1, 22, 6), forel=limb(-1, 6),
                 thighr=limb(1, 92, 10), shinr=knee(118), thighl=limb(-1, 92, 10), shinl=knee(118),
                 tail1=TL(-26), tail2=TL(-2), tail3=TL(2), tail4=TL(2))
        return _done(p, drag=0.8)
    if name == 'mecha_fist':
        p = dict(body=T(8, -12), chest=T(8, 24), neck=T(16, -14), head=T(-30, -10), jaw=JAW(10),
                 armr=limb(1, 92, 4), forer=limb(1, -64), arml=limb(-1, -14, 16), forel=limb(-1, 40),
                 thighr=limb(1, -8, 6), shinr=knee(10), thighl=limb(-1, 26, 6), shinl=knee(14),
                 tail1=TL(-4, -10), tail2=TL(-2, -10), tail3=TL(0, -10), tail4=TL(2, -8))
        return _done(p)
    raise KeyError(name)


POSE_NAMES = ('idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'run_0', 'run_1', 'run_2', 'run_3', 'roar',
              'breath_0', 'breath_1', 'stomp_0', 'stomp_1', 'tailswipe', 'sit', 'mecha_fist')
NOTES = {'idle_a': 'breathing out', 'idle_b': 'breathing in', 'roar': 'head up, jaw wide', 'breath_0': 'the charge: plates flare',
         'breath_1': 'the breath, level ahead', 'stomp_0': 'rearing on the left leg', 'stomp_1': 'slammed down',
         'tailswipe': 'twisted, tail swung round', 'sit': 'parked - mount here', 'mecha_fist': 'mecha: rocket fist (atomic: roar)'}
_PZ = {}


def _poses():
    if not _PZ:
        for n in POSE_NAMES:
            _PZ[n] = _pose(n)
    return _PZ


class _Lazy(dict):
    """POSES, solved on first use"""
    def _f(self):
        if not dict.__len__(self): dict.update(self, _poses())
    def __getitem__(self, k): self._f(); return dict.__getitem__(self, k)
    def __iter__(self): self._f(); return dict.__iter__(self)
    def __len__(self): self._f(); return dict.__len__(self)
    def __contains__(self, k): self._f(); return dict.__contains__(self, k)
    def keys(self): self._f(); return dict.keys(self)
    def items(self): self._f(); return dict.items(self)
    def values(self): self._f(); return dict.values(self)
    def get(self, k, d=None): self._f(); return dict.get(self, k, d)


POSES = _Lazy()


def pose_for(name, kind):
    """the pose the runtime should run for a kind: mecha_fist on the atomic is its roar"""
    return POSES['roar'] if (name == 'mecha_fist' and kind == 'atomic') else POSES[name]


def seat(pose_name='idle_a'):
    """the seat (blocks, display frame from the rig's origin: +z its front) in a pose"""
    return tuple(round(v, 3) for v in rigkit.point(sys_mod(), POSES[pose_name], 'saddle', SEAT_PT, scale=SCALE))


def sys_mod():
    import sys
    return sys.modules[__name__]


class _Seats(dict):
    def _f(self):
        if not dict.__len__(self): dict.update(self, {n: seat(n) for n in POSE_NAMES})
    def __getitem__(self, k): self._f(); return dict.__getitem__(self, k)
    def items(self): self._f(); return dict.items(self)
    def keys(self): self._f(); return dict.keys(self)
    def __iter__(self): self._f(); return dict.__iter__(self)
    def __len__(self): self._f(); return dict.__len__(self)


SEATS = _Seats()
SEAT = (0.0, 6.091, -0.205)                     # (= seat('idle_a'), checked by check(); blocks, +z its front)
SEAT_SIT = (0.0, 3.9, 1.5)                      # (= seat('sit'), checked by check())


def breath():
    """(origin, direction) of the breath in breath_1: the mouth in blocks (display frame, from the rig's origin) and the
    beam's unit direction (display frame: +z its front)"""
    pz = POSES['breath_1']; m = rigkit.point(sys_mod(), pz, *MOUTH, scale=SCALE)
    b = rigkit.point(sys_mod(), pz, 'head', (0.0, MOUTH[1][1], MOUTH[1][2] + 8.0), scale=SCALE)
    d = _norm(tuple(m[i] - b[i] for i in range(3)))
    return tuple(round(v, 3) for v in m), tuple(round(v, 3) for v in d)


# ---------------------------------------------------------------------------------------------------- the item icons (16 x 16, raw)
def hx(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


FOSSIL = ['#3e3b38', '#5e5a55', '#827c74', '#a8a196', '#cfc8ba']
STEELR = ['#2e3138', '#4a4f5a', '#6c7380', '#959caa', '#c6ccd6']
GUN = ['#24272e', '#3a3e48', '#565c68', '#787f8c', '#a2a9b6']
GLOWR = ['#0d2a7a', '#1c4fc8', '#3a8cff', '#7cc8ff', '#d8f6ff']
EGG = ['#3c3d43', '#5a5c63', '#7d8088', '#a2a5ad', '#c8cbd2']
PAPER = ['#12306a', '#1a4590', '#2560b6', '#3378d0', '#4c90e4']
INK = '#e6f0ff'
VORN = ['#1e6a2a', '#3ac84a', '#9cff8a']


class _S:
    """a 16 x 16 sketch (sprites280's kit, cut down): px, rectangles lit from the top left, lines, discs, polygons"""
    def __init__(self): self.p = {}

    def px(self, x, y, c):
        if 0 <= x < 16 and 0 <= y < 16:
            if c is None: self.p.pop((x, y), None)
            else: self.p[(x, y)] = hx(c) if isinstance(c, str) else c

    def blk(self, x0, y0, x1, y1, ramp, b=2):
        """a block of shade b, its top row and left column a step lighter, its bottom row and right column a step darker"""
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                v = b
                if (y == y0 and y1 > y0) or (x == x0 and x1 > x0): v += 1
                if (y == y1 and y1 > y0) or (x == x1 and x1 > x0): v -= 1
                self.px(x, y, ramp[max(0, min(len(ramp) - 1, v))])

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            self.px(round(x0 + (x1 - x0) * i / n) if n else x0, round(y0 + (y1 - y0) * i / n) if n else y0, c(i, n) if callable(c) else c)

    def disc(self, cx, cy, r, ramp, sq=1.0):
        for y in range(16):
            for x in range(16):
                dx, dy = (x + 0.5 - cx), (y + 0.5 - cy) / sq
                if math.hypot(dx, dy) <= r:
                    nx, ny = dx / r, dy / r; nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                    v = (0.6 * nx + 0.8 * ny) * -0.75 + nz * 0.55
                    self.px(x, y, ramp[max(0, min(len(ramp) - 1, int((v + 0.45) / 1.5 * len(ramp))))])

    def poly(self, pts, ramp, lo=0, hi=None):
        """a polygon filled in blocky bands of the ramp, lighter to the top left; its bottom/right edge a step darker"""
        hi = len(ramp) - 1 if hi is None else hi
        inside = lambda x, y: _inpoly(x + 0.5, y + 0.5, pts)
        cells = [(x, y) for y in range(16) for x in range(16) if inside(x, y)]
        if not cells: return
        ks = [x + y for x, y in cells]; a, b = min(ks), max(ks)
        for x, y in cells:
            t = 1 - ((x + y) - a) / max(1, b - a)
            v = lo + int(round(t * (hi - lo) * 0.9 + 0.3))
            if not inside(x + 1, y) or not inside(x, y + 1): v -= 1
            if not inside(x - 1, y) or not inside(x, y - 1): v += 1
            self.px(x, y, ramp[max(0, min(len(ramp) - 1, v))])

    def tube(self, pts, r, col, samples=90):
        """a rounded rod along a bezier, r(t) its radius, col(t) its ramp - lit as a cylinder from the top left"""
        n = len(pts) - 1

        def bz(t):
            x = y = 0.0
            for i, (px_, py) in enumerate(pts):
                b = math.comb(n, i) * (1 - t) ** (n - i) * t ** i; x += b * px_; y += b * py
            return x, y
        S_ = [(i / samples,) + bz(i / samples) for i in range(samples + 1)]
        for y in range(16):
            for x in range(16):
                best = None
                for t, cx, cy in S_:
                    rr = r(t); d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                    if d <= rr and (best is None or d / rr < best[0]): best = (d / rr, t, cx, cy, rr)
                if best:
                    _, t, cx, cy, rr = best
                    nx, ny = (x + 0.5 - cx) / rr, (y + 0.5 - cy) / rr; nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
                    ramp = col(t); v = -(nx * -0.6 + ny * -0.8) * 0.75 + nz * 0.55
                    self.px(x, y, ramp[max(0, min(len(ramp) - 1, int((v + 0.45) / 1.5 * len(ramp))))])

    def image(self, outline=True):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
        for (x, y), c in self.p.items(): px[x, y] = c
        if outline:
            add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
                   any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            for x, y in add: px[x, y] = (18, 16, 22, 255)
        return im


def _inpoly(x, y, pts):
    c = False; n = len(pts)
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: c = not c
    return c


def icon_atomic_whistle():
    """a fossil claw made a whistle: a steel mouthpiece and band at its root, a blue glowing core window, blue veins"""
    s = _S()
    s.tube([(3.0, 13.2), (3.6, 7.0), (8.5, 2.6), (14.2, 3.2)], lambda t: 2.7 * (1 - t) ** 0.8 + 0.55,
           lambda t: STEELR if t < 0.17 else FOSSIL)
    s.tube([(2.2, 14.2), (2.6, 13.0)], lambda t: 1.9, lambda t: STEELR)                         # (the mouthpiece's lip)
    for x, y in ((4, 9), (5, 9), (4, 10), (5, 10)): s.px(x, y, STEELR[1])                        # (the band's shadow)
    for x, y in ((3, 9), (3, 10)): s.px(x, y, STEELR[3])
    for x, y, c in ((5, 7, 3), (6, 6, 2), (6, 7, 4), (7, 6, 3), (7, 5, 2)): s.px(x, y, GLOWR[c])  # (the core's window)
    s.px(6, 6, GLOWR[4]); s.px(5, 7, GLOWR[3])
    for x, y in ((8, 5), (9, 4), (10, 4), (11, 3)): s.px(x, y, GLOWR[2])                         # (a vein toward the tip)
    for x, y in ((4, 8), (4, 7)): s.px(x, y, GLOWR[1])
    s.px(13, 3, FOSSIL[1]); s.px(14, 3, FOSSIL[1])
    return s.image()


def icon_mecha_remote():
    """a chunky grey remote: a blue screen, buttons (one Vorn green), a stubby antenna with a blue tip"""
    s = _S()
    s.blk(3, 5, 11, 15, GUN, 2)
    s.blk(4, 6, 10, 9, GLOWR, 2)                                                                 # (the screen)
    for x in range(5, 10): s.px(x, 7, GLOWR[3] if x % 2 else GLOWR[2])
    s.px(5, 8, GLOWR[4]); s.px(6, 8, GLOWR[3])
    for (x, y, c) in ((5, 11, None), (8, 11, None), (5, 13, None), (8, 13, 'g')):
        if c == 'g':
            s.px(x, y, VORN[2]); s.px(x + 1, y, VORN[1]); s.px(x, y + 1, VORN[1]); s.px(x + 1, y + 1, VORN[0])
        else:
            s.px(x, y, STEELR[4]); s.px(x + 1, y, STEELR[3]); s.px(x, y + 1, STEELR[3]); s.px(x + 1, y + 1, STEELR[1])
    s.line(10, 4, 12, 1, STEELR[3]); s.px(10, 5, STEELR[2])
    s.px(12, 0, GLOWR[4]); s.px(13, 0, GLOWR[3]); s.px(13, 1, GLOWR[2]); s.px(12, 1, GLOWR[3])
    return s.image()


def icon_rex_fossil():
    """a grey fossil skull fragment (side view, snout to the left): the eye socket, a nostril, a row of teeth, its back
    broken off jagged, faint blue cracks"""
    s = _S()
    s.poly([(1.0, 9.0), (3.0, 6.0), (7.0, 4.0), (11.0, 2.6), (13.0, 3.6), (14.4, 3.0), (15.0, 6.0), (13.6, 7.4), (15.0, 9.4),
            (13.0, 11.0), (9.0, 11.6), (5.0, 11.0), (1.4, 11.2)], FOSSIL, 0, 4)
    for x, y in ((9, 5), (10, 5), (9, 6), (10, 6), (11, 6)): s.px(x, y, '#1c1a1a')               # (the eye socket)
    s.px(10, 7, FOSSIL[0]); s.px(9, 4, FOSSIL[4])
    s.px(3, 8, '#1c1a1a'); s.px(4, 8, FOSSIL[1])                                                # (the nostril)
    for x in (2, 4, 6, 8, 10): s.px(x, 12, FOSSIL[4]); s.px(x, 13, FOSSIL[3]) if x in (4, 8) else None   # (teeth)
    for x, y in ((12, 8), (11, 9), (11, 10), (7, 8), (6, 9)): s.px(x, y, GLOWR[2])               # (faint blue cracks)
    s.px(12, 7, GLOWR[1]); s.px(5, 9, GLOWR[1])
    return s.image()


def icon_rex_egg():
    """a big grey egg, square speckles, glowing blue veins (charged by lightning) and a spark"""
    s = _S()
    s.disc(8.0, 8.8, 5.6, EGG, sq=1.28)
    for x, y in ((6, 4), (10, 6), (5, 9), (9, 11), (11, 13), (7, 13)): s.px(x, y, EGG[1])
    s.px(10, 5, EGG[2]); s.px(5, 10, EGG[2])
    for x, y, c in ((7, 15, 2), (7, 14, 3), (8, 13, 3), (8, 12, 4), (9, 11, 3), (9, 10, 2), (10, 9, 2), (8, 11, 3), (7, 10, 2),
                    (6, 9, 1), (10, 12, 2), (11, 11, 1)):
        s.px(x, y, GLOWR[c])
    for x, y, c in ((13, 1, 4), (12, 2, 3), (13, 2, 2), (14, 0, 3)): s.px(x, y, GLOWR[c])         # (the spark)
    return s.image()


def _sheet(s, torn):
    """a torn sheet of blueprint paper: lighter to the top left, a faint grid, its torn edge (cells removed)"""
    s.poly([(1.0, 1.5), (14.8, 1.0), (15.0, 14.6), (1.2, 15.0)], PAPER, 1, 4)
    for x in range(2, 15):
        for y in range(2, 15):
            if (x % 4 == 0 or y % 4 == 0) and (x, y) in s.p: s.px(x, y, PAPER[2])
    for (x, y) in torn: s.px(x, y, None)


def _ink(s, pts):
    for x, y in pts: s.px(x, y, INK)


def icon_blueprint(n):
    s = _S()
    if n == 1:                                          # (the head: a profile, the visor, the jaw)
        _sheet(s, [(14, y) for y in range(1, 16) if y % 3 != 1] + [(15, y) for y in range(16)] + [(13, 3), (13, 9), (13, 14)])
        _ink(s, [(3, 6), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 6), (11, 7), (11, 8), (3, 7), (3, 8), (4, 8),
                 (5, 8), (6, 8), (7, 8), (3, 10), (4, 11), (5, 11), (6, 11), (7, 11), (8, 10), (9, 9), (10, 9)])
        s.px(5, 6, GLOWR[4]); s.px(6, 6, GLOWR[4])
        _ink(s, [(4, 13), (6, 13), (8, 13), (10, 13)])
    elif n == 2:                                        # (the body: the torso, the reactor's circle)
        _sheet(s, [(1, y) for y in range(16)] + [(2, y) for y in range(0, 16, 3)] + [(x, 15) for x in range(16) if x % 4 != 2])
        _ink(s, [(5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (5, 9), (5, 10), (5, 11),
                 (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (10, 9), (10, 10), (10, 11), (6, 12), (7, 12), (8, 12), (9, 12)])
        _ink(s, [(7, 5), (8, 5), (6, 6), (9, 6), (6, 7), (9, 7), (7, 8), (8, 8)])
        s.px(7, 6, GLOWR[4]); s.px(8, 7, GLOWR[3])
    else:                                               # (the legs: a thigh, the knee, a clawed foot)
        _sheet(s, [(x, 1) for x in range(16)] + [(x, 2) for x in range(16) if x % 3 == 0] + [(14, y) for y in range(8, 16)] + [(15, y) for y in range(16)])
        _ink(s, [(5, 4), (6, 4), (7, 4), (8, 4), (4, 5), (4, 6), (4, 7), (5, 8), (9, 5), (9, 6), (9, 7), (8, 8), (6, 9), (7, 9),
                 (5, 10), (5, 11), (8, 10), (8, 11), (4, 12), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (9, 13), (10, 13),
                 (10, 12), (9, 12)])
        _ink(s, [(11, 4), (12, 4), (11, 6), (12, 6)])
    return s.image()


def icon_mecha_core():
    """a reactor core: a steel cradle top and bottom, a glass capsule with the blue core blazing inside"""
    s = _S()
    s.blk(3, 1, 12, 3, STEELR, 2); s.blk(3, 13, 12, 15, STEELR, 1)
    s.blk(4, 4, 11, 12, GLOWR, 1)
    s.disc(7.8, 8.2, 3.3, GLOWR[1:] + ['#ffffff'], sq=1.25)
    for y in range(4, 13): s.px(3, y, STEELR[3]); s.px(12, y, STEELR[1])
    s.px(5, 5, '#ffffff'); s.px(5, 6, GLOWR[4])
    for x in (5, 7, 9): s.px(x, 2, GLOWR[3])
    s.px(10, 14, VORN[1])
    return s.image()


ICON_FNS = {'atomic_whistle': icon_atomic_whistle, 'mecha_remote': icon_mecha_remote, 'rex_fossil': icon_rex_fossil,
            'rex_egg': icon_rex_egg, 'mecha_blueprint_1': lambda: icon_blueprint(1), 'mecha_blueprint_2': lambda: icon_blueprint(2),
            'mecha_blueprint_3': lambda: icon_blueprint(3), 'mecha_core': icon_mecha_core}
ITEMS = tuple(ICON_FNS)
SUMMON = {'atomic': 'atomic_whistle', 'mecha': 'mecha_remote'}


def icons():
    """{name: raw 16 x 16} (gen_rp's ICONS loop finishes them with vanilla.process)"""
    return {n: f() for n, f in ICON_FNS.items()}


def icon(name):
    """the icon as the pack ships it"""
    import vanilla
    return vanilla.process(name, icons()[name])


# ---------------------------------------------------------------------------------------------------- checks / gen_rp
def check():
    """the contract's own checks: models in range, SEAT / SEAT_SIT as computed, every pose grounded"""
    M = models()
    names = set(textures())
    for mid, (tex, els) in M.items():
        for t in tex.values(): assert t.split('/', 1)[1] in names, (mid, t)
    for n in POSE_NAMES:
        lo = lowest(POSES[n], ('footr', 'footl', 'shinr', 'shinl'))
        assert abs(lo) < 0.05 or n == 'stomp_0' and abs(lo) < 0.05, (n, lo)
        assert lowest(POSES[n], TAIL) > -0.05, (n, 'tail below ground')
    s = seat('idle_a'); assert all(abs(a - b) < 0.02 for a, b in zip(s, SEAT)), ('SEAT is', s)
    s = seat('sit'); assert all(abs(a - b) < 0.05 for a, b in zip(s, SEAT_SIT)), ('SEAT_SIT is', s)
    return len(M)


def rp(R):
    """gen_rp: the rx_ block textures (TEXTURE_MODS), every part x kind (and the charged plates) as a 3D model at display
    scale (HATS, DISPLAY_3D_EXTRA 'rx_'), the item icons (ICONS)"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
    R.ICONS.update(icons())
