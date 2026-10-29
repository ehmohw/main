"""v299a: THE HERO OF TIME's look (items.py, tier III of the armour line) - Link's own clothes, drawn the vanilla way.

Before this it was netherite with a gold wayfinder trim. Now (armor_kit.py: hand-placed pixels on the standard layers, 3-4
shades lit from the top left):
  CAP        a 3D cap on the head (the item's own model): the green crown over the brow, and its long point flopping
             down the back of the head in four blocky steps. (The layer's head is drawn as a flat cap too - only an old,
             un-synced copy that still carries the armour asset would show it.)
  TUNIC      the green tunic: a white undershirt at the neck, the brown baldric across the chest and back, the brown belt
             with its gold buckle; short green sleeves over a band of chainmail, white sleeves, brown leather gauntlets.
  LEGGINGS   the tunic's skirt to mid-thigh (green, a dark hem), pale leggings below.
  BOOTS      brown knee boots, the cuff folded over.
Icons: the cap, the tunic, the leggings and the boots at 16 x 16, in the pack's icon style (outlined; vanilla.process lights
them). The pieces keep their ids, enchantments, attributes, gold wayfinder trim and set power; only the look is new."""
from PIL import Image

import armor_kit as K

# ramps (dark -> light)
GREEN = ['#1d4a14', '#2c6b20', '#3e8c2c', '#5aab3c', '#86cc5e']
LEATHER = ['#3a2412', '#5a381c', '#7c4f28', '#9e6a38', '#c08a50']
CLOTH = ['#8c8470', '#c4bba2', '#e4dcc4', '#fbf6e6']
CHAIN = ['#4a5058', '#7a828c', '#aeb6c0']
GOLDR = ['#7a4c10', '#b07a18', '#e8b830', '#fff0a0']

PAL = {'d': GREEN[0], 'g': GREEN[1], 'G': GREEN[2], 'L': GREEN[3], 'H': GREEN[4],
       'b': LEATHER[0], 'n': LEATHER[1], 'B': LEATHER[2], 'l': LEATHER[3], 'm': LEATHER[4],
       'v': CLOTH[0], 'w': CLOTH[1], 'W': CLOTH[2], 'V': CLOTH[3],
       'c': CHAIN[0], 'C': CHAIN[1], 'X': CHAIN[2],
       'y': GOLDR[0], 'Y': GOLDR[2], 'Z': GOLDR[3]}


def humanoid():
    """the outer layer: the cap (flat, the fallback), the tunic (body and arms), the boots"""
    L = K.Layer(PAL)
    # ---- the head: a flat cap (only an un-synced copy wearing the asset shows it; the cap is a 3D model now)
    L.faces('head', top=['LLLLLLLL', 'LLLLLLLG', 'LLGGGGGG', 'LGGGGGGG', 'LGGGGGGG', 'GGGGGGGG', 'GGGGGGGg', 'GGGGGggg'])
    L.faces('head', **K.head_ring([
        'LLLLLLLL' + 'LLLLLLLL' + 'GGGGGGGG' + 'GGGGGGGG',
        'GGGGGGGG' + 'GGGGGGGG' + 'GGGGGGGG' + 'GGGGGGGG',
        'gggggggg' + 'dddddddd' + 'gggggggg' + 'GGGGGGGG',
        'ggggg...' + '........' + '...ggggg' + 'GGGGGGGG',
        'gg......' + '........' + '......gg' + 'gGGGGGGg',
        '........' + '........' + '........' + '.gGGGGg.',
        '........' + '........' + '........' + '..gGGg..',
        '........' + '........' + '........' + '...dd...']))
    # ---- the tunic
    L.faces('body', top=['LLLLLLBn', 'LGGGGGBn', 'GGGGGGBn', 'GGGGGGBn'], bottom=['gggggggg'] * 4)
    L.faces('body', **K.body_ring([
        # right  front       left   back
        'LLLG' + 'LGdVWdGG' + 'GGGB' + 'nBGGGGGG',
        'GGGg' + 'LGGdwdBn' + 'GGGg' + 'GnBGGGGg',
        'GGGg' + 'LGGGGBnG' + 'GGGg' + 'GGnBGGGg',
        'GGGg' + 'LGGGBnGg' + 'GGGg' + 'GGGnBGGg',
        'GGGg' + 'LGGBnGGg' + 'GGGg' + 'GGGGnBGg',
        'GGGg' + 'LGBnGGGg' + 'GGGg' + 'GGGGGnBg',
        'GGGg' + 'LBnGGGGg' + 'GGGg' + 'GGGGGGnB',
        'GGGg' + 'BnGGGGGg' + 'GGGg' + 'GGGGGGGn',
        'BBBB' + 'BBBZYBBB' + 'BBBB' + 'BBBBBBBB',
        'nnnn' + 'nnnYynnn' + 'nnnn' + 'nnnnnnnn',
        'GGGg' + 'LGGGGGGg' + 'GGGg' + 'GGGGGGGg',
        'gggd' + 'gggggggd' + 'gggd' + 'gggggggd']))
    L.faces('arm', top=['LLLL', 'LLLG', 'LGGG', 'GGGg'], bottom=['nnnn'] * 4)
    L.faces('arm', **K.ring([
        # outer  front  inner  back
        'LLLL' + 'LLLL' + 'GGGG' + 'GGGG',
        'GGGG' + 'GGGG' + 'GGGg' + 'GGGg',
        'GGGG' + 'GGGG' + 'GGGg' + 'GGGg',
        'dddd' + 'dddd' + 'dddd' + 'dddd',
        'XCXC' + 'XCXC' + 'CcCc' + 'CcCc',
        'CcCc' + 'CcCc' + 'cCcC' + 'cCcC',
        'VWWW' + 'VWWW' + 'WWWw' + 'WWWw',
        'WWWW' + 'WWWW' + 'WWWw' + 'WWWw',
        'wwww' + 'wwww' + 'wwww' + 'wwww',
        'mlll' + 'mlll' + 'llll' + 'llll',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'nnnn' + 'nnnn' + 'nnnn' + 'nnnn']))
    # ---- the boots: brown, to the knee, the cuff folded over
    L.faces('leg', top=['....'] * 4, bottom=['bbbb'] * 4)
    L.faces('leg', **K.ring([
        '....' + '....' + '....' + '....',
        '....' + '....' + '....' + '....',
        '....' + '....' + '....' + '....',
        '....' + '....' + '....' + '....',
        '....' + '....' + '....' + '....',
        '....' + '....' + '....' + '....',
        'mmmm' + 'mmmm' + 'mmml' + 'lllm',
        'llll' + 'llll' + 'lllB' + 'BBBl',
        'nnnn' + 'nnnn' + 'nnnn' + 'nnnn',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'BBBn' + 'lBBn' + 'BBBn' + 'BBBn',
        'bbbb' + 'bbbb' + 'bbbb' + 'bbbb']))
    return L.im


def leggings():
    """the inner layer: the tunic's skirt (the body's waist, the legs to mid-thigh), pale leggings below"""
    L = K.Layer(PAL)
    L.faces('body', top=['........'] * 4, bottom=['gggggggg'] * 4)
    L.faces('body', **K.body_ring(['....' + '........' + '....' + '........'] * 7 + [
        'BBBB' + 'BBBBBBBB' + 'BBBB' + 'BBBBBBBB',
        'nnnn' + 'nnnnnnnn' + 'nnnn' + 'nnnnnnnn',
        'GGGg' + 'LGGGGGGg' + 'GGGg' + 'GGGGGGGg',
        'GGGg' + 'LGGGGGGg' + 'GGGg' + 'GGGGGGGg',
        'gggd' + 'gggggggd' + 'gggd' + 'gggggggd']))
    L.faces('leg', top=['GGGG'] * 4, bottom=['wwww'] * 4)
    L.faces('leg', **K.ring([
        'LGGG' + 'LGGG' + 'GGGg' + 'GGGg',
        'GGGG' + 'GGGG' + 'GGGg' + 'GGGg',
        'gggg' + 'gggg' + 'gggg' + 'gggg',
        'dddd' + 'dddd' + 'dddd' + 'dddd',
        'wwww' + 'wwww' + 'wwww' + 'wwww',
        'VWWW' + 'VWWW' + 'WWWw' + 'WWWw',
        'VWWW' + 'VWWW' + 'WWWw' + 'WWWw',
        'WWWW' + 'WWWW' + 'WWWw' + 'WWWw',
        'WWWW' + 'WWWW' + 'WWWw' + 'WWWw',
        'WWWw' + 'WWWw' + 'WWWw' + 'WWWw',
        'WWWw' + 'WWWw' + 'wwww' + 'wwww',
        'wwww' + 'wwww' + 'wwww' + 'wwww']))
    return L.im


def helm():
    """the cap: a stepped cone - its rim round the brow (armour-sized, 3..13), narrowing over the crown, then the long point
    flopping back and down the back of the head in four steps"""
    G, Gd, Gk = K.shaded(GREEN, base=2), K.shaded(GREEN, base=1), K.shaded(GREEN, base=0)
    H = K.Helm('hero_cap')
    H.box((3, 9, 3), (13, 13, 13), G, over={'north': K.grid(['LLLLLLLLLL', 'GGGGGGGGGG', 'GGGGGGGGGG', 'dddddddddd'], PAL)})   # the brim of it (armour-sized)
    H.box((4, 13, 4), (12, 14, 14), G, faces=('north', 'east', 'west', 'up', 'south'))                     # the crown, rounded over...
    H.box((5, 14, 8), (11, 15, 16), G, faces=('north', 'east', 'west', 'up', 'south'))                     # ...rising toward the back
    H.box((4, 10, 13), (12, 14, 16), G, faces=('south', 'east', 'west', 'down'))                          # the point: out behind, narrowing...
    H.box((5, 9, 16), (11, 13, 18), G, faces=('south', 'east', 'west', 'up', 'down'))
    H.box((6, 6, 17), (10, 10, 20), Gd, faces=('south', 'east', 'west', 'up', 'down', 'north'))
    H.box((7, 3, 18), (9, 6, 20), Gk, faces=('south', 'east', 'west', 'down', 'north'))                    # ...and its tip flopping down
    return H


# ---------------------------------------------------------------------------------------------------------------- icons
IP = dict(PAL, k='#121014')
ICON_ROWS = {
    'hero_helmet': [            # the cap from the side: the crown, the point flopping down to the right
        '................',
        '................',
        '....LLLLG.......',
        '...LHHLLGG......',
        '..LHLLLGGGG.....',
        '..LLLLGGGGGg....',
        '..LLLGGGGGGGg...',
        '..LGGGGGGGGGGg..',
        '..GGGGGGGGgGGGg.',
        '..ddddddddggGGg.',
        '...........gGGg.',
        '............gGg.',
        '............gGg.',
        '.............gd.',
        '................',
        '................'],
    'hero_chestplate': [        # the tunic: the white collar, the baldric, the belt and its gold buckle
        '................',
        '..LLLG....GGGg..',
        '.LHLLGG..GGGBng.',
        '.LHLGGVWWVGBnGg.',
        '.LLLGGGwwGBnGGg.',
        '.CXCLGGGGBnGgcC.',
        '.....LGGBnGGg...',
        '.....LGBnGGGg...',
        '.....LBnGGGGg...',
        '.....BBBZYBBB...',
        '.....nnnYynnn...',
        '.....LGGGGGGg...',
        '.....GGGGGGGg...',
        '.....ggggggggd..',
        '................',
        '................'],
    'hero_leggings': [          # the skirt of the tunic, pale leggings
        '................',
        '................',
        '...BBBBBBBBBB...',
        '...nnnnnnnnnn...',
        '...LGGGGGGGGg...',
        '...LGGGGGGGGg...',
        '...gggggggggd...',
        '...VWWw..VWWw...',
        '...VWWw..VWWw...',
        '...VWWw..VWWw...',
        '...WWWw..WWWw...',
        '...WWWw..WWWw...',
        '...WWWw..WWWw...',
        '...wwwv..wwwv...',
        '................',
        '................'],
    'hero_boots': [             # brown knee boots, the cuff folded over
        '................',
        '................',
        '..mmmm...mmmm...',
        '..llll...llll...',
        '..nnnn...nnnn...',
        '..lBBn...lBBn...',
        '..lBBn...lBBn...',
        '..lBBn...lBBn...',
        '..lBBn...lBBn...',
        '.llBBn..llBBn...',
        'lBBBBn.lBBBBn...',
        'lBBBBn.lBBBBn...',
        'bbbbbb.bbbbbb...',
        '................',
        '................',
        '................'],
}


def icons():
    """the four icons, outlined (gen_rp's ICONS loop finishes them with vanilla.process)"""
    return {k: K.icon(rows, IP) for k, rows in ICON_ROWS.items()}


PIECES = ('hero_helmet', 'hero_chestplate', 'hero_leggings', 'hero_boots')


def write(R2):
    """the layers (asset bm:hero), the cap's model and the helmet's item definition (3D on the head, the icon elsewhere)"""
    humanoid().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid', 'hero.png'))
    leggings().save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid_leggings', 'hero.png'))
    R2.wj('assets/bm/equipment/hero.json', {'layers': {'humanoid': [{'texture': 'bm:hero'}], 'humanoid_leggings': [{'texture': 'bm:hero'}]}})
    K.write_helm(R2, 'hero_helmet', helm())


def rp(R):
    R.ICONS.update(icons())
    R.POST.append(write)
