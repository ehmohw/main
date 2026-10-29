"""The Ophanim (ophan_art.py) - the Lightbringer's "wheel within a wheel" form.   python3 tools/preview/ophan.py [form,dark,spin,parts]
form   ophan.png: the form from the front, three-quarter and below, beside the Lightbringer (idle_a) and a player for scale
dark   ophan_dark.png: the same in the dark - light_emission only (eyes, fire, core, the inner ring), and with the brightness
       override (GLOW), a bloom over what's lit (tools/render has no lights: faces are tinted after the scene is built, as mire.py)
spin   ophan_spin.png: four frames of the wheels turning (each about its own axis, SPIN_AXIS), three-quarter
parts  ophan_parts.png: each part alone, so the wheels and the core read on their own
Uses draftkit (packs, scenes, sheets), playerkit (the player) and lightbringer_art's rig. PNGs to $OPH_OUT (default
/home/user/main/previews/v299a_ophan); the throwaway packs to $BM_PREVIEW_DIR."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import draftkit as K
import playerkit as PK
import rigkit
from rigkit import qs
import ophan_art as A
import lightbringer_art as LA

OUT = os.environ.get('OPH_OUT', '/home/user/main/previews/v299a_ophan'); os.makedirs(OUT, exist_ok=True)
os.makedirs(K.OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['form', 'dark', 'spin', 'parts']
print({p: tuple(round(v, 2) for v in hb) for p, hb in A.check().items()})
ROOT = K.pack(A, K.OUT + '/rp_oph')
ROOT_LB = K.pack(LA, K.OUT + '/rp_lb')
try:
    FNB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16); FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
    FNH = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except OSError:
    FNB = FNT = FNH = None

U = A.SCALE / 16
BALL = A._ball(A.BUILD['ring_a']()) * U                     # (blocks, the flames' tips)
CY = BALL + 0.6                                             # the construct's centre, hovering
FLOOR = ('#3c3a46', '#47454f')
LB_AT, P_AT = (4.6, 0.0, 0.4), (5.9, 0.0, 0.2)              # the Lightbringer and a player, beside it
# a turned pose, so all three wheels read as wheels (at rest they'd sit square on to the view)
POSE = {'ring_a': qs(('y', 28)), 'ring_b': qs(('x', 38)), 'ring_c': qs(('z', -35)), 'core': qs(('y', 20))}


def ophan(s, pose=POSE, at=(0.0, CY, 0.0), scale=A.SCALE):
    for p in A.PARTS:
        s.display(f'bm:item/{A.model_id(p)}', pos=at, scale=scale, left=tuple(pose.get(p, rigkit.I)))


def floor(s, r=7, cols=FLOOR):
    for i in range(-r, r):
        for j in range(-r, r):
            s.solid((i, -0.25, j), (i + 1, 0.0, j + 1), cols[(i + j) % 2])


def cull(s, view, **kw):
    """Scene.render with the Lightbringer's own faces culled when they face away (the game culls a translucent item's back
    faces - lightbringer.py's way)"""
    V = view if isinstance(view, tuple) else {'front': (0, 0), 'back': (180, 0), 'side': (90, 0), 'iso': (35, 25)}[view]
    yw, pt = math.radians(V[0]), math.radians(V[1])
    fwd = np.array([-math.sin(yw) * math.cos(pt), -math.sin(pt), -math.cos(yw) * math.cos(pt)])
    keep = []
    for f in s.faces:
        if f[0] != 'box' and isinstance(f[2], str) and (f[2].startswith('bm:block/lb_') or f[2] == 'bm:block/oph_aura'):
            p = [np.array(v) for v in f[0]]
            if np.cross(p[1] - p[0], p[3] - p[0]) @ fwd < -1e-9: continue
        keep.append(f)
    allf, s.faces = s.faces, keep
    try: return s.render(view, **kw)
    finally: s.faces = allf


def dark_bg(im, top=(30, 26, 48), bot=(8, 7, 14)):
    """the renderer's sky (and its little grid) swapped for a dark gradient"""
    a = np.asarray(im).astype(np.float32); h, w = a.shape[:2]
    m = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8) | (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | \
        (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    t = np.linspace(0, 1, h)[:, None, None]
    g = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return Image.fromarray(np.where(m[..., None], np.broadcast_to(g, a.shape), a).astype(np.uint8))


def bloom(im, thr=200, r=10, k=0.85):
    """a soft glow round what's bright (the game's own light doesn't bloom, but this is how the eyes and fire read at night)"""
    a = np.asarray(im).astype(np.float32)
    lum = a.mean(axis=2)
    m = np.where((lum > thr)[..., None], a, 0).astype(np.uint8)
    g = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(r))).astype(np.float32)
    g2 = np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(r * 3))).astype(np.float32)
    out = 255 - (255 - a) * (1 - np.clip((g * k + g2 * k * 0.8) / 255, 0, 1))
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def label(im, text, sub=None, col=(250, 238, 205), sub_col=(185, 175, 160)):
    d = ImageDraw.Draw(im); d.text((10, 8), text, fill=col, font=FNB)
    if sub: d.text((10, 28), sub, fill=sub_col, font=FNT)
    return im


def sheet(tiles, out, cols, title=None, bg=(14, 12, 22)):
    W, H = tiles[0].size; rows = (len(tiles) + cols - 1) // cols; top = 44 if title else 0
    sh = Image.new('RGB', (W * cols, H * rows + top), bg)
    if title: ImageDraw.Draw(sh).text((12, 10), title, fill=(250, 238, 205), font=FNH)
    for i, t in enumerate(tiles): sh.paste(t, ((i % cols) * W, top + (i // cols) * H))
    sh.save(out); print(out); return out


def scene(dark=None, others=True, fl=True, pose=POSE):
    """the Ophanim (and the Lightbringer and a player beside it). dark: None (daylight), 'emit' (light_emission only) or 'glow'
    (the brightness override on the Ophanim's parts)"""
    s = K.multi_scene(ROOT, ROOT_LB)
    if dark:
        base, s_solid = s.display, s.solid
        def display(mid, **kw):
            n0 = len(s.faces); base(mid, **kw)
            mine = mid.split('/')[-1].startswith(A.PREFIX)
            lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
            for i, L in enumerate(lights):
                f = s.faces[n0 + i]
                if mine and (L or dark == 'glow'):
                    s.faces[n0 + i] = (f[0], f[1], f[2], f[3] if not L else False, np.array([1.0, 1.0, 1.0]))
                elif L:
                    k = 0.35 + 0.65 * (L / 15) ** 0.8
                    s.faces[n0 + i] = (f[0], f[1], f[2], f[3], np.array([k, k, k]))
                else:                                          # (moonlight - and the Ophanim's own light on what's near it)
                    s.faces[n0 + i] = (f[0], f[1], f[2], f[3], np.array([0.42, 0.40, 0.46]) if mine else np.array([0.30, 0.29, 0.36]))
        def solid(lo, hi, color='#c08060'):
            c = color.lstrip('#'); rgb = np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)]) * np.array([0.30, 0.29, 0.34])
            s_solid(lo, hi, '#%02x%02x%02x' % tuple(int(v) for v in rgb))
        s.display, s.solid = display, solid
    ophan(s, pose)
    if others:
        rigkit.render(s, LA, LA.POSES['idle_a'], at=LB_AT, scale=LA.RIG_SCALE, yaw=-20)
        n0 = len(s.faces); PK.put(s, PK.player('stand'), at=P_AT, yaw=-10)
        if dark:
            for i in range(n0, len(s.faces)):
                f = s.faces[i]
                if f[0] != 'box': s.faces[i] = tuple(f[:3]) + (f[3] if len(f) > 3 else True, np.array([0.30, 0.29, 0.36]))
    if fl: floor(s)
    return s


VIEWS = [((0, 6), 'front', 'the great wheel face-on; the one within it at right angles'),
         ((-34, 16), 'three-quarter', 'wheel within wheel within wheel, full of eyes'),
         ((-20, -62), 'from below', 'what a player under it sees')]


def view_tile(view, name, sub, dark=None, size=760):
    below = view[1] < 0
    s = scene(dark, others=not below, fl=not below)
    span = 2 * BALL + 1.2 if below else 2 * BALL + 4.4
    cx = 0.0 if below else 1.9
    cyy = CY if below else CY - 0.25
    im = cull(s, view, size=size, span=span, center=(cx * math.cos(math.radians(view[0])), cyy, -cx * math.sin(math.radians(view[0])) * 0))
    im = dark_bg(im) if not dark else dark_bg(im, (12, 10, 22), (3, 3, 7))
    if dark: im = bloom(im)
    return label(im, name, sub)


if 'form' in what:
    sheet([view_tile(v, n, sub) for v, n, sub in VIEWS], OUT + '/ophan.png', cols=3,
          title='The Ophanim - the Lightbringer\'s wheel within a wheel  (SCALE %.1f: %.1f blocks across the flames; beside her and a player)' % (A.SCALE, 2 * BALL))
if 'dark' in what:
    T = []
    for dk, txt in (('emit', 'light_emission only'), ('glow', 'GLOW: brightness 15 on its parts')):
        for v, n, sub in VIEWS[:2]:
            T.append(view_tile(v, f'{n} - night', txt, dark=dk, size=560))
    sheet(T, OUT + '/ophan_dark.png', cols=2, title='The Ophanim at night - eyes, fire and the core lit (a bloom drawn over the glow)')
if 'spin' in what:
    T = []
    for k in range(4):
        th = k * 22.5
        pose = {'ring_a': qs(('y', 28 + th)), 'ring_b': qs(('x', 38 - th * 1.5)), 'ring_c': qs(('z', -35 + th * 2.3)), 'core': qs(('y', 20 + th * 0.3))}
        s = scene(others=False, fl=False, pose=pose)
        im = dark_bg(cull(s, (-30, 14), size=460, span=2 * BALL + 2.2, center=(0, CY - 0.3, 0)))
        T.append(label(im, f'frame {k + 1}', f'ring_a Y {28 + th:.0f}, ring_b X {38 - th * 1.5:.0f}, ring_c Z {-35 + th * 2.3:.0f}'))
    sheet(T, OUT + '/ophan_spin.png', cols=4, title='The Ophanim - the wheels turning, each on its own axis (a: Y, b: X, c: Z)')
if 'parts' in what:
    T = []
    for p in A.PARTS:
        s = K.multi_scene(ROOT)
        s.display(f'bm:item/{A.model_id(p)}', pos=(0, CY, 0), scale=A.SCALE, left=tuple(POSE[p]) if p != 'ring_a' else qs(('y', 0)))
        span = {'ring_a': 2 * BALL + 0.5, 'ring_b': 4.6, 'ring_c': 3.2, 'core': 2.2}[p]
        im = dark_bg(cull(s, (-25, 12) if p != 'ring_a' else (0, 0), size=420, span=span, center=(0, CY, 0)))
        T.append(label(im, p, f'spins about {A.SPIN_AXIS[p].upper()}'))
    sheet(T, OUT + '/ophan_parts.png', cols=4, title='The Ophanim - its parts')
