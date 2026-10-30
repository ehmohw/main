"""(3.0a) The Lightbringer's elemental forms - ETHEREAL ('_e') and WRAITHFIRE ('_w'), each on her and on him ('_m'): preview sheets.
python3 tools/preview/lightbringer_forms.py [forms,faces,night,oph,looks,poses,check]
Writes to $BM_PREVIEW_DIR (default: previews/v300a_lightbringer_forms); the throwaway packs go to $BM_SCRATCH (default /tmp/bm_previews).
forms  lb_forms_<view>.png: she and he in each of base / Ethereal / Wraithfire beside a player - front, 3/4, back
faces  lb_forms_faces.png: their faces in each form, close (default, happy, fierce, surprised)
night  lb_forms_night.png: every form by night (tools/render has no light: unlit faces dimmed, lit ones kept by their level)
oph    lb_forms_oph.png: the Ophanim's charged attack begun in each element form (the wheel above; the rig's own models)
looks  lb_forms_looks.png: wardrobe looks and the shiny on each form (phase138 recolours lb_robe / lb_bodice and their _e / _w twins)
poses  lb_forms_poses.png: a run of poses in each element form (the same rig)
check  lb_forms_check.txt: every element twin against its base - same elements and boxes (so the clip check and the joints
       are hers), coords in the model box, uvs in 0..16, every texture there; and zfix's z-fight test over the forms' models"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); BM = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, BM)
os.environ.setdefault('BM_PREVIEW_DIR', os.path.join(os.path.dirname(BM), 'previews', 'v300a_lightbringer_forms'))
import numpy as np
from PIL import Image
import draftkit as K, lightbringer_art as A, rigkit
import lightbringer_male as LM                       # (its culled render, night scene and labels)
OUT = os.environ['BM_PREVIEW_DIR']; os.makedirs(OUT, exist_ok=True)
SCRATCH = os.environ.get('BM_SCRATCH', '/tmp/bm_previews'); os.makedirs(SCRATCH, exist_ok=True)
what = sys.argv[1].split(',') if len(sys.argv) > 1 else ['forms', 'faces', 'night', 'oph', 'looks', 'poses', 'check']
ROOT = K.pack(A, f'{SCRATCH}/rp_lb_forms')
I = A.POSES['idle_a']
FORMS = (('', 'base (pearl and gold)'), (A.ETHEREAL, 'ETHEREAL'), (A.WRAITH, 'WRAITHFIRE'))
VIEWS = (('front', 'front'), ((-35, 12), '3/4'), ((180, 6), 'back'))


def pair(el, view, label, sub=None, night=False, size=520, root=None, pose=I):
    """her (left), a player (middle), him (right) - in the form `el`"""
    s = LM.night_scene(root or ROOT) if night else K.multi_scene(root or ROOT)
    rigkit.render(s, A, pose, at=(-1.15, 0, 0), scale=A.RIG_SCALE, suffix=el)
    rigkit.render(s, A, pose, at=(1.15, 0, 0), scale=A.RIG_SCALE, suffix=A.MALE + el)
    K.person(s, (0.0, 0, 0.0))
    im = LM.cull_render(s, view, size=size, span=3.8, center=(0, 1.05, 0))
    return LM.dark_label(LM.darken(im), label, sub) if night else K.label(im, label, sub)


def tile(pose, sfx, view=(-30, 12), span=2.6, center=(0, 1.0, 0), size=340, label='', sub=None, root=None, night=False, extra=None):
    s = LM.night_scene(*([root or ROOT] + (extra or []))) if night else K.multi_scene(*([root or ROOT] + (extra or [])))
    rigkit.render(s, A, pose, scale=A.RIG_SCALE, suffix=sfx)
    im = LM.cull_render(s, view, size=size, span=span, center=center)
    return LM.dark_label(LM.darken(im), label, sub) if night else K.label(im, label, sub)


if 'forms' in what:
    tiles = []
    for el, nm in FORMS:
        for v, vn in VIEWS:
            tiles.append(pair(el, v, f'{nm} - {vn}', 'she - a player - he'))
    K.sheet(tiles, OUT + '/lb_forms_all.png', cols=3, title='The Lightbringer - she and he in each form (base / Ethereal / Wraithfire), beside a player')
    for v, vn in VIEWS:
        K.sheet([pair(el, v, nm, 'she - a player - he', size=620) for el, nm in FORMS], OUT + f'/lb_forms_{vn.replace("/", "q")}.png', cols=3,
                title=f'The Lightbringer - every form, {vn}')
if 'faces' in what:
    tiles = []
    for g, gn in (('', 'she'), (A.MALE, 'he')):
        for el, nm in FORMS:
            for f in (None, 'happy', 'fierce', 'surprised'):
                pose = {k: v for k, v in dict(I, _face=f, head=rigkit.I).items() if v is not None}
                tiles.append(tile(pose, g + el, 'front', span=0.62, center=(0, 1.6, 0), size=300, label=f'{gn}, {nm.split(" ")[0]}', sub=f or 'serene'))
    K.sheet(tiles, OUT + '/lb_forms_faces.png', cols=12, title='The Lightbringer - faces in each form (her row, then his): serene, happy, fierce, surprised')
    tiles = []
    for g, gn in (('', 'she'), (A.MALE, 'he')):
        for el, nm in FORMS:
            tiles.append(tile(I, g + el, (-30, 8), span=0.95, center=(0, 1.66, 0), size=360, label=f'{gn}, {nm.split(" ")[0]}', sub='head and halo, 3/4'))
    K.sheet(tiles, OUT + '/lb_forms_heads.png', cols=3, title='The Lightbringer - head and halo in each form: the gold halo, the ring of stars, the flame halo')
if 'night' in what:
    tiles = []
    for el, nm in FORMS:
        tiles += [pair(el, 'front', f'{nm}, by night', 'she - a player - he', night=True), pair(el, (-35, 12), f'{nm}, by night, 3/4', night=True),
                  pair(el, (-35, 12), f'{nm}, by night, sitting', night=True, pose=A.POSES['sit_b'])]
    K.sheet(tiles, OUT + '/lb_forms_night.png', cols=3, title='The Lightbringer - every form by night (what glows: light_emission; her night glow lights the rest in the game)')
if 'oph' in what:
    import ophan_art as OA
    from rigkit import qs
    ro = K.pack(OA, f'{SCRATCH}/rp_oph')
    tiles = []
    for sfx, nm in ((A.ETHEREAL, 'she, Ethereal'), (A.MALE + A.ETHEREAL, 'he, Ethereal'), (A.WRAITH, 'she, Wraithfire'), (A.MALE + A.WRAITH, 'he, Wraithfire')):
        for night in (False, True):
            s = (LM.night_scene if night else K.multi_scene)(ROOT, ro)
            rigkit.render(s, A, A.POSES['wings_spread'], at=(0, 0, 0), scale=A.RIG_SCALE, suffix=sfx)
            pose = {'ring_a': qs(('y', 28)), 'ring_b': qs(('x', 38)), 'ring_c': qs(('z', -35)), 'core': qs(('y', 20))}
            for p in OA.PARTS:
                s.display(f'bm:item/{OA.model_id(p)}', pos=(0, 3.9, 0), scale=OA.SCALE, left=tuple(pose.get(p, rigkit.I)))
            K.person(s, (2.0, 0, 0.5))
            im = LM.cull_render(s, (-24, 10), size=440, span=8.5, center=(0.4, 3.3, 0))
            tiles.append(LM.dark_label(LM.darken(im), nm + ', by night') if night else K.label(im, nm, 'the wheel opens over the rig - its own models, unchanged'))
    K.sheet(tiles, OUT + '/lb_forms_oph.png', cols=4, title='The Lightbringer - the Ophanim begun in each element form (the rig hides while it turns, then wings_spread in the same models)')
if 'looks' in what:
    import phase99 as P99, gild, shiny
    T0 = A.textures()
    looks = [(k, nm, pal) for k, (nm, pal) in P99.NEW['lightbringer'][3].items() if k in (1, 3, 4)] + \
            [(k, nm, pal) for k, (nm, pal) in P99.NEW['lightbringer'][3].items() if nm == shiny.LOOKS['lightbringer'][0]]
    tiles = []
    for el, enm in FORMS[1:]:
        tiles.append(tile(I, el, label=f'{enm}', sub='(her own colours)'))
        for k, name, pal in looks:
            root = f'{SCRATCH}/rp_lb_forms_c{k}'
            if not os.path.exists(root + '/assets'):
                import shutil; shutil.copytree(ROOT, root)
            keys = ('lb_robe' + el, 'lb_bodice' + el)
            ims = {n: gild.dress('lightbringer', k, T0[n]) for n in keys} if gild.is_gilded('lightbringer', k) else P99._recolour({n: T0[n] for n in keys}, pal)
            for n, im in ims.items(): im.save(f'{root}/assets/bm/textures/block/{n}.png')
            tiles.append(tile(I, el, label=f'{enm}: {name}', root=root))
    K.sheet(tiles, OUT + '/lb_forms_looks.png', cols=len(looks) + 1, title='The Lightbringer - wardrobe looks and the shiny on the Ethereal and Wraithfire forms (her robe and bodice recoloured, as a set of their own)')
if 'poses' in what:
    names = ['idle_b', 'walk_1', 'run_0', 'smite_up', 'smite', 'bless', 'ward', 'pray', 'wings_spread', 'sit_b', 'hurt']
    tiles = []
    for sfx, nm in ((A.ETHEREAL, 'she, Ethereal'), (A.MALE + A.WRAITH, 'he, Wraithfire')):
        tiles += [tile(A.POSES[n], sfx, label=n, sub=nm, size=300) for n in names]
    K.sheet(tiles, OUT + '/lb_forms_poses.png', cols=len(names), title='The Lightbringer - poses in the element forms (the same rig): her Ethereal, his Wraithfire')
if 'check' in what:
    import zfix
    M, T = A.models(), A.textures()
    lines, bad = [], 0
    for name, (tex, els) in sorted(M.items()):
        for e in els:
            for v in e['from'] + e['to']:
                if not -16 <= v <= 32: bad += 1; lines.append(f'out of the box: {name} {e["from"]} {e["to"]}')
            for fc, f in e['faces'].items():
                if any(not 0 <= u <= 16 for u in f['uv']): bad += 1; lines.append(f'uv: {name} {fc} {f["uv"]}')
                if f['texture'][1:] not in T: bad += 1; lines.append(f'no texture: {name} {f["texture"]}')
        for sfx in A.ELEMENTS:                                              # (an element's twin: the very same boxes, but the halo)
            if name.endswith(A.ELEMENTS): continue
            tw = M.get(name + sfx)
            if tw is None: bad += 1; lines.append(f'no twin: {name}{sfx}'); continue
            if 'halo' in name: continue
            if [(e['from'], e['to'], e.get('rotation')) for e in tw[1]] != [(e['from'], e['to'], e.get('rotation')) for e in els]:
                bad += 1; lines.append(f'twin differs: {name}{sfx}')
    lines.append(f'coords / uvs / textures / twins: {bad} problems over {len(M)} models ({sum(1 for n in M if n.endswith(A.ELEMENTS))} element twins)')
    n = 0
    for f in sorted(os.listdir(f'{ROOT}/assets/bm/models/item')):
        if not f.startswith(A.PREFIX) or not f[:-5].endswith(A.ELEMENTS): continue
        m = json.load(open(f'{ROOT}/assets/bm/models/item/{f}'))
        k = zfix.fix_model(f'{ROOT}/assets', m)
        if k: lines.append(f'z-fighting: {f} {k}')
        n += k
    lines.append(f'zfight: faces zfix would move in the element twins = {n}')
    rep = LM.clip_report(['idle_a', 'smite_up', 'ward', 'pray', 'wings_spread', 'sit_a', 'run_0'], A.ETHEREAL) if False else []
    open(OUT + '/lb_forms_check.txt', 'w').write('\n'.join(lines) + '\n'); print('\n'.join(lines[-6:]))
