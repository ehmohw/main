"""2.99 (v299a): THE STATUE KNIGHTS (art) - mini-bosses of the final dungeons. They stand as statues in a puzzle room, stone and
still, and come to life once its puzzle is solved: hulking dark knights with GIANT MACES they swing, slam and spin. Beaten,
each turns back to stone where it fell - and the player is granted its statue, a placeable trophy for their base.

TWO KINDS (KINDS)
  dread  the Undercrown (the Dread's gothic Nether dungeon): blackened, battered plate in the Dreadborne palette (dread_art /
         dread_armor: void-plate, bone, red light). A great helm with a narrow eye-slit and two SQUARE RED EYES glowing in it
         (the armour's square eyes, no fuss), a nasal ridge, a low crest and two bone horns; bone ribs over the breastplate
         round a red jewel, bone spikes on the pauldrons and the knees, a tattered dark cloak with a blood-red hem. The mace:
         a long iron haft wrapped in leather, a huge eight-flanged head of dark iron with a band of red light, a bone spike.
  vorn   the Vorn Armada (the alien fleet): the same build in Vorn tech (vexis_art's VORN gunmetal and XEN green, phase32's
         black trooper armour with its green stripe): black-gunmetal plate, green glowing seams, a SQUARE GREEN VISOR with two
         bright square eyes in it, a mouth grille, two short antennae with froglight tips; a black-green cloak with a glowing
         hem stripe. The mace: a gunmetal haft, an octagonal head with four glowing green PLASMA RIDGES and a plasma emitter tip.

TWO FINISHES (FINISHES) for every part - the runtime swaps the item model to change one into the other:
  stone  the statue: weathered stone, eyes unlit (dread: dark blackstone-grey, cracked; vorn: pale grey hull-stone, faint dead
         seams). No element of a stone model emits light.
  live   the knight awake: full colour, its eyes, seams and accents lit (light_emission).

THE RIG (rigkit, as vexis_art / dread_sovereign_art): PARTS = body (the hips, the root), chest, head, armr/forer, arml/forel
(upper arm with its pauldron; forearm with the gauntlet), legr/shinr, legl/shinl (thigh with its tasset; shin with the sabaton),
cape (hung from the back of the chest, kept hanging by the world's down and swung clear of the legs in every pose), mace (in the
RIGHT fist, parented to forer). Thirteen displays per knight. The mace is held two-handed in most poses: the left hand is solved
(ik) onto a point of the haft, so it rides along it. Design units: feet at y=0, facing -z, its right is +x; a design unit is
1/16 block at display scale 1.0 (one texel of the 16 px textures - vanilla's pixel density).

SCALE: RIG_SCALE = 1.0 - a pose at display scale 1.0 stands ~3.0 blocks tall (48 design units, the horns' tips; the helm's top
~2.9). The runtime passes SCALE = 1.0 (= RIG_SCALE), as phase242 does with its SCALE[form]:
    RF.part_nbt(A, p, tags, SCALE, model=A.model_id(p, kind, 'stone'))
    RF.place(A, SCALE / 16, sel)
    RF.pose(A, A.POSES[name], SCALE, dur, sel)
(PART_K: the mace and the cape are built at full size and kept inside the model box shrunk 1/k - rigfol shows them at SCALE*k.)
A different SCALE scales the whole knight (2.5 blocks: 0.83).

NAMES: model_name(part, kind, finish) -> 'bm:kn_dread_live_chest' (the full item model id); model_id(...) the same without
'bm:' (for RF.part_nbt's model=). rigfol / rigkit call model_name(part, pose[, suffix]) - with a pose dict it reads the pose's
'_kind' / '_finish' (posed(name, kind, finish) adds them) and answers without 'bm:', as theirs do.

POSES (POSES[name], one set for both kinds): statue, wake_0, wake_1, idle_a, idle_b, walk_0..3, swing_0, swing_1, spin_0,
spin_1, stagger, death_0, death_1 (see _pose for each). Every pose is grounded (its feet on y=0).

THE TROPHY (statue items): knight_statue_dread, knight_statue_vorn. One item model each, bm:knight_statue_<kind>: an item
definition that selects on the display context - in the inventory (gui, and on a shelf) the 16x16 icon (ICONS[name], drawn in
sprites280's kit: an outline, five stone shades lit from the top left, finished by vanilla.process in gen_rp), everywhere
else the 3D statue (models/item/knight_statue_<kind>.json): the stone knight in the statue pose on a square two-step plinth,
baked into one model, all inside -16..32. PLACING IT: summon an item_display with item_display:'fixed', scale 1.0, no
translation, at the CENTRE OF THE AIR BLOCK above the block clicked (x+0.5, y+1.5, z+0.5 of the clicked block) - the model's
own 'fixed' display (STATUE_FIXED: translation [0, 15, 0]) stands the plinth's base on the block top and the statue ~2.86
blocks tall, the plinth a 1-block square centred on the block. Its front is the model's north, which an item_display turns to
face its own +z (south at yaw 0) - so Rotation:[player_yaw + 180f, 0f] faces it to the player who placed it (or snap it to
the nearest 90). In a hand it is a small statue (thirdperson 0.18, firstperson 0.16, ground 0.2). (Note: an item frame also
uses 'fixed', so a framed statue would show full size - don't let it be framed, or treat that as its frame trick.)

gen_rp hook (in the PHASE2 block, beside phase242):   import knight_art; knight_art.rp(sys.modules[__name__])
"""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import qs, el, seg, shrink, D, qrot, qmul

PREFIX = 'kn_'
KINDS = ('dread', 'vorn')
FINISHES = ('stone', 'live')
RIG_SCALE = 1.0                                 # (the runtime's SCALE: ~3.0 blocks tall)
STATUES = {k: f'knight_statue_{k}' for k in KINDS}
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)

PIVOT = {'body': (0, 22.5, 0), 'chest': (0, 25.5, 0), 'head': (0, 37.5, -0.5),
         'armr': (11.0, 35.0, 0), 'forer': (11.0, 26.0, 0), 'arml': (-11.0, 35.0, 0), 'forel': (-11.0, 26.0, 0),
         'legr': (4.6, 21.5, 0), 'shinr': (4.6, 12.0, 0), 'legl': (-4.6, 21.5, 0), 'shinl': (-4.6, 12.0, 0),
         'cape': (0, 36.0, 5.0), 'mace': (11.0, 15.4, -0.2)}
PARENT = {'body': None, 'chest': 'body', 'head': 'chest', 'armr': 'chest', 'forer': 'armr', 'arml': 'chest', 'forel': 'arml',
          'legr': 'body', 'shinr': 'legr', 'legl': 'body', 'shinl': 'legl', 'cape': 'chest', 'mace': 'forer'}
PARTS = tuple(PIVOT)
PART_K = {'mace': 1.3, 'cape': 1.4}             # (built at full size, kept inside the model box)
GRIP = {1: (11.0, 15.4, -0.2), -1: (-11.0, 15.4, -0.2)}     # (where a haft passes through each fist - the mace's joint is the right one)
MACE_TIP = 26.6                                 # (the mace head's far end, design units from the grip along the haft)


# ---------------------------------------------------------------------------------------------------- names
def model_id(part, kind, finish):
    """the model's id without the namespace: kn_<kind>_<finish>_<part> (RF.part_nbt's model=)"""
    assert kind in KINDS and finish in FINISHES and part in PIVOT, (part, kind, finish)
    return f'{PREFIX}{kind}_{finish}_{part}'


def model_name(part, kind, finish=None):
    """model_name(part, kind, finish) -> 'bm:kn_dread_live_chest'. (rigfol/rigkit's call, model_name(part, pose[, suffix]):
    the pose's _kind/_finish, answered without 'bm:' and with the suffix, as their art modules do)"""
    if isinstance(kind, dict):
        return model_id(part, kind.get('_kind', 'dread'), kind.get('_finish', 'live')) + (finish or '')
    return 'bm:' + model_id(part, kind, finish)


def posed(name, kind, finish='live'):
    """a pose with its kind and finish set (for rigkit.render, or RF.pose(..., swap=PARTS) to swap the finish in the same merge)"""
    return dict(POSES[name], _kind=kind, _finish=finish)


def scale_of(pose):
    return RIG_SCALE


# ---------------------------------------------------------------------------------------------------- textures (16 px: a texel a design unit)
def _rgb(c):
    if isinstance(c, str): c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(c[:3])


def _im(base):
    return Image.new('RGBA', (16, 16), _rgb(base) + (255,))


def _px(im, x, y, c):
    if 0 <= x < 16 and 0 <= y < 16: im.putpixel((x, y), _rgb(c) + (255,))


def _crack(im, rnd, col, n=5, x=None, y=None):
    x = rnd.randrange(2, 14) if x is None else x; y = rnd.randrange(1, 10) if y is None else y
    for _ in range(n):
        _px(im, x, y, col); y += 1; x += rnd.choice((-1, 0, 1))


def _plate(P, seed, rivets=2, dents=0, cracks=0, chips=0, joint=True):
    """a plate of armour: a lit lip along its top, a dark seam under it, a joint, rivets; battered (dents), weathered (cracks,
    chips - the stone finish)"""
    rnd = random.Random(seed); im = _im(P['base']); d = ImageDraw.Draw(im)
    d.line((0, 0, 15, 0), fill=_rgb(P['lip']) + (255,)); d.line((0, 15, 15, 15), fill=_rgb(P['seam']) + (255,))
    if joint:
        x = rnd.randrange(5, 11); d.line((x, 1, x, 14), fill=_rgb(P['seam']) + (255,)); d.line((x + 1, 1, x + 1, 14), fill=_rgb(P['lip']) + (255,))
    for i in range(rivets):
        _px(im, rnd.choice((2, 13)) if i == 0 else rnd.randrange(2, 14), rnd.choice((3, 12)), P['hi'])
    for _ in range(dents):
        x, y = rnd.randrange(1, 13), rnd.randrange(2, 12)
        d.rectangle((x, y, x + 1, y), fill=_rgb(P['seam']) + (255,)); _px(im, x, y - 1, P['lip'])
    for _ in range(cracks): _crack(im, rnd, P['crack'], rnd.randint(3, 6))
    for _ in range(chips):
        x, y = rnd.randrange(0, 15), rnd.randrange(1, 14); _px(im, x, y, P['hi']); _px(im, x + 1, y, P['lip'])
    return im


def _flat(P, top=True, bottom=True):
    im = _im(P['base']); d = ImageDraw.Draw(im)
    if top: d.line((0, 0, 15, 0), fill=_rgb(P['lip']) + (255,))
    if bottom: d.line((0, 15, 15, 15), fill=_rgb(P['seam']) + (255,))
    return im


def _rings(P):
    """bone (a horn, a rib, a spike): growth rings"""
    im = _im(P['base']); d = ImageDraw.Draw(im)
    for y in range(0, 16, 4):
        d.line((0, y, 15, y), fill=_rgb(P['seam']) + (255,)); d.line((0, y + 1, 15, y + 1), fill=_rgb(P['lip']) + (255,))
    return im


def _cloth(P, seed, rips=3):
    """the cloak: vertical folds, a few darker rips"""
    rnd = random.Random(seed); im = _im(P['base']); d = ImageDraw.Draw(im)
    for x in range(0, 16, 4):
        d.line((x + 2, 0, x + 2, 15), fill=_rgb(P['lip']) + (255,)); d.line((x + 3, 0, x + 3, 15), fill=_rgb(P['seam']) + (255,))
    for _ in range(rips):
        x, y = rnd.randrange(0, 16), rnd.randrange(0, 12); d.line((x, y, x, y + rnd.randint(1, 3)), fill=_rgb(P['crack']) + (255,))
    return im


def _grip(P):
    """leather (or ribbed polymer) wound round the haft"""
    im = _im(P['base'])
    for y in range(16):
        for x in range(16):
            if (x + y) % 4 == 0: _px(im, x, y, P['seam'])
            elif (x + y) % 4 == 1: _px(im, x, y, P['lip'])
    return im


def _eye(P):
    """a square eye (whole uv): the lit colour, a pale glint in its top-left quarter (unlit: flat)"""
    im = _im(P['base']); d = ImageDraw.Draw(im)
    if P.get('glint'): d.rectangle((0, 0, 5, 5), fill=_rgb(P['glint']) + (255,))
    return im


def _plinth(P, seed):
    """the plinth's stone: two courses of blocks, mortar lines, chips"""
    rnd = random.Random(seed); im = _im(P['base']); d = ImageDraw.Draw(im)
    for y in (0, 8):
        d.line((0, y, 15, y), fill=_rgb(P['seam']) + (255,)); d.line((0, y + 1, 15, y + 1), fill=_rgb(P['lip']) + (255,))
    for x, y in ((5, 1), (12, 9), (1, 9)):
        d.line((x, y, x, y + 6), fill=_rgb(P['seam']) + (255,))
    for _ in range(4): _px(im, rnd.randrange(16), rnd.randrange(16), P['hi'])
    for _ in range(2): _crack(im, rnd, P['crack'], 3)
    return im


def _ramp(base, lip, seam, hi=None, crack=None, glint=None):
    return dict(base=base, lip=lip, seam=seam, hi=hi or lip, crack=crack or seam, glint=glint)


# the four palettes: PAL[(kind, finish)][material]. Materials: plate (the armour), dark (under-plate, the fist, the hips), trim
# (rims, cops, the belt), bone (dread: horns, ribs, spikes; vorn: the antenna sockets), tip (horn tips / the antennae' froglight),
# stalk (the antennae), accent (red light / green seams - lit when live), eye, slit (the eye-slit's dark, grilles, vents), cloth,
# hem (the cloak's hem), grip (the haft's wrap), iron (the haft, the flanges / fins), plinth (the trophy's base)
_DS = dict(base=(66, 62, 70), lip=(92, 88, 98), seam=(40, 38, 44), hi=(108, 104, 112), crack=(28, 26, 32))       # (blackstone)
_VS = dict(base=(150, 150, 146), lip=(176, 176, 170), seam=(118, 118, 114), hi=(190, 190, 184), crack=(126, 134, 126))  # (hull-stone)
PAL = {
    ('dread', 'live'): dict(
        plate=_ramp((48, 40, 56), (82, 68, 94), (20, 14, 24), (104, 90, 116)),
        dark=_ramp((28, 22, 34), (44, 36, 52), (12, 8, 16)),
        trim=_ramp((88, 84, 100), (128, 124, 140), (48, 44, 58)),
        bone=_ramp((216, 204, 176), (244, 236, 216), (154, 140, 112)),
        tip=_ramp((70, 54, 52), (96, 76, 70), (40, 28, 30)),
        stalk=_ramp((40, 34, 52), (60, 52, 72), (24, 20, 32)),
        accent=_ramp((208, 24, 46), (255, 90, 100), (150, 14, 32)),
        eye=_ramp((232, 30, 50), (255, 120, 120), (180, 20, 40), glint=(255, 150, 140)),
        slit=_ramp((10, 6, 12), (18, 12, 20), (6, 4, 8)),
        cloth=_ramp((36, 22, 32), (54, 34, 48), (20, 12, 18), crack=(12, 6, 10)),
        hem=_ramp((118, 16, 32), (156, 28, 46), (74, 8, 20)),
        grip=_ramp((70, 42, 34), (96, 62, 48), (40, 22, 18)),
        iron=_ramp((70, 68, 82), (112, 110, 126), (38, 36, 46), (130, 128, 142)),
        plinth=_ramp((40, 36, 44), (62, 56, 68), (22, 18, 26))),
    ('dread', 'stone'): dict(
        plate=dict(_DS), dark=_ramp((50, 47, 54), (64, 60, 68), (34, 32, 38)), trim=_ramp((82, 78, 86), (104, 100, 108), (52, 50, 56)),
        bone=_ramp((98, 94, 100), (118, 114, 120), (70, 66, 72)), tip=_ramp((54, 50, 58), (70, 66, 74), (36, 34, 40)),
        stalk=_ramp((54, 50, 58), (70, 66, 74), (36, 34, 40)), accent=_ramp((58, 54, 62), (70, 66, 74), (44, 40, 48)),
        eye=_ramp((34, 32, 38), (40, 38, 44), (28, 26, 32)), slit=_ramp((26, 24, 30), (32, 30, 36), (20, 18, 24)),
        cloth=_ramp((60, 56, 64), (76, 72, 80), (44, 42, 48), crack=(32, 30, 36)), hem=_ramp((52, 48, 56), (66, 62, 70), (38, 36, 42)),
        grip=_ramp((56, 52, 60), (70, 66, 74), (40, 38, 44)), iron=_ramp((72, 68, 78), (96, 92, 102), (46, 44, 50)),
        plinth=_ramp((58, 54, 62), (80, 76, 84), (34, 32, 38), (96, 92, 100), (28, 26, 32))),
    ('vorn', 'live'): dict(
        plate=_ramp((38, 40, 46), (68, 74, 86), (20, 22, 26), (100, 108, 122)),
        dark=_ramp((24, 26, 30), (38, 40, 46), (14, 15, 18)),
        trim=_ramp((100, 108, 122), (138, 148, 162), (68, 74, 86)),
        bone=_ramp((100, 108, 122), (138, 148, 162), (68, 74, 86)),
        tip=_ramp((215, 238, 213), (236, 250, 234), (160, 211, 155)),
        stalk=_ramp((40, 34, 52), (60, 52, 72), (24, 20, 32)),
        accent=_ramp((58, 200, 74), (122, 255, 106), (30, 138, 46)),
        eye=_ramp((60, 255, 80), (190, 255, 190), (40, 200, 60), glint=(216, 255, 210)),
        slit=_ramp((10, 12, 14), (18, 20, 24), (6, 7, 8)),
        cloth=_ramp((28, 34, 32), (44, 52, 48), (14, 18, 16), crack=(8, 10, 9)),
        hem=_ramp((58, 200, 74), (122, 255, 106), (30, 138, 46)),
        grip=_ramp((32, 32, 38), (60, 64, 74), (18, 18, 22)),
        iron=_ramp((68, 74, 86), (100, 108, 122), (42, 46, 54), (138, 148, 162)),
        plinth=_ramp((54, 58, 66), (80, 86, 98), (30, 32, 38))),
    ('vorn', 'stone'): dict(
        plate=dict(_VS), dark=_ramp((128, 128, 124), (142, 142, 138), (108, 108, 104)), trim=_ramp((166, 166, 160), (188, 188, 182), (134, 134, 128)),
        bone=_ramp((166, 166, 160), (188, 188, 182), (134, 134, 128)), tip=_ramp((172, 176, 170), (190, 194, 188), (140, 144, 138)),
        stalk=_ramp((136, 136, 132), (152, 152, 148), (114, 114, 110)), accent=_ramp((124, 132, 124), (138, 146, 138), (110, 116, 110)),
        eye=_ramp((112, 118, 112), (124, 130, 124), (100, 104, 100)), slit=_ramp((98, 98, 96), (110, 110, 106), (86, 86, 84)),
        cloth=_ramp((144, 144, 140), (162, 162, 156), (122, 122, 118), crack=(110, 110, 106)), hem=_ramp((130, 136, 130), (146, 152, 146), (114, 120, 114)),
        grip=_ramp((132, 132, 128), (148, 148, 144), (112, 112, 108)), iron=_ramp((140, 140, 136), (164, 164, 158), (114, 114, 110)),
        plinth=_ramp((132, 132, 128), (160, 160, 154), (100, 100, 98), (176, 176, 170), (92, 96, 92))),
}
MATS = tuple(PAL[('dread', 'live')])
GLOW = {'live': {'accent': 15, 'eye': 15}, 'stone': {}}               # (what emits light, by finish; the vorn's froglight tips and hem too)
GLOW_K = {'vorn': {'tip': 13, 'hem': 12}, 'dread': {}}
NOSHIFT = {'eye'}
_TAG = {('dread', 'live'): 'dl', ('dread', 'stone'): 'ds', ('vorn', 'live'): 'vl', ('vorn', 'stone'): 'vs'}


def tex_name(mat, kind, finish):
    return f'{PREFIX}{_TAG[(kind, finish)]}_{mat}'


def _mat_tex(mat, kind, finish, seed):
    P = PAL[(kind, finish)][mat]; stone = finish == 'stone'
    if mat == 'plate':
        return _plate(P, seed, dents=2 if kind == 'dread' else 0, cracks=(2 if kind == 'dread' else 0) if stone else (1 if kind == 'dread' else 0),
                      chips=2 if stone else 0)
    if mat == 'dark': return _plate(P, seed + 1, rivets=0, joint=False, cracks=1 if stone else 0)
    if mat in ('trim', 'iron'): return _plate(P, seed + 2, rivets=1 if mat == 'trim' else 0, joint=False, dents=1 if kind == 'dread' else 0, cracks=1 if stone else 0)
    if mat == 'bone': return _rings(P) if kind == 'dread' else _flat(P)
    if mat in ('tip', 'stalk', 'accent', 'slit', 'hem'): return _flat(P, top=mat in ('accent', 'hem', 'tip'), bottom=mat != 'slit')
    if mat == 'eye': return _eye(P)
    if mat == 'cloth': return _cloth(P, seed, rips=3 if kind == 'dread' else 1)
    if mat == 'grip': return _grip(P)
    if mat == 'plinth': return _plinth(P, seed)
    raise KeyError(mat)


def textures():
    """{name: 16 x 16 RGBA} - every material of every kind and finish (assets/bm/textures/block)"""
    T = {}
    for (kind, finish) in PAL:
        for i, mat in enumerate(MATS):
            T[tex_name(mat, kind, finish)] = _mat_tex(mat, kind, finish, 7100 + 13 * i + (0 if kind == 'dread' else 500))
    return T


# ---------------------------------------------------------------------------------------------------- building helpers
_rs = random.Random(7)
_PV = [None]


def E(fr, to, mat, **kw):
    """an element (rigkit.el) of a material (the texture key, mapped per kind x finish in models()), its texture window
    shifted at random so neighbouring boxes don't repeat the same patch"""
    if mat in NOSHIFT and 'uv' not in kw: kw['uv'] = {f: [0, 0, 16, 16] for f in ('north', 'south', 'east', 'west', 'up', 'down')}
    elif 'shift' not in kw and 'uv' not in kw: kw['shift'] = (_rs.random(), _rs.random())
    return el(fr, to, mat, _PV[0], **kw)


def BX(sx, x0, x1, y0, y1, z0, z1, mat, rot=None, **kw):
    """a box on side sx (+1 its right, -1 its left): x given for the right side, mirrored (a y or z turn mirrored with it)"""
    a, b = sorted((sx * x0, sx * x1))
    if rot and isinstance(rot[0], str):
        ax, ang, o = rot
        rot = (ax, ang, (sx * o[0], o[1], o[2]))                    # (the angle as given: the caller mirrors it)
    return E((a, y0, z0), (b, y1, z1), mat, rot=rot, **kw)


def CH(pts, ws, mat, up=FRONT, mats=None, ext=0.2):
    """a tapering run of square boxes along a polyline: a horn, a spike, an antenna"""
    n = len(pts) - 1
    if isinstance(ws, tuple): ws = [ws[0] + (ws[1] - ws[0]) * i / max(1, n - 1) for i in range(n)]
    return [seg(pts[i], pts[i + 1], ws[i], ws[i], (mats[i] if mats else mat), _PV[0], up, ext, shift=(_rs.random(), _rs.random())) for i in range(n)]


# ---------------------------------------------------------------------------------------------------- the parts (design units)
def _head(kind):
    H = [E((-4.0, 35.6, -4.2), (4.0, 37.6, 3.6), 'dark')]                                    # (the bevor, in the gorget)
    if kind == 'dread':
        H += [E((-4.4, 37.4, -4.4), (4.4, 45.4, 3.8), 'plate'), E((-3.8, 45.4, -3.8), (3.8, 46.2, 3.2), 'plate'),
              E((-4.6, 37.2, -5.2), (4.6, 41.2, -4.4), 'plate'), E((-4.6, 42.6, -5.2), (4.6, 45.6, -4.4), 'plate'),
              E((-4.2, 41.2, -4.9), (4.2, 42.6, -4.45), 'slit'),                                # (the eye-slit: dark, recessed)
              E((-4.8, 42.6, -5.5), (4.8, 43.2, -5.0), 'trim'),                                 # (the brow's ridge over it)
              E((-0.5, 37.4, -5.6), (0.5, 41.2, -5.1), 'trim'),                                 # (the nasal ridge)
              E((-0.6, 46.2, -3.6), (0.6, 47.0, 3.0), 'trim'),                                  # (the crest)
              E((-4.2, 36.4, 3.6), (4.2, 39.6, 4.6), 'plate')]                                  # (the neck guard)
        for sx in (1, -1):
            H += [BX(sx, 3.8, 4.6, 41.2, 42.6, -5.2, -4.4, 'plate'),                            # (the slit's ends)
                  BX(sx, 1.2, 2.4, 41.4, 42.4, -5.0, -4.85, 'eye'),                            # (a square red eye in the slit)
                  BX(sx, 1.4, 2.0, 38.0, 38.6, -5.3, -5.15, 'slit'), BX(sx, 2.6, 3.2, 38.0, 38.6, -5.3, -5.15, 'slit'),
                  BX(sx, 1.4, 2.0, 39.4, 40.0, -5.3, -5.15, 'slit'), BX(sx, 2.6, 3.2, 39.4, 40.0, -5.3, -5.15, 'slit'),   # (breaths)
                  BX(sx, 4.2, 5.2, 42.4, 44.8, -1.8, 0.8, 'trim')]                              # (the horn's root)
            H += CH([(sx * 4.8, 43.6, -0.5), (sx * 6.6, 44.2, -0.2), (sx * 7.7, 45.9, 0.3), (sx * 7.5, 48.0, 0.9)],
                    [2.0, 1.6, 1.1], 'bone', mats=['bone', 'bone', 'tip'])
    else:
        H += [E((-4.3, 37.4, -4.3), (4.3, 45.0, 3.8), 'plate'), E((-3.6, 45.0, -3.6), (3.6, 45.8, 3.2), 'plate'),
              E((-4.5, 37.2, -5.0), (4.5, 39.8, -4.3), 'plate'), E((-4.5, 43.6, -5.0), (4.5, 45.2, -4.3), 'plate'),
              E((-3.2, 39.8, -4.75), (3.2, 43.6, -4.35), 'accent'),                            # (the square visor)
              E((-4.35, 39.5, -4.35), (4.35, 39.8, 3.85), 'accent'),                           # (a seam round the jaw)
              E((-4.6, 43.6, -5.2), (4.6, 44.1, -4.9), 'trim'),                                # (the visor's brow)
              E((-1.8, 37.8, -5.1), (1.8, 38.2, -4.95), 'slit'), E((-1.8, 38.7, -5.1), (1.8, 39.1, -4.95), 'slit'),   # (the grille)
              E((-4.2, 36.4, 3.6), (4.2, 39.6, 4.6), 'plate')]
        for sx in (1, -1):
            H += [BX(sx, 3.2, 4.5, 39.8, 43.6, -5.0, -4.3, 'plate'),
                  BX(sx, 0.8, 2.4, 40.9, 42.5, -4.85, -4.7, 'eye'),                            # (two bright square eyes in it)
                  BX(sx, 4.3, 4.8, 39.6, 43.4, -2.6, 1.6, 'trim'),                             # (the ear plates)
                  BX(sx, 1.8, 3.0, 45.6, 46.2, -0.6, 0.6, 'bone')]                             # (the antenna's socket)
            H += CH([(sx * 2.4, 45.8, 0.0), (sx * 2.9, 47.2, 0.3), (sx * 3.5, 48.3, 0.6)], [0.7, 0.55], 'stalk')
            H.append(E((sx * 3.6 - 0.6, 48.2, 0.05), (sx * 3.6 + 0.6, 49.2, 1.25), 'tip'))
    return H


KEEL = lambda sx: ('y', -sx * 10, (0, 32, -5.6))


def _chest(kind):
    C = [E((-7.4, 25.0, -4.4), (7.4, 36.6, 4.4), 'dark'), E((-7.6, 25.6, 4.4), (7.6, 36.2, 5.2), 'plate'),
         E((-6.6, 25.2, -5.0), (6.6, 26.8, -4.4), 'plate'), E((-6.8, 26.6, -5.1), (6.8, 27.8, -4.4), 'plate'),
         E((-7.0, 27.6, -5.2), (7.0, 28.4, -4.4), 'trim'), E((-5.4, 35.6, -4.6), (5.4, 37.0, 4.4), 'trim')]
    for sx in (1, -1):
        C.append(BX(sx, 0, 8.0, 28.2, 36.2, -5.6, -4.4, 'plate', rot=KEEL(1) if sx > 0 else KEEL(-1)))
    if kind == 'dread':
        C += [E((-0.6, 28.4, -6.0), (0.6, 36.0, -5.3), 'bone'),                                  # (the sternum)
              E((-0.9, 33.0, -6.25), (0.9, 34.8, -5.95), 'accent')]                             # (a red jewel at its top)
        for sx in (1, -1):
            for i, y in enumerate((29.6, 31.4, 33.2)):
                C.append(BX(sx, 0.8, 6.4 - 0.5 * i, y, y + 0.9, -5.95, -5.5, 'bone', rot=KEEL(sx)))      # (bone ribs over the breast)
        C.append(E((-7.45, 33.9, 4.4), (7.45, 34.2, 5.25), 'accent'))                          # (a crack of red light across the back)
    else:
        C += [E((-0.3, 28.4, -5.8), (0.3, 32.0, -5.55), 'accent'),                              # (a green seam down the keel)
              E((-1.7, 32.0, -5.8), (1.7, 35.2, -5.5), 'trim'), E((-1.2, 32.4, -6.0), (1.2, 34.8, -5.7), 'accent'),   # (the node)
              E((-7.45, 27.9, -4.45), (7.45, 28.2, 4.45), 'accent')]                            # (and round the waist)
        for sx in (1, -1):
            C.append(BX(sx, 2.2, 7.2, 30.4, 30.7, -5.75, -5.5, 'accent', rot=KEEL(sx)))
            C.append(BX(sx, 2.0, 6.0, 30.0, 30.5, 5.2, 5.3, 'slit')); C.append(BX(sx, 2.0, 6.0, 31.2, 31.7, 5.2, 5.3, 'slit'))  # (vents)
    return C


def _body(kind):
    B = [E((-6.6, 18.4, -4.0), (6.6, 23.2, 4.0), 'dark'), E((-7.4, 21.0, -4.7), (7.4, 23.4, 4.7), 'trim'),
         E((-2.2, 16.6, -4.6), (2.2, 21.0, -3.8), 'plate'), E((-6.2, 17.6, 3.8), (6.2, 21.0, 4.8), 'plate')]
    if kind == 'dread':
        B += [E((-1.4, 20.6, -5.2), (1.4, 23.8, -4.6), 'bone'), E((-0.5, 21.6, -5.35), (0.5, 22.8, -5.15), 'accent')]
    else:
        B += [E((-1.4, 20.6, -5.2), (1.4, 23.8, -4.6), 'plate'), E((-0.7, 21.5, -5.35), (0.7, 22.9, -5.15), 'accent'),
              E((-7.45, 22.0, -4.75), (7.45, 22.3, 4.75), 'accent')]
    return B


def _leg(sx, kind):
    L = [BX(sx, 2.4, 6.8, 12.6, 21.6, -2.4, 2.4, 'dark'), BX(sx, 2.2, 7.0, 13.6, 20.2, -2.9, -2.3, 'plate'),
         BX(sx, 6.8, 7.5, 13.6, 21.0, -2.6, 2.2, 'plate'),
         BX(sx, 1.8, 7.8, 17.0, 21.4, -3.7, -2.9, 'plate'), BX(sx, 1.9, 7.7, 16.4, 17.2, -3.6, -2.8, 'trim')]
    L.append(BX(sx, 4.2, 4.5, 14.4, 17.0, -2.95, -2.85, 'accent') if kind == 'dread' else BX(sx, 2.0, 7.6, 17.2, 17.5, -3.75, -3.65, 'accent'))
    return L


def _shin(sx, kind):
    S = [BX(sx, 2.2, 7.0, 10.4, 13.8, -3.4, -2.0, 'trim'),
         BX(sx, 2.5, 6.7, 2.6, 11.2, -2.6, 2.4, 'plate'), BX(sx, 4.1, 5.1, 3.0, 10.4, -3.0, -2.5, 'trim'),
         BX(sx, 2.1, 7.1, 0.0, 3.0, -3.8, 2.8, 'dark'), BX(sx, 2.3, 6.9, 0.0, 2.2, -6.6, -3.8, 'plate'),
         BX(sx, 2.4, 6.8, 2.2, 2.8, -5.6, -3.6, 'trim')]
    if kind == 'dread':
        S += CH([(sx * 4.6, 12.2, -3.2), (sx * 4.6, 13.0, -4.6), (sx * 4.6, 14.0, -5.4)], [1.1, 0.7], 'bone', mats=['bone', 'tip'])
    else:
        S.append(BX(sx, 4.0, 5.2, 11.6, 12.8, -3.55, -3.35, 'accent'))
    return S


def _arm(sx, kind):
    A = [BX(sx, 9.4, 12.6, 26.4, 34.0, -1.9, 1.9, 'dark'), BX(sx, 9.2, 12.8, 27.2, 31.4, -2.2, 2.2, 'plate'),
         BX(sx, 7.8, 15.4, 31.0, 37.4, -4.6, 4.6, 'plate'), BX(sx, 8.8, 14.4, 37.4, 38.4, -3.6, 3.6, 'trim'),
         BX(sx, 9.0, 16.0, 29.4, 31.4, -4.2, 4.2, 'plate', rot=('z', -sx * 14, (9.0, 31.4, 0))),
         BX(sx, 9.2, 16.2, 28.8, 29.5, -4.0, 4.0, 'trim', rot=('z', -sx * 14, (9.0, 31.4, 0))),
         BX(sx, 7.75, 15.45, 33.9, 34.2, -4.65, 4.65, 'accent')]
    if kind == 'dread':
        for z in (-1.8, 1.8):
            A += CH([(sx * 12.0, 38.0, z), (sx * 13.4, 40.0, z * 1.15), (sx * 14.4, 41.6, z * 1.3)], [1.4, 0.9], 'bone', mats=['bone', 'tip'])
    else:
        A.append(BX(sx, 15.4, 15.8, 32.4, 35.6, -2.4, 2.4, 'slit'))
    return A


def _fore(sx, kind):
    F = [BX(sx, 9.0, 13.0, 23.8, 27.0, -1.6, 2.8, 'trim'), BX(sx, 12.6, 13.4, 23.6, 26.6, -1.4, 2.0, 'trim'),
         BX(sx, 9.3, 12.7, 18.6, 24.4, -2.0, 2.0, 'plate'), BX(sx, 8.8, 13.2, 17.4, 19.6, -2.5, 2.5, 'trim'),
         BX(sx, 9.2, 12.8, 13.4, 17.4, -2.0, 2.0, 'dark'), BX(sx, 9.1, 12.9, 14.4, 16.8, -2.5, -1.9, 'plate'),
         BX(sx, 8.6, 9.3, 14.6, 16.6, -1.6, 0.6, 'plate'),
         BX(sx, 8.75, 13.25, 18.9, 19.15, -2.55, 2.55, 'accent')]
    return F


def _cape(kind):
    C = [E((-7.0, 34.6, 5.0), (7.0, 36.6, 6.2), 'trim')]
    if kind == 'dread':
        for sx in (1, -1): C.append(BX(sx, 5.2, 6.8, 34.4, 36.8, 6.0, 6.6, 'bone'))
    else:
        for sx in (1, -1): C.append(BX(sx, 5.2, 6.8, 34.4, 36.8, 6.0, 6.6, 'accent'))
    LEN = (27.4, 29.6, 26.4, 30.0, 27.8)
    for i, ln in enumerate(LEN):
        x0 = -7.5 + 3.0 * i; yb = 35.4 - ln; dz = 0.06 * (i % 2)
        C += [E((x0, yb + 1.6, 5.3 + dz), (x0 + 3.0, 35.4, 6.0 + dz), 'cloth'),
              E((x0, yb, 5.25 + dz), (x0 + 3.0, yb + 1.6, 6.05 + dz), 'hem')]
        if i % 2 == 0:                                                                          # (a rag hanging below the hem)
            C.append(E((x0 + 0.6 + 0.4 * (i % 3), yb - 1.4, 5.35 + dz), (x0 + 1.8 + 0.4 * (i % 3), yb, 5.95 + dz), 'hem'))
    return C


def _mace(kind):
    X, Y, Z = PIVOT['mace']; M = []
    M += [E((X - 0.8, Y - 0.8, Z - 15.8), (X + 0.8, Y + 0.8, Z + 6.9), 'iron'),                # (the haft, along -z to the head)
          E((X - 0.9, Y - 0.9, Z - 6.0), (X + 0.9, Y + 0.9, Z + 6.0), 'grip'),                 # (the wrap, where the hands go)
          E((X - 1.4, Y - 1.4, Z + 6.8), (X + 1.4, Y + 1.4, Z + 8.4), 'trim'),                 # (the pommel)
          E((X - 0.7, Y - 0.7, Z + 8.4), (X + 0.7, Y + 0.7, Z + 9.2), 'accent'),
          E((X - 1.5, Y - 1.5, Z - 16.4), (X + 1.5, Y + 1.5, Z - 15.0), 'trim')]               # (the collar under the head)
    zc = Z - 19.6
    if kind == 'dread':
        M += [E((X - 2.6, Y - 2.6, Z - 23.6), (X + 2.6, Y + 2.6, Z - 15.6), 'dark'),
              E((X - 2.7, Y - 2.7, Z - 20.0), (X + 2.7, Y + 2.7, Z - 19.3), 'accent'),         # (a band of red light round it)
              E((X - 2.0, Y - 2.0, Z - 24.6), (X + 2.0, Y + 2.0, Z - 23.6), 'trim')]
        for sgn in (1, -1):                                                                     # (eight flanges, stepped)
            for ax in ('x', 'y'):
                def fl(r0, r1, z0, z1, mat):
                    if ax == 'y': return E((X - 0.45, Y + sgn * r0 if sgn > 0 else Y - r1, z0), (X + 0.45, Y + r1 if sgn > 0 else Y - r0, z1), mat)
                    return E((X + r0 if sgn > 0 else X - r1, Y - 0.45, z0), (X + r1 if sgn > 0 else X - r0, Y + 0.45, z1), mat)
                M += [fl(2.0, 4.2, Z - 23.0, Z - 16.2, 'iron'), fl(4.2, 5.2, Z - 22.0, Z - 17.4, 'trim')]
            for ang in (45, -45):
                M += [E((X - 0.45, Y + sgn * 2.0 if sgn > 0 else Y - 4.2, Z - 23.0), (X + 0.45, Y + 4.2 if sgn > 0 else Y - 2.0, Z - 16.2), 'iron', rot=('z', ang, (X, Y, zc))),
                      E((X - 0.45, Y + 4.2 if sgn > 0 else Y - 5.2, Z - 22.0), (X + 0.45, Y + 5.2 if sgn > 0 else Y - 4.2, Z - 17.4), 'trim', rot=('z', ang, (X, Y, zc)))]
        M += CH([(X, Y, Z - 24.4), (X, Y, Z - 25.6), (X, Y, Z - MACE_TIP)], [1.8, 1.0], 'bone', up=UP, mats=['bone', 'tip'], ext=0.1)
    else:
        M += [E((X - 2.8, Y - 2.8, Z - 23.6), (X + 2.8, Y + 2.8, Z - 15.6), 'plate'),
              E((X - 2.8, Y - 2.8, Z - 23.5), (X + 2.8, Y + 2.8, Z - 15.7), 'plate', rot=('z', 45, (X, Y, zc))),    # (octagonal)
              E((X - 2.2, Y - 2.2, Z - 24.6), (X + 2.2, Y + 2.2, Z - 23.6), 'trim'),
              E((X - 1.1, Y - 1.1, Z - MACE_TIP + 0.2), (X + 1.1, Y + 1.1, Z - 24.6), 'accent'),                    # (the emitter)
              E((X - 0.85, Y + 0.75, Z - 15.0), (X + 0.85, Y + 0.95, Z - 6.0), 'accent')]                           # (a seam up the haft)
        for sgn in (1, -1):
            M += [E((X - 0.5, Y + 2.6 if sgn > 0 else Y - 4.4, Z - 22.6), (X + 0.5, Y + 4.4 if sgn > 0 else Y - 2.6, Z - 16.6), 'accent'),   # (plasma ridges)
                  E((X + 2.6 if sgn > 0 else X - 4.4, Y - 0.5, Z - 22.6), (X + 4.4 if sgn > 0 else X - 2.6, Y + 0.5, Z - 16.6), 'accent')]
            for ang in (45, -45):
                M.append(E((X - 0.4, Y + 2.6 if sgn > 0 else Y - 3.9, Z - 22.0), (X + 0.4, Y + 3.9 if sgn > 0 else Y - 2.6, Z - 17.2), 'trim', rot=('z', ang, (X, Y, zc))))
        M += [E((X - 2.9, Y - 2.9, Z - 16.5), (X + 2.9, Y + 2.9, Z - 15.9), 'accent'), E((X - 2.9, Y - 2.9, Z - 23.3), (X + 2.9, Y + 2.9, Z - 22.7), 'accent')]
    return M


# ---------------------------------------------------------------------------------------------------- models
_RAW = {}


def _build():
    """{kind: {part: [elements (material keys as textures)]}} - geometry, full size"""
    if _RAW: return _RAW
    for kind in KINDS:
        _rs.seed(7 if kind == 'dread' else 8)
        def mk(part, fn, *a):
            _PV[0] = PIVOT[part]; return fn(*a)
        R = {'head': mk('head', _head, kind), 'chest': mk('chest', _chest, kind), 'body': mk('body', _body, kind),
             'cape': mk('cape', _cape, kind), 'mace': mk('mace', _mace, kind)}
        for sx, s in ((1, 'r'), (-1, 'l')):
            R[f'arm{s}'] = mk(f'arm{s}', _arm, sx, kind); R[f'fore{s}'] = mk(f'fore{s}', _fore, sx, kind)
            R[f'leg{s}'] = mk(f'leg{s}', _leg, sx, kind); R[f'shin{s}'] = mk(f'shin{s}', _shin, sx, kind)
        _RAW[kind] = R
    return _RAW


def _finish(els, kind, finish):
    """the geometry's materials as a kind x finish's textures; light_emission where that finish lights them"""
    glow = dict(GLOW[finish], **(GLOW_K[kind] if finish == 'live' else {}))
    out = []
    for e in els:
        e = dict(e, faces={f: dict(fc, texture='#' + tex_name(fc['texture'][1:], kind, finish)) for f, fc in e['faces'].items()})
        e.pop('light_emission', None)
        mats = {fc['texture'][1:] for fc in e['faces'].values()}
        lt = max([glow.get(m.split('_', 2)[-1], 0) for m in mats] + [0])
        if lt: e['light_emission'] = lt
        out.append(e)
    return out


def models():
    """{model id (no namespace): (textures, elements)} - every part x kind x finish, as gen_rp's HATS take them"""
    M = {}
    for kind, parts in _build().items():
        for part, els in parts.items():
            k = PART_K.get(part, 1.0)
            els = shrink(els, k) if k != 1.0 else els
            for finish in FINISHES:
                fe = _finish(els, kind, finish)
                for e in fe:
                    for v in e['from'] + e['to']:
                        assert -16 <= v <= 32, (part, kind, e['from'], e['to'])
                    for fc in e['faces'].values():
                        assert all(0.0 <= t <= 16.0 for t in fc['uv']), (part, fc['uv'])
                used = sorted({fc['texture'][1:] for e in fe for fc in e['faces'].values()})
                M[model_id(part, kind, finish)] = ({t: f'bm:block/{t}' for t in used}, fe)
    return M


# ---------------------------------------------------------------------------------------------------- world geometry (grounding, the hands, clip checks)
def _rotm(r):
    def rx(a): c, s = math.cos(a), math.sin(a); return [[1, 0, 0], [0, c, -s], [0, s, c]]
    def ry(a): c, s = math.cos(a), math.sin(a); return [[c, 0, s], [0, 1, 0], [-s, 0, c]]
    def rz(a): c, s = math.cos(a), math.sin(a); return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    if 'axis' in r: return {'x': rx, 'y': ry, 'z': rz}[r['axis']](math.radians(r['angle']))
    return mm(mm(rz(math.radians(r.get('z', 0))), ry(math.radians(r.get('y', 0)))), rx(math.radians(r.get('x', 0))))


def world_boxes(pose, parts=None, kind='dread', xf=None):
    """{part: [(centre, (axis, axis, axis), half extents)]} - each element as an oriented box in the world (display frame,
    design units), as the pose stands"""
    raw = _build()[kind]; xf = xf or rigkit.solve(PIVOT, PARENT, pose); out = {}
    for p in (parts or PARTS):
        Q, t = xf[p]; pv = PIVOT[p]; dp = D(pv); W = tuple(t[i] + dp[i] for i in range(3))
        bl = []
        for e in raw[p]:
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            ax = [(1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)]
            if 'rotation' in e:
                R = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
                ax = [tuple(R[i][j] for i in range(3)) for j in range(3)]
            cd = tuple(c[i] - 8 + pv[i] for i in range(3))                                     # (model -> design)
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


def _sat(a, b):
    """how deep two oriented boxes cut into each other (0 if apart)"""
    ca, aa, ha = a; cb, ab, hb = b; t = [cb[i] - ca[i] for i in range(3)]; best = 1e9
    axes = list(aa) + list(ab) + [rigkit._cross(u, v) for u in aa for v in ab]
    for L in axes:
        n = math.sqrt(sum(v * v for v in L))
        if n < 1e-6: continue
        L = [v / n for v in L]
        dt = lambda u: sum(u[i] * L[i] for i in range(3))
        o = sum(ha[i] * abs(dt(aa[i])) for i in range(3)) + sum(hb[i] * abs(dt(ab[i])) for i in range(3)) - abs(dt(t))
        if o <= 0: return 0.0
        best = min(best, o)
    return best


def penetration(pose, pa, pb, kind='dread'):
    """the deepest cut of any element of parts pa into any of parts pb"""
    wb = world_boxes(pose, tuple(pa) + tuple(pb), kind); d = 0.0
    for a in pa:
        for b in pb:
            for ea in wb[a]:
                for eb in wb[b]:
                    if sum((ea[0][i] - eb[0][i]) ** 2 for i in range(3)) > (sum(ea[2]) + sum(eb[2])) ** 2: continue
                    d = max(d, _sat(ea, eb))
    return d


def at(pose, part, p, xf=None):
    """where a design point carried by `part` stands in the world (design units), as the pose stands"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); Q, t = xf[part]; pv = D(PIVOT[part])
    r = qrot(Q, tuple(D(p)[i] - pv[i] for i in range(3)))
    return D(tuple(t[i] + pv[i] + r[i] for i in range(3)))


def local(pose, part, w, xf=None):
    """a world point (design units) in a part's rest frame (design units) - the inverse of at()"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); Q, t = xf[part]; pv = D(PIVOT[part])
    qi = (-Q[0], -Q[1], -Q[2], Q[3]); dw = D(w)
    r = qrot(qi, tuple(dw[i] - t[i] - pv[i] for i in range(3)))
    return D(tuple(pv[i] + r[i] for i in range(3)))


def axis(pose, part, v, xf=None):
    """a direction carried by a part (design frame) in the world (design frame)"""
    xf = xf or rigkit.solve(PIVOT, PARENT, pose); return D(qrot(xf[part][0], D(v)))


GROUND_PARTS = ('body', 'legr', 'legl', 'shinr', 'shinl')


def ground(pose, parts=GROUND_PARTS):
    """set the root's height so the lowest point of these parts rests on y=0"""
    pose = dict(pose); o = pose.get('_off', (0.0, 0.0, 0.0)); pose['_off'] = (o[0], 0.0, o[2])
    lo = lowest(pose, parts); pose['_off'] = (o[0], round(-lo, 4), o[2])
    return pose


# ---------------------------------------------------------------------------------------------------- posing kit
# (rigkit, display frame: ('x', +a) leans a trunk forward / nods the head down; limb(fwd) swings a hanging limb forward, (out)
#  out to its own side and up, (turn) about its own length; a shin bends back with knee(a); ('y', +a) on the chest turns its
#  right shoulder forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def knee(a):
    return qs(('x', a))


def T(lean=0.0, twist=0.0, side=0.0):
    return qs(('y', twist), ('x', lean), ('z', side))


def qa_x(d):
    return rigkit.qa('x', d)


def _unit(v):
    n = math.sqrt(sum(c * c for c in v)); return tuple(c / n for c in v)


def _mat2q(m):
    """a rotation matrix (rows) -> quaternion (x, y, z, w)"""
    tr = m[0][0] + m[1][1] + m[2][2]
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2; return ((m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, 0.25 * s)
    if m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1.0 + m[0][0] - m[1][1] - m[2][2]) * 2; return (0.25 * s, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s)
    if m[1][1] > m[2][2]:
        s = math.sqrt(1.0 + m[1][1] - m[0][0] - m[2][2]) * 2; return ((m[0][1] + m[1][0]) / s, 0.25 * s, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s)
    s = math.sqrt(1.0 + m[2][2] - m[0][0] - m[1][1]) * 2; return ((m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, 0.25 * s, (m[1][0] - m[0][1]) / s)


def _aim_q(dirw, upw):
    """the world turn (display frame) that lays the mace's haft along dirw (design frame: grip -> head) with its 'up' as near upw"""
    z = _unit(D(dirw)); u = D(upw)
    k = sum(u[i] * z[i] for i in range(3)); y = _unit(tuple(u[i] - k * z[i] for i in range(3)))
    x = rigkit._cross(y, z)
    return _mat2q([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])


def _conj(q):
    return (-q[0], -q[1], -q[2], q[3])


def _ik_arm(pose, sx, target, haft, guesses):
    """bend one arm (arm + fore: fwd, out, turn, elbow, wrist turn) so its fist's grip lands on target (world, design units) with
    the haft across the fist (along its own length, as it rests in the right fist), the elbow kept out of the trunk"""
    from scipy.optimize import minimize
    s = 'r' if sx > 0 else 'l'; a, f = f'arm{s}', f'fore{s}'
    base = dict(pose)
    def build(v):
        p = dict(base); p[a] = limb(sx, v[0], v[1], v[2]); p[f] = limb(sx, v[3], 0.0, v[4]); return p
    def cost(v):
        p = build(v); xf = rigkit.solve(PIVOT, PARENT, p)
        g = at(p, f, GRIP[sx], xf); c = sum((g[i] - target[i]) ** 2 for i in range(3))
        fa = axis(p, f, (0.0, 0.0, -1.0), xf); dd = sum(fa[i] * haft[i] for i in range(3))
        c += 6.0 * (1 - dd * dd)
        if v[3] < 0: c += 0.05 * v[3] ** 2                                                       # (elbows don't bend backward)
        if v[3] > 135: c += 0.05 * (v[3] - 135) ** 2
        c += 0.0004 * (v[2] ** 2 + v[4] ** 2)
        for pt in (at(p, f, PIVOT[f], xf), at(p, f, (sx * 11.0, 20.0, 0.0), xf)):          # (the elbow, the forearm: out of the trunk)
            lc = local(p, 'chest', pt, xf)
            if abs(lc[0]) < 8.8 and -6.2 < lc[2] < 6.0 and 23.5 < lc[1] < 38.5:
                c += 2.0 * min(8.8 - abs(lc[0]), lc[2] + 6.2) ** 2
        return c
    best = None
    for g0 in guesses:
        r = minimize(cost, g0, method='Powell', options={'xtol': 1e-3, 'ftol': 1e-6, 'maxfev': 6000})
        if best is None or r.fun < best.fun: best = r
    p = build(best.x)
    g = at(p, f, GRIP[sx]); err = math.sqrt(sum((g[i] - target[i]) ** 2 for i in range(3)))
    return p, err


GUESS = [(30, 10, 0, 50, 0), (70, 15, 20, 50, 0), (100, 5, 30, 30, 0), (140, 10, 0, 30, 0), (10, 45, 0, 70, 0), (40, -15, -30, 80, 0),
         (60, 30, -40, 70, 20), (90, 40, 10, 10, 0), (20, 70, 0, 20, 0)]


def _to_world(pose, frame, v, point=True):
    if frame == 'w': return tuple(v)
    return at(pose, 'chest', v) if point else axis(pose, 'chest', v)


def hold(pose, grip, haft, frame='c', up=None, left=None, floor=None, lframe=None):
    """the right fist on the haft at `grip`, the haft laid along `haft` (grip -> head), both in the chest's frame ('c', design
    units as the chest stands at rest - they move with the trunk) or the world's ('w'); left: where the left hand rides (design
    units along the haft from the right fist, + toward the head) - None leaves the left arm as the pose has it; floor: the mace
    head's lowest point brought to this height (the right fist moved up or down to put it there)"""
    p = dict(pose); err = 0.0
    for it in range(4 if floor is not None else 1):
        G = _to_world(p, frame, grip); H = _unit(_to_world(p, frame, haft, point=False))
        p, err = _ik_arm(p, 1, G, H, GUESS)
        xf = rigkit.solve(PIVOT, PARENT, p)
        u = up or ((0.0, 0.0, -1.0) if abs(H[1]) > 0.85 else (0.0, 1.0, 0.0))
        Qm = _aim_q(H, _to_world(p, frame, u, point=False) if frame == 'c' and up else u)
        p['mace'] = qmul(_conj(xf['forer'][0]), Qm)
        if floor is None: break
        lo = lowest(p, ('mace',)); dy = floor - lo
        if abs(dy) < 0.05: break
        if frame == 'c':
            dl = local(p, 'chest', tuple(G[i] + (0, dy, 0)[i] for i in range(3)))
            grip = dl
        else:
            grip = (grip[0], grip[1] + dy, grip[2])
    p['_err_r'] = round(err, 2)
    if left is not None:
        G = at(p, 'mace', GRIP[1]); H = axis(p, 'mace', (0.0, 0.0, -1.0))
        L = tuple(G[i] + H[i] * left for i in range(3))
        p, err = _ik_arm(p, -1, L, H, GUESS)
        p['_err_l'] = round(err, 2)
    return p


def hang(p, flow=0.0):
    """the cloak hangs by the world's down whatever the chest is doing (flow: swept back), then is swung back until its hem
    clears the floor and it no longer cuts into the legs"""
    p = dict(p)
    Qc = rigkit.solve(PIVOT, PARENT, p)['chest'][0]; u = qrot(Qc, (0.0, 1.0, 0.0))
    pitch = math.degrees(math.atan2(u[2], u[1]))
    p['cape'] = qmul(qa_x(-pitch + flow), p.get('cape', rigkit.I))
    for _ in range(30):
        if lowest(p, ('cape',)) >= 0.5 and penetration(p, ('cape',), ('legr', 'legl', 'shinr', 'shinl', 'body')) < 0.3: break
        p['cape'] = qmul(qa_x(3.0), p['cape'])
    return p


def P(**kw):
    return kw


s_ = math.sin
STAND = dict(legr=limb(1, 0, 3), shinr=limb(1, 0, -3), legl=limb(-1, 0, 3), shinl=limb(-1, 0, -3))
WIDE = dict(legr=limb(1, 14, 7), shinr=knee(16), legl=limb(-1, -10, 7), shinl=knee(12))


def _pose(name):
    """one pose (both kinds share them)"""
    if name == 'statue':                                      # (a proud sentinel: the mace head-down before it, both gauntlets on the pommel, head bowed)
        p = ground(P(chest=T(1), head=T(13), **STAND))
        p = hold(p, (1.4, 26.0, -11.0), (0.0, -1.0, 0.0), 'w', left=-4.2, floor=0.0)
        p = hang(p)
    elif name == 'wake_0':                                    # (the head lifts, the hands tighten on the haft - the left slides down beside the right)
        p = ground(P(chest=T(0), head=T(-3), **STAND))
        p = hold(p, (1.4, 26.0, -11.0), (0.0, -1.0, -0.06), 'w', left=4.2, floor=0.4)
        p = hang(p)
    elif name == 'wake_1':                                    # (it hefts the mace up across its body, its right foot forward)
        p = ground(P(chest=T(4, 12), head=T(0, -12), legr=limb(1, 24, 4), shinr=knee(16), legl=limb(-1, -12, 4), shinl=knee(10)))
        p = hold(p, (5.0, 25.0, -9.5), (-0.62, 0.72, -0.3), 'c', left=10.0)
        p = hang(p)
    elif name in ('idle_a', 'idle_b'):                        # (a battle stance: the mace two-handed at the ready, its head up by the right shoulder)
        b = name == 'idle_b'                                  # (b: the breath in - the chest up, the head lifted, the mace a touch higher)
        p = ground(P(chest=T(5 if b else 8, -8), head=T(-2 if b else 2, 8), **WIDE))
        p = hold(p, (4.0, 24.4 if b else 23.4, -10.0), (0.42, 0.82, -0.38), 'c', left=8.0)
        p = hang(p, 4)
    elif name.startswith('walk_'):                            # (heavy, stomping: the mace carried over the right shoulder, the left arm swinging)
        k = int(name[-1]); ph = math.pi * k / 2; sw = s_(ph)
        p = ground(P(chest=T(8, 5 * sw, 2 * sw), head=T(4, -4 * sw), legr=limb(1, 22 * sw, 4), shinr=knee(8 + 34 * max(0, -s_(ph + 0.6))),
                     legl=limb(-1, -22 * sw, 4), shinl=knee(8 + 34 * max(0, s_(ph + 0.6))),
                     arml=limb(-1, 6 + 20 * sw, 10), forel=limb(-1, 24 + 8 * sw)))
        p['_off'] = (p['_off'][0], p['_off'][1] + 0.6 * abs(math.cos(ph)), p['_off'][2])      # (the stomp: down on the planted foot)
        p = hold(p, (6.6, 34.8, -7.6), (0.05, 0.45, 0.89), 'c', up=(1.0, 0.0, 0.0))
        p = hang(p, 6)
    elif name == 'swing_0':                                   # (the wind-up: the mace raised high overhead in both hands, leaning back)
        p = ground(P(chest=T(-14, 6), head=T(-8), legr=limb(1, 22, 6), shinr=knee(22), legl=limb(-1, -16, 6), shinl=knee(10)))
        p = hold(p, (2.0, 47.0, 1.5), (0.0, 0.5, 0.87), 'c', left=4.6)
        p = hang(p, 8)
    elif name == 'swing_1':                                   # (the slam: the head driven down into the ground ~2 blocks before it, bent over the blow)
        p = ground(P(chest=T(34, -6), head=T(-12), legr=limb(1, 44, 6), shinr=knee(52), legl=limb(-1, -22, 6), shinl=knee(14)))
        p = hold(p, (1.2, 16.0, -14.0), (0.0, -0.42, -0.91), 'w', left=4.6, floor=0.0)
        p = hang(p, 10)
    elif name in ('spin_0', 'spin_1'):                        # (the spin: the mace held out level at full stretch to its right; 1: swung on, twisted)
        b = name == 'spin_1'
        p = ground(P(chest=T(6, -24 if not b else -40, -4), head=T(2, 14 if not b else 26), legr=limb(1, -6, 10), shinr=knee(14),
                     legl=limb(-1, 14, 10), shinl=knee(16)))
        p = hold(p, (8.0, 29.0, -12.0), (0.95, 0.04, -0.3) if not b else (0.93, 0.08, 0.36), 'c', up=(0.0, 1.0, 0.0), left=-4.0)
        p = hang(p, 14)
    elif name == 'stagger':                                   # (reeling back, the mace dipped, the left arm flung out)
        p = ground(P(chest=T(-16, 12, 6), head=T(-16, -12), legr=limb(1, -14, 6), shinr=knee(10), legl=limb(-1, 26, 8), shinl=knee(34),
                     arml=limb(-1, 34, 44), forel=limb(-1, 30)))
        p = hold(p, (9.0, 21.0, -8.0), (0.32, -0.78, -0.52), 'c')
        p = hang(p, 10)
    elif name == 'death_0':                                   # (down on its right knee, the mace head on the floor, its right hand on the haft)
        p = ground(P(body=T(2), chest=T(14, -4), head=T(16, 6), legr=limb(1, 0, 4), shinr=knee(90), legl=limb(-1, 80, 4), shinl=knee(82),
                     arml=limb(-1, 34, 4, 18), forel=limb(-1, 46, 0, 0)))
        p = hold(p, (3.0, 22.0, -12.0), (0.0, -0.94, -0.33), 'w', floor=0.0)
        p = hang(p)
    elif name == 'death_1':                                   # (slumped further over the haft, head bowed - then it turns to stone)
        p = ground(P(body=T(6), chest=T(34, -4), head=T(30, 8, 6), legr=limb(1, 0, 4), shinr=knee(92), legl=limb(-1, 74, 4), shinl=knee(84)))
        p = hold(p, (2.0, 18.0, -13.0), (0.0, -0.84, -0.54), 'w', left=-4.2, floor=0.0)
        p = hang(p)
    else:
        raise KeyError(name)
    return {k: v for k, v in p.items() if not k.startswith('_err')} | {'_err': (p.get('_err_r', 0.0), p.get('_err_l', 0.0))}


POSE_NAMES = ('statue', 'wake_0', 'wake_1', 'idle_a', 'idle_b', 'walk_0', 'walk_1', 'walk_2', 'walk_3', 'swing_0', 'swing_1',
              'spin_0', 'spin_1', 'stagger', 'death_0', 'death_1')
_PZ = {}


def _poses():
    if not _PZ:
        for n in POSE_NAMES:
            p = _pose(n); _PZ[n] = {k: v for k, v in p.items() if k != '_err'}; ERR[n] = p['_err']
    return _PZ


ERR = {}                                                       # (how far each hand missed its mark, design units - (right, left))


class _Lazy(dict):
    """POSES, solved on first use (the hands' ik runs once per pose)"""
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


# ---------------------------------------------------------------------------------------------------- the statue trophy (one baked model)
STATUE_K = 0.88                                                # (the knight in the trophy: 0.88 of its size, on the plinth)
PLINTH = (16.0, 2.0, 13.6, 1.6)                                # (the base course's side and height, the top course's)
BASE_Y = -15.0                                                 # (the plinth's foot, model units)
STATUE_FIXED = {'rotation': [0, 0, 0], 'translation': [0, -BASE_Y, 0], 'scale': [1, 1, 1]}


def _m3(q):
    x, y, z, w = q
    return [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]


def _mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def statue_elements(kind, pose_name='statue'):
    """the stone knight in a pose, every part's elements carried into one model (rigkit's pose turns folded into each element's
    own three-axis turn), scaled STATUE_K and stood on a plinth: (textures, elements)"""
    raw = _build()[kind]; pose = POSES[pose_name]; xf = rigkit.solve(PIVOT, PARENT, pose)
    Dm = [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]
    k = STATUE_K
    # the footprint's centre (feet and mace head) goes over the block's centre
    wb = world_boxes(pose, ('shinr', 'shinl', 'mace'), kind, xf)
    xs = [c[0] for bl in wb.values() for c, _a, _h in bl]; zs = [c[2] for bl in wb.values() for c, _a, _h in bl]
    cx, cz = -(min(xs) + max(xs)) / 2, -(min(zs) + max(zs)) / 2                                # (display frame -> design: D)
    top = BASE_Y + PLINTH[1] + PLINTH[3]
    def to_m(w):                                                                                   # (world design -> statue model)
        return [8 + (w[0] - cx) * k, top + w[1] * k, 8 + (w[2] - cz) * k]
    out = []
    for p in PARTS:
        Q, t = xf[p]; pv = PIVOT[p]; Qd = _mm(_mm(Dm, _m3(Q)), Dm); td = D(t)
        for e in _finish(raw[p], kind, 'stone'):
            f, to = e['from'], e['to']
            c = [(f[i] + to[i]) / 2 for i in range(3)]; h = [abs(to[i] - f[i]) / 2 for i in range(3)]
            Re = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            if 'rotation' in e:
                Re = _rotm(e['rotation']); o = e['rotation']['origin']
                c = [sum(Re[i][j] * (c[j] - o[j]) for j in range(3)) + o[i] for i in range(3)]
            cd = [c[i] - 8 + pv[i] for i in range(3)]
            r = [sum(Qd[i][j] * (cd[j] - pv[j]) for j in range(3)) for i in range(3)]
            w = [td[i] + pv[i] + r[i] for i in range(3)]
            m = to_m(w); R = _mm(Qd, Re)
            ne = {'from': [round(m[i] - h[i] * k, 4) for i in range(3)], 'to': [round(m[i] + h[i] * k, 4) for i in range(3)], 'faces': e['faces']}
            ang = rigkit.euler(R)
            if max(abs(a) for a in ang) > 1e-3: ne['rotation'] = {'origin': [round(v, 4) for v in m], 'x': ang[0], 'y': ang[1], 'z': ang[2]}
            out.append(ne)
    pl = tex_name('plinth', kind, 'stone'); tr = tex_name('trim', kind, 'stone'); ac = tex_name('accent', kind, 'stone')
    s0, h0, s1, h1 = PLINTH
    def box(x0, y0, z0, x1, y1, z1, t, shift=(0, 0)):
        fc = {}
        for fn, (a, b) in {'north': (x1 - x0, y1 - y0), 'south': (x1 - x0, y1 - y0), 'east': (z1 - z0, y1 - y0), 'west': (z1 - z0, y1 - y0),
                           'up': (x1 - x0, z1 - z0), 'down': (x1 - x0, z1 - z0)}.items():
            a, b = min(16, a), min(16, b); u0, v0 = shift[0] * (16 - a), shift[1] * (16 - b)
            fc[fn] = {'uv': [round(u0, 3), round(v0, 3), round(u0 + a, 3), round(v0 + b, 3)], 'texture': '#' + t}
        return {'from': [x0, y0, z0], 'to': [x1, y1, z1], 'faces': fc}
    out += [box(8 - s0 / 2, BASE_Y, 8 - s0 / 2, 8 + s0 / 2, BASE_Y + h0, 8 + s0 / 2, pl),
            box(8 - s1 / 2, BASE_Y + h0, 8 - s1 / 2, 8 + s1 / 2, top, 8 + s1 / 2, pl, (0.3, 0.6)),
            box(8 - s0 / 2 - 0.01, BASE_Y + h0 - 0.5, 8 - s0 / 2 - 0.01, 8 + s0 / 2 + 0.01, BASE_Y + h0, 8 + s0 / 2 + 0.01, tr),
            box(8 - 2.0, BASE_Y + 0.5, 8 - s0 / 2 - 0.05, 8 + 2.0, BASE_Y + 1.3, 8 - s0 / 2, ac)]    # (a dead rune on its front)
    for e in out:
        for v in e['from'] + e['to']: assert -16 <= v <= 32, (kind, e['from'], e['to'])
    used = sorted({fc['texture'][1:] for e in out for fc in e['faces'].values()})
    return {t: f'bm:block/{t}' for t in used}, out


def statue_display():
    """the 3D statue's views: fixed (the placed statue - see the docstring), and a small statue in a hand, on the ground, in a
    slot (the slot shows the flat icon - the item definition's select - but a model without one would show this)"""
    return {'fixed': STATUE_FIXED,
            'gui': {'rotation': [20, 200, 0], 'translation': [0, 1.0, 0], 'scale': [0.33, 0.33, 0.33]},
            'ground': {'rotation': [0, 0, 0], 'translation': [0, 3.0, 0], 'scale': [0.2, 0.2, 0.2]},
            'head': {'rotation': [0, 180, 0], 'translation': [0, 9.0, 0], 'scale': [0.25, 0.25, 0.25]},
            'thirdperson_righthand': {'rotation': [0, 180, 0], 'translation': [0, 3.0, 1.0], 'scale': [0.18, 0.18, 0.18]},
            'thirdperson_lefthand': {'rotation': [0, 180, 0], 'translation': [0, 3.0, 1.0], 'scale': [0.18, 0.18, 0.18]},
            'firstperson_righthand': {'rotation': [0, 200, 0], 'translation': [0, 3.0, 0], 'scale': [0.16, 0.16, 0.16]},
            'firstperson_lefthand': {'rotation': [0, 160, 0], 'translation': [0, 3.0, 0], 'scale': [0.16, 0.16, 0.16]},
            'on_shelf': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.3, 0.3, 0.3]}}


def statue_json(kind):
    tex, els = statue_elements(kind)
    t = dict(tex); t['particle'] = f'bm:block/{tex_name("plate", kind, "stone")}'
    return {'textures': t, 'elements': els, 'display': statue_display()}


def item_def(kind):
    """bm:knight_statue_<kind>: the icon in a slot (and on a shelf), the 3D statue everywhere else (an item_display, a hand)"""
    n = STATUES[kind]
    return {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                      'cases': [{'when': ['gui', 'on_shelf'], 'model': {'type': 'minecraft:model', 'model': f'bm:item/{n}_icon'}}],
                      'fallback': {'type': 'minecraft:model', 'model': f'bm:item/{n}'}}}


# ---------------------------------------------------------------------------------------------------- the icons (16 x 16, sprites280's look)
ICON_RAMP = {'dread': ['#25232a', '#38353e', '#4e4a55', '#68646f', '#86828c'],
             'vorn': ['#6c6e6a', '#8a8c86', '#a8aaa3', '#c4c5be', '#dedfd8']}
ICON_RUNE = {'dread': '#7a1e28', 'vorn': '#2e8a40'}
# a little stone knight on a plinth: 1-5 the stone's shades (dark -> light, lit from the top left), e: the unlit eye-slit/visor,
# r: the plinth's rune (the only colour - which dungeon it came from)
ICON_ROWS = {
    'dread': ['................',
              '..4..........2..',
              '..43........32..',
              '...4.5444.3.2...',
              '....454443.2....',
              '....4eeee2......',
              '.4544544332323..',
              '.454554433232.2.',
              '.44.5434433.22..',
              '.43.454333..21..',
              '.33..4433...21..',
              '.....4..32..2...',
              '.....43.32..1...',
              '..55555555555...',
              '..43rrrr3332221.',
              '..2222222221111.'],
    'vorn': ['................',
             '....5......4....',
             '.....4....3.....',
             '.....544443.....',
             '....54444433....',
             '....4eeeee32....',
             '.4544544332323..',
             '.454554433232.2.',
             '.44.5434433.22..',
             '.43.454333..21..',
             '.33..4433...21..',
             '.....4..32..2...',
             '.....43.32..1...',
             '..55555555555...',
             '..43rrrr3332221.',
             '..2222222221111.'],
}


def icon_raw(kind):
    """the icon before vanilla.process (gen_rp's ICONS loop finishes it): drawn, outlined"""
    from sprites280 import S
    s = S(); ramp = ICON_RAMP[kind]
    pal = {str(i + 1): ramp[i] for i in range(5)}; pal['e'] = '#141216' if kind == 'dread' else '#3c403c'; pal['r'] = ICON_RUNE[kind]
    s.g(ICON_ROWS[kind], pal)
    im = s.image(); px = im.load()
    add = [(x, y) for y in range(16) for x in range(16) if px[x, y][3] == 0 and
           any(0 <= x + dx < 16 and 0 <= y + dy < 16 and px[x + dx, y + dy][3] > 0 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in add: px[x, y] = (18, 14, 14, 255)
    return im


def icon(kind):
    """the icon as the pack ships it"""
    import vanilla
    return vanilla.process(STATUES[kind], icon_raw(kind))


ICONS = {STATUES[k]: icon_raw(k) for k in KINDS}             # ({'knight_statue_dread': image, ...} - raw: gen_rp's ICONS loop finishes them)


def icons():
    return dict(ICONS)


# ---------------------------------------------------------------------------------------------------- gen_rp
def rp(R):
    """gen_rp: the kn_ block textures (TEXTURE_MODS), every part x kind x finish as a 3D model at display scale (HATS,
    DISPLAY_3D_EXTRA 'kn_'), the statue icons (ICONS: models/item/knight_statue_<kind>.json and the texture item/knight_statue_<kind>),
    and in a post pass the 3D statues (written over the icon's flat model), the icon's own model (knight_statue_<kind>_icon)
    and the item definitions that choose between them"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (PREFIX,)
    R.ICONS.update(icons())
    def post(R2):
        for kind in KINDS:
            n = STATUES[kind]
            R2.wj(f'assets/bm/models/item/{n}_icon.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'bm:item/{n}'}})
            R2.wj(f'assets/bm/models/item/{n}.json', statue_json(kind))
            R2.wj(f'assets/bm/items/{n}.json', item_def(kind))
    R.POST.append(post)
