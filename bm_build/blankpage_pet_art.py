"""(3.1 draft, stage 1: art only - not wired) THE BLANK PAGE - the Doodles' own character. With Mr. Capshun and the Gem of Creativity
out (two of your three), and all five Doodles' summoning items on you (the Partner Wheel counts), hand Capshun a piece of paper:
the five Doodles pop out for a moment (a cutscene - the Dragon holds the page, the Cursor clicks "New", the Ink Blot inks, the
Eraser tidies the mistakes, the Speech Bubble names it) and together they draw a new friend - who climbs off the page unfinished.

LOOK  A paper cut-out in the Doodles' crayon style (doodle_dragon_art's Pic: waxy crayon, wobbly outlines, scribbled fill,
      paper flecks), flat and two-sided like Kettle and the Doodle Dragon: a little paper person ~1.1 blocks tall whose BODY is a
      sheet of ruled notebook paper (blue lines, a red margin, a dog-eared corner), a big round head, stick limbs with round
      mitten hands and round shoes. It FILLS ITSELF IN as it ranks up - three stages, the same rig:
  I   ROUGH SKETCH   pencil only: light grey wobbly construction lines that overshoot their corners, a guide-cross on the
                     face and two faint circles for eyes, a stub of pencil in its hand. Half there.
  II  INKED          black crayon-ink outlines over the pencil, a simple face (dot eyes, a smile), the ruled lines inked;
                     one arm and one shoe still pencil; a first scribble of red on its scarf. A ballpoint in its hand.
  III COLOURED       done: crayon colour everywhere - a red scarf, a yellow scribble cowlick, big shiny eyes and pink cheeks,
                     blue shoes, the page's lines bright, a doodled star on its chest; a big red CRAYON in its hand.

RIG   cards, layered like a paper puppet (front to back): armr/arml (z -1.0), prop (the pencil/pen/crayon, -1.3), head (-0.5),
      body (0), legr/legl (+1.1); fx: cage (a scribble cage round a foe), frame (the gold MASTERPIECE frame). Faces per stage:
      happy, blink, focus, wow. Design units: feet at y=0, facing -z, its right +x.
Skins (stage III): '_sh' SHINY "Gold Leaf" (gilt page, gold-and-ink lines, a gold crayon); '_bp' cosmetic "Blueprint" (white
chalk on blueprint blue; per stage: II/III)."""
import math
import zlib
import doodle_dragon_art as DD
from doodle_dragon_art import Pic, wob, ell, sq, bez, card
from fol5_kit import Rig, limb, T

Z = {'armr': -1.0, 'arml': -1.0, 'prop': -1.3, 'head': -0.5, 'body': 0.0, 'legr': 1.1, 'legl': 1.1, 'cage': -10.0, 'frame': -12.0}
BOX = {'body': (-8.0, 2.0, 16.0), 'head': (-8.0, 13.0, 16.0), 'armr': (2.5, 6.0, 8.0), 'legr': (-0.5, -0.5, 8.0), 'prop': (4.0, 3.0, 8.0),
       'cage': (-8.0, -1.0, 16.0), 'frame': (-8.0, -1.0, 16.0)}
PIVOT = {'body': (0, 6.0, 0.0), 'head': (0, 14.6, -0.5), 'armr': (3.8, 12.6, -1.0), 'arml': (-3.8, 12.6, -1.0), 'legr': (2.0, 5.4, 1.1),
         'legl': (-2.0, 5.4, 1.1), 'prop': (7.0, 8.4, -1.3), 'cage': (0, 6.0, -10.0), 'frame': (0, 6.0, -12.0)}
PARENT = {'body': None, 'head': 'body', 'armr': 'body', 'arml': 'body', 'legr': 'body', 'legl': 'body', 'prop': 'armr', 'cage': None, 'frame': None}
FACES = ('happy', 'blink', 'focus', 'wow')
PENCIL, INK = '#8e8e9a', '#22202a'
COL = dict(page='#fffdf4', line='#6aa8e8', margin='#ee5a5a', scarf='#e8343a', hair='#ffd23a', shoe='#3a7ae0', cheek='#ff8db4', star='#ffd23a',
           prop='#e8343a', mitt='#fffdf4')
SKINS = {'_sh': dict(page='#f6e2a0', line='#b8862a', margin='#8a5a10', scarf='#d8a420', hair='#fff0a0', shoe='#a87a1a', cheek='#ffb070', star='#ffffff',
                     prop='#e8b030', mitt='#f6e2a0'),
         '_bp': dict(page='#2a5aa8', line='#c8dcff', margin='#ffffff', scarf='#ffffff', hair='#e0ecff', shoe='#e0ecff', cheek='#9ac0ff', star='#ffffff',
                     prop='#ffffff', mitt='#2a5aa8')}


# ---------------------------------------------------------------------------------------------------- drawing, stage by stage
class Pen:
    """how a stage draws a line: I pencil (light, wobbly, overshooting), II ink, III ink over crayon fill"""
    def __init__(self, pic, stage, c, seed):
        self.p, self.s, self.c, self.seed = pic, stage, c, seed
        self.ink = INK if c['page'] != '#2a5aa8' else '#ffffff'

    def line(self, pts, closed=False, w=None, pencil=False, k=0):
        sd = self.seed + 17 * k
        if self.s == 1 or pencil:
            if closed: pts = pts + pts[:3]                                       # (a sketch overshoots where it closes)
            self.p.crayon(pts, PENCIL, w or 0.2, sd, closed=False, passes=3, jit=0.12)
        else:
            self.p.crayon(pts, self.ink, w or 0.4, sd, closed=closed, passes=2, jit=0.05)

    def fill(self, poly, col, k=0, ang=35):
        if self.s == 3: self.p.blob(poly, col, self.ink, self.seed + 31 * k, ang=ang, over=0.35, ow=0.38)
        elif self.s == 2: self.line(poly, closed=True, k=k)
        else: self.line(poly, closed=True, k=k)

    def page(self, poly, k=0):
        """paper: always filled (it IS paper), outlined per stage"""
        self.p.fill(poly, self.c['page'], self.seed + 5 * k)
        self.line(poly, closed=True, k=k + 1, w=0.36 if self.s > 1 else 0.22)


def _body(stage, c, back=False):
    pic = Pic(BOX['body']); pen = Pen(pic, stage, c, 300 + stage)
    sheet = [(-4.2, 5.2), (4.2, 5.2), (4.2, 12.4), (2.6, 14.0), (-4.2, 14.0)]                 # (the sheet: its top corner, his right, dog-eared)
    pen.page(sheet)
    if back:
        return pic
    for i, y in enumerate((6.6, 8.0, 9.4, 10.8, 12.2)):                                           # (ruled lines)
        x1 = 4.0 if y < 12.2 else 3.0
        if stage == 1: pic.crayon([(-4.0, y), (x1, y)], PENCIL, 0.1, 700 + i, closed=False, passes=1, jit=0.05)
        else: pic.crayon([(-4.0, y), (x1, y)], c['line'], 0.16, 700 + i, closed=False, passes=1, jit=0.03)
    if stage >= 2:
        pic.crayon([(-2.8, 5.3), (-2.8, 13.9)], c['margin'], 0.18, 720, closed=False, passes=1, jit=0.03)
    pen.line([(2.6, 14.0), (2.8, 12.6), (4.2, 12.4)], k=3)                                        # (the fold of the dog-ear)
    # the scarf at the neck
    scarf = [(-3.0, 13.2), (3.0, 13.2), (3.2, 14.6), (-3.2, 14.6)]
    tail = [(1.6, 13.4), (2.8, 13.0), (3.4, 10.6), (2.2, 10.8)]
    if stage == 3:
        pen.fill(scarf, c['scarf'], 5); pen.fill(tail, c['scarf'], 6, ang=70)
        star = [(math.cos(math.radians(90 + 36 * i)) * (1.6 if i % 2 == 0 else 0.7) - 1.0, 9.0 + math.sin(math.radians(90 + 36 * i)) * (1.6 if i % 2 == 0 else 0.7)) for i in range(10)]
        pen.fill(star, c['star'], 7)
    elif stage == 2:
        pen.line(scarf, closed=True, k=5); pic.scribble(scarf, c['scarf'], 20, 731, sp=1.3, w=0.2); pen.line(tail, closed=True, k=6, pencil=True)
    else:
        pen.line(scarf, closed=True, k=5); pen.line([(-4.2, 9.6), (4.2, 9.6)], k=8)               # (a guide line across the middle)
    return pic


def _head(stage, c, face=None, back=False):
    pic = Pic(BOX['head']); pen = Pen(pic, stage, c, 400 + stage)
    C, r = (0.0, 20.0), 4.8
    disc = ell(C[0], C[1], r, r * 0.96, 56)
    pen.page(disc)
    tuft = [(-0.6, 24.4), (-1.6, 26.6), (0.0, 25.4), (0.8, 27.2), (1.2, 25.2), (2.6, 26.0), (1.6, 24.4)]
    if stage == 3: pen.fill(tuft, c['hair'], 3, ang=80)
    elif stage == 2: pen.line(tuft, closed=True, k=3)
    else: pen.line(tuft[:4], k=3)
    if back:
        return pic
    if stage == 1:                                                                              # the guide-cross and two faint eye circles
        pic.crayon([(0.3, 15.6), (-0.3, 24.6)], PENCIL, 0.12, 811, closed=False, passes=1, jit=0.04)
        pic.crayon([(-4.6, 20.6), (4.6, 20.2)], PENCIL, 0.12, 812, closed=False, passes=1, jit=0.04)
        for i, x in enumerate((-1.9, 1.9)):
            pic.crayon(ell(x, 20.6, 0.9, 1.1, 18), PENCIL, 0.14, 820 + i, closed=True, passes=1, jit=0.05)
        pic.crayon(bez((-1.0, 17.8), (0.0, 17.1), (1.0, 17.8), 8), PENCIL, 0.14, 830, closed=False, passes=1, jit=0.04)
        return pic
    ink = pen.ink
    if face == 'blink' or face == 'happy':
        for i, x in enumerate((-1.9, 1.9)):
            up = face == 'happy'
            pic.crayon(bez((x - 1.0, 20.4), (x, 21.4 if up else 19.6), (x + 1.0, 20.4), 8), ink, 0.34, 840 + i, closed=False, passes=2, jit=0.02)
    else:
        big = 1.3 if face == 'wow' else 1.1
        for i, x in enumerate((-1.9, 1.9)):
            if stage == 2: pic.dot((x, 20.6), 0.55, 0.7, ink, 850 + i)
            else:
                pic.dot((x, 20.6), big * 0.85, big, ink, 850 + i); pic.dot((x - 0.3, 21.1), 0.32, 0.32, '#ffffff', 852 + i)
        if face == 'focus':
            for i, s_ in enumerate((-1, 1)):
                pic.crayon([(s_ * 3.0, 22.6), (s_ * 1.0, 22.0)], ink, 0.3, 860 + i, closed=False, passes=2, jit=0.02)
    if face == 'wow':
        pic.dot((0.0, 17.6), 0.6, 0.7, ink, 870)
    else:
        pic.crayon(bez((-1.2, 18.0), (0.0, 16.9 if face != 'focus' else 17.6), (1.2, 18.0), 10), ink, 0.32, 871, closed=False, passes=2, jit=0.02)
    if stage == 3:
        for i, x in enumerate((-3.2, 3.2)): pic.dot((x, 18.6), 0.8, 0.55, c['cheek'], 880 + i)
    return pic


def _arm(stage, c, pencil=False):
    pic = Pic(BOX['armr']); pen = Pen(pic, stage, c, 500 + stage)
    pen.line([(3.8, 12.6), (5.4, 10.4), (6.8, 8.8)], w=0.42 if stage > 1 else 0.22, pencil=pencil)
    mitt = ell(7.0, 8.4, 0.9, 0.9, 20)
    if stage == 3: pen.fill(mitt, c['mitt'], 2)
    else: pen.line(mitt, closed=True, k=2, pencil=pencil)
    return pic


def _leg(stage, c, pencil=False):
    pic = Pic(BOX['legr']); pen = Pen(pic, stage, c, 600 + stage)
    pen.line([(2.0, 5.4), (2.2, 3.0), (2.4, 1.3)], w=0.42 if stage > 1 else 0.22, pencil=pencil)
    shoe = sq(2.9, 0.75, 1.5, 0.75, 3.0, 30)
    if stage == 3: pen.fill(shoe, c['shoe'], 2, ang=10)
    else: pen.line(shoe, closed=True, k=2, pencil=pencil)
    return pic


def _prop(stage, c):
    """in its right hand: I a stub of pencil, II a ballpoint, III a big red crayon (held tip up)"""
    pic = Pic(BOX['prop']); pen = Pen(pic, max(stage, 3) if stage == 3 else 3, c, 900 + stage)
    if stage == 1:
        body = [(6.5, 7.6), (7.5, 7.6), (7.5, 10.6), (6.5, 10.6)]; pic.blob(body, '#ffd23a', INK, 901, over=0.1, ow=0.26)
        pic.blob([(6.5, 10.6), (7.5, 10.6), (7.0, 11.8)], '#f0d0a0', INK, 902, over=0.0, ow=0.22)
    elif stage == 2:
        pic.blob([(6.6, 7.0), (7.4, 7.0), (7.4, 11.2), (6.6, 11.2)], '#3a5ae0', INK, 903, over=0.05, ow=0.24)
        pic.blob([(6.6, 11.2), (7.4, 11.2), (7.0, 12.2)], '#d8d8e0', INK, 904, over=0.0, ow=0.2)
    else:
        pic.blob([(6.2, 6.4), (7.8, 6.4), (7.8, 11.6), (6.2, 11.6)], c['prop'], INK, 905, over=0.2, ow=0.34)
        pic.blob([(6.2, 11.6), (7.8, 11.6), (7.0, 13.4)], c['prop'], INK, 906, over=0.1, ow=0.3)
        pic.crayon([(6.2, 8.0), (7.8, 8.0)], INK, 0.22, 907, closed=False, passes=1)            # (the paper wrapper's band)
    return pic


def _cage(stage, c):
    """SKETCH TRAP: scribbled loops round a foe - pencil (I), ink (II), crayon colours (III)"""
    pic = Pic(BOX['cage']); col = PENCIL if stage == 1 else INK
    for i in range(7):
        y = 1.0 + i * 2.0; w = 5.5 - abs(i - 3) * 0.5
        pts = [(math.cos(t) * w, y + math.sin(t) * 0.9 + t * 0.15) for t in [k * 0.4 for k in range(17)]]
        pic.crayon(pts, col if stage < 3 else (c['scarf'], c['line'], c['hair'], c['shoe'])[i % 4], 0.35, 950 + i, closed=False, passes=2, jit=0.1)
    return pic


def _frame(c):
    """MASTERPIECE: a gold crayon picture frame drawn round a foe - when it's finished, the foe's 'framed' (stunned, hung up)"""
    pic = Pic(BOX['frame'])
    for i, (x0, y0, x1, y1) in enumerate(((-6.8, 12.6, 6.8, 14.2), (-6.8, -0.2, 6.8, 1.4), (-6.8, -0.2, -5.2, 14.2), (5.2, -0.2, 6.8, 14.2))):
        pic.blob([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], '#ffd23a', '#b8862a', 980 + 3 * i, over=0.1, ow=0.32, amp=0.06)   # (four crayon bars: hollow)
    for i, (x, y) in enumerate(((-5.9, 13.5), (5.9, 13.5), (-5.9, 0.5), (5.9, 0.5))): pic.dot((x, y), 0.8, 0.8, '#ffe890', 982 + i, line='#b8862a')
    return pic


def _done(pic, seed, keep=None):
    im, k = pic.done(seed, alpha=keep); return im, k


def make(stage):
    R = Rig(f'bp{stage}_', DD.RIG_SCALE, PIVOT, PARENT, FACES, opt=('cage', 'frame'))

    def two(name, front, back, c, sfx=''):
        f, keep = _done(front, zlib.crc32(name.encode()) & 0xffff); b, _ = _done(back, (zlib.crc32(name.encode()) + 1) & 0xffff, keep)
        R.tex(name + sfx, f); R.tex(name + '_b' + sfx, b)
    for sfx, c in [('', COL)] + ([(s, dict(COL, **v)) for s, v in SKINS.items()] if stage >= 2 else []):
        if stage == 2 and sfx == '_sh': continue
        two('body', _body(stage, c), _body(stage, c, True), c, sfx)
        two('face', _head(stage, c), _head(stage, c, back=True), c, sfx)
        for f in FACES: R.tex(f'face_{f}{sfx}', _done(_head(stage, c, f), 77)[0])
        R.tex('arm' + sfx, _done(_arm(stage, c), 11)[0]); R.tex('arm_p' + sfx, _done(_arm(stage, c, pencil=True), 12)[0])
        R.tex('leg' + sfx, _done(_leg(stage, c), 13)[0]); R.tex('leg_p' + sfx, _done(_leg(stage, c, pencil=True), 14)[0])
        R.tex('prop' + sfx, _done(_prop(stage, c), 15)[0]); R.tex('cage' + sfx, _done(_cage(stage, c), 16)[0])
        if sfx:
            names = ['body', 'body_b', 'face', 'face_b', 'arm', 'arm_p', 'leg', 'leg_p', 'prop', 'cage'] + [f'face_{f}' for f in FACES]
            R.skin(sfx, {n: n + sfx for n in names})
    R.tex('frame', _done(_frame(COL), 17)[0])

    def addcard(part, front, back, mirror=False):
        src = 'armr' if part.startswith('arm') else 'legr' if part.startswith('leg') else part
        els = card(BOX[src], Z[part], front, back, PIVOT[part], mirror)
        R._els[part] += els
        x0, y0, s = BOX[src]
        if mirror: x0 = -(x0 + s)
        R._pts[part] += [(x0, y0, Z[part]), (x0 + s, y0 + s, Z[part])]
    addcard('body', 'body', 'body_b')
    addcard('head', 'FACE', 'face_b')
    # stage II: its left arm and left shoe still pencil - the last bits to be inked
    addcard('armr', 'arm', 'arm'); addcard('arml', 'arm_p' if stage == 2 else 'arm', 'arm_p' if stage == 2 else 'arm', mirror=True)
    addcard('legr', 'leg', 'leg'); addcard('legl', 'leg_p' if stage == 2 else 'leg', 'leg_p' if stage == 2 else 'leg', mirror=True)
    addcard('prop', 'prop', 'prop'); addcard('cage', 'cage', 'cage'); addcard('frame', 'frame', 'frame')
    # the low points (its shoes) for grounding: the shoe's sole
    R._pts['legr'] = [(2.9, 0.0, Z['legr'])]; R._pts['legl'] = [(-2.9, 0.0, Z['legl'])]

    def P(lift=0.0, **kw):
        return R.ground(kw, lift)
    W = lambda s: dict(legr=limb(1, 0, 14 * s), legl=limb(-1, 0, -14 * s), armr=limb(1, 0, 10 - 14 * s), arml=limb(-1, 0, 10 + 14 * s), body=T(0, 0, 3 * s))
    R.POSES.update({
        'idle_a': P(armr=limb(1, 0, 6), arml=limb(-1, 0, 10), head=T(0, 0, 4)),
        'idle_b': P(_face='happy', lift=0.6, armr=limb(1, 0, 60), arml=limb(-1, 0, 60), head=T(0, 0, -6)),
        'idle_c': P(_face='wow', arml=limb(-1, 0, 120), head=T(0, 0, 10)),                                   # (looking itself over: a hand up)
        'walk_0': P(lift=0.4, **W(1)), 'walk_1': P(**W(-1)),
        # sitting: folded in half like a sheet of paper - legs out flat, then curled up dozing on its own page
        'sit_a': P(_face='happy', legr=limb(1, 0, 70), legl=limb(-1, 0, 70), armr=limb(1, 0, 30), arml=limb(-1, 0, 30)),
        'sit_b': P(_face='blink', body=T(0, 0, 70), head=T(0, 0, 10), legr=limb(1, 0, 40), legl=limb(-1, 0, 20), armr=limb(1, 0, 100), arml=limb(-1, 0, -20)),
        # SKETCH TRAP: it draws in the air - scribbled loops cage the foe (slowed, then held)
        'sketch': P(_face='focus', _show=('cage',), armr=limb(1, 0, 110), arml=limb(-1, 0, 20), head=T(0, 0, -8)),
        # SCRIBBLE: the crayon raised ... and scribbled hard at the foe (a flurry of hits)
        'scrib_up': P(_face='focus', armr=limb(1, 0, 160), arml=limb(-1, 0, 30), body=T(0, 0, -6)),
        'scrib': P(_face='wow', armr=limb(1, 0, 40), arml=limb(-1, 0, -10), body=T(0, 0, 10), legr=limb(1, 0, 20), legl=limb(-1, 0, -10)),
        # REVISE (a heal): it rubs out its own scuffs - flips over, a whole new sheet
        'revise': P(_face='happy', body=T(0, 160), head=T(0, 20)),
        # MASTERPIECE (charged): arms flung wide - a gold frame drawn round the foe
        'master': P(_face='happy', _show=('frame',), lift=0.8, armr=limb(1, 0, 140), arml=limb(-1, 0, 140), legr=limb(1, 0, 20), legl=limb(-1, 0, 20)),
        'hurt': P(_face='wow', body=T(0, 0, 14), head=T(0, 0, 16), armr=limb(1, 0, 70), arml=limb(-1, 0, 70)),
    })
    R.DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'sit_a', 'sit_b', 'sketch', 'scrib_up', 'scrib', 'revise', 'master', 'hurt']
    return R


RIGS = {s: make(s) for s in (1, 2, 3)}
R = RIGS[3]
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'head': 'head'}
SHINY = 'Shiny Gold Leaf'
SKIN_NAMES = {'_sh': 'SHINY Gold Leaf', '_bp': 'Blueprint (cosmetic)'}
