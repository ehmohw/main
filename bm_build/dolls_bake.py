"""2.78a: the follower dolls as true miniatures - each one baked from that follower's own model.

The figurines (phase134.figures: every follower's real parts at rest, the game's own transforms) are read back from the built
resource pack, part by part, and every element of every part is carried through its display's transform into one item
model - its real textures, its real face. On the way each part is pushed into chibi proportions, Emma's doll's: the head and
everything on it grows about the neck, the body shrinks about the hips, the legs shorten from the ground up - so the doll is
the follower, big-headed and small. Then the whole is fitted to the Emma doll's frame (feet at y 0, about 18 units tall,
facing north) so they stand together as a set.

An element keeps its exact shape: a uniformly scaled, turned box is still a box, turned (26.x: an element may turn on all
three axes), so nothing is approximated but the faces' auto-uvs, which are written out from where each element was."""
import json, math, os
import numpy as np

HEIGHT = 18.0                       # (units; Emma's doll stands about 18.6 with her ribbon)
HEAD = ('head', 'face', 'eyes', 'jaw', 'hat', 'hair', 'crown', 'helm')          # (a part's name past its prefix starts with one of these)
LEGS = ('leg', 'foot', 'boot')
WEAPON = ('trident', 'spear', 'scythe', 'harpoon', 'gun', 'mace', 'tend')    # (not counted in the doll's height: it would only shrink him)
TINY = 0.12                         # (an element thinner than this in every direction, once shrunk, is dropped - a speck the eye can't find)


def _rx(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def _ry(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def _rz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _quat(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _euler(R):
    """R = Rz Ry Rx -> (x, y, z) degrees (as rigkit.euler)"""
    b = math.asin(max(-1.0, min(1.0, -R[2][0])))
    if abs(math.cos(b)) > 1e-6:
        a = math.atan2(R[2][1], R[2][2]); c = math.atan2(R[1][0], R[0][0])
    else:
        a = math.atan2(-R[1][2], R[1][1]); c = 0.0
    return math.degrees(a), math.degrees(b), math.degrees(c)


def _el_rot(r):
    if not r: return np.eye(3), None
    o = np.array(r['origin'], dtype=float)
    if 'axis' in r: return {'x': _rx, 'y': _ry, 'z': _rz}[r['axis']](math.radians(r['angle'])), o
    return _rz(math.radians(r.get('z', 0))) @ _ry(math.radians(r.get('y', 0))) @ _rx(math.radians(r.get('x', 0))), o


def _auto_uv(face, f, t):
    """the uv the game would give a face without one, from where its element is"""
    x1, y1, z1 = f; x2, y2, z2 = t
    return {'north': [16 - x2, 16 - y2, 16 - x1, 16 - y1], 'south': [x1, 16 - y2, x2, 16 - y1], 'east': [16 - z2, 16 - y2, 16 - z1, 16 - y1],
            'west': [z1, 16 - y2, z2, 16 - y1], 'up': [x1, z1, x2, z2], 'down': [x1, 16 - z2, x2, 16 - z1]}[face]


def load_model(rp, mid):
    """a model by id (bm:x -> its item model), its parent chain's elements and textures merged as the game would"""
    ns, path = mid.split(':', 1)
    if '/' not in path: path = 'item/' + path
    p = os.path.join(rp, 'assets', ns, 'models', path + '.json')
    m = json.load(open(p))
    if 'parent' in m and 'elements' not in m:
        base = load_model(rp, m['parent'] if ':' in m['parent'] else 'minecraft:' + m['parent'])
        tex = dict(base.get('textures', {})); tex.update(m.get('textures', {}))
        m = dict(base, **{k: v for k, v in m.items() if k != 'parent'}); m['textures'] = tex
    return m


def _token(model):
    n = model.split(':')[-1]
    return n.split('_', 1)[1] if '_' in n else n


def group(model):
    t = _token(model)
    if t.startswith(LEGS): return 'legs'
    if t.startswith(HEAD): return 'head'
    return 'body'


def bake(rp, parts, kh=1.55, kb=0.82, kl=0.62, groups=None, neck=None, hip=None, height=HEIGHT, flip=False, ground=0.0, width=15.0):
    """parts: phase134's [(model, translation, left, right, scale)] in blocks -> (textures, elements) of one doll model.
    groups: {model: 'head'|'body'|'legs'} to override the guess by name; neck/hip: heights (blocks) of the joints the head
    grows from and the legs shorten to (default: the lowest head part's joint, the highest leg part's)."""
    RyPI = _ry(math.pi)
    G = {m: (groups or {}).get(m, group(m)) for m, *_ in parts}
    if neck is None:
        hs = [t[1] for m, t, *_ in parts if G[m] == 'head']
        neck = min(hs) if hs else None
    if hip is None:
        ls = [t[1] for m, t, *_ in parts if G[m] == 'legs']
        hip = max(ls) if ls else None
    # the chibi warp, per group, on world points (uniform about a point, then moved so the pieces still meet)
    hip0 = hip if hip is not None else ground
    hip1 = ground + (hip0 - ground) * kl
    neck1 = None if neck is None else hip1 + (neck - hip0) * kb
    gnd = np.array([0, ground, 0.0])
    def warp(g):
        if g == 'legs': return kl, gnd, gnd                                                      # (about the ground)
        if g == 'head' and neck is not None: return kh, np.array([0, neck, 0.0]), np.array([0, neck1, 0.0])
        return kb, np.array([0, hip0, 0.0]), np.array([0, hip1, 0.0])
    raw, textures = [], {}
    for i, (mid, tr, L, R, sc) in enumerate(parts):
        m = load_model(rp, mid)
        tx = m.get('textures', {})
        d = m.get('display', {}).get('fixed', {})
        dr = d.get('rotation', [0, 0, 0]); dt = np.array(d.get('translation', [0, 0, 0])) / 16; ds = d.get('scale', [1, 1, 1])
        assert abs(ds[0] - ds[1]) < 1e-6 and abs(ds[0] - ds[2]) < 1e-6, (mid, ds)
        Dm = _rx(math.radians(dr[0])) @ _ry(math.radians(dr[1])) @ _rz(math.radians(dr[2]))
        Q = _quat(L) @ _quat(R)
        k, c0, c1 = warp(G[mid])
        A = k * sc * Q @ RyPI @ Dm * ds[0]                      # (the linear part, model units -> blocks, per 16)
        def world(p):
            v = (np.array(p, dtype=float) / 16 - 0.5) * ds[0]
            v = Dm @ v + dt
            v = RyPI @ v
            w = sc * Q @ v + np.array(tr)
            return c1 + k * (w - c0)
        def res(t):
            n = 0
            while t.startswith('#') and n < 9: t = tx.get(t[1:], t); n += 1
            return t
        for e in m.get('elements', []):
            Me, o = _el_rot(e.get('rotation'))
            f, t = np.array(e['from'], dtype=float), np.array(e['to'], dtype=float)
            if o is None: o = (f + t) / 2
            faces = {}
            for fn, fc in e.get('faces', {}).items():
                tex = res(fc.get('texture', '#missing'))
                if tex.startswith('#'): continue
                key = f'p{i}_{tex.split(":")[-1].replace("/", "_")}'
                textures[key] = tex if ':' in tex else 'minecraft:' + tex
                fc2 = dict(fc, texture='#' + key)
                if 'uv' not in fc2: fc2['uv'] = _auto_uv(fn, e['from'], e['to'])
                fc2.pop('cullface', None)
                faces[fn] = fc2
            if not faces: continue
            raw.append((world(o), A, Me, f - o, t - o, faces, e, _token(mid).startswith(WEAPON)))
    # fit: the whole to the doll's frame - feet on y 0, centred, HEIGHT tall (the world points, blocks, -> model units)
    pts = []
    for q, A, Me, a, b, _f, _e, wpn in raw:
        if wpn: continue
        for x in (a[0], b[0]):
            for y in (a[1], b[1]):
                for z in (a[2], b[2]):
                    pts.append(q + A @ (Me @ np.array([x, y, z])) / 16)
    pts = np.array(pts); lo, hi = pts.min(0), pts.max(0)
    S = min(height / ((hi[1] - lo[1]) * 16), width / (max(hi[0] - lo[0], hi[2] - lo[2]) * 16))   # (as tall as the set - or as wide as a doll may be)
    cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
    def to_model(w):                                          # (world, blocks -> doll model units; the doll faces north as the dolls do)
        v = np.array([w[0] - cx, w[1] - lo[1], w[2] - cz]) * S * 16
        v = RyPI.T @ v if not flip else v
        return v + np.array([8.0, 0.0, 8.0])
    els = []
    for q, A, Me, a, b, faces, e, _w in raw:
        Rt = RyPI.T @ A @ Me if not flip else A @ Me
        sig = np.linalg.norm(Rt[:, 0])                          # (the uniform scale left in it)
        Rt = Rt / sig
        sz = (b - a) * sig * S
        if max(abs(sz)) < TINY: continue
        qm = to_model(q)
        fr, to = qm + a * sig * S, qm + b * sig * S
        el = {'from': [round(v, 4) for v in fr], 'to': [round(v, 4) for v in to], 'faces': faces}
        x, y, z = _euler(Rt)
        if max(abs(x), abs(y), abs(z)) > 1e-3:
            el['rotation'] = {'origin': [round(v, 4) for v in qm], 'x': round(x, 3), 'y': round(y, 3), 'z': round(z, 3)}
        for kk in ('light_emission', 'shade'):
            if kk in e: el[kk] = e[kk]
        els.append(el)
    return textures, els
