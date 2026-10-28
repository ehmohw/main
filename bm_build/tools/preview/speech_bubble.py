"""The Speech Bubble preview sheets (rigkit).  python3 tools/preview/speech_bubble.py [views,poses,faces,shapes,words,lineup]"""
import sys, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K, speech_bubble_art as A, capshun_art as CA, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'shapes', 'words', 'lineup']
root = K.pack(A, OUT + '/rp_sbb')


def shot(s, view, **kw):
    """render with the game's back-face culling (tools/render draws both sides of a face; the game doesn't) - its words have a
    back plane that reads right way round from behind, which would otherwise show through the front's clear parts here"""
    V = view if isinstance(view, tuple) else {'front': (0, 0), 'back': (180, 0), 'side': (90, 0), 'iso': (35, 25), 'top': (0, 89)}[view]
    yw, pt = math.radians(V[0]), math.radians(V[1])
    fwd = np.array([-math.sin(yw) * math.cos(pt), -math.sin(pt), -math.cos(yw) * math.cos(pt)])
    keep = []
    for f in s.faces:
        if f[0] != 'box' and len(f[0]) == 4 and isinstance(f[2], str) and not f[2].startswith('#'):
            q = np.array(f[0]); n = np.cross(q[1] - q[0], q[3] - q[0])
            if n @ fwd < -1e-9: continue
        keep.append(f)
    s.faces = keep
    return s.render(view, **kw)


def tile(pose, view=(-30, 12), span=2.6, center=(0, 0.95, 0), size=340, label='', sub=None):
    s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(shot(s, view, size=size, span=span, center=center), label, sub)


if 'views' in what:
    I = dict(A.POSES['idle_a'])
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ((-35, 18), '3/4'), ('side', 'side (flat!)'), ('back', 'back'))],
            OUT + '/speech_bubble_turnaround.png', cols=4, title='The Speech Bubble - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, sub=' '.join(f'{k[1:]}={A.POSES[n][k]}' for k in ('_shape', '_word') if k in A.POSES[n])) for n in A.DRAFT],
            OUT + '/speech_bubble_poses.png', cols=6, title='The Speech Bubble - poses')
    # (the word poses seen side-on and from above: the word clear of the bubble)
    W = [n for n in A.DRAFT if A.POSES[n].get('_word')]
    K.sheet([tile(A.POSES[n], v, label=f'{n} ({l})') for n in W for v, l in (('side', 'side'), ((-60, 50), 'above'))],
            OUT + '/speech_bubble_wordcheck.png', cols=6, title='The Speech Bubble - its words, from the side and above')
if 'faces' in what:
    tiles = []
    for f in (None,) + A.FACES:
        pose = {k: v for k, v in dict(A.POSES['idle_a'], _face=f, body=None).items() if v is not None}
        pose = A._ground(pose)
        s = K.multi_scene(root); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
        tiles.append(K.label(shot(s, 'front', size=260, span=1.2, center=(0, 0.78, 0)), f or 'default'))
    K.sheet(tiles, OUT + '/speech_bubble_faces.png', cols=6, title='The Speech Bubble - faces')
if 'shapes' in what:
    tiles = []
    for sh in A.SHAPES:
        pose = A._ground({'_shape': sh})
        tiles.append(tile(pose, 'front', span=1.6, center=(0, 0.75, 0), size=300, label=sh))
    pose = A._ground({'_tail': 'none'})
    tiles.append(tile(pose, 'front', span=1.6, center=(0, 0.75, 0), size=300, label='_tail none (sat on it)'))
    K.sheet(tiles, OUT + '/speech_bubble_shapes.png', cols=5, title='The Speech Bubble - _shape')
if 'words' in what:
    tiles = []
    for w in A.WORDS:
        pose = A._ground({'_word': w, '_o_word': (0, -6.0, -2.0)})
        tiles.append(tile(pose, 'front', span=1.9, center=(0, 0.95, 0), size=280, label=w))
    K.sheet(tiles, OUT + '/speech_bubble_words.png', cols=4, title='The Speech Bubble - _word')
if 'lineup' in what:
    rc = K.pack(CA, OUT + '/rp_mz')
    s = K.multi_scene(root, rc, K.REAL_RP)
    rigkit.render(s, A, A.POSES['idle_a'], at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, CA, CA.POSES['idle_a'], at=(1.3, 0, 0.2), scale=CA.RIG_SCALE)
    K.person(s, (-1.3, 0, 0.3))
    K.sheet([K.label(shot(s, (-12, 8), size=620, span=3.4, center=(0, 1.0, 0)), 'size', 'a player, the Speech Bubble, Mr. Capshun')],
            OUT + '/speech_bubble_lineup.png', cols=1, title='The Speech Bubble - next to Mr. Capshun')
