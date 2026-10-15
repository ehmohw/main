"""2.78: the follower dolls in the Emma doll's chibi style - a big head with a big-eyed face on its front, a little body, stubby
arms and legs, and each one's signature look and thing (Cecil's hood and staff, Leo's helm and trident, Pearlman's top hat and
case...). Built on the Emma doll's own frame (phase46: feet at y 0, the head from y 10.3 to 17.6, the face on its north side,
about 18 units tall), so they stand together as a set.

Twelve: Cecil, Celi, Leo, Democratus, KillerWatt, Apophiss, Tullius, Zib, Pearlman, Donado, Wilfrey and the Frog with Mustache.
Leo, Celi and Democratus wear their followers' own faces (the 36x32 corner of their face sheets, as Emma's doll does); the
others' faces are drawn here, big-eyed, in the same hand."""
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import el as _el, seg as _seg

PIV = (8.0, 8.0, 8.0)
FRONT, UP, SIDE = (0.0, 0.0, -1.0), (0.0, 1.0, 0.0), (1.0, 0.0, 0.0)
FACE_UV = {'north': [0, 0, 9, 8]}         # (a follower face sheet's 36x32 corner, as on Emma's doll)


def e(fr, to, t, rot=None, faces=None, uv=None, sh=None):
    return _el(fr, to, t, PIV, rot, uv=uv, faces=faces, shift=sh)


def s(A, B, w, h, t, up=FRONT):
    return _seg(A, B, w, h, t, PIV, up)


# ---------------------------------------------------------------------------------------------------- textures
def _face(skin, eye, iris=None, mouth='#7a3a2a', blush=None, brow=None, extra=None, lid=None):
    """a chibi face: two big eyes (white, a coloured iris, a black pupil, a shine), a small mouth, blush"""
    im = Image.new('RGBA', (16, 16), hexc(skin)); d = ImageDraw.Draw(im)
    for x0 in (3, 9):
        if eye == 'glow':
            d.rectangle((x0, 6, x0 + 3, 9), fill=hexc(iris)); d.rectangle((x0 + 1, 7, x0 + 2, 8), fill=hexc('#ffffff'))
            continue
        d.rectangle((x0, 5, x0 + 3, 10), fill=hexc('#ffffff'))
        d.rectangle((x0, 7, x0 + 3, 10), fill=hexc(iris or '#3a2a1a'))
        d.rectangle((x0 + 1, 8, x0 + 2, 10), fill=hexc('#101010'))
        d.point((x0 + 1, 6), fill=hexc('#ffffff')); d.point((x0 + 2, 8), fill=hexc('#ffffff'))
        d.line((x0, 4, x0 + 3, 4), fill=hexc(brow or '#202020'))
        if lid: d.rectangle((x0, 5, x0 + 3, 6), fill=hexc(lid))
    if mouth: d.line((7, 12, 8, 12), fill=hexc(mouth))
    if blush:
        d.point((2, 11), fill=hexc(blush)); d.point((3, 11), fill=hexc(blush)); d.point((12, 11), fill=hexc(blush)); d.point((13, 11), fill=hexc(blush))
    if extra: extra(d)
    return im


def textures():
    rnd = random.Random(7)
    N = lambda c, sd, v=6: _noise(c, sd, v)
    S = lambda c, l, sd: _shine(c, l, sd)
    T = {
        # Cecil: violet robe and hood, the hood's dark mouth with two yellow eyes and a jagged grin; his staff
        'dl_cec_robe': N('#5a2a8a', 1101), 'dl_cec_robe_dk': N('#3e1c62', 1102), 'dl_cec_hood_in': N('#141018', 1103, 3),
        'dl_cec_face': _face('#141018', 'glow', '#ffd23a', mouth=None, extra=lambda d: [d.point((x, 12 + (x % 2)), fill=hexc('#d8d8d8')) for x in range(4, 12)]),
        'dl_cec_wood': S('#4a2a18', '#7a4a2a', 1104), 'dl_cec_gold': S('#d8a830', '#ffe890', 1105), 'dl_cec_gem': S('#e04aa0', '#ffb0e0', 1106),
        'dl_cec_glove': N('#2a1a10', 1107, 4),
        # Celi: her face sheet; frost-blue skin, an orange bun, a pale blue coat with a white fur hem, her spear
        'dl_ce_skin': N('#8cc4e8', 1111, 4), 'dl_ce_hair': N('#e8862a', 1112), 'dl_ce_coat': N('#a8c8f0', 1113), 'dl_ce_fur': N('#f4f6fa', 1114, 4),
        'dl_ce_boot': N('#2a3a7a', 1115), 'dl_ce_steel': S('#b8c4d8', '#f0f6ff', 1116), 'dl_ce_shaft': S('#6a8ab8', '#a8c8f0', 1117),
        # Leo: his face sheet; a steel helm with a nasal guard, a blue tunic over mail, a trident
        'dl_le_skin': N('#8a5a3a', 1121, 4), 'dl_le_steel': S('#a0a8b4', '#e4eaf2', 1122), 'dl_le_tunic': N('#2c6ac0', 1123), 'dl_le_mail': N('#7a828e', 1124, 10),
        'dl_le_belt': N('#4a2e1a', 1125), 'dl_le_tri': S('#3a9a8a', '#8ae0d0', 1126), 'dl_le_boot': N('#3a3a44', 1127),
        # Democratus: his face sheet; a deep green hood, black plate, a storm-grey cape, his scythe
        'dl_dm_skin': N('#c88a5a', 1131, 4), 'dl_dm_hood': N('#1e3a22', 1132), 'dl_dm_plate': S('#22262a', '#4a5258', 1133), 'dl_dm_cape': N('#2a3236', 1134),
        'dl_dm_blade': S('#a8e0d8', '#ffffff', 1135), 'dl_dm_shaft': N('#18181a', 1136, 3), 'dl_dm_gold': S('#d8a830', '#ffe890', 1137),
        # KillerWatt: a green alien, dark visor eyes, yellow lightning tendrils
        'dl_kw_skin': N('#4ac04a', 1141), 'dl_kw_belly': N('#9ae07a', 1142), 'dl_kw_bolt': S('#f0d020', '#fff6a0', 1143), 'dl_kw_dark': N('#1a3a1a', 1144, 4),
        'dl_kw_face': _face('#4ac04a', 'glow', '#24124a', mouth='#1a3a1a', extra=lambda d: d.line((5, 13, 10, 13), fill=hexc('#1a3a1a'))),
        # Apophiss: green scales, a gold crown, a pale belly, red eyes
        'dl_apo_scale': N('#2e7a2e', 1151, 9), 'dl_apo_belly': N('#c8d880', 1152), 'dl_apo_gold': S('#e0b030', '#fff0a0', 1153), 'dl_apo_red': N('#c02020', 1154, 4),
        'dl_apo_face': _face('#2e7a2e', 'eye', '#d02020', mouth=None, brow='#143a14', extra=lambda d: [d.line((4, 13, 11, 13), fill=hexc('#143a14')),
                                                                                                   d.point((5, 14), fill=hexc('#ffffff')), d.point((10, 14), fill=hexc('#ffffff'))]),
        # Tullius: a pale-blue skull, one cold eye, the other under a flap; a teal coat, a green top hat, his harpoon
        'dl_tu_bone': N('#a8d8e0', 1161, 5), 'dl_tu_coat': N('#3c8088', 1162), 'dl_tu_hat': N('#163c38', 1163), 'dl_tu_band': N('#4a9a3a', 1164),
        'dl_tu_sash': N('#4a8a3a', 1165), 'dl_tu_steel': S('#8a90b2', '#d6dcf4', 1166), 'dl_tu_shoe': N('#1e4644', 1167),
        'dl_tu_face': _face('#a8d8e0', 'eye', '#8af4ff', mouth='#1a2a30', brow='#5a8f9a',
                            extra=lambda d: [d.rectangle((3, 4, 7, 10), fill=hexc('#5a8f9a')), d.line((5, 12, 11, 12), fill=hexc('#1a2a30')),
                                             [d.point((x, 13), fill=hexc('#e8f4f4')) for x in range(6, 11, 2)]]),
        # Zib: teal Donadian skin, red eyes, a black muzzle, antennae, a dark coat
        'dl_zb_skin': N('#4ab8a8', 1171, 7), 'dl_zb_muzzle': N('#1a1a1a', 1172, 3), 'dl_zb_coat': N('#2a2a44', 1173), 'dl_zb_glow': S('#7aff9a', '#e0ffe8', 1174),
        'dl_zb_face': _face('#4ab8a8', 'eye', '#e02020', mouth=None, brow='#2a6a60'),
        # Pearlman: a penguin - black back, white front, orange beak and feet, a top hat with a blue band, a gold case
        'dl_pm_black': N('#1a1c22', 1181, 4), 'dl_pm_white': N('#f4f4f0', 1182, 3), 'dl_pm_orange': N('#f0901a', 1183), 'dl_pm_band': N('#2a8ad8', 1184),
        'dl_pm_gold': S('#d8a830', '#ffe890', 1185),
        'dl_pm_face': _face('#1a1c22', 'eye', '#3a2a1a', mouth=None, brow='#000000',
                            extra=lambda d: d.rectangle((3, 4, 12, 12), outline=None) or [d.rectangle((2, 4, 13, 12), fill=hexc('#f4f4f0')),
                                                                                        [d.rectangle((x, 5, x + 2, 9), fill=hexc('#101010')) for x in (4, 10)],
                                                                                        [d.point((x + 1, 6), fill=hexc('#ffffff')) for x in (4, 10)]]),
        # Donado: a cream dog in a patched grey shirt - floppy ears, a black nose
        'dl_don_fur': N('#e8d29a', 1191), 'dl_don_ear': N('#d6b66c', 1192), 'dl_don_muzzle': N('#f6eac8', 1193, 4), 'dl_don_shirt': N('#8a8e94', 1194),
        'dl_don_patch': N('#5a6a8a', 1195), 'dl_don_dark': N('#181412', 1196, 2),
        'dl_don_face': _face('#e8d29a', 'eye', '#4a2a10', mouth='#5a2a1a', blush='#e8a890'),
        # Wilfrey: a wither skeleton knight - a charcoal skull, a steel helm, a white tabard with his gold emblem, a sword
        'dl_wil_bone': N('#2a2a2c', 1201, 5), 'dl_wil_steel': S('#8c929a', '#dfe4ea', 1202), 'dl_wil_tabard': N('#ececea', 1203, 4), 'dl_wil_gold': S('#d8a830', '#ffe890', 1204),
        'dl_wil_blade': S('#c8ccd4', '#ffffff', 1205),
        'dl_wil_face': _face('#2a2a2c', 'glow', '#f4f4f4', mouth=None, extra=lambda d: [d.point((x, 12), fill=hexc('#8a8a8a')) for x in range(4, 12, 2)]),
        # the Frog with Mustache: green, a pale throat, eyes up top, a curled moustache, a red bow tie and a gold pin
        'dl_fr_skin': N('#5aa83a', 1211), 'dl_fr_belly': N('#d8e8a0', 1212), 'dl_fr_bow': N('#c82a2a', 1213), 'dl_fr_stache': N('#3a2a18', 1214, 3),
        'dl_fr_gold': S('#d8a830', '#ffe890', 1215), 'dl_fr_eye': _face('#ffffff', 'glow', '#101010', mouth=None),
        'dl_fr_face': _face('#5aa83a', None, None, mouth=None, extra=lambda d: [d.line((3, 11, 12, 11), fill=hexc('#2a5a1a'))]),
    }
    # (the Frog's face has no eyes painted - they sit on top of his head)
    im = Image.new('RGBA', (16, 16), hexc('#5aa83a')); d = ImageDraw.Draw(im); d.line((3, 11, 12, 11), fill=hexc('#2a5a1a')); T['dl_fr_face'] = im
    return T


# ---------------------------------------------------------------------------------------------------- the shared frame
def legs(t, shoe):
    return [e((5, 0, 6.5), (7.5, 1.2, 9.5), shoe), e((8.5, 0, 6.5), (11, 1.2, 9.5), shoe),
            e((5.6, 1.2, 7.3), (7, 3.4, 8.7), t), e((9, 1.2, 7.3), (10.4, 3.4, 8.7), t)]


def torso(t, t2=None):
    return [e((5.2, 3.2, 6.4), (10.8, 10.2, 9.6), t), e((5.0, 3.2, 6.2), (11.0, 4.6, 9.8), t2 or t, sh=(0.4, 0.6))]


def arms(t, hand, up=False):
    """stubby arms at her sides (or the right one raised, holding something up)"""
    a = [e((3.6, 6.4, 7.3), (5.2, 10.0, 8.7), t), e((3.7, 5.4, 7.4), (5.1, 6.4, 8.6), hand)]
    if up:
        a += [e((10.8, 8.4, 7.3), (12.4, 12.0, 8.7), t), e((10.9, 12.0, 7.4), (12.3, 13.0, 8.6), hand)]
    else:
        a += [e((10.8, 6.4, 7.3), (12.4, 10.0, 8.7), t), e((10.9, 5.4, 7.4), (12.3, 6.4, 8.6), hand)]
    return a


def head(skin, face, uv=None, y0=10.3, y1=17.6, w=4.0):
    """the big head and its face (on the north side)"""
    return [e((8 - w, y0, 4.6), (8 + w, y1, 11.4), skin),
            e((8 - w + 0.2, y0 + 0.1, 4.5), (8 + w - 0.2, y1 - 0.4, 4.6), face, faces=('north',), uv=uv or {'north': [0, 0, 16, 16]})]


# ---------------------------------------------------------------------------------------------------- each doll
def models():
    M = {}
    def doll(name, els):
        used = sorted({x['faces'][f]['texture'][1:] for x in els for f in x['faces']})
        tex = {}
        for t in used:
            tex[t] = f'bm:block/{t}'
        M[name] = (tex, els)

    # ---- Cecil: a long robe to the floor, the big pointed hood (a dark mouth with his eyes), gloved hands, the staff
    c = [e((4.6, 0, 5.8), (11.4, 3.4, 10.2), 'dl_cec_robe'), e((5.0, 3.4, 6.2), (11.0, 10.2, 9.8), 'dl_cec_robe', sh=(0.5, 0.3)),
         e((4.4, 0, 5.6), (11.6, 0.6, 10.4), 'dl_cec_robe_dk')] + arms('dl_cec_robe', 'dl_cec_glove', up=True)
    c += [e((3.5, 9.8, 4.3), (12.5, 17.8, 11.9), 'dl_cec_robe'),                                                  # the hood
          e((4.3, 10.4, 4.2), (11.7, 16.6, 4.3), 'dl_cec_face', faces=('north',)),                                # its dark mouth, the eyes
          e((5.0, 17.6, 5.4), (11.0, 19.4, 11.0), 'dl_cec_robe', sh=(0.3, 0.6)), e((6.4, 19.2, 7.0), (9.6, 20.8, 10.0), 'dl_cec_robe_dk'),
          s((8.4, 20.6, 9.4), (6.8, 22.0, 11.2), 1.4, 1.4, 'dl_cec_robe_dk', UP)]                                  # its tip, flopping back
    c += [e((12.0, 0.4, 7.4), (12.8, 15.6, 8.2), 'dl_cec_wood'), e((11.3, 15.4, 7.1), (13.5, 16.0, 8.5), 'dl_cec_gold'),
          s((11.6, 15.8, 7.8), (10.6, 17.4, 7.8), 0.4, 0.4, 'dl_cec_gold'), s((13.2, 15.8, 7.8), (14.2, 17.4, 7.8), 0.4, 0.4, 'dl_cec_gold'),
          e((11.7, 16.0, 7.1), (13.1, 18.2, 8.5), 'dl_cec_gem')]
    doll('doll_cecil', c)

    # ---- Celi: her face; the orange bun and fringe, a pale coat with a fur hem, the spear over her shoulder
    c = legs('dl_ce_boot', 'dl_ce_boot') + torso('dl_ce_coat', 'dl_ce_fur') + arms('dl_ce_coat', 'dl_ce_skin') + head('dl_ce_skin', 'ce_face', FACE_UV)
    c += [e((3.7, 15.6, 4.3), (12.3, 18.2, 11.7), 'dl_ce_hair'), e((3.6, 11.2, 9.4), (12.4, 16.0, 11.8), 'dl_ce_hair', sh=(0.4, 0.2)),
          e((6.2, 17.8, 8.0), (9.8, 20.4, 11.2), 'dl_ce_hair', sh=(0.6, 0.6)),                                    # the bun
          e((3.4, 11.0, 4.8), (4.3, 15.6, 8.0), 'dl_ce_hair'), e((11.7, 11.0, 4.8), (12.6, 15.6, 8.0), 'dl_ce_hair'),
          e((4.9, 9.6, 6.0), (11.1, 10.6, 10.0), 'dl_ce_fur')]                                                     # the collar
    c += [s((12.0, 1.0, 8.6), (13.6, 19.0, 9.6), 0.6, 0.6, 'dl_ce_shaft', SIDE), s((13.6, 19.0, 9.6), (13.9, 21.4, 9.8), 1.0, 0.4, 'dl_ce_steel', SIDE)]
    doll('doll_celi', c)

    # ---- Leo: his face; the steel helm with a crest, a blue tunic over mail, the trident at his side
    c = legs('dl_le_mail', 'dl_le_boot') + torso('dl_le_tunic', 'dl_le_mail') + arms('dl_le_mail', 'dl_le_skin') + head('dl_le_skin', 'le_face', FACE_UV)
    c += [e((5.0, 6.4, 6.1), (11.0, 7.2, 9.9), 'dl_le_belt'),
          e((3.7, 15.2, 4.2), (12.3, 18.4, 11.8), 'dl_le_steel'), e((3.6, 10.6, 8.6), (12.4, 15.4, 11.9), 'dl_le_steel', sh=(0.4, 0.4)),
          e((3.5, 10.8, 4.4), (4.4, 15.4, 8.6), 'dl_le_steel'), e((11.6, 10.8, 4.4), (12.5, 15.4, 8.6), 'dl_le_steel'),
          e((7.4, 18.2, 6.4), (8.6, 20.0, 10.6), 'dl_le_tunic')]                                                   # the crest
    c += [e((12.6, 0.4, 7.6), (13.3, 18.0, 8.3), 'dl_le_tri'), e((11.4, 17.6, 7.6), (14.5, 18.2, 8.3), 'dl_le_tri'),
          e((11.4, 18.2, 7.7), (12.0, 20.0, 8.2), 'dl_le_tri'), e((13.9, 18.2, 7.7), (14.5, 20.0, 8.2), 'dl_le_tri'), e((12.65, 18.2, 7.7), (13.25, 20.6, 8.2), 'dl_le_tri')]
    doll('doll_leo', c)

    # ---- Democratus: his face under a deep hood, black plate, a cape, the scythe
    c = legs('dl_dm_plate', 'dl_dm_plate') + torso('dl_dm_plate', 'dl_dm_cape') + arms('dl_dm_plate', 'dl_dm_plate', up=True) + head('dl_dm_skin', 'dm_face', FACE_UV)
    c += [e((3.5, 10.0, 4.2), (12.5, 18.4, 11.9), 'dl_dm_hood'),                                                  # the hood, open at the face
          e((4.3, 10.4, 4.2), (11.7, 16.8, 4.3), 'dm_face', faces=('north',), uv=FACE_UV),
          e((4.6, 0.4, 9.6), (11.4, 10.0, 10.4), 'dl_dm_cape'), e((7.4, 7.6, 6.0), (8.6, 8.6, 6.3), 'dl_dm_gold')]
    c += [e((11.2, 0.4, 7.6), (12.0, 19.0, 8.4), 'dl_dm_shaft'), s((11.6, 18.8, 8.0), (6.0, 17.2, 8.0), 1.6, 0.35, 'dl_dm_blade'),
          s((6.0, 17.2, 8.0), (4.2, 15.2, 8.0), 1.0, 0.3, 'dl_dm_blade')]
    doll('doll_demo', c)

    # ---- KillerWatt: green, a round belly, claws, a fan of yellow lightning tendrils at his back
    c = legs('dl_kw_skin', 'dl_kw_dark') + torso('dl_kw_skin') + arms('dl_kw_skin', 'dl_kw_dark') + head('dl_kw_skin', 'dl_kw_face')
    c += [e((6.0, 4.2, 6.1), (10.0, 9.0, 6.3), 'dl_kw_belly'), e((6.6, 17.4, 6.6), (9.4, 18.6, 9.4), 'dl_kw_skin'),
          e((7.4, 18.4, 7.4), (8.6, 19.6, 8.6), 'dl_kw_dark')]
    for sx in (1, -1):                                                                                          # the zig-zag tendrils
        b = 8 + sx * 2.0
        c += [s((b, 9.0, 10.0), (8 + sx * 5.0, 12.5, 11.6), 0.7, 0.7, 'dl_kw_bolt', FRONT),
              s((8 + sx * 5.0, 12.5, 11.6), (8 + sx * 3.8, 14.6, 12.2), 0.7, 0.7, 'dl_kw_bolt', FRONT),
              s((8 + sx * 3.8, 14.6, 12.2), (8 + sx * 6.6, 17.6, 12.8), 0.6, 0.6, 'dl_kw_bolt', FRONT)]
    doll('doll_kw', c)

    # ---- Apophiss: coils for a body, little clawed arms, a scaly head with a short snout, the gold crown
    c = [e((3.8, 0, 4.8), (12.2, 2.4, 11.2), 'dl_apo_scale'), e((4.6, 2.2, 5.6), (11.4, 4.6, 10.4), 'dl_apo_scale', sh=(0.4, 0.4)),
         e((5.2, 4.4, 6.0), (10.8, 10.2, 10.0), 'dl_apo_scale', sh=(0.7, 0.2)), e((6.2, 3.2, 5.9), (9.8, 9.6, 6.1), 'dl_apo_belly'),
         s((11.6, 1.0, 9.6), (14.4, 2.8, 12.6), 1.6, 1.6, 'dl_apo_scale', UP), s((14.4, 2.8, 12.6), (14.8, 5.6, 13.0), 1.1, 1.1, 'dl_apo_scale', UP)]
    c += arms('dl_apo_scale', 'dl_apo_belly') + head('dl_apo_scale', 'dl_apo_face')
    c += [e((5.8, 10.8, 3.2), (10.2, 13.0, 4.6), 'dl_apo_scale'), e((6.6, 12.2, 3.1), (7.2, 12.6, 3.2), 'dl_apo_red'), e((8.8, 12.2, 3.1), (9.4, 12.6, 3.2), 'dl_apo_red'),
          e((4.4, 17.4, 5.0), (11.6, 18.4, 11.0), 'dl_apo_gold')]                                                 # the crown band
    for x in (4.6, 7.4, 10.2):
        c.append(e((x, 18.4, 5.2), (x + 1.2, 20.2, 6.4), 'dl_apo_gold'))
        c.append(e((x, 18.4, 9.6), (x + 1.2, 19.6, 10.8), 'dl_apo_gold'))
    c.append(e((7.5, 19.6, 5.1), (8.5, 20.6, 5.3), 'dl_apo_red'))
    doll('doll_apo', c)

    # ---- Tullius: a skull face, one eye under its flap; the teal coat to the knee, a sash; the tall green top hat; his harpoon
    c = legs('dl_tu_sash', 'dl_tu_shoe') + [e((4.8, 2.6, 6.0), (11.2, 10.2, 10.0), 'dl_tu_coat'), e((4.9, 5.4, 5.9), (11.1, 6.6, 10.1), 'dl_tu_sash')]
    c += arms('dl_tu_coat', 'dl_tu_bone') + head('dl_tu_bone', 'dl_tu_face')
    c += [e((3.4, 17.2, 4.0), (12.6, 17.8, 12.0), 'dl_tu_hat'), e((4.8, 17.8, 5.2), (11.2, 22.6, 10.8), 'dl_tu_hat', sh=(0.3, 0.3)),
          e((4.75, 17.8, 5.15), (11.25, 18.8, 10.85), 'dl_tu_band')]
    c += [s((12.4, 0.6, 7.2), (13.4, 17.0, 8.6), 0.6, 0.6, 'dl_tu_steel', SIDE), s((13.4, 17.0, 8.6), (13.6, 19.2, 8.8), 1.2, 0.4, 'dl_tu_steel', SIDE)]
    doll('doll_tul', c)

    # ---- Zib: teal, the black muzzle, red eyes, two antennae with glowing tips, a dark coat
    c = legs('dl_zb_coat', 'dl_zb_muzzle') + torso('dl_zb_coat') + arms('dl_zb_coat', 'dl_zb_skin') + head('dl_zb_skin', 'dl_zb_face')
    c += [e((6.2, 10.6, 3.6), (9.8, 12.8, 4.6), 'dl_zb_muzzle'),
          s((6.2, 17.4, 8.0), (5.0, 21.0, 8.6), 0.4, 0.4, 'dl_zb_skin', FRONT), s((9.8, 17.4, 8.0), (11.0, 21.0, 8.6), 0.4, 0.4, 'dl_zb_skin', FRONT),
          e((4.4, 20.6, 8.0), (5.6, 21.8, 9.2), 'dl_zb_glow'), e((10.4, 20.6, 8.0), (11.6, 21.8, 9.2), 'dl_zb_glow'),
          e((3.4, 13.0, 7.0), (4.2, 16.4, 9.0), 'dl_zb_skin'), e((11.8, 13.0, 7.0), (12.6, 16.4, 9.0), 'dl_zb_skin')]   # (pointed ears)
    doll('doll_zib', c)

    # ---- Pearlman: one round penguin - a black back, a white front, flippers, orange feet and beak; a top hat; his gold case
    c = [e((5, 0, 5.4), (7.5, 0.8, 9.0), 'dl_pm_orange'), e((8.5, 0, 5.4), (11, 0.8, 9.0), 'dl_pm_orange'),
         e((4.4, 0.8, 5.6), (11.6, 10.4, 10.4), 'dl_pm_black'), e((5.2, 1.2, 5.5), (10.8, 9.8, 5.6), 'dl_pm_white', faces=('north',)),
         s((4.4, 9.4, 8.0), (3.0, 5.0, 8.2), 1.2, 2.2, 'dl_pm_black', SIDE), s((11.6, 9.4, 8.0), (13.0, 5.0, 8.2), 1.2, 2.2, 'dl_pm_black', SIDE)]
    c += head('dl_pm_black', 'dl_pm_face', y0=10.2, y1=17.0)
    c += [e((7.0, 12.2, 3.4), (9.0, 13.2, 4.6), 'dl_pm_orange'),
          e((3.6, 16.8, 4.0), (12.4, 17.4, 12.0), 'dl_pm_black'), e((5.0, 17.4, 5.4), (11.0, 21.6, 10.6), 'dl_pm_black', sh=(0.4, 0.4)),
          e((4.95, 17.4, 5.35), (11.05, 18.3, 10.65), 'dl_pm_band'),
          e((12.2, 2.4, 6.4), (14.6, 5.0, 9.6), 'dl_pm_gold'), e((12.9, 5.0, 7.6), (13.9, 5.5, 8.4), 'dl_pm_gold')]  # the case
    doll('doll_pearl', c)

    # ---- Donado: a cream dog - floppy ears, a muzzle with a black nose, a patched grey shirt, a little tail
    c = legs('dl_don_fur', 'dl_don_fur') + torso('dl_don_shirt') + arms('dl_don_shirt', 'dl_don_fur') + head('dl_don_fur', 'dl_don_face')
    c += [e((6.0, 10.4, 3.4), (10.0, 12.8, 4.6), 'dl_don_muzzle'), e((7.2, 12.2, 3.3), (8.8, 13.2, 3.5), 'dl_don_dark'),
          e((3.0, 12.4, 6.0), (4.2, 17.0, 9.6), 'dl_don_ear'), e((11.8, 12.4, 6.0), (13.0, 17.0, 9.6), 'dl_don_ear'),
          e((6.0, 7.4, 6.1), (7.6, 9.0, 6.3), 'dl_don_patch'), s((8.0, 4.4, 9.6), (8.6, 7.4, 12.4), 0.9, 0.9, 'dl_don_fur', UP)]
    doll('doll_don', c)

    # ---- Wilfrey: the charcoal skull with its white points of light, a steel helm, a white tabard with his gold emblem, his sword
    c = legs('dl_wil_steel', 'dl_wil_steel') + torso('dl_wil_tabard', 'dl_wil_steel') + arms('dl_wil_steel', 'dl_wil_bone', up=True) + head('dl_wil_bone', 'dl_wil_face')
    c += [e((7.3, 6.2, 6.1), (8.7, 8.6, 6.3), 'dl_wil_gold'), e((6.6, 6.9, 6.1), (9.4, 7.9, 6.3), 'dl_wil_gold'),
          e((3.7, 15.0, 4.2), (12.3, 18.2, 11.8), 'dl_wil_steel'), e((3.6, 10.6, 8.4), (12.4, 15.2, 11.9), 'dl_wil_steel', sh=(0.4, 0.4)),
          e((7.6, 18.0, 6.0), (8.4, 19.4, 10.4), 'dl_wil_tabard')]
    c += [e((11.4, 12.8, 7.6), (12.2, 13.4, 8.4), 'dl_wil_gold'), e((10.6, 13.4, 7.7), (13.0, 13.9, 8.3), 'dl_wil_gold'),
          e((11.5, 13.9, 7.75), (12.1, 21.6, 8.25), 'dl_wil_blade')]
    doll('doll_wil', c)

    # ---- the Frog with Mustache: a wide green head with two big eyes on top, a curled moustache, a red bow tie and a gold pin
    c = legs('dl_fr_skin', 'dl_fr_skin') + torso('dl_fr_skin', 'dl_fr_belly') + arms('dl_fr_skin', 'dl_fr_skin') + \
        [e((6.0, 4.0, 6.1), (10.0, 9.4, 6.3), 'dl_fr_belly')] + head('dl_fr_skin', 'dl_fr_face', y0=10.2, y1=15.6, w=4.6)
    c += [e((3.8, 15.0, 5.4), (7.0, 18.2, 8.6), 'dl_fr_skin'), e((9.0, 15.0, 5.4), (12.2, 18.2, 8.6), 'dl_fr_skin'),
          e((4.3, 15.6, 5.3), (6.5, 17.8, 5.4), 'dl_fr_eye', faces=('north',)), e((9.5, 15.6, 5.3), (11.7, 17.8, 5.4), 'dl_fr_eye', faces=('north',)),
          s((8.0, 12.4, 4.3), (5.6, 12.0, 4.3), 0.7, 0.5, 'dl_fr_stache'), s((5.6, 12.0, 4.3), (4.8, 12.8, 4.3), 0.6, 0.45, 'dl_fr_stache'),
          s((8.0, 12.4, 4.3), (10.4, 12.0, 4.3), 0.7, 0.5, 'dl_fr_stache'), s((10.4, 12.0, 4.3), (11.2, 12.8, 4.3), 0.6, 0.45, 'dl_fr_stache'),
          e((6.2, 9.4, 5.9), (7.8, 10.6, 6.3), 'dl_fr_bow'), e((8.2, 9.4, 5.9), (9.8, 10.6, 6.3), 'dl_fr_bow'), e((7.6, 9.6, 5.8), (8.4, 10.4, 6.2), 'dl_fr_gold')]
    doll('doll_frog', c)
    return M
