"""2.96a: THE CREATIVE FORMS' OUTFITS - the machinery (the outfits themselves, and why each is what it is: creative_art.py). A Buddy (and
Emma, Queen Ava, Democratus, KillerWatt, Queen Pearl) beside the Gem of Creativity dresses for it, in an outfit of their own.

HOW IT'S WORN: every part model of theirs gets a twin, <model>_cf - the same model with the outfit's pieces added - and every item
definition naming one chooses between them by the display's custom_model_data flag 0 (no flag: exactly the model it always was).
The datapack (phase233) raises that flag on their parts while the Creative Form pair runs and lowers it when they part; since the
flag sits beside the strings that faces, poses and looks choose by (keep_flags: every command that set the whole component now
sets only its strings), the outfit stays on through every pose, face, form and look.

WHERE THE PIECES GO: each piece is placed on the follower as they stand in their display-case figure (phase134.figures - world
units, facing +z), round the part it belongs to, then carried into that part's own model space (the part's display transform and
its figure transform, undone) - so it rides the part through every pose. A twin is made for every variant of a part with the same
geometry (faces, recolours, dresses); a variant of another shape (a chibi or ghostly form) keeps its own look."""
import json
import math
import os
import re

import numpy as np

PREFIX = {'fishy': ('fy_',), 'batty': ('gb_',), 'eggbert': ('ge_',), 'count': ('gc_',), 'capshun': ('mz_',), 'sky': ('yb_',),
          'kettle': ('kt_',), 'emma': ('em_', 'ee_', 'emkw_'), 'ava': ('av_',), 'demo': ('dm_',), 'kw': ('kw_',), 'pearlq': ('pq_',)}
FORMS = tuple(PREFIX)
ITEM = {'fishy': 'fy_bowl', 'batty': 'gentry_batty', 'eggbert': 'gentry_eggbert', 'count': 'gentry_count', 'capshun': 'capshun_pencil',
        'sky': 'sky_mobile', 'kettle': 'kettle_plane', 'emma': 'emma_ribbon', 'ava': 'av_locket', 'demo': 'demo_seal', 'kw': 'kw_spark',
        'pearlq': 'pq_pearls'}
# each one's outfit: (piece, the part it's worn on (its base model), options - host: the part whose model carries it, when the part's own
#  has no room: one that moves with it)
from creative_art import textures, design, RETEX, DERIVE, rx as _rx, ry as _ry, rz as _rz      # noqa: F401 (the outfits: creative_art.py)


# ---------------------------------------------------------------------------------------------------- into a part's model space
def _quat(q):
    x, y, z, w = q
    return np.array([[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
                     [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
                     [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]])


def _euler(M):
    """M = Rz(c) Ry(b) Rx(a) -> (a, b, c) in degrees"""
    b = math.asin(max(-1, min(1, -M[2, 0])))
    a = math.atan2(M[2, 1], M[2, 2]); c = math.atan2(M[1, 0], M[0, 0])
    return math.degrees(a), math.degrees(b), math.degrees(c)


def _xform(model, tr, L, R, sc):
    """(the part's world map: world = s * Rm @ u + b, u = p/16 - 0.5 in its model) -> (s, Rm, b)"""
    d = model.get('display', {}).get('fixed', {})
    dr = d.get('rotation', [0, 0, 0]); dt = np.array(d.get('translation', [0, 0, 0])) / 16; ds = d.get('scale', [1, 1, 1])
    assert abs(ds[0] - ds[1]) < 1e-6 and abs(ds[0] - ds[2]) < 1e-6
    sc = sc if not isinstance(sc, (list, tuple)) else sc[0]
    Dm = _rx(math.radians(dr[0])) @ _ry(math.radians(dr[1])) @ _rz(math.radians(dr[2]))
    Q = _quat(L) @ _quat(R)
    Rm = Q @ _ry(math.pi) @ Dm
    return sc * ds[0], Rm, Q @ (sc * (_ry(math.pi) @ dt)) + np.array(tr)


def _corners(e):
    f, t = e['from'], e['to']
    pts = [np.array([x, y, z], float) for x in (f[0], t[0]) for y in (f[1], t[1]) for z in (f[2], t[2])]
    r = e.get('rotation')
    if r:
        o = np.array(r['origin'], float)
        if 'axis' in r: M = {'x': _rx, 'y': _ry, 'z': _rz}[r['axis']](math.radians(r['angle']))
        else: M = _rz(math.radians(r.get('z', 0))) @ _ry(math.radians(r.get('y', 0))) @ _rx(math.radians(r.get('x', 0)))
        pts = [M @ (p - o) + o for p in pts]
    return pts


def world_bounds(model, xf):
    s, Rm, b = xf
    pts = [s * Rm @ (p / 16 - 0.5) + b for e in model.get('elements', []) for p in _corners(e)]
    if not pts: return None
    return np.min(pts, axis=0), np.max(pts, axis=0)


def to_model(boxes, xf):
    """world pieces -> elements in the part's model space (each turned on all three axes, as 26.x allows); a flat piece (sprite) has
    only its two broad faces"""
    s, Rm, b = xf
    els = []
    for p in boxes:
        c, h, tex, R0 = p['c'], p['h'], p['tex'], p['R']
        cm = 16 * (Rm.T @ (c - b) / s + 0.5)
        hm = h * 16 / s
        a, bb, cc = _euler(Rm.T @ R0)
        faces = ('north', 'south', 'east', 'west', 'up', 'down')
        if p.get('sprite'):
            faces = {0: ('east', 'west'), 1: ('up', 'down'), 2: ('north', 'south')}[int(np.argmin(h))]
        e = {'from': [round(float(v), 3) for v in cm - hm], 'to': [round(float(v), 3) for v in cm + hm],
             'rotation': {'origin': [round(float(v), 3) for v in cm], 'x': round(a, 3), 'y': round(bb, 3), 'z': round(cc, 3)},
             'faces': {f: {'uv': [0, 0, 16, 16], 'texture': f'#{tex}'} for f in faces}}
        if p.get('glow'): e['light_emission'] = int(p['glow'])
        els.append(e)
    return els


def _fits(els):
    return all(-16 <= v <= 32 for e in els for v in e['from'] + e['to'])


def _geom(m):
    return json.dumps([m.get('elements', [])[:3], m.get('display', {}).get('fixed')], sort_keys=True)


# ---------------------------------------------------------------------------------------------------- the resource pack
def build(rp_dir, FIG, log=print):
    """(a post pass) the twins <model>_cf and the item definitions' choice between them; -> {follower: [pieces placed]}"""
    md = os.path.join(rp_dir, 'assets/bm/models/item')
    idir = os.path.join(rp_dir, 'assets/bm/items')
    load = lambda n: json.load(open(os.path.join(md, n + '.json')))
    names = [f[:-5] for f in os.listdir(md) if f.endswith('.json')]
    twins = set()
    placed = {}
    # (restyled textures, drawn from the part's own: creative_art.DERIVE)
    from PIL import Image
    tdir = os.path.join(rp_dir, 'assets/bm/textures/block')
    for new, (orig, fn) in DERIVE.items():
        fn(Image.open(os.path.join(tdir, orig + '.png')).convert('RGBA')).save(os.path.join(tdir, new + '.png'))
    for w in FORMS:
        parts = FIG[ITEM[w]][1]
        xfs, bounds = {}, {}
        for mid, tr, L, R, sc in parts:
            n = mid.split(':')[1].split('/')[-1]
            m = load(n)
            xfs[n] = _xform(m, tr, L, R, sc)
            wb = world_bounds(m, xfs[n])
            if wb is not None: bounds[n] = wb
        adds = {}
        for part, pieces, host in design(w, bounds):
            host = host or part                       # (a part whose model has no room for it: carried by one that moves with it)
            hgt = bounds[part][1][1] - bounds[part][0][1]
            for k in range(21):                       # (no room above, in its model: it sits a little lower, till it fits)
                els = to_model([dict(p, c=p['c'] - np.array([0, 0.02 * k * hgt, 0])) for p in pieces], xfs[host])
                if _fits(els): break
            assert _fits(els), (w, part, host, [[round(float(v), 1) for v in e['from'] + e['to']] for e in els if not _fits([e])])
            if k: log(f'creative: {w} on {part} sat {k * 2}% lower to fit {host}')
            adds.setdefault(host, []).extend(els)
            placed.setdefault(w, []).append(f'{len(pieces)} on {part}')
        retex = RETEX.get(w, {})
        for part in retex: adds.setdefault(part, [])
        for part, els in adds.items():
            base = load(part)
            g = _geom(base)
            for n in [n for n in names if n == part or n.startswith(part + '_')]:
                if n.endswith('_cf'): continue
                m = load(n)
                if _geom(m) != g and n != part: continue          # (a part of another shape: a form of its own)
                m2 = dict(m)
                m2['elements'] = list(m.get('elements', [])) + els
                tex = dict(m.get('textures', {}))
                for e in els:
                    for f in e['faces'].values():
                        t = f['texture'][1:]; tex[t] = f'bm:block/{t}'
                for k, v in retex.get(part, {}).items():          # (its own texture, restyled)
                    if k in tex: tex[k] = f'bm:block/{v}'
                m2['textures'] = tex
                json.dump(m2, open(os.path.join(md, n + '_cf.json'), 'w'), separators=(',', ':'))
                twins.add(f'bm:item/{n}')
    # every item definition naming a model with a twin: the flag chooses
    n_i = 0
    pre = tuple(p for ps in PREFIX.values() for p in ps)
    for f in os.listdir(idir):
        if not f.startswith(pre) or not f.endswith('.json'): continue
        path = os.path.join(idir, f)
        d = json.load(open(path))
        if not any(r in twins for r in re.findall(r'"model":\s*"([^"]+)"', json.dumps(d))): continue
        def twin(node):
            if isinstance(node, dict):
                node = {k: twin(v) for k, v in node.items()}
                if node.get('type') == 'minecraft:model' and node.get('model') in twins: node['model'] += '_cf'
                return node
            if isinstance(node, list): return [twin(v) for v in node]
            return node
        d['model'] = {'type': 'minecraft:condition', 'property': 'minecraft:custom_model_data', 'index': 0,
                      'on_true': twin(d['model']), 'on_false': d['model']}
        json.dump(d, open(path, 'w'), separators=(',', ':'))
        n_i += 1
    log(f'creative: {len(twins)} part models with an outfit twin, {n_i} item definitions choose by the flag')
    return placed


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])

    def post(R2):
        import phase134 as P134, phase136                     # noqa: F401
        build(R2.p(), P134.figures())
    R.POST.append(post)


# ---------------------------------------------------------------------------------------------------- the datapack: keep the flag
CMD_SET = re.compile(r'item\.components\."minecraft:custom_model_data" set value \{strings:(\[[^\]]*\])\}')
CMD_DEL = re.compile(r'^(\$?(?:execute .* run )?data remove entity .*item\.components\."minecraft:custom_model_data")$')


def keep_flags(G):
    """(a build pass) a line that set a display's whole custom_model_data to choose a face, a pose or a look sets only its strings
    now - and one that removed it removes only them - so a flag beside them (a Creative Form's outfit) stays up"""
    n = 0
    for name, L in G.FUNCS.items():
        for i, l in enumerate(L):
            l2 = CMD_SET.sub(r'item.components."minecraft:custom_model_data".strings set value \1', l)
            l2 = CMD_DEL.sub(r'\1.strings', l2)
            if l2 != l:
                L[i] = l2; n += 1
    return n
