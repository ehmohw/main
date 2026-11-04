"""(3.1 draft, stage 1: art only) THE MIMIC's outfit "TREASURE CHEST" - the owner liked the Mimic's first quality-bar look (the
dark oak strongbox: a barrel-curved lid, iron straps, brass corners and lock, brass ball-and-claw feet), so it comes back as an
OUTFIT on today's vanilla-chest Mimic (mimic_pet_art).

ONE RIG, SWAPPED PART BY PART: CLASSIC is built on the Mimic's own rig - the same PIVOT, PARENT, FACES, face part ('lid') and
opt parts, and the very same POSES dict - only its geometry and textures are its own, under the prefix 'mmt_'. So the wardrobe swaps
each part's model one for one: mm_<part>[_x<face>][<skin>] -> mmt_<part>[_x<face>][<skin>] (parts: body, lid, tongue, tonguel,
ffr, ffl, fbr, fbl, coins, gulp, aura). Its proportions are refitted to the vanilla chest's footprint (14 x 14; the rim at the
lid's hinge, y 11), so the lid swings on the same hinge and every pose's grounding holds.

EYES    the Mimic's current ones (mimic_pet_art._eyes: the smug gold CAT eyes, the KEYHOLE pupils), in the same window on the
        lid's front, either side of the brass hasp - so both looks share one face.
SKINS   '' the dark oak Treasure Chest; '_sh' its shiny (the first pass's Voidbox: obsidian wood, violet banding).
DOLL    none here: the doll stays the vanilla chibi chest (mimic_pet_art's 'doll' / 'dolllid' parts have no models in this set)."""
import math
import random
from fol5_kit import Rig, mix, T, soft, lit, planks, metal, glaze, cells, ball, chain, stack
import mimic_pet_art as M

NAME = 'Treasure Chest'
PREFIX = 'mmt_'
PARTS_SWAPPED = ('body', 'lid', 'tongue', 'tonguel', 'ffr', 'ffl', 'fbr', 'fbl', 'coins', 'gulp', 'aura')
CLASSIC = Rig(PREFIX, M.R.RIG_SCALE, M.PIVOT, M.PARENT, M.FACES, face_part='lid', opt=tuple(sorted(M.R.OPT)))
R = CLASSIC
SKIN_NAMES = {'_sh': 'SHINY: Voidbox (the Treasure Chest in obsidian and violet)'}

C = dict(seam='#24160c', wooddk='#40281a', wood='#5c3a22', woodlt='#74502e',
         iron=('#2a2a30', '#4a4a54', '#6e6e7a', '#9a9aa8'), brass=('#7a5410', '#c08a24', '#e8b84a', '#fff0a0'),
         gum=M.C['gum'], tooth=M.C['tooth'], tongue=M.C['tongue'], gold=M.C['gold'], gem=M.C['gem'], ruby=M.C['ruby'],
         eye_white=M.C['eye_white'], iris=M.C['iris'], lash=M.C['lash'])
SK = {'_sh': dict(seam='#05040a', wooddk='#0e0a18', wood='#1a1428', woodlt='#2a2040', iron=('#2a1050', '#5a2aa0', '#8a50e0', '#c0a0ff'),
                  brass=('#3a1a70', '#7a40d0', '#b06aff', '#f0d8ff'), gum=M.SK['_sh']['gum'], tooth=M.SK['_sh']['tooth'],
                  tongue=M.SK['_sh']['tongue'], gold=M.SK['_sh']['gold'], iris=M.SK['_sh']['iris'], eye_white=M.SK['_sh']['eye_white'])}

# ---- the geometry, on the Mimic's pivots: the vanilla footprint, the rim at the lid's hinge
W, D, Y0 = M.W, M.D, M.Y0
LY = M.LY0                                   # (the hinge, and the rim: 11)
Y1 = LY
th = 0.8
FLOOR = M.FLOOR
SX = 5.0                                     # (the straps' line, out past the eyes)
ARC = [(-D, -D + 1.6, LY + 4.1), (-D + 1.6, -D + 4.0, LY + 5.0), (-D + 4.0, D - 4.0, LY + 5.6), (D - 4.0, D - 1.6, LY + 5.0), (D - 1.6, D, LY + 4.1)]


# ---------------------------------------------------------------------------------------------------- textures
def _wood(c, seed, board=6):
    return lit(planks((c['seam'], c['wooddk'], c['wood'], c['woodlt']), seed, board), 1.06, 0.92, 8)


def textures(c):
    t = {'wood': _wood(c, 1), 'wood2': _wood(c, 2), 'dark': soft(c['wooddk'], c['wood'], c['seam'], 4, 0.15),
         'iron': metal(c['iron'], 5, rivets=True), 'ironp': metal(c['iron'], 6), 'brass': metal(c['brass'], 7),
         'gum': soft(c['gum'][1], c['gum'][2], c['gum'][0], 8, 0.06), 'throat': soft(c['gum'][1], c['gum'][2], c['gum'][0], 9, 0.05),
         'tooth': lit(soft(c['tooth'][0], c['tooth'][1], c['tooth'][2], 10, 0.08), 1.04, 0.9, 8),
         'tongue': glaze(c['tongue'], 11, 3), 'gold': glaze(tuple(c['gold']), 12, 2),
         'gem': soft(c['gem'], mix(c['gem'], '#ffffff', 0.5), mix(c['gem'], '#000000', 0.3), 13, 0.3),
         'ruby': soft(c['ruby'], mix(c['ruby'], '#ffffff', 0.5), mix(c['ruby'], '#000000', 0.3), 14, 0.3),
         'keyhole': cells(lambda x, y, r: '#0a0604' if (14 <= x <= 17 and 8 <= y <= 15) or (12 <= x <= 19 and 4 <= y <= 9 and (x - 15.5) ** 2 + (y - 6.5) ** 2 < 9) else c['brass'][1], 15),
         'grip': soft('#4a2a14', '#6a4020', '#2a1608', 17, 0.2), 'eyes': M._eyes(None, c)}
    for f in M.FACES: t[f'eyes_{f}'] = M._eyes(f, c)
    return t


TEX = textures(C)
for k, v in TEX.items(): R.tex(k, v)
for sfx, ch in SK.items():
    for k, v in textures(dict(C, **ch)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in TEX})

# ---------------------------------------------------------------------------------------------------- the model
B = R.box
# ---- the body: four plank walls (hollow - it's a mouth), a dark fill under a gum floor, the gum lining, the plinth, the rim band
B('body', (-W, Y0, -D), (W, Y1, -D + th), 'wood', shift=False)
B('body', (-W, Y0, D - th), (W, Y1, D), 'wood2', shift=False)
B('body', (-W, Y0, -D + th), (-W + th, Y1, D - th), 'wood2', shift=False)
B('body', (W - th, Y0, -D + th), (W, Y1, D - th), 'wood', shift=False)
B('body', (-W + th, Y0, -D + th), (W - th, FLOOR - 0.2, D - th), 'dark')
B('body', (-W + th, FLOOR - 0.2, -D + th), (W - th, FLOOR, D - th), 'gum', faces=('up',))
for a, b in (((-W + th, FLOOR, -D + th), (W - th, Y1 - 0.4, -D + th + 0.05)), ((-W + th, FLOOR, D - th - 0.05), (W - th, Y1 - 0.4, D - th)),
             ((-W + th, FLOOR, -D + th), (-W + th + 0.05, Y1 - 0.4, D - th)), ((W - th - 0.05, FLOOR, -D + th), (W - th, Y1 - 0.4, D - th))):
    B('body', a, b, 'gum')
B('body', (-W - 0.2, Y0, -D - 0.2), (W + 0.2, Y0 + 0.9, D + 0.2), 'dark')                       # (the plinth)
for a, b in (((-W - 0.12, Y1 - 0.8, -D - 0.12), (W + 0.12, Y1, -D + th)), ((-W - 0.12, Y1 - 0.8, D - th), (W + 0.12, Y1, D + 0.12)),
             ((-W - 0.12, Y1 - 0.8, -D + th), (-W + th, Y1, D - th)), ((W - th, Y1 - 0.8, -D + th), (W + 0.12, Y1, D - th))):
    B('body', a, b, 'ironp', shift=False)                                                       # (the rim band)
for sx in (-1, 1):                                                                              # (the straps down the front and back)
    for z0, z1 in ((-D - 0.16, -D), (D, D + 0.16)):
        B('body', (sx * SX - 0.55, Y0 + 0.9, z0), (sx * SX + 0.55, Y1 - 0.8, z1), 'iron')
    a, b = sorted((sx * W, sx * (W + 0.16)))                                                    # (and round each end)
    B('body', (a, Y0 + 0.9, -0.55), (b, Y1 - 0.8, 0.55), 'iron')
for sx in (-1, 1):                                                                              # (brass corner brackets)
    for sz in (-1, 1):
        for y0, y1 in ((Y0 + 0.9, Y0 + 2.6), (Y1 - 2.5, Y1 - 0.8)):
            a, b = sorted((sx * (W - 1.5), sx * (W + 0.2))); za, zb = sorted((sz * D, sz * (D + 0.2)))
            B('body', (a, y0, za), (b, y1, zb), 'brass')
            a, b = sorted((sx * W, sx * (W + 0.2))); za, zb = sorted((sz * (D - 1.5), sz * (D + 0.2)))
            B('body', (a, y0, za), (b, y1, zb), 'brass')
B('body', (-1.5, 7.4, -D - 0.28), (1.5, 10.0, -D), 'keyhole', faces=('north', 'east', 'west', 'up', 'down'), uv={'north': [0, 0, 16, 16]})   # (the lock)
B('body', (-1.7, 7.2, -D - 0.2), (1.7, 10.2, -D - 0.05), 'brass')
def teeth(part, y, up, pts):
    for (x, z, s) in pts:
        h0, h1 = 0.7 * s, 1.35 * s
        if up:
            B(part, (x - 0.45 * s, y, z - 0.45 * s), (x + 0.45 * s, y + h0, z + 0.45 * s), 'tooth')
            B(part, (x - 0.22 * s, y + h0, z - 0.22 * s), (x + 0.22 * s, y + h1, z + 0.22 * s), 'tooth')
        else:
            B(part, (x - 0.45 * s, y - h0, z - 0.45 * s), (x + 0.45 * s, y, z + 0.45 * s), 'tooth')
            B(part, (x - 0.22 * s, y - h1, z - 0.22 * s), (x + 0.22 * s, y - h0, z + 0.22 * s), 'tooth')
teeth('body', Y1, True, M.LOW)
rt = random.Random(3)                                                                           # (the loot, as the Mimic's)
for i in range(26):
    x, z = rt.uniform(-5.4, 5.4), rt.uniform(-4.8, 5.0); y = FLOOR + max(0.0, 2.2 - 0.05 * (x * x + (z - 0.8) ** 2)) + rt.uniform(0, 0.3)
    B('body', (x - 0.6, y, z - 0.6), (x + 0.6, y + 0.22, z + 0.6), 'gold', rot=('y', rt.uniform(-40, 40), (x, y, z)), light=3)
ball(R, 'body', (-2.8, FLOOR + 2.0, 1.6), 0.65, 'gem', 3, light=6); ball(R, 'body', (3.4, FLOOR + 1.6, 2.4), 0.5, 'ruby', 2, light=6)
R.seg('body', (1.8, FLOOR + 0.4, 3.2), (2.6, FLOOR + 3.0, 4.0), 0.42, 0.42, 'grip'); B('body', (1.6, FLOOR + 2.8, 3.4), (3.0, FLOOR + 3.1, 4.4), 'brass')
B('body', (2.4, FLOOR + 3.1, 3.7), (2.9, FLOOR + 3.6, 4.1), 'brass')
# ---- the lid: barrel-curved, five boards stepping up to a crown; the straps over the curve, down its faces and over each end
for i, (z0, z1, yt) in enumerate(ARC):
    B('lid', (-W, LY, z0), (W, yt, z1), 'wood2' if i % 2 else 'wood', shift=False)
    for sx in (-1, 1):
        B('lid', (sx * SX - 0.55, yt, z0), (sx * SX + 0.55, yt + 0.16, z1), 'iron')
for sx in (-1, 1):
    B('lid', (sx * SX - 0.55, LY + 0.2, -D - 0.16), (sx * SX + 0.55, ARC[0][2], -D), 'iron')
    B('lid', (sx * SX - 0.55, LY + 0.2, D), (sx * SX + 0.55, ARC[-1][2], D + 0.16), 'iron')
    a, b = sorted((sx * W, sx * (W + 0.16)))
    B('lid', (a, LY, -0.55), (b, ARC[2][2] - 0.2, 0.55), 'iron')
for a, b in (((-W - 0.1, LY, -D - 0.1), (W + 0.1, LY + 0.5, -D + th)), ((-W - 0.1, LY, D - th), (W + 0.1, LY + 0.5, D + 0.1)),
             ((-W - 0.1, LY, -D + th), (-W + th, LY + 0.5, D - th)), ((W - th, LY, -D + th), (W + 0.1, LY + 0.5, D - th))):
    B('lid', a, b, 'ironp', shift=False)                                                        # (its lower band)
# the eyes: the Mimic's cat eyes, in its own window on the lid's front (proud of the straps), either side of the hasp
B('lid', (-M.FW / 2, LY + 0.55, -D - 0.24), (M.FW / 2, LY + 0.55 + M.FH, -D - 0.22), 'EYES', faces=('north',), uv={'north': [0, 0, M.FW, M.FH]}, light=8)
B('lid', (-0.9, 8.9, -D - 0.42), (0.9, LY + 1.0, -D - 0.2), 'brass')                            # (the hasp, over the lock)
B('lid', (-0.45, 9.3, -D - 0.5), (0.45, 10.0, -D - 0.42), 'iron')
B('lid', (-W + th, LY - 0.08, -D + th), (W - th, LY - 0.03, D - th), 'throat', faces=('down',))
teeth('lid', LY, False, M.UP)
# ---- the tongue and the long tongue: the Mimic's own, in this set's textures
for (z0, z1, w, y) in ((2.0, -0.5, 2.0, 9.6), (-0.5, -2.8, 1.8, 9.9), (-2.8, -4.4, 1.4, 10.3)):
    R.seg('tongue', (0, y, z0), (0, y + 0.1, z1), w * 1.6, 0.8, 'tongue', ext=0.15)
R.seg('tongue', (0, 10.05, 1.5), (0, 10.55, -3.8), 0.3, 0.12, 'gum')
pts = [(0, 9.6, 2.0), (0, 10.2, -1.5), (0, 11.4, -5.0), (0, 12.0, -7.6), (0, 9.0, -9.6), (0, 4.6, -10.8), (0, 0.6, -11.6), (0, 0.2, -14.4),
       (0, 0.2, -17.4)]
for i in range(len(pts) - 1):
    w = 3.2 - 0.12 * i
    R.seg('tonguel', pts[i], pts[i + 1], w, 0.8, 'tongue', ext=0.2)
    R.seg('tonguel', (pts[i][0], pts[i][1] + 0.42, pts[i][2]), (pts[i + 1][0], pts[i + 1][1] + 0.42, pts[i + 1][2]), 0.3, 0.1, 'gum')
# ---- the feet: brass ball-and-claw, out of each corner (the antique chest that walks)
for p in M.FEET:
    x, y, z = M.PIVOT[p]; sx = 1 if x > 0 else -1
    R.seg(p, (x, y + 0.6, z), (x, y - 0.8, z), 1.0, 1.0, 'brass')
    ball(R, p, (x, y - 1.15, z), 0.85, 'gold', 3, ry=0.7)
    for dx, dz in ((0.0, -1.0), (sx * 0.85, -0.5), (sx * 0.75, 0.6), (-sx * 0.75, -0.4)):
        chain(R, p, [(x, y - 1.0, z), (x + dx, y - 1.4, z + dz), (x + dx * 1.35, y - 2.0, z + dz * 1.35)], [0.55, 0.42, 0.22], 'brass')
# ---- fx: the spat coins, the puffed cheeks of a gulp, the Jackpot aura (as the Mimic's)
cr = random.Random(9)
for i in range(16):
    x, y, z = cr.uniform(-5, 5), 12 + cr.uniform(-1, 7), -8 - cr.uniform(0, 8)
    B('coins', (x - 0.6, y - 0.6, z - 0.12), (x + 0.6, y + 0.6, z + 0.12), 'gold', rot=('y', cr.uniform(-70, 70), (x, y, z)), light=8)
for sx in (-1, 1):
    stack(R, 'gulp', [(Y0 + 2.0, Y0 + 3.4, 1.0, 4.4), (Y0 + 3.4, Y0 + 7.0, 1.5, 5.2), (Y0 + 7.0, Y0 + 8.4, 1.0, 4.4)], 'wood', c=(sx * (W + 0.1), 0))
for i in range(10):
    a = math.radians(i * 36); x, z = 12.5 * math.cos(a), 12.5 * math.sin(a); y = 8 + 3 * math.sin(a * 2)
    B('aura', (x - 0.8, y - 0.8, z - 0.14), (x + 0.8, y + 0.8, z + 0.14), 'gold', rot=('y', i * 36 + 90, (x, y, z)), light=12)
    if i % 2: B('aura', (x * 0.85 - 0.25, y + 2.0, z * 0.85 - 0.25), (x * 0.85 + 0.25, y + 2.5, z * 0.85 + 0.25), 'tooth', light=14)

# ---- the poses: the Mimic's own, the same dict (one rig: the wardrobe swaps models, never poses)
R.POSES = M.POSES
POSES = R.POSES
R.DRAFT = M.DRAFT


def swap(model_name):
    """the outfit's model for one of the Mimic's (mm_lid_xhappy_sh -> mmt_lid_xhappy_sh), or None (its doll parts: none here)"""
    n = PREFIX + model_name[len(M.R.PREFIX):]
    return n if n in _NAMES else None


_NAMES = set(R.models())
