"""MOCKUP (not in the build): Celi - the blue elf in the star-patterned tunic.

Same rig kit as Emma (phase57_art): one item model per part, its joint at model (8, 8, 8). Design units: feet at y=0,
facing -z, her right is +x; drawn at RIG_SCALE.
    python3 mockups/celi_art.py <out.png>     renders a preview (front / three-quarter / side / back)
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase57_art import _cloth, _hair, _el, hexc, qa, qmul

RIG_SCALE = 0.85
PIVOT = {'body': (0, 13, 0), 'head': (0, 25, 0), 'armr': (4.7, 23.2, 0), 'arml': (-4.7, 23.2, 0), 'legr': (1.8, 13, 0), 'legl': (-1.8, 13, 0)}
PARTS = tuple(PIVOT)
SKIN, SKIN_DK = '#8ec6e8', '#6aa6d0'
HAIR = ('#c4621a', '#d47420', '#e48a2c', '#f0a23a', '#f8bc4c')


# ---------------------------------------------------------------------------------------------------- textures
def _stars(base, star, seed, dark=None):
    """the tunic cloth: soft blue, faint darker stars scattered over it, deeper toward the hem (dark=the lower colour)"""
    im = _cloth(base, seed, var=0.03); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    if dark:
        a, b = hexc(base), hexc(dark)
        for y in range(64):
            t = max(0, (y - 30) / 34)
            for x in range(64):
                p = im.getpixel((x, y))
                im.putpixel((x, y), tuple(int(p[i] * (1 - t) + b[i] * t * (p[i] / max(1, a[i]))) for i in range(3)) + (255,))
    for _ in range(26):
        cx, cy, r = rnd.randint(2, 61), rnd.randint(2, 61), rnd.choice((2.0, 2.5, 3.0))
        pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(i * math.pi / 5), cy - (r if i % 2 == 0 else r * 0.45) * math.cos(i * math.pi / 5)) for i in range(10)]
        d.polygon(pts, fill=hexc(star))
    return im


def _face():
    """36 x 32: heavy-lidded golden eyes with violet shadow, orange brows, blush, a small frown with one fang"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(SKIN)); d = ImageDraw.Draw(im)
    def eye(cx, flip):
        x0, y0 = cx - 5, 14
        d.ellipse((x0 - 1, y0 - 2, x0 + 11, y0 + 6), fill=P('#a888d8'))                 # violet eyeshadow
        d.chord((x0, y0, x0 + 10, y0 + 10), 0, 180, fill=P('#fff6c0'))                   # the lower half shows: heavy lids
        d.chord((x0 + 1, y0 + 1, x0 + 9, y0 + 9), 0, 180, fill=P('#f4c830'))
        d.chord((x0 + 3, y0 + 2, x0 + 7, y0 + 8), 0, 180, fill=P('#c88a10'))
        d.line((x0 - 1, y0 + 5, x0 + 11, y0 + 5), fill=P('#2a1a3a'), width=2)              # the lid line
        ox = x0 + 11 if not flip else x0 - 1; sx = 1 if not flip else -1
        d.line((ox, y0 + 5, ox + 2 * sx, y0 + 3), fill=P('#2a1a3a'), width=1)              # lashes flick out
        d.point((cx + (2 if not flip else -2), y0 + 7), fill=P('#ffffff'))
    eye(9, False); eye(27, True)
    for cx, s in ((9, 1), (27, -1)):                                                       # brows: orange, low, a little cross
        for dx, y in ((-4, 11), (-3, 10), (-2, 10), (-1, 10), (0, 10), (1, 10), (2, 11)): im.putpixel((cx + dx * s, y), P('#d06a20'))
    for cx in (7, 29):                                                                     # blush, with little strokes
        d.ellipse((cx - 4, 24, cx + 4, 27), fill=P('#b49ae0'))
        for fx in (-2, 0, 2): im.putpixel((cx + fx, 25), P('#d88ac8'))
    d.line((16, 28, 20, 28), fill=P('#3a2a5a'), width=1); d.point((15, 29), fill=P('#3a2a5a')); d.point((21, 29), fill=P('#3a2a5a'))   # a small frown
    d.polygon([(19, 28), (20, 28), (19.5, 30)], fill=P('#ffffff'))                       # the fang
    d.line((18, 21, 18, 24), fill=P(SKIN_DK)); d.point((19, 24), fill=P(SKIN_DK))           # nose
    return im


def _belt():
    im = _cloth('#3a3630', 41, var=0.04)
    for y in range(64):
        for x in range(64):
            if (x + 2 * (y % 8 < 4 and 1 or -1) * (y % 4)) % 6 == 0: im.putpixel((x, y), hexc('#24221e'))   # the braid
    return im


def _moon():
    """the buckle (16 x 16 texels on the sheet): a dark blue orb with a golden crescent hugging its lower left"""
    im = Image.new('RGBA', (64, 64), hexc('#3a3630')); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 15, 15), fill=hexc('#f4e078')); d.ellipse((4, 0, 16, 12), fill=hexc('#2a3a7a'))
    d.ellipse((7, 2, 11, 5), fill=hexc('#5a6ab0'))
    return im


def _boot():
    im = _cloth('#34468a', 42, var=0.03); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 9):                                                            # the cross-hatched lacing
        d.line((k, 0, k + 64, 64), fill=hexc('#26346a')); d.line((k + 64, 0, k, 64), fill=hexc('#26346a'))
    return im


def _fur(seed):
    im = _cloth('#eef0fa', seed, var=0.02); rnd = random.Random(seed)
    for _ in range(260):
        x, y = rnd.randint(0, 63), rnd.randint(0, 63); im.putpixel((x, y), hexc(rnd.choice(('#c8ccf0', '#d8dcf6', '#ffffff'))))
    for y in range(44, 64):                                                                # lavender shadow underneath
        for x in range(64):
            if rnd.random() < (y - 44) / 26: im.putpixel((x, y), hexc('#b8b4ec'))
    return im


def _star():
    im = Image.new('RGBA', (64, 64), hexc('#7fa8d8')); d = ImageDraw.Draw(im)
    pts = [(8 + (7 if i % 2 == 0 else 3) * math.sin(i * math.pi / 5), 8 - (7 if i % 2 == 0 else 3) * math.cos(i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=hexc('#f8e070')); d.point((7, 6), fill=hexc('#ffffff'))
    return im


def textures():
    T = {}
    T['ce_skin'] = _cloth(SKIN, 51, var=0.02)
    T['ce_skin_dk'] = _cloth(SKIN_DK, 52, var=0.02)
    T['ce_hair'] = _hair(53, HAIR)
    T['ce_face'] = _face()
    T['ce_tunic'] = _stars('#7fa8d8', '#6a92c8', 54)
    T['ce_skirt'] = _stars('#7aa2d4', '#6088c0', 55, dark='#5a7cc0')
    T['ce_stripe'] = _cloth('#d8dcf4', 56, var=0.02)
    T['ce_fur'] = _fur(57)
    T['ce_belt'] = _belt()
    T['ce_moon'] = _moon()
    T['ce_star'] = _star()
    T['ce_mitt'] = _cloth('#3a4a8a', 58)
    T['ce_boot'] = _boot()
    T['ce_shoe'] = _cloth('#3a3c46', 59)
    T['ce_band'] = _cloth('#2a2a32', 60)
    T['ce_shorts'] = _cloth('#2a3256', 61)
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: tall lace-crossed boots, chunky dark shoes, dark shorts peeking under the hem
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.7, 3.0) if sx > 0 else (-3.0, -0.7)
        return [_el((x0, 1.6, -1.15), (x1, 10.2, 1.15), 'ce_boot', pv), _el((x0 - 0.15, 9.8, -1.3), (x1 + 0.15, 10.6, 1.3), 'ce_mitt', pv),
                _el((x0, 10.4, -1.05), (x1, 13.6, 1.05), 'ce_shorts', pv),
                _el((x0 - 0.35, 0, -3.0), (x1 + 0.35, 1.8, 1.4), 'ce_shoe', pv), _el((x0 - 0.2, 1.6, -2.4), (x1 + 0.2, 2.2, 1.2), 'ce_shoe', pv)]
    part('ce_legr', leg(1)); part('ce_legl', leg(-1))

    # ---- body: a flared tunic skirt over a cloud of white fur, pompoms, the braided belt and moon buckle, a puffed chest
    pv = PIVOT['body']
    sk = lambda fr, to, rot=None: _el(fr, to, 'ce_skirt', pv, rot)
    fur = lambda fr, to, rot=None: _el(fr, to, 'ce_fur', pv, rot)
    body = [sk((-3.8, 14.8, -2.8), (3.8, 16.4, 2.8)), sk((-4.6, 13.2, -3.4), (4.6, 15.0, 3.4)), sk((-5.4, 11.6, -4.0), (5.4, 13.4, 4.0)),
            sk((-6.0, 10.2, -4.6), (6.0, 11.8, 4.6))]
    # the cloud hem: puffs all the way round, uneven
    for i in range(14):
        a = i / 14 * 2 * math.pi; r = 5.9; cx, cz = r * math.sin(a), -r * math.cos(a) * 0.82
        s = 1.5 + 0.35 * math.sin(i * 2.3)
        body.append(fur((cx - s, 8.9 + 0.2 * math.cos(i * 1.7), cz - s * 0.8), (cx + s, 10.9 + 0.2 * math.sin(i), cz + s * 0.8)))
    # the pale stripes fanning down the front of the skirt, lying on its tiers
    body += [_el((-1.5, 14.8, -2.95), (-0.8, 16.4, -2.8), 'ce_stripe', pv), _el((0.8, 14.8, -2.95), (1.5, 16.4, -2.8), 'ce_stripe', pv),
             _el((-1.9, 13.2, -3.55), (-1.1, 15.0, -3.4), 'ce_stripe', pv), _el((1.1, 13.2, -3.55), (1.9, 15.0, -3.4), 'ce_stripe', pv),
             _el((-2.3, 11.6, -4.15), (-1.4, 13.4, -4.0), 'ce_stripe', pv), _el((1.4, 11.6, -4.15), (2.3, 13.4, -4.0), 'ce_stripe', pv),
             _el((-2.7, 10.2, -4.75), (-1.7, 11.8, -4.6), 'ce_stripe', pv), _el((1.7, 10.2, -4.75), (2.7, 11.8, -4.6), 'ce_stripe', pv),
             fur((5.0, 11.4, -2.6), (6.6, 13.0, -1.0)), fur((-6.6, 11.4, -2.6), (-5.0, 13.0, -1.0)),                          # pompoms
             _el((-3.6, 16.2, -2.6), (3.6, 17.6, 2.6), 'ce_belt', pv),
             _el((-1.6, 15.6, -3.0), (1.6, 18.2, -2.55), 'ce_moon', pv, uv={'north': [0, 0, 4, 4]}),                        # the moon buckle
             _el((-3.2, 17.6, -2.2), (3.2, 23.6, 2.3), 'ce_tunic', pv),                                                         # chest
             _el((-0.3, 17.6, -2.35), (0.3, 23.0, -2.15), 'ce_stripe', pv),                                                     # the placket
             _el((-2.8, 23.2, -2.6), (2.8, 24.4, 2.6), 'ce_fur', pv),                                                           # the fluffy collar ...
             _el((-3.4, 22.6, -2.0), (-1.4, 25.2, 2.8), 'ce_fur', pv, ('z', 12, (-2.4, 22.6, 0))),
             _el((1.4, 22.6, -2.0), (3.4, 25.2, 2.8), 'ce_fur', pv, ('z', -12, (2.4, 22.6, 0))),
             _el((-2.4, 23.0, 2.0), (2.4, 25.4, 3.2), 'ce_fur', pv),                                                            # ... high at the back
             _el((-2.4, 21.0, -2.6), (-0.6, 22.8, -2.3), 'ce_star', pv, uv={'north': [0, 0, 4, 4]}),                            # the star brooch
             _el((-1.0, 23.6, -1.0), (1.0, 25.4, 1.0), 'ce_skin', pv)]
    part('ce_body', body)

    # ---- head: blue skin, long pointed ears, swept orange hair, the braid off the back-left ending in a flame of a tuft
    pv = PIVOT['head']; hr = lambda fr, to, rot=None: _el(fr, to, 'ce_hair', pv, rot)
    head = [_el((-4.5, 25.0, -4.0), (4.5, 33.0, 4.0), 'ce_skin', pv, uv={'north': [0, 0, 9, 8]}),
            # ears: long, tipped up and back
            _el((4.4, 28.0, -0.2), (8.4, 29.4, 0.8), 'ce_skin_dk', pv, ('z', 25, (4.4, 28.7, 0.3))),
            _el((-8.4, 28.0, -0.2), (-4.4, 29.4, 0.8), 'ce_skin_dk', pv, ('z', -25, (-4.4, 28.7, 0.3))),
            # hair: a full top, swept in a big wave from her right to left over the forehead, short at the sides
            hr((-4.9, 31.4, -4.5), (4.9, 34.0, 4.6)), hr((-4.4, 33.8, -3.6), (4.4, 35.0, 3.8)),
            hr((-4.9, 26.4, 3.4), (4.9, 31.6, 4.7)),
            hr((4.5, 27.4, -2.2), (5.1, 31.6, 4.4)), hr((-5.1, 27.4, -2.2), (-4.5, 31.6, 4.4)),
            hr((-4.9, 29.6, -4.7), (1.0, 31.6, -4.0)), hr((1.0, 30.4, -4.7), (4.9, 31.6, -4.0)),
            hr((-4.9, 28.8, -4.8), (-2.0, 30.0, -4.1), ('z', 12, (-4.9, 29.4, -4.4))),        # a lock falls over her left brow
            hr((-5.2, 33.2, -5.0), (-1.0, 35.4, -1.4), ('z', 16, (-3.0, 34.4, -3.0)))]        # the swoop up front
    # the braid: from behind her right ear, out and back, three plaits, a dark band, a flaring tuft
    def mx(fr, to, rot=None):
        """mirror a design box (built on her left, -x) onto her right"""
        f2, t2 = (-to[0], fr[1], fr[2]), (-fr[0], to[1], to[2])
        return hr(f2, t2, (rot[0], -rot[1], (-rot[2][0], rot[2][1], rot[2][2])) if rot else None)
    bx, by, bz = -4.2, 29.0, 3.4
    for i in range(3):
        x, y, z = bx - 1.3 * i, by - 0.5 * i, bz + 0.6 * i
        head.append(mx((x - 1.5, y - 0.8, z - 0.8), (x, y + 0.8, z + 0.8)))
    x, y, z = bx - 4.2, by - 1.5, bz + 1.8
    band = _el((-x, y - 0.9, z - 0.9), (-x + 1.2, y + 0.9, z + 0.9), 'ce_band', pv)
    head += [band, mx((x - 3.0, y - 0.6, z - 1.2), (x - 1.0, y + 2.0, z + 1.2), ('z', -30, (x - 1.0, y, z))),
             mx((x - 3.2, y - 2.0, z - 1.0), (x - 1.0, y + 0.4, z + 1.0), ('z', 25, (x - 1.0, y, z))),
             mx((x - 2.4, y + 1.0, z - 0.8), (x - 0.8, y + 3.2, z + 0.8), ('z', -55, (x - 0.8, y + 1.0, z)))]
    part('ce_head', head)
    head[0]['faces']['north']['texture'] = '#ce_face'
    M['ce_head'] = ({**M['ce_head'][0], 'ce_face': TX['ce_face']}, head)

    # ---- arms: big puffed shoulders (a pale band round them, fur trim below), long sleeves, dark mittens
    def arm(sx):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.2 * sx
        return [_el((cx - 2.1, 19.0, -2.1), (cx + 2.1, 24.6, 2.1), 'ce_tunic', pv),
                _el((cx - 2.3, 19.8, -1.6), (cx + 2.3, 23.8, 1.6), 'ce_tunic', pv), _el((cx - 1.6, 19.6, -2.3), (cx + 1.6, 24.0, 2.3), 'ce_tunic', pv),
                _el((cx - 2.15, 22.4, -2.15), (cx + 2.15, 23.4, 2.15), 'ce_stripe', pv),
                _el((cx - 1.9, 18.4, -1.9), (cx + 1.9, 19.4, 1.9), 'ce_fur', pv),
                _el((cx - 1.15, 14.4, -1.15), (cx + 1.15, 18.6, 1.15), 'ce_tunic', pv),
                _el((cx - 1.4, 11.8, -1.4), (cx + 1.4, 14.6, 1.4), 'ce_mitt', pv),
                _el((cx - (1.9 if sx > 0 else -1.0), 12.8, -1.4) if sx > 0 else (cx + 1.0, 12.8, -1.4),
                    (cx - 1.0, 14.0, -0.4) if sx > 0 else (cx + 1.9, 14.0, -0.4), 'ce_mitt', pv)]        # the thumb (inward)
    part('ce_armr', arm(1)); part('ce_arml', arm(-1))
    return M


# ---------------------------------------------------------------------------------------------------- preview
POSES = {   # her stance in the reference: right hand on her hip, left arm hanging, weight on one leg, a little haughty
    'stance': {'body': qmul(qa('y', -8), qa('z', 2)), 'head': qmul(qa('y', 22), qa('x', -4)), 'armr': qmul(qa('z', -24), qa('x', 10)),
               'arml': qa('z', 6), 'legr': qa('z', -6), 'legl': qa('z', 4)},
    'idle': {p: (0, 0, 0, 1) for p in PARTS},
}


def write_preview_pack(root):
    import json
    os.makedirs(f'{root}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{root}/assets/bm/textures/block', exist_ok=True)
    for k, im in textures().items(): im.save(f'{root}/assets/bm/textures/block/{k}.png')
    for name, (tex, els) in models().items():
        t = dict(tex); t['particle'] = next(iter(tex.values()))
        json.dump({'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}},
                  open(f'{root}/assets/bm/models/item/{name}.json', 'w'))


def render(out):
    from tools.render import Scene
    root = os.path.join(os.path.dirname(out), 'celi_rp'); write_preview_pack(root)
    U = RIG_SCALE / 16
    tiles = []
    for pose_name, views in (('stance', ('front', 'iso', 'side', 'back')), ('idle', ('front',))):
        pose = POSES[pose_name]
        for v in views:
            s = Scene(rp=root)
            for p in PARTS:
                x, y, z = PIVOT[p]
                s.display(f'bm:item/ce_{p}', pos=(-x * U, y * U, -z * U), scale=RIG_SCALE, left=tuple(pose[p]))
            s.player_box((1.0, 0, 0))
            im = s.render(v, size=460, span=2.2, center=(0.15, 0.95, 0))
            ImageDraw.Draw(im).text((8, 8), f'{pose_name} - {v}', fill=(0, 0, 0)); tiles.append(im)
    W, H = tiles[0].size
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (W * cols, H * rows), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * W, (i // cols) * H))
    sheet.save(out)


if __name__ == '__main__':
    render(sys.argv[1])
