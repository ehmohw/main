"""2.94k: GAITS THAT TOUCH THE GROUND - two-bone limbs solved (numerically, through rigkit.point) so a foot lands where it's
told: planted on the ground through its stance, sliding back as the body passes over it, then lifted forward in an arc.

    contact(art, part)                      the design point a limb's lower part stands on (the middle of its lowest corners)
    reach(art, pose, upper, lower, mk, target, ranges)
                                            the two bends (degrees) that put that point at target (y, z) - mk(a, b) makes the
                                            pose's {upper: q, lower: q} from them
    track(phase, duty, z0, stride, lift)    where a foot is at this point of its cycle: (y, z)
Design units, rig space (point's frame: +y up, +z the rig's front)."""
import itertools
import math

import rigkit as RK

_CORNERS = {}


def _rot(c, r):
    if not r or not r.get('angle'):
        return c
    a = math.radians(r['angle']); o = r['origin']
    v = [c[i] - o[i] for i in range(3)]; ca, sa = math.cos(a), math.sin(a)
    if r['axis'] == 'x':
        v = [v[0], v[1] * ca - v[2] * sa, v[1] * sa + v[2] * ca]
    elif r['axis'] == 'y':
        v = [v[0] * ca + v[2] * sa, v[1], -v[0] * sa + v[2] * ca]
    else:
        v = [v[0] * ca - v[1] * sa, v[0] * sa + v[1] * ca, v[2]]
    return [v[i] + o[i] for i in range(3)]


def corners(art, part):
    """every corner of a part's model, back in design units (a part's model is centred on its joint: model = design - joint + 8)"""
    if part not in _CORNERS:
        m = art.models()[art.PREFIX + part]
        els = m[1] if isinstance(m, tuple) else m
        pv = art.PIVOT[part]
        out = []
        for e in els:
            for c in itertools.product(*[(e['from'][i], e['to'][i]) for i in range(3)]):
                c = _rot(list(c), e.get('rotation'))
                out.append(tuple(c[i] - 8 + pv[i] for i in range(3)))
        _CORNERS[part] = out
    return _CORNERS[part]


def contact(art, part, band=0.6):
    cs = corners(art, part)
    lo = min(c[1] for c in cs)
    pts = [c for c in cs if c[1] <= lo + band]
    return tuple(sum(c[i] for c in pts) / len(pts) for i in range(3))


def lowest(art, pose, part):
    return min(RK.point(art, pose, part, c, scale=16)[1] for c in corners(art, part))


def reach(art, pose, upper, lower, mk, target, ranges):
    """coarse-to-fine search of the two bends; the pose's other joints as they are"""
    cp = contact(art, lower)
    ty, tz = target

    def err(a, b):
        p = RK.point(art, dict(pose, **mk(a, b)), lower, cp, scale=16)
        return (p[1] - ty) ** 2 + (p[2] - tz) ** 2
    (a0, a1), (b0, b1) = ranges
    best = None
    step_a, step_b = (a1 - a0) / 24, (b1 - b0) / 24
    ca, cb = (a0 + a1) / 2, (b0 + b1) / 2
    for _ in range(5):
        cand = [(err(a, b), a, b) for a in [ca + step_a * i for i in range(-12, 13)] for b in [cb + step_b * j for j in range(-12, 13)]
                if a0 <= a <= a1 and b0 <= b <= b1]
        best = min(cand + ([best] if best else []))
        _e, ca, cb = best
        step_a, step_b = step_a / 4, step_b / 4
    return best[1], best[2], best[0] ** 0.5


def track(phase, duty, z0, stride, lift):
    """a foot through its cycle (phase 0..1): on the ground for `duty` of it, from z0+stride/2 back to z0-stride/2; then up and
    forward again in an arc (a smooth lift, highest mid-swing)"""
    phase %= 1.0
    if phase < duty:
        u = phase / duty
        return 0.0, z0 + stride / 2 - stride * u
    u = (phase - duty) / (1 - duty)
    s = 0.5 - 0.5 * math.cos(math.pi * u)                 # (eased forward)
    return lift * math.sin(math.pi * u), z0 - stride / 2 + stride * s
