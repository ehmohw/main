"""Emma's flower brooch and Leo's sea-kingdom insignia, close up (front, three-quarter, back) from a pack.
    python3 tools/preview/insignia.py [out.png] [rp root]   (default: out_p2's shipped resource pack)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import draftkit as K
import phase57_art as EM, phase96_art as LE
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(K.OUT, 'insignia.png')
rp = sys.argv[2] if len(sys.argv) > 2 else K.REAL_RP
tiles = []
for mod, pre, nm, parts in ((EM, 'em', 'Emma', ('body', 'head', 'armr', 'arml', 'legr', 'legl')), (LE, 'le', 'Leo', ('body', 'head', 'armr', 'arml', 'legr', 'legl'))):
    pose = mod.POSES['idle_a']
    for view, cam, yaw, sub in (('front', (0, 1.5, -6), 0, 'the chest, straight on'), ('3/4', (3.5, 1.6, -4.8), 0, 'from the side'),
                                ('back', (0, 1.5, -6), 180, 'turned round: the back')):
        s = K.multi_scene(rp)
        K.put_shipped(s, mod, pre, pose, parts=parts, yaw=yaw)
        tiles.append(K.label(s.render(cam, size=420, span=1.5 if view != 'back' else 2.2, center=(0, 1.35 if pre == 'em' else 1.55, 0)), f'{nm} - {view}', sub))
K.sheet(tiles, out, cols=3, title='Chest insignias')
print(out)
