"""2.96: EGGBERT, of the Gutter Gentry, as a follower - the boss's own look (phase88_art: a stacked egg, grey-white shell with slate
spots, split by a jagged crack whose toothed halves show the black ooze core between them, two pale glowing eyes in it; ooze
dripping over the lower shell; black dripping arms with three talons; stubby black legs with clawed feet; a broken pipe on top) on
a rigkit rig at follower size. A face per mood (his eyes: the 'head' part, riding the shell). The CHIBI costume ('_c'): a rounder,
bigger egg (no pipe), big round shiny eyes, chunky little arms and legs.

Rig: body (the shell, its joint 10 units up), head (the eyes, on the body's joint), the arms at the shoulders, the legs (standing
on the ground - they don't lean with the shell). Design units: feet at y=0, facing -z, his right is +x."""
import math
import phase88_art as G88
import gentry_base as GB
from gentry_base import P, I, limb
from rigkit import qs, el

PREFIX = 'ge_'
RIG_SCALE = 0.63                       # (32.8 units, pipe to toes: about 1.3 blocks)
J = G88.EGG_J
PIVOT = {'body': (0, J, 0), 'head': (0, J, 0), 'armr': (7.6, J + 7.5, -0.5), 'arml': (-7.6, J + 7.5, -0.5),
         'legr': (3.6, J - 2.5, 0), 'legl': (-3.6, J - 2.5, 0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'legr': None, 'legl': None}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('blink', 'happy', 'angry', 'surprised')
SWIM_FRAMES = 8
CHIBI = '_c'
FACE_AT, FACE_SPAN = (0, 0.6, 0), 0.5


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
_PORT = ('gnt_shell', 'gnt_shell_b', 'gnt_shell_lo', 'gnt_shell_hi', 'gnt_goo', 'gnt_pipe', 'gnt_pipe_dk', 'gnt_claw')


def textures():
    T = GB.ported_textures(PREFIX, _PORT)
    for ch, sfx in ((False, ''), (True, CHIBI)):
        T[f'ge_eye{sfx}'] = GB.egg_eye(None, ch)
        for k in FACES:
            T[f'ge_eye_{k}{sfx}'] = GB.egg_eye(k, ch)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _eyes(face=None, chibi=False):
    """the two eyes in the crack, each at a low point of its zigzag (the big one his right, the small one his left); both show
    the picture as it is, so the glints sit the same way in both eyes (one light) - but for angry, where the left eye's picture
    is mirrored so the slant meets in the middle"""
    tex = f'ge_eye_{face}' if face else 'ge_eye'
    tex += CHIBI if chibi else ''
    pv = (0, 0, 0)
    xa, xb = G88.CRACK_X0, G88.CRACK_X0 - G88.CRACK_P
    # (a follower's face has to read at a few blocks: a little bigger and higher in the band than the boss's; the chibi's big round
    # eyes stand just proud of the shell, so its teeth don't bite into them)
    if chibi: big, small, z0 = (2.6, 2.6), (2.1, 2.1), -6.62
    else: big, small, z0 = (2.1, 2.1), (1.4, 1.4), -6.3
    yb, ys = 15.4 - J, 15.2 - J
    return [el((xa - big[0], yb - big[1], z0), (xa + big[0], yb + big[1], -5.8), tex, pv, faces=('north', 'east', 'west', 'up', 'down'),
               uv={'north': [0, 0, 16, 16]}),
            el((xb - small[0], ys - small[1], z0), (xb + small[0], ys + small[1], -5.8), tex, pv, faces=('north', 'east', 'west', 'up', 'down'),
               uv={'north': [16, 0, 0, 16] if face == 'angry' else [0, 0, 16, 16]})]


def models():
    M = {}; part = GB.builder(M)
    body = GB.port(PREFIX, G88.egg_body())
    ar, al = GB.port(PREFIX, G88.egg_arm()), GB.port(PREFIX, G88._mirror(G88.egg_arm()))
    lr, ll = GB.port(PREFIX, G88.egg_leg()), GB.port(PREFIX, G88._mirror(G88.egg_leg()))
    part('ge_body', body); part('ge_armr', ar); part('ge_arml', al); part('ge_legr', lr); part('ge_legl', ll)
    # the chibi: the egg bigger and rounder (the broken pipe left off), the limbs chunky
    cb = [e for e in body if e['from'][1] < 8 + 19.0]
    part('ge_body_c', GB.scale(cb, (1.2, 1.06, 1.2)))
    part('ge_armr_c', GB.scale(ar, (0.8, 0.8, 1.15))); part('ge_arml_c', GB.scale(al, (0.8, 0.8, 1.15)))
    part('ge_legr_c', GB.scale(lr, (1.35, 1.0, 1.25))); part('ge_legl_c', GB.scale(ll, (1.35, 1.0, 1.25)))
    for ch, sfx in ((False, ''), (True, CHIBI)):
        k = (1.2, 1.06, 1.2) if ch else (1.0, 1.0, 1.0)
        part(f'ge_head{sfx}', GB.scale(_eyes(None, ch), k, (0, 0, -0.08 if ch else 0)))
        for f in FACES:
            part(f'ge_head_x{f}{sfx}', GB.scale(_eyes(f, ch), k, (0, 0, -0.08 if ch else 0)))
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (the boss's own: lean forward, sway side to side, bob, the arms raised out (up) and swung forward (arm), the legs swung)
def egg(lean=0.0, sway=0.0, bob=0.0, arm_r=0.0, arm_l=0.0, up_r=0.0, up_l=0.0, leg_r=0.0, leg_l=0.0, turn=0.0, face=None, drop=0.0, **kw):
    p = P(body=qs(('y', turn), ('z', -sway), ('x', lean)),
          armr=qs(('z', -up_r), ('x', -arm_r)), arml=qs(('z', up_l), ('x', -arm_l)),
          legr=qs(('y', turn), ('x', -leg_r)), legl=qs(('y', turn), ('x', -leg_l)),
          _off=(0, drop, 0), _o_body=(0, bob, 0), **kw)
    if face: p['_face'] = face
    return p


POSES = {
    'idle_a': egg(up_r=6, up_l=6),
    'idle_b': egg(bob=0.4, up_r=10, up_l=10, sway=2),
    'jump': egg(lean=-6, bob=1.0, leg_r=34, leg_l=18, up_r=55, up_l=55),
    # sitting: plonked down on his lower shell, his stubby legs straight out in front; or leaning back, arms out for balance
    'sit_a': egg(drop=-4.2, leg_r=82, leg_l=78, up_r=14, up_l=14, arm_r=20, arm_l=20),
    'sit_b': egg(drop=-4.2, lean=-14, leg_r=74, leg_l=86, up_r=40, up_l=40, arm_r=-20, arm_l=-20, face='blink'),
    'hurt': egg(lean=-14, sway=6, up_r=48, up_l=48, arm_r=-24, arm_l=-24, face='surprised'),
    'tired': egg(lean=18, bob=-0.8, up_r=0, up_l=0, arm_r=8, arm_l=8, face='blink'),
    'happy': egg(lean=-6, bob=1.2, up_r=70, up_l=70, arm_r=-10, arm_l=-10, face='happy'),
    # CLAW: wound up and round - then the swipe across
    'claw_up': egg(lean=-8, turn=-14, arm_r=-62, up_r=44, arm_l=10, up_l=12, leg_r=-10, leg_l=12, face='angry'),
    'claw': egg(lean=16, turn=16, arm_r=86, up_r=12, arm_l=-20, up_l=20, leg_r=14, leg_l=-10, face='angry'),
    # GOO THROW: both arms up and back, gathering ooze - then flung forward
    'goo_throw_up': egg(lean=-12, bob=1.2, up_r=68, up_l=68, arm_r=-34, arm_l=-34, face='angry'),
    'goo_throw': egg(lean=14, up_r=20, up_l=20, arm_r=88, arm_l=88, face='angry'),
}
_W = [dict(sway=3, leg_r=24, leg_l=-24, arm_r=-14, arm_l=14, up_r=6, up_l=6), dict(bob=0.8, up_r=10, up_l=10),
      dict(sway=-3, leg_r=-24, leg_l=24, arm_r=14, arm_l=-14, up_r=6, up_l=6), dict(bob=0.8, up_r=10, up_l=10)]
_R = [dict(lean=14, sway=4, leg_r=44, leg_l=-40, arm_r=-30, arm_l=30, up_r=28, up_l=28), dict(lean=14, bob=1.5, up_r=34, up_l=34),
      dict(lean=14, sway=-4, leg_r=-40, leg_l=44, arm_r=30, arm_l=-30, up_r=28, up_l=28), dict(lean=14, bob=1.5, up_r=34, up_l=34)]
for _k in range(4):
    POSES[f'walk_{_k}'] = egg(**_W[_k]); POSES[f'run_{_k}'] = egg(**_R[_k])
for _k in range(SWIM_FRAMES):                      # (bobbing like the egg he is, paddling with his arms and kicking)
    _t = 2 * math.pi * _k / SWIM_FRAMES
    POSES[f'swim_{_k}'] = egg(lean=10, drop=-9 + 0.5 * math.sin(_t), up_r=50 + 20 * math.sin(_t), up_l=50 - 20 * math.sin(_t),
                              arm_r=30 * math.cos(_t), arm_l=-30 * math.cos(_t), leg_r=30 * math.sin(_t), leg_l=-30 * math.sin(_t))
for _k in list(POSES):
    POSES[_k + CHIBI] = POSES[_k]
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'hurt', 'tired', 'happy', 'claw_up', 'claw', 'goo_throw_up', 'goo_throw', 'swim_2']
