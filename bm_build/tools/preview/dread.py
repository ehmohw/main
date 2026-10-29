"""v299: the Dreadborne redrawn (dread_art.py, dread_wings.py) - previews.   python3 tools/preview/dread.py [what,...]
  worn     the set on a player: front, back, three-quarter (the 3D wings at rest), the plate alone, the bare layers
  helm     the Dread Visage: front, three-quarter, side, behind, above - and a Dread zombie wearing it (the monsters share it)
  wings    the 3D wings: rest (both sway keys), sneak, ride, fall (both beats), glide (both beats)
  before   the old look beside the new (the worn set, the helm, gliding)
  icons    the sprites, big, beside the old ones
  both     the Seraph and the Dread side by side (at rest, falling, gliding)
The scratch pack is built through the real rp hooks (dread_set_art.rp, dread_armor.rp), so it holds both sets. PNGs to
$DREAD_OUT (default /home/user/main/previews/v299_seraph, dread_*.png); the old look from $DREAD_OLD."""
import sys, os, json, shutil, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
_argv = sys.argv; sys.argv = ['seraph.py', 'none']
import seraph as SP                                       # (its helpers: scene, floor, dark, label, sheet, flat)
sys.argv = _argv
import numpy as np
from PIL import Image
import playerkit as PK
import dread_art as A
import dread_wings as DW
import seraph_wings as W

OUT = os.environ.get('DREAD_OUT', '/home/user/main/previews/v299_seraph'); os.makedirs(OUT, exist_ok=True)
OLD = os.environ.get('DREAD_OLD', '')
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['worn', 'helm', 'wings', 'before', 'icons', 'both']


def full_pack(root):
    """both sets, as gen_rp writes them (the rp hooks, their POST, TEXTURE_MODS and HATS)"""
    if os.path.exists(root): shutil.rmtree(root)
    import dread_set_art, dread_armor
    class R:
        POST, ICONS, LANG, TEXTURE_MODS, HATS = [], {}, {}, [], {}
        DISPLAY_3D_EXTRA = ()
        @staticmethod
        def p(*a):
            f = os.path.join(root, *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f
        @staticmethod
        def wj(rel, obj): json.dump(obj, open(R.p(*rel.split('/')), 'w'))
    dread_set_art.rp(R); dread_armor.rp(R, '/home/claude/mc263/client/assets/minecraft/textures')
    for m in R.TEXTURE_MODS:
        for k, im in m.textures().items(): im.save(R.p('assets', 'bm', 'textures', 'block', k + '.png'))
    for name, (tex, els) in R.HATS.items():
        t = dict(tex); t['particle'] = list(tex.values())[0]
        R.wj(f'assets/bm/models/item/{name}.json', {'textures': t, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}})
    for f in R.POST: f(R)
    return root, R


NEW, RR = full_pack(os.path.join(SP.TMP, 'rp_dread_new'))
LAYERS = [('bm:entity/equipment/humanoid/dread', 'outer', ('body', 'armr', 'arml', 'legr', 'legl')),
          ('bm:entity/equipment/humanoid_leggings/dread', 'inner', ('body', 'legr', 'legl'))]
S_LAYERS = SP.LAYERS


def wearer(s, kind='stand', yaw=0.0, pitch=0.0, at=(0.0, 0.0, 0.0), helm=True, wings3d=None, elytra=True, layers=True, skin='minecraft:entity/player/wide/steve',
           set_='dread', old=False):
    lift = SP.LIFT[kind]
    lay, wl, hm, art = ((LAYERS, 'bm:entity/equipment/wings/dread_wings', 'bm:item/dread_helm', DW) if set_ == 'dread' else
                        (S_LAYERS, 'bm:entity/equipment/wings/seraph_wings', 'bm:item/seraph_helm', W))
    PK.put(s, PK.player(kind, lay if layers else (), wings=wl if elytra else None, skin_tex=skin), at=(at[0], at[1] + lift, at[2]), yaw=yaw, pitch=pitch)
    if helm:
        E = PK._ry(math.radians(-yaw)) @ PK._rx(math.radians(pitch))
        c = E @ np.array((0, SP.HEAD_Y[kind] * PK.S / 16, 0)) + np.array(at) + np.array((0, lift, 0))
        s.display(hm, pos=tuple(c), yaw=yaw, pitch=pitch, scale=0.625 * PK.S, ctx='head')
    if wings3d:
        W.render(s, wings3d, at=at, yaw=yaw, pitch=0.0 if kind == 'glide' else pitch, art=art)


def tile(view, text, sub=None, size=360, span=2.9, cy=1.12, root=None, **kw):
    s = SP.scene(root or NEW); SP.floor(s)
    wearer(s, **kw)
    return SP.label(SP.dark(s.render(view, size=size, span=span, center=(0, cy, 0))), text, sub)


if 'worn' in what:
    T = [tile('front', 'front', 'the plate, the Visage, the wings at rest', wings3d='rest_a'),
         tile('back', 'behind', 'the wings folded like a bat\'s, the tail', wings3d='rest_a'),
         tile((35, 12), 'three-quarter', None, wings3d='rest_a'),
         tile((150, 14), 'from behind, three-quarter', None, wings3d='rest_a'),
         tile('front', 'the plate alone', 'front (no 3D wings, no elytra)', elytra=False, helm=False),
         tile('back', 'the plate alone', 'behind', elytra=False, helm=False),
         tile((90, 4), 'the plate alone', 'its right side', elytra=False, helm=False),
         tile((-55, 25), 'the plate alone', 'from above', elytra=False, helm=False)]
    SP.sheet(T, f'{OUT}/dread_worn.png', cols=4, title='The Dreadborne - worn')
    L = [SP.flat(A.humanoid(), 'humanoid (bm:dread)', 'ribcage, spined pauldrons, chained vambraces; the Treads'),
         SP.flat(A.leggings(), 'humanoid_leggings (bm:dread)', 'chain belt, tassets, cuisses, knee eyes'),
         SP.flat(A.wings_layer(), 'wings (bm:dread_wings)', 'cut back to a mantle (the 3D wings own the rest)')]
    W0 = max(t.width for t in L); Hh = max(t.height for t in L)
    sh = Image.new('RGB', (W0 * 3, Hh), (14, 12, 22))
    for i, t in enumerate(L): sh.paste(t, (i * W0, 0))
    sh.save(f'{OUT}/dread_layers.png'); print(f'{OUT}/dread_layers.png')

if 'helm' in what:
    T = []
    for view, sub in (((180, 6), 'front'), ((145, 16), 'three-quarter'), ((90, 4), 'side'), ('front', 'behind'), ((200, 55), 'above')):
        s = SP.scene(NEW); s.display('bm:item/dread_helm', pos=(0, 0, 0), ctx='fixed')
        T.append(SP.label(SP.dark(s.render(view, size=330, span=1.6, center=(0, 0.25, 0))), 'Dread Visage', sub))
    s = SP.scene(NEW); SP.floor(s)
    wearer(s, skin='minecraft:entity/zombie/zombie', elytra=False)
    T.append(SP.label(SP.dark(s.render((25, 8), size=330, span=2.4, center=(0, 1.2, 0))), 'a Dread zombie', 'the monsters wear the same helm and plate'))
    SP.sheet(T, f'{OUT}/dread_helm.png', cols=3, title='The Dread Visage - seven eyes, a maw, a broken halo of thorns')

if 'wings' in what:
    T = [tile('back', 'at rest (sway a)', 'folded like a bat\'s; the ragged tail', wings3d='rest_a'),
         tile('back', 'at rest (sway b)', 'the idle sway, 50 ticks each way', wings3d='rest_b'),
         tile((60, 10), 'at rest, side', None, wings3d='rest_a'),
         tile('front', 'at rest, front', None, wings3d='rest_a'),
         tile('back', 'sneaking', 'leaning; drawn round like a mantle', kind='crouch', wings3d='sneak'),
         tile((70, 8), 'sneaking, side', None, kind='crouch', wings3d='sneak'),
         tile('back', 'riding', 'folded, the tail swept back', wings3d='ride'),
         tile((150, 10), 'falling (beat a)', 'spread, raised', wings3d='fall_a', span=4.4, cy=1.3),
         tile((150, 10), 'falling (beat b)', None, wings3d='fall_b', span=4.4, cy=1.3),
         tile((180, 55), 'gliding (beat a)', 'from behind and above', kind='glide', pitch=90, wings3d='glide_a', span=5.8, cy=0.3),
         tile((180, 55), 'gliding (beat b)', 'a slow, heavy beat (22 ticks each way)', kind='glide', pitch=90, wings3d='glide_b', span=5.8, cy=0.3),
         tile((215, 30), 'gliding, three-quarter', 'from the front, above', kind='glide', pitch=90, wings3d='glide_a', span=5.8, cy=0.3)]
    SP.sheet(T, f'{OUT}/dread_wings3d.png', cols=4, title="The Dread Carapace's wings - membrane on bone, eyes in it, a ragged tail")

if 'both' in what:
    T = []
    for st, kind, view, span, cy, pitch in (('rest_a', 'stand', 'back', 2.9, 1.12, 0), ('rest_a', 'stand', (30, 10), 2.9, 1.12, 0),
                                            ('fall_a', 'stand', (150, 10), 4.4, 1.3, 0), ('glide_a', 'glide', (180, 55), 5.8, 0.3, 90)):
        for set_ in ('seraph', 'dread'):
            T.append(tile(view, {'seraph': "The Seraph's Raiment", 'dread': 'The Dreadborne'}[set_], st, set_=set_, wings3d=st, kind=kind, span=span, cy=cy, pitch=pitch))
    SP.sheet(T, f'{OUT}/dread_vs_seraph.png', cols=4, title='The holy and the dread - side by side')

if 'before' in what and OLD:
    OLDR = os.path.join(SP.TMP, 'rp_dread_old')
    if os.path.exists(OLDR): shutil.rmtree(OLDR)
    def op(*a):
        f = os.path.join(OLDR, 'assets', 'bm', *a); os.makedirs(os.path.dirname(f), exist_ok=True); return f
    for f in os.listdir(os.path.join(OLD, 'block')): shutil.copy(os.path.join(OLD, 'block', f), op('textures', 'block', f))
    shutil.copy(os.path.join(OLD, 'dread_helm.json'), op('models', 'item', 'dread_helm.json'))
    shutil.copy(os.path.join(OLD, 'dread.png'), op('textures', 'entity', 'equipment', 'humanoid', 'dread.png'))
    shutil.copy(os.path.join(OLD, 'dread_leg.png'), op('textures', 'entity', 'equipment', 'humanoid_leggings', 'dread.png'))
    shutil.copy(os.path.join(OLD, 'dread_wings.png'), op('textures', 'entity', 'equipment', 'wings', 'dread_wings.png'))
    T = []
    for view, sub in (('front', 'front'), ('back', 'behind'), ((35, 12), 'three-quarter')):
        T.append(tile(view, 'BEFORE (2.93)', sub, root=OLDR))
        T.append(tile(view, 'AFTER (2.99)', sub, wings3d='rest_a'))
    for root, txt in ((OLDR, 'BEFORE'), (NEW, 'AFTER')):
        s = SP.scene(root); s.display('bm:item/dread_helm', pos=(0, 0, 0), ctx='fixed')
        T.append(SP.label(SP.dark(s.render((150, 12), size=360, span=1.6, center=(0, 0.25, 0))), txt, 'the Dread Visage'))
    for root, txt, w3 in ((OLDR, 'BEFORE', None), (NEW, 'AFTER', 'glide_a')):
        s = SP.scene(root); SP.floor(s); wearer(s, kind='glide', pitch=90, wings3d=w3)
        T.append(SP.label(SP.dark(s.render((150, 40), size=360, span=5.6, center=(0, 0.3, 0))), txt, 'gliding'))
    SP.sheet(T, f'{OUT}/dread_before_after.png', cols=2, title='The Dreadborne - before and after')

if 'icons' in what:
    import vanilla
    new = {k: vanilla.process(k, im) for k, im in A.icons().items()}; T = []
    for k in ('dread_carapace', 'dread_greaves', 'dread_treads'):
        if OLD and os.path.exists(f'{OLD}/{k}.png'): T.append(SP.flat(Image.open(f'{OLD}/{k}.png').convert('RGBA'), 'before', k, k=10))
        T.append(SP.flat(new[k], 'after', k, k=10))
    SP.sheet(T, f'{OUT}/dread_icons.png', cols=2 if OLD else 3, title='The Dreadborne - sprites')

if 'restored' in what:                                    # (v299: the owner kept the 2.90b Visage - on a player in the new plate, on a Dread zombie)
    T = []
    for view, sub in (((180, 6), 'front'), ((145, 16), 'three-quarter'), ('front', 'behind')):
        s = SP.scene(NEW); s.display('bm:item/dread_helm', pos=(0, 0, 0), ctx='fixed')
        T.append(SP.label(SP.dark(s.render(view, size=330, span=1.6, center=(0, 0.25, 0))), 'Dread Visage (2.90b, restored)', sub))
    for view in ('front', (35, 12)):
        T.append(tile(view, 'on a player', 'the new plate, the restored Visage, the wings at rest', wings3d='rest_a', size=330, span=3.1, cy=1.3))
    s = SP.scene(NEW); SP.floor(s)
    wearer(s, skin='minecraft:entity/zombie/zombie', elytra=False)
    T.append(SP.label(SP.dark(s.render((25, 8), size=330, span=2.6, center=(0, 1.2, 0))), 'a Dread zombie', 'the restored Visage, the new plate'))
    SP.sheet(T, f'{OUT}/dread_helm_restored.png', cols=3, title='The Dread Visage - restored (2.90b)')
