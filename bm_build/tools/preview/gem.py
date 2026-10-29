"""The Gem of Creativity follower's preview sheets (rigkit).  python3 tools/preview/gem.py [views,poses,swirl,lineup,orbit]
Writes preview/gem_follower_*.png (BM_PREVIEW_DIR for the scratch packs). The swirl is an animated strip in the game; a scratch
pack holds one frame of it at a time (FRAME), so a sheet can show the colours turning."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import draftkit as K, gem_art as A, kettle_art as KA, capshun_art as CA, rigkit
OUT = K.OUT; os.makedirs(OUT, exist_ok=True)
DST = os.path.join(BM, 'preview')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['views', 'poses', 'swirl', 'lineup']


def pack(frame, root):
    """the art packed, each animated strip cut to one frame"""
    K.pack(A, root)
    for k in A.ANIMATED:
        im = A.textures()[k] if not hasattr(pack, 'T') else pack.T[k]
        im.crop((0, frame * A.N, A.N, (frame + 1) * A.N)).save(f'{root}/assets/bm/textures/block/{k}.png')
    return root


pack.T = A.textures()
ROOTS = {}


def root(frame=0):
    if frame not in ROOTS: ROOTS[frame] = pack(frame, f'{OUT}/rp_gem_f{frame}')
    return ROOTS[frame]


def tile(pose, view=(-30, 12), span=1.6, center=(0, 0.8, 0), size=320, label='', sub=None, frame=0):
    s = K.multi_scene(root(frame)); rigkit.render(s, A, pose, scale=A.RIG_SCALE)
    return K.label(s.render(view, size=size, span=span, center=center), label, sub)


I = A.POSES['idle_a']
if 'views' in what:
    K.sheet([tile(I, v, label=l) for v, l in (((-30, 12), 'front 3/4'), ('front', 'front (the crown, the table)'), ('side', 'side (the cut)'),
                                              ('back', 'back (the pavilion)'), ((145, 15), 'back 3/4'), ((-30, 45), 'from above (the halo)'))],
            f'{DST}/gem_follower_views.png', cols=3, title='The Gem of Creativity - turnaround')
if 'poses' in what:
    K.sheet([tile(A.POSES[n], label=n, frame=(i * 5) % A.FRAMES) for i, n in enumerate(A.DRAFT)], f'{DST}/gem_follower_poses.png', cols=5,
            title='The Gem of Creativity - poses')
if 'swirl' in what:
    K.sheet([tile(I, 'front', span=1.0, center=(0, 0.95, 0), size=240, label=f'frame {f}', frame=f) for f in range(0, A.FRAMES, 4)],
            f'{DST}/gem_follower_swirl.png', cols=8, title='The swirl, turning (every 4th of 32 frames)')
if 'lineup' in what:
    s = K.multi_scene(root(0), K.pack(KA, f'{OUT}/rp_kt'), K.pack(CA, f'{OUT}/rp_mz'))
    rigkit.render(s, A, I, at=(0.0, 0, 0), scale=A.RIG_SCALE)
    rigkit.render(s, KA, KA.POSES['idle_a'], at=(1.0, 0, 0.2), scale=KA.RIG_SCALE)
    rigkit.render(s, CA, CA.POSES['idle_a'], at=(2.0, 0, 0.3), scale=CA.RIG_SCALE)
    K.person(s, (-1.1, 0, 0.3))
    K.sheet([K.label(s.render((-12, 8), size=640, span=3.6, center=(0.4, 1.1, 0)), 'size', 'a player, the Gem (hovering), Kettle, Mr. Capshun')],
            f'{DST}/gem_follower_lineup.png', cols=1, title='The Gem of Creativity - to scale')
if 'orbit' in what:                                # (3.0a) the halo's glints circling it at rest: phase231 turns the ring by its right_rotation
    from rigkit import qs                          # (here: the same turn about the vertical, posed on the ring)
    ODIR = os.environ.get('BM_GEM_ORBIT_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300a_gem')); os.makedirs(ODIR, exist_ok=True)
    N = 24
    frames = []
    for k in range(N):
        deg = 360.0 * k / N
        pz = dict(I, halo=qs(('y', deg)))
        frames.append(tile(pz, (-30, 12), span=1.6, center=(0, 0.95, 0), size=300, label=f'{k * A.HALO_TURN // N} ticks', sub=f'halo turned {deg:.0f} deg',
                           frame=(k * 4) % A.FRAMES))
    K.sheet(frames[::2], f'{ODIR}/gem_idle_orbit.png', cols=6, title=f'The Gem at rest - its halo circling (a full turn in {A.HALO_TURN / 20:.0f} s; every 2nd step of {N})')
    for k in (0, 3, 6, 9):
        frames[k].save(f'{ODIR}/gem_idle_orbit_{k:02d}.png')
    frames[0].save(f'{ODIR}/gem_idle_orbit.gif', save_all=True, append_images=frames[1:], duration=A.HALO_TURN * 50 // N, loop=0)
    top = [tile(dict(I, halo=qs(('y', 360.0 * k / 8))), (-30, 60), span=1.8, center=(0, 0.95, 0), size=260, label=f'from above, {45 * k} deg') for k in range(4)]
    K.sheet(top, f'{ODIR}/gem_idle_orbit_above.png', cols=4, title='From above: the ring clear of the gem all the way round')
