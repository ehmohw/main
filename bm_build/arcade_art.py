"""2.94d: THE ARCADE's art (phase216) - its four armour sets, and the icons and props from PixelLab (ref/pixellab/arcade/icons:
an item's icon as is; a prop a voxel model of its icon, so it stands in the world as pixel art you can walk round).

v299a: the four sets drawn again, the vanilla way (armor_kit.py: hand-placed pixels on the standard 64 x 32 layers, flat fields,
3-4 shades lit from the top left, square details), and each closer to the one it's an homage to:
  BOUNTY HUNTER   the Varia suit: a 3D helmet (orange-red, the wide green visor, the crest down its crown, the round side
                  lights), the great round pauldrons, the chest plate over a grey ribbed waist, yellow arms and thighs, orange
                  knee guards, red-orange boots.
  BLUE BOMBER     a 3D helmet (dark blue, the light-blue stripe from brow to nape, the round ear pieces, the face open), a
                  light-blue body and upper arms, dark-blue gloves with their flared cuffs, dark-blue shorts, light-blue
                  thighs, flared dark-blue boots.
  PLUMBER         a 3D cap (red, its brim, the white emblem with the red M), the red shirt under blue overalls - the straps,
                  the bib, the yellow buttons - white gloves, brown shoes.
  VAMPIRE HUNTER  a red-brown headband knotted at the back, its tails hanging (a layer: your hair shows); the leather
                  cuirass laced up the front, its shoulder guards, bare arms and leather bracers; the belt and its iron
                  buckle, the leather tassets; dark breeches; heavy boots, a strap and buckle at the ankle.
A 3D helm is the item's own model on the head (a head item with no armour asset); the layer's head is still drawn, flat - only
an old copy that still carries the asset shows it. The icons: the PixelLab ones still where they read well; the rest drawn
here (ICON_ROWS) at 16 x 16 in the pack's icon style."""
import os
from PIL import Image

import armor_kit as K

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = os.path.join(HERE, 'ref', 'pixellab', 'arcade', 'icons')
SETS = ('hunter', 'bomber', 'plumber', 'vhunter')
HELM_3D = {'hunter': 'hunter_helm', 'bomber': 'bomber_helm', 'plumber': 'plumber_cap'}     # (set: its helm, a 3D model)

# ===================================================================================================== BOUNTY HUNTER (Varia)
HU = {'k': '#3a0c04', 'r': '#7a1e0a', 'o': '#b03412', 'O': '#de5a1c', 'h': '#ff8a3c', 'H': '#ffbe7a',          # red-orange plate
      'y': '#8a5c0a', 'Y': '#d6a018', 'U': '#f6d040', 'u': '#fff09a',                                        # yellow
      'g': '#0c4416', 'G': '#22a034', 'E': '#7aea6e', 'e': '#d4ffc8',                                        # the visor
      'c': '#24282e', 'C': '#4a5058', 'S': '#7a828c'}                                                       # the ribbed grey suit


def hunter():
    L = K.Layer(HU)
    L.faces('head', top=['hhhhhhhh', 'hOOYYOOh', 'hOOYYOOo', 'hOOYYOOo', 'OOOYYOOo', 'OOOYYOOo', 'OOOYYOOo', 'oooyyooo'])
    L.faces('head', **K.head_ring([
        'hhhhhhhh' + 'hhhUUhhh' + 'OOOOOOOO' + 'OOOYYOOO',
        'OOOOOOOO' + 'OOOYYOOO' + 'OOOOOOOO' + 'OOOYYOOO',
        'OOOOOOOO' + 'kkkkkkkk' + 'OOOOOOOO' + 'OOOOOOOO',
        'OOOkkOOO' + 'keEGGGgk' + 'OOOkkOOO' + 'OOOOOOOO',
        'OOkUUkOO' + 'kEGGGGgk' + 'OOkUUkOO' + 'OOOOOOOO',
        'OOkYYkOO' + 'kGGGGggk' + 'OOkYYkOO' + 'oOOOOOOo',
        'OOOkkOOo' + 'okggggko' + 'oOOkkOOO' + 'oooooooo',
        'oooooooo' + 'rrrrrrrr' + 'oooooooo' + 'rrrrrrrr']))
    L.faces('body', top=['OOOOOOOO', 'OooooooO', 'ooooooOo', 'oooooooo'], bottom=['rrrrrrrr'] * 4)
    L.faces('body', **K.body_ring([
        # right  front       left   back
        'Oooo' + 'OOOooOOo' + 'oooo' + 'OOOooOOo',
        'oooo' + 'OOooooOr' + 'oooo' + 'ooooooor',
        'oooo' + 'Ooooooor' + 'oooo' + 'ooooooor',
        'ooor' + 'ooooooor' + 'ooor' + 'ooorroor',
        'ooor' + 'rooooorr' + 'ooor' + 'ooorroor',
        'rrrr' + 'krrrrrrk' + 'rrrr' + 'rrrrrrrr',
        'SSSC' + 'kSSSSSSk' + 'SSSC' + 'SSSSSSSC',
        'cccc' + 'kcccccck' + 'cccc' + 'cccccccc',
        'SSSC' + 'kSSSSSSk' + 'SSSC' + 'SSSSSSSC',
        'yyyy' + 'yyyUUyyy' + 'yyyy' + 'yyyyyyyy',
        'oooo' + 'OooYYooo' + 'oooo' + 'oooooooo',
        'rrrr' + 'rrrrrrrr' + 'rrrr' + 'rrrrrrrr']))
    # the pauldrons: a great orange dome over each shoulder (lit at its crown), a dark rim under it; the grey suit at the
    # elbow, yellow forearms
    L.faces('arm', top=['hHHh', 'HHHH', 'hHHh', 'Ohho'], bottom=['rrrr'] * 4)
    L.faces('arm', **K.ring([
        # outer  front  inner  back
        'HHHh' + 'HHHh' + 'hhhO' + 'hhhO',
        'Hhhh' + 'Hhhh' + 'hhhO' + 'hhhO',
        'hhhh' + 'hhhh' + 'hhOO' + 'hhOO',
        'hOOO' + 'hOOO' + 'OOOo' + 'OOOo',
        'OOOo' + 'OOOo' + 'OOOo' + 'oooo',
        'kkkk' + 'kkkk' + 'kkkk' + 'kkkk',
        'SSSC' + 'SSSC' + 'SSSC' + 'SSSC',
        'hhhh' + 'hhhh' + 'hhhO' + 'hhhO',
        'hOOO' + 'hOOO' + 'OOOo' + 'OOOo',
        'hOOO' + 'hOOO' + 'OOOo' + 'OOOo',
        'OOOo' + 'OOOo' + 'OOOo' + 'oooo',
        'rrrr' + 'rrrr' + 'rrrr' + 'rrrr']))
    # the boots
    L.faces('leg', top=['....'] * 4, bottom=['kkkk'] * 4)
    L.faces('leg', **K.ring(['....' * 4] * 6 + [
        'yyyy' + 'yyyy' + 'yyyy' + 'yyyy',
        'hhhh' + 'hhhh' + 'hhhO' + 'hhhO',
        'hOOO' + 'hOOO' + 'OOOo' + 'OOOo',
        'OOOO' + 'OOOO' + 'OOOo' + 'OOOo',
        'OOOo' + 'OOOo' + 'OOOo' + 'oooo',
        'rrrr' + 'rrrr' + 'rrrr' + 'rrrr']))
    Lg = K.Layer(HU)
    Lg.faces('body', top=['........'] * 4, bottom=['rrrrrrrr'] * 4)
    Lg.faces('body', **K.body_ring(['....' + '........' + '....' + '........'] * 8 + [
        'yyyy' + 'yyyUUyyy' + 'yyyy' + 'yyyyyyyy',
        'OOOo' + 'hOOYYOOo' + 'OOOo' + 'OOOOOOOo',
        'OOOo' + 'OOOOOOOo' + 'OOOo' + 'OOOOOOOo',
        'rrrr' + 'rrrrrrrr' + 'rrrr' + 'rrrrrrrr']))
    Lg.faces('leg', top=['OOOO'] * 4, bottom=['rrrr'] * 4)
    Lg.faces('leg', **K.ring([
        'rrrr' + 'rrrr' + 'rrrr' + 'rrrr',
        'UYYY' + 'UYYY' + 'YYYy' + 'YYYy',
        'UYYY' + 'UYYY' + 'YYYy' + 'YYYy',
        'YYYY' + 'YYYY' + 'YYYy' + 'YYYy',
        'yyyy' + 'yyyy' + 'yyyy' + 'yyyy',
        'hhhO' + 'hHhO' + 'OOOo' + 'OOOo',
        'OOOo' + 'hOOo' + 'OOOo' + 'oooo',
        'rrrr' + 'rrrr' + 'rrrr' + 'rrrr',
        'YYYy' + 'YYYy' + 'YYYy' + 'YYYy',
        'YYYy' + 'YYYy' + 'YYYy' + 'YYYy',
        'yyyy' + 'yyyy' + 'yyyy' + 'yyyy',
        'yyyy' + 'yyyy' + 'yyyy' + 'yyyy']))
    return L.im, Lg.im


def hunter_helm():
    """the helmet: armour-sized, orange-red; the wide green visor (a glint at its top left) over a dark chin; a crest down
    the crown from brow to nape; a round yellow light on each side"""
    RO = [HU['k'], HU['r'], HU['o'], HU['O'], HU['h'], HU['H']]
    O = K.shaded(RO, base=3)
    face = K.grid(['hhhhhhhhhh',
                   'hOOOOOOOOO',
                   'OkkkkkkkkO',
                   'kEeEGGGGgk',
                   'kEEGGGGGgk',
                   'kGGGGGGggk',
                   'okggggggko',
                   'OokkkkkkoO',
                   'OOOrrrrOOo',
                   'oooooooooo'], HU)
    side = K.grid(['hhhhhhhhhh',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'OOOOOOOOOO',
                   'oooooooooo',
                   'rrrrrrrrrr'], HU)
    H = K.Helm('hunter_helm_3d')
    H.box((3, 3, 3), (13, 13, 13), O, faces=('north', 'south', 'east', 'west', 'up'), over={'north': face, 'east': side, 'west': side, 'south': side})
    H.box((7, 13, 3), (9, 14, 13), K.shaded(RO, base=4), faces=('north', 'south', 'east', 'west', 'up'))       # the crest
    light = K.grid(['rrr', 'rUY', 'ryy'], HU)
    for x0, x1 in ((2, 3), (13, 14)):                                                                          # the side lights
        H.box((x0, 6, 7), (x1, 9, 10), K.shaded([HU['k'], HU['r'], HU['o']], base=1), over={'east': light, 'west': light})
    return H


# ===================================================================================================== BLUE BOMBER
BO = {'k': '#081440', 'd': '#0e2470', 'B': '#1a44c0', 'b': '#2a5ce0', 'L': '#5a8cff',                         # dark blue
      'q': '#0a5a8c', 'c': '#1890c8', 'C': '#38c0f4', 'X': '#84e0ff', 'x': '#d0f6ff',                         # light blue
      's': '#3a3a48'}


def bomber():
    L = K.Layer(BO)
    L.faces('head', top=['bbbCCbbb', 'bBBCCBBB', 'bBBCCBBB', 'bBBCCBBB', 'BBBCCBBB', 'BBBCCBBB', 'BBBCCBBd', 'BBBccBdd'])
    L.faces('head', **K.head_ring([
        'bbbbbbbb' + 'bbbXXbbb' + 'BBBBBBBB' + 'BBBccBBB',
        'BBBBBBBB' + 'BBBCCBBB' + 'BBBBBBBB' + 'BBBccBBB',
        'BBBBBBBB' + 'BBBccBBB' + 'BBBBBBBB' + 'BBBBBBBB',
        'BBkkkkBB' + 'B......B' + 'BBkkkkBB' + 'BBBBBBBB',
        'BBkCXkBB' + 'B......B' + 'BBkXCkBB' + 'BBBBBBBB',
        'BBkccqBB' + 'B......B' + 'BBqcckBB' + 'BBBBBBBB',
        'BBkkkkBB' + 'd......d' + 'BBkkkkBB' + 'dBBBBBBd',
        'dddddddd' + 'k......k' + 'dddddddd' + 'dddddddd']))
    L.faces('body', top=['XXXXXXXX', 'XCCCCCCC', 'CCCCCCCC', 'CCCCCCCc'], bottom=['qqqqqqqq'] * 4)
    L.faces('body', **K.body_ring([
        'XXXC' + 'XXXXXXXC' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'XCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'XCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'CCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'CCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'CCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'CCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'CCCc' + 'CCCCCCCc' + 'CCCc' + 'CCCCCCCc',
        'cccc' + 'cccccccc' + 'cccc' + 'cccccccc',
        'cccq' + 'cccccccq' + 'cccq' + 'cccccccq',
        'qqqq' + 'qqqqqqqq' + 'qqqq' + 'qqqqqqqq',
        'kkkk' + 'kkkkkkkk' + 'kkkk' + 'kkkkkkkk']))
    L.faces('arm', top=['XXXX', 'XCCC', 'XCCC', 'CCCc'], bottom=['dddd'] * 4)
    L.faces('arm', **K.ring([
        'XXXX' + 'XXXX' + 'CCCC' + 'CCCC',
        'XCCC' + 'XCCC' + 'CCCc' + 'CCCc',
        'CCCC' + 'CCCC' + 'CCCc' + 'CCCc',
        'CCCC' + 'CCCC' + 'CCCc' + 'CCCc',
        'cccc' + 'cccc' + 'cccc' + 'cccc',
        'kkkk' + 'kkkk' + 'kkkk' + 'kkkk',
        'LLLL' + 'LLLL' + 'LLLb' + 'LLLb',
        'bbbB' + 'bbbB' + 'BBBd' + 'BBBd',
        'bBBB' + 'bBBB' + 'BBBd' + 'BBBd',
        'bBBB' + 'bBBB' + 'BBBd' + 'BBBd',
        'BBBB' + 'BBBB' + 'BBBd' + 'BBBd',
        'dddd' + 'dddd' + 'dddd' + 'dddd']))
    L.faces('leg', top=['....'] * 4, bottom=['kkkk'] * 4)
    L.faces('leg', **K.ring(['....' * 4] * 6 + [
        'LLLL' + 'LLLL' + 'LLLb' + 'LLLb',
        'bbbB' + 'bbbB' + 'BBBd' + 'BBBd',
        'bBBB' + 'bBBB' + 'BBBd' + 'BBBd',
        'BBBB' + 'BBBB' + 'BBBd' + 'BBBd',
        'BBBd' + 'bBBd' + 'BBBd' + 'dddd',
        'kkkk' + 'kkkk' + 'kkkk' + 'kkkk']))
    Lg = K.Layer(BO)
    Lg.faces('body', top=['........'] * 4, bottom=['dddddddd'] * 4)
    Lg.faces('body', **K.body_ring(['....' + '........' + '....' + '........'] * 8 + [
        'bbbB' + 'bbbbbbbB' + 'BBBB' + 'BBBBBBBB',
        'BBBd' + 'bBBBBBBd' + 'BBBd' + 'BBBBBBBd',
        'BBBd' + 'bBBBBBBd' + 'BBBd' + 'BBBBBBBd',
        'dddd' + 'dddddddd' + 'dddd' + 'dddddddd']))
    Lg.faces('leg', top=['BBBB'] * 4, bottom=['cccc'] * 4)
    Lg.faces('leg', **K.ring([
        'bBBB' + 'bBBB' + 'BBBd' + 'BBBd',
        'BBBB' + 'BBBB' + 'BBBd' + 'BBBd',
        'dddd' + 'dddd' + 'dddd' + 'dddd',
        'XCCC' + 'XCCC' + 'CCCc' + 'CCCc',
        'XCCC' + 'XCCC' + 'CCCc' + 'CCCc',
        'CCCC' + 'CCCC' + 'CCCc' + 'CCCc',
        'CCCc' + 'CCCc' + 'CCCc' + 'CCCc',
        'cccc' + 'cccc' + 'cccc' + 'cccc',
        'cccc' + 'cccc' + 'cccc' + 'cccc',
        'cccq' + 'cccq' + 'cccq' + 'cccq',
        'qqqq' + 'qqqq' + 'qqqq' + 'qqqq',
        'qqqq' + 'qqqq' + 'qqqq' + 'qqqq']))
    return L.im, Lg.im


def bomber_helm():
    """the helmet: armour-sized, dark blue, the face left open; the light-blue stripe from the brow over the crown to the
    nape; a round ear piece on each side (a dark rim, a light-blue middle)"""
    B = K.shaded([BO['k'], BO['d'], BO['B'], BO['b'], BO['L']], base=2)
    face = K.grid(['bbbbXXbbbb',
                   'BBBBCCBBBB',
                   'BBBBccBBBB',
                   'BB......BB',
                   'B........B',
                   'B........B',
                   'B........B',
                   'B........B',
                   'd........d',
                   'k........k'], BO)
    side = K.grid(['bbbbbbbbbb'] + ['BBBBBBBBBB'] * 7 + ['dddddddddd', 'kkkkkkkkkk'], BO)
    back = K.grid(['bbbbCCbbbb'] + ['BBBBCCBBBB'] * 3 + ['BBBBccBBBB'] * 3 + ['BBBBBBBBBB', 'dddddddddd', 'kkkkkkkkkk'], BO)
    top = K.grid(['bbbbXXbbbb'] + ['bBBBCCBBBB'] * 8 + ['BBBBccBBBd'], BO)
    H = K.Helm('bomber_helm_3d')
    H.box((3, 3, 3), (13, 13, 13), B, faces=('north', 'south', 'east', 'west', 'up'),
          over={'north': face, 'east': side, 'west': side, 'south': back, 'up': top})
    ear = K.grid(['.XC.', 'XddC', 'CddC', '.Cc.'], BO)
    for x0, x1 in ((2, 3), (13, 14)):
        H.box((x0, 5, 6), (x1, 9, 10), K.shaded([BO['q'], BO['q'], BO['c'], BO['C']], base=2), faces=('east', 'west', 'up', 'down', 'north', 'south'), over={'east': ear, 'west': ear})
    return H


# ===================================================================================================== PLUMBER
PL = {'k': '#3a0606', 'r': '#7e1010', 'R': '#c81c1c', 'h': '#ee4434', 'H': '#ff8a72',                           # red
      'q': '#0a1450', 'u': '#142c8c', 'U': '#2246c8', 'v': '#4a6eec',                                          # blue
      'y': '#a07a0a', 'Y': '#ffd820',                                                                         # buttons
      'g': '#9aa0aa', 'w': '#d8dce4', 'W': '#ffffff',                                                         # gloves
      'b': '#2e180a', 'n': '#4e2c12', 'B': '#74441e', 'l': '#9a6430'}                                         # shoes


def plumber():
    L = K.Layer(PL)
    L.faces('head', top=['hhhhhhhh', 'hRRRRRRR', 'hRRRRRRR', 'hRRRRRRR', 'RRRRRRRR', 'RRRRRRRR', 'RRRRRRRr', 'RRRRRrrr'])
    L.faces('head', **K.head_ring([
        'hhhhhhhh' + 'hWWWWWWh' + 'RRRRRRRR' + 'RRRRRRRR',
        'RRRRRRRR' + 'WRWWWWRW' + 'RRRRRRRR' + 'RRRRRRRR',
        'RRRRRRRR' + 'WRRWWRRW' + 'RRRRRRRR' + 'RRRRRRRR',
        'rrrrrrrr' + 'kkkkkkkk' + 'rrrrrrrr' + 'rrrrrrrr'] + ['........' * 4] * 4))
    L.faces('body', top=['hhUhhUhh', 'RRURRURR', 'RRURRURR', 'RRURRURr'], bottom=['uuuuuuuu'] * 4)
    L.faces('body', **K.body_ring([
        # right  front       left   back
        'hhhR' + 'hUhhhhUR' + 'RRRr' + 'hUhhhhUR',
        'RRRr' + 'hURRRRUr' + 'RRRr' + 'RURRRRUr',
        'RRRr' + 'hURRRRUr' + 'RRRr' + 'RRURRURr',
        'RRRr' + 'hURRRRUr' + 'RRRr' + 'RRRUURRr',
        'RRRr' + 'RURRRRUr' + 'RRRr' + 'RRRUURRr',
        'RRRr' + 'RYvvvvYr' + 'RRRr' + 'RRURRURr',
        'RRRr' + 'RyUUUUyr' + 'RRRr' + 'RURRRRUr',
        'rrrr' + 'rUUUUUUr' + 'rrrr' + 'UUUUUUUU',
        'vvvv' + 'vUUUUUUu' + 'vvvv' + 'vUUUUUUu',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'uuuu' + 'uuuuuuuu' + 'uuuu' + 'uuuuuuuu']))
    L.faces('arm', top=['hhhh', 'hRRR', 'hRRR', 'RRRr'], bottom=['wwww'] * 4)
    L.faces('arm', **K.ring([
        'hhhh' + 'hhhh' + 'RRRR' + 'RRRR',
        'hRRR' + 'hRRR' + 'RRRr' + 'RRRr',
        'RRRR' + 'RRRR' + 'RRRr' + 'RRRr',
        'RRRR' + 'RRRR' + 'RRRr' + 'RRRr',
        'RRRR' + 'RRRR' + 'RRRr' + 'RRRr',
        'RRRR' + 'RRRR' + 'RRRr' + 'RRRr',
        'RRRr' + 'RRRr' + 'RRRr' + 'RRRr',
        'rrrr' + 'rrrr' + 'rrrr' + 'rrrr',
        'WWWW' + 'WWWW' + 'WWWw' + 'WWWw',
        'WWWW' + 'WWWW' + 'WWWw' + 'WWWw',
        'WWWw' + 'WWWw' + 'wwww' + 'wwww',
        'gggg' + 'gggg' + 'gggg' + 'gggg']))
    L.faces('leg', top=['....'] * 4, bottom=['bbbb'] * 4)
    L.faces('leg', **K.ring(['....' * 4] * 8 + [
        'llll' + 'llll' + 'lllB' + 'lllB',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'BBBn' + 'BBBn' + 'BBBn' + 'nnnn',
        'bbbb' + 'bbbb' + 'bbbb' + 'bbbb']))
    Lg = K.Layer(PL)
    Lg.faces('body', top=['........'] * 4, bottom=['uuuuuuuu'] * 4)
    Lg.faces('body', **K.body_ring(['....' + '........' + '....' + '........'] * 6 + [
        'vvvv' + 'vvvvvvvv' + 'vvvv' + 'vvvvvvvv',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'UUUu' + 'vUUUUUUu' + 'UUUu' + 'UUUUUUUu',
        'uuuu' + 'uuuuuuuu' + 'uuuu' + 'uuuuuuuu']))
    Lg.faces('leg', top=['UUUU'] * 4, bottom=['qqqq'] * 4)
    Lg.faces('leg', **K.ring([
        'vUUU' + 'vUUU' + 'UUUu' + 'UUUu',
        'vUUU' + 'vUUU' + 'UUUu' + 'UUUu',
        'UUUU' + 'UUUU' + 'UUUu' + 'UUUu',
        'UUUU' + 'UUUU' + 'UUUu' + 'UUUu',
        'UUUu' + 'UUUu' + 'UUUu' + 'UUUu',
        'UUUu' + 'UUUu' + 'UUUu' + 'UUUu',
        'UUUu' + 'UUUu' + 'UUUu' + 'uuuu',
        'UUUu' + 'UUUu' + 'uuuu' + 'uuuu',
        'uuuu' + 'uuuu' + 'uuuu' + 'uuuu',
        'vvvv' + 'vvvv' + 'vvvv' + 'vvvv',
        'UUUu' + 'UUUu' + 'UUUu' + 'UUUu',
        'qqqq' + 'qqqq' + 'qqqq' + 'qqqq']))
    return L.im, Lg.im


def plumber_cap():
    """the cap: a puffy red crown (armour-sized, rising past the head), the white emblem with its red M on the front, the
    brim out over the eyes"""
    RR = [PL['k'], PL['r'], PL['R'], PL['h'], PL['H']]
    R = K.shaded(RR, base=2)
    face = K.grid(['hhWWWWWWhh',
                   'RWRRWWRRWR',
                   'RWRWRRWRWR',
                   'RWRWWWWRWR',
                   'RRWWWWWWRR',
                   'RRRRRRRRRR'], PL)
    H = K.Helm('plumber_cap_3d')
    H.box((3, 8, 3), (13, 14, 13), R, faces=('north', 'south', 'east', 'west', 'up', 'down'), over={'north': face})
    H.box((3, 8, 0), (13, 9, 3), K.shaded(RR, base=2), faces=('north', 'east', 'west', 'up', 'down'),
          over={'up': K.grid(['hhhhhhhhhh', 'RRRRRRRRRR', 'RRRRRRRRRR'], PL), 'down': K.grid(['kkkkkkkkkk'] * 3, PL)})
    return H


# ===================================================================================================== VAMPIRE HUNTER
VH = {'k': '#1e1008', 'b': '#3a2210', 'n': '#5a3618', 'B': '#7a4c24', 'l': '#9c6a36', 'm': '#c08e54',         # leather
      'r': '#4a0c08', 'R': '#8a1c12', 'h': '#b8361e', 'H': '#dc5a3a',                                       # the headband
      's': '#5a5e66', 'S': '#a0a6b0', 'X': '#dce0e8',                                                        # iron
      'd': '#241a16', 'D': '#3a2c26', 'E': '#54443a'}                                                       # dark breeches


def vhunter():
    L = K.Layer(VH)
    L.faces('head', top=['........'] * 8)
    L.faces('head', **K.head_ring([
        '........' + '........' + '........' + '........',
        '........' + '........' + '........' + '........',
        'HHHHHHHH' + 'HHHHHHHH' + 'hhhhhhhh' + 'hhhHHhhh',
        'hhhhhhhh' + 'hhhhhhhh' + 'hhhhhhhh' + 'hhRRRRhh',
        'rrrrrrrr' + 'rrrrrrrr' + 'rrrrrrrr' + 'rrrhRrrr',
        '........' + '........' + '........' + '...hR...',
        '........' + '........' + '........' + '..hR.hR.',
        '........' + '........' + '........' + '..rr.rr.']))
    L.faces('body', top=['mmmmmmmm', 'mBBBBBBl', 'lBBBBBBl', 'BBBBBBBn'], bottom=['bbbbbbbb'] * 4)
    L.faces('body', **K.body_ring([
        # right  front       left   back
        'mmmm' + 'mmmnnmmm' + 'mmml' + 'mmmmmmml',
        'lBBn' + 'lllnnBBn' + 'BBBn' + 'lBBBBBBn',
        'lBBn' + 'lmlnnlBn' + 'BBBn' + 'lBBBBBBn',
        'lBBn' + 'llllllBn' + 'BBBn' + 'lBBBBBBn',
        'BBBn' + 'lllllBBn' + 'BBBn' + 'BBBBBBBn',
        'BBBn' + 'BllllBBn' + 'BBBn' + 'BBBBBBBn',
        'BBBn' + 'BBBBBBBn' + 'BBBn' + 'BBBBBBBn',
        'nnnn' + 'nnnnnnnn' + 'nnnn' + 'nnnnnnnn',
        'kkkk' + 'kkkXSkkk' + 'kkkk' + 'kkkkkkkk',
        'bbbb' + 'bbbSsbbb' + 'bbbb' + 'bbbbbbbb',
        'lBBn' + 'lBBnlBBn' + 'lBBn' + 'lBBnlBBn',
        'nnnb' + 'nnnbnnnb' + 'nnnb' + 'nnnbnnnb']))
    # shoulder guards, bare elbows, bracers
    L.faces('arm', top=['mmmm', 'mllm', 'mllm', 'llll'], bottom=['....'] * 4)
    L.faces('arm', **K.ring([
        'mmmm' + 'mmmm' + 'mmml' + 'mmml',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'BBBn' + 'BBBn' + 'BBBn' + 'nnnn',
        'nnnn' + 'nnnn' + 'nnnn' + 'nnnn',
        '....' * 4, '....' * 4,
        'mmmm' + 'mmmm' + 'mmml' + 'mmml',
        'lBBn' + 'lBBn' + 'BBBn' + 'BBBn',
        'lBBn' + 'lBBn' + 'BBBn' + 'BBBn',
        'nnnn' + 'nnnn' + 'nnnn' + 'nnnn',
        'bbbb' + 'bbbb' + 'bbbb' + 'bbbb']))
    # heavy boots to the knee: the cuff folded over, a strap and buckle at the ankle
    L.faces('leg', top=['....'] * 4, bottom=['kkkk'] * 4)
    L.faces('leg', **K.ring(['....' * 4] * 4 + [
        'mmmm' + 'mmmm' + 'mmml' + 'mmml',
        'nnnn' + 'nnnn' + 'nnnn' + 'nnnn',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'lBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'bbbb' + 'bXSb' + 'bbbb' + 'bbbb',
        'BBBB' + 'lBBB' + 'BBBn' + 'BBBn',
        'BBBn' + 'lBBn' + 'BBBn' + 'nnnn',
        'kkkk' + 'kkkk' + 'kkkk' + 'kkkk']))
    Lg = K.Layer(VH)
    Lg.faces('body', top=['........'] * 4, bottom=['bbbbbbbb'] * 4)
    Lg.faces('body', **K.body_ring(['....' + '........' + '....' + '........'] * 8 + [
        'kkkk' + 'kkkkkkkk' + 'kkkk' + 'kkkkkkkk',
        'bbbb' + 'bbbbbbbb' + 'bbbb' + 'bbbbbbbb',
        'lBBn' + 'lBBnlBBn' + 'lBBn' + 'lBBnlBBn',
        'nnnb' + 'nnnbnnnb' + 'nnnb' + 'nnnbnnnb']))
    Lg.faces('leg', top=['DDDD'] * 4, bottom=['dddd'] * 4)
    Lg.faces('leg', **K.ring([
        'lBBn' + 'lBBn' + 'lBBn' + 'lBBn',
        'lBBn' + 'lBBn' + 'lBBn' + 'lBBn',
        'nnnb' + 'nnnb' + 'nnnb' + 'nnnb',
        'EDDD' + 'EDDD' + 'DDDd' + 'DDDd',
        'EDDD' + 'EDDD' + 'DDDd' + 'DDDd',
        'DDDD' + 'DDDD' + 'DDDd' + 'DDDd',
        'DDDd' + 'DDDd' + 'DDDd' + 'DDDd',
        'DDDd' + 'DDDd' + 'DDDd' + 'dddd',
        'DDDd' + 'DDDd' + 'dddd' + 'dddd',
        'dddd' + 'dddd' + 'dddd' + 'dddd',
        'dddd' + 'dddd' + 'dddd' + 'dddd',
        'dddd' + 'dddd' + 'dddd' + 'dddd']))
    return L.im, Lg.im


PAINT = {'hunter': hunter, 'bomber': bomber, 'plumber': plumber, 'vhunter': vhunter}
HELMS = {'hunter_helm': hunter_helm, 'bomber_helm': bomber_helm, 'plumber_cap': plumber_cap}


def paint(which):
    """-> (humanoid layer, humanoid_leggings layer)"""
    return PAINT[which]()


# ===================================================================================================== icons
BOI = dict(BO, W='#ffffff')
VHI = dict(VH)
ICON_ROWS = {            # (iid: (rows, palette) - drawn here, to match the new look; the hunter's and the plumber's are still PixelLab's)
    'bomber_helm': ([     # the helmet from the front: the stripe over the crown, the open face, the round ear pieces
        '................',
        '................',
        '.....bbXXbb.....',
        '....bBBCCBBd....',
        '...bBBBCCBBBd...',
        '..bBBBBccBBBBd..',
        '..bBBBBBBBBBBd..',
        '.XCbBdkkkkdBdCc.',
        '.CXbB......BdCq.',
        '.CCbB......BdCq.',
        '..cbB......Bdq..',
        '...bB......Bd...',
        '...dd......dd...',
        '................',
        '................',
        '................'], BOI),
    'bomber_chest': ([    # the light-blue body and its upper arms; the dark-blue shorts' waistband below
        '................',
        '..XXX......CCc..',
        '.XxXCC....CCCcq.',
        '.XXCCCCCCCCCCcq.',
        '.XCCCCCCCCCCCcq.',
        '..qCXCCCCCCCcq..',
        '...CXCCCCCCCc...',
        '...CCCCCCCCCc...',
        '...CXCCCCCCCc...',
        '...CCCCCCCCCc...',
        '...ccccccccccq..',
        '...bBBBBBBBBBd..',
        '....dddddddddd..',
        '................',
        '................',
        '................'], BOI),
    'bomber_legs': ([     # dark-blue shorts, light-blue legs
        '................',
        '................',
        '...bbbbbbbbbB...',
        '...bBBBBBBBBd...',
        '...bBBBddBBBd...',
        '...XCCc..XCCc...',
        '...XCCc..XCCc...',
        '...XCCc..XCCc...',
        '...CCCc..CCCc...',
        '...CCCc..CCCc...',
        '...CCCc..CCCc...',
        '...cccq..cccq...',
        '................',
        '................',
        '................',
        '................'], BOI),
    'bomber_boots': ([    # dark-blue boots, their flared cuffs
        '................',
        '................',
        '................',
        '.LLLLL..LLLLL...',
        '.bBBBd..bBBBd...',
        '..bBd....bBd....',
        '..bBd....bBd....',
        '..bBd....bBd....',
        '.bbBBd..bbBBd...',
        'bLbBBd.bLbBBd...',
        'bbBBBd.bbBBBd...',
        'dddddd.dddddd...',
        '................',
        '................',
        '................',
        '................'], BOI),
    'vhunter_band': ([    # the red headband, tied at the back, its two tails hanging
        '................',
        '................',
        '................',
        '................',
        '....HHHHHHH.....',
        '..HHhhhhhhhHH...',
        '.Hhr.......rhH..',
        '.hR.........RhRh',
        '.Rr.........rRhR',
        '..RRr.....rRRrhR',
        '....rRRRRRr..hR.',
        '.............hR.',
        '..............R.',
        '................',
        '................',
        '................'], VHI),
    'vhunter_cuirass': ([  # the leather cuirass: shoulder guards, the laced front, the belt and its iron buckle
        '................',
        '..mmm......mml..',
        '.mlllm....mllBn.',
        '.mlBBBmmmmBBBBn.',
        '.lBBBBllllBBBBn.',
        '..kBnllllllBBk..',
        '...BlllmllllBn..',
        '...BllllllllBn..',
        '...BBllllllBBn..',
        '...BBBBBBBBBBn..',
        '...kkkkXSkkkkk..',
        '...lBnlBnlBnlBn.',
        '...nnbnnbnnbnnb.',
        '................',
        '................',
        '................'], VHI),
    'vhunter_legs': ([    # the belt and its tassets, dark breeches
        '................',
        '................',
        '...kkkkXSkkkk...',
        '...lBnlBnlBnB...',
        '...lBnlBnlBnB...',
        '...nbnnbnnbnb...',
        '...EDDD..EDDd...',
        '...EDDD..EDDd...',
        '...EDDd..EDDd...',
        '...DDDd..DDDd...',
        '...DDDd..DDDd...',
        '...DDdd..DDdd...',
        '...dddd..dddd...',
        '................',
        '................',
        '................'], VHI),
    'vhunter_boots': ([   # heavy boots: the cuff folded over, a strap and buckle at the ankle
        '................',
        '................',
        '.mmmmm..mmmmm...',
        '.nnnnn..nnnnn...',
        '..lBBn...lBBn...',
        '..lBBn...lBBn...',
        '..lBBn...lBBn...',
        '..bXSb...bXSb...',
        '.llBBn..llBBn...',
        'lBBBBn.lBBBBn...',
        'lBBBBn.lBBBBn...',
        'kkkkkk.kkkkkk...',
        '................',
        '................',
        '................',
        '................'], VHI),
}


def icon(k):
    if k in ICON_ROWS:
        rows, pal = ICON_ROWS[k]
        return K.icon(rows, pal)
    return Image.open(os.path.join(ICONS, f'{k}.png')).convert('RGBA')


def write_sets(R2):
    """(v299a) the four sets' armour layers and equipment assets, and the 3D helms (phase216's post)"""
    for k in SETS:
        hum, leg = paint(k)
        hum.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid', f'arc_{k}.png'))
        leg.save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', 'humanoid_leggings', f'arc_{k}.png'))
        R2.wj(f'assets/bm/equipment/arc_{k}.json', {'layers': {'humanoid': [{'texture': f'bm:arc_{k}'}], 'humanoid_leggings': [{'texture': f'bm:arc_{k}'}]}})
    for iid, f in HELMS.items():
        K.write_helm(R2, iid, f())
