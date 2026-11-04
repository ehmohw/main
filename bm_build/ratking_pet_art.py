"""(3.0 draft) THE RAT KING, AS A FOLLOWER (art) - the Keeper of Bonds' counterpart: where the Keeper weaves every bond you've
made, the Rat King keeps count of them (a debt is a bond too, if you ask him). Found once the 50 other followers are met: the
King's Coin, the Compass of Bonds' dark twin, points DOWN - to his Counting House at the bottom of the world, under the Loom
Sanctuary (as above, so below). The wiring is a phase-to-be; this module is only the rig.

LOOK  The heist's Rat King (ratking_art: a great, fat, upright rat in a gold crown, a crimson cape with an ermine collar, a
      blue sash and a belt with a gold buckle, a sceptre crowned with a wheel of golden cheese, a gold-ringed tail) at
      companion size - RIG_SCALE 0.48: ~1.55 blocks to his crown's orb, a head shorter than you (his ego is the tallest
      thing about him). The same geometry part for part (built by ratking_art's own builders), with his own textures (rkf_:
      the wardrobe recolours his cape and sash, the shiny paints his fur and gold - never the boss's), and a FACE: the
      boss's glowing red glare is his 'focus' face only (the Royal Decree, a fight's serious moments); at rest his eyes are
      beady rubies with a glint, under a haughty brow. Faces (head_x<face>): happy (smug crescents), blink, sleepy
      (half-lidded), surprised (wide, brows up), hurt (screwed shut), focus (the boss's glare). One new part: a gold COIN
      in his left paw (the King's Cut, a gift, counting his hoard while he sits) - shown only when a pose sets _coin.

RIG   ratking_art's 13 parts (body root; head, jaw, crown; armr + sceptre, arml + coin; legr, legl; cape; tail1-3), the
      same pivots. Design units: feet at y=0, facing -z, his right is +x.

POSES rigpet's set - idle_a/b/c, walk_0-3, run_0-3, jump, swim_0-7, sit_a/sit_b, happy, hurt, tired (fainted), rise - and his
      own: swat_up / swat (the sceptre: hauled back, brought down), decree_up / decree (THE ROYAL DECREE: rearing up, a
      screech - the sceptre slammed into the floor), whistle_a / whistle (THE COURT: two claws to his lips, a whistle - then
      the sceptre pointed: "Get him!"), cut_a / cut (THE KING'S CUT: a coin snatched out of the air, then bitten to test it),
      gift (a coin held out with a little bow - a loan, with interest), bow (a grand courtly bow, the cape swept back),
      throne_a / throne_b (the encounter: lounging on his throne of coins, chin on his paw; then drumming his claws)."""
import math
import random
from PIL import Image, ImageDraw

import rigkit as RK
from rigkit import qs, shrink
import ratking_art as RA

PREFIX = 'rkf_'
RIG_SCALE = 0.48
SCALE = RIG_SCALE
PIVOT = dict(RA.PIVOT, coin=(-12.4, 13.4, -6.6))
PARENT = dict(RA.PARENT, coin='arml')
PARTS = tuple(PIVOT)
PART_K = dict(RA.PART_K)
JOINTS = {}
FACES = ('happy', 'blink', 'sleepy', 'surprised', 'hurt', 'focus')
FACE_MAP = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'hurt', 'sleepy': 'sleepy', 'blink': 'blink', 'squint': 'happy', 'serious': 'focus'}
LOOK_TEX = ('rkf_velvet', 'rkf_sash')            # (the wardrobe's Cape: what a look recolours)


def HIDDEN(p, pose):
    if p == 'coin': return not pose.get('_coin')
    return p in pose.get('_hide', ())


def model_name(p, pose=None, suffix=''):
    face = f'_x{pose["_face"]}' if pose and p == 'head' and pose.get('_face') else ''
    return f'{PREFIX}{p}{face}{suffix}'


# ---------------------------------------------------------------------------------------------------- textures
def _eyef():
    """his eyes at rest: a beady ruby, a dark pupil low in it, a white glint top-left (unlit)"""
    im = RA._base('#b0142a', 19, 5); px = im.load()
    for x in range(16):
        for y in range(16):
            r = math.hypot(x - 8.5, y - 9.0)
            if r < 4.6: px[x, y] = (54, 6, 14, 255)
            elif r < 6.2: px[x, y] = (150, 16, 34, 255)
    for (x, y) in ((4, 3), (5, 3), (4, 4), (5, 4), (6, 4), (5, 5), (11, 11)): px[x, y] = (255, 246, 236, 255)
    return im


def _coin():
    """a gold coin: a rim, a raised crown on its face, a glint"""
    im = RA._gold(15); d = ImageDraw.Draw(im); dk = RA._rgb('#9a6a10') + (255,); hi = RA._rgb('#fff2a0') + (255,)
    d.rectangle((0, 0, 15, 15), outline=dk)
    for (x0, y0, x1, y1) in ((4, 9, 11, 10), (4, 6, 4, 9), (7, 5, 8, 9), (11, 6, 11, 9)): d.rectangle((x0, y0, x1, y1), fill=dk)
    d.point((3, 2), fill=hi); d.point((4, 2), fill=hi)
    return im


TEX = dict(RA.TEX, eyef=_eyef, coin=_coin)


def tex_name(m):
    return f'{PREFIX}{m}'


def textures():
    """{name: 16 x 16 RGBA} (assets/bm/textures/block)"""
    return {tex_name(m): f() for m, f in TEX.items()}


# ---------------------------------------------------------------------------------------------------- the head and its faces
def _head(face=None):
    """ratking_art's head - the skull, snout, brow, nose, teeth, ears and whiskers - with his face on it"""
    E, M = RA.E, RA.M
    H = [E((-7, 33.5, -8), (7, 44, 5), 'fur'), E((-4.6, 34.4, -15), (4.6, 40.2, -8), 'furlt'),
         E((-3.4, 40, -12), (3.4, 42.5, -7.5), 'fur'), E((-1.6, 37.4, -16.3), (1.6, 40.2, -15), 'nose'),
         E((-1.7, 32.8, -14.6), (-0.15, 34.6, -14.1), 'tooth'), E((0.15, 32.8, -14.6), (1.7, 34.6, -14.1), 'tooth')]
    for sx in (1, -1):
        H += [M(sx, 4.5, 12.0, 46.5, 47.5, -1.6, 1.4, 'fur'), M(sx, 5.0, 11.5, 40.5, 47.0, -1.6, 1.4, 'fur'),
              M(sx, 6.0, 10.5, 41.5, 46.2, -1.9, -1.6, 'skin'), M(sx, 11.5, 12.5, 41.5, 46.5, -1.6, 1.4, 'fur'),
              M(sx, 4.6, 11.0, 36.4, 36.7, -12.0, -11.7, 'whisker', rot=('z', 8, (4.6, 36.5, -11.8))),
              M(sx, 4.6, 10.4, 37.4, 37.7, -11.6, -11.3, 'whisker', rot=('z', -6, (4.6, 37.5, -11.4))),
              M(sx, 4.6, 9.6, 35.4, 35.7, -11.2, -10.9, 'whisker', rot=('z', 20, (4.6, 35.5, -11.0)))]
    zf, zb = -8.4, -7.95                          # (the eyes stand just proud of the skull's front, beside the snout)
    a, b, y0, y1 = 3.9, 6.9, 39.6, 42.4           # (the eye's box: x from a to b on each side, y0 to y1)
    cx, cy = (a + b) / 2, (y0 + y1) / 2
    BR = (42.7, 43.5)                             # (the brow's band, over the eye)
    def brow(tilt, lift=0.0, w=(3.4, 7.4)):
        return M(sx, w[0], w[1], BR[0] + lift, BR[1] + lift, -8.8, -8.1, 'brow', rot=('z', tilt, (cx, (BR[0] + BR[1]) / 2 + lift, -8.4)))
    def lid(): return M(sx, a, b, y0, y1, zf + 0.05, zb, 'fur')
    def line(x0, x1, ya, yb, tilt=0.0, ox=None):
        return M(sx, x0, x1, ya, yb, zf - 0.1, zb, 'brow', rot=('z', tilt, (ox if ox is not None else (x0 + x1) / 2, (ya + yb) / 2, -8.4)) if tilt else None)
    for sx in (1, -1):
        if face is None:                          # beady rubies under a haughty brow (its outer end a touch low)
            H += [M(sx, a, b, y0, y1, zf, zb, 'eyef', uv={'north': [0, 0, 16, 16]}), brow(-8)]
        elif face == 'focus':                     # the boss's own: a red glare that glows, under a scowl
            H += [M(sx, a, b, y0 + 0.2, y1 - 0.3, zf, zb, 'eye'), brow(18, -0.5)]
        elif face == 'happy':                     # smug crescents (a dark arch), the brow lifted
            H += [lid(), line(a + 0.1, a + 1.3, y0 + 0.5, y0 + 1.9, -40), line(a + 0.9, b - 0.9, y1 - 1.2, y1 - 0.4),
                  line(b - 1.3, b - 0.1, y0 + 0.5, y0 + 1.9, 40), brow(-12, 0.6)]
        elif face == 'blink':                     # shut: a lid of fur, a dark lash line across it, curving down at the ends
            H += [lid(), line(a + 0.5, b - 0.5, cy - 0.3, cy + 0.3), line(a, a + 0.8, cy - 0.6, cy, 30), line(b - 0.8, b, cy - 0.6, cy, -30), brow(-5)]
        elif face == 'sleepy':                    # half-lidded: the lid down over the top of the ruby
            H += [M(sx, a, b, y0, cy, zf, zb, 'eyef', uv={'north': [0, 6, 16, 16]}), M(sx, a, b, cy, y1, zf - 0.05, zb, 'fur'),
                  line(a, b, cy - 0.2, cy + 0.25), brow(-14, -0.3)]
        elif face == 'surprised':                 # wide: the rubies bigger, the brows flown up and flat
            H += [M(sx, a - 0.3, b + 0.2, y0 - 0.4, y1 + 0.2, zf - 0.05, zb, 'eyef', uv={'north': [0, 0, 16, 16]}), brow(-3, 0.5)]
        elif face == 'hurt':                      # screwed shut: a '>' a side, the brows knotted
            H += [lid(), line(a + 0.3, b - 0.3, cy + 0.1, cy + 0.7, -20), line(a + 0.3, b - 0.3, cy - 0.7, cy - 0.1, 20), brow(22, -0.3)]
        else:
            raise KeyError(face)
    return H


def _coin_part():
    x, y, z = PIVOT['coin']
    return [RA.E((x - 1.9, y - 1.9, z - 0.35), (x + 1.9, y + 1.9, z + 0.35), 'coin', uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}),
            RA.E((x - 1.3, y - 2.3, z - 0.3), (x + 1.3, y + 2.3, z + 0.3), 'golddk'), RA.E((x - 2.3, y - 1.3, z - 0.3), (x + 2.3, y + 1.3, z + 0.3), 'golddk')]


_RAW = {}


def _build():
    if _RAW: return _RAW
    RA._rs.seed(31)
    def mk(part, f, *a):
        RA._PV[0] = PIVOT[part]; return f(*a)
    _RAW.update(body=mk('body', RA._body), jaw=mk('jaw', RA._jaw), crown=mk('crown', RA._crown),
                armr=mk('armr', RA._arm, 1), arml=mk('arml', RA._arm, -1), sceptre=mk('sceptre', RA._sceptre),
                legr=mk('legr', RA._leg, 1), legl=mk('legl', RA._leg, -1), cape=mk('cape', RA._cape),
                tail1=mk('tail1', RA._tail, 1), tail2=mk('tail2', RA._tail, 2), tail3=mk('tail3', RA._tail, 3), coin=mk('coin', _coin_part))
    _RAW['head'] = mk('head', _head)
    for f in FACES:
        _RAW[f'head_x{f}'] = mk('head', _head, f)
    return _RAW


def models():
    """{model id: (textures, elements)} - one per part (and one per face of the head)"""
    out = {}
    for name, els in _build().items():
        part = name.split('_x')[0]
        k = PART_K.get(part, 1.0)
        els = shrink(els, k) if k != 1.0 else els
        fe = []
        for e in els:
            e = dict(e, faces={f: dict(fc, texture='#' + tex_name(fc['texture'][1:])) for f, fc in e['faces'].items()})
            for v in e['from'] + e['to']:
                assert -16 <= v <= 32, (name, e['from'], e['to'])
            fe.append(e)
        used = sorted({fc['texture'][1:] for e in fe for fc in e['faces'].values()})
        out[f'{PREFIX}{name}'] = ({t: f'bm:block/{t}' for t in used}, fe)
    return out


# ---------------------------------------------------------------------------------------------------- posing
limb, T, CROWN = RA.limb, RA.T, RA.CROWN
s_ = math.sin


def tail(sway=0.0, lift=0.0, curl=0.0):
    """the tail: swung (sway), lifted at the root (lift), and curled round at the tip (curl: toward his right)"""
    return dict(tail1=T(-10 + lift, sway), tail2=T(8 + lift * 0.5, sway * 1.2 + curl * 0.5), tail3=T(-14 + lift * 0.3, sway * 1.4 + curl))


def ground(p, parts=('legr', 'legl')):
    return RA.ground(p, parts)


def lowest(p, parts=RA.PARTS):
    return RA.lowest(p, parts)


def clear(p, k=0.3):
    return RA._tail_clear(p, k)


def seat(p, parts=('legr', 'legl', 'body', 'cape')):
    """set down: the lowest of these on the floor"""
    return clear(ground(p, parts), 0.2)


def _sitting(**kw):
    """on his haunches, the legs forward - the base every seated pose shares"""
    p = dict(body=T(-10), head=T(8), jaw=T(0), crown=CROWN, legr=limb(1, 45, 18, -6), legl=limb(-1, 45, 18, -6),
             armr=limb(1, 30, 6), arml=limb(-1, 34, 10, -10), sceptre=T(-40), cape=T(10), **tail(-60, -18, 50))
    p.update(kw)
    return seat(p)


def _poses():
    P = {}
    # ---- at rest (proud: chest out, the sceptre upright, the left paw at his belly)
    P['idle_a'] = clear(ground(dict(body=T(0), head=T(2, -4), jaw=T(0), crown=CROWN, armr=limb(1, 6, 4), arml=limb(-1, 22, 8, -10),
                                    sceptre=T(-6), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-3), **tail(-14))))
    P['idle_b'] = clear(ground(dict(body=T(-3), head=T(-6, 8, 3), jaw=T(5), crown=CROWN, armr=limb(1, 6, 4), arml=limb(-1, 26, 10, -10),
                                    sceptre=T(-6), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-2), **tail(14), _off=(0, 0.5, 0))))
    # (the third beat: admiring his own claws, the sceptre tucked under his arm)
    P['idle_c'] = clear(ground(dict(_face='happy', body=T(2, 10), head=T(14, 18), jaw=T(0), crown=CROWN, armr=limb(1, 14, 10),
                                    arml=limb(-1, 74, 4, 40), sceptre=T(-20), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-3), **tail(-22, 4))))
    # ---- moving (a heavy, rolling waddle; running, a lean and a scurry, the cape streaming)
    for k in range(4):
        ph = math.pi * k / 2; sw = s_(ph)
        p = ground(dict(body=T(6, 6 * sw, 5 * sw), head=T(-4, -6 * sw, -4 * sw), jaw=T(0), crown=CROWN,
                        armr=limb(1, 10 - 16 * sw, 6), arml=limb(-1, 18 + 22 * sw, 10), sceptre=T(-8 + 6 * sw),
                        legr=limb(1, 24 * sw, 3), legl=limb(-1, -24 * sw, 3), cape=T(-8 - 4 * abs(sw), 0, -4 * sw), **tail(22 * sw, 4)))
        p['_off'] = (p['_off'][0], p['_off'][1] + 0.7 * abs(math.cos(ph)), p['_off'][2]); P[f'walk_{k}'] = clear(p)
        p = ground(dict(body=T(24, 8 * sw, 4 * sw), head=T(-20, -8 * sw), jaw=T(8), crown=T(-6, 0, -8),
                        armr=limb(1, 30 - 40 * sw, 14), arml=limb(-1, 30 + 40 * sw, 16), sceptre=T(-30 + 10 * sw),
                        legr=limb(1, 46 * sw, 4), legl=limb(-1, -46 * sw, 4), cape=T(-34 - 6 * abs(sw), 0, -6 * sw), **tail(14 * sw, 20)))
        p['_off'] = (p['_off'][0], p['_off'][1] + 1.6 * abs(math.cos(ph)), p['_off'][2]); P[f'run_{k}'] = clear(p)
    P['jump'] = clear(dict(_face='surprised', body=T(-8), head=T(-12), jaw=T(20), crown=T(-8, 0, -12), armr=limb(1, 120, 30), arml=limb(-1, 110, 34),
                           sceptre=T(-10), legr=limb(1, 50, 6), legl=limb(-1, 40, 6), cape=T(-20), **tail(0, 30), _off=(0, 6.0, 0)))
    for i in range(8):                            # (swimming: laid forward, his chin and crown held high and dry, paddling)
        ph = 2 * math.pi * i / 8
        P[f'swim_{i}'] = dict(body=T(58), head=T(-56), jaw=T(0), crown=CROWN, armr=limb(1, 120 + 30 * s_(ph), 16), arml=limb(-1, 120 - 30 * s_(ph), 16),
                              sceptre=T(-70), legr=limb(1, -40 + 30 * s_(ph), 6), legl=limb(-1, -40 - 30 * s_(ph), 6), cape=T(-56),
                              **tail(18 * s_(ph), 30), _off=(0, 5.0 + 0.6 * s_(2 * ph), 0))
    # ---- sitting (on his haunches, the sceptre across his lap; then counting his hoard, a coin from paw to paw)
    P['sit_a'] = _sitting(armr=limb(1, 40, 4, -30), sceptre=T(-74, 0, 0))
    P['sit_b'] = _sitting(_coin=True, _face='happy', head=T(18, 12), armr=limb(1, 40, 4, -30), sceptre=T(-74), arml=limb(-1, 58, 4, 30))
    P['throne_a'] = _sitting(_face='sleepy', body=T(-14, -8), head=T(6, 14, 10), armr=limb(1, 22, 30), sceptre=T(-10),
                             arml=limb(-1, 120, 10, 70), cape=T(18))       # (lounging, chin on his left paw: "Well?")
    P['throne_b'] = _sitting(body=T(-12, 6), head=T(-2, -10), jaw=T(6), armr=limb(1, 22, 30), sceptre=T(-10), arml=limb(-1, 38, 22, -20), cape=T(16))
    P['happy'] = clear(ground(dict(_face='happy', body=T(-8), head=T(-14, 0, 8), jaw=T(22), crown=T(0, 0, -12), armr=limb(1, 150, 20),
                                   arml=limb(-1, 60, 40), sceptre=T(10), legr=limb(1, 6, 6), legl=limb(-1, -6, 6), cape=T(4), **tail(30, 24), _off=(0, 2.0, 0))))
    P['hurt'] = clear(ground(dict(_face='hurt', body=T(-12, 8, -6), head=T(-18, -10, 8), jaw=T(22), crown=T(0, 0, -14), armr=limb(1, 20, 30),
                                  arml=limb(-1, 30, 40), sceptre=T(-14), legr=limb(1, -8, 4), legl=limb(-1, 10, 4), cape=T(6), **tail(18, 16))))
    # fainted: sat down hard, slumped back, the crown slid over one eye and the sceptre dropped across his feet
    P['tired'] = _sitting(_face='blink', body=T(-26, 10, 8), head=T(26, 20, 16), jaw=T(14), crown=T(10, 0, -24), armr=limb(1, 16, 40),
                          arml=limb(-1, 10, 40), sceptre=T(-80, 20), legr=limb(1, 52, 24), legl=limb(-1, 46, 28), cape=T(26), _o_crown=(1.6, -1.6, -1.0))
    P['rise'] = clear(ground(dict(_face='sleepy', body=T(26), head=T(-10), jaw=T(4), crown=T(4, 0, -16), armr=limb(1, 46, 8), sceptre=T(-38),
                                  arml=limb(-1, 50, 20), legr=limb(1, 60, 6), legl=limb(-1, -10, 6), cape=T(-16), **tail(-10, 0))))
    # ---- SCEPTRE SWAT: hauled back over his shoulder, then brought down in front of him
    P['swat_up'] = clear(ground(dict(_face='focus', body=T(-10, -26, -4), head=T(-6, 18), jaw=T(10), crown=CROWN, armr=limb(1, 168, 16), arml=limb(-1, 46, 28),
                                     sceptre=T(170), legr=limb(1, -14, 4), legl=limb(-1, 18, 4), cape=T(-6), **tail(-26, 10))))
    P['swat'] = clear(ground(dict(_face='focus', body=T(22, 18, 4), head=T(-10, -12), jaw=T(24), crown=CROWN, armr=limb(1, 72, 4, -10), arml=limb(-1, -16, 30),
                                  sceptre=T(-160), legr=limb(1, 26, 4), legl=limb(-1, -22, 4), cape=T(-18), **tail(24, 14))))
    # ---- THE ROYAL DECREE: rearing up, both paws high, a screech - then the sceptre slammed into the floor
    P['decree_up'] = clear(ground(dict(_face='focus', body=T(-16), head=T(-24), jaw=T(38), crown=CROWN, armr=limb(1, 160, 26), arml=limb(-1, 150, 34),
                                       sceptre=T(175), legr=limb(1, 6, 8), legl=limb(-1, 6, 8), cape=T(10), **tail(0, 28))))
    P['decree'] = clear(ground(dict(_face='focus', body=T(30, 6), head=T(-20, -4), jaw=T(26), crown=CROWN, armr=limb(1, 52, 6), arml=limb(-1, 40, 30),
                                    sceptre=T(70), legr=limb(1, 44, 10), legl=limb(-1, 30, 12), cape=T(-26), **tail(-10, -4))))
    # ---- THE COURT: two claws to his lips (a whistle) ... then the sceptre levelled at the foe: "Get him!"
    P['whistle_a'] = clear(ground(dict(_face='blink', body=T(-4, -10), head=T(-14, 6), jaw=T(4), crown=CROWN, armr=limb(1, 14, 8), sceptre=T(-8),
                                       arml=limb(-1, 82, -4, 20), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-2), **tail(10, 6))))
    P['whistle'] = clear(ground(dict(_face='focus', body=T(10, 16), head=T(-8, -14), jaw=T(30), crown=CROWN, armr=limb(1, 94, 4, -10), sceptre=T(-90),
                                     arml=limb(-1, 30, 36), legr=limb(1, 22, 4), legl=limb(-1, -18, 4), cape=T(-12), **tail(-20, 12))))
    # ---- THE KING'S CUT: a coin snatched out of the air ... then bitten, to test it
    P['cut_a'] = clear(ground(dict(_coin=True, _face='surprised', body=T(-6, -8), head=T(-24, 10), jaw=T(10), crown=CROWN, armr=limb(1, 10, 6),
                                   sceptre=T(-8), arml=limb(-1, 150, 16, 10), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-2), **tail(-10, 10))))
    P['cut'] = clear(ground(dict(_coin=True, _face='happy', body=T(4, -6), head=T(10, 8), jaw=T(18), crown=CROWN, armr=limb(1, 10, 6), sceptre=T(-8),
                                 arml=limb(-1, 76, 26, 60), legr=limb(1, 2, 2), legl=limb(-1, -2, 2), cape=T(-3), **tail(16, 6))))
    # ---- A LOAN, WITH INTEREST (out of a fight): a coin held out to you with a little bow
    P['gift'] = clear(ground(dict(_coin=True, _face='happy', body=T(18), head=T(-12, -6), jaw=T(8), crown=CROWN, armr=limb(1, 10, 10), sceptre=T(-14),
                                  arml=limb(-1, 70, 4, 10), legr=limb(1, 14, 2), legl=limb(-1, -10, 2), cape=T(-10), **tail(-14, 6))))
    # ---- a grand courtly bow (his greeting; the end of the audience): bent low, the sceptre swept wide, the left paw at his heart
    P['bow'] = clear(ground(dict(_face='blink', body=T(34), head=T(10), jaw=T(0), crown=T(0, 0, -6), armr=limb(1, 40, 60, -20), sceptre=T(-30),
                                 arml=limb(-1, 50, -14, 20), legr=limb(1, 30, 2), legl=limb(-1, -24, 2), cape=T(-30), **tail(0, 20))))
    return P


POSES = _poses()
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'walk_1', 'run_0', 'run_1', 'jump', 'swim_0', 'swim_2', 'sit_a', 'sit_b', 'throne_a', 'throne_b',
         'happy', 'hurt', 'tired', 'rise', 'swat_up', 'swat', 'decree_up', 'decree', 'whistle_a', 'whistle', 'cut_a', 'cut', 'gift', 'bow']

# ---- the display case and the doll (FIT: measure from the built rig, as tools/preview/keeper.py 'fit'); Cecil's doll: the default warp
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}


# ---------------------------------------------------------------------------------------------------- the shiny (drawn: his fur and gold)
# Shiny "Moonlit Albino": white fur, pink eyes and skin, a platinum crown and sceptre, a cape of midnight sapphire, a wheel of
# pale moon cheese. phase138's SHINY_TEX paints the fur and metal; the velvet and sash take the shiny look's own palette.
SHINY_LOOK = ('Shiny Moonlit Albino', ('#0a1030', '#3a4ab0', '#c8d4ff'), 'white')
def _shiny_fur(col, seed, dark, light): return lambda: RA._fur(col, seed, dark, light)
SHINY_TEX = {'fur': _shiny_fur('#ece6e2', 1, '#c8bcb8', '#ffffff'), 'furdk': _shiny_fur('#d4ccc8', 2, '#b0a4a0', '#ece6e2'),
             'furlt': _shiny_fur('#fbf6f2', 3, '#dcd2cc', '#ffffff'), 'belly': _shiny_fur('#fff4f2', 4, '#eadad6', '#ffffff'),
             'skin': lambda: RA._flat('#f2a8b8', 5), 'nose': lambda: RA._flat('#ff8aa8', 6, 4),
             'gold': lambda: RA._gold(11, '#6a7080', '#c8ccd8', '#ffffff'), 'golddk': lambda: RA._gold(12, '#4a505c', '#9aa0b0', '#e0e4ee'),
             'coin': lambda: _coin_tinted(), 'cheese': lambda: _moon_cheese(), 'ruby': lambda: RA._base('#3a6aff', 33, 6),
             'eyef': lambda: _eyef_pink(), 'eye': lambda: RA._base('#ff5ab0', 9, 4)}


def _coin_tinted():
    im = _coin().convert('RGB'); px = im.load()
    for x in range(16):
        for y in range(16):
            r, g, b = px[x, y]; v = (r + g + b) // 3; px[x, y] = (v, v + 4, min(255, v + 14))
    return im.convert('RGBA')


def _moon_cheese():
    im = RA._base('#e8ecf4', 77, 6); d = ImageDraw.Draw(im); h = RA._rgb('#a8b4cc') + (255,); rind = RA._rgb('#8a96b0') + (255,)
    for (x, y, r) in ((4, 4, 2), (11, 6, 1), (6, 11, 2), (12, 12, 1), (9, 2, 1)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=h)
    d.rectangle((0, 0, 15, 0), fill=rind); d.rectangle((0, 15, 15, 15), fill=rind)
    return im


def _eyef_pink():
    im = _eyef().convert('RGB'); px = im.load()
    for x in range(16):
        for y in range(16):
            r, g, b = px[x, y]
            if r > 240 and g > 230: continue
            px[x, y] = (min(255, r + 70), int(g * 0.6 + 30), min(255, int(b * 1.4 + 60)))
    return im.convert('RGBA')


def shiny_textures():
    """(previews) every rkf_ texture as the shiny look would show it - the drawn ones, the cloth through the look's palette"""
    import phase99 as P99
    base = textures()
    out = P99._recolour({tex_name(k): base[tex_name(k)] for k in ('velvet', 'sash')}, SHINY_LOOK[1])
    out.update({tex_name(k): f() for k, f in SHINY_TEX.items()})
    return out
