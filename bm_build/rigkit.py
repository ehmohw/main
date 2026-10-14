"""2.76: a shared rig kit - one item model per part, parts parented in a tree, poses given as each part's own rotation.

Design units as in phase57_art / phase79_art: feet at y=0, facing -z, his right is +x; each part's joint sits at model
(8, 8, 8). A pose is {part: local rotation (display frame quaternion), '_off': (x, y, z) root shift in design units}.
solve() walks the tree: a child turns with its parent and its joint is carried round with it, so a pose only says how
each joint bends - the arm swings with the torso, the mace stays on the end of the tail. It returns, per part, the
display transformation (left_rotation, translation in design units) for a display standing at the part's rest joint.
"""
import math

I = (0.0, 0.0, 0.0, 1.0)


def qa(axis, deg):
    s, c = math.sin(math.radians(deg) / 2), math.cos(math.radians(deg) / 2)
    return (s if axis == 'x' else 0.0, s if axis == 'y' else 0.0, s if axis == 'z' else 0.0, c)


def qmul(a, b):
    ax, ay, az, aw = a; bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def qs(*rots):
    """a rotation from (axis, degrees) pairs, applied in order"""
    q = I
    for ax, d in rots:
        q = qmul(q, qa(ax, d))
    return q


def qrot(q, v):
    x, y, z, w = q
    cx = y * v[2] - z * v[1] + w * v[0]; cy = z * v[0] - x * v[2] + w * v[1]; cz = x * v[1] - y * v[0] + w * v[2]
    return (v[0] + 2 * (y * cz - z * cy), v[1] + 2 * (z * cx - x * cz), v[2] + 2 * (x * cy - y * cx))


D = lambda p: (-p[0], p[1], -p[2])          # design -> display frame (his right is display -x, his front display +z)


def order(parents):
    out, seen = [], set()
    def visit(p):
        if p in seen: return
        if parents.get(p): visit(parents[p])
        seen.add(p); out.append(p)
    for p in parents: visit(p)
    return out


def solve(pivots, parents, pose):
    """-> {part: (rotation, translation (display frame, design units))}"""
    off = D(pose.get('_off', (0.0, 0.0, 0.0)))
    world, out = {}, {}
    for p in order(parents):
        q = pose.get(p, I); par = parents.get(p)
        if par is None:
            Q, W = q, tuple(D(pivots[p])[i] + off[i] for i in range(3))
        else:
            Qp, Wp = world[par]
            d = tuple(D(pivots[p])[i] - D(pivots[par])[i] for i in range(3))
            r = qrot(Qp, d)
            Q, W = qmul(Qp, q), tuple(Wp[i] + r[i] for i in range(3))
        world[p] = (Q, W)
        out[p] = (Q, tuple(W[i] - D(pivots[p])[i] for i in range(3)))
    return out


def transform(els, fn):
    """re-place a part's elements (model units) through fn(point) - a scale/shift about some origin"""
    out = []
    for e in els:
        e = dict(e, **{'from': [round(v, 4) for v in fn(e['from'])], 'to': [round(v, 4) for v in fn(e['to'])]})
        if 'rotation' in e:
            e['rotation'] = dict(e['rotation'], origin=[round(v, 4) for v in fn(e['rotation']['origin'])])
        out.append(e)
    return out


def shrink(els, k):
    """built at full size, kept inside the model box: scaled 1/k about the joint (show the part at k times the scale)"""
    return transform(els, lambda v: [8 + (c - 8) / k for c in v])


def render(scene, rig, pose, at=(0.0, 0.0, 0.0), scale=1.0, suffix='', yaw=0.0):
    """draw a posed rig into a tools.render Scene (a display per part standing at its rest joint, as in the game)"""
    draw(scene, rig, solve(rig.PIVOT, rig.PARENT, pose), pose, at, scale, suffix, yaw)


def blend(xa, xb, t):
    """between two solved poses as the game moves its displays: each part's rotation slerped, its translation lerped"""
    out = {}
    for p in xa:
        (qa_, ta), (qb, tb) = xa[p], xb.get(p, xa[p])
        if sum(u * v for u, v in zip(qa_, qb)) < 0: qb = tuple(-v for v in qb)
        q = tuple(u * (1 - t) + v * t for u, v in zip(qa_, qb)); n = math.sqrt(sum(v * v for v in q))
        out[p] = (tuple(v / n for v in q), tuple(u * (1 - t) + v * t for u, v in zip(ta, tb)))
    return out


def draw(scene, rig, xf, pose, at=(0.0, 0.0, 0.0), scale=1.0, suffix='', yaw=0.0):
    """draw solved part transforms (solve(), or a blend() of two) - pose only names the models and what's hidden"""
    U = scale / 16
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    for p in rig.PARTS:
        if p not in xf or (rig.HIDDEN(p, pose) if hasattr(rig, 'HIDDEN') else False): continue
        q, t = xf[p]
        dp = D(rig.PIVOT[p])
        wx, wz = dp[0] * U, dp[2] * U
        pos = (at[0] + wx * cy - wz * sy, at[1] + dp[1] * U, at[2] + wx * sy + wz * cy)
        k = rig.PART_K.get(p, 1.0) if hasattr(rig, 'PART_K') else 1.0
        name = rig.model_name(p, pose, suffix) if hasattr(rig, 'model_name') else f'{rig.PREFIX}{p}{suffix}'
        scene.display(f'bm:item/{name}', pos=pos, yaw=yaw, translation=(t[0] * U, t[1] * U, t[2] * U), scale=scale * k, left=tuple(q))


# ---------------------------------------------------------------------------------------------------- shapes
# (26.x: a model element may turn on all three axes - {"origin", "x", "y", "z"}, composed Rz Ry Rx like the game's rotationZYX -
# so a box can lie along any line: limbs, coils, claws, blades and fins follow curves instead of stepping)
def euler(R):
    """a rotation matrix (rows) -> the element's (x, y, z) degrees, R = Rz Ry Rx"""
    b = math.asin(max(-1.0, min(1.0, -R[2][0])))
    if abs(math.cos(b)) > 1e-6:
        a = math.atan2(R[2][1], R[2][2]); c = math.atan2(R[1][0], R[0][0])
    else:
        a = math.atan2(-R[1][2], R[1][1]); c = 0.0
    return tuple(round(math.degrees(v), 3) for v in (a, b, c))


def el(fr, to, tex, piv, rot=None, uv=None, faces=None, light=0, shift=None):
    """an element in design units -> model units (the joint at 8, 8, 8). rot: (axis, angle, origin) or ((x, y, z), origin).
    shift: (du, dv) moves every face's window on the texture, so neighbouring boxes don't repeat the same patch"""
    off = [8 - piv[i] for i in range(3)]
    f = [round(fr[i] + off[i], 4) for i in range(3)]; t = [round(to[i] + off[i], 4) for i in range(3)]
    w, h, d = to[0] - fr[0], to[1] - fr[1], to[2] - fr[2]
    sz = {'north': (w, h), 'south': (w, h), 'east': (d, h), 'west': (d, h), 'up': (w, d), 'down': (w, d)}
    out = {}
    for fc in (faces or ('north', 'south', 'east', 'west', 'up', 'down')):
        a, b = (round(min(16, max(v, 0.25)), 4) for v in sz[fc])
        u0, v0 = (0, 0) if not shift else (round((shift[0] % 1) * (16 - a), 3), round((shift[1] % 1) * (16 - b), 3))
        out[fc] = {'uv': (uv or {}).get(fc) or [u0, v0, round(u0 + a, 4), round(v0 + b, 4)], 'texture': '#' + tex}
    e = {'from': f, 'to': t, 'faces': out}
    if rot:
        org = [round(rot[-1][i] + off[i], 4) for i in range(3)]
        if isinstance(rot[0], str): e['rotation'] = {'origin': org, 'axis': rot[0], 'angle': round(rot[1], 3)}
        else:
            ax, ay, az = rot[0]
            e['rotation'] = {'origin': org, 'x': ax, 'y': ay, 'z': az}
    if light: e['light_emission'] = light
    return e


def _sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def _add(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def _mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)
def _dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _unit(a):
    n = math.sqrt(_dot(a, a)); return (a[0] / n, a[1] / n, a[2] / n)


def frame(z, up):
    """a right-handed frame (x, y, z): z along the given line, y as near `up` as it can be"""
    z = _unit(z); x = _cross(up, z)
    if _dot(x, x) < 1e-9: x = _cross((0.0, 0.0, -1.0) if abs(z[2]) < 0.9 else (0.0, 1.0, 0.0), z)
    x = _unit(x); return x, _cross(z, x), z


def seg(A, B, w, h, tex, piv, up=(0.0, 1.0, 0.0), ext=0.0, light=0, shift=None):
    """a box w (across) by h (toward `up`) running from A to B (design units), ext longer at each end"""
    x, y, z = frame(_sub(B, A), up)
    L = math.sqrt(_dot(_sub(B, A), _sub(B, A))) / 2 + ext; m = _mul(_add(A, B), 0.5)
    R = [[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]]
    ang = euler(R)
    fr, to = (m[0] - w / 2, m[1] - h / 2, m[2] - L), (m[0] + w / 2, m[1] + h / 2, m[2] + L)
    return el(fr, to, tex, piv, None if max(abs(v) for v in ang) < 1e-3 else (ang, m), light=light, shift=shift)


def chain(pts, ws, h, tex, piv, up=(0.0, 1.0, 0.0), ext=0.25, hs=None):
    """boxes along a polyline - widths ws (one per span, or a (start, end) pair to taper), heights h (or hs per span)"""
    n = len(pts) - 1
    if isinstance(ws, tuple) and len(ws) == 2 and n != 2: ws = [ws[0] + (ws[1] - ws[0]) * i / max(1, n - 1) for i in range(n)]
    return [seg(pts[i], pts[i + 1], ws[i], (hs[i] if hs else h), tex, piv, up, ext, shift=(0.37 * i, 0.61 * i)) for i in range(n)]


def point(rig, pose, part, p, at=(0.0, 0.0, 0.0), scale=1.0, yaw=0.0):
    """where a design point carried by `part` stands in the world (blocks) in this pose - a rider's seat, a hand's grip"""
    q, t = solve(rig.PIVOT, rig.PARENT, pose)[part]
    pv = D(rig.PIVOT[part]); W = tuple(t[i] + pv[i] for i in range(3))
    r = qrot(q, tuple(D(p)[i] - pv[i] for i in range(3)))
    v = tuple((W[i] + r[i]) * scale / 16 for i in range(3))
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return (at[0] + v[0] * cy - v[2] * sy, at[1] + v[1], at[2] + v[0] * sy + v[2] * cy)
