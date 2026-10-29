"""2.99 (v299): THE SERAPH'S RAIMENT, redrawn - the holy twin of the Dreadborne (dread_set_art.py draws the Dread; phase206 the
set, phase182's Golden Cross the turning). "Each had six wings: with two they covered their faces, with two they covered their
feet, and with two they were flying" (Isaiah 6:2). Pearl and gold, sapphire, eyes in the feathers, burning edges, a halo.

THE WORN LAYERS (64 x 32, the pack's armour resolution - every other set's)
  humanoid  bm:seraph   (the Wings' plate, the Treads)  a pearl cuirass, lit from above and the left, its plates edged: a gold
            collar with a sapphire, an EYE in a gold sunburst on the breast, a gold sash, a fauld of gold-tipped feathers
            right round the waist; on the back two gold wing-mounts (rosettes set with sapphires, where the 3D wings root) and
            a gold spine; feathered pauldrons with an eye on each, vambraces with gold cuffs and a sapphire. The Treads: a ruff
            of feathers over the feet ("with two they covered their feet"), a sapphire anklet, a winglet on each outer ankle,
            gold toes.
  humanoid_leggings  bm:seraph   a gold belt with a sapphire buckle over feathered tassets; pearl cuisses with gold
            filigree, an eye on each knee cop.
  wings     bm:seraph_wings   the elytra mesh's wing (shown while gliding, under the 3D wings): a gold leading edge, coverts
            with eyes, flight feathers running back to burning tips.
THE SERAPH'S GAZE (3D, item model bm:item/seraph_helm - the item definition angel_dread_visage, as before)
  a pearl helm with a gold crest and circlet (a sapphire at the brow); WITH TWO THEY COVERED THEIR FACES: two wings from the
  temples, feather over feather, crossing over the whole face, their feathers full of eyes and burning at the tips; eyes
  open on its sides; a burning halo over it, set with eyes. Model space as the Dread Visage: a head filling 3..13, front north.
THE SPRITES  seraph_carapace / greaves / treads, drawn for themselves (not netherite recoloured).
The 3D great and lower wings that others see on a wearer of the Seraph's Wings are seraph_wings.py (they use these textures).
Every block texture here is 32 x 32 (1 px cells: two texels to a model unit, the Divine One's density)."""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import el

VAN = '/home/claude/mc263/client/assets/minecraft/textures'

# ---------------------------------------------------------------------------------------------------- the palette
WHITE = (255, 255, 255)
P1, P2, P3, P4, P5 = (244, 242, 252), (226, 222, 242), (200, 194, 228), (164, 154, 206), (112, 98, 162)     # pearl: light .. outline
G0, G1, G2, G3, G4 = (255, 246, 196), (252, 214, 96), (228, 172, 50), (172, 114, 28), (110, 66, 18)        # gold
S0, S1, S2, S3 = (176, 218, 255), (82, 142, 242), (36, 78, 198), (20, 38, 112)                          # sapphire
EYE_W, PUPIL = (250, 250, 255), (14, 16, 44)
F0, F1, F2, F3 = (255, 250, 214), (255, 214, 72), (255, 146, 36), (214, 80, 18)                          # holy fire
PAL = {'W': WHITE, 'p': P1, 'P': P2, 's': P3, 'S': P4, 'o': P5, 'y': G0, 'g': G1, 'G': G2, 'h': G3, 'H': G4,
       'b': S0, 'B': S1, 'n': S2, 'N': S3, 'e': EYE_W, 'k': PUPIL, 'f': F0, 'F': F1, 'r': F2, 'R': F3}


def _c(col, k=1.0, add=0, a=255):
    return tuple(max(0, min(255, int(v * k + add))) for v in col[:3]) + (a,)


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------------------------------------------------------------------------------------------------- the worn layers (64 x 32)
STRIP = {'body': (16, 24), 'arm': (40, 16), 'leg': (0, 16)}       # (the side strip of each box: right, front, left, back in a row)
FACE = {'body': {'right': (0, 4), 'front': (4, 8), 'left': (12, 4), 'back': (16, 8)},
        'arm': {'outer': (0, 4), 'front': (4, 4), 'inner': (8, 4), 'back': (12, 4)},
        'leg': {'outer': (0, 4), 'front': (4, 4), 'inner': (8, 4), 'back': (12, 4)}}
TOP = {'body': ((20, 16, 8, 4), (28, 16, 8, 4)), 'arm': ((44, 16, 4, 4), (48, 16, 4, 4)), 'leg': ((4, 16, 4, 4), (8, 16, 4, 4))}


class Layer:
    """a 64 x 32 armour layer painted box by box: strip coordinates (x along the strip that wraps round the box, y down from
    its top row, v 20) or a face's own (x across it, as seen from outside)"""
    def __init__(self):
        self.im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); self.px = self.im.load()

    def put(self, x, y, col):
        if 0 <= x < 64 and 0 <= y < 32: self.px[x, y] = col if len(col) == 4 else tuple(col) + (255,)

    def s(self, box, x, y, col):                      # strip
        x0, w = STRIP[box]
        self.put(x0 + x % w, 20 + y, col)

    def f(self, box, face, x, y, col):                # face
        a, w = FACE[box][face]
        if 0 <= x < w: self.s(box, a + x, y, col)

    def art(self, box, face, x, y, rows):             # ascii art on a face ('.' leaves what's there)
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != '.': self.f(box, face, x + i, y + j, PAL[ch])

    def top(self, box, which, fn):                    # the top (0) or bottom (1) face: fn(x, y, w, h) -> colour or None
        x0, y0, w, h = TOP[box][which]
        for y in range(h):
            for x in range(w):
                c = fn(x, y, w, h)
                if c: self.put(x0 + x, y0 + y, c)

    def get(self, box, x, y):
        x0, w = STRIP[box]; return self.px[x0 + x % w, 20 + y]


# every face drawn by hand (palette letters: PAL). Strips wrap each box: right/outer, front, left/inner, back; rows from v 20.
# Light falls from above and the viewer's left: the fronts' left columns lit, the sides and backs a step down, edges outlined.
BODY_CHEST = {   # (the Wings' cuirass: rows 0..11 of the body)
    'right': ['hGGh', 'sPPs', 'SPps', 'sgPs', 'Shps', 'SPPs', 'oSPs', 'hGGh', 'pWps', 'PsPS', 'gGgh', 'sPsS'],
    'front': ['HhGyyGhH',
              'SPWpypPS',
              'PWggggPS',
              'WgeBNegs',
              'pPhgghsS',
              'PpPhgsPS',
              'sPpshsSo',
              'hGgbnGhH',
              'pWpWpWPs',
              'PsPsPsSS',
              'gGgGgGhH',
              'sPsPsPSo'],
    'left': ['hGGh', 'sPPS', 'sPsS', 'sPgS', 'sPhS', 'sPsS', 'sSSo', 'hGhH', 'pPps', 'PsPS', 'gGhH', 'sPSo'],
    'back': ['HhGggGhH',
             'sgPhgPgs',
             'gBghhgBg',
             'shPhgPhs',
             'SPshgsPS',
             'SsPhgPsS',
             'oSshgSSo',
             'hGgyyGhH',
             'pPpPpPPs',
             'PsPsPsSS',
             'gGhGhGhH',
             'sSsSsSSo']}
ARM = {          # (the pauldrons: rows 0..5, an eye on the outer face; rows 6..7 bare; the vambraces: 8..11)
    'outer': ['hGyG', 'pWWp', 'PggP', 'eBNe', 'shhS', 'gGgh', '....', '....', 'hGGh', 'pbnP', 'PnNS', 'gyGh'],
    'front': ['GyGh', 'WpWs', 'PsPS', 'gGgh', 'pPpS', 'hGhH', '....', '....', 'hGGh', 'pWPs', 'PpsS', 'gyGh'],
    'inner': ['GgGh', 'pPps', 'sPsS', 'gGhh', 'sPsS', 'hGhH', '....', '....', 'hGhh', 'PPsS', 'sPSS', 'gGhH'],
    'back': ['GgGh', 'pPps', 'PsPS', 'gGhH', 'PsPS', 'hGhH', '....', '....', 'hGhH', 'PPsS', 'sPSS', 'gGhH']}
ARM_TOP = ['gyyg', 'yWpg', 'gpPh', 'ghhH']
FEET = {         # (the Treads: rows 6..11 of the legs - the ruff of feathers over the feet, the anklet, a winglet outside, gold toes)
    'outer': ['WWgh', 'pWyG', 'PpGh', 'bnGh', 'sPpP', 'HhGh'],
    'front': ['gyyg', 'WpWp', 'PsPs', 'gGgG', 'yggy', 'hGGh'],
    'inner': ['gGgh', 'pPps', 'sPsS', 'hGbn', 'PpsS', 'HhhH'],
    'back': ['hGgh', 'pWps', 'PsPS', 'gGhH', 'sPsS', 'HhhH']}
SOLE = ['hGGh', 'GSSG', 'GSSG', 'hGGh']
HIPS = {         # (the leggings' body rows 7..11: the belt and its sapphire buckle, the tassets)
    'right': ['hGGh', 'pWps', 'PsPS', 'gGgh', 'sPsS'],
    'front': ['hGgbngGh', 'pWpWpWPs', 'PsPsPsSS', 'gGgGgGhH', 'sPsPsPSo'],
    'left': ['hGhH', 'pPps', 'PsPS', 'gGhH', 'sPSo'],
    'back': ['hGhhGhhH', 'pPpPpPPs', 'PsPsPsSS', 'gGhGhGhH', 'sSsSsSSo']}
THIGH = {        # (the cuisses: leg rows 0..8 - filigree outside, an eye on each knee cop)
    'outer': ['hGGh', 'pWPs', 'Wgps', 'pgPs', 'Pghs', 'sPgS', 'PsgS', 'sPsS', 'hGhH'],
    'front': ['hGGh', 'WppP', 'pWPs', 'hggh', 'eBNe', 'hggh', 'pPsS', 'PsSS', 'hGhH'],
    'inner': ['hGhH', 'pPPs', 'PPsS', 'PsSS', 'sPsS', 'PsSS', 'sSSo', 'SsSo', 'hHhH'],
    'back': ['hGhH', 'pPPs', 'PPgS', 'PsgS', 'sPhS', 'PsgS', 'sShS', 'SsSo', 'hHhH']}
THIGH_TOP = ['hGGh', 'GpPG', 'GPsG', 'hGGh']
CHEST_TOP = ['hGGyyGGh', 'pWWppPPs', 'PpPPPPss', 'hGGhhGGh']


def _faces(L, box, table, y0, mirror_faces=()):
    for face, rows in table.items():
        L.art(box, face, 0, y0, rows)


def _top(L, box, which, rows):
    L.top(box, which, lambda x, y, w, h: PAL[rows[y][x]] if rows[y][x] != '.' else None)


def humanoid():
    """bm:seraph humanoid: the Wings' plate (body, arms) and the Treads (the legs' feet)"""
    L = Layer()
    _faces(L, 'body', BODY_CHEST, 0)
    _top(L, 'body', 0, CHEST_TOP)
    _faces(L, 'arm', ARM, 0)
    _top(L, 'arm', 0, ARM_TOP)
    _faces(L, 'leg', FEET, 6)
    _top(L, 'leg', 1, SOLE)
    return L.im


def leggings():
    """bm:seraph humanoid_leggings: the belt and its tassets, the cuisses with an eye on each knee"""
    L = Layer()
    _faces(L, 'body', HIPS, 7)
    _faces(L, 'leg', THIGH, 0)
    _top(L, 'leg', 0, THIGH_TOP)
    return L.im


def wings_layer():
    """bm:seraph_wings: the elytra mesh's wing - its back face (36..46 x 2..22: col 0 the leading edge at the shoulder, col 9
    the trailing edge; row 0 the root, row 19 the tip) as a feathered seraph wing: a gold leading edge, coverts, flight
    feathers in soft bands running back to gold tips, fire only along the trailing edge and at the tip, three eyes. Its
    edges are left as vanilla leaves them (a thin line), so the mesh reads as a sheet, not a slab; the front face is clear
    (drawn through, as vanilla's). It ends at LEN rows of the mesh's 20: the far end is all the mesh shows past the 3D wings
    (in a crouch it flares out under them; gliding, it lies well inside their span)."""
    im = Image.new('RGBA', (64, 32), (0, 0, 0, 0)); px = im.load()
    X0, Y0, LEN = 36, 2, 7
    lead = [0, 0, 0, 0, 0, 1, 1]                                                 # (the leading edge sweeps back a little)
    put = lambda c, r, col: px.__setitem__((X0 + c, Y0 + r), tuple(col) + (255,))
    for r in range(LEN):
        s0 = lead[r]
        for c in range(s0, 10):
            k = c - s0
            if k == 0: col = G0 if r % 4 == 0 else G1                                         # the leading edge
            elif k == 1: col = G3 if r % 2 else G2
            elif k <= 3: col = [WHITE, P1, P2][r % 3] if k == 2 else [P1, P2, P3][r % 3]       # coverts
            else:
                col = [P1, P2, P3][r % 3] if c < 8 else ([G1, G2, G3][r % 3] if c == 8 else [F0, F1, F2][r % 3])
                if k == 4 and r % 3 == 2: col = P4                                              # (the coverts' shadow on the flights)
            if r >= LEN - 3 and c >= 4 + (LEN - 1 - r): col = [F1, F0, F2][(r + c) % 3]          # (the end, burning)
            if r == LEN - 1 and c < 4: col = G3
            put(c, r, col)
    for (r, c) in ((2, 5), (4, 7)):                                                           # eyes in the feathers
        put(c - 1, r, EYE_W); put(c, r, S1); put(c + 1, r, EYE_W); put(c, r - 1, G1); put(c, r + 1, G3)
    # (its edges left clear: in a crouch the mesh flares out past the 3D wings, and a painted edge shows there as a stick)
    return im


# ---------------------------------------------------------------------------------------------------- the 3D pieces' textures (32 x 32)
def _paint(fn, seed, size=32):
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); px = im.load()
    for y in range(size):
        for x in range(size):
            c = fn(x, y, rnd); px[x, y] = c if len(c) == 4 else tuple(c) + (255,)
    return im


def _pearl(seed, k=1.0):
    """pearl plate: a fine grain of light and shade, rose and ice in it, a lit lip every 8 rows"""
    def c(x, y, r):
        b = P2 if r.random() > 0.3 else (P1 if r.random() > 0.4 else P3)
        q = r.random()
        if q < 0.07: b = _mix(b, (238, 222, 248), 0.7)
        elif q < 0.13: b = _mix(b, (218, 236, 252), 0.7)
        if y % 8 == 0: b = _mix(b, WHITE, 0.6)
        if y % 8 == 7: b = _mix(b, P4, 0.5)
        return _c(b, k)
    return _paint(c, seed)


SCROLL = ['..GGGG..', '.G....G.', 'G..GG..G', 'G.G..G.G', 'G.G...G.', '.G.GGG..', '..G.....', '...GG...']


def _gold(seed, bright=False):
    """gold, worked in filigree: a scroll repeated in light lines on it (bright: lit from within - the halo, the edges)"""
    base = [G1, G1, G0] if bright else [G2, G2, G1, _mix(G2, G3, 0.4)]
    def c(x, y, r):
        if SCROLL[y % 8][x % 8] == 'G': return _c(WHITE if bright and r.random() < 0.3 else (G0 if bright else G3))
        return _c(r.choice(base))
    return _paint(c, seed)


def _saph(seed):
    def c(x, y, r):
        if (x + y) % 8 == 0: return _c(S0)
        if (x - y) % 8 == 0: return _c(S3)
        return _c(r.choice((S1, S1, S2, _mix(S1, S0, 0.4))))
    return _paint(c, seed)


def _eye(seed=0, lid=G2):
    """an eye (whole uv): an almond of white in gold lids, a sapphire iris with a dark pupil, a glint"""
    def c(x, y, r):
        dx, dy = (x - 15.5) / 15.0, (y - 15.5) / 9.0
        a = abs(dy) + dx * dx * 0.9                                   # (the almond)
        if a > 1.15: return _c(_mix(lid, G3, 0.3) if r.random() < 0.3 else lid)
        if a > 0.95: return _c(G4 if dy < 0 else G3)                  # (the lash line)
        d = math.hypot(x - 15.5, y - 15.5)
        if d < 3.2: return _c(PUPIL)
        if d < 7.5: return _c(_mix(S0, S2, (d - 3.2) / 4.3)) if (x + y) % 5 else _c(S1)
        if d < 8.3: return _c(S3)
        return _c(EYE_W if dy > -0.5 else _mix(EYE_W, P3, 0.4))
    im = _paint(c, seed); d = ImageDraw.Draw(im)
    d.rectangle((11, 10, 13, 12), fill=_c(WHITE))                     # (the glint)
    return im


def _feather(seed, dark=False, eye=False):
    """a flight feather (whole uv, its length down v): a gold-white shaft, the vane in barbs slanting off it, lit on one side
    and shaded on the other, its edges darker (so feathers side by side read apart); eye: an eye in the vane"""
    lo, mid, hi = (P3, P2, P1) if dark else (P2, P1, WHITE)
    def c(x, y, r):
        if x in (15, 16): return _c(_mix(G1, WHITE, 0.45) if y > 2 else G2)
        if x <= 1 or x >= 30: return _c(_mix(lo, P4, 0.6))
        left = x < 15
        u = (x if left else 31 - x)
        if (y + (15 - u) // 2) % 5 == 0: return _c(_mix(lo, P4, 0.35))                 # (the barbs)
        b = (hi if r.random() > 0.2 else mid) if left else (mid if r.random() > 0.25 else lo)
        if y < 3: b = _mix(b, P4, 0.4)                                                   # (the root, tucked under)
        return _c(b)
    im = _paint(c, seed)
    if eye:
        e = _eye(seed + 1, lid=G1).resize((20, 12), Image.NEAREST)
        im.alpha_composite(e, (6, 11))
    return im


def _covert(seed, eye=False, full=False):
    """coverts: rows of small rounded feathers (8 x 6 each, staggered), lit on top, gold at the tip; eye: some are eyes"""
    def c(x, y, r):
        row = y // 6; sx = (x + (row % 2) * 4) % 8; sy = y % 6
        if full and (x <= 1 or x >= 30): return _c(P4)
        if sy == 5: return _c(G2 if sx in (2, 3, 4, 5) else G3)
        if sx in (0, 7): return _c(P3)
        if sy == 0: return _c(WHITE)
        return _c(P1 if sx < 4 else P2)
    im = _paint(c, seed)
    if eye:
        e = _eye(seed + 3, lid=G1).resize((8, 5), Image.NEAREST)
        for (ex, ey) in ((0, 0), (16, 12), (4, 24), (20, 0)):
            im.alpha_composite(e, (ex, ey))
    return im


def _flame(seed):
    """a burning tip (whole uv, along v): gold at its root running to orange, tongues of white-gold fire at its end, gaps
    between the tongues (cut out)"""
    def c(x, y, r):
        t = y / 31
        tongue = 22 + 6 * abs(math.sin(x * 0.55 + seed)) + r.random() * 3
        if y > tongue: return (0, 0, 0, 0)
        if t < 0.3: b = _mix(G1, F1, t / 0.3)
        else: b = _mix(F1, F2, min(1, (t - 0.3) / 0.4))
        if y > tongue - 4: b = _mix(b, F0, 0.7)
        if r.random() < 0.08: b = F0
        return _c(b)
    return _paint(c, seed)


def _light(seed):
    return _paint(lambda x, y, r: _c(r.choice((G0, G0, WHITE, G1, (255, 236, 160)))), seed)


def textures():
    return {'sr_pearl': _pearl(2991), 'sr_pearl_d': _pearl(2992, 0.88), 'sr_gold': _gold(2993), 'sr_gold_l': _gold(2994, True),
            'sr_saph': _saph(2995), 'sr_eye': _eye(2996), 'sr_feather': _feather(2997), 'sr_feather_d': _feather(2998, dark=True),
            'sr_feather_eye': _feather(2999, eye=True), 'sr_covert': _covert(3001), 'sr_covert_eye': _covert(3002, eye=True),
            'sr_flame': _flame(3003), 'sr_light': _light(3004)}


# ---------------------------------------------------------------------------------------------------- building (rigkit elements, model units)
NOSHIFT = {'sr_eye', 'sr_feather', 'sr_feather_d', 'sr_feather_eye', 'sr_flame'}
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
_rs = random.Random(29)


def E(fr, to, tex, pv, light=0, shade=True, **kw):
    if tex not in NOSHIFT and 'shift' not in kw and 'uv' not in kw: kw['shift'] = (_rs.random(), _rs.random())
    e = el(fr, to, tex, pv, light=light, **kw)
    if not shade: e['shade'] = False
    return e


def FULL():
    """the whole texture down a SEG's length on its broad faces"""
    return {'up': [0, 0, 16, 16], 'down': [0, 16, 16, 0], 'east': [0, 0, 1, 16], 'west': [0, 0, 1, 16], 'north': [0, 0, 16, 1], 'south': [0, 0, 16, 1]}


def SEG(A, B, w, h, tex, pv, up=UP, ext=0.0, light=0, shade=True, uv=None):
    """a box w across by h (toward `up`) from A to B; its 'up' face the broad one, its v running from A to B"""
    S_ = lambda a, b: tuple(a[i] - b[i] for i in range(3))
    x, y, z = rigkit.frame(S_(B, A), up)
    L = math.sqrt(sum(v * v for v in S_(B, A))) / 2 + ext; m = tuple((A[i] + B[i]) / 2 for i in range(3))
    ang = rigkit.euler([[x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]]])
    fr, to = (m[0] - w / 2, m[1] - h / 2, m[2] - L), (m[0] + w / 2, m[1] + h / 2, m[2] + L)
    kw = {} if (uv is not None or tex in NOSHIFT) else {'shift': (_rs.random(), _rs.random())}
    return E(fr, to, tex, pv, light=light, shade=shade, uv=uv, rot=None if max(abs(v) for v in ang) < 1e-3 else (ang, m), **kw)


def GEM(c, s, tex, pv, light=15, rot=(35.26, 45.0, 0.0)):
    return E((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, pv, light=light, rot=(rot, c))


def FEATHER(root, tip, w, tex, pv, up, burn=0.32, light_tip=15, h=0.36):
    """a feather from root to tip: its vane (tex), then the burning end (sr_flame, lit) - burn: the share of its length on fire"""
    m = tuple(root[i] + (tip[i] - root[i]) * (1 - burn) for i in range(3))
    return [SEG(root, m, w, h, tex, pv, up, uv=FULL()), SEG(m, tip, w * 0.92, h * 0.9, 'sr_flame', pv, up, light=light_tip, shade=False, uv=FULL())]


def EYEBOX(c, w, h, normal, pv, d=0.3, light=9):
    """an eye set in a surface facing `normal` (its 'up' face the eye)"""
    n = normal
    side = rigkit._unit(rigkit._cross(n, (0.0, 1.0, 0.0) if abs(n[1]) < 0.9 else (1.0, 0.0, 0.0)))
    A = tuple(c[i] - side[i] * w / 2 for i in range(3)); B = tuple(c[i] + side[i] * w / 2 for i in range(3))
    return SEG(A, B, h, d, 'sr_eye', pv, n, light=light,
               uv={'up': [0, 16, 16, 0], 'down': [0, 0, 16, 16], 'north': [0, 0, 1, 1], 'south': [0, 0, 1, 1], 'east': [0, 0, 1, 1], 'west': [0, 0, 1, 1]})


# ---------------------------------------------------------------------------------------------------- the Seraph's Gaze (3D)
def _set_eye(c, w, h, n, pv, light=10, rim=0.45):
    """an eye in a gold setting, flush in a surface facing n"""
    return [SEG(*_across(c, w + rim, n, -0.12), h + rim, 0.3, 'sr_gold', pv, n), EYEBOX(c, w, h, n, pv, d=0.36, light=light)]


def _across(c, w, n, dn=0.0):
    side = rigkit._unit(rigkit._cross(n, (0.0, 1.0, 0.0) if abs(n[1]) < 0.9 else (1.0, 0.0, 0.0)))
    c = tuple(c[i] + n[i] * dn for i in range(3))
    return tuple(c[i] - side[i] * w / 2 for i in range(3)), tuple(c[i] + side[i] * w / 2 for i in range(3))


def helm_model():
    """drawn for a head filling 3..13 (front north, -z): the helm, its crest and circlet; the face's two crossed wings; eyes;
    the burning halo"""
    pv = (8.0, 8.0, 8.0); _rs.seed(2990)
    H = []
    H.append(E((3.0, 2.8, 3.2), (13.0, 12.4, 13.0), 'sr_pearl', pv))                          # the helm
    for (x0, x1, z0, z1) in ((2.7, 13.3, 3.6, 12.6), (3.4, 12.6, 2.9, 13.3)):                 # (its corners bevelled: two crossed slabs)
        H.append(E((x0, 3.2, z0), (x1, 12.0, z1), 'sr_pearl', pv))
    H.append(E((3.6, 12.4, 3.8), (12.4, 13.6, 12.4), 'sr_pearl', pv))                         # its crown, stepped
    H.append(E((4.8, 13.6, 5.0), (11.2, 14.3, 11.4), 'sr_pearl_d', pv))
    H.append(E((7.3, 12.6, 2.9), (8.7, 15.0, 13.1), 'sr_gold', pv))                           # the gold crest, brow to nape
    H.append(E((7.65, 15.0, 4.0), (8.35, 15.6, 12.2), 'sr_gold_l', pv, light=8))
    H.append(E((2.5, 10.6, 2.6), (13.5, 11.8, 13.4), 'sr_gold', pv))                          # the circlet
    H.append(E((6.4, 10.4, 2.35), (9.6, 12.4, 2.7), 'sr_gold', pv))                           # its brow-piece
    H.append(GEM((8.0, 11.4, 2.3), 1.5, 'sr_saph', pv, light=11))                             # a sapphire at the brow
    H.append(E((2.6, 2.5, 10.6), (13.4, 6.0, 13.6), 'sr_pearl_d', pv))                        # the nape guard, gold-edged
    H.append(E((2.5, 2.3, 10.8), (13.5, 2.9, 13.8), 'sr_gold', pv))
    H.append(E((7.4, 2.9, 13.3), (8.6, 10.6, 13.7), 'sr_gold', pv))                           # a gold spine down the back
    for sx in (-1, 1):                                                                        # cheek plates, gold-edged
        x0, x1 = (2.3, 3.1) if sx < 0 else (12.9, 13.7)
        H.append(E((x0, 3.0, 3.0), (x1, 10.4, 8.6), 'sr_pearl', pv))
        H.append(E((x0 - 0.05, 2.8, 2.8), (x1 + 0.05, 3.4, 8.8), 'sr_gold', pv))
        H.append(E((x0 - 0.05, 3.0, 8.4), (x1 + 0.05, 10.4, 8.9), 'sr_gold', pv))
    # eyes open on its sides and back, each in a gold setting
    for (x, y, z, n) in ((2.2, 6.4, 10.6, (-1, 0, 0)), (13.8, 6.8, 10.4, (1, 0, 0)), (2.2, 9.0, 5.8, (-1, 0, 0)), (13.8, 8.6, 6.0, (1, 0, 0)),
                         (5.4, 8.0, 13.25, (0, 0, 1)), (10.6, 8.0, 13.25, (0, 0, 1)), (8.0, 12.9, 13.0, (0, 0.5, 1))):
        H += _set_eye((x, y, z), 2.1, 1.2, rigkit._unit(n), pv)
    H = rigkit.transform(H, lambda v: [8 + (v[0] - 8) * 1.1, 7.6 + (v[1] - 7.6) * 1.1, 8 + (v[2] - 8) * 1.1])   # (the shell clear of the hat layer)
    # WITH TWO THEY COVERED THEIR FACES: two wings folded corner to corner across the face in an X (the helm's right wing laid
    # over its left): each three long feathers lying side by side down its length, a gold leading edge along its upper side,
    # coverts and a sapphire at its root on the temple, the feathers' ends staggered and burning at the far cheek
    for sx in (1, -1):                                                                        # (+1: from the helm's left temple (x 13), laid first, under)
        zb = 1.95 if sx > 0 else 1.25
        R0, T0 = (8 + sx * 5.3, 11.4), (8 - sx * 4.9, 3.3)
        dx, dy = T0[0] - R0[0], T0[1] - R0[1]; Ln = math.hypot(dx, dy); dx, dy = dx / Ln, dy / Ln
        nx, ny = -dy * sx, dx * sx                                                            # (toward the wing's upper side)
        if ny < 0: nx, ny = -nx, -ny
        for k, (off, s0, s1, tex) in enumerate(((1.45, 0.05, 1.0, 'sr_feather'), (0.0, 0.0, 0.92, 'sr_feather_eye'), (-1.45, 0.08, 0.82, 'sr_feather_d'))):
            z = zb - 0.14 * k
            A = (R0[0] + nx * off + dx * Ln * s0, R0[1] + ny * off + dy * Ln * s0, z)
            B = (R0[0] + nx * off + dx * Ln * s1, R0[1] + ny * off + dy * Ln * s1, z)
            H += FEATHER(A, B, 1.7, tex, pv, FRONT, burn=0.27)
        e0 = (R0[0] + nx * 2.25, R0[1] + ny * 2.25, zb + 0.05)                                 # the leading edge
        H.append(SEG(e0, (e0[0] + dx * Ln * 0.62, e0[1] + dy * Ln * 0.62, zb + 0.05), 0.75, 0.75, 'sr_gold', pv, FRONT, ext=0.2))
        for j, (o, a0, a1, tex) in enumerate(((1.5, -0.3, 2.6, 'sr_covert'), (0.2, 0.2, 3.2, 'sr_feather_eye'), (-1.1, 0.0, 2.4, 'sr_covert'))):
            z = zb - 0.5 - 0.1 * j                                                            # (coverts over the feathers' roots)
            H.append(SEG((R0[0] + nx * o + dx * a0, R0[1] + ny * o + dy * a0, z), (R0[0] + nx * o + dx * a1, R0[1] + ny * o + dy * a1, z),
                         1.6, 0.35, tex, pv, FRONT, uv=FULL()))
        H.append(GEM((R0[0] + nx * 2.1, R0[1] + ny * 2.1, zb - 0.35), 0.95, 'sr_saph', pv, light=11))
    # the burning halo over it, tilted back: a ring of light, tongues of fire off it, four eyes set in it
    c, R, n = (8.0, 17.2, 9.0), 5.2, 20
    tilt = math.radians(16)
    def hp(a, r=R, dy=0.0):
        x, z = r * math.cos(a), r * math.sin(a)
        return (c[0] + x, c[1] + dy - z * math.sin(tilt), c[2] + z * math.cos(tilt))
    up_t = (0.0, math.cos(tilt), math.sin(tilt))
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        H.append(SEG(hp(a0), hp(a1), 1.0, 0.55, 'sr_gold_l', pv, up_t, ext=0.14, light=15, shade=False))
        H.append(SEG(hp(a0, R - 0.95), hp(a1, R - 0.95), 0.35, 0.45, 'sr_light', pv, up_t, ext=0.1, light=15, shade=False))
        if i % 2 == 0:                                                                        # tongues of fire up off it
            a = (a0 + a1) / 2; b = hp(a, dy=0.2)
            H.append(SEG(b, (b[0], b[1] + (1.7 if i % 4 == 0 else 1.1), b[2] + 0.25), 0.55, 0.55, 'sr_flame', pv, FRONT, light=15, shade=False, uv=FULL()))
    for a in (math.pi * 1.5, math.pi * 0.5, 0.0, math.pi):
        p = hp(a, dy=0.05); nn = rigkit._unit((math.cos(a) * 0.9, 0.15, math.sin(a) * 0.9))
        if a == math.pi * 1.5: nn = (0.0, 0.1, -1.0)
        H.append(EYEBOX(p, 1.6, 1.0, rigkit._unit(nn), pv, d=0.62, light=13))
    return H


def helm_json(display):
    els = helm_model()
    for e in els:
        for v in e['from'] + e['to']: assert -16 <= v <= 32, e
        for fc in e['faces'].values(): fc['uv'] = [max(0.0, min(16.0, u)) for u in fc['uv']]
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    return {'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/sr_pearl'), 'elements': els, 'display': display}


# ---------------------------------------------------------------------------------------------------- the sprites
def _sprite(rows):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); px = im.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.': px[x, y] = PAL[ch] + (255,)
    return im


ICON_ROWS = {   # (on vanilla's chestplate / leggings / boots silhouettes, drawn over)
    'seraph_carapace': [            # the Wings: a pearl cuirass, the eye on its breast, a wing rising behind each shoulder
        'yW............Wy',
        'gWp..........pWg',
        'Wooooo....oooooW',
        'pogygo....ogygop',
        'PoWpPoh..hopPsoP',
        'soWpPghyyhgpPsos',
        'SopWPsgggPpPsoSS',
        'FooWpPggggPsSooF',
        'r..opgeBNegSo..r',
        '...oPphgghPSo...',
        '...ohGgbngGho...',
        '...oWpWpWpPso...',
        '...ogGgGgGhHo...',
        '....ooPsPsoo....',
        '.....oooooo.....',
        '................'],
    'seraph_greaves': [             # the Greaves: belt and sapphire buckle, feathered tassets, an eye on each knee
        '................',
        '................',
        '....oooooooo....',
        '...ohGgbngGho...',
        '...oWpWpWpPso...',
        '...ogGgGgGhHo...',
        '...oWpPoopPso...',
        '...oWpo..oPso...',
        '...opPo..opSo...',
        '...oggo..oggo...',
        '...oeBo..oBeo...',
        '...ohho..ohho...',
        '...oPso..oPSo...',
        '...oooo..oooo...',
        '................',
        '................'],
    'seraph_treads': [              # the Treads: winglets at the ankles, feathers over the feet, sapphire anklets, gold toes
        '................',
        '.y............y.',
        '.gW..........Wg.',
        '.hWgo......ogWh.',
        '..hoWo....oWoh..',
        '...oPo....oPo...',
        '...oWpo..opWo...',
        '...oPso..osPo...',
        '...obno..onbo...',
        '..oWpPo..oPpWo..',
        '.oyWpPo..oPpWyo.',
        '.oygPoo..ooPgyo.',
        '.hhHH......HHhh.',
        '................',
        '................',
        '................'],
}


def icons():
    return {k: _sprite(v) for k, v in ICON_ROWS.items()}
