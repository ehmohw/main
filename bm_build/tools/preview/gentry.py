"""The Gutter Gentry as followers - rig preview sheets (rigkit).  python3 tools/preview/gentry.py [who,...] [views,poses,faces,lineup]
who: batty, eggbert, count (default all). Writes preview/gentry_<who>_*.png and preview/gentry_lineup.png."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import draftkit as K, rigkit
import batty_art, eggbert_art, count_art
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
DST = os.path.join(BM, 'preview')
ALL = {'batty': (batty_art, 'Batty'), 'eggbert': (eggbert_art, 'Eggbert'), 'count': (count_art, 'The Count')}
who = [w for w in (sys.argv[1].split(',') if len(sys.argv) > 1 else ALL) if w in ALL] or list(ALL)
what = sys.argv[2].split(',') if len(sys.argv) > 2 else ['views', 'poses', 'faces', 'lineup']
ROOTS = {}


def root(w):
    if w not in ROOTS: ROOTS[w] = K.pack(ALL[w][0], f'{OUT}/rp_gentry_{w}')
    return ROOTS[w]


def tile(w, pose, view=(-35, 15), suffix='', size=300, label='', sub=None, span=None, center=None):
    A = ALL[w][0]
    h = 34 * A.RIG_SCALE / 16
    s = K.multi_scene(root(w)); rigkit.render(s, A, pose, scale=A.RIG_SCALE, suffix=suffix)
    return K.label(s.render(view, size=size, span=span or h * 1.35, center=center or (0, h * 0.5, 0)), label, sub)


for w in who:
    A, nm = ALL[w]
    I = A.POSES['idle_a']
    if 'views' in what:
        tl = []
        for sfx, look in (('', 'Gentry'), ('_c', 'chibi')):
            tl += [tile(w, I, v, sfx, label=f'{look}: {l}') for v, l in (((-35, 15), 'front 3/4'), ('front', 'front'), ('side', 'side'), ('back', 'back'))]
        K.sheet(tl, f'{DST}/gentry_{w}_views.png', cols=4, title=f'{nm} - turnaround (the Gentry look; the chibi costume)')
    if 'poses' in what:
        for sfx, look in (('', 'gentry'), ('_c', 'chibi')):
            K.sheet([tile(w, A.POSES[n], suffix=sfx, label=n) for n in A.DRAFT], f'{DST}/gentry_{w}_poses_{look}.png', cols=5,
                    title=f'{nm} - poses ({look})')
    if 'faces' in what:
        tl = []
        for sfx, look in (('', 'Gentry'), ('_c', 'chibi')):
            for f in (None,) + A.FACES:
                pose = {k: v for k, v in dict(I, _face=f).items() if v is not None}
                tl.append(tile(w, pose, 'front', sfx, size=220, label=f'{look}: {f or "default"}', span=A.FACE_SPAN, center=A.FACE_AT))
        K.sheet(tl, f'{DST}/gentry_{w}_faces.png', cols=len(A.FACES) + 1, title=f'{nm} - faces')
if 'lineup' in what:
    import kettle_art as KT, rufus_art as RF
    rk, rr = K.pack(KT, f'{OUT}/rp_kt'), K.pack(RF, f'{OUT}/rp_rufus')
    for sfx, look in (('', 'gentry'), ('_c', 'chibi')):
        s = K.multi_scene(*[root(w) for w in ALL], rk, rr)
        K.person(s, (-1.2, 0, 0.3))
        rigkit.render(s, KT, KT.POSES['idle_a'], at=(0.0, 0, 0), scale=KT.RIG_SCALE)
        rigkit.render(s, RF, RF.POSES['idle_a'], at=(0.9, 0, 0), scale=RF.RIG_SCALE, yaw=-15)
        for i, w in enumerate(ALL):
            A = ALL[w][0]; rigkit.render(s, A, A.POSES['idle_a'], at=(1.9 + 1.2 * i, 0, 0), scale=A.RIG_SCALE, suffix=sfx, yaw=-10)
        K.sheet([K.label(s.render((-10, 8), size=900, span=6.4, center=(2.1, 0.75, 0)), 'size', 'a player, Kettle, Rufus, Batty, Eggbert, The Count')],
                f'{DST}/gentry_lineup_{look}.png', cols=1, title=f'The Gutter Gentry as followers - to scale ({look})')
