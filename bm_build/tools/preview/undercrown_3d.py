"""A software voxel renderer for the Undercrown (p2/dungeons/undercrown.py): numpy + PIL, vanilla block textures, per-face
shading, coloured block light flooded from every emissive block (lava, magma, shroomlight, froglights, crying obsidian, soul
lanterns, candles...), dark Nether ambient, a little fog. Rays are marched through the voxel grid (Amanatides-Woo DDA, all
pixels at once); chains, bars, lanterns and candles are alpha-cut sprites; stained and tinted glass tints what is behind it.

    python3 tools/preview/undercrown_3d.py [shot ...]        # no shot names: all of them

Shots go to the scratchpad's previews/undercrown/3d/ (or $UC3D_OUT)."""
import math, os, sys, time
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

TEXD = '/home/claude/mc263/client/assets/minecraft/textures/'
OUT = os.environ.get('UC3D_OUT', '/tmp/claude-0/-home-user-main/99867ee9-8c51-5a94-9ce7-6ff9e7d41656/scratchpad/previews/undercrown/3d')

EMPTY, SOLID, CUBECUT, CROSS, GLASS = 0, 1, 2, 3, 4
SKIP = ('air', 'cave_air', 'void_air', 'light', 'structure_void', 'carpet', 'button', 'sign', 'skull', 'head', 'banner', 'pressure_plate',
        'snow', 'tripwire', 'redstone_wire', 'rail', 'torch', 'fence')
CROSSES = ('iron_chain', 'chain', 'lantern', 'candle', 'amethyst_cluster', 'glow_lichen', 'coral', 'campfire', 'cobweb', 'dead_bush')
LIGHTS = {  # block -> (level, channel)   channels: 0 warm, 1 soul, 2 purple, 3 white
    'lava': (15, 0), 'magma_block': (6, 0), 'shroomlight': (15, 0), 'crying_obsidian': (10, 2), 'soul_lantern': (12, 1),
    'soul_campfire': (12, 1), 'pearlescent_froglight': (15, 3), 'ochre_froglight': (15, 0), 'verdant_froglight': (15, 3),
    'red_candle': (6, 0), 'purple_candle': (6, 2), 'candle': (7, 0), 'sov_glow': (9, 4), 'amethyst_cluster': (5, 2), 'glow_lichen': (7, 1),
    'blast_furnace': (13, 0), 'redstone_block': (0, 0), 'sov_eye': (13, 4), 'well': (12, 4)}
CH_COL = np.array([(1.0, 0.42, 0.14), (0.22, 0.72, 0.85), (0.62, 0.22, 1.0), (1.0, 0.94, 0.82), (1.0, 0.1, 0.08)], np.float32)
SELF_LIT = {'lava': 1.05, 'magma_block': 0.55, 'shroomlight': 1.3, 'crying_obsidian': 0.9, 'soul_lantern': 1.3, 'soul_campfire': 1.2,
            'pearlescent_froglight': 1.3, 'ochre_froglight': 1.3, 'red_candle': 1.3, 'purple_candle': 1.2, 'candle': 1.2,
            'amethyst_cluster': 0.8, 'glow_lichen': 0.7, 'blast_furnace': 0.6, 'sov_eye': 1.6, 'sov_glow': 1.1, 'well': 1.5}
ALIAS = {'magma_block': 'magma', 'lava': 'lava_still', 'snow_block': 'snow', 'smooth_quartz': 'quartz_block_bottom',
         'quartz_block': 'quartz_block_side', 'waxed_copper_bulb': 'copper_bulb', 'stripped_dark_oak_wood': 'stripped_dark_oak_log',
         'dark_oak_wood': 'dark_oak_log', 'red_candle': 'red_candle_lit', 'purple_candle': 'purple_candle_lit', 'candle': 'candle_lit',
         'soul_campfire': 'soul_campfire_fire', 'vault': 'vault_side_off', 'lectern': 'lectern_sides', 'blast_furnace': 'blast_furnace_front_on',
         'bell': 'gold_block', 'dark_oak_slab': 'dark_oak_planks', 'chest': 'barrel_side', 'reinforced_deepslate': 'reinforced_deepslate_side',
         'anvil': 'anvil', 'smithing_table': 'smithing_table_front', 'iron_chain': 'iron_chain'}
TOP = {'basalt': 'basalt_top', 'polished_basalt': 'polished_basalt_top', 'bone_block': 'bone_block_top', 'purpur_pillar': 'purpur_pillar_top',
       'quartz_pillar': 'quartz_pillar_top', 'dark_oak_log': 'dark_oak_log_top', 'target': 'target_top', 'bookshelf': 'oak_planks',
       'pearlescent_froglight': 'pearlescent_froglight_top', 'ochre_froglight': 'ochre_froglight_top', 'barrel': 'barrel_top',
       'lectern': 'lectern_top', 'reinforced_deepslate': 'reinforced_deepslate_top', 'stripped_dark_oak_log': 'stripped_dark_oak_log_top',
       'smithing_table': 'smithing_table_top', 'anvil': 'anvil_top', 'vault': 'vault_top', 'blast_furnace': 'blast_furnace_top'}
SIDE = {'basalt': 'basalt_side', 'polished_basalt': 'polished_basalt_side', 'bone_block': 'bone_block_side', 'target': 'target_side',
        'pearlescent_froglight': 'pearlescent_froglight_side', 'ochre_froglight': 'ochre_froglight_side', 'barrel': 'barrel_side'}


def bname(st):
    return st.split(':', 1)[-1].split('[', 1)[0]


def base_of(n):
    for suf in ('_stairs', '_slab', '_wall'):
        if n.endswith(suf) and n != 'iron_chain':
            b = n[:-len(suf)]
            for c in (b, b + 's', b + '_block', b.replace('brick', 'bricks'), b + '_planks'):
                if os.path.exists(TEXD + f'block/{c}.png'): return c
            return b
    return n


_TEX = {}


def load_tex(name):
    """16x16 RGBA float (the first frame of an animated strip), or None"""
    if name in _TEX: return _TEX[name]
    p = TEXD + f'block/{name}.png'
    t = None
    if os.path.exists(p):
        im = Image.open(p).convert('RGBA')
        w = im.size[0]
        im = im.crop((0, 0, w, w)).resize((16, 16), Image.NEAREST)
        t = np.asarray(im, np.float32) / 255.0
    _TEX[name] = t
    return t


def flat(rgb, a=1.0):
    t = np.zeros((16, 16, 4), np.float32); t[..., :3] = np.array(rgb, np.float32) / 255.0; t[..., 3] = a
    return t


FLAT = {'chest': (150, 105, 50), 'sov_body': (22, 16, 20), 'sov_plate': (48, 38, 44), 'sov_eye': (255, 40, 40), 'sov_glow': (200, 20, 30),
        'well': (255, 50, 60)}


class Scene:
    def __init__(self, B, extra=(), remove=None):
        """B: a structures.Build. extra: [((x, y, z), state)] voxels added for the picture only (the Sovereign, say).
        remove: a boolean grid (sx, sy, sz) of cells to leave out (cutaways)."""
        self.size = B.size
        sx, sy, sz = B.size
        self.names, self.kind, self.tex, self.emis, self.selflit, self.tint = [None], [EMPTY], [(0, 0, 0)], [(0, 0)], [0.0], [(1, 1, 1)]
        atlas = [np.zeros((16, 16, 4), np.float32)]
        tidx = {}
        def tid(name, fallback):
            key = name or ('#flat', fallback)
            if key in tidx: return tidx[key]
            t = load_tex(name) if name else None
            if t is None: t = flat(fallback)
            tidx[key] = len(atlas); atlas.append(t)
            return tidx[key]
        ids = {}
        A = np.zeros((sx, sy, sz), np.int16)
        cells = list(B.b.items()) + list(extra)
        for (x, y, z), st in cells:
            n = bname(st) if ':' in st or '[' in st or not st.startswith('sov') else st
            if n not in ids:
                ids[n] = self._add(n, tid)
            A[x, y, z] = ids[n]
        self.atlas = np.stack(atlas)
        self.kind = np.array(self.kind, np.int8)
        self.texid = np.array(self.tex, np.int32)                # (id, 3): top, side, bottom
        self.emisarr = np.array(self.emis, np.int32)
        self.selflitarr = np.array(self.selflit, np.float32)
        self.tintarr = np.array(self.tint, np.float32)
        if remove is not None: A[remove] = 0
        self.A = A
        self.decals = {}
        t = time.time()
        self.light()
        self.lt = time.time() - t

    def _add(self, n, tid):
        idx = len(self.names)
        self.names.append(n)
        if n in FLAT:
            k = SOLID; tx = (tid(None, FLAT[n]),) * 3
        elif n in SKIP or n.endswith(('_button', '_sign', '_skull', '_head', '_banner', '_carpet', '_fence', '_torch', '_plate')):
            k = EMPTY; tx = (0, 0, 0)
        else:
            b = base_of(n)
            nm = ALIAS.get(b, b)
            if 'glass' in n:
                k = GLASS
            elif n == 'iron_bars' or n == 'iron_chain' and False:
                k = CUBECUT
            elif any(c in n for c in CROSSES):
                k = CROSS
            else:
                k = SOLID
            if n == 'soul_lantern':
                side = top = 'soul_lantern'
                _TEX['soul_lantern'] = self._item('soul_lantern')
            elif n in ('red_candle', 'purple_candle', 'candle'):
                side = top = nm
            elif n.endswith('_wall') and n != 'iron_chain':
                side = top = nm
            else:
                side = SIDE.get(b, nm); top = TOP.get(b, nm)
            fb = (110, 90, 110)
            tx = (tid(top, fb), tid(side, fb), tid(top, fb))
        self.kind.append(k); self.tex.append(tx)
        lv = LIGHTS.get(n, (0, 0))
        self.emis.append(lv); self.selflit.append(SELF_LIT.get(n, 0.0))
        if k == GLASS:
            t = self.atlas_tmp(tx[1])
            self.tint.append(tuple(t))
        else:
            self.tint.append((1, 1, 1))
        return idx

    def _item(self, name):
        im = Image.open(TEXD + f'item/{name}.png').convert('RGBA').resize((16, 16), Image.NEAREST)
        return np.asarray(im, np.float32) / 255.0

    def atlas_tmp(self, t_id):
        return (0.5, 0.5, 0.5)

    def light(self):
        """four channels of block light, flooded like the game's (one level lost per block, opaque blocks stop it)"""
        A = self.A
        opaque = (self.kind[A] == SOLID)
        ems = self.emisarr[A]
        L = np.zeros((5,) + A.shape, np.float32)
        fp = ndimage.generate_binary_structure(3, 1)
        for c in range(5):
            E = np.where(ems[..., 1] == c, ems[..., 0], 0).astype(np.float32)
            if not E.any(): continue
            l = E.copy()
            for _ in range(15):
                m = ndimage.maximum_filter(l, footprint=fp, mode='constant', cval=0) - 1
                l = np.maximum(np.where(opaque, 0, m), E)
                l[l < 0] = 0
            L[c] = l
        self.L = L
        # glass tints from their textures
        for i, n in enumerate(self.names):
            if self.kind[i] == GLASS:
                t = self.atlas[self.texid[i, 1]]
                rgb = t[..., :3].mean(axis=(0, 1))
                self.tintarr[i] = (0.42, 0.34, 0.48) if n == 'tinted_glass' else np.clip(0.25 + 0.75 * rgb, 0, 1)

    # ------------------------------------------------------------------------------------------------ the ray march
    def march(self, O, D, tmax=600.0, max_steps=900):
        sx, sy, sz = self.size
        S = np.array([sx, sy, sz], np.float32)
        N = len(O)
        D = np.where(np.abs(D) < 1e-9, 1e-9, D)
        inv = 1.0 / D
        ta, tb = (0 - O) * inv, (S - O) * inv
        t0 = np.max(np.minimum(ta, tb), axis=1); t1 = np.min(np.maximum(ta, tb), axis=1)
        start = np.maximum(t0, 0) + 1e-4
        ok = (t1 > start)
        ent_ax = np.argmax(np.minimum(ta, tb), axis=1)
        res_t = np.full(N, np.inf, np.float32); res_id = np.zeros(N, np.int32); res_ax = np.zeros(N, np.int8)
        res_sg = np.zeros(N, np.int8); res_u = np.zeros(N, np.float32); res_v = np.zeros(N, np.float32)
        g_t = np.full(N, np.inf, np.float32); g_id = np.zeros(N, np.int32); g_ax = np.zeros(N, np.int8); g_sg = np.zeros(N, np.int8)
        trans = np.ones((N, 3), np.float32)
        idx = np.nonzero(ok)[0]
        o, d = O[idx], D[idx]
        t = start[idx]
        p = o + d * t[:, None]
        cell = np.clip(np.floor(p).astype(np.int32), 0, S.astype(np.int32) - 1)
        step = np.where(d > 0, 1, -1).astype(np.int32)
        tdel = np.abs(1.0 / d)
        tnext = np.where(d > 0, (cell + 1 - o) / d, (cell - o) / d)
        ax = ent_ax[idx].astype(np.int8)
        prev = np.zeros(len(idx), np.int32)
        A, kind = self.A, self.kind
        for it in range(max_steps):
            if len(idx) == 0: break
            bid = A[cell[:, 0], cell[:, 1], cell[:, 2]].astype(np.int32)
            k = kind[bid]
            hit = np.zeros(len(idx), bool)
            # solid cubes
            m = k == SOLID
            if m.any():
                hit |= m
            # glass: tint, remember the first surface
            g = (k == GLASS) & (bid != prev)
            if g.any():
                gi = idx[g]
                first = np.isinf(g_t[gi])
                fi = gi[first]
                sgall = -step[np.arange(len(idx)), ax]
                g_t[fi] = t[g][first]; g_id[fi] = bid[g][first]; g_ax[fi] = ax[g][first]; g_sg[fi] = sgall[g][first]
                trans[gi] *= self.tintarr[bid[g]]
            # cube cut-outs (bars): alpha test on the entry face
            c = (k == CUBECUT)
            if c.any():
                u, v = self.uv(o[c], d[c], t[c], ax[c])
                tx = self.texid[bid[c], 1]
                a = self.atlas[tx, (v * 16).astype(int).clip(0, 15), (u * 16).astype(int).clip(0, 15), 3]
                hc = a > 0.5
                hit[np.nonzero(c)[0][hc]] = True
            # crosses (chains, lanterns, candles...): two planes through the cell's centre
            x = (k == CROSS)
            if x.any():
                xi = np.nonzero(x)[0]
                texit = np.min(tnext[xi], axis=1)
                best_t = np.full(len(xi), np.inf, np.float32); best_ax = np.zeros(len(xi), np.int8)
                for pa in (0, 2):
                    tp = (cell[xi, pa] + 0.5 - o[xi, pa]) / d[xi, pa]
                    inside = (tp >= t[xi] - 1e-5) & (tp <= texit + 1e-5)
                    pp = o[xi] + d[xi] * tp[:, None]
                    ua = pp[:, 2] - cell[xi, 2] if pa == 0 else pp[:, 0] - cell[xi, 0]
                    va = 1 - (pp[:, 1] - cell[xi, 1])
                    tx = self.texid[bid[xi], 1]
                    a = self.atlas[tx, (va * 16).astype(int).clip(0, 15), (ua * 16).astype(int).clip(0, 15), 3]
                    good = inside & (a > 0.5) & (tp < best_t)
                    best_t[good] = tp[good]; best_ax[good] = pa
                hx = np.isfinite(best_t)
                if hx.any():
                    h = xi[hx]
                    hit[h] = True
                    t[h] = best_t[hx]; ax[h] = best_ax[hx]
            if hit.any():
                h = np.nonzero(hit)[0]
                gi = idx[h]
                res_t[gi] = t[h]; res_id[gi] = bid[h]; res_ax[gi] = ax[h]
                res_sg[gi] = -step[h, ax[h]]
                isx = kind[bid[h]] == CROSS
                res_sg[gi[isx]] = np.where(d[h[isx], ax[h[isx]]] > 0, -1, 1)
                u, v = self.uv(o[h], d[h], t[h], ax[h], cross=isx, cell=cell[h])
                res_u[gi] = u; res_v[gi] = v
            prev = np.where(k == GLASS, bid, 0)
            # advance
            a = np.argmin(tnext, axis=1)
            r = np.arange(len(idx))
            t = tnext[r, a]
            cell[r, a] += step[r, a]
            tnext[r, a] += tdel[r, a]
            ax = a.astype(np.int8)
            out = (cell < 0).any(axis=1) | (cell >= S.astype(np.int32)).any(axis=1) | (t > tmax)
            keep = ~(hit | out)
            idx, o, d, t, cell, step, tdel, tnext, ax, prev = (idx[keep], o[keep], d[keep], t[keep], cell[keep], step[keep], tdel[keep],
                                                               tnext[keep], ax[keep], prev[keep])
        return dict(t=res_t, id=res_id, ax=res_ax, sg=res_sg, u=res_u, v=res_v, g_t=g_t, g_id=g_id, g_ax=g_ax, g_sg=g_sg, trans=trans)

    def uv(self, o, d, t, ax, cross=None, cell=None):
        p = o + d * t[:, None]
        f = p - np.floor(p - 1e-4 * np.sign(d))
        f = np.clip(p - np.floor(p), 0, 0.9999)
        u = np.where(ax == 0, f[:, 2], f[:, 0])
        v = np.where(ax == 1, f[:, 2], 1 - f[:, 1])
        if cross is not None and cross.any():
            pc = p[cross] - cell[cross]
            u[cross] = np.where(ax[cross] == 0, pc[:, 2], pc[:, 0]).clip(0, 0.9999)
            v[cross] = (1 - pc[:, 1]).clip(0, 0.9999)
        return u, v

    # ------------------------------------------------------------------------------------------------ shading
    def shade_hits(self, O, D, t, bid, ax, sg, u, v, P):
        N = len(t)
        face = np.where(ax == 1, np.where(sg > 0, 0, 2), 1)
        tx = self.texid[bid, face]
        ui, vi = (u * 16).astype(int).clip(0, 15), (v * 16).astype(int).clip(0, 15)
        rgb = self.atlas[tx, vi, ui, :3]
        pt = O + D * t[:, None]
        nrm = np.zeros((N, 3), np.float32); nrm[np.arange(N), ax] = sg
        q = pt + nrm * 0.5 - 0.5
        L = np.stack([ndimage.map_coordinates(self.L[c], q.T, order=1, mode='nearest') for c in range(5)], 1)
        Ln = (np.clip(L, 0, 15) / 15.0) ** 2.2
        lightc = Ln @ CH_COL * P['gain']
        shade = np.where(ax == 1, np.where(sg > 0, 1.0, 0.45), np.where(ax == 0, 0.78, 0.62)).astype(np.float32)
        amb = np.array(P['ambient'], np.float32)
        # a dim lamp at the eye, so the dark reads
        dist = t
        fill = P['fill'] / (1.0 + (dist / P['fill_r']) ** 2)
        lit = amb + lightc + fill[:, None] * np.array((0.9, 0.82, 0.8), np.float32)
        col = rgb * lit * shade[:, None]
        sl = self.selflitarr[bid]
        col = np.where(sl[:, None] > 0, rgb * sl[:, None] * (0.75 + 0.25 * shade[:, None]) + col * 0.3, col)
        return col, pt

    def render(self, cam, W=None, H=None, P=None, decals=None):
        sc_ = float(os.environ.get('UC3D_SCALE', '1'))
        W, H = int((W or 1600) * sc_), int((H or 1000) * sc_)
        P = dict(dict(ambient=(0.055, 0.035, 0.045), gain=2.4, fill=0.22, fill_r=22.0, fog=(0.02, 0.008, 0.012), fog_d=260.0,
                      exposure=1.6, bg=(0.012, 0.006, 0.01)), **(P or {}))
        O, D = cam.rays(W, H)
        t0 = time.time()
        R = self.march(O, D)
        tm = time.time() - t0
        N = W * H
        col = np.zeros((N, 3), np.float32)
        col[:] = P['bg']
        h = np.isfinite(R['t'])
        hc, pt = self.shade_hits(O[h], D[h], R['t'][h], R['id'][h], R['ax'][h], R['sg'][h], R['u'][h], R['v'][h], P)
        if decals:
            hc = decals(self, pt, R['id'][h], R['ax'][h], R['sg'][h], R['u'][h], R['v'][h], hc)
        fogf = np.exp(-R['t'][h] / P['fog_d'])[:, None]
        col[h] = hc * fogf + np.array(P['fog'], np.float32) * (1 - fogf)
        # glass: its surface over what's behind it
        g = np.isfinite(R['g_t'])
        if g.any():
            gt = R['g_t'][g]
            gu, gv = self.uv(O[g], D[g], gt, R['g_ax'][g])
            gc, _ = self.shade_hits(O[g], D[g], gt, R['g_id'][g], R['g_ax'][g], R['g_sg'][g], gu, gv, P)
            col[g] = col[g] * R['trans'][g] + gc * P.get('glass', 0.55)
        col = 1 - np.exp(-col * P['exposure'])
        col = np.clip(col, 0, 1) ** (1 / 1.25)
        img = (col.reshape(H, W, 3) * 255).astype(np.uint8)
        print(f'   march {tm:.1f}s', flush=True)
        return Image.fromarray(img)


class Persp:
    def __init__(self, eye, at, fov=70.0, up=(0, 1, 0)):
        self.eye = np.array(eye, np.float32); at = np.array(at, np.float32)
        f = at - self.eye; self.f = f / np.linalg.norm(f)
        r = np.cross(self.f, np.array(up, np.float32)); self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)
        self.fov = fov

    def rays(self, W, H):
        tn = math.tan(math.radians(self.fov) / 2)
        xs = (np.arange(W) + 0.5) / W * 2 - 1
        ys = 1 - (np.arange(H) + 0.5) / H * 2
        X, Y = np.meshgrid(xs * tn, ys * tn * H / W)
        D = self.f[None, :] + X.reshape(-1, 1) * self.r[None, :] + Y.reshape(-1, 1) * self.u[None, :]
        D = (D / np.linalg.norm(D, axis=1, keepdims=True)).astype(np.float32)
        O = np.broadcast_to(self.eye, D.shape).astype(np.float32).copy()
        return O, D


class Ortho:
    def __init__(self, centre, direction, width, up=(0, 1, 0)):
        self.c = np.array(centre, np.float32)
        f = np.array(direction, np.float32); self.f = f / np.linalg.norm(f)
        r = np.cross(self.f, np.array(up, np.float32)); self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)
        self.w = width

    def rays(self, W, H):
        xs = ((np.arange(W) + 0.5) / W - 0.5) * self.w
        ys = (0.5 - (np.arange(H) + 0.5) / H) * self.w * H / W
        X, Y = np.meshgrid(xs, ys)
        O = self.c[None, :] - self.f[None, :] * 260 + X.reshape(-1, 1) * self.r[None, :] + Y.reshape(-1, 1) * self.u[None, :]
        D = np.broadcast_to(self.f, O.shape).astype(np.float32).copy()
        return O.astype(np.float32), D


# ==================================================================================================== the shots
def sovereign(x0=112, y0=13, z0=11):
    """the Dread Sovereign, kneeling on its throne (a stand-in, ~13 tall, for scale): black plate, red seams, six folded wings
    with shut eyes, a crown of spikes, one great red eye in the helm"""
    vox = {}
    def box(x1, y1, z1, x2, y2, z2, st):
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                for z in range(z1, z2 + 1): vox[(x, y, z)] = st
    box(x0 - 3, y0, z0 + 1, x0 - 2, y0 + 1, z0 + 5, 'sov_plate')        # shins on the floor (it kneels)
    box(x0 + 2, y0, z0 + 1, x0 + 3, y0 + 1, z0 + 5, 'sov_plate')
    box(x0 - 3, y0 + 2, z0, x0 + 3, y0 + 4, z0 + 3, 'sov_body')         # thighs, hips
    box(x0 - 3, y0 + 5, z0, x0 + 3, y0 + 9, z0 + 2, 'sov_body')         # chest
    box(x0 - 5, y0 + 8, z0, x0 + 5, y0 + 9, z0 + 2, 'sov_plate')        # pauldrons
    box(x0 - 6, y0 + 1, z0 + 1, x0 - 5, y0 + 7, z0 + 3, 'sov_body')     # arms, the fists on the floor
    box(x0 + 5, y0 + 1, z0 + 1, x0 + 6, y0 + 7, z0 + 3, 'sov_body')
    box(x0 - 6, y0, z0 + 3, x0 - 5, y0, z0 + 4, 'sov_plate'); box(x0 + 5, y0, z0 + 3, x0 + 6, y0, z0 + 4, 'sov_plate')
    box(x0 - 1, y0 + 10, z0, x0 + 1, y0 + 12, z0 + 2, 'sov_plate')      # helm
    for dx, h in ((-2, 2), (0, 3), (2, 2)): box(x0 + dx, y0 + 13, z0 + 1, x0 + dx, y0 + 12 + h, z0 + 1, 'sov_plate')   # crown
    vox[(x0, y0 + 11, z0 + 3)] = 'sov_eye'
    for y in range(y0 + 3, y0 + 10, 2): vox[(x0, y, z0 + 3)] = 'sov_glow'    # red seams down the plate
    for side in (-1, 1):                                                # six wings folded up behind, each with shut eyes
        for w, (lean, top) in enumerate(((3, 22), (6, 20), (9, 17))):
            for y in range(y0 + 6, y0 + top):
                x = x0 + side * (3 + w + (y - y0 - 6) * lean // 14)
                vox[(x, y, z0 - 1)] = 'sov_plate'
                vox[(x + side, y, z0 - 1)] = 'sov_body'
                if (y - y0) % 4 == 0: vox[(x, y, z0)] = 'sov_glow'
    return list(vox.items())


def eye_decals(B, size=1.4):
    """the Stair's eyes as the runtime shows them: a red almond `size` wide on the wall face behind each eye marker"""
    from p2.kit import VEC
    eyes = []
    for (x, y, z, f) in B.meta['under']['eyes']:
        fx, fz = VEC[f]
        axn = 0 if fx else 2
        plane = (x if fx > 0 else x + 1) if fx else (z if fz > 0 else z + 1)      # the wall face's coordinate
        eyes.append((axn, fx or fz, plane, x + 0.5 if axn == 2 else z + 0.5, y + 0.5))
    def apply(sc, pt, bid, ax, sg, u, v, col):
        for (axn, sgn, plane, cu, cv) in eyes:
            m = (ax == axn) & (sg == sgn) & (np.abs(pt[:, axn] - plane) < 0.02)
            if not m.any(): continue
            uu = (pt[m, 2] if axn == 0 else pt[m, 0]) - cu
            vv = pt[m, 1] - cv
            hw = size / 2
            half_h = 0.36 * size * np.clip(1 - (uu / hw) ** 2, 0, 1) ** 0.8
            inside = (np.abs(uu) < hw) & (np.abs(vv) < half_h)
            if not inside.any(): continue
            lid = inside & (np.abs(vv) > half_h - 0.07)
            pupil = inside & (np.abs(uu) < 0.07) & (np.abs(vv) < half_h - 0.05)
            c = col[m]
            glow = (0.7 + 0.6 * (1 - np.abs(uu) / hw))[:, None]
            c[inside] = (np.array((1.3, 0.1, 0.06)) * glow[inside])
            c[lid] = (0.18, 0.01, 0.02)
            c[pupil] = (0.03, 0.0, 0.0)
            col[m] = c
        return col
    return apply


def wells(B):
    return [((x, y, z), 'well') for (i, x, y, z) in B.meta['under']['wells']]


def cutaway(B, cam_side=(1, 1), reach=4):
    """leave out every roof and every wall on the camera's side of each space: a cell stays only if some carved space within
    `reach` cells toward the camera (cam_side = (sx, sz), the way the camera lies) rises at least as high"""
    sx, sy, sz = B.size
    top = np.full((sx, sz), -1, np.int32)
    for (x, y, z), st in B.b.items():
        if st.endswith(':air') and y > top[x, z]: top[x, z] = y
    H = top.copy()
    for a in range(reach + 1):
        for b in range(reach + 1):
            sh = np.full_like(top, -1)
            ox, oz = cam_side[0] * a, cam_side[1] * b          # H[x, z] = max top[x + ox, z + oz]
            xs_d = slice(max(0, -ox), sx - max(0, ox)); xs_s = slice(max(0, ox), sx - max(0, -ox))
            zs_d = slice(max(0, -oz), sz - max(0, oz)); zs_s = slice(max(0, oz), sz - max(0, -oz))
            sh[xs_d, zs_d] = top[xs_s, zs_s]
            H = np.maximum(H, sh)
    Y = np.arange(sy)[None, :, None]
    rm = Y > H[:, None, :]
    for (x, y, z) in B.outside:                              # the approach cave: its own roof always goes
        if y > top[x, z] and B.b[(x, y, z)] and not B.b[(x, y, z)].endswith(':air'): rm[x, y, z] = True
    return rm


SHOTS = {}


def shot(name):
    def deco(f):
        SHOTS[name] = f
        return f
    return deco


@shot('1_cutaway')
def s1(B):
    rm = cutaway(B, cam_side=(1, 1))
    sx, sy, sz = B.size
    X, Y, Z = np.meshgrid(np.arange(sx), np.arange(sy), np.arange(sz), indexing='ij')
    rm |= ((X - 112) ** 2 + (Z - 145) ** 2 <= 38.5 ** 2) & (Y > 58)          # the Hall cut open above the Hexed landing
    rm |= (Z >= 60) & (Z < 108) & (Y > 56)                                    # (and the Lantern Crawl lifted off the Stair)
    # only the skin: every solid cell with carved space beside it (the sealing rock and the deepslate behind are left out)
    air = np.zeros((sx, sy, sz), bool)
    for (x, y, z), st in B.b.items():
        if st.endswith(':air') or 'light[' in st: air[x, y, z] = True
    near = ndimage.binary_dilation(air, structure=np.ones((3, 3, 3), bool))
    rm |= ~near
    sc = Scene(B, extra=sovereign() + wells(B), remove=rm)
    cam = Ortho((116, 52, 110), (-0.62, -1.05, -1.0), 352)
    return sc.render(cam, P=dict(fill=0.0, ambient=(0.62, 0.52, 0.55), gain=2.2, fog_d=6000, exposure=1.9), decals=eye_decals(B))


@shot('2_hall_of_chains')
def s2(B):
    sc = Scene(B)
    cam = Persp((131, 98, 133), (102, 30, 158), fov=75)
    return sc.render(cam, P=dict(gain=4.0, ambient=(0.1, 0.07, 0.08), fill=0.4, fill_r=40, glass=0.32))


@shot('3_throne')
def s3(B):
    sc = Scene(B, extra=sovereign() + wells(B))
    cam = Persp((112, 32, 74), (112, 24, 22), fov=90)
    return sc.render(cam, P=dict(gain=4.5, ambient=(0.24, 0.16, 0.18), fill=0.2, fill_r=60, exposure=1.5))


@shot('4_eyes')
def s4(B):
    sc = Scene(B)
    cam = Persp((114.6, 21, 113), (108.5, 20, 99), fov=84)
    return sc.render(cam, P=dict(gain=3.2, ambient=(0.07, 0.05, 0.06), fill=0.1, fill_r=14, exposure=1.4), decals=eye_decals(B))


@shot('5_frozen_falls')
def s5(B):
    sc = Scene(B)
    cam = Persp((53, 86, 133), (31, 82, 164), fov=88)
    return sc.render(cam, P=dict(gain=3.1, ambient=(0.055, 0.05, 0.07), fill=0.15, fill_r=25, exposure=1.45))


@shot('6_hexed_library')
def s6(B):
    sc = Scene(B)
    cam = Persp((175, 57, 152), (203, 61, 124), fov=84)
    return sc.render(cam, P=dict(gain=3.5, ambient=(0.08, 0.06, 0.09), fill=0.22, fill_r=30))


@shot('7_warship')
def s7(B):
    """the cavern's north side cut away (the ship all but fills it): the Kingdom's warship hung in its chains over the lava"""
    sx, sy, sz = B.size
    X, Y, Z = np.meshgrid(np.arange(sx), np.arange(sy), np.arange(sz), indexing='ij')
    rm = (Z < 193) & (X > 60) & (X < 170) & (Y < 90)
    sc = Scene(B, remove=rm)
    cam = Persp((119, 58, 150), (119, 36, 206), fov=70)
    return sc.render(cam, P=dict(gain=4.2, ambient=(0.2, 0.13, 0.14), fill=0.0, fog_d=600))


@shot('8_approach')
def s8(B):
    """THE MAW from just inside its east mouth: the court, the moat, the stair, the knights, the facade"""
    sc = Scene(B)
    cam = Persp((221.5, 74, 186.5), (192, 95, 194.5), fov=80)
    return sc.render(cam, P=dict(gain=3.4, ambient=(0.12, 0.08, 0.09), fill=0.25, fill_r=40, fog_d=500))


@shot('10_maw_outside')
def s10(B):
    """THE MAW from the Nether outside its east mouth (only the template is drawn: the Nether's own rock round it is left out)"""
    sc = Scene(B)
    cam = Persp((258, 79, 194.5), (200, 88, 194.5), fov=58)
    return sc.render(cam, P=dict(gain=3.4, ambient=(0.12, 0.08, 0.09), fill=0.25, fill_r=40, fog_d=500))


@shot('11_maw_face')
def s11(B):
    """the facade face-on (the court's east half cut away)"""
    sx, sy, sz = B.size
    X = np.arange(sx)[:, None, None] + np.zeros((1, sy, sz), int)
    sc = Scene(B, remove=X >= 206)
    cam = Ortho((195, 90, 194.5), (-1, 0, 0), 66)
    return sc.render(cam, W=1200, H=1000, P=dict(gain=3.4, ambient=(0.16, 0.11, 0.12), fill=0.2, fill_r=40, fog_d=900))


@shot('12_maw_south')
def s12(B):
    """THE MAW from the Nether outside its south mouth"""
    sc = Scene(B)
    cam = Persp((223, 78, 246), (194, 96, 195), fov=62)
    return sc.render(cam, P=dict(gain=3.4, ambient=(0.12, 0.08, 0.09), fill=0.25, fill_r=40, fog_d=500))


@shot('14_maw_knight')
def s14(B):
    """the north knight, from the court floor"""
    sc = Scene(B)
    cam = Persp((217.5, 76, 186.5), (200, 82, 175), fov=70)
    return sc.render(cam, P=dict(gain=3.4, ambient=(0.12, 0.08, 0.09), fill=0.25, fill_r=40, fog_d=500))


@shot('13_maw_gate')
def s13(B):
    """at the stair's foot, looking up the red stair into the mouth"""
    sc = Scene(B)
    cam = Persp((216.5, 74, 194.5), (192, 92, 194.5), fov=70)
    return sc.render(cam, P=dict(gain=3.4, ambient=(0.12, 0.08, 0.09), fill=0.25, fill_r=40, fog_d=500))


@shot('9_last_light')
def s9(B):
    sc = Scene(B)
    cam = Persp((93.5, 16, 85), (82, 17, 85), fov=84)
    return sc.render(cam, P=dict(gain=1.5, ambient=(0.03, 0.025, 0.03), fill=0.04, fill_r=15, exposure=0.8))


def main():
    from p2.dungeons import undercrown
    os.makedirs(OUT, exist_ok=True)
    B = undercrown.build()
    want = sys.argv[1:] or list(SHOTS)
    for nm in want:
        for k, f in SHOTS.items():
            if k == nm or k.split('_', 1)[0] == nm or k.split('_', 1)[-1] == nm:
                t = time.time()
                im = f(B)
                p = os.path.join(OUT, f'{k}.png')
                im.save(p)
                print(f'{k}: {time.time() - t:.0f}s -> {p}', flush=True)


if __name__ == '__main__':
    main()
