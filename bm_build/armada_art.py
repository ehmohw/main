"""2.99: THE VORN ARMADA's item art - every model its items name (p2/armadaitems.py; the looks from armada_lore.py and
previews/v299_armada/PLAN.md), the Admiral's shield pylons (phase242) and the Starforged set's worn plate. gen_rp calls rp(R).

PALETTE: gunmetal, the hive's green, the Vorn's war-red, the Hive-Star's orange and its white heat (the Starforged gold-orange
#ffb14a among them); Donadian teal only on the Donadian things (Zib's squad jetpack).

FLAT ICONS (16 x 16, the pack's vanilla look - through R.ICONS, so vanilla.process gives them its outline pass):
  hive_coords    the Hive-Star Coordinates: a dark slate tablet, a red star in the middle, two orbit rings round it, a green
                 blip on the outer one (a world: yours), green glyphs along its edges
  cipher_1/2/3   the Command Ciphers: a gunmetal hexagonal data-slug, its core lit, I / II / III cut below - I bio-green (green
                 growth creeping over it, a pustule of a core); II forged red-hot (its rim and cracks glowing red and orange);
                 III the Star-Seer's eye (a violet eye open in it, watching)
  hive_sigil     a small medallion: a gunmetal rim, the hive's glyph (a hexagon, three spurs) in green on its dark face, a loop
  akey           an Armada Key: vanilla's trial key in gunmetal, its eyes green, a green line down its shank
  akey_victor    the Victor's Key: the ominous trial key, darker, its reds turned to green burning
  star_core      a sliver of the Hive-Star - white at its heart, orange out to its edges - held in a gunmetal cage, glowing
  squad_jetpack  Zib's squad jetpack: two Donadian-teal tanks on a harness, a light on it, two thrusters with a flame each
  hover_collar   Specimen 117's collar: a worn leather dog collar (stitched, scuffed, a brass buckle), a little hover-disc tag
                 hanging off it, green light under the disc
  hive_override  a green circuit chip (traces, pins, a dark die with a green eye of light), a red wire off it, cut, sparking
  stardust_kite  a small pale-blue kite on its spars, a tail of little stars and bows
  vexis_link     the Severed Link: a hive-link cable coiled in a ring, its green core showing between the segments; one end
                 cut, frayed, sparking green
  starforged_helmet / _chestplate / _leggings / _boots   the Warplate pieces (vanilla's netherite shapes) reforged: gunmetal
                 plate, gold-orange seams, star-orange cores glowing (the helm's eye slit, the breast's core, the belt's
                 buckle and knees, the thrusters' nozzles)
  singularity_launcher (+ _pull0/_pull1/_pull2/_charged)   a crossbow (vanilla's sprites): its stock gunmetal, its limbs
                 violet, its string a green energy filament; loaded, a violet singularity - a small hungry star - on the bolt.
                 Drawn as vanilla's crossbow is (parent minecraft:item/crossbow) and chosen as vanilla's item definition
                 chooses: charge_type, then using_item and crossbow/pull (written in rp's post pass)
3D MODELS (block textures am_*, written in rp's post pass):
  starfire_lance a long lance of cooled star: a gunmetal haft, a wrapped grip, red hive bands, a rondel; its head a blade of
                 the star (orange-white, emissive), flames licking off it - laid on a vanilla sword sprite's diagonal (held near
                 the butt), so vanilla's handheld transforms hold it right
  hive_breaker   a heavy Vorn axe: a dark haft, a gunmetal head, a crescent blade with red chevrons on both faces and a green
                 energy edge (emissive), a back spike - on the diagonal, its blade forward (top left) as a vanilla axe's
  admiral_crown  a crown of Vorn antennae: a gunmetal band, red-trimmed, round a head in 3..13; a plaque at its front set with
                 a green gem; six antennae curling up and back, their tips lit green - worn as black_crown is (1.28 times)
  vx_pylon       the shield pylon: a tall hexagonal crystal of green light (emissive) on a gunmetal collar, red lights round it,
                 clamps holding it, two shards hanging by it
  vx_pylon_off   the same overloaded: the crystal dark and cracked, its tip broken off, the lights dead, smoke rising off it
                 (both item models only: an item_display shows them, context none)
EQUIPMENT: bm:starforged (humanoid + humanoid_leggings): the netherite plate in gunmetal, its seams gold-orange, a star core
  glowing in the breast, the brow and the belt."""
import math
import random
from PIL import Image, ImageDraw

from rigkit import el, seg
from undercrown_art import Px, ramp, _c, _cells, _veins, reframe, _rz, _mv, I3, HANDHELD_DISP, HEAD_DISP

PIV = (8.0, 8.0, 8.0)
FRONT = (0.0, 0.0, -1.0)
VAN = '/home/claude/mc263/client/assets/minecraft/textures/'


def H(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


GM = [H(c) for c in ('#2a2e36', '#444a56', '#646c7a', '#8a94a2', '#b4bcc8')]
GN = [H(c) for c in ('#0e5a1e', '#1e8a2e', '#3ac84a', '#7aff6a', '#d8ffc8')]
RED, RED_L, RED_D = H('#d83030'), H('#ff4a4a'), (110, 16, 22)
STAR, SF, WHITE = H('#ff8a3a'), H('#ffb14a'), H('#fff0c8')
TEAL = H('#3ad8c8')
VI = [(40, 14, 70), (86, 40, 140), (140, 80, 220), (192, 138, 255), (236, 214, 255)]
INK = (12, 14, 18)
GUN = ramp([(0.0, (16, 18, 22)), (0.2, GM[0]), (0.42, GM[1]), (0.64, GM[2]), (0.84, GM[3]), (1.0, GM[4])])
GUN_DK = ramp([(0.0, (8, 9, 12)), (0.35, (22, 25, 30)), (0.7, GM[0]), (1.0, GM[2])])
FLAT = ('hive_coords', 'cipher_1', 'cipher_2', 'cipher_3', 'hive_sigil', 'akey', 'akey_victor', 'star_core', 'squad_jetpack',
        'hover_collar', 'hive_override', 'stardust_kite', 'vexis_link', 'starforged_helmet', 'starforged_chestplate',
        'starforged_leggings', 'starforged_boots')
LAUNCHER = ('singularity_launcher', 'singularity_launcher_pull0', 'singularity_launcher_pull1', 'singularity_launcher_pull2',
            'singularity_launcher_charged')
MODELS3D = ('starfire_lance', 'hive_breaker', 'admiral_crown', 'vx_pylon', 'vx_pylon_off')
CHARGE_SELECT = True          # (the launcher's item definition picks its loaded look by minecraft:charge_type, as vanilla's does)


def _lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def _P(im):
    P = Px(); P.im = im; P.px = im.load(); return P


# ==================================================================================================== flat icons
def hive_coords():
    """a dark slate tablet: a red star in its middle, an orbit round it, a green blip on the orbit, green glyphs"""
    P = Px()
    for y in range(2, 14):
        for x in range(1, 15):
            if (x in (1, 14)) and (y in (2, 13)): continue
            P.p(x, y, GUN_DK(0.42 - (x + y - 15) * 0.012))
    for x in range(2, 14): P.p(x, 2, GM[1]); P.p(x, 13, (14, 16, 20))         # (a lit top edge, a lit left side)
    for y in range(3, 13): P.p(1, y, GM[1])
    orbit = [(3, 6), (4, 5), (5, 5), (6, 4), (7, 4), (8, 4), (9, 4), (10, 5), (11, 5), (12, 6), (12, 7), (12, 8), (11, 9), (10, 9),
             (9, 10), (8, 10), (7, 10), (6, 10), (5, 9), (4, 9), (3, 8), (3, 7)]
    for x, y in orbit: P.p(x, y, GM[2])
    for x, y, c in ((7, 6, RED_D), (8, 6, RED_D), (6, 7, RED_D), (9, 7, RED), (6, 8, RED_D), (9, 8, RED_D), (7, 9, RED_D), (8, 9, RED_D),
                    (7, 7, WHITE), (8, 7, RED_L), (7, 8, RED_L), (8, 8, RED)):
        P.p(x, y, c)                                                            # (the Hive-Star)
    P.p(11, 9, GN[3]); P.p(12, 9, GN[2])                                        # (a world on its orbit: yours)
    P.p(4, 5, GM[4])                                                            # (another, already taken)
    for x in (3, 4, 6, 9, 10, 12): P.p(x, 12, GN[2] if x % 3 else GN[3])        # (glyphs, along its foot and its head)
    for x in (3, 5, 6, 10, 11): P.p(x, 3, GN[1])
    P.outline()
    return P.im


def _hex_mask():
    """a pointy-topped hexagon, 14 wide and 14 tall: its slanting edges two pixels across for each one down"""
    rows = {1: (6, 9), 2: (4, 11), 3: (2, 13), 12: (2, 13), 13: (4, 11), 14: (6, 9)}
    out = {}
    for y in range(1, 15):
        a, b = rows.get(y, (1, 14))
        for x in range(a, b + 1): out[(x, y)] = (abs(x - 7.5), abs(y - 7.5))
    return out


def _cipher_base():
    P = Px(); m = _hex_mask()
    for (x, y), (dx, dy) in m.items():
        rim = not all((x + a, y + b) in m for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        t = 0.5 - (x - 7.5) * 0.03 - (y - 7.5) * 0.035
        P.p(x, y, GUN(t + 0.22) if rim else GUN(t - 0.08))
    for (x, y) in m:                                                            # (an inner bevel: lit on the upper left)
        if (x + 1, y + 1) not in m or (x + 2, y + 2) not in m: continue
        if (x - 1, y - 1) in m and (x - 2, y - 2) not in m: P.p(x, y, GM[3])
        elif (x + 2, y + 2) in m and (x + 3, y + 3) not in m: P.p(x, y, GM[0])
    return P, m


def _core(P, col, cy=6):
    lo, mid, hi, hot = col
    for x, y in ((6, cy - 1), (7, cy - 2), (8, cy - 2), (9, cy - 1), (6, cy + 2), (9, cy + 2), (7, cy + 3), (8, cy + 3),
                 (5, cy), (5, cy + 1), (10, cy), (10, cy + 1)):
        P.p(x, y, INK)                                                          # (its socket)
    for y in range(cy - 1, cy + 3):
        for x in range(6, 10):
            if (x, y) in ((6, cy - 1), (9, cy - 1), (6, cy + 2), (9, cy + 2)): continue
            P.p(x, y, mid)
    for x in range(6, 10):
        if 7 <= x <= 8: P.p(x, cy - 1, mid)
    for x, y in ((7, cy - 1), (8, cy - 1), (6, cy), (6, cy + 1), (9, cy), (9, cy + 1), (7, cy + 2), (8, cy + 2)):
        P.p(x, y, mid)
    for x, y in ((7, cy), (8, cy), (7, cy + 1)): P.p(x, y, hi)
    P.p(7, cy, hot); P.p(8, cy + 1, lo); P.p(9, cy + 1, lo); P.p(8, cy + 2, lo)


def _marks(P, n, col, y0=11):
    xs = {1: (7,), 2: (6, 9), 3: (5, 7, 10)}[n]
    for x in xs:
        for y in (y0, y0 + 1):
            P.p(x, y, col); P.p(x + 1, y, GM[0])


def cipher(k):
    P, m = _cipher_base()
    if k == 1:                                                                  # I: the Brood-Warden's - green growth over the slug
        _core(P, (GN[0], GN[2], GN[3], GN[4]))
        for x, y in ((2, 9), (3, 9), (3, 10), (4, 11), (2, 8), (3, 4), (2, 5), (12, 4), (13, 5), (13, 6), (12, 12), (11, 13),
                     (10, 13), (4, 3), (5, 2), (13, 10)):
            if (x, y) in m: P.p(x, y, GN[1])
        for x, y in ((3, 9), (12, 5), (11, 13), (4, 3)): P.p(x, y, GN[2])
        P.p(2, 9, GN[3]); P.p(13, 5, GN[3])
        _marks(P, 1, GN[3])
    elif k == 2:                                                                # II: the Forgemaster's - forged into it, still red-hot
        for (x, y), (dx, dy) in m.items():
            rim = not all((x + a, y + b) in m for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if rim and y >= 8: P.p(x, y, RED if y < 12 else STAR)
            if rim and y >= 13: P.p(x, y, SF)
        _core(P, (GN[0], GN[2], GN[3], GN[4]))
        for x, y, c in ((3, 6, RED_D), (4, 7, RED), (3, 8, RED), (12, 8, RED_D), (11, 9, RED), (12, 10, RED), (5, 13, RED_D)):
            P.p(x, y, c)
        _marks(P, 2, STAR)
    else:                                                                       # III: the Star-Seer's - a violet eye, watching
        eye = ['..KKKKKK..', '.KWVVVVWK.', 'KWWVPPVWWK', 'KWWVPPVWWK', '.KWVVVVWK.', '..KKKKKK..']
        pal = {'K': INK, 'W': (214, 208, 226), 'V': VI[2], 'P': (8, 4, 14)}
        for j, row in enumerate(eye):
            for i, ch in enumerate(row):
                if ch != '.': P.p(3 + i, 3 + j, pal[ch])
        P.p(6, 5, VI[4]); P.p(7, 4, VI[3]); P.p(8, 7, VI[1])
        _marks(P, 3, VI[3])
    P.outline()
    return P.im


def hive_sigil():
    """a small medallion: a gunmetal rim, the hive's glyph in green on its dark face, a loop at its top"""
    P = Px(); cx, cy = 7.5, 8.5
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - cx, y - cy)
            if d <= 5.4:
                if d > 4.2: P.p(x, y, GUN(0.75 - (x + y - 16) * 0.05))
                else: P.p(x, y, GUN_DK(0.5 - (x + y - 16) * 0.03))
    for x, y in ((7, 2), (8, 2), (6, 1), (9, 1), (7, 0), (8, 0)):                # (the loop)
        P.p(x, y, GM[3] if y < 2 else GM[2])
    glyph = ['..GG..', '.G..G.', 'G.LL.G', 'G.LL.G', '.G..G.', '..GG..']
    for j, row in enumerate(glyph):
        for i, ch in enumerate(row):
            if ch != '.': P.p(5 + i, 6 + j - 0, GN[2] if ch == 'G' else GN[4])
    for x, y in ((7, 5), (8, 5), (4, 12), (11, 12)):                            # (its three spurs: up, and down to each side)
        P.p(x, y, GN[1])
    P.p(5, 11, GN[1]); P.p(10, 11, GN[1])
    P.p(4, 5, GM[4]); P.p(5, 4, GM[3])
    P.outline()
    return P.im


def _recolor_key(src, rmp, keep_red=None):
    im = Image.open(VAN + 'item/' + src).convert('RGBA'); px = im.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if not a: continue
            if keep_red and r > g + 40 and r > b + 30:                         # (the ominous key's reds: turned to green fire)
                px[x, y] = _c(GN[3] if r > 200 else GN[2]); continue
            if r > g + 40 and r > 200 and y < 6:                                # (the trial key's orange eyes: green)
                px[x, y] = _c(GN[3]); continue
            px[x, y] = _c(rmp((0.299 * r + 0.587 * g + 0.114 * b) / 190))
    return im


def akey():
    im = _recolor_key('trial_key.png', GUN); P = _P(im)
    P.p(6, 3, GN[3]); P.p(9, 3, GN[3]); P.p(6, 4, GN[1]); P.p(9, 4, GN[1])
    for y in range(8, 14): P.p(7, y, GN[2] if y % 2 else GN[1])                  # (a green line down its shank)
    P.p(9, 12, GN[2]); P.p(10, 14, GN[1])
    return im


def akey_victor():
    im = _recolor_key('ominous_trial_key.png', GUN_DK, keep_red=True); P = _P(im)
    for x, y, c in ((6, 3, GN[4]), (9, 3, GN[4]), (6, 4, GN[2]), (9, 4, GN[2]), (7, 1, GN[1]), (8, 1, GN[1])):
        P.p(x, y, c)
    for y in range(9, 14): P.p(7, y, GN[3] if y % 2 else GN[2])                  # (green burning down its shank)
    P.p(8, 11, GN[1]); P.p(9, 12, GN[3]); P.p(10, 14, GN[2]); P.p(8, 14, GN[1])
    return im


def star_core():
    """the star's sliver: a long diamond, white at its heart, orange to its edges; a gunmetal cage round it, glowing out"""
    P = Px()
    halfw = {2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 9: 2, 10: 2, 11: 1, 12: 1, 13: 0}
    for y, w in halfw.items():
        for x in range(7 - w, 9 + w):
            d = abs(x - 7.5) / (w + 0.5)
            P.p(x, y, WHITE if d < 0.35 else (SF if d < 0.7 else STAR))
    for y in range(1, 15):                                                      # (the cage's bars: outside, and two in front)
        for x in (3, 12): P.p(x, y, GM[2] if x == 3 else GM[1])
    for y in (1, 14):
        for x in range(3, 13): P.p(x, y, GM[3] if y == 1 else GM[1])
    for x in range(4, 12): P.p(x, 2 if x not in (7, 8) else 2, GM[2]); P.p(x, 13, GM[0])
    for y in range(3, 13):
        P.p(5, y, GM[3] if y % 3 else GM[4]); P.p(10, y, GM[2])
    P.p(7, 0, GM[2]); P.p(8, 0, GM[2])                                          # (its ring, to hang it by)
    for x, y in ((4, 6), (4, 9), (11, 7), (11, 8), (4, 7), (11, 6)):            # (glow, between the bars)
        P.p(x, y, (255, 120, 40))
    for x, y in ((14, 4), (1, 11), (14, 12), (1, 3)):                           # (sparks)
        P.p(x, y, SF)
    P.outline((40, 20, 8))
    return P.im


def squad_jetpack():
    """two teal tanks on a harness, a light on it, two thrusters below, a flame from each"""
    P = Px()
    TL, T, TD, TS = (160, 252, 240), TEAL, (30, 148, 138), (18, 92, 88)
    for cx in (4, 10):                                                          # (the tanks: rounded tops, lit on their left)
        for y in range(2, 12):
            for x in range(cx - 1, cx + 3):
                if y == 2 and x in (cx - 1, cx + 2): continue
                c = TL if x == cx - 1 or (y == 2) else (T if x <= cx + 1 else TD)
                if x == cx and y == 3: c = (230, 255, 252)
                P.p(x, y, c)
        for x in range(cx - 1, cx + 3): P.p(x, 8, TS)                           # (a band round each tank)
    for y in range(4, 10):                                                      # (the harness between)
        for x in (7, 8): P.p(x, y, GM[1] if x == 8 else GM[2])
    P.p(7, 5, (255, 220, 80)); P.p(8, 5, (255, 180, 40))                        # (its light)
    for x in (7, 8): P.p(x, 3, GM[3])
    for cx in (4, 10):                                                          # (thrusters, a flame each)
        P.p(cx, 12, GM[1]); P.p(cx + 1, 12, GM[0]); P.p(cx - 1, 12, GM[2]); P.p(cx + 2, 12, GM[0])
        P.p(cx, 13, SF); P.p(cx + 1, 13, STAR); P.p(cx, 14, STAR); P.p(cx + 1, 14, (220, 80, 30)); P.p(cx, 15, (220, 80, 30))
    P.outline()
    return P.im


def hover_collar():
    """a worn leather collar seen from above and in front - stitched, scuffed, a brass buckle - and a hover-disc tag hanging"""
    P = Px()
    LD, LM, LL, ST = (82, 50, 24), (138, 88, 44), (176, 120, 64), (232, 206, 150)
    cx, cy = 7.5, 6.0
    for y in range(16):
        for x in range(16):
            e = ((x - cx) / 6.6) ** 2 + ((y - cy) / 4.4) ** 2
            if 0.48 <= e <= 1.0:
                front = y > cy
                P.p(x, y, LL if (front and e < 0.7) else (LM if front else LD))
    for i in range(36):                                                         # (the stitching, on its near side)
        a = i / 36 * math.tau
        x, y = round(cx + 5.4 * math.cos(a)), round(cy + 3.6 * math.sin(a))
        if y > cy + 1 and i % 2 == 0: P.p(x, y, ST)
    for x, y in ((10, 9), (11, 9)): P.p(x, y, LM)                               # (scuffs)
    for x, y, c in ((1, 5, (200, 168, 80)), (1, 6, (236, 210, 120)), (2, 5, (150, 120, 50)), (2, 6, (200, 168, 80)),
                    (1, 7, (150, 120, 50)), (0, 6, (120, 96, 40))):             # (a brass buckle)
        P.p(x, y, c)
    P.p(7, 10, GM[3]); P.p(8, 11, GM[2])                                        # (the tag's ring)
    for x in range(5, 11): P.p(x, 12, GM[3] if x < 8 else GM[2])                # (the hover-disc)
    for x in range(6, 10): P.p(x, 11, GM[4] if x < 8 else GM[3])
    P.p(7, 12, GN[3])
    for x in range(6, 10): P.p(x, 13, GN[2] if x in (7, 8) else GN[1])          # (green light under it)
    P.p(7, 14, GN[1]); P.p(8, 14, GN[1]); P.p(7, 15, GN[0])
    P.outline()
    return P.im


def hive_override():
    """a green circuit chip - traces, pins, a dark die with a green light - a red wire off it, cut, sparking"""
    P = Px()
    PCB, TR, PAD = GN[0], GN[1], GN[2]
    for y in range(2, 12):
        for x in range(1, 11): P.p(x, y, PCB)
    for x in range(1, 11): P.p(x, 2, GN[1])
    for x, y in ((2, 4), (3, 4), (4, 4), (2, 9), (3, 9), (8, 9), (9, 9), (9, 4), (9, 5), (2, 5), (2, 6), (9, 8), (8, 4)):
        P.p(x, y, TR)
    for y in range(5, 9):                                                       # (the die)
        for x in range(4, 8): P.p(x, y, GM[0] if (x + y) % 2 else GM[1])
    P.p(5, 6, GN[3]); P.p(6, 7, GN[2]); P.p(5, 7, GN[1])
    for i in range(2, 11, 2):                                                   # (pins)
        P.p(i, 1, GM[4]); P.p(i, 12, GM[3]); P.p(0, i + 1, GM[3])
    for x, y in ((3, 10), (8, 3)): P.p(x, y, PAD)
    for x, y in ((11, 7), (12, 7), (13, 8), (13, 9)):                           # (the red wire, cut)
        P.p(x, y, RED_L if y == 7 else RED)
    P.p(12, 8, RED_D); P.p(13, 10, (240, 200, 150))                             # (its copper, bared)
    for x, y in ((13, 13), (12, 14), (11, 14), (10, 14)): P.p(x, y, RED)        # (the other end, fallen)
    P.p(13, 12, (240, 200, 150))
    P.p(14, 11, (255, 252, 220)); P.p(15, 10, (255, 230, 120)); P.p(15, 12, (255, 230, 120))   # (sparks between)
    P.outline()
    return P.im


def stardust_kite():
    """a small pale-blue kite on its spars, a tail of stars and bows trailing down to the right"""
    P = Px()
    K1, K2, K3, SP = (191, 232, 255), (140, 196, 240), (230, 248, 255), (250, 252, 255)
    top, left, right, bot = (5, 0), (0, 5), (10, 4), (5, 11)
    for y in range(16):
        for x in range(16):
            def side(a, b): return (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])
            if side(top, right) >= 0 and side(right, bot) >= 0 and side(bot, left) >= 0 and side(left, top) >= 0:
                P.p(x, y, K3 if (x < 5 and y < 5) else (K1 if (x <= 5 or y <= 4) else K2))
    for i in range(11):                                                         # (the spars)
        x = round(top[0] + (bot[0] - top[0]) * i / 11); y = round(top[1] + (bot[1] - top[1]) * i / 11)
        P.p(x, y, (110, 160, 210))
    for i in range(11):
        x = round(left[0] + (right[0] - left[0]) * i / 10); y = round(left[1] + (right[1] - left[1]) * i / 10)
        P.p(x, y, (110, 160, 210))
    tail = [(6, 12), (7, 13), (8, 13), (9, 14), (10, 14), (11, 14), (12, 13), (13, 13), (14, 14), (15, 15)]
    for x, y in tail: P.p(x, y, (200, 210, 230))
    for x, y in ((8, 12), (8, 14), (12, 12), (12, 14)): P.p(x, y, (255, 150, 190))   # (two bows)
    for x, y in ((10, 14), (14, 14)): P.p(x, y, (255, 236, 140))                 # (stars along it, glittering off it)
    for x, y in ((10, 12), (15, 12), (2, 13)): P.p(x, y, WHITE)
    P.outline((30, 44, 70))
    return P.im


def vexis_link():
    """the hive-link cable coiled in a ring - gunmetal segments, its green core between - cut at the top right, frayed,
    sparking"""
    P = Px(); cx, cy = 7.5, 8.0
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - cx, y - cy); a = math.degrees(math.atan2(y - cy, x - cx)) % 360
            if 4.0 <= d <= 6.4 and not (292 <= a <= 334):
                seg_ = int(a / 26) % 2
                if 4.8 <= d <= 5.6: P.p(x, y, GN[2] if seg_ else GN[1])          # (the core: lit between the segments)
                else:
                    t = 0.55 - (x + y - 15) * 0.03
                    P.p(x, y, GUN(t + (0.18 if seg_ else 0.0)))
    for x, y, c in ((10, 3, GM[4]), (10, 4, GM[3])):                           # (one end: a clean cap)
        P.p(x, y, c)
    for x, y, c in ((12, 5, GN[2]), (13, 5, GM[3]), (13, 4, GN[3]), (14, 4, GM[2]), (12, 4, GM[2])):   # (the other: frayed wires)
        P.p(x, y, c)
    for x, y, c in ((15, 2, GN[4]), (14, 1, GN[3]), (12, 2, GN[3]), (15, 4, GN[2])):                     # (green sparks off them)
        P.p(x, y, c)
    P.outline()
    return P.im


# ---- the Starforged set's icons: vanilla's netherite pieces in gunmetal, gold-orange seams, star cores glowing
SF_PAINT = {
    'helmet': [((5, 7), STAR), ((6, 7), WHITE), ((9, 7), WHITE), ((10, 7), STAR), ((5, 8), (150, 50, 14)), ((6, 8), STAR),
               ((9, 8), STAR), ((10, 8), (150, 50, 14)), ((7, 4), SF), ((8, 4), SF), ((7, 5), STAR), ((8, 5), STAR), ((7, 6), SF), ((8, 6), SF),
               ((4, 9), SF), ((11, 9), SF)],
    'chestplate': [((7, 9), WHITE), ((8, 9), SF), ((7, 10), STAR), ((8, 10), STAR), ((6, 6), SF), ((9, 6), SF), ((3, 6), SF), ((12, 6), SF),
                   ((7, 7), SF), ((8, 7), SF), ((7, 12), SF), ((8, 12), SF), ((7, 11), (180, 70, 20)), ((8, 11), (180, 70, 20)),
                   ((2, 3), SF), ((13, 3), SF)],
    'leggings': [((x, 3), SF) for x in range(4, 12)] + [((7, 3), WHITE), ((8, 3), STAR), ((4, 8), STAR), ((10, 8), STAR),
                                                         ((4, 9), (200, 80, 24)), ((10, 9), (200, 80, 24)), ((5, 11), SF), ((11, 11), SF)],
    'boots': [((4, 4), SF), ((11, 4), SF), ((4, 5), SF), ((11, 5), SF), ((3, 10), SF), ((12, 10), SF),
              ((2, 11), STAR), ((3, 11), WHITE), ((12, 11), WHITE), ((13, 11), STAR), ((4, 11), SF), ((11, 11), SF)],
}


def starforged(piece):
    im = Image.open(VAN + f'item/netherite_{piece}.png').convert('RGBA'); px = im.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a: px[x, y] = _c(GUN(min(1.0, ((r + g + b) / 3 / 112) ** 0.85 * 1.05)))
    P = _P(im)
    for (x, y), c in SF_PAINT[piece]: P.p(x, y, c)
    return im


# ---- the Singularity Launcher: vanilla's crossbow frames, recoloured
def _launcher(src, loaded=False):
    im = Image.open(VAN + f'item/{src}.png').convert('RGBA'); px = im.load()
    GUNR = ramp([(0.0, (14, 16, 20)), (0.3, GM[0]), (0.6, GM[1]), (0.8, GM[2]), (1.0, GM[3])])
    VIR = ramp([(0.0, VI[0]), (0.45, VI[1]), (0.75, VI[2]), (1.0, VI[3])])
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            if not a: continue
            L = _lum((r, g, b))
            grey = max(r, g, b) - min(r, g, b) < 12
            if grey and L > 200 and loaded: continue                             # (the arrowhead: painted over below)
            if grey:                                                            # (the string: a green energy filament)
                px[x, y] = _c(GN[3] if L > 130 else (GN[2] if L > 90 else GN[1])); continue
            if loaded and (r, g, b) in ((137, 103, 39), (84, 61, 18), (109, 79, 24), (69, 50, 13)):   # (the bolt: violet light)
                px[x, y] = _c(VI[3] if L > 100 else VI[2]); continue
            limb = y <= 2 or x <= 2
            px[x, y] = _c((VIR if limb else GUNR)(L / 150))
    P = _P(im)
    if loaded:                                                                  # (the singularity: a black heart in a violet halo)
        for x, y, c in ((2, 2, VI[3]), (3, 2, VI[4]), (4, 2, VI[3]), (2, 3, VI[4]), (3, 3, (6, 2, 12)), (4, 3, VI[2]),
                        (2, 4, VI[3]), (3, 4, VI[2]), (4, 4, VI[1]), (1, 1, VI[2]), (5, 1, VI[4]), (1, 5, VI[4])):
            P.p(x, y, c)
    else:
        P.p(9, 9, GN[2]); P.p(10, 10, GN[1])                                    # (a charge light on the stock)
    return im


def launcher_icons():
    return {'singularity_launcher': _launcher('crossbow_standby'), 'singularity_launcher_pull0': _launcher('crossbow_pulling_0'),
            'singularity_launcher_pull1': _launcher('crossbow_pulling_1'), 'singularity_launcher_pull2': _launcher('crossbow_pulling_2'),
            'singularity_launcher_charged': _launcher('crossbow_arrow', loaded=True)}


def icons():
    out = {'hive_coords': hive_coords(), 'cipher_1': cipher(1), 'cipher_2': cipher(2), 'cipher_3': cipher(3), 'hive_sigil': hive_sigil(),
           'akey': akey(), 'akey_victor': akey_victor(), 'star_core': star_core(), 'squad_jetpack': squad_jetpack(),
           'hover_collar': hover_collar(), 'hive_override': hive_override(), 'stardust_kite': stardust_kite(), 'vexis_link': vexis_link()}
    for p in ('helmet', 'chestplate', 'leggings', 'boots'): out[f'starforged_{p}'] = starforged(p)
    out.update(launcher_icons())
    return out


# ==================================================================================================== the worn plate (bm:starforged)
def equip_layer(kind):
    """vanilla's netherite plate in gunmetal; its seams (a pixel darker than the plate round it) gold-orange; star cores glowing
    in the breast and the brow (humanoid) or the belt's buckle (leggings); the boots' soles thrusters"""
    im = Image.open(f'{VAN}entity/equipment/{kind}/netherite.png').convert('RGBA'); src = im.copy().load(); px = im.load(); w, h = im.size
    L = lambda x, y: (sum(src[x, y][:3]) / 3) if (0 <= x < w and 0 <= y < h and src[x, y][3]) else None
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if not a: continue
            v = L(x, y); ns = [L(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            px[x, y] = _c(GUN(min(1.0, (v / 112) ** 0.85 * 1.05)), a)
            if all(n is not None for n in ns) and v < sum(ns) / 4 - 11 and v > 18:
                px[x, y] = _c(SF if (x + y) % 3 else STAR, a)
    def put(x, y, c):
        if px[x, y][3]: px[x, y] = _c(c)
    if kind == 'humanoid':
        for x, y, c in ((23, 23, WHITE), (24, 23, SF), (23, 24, STAR), (24, 24, STAR), (22, 23, (190, 80, 24)), (25, 24, (190, 80, 24))):
            put(x, y, c)                                                        # (the breast's core)
        for x, y, c in ((11, 9, WHITE), (12, 9, STAR), (10, 9, SF), (13, 9, SF)):  # (the brow's)
            put(x, y, c)
        for x in range(0, 16):                                                  # (the boots' soles: thrusters)
            if px[x, 31][3]: px[x, 31] = _c(STAR if x % 4 in (1, 2) else SF)
    else:
        for x, y, c in ((23, 20, WHITE), (24, 20, STAR), (22, 20, SF), (25, 20, SF)):
            put(x, y, c)
        for x in (4, 5): put(x, 25, STAR)                                     # (the knees)
    return im


# ==================================================================================================== block textures (am_*)
def _stripes(base, dark, seed, size=64, step=8):
    im = _cells(base, seed, 0.08, size); d = ImageDraw.Draw(im)
    for k in range(-size, size, step):
        d.line((k, size, k + size, 0), fill=_c(dark), width=2)
    return im


def _xtal(lo, mid, hi, seed, size=64):
    """a crystal face: long streaks of light down it"""
    im = _cells(mid, seed, 0.1, size); d = ImageDraw.Draw(im); rnd = random.Random(seed + 1)
    for _ in range(14):
        x = rnd.randrange(0, size, 2); y0 = rnd.randrange(0, size // 2); ln = rnd.randint(12, 40)
        d.rectangle((x, y0, x + 1, min(size - 1, y0 + ln)), fill=_c(rnd.choice((hi, lo))))
    return im


def textures():
    return {
        'am_gun': _cells(GM[1], 2201, 0.08, spots=[(GM[2], 70), (GM[0], 60)]),
        'am_gun_l': _cells(GM[2], 2202, 0.07, spots=[(GM[3], 60), (GM[1], 40)]),
        'am_gun_d': _cells(GM[0], 2203, 0.1, spots=[((24, 26, 32), 80), (GM[1], 30)]),
        'am_red': _cells(RED, 2204, 0.07, spots=[(RED_L, 50), ((168, 30, 34), 40)]),
        'am_red_d': _cells((70, 20, 24), 2205, 0.1, spots=[((40, 12, 14), 60)]),
        'am_green': _cells(GN[2], 2206, 0.08, spots=[(GN[3], 60), (GN[1], 30)]),
        'am_green_l': _cells(GN[3], 2207, 0.06, spots=[(GN[4], 70)]),
        'am_star': _cells(STAR, 2208, 0.06, spots=[(SF, 80), ((255, 110, 40), 40)]),
        'am_star_w': _cells(WHITE, 2209, 0.03, spots=[((255, 250, 230), 80), (SF, 20)]),
        'am_gold': _cells(SF, 2210, 0.06, spots=[((255, 200, 110), 50)]),
        'am_wrap': _stripes((40, 42, 48), (20, 22, 26), 2211),
        'am_chitin': _veins(_cells((40, 96, 50), 2212, 0.12, spots=[((26, 64, 34), 80), ((64, 130, 70), 40)]), 2213, 4, GN[1], GN[2]),
        'am_xtal': _xtal(GN[1], GN[2], GN[4], 2214),
        'am_xtal_c': _cells(GN[3], 2215, 0.05, spots=[(GN[4], 90)]),
        'am_xdead': _veins(_cells((34, 42, 38), 2216, 0.12, spots=[((22, 28, 26), 90), ((56, 64, 60), 40)]), 2217, 10, (10, 12, 12)),
        'am_crack': _cells((8, 10, 10), 2218, 0.05),
        'am_smoke': _cells((96, 100, 106), 2219, 0.1, spots=[((130, 134, 140), 60), ((70, 74, 80), 60)]),
        'am_smoke_d': _cells((62, 66, 72), 2220, 0.1, spots=[((84, 88, 94), 50)]),
    }


# ==================================================================================================== 3D models
def B(fr, to, tex, light=0, rot=None, uv=None, faces=None, shift=True):
    rs = B.rnd
    return el(fr, to, tex, PIV, rot=rot, uv=uv, faces=faces, light=light, shift=(rs.random(), rs.random()) if shift and not uv else None)


B.rnd = random.Random(23)


def S(a, b, w, h, tex, light=0, up=FRONT):
    return seg(a, b, w, h, tex, PIV, up, 0.15, light=light, shift=(B.rnd.random(), B.rnd.random()))


def CH(pts, ws, hs, tex, light=0, up=FRONT):
    return [S(pts[i], pts[i + 1], ws[i], hs[i], tex, light, up) for i in range(len(pts) - 1)]


def GEM(c, s, tex, light=15, rot=(35.26, 45.0, 0.0)):
    return el((c[0] - s / 2, c[1] - s / 2, c[2] - s / 2), (c[0] + s / 2, c[1] + s / 2, c[2] + s / 2), tex, PIV, rot=(rot, c), light=light)


def C(c, size, tex, light=0, rot=None):
    """a box by its centre and size (x, y, z), turned (x, y, z degrees) about its centre"""
    lo = tuple(c[i] - size[i] / 2 for i in range(3)); hi = tuple(c[i] + size[i] / 2 for i in range(3))
    return B(lo, hi, tex, light=light, rot=(rot, c) if rot else None)


def HEXP(y0, y1, r, tex, light=0, cx=8.0, cz=8.0):
    """a hexagonal prism (circumradius r): three boxes, each turned 60 degrees on from the last"""
    w, d = r, r * math.sqrt(3)
    out = []
    for a in (0.0, 60.0, -60.0):
        out.append(B((cx - w / 2, y0, cz - d / 2), (cx + w / 2, y1, cz + d / 2), tex, light=light,
                     rot=(('y', a, (cx, y0, cz)) if a else None)))
    return out


def _diag(els, grip, s):
    """a weapon built standing up (its grip at 8, 8, 8, its length up +y, its blade's edge to -x) laid on a vanilla sword
    sprite's diagonal: the grip at `grip`, the length toward the upper right, scaled s"""
    G = _rz(-45)
    def fpt(c):
        r = _mv(G, [c[i] - 8 for i in range(3)])
        return [grip[i] + r[i] * s for i in range(3)]
    return reframe(els, fpt, G, s)


def _lance():
    """standing up: a butt cap and spike, the haft, a wrapped grip, a rondel, red hive bands, a socket and wings, and the head -
    a blade of the star, white-hot inside, orange round it, flames off its root"""
    Y = lambda v: 8.0 + v
    E = [C((8, Y(-8.6), 8), (0.7, 1.2, 0.7), 'am_gun_l'), C((8, Y(-7.4), 8), (1.8, 1.4, 1.8), 'am_gun_l'),
         C((8, Y(-7.4), 8), (1.9, 0.4, 1.9), 'am_red', light=8),
         B((7.3, Y(-6.8), 7.3), (8.7, Y(5.0), 8.7), 'am_gun_d'), B((7.3, Y(5.0), 7.3), (8.7, Y(18.0), 8.7), 'am_gun'),
         B((7.1, Y(-3.4), 7.1), (8.9, Y(2.8), 8.9), 'am_wrap'),
         C((8, Y(3.6), 8), (3.0, 0.9, 3.0), 'am_gun_l'), C((8, Y(3.6), 8), (3.0, 0.9, 3.0), 'am_gun_l', rot=(0.0, 45.0, 0.0)),
         C((8, Y(4.3), 8), (2.0, 0.5, 2.0), 'am_gun')]
    for v in (7.0, 10.5, 14.0):                                                 # (red hive bands)
        E.append(C((8, Y(v), 8), (1.8, 0.8, 1.8), 'am_red', light=8))
    E += [C((8, Y(17.6), 8), (2.4, 1.0, 2.4), 'am_gun_l'), C((8, Y(18.6), 8), (1.9, 1.2, 1.9), 'am_gun'),
          C((8, Y(18.0), 8), (2.5, 0.35, 2.5), 'am_gold', light=10)]
    for sx in (1, -1):                                                          # (the socket's wings, swept back)
        E += CH([(8 + sx * 0.8, Y(18.6), 8.0), (8 + sx * 2.6, Y(17.6), 8.0), (8 + sx * 3.2, Y(15.8), 8.0)], [0.6, 0.45], [0.9, 0.7], 'am_gun_l')
    for (v0, v1, wd) in ((19.2, 22.4, 3.0), (22.2, 25.4, 2.4), (25.2, 28.2, 1.6), (28.0, 30.0, 0.9), (29.8, 31.0, 0.4)):
        E.append(B((8 - wd / 2, Y(v0), 7.4), (8 + wd / 2, Y(v1), 8.6), 'am_star', light=15))
    for (v0, v1, wd) in ((19.4, 23.0, 1.6), (22.8, 26.4, 1.1), (26.2, 29.0, 0.6)):
        E.append(B((8 - wd / 2, Y(v0), 7.2), (8 + wd / 2, Y(v1), 8.8), 'am_star_w', light=15))
    for (a, b, wdt) in (((6.4, Y(19.6), 8.0), (5.4, Y(22.4), 8.3), 0.6), ((9.6, Y(19.8), 8.0), (10.6, Y(23.0), 7.7), 0.6),
                        ((7.6, Y(20.0), 7.0), (7.2, Y(23.4), 6.2), 0.5), ((8.4, Y(20.2), 9.0), (8.8, Y(23.6), 9.8), 0.5)):
        E.append(S(a, b, wdt, wdt, 'am_star', light=15))                       # (flames off its root)
    for (x, v, z, s) in ((5.0, 24.6, 8.0, 0.4), (11.0, 26.0, 8.0, 0.35), (8.0, 32.0, 8.0, 0.3)):
        E.append(B((x - s, Y(v) - s, z - s), (x + s, Y(v) + s, z + s), 'am_star_w', light=15, shift=False))
    return _diag(E, (4.0, 4.0, 8.0), 0.78)


def _axe():
    """standing up: a pommel with a red stone, a dark haft, a wrapped grip, a red band; the head - a gunmetal block, a crescent
    blade to -x (red chevrons on both faces, a green energy edge), a back spike, a top spike"""
    Y = lambda v: 8.0 + v
    E = [C((8, Y(-6.6), 8), (2.0, 1.6, 2.0), 'am_gun_l'), C((8, Y(-6.6), 7.0), (0.8, 0.8, 0.3), 'am_red', light=10),
         B((7.4, Y(-5.8), 7.4), (8.6, Y(17.0), 8.6), 'am_gun_d'),
         B((7.2, Y(-3.6), 7.2), (8.8, Y(3.4), 8.8), 'am_wrap'), C((8, Y(6.4), 8), (1.6, 0.7, 1.6), 'am_red', light=6),
         C((8, Y(15.0), 8), (3.0, 6.4, 2.6), 'am_gun'), C((8, Y(15.0), 8), (3.3, 0.6, 2.8), 'am_red', light=6),
         C((8, Y(18.6), 8), (1.4, 1.2, 1.4), 'am_gun_l'), C((8, Y(19.8), 8), (0.8, 1.4, 0.8), 'am_gun_l')]
    for (x0, x1, v0, v1) in ((-3.0, -1.4, 12.6, 17.4), (-5.0, -3.0, 11.6, 18.4), (-7.0, -5.0, 10.6, 19.4), (-8.4, -7.0, 10.0, 20.0)):
        E.append(B((8 + x0, Y(v0), 7.5), (8 + x1, Y(v1), 8.5), 'am_gun_l'))
    E.append(B((8 - 9.1, Y(9.6), 7.7), (8 - 8.3, Y(20.4), 8.3), 'am_green_l', light=15))   # (the green energy edge)
    E.append(B((8 - 8.6, Y(9.4), 7.6), (8 - 7.6, Y(10.2), 8.4), 'am_green', light=12))
    E.append(B((8 - 8.6, Y(19.8), 7.6), (8 - 7.6, Y(20.6), 8.4), 'am_green', light=12))
    for z in (7.38, 8.62):                                                      # (red chevrons, pointing to the edge, both faces)
        for cx in (-3.2, -5.9):
            E += [S((8 + cx + 1.0, Y(13.2), z), (8 + cx - 0.4, Y(15.0), z), 0.55, 0.2, 'am_red', light=6, up=(0.0, 0.0, 1.0)),
                  S((8 + cx - 0.4, Y(15.0), z), (8 + cx + 1.0, Y(16.8), z), 0.55, 0.2, 'am_red', light=6, up=(0.0, 0.0, 1.0))]
    E += CH([(9.5, Y(15.0), 8.0), (11.6, Y(15.0), 8.0), (13.2, Y(14.4), 8.0)], [1.0, 0.6], [1.8, 1.0], 'am_gun_l')   # (the back spike)
    E.append(C((13.5, Y(14.3), 8), (0.6, 0.6, 0.6), 'am_red', light=8))
    return _diag(E, (4.0, 4.0, 8.0), 0.74)


def _crown():
    """a gunmetal band round a head in 3..13 (front north), red-trimmed; a plaque at its front, a green gem set in it; six
    antennae curling up and back, their tips lit"""
    E = [B((2.5, 11.0, 2.5), (13.5, 13.0, 3.1), 'am_gun'), B((2.5, 11.0, 12.9), (13.5, 13.0, 13.5), 'am_gun'),
         B((2.5, 11.0, 3.1), (3.1, 13.0, 12.9), 'am_gun'), B((12.9, 11.0, 3.1), (13.5, 13.0, 12.9), 'am_gun'),
         B((2.4, 10.7, 2.4), (13.6, 11.2, 3.0), 'am_red', light=6), B((2.4, 10.7, 13.0), (13.6, 11.2, 13.6), 'am_red', light=6),   # (red trim
         B((2.4, 10.7, 3.0), (3.0, 11.2, 13.0), 'am_red', light=6), B((13.0, 10.7, 3.0), (13.6, 11.2, 13.0), 'am_red', light=6),  #  along its foot)
         B((2.6, 13.0, 2.6), (13.4, 13.4, 13.4), 'am_gun_l', faces=('north', 'south', 'east', 'west'))]   # (its lit lip; open above)
    E += [B((5.8, 12.4, 2.0), (10.2, 15.6, 2.6), 'am_gun'), B((6.6, 15.6, 2.1), (9.4, 16.8, 2.6), 'am_gun'),
          B((7.4, 16.8, 2.2), (8.6, 17.8, 2.6), 'am_gun_l'),
          B((5.6, 12.2, 1.9), (10.4, 12.6, 2.7), 'am_red', light=6)]
    E.append(GEM((8.0, 14.4, 2.0), 2.0, 'am_green_l', rot=(0.0, 0.0, 45.0)))
    E.append(B((7.6, 14.0, 1.4), (8.4, 14.8, 1.8), 'am_green', light=15))
    ants = [  # (root, bend, tip, widths)
        ((4.4, 13.0, 3.2), (3.2, 18.0, 4.0), (1.6, 22.0, 7.6), (0.9, 0.6)),
        ((11.6, 13.0, 3.2), (12.8, 18.0, 4.0), (14.4, 22.0, 7.6), (0.9, 0.6)),
        ((3.0, 13.0, 8.0), (1.6, 16.6, 9.0), (0.6, 18.6, 12.4), (0.75, 0.5)),
        ((13.0, 13.0, 8.0), (14.4, 16.6, 9.0), (15.4, 18.6, 12.4), (0.75, 0.5)),
        ((6.0, 13.0, 12.9), (5.2, 16.2, 14.6), (4.6, 17.4, 17.0), (0.7, 0.45)),
        ((10.0, 13.0, 12.9), (10.8, 16.2, 14.6), (11.4, 17.4, 17.0), (0.7, 0.45))]
    for a, b, c, (w0, w1) in ants:
        E += CH([a, b, c], [w0 * 1.25, w1 * 1.3], [w0 * 1.25, w1 * 1.3], 'am_chitin', up=(0.0, 0.0, 1.0))
        E.append(C(a, (w0 * 1.9, 0.8, w0 * 1.9), 'am_gun_l'))                   # (a socket in the band)
        E.append(GEM(c, 1.5 if w0 > 0.8 else 1.15, 'am_green_l', rot=(20.0, 30.0, 10.0)))
    return E


def _pylon(lit):
    """a hexagonal crystal stood in a gunmetal collar (its foot at y 2: the display stands it on the floor), red lights round the
    collar, three clamps up its sides; lit - green light, emissive, a point, two shards hanging by it; dead - dark, cracked, its
    tip broken off, smoke going up"""
    L = 15 if lit else 0
    E = HEXP(1.2, 2.2, 5.6, 'am_gun_d') + HEXP(2.2, 5.0, 4.8, 'am_gun') + HEXP(5.0, 5.8, 4.0, 'am_gun_l')
    for k in range(6):                                                          # (lights round the collar)
        a = math.radians(30 + k * 60); x, z = 8 + 4.15 * math.cos(a), 8 + 4.15 * math.sin(a)
        E.append(C((x, 3.6, z), (0.8, 0.8, 0.8), 'am_red' if lit else 'am_red_d', light=12 if lit else 0, rot=(0.0, -(30 + k * 60), 0.0)))
    for k in range(3):                                                          # (clamps)
        ang = 90 + k * 120; a = math.radians(ang)
        r0, r1 = 3.6, 2.6
        E += CH([(8 + r0 * math.cos(a), 5.4, 8 + r0 * math.sin(a)), (8 + r1 * math.cos(a), 10.0, 8 + r1 * math.sin(a))], [1.0], [0.6], 'am_gun_l')
    if lit:
        E += HEXP(5.0, 15.0, 2.6, 'am_xtal', L) + HEXP(15.0, 17.2, 2.0, 'am_xtal', L) + HEXP(17.2, 18.8, 1.3, 'am_xtal_c', L) + \
            HEXP(18.8, 19.8, 0.6, 'am_xtal_c', L)
        E += [GEM((3.4, 12.6, 8.4), 1.3, 'am_xtal_c', rot=(10.0, 20.0, 35.0)), GEM((12.6, 10.4, 7.2), 1.0, 'am_xtal_c', rot=(30.0, 10.0, 20.0)),
              GEM((8.6, 21.4, 8.0), 0.6, 'am_xtal_c')]
    else:
        E += HEXP(5.0, 13.0, 2.6, 'am_xdead')
        E += [C((7.4, 13.8, 8.2), (2.6, 1.8, 3.4), 'am_xdead', rot=(8.0, 0.0, 14.0)), C((9.0, 13.4, 7.6), (1.6, 1.6, 2.4), 'am_xdead', rot=(-12.0, 20.0, -18.0)),
              C((6.8, 14.8, 8.6), (1.0, 1.6, 1.2), 'am_xdead', rot=(0.0, 30.0, 22.0))]
        for (a, b) in (((6.0, 6.0, 5.5), (6.8, 9.4, 5.5)), ((6.8, 9.4, 5.5), (6.2, 12.0, 5.6)), ((10.4, 7.0, 8.6), (10.5, 10.8, 9.2)),
                       ((9.2, 8.4, 10.3), (8.4, 11.6, 10.3))):
            E.append(S(a, b, 0.35, 0.2, 'am_crack', up=(0.0, 0.0, 1.0)))
        for (x, y, z, s, tex) in ((8.4, 16.4, 8.0, 2.2, 'am_smoke_d'), (7.4, 18.6, 8.6, 1.8, 'am_smoke'), (8.6, 20.6, 7.6, 1.4, 'am_smoke'),
                                  (7.8, 22.4, 8.2, 1.0, 'am_smoke')):
            E.append(C((x, y, z), (s, s, s), tex, rot=(B.rnd.uniform(-30, 30), B.rnd.uniform(0, 90), B.rnd.uniform(-30, 30))))
    return E


def models():
    B.rnd.seed(23)
    M = {'starfire_lance': _lance(), 'hive_breaker': _axe(), 'admiral_crown': _crown(), 'vx_pylon': _pylon(True), 'vx_pylon_off': _pylon(False)}
    for name, els in M.items():
        for e in els:
            for v in e['from'] + e['to']: assert -16 <= v <= 32, (name, e)
            for f in e['faces'].values():
                assert all(0 <= u <= 16 for u in f['uv']), (name, f)
    return M


# ---- display transforms
def _fit_gui(lo, hi, base, rot=(0, 0, 0), pad=0.94):
    s = 16 * pad / max(hi[0] - lo[0], hi[1] - lo[1])
    return dict(base, gui={'rotation': list(rot), 'translation': [round(-((lo[0] + hi[0]) / 2 - 8) * s, 3), round(-((lo[1] + hi[1]) / 2 - 8) * s, 3), 0],
                           'scale': [round(s, 3)] * 3})


LANCE_DISP = dict(_fit_gui((-0.8, -0.8), (21.8, 21.8), HANDHELD_DISP),
                  fixed={'rotation': [0, 180, 0], 'translation': [-1.6, -1.6, 0], 'scale': [0.72, 0.72, 0.72]},
                  ground={'rotation': [0, 0, 0], 'translation': [0, 2, 0], 'scale': [0.35, 0.35, 0.35]})
AXE_DISP = dict(_fit_gui((-1.0, -1.0), (19.0, 19.5), HANDHELD_DISP),
                fixed={'rotation': [0, 180, 0], 'translation': [-0.8, -1.0, 0], 'scale': [0.78, 0.78, 0.78]})
CROWN_DISP = dict(HEAD_DISP, gui={'rotation': [25, 200, 0], 'translation': [0, -6.4, 0], 'scale': [0.85, 0.85, 0.85]},
                  fixed={'rotation': [0, 180, 0], 'translation': [0, -4.5, 0], 'scale': [0.62, 0.62, 0.62]},
                  ground={'rotation': [0, 0, 0], 'translation': [0, -3, 0], 'scale': [0.4, 0.4, 0.4]})
PYLON_DISP = {'gui': {'rotation': [20, 225, 0], 'translation': [0, -1.6, 0], 'scale': [0.62, 0.62, 0.62]},
              'ground': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.35, 0.35, 0.35]},
              'fixed': {'rotation': [0, 0, 0], 'translation': [0, -2.5, 0], 'scale': [0.7, 0.7, 0.7]}}
DISP = {'starfire_lance': LANCE_DISP, 'hive_breaker': AXE_DISP, 'admiral_crown': CROWN_DISP, 'vx_pylon': PYLON_DISP, 'vx_pylon_off': PYLON_DISP}


def model_json(name, els):
    used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
    t = {u: f'bm:block/{u}' for u in used}; t['particle'] = t[used[0]]
    return {'textures': t, 'elements': els, 'display': DISP[name]}


def launcher_def():
    """vanilla's crossbow item definition, with the launcher's frames"""
    mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
    drawn = {'type': 'minecraft:condition', 'property': 'minecraft:using_item', 'on_false': mdl('singularity_launcher'),
             'on_true': {'type': 'minecraft:range_dispatch', 'property': 'minecraft:crossbow/pull',
                         'entries': [{'threshold': 0.58, 'model': mdl('singularity_launcher_pull1')},
                                     {'threshold': 1.0, 'model': mdl('singularity_launcher_pull2')}],
                         'fallback': mdl('singularity_launcher_pull0')}}
    if not CHARGE_SELECT: return {'model': drawn}
    return {'model': {'type': 'minecraft:select', 'property': 'minecraft:charge_type',
                      'cases': [{'when': ['arrow', 'rocket'], 'model': mdl('singularity_launcher_charged')}], 'fallback': drawn}}


def equipment(R2):
    for layer in ('humanoid', 'humanoid_leggings'):
        equip_layer(layer).save(R2.p('assets', 'bm', 'textures', 'entity', 'equipment', layer, 'starforged.png'))
    R2.wj('assets/bm/equipment/starforged.json', {'layers': {'humanoid': [{'texture': 'bm:starforged'}], 'humanoid_leggings': [{'texture': 'bm:starforged'}]}})


# ==================================================================================================== the pack
def rp(R):
    """gen_rp: the flat icons (the launcher's frames among them) through ICONS, the am_ textures through TEXTURE_MODS; in a
    post pass the 3D models with their item definitions, the launcher's crossbow models and definition, and the Starforged
    plate (equipment asset bm:starforged)"""
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS.update(icons())
    def post(R2):
        for name, els in models().items():
            R2.wj(f'assets/bm/models/item/{name}.json', model_json(name, els))
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        for name in LAUNCHER:                                                   # (held as a crossbow: vanilla's crossbow display)
            R2.wj(f'assets/bm/models/item/{name}.json', {'parent': 'minecraft:item/crossbow', 'textures': {'layer0': f'bm:item/{name}'}})
        R2.wj('assets/bm/items/singularity_launcher.json', launcher_def())
        equipment(R2)
    R.POST.append(post)
