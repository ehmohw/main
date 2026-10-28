"""The Cursor preview sheets (rigkit).  python3 tools/preview/cursor.py [views,poses,faces,forms,lineup]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from PIL import Image
import draftkit as K, cursor_art as A, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'forms', 'lineup']
root = K.pack(A, OUT + '/rp_cu')


def tile(pose, view=(-30, 12), span=2.3, center=(0, 1.0, 0), size=340, label='', sub=None, floor=True):
    s = K.multi_scene(root)
    if floor:                                                                  # (a thin floor slab: to see it hover, or rest on it)
        s.solid((-0.7, -0.04, -0.7), (0.7, 0.0, 0.7), '#d8d2c4')
    rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


class _PxEmma:
    """8-Bit Emma, as the shipped pack draws her (phase213 / pxart): one two-sided quad, her standing frame"""
    PARTS = ('head',); PARENT = {'head': None}; PREFIX = 'pxe_'

    def __init__(self):
        rot = Image.open(os.path.join(K.BM, 'ref', 'pixellab', 'twins', 'emma', 'Idle', 'rotations', 'south.png')).convert('RGBA')
        bb = rot.getbbox(); n = Image.open(os.path.join(K.REAL, 'assets', 'bm', 'textures', 'block', 'pxe_idle_0.png')).width
        self.RIG_SCALE = n / ((bb[3] - bb[1]) / 1.6)
        self.PIVOT = {'head': (0.0, 8.0 - 96.0 / n, 0.0)}

    def model_name(self, p, pose, suffix=''):
        return 'pxe_idle_0'


if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (2 px deep)'), ('back', 'back'))],
            OUT + '/cursor_turnaround.png', cols=4, title='The Cursor - turnaround (hovering)')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n) for n in A.DRAFT], OUT + '/cursor_poses.png', cols=6, title='The Cursor - poses')
    K.sheet([tile(A.POSES[n], (-70, 10), label=n, sub='side-ish') for n in ('click_up', 'click', 'select', 'sit_a', 'sit_b', 'tired')],
            OUT + '/cursor_poses_side.png', cols=6, title='The Cursor - poses, from the side')
    K.sheet([tile(A.POSES[f'{n}_{k}'], label=f'{n}_{k}') for n, c in (('walk', 4), ('run', 4), ('swim', 8)) for k in range(c)],
            OUT + '/cursor_cycles.png', cols=8, title='The Cursor - walk, run, swim')
    # (close up, straight on: the tail's root stays inside the arrow however it wags)
    K.sheet([tile(A.POSES[n], 'front', span=1.4, center=(0, 1.0, 0), size=300, label=n, sub='front, close') for n in ('idle_b', 'drag_1', 'hurt', 'happy', 'sit_b', 'swim_2', 'swim_6')],
            OUT + '/cursor_tail.png', cols=7, title='The Cursor - the tail joint, close up')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f, body=None).items() if v is not None}
        tiles.append(tile(pose, 'front', span=1.0, center=(0, 1.15, 0), size=260, label=f or 'default', floor=False))
    K.sheet(tiles, OUT + '/cursor_faces.png', cols=7, title='The Cursor - faces')
if 'forms' in what:
    tiles = []
    for form in A.FORMS:
        for f in (None, 'happy', 'surprised', 'hurt'):
            pose = {'_shape': form, '_face': f} if f else {'_shape': form}
            tiles.append(tile(pose, 'front', span=1.1, center=(0, 1.1, 0), size=220, label=form, sub=f or 'default', floor=False))
    K.sheet(tiles, OUT + '/cursor_forms.png', cols=8, title='The Cursor - forms (_shape) x faces')
if 'lineup' in what:
    s = K.multi_scene(root, K.REAL_RP)
    s.solid((-2.2, -0.04, -0.8), (2.2, 0.0, 1.0), '#d8d2c4')
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    PE = _PxEmma()
    rigkit.render(s, PE, {}, at=(1.2, 0, 0.2), scale=PE.RIG_SCALE)
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.1, 0)), 'size', 'a player, the Cursor (hovering), 8-Bit Emma')], OUT + '/cursor_lineup.png',
            cols=1, title='The Cursor - next to 8-Bit Emma')
