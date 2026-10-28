"""2.96: THE COUNT, of the Gutter Gentry, as a follower - the boss's own look (phase88_art: a pale blue gumdrop of a blob in tiers,
grumpy - furrowed brows, round empty white spectacle eyes, a frown with two little fangs - drooping side lobes, a blocky black top hat
with a red band, stick legs in pointed shoes, and his cane) on a rigkit rig at follower size. His face is its own plate on the
blob's front (the 'head' part: a model per mood). The CHIBI costume ('_c'): a rounder, bigger blob with big soft spectacle eyes and
a little pout, the hat perched on top, chunky little legs.

Rig: body (the blob, its joint 9 units up), head (the face plate, on the body's joint), the hat on top, the cane at his left lobe,
the legs (standing on the ground - they don't lean with the blob). Design units: feet at y=0, facing -z, his right is +x."""
import math
import phase88_art as G88
import gentry_base as GB
from gentry_base import P, I
from rigkit import qs

PREFIX = 'gc_'
RIG_SCALE = 0.70                       # (27.5 units, hat to toes: about 1.2 blocks)
J = G88.CNT_J
PIVOT = {'body': (0, J, 0), 'head': (0, J, 0), 'hat': (0, J + 10.5, -0.3), 'cane': (-11.3, J + 2.0, -1.0),
         'legr': (3.4, J - 0.5, 0), 'legl': (-3.4, J - 0.5, 0)}
PARENT = {'body': None, 'head': 'body', 'hat': 'body', 'cane': 'body', 'legr': None, 'legl': None}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('blink', 'happy', 'angry', 'surprised')
SWIM_FRAMES = 8
CHIBI = '_c'
FACE_AT, FACE_SPAN = (0, 0.56, 0), 0.62
CK = (1.12, 1.12, 1.12)                  # (the chibi blob's growth; the hat rides up on top of it)
HAT_UP = round(10.6 * (CK[1] - 1) + 0.2, 3)


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
_PORT = ('gnt_blob', 'gnt_blob_dk', 'gnt_black', 'gnt_hat', 'gnt_band', 'gnt_pipe')


def textures():
    T = GB.ported_textures(PREFIX, _PORT)
    for ch, sfx in ((False, ''), (True, CHIBI)):
        T[f'gc_face{sfx}'] = GB.count_face(None, ch)
        for k in FACES:
            T[f'gc_face_{k}{sfx}'] = GB.count_face(k, ch)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _body():
    """the blob - its front now plain (the face is the head's plate, just in front of it)"""
    els = GB.port(PREFIX, G88.count_body())
    return [dict(e, faces={f: (dict(v, texture='#gc_blob', uv=[0, 0, 16, 7]) if v['texture'] == '#gc_count_face' else v) for f, v in e['faces'].items()})
            for e in els]


def _face(face=None, chibi=False):
    tex = (f'gc_face_{face}' if face else 'gc_face') + (CHIBI if chibi else '')
    e = G88._box((-9, 0, -6.56), (9, 7, -6.5), 'gnt_blob', faces=('north',), uv={'north': G88.UV['gnt_count_face']})
    e['faces']['north']['texture'] = '#' + tex
    return GB.scale([e], CK) if chibi else [e]


def models():
    M = {}; part = GB.builder(M)
    body, hat, cane = _body(), GB.port(PREFIX, G88.count_hat()), GB.port(PREFIX, G88.count_cane())
    lr, ll = GB.port(PREFIX, G88.count_leg()), GB.port(PREFIX, G88._mirror(G88.count_leg()))
    part('gc_body', body); part('gc_hat', hat); part('gc_cane', cane); part('gc_legr', lr); part('gc_legl', ll)
    part('gc_body_c', GB.scale(body, CK)); part('gc_hat_c', GB.scale(hat, (0.9, 0.9, 0.9), (0, HAT_UP, 0)))
    part('gc_cane_c', GB.scale(cane, (1.0, 0.85, 1.0))); part('gc_legr_c', GB.scale(lr, (1.5, 1.0, 1.3))); part('gc_legl_c', GB.scale(ll, (1.5, 1.0, 1.3)))
    for ch, sfx in ((False, ''), (True, CHIBI)):
        part(f'gc_head{sfx}', _face(None, ch))
        for f in FACES:
            part(f'gc_head_x{f}{sfx}', _face(f, ch))
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (the boss's own: lean, sway, bob; the legs; the hat lifted (hat_up) and tilted; the cane swung forward (cane) and out (cane_out))
def cnt(lean=0.0, sway=0.0, bob=0.0, leg_r=0.0, leg_l=0.0, hat_up=0.0, hat_tilt=0.0, hat_fwd=0.0, cane=0.0, cane_out=0.0, turn=0.0,
        face=None, drop=0.0, **kw):
    p = P(body=qs(('y', turn), ('z', -sway), ('x', lean)), hat=qs(('z', -hat_tilt), ('x', hat_fwd)),
          cane=qs(('z', cane_out), ('x', -cane)), legr=qs(('y', turn), ('x', -leg_r)), legl=qs(('y', turn), ('x', -leg_l)),
          _off=(0, drop, 0), _o_body=(0, bob, 0), _o_hat=(0, hat_up, 0), **kw)
    if face: p['_face'] = face
    return p


POSES = {
    'idle_a': cnt(),
    'idle_b': cnt(bob=0.3, hat_up=0.3, cane=4),
    'jump': cnt(bob=1.0, leg_r=30, leg_l=26, hat_up=2.0, cane=-20, cane_out=20),
    # sitting: settled down on his bottom tier, his stick legs out in front; or with his hat tipped down over his eyes, napping
    'sit_a': cnt(drop=-6.6, leg_r=84, leg_l=84, cane=-30, cane_out=30),
    'sit_b': cnt(drop=-6.6, lean=-8, leg_r=80, leg_l=88, hat_up=-2.6, hat_fwd=28, cane=-40, cane_out=40, face='blink'),
    'hurt': cnt(lean=-12, sway=5, hat_up=2.2, hat_tilt=14, cane=-30, cane_out=24, face='surprised'),
    'tired': cnt(lean=14, bob=-0.8, hat_up=-0.6, hat_tilt=-10, cane=12, face='blink'),
    'happy': cnt(bob=1.2, hat_up=1.6, hat_tilt=-8, cane=-20, cane_out=36, face='happy'),
    # THE CANE: drawn back - and swung round at it
    'cane_up': cnt(turn=16, lean=-4, cane=-46, cane_out=26, face='angry'),
    'cane': cnt(turn=-18, lean=8, cane=96, cane_out=6, face='angry'),
    # TIP OF THE HAT: the hat lifted and tilted, a little bow
    'tip_hat': cnt(hat_up=4.5, hat_tilt=-26, lean=10, face='happy'),
}
_W = [dict(sway=3, leg_r=22, leg_l=-22, cane=14, lean=3), dict(bob=0.6, lean=3, cane=4),
      dict(sway=-3, leg_r=-22, leg_l=22, cane=-8, lean=3), dict(bob=0.6, lean=3, cane=4)]
_R = [dict(lean=10, leg_r=38, leg_l=-38, cane=-26, cane_out=10), dict(lean=10, bob=1.2, hat_up=1.2, cane=-30, cane_out=12),
      dict(lean=10, leg_r=-38, leg_l=38, cane=-26, cane_out=10), dict(lean=10, bob=1.2, hat_up=1.2, cane=-30, cane_out=12)]
for _k in range(4):
    POSES[f'walk_{_k}'] = cnt(**_W[_k]); POSES[f'run_{_k}'] = cnt(**_R[_k])
for _k in range(SWIM_FRAMES):                      # (afloat like a buoy, holding his hat on, kicking)
    _t = 2 * math.pi * _k / SWIM_FRAMES
    POSES[f'swim_{_k}'] = cnt(lean=8, drop=-8 + 0.5 * math.sin(_t), leg_r=40 * math.sin(_t), leg_l=-40 * math.sin(_t), cane=-60, cane_out=50,
                              hat_tilt=4 * math.sin(_t))
for _k in list(POSES):
    POSES[_k + CHIBI] = POSES[_k]
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'hurt', 'tired', 'happy', 'cane_up', 'cane', 'tip_hat', 'swim_2']
