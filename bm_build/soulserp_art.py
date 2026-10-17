"""SOUL SERPENTS - King Omega's undead soldiers (a draft for approval: rig, textures, faces, poses; not in the pack).

From the owner's art: small ghastly serpents left over from the war between Apophiss and Omega - soldiers once, mischievous
now. Serpents of the brothers' own kind (the owner: "more serpentine, like Apophiss and Omega"): built on the brothers' rig -
the same serpent's head with its snout, nostrils and heavy lids, the same rearing S of a body out of a coil, the light belly
plate down the front, fins down the back - but small, leaner, and none of a king's things (no crown, no monocle, no scars):
  - pale grey-blue hide, see-through like their king's (more so), the belly plate lighter, the honeycomb marks dropped;
  - solid glowing yellow eyes under grey lids and thin black brows (the family's scowl);
  - a purple maw, cream fangs, the long purple forked tongue;
  - a little blue soul flame on the tip of the tail (where Apophiss carries his mace and Omega his great flame).
Three crests (the art's three soldiers - mixed in a squad so they aren't clones):
  a: pale spikes swept back off the back of the skull (a centre row, a pair either side)
  b: the spikes dark, and one tall dark horn up from the crown of the head (the middle soldier)
  c: no spikes - two big black horns curving back (the lone one)
Cute but mischievous: smaller than a player's head-height (RIG_SCALE 0.6, about two blocks), solid glowing yellow eyes (no
pupils), the family's scowling lids and brows.
Faces (the brothers' lids and brows): grin (smug, half-lidded), shriek (eyes wide), hurt, blink.

Rig: Apophiss's (coil - body - chest - head - jaw, arms off the chest, tail1-4 - flame), the body parts narrowed to 0.78 and
the arms brought in to match. Design units as there (the coil on y=0, facing -z, his right +x); about two blocks tall at
RIG_SCALE 0.6."""
import math
import os
import random
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apophiss_art as A
import omega_art as O
from rigkit import qs, el, seg, chain, I, mid, solve, qmul

PREFIX = 'ss_'
RIG_SCALE = 0.6                                # (about two blocks - a player's height; v2 was 0.75)
LEAN = 0.78                                    # (the body parts' width, x, against the brothers')
ARM_X = 6.6                                    # (the arms' shoulders, brought in from the brothers' 8.4)
PIVOT = {('flame' if k == 'mace' else k): v for k, v in A.PIVOT.items() if k not in ('wingr', 'wingl')}
PIVOT['armr'] = (ARM_X, PIVOT['armr'][1], PIVOT['armr'][2]); PIVOT['arml'] = (-ARM_X, PIVOT['arml'][1], PIVOT['arml'][2])
PARENT = {('flame' if k == 'mace' else k): ('flame' if v == 'mace' else v) for k, v in A.PARENT.items() if k not in ('wingr', 'wingl')}
PARTS = tuple(PIVOT)
PART_K = {}
CRESTS = ('a', 'b', 'c')
FACES = ('grin', 'shriek', 'hurt', 'blink')
_AFACE = {'grin': 'smug', 'shriek': 'shock', 'hurt': 'hurt', 'blink': 'blink'}
GHOST_A = 128
UP, FRONT, SIDE = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    if p == 'head':
        face = f'_x{pose["_face"]}' if pose.get('_face') else ''
        return f'{PREFIX}head_{pose.get("_crest", "a")}{face}{suffix}'
    return f'{PREFIX}{p}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def textures():
    g = O._ghost
    return {'ss_body': g(A._scales('#b4bcc6', '#949ca8', '#d6dce4', 901), GHOST_A), 'ss_body_dk': g(A._scales('#8a929e', '#6e7682', '#a6aeb8', 902), GHOST_A),
            'ss_belly': g(A._bands('#dfe6ee', '#c2cad4', 903), GHOST_A + 20), 'ss_fin': g(A._fin('#d4dae2', '#f2f6fa', '#a8b0bc', 904), 120),
            'ss_spike': A._fin('#2a2c34', '#4a4e5a', '#16161c', 905), 'ss_horn': A._noise('#141418', 906, 5),
            'ss_claw': A._noise('#3a3e4a', 907, 6), 'ss_mouth': A._noise('#3a1446', 908, 8), 'ss_tongue': A._noise('#9a3ac8', 909, 8),
            'ss_fang': A._noise('#f0eee6', 910, 5), 'ss_eye': A._noise('#ffe23a', 911, 6),        # (solid glowing yellow - no pupils)
            'ss_lid': g(A._scales('#a2aab4', '#868e9a', '#c2c8d0', 913), 220), 'ss_brow': A._brush('#121214', '#26262a', 914), 'ss_lash': A._noise('#08080a', 915, 2),
            'ss_flame': O._flame(916), 'ss_flame_core': Image.new('RGBA', (64, 64), (236, 250, 255, 240))}


TEXMAP = {'apo_scale': 'ss_body', 'apo_scale_dk': 'ss_body_dk', 'apo_belly': 'ss_belly', 'apo_fin': 'ss_fin', 'apo_claw': 'ss_claw',
          'apo_mouth': 'ss_mouth', 'apo_tongue': 'ss_tongue', 'apo_fang': 'ss_fang', 'apo_eye': 'ss_eye', 'apo_pupil': 'ss_eye',
          'apo_bag': 'ss_body_dk', 'apo_lash': 'ss_lash', 'apo_lid': 'ss_lid', 'apo_brow': 'ss_brow'}
DROP = {'apo_dot', 'apo_hex', 'ap_black', 'ap_emerald', 'ap_emerald_lt', 'ap_fur', 'ap_gold', 'ap_ruby', 'ap_ruby_lt'}   # (the family marks, the crown)
GLOW = {'ss_eye': 14, 'ss_flame': 15, 'ss_flame_core': 15}


# ---------------------------------------------------------------------------------------------------- models
def _tex(e):
    return {v['texture'][1:] for v in e['faces'].values()}


def _retex(els, swap=None):
    out = []
    m = dict(TEXMAP, **(swap or {}))
    for e in els:
        if _tex(e) & DROP: continue
        faces = {f: dict(v, texture='#' + m.get(v['texture'][1:], v['texture'][1:])) for f, v in e['faces'].items()}
        e2 = dict(e, faces=faces)
        g = max([GLOW.get(v['texture'][1:], 0) for v in faces.values()] + [e.get('light_emission', 0)])
        if g: e2['light_emission'] = g
        out.append(e2)
    return out


def _lean(els, k=LEAN):
    """narrow a part across (x, about its own pivot - model x 8): the brothers' bulk on a soldier's frame"""
    out = []
    for e in els:
        f, t = e['from'], e['to']
        e2 = dict(e, **{'from': [8 + (f[0] - 8) * k, f[1], f[2]], 'to': [8 + (t[0] - 8) * k, t[1], t[2]]})
        if 'rotation' in e:
            r = dict(e['rotation']); o = r['origin']; r['origin'] = [8 + (o[0] - 8) * k, o[1], o[2]]; e2['rotation'] = r
        out.append(e2)
    return out


def _spike(root, d, L, w, tex, pv):
    """one tapered spike, square in section (not a flat fin): from its root along d (unit-ish), L long, w thick at the root"""
    n = 4
    pts = [tuple(root[i] + d[i] * L * k / n for i in range(3)) for k in range(n + 1)]
    ws = [w * (1 - 0.8 * k / n) for k in range(n)]
    return chain(pts, ws, ws[0], tex, pv, UP if abs(d[1]) < 0.7 else FRONT, ext=0.15, hs=ws)


def _norm(v):
    m = math.sqrt(sum(c * c for c in v)); return tuple(c / m for c in v)


# the swept-back spikes off the back of the skull (the head's own fins are dropped - flat panels that read as sticks from behind):
# a centre row and a pair either side, rooted in the skull and swept back and up, the rearmost the longest
SPIKES = [((0, 43.2, 1.5), (0, 0.55, 0.85), 5.6, 2.2), ((0, 41.6, 5.6), (0, 0.45, 0.9), 6.8, 2.4), ((0, 38.6, 8.6), (0, 0.2, 1.0), 6.0, 2.2),
          ((3.4, 42.6, 2.2), (0.35, 0.5, 0.8), 4.8, 1.8), ((4.4, 40.2, 6.4), (0.4, 0.3, 0.86), 5.6, 1.9),
          ((-3.4, 42.6, 2.2), (-0.35, 0.5, 0.8), 4.8, 1.8), ((-4.4, 40.2, 6.4), (-0.4, 0.3, 0.86), 5.6, 1.9)]


def _crest(crest, pv):
    """a: the pale swept-back spikes; b: the same, dark, and one tall dark horn up from the crown of the head; c: no spikes -
    two big black horns curving back"""
    h = []
    if crest in ('a', 'b'):
        for root, d, L, w in SPIKES:
            if crest == 'b' and root[0] == 0 and root[2] < 3: continue            # (the horn stands there)
            h += _spike(root, _norm(d), L, w, 'ss_fin' if crest == 'a' else 'ss_spike', pv)
    if crest == 'b':
        pts = [(0, 42.6, 0.6), (0, 46.4, 0.9), (0, 49.6, 1.8), (0, 52.2, 3.4), (0, 53.6, 5.2)]
        ws = [2.8, 2.3, 1.7, 1.0]
        h += chain(pts, ws, ws[0], 'ss_horn', pv, FRONT, ext=0.15, hs=ws)
    if crest == 'c':
        for sx in (1, -1):                                  # (up from the brow, curving back over the head: a smooth arc, tapering)
            pts = []
            for k in range(7):
                t = k / 6; a = math.radians(-10 + 125 * t)
                pts.append((sx * (4.2 + 1.8 * math.sin(math.pi * t) * 0.8), 42.4 + 7.4 * math.sin(a) * (1 - 0.15 * t), 0.2 + 7.6 * (1 - math.cos(a))))
            ws = [3.0 * (1 - 0.72 * k / 6) for k in range(6)]
            h += chain(pts, ws, ws[0], 'ss_horn', pv, FRONT, ext=0.15, hs=ws)
    return h


def models():
    src = A.models()
    M = {}
    def part(name, els):
        used = sorted({t for e in els for t in _tex(e)})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    for p in ('coil', 'body', 'chest', 'tail1', 'tail2', 'tail3', 'tail4'):
        part(f'ss_{p}', _lean(_retex(src[f'apo_{p}'][1])))
    for p in ('jaw', 'armr', 'arml'):
        part(f'ss_{p}', _retex(src[f'apo_{p}'][1]))
    pv = PIVOT['head']
    for cr in CRESTS:
        for f in (None,) + FACES:
            els = [e for e in src[f'apo_head_x{_AFACE[f]}' if f else 'apo_head'][1] if 'apo_fin' not in _tex(e)]
            part(f'ss_head_{cr}' + (f'_x{f}' if f else ''), _retex(els) + _crest(cr, pv))
    # the flame: a little soul fire on the tail's tip (Omega's, small - where his brother carries the mace)
    pv = PIVOT['flame']; c = (2.75, 2.4, 55.4)
    fl = [seg((2.75, 3.0, 53.6), (2.75, 3.0, 54.8), 1.6, 1.6, 'ss_body_dk', pv, UP)]
    fl += chain([c, (c[0], c[1] + 2.6, c[2]), (c[0] + 0.3, c[1] + 5.0, c[2] - 0.2)], [1.6, 0.8], 1.6, 'ss_flame_core', pv, FRONT, hs=[1.6, 0.8])
    rnd = random.Random(960)
    for ring, (r, h, w, n) in enumerate(((2.2, 6.0, 1.6, 7), (1.4, 8.5, 1.2, 4))):
        for i in range(n):
            a = math.radians(360 * i / n + 23 * ring); ca, sa = math.cos(a), math.sin(a); hh = h * (0.8 + 0.4 * rnd.random())
            pts = [(c[0] + r * ca, c[1] - 0.4, c[2] + r * sa), (c[0] + 1.05 * r * ca, c[1] + 0.4 * hh, c[2] + 1.05 * r * sa),
                   (c[0] + 0.3 * r * ca + rnd.uniform(-0.5, 0.5), c[1] + hh, c[2] + 0.3 * r * sa)]
            fl += chain(pts, [w, 0.5 * w], w * 0.8, 'ss_flame', pv, (ca, 0.0, sa), ext=0.2, hs=[w * 0.8, w * 0.4])
    for k in range(3):
        x, z = c[0] + rnd.uniform(-1.2, 1.2), c[2] + rnd.uniform(-1.2, 1.2); y = c[1] + 9.0 + 1.3 * k
        fl.append(el((x - 0.3, y, z - 0.3), (x + 0.3, y + 0.7, z + 0.3), 'ss_flame', pv, ('y', 45, (x, y, z))))
    for e in fl:
        g = max(GLOW.get(t, 0) for t in _tex(e))
        if g: e['light_emission'] = g
    part('ss_flame', fl)
    return M


# ---------------------------------------------------------------------------------------------------- poses
# As the brothers': coil/body/chest/head +x leans forward (the head nods down), +y turns to his left; jaw +x opens; arms -x
# forward/up, -z (right) / +z (left) out to the side; the tail +x lifts it, +y swings it to his right.
def P(**kw):
    return kw


HOVER = 6.0                                     # (spirits: they float)
CURL = dict(tail1=qs(('x', 30), ('y', -30)), tail2=qs(('x', 34), ('y', -20)), tail3=qs(('x', 30), ('y', -10)), tail4=qs(('x', 24)))     # (the tail curled up beside him, the flame held aloft)
POSES = {
    # idle: bobbing, a lazy cackle - jaw hanging, tongue out; the tail curling up beside him (a/b)
    'idle_a': P(_off=(0, HOVER, 0), body=qs(('x', -2)), chest=qs(('x', 6)), head=qs(('x', 6), ('z', -6)), jaw=qs(('x', 18)),
                armr=qs(('x', -34), ('z', -16)), arml=qs(('x', -40), ('z', 16)), **CURL),
    'idle_b': P(_off=(0, HOVER + 1.6, 0), body=qs(('x', 0)), chest=qs(('x', 8)), head=qs(('x', 2), ('y', 10), ('z', 4)), jaw=qs(('x', 14)),
                armr=qs(('x', -44), ('z', -12)), arml=qs(('x', -30), ('z', 20)),
                tail1=qs(('x', 26), ('y', -20)), tail2=qs(('x', 36), ('y', -12)), tail3=qs(('x', 34)), tail4=qs(('x', 28))),
    # float (on the move): streaming forward and low, the tail rippling out behind
    'float_a': P(_off=(0, HOVER + 0.6, 0), coil=qs(('y', 8)), body=qs(('x', 26), ('y', -8)), chest=qs(('x', 12)), head=qs(('x', -30), ('y', -6)), jaw=qs(('x', 10)),
                 armr=qs(('x', 10), ('z', -10)), arml=qs(('x', 20), ('z', 10)), tail1=qs(('x', -4), ('y', -24)), tail2=qs(('y', 30)), tail3=qs(('y', 26)), tail4=qs(('y', 12))),
    'float_b': P(_off=(0, HOVER + 1.6, 0), coil=qs(('y', -8)), body=qs(('x', 26), ('y', 8)), chest=qs(('x', 12)), head=qs(('x', -30), ('y', 6)), jaw=qs(('x', 10)),
                 armr=qs(('x', 20), ('z', -10)), arml=qs(('x', 10), ('z', 10)), tail1=qs(('x', -4), ('y', 24)), tail2=qs(('y', -30)), tail3=qs(('y', -26)), tail4=qs(('y', -12))),
    # the cackle: head thrown back, maw wide, claws up and grasping
    'cackle': P(_off=(0, HOVER + 1.0, 0), body=qs(('x', -10)), chest=qs(('x', -10)), head=qs(('x', -30)), jaw=qs(('x', 44)),
                armr=qs(('x', -120), ('z', -34)), arml=qs(('x', -110), ('z', 40)), tail1=qs(('x', 30), ('y', 20)), tail2=qs(('x', 30)), tail3=qs(('x', 30)), tail4=qs(('x', 20))),
    # the grin: mouth shut on a smug half-lidded smirk, claws steepled, head cocked (plotting)
    'grin': P(_face='grin', _off=(0, HOVER, 0), chest=qs(('x', 6), ('y', -8)), head=qs(('x', 8), ('z', 14), ('y', -12)), jaw=qs(('x', 2)),
              armr=qs(('x', -70), ('z', 30)), arml=qs(('x', -70), ('z', -30)), tail1=qs(('x', 6), ('y', 40)), tail2=qs(('y', 40)), tail3=qs(('y', 40)), tail4=qs(('y', 30))),
    # sneak: low and hunched, coiled to strike, claws together - creeping up behind you
    'sneak': P(_face='grin', _off=(0, HOVER - 3.0, 0), body=qs(('x', 34)), chest=qs(('x', 20)), head=qs(('x', -40), ('y', 12)), jaw=qs(('x', 4)),
               armr=qs(('x', -60), ('z', 20)), arml=qs(('x', -60), ('z', -20)), tail1=qs(('y', -14)), tail2=qs(('y', 20)), tail3=qs(('y', 14)), tail4=I),
    # boo!: rearing up tall - arms flung wide, eyes wide, maw wide
    'boo': P(_face='shriek', _off=(0, HOVER + 3.0, 0), body=qs(('x', -12)), chest=qs(('x', -8)), head=qs(('x', -14)), jaw=qs(('x', 50)),
             armr=qs(('x', -90), ('z', -80)), arml=qs(('x', -90), ('z', 80)), tail1=qs(('x', 40)), tail2=qs(('x', 30)), tail3=qs(('x', 20)), tail4=qs(('x', 10))),
    # the swipe (attack): wound up, then raked across
    'swipe_up': P(_off=(0, HOVER, 0), body=qs(('x', 6), ('y', -18)), chest=qs(('y', -20), ('x', 4)), head=qs(('y', 12)), jaw=qs(('x', 26)),
                  armr=qs(('x', -130), ('z', -50)), arml=qs(('x', -30), ('z', 36)), **CURL),
    'swipe': P(_off=(0, HOVER - 0.4, 0), body=qs(('x', 18), ('y', 20)), chest=qs(('y', 22), ('x', 10)), head=qs(('y', -16), ('x', -20)), jaw=qs(('x', 30)),
               armr=qs(('x', -80), ('z', 16)), arml=qs(('x', -40), ('z', 40)), tail1=qs(('x', 20), ('y', -24)), tail2=qs(('x', 26), ('y', -10)), tail3=qs(('x', 28)), tail4=qs(('x', 24))),
    # the bite: a lunge, the snout thrust forward, maw gaping
    'lunge': P(_face='shriek', _off=(0, HOVER - 1.0, -4.0), body=qs(('x', 40)), chest=qs(('x', 20)), head=qs(('x', -44)), jaw=qs(('x', 54)),
               armr=qs(('x', -80), ('z', -20)), arml=qs(('x', -80), ('z', 20)), tail1=qs(('x', -10)), tail2=qs(('x', -6)), tail3=I, tail4=I),
    # the soul spit: the tail whipped up over the head and the flame flicked forward (the game throws a little fireball)
    'flick_up': P(_off=(0, HOVER, 0), body=qs(('x', -10)), chest=qs(('x', -4)), head=qs(('x', -6)), jaw=qs(('x', 20)),
                  armr=qs(('x', -40), ('z', -30)), arml=qs(('x', -40), ('z', 30)), tail1=qs(('x', 60), ('y', 16)), tail2=qs(('x', 50)), tail3=qs(('x', 30)), tail4=qs(('x', 20))),
    'flick': P(_off=(0, HOVER - 0.4, 0), body=qs(('x', 20)), chest=qs(('x', 14)), head=qs(('x', -18)), jaw=qs(('x', 34)),
               armr=qs(('x', -50), ('z', -36)), arml=qs(('x', -50), ('z', 36)), tail1=qs(('x', 76), ('y', 24)), tail2=qs(('x', 56), ('y', 14)), tail3=qs(('x', 50)), tail4=qs(('x', 40))),
    # hurt, and fading into wisps (beaten): reeling back, then slumping over the coil
    'hurt': P(_face='hurt', _off=(0, HOVER + 0.8, 1.0), body=qs(('x', -20), ('z', 10)), chest=qs(('x', -12), ('z', 8)), head=qs(('x', -20), ('z', 14)), jaw=qs(('x', 30)),
              armr=qs(('x', -40), ('z', -60)), arml=qs(('x', -40), ('z', 60)), tail1=qs(('x', 20), ('y', 20)), tail2=qs(('y', 20)), tail3=qs(('y', 20)), tail4=qs(('y', 10))),
    'fade': P(_face='blink', _off=(0, 0.6, 0), body=qs(('x', 28), ('z', -8)), chest=qs(('x', 20), ('z', -6)), head=qs(('x', 8), ('z', -12)), jaw=qs(('x', 8)),
              armr=qs(('x', 20), ('z', -8)), arml=qs(('x', 28), ('z', 10)), tail1=qs(('y', -20)), tail2=qs(('y', -24)), tail3=qs(('y', -18)), tail4=qs(('y', -18))),
    # saluting their king (soldiers once - and they still mean it, mostly)
    'salute': P(_face='grin', _off=(0, HOVER + 0.4, 0), body=qs(('x', -4)), chest=qs(('x', -2)), head=qs(('x', -6)), jaw=qs(('x', 2)),
                armr=qs(('x', -150), ('z', -10), ('y', -30)), arml=qs(('x', -6), ('z', 8)), tail1=qs(('x', -4)), tail2=qs(('x', 4)), tail3=I, tail4=I),
}


def _upright(pose, tilt=6.0):
    """fire rises: the flame's own turn undoes everything the coil and tail have done to it"""
    q = solve(PIVOT, PARENT, dict(pose, flame=I))['tail4'][0]
    return qmul((-q[0], -q[1], -q[2], q[3]), qs(('x', tilt)))


POSES['float_m'] = mid(POSES['float_a'], POSES['float_b'])
for _p in POSES.values():
    _p['flame'] = _upright(_p)
DRAFT = ['idle_a', 'float_a', 'cackle', 'grin', 'sneak', 'boo', 'swipe_up', 'swipe', 'lunge', 'flick', 'hurt', 'fade', 'salute']
ANIMS = {'idle': [('idle_a', 14), ('idle_b', 14), ('idle_a', 14)],
         'float': [('float_a', 6), ('float_m', 6), ('float_b', 6), ('float_m', 6), ('float_a', 6)],
         'cackle': [('idle_a', 6), ('cackle', 6), ('idle_b', 4), ('cackle', 4), ('idle_a', 6)],
         'sneak_boo': [('sneak', 12), ('sneak', 10), ('boo', 3), ('boo', 10), ('cackle', 8), ('idle_a', 8)],
         'swipe': [('idle_a', 6), ('swipe_up', 6), ('swipe', 3), ('idle_a', 6)],
         'lunge': [('idle_a', 6), ('sneak', 6), ('lunge', 3), ('idle_a', 8)],
         'flick': [('idle_a', 6), ('flick_up', 8), ('flick', 3), ('idle_a', 8)],
         'fade': [('hurt', 4), ('hurt', 8), ('fade', 14), ('fade', 8)],
         'salute': [('idle_a', 8), ('salute', 8), ('salute', 14), ('idle_a', 8)]}
