"""THE LIGHTBRINGER (a draft for the owner's approval: rig, textures, faces, poses) - a herald of the Divine One.

WHO   The Dread - the eldritch corruption behind hard mode, its Dread mobs and Dread Nights and the three Dread bosses - has a
      counterweight coming, and she is its first light: a herald and premonition of the Divine One, sent ahead to offset the
      Dread. She is not the Divine One, only the dawn before it. Solemn, serene and kind; quietly fierce against the Dread and
      the undead. She loves it when you wear holy things - the Holy-forged pieces (phase182) and the Seraph's Raiment - and
      lights up for them (behaviour for later wiring: a happy face, a little bless, a remark).

LOOK  A young woman, an angel, a little shorter than a player, in the pack's blocky humanoid style (the royal family's build:
      Emma's head and face scale). TRANSLUCENT, white and gold (the owner's direction): her robes, skin, hair and the pearl of
      her wings are see-through light (partial alpha), while what has to read stays solid - the face's features and her
      gold-lit eyes, every gold trim, the halo, the staff. Royal blue and royal purple only as accents: the sash, the purple
      stole down her front, the cuffs, the staff's gems, a blue edge on the primaries' tips.
      - A long pearl-white robe falling in tiers to just above her feet, gold at the hem (a fine blue line above it), a royal
        purple stole edged in gold hanging straight down the middle from under the gold collar, a royal blue sash with a
        gold clasp, a small gold sun on the stole at her breast.
      - Pale-gold hair with bright gold strands, very long and stylised: a crown of hair in soft steps (and stepped out at
        the back) so the head isn't a cube; a fringe parted in the middle with pointed locks over her brow (the face kept
        clear); long locks framing her face and falling on in front of her shoulders to the breast; down her back between
        the wings a full fall, gathered at the shoulder blades in a gold clasp with a sapphire, then parting into three
        layered locks - the middle one to a point at the backs of her knees, the two beside it swaying out and flipping up.
        Every tip glows gold (lit, like the wing tips).
      - A glowing gold halo floating above her head (light 15).
      - Two large wings of light behind her shoulders: a band of coverts along the leading edge, then secondaries and long
        primaries hanging in one layer, pearl-white running to gold tips (glowing). They are rooted on her back, outside her
        hair, and swept back so the arms swing clear of them.
      - Gentle face: big gold eyes (an emissive overlay over each open eye, so they glow in the dark), soft brows, a blush.
      - Her weapon: a STAFF OF LIGHT (not a sword - she is support first: bless, ward, then smite). A gold staff a little
        taller than she is, a sapphire band under its head, a gold ring holding a glowing core of light, an amethyst finial.
        She raises it to call a beam down (smite), plants it to bless and ward.

MOTION  She HOVERS: standing poses lift her clear of the ground (_off y = HOVER, with a slow bob), her toes pointing down
      below the hem. She glides rather than walks; running is a low flight with her wings beating. She only touches the
      ground to kneel - sitting, praying and fainting set her down on her robe (the 'pool': the robe spread on the floor).

RIG (rigkit) body (the hips: bodice, sash, the robe's upper tiers), skirt (the robe's lower tiers - hidden when she kneels,
      the pool shows instead), head (a model per expression), halo (on the head), hair (the long fall down her back, on the
      body: nape to waist) and hairlo (its three locks, waist to knees - a second joint, so it streams back in flight and
      drapes back over the robe when she kneels), the arms bent at the elbow, the staff (in her right hand), the two wings (on the body, each its own joint), the
      feet (on their own, from the ankle). Design units: feet at y=0, facing -z, her right is +x. RIG_SCALE 0.84: the top of
      her head stands at 1.70 blocks, the halo's top at 1.86.

TRANSLUCENT textures (alpha < 255): lb_robe and lb_bodice (178), lb_skin (205: hands, neck, the head's sides), lb_hair (212; its tips, lb_hairtip, are solid
      and lit), lb_feather and lb_covert (186). Everything else is solid - the face plate (lb_face*) too, so she reads clearly. Faces covered by a neighbour are left off (the robe's tiers have no tops
      - a ring of gold or pearl steps out over each one instead; the hair has no faces turned in to the head), so nothing
      inside shows through the glassy parts.

(3.0) HE: the male form - every part's '_m' twin (MALE; rigpet's FORM puts them on), below the textures and models: same rig,
      poses and faces; broad shoulders, a gold-collared surcoat, pauldrons and vambraces, a gold-edged purple tabard front and back
      (the back on the 'hair' joints), a straight long tunic, armoured feet, short cropped hair, ears, a heavy brow and a square jaw.
      Preview: tools/preview/lightbringer_male.py."""
import math
import random
from PIL import Image, ImageDraw

from phase57_art import hexc
from rigkit import qs, el, seg, chain, solve, qmul

PREFIX = 'lb_'
RIG_SCALE = 0.84
HOVER = 1.6                                         # (design units off the ground in her floating poses)
UP, FRONT = (0.0, 1.0, 0.0), (0.0, 0.0, -1.0)
HB, HT = 24.4, 32.4                                 # the head's bottom and top
PIVOT = {'body': (0, 13.0, 0), 'skirt': (0, 5.6, 0), 'head': (0, HB, 0), 'halo': (0, HT + 3.6, 0.5), 'hair': (0, 24.6, 3.5), 'hairlo': (0, 14.6, 3.45),
         'armr': (4.45, 23.0, 0), 'forer': (4.9, 18.6, 0), 'arml': (-4.45, 23.0, 0), 'forel': (-4.9, 18.6, 0),
         'staff': (5.1, 13.3, -0.05), 'wingr': (3.2, 19.8, 3.0), 'wingl': (-3.2, 19.8, 3.0),
         'legr': (1.3, 1.0, 0.2), 'legl': (-1.3, 1.0, 0.2), 'pool': (0, 0.0, 0)}
PARENT = {'body': None, 'skirt': 'body', 'head': 'body', 'halo': 'head', 'hair': 'body', 'hairlo': 'hair', 'armr': 'body', 'forer': 'armr',
          'arml': 'body', 'forel': 'arml', 'staff': 'forer', 'wingr': 'body', 'wingl': 'body', 'legr': None, 'legl': None, 'pool': None}
PARTS = tuple(PIVOT)
PART_K = {}
JOINTS = {}                                         # (model -> {element index: parts it grows out of} - for the preview's clip check)
FACES = ('happy', 'fierce', 'sad', 'blink', 'surprised', 'hurt')
OPEN_EYES = (None, 'fierce', 'sad', 'surprised')     # (the faces whose eyes glow)

# white and gold; royal blue and purple for accents (the Holy forging's palette, phase182 / dread_set_art)
PEARL, PEARL_D, PEARL_L = '#f0edf9', '#cfc8e6', '#ffffff'
GOLD, GOLD_D, GOLD_L, GOLD_W = '#e8b630', '#a8741a', '#ffe478', '#fff6c8'
ROYAL, ROYAL_D, ROYAL_L = '#3a5ad8', '#20307e', '#6a8cff'
PURPLE, PURPLE_D, PURPLE_L = '#6a3cc0', '#3e1e7a', '#9a72e6'
SKIN, SKIN_D = '#fbe8da', '#e8c8b4'
HAIR, HAIR_D, HAIR_L = '#f2dc96', '#c8a456', '#fff4c4'
A_ROBE, A_SKIN, A_HAIR, A_FEATHER = 178, 205, 212, 186  # (her translucency, out of 255)


def HIDDEN(p, pose):
    if p == 'pool': return not pose.get('_pool')
    if p == 'skirt': return bool(pose.get('_pool'))
    if p in ('legr', 'legl'): return bool(pose.get('_pool') or pose.get('_swim'))
    if p == 'staff': return pose.get('_staff') == 'none'
    return p in pose.get('_hide', ())


def model_name(p, pose, suffix=''):
    face = f'_x{pose["_face"]}' if p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _cells(fn, seed, cell=2, alpha=255):
    """a 64 px texture painted in square cells half a unit across (the pack's blocky look): fn(cx, cy, rnd) -> colour"""
    im = Image.new('RGBA', (64, 64)); d = ImageDraw.Draw(im); rnd = random.Random(seed); n = 64 // cell
    for cy in range(n):
        for cx in range(n):
            c = fn(cx, cy, rnd)
            d.rectangle((cx * cell, cy * cell, cx * cell + cell - 1, cy * cell + cell - 1), fill=hexc(c, alpha) if isinstance(c, str) else c)
    return im


def _mix(a, b, t):
    a, b = hexc(a), hexc(b)
    return '#%02x%02x%02x' % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _shade(base, var, seed, p=0.22, alpha=255):
    return _cells(lambda x, y, r: r.choice(var) if r.random() < p else base, seed, alpha=alpha)


def _robe(seed, alpha=A_ROBE):
    """pearl silk: long soft folds (a paler crest beside a shaded crease every few cells), a sheen of white"""
    folds = {3: PEARL_D, 4: PEARL_L, 10: _mix(PEARL, PEARL_D, 0.6), 11: PEARL_L, 17: PEARL_D, 18: PEARL_L, 25: _mix(PEARL, PEARL_D, 0.6), 26: PEARL_L}
    def c(x, y, r):
        if x in folds and r.random() < 0.85: return folds[x]
        return r.choice((PEARL, PEARL, PEARL, PEARL_L, _mix(PEARL, PEARL_D, 0.35)))
    return _cells(c, seed, alpha=alpha)


def _gold(seed):
    """gold trim: bright, a running diagonal glint, darker cells at the edges of each band"""
    def c(x, y, r):
        if (x + y) % 7 == 0: return GOLD_W
        if (x - y) % 9 == 0: return GOLD_D
        return r.choice((GOLD, GOLD, GOLD, GOLD_L, _mix(GOLD, GOLD_D, 0.4)))
    return _cells(c, seed)


def _hem(seed):
    """the hem band: gold, a fine royal blue line along its top (rows 0-1: the band's top edge)"""
    im = _gold(seed); d = ImageDraw.Draw(im)
    for y0 in range(0, 64, 16):                                            # (each band is 3.2 units tall at most: blue every 4)
        d.rectangle((0, y0, 63, y0 + 1), fill=hexc(ROYAL))
    return im


def _stole_v(seed):
    """the stole's strips over her breast: a 6 px window - gold edges (cells 0 and 2), purple between, a gold fleck every 4 units"""
    def c(x, y, r):
        if x % 3 != 1: return GOLD if (y % 3) else GOLD_L
        if y % 8 == 4: return GOLD_L
        return r.choice((PURPLE, PURPLE, PURPLE_L, PURPLE_D))
    return _cells(c, seed)


def _bodice(seed):
    """the bodice's front: plain pearl silk (the gold collar is her neckline; the stole and the sun sit over it)"""
    return _robe(seed)


def _skin(seed):
    return _shade(SKIN, (SKIN_D, '#fff2e8'), seed, 0.18, alpha=A_SKIN)


def _hair(seed):
    """pale gold, in falling strands: each column a strand, lit and shaded in runs, every few a bright gold highlight"""
    def c(x, y, r):
        if x % 5 == 2 and (y // 4) % 3 != 1: return GOLD_L                     # (the bright gold strands)
        k = (x * 7 + (y // 3) * 3) % 5
        return (HAIR, HAIR_L, HAIR, HAIR_D, HAIR)[k] if r.random() > 0.12 else _mix(HAIR, HAIR_L, 0.5)
    return _cells(c, seed, alpha=A_HAIR)


def _hairtip(seed):
    """a lock's tip: pale gold running to white-gold light down its length (lit, like the feathers' tips)"""
    def c(x, y, r):
        t = min(1.0, y / 20)
        if x % 5 == 2: return GOLD_W
        return _mix(GOLD_L, GOLD, t * 0.6) if r.random() > 0.2 else GOLD_W
    return _cells(c, seed)


def _feather(seed):
    """a feather's broad face (a 6 px window across, the length down it): pearl vanes, a pale gold shaft down the middle
    (cols 2-3), the barbs' lines slanting off it"""
    def c(x, y, r):
        xx = x % 3
        if xx == 1: return _mix(PEARL_L, GOLD_L, 0.45)
        if y % 3 == 0: return _mix(PEARL, PEARL_D, 0.5)
        return r.choice((PEARL, PEARL_L, PEARL_L, PEARL))
    return _cells(c, seed, alpha=A_FEATHER)


def _covert(seed):
    """the coverts' band: small rounded feathers in rows - scale shapes, each lit at the top, shaded at the bottom"""
    def c(x, y, r):
        sx = (x + (y // 3 % 2) * 1) % 3
        if y % 3 == 2: return _mix(PEARL, PEARL_D, 0.55) if sx != 1 else PEARL
        if y % 3 == 0 and sx == 1: return _mix(PEARL_L, GOLD_L, 0.35)
        return r.choice((PEARL, PEARL_L))
    return _cells(c, seed, alpha=A_FEATHER)


def _tip(seed, blue=False):
    """a feather's gold tip (glowing); blue: the primaries' very ends, royal blue with a gold glint"""
    def c(x, y, r):
        if blue: return r.choice((ROYAL, ROYAL, ROYAL_L, GOLD_L))
        if x % 3 == 1: return GOLD_W
        return r.choice((GOLD, GOLD_L, GOLD_L))
    return _cells(c, seed)


def _light(seed):
    """the staff's core: white-gold light, brightest in the middle"""
    def c(x, y, r):
        k = max(abs(x % 8 - 3.5), abs(y % 8 - 3.5)) / 3.5
        return _mix(GOLD_W, GOLD_L, k) if r.random() > 0.1 else PEARL_L
    return _cells(c, seed)


def _gem(base, light, dark, seed):
    def c(x, y, r):
        if (x % 8, y % 8) in ((2, 2), (3, 2), (2, 3)): return light
        if (x + y) % 8 == 7: return dark
        return r.choice((base, base, light, dark)) if r.random() < 0.25 else base
    return _cells(c, seed)


def _put(im, x, y, c):
    if 0 <= x < 64 and 0 <= y < 64:
        im.putpixel((x, y), hexc(c) if isinstance(c, str) else c)


# ---- the face: 36 x 32 px on a 64 sheet (4 texels a unit - Emma's scale, as the royal family's), the head's front uv [0, 0, 9, 8]
EYES = ((9, 11), (26, 11))                          # (each eye's top-centre; the sheet's left eye is her right)
EYE_W, EYE_H = 12, 14
LASH = '#4a2814'                                    # (a deep warm brown, never black)
IRIS_RAMP = ['#a8620a', '#c87e12', '#e29e1e', '#f4be38', '#fcd862', '#fff0a2']   # deep amber at the top to pale gold
PUPIL, PUPIL_L = '#4a2404', '#7a4208'
WHITE = '#fffaf4'
FACE_SKIN = ('#ffe8da', '#fff0e6', '#fde0d0')       # (warm porcelain peach)


def _eye(im, glow, cx, y0, flip, kind):
    """one eye - big, gentle anime eyes: a soft curved upper lid drawn as a clean warm-brown lash line with a flick at the
    outer corner, a faint lower lash; a luminous gold iris graded from deep amber at the top to pale gold at the bottom, a
    thin lighter rim, a dark pupil, one clear white highlight and a small second one. glow: the same eye's iris alone (the
    light-15 overlay). flip: the eye on the sheet's right (her left), mirrored - its outer corner is to the right."""
    w, h = EYE_W, EYE_H + (1 if kind == 'surprised' else 0)
    o = 1 if flip else -1                                                     # (toward the outer corner)
    xs = range(cx - w // 2, cx + w // 2)
    dxn = lambda x: (x + 0.5 - cx) / (w / 2)                                 # (-1 .. 1 across the eye)
    inner = lambda x: max(0.0, min(1.0, 0.5 - 0.5 * dxn(x) * (-o)))           # (0 at the outer corner, 1 at the inner)
    if kind in ('happy', 'blink'):                                            # closed: a clean curved lash line
        for x in xs:
            d = dxn(x)
            y = y0 + 9 - round(3.4 * (1 - d * d)) if kind == 'happy' else y0 + 7 + round(2.6 * (1 - d * d))
            _put(im, x, y, LASH)
            if abs(d) < 0.7: _put(im, x, y + (1 if kind == 'happy' else -1) * 0 + 1, LASH)
        ox = cx + (w // 2 if flip else -w // 2 - 1)
        if kind == 'blink':
            _put(im, ox, y0 + 6, LASH); _put(im, ox + o, y0 + 5, LASH)          # (the lashes' flick)
        else:
            _put(im, ox, y0 + 10, LASH)
        return
    if kind == 'hurt':                                                        # squeezed shut: > <
        tip = cx + (3 if not flip else -4)
        far = cx + (-5 if not flip else 4)
        for i in range(9):
            t = i / 8
            x = round(far + (tip - far) * t)
            _put(im, x, round(y0 + 3 + 4 * t), LASH); _put(im, x, round(y0 + 11 - 4 * t), LASH)
            if 0.3 < t < 0.85: _put(im, x, round(y0 + 3 + 4 * t) + 1, LASH); _put(im, x, round(y0 + 11 - 4 * t) - 1, LASH)
        return
    # the open eye: the white inside an ellipse, under a lid line that arcs (higher in the middle)
    L, A, slant = {None: (3, 2.4, 0), 'fierce': (5, 1.4, 2), 'sad': (3, 2.2, -2), 'surprised': (0, 0, 0)}[kind]
    def lid(x):
        d = dxn(x)
        return y0 + L - round(A * (1 - d * d)) + round(slant * inner(x) if slant > 0 else -slant * (1 - inner(x)))
    vis = set()
    for y in range(y0, y0 + h):
        t = (y + 0.5 - y0) / h
        half = (w / 2) * math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2 * 0.86))
        for x in xs:
            if abs(x + 0.5 - cx) < half and y >= lid(x):
                vis.add((x, y))
    for x, y in vis:
        _put(im, x, y, WHITE)
    # the iris: an upright ellipse, sitting low in the eye; its colour graded down it; a lighter rim at its sides and foot
    ir = 3.3 if kind == 'surprised' else 4.3
    icy, ih = y0 + h * 0.55, h * 0.5 if kind != 'surprised' else h * 0.38
    iris = {(x, y) for (x, y) in vis if ((x + 0.5 - cx) / ir) ** 2 + ((y + 0.5 - icy) / ih) ** 2 <= 1 and y < y0 + h - 1}
    if iris:
        top, bot = min(y for _, y in iris), max(y for _, y in iris)
        for x, y in iris:
            t = (y - top) / max(1, bot - top)
            c = IRIS_RAMP[min(len(IRIS_RAMP) - 1, int(t * len(IRIS_RAMP)))]
            edge = any((x + dx, y + dy) not in iris for dx, dy in ((1, 0), (-1, 0), (0, 1)))
            if edge and y > top + 1: c = _mix(c, '#fff4c4', 0.4)
            _put(im, x, y, c)
        pr = 1.4 if kind == 'surprised' else 2.0                              # the pupil
        pcy = icy - 0.5
        for x, y in iris:
            if ((x + 0.5 - cx) / pr) ** 2 + ((y + 0.5 - pcy) / (pr * 1.35)) ** 2 <= 1:
                _put(im, x, y, PUPIL_L if y + 0.5 > pcy + pr else PUPIL)
        hx = cx - 3 if kind != 'surprised' else cx - 2                        # one clear highlight (up and to the viewer's left on both)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2)):
            if (hx + dx, top + 1 + dy) in iris: _put(im, hx + dx, top + 1 + dy, '#ffffff')
        if (cx + 2, bot - 2) in iris: _put(im, cx + 2, bot - 2, '#ffffff')    # and a small second one
        for x, y in iris:                                                     # (the glow overlay: the iris alone)
            glow.putpixel((x, y), im.getpixel((x, y)))
    # the upper lash line along the top of the open eye, the flick at the outer corner; a faint lower lash
    tops = {}
    for x, y in vis:
        tops[x] = min(y, tops.get(x, 99))
    for x, ty in tops.items():
        _put(im, x, ty - 1, LASH)
        if abs(dxn(x)) < 0.75: _put(im, x, ty, LASH)
    ox = max(tops) if flip else min(tops)
    _put(im, ox + o, tops[ox] - 1, LASH); _put(im, ox + o, tops[ox] - 2, LASH); _put(im, ox + 2 * o, tops[ox] - 3, LASH)
    for x in range(cx - 3, cx + 3):
        _put(im, x, y0 + h, '#dca896')
    _put(im, cx + o * 4, y0 + h - 1, '#dca896')
    if kind == 'sad':                                                         # a tear at the outer corner
        for dy, c in ((0, '#bfe6ff'), (1, '#e8f8ff'), (2, '#bfe6ff')):
            _put(im, cx + o * 5, y0 + h + dy, c)


def _brows(im, kind):
    """thin, soft, pale gold (her hair's own), set above the eyes under the fringe's points"""
    col = HAIR_D
    for (cx, _), flip in zip(EYES, (False, True)):
        for i, x in enumerate(range(cx - 3, cx + 4)):
            t = i if not flip else 6 - i                                     # (0 at the outer end, 6 at the inner)
            # (row 8 and above sits under the fringe's 3D edge: the brows live in rows 9-11)
            if kind == 'fierce': y = 9 + round(t / 3)                        # down toward the middle
            elif kind == 'sad': y = 11 - round(t / 3)                        # up toward the middle
            elif kind == 'surprised': y = 9                                  # (raised, high and level)
            elif kind == 'hurt': y = 10 + (1 if t > 4 else 0)
            else: y = 10 - (1 if 1 <= t <= 5 else 0)                        # (a soft arch)
            _put(im, x, y, col)


def _mouth(im, kind):
    ink, lip, inner = '#c06a5c', '#f0a49a', '#8a3a38'
    x, y = 15, 28
    rows = {'happy': ('.mmmmmm.', 'mwwwwwwm', '.mpppm..', '..mmm...'),
            'fierce': ('.mmmm.',),
            'sad': ('..mm..', '.m..m.', 'm....m'),
            'surprised': ('.mm.', 'mrrm', 'mrrm', '.mm.'),
            'hurt': ('m.m.m.m', '.m.m.m.'),
            'blink': ('m....m', '.mmmm.'),
            None: ('m....m', '.mmmm.')}[kind]
    if kind == 'surprised': x += 2
    if kind == 'happy': x -= 1
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch != '.': _put(im, x + dx, y + dy, {'m': ink, 'w': '#ffffff', 'p': lip, 'r': inner}[ch])


def _face(kind=None, glow=None):
    """her face (solid, so she reads clearly): warm porcelain, pale-gold bangs parted in the middle and falling to each
    temple, soft pale-gold brows, big luminous gold eyes, a soft blush, a small nose, a gentle mouth. glow: an image to
    take the irises alone (the eyes' light-15 overlay)."""
    im = _shade(FACE_SKIN[0], FACE_SKIN[1:], 4101, 0.08)
    for y in range(32):                                                      # (a touch of shade at its edges)
        for x in range(36):
            r, g, b, a = im.getpixel((x, y))
            if y > 29 or x < 1 or x > 34: im.putpixel((x, y), (int(r * 0.98), int(g * 0.95), int(b * 0.93), a))
    # the bangs: a centre part (a small V of brow at x 17-18), the fringe sweeping down to each side, longer at the temples
    hd, hm, hl = hexc(HAIR_D, 255), hexc(HAIR, 255), hexc(HAIR_L, 255)
    for x in range(36):
        dx = abs(x - 17.5)
        edge = int(3.5 + min(dx, 11) * 0.4 + (3 if dx > 14 else 0) + (6 if dx > 16 else 0))
        edge += (1, 0, -1)[(x // 2) % 3] if 2 < dx < 14 else 0                # (pointed locks)
        for y in range(edge):
            j = (x + y // 3) % 4
            c = (hm, hl, hm, hd)[j]
            if y == edge - 1: c = hd
            _put(im, x, y, c)
    _brows(im, kind)
    glow = glow if glow is not None else Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for (cx, y0), flip in zip(EYES, (False, True)):
        _eye(im, glow, cx, y0, flip, kind)
    if kind not in ('fierce', 'hurt'):                                       # the blush
        for cx in (5, 30):
            for x in range(cx - 3, cx + 4):
                for y in (26, 27):
                    if not (y == 27 and x in (cx - 3, cx + 3)): _put(im, x, y, '#f8bcb4')
    _put(im, 17, 24, '#ecb8a2'); _put(im, 18, 25, '#ecb8a2')                # the nose
    _mouth(im, kind)
    return im


def _eyes_glow(kind=None):
    g = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); _face(kind, g); return g


def textures():
    T = {'lb_robe': _robe(4001), 'lb_bodice': _bodice(4002), 'lb_gold': _gold(4003), 'lb_hem': _hem(4004),
         'lb_stole': _shade(PURPLE, (PURPLE_D, PURPLE_L), 4005, 0.25), 'lb_stole_v': _stole_v(4006),
         'lb_blue': _shade(ROYAL, (ROYAL_D, ROYAL_L), 4007, 0.25), 'lb_skin': _skin(4008), 'lb_hair': _hair(4009), 'lb_hairtip': _hairtip(4018),
         'lb_feather': _feather(4010), 'lb_covert': _covert(4011), 'lb_tip': _tip(4012), 'lb_tip_blue': _tip(4013, True),
         'lb_halo': _cells(lambda x, y, r: r.choice((GOLD_L, GOLD_W, GOLD_W, GOLD)), 4014), 'lb_light': _light(4015),
         'lb_sapph': _gem(ROYAL, '#b0c8ff', ROYAL_D, 4016), 'lb_ameth': _gem(PURPLE_L, '#e6d4ff', PURPLE_D, 4017),
         'lb_face': _face(), 'lb_eyes': _eyes_glow()}
    for k in FACES:
        T[f'lb_face_{k}'] = _face(k)
        if k in OPEN_EYES: T[f'lb_eyes_{k}'] = _eyes_glow(k)
    T.update(textures_m())                                                   # (3.0: his face and eyes - the male form)
    return T


def _faces_but(*drop):
    return tuple(f for f in ('north', 'south', 'east', 'west', 'up', 'down') if f not in drop)


ROBE_Y = [13.4, 11.8, 10.2, 8.6, 7.1, 5.6, 4.1, 2.6, 1.0]          # the robe's tiers, the sash down to the hem (5.6: the skirt's cut)


def _robe_w(i):
    """tier i's half width, half depth (a slim A-line: 3.5 x 2.6 under the sash, 5.4 x 3.9 at the hem)"""
    t = (i + 1) / (len(ROBE_Y) - 1)
    return 3.5 + 1.9 * t ** 0.9, 2.6 + 1.3 * t


def _tier(i, pv):
    """one tier of the robe: no top (the tier above sits on it, and through the silk it would show as a floor) - a ring of
    pearl round the step instead; the purple stole down the front with gold edges; the hem in gold"""
    y1, y0 = ROBE_Y[i], ROBE_Y[i + 1]
    hw, hd = _robe_w(i)
    last = i == len(ROBE_Y) - 2
    out = [el((-hw, y0, -hd), (hw, y1, hd), 'lb_robe', pv, faces=_faces_but('up') if not last else _faces_but('up'), shift=(0.17 * i, 0.31 * i))]
    if i > 0:                                                                     # the step's ring (the tier above is narrower)
        pw, pd = _robe_w(i - 1)
        for (a, b) in (((-hw, y1 - 0.01, -hd), (hw, y1, -pd)), ((-hw, y1 - 0.01, pd), (hw, y1, hd)),
                       ((-hw, y1 - 0.01, -pd), (-pw, y1, pd)), ((pw, y1 - 0.01, -pd), (hw, y1, pd))):
            out.append(el(a, b, 'lb_robe', pv, faces=('up',), shift=(0.3, 0.6)))
    sw = 0.5 + 0.06 * i                                                           # the stole: a narrow purple band, edged in gold
    out += [el((-sw, y0, -hd - 0.04), (sw, y1, -hd - 0.02), 'lb_stole', pv, faces=('north',), shift=(0.2 * i, 0.4)),
            el((-sw - 0.4, y0, -hd - 0.06), (-sw, y1, -hd - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), shift=(0.1 * i, 0.2), light=4),
            el((sw, y0, -hd - 0.06), (sw + 0.4, y1, -hd - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), shift=(0.3 * i, 0.5), light=4)]
    if last:                                                                      # the hem: a gold band (a blue line along its top)
        out.append(el((-hw - 0.08, y0, -hd - 0.08), (hw + 0.08, y0 + 0.8, hd + 0.08), 'lb_hem', pv, faces=_faces_but('up'),
                      uv={f: [0, 0, 16, 0.8] for f in ('north', 'south', 'east', 'west')}))
        out.append(el((-hw - 0.08, y0 + 0.79, -hd - 0.08), (hw + 0.08, y0 + 0.8, hd + 0.08), 'lb_gold', pv, faces=('up',)))
    return out


def _ring(c, r, n, w, h, tex, pv, plane='xz', tilt=0.0, light=0):
    """a ring of n boxes (a halo, a staff's head): radius r round centre c, in the xz plane (flat) or the xy plane (upright)"""
    pts = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        if plane == 'xz':
            x, y, z = r * math.cos(a), 0.0, r * math.sin(a)
            y, z = y * math.cos(math.radians(tilt)) - z * math.sin(math.radians(tilt)), y * math.sin(math.radians(tilt)) + z * math.cos(math.radians(tilt))
        else:
            x, y, z = r * math.cos(a), r * math.sin(a), 0.0
        pts.append((c[0] + x, c[1] + y, c[2] + z))
    up = (0.0, math.cos(math.radians(tilt)), math.sin(math.radians(tilt))) if plane == 'xz' else FRONT
    return [seg(pts[k], pts[k + 1], w, h, tex, pv, up, ext=0.18, light=light, shift=(0.3 * k, 0.17 * k)) for k in range(n)]


# ---- the wings: drawn flat (u outward from the root, v up) and set into the back, swept back by SWEEP
SWEEP = 34.0
LEAD = [(0.7, 0.6), (3.0, 2.6), (5.0, 5.6), (6.8, 9.2), (8.8, 11.4), (10.6, 11.2)]    # the leading edge (the wing's 'arm')
SECONDARIES = [(1.3, 9.0, 0.03), (2.6, 10.6, 0.05), (3.9, 13.0, 0.07), (5.2, 15.4, 0.09)]      # (u at the root, length, outward lean)
PRIMARIES = [(6.4, 17.6, 0.11), (7.6, 18.8, 0.15), (8.8, 18.8, 0.20), (9.9, 17.6, 0.27), (10.9, 15.6, 0.36)]


def _lead_v(u):
    for (u0, v0), (u1, v1) in zip(LEAD, LEAD[1:]):
        if u <= u1: return v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return LEAD[-1][1]


def _wing(sx):
    pv = PIVOT['wingr' if sx > 0 else 'wingl']
    a = math.radians(SWEEP)
    du, n = (sx * math.cos(a), 0.0, math.sin(a)), (-sx * math.sin(a), 0.0, math.cos(a))     # (n: the wing's back, away from her)
    P = lambda u, v, w=0.0: (pv[0] + u * du[0] + w * n[0], pv[1] + v, pv[2] + u * du[2] + w * n[2])
    els = []
    # the root: a short thick stub of down from her back to the wing
    els.append(seg(P(-0.2, 0.0, 0.1), P(1.2, 1.6, 0.1), 1.6, 1.0, 'lb_covert', pv, n, ext=0.1))
    # the coverts: a band along the leading edge, its lower edge where the flight feathers start
    band = [P(u, v - 1.25, 0.5) for u, v in LEAD]
    els += [seg(band[i], band[i + 1], 2.6, 0.7, 'lb_covert', pv, n, ext=0.2, shift=(0.29 * i, 0.43 * i)) for i in range(len(band) - 1)]
    els.append(seg(P(LEAD[-1][0] - 0.2, LEAD[-1][1] - 0.6, 0.15), P(LEAD[-1][0] + 0.9, LEAD[-1][1] - 2.0, 0.15), 1.4, 0.7, 'lb_covert', pv, n))
    # the flight feathers, one layer: each from the band's lower edge, down and a little out; pearl to a gold tip (lit)
    for k, (u, L, lean) in enumerate(SECONDARIES + PRIMARIES):
        prim = k >= len(SECONDARIES)
        v0 = _lead_v(u) - 2.4
        dx, dy = lean, -1.0
        m = math.hypot(dx, dy); dx, dy = dx / m, dy / m
        A = P(u, v0); B = P(u + dx * L, v0 + dy * L); C = P(u + dx * L * 0.74, v0 + dy * L * 0.74)
        w = 1.95 if prim else 1.85                                       # (a little wider than their spacing: a closed wing,
        lay = 0.22 * (k % 2)                                               #  the neighbours a hair apart in depth where they overlap)
        A, B, C = P(u, v0, lay), P(u + dx * L, v0 + dy * L, lay), P(u + dx * L * 0.74, v0 + dy * L * 0.74, lay)
        els.append(seg(A, C, w, 0.42, 'lb_feather', pv, n, ext=0.0, light=7, shift=(0.21 * k, 0.37 * k)))
        els.append(seg(C, B, w, 0.42, 'lb_tip', pv, n, ext=0.0, light=15, shift=(0.13 * k, 0.29 * k)))
        els.append(seg(B, P(u + dx * (L + 0.8), v0 + dy * (L + 0.8), lay), w * 0.55, 0.36, 'lb_tip_blue' if prim else 'lb_tip', pv, n, ext=0.0, light=15))
    return els


def _uncovered(A, B, axis, sign, tex, pv):
    """the face of box A (on axis 0/1/2, the +1 or -1 side) that box B, stacked against it there, leaves showing - strips
    round B's footprint, so A has no face inside B (it would show through her translucent hair)"""
    u, v = [i for i in range(3) if i != axis]
    at = A[1][axis] if sign > 0 else A[0][axis]
    a0, a1, b0, b1 = A[0], A[1], B[0], B[1]
    rects = [((a0[u], a0[v]), (a1[u], b0[v])), ((a0[u], b1[v]), (a1[u], a1[v])), ((a0[u], b0[v]), (b0[u], b1[v])), ((b1[u], b0[v]), (a1[u], b1[v]))]
    face = {(0, 1): 'east', (0, -1): 'west', (1, 1): 'up', (1, -1): 'down', (2, 1): 'south', (2, -1): 'north'}[(axis, sign)]
    out = []
    for (p0, q0), (p1, q1) in rects:
        if p1 - p0 < 1e-3 or q1 - q0 < 1e-3: continue
        lo, hi = [0.0] * 3, [0.0] * 3
        lo[u], hi[u], lo[v], hi[v] = p0, p1, q0, q1
        lo[axis], hi[axis] = (at - 0.01, at) if sign > 0 else (at, at + 0.01)
        out.append(el(tuple(lo), tuple(hi), tex, pv, faces=(face,)))
    return out


def _ring_up(A, B, tex, pv):
    """the top face of box A that box B (stacked on it) leaves showing - four strips, so A has no top inside B"""
    (ax0, _, az0), (ax1, ay, az1) = A; (bx0, _, bz0), (bx1, _, bz1) = B
    q = [((ax0, az0), (ax1, bz0)), ((ax0, bz1), (ax1, az1)), ((ax0, bz0), (bx0, bz1)), ((bx1, bz0), (ax1, bz1))]
    return [el((x0, ay - 0.01, z0), (x1, ay, z1), tex, pv, faces=('up',)) for (x0, z0), (x1, z1) in q if x1 - x0 > 1e-3 and z1 - z0 > 1e-3]


def _ring_back(A, B, tex, pv):
    """the back face of box A that box B (stepped out behind it) leaves showing"""
    (ax0, ay0, _), (ax1, ay1, az) = A; (bx0, by0, _), (bx1, by1, _) = B
    q = [((ax0, ay0), (ax1, by0)), ((ax0, by1), (ax1, ay1)), ((ax0, by0), (bx0, by1)), ((bx1, by0), (ax1, by1))]
    return [el((x0, y0, az - 0.01), (x1, y1, az), tex, pv, faces=('south',)) for (x0, y0), (x1, y1) in q if x1 - x0 > 1e-3 and y1 - y0 > 1e-3]


def _lock(pts, ws, tex_tip_from, pv, h=1.0):
    """a lock of hair down a polyline: pale gold, its last spans lit gold (from span tex_tip_from on)"""
    out = []
    for i in range(len(pts) - 1):
        tip = i >= tex_tip_from
        out.append(seg(pts[i], pts[i + 1], ws[i], h * (0.75 if tip else 1.0), 'lb_hairtip' if tip else 'lb_hair', pv, FRONT,
                       ext=0.02, light=12 if tip else 0, shift=(0.31 * i, 0.47 * i)))
    return out


def _upright(pose, part, want):
    """pose[part] such that the part's world rotation is `want` (a staff kept upright however the arm bends)"""
    xf = solve(PIVOT, PARENT, dict(pose, **{part: (0.0, 0.0, 0.0, 1.0)}))
    q = xf[PARENT[part]][0]
    return qmul((-q[0], -q[1], -q[2], q[3]), want)


def models():
    M = {}

    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({t: f'bm:block/{t}' for t in used}, els)

    # ---- the body: the robe's upper tiers, the blue sash and gold clasp, the bodice (gold neckline, the sun), the purple
    #      stole's two strips up over her breast, the shoulders, a gold collar, the neck
    pv = PIVOT['body']
    body = []
    for i in range(5):
        body += _tier(i, pv)
    body += [el((-3.55, 13.2, -2.65), (3.55, 14.4, 2.65), 'lb_blue', pv, faces=_faces_but('down'), shift=(0.2, 0.2)),    # the sash
             el((-0.8, 13.0, -2.85), (0.8, 14.6, -2.65), 'lb_gold', pv, light=6),                                          # its clasp
             el((-0.35, 13.45, -2.95), (0.35, 14.15, -2.85), 'lb_sapph', pv, faces=('north',)),
             el((-3.3, 14.4, -2.3), (3.3, 21.4, 2.3), 'lb_robe', pv, faces=('south', 'east', 'west'), shift=(0.3, 0.2)),   # the bodice
             el((-3.3, 14.4, -2.3), (3.3, 21.4, -2.3), 'lb_bodice', pv, faces=('north',), uv={'north': [0, 0, 6.6, 7.0]}),
             el((-3.5, 21.4, -2.45), (3.5, 22.6, 2.45), 'lb_robe', pv, faces=_faces_but('down'), shift=(0.6, 0.1)),       # the shoulders
             el((-1.8, 22.6, -1.8), (1.8, 23.2, 1.8), 'lb_gold', pv, faces=_faces_but('down')),                           # the collar
             el((-1.2, 23.2, -1.2), (1.2, 24.6, 1.2), 'lb_skin', pv, faces=('north', 'south', 'east', 'west'))]            # the neck
    # the stole: one straight band, purple edged in gold, hanging from under the collar down the middle to the sash (the
    # robe's panel below carries it on to the hem); the gold sun on it, at her breast
    body += [el((-0.75, 14.4, -2.36), (0.75, 22.62, -2.31), 'lb_stole_v', pv, faces=('north',), uv={'north': [0, 0, 1.5, 8.2]}),
             el((-0.75, 22.6, -2.47), (0.75, 22.64, -1.8), 'lb_stole_v', pv, faces=('up',), uv={'up': [0, 0, 1.5, 0.7]}),
             el((-0.85, 18.65, -2.46), (0.85, 20.35, -2.36), 'lb_gold', pv, rot=('z', 45, (0, 19.5, -2.41)), light=10),
             el((-0.36, 19.14, -2.54), (0.36, 19.86, -2.46), 'lb_light', pv, faces=('north',), light=15)]
    # the long locks that frame her face, falling on down in front of her shoulders to the breast (on the body: the head's
    # nod doesn't swing them into her chest); their tips lit
    for sx in (-1, 1):
        JOINTS.setdefault('lb_body', {})[len(body)] = ('head',)                     # (where the lock leaves her cheek)
        pts = [(sx * 4.15, 24.1, -3.35), (sx * 3.15, 22.4, -2.95), (sx * 2.75, 20.0, -2.8), (sx * 2.6, 18.7, -2.75)]
        body += chain(pts[:3], [1.2, 1.05], 0.7, 'lb_hair', pv, FRONT, ext=0.05)
        body.append(seg(pts[2], pts[3], 0.75, 0.6, 'lb_hairtip', pv, FRONT, ext=0.0, light=12))
    part('lb_body', body)
    skirt = []
    for i in range(5, len(ROBE_Y) - 1):
        skirt += _tier(i, PIVOT['skirt'])
    part('lb_skirt', skirt)
    # the robe pooled round her when she kneels: low tiers on the floor, reaching forward over her knees; gold at the edge
    pv = PIVOT['pool']
    part('lb_pool', [el((-7.2, 0.0, -7.4), (7.2, 0.8, 5.6), 'lb_robe', pv, faces=_faces_but('up', 'down')),
                     el((-6.4, 0.8, -6.6), (6.4, 1.6, 4.8), 'lb_robe', pv, faces=_faces_but('up', 'down'), shift=(0.4, 0.3)),
                     el((-5.5, 1.6, -5.6), (5.5, 2.4, 4.3), 'lb_robe', pv, faces=_faces_but('down'), shift=(0.7, 0.6)),
                     el((-7.2, 0.79, -7.4), (7.2, 0.8, 5.6), 'lb_robe', pv, faces=('up',)),
                     el((-6.4, 1.59, -6.6), (6.4, 1.6, 4.8), 'lb_robe', pv, faces=('up',), shift=(0.4, 0.3)),
                     el((-7.28, 0.0, -7.48), (7.28, 0.35, 5.68), 'lb_gold', pv, faces=_faces_but('up', 'down')),
                     el((-1.8, 0.0, -7.46), (1.8, 0.8, -7.42), 'lb_stole', pv, faces=('north',)),
                     el((-1.6, 0.8, -6.66), (1.6, 1.6, -6.62), 'lb_stole', pv, faces=('north',)),
                     el((-1.4, 1.6, -5.66), (1.4, 2.4, -5.62), 'lb_stole', pv, faces=('north',))])

    # ---- the head: Emma's head (9 x 8 x 8); hair parted in the middle - a cap, the back to the nape, sides, a lock
    #      framing each cheek, the fringe's edge over her brow. Hair faces turned in to the head are left off (they'd show
    #      through her skin); the head has no back or top of its own (the hair is its back and top).
    pv = PIVOT['head']

    def head(face=None):
        tex = 'lb_face' if face is None else f'lb_face_{face}'
        hr = lambda fr, to, faces=None, sh=None, rot=None: el(fr, to, 'lb_hair', pv, faces=faces, shift=sh, rot=rot)
        C1, C2, C3 = ((-4.9, HT - 1.4, -4.4), (4.9, HT + 0.4, 4.6)), ((-4.4, HT + 0.4, -3.9), (4.4, HT + 1.3, 4.2)), \
            ((-3.3, HT + 1.3, -2.7), (3.3, HT + 2.0, 3.3))                                     # the crown, in three soft steps
        B1, B2, B3 = ((-4.6, HB - 0.6, 3.4), (4.6, HT - 1.4, 4.6)), ((-4.0, HB + 0.8, 4.6), (4.0, HT - 1.4, 5.4)), \
            ((-2.9, HB + 2.2, 5.4), (2.9, HT - 2.6, 5.9))                                       # the back, stepped out round
        S = [((sx * 5.1 if sx > 0 else -5.75, HB + 1.8, -1.6), (5.75 if sx > 0 else -5.1, HT - 1.6, 2.8)) for sx in (1, -1)]   # (fullness over the ears)
        h = [el((-4.5, HB, -4.0), (4.5, HT - 1.4, 3.4), 'lb_skin', pv, faces=('east', 'west', 'down')),
             dict(el((-4.5, HB, -4.0), (4.5, HT, -4.0), tex, pv, faces=('north',), uv={'north': [0, 0, 9, 8]}), shade=False),   # (unshaded: warm and clear)
             hr(*C1, faces=('north', 'south', 'east', 'west', 'down'), sh=(0.2, 0.1)),
             hr(*C2, faces=('north', 'south', 'east', 'west'), sh=(0.6, 0.4)),
             hr(*C3, faces=('north', 'south', 'east', 'west', 'up'), sh=(0.4, 0.7)),
             hr(*B1, faces=('east', 'west', 'down'), sh=(0.5, 0.3)),
             hr(*B2, faces=('east', 'west', 'up', 'down'), sh=(0.3, 0.5)),
             hr(*B3, faces=('south', 'east', 'west', 'up', 'down'), sh=(0.7, 0.2)),
             hr(*S[0], faces=('north', 'south', 'east', 'up', 'down'), sh=(0.4, 0.4)),
             hr(*S[1], faces=('north', 'south', 'west', 'up', 'down'), sh=(0.6, 0.6)),
             hr((4.5, HB + 1.0, -2.6), (5.1, HT - 1.4, 3.4), faces=('north', 'down'), sh=(0.1, 0.4)),                     # the sides
             hr((-5.1, HB + 1.0, -2.6), (-4.5, HT - 1.4, 3.4), faces=('north', 'down'), sh=(0.6, 0.2)),
             hr((0.35, HT - 2.0, -4.6), (4.9, HT - 1.4, -4.0), faces=('north', 'east', 'west', 'down'), sh=(0.3, 0.6)),   # the fringe, parted
             hr((-4.9, HT - 2.0, -4.6), (-0.35, HT - 1.4, -4.0), faces=('north', 'east', 'west', 'down'), sh=(0.7, 0.2)),
             hr((4.0, HB - 0.3, -4.5), (5.15, HT - 1.4, -2.6), faces=('north', 'east', 'south', 'down', 'west'), sh=(0.2, 0.7)),   # the locks at her cheeks
             hr((-5.15, HB - 0.3, -4.5), (-4.0, HT - 1.4, -2.6), faces=('north', 'west', 'south', 'down', 'east'), sh=(0.8, 0.5))]
        h += _ring_up(C1, C2, 'lb_hair', pv) + _ring_up(C2, C3, 'lb_hair', pv) + _ring_back(B1, B2, 'lb_hair', pv) + _ring_back(B2, B3, 'lb_hair', pv)
        for sx, Sd in zip((1, -1), S):                                                             # (the sides' outer faces round the fullness)
            side = ((4.5, HB + 1.0, -2.6), (5.1, HT - 1.4, 3.4)) if sx > 0 else ((-5.1, HB + 1.0, -2.6), (-4.5, HT - 1.4, 3.4))
            h += _uncovered(side, Sd, 0, sx, 'lb_hair', pv)
        for x in (-3.6, -0.85, 0.85, 3.6):                                                     # pointed locks over her brow (between and
            dy = 0.25 if abs(x) < 2 else 0.0                                                   #  outside the brows, so they show)
            h.append(el((x - 0.4, HT - 2.4 + dy, -4.62), (x + 0.4, HT - 1.6 + dy, -4.04), 'lb_hair', pv, faces=('north', 'east', 'west', 'down'),
                        rot=('z', 45, (x, HT - 2.0 + dy, -4.33)), shift=(0.1 * x, 0.3)))
        if face in OPEN_EYES:                                     # her eyes, lit: each iris again (alone - its own texture), just in front, glowing
            gt = 'lb_eyes' if face is None else f'lb_eyes_{face}'
            for (cx, y0), flip in zip(EYES, (False, True)):
                u0, u1, v0, v1 = (cx - 6) / 4, (cx + 6) / 4, (y0 - 1) / 4, (y0 + EYE_H + 2) / 4
                h.append(dict(el((4.5 - u1, HT - v1, -4.03), (4.5 - u0, HT - v0, -4.02), gt, pv, faces=('north',),
                                 uv={'north': [u0, v0, u1, v1]}, light=15), shade=False))
        return h
    part('lb_head', head())
    for fc in FACES:
        part(f'lb_head_x{fc}', head(fc))

    # ---- the halo: a ring of light above her head, tipped back a little
    pv = PIVOT['halo']
    part('lb_halo', _ring(pv, 3.6, 14, 0.75, 0.45, 'lb_halo', pv, 'xz', tilt=-12, light=15))

    # ---- the long hair down her back, between the wings' roots and behind the robe (on the body, two joints so it can stream
    #      and drape): from the nape a full fall, gathered at the shoulder blades in a gold clasp with a sapphire, then
    #      parting into three layered locks - the middle one to a point at the backs of her knees, the two beside it swaying
    #      out and flipping up at the ends; every tip lit
    pv = PIVOT['hair']
    up = chain([(0, 23.9, 3.55), (0, 22.0, 3.3), (0, 19.0, 3.2)], [5.6, 3.9], 1.1, 'lb_hair', pv, FRONT, ext=0.02)
    up += [seg((0, 20.2, 3.2), (0, 19.3, 3.2), 4.0, 1.34, 'lb_gold', pv, FRONT, ext=0.0, light=6),              # the clasp
           el((-0.45, 19.3, 3.87), (0.45, 20.2, 4.02), 'lb_sapph', pv, faces=('south', 'east', 'west', 'up', 'down'), light=6)]
    up += chain([(0, 19.0, 3.3), (0, 14.6, 3.5)], [2.2], 1.0, 'lb_hair', pv, FRONT, ext=0.02)
    for sx in (-1, 1):
        up += chain([(sx * 1.7, 19.0, 3.15), (sx * 1.95, 14.6, 3.35)], [1.25], 0.9, 'lb_hair', pv, FRONT, ext=0.02)
    JOINTS['lb_hair'] = {0: ('head',)}                                                 # (where the fall leaves her nape)
    part('lb_hair', up)
    pv = PIVOT['hairlo']
    lo = _lock([(0, 14.6, 3.5), (0, 11.0, 3.85), (0, 8.0, 4.2), (0, 6.2, 4.35), (0, 4.9, 4.45)], [2.2, 1.9, 1.4, 0.75], 2, pv)
    for sx in (-1, 1):
        lo += _lock([(sx * 1.95, 14.6, 3.35), (sx * 2.2, 11.5, 3.65), (sx * 2.6, 9.3, 3.95), (sx * 2.95, 8.0, 4.1), (sx * 3.45, 8.4, 4.15)],
                    [1.25, 1.15, 0.95, 0.65], 2, pv, h=0.9)
    part('lb_hairlo', lo)

    # ---- the arms: pearl sleeves (a gold band at the shoulder), bell sleeves to the wrist with a blue cuff edged in gold
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        e = (sx * 4.9, 18.6, 0)
        return [seg((x0, y0 + 0.15, 0), e, 2.1, 2.1, 'lb_robe', pv, FRONT, ext=0.0, shift=(0.3, 0.1)),
                seg((x0 + sx * 0.03, y0 - 0.9, 0), (x0 + sx * 0.06, y0 - 1.5, 0), 2.22, 2.22, 'lb_gold', pv, FRONT, light=6)]

    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 5.1, 14.6
        return [seg((ex, ey, 0), (wx, wy + 0.8, 0), 2.0, 2.0, 'lb_robe', pv, FRONT, ext=0.0, shift=(0.6, 0.4)),
                seg((ex + sx * 0.16, wy + 0.8, 0), (wx, wy + 0.1, 0), 2.45, 2.45, 'lb_blue', pv, FRONT, ext=0.0),     # the bell, blue inside
                seg((wx, wy + 0.1, 0), (wx, wy - 0.25, 0), 2.55, 2.55, 'lb_gold', pv, FRONT, ext=0.0, light=6),      # its gold edge
                el((wx - 0.8, wy - 2.3, -0.85), (wx + 0.8, wy - 0.25, 0.8), 'lb_skin', pv, faces=_faces_but('up')),  # the hand
                el((wx - 0.65, wy - 2.75, -0.8), (wx + 0.65, wy - 2.3, -0.2), 'lb_skin', pv, faces=_faces_but('up'))]
    part('lb_armr', upper(1)); part('lb_arml', upper(-1)); part('lb_forer', lower(1)); part('lb_forel', lower(-1))

    # ---- the feet: small and bare, gold sandal straps; from the ankle, so her toes can point down as she floats
    def foot(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 0.8, 0.2, -2.4), (cx + 0.8, 1.0, 0.9), 'lb_skin', pv, faces=_faces_but('up')),
                el((cx - 0.7, 0.2, -2.9), (cx + 0.7, 0.75, -2.4), 'lb_skin', pv, faces=_faces_but('south')),
                el((cx - 0.85, 0.0, -2.95), (cx + 0.85, 0.2, 0.95), 'lb_gold', pv),                                 # the sole
                el((cx - 0.86, 0.4, -1.6), (cx + 0.86, 0.75, -1.2), 'lb_gold', pv, faces=_faces_but('down')),       # a strap
                el((cx - 0.86, 0.75, -0.2), (cx + 0.86, 1.0, 0.96), 'lb_gold', pv, faces=_faces_but('down'))]
    part('lb_legr', foot(1)); part('lb_legl', foot(-1))

    # ---- the staff of light, upright in her right fist (the grip at the joint): a gold staff, a sapphire band, a gold ring
    #      round a glowing core, rays, an amethyst finial; a gold foot
    pv = PIVOT['staff']; X, Y, Z = pv
    st = [el((X - 0.35, Y - 11.0, Z - 0.35), (X + 0.35, Y + 13.4, Z + 0.35), 'lb_gold', pv, light=4),
          el((X - 0.5, Y - 11.6, Z - 0.5), (X + 0.5, Y - 10.6, Z + 0.5), 'lb_gold', pv, light=4),
          el((X - 0.55, Y + 11.6, Z - 0.55), (X + 0.55, Y + 12.6, Z + 0.55), 'lb_sapph', pv, light=6),
          el((X - 0.7, Y + 12.6, Z - 0.7), (X + 0.7, Y + 13.4, Z + 0.7), 'lb_gold', pv, light=6),
          el((X - 0.9, Y + 15.2, Z - 0.9), (X + 0.9, Y + 17.0, Z + 0.9), 'lb_light', pv, light=15)]                     # the core
    st += _ring((X, Y + 16.1, Z), 2.3, 10, 0.55, 0.6, 'lb_gold', pv, 'xy', light=10)
    for a in (30, 150, 60, 120):                                                                                   # rays off the ring
        r0, r1 = 2.6, 3.6 if a in (60, 120) else 3.2
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        st.append(seg((X + r0 * ca, Y + 16.1 + r0 * sa, Z), (X + r1 * ca, Y + 16.1 + r1 * sa, Z), 0.35, 0.35, 'lb_halo', pv, FRONT, light=15))
    st += [el((X - 0.45, Y + 18.4, Z - 0.45), (X + 0.45, Y + 19.3, Z + 0.45), 'lb_gold', pv, light=8),
           el((X - 0.55, Y + 19.3, Z - 0.55), (X + 0.55, Y + 20.4, Z + 0.55), 'lb_ameth', pv, rot=('y', 45, (X, Y + 19.8, Z)), light=8),
           el((X - 0.3, Y + 20.4, Z - 0.3), (X + 0.3, Y + 21.1, Z + 0.3), 'lb_ameth', pv, rot=('y', 45, (X, Y + 20.7, Z)), light=8)]
    part('lb_staff', st)

    part('lb_wingr', _wing(1)); part('lb_wingl', _wing(-1))
    for w in ('lb_wingr', 'lb_wingl'): JOINTS[w] = {0: ('body', 'hair'), 1: ('body', 'hair')}                 # (the root on her back)
    _male(M, part)
    return M


# ---------------------------------------------------------------------------------------------------- the male form (3.0)
# (the owner: "a toggleable male variant") - HE: the same herald, the same rig, joints, poses and faces, so every animation,
# ability and the Ophanim work unchanged; his twin of each part is the same name with MALE ('_m': rigpet's FORM suffix, which
# the dress function puts on every part). The same holy design language - translucent pearl, gold, royal blue and purple, the
# halo, the wings, the staff - but clearly a man: broad shoulders and chest under a gold-collared surcoat, gold pauldrons and
# vambraces, a purple tabard (gold-edged, the sun on its breast) hanging front and back over a straight long tunic - no
# dress's flare - a gold sword-belt, armoured feet; short cropped hair swept to the side, ears, a strong brow and jaw. His
# cloth is the robe's and the bodice's own textures, so every wardrobe look (and the shiny) recolours him too.
MALE = '_m'
EYES_M = ((9, 14), (26, 14))                       # (each eye's top-centre: narrower, lower, under a heavier brow)
EYE_W_M, EYE_H_M = 10, 8
FACE_SKIN_M = ('#f6dcc8', '#fae6d6', '#ecccb6')   # (a touch warmer than hers)
BROW_M = '#8a6424'                                 # (dark gold-brown, heavy)
JAW_M = '#e2b89e'
JAW_EDGE = '#d4a088'


def _eye_m(im, glow, cx, y0, flip, kind):
    """one eye of his: almond, narrower than hers, a single clean lid line (no lashes' flick), the same luminous gold iris"""
    w, h = EYE_W_M, EYE_H_M + (2 if kind == 'surprised' else 0)
    y0 = y0 - (1 if kind == 'surprised' else 0)
    xs = range(cx - w // 2, cx + w // 2)
    dxn = lambda x: (x + 0.5 - cx) / (w / 2)
    o = 1 if flip else -1
    if kind in ('happy', 'blink'):
        for x in xs:
            d = dxn(x)
            y = y0 + 5 - round(2.0 * (1 - d * d)) if kind == 'happy' else y0 + 5
            _put(im, x, y, LASH)
            if kind == 'blink' and abs(d) < 0.8: _put(im, x, y + 1, '#c89a84')
        return
    if kind == 'hurt':                                                        # squeezed shut: > <
        tip, far = (cx + 3, cx - 4) if not flip else (cx - 4, cx + 3)
        for i in range(8):
            t = i / 7
            x = round(far + (tip - far) * t)
            _put(im, x, round(y0 + 1 + 3 * t), LASH); _put(im, x, round(y0 + 7 - 3 * t), LASH)
        return
    L, A, slant = {None: (2, 1.4, 0), 'fierce': (3, 0.6, 2), 'sad': (2, 1.2, -2), 'surprised': (0, 0.4, 0)}[kind]
    inner = lambda x: max(0.0, min(1.0, 0.5 - 0.5 * dxn(x) * (-o)))
    lid = lambda x: y0 + L - round(A * (1 - dxn(x) ** 2)) + round(slant * inner(x) if slant > 0 else -slant * (1 - inner(x)))
    vis = set()
    for y in range(y0, y0 + h):
        t = (y + 0.5 - y0) / h
        half = (w / 2) * math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2 * 0.9))
        for x in xs:
            if abs(x + 0.5 - cx) < half and y >= lid(x):
                vis.add((x, y))
    for x, y in vis:
        _put(im, x, y, WHITE)
    ir = 2.6 if kind == 'surprised' else 3.1
    icy, ih = y0 + h * 0.55, h * 0.42
    iris = {(x, y) for (x, y) in vis if ((x + 0.5 - cx) / ir) ** 2 + ((y + 0.5 - icy) / ih) ** 2 <= 1}
    if iris:
        top, bot = min(y for _, y in iris), max(y for _, y in iris)
        for x, y in iris:
            t = (y - top) / max(1, bot - top)
            _put(im, x, y, IRIS_RAMP[min(len(IRIS_RAMP) - 1, int(t * len(IRIS_RAMP)))])
        pr = 1.0 if kind == 'surprised' else 1.4
        for x, y in iris:
            if ((x + 0.5 - cx) / pr) ** 2 + ((y + 0.5 - icy) / (pr * 1.3)) ** 2 <= 1:
                _put(im, x, y, PUPIL)
        if (cx - 2, top) in iris: _put(im, cx - 2, top, '#ffffff')
        if (cx - 2, top + 1) in iris: _put(im, cx - 2, top + 1, '#ffffff')
        for x, y in iris:
            glow.putpixel((x, y), im.getpixel((x, y)))
    tops = {}
    for x, y in vis:
        tops[x] = min(y, tops.get(x, 99))
    for x, ty in tops.items():
        _put(im, x, ty - 1, LASH)
    for x in range(cx - 3, cx + 3):                                           # a faint crease under it
        _put(im, x, y0 + h, '#dcae98')


def _brows_m(im, kind):
    """heavy, straight, low brows: two pixels thick, a shade under them (the brow ridge)"""
    for (cx, _), flip in zip(EYES_M, (False, True)):
        for i, x in enumerate(range(cx - 5, cx + 5)):
            t = i if not flip else 9 - i                                     # (0 at the outer end, 9 at the inner)
            if kind == 'fierce': y = 10 + round(t / 3.2)                     # hard down toward the middle
            elif kind == 'sad': y = 12 - round(t / 4)
            elif kind == 'surprised': y = 9
            elif kind == 'hurt': y = 11 + (1 if t > 6 else 0)
            else: y = 11 - (1 if 2 <= t <= 7 else 0)                         # (a low, flat arch)
            _put(im, x, y, BROW_M); _put(im, x, y + 1, BROW_M)
            if t > 1: _put(im, x, y + 2, _mix(FACE_SKIN_M[0], JAW_M, 0.7))


def _mouth_m(im, kind):
    ink, lip, inner = '#a85a4c', '#d89484', '#6a2a28'
    x, y = 13, 27
    rows = {'happy': ('m........m', '.mmmmmmmm.'),
            'fierce': ('.mmmmmmmm.', 'm........m'),
            'sad': ('...mmmm...', '.mm....mm.'),
            'surprised': ('...mmmm...', '..mrrrrm..', '...mmmm...'),
            'hurt': ('.mmmmmmmm.', '.mwmwmwmm.', '.mmmmmmmm.'),
            'blink': ('.mmmmmmmm.',),
            None: ('.mmmmmmmm.', '...pppp...')}[kind]
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch != '.': _put(im, x + dx, y + dy, {'m': ink, 'w': '#ffffff', 'p': lip, 'r': inner}[ch])


def _face_m(kind=None, glow=None):
    """his face (solid): warm porcelain, a short pale-gold fringe swept to his left, heavy straight brows, narrower glowing gold
    eyes, a straight nose with its shadow, a firm mouth, the jaw and chin drawn in shade (no blush)"""
    im = _shade(FACE_SKIN_M[0], FACE_SKIN_M[1:], 4201, 0.08)
    for y in range(32):                                                      # the jaw: a square line in shade coming in to the chin
        for x in range(36):
            k = y - 19
            if k <= 0: continue
            e = min(k * 0.9, 8)                                              # (how far in the jaw has come at this row)
            if x < e - 1 or x > 35 - e + 1: _put(im, x, y, JAW_M)
            elif x < e or x > 35 - e: _put(im, x, y, JAW_EDGE)
            elif x < e + 1.4 or x > 34 - e: _put(im, x, y, _mix(FACE_SKIN_M[0], JAW_M, 0.5))
    for x in range(10, 26): _put(im, x, 31, _mix(FACE_SKIN_M[0], JAW_M, 0.7))   # (the chin's square underside)
    for x in range(15, 21): _put(im, x, 30, _mix(FACE_SKIN_M[0], JAW_M, 0.35))
    for cx in (5, 30):                                                       # (cheekbones)
        for x in range(cx - 2, cx + 3): _put(im, x, 23, _mix(FACE_SKIN_M[0], JAW_M, 0.45))
    hd, hm, hl = hexc(HAIR_D, 255), hexc(HAIR, 255), hexc(HAIR_L, 255)
    for x in range(36):                                                      # the fringe: short, swept to his left (the sheet's right)
        edge = 6 + (1 if (x // 3) % 2 else 0) - (1 if x > 26 else 0) + (2 if x < 3 or x > 33 else 0)
        for y in range(edge):
            j = (x + y + y // 2) % 4
            c = (hm, hl, hm, hd)[j]
            if y == edge - 1: c = hd
            _put(im, x, y, c)
    _brows_m(im, kind)
    glow = glow if glow is not None else Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    for (cx, y0), flip in zip(EYES_M, (False, True)):
        _eye_m(im, glow, cx, y0, flip, kind)
    for y in range(19, 25): _put(im, 18, y, '#e4b49c')                     # the nose: a straight shade line, its tip
    for x in (16, 17, 19): _put(im, x, 24, '#e0ae96')
    _put(im, 17, 23, '#ecc0a8')
    _mouth_m(im, kind)
    return im


def _eyes_glow_m(kind=None):
    g = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); _face_m(kind, g); return g


def textures_m():
    T = {'lb_face_m': _face_m(), 'lb_eyes_m': _eyes_glow_m()}
    for k in FACES:
        T[f'lb_face_m_{k}'] = _face_m(k)
        if k in OPEN_EYES: T[f'lb_eyes_m_{k}'] = _eyes_glow_m(k)
    return T


def _tunic_w(i):
    """tier i's half width, half depth: a straight long tunic (3.85 x 2.75 under the belt, 4.5 x 3.2 at the hem)"""
    t = (i + 1) / (len(ROBE_Y) - 1)
    return 3.85 + 0.65 * t, 2.75 + 0.45 * t


TABARD = 1.5                                         # (the tabard's half width, front and back)


def _tier_m(i, pv):
    """one tier of his tunic: straight, pearl; the tabard down the front - purple, gold-edged; the hem in gold"""
    y1, y0 = ROBE_Y[i], ROBE_Y[i + 1]
    hw, hd = _tunic_w(i)
    last = i == len(ROBE_Y) - 2
    out = [el((-hw, y0, -hd), (hw, y1, hd), 'lb_robe', pv, faces=_faces_but('up'), shift=(0.17 * i, 0.31 * i))]
    if i > 0:
        pw, pd = _tunic_w(i - 1)
        for (a, b) in (((-hw, y1 - 0.01, -hd), (hw, y1, -pd)), ((-hw, y1 - 0.01, pd), (hw, y1, hd)),
                       ((-hw, y1 - 0.01, -pd), (-pw, y1, pd)), ((pw, y1 - 0.01, -pd), (hw, y1, pd))):
            out.append(el(a, b, 'lb_robe', pv, faces=('up',), shift=(0.3, 0.6)))
    tw = TABARD
    out += [el((-tw, y0, -hd - 0.05), (tw, y1, -hd - 0.02), 'lb_stole', pv, faces=('north',), shift=(0.2 * i, 0.4)),
            el((-tw - 0.4, y0, -hd - 0.07), (-tw, y1, -hd - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), shift=(0.1 * i, 0.2), light=4),
            el((tw, y0, -hd - 0.07), (tw + 0.4, y1, -hd - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), shift=(0.3 * i, 0.5), light=4)]
    if last:
        out.append(el((-hw - 0.08, y0, -hd - 0.08), (hw + 0.08, y0 + 0.8, hd + 0.08), 'lb_hem', pv, faces=_faces_but('up'),
                      uv={f: [0, 0, 16, 0.8] for f in ('north', 'south', 'east', 'west')}))
        out.append(el((-hw - 0.08, y0 + 0.79, -hd - 0.08), (hw + 0.08, y0 + 0.8, hd + 0.08), 'lb_gold', pv, faces=('up',)))
    return out


def _sun(pv, y, z):
    """the gold sun of the Divine One: a gold lozenge, a core of light"""
    return [el((-0.95, y - 0.95, z - 0.06), (0.95, y + 0.95, z + 0.04), 'lb_gold', pv, rot=('z', 45, (0, y, z)), light=10),
            el((-0.4, y - 0.4, z - 0.12), (0.4, y + 0.4, z - 0.06), 'lb_light', pv, faces=('north',), light=15)]


def _male(M, part):
    """his twin of every part (MALE): his own body, skirt, head (and its faces), tabard (the 'hair' joints), arms and feet;
    the halo, the staff, the wings and the kneeling pool are hers, unchanged"""
    for p in ('halo', 'staff', 'wingr', 'wingl', 'pool'):
        M[f'lb_{p}{MALE}'] = M[f'lb_{p}']
    for w in ('lb_wingr', 'lb_wingl'): JOINTS[w + MALE] = JOINTS[w]
    # ---- the body: the tunic's upper tiers, the gold sword-belt, a broad chest (the surcoat - the bodice's own silk), broad
    #      shoulders, the gold collar, a thicker neck; the tabard from the collar to the hem, the sun on its breast
    pv = PIVOT['body']
    body = []
    for i in range(5):
        body += _tier_m(i, pv)
    CW, CD = 3.6, 2.3                                                          # (his chest's half width, half depth)
    body += [el((-4.0, 13.1, -2.9), (4.0, 14.5, 2.9), 'lb_gold', pv, faces=_faces_but('down'), shift=(0.2, 0.2), light=4),    # the belt
             el((-0.75, 13.15, -3.02), (0.75, 14.45, -2.9), 'lb_gold', pv, light=6),                                            # its buckle
             el((-0.35, 13.45, -3.1), (0.35, 14.15, -3.02), 'lb_sapph', pv, faces=('north',)),
             el((-CW, 14.5, -CD), (CW, 21.4, CD), 'lb_robe', pv, faces=('south', 'east', 'west'), shift=(0.3, 0.2)),          # the chest
             el((-CW, 14.5, -CD), (CW, 21.4, -CD), 'lb_bodice', pv, faces=('north',), uv={'north': [0, 0, 7.9, 6.9]}),
             el((-4.25, 21.4, -2.45), (4.25, 22.8, 2.45), 'lb_robe', pv, faces=_faces_but('down'), shift=(0.6, 0.1)),            # the shoulders
             el((-4.27, 21.38, -2.47), (4.27, 21.62, 2.47), 'lb_gold', pv, faces=('north', 'south', 'east', 'west'), light=4),  # (their gold edge)
             el((-2.3, 22.8, -2.1), (2.3, 23.4, 2.1), 'lb_gold', pv, faces=_faces_but('down'), light=4),                        # the collar
             el((-1.5, 23.4, -1.45), (1.5, 24.6, 1.45), 'lb_skin', pv, faces=('north', 'south', 'east', 'west'))]               # the neck
    tw = TABARD
    body += [el((-tw, 14.5, -CD - 0.06), (tw, 22.82, -CD - 0.02), 'lb_stole', pv, faces=('north',), shift=(0.4, 0.1)),       # the tabard, its front
             el((-tw - 0.4, 14.5, -CD - 0.08), (-tw, 22.82, -CD - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), light=4),
             el((tw, 14.5, -CD - 0.08), (tw + 0.4, 22.82, -CD - 0.02), 'lb_gold', pv, faces=('north', 'west', 'east'), light=4),
             el((-tw - 0.4, 22.8, -2.47), (tw + 0.4, 22.84, -CD - 0.02), 'lb_stole', pv, faces=('up',))]
    body += _sun(pv, 19.3, -CD - 0.1)
    part('lb_body' + MALE, body)
    skirt = []
    for i in range(5, len(ROBE_Y) - 1):
        skirt += _tier_m(i, PIVOT['skirt'])
    part('lb_skirt' + MALE, skirt)

    # ---- the head: the same head and face plate; short cropped hair - a close cap, the back only to the nape, short sides
    #      over his ears, a swept fringe; no long locks
    pv = PIVOT['head']

    def head(face=None):
        tex = 'lb_face_m' if face is None else f'lb_face_m_{face}'
        hr = lambda fr, to, faces=None, sh=None, rot=None: el(fr, to, 'lb_hair', pv, faces=faces, shift=sh, rot=rot)
        C1, C2 = ((-4.8, HT - 1.2, -4.3), (4.8, HT + 0.5, 4.5)), ((-4.1, HT + 0.5, -3.5), (4.1, HT + 1.05, 3.9))
        B1 = ((-4.75, HB + 0.7, 3.4), (4.75, HT - 1.2, 4.5))
        h = [el((-4.5, HB, -4.0), (4.5, HT - 1.2, 3.4), 'lb_skin', pv, faces=('east', 'west', 'down', 'south')),
             dict(el((-4.5, HB, -4.0), (4.5, HT, -4.0), tex, pv, faces=('north',), uv={'north': [0, 0, 9, 8]}), shade=False),
             hr(*C1, faces=('north', 'south', 'east', 'west', 'down'), sh=(0.2, 0.1)),
             hr(*C2, faces=('north', 'south', 'east', 'west', 'up'), sh=(0.6, 0.4)),
             hr(*B1, faces=('south', 'east', 'west', 'down'), sh=(0.5, 0.3)),
             hr((4.5, HB + 3.4, -3.0), (4.95, HT - 1.2, 3.4), faces=('north', 'east', 'down'), sh=(0.1, 0.4)),          # the sides, short
             hr((-4.95, HB + 3.4, -3.0), (-4.5, HT - 1.2, 3.4), faces=('north', 'west', 'down'), sh=(0.6, 0.2)),
             hr((4.5, HB + 1.6, -3.0), (4.85, HB + 3.4, -1.9), faces=('north', 'east', 'south', 'down'), sh=(0.3, 0.3)),   # sideburns
             hr((-4.85, HB + 1.6, -3.0), (-4.5, HB + 3.4, -1.9), faces=('north', 'west', 'south', 'down'), sh=(0.7, 0.3)),
             el((4.5, HB + 1.9, -0.9), (4.95, HB + 3.6, 0.5), 'lb_skin', pv, faces=('north', 'south', 'east', 'down', 'up')),  # the ears
             el((-4.95, HB + 1.9, -0.9), (-4.5, HB + 3.6, 0.5), 'lb_skin', pv, faces=('north', 'south', 'west', 'down', 'up')),
             hr((-4.9, HT - 1.85, -4.6), (4.9, HT - 1.2, -4.0), faces=('north', 'east', 'west', 'down'), sh=(0.3, 0.6))]      # the fringe
        h += _ring_up(C1, C2, 'lb_hair', pv)
        for x, a in ((-3.9, 32), (-0.4, 28), (2.6, 24)):                          # its swept points (to his left: the sheet's right)
            h.append(el((x - 0.5, HT - 2.25, -4.62), (x + 0.5, HT - 1.6, -4.04), 'lb_hair', pv, faces=('north', 'east', 'west', 'down'),
                        rot=('z', -a, (x, HT - 1.9, -4.33)), shift=(0.1 * x, 0.3)))
        if face in OPEN_EYES:                                     # his eyes, lit: each iris again, just in front, glowing
            gt = 'lb_eyes_m' if face is None else f'lb_eyes_m_{face}'
            for (cx, y0) in EYES_M:
                u0, u1, v0, v1 = (cx - 6) / 4, (cx + 6) / 4, (y0 - 2) / 4, (y0 + EYE_H_M + 2) / 4
                h.append(dict(el((4.5 - u1, HT - v1, -4.03), (4.5 - u0, HT - v0, -4.02), gt, pv, faces=('north',),
                                 uv={'north': [u0, v0, u1, v1]}, light=15), shade=False))
        return h
    part('lb_head' + MALE, head())
    for fc in FACES:
        part(f'lb_head_x{fc}{MALE}', head(fc))

    # ---- the tabard's back (on the 'hair' joints, so it streams back in flight and drapes over the robe when he kneels):
    #      from under the collar between the wings' roots to the belt, the sun on it; then on down to the backs of his knees
    pv = PIVOT['hair']
    bz = 2.5
    up = [el((-1.5, 14.6, bz), (1.5, 22.75, bz + 0.3), 'lb_stole', pv, faces=('south', 'up', 'down'), shift=(0.3, 0.2)),
          el((-1.84, 14.6, bz), (-1.5, 22.75, bz + 0.34), 'lb_gold', pv, faces=('south', 'east', 'west', 'up', 'down'), light=4),
          el((1.5, 14.6, bz), (1.84, 22.75, bz + 0.34), 'lb_gold', pv, faces=('south', 'east', 'west', 'up', 'down'), light=4)]
    up += [el((-0.8, 18.6, bz + 0.3), (0.8, 20.2, bz + 0.4), 'lb_gold', pv, rot=('z', 45, (0, 19.4, bz + 0.35)), light=10),
           el((-0.35, 19.05, bz + 0.4), (0.35, 19.75, bz + 0.46), 'lb_light', pv, faces=('south',), light=15)]
    JOINTS['lb_hair' + MALE] = {0: ('body',), 1: ('body',), 2: ('body',)}
    part('lb_hair' + MALE, up)
    pv = PIVOT['hairlo']
    A_, B_ = (0, 14.6, 3.12), (0, 3.6, 3.6)
    lo = [seg(A_, B_, 3.1, 0.28, 'lb_stole', pv, FRONT, ext=0.0, shift=(0.5, 0.3))]
    for sx in (-1, 1):
        lo.append(seg((sx * 1.72, A_[1], A_[2]), (sx * 1.72, B_[1], B_[2]), 0.34, 0.32, 'lb_gold', pv, FRONT, ext=0.0, light=4))
    lo.append(seg((0, B_[1] + 0.55, B_[2] - 0.02), (0, B_[1], B_[2]), 3.8, 0.34, 'lb_gold', pv, FRONT, ext=0.0, light=6))   # (its gold hem)
    JOINTS['lb_hairlo' + MALE] = {0: ('hair',)}
    part('lb_hairlo' + MALE, lo)

    # ---- the arms: broad pearl sleeves under gold pauldrons (two plates, a sapphire stud); gold vambraces, a blue band at the wrist
    def upper(sx):
        pv = PIVOT['armr' if sx > 0 else 'arml']; x0, y0, _ = pv
        e = (sx * 4.9, 18.6, 0)
        X = lambda a, b: (min(sx * a, sx * b), max(sx * a, sx * b))
        p1, p2 = X(4.3, 5.95), X(4.2, 6.1)
        return [seg((x0, y0 + 0.15, 0), e, 2.1, 2.1, 'lb_robe', pv, FRONT, ext=0.0, shift=(0.3, 0.1)),
                el((p1[0], 21.9, -1.3), (p1[1], 23.05, 1.3), 'lb_gold', pv, light=5, shift=(0.2, 0.4)),                  # the pauldron
                el((p2[0], 20.9, -1.3), (p2[1], 21.95, 1.3), 'lb_gold', pv, faces=_faces_but('up'), light=5, shift=(0.6, 0.1)),
                el((X(5.95, 6.07)[0], 22.2, -0.4), (X(5.95, 6.07)[1], 23.0, 0.4), 'lb_sapph', pv, light=6)]

    def lower(sx):
        pv = PIVOT['forer' if sx > 0 else 'forel']; ex, ey, _ = pv
        wx, wy = sx * 5.1, 14.6
        return [seg((ex, ey, 0), (wx, wy + 2.0, 0), 2.0, 2.0, 'lb_robe', pv, FRONT, ext=0.0, shift=(0.6, 0.4)),
                seg((ex + sx * 0.12, wy + 2.6, 0), (wx, wy + 0.55, 0), 2.2, 2.2, 'lb_gold', pv, FRONT, ext=0.0, light=5),       # the vambrace
                seg((wx, wy + 0.55, 0), (wx, wy + 0.05, 0), 2.3, 2.3, 'lb_blue', pv, FRONT, ext=0.0),                         # its blue band
                el((wx - 0.85, wy - 2.35, -0.88), (wx + 0.85, wy + 0.05, 0.82), 'lb_skin', pv, faces=_faces_but('up')),       # the hand
                el((wx - 0.7, wy - 2.8, -0.82), (wx + 0.7, wy - 2.35, -0.2), 'lb_skin', pv, faces=_faces_but('up'))]
    part('lb_armr' + MALE, upper(1)); part('lb_arml' + MALE, upper(-1)); part('lb_forer' + MALE, lower(1)); part('lb_forel' + MALE, lower(-1))

    # ---- the feet: armoured - gold sabatons over a pearl foot, a blue strap; from the ankle, toes pointing down as he floats
    def foot(sx):
        pv = PIVOT['legr' if sx > 0 else 'legl']; cx = pv[0]
        return [el((cx - 0.9, 0.2, -2.5), (cx + 0.9, 1.1, 0.95), 'lb_robe', pv, faces=_faces_but('up')),
                el((cx - 0.95, 0.15, -3.05), (cx + 0.95, 0.85, -0.9), 'lb_gold', pv, faces=_faces_but('up'), light=4),        # the toe plate
                el((cx - 0.92, 0.0, -3.1), (cx + 0.92, 0.2, 1.0), 'lb_gold', pv, light=3),                                   # the sole
                el((cx - 0.96, 0.55, -0.4), (cx + 0.96, 1.0, 1.02), 'lb_blue', pv, faces=_faces_but('down'))]                # a strap
    part('lb_legr' + MALE, foot(1)); part('lb_legl' + MALE, foot(-1))

# ---------------------------------------------------------------------------------------------------- poses
# (rigkit: ('x', -a) swings a hanging limb forward by a; ('x', +a) on the body or head leans/nods it forward)
def limb(sx, fwd=0.0, out=0.0, turn=0.0):
    return qs(('y', turn * sx), ('x', -fwd), ('z', -out * sx))


def wing(sx, fold=0.0, raise_=0.0, tilt=0.0):
    """a wing's turn at its root: fold sweeps it further back (negative brings it forward, round her); raise_ lifts it
    up and out (its feathers fan out to the side); tilt leans its top forward over her shoulder"""
    return qs(('y', fold * sx), ('z', -raise_ * sx), ('x', tilt))


def wings(fold=0.0, raise_=0.0, tilt=0.0, **kw):
    return dict(wingr=wing(1, fold, raise_, tilt), wingl=wing(-1, fold, raise_, tilt))


def P(**kw):
    return kw


def held(pose, lean=0.0, side=0.0, roll=0.0):
    """the pose with her staff upright in the world (leaned forward by lean, out to her right by side)"""
    pose = dict(pose)
    pose['staff'] = _upright(pose, 'staff', qs(('x', lean), ('z', side), ('y', roll)))
    return pose


TOES = dict(legr=qs(('x', -38)), legl=qs(('x', -30)))                  # (floating: the toes pointing down)
STAFF_ARM = dict(armr=limb(1, 8, 22), forer=limb(1, 34, 0, -16))
HEART = dict(arml=limb(-1, 30, 20), forel=limb(-1, 60, 0, 80))         # (her left hand raised before her breast)
REST = dict(**STAFF_ARM, **HEART, **TOES)
s = math.sin
POSES = {
    # floating at rest: the staff upright in her right hand, her left raised before her breast, wings at rest
    'idle_a': held(P(_off=(0, HOVER, 0), **REST, head=qs(('z', 4)), hairlo=qs(('z', 2))), 0, 6),
    # looking up toward the light, her left palm open at her side; the wings stir open a little
    'idle_b': held(P(_off=(0, HOVER + 0.4, 0), **STAFF_ARM, arml=limb(-1, 14, 20), forel=limb(-1, 24, 0, -40), **TOES,
                     head=qs(('x', -16), ('y', 6)), hair=qs(('z', -2)), hairlo=qs(('z', -3)), **wings(-6, 8)), 3, 6),
    # a quiet moment: eyes closed, head bowed, the wings drooping a little
    'idle_c': held(P(_face='blink', _off=(0, HOVER - 0.3, 0), **REST, head=qs(('x', 10)), body=qs(('x', 3)), **wings(4, 0)), 0, 6),
    # gliding: she doesn't step - a slow bob, the robe and feet trailing, a soft beat of the wings
    **{f'walk_{i}': held(P(_off=(0, HOVER + 0.5 + 0.35 * s(math.pi * i / 2), 0), body=qs(('x', 5), ('z', 2 * s(math.pi * i / 2))),
                           skirt=qs(('x', -7)), **STAFF_ARM, arml=limb(-1, 6 + 10 * s(math.pi * i / 2), 8), forel=limb(-1, 24),
                           legr=qs(('x', -48)), legl=qs(('x', -40)), head=qs(('x', -4)), hair=qs(('x', 10), ('z', 2 * s(math.pi * i / 2))),
                           hairlo=qs(('x', 6), ('z', 3 * s(math.pi * i / 2))), **wings(0, 6 + 6 * s(math.pi * i / 2))), 8, 6)
      for i in range(4)},
    # flying low and fast: leaning into it, the wings beating (up, out, down, in), the staff held out ahead like a lance
    **{f'run_{i}': held(P(_off=(0, HOVER + 3.0 + (0.6, 1.0, 0.4, 0.0)[i], 0), body=qs(('x', 34)), head=qs(('x', -22)), skirt=qs(('x', -20)),
                          armr=limb(1, 30, 14), forer=limb(1, 20), arml=limb(-1, -10, 18), forel=limb(-1, 16),
                          legr=qs(('x', -64)), legl=qs(('x', -58)), hair=qs(('x', 30)), hairlo=qs(('x', 14 - 4 * (i % 2)), ('z', (4, 0, -4, 0)[i])),
                          **wings(6, (12, 6, -16, 2)[i])), 74, 4)
      for i in range(4)},
    # a jump: the wings flung up for the downbeat
    'jump': held(P(_face='happy', _off=(0, HOVER + 4.0, 0), **STAFF_ARM, arml=limb(-1, 30, 30), forel=limb(-1, 20), legr=qs(('x', -50)),
                   legl=qs(('x', -44)), head=qs(('x', -8)), hair=qs(('x', 8)), hairlo=qs(('x', 10)), **wings(18, 16)), 0, 8),
    # SMITE: the staff raised high over her head, her left hand marking the foe ...
    'smite_up': held(P(_face='fierce', _off=(0, HOVER + 0.8, 0), body=qs(('y', 14), ('x', -4)), armr=limb(1, 140, 54), forer=limb(1, 10),
                       arml=limb(-1, 62, 28, 6), forel=limb(-1, 10), head=qs(('y', -10), ('x', -6), ('z', -6)), **TOES, **wings(4, 18)), -6, 10),
    # ... and brought down to point at it: the beam is called down where it points
    'smite': held(P(_face='fierce', _off=(0, HOVER + 0.2, -0.4), body=qs(('y', -10), ('x', 10)), armr=limb(1, 84, 16), forer=limb(1, 6),
                    arml=limb(-1, 10, 30), forel=limb(-1, 30), head=qs(('x', -4), ('y', 6)), hair=qs(('x', 14), ('z', 4)), hairlo=qs(('x', 6)), **TOES, **wings(0, 18)), 62, 6),
    # (the follow-through: the staff swung back upright, the wings closing)
    'smite_end': held(P(_face='fierce', _off=(0, HOVER, 0), body=qs(('x', 3)), **STAFF_ARM, arml=limb(-1, 20, 18), forel=limb(-1, 30),
                        head=qs(('x', 2)), **TOES, **wings(0, 10)), 4, 6),
    # BLESS: the staff held out, her left hand cupped low before her, gathering light ...
    'bless_a': held(P(_face='blink', _off=(0, HOVER, 0), body=qs(('x', 4)), armr=limb(1, 30, 16), forer=limb(1, 20),
                      arml=limb(-1, 24, 10), forel=limb(-1, 50, 0, 50), head=qs(('x', 12)), **TOES, **wings(4, 0)), 0, 4),
    # ... and arms opened wide, palms up: healing light poured out round her
    'bless': held(P(_face='happy', _off=(0, HOVER + 0.8, 0), body=qs(('x', -6)), armr=limb(1, 20, 62), forer=limb(1, 20),
                    arml=limb(-1, 20, 62), forel=limb(-1, 20, 0, 40), head=qs(('x', -12)), hairlo=qs(('x', 6)), **TOES, **wings(-6, 16)), 0, 16),
    # WARD: the wings lifted ...
    'ward_up': held(P(_face='fierce', _off=(0, HOVER + 0.4, 0), **STAFF_ARM, arml=limb(-1, 30, 14), forel=limb(-1, 50),
                      head=qs(('x', 4)), **TOES, **wings(0, 26)), 0, 6),
    # ... and swept forward round her like a shield, the staff planted before her
    'ward': held(P(_face='fierce', _off=(0, HOVER, 0), body=qs(('x', 4)), armr=limb(1, 40, 4), forer=limb(1, 40, 0, 20),
                   arml=limb(-1, 40, 4), forel=limb(-1, 60, 0, 60), head=qs(('x', 6)), **TOES, **wings(-62, 0, 10)), 0, 14),
    # PRAY: kneeling on her robe, the staff planted at her side, her left hand at her breast, head bowed, the wings folded down
    'pray': held(P(_pool=True, _face='blink', _off=(0, -4.6, 0), _o_staff=(0, 4.0, 0), **STAFF_ARM, **HEART, head=qs(('x', 12)), hairlo=qs(('x', 40)), **wings(8, -8)), 0, 8),
    # WINGS SPREAD (the charged move): gathered in, hunched ... then flung open wide, the staff held high, rising
    'wings_spread_up': held(P(_face='fierce', _off=(0, HOVER - 0.6, 0), body=qs(('x', 14)), **STAFF_ARM, arml=limb(-1, 20, 4), forel=limb(-1, 50, 0, 40),
                              head=qs(('x', 12)), hair=qs(('x', 12)), **TOES, **wings(24, -6)), 0, 10),
    'wings_spread': held(P(_face='surprised', _off=(0, HOVER + 2.6, 0), body=qs(('x', -8)), armr=limb(1, 130, 60), forer=limb(1, 6),
                           arml=limb(-1, 30, 76), forel=limb(-1, 10), head=qs(('x', -16)), legr=qs(('x', -50)), legl=qs(('x', -44)),
                           hair=qs(('x', 6)), hairlo=qs(('x', 16)), **wings(10, -20)), 0, 14),
    # sitting: kneeling back on her heels on the spread robe, the staff laid across her lap
    'sit_a': P(_pool=True, _off=(0, -5.5, 0), armr=limb(1, 24, 4), forer=limb(1, 50, 0, 20), arml=limb(-1, 24, 4), forel=limb(-1, 50, 0, 20),
               staff=qs(('z', 90)), head=qs(('z', 4)), hairlo=qs(('x', 58)), **wings(6, -8)),
    # a seated idle: the staff planted beside her, her left hand resting on her lap, looking up and smiling
    'sit_b': held(P(_pool=True, _face='happy', _off=(0, -5.5, 0), armr=limb(1, 40, 14), forer=limb(1, 30), arml=limb(-1, 18, 4),
                    forel=limb(-1, 50, 0, 30), head=qs(('x', -12), ('z', -6)), hairlo=qs(('x', 58)), **wings(4, 4)), 0, 8),
    'happy': held(P(_face='happy', _off=(0, HOVER + 1.0, 0), **STAFF_ARM, arml=limb(-1, 30, 40), forel=limb(-1, 30), head=qs(('z', 8), ('x', -4)),
                    **TOES, **wings(0, 18)), 0, 6),
    'hurt': held(P(_face='hurt', _off=(0, HOVER - 0.4, 0.5), body=qs(('x', -12)), head=qs(('x', -14)), **STAFF_ARM, arml=limb(-1, 34, 30),
                   forel=limb(-1, 50), **TOES, hair=qs(('x', 8)), hairlo=qs(('x', 8)), **wings(12, 8)), -8, 6),
    # worn out: she sinks to the ground on her robe, slumped, her head down, the staff leaning on her shoulder, the wings fallen
    'tired': held(P(_pool=True, _face='sad', _off=(0, -4.4, 0), _o_staff=(0, 3.4, 0), body=qs(('x', 12)), head=qs(('x', 16)), armr=limb(1, 20, 8), forer=limb(1, 30),
                    arml=limb(-1, 20, 4), forel=limb(-1, 40, 0, 30), hair=qs(('x', 12)), hairlo=qs(('x', 34)), **wings(14, -14)), -6, 14),
}
SWIM_FRAMES = 8
for _i in range(SWIM_FRAMES):                                  # (gliding through the water: a slow breaststroke, the wings laid back along her)
    _p = 2 * math.pi * _i / SWIM_FRAMES
    POSES[f'swim_{_i}'] = P(_swim=True, _staff='none', _off=(0, 3.0 + 0.4 * math.sin(2 * _p), 0), body=qs(('x', 70)), head=qs(('x', -20)),
                            skirt=qs(('x', -10)), armr=limb(1, 118 + 20 * math.sin(_p), 70 + 10 * math.cos(_p)), forer=limb(1, 16),
                            arml=limb(-1, 118 + 20 * math.sin(_p), 70 + 10 * math.cos(_p)), forel=limb(-1, 16),
                            hair=qs(('x', 10)), hairlo=qs(('x', 8 * math.sin(_p))), **wings(24, 8 + 3 * math.sin(_p)))
for _k, _v in POSES.items():                                   # (kneeling: the pool stays on the floor however low she sinks)
    if _v.get('_pool'): _v['_o_pool'] = (0.0, -_v['_off'][1], 0.0)
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_1', 'walk_3', 'run_0', 'run_2', 'jump', 'smite_up', 'smite', 'smite_end', 'bless_a', 'bless',
         'ward_up', 'ward', 'pray', 'wings_spread_up', 'wings_spread', 'sit_a', 'sit_b', 'happy', 'hurt', 'tired', 'swim_0', 'swim_2']
