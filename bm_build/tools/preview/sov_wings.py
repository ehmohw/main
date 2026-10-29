"""v299: the Dread Sovereign's spoils - the Wings of the Last Night and of the First Light (sov_wings.py) - previews.
    python3 tools/preview/sov_wings.py [states,lineup,icons]
  states   both, as worn (a plain player, the elytra's mantle, the 3D wings): rest (both breaths), sneak, ride, fall, glide
  lineup   beside the Wings of the Damned (hollow_wings, the elytra mesh alone) and the Seraph's - at rest, falling, gliding
  icons    the sprites and the 3D inventory model beside hollow_wings' sprite
PNGs to $SOV_OUT (default /home/user/main/previews/v299_seraph, sov_wings_*.png). The ds_ / dvn_ textures come from the built
pack (out_p2: the Sovereign's and the Divine One's)."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
_argv = sys.argv; sys.argv = ['dread.py', 'none']
import dread as DP                                        # (its full pack holds every set - seraph_wings.rp registers these)
sys.argv = _argv
SP = DP.SP
import numpy as np
from PIL import Image
import playerkit as PK
import sov_wings as V
import seraph_wings as W

OUT = os.environ.get('SOV_OUT', '/home/user/main/previews/v299_seraph'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['states', 'lineup', 'icons']
NEW = DP.NEW
ART = {'night': V.NIGHT, 'light': V.LIGHT}
NAME = {'night': 'the Last Night', 'light': 'the First Light'}


def wearer(s, kind, which, w3=None, pitch=0.0, elytra=True):
    lift = SP.LIFT[kind]
    wl = {'night': 'bm:entity/equipment/wings/sov_wings', 'light': 'bm:entity/equipment/wings/sov_wings_holy',
          'hollow': 'bm:entity/equipment/wings/damned_wings', 'seraph': 'bm:entity/equipment/wings/seraph_wings'}[which]
    PK.put(s, PK.player(kind, SP.LAYERS if which == 'seraph' else (), wings=wl if elytra else None), at=(0, lift, 0), pitch=pitch)
    if which == 'seraph':
        c = PK._rx(math.radians(pitch)) @ np.array((0, SP.HEAD_Y[kind] * PK.S / 16, 0)) + np.array((0, lift, 0))
        s.display('bm:item/seraph_helm', pos=tuple(c), pitch=pitch, scale=0.625 * PK.S, ctx='head')
    if w3:
        W.render(s, w3, pitch=0.0, art=ART.get(which) if which in ART else None)


def tile(which, view, text, sub=None, kind='stand', w3=None, pitch=0.0, span=3.6, cy=1.2, size=380):
    s = SP.scene(NEW); SP.floor(s, r=3.0)
    wearer(s, kind, which, w3, pitch)
    return SP.label(SP.dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


if 'states' in what:
    for which in ('night', 'light'):
        n = NAME[which]
        T = [tile(which, 'back', f'{n}: at rest', 'three pairs folded, the halo (breath a)', w3='rest_a'),
             tile(which, 'back', f'{n}: at rest', 'the breath (b): eased out, the halo turned, swollen', w3='rest_b'),
             tile(which, (35, 12), f'{n}: at rest', 'three-quarter', w3='rest_a'),
             tile(which, 'front', f'{n}: at rest', 'front', w3='rest_a'),
             tile(which, 'back', f'{n}: sneaking', 'a mantle', kind='crouch', w3='sneak'),
             tile(which, 'back', f'{n}: riding', None, w3='ride'),
             tile(which, (150, 10), f'{n}: falling (a)', 'raised', w3='fall_a', span=5.6, cy=1.5),
             tile(which, (150, 10), f'{n}: falling (b)', 'the downbeat', w3='fall_b', span=5.6, cy=1.5),
             tile(which, (180, 55), f'{n}: gliding (a)', 'from behind and above', kind='glide', pitch=90, w3='glide_a', span=6.8, cy=0.3),
             tile(which, (180, 55), f'{n}: gliding (b)', None, kind='glide', pitch=90, w3='glide_b', span=6.8, cy=0.3),
             tile(which, (215, 30), f'{n}: gliding', 'from the front, above', kind='glide', pitch=90, w3='glide_a', span=6.8, cy=0.3),
             tile(which, (100, 8), f'{n}: gliding', 'from the side', kind='glide', pitch=90, w3='glide_a', span=6.8, cy=0.3)]
        SP.sheet(T, f'{OUT}/sov_wings_{which}.png', cols=4, title=f'The Wings of {n.split(" ", 1)[1]} - the Dread Sovereign\'s spoils')

if 'lineup' in what:
    T = []
    for st, kind, view, span, cy, pitch, lab in (('rest_a', 'stand', 'back', 3.6, 1.2, 0, 'at rest'), ('fall_a', 'stand', (150, 10), 5.6, 1.5, 0, 'falling'),
                                                 ('glide_a', 'glide', (180, 55), 6.8, 0.3, 90, 'gliding')):
        T.append(tile('hollow', view, 'Wings of the Damned (before)', lab, kind=kind, pitch=pitch, span=span, cy=cy))
        T.append(tile('seraph', view, "the Seraph's Wings", lab, kind=kind, w3=st, pitch=pitch, span=span, cy=cy))
        T.append(tile('night', view, 'the Last Night', lab, kind=kind, w3=st, pitch=pitch, span=span, cy=cy))
        T.append(tile('light', view, 'the First Light', lab, kind=kind, w3=st, pitch=pitch, span=span, cy=cy))
    SP.sheet(T, f'{OUT}/sov_wings_lineup.png', cols=4, title='Wings, side by side - the Damned, the Seraph, the Last Night, the First Light')

if 'icons' in what:
    import vanilla
    T = [SP.flat(Image.open(f'{BM}/out_p2/BlackMarket_RP/assets/bm/textures/item/hollow_wings.png').convert('RGBA'), 'hollow_wings', 'the Wings of the Damned (before)', k=12)]
    for which, iid in V.ITEMS.items():
        T.append(SP.flat(vanilla.process(f'{iid}_sprite', V.icons()[iid]), iid, 'the sprite (in the hand, on the ground)', k=12))
        s = SP.scene(NEW); s.display(f'bm:item/{iid}_3d', pos=(0, 0, 0), ctx='gui')
        T.append(SP.label(SP.dark(s.render('front', size=T[0].width, span=1.15, center=(0, 0.0, 0))).resize(T[0].size), iid, 'the 3D inventory model (gui)'))
    SP.sheet(T, f'{OUT}/sov_wings_icons.png', cols=5, title="The Sovereign's wings - their icons")
