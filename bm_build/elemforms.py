"""3.0g: ETHEREAL AND WRAITHFIRE FORMS FOR TEN MORE FOLLOWERS - Bender, Mr. Capshun, the Bound Sovereign, the Keeper of Bonds, the
Arachno-Lantern, Leo, Celi, Democratus; and two joke forms that are actually kind of OP, the Eraser's and Donado's.

THE GIVING (as the Gem's are: phase231): right-click one of them (yours, out with you) holding an ETHEREAL GEM or a WRAITHFIRE HEART.
  It KEEPS it (one taken from your hand) and takes that form at once - one at a time: hand it the other and the first comes back to
  you. What it holds and whether the form shows is yours (bm.ef<k> on you: 1 the gem, 2 the heart, +10 while the form shows), so
  sent home, fainted, logged out - it comes back in it. THEIR WARDROBE (sneak + use their item; Wardrobe) has two rows of their own
  (phase99.ROWS, codes in each wardrobe's block): ETHEREAL / WRAITHFIRE (the form on or off, the gem or heart kept) and GIVE BACK
  THE GEM / HEART (handed back; their own look again). Celi and Leo's wardrobe is their menu; the rest reach it from theirs.
THE LOOK (one helper for all ten - the Creative Forms' trick, phase233/creative.py, on another channel): every item definition of
  theirs (every part, face, pose, look, the creative outfit too) chooses by its display's custom_model_data FLOAT 0 - none: exactly
  what it always was; 1: its ETHEREAL twin; 2: its WRAITHFIRE twin (bm:item/elf/<model>_e / _w). The twins are made at the end of the
  resource pack's build from the finished models and textures (rp, below): the same elements, the textures recoloured
  procedurally (_ethereal / _wraith, below), the glow (light_emission) raised, and a few accents added where they're cheap. So every
  pose, face, form and look keeps working, and a look's colours give way to the form's (the form overrides colours, as Cecil's gems
  do; a look's model is mapped to its base model's twin). The datapack raises the float on their parts (keep: every tick while a
  form shows, a part summoned plain - a new rig, a call - is dressed within the tick) and lowers it when the form goes (repaint).
  Nothing else in the pack touches floats (creative.keep_flags keeps a display's custom_model_data whole but its strings).
  ETHEREAL   crystalline, prismatic light - pale cyan and white, a diamond's facets, rainbow glints, glowing.
  WRAITHFIRE soul fire - smoky dark, veined and edged with cyan-blue flame, embers and soul motes; eyes and fires burn cyan.
  Each follower's own accents (ACCENT: Leo's trident, Democratus's scythe, the Keeper's threads, the Lantern's carved face and
  flame...) take the form's brightest light; a few get small accent parts (SPIKES: crystal spikes on Bender's back, a crown of ice on
  Celi; soul-fire tongues in Wraithfire).
WHAT IT DOES (hits, below: every blow of theirs - each `damage @s N ... by <its *me tag>` line, and rigpet's hurt):
  ETHEREAL   +2 to every blow, and a prismatic flash on the foe.
  WRAITHFIRE every blow sets the foe alight (soul fire); beside it (16), fire can't touch you (Fire Resistance).
  THE ERASER (joke, OP):  ETHEREAL "CLEAN SLATE" - now and then (every ~5 s, and a third of its blows) it rubs a weak monster
              (12 health left or less, no boss, nothing over 60 health) right out of existence. WRAITHFIRE "NO MORE FIRE" - every
              second it rubs out the fire round you (and the lava, in the Overworld, the Nether and the End: you stand in a hole
              in it), and you're fireproof.
  DONADO (joke, OP):      ETHEREAL "TRACTOR BEAM" - Specimen 042 learnt a thing or two aboard the mothership: every 5 s the nearest
              monster (no boss) is beamed up in a prismatic tractor beam, and let go. WRAITHFIRE "SOUL ZOOMIES" - every 8 s, with
              monsters near you, he tears round you in a ring of soul fire: every monster within 6 burns, takes 5 and is thrown
              back; you get the zoomies too (Speed, Fire Resistance).
Figurines and dolls are unchanged (their displays carry no float)."""
import json
import math
import os
import re
import colorsys

import rigkit as _RK

from items import T, ITEMS

ETH, WR = 'e', 'w'
ETH_C, WR_C = '#e8d8ff', '#5ae0ff'
FLOAT = {ETH: 1, WR: 2}
SUB = 'elf'                                  # (the twins' own folders: bm:item/elf/..., bm:block/elf/...)

# ---------------------------------------------------------------------------------------------------- the ten
# k: wardrobe key (phase99), the score stem (bm.ef<s>), their item-definition prefixes, the host (type, tag), their parts as the host
# sees them ('rig' tag + excluded tags, or 'riders' tag), the blow tag (atk.ME), the click (rigpet / own 'who' / 'adv' / donado's),
# ACCENT / GLOW: texture names (or stems) that take the form's brightest light, SPIKES: (models, count) given accent parts
FOL = {
    'bender':    dict(s='bv', pre=('bd_',), host='bm.bvpet', parts=('rig', 'bm.bvp_pet', ('bm.bvfade',)), me='bm.bvme', who='p195/who', hurt='p195/hurt',
                      item='bv_ball', accent=('bd_ear_in', 'bd_tip'), glow=('bd_face',), spikes=(('bd_body',), 4)),
    'capshun':   dict(s='mz', pre=('mz_',), host='bm.mzpet', parts=('rig', 'bm.mzp_pet', ('bm.mzfade',)), me='bm.mzme', who='p198/who', hurt='p198/hurt',
                      item='capshun_pencil', accent=('mz_t_', 'mz_sk_', 'mz_ink'), glow=('mz_face',), spikes=((), 0)),
    'sovereign': dict(s='xv', pre=('ds_',), host='bm.xvpet', parts=('rig', 'bm.xvp_pet', ('bm.xvfade',)), me='bm.xvme', who='p239/who', hurt='p239/hurt',
                      item='sov_eye', accent=('ds_chain', 'ds_horn', 'ds_glass', 'ds_edge'), glow=('ds_eye', 'ds_beye', 'ds_heart', 'ds_red'), spikes=((), 0)),
    'keeper':    dict(s='tk', pre=('kb_',), host='bm.tkpet', parts=('rig', 'bm.tkp_pet', ('bm.tkfade',)), me='bm.tkme', who='p254/who', hurt='p254/hurt',
                      item='bond_thread', accent=('kb_bonds', 'kb_brd', 'kb_ray', 'kb_tier', 'kb_wing', 'kb_gold', 'kb_rim'), glow=('kb_eyes', 'kb_light'), spikes=((), 0)),
    'lantern':   dict(s='ln', pre=('ln_',), host='bm.lnpet', parts=('rig', 'bm.lnp_pet', ('bm.lnfade',)), me='bm.lnme', who='p194/who', hurt='p194/hurt',
                      item='ln_gourd', accent=('ln_stem', 'ln_leaf'), glow=('ln_flame', 'ln_tongue'), holes=('ln_face',), spikes=((), 0)),
    'leo':       dict(s='le', pre=('le_',), host='bm.leopet', parts=('rig', 'bm.lep', ('bm.lefade', 'bm.leencp')), me='bm.leme', who='p96/who', hurt=None,
                      item='leo_crest', accent=('le_tri', 'le_gem', 'le_emblem', 'le_gold'), glow=(), spikes=((), 0)),
    'celi':      dict(s='ce', pre=('ce_',), host='bm.celipet', parts=('rig', 'bm.cep', ('bm.cefade', 'bm.ceencp')), me='bm.ceme', who='adv', hurt=None,
                      item='celi_charm', accent=('ce_ice', 'ce_moon', 'ce_star', 'ce_band'), glow=(), spikes=(('ce_head',), 5)),
    'demo':      dict(s='dm', pre=('dm_',), host='bm.dmpet', parts=('rig', 'bm.dmp', ('bm.dmfade', 'bm.dmencp', 'bm.dmbp')), me='bm.dmme', who='p97/who', hurt=None,
                      item='demo_seal', accent=('dm_blade', 'dm_crystal', 'dm_gem', 'dm_gold', 'dm_buckle'), glow=('dm_glow',), spikes=((), 0)),
    'eraser':    dict(s='ez', pre=('er_',), host='bm.ezpet', parts=('rig', 'bm.ezp_pet', ('bm.ezfade',)), me='bm.ezme', who='p235e/who', hurt='p235e/hurt',
                      item='eraser_crumb', accent=('er_crumb', 'er_worn'), glow=('er_face',), spikes=((), 0)),
    'don':       dict(s='dn', pre=('dnr_',), host='bm.donado,tag=!bm.ffpet', parts=('riders', 'bm.dnr', ()), me=None, who='p25/don/interact', hurt=None,
                      item='donado_tag', accent=('don_patch', 'don_ear'), glow=(), spikes=((), 0)),
}
JOKE = ('eraser', 'don')


def obj(k):
    return f'bm.ef{FOL[k]["s"]}'


# ---------------------------------------------------------------------------------------------------- the art (numpy)
def _np():
    import numpy as np
    return np


def _hexf(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def _ramp(stops, t):
    """stops: hex colours; t: array 0..1 -> (..., 3) floats"""
    np = _np()
    S = np.array([_hexf(s) for s in stops])
    t = np.clip(np.nan_to_num(np.asarray(t, float)), 0, 1) * (len(stops) - 1)
    i = np.minimum(t.astype(int), len(stops) - 2)
    f = (t - i)[..., None]
    return S[i] * (1 - f) + S[i + 1] * f


def _hash(x, y, seed):
    np = _np()
    v = (x.astype(np.int64) * 73856093) ^ (y.astype(np.int64) * 19349663) ^ (seed * 83492791)
    return ((v * 2654435761) & 0xffffffff) / 0xffffffff


def _vnoise(x, y, scale, seed):
    """smooth value noise on a grid of `scale` texels"""
    np = _np()
    gx, gy = x / scale, y / scale
    x0, y0 = np.floor(gx).astype(int), np.floor(gy).astype(int)
    fx, fy = gx - x0, gy - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    h = lambda a, b: _hash(a, b, seed)
    return (h(x0, y0) * (1 - fx) + h(x0 + 1, y0) * fx) * (1 - fy) + (h(x0, y0 + 1) * (1 - fx) + h(x0 + 1, y0 + 1) * fx) * fy


def _rainbow(h, l, s):
    """hls -> rgb, over arrays (colorsys's formula)"""
    np = _np()
    h = np.mod(h, 1.0)
    l = np.broadcast_to(np.asarray(l, float), h.shape)
    m2 = np.where(l <= 0.5, l * (1 + s), l + s - l * s)
    m1 = 2 * l - m2

    def v(hh):
        hh = np.mod(hh, 1.0)
        return np.where(hh < 1 / 6, m1 + (m2 - m1) * hh * 6, np.where(hh < 0.5, m2, np.where(hh < 2 / 3, m1 + (m2 - m1) * (2 / 3 - hh) * 6, m1)))
    return np.stack([v(h + 1 / 3), v(h), v(h - 1 / 3)], -1)


def _prep(im):
    np = _np()
    a = np.asarray(im.convert('RGBA')).astype(float) / 255
    rgb, al = a[..., :3], a[..., 3]
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    vis = al > 0
    lo, hi = (lum[vis].min(), lum[vis].max()) if vis.any() else (0, 1)
    t = np.clip((lum - lo) / max(1e-6, hi - lo), 0, 1) if hi - lo > 0.04 else np.full(lum.shape, 0.55)
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    H, W = lum.shape
    yy, xx = np.mgrid[0:H, 0:W]
    cell = max(1, W // 16)                             # (the pack paints in cells: a 16-px texture's texel, a 64-px one's 4)
    return np, rgb, al, lum, t, sat, xx // cell, yy // cell, xx, yy, cell


def _out(np, rgb, al):
    from PIL import Image
    a = np.concatenate([np.clip(rgb, 0, 1), al[..., None]], -1)
    return Image.fromarray((a * 255 + 0.5).astype('uint8'), 'RGBA')


def ethereal(im, kind='base', seed=1, holes=False):
    """crystalline, prismatic light: pale ice-blue to white, cut into a diamond's facets (a diagonal lattice of panes, each tinted
    a little - ice, lavender, mint, rose - their edges prismatic, a pastel rainbow along them), white glints; the darkest marks
    (eyes, mouths, lines) stay deep sapphire so a face still reads. kind: 'accent' - rainbow crystal, brighter; 'glow' - white-cyan
    light"""
    np, rgb, al, lum, t, sat, cx, cy, xx, yy, cell = _prep(im)
    t2 = 0.55 * t + 0.45 * lum
    if holes: t2 = 0.05 + t2 * 0.3                                  # (a carved rind: deeper crystal, so the light inside shows)
    base = _ramp(['#2f78c0', '#58b4e6', '#96e0f8', '#d2f8ff', '#ffffff'], 0.12 + 0.88 * t2)
    # (the facets: panes of a diamond lattice, each its own tint; their edges catch the light and split it)
    u, v = cx + cy, cx - cy
    pane = _hash(u // 4, v // 4, seed)
    tints = np.array([_hexf(h) for h in ('#9ae4ff', '#c4b8ff', '#9cf8dc', '#ffc4ea', '#e8f8ff')])
    tint = tints[np.minimum((pane * len(tints)).astype(int), len(tints) - 1)]
    base = base * 0.74 + tint * 0.26
    base = base * (0.84 + 0.22 * pane)[..., None]
    edge = ((u % 4) == 0) | ((v % 4) == 0)
    hue = (cx + cy) / 20.0 + 0.13 * seed
    edgec = _rainbow(hue, 0.8, 1.0) * 0.5 + 0.5
    out = np.where(edge[..., None], base * 0.25 + edgec * 0.75, base)
    if kind == 'accent':
        band = _rainbow((cx * 0.7 + cy) / 9.0 + 0.2 * seed, 0.72, 1.0)
        out = out * 0.45 + band * 0.55
        out = np.where(edge[..., None], out * 0.5 + 0.5, out)
    if kind == 'glow':
        out = _ramp(['#a8f4ff', '#e8ffff', '#ffffff'], 0.3 + 0.7 * t2) * 0.88 + _rainbow(hue, 0.85, 0.9) * 0.12
    dark = (lum < 0.15) & (t < 0.3) & (kind == 'base')          # (marks darker than the rest of their texture: eyes, mouths, lines)
    if holes: out = out * 0.6
    out = np.where(dark[..., None], _ramp(['#e8ffff', '#ffffff'], t * 4) if holes else _ramp(['#1a2466', '#34449a'], t * 4), out)
    g = _hash(cx, cy, seed + 7)
    out = np.where(((g < 0.035) & ~dark)[..., None], 1.0, out)                                                  # (white glints)
    out = np.where(((g > 0.99) & ~dark)[..., None], _rainbow(g * 37, 0.8, 1.0), out)                              # (a few in colour)
    return _out(np, out, al)


def wraith(im, kind='base', seed=1, face=False):
    """soul fire: smoky dark (charcoal to deep sea-teal), veined with cyan-blue flame along the contours of a slow noise, the
    brightest of it licking up cyan; embers. kind 'accent' / 'glow' - cyan flame through and through. face: its darkest marks
    (eyes) burn cyan"""
    np, rgb, al, lum, t, sat, cx, cy, xx, yy, cell = _prep(im)
    t2 = 0.5 * t + 0.5 * lum
    smoke = _ramp(['#070d14', '#0c2130', '#123a4a', '#1a5a6e', '#2e8ca4'], 0.12 + 0.72 * np.power(t2, 1.15))
    n = _vnoise(cx * 1.0, cy * 0.35, 5.0, seed) * 0.7 + _vnoise(cx * 1.0, cy * 0.35, 2.2, seed + 3) * 0.3
    vein = np.clip(1.25 - np.abs(np.mod(n * 5.0, 1.0) - 0.5) * 6.5, 0, 1)            # (contours of a tall noise: flame veins, rising)
    flame = _ramp(['#1a8cb0', '#3ad0ea', '#9af6ff', '#ffffff'], 0.25 + 0.75 * t2)
    out = smoke * (1 - vein[..., None] * 0.9) + flame * (vein[..., None] * 0.9)
    lick = np.clip((t2 - 0.72) * 3.2, 0, 1)[..., None]                               # (its highlights catch fire)
    out = out * (1 - lick * 0.6) + flame * lick * 0.6
    if kind in ('accent', 'glow'):
        hot = _ramp(['#0c6a88', '#1aa8c8', '#6ef0ff', '#c8fcff', '#ffffff'], 0.2 + 0.8 * t2)
        out = hot * 0.8 + flame * 0.2 * vein[..., None] + hot * 0.2 * (1 - vein[..., None])
    dark = (lum < 0.15) & (t < 0.3)
    if kind == 'accent':
        dark = dark & False
    if face or kind == 'glow':
        out = np.where(dark[..., None], _ramp(['#6ef0ff', '#e0ffff'], 1 - lum * 5), out)                # (the eyes burn)
    else:
        out = np.where(dark[..., None], _ramp(['#03070b', '#0a1822'], t * 4), out)
    e = _hash(cx, cy, seed + 11)
    out = np.where(((e < 0.018) & (kind == 'base'))[..., None], _ramp(['#6ef0ff', '#ffffff'], e * 50), out)   # (embers)
    return _out(np, out, al)


def crystal_tex():
    """the accent parts' own texture: an Ethereal crystal (16 px, facets and a rainbow)"""
    from PIL import Image
    np = _np()
    yy, xx = np.mgrid[0:16, 0:16]
    t = 0.55 + 0.45 * np.sin((xx + yy) / 3.2)
    rgb = _ramp(['#bfe8ff', '#e8fbff', '#ffffff'], t) * 0.8 + _rainbow((xx + yy) / 18.0, 0.85, 0.9) * 0.2
    rgb = np.where((((xx + yy) % 5) == 0)[..., None], 1.0, rgb)
    return _out(np, rgb, np.ones((16, 16)))


def flame_strip(frames=8):
    """the Wraithfire accent parts' texture: tongues of cyan flame rising, an animated strip (frametime 2)"""
    np = _np()
    H = 16 * frames
    yy, xx = np.mgrid[0:H, 0:16]
    f, y = yy // 16, yy % 16
    n = _vnoise(xx * 1.0, (y + f * 4) * 1.0, 3.0, 5)
    h = (15 - y) / 15.0                                       # (0 at the bottom, 1 at the top)
    core = np.clip(1.2 - h * 1.3 - np.abs(xx - 7.5) / 9.0 + (n - 0.5) * 0.7, 0, 1)
    rgb = _ramp(['#0a3a4c', '#1aa8c8', '#6ef0ff', '#e8ffff'], core)
    al = np.clip(core * 3.0, 0, 1)
    al = np.where(al > 0.35, 1.0, 0.0)
    return _out(np, rgb, al)


def kind_of(k, tex):
    """what a follower's texture is to the form: 'glow', 'accent' or 'base' (and whether it's a face, for Wraithfire's eyes)"""
    F = FOL[k]
    n = tex.split('/')[-1]
    if any(n.startswith(g) for g in F['glow']): return 'glow', True
    if any(n.startswith(a) for a in F['accent']): return 'accent', False
    if any(n.startswith(h) for h in F.get('holes', ())): return 'base', 'holes'      # (carved: its dark holes are lit from inside)
    return 'base', ('face' in n or 'eye' in n)


LIGHT = {ETH: {'base': 9, 'accent': 13, 'glow': 15}, WR: {'base': 4, 'accent': 13, 'glow': 15}}


def tex_twin(k, im, tex, el):
    """(3.0g redo) one of a follower's own textures in a form: its design's painter, or a clean recolour to its design's palette
    (elemforms_art / elemforms_designs). The first pass's procedural lattice (ethereal / wraith above) is no longer used."""
    import elemforms_art as EA
    kind, _face = kind_of(k, tex)
    P = EA.palette(k, el, tex.split('/')[-1], kind)
    if callable(P): return P(im)
    P = {a: b for a, b in P.items() if a != 'L'}
    return EA.recolour(im, **P)


def light_twin(k, tex, el):
    """the light an element takes from one of its textures in a form"""
    import elemforms_art as EA
    kind, _face = kind_of(k, tex)
    P = EA.palette(k, el, tex.split('/')[-1], kind)
    if isinstance(P, dict) and 'L' in P: return P['L']
    return EA.light_of(k, el, kind)


# ---------------------------------------------------------------------------------------------------- the twins (rp)
LOOK = re.compile(r'_(?:c|o)\d+(?=_|$)')


def canon(mdir, m):
    """a look's model (a recolour: _c<k> / _o<k>, the same elements) -> its base model, so the form overrides the look's colours"""
    b = LOOK.sub('', m)
    if b == m or not os.path.exists(os.path.join(mdir, b + '.json')): return m
    try:
        e1 = json.load(open(os.path.join(mdir, m + '.json'))).get('elements')
        e2 = json.load(open(os.path.join(mdir, b + '.json'))).get('elements')
    except (OSError, ValueError):
        return m
    return b if e1 is not None and e2 is not None and len(e1) == len(e2) else m


def _bbox(els):
    lo = [min(e['from'][i] for e in els) for i in range(3)]
    hi = [max(e['to'][i] for e in els) for i in range(3)]
    return lo, hi


def spikes(els, n, el, tex):
    """accent parts on top of a model: ETHEREAL crystal spikes (thin, tall, leaning), WRAITHFIRE tongues of soul flame (crossed
    planes) - set along its longer side, on its highest face"""
    if not n or not els: return []
    lo, hi = _bbox(els)
    ax = 2 if (hi[2] - lo[2]) >= (hi[0] - lo[0]) else 0
    out = []
    top = min(hi[1], 30.0)
    for i in range(n):
        f = (i + 0.5) / n
        c = [(lo[0] + hi[0]) / 2, top, (lo[2] + hi[2]) / 2]
        c[ax] = lo[ax] + (hi[ax] - lo[ax]) * (0.15 + 0.7 * f)
        h = min(2.6 + 1.4 * (1 - abs(f - 0.5) * 2), 32 - top)
        if h < 0.6: continue
        lean = (-22.5, 0, 22.5, 0)[i % 4] if el == ETH else 0
        if el == ETH:
            w = 0.7
            out.append({'from': [round(c[0] - w / 2, 3), round(top - 0.4, 3), round(c[2] - w / 2, 3)],
                        'to': [round(c[0] + w / 2, 3), round(top + h, 3), round(c[2] + w / 2, 3)],
                        'rotation': {'origin': [round(c[0], 3), round(top, 3), round(c[2], 3)], 'axis': 'x' if ax == 0 else 'z', 'angle': lean},
                        'faces': {fc: {'uv': [4, 0, 8, 16], 'texture': '#elf_x'} for fc in ('north', 'south', 'east', 'west', 'up')},
                        'light_emission': 15})
        else:
            for rot in (45, -45):
                out.append({'from': [round(c[0] - 1.1, 3), round(top - 0.3, 3), round(c[2], 3)], 'to': [round(c[0] + 1.1, 3), round(top + h + 0.6, 3), round(c[2], 3)],
                            'rotation': {'origin': [round(c[0], 3), round(top, 3), round(c[2], 3)], 'axis': 'y', 'angle': rot},
                            'faces': {fc: {'uv': [0, 0, 16, 16], 'texture': '#elf_x'} for fc in ('north', 'south')}, 'light_emission': 15})
    return out


def room(els):
    """how much smaller a twin must be built to keep every element inside the model box (-16..32 about its middle, 8)"""
    import elemforms_art as EA
    k = 1.0
    for e in els:
        for p in EA._corners(e):
            for v in p:
                if v > 32: k = max(k, (v - 8) / 23.9)
                if v < -16: k = max(k, (8 - v) / 23.9)
    return math.ceil(k * 8) / 8 if k > 1 else 1.0


class Twins:
    """makes the twins of one follower's models in a pack: src (read) and dst (write) roots - the same in the build, a scratch pack
    for a preview"""

    def __init__(self, src, dst, vanilla=None):
        self.src, self.dst, self.vanilla = src, dst, vanilla
        self.mdir = os.path.join(src, 'assets', 'bm', 'models', 'item')
        self.tdone, self.mdone = {}, {}

    def _tex_path(self, tid):
        ns, p = tid.split(':') if ':' in tid else ('minecraft', tid)
        for root in [os.path.join(self.dst, 'assets'), os.path.join(self.src, 'assets')] + ([self.vanilla] if self.vanilla else []):
            f = os.path.join(root, ns, 'textures', p + '.png')
            if os.path.exists(f): return f
        return None

    def _wpng(self, rel, im):
        f = os.path.join(self.dst, 'assets', 'bm', 'textures', rel + '.png')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        im.save(f)
        return f

    def accent_tex(self, el):
        tid = f'bm:block/{SUB}/accent_{el}'
        if tid not in self.tdone:
            if el == ETH:
                self._wpng(f'block/{SUB}/accent_{el}', crystal_tex())
            else:
                f = self._wpng(f'block/{SUB}/accent_{el}', flame_strip())
                json.dump({'animation': {'frametime': 2}}, open(f + '.mcmeta', 'w'))
            self.tdone[tid] = tid
        return tid

    def own_tex(self, k, el, name, painter):
        """a texture the design paints for its new parts (shared ones once: x_*; a design's own per follower)"""
        rel = f'block/{SUB}/{name}' if name.startswith('x_') else f'block/{SUB}/{k}_{name}_{el}'
        tid = 'bm:' + rel
        if tid not in self.tdone:
            self._wpng(rel, painter()); self.tdone[tid] = tid
        return tid

    def tex(self, k, tid, el):
        key = (tid, el)
        if key in self.tdone: return self.tdone[key]
        p = self._tex_path(tid)
        if not p:
            self.tdone[key] = tid; return tid
        from PIL import Image
        ns, path = tid.split(':') if ':' in tid else ('minecraft', tid)
        flat = (path.split('/', 1)[1] if path.startswith('block/') and ns == 'bm' else f'{ns}_{path.replace("/", "_")}')
        im = Image.open(p)
        out = tex_twin(k, im, tid, el)
        f = self._wpng(f'block/{SUB}/{flat}_{el}', out)
        if os.path.exists(p + '.mcmeta'):
            meta = json.load(open(p + '.mcmeta'))
            json.dump(meta, open(f + '.mcmeta', 'w'))
        self.tdone[key] = f'bm:block/{SUB}/{flat}_{el}'
        return self.tdone[key]

    def _resolve(self, m):
        """a model with its parent chain folded in (textures merged; elements and display from the nearest that has them)"""
        mm = json.load(open(os.path.join(self.mdir, m + '.json')))
        par = mm.get('parent', '')
        if par.startswith('bm:item/') and os.path.exists(os.path.join(self.mdir, par[8:] + '.json')):
            base = self._resolve(par[8:])
            out = dict(base); out.update({a: b for a, b in mm.items() if a != 'parent'})
            out['textures'] = dict(base.get('textures', {}), **mm.get('textures', {}))
            if 'parent' in base: out['parent'] = base['parent']
            else: out.pop('parent', None)
            return out
        return mm

    def model(self, k, m, el):
        """bm:item/<m> -> its twin's id (made once)"""
        key = (m, el)
        if key in self.mdone: return self.mdone[key]
        c = canon(self.mdir, m)
        if c != m:
            self.mdone[key] = self.model(k, c, el); return self.mdone[key]
        if not os.path.exists(os.path.join(self.mdir, m + '.json')):
            self.mdone[key] = f'bm:item/{m}'; return self.mdone[key]
        mm = self._resolve(m)
        tex = {a: (self.tex(k, v, el) if not v.startswith('#') else v) for a, v in mm.get('textures', {}).items()}
        out = dict(mm); out['textures'] = tex
        els = mm.get('elements')
        if els is not None:
            import elemforms_art as EA
            src_tex = {a: v for a, v in mm.get('textures', {}).items() if not v.startswith('#')}
            new = []
            for e in els:
                e2 = dict(e)
                ls = [light_twin(k, src_tex.get(f.get('texture', '#')[1:], ''), el) for f in e.get('faces', {}).values()]
                e2['light_emission'] = max([e.get('light_emission', 0)] + ls)
                new.append(e2)
            new, used = EA.build(k, el, m, new, src_tex)          # (the design's: its own pieces dropped, its new parts built on)
            own = EA.own_tex(k, el)
            for u in used:
                tex[u] = self.own_tex(k, el, u, own[u])
            if not new:                                            # (a bone the design leaves bare: one speck, out of sight)
                new = [{'from': [8, 8, 8], 'to': [8.01, 8.01, 8.01], 'faces': {'north': {'uv': [0, 0, 1, 1], 'texture': '#' + next(iter(tex))}}}]
            k_ = room(new)
            if k_ > 1:                                             # (the new parts reach out of the model box: the whole twin built smaller
                new = _RK.shrink(new, k_)                          #  and shown bigger - a display scales about the model's middle)
                d0 = (out.get('display') or {}).get('fixed') or {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}
                out['display'] = dict(out.get('display') or {}, fixed=dict(d0, scale=[round(v * k_, 4) for v in d0.get('scale', [1, 1, 1])]))
            out['elements'] = new
        rel = f'{SUB}/{m}_{el}'
        f = os.path.join(self.dst, 'assets', 'bm', 'models', 'item', rel + '.json')
        os.makedirs(os.path.dirname(f), exist_ok=True)
        json.dump(out, open(f, 'w'), separators=(',', ':'))
        self.mdone[key] = f'bm:item/{rel}'
        return self.mdone[key]

    def tree(self, k, node, el):
        if isinstance(node, dict):
            node = {a: self.tree(k, v, el) for a, v in node.items()}
            if node.get('type') == 'minecraft:model' and str(node.get('model', '')).startswith('bm:item/'):
                node['model'] = self.model(k, node['model'][len('bm:item/'):], el)
            return node
        if isinstance(node, list): return [self.tree(k, v, el) for v in node]
        return node

    def wrap(self, k, d):
        """an item definition -> the float chooses: none, its Ethereal twin, its Wraithfire twin"""
        m = d['model']
        if m.get('type') == 'minecraft:range_dispatch' and m.get('property') == 'minecraft:custom_model_data' and m.get('index') == 0:
            return d                                                  # (already chosen: a second pass changes nothing)
        d = dict(d)
        d['model'] = {'type': 'minecraft:range_dispatch', 'property': 'minecraft:custom_model_data', 'index': 0,
                      'entries': [{'threshold': 0.5, 'model': self.tree(k, m, ETH)}, {'threshold': 1.5, 'model': self.tree(k, m, WR)}],
                      'fallback': m}
        return d


def build_rp(root, log=print, vanilla=None):
    """(the resource pack's last pass) every item definition of the ten chooses by the float; their twins written"""
    idir = os.path.join(root, 'assets', 'bm', 'items')
    names = sorted(f[:-5] for f in os.listdir(idir) if f.endswith('.json'))
    Tw = Twins(root, root, vanilla)
    n_d = 0
    for k, F in FOL.items():
        mine = [n for n in names if n.startswith(F['pre'])]
        assert mine, k
        for n in mine:
            path = os.path.join(idir, n + '.json')
            d = json.load(open(path))
            d2 = Tw.wrap(k, d)
            if d2 is not d:
                json.dump(d2, open(path, 'w'), separators=(',', ':')); n_d += 1
    log(f'elemforms: {n_d} item definitions choose by the float; {len(Tw.mdone)} twin models, {len(Tw.tdone)} twin textures')
    return n_d


def rp(R):
    def post(R2):
        van = '/home/claude/mc263/client/assets'
        build_rp(R2.p(), vanilla=van if os.path.isdir(van) else None)
    R.POST.append(post)


# ==================================================================================================== the datapack
GEM, HEART = 'ethereal_gem', 'wraithfire_heart'
GIVE = {1: (GEM, 'Ethereal Gem', 'ETHEREAL FORM', ETH_C), 2: (HEART, 'Wraithfire Heart', 'WRAITHFIRE FORM', WR_C)}
# the wardrobe rows' codes (phase99.ROWS: inside each one's wardrobe block, free in 3.0f's BUTTON_CODES): (form on / off, give back)
CODES = {'celi': 9855, 'leo': 9935, 'demo': 9955, 'don': 9075, 'lantern': 2775, 'bender': 2815, 'capshun': 2895, 'eraser': 4685,
         'sovereign': 4985, 'keeper': 5285}
# their names and colours (name on the action bar, its colour, their words' colour)
WHO = {'bender': ('Bender', '#e0a860', '#fff0d8'), 'capshun': ('Mr. Capshun', '#f0f0f0', '#d8e4ff'), 'sovereign': ('The Bound Sovereign', '#d0182e', '#ff9a9a'),
       'keeper': ('The Keeper of Bonds', '#ffd6f0', '#fff4e0'), 'lantern': ('The Arachno-Lantern', '#ff8a2a', '#ffd8a0'), 'leo': ('Leo', '#5ab8e0', '#e8f4ff'),
       'celi': ('Celi', '#8ed8ff', '#d8f0ff'), 'demo': ('Democratus', '#7ad06a', '#e0f8d8'), 'eraser': ('The Eraser', '#f08aa0', '#fcdce4'),
       'don': ('Donado', '#e8d29a', '#f4ead0')}
# each in their own voice: take1 / take2 (handed the gem / the heart), on1 / on2 / off (the wardrobe's switch), back (given back),
# again (handed one it wears), none (nothing held)
VOICE = {
    'bender': dict(
        take1='(Bender sniffs the Ethereal Gem, sneezes - and his coat goes to crystal, prisms where his fur was, a row of little diamond spikes down his back. He looks at you. Tail: maximum.)',
        take2='(Bender licks the Wraithfire Heart. Cold blue fire runs down his back to the tip of his tail - he spins after it, delighted, and does not get burnt.)',
        on1='(he shakes himself - and comes up crystal, sparkling)', on2='(blue fire flickers up along his back; he wags it into a little blaze)',
        off='(he shakes the light off like bathwater. Fawn fur again. Still the goodest.)', back='(he drops it in your hand, very gently, and nudges it toward you. Good boy.)',
        again='(he already wears it - and wags at this one too)', none='(he tilts his head. Nothing to give back - an Ethereal Gem or a Wraithfire Heart, maybe?)'),
    'capshun': dict(
        take1='[Mr. Capshun narrates: "And then he was redrawn - in light. Every line of him prism-sharp, glittering at the edges."]',
        take2='[Mr. Capshun narrates: "His ink caught fire. Blue fire. He decided, on balance, that this was fine."]',
        on1='"Ethereal draft, take two."', on2='[Mr. Capshun narrates: "The fire came back. It always comes back in the sequel."]',
        off='"Back to black ink. Classic. Timeless. Cheaper."', back='"Here - you hold the plot device. I\'d only lose it between chapters."',
        again='"Already got one. Two would be a retcon."', none='"No gem, no heart, no glow-up. That\'s just the story so far."'),
    'sovereign': dict(
        take1='"...light. Cold, and clear, and full of colours. I had forgotten that it could be gentle."',
        take2='"Soul fire. It burned the Dread out of me once. Now it burns for you."',
        on1='(its plate turns to crystal, and light runs through the cracks where the Dread was)', on2='(cold blue fire rises off its chains)',
        off='"As I am, then. Bound."', back='"Take it back. I will not hold what is not mine a moment longer than I am asked."',
        again='"I hold it already. I will not take more."', none='"I hold nothing of yours."'),
    'keeper': dict(
        take1='(every thread of the Keeper takes up a colour of its own - a little rainbow loom of light) "Oh. Oh, it\'s beautiful."',
        take2='"A heart of soul fire... I will weave it in carefully. It is warm, for a cold thing."',
        on1='(its threads run prismatic again, one colour each)', on2='(its threads glow cyan, and burn without burning)',
        off='"Back to cream and gold. I like these too."', back='"Here. A thread lent is a thread returned."',
        again='"I am already woven with it."', none='"There is nothing of yours in my weave to give back."'),
    'lantern': dict(
        take1='(it swallows the Ethereal Gem whole. Its rind goes to cut crystal, light pouring out of every carved line)',
        take2='(it gulps the Wraithfire Heart. Its fire goes out - and comes back blue and roaring: soul fire, inside the pumpkin)',
        on1='(its rind crackles into crystal)', on2='(blue fire roars up behind its grin)',
        off='(its fires settle back to orange, purring like a hearth)', back='(it coughs it up into your hand. It is warm, and only a little sticky)',
        again='(it already has one in there. It clacks its legs, pleased)', none='(it hisses a little steam. There\'s nothing of yours in there)'),
    'leo': dict(
        take1='"Look at that - my trident\'s gone to crystal! Light right through it, friend. I feel like a lighthouse."',
        take2='"Soul fire? Cold as the deep, and it doesn\'t burn me. Strange tides. I like it."',
        on1='"Crystal again. Hold steady - I\'m shining."', on2='"Blue fire, back on. Stand close - it keeps the heat off you."',
        off='"Just me, then. Steel and salt."', back='"Here, back to you - safe and sound. A knight keeps what he\'s lent."',
        again='"I\'ve got it already, friend. Keep yours."', none='"I\'m not holding anything of yours - bring me an Ethereal Gem, or a Wraithfire Heart."'),
    'celi': dict(
        take1='"Tch. Fine. ...Okay, this is actually really pretty. Don\'t look at me like that."',
        take2='"Cold fire? Cold fire. Oh, I am going to have so much fun with this."',
        on1='"Ice and starlight. Try and keep up."', on2='"Blue fire on. Don\'t touch."',
        off='"Plain old me. Still faster than you."', back='"Here. Take it before I lose it in a snowbank."',
        again='"I\'ve GOT one. Hands off."', none='"You haven\'t given me anything. Gem or heart - pick one."'),
    'demo': dict(
        take1='"Hmph. The storm, turned to glass. ...It suits me."', take2='"Soul fire on the blade. The dead will see me coming. Good."',
        on1='"Glass and lightning. Onward."', on2='"The scythe burns. Onward."',
        off='"Enough show. The storm will do."', back='"Take it. I owe no one."',
        again='"I hold it already. Do not waste it."', none='"I carry nothing of yours."'),
    'eraser': dict(
        take1='"Oh! Oh no - I\'m all sparkly. S-sorry! Can I keep it? I\'ll be careful. I\'ll only erase BAD things."',
        take2='"It\'s cold! It\'s cold fire! S-sorry - I\'m going to rub out every fire near you, okay? Just to be safe. Sorry, fire."',
        on1='"Sparkly again! S-sorry."', on2='"No more fire, okay? Sorry, fire."',
        off='"Just pink again. Sorry. Pink is fine."', back='"H-here, it\'s yours! I didn\'t smudge it. Much."',
        again='"I already have it! S-sorry - I\'ll give it back if you want."', none='"I don\'t have anything of yours! I checked. Twice. Sorry."'),
    'don': dict(
        take1='*astonished bark* (Donado chomps the Ethereal Gem. His coat lights up in every colour - the mothership\'s tractor beam, only prismatic, and he\'s the one working it now.)',
        take2='*AWOOO* (Donado swallows the Wraithfire Heart. Blue fire bursts out of his coat. He gets the zoomies immediately.)',
        on1='*happy bark* (Donado glitters all over)', on2='*excited barking* (blue fire - zoomies imminent)',
        off='*sneeze* (just a scrappy cream dog again. Specimen 042, off duty.)', back='*drops it at your feet, tail going* (it\'s only a little slobbery)',
        again='*wag* (Donado already has one)', none='*head tilt* (Donado has nothing of yours to give back)'),
}
ERASE_SAY = ['"S-sorry! It\'s... gone. Completely. Oops."', '"Clean slate! S-sorry."', '"I only erase BAD things. That was a bad thing."',
             '"Oops. I mean - you\'re welcome?"']
UNFIRE_SAY = '(it scrubs the fire right out of the world round you) "S-sorry, fire!"'
BEAM_SAY = '*proud bark* (Donado beams a monster up into the sky. Then lets go.)'
ZOOM_SAY = '*ZOOMIES* (Donado tears round you in a ring of soul fire, barking his head off)'
# (no boss, nor anything that isn't a monster, for the jokes' beam, erasing and zoomies)
VAN_BOSS = ('minecraft:wither', 'minecraft:ender_dragon', 'minecraft:warden', 'minecraft:elder_guardian')
RIGPET = ('bender', 'capshun', 'sovereign', 'keeper', 'lantern', 'eraser')
WAYS = ('Ethereal and Wraithfire', 'right-click {p} with an Ethereal Gem or a Wraithfire Heart: {t} keeps it (one at a time) and takes its form - ETHEREAL '
        '(crystal and prismatic light: every blow +2, and a prismatic flash) or WRAITHFIRE (soul fire: every blow sets the foe alight, and beside {p}, '
        'fire can\'t touch you). {P} wardrobe turns it on or off, and gives it back{x}')
WAYS_X = {'eraser': '. ETHEREAL also rubs weak monsters (12 health or less) right out of existence now and then; WRAITHFIRE rubs out the fire (and the lava) round you',
          'don': '. ETHEREAL Donado beams the nearest monster up in a tractor beam every 5 s; WRAITHFIRE, he does soul-fire zoomies round you every 8 s'}


def setup():
    """(at import, from gen_dp - before any generate) the wardrobe rows (phase99.ROWS), the gem's and the heart's lore, the rigpet
    followers' ways"""
    import phase99 as P99
    for k in FOL:
        c, o = CODES[k], obj(k)
        sc = lambda n: f'score @s {o} matches {n}'
        P99.ROWS.setdefault(k, []).append(
            (c, 'efm', 'Ethereal / Wraithfire', ETH_C,
             f'{WHO[k][0]}\'s form: on or off. Right-click {_pron(k)} holding an Ethereal Gem or a Wraithfire Heart to hand it over - kept, one at a time.',
             [(None, 'nothing held', 'dark_gray'), (sc(1), 'Ethereal: off', 'gray'), (sc(2), 'Wraithfire: off', 'gray'),
              (sc(11), 'Ethereal: on', ETH_C), (sc(12), 'Wraithfire: on', WR_C)], f'elf/{k}/toggle'))
        P99.ROWS[k].append(
            (c + 1, 'efg', 'Give back the gem / heart', WR_C, f'{WHO[k][0]} hands back the Ethereal Gem or the Wraithfire Heart - and is {_pron(k)}self again.',
             [(None, 'nothing held', 'dark_gray'), (sc(1), 'the Ethereal Gem', ETH_C), (sc(11), 'the Ethereal Gem', ETH_C),
              (sc(2), 'the Wraithfire Heart', WR_C), (sc(12), 'the Wraithfire Heart', WR_C)], f'elf/{k}/take'))
    for iid, col in ((GEM, ETH_C), (HEART, WR_C)):
        if iid in ITEMS:
            ITEMS[iid]['comps']['minecraft:lore'].insert(-1, T('Bender, Mr. Capshun, Leo, Celi, Democratus and five more: right-click one to give it its form.', col))
    import phase195, phase198, phase239, phase254, phase194, phase235
    cfg = {'bender': phase195.C, 'capshun': phase198.C, 'sovereign': phase239.Sovereign, 'keeper': phase254.Keeper, 'lantern': phase194.C, 'eraser': phase235.Eraser}
    for k, C in cfg.items():
        assert C.W == k, (k, C.W)
        p, t = ('it', 'it') if C.pron == 'it' else (C.pron, C.they)
        P = {'her': 'Her', 'him': 'His', 'it': 'Its'}[C.pron]
        C.POWERS = list(C.POWERS) + [(WAYS[0], WAYS[1].format(p=p, t=t, P=P, x=WAYS_X.get(k, '')))]


POSS = {'her': 'her', 'him': 'his', 'it': 'its'}
THEY = {'her': 'she', 'him': 'he', 'it': 'it'}


def _pron(k):
    return {'celi': 'her', 'eraser': 'it', 'lantern': 'it', 'keeper': 'it', 'sovereign': 'it'}.get(k, 'him')


def generate(G):
    """(late: every follower built, before the attack kit's pass) -> how many blow lines answer to a form"""
    fn, title, tellraw = G.fn, G.title, G.tellraw
    objs = [obj(k) for k in FOL] + ['bm.efcd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    F = 'item.components."minecraft:custom_model_data".floats'
    # ---- shared: a part dressed for the form #efv (0 none, 1 Ethereal, 2 Wraithfire); the forms' bursts; a blow's touch
    fn('elf/paint', [f'execute if score #efv bm.rng matches 0 run return run data remove entity @s {F}',
                     f'execute if score #efv bm.rng matches 1 run return run data modify entity @s {F} set value [1.0f]',
                     f'data modify entity @s {F} set value [2.0f]'])
    fn('elf/fx0', ['particle minecraft:poof ~ ~1 ~ 0.4 0.6 0.4 0.02 16', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('elf/fx1', ['particle minecraft:end_rod ~ ~1.1 ~ 0.5 0.8 0.5 0.08 40', 'particle minecraft:dust{color:[1.0,0.45,0.7],scale:1.3} ~ ~1.1 ~ 0.6 0.8 0.6 0 14',
                   'particle minecraft:dust{color:[0.4,0.8,1.0],scale:1.3} ~ ~1.1 ~ 0.6 0.8 0.6 0 14', 'particle minecraft:dust{color:[1.0,0.92,0.4],scale:1.3} ~ ~1.1 ~ 0.6 0.8 0.6 0 14',
                   'particle minecraft:flash{color:[0.85,0.95,1.0,1.0]} ~ ~1.1 ~ 0 0 0 0 1',
                   'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.4', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.7 1.6'])
    fn('elf/fx2', ['particle minecraft:soul_fire_flame ~ ~1.1 ~ 0.4 0.8 0.4 0.06 50', 'particle minecraft:soul ~ ~1.3 ~ 0.3 0.6 0.3 0.03 12',
                   'particle minecraft:flash{color:[0.43,0.94,1.0,1.0]} ~ ~1.1 ~ 0 0 0 0 1', 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 2 1.2',
                   'playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..16] ~ ~ ~ 0.7 1.0'])
    fn('elf/hit1', ['particle minecraft:flash{color:[0.85,0.95,1.0,1.0]} ~ ~0.9 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~1 ~ 0.25 0.4 0.25 0.1 8',
                    'particle minecraft:dust{color:[1.0,0.45,0.7],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 5', 'particle minecraft:dust{color:[0.4,0.8,1.0],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 5',
                    'particle minecraft:dust{color:[1.0,0.92,0.4],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 5', 'playsound minecraft:block.amethyst_block.hit neutral @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    fn('elf/hit2', ['data modify entity @s Fire set value 100s', 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.3 0.5 0.3 0.03 14',
                    'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 1 1.4'])
    fn('elf/unsit', ['execute store success score #s0 bm.rng if data entity @s {Sitting:1b}',
                     'execute if score #s0 bm.rng matches 1 run data modify entity @s Sitting set value 0b',
                     'execute if score #s0 bm.rng matches 0 run data modify entity @s Sitting set value 1b'])
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,tag=!bm.boss,tag=!bm.vboss,tag=!bm.gvboss'
    import phase67 as P67
    foe += ''.join(f',tag=!{t}' for t, _b in P67.BOSSES) + ''.join(f',type=!{t}' for t in VAN_BOSS)
    n_hit = 0
    for k in FOL:
        _one(G, k, holds, F, foe)
    n_hit = hits(G)
    _jokes(G, foe)
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/elemforms', 'yellow'),
                                                T('  an Ethereal Gem and a Wraithfire Heart, to hand ten followers (elemforms)', 'gray')]))
    fn('admin/elemforms', [G.give(GEM), G.give(HEART)])
    return n_hit


def _host(k):
    t = FOL[k]['host']
    return f'@e[type=minecraft:wolf,tag={t}]'


def _one(G, k, holds, F, foe):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    D, o = FOL[k], obj(k)
    nm, col, line = WHO[k]
    V = VOICE[k]
    say = lambda txt: title('@s', 'actionbar', [T(f'{nm}: ', col, bold=True), T(txt, line)])
    mine = 'if score @s bm.pid = #me bm.pid'
    pet = f'execute as {_host(k)} {mine} at @s run function'
    p = f'elf/{k}'
    # ---- (as the player) #efv: the form shown (0 none, 1 / 2)
    fn(f'{p}/f', ['scoreboard players set #efv bm.rng 0', f'execute if score @s {o} matches 11 run scoreboard players set #efv bm.rng 1',
                  f'execute if score @s {o} matches 12 run scoreboard players set #efv bm.rng 2'])
    # ---- (as the host, at it; #me its pid) its parts tagged bm.efsel
    kind, tag, excl = D['parts']
    if kind == 'rig':
        ex = ''.join(f',tag=!{e}' for e in excl)
        parts = [f'execute as @e[type=minecraft:item_display,tag={tag}{ex},distance=..10] {mine} run tag @s add bm.efsel']
    else:
        parts = [f'execute on passengers if entity @s[type=minecraft:item_display,tag={tag}] run tag @s add bm.efsel']
    fn(f'{p}/parts', parts)
    # ---- KEEP: every tick while a form shows - a part summoned plain (a new rig, a call, a faint's return) dressed at once
    G.FUNCS['tick'].append(f'execute as @a[scores={{{o}=11..12}}] run function bm:{p}/keep')
    fn(f'{p}/keep', ['scoreboard players operation #me bm.pid = @s bm.pid', f'function bm:{p}/f', f'{pet} bm:{p}/keep2'])
    fn(f'{p}/keep2', ['tag @s add bm.efh', f'function bm:{p}/parts',
                      f'execute as @e[type=minecraft:item_display,tag=bm.efsel] unless data entity @s {F}[0] run function bm:elf/paint',
                      'tag @e[type=minecraft:item_display,tag=bm.efsel] remove bm.efsel'])
    # ---- REPAINT: the form changed (as the player) - every part now, and its burst
    fn(f'{p}/repaint', ['scoreboard players operation #me bm.pid = @s bm.pid', f'function bm:{p}/f', f'{pet} bm:{p}/repaint2'])
    fn(f'{p}/repaint2', ['tag @s remove bm.efh', 'execute unless score #efv bm.rng matches 0 run tag @s add bm.efh', f'function bm:{p}/parts',
                         'execute as @e[type=minecraft:item_display,tag=bm.efsel] run function bm:elf/paint',
                         'tag @e[type=minecraft:item_display,tag=bm.efsel] remove bm.efsel',
                         'execute if score #efv bm.rng matches 0 run function bm:elf/fx0', 'execute if score #efv bm.rng matches 1 run function bm:elf/fx1',
                         'execute if score #efv bm.rng matches 2 run function bm:elf/fx2'])
    # ---- GIVEN the gem (1) or the heart (2), as the player: kept (one at a time - the other comes back), the form on
    for n, (iid, inm, form, c) in GIVE.items():
        m = 3 - n
        oiid, oinm = GIVE[m][0], GIVE[m][1]
        fn(f'{p}/give{n}', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute if score @s {o} matches {n + 10} run return run ' + say(V['again']),
                            f'execute if score @s {o} matches {n} run return run function bm:{p}/show{n}',
                            f'execute if score @s {o} matches {m} run loot give @s loot bm:items/{oiid}',
                            f'execute if score @s {o} matches {m + 10} run loot give @s loot bm:items/{oiid}',
                            f'execute if score @s {o} matches {m} run ' + tellraw('@s', [T(f'{nm} gives you back the {oinm}.', 'gray')]),
                            f'execute if score @s {o} matches {m + 10} run ' + tellraw('@s', [T(f'{nm} gives you back the {oinm}.', 'gray')]),
                            'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand bm:p2/consume_one',
                            f'scoreboard players set @s {o} {n + 10}',
                            tellraw('@s', G.PREFIX + [T(f'{nm} keeps the {inm}: ', 'gray'), T(form, c, bold=True),
                                                      T(f' ({POSS[_pron(k)]} wardrobe - sneak + use {ITEMS[D["item"]]["name"]} - turns it on or off, and gives it back).', 'dark_gray')]),
                            say(V[f'take{n}']), f'function bm:{p}/repaint'])
        fn(f'{p}/show{n}', [f'scoreboard players set @s {o} {n + 10}', say(V[f'on{n}']), f'function bm:{p}/repaint'])
    # ---- THE WARDROBE (phase99.ROWS; as the player, #me set): the form on / off; given back
    w99 = f'function bm:p99/menu/{k}'
    fn(f'{p}/toggle', [f'execute unless score @s {o} matches 1.. run return run function bm:{p}/none',
                       f'execute store success score #f0 bm.rng if score @s {o} matches 10..',
                       f'execute if score #f0 bm.rng matches 1 run scoreboard players remove @s {o} 10',
                       f'execute if score #f0 bm.rng matches 0 run scoreboard players add @s {o} 10',
                       f'execute if score @s {o} matches 1..2 run ' + say(V['off']), f'execute if score @s {o} matches 11 run ' + say(V['on1']),
                       f'execute if score @s {o} matches 12 run ' + say(V['on2']), f'function bm:{p}/repaint', w99])
    fn(f'{p}/take', [f'execute unless score @s {o} matches 1.. run return run function bm:{p}/none',
                     f'execute if score @s {o} matches 1 run loot give @s loot bm:items/{GEM}', f'execute if score @s {o} matches 11 run loot give @s loot bm:items/{GEM}',
                     f'execute if score @s {o} matches 2 run loot give @s loot bm:items/{HEART}', f'execute if score @s {o} matches 12 run loot give @s loot bm:items/{HEART}',
                     f'scoreboard players set @s {o} 0', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 0.9', say(V['back']),
                     f'function bm:{p}/repaint', w99])
    fn(f'{p}/none', [say(V['none']), w99])
    # ---- THE CLICK: right-click it holding one
    give = [f'execute if items entity @s weapon.mainhand {holds(GEM)} run return run function bm:{p}/give1',
            f'execute if items entity @s weapon.mainhand {holds(HEART)} run return run function bm:{p}/give2']
    who = D['who']
    if who == 'adv':                  # (Celi: no click box - the dog under her; the click sat her down or stood her up: undone)
        G.wjson(f'bm/advancement/elf/{k}_click.json', {'criteria': {'i': {'trigger': 'minecraft:player_interacted_with_entity', 'conditions': {
            'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                        'predicate': {'minecraft:entity_type': 'minecraft:wolf', 'minecraft:nbt': '{Tags:["%s"]}' % D['host']}}]}}},
            'rewards': {'function': f'bm:{p}/click'}})
        fn(f'{p}/click', [f'advancement revoke @s only bm:elf/{k}_click',
                          f'execute unless items entity @s weapon.mainhand {holds(GEM)} unless items entity @s weapon.mainhand {holds(HEART)} run return 0',
                          f'function bm:{p}/click2'])
    elif who == 'p25/don/interact':   # (Donado: the frog pipeline's click - a gem isn't gear; the click's sit undone)
        L = G.FUNCS[who]
        assert L[0] == 'advancement revoke @s only bm:donado_interact', L[0]
        L[1:1] = [f'execute if items entity @s weapon.mainhand {holds(GEM)} run return run function bm:{p}/click2',
                  f'execute if items entity @s weapon.mainhand {holds(HEART)} run return run function bm:{p}/click2']
    else:                             # (a click box: its who, as you - after "not yours")
        L = G.FUNCS[who]
        j = next(i for i, l in enumerate(L) if 'bm.pid = #me bm.pid run return run' in l)
        L[j + 1:j + 1] = give
    if who in ('adv', 'p25/don/interact'):
        fn(f'{p}/click2', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #had bm.rng 0',
                           f'execute as {_host(k)} {mine} if entity @s[distance=..8] run scoreboard players set #had bm.rng 1',
                           'execute if score #had bm.rng matches 0 run return run ' + title('@s', 'actionbar', T(f'{nm} only takes it from the one {THEY[_pron(k)]} walks with.', 'gray')),
                           f'execute as {_host(k)} {mine} if entity @s[distance=..8] run function bm:elf/unsit'] + give)
    # ---- each second while a form shows (as the player): the aura; Wraithfire - fire can't touch you beside it
    import phase138 as P138
    h = P138.AURA[k][2]
    G.FUNCS['loop/second'].append(f'execute as @a[scores={{{o}=11..12}}] run function bm:{p}/sec')
    fn(f'{p}/sec', ['scoreboard players operation #me bm.pid = @s bm.pid', f'function bm:{p}/f', f'{pet} bm:{p}/sec2'])
    fn(f'{p}/sec2', [f'execute if score #efv bm.rng matches 1 run particle minecraft:end_rod ~ ~{h * 0.75:.2f} ~ 0.35 0.5 0.35 0.01 2',
                     f'execute if score #efv bm.rng matches 1 run particle minecraft:dust{{color:[0.7,0.92,1.0],scale:0.8}} ~ ~{h * 0.75:.2f} ~ 0.4 0.5 0.4 0 2',
                     f'execute if score #efv bm.rng matches 1 run particle minecraft:dust{{color:[1.0,0.6,0.85],scale:0.7}} ~ ~{h * 0.75:.2f} ~ 0.4 0.5 0.4 0 1',
                     f'execute if score #efv bm.rng matches 2 run particle minecraft:soul_fire_flame ~ ~{h * 0.75:.2f} ~ 0.3 0.5 0.3 0.01 2',
                     f'execute if score #efv bm.rng matches 2 run particle minecraft:soul ~ ~{h * 0.9:.2f} ~ 0.3 0.4 0.3 0.01 1',
                     'execute if score #efv bm.rng matches 2 on owner if entity @s[distance=..16] run effect give @s minecraft:fire_resistance 3 0 true'] +
       ([f'function bm:elf/{k}/joke'] if k in JOKE else []))
    # ---- (as a struck foe, the blow's *me host tagged) #efx: that host's owner's form
    if D['me']:
        fn(f'elf/q/{k}', ['scoreboard players set #efx bm.rng 0',
                          f'execute as @e[type=minecraft:wolf,tag={D["me"]},limit=1] on owner if score @s {o} matches 11 run scoreboard players set #efx bm.rng 1',
                          f'execute as @e[type=minecraft:wolf,tag={D["me"]},limit=1] on owner if score @s {o} matches 12 run scoreboard players set #efx bm.rng 2'])
    fn(f'elf/hit/{k}', ['execute if score #efx bm.rng matches 1 at @s run function bm:elf/hit1', 'execute if score #efx bm.rng matches 2 at @s run function bm:elf/hit2'] +
       (['execute if score #efx bm.rng matches 1 at @s run function bm:elf/eraser/hit_erase'] if k == 'eraser' else []))


# (each blow of theirs: the damage line, as the struck foe; its *me host in the selector)
DMG = re.compile(r'^(?P<pre>execute .* run )?damage @s (?P<amt>\d+(?:\.\d+)?) (?P<typ>[a-z_:]+) by (?P<sel>@e\[[^\]]*\])$')


def hits(G):
    """every blow of the ten's (a `damage @s N <type> by <its *me host>` line, outside elf/): #efx asked of the blow's host's owner
    first; Ethereal - the blow 2 harder; then the form's touch on the foe (elf/hit/<k>). rigpet's hurt (its macro blow, #pd) the
    same. -> lines"""
    ME = {D['me']: k for k, D in FOL.items() if D['me']}
    n, per = 0, {}
    for name in list(G.FUNCS):
        if name.startswith('elf/'): continue
        L = G.FUNCS[name]
        out, hit = [], False
        for l in L:
            m = DMG.match(l)
            k = None
            if m and 'vindicator' not in m['sel']:
                k = next((ME[t] for t in re.findall(r'tag=(bm\.[a-z0-9]+)', m['sel']) if t in ME), None)
            if not k:
                out.append(l); continue
            pre = m['pre'] or ''
            when = lambda c: f'execute {c} {pre[len("execute "):]}' if pre else f'execute {c} run '
            amt = float(m['amt'])
            out += [f'function bm:elf/q/{k}', when('if score #efx bm.rng matches 1') + f'damage @s {amt + 2:g} {m["typ"]} by {m["sel"]}',
                    when('unless score #efx bm.rng matches 1') + l[len(pre):], when('if score #efx bm.rng matches 1..') + f'function bm:elf/hit/{k}']
            hit = True; n += 1; per[k] = per.get(k, 0) + 1
        if hit: G.FUNCS[name] = out
    for k, D in FOL.items():
        if not D['hurt']: continue
        H = G.FUNCS[D['hurt']]
        assert H[0].startswith('execute store result storage bm:tmp') and 'scoreboard players get #pd bm.rng' in H[0], (k, H[0])
        per[k] = per.get(k, 0) + 1
        G.FUNCS[D['hurt']] = [f'function bm:elf/q/{k}', 'execute if score #efx bm.rng matches 1 run scoreboard players add #pd bm.rng 2'] + H + \
                             ['execute if score #efx bm.rng matches 1 run scoreboard players remove #pd bm.rng 2', f'execute if score #efx bm.rng matches 1.. run function bm:elf/hit/{k}']
        n += 1
    assert all(per.get(k) for k, D in FOL.items() if D['me']), ('no blow of theirs found', [k for k, D in FOL.items() if D['me'] and not per.get(k)])
    # (Donado bites with the dog under him - no blow line: a monster just hurt near him, by him, in a form)
    G.FUNCS['tick'].append('execute as @e[type=minecraft:wolf,tag=bm.donado,tag=bm.efh] at @s as @e[type=#bm:hostile,distance=..4] if data entity @s {HurtTime:9s} '
                           'run function bm:elf/don/bit')
    G.fn('elf/don/bit', ['scoreboard players set #efx bm.rng 0', 'execute on attacker if entity @s[type=minecraft:wolf,tag=bm.donado,tag=bm.efh] on owner run function bm:elf/don/q2',
                         'execute if score #efx bm.rng matches 1.. run function bm:elf/hit/don'])
    G.fn('elf/don/q2', [f'execute if score @s {obj("don")} matches 11 run scoreboard players set #efx bm.rng 1',
                        f'execute if score @s {obj("don")} matches 12 run scoreboard players set #efx bm.rng 2'])
    return n


def _jokes(G, foe):
    """the Eraser's and Donado's OP forms (sec2 -> elf/<k>/joke, as the host, at it; #efv the form; its cooldown bm.efcd)"""
    fn, title = G.fn, G.title
    esay = lambda txt: title('@s', 'actionbar', [T('The Eraser: ', WHO['eraser'][1], bold=True), T(txt, WHO['eraser'][2])])
    dsay = lambda txt: title('@s', 'actionbar', [T('Donado: ', WHO['don'][1], bold=True), T(txt, WHO['don'][2])])
    cd = ['execute if score @s bm.efcd matches 1.. run scoreboard players remove @s bm.efcd 1']
    # ---- THE ERASER. Ethereal: CLEAN SLATE - a weak monster (12 health left or less, 60 at most, no boss) rubbed out of existence:
    #      every ~5 s the nearest such within 10, and a third of its blows' foes. Wraithfire: NO MORE FIRE - the fire round you
    #      rubbed out every second (and the lava, in the Overworld, the Nether and the End; never in a heist), fireproof.
    fn('elf/eraser/joke', cd + ['tag @s add bm.efby',
                                'execute if score #efv bm.rng matches 1 unless score @s bm.efcd matches 1.. run function bm:elf/eraser/hunt',
                                'execute if score #efv bm.rng matches 2 on owner if entity @s[distance=..16] at @s run function bm:elf/eraser/unfire',
                                'tag @s remove bm.efby'])
    # (the nearest weak one only: the first found ends the hunt)
    fn('elf/eraser/hunt', [f'execute as @e[{foe},distance=..10,sort=nearest] if function bm:elf/eraser/can at @s run return run function bm:elf/eraser/seek'])
    fn('elf/eraser/seek', ['scoreboard players set @e[type=minecraft:wolf,tag=bm.efby,limit=1] bm.efcd 5', 'function bm:elf/eraser/erase'])
    fn('elf/eraser/can', [f'execute unless entity @s[{foe}] run return 0', 'execute store result score #mh bm.rng run attribute @s minecraft:max_health get',
                          'execute if score #mh bm.rng matches 61.. run return 0', 'execute store result score #hp bm.rng run data get entity @s Health',
                          'execute if score #hp bm.rng matches 13.. run return 0', 'execute if score #hp bm.rng matches ..0 run return 0', 'return 1'])
    fn('elf/eraser/hit_erase', ['execute store result score #r bm.rng run random value 1..3', 'execute unless score #r bm.rng matches 1 run return 0',
                                'execute unless function bm:elf/eraser/can run return 0',
                                'tag @e[type=minecraft:wolf,tag=bm.ezme,limit=1] add bm.efby', 'function bm:elf/eraser/erase',
                                'tag @e[type=minecraft:wolf,tag=bm.efby] remove bm.efby'])
    fn('elf/eraser/erase', ['particle minecraft:poof ~ ~0.8 ~ 0.3 0.5 0.3 0.04 24', 'particle minecraft:dust{color:[1.0,0.62,0.7],scale:1.4} ~ ~0.8 ~ 0.4 0.6 0.4 0 20',
                            'particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.5 0.3 0.1 16', 'particle minecraft:flash{color:[1.0,0.9,0.95,1.0]} ~ ~0.8 ~ 0 0 0 0 1',
                            'playsound minecraft:item.brush.brushing.generic neutral @a[distance=..16] ~ ~ ~ 1 1.6', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.8',
                            'damage @s 1000 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.efby,limit=1]',
                            'execute store result score #r bm.rng run random value 1..%d' % len(ERASE_SAY)] +
       [f'execute if score #r bm.rng matches {i + 1} as @e[type=minecraft:wolf,tag=bm.efby,limit=1] on owner if entity @s[tag=!bm.hush] run ' + esay(t) for i, t in enumerate(ERASE_SAY)])
    fn('elf/eraser/unfire', ['execute store result score #n bm.rng run fill ~-5 ~-2 ~-5 ~5 ~3 ~5 minecraft:air replace #minecraft:fire',
                             'execute unless entity @s[tag=bm.gvp] if dimension minecraft:overworld run function bm:elf/eraser/unlava',
                             'execute unless entity @s[tag=bm.gvp] if dimension minecraft:the_nether run function bm:elf/eraser/unlava',
                             'execute unless entity @s[tag=bm.gvp] if dimension minecraft:the_end run function bm:elf/eraser/unlava',
                             'effect give @s minecraft:fire_resistance 3 0 true',
                             'execute if score #n bm.rng matches 1.. run particle minecraft:poof ~ ~0.5 ~ 2 0.6 2 0.02 30',
                             'execute if score #n bm.rng matches 1.. run playsound minecraft:item.brush.brushing.generic neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                             'execute if score #n bm.rng matches 1.. if entity @s[tag=!bm.hush] run ' + esay(UNFIRE_SAY)])
    fn('elf/eraser/unlava', ['execute store result score #l bm.rng run fill ~-3 ~-2 ~-3 ~3 ~1 ~3 minecraft:air replace minecraft:lava',
                             'scoreboard players operation #n bm.rng += #l bm.rng'])
    # ---- DONADO. Ethereal: TRACTOR BEAM - every 5 s the nearest monster within 10 (no boss) beamed up, and let go. Wraithfire: SOUL
    #      ZOOMIES - every 8 s, monsters within 7 of you: a ring of soul fire round you - every one within 6 burns, takes 5, thrown back;
    #      you get the zoomies too.
    fn('elf/don/joke', cd + ['tag @s add bm.efby',
                             f'execute if score #efv bm.rng matches 1 unless score @s bm.efcd matches 1.. as @e[{foe},distance=..10,sort=nearest,limit=1] at @s run function bm:elf/don/beam',
                             f'execute if score #efv bm.rng matches 2 unless score @s bm.efcd matches 1.. on owner if entity @s[distance=..16] at @s if entity @e[{foe},distance=..7] run function bm:elf/don/zoom',
                             'tag @s remove bm.efby'])
    fn('elf/don/beam', ['scoreboard players set @e[type=minecraft:wolf,tag=bm.efby,limit=1] bm.efcd 5', 'effect give @s minecraft:levitation 2 9 true',
                        'damage @s 4 minecraft:magic by @e[type=minecraft:wolf,tag=bm.efby,limit=1]',
                        'particle minecraft:end_rod ~ ~3 ~ 0.15 3 0.15 0 60', 'particle minecraft:dust{color:[1.0,0.45,0.7],scale:1.4} ~ ~3 ~ 0.25 3 0.25 0 20',
                        'particle minecraft:dust{color:[0.4,1.0,0.6],scale:1.4} ~ ~3 ~ 0.25 3 0.25 0 20', 'particle minecraft:dust{color:[0.4,0.7,1.0],scale:1.4} ~ ~3 ~ 0.25 3 0.25 0 20',
                        'playsound minecraft:block.beacon.activate neutral @a[distance=..24] ~ ~ ~ 0.8 1.8', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                        'execute as @e[type=minecraft:wolf,tag=bm.efby,limit=1] on owner if entity @s[tag=!bm.hush] run ' + dsay(BEAM_SAY)])
    ring = [f'particle minecraft:soul_fire_flame ~{2.2 * math.cos(a * math.pi / 8):.2f} ~0.2 ~{2.2 * math.sin(a * math.pi / 8):.2f} 0.05 0.1 0.05 0.02 3' for a in range(16)]
    fn('elf/don/zoom', ['scoreboard players set @e[type=minecraft:wolf,tag=bm.efby,limit=1] bm.efcd 8', 'tag @s add bm.efzme',
                        f'execute as @e[{foe},distance=..6] at @s run function bm:elf/don/zoomed', 'tag @s remove bm.efzme',
                        'effect give @s minecraft:speed 6 1 true', 'effect give @s minecraft:fire_resistance 8 0 true'] + ring +
       ['playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.6', 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 2 0.9',
        'execute if entity @s[tag=!bm.hush] run ' + dsay(ZOOM_SAY)])
    fn('elf/don/zoomed', ['data modify entity @s Fire set value 160s', 'damage @s 5 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.efby,limit=1]',
                          'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.3 0.5 0.3 0.04 14',
                          'execute facing entity @a[tag=bm.efzme,limit=1] feet positioned ^ ^0.2 ^-2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
