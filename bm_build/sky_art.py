"""2.94: THE SKY BUDDIES - Sunny, Snooze, Twinkle and Nimbus, from the owner's painting (ref/sky_buddies.png). (2.94e) Each part
is a new blocky 3D model of its own, designed from the painting (sky3d.py) - boxes, painted in pixel art, like Emma - on its
own item display, floating. (2.94c's were the painting itself, sculpted into voxels; before that, flat billboarded sprites.)

THE PARTS   head (Sunny: the ball, his 3D shades, the smirk), rays (his twelve rays, a part of their own so they can spin), moon
            (Snooze, asleep), cap (Snooze's nightcap - a texture of its own, so the wardrobe can recolour it), star (Twinkle,
            grumpy), body (Nimbus, the front cloud: ":3") and back (the darker cloud behind him).
ONE JOINT   every part shares one joint - the middle of Sunny - and the layout is in the models (each part built where it sits
            round that joint, as the painting has them). A part moves on its own with rigkit's '_o_<part>' offsets (a pose's
            per-part shift, carried to its children: the cap rides the moon).
FACES       each faced part has a model per expression (sky3d draws them): the painting's own faces, and the rest in the same
            spirit.
Design units: 1 = 1/8 block at RIG_SCALE 2. LAYOUT keeps the painting's pixel coordinates: the poses' shifts are in them."""
import math
import os
import sys

from rigkit import qs

PREFIX = 'yb_'
RIG_SCALE = 2.0
HERE = os.path.dirname(os.path.abspath(__file__))
PPB = 440.0                                     # (art pixels to a block)
DU = 16.0 / RIG_SCALE / PPB                     # (design units per art pixel)
SUN_C = (271.0, 270.0)                          # (the middle of Sunny's disc in the painting: the joint)
FACED = ('head', 'moon', 'star', 'body')
# a part: its anchor in the painting (the middle of its window), where that anchor sits round the joint (on screen, in painting
# pixels: +x your right, +y down), and its depth (+ toward you)
LAYOUT = {'back': ((536, 685), None, -3.0), 'rays': (SUN_C, (0.0, 0.0), -2.0), 'head': (SUN_C, (0.0, 0.0), -1.0),
          'moon': ((857, 400), (+420.0, +10.0), 0.0), 'cap': ((965, 222), None, 0.6), 'star': ((809, 381), None, 1.2),
          'body': ((460, 690), (+190.0, +300.0), 2.0)}
FOLLOW = {'back': 'body', 'cap': 'moon', 'star': 'moon'}          # (placed as the painting has them, round their partner)
PARTS = ('body', 'head', 'rays', 'moon', 'cap', 'star', 'back')
PARENT = {'body': None, 'head': None, 'rays': 'head', 'moon': None, 'cap': 'moon', 'star': None, 'back': 'body'}
JOINT = (0.0, 14.0, 0.0)                        # (design units: the joint, over the host's feet - Sunny about head height)
PIVOT = {p: JOINT for p in PARTS}
PART_K = {}
EXPR = {'head': ('grin', 'surprised', 'hurt', 'sleepy', 'blink', 'fierce'),
        'moon': ('drowsy', 'surprised', 'hurt', 'yawn', 'happy', 'awake'),
        'star': ('smug', 'surprised', 'hurt', 'blink', 'angry', 'happy'),
        'body': ('happy', 'surprised', 'hurt', 'blink', 'angry', 'sing')}


def HIDDEN(p, pose):
    return pose.get('_hide') is not None and p in pose['_hide']


def model_name(p, pose, suffix=''):
    face = pose.get('_face_' + p) if p in FACED else None
    return f'{PREFIX}{p}{"_x" + face if face else ""}{suffix}'


EXTRA_TAGS = {p: ['bm.ybp_face'] for p in FACED}                 # (the four with faces: phase95's moods reach them all)
SWAP = FACED                                                     # (each pose sets their model: a face of its own, or back to the mood's)


def place_of(p):
    """a part's anchor round the joint, on screen (painting pixels, +x right, +y down)"""
    a, off, _z = LAYOUT[p]
    if off is not None:
        return off
    q = FOLLOW.get(p, 'moon')
    qa, qo = LAYOUT[q][0], place_of(q)
    return (qo[0] + a[0] - qa[0], qo[1] + a[1] - qa[1])


# ---------------------------------------------------------------------------------------------------- the models (sky3d)
# 2.94e: entirely new blocky 3D models, designed from the painting rather than cut from it (sky3d.py): boxes, painted in pixel
# art. Each part is built round its own middle and set where the painting has it round the joint, nested in depth.
DEPTH = {'body': 0.0, 'back': -1.75, 'head': -1.5, 'rays': -1.5, 'moon': 0.0, 'cap': 0.0, 'star': 0.9}     # (+ toward you)
_CACHE = {}


def _built(p, e=None):
    key = (p, e)
    if key not in _CACHE:
        import sky3d
        part = sky3d.BUILD[p](e) if p in FACED else sky3d.BUILD[p]()
        ox, oy = place_of(p)
        jx, jy, jz = JOINT
        tex = f'{PREFIX}{p}_{e}' if e else f'{PREFIX}{p}'
        _CACHE[key] = sky3d.build(part, tex, (jx - ox * DU, jy - oy * DU, jz - DEPTH[p]), JOINT) + (tex,)
    return _CACHE[key]


def textures():
    T = {}
    for p in PARTS:
        for e in (None,) + EXPR.get(p, ()):
            els, im, tex = _built(p, e)
            T[tex] = im
    return T


def models():
    M = {}
    for p in PARTS:
        for e in (None,) + EXPR.get(p, ()):
            els, im, tex = _built(p, e)
            M[f'{PREFIX}{p}_x{e}' if e else f'{PREFIX}{p}'] = ({tex: f'bm:block/{tex}'}, els)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def o(dx=0.0, dy=0.0):
    """a screen shift (painting pixels: +x your right, +y up) -> a design shift"""
    return (-dx * DU, dy * DU, 0.0)


def _turned(p, deg):
    """the shift that keeps a part turning about its own middle, not the shared joint: the part's middle, carried round by
    the turn, put back where it was (rigkit: a model point v is drawn at W + Q.D(v - joint))"""
    from rigkit import D, qrot
    ox, oy = place_of(p)
    c = D((-ox * DU, -oy * DU, 0.0))
    r = qrot(qs(('z', deg)), c)
    return D(tuple(c[i] - r[i] for i in range(3)))


def Q(lift=0.0, **spec):
    """a pose: lift (design units, the whole trio), then per part a face (a string) or dict(r=turn in degrees - about the
    part's own middle, on the screen's plane; o=(dx, dy) screen shift in painting pixels; f=face)"""
    out = {'_off': (0.0, lift, 0.0)}
    for p, sp in spec.items():
        if isinstance(sp, str):
            sp = {'f': sp}
        if sp.get('f'):
            out[f'_face_{p}'] = sp['f']
        sh = o(*sp.get('o', (0.0, 0.0)))
        if sp.get('r'):
            out[p] = qs(('z', sp['r']))
            if PARENT[p] is None and p != 'head':
                t = _turned(p, sp['r']); sh = tuple(sh[i] + t[i] for i in range(3))
        if any(abs(v) > 1e-9 for v in sh):
            out[f'_o_{p}'] = sh
    return out


def bob(k, n, amp=10.0, phase=0.0):
    return amp * math.sin(2 * math.pi * k / n + phase)


def drift(k, n=4, faces=None, lift=0.0, lean=0.0, trail=0.0, amp=1.0):
    """their float: each on its own beat (and leaning into a move, the small ones trailing behind)"""
    f = faces or {}
    return Q(lift + bob(k, n, 0.45 * amp),
             head=dict(o=(0, bob(k, n, 6 * amp, 0.9)), r=lean * 0.6, f=f.get('head')),
             moon=dict(o=(-trail * 0.6, bob(k, n, 9 * amp, 1.6)), r=lean + bob(k, n, 3 * amp, 2.2), f=f.get('moon')),
             star=dict(o=(bob(k, n, 5 * amp, 0.6) - trail, bob(k, n, 7 * amp, 2.6)), r=bob(k, n, 8 * amp, 1.1) + lean * 1.5, f=f.get('star')),
             body=dict(o=(bob(k, n, 6 * amp, 3.1) - trail * 0.4, bob(k, n, 5 * amp, 0.3)), r=lean * 0.4, f=f.get('body')))


POSES = {}
for _k in range(4):
    POSES[f'idle_{_k}'] = drift(_k)
POSES['idle_a'] = POSES['idle_0']
POSES['idle_b'] = drift(2, faces=dict(moon='awake', star='blink', body='happy'))            # (Snooze opens an eye; Nimbus beams)
POSES['idle_c'] = drift(1, faces=dict(head='grin', star='smug'))                            # (Sunny shows off; Twinkle unimpressed)
for _k in range(4):                                                                         # moving: leaning into it, the small ones trailing
    POSES[f'walk_{_k}'] = drift(_k, lean=-5, trail=10)
    POSES[f'run_{_k}'] = drift(_k, lean=-11, trail=34, amp=1.3, faces=dict(head='grin', star='angry'))
POSES['jump'] = Q(2.0, head='surprised', body='surprised', star='surprised', moon='surprised')
# sitting: they settle low - Nimbus a bed, Snooze curled up asleep on him, Twinkle tucked by her, Sunny dozing behind
POSES['sit_a'] = Q(-6.0, moon=dict(o=(-60, -170), r=-72), star=dict(o=(-150, -150), r=-20, f='blink'), head=dict(o=(-30, -50), f='sleepy'))
POSES['sit_b'] = Q(-6.2, moon=dict(o=(-58, -166), r=-76), star=dict(o=(-146, -146), r=-26, f='blink'), head=dict(o=(-30, -56), f='sleepy'), body='blink')
# SUNBEAM: Sunny rises, swells, glares - then the beam
POSES['beam_up'] = Q(0.5, head=dict(o=(-10, 40), r=-6, f='fierce'), star='smug')
POSES['beam'] = Q(0.5, head=dict(o=(-20, 54), r=4, f='fierce'), body='surprised', star='smug')
# STAR SHOT: Twinkle winds back - and hurls herself forward (a star of light leaves her)
POSES['shot_up'] = Q(star=dict(o=(40, 40), r=40, f='angry'))
POSES['shot'] = Q(star=dict(o=(-90, -10), r=-60, f='angry'), head='grin')
# ZAP: Nimbus puffs up, glowering - then the bolt
POSES['zap_up'] = Q(body=dict(o=(0, 26), r=-3, f='angry'))
POSES['zap'] = Q(body=dict(o=(0, -12), r=3, f='angry'), head='surprised')
# LULLABY: Snooze rocks and sings (Nimbus hums along; the others nod off)
POSES['lull_a'] = Q(moon=dict(o=(-10, 10), r=-14, f='yawn'), body='sing', star='blink', head='sleepy')
POSES['lull_b'] = Q(moon=dict(o=(10, 14), r=14, f='happy'), body='happy', star='blink', head='sleepy')
# DRIZZLE: Nimbus drifts over you, raining - the rest cheer
POSES['drizzle'] = Q(body=dict(o=(-60, 70), f='happy'), head='grin', star='happy', moon='happy')
# THE FORECAST (charged): all three rise and let everything go at once
POSES['forecast_a'] = Q(1.5, head=dict(o=(-40, 30), f='fierce'), moon=dict(o=(30, 50), f='awake'), star=dict(o=(30, 60), f='angry'), body=dict(o=(0, 40), f='angry'))
POSES['forecast_b'] = Q(2.0, head=dict(o=(-60, 60), r=8, f='fierce'), moon=dict(o=(50, 70), r=-10, f='surprised'), star=dict(o=(50, 90), r=30, f='angry'),
                        body=dict(o=(0, 70), f='angry'))
POSES['happy'] = Q(1.5, head='grin', moon='happy', star='happy', body='happy')
POSES['wave_a'] = Q(1.0, head=dict(r=10, f='grin'), moon=dict(r=-12, f='happy'), star=dict(r=20, f='smug'), body=dict(r=-3, f='happy'))
POSES['wave_b'] = Q(1.3, head=dict(r=-10, f='grin'), moon=dict(r=12, f='happy'), star=dict(r=-20, f='smug'), body=dict(r=3, f='happy'))
POSES['hurt'] = Q(-1.0, moon=dict(o=(10, 0), r=8, f='hurt'), star=dict(o=(-10, 6), r=-15, f='hurt'), head='hurt', body='hurt')
POSES['tired'] = Q(-3.0, head='sleepy', moon=dict(r=-10, f='yawn'), star='blink', body='blink')
SWIM_FRAMES = 4
for _k in range(SWIM_FRAMES):                      # (over water they bob along above it)
    POSES[f'swim_{_k}'] = drift(_k, SWIM_FRAMES, lift=2.0, faces=dict(head='surprised', body='surprised'))
# the rays' own clock: a step at a time on right_rotation (under any pose's left_rotation, so the two never fight)
SPIN = 12
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'run_1', 'sit_a', 'beam_up', 'beam', 'shot_up', 'shot', 'zap', 'lull_a', 'drizzle', 'forecast_b', 'happy', 'hurt']


if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/sky_tex'
    os.makedirs(out, exist_ok=True)
    for k, im in textures().items():
        im.save(os.path.join(out, k + '.png'))
    print(len(textures()), 'textures')
