"""2.78: the wall-mount transforms for phase135's XF table - each 3D model's long axis up the plaque's diagonal, its thin side to the wall,
its back just off the board - and a preview render of each (python3 tools/mount_xf.py, from bm_build)."""
import sys, json, math
sys.path.insert(0, '/home/user/main/bm_build')
import numpy as np
from tools.render import Scene

def quat_of(R):
    t = np.trace(R)
    if t > 0:
        s = math.sqrt(t + 1) * 2; w = s / 4; x = (R[2][1] - R[1][2]) / s; y = (R[0][2] - R[2][0]) / s; z = (R[1][0] - R[0][1]) / s
    else:
        i = int(np.argmax([R[0][0], R[1][1], R[2][2]]))
        if i == 0: s = math.sqrt(1 + R[0][0] - R[1][1] - R[2][2]) * 2; x = s / 4; y = (R[0][1] + R[1][0]) / s; z = (R[0][2] + R[2][0]) / s; w = (R[2][1] - R[1][2]) / s
        elif i == 1: s = math.sqrt(1 + R[1][1] - R[0][0] - R[2][2]) * 2; y = s / 4; x = (R[0][1] + R[1][0]) / s; z = (R[1][2] + R[2][1]) / s; w = (R[0][2] - R[2][0]) / s
        else: s = math.sqrt(1 + R[2][2] - R[0][0] - R[1][1]) * 2; z = s / 4; x = (R[0][2] + R[2][0]) / s; y = (R[1][2] + R[2][1]) / s; w = (R[1][0] - R[0][1]) / s
    return [round(float(v), 4) for v in (x, y, z, w)]

def auto(lo, hi, tip, out, L, front=0.07):
    tip = np.array(tip, float); tip /= np.linalg.norm(tip); out = np.array(out, float); out -= tip * (out @ tip); out /= np.linalg.norm(out)
    Mf = np.column_stack([tip, np.cross(out, tip), out])
    d = np.array([1, 1, 0]) / math.sqrt(2); z = np.array([0, 0, 1.0])
    W = np.column_stack([d, np.cross(z, d), z])
    A = W @ Mf.T
    Ry = np.diag([-1, 1, -1.0])
    Lq = A @ Ry
    cs = np.array([[x, y, zz] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for zz in (lo[2], hi[2])]) / 16 - 0.5
    ext = (cs @ tip).max() - (cs @ tip).min()
    s = L / ext
    v = (s * (A @ cs.T)).T
    T = [-(v[:, 0].max() + v[:, 0].min()) / 2, -(v[:, 1].max() + v[:, 1].min()) / 2, front - v[:, 2].min()]
    return quat_of(Lq), round(float(s), 4), tuple(round(float(t), 4) for t in T)

M = {'cecil_staff': ('bm:item/cecil_staff', (2.7, -13.6, 3.94), (13.3, 20.72, 5.97), (0, 1, 0), (0, 0, 1), 1.2),
     'leo_trident': ('bm:item/le_trident', (5.6, -3.8, 7.32), (10.4, 31.0, 8.68), (0, 1, 0), (0, 0, 1), 1.2),
     'apo_mace': ('bm:item/apo_mace_held', (2.2, -13.6, -3.02), (13.8, 17.63, 19.02), (0, 1, 0), (-1, 0, 0), 1.05),
     'frisbee_shield': ('bm:item/frisbee_shield', (0, 7.25, 0), (16, 8.75, 16), (0, 0, -1), (0, 1, 0), 0.62)}
if __name__ == '__main__':
    for k, (mid, lo, hi, tip, out, L) in M.items():
        q, s, t = auto(lo, hi, tip, out, L)
        print(f"'{k}': ({q}, {s}, {t}),")
        sc = Scene(rp='/home/user/main/bm_build/out_p2/BlackMarket_RP')
        sc.solid((-0.5, 0.5, -0.1), (0.5, 1.5, 0.0), '#808080')         # the wall (its face at z = 0, the entity 1 up)
        c = 0.7071 * 0.62
        sc.display(mid, pos=(0, 1, 0), yaw=0, translation=t, scale=s, left=q, ctx='none')
        sc.save(f'/tmp/mount_{k}.png', views=('front', 'side'), span=1.8, center=(0, 1, 0))
