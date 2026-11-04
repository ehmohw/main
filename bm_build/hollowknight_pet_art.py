"""(3.1 draft, stage 1: art only - not wired) THE HOLLOW STATUE KNIGHT - two in one: an Undercrown Statue Knight's armour (knight_art,
'dread') with a SOUL SERPENT coiled inside it. (2nd pass: the owner changed the ghost to a soul serpent; polished to the bar.)

LORE (kept to phase169's Omega's Book and phase163's Pistachio): the soul is SIR ALDOUS VANE, Captain of King Omega's palace guard
on Omega Island, who held the great stair beside his king in the War of Brothers and fell there. Apophiss "went away to make other
kings - hollow ones": he took the fallen guards' souls and bound them into the Dread's statue armour in the Undercrown - and, as
his mark on them, bound them IN SERPENT FORM, his own shape, so they would never again stand as men. Sir Aldous has been a soul
serpent coiled in a hollow suit of armour for three hundred years. He isn't a serpent at heart: his eyes are still a kind man's
(warm gold, gently lidded - nothing like the Apophiss line's glare), his crest a small soul-flame like a candle in a window.
Before the war Pistachio was Sir Aldous's dog - "Pip", a pup at his heel on the guard's rounds - until the Captain gave him to the
King's household the night he rode to the stair: "Mind the door, Pip." Pistachio has minded it for three hundred years.

UNLOCK  Place a knight statue you've earned (knight_statue_dread), then call Pistachio and King Omega beside it (two of your
        three). Pistachio sniffs the plinth - and BARKS (his first bark in the pack: he's a butler); Omega: "...Aldous? Is that
        you in there?" Two kind gold eyes open in the eye-slit; a soul serpent's head slides out of the visor, looks at the dog a
        long moment, and lays its chin on Pistachio's head. The armour kneels.

TWO IN ONE (two rigs, one follower)
  ARMOUR   knight_art's rig and geometry at companion size (0.5: ~1.5 blocks), with this follower's finishes (FINISHES) and the
           SERPENT SHOWING THROUGH IT: its two kind gold eyes in the eye-slit (the Dread's red squares are gone), a coil of
           translucent soul glimpsed in the gorget and in the gap at the waist, its tail-tip curling out under the cape's hem.
           Finishes: 'hollow' (the default: black plate and bone, soul-blue light, the cloak re-dyed Omega's palace violet with a
           gold hem), 'freed' (the holy cosmetic: polished silver, gold for bone, a white cloak, warm gold light - the serpent in
           it pale gold), 'shiny' (Starlit: deep blue plate, silver trim; a starry indigo serpent).
           It swings the giant mace: knight_art's own poses, plus the kneel (sit_a, the vigil), the statue stance (sit_b) and the
           heap (BROKEN: helm knocked off, the mace dropped).
  SERPENT  the soul itself (SERPENT, 'hs_'): SLIM AND WISPY - its own design, not an Apophiss recolour: a small rounded head (a
           short snout, a soft smile line), big kind gold eyes with lids, a faint blush; a little SOUL-FLAME CREST on its crown;
           ghostly frill-wisps trailing from its cheeks; a slender translucent body of soul-blue scales with a bright glowing CORE
           down its length (seen through the scales), a pale banded belly, small wisp-fins along its back; its tail thins and
           DISSOLVES into motes. Its body is a set of shapes, one shown per pose (_show): 's' (reared), 'lunge' (a strike),
           'coil' (wound round a foe - 1.5 turns, radius ~1/3 block), 'drape' (over the kneeling armour's shoulders), 'helm'
           (curled round the helm: the doll), 'dive' (streamlined, back in through the visor), 'peek' (half out of the visor).
  BROKEN   beaten down, the armour falls apart ('heap') and the serpent fights alone with snake strikes until it reforms (30 s).
  FREED    (cosmetic) holy items - a Totem, a golden apple and a Pistachio-made dinner - "free" him: the 'freed' finish and a
           pale-gold, gentler serpent ('_f': rounder lids, blue eyes, a warm white flame); he stays because he wants to."""
import math
import knight_art as KA
from rigkit import el
from fol5_kit import (Rig, hexc, mix, limb, T, remap, cells, soft, lit, leaves, alpha, eye, blush, put, glow, chain, slab, stack, ring)

COMPANION = 0.5
FINISHES = ('hollow', 'freed', 'shiny')
_TAG = {'hollow': 'h', 'freed': 'f', 'shiny': 's'}
SOUL = ['#0a3a5a', '#2a8ad0', '#7ad8ff', '#e0f8ff']
RECOL = {
    'hollow': {'eye': SOUL, 'accent': SOUL, 'cloth': ['#1a0e2a', '#3a2260', '#5a3a8a'], 'hem': ['#5a3a08', '#b8862a', '#ffd870']},
    'freed': {'plate': ['#4a5060', '#a8b0c0', '#e4e8f0', '#ffffff'], 'dark': ['#3a3e48', '#7a808e', '#b8bcc8'], 'trim': ['#6a4a10', '#c8962a', '#ffe08a'],
              'bone': ['#7a5a10', '#d8aa3a', '#fff0a8'], 'tip': ['#7a5a10', '#d8aa3a', '#fff0a8'], 'eye': ['#8a5a00', '#ffc840', '#fff4c0'],
              'accent': ['#8a5a00', '#ffc840', '#fff4c0'], 'cloth': ['#a8a49a', '#e8e4da', '#ffffff'], 'hem': ['#6a4a10', '#c8962a', '#ffe08a'],
              'iron': ['#5a6070', '#b0b8c8', '#f0f4ff'], 'grip': ['#3a2a60', '#5a3a8a', '#8a6ab8']},
    'shiny': {'plate': ['#060a20', '#14204a', '#2a3a7a', '#4a5aa0'], 'dark': ['#04061a', '#0c1236', '#1a2450'], 'trim': ['#5a6070', '#b0b8c8', '#f0f4ff'],
              'bone': ['#5a6070', '#c0c8d8', '#ffffff'], 'eye': ['#7a5a10', '#ffe08a', '#fffbe8'], 'accent': ['#7a5a10', '#ffe08a', '#fffbe8'],
              'cloth': ['#0a1030', '#1a2a6a', '#3a4ab0'], 'hem': ['#5a6070', '#c0c8d8', '#ffffff']},
}

# ---- the serpent's palettes: scales (dark, base, light, tip), head (base, light, dark), belly, core, flame, eyes
SP = {'scale': ('#2a78c0', '#5ab4ec', '#8ad4ff', '#c0ecff'), 'head': ('#78ccf8', '#a8e2ff', '#4aa2dc'), 'belly': ('#cdeeff', '#eaf8ff', '#9cd4f4'),
      'core': ('#d8f8ff', '#ffffff', '#a8eeff'), 'flame': ('#8ae0ff', '#e4faff', '#4ab4f8'), 'blush': '#b8b0ff',
      'iris': ('#6a3a08', '#a8661a', '#d89a2a', '#f4c650', '#ffe490'), 'lash': '#16285a', 'white': '#f4fcff', 'mouth': '#2a5a8a',
      'gleye': ('#ffd870', '#fff6d0')}
SPSKINS = {
    '_f': {'scale': ('#b88a2a', '#e8c060', '#fde49a', '#fff6d0'), 'head': ('#f6dc8a', '#fff0c0', '#d8b04a'), 'belly': ('#fff6dc', '#fffcf0', '#f0dca0'),
           'core': ('#fffbe8', '#ffffff', '#ffe8a0'), 'flame': ('#fff0c0', '#ffffff', '#ffd060'), 'blush': '#ffb0a0',
           'iris': ('#1a3a6a', '#2a6ab0', '#4a9ae0', '#8ac8ff', '#c8e8ff'), 'lash': '#6a4a14', 'mouth': '#8a6a2a', 'gleye': ('#8ac8ff', '#e8f6ff')},
    '_s': {'scale': ('#120a3a', '#2a1a6a', '#4a3aa0', '#8a7ae0'), 'head': ('#3a2a8a', '#5a4ab0', '#24186a'), 'belly': ('#8a80d0', '#b0a8f0', '#6a60b0'),
           'core': ('#e8e8ff', '#ffffff', '#c0c0ff'), 'flame': ('#c0c8ff', '#ffffff', '#8a90ff'), 'blush': '#d090ff',
           'iris': ('#4a4a5a', '#8a8aa0', '#c0c0d0', '#e8e8f4', '#ffffff'), 'lash': '#0a0820', 'mouth': '#1a1040', 'gleye': ('#e8e8ff', '#ffffff')},
}
GA, HA, BA = 150, 210, 175                                   # (alphas: the scales, the head, the belly - see-through; the core opaque)


# ---------------------------------------------------------------------------------------------------- the armour
def _glimpse_tex(c, tag):
    """the textures of the serpent showing through the armour (by finish)"""
    sc = c['scale']
    return {f'hk_{tag}_sglim': alpha(leaves(sc, 61), GA), f'hk_{tag}_score': soft(*c['core'], 62, 0.15),
            f'hk_{tag}_seye': cells(lambda x, y, r: c['gleye'][1] if (x < 2 and y < 2) else c['gleye'][0], 63)}


_GL_FIN = {'hollow': SP, 'freed': dict(SP, **SPSKINS['_f']), 'shiny': dict(SP, **SPSKINS['_s'])}


def _glimpses(part, tag):
    """extra elements on the armour: the serpent seen through it (knight_art's own design units; this part's pivot)"""
    pv = KA.PIVOT[part]; g, cr, ey = f'hk_{tag}_sglim', f'hk_{tag}_score', f'hk_{tag}_seye'
    out = []
    if part == 'head':                                       # its two kind eyes in the eye-slit (rounded: a bar and a cap), a glint
        for sx in (1, -1):
            a, b = sorted((sx * 1.0, sx * 2.6))
            out += [el((a, 41.35, -5.0), (b, 42.35, -4.86), ey, pv, faces=('north',), light=15, uv={'north': [0, 0, 16, 16]}),
                    el((a + 0.25, 42.35, -5.0), (b - 0.25, 42.55, -4.86), ey, pv, faces=('north',), light=15, uv={'north': [0, 0, 16, 16]})]
    if part == 'chest':                                      # a coil in the gorget, a coil in the waist gap (glowing core inside)
        for (cy, r, n) in ((36.6, 3.9, 10), (24.6, 6.7, 14)):
            for k in range(n):
                a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
                A = (r * math.cos(a0), cy + 0.25 * math.sin(3 * a0), r * math.sin(a0) - 0.3)
                B = (r * math.cos(a1), cy + 0.25 * math.sin(3 * a1), r * math.sin(a1) - 0.3)
                from rigkit import seg
                out.append(seg(A, B, 1.6, 1.2, g, pv, ext=0.15, light=6))
                out.append(seg(A, B, 0.6, 0.5, cr, pv, ext=0.1, light=12))
    if part == 'cape':                                       # its tail-tip curling out under the cape's hem
        from rigkit import seg
        pts = [(1.5, 23.4, 5.3), (3.0, 22.2, 6.2), (4.6, 21.8, 6.9), (5.8, 22.6, 7.2), (6.2, 23.8, 6.9)]
        ws = [1.4, 1.1, 0.8, 0.55, 0.3]
        for i in range(len(pts) - 1):
            out.append(seg(pts[i], pts[i + 1], (ws[i] + ws[i + 1]) / 2, (ws[i] + ws[i + 1]) / 2, g, pv, ext=0.1, light=6))
            out.append(seg(pts[i], pts[i + 1], (ws[i] + ws[i + 1]) / 5, (ws[i] + ws[i + 1]) / 5, cr, pv, ext=0.05, light=12))
    return out


class Armour:
    """knight_art's dread knight under this follower's own names and finishes (hk_<finish>_<part>); a pose's _finish picks one"""
    PREFIX = 'hk_'
    PIVOT, PARENT, PARTS, PART_K = KA.PIVOT, KA.PARENT, KA.PARTS, KA.PART_K
    RIG_SCALE = KA.RIG_SCALE
    COMPANION = COMPANION

    def HIDDEN(self, p, pose):
        return p in pose.get('_hide', ())

    def model_name(self, p, pose=None, suffix=''):
        return f'hk_{(pose or {}).get("_finish", "hollow")}_{p}{suffix}'

    def textures(self):
        base = KA.textures(); out = {}
        for fin in FINISHES:
            for mat in KA.MATS:
                im = base[KA.tex_name(mat, 'dread', 'live')]
                rc = RECOL[fin].get(mat)
                out[f'hk_{_TAG[fin]}_{mat}'] = remap(im, rc, stretch=True) if rc else im
            out.update(_glimpse_tex(_GL_FIN[fin], _TAG[fin]))
        return out

    def models(self):
        out = {}
        for mid, (tex, els) in KA.models().items():
            if not mid.startswith('kn_dread_live_'): continue
            part = mid[len('kn_dread_live_'):]
            for fin in FINISHES:
                tag = _TAG[fin]
                rn = lambda t: t.replace('kn_dl_', f'hk_{tag}_')
                fe = [dict(e, faces={f: dict(fc, texture='#' + rn(fc['texture'][1:])) for f, fc in e['faces'].items()}) for e in els
                      if not (part == 'head' and any(fc['texture'].endswith('_eye') for fc in e['faces'].values()))]   # (the red squares: gone)
                fe += _glimpses(part, tag)
                used = sorted({fc['texture'][1:] for e in fe for fc in e['faces'].values()})
                out[f'hk_{fin}_{part}'] = ({t: f'bm:block/{t}' for t in used}, fe)
        return out


ARMOUR = Armour()


def _armour_poses():
    P = {}
    for n in ('idle_a', 'idle_b', 'walk_0', 'walk_1', 'swing_0', 'swing_1', 'spin_0', 'spin_1', 'stagger', 'statue', 'wake_0', 'wake_1'):
        P[n] = dict(KA.POSES[n])
    P['sit_a'] = dict(KA.POSES['death_0'])                   # (the vigil: down on one knee, the mace planted before him)
    P['sit_b'] = dict(KA.POSES['statue'])                    # (resting: the statue's stance, head bowed)
    heap = dict(KA.POSES['death_1'])                         # BROKEN: slumped, the helm knocked off and rolled away, the mace dropped
    heap['_o_head'] = (7.0, -16.0, -10.0); heap['_o_mace'] = (-4.0, -6.0, -6.0)
    P['heap'] = heap
    return P


ARMOUR.POSES = _armour_poses()
ARMOUR.DRAFT = ['idle_a', 'walk_0', 'swing_0', 'swing_1', 'spin_0', 'spin_1', 'sit_a', 'sit_b', 'stagger', 'heap']


# ---------------------------------------------------------------------------------------------------- the soul serpent
SHAPES = ('s', 'lunge', 'coil', 'drape', 'helm', 'dive', 'peek')
SPV = {'root': (0, 0, 0), 'head': (0, 0, 0), 'jaw': (0, 0.2, 0.6), 'tongue': (0, 0.6, -4.2), 'mist': (0, 2, -8),
       **{f'b_{s}': (0, 0, 0) for s in SHAPES}}
SPV['b_coil'] = (0, -14, 6)
SPP = {'root': None, 'head': 'root', 'jaw': 'head', 'tongue': 'head', 'mist': 'head', **{f'b_{s}': 'root' for s in SHAPES}}
SFACES = ('blink', 'happy', 'hiss', 'focus', 'hurt', 'sad', 'sleepy')
SERPENT = Rig('hs_', 0.75, SPV, SPP, SFACES, opt=('tongue', 'mist') + tuple(f'b_{s}' for s in SHAPES), companion=0.75)
SPIRIT = SERPENT                                              # (the old name)
S = SERPENT
FW, FH = 4.8, 2.9                                             # (the face plate on the cranium's front, above the snout: 19 x 12 texels)


def _sface(kind, c):
    im = lit(soft(c['head'][0], c['head'][1], c['head'][2], 71, 0.025), 1.06, 0.95, 6)
    im = alpha(im, 235)
    if kind not in ('hiss', 'hurt'):
        blush(im, 2, 10, 4, c['blush']); blush(im, 17, 10, 4, c['blush'])
    return im


def _seyes(kind, c):
    from PIL import Image
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    k = {'hiss': 'fierce', 'focus': 'fierce'}.get(kind, kind)
    for cx, fl in ((5, False), (15, True)):
        eye(im, cx, 2, 8, 9, fl, k, iris=c['iris'], lash=mix(c['lash'], c['head'][2], 0.35), pupil='#2a1404', sclera=False, irk=0.7)
    return im


def _snout(kind, c):
    """the snout's front: two nostrils, a soft smile line (a hiss: an open dark mouth line)"""
    im = lit(soft(c['head'][0], c['head'][1], c['head'][2], 72, 0.025), 1.05, 0.95, 4)
    for x in (4, 9): put(im, x, 1, c['mouth'])
    if kind == 'hiss':
        for x in range(2, 12): put(im, x, 6, c['mouth'])
    elif kind in ('sad', 'hurt'):
        for x in range(4, 10): put(im, x, 5, c['mouth'])
        put(im, 3, 6, c['mouth']); put(im, 10, 6, c['mouth'])
    else:
        for x in range(4, 10): put(im, x, 6, c['mouth'])
        put(im, 3, 5, c['mouth']); put(im, 10, 5, c['mouth'])
    return alpha(im, 235)


def _stex(c):
    t = {'scale': alpha(leaves(c['scale'], 73), GA), 'scale2': alpha(leaves(c['scale'], 74), GA - 25),
         'scalef': alpha(leaves(c['scale'], 75), 95),                                                  # (the dissolving tail)
         'head': alpha(lit(soft(c['head'][0], c['head'][1], c['head'][2], 76, 0.03), 1.08, 0.92, 10), HA),
         'belly': alpha(cells(lambda x, y, r: c['belly'][2] if y % 3 == 0 else (c['belly'][1] if y % 3 == 1 else c['belly'][0]), 77), BA),
         'core': soft(*c['core'], 78, 0.15), 'wisp': alpha(soft(c['core'][0], c['core'][1], c['scale'][2], 79, 0.2), 105),
         'flame': lit(soft(c['flame'][0], c['flame'][1], c['flame'][2], 80, 0.2), 1.2, 0.85, 12), 'flamec': soft(c['core'][1], '#ffffff', c['core'][0], 81, 0.1),
         'tongue': soft('#6a8ae0', '#9ab4ff', '#4a6ac0', 82, 0.1), 'mist': glow((c['core'][1], c['core'][0], c['scale'][2], c['scale'][2]), 16, alpha=(170, 120, 70, 0)),
         'face': _sface(None, c), 'eyes': _seyes(None, c), 'snout': _snout(None, c)}
    for f in SFACES:
        t[f'face_{f}'] = _sface(f, c); t[f'eyes_{f}'] = _seyes(f, c); t[f'snout_{f}'] = _snout(f, c)
    return t


BASE = _stex(SP)
for k, v in BASE.items(): S.tex(k, v)
for sfx, ch in SPSKINS.items():
    for k, v in _stex(dict(SP, **ch)).items(): S.tex(k + sfx, v)
    S.skin(sfx, {k: k + sfx for k in BASE})

# ---- the head: a rounded cranium, a short snout, the jaw (its own part), the face plate and eye overlay, cheek wisps, the crest
B = S.box
B('head', (-2.4, 0.2, -2.6), (2.4, 4.5, 2.2), 'head', shift=False)
B('head', (-2.0, 4.5, -2.3), (2.0, 4.95, 1.8), 'head')
B('head', (-2.75, 0.6, -2.2), (2.75, 3.6, 1.7), 'head')
B('head', (-1.9, 0.5, 2.2), (1.9, 3.6, 3.1), 'head')
B('head', (-1.2, 0.9, 3.1), (1.2, 3.0, 3.6), 'scale')
B('head', (-FW / 2, 1.6, -2.62), (FW / 2, 1.6 + FH, -2.6), 'FACE', faces=('north',), uv={'north': [0, 0, FW, FH]})
B('head', (-FW / 2, 1.6, -2.66), (FW / 2, 1.6 + FH, -2.64), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]}, light=10)
B('head', (-1.8, 0.0, -4.3), (1.8, 1.65, -2.6), 'head')
B('head', (-1.4, 1.65, -4.0), (1.4, 1.95, -2.6), 'head')
B('head', (-1.82, 0.0, -4.32), (1.82, 1.65, -4.3), 'SNOUT', faces=('north',), uv={'north': [0, 0, 3.64, 1.65]})
B('head', (-2.5, 1.7, -2.68), (2.5, 2.0, -2.6), 'head')                                    # (the lids' ledge: a soft brow)
for sx in (1, -1):                                                                          # (cheek wisps trailing back)
    S.seg('head', (sx * 2.6, 2.6, 0.2), (sx * 4.4, 3.6, 3.4), 1.0, 0.14, 'wisp', up=(sx * 0.4, 1.0, 0.0), light=8)
    S.seg('head', (sx * 2.6, 1.2, 0.5), (sx * 4.0, 0.6, 3.6), 0.8, 0.14, 'wisp', up=(sx * 0.4, 1.0, 0.0), light=8)
# the crest: a small soul-flame on the crown, its tip curling back, a white core
stack(S, 'head', [(4.9, 5.5, 0.95), (5.5, 6.5, 1.12), (6.5, 7.3, 0.8), (7.3, 7.8, 0.46)], 'flame', c=(0, 0.2), light=14)
S.seg('head', (0, 7.7, 0.25), (0, 8.6, 1.2), 0.44, 0.44, 'flame', light=14)
S.seg('head', (0, 8.6, 1.2), (0, 8.5, 1.9), 0.3, 0.3, 'flame', light=14)
stack(S, 'head', [(5.0, 5.7, 0.58), (5.7, 6.4, 0.45)], 'flamec', c=(0, -0.55), light=15)
for sx in (1, -1): S.seg('head', (sx * 0.7, 4.9, 0.6), (sx * 1.6, 6.1, 1.5), 0.4, 0.4, 'flame', light=14)
# the jaw: pale belly-scale underneath, its own part (opens for the hiss)
B('jaw', (-1.7, -0.75, -4.1), (1.7, 0.05, 1.8), 'belly')
B('jaw', (-1.3, -1.0, -2.6), (1.3, -0.75, 1.6), 'belly')
# the tongue (a hiss): forked
tx, ty, tz = SPV['tongue']
S.seg('tongue', (0, ty, tz), (0, ty - 0.2, tz - 2.0), 0.3, 0.12, 'tongue')
for sx in (1, -1): S.seg('tongue', (0, ty - 0.2, tz - 2.0), (sx * 0.4, ty - 0.3, tz - 2.7), 0.2, 0.1, 'tongue')
# the mist of the hiss: soft rings going out
for i in range(3):
    z = -7 - i * 2.6; r = 1.2 + i * 0.7
    ring(S, 'mist', (0, 1.0, z), r, 8, 0.25, 0.25, 'wisp', plane='xy', light=10)


def body(shape, pts, w0=2.7, w1=0.35, fade=3, fins=True):
    """the body along a path from the neck back to the tip: translucent scales over a glowing core, the pale belly on the
    down faces, little wisp-fins along the back, the last spans fading into motes"""
    part = f'b_{shape}'; n = len(pts) - 1
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        w = w0 + (w1 - w0) * ((t0 + t1) / 2) ** 0.8
        tx = 'scale' if i < n - fade else ('scale2' if i < n - 1 else 'scalef')
        e = S.seg(part, pts[i], pts[i + 1], w, w * 0.92, tx, ext=0.06, light=4)
        if 'down' in e['faces'] and i < n - fade: e['faces']['down']['texture'] = '#belly'
        if i < n - 1: S.seg(part, pts[i], pts[i + 1], w * 0.36, w * 0.32, 'core', ext=0.06, light=12)
        if fins and i % 2 == 1 and i < n - 2:                                                  # (a wisp-fin standing off the back)
            m = tuple((pts[i][k] + pts[i + 1][k]) / 2 for k in range(3)); d = tuple(pts[i + 1][k] - pts[i][k] for k in range(3))
            L = math.sqrt(sum(v * v for v in d)) or 1
            S.seg(part, (m[0], m[1] + w * 0.4, m[2]), (m[0] + d[0] / L * 1.2, m[1] + w * 0.4 + 1.1, m[2] + d[2] / L * 1.2), 0.16, w * 0.5, 'wisp', light=8)
    tip, prev = pts[-1], pts[-2]
    for k, s in enumerate((0.42, 0.3, 0.2)):                                                      # (motes drifting off the tail)
        p = tuple(tip[j] + (tip[j] - prev[j]) * (0.8 + 0.9 * k) + (0.5 if j == 1 else 0) * k for j in range(3))
        S.box(part, tuple(v - s for v in p), tuple(v + s for v in p), 'core', light=12)


def _spiral(c, r0, r1, y0, y1, a0, turns, n):
    pts = []
    for k in range(n + 1):
        t = k / n; a = a0 + 2 * math.pi * turns * t; r = r0 + (r1 - r0) * t
        pts.append((c[0] + r * math.cos(a), y0 + (y1 - y0) * t, c[2] + r * math.sin(a)))
    return pts


# 's': reared from a ground coil - the neck rises in a soft S
body('s', [(0, 0, 0), (0, -2.4, 0.9), (0.7, -4.8, 2.3), (0.5, -7.2, 3.2), (-0.6, -9.4, 2.8)] +
     _spiral((0, 0, 5.4), 3.2, 1.6, -10.6, -10.3, math.radians(220), 1.15, 9)[1:])
# 'lunge': stretched forward low over its coil, striking
body('lunge', [(0, 0, 0), (0, -0.6, 3.0), (0, -2.0, 6.2), (0.4, -4.2, 8.6), (0.2, -6.2, 10.0)] +
     _spiral((0, 0, 12.6), 3.0, 1.6, -6.9, -6.6, math.radians(200), 1.1, 8)[1:])
# 'coil': wound round a foe - 1.5 turns of radius 7, the head over the top looking down at its face (its own pivot)
cc = (0, 0, 6.0)
body('coil', [(0, 0, 0), (0, -1.2, 1.6), (0, -2.6, 2.4)] + _spiral(cc, 7.4, 7.0, -3.6, -22.0, math.radians(260), 1.5, 24), w0=3.0, w1=1.0)
# 'drape': across the kneeling armour's shoulders (the head on its right pauldron, the tail down the front of its left)
body('drape', [(0, 0, 0), (0.2, 0.2, 2.0), (-1.2, 0.7, 4.0), (-5.0, 0.9, 4.7), (-9.6, 0.7, 3.8), (-13.8, 0.1, 2.2), (-15.0, -1.0, -0.3),
               (-14.8, -3.4, -1.5), (-14.4, -6.2, -1.2), (-14.6, -8.6, -0.2)])
# 'helm': curled once round the helm, the head resting on its brow (the doll)
HELM_C = (-3.4, -1.8, 1.2)                                   # (the ring's centre, from the neck: the head rests on the helm's right-top corner)
body('helm', [(0, 0, 0), (0.3, -0.7, 1.4)] + _spiral(HELM_C, 4.4, 4.2, -1.4, -2.2, math.radians(16), 0.97, 14) +
     [(-0.6, -3.4, -3.0), (0.8, -5.0, -3.0), (1.4, -6.8, -2.4)], w0=2.2, w1=0.45)
# 'dive': streamlined behind the head, a wave in it
body('dive', [(0, 0, 0), (0, 0.4, 3.0), (0.6, 0.6, 6.0), (0, 1.0, 9.0), (-0.6, 1.8, 12.0), (0, 3.0, 14.8), (0.3, 4.4, 17.0)], w0=2.0, w1=0.4)
# 'peek': only the neck, going back into the visor (half out)
body('peek', [(0, 0, 0), (0, -0.3, 2.5), (0, -0.5, 5.0), (0, -0.6, 7.5)], w0=2.6, w1=2.1, fade=1, fins=False)


def SPZ(lift=None, **kw):
    return S.ground(kw, lift) if lift is not None else kw


S.POSES.update({
    'idle_a': SPZ(0.0, _show=('b_s',), head=T(4, 0, 6)),
    'idle_b': SPZ(0.0, _show=('b_s',), _face='happy', head=T(-8, 14, -10)),
    'hiss': SPZ(0.0, _face='hiss', _show=('b_s', 'tongue', 'mist'), head=T(-16), jaw=T(30)),
    'strike_up': SPZ(0.0, _face='focus', _show=('b_s',), head=T(-28), jaw=T(16)),
    'strike': SPZ(0.0, _face='hiss', _show=('b_lunge', 'tongue'), head=T(14), jaw=T(40)),
    'coil': {'_face': 'focus', '_show': ('b_coil',), 'head': T(34)},
    'dive': {'_face': 'focus', '_show': ('b_dive',), 'head': T(0), 'root': T(68)},
    'peek': {'_face': None, '_show': ('b_peek',), 'head': T(6, -10, 4)},
    'emerge': {'_face': 'happy', '_show': ('b_peek',), 'root': T(-6), 'head': T(10, 0, 8)},
    'divein': {'_face': 'focus', '_show': ('b_dive',), 'root': T(-8), 'head': T(4)},
    'drape': {'_face': 'sleepy', '_show': ('b_drape',), 'head': T(14, -8, 6)},
    'helm': {'_face': 'happy', '_show': ('b_helm',), 'head': T(14, 24, -8)},
    'happy': SPZ(0.0, _face='happy', _show=('b_s',), head=T(-12, 0, 10)),
    'hurt': SPZ(0.0, _face='hurt', _show=('b_s',), head=T(-20, 20, 14), jaw=T(10)),
})
S.DRAFT = ['idle_a', 'idle_b', 'hiss', 'strike_up', 'strike', 'happy', 'hurt']
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'legr': 'legs', 'shinr': 'legs', 'legl': 'legs', 'shinl': 'legs'}
SHINY = 'Shiny Starlit (deep blue plate, silver trim; a starry indigo serpent with silver eyes)'
SKIN_NAMES = {'_f': 'FREED (holy cosmetic): pale gold, gentler', '_s': 'SHINY Starlit'}
