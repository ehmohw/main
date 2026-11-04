"""(3.1 draft, stage 1: art only - not wired) THE DOODLE MOB - the Doodle Dragon's new display name (his internal id, dd_ /
'dragon', stays, so saves don't break). Kettle has started drawing him as Minecraft's own mobs: a costume per mob, all in the
crayon style of his Doodle Creeper (3.0b, doodle_dragon_art: waxy crayon, wobbly dark outlines, scribbled fill that runs outside
the lines, paper flecks; flat two-sided paper cards layered like a puppet). This module holds the NEW forms only - the Creeper
and the Ender Dragon (his current model; players who recruited him as the dragon keep it) stay in doodle_dragon_art.

FORMS (FORMS[name]: a Rig each - its own cards and, where a mob's build needs it, its own pivots)
  zombie   THE DOODLE ZOMBIE (the new DEFAULT): a big boxy green head (square black eyes with a shine, a wobbly little frown,
           pink cheeks, a dark scribbled hairline), a cyan shirt torn at the hem, blue trousers and grey shoes, green arms held
           straight out in front... as a kid draws it: straight out to the sides.
  skeleton THE DOODLE SKELETON: an off-white skull (square sockets, a nose hole, a row of teeth), a ribcage of crayon bones on a
           spine, stick-bone arms and legs; a brown crayon BOW in his left hand.
  jockey   THE DOODLE CHICKEN JOCKEY: a white crayon chicken drawn side-on (as kids draw chickens) - red comb and wattle,
           orange beak and legs, a scribbled wing either side that flaps (wingr/wingl) - and riding it, a tiny baby zombie
           (the 'head' card), waving.
  golem    THE DOODLE IRON GOLEM: a broad pale-iron body with green vines scribbled up it and cracks, a small head with a long
           nose and a heavy brow, long arms down to his knees - holding a red crayon POPPY.
  axolotl  THE DOODLE AXOLOTL: pink and round: a wide head with three frilly magenta gills a side, dot eyes, a big smile; a
           little body with a pale belly, stubby legs, a fat fin tail out to his left.
  enderman THE DOODLE ENDERMAN: tall (his own pivots): black crayon pressed hard, a square head with glowing violet eyes (an
           eye card, light_emission), a thin body, long thin arms and legs - carrying a crayon GRASS BLOCK; violet specks.

Every form: idle_a, walk_0/1, atk_up/atk (its own attack), sit_a, happy; faces happy, blink, fierce. Design units as
doodle_dragon_art: feet at y=0, facing -z, his right +x; RIG_SCALE 0.78 (Kettle's)."""
import math
import zlib
import doodle_dragon_art as DD
from doodle_dragon_art import Pic, ell, sq, bez, card, capsule, tri, tube
from fol5_kit import Rig, limb, T

INK = '#26222c'
FACES = ('happy', 'blink', 'fierce')
DZ_EYE = 0.12


def _eyes_sq(pic, x, y, s, kind, col=INK, shine=True, line=None):
    """square crayon eyes (Minecraft's) - each expression redraws them"""
    for i, sx in enumerate((1, -1)):
        cx = sx * x
        if kind == 'happy':
            pic.crayon([(cx - s, y - s * 0.4), (cx, y + s * 0.6), (cx + s, y - s * 0.4)], col, 0.42, 50 + i, closed=False, passes=2, jit=0.02)
        elif kind == 'blink':
            pic.crayon([(cx - s, y), (cx + s, y)], col, 0.42, 52 + i, closed=False, passes=2, jit=0.02)
        else:
            q = sq(cx, y - (0.2 if kind == 'fierce' else 0), s, s * (0.75 if kind == 'fierce' else 1.0), 4.5, 32)
            pic.blob(q, col, line or DD.CK_L, 54 + i, over=0.05, light=0.1, amp=0.03, ow=0.26)
            if shine: pic.fill(sq(cx - s * 0.4, y + s * 0.35, s * 0.28, s * 0.28, 3, 12), '#ffffff', 56 + i)
            if kind == 'fierce':
                pic.crayon([(cx + sx * s * 1.3, y + s * 1.6), (cx - sx * s * 1.1, y + s * 1.1)], INK, 0.38, 58 + i, closed=False, passes=2, jit=0.02)


def _cheeks(pic, x, y, r=0.9):
    for i, sx in enumerate((1, -1)): pic.dot((sx * x, y), r, r * 0.7, DD.CHEEK, 60 + i)


def _mouth(pic, y, kind, w=1.4, col=INK):
    if kind == 'happy': pic.crayon(bez((-w, y + 0.3), (0, y - 0.9), (w, y + 0.3), 10), col, 0.36, 70, closed=False, passes=2, jit=0.02)
    elif kind == 'fierce': pic.blob(sq(0, y - 0.2, w * 0.9, 0.55, 3, 24), col, col, 71, over=0.0, ow=0.2)
    else: pic.crayon(bez((-w * 0.8, y - 0.2), (0, y + 0.4), (w * 0.8, y - 0.2), 10), col, 0.32, 72, closed=False, passes=2, jit=0.02)


# ---------------------------------------------------------------------------------------------------- the forms' pictures
def zombie():
    G, GL, CY, CYL, BL, BLL = '#5aa84a', '#24581e', '#2cb8c0', '#145e66', '#3a4ab8', '#1c2260'
    def body(back=False):
        p = Pic((-8.0, 3.0, 16.0))
        shirt = [(-4.6, 16.4), (4.6, 16.4), (4.8, 6.4), (3.4, 5.4), (2.2, 6.6), (0.8, 5.2), (-0.6, 6.6), (-2.0, 5.3), (-3.4, 6.5), (-4.8, 5.6)]
        p.blob(shirt, CY, CYL, 101, ang=30, over=0.4)
        if not back: p.blob(sq(0, 15.8, 1.4, 0.6, 3, 20), G, GL, 102, over=0.0, ow=0.25)              # (his neck, in the collar)
        return p
    def head(face=None, back=False):
        p = Pic((-8.0, 16.0, 16.0))
        s = p.blob(sq(0, 22.6, 5.6, 5.6, 4.0, 64), G, GL, 111, ang=40, over=0.45)
        p.blob([(-5.6, 28.2), (5.6, 28.2), (5.6, 26.2), (3.0, 26.9), (1.0, 26.0), (-1.4, 26.9), (-3.6, 25.9), (-5.6, 26.6)], '#2e5a24', GL, 112, over=0.1, ow=0.3)
        if not back:
            _eyes_sq(p, 2.4, 23.2, 1.15, face); _cheeks(p, 4.0, 20.8); _mouth(p, 19.6, face if face else 'frown')
        return p
    def arm(back=False):
        p = Pic((2.5, 7.0, 8.0))
        p.blob(sq(6.0, 13.0, 1.9, 1.15, 3.2, 30), CY, CYL, 121, ang=80, over=0.2)                      # (the sleeve)
        p.blob(sq(8.9, 13.0, 1.4, 1.05, 3.2, 30), G, GL, 122, ang=80, over=0.2)                       # (the hand, straight out)
        return p
    def leg(back=False):
        p = Pic((-0.5, -0.5, 8.0))
        p.blob(sq(2.5, 3.6, 1.8, 2.6, 3.4, 40), BL, BLL, 131, ang=70, over=0.2)
        p.blob(sq(2.6, 0.75, 1.9, 0.75, 3.0, 30), '#8a8a92', '#3a3a40', 132, over=0.0)
        return p
    fx = None
    return dict(body=body, head=head, armr=arm, legr=leg), dict(), fx


def skeleton():
    B, BL = '#f0ece0', '#6a6a70'
    def body(back=False):
        p = Pic((-8.0, 3.0, 16.0))
        p.blob(sq(0, 11.0, 0.7, 5.6, 3, 30), B, BL, 201, over=0.0, ow=0.3)                             # (the spine)
        for i, y in enumerate((15.0, 13.4, 11.8, 10.2)):
            p.blob(tube([(-3.8, y - 0.6), (-1.8, y + 0.1), (1.8, y + 0.1), (3.8, y - 0.6)], 0.8, 0.8), B, BL, 202 + i, over=0.0, ow=0.26)
        p.blob(sq(0, 6.6, 3.2, 0.9, 3, 30), B, BL, 210, over=0.0, ow=0.3)                              # (the hips)
        return p
    def head(face=None, back=False):
        p = Pic((-8.0, 16.0, 16.0))
        p.blob(sq(0, 22.6, 5.4, 5.4, 4.0, 64), B, BL, 211, ang=40, over=0.3)
        if not back:
            _eyes_sq(p, 2.4, 23.4, 1.3, face if face != 'blink' else 'blink', col='#2a2a30', shine=face is None)
            p.blob(sq(0, 21.0, 0.5, 0.5, 3, 12), '#2a2a30', '#2a2a30', 214, over=0, ow=0.1)
            p.crayon([(-2.8, 19.0), (2.8, 19.0)], '#2a2a30', 0.3, 215, closed=False, passes=1)
            for x in (-2.0, -0.7, 0.7, 2.0): p.crayon([(x, 18.4), (x, 19.6)], '#2a2a30', 0.22, 216 + int(x * 10), closed=False, passes=1)
        return p
    def arm(back=False):
        p = Pic((2.5, 7.0, 8.0)); p.blob(tube([(4.2, 13.4), (5.8, 11.0), (6.6, 8.6)], 0.9, 0.8), B, BL, 221, over=0, ow=0.28); return p
    def arml(back=False):
        p = arm(back)
        bow = [(7.6, 14.2), (8.6, 11.2), (8.4, 8.6), (7.4, 6.2)]
        p.blob(tube(DD.spline(bow, 6), 0.7, 0.7), '#a8642a', '#5a3010', 225, over=0, ow=0.26)
        p.crayon([(7.6, 14.2), (6.8, 10.2), (7.4, 6.2)], '#e8e8e8', 0.14, 226, closed=False, passes=1, jit=0.02)
        return p
    def leg(back=False):
        p = Pic((-0.5, -0.5, 8.0)); p.blob(tube([(2.4, 6.0), (2.4, 0.6)], 0.9, 0.9), B, BL, 231, over=0, ow=0.28)
        p.blob(sq(2.8, 0.5, 1.2, 0.5, 3, 20), B, BL, 232, over=0, ow=0.26); return p
    def fx(back=False):                                                                                    # (BONE ARROW: a crayon arrow in flight)
        p = Pic((-8.0, 4.0, 16.0))
        p.blob(tube([(-6.0, 12.0), (5.0, 12.0)], 0.4, 0.4, cap=False), '#a8642a', '#5a3010', 241, over=0, ow=0.2)
        p.blob(tri((5.0, 12.0), 0, 1.6, 1.8), '#c8c8d0', '#5a5a60', 242, over=0, ow=0.2)
        for dy in (0.7, -0.7): p.blob(tri((-5.4, 12.0), 180 + dy * 30, 0.8, 1.4), '#ffffff', '#8a8a90', 243, over=0, ow=0.16)
        return p
    return dict(body=body, head=head, armr=arm, arml=arml, legr=leg), dict(), fx


def jockey():
    W, WL, OR, ORL, RD = '#fbfaf6', '#8a8a86', '#f6a23a', '#a85a10', '#e8343a'
    G, GL, CY, CYL = '#5aa84a', '#24581e', '#2cb8c0', '#145e66'
    def body(back=False):                                                                                  # the chicken, side-on: its head to his right
        p = Pic((-8.0, 1.0, 16.0))
        p.blob(ell(-0.4, 8.4, 5.6, 4.4, 60), W, WL, 301, ang=20, over=0.35)
        p.blob(ell(4.6, 12.0, 2.4, 2.6, 40), W, WL, 302, ang=60, over=0.2)
        p.blob(tri((-5.6, 9.6), 160, 2.6, 2.2), W, WL, 303, over=0.1, ow=0.3)                            # (its tail)
        if not back:
            p.blob(tri((6.8, 12.0), 0, 1.4, 1.6), OR, ORL, 304, over=0, ow=0.24)
            p.blob(ell(6.4, 10.6, 0.5, 0.9, 16), RD, '#8a1010', 305, over=0, ow=0.2)
            p.blob([(3.6, 14.2), (4.2, 15.4), (4.8, 14.4), (5.4, 15.2), (5.6, 14.0)], RD, '#8a1010', 306, over=0, ow=0.2)
            p.dot((5.4, 12.6), 0.42, 0.5, INK, 307); p.dot((5.3, 12.8), 0.14, 0.14, '#ffffff', 308)
        return p
    def head(face=None, back=False):                                                                       # the baby zombie, riding
        p = Pic((-8.0, 10.0, 16.0))
        p.blob(sq(0, 14.6, 2.0, 1.9, 3.4, 40), CY, CYL, 311, ang=40, over=0.25)
        p.blob(sq(0, 19.0, 3.0, 2.9, 4.0, 48), G, GL, 312, ang=40, over=0.3)
        for sx in (1, -1): p.blob(sq(sx * 2.6, 13.6, 0.7, 1.4, 3, 20), '#3a4ab8', '#1c2260', 313 + sx, over=0.05, ow=0.22)   # (little legs, astride)
        if not back:
            _eyes_sq(p, 1.25, 19.4, 0.65, face); _cheeks(p, 2.2, 18.0, 0.55); _mouth(p, 17.6, face, 0.7)
        return p
    def arm(back=False):                                                                                   # (his arm, waving: on his right only)
        p = Pic((2.5, 7.0, 8.0)); p.blob(tube([(2.6, 14.6), (4.0, 16.4), (4.6, 17.8)], 0.9, 0.9), G, GL, 321, over=0.05, ow=0.24); return p
    def leg(back=False):
        p = Pic((-0.5, -0.5, 8.0))
        p.blob(tube([(1.6, 5.2), (1.8, 1.0)], 0.6, 0.6), OR, ORL, 331, over=0, ow=0.22)
        for a in (-30, 0, 30): p.blob(tube([(1.8, 0.8), (1.8 + 1.4 * math.sin(math.radians(a)), 0.3)], 0.45, 0.4), OR, ORL, 332 + a, over=0, ow=0.18)
        return p
    def wing(back=False):
        p = Pic((3.0, 9.0, 16.0))
        p.blob([(3.2, 10.6), (6.4, 12.4), (8.8, 11.6), (9.6, 9.8), (7.6, 9.6), (8.4, 8.6), (6.0, 8.4), (6.6, 7.4), (3.6, 8.0)], W, WL, 341, ang=10, over=0.3)
        return p
    def fx(back=False):                                                                                    # (EGG TOSS: a crayon egg in flight, a crack)
        p = Pic((-8.0, 4.0, 16.0)); p.blob(ell(0, 12, 1.6, 2.1, 30), '#f2e6c8', '#8a7a5a', 351, over=0.1)
        p.crayon([(-1.4, 12.2), (-0.6, 11.6), (0.2, 12.4), (1.0, 11.6), (1.5, 12.2)], '#8a7a5a', 0.2, 352, closed=False, passes=1)
        return p
    return dict(body=body, head=head, armr=arm, legr=leg, wingr=wing), dict(gone=('arml',)), fx


def golem():
    I, IL, V, VL, RD = '#d8d2c4', '#6a645a', '#4a9a3a', '#225a1a', '#e8343a'
    def body(back=False):
        p = Pic((-8.0, 3.0, 16.0))
        p.blob(sq(0, 12.4, 6.2, 5.4, 3.4, 64), I, IL, 401, ang=30, over=0.35)
        p.blob(sq(0, 6.4, 3.4, 1.2, 3, 30), I, IL, 402, over=0.1, ow=0.3)
        for i, pts in enumerate(([(-4.6, 7.4), (-3.8, 10.4), (-4.8, 13.2), (-3.6, 16.8)], [(3.6, 8.0), (4.4, 11.6), (3.4, 14.6)])):
            p.crayon(pts, V, 0.5, 410 + i, closed=False, passes=2, jit=0.1)
            for j, q in enumerate(pts[1:]): p.dot(q, 0.6, 0.45, V, 412 + i * 5 + j, line=VL, ow=0.16)
        p.crayon([(1.0, 15.4), (1.8, 14.2), (1.2, 13.0)], IL, 0.2, 420, closed=False, passes=1)          # (a crack)
        return p
    def head(face=None, back=False):
        p = Pic((-8.0, 16.0, 16.0))
        p.blob(sq(0, 21.6, 3.4, 3.6, 3.6, 48), I, IL, 431, ang=40, over=0.3)
        if not back:
            p.blob(sq(0, 20.2, 0.8, 1.8, 3, 24), '#c8c0b0', IL, 432, over=0, ow=0.24)                     # (the long nose)
            p.crayon([(-2.8, 23.6), (2.8, 23.6)], '#5a544a', 0.6, 433, closed=False, passes=2)            # (the heavy brow)
            for i, sx in enumerate((1, -1)):
                if face == 'blink': p.crayon([(sx * 1.4 - 0.6, 22.6), (sx * 1.4 + 0.6, 22.6)], INK, 0.3, 434 + i, closed=False, passes=1)
                elif face == 'happy': p.crayon([(sx * 1.4 - 0.6, 22.4), (sx * 1.4, 23.0), (sx * 1.4 + 0.6, 22.4)], INK, 0.3, 434 + i, closed=False, passes=1)
                else: p.dot((sx * 1.4, 22.6), 0.45, 0.45, '#8a1a1a' if face != 'fierce' else '#e83030', 434 + i)
            _cheeks(p, 2.6, 19.6, 0.6)
            if face == 'happy': _mouth(p, 18.6, 'happy', 0.8)
        return p
    def arm(back=False):                                                                                   # (long, hanging to his knees)
        p = Pic((2.0, 1.0, 16.0)); p.blob(sq(7.4, 10.6, 1.6, 5.6, 3.4, 40), I, IL, 441, ang=80, over=0.25)
        p.crayon([(7.0, 14.0), (7.8, 11.0), (7.2, 8.0)], V, 0.4, 442, closed=False, passes=2, jit=0.1); return p
    def arml(back=False):
        p = arm(back)                                                                                      # (a red crayon poppy in his hand)
        p.crayon([(7.4, 5.0), (7.8, 2.4)], V, 0.3, 445, closed=False, passes=1)
        for a in range(0, 360, 72): p.dot((7.4 + 0.9 * math.cos(math.radians(a)), 2.0 + 0.9 * math.sin(math.radians(a))), 0.7, 0.7, RD, 446 + a, line='#8a1010', ow=0.14)
        p.dot((7.4, 2.0), 0.4, 0.4, INK, 449); return p
    def leg(back=False):
        p = Pic((-0.5, -0.5, 8.0)); p.blob(sq(2.6, 2.8, 2.0, 2.8, 3.4, 40), I, IL, 451, ang=70, over=0.2); return p
    def fx(back=False):                                                                                    # (IRON TOSS: dust thrown up under a foe)
        p = Pic((-8.0, -1.0, 16.0))
        for i, (x, y, r) in enumerate(((-3, 1.6, 1.8), (0, 2.6, 2.4), (3.2, 1.4, 1.7), (-1.4, 4.6, 1.3), (1.8, 4.8, 1.2))):
            p.blob(ell(x, y, r, r * 0.8, 30), '#ece6d8', '#8a8478', 461 + i, over=0.1, ow=0.26)
        return p
    return dict(body=body, head=head, armr=arm, arml=arml, legr=leg), dict(pivot={'head': (0, 18.4, -0.5), 'armr': (6.4, 15.6, -1.0), 'arml': (-6.4, 15.6, -1.0)}), fx


def axolotl():
    PK, PKL, MG, MGL, BEL = '#ffa8c8', '#c0507a', '#e0408a', '#80184a', '#ffe0ea'
    def body(back=False):
        p = Pic((-8.0, 3.0, 16.0))
        p.blob(ell(0, 10.0, 4.4, 4.4, 56), PK, PKL, 501, ang=30, over=0.35)
        if not back: p.blob(ell(0, 9.4, 2.6, 3.0, 40), BEL, PKL, 502, over=0.05, ow=0.22)
        return p
    def head(face=None, back=False):
        p = Pic((-8.0, 12.0, 16.0)); HY = -2.4                                                              # (his head sits low, on his shoulders)
        for sx in (1, -1):
            for j, a in enumerate((25, 0, -25)):
                p.blob(tube([(sx * 5.0, 21.6 + HY + a / 12), (sx * 7.2, 22.4 + HY + a / 7)], 1.0, 0.9), MG, MGL, 511 + j + (3 if sx > 0 else 0), over=0.1, ow=0.22)
        p.blob(sq(0, 21.0 + HY, 5.6, 4.2, 2.6, 64), PK, PKL, 520, ang=40, over=0.4)
        if not back:
            for i, sx in enumerate((1, -1)):
                if face == 'blink': p.crayon([(sx * 2.8 - 0.6, 22.0 + HY), (sx * 2.8 + 0.6, 22.0 + HY)], INK, 0.32, 521 + i, closed=False, passes=1)
                elif face == 'happy': p.crayon([(sx * 2.8 - 0.6, 21.8 + HY), (sx * 2.8, 22.5 + HY), (sx * 2.8 + 0.6, 21.8 + HY)], INK, 0.32, 521 + i, closed=False, passes=1)
                else:
                    p.dot((sx * 2.8, 22.0 + HY), 0.6 if face != 'fierce' else 0.5, 0.7, INK, 521 + i); p.dot((sx * 2.8 - 0.2, 22.3 + HY), 0.2, 0.2, '#ffffff', 523 + i)
            p.crayon(bez((-2.2, 19.8 + HY), (0, 18.6 + HY if face != 'fierce' else 19.4 + HY), (2.2, 19.8 + HY), 12), INK, 0.32, 525, closed=False, passes=2, jit=0.02)
            _cheeks(p, 3.9, 20.0 + HY, 0.7)
        return p
    def arm(back=False):
        p = Pic((2.5, 7.0, 8.0)); p.blob(tube([(3.6, 11.6), (5.2, 10.4)], 1.2, 1.0), PK, PKL, 531, over=0.05, ow=0.24); return p
    def leg(back=False):
        p = Pic((-0.5, -0.5, 8.0)); p.blob(sq(2.2, 4.2, 1.2, 1.6, 3, 30), PK, PKL, 541, over=0.05, ow=0.24); return p
    def tail(back=False):
        p = Pic((-17.0, 2.0, 16.0))
        p.blob(DD.spline([(-3.8, 8.0), (-7.4, 7.4), (-10.6, 8.6), (-12.8, 10.6), (-10.4, 10.4), (-7.0, 9.6), (-4.0, 10.0)], 6), PK, PKL, 551, ang=10, over=0.3)
        p.crayon([(-5.0, 9.8), (-8.0, 9.4), (-11.0, 10.2)], MG, 0.3, 552, closed=False, passes=1)
        return p
    def fx(back=False):                                                                                    # (BUBBLE: a stream of crayon bubbles)
        p = Pic((-8.0, 4.0, 16.0))
        for i, (x, y, r) in enumerate(((-4, 8, 1.2), (-1, 10.5, 1.6), (2.6, 13, 2.0), (5.4, 9.4, 1.0))):
            p.crayon(ell(x, y, r, r, 24), '#5ac8ff', 0.3, 561 + i, closed=True, passes=2, jit=0.03); p.dot((x - r * 0.4, y + r * 0.4), r * 0.2, r * 0.2, '#ffffff', 565 + i)
        return p
    return dict(body=body, head=head, armr=arm, legr=leg, tail=tail), dict(), fx


def enderman():
    K, KL, VI = '#2a2630', '#0e0c12', '#d86aff'
    def body(back=False):
        p = Pic((-8.0, 11.0, 16.0)); p.blob(sq(0, 19.0, 2.8, 5.2, 3.4, 48), K, KL, 601, ang=30, over=0.3); return p
    def head(face=None, back=False):
        p = Pic((-8.0, 23.0, 16.0)); p.blob(sq(0, 28.6, 4.4, 4.0, 4.0, 56), K, KL, 611, ang=40, over=0.3)
        if not back:
            _cheeks(p, 3.0, 27.0, 0.6)
            _mouth(p, 26.0, face, 1.0, col='#5a5060')
            for i, sx in enumerate((1, -1)):                                                              # (violet specks round him)
                p.dot((sx * 5.6, 31.4 - i * 2.6), 0.4, 0.4, VI, 615 + i)
        return p
    def eyes(face=None):
        p = Pic((-8.0, 23.0, 16.0))
        for i, sx in enumerate((1, -1)):
            if face == 'blink': p.crayon([(sx * 2.2 - 1.2, 29.0), (sx * 2.2 + 1.2, 29.0)], VI, 0.4, 621 + i, closed=False, passes=1)
            elif face == 'happy': p.crayon([(sx * 2.2 - 1.2, 28.8), (sx * 2.2, 29.6), (sx * 2.2 + 1.2, 28.8)], VI, 0.4, 621 + i, closed=False, passes=1)
            else:
                p.blob(sq(sx * 2.2, 29.0, 1.4, 0.55 if face == 'fierce' else 0.7, 3.6, 28), VI, '#8a2ab0', 621 + i, over=0, ow=0.18)
                p.dot((sx * 2.2, 29.0), 0.35, 0.35, '#ffffff', 623 + i)
        return p
    def arm(back=False):
        p = Pic((0.0, 6.0, 16.0)); p.blob(tube([(2.8, 23.4), (4.2, 16.0), (4.8, 10.0)], 1.0, 0.9), K, KL, 631, over=0.05, ow=0.26); return p
    def arml(back=False):
        p = arm(back)                                                                                      # (carrying a crayon grass block)
        p.blob(sq(5.6, 9.6, 2.0, 2.0, 6, 40), '#8a5a3a', '#4a2a14', 635, over=0.05, ow=0.26)
        p.blob([(3.6, 11.6), (7.6, 11.6), (7.6, 10.2), (6.6, 9.6), (5.6, 10.4), (4.6, 9.6), (3.6, 10.2)], '#5ab84a', '#2a6a22', 636, over=0.05, ow=0.22)
        return p
    def leg(back=False):
        p = Pic((-1.0, -0.5, 16.0)); p.blob(tube([(1.4, 14.4), (1.6, 0.6)], 1.1, 1.0), K, KL, 641, over=0.05, ow=0.26); return p
    def fx(back=False):                                                                                    # (BLINK: a ring of violet specks where he was)
        p = Pic((-8.0, 4.0, 16.0))
        for i in range(14):
            a = math.radians(i * 360 / 14); p.dot((5.4 * math.cos(a), 12 + 5.4 * math.sin(a)), 0.55, 0.55, VI, 651 + i, line='#8a2ab0', ow=0.12)
        return p
    pv = {'body': (0, 14.0, 0.0), 'head': (0, 24.0, -0.5), 'armr': (2.8, 23.0, -1.0), 'arml': (-2.8, 23.0, -1.0), 'legr': (1.4, 14.2, 1.1), 'legl': (-1.4, 14.2, 1.1)}
    return dict(body=body, head=head, armr=arm, arml=arml, legr=leg), dict(pivot=pv, eyes=eyes), fx


# ---------------------------------------------------------------------------------------------------- building
BASE_PIVOT = {'body': DD.PIVOT['body'], 'head': DD.PIVOT['head'], 'armr': DD.PIVOT['armr'], 'arml': DD.PIVOT['arml'], 'legr': DD.PIVOT['legr'],
              'legl': DD.PIVOT['legl'], 'wingr': DD.PIVOT['wingr'], 'wingl': DD.PIVOT['wingl'], 'tail': DD.PIVOT['tail'], 'fx': (0, 6.0, -9.0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'legr': 'body', 'legl': 'body', 'wingr': 'body', 'wingl': 'body', 'tail': 'body', 'fx': None}
ZL = {'armr': DD.ZA, 'arml': DD.ZA, 'head': DD.ZH, 'body': DD.ZB, 'legr': DD.ZL, 'legl': DD.ZL, 'tail': DD.ZT, 'wingr': DD.ZW, 'wingl': DD.ZW, 'fx': -9.0}
MAKERS = {'zombie': zombie, 'skeleton': skeleton, 'jockey': jockey, 'golem': golem, 'axolotl': axolotl, 'enderman': enderman}
NAMES = {'zombie': 'Doodle Zombie (default)', 'skeleton': 'Doodle Skeleton', 'jockey': 'Doodle Chicken Jockey', 'golem': 'Doodle Iron Golem',
         'axolotl': 'Doodle Axolotl', 'enderman': 'Doodle Enderman'}


def _tex(R, name, pic, keep=None):
    im, k = pic.done(zlib.crc32((R.PREFIX + name).encode()) & 0xffff, alpha=keep); R.tex(name, im); return k


def make(form):
    pics, opt, fx = MAKERS[form]()
    pivot = dict(BASE_PIVOT, **opt.get('pivot', {}))
    R = Rig(f'dm{form[:2]}_', DD.RIG_SCALE, pivot, PARENT, FACES, opt=('fx',))
    def add(part, tex_f, tex_b, pic, mirror=False):
        x0, y0, s = pic.x0, pic.y0, pic.sz
        R._els[part] += card((x0, y0, s), ZL[part], tex_f, tex_b, pivot[part], mirror)
        if mirror: x0 = -(x0 + s)
        R._pts[part] += [(x0 + s * 0.5, y0 + s * 0.5, ZL[part])]
        for poly in pic.edges if hasattr(pic, 'edges') else []:
            pass
    # body, head (and its faces), arms, legs, wings, tail - each card drawn, its back the same shape plain
    for part in ('body',):
        f = pics['body'](); keep = _tex(R, 'body', f); _tex(R, 'body_b', pics['body'](True), keep); add('body', 'body', 'body_b', f)
    hf = pics['head'](); keep = _tex(R, 'face', hf); _tex(R, 'head_b', pics['head'](back=True), keep)
    for fc in FACES: _tex(R, f'face_{fc}', pics['head'](fc), keep)
    add('head', 'FACE', 'head_b', hf)
    if 'eyes' in opt:                                                                                      # (glowing eyes: a card just in front)
        ep = opt['eyes'](); _tex(R, 'eyes', ep)
        R._els['head'].append(DD.eyecard((ep.x0, ep.y0, ep.sz), ZL['head'] - DD.DZ - DZ_EYE, 'eyes', pivot['head']))
    ar = pics['armr'](); _tex(R, 'arm', ar)
    if 'armr' not in opt.get('gone', ()): add('armr', 'arm', 'arm', ar)
    if 'arml' in pics:
        al = pics['arml'](); _tex(R, 'arm_l', al); add('arml', 'arm_l', 'arm_l', al, mirror=True)
    elif 'arml' not in opt.get('gone', ()):
        add('arml', 'arm', 'arm', ar, mirror=True)
    lg = pics['legr'](); _tex(R, 'leg', lg); add('legr', 'leg', 'leg', lg); add('legl', 'leg', 'leg', lg, mirror=True)
    if 'wingr' in pics:
        w = pics['wingr'](); _tex(R, 'wing', w); add('wingr', 'wing', 'wing', w); add('wingl', 'wing', 'wing', w, mirror=True)
    if 'tail' in pics:
        t = pics['tail'](); _tex(R, 'tail', t); add('tail', 'tail', 'tail', t)
    if fx:
        p = fx(); _tex(R, 'fx', p); add('fx', 'fx', 'fx', p)
    R._pts['legr'] = [(2.6, 0.0, ZL['legr'])]; R._pts['legl'] = [(-2.6, 0.0, ZL['legl'])]
    if form == 'enderman': R._pts['legr'] = [(1.6, 0.0, ZL['legr'])]; R._pts['legl'] = [(-1.6, 0.0, ZL['legl'])]
    return R


def poses(R, form):
    P = lambda lift=0.0, **kw: R.ground(kw, lift)
    W = lambda s: dict(legr=limb(1, 0, 12 * s), legl=limb(-1, 0, -12 * s), body=T(0, 0, 3 * s), armr=limb(1, 0, -8 * s), arml=limb(-1, 0, 8 * s))
    atk = {  # each mob's own attack, in the page
        'zombie':   (dict(_face='fierce', armr=limb(1, 0, 20), arml=limb(-1, 0, 20), body=T(0, 0, -6)),                              # GRAB: arms up ...
                     dict(_face='happy', armr=limb(1, 0, -30), arml=limb(-1, 0, -30), body=T(0, 0, 4), head=T(0, 0, 8))),           # ... and a hug-bite
        'skeleton': (dict(_face='fierce', arml=limb(-1, 0, 80), armr=limb(1, 0, 60), head=T(0, 0, -6)),                              # BONE ARROW: drawn ...
                     dict(_face='happy', _show=('fx',), arml=limb(-1, 0, 80), armr=limb(1, 0, 10))),                                 # ... loosed
        'jockey':   (dict(_face='fierce', wingr=limb(1, 0, 40), wingl=limb(-1, 0, 40), armr=limb(1, 0, 40)),                         # FLAP CHARGE
                     dict(_face='happy', _show=('fx',), wingr=limb(1, 0, -20), wingl=limb(-1, 0, -20), body=T(0, 0, 8))),           # EGG TOSS
        'golem':    (dict(_face='fierce', armr=limb(1, 0, 150), arml=limb(-1, 0, 20)),                                               # IRON TOSS: wound up ...
                     dict(_face='fierce', _show=('fx',), armr=limb(1, 0, 60), body=T(0, 0, 8))),                                     # ... flung up
        'axolotl':  (dict(_face='blink', body=T(0, 0, 80), head=T(0, 0, 10)),                                                         # PLAY DEAD (a heal)
                     dict(_face='happy', _show=('fx',), head=T(0, 0, -10), armr=limb(1, 0, 40), arml=limb(-1, 0, 40))),              # BUBBLE
        'enderman': (dict(_face='fierce', armr=limb(1, 0, 30), arml=limb(-1, 0, 30), head=T(0, 0, 10)),                              # STARE ...
                     dict(_face='fierce', _show=('fx',), body=T(0, 0, 14), armr=limb(1, 0, 80))),                                    # ... BLINK (teleport-strike)
    }[form]
    R.POSES.update({
        'idle_a': P(), 'idle_b': P(_face='happy', head=T(0, 0, -6), lift=0.4),
        'walk_0': P(lift=0.4, **W(1)), 'walk_1': P(**W(-1)),
        'atk_up': P(**atk[0]), 'atk': P(**atk[1]),
        'sit_a': P(_face='happy', legr=limb(1, 0, 70), legl=limb(-1, 0, 70)),
        'happy': P(lift=1.2, _face='happy', armr=limb(1, 0, 60), arml=limb(-1, 0, 60), wingr=limb(1, 0, 40), wingl=limb(-1, 0, 40)),
    })
    if form == 'axolotl': R.POSES['atk_up'] = R.ground(R.POSES['atk_up'])
    R.DRAFT = ['idle_a', 'walk_0', 'atk_up', 'atk', 'sit_a', 'happy']
    return R


FORMS = {f: poses(make(f), f) for f in MAKERS}
R = FORMS['zombie']                                         # (the default)
UNLOCKS = {'zombie': 'default (rotten flesh resets him to it)', 'skeleton': 'a bone', 'jockey': 'an egg, after you kill a baby zombie with him out',
           'golem': 'a block of iron', 'axolotl': 'a bucket of axolotl (he gives the bucket back, empty... and the axolotl a hug)', 'enderman': 'an ender pearl'}
