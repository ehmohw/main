"""(3.1 draft, stage 1: art only - not wired) THE FIXER, UNMASKED - the heist broker of the Gilded Gutter. Until now nobody has seen
more of him than his hatch (the gold-framed "THE FIXER'S HATCH" in the Tinker's Bench, the Apothecary, the Herald's Banner), his
gold-edged Calling Card ("smells of cigar smoke"), his Lamp ("a brass lamp that never goes out") and his Ledger. After enough
heists, hand him the Rat King's Royal Marker at his hatch: the hatch opens, and he steps out to join your crew.

LOOK  Everything he's known by, worn: a lean, sharp man in his fifties, head-big chibi like the cast (~1.45 blocks to the hat's
      crown). A charcoal double-breasted PINSTRIPE suit with GOLD buttons and a gold pocket square (the hatch's gold), an oxblood
      tie; a low charcoal FEDORA with a gold band; grey-at-the-temples slicked hair; black leather gloves; two-tone shoes (black
      with bone spats). A thin moustache, a cocked brow, narrow amused amber eyes (they catch the lamp's light), a CIGAR in the
      corner of his mouth, its tip glowing. In his left hand his BRASS LAMP, lit (light_emission); in his right, when he means
      it, a CALLING CARD - or his LEDGER under his arm.

RIG   hips (the root) - body - head (faces; hat, hair, cigar on it) - armr/forer, arml/forel (bent at the elbow) - legr/legl -
      lamp (left hand) - card (right hand, _show) - ledger (left arm, _show; the lamp hides) - fx: cards3 (a fan of thrown cards),
      dial (a safe's dial, glowing, in the air before him), smoke (a ring of cigar smoke).

SKINS '_sh' the SHINY "White Tie": an ivory pinstripe on cream, white hat with a black band, platinum for the gold, and a lamp
      burning blue. Cosmetic suits: '_nav' (midnight navy, silver), '_brw' (tobacco brown tweed, brass)."""
import math
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, remap

PIVOT = {'hips': (0, 11.0, 0), 'body': (0, 11.0, 0), 'head': (0, 19.0, 0), 'armr': (5.0, 18.0, 0), 'forer': (5.6, 13.6, 0),
         'arml': (-5.0, 18.0, 0), 'forel': (-5.6, 13.6, 0), 'legr': (2.0, 11.0, 0), 'legl': (-2.0, 11.0, 0),
         'lamp': (-5.8, 9.4, -0.6), 'card': (5.8, 9.4, -0.8), 'ledger': (-5.6, 14.0, 0.6),
         'cards3': (0, 14.0, -8), 'dial': (0, 14.0, -9), 'smoke': (2.6, 21.8, -6)}
PARENT = {'hips': None, 'body': 'hips', 'head': 'body', 'armr': 'body', 'forer': 'armr', 'arml': 'body', 'forel': 'arml',
          'legr': 'hips', 'legl': 'hips', 'lamp': 'forel', 'card': 'forer', 'ledger': 'forel', 'cards3': 'body', 'dial': 'body', 'smoke': 'head'}
FACES = ('blink', 'grin', 'focus', 'surprised', 'hurt', 'sly')
R = Rig('fx_', 0.75, PIVOT, PARENT, FACES, opt=('card', 'ledger', 'cards3', 'dial', 'smoke'), companion=0.75)

C = {'suit': '#30303a', 'stripe': '#6a6a78', 'shirt': '#ece4d4', 'tie': '#7a1a26', 'gold': '#e8b83a', 'golddk': '#a8781a',
     'glove': '#18181c', 'skin': '#d6a47c', 'hair': '#4a4a50', 'grey': '#a0a0a8', 'hat': '#25252c', 'shoe': '#141012', 'spat': '#d8cfbc',
     'eye': '#e8a020', 'lampglow': '#ffd27a'}
SUITS = {'_sh': {'suit': '#ece4d0', 'stripe': '#b8ae98', 'hat': '#f4eee0', 'gold': '#dfe4ee', 'golddk': '#8a92a4', 'tie': '#1a1a22',
                 'lampglow': '#8ad8ff', 'glove': '#f4f0e8', 'shoe': '#f0ece0', 'spat': '#202024'},
         '_nav': {'suit': '#1a2238', 'stripe': '#4a5a80', 'hat': '#141a2c', 'gold': '#c8ccd8', 'golddk': '#7a8090', 'tie': '#3a5aa0'},
         '_brw': {'suit': '#5a3e28', 'stripe': '#8a6a48', 'hat': '#3e2a1a', 'tie': '#2a4a2a'}}


def _tex(c):
    t = {}
    im = coat(c['suit'], 1, 16, 0.05, 1); px = im.load(); s = hexc(c['stripe'])
    for x in range(1, 16, 4):
        for y in range(16):
            if y % 5: px[x, y] = s
    t['suit'] = im
    t['suitpl'] = coat(c['suit'], 2, 16, 0.05, 1)
    t['shirt'] = coat(c['shirt'], 3, 16, 0.03, 1); t['tie'] = coat(c['tie'], 4, 16, 0.06, 1)
    t['gold'] = coat(c['gold'], 5, 16, 0.08, 1, spots=[('#fff2b0', 6), (c['golddk'], 6)])
    t['glove'] = coat(c['glove'], 6, 16, 0.08, 1, spots=[('#3a3a44', 6)]); t['skin'] = coat(c['skin'], 7, 16, 0.04, 1)
    t['hair'] = coat(c['hair'], 8, 16, 0.08, 1, spots=[(c['grey'], 30)]); t['hat'] = coat(c['hat'], 9, 16, 0.05, 1)
    t['shoe'] = coat(c['shoe'], 10, 16, 0.06, 1, spots=[('#40363a', 4)]); t['spat'] = coat(c['spat'], 11, 16, 0.04, 1)
    t['glass'] = coat(c['lampglow'], 12, 16, 0.08, 1, spots=[('#ffffff', 10)])
    t['cigar'] = coat('#6a4024', 13, 16, 0.08, 1); t['ember'] = flat('#ff6a1a'); t['smoke'] = flat('#d8d8dc', alpha=150)
    t['vest'] = _front(c)
    t['face'] = _face(None, c)
    for f in FACES: t[f'face_{f}'] = _face(f, c)
    t['cardf'] = _card(c); t['ledgerc'] = coat('#5a1a1a', 14, 16, 0.06, 1, spots=[(c['gold'], 4)])
    t['dialf'] = _dial(c)
    return t


def _front(c):
    """his chest: the double-breasted jacket's lapels in a V over the shirt and tie, two rows of gold buttons, the pocket square"""
    im, d = canvas(32); im.paste(_tex_suit(c).resize((32, 32)))
    d.polygon([(10, 0), (22, 0), (16, 14)], fill=hexc(c['shirt']))
    d.polygon([(14, 1), (18, 1), (17, 13), (16, 15), (15, 13)], fill=hexc(c['tie'])); d.rectangle((14, 0, 18, 2), fill=hexc(c['tie']))
    d.line((10, 0, 16, 15), fill=hexc('#1a1a22'), width=1); d.line((22, 0, 16, 15), fill=hexc('#1a1a22'), width=1)
    for x in (11, 21):
        for y in (17, 23):
            d.rectangle((x, y, x + 1, y + 1), fill=hexc(c['gold']))
    d.polygon([(4, 7), (8, 7), (7, 4), (6, 6), (5, 4)], fill=hexc(c['gold']))                # (the pocket square, his right... our left)
    d.line((3, 8, 9, 8), fill=hexc('#1a1a22'))
    return im


def _tex_suit(c):
    im = coat(c['suit'], 1, 16, 0.05, 1); px = im.load(); s = hexc(c['stripe'])
    for x in range(1, 16, 4):
        for y in range(16):
            if y % 5: px[x, y] = s
    return im


def _face(kind, c):
    """a lean face: stubble along the jaw, a thin moustache, narrow amber eyes under heavy brows (his right one cocked)"""
    im, d = canvas(32, c['skin']); px = im.load()
    sk = hexc(c['skin']); dk = tuple(int(v * 0.86) for v in sk[:3]) + (255,)
    for y in range(22, 32):
        for x in range(32):
            if (x * 7 + y * 3) % 5 == 0: px[x, y] = dk                                           # (the stubble)
    d.rectangle((0, 0, 31, 3), fill=hexc(c['hair']))                                             # (the hairline, slicked back)
    K, E, W = hexc('#1e1414'), hexc(c['eye']), hexc('#fff6e0')
    br = hexc(c['hair'])
    def eyes(h=2, look=0):
        for x0 in (6, 19):
            d.rectangle((x0, 12, x0 + 6, 12 + h), fill=W); d.rectangle((x0 + 2 + look, 12, x0 + 4 + look, 12 + h), fill=E)
            d.point((x0 + 3 + look, 12), fill=K); d.line((x0, 11, x0 + 6, 11), fill=K)
    if kind in (None, 'sly', 'focus', 'grin'):
        eyes(2 if kind != 'focus' else 1, -1 if kind == 'sly' else 0)
    elif kind == 'surprised':
        for x0 in (6, 19):
            d.rectangle((x0, 10, x0 + 6, 15), fill=W); d.rectangle((x0 + 2, 11, x0 + 4, 14), fill=E); d.point((x0 + 3, 12), fill=K)
    elif kind == 'blink':
        for x0 in (6, 19): d.line((x0, 13, x0 + 6, 13), fill=K)
    elif kind == 'hurt':
        for x0 in (6, 19): d.line((x0, 11, x0 + 6, 14), fill=K); d.line((x0, 14, x0 + 6, 11), fill=K)
    # brows: heavy, his right (our left) cocked up - flattened to a scowl in focus
    if kind == 'focus':
        d.line((5, 8, 12, 10), fill=br, width=2); d.line((26, 8, 19, 10), fill=br, width=2)
    elif kind == 'surprised':
        d.line((5, 6, 12, 6), fill=br, width=2); d.line((19, 6, 26, 6), fill=br, width=2)
    else:
        d.line((5, 7, 12, 8), fill=br, width=2); d.line((19, 9, 26, 8), fill=br, width=2)
    d.line((15, 14, 15, 19), fill=dk); d.line((15, 19, 17, 19), fill=dk)                         # (the nose)
    d.line((10, 21, 21, 21), fill=hexc(c['hair']), width=2); d.point((9, 22), fill=hexc(c['hair'])); d.point((22, 22), fill=hexc(c['hair']))  # moustache
    if kind == 'grin':
        d.chord((11, 21, 21, 27), 0, 180, fill=W, outline=K)
    elif kind == 'surprised':
        d.ellipse((14, 23, 18, 27), fill=K)
    elif kind == 'hurt':
        d.line((12, 25, 20, 24), fill=K)
    else:                                                                                        # (a sideways half-smile)
        d.line((12, 24, 17, 24), fill=K); d.line((17, 24, 20, 23), fill=K)
    return im


def _card(c):
    im, d = canvas(16, '#f6f0e0'); d.rectangle((0, 0, 15, 15), outline=hexc(c['gold'])); d.rectangle((1, 1, 14, 14), outline=hexc(c['golddk']))
    d.text((5, 2), 'F', fill=hexc('#1a1a1a')); return im


def _dial(c):
    im, d = canvas(32); d.ellipse((1, 1, 30, 30), fill=hexc('#2a2a30'), outline=hexc(c['gold']), width=2)
    for i in range(12):
        a = math.radians(i * 30); d.line((16 + 11 * math.cos(a), 16 + 11 * math.sin(a), 16 + 14 * math.cos(a), 16 + 14 * math.sin(a)), fill=hexc(c['gold']))
    d.ellipse((11, 11, 21, 21), fill=hexc(c['gold'])); d.polygon([(16, 2), (14, 6), (18, 6)], fill=hexc('#ff4040'))
    return im


for k, v in _tex(C).items(): R.tex(k, v)
for sfx, ch in SUITS.items():
    for k, v in _tex(dict(C, **ch)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in _tex(C)})

# ---- the model
B = R.box
B('hips', (-3.8, 9.6, -2.2), (3.8, 11.6, 2.2), 'suitpl')
B('body', (-4.2, 11.4, -2.4), (4.2, 18.4, 2.4), 'suit')
B('body', (-4.0, 11.6, -2.55), (4.0, 18.2, -2.4), 'vest', faces=('north',), uv={'north': [0, 0, 16, 16]})
B('body', (-4.4, 10.0, 1.6), (4.4, 12.0, 2.6), 'suit')                                         # (the jacket's skirt at the back)
B('body', (-4.6, 17.0, -2.6), (4.6, 18.8, 2.6), 'suit')                                         # (square shoulders)
B('body', (-1.4, 18.4, -1.4), (1.4, 19.2, 1.4), 'shirt')                                        # (the collar)
# head, hair, hat, cigar
B('head', (-4.4, 19.0, -4.0), (4.4, 27.4, 4.0), 'skin')
B('head', (-4.45, 19.0, -4.05), (4.45, 27.4, -4.0), 'FACE', faces=('north',), uv={'north': [0, 0, 16, 16]})
B('head', (-4.7, 22.0, -2.6), (4.7, 27.8, 4.3), 'hair')                                         # (slicked back, grey at the temples)
B('head', (-7.0, 26.6, -6.6), (7.0, 27.4, 6.2), 'hat')                                          # (the brim, snapped down at the front)
B('head', (-7.0, 26.0, -7.6), (7.0, 26.8, -5.8), 'hat', rot=('x', 14, (0, 26.6, -6.4)))
B('head', (-4.8, 27.2, -4.4), (4.8, 31.4, 4.4), 'hat')
B('head', (-4.95, 27.3, -4.55), (4.95, 28.4, 4.55), 'gold')                                     # (the gold band)
B('head', (-2.4, 31.0, -3.4), (2.4, 31.6, 3.4), 'hat')                                          # (the crown's pinch)
R.seg('head', (1.8, 20.4, -4.0), (3.8, 20.0, -6.6), 0.7, 0.7, 'cigar')
B('head', (3.5, 19.65, -7.0), (4.2, 20.35, -6.4), 'ember', light=12)
# arms (suit sleeves, gloves), legs
for s, sx in (('r', 1), ('l', -1)):
    a, f = PIVOT['arm' + s], PIVOT['fore' + s]
    B('arm' + s, (a[0] - 1.3, f[1] - 0.2, -1.3), (a[0] + 1.3, a[1] + 0.6, 1.3), 'suit')
    B('fore' + s, (f[0] - 1.2, f[1] - 3.4, -1.2), (f[0] + 1.2, f[1] + 0.2, 1.2), 'suit')
    B('fore' + s, (f[0] - 1.25, f[1] - 3.6, -1.25), (f[0] + 1.25, f[1] - 3.0, 1.25), 'shirt')     # (a cuff of shirt)
    B('fore' + s, (f[0] - 1.1, f[1] - 5.4, -1.1), (f[0] + 1.1, f[1] - 3.5, 1.1), 'glove')
    l = PIVOT['leg' + s]
    B('leg' + s, (l[0] - 1.6, 1.6, -1.6), (l[0] + 1.6, l[1], 1.6), 'suit')
    B('leg' + s, (l[0] - 1.7, 0.0, -2.8), (l[0] + 1.7, 1.0, 1.8), 'shoe')
    B('leg' + s, (l[0] - 1.75, 1.0, -2.0), (l[0] + 1.75, 2.0, 1.85), 'spat')
# the brass lamp, hanging from his left hand: a ring, a cap, the glass (lit), a base
lx, ly, lz = PIVOT['lamp']
B('lamp', (lx - 0.3, ly - 1.4, lz - 0.3), (lx + 0.3, ly, lz + 0.3), 'gold')
B('lamp', (lx - 1.5, ly - 2.4, lz - 1.5), (lx + 1.5, ly - 1.4, lz + 1.5), 'gold')
B('lamp', (lx - 1.2, ly - 5.0, lz - 1.2), (lx + 1.2, ly - 2.4, lz + 1.2), 'glass', light=14)
for dx, dz in ((-1.2, -1.2), (1.2, -1.2), (-1.2, 1.2), (1.2, 1.2)):
    B('lamp', (lx + dx - 0.2, ly - 5.0, lz + dz - 0.2), (lx + dx + 0.2, ly - 2.4, lz + dz + 0.2), 'gold')
B('lamp', (lx - 1.6, ly - 5.8, lz - 1.6), (lx + 1.6, ly - 5.0, lz + 1.6), 'gold')
cx, cy, cz = PIVOT['card']
B('card', (cx - 1.4, cy - 2.0, cz - 0.05), (cx + 1.4, cy + 0.0, cz + 0.05), 'cardf', uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]})
gx, gy, gz = PIVOT['ledger']
B('ledger', (gx - 0.7, gy - 4.4, gz - 3.2), (gx + 0.7, gy + 0.4, gz + 0.4), 'ledgerc')
for i, (x, y, rz) in enumerate(((-3.0, 15.0, 20), (0.0, 16.0, 0), (3.0, 15.0, -20))):
    B('cards3', (x - 1.4, y - 1.0, -8.05 - i), (x + 1.4, y + 1.0, -7.95 - i), 'cardf', rot=('z', rz, (x, y, -8)), uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, light=6)
B('dial', (-4.0, 10.0, -9.05), (4.0, 18.0, -8.95), 'dialf', uv={'north': [0, 0, 16, 16], 'south': [0, 0, 16, 16]}, faces=('north', 'south'), light=10)
for i in range(8):
    a = math.radians(i * 45); x, y = 2.6 + 2.2 * math.cos(a), 22.6 + 2.2 * math.sin(a)
    B('smoke', (x - 0.6, y - 0.6, -7.0), (x + 0.6, y + 0.6, -6.0), 'smoke')


# ---- poses
def P(**kw):
    return R.ground(kw)


def arms(rf=8, ro=6, rb=10, lf=14, lo=6, lb=20):
    return dict(armr=limb(1, rf, ro), forer=limb(1, rb), arml=limb(-1, lf, lo), forel=limb(-1, lb))


def walk(k, a=24):
    s = math.sin(math.pi * k / 2)
    return dict(legr=limb(1, a * s), legl=limb(-1, -a * s), armr=limb(1, -a * 0.7 * s, 6), forer=limb(1, 16), arml=limb(-1, 18, 6), forel=limb(-1, 26),
                hips=T(0, 6 * s))


POSES = R.POSES
POSES.update({
    'idle_a': P(_face='sly', head=T(0, -6, 3), **arms()),
    'idle_b': P(_show=('smoke',), _face='blink', head=T(-10, 0, -2), **arms(rf=60, ro=10, rb=90)),           # (a draw on the cigar - a smoke ring)
    'idle_c': P(_show=('card',), _face='sly', head=T(6, 10), **arms(rf=50, ro=20, rb=70)),                     # (the card turned over his knuckles)
    'walk_0': P(**walk(1)), 'walk_1': P(**walk(3)),
    'run_0': P(body=T(14), head=T(-10), legr=limb(1, 40), legl=limb(-1, -36), armr=limb(1, -40, 8), forer=limb(1, 50), arml=limb(-1, 30, 8), forel=limb(-1, 40)),
    # sitting: on a crate, one leg crossed over the other, the lamp at his feet; then the Ledger open on his knee
    'sit_a': P(_face='sly', legr=limb(1, 90, 0, 0), legl=limb(-1, 90, -14, 20), hips=T(0), body=T(-6), **arms(rf=30, ro=14, rb=40, lf=36, lo=6, lb=30)),
    'sit_b': P(_show=('ledger',), _hide=('lamp',), _face='blink', head=T(20), legr=limb(1, 90), legl=limb(-1, 90, -14, 20), body=T(6),
               **arms(rf=40, ro=-4, rb=60, lf=50, lo=-4, lb=40)),
    # CALLING CARD: drawn from his breast pocket ... flicked - a fan of three gold-edged cards (they stick: the foe is marked)
    'card_up': P(_show=('card',), _face='focus', body=T(0, -24), armr=limb(1, 30, -30, 10), forer=limb(1, 110)),
    'card': P(_show=('cards3',), _face='sly', body=T(6, 22), armr=limb(1, 90, 14), forer=limb(1, 4), arml=limb(-1, -10, 20), forel=limb(-1, 20), legr=limb(1, -14), legl=limb(-1, 18)),
    # LIGHTS OUT: the lamp's shutter snapped shut, held high (every foe near goes dark - he steps behind one)
    'lights_out': P(_face='focus', _hide=('lamp',), arml=limb(-1, 0, 150), forel=limb(-1, 0, 20), armr=limb(1, 10, 20), forer=limb(1, 40), head=T(-8)),
    # SAFECRACKER (charged): a glowing safe-dial in the air before him - two gloved fingers spin it; the foe's armour 'clicks' open
    'crack': P(_show=('dial',), _face='focus', body=T(10), head=T(4), armr=limb(1, 80, -10), forer=limb(1, 20), arml=limb(-1, 70, -14), forel=limb(-1, 30)),
    # INSIDE JOB: the Ledger snapped open - "you owe" - every foe near pays (a cut of loot)
    'ledger': P(_show=('ledger',), _hide=('lamp',), _face='grin', arml=limb(-1, 80, 10), forel=limb(-1, 40), armr=limb(1, 60, -20), forer=limb(1, 60)),
    'tip_hat': P(_face='grin', head=T(10, 0, 6), armr=limb(1, 150, -20), forer=limb(1, 80), arml=limb(-1, 14, 6), forel=limb(-1, 20)),
    'happy': P(_face='grin', **arms(rf=0, ro=40, rb=20)),
    'hurt': P(_face='hurt', body=T(-12), head=T(-14), **arms(rf=20, ro=40, rb=40, lf=20, lo=40, lb=40)),
    'tired': P(_face='blink', body=T(0, 0, 0), hips=T(-90), legr=limb(1, 0), legl=limb(-1, 0), **arms(rf=0, ro=10, rb=0, lf=0, lo=10, lb=0)),
})
DRAFT = ['idle_a', 'idle_b', 'idle_c', 'walk_0', 'run_0', 'sit_a', 'sit_b', 'card_up', 'card', 'lights_out', 'crack', 'ledger', 'tip_hat', 'happy', 'hurt', 'tired']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
SHINY = 'Shiny White Tie'
