"""2.93: the art of the DREADBORNE set (the Dread bosses' armour) and its holy twin, the SERAPH'S RAIMENT.

DREADBORNE   the Visage is the Dread monsters' own 3D helm (dread_armor.py); the Carapace, Greaves and Treads wear their
             cracked void-plate (bm:dread). (2.99: all redrawn in dread_art.py - the plate, the Visage, the elytra layer, the
             sprites - with the Carapace's 3D membrane wings and ragged tail in dread_wings.py; registered here and in dread_armor.)
SERAPH       (2.99: redrawn in seraph_art.py - the worn layers, the elytra layer, the Seraph's Gaze, the sprites - with the 3D
             great and lower wings others see on a wearer of the Seraph's Wings in seraph_wings.py; this module registers them.)
Sprites for all eight pieces. Helm model space as the Dread Visage's: a head filling 3..13, front north (-z)."""
from PIL import Image, ImageDraw

import dread_armor as DA
import seraph_art as SA
import seraph_wings as SW
import dread_wings as DW
import dread_art as DK

RED, VOID, VOID_L = (208, 24, 46), (22, 16, 26), (48, 34, 54)


# ---------------------------------------------------------------------------------------------------- the sprites
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


def rp(R):
    def post(R2):
        R2.wj('assets/bm/models/item/seraph_helm.json', SA.helm_json(DA.HELM_DISPLAY))     # (2.99: seraph_art)
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
