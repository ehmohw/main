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
    U = scale / 16
    xf = solve(rig.PIVOT, rig.PARENT, pose)
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
