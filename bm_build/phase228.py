"""2.96: RUFUS GNAW, RAT FOR HIRE - FOR KEEPS. (rufus_art.py; the machinery is rigpet's.) The old mercenary (phase29: a single
figure on a wolf, hired by the week, gone home when his purse ran dry) is a whole follower now, and his contract never runs out.

THE MERCENARY CONTRACT (the Dark Auction, as ever): use it the first time and he signs on - for good. Use: call him (again: call
  him over); sneak + use: his menu - sit / send home, his ways, the wardrobe (his bandana), and his PAY: a week's wages into his
  purse (4 Tokens for 7 days), and his pay book.
PAYDAY  each new day he takes a day's wage from his purse. PAID TODAY: his blows hit 30% harder, he's tougher (Resistance), you
        have Luck, his scavenging comes twice as often - and his charged PAYDAY VOLLEY is his to use. UNPAID: he grumbles, but a
        contract's a contract: he stays and fights, just without the extras.
RANKS   by days paid: Recruit, VETERAN (7: more health, harder blows), CAPTAIN (28: more again).
CROSSBOW   a foe 4-16 away, every 2.5 s: aim, a bolt (6), reload.
BLADE      a foe within 2.6, every second: a slash (7).
DIRTY TRICK  three or more foes within 5, every 15 s: a smoke bomb - they're blinded, slowed and weakened (4).
PAYDAY VOLLEY  (paid today; charged, every minute; two or more foes within 14) a bolt at each of two foes, then at three more (8 each).
SCAVENGE   out of a fight beside you, every 2 minutes (1, paid): he hands you something he found - nuggets, arrows, an emerald,
           a loaf, now and then a Token.
Right-click him: sit / stand (cross-legged, or leaning back with his bandana over his eyes). A frame keeps him, a display case
shows him, Cecil sells his doll, the Tailor his bandanas and his aura (Gold Rush). His Piercing Blow (Queen Ava's honours, rank
III) is DIRTY FIGHTING: grit in its eyes, two slashes and the crossbow point-blank."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import rufus_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase212 as P212
import phase28 as P28

RU_C, RU_LINE = '#c0392b', '#f0c8c0'
W = 'rufus'
NAME = 'Rufus Gnaw'
RANKS = [(0, 'Recruit', 'gray', 30), (7, 'Veteran', 'aqua', 40), (28, 'Captain', 'gold', 50)]     # (days paid, title, colour, health)
WEEK_COST, WEEK_DAYS = 4, 7


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, NAME, RU_C, RU_LINE, 'p228', 'ru', 'rg'
    A = A
    MENU = 2590
    PET_HP, PET_CD = 30, 120
    ITEM = 'merc_contract'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': 'grin', 'surprised': 'squint', 'hurt': 'hurt', 'sleepy': 'shade', 'blink': 'blink', 'squint': 'squint', 'serious': 'angry'}
    ATTRS = dict(armor=4, attack_damage=5, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE = 0.7
    HIT = (0.6, 1.0)
    SWAP = ('tool',)
    CYCLE = {0: (240, [(0, 'idle_a'), (80, 'idle_b'), (120, 'idle_a'), (180, 'idle_c'), (210, 'idle_a')]),
             1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (240, [(0, 'sit_a'), (120, 'sit_b')]),
             6: (None, [(0, 'happy'), (12, 'salute')]),
             7: (None, [(0, 'slash_up'), (4, 'slash')]),
             8: (None, [(0, 'aim'), (8, 'shoot'), (11, 'reload')]),
             11: (None, [(0, 'slash_up'), (8, 'happy')]),
             12: (None, [(0, 'aim'), (10, 'shoot'), (13, 'aim'), (18, 'shoot'), (22, 'reload'), (30, 'happy')]),
             14: (None, [(0, 'count_coins'), (26, 'salute')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(8)])}
    DUR = {'idle_a': 20, 'idle_b': 14, 'idle_c': 16, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3,
           'jump': 4, 'sit_a': 20, 'sit_b': 30, 'slash_up': 3, 'slash': 2, 'aim': 5, 'shoot': 2, 'reload': 5, 'happy': 6, 'salute': 6,
           'count_coins': 10, 'hurt': 3, 'tired': 10}
    CYCLE[16] = (None, [(0, 'ride')])                   # (2.96c: riding Bender - phase234 seats him)
    DUR['ride'] = 6
    QUIPS = ['"Business is business."', '"That one\'s on the house."', '"Another day, another Token."', '"Duck, boss."',
             '"I charge extra for ugly ones. That one\'s extra."', '"Never miss. Well. Rarely miss."', '"You call that a monster? I\'ve seen scarier rent."',
             '"Pay a rat, get a rat. Pay ME, get the best rat."', '"Bolts aren\'t free, you know. ...They are for you, boss."',
             '"Sneak attack? I invented sneak attacks. Well. Rats did."']
    HELLO = ('"Right behind you, boss."', '(Rufus tips his bandana.) "Rufus Gnaw, reporting. Who are we hitting?"',
             '"I\'ll be at the market. Counting. You know where to find me."')
    SIT = ('"Break\'s over. Who needs stabbing?"', '(Rufus leans back and pulls his bandana down over his eyes.) "Wake me if it\'s money."')
    FAINT = 'Put it... on my tab...'
    NOT_YOURS = '"Not your rat, pal. I\'ve got a contract. And a boss."'
    POWERS = [('Payday', 'each new day he takes a day\'s wage from his purse. Paid: blows +30%, Resistance for him, Luck for you, scavenging twice as often'),
              ('Ranks', 'by days paid: Veteran (7) and Captain (28) - more health, harder blows'),
              ('Crossbow', 'a foe 4-16 away, every 2.5 s: a bolt (6)'),
              ('Blade', 'a foe within 2.6, every second: a slash (7)'),
              ('Dirty Trick', 'three or more foes within 5, every 15 s: a smoke bomb - blinded, slowed, weakened (4)'),
              ('Payday Volley', 'paid today, charged, every minute: five bolts, fanned (6 each)'),
              ('Scavenge', 'out of a fight, every 2 minutes (1 if paid): he hands you something he found')]
    INTRO = [T(NAME, RU_C, bold=True), T(' - rat for hire, and now for keeps. ', 'gray'),
             T('Crossbow at range, blade up close, and a smoke bomb for when it\'s rude. Pay him daily and he\'s worth twice the money.', 'white')]
    BUTTONS = ((6, "Pay a week's wages", f'{WEEK_COST} Tokens: {WEEK_DAYS} days into his purse', 'p228/pay'),
               (7, 'His pay book', 'his rank, days served, his purse, and whether he\'s been paid today', 'p228/book'))
    BURST = ['particle minecraft:poof ~ ~0.4 ~ 0.3 0.3 0.3 0.03 10', 'particle minecraft:crit ~ ~0.6 ~ 0.3 0.3 0.3 0.1 8']
    FADE_SOUND = 'playsound minecraft:entity.rabbit.jump neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:item.crossbow.loading_end neutral @a[distance=..24] ~ ~ ~ 0.6 1.2']
    ENC_POSES = [(0, 'idle_a'), (20, 'count_coins'), (60, 'salute')]
    ADV = ('Rat for Hire', 'Sign Rufus Gnaw\'s Mercenary Contract')
    ADMIN_HINT = 'The Mercenary Contract: the Dark Auction.'
    MEET_HINT = 'Buy his Mercenary Contract at the Dark Auction.'


RP.register(C)
item('merc_contract', TOTEM, 'Mercenary Contract', RU_C,
     ['Signed: Rufus Gnaw, Rat for Hire.', 'Terms: for keeps. Wages: one Token a day, from his purse.',
      ('Use: call Rufus (again: call him over).', 'blue'), ('Sneak + use: his menu - and his pay.', 'blue'),
      ('Crossbow at range, blade up close.', 'blue'), ('Paid today: he\'s worth twice the money.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray'), ('"Business is business."', 'dark_gray')],
     model='bm:merc_contract', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_rufus', TOTEM, 'Rufus Gnaw Doll', RU_C, ['A doll of Rufus - bandana, crossbow and all.', ('Right-click a block: set it down.', 'blue'),
                                                    ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_rufus', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_rufus'] = 'bm:p141/doll_rufus/use'
P141.DOLLS.append(('doll_rufus', NAME, RU_C, 'A doll of Rufus - bandana, crossbow and all.', 'minecraft:crit',
                   'minecraft:entity.rabbit.ambient', 'minecraft:poof'))
P141.DOLL_FROM['doll_rufus'] = ('merc_contract', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['merc_contract'] = (0.0, 0.7, -0.3, 0.3, -0.3, 0.3)
POSES = A.POSES

# ---- his bonds (phase188 runs the pairs; phase100 the trios)
import phase188 as P188
import phase100 as P100
_O, _FOE = P188.O, 'type=#bm:hostile,tag=!bm.npc'
P188.VNAME['rufus'] = 'Rufus'
P100.VOICE['Rufus'] = (RU_C, RU_LINE)
P188.PAIRS.update({
    'rf_bender': ('rufus', 'bender', 'Rat Terrier', '#e0a860', 'Rufus and Bender - one of them is very, very interested in the other',
                  [f'effect give {_O} minecraft:speed 3 0 true', f'effect give {_O} minecraft:luck 3 0 true'],
                  [('bender', '(spots Rufus. His whole body wags.)'), ('rufus', '"No. No chasing. I am a PROFESSIONAL."')],
                  [('bender', '(drops a slobbery ball at Rufus\'s feet)', 'rufus', '"...Fine. ONE throw. And this is off the clock."'),
                   ('rufus', '"Heel. HEEL. Does he know heel?"', 'bender', '(sits on Rufus)'),
                   ('rufus', '"Good dog. Don\'t tell anyone I said that."', 'bender', '(tail goes so fast it hums)')]),
    'rf_capshun': ('rufus', 'capshun', 'The Hired Pen', '#f0f0f0', 'Rufus and Mr. Capshun - every mercenary needs a legend, and every legend needs a narrator',
                   [f'effect give {_O} minecraft:strength 3 0 true', f'effect give {_O} minecraft:luck 3 0 true'],
                   [('capshun', '[Mr. Capshun narrates: "Enter the rat. Scarred, cynical - and, unbeknownst to all, a softie."]'),
                    ('rufus', '"I heard that. I\'m charging you for the \'softie\'."')],
                   [('rufus', '"Can you narrate me taller?"', 'capshun', '[Mr. Capshun narrates: "He was, in fact, exactly as tall as before."]'),
                    ('capshun', '"What\'s your motivation, Rufus? Your tragic backstory?"', 'rufus', '"Rent."'),
                    ('capshun', '[Mr. Capshun narrates: "The bolt flew true, as bolts in good stories do."]', 'rufus', '"It was a good shot. Write that down."')]),
    'rf_dennis': ('rufus', 'dennis', 'Gold Diggers', '#e0a040', 'Rufus and Dennis - one digs it up, the other prices it',
                  [f'effect give {_O} minecraft:haste 3 1 true', f'effect give {_O} minecraft:luck 3 0 true'],
                  [('dennis', '"A rat with a crossbow. You any good with a pick?"'), ('rufus', '"I\'m good with whatever pays."')],
                  [('rufus', '"That vein\'s worth forty Tokens, easy."', 'dennis', '"It\'s copper, rat."'),
                   ('dennis', '"Hold the lantern."', 'rufus', '"Lantern\'s extra."')]),
    'rf_leo': ('rufus', 'leo', 'Sword and Sellsword', '#5ab8e0', 'Rufus and Leo - a knight who fights for honour, and a rat who fights for Tokens',
               [f'effect give {_O} minecraft:strength 3 0 true', f'effect give {_O} minecraft:resistance 3 0 true'],
               [('leo', '"A sellsword. I suppose you\'ll want paying to stand beside me."'), ('rufus', '"Already paid, tin can. Same side today."')],
               [('leo', '"For honour!"', 'rufus', '"For overtime!"'),
                ('rufus', '"You ever think about going freelance, Leo? Good money."', 'leo', '"My sword is not for sale."'),
                ('leo', '"...That was a fine shot, rat."', 'rufus', '"Put it in writing. I\'ll frame it."')]),
    'rf_tul': ('rufus', 'tul', 'Privateers', '#7ad8ff', 'Rufus and Tullius - a drowned captain and a rat who\'d sail with anyone for the right price',
               [f'effect give {_O} minecraft:water_breathing 3 0 true', f'effect give {_O} minecraft:strength 3 0 true'],
               [('tul', '"Ship\'s rat. Every crew has one."'), ('rufus', '"Ship\'s MERCENARY, Captain. I bill by the knot."')],
               [('tul', '"On my ship, rats went overboard."', 'rufus', '"On mine, captains paid on time."'),
                ('rufus', '"What\'s a share of the plunder, Captain?"', 'tul', '"Whatever you can carry, ratling."')]),
    'rf_emma': ('rufus', 'emma', 'The Princess\'s Bodyguard', '#ff8ad8', 'Rufus and Emma - she decided he\'s her bodyguard. He didn\'t argue with the pay',
                [f'effect give {_O} minecraft:resistance 3 0 true', 'execute unless predicate bm:p100/regen run effect give ' + _O + ' minecraft:regeneration 5 0 true'],
                [('emma', '"A rat with a hat! Are you a knight?"'), ('rufus', '"Mercenary, Princess. It\'s like a knight, but honest about the money."')],
                [('emma', '"Rufus, will you guard me?"', 'rufus', '"I\'m already on the clock, Princess. Consider yourself guarded."'),
                 ('emma', '"Can I pet you?"', 'rufus', '"...That\'s extra. ...Fine. Once."')]),
    'rf_cecil': ('rufus', 'cecil', 'Shady Dealings', '#b48cff', 'Rufus and Cecil - two professionals who don\'t ask where the other gets his things',
                 [f'effect give {_O} minecraft:night_vision 15 0 true', f'effect give {_O} minecraft:speed 3 0 true'],
                 [('cecil', '"A rat of business. I know your kind - I shop at your market."'), ('rufus', '"Wizard. I don\'t ask, you don\'t ask."')],
                 [('rufus', '"What\'s in the bag, wizard?"', 'cecil', '"Nothing you could afford."'),
                  ('cecil', '"Does your crossbow need enchanting?"', 'rufus', '"Does your wand need a bodyguard?"')]),
})
P188.ICON.update({k: 'bm:merc_contract' for k in ('rf_bender', 'rf_capshun', 'rf_dennis', 'rf_leo', 'rf_tul', 'rf_emma', 'rf_cecil')})
TRIOS = {   # key: (name, colour, members, advancement title, description)
    'fortune': ('Soldiers of Fortune', '#c0392b', ('rufus', 'leo', 'tul'), 'Soldiers of Fortune', 'Walk with Rufus, Leo and Tullius at once'),
    'odd_jobs': ('Odd Jobs', '#e0a860', ('rufus', 'bender', 'capshun'), 'Odd Jobs', 'Walk with Rufus, Bender and Mr. Capshun at once'),
    'heist_crew': ('The Heist Crew', '#e0a040', ('rufus', 'dennis', 'pistachio'), 'The Heist Crew', 'Walk with Rufus, Dennis and Pistachio at once'),
}
P100.TRIOS.update(TRIOS)
P188.ICON.update({k: 'bm:merc_contract' for k in TRIOS})
P100.BANTER.update({
    'fortune': [('Leo', 'A knight, a captain and a sellsword. This sounds like the start of a joke.', 'Rufus', 'Punchline\'s the monsters.'),
                ('Tullius', 'We fought each other for years, boy. Now we fight beside a rat.', 'Leo', 'He shoots straighter than your crew ever did.'),
                ('Rufus', 'Split three ways, the loot. Fair\'s fair.', 'Tullius', 'Ha! A pirate\'s share, then.')],
    'odd_jobs': [('Mr. Capshun', '[Mr. Capshun narrates: "A dog, a rat and a narrator walked into a dungeon."]', 'Rufus', 'Stop narrating the jokes.'),
                 ('Bender', '(carries Rufus\'s crossbow bolts round in his mouth, one by one)', 'Rufus', 'Those are COUNTED, dog.'),
                 ('Rufus', 'What\'s the job today?', 'Mr. Capshun', '"Whatever the plot needs!"')],
    'heist_crew': [('Dennis', 'I dig in, the ghost walks through, the rat watches the door.', 'Rufus', 'And the rat gets paid first.'),
                   ('Pistachio', 'Shall I fetch the silverware, sirs? I mean - for the getaway?', 'Rufus', 'I like this butler.'),
                   ('Rufus', 'In and out. Nobody gets hurt. Except them.', 'Dennis', 'Mostly them.')]})


def extend_offers(O, offer):
    pass


def _icon():
    import sprites280d
    im = sprites280d.merc_contract()
    return im.resize((32, 32), 0) if hasattr(im, 'resize') else im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    say = lambda txt: title('@s', 'actionbar', [T('Rufus: ', RU_C, bold=True), T(txt, RU_LINE)])
    pet = 'bm.rupet'
    objs = ['bm.mpaid', 'bm.rgrk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    PREFIX = G.PREFIX

    def abilities(G, X):
        S, go, end, face, foe, pfx = X.S, X.go, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight

        def hit(d):          # (paid today: 30% harder)
            return X.hit(d) + [f'execute if entity @s[tag=bm.rupaid] run scoreboard players add #pd bm.rng {max(1, round(d * 0.3))}']
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..14]',
                 f'execute {idle} if entity @s[tag=bm.rupaid] unless score @s {S("gc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/volley_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..5]',
                 f'execute {idle} unless score @s {S("k2")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/smoke_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..2.6] run function bm:{pfx}/slash_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3.5] if entity @e[{foe},distance=..16] run function bm:{pfx}/shoot_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner run function bm:{pfx}/scav_go']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..8] run return 1', 'return 0'])
        fn(f'{pfx}/slash_go', go(7, 8, 'mc', 20, ['playsound minecraft:item.armor.equip_iron neutral @a[distance=..16] ~ ~ ~ 0.4 1.8']))
        fn(f'{pfx}/shoot_go', go(8, 16, 'rc', 50, face('serious', 14) + ['playsound minecraft:item.crossbow.loading_middle neutral @a[distance=..16] ~ ~ ~ 0.6 1.2']))
        fn(f'{pfx}/smoke_go', go(11, 20, 'k2', 300, face('squint', 20)))
        fn(f'{pfx}/volley_go', go(12, 36, 'gc', 1200, face('serious', 34) + ['execute on owner if entity @s[distance=..24] run ' + X.csay('"Payday!"'),
                                                                             'playsound minecraft:item.crossbow.quick_charge_3 neutral @a[distance=..24] ~ ~ ~ 1 1.2']))
        fn(f'{pfx}/scav_go', go(14, 40, 'k', 2400, face('happy', 40)) + ['execute if entity @s[tag=bm.rupaid] run scoreboard players set @s ' + S('k') + ' 1200'])
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/slash',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/shoot',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 12 run function bm:{pfx}/smoke',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 26 run function bm:{pfx}/volley_a',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/volley_b',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 16 run function bm:{pfx}/scavenge'])
        # BLADE
        fn(f'{pfx}/slash', hit(7) + [f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/slashed'] + end)
        fn(f'{pfx}/slashed', [f'function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~0.8 ~ 0.1 0.1 0.1 0 1',
                              'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.7 1.5'])
        # CROSSBOW: a bolt (the paid bonus rides the bolt's own damage)
        pjs = f'@e[type=minecraft:wolf,tag={pet}]'
        for key, dmg in (('ru_bolt', 6), ('ru_boltp', 8)):
            fn(f'{pfx}/{key}', P212.projectile(G, key, 'minecraft:arrow', dmg, pjs, scale=0.6, fxname='syn_offense',
                                              trail=['particle minecraft:crit ~ ~ ~ 0.02 0.02 0.02 0 1'],
                                              on_hit=['playsound minecraft:entity.arrow.hit neutral @a[distance=..16] ~ ~ ~ 0.8 1.1']))
        bolt = [f'execute if entity @s[tag=bm.rupaid] run function bm:{pfx}/ru_boltp', f'execute unless entity @s[tag=bm.rupaid] run function bm:{pfx}/ru_bolt']
        fn(f'{pfx}/bolt', bolt)
        aim = f'facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes positioned ^-0.2 ^0.55 ^0.5'
        fn(f'{pfx}/shoot', [f'execute {aim} run function bm:{pfx}/bolt', 'playsound minecraft:item.crossbow.shoot neutral @a[distance=..16] ~ ~ ~ 0.9 1.1'])
        # (one bolt at each - let go a little way down its own line, so the foe it's after is the one it homes on)
        each_foe = lambda n, srt: f'facing entity @e[{foe},distance=..16,sort={srt},limit={n}] eyes positioned ^-0.2 ^0.55 ^2.5'
        fn(f'{pfx}/volley_a', [f'execute {each_foe(2, "nearest")} run function bm:{pfx}/bolt'] +
           ['playsound minecraft:item.crossbow.shoot neutral @a[distance=..16] ~ ~ ~ 1 1.0'])
        fn(f'{pfx}/volley_b', [f'execute {each_foe(3, "random")} run function bm:{pfx}/bolt'] +
           ['playsound minecraft:item.crossbow.shoot neutral @a[distance=..16] ~ ~ ~ 1 0.9', 'particle minecraft:crit ~ ~0.6 ~ 0.3 0.2 0.3 0.2 12'])
        # DIRTY TRICK: a smoke bomb
        fn(f'{pfx}/smoke', hit(4) + [f'execute as @e[{foe},distance=..5] at @s run function bm:{pfx}/smoked',
                                     'particle minecraft:large_smoke ~ ~0.6 ~ 1.6 0.6 1.6 0.02 60', 'particle minecraft:campfire_cosy_smoke ~ ~0.4 ~ 1.2 0.2 1.2 0.01 16',
                                     'playsound minecraft:entity.generic.extinguish_fire neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                                     'playsound minecraft:entity.firework_rocket.blast neutral @a[distance=..16] ~ ~ ~ 0.5 0.6'] + end)
        fn(f'{pfx}/smoked', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:blindness 4 0', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:weakness 4 0'])
        # SCAVENGE: something he found, for you
        fn(f'{pfx}/scavenge', ['execute on owner if entity @s[distance=..12] run function bm:p228/scav_give'])
        loot = [(6, 'minecraft:gold_nugget 4', 'a handful of gold nuggets'), (11, 'minecraft:iron_nugget 6', 'some iron nuggets'),
                (15, 'minecraft:arrow 8', 'a fistful of arrows'), (18, 'minecraft:emerald 1', 'an emerald'), (19, 'minecraft:bread 3', 'three loaves')]
        lo = 1
        sv = ['execute store result score #r bm.rng run random value 1..20']
        for hi, what, txt in loot:
            sv += [f'execute if score #r bm.rng matches {lo}..{hi} run give @s {what}',
                   f'execute if score #r bm.rng matches {lo}..{hi} unless entity @s[tag=bm.hush] run ' + say(f'"Found {txt}. Yours. Don\'t ask where."')]
            lo = hi + 1
        sv += [f'execute if score #r bm.rng matches 20 run {X.give("token")}',
               'execute if score #r bm.rng matches 20 unless entity @s[tag=bm.hush] run ' + say('"A Token. Fell out of somebody\'s pocket. Somebody rude."'),
               'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 0.8']
        fn('p228/scav_give', sv)
        return lines

    def encounter(G, X):
        # (he's bought, not found: the Mercenary Contract at the Dark Auction - the first use signs him on, p228/hire)
        fn('p228/enc/talk', [X.csay('"Got a contract? The Dark Auction sells \'em. I\'ll wait."')])

    RP.build(C, G, abilities, encounter)
    X = RP.X
    del G.FUNCS['p228/enc/joined']          # (he's bought, not recruited: p228/hire signs him on - and the contract is already in hand)

    # ---- THE CONTRACT: the first use signs him on, for keeps (a week's wages in the purse to start)
    U = G.FUNCS['p228/use']
    k = next(i for i, l in enumerate(U) if 'function bm:p21/pid' in l) + 1
    U.insert(k, 'execute unless entity @s[tag=bm.rumet] run function bm:p228/hire')
    fn('p228/hire', ['tag @s add bm.rumet', 'advancement grant @s only bm:story/rufus_friend',
                     'execute unless score @s bm.mpurse matches 1.. run scoreboard players set @s bm.mpurse 7',
                     'execute unless score @s bm.mdays matches 0.. run scoreboard players set @s bm.mdays 0',
                     'scoreboard players operation @s bm.mday = #day bm.bm', 'scoreboard players operation @s bm.mpaid = #day bm.bm',
                     'title @s times 10 60 15', title('@s', 'subtitle', T('A contract for keeps. Pay him daily and he\'s worth twice the money.', 'gray', italic=True)),
                     title('@s', 'title', T(f'{NAME} signs on!', RU_C, bold=True)),
                     tellraw('@s', PREFIX + [T(f'{NAME}: ', RU_C, bold=True), T('"For keeps, boss. A week\'s wages are in the purse already - top it up from my menu."', RU_LINE)])])

    # ---- PAYDAY: each new day, a day's wage out of his purse (as each player who's hired him)
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.rumet] unless score @s bm.mday = #day bm.bm run function bm:p228/payday')
    pd = ['scoreboard players operation @s bm.mday = #day bm.bm',
          'execute unless score @s bm.mpurse matches 1.. run return run ' + tellraw('@s', PREFIX + [T(f'{NAME}: ', RU_C, bold=True),
              T('"No wages in the purse today, boss. I\'m still here - a contract\'s a contract - but the extras cost extra."', RU_LINE),
              T(' (Pay a week from his menu: sneak + use the contract.)', 'dark_gray')]),
          'scoreboard players remove @s bm.mpurse 1', 'scoreboard players add @s bm.mdays 1', 'scoreboard players operation @s bm.mpaid = #day bm.bm']
    for days, nm, col, hp in RANKS[1:]:
        pd.append(f'execute if score @s bm.mdays matches {days} run ' + tellraw('@s', PREFIX + [T(f'{NAME} is a ', 'gray'), T(nm, col, bold=True),
                                                                                                T(' now: tougher, harder-hitting.', 'gray')]))
    pd += ['execute if score @s bm.mpurse matches 1 run ' + tellraw('@s', PREFIX + [T(f'{NAME}: ', RU_C, bold=True), T('"One day left in the purse, boss. Just saying."', RU_LINE)]),
           'execute unless entity @s[tag=bm.hush] run ' + say('"Payday. Pleasure doing business."')]
    fn('p228/payday', pd)
    fn('p228/pay', P28.pay_lines('token', WEEK_COST, 'function bm:p28/back/broke {m:"A week costs 4 Tokens."}') +
       [f'scoreboard players add @s bm.mpurse {WEEK_DAYS}', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.8',
        'execute unless score @s bm.mpaid = #day bm.bm run function bm:p228/pay_today',
        tellraw('@s', PREFIX + [T(f'{WEEK_COST} Tokens: a week\'s wages into the purse. ', 'gold'), T(f'{NAME} bites one to check it.', 'gray')])])
    fn('p228/pay_today', ['scoreboard players remove @s bm.mpurse 1', 'scoreboard players add @s bm.mdays 1', 'scoreboard players operation @s bm.mpaid = #day bm.bm',
                          'scoreboard players operation @s bm.mday = #day bm.bm', say('"Paid for today too? Now THAT\'S a boss."')])
    bk = ['scoreboard players set #rk bm.rng 0'] + [f'execute if score @s bm.mdays matches {d}.. run scoreboard players set #rk bm.rng {i}' for i, (d, *_r) in enumerate(RANKS)]
    for i, (d, nm, col, hp) in enumerate(RANKS):
        bk.append(f'execute if score #rk bm.rng matches {i} run ' + tellraw('@s', [T('Rank: ', 'gray'), T(nm, col, bold=True), T('   Days served: ', 'gray'),
                                                                                   {'score': {'name': '@s', 'objective': 'bm.mdays'}, 'color': 'white'},
                                                                                   T('   In the purse: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.mpurse'}, 'color': 'gold'},
                                                                                   T(' days', 'gray')]))
    bk += ['execute if score @s bm.mpaid = #day bm.bm run ' + tellraw('@s', [T('Paid today: ', 'gray'), T('yes', 'green', bold=True), T(' - blows +30%, Resistance for him, Luck for you.', 'gray')]),
           'execute unless score @s bm.mpaid = #day bm.bm run ' + tellraw('@s', [T('Paid today: ', 'gray'), T('no', 'red', bold=True), T(' - top up the purse (4 Tokens a week).', 'gray')])]
    fn('p228/book', [tellraw('@s', PREFIX + [T(f"{NAME}'s pay book", RU_C, bold=True)])] + bk)

    # ---- each second, as Rufus: paid today? (his extras) - and his rank (health)
    G.FUNCS['loop/second'].append(f'execute as @e[type=minecraft:wolf,tag={pet}] at @s run function bm:p228/sec')
    rk = ['scoreboard players set #rk bm.rng 0']
    for i, (d, *_r) in enumerate(RANKS):
        rk.append(f'execute on owner if score @s bm.mdays matches {d}.. run scoreboard players set #rk bm.rng {i}')
    fn('p228/sec', ['scoreboard players set #pd bm.rng 0', 'execute on owner if score @s bm.mpaid = #day bm.bm run scoreboard players set #pd bm.rng 1',
                    'execute if score #pd bm.rng matches 1 run tag @s add bm.rupaid', 'execute if score #pd bm.rng matches 0 run tag @s remove bm.rupaid',
                    'execute if score #pd bm.rng matches 1 run effect give @s minecraft:resistance 2 0 true',
                    'execute if score #pd bm.rng matches 1 on owner if entity @s[distance=..24] run effect give @s minecraft:luck 3 0 true'] + rk +
       ['execute unless score @s bm.rgrk = #rk bm.rng run function bm:p228/rank'])
    fn('p228/rank', ['scoreboard players operation @s bm.rgrk = #rk bm.rng'] +
       [f'execute if score #rk bm.rng matches {i} run attribute @s minecraft:max_health base set {hp}' for i, (d, nm, col, hp) in enumerate(RANKS)] +
       [f'execute if score #rk bm.rng matches {i} run attribute @s minecraft:attack_damage base set {5 + 2 * i}' for i in range(len(RANKS))])

    # ---- THE OLD MERCENARY (before 2.96): his old figure on its wolf goes; an old contract becomes the new one; signed on already
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.mercpet] at @s run function bm:p228/old_merc_retire',
                               'execute as @a if items entity @s container.* minecraft:carrot_on_a_stick[minecraft:custom_data~{bm:"merc_contract"}] run function bm:p228/old_contract',
                               'execute as @a[tag=!bm.rumet,scores={bm.mstate=1..}] run function bm:p228/old_hire']
    fn('p228/old_merc_retire', ['execute on passengers run kill @s', 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.3 0.3 0.02 12', 'tp @s ~ ~-2000 ~', 'kill @s'])
    fn('p228/old_contract', ['clear @s minecraft:carrot_on_a_stick[minecraft:custom_data~{bm:"merc_contract"}]', X.give('merc_contract'),
                             tellraw('@s', PREFIX + [T(f'{NAME}: ', RU_C, bold=True), T('"New paperwork, boss. Same rat - for keeps now. Use it to call me."', RU_LINE)])])
    fn('p228/old_hire', ['tag @s add bm.rumet', 'advancement grant @s only bm:story/rufus_friend', 'scoreboard players set @s bm.mstate 0',
                         'execute unless score @s bm.mpurse matches 1.. run scoreboard players set @s bm.mpurse 3'])

    # ---- the trios (phase100 finds them and calls p100/<key> as the player)
    mine = lambda k: f'@e[type=minecraft:{P100.WHO[k][0]},tag={P100.WHO[k][1]},distance=..24]'
    each = lambda mem, cmd: [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    REGEN = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    fn('p100/fortune', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:resistance 3 0 true', 'effect give @s minecraft:luck 3 0 true'] +
       each(TRIOS['fortune'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    fn('p100/odd_jobs', ['effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:luck 3 0 true', 'effect give @s minecraft:jump_boost 3 0 true'] +
       each(TRIOS['odd_jobs'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p100/heist_crew', ['effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:haste 3 1 true', 'effect give @s minecraft:night_vision 15 0 true',
                           'effect give @s minecraft:luck 3 1 true'] + each(TRIOS['heist_crew'][2], REGEN) + ['function bm:p100/banter_tick'])
    for k, (nm, col, mem, at, desc) in TRIOS.items():
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:merc_contract'}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal', 'show_toast': True,
                                                                 'announce_to_chat': True, 'hidden': True}})
