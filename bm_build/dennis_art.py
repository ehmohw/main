"""Dennis (2.80d): the Black Market's dwarf - from the owner's art. Short and broad: a black horned helmet with a gold riveted
band, a white skull on its front and a gold spike on top; black wrap-round sunglasses; a great black beard with a grey-tipped
goatee and a curled moustache; a gold earring; an open dark-grey leather jacket over a red tee (a little gold cross on a
chain); rolled blue jeans and big brown boots. He carries his Dwarven wrench in his right hand, its head by his fist and its
handle down to his boots.

A rigkit rig like Fishy's: body, head (its face a model of its own per expression), the arms bent at the elbow, the legs, and
the wrench (on his right forearm). Design units: feet at y=0, facing -z, his right is +x."""
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, seg, chain, I

PREFIX = 'dw_'
RIG_SCALE = 1.0
PIVOT = {'body': (0, 7.0, 0), 'legr': (2.3, 7.0, 0), 'legl': (-2.3, 7.0, 0), 'head': (0, 15.8, 0),
         'armr': (5.4, 14.6, 0), 'forer': (6.0, 10.8, 0), 'arml': (-5.4, 14.6, 0), 'forel': (-6.0, 10.8, 0),
         'wrench': (6.2, 6.6, -0.3)}
PARENT = {'body': None, 'legr': None, 'legl': None, 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'wrench': 'forer'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('grin', 'shout', 'hurt')
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)


def HIDDEN(p, pose):
    return p == 'wrench' and pose.get('_nowrench', False)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _denim(seed, base='#5f70b8', lt='#8796d6'):
    im = _noise(base, seed, 6); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for x in range(0, 64, 3):
        d.line((x, 0, x + 6, 63), fill=hexc(lt)[:3] + (90,))
    for _ in range(40):
        x, y = rnd.randrange(64), rnd.randrange(64); im.putpixel((x, y), hexc('#4a5aa0'))
    return im


def _leather(seed, base='#3e4246', lt='#6a7076', dk='#26282c'):
    im = _shine(base, lt, seed); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(6):                                     # creases
        x, y = rnd.randrange(64), rnd.randrange(64)
        d.line((x, y, x + rnd.randint(-8, 8), y + rnd.randint(6, 16)), fill=hexc(dk))
    return im


def _beard(seed):
    im = _noise('#151516', seed, 5); rnd = random.Random(seed)
    for _ in range(120):
        x, y = rnd.randrange(64), rnd.randrange(64); im.putpixel((x, y), hexc(rnd.choice(['#3a3a3e', '#2a2a2c', '#5a5a5e'])))
    for x in range(0, 64, 4):
        for y in range(rnd.randrange(4), 64, 7):
            im.putpixel((x, y), hexc('#2e2e32'))
    return im


def _glass(seed):
    im = _shine('#0b0b0f', '#2a2a36', seed); d = ImageDraw.Draw(im)
    for x0 in (14, 40):                                     # the art's "S" glint on each lens
        d.arc((x0, 14, x0 + 10, 26), 200, 360, fill=hexc('#e8e8f0'), width=3)
        d.arc((x0, 24, x0 + 10, 36), 20, 180, fill=hexc('#e8e8f0'), width=3)
    return im


def _skull():
    im = Image.new('RGBA', (16, 16), hexc('#1c1c20')); d = ImageDraw.Draw(im)
    d.ellipse((3, 1, 12, 10), fill=hexc('#f2f2f2')); d.rectangle((5, 9, 10, 13), fill=hexc('#f2f2f2'))
    d.rectangle((4, 5, 6, 7), fill=hexc('#1c1c20')); d.rectangle((9, 5, 11, 7), fill=hexc('#1c1c20'))
    d.point((7, 8), fill=hexc('#1c1c20')); d.point((8, 8), fill=hexc('#1c1c20'))
    for x in (6, 8, 10): d.line((x, 11, x, 13), fill=hexc('#9a9a9a'))
    return im


def _band(seed):
    im = _shine('#d6ac2e', '#fff0a0', seed); d = ImageDraw.Draw(im)
    for x in range(4, 64, 12):                              # its rivets
        d.ellipse((x, 22, x + 7, 40), fill=hexc('#8a6418'), outline=hexc('#4a3408'))
        d.ellipse((x + 2, 25, x + 4, 30), fill=hexc('#e8c060'))
    d.line((0, 2, 63, 2), fill=hexc('#fff4c0')); d.line((0, 61, 63, 61), fill=hexc('#7a5810'))
    return im


def _helm(seed):
    im = _shine('#1e1e22', '#4a4a52', seed); d = ImageDraw.Draw(im)
    for x in (15, 47):                                      # its seams
        d.line((x, 0, x, 63), fill=hexc('#55555e'), width=2)
    return im


def _mouth(kind):
    im = Image.new('RGBA', (16, 16), hexc('#151516')); d = ImageDraw.Draw(im)
    if kind == 'grin':
        d.rectangle((1, 4, 14, 11), fill=hexc('#3a1410')); d.rectangle((2, 4, 13, 7), fill=hexc('#f4f0e4'))
    elif kind == 'shout':
        d.ellipse((3, 1, 12, 15), fill=hexc('#3a1410')); d.rectangle((4, 1, 11, 4), fill=hexc('#f4f0e4'))
    elif kind == 'hurt':
        d.line((1, 10, 5, 6), fill=hexc('#3a1410'), width=2); d.line((5, 6, 10, 10), fill=hexc('#3a1410'), width=2)
        d.line((10, 10, 14, 6), fill=hexc('#3a1410'), width=2)
    else:
        d.rectangle((2, 6, 13, 10), fill=hexc('#3a1410'))
    return im


def textures():
    return {'dw_skin': _noise('#e6b284', 1301, 6), 'dw_skin_dk': _noise('#c98f62', 1302, 5), 'dw_jacket': _leather(1303),
            'dw_jacket_dk': _leather(1304, '#2a2c30', '#4a4e54', '#18181a'), 'dw_cuff': _noise('#18181a', 1305, 3),
            'dw_shirt': _noise('#9e3a4a', 1306, 6), 'dw_denim': _denim(1307), 'dw_denim_lt': _denim(1308, '#8494d4', '#a8b4ea'),
            'dw_boot': _shine('#6e4024', '#a06a3c', 1309), 'dw_boot_dk': _shine('#3e2210', '#6a4022', 1310), 'dw_beard': _beard(1311),
            'dw_grey': _noise('#6a6a6e', 1312, 6), 'dw_glass': _glass(1313), 'dw_frame': _noise('#101012', 1314, 2),
            'dw_helm': _helm(1315), 'dw_band': _band(1316), 'dw_gold': _shine('#d8b030', '#fff0a0', 1317), 'dw_horn': _shine('#e2d8bc', '#fffaf0', 1318),
            'dw_horn_dk': _shine('#bfb294', '#e6dcc0', 1319), 'dw_skull': _skull(), 'dw_steel': _shine('#9aa2b4', '#e4eaf4', 1320),
            'dw_steel_dk': _shine('#6a7286', '#a4acbe', 1321), 'dw_collar': _noise('#b04a5a', 1322, 5),
            'dw_mouth': _mouth(None), 'dw_mouth_grin': _mouth('grin'), 'dw_mouth_shout': _mouth('shout'), 'dw_mouth_hurt': _mouth('hurt')}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: rolled jeans at the hips, the red tee, the open leather jacket (its popped collar), the cross on its chain
    pv = PIVOT['body']
    body = [el((-4.0, 6.4, -2.3), (4.0, 8.6, 2.3), 'dw_denim', pv),
            el((-3.7, 8.0, -2.9), (3.7, 15.4, 2.6), 'dw_shirt', pv),
            el((0.9, 7.4, -3.3), (5.2, 15.8, 3.0), 'dw_jacket', pv, shift=(0.2, 0.1)),         # his right front panel
            el((-5.2, 7.4, -3.3), (-0.9, 15.8, 3.0), 'dw_jacket', pv, shift=(0.6, 0.3)),       # his left
            el((-5.2, 7.4, 1.9), (5.2, 15.8, 3.2), 'dw_jacket_dk', pv),                        # the back
            el((-5.0, 15.2, -1.4), (5.0, 16.8, 3.0), 'dw_jacket_dk', pv, shift=(0.4, 0.5)),    # the collar, popped
            el((-5.3, 7.1, -3.4), (5.3, 7.7, 3.3), 'dw_cuff', pv),                             # its hem
            el((1.0, 9.0, -3.45), (1.6, 15.2, -3.25), 'dw_jacket_dk', pv),                     # lapel edges
            el((-1.6, 9.0, -3.45), (-1.0, 15.2, -3.25), 'dw_jacket_dk', pv),
            el((-1.0, 13.4, -2.95), (1.0, 15.2, -2.85), 'dw_collar', pv)]                      # the tee's neckline
    body += chain([(-1.4, 15.0, -2.95), (0.0, 12.6, -3.0), (1.4, 15.0, -2.95)], [0.12, 0.12], 0.08, 'dw_gold', pv, FRONT, ext=0.04)
    body += [el((-0.1, 11.2, -3.06), (0.1, 12.6, -2.98), 'dw_gold', pv), el((-0.45, 11.9, -3.06), (0.45, 12.1, -2.98), 'dw_gold', pv)]
    part('dw_body', body)

    # ---- the head: the face (its mouth per expression), the shades, the beard, the hair at the back, the earring; the helmet
    #      with its riveted gold band, its skull, its spike, and the two great curling horns
    pv = PIVOT['head']
    def head(face=None):
        h = [el((-1.8, 15.2, -1.6), (1.8, 16.6, 1.6), 'dw_skin_dk', pv),
             el((-3.2, 16.2, -3.2), (3.2, 22.4, 3.0), 'dw_skin', pv),
             el((-3.4, 17.0, 0.4), (3.4, 22.2, 3.3), 'dw_beard', pv, shift=(0.3, 0.2)),           # his hair, long at the back
             el((-3.45, 17.6, -1.2), (-3.0, 21.8, 3.2), 'dw_beard', pv), el((3.0, 17.6, -1.2), (3.45, 21.8, 3.2), 'dw_beard', pv),
             el((-3.4, 13.4, -4.1), (3.4, 19.4, -1.8), 'dw_beard', pv, shift=(0.1, 0.6)),         # the beard, down over his chest
             el((-3.55, 16.8, -3.4), (-2.9, 20.4, 0.2), 'dw_beard', pv), el((2.9, 16.8, -3.4), (3.55, 20.4, 0.2), 'dw_beard', pv),
             el((-2.4, 11.8, -4.0), (2.4, 13.6, -2.4), 'dw_beard', pv, shift=(0.5, 0.2)),
             el((-0.8, 10.8, -4.15), (0.8, 12.2, -3.6), 'dw_grey', pv),                           # the goatee's grey tip
             el((-0.6, 19.6, -3.95), (0.6, 20.7, -3.2), 'dw_skin_dk', pv),                        # the nose
             el((-1.0, 18.25, -4.16), (1.0, 18.95, -4.1), {None: 'dw_mouth', 'grin': 'dw_mouth_grin', 'shout': 'dw_mouth_shout',
                                                             'hurt': 'dw_mouth_hurt'}[face], pv, faces=('north',), uv={'north': [0, 0, 16, 16]})]
        h += chain([(-2.4, 19.6, -4.15), (-1.0, 19.2, -4.25), (0.0, 19.35, -4.25)], [0.6, 0.5], 0.45, 'dw_grey', pv, FRONT, ext=0.08)    # the moustache
        h += chain([(2.4, 19.6, -4.15), (1.0, 19.2, -4.25), (0.0, 19.35, -4.25)], [0.6, 0.5], 0.45, 'dw_grey', pv, FRONT, ext=0.08)
        gy = 0.25 if face == 'shout' else 0.0                                                     # (a shout: the shades jump)
        h += [el((-2.9, 20.2 + gy, -3.5), (-0.45, 21.5 + gy, -3.25), 'dw_glass', pv), el((0.45, 20.2 + gy, -3.5), (2.9, 21.5 + gy, -3.25), 'dw_glass', pv, shift=(0.5, 0)),
              el((-0.5, 20.85 + gy, -3.5), (0.5, 21.15 + gy, -3.3), 'dw_frame', pv),
              el((-3.3, 20.9 + gy, -3.3), (-3.15, 21.2 + gy, -0.2), 'dw_frame', pv), el((3.15, 20.9 + gy, -3.3), (3.3, 21.2 + gy, -0.2), 'dw_frame', pv),
              el((-3.42, 18.6, -0.3), (-3.22, 19.5, 0.3), 'dw_gold', pv)]                                       # the earring
        # the helmet
        h += [el((-3.65, 21.4, -3.65), (3.65, 22.55, 3.45), 'dw_band', pv),
              el((-3.4, 22.4, -3.4), (3.4, 24.6, 3.2), 'dw_helm', pv), el((-2.7, 24.5, -2.7), (2.7, 25.6, 2.5), 'dw_helm', pv, shift=(0.3, 0.4)),
              el((-1.6, 25.5, -1.6), (1.6, 26.15, 1.4), 'dw_helm', pv, shift=(0.6, 0.2)),
              el((-1.1, 22.7, -3.52), (1.1, 24.5, -3.42), 'dw_skull', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
              el((-0.45, 26.0, -0.45), (0.45, 26.9, 0.35), 'dw_gold', pv), el((-0.25, 26.8, -0.25), (0.25, 27.6, 0.15), 'dw_gold', pv)]
        for sx in (1, -1):
            h += chain([(sx * 3.3, 23.4, 0), (sx * 5.3, 24.4, -0.2), (sx * 6.5, 26.3, -0.3), (sx * 6.9, 28.6, -0.3), (sx * 6.3, 30.4, -0.2)],
                       (1.7, 0.5), 1.5, 'dw_horn', pv, FRONT, hs=[1.6, 1.3, 1.0, 0.7])
            h.append(el((sx * 3.3 - 0.75, 22.8, -0.8), (sx * 3.3 + 0.75, 24.2, 0.8), 'dw_horn_dk', pv))           # (their roots)
        return h
    part('dw_head', head())
    for fc in FACES:
        part(f'dw_head_x{fc}', head(fc))

    # ---- the arms: jacket sleeves, black cuffs, big hands (a gold ring on his right)
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        a = [el((x0 - 1.7, y0 - 1.6, -1.8), (x0 + 1.7, y0 + 1.3, 1.8), 'dw_jacket', pv, shift=(0.4, 0.2))]          # the shoulder
        a += chain([(x0, y0, 0), (sx * 6.0, 10.8, 0)], [3.1], 3.1, 'dw_jacket', pv, FRONT, ext=0.3)
        return a
    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 6.2, 7.8
        a = chain([(ex, ey, 0), (wx, wy, 0)], [2.9], 2.9, 'dw_jacket', pv, FRONT, ext=0.25)
        a += [el((wx - 1.55, wy - 0.3, -1.55), (wx + 1.55, wy + 0.6, 1.55), 'dw_cuff', pv),
              el((wx - 1.25, wy - 2.3, -1.3), (wx + 1.25, wy - 0.2, 1.2), 'dw_skin', pv),                               # the fist
              el((wx - 1.0, wy - 2.55, -1.4), (wx + 1.0, wy - 1.9, -0.9), 'dw_skin_dk', pv)]                            # knuckles
        if sx > 0:
            a.append(el((wx - 1.3, wy - 1.7, -1.35), (wx - 1.15, wy - 1.3, -0.7), 'dw_gold', pv))
        return a
    part('dw_armr', upper(1)); part('dw_arml', upper(-1)); part('dw_forer', lower(1)); part('dw_forel', lower(-1))

    # ---- the legs: rolled jeans, big round-toed brown boots
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 1.75, 2.2, -1.55), (cx + 1.75, 7.4, 1.55), 'dw_denim', pv, shift=(0.3 if sx > 0 else 0.7, 0.2)),
                el((cx - 1.9, 2.1, -1.7), (cx + 1.9, 3.0, 1.7), 'dw_denim_lt', pv),                                  # the roll-up
                el((cx - 1.95, 0.0, -3.4), (cx + 1.95, 2.3, 1.9), 'dw_boot', pv),
                el((cx - 1.75, 0.0, -4.3), (cx + 1.75, 1.9, -3.2), 'dw_boot', pv, shift=(0.5, 0.5)),                  # the round toe
                el((cx - 2.0, 0.0, -4.4), (cx + 2.0, 0.4, 2.0), 'dw_boot_dk', pv)]                                    # the sole
    part('dw_legr', leg(1)); part('dw_legl', leg(-1))

    # ---- the Dwarven wrench: an adjustable spanner as long as he is tall - its jaws by his fist, a red collar, the handle down
    #      to his boots (thin across, broad front to back)
    pv = PIVOT['wrench']; x = 6.2
    w = [el((x - 0.42, 0.7, -1.0), (x + 0.42, 4.7, 0.3), 'dw_steel', pv),                   # the handle
         el((x - 0.52, 0.3, -1.15), (x + 0.52, 1.1, 0.45), 'dw_steel_dk', pv),               # its end
         el((x - 0.62, 4.6, -1.25), (x + 0.62, 5.4, 0.55), 'dw_collar', pv),                 # the red collar, under his fist
         el((x - 0.42, 5.3, -1.0), (x + 0.42, 7.4, 0.3), 'dw_steel', pv, shift=(0.5, 0.3)),  # (in his fist)
         el((x - 0.5, 5.6, -2.6), (x + 0.5, 6.4, -1.0), 'dw_steel', pv, shift=(0.2, 0.6)),   # the head, out in front of his fist
         el((x - 0.5, 6.4, -3.6), (x + 0.5, 7.4, -2.4), 'dw_steel', pv, shift=(0.7, 0.1)),   # the fixed jaw
         el((x - 0.5, 4.4, -3.6), (x + 0.5, 5.6, -2.4), 'dw_steel_dk', pv),                  # the sliding jaw
         el((x - 0.55, 5.6, -2.5), (x + 0.55, 6.4, -1.7), 'dw_steel_dk', pv)]                # the thumbscrew
    part('dw_wrench', w)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


POSES = {
    'idle_a': P(armr=limb(1, 4, 4), forer=limb(1, 8), arml=limb(-1, -6, 6), forel=limb(-1, 30), head=qs(('y', 6))),
    'idle_b': P(_off=(0, -0.12, 0), armr=limb(1, 2, 5), forer=limb(1, 12), arml=limb(-1, -8, 7), forel=limb(-1, 34), head=qs(('y', -8), ('x', 3))),
    'walk_a': P(_off=(0, 0.2, 0), body=qs(('z', 3)), legr=limb(1, 26), legl=limb(-1, -24), armr=limb(1, -14, 4), arml=limb(-1, 20, 4),
                forer=limb(1, 10), forel=limb(-1, 24), head=qs(('z', -2))),
    'walk_b': P(_off=(0, 0.2, 0), body=qs(('z', -3)), legr=limb(1, -24), legl=limb(-1, 26), armr=limb(1, 16, 4), arml=limb(-1, -18, 4),
                forer=limb(1, 16), forel=limb(-1, 18), head=qs(('z', 2))),
    'wave_a': P(_face='grin', armr=limb(1, 4, 6), forer=limb(1, 10), arml=limb(-1, 10, 120), forel=limb(-1, 40), head=qs(('y', -8))),
    'wave_b': P(_face='grin', armr=limb(1, 4, 6), forer=limb(1, 10), arml=limb(-1, 10, 134), forel=limb(-1, 14), head=qs(('y', -4), ('z', 4))),
    'bow': P(_off=(0, -0.5, 0), body=qs(('x', 16)), head=qs(('x', 10)), legr=limb(1, -12), legl=limb(-1, -12), armr=limb(1, 10, 4), forer=limb(1, 20),
             arml=limb(-1, 30, -10), forel=limb(-1, 70)),
    'point': P(_face='grin', armr=limb(1, 4, 6), forer=limb(1, 8), arml=limb(-1, 84, 6), forel=limb(-1, 4), head=qs(('y', -14))),
    'shock': P(_face='shout', _off=(0, 0.4, 0), armr=limb(1, 26, 34), forer=limb(1, 50), arml=limb(-1, 26, 34), forel=limb(-1, 50), head=qs(('x', -8))),
    'sit': P(_off=(0, -4.6, 0), legr=limb(1, 84, 8), legl=limb(-1, 84, 8), armr=limb(1, 26, 8), forer=limb(1, 46), arml=limb(-1, 26, 8), forel=limb(-1, 50),
             head=qs(('y', 8))),
    'tired': P(_face='hurt', _off=(0, -0.8, 0), body=qs(('x', 10), ('z', -4)), head=qs(('x', 16)), armr=limb(1, 0, 2), arml=limb(-1, 0, 2),
               forer=limb(1, 4), forel=limb(-1, 4), legr=limb(1, 6, 4), legl=limb(-1, -4, 4))}
DRAFT = ['idle_a', 'walk_a', 'wave_a', 'bow', 'point', 'shock', 'sit', 'tired']
