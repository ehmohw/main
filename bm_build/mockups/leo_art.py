"""MOCKUP (not in the build): Leo the knight - blue tunic, open-faced silver helm, chainmail sleeves, pointed sabatons.

Same rig kit as Emma (phase57_art) and Celi: one item model per part, its joint at model (8, 8, 8). Design units: feet at
y=0, facing -z, his right is +x; drawn at RIG_SCALE. He is a grown-up next to Emma and Cecil: about a player's height.
    python3 mockups/leo_art.py <out.png>     renders a preview (salute: front / three-quarter / side / back; idle front)
"""
import math
import os
import random
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase57_art import _cloth, _hair, _el, hexc, qa, qmul

RIG_SCALE = 0.82
SALUTE_FOLD = -45
PIVOT = {'body': (0, 14, 0), 'head': (0, 26, 0), 'armr': (5.4, 24.2, 0), 'arml': (-5.4, 24.2, 0), 'legr': (2.1, 14, 0), 'legl': (-2.1, 14, 0)}
HEAD_K = 0.84          # (the helmeted head, smaller than Emma's: a grown man)
PARTS = tuple(PIVOT)
SKIN, SKIN_DK = '#9a6c50', '#7e5440'
HAIR = ('#1c1816', '#24201c', '#2c2622', '#342e28', '#3e3630')
STEEL, STEEL_DK, STEEL_LT = '#b4b8c0', '#868c96', '#dfe2e8'
BLUE, BLUE_LT, BLUE_DK = '#3f8fd6', '#78bce8', '#24528c'


# ---------------------------------------------------------------------------------------------------- textures
def _steel(seed, base=STEEL):
    """polished plate: a soft vertical sheen, a bright streak and a darker lower edge"""
    im = _cloth(base, seed, var=0.015); b = hexc(base)
    for y in range(64):
        for x in range(64):
            k = 1.0 + 0.10 * math.cos((x - 20) / 64 * math.pi * 2) - (0.12 if y > 54 else 0)
            if 14 <= x <= 17: k += 0.18
            p = im.getpixel((x, y)); im.putpixel((x, y), tuple(int(max(0, min(255, p[i] * k))) for i in range(3)) + (255,))
    return im


def _mail(seed):
    """chainmail: grey with a dark diamond lattice, the way the art draws it"""
    im = _cloth('#7c8188', seed, var=0.03); d = ImageDraw.Draw(im)
    for k in range(-64, 64, 6):
        d.line((k, 0, k + 64, 64), fill=hexc('#50555c')); d.line((k + 64, 0, k, 64), fill=hexc('#50555c'))
    for y in range(0, 64, 3):
        for x in range((y // 3) % 2, 64, 3): im.putpixel((x, y), hexc('#9aa0a8'))
    return im


def _face():
    """32 x 32: a dark fringe under the helm, heavy brows drawn down, narrowed green eyes, a scar through the left
    brow, a long nose, a set mouth and a few days' stubble on a square jaw - a soldier, not a boy"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(SKIN)); d = ImageDraw.Draw(im); rnd = random.Random(7)
    for y in range(24, 32):                                                                  # stubble: the jaw and chin, sparse
        for x in range(3, 29):
            edge = y >= 29 or x < 7 or x > 24 or (y >= 26 and 10 <= x <= 22 and y != 27)
            if edge and rnd.random() < 0.12 + 0.03 * (y - 24): im.putpixel((x, y), P(rnd.choice(('#7e5644', '#76503c', '#6a4634'))))
    for x in range(32):                                                                      # the fringe, ragged
        for y in range(0, 9 + (rnd.random() < 0.5) + (2 if x in (5, 6, 13, 14, 22, 27, 28) else 0)):
            im.putpixel((x, y), P(rnd.choice(HAIR[:3])))
    def eye(cx, flip):
        x0, y0 = cx - 4, 15
        d.polygon([(x0, y0 + 1), (x0 + 2, y0), (x0 + 7, y0), (x0 + 8, y0 + 1), (x0 + 6, y0 + 3), (x0 + 2, y0 + 3)], fill=P('#f2eee6'))
        d.rectangle((x0 + 3, y0, x0 + 5, y0 + 3), fill=P('#2f8a3a')); d.rectangle((x0 + 3, y0 + 2, x0 + 5, y0 + 3), fill=P('#4cb456'))
        d.rectangle((x0 + 4, y0 + 1, x0 + 4, y0 + 2), fill=P('#0e1a10'))
        d.point((x0 + (5 if not flip else 3), y0), fill=P('#d8f0d8'))
        d.line((x0, y0, x0 + 8, y0), fill=P('#1a1410')); d.line((x0 + 1, y0 - 1, x0 + 7, y0 - 1), fill=P('#5e3c2c'))   # a heavy upper lid
        d.line((x0 + 1, y0 + 4, x0 + 7, y0 + 4), fill=P(SKIN_DK))                                                  # tired shadow under
    eye(9, False); eye(23, True)
    for cx, s in ((9, 1), (23, -1)):                                                          # brows: thick, drawn down toward the nose
        for dx in range(-5, 5):
            y = 12 + (dx + 5) * 3 // 10
            x = cx + dx * s
            im.putpixel((x, y), P('#16110e')); im.putpixel((x, y + 1), P('#1e1814'))
    for y in range(9, 21): im.putpixel((25 - (y - 9) // 4, y), P('#c49680'))                 # the scar, through the left brow
    for y in range(15, 24): im.putpixel((16, y), P(SKIN_DK))                                  # a long nose, shaded down one side
    for y in range(18, 24): im.putpixel((17, y), P('#8a5e46'))
    d.line((14, 24, 18, 24), fill=P(SKIN_DK)); d.point((13, 23), fill=P(SKIN_DK)); d.point((19, 23), fill=P(SKIN_DK))
    d.line((12, 27, 20, 27), fill=P('#3a2016')); d.point((11, 28), fill=P('#3a2016')); d.point((21, 28), fill=P('#3a2016'))   # a set mouth
    for x in range(13, 20): im.putpixel((x, 28), P('#7e5440'))
    for cx in (5, 27):                                                                        # hard cheekbones
        for y in range(19, 23): im.putpixel((cx, y), P(SKIN_DK)); im.putpixel((cx + (1 if cx < 16 else -1), y + 1), P('#8a5e46'))
    for x in range(4, 28): im.putpixel((x, 31), P('#4e3226'))                                 # the jaw line
    return im


def _emblem():
    """the chest badge (10 x 11 texels): a pale water-drop in a crescent, a pink gem at its heart, three dots round it"""
    P = hexc
    im = Image.new('RGBA', (64, 64), P(BLUE)); d = ImageDraw.Draw(im)
    d.ellipse((1, 3, 9, 11), fill=P('#bfe6f6')); d.ellipse((2, 2, 8, 9), fill=P(BLUE))      # the crescent
    d.polygon([(5, 0), (7, 4), (5, 7), (3, 4)], fill=P('#d8f2fc'))                          # the drop
    d.polygon([(5, 3), (6, 4), (5, 6), (4, 4)], fill=P('#e04aa8')); d.point((5, 4), fill=P('#ff9ad8'))   # the gem
    for x, y in ((1, 2), (9, 2), (5, 10)): d.point((x, y), fill=P('#3a5ac8'))
    return im


def _cloth_hem(base, hem, seed):
    im = _cloth(base, seed, var=0.03)
    for y in range(50, 64):
        for x in range(64):
            t = (y - 50) / 14; a, b = hexc(base), hexc(hem)
            im.putpixel((x, y), tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3)) + (255,))
    return im


def textures():
    T = {}
    T['le_skin'] = _cloth(SKIN, 71, var=0.02)
    T['le_hair'] = _hair(72, HAIR)
    T['le_face'] = _face()
    T['le_steel'] = _steel(73)
    T['le_steel_dk'] = _steel(74, STEEL_DK)
    T['le_rim'] = _cloth(STEEL_LT, 75, var=0.01)
    T['le_mail'] = _mail(76)
    T['le_hose'] = _cloth('#6a6e75', 77, var=0.03)
    T['le_tunic'] = _cloth(BLUE, 78, var=0.03)
    T['le_skirt'] = _cloth_hem(BLUE, BLUE_LT, 79)
    T['le_cape'] = _cloth(BLUE_DK, 80, var=0.03)
    T['le_belt'] = _cloth('#6a4a2c', 81, var=0.04)
    T['le_emblem'] = _emblem()
    return T


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)

    # ---- legs: grey hose, a brown garter, a pointed knee plate, silver sabatons with long pointed toes
    def leg(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']
        x0, x1 = (0.5, 3.5) if sx > 0 else (-3.5, -0.5)
        cx = (x0 + x1) / 2
        return [_el((x0, 2.4, -1.4), (x1, 14.0, 1.4), 'le_hose', pv),
                _el((x0 - 0.1, 11.6, -1.5), (x1 + 0.1, 12.3, 1.5), 'le_belt', pv),                     # the garter
                _el((x0 - 0.2, 7.0, -1.9), (x1 + 0.2, 10.0, -1.3), 'le_steel', pv),                    # knee plate
                _el((cx - 0.8, 5.6, -1.85), (cx + 0.8, 7.4, -1.35), 'le_steel', pv, ('x', 0, (cx, 7, -1.6))),
                _el((x0 - 0.2, 1.6, -1.7), (x1 + 0.2, 3.0, 1.7), 'le_steel', pv),                     # the sabaton's cuff
                _el((x0 - 0.3, 0, -3.4), (x1 + 0.3, 1.8, 1.8), 'le_steel', pv),                       # the foot
                _el((cx - 1.0, 0, -4.8), (cx + 1.0, 1.2, -3.3), 'le_steel', pv),                      # the long toe
                _el((cx - 0.5, 0, -5.8), (cx + 0.5, 0.8, -4.7), 'le_steel', pv),
                _el((x0 - 0.35, 0, 1.6), (x1 + 0.35, 1.0, 2.2), 'le_steel_dk', pv)]                    # the heel
    part('le_legr', leg(1)); part('le_legl', leg(-1))

    # ---- body: tunic to the knee (paler at the hem), the badge, a broad belt and silver buckle, a mail gorget, a cape
    pv = PIVOT['body']
    body = [_el((-4.0, 17.4, -2.4), (4.0, 24.8, 2.4), 'le_tunic', pv),                                  # chest, broad
            _el((-3.8, 13.0, -2.4), (3.8, 17.6, 2.4), 'le_skirt', pv, uv={f: [0, 0, 7.6, 4.6] for f in ('north', 'south')}),
            _el((-4.3, 9.4, -2.9), (4.3, 13.2, 2.9), 'le_skirt', pv, uv={f: [0, 8, 8.6, 16] for f in ('north', 'south', 'east', 'west')}),
            _el((-4.4, 8.8, -3.0), (4.4, 9.6, 3.0), 'le_skirt', pv, uv={f: [0, 15, 8.8, 16] for f in ('north', 'south', 'east', 'west')}),
            _el((1.0, 8.0, -3.1), (4.6, 9.4, 1.0), 'le_skirt', pv, ('z', -12, (4.4, 9.4, 0)), uv={f: [0, 15, 3.6, 16] for f in ('north', 'south', 'east', 'west')}),   # a flick of the hem
            _el((-3.9, 16.6, -2.6), (3.9, 18.0, 2.6), 'le_belt', pv),
            _el((-1.0, 16.2, -2.95), (1.5, 18.4, -2.55), 'le_rim', pv), _el((0.6, 16.3, -3.05), (1.2, 18.3, -2.9), 'le_steel_dk', pv),   # the buckle
            _el((-1.25, 20.4, -2.35), (1.25, 23.2, -2.2), 'le_emblem', pv, uv={'north': [0, 0, 2.5, 2.8]}),
            # the mail gorget, round over the shoulders, with a bright rim
            _el((-3.0, 22.8, -2.55), (3.0, 25.2, -2.25), 'le_mail', pv),
            _el((-3.2, 22.5, -2.6), (3.2, 22.9, -2.3), 'le_rim', pv),
            _el((-3.4, 24.6, -2.7), (3.4, 26.4, 2.7), 'le_mail', pv),
            _el((-3.6, 24.4, -2.75), (3.6, 24.8, 2.75), 'le_rim', pv),
            # the cape: from the shoulders to the back of the knees, a little away from him at the bottom
            _el((-3.6, 10.0, 2.3), (3.6, 25.0, 2.8), 'le_cape', pv, ('x', -7.5, (0, 25.0, 2.5))),
            _el((-3.6, 10.0, 2.4), (3.6, 10.6, 3.0), 'le_rim', pv, ('x', -7.5, (0, 25.0, 2.5)))]
    part('le_body', body)

    # ---- head: an open-faced helm - a round skull, a finial on top, a brow that dips at the centre, cheek guards
    #      sweeping down to points at the jaw, a flared back; dark hair shows under the brow
    pv = PIVOT['head']; st = lambda fr, to, rot=None, t='le_steel': _el(fr, to, t, pv, rot)
    head = [_el((-4.0, 26.0, -3.8), (4.0, 34.0, 3.8), 'le_skin', pv, uv={'north': [0, 0, 8, 8]}),
            st((-4.5, 31.8, -4.3), (4.5, 34.8, 4.4)), st((-3.9, 34.6, -3.7), (3.9, 35.8, 3.8)), st((-2.6, 35.6, -2.4), (2.6, 36.3, 2.5)),
            st((-0.45, 36.0, -0.6), (0.45, 37.4, 0.3)), st((-0.3, 37.2, -0.4), (0.3, 38.0, 0.1), t='le_rim'),     # the finial
            st((-4.6, 31.2, -4.5), (-1.0, 32.0, -4.25), t='le_rim'), st((1.0, 31.2, -4.5), (4.6, 32.0, -4.25), t='le_rim'),
            st((-1.2, 30.7, -4.5), (1.2, 31.8, -4.25), t='le_rim'),                                         # the brow dips at the centre
            st((-0.8, 32.6, -4.45), (0.8, 33.4, -4.3), t='le_steel_dk'),                                     # the little crest on the brow
            # cheek guards: down the sides, flaring out to points beside the jaw
            st((3.9, 27.6, -3.4), (4.7, 31.2, 4.4)), st((-4.7, 27.6, -3.4), (-3.9, 31.2, 4.4)),
            st((3.9, 25.6, -3.2), (4.6, 27.8, -1.0), ('z', 22.5, (4.2, 27.8, -2.0))),
            st((-4.6, 25.6, -3.2), (-3.9, 27.8, -1.0), ('z', -22.5, (-4.2, 27.8, -2.0))),
            st((3.85, 27.6, -3.5), (4.75, 28.0, 0.8), t='le_rim'), st((-4.75, 27.6, -3.5), (-3.85, 28.0, 0.8), t='le_rim'),
            # the back, down to the nape, flicking out
            st((-4.5, 27.0, 3.8), (4.5, 31.2, 4.5)), st((-3.0, 25.6, 4.0), (3.0, 27.4, 4.8), ('x', -22.5, (0, 27.4, 4.2))),
            # hair at the temples, under the guards
            _el((-4.1, 29.0, -3.9), (-3.6, 31.0, -1.0), 'le_hair', pv), _el((3.6, 29.0, -3.9), (4.1, 31.0, -1.0), 'le_hair', pv)]
    for e in head:                                                                                       # shrink about the neck
        e['from'] = [round(8 + (v - 8) * HEAD_K, 4) for v in e['from']]; e['to'] = [round(8 + (v - 8) * HEAD_K, 4) for v in e['to']]
        if 'rotation' in e: e['rotation']['origin'] = [round(8 + (v - 8) * HEAD_K, 4) for v in e['rotation']['origin']]
    part('le_head', head)
    head[0]['faces']['north']['texture'] = '#le_face'
    M['le_head'] = ({**M['le_head'][0], 'le_face': TX['le_face']}, head)

    # ---- arms: a domed pauldron, a short blue sleeve, a bright rim, chainmail forearm, a plated gauntlet
    def arm(sx):
        nm = 'armr' if sx > 0 else 'arml'; pv = PIVOT[nm]; cx = pv[0] + 0.3 * sx
        return [_el((cx - 2.1, 22.8, -2.2), (cx + 2.1, 25.6, 2.2), 'le_steel', pv), _el((cx - 1.6, 25.4, -1.7), (cx + 1.6, 26.3, 1.7), 'le_steel', pv),
                _el((cx - 2.15, 22.6, -2.25), (cx + 2.15, 23.0, 2.25), 'le_rim', pv),
                _el((cx - 1.5, 19.0, -1.5), (cx + 1.5, 23.0, 1.5), 'le_tunic', pv), _el((cx - 1.7, 18.8, -1.7), (cx + 1.7, 19.8, 1.7), 'le_tunic', pv),
                _el((cx - 1.45, 18.2, -1.45), (cx + 1.45, 18.9, 1.45), 'le_rim', pv),
                _el((cx - 1.3, 14.4, -1.3), (cx + 1.3, 18.4, 1.3), 'le_mail', pv),
                _el((cx - 1.5, 13.8, -1.5), (cx + 1.5, 14.6, 1.5), 'le_rim', pv),                                     # the gauntlet's cuff
                _el((cx - 1.25, 11.6, -1.25), (cx + 1.25, 14.0, 1.25), 'le_steel', pv),
                _el((cx - 1.0, 10.6, -1.1), (cx + 1.0, 11.8, 0.9), 'le_steel_dk', pv),                                 # fingers
                _el((cx - 1.9 * sx if sx > 0 else cx + 1.0, 12.4, -1.4) if sx > 0 else (cx + 1.0, 12.4, -1.4),
                    (cx - 1.0, 13.6, -0.4) if sx > 0 else (cx + 1.9, 13.6, -0.4), 'le_steel', pv)]                     # the thumb (inward)
    part('le_armr', arm(1)); part('le_arml', arm(-1))

    # ---- the saluting arm (his left, as in the art): the same sleeve, bent hard at the elbow - the forearm folds back
    #      up toward the helm, two fingers raised
    def salute(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; cx = pv[0] + 0.3 * sx; ey = 18.6; FA = SALUTE_FOLD * sx
        fold = lambda fr, to, t: _el(fr, to, t, pv, ('z', FA, (cx, ey, 0)))
        up = lambda y0, y1: (2 * ey - y1, 2 * ey - y0)          # (a forearm span, mirrored to run UP from the elbow)
        box = lambda w, y0, y1, t, z0=None, z1=None: fold((cx - w, up(y0, y1)[0], -w if z0 is None else z0), (cx + w, up(y0, y1)[1], w if z1 is None else z1), t)
        return arm(sx)[:6] + [box(1.3, 14.4, 18.4, 'le_mail'), box(1.5, 13.8, 14.6, 'le_rim'), box(1.25, 11.6, 14.0, 'le_steel'),
                              box(0.5, 9.4, 11.8, 'le_steel_dk', -1.0, -0.2), box(0.5, 9.4, 11.8, 'le_steel_dk', 0.0, 0.8),      # two fingers, up
                              box(1.0, 10.8, 11.8, 'le_steel_dk', -1.1, 1.0)]                                                     # the curled ones
    part('le_arml_salute', salute(-1))
    return M


# ---------------------------------------------------------------------------------------------------- preview
POSES = {   # the reference: mid-stride, a two-finger salute off the helm with his right hand, left arm swinging
    'salute': {'body': qa('y', 8), 'head': qmul(qa('y', -10), qa('x', 4)),
               'arml': qmul(qa('y', 6), qmul(qa('z', 96), qa('x', -18))), 'armr': qmul(qa('x', 18), qa('z', 5)),     # (arml solved: fingertips on the helm's side, elbow out)
               'legr': qa('x', 22), 'legl': qa('x', -20)},
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


def render(out, compare_rp=None):
    from tools.render import Scene
    root = os.path.join(os.path.dirname(os.path.abspath(out)), 'leo_rp'); write_preview_pack(root)
    U = RIG_SCALE / 16
    tiles = []
    for pose_name, views in (('salute', ('front', 'iso', 'side', 'back')), ('idle', ('front', 'face'))):
        pose = POSES[pose_name]
        for v in views:
            s = Scene(rp=root)
            for p in PARTS:
                x, y, z = PIVOT[p]
                mdl = 'le_arml_salute' if (p == 'arml' and pose_name == 'salute') else f'le_{p}'
                s.display(f'bm:item/{mdl}', pos=(-x * U, y * U, -z * U), scale=RIG_SCALE, left=tuple(pose[p]))
            s.player_box((1.1, 0, 0))
            im = s.render('front', size=460, span=0.75, center=(0, 1.62, 0)) if v == 'face' else s.render(v, size=460, span=2.4, center=(0.2, 1.0, 0))
            ImageDraw.Draw(im).text((8, 8), f'{pose_name} - {v}', fill=(0, 0, 0)); tiles.append(im)
    W, H = tiles[0].size
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (W * cols, H * rows), 'white')
    for i, t in enumerate(tiles): sheet.paste(t, ((i % cols) * W, (i // cols) * H))
    sheet.save(out)


if __name__ == '__main__':
    render(sys.argv[1])
