"""3D renders of the Vorn Armada (p2/dungeons/armada.py), on the Undercrown's voxel ray-marcher (undercrown_3d.Scene): vanilla
textures, coloured block light flooded from every emissive block (a green channel added for the Vorn's froglights), and the
Hive-Star's own light - every surface that faces it and can see it (a shadow ray marched toward the star, through glass) is lit
orange - over a field of stars, with a little bloom.

    python3 tools/preview/armada_3d.py [shot ...]        # no shot names: all of them

Shots go to /home/user/main/previews/v299_armada/ship/ (or $AR3D_OUT)."""
import math, os, sys, time
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(__file__))
import undercrown_3d as U3

OUT = os.environ.get('AR3D_OUT', '/home/user/main/previews/v299_armada/ship')
NCH = 6
CH_COL = np.array([(1.0, 0.42, 0.14), (0.22, 0.72, 0.85), (0.62, 0.22, 1.0), (1.0, 0.94, 0.82), (1.0, 0.1, 0.08), (0.42, 1.0, 0.3)], np.float32)
U3.LIGHTS.update({'verdant_froglight': (15, 3), 'ochre_froglight': (15, 0), 'pearlescent_froglight': (15, 3), 'shroomlight': (15, 0),
                  'magma_block': (9, 4), 'glowstone': (15, 0), 'sea_lantern': (15, 3), 'end_rod': (14, 3), 'campfire': (15, 0),
                  'blast_furnace': (13, 0), 'waxed_copper_bulb': (15, 0), 'copper_bulb': (15, 0), 'redstone_lamp': (12, 0), 'lantern': (15, 0),
                  'crying_obsidian': (10, 2), 'lava': (15, 0), 'sculk_catalyst': (6, 1)})
U3.SELF_LIT.update({'verdant_froglight': 1.3, 'shroomlight': 1.35, 'ochre_froglight': 1.35, 'pearlescent_froglight': 1.3, 'glowstone': 1.3,
                    'sea_lantern': 1.25, 'end_rod': 1.4, 'magma_block': 0.95, 'campfire': 1.2, 'waxed_copper_bulb': 1.1, 'redstone_lamp': 1.0,
                    'lantern': 1.3, 'lava': 1.1, 'blast_furnace': 0.7, 'crying_obsidian': 1.0})
U3.ALIAS.update({'waxed_cut_copper': 'cut_copper', 'waxed_weathered_cut_copper': 'weathered_cut_copper', 'waxed_copper_block': 'copper_block',
                 'waxed_copper_grate': 'copper_grate', 'waxed_copper_bulb': 'copper_bulb_lit', 'observer': 'observer_front', 'crafter': 'crafter_north',
                 'dispenser': 'dispenser_front', 'redstone_lamp': 'redstone_lamp_on', 'sculk_catalyst': 'sculk_catalyst_side',
                 'grass_block': 'grass_block_side', 'birch_log': 'birch_log', 'azalea': 'azalea_side', 'flowering_azalea': 'flowering_azalea_side'})
U3.TOP.update({'verdant_froglight': 'verdant_froglight_top', 'grass_block': 'grass_block_top', 'birch_log': 'birch_log_top',
               'sculk_catalyst': 'sculk_catalyst_top', 'azalea': 'azalea_top', 'flowering_azalea': 'flowering_azalea_top', 'campfire': 'campfire_log_lit'})
U3.SIDE.update({'verdant_froglight': 'verdant_froglight_side'})
U3.CROSSES = U3.CROSSES + ('lightning_rod', 'end_rod', 'vines', 'cornflower', 'allium', 'blue_orchid', 'oxeye_daisy', 'short_grass', 'fern',
                           'lily_of_the_valley')
STAR_COL = np.array((1.0, 0.66, 0.42), np.float32)


class Scene(U3.Scene):
    def light(self):
        A = self.A
        opaque = (self.kind[A] == U3.SOLID)
        ems = self.emisarr[A]
        L = np.zeros((NCH,) + A.shape, np.float32)
        fp = ndimage.generate_binary_structure(3, 1)
        for c in range(NCH):
            E = np.where(ems[..., 1] == c, ems[..., 0], 0).astype(np.float32)
            if not E.any(): continue
            l = E.copy()
            for _ in range(15):
                m = ndimage.maximum_filter(l, footprint=fp, mode='constant', cval=0) - 1
                l = np.maximum(np.where(opaque, 0, m), E)
                l[l < 0] = 0
            L[c] = l
        self.L = L
        for i, n in enumerate(self.names):
            if self.kind[i] == U3.GLASS:
                t = self.atlas[self.texid[i, 1]]
                rgb = t[..., :3].mean(axis=(0, 1))
                self.tintarr[i] = (0.42, 0.34, 0.48) if n == 'tinted_glass' else np.clip(0.25 + 0.75 * rgb, 0, 1)

    def shade_hits(self, O, D, t, bid, ax, sg, u, v, P):
        N = len(t)
        face = np.where(ax == 1, np.where(sg > 0, 0, 2), 1)
        tx = self.texid[bid, face]
        ui, vi = (u * 16).astype(int).clip(0, 15), (v * 16).astype(int).clip(0, 15)
        rgb = self.atlas[tx, vi, ui, :3]
        pt = O + D * t[:, None]
        nrm = np.zeros((N, 3), np.float32); nrm[np.arange(N), ax] = sg
        q = pt + nrm * 0.5 - 0.5
        L = np.stack([ndimage.map_coordinates(self.L[c], q.T, order=1, mode='nearest') for c in range(NCH)], 1)
        Ln = (np.clip(L, 0, 15) / 15.0) ** 2.2
        lightc = Ln @ CH_COL * P['gain']
        shade = np.where(ax == 1, np.where(sg > 0, 1.0, 0.45), np.where(ax == 0, 0.78, 0.62)).astype(np.float32)
        amb = np.array(P['ambient'], np.float32)
        fill = P['fill'] / (1.0 + (t / P['fill_r']) ** 2)
        lit = amb + lightc + fill[:, None] * np.array((0.8, 0.9, 0.85), np.float32)
        # the Hive-Star: lambert toward its centre, shadowed (a ray marched toward it, glass tinting what passes)
        if P.get('sun', 0) > 0:
            sc = np.array(P['star_c'], np.float32) + 0.5
            Ls = sc[None, :] - pt
            dist = np.linalg.norm(Ls, axis=1)
            Ld = Ls / dist[:, None]
            ndl = np.clip((nrm * Ld).sum(1), 0, 1)
            vis = np.zeros(N, np.float32)
            cand = (ndl > 0) & (dist > P['star_r'] + 1.5)
            if cand.any():
                ci = np.nonzero(cand)[0]
                R = self.march(pt[ci] + nrm[ci] * 0.02 + Ld[ci] * 0.02, Ld[ci].astype(np.float32), tmax=float(dist.max()) + 2)
                hp = pt[ci] + Ld[ci] * np.where(np.isfinite(R['t']), R['t'], 0)[:, None]
                ok = ~np.isfinite(R['t']) | (np.linalg.norm(hp - sc[None, :], axis=1) <= P['star_r'] + 9)
                vis[ci] = ok * R['trans'].mean(1)
            sun = (ndl * vis * P['sun'] / (1 + (np.maximum(dist - P['star_r'], 0) / 140.0) ** 2))[:, None] * STAR_COL[None, :]
            lit = lit + sun
        col = rgb * lit * shade[:, None]
        sl = self.selflitarr[bid]
        col = np.where(sl[:, None] > 0, rgb * sl[:, None] * (0.75 + 0.25 * shade[:, None]) + col * 0.3, col)
        return col, pt

    def render(self, cam, W=None, H=None, P=None, decals=None):
        sc_ = float(os.environ.get('AR3D_SCALE', '1'))
        W, H = int((W or 1600) * sc_), int((H or 1000) * sc_)
        P = dict(dict(ambient=(0.07, 0.07, 0.09), gain=2.4, fill=0.12, fill_r=40.0, fog=(0.0, 0.0, 0.0), fog_d=2000.0, exposure=1.5,
                      bg=(0.004, 0.004, 0.012), sun=1.6, bloom=0.5), **(P or {}))
        O, D = cam.rays(W, H)
        t0 = time.time()
        R = self.march(O, D, tmax=900.0, max_steps=1400)
        N = W * H
        col = np.zeros((N, 3), np.float32)
        col[:] = P['bg']
        rng = np.random.default_rng(7)                          # the stars, behind everything
        stars = rng.random(N) < 0.0016
        col[stars] = rng.uniform(0.25, 1.0, (stars.sum(), 1)) * np.array((0.9, 0.95, 1.0), np.float32)
        neb = (0.5 + 0.5 * np.sin(D[:, 0] * 3.1 + D[:, 1] * 5.2) * np.cos(D[:, 2] * 2.7 - D[:, 1] * 1.9)) ** 3
        col += neb[:, None] * np.array((0.01, 0.03, 0.012), np.float32)
        h = np.isfinite(R['t'])
        if h.any():
            hc, pt = self.shade_hits(O[h], D[h], R['t'][h], R['id'][h], R['ax'][h], R['sg'][h], R['u'][h], R['v'][h], P)
            fogf = np.exp(-R['t'][h] / P['fog_d'])[:, None]
            col[h] = hc * fogf + np.array(P['fog'], np.float32) * (1 - fogf)
        g = np.isfinite(R['g_t'])
        if g.any():
            gt = R['g_t'][g]
            gu, gv = self.uv(O[g], D[g], gt, R['g_ax'][g])
            gc, _ = self.shade_hits(O[g], D[g], gt, R['g_id'][g], R['g_ax'][g], R['g_sg'][g], gu, gv, dict(P, sun=P['sun'] * 0.3))
            col[g] = col[g] * R['trans'][g] + gc * P.get('glass', 0.35)
        col = 1 - np.exp(-col * P['exposure'])
        col = np.clip(col, 0, 1) ** (1 / 1.25)
        img = col.reshape(H, W, 3)
        if P['bloom']:
            br = np.clip(img - 0.62, 0, 1)
            bim = Image.fromarray((br * 255).astype(np.uint8))
            b1 = np.asarray(bim.filter(ImageFilter.GaussianBlur(W / 220)), np.float32) / 255
            b2 = np.asarray(bim.filter(ImageFilter.GaussianBlur(W / 45)), np.float32) / 255
            img = np.clip(img + P['bloom'] * (b1 * 0.9 + b2 * 1.6), 0, 1)
        print(f'   march+shade {time.time() - t0:.1f}s', flush=True)
        return Image.fromarray((img * 255).astype(np.uint8))


SHOTS = {}


def shot(name):
    def deco(f):
        SHOTS[name] = f
        return f
    return deco


def P_(B, **kw):
    import p2.armadacfg as A
    return dict(star_c=A.STAR['c'], star_r=A.STAR['r'], **kw)


@shot('1_fleet')
def s1(B, sc):
    """the whole fleet round its star, from high over the Dock's quarter"""
    cam = U3.Persp((330, 150, 345), (112, 40, 110), fov=50)
    return sc.render(cam, W=1800, H=1100, P=P_(B, ambient=(0.13, 0.13, 0.16), fill=0.0, sun=1.4))


@shot('2_fleet_low')
def s2(B, sc):
    """low along the orbit: the Flagship's dome and the Dock black against the star"""
    cam = U3.Persp((-30, 62, 270), (150, 44, 100), fov=58)
    return sc.render(cam, W=1800, H=1000, P=P_(B, ambient=(0.11, 0.11, 0.14), fill=0.0, sun=1.4))


def ship_shot(eye, at, fov=55, **kw):
    def f(B, sc):
        cam = U3.Persp(eye, at, fov=fov)
        return sc.render(cam, W=1600, H=1000, P=P_(B, ambient=kw.get('amb', (0.15, 0.15, 0.18)), fill=0.05, fill_r=80, sun=1.25))
    return f


SHOTS['3_dock'] = ship_shot((176, 76, 262), (122, 50, 204), 55)
SHOTS['4_brood'] = ship_shot((258, 82, 214), (190, 48, 170), 60)
SHOTS['5_forge'] = ship_shot((262, 80, 40), (204, 50, 86), 58)
SHOTS['6_nav'] = ship_shot((176, 86, -46), (140, 52, 22), 62)
SHOTS['7_dread_a'] = ship_shot((10, 84, -40), (58, 50, 22), 58)
SHOTS['8_dread_b'] = ship_shot((-46, 84, 120), (24, 52, 90), 58)
SHOTS['9_flagship'] = ship_shot((-30, 96, 262), (50, 56, 182), 58)


@shot('10_bridge')
def s10(B, sc):
    """THE BRIDGE: from just inside the battle door, the great window and the Hive-Star in it, the helm before it"""
    cam = U3.Persp((31.5, 58.6, 197.5), (86, 61, 150), fov=88)
    return sc.render(cam, W=1800, H=1050, P=P_(B, ambient=(0.1, 0.1, 0.12), gain=3.0, fill=0.2, fill_r=30, sun=1.0, exposure=1.4, glass=0.12))


@shot('11_bridge_helm')
def s11(B, sc):
    """from behind the helm's left, the window filled with the star"""
    cam = U3.Persp((66.5, 57.4, 168.5), (110, 58, 128), fov=78)
    return sc.render(cam, W=1800, H=1050, P=P_(B, ambient=(0.1, 0.1, 0.12), gain=3.0, fill=0.2, fill_r=30, sun=1.0, exposure=1.4, glass=0.12))


def inside(eye, at, fov=80, **kw):
    def f(B, sc):
        cam = U3.Persp(eye, at, fov=fov)
        return sc.render(cam, W=1600, H=1000, P=P_(B, ambient=kw.get('amb', (0.08, 0.08, 0.1)), gain=3.0, fill=0.15, fill_r=24, sun=1.0,
                                                   exposure=1.4, glass=0.15))
    return f


SHOTS['12_hatchery'] = inside((185.5, 49.6, 166.5), (194, 52, 146), 84)
SHOTS['13_star_dome'] = inside((174.5, 53.6, 34.5), (166, 58, 26), 88)
SHOTS['14_zero_g'] = inside((163.5, 54.6, 30.5), (140, 50, 30), 80)
SHOTS['15_gauntlet'] = inside((8.5, 56.6, 155.5), (8.5, 56, 200), 75)
SHOTS['16_foundry'] = inside((214.5, 51.6, 81.5), (203, 50, 66), 84)
SHOTS['17_reactor'] = inside((69.5, 50.6, 22.5), (56, 53, 25), 80)


def main():
    from p2.dungeons import armada
    os.makedirs(OUT, exist_ok=True)
    B = armada.build()
    want = sys.argv[1:] or list(SHOTS)
    t = time.time()
    sc = Scene(B)
    print(f'scene {time.time() - t:.0f}s', flush=True)
    for nm in want:
        for k, f in SHOTS.items():
            if k == nm or k.split('_', 1)[0] == nm or k.split('_', 1)[-1] == nm:
                t = time.time()
                im = f(B, sc)
                p = os.path.join(OUT, f'{k}.png')
                im.save(p)
                print(f'{k}: {time.time() - t:.0f}s -> {p}', flush=True)


if __name__ == '__main__':
    main()
