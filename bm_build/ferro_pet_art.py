"""(3.1 draft, stage 1: art only - not wired) THE FERRO - a glossy, mirror-black ferrofluid symbiote that learns your friends.

The owner: "a metallic, sheeny black symbiotic creature follower that can morph into and mimic other followers. It's friendly,
cute, but a bit terrifying. Found deep in caves rarely, with the right followers. Sort of like ferrofluid. It gains the ability
to mimic a follower after meeting them one time. Or, it can fight in its ferrofluid form. Its mimicked forms are sludgy and a bit
imperfect, but oddly cute."

LOOK   Shin-high (~0.6 blocks; 0.9 with its crown up). A plump gumdrop of mirror-black goo sitting in its own puddle: the puddle's
       rim beaded, two or three loose droplets on the floor beside it that never quite rejoin. Its sheen is PROJECTED, not painted
       per box (fe_proj): every side face samples one shared "studio reflection" by where it is on the whole blob - a softbox
       window reflected down its front-left, a bright sky band high up, a thin reflected horizon, deep ink below and a faint cool
       floor bounce at the bottom - and every top face samples one shared specular map, so the slabs' ring-tops break one hot
       highlight into arcs the way a real glossy ball does. Hand-placed glints (a curved white streak on the dome, a dot under it)
       on top of that, so it reads glossy at in-game size.
       Its FACE: two big round glossy eyes that float in the goo on little bead-lenses (a meniscus of goo lifts round each), the
       irises an oil-slick ramp - deep violet at the top through blue to a pale aqua at the bottom - with a big white shine and a
       small second one (the kit's eye(), all-iris). A tiny violet cat-mouth. Its two little pseudopod hands end in beads with
       three stubby finger-nubs. On top, three resting ferro nubs - it is never quite still.
       THE UNSETTLING HALF: when it is excited or fighting, a SPIKE CROWN rises out of its top (real ferrofluid: a tall centre
       spike, a ring of six, a ring of nine short ones leaning out - each a tapered cone that glints at the tip); its 'wide' eyes
       carry too many reflections (four shines, a pin pupil); and its mouth opens a little too wide ('maw': a slot across most
       of its face, lined with tiny ferro spikes for teeth). Nothing like a comic symbiote: no white eye patches, no tongue.
RIG    pool (the root: the puddle, beaded rim, loose droplets) - body (the blob, its glints, the nubs) - eyes (face part: the lenses,
       the eye overlay, the mouth plate; per expression) - crown (the spike crown: in game it rises by its display's scale.y,
       0.05 -> 1) - pr / pl (pseudopods) - maw (the too-wide mouth); fx: 'lash' (the pseudopod whip, on the right), 'burst'
       (a ring of ferro spikes out of the ground), 'pull' (magnetic field lines of beads, and a spiked collar on the foe), 'engulf'
       (the goo shell wrapped round a foe), 'splash' (the spit), 'puddle' (sitting: melted), 'seat' (sitting: the little armchair
       it makes of itself), 'aura' (the rare MAGNETAR aura), 'meyes' (the shared eyes every mimic form wears - see MIMICRY).
SKINS  '_qs' QUICKSILVER (chrome-silver: liquid mercury, the reflection inverted bright), '_au' GOLD LEAF (the black goo with gold
       leaf flakes suspended in it and a gold sheen), '_sh' SHINY "OIL SLICK" (black with an iridescent magenta-gold-teal sheen,
       gold eyes - "trying something new today").

MIMICRY (the scalable part: one generator for every follower, ferro_form())
       Source: phase134.figures() - every follower already ships a figurine (the checklist), as [(model, translation, left, right,
       scale)] in blocks at its own RIG_SCALE: the game's own part transforms at rest. ferro_form() reads each part's built model
       back from the resource pack (dolls_bake.load_model) and carries every element through its display's transform into ONE
       merged item model (as dolls_bake does, with no chibi warp), at true size. On the way it:
         - swaps every opaque texture for the shared ferro set (FERRO_SET: side / side-dark / top / bottom), PROJECTED by where the
           face is on the whole figure, so any follower's silhouette reads as one glossy black object with one coherent highlight;
           dark source textures take 'sxd' (a dimmer reflection), so hair against a face still separates, faintly;
         - drops see-through glow/ghost faces (a ferro copy is opaque), keeps cut-out sprites as ferro-masked copies;
         - drops the specks (every element under SPECK units in all directions): details soften;
         - inflates every element a hair (INFLATE) and jitters it (JIT): fatter, sludgier, slightly wrong;
         - adds goo LIPS under the big overhangs and DRIPS (a stalk and a bead) hanging off them, a PUDDLE round the feet (and,
           for a floater, a goo stalk down to it: it can't quite let go of the ground);
         - drops light_emission: the source's own eyes go dark - THE FERRO'S EYES show through instead: a separate display
           of the shared 'meyes' model at EYES[follower] (the head's front, found from the head parts by name), so the mimic's
           expressions cost nothing per follower.
       Variants (cosmetic, shiny) are 'parent' models that only override the texture variables: ~150 bytes each per follower.
"""
import json
import math
import os
import random
from PIL import Image, ImageDraw
from fol5_kit import (Rig, hexc, mix, limb, T, cells, soft, lit, glow, eye, blush, mouth, put, slab, stack, ball, profile,
                      chain, ring)

PIVOT = {'pool': (0, 0, 0), 'body': (0, 1.0, 0), 'eyes': (0, 7.4, -6.0), 'crown': (0, 9.4, 0.4), 'pr': (5.9, 4.6, -1.6),
         'pl': (-5.9, 4.6, -1.6), 'maw': (0, 5.0, -5.6), 'lash': (5.9, 4.6, -1.6), 'burst': (0, 0, 0), 'pull': (0, 6.0, -20.0),
         'engulf': (0, 14.0, -20.0), 'splash': (0, 0, -16.0), 'puddle': (0, 0, 0), 'seat': (0, 0, 0), 'aura': (0, 0, 0),
         'meyes': (0, 8.0, 0)}
PARENT = {'pool': None, 'body': 'pool', 'eyes': 'body', 'crown': 'body', 'pr': 'body', 'pl': 'body', 'maw': 'body', 'lash': 'body',
          'burst': None, 'pull': 'body', 'engulf': None, 'splash': None, 'puddle': None, 'seat': None, 'aura': None, 'meyes': None}
FACES = ('happy', 'blink', 'wide', 'fierce', 'hurt', 'sleepy', 'look', 'grin', 'maw')
OPT = ('crown', 'maw', 'lash', 'burst', 'pull', 'engulf', 'splash', 'puddle', 'seat', 'aura', 'meyes')
R = Rig('fe_', 0.9, PIVOT, PARENT, FACES, face_part=('eyes', 'meyes'), opt=OPT)
SKIN_NAMES = {'_qs': 'cosmetic: Quicksilver (chrome-silver)', '_au': 'cosmetic: Gold Leaf', '_sh': 'SHINY: Oil Slick'}

# ---------------------------------------------------------------------------------------------------- the ferro palette
# (ink: the goo; sky / spec: what it reflects; rim: the cool floor bounce; oil: the faint iridescence at a sheen's edge)
PAL = {'': dict(ink='#08080d', ink2='#0e0f17', mid='#171a26', sky='#2c3348', sky2='#4a5571', spec='#a8b4d4', hot='#f2f6ff',
                rim='#1d2233', oil='#3a2a62', oil2='#1f4a5e', dn='#050507',
                iris=('#2a0c4e', '#3e1a7a', '#2c3c9e', '#1a74b4', '#2ab4c4', '#7ae8dc', '#d0fff4'), mouth='#7a4ab8', gum='#1c0a2a',
                tooth='#8c96b6'),
       '_qs': dict(ink='#5c6270', ink2='#727886', mid='#8a909e', sky='#c4cad6', sky2='#e2e6ee', spec='#ffffff', hot='#ffffff',
                   rim='#9aa2b2', oil='#a8a0c8', oil2='#9ab8c4', dn='#2a2e36',
                   iris=('#0a2a4a', '#123e6a', '#1a5a8e', '#2a7ab0', '#4aa0d0', '#8acaf0', '#e0f4ff'), mouth='#2a3a5a', gum='#20242e',
                   tooth='#ffffff'),
       '_au': dict(ink='#0c0a08', ink2='#141009', mid='#1e1810', sky='#3a2e18', sky2='#6a5226', spec='#e8c060', hot='#fff4c8',
                   rim='#2a2010', oil='#8a6a1a', oil2='#5a4410', dn='#060504',
                   iris=('#3a1a02', '#6a3a06', '#a0600c', '#d08a1a', '#f0b43a', '#ffd870', '#fff4c0'), mouth='#a06a1a', gum='#2a1806',
                   tooth='#e8c060', flake=('#c89a2a', '#f0c84a', '#fff0a0')),
       '_sh': dict(ink='#07060c', ink2='#0e0b18', mid='#181428', sky='#3a1e4e', sky2='#7a2a7a', spec='#ffd070', hot='#fffbe8',
                   rim='#123a44', oil='#c0308a', oil2='#20a0a0', dn='#050409',
                   iris=('#4a1a00', '#7a3a00', '#b06a0a', '#e0a020', '#ffd040', '#fff090', '#ffffe0'), mouth='#c04a9a', gum='#2a0a2a',
                   tooth='#ffd070')}


# ---------------------------------------------------------------------------------------------------- the shared ferro set
def tex_side(c, dark=False):
    """the studio reflection a side face samples by its place on the whole object (rows = height, top to bottom; columns =
    across, the viewer's left to right): a bright sky band high up with a softbox WINDOW reflected down the left, a thin
    reflected horizon, deep ink, a faint cool floor bounce with a thread of oil-slick colour at the very bottom"""
    k = 0.62 if dark else 1.0
    S = lambda a: mix(c['ink'], a, k)
    def f(x, y, r):
        v, u = y / 32, x / 32
        if 0.17 <= u < 0.27 and 0.05 <= v < 0.72:                        # the window: a bright core, a soft edge, fading down
            core = 0.19 <= u < 0.24 and v < 0.36
            if v >= 0.44: return S(c['sky'] if core else c['mid'])         # (its reflection below the horizon, dimmer)
            return S(c['hot'] if core and v < 0.2 else c['spec'] if core else c['sky2'] if v < 0.3 else c['sky'])
        if 0.70 <= u < 0.75 and 0.08 <= v < 0.22: return S(c['sky2'])       # (a second, smaller window: the other light)
        if v < 0.05: return S(c['sky'])
        if v < 0.09: return S(c['sky2'])
        if v < 0.12: return S(c['spec'] if (x // 3) % 5 else c['sky2'])
        if v < 0.22: return S(mix(c['sky2'], c['sky'], (v - 0.12) / 0.1))
        if v < 0.32: return S(mix(c['sky'], c['mid'], (v - 0.22) / 0.1))
        if v < 0.41: return S(c['mid']) if v < 0.36 else S(c['sky'])
        if v < 0.44: return S(c['sky2'])                                    # (the reflected horizon: crisp)
        if v < 0.48: return c['ink2']
        if v < 0.56: return c['ink'] if (x + y // 3) % 9 else c['ink2']
        if v < 0.64: return S(c['mid']) if (x // 2) % 6 else S(c['rim'])         # (the ground's reflection: a dim band)
        if v < 0.84: return c['ink'] if (x + y // 3) % 9 else c['ink2']
        if v < 0.9: return c['ink2']
        if v < 0.95: return S(c['sky']) if v >= 0.92 else S(c['rim'])
        return S(c['oil'] if (x // 4) % 2 else c['oil2'])
    im = cells(f, 3)
    if 'flake' in c: _flakes(im, c, 41)
    return im


def tex_top(c):
    """the shared specular map every top face samples by where it is seen from above: sky-lit, one hot highlight up and to
    the viewer's left (the kit's one light), a halo round it, darker toward the far edge"""
    def f(x, y, r):
        u, v = (x + 0.5) / 32, (y + 0.5) / 32
        d = math.hypot((u - 0.3) * 1.1, v - 0.3)
        if d < 0.055: return c['hot']
        if d < 0.11: return c['spec']
        if d < 0.19: return c['sky2']
        e = math.hypot(u - 0.5, v - 0.5)
        if e > 0.4: return c['ink2']
        if e > 0.3: return c['mid'] if u + v < 1.0 else c['ink2']
        if e > 0.2: return c['sky'] if u + v < 0.9 else c['mid']
        return c['sky']
    im = cells(f, 4)
    if 'flake' in c: _flakes(im, c, 43)
    return im


def _flakes(im, c, seed):
    """gold leaf suspended in the goo: small irregular flakes (2-4 cells), lit on one edge"""
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(14):
        x, y = rnd.randrange(0, 60, 2), rnd.randrange(0, 60, 2); w, h = rnd.choice(((4, 2), (2, 4), (4, 4), (6, 2)))
        d.rectangle((x, y, x + w - 1, y + h - 1), fill=hexc(c['flake'][1])); d.rectangle((x, y, x + w - 1, y), fill=hexc(c['flake'][2]))
        d.rectangle((x + w - 2, y + h - 1, x + w - 1, y + h - 1), fill=hexc(c['flake'][0]))


def tex_spike(c):
    """a spike's long faces (anchored): a lit ridge along its top rows, the cone dark, the tip end (u high) catching light"""
    def f(x, y, r):
        if y < 1: return c['spec']
        if y < 3: return c['sky2'] if x > 18 else c['sky']
        if x > 26: return c['sky'] if y < 8 else c['ink2']
        return c['ink2'] if y < 6 else c['ink']
    return cells(f, 5)


def tex_glint(c):
    return cells(lambda x, y, r: c['hot'] if 3 < y < 28 else c['spec'], 6)


def tex_gum(c):
    return cells(lambda x, y, r: c['gum'] if (x + y) % 7 else mix(c['gum'], c['mouth'], 0.35), 7)


def ferro_set(c):
    """the textures a mimic form (and the Ferro itself) wear: side, side-dark, top, bottom, spike, glint, gum"""
    return {'sx': tex_side(c), 'sxd': tex_side(c, True), 'up': tex_top(c), 'dn': cells(lambda x, y, r: c['dn'], 8),
            'spk': tex_spike(c), 'gl': tex_glint(c),
            'spk0': cells(lambda x, y, r: c['mid'] if y < 1 else c['ink2'], 10), 'spk1': cells(lambda x, y, r: c['sky'] if y < 1 else c['mid'], 11),
            'spk2': cells(lambda x, y, r: c['sky2'] if y < 1 else c['sky'], 12), 'spk3': cells(lambda x, y, r: c['hot'] if y < 1 else c['spec'], 13), 'gum': tex_gum(c), 'tooth': cells(lambda x, y, r: c['tooth'] if y > 2 else c['hot'], 9)}


# ---------------------------------------------------------------------------------------------------- the face
# the eye overlay on the 'eyes' part: 11 x 5.5 units (44 x 22 texels), two eyes 15 x 17 centred at 10 and 34; the mouth plate
# under them: 6 x 2 units (24 x 8 texels)
FW, FH, EC, EYY, EW, EH = 11.0, 5.5, (11, 33), 2, 15, 17
MW, MH = 6.0, 2.0


def _eyes(kind, c):
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    rim = mix(c['sky'], c['ink'], 0.25)
    for i, cx in enumerate(EC):
        flip = i == 1
        if kind not in ('happy', 'blink', 'hurt', 'sleepy'):                       # (the meniscus: goo lifting round the eye)
            for a in range(0, 360, 6):
                x = cx + (EW / 2 + 0.8) * math.cos(math.radians(a)); y = EYY + EH / 2 + (EH / 2 + 0.6) * math.sin(math.radians(a))
                put(im, x - 0.5, y - 0.5, rim if a < 200 else c['mid'])
        k = {'grin': None, 'maw': 'wide', 'look': 'look'}.get(kind, kind)
        kw = dict(sclera=False, iris=c['iris'], lash=c['ink'], pupil='#020104', shine=c['hot'], irk=0.62)
        if kind in ('happy', 'blink', 'hurt'):
            kw['lash'] = c['spec']                                                   # (closed: the lids catch the light)
        if kind in ('wide', 'maw'):
            kw['irk'] = 0.3                                                          # (a pin pupil)
        eye(im, cx, EYY, EW, EH, flip=flip, kind=k, **kw)
        if kind in ('wide', 'maw'):                                                  # (too many reflections: four shines)
            for dx, dy in ((4, 4), (-3, 9), (3, 12), (-5, 13)):
                put(im, cx + dx, EYY + dy, c['hot']); put(im, cx + dx + 1, EYY + dy, c['spec'])
        if kind == 'sleepy':
            for x in range(cx - 6, cx + 7): put(im, x, EYY + 10, c['spec'])
    return im


def _face(kind, c):
    """the mouth plate (see-through but for the mouth): a tiny violet cat-mouth with a lit lower lip; 'grin' a little too wide"""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    cx, y = 12, 2
    if kind in ('maw',): return im                                                    # (the maw geometry shows instead)
    if kind == 'grin':                                                                # (too wide: the whole plate, tiny teeth)
        for x in range(1, 23):
            yy = y + (1 if 3 < x < 20 else 0)
            put(im, x, yy, c['mouth']); put(im, x, yy + 1, c['gum']); put(im, x, yy + 2, c['mouth'] if x in (1, 22) or 3 < x < 20 else (0, 0, 0, 0))
            if x % 2 and 3 < x < 20: put(im, x, yy + 1, c['tooth'])
        return im
    kind2 = {'hurt': 'wobble', 'wide': 'o', 'fierce': 'flat', 'sleepy': 'flat', 'blink': 'cat', 'happy': 'cat', 'look': 'cat'}.get(kind, 'cat')
    mouth(im, cx, y, kind2, col=c['mouth'], tongue=c['gum'], w=6)
    if kind2 == 'cat':
        for x in (cx - 1, cx + 1): put(im, x, y + 2, mix(c['mouth'], c['spec'], 0.35))
    return im


# ---------------------------------------------------------------------------------------------------- textures
def _tex(c):
    t = ferro_set(c)
    t['eyes'] = _eyes(None, c); t['face'] = _face(None, c)
    for f in FACES:
        t[f'eyes_{f}'] = _eyes(f, c); t[f'face_{f}'] = _face(f, c)
    t['field'] = glow((c['hot'], c['spec'], c['oil2'], c['oil']), 16, alpha=(230, 200, 150, 0))
    t['mote'] = glow((c['hot'], c['spec'], c['oil']), 16, alpha=(255, 200, 0))
    return t


BASE_T = _tex(PAL[''])
for k, v in BASE_T.items(): R.tex(k, v)
for sfx in ('_qs', '_au', '_sh'):
    c = dict(PAL[''], **PAL[sfx])
    for k, v in _tex(c).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in BASE_T})


# ---------------------------------------------------------------------------------------------------- projection (the sheen)
_QUAD = {'north': lambda f, t: [(t[0], t[1], f[2]), (f[0], t[1], f[2]), (f[0], f[1], f[2])],
         'south': lambda f, t: [(f[0], t[1], t[2]), (t[0], t[1], t[2]), (t[0], f[1], t[2])],
         'east': lambda f, t: [(t[0], t[1], t[2]), (t[0], t[1], f[2]), (t[0], f[1], f[2])],
         'west': lambda f, t: [(f[0], t[1], f[2]), (f[0], t[1], t[2]), (f[0], f[1], t[2])],
         'up': lambda f, t: [(f[0], t[1], f[2]), (t[0], t[1], f[2]), (t[0], t[1], t[2])],
         'down': lambda f, t: [(f[0], f[1], t[2]), (t[0], f[1], t[2]), (t[0], f[1], f[2])]}


def _rotf(e):
    r = e.get('rotation')
    if not r: return lambda p: p
    o = r['origin']
    if 'axis' in r:
        a = math.radians(r['angle']); c, s = math.cos(a), math.sin(a)
        M = {'x': [[1, 0, 0], [0, c, -s], [0, s, c]], 'y': [[c, 0, s], [0, 1, 0], [-s, 0, c]], 'z': [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[r['axis']]
    else:
        ax, ay, az = (math.radians(r.get(k, 0)) for k in 'xyz')
        cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
        Rx = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]; Ry = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]; Rz = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
        mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        M = mm(Rz, mm(Ry, Rx))
    return lambda p: tuple(sum(M[i][k] * (p[k] - o[k]) for k in range(3)) + o[i] for i in range(3))


def project(els, c, rad, ytop, h, side='sx', top='up', bot='dn', only=None, keep=()):
    """re-map every face of these elements (model space) onto the shared ferro set by WHERE it is: a side face's rows by its
    height on the object (ytop .. ytop - h), its columns across the object (centre c = (x, z), half-width rad) along the face's
    own left-to-right; a top face's uv by its place seen from above. One coherent reflection over a whole stack of boxes.
    only: re-map only faces whose texture is in it; keep: textures left alone (eyes, glints)"""
    cx, cz = c
    for e in els:
        rf = _rotf(e)
        for fn, fc in e['faces'].items():
            t = fc['texture'][1:]
            if t in keep or (only is not None and t not in only): continue
            p0, p1, p3 = (rf(p) for p in _QUAD[fn](e['from'], e['to']))
            n = [(p1[1] - p0[1]) * (p3[2] - p0[2]) - (p1[2] - p0[2]) * (p3[1] - p0[1]),
                 (p1[2] - p0[2]) * (p3[0] - p0[0]) - (p1[0] - p0[0]) * (p3[2] - p0[2]),
                 (p1[0] - p0[0]) * (p3[1] - p0[1]) - (p1[1] - p0[1]) * (p3[0] - p0[0])]
            nn = math.sqrt(sum(v * v for v in n)) or 1.0
            ny = n[1] / nn
            tu = [p1[i] - p0[i] for i in range(3)]; L = math.sqrt(sum(v * v for v in tu)) or 1.0; tu = [v / L for v in tu]
            cl = lambda v: round(max(0.0, min(16.0, v)), 3)
            if abs(ny) > 0.7:                                                       # (a top or bottom face: seen from above)
                if ny < 0: fc['texture'] = '#' + bot; fc['uv'] = [0, 0, 16, 16]; continue
                U = lambda p: 8 - (p[0] - cx) / rad * 8
                V = lambda p: 8 + (p[2] - cz) / rad * 8
                fc['texture'] = '#' + top
                fc['uv'] = [cl(U(p0)), cl(V(p0)), cl(U(p1)), cl(V(p3))]
                if abs(fc['uv'][0] - fc['uv'][2]) < 0.05: fc['uv'][2] = cl(fc['uv'][0] + 0.1)
                if abs(fc['uv'][1] - fc['uv'][3]) < 0.05: fc['uv'][3] = cl(fc['uv'][1] + 0.1)
                continue
            U = lambda p: 8 + ((p[0] - cx) * tu[0] + (p[2] - cz) * tu[2]) / rad * 8
            V = lambda p: (ytop - p[1]) / h * 16
            fc['texture'] = '#' + side
            uv = [cl(U(p0)), cl(V(p0)), cl(U(p1)), cl(V(p3))]
            if abs(uv[0] - uv[2]) < 0.05: uv[2] = cl(uv[0] + 0.1)
            if abs(uv[1] - uv[3]) < 0.05: uv[3] = cl(uv[1] + 0.1)
            fc['uv'] = uv
    return els


def fproj(part, els, c, rad, y0, y1, **kw):
    """project() in design units on one of this rig's parts"""
    pv = PIVOT[part]; o = (8 - pv[0], 8 - pv[1], 8 - pv[2])
    return project(els, (c[0] + o[0], c[1] + o[2]), rad, y1 + o[1], y1 - y0, **kw)


# ---------------------------------------------------------------------------------------------------- the model
B = R.box


def blob(part, c, rx, y0, y1, n=4, d=1.0, power=1.0, lo=0.0, hi=1.0, light=0):
    """a glossy goo lump: slabs, its sheen projected over the whole lump"""
    rows = profile(y0, y1 - y0, rx, n, d=d, power=power, lo=lo, hi=hi)
    els = stack(R, part, rows, 'sx', c=(c[0], c[1]), light=light, k=0.55)
    return fproj(part, els, c, rx, min(r[0] for r in rows), max(r[1] for r in rows))


def spike(part, base, direc, L, w, tip=True):
    """one ferrofluid spike: a tapered cone of four segs from base along direc, concave (it narrows fast, then needles out);
    the long faces carry the lit-ridge spike texture, the last seg a glint"""
    m = math.sqrt(sum(v * v for v in direc)); u = tuple(v / m for v in direc)
    P = lambda s: tuple(base[i] + u[i] * L * s for i in range(3))
    up = (0.0, 0.0, -1.0) if abs(u[1]) > 0.9 else (0.0, 1.0, 0.0)
    out = []
    n = 6 if L > 3 else 4
    for i in range(n):
        a, b = i / n, (i + 1) / n
        ww = max(0.1, w * (1 - (a + b) / 2) ** 1.25)
        out.append(R.seg(part, P(a), P(b), ww, ww, f'spk{min(3, i * 4 // n)}', up=up, ext=0.05, shift=False))
    return out


def bead(part, c, r, n=None):
    n = n or (1 if r < 0.8 else 2)
    return blob(part, (c[0], c[2]), r, c[1] - r * (0.6 if n == 1 else 0.85), c[1] + r * (0.6 if n == 1 else 0.85), n=n)


# ---- the puddle: a thin pool, three lobes, a beaded rim, loose droplets on the floor
fproj('pool', stack(R, 'pool', [(0.0, 0.4, 8.6, 7.8), (0.4, 0.75, 7.8, 7.0)], 'sx', k=0.5), (0, 0), 8.6, 0.0, 0.75)
for (x, z, r) in ((5.6, 4.6, 2.8), (-6.6, 2.4, 2.4)):
    fproj('pool', stack(R, 'pool', [(0.0, 0.35, r), (0.35, 0.6, r * 0.7)], 'sx', c=(x, z), k=0.5), (x, z), r, 0.0, 0.6)
for i in range(8):                                                                 # (the rim beads: surface tension)
    a = math.radians(i * 45 + 22); rr = 8.2 + (i % 3) * 0.3
    bead('pool', (rr * math.cos(a), 0.5, rr * math.sin(a) * 0.9), 0.6 + (i % 2) * 0.2)
for (x, z, r) in ((10.6, -3.4, 0.95), (11.8, -1.2, 0.55), (-9.8, -5.8, 0.7)):            # (loose droplets that never quite rejoin)
    bead('pool', (x, r * 0.8, z), r)

# ---- the body: a plump gumdrop, fuller low, settling into the puddle; a lip where it meets the pool
BODY = [(0.6, 1.3, 6.6), (1.3, 2.2, 6.2), (2.2, 3.4, 6.6), (3.4, 4.8, 6.9), (4.8, 6.0, 6.8), (6.0, 7.0, 6.5), (7.0, 7.9, 6.1),
        (7.9, 8.7, 5.6), (8.7, 9.4, 5.0), (9.4, 10.1, 4.3), (10.1, 10.7, 3.5), (10.7, 11.3, 2.6), (11.3, 11.7, 1.5)]
BODY = [(a, b, w, w * 0.9) for a, b, w in BODY]
KB = 0.5                                    # (the body's slabs: corners cut deep - it reads round, not boxed)
fproj('body', stack(R, 'body', BODY, 'sx', k=KB), (0, 0), 6.9, 0.6, 11.7)
# the resting nubs on top: three, a magnet's echo
for (x, z, L) in ((0.4, 0.0, 1.5), (-1.8, 1.0, 1.0), (1.9, 1.3, 0.8)):
    spike('body', (x, 11.7 if abs(x) < 1 else 11.3, z), (x * 0.15, 1.0, z * 0.1), L, 1.2)
# hand-placed glints: a curved white streak high on its front-left, a dot under it, a cool rim light low on the right
GL = [((2.1, 9.5, -3.96), (1.7, 10.2, -3.2)), ((1.7, 10.2, -3.2), (1.15, 10.85, -2.42)), ((1.15, 10.85, -2.42), (0.4, 11.4, -1.45))]
for a, b in GL: R.seg('body', a, b, 0.55, 0.12, 'gl', up=(0.0, 0.5, -0.86), shift=False, light=10)
B('body', (4.5, 1.6, -3.33), (5.05, 3.9, -3.31), 'gl', faces=('north',), full=True, light=10)     # (a softbox streak low on its left flank)
B('body', (4.6, 4.0, -3.33), (4.95, 4.6, -3.31), 'gl', faces=('north',), full=True, light=10)
B('body', (-3.2, 1.5, -5.62), (-1.4, 1.8, -5.6), 'up', faces=('north',), uv={'north': [3, 2, 5, 3]})   # (the floor's bounce, low right)

# ---- the eyes: two bead-lenses floating proud of its front flat, an overlay with the eyes, the mouth plate
ez = -5.85
for sx in (1, -1):
    ex = 2.75 * sx
    fproj('eyes', stack(R, 'eyes', [(4.2, 4.8, 1.9, 0.55), (4.8, 8.4, 2.5, 0.8), (8.4, 9.0, 1.9, 0.55)], 'sx', c=(ex, ez), k=0.55), (ex, ez), 2.5, 4.2, 9.0)
B('eyes', (-FW / 2, 3.85, ez - 0.85), (FW / 2, 3.85 + FH, ez - 0.83), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]}, light=6)
B('eyes', (-MW / 2, 1.9, -6.0), (MW / 2, 1.9 + MH, -5.98), 'FACE', faces=('north',), uv={'north': [0, 0, MW, MH]})

# ---- the spike crown: a tall centre spike, a ring of six, a ring of nine leaning out (in game it rises by scale.y)
cy = 11.6                                  # (the crown's spikes stand on the dome's top; its joint is lower, inside, so it rises out of it)
spike('crown', (0, cy - 0.6, 0.4), (0, 1, 0), 8.0, 2.2)
for i in range(6):
    a = math.radians(i * 60 + 30); x, z = 2.4 * math.cos(a), 0.4 + 2.4 * math.sin(a)
    spike('crown', (x, cy - 1.0, z), (x * 0.18, 1.0, (z - 0.4) * 0.18), 5.4, 1.7)
for i in range(9):
    a = math.radians(i * 40 + 5); x, z = 4.4 * math.cos(a), 0.4 + 4.4 * math.sin(a)
    spike('crown', (x, cy - 2.4, z), (x * 0.42, 1.0, (z - 0.4) * 0.42), 3.2, 1.3)

# ---- the pseudopods: a tapered arm out of its side, a bead hand, three finger-nubs
for p, sx in (('pr', 1), ('pl', -1)):
    x, y, z = PIVOT[p]
    els = chain(R, p, [(x - 0.4 * sx, y + 0.2, z), (x + 1.5 * sx, y - 0.3, z - 0.8), (x + 2.6 * sx, y - 0.7, z - 1.3)], [1.7, 1.3, 1.05], 'sx')
    fproj(p, els, (x + 1.2 * sx, z - 0.6), 3.5, y - 2.5, y + 2.5)
    bead(p, (x + 0.3 * sx, y, z - 0.3), 1.45, 2)
    hx, hy, hz = x + 2.9 * sx, y - 0.8, z - 1.45
    bead(p, (hx, hy, hz), 1.2, 3)
    for dx, dz in ((0.8, -0.6), (0.0, -1.0), (-0.8, -0.6)):
        bead(p, (hx + dx * sx, hy - 0.65, hz + dz), 0.42, 1)

# ---- the maw (fx of the face): a slot across most of its front, a dark gum, rows of tiny ferro-spike teeth
mz = -6.15
B('maw', (-4.6, 1.3, mz), (4.6, 4.0, mz + 0.4), 'gum', faces=('north', 'up', 'down', 'east', 'west'))
for i in range(11):
    x = -4.0 + i * 0.8
    R.seg('maw', (x, 4.05, mz - 0.1), (x, 3.1 + (0.3 if i % 2 else 0), mz - 0.1), 0.5, 0.4, 'tooth', shift=False)
    if i % 2 == 0: R.seg('maw', (x + 0.4, 1.25, mz - 0.1), (x + 0.4, 2.1, mz - 0.1), 0.45, 0.4, 'tooth', shift=False)
fproj('maw', [B('maw', (-5.0, 4.0, mz - 0.4), (5.0, 4.4, mz + 0.5), 'sx'), B('maw', (-4.4, 0.8, mz - 0.4), (4.4, 1.3, mz + 0.5), 'sx')],
      (0, 0), 7.3, 0.8, 12.1)

# ---- LASH: the pseudopod whip - beaded along its length (ferrofluid beads on a stretched thread), a star of spikes at the tip
x0, y0, z0 = PIVOT['lash']
LP = [(x0 - 1.0, y0 + 0.4, z0), (x0 + 3.0, y0 + 1.6, z0 - 2.0), (x0 + 6.0, y0 + 3.2, z0 - 5.5), (x0 + 7.6, y0 + 3.6, z0 - 9.5),
      (x0 + 7.8, y0 + 2.8, z0 - 13.5), (x0 + 6.8, y0 + 1.4, z0 - 17.5), (x0 + 5.0, y0 + 0.4, z0 - 20.5)]
fproj('lash', chain(R, 'lash', LP, [2.6, 2.0, 1.6, 1.25, 1.0, 0.8, 0.6], 'sx'), (x0 + 5, z0 - 12), 6.0, y0 - 2, y0 + 6)
for i in (2, 3, 4, 5):
    bead('lash', LP[i], 1.25 - i * 0.12, 2)
tx, ty, tz = LP[-1]
for d in ((0, 1, -0.4), (0.8, -0.3, -0.6), (-0.8, -0.3, -0.6), (0, -0.2, -1), (0.9, 0.6, -0.3), (-0.9, 0.6, -0.3)):
    spike('lash', (tx, ty, tz), d, 2.4, 0.9)

# ---- BURST: a ring of ferro spikes out of the ground, each from a little beaded puddle, leaning out
for i in range(12):
    a = math.radians(i * 30); r0 = 11.0 + (i % 2) * 1.6; x, z = r0 * math.cos(a), r0 * math.sin(a)
    fproj('burst', stack(R, 'burst', [(0.0, 0.5, 1.9), (0.5, 0.9, 1.2)], 'sx', c=(x, z)), (x, z), 1.9, 0, 0.9)
    spike('burst', (x, 0.4, z), (math.cos(a) * 0.45, 1.0, math.sin(a) * 0.45), 8.5 + (i % 3) * 1.6, 2.0)
for i in range(6):
    a = math.radians(i * 60 + 15); x, z = 7.4 * math.cos(a), 7.4 * math.sin(a)
    spike('burst', (x, 0.3, z), (math.cos(a) * 0.3, 1.0, math.sin(a) * 0.3), 4.6, 1.4)

# ---- PULL: magnetic field lines - beads strung along three arcs to the foe, a faint glowing thread, a spiked collar on the foe
px, py, pz = 0.0, 6.0, -7.0
FOE = (0.0, 9.0, -36.0)
for k, (bx, by) in enumerate(((8.0, 1.0), (-8.0, 1.0), (0.0, 8.0))):
    pts = []
    for j in range(13):
        t = j / 12; s = math.sin(math.pi * t)
        pts.append((px + bx * s, py + (FOE[1] - py) * t + by * s, pz + (FOE[2] - pz) * t))
    for j in range(12):
        if j % 2 == 0:
            a, b = pts[j], pts[j + 1]
            R.seg('pull', a, b, 0.9 - 0.25 * abs(j - 6) / 6, 0.9 - 0.25 * abs(j - 6) / 6, 'spk', ext=0.1, shift=False)
        R.seg('pull', pts[j], pts[j + 1], 0.3, 0.3, 'field', light=12, full=True)
for i in range(10):
    a = math.radians(i * 36); x, y = FOE[0] + 3.4 * math.cos(a), FOE[1] + 3.4 * math.sin(a)
    spike('pull', (x + 1.4 * math.cos(a), y + 1.4 * math.sin(a), FOE[2]), (-math.cos(a), -math.sin(a), 0.0), 1.8, 1.0)
ring(R, 'pull', FOE, 4.8, 12, 0.9, 0.9, 'spk', plane='xy')

# ---- ENGULF: the goo shell over a foe (a zombie's height), a bridge back to the body, a lump where the foe pushes out
ex0, _, ez0 = PIVOT['engulf']
EG = [stack(R, 'engulf', profile(0.0, 26.0, 9.6, 11, d=0.92, power=0.9), 'sx', c=(0, ez0), k=0.5),
      stack(R, 'engulf', [(0.0, 0.6, 12.6, 11.6), (0.6, 1.1, 11.4, 10.4)], 'sx', c=(0, ez0), k=0.5)]
for (x, y, z, r) in ((6.4, 8.0, ez0 - 3.0, 5.0), (-6.6, 12.0, ez0 + 1.0, 4.8), (2.0, 20.5, ez0 - 1.5, 4.6), (-3.0, 4.0, ez0 - 5.0, 4.2)):
    EG.append(stack(R, 'engulf', profile(y - r, 2 * r, r, 4, d=0.9), 'sx', c=(x, z), k=0.5))   # (the lobes: something inside is pushing)
fproj('engulf', [e for g in EG for e in g], (0, ez0), 10.5, 0.0, 26.0)
bead('engulf', (9.2, 16.0, ez0 - 4.6), 2.2, 3)                                         # (a hand pressing out from inside)
fproj('engulf', chain(R, 'engulf', [(0, 3.0, -2.0), (0, 4.4, -6.0), (0, 4.0, -10.5)], [6.0, 4.6, 6.4], 'sx'), (0, -6), 7.0, 0, 8)
for (x, z, L) in ((-5.0, ez0 - 7.6, 3.0), (3.6, ez0 - 8.0, 4.4), (7.6, ez0 - 4.0, 2.2)):               # (drips off its front)
    R.seg('engulf', (x, 10.0, z), (x, 10.0 - L, z), 0.9, 0.9, 'sx', shift=False); bead('engulf', (x, 9.8 - L, z), 0.75, 2)
for i, a in enumerate((-20, 0, 20)):                                                   # (three spikes on top: still the Ferro)
    spike('engulf', (2.0 + a * 0.12, 24.0, ez0 - 1.5), (math.sin(math.radians(a)), 1.0, 0.0), 4.4 - abs(a) * 0.05, 1.6)

# ---- SPLASH: the spit - a ring of flung goo droplets
for i in range(10):
    a = math.radians(i * 36 + 8); r0 = 6.0 + (i % 3) * 2.4
    bead('splash', (r0 * math.cos(a), 2.0 + (i % 4) * 2.2, PIVOT['splash'][2] + r0 * math.sin(a)), 0.8 + (i % 3) * 0.25, 2)

# ---- SITTING: melted into a puddle (the eyes on top of a low hump) - and the little armchair it makes of itself
fproj('puddle', stack(R, 'puddle', [(0.0, 0.5, 10.6, 9.0), (0.5, 0.9, 9.6, 8.2)], 'sx'), (0, 0), 10.6, 0, 0.9)
fproj('puddle', stack(R, 'puddle', profile(-2.6, 5.2, 6.8, 4, d=0.9, lo=0.5), 'sx', k=0.5), (0, 0), 6.8, 0, 2.6)
for i in range(13):
    a = math.radians(i * 27.7); bead('puddle', (10.0 * math.cos(a), 0.6, 8.4 * math.sin(a)), 0.55 + (i % 3) * 0.18)
# the seat: a low round goo cushion, a curved back of three stacked arcs behind it, two bead armrests, drips off the front
fproj('seat', stack(R, 'seat', [(0.0, 0.6, 9.0, 8.2), (0.6, 2.8, 8.4, 7.6), (2.8, 3.6, 7.8, 7.0)], 'sx', k=0.5), (0, 0), 9.0, 0, 3.6)
SB = []
for y, r, hh in ((3.4, 7.8, 2.8), (6.0, 7.4, 2.6), (8.4, 6.6, 2.0)):
    SB += ring(R, 'seat', (0, y + hh / 2, 0.8), r, 5, 1.8, hh, 'sx', a0=25 + (8.4 - y) * 1.5, arc=130 - (8.4 - y) * 3)
fproj('seat', SB, (0, 0.8), 8.0, 3.4, 9.4)
for sx in (1, -1):
    bead('seat', (sx * 7.2, 4.6, -1.0), 1.5, 3)
    bead('seat', (sx * 6.6, 6.6, 3.4), 1.3, 2)
for x, L in ((-4.6, 1.6), (-1.0, 2.4), (2.4, 1.2), (5.6, 1.9)):
    R.seg('seat', (x, 3.2, -7.2), (x, 3.2 - L, -7.3), 0.8, 0.8, 'sx', shift=False); bead('seat', (x, 3.0 - L, -7.3), 0.6, 2)

# ---- the rare MAGNETAR aura: two tilted loops of field-line beads round it, glowing threads, motes
for k, tilt in enumerate((28, -28)):
    for i in range(16):
        a = math.radians(i * 22.5); x, y = 13.0 * math.cos(a), 8.0 + 9.0 * math.sin(a)
        zz = math.sin(math.radians(tilt)) * x * 0.6
        if i % 2 == 0: bead('aura', (x * math.cos(math.radians(tilt)), y, zz), 0.7, 2)
        a2 = math.radians((i + 1) * 22.5); x2, y2 = 13.0 * math.cos(a2), 8.0 + 9.0 * math.sin(a2)
        R.seg('aura', (x * math.cos(math.radians(tilt)), y, zz), (x2 * math.cos(math.radians(tilt)), y2, math.sin(math.radians(tilt)) * x2 * 0.6),
              0.3, 0.3, 'field', light=13, full=True)
for i in range(6):
    a = math.radians(i * 60 + 20)
    B('aura', (9 * math.cos(a) - 0.6, 18 + (i % 3) * 1.6, 9 * math.sin(a)), (9 * math.cos(a) + 0.6, 19.2 + (i % 3) * 1.6, 9 * math.sin(a) + 0.02),
      'mote', faces=('north', 'south'), full=True, light=14)

# ---- MEYES: the shared eyes every mimic form wears (a separate display at that form's EYES anchor; 8 units across here)
for sx in (1, -1):
    fproj('meyes', stack(R, 'meyes', [(5.6, 6.2, 1.55), (6.2, 9.8, 1.95), (9.8, 10.4, 1.55)], 'sx', c=(2.05 * sx, 0.4)), (2.05 * sx, 0.4), 1.9, 5.6, 10.4)
B('meyes', (-4.05, 6.0, -1.62), (4.05, 6.0 + 4.05, -1.6), 'EYES', faces=('north',), uv={'north': [0, 0, FW, FH]}, light=6)


# ---------------------------------------------------------------------------------------------------- poses
def P(lift=0.0, **kw):
    return R.ground(kw, lift)


PODS = dict(pr=limb(1, 10, -6), pl=limb(-1, 10, -6))
POSES = R.POSES
POSES.update({
    'idle_a': P(**PODS, body=T(2, 0, 2)),
    'idle_b': P(_face='happy', body=T(-4, 0, -5), pr=limb(1, 30, 40), pl=limb(-1, 20, 30)),                        # (a wobble: pleased)
    'idle_c': P(_face='look', body=T(2, 14, 4), pr=limb(1, 0, -10), pl=limb(-1, 40, 10), _o_eyes=(0.8, 0.2, 0)),   # (curious: a lean)
    'alert': P(_face='wide', _show=('crown',), body=T(-6), pr=limb(1, 20, 30), pl=limb(-1, 20, 30)),               # (bristling)
    'walk_0': P(body=T(10, 0, 6), pr=limb(1, 40, 0), pl=limb(-1, -20, 0), _o_body=(0.6, 0, -0.6)),                # (it oozes: a lean
    'walk_1': P(body=T(4, 0, -6), pr=limb(1, -20, 0), pl=limb(-1, 40, 0), _o_body=(-0.6, -0.3, -1.0)),            #  and a slump)
    'run_0': P(_face='happy', body=T(22), pr=limb(1, -60, 10), pl=limb(-1, -60, 10), _o_body=(0, 0.3, -1.6)),
    'happy': P(_face='happy', _show=('crown',), lift=0.6, pr=limb(1, 0, 130), pl=limb(-1, 0, 130), body=T(-6)),
    'grin': P(_face='grin', body=T(-4, 0, 3), **PODS),
    'hurt': P(_face='hurt', body=T(-16, 0, 10), pr=limb(1, 10, 60), pl=limb(-1, 10, 60)),
    # SPIKE BURST: a squash and a bristle (5 ticks) - then the ring erupts out of the floor (2 ticks), holds 4, sinks 6
    'burst_up': P(_face='fierce', _show=('crown',), body=T(8), _o_body=(0, -0.8, 0), pr=limb(1, -10, 70), pl=limb(-1, -10, 70)),
    'burst': P(_face='maw', _show=('crown', 'burst', 'maw'), body=T(-10), pr=limb(1, 0, 95), pl=limb(-1, 0, 95)),
    # LASH: the pseudopod coils back over its shoulder (4 ticks) - and cracks forward (2 ticks), recoil 6
    'lash_up': P(_face='fierce', _show=('crown', 'lash'), _hide=('pr',), body=T(-8, -20), lash=T(-30, 140, -40), pl=limb(-1, 20, 30)),
    'lash': P(_face='fierce', _show=('lash',), _hide=('pr',), body=T(10, 16), lash=T(4, -6), pl=limb(-1, -20, 30)),
    # MAGNETIC PULL: every spike leans at the foe (6 ticks), the field lines string out, the foe yanked in (8 ticks)
    'pull': P(_face='wide', _show=('crown', 'pull'), body=T(12), crown=T(34), pr=limb(1, 80, 10), pl=limb(-1, 80, 10)),
    # ENGULF (charged): it swells, eyes wide and mouth too wide (20 ticks) - lunges (4) - the shell over the foe (40) - spits (6)
    'engulf_up': P(_face='maw', _show=('crown', 'maw'), body=T(-14), _o_body=(0, 0.6, 0), pr=limb(1, 0, 120), pl=limb(-1, 0, 120)),
    'engulf': P(_face='happy', _show=('engulf',), _hide=('body', 'pr', 'pl'), _o_eyes=(0, 13.0, -22.0)),
    'spit': P(_face='maw', _show=('maw', 'splash'), body=T(-18), pr=limb(1, 0, 70), pl=limb(-1, 0, 70)),
    # sitting: right-click melts it into a puddle (10 ticks), then the goo rises into a little armchair it lounges in
    'melt': P(_show=('puddle',), _hide=('body', 'pool', 'pr', 'pl'), _o_eyes=(0, -3.0, 2.0)),
    'sit_a': P(_show=('seat',), _hide=('pool',), _o_body=(0, 2.9, 0.6), body=T(-6), pr=limb(1, 10, 20), pl=limb(-1, 10, 20)),
    'sit_b': P(_face='sleepy', _show=('puddle',), _hide=('body', 'pool', 'pr', 'pl'), _o_eyes=(0, -3.2, 2.2)),
    'tired': P(_face='blink', _show=('puddle',), _hide=('body', 'pool', 'pr', 'pl'), _o_eyes=(0, -3.0, 2.6)),
    'aura': P(_face='happy', _show=('aura',), **PODS),
})
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'alert', 'walk_0', 'walk_1', 'run_0', 'happy', 'grin', 'hurt', 'burst_up', 'burst', 'lash_up',
         'lash', 'pull', 'engulf_up', 'engulf', 'spit', 'melt', 'sit_a', 'sit_b', 'aura']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'body': 'head', 'eyes': 'head', 'crown': 'head', 'pr': 'body', 'pl': 'body', 'pool': 'legs'}   # (a blob is all head; its puddle the feet)
SHINY = 'Shiny Oil Slick'

# ATTACKS (ticks): wind-up, the hit tick, hold, recover; damage; cooldown (s) - for the wiring stage
ATTACKS = {
    'burst': dict(poses=('burst_up', 'burst'), windup=5, hit=6, hold=4, recover=6, rise=2, dmg=4, radius=2.0, cd=8,
                  fx='a ring of 12 spikes out of the floor round it (r ~0.7 block), scale.y 0 -> 1 in 2 ticks; knock-up 0.4'),
    'lash': dict(poses=('lash_up', 'lash'), windup=4, hit=5, hold=1, recover=6, dmg=5, reach=3.0, cd=3,
                 fx='the whip cracks out 2.5 blocks; its spiked tip hits the first foe in a 3-block line'),
    'pull': dict(poses=('alert', 'pull'), windup=6, hit=7, hold=8, recover=6, dmg=1, reach=8.0, cd=10,
                 fx='every spike leans at the foe; field-line beads string out; the foe is yanked 4 blocks in over 8 ticks '
                    '(Motion on a mob; a player gets a short Levitation-free pull: slowness I 2 s instead); chains into lash'),
    'engulf': dict(poses=('engulf_up', 'engulf', 'spit'), windup=20, lunge=4, wrap=40, spit=6, dmg=1, dmg_spit=6, cd=20,
                   fx='the shell closes over one foe (no bosses, no players: they get a 2-heart squeeze instead); while wrapped '
                      'the foe is parked in its hitbox with invisibility and no AI (as the Mimic does), 1 damage per 10 ticks; '
                      'then SPAT 4 blocks with a ring of droplets'),
}


# ======================================================================================================== MIMICRY
SPECK = 0.6          # (units: an element under this in every direction is dropped - a mimic's details soften)
INFLATE = 0.12       # (units each side: every element a little fatter - the gaps close, the form goes sludgy)
JIT = 0.14           # (units: each element nudged by up to this - slightly wrong)
SAG = 0.07          # (the slump: up to 7% wider at its feet, 3.5% lower at its top)
CAP_H = 2.6          # (blocks: the most of itself it can raise - a nine-block serpent is mimicked Ferro-sized, as a 2.6-block one)
MIMIC_K = 0.96       # (a mimic stands a touch smaller than the real one: it is still a little puddle at heart)


def _lum_class(rp, tid, cache={}):
    """how a source texture reads to the generator: 'drop' (a see-through glow or ghost), 'cut' (a cut-out sprite), 'dark', 'mid'"""
    if tid in cache: return cache[tid]
    ns, p = tid.split(':') if ':' in tid else ('minecraft', tid)
    f = os.path.join(rp, 'assets', ns, 'textures', p + '.png')
    if not os.path.exists(f):
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools', 'vanilla', 'assets', ns, 'textures', p + '.png')
    try:
        im = Image.open(f).convert('RGBA')
    except (OSError, FileNotFoundError):
        cache[tid] = ('mid', None); return cache[tid]
    if im.height > im.width: im = im.crop((0, 0, im.width, im.width))
    px = list(im.getdata()); n = len(px)
    semi = sum(1 for p in px if 10 < p[3] < 200) / n; clear = sum(1 for p in px if p[3] <= 10) / n
    op = [p for p in px if p[3] >= 200] or [(0, 0, 0, 255)]
    lum = sum(0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2] for p in op) / len(op) / 255
    k = 'drop' if semi > 0.3 else 'cut' if clear > 0.08 else 'dark' if lum < 0.2 else 'mid'
    cache[tid] = (k, im)
    return cache[tid]


def _mask(im, c):
    """a cut-out sprite in ferro: its alpha kept, filled with ink and a lit top row"""
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); a = im.load(); o = out.load(); w, h = im.size
    for y in range(h):
        for x in range(w):
            if a[x, y][3] > 10:
                top = y == 0 or a[x, y - 1][3] <= 10
                o[x, y] = hexc(c['sky2'] if top else c['ink2'] if (x + y) % 5 else c['mid'])
    return out


def ferro_form(rp, parts, key, seed=None, drips=12, lips=10, lod=0, c=None, budget=None):
    """ANY follower's figurine (phase134.figures: [(model, translation, left, right, scale)], blocks) -> its ferro mimic:
    (model json, extra textures {name: image}, info). One merged item model at true size / F (F >= 1 keeps it inside the
    model box; the display is scaled by F * MIMIC_K), its sheen projected from the shared set, softened, inflated, jittered,
    dripping, standing in a puddle; info: F, the eyes' anchor (model units) and size, counts. lod 1: the low-element silhouette
    (only elements 1.2 units or more in their longest direction - the body masses)"""
    import numpy as np
    import dolls_bake as DB
    c = c or PAL['']
    rnd = random.Random(seed if seed is not None else sum(map(ord, key)))
    RyPI = DB._ry(math.pi)
    raw, extra = [], {}
    for i, (mid, tr, L, Rr, sc) in enumerate(parts):
        m = DB.load_model(rp, mid); tx = m.get('textures', {})
        d = m.get('display', {}).get('fixed', {})
        dr = d.get('rotation', [0, 0, 0]); dt = np.array(d.get('translation', [0, 0, 0])) / 16; ds = d.get('scale', [1, 1, 1])
        Dm = DB._rx(math.radians(dr[0])) @ DB._ry(math.radians(dr[1])) @ DB._rz(math.radians(dr[2]))
        Q = DB._quat(L) @ DB._quat(Rr)
        A = sc * Q @ RyPI @ Dm * ds[0]
        def world(p, Dm=Dm, dt=dt, ds=ds, sc=sc, Q=Q, tr=tr):
            v = (np.array(p, dtype=float) / 16 - 0.5) * ds[0]
            return sc * Q @ (RyPI @ (Dm @ v + dt)) + np.array(tr)
        def res(t, tx=tx):
            n = 0
            while t.startswith('#') and n < 9: t = tx.get(t[1:], t); n += 1
            return t
        grp = DB.group(mid)
        for e in m.get('elements', []):
            Me, o = DB._el_rot(e.get('rotation'))
            f, t = np.array(e['from'], dtype=float), np.array(e['to'], dtype=float)
            if o is None: o = (f + t) / 2
            faces = {}
            tns = [res(fc.get('texture', '')) for fc in e.get('faces', {}).values()]
            look = 'eye' if (e.get('light_emission') and grp == 'head') or any('eye' in t for t in tns) else 'face' if grp == 'head' and any('face' in t for t in tns) else None
            for fn, fc in e.get('faces', {}).items():
                tid = res(fc.get('texture', '#missing'))
                if tid.startswith('#'): continue
                kind, im = _lum_class(rp, tid if ':' in tid else 'minecraft:' + tid)
                if kind == 'drop': continue
                if kind == 'cut':
                    nm = f'fm_{key}_{len(extra)}'
                    if not any(v[0] == tid for v in extra.values()): extra[nm] = (tid, _mask(im, c))
                    nm = next(k for k, v in extra.items() if v[0] == tid)
                    faces[fn] = dict(fc, texture='#' + nm, uv=fc.get('uv') or DB._auto_uv(fn, e['from'], e['to']))
                else:
                    faces[fn] = {'texture': '#' + ('sxd' if kind == 'dark' else 'sx'), 'uv': [0, 0, 16, 16]}
            if not faces and not look: continue
            raw.append((world(o), A, Me, f - o, t - o, faces, grp, look))
    # true size, inside the model box: blocks -> units / F, feet at model y -16, centred at 8, 8, facing north
    pts = []
    for q, A, Me, a, b, _f, _g, _l in raw:
        for x in (a[0], b[0]):
            for y in (a[1], b[1]):
                for z in (a[2], b[2]):
                    pts.append(q + A @ (Me @ np.array([x, y, z])) / 16)
    pts = np.array(pts); lo, hi = pts.min(0), pts.max(0)
    H = (hi[1] - min(lo[1], 0.0)) * 16; Wd = max(hi[0] - lo[0], hi[2] - lo[2]) * 16
    F = max(1.0, H / 46.0, Wd / 44.0)
    cx, cz = (lo[0] + hi[0]) / 2, (lo[2] + hi[2]) / 2
    def to_model(w): return RyPI.T @ (np.array([w[0] - cx, w[1], w[2] - cz]) * 16 / F) + np.array([8.0, -16.0, 8.0])
    els, heads, looks = [], [], {'eye': [], 'face': []}
    for q, A, Me, a, b, faces, grp, look in raw:
        Rt = RyPI.T @ A @ Me; sig = np.linalg.norm(Rt[:, 0]); Rt = Rt / sig
        sz = (b - a) * sig / F
        true = abs(sz) * F
        if look: looks[look].append(to_model(q) + np.array([0, 0, min(a[2], b[2]) * sig / F]))   # (where its own eyes / face plate were)
        if not faces or max(true) < SPECK: continue
        if lod and max(true) < 1.2: continue
        qm = to_model(q) + np.array([rnd.uniform(-JIT, JIT) for _ in range(3)]) / F
        yn = max(0.0, min(1.0, (qm[1] + 16) * F / max(16.0, H)))                 # (0 at its feet, 1 at its top)
        sag = SAG * (1 - yn)                                                      # (THE SAG: it settles - wider, fatter and lower toward the floor)
        qm = np.array([8 + (qm[0] - 8) * (1 + sag), -16 + (qm[1] + 16) * (1 - SAG * 0.5 * yn), 8 + (qm[2] - 8) * (1 + sag)])
        pad = np.sign(b - a) * INFLATE * (1 + 2.5 * (1 - yn) ** 2) / F
        fr, to = qm + a * sig / F - pad, qm + b * sig / F + pad
        fr, to = np.minimum(fr, to), np.maximum(fr, to)
        el = {'from': [round(float(v), 3) for v in fr], 'to': [round(float(v), 3) for v in to], 'faces': faces}
        x, y, z = DB._euler(Rt)
        if max(abs(x), abs(y), abs(z)) > 1e-3:
            el['rotation'] = {'origin': [round(float(v), 3) for v in qm], 'x': round(float(x), 2), 'y': round(float(y), 2), 'z': round(float(z), 2)}
        els.append(el)
        if grp == 'head': heads.append(el)
    if budget and len(els) > budget:                                              # (the light option: only its biggest masses)
        vol = lambda e: (e['to'][0] - e['from'][0]) * (e['to'][1] - e['from'][1]) * (e['to'][2] - e['from'][2])
        keep = set(map(id, sorted(els, key=vol, reverse=True)[:budget]))
        els = [e for e in els if id(e) in keep]; heads = [e for e in heads if id(e) in keep]
    # the figure's own box (model units)
    def box(es):
        P = []
        for e in es:
            rf = _rotf(e); f, t = e['from'], e['to']
            P += [rf((xx, yy, zz)) for xx in (f[0], t[0]) for yy in (f[1], t[1]) for zz in (f[2], t[2])]
        return [min(p[i] for p in P) for i in range(3)], [max(p[i] for p in P) for i in range(3)]
    (x0, y0, z0), (x1, y1, z1) = box(els)
    G = lambda: {k: {'texture': '#sx'} for k in _QUAD}
    def under(e):
        """an element's underside, if it faces the floor (its turned bottom face within ~30 degrees of level): its 4 corners"""
        rf = _rotf(e); f, t = e['from'], e['to']
        best = None
        for fn in _QUAD:
            p0, p1, p3 = (rf(p) for p in _QUAD[fn](f, t))
            n = np.cross(np.subtract(p1, p0), np.subtract(p3, p0)); n = n / (np.linalg.norm(n) or 1)
            if best is None or n[1] < best[0]: best = (n[1], p0, p1, p3)
        ny, p0, p1, p2 = best                                                      # (_QUAD lists three corners in order: p1 -> p2 is an edge)
        if ny > -0.86: return None
        return np.array(p0), np.array(p1) - np.array(p0), np.array(p2) - np.array(p1)
    unders = []
    for e in els:
        u = under(e)
        if u is None: continue
        o, du, dv = u
        area = np.linalg.norm(du) * np.linalg.norm(dv) * F * F
        lowy = min(o[1], (o + du)[1], (o + dv)[1], (o + du + dv)[1])
        if area > 2.0 and lowy > y0 + 2.0 / F: unders.append((area, e, o, du, dv))
    unders.sort(key=lambda t: -t[0])
    boxes = [box([e]) for e in els]
    def free(p, L, src):                                                          # (clear air under this point for the drip's length: it shows)
        for k_ in range(6):
            y_ = p[1] - 0.35 / F - (L + 0.8 / F) * k_ / 5
            for e_, (lo_, hi_) in zip(els, boxes):
                if e_ is src: continue
                if lo_[0] - 0.2 / F < p[0] < hi_[0] + 0.2 / F and lo_[2] - 0.2 / F < p[2] < hi_[2] + 0.2 / F and lo_[1] < y_ < hi_[1]: return False
        return True
    add = []
    for area, e, o, du, dv in unders[:lips]:                                      # (goo LIPS: the underside's edge thickened, as goo gathers there)
        if 'rotation' in e: continue
        f, t = e['from'], e['to']; p = 0.16 / F
        add.append({'from': [f[0] - p, f[1] - 0.22 / F, f[2] - p], 'to': [t[0] + p, f[1] + 0.3 / F, t[2] + p], 'faces': G()})
    n = 0
    for area, e, o, du, dv in unders:                                             # (DRIPS: a stalk and a bead, off the front of the undersides)
        if n >= drips: break
        for _try in range(8):
            a_, b_ = rnd.uniform(0.12, 0.88), rnd.uniform(0.12, 0.88)
            p = o + du * a_ + dv * b_
            L = min(rnd.uniform(1.8, 4.2), (p[1] - y0) * F - 0.6) / F
            if p[2] > z0 + (z1 - z0) * 0.55: continue                              # (the front half: where they're seen)
            if L > 0.4 / F and free(p, L, e): break
        else:
            continue
        w = rnd.uniform(0.95, 1.35) / F; bw = w * 1.45
        add.append({'from': [p[0] - w / 2, p[1] - L, p[2] - w / 2], 'to': [p[0] + w / 2, p[1] + 0.25 / F, p[2] + w / 2], 'faces': G()})
        add.append({'from': [p[0] - bw / 2, p[1] - L - bw * 0.7, p[2] - bw / 2], 'to': [p[0] + bw / 2, p[1] - L + bw * 0.25, p[2] + bw / 2], 'faces': G()})
        n += 1
        if os.environ.get('FE_DEBUG') == '2':
            for d_ in add[-2:]: d_['faces'] = {k: {'texture': '#dbg', 'uv': [0, 0, 16, 16]} for k in _QUAD}
    if os.environ.get('FE_DEBUG'): print(key, 'undersides', len(unders), 'drips', n)
    # the PUDDLE round its feet (and a goo stalk up to a floater)
    feet = [e for e in els if min(e['from'][1], e['to'][1]) < -16 + 1.5 / F]
    if feet:
        (fx0, _, fz0), (fx1, _, fz1) = box(feet)
    else:
        fx0, fx1, fz0, fz1 = (x0 + x1) / 2 - 2.5 / F, (x0 + x1) / 2 + 2.5 / F, (z0 + z1) / 2 - 2.5 / F, (z0 + z1) / 2 + 2.5 / F
        sw = min(3.0, (x1 - x0) * F * 0.25) / F
        add.append({'from': [(fx0 + fx1) / 2 - sw / 2, -16, (fz0 + fz1) / 2 - sw / 2], 'to': [(fx0 + fx1) / 2 + sw / 2, y0 + 0.5 / F, (fz0 + fz1) / 2 + sw / 2],
                    'faces': G()})
    pcx, pcz = (fx0 + fx1) / 2, (fz0 + fz1) / 2; k = 0.72
    cap = min(9.0, 0.6 * max(x1 - x0, z1 - z0) * F) / F
    hx, hz = min(cap, (fx1 - fx0) / 2 + 2.0 / F), min(cap, (fz1 - fz0) / 2 + 2.0 / F)
    pud = [({'from': [pcx - hx, -16, pcz - hz * k], 'to': [pcx + hx, -16 + 0.5 / F, pcz + hz * k]}),
           ({'from': [pcx - hx * k, -16, pcz - hz], 'to': [pcx + hx * k, -16 + 0.5 / F, pcz + hz]}),
           ({'from': [pcx - hx * 0.8, -16 + 0.5 / F, pcz - hz * 0.6], 'to': [pcx + hx * 0.8, -16 + 0.8 / F, pcz + hz * 0.6]})]
    for i in range(7):
        a = rnd.uniform(0, 6.28); r = rnd.uniform(0.35, 0.7) / F
        bx, bz = pcx + hx * 0.95 * math.cos(a), pcz + hz * 0.95 * math.sin(a)
        pud.append({'from': [bx - r, -16, bz - r], 'to': [bx + r, -16 + r * 1.5, bz + r]})
    for p in pud: p['faces'] = {k: {'texture': '#sx'} for k in _QUAD}
    add += pud
    els += add
    # the sheen: one coherent reflection over the whole form
    rad = max(x1 - x0, z1 - z0) / 2 + 0.5
    project(els, ((x0 + x1) / 2, (z0 + z1) / 2), rad, y1, y1 - (-16), only=('sx',))
    project(els, ((x0 + x1) / 2, (z0 + z1) / 2), rad, y1, y1 - (-16), side='sxd', only=('sxd',))
    for e in els:
        e.pop('light_emission', None); e['faces'] = {k: v for k, v in e['faces'].items()}
        e['from'] = [round(float(min(32.0, max(-16.0, v))), 3) for v in e['from']]; e['to'] = [round(float(min(32.0, max(-16.0, v))), 3) for v in e['to']]
        if 'rotation' in e: e['rotation']['origin'] = [round(float(min(32.0, max(-16.0, v))), 3) for v in e['rotation']['origin']]
    # the eyes' anchor: the head parts' front, a little over half way up them (else the top third of the whole form)
    if heads:
        (hx0, hy0, hz0), (hx1, hy1, hz1) = box(heads)
    else:
        hx0, hx1, hy0, hy1, hz0 = x0, x1, y0 + (y1 - y0) * 0.6, y1, z0
    hw = min((hx1 - hx0) * 0.78, (hy1 - hy0) * 1.05)
    if heads:                                                                     # (the head's middle: the median of its parts - a ponytail doesn't pull it aside)
        xs = sorted((e['from'][0] + e['to'][0]) / 2 for e in heads); mx = xs[len(xs) // 2]
    else:
        mx = (hx0 + hx1) / 2
    ay = hy0 + (hy1 - hy0) * 0.5
    at = [min(e['from'][2], e['to'][2]) for e in (heads or els) if 'rotation' not in e and e['from'][1] <= ay <= e['to'][1]
          and e['from'][0] - 0.5 <= mx <= e['to'][0] + 0.5]                      # (the face's front at the eyes' height - not a snout's tip)
    zs = sorted(at)
    fz = zs[len(zs) // 3] if zs else hz0
    E = looks['eye'] or looks['face']                                             # (where its own eyes were - else its face plate: the Ferro's go there)
    if E:
        mx = sorted(p[0] for p in E)[len(E) // 2]; ay = sum(p[1] for p in E) / len(E) + (0 if looks['eye'] else 0.6 / F)
        fz = min(p[2] for p in E) + 0.1 / F
    anchor = (float(mx), float(ay), float(fz) - 0.15 / F)
    used = sorted({fc['texture'][1:] for e in els for fc in e['faces'].values()})
    tex = {t: (f'bm:block/fe_{t}' if t in ('sx', 'sxd', 'up', 'dn') else 'minecraft:block/redstone_block' if t == 'dbg' else f'bm:block/{t}') for t in used}
    tex['particle'] = 'bm:block/fe_sx'
    model = {'textures': tex, 'elements': els, 'display': {'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}}
    info = dict(k=round(MIMIC_K * min(1.0, CAP_H * 16 / H), 4), F=round(float(F), 4), eyes=tuple(round(float(v), 3) for v in anchor), eye_w=round(float(hw), 3), n=len(els), added=len(add),
                cut=len(extra), height=round(float(H) / 16, 3))
    return model, {k: v[1] for k, v in extra.items()}, info


def variant(key, sfx):
    """a cosmetic / shiny mimic form: a parent model that only overrides the shared set's texture variables (~150 bytes)"""
    return {'parent': f'bm:item/fm_{key}', 'textures': {t: f'bm:block/fe_{t}{sfx}' for t in ('sx', 'sxd', 'up', 'dn')} | {'particle': f'bm:block/fe_sx{sfx}'}}


def eyes_xf(info, at=(0.0, 0.0, 0.0), k=None):
    """where the shared 'meyes' display stands for a mimic form (blocks), and its scale: the anchor carried as the form's own
    display carries its model (model units -> blocks, turned to face the way the form does), 0.8 of the head's width"""
    k = info['k'] if k is None else k
    F = info['F'] * k
    x, y, z = info['eyes']
    v = ((x / 16 - 0.5) * F, (y / 16 - 0.5) * F, (z / 16 - 0.5) * F)
    pos = (at[0] - v[0], at[1] + 1.5 * F + v[1], at[2] - v[2])
    eye_k = max(0.35, min(1.3, 0.8 * info['eye_w'] * info['F'] / 8.1)) * k
    return pos, eye_k


# which simplified signature move each mimicked form gets (the wiring stage maps every WHO key; these are the prototypes)
MOVES = {
    'emma': ('ribbon twirl', 'a spin; a ring of black ribbon-drips; 60% of her damage, no charm'),
    'bender': ('bite', 'a lunge and a snap (bite_up -> bite as whole-form motion), 60% damage; it spits a droplet after'),
    'kettle': ('steam puff', 'it squashes and puffs a jet of black droplets: a small knockback cone, no scald'),
    'gem': ('conjure', 'it floats up and drops a little black goo cube on the foe: 60% damage, no buff'),
    'ratking': ('decree', 'it rears, a goo sceptre-drip held up: Weakness I 3 s to one foe (his decree, without the rats)'),
    'killerwatt': ('static', 'its spikes bristle all over the form; one arc to the nearest foe at 50% damage'),
    'inkblot': ('splash', 'a splash of goo: Blindness 1 s (the ink blot\'s, shorter)'),
}
MIMIC_KEYS = {'emma': 'emma_ribbon', 'bender': 'bv_ball', 'kettle': 'kettle_plane', 'gem': 'creativity_gem', 'ratking': 'royal_marker',
              'killerwatt': 'kw_spark', 'inkblot': 'ink_pot'}
