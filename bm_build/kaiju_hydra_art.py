"""(3.1 draft, stage 1: art only - not wired) TRIVYRN, THE THREE-WORLD WYRM - follower 63, the Kaiju trio's dragon (the design:
scratchpad/design_kaiju.md). An ORIGINAL three-headed wyrm: one body, three heads, and each head drank from a different world.

WHO  A wyrm hatched where the three worlds touch - and its heads never agreed on which one was home. SQUALL (the middle head)
     is the Overworld's storm: vain, bossy, sure it is in charge. CINDER (its right) is the Nether's fire: a hothead that snaps
     at everything, Squall most of all. HUSH (its left) is the End's quiet: dreamy, odd, half asleep, and the only one the
     other two are a little afraid of. The Atomic Rex's roar woke all three, and for once they agreed: that was a challenge.
LOOK (built to be nobody else's dragon - not gold, not bipedal, no twin tails)
       - A QUADRUPED: four planted legs, a deep barrel body, one heavy tail ending in a THREE-LOBED FAN (a lobe in each head's
         colour). Oxblood-maroon scales in overlapping rows (leaves()), a belly of pale bone scutes, bone spines down the back.
       - THE WINGS: great dusk-plum membranes on four fingers, folded along its flanks like a cloak when it walks; each wing's
         trailing edge rimmed in the three heads' colours (an aurora, not gold).
       - THREE NECKS, EACH ITS OWN WORLD: the necks' scales shade from the body's maroon into the head's own colours.
           SQUALL  the longest neck, the middle; a long wedge head, storm-jade scales, a crest of swept-back blades zig-zagged
                   like lightning with a yellow-white core; sharp slit eyes of electric yellow; yellow glow in the mouth.
           CINDER  thick, short, its right; a broad blunt bulldog head in basalt plates cracked with glowing magma, two great
                   curling RAM HORNS, a permanent toothy overbite; small round ember eyes deep under a scowling brow.
           HUSH    thin and long, its left; a slender eel-like head with no horns at all, pale End-stone lilac, FRILLED FINS
                   like chorus fronds, two drifting chin barbels; big pale MOON EYES, always half-lidded; a magenta glow.
       - Each head has ITS OWN EYES and its own expressions, and turns, bites and bickers on its own (per-head faces:
         a pose's '_face_<head part>' overrides '_face' for that head).
SCALE  RIG_SCALE 2.8 (the Atomic Rex's): ~7.8 blocks to Squall's crest with the heads up, ~14 nose to tail. COMPANION 0.9 (~2.5
       blocks): compsize twins the rig at COMPANION / RIG_SCALE, as the Rat King's (the hitbox follows).
RIG    body (root: the barrel and hips) - chest (the shoulders and the necks' roots) - n1s / n2s / hs / js (Squall: two neck
       segments, the head, the jaw), n1c / n2c / hc / jc (Cinder), n1h / n2h / hh / jh (Hush) - wr / wr2, wl / wl2 (the wings: the
       arm, the hand) - tail1 / tail2 / tail3 - legs: ufr lfr pfr, ufl lfl pfl (front: upper, lower, paw), thr shr ftr, thl shl ftl
       (hind: thigh, shin, foot) - saddle. fx (opt): fx_s fx_c fx_h (THE TRI-BREATH: storm, fire, void - each on its own head),
       ls lc lh (RANK III: the lightning streams, one from each head), strike (the bolt at the target), gust (the wing gust),
       aura (the rare aura).
SKINS  '_dw' DAWNSCALE (the cosmetic: rose-gold dawn scales... no: copper-and-cream - see the doc), '_ab' ABYSSAL (the
       cosmetic: deep-sea teal and black), '_sh' SHINY "Opal" (pearl-white scales, the three glows kept), '_ch' charged
       (Rank III's crackle: storm veins lit over every scale)."""
import math
import random
from PIL import Image, ImageDraw
from fol5_kit import (Rig, hexc, mix, mul, limb, T, cells, soft, lit, glow, put, strands, leaves, slab, stack, profile, cleaf, leaf,
                      ring, ghost, recolor, hue, eye, cat_eye, flame_eye, _ell, _rim, _curve, _thick, _vee, stroke, alpha, metal)
import rigkit
from rigkit import qs, qmul

# ---------------------------------------------------------------------------------------------------- the rig
HEADS = ('s', 'c', 'h')                         # Squall (middle), Cinder (its right), Hush (its left)
NAME = {'s': 'Squall', 'c': 'Cinder', 'h': 'Hush'}
NECK = {  # root, mid, head joint, head end (snout tip), widths (root, mid, top)
    's': ((0.0, 27.0, -13.0), (0.0, 35.0, -21.6), (0.0, 42.0, -29.0), (5.4, 4.6, 4.0)),
    'c': ((5.6, 26.0, -12.0), (13.0, 31.0, -19.6), (19.0, 35.6, -26.0), (6.4, 5.8, 5.2)),
    'h': ((-5.6, 26.0, -12.0), (-12.6, 32.6, -19.4), (-18.6, 39.0, -26.6), (4.4, 3.8, 3.2)),
}
PIVOT = {'body': (0, 22.0, 6.0), 'chest': (0, 23.0, -4.0),
         'tail1': (0, 23.0, 17.0), 'tail2': (0, 19.6, 30.0), 'tail3': (0, 14.2, 44.0),
         'ufr': (8.6, 22.0, -8.0), 'lfr': (9.4, 12.6, -7.4), 'pfr': (9.4, 3.6, -9.4),
         'ufl': (-8.6, 22.0, -8.0), 'lfl': (-9.4, 12.6, -7.4), 'pfl': (-9.4, 3.6, -9.4),
         'thr': (8.4, 22.0, 11.0), 'shr': (9.4, 12.6, 6.6), 'ftr': (9.4, 4.0, 12.4),
         'thl': (-8.4, 22.0, 11.0), 'shl': (-9.4, 12.6, 6.6), 'ftl': (-9.4, 4.0, 12.4),
         'wr': (6.6, 29.6, -5.0), 'wr2': (27.0, 37.0, 2.0), 'wl': (-6.6, 29.6, -5.0), 'wl2': (-27.0, 37.0, 2.0),
         'saddle': (0, 30.0, -2.0), 'strike': (0, 0.0, -70.0), 'gust': (0, 20.0, -30.0), 'aura': (0, 24.0, 0.0)}
PARENT = {'body': None, 'chest': 'body', 'tail1': 'body', 'tail2': 'tail1', 'tail3': 'tail2',
          'ufr': 'chest', 'lfr': 'ufr', 'pfr': 'lfr', 'ufl': 'chest', 'lfl': 'ufl', 'pfl': 'lfl',
          'thr': 'body', 'shr': 'thr', 'ftr': 'shr', 'thl': 'body', 'shl': 'thl', 'ftl': 'shl',
          'wr': 'chest', 'wr2': 'wr', 'wl': 'chest', 'wl2': 'wl', 'saddle': 'chest', 'strike': None, 'gust': None, 'aura': None}
for k, (root, mid, top, ws) in NECK.items():
    PIVOT[f'n1{k}'] = root; PIVOT[f'n2{k}'] = mid; PIVOT[f'h{k}'] = top
    PIVOT[f'j{k}'] = (top[0], top[1] - 1.4, top[2] - 2.6)
    PIVOT[f'fx_{k}'] = (top[0], top[1] - 0.6, top[2] - 12.0); PIVOT[f'l{k}'] = PIVOT[f'fx_{k}']
    PARENT[f'n1{k}'] = 'chest'; PARENT[f'n2{k}'] = f'n1{k}'; PARENT[f'h{k}'] = f'n2{k}'; PARENT[f'j{k}'] = f'h{k}'
    PARENT[f'fx_{k}'] = f'h{k}'; PARENT[f'l{k}'] = f'h{k}'
HEADP = tuple(f'h{k}' for k in HEADS)
FACES = ('fierce', 'happy', 'blink', 'hurt', 'wide', 'sleepy', 'smug', 'snarl')
OPT = ('fx_s', 'fx_c', 'fx_h', 'ls', 'lc', 'lh', 'strike', 'gust', 'aura')
RIG_SCALE = 2.4
COMPANION = 0.77


class HydraRig(Rig):
    """a Rig whose three heads each wear their own expression: '_face_<head part>' (else '_face') picks that head's model"""
    def model_name(self, p, pose=None, suffix=''):
        f = (pose.get('_face_' + p, pose.get('_face')) if pose else None)
        face = f'_x{f}' if pose and p in self.FACE_PARTS and f else ''
        return f'{self.PREFIX}{p}{face}{suffix}'


R = HydraRig('tw_', RIG_SCALE, PIVOT, PARENT, FACES, face_part=HEADP, opt=OPT, companion=COMPANION)
SKIN_NAMES = {'_dw': 'cosmetic: Dawnscale', '_ab': 'cosmetic: Abyssal', '_sh': 'SHINY: Opal', '_ch': 'charged (Rank III)'}

# ---------------------------------------------------------------------------------------------------- palette
BODY = dict(deep='#1c080e', dark='#341018', base='#521a22', light='#702c2c', shine='#90443a')
BONE = dict(deep='#5a4a36', dark='#8a7a5e', base='#bcac8a', light='#dccdaa', shine='#f2e8cc')
MEMB = dict(deep='#1a0a1a', dark='#2c1228', base='#421a36', light='#5c2848', shine='#7a3a58')
HP = {  # each head's own world: scales (deep, dark, base, light, shine) and its glow (dim, mid, hot, white)
    's': dict(deep='#16221e', dark='#263a34', base='#3a5a4c', light='#567e6a', shine='#7eaa90', g=('#a07a08', '#e8c018', '#fff070', '#fffde0')),
    'c': dict(deep='#140a08', dark='#261210', base='#3c1c16', light='#562a1e', shine='#743c26', g=('#8a2a04', '#e8600c', '#ffb030', '#fff0b0')),
    'h': dict(deep='#30263e', dark='#54476a', base='#80729a', light='#ab9fc4', shine='#d6ccea', g=('#7a1a8a', '#c040e0', '#f090ff', '#ffe8ff')),
}


# ---------------------------------------------------------------------------------------------------- textures (64 px, 2-px cells)
def scales(P, seed):
    """overlapping scale rows (the kit's leaves(): each scale lit at its tip, a scalloped shadow under it) - at low contrast,
    so a kaiju's hide reads as scales at 10 blocks and not as gravel"""
    return leaves((mix(P['base'], P['dark'], 0.65), P['base'], mix(P['base'], P['light'], 0.5), P['light']), seed)


def plates(P, seed, crack=None):
    """armour plates (Cinder's basalt): a brick of big plates, a lit top lip, a dark seam; glowing magma cracks if asked"""
    rnd = random.Random(seed); C = set()
    if crack:
        for _ in range(4):
            x, y = rnd.randrange(32), rnd.randrange(32)
            for i in range(rnd.randint(5, 10)):
                C.add((x % 32, y % 32)); x += rnd.choice((-1, 0, 1)); y += 1
    def c(x, y, r):
        if (x, y) in C: return crack[2] if (x + y) % 3 else crack[3]
        row = y // 8; k = y % 8; bx = (x + (row % 2) * 6) % 12
        if k == 7 or bx == 0: return P['deep']
        if k == 0: return P['light']
        if bx == 1: return mix(P['base'], P['light'], 0.4)
        return P['base']
    return cells(c, seed)


def scutes(P, seed):
    """the belly: bone scutes in bands, a lit top row, a dark seam, split staggered"""
    def c(x, y, r):
        k = y % 6; sx = (x + (y // 6) % 2 * 5) % 10
        if k == 5 or sx == 0: return P['dark']
        if k == 0: return P['light']
        return P['base']
    return cells(c, seed)


def bone(P, seed):
    def c(x, y, r):
        if y < 3: return P['shine']
        if x % 8 == 0: return P['dark']
        if x % 8 == 1: return P['light']
        return P['base'] if y < 26 else P['dark']
    return cells(c, seed)


def membrane(P, seed, rim=None):
    """a wing membrane: soft folds (a dark crease, a lit edge beside it, every 9 cells), veins, the rim's aurora along the bottom
    rows if given (the three heads' colours)"""
    def c(x, y, r):
        if rim and y >= 28: return rim[(x // 4) % len(rim)] if y >= 30 else mix(P['base'], rim[(x // 4) % len(rim)], 0.5)
        k = (x + y // 3) % 9
        if k == 0: return P['deep']
        if k == 1: return P['light']
        if (x * 3 + y) % 17 == 0: return P['shine']
        return P['base'] if y > 6 else P['dark']
    return cells(c, seed)


def glowtex(g, seed=0):
    def c(x, y, r):
        k = (x + y * 2) % 11
        return g[3] if k < 2 else g[2] if k < 6 else g[1]
    return cells(c, seed)


def mouth_tex(g):
    return cells(lambda x, y, r: g[1] if y % 8 == 0 else (mix(g[0], '#1a0606', 0.5) if (x // 4 + y // 8) % 2 else mix(g[0], '#1a0606', 0.7)), 0)


def tooth_tex():
    return cells(lambda x, y, r: '#fffaf0' if y < 6 else ('#e6dcc6' if x % 8 else '#b8ac94'), 0)


def frill(P, g, seed):
    """Hush's fins: thin pale membrane ribbed with fine magenta rays, its rim glowing"""
    def c(x, y, r):
        if y < 2 or x in (0, 31): return g[2]
        if x % 5 == 0: return mix(P['light'], g[1], 0.6)
        return P['light'] if y < 14 else P['shine']
    return cells(c, seed)


def zigzag_tex(g):
    """the lightning's own texture (full uv): a white-hot core, a yellow sheath"""
    return glow([g[3], g[3], g[2], g[1], g[0]], alpha=[255, 255, 240, 200, 120])


def fire_tex():
    return glow(['#ffffff', '#fff0a0', '#ffb030', '#e8600c', '#8a2a04'], alpha=[255, 250, 230, 190, 110])


def void_tex():
    return glow(['#ffffff', '#ffd8ff', '#f090ff', '#c040e0', '#4a0a5a'], alpha=[255, 245, 220, 180, 90])


def wind_tex():
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k, (y, a) in enumerate(((14, 200), (30, 170), (46, 140))):
        d.arc((4, y - 10, 60, y + 18), 200, 340, fill=hexc('#eaf4ff', a), width=3)
    return im


def ring_tex(col, a=210):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for r, w, c in ((30, 3, mix(col, '#ffffff', 0.5)), (24, 2, col)):
        d.ellipse((32 - r, 32 - r, 32 + r, 32 + r), outline=hexc(c, a), width=w)
    return im


# ---- the eyes: each head its own eye language (4 texels a unit, on a box on each side of its head, turned to look forward)
EYE_W = {'s': (4.0, 2.4), 'c': (3.0, 2.6), 'h': (4.0, 3.0)}           # (z length, height) of each head's eye box, units


def eye_s(kind=None):
    """SQUALL: a hawk's eye - a long sharp almond, all electric yellow, a slit pupil, a hard brow line slanting down to the snout
    (its default is SMUG: one lid lowered, superior)"""
    g = HP['s']['g']; w, h = (int(EYE_W['s'][0] * 4), int(EYE_W['s'][1] * 4))
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    k = {'smug': None, None: None, 'fierce': 'fierce', 'snarl': 'fierce', 'wide': 'greedy', 'happy': 'happy', 'blink': 'blink',
         'hurt': 'hurt', 'sleepy': 'sleepy'}[kind]
    lid = {'smug': 0.42, None: 0.3}.get(kind, 0.3)
    cat_eye(im, w // 2, 1, w - 1, h - 2, flip=True, kind=k, iris=(g[0], g[1], g[2], g[3], '#ffffff'), line='#0c1410', pupil='#081008',
            lid=lid, slant=-1.0 if kind == 'smug' else -0.4, pkind='slit', tilt=0.8, wing=True)
    return im


def eye_c(kind=None):
    """CINDER: a small round ember deep in the basalt - its features are LIGHT (the kit's flame eye), a heavy scowl over it
    (its default is SNARL)"""
    g = HP['c']['g']; w, h = (int(EYE_W['c'][0] * 4), int(EYE_W['c'][1] * 4))
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, w - 1, h - 1), fill=hexc('#120604'))
    k = {None: None, 'snarl': 'focus', 'fierce': 'focus', 'smug': None, 'wide': 'wow', 'happy': 'happy', 'blink': 'blink', 'hurt': 'hurt',
         'sleepy': 'sleepy'}[kind]
    flame_eye(im, w // 2, 1, w - 3, h - 2, flip=True, kind=k, core='#ffffff', halo=g[2], char=g[0])
    return im


def eye_h(kind=None):
    """HUSH: a big pale MOON EYE - glossy, all iris, lilac fading to white at its rim, a magenta pupil - always half-lidded
    (its default is SLEEPY: it is not asleep. It is watching.)"""
    g = HP['h']['g']; w, h = (int(EYE_W['h'][0] * 4), int(EYE_W['h'][1] * 4))
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    k = {None: 'sleepy', 'sleepy': 'sleepy', 'smug': 'sleepy', 'fierce': 'fierce', 'snarl': 'fierce', 'wide': 'wide', 'happy': 'happy',
         'blink': 'blink', 'hurt': 'hurt'}[kind]
    lid = {'sleepy': h * 0.45}.get(k)
    eye(im, w // 2, 1, w - 1, h - 2, flip=True, kind=k if k != 'sleepy' else None, iris=('#4a2a6a', '#8a6ab4', '#c8b4e8', '#eee4ff', '#ffffff'),
        lash='#2a1a3a', pupil=g[1], sclera=False, lid=lid, irk=0.62)
    return im


EYEFN = {'s': eye_s, 'c': eye_c, 'h': eye_h}


def _tex(B_=BODY, Bo=BONE, M=MEMB, H=HP, sfx=''):
    t = {'scale': scales(B_, 1), 'scale2': scales(dict(B_, base=B_['dark'], light=B_['base'], shine=B_['light']), 2),
         'belly': scutes(Bo, 3), 'bone': bone(Bo, 4), 'claw': bone(dict(Bo, base='#3a3030', light='#5a4e48', shine='#8a7e70', dark='#1a1414'), 5),
         'memb': membrane(M, 6), 'membr': membrane(M, 7, rim=(H['s']['g'][1], H['c']['g'][1], H['h']['g'][1])),
         'tooth': tooth_tex(), 'dark': cells(lambda x, y, r: '#120608', 0)}
    for k in HEADS:
        P = H[k]
        t[f'sc_{k}'] = scales(P, 10 + ord(k)); t[f'mix_{k}'] = scales({q: mix(B_[q], P[q], 0.5) for q in ('dark', 'base', 'light', 'shine')}, 20 + ord(k))
        t[f'glow_{k}'] = glowtex(P['g']); t[f'mouth_{k}'] = mouth_tex(P['g'])
        t[f'eye_{k}'] = EYEFN[k]()
        for f in FACES: t[f'eye_{k}_{f}'] = EYEFN[k](f)
    t['plate_c'] = plates(H['c'], 31, crack=H['c']['g']); t['frill_h'] = frill(H['h'], H['h']['g'], 32)
    t['horn_c'] = bone(dict(Bo, base='#4a3a30', light='#6a5848', shine='#a08a6a', dark='#2a2018'), 33)
    t['blade_s'] = metal((H['s']['dark'], H['s']['base'], H['s']['light'], H['s']['shine']), 34)
    t['fan_s'] = membrane(H['s'], 35, rim=(H['s']['g'][2],)); t['fan_c'] = membrane(H['c'], 36, rim=(H['c']['g'][2],)); t['fan_h'] = membrane(H['h'], 37, rim=(H['h']['g'][2],))
    return t


TEX = _tex()
TEX.update({'zap': zigzag_tex(HP['s']['g']), 'fire': fire_tex(), 'void': void_tex(), 'wind': wind_tex(),
            'ring': ring_tex(HP['s']['g'][2]), 'leather': cells(lambda x, y, r: '#d8c090' if y in (2, 29) and x % 3 == 0 else ('#4a2e22' if (x // 6 + y // 5) % 5 else '#3a241a'), 40),
            'brass': lit(cells(lambda x, y, r: '#b08a3a' if (x + y) % 7 else '#d8b05a', 0), 1.3, 0.8, 6),
            'aura': glow(['#ffffff', HP['s']['g'][2], HP['h']['g'][2], HP['c']['g'][1]], alpha=[230, 210, 170, 0]),
            'mote_s': glow([HP['s']['g'][3], HP['s']['g'][2], HP['s']['g'][1]], alpha=[255, 220, 0]),
            'mote_c': glow([HP['c']['g'][3], HP['c']['g'][2], HP['c']['g'][1]], alpha=[255, 220, 0]),
            'mote_h': glow([HP['h']['g'][3], HP['h']['g'][2], HP['h']['g'][1]], alpha=[255, 220, 0])})
for k, v in TEX.items(): R.tex(k, v)
GLOW = {f'glow_{k}': 13 for k in HEADS} | {'zap': 15, 'fire': 15, 'void': 15, 'aura': 15, 'mote_s': 15, 'mote_c': 15, 'mote_h': 15}

# ---------------------------------------------------------------------------------------------------- helpers
B = R.box
SEG = R.seg


def zoct(part, z0, z1, hw, hh, tex, c=(0.0, 0.0), k=0.68, light=0, under=None):
    x, y = c
    es = [B(part, (x - hw, y - hh * k, z0), (x + hw, y + hh * k, z1), tex, light=light),
          B(part, (x - hw * k, y + hh * k, z0), (x + hw * k, y + hh, z1), tex, light=light),
          B(part, (x - hw * k, y - hh, z0), (x + hw * k, y - hh * k, z1), tex, light=light)]
    if under:
        for f in es[2]['faces'].values(): f['texture'] = '#' + under
    return es


def zmass(part, rows, tex, under=None):
    """a body along z: rows of (z0, z1, half-width, half-height, y centre[, x centre]) - each an octagon section, split in two
    when wider than 16 units (4 texels a unit on a kaiju)"""
    out = []
    for r in rows:
        z0, z1, hw, hh, yc = r[:5]; xc = r[5] if len(r) > 5 else 0.0
        if 2 * hw > 16:
            for sx in (1, -1):
                lo, hi = sorted((xc, xc + sx * hw))
                out.append(B(part, (lo, yc - hh * 0.68, z0), (hi, yc + hh * 0.68, z1), tex))
                lo, hi = sorted((xc, xc + sx * hw * 0.68))
                out.append(B(part, (lo, yc + hh * 0.68, z0), (hi, yc + hh, z1), tex))
                e = B(part, (lo, yc - hh, z0), (hi, yc - hh * 0.68, z1), tex); out.append(e)
                if under:
                    for f in e['faces'].values(): f['texture'] = '#' + under
        else:
            out += zoct(part, z0, z1, hw, hh, tex, c=(xc, yc), under=under)
    return out


def rod(part, pts, ws, tex, front=(0.0, 0.0, -1.0), k=0.78, ext=0.2, light=0, texs=None):
    f2 = (0.7, 0.0, -0.7) if abs(front[0]) < 0.5 else (0.7, 0.0, 0.7)
    out = []
    for i in range(len(pts) - 1):
        w = (ws[i] + ws[i + 1]) / 2; t = texs[i] if texs else tex
        out.append(SEG(part, pts[i], pts[i + 1], w, w, t, front, ext=ext, light=light))
        out.append(SEG(part, pts[i], pts[i + 1], w * k * 1.12, w * k * 1.12, t, f2, ext=ext * 0.4, light=light))
    return out


def spike(part, base, tip, w, tex='bone', light=0):
    P = lambda s: tuple(base[i] + (tip[i] - base[i]) * s for i in range(3))
    d = [tip[i] - base[i] for i in range(3)]
    up = (0.0, 0.0, -1.0) if abs(d[1]) > 0.6 * math.sqrt(sum(v * v for v in d)) else (0.0, 1.0, 0.0)
    SEG(part, P(0.0), P(0.5), w, w, tex, up, ext=0.1, light=light)
    SEG(part, P(0.48), P(0.82), w * 0.62, w * 0.62, tex, up, ext=0.05, light=light)
    SEG(part, P(0.8), P(1.0), w * 0.3, w * 0.3, tex, up, light=light)


def panel(part, O, P1, P2, tex, n=3, t=0.3, light=0):
    M = tuple((P1[i] + P2[i]) / 2 for i in range(3))
    e1 = [P1[i] - O[i] for i in range(3)]; e2 = [P2[i] - O[i] for i in range(3)]
    nrm = (e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0])
    L = math.sqrt(sum(v * v for v in nrm)) or 1.0; nrm = tuple(v / L for v in nrm)
    W = math.dist(P1, P2); out = []
    for i in range(n):
        a, b = i / n, (i + 1) / n
        A_ = tuple(O[k] + (M[k] - O[k]) * a for k in range(3)); B_ = tuple(O[k] + (M[k] - O[k]) * b for k in range(3))
        out.append(SEG(part, A_, B_, max(0.4, W * (a + b) / 2 * 0.98), t, tex, nrm, ext=0.0, light=light, full=True))
    return out


def capture(part, fn):
    n, m = len(R._els[part]), len(R._pts[part])
    fn()
    els = R._els[part][n:]; del R._els[part][n:]; del R._pts[part][m:]
    return els


def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


# ---------------------------------------------------------------------------------------------------- the body: a deep barrel
zmass('body', [(-4.6, 0.0, 9.0, 7.6, 22.6), (0.0, 5.0, 9.2, 7.6, 22.4), (5.0, 10.0, 8.8, 7.2, 22.2), (10.0, 14.6, 8.2, 6.8, 22.4),
               (14.6, 18.4, 6.8, 5.8, 22.8)], 'scale', under='belly')
for z in (-3.0, 1.6, 6.2, 10.8):                                                    # (bone scute bands across the belly, proud)
    B('body', (-5.6, 14.6, z), (5.6, 15.2, z + 3.6), 'belly')
for i, (z, h) in enumerate(((-2.4, 4.6), (1.8, 4.0), (6.0, 3.6), (10.0, 3.2), (14.0, 2.8))):     # (the dorsal spines)
    y = 30.4 - i * 0.2
    spike('body', (0, y - 0.8, z), (0, y + h, z + 1.6), 1.6 - i * 0.12)
for sx in (1, -1):                                                                  # (the flanks: a darker band where the wings lie)
    lo, hi = sorted((sx * 8.6, sx * 9.6)); B('body', (lo, 20.0, -3.0), (hi, 26.0, 13.0), 'scale2')

# ---- the chest: the shoulders, the necks' roots in a fan, the keel of the breast
zmass('chest', [(-14.0, -10.0, 7.6, 7.2, 24.0), (-10.0, -4.4, 9.0, 7.8, 23.2)], 'scale', under='belly')
B('chest', (-5.0, 15.6, -13.0), (5.0, 17.0, -5.0), 'belly')
zoct('chest', -16.8, -12.0, 6.8, 4.8, 'scale', c=(0.0, 26.0))                       # (the fan of the necks' roots)
for i, (z, h) in enumerate(((-11.0, 3.4), (-7.0, 4.4))):
    spike('chest', (0, 30.0, z), (0, 30.0 + h, z + 1.6), 1.4)
for sx in (1, -1):
    stack(R, 'chest', profile(17.0, 12.0, 4.6, n=4), 'scale', c=(sx * 8.4, -7.6))   # (the shoulders)

# ---------------------------------------------------------------------------------------------------- the necks
def neck(k):
    root, mid, top, (w0, w1, w2) = NECK[k]
    P = HP[k]
    n1, n2 = f'n1{k}', f'n2{k}'
    for part, A_, B_, wa, wb, tex in ((n1, root, mid, w0, w1, f'mix_{k}'), (n2, mid, top, w1, w2, f'sc_{k}')):
        L = math.dist(A_, B_); n = max(2, int(L / 2.6))
        for i in range(n):
            a = lerp(A_, B_, i / n); b = lerp(A_, B_, (i + 1) / n); w = wa + (wb - wa) * (i + 0.5) / n
            SEG(part, a, b, w, w, tex, (0.0, 0.0, -1.0), ext=0.35)                  # (ringed: each segment a little proud of the next)
            SEG(part, a, b, w * 0.86, w * 0.86, tex, (0.7, 0.0, -0.7), ext=0.15)
            d = [b[j] - a[j] for j in range(3)]; m = math.sqrt(sum(v * v for v in d)); d = [v / m for v in d]
            fr = (0.0, -d[2] * 0.0 + d[1] * 0.0, -1.0)
            c = lerp(a, b, 0.5)
            # the throat's scutes, pale, down its front
            SEG(part, (c[0], c[1], c[2] - w * 0.5), (c[0] + d[0] * 1.4, c[1] + d[1] * 1.4, c[2] - w * 0.5 + d[2] * 1.4), w * 0.62, 0.4, 'belly', (0.0, 0.0, -1.0))
            # its dorsal crest along its back: each head's own
            back = (c[0] - 0.0, c[1] + 0.2, c[2] + w * 0.5)
            if k == 's':
                SEG(part, back, (back[0], back[1] + 1.2, back[2] + 2.0), 0.5, 1.8, 'blade_s', (1.0, 0.0, 0.0))
                SEG(part, back, (back[0], back[1] + 0.9, back[2] + 1.5), 0.6, 0.7, f'glow_{k}', (1.0, 0.0, 0.0), light=13)
            elif k == 'c':
                B(part, (c[0] - w * 0.36, c[1] - 0.8, c[2] + w * 0.36), (c[0] + w * 0.36, c[1] + 0.8, c[2] + w * 0.56), 'plate_c', light=0)
                spike(part, back, (back[0], back[1] + 1.4, back[2] + 1.6), 0.9, 'horn_c')
            else:
                SEG(part, back, (back[0], back[1] + 0.6, back[2] + 2.0), 0.3, 1.6, 'frill_h', (1.0, 0.0, 0.0))


for k in HEADS: neck(k)


# ---------------------------------------------------------------------------------------------------- the heads
def eyes(part, k, face, c, side_yaw=26.0):
    """the head's two eyes: a box on each side at c (its right one; the left mirrored), turned side_yaw toward the front so they
    read from ahead; the texture its own eye language, per expression; light 12"""
    L, Hh = EYE_W[k]
    tex = f'eye_{k}' if face is None else f'eye_{k}_{face}'
    x, y, z = c; hx = PIVOT[part][0]
    for sx in (1, -1):
        X = hx + sx * x
        lo, hi = sorted((X, X + sx * 0.04))
        fc = 'east' if sx > 0 else 'west'
        B(part, (lo, y, z - L / 2), (hi, y + Hh, z + L / 2), tex, faces=(fc,), uv={fc: [0, 0, L, Hh] if sx > 0 else [L, 0, 0, Hh]},
          rot=('y', side_yaw * sx, (X, y, z)) if side_yaw else None, light=12)


def head_s(face=None):
    """SQUALL: a long wedge, a crest of swept-back lightning blades"""
    p = 'hs'; x0, y0, z0 = PIVOT[p]
    zmass(p, [(z0 - 3.4, z0 + 1.6, 3.6, 3.0, y0 + 0.6), (z0 - 7.4, z0 - 3.4, 3.0, 2.5, y0 + 0.2), (z0 - 11.0, z0 - 7.4, 2.3, 1.8, y0 - 0.2)], 'sc_s', under='belly')
    B(p, (-1.7, y0 - 0.9, z0 - 12.0), (1.7, y0 + 0.7, z0 - 10.8), 'sc_s')              # (the snout's tip)
    B(p, (-1.9, y0 - 2.0, z0 - 11.2), (1.9, y0 - 1.6, z0 - 1.0), f'mouth_s', light=6)
    for i in range(7):                                                               # (fangs down the upper jaw)
        z = z0 - 10.6 + i * 1.3
        for sx in (1, -1):
            SEG(p, (sx * (1.6 + i * 0.12), y0 - 1.7, z), (sx * (1.5 + i * 0.12), y0 - 2.7 + abs(i - 2) * 0.1, z - 0.2), 0.36, 0.36, 'tooth')
    tilt = {'fierce': 14, 'snarl': 14, 'smug': 6, 'wide': -10, 'happy': -6, 'hurt': 10, 'sleepy': 2}.get(face, 0)
    for sx in (1, -1):                                                               # (the brow: a hard ridge, slanting at the snout)
        r = ('x', -tilt, (sx * 2.8, y0 + 2.4, z0 - 4.2))
        lo, hi = sorted((sx * 1.4, sx * 3.7)); B(p, (lo, y0 + 1.9, z0 - 6.4), (hi, y0 + 2.9, z0 - 2.4), 'sc_s', rot=r)
        if face == 'smug' and sx < 0:                                                 # (one brow up: superior)
            B(p, (min(sx * 1.6, sx * 3.6), y0 + 3.0, z0 - 6.0), (max(sx * 1.6, sx * 3.6), y0 + 3.4, z0 - 3.0), 'blade_s')
    eyes(p, 's', face, (3.06, y0 - 0.6, z0 - 5.4), side_yaw=0.0)
    for sx in (1, -1):                                                               # THE CREST: lightning blades, zig-zagged back
        pts = [(sx * 1.6, y0 + 2.4, z0 - 2.6), (sx * 2.6, y0 + 5.0, z0 + 0.2), (sx * 2.0, y0 + 5.6, z0 + 2.0), (sx * 3.4, y0 + 8.6, z0 + 5.4)]
        for a, b, w in zip(pts, pts[1:], (1.3, 1.0, 0.8)):
            SEG(p, a, b, 0.6, w * 1.6, 'blade_s', (sx * 1.0, 0.0, 0.0), ext=0.2)
            SEG(p, a, b, 0.7, w * 0.6, 'glow_s', (sx * 1.0, 0.0, 0.0), light=13)
    SEG(p, (0, y0 + 3.0, z0 - 1.0), (0, y0 + 6.4, z0 + 4.2), 0.6, 1.8, 'blade_s', (1.0, 0.0, 0.0))
    for sx in (1, -1):
        lo, hi = sorted((sx * 0.5, sx * 1.4)); B(p, (lo, y0 + 0.0, z0 - 12.05), (hi, y0 + 0.5, z0 - 11.95), 'dark')    # (nostrils)


def head_c(face=None):
    """CINDER: broad and blunt, basalt plates cracked with magma, two great curling ram horns, the overbite"""
    p = 'hc'; x0, y0, z0 = PIVOT[p]
    zmass(p, [(z0 - 3.0, z0 + 2.0, 4.6, 3.6, y0 + 0.4, x0), (z0 - 6.6, z0 - 3.0, 4.2, 3.0, y0 + 0.0, x0), (z0 - 9.0, z0 - 6.6, 3.6, 2.6, y0 - 0.2, x0)], 'plate_c', under='sc_c')
    B(p, (x0 - 3.2, y0 - 1.8, z0 - 9.4), (x0 + 3.2, y0 + 1.4, z0 - 8.8), 'plate_c')          # (the blunt nose)
    B(p, (x0 - 2.6, y0 - 2.6, z0 - 8.8), (x0 + 2.6, y0 - 2.2, z0 - 1.0), 'mouth_c', light=7)
    for sx in (1, -1):                                                                   # (jowls)
        lo, hi = sorted((x0 + sx * 3.6, x0 + sx * 4.8)); B(p, (lo, y0 - 3.0, z0 - 7.0), (hi, y0 - 0.4, z0 - 1.2), 'sc_c')
    for i in range(5):                                                                   # (THE OVERBITE: fangs over the lower lip)
        z = z0 - 8.6 + i * 1.5
        for sx in (1, -1):
            L = 1.7 if i in (0, 2) else 1.1
            SEG(p, (x0 + sx * (2.3 + i * 0.15), y0 - 2.3, z), (x0 + sx * (2.3 + i * 0.15), y0 - 2.3 - L, z - 0.3), 0.55, 0.55, 'tooth')
    tilt = {None: 16, 'snarl': 22, 'fierce': 26, 'smug': 12, 'wide': -6, 'happy': 4, 'hurt': 18, 'sleepy': 8}.get(face, 16)
    for sx in (1, -1):                                                                   # (the scowling brow: a heavy basalt plate per eye)
        r = ('z', -tilt * sx, (x0 + sx * 1.0, y0 + 3.0, z0 - 6.0))
        lo, hi = sorted((x0 + sx * 0.6, x0 + sx * 4.4)); B(p, (lo, y0 + 2.4, z0 - 7.4), (hi, y0 + 3.8, z0 - 3.6), 'plate_c', rot=r)
    eyes(p, 'c', face, (4.26, y0 - 0.6, z0 - 4.8), side_yaw=0.0)
    for sx in (1, -1):                                                                   # THE RAM HORNS: curling back, out, down and forward
        c0 = (x0 + sx * 3.4, y0 + 2.6, z0 + 0.4)
        pts = [c0, (x0 + sx * 5.6, y0 + 5.2, z0 + 2.4), (x0 + sx * 8.2, y0 + 5.4, z0 + 3.6), (x0 + sx * 9.6, y0 + 3.0, z0 + 2.4),
               (x0 + sx * 9.2, y0 + 0.4, z0 - 0.4), (x0 + sx * 8.4, y0 - 0.8, z0 - 2.6)]
        ws = (2.6, 2.4, 2.0, 1.6, 1.2, 0.7)
        for a, b, w in zip(pts, pts[1:], ws):
            SEG(p, a, b, w, w, 'horn_c', (0.0, 1.0, 0.0), ext=0.3)
    for sx in (1, -1):                                                                   # (smoking nostrils: a glow in each)
        lo, hi = sorted((x0 + sx * 0.8, x0 + sx * 2.0)); B(p, (lo, y0 + 0.0, z0 - 9.45), (hi, y0 + 0.8, z0 - 9.38), 'glow_c', light=12)


def head_h(face=None):
    """HUSH: a slender eel-like head, frilled fins like chorus fronds, chin barbels, big pale moon eyes"""
    p = 'hh'; x0, y0, z0 = PIVOT[p]
    zmass(p, [(z0 - 3.6, z0 + 1.4, 2.8, 2.6, y0 + 0.6, x0), (z0 - 7.8, z0 - 3.6, 2.6, 2.6, y0 + 0.3, x0), (z0 - 11.4, z0 - 7.8, 1.7, 1.5, y0 - 0.1, x0)], 'sc_h', under='belly')
    B(p, (x0 - 1.1, y0 - 0.9, z0 - 12.4), (x0 + 1.1, y0 + 0.6, z0 - 11.2), 'sc_h')
    B(p, (x0 - 1.4, y0 - 1.65, z0 - 11.6), (x0 + 1.4, y0 - 1.3, z0 - 3.0), 'mouth_h', light=6)
    for i in range(8):                                                                   # (fine needle teeth)
        z = z0 - 11.2 + i * 1.0
        for sx in (1, -1): SEG(p, (x0 + sx * 1.2, y0 - 1.4, z), (x0 + sx * 1.15, y0 - 2.0, z), 0.22, 0.22, 'tooth')
    eyes(p, 'h', face, (2.66, y0 - 1.2, z0 - 5.7), side_yaw=0.0)
    lid = {None: 0.5, 'sleepy': 0.5, 'smug': 0.5, 'fierce': 0.2, 'snarl': 0.2}.get(face)
    for sx in (1, -1):                                                                   # THE FRILLS: three fan fins each side, and a crest
        for j, (dy, dz, L, a) in enumerate(((1.6, 0.4, 5.6, 30), (0.2, 1.6, 6.4, 0), (-1.4, 0.8, 5.0, -26))):
            b0 = (x0 + sx * 2.2, y0 + dy, z0 + dz)
            tip = (x0 + sx * (2.2 + L * 0.55), y0 + dy + L * math.sin(math.radians(a)) * 0.8, z0 + dz + L * 0.8)
            panel(p, b0, tip, (tip[0] - sx * 0.6, tip[1] - 1.6, tip[2] + 0.6), 'frill_h', n=2, t=0.25)
            SEG(p, b0, tip, 0.35, 0.35, 'glow_h', (0.0, 1.0, 0.0), light=12)
    for j in range(3):
        z = z0 - 3.0 + j * 2.4
        SEG(p, (x0, y0 + 2.4, z), (x0, y0 + 4.6 - j * 0.4, z + 2.2), 0.3, 2.0, 'frill_h', (1.0, 0.0, 0.0))
    for sx in (1, -1):                                                                   # (the chin barbels, drifting)
        a = (x0 + sx * 0.9, y0 - 1.8, z0 - 9.6); b = (x0 + sx * 1.4, y0 - 4.4, z0 - 8.4); c = (x0 + sx * 2.2, y0 - 6.0, z0 - 6.8)
        SEG(p, a, b, 0.4, 0.4, 'sc_h', (0.0, 0.0, -1.0)); SEG(p, b, c, 0.3, 0.3, 'glow_h', (0.0, 0.0, -1.0), light=12)


HEADFN = {'s': head_s, 'c': head_c, 'h': head_h}
for k in HEADS:
    HEADFN[k]()
    for f in FACES:
        R.face_els(f'h{k}', f, capture(f'h{k}', lambda k=k, f=f: HEADFN[k](f)))


def jaw(k):
    p = f'j{k}'; x0, y0, z0 = PIVOT[f'h{k}']
    L = {'s': 11.0, 'c': 8.6, 'h': 11.0}[k]; w = {'s': 2.0, 'c': 3.6, 'h': 1.4}[k]
    tex = {'s': 'sc_s', 'c': 'plate_c', 'h': 'sc_h'}[k]
    B(p, (x0 - w, y0 - 3.6, z0 - L), (x0 + w, y0 - 2.1, z0 - 0.6), tex)
    B(p, (x0 - w * 0.8, y0 - 4.1, z0 - L + 1.0), (x0 + w * 0.8, y0 - 3.5, z0 - 1.4), 'belly')
    B(p, (x0 - w * 0.8, y0 - 2.15, z0 - L + 0.6), (x0 + w * 0.8, y0 - 1.95, z0 - 1.0), f'mouth_{k}', light=6)
    n = int(L / 1.3)
    for i in range(n):
        z = z0 - L + 0.8 + i * 1.3
        for sx in (1, -1): SEG(p, (x0 + sx * (w - 0.35), y0 - 2.0, z), (x0 + sx * (w - 0.4), y0 - 1.2, z), 0.32, 0.32, 'tooth')


for k in HEADS: jaw(k)

# ---------------------------------------------------------------------------------------------------- the legs
def front(sx):
    u, l, p = ('ufr', 'lfr', 'pfr') if sx > 0 else ('ufl', 'lfl', 'pfl')
    S, E, W = PIVOT[u], PIVOT[l], PIVOT[p]
    rod(u, [S, E], [6.8, 5.4], 'scale')
    stack(R, u, profile(E[1] + 2.0, 8.0, 4.0, n=3), 'scale', c=(S[0], S[2] + 0.4))
    rod(l, [E, W], [5.0, 4.2], 'scale')
    B(l, (E[0] - 1.6, E[1] - 6.0, E[2] - 2.8), (E[0] + 1.6, E[1] - 0.4, E[2] - 2.2), 'belly')
    spike(l, (E[0], E[1] - 0.4, E[2] + 2.0), (E[0], E[1] - 1.6, E[2] + 4.4), 1.0, 'bone')            # (an elbow spur)
    x, y, z = W
    B(p, (x - 3.0, 0.0, z - 3.0), (x + 3.0, 3.6, z + 2.4), 'scale')
    for i, dx in enumerate((-2.0, -0.6, 0.8, 2.2)):
        tip = (x + dx * 1.2, 0.6, z - 6.4 + abs(dx) * 0.5)
        SEG(p, (x + dx, 1.4, z - 2.6), tip, 1.3, 1.3, 'scale', (0.0, 1.0, 0.0), ext=0.2)
        spike(p, tip, (tip[0] + dx * 0.2, 0.0, tip[2] - 1.8), 0.9, 'claw')


def hind(sx):
    t, s, f = ('thr', 'shr', 'ftr') if sx > 0 else ('thl', 'shl', 'ftl')
    H_, K_, A_ = PIVOT[t], PIVOT[s], PIVOT[f]
    stack(R, t, profile(K_[1] + 1.0, 12.0, 5.4, n=4, d=1.2), 'scale', c=(H_[0] + sx * 0.4, (H_[2] + K_[2]) / 2 + 0.6))
    rod(t, [H_, K_], [7.4, 6.0], 'scale')
    rod(s, [K_, A_], [5.2, 4.0], 'scale')
    B(s, (K_[0] - 1.8, K_[1] - 1.4, K_[2] - 3.0), (K_[0] + 1.8, K_[1] + 1.6, K_[2] - 2.0), 'bone')     # (the knee's cap)
    x, y, z = A_
    rod(f, [(x, y, z), (x, 1.8, z - 4.0)], [3.8, 3.4], 'scale')
    B(f, (x - 3.0, 0.0, z - 6.4), (x + 3.0, 2.4, z - 1.6), 'scale')
    for i, dx in enumerate((-1.8, 0.0, 1.8)):
        tip = (x + dx * 1.3, 0.6, z - 10.0 + abs(dx) * 0.4)
        SEG(f, (x + dx, 1.2, z - 5.0), tip, 1.5, 1.4, 'scale', (0.0, 1.0, 0.0), ext=0.2)
        spike(f, tip, (tip[0] + dx * 0.2, 0.0, tip[2] - 2.0), 1.0, 'claw')
    spike(f, (x, 1.0, z + 0.6), (x, 0.2, z + 3.2), 0.9, 'claw')                                    # (the dew claw, behind)


front(1); front(-1); hind(1); hind(-1)

# ---------------------------------------------------------------------------------------------------- the tail, its three-lobed fan
TAILPTS = [PIVOT['tail1'], PIVOT['tail2'], PIVOT['tail3'], (0, 10.4, 56.0)]
TW = [(6.4, 5.2), (5.2, 3.8), (3.8, 2.4)]
for i, part in enumerate(('tail1', 'tail2', 'tail3')):
    a, b = TAILPTS[i], TAILPTS[i + 1]; w0, w1 = TW[i]
    if i:                                                                               # (the knuckle: a collar so a bend never opens)
        d = [b[j] - a[j] for j in range(3)]; m = math.sqrt(sum(v * v for v in d)); d = [v / m for v in d]
        SEG(part, tuple(a[j] - d[j] * 1.4 for j in range(3)), tuple(a[j] + d[j] * 1.4 for j in range(3)), TW[i - 1][1] * 1.02, TW[i - 1][1] * 1.02, 'scale', (0.0, 1.0, 0.0))
    rod(part, [a, lerp(a, b, 0.5), b], [w0, (w0 + w1) / 2, w1], 'scale', front=(0.0, 1.0, 0.0))
    for t in (0.3, 0.75):
        c = lerp(a, b, t); w = w0 + (w1 - w0) * t
        spike(part, (c[0], c[1] + w * 0.4, c[2]), (c[0], c[1] + w * 0.4 + 2.4 - i * 0.5, c[2] + 1.6), 1.2 - i * 0.2)
        B(part, (c[0] - w * 0.36, c[1] - w * 0.56, c[2] - 1.4), (c[0] + w * 0.36, c[1] - w * 0.4, c[2] + 1.4), 'belly')
tip = TAILPTS[3]
for j, (k, ang) in enumerate((('s', 0.0), ('c', 50.0), ('h', -50.0))):                  # THE FAN: a lobe in each head's colour
    a = math.radians(ang); L = 10.4 if k == 's' else 8.8
    end = (tip[0] + L * math.sin(a), tip[1] + 1.0 + (2.4 if k == 's' else 0.0), tip[2] + L * math.cos(a) * 0.9)
    side = (tip[0] + L * 0.6 * math.sin(a) + 2.4 * math.cos(a), tip[1] + 0.6, tip[2] + L * 0.6 * math.cos(a) - 2.4 * math.sin(a))
    side2 = (tip[0] + L * 0.6 * math.sin(a) - 2.4 * math.cos(a), tip[1] + 0.6, tip[2] + L * 0.6 * math.cos(a) + 2.4 * math.sin(a))
    panel('tail3', (tip[0], tip[1], tip[2] - 1.0), side, end, f'fan_{k}', n=2, t=0.35)
    panel('tail3', (tip[0], tip[1], tip[2] - 1.0), end, side2, f'fan_{k}', n=2, t=0.35)
    SEG('tail3', tip, end, 0.6, 0.6, f'glow_{k}', (0.0, 1.0, 0.0), light=13)

# ---------------------------------------------------------------------------------------------------- the wings (built spread)
for a, h, sx in (('wr', 'wr2', 1), ('wl', 'wl2', -1)):
    S = lambda v: (sx * v[0], v[1], v[2])
    SH, EL, WR = S((6.6, 29.6, -5.0)), S((17.0, 34.0, -1.6)), S((27.0, 37.0, 2.0))
    rod(a, [SH, EL], [3.2, 2.6], 'scale'); rod(a, [EL, WR], [2.6, 2.0], 'scale')
    stack(R, a, [(EL[1] - 1.4, EL[1] + 1.4, 1.6)], 'scale', c=(EL[0], EL[2]))
    panel(a, SH, WR, S((10.0, 24.0, 8.0)), 'memb', n=3, t=0.3)                         # (the inner membrane, down to the flank)
    panel(a, SH, S((10.0, 24.0, 8.0)), S((6.0, 26.0, 6.0)), 'memb', n=2, t=0.3)
    spike(a, WR, S((28.4, 40.2, 0.2)), 1.0, 'claw')                                  # (the thumb claw)
    FT = [S((45.0, 45.0, 6.0)), S((46.0, 34.0, 10.0)), S((40.0, 25.0, 13.0)), S((30.0, 19.0, 13.0))]
    for i, t in enumerate(FT):
        m = lerp(WR, t, 0.5); m = (m[0], m[1] + 1.0, m[2])
        rod(h, [WR, m, t], [1.6, 1.1, 0.5], 'bone', ext=0.1)
    for i in range(3):
        panel(h, WR, FT[i], FT[i + 1], 'memb' if i < 2 else 'membr', n=3, t=0.26)
    panel(h, WR, FT[3], S((24.0, 26.0, 10.0)), 'membr', n=2, t=0.26)
    for i in range(3):                                                               # (the trailing edge between the fingers: the aurora rim)
        SEG(h, FT[i], FT[i + 1], 0.5, 0.4, ('glow_s', 'glow_c', 'glow_h')[i], (0.0, 0.0, 1.0), light=11)

# ---------------------------------------------------------------------------------------------------- the saddle, between the wing roots
LEAN = 0.0
SEAT_PT = (0.0, 32.2, -4.0)
B('saddle', (-4.4, 30.0, -8.6), (4.4, 31.0, 1.0), 'leather')
B('saddle', (-3.0, 30.8, -7.0), (3.0, 32.2, -0.6), 'leather')
B('saddle', (-3.2, 31.6, -1.2), (3.2, 34.4, 0.4), 'leather')                         # (the cantle)
SEG('saddle', (0, 31.0, -8.4), (0, 34.6, -9.6), 1.0, 1.0, 'bone')                      # (a bone pommel: the horn it shed)
B('saddle', (-0.6, 34.4, -10.0), (0.6, 35.0, -9.2), 'brass')
for sx in (1, -1):
    SEG('saddle', (sx * 4.2, 30.4, -4.0), (sx * 9.4, 22.0, -4.6), 1.0, 0.6, 'leather', (0.0, 0.0, -1.0))          # (the girth)
    B('saddle', (min(sx * 9.0, sx * 10.0), 20.4, -5.4), (max(sx * 9.0, sx * 10.0), 22.2, -3.6), 'brass')

# ---------------------------------------------------------------------------------------------------- fx
FXK = 2.4                                                                              # (the breaths are built full length, shown at 2.4x)


def zigzag(part, A_, B_, n, amp, w, tex, rnd, light=15):
    pts = [A_]
    for i in range(1, n):
        c = lerp(A_, B_, i / n)
        pts.append((c[0] + rnd.uniform(-amp, amp), c[1] + rnd.uniform(-amp, amp), c[2]))
    pts.append(B_)
    for a, b in zip(pts, pts[1:]):
        SEG(part, a, b, w, w, tex, (0.0, 1.0, 0.0), ext=0.1, light=light, full=True)
    return pts


for k in HEADS:
    x0, y0, z0 = PIVOT[f'h{k}']
    m0 = (x0, y0 - 2.0, z0 - 12.0)                                                     # (the mouth's front)
    end = (x0, y0 - 2.0, z0 - 12.0 - 46.0)
    rnd = random.Random(ord(k))
    if k == 's':                                                                       # SQUALL: a forked bolt of storm
        zigzag('fx_s', m0, end, 10, 1.8, 1.0, 'zap', rnd); zigzag('fx_s', lerp(m0, end, 0.4), (end[0] + 6, end[1] - 4, end[2] + 6), 5, 1.4, 0.6, 'zap', rnd)
        zigzag('fx_s', lerp(m0, end, 0.6), (end[0] - 5, end[1] + 4, end[2] + 4), 4, 1.2, 0.5, 'zap', rnd)
    elif k == 'c':                                                                     # CINDER: a roaring cone of fire
        for i in range(7):
            t0, t1 = i / 7, (i + 1) / 7; c = lerp(m0, end, (t0 + t1) / 2); r = 1.6 + 9.0 * (t0 + t1) / 2
            SEG('fx_c', lerp(m0, end, t0), lerp(m0, end, t1), r, r, 'fire', (0.0, 1.0, 0.0), light=15, full=True)
            SEG('fx_c', lerp(m0, end, t0), lerp(m0, end, t1), r * 0.7, r * 0.7, 'fire', (0.7, 0.7, 0.0), light=15, full=True)
    else:                                                                              # HUSH: a slow stream of void orbs, spiralling
        for i in range(12):
            t = (i + 0.5) / 12; c = lerp(m0, end, t); a = t * 12.0; r = 1.0 + t * 3.0; s = 1.2 + t * 2.6
            c = (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2])
            B('fx_h', (c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), 'void', full=True, light=15,
              rot=((45.0, 35.26, 0.0), c))
        SEG('fx_h', m0, end, 0.6, 0.6, 'void', (0.0, 1.0, 0.0), light=15, full=True)
    # RANK III: the LIGHTNING STREAM - every head breathes Squall's lightning (a thick braided bolt, a sheath, rings)
    lp = f'l{k}'
    for j in range(2):
        zigzag(lp, m0, end, 12, 1.3, 1.1 - j * 0.4, 'zap', random.Random(ord(k) * 7 + j))
    SEG(lp, m0, end, 2.6, 2.6, 'zap', (0.0, 1.0, 0.0), light=15, full=True)
    for i in range(4):
        ring(R, lp, lerp(m0, end, 0.15 + i * 0.22), 2.4 + i * 0.6, 8, 0.4, 0.4, 'glow_s', plane='xy', light=15)
for p in ('fx_s', 'fx_c', 'fx_h', 'ls', 'lc', 'lh'):
    R.PART_K[p] = FXK
    pv = PIVOT[p]; R._els[p] = rigkit.shrink(R._els[p], FXK)
    R._pts[p] = [tuple(pv[i] + (v[i] - pv[i]) / FXK for i in range(3)) for v in R._pts[p]]

# THE STRIKE: the bolt from the sky at the target (Rank III) - a jagged column, a scorch ring, sparks
sx_, sy_, sz_ = PIVOT['strike']
rnd = random.Random(9)
zigzag('strike', (sx_, 24.0, sz_), (sx_, 0.0, sz_), 8, 1.8, 1.4, 'zap', rnd)
zigzag('strike', (sx_ + 2.0, 20.0, sz_), (sx_ + 5.0, 6.0, sz_ + 2.0), 4, 1.0, 0.7, 'zap', rnd)
B('strike', (sx_ - 7.0, 0.05, sz_ - 7.0), (sx_ + 7.0, 0.1, sz_ + 7.0), 'ring', faces=('up',), full=True, light=15)
# THE GUST: wind arcs swept forward off the wings
for i, (y, z, w) in enumerate(((18.0, -30.0, 30.0), (24.0, -36.0, 36.0), (14.0, -42.0, 40.0))):
    B('gust', (-w / 2, y - 4.0, z), (w / 2, y + 4.0, z + 0.02), 'wind', faces=('north', 'south'), full=True)
# THE RARE AURA: THE THREE WORLDS - three rings of motes orbiting it, one per head's colour, tilted against each other
for j, k in enumerate(HEADS):
    for i in range(8):
        a = math.radians(i * 45 + j * 15); r = 22.0
        c = (r * math.cos(a), 26.0 + 8.0 * math.sin(a) * (j - 1), r * math.sin(a))
        B('aura', (c[0] - 0.9, c[1] - 0.9, c[2] - 0.9), (c[0] + 0.9, c[1] + 0.9, c[2] + 0.9), f'mote_{k}', full=True, light=15, rot=((45.0, 35.26, 0.0), c))

# ---------------------------------------------------------------------------------------------------- skins
def _skin(sfx, B_, Bo, M, H):
    t = _tex(B_, Bo, M, H, sfx)
    sw = {}
    for k_, im in t.items(): R.tex(k_ + sfx, im); sw[k_] = k_ + sfx
    R.skin(sfx, sw)


def _hp(**over):
    return {k: dict(HP[k], **over.get(k, {})) for k in HEADS}


_skin('_dw', dict(deep='#3a1a0a', dark='#6a3418', base='#9a5626', light='#c27a3a', shine='#e8a85a'),
      dict(BONE, base='#ece0c8', light='#fff4e0', shine='#ffffff'), dict(deep='#3a1a14', dark='#5a2a1e', base='#7a3e2a', light='#9a5a3a', shine='#c27a4a'), HP)
_skin('_ab', dict(deep='#04100e', dark='#082220', base='#0e3634', light='#1a5450', shine='#2e7a72'),
      dict(BONE, base='#9ab4ae', light='#c0d8d2', shine='#e4f4f0', dark='#5a7470'), dict(deep='#020808', dark='#061614', base='#0c2624', light='#143c38', shine='#225a54'), HP)
_skin('_sh', dict(deep='#8a8296', dark='#b4acc0', base='#ddd6e6', light='#f2eef8', shine='#ffffff'),
      dict(BONE, base='#f4e8d0', light='#fff8ec', shine='#ffffff'), dict(deep='#6a5a7a', dark='#8a7a9a', base='#b4a4c4', light='#d4c8e0', shine='#f0eaf8'),
      _hp(s=dict(deep='#8aa69a', dark='#a8c4b6', base='#c8e0d2', light='#e2f2e8', shine='#ffffff'),
          c=dict(deep='#a6847a', dark='#c4a094', base='#dcbcae', light='#f0d8cc', shine='#fff0e8'),
          h=dict(deep='#9a8ab4', dark='#b8aad0', base='#d4caea', light='#ece4fa', shine='#ffffff')))
# charged: the storm crackling over every scale (Rank III's wind-up)
def _charge(im):
    im = im.convert('RGBA').copy(); px = im.load(); rnd = random.Random(3)
    for _ in range(6):
        x, y = rnd.randrange(64), rnd.randrange(64)
        for i in range(14):
            if 0 <= x < 64 and 0 <= y < 64: px[x, y] = hexc('#fff070') if i % 3 else hexc('#ffffff')
            x += rnd.choice((-1, 0, 1)); y += 1
    return im


sw = {}
for k_ in ('scale', 'scale2', 'memb', 'membr') + tuple(f'sc_{k}' for k in HEADS) + tuple(f'mix_{k}' for k in HEADS) + ('plate_c',):
    R.tex(k_ + '_ch', _charge(R._tex[k_])); sw[k_] = k_ + '_ch'
for k in HEADS: R.tex(f'glow_{k}_ch', glowtex(HP['s']['g'])); sw[f'glow_{k}'] = f'glow_{k}_ch'
R.skin('_ch', sw)

# ---------------------------------------------------------------------------------------------------- poses
FEET = ('pfr', 'pfl', 'ftr', 'ftl')


def plant(p, lift=0.0):
    """all four feet flat (each foot's world turn undone), the lowest foot on y=0"""
    p = dict(p); xf = rigkit.solve(R.PIVOT, R.PARENT, p)
    for f, par in (('pfr', 'lfr'), ('pfl', 'lfl'), ('ftr', 'shr'), ('ftl', 'shl')):
        Q = rigkit.solve(R.PIVOT, R.PARENT, p)[par][0]
        p[f] = qmul((-Q[0], -Q[1], -Q[2], Q[3]), p.get('_t_' + f, rigkit.I))
    return R.ground(p, lift)


def feet_low(p):
    xf = rigkit.solve(R.PIVOT, R.PARENT, p); out = {}
    for f in FEET:
        q, t = xf[f]; pv = rigkit.D(R.PIVOT[f]); ys = []
        for v in R._pts[f]:
            r = rigkit.qrot(q, tuple(rigkit.D(v)[i] - pv[i] for i in range(3))); ys.append(pv[1] + t[1] + r[1])
        out[f] = round(min(ys), 2)
    return out


FOLD = dict(wr=limb(1, 0, 20, -100), wr2=qs(('y', -170)), wl=limb(-1, 0, 20, -100), wl2=qs(('y', 170)))     # (folded high on its back, a cloak)
HALF = dict(wr=limb(1, -4, 6, -30), wr2=qs(('y', -60)), wl=limb(-1, -4, 6, -30), wl2=qs(('y', 60)))
OPEN = dict(wr=limb(1, 0, 18, 0), wr2=T(0, -10, 0), wl=limb(-1, 0, 18, 0), wl2=T(0, 10, 0))
CROUCH = dict(ufr=limb(1, 0, 30), lfr=limb(1, -60), ufl=limb(-1, 0, 30), lfl=limb(-1, -60), thr=limb(1, 30, 30), shr=limb(1, 30), thl=limb(-1, 30, 30), shl=limb(-1, 30))
LEGS = dict(ufr=limb(1, 0), lfr=limb(1, 0), ufl=limb(-1, 0), lfl=limb(-1, 0), thr=limb(1, 0), shr=limb(1, 0), thl=limb(-1, 0), shl=limb(-1, 0))
TAIL = dict(tail1=T(-4), tail2=T(-4), tail3=T(-2))


def heads(s=(0, 0, 0), c=(0, 0, 0), h=(0, 0, 0), js=0, jc=0, jh=0, ns=(0, 0), nc=(0, 0), nh=(0, 0)):
    """each head's turn: (pitch + nods down, yaw + turns to its right, roll) on the head; ns/nc/nh: (pitch, yaw) bent along its
    neck (shared by both neck segments); js/jc/jh the jaws (degrees open)"""
    out = {}
    for k, hv, nv, jv in (('s', s, ns, js), ('c', c, nc, jc), ('h', h, nh, jh)):
        out[f'n1{k}'] = T(nv[0] * 0.5, nv[1] * 0.5); out[f'n2{k}'] = T(nv[0] * 0.5, nv[1] * 0.5)
        out[f'h{k}'] = T(*hv); out[f'j{k}'] = T(jv)
    return out


def P(_lift=0.0, **kw):
    p = dict(LEGS); p.update(TAIL); p.update(FOLD); p.update(kw)
    return plant(p, _lift)


s_ = math.sin
POSES = R.POSES
FACE0 = dict(_face_hs='smug', _face_hc='snarl', _face_hh='sleepy')        # (their resting selves)
POSES.update({
    # IDLE: three heads, three minds - Squall surveys ahead, Cinder glowers to the right, Hush gazes off at nothing
    'idle_a': P(**FACE0, **heads(s=(4, 0, 0), c=(10, 18, 0), h=(-6, -22, 8), nc=(0, 10), nh=(-6, -10), jc=4)),
    # BICKERING: Cinder snaps at Squall's neck; Squall rears away, outraged; Hush, unbothered, looks at you
    'idle_b': P(_face_hs='wide', _face_hc='fierce', _face_hh='happy',
                **heads(s=(-14, -18, -10), c=(6, -42, 0), h=(4, 30, 0), ns=(-10, -16), nc=(16, -28), nh=(0, 20), jc=34, js=14)),
    # LOOKING ROUND: each head a different way (and Hush upside down, because it can)
    'idle_c': P(_face_hs=None, _face_hc='snarl', _face_hh='wide', **heads(s=(-8, 30, 0), c=(16, 40, 0), h=(0, -50, 150), ns=(-6, 20), nc=(6, 20), nh=(-10, -24), jh=6)),
})
for k in range(4):                                                     # THE WALK (24 ticks): a heavy four-beat, the necks bobbing out of step
    ph = math.pi * k / 2; w = s_(ph); c = math.cos(ph)
    POSES[f'walk_{k}'] = P(**FACE0, body=T(0, 3 * w, 2 * w), chest=T(0, -3 * w, -2 * w),
                           ufr=limb(1, 18 * w), lfr=limb(1, -18 * max(0.0, -c)), ufl=limb(-1, -18 * w), lfl=limb(-1, -18 * max(0.0, c)),
                           thr=limb(1, -18 * w), shr=limb(1, -22 * max(0.0, c)), thl=limb(-1, 18 * w), shl=limb(-1, -22 * max(0.0, -c)),
                           tail1=T(-4, -6 * w), tail2=T(-4, -7 * w), tail3=T(-2, -8 * w),
                           **heads(s=(4 + 3 * w, 0, 0), c=(10 - 3 * c, 14, 0), h=(-6 + 3 * c, -18, 6), ns=(2 * w, 4 * w), nc=(0, 8 - 4 * w), nh=(-6, -8 + 4 * w), jc=4))
for k in range(4):                                                     # THE RUN (12 ticks): a bounding gallop, the wings half open for balance
    ph = math.pi * k / 2; w = s_(ph)
    p = P(**FACE0, **HALF, body=T(4 + 4 * w), chest=T(-4 * w),
          ufr=limb(1, 30 * w), lfr=limb(1, -30 * max(0.0, -w)), ufl=limb(-1, 24 * w), lfl=limb(-1, -30 * max(0.0, -w)),
          thr=limb(1, -30 * w), shr=limb(1, -30 * max(0.0, w)), thl=limb(-1, -24 * w), shl=limb(-1, -30 * max(0.0, w)),
          tail1=T(0, 0), tail2=T(2, 0), tail3=T(4),
          **heads(s=(14, 0, 0), c=(18, 8, 0), h=(10, -8, 0), ns=(16, 0), nc=(16, 6), nh=(16, -6), js=8, jc=10, jh=4))
    o = p['_off']; p['_off'] = (o[0], o[1] + 2.0 * max(0.0, s_(ph + 1.0)), o[2]); POSES[f'run_{k}'] = p
POSES.update({
    # THE ROAR: reared on its hind legs, wings flung wide, all three heads up, all three jaws open - for once they agree
    'roar': P(_face='wide', _face_hc='snarl', **OPEN, body=T(-22), chest=T(-8), ufr=limb(1, 40), lfr=limb(1, -40), ufl=limb(-1, 30), lfl=limb(-1, -40),
              thr=limb(1, 22), shr=limb(1, -10), thl=limb(-1, 22), shl=limb(-1, -10), tail1=T(14), tail2=T(6), tail3=T(4),
              **heads(s=(-30, 0, 0), c=(-24, 24, 0), h=(-30, -24, 0), ns=(-10, 0), nc=(-10, 20), nh=(-10, -20), js=36, jc=40, jh=34)),
    # THE TRI-BREATH: each head breathes its own world - storm, fire, void - wind-up (heads drawn back), then the breath
    'breath_0': P(_face='fierce', **HALF, body=T(-4), **heads(s=(-24, 0, 0), c=(-20, 10, 0), h=(-24, -10, 0), ns=(-16, 0), nc=(-16, 10), nh=(-16, -10), js=16, jc=18, jh=12)),
    'breath_1': P(_face='wide', _face_hc='snarl', _show=('fx_s', 'fx_c', 'fx_h'), **HALF, chest=T(4),
                  **heads(s=(2, 0, 0), c=(4, 8, 0), h=(2, -10, 0), ns=(8, 0), nc=(6, 14), nh=(6, -16), js=30, jc=34, jh=26)),
    # THE WING GUST: both wings raised high and back - then swept down and forward, a wall of wind
    'gust_0': P(_face='fierce', body=T(-10), wr=limb(1, -20, 70, -20), wl=limb(-1, -20, 70, -20), wr2=T(0, -20, 20), wl2=T(0, 20, -20),
                **heads(s=(-10, 0, 0), c=(-6, 20, 0), h=(-10, -20, 0), ns=(-10, 0), nc=(-6, 14), nh=(-6, -14))),
    'gust_1': P(_face='fierce', _show=('gust',), body=T(8), wr=limb(1, 50, -10, 20), wl=limb(-1, 50, -10, 20), wr2=T(0, 30, 0), wl2=T(0, -30, 0),
                **heads(s=(10, 0, 0), c=(14, 14, 0), h=(10, -14, 0), ns=(10, 0), nc=(10, 10), nh=(10, -10), js=10, jc=14)),
    # THE LASH: the heads strike in turn like snakes - coiled back, then Cinder first, Squall, Hush last
    'lash_0': P(_face='fierce', **HALF, **heads(s=(-20, 0, 0), c=(-24, 16, 0), h=(-20, -16, 0), ns=(-30, 0), nc=(-30, 14), nh=(-30, -14), jc=10)),
    'lash_1': P(_face='wide', _face_hs='fierce', _face_hh='fierce', **HALF, body=T(6),
                **heads(s=(-10, 0, 0), c=(16, -6, 0), h=(-14, -10, 0), ns=(-16, 0), nc=(40, -10), nh=(-20, -14), jc=44)),
    'lash_2': P(_face='fierce', **HALF, body=T(8), **heads(s=(14, 0, 0), c=(0, 10, 0), h=(-10, -16, 0), ns=(40, 0), nc=(10, 14), nh=(-10, -14), js=44)),
    'lash_3': P(_face='fierce', _face_hh='wide', **HALF, body=T(6), **heads(s=(0, 4, 0), c=(0, 16, 0), h=(16, 10, 0), ns=(10, 4), nc=(4, 14), nh=(40, 10), jh=40)),
    # RANK III, LIGHTNING BREATH: all three rear back crackling (the charged skin) - then a sustained stream from every mouth,
    # the heads swaying as they breathe (two sway keys), a bolt striking the target
    'storm_0': P(_face='fierce', _face_hh='wide', **OPEN, body=T(-12), chest=T(-4), tail1=T(8),
                 **heads(s=(-36, 0, 0), c=(-30, 14, 0), h=(-36, -14, 0), ns=(-24, 0), nc=(-20, 16), nh=(-20, -16), js=20, jc=24, jh=20)),
    'storm_1': P(_face='wide', _face_hc='snarl', _show=('ls', 'lc', 'lh', 'strike'), **HALF, chest=T(4),
                 **heads(s=(4, -4, 0), c=(6, -14, 0), h=(4, 6, 0), ns=(8, -4), nc=(6, -8), nh=(6, 4), js=34, jc=38, jh=30)),
    'storm_2': P(_face='wide', _face_hc='snarl', _show=('ls', 'lc', 'lh', 'strike'), **HALF, chest=T(4),
                 **heads(s=(4, 4, 0), c=(6, -6, 0), h=(4, 14, 0), ns=(8, 4), nc=(6, -2), nh=(6, 10), js=34, jc=38, jh=30)),
    # SITTING (right-click): sat back on its haunches like a great cat, the wings folded, the heads up and watching three ways
    'sit_a': P(**FACE0, **CROUCH, tail1=T(4, 20), tail2=T(0, 20), tail3=T(0, 16),
               **heads(s=(6, 0, 0), c=(14, 28, 0), h=(0, -30, 10), ns=(-6, 0), nc=(0, 10), nh=(-4, -10))),
    # (sneak) CURLED UP: down low, the tail wrapped round, the three heads laid together - Squall and Cinder asleep; Hush, one eye open
    'sit_b': P(_face='blink', _face_hh='sleepy', **CROUCH, tail1=T(4, 40), tail2=T(0, 36), tail3=T(0, 30),
               **heads(s=(24, 0, 0), c=(22, -24, -10), h=(14, 30, 20), ns=(34, 0), nc=(30, -16), nh=(30, 18))),
    'happy': P(_face='happy', **OPEN, body=T(-8), **heads(s=(-14, 0, 0), c=(-6, 20, -10), h=(-10, -24, 14), ns=(-10, 0), nc=(-6, 10), nh=(-6, -10), js=20, jc=24, jh=16)),
    'hurt': P(_face='hurt', **HALF, body=T(6, 0, 8), **heads(s=(-20, -10, 10), c=(-10, 30, -10), h=(-16, -30, 20), ns=(-20, -6), nc=(-14, 18), nh=(-14, -18), js=24, jc=20, jh=20)),
    'ride': P(**FACE0, **heads(s=(8, 0, 0), c=(12, 10, 0), h=(4, -12, 6), nc=(4, 10), nh=(-2, -10))),
    'aura': P(_face='happy', _face_hh='sleepy', _show=('aura',), **heads(s=(4, 0, 0), c=(10, 18, 0), h=(-6, -22, 8), nc=(0, 10), nh=(-6, -10))),
    'doll': P(_face='happy', _face_hh='sleepy', **heads(s=(4, 0, 0), c=(8, 16, 0), h=(0, -16, 6), nc=(0, 10), nh=(-4, -10))),
})
DRAFT = list(POSES)
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {p: 'body' for p in PIVOT}
DOLL_GROUPS.update({f'h{k}': 'head' for k in HEADS}); DOLL_GROUPS.update({f'j{k}': 'head' for k in HEADS})
DOLL_GROUPS.update({p: 'legs' for p in ('ufr', 'lfr', 'pfr', 'ufl', 'lfl', 'pfl', 'thr', 'shr', 'ftr', 'thl', 'shl', 'ftl')})

MOVES = {
    'breath': dict(keys=((0, 'breath_0'), (14, 'breath_1')), hit=16, hold=40, per=10, recover=14, cd=12 * 20, dmg=6,
                   fx='the TRI-BREATH: 14 t drawn back; then 40 t: Squall\'s storm (6 + chains to 2 more within 4 blocks), Cinder\'s fire cone (6 + 5 s alight), Hush\'s void stream (4 + Levitation 1 s, then Slow Falling: a gentle lift-and-drop)'),
    'gust': dict(keys=((0, 'gust_0'), (10, 'gust_1')), hit=12, recover=12, cd=8 * 20, radius=10.0,
                 fx='WING GUST: up 10 t, down at 12: a 10-block cone of wind - knockback 2.5 away, projectiles in it deflected, fires blown out'),
    'lash': dict(keys=((0, 'lash_0'), (8, 'lash_1'), (11, 'lash_2'), (14, 'lash_3')), hit=(9, 12, 15), recover=10, cd=6 * 20, dmg=(8, 8, 8), reach=7.0,
                 fx='THE LASH: coiled 8 t; Cinder bites at 9, Squall at 12, Hush at 15 - three snake-strikes 7 blocks out'),
    'storm': dict(keys=((0, 'storm_0'), (20, 'storm_1'), (30, 'storm_2'), (40, 'storm_1'), (50, 'storm_2'), (60, 'storm_1')), hit=22, hold=40, per=8,
                  recover=16, cd=16 * 20, dmg=5, pierce=True,
                  fx='RANK III, LIGHTNING BREATH: armour-piercing; 20 t reared back crackling (_ch); then 40 t of three lightning streams converging on the target, the heads swaying (storm_1 <-> storm_2 every 10 t), a real lightning_bolt (visual only) on the target every 20 t, 5 every 8 t'),
}
