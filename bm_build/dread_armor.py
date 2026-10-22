"""2.90b: THE DREAD'S ARMOUR - what a Dread monster wears, its own and nothing like netherite.

THE DREAD VISAGE  (the helmet) a true 3D model worn on the head: a hood of black chitin that swallows the face. A ring of red
                  eyes across its brow, more eyes opening on its sides; a slit of a maw with teeth down the front, mandibles
                  at the jaw; two great bone horns sweeping out and back; a crown of spines along its crest; tendrils of dark
                  flesh hanging down its back. (A head item with no armour asset is drawn as its own model on the head, as
                  the True Crown is.)
THE PLATE         (chest, legs, feet) an armour layer of its own (asset bm:dread): black void-plate cracked with red light,
                  bone ribs over the breast, an eye staring from the sternum, bony knee-caps,
                  clawed boots.

Model space for the helmet: drawn for a head filling 3..13 on every axis (its head display scales it 1.28 to the 1.6..14.4
the head really fills); the front is north (-z)."""
import random
from PIL import Image, ImageDraw

from phase57_art import hexc

VOID, VOID_LT, VOID_DK = '#16101a', '#2c2030', '#08060a'
RED, RED_LT, RED_DK = '#d0182e', '#ff5a64', '#6a0812'
BONE, BONE_LT, BONE_DK = '#d8ccb0', '#f4ecd8', '#9a8c70'
FLESH, FLESH_LT, FLESH_DK = '#5a1420', '#86283a', '#30080e'


# ---------------------------------------------------------------------------------------------------- the helmet's textures
def _px(n=16):
    return Image.new('RGBA', (n, n), (0, 0, 0, 0))


def _chitin(seed):
    """black chitin plates: dark seams, a lit edge on each plate, hairline red cracks"""
    rnd = random.Random(seed); im = Image.new('RGBA', (32, 32), hexc(VOID)); d = ImageDraw.Draw(im)
    for _ in range(90):
        im.putpixel((rnd.randrange(32), rnd.randrange(32)), hexc(rnd.choice([VOID_LT, VOID_DK, '#1e1622'])))
    for y in (7, 15, 23, 31):                                       # plate seams, a lit lip over each
        d.line((0, y, 31, y), fill=hexc(VOID_DK)); d.line((0, y - 1, 31, y - 1), fill=hexc('#3a2a40'))
    for x0 in (5, 19):
        d.line((x0, 0, x0, 31), fill=hexc(VOID_DK))
    for _ in range(4):                                              # cracks of red light
        x, y = rnd.randrange(32), rnd.randrange(32)
        for _s in range(7):
            if 0 <= x < 32 and 0 <= y < 32: im.putpixel((x, y), hexc(RED))
            x += rnd.choice((-1, 0, 1)); y += 1
    return im.resize((64, 64), Image.NEAREST)


def _face():
    """the Visage's front (whole-face uv): a ring of red eyes across the brow, a slit of a maw with teeth below"""
    im = Image.new('RGBA', (32, 32), hexc(VOID)); d = ImageDraw.Draw(im); rnd = random.Random(7)
    for _ in range(60):
        im.putpixel((rnd.randrange(32), rnd.randrange(32)), hexc(rnd.choice([VOID_LT, VOID_DK])))
    d.line((0, 0, 31, 0), fill=hexc('#3a2a40'))
    for (cx, cy, r) in ((16, 9, 3), (9, 8, 2), (23, 8, 2), (4, 11, 1), (28, 11, 1), (12, 4, 1), (20, 4, 1)):
        d.ellipse((cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1), fill=hexc(VOID_DK))       # the socket
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hexc(RED))                           # the eye
        d.line((cx, cy - r + 1, cx, cy + r - 1), fill=hexc('#160204'))                         # a slit pupil
        im.putpixel((cx - r + 1 if r > 1 else cx - 1, cy - r + 1 if r > 1 else cy - 1), hexc(RED_LT))   # its glint
    d.polygon([(13, 17), (19, 17), (18, 30), (14, 30)], fill=hexc('#0a0204'))                # the maw
    for y in range(18, 30, 2):                                                                 # its teeth
        d.line((13, y, 15, y + 1), fill=hexc(BONE)); d.line((19, y, 17, y + 1), fill=hexc(BONE))
    d.line((14, 30, 18, 30), fill=hexc(RED_DK))
    for x in (6, 26):                                                                          # cheek ridges
        d.line((x, 15, x + (3 if x < 16 else -3), 29), fill=hexc('#3a2a40'))
    return im.resize((64, 64), Image.NEAREST)


def _bone(seed, tip=False):
    rnd = random.Random(seed); base = BONE if not tip else '#5a4a40'
    im = Image.new('RGBA', (16, 16), hexc(base)); d = ImageDraw.Draw(im)
    for y in range(0, 16, 4):                                       # growth rings
        d.line((0, y, 15, y), fill=hexc(BONE_DK if not tip else '#2a2020')); d.line((0, y + 1, 15, y + 1), fill=hexc(BONE_LT if not tip else '#7a6656'))
    for _ in range(8):
        im.putpixel((rnd.randrange(16), rnd.randrange(16)), hexc(BONE_DK if not tip else '#3a2c26'))
    return im.resize((32, 32), Image.NEAREST)


def _eye():
    im = Image.new('RGBA', (8, 8), hexc(VOID_DK)); d = ImageDraw.Draw(im)
    d.rectangle((1, 1, 6, 6), fill=hexc(RED)); d.rectangle((3, 1, 4, 6), fill=hexc('#160204'))
    im.putpixel((1, 1), hexc(RED_LT)); im.putpixel((2, 1), hexc(RED_LT))
    return im.resize((32, 32), Image.NEAREST)


def _flesh(seed):
    rnd = random.Random(seed); im = Image.new('RGBA', (16, 16), hexc(FLESH)); d = ImageDraw.Draw(im)
    for x in range(0, 16, 3):
        d.line((x, 0, x, 15), fill=hexc(FLESH_DK))
    for _ in range(14):
        im.putpixel((rnd.randrange(16), rnd.randrange(16)), hexc(rnd.choice([FLESH_LT, RED_DK])))
    for y in range(2, 16, 5):                                       # suckers
        im.putpixel((8, y), hexc(FLESH_LT)); im.putpixel((9, y), hexc(FLESH_LT))
    return im.resize((32, 32), Image.NEAREST)


def helm_textures():
    return {'dread_chitin': _chitin(301), 'dread_face': _face(), 'dread_bone': _bone(302), 'dread_bone_tip': _bone(303, True),
            'dread_eye': _eye(), 'dread_flesh': _flesh(304)}


# ---------------------------------------------------------------------------------------------------- the helmet's model
def _box(fr, to, tex, uv_full=(), faces=None):
    w = {'north': (to[0] - fr[0], to[1] - fr[1]), 'south': (to[0] - fr[0], to[1] - fr[1]), 'east': (to[2] - fr[2], to[1] - fr[1]),
         'west': (to[2] - fr[2], to[1] - fr[1]), 'up': (to[0] - fr[0], to[2] - fr[2]), 'down': (to[0] - fr[0], to[2] - fr[2])}
    out = {}
    for f in (faces or w):
        a, b = (round(min(16, max(0.25, v)), 3) for v in w[f])
        out[f] = {'uv': [0, 0, 16, 16] if f in uv_full else [0, 0, a, b], 'texture': '#' + tex}
    return {'from': [round(v, 3) for v in fr], 'to': [round(v, 3) for v in to], 'faces': out}


def _mx(fr, to):
    """the same box mirrored across the head's middle (x -> 16 - x)"""
    return (16 - to[0], fr[1], fr[2]), (16 - fr[0], to[1], to[2])


def helm_model():
    E = []
    E.append(_box((2.4, 2.4, 2.6), (13.6, 13.4, 13.6), 'dread_chitin'))                                  # the hood (down past the chin)
    E.append(_box((2.3, 2.2, 2.4), (13.7, 13.2, 2.6), 'dread_face', uv_full=('north',), faces=('north',)))   # its face
    E.append(_box((3.4, 13.4, 3.6), (12.6, 14.8, 12.6), 'dread_chitin'))                                 # the crest
    E.append(_box((5.0, 14.8, 5.0), (11.0, 15.6, 11.4), 'dread_chitin'))
    E.append(_box((3.0, 2.4, 10.0), (13.0, 4.8, 13.4), 'dread_chitin'))                                  # the nape guard
    for fr, to in (((2.0, 1.6, 1.6), (4.6, 5.4, 4.4)),):                                                  # mandibles at the jaw...
        E += [_box(fr, to, 'dread_chitin'), _box(*_mx(fr, to), 'dread_chitin')]
    for fr, to in (((3.6, 0.4, 1.4), (4.6, 1.8, 2.6)),):                                                  # ...each ending in a fang
        E += [_box(fr, to, 'dread_bone'), _box(*_mx(fr, to), 'dread_bone')]
    # the horns: out from the temples, sweeping back and up, bone to a dark tip
    HORN = [((0.6, 2.6), (10.4, 13.0), (6.6, 9.6), 'dread_bone'),
            ((-1.0, 1.0), (12.2, 15.4), (7.8, 10.8), 'dread_bone'),
            ((-1.8, 0.0), (14.8, 18.4), (9.4, 12.2), 'dread_bone'),
            ((-1.6, -0.2), (17.8, 21.0), (11.2, 13.6), 'dread_bone'),
            ((-0.8, 0.4), (20.4, 23.2), (12.8, 14.8), 'dread_bone_tip')]
    for (x0, x1), (y0, y1), (z0, z1), t in HORN:
        E += [_box((x0, y0, z0), (x1, y1, z1), t), _box(*_mx((x0, y0, z0), (x1, y1, z1)), t)]
    # a crown of spines along the crest, tallest in the middle
    for x, h in ((4.6, 2.2), (6.4, 3.6), (8.0, 4.8), (9.6, 3.6), (11.4, 2.2)):
        E.append(_box((x - 0.5, 15.4, 8.2), (x + 0.5, 15.4 + h, 9.2), 'dread_bone'))
        E.append(_box((x - 0.3, 15.4 + h, 8.4), (x + 0.3, 16.2 + h, 9.0), 'dread_bone_tip'))
    # more eyes, opening on its sides and crest
    for (x, y, z) in ((2.1, 9.6, 6.0), (2.1, 7.0, 9.4), (13.0, 10.4, 7.6), (13.0, 7.4, 4.6), (6.0, 14.6, 4.2), (10.6, 14.6, 5.6)):
        s = 0.7
        E.append(_box((x, y - s, z - s), (x + 0.9, y + s, z + s), 'dread_eye', uv_full=('north', 'south', 'east', 'west', 'up', 'down')))
    # tendrils hanging down the back, each thinning to its tip
    for x, sway in ((4.4, -0.6), (7.0, 0.4), (9.4, -0.3), (11.8, 0.6)):
        y, z, w = 4.0, 13.4, 1.5
        for k in range(4):
            L = 2.6 - k * 0.3
            E.append(_box((x - w / 2 + sway * k * 0.4, y - L, z), (x + w / 2 + sway * k * 0.4, y, z + w), 'dread_flesh'))
            y -= L - 0.2; z += 0.3; w *= 0.8
    return E


def helm_json():
    tex = helm_textures()
    els = helm_model()
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    return tex, {'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/dread_chitin'), 'elements': els,
                 'display': {'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.28, 1.28, 1.28]},   # (the head fills 1.6..14.4 worn: drawn for 3..13)
                             'gui': {'rotation': [25, 200, 0], 'translation': [0, -3.5, 0], 'scale': [0.6, 0.6, 0.6]},
                             'ground': {'rotation': [0, 0, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]},
                             'fixed': {'rotation': [0, 180, 0], 'translation': [0, -3, 0], 'scale': [0.6, 0.6, 0.6]}}}


# ---------------------------------------------------------------------------------------------------- the plate (armour layers)
def _recolor(im):
    """netherite's shading carried over to the void: its darks black, its lights a dim violet-grey"""
    px = im.load(); lo, hi = hexc(VOID_DK)[:3], hexc('#4a3a50')[:3]
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            t = min(1.0, (r + g + b) / 765 * 1.6) ** 1.1
            px[x, y] = tuple(int(lo[c] + (hi[c] - lo[c]) * t) for c in range(3)) + (a,)
    return im


def _put(px, im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height and px[x, y][3]: px[x, y] = hexc(c)


def _eye_at(px, im, cx, cy):
    for dx in (-1, 0, 1, 2):
        _put(px, im, cx + dx, cy, RED)
    _put(px, im, cx, cy, '#160204'); _put(px, im, cx + 1, cy, '#160204')
    _put(px, im, cx - 1, cy - 1, VOID_DK); _put(px, im, cx + 2, cy - 1, VOID_DK)
    _put(px, im, cx, cy - 1, RED_LT)


def layer(van_png, kind, seed=90):
    im = _recolor(Image.open(van_png).convert('RGBA')); px = im.load(); rnd = random.Random(seed)
    for _ in range(30 if kind == 'humanoid' else 18):                    # cracks of red light, branching as they go down
        x, y = rnd.randrange(im.width), rnd.randrange(im.height)
        for _s in range(rnd.randint(3, 7)):
            _put(px, im, x, y, RED if rnd.random() < 0.8 else RED_LT)
            x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1, 1))
    if kind == 'humanoid':
        for y in (22, 25, 28):                                            # bone ribs over the breast (the body's front: x 20..27)
            for x in range(20, 28):
                if x not in (23, 24): _put(px, im, x, y + (1 if x in (20, 27) else 0), BONE_DK if x in (20, 27) else BONE)
            _put(px, im, 21, y - 1, BONE_LT); _put(px, im, 26, y - 1, BONE_LT)
        for y in range(20, 31):                                           # the sternum
            _put(px, im, 23, y, BONE_DK); _put(px, im, 24, y, BONE)
        _eye_at(px, im, 23, 21)                                           # an eye staring out of the breastbone
        for x in range(0, 16, 2):                                         # claws on the boots' toes (the legs' fronts, bottom row)
            _put(px, im, x, 31, BONE)
    else:
        for (x, y) in ((4, 22), (5, 22), (4, 23), (5, 23)):               # bony knee-caps
            _put(px, im, x, y, BONE)
        _put(px, im, 4, 21, BONE_LT)
    return im


def rp(R, van):
    def post(R2):
        tex, model = helm_json()
        for k, im in tex.items(): im.save(R2.p('assets', 'bm', 'textures', 'block', f'{k}.png'))
        R2.wj('assets/bm/models/item/dread_helm.json', model)
        R2.wj('assets/bm/items/dread_helm.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/dread_helm'}})
        for kind in ('humanoid', 'humanoid_leggings'):
            layer(f'{van}/entity/equipment/{kind}/netherite.png', kind).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', kind, 'dread.png'))
        R2.wj('assets/bm/equipment/dread.json', {'layers': {'humanoid': [{'texture': 'bm:dread'}], 'humanoid_leggings': [{'texture': 'bm:dread'}]}})
    R.POST.append(post)
