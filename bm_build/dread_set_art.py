"""2.93: the art of the DREADBORNE set (the Dread bosses' armour) and its holy twin, the SERAPH'S RAIMENT.

DREADBORNE   the Visage is the Dread monsters' own 3D helm (dread_armor.py); the Carapace, Greaves and Treads wear their
             cracked void-plate (bm:dread); the Carapace carries wings of black membrane veined in red, with eyes in them.
SERAPH       "Each had six wings: with two they covered their faces, with two they covered their feet, and with two they were
             flying" (Isaiah 6:2). The Seraph's Gaze is a pearl-and-gold helm whose face is hidden behind two crossed wings,
             their feathers full of eyes, under a burning halo; the Seraph's Wings fly (the elytra layer: three tiers of pearl
             feathers, eyes in them, their edges on fire); the Treads' feathers cover the feet; the plate is pearl and gold
             with eyes open across it.
Sprites for all eight pieces. Helm model space as the Dread Visage's: a head filling 3..13, front north (-z)."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
import dread_armor as DA

VAN = '/home/claude/mc263/client/assets/minecraft/textures'
WINGS_SRC = '/home/claude/bm_build/vendor/elytra_wings.png'
PEARL, PEARL_D, PEARL_L = (236, 232, 248), (176, 168, 206), (255, 255, 255)
GOLD, GOLD_D, GOLD_L = (232, 182, 48), (150, 100, 20), (255, 228, 120)
FLAME, FLAME_Y = (255, 120, 24), (255, 214, 72)
SAPH, IRIS = (40, 90, 220), (64, 150, 255)
RED, RED_L, VOID, VOID_L = (208, 24, 46), (255, 90, 100), (22, 16, 26), (48, 34, 54)


# ---------------------------------------------------------------------------------------------------- the sprites
def _sprite(base, recolor, marks):
    im = Image.open(f'{VAN}/item/{base}.png').convert('RGBA')
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a: px[x, y] = recolor((r + g + b) / 765) + (a,)
    d = ImageDraw.Draw(im)
    for xy, c in marks: d.point(xy, fill=c + (255,))
    return im


def _ramp(stops):
    def f(t):
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1:
                k = (t - t0) / max(1e-6, t1 - t0)
                return tuple(round(c0[i] + (c1[i] - c0[i]) * k) for i in range(3))
        return stops[-1][1]
    return f


DREAD_RAMP = _ramp([(0.0, (6, 4, 8)), (0.35, VOID), (0.6, VOID_L), (0.85, (110, 40, 60)), (1.0, RED_L)])
HOLY_RAMP = _ramp([(0.0, (40, 30, 90)), (0.3, PEARL_D), (0.6, PEARL), (0.85, GOLD_L), (1.0, PEARL_L)])


DA_BONE = (216, 204, 176, 255)


def plate_icon(kind, holy=False):
    base = {'chest': 'netherite_chestplate', 'legs': 'netherite_leggings', 'feet': 'netherite_boots'}[kind]
    marks = []
    if kind == 'chest':
        marks = [((7, 4), IRIS if holy else RED_L), ((8, 4), IRIS if holy else RED_L), ((7, 6), GOLD if holy else DA_BONE[:3]), ((8, 6), GOLD if holy else DA_BONE[:3])]
    elif kind == 'legs':
        marks = [((5, 7), GOLD if holy else DA_BONE[:3]), ((10, 7), GOLD if holy else DA_BONE[:3]), ((5, 3), IRIS if holy else RED)]
    else:
        marks = [((3, 13), DA_BONE[:3]), ((12, 13), DA_BONE[:3])] if not holy else [((1, 9), PEARL_L), ((14, 9), PEARL_L), ((0, 8), PEARL), ((15, 8), PEARL)]
    im = _sprite(base, HOLY_RAMP if holy else DREAD_RAMP, marks)
    if kind == 'chest':                                     # (the Carapace and the Wings fly: a wing behind each shoulder)
        d = ImageDraw.Draw(im)
        c, e = ((PEARL_L, GOLD) if holy else ((70, 20, 34), RED))
        for s in (-1, 1):
            x0 = 1 if s < 0 else 14
            d.line((x0, 1, x0, 7), fill=c + (255,)); d.point((x0, 8), fill=e + (255,)); d.point((x0 - s, 0), fill=c + (255,))
    return im


def heart_icon():
    """the Dread Heart: a black heart veined in red, an eye open in it"""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(8, 15), (1, 7), (1, 4), (3, 2), (6, 2), (8, 4), (10, 2), (13, 2), (15, 4), (15, 7)], fill=VOID + (255,), outline=(70, 10, 20, 255))
    d.line((4, 5, 6, 9), fill=RED + (255,)); d.line((12, 5, 10, 10), fill=RED + (255,)); d.line((8, 11, 8, 13), fill=RED + (255,))
    d.ellipse((5, 5, 11, 9), fill=(240, 236, 230, 255)); d.ellipse((7, 6, 9, 8), fill=RED + (255,)); d.point((8, 7), fill=(10, 0, 0, 255))
    d.point((3, 4), fill=VOID_L + (255,))
    return im


def icons():
    out = {'dread_heart': heart_icon()}                     # (the helms are their own 3D models, in the hand as on the head)
    for k, iid in (('chest', 'carapace'), ('legs', 'greaves'), ('feet', 'treads')):
        out[f'dread_{iid}'] = plate_icon(k)
        out[f'seraph_{iid}'] = plate_icon(k, True)
    return out


# ---------------------------------------------------------------------------------------------------- the wings (an elytra layer)
def _eye(px, w, h, cx, cy, iris):
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)):
        x, y = cx + dx, cy + dy
        if 0 <= x < w and 0 <= y < h and px[x, y][3]: px[x, y] = (250, 250, 250, 255)
    if 0 <= cx < w and 0 <= cy < h: px[cx, cy] = iris + (255,)


def wings(holy):
    im = Image.open(WINGS_SRC).convert('RGBA'); px = im.load(); w, h = im.size
    rnd = random.Random(7 if holy else 3)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if not a: continue
            t = (r + g + b) / 765
            if holy:                                         # three tiers of pearl feathers, gold at their roots, fire at their edges
                tier = (y * 3) // h
                c = HOLY_RAMP(min(1.0, 0.35 + t * 0.7 - tier * 0.05))
                if (x + tier * 2) % 4 == 0: c = tuple(max(0, v - 26) for v in c)
                px[x, y] = c + (a,)
            else:                                            # black membrane, red veins
                px[x, y] = DREAD_RAMP(t * 0.55) + (a,)
    if holy:
        for x in range(w):                                   # the fiery trailing edge
            for y in range(h - 1, -1, -1):
                if px[x, y][3]:
                    px[x, y] = (FLAME if x % 3 else FLAME_Y) + (255,)
                    if y > 0 and px[x, y - 1][3] and x % 2: px[x, y - 1] = FLAME_Y + (255,)
                    break
    else:
        for _ in range(14):                                  # veins of red light, branching as they spread
            x, y = rnd.randrange(w), rnd.randrange(h)
            for _s in range(rnd.randint(4, 9)):
                if 0 <= x < w and 0 <= y < h and px[x, y][3]: px[x, y] = (RED if rnd.random() < 0.75 else RED_L) + (255,)
                x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1, 1))
    for _ in range(10 if holy else 6):                       # eyes in the wings
        for _try in range(40):
            x, y = rnd.randrange(2, w - 2), rnd.randrange(2, h - 2)
            if all(px[x + dx, y + dy][3] for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                _eye(px, w, h, x, y, IRIS if holy else RED); break
    return im


# ---------------------------------------------------------------------------------------------------- the seraph's plate
def seraph_layer(kind):
    """the angelic plate (netherite turned pearl and gold), eyes open across it; the boots feathered over the feet"""
    im = Image.open(f'{VAN}/entity/equipment/{kind}/netherite.png').convert('RGBA'); px = im.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a: px[x, y] = HOLY_RAMP((r + g + b) / 765 * 0.9 + 0.1) + (a,)
    rnd = random.Random(11 if kind == 'humanoid' else 12)
    for _ in range(9 if kind == 'humanoid' else 5):
        for _try in range(40):
            x, y = rnd.randrange(1, w - 1), rnd.randrange(1, h - 1)
            if all(px[x + dx, y + dy][3] for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                _eye(px, w, h, x, y, IRIS); break
    if kind == 'humanoid':
        for y in range(20, 32):                              # a gold seam down the breast
            if px[20 + 3, y][3]: px[23, y] = GOLD + (255,); px[24, y] = GOLD_L + (255,)
        for x in range(0, 16):                               # feathers over the feet (the boots' bottom rows), tipped with gold
            for y in (29, 30, 31):
                if px[x, y][3]: px[x, y] = (PEARL_L if (x + y) % 2 else PEARL) + (255,)
            if px[x, 31][3] and x % 3 == 0: px[x, 31] = GOLD + (255,)
    return im


# ---------------------------------------------------------------------------------------------------- the Seraph's Gaze (3D)
TILES = ['pearl', 'pearl_d', 'gold', 'gold_l', 'feather', 'feather_eye', 'flame', 'flame_y', 'saph']


def seraph_textures():
    out = {}
    def tile(fill, f=None):
        im = Image.new('RGBA', (16, 16), fill + (255,)); px = im.load()
        rnd = random.Random(sum(fill))
        for y in range(16):
            for x in range(16):
                k = rnd.uniform(-0.05, 0.05) + (0.12 if y < 2 else 0) - (0.14 if y > 13 else 0)
                px[x, y] = tuple(max(0, min(255, round(v * (1 + k)))) for v in fill) + (255,)
        if f: f(im, px)
        return im
    out['seraph_pearl'] = tile(PEARL)
    out['seraph_pearl_d'] = tile(PEARL_D)
    out['seraph_gold'] = tile(GOLD)
    out['seraph_gold_l'] = tile(GOLD_L)
    def feather(im, px, eye=False):
        d = ImageDraw.Draw(im)
        d.line((8, 0, 8, 15), fill=GOLD_D + (255,))                         # the quill
        for y in range(0, 16, 3):
            d.line((1, y + 2, 8, y), fill=PEARL_D + (255,)); d.line((15, y + 2, 8, y), fill=PEARL_D + (255,))
        if eye:
            d.ellipse((4, 5, 11, 10), fill=(250, 250, 250, 255), outline=GOLD_D + (255,))
            d.ellipse((6, 6, 9, 9), fill=IRIS + (255,)); d.point((7, 7), fill=(10, 10, 30, 255))
    out['seraph_feather'] = tile(PEARL_L, lambda im, px: feather(im, px))
    out['seraph_feather_eye'] = tile(PEARL_L, lambda im, px: feather(im, px, True))
    out['seraph_flame'] = tile(FLAME, lambda im, px: [px.__setitem__((x, y), FLAME_Y + (255,)) for x in range(16) for y in range(16) if (x * 7 + y * 3) % 5 == 0])
    out['seraph_flame_y'] = tile(FLAME_Y)
    out['seraph_saph'] = tile(SAPH)
    return out


def _b(fr, to, tex, rot=None):
    e = DA._box(fr, to, tex)
    if rot:
        axis, ang, o = rot
        e['rotation'] = {'origin': list(o), 'axis': axis, 'angle': ang}
    return e


def seraph_helm_model():
    E = []
    E.append(_b((2.6, 2.6, 2.8), (13.4, 13.4, 13.4), 'seraph_pearl'))              # the helm
    E.append(_b((2.4, 12.4, 2.6), (13.6, 13.6, 13.6), 'seraph_gold'))              # its gold rim and crest
    E.append(_b((7.2, 13.4, 3.2), (8.8, 15.2, 13.2), 'seraph_gold_l'))
    E.append(_b((2.4, 2.4, 2.6), (13.6, 3.4, 13.6), 'seraph_gold'))
    E.append(_b((6.8, 7.6, 2.3), (9.2, 9.6, 2.7), 'seraph_saph'))                  # a sapphire at the brow, above the wings
    # with two they covered their faces: two great wings from the temples, their feathers crossing over the whole face
    for s in (-1, 1):
        root = 8 + s * 6.6
        for k in range(5):
            y = 13.2 - k * 2.15
            L = 10.2 - k * 0.5
            x0, x1 = (root, root + L) if s < 0 else (root - L, root)
            z0 = 0.9 + (0.35 if (k + (s > 0)) % 2 else 0.0)                 # (the two wings' feathers overlap, left over right)
            E.append(_b((x0, y - 2.3, z0), (x1, y, z0 + 0.9), 'seraph_feather_eye' if (k + (s > 0)) % 2 == 0 else 'seraph_feather',
                        rot=('z', 22.5 * s * -1, (root, y - 1.1, z0 + 0.45))))
        E.append(_b((root - 1.0, 2.8, 0.8), (root + 1.0, 14.0, 4.0), 'seraph_gold'))                     # the wings' roots at the temples
        E.append(_b((root - 0.6, 13.6, 1.4), (root + 0.6, 15.4, 3.2), 'seraph_gold_l'))
    # a burning halo, close over the head
    R, n = 6.0, 16
    for i in range(n):
        a = 2 * math.pi * i / n
        x, z = 8 + R * math.cos(a), 8 + R * math.sin(a)
        E.append(_b((x - 0.75, 15.8, z - 0.75), (x + 0.75, 16.5, z + 0.75), 'seraph_gold_l'))
        E.append(_b((x - 0.35, 16.5, z - 0.35), (x + 0.35, 17.9 if i % 2 else 17.2, z + 0.35), 'seraph_flame_y' if i % 2 else 'seraph_flame'))
    # eyes all about it (on its sides and back)
    for (x, y, z) in ((2.3, 9.6, 6.0), (2.3, 6.4, 10.2), (12.8, 9.0, 8.0), (12.8, 5.8, 4.6), (6.0, 7.0, 13.2), (10.0, 9.4, 13.2)):
        s_ = 0.8
        if x < 4 or x > 12:
            E.append(_b((x - 0.25, y - s_, z - s_), (x + 0.65, y + s_, z + s_), 'seraph_feather_eye'))
        else:
            E.append(_b((x - s_, y - s_, z - 0.25), (x + s_, y + s_, z + 0.65), 'seraph_feather_eye'))
    return E


def seraph_helm_json():
    els = seraph_helm_model()
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    disp = DA.helm_json()[1]['display']
    return {'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/seraph_pearl'), 'elements': els, 'display': disp}


def rp(R):
    def post(R2):
        for k, im in seraph_textures().items(): im.save(R2.p('assets', 'bm', 'textures', 'block', f'{k}.png'))
        R2.wj('assets/bm/models/item/seraph_helm.json', seraph_helm_json())
        R2.wj('assets/bm/items/angel_dread_visage.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/seraph_helm'}})
        for holy in (False, True):
            nm = 'seraph' if holy else 'dread'
            wings(holy).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', f'{nm}_wings.png'))
        for kind in ('humanoid', 'humanoid_leggings'):
            seraph_layer(kind).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', kind, 'seraph.png'))
        R2.wj('assets/bm/equipment/dread_carapace.json', {'layers': {'humanoid': [{'texture': 'bm:dread'}], 'wings': [{'texture': 'bm:dread_wings'}]}})
        R2.wj('assets/bm/equipment/seraph.json', {'layers': {'humanoid': [{'texture': 'bm:seraph'}], 'humanoid_leggings': [{'texture': 'bm:seraph'}]}})
        R2.wj('assets/bm/equipment/seraph_wings.json', {'layers': {'humanoid': [{'texture': 'bm:seraph'}], 'wings': [{'texture': 'bm:seraph_wings'}]}})
        for iid in ('carapace', 'greaves', 'treads'):          # (the holy pieces' sprites, as the forge names their models)
            R2.wj(f'assets/bm/items/angel_dread_{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/seraph_{iid}'}})
    R.POST.append(post)
    R.ICONS.update(icons())
    R.LANG.update({'death.attack.bm.dread_rend': '%1$s was rent apart by the Dread', 'death.attack.bm.dread_rend.player': '%1$s was rent apart by %2$s\'s Dread',
                   'death.attack.bm.dread_proc': '%1$s fell to the Dread', 'death.attack.bm.dread_proc.player': '%1$s fell to %2$s\'s Dread',
                   'death.attack.bm.dread_hex': '%1$s was hexed to death', 'death.attack.bm.dread_hex.player': '%1$s was hexed to death by %2$s',
                   'death.attack.bm.seraph_fire': '%1$s was judged by holy fire', 'death.attack.bm.seraph_fire.player': '%1$s was judged by %2$s\'s holy fire'})
