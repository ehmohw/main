"""2.94k: Z-FIGHTING, swept out of every model the resource pack builds.

Two faces of one model pointing the same way, in the same plane (or all but - less than ZTOL apart) and overlapping, flicker
in the game as the depth buffer picks one and then the other. Where their pixels differ there (sampled over the overlap -
the same colour on both is harmless), the smaller element's face is pushed out by PUSH, so it sits proud of the larger one:
the detail on top, as it was meant. Elements under a rotation are compared with others under exactly the same rotation (one
frame). A model of over LIMIT faces (the voxel sculptures) is left alone.
    apply(rp_dir) -> how many faces it moved"""
import collections
import glob
import json
import os
from PIL import Image

ZTOL, PUSH, MIN, LIMIT, ROUNDS = 0.03, 0.06, 0.05, 6000, 6
VANILLA = '/home/claude/mc263/client/assets'
AX = {'east': 0, 'west': 0, 'up': 1, 'down': 1, 'south': 2, 'north': 2}
POS = ('east', 'up', 'south')
_tex = {}


def _image(assets, ref):
    ns, p = ref.split(':', 1) if ':' in ref else ('minecraft', ref)
    for root in (assets, VANILLA):
        f = f'{root}/{ns}/textures/{p}.png'
        if os.path.exists(f):
            if f not in _tex:
                _tex[f] = Image.open(f).convert('RGBA')
            return _tex[f]
    return None


def _resolve(m, key):
    t = m.get('textures', {})
    for _ in range(8):
        if not key.startswith('#'):
            return key
        key = t.get(key[1:], '')
    return None


def _auto(fn, f, t):
    return {'north': [16 - t[0], 16 - t[1], 16 - f[0], 16 - f[1]], 'south': [f[0], 16 - t[1], t[0], 16 - f[1]],
            'east': [16 - t[2], 16 - t[1], 16 - f[2], 16 - f[1]], 'west': [f[2], 16 - t[1], t[2], 16 - f[1]],
            'up': [f[0], f[2], t[0], t[2]], 'down': [f[0], 16 - t[2], t[0], 16 - f[2]]}[fn]


def _pixel(assets, m, e, fn, p):
    face = e['faces'][fn]
    im = _image(assets, _resolve(m, face.get('texture', '')) or '')
    if im is None:
        return None
    f, t = e['from'], e['to']
    uv = face.get('uv') or _auto(fn, f, t)
    d = lambda a, b, c: (c - a) / (b - a) if b != a else 0.5
    x, y, z = p
    s, q = {'north': (d(t[0], f[0], x), d(t[1], f[1], y)), 'south': (d(f[0], t[0], x), d(t[1], f[1], y)),
            'east': (d(t[2], f[2], z), d(t[1], f[1], y)), 'west': (d(f[2], t[2], z), d(t[1], f[1], y)),
            'up': (d(f[0], t[0], x), d(f[2], t[2], z)), 'down': (d(f[0], t[0], x), d(t[2], f[2], z))}[fn]
    u, v = uv[0] + (uv[2] - uv[0]) * s, uv[1] + (uv[3] - uv[1]) * q
    W, H = im.size
    return im.getpixel((min(W - 1, max(0, int(u / 16 * W))), min(H - 1, max(0, int(v / 16 * H)))))


def _differ(assets, m, ea, eb, fn, plane, ov, o):
    if ea['faces'][fn].get('rotation') or eb['faces'][fn].get('rotation'):
        return True
    for fa in (0.2, 0.5, 0.8):
        for fb in (0.2, 0.5, 0.8):
            c = [0.0, 0.0, 0.0]
            c[AX[fn]] = plane
            c[o[0]] = ov[0][0] + (ov[0][1] - ov[0][0]) * fa
            c[o[1]] = ov[1][0] + (ov[1][1] - ov[1][0]) * fb
            pa, pb = _pixel(assets, m, ea, fn, c), _pixel(assets, m, eb, fn, c)
            if pa is None or pb is None or (pa[3] < 10 and pb[3] < 10):
                continue
            if sum(abs(pa[k] - pb[k]) for k in range(4)) > 24:
                return True
    return False


def _area(e, o):
    return abs(e['to'][o[0]] - e['from'][o[0]]) * abs(e['to'][o[1]] - e['from'][o[1]])


def _shift(e, fn, by):
    """move the element's fn face along its axis by `by` (the box grows or shrinks on that side), inside -16..32 and never inside out"""
    ax = AX[fn]
    mx, mn = ('to', 'from') if e['to'][ax] >= e['from'][ax] else ('from', 'to')
    k = mx if fn in POS else mn
    v = round(e[k][ax] + by, 4)
    if not -16 <= v <= 32 or (k == mx and v <= e[mn][ax]) or (k == mn and v >= e[mx][ax]):
        return False
    e[k][ax] = v
    return True


def fix_model(assets, m):
    els = m.get('elements') or []
    if sum(len(e.get('faces', {})) for e in els) > LIMIT:
        return 0
    groups = collections.defaultdict(list)
    for i, e in enumerate(els):
        r = e.get('rotation') or {}
        rk = json.dumps(r, sort_keys=True) if r.get('angle', 0) else ''
        for fn in e.get('faces', {}):
            ax = AX[fn]
            plane = e['to'][ax] if fn in POS else e['from'][ax]
            groups[(rk, fn)].append((plane, i))
    moved = set()
    for (rk, fn), L in groups.items():
        ax = AX[fn]
        o = [k for k in range(3) if k != ax]
        L.sort()
        for ai, (pa, ia) in enumerate(L):
            for pb, ib in L[ai + 1:]:
                if pb - pa > ZTOL:
                    break
                if ia == ib or (ia, fn) in moved or (ib, fn) in moved:
                    continue
                ea, eb = els[ia], els[ib]
                ov = [(max(min(ea['from'][k], ea['to'][k]), min(eb['from'][k], eb['to'][k])),
                       min(max(ea['from'][k], ea['to'][k]), max(eb['from'][k], eb['to'][k]))) for k in o]
                if not all(hi - lo > MIN for lo, hi in ov):
                    continue
                if not _differ(assets, m, ea, eb, fn, (pa + pb) / 2, ov, o):
                    continue
                aa, ab = _area(ea, o), _area(eb, o)
                j = ia if aa < ab else ib if ab < aa else max(ia, ib)          # (the smaller - the detail - comes forward)
                out = PUSH if fn in POS else -PUSH
                if not _shift(els[j], fn, out):                                  # (past the model's bounds: the other steps back)
                    j = ib if j == ia else ia
                    if not _shift(els[j], fn, -out):
                        continue
                moved.add((j, fn))
    return len(moved)


def apply(rp_dir):
    assets = os.path.join(rp_dir, 'assets')
    n = 0
    for p in glob.glob(f'{assets}/*/models/**/*.json', recursive=True):
        try:
            m = json.load(open(p))
        except (ValueError, OSError):
            continue
        k = 0
        for _ in range(ROUNDS):                       # (again, until nothing moves: a face brought forward can meet a third)
            r = fix_model(assets, m)
            k += r
            if not r:
                break
        if k:
            with open(p, 'w') as f:
                json.dump(m, f, separators=(',', ':'))
            n += k
    return n
