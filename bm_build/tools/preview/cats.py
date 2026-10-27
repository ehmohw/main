"""Nia and Henry preview sheets (rigkit).  python3 tools/preview/cats.py [views,poses,faces,lineup]
Writes preview/nia_henry_*.png (BM_PREVIEW_DIR for the scratch packs)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import draftkit as K, nia_art as NI, henry_art as HY, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
DST = os.path.join(BM, 'preview')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'faces', 'lineup']
CATS = (('nia', 'Nia', NI), ('henry', 'Henry', HY))
ROOT = {k: K.pack(A, f'{OUT}/rp_{k}') for k, _n, A in CATS}


def tile(k, A, pose, view=(-35, 15), span=1.6, center=(0, 0.45, -0.1), size=340, label='', sub=None):
    s = K.multi_scene(ROOT[k]); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


for k, nm, A in CATS:
    I = A.POSES['idle_a']
    if 'views' in what:
        K.sheet([tile(k, A, I, v, label=l) for v, l in (((-35, 15), 'front 3/4'), ('front', 'front'), ('side', 'side'), ('back', 'back'))],
                f'{DST}/nia_henry_{k}_views.png', cols=4, title=f'{nm} - turnaround')
    if 'poses' in what:
        K.sheet([tile(k, A, A.POSES[n], label=n) for n in A.DRAFT], f'{DST}/nia_henry_{k}_poses.png', cols=6, title=f'{nm} - poses')
    if 'faces' in what:
        tiles = []
        for f in (None,) + A.FACES:
            pose = {kk: v for kk, v in dict(I, _face=f).items() if v is not None}
            tiles.append(tile(k, A, pose, 'front', span=0.55, center=(0, 0.72, 0), size=260, label=f or 'default'))
        K.sheet(tiles, f'{DST}/nia_henry_{k}_faces.png', cols=4, title=f'{nm} - faces')
if 'lineup' in what:
    s = K.multi_scene(ROOT['nia'], ROOT['henry'])
    rigkit.render(s, NI, NI.POSES['idle_a'], at=(0.2, 0, 0), scale=NI.RIG_SCALE, yaw=-90)
    rigkit.render(s, HY, HY.POSES['sit_a'], at=(1.3, 0, 0), scale=HY.RIG_SCALE, yaw=-25)
    s.solid((-0.9, 0, 0.5), (-0.3, 0.7, 0.55), '#b0b0b0')                        # (a vanilla cat's box: 0.6 wide, 0.7 tall)
    K.person(s, (-1.7, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=620, span=3.6, center=(-0.1, 0.9, 0)), 'size', 'a player, the vanilla cat box (grey, 0.6 x 0.7), Nia, Henry (sitting)')],
            f'{DST}/nia_henry_lineup.png', cols=1, title='Nia and Henry - to scale')
