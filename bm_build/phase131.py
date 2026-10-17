"""2.77: APOPHISS, THE SERPENT KING - the Hollow Throne's hidden boss, and the follower he becomes.
(2.77b: he made the Hollow King - "all he is, he has from me"; the den lets in only those the seal swallows; he comes in black fire;
 he plays dead at half; the follower is his full size.)

- THE SEAL: once you've conquered the Hollow King, a great serpent coiled in the floor of his throne room glimmers
  (the moment the King falls, it flashes). Stand on it: three hollows ring it - a ribbon, a crest, a gem. Followers are
  welcome in the Hollow now for its conquerors (and its gates open for you, the puzzles asleep): bring EMMA, LEO and
  CECIL - the three who bound him once - onto the seal together and it breaks. One or two of them and it only stirs (and
  they'll tell you who's missing). Everyone near it is swallowed into THE SERPENT'S DEN, a drowned temple deep under the
  citadel (a pad by the door goes back up).
- THE DEN (2.77b): only the seal takes anyone down - anyone else in it (a pearl, a chorus fruit, a teleport, a dig through
  the dome) is thrown back up to the throne room; and he rises only when someone who has beaten the Hollow King (once, at
  any time, in any company) comes back with Emma, Leo and Cecil as followers - the three must be in the den now.
- HIS COMING (2.77b): the den goes dark, a heartbeat quickens, and black fire climbs out of the floor before his throne -
  sixteen tongues spiralling into a vortex that tightens while he grows inside it - then it bursts and he roars (7 s).
- THE FIGHT: CLAW (a raking sweep), BITE (a lunge,
  withering), MACE (his tail-mace crashes down in a quake), SERPENT'S FANGS (lines of fangs at you), VENOM (a spat glob
  that splashes poison and wither), THE SERPENT'S JUDGEMENT (2.80: a ring of fire under each of you erupts a breath later -
  nothing turns it, not armour, Protection, Resistance or a shield: step out of it); at three-quarters he calls his drowned
  court. At half he falls - the bar goes, his
  court crumbles, he lies still while his old enemies wonder - then a heartbeat, a laugh, and THE SERPENT UNBOUND: the
  ethereal king tears out of his scales on violet wings and takes to the air (13 s): VOID ORBS that leave pools of dark,
  the SWOOP (a dive through you), the WINGBEAT (thrown back), GRAND FANGS (he lands in rings of fangs) and spectral
  serpents, and his Judgement again, violet, wider, quicker and twice. (2.80: 1024 health, the game's ceiling - and he
  rises Unbound at full health again; every blow about a third harder.) Every player in the den when he falls shares the win (a follower's killing blow counts).
- DROPS: the first time, THE SERPENT'S OATH (he serves you), APOPHISS'S TRUE CROWN (his crown, the emerald awake - the
  relic Cecil sells, stronger) and THE SERPENT KING'S MACE; a hoard every time; later wins have a chance at each.
- THE FOLLOWER (the Oath; 2.77b: his full size, his reach to match): claw, bite, venom spit; every eighth blow THE SERPENT KING'S WRATH (the mace and a ring of
  fangs). Smug, scowling, secretly fond. Right-click him to sit; right-click him with a saddle and he wears it - then use
  the Oath beside him to ride (walk to slither, jump to lunge; the Oath while riding: SERPENT'S FANGS ahead). Sneak + use
  the Oath: his menu. 5 minutes if he faints; an item frame keeps him; a Raid Contract at Goldtooth.
"""
import math
import json
import os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import apophiss_art as ART
import rigfol as RF
import rigkit as RK
from rigkit import qs, I
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase67 as P67
import phase98 as P98
import phase100 as P100
import allies

GRN, GRN_LT, VIOLET, VIOLET_LT, GOLD = '#3ad06a', '#c8f0b0', '#b07aff', '#e0ccff', '#ffcf40'
BOSS_HP, PET_HP, PET_CD = 1024, 70, 300          # (2.80: 1024, the game's ceiling - and the Unbound king rises at full health again)
SB, SP = ART.BOSS_SCALE, ART.PET_SCALE
UB, UP = SB / 16, SP / 16
MENU = 8600                        # his menu (bm.menu) and its buttons 8601..8609
HOLLOW_VER_KEY = 'p2.data.HOLLOW_VER'
# the den: placed once in bm:hollow_throne, under the floating rock (the citadel's box starts at y40)
LAIR = (1046, 2, 1046)
LSX, LSY, LSZ = 60, 36, 60
LAIR_VER = 3                                     # (2.77: 2 - no column on the arrival step; 2.78: 3 - no chain holes in the dome)
lair_abs = lambda x, y, z: (LAIR[0] + x, LAIR[1] + y, LAIR[2] + z)
ARRIVE = lair_abs(30.5, 4, 51.5)                   # (the floor is y2 in the den, its walk y3; the step you land on is a block up)
SPAWN = lair_abs(30.5, 3, 15.5)
CENTER = lair_abs(30.5, 3, 30.5)
# the seal: the throne room floor (L3 = 62, its walk 63) at x84 z83 of the citadel (origin 1000 40 1000)
SEAL = (1084.5, 103.0, 1083.5)
BACK = (1078.5, 103.0, 1083.5)                     # (where the pad in the den sets you down again)
HOSTS = {'emma': ('cat', 'bm.emmapet'), 'leo': ('wolf', 'bm.leopet'), 'cecil': ('wolf', 'bm.cecilpet')}

# ------------------------------------------------------------------------------------------------ items
item('apo_oath', TOTEM, "The Serpent's Oath", GRN,
     ['A ring of black scales round a green fang.', ('Use: call Apophiss (or call him back).', 'blue'), ('Beside him, saddled: ride him.', 'blue'),
      ('Riding, use it: Serpent\'s Fangs ahead.', 'blue'), ('Sneak + use: his menu (sit, send home).', 'blue'),
      ('Right-click him with a saddle to saddle him.', 'gray'), ('If he faints: 5 minutes before he can return.', 'gray'),
      ('"I keep my word. Mostly."', 'dark_gray')],
     model='bm:apo_oath', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['apo_oath'] = 'bm:p131/use'


def _attr(a, amt, slot, op='add_value', ident=None):
    return {'type': f'minecraft:{a}', 'amount': D(amt), 'operation': op, 'slot': slot, 'id': ident or f'bm:apo_{a}_{slot}'}


# (2.77c: the strongest thing anyone can wear - stronger than every other boss's relic, his own shadow-crown included. A use
#  wears it (a hold item can't use the vanilla swap, so the use does the swap itself); a sneak + use on a block sets it there.)
item('apo_true_crown', TOTEM, "Apophiss's True Crown", GRN,
     ['His own crown, from his own den. The emerald is awake.', 'The Hollow King only ever wore its shadow.',
      ('Worn: +8 damage, +3 reach, +12 health,', 'blue'), ('+8 armour, +6 toughness, +10% speed; you are', 'blue'),
      ('hard to knock back, and your blows wither.', 'blue'), ('Wither, poison and fire can\'t touch you; you', 'blue'),
      ('breathe water and see in the dark.', 'blue'), ('Badly hurt: Regeneration. Monsters near you weaken.', 'blue'),
      ('Sneak + jump: Serpent\'s Fangs in five lines (2 s).', 'blue'), ('Near death: the Serpent King\'s Wrath (every 2 min).', 'blue'),
      ('Night: Strength II and Regeneration.', 'dark_purple'), ('Protection X, Thorns III, Respiration V.', 'blue'),
      ('Counts as the Hollow King\'s Regalia: worn with', 'dark_purple'), ('the rest of it, the set wakes.', 'dark_purple'),
      ('With Apophiss at your side: Resistance II, Regeneration II.', 'dark_purple'),
      ('Use: wear it. Sneak + use on a block: set it there.', 'gray'),
      ('Taken from Apophiss himself.', 'dark_gray')],
     model='bm:apo_true_crown', stack=1, cat='relic', glint=True, tier=3, custom_extra={'bm_set': 'conqueror'},
     comps=dict(hold('none'), **{
         'minecraft:equippable': {'slot': 'head', 'swappable': True, 'equip_sound': 'minecraft:item.armor.equip_netherite'},
         'minecraft:attribute_modifiers': [_attr('attack_damage', 8, 'head'),        # (2.82b: no more growing a size - players asked)
                                            _attr('entity_interaction_range', 3, 'head'),
                                           _attr('block_interaction_range', 2.0, 'head'), _attr('max_health', 12, 'head'), _attr('armor', 8, 'head'),
                                           _attr('armor_toughness', 6, 'head'), _attr('knockback_resistance', 0.5, 'head'),
                                           _attr('movement_speed', 0.1, 'head', 'add_multiplied_base')],
         # (2.80: better than the Hollow King's own Deathmask in every way - his Protection, Thorns and Respiration too - and a
         #  piece of his Regalia: the crown he only ever wore the shadow of)
         'minecraft:enchantments': {'bm:serpent_venom': 1, 'minecraft:protection': Int(10), 'minecraft:thorns': Int(3), 'minecraft:respiration': Int(5),
                                    'minecraft:aqua_affinity': Int(1)}}))
HOLD['apo_true_crown'] = 'bm:p131/crown/use'
# (2.80) THE SERPENT KING'S MACE - above Sepulchre, the Hollow King's maul, in everything - and in seven forms: swap-hands
# (F) for the next, sneak + F for the one before (as the Shifting arms). It always looks like his mace (its spikes take each
# form's colour); every form has its own enchantments and its own bite; the mace, the sword and the axe call the Serpent
# King's Wrath on a right-click. Its wrath gathers faster as the Regalia wakes (night, the moons, a Blood Moon - whether or
# not you wear it, as with Sepulchre), and faster still with Apophiss at your side.
MACE_FORMS = [  # key, name, base item, enchantments, attack damage, attack speed, spike colour, its bite
    ('sword', 'Sword', 'minecraft:netherite_sword', {'sharpness': 6, 'looting': 4, 'sweeping_edge': 4, 'knockback': 1}, 12, -2.4, '#3ad0b0', 'blows poison as well as wither'),
    ('axe', 'Axe', 'minecraft:netherite_axe', {'sharpness': 6, 'efficiency': 6, 'fortune': 3}, 15, -3.0, '#d04a3a', 'blows cleave the monsters round your target, and sap them'),
    ('mace', 'Mace', 'minecraft:mace', {'density': 6, 'breach': 5, 'smite': 7, 'wind_burst': 3}, 13, -3.4, '#4a4a54', 'a smash from a fall bursts fangs round where it lands'),
    ('pickaxe', 'Pickaxe', 'minecraft:netherite_pickaxe', {'efficiency': 6, 'fortune': 4}, 8, -2.8, '#e0b040', 'Haste II while you hold it'),
    ('shovel', 'Shovel', 'minecraft:netherite_shovel', {'efficiency': 6, 'fortune': 3}, 8.5, -3.0, '#b07a40', 'Haste II while you hold it; blows throw monsters up'),
    ('hoe', 'Hoe', 'minecraft:netherite_hoe', {'efficiency': 6, 'fortune': 4}, 7, 0.0, '#8ae040', 'every blow mends you'),
    ('trident', 'Trident', 'minecraft:trident', {'impaling': 6, 'loyalty': 3, 'channeling': 1}, 11, -2.9, '#40a8e0', 'blows burst fangs round your target'),
]
WRATH_FORMS = ('mace', 'sword', 'axe')
mace_id = lambda k: 'apo_mace' if k == 'mace' else f'apo_mace_{k}'
MACE_IDS = [mace_id(f[0]) for f in MACE_FORMS]
for _k, _nm, _base, _en, _dmg, _spd, _col, _bite in MACE_FORMS:
    _lore = ['The end of his tail: black spikes, white crescents.', (f'{_nm} form: {_bite}.', 'blue')]
    if _k in WRATH_FORMS:
        _lore += [('Right-click: the Serpent King\'s Wrath - fangs burst', 'blue'), ('out in rings round you and in lines ahead;', 'blue'),
                  ('monsters within 9 blocks wither, sicken and', 'blue'), ('take a heavy blow (12 s).', 'blue')]
    _lore += [('Every blow withers. Unbreakable.', 'blue'), ('Swap-hands (F): the next form. Sneak + F: the one before.', 'gray'),
              ('Sword · Axe · Mace · Pickaxe · Shovel · Hoe · Trident', 'dark_gray'),
              ('Its wrath gathers faster as the Regalia wakes;', 'dark_purple'), ('with Apophiss at your side: Strength II.', 'dark_purple'),
              ('Taken from Apophiss himself.', 'dark_gray')]
    _comps = {'minecraft:enchantments': {f'minecraft:{e}': Int(v) for e, v in _en.items()}, 'minecraft:unbreakable': {},
              'minecraft:attribute_modifiers': [_attr('attack_damage', _dmg, 'mainhand', ident='minecraft:base_attack_damage'),
                                                _attr('attack_speed', _spd, 'mainhand', ident='minecraft:base_attack_speed')]}
    if _k in WRATH_FORMS:
        _comps = dict(hold('none'), **_comps)
        HOLD[mace_id(_k)] = 'bm:p131/mace/use'
    item(mace_id(_k), _base, "The Serpent King's Mace" + ('' if _k == 'mace' else f': {_nm}'), GRN, _lore,
         model='bm:apo_mace_item' + ('' if _k == 'mace' else f'_{_k}'), stack=1, cat='weapon', glint=False, tier=3,
         custom_extra={'bm_apomace': B(1)}, comps=_comps)
item('fcontract_apo', TOTEM, 'Raid Contract: Apophiss', GRN,
     ['Signed in gold ink, sealed in wax - and venom.', ('Use once: from then on Apophiss', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_apo'] = 'bm:p131/sign'

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.appet'                 # (Cecil's spells pass him by)
allies.ALLIES.append('bm.appet')
BIT = 2 ** len(P89.BIT)
P89.BIT['apo'] = BIT
P68.KINDS['apo'] = (7, 'apo_oath', 'wolf', 'bm.appet', 'p131/summon', 'p131/dismiss', 'bm.apsel2', 'Apophiss', GRN)
P68.HE.add('apo')
P67.BOSSES.append(('bm.apboss', 'bm:apob'))
P98.CALLED.append(('apo', 'Apophiss', GRN, 'wolf', 'bm.appet', 'bm.apsel2', 'bm.apcd', 'p131/try_summon', 'p131/dismiss', 'p131/recall', 'p131/go'))
P100.WHO['apo'] = ('wolf', 'bm.appet')
P100.VOICE['Apophiss'] = (GRN, GRN_LT)
EXPR = ('smug', 'surprised', 'hurt', 'sleepy', 'blink', 'shock', 'tired', 'serious')
FACE_MODEL = {'smug': 'smug', 'surprised': 'shock', 'hurt': 'hurt', 'sleepy': 'tired', 'blink': 'blink', 'shock': 'shock', 'tired': 'tired', 'serious': None}
FX.FOLK['apo'] = ('minecraft:wolf', 'bm.appet', 'type=minecraft:item_display,tag=bm.app,tag=bm.app_head,tag=bm.app_pet,tag=!bm.apfade', EXPR,
                  (60, 140), [('smug', 40, 3)], ('smug', 40), 'tired', 'serious')
_orig_exprs = FX.exprs
FX.exprs = lambda k: EXPR if k == 'apo' else _orig_exprs(k)

# ------------------------------------------------------------------------------------------------ the poses (the art's, and a few of the game's own)
P = dict
POSES = {k: dict(v) for k, v in ART.POSES.items()}
# (2.78: the game's own poses - asleep, the sit's glance, ridden, swimming, the ethereal dive and landing - and the in-between
#  keyframes that keep his tail on its arc are drawn with the art, in apophiss_art.POSES)
for _p in POSES.values():
    if 'tail4' not in _p and 'tail3' in _p: _p['tail4'] = _p['tail3']


class _Art:                                         # (the art, with the game's poses: what rigfol needs)
    PIVOT, PARENT, PARTS, PART_K, PREFIX = ART.PIVOT, ART.PARENT, ART.PARTS, ART.PART_K, ART.PREFIX
    HIDDEN = staticmethod(ART.HIDDEN)
    model_name = staticmethod(ART.model_name)


A = _Art
DUR_B = {'idle_a': 30, 'idle_b': 30, 'slither_a': 5, 'slither_m': 5, 'slither_b': 5, 'battle': 6, 'claw_up': 7, 'claw': 3, 'bite': 3, 'mace_up': 12,
         'mace_swing': 2, 'mace_slam': 2, 'mace_rec': 4, 'mace_back': 4, 'tired_b': 30, 'eth_dland': 3, 'eth_lift': 4, 'eth_bdive': 3, 'eth_hdive': 4,
         'cast': 10, 'cast_point': 5, 'roar': 8, 'tired': 20, 'crouch': 6, 'defeated': 14,
         'eth_hover': 8, 'eth_beat': 8, 'eth_cast': 8, 'eth_dive': 5, 'eth_land': 5}
DUR_P = {'idle_a': 30, 'idle_b': 30, 'slither_a': 4, 'slither_m': 4, 'slither_b': 4, 'battle': 4, 'claw_up': 5, 'claw': 3, 'bite': 3, 'mace_up': 6,
         'mace_swing': 2, 'mace_slam': 2, 'mace_rec': 3, 'mace_back': 3, 'swim_m': 5,
         'cast': 6, 'cast_point': 4, 'roar': 6, 'crouch': 4, 'sit': 20, 'sit_b': 20, 'ride': 8, 'ride_b': 8, 'ride_c': 8, 'swim_a': 5, 'swim_b': 5}
# where the mace lands in its slam, and where his claws are casting (blocks, from the host, ^left ^up ^forward)
MACE_HIT = RK.point(A, POSES['mace_slam'], 'mace', (ART.PIVOT['mace'][0], ART.PIVOT['mace'][1] + 2, ART.PIVOT['mace'][2] + 5), scale=SB)
CLAW_R = RK.point(A, POSES['cast'], 'armr', (ART.PIVOT['armr'][0] + 2, ART.PIVOT['armr'][1] + 10, ART.PIVOT['armr'][2] - 2), scale=SB)
CLAW_L = RK.point(A, POSES['cast'], 'arml', (ART.PIVOT['arml'][0] - 2, ART.PIVOT['arml'][1] + 10, ART.PIVOT['arml'][2] - 2), scale=SB)
loc = lambda v: f'^{v[0]:.2f} ^{v[1]:.2f} ^{v[2]:.2f}'


def extend_offers(O, offer):
    pass                                            # (won in his den, never sold - only his raid contract, at Goldtooth)


# ================================================================================================= resource pack
def _seal_tex(lit):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    import random
    n = 64; im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); d = ImageDraw.Draw(im); rnd = random.Random(7)
    stone, dark, line = ('#3a4a44', '#1e2824', '#5ad87a' if lit else '#121a16')
    c = n / 2
    for y in range(n):
        for x in range(n):
            r = math.hypot(x + 0.5 - c, y + 0.5 - c)
            if r <= 31.5:
                v = rnd.randint(-8, 8); b = hexc(stone)[:3]
                im.putpixel((x, y), tuple(max(0, min(255, q + v)) for q in b) + (255 if r <= 30.5 else 200,))
    d.ellipse((2, 2, n - 3, n - 3), outline=hexc(dark), width=2)
    d.ellipse((6, 6, n - 7, n - 7), outline=hexc(line), width=1)
    pts = []                                        # the serpent: a spiral, thick to thin, its head at the middle
    for i in range(160):
        t = i / 160 * 4.6 * math.pi
        r = 25 - i * 0.135
        pts.append((c + r * math.cos(t), c + r * math.sin(t), 3.2 - i * 0.012))
    for x, y, w in pts:
        d.ellipse((x - w, y - w, x + w, y + w), fill=hexc(dark))
    for x, y, w in pts[::3]:
        d.ellipse((x - w * 0.45, y - w * 0.45, x + w * 0.45, y + w * 0.45), fill=hexc(line))
    hx, hy, _w = pts[-1]
    d.ellipse((hx - 4, hy - 3, hx + 4, hy + 3), fill=hexc(dark))
    d.point((hx + 1, hy - 1), fill=hexc('#ffffff' if lit else '#7a8a80'))
    for k, a in enumerate((90, 210, 330)):           # three hollows: a ribbon, a crest, a gem
        x, y = c + 27 * math.cos(math.radians(a)), c + 27 * math.sin(math.radians(a))
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=hexc('#0c1210'), outline=hexc(line))
        col = ('#ff7ad0', '#5ab8e0', '#b48cff')[k] if lit else '#24302a'
        if k == 0: d.polygon([(x - 2.5, y - 2), (x, y), (x - 2.5, y + 2)], fill=hexc(col)); d.polygon([(x + 2.5, y - 2), (x, y), (x + 2.5, y + 2)], fill=hexc(col))
        if k == 1: d.ellipse((x - 2.5, y - 2.5, x + 2.5, y + 2.5), outline=hexc(col)); d.point((x, y), fill=hexc(col))
        if k == 2: d.polygon([(x, y - 3), (x + 2.2, y), (x, y + 3), (x - 2.2, y)], fill=hexc(col))
    return im


def _blackfire_tex():
    """2.77b: black fire, for his coming - 8 frames of 32 x 32 stacked (an animated texture): a near-black heart, a deep violet body, a
    thin hot-violet rim and a few of his green sparks; tongues that lean and curl as they climb (a warped noise field that scrolls up
    exactly one period over the loop, so it never jumps)"""
    from PIL import Image
    import random
    W, NF, G = 32, 8, 8
    im = Image.new('RGBA', (W, W * NF), (0, 0, 0, 0)); rnd = random.Random(1316)
    grid = [[rnd.random() for _ in range(G)] for _ in range(G)]
    def vn(x, y):                                   # value noise, tiling every 32 pixels both ways
        gx, gy = x / 4.0, y / 4.0
        x0, y0 = int(math.floor(gx)), int(math.floor(gy)); fx, fy = gx - x0, gy - y0
        x0, y0 = x0 % G, y0 % G; x1, y1 = (x0 + 1) % G, (y0 + 1) % G
        sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        a = grid[y0][x0] + (grid[y0][x1] - grid[y0][x0]) * sx
        b = grid[y1][x0] + (grid[y1][x1] - grid[y1][x0]) * sx
        return a + (b - a) * sy
    rim, rim2, body, body2, core, spark = (226, 170, 255), (160, 72, 240), (58, 16, 92), (24, 6, 38), (6, 2, 10), (120, 255, 160)
    mix = lambda c1, c2, k: tuple(int(c1[i] + (c2[i] - c1[i]) * max(0.0, min(1.0, k))) for i in range(3))
    for f in range(NF):
        off = f * W / NF
        for y in range(W):
            v = 1 - (y + 0.5) / W                   # (0 at the foot, 1 at the tip)
            for x in range(W):
                u, yy = (x + 0.5) / W - 0.5, y + off
                wx = (vn(x * 0.5 + 11, yy * 0.5) - 0.5) * 9 * (0.2 + v)
                n = vn(x + wx, yy) * 0.6 + vn((x + wx) * 2, yy * 2) * 0.4
                half = 0.40 * (1 - v) ** 0.9 * min(1.0, 0.5 + v * 4) + 0.015
                lean = (vn(5, yy * 0.5 + 3) - 0.5) * 0.25 * v
                h = (1 - (abs(u - lean) / half) ** 1.6 - v ** 1.4 * 0.55 - (n - 0.5) * (0.5 + 1.3 * v)) * (1 - v ** 6)
                if h <= 0.0:
                    if 0.5 < v < 0.95 and n > 0.8 and abs(u - lean) < 0.25: im.putpixel((x, y + f * W), rim + (150,))
                    continue
                if h < 0.09: c = spark if (n > 0.78 and v < 0.6) else mix(rim, rim2, h / 0.09)
                elif h < 0.25: c = mix(rim2, body, (h - 0.09) / 0.16)
                elif h < 0.5: c = mix(body, body2, (h - 0.25) / 0.25)
                else: c = mix(body2, core, (h - 0.5) / 0.3)
                im.putpixel((x, y + f * W), c + (230 if h < 0.09 else 255,))
    return im


def textures():
    out = {'apo_seal': _seal_tex(False), 'apo_seal_lit': _seal_tex(True), 'apo_blackfire': _blackfire_tex()}
    out.update({f'apo_mace_f_{k}': ART._mace('#222226', col, 713) for k, _n, _b, _e, _d, _s, col, _t in MACE_FORMS if k != 'mace'})     # (2.80: the forms' spikes)
    return out


def _oath_icon(R):
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 13, 13), outline=hexc('#141c18'), width=2)
    for a in range(0, 360, 45):
        x, y = 7.5 + 5.5 * math.cos(math.radians(a)), 7.5 + 5.5 * math.sin(math.radians(a))
        im.putpixel((int(round(x)), int(round(y))), hexc('#2a8a46'))
    d.polygon([(7, 3), (9, 3), (8, 11)], fill=hexc('#7af0a0'))
    d.line((8, 4, 8, 9), fill=hexc('#e8fff0'))
    return im



def held_mace(tail):
    """2.78: the mace in a hand - his tail's mace head stood upright on a haft (a leather grip, a gold collar and pommel), and
    each hand's transform worked out from vanilla's handheld one, so the grip lands where a sword's does and the haft points
    where its blade would. (The tail's mace has no handle: it hung sideways off the hand.)"""
    import copy, numpy as np
    Rx = lambda a: np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = lambda a: np.array([[math.cos(a), 0, math.sin(a)], [0, 1, 0], [-math.sin(a), 0, math.cos(a)]])
    Rz = lambda a: np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    eul = lambda r: Rx(math.radians(r[0])) @ Ry(math.radians(r[1])) @ Rz(math.radians(r[2]))
    TOP = 4.0                                            # the head sits from here up; the haft below
    Z0 = min(min(e['from'][2], e['to'][2]) for e in tail['elements'])
    m = lambda p: [p[0], p[2] - Z0 + TOP, 16 - p[1]]     # tail's +z (out along the tail) -> up; its up -> north
    M = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])     # (the same swing as a rotation)
    FACE = {'north': 'down', 'south': 'up', 'up': 'north', 'down': 'south', 'east': 'east', 'west': 'west'}
    els = []
    for e in tail['elements']:
        a, b = m(e['from']), m(e['to'])
        n = {'from': [round(min(a[i], b[i]), 4) for i in range(3)], 'to': [round(max(a[i], b[i]), 4) for i in range(3)],
             'faces': {FACE[k]: v for k, v in e['faces'].items()}}
        if 'rotation' in e:                              # (a turn on any axes, Rz Ry Rx as rigkit writes it, carried through the same swing)
            r = e['rotation']
            ang = {k: math.radians(r.get(k, 0.0)) for k in 'xyz'}
            if 'axis' in r: ang = {k: (math.radians(r['angle']) if k == r['axis'] else 0.0) for k in 'xyz'}
            R = Rz(ang['z']) @ Ry(ang['y']) @ Rx(ang['x'])
            ax, ay, az = RK.euler((M @ R @ M.T).tolist())
            n['rotation'] = {'origin': [round(v, 4) for v in m(r['origin'])], 'x': ax, 'y': ay, 'z': az}
        els.append(n)
    box = lambda f, t, tex: {'from': list(f), 'to': list(t), 'faces': {d: {'uv': [0, 0, 16, 16], 'texture': f'#{tex}'} for d in FACE}}
    els += [box((7.1, -11.8, 7.1), (8.9, 4.4, 8.9), 'apo_scale_dk'),            # the haft
            box((6.85, -9.4, 6.85), (9.15, -2.6, 9.15), 'apo_strap'),           # the grip
            box((6.6, 2.8, 6.6), (9.4, 4.6, 9.4), 'apo_gold'),                  # the collar under the head
            box((6.5, -13.6, 6.5), (9.5, -11.6, 9.5), 'apo_gold')]              # the pommel
    tex = dict(tail['textures']); tex.update({'apo_strap': 'bm:block/apo_strap', 'apo_gold': 'bm:block/apo_gold'})
    G = np.array([8, -6.0, 8]) / 16 - 0.5                 # where the hand closes on the grip
    lo = min(min(e['from'][1], e['to'][1]) for e in els); hi = max(max(e['from'][1], e['to'][1]) for e in els)
    C = np.array([8, (lo + hi) / 2, 8]) / 16 - 0.5        # the middle of the whole mace
    def hand(vr, vt, vs, s):
        """vanilla handheld (rotation, translation, scale) for a sprite gripped at (3, 3), blade up its diagonal -> ours"""
        Rv = eul(vr); Rm = Rv @ Rz(math.radians(-45))     # (its diagonal is our haft; its plane's normal our z)
        gv = np.array(vt) / 16 + Rv @ (vs * (np.array([3, 3, 8]) / 16 - 0.5))
        t = (gv - Rm @ (s * G)) * 16
        r = [vr[0], vr[1], vr[2] - 45]
        assert np.allclose(eul(r), Rm), r
        return {'rotation': [round(v, 2) for v in r], 'translation': [round(float(v), 3) for v in t], 'scale': [s] * 3}
    def centred(r, s):
        t = -(eul(r) @ (s * C)) * 16
        return {'rotation': r, 'translation': [round(float(v), 3) for v in t], 'scale': [s] * 3}
    disp = {'thirdperson_righthand': hand([0, -90, 55], [0, 4, 0.5], 0.85, 0.8), 'thirdperson_lefthand': hand([0, 90, -55], [0, 4, 0.5], 0.85, 0.8),
            'firstperson_righthand': hand([0, -90, 25], [1.13, 3.2, 1.13], 0.68, 0.6), 'firstperson_lefthand': hand([0, 90, -25], [1.13, 3.2, 1.13], 0.68, 0.6),
            'gui': centred([0, 30, -45], 0.62), 'ground': centred([0, 0, 0], 0.45), 'fixed': centred([0, 180, -45], 0.7)}
    for k, d in disp.items():
        assert all(abs(v) <= 80 for v in d['translation']), (k, d)
    return {'textures': tex, 'elements': els, 'display': disp}

def rp(R):
    import sys
    from gen_rp import GUI_3D
    R.TEXTURE_MODS.append(ART)
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (ART.PREFIX,)
    R.LANG.update({'death.attack.bm.apo_judgement': '%1$s was judged by the Serpent King',          # (2.80: his Judgement)
                   'death.attack.bm.apo_judgement.player': '%1$s was judged by %2$s'})
    # the seal: a plate in the floor (4 blocks across at the display's scale)
    for nm in ('apo_seal', 'apo_seal_lit'):
        face = {'uv': [0, 0, 16, 16], 'texture': '#s'}
        R.HATS[nm] = ({'s': f'bm:block/{nm}'}, [{'from': [0, 8, 0], 'to': [16, 8.05, 16], 'faces': {'up': face, 'down': dict(face)},
                                                  **({'light_emission': 12} if nm.endswith('lit') else {})}])
    R.ICONS['apo_oath'] = _oath_icon(R)
    # (2.77b: a tongue of black fire - one upright plane; the display turns it to face you)
    face = {'uv': [0, 0, 16, 16], 'texture': '#f'}
    R.HATS['apo_blackfire'] = ({'f': 'bm:block/apo_blackfire'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False,
                                                                   'faces': {'north': face, 'south': dict(face)}}])
    cases = {base: [] for base in ('apo_head', 'apo_head_eth', 'apo_head_wf')}
    for e, m in FACE_MODEL.items():
        if m:
            cases['apo_head'].append((e, f'apo_head_x{m}'))
            cases['apo_head_eth'].append((e, f'apo_head_x{m}_eth'))
            cases['apo_head_wf'].append((e, f'apo_head_x{m}_wf'))
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/textures/block/apo_blackfire.png.mcmeta', {'animation': {'frametime': 2, 'interpolate': True}})
        for name, cs in cases.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cs], 'fallback': mdl(name)}})
        # the crown and the mace in the hand: the art's own crown (phase59's) and his tail's mace
        R2.wj('assets/bm/items/apo_true_crown.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/apophiss_crown'}})
        R2.wj('assets/bm/models/item/apo_mace_held.json', held_mace(json.load(open(R2.p('assets', 'bm', 'models', 'item', 'apo_mace.json')))))
        R2.wj('assets/bm/items/apo_mace_item.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/apo_mace_held'}})
        # (2.80: each other form - the same mace, its spikes in the form's colour)
        held = json.load(open(R2.p('assets', 'bm', 'models', 'item', 'apo_mace_held.json')))
        for k, *_r in MACE_FORMS:
            if k == 'mace': continue
            m = dict(held, textures=dict(held['textures'], apo_mace=f'bm:block/apo_mace_f_{k}'))
            R2.wj(f'assets/bm/models/item/apo_mace_held_{k}.json', m)
            R2.wj(f'assets/bm/items/apo_mace_item_{k}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/apo_mace_held_{k}'}})
    R.POST.append(post)


# ================================================================================================= the den (a structure)
def lair():
    import random
    from structures import Build
    Bd = Build(LSX, LSY, LSZ)
    rnd = random.Random(1311)
    pick = lambda pal: rnd.choices([p for p, _ in pal], [w for _, w in pal])[0]
    S = Bd.set
    CX, CZ, FY = 30, 30, 2
    RX, RY = 26.5, 30.0
    WALL = [('dark_prismarine', 5), ('prismarine_bricks', 3), ('deepslate_tiles', 3), ('cracked_deepslate_tiles', 1), ('mossy_stone_bricks', 1)]
    DOME = [('deepslate_tiles', 4), ('dark_prismarine', 3), ('cobbled_deepslate', 2), ('tuff', 1)]
    FLOOR = [('polished_deepslate', 4), ('deepslate_tiles', 3), ('dark_prismarine', 2), ('prismarine_bricks', 1)]
    for x in range(LSX):
        for z in range(LSZ):
            d = math.hypot(x - CX, z - CZ)
            if d > RX + 2.6: continue
            for y in range(0, FY): S(x, y, z, 'deepslate' if y else 'cobbled_deepslate')
            S(x, FY, z, pick(FLOOR))
            for y in range(FY + 1, LSY):
                h = y - FY
                inner = (d / RX) ** 2 + (h / RY) ** 2 < 1.0
                outer = (d / (RX + 2.2)) ** 2 + (h / (RY + 2.2)) ** 2 < 1.0
                if inner: S(x, y, z, 'air')
                elif outer: S(x, y, z, pick(WALL) if h < 7 else pick(DOME))
    # the serpent in the floor: a spiral of green from the rim of the middle to its head at the centre
    for i in range(400):
        t = i / 400 * 4.2 * math.pi
        r = 12.5 - i * 0.028
        w = 1.4 - i * 0.002
        x0, z0 = CX + r * math.cos(t), CZ + r * math.sin(t)
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if math.hypot(dx, dz) <= w:
                    S(int(round(x0 + dx)), FY, int(round(z0 + dz)), 'green_terracotta' if (i // 9) % 3 else 'lime_terracotta')
    for dx, dz in ((0, 0), (1, 0), (0, 1), (1, 1)): S(CX + dx, FY, CZ + dz, 'emerald_block')
    S(CX - 1, FY, CZ, 'verdant_froglight'); S(CX + 2, FY, CZ + 1, 'verdant_froglight')
    # a ring of shallow water (the drowned kingdom came down with him), four bridges, sea pickles glowing in it
    for x in range(LSX):
        for z in range(LSZ):
            d = math.hypot(x - CX, z - CZ)
            if 17.0 <= d < 18.7 and abs(x - CX) > 1 and abs(z - CZ) > 1:
                S(x, FY - 1, z, 'dark_prismarine')
                S(x, FY, z, 'sea_pickle[pickles=3,waterlogged=true]' if rnd.random() < 0.12 else 'water')
    # broken columns of the sunken court
    for k in range(10):
        if k in (2, 7): continue                    # (those two would stand on the arrival step, where the seal sets you down, and on his throne)
        a = math.radians(k * 36 + 18)
        cx, cz = int(round(CX + 22 * math.cos(a))), int(round(CZ + 22 * math.sin(a)))
        top = FY + (30 if k % 3 else 3 + rnd.randrange(6))
        for y in range(FY + 1, min(top, LSY - 1)):
            h = y - FY
            if (math.hypot(cx - CX, cz - CZ) / RX) ** 2 + (h / RY) ** 2 >= 0.98: break
            for dx, dz in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
                S(cx + dx, y, cz + dz, 'dark_prismarine' if h % 5 == 0 else 'prismarine_bricks')
            if h == 9 and k % 3: S(cx, y, cz, 'sea_lantern')
        if not k % 3:
            S(cx, top, cz, 'prismarine_brick_slab[type=bottom,waterlogged=false]')
            for dx, dz in ((2, 0), (-1, 2)): S(cx + dx, FY + 1, cz + dz, 'prismarine_bricks')
    # his throne in the north: a dais, the hoard on it, a backrest with the great emerald
    for x in range(21, 40):
        for z in range(4, 14):
            S(x, FY + 1, z, 'polished_blackstone_bricks' if (x + z) % 4 else 'chiseled_polished_blackstone')
            if 24 <= x <= 36 and z <= 10: S(x, FY + 2, z, 'dark_prismarine')
    for x in range(21, 40): S(x, FY + 1, 13, 'polished_blackstone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
    for x in range(24, 37): S(x, FY + 2, 11, 'prismarine_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]')
    for x in range(25, 36):
        for y in range(FY + 3, FY + 10):
            if abs(x - 30) + (y - FY - 3) // 2 <= 6: S(x, y, 4, 'dark_prismarine' if (x + y) % 3 else 'prismarine_bricks')
    S(30, FY + 8, 5, 'emerald_block'); S(29, FY + 9, 4, 'gold_block'); S(31, FY + 9, 4, 'gold_block'); S(30, FY + 10, 4, 'gold_block')
    for _ in range(26):
        x, z = rnd.randint(22, 38), rnd.randint(5, 11)
        y = FY + 3 if 24 <= x <= 36 and z <= 10 else FY + 2
        if Bd.get(x, y, z) in (None, 'minecraft:air'):
            S(x, y, z, rnd.choice(['gold_block', 'raw_gold_block', 'gold_block', 'emerald_block']) if rnd.random() < 0.5 else
              rnd.choice(['yellow_carpet', 'yellow_carpet', 'skeleton_skull[rotation=8]']))
    # where you arrive: a raised step by the south wall, the pad home
    for x in range(26, 35):
        for z in range(49, 56):
            if math.hypot(x - CX, z - CZ) <= RX - 0.6: S(x, FY + 1, z, 'polished_deepslate')
    S(30, FY + 1, 54, 'crying_obsidian')
    for x in (27, 33): S(x, FY + 2, 54, 'soul_lantern[hanging=false,waterlogged=false]')
    # light: lanterns on chains from the dome, sea lanterns round the wall, a soft fill
    for k in range(8):
        a = math.radians(k * 45)
        x, z = int(round(CX + 12 * math.cos(a))), int(round(CZ + 12 * math.sin(a)))
        y = LSY - 1                                 # (2.78: down through the open sky over the dome first, then through its shell -
        while y > FY + 1 and Bd.get(x, y, z) in (None, 'minecraft:air'): y -= 1          #  the chains used to start up in the sky and
        while y > FY + 1 and Bd.get(x, y, z) not in (None, 'minecraft:air'): y -= 1      #  punch a hole down through the ceiling)
        top = y
        while y > FY + 15: S(x, y, z, 'iron_chain[axis=y,waterlogged=false]'); y -= 1
        if top > FY + 15: S(x, y, z, 'soul_lantern[hanging=true,waterlogged=false]')
    for k in range(16):
        a = math.radians(k * 22.5 + 11)
        x, z = int(round(CX + (RX + 0.6) * math.cos(a))), int(round(CZ + (RX + 0.6) * math.sin(a)))
        if Bd.get(x, FY + 4, z) not in (None, 'minecraft:air'): S(x, FY + 4, z, 'sea_lantern')
    for x in range(6, 55, 6):
        for z in range(6, 55, 6):
            for y in (FY + 6, FY + 14):
                if Bd.get(x, y, z) == 'minecraft:air' and (math.hypot(x - CX, z - CZ) / RX) ** 2 + ((y - FY) / RY) ** 2 < 0.8:
                    S(x, y, z, 'light[level=10,waterlogged=false]')
    # bones and dead coral where the sea left them
    for _ in range(70):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(19.5, RX - 1)
        x, z = int(round(CX + r * math.cos(a))), int(round(CZ + r * math.sin(a)))
        if Bd.get(x, FY + 1, z) == 'minecraft:air':
            S(x, FY + 1, z, rnd.choice(['bone_block[axis=x]', 'bone_block[axis=z]', 'dead_brain_coral_block', 'dead_tube_coral_block',
                                        'skeleton_skull[rotation=3]', 'dead_horn_coral_fan[waterlogged=false]', 'dead_fire_coral_fan[waterlogged=false]']))
    for _ in range(60):                               # dripstone from the dome
        x, z = rnd.randint(8, 52), rnd.randint(8, 52)
        y = LSY - 1
        while y > FY + 8 and Bd.get(x, y, z) in (None, 'minecraft:air'): y -= 1
        while y > FY + 8 and Bd.get(x, y, z) not in (None, 'minecraft:air'): y -= 1
        if y > FY + 12 and Bd.get(x, y + 1, z) not in (None, 'minecraft:air'):
            S(x, y, z, 'pointed_dripstone[thickness=tip,vertical_direction=down,waterlogged=false]')
    Bd.marker(CX + 0.5, FY + 1.0, CZ + 0.5, ['bm.aplair'])
    Bd.marker(30.5, FY + 2.0, 54.5, ['bm.aprift'])
    return Bd


# ================================================================================================= the datapack
def generate(G):
    import phase28 as P28
    import phase73 as P73
    from p2 import data as P2D
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    apsay = lambda txt, who='@s': title(who, 'actionbar', [T('Apophiss: ', GRN, bold=True), T(txt, GRN_LT)])
    apchat = lambda txt, who='@s': tellraw(who, [T('Apophiss: ', GRN, bold=True), T(f'"{txt}"', GRN_LT)])
    voice = {'Emma': ('#ff8ad8', '#ffd8f0'), 'Leo': ('#5ab8e0', '#d8f0ff'), 'Cecil': ('#b48cff', '#e8d8ff'), 'Apophiss': (GRN, GRN_LT)}
    chat = lambda who, txt, aud='@s': tellraw(aud, [T(f'{who}: ', voice[who][0], bold=True), T(f'"{txt}"', voice[who][1])])
    tick, fast, second = [], [], []
    objs = ['bm.apfi', 'bm.apid', 'bm.apatk', 'bm.apt', 'bm.apc', 'bm.apph', 'bm.apr', 'bm.aplone', 'bm.apk', 'bm.apcd', 'bm.aps', 'bm.apf', 'bm.apa', 'bm.apx',
            'bm.apm', 'bm.apv', 'bm.apch', 'bm.apz', 'bm.apq', 'bm.apsd', 'bm.apsl', 'bm.apl', 'bm.apcl', 'bm.apw', 'bm.apsn', 'bm.apfg', 'bm.apfn', 'bm.apb', 'bm.crw']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        ['bossbar add bm:apob {text:"Apophiss, the Serpent King",color:"green"}', 'bossbar set bm:apob color green', 'bossbar set bm:apob style notched_10'] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (2, 3, 4, 8, 10, 16, 20, 24, 40, 60, 80, 100)]
    G.OBJECTIVES += objs
    HV = P2D.HOLLOW_VER
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.apboss'
    pl = lambda r, extra='': f'@a[distance=..{r},gamemode=!creative,gamemode=!spectator{extra}]'
    me = '@e[type=minecraft:husk,tag=bm.apme,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.apt matches {t} run {cmd}'

    # ================================================================== followers are welcome in the Hollow (2.78: anyone's - no conquest asked;
    #                                                                    they're called in the Serpent's Den like anywhere else)
    fo = G.FUNCS['p74/fol_ok']
    fo.remove('execute if dimension bm:hollow_throne run return 0')
    # (and its gates know them: a closed gate opens as a conqueror walks up, while the trials sleep - the way back to the throne is never shut)
    second.append('execute if score #hsafe bm.p2 matches 1 in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.gate,tag=bm.d_hollow,scores={bm.gs=0}] at @s '
                  'if entity @a[distance=..7,scores={bm.conq=6..},gamemode=!spectator] run function bm:p131/gate')
    fn('p131/gate', ['function bm:p2/hollow/gate_open', title('@a[distance=..10]', 'actionbar', T('The gate knows its conqueror. It opens.', 'gray', italic=True))])

    # ================================================================== THE DEN: placed once, under the citadel
    lair().export(G.path('data', 'bm', 'structure', 'p131_lair.nbt'))
    lx, ly, lz = LAIR
    lbox = f'x={lx},y={ly},z={lz},dx={LSX},dy={LSY},dz={LSZ}'
    # (2.78: the chains that used to stick up through the dome out of a den built before - a template's empty space leaves them)
    stray = []
    for k in range(8):
        a = math.radians(k * 45)
        x, z = lx + int(round(30 + 12 * math.cos(a))), lz + int(round(30 + 12 * math.sin(a)))
        stray.append(f'execute if score #apbuilt bm.p2 matches 1 in bm:hollow_throne run fill {x} {ly + 32} {z} {x} {ly + LSY + 4} {z} minecraft:air replace minecraft:iron_chain')
    # (2.78: the chains that used to stick up through the dome out of a den built before - a template's empty space leaves them)
    stray = []
    for k in range(8):
        a = math.radians(k * 45)
        x, z = lx + int(round(30 + 12 * math.cos(a))), lz + int(round(30 + 12 * math.sin(a)))
        stray.append(f'execute if score #apbuilt bm.p2 matches 1 in bm:hollow_throne run fill {x} {ly + 32} {z} {x} {ly + LSY + 4} {z} minecraft:air replace minecraft:iron_chain')
    fn('p131/lair/try', [f'execute in bm:hollow_throne run forceload add {lx - 4} {lz - 4} {lx + LSX + 4} {lz + LSZ + 4}',
                         f'execute in bm:hollow_throne store success score #apld bm.p2 if loaded {lx} {ly} {lz} if loaded {lx + LSX - 1} {ly} {lz + LSZ - 1} if loaded {lx} {ly} {lz + LSZ - 1} if loaded {lx + LSX - 1} {ly} {lz}',
                         'execute unless score #apld bm.p2 matches 1 run return run scoreboard players set #apwt bm.p2 0',
                         'scoreboard players add #apwt bm.p2 1', 'execute unless score #apwt bm.p2 matches 4.. run return 0',
                         f'execute if score #apver bm.p2 matches 1.. in bm:hollow_throne run kill @e[type=!minecraft:player,{lbox}]',
                         'scoreboard players set #apbuilt bm.p2 0',
                         f'execute in bm:hollow_throne store success score #apbuilt bm.p2 run place template bm:p131_lair {lx} {ly} {lz}',
                         *stray,
                         *stray,
                         f'execute if score #apbuilt bm.p2 matches 1 run scoreboard players set #apver bm.p2 {LAIR_VER}',
                         f'execute in bm:hollow_throne run forceload remove {lx - 4} {lz - 4} {lx + LSX + 4} {lz + LSZ + 4}'])
    second.append(f'execute unless score #apver bm.p2 matches {LAIR_VER} if score #hver bm.p2 matches {HV} if score #gver bm.p2 matches 2 run function bm:p131/lair/try')
    # the pad home (up to the throne room - followers too)
    fast.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.aprift] at @s if entity @a[distance=..24] run function bm:p131/lair/pad')
    fn('p131/lair/pad', ['particle minecraft:reverse_portal ~ ~0.8 ~ 0.3 0.6 0.3 0.02 6', 'particle minecraft:dust{color:[0.25,0.85,0.4],scale:1.0} ~ ~0.2 ~ 0.4 0.1 0.4 0 2',
                         'execute as @a[distance=..1.3,gamemode=!spectator] at @s run function bm:p131/lair/up'])
    fn('p131/lair/up', ['tag @s add bm.aptp', 'execute as @e[type=#bm:p131_fol,distance=..20] if function bm:p131/tp_owned run tag @s add bm.aptp',
                        'effect give @a[tag=bm.aptp] minecraft:darkness 2 0 true',
                        f'execute as @e[tag=bm.aptp] in bm:hollow_throne run tp @s {BACK[0]} {BACK[1]} {BACK[2]} -90 0',
                        'tag @e[tag=bm.aptp] remove bm.aptp', 'playsound minecraft:block.portal.travel ambient @s ~ ~ ~ 0.3 1.4',
                        say('Up through the dark - back in the Hollow King\'s throne room.', GRN_LT)])
    fn('p131/tp_owned', ['execute on owner if entity @s[tag=bm.aptp] run return 1', 'return 0'])
    # ---- no way in but the seal (2.77b): anyone in the den - or on its dome, or just outside it - whom the seal didn't swallow is thrown
    #      back up to the throne room: a pearl through the floor, a chorus fruit, a teleport, a dig through the dome all end the same way.
    #      (bm.apin: given by the swallow; gone the moment you're out of the den - the pad, a death, another dimension)
    gbox = f'x={lx - 4},y={ly - 6},z={lz - 4},dx={LSX + 8},dy={LSY + 14},dz={LSZ + 8}'
    fast.append(f'execute in bm:hollow_throne as @a[{gbox},tag=!bm.apin,gamemode=!spectator,gamemode=!creative] at @s run function bm:p131/lair/expel')
    fn('p131/lair/expel', ['tag @s add bm.aptp', f'execute as @e[type=#bm:p131_fol,{gbox}] if function bm:p131/tp_owned run tag @s add bm.aptp',
                           'effect give @s minecraft:darkness 3 0 true', 'effect give @s minecraft:slow_falling 2 0 true',
                           f'execute as @e[tag=bm.aptp] in bm:hollow_throne run tp @s {BACK[0]} {BACK[1]} {BACK[2]} -90 0',
                           'tag @e[tag=bm.aptp] remove bm.aptp', 'execute at @s run playsound minecraft:entity.warden.sonic_boom ambient @s ~ ~ ~ 0.3 1.6',
                           say("The dark beneath the throne spits you back out. Only the serpent's seal takes anyone down there.", GRN_LT)])
    second += ['execute as @a[tag=bm.apin] at @s unless dimension bm:hollow_throne run tag @s remove bm.apin',
               f'execute as @a[tag=bm.apin] at @s if dimension bm:hollow_throne unless entity @s[{gbox}] run tag @s remove bm.apin']
    wjson('bm/tags/entity_type/p131_fol.json', {'values': ['minecraft:wolf', 'minecraft:cat']})

    # ================================================================== THE SEAL (the throne room floor)
    sx, sy, sz = SEAL
    seal_v = snbt({'Tags': ['bm.apsealv'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:apo_seal'}},
                   'item_display': 'fixed', 'brightness': {'block': Int(9), 'sky': Int(9)}, 'view_range': F(1.5),
                   'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.02), F(0)], 'scale': [F(4), F(4), F(4)]}})
    second.append(f'execute if score #hver bm.p2 matches {HV} in bm:hollow_throne positioned {sx} {sy} {sz} if entity @a[distance=..40] '
                  'unless entity @e[type=minecraft:marker,tag=bm.apseal,distance=..2] run function bm:p131/seal/make')
    fn('p131/seal/make', ['kill @e[type=minecraft:item_display,tag=bm.apsealv,distance=..2]', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.apseal"]}',
                          f'summon minecraft:item_display ~ ~ ~ {seal_v}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.apseal,distance=..1] bm.apw 0'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.apsealv]', 'kill @e[type=minecraft:marker,tag=bm.apseal]']
    second.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.apseal] at @s if entity @a[distance=..20] run function bm:p131/seal/sec')
    near = lambda k: f'@e[type=minecraft:{HOSTS[k][0]},tag={HOSTS[k][1]},distance=..9]'
    fn('p131/seal/sec', ['execute if score @s bm.apw matches 1 run return 0',
                         'execute if score @s bm.apt matches 1.. run scoreboard players remove @s bm.apt 1',
                         'execute if score @e[type=minecraft:marker,tag=bm.arena,tag=bm.d_hollow,distance=..16,limit=1] bm.bs matches 1..2 run return 0',
                         'execute if entity @e[type=minecraft:husk,tag=bm.apboss] run return 0',
                         'particle minecraft:dust{color:[0.2,0.6,0.3],scale:0.8} ~ ~0.1 ~ 1.6 0 1.6 0 2',
                         'scoreboard players set #sn bm.rng 0'] +
       [f'execute if entity {near(k)} run scoreboard players add #sn bm.rng 1' for k in HOSTS] +
       ['execute unless entity @a[distance=..8,scores={bm.conq=6..},gamemode=!spectator] run scoreboard players set #sn bm.rng 0',
        'execute if score #sn bm.rng matches 3 run return run function bm:p131/seal/wake',
        'execute if score #sn bm.rng matches 1..2 run function bm:p131/seal/stir',
        'execute if score #sn bm.rng > @s bm.apsn unless score @s bm.apt matches 1.. run function bm:p131/seal/more',
        'scoreboard players operation @s bm.apsn = #sn bm.rng',
        'execute if score #sn bm.rng matches 0 as @a[distance=..2.8,scores={bm.conq=6..},gamemode=!spectator] unless score @s bm.apcl matches 1.. at @s run function bm:p131/seal/read',
        'execute if score #sn bm.rng matches 0 as @a[distance=..2.8,scores={bm.conq=..5},gamemode=!spectator] unless score @s bm.apcl matches 1.. run function bm:p131/seal/cold'])
    second.append('scoreboard players remove @a[scores={bm.apcl=1..}] bm.apcl 1')
    fn('p131/seal/read', ['scoreboard players set @s bm.apcl 6',
                          'execute unless entity @s[tag=bm.apread] run ' + tellraw('@s', [T('Words are cut into the stone round the serpent, worn almost smooth: ', 'gray', italic=True),
                                                                                        T('"HE WHO SITS THIS THRONE SITS IT BY MY LEAVE. ALL HE IS, HE HAS FROM ME."', GRN_LT, italic=True)]),
                          'tag @s add bm.apread',
                          title('@s', 'actionbar', [T('A great serpent, coiled in the stone. Three hollows ring it: ', 'gray', italic=True),
                                                    T('a ribbon', '#ff8ad8'), T(', ', 'gray'), T('a crest', '#5ab8e0'), T(', ', 'gray'), T('a gem', '#b48cff'), T('.', 'gray')]),
                          'playsound minecraft:block.sculk.charge ambient @s ~ ~ ~ 0.5 0.6'])
    fn('p131/seal/cold', ['scoreboard players set @s bm.apcl 6', say('A serpent carved in the floor. Cold. (It means nothing yet.)')])
    fn('p131/seal/stir', ['particle minecraft:dust{color:[0.3,0.95,0.45],scale:1.2} ~ ~0.2 ~ 1.4 0.1 1.4 0 14', 'particle minecraft:witch ~ ~0.3 ~ 1.2 0.1 1.2 0 4',
                          'playsound minecraft:block.sculk_shrieker.shriek ambient @a[distance=..14] ~ ~ ~ 0.15 0.5',
                          'execute if score #sn bm.rng matches 1 run ' + title('@a[distance=..10]', 'actionbar', [T('The seal stirs... ', GRN, italic=True), T('one of the three is here.', 'gray', italic=True)]),
                          'execute if score #sn bm.rng matches 2 run ' + title('@a[distance=..10]', 'actionbar', [T('The seal stirs... ', GRN, italic=True), T('two of the three. One more.', 'gray', italic=True)])])
    fn('p131/seal/more', ['scoreboard players set @s bm.apt 40',
                          f'execute if entity {near("emma")} run ' + chat('Emma', "This mark... I know this mark. Leo, Cecil - we have to be together for this. All of us.", '@a[distance=..12]'),
                          f'execute if entity {near("leo")} run ' + chat('Leo', "That's his mark. The serpent's - under the King's own throne. It was him behind the King all along. The three of us should be the ones to go.", '@a[distance=..12]'),
                          f'execute if entity {near("cecil")} run ' + chat('Cecil', 'A seal. With a serpent on it. Under a throne. I can\'t IMAGINE who that could be.', '@a[distance=..12]')])
    fn('p131/seal/wake', ['scoreboard players set @s bm.apw 1', 'scoreboard players set @s bm.apt 0',
                          'data modify entity @e[type=minecraft:item_display,tag=bm.apsealv,distance=..2,limit=1] item.components."minecraft:item_model" set value "bm:apo_seal_lit"',
                          'title @a[distance=..24] times 10 60 20', title('@a[distance=..24]', 'subtitle', T('It remembers the three who bound it.', 'gray', italic=True)),
                          title('@a[distance=..24]', 'title', T("THE SERPENT'S SEAL", GRN, bold=True)),
                          'playsound minecraft:entity.warden.emerge hostile @a[distance=..40] ~ ~ ~ 1 0.6', 'playsound minecraft:block.end_portal.spawn ambient @a[distance=..40] ~ ~ ~ 0.5 0.6'])
    tick.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.apseal,scores={bm.apw=1}] at @s run function bm:p131/seal/waking')
    fn('p131/seal/waking', ['scoreboard players add @s bm.apt 1',
                            'particle minecraft:dust{color:[0.3,1.0,0.45],scale:1.5} ~ ~0.2 ~ 1.6 0.2 1.6 0 6', 'particle minecraft:witch ~ ~0.5 ~ 1.5 0.4 1.5 0.05 3',
                            at(4, chat('Emma', "It's him. It's really him...", '@a[distance=..16]')),
                            at(30, chat('Cecil', 'I SAID we should have made sure he was dead.', '@a[distance=..16]')),
                            at(56, chat('Leo', 'Stay behind me, Princess. Whatever is down there.', '@a[distance=..16]')),
                            at('20..80', 'particle minecraft:large_smoke ~ ~0.3 ~ 1.4 0.2 1.4 0.02 4'),
                            at(40, 'playsound minecraft:block.deepslate.break block @a[distance=..30] ~ ~ ~ 2 0.5'),
                            at(40, 'particle minecraft:block{block_state:"minecraft:dark_prismarine"} ~ ~0.3 ~ 1.6 0.2 1.6 0 60'),
                            at(60, 'playsound minecraft:entity.warden.dig hostile @a[distance=..30] ~ ~ ~ 2 0.6'),
                            at(84, 'function bm:p131/seal/swallow')])
    ax, ay, az = ARRIVE
    fn('p131/seal/swallow', ['scoreboard players set @s bm.apw 0', 'scoreboard players set @s bm.apt 60', 'scoreboard players set @s bm.apsn 0',
                             'data modify entity @e[type=minecraft:item_display,tag=bm.apsealv,distance=..2,limit=1] item.components."minecraft:item_model" set value "bm:apo_seal"',
                             'tag @a[distance=..12,gamemode=!spectator] add bm.aptp',
                             'execute as @e[type=#bm:p131_fol,distance=..16] if function bm:p131/tp_owned run tag @s add bm.aptp',
                             'execute as @e[type=#bm:p131_fol,distance=..12] run tag @s add bm.aptp',
                             'effect give @a[tag=bm.aptp] minecraft:darkness 4 0 true', 'effect give @a[tag=bm.aptp] minecraft:blindness 2 0 true',
                             'effect give @a[tag=bm.aptp] minecraft:slow_falling 3 0 true',
                             'scoreboard players set #apwake bm.p2 1',
                             f'execute as @e[tag=bm.aptp] in bm:hollow_throne run tp @s {ax} {ay} {az} 180 0',
                             'tag @a[tag=bm.aptp] add bm.apin', 'execute as @a[tag=bm.aptp] at @s run function bm:p131/arrive',
                             'tag @e[tag=bm.aptp] remove bm.aptp',
                             'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..30] ~ ~ ~ 0.6 0.5'])
    fn('p131/arrive', ['title @s times 10 60 20', title('@s', 'subtitle', T('Deep beneath the Hollow Throne', 'gray', italic=True)),
                       title('@s', 'title', T("THE SERPENT'S DEN", GRN, bold=True)), 'playsound minecraft:ambient.underwater.loop.additions.ultra_rare ambient @s ~ ~ ~ 1 0.6'])
    # the King falls: the seal flashes, once, for his conqueror to notice
    G.FUNCS['p2/hollow/victory'].append(f'execute in bm:hollow_throne positioned {sx} {sy} {sz} as @e[type=minecraft:item_display,tag=bm.apsealv,distance=..2] at @s run function bm:p131/seal/flash')
    fn('p131/seal/flash', ['data modify entity @s item.components."minecraft:item_model" set value "bm:apo_seal_lit"', 'schedule function bm:p131/seal/dim 80t replace',
                           'execute at @s run particle minecraft:dust{color:[0.3,1.0,0.45],scale:1.6} ~ ~0.2 ~ 1.8 0.1 1.8 0 60',
                           'execute at @s run playsound minecraft:block.sculk_shrieker.shriek ambient @a[distance=..48] ~ ~ ~ 0.4 0.5'])
    fn('p131/seal/dim', ['execute in bm:hollow_throne as @e[type=minecraft:item_display,tag=bm.apsealv] run data modify entity @s item.components."minecraft:item_model" set value "bm:apo_seal"'])
    G.FUNCS['p2/hollow/victory'].append(f'execute in bm:hollow_throne positioned {sx} {sy} {sz} run ' + tellraw('@a[distance=..80]', [T('The Hollow King: ', '#e5e4e2', bold=True),
                                                                      T('"The serpent... promised me... forever..."', 'gray', italic=True)]))
    # (and as he rises a Wither, for an instant something green and serpentine coils through the dark round him)
    G.FUNCS['p2/hollow/ascend'] += ['particle minecraft:dust{color:[0.25,0.9,0.4],scale:2.0} ~ ~6 ~ 3 3 3 0 140 force @a[distance=..80]',
                                    'playsound minecraft:entity.cat.hiss hostile @a[distance=..60] ~ ~ ~ 1.5 0.4',
                                    tellraw('@a[distance=..60]', [T('(For an instant something green and serpentine coils through the dark round him - and is gone.)', GRN_LT, italic=True)])]
    G.FUNCS['p2/hollow/credit_first'].append(tellraw('@s', PREFIX + [T('As the King falls, the power in him drains away - not into the air, but down, into the floor of his throne room, where a serpent coiled in the stone flickers cold and green. ', GRN_LT),
                                                                      T('Whatever made him a king is still down there... and it remembers three old friends.', 'gray', italic=True)]))

    # ================================================================== THE RIG (boss and follower: the same parts, two sizes)
    def bsel(p=None):
        return '@e[type=minecraft:item_display,tag=bm.apsel' + (f',tag=bm.app_{p}]' if p else ']')
    fn('p131/b/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.app", f"bm.app_{p}", "bm.apb", "bm.apnew"], SB, extra={"view_range": F(3.0), "brightness": {"block": Int(11), "sky": Int(11)}, "shadow_radius": F(1.6 if p == "coil" else 0.0), "shadow_strength": F(0.7)})}'
                      for p in A.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.apnew,distance=..1] bm.apid = #aid bm.rng',
        'tag @e[type=minecraft:item_display,tag=bm.apnew,distance=..1] add bm.apsel', 'tag @e[type=minecraft:item_display,tag=bm.apnew] remove bm.apnew',
        'function bm:p131/b/look', 'scoreboard players set @s bm.aps -1'])
    fn('p131/b/rerig', [f'kill {bsel()}', 'execute as @e[type=minecraft:item_display,tag=bm.apb,tag=!bm.apdie] if score @s bm.apid = #aid bm.rng run kill @s', 'function bm:p131/b/rig'])
    fn('p131/b/place', RF.place(A, UB, bsel))
    for name, pz in POSES.items():
        if name in DUR_B:
            fn(f'p131/b/pose/{name}', RF.pose(A, pz, SB, DUR_B[name], bsel))
    # (the look: his scales, or the ethereal king's)
    fn('p131/b/look', ['execute if score @s bm.apph matches 2 run return run function bm:p131/b/look_eth'] +
       [f'data modify entity {bsel(p)[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_{p}"' for p in A.PARTS])
    fn('p131/b/look_eth', [f'data modify entity {bsel(p)[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_{p}_eth"' for p in A.PARTS])
    bface = lambda e: (f'data modify entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}' if e
                       else f'data remove entity {bsel("head")[:-1]},limit=1] item.components."minecraft:custom_model_data"')

    # ================================================================== THE BOSS
    bnbt = {'Tags': ['bm.apboss', 'bm.aphost', 'bm.apnew', 'bm.seen'], 'PersistenceRequired': B(1), 'Silent': B(1), 'NoAI': B(1), 'Invulnerable': B(1),
            'CustomName': T('Apophiss', GRN, bold=True), 'IsBaby': B(0), 'CanBreakDoors': B(0), 'DeathLootTable': 'minecraft:empty', 'Health': F(BOSS_HP),
            'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(scale=2.6, max_health=BOSS_HP, attack_damage=12, armor=18, armor_toughness=10,
                                                                                  movement_speed=0.25, follow_range=48, knockback_resistance=1.0,
                                                                                  spawn_reinforcements=0.0, step_height=2.0, jump_strength=0.0).items()],   # (2.78: he slithers - he steps up, never hops)
            'active_effects': [{'id': f'minecraft:{e}', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
                               for e in ('invisibility', 'fire_resistance', 'water_breathing')],
            'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}}
    # (the den: when the seal has swallowed someone and they're here, he's there - asleep before his throne)
    second.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.aplair] at @s if entity @a[distance=..40] run function bm:p131/lair/sec')
    spx, spy, spz = SPAWN
    # (2.77b: and only for the worthy, however they got here - someone who has beaten the Hollow King (ever: bm.conq), back now with
    #  Emma, Leo and Cecil, all three in the den;
    #  until then the den waits, and says so)
    worthy = f'@a[{lbox},tag=bm.apin,scores={{bm.conq=6..}},gamemode=!spectator]'
    fn('p131/lair/worthy', [f'execute unless entity {worthy} run return 0'] +
       [f'execute unless entity @e[type=minecraft:{HOSTS[k][0]},tag={HOSTS[k][1]},{lbox}] run return 0' for k in HOSTS] + ['return 1'])
    fn('p131/lair/sec', ['execute if score #apwake bm.p2 matches 1 unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..60] if function bm:p131/lair/worthy run function bm:p131/b/spawn',
                         'execute if entity @e[type=minecraft:husk,tag=bm.apboss,distance=..60] run scoreboard players set #apwake bm.p2 0',
                         f'execute unless entity @a[{lbox},tag=bm.apin] run scoreboard players set #apwake bm.p2 0',
                         'execute if score #apwake bm.p2 matches 1 run function bm:p131/lair/waits',
                         'execute store result score #r bm.rng run random value 1..20',
                         'execute if score #r bm.rng matches 1 run playsound minecraft:ambient.underwater.loop.additions.rare ambient @a[distance=..40] ~ ~ ~ 0.8 0.6',
                         'execute if score #r bm.rng matches 2 run playsound minecraft:block.pointed_dripstone.drip_water ambient @a[distance=..40] ~ ~6 ~ 1 0.8'])
    fn('p131/lair/waits', ['scoreboard players add #apnw bm.p2 1', 'execute unless score #apnw bm.p2 matches 4.. run return 0', 'scoreboard players set #apnw bm.p2 0',
                           title(f'@a[{lbox},tag=bm.apin]', 'actionbar', T('The den is silent. He rises only when one who has beaten the Hollow King comes back with Emma, Leo and Cecil - all three, here.', 'gray', italic=True))])
    fn('p131/b/spawn', [f'execute positioned {spx} {spy} {spz} run summon minecraft:husk ~ ~ ~ {snbt(bnbt)}',
                        f'execute positioned {spx} {spy} {spz} as @e[type=minecraft:husk,tag=bm.apnew,distance=..2,limit=1] at @s run function bm:p131/b/init'])
    fn('p131/b/init', ['scoreboard players add #apn bm.apid 1', 'scoreboard players operation @s bm.apid = #apn bm.apid', 'tp @s ~ ~ ~ 0 0',
                       'scoreboard players set @s bm.apatk 9', 'scoreboard players set @s bm.apt 0', 'scoreboard players set @s bm.apc 40', 'scoreboard players set @s bm.apph 1',
                       'scoreboard players set @s bm.apr 0', 'scoreboard players set @s bm.aplone 0', 'tag @s remove bm.apnew', 'bossbar set bm:apob visible false',
                       'scoreboard players operation #aid bm.rng = @s bm.apid', 'function bm:p131/b/rig', 'function bm:p131/b/hide', 'function bm:p131/b/posen/sleep', bface('blink'),
                       f'tag {bsel()} remove bm.apsel', 'team join bm.blood @s'])
    tick.append('execute as @e[type=minecraft:husk,tag=bm.apboss] at @s run function bm:p131/b/tick')
    fn('p131/b/tick', ['scoreboard players operation #aid bm.rng = @s bm.apid',
                       'execute as @e[type=minecraft:item_display,tag=bm.apb,tag=!bm.apdie,distance=..32] if score @s bm.apid = #aid bm.rng run tag @s add bm.apsel',
                       f'execute unless entity {bsel("coil")} run function bm:p131/b/rerig',
                       f'execute unless entity {bsel("mace")} run function bm:p131/b/rerig',
                       'execute rotated as @s rotated ~ 0 run function bm:p131/b/place',
                       # (2.78: half his health, and he transforms - checked every tick, mid-attack too, and held there: a strong blow
                       #  used to carry him past it, or kill him outright in his first form, between the mind's once-a-second looks)
                       'execute if score @s bm.apph matches 1 unless score @s bm.apatk matches 7 unless score @s bm.apatk matches 9 run function bm:p131/b/half',
                       'execute if score @s bm.apatk matches 1.. run function bm:p131/b/attack',
                       'execute if score @s bm.apph matches 1 unless score @s bm.apatk matches 1.. run function bm:p131/b/move',
                       'execute if score @s bm.apph matches 2 unless score @s bm.apatk matches 1.. run function bm:p131/b/fly',
                       'execute if score @s bm.apph matches 1.. unless score @s bm.apatk matches 1.. run function bm:p131/b/mind',
                       # his hitbox: blows on it are blows on him (phase82's relay)
                       'execute as @e[type=minecraft:interaction,tag=bm.bhit_ap,distance=..12] if score @s bm.hbid = #aid bm.rng run tag @s add bm.hbsel',
                       'execute unless entity @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_ap] run function bm:p131/b/hitbox',
                       'execute if score @s bm.apph matches ..1 run tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_ap] ~ ~ ~',
                       'execute if score @s bm.apph matches 2 run tp @e[type=minecraft:interaction,tag=bm.hbsel,tag=bm.bhit_ap] ~ ~1.4 ~',
                       'tag @e[type=minecraft:interaction,tag=bm.hbsel] remove bm.hbsel',
                       f'tag {bsel()} remove bm.apsel'])
    fn('p131/b/hitbox', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.bhit","bm.bhit_ap","bm.hbnew"],width:3.4f,height:6.6f}',
                         'scoreboard players operation @e[type=minecraft:interaction,tag=bm.hbnew] bm.hbid = #aid bm.rng',
                         'tag @e[type=minecraft:interaction,tag=bm.hbnew] add bm.hbsel', 'tag @e[type=minecraft:interaction,tag=bm.hbnew] remove bm.hbnew'])
    # (phase82's relay: a hit on his box is a hit on him; his box goes when he does)
    h = G.FUNCS['p82/hb/hit']
    h.insert(h.index(next(l for l in h if l.startswith('execute on attacker'))), 'execute if entity @s[tag=bm.bhit_ap] run scoreboard players set #hbk bm.rng 31')
    r = G.FUNCS['p82/hb/relay']
    r.insert(r.index('tag @s remove bm.hbatk'), 'execute if score #hbk bm.rng matches 31 as @e[type=minecraft:husk,tag=bm.apboss] if score @s bm.apid = #hbid bm.rng at @s run function bm:p82/hb/dmg with storage bm:tmp hb')
    o = G.FUNCS['p82/hb/orphan']
    o.insert(o.index('kill @s'), 'execute if entity @s[tag=bm.bhit_ap] as @e[type=minecraft:husk,tag=bm.apboss,distance=..40] if score @s bm.apid = #hbid bm.rng run return 0')
    # ================================================================== HIS COMING (2.77b; attack 9, at once when he spawns): the den goes dark, a
    #   heartbeat quickens - and black fire climbs out of the floor before his throne, sixteen tongues of it spiralling into a
    #   vortex that tightens and quickens while he grows inside it; then it bursts, and he roars (7 s). Then he speaks.
    VXN = 16
    def vx_at(t):                                   # (the vortex, tick by tick: its radius, its turn a tick, how far it has risen)
        e = lambda k: k * k * (3 - 2 * k)
        if t < 20: return 5.0, 4.0, -3.0
        if t < 60: k = (t - 20) / 40; return 5.0 - 0.8 * e(k), 4 + 6 * k, -3.0 + 3.0 * (1 - (1 - k) ** 2)
        if t < 120: k = (t - 60) / 60; return 4.2 - 2.2 * e(k), 10 + 22 * k ** 1.5, 0.6 * k
        if t < 145: k = (t - 120) / 25; return 2.0 - 0.5 * k, 32 + 8 * k, 0.6
        k = min(1.0, (t - 145) / 20); return 1.5 + 11 * (1 - (1 - k) ** 2), 40 - 30 * k, 0.6 + 2 * k
    G.FUNCS['load'][-1:-1] = ['data modify storage bm:p131 vxt set value [' +
                              ','.join('{r:%.3fd,s:%.2fd,y:%.3fd}' % vx_at(t) for t in range(171)) + ']']
    fire = lambda i: snbt({'Tags': ['bm.apfire', 'bm.apfnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:apo_blackfire'}},
                           'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(2),
                           'view_range': F(2.0), 'interpolation_duration': Int(30),
                           'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0), F(0)], 'scale': [F(0)] * 3}})
    fn('p131/b/vx_make', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.apvx"]}'] +
       [l for i in range(VXN) for l in (f'summon minecraft:item_display ~ ~-3 ~ {fire(i)}',
                                         f'scoreboard players set @e[type=minecraft:item_display,tag=bm.apfnew,limit=1] bm.apfi {i}',
                                         'tag @e[type=minecraft:item_display,tag=bm.apfnew] remove bm.apfnew')] +
       ['execute as @e[type=minecraft:item_display,tag=bm.apfire,distance=..6] run data merge entity @s {start_interpolation:0,interpolation_duration:30,'
        'transformation:{translation:[0f,1.1f,0f],scale:[1.4f,2.2f,1.4f]}}'])
    # (each tick: the marker turns; the tongues ride a rising spiral round it - a golden-angle scatter, wider toward the top)
    fn('p131/b/vx', ['execute store result storage bm:p131 vi.t int 1 run scoreboard players get @s bm.apt',
                     'function bm:p131/b/vx_pick with storage bm:p131 vi',
                     'execute as @e[type=minecraft:marker,tag=bm.apvx,distance=..4,limit=1] at @s run function bm:p131/b/vx_spin with storage bm:p131 vx',
                     'execute as @e[type=minecraft:marker,tag=bm.apvx,distance=..4,limit=1] at @s run function bm:p131/b/vx_fx'])
    fn('p131/b/vx_pick', ['$data modify storage bm:p131 vx set from storage bm:p131 vxt[$(t)]'])
    fn('p131/b/vx_spin', ['$tp @s ~ ~ ~ ~$(s) 0'] +
       [f'$execute rotated as @s rotated ~{i * 137.5 % 360:.1f} 0 positioned ^ ^{0.2 + 0.4 * i:.2f} ^$(r) positioned ^ ^ ^{(i - 8) * 0.08:.2f} positioned ~ ~$(y) ~ '
        f'run tp @e[type=minecraft:item_display,tag=bm.apfire,scores={{bm.apfi={i}}},distance=..30,limit=1] ~ ~ ~' for i in range(VXN)])
    dk = 'minecraft:dust{color:[0.03,0.0,0.05],scale:2.8}'
    fn('p131/b/vx_fx', [f'execute rotated as @s rotated ~{arm + k * 50} 0 positioned ^ ^{0.3 + k * 1.1:.1f} ^{2.6 - k * 0.15:.2f} run particle {dk} ~ ~ ~ 0.12 0.2 0.12 0 2 force @a[distance=..96]'
                        for arm in (0, 180) for k in range(6)] +
       ['particle minecraft:squid_ink ~ ~0.6 ~ 2.4 0.3 2.4 0.03 5 force @a[distance=..96]', 'particle minecraft:large_smoke ~ ~2.5 ~ 2 2.5 2 0.04 4 force @a[distance=..96]',
        'particle minecraft:reverse_portal ~ ~4 ~ 4 4 4 0.25 12 force @a[distance=..96]', 'particle minecraft:dragon_breath ~ ~0.2 ~ 4 0.1 4 0.01 4 force @a[distance=..96]',
        'particle minecraft:dust_color_transition{from_color:[0.0,0.0,0.0],to_color:[0.55,0.15,0.85],scale:2.0} ~ ~3 ~ 1.8 3 1.8 0 8 force @a[distance=..96]'])
    vring = lambda part, r, n, y=0.15: [f'particle {part} ^{r * math.cos(2 * math.pi * k / n):.2f} ^{y} ^{r * math.sin(2 * math.pi * k / n):.2f} 0.1 0.05 0.1 0 2 force @a[distance=..96]'
                                         for k in range(n)]
    ringd = 'minecraft:dust{color:[0.3,0.06,0.45],scale:2.2}'
    fn('p131/b/vx_ring', vring(ringd, 5.2, 36))
    fn('p131/b/vx_burst', ['particle minecraft:flash{color:[0.6,0.2,0.9,1.0]} ~ ~4 ~ 0 0 0 0 1 force @a[distance=..96]',
                           'particle minecraft:explosion_emitter ~ ~3 ~ 0 0 0 0 1 force @a[distance=..96]',
                           'particle minecraft:squid_ink ~ ~3 ~ 1 2 1 0.6 220 force @a[distance=..96]', 'particle minecraft:large_smoke ~ ~3 ~ 1 2 1 0.4 120 force @a[distance=..96]',
                           'particle minecraft:dust_color_transition{from_color:[0.0,0.0,0.0],to_color:[0.6,0.2,0.9],scale:3.0} ~ ~3 ~ 3 3 3 0 120 force @a[distance=..96]',
                           'particle minecraft:reverse_portal ~ ~3 ~ 1 2 1 1.2 200 force @a[distance=..96]',
                           'execute as @e[type=minecraft:item_display,tag=bm.apfire,distance=..12] run data merge entity @s {start_interpolation:0,interpolation_duration:18,'
                           'transformation:{scale:[0f,0f,0f]}}',
                           'playsound minecraft:entity.generic.explode hostile @a[distance=..96] ~ ~ ~ 2 0.6', 'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..96] ~ ~ ~ 2 0.6',
                           'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..96] ~ ~ ~ 2 0.6', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..96] ~ ~ ~ 2 0.5'])
    for r_ in (4, 8, 12):
        fn(f'p131/b/vx_wave_{r_}', vring('minecraft:dust{color:[0.08,0.0,0.12],scale:3.0}', r_, 8 * r_, 0))
    fn('p131/b/vx_end', ['kill @e[type=minecraft:item_display,tag=bm.apfire,distance=..40]', 'kill @e[type=minecraft:marker,tag=bm.apvx,distance=..8]'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.apfire]', 'kill @e[type=minecraft:marker,tag=bm.apvx]']
    # (a coming cut short - he left, or was removed - leaves no fire behind)
    second.append('execute in bm:hollow_throne as @e[type=minecraft:marker,tag=bm.apvx] at @s unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..4] run function bm:p131/b/vx_end')
    # (the tongues flicker: two sizes, three ticks each; bigger once the vortex is roaring)
    flick = lambda sx, sy: ('execute as @e[type=minecraft:item_display,tag=bm.apfire,distance=..16] run data merge entity @s {start_interpolation:0,interpolation_duration:3,'
                            f'transformation:{{translation:[0f,{sy / 2:.2f}f,0f],scale:[{sx}f,{sy}f,{sx}f]}}}}')
    fn('p131/b/vx_flick', ['scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #6 bm.rng',
                           'execute if score @s bm.apt matches ..89 if score #f bm.rng matches 0 run ' + flick(1.5, 2.4),
                           'execute if score @s bm.apt matches ..89 if score #f bm.rng matches 3 run ' + flick(1.3, 2.0),
                           'execute if score @s bm.apt matches 90.. if score #f bm.rng matches 0 run ' + flick(2.1, 3.5),
                           'execute if score @s bm.apt matches 90.. if score #f bm.rng matches 3 run ' + flick(1.8, 3.0)])
    beats = (1, 18, 34, 48, 60, 70, 80, 88, 96, 104, 112, 118, 124, 130, 136, 141)
    fn('p131/b/a_wake', [at(1, 'effect give @a[distance=..64] minecraft:darkness 4 0 true'),
                         at(1, 'playsound minecraft:block.beacon.deactivate hostile @a[distance=..96] ~ ~ ~ 2 0.5'),
                         at(1, 'playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..96] ~ ~ ~ 2 0.6')] +
       [at(t, f'playsound minecraft:entity.warden.heartbeat hostile @a[distance=..96] ~ ~ ~ {0.8 + j * 0.1:.1f} {0.55 + j * 0.03:.2f}') for j, t in enumerate(beats)] +
       [at(20, 'function bm:p131/b/vx_make'), at('20..165', 'function bm:p131/b/vx'), at('50..144', 'function bm:p131/b/vx_flick'),
        at(20, 'playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..96] ~ ~ ~ 1.5 0.5'),
        at(20, 'playsound minecraft:entity.blaze.burn hostile @a[distance=..96] ~ ~ ~ 2 0.5')] +
       [at(t, 'playsound minecraft:block.fire.ambient hostile @a[distance=..96] ~ ~ ~ 3 0.5') for t in range(20, 141, 15)] +
       [at(t, 'function bm:p131/b/vx_ring') for t in range(25, 141, 12)] +
       [at(40, 'playsound minecraft:entity.wither.ambient hostile @a[distance=..96] ~ ~ ~ 1.5 0.4'),
        at(60, 'playsound minecraft:item.trident.thunder hostile @a[distance=..96] ~ ~ ~ 1.2 0.6'),
        at(60, 'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..96] ~ ~ ~ 2 0.5'),
        at(70, 'function bm:p131/b/grow'),
        at(80, 'playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..96] ~ ~ ~ 2 0.4'),
        at('90..144', 'particle minecraft:sculk_soul ~ ~2 ~ 1.4 2 1.4 0.06 4 force @a[distance=..96]'),
        at('90..144', 'particle minecraft:witch ~ ~3 ~ 2 3 2 0 6 force @a[distance=..96]'),
        at(100, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..96] ~ ~ ~ 2 0.5'),
        at(100, 'playsound minecraft:entity.ender_dragon.ambient hostile @a[distance=..96] ~ ~ ~ 1.5 0.5'),
        at(118, 'function bm:p131/b/posen/idle_a'), at(118, bface(None)),
        at(120, 'playsound minecraft:entity.wither.spawn hostile @a[distance=..96] ~ ~ ~ 1 0.5'),
        at(135, 'playsound minecraft:entity.warden.emerge hostile @a[distance=..96] ~ ~ ~ 2 0.6'),
        # (the burst: he is there)
        at(145, 'function bm:p131/b/vx_burst'), at(145, 'function bm:p131/b/pose/roar'), at(145, bface('shock')),
        at(145, 'execute positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_4'), at(147, 'execute positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_8'),
        at(149, 'execute positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_12'),
        at(145, 'title @a[distance=..64] times 6 60 20'), at(145, title('@a[distance=..64]', 'title', T('APOPHISS', GRN, bold=True))),
        at(145, title('@a[distance=..64]', 'subtitle', T('the Serpent King', GRN_LT))),
        at(166, 'function bm:p131/b/vx_end'),
        # (and then he speaks)
        at(166, 'function bm:p131/b/pose/idle_a'), at(170, bface('smug')),
        at(170, apchat("Hsss... the little princess. All grown up. And she brought the tin knight, and the spark-fingered boy.", '@a[distance=..64]')),
        at(204, chat('Emma', "We beat you once, Apophiss! We'll beat you again!", '@a[distance=..64]')),
        at(232, apchat('Once, child. ONCE. And while I slept, who do you think kept that "King" on his throne? His crown of shadow was MINE. I lent it. He wore it. You BROKE it.', '@a[distance=..64]')),
        at(272, 'function bm:p131/b/pose/battle'), at(272, bface(None)),
        at(272, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 2 0.5'), at(280, 'function bm:p131/b/begin')])
    # (his rig at nothing - and growing in, in whatever pose he is in; the no-scale poses turn him without touching his size)
    fn('p131/b/hide', [f'execute as {bsel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[0f,0f,0f]}}}}' for p in A.PARTS])
    fn('p131/b/grow', [f'execute as {bsel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:60,transformation:{{scale:[{SB * A.PART_K.get(p, 1.0):.4f}f,{SB * A.PART_K.get(p, 1.0):.4f}f,{SB * A.PART_K.get(p, 1.0):.4f}f]}}}}'
                       for p in A.PARTS if not A.HIDDEN(p, POSES['sleep'])])
    for name, dur in (('sleep', 1), ('idle_a', 16)):
        fn(f'p131/b/posen/{name}', RF.pose(A, POSES[name], SB, dur, bsel, hide=False))
    fn('p131/b/begin', ['data merge entity @s {NoAI:0b,Invulnerable:0b}', 'attribute @s minecraft:jump_strength base set 0',
                        'attribute @s minecraft:step_height base set 2', 'bossbar set bm:apob name {text:"Apophiss, the Serpent King",color:"green"}',
                        'bossbar set bm:apob color green', 'bossbar set bm:apob visible true', 'function bm:p131/b/done', 'scoreboard players set @s bm.apc 30'])
    # moving (phase 1): the husk's own feet; a slither while he goes, his slow breath while he waits
    fn('p131/b/move', ['scoreboard players add @s bm.apf 1',
                       'scoreboard players set #st bm.rng 0', 'execute if predicate bm:p21/walking run scoreboard players set #st bm.rng 1',
                       'execute unless score @s bm.aps = #st bm.rng run scoreboard players set @s bm.apf 0', 'scoreboard players operation @s bm.aps = #st bm.rng',
                       'scoreboard players operation #f bm.rng = @s bm.apf',
                       'execute if score #st bm.rng matches 1 run scoreboard players operation #f bm.rng %= #20 bm.rng',
                       'execute if score #st bm.rng matches 0 run scoreboard players operation #f bm.rng %= #60 bm.rng',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 0 run function bm:p131/b/pose/slither_a',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 5 run function bm:p131/b/pose/slither_m',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 10 run function bm:p131/b/pose/slither_b',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 15 run function bm:p131/b/pose/slither_m',
                       'execute if score #st bm.rng matches 1 if score #f bm.rng matches 5 run playsound minecraft:entity.armadillo.scute_drop hostile @a[distance=..24] ~ ~ ~ 0.8 0.5',
                       # (low: he's flagging, and it shows - slumped on his coils, breathing hard, no longer rearing up between)
                       'execute store result score #hp bm.rng run data get entity @s Health',
                       'execute if score #st bm.rng matches 0 if score #hp bm.rng matches 121.. if score #f bm.rng matches 0 run function bm:p131/b/pose/idle_a',
                       'execute if score #st bm.rng matches 0 if score #hp bm.rng matches 121.. if score #f bm.rng matches 30 run function bm:p131/b/pose/idle_b',
                       'execute if score #st bm.rng matches 0 if score #hp bm.rng matches ..120 if score #f bm.rng matches 0 run function bm:p131/b/pose/tired',
                       'execute if score #st bm.rng matches 0 if score #hp bm.rng matches ..120 if score #f bm.rng matches 30 run function bm:p131/b/pose/tired_b'])
    # flying (phase 2): NoAI - toward his quarry, keeping six blocks above the floor; the wings beat
    fn('p131/b/fly', ['scoreboard players add @s bm.apf 1', 'scoreboard players operation #f bm.rng = @s bm.apf', 'scoreboard players operation #f bm.rng %= #16 bm.rng',
                      'execute if score #f bm.rng matches 0 run function bm:p131/b/pose/eth_hover',
                      'execute if score #f bm.rng matches 8 run function bm:p131/b/pose/eth_beat',
                      'execute if score #f bm.rng matches 8 run playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..40] ~ ~ ~ 0.8 0.8',
                      'particle minecraft:dust{color:[0.7,0.45,1.0],scale:1.4} ~ ~2 ~ 1.2 1 1.2 0 2',
                      f'execute unless entity @a[tag=bm.aptgt,distance=..48] run tag @a[distance=..48,gamemode=!creative,gamemode=!spectator,sort=random,limit=1] add bm.aptgt',
                      'execute if entity @a[tag=bm.aptgt,distance=8..48] facing entity @a[tag=bm.aptgt,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.22 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~ ~ ~',
                      'execute positioned ~ ~-5 ~ unless block ~ ~ ~ #bm:grap_pass run tp @s ~ ~0.15 ~',
                      'execute positioned ~ ~-7 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~-0.1 ~',
                      'execute positioned ~ ~6 ~ unless block ~ ~ ~ #bm:grap_pass run tp @s ~ ~-0.2 ~',
                      'execute facing entity @a[tag=bm.aptgt,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                      # (never out of the den)
                      f'execute if dimension bm:hollow_throne positioned {CENTER[0]} {CENTER[1]} {CENTER[2]} unless entity @s[distance=..22] at @s facing {CENTER[0]} {CENTER[1]} {CENTER[2]} run tp @s ^ ^ ^0.4'])
    # the leash (phase 1 too): out past the columns, back he comes
    second.append(f'execute in bm:hollow_throne positioned {CENTER[0]} {CENTER[1]} {CENTER[2]} as @e[type=minecraft:husk,tag=bm.apboss,distance=23..80] run tp @s {SPAWN[0]} {SPAWN[1]} {SPAWN[2]}')

    # ---- the mind: every second he isn't mid-attack, maybe one (3 s between, under 2 once enraged)
    fn('p131/b/mind', ['scoreboard players remove @s bm.apc 1', 'execute if score @s bm.apc matches 1.. run return 0', 'scoreboard players set @s bm.apc 20',
                       'execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
                       'scoreboard players operation #h2 bm.rng = #mx bm.rng', 'scoreboard players operation #h2 bm.rng /= #2 bm.rng',
                       'scoreboard players operation #h4 bm.rng = #mx bm.rng', 'scoreboard players operation #h4 bm.rng *= #3 bm.rng', 'scoreboard players operation #h4 bm.rng /= #4 bm.rng',
                       'execute if score @s bm.apph matches 1 if score #hp bm.rng <= #h2 bm.rng run return run function bm:p131/b/start {a:7}',
                       'execute if score @s bm.apph matches 1 if score @s bm.apr matches 0 if score #hp bm.rng <= #h4 bm.rng run return run function bm:p131/b/start {a:6}',
                       'execute if score @s bm.apph matches 2 run return run function bm:p131/b/mind2',
                       'execute store result score #r bm.rng run random value 1..100',
                       f'execute if score #r bm.rng matches 1..20 if entity {pl(28)} run return run function bm:p131/b/start {{a:8}}',
                       'execute store result score #r bm.rng run random value 1..100',
                       f'execute if entity {pl(5.5)} if score #r bm.rng matches 1..45 run return run function bm:p131/b/start {{a:1}}',
                       f'execute if entity {pl(8)} if score #r bm.rng matches 46..72 run return run function bm:p131/b/start {{a:2}}',
                       f'execute if entity {pl(11)} if score #r bm.rng matches 73..92 run return run function bm:p131/b/start {{a:3}}',
                       f'execute if entity {pl(24)} if score #r bm.rng matches 1..55 run return run function bm:p131/b/start {{a:4}}',
                       f'execute if entity {pl(24)} run return run function bm:p131/b/start {{a:5}}'])
    fn('p131/b/mind2', ['execute store result score #r bm.rng run random value 1..5', 'execute if score #r bm.rng matches 1 run tag @a remove bm.aptgt',
                        'execute store result score #r bm.rng run random value 1..100',
                        f'execute if score #r bm.rng matches 1..20 if entity {pl(40)} run return run function bm:p131/b/start {{a:16}}',
                        'execute store result score #r bm.rng run random value 1..100',
                        'execute if score #r bm.rng matches 1..30 run return run function bm:p131/b/start {a:11}',
                        f'execute if score #r bm.rng matches 31..52 if entity {pl(28)} run return run function bm:p131/b/start {{a:12}}',
                        f'execute if score #r bm.rng matches 53..68 if entity {pl(11)} run return run function bm:p131/b/start {{a:13}}',
                        'execute if score #r bm.rng matches 69..84 run return run function bm:p131/b/start {a:14}',
                        # (the call only on its own roll, and only while fewer than two serpents are out: never more than three)
                        'scoreboard players set #vx bm.rng 9',
                        'execute if score #r bm.rng matches 85..100 run function bm:p131/b/vexes', 'execute if score #vx bm.rng matches ..1 run return run function bm:p131/b/start {a:15}',
                        'function bm:p131/b/start {a:11}'])
    fn('p131/b/vexes', ['execute store result score #vx bm.rng if entity @e[type=minecraft:vex,tag=bm.apvex,distance=..48]'])
    fn('p131/b/start', ['$scoreboard players set @s bm.apatk $(a)', 'scoreboard players set @s bm.apt 0', 'scoreboard players set @s bm.apc 46',
                        'execute if score @s bm.apph matches 2 run scoreboard players set @s bm.apc 36',
                        'execute if score @s bm.apph matches 1 run effect give @s minecraft:slowness 2 6 true',
                        'execute if score #hp bm.rng matches ..200 run scoreboard players set @s bm.apc 28'])
    fn('p131/b/half', ['execute store result score #hp bm.rng run data get entity @s Health 100',
                       'execute store result score #h2 bm.rng run attribute @s minecraft:max_health get 50',
                       'execute if score #hp bm.rng > #h2 bm.rng run return 0',
                       'execute store result entity @s Health float 0.01 run scoreboard players get #h2 bm.rng',
                       'function bm:p131/b/done', 'execute store result score #hp bm.rng run data get entity @s Health', 'function bm:p131/b/start {a:7}'])
    fn('p131/b/done', ['scoreboard players set @s bm.apatk 0', 'scoreboard players set @s bm.aps -1', 'scoreboard players set @s bm.apf 0', 'tag @a[tag=bm.aphitp] remove bm.aphitp'])
    names = {1: 'claw', 2: 'bite', 3: 'mace', 4: 'fangs', 5: 'venom', 6: 'court', 7: 'ascend', 8: 'judge', 9: 'wake', 11: 'orbs', 12: 'swoop', 13: 'gust', 14: 'grand',
             15: 'call', 16: 'judge2'}
    fn('p131/b/attack', ['scoreboard players add @s bm.apt 1', 'tag @s add bm.apme'] +
       [f'execute if score @s bm.apatk matches {n} run function bm:p131/b/a_{w}' for n, w in names.items()] + ['tag @s remove bm.apme'])
    face_t = 'execute facing entity @p[gamemode=!creative,gamemode=!spectator] feet run tp @s ~ ~ ~ ~ 0'
    # CLAW: wound up to his right, then a raking sweep across his front
    fn('p131/b/a_claw', [at(1, face_t), at(1, 'function bm:p131/b/pose/claw_up'), at(1, 'playsound minecraft:entity.ravager.attack hostile @a[distance=..32] ~ ~ ~ 1 0.6'),
                         at(8, 'function bm:p131/b/pose/claw'), at(9, 'function bm:p131/b/claw_hit'),
                         at(20, 'function bm:p131/b/pose/battle'), at('26..', 'function bm:p131/b/done')])
    fn('p131/b/claw_hit', [f'particle minecraft:sweep_attack ^{x} ^3 ^{z} 0 0 0 0 1' for x, z in ((-3, 2), (-1.5, 3.5), (0, 4), (1.5, 3.5), (3, 2))] +
       ['playsound minecraft:entity.player.attack.sweep hostile @a[distance=..32] ~ ~ ~ 1.4 0.5',
        f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^3 as {pl(4.4)} run damage @s 22 minecraft:mob_attack by {me}'])
    # BITE: down low, then a lunge - the maw shuts on you (withering)
    fn('p131/b/a_bite', [at(1, face_t), at(1, 'function bm:p131/b/pose/crouch'), at(1, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..32] ~ ~ ~ 0.6 1.4'),
                         at('6..8', 'execute rotated as @s rotated ~ 0 positioned ^ ^ ^1 if block ~ ~0.5 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run tp @s ~ ~ ~'),
                         at(6, 'function bm:p131/b/pose/bite'), at(9, 'function bm:p131/b/bite_hit'),
                         at(20, 'function bm:p131/b/pose/battle'), at('26..', 'function bm:p131/b/done')])
    fn('p131/b/bite_hit', ['playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..32] ~ ~ ~ 1.4 0.6', 'playsound minecraft:entity.fox.bite hostile @a[distance=..32] ~ ~ ~ 1 0.4',
                           f'execute rotated as @s rotated ~ 0 positioned ^ ^1 ^4 as {pl(3.4)} at @s run function bm:p131/b/bitten'])
    fn('p131/b/bitten', [f'damage @s 26 minecraft:mob_attack by {me}', 'effect give @s minecraft:wither 5 1', 'effect give @s minecraft:poison 4 0',
                         'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 8'])
    # MACE: the tail lifts the mace high over him - and brings it down in a quake (enraged: fangs where it lands)
    fn('p131/b/a_mace', [at(1, face_t), at(1, 'function bm:p131/b/pose/mace_up'), at(1, 'playsound minecraft:item.mace.smash_air hostile @a[distance=..32] ~ ~ ~ 1 0.5'),
                         at('2..15', f'execute rotated as @s rotated ~ 0 positioned {loc(MACE_HIT)} run particle minecraft:dust{{color:[0.9,0.25,0.25],scale:1.6}} ~ ~0.1 ~ 1.6 0 1.6 0 6'),
                         at(14, 'function bm:p131/b/pose/mace_swing'), at(16, 'function bm:p131/b/pose/mace_slam'),
                         at(18, f'execute rotated as @s rotated ~ 0 positioned {loc(MACE_HIT)} run function bm:p131/b/quake'),
                         at(21, 'function bm:p131/b/pose/mace_rec'), at(25, 'function bm:p131/b/pose/mace_back'),
                         at(30, 'function bm:p131/b/pose/battle'), at('34..', 'function bm:p131/b/done')])
    fn('p131/b/quake', ['particle minecraft:explosion ~ ~0.3 ~ 2.5 0.1 2.5 0 10', 'particle minecraft:block{block_state:"minecraft:dark_prismarine"} ~ ~0.2 ~ 3 0.1 3 0 80',
                        'particle minecraft:dust{color:[0.2,0.9,0.4],scale:2} ~ ~0.3 ~ 3 0.2 3 0 40',
                        'playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..40] ~ ~ ~ 1.5 0.6', 'playsound minecraft:entity.generic.explode hostile @a[distance=..40] ~ ~ ~ 1 0.6',
                        f'execute as {pl(4.8)} run damage @s 24 minecraft:mob_attack by {me}', f'effect give {pl(4.8)} minecraft:slowness 3 1',
                        'execute store result score #hp bm.rng run data get entity @s Health',
                        'execute if score #hp bm.rng matches ..300 run function bm:p131/b/ring3'])
    # SERPENT'S FANGS: claws high, green fire in them - then lines of fangs at up to three of you
    fn('p131/b/a_fangs', [at(1, 'function bm:p131/b/pose/cast'), at(1, 'playsound minecraft:entity.evoker.prepare_attack hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'),
                          at('2..16', f'execute rotated as @s rotated ~ 0 positioned {loc(CLAW_R)} run particle minecraft:dust{{color:[0.3,1.0,0.45],scale:1.3}} ~ ~ ~ 0.3 0.3 0.3 0 3'),
                          at('2..16', f'execute rotated as @s rotated ~ 0 positioned {loc(CLAW_L)} run particle minecraft:dust{{color:[0.3,1.0,0.45],scale:1.3}} ~ ~ ~ 0.3 0.3 0.3 0 3'),
                          at(12, 'function bm:p131/b/pose/cast_point'), at(14, 'playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..40] ~ ~ ~ 1.5 0.6'),
                          at(14, f'execute as {pl(26, ",sort=random,limit=3")} at @s run function bm:p131/b/fang_line'),
                          at(30, 'function bm:p131/b/pose/idle_a'), at('34..', 'function bm:p131/b/done')])
    fn('p131/b/fang_line', [f'execute positioned as {me} rotated ~ 0 facing entity @s feet rotated ~ 0 run function bm:p131/b/fangs'])
    fn('p131/b/fangs', [f'summon minecraft:evoker_fangs ^ ^ ^{2.5 + i * 1.3:.1f} {{Warmup:{i * 2}}}' for i in range(14)])
    # VENOM: a glob spat at you - it splashes poison and wither
    glob = snbt({'Tags': ['bm.apglob', 'bm.apgn'], 'item': {'id': 'minecraft:slime_ball', 'count': Int(1)}, 'item_display': 'fixed', 'teleport_duration': Int(1),
                 'brightness': {'block': Int(15), 'sky': Int(15)},
                 'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(1.4)] * 3}})
    fn('p131/b/a_venom', [at(1, face_t), at(1, 'function bm:p131/b/pose/cast_point'), at(1, 'playsound minecraft:entity.llama.spit hostile @a[distance=..32] ~ ~ ~ 1.4 0.5'),
                          at(7, f'execute facing entity @p[gamemode=!creative,gamemode=!spectator] eyes positioned ^ ^4.6 ^2.5 run summon minecraft:item_display ~ ~ ~ {glob}'),
                          at(7, 'execute as @e[type=minecraft:item_display,tag=bm.apgn] at @s facing entity @p[gamemode=!creative,gamemode=!spectator] eyes run tp @s ~ ~ ~ ~ ~'),
                          at(7, 'scoreboard players set @e[type=minecraft:item_display,tag=bm.apgn] bm.apl 40'), at(7, 'tag @e[type=minecraft:item_display,tag=bm.apgn] remove bm.apgn'),
                          at('20..', 'function bm:p131/b/done')])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.apglob] at @s run function bm:p131/glob')
    fn('p131/glob', ['scoreboard players remove @s bm.apl 1', 'particle minecraft:item_slime ~ ~ ~ 0.1 0.1 0.1 0 2', 'particle minecraft:dust{color:[0.4,0.9,0.2],scale:1} ~ ~ ~ 0.1 0.1 0.1 0 2',
                     f'execute if entity {pl(1.6)} run return run function bm:p131/splash',
                     'execute if score @s bm.apl matches ..0 run return run function bm:p131/splash',
                     'execute positioned ^ ^ ^0.8 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p131/splash',
                     f'execute if entity {pl(30)} facing entity @p[gamemode=!creative,gamemode=!spectator] eyes rotated ~ ~ run tp @s ^ ^ ^0.8 ~ ~',
                     f'execute unless entity {pl(30)} run tp @s ^ ^ ^0.8'])
    fn('p131/splash', ['particle minecraft:item_slime ~ ~ ~ 1.2 0.6 1.2 0.2 50', 'particle minecraft:dust{color:[0.4,0.9,0.2],scale:2} ~ ~ ~ 1.4 0.6 1.4 0 30',
                       'playsound minecraft:entity.slime.squish_small hostile @a[distance=..24] ~ ~ ~ 1.5 0.5',
                       'execute as @a[distance=..3,gamemode=!creative,gamemode=!spectator] at @s run function bm:p131/splashed', 'kill @s'])
    fn('p131/splashed', ['execute if entity @e[type=minecraft:husk,tag=bm.apboss,distance=..48] run damage @s 14 minecraft:mob_projectile by @e[type=minecraft:husk,tag=bm.apboss,limit=1,sort=nearest]',
                         'execute unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..48] run damage @s 14 minecraft:mob_projectile',
                         'effect give @s minecraft:poison 5 1', 'effect give @s minecraft:wither 5 0'])
    # THE SERPENT'S JUDGEMENT (2.80): the emerald in his crown blazes - a ring of fire marks the ground under each of you, closing
    # as it counts down, and then it erupts. Nothing turns it: not armour, not Protection, not Resistance, not a shield - only being
    # out of the ring when it goes (bm:apo_judgement). The Unbound king's is violet, wider and quicker, and comes twice.
    jcol = {1: (0.3, 1.0, 0.45), 2: (0.7, 0.45, 1.0)}
    JR, JT, JD = {1: 3.0, 2: 3.5}, {1: 36, 2: 30}, {1: 16, 2: 20}         # (radius, ticks to get out - 1.8 s, 1.5 s: a sprint clears it with ping to spare - damage)
    fn('p131/b/a_judge', [at(1, face_t), at(1, 'function bm:p131/b/pose/cast'), at(1, bface('smug')),
                          at(1, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 2 0.7'),
                          at('1..30', 'particle minecraft:dust{color:[0.3,1.0,0.45],scale:1.6} ~ ~6.4 ~ 0.5 0.3 0.5 0 3'),
                          at(4, 'function bm:p131/b/judge_mark {k:1}'), at(4, apchat('Kneel.', '@a[distance=..48]')),
                          at(32, 'function bm:p131/b/pose/roar'), at(44, 'function bm:p131/b/pose/battle'), at('50..', 'function bm:p131/b/done')])
    fn('p131/b/a_judge2', [at(1, 'function bm:p131/b/pose/eth_cast'), at(1, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 2 0.9'),
                           at('1..52', 'particle minecraft:dust{color:[0.7,0.45,1.0],scale:1.6} ~ ~6 ~ 0.6 0.4 0.6 0 3'),
                           at(3, 'function bm:p131/b/judge_mark {k:2}'), at(3, apchat('BOW.', '@a[distance=..48]')),
                           at(30, 'function bm:p131/b/judge_mark {k:2}'), at(30, 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 2 1.1'),
                           at(56, 'function bm:p131/b/pose/eth_hover'), at('62..', 'function bm:p131/b/done')])
    fn('p131/b/judge_mark', [f'$execute as {pl(40)} at @s run summon minecraft:marker ~ ~ ~ {{Tags:["bm.apjm","bm.apjm$(k)","bm.apjn"]}}',
                             'execute if entity @s[scores={bm.apph=1}] run scoreboard players set @e[type=minecraft:marker,tag=bm.apjn] bm.apl ' + str(JT[1]),
                             'execute if entity @s[scores={bm.apph=2}] run scoreboard players set @e[type=minecraft:marker,tag=bm.apjn] bm.apl ' + str(JT[2]),
                             'tag @e[type=minecraft:marker,tag=bm.apjn] remove bm.apjn',
                             f'execute as {pl(40)} at @s run playsound minecraft:block.respawn_anchor.charge hostile @s ~ ~ ~ 1 0.6',
                             title(pl(40), 'actionbar', T('The ground under you burns - GET OUT OF THE RING!', GRN, bold=True))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.apjm] at @s run function bm:p131/jm')
    fn('p131/jm', ['scoreboard players remove @s bm.apl 1', 'execute if block ~ ~-0.2 ~ #bm:grap_pass run tp @s ~ ~-0.25 ~',
                   'execute if entity @s[tag=bm.apjm1] run function bm:p131/jm1', 'execute if entity @s[tag=bm.apjm2] run function bm:p131/jm2'])
    for k in (1, 2):
        c, R = jcol[k], JR[k]
        dust = f'minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:1.3}}'
        rim = [f'particle {dust} ~{R * math.cos(2 * math.pi * i / 24):.2f} ~0.15 ~{R * math.sin(2 * math.pi * i / 24):.2f} 0 0 0 0 1' for i in range(24)]
        fn(f'p131/jm{k}_rim', rim)
        steps = (0.25, 0.5, 0.75)                                      # (the closing ring: in from the rim as the count runs down)
        for j, f_ in enumerate(steps):
            r = R * (1 - f_)
            fn(f'p131/jm{k}_in{j}', [f'particle {dust} ~{r * math.cos(2 * math.pi * i / 16):.2f} ~0.2 ~{r * math.sin(2 * math.pi * i / 16):.2f} 0 0 0 0 1' for i in range(16)])
        T0 = JT[k]
        fn(f'p131/jm{k}', ['execute if score @s bm.apl matches ..0 run return run function bm:p131/jm' + str(k) + '_go',
                           'execute store result score #j bm.rng run scoreboard players get @s bm.apl', 'scoreboard players operation #j bm.rng %= #2 bm.rng',
                           f'execute if score #j bm.rng matches 0 run function bm:p131/jm{k}_rim'] +
           [f'execute if score @s bm.apl matches {max(1, int(T0 * (1 - f_)) - 2)}..{int(T0 * (1 - f_))} run function bm:p131/jm{k}_in{j}' for j, f_ in enumerate(steps)] +
           [f'particle minecraft:soul_fire_flame ~ ~0.2 ~ {R / 2:.1f} 0 {R / 2:.1f} 0.01 2',
            'execute if score @s bm.apl matches 10 run playsound minecraft:block.note_block.basedrum hostile @a[distance=..16] ~ ~ ~ 1.5 0.5',
            'execute if score @s bm.apl matches 5 run playsound minecraft:block.note_block.basedrum hostile @a[distance=..16] ~ ~ ~ 1.5 0.7'])
        fn(f'p131/jm{k}_go', [f'particle {dust.replace("scale:1.3", "scale:2.4")} ~ ~1.5 ~ {R / 2:.1f} 1.4 {R / 2:.1f} 0 90',
                              f'particle minecraft:soul_fire_flame ~ ~0.4 ~ {R / 2:.1f} 0.2 {R / 2:.1f} 0.15 60',
                              'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:explosion ~ ~0.5 ~ 0.6 0.2 0.6 0 3',
                              'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..32] ~ ~ ~ 1.2 0.8',
                              f'execute positioned ~ ~1 ~ as @a[distance=..{R + 0.3:.1f},gamemode=!creative,gamemode=!spectator] at @s run function bm:p131/judged{k}',
                              'kill @s'])
        fn(f'p131/judged{k}', [f'execute if entity @e[type=minecraft:husk,tag=bm.apboss,distance=..64] run return run function bm:p131/judged{k}_by',
                               f'damage @s {JD[k]} bm:apo_judgement', 'effect give @s minecraft:wither 4 1'])
        fn(f'p131/judged{k}_by', [f'damage @s {JD[k]} bm:apo_judgement by @e[type=minecraft:husk,tag=bm.apboss,limit=1,sort=nearest]', 'effect give @s minecraft:wither 4 1',
                                  'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 8'])
    # (a ring never outlives him)
    second.append('execute as @e[type=minecraft:marker,tag=bm.apjm] at @s unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..64] run kill @s')
    wjson('bm/damage_type/apo_judgement.json', {'exhaustion': 0.0, 'message_id': 'bm.apo_judgement', 'scaling': 'never', 'effects': 'burning'})
    for tg in ('bypasses_armor', 'bypasses_enchantments', 'bypasses_resistance', 'bypasses_shield'):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:apo_judgement'] + ['bm:apo_judgement']})
    # THE COURT (once, at three quarters): a roar - and the drowned of his sunken court climb up out of the floor
    court = {'Tags': ['bm.apcourt', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Drowned Courtier', '#5ab89a'), 'DeathLootTable': 'minecraft:empty',
             'Health': F(34), 'attributes': [{'id': 'minecraft:max_health', 'base': D(34)}, {'id': 'minecraft:attack_damage', 'base': D(9)}, {'id': 'minecraft:follow_range', 'base': D(40)}],
             'equipment': {'mainhand': {'id': 'minecraft:trident', 'count': Int(1)}, 'head': {'id': 'minecraft:golden_helmet', 'count': Int(1)}},
             'drop_chances': {'mainhand': F(0.0), 'head': F(0.0)}}
    fn('p131/b/a_court', [at(1, 'function bm:p131/b/pose/roar'), at(1, bface('shock')), at(1, 'scoreboard players set @s bm.apr 1'),
                          at(1, 'playsound minecraft:entity.ravager.roar hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
                          at(1, 'playsound minecraft:entity.drowned.ambient_water hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
                          at(10, title('@a[distance=..48]', 'actionbar', T('"RISE, MY COURT. YOUR KING HAS NEED OF YOU."', GRN, bold=True)))] +
       [at(10, f'execute positioned ^{x} ^ ^{z} run function bm:p131/b/court_at') for x, z in ((5, 3), (-5, 3), (4, -4), (-4, -4))] +
       [at(10, f'execute positioned ^{x} ^ ^{z} run particle minecraft:block{{block_state:"minecraft:dark_prismarine"}} ~ ~0.5 ~ 0.4 0.5 0.4 0 30') for x, z in ((5, 3), (-5, 3), (4, -4), (-4, -4))] +
       [at(24, bface(None)), at('34..', 'function bm:p131/b/done')])
    # (2.77c: a courtier only ever climbs out where there's room for him - feet and head clear, here or a step or two up; failing
    #  that, beside the king himself - never inside the floor, a step or a column, where one once suffocated)
    clear = 'if block ~ ~ ~ #minecraft:replaceable if block ~ ~1 ~ #minecraft:replaceable'
    fn('p131/b/court_at', [f'execute {clear} run return run function bm:p131/b/court_one',
                           f'execute positioned ~ ~1 ~ {clear} run return run function bm:p131/b/court_one',
                           f'execute positioned ~ ~2 ~ {clear} run return run function bm:p131/b/court_one',
                           'execute at @s run function bm:p131/b/court_one'])
    fn('p131/b/court_one', [f'summon minecraft:drowned ~ ~ ~ {snbt(court)}'])
    # THE SERPENT UNBOUND (at half - 2.77b: a feint first). He falls: the bar goes, his court crumbles with him, he sinks onto his coils
    # and lies still - long enough for Emma, Cecil and Leo to wonder. Then a heartbeat; his eyes snap open; he laughs - and tears out
    # of his scales, the ethereal king, wings unfurling, and takes to the air (13 s, invulnerable throughout: nothing is won here).
    vcol = 'minecraft:dust{color:[0.7,0.45,1.0],scale:2.2}'
    fn('p131/b/a_ascend', [at(1, 'data merge entity @s {Invulnerable:1b,NoAI:1b}'), at(1, 'bossbar set bm:apob visible false'),
                           at(1, 'function bm:p131/b/pose/tired'), at(1, bface('hurt')),
                           at(1, 'playsound minecraft:entity.ravager.hurt hostile @a[distance=..64] ~ ~ ~ 2 0.4'),
                           at(1, 'playsound minecraft:entity.ender_dragon.hurt hostile @a[distance=..64] ~ ~ ~ 1.5 0.5'),
                           at(1, 'particle minecraft:dust{color:[0.3,0.9,0.45],scale:2} ~ ~2 ~ 2 2 2 0 90'),
                           at(1, 'execute as @e[type=minecraft:drowned,tag=bm.apcourt,distance=..64] at @s run function bm:p131/vex_go'),
                           at(1, 'kill @e[type=minecraft:item_display,tag=bm.apglob,distance=..64]'),
                           at(10, 'playsound minecraft:entity.ravager.death hostile @a[distance=..64] ~ ~ ~ 1 0.5'),
                           at(12, 'function bm:p131/b/pose/defeated'), at('12..31', 'tp @s ~ ~-0.03 ~'),
                           at('12..40', 'particle minecraft:dust{color:[0.3,0.9,0.45],scale:1.2} ~ ~0.5 ~ 1.4 0.3 1.4 0 3'),
                           at(30, bface('blink')),
                           at(42, chat('Emma', 'Is he... did we...?', '@a[distance=..64]')),
                           at(78, chat('Cecil', 'Please be dead. Please, PLEASE be dead.', '@a[distance=..64]')),
                           at(112, chat('Leo', "Stay back, Princess. Serpents play dead.", '@a[distance=..64]'))] +
       [at(t, f'playsound minecraft:entity.warden.heartbeat hostile @a[distance=..64] ~ ~ ~ {v} {pt}') for t, v, pt in ((128, 1.0, 0.5), (146, 1.3, 0.55), (160, 1.6, 0.6), (170, 2.0, 0.65))] +
       [at('128..175', 'particle minecraft:dust{color:[0.7,0.45,1.0],scale:1.0} ~ ~0.8 ~ 1.2 0.4 1.2 0 2'),
        at(146, 'function bm:p131/b/posen/idle_a'),
        # (the eyes, and the laugh)
        at(176, bface('shock')), at(176, 'playsound minecraft:entity.witch.celebrate hostile @a[distance=..64] ~ ~ ~ 2 0.5'),
        at(176, 'playsound minecraft:entity.cat.hiss hostile @a[distance=..64] ~ ~ ~ 2 0.4'),
        at(176, apchat('Hsss... hss-hss-HSSS. Did you really think the Hollow would let me die so EASILY?', '@a[distance=..64]')),
        # (the change: the scales crack, the dark swirls up round him - and the ethereal king tears free)
        at(190, 'function bm:p131/b/pose/roar'), at(190, bface('smug')),
        at(190, 'playsound minecraft:entity.wither.spawn hostile @a[distance=..64] ~ ~ ~ 1 0.6'),
        at(190, 'playsound minecraft:block.portal.trigger hostile @a[distance=..64] ~ ~ ~ 1 0.5'),
        at('190..230', f'particle {vcol} ~ ~3 ~ 1.5 2.5 1.5 0 10'),
        at('190..230', 'particle minecraft:reverse_portal ~ ~3 ~ 2 3 2 0.3 14'),
        at('190..230', 'particle minecraft:large_smoke ~ ~2 ~ 1.4 1.6 1.4 0.02 6'),
        at('190..210', 'tp @s ~ ~0.03 ~')] +
       [at(t, 'particle minecraft:block{block_state:"minecraft:dark_prismarine"} ~ ~3 ~ 1.4 2 1.4 0.3 30') for t in range(194, 231, 6)] +
       [at(t, 'playsound minecraft:block.deepslate_tiles.break hostile @a[distance=..64] ~ ~ ~ 1.5 0.5') for t in range(194, 231, 6)] +
       [at(205, apchat('That "king" wore a SLIVER of my power - and you could barely stand against HIM. Now face ALL of it!', '@a[distance=..64]')),
        at(215, 'playsound minecraft:item.trident.thunder hostile @a[distance=..64] ~ ~ ~ 1.5 0.6'),
        at(232, 'particle minecraft:flash{color:[0.75,0.5,1.0,1.0]} ~ ~3 ~ 0 0 0 0 1'), at(232, 'particle minecraft:explosion_emitter ~ ~2 ~ 0 0 0 0 1'),
        at(232, 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..64] ~ ~ ~ 2 0.7'),
        at(232, 'scoreboard players set @s bm.apph 2'), at(232, 'function bm:p131/b/look_eth'),
        at(232, 'execute store result entity @s Health float 1 run attribute @s minecraft:max_health get'),     # (2.80: whole again - the second half is a fight of its own) at(232, 'function bm:p131/b/pose/eth_hover'),
        # (his wings unfurl slower than the rest of him moves)
        at(232, f'execute as {bsel("wingr")} run data merge entity @s {{interpolation_duration:30}}'),
        at(232, f'execute as {bsel("wingl")} run data merge entity @s {{interpolation_duration:30}}'),
        at(232, 'data merge entity @s {NoAI:1b,NoGravity:1b}'), at(232, bface(None)),
        at(232, 'title @a[distance=..64] times 5 70 20'), at(232, title('@a[distance=..64]', 'title', T('THE SERPENT UNBOUND', VIOLET, bold=True))),
        at(232, title('@a[distance=..64]', 'subtitle', T('Something vast and winged tears free of his scales.', 'gray', italic=True))),
        at(234, apchat('You want to see what the Hollow made of me? LOOK.', '@a[distance=..64]')),
        at('233..256', 'execute if block ~ ~6 ~ #bm:grap_pass run tp @s ~ ~0.22 ~'),
        at(244, 'bossbar set bm:apob name {text:"Apophiss, Unbound",color:"light_purple"}'), at(244, 'bossbar set bm:apob color purple'),
        at(244, 'bossbar set bm:apob visible true'),
        at(258, 'data merge entity @s {Invulnerable:0b}'), at('260..', 'function bm:p131/b/done')])
    # ---- phase 2
    orb = snbt({'Tags': ['bm.aporb', 'bm.apon'], 'item': {'id': 'minecraft:ender_eye', 'count': Int(1)}, 'item_display': 'fixed', 'teleport_duration': Int(1),
                'brightness': {'block': Int(15), 'sky': Int(15)}, 'Glowing': B(1), 'glow_color_override': Int(0xb07aff),
                'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(1.2)] * 3}})
    # VOID ORBS: three, one at a time, slow and homing; where they burst, a pool of dark that bites
    fn('p131/b/a_orbs', [at(1, 'function bm:p131/b/pose/eth_cast'), at(1, 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..48] ~ ~ ~ 1 1.2')] +
       [at(t, f'execute facing entity @a[distance=..48,gamemode=!creative,gamemode=!spectator,sort=random,limit=1] eyes positioned ^ ^4 ^2 run function bm:p131/b/orb') for t in (10, 18, 26)] +
       [at(36, 'function bm:p131/b/pose/eth_hover'), at('40..', 'function bm:p131/b/done')])
    fn('p131/b/orb', [f'summon minecraft:item_display ~ ~ ~ {orb}', 'tp @e[type=minecraft:item_display,tag=bm.apon,limit=1,sort=nearest] ~ ~ ~ ~ ~',
                      'execute as @a[distance=..48,gamemode=!creative,gamemode=!spectator,sort=nearest,limit=1] run tag @s add bm.aporbt',
                      'scoreboard players set @e[type=minecraft:item_display,tag=bm.apon,limit=1,sort=nearest] bm.apl 70',
                      'tag @e[type=minecraft:item_display,tag=bm.apon] remove bm.apon', 'tag @a remove bm.aporbt',
                      'playsound minecraft:entity.ender_dragon.shoot hostile @a[distance=..40] ~ ~ ~ 1 0.6'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.aporb] at @s run function bm:p131/orb')
    fn('p131/orb', ['scoreboard players remove @s bm.apl 1', 'particle minecraft:dragon_breath ~ ~ ~ 0.15 0.15 0.15 0.01 3', 'particle minecraft:portal ~ ~ ~ 0.2 0.2 0.2 0.3 4',
                    f'execute if entity {pl(1.6)} run return run function bm:p131/orb_burst',
                    'execute if score @s bm.apl matches ..0 run return run function bm:p131/orb_burst',
                    'execute positioned ^ ^ ^0.5 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p131/orb_burst',
                    f'execute if entity {pl(40)} facing entity @p[gamemode=!creative,gamemode=!spectator] eyes rotated ~ ~ run tp @s ^ ^ ^0.5 ~ ~',
                    f'execute unless entity {pl(40)} run tp @s ^ ^ ^0.5'])
    pool = snbt({'Radius': F(2.6), 'Duration': Int(120), 'RadiusPerTick': F(0.0), 'ReapplicationDelay': Int(20), 'WaitTime': Int(0),
                 'custom_particle': {'type': 'minecraft:dragon_breath'}, 'Tags': ['bm.appool'],
                 'potion_contents': {'custom_effects': [{'id': 'minecraft:instant_damage', 'amplifier': B(0), 'duration': Int(1)},
                                                        {'id': 'minecraft:wither', 'amplifier': B(0), 'duration': Int(60)}]}})
    fn('p131/orb_burst', ['particle minecraft:dragon_breath ~ ~ ~ 0.8 0.8 0.8 0.05 60', 'particle minecraft:flash{color:[0.7,0.45,1.0,1.0]} ~ ~ ~ 0 0 0 0 1',
                      'playsound minecraft:entity.dragon_fireball.explode hostile @a[distance=..32] ~ ~ ~ 1 0.8',
                      'execute as @a[distance=..2.6,gamemode=!creative,gamemode=!spectator] at @s run function bm:p131/burned',
                      f'execute align y positioned ~ ~0.1 ~ run summon minecraft:area_effect_cloud ~ ~ ~ {pool}', 'kill @s'])
    fn('p131/burned', ['execute if entity @e[type=minecraft:husk,tag=bm.apboss,distance=..60] run damage @s 13 minecraft:indirect_magic by @e[type=minecraft:husk,tag=bm.apboss,limit=1,sort=nearest]',
                       'execute unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..60] run damage @s 13 minecraft:magic', 'effect give @s minecraft:wither 4 1'])
    # (the pools never outlive him)
    second.append('execute in bm:hollow_throne as @e[type=minecraft:area_effect_cloud,tag=bm.appool] unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..60] run kill @s')
    # THE SWOOP: he climbs, folds his wings - and dives through you
    fn('p131/b/a_swoop', [at(1, 'function bm:p131/b/pose/eth_beat'), at(1, 'tag @a remove bm.apsw'),
                          at(1, f'tag {pl(30, ",sort=random,limit=1")} add bm.apsw'),
                          at(1, 'playsound minecraft:entity.phantom.swoop hostile @a[distance=..48] ~ ~ ~ 1.5 0.5'),
                          at('2..10', 'execute if block ~ ~7 ~ #bm:grap_pass run tp @s ~ ~0.2 ~'),
                          at('2..10', 'execute facing entity @a[tag=bm.apsw,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
                          at(11, 'function bm:p131/b/pose/eth_bdive'), at(14, 'function bm:p131/b/pose/eth_dive'), at(11, 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..48] ~ ~ ~ 1.2 1.4'),
                          at('12..34', 'function bm:p131/b/dive'),
                          at(35, 'function bm:p131/b/pose/eth_bdive'), at(39, 'function bm:p131/b/pose/eth_beat'), at('36..52', 'execute if block ~ ~6 ~ #bm:grap_pass run tp @s ~ ~0.3 ~'),
                          at('54..', 'function bm:p131/b/done')])
    fn('p131/b/dive', ['execute unless entity @a[tag=bm.apsw] run return run scoreboard players set @s bm.apt 34',
                       'execute facing entity @a[tag=bm.apsw,limit=1] feet positioned ^ ^ ^1 if block ~ ~0.5 ~ #bm:grap_pass run tp @s ~ ~ ~ facing entity @a[tag=bm.apsw,limit=1] feet',
                       'particle minecraft:dust{color:[0.7,0.45,1.0],scale:2} ~ ~2 ~ 1 1 1 0 8', 'particle minecraft:cloud ~ ~1 ~ 0.6 0.6 0.6 0.02 3',
                       f'execute as {pl(3.4, ",tag=!bm.aphitp")} at @s run function bm:p131/b/swooped',
                       'execute if entity @a[tag=bm.apsw,distance=..2.2] run scoreboard players set @s bm.apt 34',
                       'execute unless block ~ ~-0.6 ~ #bm:grap_pass run scoreboard players set @s bm.apt 34'])
    fn('p131/b/swooped', ['tag @s add bm.aphitp', f'damage @s 30 minecraft:mob_attack by {me}', 'particle minecraft:crit ~ ~1 ~ 0.3 0.5 0.3 0.4 20',
                          'playsound minecraft:entity.player.attack.knockback hostile @a[distance=..24] ~ ~ ~ 1 0.6'])
    # THE WINGBEAT: three great beats - and you're thrown back
    fn('p131/b/a_gust', [at(1, 'function bm:p131/b/pose/eth_beat'), at(4, 'function bm:p131/b/pose/eth_hover'), at(7, 'function bm:p131/b/pose/eth_beat'),
                         at(10, 'function bm:p131/b/pose/eth_hover'), at(13, 'function bm:p131/b/pose/eth_beat')] +
       [at(t, 'playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..48] ~ ~ ~ 2 0.6') for t in (1, 7, 13)] +
       [at(14, 'particle minecraft:cloud ~ ~ ~ 5 1 5 0.3 120'), at(14, 'particle minecraft:sweep_attack ~ ~1 ~ 4 0.5 4 0 12'),
        at(14, f'execute as {pl(11)} run function bm:p131/b/gusted'), at('24..', 'function bm:p131/b/done')])
    fn('p131/b/gusted', [f'damage @s 12 minecraft:mob_attack by {me}', 'effect give @s minecraft:levitation 1 2 true', 'effect give @s minecraft:slow_falling 4 0 true'])
    # GRAND FANGS: he comes down hard - rings of fangs, out and out
    fn('p131/b/a_grand', [at(1, 'function bm:p131/b/pose/eth_hdive'), at(5, 'function bm:p131/b/pose/eth_dive'), at(1, 'playsound minecraft:entity.ender_dragon.growl hostile @a[distance=..48] ~ ~ ~ 1.5 0.5'),
                          at('2..22', 'execute if block ~ ~-0.6 ~ #bm:grap_pass run tp @s ~ ~-0.45 ~'),
                          at(20, 'function bm:p131/b/pose/eth_dland'), at(23, 'function bm:p131/b/pose/eth_land'), at(24, 'function bm:p131/b/ring3'),
                          at(24, 'particle minecraft:explosion ~ ~0.3 ~ 2 0.1 2 0 8'), at(24, 'playsound minecraft:item.mace.smash_ground_heavy hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'),
                          at(24, f'execute as {pl(4)} run damage @s 18 minecraft:mob_attack by {me}'),
                          at(44, 'function bm:p131/b/pose/eth_lift'), at(48, 'function bm:p131/b/pose/eth_beat'),
                          at('46..62', 'execute if block ~ ~6 ~ #bm:grap_pass run tp @s ~ ~0.3 ~'), at('64..', 'function bm:p131/b/done')])
    ring = []
    for rr, nf, w in ((3, 8, 0), (5, 12, 6), (7, 16, 12)):
        for i in range(nf):
            a = 2 * math.pi * i / nf
            ring.append(f'summon minecraft:evoker_fangs ~{rr * math.cos(a):.2f} ~ ~{rr * math.sin(a):.2f} {{Warmup:{w}}}')
    fn('p131/b/ring3', ['execute align y run function bm:p131/b/ring3_at', 'playsound minecraft:entity.evoker.cast_spell hostile @a[distance=..40] ~ ~ ~ 1.5 0.5'])
    fn('p131/b/ring3_at', ring)
    # THE CALL: spectral serpents out of the dark (never more than three)
    vexn = {'Tags': ['bm.apvex', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Spectral Serpent', VIOLET), 'Glowing': B(1), 'DeathLootTable': 'minecraft:empty',
            'Health': F(18), 'attributes': [{'id': 'minecraft:max_health', 'base': D(18)}, {'id': 'minecraft:attack_damage', 'base': D(8)}]}
    fn('p131/b/a_call', [at(1, 'function bm:p131/b/pose/eth_cast'), at(1, 'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..48] ~ ~ ~ 1.5 0.6'),
                         at(12, f'execute positioned ^3 ^2 ^2 run summon minecraft:vex ~ ~ ~ {snbt(vexn)}'), at(12, f'execute positioned ^-3 ^2 ^2 run summon minecraft:vex ~ ~ ~ {snbt(vexn)}'),
                         at(12, 'particle minecraft:dragon_breath ~ ~2 ~ 3 1 3 0.02 40'), at('24..', 'function bm:p131/b/done')])
    second.append('execute as @e[type=minecraft:vex,tag=bm.apvex] at @s unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..64] run function bm:p131/vex_go')
    second.append('execute as @e[type=minecraft:drowned,tag=bm.apcourt] at @s unless entity @e[type=minecraft:husk,tag=bm.apboss,distance=..64] run function bm:p131/vex_go')
    fn('p131/vex_go', ['particle minecraft:dragon_breath ~ ~0.6 ~ 0.3 0.4 0.3 0.02 16', 'tp @s ~ -400 ~', 'kill @s'])
    # each blow on him: a hiss and a hurt look (he's Silent - these are his own)
    wjson('bm/advancement/p131/hit.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.apboss"]}'}}]}}}, 'rewards': {'function': 'bm:p131/hit'}})
    fn('p131/hit', ['advancement revoke @s only bm:p131/hit', 'execute at @s as @e[type=minecraft:husk,tag=bm.apboss,distance=..48,limit=1,sort=nearest] at @s run function bm:p131/b/ouch'])
    fn('p131/b/ouch', ['playsound minecraft:entity.ravager.hurt hostile @a[distance=..32] ~ ~ ~ 0.8 0.6', 'playsound minecraft:entity.cat.hiss hostile @a[distance=..32] ~ ~ ~ 1 0.5',
                       'particle minecraft:dust{color:[0.25,0.8,0.35],scale:1.2} ~ ~3 ~ 0.8 1.2 0.8 0 8'])
    # every second: the bar, and whether anyone's still here
    second += ['bossbar set bm:apob players', 'execute as @e[type=minecraft:husk,tag=bm.apboss] at @s run function bm:p131/b/sec']
    fn('p131/b/sec', ['execute store result bossbar bm:apob value run data get entity @s Health', 'execute store result bossbar bm:apob max run attribute @s minecraft:max_health get',
                      'execute if score @s bm.apph matches 1.. run bossbar set bm:apob players @a[distance=..48]',
                      'data modify entity @s InWaterTime set value -1',
                      'execute if entity @a[distance=..48,gamemode=!spectator] run scoreboard players set @s bm.aplone 0',
                      'execute unless entity @a[distance=..48,gamemode=!spectator] run scoreboard players add @s bm.aplone 1',
                      'execute if score @s bm.aplone matches 30.. run function bm:p131/b/leave'])
    # (2.78: his chunk unloaded a minute or more - everyone died or went far, and he sat frozen where they left him: the fight is over.
    #  And a death with nobody else near him ends it at once.)
    G.FUNCS['p131/b/sec'][0:0] = ['execute store result score #now bm.rng run time query gametime',
                                  'execute unless score @s bm.apseen matches 1.. run scoreboard players operation @s bm.apseen = #now bm.rng',
                                  'scoreboard players operation #gap bm.rng = #now bm.rng', 'scoreboard players operation #gap bm.rng -= @s bm.apseen',
                                  'scoreboard players operation @s bm.apseen = #now bm.rng',
                                  'execute if score #gap bm.rng matches 1200.. run return run function bm:p131/b/leave']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.apseen dummy']
    G.OBJECTIVES += ['bm.apseen']
    fn('p131/b/died', ['tag @s add bm.dying', 'execute as @e[type=minecraft:husk,tag=bm.apboss,distance=..96] at @s unless entity @a[tag=!bm.dying,distance=..64,gamemode=!spectator] run function bm:p131/b/leave', 'tag @s remove bm.dying'])
    G.FUNCS['p62/died'][0:0] = ['execute at @s run function bm:p131/b/died']
    fn('p131/b/leave', ['bossbar set bm:apob visible false', 'function bm:p131/b/unrig', 'function bm:p131/b/vx_end', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p131/b/unrig', ['scoreboard players operation #aid bm.rng = @s bm.apid',
                        'execute as @e[type=minecraft:item_display,tag=bm.apb,distance=..40] if score @s bm.apid = #aid bm.rng run kill @s'])
    # ---- he falls (2.77c): the rig with no host. He roars and the den shakes; the dark gathers into him, his scales go black, he
    #      trembles - and bursts into black magic. It whirls round where he was, and a seal opens in the floor beneath it and drags
    #      it down, and closes. His crown, left in the air where his head was, drifts slowly down for whoever earned it. The win is
    #      everyone's who was here when he fell (within 48).
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.apb,tag=bm.app_coil,tag=!bm.apdie] at @s if entity @a[distance=..96] run function bm:p131/b/orphan')
    # (once per boss, whatever happens: he is gone only if no husk of his is anywhere; a copy of his rig found after he has begun
    #  to fall - or far from the rest - is a stray, and just goes)
    fn('p131/b/orphan', ['scoreboard players operation #aid bm.rng = @s bm.apid',
                         'execute as @e[type=minecraft:husk,tag=bm.apboss] if score @s bm.apid = #aid bm.rng run return 0',
                         'execute as @e[type=minecraft:marker,tag=bm.apend] if score @s bm.apid = #aid bm.rng run return run function bm:p131/b/strays',
                         'execute as @e[type=minecraft:item_display,tag=bm.apb] if score @s bm.apid = #aid bm.rng unless entity @s[distance=..32] run kill @s',
                         'execute as @e[type=minecraft:item_display,tag=bm.apb,distance=..32] if score @s bm.apid = #aid bm.rng run tag @s add bm.apdie',
                         'bossbar set bm:apob visible false', 'kill @e[type=minecraft:item_display,tag=bm.aporb,distance=..64]', 'tag @a remove bm.aptgt', 'tag @a remove bm.apsw',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.apend","bm.apenew"]}',
                         'execute as @e[type=minecraft:marker,tag=bm.apenew,distance=..1] at @s run function bm:p131/d/init',
                         'execute as @a[distance=..48,gamemode=!spectator] run function bm:p131/d/claim'])
    fn('p131/b/strays', ['execute as @e[type=minecraft:item_display,tag=bm.apb,tag=!bm.apdie] if score @s bm.apid = #aid bm.rng run kill @s'])
    fn('p131/d/init', ['scoreboard players operation @s bm.apid = #aid bm.rng', 'scoreboard players set @s bm.apt 0', 'tag @s remove bm.apenew',
                       'scoreboard players set #fl bm.rng 48', 'function bm:p131/d/floor',
                       'scoreboard players operation @e[type=minecraft:marker,tag=bm.apenew,distance=..30] bm.apid = #aid bm.rng',
                       'tag @e[type=minecraft:marker,tag=bm.apenew,distance=..30] remove bm.apenew'])
    # (where the floor is under him - he may have died in the air)
    fn('p131/d/floor', ['execute unless block ~ ~-0.5 ~ #bm:grap_pass align y run return run summon minecraft:marker ~ ~ ~ {Tags:["bm.apflr","bm.apenew"]}',
                        'scoreboard players remove #fl bm.rng 1', 'execute if score #fl bm.rng matches 1.. positioned ~ ~-0.5 ~ run function bm:p131/d/floor'])
    # (what each of them has won is settled now: the crown falls only if it falls for someone)
    fn('p131/d/claim', ['tag @s add bm.apwin', 'scoreboard players add @s bm.apk 1', 'execute if score @s bm.apk matches 1 run tag @s add bm.apcrown',
                        'execute if score @s bm.apk matches 2.. store result score #r bm.rng run random value 1..100',
                        'execute if score @s bm.apk matches 2.. if score #r bm.rng matches 1..15 run tag @s add bm.apcrown',
                        'execute if score @s bm.apk matches 2.. if score #r bm.rng matches 16..30 run tag @s add bm.apmace',
                        'execute if score @s bm.apk matches 2.. if score #r bm.rng matches 31..38 run tag @s add bm.apoath'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.apend] at @s run function bm:p131/d/tick')
    fn('p131/d/tick', ['scoreboard players add @s bm.apt 1', 'scoreboard players operation #aid bm.rng = @s bm.apid',
                       'execute if score @s bm.apt matches ..54 as @e[type=minecraft:item_display,tag=bm.apdie,distance=..40] if score @s bm.apid = #aid bm.rng run tag @s add bm.apsel',
                       'function bm:p131/d/seq', f'tag {bsel()} remove bm.apsel'])
    # (the vortex of his black magic, tick by tick: radius, turn a tick, how far below the marker - it ends under the floor)
    def vxd_at(t):
        e = lambda k: k * k * (3 - 2 * k)
        if t < 8: return 6.0, 4.0, -0.4
        if t < 48: k = (t - 8) / 40; return 6.0 - 4.6 * e(k), 4 + 30 * k, -0.4 + 0.4 * k
        if t < 54: k = (t - 48) / 6; return 1.4 + 6.6 * (1 - (1 - k) ** 2), 34 - 26 * k, 0.0
        if t < 90: k = (t - 54) / 36; return 8.0 - 4.0 * e(k), 8 + 8 * k, 0.0
        if t < 128: k = (t - 90) / 38; return 4.0 - 3.4 * e(k), 16 + 28 * k, -7.5 * k ** 1.6
        return 0.6, 44.0, -7.5
    G.FUNCS['load'][-1:-1] = ['data modify storage bm:p131 vxd set value [' + ','.join('{r:%.3fd,s:%.2fd,y:%.3fd}' % vxd_at(t) for t in range(171)) + ']']
    fn('p131/d/vx', ['execute store result storage bm:p131 vi.t int 1 run scoreboard players get @s bm.apt', 'function bm:p131/d/vx_pick with storage bm:p131 vi',
                     'function bm:p131/b/vx_spin with storage bm:p131 vx'])
    fn('p131/d/vx_pick', ['$data modify storage bm:p131 vx set from storage bm:p131 vxd[$(t)]'])
    fn('p131/d/fire', [l for i in range(VXN) for l in (f'summon minecraft:item_display ~ ~ ~ {fire(i)}',
                                                       f'scoreboard players set @e[type=minecraft:item_display,tag=bm.apfnew,limit=1] bm.apfi {i}',
                                                       'tag @e[type=minecraft:item_display,tag=bm.apfnew] remove bm.apfnew')] +
       ['execute as @e[type=minecraft:item_display,tag=bm.apfire,distance=..6] run data merge entity @s {start_interpolation:0,interpolation_duration:30,'
        'transformation:{translation:[0f,1.1f,0f],scale:[1.4f,2.2f,1.4f]}}'])
    # (the screen shakes: the view jolted and put back, tick by tick, the jolts dying away)
    rs = __import__('random').Random(131)
    def shake(t0, n, amp):
        out = []
        for i in range(0, n - 1, 2):
            a = amp * (1 - i / n)
            dx, dy = a * rs.choice((-1, 1)) * rs.uniform(0.6, 1.0), a * 0.6 * rs.choice((-1, 1)) * rs.uniform(0.6, 1.0)
            out += [at(t0 + i, f'execute as @a[distance=..64] at @s run rotate @s ~{dx:.2f} ~{dy:.2f}'),
                    at(t0 + i + 1, f'execute as @a[distance=..64] at @s run rotate @s ~{-dx:.2f} ~{-dy:.2f}')]
        return out
    # (the crown on his head in his roar, from his head's joint - his rig holds that pose from t26 (8 ticks to settle) until he bursts at t48)
    xf = RK.solve(A.PIVOT, A.PARENT, POSES['roar']); hq, ht = xf['head']
    hr = RK.qrot(hq, tuple(c - p for c, p in zip(ART.CROWN_AT, A.PIVOT["head"])))
    cx, cy, cz = (UB * (ht[i] + hr[i]) for i in range(3))
    dim = lambda b: f'execute as {bsel()} run data merge entity @s[type=minecraft:item_display] {{brightness:{{block:{b},sky:{b}}}}}'
    snd = lambda s, v, p, r=96: f'playsound minecraft:{s} hostile @a[distance=..{r}] ~ ~ ~ {v} {p}'
    flr = '@e[type=minecraft:marker,tag=bm.apflr,sort=nearest,limit=1]'
    seal = '@e[type=minecraft:item_display,tag=bm.apdseal,distance=..40]'
    fn('p131/d/seq', [l.replace(' run execute ', ' ', 1) for l in [
        # (the roar: the ethereal king is torn off him, and he rears and roars - the den shakes)
        at(1, 'function bm:p131/b/look'), at(1, 'function bm:p131/b/pose/roar'), at(1, bface('shock')),
        at(1, snd('entity.warden.roar', 3, 0.6)), at(1, snd('entity.ender_dragon.growl', 3, 0.5)), at(1, snd('entity.ravager.roar', 3, 0.4)),
        at(2, apchat('NO! Not again - not to HER!', '@a[distance=..64]')),
        at(12, 'function bm:p131/b/pose/defeated'), at(12, bface('hurt')), at(12, snd('entity.wither.ambient', 2, 0.5)),
        at(26, 'function bm:p131/b/pose/roar'), at(26, bface('shock')), at(26, snd('entity.ravager.roar', 2, 0.5)), at(26, snd('entity.warden.angry', 2, 0.5)),
        at(40, snd('entity.warden.sonic_charge', 3, 0.5)),
        # (the dark gathers into him: black fire climbs round him, closer and faster; his scales go black; he trembles)
        at(4, 'function bm:p131/d/fire'), at(4, snd('block.respawn_anchor.charge', 2, 0.5)), at(4, snd('entity.blaze.burn', 2, 0.5)),
        at('4..127', 'function bm:p131/d/vx'), at('4..108', 'function bm:p131/b/vx_flick'),
        at('6..47', 'particle minecraft:portal ~ ~3 ~ 2.5 2.5 2.5 1.2 30 force @a[distance=..96]'),
        at('6..47', 'particle minecraft:squid_ink ~ ~3 ~ 2 2.5 2 0.02 4 force @a[distance=..96]'),
        at('20..47', 'function bm:p131/b/vx_fx'),
        at(20, dim(7)), at(34, dim(3)), at(44, dim(0)), at(30, snd('block.fire.ambient', 3, 0.5)), at(40, snd('entity.wither.spawn', 1, 0.6))] +
       [at(t, f'execute as {bsel()} at @s run tp @s ~{0.12 if t % 2 else -0.12} ~ ~') for t in range(30, 48)] +
       shake(1, 40, 2.6) +
       [# (he bursts into black magic - his crown left hanging where his head was)
        at(48, 'function bm:p131/d/burst'),
        at(48, f'execute if entity @a[tag=bm.apcrown] as {bsel("head")[:-1]},limit=1] at @s rotated as @s positioned ^{-cx:.3f} ^{cy:.3f} ^{-cz:.3f} run function bm:p131/d/crown_make'),
        at(48, f'execute at {flr} positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_4'), at(50, f'execute at {flr} positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_8'),
        at(52, f'execute at {flr} positioned ~ ~0.2 ~ run function bm:p131/b/vx_wave_12'),
        at(52, f'kill {bsel()}')] +
       shake(48, 18, 3.4) +
       [# (the black magic whirls, and sinks toward the floor; a seal opens in it, and drags the magic down)
        at('54..100', 'function bm:p131/b/vx_fx'), at(56, snd('block.portal.trigger', 1, 0.5, 64)),
        at('60..110', f'execute if entity @e[type=minecraft:marker,tag=bm.apflr,distance=0.25..14] run tp @s ~ ~-0.2 ~'),
        at(70, f'execute at {flr} run function bm:p131/d/seal_make'),
        at('70..129', f'execute as {seal} at @s run tp @s ~ ~ ~ ~3 ~'), at('130..152', f'execute as {seal} at @s run tp @s ~ ~ ~ ~12 ~')] +
       [at(t, snd('block.end_portal_frame.fill', 1.5, 0.6 + 0.08 * k)) for k, t in enumerate((70, 76, 82, 88))] +
       [at(t, f'execute at {flr} run function bm:p131/d/seal_fx') for t in range(72, 129, 3)] +
       [at(98, apchat('Hsss... seal me away, then. Again. I am patient, princess... I am so... very... patient...', '@a[distance=..64]')),
        at(100, snd('block.sculk_shrieker.shriek', 1, 0.5)),
        at(110, 'execute as @e[type=minecraft:item_display,tag=bm.apfire,distance=..40] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{scale:[0f,0f,0f]}}'),
        at(126, f'execute as {seal} run data merge entity @s {{start_interpolation:0,interpolation_duration:4,transformation:{{scale:[8.5f,8.5f,8.5f]}}}}'),
        # (it closes over him)
        at(130, 'function bm:p131/d/close'), at(130, 'function bm:p131/b/fallen')] +
       shake(130, 12, 1.6) +
       [at(160, f'kill {seal}'), at(160, 'kill @e[type=minecraft:marker,tag=bm.apflr,distance=..40]'), at(160, 'kill @s')]])
    fn('p131/d/burst', [f'execute as {bsel()} run data merge entity @s {{start_interpolation:0,interpolation_duration:3,transformation:{{scale:[0f,0f,0f]}}}}',
                        f'execute as {bsel()} at @s run particle minecraft:squid_ink ~ ~ ~ 0.6 0.6 0.6 0.35 24 force @a[distance=..96]',
                        'particle minecraft:flash{color:[0.35,0.05,0.5,1.0]} ~ ~4 ~ 0 0 0 0 1 force @a[distance=..96]',
                        'particle minecraft:explosion_emitter ~ ~3 ~ 1 1 1 0 2 force @a[distance=..96]', 'particle minecraft:sonic_boom ~ ~3 ~ 0 0 0 0 1 force @a[distance=..96]',
                        'particle minecraft:squid_ink ~ ~3 ~ 1.5 2.5 1.5 0.8 300 force @a[distance=..96]', 'particle minecraft:large_smoke ~ ~3 ~ 1.5 2.5 1.5 0.5 160 force @a[distance=..96]',
                        'particle minecraft:dust_color_transition{from_color:[0.0,0.0,0.0],to_color:[0.55,0.15,0.85],scale:3.0} ~ ~3 ~ 4 3 4 0 160 force @a[distance=..96]',
                        'particle minecraft:reverse_portal ~ ~3 ~ 1 2 1 1.5 260 force @a[distance=..96]',
                        snd('entity.generic.explode', 3, 0.5), snd('entity.warden.sonic_boom', 3, 0.6), snd('entity.wither.death', 1.2, 0.7),
                        snd('entity.lightning_bolt.thunder', 1.5, 0.6)])
    sealn = {'Tags': ['bm.apdseal'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:apo_seal_lit'}},
             'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(1), 'view_range': F(2.0),
             'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.03), F(0)], 'scale': [F(0)] * 3}}
    fn('p131/d/seal_make', ['summon minecraft:item_display ~ ~ ~ ' + snbt(sealn),
                            f'execute as {seal} run data merge entity @s {{start_interpolation:0,interpolation_duration:24,transformation:{{scale:[7f,7f,7f]}}}}',
                            'particle minecraft:dust{color:[0.3,1.0,0.45],scale:2.0} ~ ~0.2 ~ 2.5 0.05 2.5 0 80 force @a[distance=..96]',
                            snd('block.beacon.activate', 2, 0.5), snd('block.end_portal_frame.fill', 1.5, 0.5)])
    fn('p131/d/seal_fx', vring('minecraft:dust{color:[0.3,1.0,0.45],scale:1.5}', 3.4, 28, 0.1) +
       ['particle minecraft:enchant ~ ~0.4 ~ 2.6 0.1 2.6 0.6 16 force @a[distance=..96]', 'particle minecraft:end_rod ~ ~0.3 ~ 2.2 0.05 2.2 0.02 3 force @a[distance=..96]'])
    fn('p131/d/close', [f'execute as {seal} run data merge entity @s {{start_interpolation:0,interpolation_duration:22,transformation:{{scale:[0f,0f,0f]}}}}',
                        'kill @e[type=minecraft:item_display,tag=bm.apfire,distance=..40]',
                        'particle minecraft:flash{color:[0.3,1.0,0.5,1.0]} ~ ~0.5 ~ 0 0 0 0 1 force @a[distance=..96]',
                        'particle minecraft:totem_of_undying ~ ~0.5 ~ 1 0.3 1 0.6 120 force @a[distance=..96]',
                        'particle minecraft:dust{color:[0.3,1.0,0.45],scale:2.4} ~ ~0.3 ~ 3 0.2 3 0 120 force @a[distance=..96]',
                        'particle minecraft:end_rod ~ ~0.5 ~ 0.4 0.2 0.4 0.3 60 force @a[distance=..96]',
                        snd('block.end_portal.spawn', 1.5, 0.8), snd('block.beacon.deactivate', 2, 0.6)])
    # (the crown: big as it was on him at first, shrinking as it drifts down; turning, sparkling; it lands - and one lies there for
    #  each who earned it (theirs alone to pick up, and it never goes))
    crn = {'Tags': ['bm.apcrf'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:apo_true_crown',
                                                                                                   'minecraft:enchantment_glint_override': True}},
           'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(1), 'view_range': F(2.0),
           'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(-0.45), F(0)], 'scale': [F(round(ART.CROWN_K * 2.6, 3))] * 3}}
    fn('p131/d/crown_make', ['summon minecraft:item_display ~ ~ ~ ' + snbt(crn), 'scoreboard players set @e[type=minecraft:item_display,tag=bm.apcrf,distance=..1] bm.apt 0',
                             'particle minecraft:totem_of_undying ~ ~ ~ 0.3 0.3 0.3 0.3 30 force @a[distance=..96]',
                             snd('block.bell.resonate', 1.5, 0.8), snd('block.amethyst_block.resonate', 2, 0.5)])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.apcrf] at @s run function bm:p131/d/crown')
    fn('p131/d/crown', ['scoreboard players add @s bm.apt 1',
                        'execute if score @s bm.apt matches 3 run data merge entity @s {start_interpolation:0,interpolation_duration:110,transformation:{scale:[1f,1f,1f],translation:[0f,0f,0f]}}',
                        'execute if score @s bm.apt matches ..14 run tp @s ~ ~ ~ ~5 ~', 'execute if score @s bm.apt matches 15.. run function bm:p131/d/crown_fall',
                        'particle minecraft:end_rod ~ ~0.3 ~ 0.25 0.25 0.25 0.02 1 force @a[distance=..96]',
                        'particle minecraft:dust{color:[0.25,1.0,0.45],scale:0.9} ~ ~0.3 ~ 0.3 0.2 0.3 0 2 force @a[distance=..96]',
                        'scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #4 bm.rng',
                        'execute if score #f bm.rng matches 0 run particle minecraft:totem_of_undying ~ ~0.3 ~ 0.2 0.2 0.2 0.05 1 force @a[distance=..96]',
                        'execute if score #f bm.rng matches 2 run particle minecraft:witch ~ ~0.3 ~ 0.2 0.2 0.2 0 1 force @a[distance=..96]',
                        'scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #20 bm.rng',
                        'execute if score #f bm.rng matches 0 run ' + snd('block.amethyst_block.chime', 1.5, 0.6, 48),
                        'execute if score @s bm.apt matches 600.. run function bm:p131/d/crown_land'])
    deep = ' '.join(f'if block ~ ~-{k} ~ #bm:grap_pass' for k in range(1, 7))
    fn('p131/d/crown_fall', ['execute unless block ~ ~-0.2 ~ #bm:grap_pass run return run function bm:p131/d/crown_land',
                             f'execute {deep} run return run tp @s ~ ~-0.18 ~ ~5 ~', 'tp @s ~ ~-0.07 ~ ~5 ~'])
    fn('p131/d/crown_land', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.apcrspot"]}', 'execute as @a[tag=bm.apcrown] run function bm:p131/d/crown_give',
                             'kill @e[type=minecraft:marker,tag=bm.apcrspot,distance=..1]',
                             'particle minecraft:totem_of_undying ~ ~0.4 ~ 0.4 0.3 0.4 0.4 60 force @a[distance=..96]',
                             'particle minecraft:end_rod ~ ~0.3 ~ 0.3 0.1 0.3 0.15 30 force @a[distance=..96]'] +
       vring('minecraft:dust{color:[0.25,1.0,0.45],scale:1.2}', 1.2, 16, 0.1) +
       [snd('block.amethyst_cluster.break', 1.5, 0.8, 48), snd('block.bell.resonate', 1, 1.2, 48), snd('entity.player.levelup', 0.8, 0.6, 48), 'kill @s'])
    fn('p131/d/crown_give', ['tag @s add bm.apcrme', 'execute at @e[type=minecraft:marker,tag=bm.apcrspot,limit=1] run function bm:p131/d/crown_drop',
                             'tag @s remove bm.apcrme', 'tag @s remove bm.apcrown',
                             title('@s', 'actionbar', [T("Apophiss's True Crown", GRN, bold=True), T(' has fallen - it is yours. Pick it up.', 'gray')])])
    fn('p131/d/crown_drop', ['loot spawn ~ ~0.25 ~ loot bm:items/apo_true_crown',
                             'execute as @e[type=minecraft:item,tag=!bm.apcrd,distance=..1.5] if items entity @s contents *[minecraft:custom_data~{bm:"apo_true_crown"}] run function bm:p131/d/crown_own'])
    fn('p131/d/crown_own', ['data modify entity @s Owner set from entity @a[tag=bm.apcrme,limit=1] UUID', 'data modify entity @s Age set value -32768s',
                            'data modify entity @s Invulnerable set value 1b', 'data modify entity @s PickupDelay set value 10s', 'data modify entity @s Glowing set value 1b',
                            'data modify entity @s Motion set value [0.0d,0.1d,0.0d]', 'tag @s add bm.apcrd'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.apend]', 'kill @e[type=minecraft:marker,tag=bm.apflr]',
                                       'kill @e[type=minecraft:item_display,tag=bm.apdseal]', 'kill @e[type=minecraft:item_display,tag=bm.apcrf]']
    fn('p131/b/fallen', [snd('entity.ender_dragon.death', 0.6, 1.4, 64),
                         'title @a[distance=..64] times 10 80 20', title('@a[distance=..64]', 'title', T('APOPHISS IS SEALED', GRN, bold=True)),
                         title('@a[distance=..64]', 'subtitle', T('the serpent king, beaten - and bound again', 'gray', italic=True)),
                         tellraw('@a[distance=..64]', [T('(From under the floor, faint:) ', 'gray', italic=True),
                                                      T('"...The old oath binds me to the victor. I am yours. Call, and I will come."', GRN_LT, italic=True)]),
                         'execute as @a[tag=bm.apwin] at @s run function bm:p131/reward',
                         tellraw('@a', PREFIX + [T('Apophiss, the Serpent King', GRN, bold=True), T(' has been beaten - and sealed away again - in the depths of the Hollow!', 'gray')])])
    fn('p131/reward', ['tag @s remove bm.apwin', 'execute if score @s bm.apk matches 1 run function bm:p131/first',
                       'execute if entity @s[tag=bm.apmace] run ' + give('apo_mace'), 'tag @s remove bm.apmace',
                       'execute if entity @s[tag=bm.apoath] run ' + give('apo_oath'), 'tag @s remove bm.apoath',
                       'loot give @s loot bm:p131/hoard', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1',
                       'advancement grant @s only bm:story/apophiss'])
    fn('p131/first', [give('apo_oath'), give('apo_mace'),
                      tellraw('@s', PREFIX + [T("The Serpent's Oath", GRN, bold=True), T(' and ', 'gray'), T("the Serpent King's Mace", GRN, bold=True),
                                              T(' are yours - and so is ', 'gray'), T("Apophiss's True Crown", GRN, bold=True),
                                              T(', falling where he fell: pick it up. Use the Oath and he\'ll serve you - grudgingly.', 'gray')])])
    wjson('bm/loot_table/p131/hoard.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('medallion', G.uni(6, 10))]},
                                                      {'rolls': 1, 'entries': [G.loot_entry('trophy', G.uni(2, 4))]},
                                                      {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(8, 14))]},
                                                      {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:enchanted_golden_apple',
                                                                                'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 2)}]}]},
                                                      {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:netherite_ingot',
                                                                                'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]}]}]})
    wjson('bm/advancement/story/apophiss.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                 'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:apo_oath'}},
                                                             'title': T('The Serpent Beneath', 'yellow'), 'description': T('Break the seal under the Hollow Throne and beat Apophiss', 'gray'),
                                                             'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== HIS RELICS: the True Crown, the Mace
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    CROWN = holds('apo_true_crown')
    # (2.77c: phase59's handler resets everyone's jump count first - so the True Crown is dispatched from inside it; before, its
    #  fangs never came)
    j = G.FUNCS['p59/crown/jump']
    j.insert(1, f'execute if items entity @s armor.head {CROWN} run return run function bm:p131/crown/jump')
    fn('p131/crown/jump', ['scoreboard players reset @s bm.crj', 'execute unless predicate bm:p20/sneaking run return 0',
                           'execute if score @s bm.crcd matches 1.. run return run ' + say("The crown's power is still gathering."),
                           'execute if entity @s[tag=bm.adv] run return 0', 'scoreboard players set @s bm.crcd 40'] +
       [f'execute at @s rotated ~{a} 0 run function bm:p59/crown/fangs' for a in (-30, -15, 0, 15, 30)] +
       ['particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.4} ~ ~1 ~ 0.8 0.4 0.8 0 16'])
    # worn, every second: no wither, no poison, no fire; water-breathing and night-sight; badly hurt - Regeneration; monsters near
    # weaken; at night Strength II and Regeneration
    G.FUNCS['loop/second'][-1:-1] = [f'execute as @a[gamemode=!spectator] if items entity @s armor.head {CROWN} at @s run function bm:p131/crown/sec',
                                     'scoreboard players remove @a[scores={bm.crw=1..}] bm.crw 1']
    fn('p131/crown/sec', ['effect clear @s minecraft:wither', 'effect clear @s minecraft:poison',
                          'effect give @s minecraft:fire_resistance 12 0 true', 'effect give @s minecraft:water_breathing 12 0 true',
                          'effect give @s minecraft:night_vision 15 0 true',
                          'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.0} ~ ~2.5 ~ 0.25 0.1 0.25 0 3',
                          'execute store result score #hp bm.rng run data get entity @s Health 2',
                          'execute store result score #mh bm.rng run attribute @s minecraft:max_health get 1',
                          'execute if score #hp bm.rng < #mh bm.rng run effect give @s minecraft:regeneration 3 0 true',
                          'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..6] run effect give @s minecraft:weakness 3 0',
                          'execute unless score #tod bm.bm matches 0..12999 run function bm:p131/crown/night',
                          # (2.80: the Serpent's Bond - your Apophiss out: Resistance II and Regeneration II, a step past the Regalia's own)
                          'function bm:p131/bond/q', 'execute if score #bond bm.rng matches 1 run effect give @s minecraft:resistance 3 1 true',
                          'execute if score #bond bm.rng matches 1 run effect give @s minecraft:regeneration 3 1 true'])
    fn('p131/crown/night', ['effect give @s minecraft:strength 2 1 true', 'effect give @s minecraft:regeneration 3 0 true'])
    # near death (at or under 30%): the Serpent King's Wrath - Resistance III, Absorption III, Regeneration II, and fangs under every
    # monster round you; then two minutes before it can come again
    fast.append(f'execute as @a[gamemode=!spectator,gamemode=!creative] unless score @s bm.crw matches 1.. if items entity @s armor.head {CROWN} run function bm:p131/crown/low')
    fn('p131/crown/low', ['execute store result score #hp bm.rng run data get entity @s Health 10',
                          'execute store result score #mh bm.rng run attribute @s minecraft:max_health get 3',
                          'execute if score #hp bm.rng <= #mh bm.rng at @s run function bm:p131/crown/wrath'])
    fn('p131/crown/wrath', ['scoreboard players set @s bm.crw 120', 'tag @s add bm.crme',
                            'effect give @s minecraft:resistance 6 2 true', 'effect give @s minecraft:absorption 30 2 true', 'effect give @s minecraft:regeneration 8 1 true',
                            'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..7] at @s run function bm:p131/crown/wrath_hit', 'tag @s remove bm.crme'] +
       [f'particle minecraft:dust{{color:[0.25,0.95,0.45],scale:1.6}} ~{3 * math.cos(2 * math.pi * k / 20):.2f} ~0.2 ~{3 * math.sin(2 * math.pi * k / 20):.2f} 0.1 0.1 0.1 0 3' for k in range(20)] +
       ['particle minecraft:squid_ink ~ ~1 ~ 0.6 0.8 0.6 0.25 60', 'particle minecraft:totem_of_undying ~ ~1.2 ~ 0.6 0.8 0.6 0.4 50',
        'particle minecraft:flash{color:[0.3,1.0,0.5,1.0]} ~ ~1.2 ~ 0 0 0 0 1',
        'playsound minecraft:entity.ender_dragon.growl player @a[distance=..32] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.evoker.cast_spell player @a[distance=..32] ~ ~ ~ 1 0.5',
        'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 0.6',
        title('@s', 'actionbar', [T("The crown wakes in anger: ", GRN, bold=True), T("the Serpent King's Wrath!", GRN_LT)])])
    fn('p131/crown/wrath_hit', ['summon minecraft:evoker_fangs ~ ~ ~ {Warmup:0,Tags:["bm.cfnew"]}',
                                'execute as @e[type=minecraft:evoker_fangs,tag=bm.cfnew,distance=..1] run data modify entity @s Owner set from entity @a[tag=bm.crme,limit=1] UUID',
                                'tag @e[type=minecraft:evoker_fangs,tag=bm.cfnew] remove bm.cfnew',
                                'effect give @s minecraft:wither 6 1', 'effect give @s minecraft:slowness 4 2'])
    # THE SERPENT KING'S WRATH (2.80: the mace's right-click) - rings of fangs round you, five lines ahead, and every monster within
    # nine blocks withered, sickened and struck (12 s; 8 s with his crown on)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.amq dummy']
    G.OBJECTIVES += ['bm.amq']
    fast.append('scoreboard players remove @a[scores={bm.amq=1..}] bm.amq 5')
    fn('p131/mace/use', ['execute if score @s bm.amq matches 1.. run return run function bm:p131/mace/wait',
                         'function bm:p2/rg/tier', 'function bm:p131/bond/q', 'scoreboard players set @s bm.amq 240', 'data modify storage bm:tmp amw.d set value 12',
                         'execute if score #rg bm.rng matches 1..2 run scoreboard players set @s bm.amq 160', 'execute if score #rg bm.rng matches 1..2 run data modify storage bm:tmp amw.d set value 15',
                         'execute if score #rg bm.rng matches 3.. run scoreboard players set @s bm.amq 100', 'execute if score #rg bm.rng matches 3.. run data modify storage bm:tmp amw.d set value 18',
                         'execute if score #bond bm.rng matches 1 run scoreboard players operation @s bm.amq /= #2 bm.rng',
                         'tag @s add bm.crme', 'tag @s add bm.amme',
                         'execute at @s align y run function bm:p131/mace/rings'] +
       [f'execute at @s rotated ~{a} 0 run function bm:p59/crown/fangs' for a in (-40, -20, 0, 20, 40)] +
       ['execute at @s as @e[type=#bm:p42_foe,distance=..9] at @s run function bm:p131/mace/wrath_hit with storage bm:tmp amw',
        'tag @s remove bm.crme', 'tag @s remove bm.amme',
        'particle minecraft:squid_ink ~ ~1 ~ 1.2 0.6 1.2 0.15 60', 'particle minecraft:dust{color:[0.25,0.95,0.45],scale:2} ~ ~0.4 ~ 3 0.2 3 0 80',
        'particle minecraft:flash{color:[0.3,1.0,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1',
        'playsound minecraft:item.mace.smash_ground_heavy player @a[distance=..32] ~ ~ ~ 1.5 0.6',
        'playsound minecraft:entity.ender_dragon.growl player @a[distance=..32] ~ ~ ~ 0.8 0.9',
        title('@s', 'actionbar', T("THE SERPENT KING'S WRATH", GRN, bold=True))])
    ring = [f'summon minecraft:evoker_fangs ~{r * math.cos(2 * math.pi * i / n):.2f} ~ ~{r * math.sin(2 * math.pi * i / n):.2f} {{Warmup:{w},Tags:["bm.amf"]}}'
            for r, n, w in ((2.5, 8, 0), (4.5, 14, 5), (6.5, 20, 10)) for i in range(n)]
    fn('p131/mace/rings', ring + ['execute as @e[type=minecraft:evoker_fangs,tag=bm.amf,distance=..9] run data modify entity @s Owner set from entity @a[tag=bm.amme,limit=1] UUID',
                                  'tag @e[type=minecraft:evoker_fangs,tag=bm.amf] remove bm.amf'])
    fn('p131/mace/wrath_hit', ['$damage @s $(d) minecraft:magic by @a[tag=bm.amme,limit=1]', 'effect give @s minecraft:wither 8 1', 'effect give @s minecraft:poison 4 1',
                         'effect give @s minecraft:slowness 4 2', 'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.4} ~ ~1 ~ 0.3 0.5 0.3 0 10'])
    fn('p131/mace/wait', ['scoreboard players operation #s bm.rng = @s bm.amq', 'scoreboard players add #s bm.rng 19', 'scoreboard players operation #s bm.rng /= #20 bm.rng',
                          title('@s', 'actionbar', [T("The Serpent King's wrath is gathering... ", 'gray'), {'score': {'name': '#s', 'objective': 'bm.rng'}, 'color': 'white'},
                                                    T(' s', 'gray')])])
    wjson('bm/advancement/p131/crown_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'head': {'predicates': {'minecraft:custom_data': '{bm:"apo_true_crown"}'}}}}}]}}},
        'rewards': {'function': 'bm:p131/crown/hit'}})
    fn('p131/crown/hit', ['advancement revoke @s only bm:p131/crown_hit',
                          'execute at @s as @e[type=#bm:hostile,tag=!bm.npc,distance=..8,nbt={HurtTime:10s}] at @s run effect give @s minecraft:wither 4 1'])
    # ---- a use: wear it (the hold item can't use the vanilla swap, so this is the swap: whatever was on your head comes to your hand)
    in_main = f'if items entity @s weapon.mainhand {CROWN}'
    in_off = f'unless items entity @s weapon.mainhand {CROWN} if items entity @s weapon.offhand {CROWN}'
    tmp = '@e[type=minecraft:item_display,tag=bm.crtmp,distance=..2,limit=1]'
    fn('p131/crown/use', ['execute if predicate bm:p20/sneaking run return run function bm:p131/crown/set',
                          'execute unless entity @s[gamemode=creative] if items entity @s armor.head *[minecraft:enchantments~[{enchantments:"minecraft:binding_curse"}]] '
                          'run return run ' + say("Whatever you're wearing won't come off."),
                          'summon minecraft:item_display ~ ~ ~ {Tags:["bm.crtmp"]}', f'item replace entity {tmp} contents from entity @s armor.head',
                          f'execute {in_main} run function bm:p131/crown/wear_main', f'execute {in_off} run function bm:p131/crown/wear_off',
                          f'kill {tmp}', 'playsound minecraft:item.armor.equip_netherite player @a[distance=..16] ~ ~ ~ 1 1',
                          'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.0} ~ ~2.2 ~ 0.3 0.15 0.3 0 10'])
    fn('p131/crown/wear_main', ['item replace entity @s armor.head from entity @s weapon.mainhand', f'item replace entity @s weapon.mainhand from entity {tmp} contents'])
    fn('p131/crown/wear_off', ['item replace entity @s armor.head from entity @s weapon.offhand', f'item replace entity @s weapon.offhand from entity {tmp} contents'])
    # ---- sneak + use on a block: set it there, on top - the very crown (its name, its everything) kept in the display; it turns
    #      slowly, gleams and smokes. Sneak + punch it to take it back (only whoever set it down).
    fn('p131/crown/set', ['execute if dimension bm:gutter run return run ' + say('Not in the vault - set it down out in the world.'),
                          'execute if dimension bm:hollow_throne run return run ' + say('Not here - set it down out in the world.'),
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                          'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                          'execute anchored eyes positioned ^ ^ ^ run function bm:p131/crown/ray', 'tag @s remove bm.placer',
                          'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks, with room above it.'),
                          f'execute unless entity @s[gamemode=creative] {in_main} run return run item replace entity @s weapon.mainhand with minecraft:air',
                          f'execute unless entity @s[gamemode=creative] {in_off} run item replace entity @s weapon.offhand with minecraft:air'])
    fn('p131/crown/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p131/crown/hit_block',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p131/crown/ray'])
    fn('p131/crown/hit_block', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                                'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.8] run return 0',
                                'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p131/crown/place', 'scoreboard players set #placed bm.rng 1'])
    cdisp = {'Tags': ['bm.crd', 'bm.crnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1)}, 'item_display': 'fixed',
             'brightness': {'sky': Int(15), 'block': Int(15)}, 'teleport_duration': Int(5), 'view_range': F(0.6),
             'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.03), F(0)], 'scale': [F(1.0)] * 3}}
    sel_new = '@e[type=minecraft:item_display,tag=bm.crnew,distance=..0.5,limit=1]'
    fn('p131/crown/place', ['summon minecraft:item_display ~ ~ ~ ' + snbt(cdisp),
                            f'execute as @a[tag=bm.placer,limit=1] {in_main} run item replace entity {sel_new} contents from entity @s weapon.mainhand',
                            f'execute as @a[tag=bm.placer,limit=1] {in_off} run item replace entity {sel_new} contents from entity @s weapon.offhand',
                            f'execute as {sel_new} at @s facing entity @a[tag=bm.placer,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                            'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.crst', 'bm.gvdeco', 'bm.crnew'], 'width': F(0.7), 'height': F(0.75), 'response': B(1)}),
                            'scoreboard players operation @e[type=minecraft:interaction,tag=bm.crnew,distance=..0.5] bm.pid = @a[tag=bm.placer,limit=1] bm.pid',
                            'tag @e[tag=bm.crnew,distance=..0.5] remove bm.crnew',
                            'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.2} ~ ~0.4 ~ 0.3 0.3 0.3 0 24', 'particle minecraft:squid_ink ~ ~0.3 ~ 0.3 0.1 0.3 0.04 12',
                            'particle minecraft:end_rod ~ ~0.6 ~ 0.2 0.2 0.2 0.05 10',
                            'playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 0.6',
                            'playsound minecraft:entity.evoker.prepare_summon block @a[distance=..16] ~ ~ ~ 0.4 1.4',
                            title('@a[tag=bm.placer]', 'actionbar', [T("Apophiss's True Crown ", GRN, bold=True), T('gleams where you set it. (Sneak + punch it to take it back.)', 'gray')])])
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.crd] at @s if entity @a[distance=..40] run function bm:p131/crown/glow')
    bob = lambda y: f'data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{translation:[0f,{y}f,0f]}}}}'
    fn('p131/crown/glow', ['scoreboard players add @s bm.apt 1', 'tp @s ~ ~ ~ ~4 ~',
                           'particle minecraft:dust{color:[0.25,1.0,0.45],scale:0.6} ~ ~0.45 ~ 0.22 0.14 0.22 0 2',
                           'particle minecraft:witch ~ ~0.55 ~ 0.2 0.12 0.2 0 1',
                           'execute store result score #r bm.rng run random value 0..5',
                           'execute if score #r bm.rng matches 0..1 run particle minecraft:end_rod ~ ~0.75 ~ 0.18 0.1 0.18 0.01 1',
                           'execute if score #r bm.rng matches 2 run particle minecraft:squid_ink ~ ~0.25 ~ 0.25 0.05 0.25 0.004 2',
                           'execute if score #r bm.rng matches 3 run particle minecraft:electric_spark ~ ~0.55 ~ 0.2 0.15 0.2 0.05 2',
                           'execute if score #r bm.rng matches 4 run particle minecraft:smoke ~ ~0.3 ~ 0.2 0.05 0.2 0.005 2',
                           'execute if score #r bm.rng matches 5 run particle minecraft:totem_of_undying ~ ~0.6 ~ 0.15 0.1 0.15 0.05 1',
                           'scoreboard players operation #f bm.rng = @s bm.apt', 'scoreboard players operation #f bm.rng %= #8 bm.rng',
                           'execute if score #f bm.rng matches 0 run ' + bob(0.14), 'execute if score #f bm.rng matches 4 run ' + bob(0.03),
                           'execute if score #f bm.rng matches 0 if score #r bm.rng matches 0..2 run playsound minecraft:block.amethyst_block.chime block @a[distance=..10] ~ ~ ~ 0.5 0.6'])
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.crst] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'run return run function bm:p131/crown/take']
    fn('p131/crown/take', ['execute if score @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] bm.pid matches 1.. unless score @s bm.pid = @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] bm.pid '
                           'run return run ' + say("It isn't yours to take."),
                           'execute at @s run summon minecraft:item ~ ~0.4 ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:0s,Tags:["bm.crgive"]}',
                           'data modify entity @e[type=minecraft:item,tag=bm.crgive,limit=1] Item set from entity @e[type=minecraft:item_display,tag=bm.crd,distance=..0.6,limit=1] item',
                           'data modify entity @e[type=minecraft:item,tag=bm.crgive,limit=1] Owner set from entity @s UUID',
                           'tag @e[type=minecraft:item,tag=bm.crgive] remove bm.crgive',
                           'kill @e[type=minecraft:item_display,tag=bm.crd,distance=..0.6]', 'kill @e[type=minecraft:interaction,tag=bm.gvdme,distance=..0.6]',
                           'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.2} ~ ~0.4 ~ 0.3 0.3 0.3 0 16', 'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6',
                           'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 0.8 0.8'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.crd]', 'kill @e[type=minecraft:interaction,tag=bm.crst]']
    second.append('execute as @e[type=minecraft:item_display,tag=bm.crd] at @s run function bm:p131/crown/check')
    fn('p131/crown/check', ['scoreboard players set #mtd bm.rng 0', 'execute if block ~ ~-0.5 ~ #minecraft:replaceable run scoreboard players set #mtd bm.rng 1',
                            'execute unless entity @e[type=minecraft:interaction,tag=bm.crst,distance=..0.3] run scoreboard players set #mtd bm.rng 1',
                            'execute if score #mtd bm.rng matches 1 run function bm:p131/crown/drop'])
    fn('p131/crown/drop', ['summon minecraft:item ~ ~0.2 ~ {Item:{id:"minecraft:stone",count:1},Tags:["bm.crgive"]}',
                           'data modify entity @e[type=minecraft:item,tag=bm.crgive,distance=..0.5,limit=1] Item set from entity @s item',
                           'tag @e[type=minecraft:item,tag=bm.crgive] remove bm.crgive', 'kill @e[type=minecraft:interaction,tag=bm.crst,distance=..0.3]',
                           'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.0} ~ ~0.3 ~ 0.2 0.2 0.2 0 10', 'kill @s'])
    # the mace: every blow withers; a smash from a fall (the mace's own) bursts fangs out round where it lands
    wjson('bm/advancement/p131/mace_hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm_apomace:1b}'}}}}}]}}},
        'rewards': {'function': 'bm:p131/mace/hit'}})
    fn('p131/mace/hit', ['advancement revoke @s only bm:p131/mace_hit', 'execute store result score #fd bm.rng run data get entity @s fall_distance 10',
                         'scoreboard players set #mf bm.rng 0'] +
       [f'execute if items entity @s weapon.mainhand {holds(mace_id(f[0]))} run scoreboard players set #mf bm.rng {i + 1}' for i, f in enumerate(MACE_FORMS)] +
       ['tag @s add bm.amme', 'execute at @s as @e[type=#bm:hostile,tag=!bm.npc,distance=..6,nbt={HurtTime:10s}] at @s run function bm:p131/mace/struck', 'tag @s remove bm.amme'])
    MF = {f[0]: i + 1 for i, f in enumerate(MACE_FORMS)}
    fn('p131/mace/struck', ['effect give @s minecraft:wither 4 1', 'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.2} ~ ~1 ~ 0.3 0.4 0.3 0 8',
                            f'execute if score #mf bm.rng matches {MF["sword"]} run effect give @s minecraft:poison 4 1',
                            f'execute if score #mf bm.rng matches {MF["axe"]} run function bm:p131/mace/cleave',
                            f'execute if score #mf bm.rng matches {MF["mace"]} if score #fd bm.rng matches 15.. run function bm:p131/mace/burst',
                            f'execute if score #mf bm.rng matches {MF["shovel"]} run effect give @s minecraft:levitation 1 3 true',
                            f'execute if score #mf bm.rng matches {MF["hoe"]} run effect give @a[tag=bm.amme,limit=1] minecraft:regeneration 2 2 true',
                            f'execute if score #mf bm.rng matches {MF["trident"]} run function bm:p131/mace/burst'])
    fn('p131/mace/cleave', ['effect give @s minecraft:weakness 4 1', 'effect give @s minecraft:slowness 3 1',
                            'execute as @e[type=#bm:p42_foe,tag=!bm.npc,distance=0.1..3] run damage @s 4 minecraft:magic by @a[tag=bm.amme,limit=1]',
                            'particle minecraft:sweep_attack ~ ~1 ~ 1 0.2 1 0 3'])
    fn('p131/mace/burst', [f'summon minecraft:evoker_fangs ~{2.4 * math.cos(2 * math.pi * i / 8):.2f} ~ ~{2.4 * math.sin(2 * math.pi * i / 8):.2f} {{Warmup:2,Tags:["bm.amf"]}}' for i in range(8)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.amf,distance=..4] run data modify entity @s Owner set from entity @a[tag=bm.amme,limit=1] UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.amf] remove bm.amf',
        'playsound minecraft:entity.evoker.cast_spell player @a[distance=..24] ~ ~ ~ 1 0.6'])
    # the forms, swapped by swap-hands (F) - put back what was in the off-hand, and hand over the next form (or, sneaking, the one before)
    tick.append('execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{bm_apomace:1b}] at @s run function bm:p131/mf/swap')
    swap = []
    for i, f in enumerate(MACE_FORMS):
        for d, nm in ((1, 'next'), (-1, 'prev')):
            to = MACE_FORMS[(i + d) % len(MACE_FORMS)]
            fn(f'p131/mf/{f[0]}_{nm}', ['item replace entity @s weapon.offhand from entity @s weapon.mainhand',
                                        f'item replace entity @s weapon.mainhand with {G.item_arg(mace_id(to[0]))}',
                                        'particle minecraft:dust{color:[0.25,0.95,0.45],scale:1.2} ~ ~1.2 ~ 0.3 0.4 0.3 0 14', 'particle minecraft:squid_ink ~ ~1.1 ~ 0.2 0.3 0.2 0.02 6',
                                        'playsound minecraft:item.armor.equip_netherite player @a[distance=..12] ~ ~ ~ 0.8 0.9',
                                        'playsound minecraft:entity.cat.hiss player @a[distance=..12] ~ ~ ~ 0.5 1.4',
                                        title('@s', 'actionbar', [T("The Serpent King's Mace: ", GRN, bold=True), T(to[1], 'white', bold=True)])])
        swap += [f'execute if items entity @s weapon.offhand {holds(mace_id(f[0]))} if predicate bm:p20/sneaking run return run function bm:p131/mf/{f[0]}_prev',
                 f'execute if items entity @s weapon.offhand {holds(mace_id(f[0]))} run return run function bm:p131/mf/{f[0]}_next']
    fn('p131/mf/swap', swap)
    # held, every second: the pickaxe and shovel lend Haste II; with your Apophiss out, Strength (the Serpent's Bond)
    G.FUNCS['loop/second'][-1:-1] = ['execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_apomace:1b}] at @s run function bm:p131/mace/held']
    fn('p131/mace/held', [f'execute if items entity @s weapon.mainhand {holds(mace_id("pickaxe"))} run effect give @s minecraft:haste 3 1 true',
                          f'execute if items entity @s weapon.mainhand {holds(mace_id("shovel"))} run effect give @s minecraft:haste 3 1 true',
                          'function bm:p131/bond/q', 'execute if score #bond bm.rng matches 1 run effect give @s minecraft:strength 3 1 true',
                          'execute if score #bond bm.rng matches 1 run particle minecraft:dust{color:[0.25,0.95,0.45],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 2'])
    # (is this player's Apophiss out?)
    fn('p131/bond/q', ['scoreboard players set #bond bm.rng 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @e[type=minecraft:wolf,tag=bm.appet] if score @s bm.pid = #me bm.pid run scoreboard players set #bond bm.rng 1'])

    # ================================================================== THE FOLLOWER
    def psel(p=None):
        return '@e[type=minecraft:item_display,tag=bm.apsel' + (f',tag=bm.app_{p}]' if p else ']')
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.appet] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd('apo', e, t)
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.app", f"bm.app_{p}", "bm.app_pet", "bm.apnew"], SP, scale0=True, extra={"shadow_radius": F(0.9 if p == "coil" else 0.0), "shadow_strength": F(0.6)})}'
           for p in A.PARTS]
    fn('p131/place', RF.place(A, UP, psel))
    for name, pz in POSES.items():
        if name in DUR_P:
            fn(f'p131/pose/{name}', RF.pose(A, pz, SP, DUR_P[name], psel))
    fn('p131/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f]}}}}'
                     for p in A.PARTS if p not in ('wingr', 'wingl')] +
       [f'execute at {psel("coil")[:-1]},limit=1] run function bm:p131/burst']
       )
    fn('p131/burst', ['particle minecraft:dust{color:[0.25,0.9,0.4],scale:2.2} ~ ~3 ~ 1.6 2.4 1.6 0 120', 'particle minecraft:witch ~ ~3 ~ 1.2 2 1.2 0.1 60',
                      'particle minecraft:squid_ink ~ ~2 ~ 1.2 1.6 1.2 0.05 40', 'particle minecraft:flash{color:[0.4,1.0,0.5,1.0]} ~ ~3 ~ 0 0 0 0 1'])
    fn('p131/saddle_look', [f'execute if score #sad bm.rng matches 1 run data modify entity {psel("body")[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_body_saddle"',
                            f'execute if score #sad bm.rng matches 1 run data modify entity {psel("chest")[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_chest_saddle"',
                            f'execute if score #sad bm.rng matches 0 run data modify entity {psel("body")[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_body"',
                            f'execute if score #sad bm.rng matches 0 run data modify entity {psel("chest")[:-1]},limit=1] item.components."minecraft:item_model" set value "bm:apo_chest"'])
    # states: 0 idle, 1 slither, 2 fast, 3 air, 4 sit, 5 ridden on the move, 11 ridden still, 6 arriving, 7 claw, 8 bite, 9 spit, 12 the wrath, 10 swim
    CYCLE = {0: (60, [(0, 'idle_a'), (30, 'idle_b')]), 1: (16, [(0, 'slither_a'), (4, 'slither_m'), (8, 'slither_b'), (12, 'slither_m')]),
             2: (12, [(0, 'slither_a'), (3, 'slither_m'), (6, 'slither_b'), (9, 'slither_m')]),
             3: (None, [(0, 'crouch')]), 4: (120, [(0, 'sit'), (60, 'sit_b')]), 5: (16, [(0, 'ride_b'), (8, 'ride_c')]), 11: (None, [(0, 'ride')]),
             6: (None, [(0, 'roar')]), 7: (None, [(0, 'claw_up'), (5, 'claw')]), 8: (None, [(0, 'battle'), (4, 'bite')]), 9: (None, [(0, 'cast'), (6, 'cast_point')]),
             12: (None, [(0, 'mace_up'), (5, 'mace_swing'), (7, 'mace_slam'), (11, 'mace_rec'), (14, 'mace_back')]),
             10: (20, [(0, 'swim_a'), (5, 'swim_m'), (10, 'swim_b'), (15, 'swim_m')])}
    RF.cycles(fn, 'p131', CYCLE, 'bm.apf', 'bm.aps', lambda p: f'p131/pose/{p}')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn('p131/state', ['execute if score @s bm.apsl matches 1.. run return run scoreboard players set #st bm.rng 6',
                      'execute if score @s bm.apx matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.apa',
                      'execute if score #rid bm.rng matches 1 if score #fw bm.rng matches 1 run return run scoreboard players set #st bm.rng 5',
                      'execute if score #rid bm.rng matches 1 run return run scoreboard players set #st bm.rng 11',
                      'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                      'execute store result score #og bm.rng run data get entity @s OnGround',
                      'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                      'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.apz 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.apz 0',
                      'execute if score @s bm.apz matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                      'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                      'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                      'scoreboard players operation #vx bm.rng += #vz bm.rng',
                      'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                      'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                      'scoreboard players set #st bm.rng 0'])
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.appet] at @s run function bm:p131/tick')
    fn('p131/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:item_display,tag=bm.app_pet,tag=!bm.apfade] if score @s bm.pid = #me bm.pid run tag @s add bm.apsel',
                     f'execute unless entity {psel("mace")} run function bm:p131/rerig',
                     'scoreboard players set #rid bm.rng 0', 'scoreboard players set #fw bm.rng 0',
                     'execute on passengers if entity @s[type=minecraft:player] run scoreboard players set #rid bm.rng 1',
                     'execute if score #rid bm.rng matches 1 run function bm:p131/ride',
                     'execute if score #rid bm.rng matches 0 if entity @s[tag=bm.aprd] run function bm:p131/unride',
                     'execute if score @s bm.apx matches 1.. run function bm:p131/act_tick',
                     'execute if score @s bm.apm matches 1.. run scoreboard players remove @s bm.apm 1',
                     'execute if score @s bm.apv matches 1.. run scoreboard players remove @s bm.apv 1',
                     'execute if score @s bm.apsl matches 1.. run scoreboard players remove @s bm.apsl 1',
                     'execute if score @s bm.apfn matches 1.. run scoreboard players remove @s bm.apfn 1',
                     # his fights (not ridden, not sitting): the claw or the bite up close, the spit further off; the eighth blow, his WRATH
                     f'execute if score #rid bm.rng matches 0 unless score @s bm.apx matches 1.. unless score @s bm.apm matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=..5.5] run function bm:p131/melee_go',
                     f'execute if score #rid bm.rng matches 0 unless score @s bm.apx matches 1.. unless score @s bm.apv matches 1.. unless data entity @s {{Sitting:1b}} '
                     f'unless entity @e[{foe},distance=..5.5] if entity @e[{foe},distance=8..18] run function bm:p131/spit_go',
                     'function bm:p131/state',
                     'execute if score #st bm.rng = @s bm.aps run scoreboard players add @s bm.apf 1',
                     'execute unless score #st bm.rng = @s bm.aps run scoreboard players set @s bm.apf 0',
                     'scoreboard players operation @s bm.aps = #st bm.rng',
                     'function bm:p131/anim',
                     'execute on owner run tag @s add bm.apown',
                     f'execute if score @s bm.aps matches 7..9 if entity @e[{foe},distance=..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p131/place',
                     f'execute if score @s bm.aps matches 12 if entity @e[{foe},distance=..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p131/place',
                     f'execute if score @s bm.aps matches 7..9 unless entity @e[{foe},distance=..16] rotated as @s rotated ~ 0 run function bm:p131/place',
                     f'execute if score @s bm.aps matches 12 unless entity @e[{foe},distance=..16] rotated as @s rotated ~ 0 run function bm:p131/place',
                     'execute if score @s bm.aps matches 0 run function bm:p131/face_you', 'execute if score @s bm.aps matches 4 run function bm:p131/face_you',
                     'execute if score @s bm.aps matches 6 run function bm:p131/face_you',
                     'execute if score @s bm.aps matches 1..3 rotated as @s rotated ~ 0 run function bm:p131/place',
                     'execute if score @s bm.aps matches 10 rotated as @s rotated ~ 0 run function bm:p131/place',
                     'execute if score @s bm.aps matches 5 rotated as @s rotated ~ 0 positioned ^ ^ ^0.8 run function bm:p131/place',
                     'execute if score @s bm.aps matches 11 rotated as @s rotated ~ 0 positioned ^ ^ ^0.8 run function bm:p131/place',
                     'tag @a[tag=bm.apown] remove bm.apown', 'tag @e[tag=bm.apsel] remove bm.apsel'])
    fn('p131/face_you', ['execute if entity @a[tag=bm.apown,distance=2.5..14] facing entity @a[tag=bm.apown,limit=1] feet rotated ~ 0 run return run function bm:p131/place',
                         'execute rotated as @s rotated ~ 0 run function bm:p131/place'])
    # ---- his blows: the claw (10, a sweep) or the bite (12, a lunge, withering); the spit at range (8 + poison); every 8th: THE WRATH
    fn('p131/melee_go', ['scoreboard players add @s bm.apch 1', 'execute if score @s bm.apch matches 8.. run return run function bm:p131/wrath_go',
                         'execute store result score #r bm.rng run random value 0..1',
                         'execute if score #r bm.rng matches 0 run scoreboard players set @s bm.apa 7', 'execute if score #r bm.rng matches 1 run scoreboard players set @s bm.apa 8',
                         'scoreboard players set @s bm.apx 10', 'scoreboard players set @s bm.apm 20'])
    fn('p131/spit_go', ['scoreboard players set @s bm.apa 9', 'scoreboard players set @s bm.apx 12', 'scoreboard players set @s bm.apv 60',
                        'playsound minecraft:entity.llama.spit neutral @a[distance=..16] ~ ~ ~ 0.8 0.7'])
    fn('p131/wrath_go', ['scoreboard players set @s bm.apch 0', 'scoreboard players set @s bm.apa 12', 'scoreboard players set @s bm.apx 16', 'scoreboard players set @s bm.apm 40',
                         'playsound minecraft:item.mace.smash_air neutral @a[distance=..20] ~ ~ ~ 1 0.6'] + face('shock', 16))
    fn('p131/act_tick', ['scoreboard players remove @s bm.apx 1',
                         'execute if score @s bm.apa matches 7 if score @s bm.apx matches 5 run function bm:p131/claw_hit',
                         'execute if score @s bm.apa matches 8 if score @s bm.apx matches 5 run function bm:p131/bite_hit',
                         'execute if score @s bm.apa matches 9 if score @s bm.apx matches 6 run function bm:p131/spit',
                         'execute if score @s bm.apa matches 12 if score @s bm.apx matches 7 run function bm:p131/wrath_hit'])
    fn('p131/claw_hit', ['tag @s add bm.apme2', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                         f'execute as @e[{foe},distance=..6,sort=nearest,limit=1] at @s run function bm:p131/clawed',
                         f'execute as @e[{foe},distance=..4.8] run damage @s 4 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.apme2,limit=1]',
                         'tag @s remove bm.apme2', 'function bm:p131/hit_count'])
    fn('p131/clawed', ['damage @s 10 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.apme2,limit=1]', 'particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 1'])
    fn('p131/bite_hit', ['tag @s add bm.apme2', 'playsound minecraft:entity.evoker_fangs.attack neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                         f'execute as @e[{foe},distance=..7,sort=nearest,limit=1] at @s run function bm:p131/bitten2',
                         'tag @s remove bm.apme2', 'function bm:p131/hit_count'])
    fn('p131/bitten2', ['damage @s 12 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.apme2,limit=1]', 'effect give @s minecraft:wither 3 0',
                        'particle minecraft:dust{color:[0.3,0.9,0.4],scale:1} ~ ~1 ~ 0.3 0.4 0.3 0 8'])
    pglob = snbt({'Tags': ['bm.apspit', 'bm.apgn'], 'item': {'id': 'minecraft:slime_ball', 'count': Int(1)}, 'item_display': 'fixed', 'teleport_duration': Int(1),
                  'brightness': {'block': Int(15), 'sky': Int(15)},
                  'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.8)] * 3}})
    fn('p131/spit', [f'execute facing entity @e[{foe},distance=..15,sort=nearest,limit=1] eyes positioned ^ ^4.6 ^2 run summon minecraft:item_display ~ ~ ~ {pglob}',
                     f'execute as @e[type=minecraft:item_display,tag=bm.apgn] at @s facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',
                     'scoreboard players operation @e[type=minecraft:item_display,tag=bm.apgn] bm.pid = #me bm.pid',
                     'scoreboard players set @e[type=minecraft:item_display,tag=bm.apgn] bm.apl 30', 'tag @e[type=minecraft:item_display,tag=bm.apgn] remove bm.apgn'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.apspit] at @s run function bm:p131/spit_fly')
    fn('p131/spit_fly', ['scoreboard players remove @s bm.apl 1', 'particle minecraft:item_slime ~ ~ ~ 0.05 0.05 0.05 0 1',
                         f'execute positioned ~ ~-0.6 ~ if entity @e[{foe},distance=..1.3] run return run function bm:p131/spit_hit',
                         'execute if score @s bm.apl matches ..0 run return run kill @s',
                         'execute positioned ^ ^ ^0.9 unless block ~ ~ ~ #bm:grap_pass run return run kill @s',
                         f'execute if entity @e[{foe},distance=..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes run tp @s ^ ^ ^0.9 ~ ~',
                         f'execute unless entity @e[{foe},distance=..16] run tp @s ^ ^ ^0.9'])
    fn('p131/spit_hit', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.apme2',
                         f'execute positioned ~ ~-0.6 ~ as @e[{foe},distance=..2.2] at @s run function bm:p131/spat',
                         'particle minecraft:item_slime ~ ~ ~ 0.5 0.5 0.5 0.1 20', 'playsound minecraft:entity.slime.squish_small neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                         'tag @e[tag=bm.apme2] remove bm.apme2', 'kill @s'])
    fn('p131/spat', ['execute if entity @e[tag=bm.apme2] run damage @s 8 minecraft:mob_projectile by @e[tag=bm.apme2,limit=1]',
                     'execute unless entity @e[tag=bm.apme2] run damage @s 8 minecraft:mob_projectile', 'effect give @s minecraft:poison 4 1'])
    fn('p131/wrath_hit', ['tag @s add bm.apme2', 'particle minecraft:explosion ~ ~0.3 ~ 2 0.1 2 0 6', 'particle minecraft:dust{color:[0.3,0.95,0.45],scale:2} ~ ~0.3 ~ 3 0.2 3 0 40',
                          'playsound minecraft:item.mace.smash_ground_heavy neutral @a[distance=..24] ~ ~ ~ 1.2 0.7',
                          f'execute as @e[{foe},distance=..6.5] run damage @s 24 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.apme2,limit=1]',
                          f'effect give @e[{foe},distance=..6.5] minecraft:wither 5 1', 'function bm:p131/pet_ring', 'tag @s remove bm.apme2',
                          'execute on owner if entity @s[distance=..24] run ' + apsay('KNEEL!')])
    fn('p131/pet_ring', [f'summon minecraft:evoker_fangs ~{4.5 * math.cos(2 * math.pi * i / 14):.2f} ~ ~{4.5 * math.sin(2 * math.pi * i / 14):.2f} {{Warmup:{2 + i % 2 * 2},Tags:["bm.apfg"]}}'
                         for i in range(14)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.apfg,distance=..8] run data modify entity @s Owner set from entity @e[type=minecraft:wolf,tag=bm.apme2,limit=1] UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.apfg] remove bm.apfg'])
    QUIPS = ['Pathetic.', 'Kneel.', 'Another one for the den.', 'Is that all? Hss.', "Don't thank me. Truly, don't.", 'I have eaten worse. Recently.', 'Hsss-hss-hss!',
             'That "king" of yours had a sliver of me. Imagine what ALL of me does.', 'I made a king out of a beggar once. Do try not to disappoint me as he did.']
    fn('p131/hit_count', ['scoreboard players add @s bm.apq 1', 'execute if score @s bm.apq matches 10.. run function bm:p131/quip'])
    fn('p131/quip', ['scoreboard players set @s bm.apq 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..20] run ' + apsay(q) for i, q in enumerate(QUIPS)] + face('smug', 30))

    # ---- the Oath: call, recall, ride (saddled), sneak for his menu
    pet = {'Tags': ['bm.appet', 'bm.apnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
           'CustomName': T('Apophiss', GRN, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': f'minecraft:{k}', 'base': D(v)} for k, v in dict(max_health=PET_HP, armor=12, armor_toughness=4, attack_damage=4, knockback_resistance=0.7,
                                                                                  movement_speed=0.34, follow_range=32, step_height=1.5, scale=SP).items()],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn('p131/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                    'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                    'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    f'{sel_pet} run tag @s add bm.apsel2',
                    # (what it does: riding him - his fangs; sneaking - his menu; beside him, saddled - climb on; out - call him over; else - call him)
                    'scoreboard players set #am bm.rng 0',
                    'execute on vehicle if entity @s[tag=bm.apsel2] run scoreboard players set #am bm.rng 1',
                    'execute if score #am bm.rng matches 0 if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                    'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag=bm.apsel2,distance=..5.5] if score @s bm.apsd matches 1 run scoreboard players set #am bm.rng 3',
                    'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag=bm.apsel2] run scoreboard players set #am bm.rng 4',
                    'execute if score #am bm.rng matches 1 run function bm:p131/rfangs', 'execute if score #am bm.rng matches 2 run function bm:p131/menu',
                    'execute if score #am bm.rng matches 3 run function bm:p131/mount', 'execute if score #am bm.rng matches 4 run function bm:p131/recall',
                    'execute if score #am bm.rng matches 0 run function bm:p131/try_summon',
                    'tag @e[tag=bm.apsel2] remove bm.apsel2'])
    fn('p131/recall', ['tp @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] Sitting set value 0b',
                       'particle minecraft:dust{color:[0.25,0.9,0.4],scale:1.4} ~ ~1 ~ 0.5 0.8 0.5 0 30', 'playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..16] ~ ~ ~ 0.6 1.2',
                       apsay('I came. Do not make a habit of whistling for me.')])
    fn('p131/try_summon', ['execute if score @s bm.apcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.apcd',
                           'execute if score @s bm.apcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.apcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                           'execute if score @s bm.apcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Apophiss is still nursing his pride: about ', 'gray'),
                                                                                                              {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                           'execute unless function bm:p131/ok run return run ' + say("Apophiss won't come here."),
                           'execute if function bm:p58/full run return 0',
                           'function bm:p131/summon'])
    fn('p131/summon', ['execute positioned ^ ^ ^2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p131/summon_here',
                       'execute positioned ^ ^1 ^2.5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p131/summon_here',
                       'function bm:p131/summon_here'])
    fn('p131/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                            'data modify entity @e[type=minecraft:wolf,tag=bm.apnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                            f'attribute @e[type=minecraft:wolf,tag=bm.apnew,limit=1,sort=nearest] minecraft:max_health base set {PET_HP}',
                            f'data modify entity @e[type=minecraft:wolf,tag=bm.apnew,limit=1,sort=nearest] Health set value {PET_HP}f',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.apnew,limit=1,sort=nearest] bm.aps -1',
                            'scoreboard players set @e[type=minecraft:wolf,tag=bm.apnew,limit=1,sort=nearest] bm.apsl 30',
                            'execute rotated ~180 0 run function bm:p131/rig_here',
                            'scoreboard players operation @e[tag=bm.apnew,distance=..4] bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:item_display,tag=bm.apnew,distance=..4] run tag @s add bm.apsel', 'function bm:p131/grow',
                            'scoreboard players operation #sad bm.rng = @s bm.apsd', 'execute unless score #sad bm.rng matches 1 run scoreboard players set #sad bm.rng 0',
                            'function bm:p131/saddle_look',
                            'tag @e[tag=bm.apsel] remove bm.apsel', 'tag @e[tag=bm.apnew,distance=..4] remove bm.apnew',
                            'playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..20] ~ ~ ~ 1 0.7',
                            'playsound minecraft:entity.ravager.roar neutral @a[distance=..20] ~ ~ ~ 0.4 1.4',
                            apsay('You called. I came. Let us not pretend either of us enjoys it.')])
    fn('p131/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.apnew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p131/rerig', ['kill @e[type=minecraft:item_display,tag=bm.apsel]', 'execute rotated as @s rotated ~ 0 run function bm:p131/rig_here',
                      'scoreboard players operation @e[type=minecraft:item_display,tag=bm.apnew,distance=..2] bm.pid = #me bm.pid',
                      'tag @e[type=minecraft:item_display,tag=bm.apnew,distance=..2] add bm.apsel', 'tag @e[type=minecraft:item_display,tag=bm.apnew,distance=..2] remove bm.apnew',
                      'function bm:p131/grow', 'scoreboard players set @s bm.aps -1',
                      'scoreboard players set #sad bm.rng 0', 'execute on owner if score @s bm.apsd matches 1 run scoreboard players set #sad bm.rng 1', 'function bm:p131/saddle_look'])
    fn('p131/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.apsel2] at @s run function bm:p131/fade',
                        'execute as @e[type=minecraft:wolf,tag=bm.apsel2] on passengers run ride @s dismount',
                        'execute as @e[type=minecraft:wolf,tag=bm.apsel2] on passengers run kill @s[type=!minecraft:player]',
                        'execute as @e[type=minecraft:wolf,tag=bm.apsel2] run data remove entity @s Owner',
                        'execute as @e[type=minecraft:wolf,tag=bm.apsel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.apsel2]',
                        apsay('Back to my den, then. Call when you need someone frightening.')])
    # ---- the menu (sneak + use the Oath): sit / follow, ride, saddle, send home / call
    dlg = lambda out: P28.multi([T("The Serpent's Oath", GRN, bold=True)],
                                [P28.body([T('Apophiss', GRN, bold=True), T(' - the serpent king, bound to you by the old oath. Smug, sharp-tongued, ', 'gray'),
                                           T('a monster in a fight.', 'white')]),
                                 P28.body([T('Claw, bite, venom; every eighth blow ', 'gray'), T("the Serpent King's Wrath", GRN, bold=True), T('. ', 'gray'),
                                           T('Saddled, he carries you: ', 'gray'), T('use the Oath beside him', 'white'), T(' to climb on; riding, the Oath casts ', 'gray'),
                                           T("Serpent's Fangs", GRN, bold=True), T('.', 'gray')], 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Ride him', GRN, bold=True), MENU + 2, width=150),
                                  P28.btn(T('Take off the saddle', 'gray'), MENU + 3, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T('Call for Apophiss', GRN, bold=True), MENU + 8, width=150)]) + [P28.btn(T('Wardrobe', GRN, bold=True), MENU + 4, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))], columns=2, exit_label='Close')
    fn('p131/menu', [f'scoreboard players set @s bm.menu {MENU}', 'scoreboard players set #out bm.rng 0',
                     'execute if entity @e[type=minecraft:wolf,tag=bm.apsel2] run scoreboard players set #out bm.rng 1',
                     f'execute if score #out bm.rng matches 1 run return run dialog show @s {snbt(dlg(True))}', f'dialog show @s {snbt(dlg(False))}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {MENU + n} run return run function bm:p131/act' for n in (1, 2, 3, 4, 8, 9)]
    fn('p131/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                    f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:p119/plain/apo',     # (2.78: his wardrobe)
                    'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.apsel2',
                    f'execute if score #act bm.pay matches {MENU + 8} unless entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/try_summon',
                    f'execute if score #act bm.pay matches {MENU + 8} if entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/recall',
                    f'execute if score #act bm.pay matches {MENU + 1} if entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/sit',
                    f'execute if score #act bm.pay matches {MENU + 2} if entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/ride_ask',
                    f'execute if score #act bm.pay matches {MENU + 3} if entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/unsaddle',
                    f'execute if score #act bm.pay matches {MENU + 9} if entity @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/dismiss',
                    'tag @e[tag=bm.apsel2] remove bm.apsel2'])
    fn('p131/sit', ['execute store success score #s0 bm.rng if data entity @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] {Sitting:1b}',
                    'execute if score #s0 bm.rng matches 1 run data modify entity @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] Sitting set value 0b',
                    'execute if score #s0 bm.rng matches 0 run data modify entity @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] Sitting set value 1b',
                    'execute if score #s0 bm.rng matches 1 run ' + apsay('Finally. Lead on - try to keep up with me.'),
                    'execute if score #s0 bm.rng matches 0 run ' + apsay('Fine. I shall coil here and judge everything that passes.'),
                    'execute if score #s0 bm.rng matches 0 as @e[type=minecraft:wolf,tag=bm.apsel2] run function bm:p131/sat'])
    fn('p131/sat', face('smug', 40))
    fn('p131/ride_ask', ['execute unless score @s bm.apsd matches 1 run return run ' + say('He needs a saddle first: right-click him holding one.', GRN_LT),
                         'tp @e[type=minecraft:wolf,tag=bm.apsel2,limit=1] @s', 'function bm:p131/mount'])
    fn('p131/unsaddle', ['execute unless score @s bm.apsd matches 1 run return run ' + say("He isn't wearing a saddle.", GRN_LT),
                         'scoreboard players set @s bm.apsd 0', 'give @s minecraft:saddle', 'scoreboard players set #sad bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.apsel2] at @s run function bm:p131/saddle_set', apsay('Ahh. Much better. It chafed, you know.')])
    fn('p131/saddle_set', ['scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:item_display,tag=bm.app_pet,distance=..8] if score @s bm.pid = #me bm.pid run tag @s add bm.apsel',
                           'function bm:p131/saddle_look', 'tag @e[tag=bm.apsel] remove bm.apsel'])
    # ---- a click box the size of him, beside him (not riding him - his back is for you): right-click to sit / stand;
    #      with a saddle in hand, he wears it
    t_ = G.FUNCS['p131/tick']
    t_.insert(len(t_) - 2, 'function bm:p131/box')
    fn('p131/box', ['execute if entity @s[tag=bm.ffpet] run return 0',
                    'execute if entity @s[tag=bm.aprd] as @e[type=minecraft:interaction,tag=bm.aphit,distance=..8] if score @s bm.pid = #me bm.pid run kill @s',
                    'execute if entity @s[tag=bm.aprd] run return 0',
                    # (2.78c: his box found wherever it is - after a long jump (a teleport to you, a flight) a box looked for only nearby
                    #  was left behind and another made; the nearest is kept, any strays go)
                    'execute as @e[type=minecraft:interaction,tag=bm.aphit] if score @s bm.pid = #me bm.pid run tag @s add bm.aphs',
                    'tag @e[type=minecraft:interaction,tag=bm.aphs,sort=nearest,limit=1] add bm.aphk', 'kill @e[type=minecraft:interaction,tag=bm.aphs,tag=!bm.aphk]',
                    'tag @e[type=minecraft:interaction,tag=bm.aphk] remove bm.aphk',
                    'execute unless entity @e[type=minecraft:interaction,tag=bm.aphs] run summon minecraft:interaction ~ ~ ~ {Tags:["bm.aphit","bm.aphs","bm.aphnew"],width:3.4f,height:6.6f,response:1b}',
                    'scoreboard players operation @e[type=minecraft:interaction,tag=bm.aphnew] bm.pid = #me bm.pid', 'tag @e[type=minecraft:interaction,tag=bm.aphnew] remove bm.aphnew',
                    'tp @e[type=minecraft:interaction,tag=bm.aphs] ~ ~ ~', 'tag @e[type=minecraft:interaction,tag=bm.aphs] remove bm.aphs'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.aphit] run function bm:p131/box_orphan')
    fn('p131/box_orphan', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #f bm.rng 0',
                           f'{sel_pet} run scoreboard players set #f bm.rng 1', 'execute if score #f bm.rng matches 0 run kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.aphit] if data entity @s interaction at @s run function bm:p131/click',
             'execute as @e[type=minecraft:interaction,tag=bm.aphit] if data entity @s attack run data remove entity @s attack']
    aw = '@e[type=minecraft:wolf,tag=bm.apclk,limit=1]'
    fn('p131/click', ['scoreboard players operation #bp bm.rng = @s bm.pid', 'execute on target at @s run function bm:p131/who', 'data remove entity @s interaction'])
    tick.append('scoreboard players remove @a[scores={bm.apcl=1..}] bm.apcl 1')
    fn('p131/who', ['execute if score @s bm.apcl matches 1.. run return 0', 'scoreboard players set @s bm.apcl 10',
                    'execute unless score @s bm.pid = #bp bm.rng run return run ' + apsay('Do I look like YOUR serpent? Move along.'),
                    'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"apo_oath"}] run return run function bm:p131/use',
                    'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.apclk',
                    'execute if items entity @s weapon.mainhand minecraft:saddle unless score @s bm.apsd matches 1 run function bm:p131/saddle_on',
                    'execute unless items entity @s weapon.mainhand minecraft:saddle run function bm:p131/sit_toggle',
                    'execute if items entity @s weapon.mainhand minecraft:saddle if score @s bm.apsd matches 1 run ' + say("He's already wearing a saddle.", GRN_LT),
                    'tag @e[tag=bm.apclk] remove bm.apclk'])
    fn('p131/sit_toggle', [f'execute store success score #s0 bm.rng if data entity {aw} {{Sitting:1b}}',
                           f'execute if score #s0 bm.rng matches 1 run data modify entity {aw} Sitting set value 0b',
                           f'execute if score #s0 bm.rng matches 0 run data modify entity {aw} Sitting set value 1b',
                           'execute if score #s0 bm.rng matches 1 run ' + apsay('Finally. Lead on - try to keep up with me.'),
                           'execute if score #s0 bm.rng matches 0 run ' + apsay('Fine. I shall coil here and judge everything that passes.'),
                           f'execute if score #s0 bm.rng matches 0 as {aw} run function bm:p131/sat'])
    fn('p131/saddle_on', ['scoreboard players set @s bm.apsd 1', 'item modify entity @s weapon.mainhand bm:p2/consume_one', 'scoreboard players set #sad bm.rng 1',
                          f'execute as {aw} at @s run function bm:p131/saddle_set', 'playsound minecraft:entity.horse.saddle neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                          apsay('A SADDLE. On ME. ...Fine. But you will NOT kick.'),
                          tellraw('@s', PREFIX + [T('Apophiss is saddled. ', GRN, bold=True), T('Use the Oath beside him to climb on (sneak to get off). He keeps the saddle until you take it off in his menu.', 'gray')])])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.aphit]')
    # ---- riding: his rider's facing is his; walk to slither (fast), jump to lunge forward; the Oath: Serpent's Fangs ahead
    fn('p131/mount', ['ride @s mount @e[type=minecraft:wolf,tag=bm.apsel2,limit=1]', 'playsound minecraft:entity.horse.saddle neutral @a[distance=..16] ~ ~ ~ 0.6 0.6',
                      title('@s', 'actionbar', [T('On his back. ', GRN, bold=True), T('Walk to slither; jump to lunge. The Oath: SERPENT\'S FANGS. ', 'gray'),
                                                T('Sneak to get off.', 'dark_gray')])])
    fn('p131/ride', ['tag @s add bm.aprd', 'data modify entity @s Sitting set value 1b',
                     'execute on passengers if predicate bm:p39/forward run scoreboard players set #fw bm.rng 1',
                     'scoreboard players set #jp bm.rng 0', 'execute on passengers if predicate bm:p26/jump_key run scoreboard players set #jp bm.rng 1',
                     'execute on passengers run function bm:p131/rider',
                     'execute on passengers store result score #yaw bm.rng run data get entity @s Rotation[0] 100',
                     'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bm.rng',
                     'execute if score #fw bm.rng matches 1 run function bm:p131/drive',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[0] set value 0.0d',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[2] set value 0.0d',
                     'execute if score #jp bm.rng matches 1 if predicate bm:p39/on_ground unless score @s bm.apfn matches 1.. run function bm:p131/lunge'])
    fn('p131/drive', ['data modify storage bm:tmp kxd.s set value 0.36d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                      'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                      'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    fn('p131/lunge', ['scoreboard players set @s bm.apfn 16', 'data modify storage bm:tmp kxd.s set value 1.1d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                      'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                      'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                      'data modify entity @s Motion[1] set value 0.42d', 'playsound minecraft:entity.ravager.step neutral @a[distance=..16] ~ ~ ~ 1 0.7'])
    fn('p131/rider', ['tag @s add bm.aprider', 'attribute @s minecraft:fall_damage_multiplier modifier add bm:ap_ride -1 add_multiplied_total'])
    fn('p131/unride', ['tag @s remove bm.aprd', 'data modify entity @s Sitting set value 0b', 'scoreboard players set @s bm.aps -1'])
    second += ['execute as @a[tag=bm.aprider] unless function bm:p131/on_him run function bm:p131/rider_off']
    fn('p131/on_him', ['execute on vehicle if entity @s[type=minecraft:wolf,tag=bm.appet] run return 1', 'return 0'])
    fn('p131/rider_off', ['tag @s remove bm.aprider', 'attribute @s minecraft:fall_damage_multiplier modifier remove bm:ap_ride'])
    fn('p131/rfangs', ['execute if score @s bm.apfn matches 1.. run return 0', 'scoreboard players set @s bm.apfn 60',
                       'execute rotated ~ 0 run function bm:p131/rfangs_at'])
    fn('p131/rfangs_at', [f'summon minecraft:evoker_fangs ^ ^ ^{3.6 + i * 1.3:.1f} {{Warmup:{i * 2},Tags:["bm.apfg"]}}' for i in range(12)] +
       [f'summon minecraft:evoker_fangs ^{s} ^ ^{4.4 + i * 1.4:.1f} {{Warmup:{3 + i * 2},Tags:["bm.apfg"]}}' for s in (-1.8, 1.8) for i in range(5)] +
       ['execute as @e[type=minecraft:evoker_fangs,tag=bm.apfg,distance=..24] run data modify entity @s Owner set from entity @p UUID',
        'tag @e[type=minecraft:evoker_fangs,tag=bm.apfg] remove bm.apfg',
        'playsound minecraft:entity.evoker.cast_spell neutral @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.ender_dragon.growl neutral @a[distance=..24] ~ ~ ~ 0.4 1.6',
        apsay('HSSSAH!')])
    tick.append('scoreboard players remove @a[scores={bm.apfn=1..}] bm.apfn 1')

    # ---- fainting: the rig without its host (4 ticks) dissolves into green; the Oath rests 5 minutes
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.app_pet,tag=bm.app_coil,tag=!bm.apfade] at @s run function bm:p131/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.apfade] bm.apl 1',
             'kill @e[type=minecraft:item_display,tag=bm.apfade,scores={bm.apl=..0}]']
    fn('p131/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet.replace("tag=bm.appet]", "tag=bm.appet,distance=..16]")} run return run scoreboard players set @s bm.apz 0',
                      'scoreboard players add @s bm.apz 1', 'execute if score @s bm.apz matches 4.. run function bm:p131/fell'])
    fn('p131/fell', ['function bm:p131/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p131/cooldown'])
    fn('p131/cooldown', [f'scoreboard players set @s bm.apcd {PET_CD}',
                         tellraw('@s', PREFIX + [T('Apophiss goes down. ', GRN, bold=True), T('"...I am RESTING. Do not look at me." ', GRN_LT),
                                                 T(f'The Oath needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn('p131/fade', ['execute as @e[type=minecraft:item_display,tag=bm.app_pet,tag=!bm.apfade] if score @s bm.pid = #me bm.pid run function bm:p131/fade1',
                     'execute as @e[type=minecraft:item_display,tag=bm.apspit] if score @s bm.pid = #me bm.pid run kill @s',
                     'particle minecraft:dust{color:[0.25,0.9,0.4],scale:2.2} ~ ~3 ~ 1.6 2.4 1.6 0 140', 'particle minecraft:witch ~ ~3 ~ 1.2 2 1.2 0.1 60',
                     'particle minecraft:flash{color:[0.4,1.0,0.5,1.0]} ~ ~3 ~ 0 0 0 0 1',
                     'playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..20] ~ ~ ~ 1 1.4', 'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 0.8 0.8'])
    fn('p131/fade1', ['tag @s add bm.apfade', 'scoreboard players set @s bm.apl 3',
                      'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:3854442}'])
    second.append('scoreboard players remove @a[scores={bm.apcd=1..}] bm.apcd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.appet] if score @s bm.pid = #me bm.pid at @s run function bm:p131/go')
    fn('p131/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p131/fade', 'execute on passengers run ride @s dismount',
                   'execute on passengers run kill @s[type=!minecraft:player]', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, ('apo', 'wolf', 'bm.appet', 'apo_oath', 'p131/go', 'Apophiss', 'bm.apfg', 'p131/summon_here'), second)
    L = G.FUNCS['p73/fol/apo']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:wolf,tag=bm.appet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', 'tag=bm.appet') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    # ---- the serpent's presence: in a fight beside you, the monsters round you weaken in his shadow
    second.append('execute as @e[type=minecraft:wolf,tag=bm.appet,tag=!bm.ffpet] at @s run function bm:p131/sec')
    fn('p131/sec', ['execute on owner if entity @s[distance=..16] run tag @s add bm.apown',
                    f'execute as @a[tag=bm.apown] at @s run effect give @e[{foe},distance=..8] minecraft:weakness 3 0',
                    f'execute as @a[tag=bm.apown] at @s if entity @e[{foe},distance=..6] run particle minecraft:dust{{color:[0.25,0.8,0.35],scale:0.9}} ~ ~0.2 ~ 2.5 0.1 2.5 0 6',
                    'tag @a[tag=bm.apown] remove bm.apown'])

    # ---- his raid contract (the Recruiter: 2 Gutter Trophies + 6 Medallions)
    def signed():
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    fn('p131/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return run ' + say('Apophiss is already under contract.', 'gray'),
        f'scoreboard players add @s bm.fcon {BIT}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_apo"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T('Apophiss', GRN, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p131/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T('Apophiss', GRN), T(' needs a ', 'gray'), T('Raid Contract', '#ffcf40'), T(' to come into the vault. The Recruiter in the den sells them.', 'gray')]), 'return 0'])
    # (the Recruiter in the den sells the contracts - 2.67d split Goldtooth's trades three ways)
    from gen_dp import offer
    L = G.FUNCS['p70/r/lobby/init']
    k = next(i for i, l in enumerate(L) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    o = offer(('gutter_trophy', 2), ('fcontract_apo', 1), ('gutter_medallion', 6))
    L[k] = L[k].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    import phase103 as P103
    P103.RECRUITER_OFFERS.append(o)

    # ================================================================== admin
    fn('admin/apophiss', [say('Apophiss comes for you: black fire, then the Serpent King.', GRN), 'execute rotated ~ 0 positioned ^ ^ ^8 run summon minecraft:husk ~ ~ ~ ' + snbt(bnbt),
                          'execute rotated ~ 0 positioned ^ ^ ^8 as @e[type=minecraft:husk,tag=bm.apnew,distance=..2,limit=1] at @s run function bm:p131/b/init'])
    fn('admin/apophiss_den', ['tag @s add bm.apin', f'execute in bm:hollow_throne run tp @s {ARRIVE[0]} {ARRIVE[1]} {ARRIVE[2]} 180 0', 'scoreboard players set #apwake bm.p2 1'])
    fn('admin/apophiss_seal', [f'execute in bm:hollow_throne run tp @s {SEAL[0] - 3} {SEAL[1]} {SEAL[2]} -90 0'])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/apophiss', 'yellow'), T('  Apophiss (boss) in front of you', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/apophiss_seal', 'yellow'), T('  to the serpent seal in the Hollow throne room', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/apophiss_den', 'yellow'), T('  into his den (he rises for a Hollow conqueror with Emma, Leo and Cecil)', 'gray')])]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.app]', 'kill @e[type=minecraft:husk,tag=bm.apboss]', 'bossbar remove bm:apob',
                                       'kill @e[type=minecraft:item_display,tag=bm.apglob]', 'kill @e[type=minecraft:item_display,tag=bm.aporb]',
                                       'kill @e[type=minecraft:item_display,tag=bm.apspit]']
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
