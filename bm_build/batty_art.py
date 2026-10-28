"""2.96: BATTY, of the Gutter Gentry, as a follower - the boss's own look (phase88_art: the big square navy head with stepped ears and
a little grey pipe-cap, heavy-lidded sleepy yellow eyes, the gritted toothy grin under a pink nose, the spiky collar, the banded grey
belly, brown wings on blocky finger bones, dangling clawed feet) on a rigkit rig at follower size: he hovers, flapping, his feet
clear of the ground. A face per mood; the CHIBI costume ('_c'): a big round head with big shiny eyes and a small fanged smile, a
little body and wings.

Rig: body (the neck joint; the torso, legs and tail web hang below it), head, the two wings at the shoulders.
Design units: feet at y=0 (hovering a little over it), facing -z, his right is +x."""
import math
import phase88_art as G88
import gentry_base as GB
from gentry_base import P, I
from rigkit import qs

PREFIX = 'gb_'
RIG_SCALE = 0.44                       # (head-top to dangling toes ~33 units: about 0.9 blocks hovering)
PIVOT = {'body': (0, 18.0, 0), 'head': (0, 18.2, 0), 'wingr': (3.6, 16.4, 0.6), 'wingl': (-3.6, 16.4, 0.6)}
PARENT = {'body': None, 'head': 'body', 'wingr': 'body', 'wingl': 'body'}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('blink', 'happy', 'angry', 'surprised')
SWIM_FRAMES = 8
CHIBI = '_c'
FACE_AT, FACE_SPAN = (0, 0.66, 0), 0.5           # (the preview's close-up of the face)


def HIDDEN(p, pose):
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
_PORT = ('gnt_fur', 'gnt_fur_dk', 'gnt_fur_lt', 'gnt_bat_chest', 'gnt_wing', 'gnt_tail', 'gnt_pipe', 'gnt_pipe_dk', 'gnt_claw')


def textures():
    T = GB.ported_textures(PREFIX, _PORT)
    for ch, sfx in ((False, ''), (True, CHIBI)):
        T[f'gb_bat_face{sfx}'] = GB.bat_face(None, ch); T[f'gb_bat_grin{sfx}'] = GB.bat_grin(None, ch)
        for k in FACES:
            T[f'gb_bat_face_{k}{sfx}'] = GB.bat_face(k, ch)
        T[f'gb_bat_grin_happy{sfx}'] = GB.bat_grin('happy', ch)
    return T


# ---------------------------------------------------------------------------------------------------- models
def _head(face=None, chibi=False):
    sfx = CHIBI if chibi else ''
    els = GB.port(PREFIX, G88.bat_head())
    els = GB.with_tex(els, 'gb_bat_face', f'gb_bat_face_{face}{sfx}' if face else f'gb_bat_face{sfx}')
    els = GB.with_tex(els, 'gb_bat_grin', f'gb_bat_grin_happy{sfx}' if face == 'happy' else f'gb_bat_grin{sfx}')
    return GB.scale(els, (1.38, 1.38, 1.38)) if chibi else els


def models():
    M = {}; part = GB.builder(M)
    body, wr = GB.port(PREFIX, G88.bat_body()), GB.port(PREFIX, G88.bat_wing())
    wl = GB.port(PREFIX, G88._mirror(G88.bat_wing()))
    for ch, sfx in ((False, ''), (True, CHIBI)):
        part(f'gb_head{sfx}', _head(None, ch))
        for k in FACES:
            part(f'gb_head_x{k}{sfx}', _head(k, ch))
    part('gb_body', body); part('gb_wingr', wr); part('gb_wingl', wl)
    part('gb_body_c', GB.scale(body, (0.72, 0.68, 0.72)))
    part('gb_wingr_c', GB.scale(wr, (0.72, 0.72, 0.72))); part('gb_wingl_c', GB.scale(wl, (0.72, 0.72, 0.72)))
    return M


# ---------------------------------------------------------------------------------------------------- poses
# (the boss's own gaits: pitch = the body tilted forward, flap = wings up (+) / down (-), sweep = wings swept back, head = nods down)
def bat(pitch=10.0, flap=0.0, sweep=0.0, head=0.0, bob=0.0, roll=0.0, face=None, lift=0.0, **kw):
    w = lambda sx: qs(('z', -sx * flap), ('y', -sx * sweep))
    p = P(body=qs(('z', -roll), ('x', pitch)), head=qs(('x', -pitch * 0.6 + head)), wingr=w(1), wingl=w(-1), _off=(0, bob + lift, 0), **kw)
    if face: p['_face'] = face
    return p


def _flap(k, n, pitch, up, down, head=0.0, bob=0.6, **kw):
    t = math.cos(2 * math.pi * k / n)
    return bat(pitch=pitch, flap=down + (up - down) * (t + 1) / 2, head=head, bob=bob * t, **kw)


POSES = {
    'idle_a': bat(pitch=12, flap=38, bob=0.6),
    'idle_b': bat(pitch=12, flap=-30, bob=-0.6),
    'jump': bat(pitch=70, flap=12, sweep=40, head=-22),
    # sitting: perched on the ground, his wings folded down his sides like a cloak; dozing, or peering about
    'sit_a': bat(pitch=0, flap=-42, sweep=82, head=6, lift=-1.6),
    'sit_b': bat(pitch=-4, flap=-38, sweep=86, head=14, lift=-1.6, roll=8, face='blink'),
    'hurt': bat(pitch=-22, flap=64, sweep=-10, head=-20, face='surprised'),
    'tired': bat(pitch=26, flap=-34, sweep=70, head=18, lift=-1.0, face='blink'),
    'happy': bat(pitch=4, flap=56, head=-12, bob=1.4, face='happy'),
    # BITE: up and back - then down on it, jaws first
    'bite_up': bat(pitch=18, flap=52, head=-26, face='angry'),
    'bite': bat(pitch=42, flap=-42, head=26, face='angry'),
    # SCREECH: reared back, wings spread wide, head thrown up
    'screech': bat(pitch=-12, flap=8, sweep=-30, head=-38, face='angry'),
    # WING FLAP: a great beat - a gust off the wings
    'wing_flap': bat(pitch=-6, flap=80, sweep=-18, head=-8, bob=1.0, face='angry'),
}
for _k in range(4):
    POSES[f'walk_{_k}'] = _flap(_k, 4, 30, 44, -40)
    POSES[f'run_{_k}'] = _flap(_k, 4, 55, 48, -46, head=-14)
for _k in range(SWIM_FRAMES):                      # (paddling along the surface with his wings, nose up)
    _t = 2 * math.pi * _k / SWIM_FRAMES
    POSES[f'swim_{_k}'] = bat(pitch=50, flap=10 + 40 * math.sin(_t), sweep=20 * math.cos(_t), head=-30, lift=-6 + 0.4 * math.sin(2 * _t))
for _k in list(POSES):                             # (the chibi costume shares every pose)
    POSES[_k + CHIBI] = POSES[_k]
DRAFT = ['idle_a', 'idle_b', 'walk_1', 'run_1', 'jump', 'sit_a', 'sit_b', 'hurt', 'tired', 'happy', 'bite_up', 'bite', 'screech', 'wing_flap', 'swim_2']
