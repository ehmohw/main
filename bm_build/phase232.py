"""2.98: THE GUTTER GENTRY, REFORMED - Batty, Eggbert and The Count as three followers (batty_art / eggbert_art / count_art on
gentry_base: their own Gutter Gentry look, kept - and a chibi costume besides; the machinery is rigpet's).

Their story: the Gem of Creativity made them, as it made every Buddy. They didn't steal from it and they weren't born bad - they
fell in with the wrong crowd down in the Gutter, and went outlaw. Beat them, and each time you do one of them comes round to the
idea of a second chance: ONE CALLING TOKEN PER GENTRY WIN (Batty's first, then Eggbert's, then the Count's) - the token is theirs
to answer, and the first use signs them on.

BATTY (Batty's Calling Token)   BITE a foe within 2.4, every second (6). SCREECH two or more foes within 5, every 12 s: dizzy and
  slowed (3). WING GUST (charged, every minute): everything round him blown back (8). NIGHT FLIGHT out of a fight: Night Vision and
  Slow Falling for you.
EGGBERT (Eggbert's Calling Token)   CLAW (7). GOO a foe 4-14 off, every 3 s: a glob of ooze (5, slowed). OOZE SPILL (charged): the
  ground round him goes sticky - slowed hard, and 10. YOLK out of a fight: a bite to eat and Regeneration for you.
THE COUNT (The Count's Calling Token)   CANE (7). BLOBLINGS two or more foes within 8, every 10 s: his little Bloblings bounce off
  them (4 each, weakened). A GENTLEMAN'S DUEL (charged): he tips his hat - and every foe within 8 is weakened (10). NOBLESSE OBLIGE
  out of a fight: Resistance and Absorption for you.
CHIBI: each has a "Gentry / chibi" button in their menu - the chibi costume (big head, little body), swapped back any time.
THE TRIO: Batty, Eggbert and The Count together - "The Gutter Gentry, Reformed": Strength, Speed and Luck; every 20 s a Gentry
ambush on the monsters round you (6, slowed). Their pairs: Bender, Mr. Capshun, Henry and Nia (the everyone-pairs), and the Gem
(their maker, phase233)."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import batty_art as BA, eggbert_art as EA, count_art as CA
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase212 as P212

GENT = '#a8c8f0'
_CYC = lambda melee, ranged, crowd, charged, kind: {
    0: (240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_a')]),
    1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
    2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
    4: (240, [(0, 'sit_a'), (120, 'sit_b')]), 6: (None, [(0, 'happy')]),
    7: (None, [(0, melee[0]), (3, melee[1])]), 8: (None, [(0, ranged[0]), (6, ranged[1]), (12, 'idle_a')]),
    11: (None, [(0, crowd)]), 12: (None, [(0, charged[0]), (8, charged[1]), (20, 'happy')]), 14: (None, [(0, kind), (20, 'happy')]),
    10: (16, [(2 * i, f'swim_{i}') for i in range(8)])}
_DUR = {'idle_a': 20, 'idle_b': 16, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3, 'jump': 4,
        'sit_a': 20, 'sit_b': 24, 'happy': 8, 'hurt': 3, 'tired': 12}
_FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'surprised', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': 'angry'}


class Batty(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'batty', 'Batty', '#8a8ad8', '#d4d4f4', 'p232b', 'yt', 'yk'
    A = BA
    MENU, PET_HP, PET_CD, ITEM = 4450, 30, 120, 'gentry_batty'
    pron, they = 'him', 'he'
    FACE, ATTRS, SCALE, HIT = _FACE, dict(armor=2, attack_damage=5, movement_speed=0.42, follow_range=32, step_height=1.1), 0.7, (0.8, 1.0)
    CYCLE = _CYC(('bite_up', 'bite'), ('wing_flap', 'bite'), 'screech', ('wing_flap', 'screech'), 'wing_flap')
    DUR = dict(_DUR, bite_up=3, bite=2, screech=5, wing_flap=4)
    FORM = ('bm.ytform', '_c', 'Gentry / chibi', None, '"...Fine. The chibi one. Don\'t look at me."', '"Back to the real me. Much better."',
            'Switch between his Gutter Gentry look and the chibi costume.')
    QUIPS = ['"Hah! Got \'im!"', '"Still got it."', '"Upside-down is the RIGHT way up."', '"The Gentry never forgets. Mostly."', '"Screech! ...Sorry. Habit."']
    HELLO = ('"Yeah, yeah, I\'m here."', '(Batty swoops down and hangs off your arm) "Miss me?"', '"Back to the rafters. Holler if you need me."')
    SIT = ('"Up and at \'em."', '(Batty folds his wings round himself like a cloak)')
    FAINT = '"Ugh... the room\'s spinning... upside down..."'
    NOT_YOURS = '"Not your bat, pal."'
    POWERS = [('Bite', 'a foe within 2.4, every second: 6'), ('Screech', 'two or more foes within 5, every 12 s: dizzy and slowed (3)'),
              ('Wing Gust', 'charged, every minute: everything round him blown back (8)'), ('Night Flight', 'out of a fight: Night Vision and Slow Falling for you')]
    INTRO = [T('Batty', '#8a8ad8', bold=True), T(' - once of the Gutter Gentry. ', 'gray'), T('The Gem made him; the Gutter made him an outlaw. You\'re his second chance.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:large_smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.02 10']
    FADE_SOUND = 'playsound minecraft:entity.bat.takeoff neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.bat.ambient neutral @a[distance=..24] ~ ~ ~ 1 0.6']
    ENC_POSES = [(0, 'idle_a')]
    ADV = ('A Second Chance: Batty', "Answer Batty's Calling Token")
    ADMIN_HINT = 'Beat the Gutter Gentry: the first win gives Batty\'s Calling Token.'
    MEET_HINT = 'Beat the Gutter Gentry.'


class Eggbert(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'eggbert', 'Eggbert', '#d8d4c0', '#f4f2e8', 'p232e', 'eb', 'ey'
    A = EA
    MENU, PET_HP, PET_CD, ITEM = 4500, 40, 120, 'gentry_eggbert'
    pron, they = 'him', 'he'
    FACE, ATTRS, SCALE, HIT = _FACE, dict(armor=6, attack_damage=6, movement_speed=0.34, follow_range=32, step_height=1.1), 0.9, (0.8, 1.4)
    CYCLE = _CYC(('claw_up', 'claw'), ('goo_throw_up', 'goo_throw'), 'claw_up', ('goo_throw_up', 'goo_throw'), 'happy')
    DUR = dict(_DUR, claw_up=3, claw=2, goo_throw_up=5, goo_throw=3)
    FORM = ('bm.ebform', '_c', 'Gentry / chibi', None, '"Round. I am ROUND now. ...I like it."', '"Back in my good old shell."',
            'Switch between his Gutter Gentry look and the chibi costume.')
    QUIPS = ['"Cracked it."', '"Ooze you gonna call? Me."', '"Scrambled."', '"Don\'t mind the drips."', '"Sunny side up!"']
    HELLO = ('"Here, here. Coming. Mind the ooze."', '(Eggbert waddles up, dripping a little) "Reporting."', '"Off to my nest. Keep it clean out here."')
    SIT = ('"Up I get."', '(Eggbert settles down like he\'s being kept warm)')
    FAINT = '"I think... I\'m cracked..."'
    NOT_YOURS = '"I\'m spoken for, egg-sactly."'
    POWERS = [('Claw', 'a foe within 2.4, every second: 7'), ('Goo', 'a foe 4-14 off, every 3 s: a glob of ooze (5, slowed)'),
              ('Ooze Spill', 'charged, every minute: the ground round him goes sticky - slowed hard, and 10'), ('Yolk', 'out of a fight: a bite to eat and Regeneration for you')]
    INTRO = [T('Eggbert', '#d8d4c0', bold=True), T(' - once of the Gutter Gentry. ', 'gray'), T('Cracked, oozing, and trying to be good. Mostly succeeding.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:squid_ink ~ ~0.6 ~ 0.3 0.3 0.3 0.02 10']
    FADE_SOUND = 'playsound minecraft:entity.turtle.egg_crack neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.slime.squish neutral @a[distance=..24] ~ ~ ~ 1 0.6']
    ENC_POSES = [(0, 'idle_a')]
    ADV = ('A Second Chance: Eggbert', "Answer Eggbert's Calling Token")
    ADMIN_HINT = 'Beat the Gutter Gentry: the second win gives Eggbert\'s Calling Token.'
    MEET_HINT = 'Beat the Gutter Gentry, twice.'


class Count(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'count', 'The Count', '#a8c8f0', '#e0ecfa', 'p232c', 'kn', 'kz'
    A = CA
    MENU, PET_HP, PET_CD, ITEM = 4550, 36, 120, 'gentry_count'
    pron, they = 'him', 'he'
    FACE, ATTRS, SCALE, HIT = _FACE, dict(armor=4, attack_damage=6, movement_speed=0.36, follow_range=32, step_height=1.1), 0.85, (0.9, 1.3)
    CYCLE = _CYC(('cane_up', 'cane'), ('tip_hat', 'cane'), 'tip_hat', ('cane_up', 'tip_hat'), 'tip_hat')
    DUR = dict(_DUR, cane_up=3, cane=2, tip_hat=6)
    FORM = ('bm.knform', '_c', 'Gentry / chibi', None, '"How... undignified. Carry on."', '"Ah. The proper attire."',
            'Switch between his Gutter Gentry look and the chibi costume.')
    QUIPS = ['"Good day to you, sir. GOOD DAY."', '"A gentleman always settles his debts."', '"Hmph. Adequate."', '"Bloblings - attend me!"', '"Do mind the hat."']
    HELLO = ('"At your service. Reluctantly."', '(The Count tips his hat) "You summoned me?"', '"I shall retire to my parlour."')
    SIT = ('"Onwards, then."', '(The Count tips his hat down over his eyes)')
    FAINT = '"Most... undignified..."'
    NOT_YOURS = '"We have not been introduced."'
    POWERS = [('Cane', 'a foe within 2.4, every second: 7'), ('Bloblings', 'two or more foes within 8, every 10 s: his Bloblings bounce off them (4 each, weakened)'),
              ("A Gentleman's Duel", 'charged, every minute: he tips his hat - every foe within 8 weakened (10)'),
              ('Noblesse Oblige', 'out of a fight: Resistance and Absorption for you')]
    INTRO = [T('The Count', '#a8c8f0', bold=True), T(' - once the head of the Gutter Gentry. ', 'gray'), T('A gentleman gone astray, now very nearly respectable.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:item_slime ~ ~0.6 ~ 0.3 0.3 0.3 0.05 12']
    FADE_SOUND = 'playsound minecraft:entity.slime.jump neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.slime.squish neutral @a[distance=..24] ~ ~ ~ 1 0.5']
    ENC_POSES = [(0, 'idle_a')]
    ADV = ('A Second Chance: The Count', "Answer the Count's Calling Token")
    ADMIN_HINT = 'Beat the Gutter Gentry: the third win gives the Count\'s Calling Token.'
    MEET_HINT = 'Beat the Gutter Gentry, three times.'


GENTRY = (Batty, Eggbert, Count)
for _C in GENTRY:
    RP.register(_C)
for _C, _what in ((Batty, "A tarnished token with a little bat stamped on it."), (Eggbert, 'A token with a crack across it. It drips, a bit.'),
                  (Count, 'An engraved calling card, very proper, with a top hat on it.')):
    item(_C.ITEM, TOTEM, f"{_C.NAME}'s Calling Token" if _C is not Count else "The Count's Calling Token", _C.COL,
         [_what, 'Once of the Gutter Gentry. The Gem made them; the Gutter led them astray.',
          ('Use: call him (again: call him over).', 'blue'), ('Sneak + use: his menu - and his chibi costume.', 'blue'),
          ('If he faints: 2 minutes before he can return.', 'gray')],
         model=f'bm:{_C.ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
    _w = _C.W
    item(f'doll_{_w}', TOTEM, f'{_C.NAME} Doll', _C.COL, [f'A doll of {_C.NAME} - Gutter Gentry, reformed.', ('Right-click a block: set it down.', 'blue'),
                                                         ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:doll_{_w}', stack=16, cat='fun', comps=hold('none'))
    HOLD[f'doll_{_w}'] = f'bm:p141/doll_{_w}/use'
    P141.DOLLS.append((f'doll_{_w}', _C.NAME, _C.COL, f'A doll of {_C.NAME} - Gutter Gentry, reformed.', 'minecraft:crit', 'minecraft:entity.slime.jump', 'minecraft:poof'))
    P141.DOLL_FROM[f'doll_{_w}'] = (_C.ITEM, {'kh': 1.55, 'kb': 0.82, 'kl': 0.62,     # (the Count is all head - his blob grows with his face and hat, or the hat floats off)
                                              **({'groups': {'bm:gc_body': 'head'}} if _w == 'count' else {})})
    P134.FIT[_C.ITEM] = (0.0, 1.3, -0.5, 0.5, -0.5, 0.5)

# ---- the trio, and their pairs with the everyone-pairs (Bender, Mr. Capshun; Henry and Nia's come from cat_bonds)
import phase100 as P100
import phase188 as P188
P188.VNAME.update({'batty': 'Batty', 'eggbert': 'Eggbert', 'count': 'The Count'})
P100.TRIOS['gentry'] = ('The Gutter Gentry, Reformed', GENT, ('batty', 'eggbert', 'count'), 'The Gutter Gentry, Reformed', 'Walk with Batty, Eggbert and the Count at once')
P188.ICON['gentry'] = 'bm:gentry_count'
P100.BANTER['gentry'] = [('The Count', 'The Gutter Gentry rides again. For good, this time.', 'Batty', 'For GOOD good? Like, good-guy good?'),
                         ('Eggbert', 'Remember the old days? Robbing the Rat Bank?', 'The Count', 'We do NOT speak of the old days, Eggbert.'),
                         ('Batty', 'The Gem would be proud. Right? Right?', 'Eggbert', 'It made us. It\'s gotta be a LITTLE proud.')]
_O = P188.O
P188.PAIRS.update({
    'gb_bender': ('batty', 'bender', 'Fetch!', '#e0a860', 'Batty and Bender - one of them flies, the other really, really wants to catch him',
                  [f'effect give {_O} minecraft:speed 3 0 true', f'effect give {_O} minecraft:jump_boost 3 0 true'],
                  [('bender', '(spots a flying thing. His whole body vibrates.)'), ('batty', '"Don\'t. Even. Think about it."')],
                  [('bender', '(jumps for Batty, misses, jumps again)', 'batty', '"Missed me! ...Okay that one was close."')]),
    'gb_capshun': ('batty', 'capshun', 'Creature of the Night', '#f0f0f0', 'Batty and Mr. Capshun - a narrator who loves a spooky bit',
                   [f'effect give {_O} minecraft:night_vision 15 0 true', f'effect give {_O} minecraft:strength 3 0 true'],
                   [('capshun', '[Mr. Capshun narrates: "Out of the dark swooped a creature of the night!"]'), ('batty', '"Aw, thanks, pal."')],
                   [('batty', '"Narrate me cooler."', 'capshun', '[Mr. Capshun narrates: "He was, by all accounts, extremely cool."]')]),
    'eg_bender': ('eggbert', 'bender', 'Good Egg', '#e0a860', 'Eggbert and Bender - an egg and a dog who wants to know what eggs taste like',
                  [f'effect give {_O} minecraft:resistance 3 0 true', 'effect give ' + _O + ' minecraft:saturation 1 0 true'],
                  [('bender', '(sniffs Eggbert very, very carefully)'), ('eggbert', '"I am NOT breakfast."')],
                  [('bender', '(licks a drip of ooze, makes a face)', 'eggbert', '"Told you."')]),
    'eg_capshun': ('eggbert', 'capshun', 'Plot Twist', '#f0f0f0', 'Eggbert and Mr. Capshun - every story needs an egg with a dark past',
                   [f'effect give {_O} minecraft:resistance 3 0 true', f'effect give {_O} minecraft:luck 3 0 true'],
                   [('capshun', '[Mr. Capshun narrates: "The egg had a past. A cracked one."]'), ('eggbert', '"Rude. Accurate. Rude."')],
                   [('eggbert', '"Am I a good guy now, Capshun?"', 'capshun', '"[You\'re in the good guys\' chapter. That counts.]"')]),
    'ct_bender': ('count', 'bender', 'A Gentleman\'s Hound', '#e0a860', 'The Count and Bender - every gentleman needs a hound. This one is very enthusiastic',
                  [f'effect give {_O} minecraft:strength 3 0 true', f'effect give {_O} minecraft:speed 3 0 true'],
                  [('bender', '(brings the Count his own cane, very slobbery)'), ('count', '"...Good boy. I suppose."')],
                  [('count', '"Sit."', 'bender', '(sits on the Count\'s foot)')]),
    'ct_capshun': ('count', 'capshun', 'The Villain\'s Redemption', '#f0f0f0', 'The Count and Mr. Capshun - the narrator always liked a redemption arc',
                   [f'effect give {_O} minecraft:resistance 3 0 true', f'effect give {_O} minecraft:strength 3 0 true'],
                   [('capshun', '[Mr. Capshun narrates: "The villain turned, at last, to the light."]'), ('count', '"Hmph. I was never a VILLAIN. An entrepreneur."')],
                   [('count', '"Must you narrate my every step?"', 'capshun', '[Mr. Capshun narrates: "He said, stepping."]')]),
})
P188.ICON.update({'gb_bender': 'bm:gentry_batty', 'gb_capshun': 'bm:gentry_batty', 'eg_bender': 'bm:gentry_eggbert', 'eg_capshun': 'bm:gentry_eggbert',
                  'ct_bender': 'bm:gentry_count', 'ct_capshun': 'bm:gentry_count'})


def extend_offers(O, offer):
    pass


def _icon(c):
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((1, 1, 14, 14), fill=(170, 150, 90, 255), outline=(90, 70, 30, 255)); d.ellipse((3, 3, 12, 12), outline=(210, 190, 120, 255))
    col = {'batty': (60, 56, 110, 255), 'eggbert': (230, 226, 210, 255), 'count': (150, 190, 235, 255)}[c]
    if c == 'batty':
        d.polygon([(4, 7), (8, 5), (12, 7), (10, 9), (8, 8), (6, 9)], fill=col)
    elif c == 'eggbert':
        d.ellipse((5, 4, 10, 11), fill=col); d.line((5, 8, 7, 7, 8, 8, 10, 7), fill=(30, 30, 34, 255))
    else:
        d.rectangle((6, 4, 10, 8), fill=(20, 20, 24, 255)); d.rectangle((5, 8, 11, 9), fill=(20, 20, 24, 255)); d.rectangle((6, 7, 10, 7), fill=(200, 40, 40, 255))
    return im.resize((32, 32), 0)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for _C in GENTRY:
        RP.rp(_C, R, _icon(_C.W))


def textures():
    T_ = {}
    for A in (BA, EA, CA):
        T_.update(A.textures())
    return T_


def generate_early(G):
    for _C in GENTRY:
        RP.contract(_C, G)


def _abilities(who):
    def abilities(G, X):
        fn, S, go, hit, end, face, foe, pfx = G.fn, X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        rng = {'batty': (None, None), 'eggbert': (4, 14), 'count': (None, None)}[who]
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..7] run function bm:{pfx}/charge_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..{5 if who == "batty" else 8}]',
                 f'execute {idle} unless score @s {S("k2")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/crowd_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..2.4] run function bm:{pfx}/melee_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner run function bm:{pfx}/kind_go']
        if rng[0]:
            lines.append(f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..{rng[0]}] if entity @e[{foe},distance=..{rng[1]}] run function bm:{pfx}/ranged_go')
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..8] run return 1', 'return 0'])
        fn(f'{pfx}/melee_go', go(7, 6, 'mc', 20, []))
        if rng[0]: fn(f'{pfx}/ranged_go', go(8, 14, 'rc', 60, face('serious', 12)))
        fn(f'{pfx}/crowd_go', go(11, 10, 'k2', 240 if who == 'batty' else 200, face('serious', 10)))
        fn(f'{pfx}/charge_go', go(12, 24, 'gc', 1200, face('serious', 22)))
        fn(f'{pfx}/kind_go', go(14, 24, 'k', 1200, face('happy', 24)))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 3 run function bm:{pfx}/melee',
                               *([f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/ranged'] if rng[0] else []),
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 6 run function bm:{pfx}/crowd',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 15 run function bm:{pfx}/charge',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 12 run function bm:{pfx}/kind'])
        md = {'batty': 6, 'eggbert': 7, 'count': 7}[who]
        msnd = {'batty': 'minecraft:entity.bat.hurt', 'eggbert': 'minecraft:entity.slime.attack', 'count': 'minecraft:entity.player.attack.strong'}[who]
        fn(f'{pfx}/melee', hit(md) + [f'execute as @e[{foe},distance=..2.8,sort=nearest,limit=1] at @s run function bm:{pfx}/meleed'] + end)
        fn(f'{pfx}/meleed', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 8', f'playsound {msnd} neutral @a[distance=..16] ~ ~ ~ 0.8 1.2'])
        if who == 'eggbert':
            pjs = '@e[type=minecraft:wolf,tag=bm.ebpet]'
            fn(f'{pfx}/goo', P212.projectile(G, 'eb_goo', 'minecraft:slime_ball', 5, pjs, scale=0.7, fxname='syn_control',
                                             trail=['particle minecraft:squid_ink ~ ~ ~ 0.03 0.03 0.03 0 1'],
                                             on_hit=['effect give @s minecraft:slowness 3 1', 'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 0.8']))
            fn(f'{pfx}/ranged', [f'execute facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes positioned ^0.3 ^1.0 ^0.6 run function bm:{pfx}/goo',
                                 'playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
        if who == 'batty':      # SCREECH, WING GUST, NIGHT FLIGHT
            fn(f'{pfx}/crowd', hit(3) + [f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/screeched', 'playsound minecraft:entity.bat.ambient neutral @a[distance=..20] ~ ~ ~ 2 0.4',
                                         'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1'] + end)
            fn(f'{pfx}/screeched', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:nausea 5 0', 'effect give @s minecraft:slowness 4 1'])
            fn(f'{pfx}/charge', hit(8) + [f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/gusted', 'particle minecraft:gust ~ ~1 ~ 1.5 0.5 1.5 0 6',
                                          'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..20] ~ ~ ~ 1 0.8'] + end)
            fn(f'{pfx}/gusted', [f'function bm:{pfx}/hurt', f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet rotated ~ 0 positioned ^ ^0.3 ^-3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~'])
            fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p232b/kind_you'])
            fn('p232b/kind_you', ['effect give @s minecraft:night_vision 60 0 true', 'effect give @s minecraft:slow_falling 30 0 true', 'playsound minecraft:entity.bat.ambient player @s ~ ~ ~ 1 1.2'])
        elif who == 'eggbert':  # OOZE SPILL, YOLK
            fn(f'{pfx}/crowd', [f'function bm:{pfx}/melee'])
            fn(f'{pfx}/charge', hit(10) + [f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/oozed', 'particle minecraft:squid_ink ~ ~0.1 ~ 2 0.05 2 0.01 60',
                                           'playsound minecraft:block.honey_block.slide neutral @a[distance=..20] ~ ~ ~ 1 0.5'] + end)
            fn(f'{pfx}/oozed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 5 3'])
            fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p232e/kind_you'])
            fn('p232e/kind_you', ['effect give @s minecraft:saturation 1 2 true', 'effect give @s minecraft:regeneration 8 0 true', 'playsound minecraft:entity.generic.eat player @s ~ ~ ~ 1 1'])
        else:                   # BLOBLINGS, A GENTLEMAN'S DUEL, NOBLESSE OBLIGE
            fn(f'{pfx}/crowd', hit(4) + [f'execute as @e[{foe},distance=..8,sort=random,limit=3] at @s run function bm:{pfx}/blobbed',
                                         'playsound minecraft:entity.slime.jump_small neutral @a[distance=..20] ~ ~ ~ 1 1.2'] + end)
            fn(f'{pfx}/blobbed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 4 0', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0.1 12'])
            fn(f'{pfx}/charge', hit(10) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/dueled', 'playsound minecraft:block.note_block.bell neutral @a[distance=..20] ~ ~ ~ 1 0.8'] + end)
            fn(f'{pfx}/dueled', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 6 1', 'particle minecraft:enchanted_hit ~ ~1 ~ 0.3 0.4 0.3 0.2 10'])
            fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p232c/kind_you'])
            fn('p232c/kind_you', ['effect give @s minecraft:resistance 30 0 true', 'effect give @s minecraft:absorption 60 0 true', 'playsound minecraft:block.note_block.bell player @s ~ ~ ~ 1 1.2'])
        return lines
    return abilities


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    for _C in GENTRY:
        def enc(G, X, C=_C):
            fn(f'{C.pfx}/enc/talk', [X.csay('"Later, pal."')])
        RP.build(_C, G, _abilities(_C.W), enc)
        del G.FUNCS[f'{_C.pfx}/enc/joined']
        X = RP.X
        # (the first use of the token signs him on)
        U = G.FUNCS[f'{_C.pfx}/use']
        k = next(i for i, l in enumerate(U) if 'function bm:p21/pid' in l) + 1
        U.insert(k, f'execute unless entity @s[tag=bm.{_C.ab}met] run function bm:{_C.pfx}/hire')
        fn(f'{_C.pfx}/hire', [f'tag @s add bm.{_C.ab}met', f'advancement grant @s only bm:story/{_C.W}_friend',
                              tellraw('@s', [T(f'{_C.NAME} answers the token. ', _C.COL, bold=True), T('Once of the Gutter Gentry - and now, it seems, yours. A second chance.', 'gray')])])
    # ---- ONE CALLING TOKEN PER GENTRY WIN: Batty's first, then Eggbert's, then the Count's
    G.FUNCS['p88/lair/won'].append('execute as @a[tag=bm.gvp,distance=..30] at @s run function bm:p232/won')
    GW = [('batty', 'Batty'), ('eggbert', 'Eggbert'), ('count', 'The Count')]
    fn('p232/won', [f'execute unless entity @s[tag=bm.gtk{n}] run return run function bm:p232/give_{w}' for n, (w, who) in enumerate(GW, 1)])
    for n, (w, who) in enumerate(GW, 1):
        fn(f'p232/give_{w}', [f'tag @s add bm.gtk{n}', f'loot give @s loot bm:items/gentry_{w}',
                              tellraw('@s', [T(who, GENT, bold=True), T(' slips you a calling token as the dust settles. ', 'gray'),
                                             T('"Maybe... we went wrong somewhere. Call me, if you\'ll have me."', 'white', italic=True)]),
                              'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.6 1.4'])
    # ---- the trio: Strength, Speed, Luck; every 20 s, a Gentry ambush on the monsters round you
    mine = lambda k: f'@e[type=minecraft:{P100.WHO[k][0]},tag={P100.WHO[k][1]},distance=..24]'
    REGEN = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    fn('p100/gentry', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:luck 3 0 true',
                       'scoreboard players add @s bm.p188 1', 'execute if score @s bm.p188 matches 20.. run function bm:p232/ambush'] +
       [f'execute as {mine(m)} if function bm:p100/is_mine run {REGEN}' for m in ('batty', 'eggbert', 'count')] + ['function bm:p100/banter_tick'])
    fn('p232/ambush', ['scoreboard players set @s bm.p188 0', 'tag @s add bm.gtme',
                       'execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..8] at @s run function bm:p232/ambushed', 'tag @s remove bm.gtme',
                       'playsound minecraft:entity.bat.takeoff player @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn('p232/ambushed', ['damage @s 6 minecraft:mob_attack by @a[tag=bm.gtme,limit=1]', 'effect give @s minecraft:slowness 3 1', 'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.4 0.3 0.02 8'])
    wjson('bm/advancement/story/trio_gentry.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                   'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:gentry_count'}},
                                                               'title': T('The Gutter Gentry, Reformed', 'yellow'), 'description': T('Walk with Batty, Eggbert and the Count at once', 'gray'),
                                                               'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    fn('admin/gentry_tokens', [f'loot give @s loot bm:items/gentry_{w}' for w in ('batty', 'eggbert', 'count')])
