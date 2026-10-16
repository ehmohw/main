"""Dennis and Pistachio (2.80d) preview sheets: python3 tools/preview/npc280d.py [dennis|pistachio] [views,poses]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import importlib
import draftkit as K, rigkit
who = sys.argv[1] if len(sys.argv) > 1 else 'dennis'
what = sys.argv[2].split(',') if len(sys.argv) > 2 else ['views', 'poses']
F = importlib.import_module(f'{who}_art')
EXTRA = getattr(importlib.import_module('phase163'), 'POSES_' + who.upper(), {}) if 'follower' in what else {}
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
root = K.pack(F, f'{OUT}/rp_{who}')
POSES = dict(F.POSES, **EXTRA)


def tile(pose, view='iso', span=2.6, center=(0, 0.85, 0), size=340, label=''):
    s = K.multi_scene(root, K.REAL_RP); rigkit.draw(s, F, rigkit.solve(F.PIVOT, F.PARENT, pose), pose, scale=F.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label)


if 'views' in what:
    I = POSES['idle_a']
    K.sheet([tile(I, v, label=l) for v, l in (('front', 'front'), ('side', 'side'), ('back', 'back'), ((-35, 18), '3/4'))],
            f'{OUT}/{who}_turnaround.png', cols=4, title=f'{who} - turnaround')
if 'poses' in what or 'follower' in what:
    names = sorted(POSES) if 'follower' in what else F.DRAFT
    K.sheet([tile(POSES[n], (-30, 15), label=n) for n in names], f'{OUT}/{who}_poses.png', cols=5, title=f'{who} - poses')
print(OUT)
