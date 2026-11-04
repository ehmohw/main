"""(3.1 draft, stage 1: art only - not wired) THE MIMIC - a Black Market vault chest with teeth. (3rd pass, the owner: "should
look more like a MC chest" - so it IS one: the vanilla chest's own shape, texture and latch, with a creature fitted inside it.)

UNLOCK  In a heist vault (Tier III+, 1 run in 40), one of the loot chests "looks back at you": its latch twitches. Open it and it
        throws a TANTRUM - 30 seconds of snapping and hopping round the vault (it can't really hurt you: 1 heart a bite, and it
        spits your loot back if it eats any). Survive it - or hand it a Gutter Coin mid-tantrum, which it eats, delighted - and
        it calms down, licks you, and joins you (its summoning item: the Mimic's Key, a gold key with a tooth for a bit).

LOOK    A vanilla Minecraft chest, exactly: ChestModel's own boxes (read from the 26.3 client jar: the body 14 x 10 x 14, the lid
        14 x 5 x 14 hinged at the back, overlapping the body by 1 px, the small 2 x 4 x 1 latch on the lid's front) wearing the
        jar's own entity/chest texture, uv-mapped face by face as the game maps it (the planks, the dark outline edges, the
        latch's shadow, the black inside). RIG_SCALE 1.0: a disguised Mimic is a real chest's size.
        DISGUISED ('disguise'): feet tucked away, lid shut, no eyes ('disg'): just a chest. Nothing else shows - every creature
          part sits inside the closed volume.
        REVEALED: the lid lifts on two rows of tapered teeth (the lower row on the body's rim, the upper under the lid), a fat
          grooved tongue, the inside a dark crimson gum with a heap of gold coins (and a gem, and someone's dagger) in it; two
          big gold eyes open on the lid's front, either side of the latch - smug, a heavy lid; four small peg feet come out of its
          corners.
RIG     body (the root: the box, its rim teeth, the gum, the loot) - lid (hinged at the back: the lid, the latch, the upper teeth,
        the face: eyes per expression) - tongue (resting) / tonguel (the long tongue: the swallow, the stash) - feet ffr ffl fbr
        fbl; fx: 'coins' (a burst of spat coins), 'gulp' (cheeks puffed - a foe swallowed), 'aura' (the rare Jackpot aura).
STASH   'stash': opened wide, the long tongue laid out flat like a welcome mat, the loot showing - it is a small portable stash.
SKINS   all vanilla-shaped, each on a vanilla chest texture: '_sh' SHINY "Voidbox" (the ender chest's, turned violet: obsidian
        panels, violet banding, amethyst teeth, a starry violet gum). Cosmetics: '_crate' "Trapped Chest" (the trapped chest's
        texture: the red-marked latch - the heist's own trap), '_gild' "Christmas Chest" (the festive chest's red wrap and gold
        ribbon: the vault's showpiece)."""
import colorsys
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, planks, metal, glaze, eye, blush, mouth, put, slab, stack, ball,
                      chain, ring, van)

# ---- the vanilla chest's geometry (net/minecraft/client/model/object/chest/ChestModel.createSingleBodyLayer, 26.3), in design
# units (feet at y=0, facing -z): bottom box (1,0,1)+14x10x14; lid box (1,0,0)+14x5x14 at offset (0,9,1); lock box (7,-2,14)+2x4x1
# at offset (0,9,1). The latch is on the front (vanilla +z, here -z); the lid hinges at the back.
W, D = 7.0, 7.0                         # (half width, half depth: 14 x 14)
Y0 = 2.0                                # (the body's bottom: the feet's height)
Y1 = Y0 + 10.0                          # (the body's rim)
LY0, LY1 = Y0 + 9.0, Y0 + 14.0          # (the lid: 5 px, overlapping the body by 1)
th = 0.9                                # (the walls' thickness, inside)
E = 0.03                                # (the lid a hair proud of the body, so the 1-px overlap doesn't z-fight)

PIVOT = {'body': (0, Y0, 0), 'lid': (0, LY0, D), 'tongue': (0, 9.4, 2.0), 'tonguel': (0, 9.4, 2.0),
         'ffr': (4.9, Y0, -4.9), 'ffl': (-4.9, Y0, -4.9), 'fbr': (4.9, Y0, 4.9), 'fbl': (-4.9, Y0, 4.9),
         'coins': (0, 12, -10), 'gulp': (0, 8, 0), 'aura': (0, 0, 0), 'doll': (0, 1.4, 0), 'dolllid': (0, 9.0, 6.7)}
PARENT = {'body': None, 'lid': 'body', 'tongue': 'body', 'tonguel': 'body', 'ffr': 'body', 'ffl': 'body', 'fbr': 'body', 'fbl': 'body',
          'coins': None, 'gulp': 'body', 'aura': None, 'doll': None, 'dolllid': 'doll'}
FACES = ('disg', 'happy', 'greedy', 'fierce', 'blink', 'hurt', 'sleepy')
R = Rig('mm_', 1.0, PIVOT, PARENT, FACES, face_part='lid', opt=('tonguel', 'coins', 'gulp', 'aura', 'doll', 'dolllid'))
FEET = ('ffr', 'ffl', 'fbr', 'fbl')
SKIN_NAMES = {'_sh': 'SHINY: Voidbox (ender-chest style)', '_crate': 'cosmetic: Trapped Chest', '_gild': 'cosmetic: Christmas Chest'}

C = dict(van='normal', gum=('#3a0610', '#6a1220', '#8a1e2c'), tooth=('#fbf4e4', '#ffffff', '#e0d4bc'),
         tongue=('#b8304a', '#e0506a', '#f080a0', '#ffc0d0'), gold=('#a87010', '#f0c030', '#ffe070', '#fff8d0'), gem='#30d080',
         ruby='#e02040', brass=('#7a5410', '#c08a24', '#e8b84a', '#fff0a0'),
         eye_white='#fff6d8', iris=('#5a3000', '#a06008', '#e0a020', '#ffd040', '#fff090'), lash='#1a0e06', glow='#ffd23a')
SK = {'_sh': dict(van='ender', hue=0.77, gum=('#0a0820', '#181a40', '#2a2a6a'), tooth=('#e8d0ff', '#ffffff', '#b090e0'),
                  tongue=('#5a2090', '#8a3ab0', '#b060e0', '#e0b0ff'), gold=('#5a2aa0', '#b06aff', '#d8b0ff', '#ffffff'),
                  brass=('#3a1a70', '#7a40d0', '#b06aff', '#f0d8ff'),
                  iris=('#3a0a6a', '#6a2ab0', '#a060f0', '#d0a0ff', '#f8e8ff'), eye_white='#f4eaff'),
      '_crate': dict(van='trapped'),
      '_gild': dict(van='christmas', iris=('#0a3a10', '#1a6a20', '#30a040', '#70d070', '#c0f0b0'))}

# the face: an eye overlay on the lid's front, either side of the latch: 12 x 3.5 units (48 x 14 texels); eyes 12 x 13 at 12, 36
FW, FH = 12.0, 3.5
DFW, DFH, DEYC = 14.4, 6.4, (14, 44)          # (the doll's eye window on its lid front: 57.6 x 25.6 texels; eyes 18 x 19 at 14, 44)
EYC, EYY, EYW, EYH = (12, 36), 1, 12, 13


# ---------------------------------------------------------------------------------------------------- the vanilla chest's uv
def _px(u0, v0, u1, v1, flip=True):
    """a pixel window on the 64 x 64 chest texture -> a face uv (16ths). The jar's chest sheet is drawn upside down for its
    sides (ChestModel is built y-up on a y-down texture layout): flip mirrors the window back, top to bottom"""
    return [u0 / 4, v1 / 4, u1 / 4, v0 / 4] if flip else [u0 / 4, v0 / 4, u1 / 4, v1 / 4]


# vanilla's south face (the latch's, its front) is ours north; its west (-x) is ours east (the chest turned to face -z)
UV_BODY = {'north': _px(42, 33, 56, 43), 'south': _px(14, 33, 28, 43), 'east': _px(0, 33, 14, 43), 'west': _px(28, 33, 42, 43),
           'down': _px(14, 19, 28, 33, False), 'up': _px(28, 19, 42, 33, False)}
UV_LID = {'north': _px(42, 14, 56, 19), 'south': _px(14, 14, 28, 19), 'east': _px(0, 14, 14, 19), 'west': _px(28, 14, 42, 19),
          'up': _px(28, 0, 42, 14, False), 'down': _px(14, 0, 28, 14, False)}
UV_LOCK = {'north': _px(4, 1, 6, 5), 'south': _px(1, 1, 3, 5), 'east': _px(0, 1, 1, 5), 'west': _px(3, 1, 4, 5),
           'up': _px(1, 0, 3, 1, False), 'down': _px(3, 0, 5, 1, False)}


def _recreate():
    """a faithful recreation of entity/chest/normal (when the jar isn't unpacked): the same layout, the planks and the outline"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    out, pl = '#2c271e', ('#7f5f22', '#8f691d', '#a47227', '#ab792d')
    def panel(x0, y0, x1, y1, fill=None):
        d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=hexc(out))
        for y in range(y0 + 1, y1 - 1):
            for x in range(x0 + 1, x1 - 1):
                c = fill or (pl[0] if (y - y0) % 4 == 0 else pl[1 + (x * 7 + y * 3) % 3])
                im.putpixel((x, y), hexc(c))
    for (y0, h) in ((14, 5), (33, 10)):
        for k in range(4): panel(14 * k, y0, 14 * k + 14, y0 + h)
    panel(14, 0, 28, 14, '#392600'); panel(28, 0, 42, 14); panel(14, 19, 28, 33); d.rectangle((28, 19, 41, 32), fill=(0, 0, 0, 255))
    d.rectangle((0, 1, 5, 4), fill=hexc('#767676')); d.rectangle((1, 0, 4, 0), fill=hexc('#cdcdcd'))
    return im


def chest_tex(name='normal', hue=None):
    """the vanilla chest sheet (entity/chest/<name>); hue: every coloured pixel turned to that hue (0-1), its lightness and
    saturation kept and lifted a little (the Voidbox: the ender chest gone violet, its eye and its latch too)"""
    im = van(f'entity/chest/{name}', _recreate)
    if hue:
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b, a = px[x, y]
                if not a: continue
                h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
                r2, g2, b2 = colorsys.hls_to_rgb(hue, min(1, l * 1.12), min(1, s * 1.3 + 0.08))
                px[x, y] = (int(r2 * 255), int(g2 * 255), int(b2 * 255), a)
    return im


def chest_pal(im):
    """the sheet's own wood: (seam, dark, base, light) from the body's front panel, for the parts vanilla hasn't got (feet, cheeks)"""
    px = im.load()
    vs = sorted({px[x, y][:3] for x in range(43, 55) for y in range(34, 42)}, key=lambda c: 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2])
    h = lambda c: '#%02x%02x%02x' % c
    return (h(px[45, 33][:3]), h(vs[len(vs) // 6]), h(vs[len(vs) // 2]), h(vs[len(vs) * 5 // 6]))


def chest_boxes(rig, body='body', lid='lid', tex='chest', y0=0.0, open_lid=False):
    """the vanilla chest itself (for a reference render beside the Mimic): its three boxes on the given parts"""
    rig.box(body, (-W, y0, -D), (W, y0 + 10, D), tex, uv=UV_BODY)
    rig.box(lid, (-W, y0 + 9, -D), (W, y0 + 14, D), tex, uv=UV_LID)
    rig.box(lid, (-1, y0 + 7, -D - 1), (1, y0 + 11, -D), tex, uv=UV_LOCK)


# ---------------------------------------------------------------------------------------------------- textures
def _wood(c, seed, board=6):
    seam, dk, base, lt = c['_pal']
    return lit(planks((seam, dk, base, lt), seed, board, nails=False), 1.06, 0.92, 8)


def _face(kind, c):
    return _wood(c, 31, 7)


def _eyes(kind, c):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    if kind == 'disg': return im
    for i, cx in enumerate(EYC):
        k = {'greedy': 'wide', 'fierce': 'fierce', 'sleepy': 'sleepy'}.get(kind, kind)
        eye(im, cx, EYY, EYW, EYH, i == 1, k, iris=c['iris'], lash=c['lash'], white=c['eye_white'], pupil='#1a0a00',
            lid=4 if kind is None else None)
        if kind == 'greedy':                                                 # (gold coins in its eyes: a $ glint)
            for dy in range(3, 10): put(im, cx, EYY + dy, '#fff8d0')
    return im


def _deyes(c):
    """the doll's eyes: two big glossy all-iris kawaii eyes (sclera=False) and a blush under each, on the doll lid's front"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for i, cx in enumerate(DEYC):
        eye(im, cx, 3, 18, 19, i == 1, None, iris=c['iris'], lash=c['lash'], pupil='#1a0a00', sclera=False, irk=0.62)
        blush(im, cx + (-5 if i == 0 else 5), 23, 6, '#f08a8a')
    return im


def textures(c):
    ch = chest_tex(c['van'], c.get('hue'))
    c = dict(c, _pal=chest_pal(ch)); seam, dk, base, lt = c['_pal']
    t = {'chest': ch, 'wood': _wood(c, 1), 'dark': soft(seam, dk, mix(seam, '#000000', 0.3), 4, 0.15),
         'rim': soft(seam, mix(seam, dk, 0.4), mix(seam, '#000000', 0.25), 5, 0.12),
         'gum': soft(c['gum'][1], c['gum'][2], c['gum'][0], 8, 0.06), 'throat': soft(c['gum'][1], c['gum'][2], c['gum'][0], 9, 0.05),
         'tooth': lit(soft(c['tooth'][0], c['tooth'][1], c['tooth'][2], 10, 0.08), 1.04, 0.9, 8),
         'tongue': glaze(c['tongue'], 11, 3), 'gold': glaze((c['gold'][0], c['gold'][1], c['gold'][2], c['gold'][3]), 12, 2),
         'gem': soft(c['gem'], mix(c['gem'], '#ffffff', 0.5), mix(c['gem'], '#000000', 0.3), 13, 0.3),
         'ruby': soft(c['ruby'], mix(c['ruby'], '#ffffff', 0.5), mix(c['ruby'], '#000000', 0.3), 14, 0.3),
         'brass': metal(c['brass'], 7), 'grip': soft('#4a2a14', '#6a4020', '#2a1608', 17, 0.2), 'eyes': _eyes(None, c), 'deyes': _deyes(c)}
    for f in FACES: t[f'eyes_{f}'] = _eyes(f, c)
    return t


TEX = textures(C)
for k, v in TEX.items(): R.tex(k, v)
for sfx, ch_ in SK.items():
    for k, v in textures(dict(C, **ch_)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in TEX})

# ---------------------------------------------------------------------------------------------------- the model
B = R.box
# ---- the body: vanilla's bottom box, its outer faces in the jar's texture; open on top (it's a mouth)
B('body', (-W, Y0, -D), (W, Y1, D), 'chest', faces=('north', 'south', 'east', 'west', 'down'), uv=UV_BODY)
# the gum lining its walls (facing in), their tops the dark rim you see round the mouth; a gum floor under the loot
FLOOR = Y0 + 5.4
for a, b, f in (((-W + 0.02, Y0 + 0.5, -D + 0.02), (W - 0.02, Y1, -D + th), 'south'), ((-W + 0.02, Y0 + 0.5, D - th), (W - 0.02, Y1, D - 0.02), 'north'),
                ((-W + 0.02, Y0 + 0.5, -D + th), (-W + th, Y1, D - th), 'east'), ((W - th, Y0 + 0.5, -D + th), (W - 0.02, Y1, D - th), 'west')):
    e = B('body', a, b, 'gum', faces=(f, 'up'))
    e['faces']['up']['texture'] = '#rim'
B('body', (-W + th, Y0 + 0.5, -D + th), (W - th, FLOOR, D - th), 'gum', faces=('up',))
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
LOW = [(-6.0 + i * 1.2, -D + 0.7, (1.25 if i in (0, 10) else 0.8 + 0.2 * (i % 2))) for i in range(11)] + \
      [(sx * (W - 0.7), -4.8 + j * 1.6, 0.75 + 0.15 * (j % 2)) for sx in (-1, 1) for j in range(6)]
teeth('body', Y1, True, LOW)
# the loot inside: a heap of coins, a gem, a ruby, a dagger's hilt sticking up
for i in range(26):
    x, z = rt.uniform(-5.4, 5.4), rt.uniform(-4.8, 5.0); y = FLOOR + max(0.0, 2.2 - 0.05 * (x * x + (z - 0.8) ** 2)) + rt.uniform(0, 0.3)
    B('body', (x - 0.6, y, z - 0.6), (x + 0.6, y + 0.22, z + 0.6), 'gold', rot=('y', rt.uniform(-40, 40), (x, y, z)), light=3)
ball(R, 'body', (-2.8, FLOOR + 2.0, 1.6), 0.65, 'gem', 3, light=6); ball(R, 'body', (3.4, FLOOR + 1.6, 2.4), 0.5, 'ruby', 2, light=6)
R.seg('body', (1.8, FLOOR + 0.4, 3.2), (2.6, FLOOR + 4.0, 4.0), 0.42, 0.42, 'grip'); B('body', (1.6, FLOOR + 3.8, 3.4), (3.0, FLOOR + 4.1, 4.4), 'brass')
B('body', (2.4, FLOOR + 4.1, 3.7), (2.9, FLOOR + 4.6, 4.1), 'brass')
# ---- the lid: vanilla's lid box (its underside the dark inside of the lid, a gum roof inset in it) and the latch
B('lid', (-W - E, LY0, -D - E), (W + E, LY1 + E, D + E), 'chest', uv=UV_LID)
B('lid', (-W + th, LY0 - 0.04, -D + th), (W - th, LY0 - 0.02, D - th), 'throat', faces=('down',))
B('lid', (-1, Y0 + 7, -D - 1 - E), (1, Y0 + 11, -D - E), 'chest', uv=UV_LOCK, faces=('north', 'east', 'west', 'up', 'down'))
# the eyes on the lid's front, either side of the latch (the overlay: the jar's planks stay under them)
B('lid', (-FW / 2, LY0 + 0.75, -D - E - 0.04), (FW / 2, LY0 + 0.75 + FH, -D - E - 0.02), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]}, light=8)
# the upper teeth hanging under the lid's front and sides
UP = [(-5.4 + i * 1.2, -D + 0.75, (1.15 if i in (0, 9) else 0.75 + 0.2 * ((i + 1) % 2))) for i in range(10)] + \
     [(sx * (W - 0.75), -4.0 + j * 1.6, 0.7 + 0.15 * (j % 2)) for sx in (-1, 1) for j in range(5)]
teeth('lid', LY0, False, UP)
# ---- the tongue: fat, a groove down its middle, resting in the coins; the long one rolled out over the rim (swallow, stash)
for (z0, z1, w, y) in ((2.0, -0.5, 2.0, 9.6), (-0.5, -2.8, 1.8, 9.9), (-2.8, -4.4, 1.4, 10.3)):
    R.seg('tongue', (0, y, z0), (0, y + 0.1, z1), w * 1.6, 0.8, 'tongue', ext=0.15)
R.seg('tongue', (0, 10.05, 1.5), (0, 10.55, -3.8), 0.3, 0.12, 'gum')
pts = [(0, 9.6, 2.0), (0, 10.2, -1.5), (0, 11.4, -5.0), (0, 12.6, -7.6), (0, 9.0, -9.6), (0, 4.6, -10.8), (0, 0.6, -11.6), (0, 0.2, -14.4),
       (0, 0.2, -17.4)]
for i in range(len(pts) - 1):
    w = 3.2 - 0.12 * i
    R.seg('tonguel', pts[i], pts[i + 1], w, 0.8, 'tongue', ext=0.2)
    R.seg('tonguel', (pts[i][0], pts[i][1] + 0.42, pts[i][2]), (pts[i + 1][0], pts[i + 1][1] + 0.42, pts[i + 1][2]), 0.3, 0.1, 'gum')
# ---- the feet: small and simple - a stubby peg of its own wood, a dark pad, three little toes
for p in FEET:
    x, y, z = PIVOT[p]
    B(p, (x - 0.9, 0.7, z - 0.9), (x + 0.9, y + 0.2, z + 0.9), 'wood')
    B(p, (x - 1.2, 0.0, z - 1.3), (x + 1.2, 0.8, z + 1.1), 'dark')
    for dx in (-0.75, 0.0, 0.75):
        B(p, (x + dx - 0.3, 0.0, z - 1.8), (x + dx + 0.3, 0.55, z - 1.3), 'dark')
# ---- fx: the spat coins, the puffed cheeks of a gulp, the Jackpot aura
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


# ---- THE DOLL (opt parts 'doll' + 'dolllid', shown only by the 'doll' pose; Cecil's doll is baked from it): a chibi chest - the
# body squat (8.2 of 14) under a big lid (6.4, a hair wider, a rounded cap on top) joined at the hinge and ajar, so the teeth peek
# out; big glossy kawaii eyes with a blush, a blep of tongue over the rim, four tiny feet. The same vanilla texture and uv.
DY0, DY1, DL0, DL1 = 1.4, 9.6, 9.0, 15.4
B('doll', (-W, DY0, -6.5), (W, DY1, 6.5), 'chest', faces=('north', 'south', 'east', 'west', 'down'), uv=UV_BODY)
B('doll', (-W + 0.7, DY1 - 0.4, -5.8), (W - 0.7, DY1 - 0.2, 5.8), 'gum', faces=('up',))
for a, b, f in (((-W + 0.02, DY1 - 2.0, -6.48), (W - 0.02, DY1, -5.8), 'south'), ((-W + 0.02, DY1 - 2.0, -5.8), (-W + 0.7, DY1, 5.8), 'east'),
                ((W - 0.7, DY1 - 2.0, -5.8), (W - 0.02, DY1, 5.8), 'west'), ((-W + 0.02, DY1 - 2.0, 5.8), (W - 0.02, DY1, 6.48), 'north')):
    e = B('doll', a, b, 'gum', faces=(f, 'up')); e['faces']['up']['texture'] = '#rim'
teeth('doll', DY1, True, [(-5.2 + i * 1.73, -6.0, (1.15 if i in (0, 6) else 0.85)) for i in range(7)])
R.seg('doll', (2.9, DY1 - 0.1, -3.6), (3.0, DY1 + 0.15, -6.7), 2.1, 0.6, 'tongue', ext=0.1)             # (a blep, over the rim)
R.seg('doll', (3.0, DY1 + 0.1, -6.8), (3.1, DY1 - 1.6, -7.05), 2.0, 0.5, 'tongue', ext=0.15)
for sx in (-1, 1):
    for sz in (-1, 1):
        x, z = sx * 4.9, sz * 4.4
        B('doll', (x - 1.1, 0.0, z - 1.1), (x + 1.1, DY0 + 0.2, z + 1.1), 'dark')
        B('doll', (x - 0.9, 0.0, z - 1.6), (x + 0.9, 0.6, z - 1.1), 'dark')
B('dolllid', (-W - 0.2, DL0, -6.7), (W + 0.2, DL1, 6.7), 'chest', uv=UV_LID)
B('dolllid', (-W + 0.5, DL1, -6.0), (W - 0.5, DL1 + 0.5, 6.0), 'chest', uv={**UV_LID, 'up': UV_LID['up']})    # (the rounded cap)
B('dolllid', (-W + 0.7, DL0 - 0.04, -6.0), (W - 0.7, DL0 - 0.02, 6.0), 'throat', faces=('down',))
B('dolllid', (-1.2, DL0 - 1.8, -7.8), (1.2, DL0 + 2.6, -6.7), 'chest', uv=UV_LOCK, faces=('north', 'east', 'west', 'up', 'down'))
B('dolllid', (-DFW / 2, DL0 + 0.0, -6.76), (DFW / 2, DL0 + DFH, -6.74), 'deyes', faces=('north',), uv={'north': [0, 0, DFW, DFH]}, light=8)
teeth('dolllid', DL0, False, [(-4.4 + i * 1.76, -5.9, 0.8 + 0.15 * (i % 2)) for i in range(6)])


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
    # the doll's source (dolls_bake reads it; never shown in play): the chibi chest alone, lid ajar on its teeth
    'doll': P(_show=('doll', 'dolllid'), _hide=('body', 'lid', 'tongue') + FEET, dolllid=lid(13)),
})
DRAFT = ['disguise', 'idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'sit_a', 'sit_b', 'snap_up', 'snap', 'swallow', 'gulp', 'spit',
         'stash', 'tantrum', 'hurt', 'aura']
R.DRAFT = DRAFT
# THE DOLL: baked from the 'doll' pose (DOLL_POSE), not idle_a. Its chibi proportions are in its own geometry (the big lid, the squat
# body, the big eyes, the tiny feet), and the whole chest is ONE 'head' mass (DOLL_GROUPS), so the default warp grows lid and body
# together, joined at the hinge (warping the lid alone blew it up off the body). width/height: dolls_bake's fit, so it stands in its
# own shelf slot (0.72 blocks) the size of the dolls beside it (Cecil 10 wide, the Gem 9; about 11 x 12 here).
DOLL_POSE = 'doll'
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, 'width': 11.0, 'height': 12.5}
DOLL_GROUPS = {'doll': 'head', 'dolllid': 'head'}
SHINY = 'Shiny Voidbox'
