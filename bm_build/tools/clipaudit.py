"""2.78: the clipping audit - every follower (and the bosses that share their rigs) in every pose: where one part sinks into
another. Each pose is built as phase134's figures are - the game's own part transforms, from the built resource pack - and
every model element becomes a box in the world; the separating-axis test says how deep two boxes of different parts go into
each other. Boxes that already overlap at rest (a shoulder inside the torso, a hand round its weapon) are judged by how much
deeper they go than at rest; boxes that don't touch at rest are judged as they are.

    python3 tools/clipaudit.py [rig ...] [--min 1.0] [--top 8] [--pose name]

Depths are in the rig's own design pixels (1/16 of a block at its own scale)."""
import math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from render import Scene, rx, ry, rz, quat

RP = os.path.join(os.path.dirname(HERE), 'out_p2', 'BlackMarket_RP')


class BoxScene(Scene):
    """a Scene that keeps every element as a box (8 corners) per display, instead of drawing it"""
    def __init__(self, rp):
        super().__init__(rp); self.boxes = []; self.n = 0

    def display(self, mid, pos=(0, 0, 0), yaw=0.0, pitch=0.0, translation=(0, 0, 0), scale=1.0, left=(0, 0, 0, 1), right=(0, 0, 0, 1), ctx='fixed', tag=None):
        m = self.model(mid)
        tx = m.get('textures', {})
        def resolve(t):
            while t.startswith('#'): t = tx.get(t[1:], t[1:])
            return t
        d = m.get('display', {}).get(ctx, {}) if ctx != 'none' else {}
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
        for i, el in enumerate(m.get('elements', [])):
            f, t = el['from'], el['to']
            r = el.get('rotation')
            if r:
                o = np.array(r['origin'])
                if 'axis' in r: M = {'x': rx, 'y': ry, 'z': rz}[r['axis']](math.radians(r['angle']))
                else: M = rz(math.radians(r.get('z', 0))) @ ry(math.radians(r.get('y', 0))) @ rx(math.radians(r.get('x', 0)))
                er = lambda p: M @ (np.array(p, dtype=float) - o) + o
            else:
                er = lambda p: np.array(p, dtype=float)
            corners = np.array([xf(er((x, y, z))) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])])
            texs = {resolve(fc.get('texture', '')) for fc in el.get('faces', {}).values()}
            self.boxes.append((self.n, tag or mid, i, corners, '/'.join(sorted(texs))[-48:]))
        self.n += 1


def _axes(c):
    """a box's three edge directions from its corners (ordered x0y0z0, x0y0z1, x0y1z0, x0y1z1, x1...)"""
    a = c[4] - c[0]; b = c[2] - c[0]; d = c[1] - c[0]
    out = []
    for v in (a, b, d):
        n = np.linalg.norm(v)
        out.append(v / n if n > 1e-9 else None)
    return out


def depth(c1, c2):
    """how far two boxes overlap along the axis where they overlap least (0 when apart)"""
    A, B = _axes(c1), _axes(c2)
    axes = [v for v in A + B if v is not None]
    for u in A:
        for v in B:
            if u is None or v is None: continue
            w = np.cross(u, v); n = np.linalg.norm(w)
            if n > 1e-6: axes.append(w / n)
    best = 1e9
    for ax in axes:
        p1, p2 = c1 @ ax, c2 @ ax
        ov = min(p1.max(), p2.max()) - max(p1.min(), p2.min())
        if ov <= 0: return 0.0
        best = min(best, ov)
    return best


def pair_depths(boxes):
    """{(i, j): depth} for box pairs of different displays that overlap"""
    lo = np.array([b[3].min(0) for b in boxes]); hi = np.array([b[3].max(0) for b in boxes])
    disp = np.array([b[0] for b in boxes])
    out = {}
    for i in range(len(boxes)):
        m = (disp != disp[i]) & np.all(lo <= hi[i] + 1e-6, axis=1) & np.all(hi >= lo[i] - 1e-6, axis=1)
        m[:i + 1] = False
        for j in np.nonzero(m)[0]:
            d = depth(boxes[i][3], boxes[j][3])
            if d > 0: out[(i, int(j))] = d
    return out


def build(parts, rp=RP):
    """phase134-style parts [(model, translation, left, right, scale)] -> BoxScene"""
    s = BoxScene(rp)
    for k, (model, tr, L, R, sc) in enumerate(parts):
        s.display(model.replace('bm:', 'bm:item/'), translation=tr, scale=sc, left=L, right=R, tag=model)
    return s


# ------------------------------------------------------------------------------------------------ the rigs, pose by pose
def rigs():
    import phase134 as F
    import phase96_art as LEO, phase66_art as CELI, phase97_art as DEMO, phase57_art as EMMA, phase79_art as KW
    import apophiss_art as APO, tullius_art as TUL, phase72_art as ZIB, phase63 as P63
    R = {}
    R['leo'] = (LEO.RIG_SCALE, list(LEO.POSES), lambda p: F._jointed(LEO, lambda q: f'bm:le_{q}', p, LEO.RIG_SCALE))
    R['celi'] = (CELI.RIG_SCALE, list(CELI.POSES), lambda p: F._jointed(CELI, lambda q: f'bm:ce_{q}', p, CELI.RIG_SCALE))
    sk = round(DEMO.RIG_SCALE / DEMO.SCYTHE_K, 4)
    R['demo'] = (DEMO.RIG_SCALE, list(DEMO.POSES), lambda p: F._jointed(DEMO, lambda q: f'bm:dm_{q}', p, DEMO.RIG_SCALE,
                                                                       scale_of=lambda q: sk if q == 'scythe' else DEMO.RIG_SCALE))
    R['emma'] = (EMMA.RIG_SCALE, list(EMMA.POSES), lambda p: F._jointed(EMMA, lambda q: f'bm:em_{q}', p, EMMA.RIG_SCALE, pivot=lambda q: EMMA.PIVOT[q],
                                                                       skip=[q for q in EMMA.PARTS if q.startswith('wing')]))
    def kw(pose):
        S, U = 1.05, 1.05 / 16
        out = []
        for p in KW.PARTS:
            x, y, z = KW.PIVOT[p]
            rot, (ox, oy, oz), dy = KW.part_xf(KW.POSES[pose], p)
            out.append((f'bm:kw_{p}', (-x * U + ox * U, y * U + oy * U + dy * S / KW.RIG_SCALE, -z * U + oz * U), tuple(rot), F.IDENT,
                        S * (KW.TEND_K if p in KW.TEND_PARTS else 1)))
        return out
    R['kw'] = (1.05, list(KW.POSES), kw)
    # (the rigkit rigs pick model variants by pose - ethereal, saddled, a face: each pose's rest is the idle pose in its variant)
    VAR = ('_eth', '_saddle', '_face')
    def rk(art, S):
        def make(p):
            if isinstance(p, tuple):                                  # (('rest', pose): the idle pose in that pose's variant)
                if p[1] not in art.POSES: p = ('rest', inbetweens(art)[p[1]][0])
                base = dict(art.POSES['idle_a']); base.update({k: v for k, v in art.POSES[p[1]].items() if k in VAR}); return F._rigkit(art, base, S)
            if p in art.POSES: return F._rigkit(art, art.POSES[p], S)
            return _blended(art, S, *inbetweens(art)[p])
        return make
    R['apo'] = (APO.PET_SCALE, list(APO.POSES) + list(inbetweens(APO)), rk(APO, APO.PET_SCALE))
    R['tul'] = (TUL.RIG_SCALE, list(TUL.POSES) + list(inbetweens(TUL)), rk(TUL, TUL.RIG_SCALE))
    zr = ZIB.zib_rig(); zp = ZIB.zib_poses()
    R['zib'] = (zr.S, list(zp), lambda p: [(f'bm:zbr_{n}', tuple(J), tuple(Rm), F.IDENT, zr.S) for n, (Rm, J) in zr.solve(zp[p]).items()])
    fr, fp = P63.frog_rig(), P63.frog_poses()
    R['frog'] = (fr.S, list(fp), lambda p: [(f'bm:frr_{n}' if n != 'head' else 'bm:frr_head_none', tuple(J), tuple(Rm), F.IDENT, fr.S) for n, (Rm, J) in fr.solve(fp[p]).items()])
    # Cecil (phase46): five parts at fixed joints, each frame a lean/tilt of the whole, plus a head turn and the arms' swing - the
    # same sums as phase46's cpose, frame for frame (walk, run, air, idle, sit, swim)
    import cecil2_art as CEC, math as _m
    from phase57_art import qa as _qa, qmul as _qm
    def _rot(q, v):
        x, y, z, w = q; cx = y * v[2] - z * v[1] + w * v[0]; cy = z * v[0] - x * v[2] + w * v[1]; cz = x * v[1] - y * v[0] + w * v[2]
        return (v[0] + 2 * (y * cz - z * cy), v[1] + 2 * (z * cx - x * cz), v[2] + 2 * (x * cy - y * cx))
    _qy = lambda a: (0.0, _m.sin(_m.radians(a) / 2), 0.0, _m.cos(_m.radians(a) / 2))
    CF = {f'w{i}': f for i, f in enumerate([(8, 4, 0.0, -5, -2, 28), (9, 2, 0.03, -6, -1, 20), (10, 0, 0.05, -7, 0, 8), (9, -2, 0.03, -6, 1, -2),
                                            (8, -4, 0.0, -5, 2, -8), (9, -2, 0.03, -6, 1, 0), (10, 0, 0.05, -7, 0, 12), (9, 2, 0.03, -6, -1, 22)])}
    CF.update({f'r{i}': f for i, f in enumerate([(16, 6, 0.0, -11, -3, 44), (17, 3, 0.05, -12, -1, 30), (18, 0, 0.09, -13, 0, 12), (17, -3, 0.05, -12, 1, -4),
                                                 (16, -6, 0.0, -11, 3, -12), (17, -3, 0.05, -12, 1, 2), (18, 0, 0.09, -13, 0, 20), (17, 3, 0.05, -12, -1, 36)])})
    CF.update({'air': (-5, 0, 0.08, 8, 0, 34), 'i0': (1.5, 0.8, 0.0, 3, -2, 0), 'i1': (-0.5, -0.8, 0.02, -2, 3, 2), 's0': (6, 0, -0.16, 12, -4, -4),
               's1': (7, 0, -0.17, 16, -6, -4)})
    CF.update({f'sw{i}': (6, 6 * _m.sin(2 * _m.pi * i / 8), -0.36 + 0.03 * _m.sin(4 * _m.pi * i / 8), -12, -4 * _m.sin(2 * _m.pi * i / 8), 44 + 18 * _m.sin(2 * _m.pi * i / 8))
               for i in range(8)})
    COFF = {'body': ((0, 0, 0), (0, 0.5, 0)), 'head': (CEC.HEAD_AT, (0, 0, 0)), 'eyes': (CEC.HEAD_AT, (0, 0, 0)), 'arm': (CEC.ARM_AT, (0, 0, 0)), 'larm': (CEC.LARM_AT, (0, 0, 0))}
    def cec(pose):
        lean, tilt, bob, hl, ht, af = CF[pose]
        R_ = _qm(_qa('x', lean), _qa('z', tilt)); out = []
        for p, (o, t) in COFF.items():
            L = R_
            if p in ('head', 'eyes'): L = _qm(R_, _qm(_qa('x', hl), _qa('z', ht)))
            if p == 'arm': L = _qm(R_, _qa('x', 6 - af))
            if p == 'larm': L = _qm(R_, _qa('x', 0.45 * af))
            rp = _rot(R_, tuple(o[i] + t[i] for i in range(3)))
            right = _qy(CEC.ARM_YAW) if p == 'arm' else (_qy(CEC.LARM_YAW) if p == 'larm' else F.IDENT)
            out.append((f'bm:cec2_{p}', (rp[0], rp[1] + bob, rp[2]), tuple(L), right, 1.0))
        return out
    R['cecil'] = (1.0, list(CF), cec)
    # (2.89: the deep's royals, Bloo and the Arachno-Lantern - rigkit rigs, measured in their own design scale)
    import ava_art as AVA, pearl_art as PQ, bloo_art as BLO, lantern_art as LAN
    for nm, art in (('ava', AVA), ('pearl', PQ), ('bloo', BLO), ('lantern', LAN)):
        R[nm] = (art.RIG_SCALE, list(art.POSES) + list(inbetweens(art)), rk(art, art.RIG_SCALE))
    dr, dp = P63.don_rig(), P63.don_poses()
    R['donado'] = (dr.S, list(dp), lambda p: [(f'bm:dnr_{n}' if n != 'head' else 'bm:dnr_head_none', tuple(J), tuple(Rm), F.IDENT, dr.S) for n, (Rm, J) in dr.solve(dp[p]).items()])
    return R


def inbetweens(art, ts=(0.33, 0.67)):
    """the frames the game shows between an animation's keyframes (each display slerps its rotation and lerps its
    translation on its own): {'anim:a>b@t': (a, b, t)}"""
    out = {}
    for anim, keys in getattr(art, 'ANIMS', {}).items():
        for (a, _), (b, _) in zip(keys, keys[1:]):
            if a == b: continue
            for t in ts: out.setdefault(f'{anim}:{a}>{b}@{t}', (a, b, t))
    return out


def _blended(art, S, a, b, t):
    import phase134 as F, rigkit as RK
    U = S / 16
    xa, xb = RK.solve(art.PIVOT, art.PARENT, art.POSES[a]), RK.solve(art.PIVOT, art.PARENT, art.POSES[b])
    xf = RK.blend(xa, xb, t); pose = art.POSES[b if t >= 0.5 else a]
    out = []
    for p in art.PARTS:
        # (a part either end hides is out of it: one going away shrinks where it is within 2 ticks - rigfol.pose - and one
        #  coming back grows from nothing where it was last seen)
        if art.HIDDEN(p, art.POSES[a]) or art.HIDDEN(p, art.POSES[b]): continue
        x, y, z = art.PIVOT[p]; q, tr = xf[p]
        out.append((f'bm:{art.model_name(p, pose)}', (-x * U + tr[0] * U, y * U + tr[1] * U, -z * U + tr[2] * U), tuple(q), F.IDENT, S * art.PART_K.get(p, 1.0)))
    return out


REST = {'cecil': 'i0', 'apo': 'idle_a', 'tul': 'idle_a', 'leo': 'idle_a', 'demo': 'idle_a', 'emma': 'idle_a', 'kw': 'idle_a', 'celi': 'idle', 'zib': 'idle0',
        'frog': 'idle0', 'donado': 'idle0', 'ava': 'idle_a', 'pearl': 'idle_a', 'bloo': 'idle_a', 'lantern': 'idle_a'}


def audit(name, S, poses, make, min_px=1.0, top=8, only=None, rp=RP):
    px = 16 / S                                                    # (blocks -> the rig's design pixels)
    rest_pose = REST.get(name, poses[0])
    key = lambda s, i: (s.boxes[i][1], s.boxes[i][2])            # (a box: its model and element number - the same box pose to pose)
    rests = {}
    def rest_for(pose):
        try:
            parts = make(('rest', pose.split(':', 1)[1].split('>')[0] if ':' in pose else pose)) if name in ('apo', 'tul', 'ava', 'pearl', 'bloo', 'lantern') else make(rest_pose)
        except Exception:
            parts = make(rest_pose)
        sig = tuple(m for m, *_r in parts)
        if sig not in rests:
            rs = build(parts, rp); r = {}
            for (i, j), d in pair_depths(rs.boxes).items():
                r[tuple(sorted((key(rs, i), key(rs, j))))] = d * px
            rests[sig] = r
        return rests[sig]
    report = {}
    for pose in poses:
        if only and pose not in only: continue
        rest = rest_for(pose)
        try:
            s = build(make(pose), rp)
        except Exception as e:
            report[pose] = [('?', '?', 0.0, f'{type(e).__name__}: {e}'[:60], '')]; continue
        worst = {}
        for (i, j), d in pair_depths(s.boxes).items():
            k = tuple(sorted((key(s, i), key(s, j))))
            extra = d * px - rest.get(k, 0.0)
            if extra < min_px: continue
            pa, pb = s.boxes[i][1], s.boxes[j][1]
            pk = tuple(sorted((pa, pb)))
            if extra > worst.get(pk, (0,))[0]:
                worst[pk] = (extra, s.boxes[i][4], s.boxes[j][4])
        if worst:
            report[pose] = sorted(((a, b, e, ta, tb) for (a, b), (e, ta, tb) in worst.items()), key=lambda r: -r[2])[:top]
    return report


if __name__ == '__main__':
    args = sys.argv[1:]
    min_px = float(args[args.index('--min') + 1]) if '--min' in args else 1.0
    top = int(args[args.index('--top') + 1]) if '--top' in args else 8
    only = args[args.index('--pose') + 1].split(',') if '--pose' in args else None
    names = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] not in ('--min', '--top', '--pose'))]
    R = rigs()
    total = 0
    for name in (names or list(R)):
        S, poses, make = R[name]
        rep = audit(name, S, poses, make, min_px, top, only)
        print(f'=== {name}: {len(poses)} poses, {len(rep)} with clipping >= {min_px} px')
        for pose, rows in rep.items():
            total += len(rows)
            print(f'  {pose}: ' + '; '.join(f'{a.split("_", 1)[-1]}x{b.split("_", 1)[-1]} {e:.1f}px ({ta.split("/")[-1][:14]}|{tb.split("/")[-1][:14]})' for a, b, e, ta, tb in rows))
    print('total flagged pairs:', total)
