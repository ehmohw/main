"""2.98: THE UNDERCROWN's item art - every model its items name (p2/underitems.py; the looks from undercrown_lore.py), the Stair
of a Thousand Eyes' wall eyes (phase237) and the Sovereign's trophy. gen_rp calls rp(R).

FLAT ICONS (16 x 16, the pack's vanilla look - through R.ICONS, so vanilla.process gives them its outline pass):
  ublack_seal    a black wax seal, its edge running, stamped with a chain link
  ukey           a trial key in the Dread's colours (vanilla's trial key, recoloured), a red eye set in its bow
  ukey_victor    the ominous trial key, darker, its red burning
  sov_eye        the follower's summons: a closed eye in a roundel of black plate, red light leaking from under the lid
  dawnshard      a sliver of white-gold light, sparkling
  unwriting      an old page, every line rubbed out but one word
  chainwhip      (handheld) a chain whip: a void-plate handle and guard, links of iron, a hooked barb at its end
  nine_lives     a little silver bell on a red ribbon
  ulantern_wick  a braided wick, its tip a coal, a small flame over it
3D MODELS (block textures uc_*, written in rp's post pass):
  ushard_snow / ushard_witch / ushard_shark   a jagged black-crown spike, broken off at its root, the Dread's red veins down it
                 (glowing): FEAR rimed with frost and icicles; HUNGER black glass with a green eye open in it; WAR crusted with
                 salt, a gold band round it. Chunky and lit, so they read hovering over the Throne Gate's sockets.
  dread_ember    a lump of dark coal, its red-hot core glowing out through the cracks (emissive), sparks over it
  sov_heart      the heart crystal stood on its point, smaller crystals at its foot (emissive)
  sov_edge       the Sovereign's own greatsword (dread_sovereign_art's weapon part), brought down to a handheld greatsword
                 and laid on the diagonal a vanilla sword's sprite takes - so vanilla's handheld transforms hold it right
  black_crown    the Sovereign's crowned helm (dread_sovereign_art's armored head, its burning slit glowing) at the size of the
                 Dread Visage: a model drawn for a head filling 3..13, shown 1.28 times on the head - worn as the Visage is
  unbound_helm   a dark-steel great-helm: a cross of eye slit and nasal, breaths, rivets, a crest, a broken chain off one side
  ueye_shut / ueye_open   the Stair's wall eyes: an almond of dark flesh in folds - shut: the lids met, red lashes over the seam;
                 open: the lids drawn back from a wet, veined, yellowed eye with a red iris and a slit pupil. Their front is
                 the model's north face: an item_display (context none) turns a model half round, so north faces the
                 display's +z, the way the Stair's markers look - out into the corridor.
  sov_trophy     a bust of the armored Sovereign (pauldrons, collar, the crowned helm) on a plinth of void-plate, red seams in
                 it; front north, model y 0 its foot (as the trophy3d_ figures)."""
import math
import random
from PIL import Image, ImageDraw

import rigkit
from rigkit import el, seg, euler

PIV = (8.0, 8.0, 8.0)                      # (3D models here are built straight in model units)
FRONT = (0.0, 0.0, -1.0)
VAN = '/home/claude/mc263/client/assets/minecraft/textures/item/'
VOID, VOID_L, RED, RED_L = (22, 16, 26), (48, 34, 54), (208, 24, 46), (255, 90, 100)
RED_D, EMBER = (118, 12, 28), (255, 170, 150)
FLAT = ('ublack_seal', 'ukey', 'ukey_victor', 'sov_eye', 'dawnshard', 'unwriting', 'chainwhip', 'nine_lives', 'ulantern_wick')
MODELS3D = ('ushard_snow', 'ushard_witch', 'ushard_shark', 'dread_ember', 'sov_heart', 'sov_edge', 'black_crown', 'unbound_helm',
            'ueye_shut', 'ueye_open', 'sov_trophy')
HANDHELD = {'chainwhip'}


# ==================================================================================================== flat icons
def _c(rgb, a=255):
    return tuple(int(max(0, min(255, v))) for v in rgb[:3]) + (a,)


def _mix(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


class Px:
    def __init__(self):
        self.im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); self.px = self.im.load()

    def p(self, x, y, col):
        if 0 <= x < 16 and 0 <= y < 16: self.px[int(x), int(y)] = _c(col)

    def get(self, x, y):
        return self.px[x, y] if 0 <= x < 16 and 0 <= y < 16 else (0, 0, 0, 0)

    def on(self, x, y):
        return self.get(x, y)[3] > 0

    def outline(self, col=(10, 6, 12)):
        """a dark rim round everything drawn (vanilla.process deepens it to a shade of what it wraps)"""
        pts = [(x, y) for y in range(16) for x in range(16) if not self.on(x, y) and
               any(self.on(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        for x, y in pts: self.p(x, y, col)

    def grid(self, rows, pal):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in pal: self.p(x, y, pal[ch])


def ramp(stops):
    def f(t):
        t = max(0.0, min(1.0, t))
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1: return _mix(c0, c1, (t - t0) / max(1e-6, t1 - t0))
        return stops[-1][1]
    return f


DREAD = ramp([(0.0, (8, 5, 10)), (0.3, (24, 17, 29)), (0.55, (48, 34, 56)), (0.8, (82, 60, 94)), (1.0, (132, 104, 146))])
DREAD_DK = ramp([(0.0, (5, 3, 6)), (0.35, (16, 11, 19)), (0.65, (34, 24, 40)), (1.0, (70, 52, 80))])


def _recolor_key(src, rmp, red_from=None):
    im = Image.open(VAN + src).convert('RGBA'); px = im.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if not a: continue
            if red_from and r > g + 40 and r > b + 30:                       # (the ominous key's own reds stay red, hotter)
                px[x, y] = _c(RED_L if r > 200 else RED); continue
            px[x, y] = _c(rmp((0.299 * r + 0.587 * g + 0.114 * b) / 200))
    return im


def ukey():
    im = _recolor_key('trial_key.png', DREAD); P = Px(); P.im = im; P.px = im.load()
    for x, y, c in ((7, 3, RED), (8, 3, RED_L), (7, 4, RED_D), (8, 4, RED)):    # (a red eye in the bow)
        P.p(x, y, c)
    P.p(7, 12, RED_D); P.p(9, 14, RED_D)                                       # (red in the bit's notches)
    return im


def ukey_victor():
    im = _recolor_key('ominous_trial_key.png', DREAD_DK, red_from=True); P = Px(); P.im = im; P.px = im.load()
    for x, y, c in ((7, 3, RED_L), (8, 3, RED_L), (7, 4, RED), (8, 4, RED), (6, 4, RED_D), (9, 4, RED_D)):
        P.p(x, y, c)
    for y in range(8, 12): P.p(7, y, RED_D)                                   # (a red seam down its shank)
    P.p(8, 12, RED); P.p(9, 13, RED); P.p(10, 14, RED_L)
    return im


def ublack_seal():
    """black wax: a wavy round blob, a raised rim, a chain link stamped in it; a run of wax off its foot"""
    P = Px(); cx, cy = 7.5, 7.6
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy; d = math.hypot(dx, dy); a = math.atan2(dy, dx)
            r = 6.3 + 0.55 * math.sin(a * 5 + 0.7)
            if d <= r:
                t = 0.45 - (dx * 0.55 + dy * 0.7) / 12
                if d > r - 1.3: t += 0.18                                      # (the rim, raised)
                P.p(x, y, DREAD(t))
    for x, y in ((9, 14), (9, 15), (10, 14)):                                   # (a drip)
        P.p(x, y, DREAD(0.3))
    # the stamp: a chain link pressed into it - its ring dark in the wax, lit along the lower right where the wax rises
    #             again, the ends of its neighbours above and below
    for y in range(16):
        for x in range(16):
            e = ((x - cx) / 2.4) ** 2 + ((y - cy) / 3.5) ** 2
            if 0.5 <= e <= 1.3:
                P.p(x, y, (8, 5, 10))
                e2 = ((x + 1 - cx) / 2.4) ** 2 + ((y + 1 - cy) / 3.5) ** 2
                if e2 > 1.3: P.p(x + 1, y + 1, DREAD(0.95))
                if e2 < 0.5: P.p(x + 1, y + 1, DREAD(0.75))
    for y in (2, 13):
        for x in (7, 8): P.p(x, y, (8, 5, 10))
        P.p(9, y + 1 if y == 2 else y, DREAD(0.9))
    P.p(3, 4, DREAD(0.95)); P.p(4, 3, DREAD(0.95)); P.p(4, 4, DREAD(0.85))       # (the shine)
    P.p(11, 5, RED_D)
    P.outline()
    return P.im


def sov_eye():
    """a roundel of black plate, a closed eye across it: the lid a dome of plate, its seam a line of red light, red lashes"""
    P = Px()
    for y in range(1, 15):
        for x in range(1, 15):
            if (x in (1, 14) and y in (1, 2, 13, 14)) or (y in (1, 14) and x in (1, 2, 13, 14)): continue
            P.p(x, y, DREAD(0.42 - (x + y - 15) * 0.02))
    for i in range(1, 15):                                                      # (a lit top edge, a seam round the rim)
        P.p(i, 1 if 3 <= i <= 12 else 2, DREAD(0.8))
    for (x, y) in ((3, 3), (12, 3), (3, 12), (12, 12)):                         # (rivets)
        P.p(x, y, DREAD(0.9)); P.p(x + 1, y + 1, DREAD(0.1))
    lid = [(3, 8), (4, 7), (5, 6), (6, 6), (7, 5), (8, 5), (9, 6), (10, 6), (11, 7), (12, 8)]
    for x, y in lid:                                                            # (the lid's dome)
        for yy in range(y, 8): P.p(x, yy, DREAD(0.62 + (8 - yy) * 0.06))
    for x in range(3, 13):                                                      # (the seam: red light)
        P.p(x, 8, RED_L if 5 <= x <= 10 else RED)
        P.p(x, 9, RED_D if 4 <= x <= 11 else DREAD(0.3))
    for x, y in ((4, 10), (6, 10), (8, 10), (10, 10), (11, 10), (5, 11), (9, 11)):   # (lashes, hanging)
        P.p(x, y, RED if y == 10 else RED_D)
    P.outline()
    return P.im


def dawnshard():
    """a sliver of the last light: white at its heart, gold along its edges, a star at its tip"""
    P = Px()
    W, G, GL, GD = (255, 255, 250), (232, 182, 48), (255, 228, 120), (150, 100, 20)
    pts = [(3 + i * 0.75, 13 - i) for i in range(12)]
    for i, (x, y) in enumerate(pts):
        xi = int(round(x))
        w = 1 if i < 2 or i > 9 else 2
        for k in range(-w, w + 1):
            c = W if k == 0 else (GL if abs(k) == 1 else G)
            if k == w: c = G if i > 6 else GD
            P.p(xi + k, y, c)
    for x, y, c in ((12, 0, W), (12, 2, GL), (11, 1, GL), (13, 1, GL), (2, 4, GL), (3, 5, W), (13, 9, GL), (5, 14, GL)):
        P.p(x, y, c)
    P.outline((60, 40, 8))
    return P.im


def unwriting():
    """an old page, its corner curling, every line rubbed to a smudge but one word, dark and plain"""
    P = Px()
    PAGE, EDGE, SMUDGE, INK = (232, 220, 190), (190, 168, 128), (212, 198, 168), (52, 34, 26)
    for y in range(1, 15):
        for x in range(2, 14):
            if x >= 11 and y <= 13 - x + 12 - 10 and y < 4: continue
            P.p(x, y, PAGE if (x + y) % 5 else (224, 210, 178))
    for y in range(1, 15): P.p(2, y, EDGE); P.p(13, y, EDGE if y > 3 else EDGE)
    for x in range(2, 14): P.p(x, 14, EDGE)
    for x, y in ((11, 1), (12, 1), (13, 1), (12, 2), (13, 2), (13, 3)):       # (the dog-eared corner)
        P.px[x, y] = (0, 0, 0, 0)
    for x, y in ((11, 2), (11, 3), (12, 3)): P.p(x, y, EDGE)
    for y in (3, 5, 10, 12):                                                    # (the lines, rubbed out)
        for x in range(4, 12 if y > 3 else 10):
            if (x * 7 + y) % 4: P.p(x, y, SMUDGE)
    glyph = ['xx.x.xx.x', 'x.xx.x..x', 'xx.x.xx.x']
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch == 'x': P.p(4 + i, 7 + j, INK)
    P.outline((70, 52, 34))
    return P.im


def chainwhip():
    """(handheld) a void-plate handle at the bottom left, a guard; links of iron up and over to the top right, a hooked barb"""
    P = Px()
    H, HL, GD = DREAD(0.35), DREAD(0.7), DREAD(0.55)
    for i in range(4):                                                          # (the handle, diagonal, wrapped)
        x, y = 1 + i, 14 - i
        P.p(x, y, H if i % 2 else HL); P.p(x + 1, y, H)
    P.p(1, 15, RED); P.p(0, 15, RED_D)                                          # (a red stone in the pommel)
    for x, y in ((4, 9), (5, 10), (6, 11), (7, 12), (5, 9), (6, 10)):           # (the guard)
        P.p(x, y, GD)
    P.p(5, 10, RED)
    pts = [(6, 9), (7, 8), (8, 7), (9, 6), (10, 5), (11, 5), (12, 4), (13, 4), (13, 3), (14, 2)]
    for i, (x, y) in enumerate(pts):                                            # (links: rings, and links edge-on between them)
        if i % 2 == 0:
            P.p(x, y, (150, 140, 158)); P.p(x + 1, y, (96, 88, 104)); P.p(x, y - 1, (110, 102, 120))
        else:
            P.p(x, y, (70, 64, 78))
    for x, y, c in ((15, 1, (180, 170, 186)), (15, 2, (120, 112, 128)), (14, 0, (180, 170, 186)), (13, 1, RED_D)):     # (the barb)
        P.p(x, y, c)
    P.outline()
    return P.im


def nine_lives():
    """a little silver bell (its clapper, a shine) hung from a bow of red ribbon"""
    P = Px()
    S, SL, SD, SW = (196, 200, 212), (236, 240, 248), (120, 124, 140), (255, 255, 255)
    R1, R2 = (196, 36, 58), (140, 20, 40)
    rows = {6: (6, 9), 7: (5, 10), 8: (5, 10), 9: (4, 11), 10: (4, 11), 11: (3, 12), 12: (3, 12)}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            t = (x - a) / max(1, b - a)
            P.p(x, y, SL if t < 0.25 else (S if t < 0.7 else SD))
    for x in range(3, 13): P.p(x, 13, SD)
    P.p(7, 14, (60, 60, 70)); P.p(8, 14, (40, 40, 50))                            # (the clapper)
    P.p(5, 8, SW); P.p(5, 9, SL)
    for x in (7, 8): P.p(x, 5, SD)                                              # (its loop)
    bow = ['..rr....rr..', '.rRRr..rRRr.', '..rrRRRRrr..', '....rRRr....', '...rr..rr...']
    for j, row in enumerate(bow):
        for i, ch in enumerate(row):
            if ch != '.': P.p(2 + i, j, R1 if ch == 'R' else R2)
    P.outline()
    return P.im


def ulantern_wick():
    """a braided wick in a little iron cup, its tip a live coal, a small flame standing over it"""
    P = Px()
    C1, C2, IR, IRL = (226, 206, 168), (160, 128, 86), (70, 66, 74), (120, 114, 126)
    for y in range(7, 13):                                                      # (the braid)
        P.p(7, y, C1 if y % 2 else C2); P.p(8, y, C2 if y % 2 else C1)
    for x in range(5, 11): P.p(x, 13, IR); P.p(x, 14, IR)
    P.p(5, 12, IR); P.p(10, 12, IR); P.p(6, 13, IRL); P.p(5, 13, IRL)
    P.p(7, 6, (255, 120, 40)); P.p(8, 6, (220, 70, 30))                          # (the coal at its tip)
    fl = ['...y...', '..yYy..', '..YWY..', '.yYWWy.', '.yYWYy.', '..yYy..']
    for j, row in enumerate(fl):
        for i, ch in enumerate(row):
            if ch != '.': P.p(4 + i, j, {'y': (255, 150, 40), 'Y': (255, 200, 80), 'W': (255, 250, 220)}[ch])
    P.p(2, 3, (255, 200, 80)); P.p(13, 5, (255, 180, 60)); P.p(12, 1, (255, 220, 120))
    P.outline()
    return P.im


def icons():
    return {'ublack_seal': ublack_seal(), 'ukey': ukey(), 'ukey_victor': ukey_victor(), 'sov_eye': sov_eye(), 'dawnshard': dawnshard(),
            'unwriting': unwriting(), 'chainwhip': chainwhip(), 'nine_lives': nine_lives(), 'ulantern_wick': ulantern_wick()}


# ==================================================================================================== block textures (uc_*)
def _cells(base, seed, var=0.12, size=64, cz=2, spots=(), add=5):
    rnd = random.Random(seed); im = Image.new('RGBA', (size, size)); d = ImageDraw.Draw(im)
    for cy in range(0, size, cz):
        for cx in range(0, size, cz):
            k = 1 + rnd.uniform(-var, var); a = rnd.uniform(-add, add)
            d.rectangle((cx, cy, cx + cz - 1, cy + cz - 1), fill=_c(tuple(v * k + a for v in base)))
    for col, n in spots:
        for _ in range(n):
            x, y = rnd.randrange(0, size, cz), rnd.randrange(0, size, cz)
            d.rectangle((x, y, x + cz - 1, y + cz - 1), fill=_c(col))
    return im


def _veins(im, seed, n, col, hot=None, size=64):
    rnd = random.Random(seed); d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y = rnd.randrange(0, size, 2), rnd.randrange(0, size, 2)
        for i in range(rnd.randint(5, 12)):
            d.rectangle((x, y, x + 1, y + 1), fill=_c(hot if (hot and i == 0) else col))
            x = (x + rnd.choice((-2, 0, 2))) % size; y = (y + 2) % size
    return im


def _eye_tex(kind, iris=(255, 60, 40), sclera=(222, 206, 160)):
    """a painted eye (whole uv; drawn at 32, doubled): open - a veined yellowed eye, a red iris, a slit pupil, wet shines;
    green - a small green eye for the witch's shard"""
    N = 32; im = Image.new('RGBA', (N, N), _c(sclera)); d = ImageDraw.Draw(im); rnd = random.Random(9)
    for _ in range(14):                                                         # (veins, from the rim in)
        x, y = rnd.choice((0, N - 1)), rnd.randrange(N)
        for _s in range(rnd.randint(4, 10)):
            d.point((x, y), fill=_c((176, 30, 36))); x += 1 if x < N // 2 else -1; y += rnd.choice((-1, 0, 1))
    if kind == 'green':
        d.rectangle((0, 0, N - 1, N - 1), fill=_c((10, 26, 14)))
        d.ellipse((4, 4, N - 5, N - 5), fill=_c((80, 230, 70))); d.ellipse((9, 9, N - 10, N - 10), fill=_c((170, 255, 120)))
        d.rectangle((N // 2 - 2, 5, N // 2 + 1, N - 6), fill=_c((4, 10, 4))); d.rectangle((9, 8, 11, 10), fill=_c((240, 255, 230)))
        return im.resize((64, 64), Image.NEAREST)
    # (the wall eye: its texture stretched 15 wide by 10 tall, so the iris is painted narrow to come out round)
    cx, cy, ry = N // 2, N // 2, 13; rx = int(ry * 10 / 15)
    d.ellipse((cx - rx - 1, cy - ry - 1, cx + rx + 1, cy + ry + 1), fill=_c((60, 4, 10)))
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=_c(iris))
    d.ellipse((cx - rx + 2, cy - ry + 3, cx + rx - 2, cy + ry - 3), fill=_c((255, 110, 60)))
    d.ellipse((cx - rx + 4, cy - ry + 6, cx + rx - 4, cy + ry - 6), fill=_c((255, 170, 90)))
    d.rectangle((cx - 1, cy - ry + 1, cx, cy + ry - 1), fill=_c((6, 0, 2)))
    d.rectangle((cx - 2, cy - 5, cx + 1, cy + 4), fill=_c((6, 0, 2)))
    for (x, y, w, h) in ((cx - rx + 1, cy - ry + 3, 2, 3), (cx + rx - 4, cy + 3, 1, 2), (4, 8, 2, 2)):   # (wet shines)
        d.rectangle((x, y, x + w - 1, y + h - 1), fill=_c((255, 255, 255)))
    for y in range(N):                                                          # (darker toward its corners)
        for x in range(N):
            e = ((x - cx) / (N / 2)) ** 2 + ((y - cy) / (N / 2)) ** 2
            if e > 0.75:
                r, g, b, a = im.getpixel((x, y)); k = 0.65
                im.putpixel((x, y), (int(r * k), int(g * k), int(b * k), a))
    return im.resize((64, 64), Image.NEAREST)


def _ds_textures():
    """the Sovereign's own textures (dread_sovereign_art), under uc_ names"""
    import dread_sovereign_art as DS
    return {'uc_' + k[3:]: v for k, v in DS.textures().items()}


def textures():
    T = _ds_textures()
    T.update({
        'uc_frost': _cells((196, 226, 246), 501, 0.08, spots=[((255, 255, 255), 90), ((150, 196, 230), 60)]),
        'uc_ice': _cells((150, 210, 240), 502, 0.1, spots=[((230, 248, 255), 50)]),
        'uc_gmote': _cells((120, 255, 100), 520, 0.08),
        'uc_kglass': _veins(_cells((16, 12, 22), 503, 0.2, spots=[((60, 44, 80), 60), ((40, 90, 60), 30)]), 504, 4, RED_D, RED),
        'uc_geye': _eye_tex('green'),
        'uc_salt': _cells((214, 210, 200), 505, 0.1, spots=[((250, 250, 246), 120), ((170, 164, 150), 70)]),
        'uc_gold': _cells((232, 182, 48), 506, 0.1, spots=[((255, 228, 120), 60), ((160, 110, 24), 40)]),
        'uc_coal': _veins(_cells((26, 18, 24), 507, 0.18, spots=[((44, 30, 40), 80), ((10, 6, 10), 50)]), 508, 10, RED_D, RED),
        'uc_flesh': _veins(_cells((46, 20, 30), 509, 0.14, spots=[((28, 10, 18), 120), ((66, 32, 42), 50)]), 510, 8, (104, 18, 30)),
        'uc_fold': _cells((24, 10, 16), 511, 0.15, spots=[((14, 5, 9), 120), ((40, 18, 26), 50)]),
        'uc_lash': _cells(RED, 512, 0.1, spots=[(RED_L, 40)]),
        'uc_seam': _cells((10, 2, 6), 513, 0.1, spots=[(RED_D, 30)]),
        'uc_weye': _eye_tex('open'),
        'uc_steel': _cells((66, 72, 84), 514, 0.1, spots=[((96, 104, 118), 60), ((40, 44, 52), 60), ((90, 50, 40), 10)]),
        'uc_steel_l': _cells((112, 120, 134), 515, 0.08, spots=[((150, 158, 170), 40)]),
        'uc_slit': _cells((6, 6, 8), 516, 0.05),
        'uc_iron': _cells((74, 68, 82), 517, 0.1, spots=[((110, 100, 120), 40)]),
        'uc_stone': _veins(_cells((30, 22, 34), 518, 0.12, spots=[((46, 34, 52), 70)]), 519, 3, RED_D, RED),
    })
    return T


# ==================================================================================================== 3D models
def B(fr, to, tex, light=0, rot=None, uv=None, faces=None, shift=True):
    rs = B.rnd
    return el(fr, to, tex, PIV, rot=rot, uv=uv, faces=faces, light=light, shift=(rs.random(), rs.random()) if shift and not uv else None)


B.rnd = random.Random(7)


def S(a, b, w, h, tex, light=0, up=FRONT):
    return seg(a, b, w, h, tex, PIV, up, 0.15, light=light, shift=(B.rnd.random(), B.rnd.random()))


def CH(pts, ws, hs, tex, light=0, up=FRONT, texs=None):
    out = []
    for i in range(len(pts) - 1):
        t = texs[i] if texs else tex
        out.append(S(pts[i], pts[i + 1], ws[i], hs[i], t, light if (texs is None or t in ('uc_horn_r', 'uc_red', 'uc_red_l')) else 0, up))
    return out


def GEM(c, s, tex, light=15, rot=(35.26, 45.0, 0.0)):
    return el((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, PIV, rot=(rot, c), light=light)


def _rot_of(e):
    """an element's box: its centre after its own turn, the turn (a matrix), its half sizes"""
    f, t = e['from'], e['to']
    c = [(f[i] + t[i]) / 2 for i in range(3)]; h = [(t[i] - f[i]) / 2 for i in range(3)]
    R = [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]
    if 'rotation' in e:
        import dread_sovereign_art as DS
        R = DS._rotm(e['rotation']); o = e['rotation']['origin']
        c = [sum(R[i][k] * (c[k] - o[k]) for k in range(3)) + o[i] for i in range(3)]
    return c, R, h


def reframe(els, fpt, G, s):
    """carry elements through a map: each box's centre through fpt (a point -> point), its turn through G (a rotation
    matrix: the map's own turn), its size scaled by s - faces and their texture windows untouched"""
    out = []
    for e in els:
        c, R, h = _rot_of(e)
        nc = fpt(c)
        R2 = [[sum(G[i][k] * R[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
        ne = {k: v for k, v in e.items() if k not in ('from', 'to', 'rotation')}
        ne['from'] = [round(nc[i] - h[i] * s, 4) for i in range(3)]; ne['to'] = [round(nc[i] + h[i] * s, 4) for i in range(3)]
        ang = euler(R2)
        if max(abs(a) for a in ang) > 1e-3:
            ne['rotation'] = {'origin': [round(v, 4) for v in nc], 'x': ang[0], 'y': ang[1], 'z': ang[2]}
        out.append(ne)
    return out


def _retex(els):
    """the Sovereign's texture names (ds_) to this module's (uc_)"""
    for e in els:
        for f in e['faces'].values():
            if f['texture'].startswith('#ds_'): f['texture'] = '#uc_' + f['texture'][4:]
    return els


def _ds_head(face=None):
    import dread_sovereign_art as DS
    DS._PV[0] = DS.PIVOT['head']; DS._rs.seed(11)
    return [dict(e, faces={k: dict(v) for k, v in e['faces'].items()}) for e in DS._head0('armored', face)]


def _ds_weapon():
    import dread_sovereign_art as DS
    DS._PV[0] = DS.PIVOT['weapon']; DS._rs.seed(12)
    return [dict(e, faces={k: dict(v) for k, v in e['faces'].items()}) for e in DS._weapon('armored')]


I3 = [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]


def _rz(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1.0]]


def _mm(A, Bm):
    return [[sum(A[i][k] * Bm[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _mv(A, v):
    return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]


# ---- the Crown Shards
def _shard(kind):
    """a spike of the black crown, broken off at its root: a tapering blade of horn bent a little, a lesser spike off its side,
    a jagged stump; the red veins down both faces glow"""
    glass = kind == 'witch'
    body = 'uc_kglass' if glass else 'uc_horn'
    E = []
    E += CH([(8.0, 1.2, 8.0), (7.4, 5.6, 8.0), (8.3, 10.2, 8.0), (9.3, 13.6, 8.0), (9.9, 15.8, 8.0)], [5.4, 4.2, 2.8, 1.2], [3.0, 2.6, 2.0, 1.0], body)
    E += CH([(6.6, 3.4, 8.0), (4.0, 7.4, 8.2), (2.8, 10.8, 8.3)], [2.6, 1.2], [1.8, 1.0], body)
    E += CH([(9.6, 2.6, 8.0), (12.4, 5.6, 7.8), (13.2, 7.8, 7.8)], [2.0, 0.9], [1.5, 0.8], body)
    E += [B((5.4, 0.2, 6.4), (10.6, 2.4, 9.6), body, rot=('y', 18, (8, 1.3, 8))),
          B((6.0, 0.0, 7.0), (8.6, 1.4, 9.8), body, rot=('z', 12, (7, 0.7, 8))), B((8.8, 0.3, 6.6), (10.8, 1.6, 8.6), body, rot=('x', -14, (9.8, 1, 7.6)))]
    for z, s in ((6.4, -1), (9.6, 1)):                                          # (the veins: down its faces, branching)
        E += CH([(8.0, 1.8, z), (7.5, 5.6, z + 0.05 * s), (8.3, 9.8, z + 0.3 * s), (9.0, 12.6, z + 0.5 * s)], [0.7, 0.6, 0.5], [0.2, 0.2, 0.2], 'uc_red', light=15)
        E += CH([(7.6, 5.2, z + 0.05 * s), (5.2, 7.6, z + 0.2 * s)], [0.5], [0.2], 'uc_red', light=15)
        E += CH([(8.1, 8.0, z + 0.2 * s), (10.2, 6.2, z + 0.2 * s)], [0.45], [0.2], 'uc_red', light=15)
    E.append(B((5.6, 2.4, 6.5), (10.4, 2.8, 9.5), 'uc_red_l', light=15))       # (its broken root glowing)
    if kind == 'snow':                                                          # FEAR: rime along its edges, icicles off the side spike
        E += [B((4.9, 3.6, 6.3), (6.2, 8.4, 9.7), 'uc_frost', rot=('z', -8, (5.5, 6, 8))), B((8.8, 8.6, 6.8), (10.2, 13.4, 9.2), 'uc_frost', rot=('z', -20, (9.5, 11, 8))),
              B((2.0, 10.0, 7.2), (3.8, 11.8, 9.4), 'uc_frost'), B((4.6, 2.2, 6.0), (11.4, 3.2, 10.0), 'uc_frost', rot=('y', 18, (8, 2.7, 8))),
              B((9.0, 14.4, 7.2), (10.6, 15.6, 8.8), 'uc_frost'), B((12.4, 6.6, 7.0), (13.8, 8.2, 8.6), 'uc_frost')]
        for x, y, ln in ((4.2, 7.6, 3.0), (5.4, 6.4, 2.0), (11.6, 4.6, 2.6), (12.8, 6.8, 1.8)):
            E += CH([(x, y, 8.0), (x + 0.1, y - ln, 8.0)], [0.8], [0.8], 'uc_ice', light=4)
    elif kind == 'witch':                                                       # HUNGER: an eye open in the black glass
        E.append(B((5.4, 4.6, 5.9), (9.8, 8.0, 10.1), 'uc_geye', light=15, uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]},
                   faces=('north', 'south', 'east', 'west', 'up', 'down')))
        for x, y in ((11.4, 9.0), (3.8, 4.6), (12.0, 12.4)):
            E.append(B((x - 0.35, y - 0.35, 7.65), (x + 0.35, y + 0.35, 8.35), 'uc_gmote', light=15))
    else:                                                                       # WAR: salt crusting its lower half, a gold band
        E += [B((5.0, 1.6, 6.2), (8.2, 5.2, 9.8), 'uc_salt', rot=('z', 10, (6.6, 3.4, 8))), B((8.2, 2.2, 6.4), (11.0, 4.4, 9.6), 'uc_salt'),
              B((2.4, 9.2, 7.3), (4.2, 11.2, 9.3), 'uc_salt'), B((6.2, 6.8, 6.5), (8.4, 8.2, 9.5), 'uc_salt'), B((11.4, 4.6, 7.0), (13.0, 6.2, 8.8), 'uc_salt')]
        E += [B((5.8, 9.2, 6.2), (10.8, 10.6, 9.8), 'uc_gold', rot=('z', -12, (8.3, 9.9, 8))), B((7.4, 9.0, 6.0), (9.0, 10.8, 6.3), 'uc_gold', light=6)]
        for x, y in ((9.8, 3.2), (4.8, 6.6), (11.2, 7.0), (8.8, 12.4)):
            E.append(B((x - 0.4, y - 0.4, 6.2), (x + 0.4, y + 0.4, 9.8), 'uc_gold'))
    return E


def _ember():
    """a lump of dark coal, its core red-hot, glowing out through the cracks between its pieces; sparks above"""
    E = [GEM((8.0, 6.6, 8.0), 5.7, 'uc_red_l', light=15, rot=(30.0, 40.0, 10.0))]
    E += [B((4.4, 3.0, 4.8), (10.8, 8.4, 11.0), 'uc_coal', rot=((0.0, 22.0, 0.0), (8, 6, 8))),
          B((5.6, 2.6, 4.0), (12.0, 7.2, 10.2), 'uc_coal', rot=((8.0, -18.0, 6.0), (8, 5, 7))),
          B((5.0, 6.2, 5.8), (10.2, 10.0, 10.6), 'uc_coal', rot=((-10.0, 40.0, 8.0), (7.6, 8, 8))),
          B((3.6, 2.4, 6.8), (7.4, 6.4, 11.4), 'uc_coal', rot=((6.0, -30.0, -8.0), (5.4, 4.4, 9)))]
    for (x, y, z, s) in ((9.6, 11.6, 7.6, 0.6), (6.6, 12.8, 8.6, 0.45), (8.4, 14.0, 8.0, 0.35)):
        E.append(B((x - s, y - s, z - s), (x + s, y + s, z + s), 'uc_red_l', light=15, shift=False))
    return E


def _heart():
    """the heart crystal on its point, smaller ones round its foot, dark glass veins wrapping it"""
    E = [GEM((8.0, 8.6, 8.0), 6.6, 'uc_heart'), GEM((8.0, 8.6, 8.0), 3.4, 'uc_red_l', rot=(0.0, 45.0, 45.0))]
    for (x, y, z, s, r) in ((4.6, 3.6, 7.0, 2.2, (20.0, 10.0, 30.0)), (11.0, 3.4, 9.0, 1.8, (10.0, 50.0, -20.0)), (8.6, 2.6, 4.8, 1.6, (40.0, 20.0, 10.0))):
        E.append(GEM((x, y, z), s, 'uc_heart', rot=r))
    E += CH([(4.4, 10.4, 6.0), (6.6, 13.4, 7.0), (9.4, 14.0, 7.6)], [0.6, 0.5], [0.6, 0.5], 'uc_glass')
    E += CH([(11.6, 7.0, 9.6), (12.0, 10.6, 8.8)], [0.6], [0.6], 'uc_glass')
    return E


def _edge():
    """the Sovereign's greatsword (its weapon part as built for the rig), blade up, laid on a vanilla sword sprite's diagonal:
    grip at the lower left, tip at the upper right; about 1.5 vanilla swords long"""
    import dread_sovereign_art as DS
    X, Y, Z = DS.PIVOT['weapon']
    s = 0.8
    M = [[0, 1.0, 0], [0, 0, -1.0], [-1.0, 0, 0]]                             # (its -z (the blade) up, its y (the edges) across, x through)
    G = _mm(_rz(-45), M)
    grip = (4.4, 4.4, 8.0)
    def fpt(c):
        m = _mv(M, [c[i] - (8 if i else 8) for i in range(3)])                 # (model -> about the grip, the joint at 8,8,8)
        r = _mv(_rz(-45), m)
        return [grip[i] + r[i] * s for i in range(3)]
    return _retex(reframe(_ds_weapon(), fpt, G, s))


HELM_S = 11.2 / 8.4                                                            # (the Sovereign's hood, 8.4 wide, to the Visage's 11.2)


def _crown():
    """the Sovereign's crowned helm, the burning slit and all, at the Visage's size: the hood filling 2.4..13.6 round a head
    in 3..13, the horns and the crown above"""
    import dread_sovereign_art as DS
    hp = DS.PIVOT['head']
    def fpt(c):
        d = [c[i] - 8 + hp[i] for i in range(3)]                               # (model -> the Sovereign's design units)
        return [8 + d[0] * HELM_S, 2.4 + (d[1] - 33.0) * HELM_S, 8 + (d[2] + 0.2) * HELM_S]
    return _retex(reframe(_ds_head(), fpt, I3, HELM_S))


def _unbound_helm():
    """a great-helm of dark steel: a flat-topped bucket, a ridge over its crown, a cross of eye slit and nasal, breaths
    punched below, rivets; a broken chain hanging off its left side"""
    E = [B((2.6, 2.4, 2.6), (13.4, 13.2, 13.4), 'uc_steel'), B((3.2, 13.2, 3.2), (12.8, 14.0, 12.8), 'uc_steel_l'),
         B((7.3, 13.2, 2.4), (8.7, 14.8, 13.4), 'uc_steel_l'),                  # (the crest ridge)
         B((2.4, 8.6, 2.2), (13.6, 9.6, 2.6), 'uc_steel_l'),                     # (the brow band)
         B((2.4, 2.2, 2.3), (13.6, 3.0, 13.7), 'uc_steel_l'),                    # (the rim)
         B((3.0, 7.0, 2.25), (13.0, 8.0, 2.6), 'uc_slit', faces=('north',)),     # (the eye slit)
         B((7.4, 3.4, 2.0), (8.6, 8.6, 2.6), 'uc_steel_l')]                      # (the nasal)
    for x in (4.0, 5.4, 10.0, 11.4):                                            # (breaths)
        for y in (4.0, 5.4):
            E.append(B((x, y, 2.25), (x + 0.7, y + 0.5, 2.6), 'uc_slit', faces=('north',)))
    for (x, y, z) in ((3.0, 11.2, 2.2), (13.0, 11.2, 2.2), (2.2, 11.2, 8.0), (13.8, 11.2, 8.0), (8.0, 11.2, 13.8)):
        E.append(B((x - 0.4, y - 0.4, z - 0.4), (x + 0.4, y + 0.4, z + 0.4), 'uc_steel_l', shift=False))
    E.append(B((1.8, 8.6, 6.6), (2.6, 10.6, 9.4), 'uc_iron'))                  # (a shackle on its left side, the chain broken off it)
    pts = [(2.0, 8.6, 8.0), (1.6, 6.4, 8.3), (1.4, 4.2, 8.0), (1.2, 2.2, 7.8)]
    for i in range(len(pts) - 1):
        E.append(S(pts[i], pts[i + 1], 0.9, 0.3, 'uc_chain', up=(0.0, 0.0, 1.0) if i % 2 else (1.0, 0.0, 0.0)))
    E.append(S((1.2, 2.2, 7.8), (1.5, 1.0, 7.6), 0.9, 0.3, 'uc_chain', up=(1.0, 0.0, 0.0)))
    return E


def _wall_eye(open_):
    """an almond of dark flesh set in folds (rows of boxes, so it is round at the ends), its front the model's north face:
    shut - the lids met and bulging, a black seam, red lashes over it; open - the lids drawn back, the eye in rows showing one
    painted eye between them"""
    E = []; X0, X1, Y0, Y1 = 0.6, 15.4, 3.0, 13.0
    def half(y, grow=0.0):                                                      # (an almond: pointed at its corners, round above and below)
        t = abs(y - 8.0) / (5.0 + grow)
        return 0.0 if t >= 1 else (7.4 + grow) * (1 - t ** 1.4) ** 0.6
    for y in [Y0 - 1.6 + 0.8 * i for i in range(17)]:                          # (the folds round it)
        w = half(y + 0.4, 1.6)
        if w > 0.3: E.append(B((8 - w, y, 5.0), (8 + w, y + 0.8, 8.0), 'uc_fold'))
    rows = [Y0 + i * 0.5 for i in range(20)]
    for y in rows:
        w = half(y + 0.25)
        if w < 0.3: continue
        if not open_:                                                           # (the lids, bulging most at the middle)
            z = 2.6 + 1.6 * ((y + 0.25 - 8.0) / 5.0) ** 2
            E.append(B((8 - w, y, z), (8 + w, y + 0.5, 6.0), 'uc_flesh'))
        else:
            up, lo = y >= 10.6, y < 4.8
            if up or lo:                                                        # (the lids, drawn back)
                z = 3.0 + 0.8 * ((y + 0.25 - 8.0) / 5.0) ** 2
                E.append(B((8 - w, y, z), (8 + w, y + 0.5, 6.0), 'uc_flesh'))
            else:                                                               # (the eye: each row its own window of the one picture)
                xa, xb = 8 - w, 8 + w; ya, yb = y, y + 0.5
                u1, u2 = (X1 - xb) / (X1 - X0) * 16, (X1 - xa) / (X1 - X0) * 16
                v1, v2 = (10.6 - yb) / (10.6 - 4.8) * 16, (10.6 - ya) / (10.6 - 4.8) * 16
                v1, v2 = max(0.0, v1), min(16.0, v2)                                # (the top row overhangs the picture a little)
                z = 3.2 + 0.9 * ((y + 0.25 - 7.7) / 3.0) ** 2
                E.append(el((xa, ya, z), (xb, yb, 6.0), 'uc_weye', PIV, uv={'north': [round(u1, 3), round(v1, 3), round(u2, 3), round(v2, 3)]},
                            faces=('north',), light=10))
                E.append(B((xa, ya, z + 0.05), (xb, yb, 6.0), 'uc_flesh', faces=('east', 'west', 'up', 'down')))
    if not open_:
        E.append(B((1.6, 7.85, 2.5), (14.4, 8.25, 2.7), 'uc_seam'))
        for i in range(11):                                                     # (lashes, from the seam down over the lower lid)
            x = 2.6 + i * 1.08; a = (i - 5) * 6
            E.append(B((x - 0.18, 6.2, 2.45), (x + 0.18, 8.0, 2.75), 'uc_lash', light=10, rot=('z', a, (x, 8.0, 2.6)), shift=False))
    else:
        for i in range(9):                                                      # (lashes, standing off the upper lid's edge)
            x = 3.2 + i * 1.2; a = (i - 4) * 9
            E.append(B((x - 0.18, 10.4, 2.9), (x + 0.18, 12.2, 3.2), 'uc_lash', light=10, rot=('z', a, (x, 10.6, 3.0)), shift=False))
    return E


def _trophy():
    """a bust of the armored Sovereign on a plinth: the plinth of void-plate with red seams, its chest and pauldrons, the
    crowned helm"""
    import dread_sovereign_art as DS
    hp = DS.PIVOT['head']; k = 0.62
    def fpt(c):
        d = [c[i] - 8 + hp[i] for i in range(3)]
        return [8 + d[0] * k, 7.6 + (d[1] - 33.0) * k, 8 + (d[2] + 0.2) * k]
    E = [B((2.0, 0.0, 2.0), (14.0, 1.6, 14.0), 'uc_stone'), B((3.0, 1.6, 3.0), (13.0, 3.4, 13.0), 'uc_stone'),
         B((2.4, 1.5, 2.4), (13.6, 1.75, 13.6), 'uc_red', light=12)]
    E += [B((3.6, 3.4, 5.2), (12.4, 7.8, 10.8), 'uc_plate'), B((5.0, 3.6, 4.4), (11.0, 7.4, 5.2), 'uc_plate'),   # (the chest, its keel)
          B((7.4, 3.6, 4.0), (8.6, 7.6, 4.4), 'uc_edge'), GEM((8.0, 6.2, 4.0), 0.9, 'uc_heart', light=15, rot=(0.0, 0.0, 45.0)),
          B((5.6, 7.4, 5.6), (10.4, 8.2, 10.4), 'uc_dark')]
    for sx in (1, -1):                                                          # (pauldrons, a spike each)
        a, b = sorted((8 + sx * 3.4, 8 + sx * 6.8))
        E += [B((a, 5.4, 4.8), (b, 8.0, 11.2), 'uc_plate'), B((a + 0.3, 8.0, 5.4), (b - 0.3, 8.5, 10.6), 'uc_edge')]
        E += CH([(8 + sx * 5.6, 8.4, 8.0), (8 + sx * 6.4, 10.4, 8.0), (8 + sx * 6.9, 11.8, 8.0)], [1.0, 0.5], [1.0, 0.5], 'uc_horn', light=12,
                texs=['uc_horn', 'uc_horn_r'])
    E += _retex(reframe(_ds_head(), fpt, I3, k))
    return E


def models():
    tex_extra = {}
    M = {}
    for k in ('snow', 'witch', 'shark'): M[f'ushard_{k}'] = _shard(k)
    M['dread_ember'] = _ember(); M['sov_heart'] = _heart(); M['sov_edge'] = _edge(); M['black_crown'] = _crown()
    M['unbound_helm'] = _unbound_helm(); M['ueye_shut'] = _wall_eye(False); M['ueye_open'] = _wall_eye(True); M['sov_trophy'] = _trophy()
    for name, els in M.items():
        for e in els:
            for v in e['from'] + e['to']: assert -16 <= v <= 32, (name, e)
    return M


# ---- display transforms
GUI3 = {'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.62, 0.62, 0.62]},
        'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.4, 0.4, 0.4]},
        'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.7, 0.7, 0.7]},
        'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 1.5, 0], 'scale': [0.35, 0.35, 0.35]},
        'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 1, 0], 'scale': [0.4, 0.4, 0.4]},
        'head': {'rotation': [0, 0, 0], 'translation': [0, 8, 0], 'scale': [0.6, 0.6, 0.6]}}
HANDHELD_DISP = {                                                               # (vanilla item/handheld's, for a sword on its diagonal)
    'thirdperson_righthand': {'rotation': [0, -90, 55], 'translation': [0, 4.0, 0.5], 'scale': [0.85, 0.85, 0.85]},
    'thirdperson_lefthand': {'rotation': [0, 90, -55], 'translation': [0, 4.0, 0.5], 'scale': [0.85, 0.85, 0.85]},
    'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
    'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
    'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.62, 0.62, 0.62]},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.4, 0.4, 0.4]},
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.8, 0.8, 0.8]}}
HEAD_DISP = {                                                                   # (as the Dread Visage: drawn for a head in 3..13, worn 1.28 times over)
    'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.28, 1.28, 1.28]},
    'gui': {'rotation': [25, 200, 0], 'translation': [0, -3.5, 0], 'scale': [0.5, 0.5, 0.5]},
    'ground': {'rotation': [0, 0, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]},
    'fixed': {'rotation': [0, 180, 0], 'translation': [0, -3, 0], 'scale': [0.55, 0.55, 0.55]},
    'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 1, 0], 'scale': [0.3, 0.3, 0.3]},
    'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.35, 0.35, 0.35]}}
EYE_DISP = {'gui': {'rotation': [0, 180, 0], 'translation': [0, 0, 0], 'scale': [0.9, 0.9, 0.9]},
            'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]}}
TROPHY_DISP = {'gui': {'rotation': [20, 200, 0], 'translation': [0, -2.5, 0], 'scale': [0.55, 0.55, 0.55]},
               'ground': {'rotation': [0, 0, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]},
               'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
               'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 1, 0], 'scale': [0.3, 0.3, 0.3]},
               'firstperson_righthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.35, 0.35, 0.35]}}
GUI_BIG = dict(GUI3, gui={'rotation': [15, 200, 0], 'translation': [0, 0, 0], 'scale': [0.85, 0.85, 0.85]})
HELM_DISP2 = dict(HEAD_DISP, gui={'rotation': [25, 200, 0], 'translation': [0, -1, 0], 'scale': [0.72, 0.72, 0.72]})
GUI_GEM = dict(GUI3, gui={'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.8, 0.8, 0.8]})
DISP = {'ushard_snow': GUI_BIG, 'ushard_witch': GUI_BIG, 'ushard_shark': GUI_BIG, 'dread_ember': GUI_GEM, 'sov_heart': GUI_GEM,
        'sov_edge': HANDHELD_DISP, 'black_crown': HEAD_DISP, 'unbound_helm': HELM_DISP2, 'ueye_shut': EYE_DISP, 'ueye_open': EYE_DISP,
        'sov_trophy': TROPHY_DISP}


def model_json(name, els):
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    t = {u: f'bm:block/{u}' for u in used}; t['particle'] = t[used[0]]
    return {'textures': t, 'elements': els, 'display': DISP.get(name, GUI3)}


# ==================================================================================================== the pack
def rp(R):
    """gen_rp: the flat icons through ICONS (the chain whip held as a tool), the uc_ textures through TEXTURE_MODS, and the 3D
    models with their item definitions written in a post pass"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS.update(icons())
    R.HANDHELD_EXTRA.update(HANDHELD)
    def post(R2):
        for name, els in models().items():
            R2.wj(f'assets/bm/models/item/{name}.json', model_json(name, els))
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
    R.POST.append(post)
