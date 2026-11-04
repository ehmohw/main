"""(3.1 draft, stage 1: art only - not wired) THE MIMIC - a Black Market vault chest with teeth. (2nd pass: redone to the quality
bar - a hollow plank chest with a barrel lid, iron straps, brass corners and lock, claw feet, a real mouth inside.)

UNLOCK  In a heist vault (Tier III+, 1 run in 40), one of the loot chests "looks back at you": its keyhole blinks. Open it and it
        throws a TANTRUM - 30 seconds of snapping and hopping round the vault (it can't really hurt you: 1 heart a bite, and it
        spits your loot back if it eats any). Survive it - or hand it a Gutter Coin mid-tantrum, which it eats, delighted - and
        it calms down, licks you, and joins you (its summoning item: the Mimic's Key, a gold key with a tooth for a bit).

LOOK    Knee-high (~0.8 blocks with its feet out), a proper treasure chest.
        DISGUISED ('disguise'): a dark oak strongbox - horizontal boards, a barrel-curved lid, two iron straps over the lid and
          down the front, brass corner brackets, rivets, a brass lock plate with a keyhole and a hasp - feet tucked away, eyes
          shut (the 'disg' face is just the lid's boards). Just a chest.
        REVEALED: the lid lifts on two rows of tapered teeth (the lower row on the box's rim, the upper under the lid), a fat
          grooved tongue, the inside a dark crimson gum with a heap of gold coins (and a gem, and someone's dagger) in it; two
          big gold eyes open on the lid's front - smug, a heavy lid; four brass BALL-AND-CLAW FEET come out of its corners.
RIG     body (the root: the box, its rim teeth, the gum, the loot) - lid (hinged at the back: the dome, its straps, the hasp, the
        upper teeth, the face: eyes per expression) - tongue (resting) / tonguel (the long tongue: the swallow, the stash) -
        feet fl fr bl br; fx: 'coins' (a burst of spat coins), 'gulp' (cheeks puffed - a foe swallowed), 'aura' (the rare
        Jackpot aura).
STASH   'stash': opened wide, the long tongue laid out flat like a welcome mat, the loot showing - it is a small portable stash.
SKINS   '_sh' SHINY "Voidbox": obsidian-black wood, violet-glowing banding, amethyst teeth, a starry violet gum. Cosmetics:
        '_crate' "Heist Crate" (pale pine, rope-brown straps, a stencilled FRAGILE), '_gild' "Royal Coffer" (red lacquer, gold
        everywhere - the vault's showpiece)."""
import math
import random
from PIL import Image
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, planks, metal, glaze, eye, blush, mouth, put, slab, stack, ball,
                      chain, ring)

PIVOT = {'body': (0, 2.0, 0), 'lid': (0, 10.0, 5.0), 'tongue': (0, 8.2, 2.0), 'tonguel': (0, 8.2, 2.0),
         'ffr': (5.6, 2.0, -3.8), 'ffl': (-5.6, 2.0, -3.8), 'fbr': (5.6, 2.0, 3.8), 'fbl': (-5.6, 2.0, 3.8),
         'coins': (0, 10, -9), 'gulp': (0, 8, 0), 'aura': (0, 0, 0)}
PARENT = {'body': None, 'lid': 'body', 'tongue': 'body', 'tonguel': 'body', 'ffr': 'body', 'ffl': 'body', 'fbr': 'body', 'fbl': 'body',
          'coins': None, 'gulp': 'body', 'aura': None}
FACES = ('disg', 'happy', 'greedy', 'fierce', 'blink', 'hurt', 'sleepy')
R = Rig('mm_', 0.8, PIVOT, PARENT, FACES, face_part='lid', opt=('tonguel', 'coins', 'gulp', 'aura'))
FEET = ('ffr', 'ffl', 'fbr', 'fbl')
SKIN_NAMES = {'_sh': 'SHINY: Voidbox', '_crate': 'cosmetic: Heist Crate', '_gild': 'cosmetic: Royal Coffer'}

C = dict(seam='#24160c', wooddk='#40281a', wood='#5c3a22', woodlt='#74502e',
         iron=('#2a2a30', '#4a4a54', '#6e6e7a', '#9a9aa8'), brass=('#7a5410', '#c08a24', '#e8b84a', '#fff0a0'),
         gum=('#3a0610', '#6a1220', '#8a1e2c'), tooth=('#fbf4e4', '#ffffff', '#e0d4bc'), tongue=('#b8304a', '#e0506a', '#f080a0', '#ffc0d0'),
         gold=('#a87010', '#f0c030', '#ffe070', '#fff8d0'), gem='#30d080', ruby='#e02040',
         eye_white='#fff6d8', iris=('#5a3000', '#a06008', '#e0a020', '#ffd040', '#fff090'), lash='#1a0e06', glow='#ffd23a')
SK = {'_sh': dict(seam='#05040a', wooddk='#0e0a18', wood='#1a1428', woodlt='#2a2040', iron=('#2a1050', '#5a2aa0', '#8a50e0', '#c0a0ff'),
                  brass=('#3a1a70', '#7a40d0', '#b06aff', '#f0d8ff'), gum=('#0a0820', '#181a40', '#2a2a6a'), tooth=('#e8d0ff', '#ffffff', '#b090e0'),
                  tongue=('#5a2090', '#8a3ab0', '#b060e0', '#e0b0ff'), gold=('#5a2aa0', '#b06aff', '#d8b0ff', '#ffffff'),
                  iris=('#3a0a6a', '#6a2ab0', '#a060f0', '#d0a0ff', '#f8e8ff'), eye_white='#f4eaff'),
      '_crate': dict(seam='#8a6438', wooddk='#b8925a', wood='#d4ae74', woodlt='#e8c890', iron=('#4a3018', '#6a4a28', '#8a6a40', '#a8885a'),
                     brass=('#5a4020', '#8a6a3a', '#a88a58', '#c8aa78')),
      '_gild': dict(seam='#3a0808', wooddk='#5a1010', wood='#8a1a1a', woodlt='#b02a24', iron=('#7a5410', '#c08a24', '#e8b84a', '#fff0a0'))}

# the face: on the lid's front strip, 11 x 3.4 units (44 x 14 texels); eyes 12 x 12 at 13 and 31
FW, FH = 11.0, 3.4
EYC, EYY, EYW, EYH = (13, 31), 1, 12, 12


# ---------------------------------------------------------------------------------------------------- textures
def _wood(c, seed, board=6):
    return lit(planks((c['seam'], c['wooddk'], c['wood'], c['woodlt']), seed, board), 1.06, 0.92, 8)


def _face(kind, c):
    im = _wood(c, 31, 7)
    return im


def _eyes(kind, c):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if kind == 'disg': return im
    for i, cx in enumerate(EYC):
        k = {'greedy': 'wide', 'fierce': 'fierce', 'sleepy': 'sleepy'}.get(kind, kind)
        eye(im, cx, EYY, EYW, EYH, i == 1, k, iris=c['iris'], lash=c['lash'], white=c['eye_white'], pupil='#1a0a00',
            lid=4 if kind is None else None)
        if kind == 'greedy':                                                 # (gold coins in its eyes: a $ glint)
            for dy in range(3, 9): put(im, cx, EYY + dy, '#fff8d0')
    return im


def textures(c):
    t = {'wood': _wood(c, 1), 'wood2': _wood(c, 2), 'woodv': lit(planks((c['seam'], c['wooddk'], c['wood'], c['woodlt']), 3, 32, nails=False), 1.06, 0.92, 8),
         'dark': soft(c['wooddk'], c['wood'], c['seam'], 4, 0.15), 'iron': metal(c['iron'], 5, rivets=True), 'ironp': metal(c['iron'], 6),
         'brass': metal(c['brass'], 7), 'gum': soft(c['gum'][1], c['gum'][2], c['gum'][0], 8, 0.06), 'throat': soft(c['gum'][1], c['gum'][2], c['gum'][0], 9, 0.05),
         'tooth': lit(soft(c['tooth'][0], c['tooth'][1], c['tooth'][2], 10, 0.08), 1.04, 0.9, 8),
         'tongue': glaze(c['tongue'], 11, 3), 'gold': glaze((c['gold'][0], c['gold'][1], c['gold'][2], c['gold'][3]), 12, 2),
         'gem': soft(c['gem'], mix(c['gem'], '#ffffff', 0.5), mix(c['gem'], '#000000', 0.3), 13, 0.3),
         'ruby': soft(c['ruby'], mix(c['ruby'], '#ffffff', 0.5), mix(c['ruby'], '#000000', 0.3), 14, 0.3),
         'keyhole': cells(lambda x, y, r: '#0a0604' if (14 <= x <= 17 and 8 <= y <= 15) or (12 <= x <= 19 and 4 <= y <= 9 and (x - 15.5) ** 2 + (y - 6.5) ** 2 < 9) else c['brass'][1], 15),
         'steel': metal(('#5a5a66', '#a0a0b0', '#d0d0dc', '#ffffff'), 16), 'grip': soft('#4a2a14', '#6a4020', '#2a1608', 17, 0.2),
         'face': _face(None, c), 'eyes': _eyes(None, c)}
    for f in FACES: t[f'face_{f}'] = _face(f, c); t[f'eyes_{f}'] = _eyes(f, c)
    return t


TEX = textures(C)
for k, v in TEX.items(): R.tex(k, v)
for sfx, ch in SK.items():
    for k, v in textures(dict(C, **ch)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in TEX})

# ---------------------------------------------------------------------------------------------------- the model
B = R.box
W, D = 7.0, 5.0                         # (half width, half depth)
Y0, Y1 = 2.0, 10.0                      # (the box's bottom and rim)
th = 0.8                                # (the walls' thickness)
# ---- the box: four plank walls (hollow - it's a mouth), a gum floor, a dark plinth, the rim's iron band
B('body', (-W, Y0, -D), (W, Y1, -D + th), 'wood', shift=False)
B('body', (-W, Y0, D - th), (W, Y1, D), 'wood2', shift=False)
B('body', (-W, Y0, -D + th), (-W + th, Y1, D - th), 'wood2', shift=False)
B('body', (W - th, Y0, -D + th), (W, Y1, D - th), 'wood', shift=False)
B('body', (-W + th, Y0, -D + th), (W - th, 6.2, D - th), 'dark')
B('body', (-W + th, 6.2, -D + th), (W - th, 6.4, D - th), 'gum', faces=('up',))
for a, b in (((-W + th, 6.2, -D + th), (W - th, 9.6, -D + th + 0.05)), ((-W + th, 6.2, D - th - 0.05), (W - th, 9.6, D - th)),
             ((-W + th, 6.2, -D + th), (-W + th + 0.05, 9.6, D - th)), ((W - th - 0.05, 6.2, -D + th), (W - th, 9.6, D - th))):
    B('body', a, b, 'gum')                                                          # (the gum lining its inside)
B('body', (-W - 0.2, Y0, -D - 0.2), (W + 0.2, Y0 + 0.9, D + 0.2), 'dark')            # (the plinth)
for a, b in (((-W - 0.12, Y1 - 0.8, -D - 0.12), (W + 0.12, Y1, -D + th)), ((-W - 0.12, Y1 - 0.8, D - th), (W + 0.12, Y1, D + 0.12)),
             ((-W - 0.12, Y1 - 0.8, -D + th), (-W + th, Y1, D - th)), ((W - th, Y1 - 0.8, -D + th), (W + 0.12, Y1, D - th))):
    B('body', a, b, 'ironp', shift=False)                                            # (the rim band: a frame round the mouth)
for sx in (-1, 1):                                                                   # (the front and back straps, down from the rim)
    x0 = sx * 3.8
    for z0, z1 in ((-D - 0.16, -D), (D, D + 0.16)):
        B('body', (x0 - 0.55, Y0 + 0.9, z0), (x0 + 0.55, Y1 - 0.8, z1), 'iron')
for sx in (-1, 1):                                                                   # (a strap round each end)
    a, b = sorted((sx * W, sx * (W + 0.16)))
    B('body', (a, Y0 + 0.9, -0.55), (b, Y1 - 0.8, 0.55), 'iron')
for sx in (-1, 1):                                                                   # (brass corner brackets, top and bottom, front and back)
    for sz in (-1, 1):
        for y0, y1 in ((Y0 + 0.9, Y0 + 2.6), (Y1 - 2.4, Y1 - 0.8)):
            a, b = sorted((sx * (W - 1.5), sx * (W + 0.2))); za, zb = sorted((sz * D, sz * (D + 0.2)))
            B('body', (a, y0, za), (b, y1, zb), 'brass')
            a, b = sorted((sx * W, sx * (W + 0.2))); za, zb = sorted((sz * (D - 1.5), sz * (D + 0.2)))
            B('body', (a, y0, za), (b, y1, zb), 'brass')
B('body', (-1.5, 6.8, -D - 0.28), (1.5, 9.4, -D), 'keyhole', faces=('north', 'east', 'west', 'up', 'down'), uv={'north': [0, 0, 16, 16]})   # (the lock)
B('body', (-1.7, 6.6, -D - 0.2), (1.7, 9.6, -D - 0.05), 'brass')
# the lower teeth along the rim: tapered (a base and a point), varied, a pair of fangs at the front corners
rt = random.Random(3)
def teeth(part, y, up, pts, scale=1.0):
    for (x, z, s) in pts:
        s *= scale
        h0, h1 = 0.7 * s, 1.35 * s
        if up:
            B(part, (x - 0.45 * s, y, z - 0.45 * s), (x + 0.45 * s, y + h0, z + 0.45 * s), 'tooth')
            B(part, (x - 0.22 * s, y + h0, z - 0.22 * s), (x + 0.22 * s, y + h1, z + 0.22 * s), 'tooth')
        else:
            B(part, (x - 0.45 * s, y - h0, z - 0.45 * s), (x + 0.45 * s, y, z + 0.45 * s), 'tooth')
            B(part, (x - 0.22 * s, y - h1, z - 0.22 * s), (x + 0.22 * s, y - h0, z + 0.22 * s), 'tooth')
LOW = [(-6.1 + i * 1.22, -4.5, (1.25 if i in (0, 10) else 0.8 + 0.2 * (i % 2))) for i in range(11)] + \
      [(sx * 6.4, -3.2 + j * 1.5, 0.75 + 0.15 * (j % 2)) for sx in (-1, 1) for j in range(5)]
teeth('body', Y1, True, LOW)
# the loot inside: a heap of coins, a gem, a ruby, a dagger's hilt sticking up
for i in range(26):
    x, z = rt.uniform(-5.4, 5.4), rt.uniform(-3.4, 3.8); y = 6.4 + max(0.0, 2.2 - 0.06 * (x * x + (z - 0.8) ** 2)) + rt.uniform(0, 0.3)
    B('body', (x - 0.6, y, z - 0.6), (x + 0.6, y + 0.22, z + 0.6), 'gold', rot=('y', rt.uniform(-40, 40), (x, y, z)), light=3)
ball(R, 'body', (-2.6, 8.6, 1.4), 0.65, 'gem', 3, light=6); ball(R, 'body', (3.2, 8.2, 2.0), 0.5, 'ruby', 2, light=6)
R.seg('body', (1.8, 7.0, 2.6), (2.6, 10.6, 3.4), 0.42, 0.42, 'grip'); B('body', (1.6, 10.4, 2.8), (3.0, 10.7, 3.8), 'brass')
B('body', (2.4, 10.7, 3.1), (2.9, 11.2, 3.5), 'brass')
# ---- the lid: closed over the box (y 10..14.6), barrel-curved front to back; its straps follow the curve; the face on its front
ARC = [(-D, -D + 1.4, 12.6), (-D + 1.4, -D + 3.2, 13.8), (-D + 3.2, D - 3.2, 14.6), (D - 3.2, D - 1.4, 13.8), (D - 1.4, D, 12.6)]
for i, (z0, z1, yt) in enumerate(ARC):
    B('lid', (-W, Y1, z0), (W, yt, z1), 'wood2' if i % 2 else 'wood', shift=False)
    for sx in (-1, 1):                                                               # (the straps over the curve)
        x0 = sx * 3.8
        B('lid', (x0 - 0.55, yt, z0), (x0 + 0.55, yt + 0.16, z1), 'iron')
for sx in (-1, 1):                                                                   # (the straps down the lid's front and back faces)
    x0 = sx * 3.8
    B('lid', (x0 - 0.55, Y1 + 0.2, -D - 0.16), (x0 + 0.55, 12.6, -D), 'iron')
    B('lid', (x0 - 0.55, Y1 + 0.2, D), (x0 + 0.55, 12.6, D + 0.16), 'iron')
    a, b = sorted((sx * W, sx * (W + 0.16)))
    B('lid', (a, Y1, -0.55), (b, 14.4, 0.55), 'iron')                                  # (and over each end)
for a, b in (((-W - 0.1, Y1, -D - 0.1), (W + 0.1, Y1 + 0.5, -D + th)), ((-W - 0.1, Y1, D - th), (W + 0.1, Y1 + 0.5, D + 0.1)),
             ((-W - 0.1, Y1, -D + th), (-W + th, Y1 + 0.5, D - th)), ((W - th, Y1, -D + th), (W + 0.1, Y1 + 0.5, D - th))):
    B('lid', a, b, 'ironp', shift=False)                                             # (the lid's lower band, a frame)
# the face plate and the eyes on the lid's front (between the straps' run: the straps sit on top of it)
B('lid', (-FW / 2, Y1 + 0.5, -D - 0.02), (FW / 2, Y1 + 0.5 + FH, -D), 'FACE', faces=('north',), uv={'north': [0, 0, FW, FH]})
B('lid', (-FW / 2, Y1 + 0.5, -D - 0.24), (FW / 2, Y1 + 0.5 + FH, -D - 0.22), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]}, light=8)
B('lid', (-0.9, 8.8, -D - 0.42), (0.9, 11.4, -D - 0.2), 'brass')                       # (the hasp, hanging over the lock)
B('lid', (-0.45, 9.2, -D - 0.5), (0.45, 9.9, -D - 0.42), 'iron')
# its underside: the gum, and the upper teeth hanging down round the front and the sides
B('lid', (-W + th, Y1 - 0.08, -D + th), (W - th, Y1 - 0.03, D - th), 'throat', faces=('down',))
UP = [(-5.5 + i * 1.22, -4.5, (1.15 if i in (0, 9) else 0.75 + 0.2 * ((i + 1) % 2))) for i in range(10)] + \
     [(sx * 6.4, -2.6 + j * 1.6, 0.7 + 0.15 * (j % 2)) for sx in (-1, 1) for j in range(4)]
teeth('lid', Y1, False, UP)
# ---- the tongue: fat, a groove down its middle, resting in the coins; the long one rolled out (swallow, stash)
tx, ty, tz = PIVOT['tongue']
for (z0, z1, w, y) in ((2.0, -0.5, 2.0, 8.4), (-0.5, -2.8, 1.8, 8.7), (-2.8, -4.0, 1.4, 9.1)):
    R.seg('tongue', (0, y, z0), (0, y + 0.1, z1), w * 1.6, 0.8, 'tongue', ext=0.15)
R.seg('tongue', (0, 8.85, 1.5), (0, 9.35, -3.4), 0.3, 0.12, 'gum')
pts = [(0, 8.4, 2.0), (0, 8.8, -1.5), (0, 9.4, -5.0), (0, 8.4, -8.0), (0, 4.6, -10.0), (0, 1.0, -10.6), (0, 0.2, -13.4), (0, 0.2, -16.4)]
for i in range(len(pts) - 1):
    w = 3.2 - 0.12 * i
    R.seg('tonguel', pts[i], pts[i + 1], w, 0.8, 'tongue', ext=0.2)
    R.seg('tonguel', (pts[i][0], pts[i][1] + 0.42, pts[i][2]), (pts[i + 1][0], pts[i + 1][1] + 0.42, pts[i + 1][2]), 0.3, 0.1, 'gum')
# ---- the feet: brass ball-and-claw, out of each corner
for p in FEET:
    x, y, z = PIVOT[p]; sx = 1 if x > 0 else -1; sz = 1 if z > 0 else -1
    R.seg(p, (x, y + 0.6, z), (x, y - 0.8, z), 1.0, 1.0, 'brass')
    ball(R, p, (x, y - 1.15, z), 0.85, 'gold', 3, ry=0.7)
    for dx, dz in ((0.0, -1.0), (sx * 0.85, -0.5), (sx * 0.75, 0.6), (-sx * 0.75, -0.4)):
        chain(R, p, [(x, y - 1.0, z), (x + dx * 1.0, y - 1.4, z + dz * 1.0), (x + dx * 1.35, y - 2.0, z + dz * 1.35)], [0.55, 0.42, 0.22], 'brass')
# ---- fx: the spat coins, the puffed cheeks of a gulp, the Jackpot aura
cr = random.Random(9)
for i in range(16):
    x, y, z = cr.uniform(-5, 5), 10 + cr.uniform(-1, 7), -6 - cr.uniform(0, 8)
    B('coins', (x - 0.6, y - 0.6, z - 0.12), (x + 0.6, y + 0.6, z + 0.12), 'gold', rot=('y', cr.uniform(-70, 70), (x, y, z)), light=8)
for sx in (-1, 1):
    stack(R, 'gulp', [(4.0, 5.0, 1.0, 3.6), (5.0, 8.0, 1.4, 4.2), (8.0, 9.0, 1.0, 3.6)], 'wood', c=(sx * (W + 0.1), 0))
for i in range(10):
    a = math.radians(i * 36); x, z = 11 * math.cos(a), 11 * math.sin(a); y = 6 + 3 * math.sin(a * 2)
    B('aura', (x - 0.8, y - 0.8, z - 0.14), (x + 0.8, y + 0.8, z + 0.14), 'gold', rot=('y', i * 36 + 90, (x, y, z)), light=12)
    if i % 2: B('aura', (x * 0.85 - 0.25, y + 2.0, z * 0.85 - 0.25), (x * 0.85 + 0.25, y + 2.5, z * 0.85 + 0.25), 'tooth', light=14)


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


def lid(a):
    return T(-a)                                                    # (open: the lid's front lifts, swinging back on the hinge)


POSES = R.POSES
POSES.update({
    'disguise': P(_face='disg', _hide=FEET),
    'idle_a': P(lid=lid(14)),
    'idle_b': P(_face='happy', lid=lid(30), tongue=T(-6)),
    'idle_c': P(_face='greedy', lid=lid(8), body=T(0, 0, 6)),                                   # (eyeing your coin purse)
    'walk_0': P(lift=0.6, lid=lid(10), body=T(4, 0, 6), ffr=T(-26), fbl=T(-26), ffl=T(18), fbr=T(18)),
    'walk_1': P(lid=lid(16), body=T(-2, 0, -6), ffr=T(18), fbl=T(18), ffl=T(-26), fbr=T(-26)),
    # sitting: it settles, feet tucked; a doze with the lid shut and a coin on its tongue
    'sit_a': P(_face='happy', lid=lid(6), _hide=FEET),
    'sit_b': P(_face='sleepy', lid=lid(2), _hide=FEET, body=T(0, 0, 4)),
    # SNAP (the lunge): the lid flung wide - then the leap, slamming shut on the foe
    'snap_up': P(_face='fierce', lid=lid(78), body=T(-14), ffr=T(30), ffl=T(30)),
    'snap': P(lift=2.5, _face='fierce', lid=lid(4), body=T(22), ffr=T(-40), ffl=T(-40), fbr=T(40), fbl=T(40), _off=(0, 0, -6)),
    # SWALLOW (charged): open wide, the long tongue out round the foe ... gulp (cheeks puffed) ... and SPIT it out, coins flying
    'swallow': P(_face='greedy', _show=('tonguel',), _hide=('tongue',), lid=lid(96), body=T(-10)),
    'gulp': P(_face='blink', _show=('gulp',), lid=lid(0), body=T(-6, 0, 4)),
    'spit': P(_face='fierce', _show=('coins',), lid=lid(70), body=T(18), tongue=T(20)),
    # THE STASH: wide open, the long tongue laid out flat like a welcome mat, the loot showing
    'stash': P(_face='happy', _show=('tonguel',), _hide=('tongue',), lid=lid(105)),
    'tantrum': P(lift=3.5, _face='fierce', lid=lid(55), body=T(10, 20, -14), ffr=T(-40), fbl=T(30)),
    'hurt': P(_face='hurt', lid=lid(22), body=T(-14, 0, 10)),
    'aura': P(_face='happy', _show=('aura',), lid=lid(20)),
})
DRAFT = ['disguise', 'idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'sit_a', 'sit_b', 'snap_up', 'snap', 'swallow', 'gulp', 'spit',
         'stash', 'tantrum', 'hurt', 'aura']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'lid': 'head', 'body': 'body', 'tongue': 'body', 'ffr': 'legs', 'ffl': 'legs', 'fbr': 'legs', 'fbl': 'legs'}
SHINY = 'Shiny Voidbox'
