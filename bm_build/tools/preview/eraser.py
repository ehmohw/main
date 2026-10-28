"""The Eraser preview sheets (rigkit; the draft for approval).  python3 tools/preview/eraser.py [views,poses,faces,lineup,crumbs]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, eraser_art as A, capshun_art as CA, rigkit
from PIL import Image
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup', 'crumbs']
root = K.pack(A, OUT + '/rp_er')
DESC = {'idle_a': 'fidgeting', 'idle_b': 'a nervous glance back', 'idle_c': '"sorry!" - a little bow', 'walk_1': 'walk (a waddle)',
        'run_1': 'run (arms flapping)', 'sit_a': 'sit', 'sit_b': 'seated idle: swinging its feet', 'tired': 'fainted', 'swim_2': 'swim (sunk to the eyes)',
        'rub_0': 'RUB OUT: scrub to its right', 'rub_1': '...and to its left', 'wince': 'after: it winces', 'hop_up': 'BOUNCE: crouch',
        'hop': '...up', 'slam': '...and down flat', 'hide': 'hide: covers its face'}


def tile(pose, view=(-30, 14), span=1.9, center=(0, 0.48, -0.1), size=320, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = A.POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side'), ('back', 'back'), ((140, 20), '3/4 back (the worn end)'))],
            OUT + '/eraser_turnaround.png', cols=5, title='The Eraser - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, sub=DESC.get(n), center=(0, 0.6 if n in ('jump', 'hop') else 0.48, -0.2)) for n in A.DRAFT],
            OUT + '/eraser_poses.png', cols=5, title='The Eraser - poses')
    K.sheet([tile(A.POSES[n], 'side', label=n + ' (side)') for n in ('rub_0', 'wince', 'hop_up', 'slam', 'hide', 'sit_a', 'tired', 'idle_c')],
            OUT + '/eraser_poses_side.png', cols=4, title='The Eraser - poses from the side (clipping / ground check)')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f).items() if v is not None}
        tiles.append(tile(pose, 'front', span=0.82, center=(0, 0.42, 0), size=260, label=f or 'default (worried)'))
    K.sheet(tiles, OUT + '/eraser_faces.png', cols=7, title='The Eraser - faces')
if 'lineup' in what:
    rc = K.pack(CA, OUT + '/rp_mz')
    s = K.multi_scene(root, rc)
    rigkit.render(s, A, A.POSES['idle_c'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    cp = {k: v for k, v in dict(CA.POSES['idle_a'], _face='surprised').items() if v is not None}
    rigkit.render(s, CA, cp, at=(1.3, 0, 0.3), scale=CA.RIG_SCALE)                   # (Mr. Capshun keeping his distance)
    K.person(s, (-1.2, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.4, center=(0, 1.1, 0)), 'size', 'a player, the Eraser (sorry!), Mr. Capshun (terrified)')],
            OUT + '/eraser_lineup.png', cols=1, title='The Eraser - next to Mr. Capshun')
if 'crumbs' in what:                                                          # (the crumb sprite, blown up, for the datapack's particle)
    im = A.textures()['er_crumb_bit']
    bg = Image.new('RGBA', (16, 16), (255, 255, 255, 255)); bg.alpha_composite(im)
    big = bg.resize((256, 256), Image.NEAREST).convert('RGB')
    K.sheet([K.label(big, 'er_crumb_bit', '16 px, transparent')], OUT + '/eraser_crumb_bit.png', cols=1)
print('ok', OUT)
