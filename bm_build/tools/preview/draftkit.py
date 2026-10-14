"""Character draft previews (never shipped): pack an art module's textures + models into a throwaway resource pack, then
pose and render it with tools/render.Scene - rigkit modules (hierarchical) or flat phase57-style ones - into sheets and GIFs.
Output goes to $BM_PREVIEW_DIR (default /tmp/bm_previews). The shipped pack (out_p2) must be built: shared textures and the
other characters in a lineup come from it."""
import sys, os, json, math, shutil
BM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BM)
from PIL import Image, ImageDraw, ImageFont
from tools.render import Scene
import rigkit

OUT = os.environ.get('BM_PREVIEW_DIR', '/tmp/bm_previews')
REAL = os.path.join(BM, 'out_p2', 'BlackMarket_RP')


def pack(mod, root):
    os.makedirs(f'{root}/assets/bm/models/item', exist_ok=True); os.makedirs(f'{root}/assets/bm/textures/block', exist_ok=True)
    for k, im in mod.textures().items(): im.save(f'{root}/assets/bm/textures/block/{k}.png')
    for name, (tex, els) in mod.models().items():
        t = dict(tex); t['particle'] = next(iter(tex.values()))
        json.dump({'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}},
                  open(f'{root}/assets/bm/models/item/{name}.json', 'w'))
        for v in tex.values():                         # (textures shared with shipped items: taken from the real pack)
            if v.startswith('bm:block/'):
                k = v.split('/', 1)[1]; dst = f'{root}/assets/bm/textures/block/{k}.png'; src = f'{REAL}/assets/bm/textures/block/{k}.png'
                if not os.path.exists(dst) and os.path.exists(src): shutil.copy(src, dst)
    return root


def put_flat(s, mod, pose, at=(0, 0, 0), yaw=0, prefix=None, scale=None):
    sc = scale or mod.RIG_SCALE; U = sc / 16; prefix = prefix or mod.PREFIX
    for p in mod.PARTS:
        if hasattr(mod, 'HIDDEN') and mod.HIDDEN(p, pose): continue
        x, y, z = mod.joint(p)
        rot, tr = mod.part_xf(pose, p)
        k = sc / mod.RIG_SCALE
        tr = (tr[0] * k, tr[1] * k, tr[2] * k)
        cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        wx, wz = -x * U, -z * U
        name = mod.model_name(p, pose) if hasattr(mod, 'model_name') else f'{prefix}_{p}'
        s.display(f'bm:item/{name}', pos=(at[0] + wx * cy - wz * sy, at[1] + y * U, at[2] + wx * sy + wz * cy), scale=sc, left=tuple(rot), translation=tr, yaw=yaw)


def label(im, text, sub=None):
    d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15); g = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    except OSError: f = g = None
    d.text((8, 6), text, fill=(30, 30, 30), font=f)
    if sub: d.text((8, 25), sub, fill=(90, 90, 90), font=g)
    return im


def sheet(tiles, out, cols=4, bg='white', title=None):
    W, H = tiles[0].size; rows = (len(tiles) + cols - 1) // cols; top = 40 if title else 0
    sh = Image.new('RGB', (W * cols, H * rows + top), bg)
    if title:
        d = ImageDraw.Draw(sh)
        try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
        except OSError: f = None
        d.text((12, 8), title, fill=(20, 20, 20), font=f)
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * W, top + (i // cols) * H))
    sh.save(out); return out


REAL_RP = REAL


def multi_scene(*roots):
    """a Scene that finds models/textures in several packs (a draft's scratch pack, then the real one, then vanilla)"""
    from tools.render import VANILLA
    s = Scene(roots[0])
    def _path(ns_id, kind, ext):
        ns, p = ns_id.split(':') if ':' in ns_id else ('minecraft', ns_id)
        for root in [os.path.join(r, 'assets') for r in roots] + [VANILLA]:
            f = os.path.join(root, ns, kind, p + ext)
            if os.path.exists(f): return f
        raise FileNotFoundError(ns_id)
    s._path = _path
    return s


def put_shipped(s, mod, prefix, pose, at=(0, 0, 0), yaw=0, parts=None, scale=None):
    """a shipped flat rig (Emma: phase57_art 'em', Leo: phase96_art 'le', ...) from the real pack, posed"""
    sc = scale or mod.RIG_SCALE; U = sc / 16
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    for p in (parts or mod.PARTS):
        x, y, z = mod.joint(p) if hasattr(mod, 'joint') else mod.PIVOT[p]
        rot, tr = mod.part_xf(pose, p)
        k = sc / mod.RIG_SCALE; tr = (tr[0] * k, tr[1] * k, tr[2] * k)
        tr = (tr[0] * cy - tr[2] * sy, tr[1], tr[0] * sy + tr[2] * cy) if yaw else tr
        wx, wz = -x * U, -z * U
        s.display(f'bm:item/{prefix}_{p}', pos=(at[0] + wx * cy - wz * sy, at[1] + y * U, at[2] + wx * sy + wz * cy), scale=sc, left=tuple(rot), translation=tr, yaw=yaw)


def person(s, at=(0, 0, 0), sit=False, shirt='#2f9ec4', skin='#c8956c', pants='#3a3aa0', hair='#4a2c14'):
    """a plain player figure of solid boxes (1.8 tall standing) - for scale, or astride a mount (sit=True: at = the seat)"""
    x, y, z = at
    if sit:                                                                                       # (facing +z, astride: legs down both flanks)
        s.solid((x - 0.25, y, z - 0.1), (x + 0.25, y + 0.75, z + 0.15), shirt)                       # body
        s.solid((x - 0.25, y + 0.75, z - 0.25), (x + 0.25, y + 1.25, z + 0.25), skin)                # head
        s.solid((x - 0.27, y + 1.12, z - 0.27), (x + 0.27, y + 1.27, z + 0.27), hair)
        for sx in (-1, 1):
            x0, x1 = sorted((x + sx * 0.05, x + sx * 0.42))
            s.solid((x0, y - 0.05, z - 0.1), (x1, y + 0.2, z + 0.45), pants)                         # thighs, splayed over his back
            s.solid((x0 + sx * 0.12, y - 0.55, z + 0.2), (x1 + sx * 0.12, y + 0.0, z + 0.45), pants)    # shins down his flanks
            a0, a1 = sorted((x + sx * 0.25, x + sx * 0.5))
            s.solid((a0, y + 0.3, z + 0.05), (a1, y + 0.6, z + 0.55), shirt)                          # arms reaching forward to the reins
        return
    s.solid((x - 0.25, y + 0.75, z - 0.13), (x + 0.25, y + 1.5, z + 0.13), shirt)
    s.solid((x - 0.25, y + 1.5, z - 0.25), (x + 0.25, y + 2.0, z + 0.25) if False else (x + 0.25, y + 1.8 + 0.2, z + 0.25), skin)
    s.solid((x - 0.27, y + 1.86, z - 0.27), (x + 0.27, y + 2.02, z + 0.27), hair)
    s.solid((x - 0.25, y, z - 0.13), (x + 0.25, y + 0.75, z + 0.13), pants)
    s.solid((x - 0.5, y + 0.75, z - 0.13), (x - 0.25, y + 1.5, z + 0.13), skin); s.solid((x + 0.25, y + 0.75, z - 0.13), (x + 0.5, y + 1.5, z + 0.13), skin)


def slerp_pose(a, b, t, parts):
    """between two rigkit poses (eased), quaternion by quaternion"""
    t = t * t * (3 - 2 * t); out = {}
    I = (0.0, 0.0, 0.0, 1.0)
    for p in parts:
        qa, qb = a.get(p, I), b.get(p, I)
        if sum(x * y for x, y in zip(qa, qb)) < 0: qb = tuple(-v for v in qb)
        q = tuple(x * (1 - t) + y * t for x, y in zip(qa, qb)); n = math.sqrt(sum(v * v for v in q))
        out[p] = tuple(v / n for v in q)
    oa, ob = a.get('_off', (0, 0, 0)), b.get('_off', (0, 0, 0))
    out['_off'] = tuple(x * (1 - t) + y * t for x, y in zip(oa, ob))
    for k in ('_eth', '_face'):
        v = a.get(k) if t < 0.5 else b.get(k)
        if v: out[k] = v
    return out


def anim_frames(poses, seq, step=3, parts=()):
    """keyframes [(pose name, ticks to reach it)] looped -> per-frame poses, a frame every `step` ticks"""
    frames = []
    for i, (name, ticks) in enumerate(seq):
        prev = poses[seq[i - 1][0]]
        for k in range(0, ticks, step):
            frames.append(slerp_pose(prev, poses[name], k / ticks, parts))
    return frames


def gif(images, out, step=3):
    images[0].save(out, save_all=True, append_images=images[1:], duration=step * 50, loop=0, optimize=True)
    return out


def anim_world(rig, seq, step=2):
    """keyframes [(pose, ticks to reach it)] looped -> [(solved transforms, pose for names/flags)], blended part by part in
    the world as the game interpolates each display (eased between keyframes)"""
    frames = []
    for i, (name, ticks) in enumerate(seq):
        a, b = rig.POSES[seq[i - 1][0]], rig.POSES[name]
        xa, xb = rigkit.solve(rig.PIVOT, rig.PARENT, a), rigkit.solve(rig.PIVOT, rig.PARENT, b)
        for k in range(0, ticks, step):
            t = k / ticks; t = t * t * (3 - 2 * t)
            frames.append((rigkit.blend(xa, xb, t), a if t < 0.5 else b))
    return frames
