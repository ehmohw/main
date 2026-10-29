"""2.93: the art of the DREADBORNE set (the Dread bosses' armour) and its holy twin, the SERAPH'S RAIMENT.

DREADBORNE   the Visage is the Dread monsters' own 3D helm (dread_armor.py); the Carapace, Greaves and Treads wear their
             cracked void-plate (bm:dread); the Carapace carries wings of black membrane veined in red, with eyes in them.
SERAPH       (2.99: redrawn in seraph_art.py - the worn layers, the elytra layer, the Seraph's Gaze, the sprites - with the 3D
             great and lower wings others see on a wearer of the Seraph's Wings in seraph_wings.py; this module registers them.)
Sprites for all eight pieces. Helm model space as the Dread Visage's: a head filling 3..13, front north (-z)."""
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
import dread_armor as DA
import seraph_art as SA
import seraph_wings as SW
import dread_wings as DW
import dread_art as DK

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
    out.update(DK.icons())                                  # (2.99: the Dread's sprites, drawn on vanilla's silhouettes - dread_art)
    out.update(SA.icons())                                  # (2.99: the Seraph's sprites, drawn for themselves - seraph_art)
    return out


# ---------------------------------------------------------------------------------------------------- the wings (an elytra layer)
def _eye(px, w, h, cx, cy, iris):
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, -1), (0, 1)):
        x, y = cx + dx, cy + dy
        if 0 <= x < w and 0 <= y < h and px[x, y][3]: px[x, y] = (250, 250, 250, 255)
    if 0 <= cx < w and 0 <= cy < h: px[cx, cy] = iris + (255,)


def wings(holy=False):
    """the Dread Carapace's elytra layer: black membrane veined in red, eyes in it (the Seraph's is seraph_art.wings_layer)"""
    assert not holy
    im = Image.open(WINGS_SRC).convert('RGBA'); px = im.load(); w, h = im.size
    rnd = random.Random(3)
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a: px[x, y] = DREAD_RAMP((r + g + b) / 765 * 0.55) + (a,)
    for _ in range(14):                                      # veins of red light, branching as they spread
        x, y = rnd.randrange(w), rnd.randrange(h)
        for _s in range(rnd.randint(4, 9)):
            if 0 <= x < w and 0 <= y < h and px[x, y][3]: px[x, y] = (RED if rnd.random() < 0.75 else RED_L) + (255,)
            x += rnd.choice((-1, 0, 1)); y += rnd.choice((0, 1, 1))
    for _ in range(6):                                       # eyes in the wings
        for _try in range(40):
            x, y = rnd.randrange(2, w - 2), rnd.randrange(2, h - 2)
            if all(px[x + dx, y + dy][3] for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                _eye(px, w, h, x, y, RED); break
    return im


def rp(R):
    def post(R2):
        R2.wj('assets/bm/models/item/seraph_helm.json', SA.helm_json(DA.helm_json()[1]['display']))     # (2.99: seraph_art)
        R2.wj('assets/bm/items/angel_dread_visage.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/seraph_helm'}})
        DK.wings_layer().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'dread_wings.png'))   # (2.99: cut back to a mantle - dread_art)
        SA.wings_layer().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'wings', 'seraph_wings.png'))
        SA.humanoid().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid', 'seraph.png'))
        SA.leggings().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid_leggings', 'seraph.png'))
        R2.wj('assets/bm/equipment/dread_carapace.json', {'layers': {'humanoid': [{'texture': 'bm:dread'}], 'wings': [{'texture': 'bm:dread_wings'}]}})
        R2.wj('assets/bm/equipment/seraph.json', {'layers': {'humanoid': [{'texture': 'bm:seraph'}], 'humanoid_leggings': [{'texture': 'bm:seraph'}]}})
        R2.wj('assets/bm/equipment/seraph_wings.json', {'layers': {'humanoid': [{'texture': 'bm:seraph'}], 'wings': [{'texture': 'bm:seraph_wings'}]}})
        for iid in ('carapace', 'greaves', 'treads'):          # (the holy pieces' sprites, as the forge names their models)
            R2.wj(f'assets/bm/items/angel_dread_{iid}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/seraph_{iid}'}})
    R.POST.append(post)
    R.TEXTURE_MODS.append(SA)                              # (2.99: the Seraph's block textures - the helm's, the 3D wings')
    SW.rp(R)                                               # (2.99: the 3D wings' models and quills)
    DW.rp(R)                                               # (2.99: the Dread Carapace's 3D wings)
    R.ICONS.update(icons())
    R.LANG.update({'death.attack.bm.dread_rend': '%1$s was rent apart by the Dread', 'death.attack.bm.dread_rend.player': '%1$s was rent apart by %2$s\'s Dread',
                   'death.attack.bm.dread_proc': '%1$s fell to the Dread', 'death.attack.bm.dread_proc.player': '%1$s fell to %2$s\'s Dread',
                   'death.attack.bm.dread_hex': '%1$s was hexed to death', 'death.attack.bm.dread_hex.player': '%1$s was hexed to death by %2$s',
                   'death.attack.bm.seraph_fire': '%1$s was judged by holy fire', 'death.attack.bm.seraph_fire.player': '%1$s was judged by %2$s\'s holy fire'})
