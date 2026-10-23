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
from rigkit import qs, el, chain

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
BAND_UV = {f: [0, 0, 16, 4] for f in ('north', 'south', 'east', 'west')}       # (the band's strip, the whole way round)
LENS_UV = {'north': [0, 0, 16, 8]}                                                  # (a lens shows its whole glint)


def HIDDEN(p, pose):
    return p == 'wrench' and pose.get('_nowrench', False)


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
# (2.90 rework: drawn as 32 x 32 pixel art - every texel placed on purpose, a lit top edge and a shaded bottom, seams and
#  stitching - then doubled to the pack's 64 x 64, so he reads as crisp blocks rather than speckled noise)
def _sheet(base, seed, var=0, n=32):
    rnd = random.Random(seed); b = hexc(base)[:3]; im = Image.new('RGBA', (n, n))
    for y in range(n):
        for x in range(n):
            d = rnd.choice((0, 0, 0, var, -var)) if var else 0
            im.putpixel((x, y), tuple(max(0, min(255, v + d)) for v in b) + (255,))
    return im


def _up(im):
    return im.resize((64, 64), Image.NEAREST)


def _edge(im, lt, dk, top=1, bot=1):
    """a lit top row and a shaded bottom row (every box catches the light from above)"""
    d = ImageDraw.Draw(im); w, h = im.size
    for i in range(top): d.line((0, i, w - 1, i), fill=hexc(lt))
    for i in range(bot): d.line((0, h - 1 - i, w - 1, h - 1 - i), fill=hexc(dk))
    return im


def _denim(seed, base='#5468b0', lt='#6276bc', dk='#3c4c8c'):
    im = _sheet(base, seed, 4); d = ImageDraw.Draw(im)
    px = im.load()
    for y in range(32):                                         # the twill: faint diagonal ribs
        for x in range(32):
            if (x + y) % 3 == 0: px[x, y] = hexc(lt)[:3] + (255,) if (x * 7 + y) % 5 else px[x, y]
    d.line((15, 0, 15, 31), fill=hexc(dk)); d.line((16, 0, 16, 31), fill=hexc('#c88a3a'))      # the side seam, orange stitch
    for y in range(1, 32, 3): d.point((16, y), fill=hexc(dk))
    return _up(_edge(im, lt, dk))


def _cuffroll(seed):
    im = _sheet('#8a9ad8', seed, 3); d = ImageDraw.Draw(im)
    for y in (6, 14, 22): d.line((0, y, 31, y), fill=hexc('#6878bc'))
    return _up(_edge(im, '#b4c0ee', '#5464a8'))


def _leather(seed, base='#3c4046', lt='#5c626a', dk='#25282c', hi='#727a84'):
    im = _sheet(base, seed, 2); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(5):                                          # creases: a dark line with a lit pixel beside it
        x, y = rnd.randrange(2, 30), rnd.randrange(4, 26)
        L = rnd.randint(3, 6)
        d.line((x, y, x + 1, y + L), fill=hexc(dk)); d.point((x + 1, y), fill=hexc(hi))
    for y in range(2, 32, 2): d.point((1, y), fill=hexc(lt)); d.point((30, y), fill=hexc(lt))   # the stitching down each edge
    return _up(_edge(im, hi, dk))


def _cuff(seed):
    im = _sheet('#1a1a1e', seed, 2); d = ImageDraw.Draw(im)
    for x in range(1, 32, 4): d.line((x, 10, x, 21), fill=hexc('#2c2c32'))          # ribbing
    return _up(_edge(im, '#34343a', '#0c0c0e'))


def _tee(seed):
    im = _sheet('#a83a48', seed, 3); d = ImageDraw.Draw(im)
    for x in (8, 22): d.line((x, 4, x - 1, 31), fill=hexc('#8a2c3a'))                # two soft folds
    d.line((9, 4, 8, 31), fill=hexc('#c25060'))
    return _up(_edge(im, '#c85a6a', '#7a2432'))


def _beard(seed, base='#17171a'):
    """a black beard as pixel strands: long dark-grey locks running down, a few lit tips, never salt-and-pepper"""
    im = _sheet(base, seed, 0); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for x in range(0, 32, 3):
        x0 = x + rnd.randint(0, 1); y0 = rnd.randint(0, 6)
        d.line((x0, y0, x0, y0 + rnd.randint(8, 18)), fill=hexc('#2a2a30'))
        d.point((x0, y0), fill=hexc('#3c3c44'))
    for _ in range(10):
        x, y = rnd.randrange(32), rnd.randrange(32); d.line((x, y, x, y + 2), fill=hexc('#0a0a0c'))
    return _up(_edge(im, '#34343c', '#0a0a0c'))


def _grey(seed):
    im = _sheet('#8a8a90', seed, 0); d = ImageDraw.Draw(im)
    for x in range(1, 32, 3): d.line((x, 0, x, 31), fill=hexc('#a6a6ac'))
    for x in range(2, 32, 3): d.line((x, 6, x, 31), fill=hexc('#6c6c72'))
    return _up(_edge(im, '#c0c0c6', '#55555a'))


def _skin(seed, base='#e6b284', dk='#c8905e'):
    im = _sheet(base, seed, 3)
    return _up(_edge(im, '#f2c69c', dk))


def _glass(seed):
    """a lens: black glass, a lit rim along the top, a white glint slashed across it - drawn in the top half (uv [0, 0, 16, 8])"""
    im = _sheet('#0c0c12', seed, 0, 64); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 63, 2), fill=hexc('#34344a'))
    w, w2 = hexc('#e8e8f0'), hexc('#7a7a90')
    for k in range(4):                                          # the glint: a bold diagonal shine and a thin one beside it
        d.rectangle((14 + 3 * k, 22 - 4 * k, 18 + 3 * k, 25 - 4 * k), fill=w)
        d.rectangle((26 + 2 * k, 24 - 4 * k, 27 + 2 * k, 27 - 4 * k), fill=w2)
    return im


def _skull():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((4, 2, 11, 9), fill=hexc('#f2f2f2')); d.rectangle((3, 3, 12, 8), fill=hexc('#f2f2f2'))
    d.rectangle((5, 10, 10, 12), fill=hexc('#f2f2f2'))
    d.rectangle((4, 5, 6, 7), fill=hexc('#1c1c20')); d.rectangle((9, 5, 11, 7), fill=hexc('#1c1c20'))
    d.point((7, 8), fill=hexc('#1c1c20')); d.point((8, 8), fill=hexc('#1c1c20'))
    for x in (6, 8): d.line((x, 11, x, 12), fill=hexc('#8a8a8a'))
    d.line((4, 2, 11, 2), fill=hexc('#ffffff'))
    return im


def _band(seed):
    """the riveted gold band: a 64 x 16 strip (shown through uv [0, 0, 16, 4] - the band is long and thin), four times down"""
    strip = Image.new('RGBA', (64, 16)); d = ImageDraw.Draw(strip); rnd = random.Random(seed)
    for y in range(16):
        for x in range(64):
            v = rnd.choice((0, 0, 6, -6)); b = hexc('#d6ac2e')[:3]
            strip.putpixel((x, y), tuple(max(0, min(255, c + v)) for c in b) + (255,))
    d.rectangle((0, 0, 63, 1), fill=hexc('#fff0a0')); d.rectangle((0, 14, 63, 15), fill=hexc('#8a6614'))
    for x in range(3, 64, 10):                                  # its rivets: domed studs, lit top-left
        d.rectangle((x, 4, x + 4, 11), fill=hexc('#9a7420')); d.rectangle((x + 1, 5, x + 3, 10), fill=hexc('#c89a30'))
        d.rectangle((x + 1, 5, x + 2, 6), fill=hexc('#fff4c0')); d.line((x, 11, x + 4, 11), fill=hexc('#5a4008'))
    im = Image.new('RGBA', (64, 64))
    for k in range(4): im.paste(strip, (0, 16 * k))
    return im


def _helm(seed):
    im = _sheet('#202026', seed, 2); d = ImageDraw.Draw(im)
    d.line((0, 0, 31, 0), fill=hexc('#55555f')); d.line((0, 1, 31, 1), fill=hexc('#3a3a42'))
    for x in (7, 23):                                           # its plate seams, riveted
        d.line((x, 0, x, 31), fill=hexc('#0e0e12')); d.line((x + 1, 0, x + 1, 31), fill=hexc('#3a3a44'))
        for y in range(4, 32, 7): d.point((x + 1, y), fill=hexc('#8a8a96'))
    d.line((0, 31, 31, 31), fill=hexc('#0e0e12'))
    return _up(im)


def _horn(seed, base='#e4d8b6', lt='#fff8e4', dk='#b8a882', tip=False):
    """horn: chunky growth rings, lit on top; the tip darkens to a weathered brown"""
    im = _sheet(base if not tip else '#a8916a', seed, 2); d = ImageDraw.Draw(im)
    for y in range(0, 32, 5):
        d.line((0, y, 31, y), fill=hexc(dk if not tip else '#7a6648'))
        d.line((0, y + 1, 31, y + 1), fill=hexc(lt if not tip else '#c8b088'))
    return _up(im)


def _boot(seed, base='#734426', lt='#a0683c', dk='#4a2a14'):
    im = _sheet(base, seed, 3); d = ImageDraw.Draw(im)
    for y in range(4, 30, 4):                                   # laces up the front
        d.line((12, y, 19, y + 2), fill=hexc('#e2d0a8')); d.line((19, y, 12, y + 2), fill=hexc('#c2ae88'))
    d.line((0, 28, 31, 28), fill=hexc(dk))
    return _up(_edge(im, lt, dk, 2, 1))


def _sole(seed):
    im = _sheet('#3a2210', seed, 2); d = ImageDraw.Draw(im)
    for x in range(0, 32, 4): d.line((x, 0, x, 31), fill=hexc('#26160a'))
    return _up(im)


def _steel(seed, base='#a0a8b8', lt='#e6ecf6', dk='#6a7286'):
    im = _sheet(base, seed, 2); d = ImageDraw.Draw(im)
    d.line((3, 0, 3, 31), fill=hexc(lt)); d.line((4, 0, 4, 31), fill=hexc(lt)); d.line((27, 0, 27, 31), fill=hexc(dk))
    return _up(_edge(im, lt, dk))


def _gold(seed):
    im = _sheet('#d8b030', seed, 3); d = ImageDraw.Draw(im)
    d.line((2, 2, 8, 2), fill=hexc('#fff0a0')); d.line((2, 3, 2, 8), fill=hexc('#fff0a0'))
    return _up(_edge(im, '#ffe880', '#8a6a10'))


def _mouth(kind):
    im = Image.new('RGBA', (16, 16), hexc('#17171a')); d = ImageDraw.Draw(im)
    if kind == 'grin':
        d.rectangle((1, 4, 14, 11), fill=hexc('#3a1410')); d.rectangle((2, 4, 13, 7), fill=hexc('#f4f0e4'))
        for x in (5, 8, 11): d.line((x, 4, x, 7), fill=hexc('#c8c0b0'))
    elif kind == 'shout':
        d.rectangle((3, 1, 12, 15), fill=hexc('#3a1410')); d.rectangle((4, 1, 11, 4), fill=hexc('#f4f0e4'))
        d.rectangle((5, 11, 10, 14), fill=hexc('#a83a48'))
    elif kind == 'hurt':
        d.line((1, 10, 5, 6), fill=hexc('#3a1410'), width=2); d.line((5, 6, 10, 10), fill=hexc('#3a1410'), width=2)
        d.line((10, 10, 14, 6), fill=hexc('#3a1410'), width=2)
    else:
        d.rectangle((2, 6, 13, 10), fill=hexc('#3a1410')); d.line((3, 6, 12, 6), fill=hexc('#f4f0e4'))
    return im


def textures():
    return {'dw_skin': _skin(1301), 'dw_skin_dk': _skin(1302, '#c98f62', '#a8703e'), 'dw_jacket': _leather(1303),
            'dw_jacket_dk': _leather(1304, '#2a2c31', '#454a52', '#17181b', '#585e68'), 'dw_cuff': _cuff(1305),
            'dw_shirt': _tee(1306), 'dw_denim': _denim(1307), 'dw_denim_lt': _cuffroll(1308),
            'dw_boot': _boot(1309), 'dw_boot_dk': _sole(1310), 'dw_beard': _beard(1311),
            'dw_grey': _grey(1312), 'dw_glass': _glass(1313), 'dw_frame': _up(_sheet('#101012', 1314)),
            'dw_helm': _helm(1315), 'dw_band': _band(1316), 'dw_gold': _gold(1317), 'dw_horn': _horn(1318),
            'dw_horn_dk': _horn(1319, tip=True), 'dw_skull': _skull(), 'dw_steel': _steel(1320),
            'dw_steel_dk': _steel(1321, '#6a7286', '#a4acbe', '#4a5264'), 'dw_collar': _up(_edge(_sheet('#b8404e', 1322, 3), '#d8606e', '#80242e')),
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
             el((-3.4, 14.6, -4.1), (3.4, 19.4, -1.8), 'dw_beard', pv, shift=(0.1, 0.6)),         # the beard, a square block over his chest
             el((-3.55, 16.8, -3.4), (-2.9, 20.4, 0.2), 'dw_beard', pv), el((2.9, 16.8, -3.4), (3.55, 20.4, 0.2), 'dw_beard', pv),
             el((-2.8, 12.8, -4.0), (2.8, 14.8, -2.0), 'dw_beard', pv, shift=(0.5, 0.2)),         # stepping in toward its point
             el((-1.8, 11.6, -3.95), (1.8, 13.0, -2.3), 'dw_beard', pv, shift=(0.8, 0.4)),
             el((-1.0, 10.6, -3.9), (1.0, 11.8, -2.6), 'dw_grey', pv),                            # the goatee's grey tip
             el((-0.6, 19.6, -3.95), (0.6, 20.7, -3.2), 'dw_skin_dk', pv),                        # the nose
             el((-1.0, 18.25, -4.16), (1.0, 18.95, -4.1), {None: 'dw_mouth', 'grin': 'dw_mouth_grin', 'shout': 'dw_mouth_shout',
                                                             'hurt': 'dw_mouth_hurt'}[face], pv, faces=('north',), uv={'north': [0, 0, 16, 16]})]
        h += [el((-2.0, 18.95, -4.3), (2.0, 19.75, -3.9), 'dw_grey', pv),                                          # the moustache: a bar...
              el((-2.8, 19.3, -4.25), (-1.9, 20.2, -3.85), 'dw_grey', pv), el((1.9, 19.3, -4.25), (2.8, 20.2, -3.85), 'dw_grey', pv),
              el((-3.2, 20.0, -4.2), (-2.5, 20.6, -3.8), 'dw_grey', pv), el((2.5, 20.0, -4.2), (3.2, 20.6, -3.8), 'dw_grey', pv)]   # ...curled up at the ends
        gy = 0.25 if face == 'shout' else 0.0                                                     # (a shout: the shades jump)
        h += [el((-2.9, 20.2 + gy, -3.5), (-0.45, 21.5 + gy, -3.25), 'dw_glass', pv, uv=LENS_UV), el((0.45, 20.2 + gy, -3.5), (2.9, 21.5 + gy, -3.25), 'dw_glass', pv, uv=LENS_UV),
              el((-0.5, 20.85 + gy, -3.5), (0.5, 21.15 + gy, -3.3), 'dw_frame', pv),
              el((-3.3, 20.9 + gy, -3.3), (-3.15, 21.2 + gy, -0.2), 'dw_frame', pv), el((3.15, 20.9 + gy, -3.3), (3.3, 21.2 + gy, -0.2), 'dw_frame', pv),
              el((-3.42, 18.6, -0.3), (-3.22, 19.5, 0.3), 'dw_gold', pv)]                                       # the earring
        # the helmet
        h += [el((-3.65, 21.4, -3.65), (3.65, 22.55, 3.45), 'dw_band', pv, uv=BAND_UV),
              el((-3.4, 22.4, -3.4), (3.4, 24.6, 3.2), 'dw_helm', pv), el((-2.7, 24.5, -2.7), (2.7, 25.6, 2.5), 'dw_helm', pv, shift=(0.3, 0.4)),
              el((-1.6, 25.5, -1.6), (1.6, 26.15, 1.4), 'dw_helm', pv, shift=(0.6, 0.2)),
              el((-1.1, 22.7, -3.52), (1.1, 24.5, -3.42), 'dw_skull', pv, faces=('north',), uv={'north': [0, 0, 16, 16]}),
              el((-0.45, 26.0, -0.45), (0.45, 26.9, 0.35), 'dw_gold', pv), el((-0.25, 26.8, -0.25), (0.25, 27.6, 0.15), 'dw_gold', pv)]
        # the two great horns, block by block: out from the helmet, sweeping up, curling a little back in at the tips
        HORN = [((3.3, 5.6), (22.4, 24.8), 1.1, 'dw_horn_dk'),     # the root, a dark collar against the helmet
                ((5.3, 7.7), (23.2, 25.9), 1.0, 'dw_horn'),          # out...
                ((6.6, 8.5), (25.6, 28.7), 0.85, 'dw_horn'),         # ...and up...
                ((6.3, 7.8), (28.5, 30.7), 0.62, 'dw_horn_dk')]      # ...to a weathered tip, curling in
        for sx in (1, -1):
            for k, ((x0, x1), (y0, y1), hz, tx) in enumerate(HORN):
                a, b = sorted((sx * x0, sx * x1))
                h.append(el((a, y0, -hz - 0.15), (b, y1, hz - 0.15), tx, pv, shift=(0.3 * k, 0.17 * k)))
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
    w = [el((x - 0.55, 0.7, -1.1), (x + 0.55, 4.7, 0.4), 'dw_steel', pv),                   # the handle
         el((x - 0.68, 0.3, -1.25), (x + 0.68, 1.1, 0.55), 'dw_steel_dk', pv),               # its end
         el((x - 0.75, 4.6, -1.3), (x + 0.75, 5.4, 0.6), 'dw_collar', pv),                 # the red collar, under his fist
         el((x - 0.55, 5.3, -1.1), (x + 0.55, 7.4, 0.4), 'dw_steel', pv, shift=(0.5, 0.3)),  # (in his fist)
         el((x - 0.62, 5.6, -2.6), (x + 0.62, 6.4, -1.0), 'dw_steel', pv, shift=(0.2, 0.6)),   # the head, out in front of his fist
         el((x - 0.62, 6.4, -3.6), (x + 0.62, 7.4, -2.4), 'dw_steel', pv, shift=(0.7, 0.1)),   # the fixed jaw
         el((x - 0.62, 4.4, -3.6), (x + 0.62, 5.6, -2.4), 'dw_steel_dk', pv),                  # the sliding jaw
         el((x - 0.75, 5.75, -2.4), (x + 0.75, 6.25, -1.8), 'dw_steel_dk', pv)]                # the thumbscrew
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


# (2.93e: every material with life in it - matkit)
import matkit as _mk
textures = _mk.wrapped(textures, __name__)
