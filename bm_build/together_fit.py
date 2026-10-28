"""2.96c: WHERE ONE FOLLOWER SITS ON (OR LIES BY) ANOTHER - measured from the rigs themselves (phase134's figure solve and each
part's own model), so a seat follows the art: a rider's body bottom on Bender's back, a cat's paws on it, the back's rise and
fall through every pose of his (his bob). Units: blocks, in the figure's frame (feet at y 0, facing +z, at the host).
(phase234 builds the riding and the cuddle on these; phase195 publishes his bob in each pose.)"""
import functools

import numpy as np

import phase134 as P134
import creative


@functools.lru_cache(None)
def _models(A):
    return {n: {'elements': els} for n, (_tex, els) in A.models().items()}


def _pose(A, pose):
    return A.POSES[pose] if isinstance(pose, str) else pose


def bounds(A, pose):
    """{part model: (lo, hi)} - each part's box in the figure"""
    out = {}
    for mid, tr, L, R, sc in P134._rigkit(A, _pose(A, pose), A.RIG_SCALE):
        n = mid.split(':')[1]
        m = _models(A).get(n)
        if m is None or not m['elements']:
            continue
        wb = creative.world_bounds(m, creative._xform(m, tr, L, R, sc))
        if wb is not None and float(np.max(wb[1] - wb[0])) > 1e-4:
            out[n] = wb
    return out


def _body(A):
    return A.PREFIX + 'body'


@functools.lru_cache(None)
def back(pose):
    """Bender's back in a pose: the top of his body's main box, at its middle -> (y, z)"""
    import bender_art as A
    m = _models(A)[_body(A)]
    e = max(m['elements'], key=lambda e: np.prod(np.array(e['to']) - np.array(e['from'])))
    p = np.array([(e['from'][0] + e['to'][0]) / 2, e['to'][1], (e['from'][2] + e['to'][2]) / 2], float)
    for mid, tr, L, R, sc in P134._rigkit(A, _pose(A, pose), A.RIG_SCALE):
        if mid.split(':')[1] == _body(A):
            s, Rm, b = creative._xform(m, tr, L, R, sc)
            w = s * Rm @ (p / 16 - 0.5) + b
            return round(float(w[1]), 4), round(float(w[2]), 4)
    raise KeyError(pose)


def seat(A, pose, on='body'):
    """how high a rider's host sits over Bender's (idle) - its body's bottom on his back (on='body'), or its lowest point - its
    paws (on='feet')"""
    b = bounds(A, pose)
    if on == 'body':
        lo = min(v[0][1] for k, v in b.items() if k.startswith(_body(A)))
    else:
        lo = min(v[0][1] for v in b.values())
    return round(back('idle_a')[0] - float(lo) + 0.01, 3)


def bob(pose):
    """Bender's back in a pose against his idle one: (dy, dz), to the hundredth"""
    y0, z0 = back('idle_a')
    y, z = back(pose)
    return round(y - y0, 2), round(z - z0, 2)


# ---------------------------------------------------------------------------------------------------- clipping: one rig into another
def _el_frames(A, pose, off=(0, 0, 0), yaw=0.0):
    """every element of every part as (M, o, lo, hi): world = M @ (q - o) + c ... in a form both ways can use: a point q in the
    element's model space (px) maps to the world as W(q) = s Rm Re (q - o)/16 + s Rm (o/16 - .5) + b, Re its own turn about o"""
    import math
    from creative import _rx, _ry, _rz
    c, sn = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    Y = np.array([[c, 0, -sn], [0, 1, 0], [sn, 0, c]])          # (a Minecraft yaw: +yaw turns +z towards -x)
    out = []
    for mid, tr, L, R, sc in P134._rigkit(A, _pose(A, pose), A.RIG_SCALE):
        m = _models(A).get(mid.split(':')[1])
        if not m:
            continue
        s, Rm, b = creative._xform(m, tr, L, R, sc)
        for e in m['elements']:
            r = e.get('rotation')
            o = np.array(r['origin'], float) if r else np.zeros(3)
            Re = np.eye(3)
            if r and 'axis' in r:
                Re = {'x': _rx, 'y': _ry, 'z': _rz}[r['axis']](math.radians(r['angle']))
            elif r:
                Re = _rz(math.radians(r.get('z', 0))) @ _ry(math.radians(r.get('y', 0))) @ _rx(math.radians(r.get('x', 0)))
            M = Y @ (s * Rm @ Re) / 16
            base = Y @ (s * Rm @ (o / 16 - 0.5) + b) + np.array(off, float)
            lo, hi = np.minimum(e['from'], e['to']), np.maximum(e['from'], e['to'])
            if np.min(hi - lo) < 0.05:                            # (a flat face - paint, no body)
                continue
            out.append((M, o, lo, hi, base, mid))
    return out


def clips(a, b, depth=0.02, n=4, deep=False):
    """(A, pose, off, yaw) x 2 -> [(part of a, part of b, points)]: how far a's parts sink into b's (sampled n^3 a box; a point
    counts when it lies deeper than `depth` blocks inside a box of b)"""
    fa, fb = _el_frames(*a), _el_frames(*b)
    hits = {}
    for M, o, lo, hi, base, ma in fa:
        g = np.stack(np.meshgrid(*[np.linspace(lo[i], hi[i], n) for i in range(3)], indexing='ij'), -1).reshape(-1, 3)
        W = (M @ (g - o).T).T + base
        for M2, o2, lo2, hi2, base2, mb in fb:
            k = np.linalg.norm(M2[:, 0])                          # (px -> blocks)
            q = (np.linalg.inv(M2) @ (W - base2).T).T + o2
            d = depth / k
            inside = np.all((q > lo2 + d) & (q < hi2 - d), axis=1)
            if inside.any():
                key = (ma.split(':')[1], mb.split(':')[1])
                if deep:                                          # (how deep the deepest point lies, in blocks)
                    dd = np.min(np.minimum(q[inside] - lo2, hi2 - q[inside]), axis=1).max() * k
                    hits[key] = max(hits.get(key, 0), round(float(dd), 3))
                else:
                    hits[key] = hits.get(key, 0) + int(inside.sum())
    return sorted(hits.items(), key=lambda kv: -kv[1])


@functools.lru_cache(None)
def bobs():
    """every rise and fall of his back his poses have, once each: [(dy, dz)] - the first, none"""
    import bender_art as A
    out = [(0.0, 0.0)]
    for p in A.POSES:
        b = bob(p)
        if b not in out:
            out.append(b)
    return tuple(out)


def bob_index(pose):
    return bobs().index(bob(pose))
