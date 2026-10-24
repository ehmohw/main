"""The Arachno-Lantern (2.87) as a mount: the Scorching Arachno-Lantern's own kind (phase82_art), small enough to ride - a carved
pumpkin about as wide as a horse, lit from inside and burning at both corners of its grin, its purple tongue lolling, carried on
eight long black legs knuckled high above it. Blocky like its parent: square tiers for the pumpkin, the face painted square-cut on
its flat front (the parent's own face), square legs.

A rigkit rig: body (the hub the legs grow from, hidden inside the pumpkin), head (the pumpkin - a model per expression: carved and
dull, carved and blazing, or dark and asleep), the tongue, and eight legs (each one bent piece - up to a high knuckle, down to a
point - swinging at the hip). Design units: feet at y=0, facing -z, its right is +x."""
import math
from PIL import Image

from phase57_art import hexc
import phase82_art as BOSS
from rigkit import qs, el, chain

PREFIX = 'ln_'
RIG_SCALE = 1.0
HIP_Y = 21.0
YAWS = (54, 86, 116, 146)                 # (each leg's direction, degrees round from straight ahead)
LEGS = [f'leg{"r" if s > 0 else "l"}{i}' for s in (1, -1) for i in range(4)]


def _dir(s, i):
    a = math.radians(YAWS[i])
    return (s * math.sin(a), -math.cos(a))


PIVOT = {'body': (0, 18.0, 0), 'head': (0, 20.0, 0), 'tongue': (0, 22.6, -10.2),
         **{f'leg{"r" if s > 0 else "l"}{i}': (_dir(s, i)[0] * 4.6, HIP_Y, _dir(s, i)[1] * 4.6) for s in (1, -1) for i in range(4)}}
PARENT = {'body': None, 'head': 'body', 'tongue': 'head', **{k: 'body' for k in LEGS}}
PARTS = tuple(PIVOT)
PART_K = {}
FACES = ('glare', 'shut')
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)


def HIDDEN(p, pose):
    return False


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures (its parent's)
def _blaze(im):
    """the carved face with its fires roaring up: the dull red deep in the cuts turned to white-hot yellow"""
    im = im.copy(); px = im.load()
    swap = {hexc('#2a0c06')[:3]: hexc('#c04a10'), hexc('#120406')[:3]: hexc('#ff7a14'), hexc('#1c0607')[:3]: hexc('#ffc030'), hexc('#3a0c0a')[:3]: hexc('#fff4a8')}
    for y in range(im.height):
        for x in range(im.width):
            c = px[x, y][:3]
            if c in swap: px[x, y] = swap[c]
    return im


def textures():
    face = BOSS._face()
    return {'ln_rind': BOSS._skin(31), 'ln_rind_top': BOSS._skin_top(), 'ln_rind_dk': BOSS._skin_dk(), 'ln_face': face, 'ln_face_glare': _blaze(face),
            'ln_face_shut': BOSS._skin(32), 'ln_flame': BOSS._flame(33), 'ln_tongue': BOSS._tongue(), 'ln_stem': BOSS._stem(), 'ln_leaf': BOSS._leaf(),
            'ln_leg': BOSS._chitin(34)}


# ---------------------------------------------------------------------------------------------------- models
def models():
    M = {}
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)
    faceuv = [0, 0, 16, 8.8]                                                     # (the parent's face plate: 40 x 22)

    # ---- the hub, where the legs grow from - (2.93c, the owner's call) no longer a black lump hanging under the pumpkin: the
    #      legs meet inside it, so the bone keeps only a speck tucked away inside the pumpkin
    pv = PIVOT['body']
    part('ln_body', [el((-1.0, 24.0, -1.0), (1.0, 25.0, 1.0), 'ln_leg', pv)])

    # ---- the pumpkin: square tiers - a dark base, the broad middle tier with the face on its front, tiers stepping in above;
    #      raised ribs down the sides and back; the stem hooking over and its leaf; the fires at the corners of the grin
    pv = PIVOT['head']
    def head(face=None):
        ftex = 'ln_face' if face is None else f'ln_face_{face}'
        h = [el((-7.5, 19.2, -6.5), (7.5, 20.6, 6.5), 'ln_rind_dk', pv),
             el((-9.6, 20.4, -8.6), (9.6, 22.2, 8.6), 'ln_rind', pv, shift=(0.3, 0.1)),
             el((-11.0, 22.0, -10.0), (11.0, 34.1, 10.0), 'ln_rind', pv, shift=(0.0, 0.2)),
             el((-11.0, 22.0, -10.02), (11.0, 34.1, -10.0), ftex, pv, faces=('north',), uv={'north': faceuv}),
             el((-9.6, 33.9, -8.6), (9.6, 35.4, 8.6), 'ln_rind', pv, shift=(0.5, 0.4)),
             el((-6.6, 35.2, -5.6), (6.6, 36.2, 5.6), 'ln_rind_top', pv)]
        for e in h[1:]:                                                          # (the tops of the tiers: the ribs as a star)
            if 'up' in e['faces'] and e['faces']['up']['texture'] == '#ln_rind': e['faces']['up']['texture'] = '#ln_rind_top'
        for sx in (-1, 1):                                                       # the ribs, raised strips down the sides...
            for zc in (-4.4, 4.4):
                h.append(el((sx * 11.0 - (0.0 if sx > 0 else 0.7), 24.0, zc - 2.0), (sx * 11.0 + (0.7 if sx > 0 else 0.0), 32.0, zc + 2.0), 'ln_rind', pv, shift=(0.7, 0.2)))
        for xc in (-4.4, 4.4):                                                   # ...and the back
            h.append(el((xc - 2.0, 24.0, 10.0), (xc + 2.0, 32.0, 10.7), 'ln_rind', pv, shift=(0.4, 0.2)))
        # the stem: thick and ribbed, stepping over and hooking down; its leaf
        h += [el((-1.8, 36.0, -1.8), (1.8, 38.6, 1.8), 'ln_stem', pv), el((-1.5, 38.4, -1.2), (1.5, 40.4, 2.0), 'ln_stem', pv),
              el((-1.3, 39.6, 1.8), (1.3, 41.2, 4.4), 'ln_stem', pv), el((-1.0, 38.6, 4.0), (1.0, 40.2, 5.6), 'ln_stem', pv),
              el((1.6, 36.1, -3.0), (7.4, 36.6, 2.6), 'ln_leaf', pv)]
        # the fires at the corners of the grin: square licks out and up, yellow at the root, red at the tips (glowing)
        for sx in (-1, 1):
            for k, (x0, x1, y0, y1, z0, z1, v0, v1) in enumerate(((9.6, 11.6, 23.0, 25.2, -11.2, -9.6, 12.8, 16.0), (10.8, 12.8, 24.6, 27.4, -11.0, -9.8, 9.6, 12.8),
                                                                  (11.8, 13.6, 26.8, 29.6, -10.8, -9.8, 6.4, 9.6), (12.6, 13.9, 29.0, 31.6, -10.6, -9.9, 3.2, 6.4),
                                                                  (13.0, 13.9, 31.0, 33.0, -10.4, -10.0, 0.0, 3.2))):
                a, b = sorted((sx * x0, sx * x1))
                e = el((a, y0, z0), (b, y1, z1), 'ln_flame', pv, light=15)
                for f in e['faces'].values():
                    f['uv'] = [0, v0, 16, v1]
                h.append(e)
        return h
    part('ln_head', head())
    for fc in FACES:
        part(f'ln_head_x{fc}', head(fc))

    # ---- the tongue: out of the grin's lower lip, lolling down and curling at the tip
    pv = PIVOT['tongue']; tx, ty, tz = pv
    part('ln_tongue', [el((tx - 1.6, ty - 1.0, tz - 2.4), (tx + 1.6, ty + 0.6, tz + 0.4), 'ln_tongue', pv),
                       el((tx - 1.7, ty - 3.8, tz - 4.0), (tx + 1.7, ty - 0.9, tz - 1.6), 'ln_tongue', pv),
                       el((tx - 1.5, ty - 6.4, tz - 5.2), (tx + 1.5, ty - 3.6, tz - 3.0), 'ln_tongue', pv),
                       el((tx - 1.3, ty - 7.8, tz - 5.4), (tx + 1.3, ty - 6.2, tz - 2.4), 'ln_tongue', pv)])

    # ---- the legs: from the hip up and out to a high knuckle (well above the pumpkin's middle), then down and out to a point
    #      on the ground - square chitin, stepping thinner, a knob at each joint and a few square bristles
    for s in (1, -1):
        for i in range(4):
            name = f'leg{"r" if s > 0 else "l"}{i}'
            pv = PIVOT[name]
            dx, dz = _dir(s, i)
            P_ = lambda r, y: (dx * r, y, dz * r)
            hip, knee, ankle, foot = P_(4.6, HIP_Y), P_(14.5, 40.0), P_(20.0, 15.0), P_(22.0, 0.0)
            L = [el((hip[0] - 1.4, hip[1] - 1.4, hip[2] - 1.4), (hip[0] + 1.4, hip[1] + 1.4, hip[2] + 1.4), 'ln_leg', pv)]
            L += chain([hip, knee], [1.9], 1.9, 'ln_leg', pv, UP, ext=0.4)
            L += [el((knee[0] - 1.3, knee[1] - 1.2, knee[2] - 1.3), (knee[0] + 1.3, knee[1] + 1.4, knee[2] + 1.3), 'ln_leg', pv)]
            L += chain([knee, ankle, foot], (1.6, 0.8), 1.4, 'ln_leg', pv, UP, ext=0.3)
            for t, side in ((0.35, 1), (0.6, -1)):                               # bristles on the long downward segment
                bx, by, bz = (knee[k] + (ankle[k] - knee[k]) * t for k in range(3))
                L.append(el((bx - 0.25, by, bz - 0.25), (bx + 0.25, by + 0.6, bz + 0.25), 'ln_leg', pv))
                L += chain([(bx, by, bz), (bx + dx * 1.2 * side + dz * 0.6, by + 0.9, bz + dz * 1.2 * side - dx * 0.6)], [0.3], 0.3, 'ln_leg', pv, UP, ext=0.0)
            part(f'ln_{name}', L)
    return M


# ---------------------------------------------------------------------------------------------------- poses
def leg(s, i, swing=0.0, lift=0.0, spread=0.0):
    """a leg's own turn at the hip: swing (degrees, +: forward), lift (+: the foot up and out; spread the same, for a wider stance).
    The lift turns about the line across the leg (out x up, in the display frame), then the swing about the vertical."""
    a = math.radians(YAWS[i])
    ax, az = -math.cos(a), -s * math.sin(a)
    k = math.radians(lift + spread) / 2
    ql = (ax * math.sin(k), 0.0, az * math.sin(k), math.cos(k))
    return _qmul(qs(('y', swing * s)), ql)


def _qmul(a, b):
    from rigkit import qmul
    return qmul(a, b)


def P(**kw):
    return kw


def legs(fn):
    return {f'leg{"r" if s > 0 else "l"}{i}': leg(s, i, **fn(s, i)) for s in (1, -1) for i in range(4)}


# (the wave gait: alternating tetrapods - R0, L1, R2, L3 step together; then L0, R1, L2, R3)
def _set(s, i):
    return (i + (0 if s > 0 else 1)) % 2
WALK_N, RUN_N = 8, 6
WALK_AMP, WALK_LIFT, RUN_AMP, RUN_LIFT = 13.0, 12.0, 14.0, 16.0


def _walk(k, n=4, amp=18.0, lift=14.0):
    ph = 2 * math.pi * k / n
    return legs(lambda s, i: dict(swing=amp * math.sin(ph + math.pi * _set(s, i)), lift=max(0.0, lift * math.cos(ph + math.pi * _set(s, i)))))


POSES = {
    'idle_a': P(**legs(lambda s, i: {}), head=qs(('x', 0))),
    'idle_b': P(_off=(0, -0.6, 0), **legs(lambda s, i: dict(spread=4)), head=qs(('x', 4), ('z', 3)), tongue=qs(('x', 12))),
    # (2.89: eight walk frames and six run frames, with a shorter stride - the legs no longer scissor through their neighbours;
    #  the body bobs twice a cycle, as each tetrapod plants)
    **{f'walk_{k}': P(_off=(0, 0.05 + 0.25 * math.cos(4 * math.pi * k / WALK_N), 0), head=qs(('z', 2 * math.sin(2 * math.pi * k / WALK_N))),
                      tongue=qs(('x', 2 + 6 * math.cos(4 * math.pi * k / WALK_N))), **_walk(k, WALK_N, WALK_AMP, WALK_LIFT)) for k in range(WALK_N)},
    **{f'run_{k}': P(_off=(0, 0.4 + 0.4 * math.cos(4 * math.pi * k / RUN_N), 0), head=qs(('x', 6)), tongue=qs(('x', -20)),
                     **_walk(k, RUN_N, RUN_AMP, RUN_LIFT)) for k in range(RUN_N)},
    'jump': P(_off=(0, 2.0, 0), head=qs(('x', -8)), tongue=qs(('x', -30)), **legs(lambda s, i: dict(lift=-18, swing=(10, 4, -4, -10)[i]))),
    # STOMP: the front pair rears up high - and comes down
    'rear': P(_off=(0, 2.0, 0), body=qs(('x', -14)), head=qs(('x', -6)), tongue=qs(('x', -30)),
              **legs(lambda s, i: dict(lift=(46, 18, 0, 0)[i], swing=(8, 4, -5, -5)[i]))),        # (2.94k: up and out - swung 22 forward they ran through the pumpkin)
    'stomp': P(_off=(0, -1.6, 0), body=qs(('x', 10)), head=qs(('x', 4)), tongue=qs(('x', 20)), **legs(lambda s, i: dict(spread=(8, 4, 0, 0)[i], swing=(16, 8, 0, 0)[i]))),
    # TONGUE LASH: it leans in, and the tongue shoots out
    'lash_a': P(_face='glare', body=qs(('x', 6)), head=qs(('x', 6)), tongue=qs(('x', 25))),
    'lash_b': P(_face='glare', _off=(0, -0.6, 0), body=qs(('x', 14)), head=qs(('x', 4)), tongue=qs(('x', -80))),
    # THE GLARE / EMBER RAIN: it throws its head back and the fires roar up
    'flare': P(_face='glare', _off=(0, 0.8, 0), body=qs(('x', -10)), head=qs(('x', -8)), tongue=qs(('x', -20)), **legs(lambda s, i: dict(spread=6))),
    # sitting: it folds its legs in under it and the pumpkin settles on the ground (dark, asleep on the second beat)
    'sit_a': P(_off=(0, -10.7, 0), tongue=qs(('x', 30)), **legs(lambda s, i: dict(lift=29))),
    'sit_b': P(_face='shut', _off=(0, -10.9, 0), head=qs(('z', 3)), tongue=qs(('x', 40)), **legs(lambda s, i: dict(lift=30))),
    'hurt': P(_face='glare', _off=(0, -0.8, 0), body=qs(('x', -8), ('z', 6)), head=qs(('x', -6)), tongue=qs(('x', -20)), **legs(lambda s, i: dict(spread=6))),
    'tired': P(_face='shut', _off=(0, -4.0, 0), body=qs(('x', 10)), tongue=qs(('x', 40)), **legs(lambda s, i: dict(lift=12, spread=10))),
    'wave_a': P(**legs(lambda s, i: dict(lift=(40 if s < 0 and i == 0 else 0), swing=(20 if s < 0 and i == 0 else 0)))),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                            # (it paddles like a water-strider: the legs splayed flat and sculling)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_off=(0, -12.0 + 0.5 * math.sin(2 * _p), 0), tongue=qs(('x', -10)),
                            **legs(lambda s, i: dict(lift=28, swing=20 * math.sin(_p + math.pi * _set(s, i)))))
DRAFT = ['idle_a', 'idle_b', 'walk_0', 'walk_1', 'run_0', 'jump', 'rear', 'stomp', 'lash_b', 'flare', 'sit_a', 'sit_b', 'swim_2']


# (2.93e: every material with life in it - matkit)
import matkit as _mk
textures = _mk.wrapped(textures, __name__)
