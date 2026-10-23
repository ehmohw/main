"""2.92: the Underwater Kingdom's gear, drawn - from the owner's art in ref/ where there is art.

LEO'S AEGIS       ref/leo_shield.png - the knight's heater shield (slate rim, navy field, the kingdom's insignia: a sea-glass
                  teardrop round a magenta gem), a 64x64 sprite extruded into the hand, raised in front of you when blocking.
EMMA'S CRESCENT   ref/emma_axe.png - her crescent axe (sea-glass blade, the pink flower and its gem at the head), extruded.
THE INSIGNIA      ref/insignia.png - the teardrop and its gem, for the plaques on the castle's walls and the Tidewarden's breast.
THE CROWN OF THE DEEP  ref/crown.png, built in boxes: a band of sea-gold, four arches meeting at the crown's top under a
                  violet diamond, sea-blue gems in the arches, a green cabochon at the front.
THE TIDEWARDEN'S HELM  a knight's great helm in Leo's steel blue: a visor slit, cheek guards, a sea-glass fin crest and the
                  insignia's gem on the brow.        THE PEARLGUARD TIARA  a silver circlet of pearls, the pink flower and gem.
THE PLATE         armour layers: the Tidewarden's steel-blue plate trimmed in sea-glass with the insignia on the breast; the
                  Pearlguard's pearl-white scale trimmed in rose.
Model space for the helms and the crown: drawn for a head filling 3..13 on every axis (head display x1.28, as dread_armor)."""
import os
from PIL import Image, ImageDraw

from phase57_art import hexc

HERE = os.path.dirname(os.path.abspath(__file__))
REF = lambda n: os.path.join(HERE, 'ref', n)

STEEL, STEEL_LT, STEEL_DK = '#4f6f92', '#86a6c4', '#2a3e58'
GLASS, GLASS_LT, GLASS_DK = '#a6dcea', '#e2f6fb', '#3f7f96'
GEM, GEM_LT, GEM_DK = '#a8237a', '#e05cb4', '#5c0e42'
GOLD, GOLD_LT, GOLD_DK = '#c9d23a', '#f0f48a', '#7d8a1a'
SEA, SEA_LT = '#2a6ad0', '#7ab8ff'
PEARL, PEARL_LT, PEARL_DK = '#ece6f0', '#ffffff', '#b8aec4'
ROSE, ROSE_LT = '#ff5ac8', '#ffaae4'


# ---------------------------------------------------------------------------------------------------- sprites from the owner's art
def _largest(im):
    """the stray splashes round the insignia dropped: opaque islands far smaller than the biggest (the gem stays)"""
    px = im.load(); w, h = im.size; seen = set(); comps = []
    for y in range(h):
        for x in range(w):
            if (x, y) in seen or px[x, y][3] == 0: continue
            comp, st = [], [(x, y)]; seen.add((x, y))
            while st:
                cx, cy = st.pop(); comp.append((cx, cy))
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen and px[nx, ny][3]:
                        seen.add((nx, ny)); st.append((nx, ny))
            comps.append(comp)
    big = max(len(c) for c in comps)
    keep = {p for c in comps if len(c) >= big * 0.06 for p in c}
    for y in range(h):
        for x in range(w):
            if px[x, y][3] and (x, y) not in keep: px[x, y] = (0, 0, 0, 0)
    return im


def _fit(src, size, crop=None, pad=1, largest=False):
    im = Image.open(src).convert('RGBA')
    if crop: im = im.crop(crop)
    bb = im.getbbox(); im = im.crop(bb)
    s = (size - 2 * pad) / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
    px = out.load()                                   # (hard edges: the extruder wants alpha 0 or 255)
    for y in range(size):
        for x in range(size):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255) if a >= 110 else (0, 0, 0, 0)
    return _largest(out) if largest else out


def aegis_sprite():
    return _fit(REF('leo_shield.png'), 64)


def crescent_sprite():
    return _fit(REF('emma_axe.png'), 64)


def insignia_sprite(size=64):
    # (the teardrop and its gem; the little splashes round it left out)
    return _fit(REF('insignia.png'), size, crop=(120, 20, 525, 640), largest=True)


def icon_from(im, size=16):
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------------------------------------------- small pixel textures for the 3D pieces
def _solid(c, c2=None, size=16, noise=()):
    im = Image.new('RGBA', (size, size), hexc(c)); d = ImageDraw.Draw(im)
    if c2:
        for x in range(size): d.point((x, 0), fill=hexc(c2)); d.point((0, x), fill=hexc(c2))
    for (x, y, col) in noise: d.point((x, y), fill=hexc(col))
    return im


def _gem(c, lt, dk):
    im = Image.new('RGBA', (16, 16), hexc(c)); d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (16, 0), (8, 8)], fill=hexc(lt)); d.polygon([(0, 16), (16, 16), (8, 8)], fill=hexc(dk))
    d.rectangle((5, 3, 7, 5), fill=hexc('#ffffff'))
    return im


def piece_textures():
    import random
    rnd = random.Random(2920)
    gold_n = [(rnd.randrange(16), rnd.randrange(16), rnd.choice((GOLD_LT, GOLD_DK))) for _ in range(30)]
    steel_n = [(rnd.randrange(16), rnd.randrange(16), rnd.choice((STEEL_LT, STEEL_DK))) for _ in range(28)]
    pearl_n = [(rnd.randrange(16), rnd.randrange(16), rnd.choice((PEARL_LT, PEARL_DK))) for _ in range(24)]
    visor = _solid(STEEL_DK); d = ImageDraw.Draw(visor)
    d.rectangle((0, 0, 15, 15), fill=hexc(STEEL)); d.rectangle((1, 6, 14, 8), fill=hexc('#0c141e'))
    d.rectangle((7, 9, 8, 15), fill=hexc(STEEL_DK)); d.line((1, 5, 14, 5), fill=hexc(STEEL_LT))
    for x in range(2, 14, 3): d.point((x, 11), fill=hexc('#0c141e')); d.point((x, 13), fill=hexc('#0c141e'))
    return {'kg_gold': _solid(GOLD, None, noise=gold_n), 'kg_seagem': _gem(SEA, SEA_LT, '#163c80'), 'kg_violet': _gem('#a040e0', '#e0a0ff', '#4a1880'),
            'kg_green': _gem('#20a070', '#7ae0b0', '#0c5038'), 'kg_steel': _solid(STEEL, None, noise=steel_n), 'kg_visor': visor,
            'kg_glass': _solid(GLASS, None, noise=[(x, y, GLASS_LT) for x in range(0, 16, 3) for y in range(0, 16, 5)]),
            'kg_magenta': _gem(GEM, GEM_LT, GEM_DK), 'kg_pearl': _solid(PEARL, None, noise=pearl_n),
            'kg_rose': _solid(ROSE, None, noise=[(x, x, ROSE_LT) for x in range(16)]), 'kg_silver': _solid('#c8ccd8', None, noise=[(x, 15 - x, '#f4f6ff') for x in range(16)])}


# ---------------------------------------------------------------------------------------------------- the 3D pieces (boxes; front is north, -z)
def _box(fr, to, tex, uv_full=(), faces=None, rot=None):
    w = {'north': (to[0] - fr[0], to[1] - fr[1]), 'south': (to[0] - fr[0], to[1] - fr[1]), 'east': (to[2] - fr[2], to[1] - fr[1]),
         'west': (to[2] - fr[2], to[1] - fr[1]), 'up': (to[0] - fr[0], to[2] - fr[2]), 'down': (to[0] - fr[0], to[2] - fr[2])}
    out = {}
    for f in (faces or w):
        a, b = (round(min(16, max(0.25, v)), 3) for v in w[f])
        out[f] = {'uv': [0, 0, 16, 16] if f in uv_full else [0, 0, a, b], 'texture': '#' + tex}
    e = {'from': [round(v, 3) for v in fr], 'to': [round(v, 3) for v in to], 'faces': out}
    if rot: e['rotation'] = rot
    return e


ALL = ('north', 'south', 'east', 'west', 'up', 'down')


def crown_model():
    E = []
    y0, y1 = 12.4, 14.6                                                            # the band, round the brow
    E += [_box((2.6, y0, 2.6), (13.4, y1, 3.4), 'kg_gold'), _box((2.6, y0, 12.6), (13.4, y1, 13.4), 'kg_gold'),
          _box((2.6, y0, 3.4), (3.4, y1, 12.6), 'kg_gold'), _box((12.6, y0, 3.4), (13.4, y1, 12.6), 'kg_gold')]
    E.append(_box((6.9, 12.7, 2.2), (9.1, 14.3, 2.6), 'kg_green', uv_full=ALL))     # the green cabochon at the front
    for x in (4.2, 11.0):
        E.append(_box((x, 12.9, 2.3), (x + 0.8, 13.9, 2.6), 'kg_seagem', uv_full=ALL))
    # four arches rising from the band's middles to the top, sea-blue gems set in each
    for (x0, x1, z0, z1, axis) in ((7.3, 8.7, 2.6, 3.4, 'n'), (7.3, 8.7, 12.6, 13.4, 's'), (2.6, 3.4, 7.3, 8.7, 'w'), (12.6, 13.4, 7.3, 8.7, 'e')):
        for i, (h, inset) in enumerate(((1.6, 0.0), (1.4, 1.2), (1.0, 2.6), (0.8, 3.8))):
            dx = inset if axis == 'w' else -inset if axis == 'e' else 0
            dz = inset if axis == 'n' else -inset if axis == 's' else 0
            yb = y1 + sum(hh for hh, _ in ((1.6, 0.0), (1.4, 1.2), (1.0, 2.6), (0.8, 3.8))[:i])
            E.append(_box((x0 + dx, yb, z0 + dz), (x1 + dx, yb + h, z1 + dz), 'kg_gold'))
        # a sea-blue gem in the arch's opening
        gx0, gx1 = (x0 - 1.2, x1 + 1.2) if axis in 'ns' else (x0, x1)
        gz0, gz1 = (z0, z1) if axis in 'ns' else (z0 - 1.2, z1 + 1.2)
        E.append(_box((gx0 + 0.3 if axis in 'ns' else gx0 + (0.2 if axis == 'w' else -0.2), y1 + 0.2, gz0 + (0.2 if axis == 'n' else -0.2 if axis == 's' else 0.3)),
                      (gx1 - 0.3 if axis in 'ns' else gx1 + (0.2 if axis == 'w' else -0.2), y1 + 1.5, gz1 + (0.2 if axis == 'n' else -0.2 if axis == 's' else -0.3)),
                      'kg_seagem', uv_full=ALL))
    E.append(_box((6.6, 19.2, 6.6), (9.4, 19.8, 9.4), 'kg_gold'))                   # the boss where they meet
    E.append(_box((7.0, 19.8, 7.6), (9.0, 22.6, 8.4), 'kg_violet', uv_full=ALL,     # the violet diamond, stood on its point
                  rot={'angle': 45, 'axis': 'z', 'origin': [8, 21.2, 8]}))
    return E


def tidewarden_helm_model():
    E = [_box((2.5, 2.2, 2.5), (13.5, 13.6, 13.5), 'kg_steel'),
         _box((2.4, 2.4, 2.3), (13.6, 12.6, 2.5), 'kg_visor', uv_full=('north',), faces=('north',)),
         _box((2.0, 2.0, 3.0), (3.6, 9.0, 10.0), 'kg_steel'), _box((12.4, 2.0, 3.0), (14.0, 9.0, 10.0), 'kg_steel'),     # cheek guards
         _box((3.2, 13.6, 3.2), (12.8, 14.6, 12.8), 'kg_steel'),
         _box((2.2, 2.0, 11.0), (13.8, 4.4, 14.0), 'kg_steel')]                                                       # the nape
    for i, (z, h) in enumerate(((3.0, 1.6), (5.0, 2.6), (7.0, 3.2), (9.0, 3.0), (11.0, 2.2), (12.6, 1.2))):          # the fin crest, sea-glass
        E.append(_box((7.4, 14.6, z), (8.6, 14.6 + h, z + 2.0), 'kg_glass'))
    E.append(_box((7.1, 11.0, 2.0), (8.9, 12.8, 2.4), 'kg_magenta', uv_full=ALL))                                    # the gem on the brow
    E += [_box((7.6, 9.4, 2.2), (8.4, 11.0, 2.4), 'kg_glass'), _box((6.4, 10.2, 2.2), (7.1, 12.4, 2.4), 'kg_glass'),
          _box((8.9, 10.2, 2.2), (9.6, 12.4, 2.4), 'kg_glass')]                                                       # the teardrop round it
    return E


def pearlguard_tiara_model():
    E = [_box((2.8, 12.0, 2.8), (13.2, 12.8, 3.4), 'kg_silver'), _box((2.8, 12.0, 12.6), (13.2, 12.8, 13.2), 'kg_silver'),
         _box((2.8, 12.0, 3.4), (3.4, 12.8, 12.6), 'kg_silver'), _box((12.6, 12.0, 3.4), (13.2, 12.8, 12.6), 'kg_silver')]
    for x in (3.6, 5.2, 10.0, 11.6):                                                                                  # pearls along the front
        E.append(_box((x, 12.8, 2.7), (x + 0.9, 13.7, 3.5), 'kg_pearl'))
    for (fr, to) in (((6.2, 13.0, 2.4), (9.8, 14.4, 2.9)), ((7.3, 12.0, 2.4), (8.7, 15.6, 2.9)),                       # the flower, four petals
                     ((6.6, 12.4, 2.5), (9.4, 15.2, 2.9))):
        E.append(_box(fr, to, 'kg_rose'))
    E.append(_box((7.4, 13.1, 2.1), (8.6, 14.3, 2.4), 'kg_magenta', uv_full=ALL))
    for z in (5.0, 8.0, 11.0):
        E += [_box((2.6, 12.8, z), (3.3, 13.5, z + 0.8), 'kg_pearl'), _box((12.7, 12.8, z), (13.4, 13.5, z + 0.8), 'kg_pearl')]
    return E


def head_json(els, gui_y=-3.5):
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    return {'textures': dict({t: f'bm:block/{t}' for t in used}, particle=f'bm:block/{used[0]}'), 'elements': els,
            'display': {'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.28, 1.28, 1.28]},
                        'gui': {'rotation': [25, 200, 0], 'translation': [0, gui_y, 0], 'scale': [0.62, 0.62, 0.62]},
                        'ground': {'rotation': [0, 0, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]},
                        'fixed': {'rotation': [0, 180, 0], 'translation': [0, -3, 0], 'scale': [0.62, 0.62, 0.62]},
                        'thirdperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]},
                        'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]}}}


# ---------------------------------------------------------------------------------------------------- the plate (armour layers)
def _recolor(im, lo, hi):
    px = im.load(); lo, hi = hexc(lo)[:3], hexc(hi)[:3]
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if not a: continue
            t = min(1.0, (r + g + b) / 765 * 1.35)
            px[x, y] = tuple(int(lo[c] + (hi[c] - lo[c]) * t) for c in range(3)) + (a,)
    return im


def _edge(im, col):
    """trim: every opaque pixel bordering transparency (the plate's outline) takes the trim colour"""
    px = im.load(); src = im.copy().load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if not src[x, y][3]: continue
            if any(not (0 <= x + dx < w and 0 <= y + dy < h) or not src[x + dx, y + dy][3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = hexc(col)
    return im


def layer(van, kind, which):
    base = 'diamond' if which == 'tidewarden' else 'iron'
    im = Image.open(f'{van}/entity/equipment/{kind}/{base}.png').convert('RGBA')
    if which == 'tidewarden':
        im = _edge(_recolor(im, STEEL_DK, STEEL_LT), GLASS)
        if kind == 'humanoid':
            ins = insignia_sprite(8)                                    # the insignia on the breast (the body's front: x 20..27, y 20..31)
            im.alpha_composite(ins, (20, 21))
            px = im.load()
            for x in range(20, 28):
                if px[x, 31][3]: px[x, 31] = hexc(GLASS_DK)
    else:
        im = _edge(_recolor(im, PEARL_DK, PEARL_LT), ROSE)
        if kind == 'humanoid':
            px = im.load()
            for (x, y, c) in ((23, 22, ROSE), (24, 22, ROSE), (22, 23, ROSE), (25, 23, ROSE), (23, 23, GEM), (24, 23, GEM), (23, 24, ROSE), (24, 24, ROSE)):
                if px[x, y][3]: px[x, y] = hexc(c)
    return im


# ---------------------------------------------------------------------------------------------------- inventory icons for the plate, the scales
def _plate_icon(kind, which):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    b, lt, dk, tr = ((STEEL, STEEL_LT, STEEL_DK, GLASS) if which == 'tidewarden' else (PEARL, PEARL_LT, PEARL_DK, ROSE))
    if kind == 'chest':
        d.polygon([(2, 2), (5, 1), (10, 1), (13, 2), (14, 6), (12, 7), (12, 14), (3, 14), (3, 7), (1, 6)], fill=hexc(b), outline=hexc(dk))
        d.line((5, 1, 7, 4), fill=hexc(tr)); d.line((10, 1, 8, 4), fill=hexc(tr)); d.line((4, 13, 11, 13), fill=hexc(tr))
        d.rectangle((7, 6, 8, 8), fill=hexc(GEM if which == 'tidewarden' else ROSE)); d.point((4, 4), fill=hexc(lt))
    elif kind == 'legs':
        d.polygon([(3, 1), (12, 1), (13, 15), (9, 15), (8, 6), (7, 6), (6, 15), (2, 15)], fill=hexc(b), outline=hexc(dk))
        d.line((3, 2, 12, 2), fill=hexc(tr)); d.point((4, 4), fill=hexc(lt)); d.point((11, 4), fill=hexc(lt))
    else:
        d.polygon([(2, 5), (6, 5), (6, 11), (8, 13), (8, 15), (1, 15), (1, 12)], fill=hexc(b), outline=hexc(dk))
        d.polygon([(9, 5), (13, 5), (14, 12), (15, 15), (8, 15), (8, 13), (9, 11)], fill=hexc(b), outline=hexc(dk))
        d.line((2, 6, 5, 6), fill=hexc(tr)); d.line((10, 6, 13, 6), fill=hexc(tr))
    return im


def icons():
    out = {f'{w}_{k}': _plate_icon(k, w) for w in ('tidewarden', 'pearlguard') for k in ('chest', 'legs', 'boots')}
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)         # the Tide Scale: a sea-glass scale with a shine
    d.polygon([(8, 1), (14, 6), (12, 13), (8, 15), (4, 13), (2, 6)], fill=hexc(GLASS), outline=hexc(GLASS_DK))
    d.line((8, 3, 8, 13), fill=hexc(GLASS_DK)); d.line((5, 6, 6, 11), fill=hexc(GLASS_LT)); d.point((6, 4), fill=hexc('#ffffff'))
    out['tide_scale'] = im
    return out


def rp(R, van):
    import json
    def post(R2):
        tex = piece_textures()
        for k, im in tex.items(): im.save(R2.p('assets', 'bm', 'textures', 'block', f'{k}.png'))
        for name, els, gy in (('crown_of_the_deep', crown_model(), -5.0), ('tidewarden_helm', tidewarden_helm_model(), -3.5),
                              ('pearlguard_tiara', pearlguard_tiara_model(), -4.5)):
            R2.wj(f'assets/bm/models/item/{name}.json', head_json(els, gy))
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        # the sprites from the owner's art: handheld, extruded
        aegis, cres, ins = aegis_sprite(), crescent_sprite(), insignia_sprite(64)
        for name, im in (('leo_aegis', aegis), ('emma_crescent', cres), ('kingdom_insignia', ins)):
            im.save(R2.p('assets', 'bm', 'textures', 'item', f'{name}.png'))
        R2.wj('assets/bm/models/item/emma_crescent.json', {'parent': 'minecraft:item/handheld', 'textures': {'layer0': 'bm:item/emma_crescent'},
                                                           'display': {'thirdperson_righthand': {'rotation': [0, -90, 55], 'translation': [0, 6, 0.5], 'scale': [1.25, 1.25, 0.85]},
                                                                       'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 4.2, 1.13], 'scale': [0.95, 0.95, 0.68]}}})
        R2.wj('assets/bm/items/emma_crescent.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/emma_crescent'}})
        shield = {'thirdperson_righthand': {'rotation': [0, 90, 0], 'translation': [0, 0, -2], 'scale': [1.0, 1.0, 1.0]},
                  'thirdperson_lefthand': {'rotation': [0, 90, 0], 'translation': [0, 0, -2], 'scale': [1.0, 1.0, 1.0]},
                  'firstperson_righthand': {'rotation': [0, 180, 5], 'translation': [-2, 1, -4], 'scale': [0.8, 0.8, 0.8]},
                  'firstperson_lefthand': {'rotation': [0, 180, 5], 'translation': [8, 1, -4], 'scale': [0.8, 0.8, 0.8]},
                  'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
                  'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}
        block = {'thirdperson_righthand': {'rotation': [45, 135, 0], 'translation': [3.5, 2, -1], 'scale': [1.0, 1.0, 1.0]},
                 'thirdperson_lefthand': {'rotation': [45, 135, 0], 'translation': [3.5, 2, -1], 'scale': [1.0, 1.0, 1.0]},
                 'firstperson_righthand': {'rotation': [0, 180, -5], 'translation': [-7, 1.5, -2], 'scale': [0.8, 0.8, 0.8]},
                 'firstperson_lefthand': {'rotation': [0, 180, -5], 'translation': [3, 1.5, -2], 'scale': [0.8, 0.8, 0.8]}}
        R2.wj('assets/bm/models/item/leo_aegis.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'bm:item/leo_aegis'}, 'display': shield})
        R2.wj('assets/bm/models/item/leo_aegis_blocking.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'bm:item/leo_aegis'}, 'display': dict(shield, **block)})
        R2.wj('assets/bm/items/leo_aegis.json', {'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item',
                                                           'on_true': {'type': 'minecraft:model', 'model': 'bm:item/leo_aegis_blocking'},
                                                           'on_false': {'type': 'minecraft:model', 'model': 'bm:item/leo_aegis'}}})
        # the insignia plaque: a flat panel for the castle's walls (an item_display), the insignia on both faces
        R2.wj('assets/bm/models/item/kingdom_insignia.json', {'parent': 'minecraft:item/generated', 'textures': {'layer0': 'bm:item/kingdom_insignia'}})
        R2.wj('assets/bm/items/kingdom_insignia.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/kingdom_insignia'}})
        # the plate
        for which in ('tidewarden', 'pearlguard'):
            for kind in ('humanoid', 'humanoid_leggings'):
                layer(van, kind, which).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', kind, f'{which}.png'))
            R2.wj(f'assets/bm/equipment/{which}.json', {'layers': {'humanoid': [{'texture': f'bm:{which}'}], 'humanoid_leggings': [{'texture': f'bm:{which}'}]}})
    R.POST.append(post)
    R.ICONS.update(icons())


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
    sheet = Image.new('RGBA', (64 * 3 + 16 * 8, 64), (40, 50, 70, 255))
    for i, im in enumerate((aegis_sprite(), crescent_sprite(), insignia_sprite())): sheet.alpha_composite(im, (64 * i, 0))
    for i, (k, im) in enumerate(icons().items()): sheet.alpha_composite(im, (192 + 16 * (i % 8), 16 * (i // 8)))
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save(os.path.join(out, 'kingdom_art.png'))
    print('wrote', os.path.join(out, 'kingdom_art.png'))
