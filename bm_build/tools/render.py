"""Software preview of item_display models as the game draws them (no client needed).

    from tools.render import Scene
    s = Scene(rp='/home/claude/bm_build/out_p2/BlackMarket_RP')
    s.display('bm:item/cecil_body', pos=(0, 0, 0), yaw=0, translation=(0, 0.5, 0), scale=1)
    s.player_box((1.5, 0, 0))            # a 0.6 x 1.8 reference box
    s.save('out.png', views=('front', 'side', 'iso'))

Pipeline per vertex (DisplayRenderer + ItemDisplay + ItemRenderer.FIXED):
    world = pos + Yaw(-yaw) * Pitch(pitch) * (T + Lrot * S * Rrot) * Ry(180) * Display_fixed * (p/16 - 0.5)
Faces are z-buffered and textured from the RP or the vanilla client assets."""
import json, math, os
import numpy as np
from PIL import Image

VANILLA = '/home/claude/mc263/client/assets'


def rx(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def ry(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def quat(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


class Scene:
    def __init__(self, rp):
        self.rp = rp; self.faces = []; self.tex = {}

    def _path(self, ns_id, kind, ext):
        ns, p = ns_id.split(':') if ':' in ns_id else ('minecraft', ns_id)
        for root in (os.path.join(self.rp, 'assets'), VANILLA):
            f = os.path.join(root, ns, kind, p + ext)
            if os.path.exists(f): return f
        raise FileNotFoundError(ns_id)

    def model(self, mid):
        m = json.load(open(self._path(mid, 'models', '.json')))
        if 'parent' in m and 'elements' not in m:
            base = self.model(m['parent']); base['textures'] = dict(base.get('textures', {}), **m.get('textures', {}))
            if 'display' in m: base['display'] = dict(base.get('display', {}), **m['display'])
            return base
        return m

    def texture(self, tid):
        if tid not in self.tex:
            im = Image.open(self._path(tid, 'textures', '.png')).convert('RGBA')
            if im.height > im.width: im = im.crop((0, 0, im.width, im.width))
            self.tex[tid] = np.asarray(im).astype(np.float32) / 255.0
        return self.tex[tid]

    def display(self, mid, pos=(0, 0, 0), yaw=0.0, pitch=0.0, translation=(0, 0, 0), scale=1.0, left=(0, 0, 0, 1), right=(0, 0, 0, 1)):
        m = self.model(mid)
        tx = m.get('textures', {})
        def resolve(t):
            while t.startswith('#'): t = tx[t[1:]]
            return t
        d = m.get('display', {}).get('fixed', {})
        dr = d.get('rotation', [0, 0, 0]); dt = np.array(d.get('translation', [0, 0, 0])) / 16; ds = np.array(d.get('scale', [1, 1, 1]))
        Dm = rx(math.radians(dr[0])) @ ry(math.radians(dr[1])) @ rz(math.radians(dr[2]))
        sc = np.array(scale if isinstance(scale, (list, tuple)) else [scale] * 3, dtype=float)
        E = ry(math.radians(-yaw)) @ rx(math.radians(pitch))
        Tm = quat(left) @ np.diag(sc) @ quat(right)
        def xf(p):
            v = np.array(p) / 16 - 0.5
            v = Dm @ (v * ds) + dt
            v = ry(math.pi) @ v
            v = Tm @ v + np.array(translation)
            return E @ v + np.array(pos)
        for el in m.get('elements', []):
            f, t = el['from'], el['to']
            r = el.get('rotation')
            def er(p):
                if not r: return p
                o = np.array(r['origin']); a = math.radians(r['angle'])
                M = {'x': rx, 'y': ry, 'z': rz}[r['axis']](a)
                return M @ (np.array(p) - o) + o
            x1, y1, z1 = f; x2, y2, z2 = t
            quads = {'north': [(x2, y2, z1), (x1, y2, z1), (x1, y1, z1), (x2, y1, z1)],
                     'south': [(x1, y2, z2), (x2, y2, z2), (x2, y1, z2), (x1, y1, z2)],
                     'east': [(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)],
                     'west': [(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)],
                     'up': [(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)],
                     'down': [(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)]}
            for name, fc in el.get('faces', {}).items():
                uv = fc.get('uv', [0, 0, 16, 16]); tid = resolve(fc['texture'])
                pts = [xf(er(p)) for p in quads[name]]
                u1, v1, u2, v2 = uv
                self.faces.append((pts, [(u1, v1), (u2, v1), (u2, v2), (u1, v2)], tid))

    def box(self, lo, hi, color=(1, 0, 0)):
        self.faces.append(('box', lo, hi, color))

    def player_box(self, at=(1.2, 0, 0)):
        self.box((at[0] - 0.3, at[1], at[2] - 0.3), (at[0] + 0.3, at[1] + 1.8, at[2] + 0.3), (1, 0.2, 0.2))

    def render(self, view='front', size=420, span=3.2, center=(0, 1, 0)):
        # camera axes: right, up, forward (into the screen)
        V = {'front': (0, 0), 'back': (180, 0), 'side': (90, 0), 'iso': (35, 25), 'top': (0, 89)}[view]
        yw, pt = math.radians(V[0]), math.radians(V[1])
        fwd = np.array([-math.sin(yw) * math.cos(pt), -math.sin(pt), -math.cos(yw) * math.cos(pt)])   # front: looking toward -z (we stand south)
        right = np.cross(fwd, [0, 1, 0]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
        c = np.array(center)
        img = np.ones((size, size, 3), np.float32) * np.array([0.78, 0.86, 0.95])
        zb = np.full((size, size), np.inf)
        k = size / span
        def proj(p):
            d = np.array(p) - c
            return np.array([size / 2 + d @ right * k, size / 2 - d @ up * k, d @ fwd])
        # ground grid
        for g in np.arange(-3, 3.01, 0.5):
            for a, b in (((g, 0, -3), (g, 0, 3)), ((-3, 0, g), (3, 0, g))):
                pa, pb = proj(a), proj(b)
                n = int(max(abs(pb[0] - pa[0]), abs(pb[1] - pa[1]))) + 1
                for t in np.linspace(0, 1, n):
                    x, y = (pa[:2] * (1 - t) + pb[:2] * t).astype(int)
                    if 0 <= x < size and 0 <= y < size: img[y, x] = [0.55, 0.62, 0.55] if g else [0.2, 0.5, 0.2]
        light = np.array([0.4, 0.8, 0.45]); light /= np.linalg.norm(light)
        for f in self.faces:
            if f[0] == 'box':
                _, lo, hi, col = f
                corners = [(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
                P = [proj(p) for p in corners]
                for i in range(8):
                    for j in range(i + 1, 8):
                        if sum(a != b for a, b in zip(corners[i], corners[j])) == 1:
                            n = int(max(abs(P[j][0] - P[i][0]), abs(P[j][1] - P[i][1]))) + 1
                            for t in np.linspace(0, 1, n):
                                x, y = (P[i][:2] * (1 - t) + P[j][:2] * t).astype(int)
                                if 0 <= x < size and 0 <= y < size: img[y, x] = col
                continue
            pts, uvs, tid = f
            tex = self.texture(tid); th, tw = tex.shape[:2]
            P = [proj(p) for p in pts]
            nrm = np.cross(np.array(pts[1]) - pts[0], np.array(pts[3]) - pts[0])
            if np.linalg.norm(nrm) < 1e-9: continue
            nrm = nrm / np.linalg.norm(nrm)
            shade = 0.55 + 0.45 * abs(nrm @ light)
            for tri in ((0, 1, 2), (0, 2, 3)):
                A, B, C = (P[i] for i in tri); ua, ub, uc = (np.array(uvs[i]) for i in tri)
                xs = [A[0], B[0], C[0]]; ys = [A[1], B[1], C[1]]
                x0, x1 = max(int(min(xs)), 0), min(int(max(xs)) + 1, size - 1)
                y0, y1 = max(int(min(ys)), 0), min(int(max(ys)) + 1, size - 1)
                if x0 > x1 or y0 > y1: continue
                den = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
                if abs(den) < 1e-9: continue
                gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
                w1 = ((B[1] - C[1]) * (gx - C[0]) + (C[0] - B[0]) * (gy - C[1])) / den
                w2 = ((C[1] - A[1]) * (gx - C[0]) + (A[0] - C[0]) * (gy - C[1])) / den
                w3 = 1 - w1 - w2
                inside = (w1 >= -1e-6) & (w2 >= -1e-6) & (w3 >= -1e-6)
                if not inside.any(): continue
                z = w1 * A[2] + w2 * B[2] + w3 * C[2]
                u = (w1 * ua[0] + w2 * ub[0] + w3 * uc[0]) / 16 * tw
                v = (w1 * ua[1] + w2 * ub[1] + w3 * uc[1]) / 16 * th
                ui = np.clip(u.astype(int), 0, tw - 1); vi = np.clip(v.astype(int), 0, th - 1)
                texel = tex[vi, ui]
                sub = zb[y0:y1 + 1, x0:x1 + 1]
                ok = inside & (z < sub) & (texel[..., 3] > 0.1)
                sub[ok] = z[ok]
                img[y0:y1 + 1, x0:x1 + 1][ok] = texel[..., :3][ok] * shade
        return Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))

    def save(self, path, views=('front', 'side', 'iso'), **kw):
        ims = [self.render(v, **kw) for v in views]
        out = Image.new('RGB', (sum(i.width for i in ims), ims[0].height), 'white')
        x = 0
        for i in ims: out.paste(i, (x, 0)); x += i.width
        out.save(path)
        return path
