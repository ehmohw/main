"""(3.1 draft, stage 1: art only - not wired) THE HOLLOW STATUE KNIGHT - two in one: an Undercrown Statue Knight's armour (knight_art,
'dread') with a SOUL SERPENT coiled inside it. (2nd pass: the owner changed the ghost to a soul serpent; polished to the bar.)

LORE (kept to phase169's Omega's Book and phase163's Pistachio): the soul is SIR ALDOUS VANE, Captain of King Omega's palace guard
on Omega Island, who held the great stair beside his king in the War of Brothers and fell there. Apophiss "went away to make other
kings - hollow ones": he took the fallen guards' souls and bound them into the Dread's statue armour in the Undercrown - and, as
his mark on them, bound them IN SERPENT FORM, his own shape, so they would never again stand as men. Sir Aldous has been a soul
serpent coiled in a hollow suit of armour for three hundred years. He isn't a serpent at heart: he wears the soldiers' shape and
scowl, but his soul flame burns on his tail like a candle in a window.
Before the war Pistachio was Sir Aldous's dog - "Pip", a pup at his heel on the guard's rounds - until the Captain gave him to the
King's household the night he rode to the stair: "Mind the door, Pip." Pistachio has minded it for three hundred years.

UNLOCK  Place a knight statue you've earned (knight_statue_dread), then call Pistachio and King Omega beside it (two of your
        three). Pistachio sniffs the plinth - and BARKS (his first bark in the pack: he's a butler); Omega: "...Aldous? Is that
        you in there?" Two glowing yellow eyes open in the eye-slit; a soul serpent's head slides out of the visor, looks at the dog a
        long moment, and lays its chin on Pistachio's head. The armour kneels.

TWO IN ONE (two rigs, one follower)
  ARMOUR   knight_art's rig and geometry at companion size (0.5: ~1.5 blocks), with this follower's finishes (FINISHES) and the
           SERPENT SHOWING THROUGH IT: its two glowing yellow eyes in the eye-slit (the Dread's red squares are gone), a coil of
           translucent soul glimpsed in the gorget and in the gap at the waist, its tail-tip curling out under the cape's hem.
           Finishes: 'hollow' (the default: black plate and bone, soul-blue light, the cloak re-dyed Omega's palace violet with a
           gold hem), 'freed' (the holy cosmetic: polished silver, gold for bone, a white cloak, warm gold light - the serpent in
           it pale gold), 'shiny' (Starlit: deep blue plate, silver trim; a starry indigo serpent).
           It swings the giant mace: knight_art's own poses, plus the kneel (sit_a, the vigil), the statue stance (sit_b) and the
           heap (BROKEN: helm knocked off, the mace dropped).
  SERPENT  the soul itself (SERPENT, 'hs_'): ONE OF KING OMEGA'S SOUL SERPENTS (3rd pass, the owner: "should look like the existing
           one in game") - soulserp_art's own head, jaw and crest 'a' (the pale spikes swept back), imported and scaled (K_HEAD):
           the snout and nostrils, heavy grey lids and the family's brows, solid glowing yellow eyes, a purple maw with cream fangs
           and the long forked tongue; its see-through pale grey-blue hide, banded belly and back fins (soulserp's textures); the
           blue soul flame on its tail tip. Its body is a set of shapes, one shown per pose (_show): 's' (reared, the tail up
           with its flame), 'lunge' (a strike), 'coil' (wound round a foe - 1.5 turns, radius ~1/3 block), 'drape' (over the
           kneeling armour's shoulders), 'helm' (curled round the helm: the doll), 'dive' (back in through the visor), 'peek'
           (half out of the visor).
  BROKEN   beaten down, the armour falls apart ('heap') and the serpent fights alone with snake strikes until it reforms (30 s).
  FREED    (cosmetic) holy items - a Totem, a golden apple and a Pistachio-made dinner - "free" him: the 'freed' finish and the
           same serpent, gentler, in pale gold ('_f': soulserp's textures tinted - soft blue eyes, a rose maw, a warm white flame);
           he stays because he wants to."""
import math
import knight_art as KA
import soulserp_art as SS
import apophiss_art as AP
from rigkit import el, frame as rframe
from fol5_kit import (Rig, hexc, mix, limb, T, remap, cells, soft, lit, leaves, alpha, eye, blush, put, glow, chain, slab, stack, ring,
                      xform_els)

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

# ---- the serpent's palettes. The default IS soulserp_art's (King Omega's Soul Serpents: its textures, used as they are); the
# skins are those same textures tinted (_tint keeps every streak, scale and ghost alpha):
# '_f' FREED - gentler, pale gold: a warm hide, soft blue eyes, a rose maw, a warm white flame; '_s' STARLIT - starry indigo,
# silver eyes. gleye/core: the colours the armour's glimpses use (the eyes in the slit, the soul light in the gaps).
SP = {'hide': '#b4bcc6', 'belly': '#dfe6ee', 'lid': '#a2aab4', 'eye': '#ffe23a', 'maw': '#3a1446', 'tongue': '#9a3ac8', 'fang': '#f0eee6',
      'flame': '#7ad8ff', 'gleye': ('#ffe23a', '#fff6a0'), 'core': ('#d8f8ff', '#ffffff', '#a8eeff')}
SPSKINS = {
    '_f': {'hide': '#ecd08a', 'belly': '#fff6dc', 'lid': '#d8b470', 'eye': '#a8d4ff', 'maw': '#7a3a4a', 'tongue': '#e08aa8', 'fang': '#fff8e8',
           'flame': '#fff0c0', 'gleye': ('#8ac8ff', '#e8f6ff'), 'core': ('#fffbe8', '#ffffff', '#ffe8a0'),
           'ramps': {'ss_body': ('#8a6a2a', '#c8a050', '#ecd08a', '#fff0c8'), 'ss_body_dk': ('#6a4a1a', '#a8803a', '#d8b470'),
                     'ss_lid': ('#8a6a2a', '#c8a050', '#ecd08a'), 'ss_belly': ('#c8b080', '#f0e0b0', '#fff8e0'),
                     'ss_fin': ('#b89a50', '#f0dca0', '#fffbe8'), 'ss_eye': ('#7ab8f0', '#a8d4ff', '#d8eeff'),
                     'ss_mouth': ('#4a2030', '#7a3a4a', '#9a5060'), 'ss_tongue': ('#b85a7a', '#e08aa8', '#f4b8c8'),
                     'ss_fang': ('#e8dcc0', '#fff8e8'), 'ss_brow': ('#6a4a20', '#8a6a3a'), 'ss_lash': ('#5a3a14', '#6a4a20'),
                     'ss_flame': ('#d8a040', '#ffd878', '#fff0c0', '#ffffff'), 'ss_flame_core': ('#fffbe8', '#ffffff'),
                     'wisp': ('#e8d8a8', '#fff4d8', '#fffcf0'), 'ss_claw': ('#3a2a14', '#5a4424', '#7a6038')}},
    '_s': {'hide': '#4a3aa0', 'belly': '#b0a8f0', 'lid': '#2a1a6a', 'eye': '#f0f0ff', 'maw': '#1a0a3a', 'tongue': '#8a5ae0', 'fang': '#e8e8ff',
           'flame': '#c0c8ff', 'gleye': ('#e8e8ff', '#ffffff'), 'core': ('#e8e8ff', '#ffffff', '#c0c0ff'), 'stars': True,
           'ramps': {'ss_body': ('#120a3a', '#2a1a6a', '#4a3aa0', '#8a7ae0'), 'ss_body_dk': ('#0a0628', '#1a1050', '#2a1a6a'),
                     'ss_lid': ('#1a1050', '#2a1a6a', '#4a3aa0'), 'ss_belly': ('#6a60b0', '#8a80d0', '#b0a8f0'),
                     'ss_fin': ('#4a3aa0', '#8a7ae0', '#c0b8ff'), 'ss_eye': ('#d0d0e0', '#f0f0ff', '#ffffff'),
                     'ss_mouth': ('#0a0420', '#1a0a3a', '#2a1650'), 'ss_tongue': ('#5a2ab0', '#8a5ae0', '#b08aff'),
                     'ss_fang': ('#d0d0f0', '#f4f4ff'), 'ss_brow': ('#05040c', '#12102a'), 'ss_lash': ('#05040c', '#0a0820'),
                     'ss_flame': ('#6a70e0', '#a0a8ff', '#d8dcff', '#ffffff'), 'ss_flame_core': ('#f0f0ff', '#ffffff'),
                     'wisp': ('#8a80d0', '#b0a8f0', '#e0dcff'), 'ss_claw': ('#06051a', '#12103a', '#24205a')}},
}
GA, HA, BA = 128, 220, 148                                   # (alphas: soulserp's - the hide, the lids, the belly: see-through)


def _soul_tex():
    """the serpent's textures: soulserp_art's own (local names; the rig prefixes hs_), plus the hiss's mist"""
    t = {k: v for k, v in SS.textures().items() if k in _SS_USED}
    t['wisp'] = alpha(soft('#d6dce4', '#f2f6fa', '#a8b0bc', 79, 0.2), 105)
    return t


def _tint(im, col):
    """soulserp's texture recoloured toward col, keeping its own light and dark (each pixel's lightness against the texture's
    mean - its scale rims, streaks and noise stay as subtle as they were) and its ghost alpha"""
    im = im.convert('RGBA').copy(); px = im.load(); c = hexc(col)
    lum = lambda p: 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]
    vs = [lum(px[x, y]) for y in range(im.height) for x in range(im.width) if px[x, y][3]]
    m = max(1.0, sum(vs) / max(1, len(vs)))
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3]: k = lum(p) / m; px[x, y] = tuple(max(0, min(255, int(c[i] * k))) for i in range(3)) + (p[3],)
    return im


def _skin_tex(base, sk):
    out = {}
    for k, im in base.items():
        rp = sk['ramps'].get(k)
        im = _tint(im, rp[len(rp) // 2]) if rp else im
        if sk.get('stars') and k in ('ss_body', 'ss_body_dk', 'ss_belly', 'ss_fin'):
            im = im.copy(); rnd = __import__('random').Random(sum(map(ord, k)))
            for _ in range(14):
                x, y = rnd.randrange(64), rnd.randrange(64)
                if im.getpixel((x, y))[3]: im.putpixel((x, y), (255, 255, 255, im.getpixel((x, y))[3]))
        out[k] = im
    return out


def _glimpse_tex(fin, tag):
    """the textures of the serpent showing through the armour (by finish): its own hide, its soul light, its glowing eyes"""
    t = STEX[_GL_FIN[fin]]; c = SP if _GL_FIN[fin] == '' else dict(SP, **SPSKINS[_GL_FIN[fin]])
    return {f'hk_{tag}_sglim': alpha(t['ss_body'], 170), f'hk_{tag}_score': soft(*c['core'], 62, 0.15),
            f'hk_{tag}_seye': cells(lambda x, y, r: c['gleye'][1] if (x < 2 and y < 2) else c['gleye'][0], 63)}


_GL_FIN = {'hollow': '', 'freed': '_f', 'shiny': '_s'}


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
            out.update(_glimpse_tex(fin, _TAG[fin]))
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
# Sir Aldous is one of King Omega's Soul Serpents (soulserp_art): the same head (built from it - its snout, nostrils, heavy grey
# lids, the family's brows, solid glowing yellow eyes, the purple maw with cream fangs and the long forked tongue; crest 'a', the
# pale spikes swept back), the same see-through pale grey-blue hide, banded belly and fins, the same blue soul flame on the tail
# tip - scaled to a knight's soul (K_HEAD) and laid along this follower's own body shapes.
SHAPES = ('s', 'lunge', 'coil', 'drape', 'helm', 'dive', 'peek')
CREST = 'a'
K_HEAD = 0.34                                                 # (soulserp's head at this follower's size)
K_FLAME = 0.46                                                # (and its tail flame, a little larger: a candle you can see)
_PH, _PJ, _PF = SS.PIVOT['head'], SS.PIVOT['jaw'], SS.PIVOT['flame']
_FLAME_C = (2.75, 2.4, 55.4)                                  # (where soulserp's flame sits on its tail tip)
SPV = {'root': (0, 0, 0), 'head': (0, 0, 0), 'jaw': tuple(round((_PJ[i] - _PH[i]) * K_HEAD, 3) for i in range(3)),
       'tongue': (0, 0.35, -4.4), 'mist': (0, 2, -8), **{f'b_{s}': (0, 0, 0) for s in SHAPES}}
SPV['b_coil'] = (0, -14, 6)
# its arms (3.1, the owner: "the soul serpent is missing its arms"): soulserp's small arms and dark claws, at the head's scale; their
# shoulders where the soldiers' are against the head (each shape moves them onto its own neck: ARMS_AT, by '_o_armr' / '_o_arml')
_PAR, _PAL = SS.PIVOT['armr'], SS.PIVOT['arml']
SPV['armr'] = tuple(round((_PAR[i] - _PH[i]) * K_HEAD, 3) for i in range(3))
SPV['arml'] = tuple(round((_PAL[i] - _PH[i]) * K_HEAD, 3) for i in range(3))
SPP = {'root': None, 'head': 'root', 'jaw': 'head', 'tongue': 'head', 'mist': 'head', **{f'b_{s}': 'root' for s in SHAPES},
       'armr': 'root', 'arml': 'root'}
SFACES = ('blink', 'happy', 'hiss', 'focus', 'hurt', 'sad', 'sleepy')
_AF = {'blink': 'blink', 'happy': 'smug', 'hiss': 'shock', 'focus': 'smug', 'hurt': 'hurt', 'sad': 'tired', 'sleepy': 'tired'}   # (-> the family's faces)
SERPENT = Rig('hs_', 0.75, SPV, SPP, SFACES, opt=('tongue', 'mist') + tuple(f'b_{s}' for s in SHAPES), companion=0.75)
SPIRIT = SERPENT                                              # (the old name)
S = SERPENT
FW, FH = 4.8, 2.9                                             # (kept: the old face plate's size)

_ASRC = AP.models()
_SS_USED = {'ss_body', 'ss_body_dk', 'ss_belly', 'ss_fin', 'ss_mouth', 'ss_tongue', 'ss_fang', 'ss_eye', 'ss_lid', 'ss_brow', 'ss_lash',
            'ss_flame', 'ss_flame_core', 'ss_claw'}
BASE = _soul_tex()
STEX = {'': BASE, **{sfx: _skin_tex(BASE, sk) for sfx, sk in SPSKINS.items()}}
for k, v in BASE.items(): S.tex(k, v)
for sfx in SPSKINS:
    for k, v in STEX[sfx].items(): S.tex(k + sfx, v)
    S.skin(sfx, {k: k + sfx for k in BASE})


def _head_els(face):
    """soulserp's head for this expression (as soulserp_art.models builds it: the brothers' head, retextured, its fins dropped,
    the crest added), brought to this rig's head"""
    src = _ASRC[f'apo_head_x{_AF[face]}' if face else 'apo_head'][1]
    els = SS._retex([e for e in src if 'apo_fin' not in SS._tex(e)]) + SS._crest(CREST, _PH)
    return xform_els(els, _PH, _PH, K_HEAD, SPV['head'], SPV['head'])


S.add('head', _head_els(None))
for _f in SFACES: S.face_els('head', _f, _head_els(_f))
S.add('jaw', xform_els(SS._retex(_ASRC['apo_jaw'][1]), _PJ, _PH, K_HEAD, SPV['head'], SPV['jaw']))
_SSM = SS.models()
for _a, _sp in (('armr', _PAR), ('arml', _PAL)):
    S.add(_a, xform_els(_SSM[f'ss_{_a}'][1], _sp, _PH, K_HEAD, SPV['head'], SPV[_a]))
_FLAME = [e for e in _SSM['ss_flame'][1] if 'ss_body_dk' not in SS._tex(e)]      # (its stem dropped: the tail tip is its stem)
# the tongue (the hiss): soulserp's long purple forked tongue, flicked straight out
tx, ty, tz = SPV['tongue']
S.seg('tongue', (0, ty, tz), (0, ty - 0.2, tz - 2.4), 0.5, 0.16, 'ss_tongue')
for sx in (1, -1): S.seg('tongue', (0, ty - 0.2, tz - 2.4), (sx * 0.5, ty - 0.3, tz - 3.3), 0.26, 0.12, 'ss_tongue')
# the mist of the hiss: soft rings going out
for i in range(3):
    z = -7.6 - i * 2.6; r = 1.3 + i * 0.7
    ring(S, 'mist', (0, 1.0, z), r, 8, 0.25, 0.25, 'wisp', plane='xy', light=10)


def body(shape, pts, w0=3.2, w1=1.1, fade=None, fins=True, flame=True):
    """the body along a path from the neck back to the tip, soulserp's: the see-through pale hide, the banded belly plate on its
    underside (a hair proud), a fin off the back every other span (the brothers' sail), and the blue soul flame on the tip"""
    part = f'b_{shape}'; n = len(pts) - 1; pv = SPV[part]
    for i in range(n):
        A, B = pts[i], pts[i + 1]
        w = w0 + (w1 - w0) * ((i + 0.5) / n) ** 0.8; h = w * 0.88
        e = S.seg(part, A, B, w, h, 'ss_body', ext=0.08)
        if 'down' in e['faces']: e['faces']['down']['texture'] = '#ss_belly'
        x, y, z = rframe(tuple(B[k] - A[k] for k in range(3)), (0.0, 1.0, 0.0))
        dn = lambda p, d: tuple(p[k] - y[k] * d for k in range(3))
        S.seg(part, dn(A, h / 2 + 0.05), dn(B, h / 2 + 0.05), w * 0.62, 0.12, 'ss_belly', up=y, ext=0.04)
        if fins and i % 2 == 0 and i < n - 1:
            a, b = dn(A, -h / 2 + 0.15), dn(B, -h / 2 + 0.15)
            tip = tuple(b[k] + y[k] * w * 0.45 + z[k] * w * 0.4 for k in range(3))
            S.add(part, AP._sail(a, b, tip, 0.22, 'ss_fin', pv, 2, up=x))
    if flame:
        tip, prev = pts[-1], pts[-2]
        S.add(part, xform_els(_FLAME, _PF, _FLAME_C, K_FLAME, (tip[0], tip[1] + w1 * 0.35, tip[2]), pv))


def _spiral(c, r0, r1, y0, y1, a0, turns, n):
    pts = []
    for k in range(n + 1):
        t = k / n; a = a0 + 2 * math.pi * turns * t; r = r0 + (r1 - r0) * t
        pts.append((c[0] + r * math.cos(a), y0 + (y1 - y0) * t, c[2] + r * math.sin(a)))
    return pts


# 's': reared from a ground coil - the neck rises in a soft S
# (its tail curls up out of the coil beside it, the soul flame held aloft - as soulserp's soldiers hold theirs)
body('s', [(0, -0.6, 0.6), (0, -2.8, 1.4), (0.7, -5.2, 2.6), (0.5, -7.6, 3.4), (-0.6, -9.6, 3.0)] +
     _spiral((0, 0, 5.6), 3.4, 2.8, -10.6, -10.3, math.radians(220), 0.85, 8)[1:] + [(-4.2, -9.4, 6.6), (-5.2, -7.6, 6.9), (-5.6, -5.6, 7.0)])
# 'lunge': stretched forward low over its coil, striking
body('lunge', [(0, -0.6, 0.6), (0, -1.0, 3.2), (0, -2.4, 6.4), (0.4, -4.4, 8.8), (0.2, -6.2, 10.2)] +
     _spiral((0, 0, 12.8), 3.2, 2.4, -6.9, -6.6, math.radians(200), 0.8, 7)[1:] + [(-2.6, -5.8, 16.1), (-3.3, -4.2, 17.0), (-3.5, -2.6, 17.3)])
# 'coil': wound round a foe - 1.5 turns of radius 7, the head over the top looking down at its face (its own pivot)
cc = (0, 0, 6.0)
body('coil', [(0, -0.6, 0.6), (0, -1.4, 1.8), (0, -2.6, 2.4)] + _spiral(cc, 7.4, 7.0, -3.6, -22.0, math.radians(260), 1.5, 24), w0=3.0, w1=1.0)
# 'drape': across the kneeling armour's shoulders (the head on its right pauldron, the tail down the front of its left)
body('drape', [(0, -0.6, 0.6), (0.2, -0.2, 2.2), (-1.2, 0.5, 4.2), (-5.0, 0.9, 4.8), (-9.6, 0.7, 3.8), (-13.8, 0.1, 2.2), (-15.0, -1.0, -0.3),
               (-14.8, -3.4, -1.5), (-14.4, -6.2, -1.2), (-14.6, -8.6, -0.2)], w0=3.0)
# 'helm': curled once round the helm, the head resting on its brow (the doll)
HELM_C = (-4.8, -2.4, 1.4)                                   # (the ring's centre, from the neck: the head rests on the helm's right-top corner)
body('helm', [(0, -0.6, 0.6), (0.3, -0.9, 1.6)] + _spiral(HELM_C, 4.6, 4.4, -1.4, -2.2, math.radians(16), 0.97, 14) +
     [(-0.6, -3.4, -3.0), (0.8, -5.0, -3.0), (1.4, -6.8, -2.4)], w0=2.6, w1=0.9)
# 'dive': streamlined behind the head, a wave in it
body('dive', [(0, -0.4, 0.6), (0, 0.2, 3.2), (0.6, 0.6, 6.0), (0, 1.0, 9.0), (-0.6, 1.8, 12.0), (0, 3.0, 14.8), (0.3, 4.4, 17.0)], w0=2.8, w1=1.0)
# 'peek': only the neck, going back into the visor (half out)
body('peek', [(0, -0.4, 0.6), (0, -0.5, 2.5), (0, -0.6, 5.0), (0, -0.6, 7.5)], w0=3.0, w1=2.6, fins=False, flame=False)


def SPZ(lift=None, **kw):
    return S.ground(kw, lift) if lift is not None else kw


# where each shape's shoulders are (on its neck, just under the head), and the arms' turns pose by pose - soulserp's conventions:
# x negative swings an arm forward / up, z out to its own side (armr -z, arml +z)
ARMS_AT = {'s': (1.85, -1.7, -0.3), 'lunge': (1.8, -1.4, 1.5), 'coil': (1.9, -1.5, 1.1), 'drape': (1.8, -1.2, 1.6), 'helm': (1.8, -1.4, 1.3),
           'dive': (1.7, -1.0, 1.8), 'peek': (1.8, -1.4, 1.5)}


def ARMS(shape, r, l=None):
    """the arms for a pose on this body shape: r = (x, z) turns for its right arm, l for its left (default: r mirrored)"""
    l = l or (r[0], -r[1]); a = ARMS_AT[shape]
    return {'_o_armr': tuple(round((a[0], a[1], a[2])[i] - SPV['armr'][i], 3) for i in range(3)),
            '_o_arml': tuple(round((-a[0], a[1], a[2])[i] - SPV['arml'][i], 3) for i in range(3)),
            'armr': T(r[0], 0, r[1]), 'arml': T(l[0], 0, l[1])}


S.POSES.update({
    'idle_a': SPZ(0.0, _show=('b_s',), head=T(4, 0, 6), jaw=T(8), **ARMS('s', (-34, -16), (-40, 16))),
    'idle_b': SPZ(0.0, _show=('b_s',), _face='happy', head=T(-8, 14, -10), jaw=T(14), **ARMS('s', (-44, -12), (-30, 20))),
    'hiss': SPZ(0.0, _face='hiss', _show=('b_s', 'tongue', 'mist'), head=T(-16), jaw=T(30), **ARMS('s', (-115, -45))),
    'strike_up': SPZ(0.0, _face='focus', _show=('b_s',), head=T(-28), jaw=T(16), **ARMS('s', (-70, -34))),
    'strike': SPZ(0.0, _face='hiss', _show=('b_lunge', 'tongue'), head=T(14), jaw=T(40), **ARMS('lunge', (-85, -18))),
    'coil': {'_face': 'focus', '_show': ('b_coil',), 'head': T(34), **ARMS('coil', (-58, 26))},
    'dive': {'_face': 'focus', '_show': ('b_dive',), 'head': T(0), 'root': T(68), **ARMS('dive', (62, -6))},
    'peek': {'_face': None, '_show': ('b_peek',), 'head': T(6, -10, 4), **ARMS('peek', (-72, 12))},
    'emerge': {'_face': 'happy', '_show': ('b_peek',), 'root': T(-6), 'head': T(10, 0, 8), **ARMS('peek', (-66, 14))},
    'divein': {'_face': 'focus', '_show': ('b_dive',), 'root': T(-8), 'head': T(4), **ARMS('dive', (58, -6))},
    'drape': {'_face': 'sleepy', '_show': ('b_drape',), 'head': T(14, -8, 6), **ARMS('drape', (-22, -14))},
    'helm': {'_face': 'happy', '_show': ('b_helm',), 'head': T(16, 34, -12), **ARMS('helm', (-30, 22))},
    'happy': SPZ(0.0, _face='happy', _show=('b_s',), head=T(-12, 0, 10), jaw=T(12), **ARMS('s', (-70, 30), (-70, -30))),
    'hurt': SPZ(0.0, _face='hurt', _show=('b_s',), head=T(-20, 20, 14), jaw=T(10), **ARMS('s', (-40, -60))),
})
S.DRAFT = ['idle_a', 'idle_b', 'hiss', 'strike_up', 'strike', 'happy', 'hurt']
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'legr': 'legs', 'shinr': 'legs', 'legl': 'legs', 'shinl': 'legs'}
SHINY = 'Shiny Starlit (deep blue plate, silver trim; a starry indigo serpent with silver eyes)'
SKIN_NAMES = {'_f': 'FREED (holy cosmetic): pale gold, gentler', '_s': 'SHINY Starlit'}
