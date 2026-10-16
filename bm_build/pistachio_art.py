"""Pistachio (2.80d): the ghost who keeps house at the Omega Palace - from the owner's art. A mint-green spirit with a green
glow at his edges: a tall grey top hat with a red band (and a toothy grin of its own on its front), big round eyes under
stern brows, a gold monocle on his left eye, a curled black moustache over one small fang; a charcoal tail-coat with a red
tie, its buttons and its breast pocket; no legs - his body thins into a tail that curls up behind him. In his right hand,
held out on its platter, a silver serving cloche (its lid lifts: the cloche is his trick).

A rigkit rig like Fishy's: body, tail, head (a model per expression), arms bent at the elbow (his right forearm holds the
platter out in front of him), and the cloche's lid. He floats - his feet would be at y=0, but he has none. Design units: facing
-z, his right is +x."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from tullius_art import _noise, _shine
from rigkit import qs, el, seg, chain, I

PREFIX = 'ps_'
RIG_SCALE = 1.0
PIVOT = {'body': (0, 8.0, 0), 'tail': (0, 5.6, 0.6), 'head': (0, 15.6, 0),
         'armr': (3.6, 14.4, 0), 'forer': (5.0, 11.4, 0), 'arml': (-3.6, 14.4, 0), 'forel': (-5.0, 11.2, 0),
         'lid': (5.6, 12.5, -2.4)}
PARENT = {'body': None, 'tail': 'body', 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml', 'lid': 'forer'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('happy', 'shock', 'squint')
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)
TRAY = (5.6, 11.9, -5.0)                     # the platter's centre (on his right palm)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
GHOST_A = 150                                               # (2.80d: his ghostly body is see-through - his clothes aren't)


def _ghost(seed, base='#c8f7d2', edge='#46c864'):
    im = _noise(base, seed, 4); d = ImageDraw.Draw(im)
    for i in range(3):                                      # the green glow at his edges (a touch more solid than the rest)
        d.rectangle((i, i, 63 - i, 63 - i), outline=hexc(edge)[:3] + (255 - i * 70,))
    px = im.load()
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, a = px[x, y]
            edge_px = min(x, y, im.width - 1 - x, im.height - 1 - y) < 3
            px[x, y] = (r, g, b, min(a, 200 if edge_px else GHOST_A))
    return im


def _coat(seed, base='#3c3c3e', lt='#5c5c60'):
    im = _shine(base, lt, seed); d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(4):
        x = rnd.randrange(64); d.line((x, 0, x + rnd.randint(-4, 4), 63), fill=hexc('#2c2c2e'))
    return im


def _eye(look=0, wide=False, happy=False, shut=False):
    im = Image.new('RGBA', (16, 16), hexc('#c8f7d2')); d = ImageDraw.Draw(im)
    if shut:
        d.line((1, 9, 14, 9), fill=hexc('#1e6a2e'), width=2); return im
    if happy:
        d.arc((2, 4, 13, 15), 200, 340, fill=hexc('#1e6a2e'), width=2); return im
    d.ellipse((0, 0, 15, 15), fill=hexc('#ecf0ea'), outline=hexc('#1e6a2e'))
    r = 1 if wide else 2
    d.ellipse((7 - r + look, 8 - r, 7 + r + look, 8 + r), fill=hexc('#1a7a2a'))
    return im


def _hatface():
    """the top hat's own grin: a curved line with two big fangs at its ends and two little ones"""
    im = _shine('#5e5e5c', '#7a7a78', 1418); d = ImageDraw.Draw(im)
    d.arc((14, 6, 50, 34), 20, 160, fill=hexc('#1a1a1a'), width=2)
    for x, y, w, h in ((16, 18, 4, 7), (44, 18, 4, 7), (26, 30, 2, 4), (36, 30, 2, 4)):
        d.polygon([(x, y), (x + w, y), (x + w // 2, y + h)], fill=hexc('#f4f0ea'))
    return im


def _stache(seed):
    im = _noise('#1e1e20', seed, 4); rnd = random.Random(seed)
    for x in range(0, 64, 3):
        for y in range(rnd.randrange(3), 64, 5):
            im.putpixel((x, y), hexc('#3a3a3e'))
    return im


def textures():
    return {'ps_ghost': _ghost(1401), 'ps_ghost_dk': _ghost(1402, '#a8ecb8', '#36b054'), 'ps_coat': _coat(1403), 'ps_coat_dk': _coat(1404, '#2a2a2c', '#3e3e42'),
            'ps_lapel': _coat(1405, '#4a4a4e', '#6e6e72'), 'ps_tie': _shine('#b02a30', '#e05a5e', 1406), 'ps_button': _noise('#141414', 1407, 2),
            'ps_hat': _shine('#5e5e5c', '#7a7a78', 1408), 'ps_hat_dk': _shine('#363634', '#4e4e4c', 1409), 'ps_band': _shine('#c8383a', '#ff7068', 1410),
            'ps_hatface': _hatface(), 'ps_stache': _stache(1411), 'ps_gold': _shine('#e2c02c', '#fff2a0', 1412), 'ps_lens': _noise('#e6f4f0', 1413, 3),
            'ps_brow': _noise('#226a32', 1414, 3), 'ps_fang': _noise('#f4f2ec', 1415, 2), 'ps_silver': _shine('#a8aaa6', '#f0f2ee', 1416),
            'ps_silver_dk': _shine('#7a7c78', '#b8bab6', 1417), 'ps_plate': _shine('#d8d6cc', '#ffffff', 1419),
            'ps_eye': _eye(), 'ps_eye_l': _eye(look=-2), 'ps_eye_wide': _eye(wide=True), 'ps_eye_happy': _eye(happy=True), 'ps_eye_shut': _eye(shut=True)}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the tail-coat (lapels, buttons, pocket), the red tie, the green of his neck; under the coat his body
    #      narrowing into the tail's root
    pv = PIVOT['body']
    body = [el((-3.3, 8.2, -2.4), (3.3, 15.4, 2.4), 'ps_coat', pv),
            el((-3.6, 6.6, -2.6), (3.6, 9.0, 2.6), 'ps_coat_dk', pv, shift=(0.3, 0.2)),           # the coat's skirts
            el((-2.9, 4.6, -2.1), (2.9, 7.0, 2.1), 'ps_ghost', pv),                                # his body, out from under it
            el((-2.2, 3.8, -1.6), (2.2, 4.6, 1.8), 'ps_ghost_dk', pv),
            el((-1.5, 14.0, -2.5), (1.5, 15.5, -2.3), 'ps_ghost', pv, faces=('north',)),           # his neck, in the coat's V
            el((-0.55, 11.4, -2.6), (0.55, 14.6, -2.45), 'ps_tie', pv), el((-0.7, 14.4, -2.62), (0.7, 15.2, -2.45), 'ps_tie', pv, shift=(0.5, 0.5)),
            el((1.4, 12.2, -2.55), (2.6, 13.4, -2.42), 'ps_lapel', pv, faces=('north',))]          # the pocket
    for sx in (1, -1):                                                                             # the lapels
        body += [seg((sx * 0.7, 15.2, -2.52), (sx * 1.9, 10.2, -2.52), 0.9, 0.12, 'ps_lapel', pv, FRONT)]
    for y in (9.6, 11.0, 12.4):
        body.append(el((-1.25, y, -2.56), (-0.75, y + 0.5, -2.45), 'ps_button', pv))
    part('ps_body', body)

    # ---- the tail: down from his body and curling round up behind him (his right side), tapering to a point
    pv = PIVOT['tail']
    tail = chain([(0, 5.6, 0.6), (0.4, 3.4, 1.0), (1.8, 1.6, 1.8), (3.8, 1.0, 2.6), (5.6, 2.0, 3.0), (6.6, 4.2, 3.1), (6.6, 6.6, 3.0)],
                 [4.6, 4.0, 3.2, 2.5, 1.8, 1.2], 3.6, 'ps_ghost', pv, SIDE, hs=[4.0, 3.4, 2.8, 2.2, 1.6, 1.0])
    part('ps_tail', tail)

    # ---- the head: round and wide, big eyes (his right one plain, his left behind the monocle), stern brows, the moustache
    #      and its fang; the top hat (its brim, its red band, its grin)
    pv = PIVOT['head']
    def head(face=None):
        h = [el((-3.6, 15.5, -3.2), (3.6, 21.6, 3.0), 'ps_ghost', pv),                     # (side cheeks and chin butt onto it, never inside:
             el((3.6, 16.2, -2.6), (3.95, 20.4, 2.4), 'ps_ghost', pv, shift=(0.4, 0.3)),          #  he's see-through, and an inner face would show)
             el((-3.95, 16.2, -2.6), (-3.6, 20.4, 2.4), 'ps_ghost', pv, shift=(0.4, 0.3)),
             el((-3.0, 15.0, -2.6), (3.0, 15.5, 2.4), 'ps_ghost_dk', pv)]
        tex = {None: ('ps_eye', 'ps_eye_l'), 'happy': ('ps_eye_happy', 'ps_eye_happy'), 'shock': ('ps_eye_wide', 'ps_eye_wide'),
               'squint': ('ps_eye_shut', 'ps_eye_l')}[face]
        for sx, t in ((1, tex[0]), (-1, tex[1])):
            h.append(el((sx * 1.75 - 1.25, 18.0, -3.3), (sx * 1.75 + 1.25, 20.6, -3.18), t, pv, faces=('north',), uv={'north': [0, 0, 16, 16]}))
        # the brows: stern (slanting down to the middle), raised when he's pleased or shocked
        by = {None: 0.0, 'happy': 0.5, 'shock': 0.8, 'squint': -0.2}[face]
        for sx in (1, -1):
            tilt = -10 if face in (None, 'squint') else 8
            h.append(el((sx * 1.75 - 1.3, 20.8 + by, -3.36), (sx * 1.75 + 1.3, 21.3 + by, -3.22), 'ps_brow', pv, ('z', tilt * sx, (sx * 1.75, 21.05 + by, -3.3))))
        # the monocle, on his left eye (dropped on its chain when he's shocked)
        mx, my, mz = -1.75, 19.3, -3.42
        if face == 'shock':
            mx, my = -2.6, 16.6
        ring = [((mx - 1.0, my - 1.0), (mx + 1.0, my - 0.8)), ((mx - 1.0, my + 0.8), (mx + 1.0, my + 1.0)),
                ((mx - 1.0, my - 0.8), (mx - 0.8, my + 0.8)), ((mx + 0.8, my - 0.8), (mx + 1.0, my + 0.8))]
        h += [el((a[0], a[1], mz - 0.08), (b[0], b[1], mz + 0.04), 'ps_gold', pv) for a, b in ring]
        h += chain([(mx + 0.5, my - 0.9, mz), (-1.2, 16.4, -3.3), (-0.9, 15.6, -3.0)], [0.14, 0.14], 0.1, 'ps_gold', pv, FRONT, ext=0.04)
        # the moustache: two fat curls, and the fang under it
        for sx in (1, -1):
            h += chain([(sx * 0.1, 17.4, -3.36), (sx * 1.3, 17.2, -3.42), (sx * 2.4, 17.5, -3.4), (sx * 2.7, 18.1, -3.36), (sx * 2.25, 18.35, -3.34)],
                       [0.95, 0.8, 0.6, 0.45], 0.3, 'ps_stache', pv, FRONT, ext=0.08)
        if face != 'happy':
            h.append(el((0.2, 16.3, -3.3), (0.6, 16.9, -3.2), 'ps_fang', pv))
        # the top hat, cocked a touch to his left
        hp = (0, 21.4, 0)
        rot = lambda: ((0.0, 0.0, 5.0), hp)
        h += [el((-4.7, 21.3, -4.0), (4.7, 21.9, 3.8), 'ps_hat_dk', pv, rot()),
              el((-3.0, 21.8, -2.6), (3.0, 27.8, 2.4), 'ps_hat', pv, rot(), shift=(0.2, 0.1)),
              el((-3.3, 27.4, -2.9), (3.3, 28.6, 2.7), 'ps_hat', pv, rot(), shift=(0.6, 0.4)),     # (flaring out at the top)
              el((-3.06, 21.9, -2.66), (3.06, 23.1, 2.46), 'ps_band', pv, rot()),
              el((-2.6, 23.6, -2.7), (2.6, 27.2, -2.62), 'ps_hatface', pv, rot(), faces=('north',), uv={'north': [0, 0, 16, 16]})]
        return h
    part('ps_head', head())
    for fc in FACES:
        part(f'ps_head_x{fc}', head(fc))

    # ---- the arms: coat sleeves, mint mitten hands. His right forearm reaches forward, palm up, the platter and the cloche's
    #      dome on it; his left hangs, three fingers and a thumb
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        a = [el((x0 - 1.3, y0 - 1.2, -1.4), (x0 + 1.3, y0 + 1.0, 1.4), 'ps_coat', pv, shift=(0.4, 0.2))]
        a += chain([(x0, y0, 0), PIVOT['forer' if sx > 0 else 'forel']], [2.2], 2.2, 'ps_coat', pv, FRONT, ext=0.25)
        return a
    def lower_r():
        pv = PIVOT['forer']; ex, ey, ez = pv
        wx, wy, wz = 5.6, 11.6, -3.2
        a = chain([(ex, ey, ez), (wx, wy, wz)], [2.0], 2.0, 'ps_coat', pv, UP, ext=0.2)
        a += [el((wx - 1.15, wy - 0.9, wz - 2.6), (wx + 1.15, wy + 0.1, wz - 0.4), 'ps_ghost', pv),           # the palm, up
              el((wx + 1.15, wy - 0.6, wz - 1.6), (wx + 1.6, wy + 0.3, wz - 0.6), 'ps_ghost_dk', pv)]          # the thumb
        tx, ty, tz = TRAY
        a += [el((tx - 2.7, ty, tz - 2.7), (tx + 2.7, ty + 0.25, tz + 2.7), 'ps_plate', pv),
              el((tx - 2.0, ty - 0.05, tz - 3.15), (tx + 2.0, ty + 0.25, tz + 3.15), 'ps_plate', pv, shift=(0.5, 0.5)),
              el((tx - 3.15, ty - 0.05, tz - 2.0), (tx + 3.15, ty + 0.25, tz + 2.0), 'ps_plate', pv, shift=(0.3, 0.7))]
        return a
    def lower_l():
        pv = PIVOT['forel']; ex, ey, _ = pv
        wx, wy = -5.5, 8.4
        a = chain([(ex, ey, 0), (wx, wy, 0)], [2.0], 2.0, 'ps_coat', pv, FRONT, ext=0.2)
        a += [el((wx - 1.1, wy - 2.0, -1.0), (wx + 1.1, wy + 0.1, 1.0), 'ps_ghost', pv),
              el((wx + 0.6, wy - 1.6, -1.4), (wx + 1.3, wy - 0.4, -1.0), 'ps_ghost_dk', pv)]
        return a
    part('ps_armr', upper(1)); part('ps_arml', upper(-1)); part('ps_forer', lower_r()); part('ps_forel', lower_l())

    # ---- the cloche's lid: a silver dome (four tiers) with a knob, hinged at the platter's back edge
    pv = PIVOT['lid']; tx, ty, tz = TRAY; ty += 0.25
    lid = [el((tx - 2.3, ty, tz - 2.3), (tx + 2.3, ty + 1.3, tz + 2.3), 'ps_silver', pv),
           el((tx - 1.9, ty + 1.2, tz - 1.9), (tx + 1.9, ty + 2.1, tz + 1.9), 'ps_silver', pv, shift=(0.4, 0.3)),
           el((tx - 1.3, ty + 2.0, tz - 1.3), (tx + 1.3, ty + 2.6, tz + 1.3), 'ps_silver', pv, shift=(0.7, 0.6)),
           el((tx - 0.3, ty + 2.5, tz - 0.3), (tx + 0.3, ty + 3.1, tz + 0.3), 'ps_silver_dk', pv),
           el((tx - 2.45, ty, tz - 2.45), (tx + 2.45, ty + 0.3, tz + 2.45), 'ps_silver_dk', pv)]
    part('ps_lid', lid)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def limb(sx, fwd=0.0, out=0.0):
    return qs(('x', -fwd), ('z', -out * sx))


def P(**kw):
    return kw


HOVER = 1.4                                  # (he floats: every pose lifts him off the ground a little)
POSES = {
    'idle_a': P(_off=(0, HOVER, 0), arml=limb(-1, 4, 6), forel=limb(-1, 10), tail=qs(('y', 8)), head=qs(('y', 4))),
    'idle_b': P(_off=(0, HOVER + 0.5, 0), arml=limb(-1, 8, 4), forel=limb(-1, 16), tail=qs(('y', -10), ('z', 4)), head=qs(('y', -6), ('x', 3))),
    'walk_a': P(_off=(0, HOVER + 0.4, 0), body=qs(('x', 10)), tail=qs(('x', 18), ('y', 12)), arml=limb(-1, -14, 6), forel=limb(-1, 14), head=qs(('x', -6))),
    'walk_b': P(_off=(0, HOVER + 0.8, 0), body=qs(('x', 12)), tail=qs(('x', 24), ('y', -12)), arml=limb(-1, 14, 6), forel=limb(-1, 20), head=qs(('x', -8))),
    'wave_a': P(_face='happy', _off=(0, HOVER, 0), arml=limb(-1, 10, 120), forel=limb(-1, 40), tail=qs(('y', 10)), head=qs(('y', -8))),
    'wave_b': P(_face='happy', _off=(0, HOVER, 0), arml=limb(-1, 10, 134), forel=limb(-1, 14), tail=qs(('y', -10)), head=qs(('y', -4), ('z', 4))),
    # a butler's bow: the hat stays put on his head, the platter kept level
    'bow': P(_off=(0, HOVER - 0.4, 0), body=qs(('x', 24)), head=qs(('x', 8)), armr=limb(1, -24), forer=limb(1, 0), arml=limb(-1, 34, -14), forel=limb(-1, 70),
             tail=qs(('x', -12))),
    'point': P(_face='squint', _off=(0, HOVER, 0), arml=limb(-1, 84, 6), forel=limb(-1, 4), head=qs(('y', -14))),
    'shock': P(_face='shock', _off=(0, HOVER + 1.2, 0), armr=limb(1, 10, 20), arml=limb(-1, 30, 40), forel=limb(-1, 60), tail=qs(('x', -20)), head=qs(('x', -8))),
    # (sat in the air, the tail coiled under him like a cushion)
    'sit': P(_off=(0, -1.6, 0), tail=qs(('x', -40), ('y', 30)), arml=limb(-1, 24, 8), forel=limb(-1, 50), head=qs(('y', 8))),
    'tired': P(_face='squint', _off=(0, 0.2, 0), body=qs(('x', 12), ('z', -6)), head=qs(('x', 18)), armr=limb(1, -6, 2), arml=limb(-1, 0, 2), forel=limb(-1, 4),
               tail=qs(('x', 20))),
    'lid_up': P(_face='happy', _off=(0, HOVER, 0), lid=qs(('x', -70)), arml=limb(-1, 50, 30), forel=limb(-1, 40), head=qs(('y', -10)))}
DRAFT = ['idle_a', 'walk_a', 'wave_a', 'bow', 'point', 'shock', 'sit', 'tired', 'lid_up']
