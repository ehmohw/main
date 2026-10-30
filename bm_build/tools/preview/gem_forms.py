"""(3.0a) The Gem of Creativity's two forms - preview sheets.  python3 tools/preview/gem_forms.py [both,faces,wings,night,looks,orbit,clip]
Writes to $BM_PREVIEW_DIR (default: previews/v300a_gem_ethereal); the throwaway packs go to $BM_SCRATCH (default /tmp/bm_previews).
both   gem_forms_both.png: its own form, a player, the Ethereal Form, the Wraithfire Form - front, three-quarter, back
faces  gem_forms_faces.png: every emoticon on each form's table
wings  gem_forms_wings.png: the wings in its poses - at rest and beating, spread (conjuring, leaping, a twirl), folded back (walking,
       seated, tired)
night  gem_forms_night.png: both forms by night (tools/render has no light: unlit faces dimmed, lit ones kept by their level)
looks  gem_forms_looks.png: the wardrobe's looks and the shiny on the Ethereal Form (phase138's recolour: the swirl, and the shards
       on its range); the Wraithfire Form keeps its own colours
orbit  gem_forms_orbit.png / .gif: the halo circling a form (phase231's _spin: its right_rotation, a step every few ticks)
clip   gem_forms_clip.txt: per pose and form, the halo's glints against the wings and the gem (they must never meet), the wings
       against the gem beyond their roots, and the lowest point"""
import sys, os, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
os.environ.setdefault('BM_PREVIEW_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300a_gem_ethereal'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import draftkit as K, gem_art as A, rigkit
from rigkit import qs
from tools import render as R
OUT = os.environ['BM_PREVIEW_DIR']; os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews'); os.makedirs(SCRATCH, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['both', 'faces', 'wings', 'night', 'looks', 'orbit', 'clip']
I = A.POSES['idle_a']
TEX = A.textures()
NIGHT_BG, NIGHT_GRID = (16, 18, 34), (34, 38, 52)
NAMES = {'': 'its own form', '_e': 'ETHEREAL', '_w': 'WRAITHFIRE'}
ROOTS = {}


def root(frame=0):
    """the art packed, each animated strip cut to one frame"""
    if frame not in ROOTS:
        r = K.pack(A, f'{SCRATCH}/rp_gemf_f{frame}')
        for k in A.ANIMATED:
            TEX[k].crop((0, frame * A.N, A.N, (frame + 1) * A.N)).save(f'{r}/assets/bm/textures/block/{k}.png')
        ROOTS[frame] = r
    return ROOTS[frame]


def font(sz, bold=True):
    try: return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if bold else ""}.ttf', sz)
    except OSError: return None


def night_scene(*roots):
    """a Scene whose display() tints every face by its element's light_emission (dim night when 0)"""
    s = K.multi_scene(*roots); base = s.display

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            k = 0.22 + 0.78 * (L / 15) ** 0.8 if L else None
            tint = np.array([0.16, 0.17, 0.27]) if not L else np.array([k, k * 0.98, k * 0.92])
            s.faces[n0 + i] = (f[0], f[1], f[2], False if L else f[3], tint)
    s.display = display

    def solid(lo, hi, color='#c08060'):
        c = tuple(int(int(color[i:i + 2], 16) * 0.22) for i in (1, 3, 5))
        R.Scene.solid(s, lo, hi, '#%02x%02x%02x' % c)
    s.solid = solid
    return s


def darken(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 2)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 2) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 2)
    a[sky] = NIGHT_BG; a[grid] = NIGHT_GRID
    return Image.fromarray(a.astype(np.uint8))


def dark_label(im, text, sub=None):
    d = ImageDraw.Draw(im); d.text((8, 6), text, fill=(235, 228, 210), font=font(15))
    if sub: d.text((8, 25), sub, fill=(170, 170, 190), font=font(12, False))
    return im


def gem(s, pose, sfx='', at=(0.0, 0, 0), face=None, look=None, halo_deg=0.0, yaw=0.0):
    """the Gem posed in a form (sfx), its face an emoticon key (None: its plain :) ), a look's '_c<k>' over it"""
    def name(p, pz, suffix=''):
        if p == 'head' and face and face != 'smile':
            n = f'cg_head_x{face}{sfx}'
        else:
            n = f'cg_{p}{sfx}'
        return n + (f'_c{look}' if look and p in ('body', 'halo', 'wing_r', 'wing_l') else '')
    keep = A.model_name
    A.model_name = name
    try:
        rigkit.render(s, A, dict(pose, halo=qs(('y', halo_deg))) if halo_deg else pose, at=at, scale=A.RIG_SCALE, yaw=yaw)
    finally:
        A.model_name = keep


def scene(night=False, frame=0, extra=()):
    return (night_scene if night else K.multi_scene)(root(frame), *extra)


def label(im, text, sub=None, night=False):
    return dark_label(darken(im), text, sub) if night else K.label(im, text, sub)


def tile(pose, sfx, view=(-30, 12), span=2.3, center=(0, 1.05, 0), size=330, text='', sub=None, night=False, face=None, look=None, frame=0, halo_deg=0.0, extra=()):
    s = scene(night, frame, extra); gem(s, pose, sfx, face=face, look=look, halo_deg=halo_deg)
    return label(s.render(view, size=size, span=span, center=center), text, sub, night)


def lineup(view, text, sub=None, night=False, size=640, pose=I, frame=0):
    """its own form - a player - the Ethereal Form - the Wraithfire Form"""
    s = scene(night, frame)
    for x, sfx in ((-1.9, ''), (0.75, '_e'), (2.85, '_w')):
        gem(s, pose, sfx, at=(x, 0, 0))
    K.person(s, (-0.6, 0, 0.0))
    return label(s.render(view, size=size, span=6.4, center=(0.45, 1.05, 0)), text, sub, night)


if 'both' in what:
    K.sheet([lineup('front', 'front', 'its own form - a player - Ethereal - Wraithfire'), lineup((-35, 12), 'three-quarter'), lineup('back', 'back (the wings at its back)'),
             lineup((-90, 8), 'side')],
            OUT + '/gem_forms_both.png', cols=2, title='The Gem of Creativity - its own form, the Ethereal Form, the Wraithfire Form (beside a player)')
    for sfx in ('_e', '_w'):
        K.sheet([tile(I, sfx, v, text=t, size=380, frame=(i * 7) % A.FRAMES) for i, (v, t) in enumerate(
            (('front', 'front'), ((-35, 12), 'front 3/4'), ('side', 'side'), ((145, 15), 'back 3/4'), ('back', 'back'), ((-30, 55), 'from above')))],
                OUT + f'/gem_form{sfx}_turnaround.png', cols=3, title=f'The Gem of Creativity - {NAMES[sfx].capitalize()} Form, all round')

if 'faces' in what:
    for sfx in ('_e', '_w'):
        tiles = [tile(I, sfx, 'front', span=1.35, center=(0, 1.08, 0), size=210, text=t, face=k) for k, t in A.EMOTES]
        K.sheet(tiles, OUT + f'/gem_form{sfx}_faces.png', cols=7, title=f'{NAMES[sfx].capitalize()} Form - every emoticon on its table ({len(A.EMOTES)})')

if 'wings' in what:
    for sfx in ('_e', '_w'):
        names = ['idle_a', 'idle_b', 'conjure_up', 'conjure', 'jump', 'happy', 'walk_1', 'run_1', 'sit_b', 'sit_a', 'hurt', 'tired']
        tiles = [tile(A.POSES[n], sfx, (-30, 14), text=n, sub='lift %d, sweep %d' % A.WING_POSE.get(n, (0, 0)), frame=(i * 5) % A.FRAMES, size=300)
                 for i, n in enumerate(names)]
        tiles += [tile(A.POSES['conjure'], sfx, (180, 18), text='conjure, from behind', sub='spread', size=300),
                  tile(A.POSES['jump'], sfx, (0, -25), text='leaping, from below', sub='flying', size=300)]
        K.sheet(tiles, OUT + f'/gem_form{sfx}_wings.png', cols=7, title=f'{NAMES[sfx].capitalize()} Form - its wings: beating at rest, spread to conjure and leap, folded back to walk and rest')

if 'night' in what:
    K.sheet([lineup('front', 'by night', 'its own form - a player - Ethereal - Wraithfire', night=True),
             lineup((-35, 12), 'by night, 3/4', night=True),
             lineup((-35, 12), 'by night, spread (conjuring)', night=True, pose=A.POSES['conjure'])],
            OUT + '/gem_forms_night.png', cols=1, title='By night - the crystal points, the wings, the halo and its face glow; its facets don\'t')

if 'looks' in what:
    import phase99 as P99, phase138 as P138, gild
    import phase231                                       # (it hands the shards to phase138's SIDE and RECOL)
    keys = P138.RECOL['gem'][1]
    tiles = [tile(I, '_e', text='Ethereal - its own colours')]
    for k, (nm, pal) in P99.NEW['gem'][3].items():
        r = f'{SCRATCH}/rp_gemf_look{k}'; os.makedirs(f'{r}/assets/bm/textures/block', exist_ok=True); os.makedirs(f'{r}/assets/bm/models/item', exist_ok=True)
        base = {n: (TEX[n].crop((0, 0, A.N, A.N)) if n in A.ANIMATED else TEX[n]) for n in keys}
        if gild.is_gilded('gem', k):
            ims = {n: gild.dress('gem', k, base[n]) for n in keys}
        else:
            main = {n: base[n] for n in keys if n not in P138.SIDE}
            ims = P99._recolour(main, pal)
            side = {n: base[n] for n in keys if n in P138.SIDE}
            if side: ims.update(P99._recolour(side, pal, rng=P99._lumrange(main)))
        for n, im in ims.items():
            im.save(f'{r}/assets/bm/textures/block/{n}_c{k}.png')
        for mn in ('cg_body_e', 'cg_halo_e', 'cg_wing_r_e', 'cg_wing_l_e'):
            m = json.load(open(f'{root()}/assets/bm/models/item/{mn}.json'))
            m['textures'] = {a: (v + f'_c{k}' if v.split('/')[-1] in keys else v) for a, v in m['textures'].items()}
            json.dump(m, open(f'{r}/assets/bm/models/item/{mn}_c{k}.json', 'w'))
        s = K.multi_scene(r, root()); gem(s, I, '_e', look=k)
        tiles.append(K.label(s.render((-30, 12), size=330, span=2.3, center=(0, 1.05, 0)), f'Ethereal - {nm}', f'look {k}'))
    tiles.append(tile(I, '_w', text='Wraithfire - in any look', sub='its own colours: a form outranks a look'))
    K.sheet(tiles, OUT + '/gem_forms_looks.png', cols=5, title='The looks on the Ethereal Form (swirl and shards recoloured); the Wraithfire Form keeps its own')

if 'orbit' in what:
    for sfx in ('_e', '_w'):
        N = 24; frames = []
        for k in range(N):
            deg = 360.0 * k / N
            frames.append(tile(I, sfx, (-30, 14), span=2.3, size=300, text=f'{k * A.HALO_TURN // N} ticks', sub=f'halo turned {deg:.0f} deg',
                               frame=(k * 4) % A.FRAMES, halo_deg=deg))
        K.sheet(frames[::3], OUT + f'/gem_form{sfx}_orbit.png', cols=4, title=f'{NAMES[sfx].capitalize()} Form - its halo circling (a full turn in {A.HALO_TURN / 20:.0f} s; every 3rd step of {N})')
        frames[0].save(OUT + f'/gem_form{sfx}_orbit.gif', save_all=True, append_images=frames[1:], duration=A.HALO_TURN * 50 // N, loop=0)


# ---------------------------------------------------------------------------------------------------- clipping
class _Rec:
    def __init__(self): self.d = []
    def display(self, mid, pos, yaw, translation, scale, left): self.d.append((mid, pos, yaw, translation, scale, left))


def boxes(pose, sfx, halo_deg=0.0):
    rec = _Rec(); gem(rec, pose, sfx, halo_deg=halo_deg)
    out = []
    for (mid, pos, yaw, tr, sc, left), p in zip(rec.d, [p for p in A.PARTS if not A.HIDDEN(p, pose)]):
        nm = mid.split('/')[-1]
        m = json.load(open(f'{root()}/assets/bm/models/item/{nm}.json'))
        Q = R.quat(left); E = R.ry(math.radians(-yaw))
        for i, e in enumerate(m['elements']):
            f, t = e['from'], e['to']
            cs = [np.array((x, y, z), float) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])]
            r = e.get('rotation')
            if r:
                o = np.array(r['origin'])
                Mx = {'x': R.rx, 'y': R.ry, 'z': R.rz}[r['axis']](math.radians(r['angle'])) if 'axis' in r else \
                    R.rz(math.radians(r.get('z', 0))) @ R.ry(math.radians(r.get('y', 0))) @ R.rx(math.radians(r.get('x', 0)))
                cs = [Mx @ (c - o) + o for c in cs]
            w = [E @ (Q @ (sc * (R.ry(math.pi) @ (c / 16 - 0.5))) + np.array(tr)) + np.array(pos) for c in cs]
            out.append((p, np.array(w), i))
    return out


def _sat(a, b):
    def axes(c): return [c[4] - c[0], c[2] - c[0], c[1] - c[0]]
    ax = [v for v in axes(a) + axes(b) if np.linalg.norm(v) > 1e-6]
    for u, v in itertools.product(axes(a), axes(b)):
        x = np.cross(u, v)
        if np.linalg.norm(x) > 1e-6: ax.append(x)
    depth = 1e9
    for v in ax:
        v = v / np.linalg.norm(v); pa, pb = a @ v, b @ v
        d = min(pa.max(), pb.max()) - max(pa.min(), pb.min())
        if d <= 0: return 0.0
        depth = min(depth, d)
    return depth


if 'clip' in what:
    U = A.RIG_SCALE / 16
    lines = []
    names = [n for n in A.POSES if not n.startswith('swim_') or n in ('swim_0', 'swim_2', 'swim_4', 'swim_6')]
    worst = 0.0
    for sfx in ('_e', '_w'):
        for n in names:
            pose = A.POSES[n]
            hits = {}
            for hd in range(0, 360, 15):                   # (the halo all the way round)
                bx = boxes(pose, sfx, hd)
                halo = [b for b in bx if b[0] == 'halo']
                rest = [b for b in bx if b[0] in ('body', 'wing_r', 'wing_l', 'head')]
                for (pa, ca, ia), (pb, cb, ib) in itertools.product(halo, rest):
                    d = _sat(ca, cb) / U
                    if d > 0.0: hits[f'halo/{pb}'] = max(hits.get(f'halo/{pb}', 0), d)
                if hd: continue
                # the wings against the gem: past their roots (a shard's first box and the knot meet it on purpose)
                body = [b for b in bx if b[0] == 'body']
                for (pa, ca, ia) in [b for b in bx if b[0] in ('wing_r', 'wing_l')]:
                    nb = len([1 for b in bx if b[0] == pa])
                    if ia % 4 == 0 or ia == nb - 1: continue
                    for (pb, cb, ib) in body:
                        d = _sat(ca, cb) / U
                        if d > 0.25: hits[f'{pa}/body'] = max(hits.get(f'{pa}/body', 0), d)
                if sfx and n == names[0]: pass
            low = min(c[:, 1].min() for p, c, i in boxes(pose, sfx)) / U
            worst = max([worst] + [v for k, v in hits.items() if k.startswith('halo')])
            lines.append(f'{NAMES[sfx]:10s} {n:12s} lowest {low:+6.2f}  ' + ('  '.join(f'{k} {d:.2f}' for k, d in sorted(hits.items())) or 'clean'))
    txt = '\n'.join(lines) + f'\n(design units; the halo checked every 15 deg of its turn) halo contacts: {"none" if worst == 0 else worst}\n'
    open(OUT + '/gem_forms_clip.txt', 'w').write(txt); print(txt)
