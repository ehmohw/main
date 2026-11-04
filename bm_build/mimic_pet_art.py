"""(3.1 draft, stage 1: art only - not wired) THE MIMIC - a Black Market vault chest with teeth.

UNLOCK  In a heist vault (Tier III+, 1 run in 40), one of the loot chests "looks back at you": its latch blinks. Open it and it
        throws a TANTRUM - 30 seconds of snapping and hopping round the vault (it can't really hurt you: 1 heart a bite, and it
        spits your loot back if it eats any). Survive it - or hand it a Gutter Coin mid-tantrum, which it eats, delighted - and
        it calms down, licks you, and joins you (its summoning item: the Mimic's Key, a gold key with a tooth for a bit).

LOOK    Knee-high (~0.7 blocks), a real block-shaped chest. DISGUISED: a dark-stained oak strongbox with gold banding at the
        corners and across the lid, a gold padlock latch with a coin-slot keyhole - just a chest (no eyes, no feet: '_hide').
        REVEALED: the lid lifts a crack on a row of white teeth, two gold-glowing eyes open on the lid's front above the latch,
        four stubby clawed gold feet come out, a fat red tongue lolls, and a few gold coins rattle about inside. The inside is
        lined with crimson velvet.
RIG     base (the root: the box, its banding, the lower teeth, the velvet, the coins inside) - lid (hinged at the back: its
        banding, the latch, the upper teeth, the face: eyes per expression) - tongue (two segments, curling out) - feet (four);
        fx: 'coins' (a burst of spat coins), 'gulp' (a foe's outline, swallowed - a shadow in its mouth).
STASH   'stash': open wide, tongue out flat like a welcome mat over the front, the velvet and coins showing - the player opens
        it as a small portable stash (9 slots).
SKINS   '_sh' SHINY "Voidbox": obsidian-black wood, violet-glowing banding, amethyst teeth, a starfield velvet. Cosmetic '_crate'
        "Heist Crate" disguise: pale pine slats, stencilled FRAGILE, rope handles - a crate that bites."""
import math
from PIL import ImageDraw
from fol5_kit import Rig, coat, flat, canvas, hexc, limb, T, blob

PIVOT = {'base': (0, 3.0, 0), 'lid': (0, 9.0, 4.5), 'tongue': (0, 7.6, 1.0), 'tip': (0, 7.8, -3.0), 'footfr': (3.6, 1.6, -3.4),
         'footfl': (-3.6, 1.6, -3.4), 'footbr': (3.6, 1.6, 3.4), 'footbl': (-3.6, 1.6, 3.4), 'coins': (0, 10, -8), 'gulp': (0, 9, 0)}
PARENT = {'base': None, 'lid': 'base', 'tongue': 'base', 'tip': 'tongue', 'footfr': None, 'footfl': None, 'footbr': None, 'footbl': None,
          'coins': None, 'gulp': 'base'}
FACES = ('happy', 'blink', 'fierce', 'greedy', 'disg')                 # ('disg': the disguise - no eyes, just the latch)
R = Rig('mm_', 0.8, PIVOT, PARENT, FACES, face_part='lid', opt=('coins', 'gulp'))
C = dict(wood='#5a3a22', wooddk='#3a2414', gold='#e8b83a', golddk='#9a6a10', velvet='#9a1a2a', tooth='#fbf4e4', tongue='#e0506a', eye='#ffd23a')
SK = {'_sh': dict(wood='#1a1424', wooddk='#0a0810', gold='#b06aff', golddk='#5a2aa0', velvet='#141a3a', tooth='#d8b0ff', tongue='#8a3ab0', eye='#e0a0ff'),
      '_crate': dict(wood='#d8b47a', wooddk='#a8844a', gold='#8a6a3a', golddk='#5a4020', velvet='#6a5030', tooth='#fbf4e4', tongue='#e0506a', eye='#ffd23a')}


def _planks(c, seed):
    im = coat(c['wood'], seed, 16, 0.07, 1); px = im.load(); dk = hexc(c['wooddk'])
    for y in (3, 7, 11, 15):
        for x in range(16): px[x, y] = dk
    for (x, y) in ((5, 1), (12, 5), (2, 9), (9, 13)): px[x, y] = dk
    return im


def _face(kind, c, disguised=False):
    """the lid's front: planks, the gold band along the bottom, the latch (gold, a coin-slot keyhole) - and, revealed, its eyes"""
    im = _planks(c, 9).resize((32, 32)); d = ImageDraw.Draw(im); g, gd = hexc(c['gold']), hexc(c['golddk'])
    d.rectangle((0, 27, 31, 31), fill=g); d.line((0, 27, 31, 27), fill=gd)
    d.rectangle((12, 22, 19, 31), fill=g, outline=gd); d.rectangle((15, 25, 16, 29), fill=hexc('#1a1008'))                # (the latch)
    if c['wood'] == '#d8b47a':                                                                                       # (the crate: stencil)
        d.text((3, 3), 'FRAGILE', fill=hexc('#7a2a1a'))
    if disguised or kind == 'disg': return im
    E, K = hexc(c['eye']), hexc('#1a0a04')
    for x0 in (5, 20):
        if kind in (None, 'greedy', 'fierce'):
            d.ellipse((x0, 9, x0 + 7, 18 if kind != 'fierce' else 16), fill=E, outline=K)
            if kind == 'greedy':                                                                                     # (coin-eyes)
                d.rectangle((x0 + 3, 11, x0 + 4, 16), fill=hexc(c['golddk'])); d.line((x0 + 2, 12, x0 + 5, 12), fill=hexc(c['golddk']))
            else:
                d.rectangle((x0 + 3, 11 if kind != 'fierce' else 12, x0 + 4, 16 if kind != 'fierce' else 14), fill=K)
            if kind == 'fierce': d.line((x0, 7, x0 + 7, 10) if x0 < 16 else (x0, 10, x0 + 7, 7), fill=K, width=2)
        elif kind == 'happy':
            d.arc((x0, 10, x0 + 7, 18), 200, 340, fill=E, width=2)
        else:
            d.line((x0, 14, x0 + 7, 14), fill=K, width=2)
    return im


def _tex(c):
    t = {'planks': _planks(c, 1), 'planks2': _planks(c, 2), 'gold': coat(c['gold'], 3, 16, 0.07, 1, spots=[('#fff2b0', 5), (c['golddk'], 6)]),
         'velvet': coat(c['velvet'], 4, 16, 0.08, 1), 'tooth': coat(c['tooth'], 5, 16, 0.03, 1), 'tongue': coat(c['tongue'], 6, 16, 0.06, 1, spots=[('#ff8aa0', 8)]),
         'coin': coat('#ffd23a' if c['gold'] != '#b06aff' else '#d8b0ff', 7, 16, 0.06, 1, spots=[('#fff8c0', 4)]), 'shadow': flat('#140a10', alpha=190)}
    t['face'] = _face(None, c)
    for f in FACES: t[f'face_{f}'] = _face(f, c)
    return t


for k, v in _tex(C).items(): R.tex(k, v)
for sfx, c in SK.items():
    for k, v in _tex(dict(C, **c)).items(): R.tex(k + sfx, v)
    R.skin(sfx, {k: k + sfx for k in _tex(C)})
B = R.box
W, D_ = 5.0, 4.5
# the base: the box, gold corner bands, the velvet floor, coins inside, the lower teeth along its rim
B('base', (-W, 0.6, -D_), (W, 9.0, D_), 'planks')
for sx in (1, -1):
    for sz in (1, -1):
        B('base', (sx * W - 0.6 * (sx > 0) - 0.05 * sx, 0.5, sz * D_ - 0.6 * (sz > 0) - 0.05 * sz),
          (sx * W + 0.6 * (sx < 0) + 0.05 * sx, 9.0, sz * D_ + 0.6 * (sz < 0) + 0.05 * sz), 'gold')
B('base', (-W - 0.05, 0.5, -D_ - 0.05), (W + 0.05, 1.3, D_ + 0.05), 'gold')
B('base', (-W + 0.6, 8.2, -D_ + 0.6), (W - 0.6, 9.02, D_ - 0.6), 'velvet')
for i, (x, z) in enumerate(((-2.0, 1.0), (1.6, 2.2), (0.2, -0.6), (2.6, -1.8), (-3.0, -2.0))):
    B('base', (x - 0.9, 9.0, z - 0.9), (x + 0.9, 9.4 + 0.2 * (i % 2), z + 0.9), 'coin')
for i in range(7):                                                                                    # (the lower teeth, the front rim)
    x = -4.2 + i * 1.4
    B('base', (x - 0.45, 9.0, -D_ + 0.1), (x + 0.45, 10.2, -D_ + 0.9), 'tooth')
for sx in (1, -1):
    for i in range(3):
        z = -2.6 + i * 2.2; B('base', (sx * (W - 0.5) - 0.4, 9.0, z - 0.4), (sx * (W - 0.5) + 0.4, 9.9, z + 0.4), 'tooth')
# the lid: hinged at the back top edge; its front is the face
B('lid', (-W, 9.0, -D_), (W, 12.4, D_), 'planks2')
B('lid', (-W - 0.05, 9.0, -D_ - 0.06), (W + 0.05, 12.4, -D_), 'FACE', faces=('north',), uv={'north': [0, 0, 16, 16]}, light=0)
B('lid', (-W - 0.05, 11.6, -D_ - 0.05), (W + 0.05, 12.45, D_ + 0.05), 'gold')
B('lid', (-0.7, 9.0, -D_ - 0.05), (0.7, 12.45, D_ + 0.05), 'gold')
for i in range(6):                                                                                    # (the upper teeth, hanging from the lid's rim)
    x = -3.5 + i * 1.4
    B('lid', (x - 0.45, 8.0, -D_ + 0.2), (x + 0.45, 9.0, -D_ + 1.0), 'tooth')
# the tongue: two fat segments, curling out over the front
B('tongue', (-1.8, 7.8, -3.4), (1.8, 8.8, 1.2), 'tongue')
B('tip', (-1.6, 7.6, -6.4), (1.6, 8.4, -3.0), 'tongue')
for p in ('footfr', 'footfl', 'footbr', 'footbl'):
    x, y, z = PIVOT[p]
    B(p, (x - 1.2, 0.0, z - 1.4), (x + 1.2, 1.6, z + 1.0), 'gold')
    for dx in (-0.7, 0.0, 0.7): B(p, (x + dx - 0.25, 0.0, z - 2.0), (x + dx + 0.25, 0.7, z - 1.4), 'tooth')      # (claws)
for i in range(9):
    a = math.radians(i * 40); x, y = 4.2 * math.cos(a), 10 + 3.4 * math.sin(a)
    B('coins', (x - 0.8, y - 0.8, -8.2 - (i % 3)), (x + 0.8, y + 0.8, -7.8 - (i % 3)), 'coin', light=8)
B('gulp', (-2.6, 4.0, -2.6), (2.6, 9.0, 2.6), 'shadow')

FEET = ('footfr', 'footfl', 'footbr', 'footbl')


def P(lift=0.0, **kw):
    return R.ground(kw, lift)


def hop(fwd=0.0):
    return {p: limb(1 if p.endswith('r') else -1, fwd if p.startswith('footf') else -fwd) for p in FEET}


POSES = R.POSES
POSES.update({
    # the disguise: a plain chest, shut - no eyes, no feet, no tongue
    'disguise': P(_hide=FEET + ('tongue', 'tip'), _face='disg'),
    'idle_a': P(lid=T(-12), tongue=T(0), tip=T(30), _face=None),
    'idle_b': P(_face='happy', lid=T(-22), tongue=T(-10), tip=T(-30), lift=0.8, **hop(10)),
    'idle_c': P(_face='greedy', lid=T(-8), _hide=('tongue', 'tip')),                                 # (counting its coins)
    'walk_0': P(lift=1.6, base=T(-6), lid=T(-16), tip=T(30), **hop(30)), 'walk_1': P(base=T(4), lid=T(-6), tip=T(20), **hop(-20)),
    # sitting: settled down flat, feet tucked in, lid shut, a snore through the latch; then a sleepy half-open "come and look"
    'sit_a': P(_face='blink', _hide=FEET + ('tongue', 'tip')),
    'sit_b': P(_face='happy', lid=T(-30), tongue=T(0), tip=T(10), _hide=FEET),
    # SNAP: crouched, the lid cracked wide ... then a lunge and a slam shut
    'snap_up': P(_face='fierce', base=T(-14), lid=T(-80), tongue=T(-20), tip=T(-20), **hop(-20)),
    'snap': P(_face='fierce', base=T(18), lid=T(0), _hide=('tongue', 'tip'), _off=(0, 0, -4), lift=2.0, **hop(40)),
    # SWALLOW (charged): gulps a foe whole (the shadow in its mouth) ... rattles ... and SPITS it out in a shower of coins
    'swallow': P(_face='greedy', _show=('gulp',), base=T(-20), lid=T(-110), _hide=('tongue', 'tip')),
    'gulp': P(_face='blink', base=T(0, 0, 10), lid=T(0), _hide=('tongue', 'tip'), lift=1.0),
    'spit': P(_face='happy', _show=('coins',), base=T(14), lid=T(-100), tongue=T(30), tip=T(30)),
    # THE STASH: open wide for you - tongue out flat like a welcome mat
    'stash': P(_face='happy', lid=T(-105), tongue=T(20), tip=T(-10)),
    'hurt': P(_face='blink', base=T(-10, 0, 12), lid=T(-30), tongue=T(30), tip=T(50)),
})
DRAFT = ['disguise', 'idle_a', 'idle_b', 'idle_c', 'walk_0', 'sit_a', 'sit_b', 'snap_up', 'snap', 'swallow', 'gulp', 'spit', 'stash', 'hurt']
R.DRAFT = DRAFT
DOLL = {'kh': 1.55, 'kb': 0.82, 'kl': 0.62}
DOLL_GROUPS = {'lid': 'head', 'base': 'body', 'tongue': 'head', 'tip': 'head'}
SKIN_NAMES = {'_sh': 'SHINY Voidbox', '_crate': 'Heist Crate (cosmetic)'}
