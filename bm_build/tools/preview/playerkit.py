"""A player for previews: the vanilla humanoid (skin, the outer and inner armour layers, the elytra mesh) as the game builds it,
posed (standing, crouching, gliding), drawn straight into a tools/render Scene's face list - so a worn armour texture or an
elytra 'wings' layer can be seen on a body without a client.

Coordinates: design px (the player model's own pixels: feet at y=0, facing -z, its right +x); the player model is drawn at
0.9375 (as the game draws it), so a design px is 0.9375/16 of a block. Faces carry uv in the texture's own pixels.
Box UV (ModelPart.Cube): top (u+d, v), bottom (u+d+w, v), right side (u, v+d), front (u+d, v+d), left (u+d+w, v+d),
back (u+2d+w, v+d); every face unmirrored seen from outside. Left limbs in the armour layers are the right ones mirrored."""
import math
import numpy as np

S = 0.9375                          # (the player model's scale)
VAN = '/home/claude/mc263/client/assets/minecraft/textures'
SKIN = 'minecraft:entity/player/wide/steve'


def _rx(a): c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
def _ry(a): c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def _rz(a): c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def e2d(xr=0.0, yr=0.0, zr=0.0):
    """an entity-space part rotation (ModelPart xRot, yRot, zRot, radians: Rz Ry Rx in a y-down, x-left space) in design space"""
    return _rz(zr) @ _ry(-yr) @ _rx(-xr)


def box_faces(lo, hi, uv, wh, tw=64, th=32, mirror=False):
    """the six quads of a box (design px) with their uv (texture px): uv=(u, v), wh=(w, h, d) the uv box size"""
    (x0, y0, z0), (x1, y1, z1) = lo, hi
    u, v = uv; w, h, d = wh
    R = {
        'front': ([(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)], (u + d, v + d, u + d + w, v + d + h)),
        'back': ([(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)], (u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h)),
        'right': ([(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)], (u, v + d, u + d, v + d + h)),
        'left': ([(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)], (u + d + w, v + d, u + 2 * d + w, v + d + h)),
        'top': ([(x1, y1, z1), (x0, y1, z1), (x0, y1, z0), (x1, y1, z0)], (u + d, v, u + d + w, v + d)),
        'bottom': ([(x1, y0, z0), (x0, y0, z0), (x0, y0, z1), (x1, y0, z1)], (u + d + w, v, u + d + 2 * w, v + d)),
    }
    out = []
    for name, (q, (a, b, c, e)) in R.items():
        if mirror: q = [(-p[0], p[1], p[2]) for p in q]
        out.append((q, [(a / tw * 16, b / th * 16), (c / tw * 16, b / th * 16), (c / tw * 16, e / th * 16), (a / tw * 16, e / th * 16)]))
    return out


# the humanoid's parts: (texOffs, box size, box origin rel. to the pivot (design px, at rest), pivot)
PARTS = {
    'head': ((0, 0), (8, 8, 8), (-4, 0, -4), (0, 24, 0)),
    'body': ((16, 16), (8, 12, 4), (-4, -12, -2), (0, 24, 0)),
    'armr': ((40, 16), (4, 12, 4), (-1, -10, -2), (5, 22, 0)),
    'arml': ((40, 16), (4, 12, 4), (-3, -10, -2), (-5, 22, 0)),
    'legr': ((0, 16), (4, 12, 4), (-2, -12, -2), (1.9, 12, 0)),
    'legl': ((0, 16), (4, 12, 4), (-2, -12, -2), (-1.9, 12, 0)),
}
SKIN_UV = {'head': (0, 0), 'body': (16, 16), 'armr': (40, 16), 'arml': (32, 48), 'legr': (0, 16), 'legl': (16, 48)}
HAT_UV = {'head': (32, 0), 'body': (16, 32), 'armr': (40, 32), 'arml': (48, 48), 'legr': (0, 32), 'legl': (0, 48)}


def pose(kind='stand'):
    """{part: (rotation matrix (design), pivot (design px))}, the elytra's (xRot, zRot, yRot, y) and the whole body's turn"""
    P = {p: (np.eye(3), np.array(PARTS[p][3], float)) for p in PARTS}
    el = (0.2617994, -0.2617994, 0.0, 0.0)
    if kind == 'crouch':                                   # (HumanoidModel.setupAnim, crouching - entity y-down: design y = 24 - y)
        P['body'] = (e2d(0.5), np.array((0, 24 - 3.2, 0)))
        P['head'] = (np.eye(3), np.array((0, 24 - 4.2, 0)))
        P['armr'] = (e2d(0.4), np.array((5, 24 - 5.2, 0))); P['arml'] = (e2d(0.4), np.array((-5, 24 - 5.2, 0)))
        P['legr'] = (np.eye(3), np.array((1.9, 24 - 12.2, 4.0))); P['legl'] = (np.eye(3), np.array((-1.9, 24 - 12.2, 4.0)))
        el = (0.6981317, -0.7853982, 0.08726646, 3.0)
    if kind == 'glide':
        P['armr'] = (e2d(0, 0, 0.12), P['armr'][1]); P['arml'] = (e2d(0, 0, -0.12), P['arml'][1])
        el = (0.34906584, -math.pi / 2, 0.0, 0.0)
    return P, el


def _xf(pts, R, pivot, rest_pivot):
    return [tuple(R @ (np.array(p, float) - rest_pivot) + pivot) for p in pts]


def player(kind='stand', layers=(), wings=None, skin=True, skin_tex=SKIN):
    """-> [(quad (design px), uvs (0..16), texture id)] for the body; layers: [(texture id, 'outer'|'inner', parts)], the armour
    layers as the game draws them; wings: an elytra 'wings' texture id (drawn behind, as WingsLayer: 2 px back)"""
    P, el = pose(kind)
    out = []
    def part(p, uv, tex, g, tw, th, mirror=False):
        src = p.replace('arml', 'armr').replace('legl', 'legr') if mirror else p     # (a mirrored limb: the right one, mirrored)
        (w, h, d), o, piv = PARTS[src][1], PARTS[src][2], np.array(PARTS[src][3], float)
        lo = (piv[0] + o[0] - g, piv[1] + o[1] - g, piv[2] + o[2] - g); hi = (piv[0] + o[0] + w + g, piv[1] + o[1] + h + g, piv[2] + o[2] + d + g)
        R, pv = P[p]
        for q, uvs in box_faces(lo, hi, uv, (w, h, d), tw, th, mirror):
            out.append((_xf(q, R, pv, np.array(PARTS[p][3], float)), uvs, tex))
    if skin:
        for p in PARTS:
            part(p, SKIN_UV[p], skin_tex, 0.0, 64, 64)
            part(p, HAT_UV[p], skin_tex, 0.5 if p == 'head' else 0.25, 64, 64)
    for tex, which, parts in layers:
        g = 1.0 if which == 'outer' else 0.5
        for p in parts:
            part(p, PARTS[p][0], tex, g, 64, 32, mirror=p in ('arml', 'legl'))
    if wings:
        xr, zr, yr, y = el
        # ElytraModel's left wing: texOffs (22, 0), box (-10, 0, 0) 10 x 20 x 2 grown by 1, hinged at (5, y, 0) turned (xr, yr, zr);
        # in design px (x = -x_e, y = 24 - y_e): the box x -1..11, y -21..1 about the hinge (-5, 24 - y, 2) (WingsLayer: 2 px back)
        R = e2d(xr, yr, zr); pv = np.array((-5.0, 24.0 - y, 2.0))
        for q, uvs in box_faces((-1.0, -21.0, -1.0), (11.0, 1.0, 3.0), (22, 0), (10, 20, 2), 64, 32):
            left = [tuple(R @ np.array(p) + pv) for p in q]                        # (x_e -11..1 is design -1..11: its +x face is MC's west)
            out.append((left, uvs, wings))
            out.append(([(-p[0], p[1], p[2]) for p in left], uvs, wings))         # (the right wing: the left one mirrored)
    return out


def put(scene, faces, at=(0, 0, 0), yaw=0.0, pitch=0.0, lift=0.0):
    """into a Scene: design px -> blocks (x S/16), turned to yaw (as an entity) and pitched about the feet (gliding: 90)"""
    E = _ry(math.radians(-yaw)) @ _rx(math.radians(pitch))
    k = S / 16
    for q, uvs, tex in faces:
        # design front is -z: the game shows an entity at yaw 0 facing +z - a turn of 180 about y, as an item display's model
        pts = [tuple(E @ (_ry(math.pi) @ (np.array(p) * k)) + np.array(at) + np.array((0, lift, 0))) for p in q]
        scene.faces.append((pts, uvs, tex, True, None))
