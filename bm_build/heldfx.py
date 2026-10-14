"""2.78: a 3D model held the way vanilla holds a flat item - its hand transforms worked out from vanilla's own.

A vanilla item sprite is held by a corner and points up its diagonal: a sword's blade, a crossbow's bolt. Given a model's
tip direction (out along the blade or barrel), its up direction and where the hand closes on it, each hand's transform puts
that grip where vanilla's grip goes and turns the tip along vanilla's diagonal, the model's up along the sprite's upper edge.
(Minecraft: vertex = T + Rx Ry Rz . S . (p/16 - 0.5).)"""
import math
import numpy as np

HANDHELD = {'thirdperson_righthand': ([0, -90, 55], [0, 4.0, 0.5], 0.85), 'thirdperson_lefthand': ([0, 90, -55], [0, 4.0, 0.5], 0.85),
            'firstperson_righthand': ([0, -90, 25], [1.13, 3.2, 1.13], 0.68), 'firstperson_lefthand': ([0, 90, -25], [1.13, 3.2, 1.13], 0.68)}
CROSSBOW = {'thirdperson_righthand': ([-90, 0, -60], [2, 0.1, -3], 0.9), 'thirdperson_lefthand': ([-90, 0, 30], [2, 0.1, -3], 0.9),
            'firstperson_righthand': ([-90, 0, -55], [1.13, 3.2, 1.13], 0.68), 'firstperson_lefthand': ([-90, 0, 35], [1.13, 3.2, 1.13], 0.68)}
GRIP = {'handheld': (3, 3, 8), 'crossbow': (4, 4, 8)}          # where the hand closes on each sprite


def _rx(a): return np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
def _ry(a): return np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
def _rz(a): return np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])


def eul(r):
    return _rx(math.radians(r[0])) @ _ry(math.radians(r[1])) @ _rz(math.radians(r[2]))


def to_eul(R):
    """R = Rx(a) Ry(b) Rz(c) -> degrees (a, b, c)"""
    b = math.asin(max(-1.0, min(1.0, R[0][2])))
    if abs(math.cos(b)) > 1e-6:
        a, c = math.atan2(-R[1][2], R[2][2]), math.atan2(-R[0][1], R[0][0])
    else:
        a, c = math.atan2(R[2][1], R[1][1]), 0.0
    return [round(math.degrees(v), 2) for v in (a, b, c)]


def frame(tip, up):
    """Q: the model's (tip, up, tip x up) onto the sprite's (diagonal, upper edge, normal)"""
    u = np.array(tip, float); u /= np.linalg.norm(u)
    y = np.array(up, float); y -= u * (y @ u); y /= np.linalg.norm(y)
    m = np.column_stack([u, y, np.cross(u, y)])
    d = np.array([1, 1, 0]) / math.sqrt(2); p = np.array([-1, 1, 0]) / math.sqrt(2)
    s = np.column_stack([d, p, np.cross(d, p)])
    return s @ m.T


def display(tip, up, grip, bounds, style='handheld', hand=0.8, first=0.6, gui=0.6, ground=0.4, fixed=0.6):
    """the display block: the four hands from the vanilla preset, gui / ground / fixed centred on the model (bounds: (lo, hi) 3-vectors)"""
    Q = frame(tip, up)
    preset = {'handheld': HANDHELD, 'crossbow': CROSSBOW}[style]
    G = np.array(grip, float) / 16 - 0.5
    gs = np.array(GRIP[style], float) / 16 - 0.5
    out = {}
    for k, (vr, vt, vs) in preset.items():
        Rv = eul(vr); Rm = Rv @ Q
        s = first if k.startswith('first') else hand
        gv = np.array(vt) / 16 + Rv @ (vs * gs)
        r = to_eul(Rm)
        assert np.allclose(eul(r), Rm, atol=1e-4), (k, r)
        t = (gv - Rm @ (s * G)) * 16
        out[k] = {'rotation': r, 'translation': [round(float(v), 3) for v in t], 'scale': [s] * 3}
    C = (np.array(bounds[0], float) + np.array(bounds[1], float)) / 2 / 16 - 0.5
    for k, R, s in (('gui', Q, gui), ('ground', Q, ground), ('fixed', _ry(math.pi) @ Q, fixed)):
        r = to_eul(R)
        out[k] = {'rotation': r, 'translation': [round(float(v), 3) for v in -(eul(r) @ (s * C)) * 16], 'scale': [s] * 3}
    for k, d in out.items():
        assert all(abs(v) <= 80 for v in d['translation']), (k, d)
    return out


def bounds(model):
    els = model['elements']
    lo = [min(min(e['from'][i], e['to'][i]) for e in els) for i in range(3)]
    hi = [max(max(e['from'][i], e['to'][i]) for e in els) for i in range(3)]
    return lo, hi
