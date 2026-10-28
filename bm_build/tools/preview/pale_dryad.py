"""The Pale Dryad's preview sheets (rigkit).  python3 tools/preview/pale_dryad.py [views,poses,faces,night,lineup]
Writes $BM_PREVIEW_DIR/pale_dryad_*.png. The night tile: tools/render has no light, so each face is tinted after the scene is
built - unlit faces dimmed to moonlight, faces of elements with light_emission kept bright in proportion to their level."""
import sys, os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import draftkit as K, pale_dryad_art as A, henry_art as HY, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'night', 'lineup']
ROOT = K.pack(A, f'{OUT}/rp_pd')


def tile(pose, view=(-35, 15), span=1.45, center=(0, 0.6, 0), size=360, label='', sub=None):
    s = K.multi_scene(ROOT); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


def night_scene():
    """a Scene whose display() tints every face by its element's light_emission (moonlit when 0)"""
    s = K.multi_scene(ROOT); base = s.display

    def display(mid, **kw):
        n0 = len(s.faces); base(mid, **kw)
        lights = [e.get('light_emission', 0) for e in s.model(mid).get('elements', []) for _ in e.get('faces', {})]
        for i, L in enumerate(lights):
            f = s.faces[n0 + i]
            k = 0.16 + 0.84 * (L / 15) ** 0.7 if L else None
            tint = np.array([0.17, 0.19, 0.30]) if not L else np.array([k, k, min(1.0, k * 1.05)])
            s.faces[n0 + i] = (f[0], f[1], f[2], False if L else f[3], tint)
    s.display = display
    return s


def night(im):
    a = np.asarray(im).astype(np.float32)
    sky = (np.abs(a - np.array([199, 219, 242])).sum(axis=2) < 8)
    grid = (np.abs(a - np.array([140, 158, 140])).sum(axis=2) < 10) | (np.abs(a - np.array([51, 127, 51])).sum(axis=2) < 10)
    a[sky] = [14, 18, 34]; a[grid] = [34, 40, 46]
    from PIL import Image
    return Image.fromarray(a.astype(np.uint8))


I = A.POSES['idle_a']
if 'views' in what:
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 15), 'front 3/4'), ('side', 'side'), ('back', 'back'),
                                              ((145, 15), 'back 3/4'), ((-30, 50), 'from above'))],
            f'{OUT}/pale_dryad_views.png', cols=3, title='The Pale Dryad - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], (-60, 22) if n.startswith('swim') else (-35, 15), center=(0, 0.3, 0) if n.startswith('swim') else (0, 0.62, 0),
                  label=n, sub='(mushrooms flaring)' if A.POSES[n].get('_glow') else ('(low in the water)' if n.startswith('swim') else None)) for n in A.DRAFT],
            f'{OUT}/pale_dryad_poses.png', cols=6, title='The Pale Dryad - poses')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
        tiles.append(tile(dict(pose, head=rigkit.I), 'front', span=0.48, center=(0, 0.8, 0), size=240, label=f or 'default'))
    K.sheet(tiles, f'{OUT}/pale_dryad_faces.png', cols=7, title='The Pale Dryad - faces')
if 'night' in what:
    tiles = []
    for pose, v, l in ((I, (-35, 15), 'night: at rest'), (I, (145, 15), 'night: from behind'), (A.POSES['heal'], (-35, 15), 'night: healing (_glow)')):
        s = night_scene(); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        im = night(s.render(v, size=320, span=1.6, center=(0, 0.62, 0)))
        from PIL import ImageDraw
        ImageDraw.Draw(im).text((8, 6), l, fill=(220, 225, 235))
        tiles.append(im)
    K.sheet(tiles, f'{OUT}/pale_dryad_night.png', cols=3, title='The Pale Dryad - her glow (light_emission, simulated)')
if 'lineup' in what:
    HROOT = K.pack(HY, f'{OUT}/rp_henry')
    s = K.multi_scene(ROOT, HROOT)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE, yaw=-15)
    rigkit.render(s, A, A.POSES['heal'], at=(1.7, 0, 0.3), scale=A.RIG_SCALE, yaw=-50)
    rigkit.render(s, HY, HY.POSES['sit_a'], at=(0.85, 0, -0.1), scale=HY.RIG_SCALE, yaw=-30)
    K.person(s, (-0.95, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=720, span=3.8, center=(0.35, 0.95, 0)), 'size', 'a player, the Pale Dryad (and again, healing), Henry')],
            f'{OUT}/pale_dryad_lineup.png', cols=1, title='The Pale Dryad - to scale')
