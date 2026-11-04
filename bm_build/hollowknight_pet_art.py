"""(3.1 draft, stage 1: art only - not wired) THE HOLLOW STATUE KNIGHT - two in one: an Undercrown Statue Knight's armour (knight_art,
'dread') with a ghost bound inside it.

LORE (kept to phase169's Omega's Book and phase163's Pistachio): the spirit is SIR ALDOUS VANE, Captain of King Omega's palace
guard on Omega Island, who held the great stair beside his king in the War of Brothers and fell there. Apophiss "went away to
make other kings - hollow ones": he took the fallen guards' souls and bound them into the Dread's statue armour in the
Undercrown, to stand watch for a crown that wasn't theirs (the Statue Knights). Before the war, Pistachio was Sir Aldous's dog -
"Pip", a pup at his heel on the guard's rounds - until the Captain gave him to the King's household the night he rode to the
stair: "Mind the door, Pip." Pistachio has minded it for three hundred years. (Omega's own Ghost Guard - "GUARD! To your king!" -
is the rest of that guard.)

UNLOCK  Place a knight statue you've earned (knight_statue_dread - sneak + use to set it up), then call Pistachio and King
        Omega beside it (two of your three). Pistachio sniffs the plinth - and BARKS (his first bark in the pack: he's a butler);
        Omega: "...Aldous? Is that you in there?" The statue's eye-slit lights SOUL BLUE instead of red, and the armour kneels.

TWO IN ONE (two rigs, one follower)
  ARMOUR   knight_art's rig and geometry at companion size (0.5: ~1.5 blocks), its own finishes (FINISHES) on the dread build:
           'hollow' (the default: the Dread's black plate and bone, but the eyes and the chest jewel lit soul blue, the cloak re-dyed
           Omega's palace violet with a gold hem - the colours he died in), 'freed' (the holy cosmetic: polished silver plate, gold
           where the bone was, a white cloak, warm gold light), 'shiny' (Starlit: deep blue plate, silver trim, a pale gold soul).
           It swings the giant mace: knight_art's own poses - swing_0/1 (overhead slam), spin_0/1 (the spin), stagger - plus a
           kneel (sit_a: down on one knee, the mace planted - the vigil) and the statue stance (sit_b).
  SPIRIT   a translucent soul (SPIRIT, 'hs_', a fol5_kit rig): a young captain with a short beard and a scar, kind glowing eyes, the
           palace guard's violet tabard with Omega's gold crown on it, a short cape; no legs - he trails off into a wisp. A phantom
           sword. Poses: float, slip out (leaving the armour), HAUNT (arms out, a wail: foes slowed and weakened), DIVE (head first
           back into the armour), SLASH (fighting alone, while the armour is broken), sit (on the kneeling armour's knee).
  BROKEN   beaten down, the armour falls apart (the 'heap' pose: helm off, the mace dropped) and the spirit fights alone until it
           reassembles (30 s).
  FREED    (cosmetic) holy items - a Totem, a golden apple and a Pistachio-made dinner - "free" him: the 'freed' finish; the spirit
           shines gold, no longer bound (he stays because he wants to)."""
import math
import knight_art as KA
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, remap, blob

COMPANION = 0.5
FINISHES = ('hollow', 'freed', 'shiny')
_TAG = {'hollow': 'h', 'freed': 'f', 'shiny': 's'}
# recolours of the dread-live materials, by finish: each a luminance ramp (dark .. light), or None (kept)
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
        return out

    def models(self):
        out = {}
        for mid, (tex, els) in KA.models().items():
            if not mid.startswith('kn_dread_live_'): continue
            part = mid[len('kn_dread_live_'):]
            for fin in FINISHES:
                rn = lambda t: t.replace('kn_dl_', f'hk_{_TAG[fin]}_')
                fe = [dict(e, faces={f: dict(fc, texture='#' + rn(fc['texture'][1:])) for f, fc in e['faces'].items()}) for e in els]
                out[f'hk_{fin}_{part}'] = ({rn(k): rn(v) for k, v in tex.items()}, fe)
        return out


ARMOUR = Armour()


def _armour_poses():
    P = {}
    for n in ('idle_a', 'idle_b', 'walk_0', 'walk_1', 'swing_0', 'swing_1', 'spin_0', 'spin_1', 'stagger', 'statue', 'wake_0', 'wake_1'):
        P[n] = dict(KA.POSES[n])
    P['sit_a'] = dict(KA.POSES['death_0'])                   # (the vigil: down on one knee, the mace planted before him)
    P['sit_b'] = dict(KA.POSES['statue'])                    # (resting: the statue's stance, head bowed - the spirit out for a stretch)
    heap = dict(KA.POSES['death_1'])                         # BROKEN: slumped, the helm knocked off and rolled away, the mace dropped
    heap['_o_head'] = (7.0, -16.0, -10.0); heap['_o_mace'] = (-4.0, -6.0, -6.0)
    P['heap'] = heap
    return P


ARMOUR.POSES = _armour_poses()
ARMOUR.DRAFT = ['idle_a', 'walk_0', 'swing_0', 'swing_1', 'spin_0', 'spin_1', 'sit_a', 'sit_b', 'stagger', 'heap']


# ---------------------------------------------------------------------------------------------------- the spirit
SPV = {'torso': (0, 12.0, 0), 'head': (0, 19.0, 0), 'armr': (4.4, 18.0, 0), 'forer': (5.0, 13.6, 0), 'arml': (-4.4, 18.0, 0), 'forel': (-5.0, 13.6, 0),
       'wisp1': (0, 10.0, 0), 'wisp2': (0, 6.0, 0.6), 'sword': (5.4, 9.6, -0.6), 'wail': (0, 18.0, -6)}
SPP = {'torso': None, 'head': 'torso', 'armr': 'torso', 'forer': 'armr', 'arml': 'torso', 'forel': 'arml', 'wisp1': 'torso', 'wisp2': 'wisp1',
       'sword': 'forer', 'wail': 'head'}
SFACES = ('wail', 'blink', 'focus', 'happy')
SPIRIT = Rig('hs_', 0.75, SPV, SPP, SFACES, opt=('wail', 'sword'), companion=0.75)
GA = 150                                                    # (his alpha: see-through)
SC = {'soul': '#a8eeff', 'souldk': '#4aa8e0', 'tabard': '#6a40b0', 'gold': '#ffd870', 'eye': '#ffffff', 'blade': '#c8f4ff'}
SSKINS = {'_f': {'soul': '#fff4c8', 'souldk': '#e8b84a', 'tabard': '#f4f0e8', 'gold': '#ffd23a', 'eye': '#fff8e0', 'blade': '#fff0b0'},
          '_s': {'soul': '#ffe8a8', 'souldk': '#c89a3a', 'tabard': '#1a2a6a', 'gold': '#e0e8ff', 'eye': '#ffffff', 'blade': '#f0f4ff'}}


def _sface(kind, c):
    im, d = canvas(32); im.paste(coat(c['soul'], 71, 32, 0.04, 2, alpha=GA))
    dk = hexc(c['souldk'], 220); W = hexc(c['eye'])
    d.rectangle((0, 0, 31, 4), fill=dk)                                                      # (his hair, cropped short)
    for x0 in (7, 19):
        if kind == 'blink' or kind == 'happy':
            d.arc((x0, 11, x0 + 6, 17), 200 if kind == 'happy' else 20, 340 if kind == 'happy' else 160, fill=dk, width=2)
        elif kind == 'wail':
            d.ellipse((x0, 10, x0 + 6, 18), fill=dk); d.ellipse((x0 + 2, 12, x0 + 4, 15), fill=W)
        else:
            d.rectangle((x0, 12, x0 + 6, 15 if kind != 'focus' else 14), fill=W); d.rectangle((x0 + 2, 12, x0 + 4, 15 if kind != 'focus' else 14), fill=dk)
        d.line((x0, 9 if kind != 'focus' else 10, x0 + 6, 9), fill=dk, width=1)
    d.line((22, 6, 26, 12), fill=dk)                                                         # (the scar through his brow)
    for y in range(22, 30):                                                                  # (a short beard)
        for x in range(8, 24):
            if (x + y) % 2 and abs(x - 16) < 9 - (29 - y) * 0.2: im.putpixel((x, y), dk)
    if kind == 'wail': d.ellipse((13, 21, 19, 29), fill=hexc('#0a2a4a', 230))
    elif kind == 'happy': d.arc((11, 18, 21, 25), 20, 160, fill=hexc('#0a2a4a', 230), width=2)
    else: d.line((12, 23, 20, 23), fill=hexc('#0a2a4a', 230))
    return im


def _tabard(c):
    im = coat(c['tabard'], 72, 16, 0.05, 1, alpha=200); d = canvas(16)[1]
    from PIL import ImageDraw
    d = ImageDraw.Draw(im); g = hexc(c['gold'], 230)
    d.polygon([(4, 9), (4, 5), (6, 7), (8, 4), (10, 7), (12, 5), (12, 9)], fill=g)          # (Omega's crown, in gold)
    d.rectangle((0, 0, 15, 0), fill=g); d.rectangle((0, 15, 15, 15), fill=g)
    return im


def _stex(c):
    t = {'soul': coat(c['soul'], 73, 16, 0.05, 1, alpha=GA), 'souldk': coat(c['souldk'], 74, 16, 0.05, 1, alpha=GA), 'tabard': _tabard(c),
         'gold': coat(c['gold'], 75, 16, 0.05, 1, alpha=220), 'blade': coat(c['blade'], 76, 16, 0.04, 1, alpha=170), 'wail': coat(c['soul'], 77, 16, 0.1, 1, alpha=90)}
    t['face'] = _sface(None, c)
    for f in SFACES: t[f'face_{f}'] = _sface(f, c)
    return t


for k, v in _stex(SC).items(): SPIRIT.tex(k, v)
for sfx, ch in SSKINS.items():
    for k, v in _stex(dict(SC, **ch)).items(): SPIRIT.tex(k + sfx, v)
    SPIRIT.skin(sfx, {k: k + sfx for k in _stex(SC)})
B = SPIRIT.box
B('torso', (-3.8, 10.5, -2.2), (3.8, 18.6, 2.2), 'soul')
B('torso', (-3.9, 10.0, -2.35), (3.9, 18.2, -2.2), 'tabard', faces=('north',), uv={'north': [0, 0, 16, 16]})
B('torso', (-3.9, 10.0, 2.2), (3.9, 18.2, 2.35), 'tabard', faces=('south',), uv={'south': [0, 0, 16, 16]})
B('torso', (-4.6, 17.4, -2.4), (4.6, 18.8, 2.4), 'gold')                                    # (a gorget of light)
B('torso', (-4.0, 9.0, 2.0), (4.0, 18.4, 3.0), 'tabard', rot=('x', 10, (0, 18.4, 2.0)))          # (the short cape)
B('head', (-4.2, 18.8, -3.8), (4.2, 26.6, 3.8), 'soul')
B('head', (-4.25, 18.8, -3.85), (4.25, 26.6, -3.8), 'FACE', faces=('north',), uv={'north': [0, 0, 16, 16]}, light=10)
B('head', (-4.6, 25.4, -4.2), (4.6, 26.4, 4.2), 'gold')                                     # (the guard captain's circlet)
B('head', (-0.6, 26.4, -4.4), (0.6, 28.0, -3.4), 'gold')
for s, sx in (('r', 1), ('l', -1)):
    a, f = SPV['arm' + s], SPV['fore' + s]
    B('arm' + s, (a[0] - 1.1, f[1], -1.1), (a[0] + 1.1, a[1] + 0.6, 1.1), 'soul')
    B('fore' + s, (f[0] - 1.0, f[1] - 4.2, -1.0), (f[0] + 1.0, f[1] + 0.2, 1.0), 'souldk')
B('wisp1', (-3.0, 5.6, -1.8), (3.0, 10.6, 1.8), 'soul')
B('wisp2', (-1.6, 1.0, -1.0), (1.4, 6.0, 1.6), 'souldk')
B('wisp2', (-0.6, -1.0, -0.2), (0.6, 1.2, 1.0), 'soul')
sx_, sy_, sz_ = SPV['sword']
B('sword', (sx_ - 0.3, sy_ - 1.2, sz_ - 0.3), (sx_ + 0.3, sy_ + 0.6, sz_ + 0.3), 'gold')
B('sword', (sx_ - 1.4, sy_ + 0.6, sz_ - 0.3), (sx_ + 1.4, sy_ + 1.2, sz_ + 0.3), 'gold')
B('sword', (sx_ - 0.45, sy_ + 1.2, sz_ - 0.15), (sx_ + 0.45, sy_ + 11.0, sz_ + 0.15), 'blade', light=12)
for i in range(6):                                                                         # (the wail: rings of cold breath going out)
    r = 2.0 + i * 1.2; z = -6 - i * 1.6
    for a in range(0, 360, 60):
        x, y = r * math.cos(math.radians(a)), 22 + r * math.sin(math.radians(a))
        B('wail', (x - 0.5, y - 0.5, z - 0.2), (x + 0.5, y + 0.5, z + 0.2), 'wail')


def SP(lift=3.0, **kw):
    return SPIRIT.ground(kw, lift)


SPIRIT.POSES.update({
    'idle_a': SP(armr=limb(1, 0, 8), arml=limb(-1, 0, 8), forer=limb(1, 10), forel=limb(-1, 10), wisp1=T(8), wisp2=T(14)),
    'slip_out': SP(lift=4.0, _face='happy', torso=T(-10), armr=limb(1, 40, 30), arml=limb(-1, 40, 30), forer=limb(1, 30), forel=limb(-1, 30), wisp1=T(30), wisp2=T(30)),
    # HAUNT: arms flung out, a wail - rings of cold breath (foes slowed and weakened)
    'haunt': SP(lift=5.0, _face='wail', _show=('wail',), torso=T(-12), head=T(-10), armr=limb(1, 10, 100), arml=limb(-1, 10, 100), forer=limb(1, 0, 20),
                forel=limb(-1, 0, 20), wisp1=T(-10), wisp2=T(-20)),
    # DIVE: head first, arms ahead - back into the armour
    'dive': SP(lift=1.0, _face='focus', torso=T(110), head=T(-20), armr=limb(1, 170), arml=limb(-1, 170), forer=limb(1, 0), forel=limb(-1, 0), wisp1=T(-20), wisp2=T(-20)),
    # FIGHTING ALONE (the armour broken): the phantom sword, raised ... and cut down
    'slash_up': SP(_face='focus', _show=('sword',), torso=T(-6, -20), armr=limb(1, 150, 20), forer=limb(1, 40), arml=limb(-1, 20, 30), forel=limb(-1, 30)),
    'slash': SP(_face='focus', _show=('sword',), torso=T(16, 24), armr=limb(1, 60, -10), forer=limb(1, 10), arml=limb(-1, -10, 30), forel=limb(-1, 20), wisp1=T(-20)),
    'sit': SP(lift=0.0, _face='happy', torso=T(-4), armr=limb(1, 30, 10), arml=limb(-1, 30, 10), forer=limb(1, 50), forel=limb(-1, 50), wisp1=T(-80), wisp2=T(-20)),
    'happy': SP(lift=4.0, _face='happy', armr=limb(1, 0, 140), arml=limb(-1, 0, 140), forer=limb(1, 0, 20), forel=limb(-1, 0, 20), wisp1=T(20)),
})
SPIRIT.DRAFT = ['idle_a', 'slip_out', 'haunt', 'dive', 'slash_up', 'slash', 'sit', 'happy']
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head', 'legr': 'legs', 'shinr': 'legs', 'legl': 'legs', 'shinl': 'legs'}
SHINY = 'Shiny Starlit (deep blue plate, silver trim, a pale gold soul)'
