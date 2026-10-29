"""v299: the Wings of the Damned and their holy twin redrawn (sprites294: damned_wings_tex, holy_wings_tex, hollow_wings,
angel_hollow_wings) - previews.   python3 tools/preview/damned.py [before,lineup,icons]
  before   the old layers beside the new, on the elytra mesh: at rest from behind, gliding from above - both twins
  lineup   the Damned, the Holy Damned, the Seraph's, the Last Night, the First Light - at rest, falling, gliding
  icons    the old sprites beside the new
PNGs to $DAMNED_OUT (default /home/user/main/previews/v299_seraph, damned_*.png); the old look is the built pack's (out_p2)."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
import importlib.util
_argv = sys.argv; sys.argv = ['sov_wings.py', 'none']
_spec = importlib.util.spec_from_file_location('sov_preview', os.path.join(HERE, 'sov_wings.py'))   # (tools/preview's, not the art module)
SV = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(SV)
sys.argv = _argv
SP, DP = SV.SP, SV.DP
from PIL import Image
import playerkit as PK
import sprites294
import vanilla
import seraph_wings as W

OUT = os.environ.get('DAMNED_OUT', '/home/user/main/previews/v299_seraph'); os.makedirs(OUT, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['before', 'lineup', 'icons']
OLD = f'{BM}/out_p2/BlackMarket_RP/assets/bm/textures'
NEW = SV.NEW
EQ = os.path.join(NEW, 'assets', 'bm', 'textures', 'entity', 'equipment', 'wings')
os.makedirs(EQ, exist_ok=True)
sprites294.damned_wings_tex().save(os.path.join(EQ, 'damned_wings.png')); sprites294.holy_wings_tex().save(os.path.join(EQ, 'angelic_wings.png'))
OLDR = os.path.join(SP.TMP, 'rp_damned_old'); os.makedirs(os.path.join(OLDR, 'assets', 'bm', 'textures', 'entity', 'equipment', 'wings'), exist_ok=True)
for n in ('damned_wings', 'angelic_wings'):
    Image.open(f'{OLD}/entity/equipment/wings/{n}.png').save(os.path.join(OLDR, 'assets', 'bm', 'textures', 'entity', 'equipment', 'wings', f'{n}.png'))


def tile(root, tex, view, text, sub=None, kind='stand', pitch=0.0, span=3.6, cy=1.2, w3=None, art=None, helm=None, layers=(), size=360):
    s = SP.scene(root); SP.floor(s, r=3.0)
    lift = SP.LIFT[kind]
    PK.put(s, PK.player(kind, layers, wings=f'bm:entity/equipment/wings/{tex}'), at=(0, lift, 0), pitch=pitch)
    if helm:
        c = PK._rx(math.radians(pitch)) @ __import__('numpy').array((0, SP.HEAD_Y[kind] * PK.S / 16, 0)) + __import__('numpy').array((0, lift, 0))
        s.display(helm, pos=tuple(c), pitch=pitch, scale=0.625 * PK.S, ctx='head')
    if w3: W.render(s, w3, art=art)
    return SP.label(SP.dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


if 'before' in what:
    T = []
    for tex, name in (('damned_wings', 'the Wings of the Damned'), ('angelic_wings', 'their holy twin')):
        for view, sub, kind, pitch, span, cy in (('back', 'at rest, behind', 'stand', 0, 2.6, 1.1), ((150, 12), 'at rest', 'stand', 0, 2.6, 1.1),
                                                 ((180, 55), 'gliding, from above', 'glide', 90, 3.4, 0.3)):
            T.append(tile(OLDR, tex, view, f'BEFORE: {name}', sub, kind, pitch, span, cy))
            T.append(tile(NEW, tex, view, f'AFTER: {name}', sub, kind, pitch, span, cy))
    SP.sheet(T, f'{OUT}/damned_before_after.png', cols=4, title='The Wings of the Damned and their holy twin - before and after')
    L = [SP.flat(sprites294.damned_wings_tex(), 'damned_wings (2.99)', 'tattered black-violet feathers, soul fire', k=8),
         SP.flat(sprites294.holy_wings_tex(), 'angelic_wings (2.99)', 'pearl and gold feathers, a light edge', k=8)]
    sh = Image.new('RGB', (L[0].width * 2, L[0].height), (14, 12, 22))
    for i, t in enumerate(L): sh.paste(t, (i * L[0].width, 0))
    sh.save(f'{OUT}/damned_layers.png'); print(f'{OUT}/damned_layers.png')

if 'lineup' in what:
    T = []
    for st, kind, view, span, cy, pitch, lab in (('rest_a', 'stand', 'back', 3.6, 1.2, 0, 'at rest'), ('fall_a', 'stand', (150, 10), 5.6, 1.5, 0, 'falling'),
                                                 ('glide_a', 'glide', (180, 55), 6.8, 0.3, 90, 'gliding')):
        T.append(tile(NEW, 'damned_wings', view, 'the Wings of the Damned', lab, kind, pitch, span, cy))
        T.append(tile(NEW, 'angelic_wings', view, '... made holy', lab, kind, pitch, span, cy))
        T.append(tile(NEW, 'seraph_wings', view, "the Seraph's Wings", lab, kind, pitch, span, cy, w3=st, helm='bm:item/seraph_helm', layers=SP.LAYERS))
        T.append(tile(NEW, 'sov_wings', view, 'the Last Night', lab, kind, pitch, span, cy, w3=st, art=SV.ART['night']))
        T.append(tile(NEW, 'sov_wings_holy', view, 'the First Light', lab, kind, pitch, span, cy, w3=st, art=SV.ART['light']))
    SP.sheet(T, f'{OUT}/damned_lineup.png', cols=5, title='Wings, in their order - the Damned, made holy, the Seraph, the Last Night, the First Light')

if 'icons' in what:
    T = []
    for iid, fn in (('hollow_wings', sprites294.hollow_wings), ('angel_hollow_wings', sprites294.angel_hollow_wings)):
        T.append(SP.flat(Image.open(f'{OLD}/item/{iid}.png').convert('RGBA'), 'before', iid, k=12))
        T.append(SP.flat(vanilla.process(iid, fn()) if iid == 'hollow_wings' else fn(), 'after', iid, k=12))   # (phase182 saves the holy one as drawn)
    SP.sheet(T, f'{OUT}/damned_icons.png', cols=4, title='The Wings of the Damned - their icons')
