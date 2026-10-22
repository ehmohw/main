"""2.88: BONES - EMMA'S SHARK. (bones_art.py, after the owner's drawings; the machinery is rigpet's, his riding the Lantern's.)
Emma's loyal pet shark, a guardian of the Underwater Kingdom: grey, a scar and stitches over one eye, a skull and crossbones on
his flank, and the biggest grin in the sea. On land he swims along in a magically suspended ball of water.

FINDING HIM (rare): out on the ocean - swimming or in a boat - now and then a fin cuts the water beside you. Right-click him
  holding a raw fish and he's yours (with Emma beside you, he knows you're family). He gives you his whistle.
BONES'S WHISTLE  use: call him (again: call him over); sneak + use: his menu - sit / send home, his ways, the wardrobe, and Ride.
RIDE           (his menu) on his back: in water he goes where you look - up, down, fast - and you breathe and swim like a dolphin;
               on land he floats along in his bubble. The whistle from his back is CHOMP: he lunges and bites what's ahead.
               Sneak to get off.
BITE           a bite every 0.8 s at a foe within 3 - 8 (11 in water).
THRASH         every 5 s: he grabs the nearest foe and shakes it - three tears, 4 each, and it's slowed.
TORPEDO        every 8 s, a foe within 5-14: he rams through it and everything in his way (10, flung back).
FEEDING FRENZY (charged, every minute) five seconds of teeth: a bite every 0.4 s on foe after foe within 10, 8 each - and every
               bite heals him and you.
GUARDIAN OF THE KINGDOM  near him you have Dolphin's Grace in water (and Water Breathing while you ride). Emma beside him: he
               hits 2 harder.
Right-click him: sit / stand. A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the Ember Rat a
golden one, the Tailor his skins (and his aura, Abyssal Tide), the Recruiter his Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import bones_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134

BJ_C, BJ_LINE = '#8ab0c8', '#e0f0ff'
W = 'bones'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Bones', BJ_C, BJ_LINE, 'p196', 'bj', 'bz'
    A = A
    MENU = 2820
    PET_HP, PET_CD = 70, 120
    ITEM = 'bn_whistle'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': 'happy', 'surprised': 'angry', 'hurt': 'angry', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'angry', 'serious': None}
    ATTRS = dict(armor=10, attack_damage=8, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE = 1.1
    HIT = (1.4, 1.6)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'happy')]), 7: (None, [(0, 'bite_open'), (3, 'bite')]),
             8: (None, [(0, 'bite_open'), (3, 'thrash_a'), (6, 'thrash_b'), (9, 'thrash_a'), (12, 'thrash_b')]),
             9: (None, [(0, 'charge'), (8, 'bite')]),
             11: (None, [(0, 'bite_open'), (3, 'bite')]),
             12: (None, [(0, 'bite_open')] + [(4 + 8 * i + k, p) for i in range(12) for k, p in ((0, 'bite_open'), (3, 'bite'), (5, ('thrash_a', 'thrash_b')[i % 2]))]),
             14: (None, [(0, 'happy')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3, 'jump': 4,
           'sit_a': 20, 'sit_b': 20, 'bite_open': 3, 'bite': 2, 'thrash_a': 3, 'thrash_b': 3, 'charge': 5, 'happy': 8}
    QUIPS = ['(he grins. He is always grinning. It is a LOT of teeth.)', '(chomp chomp chomp - at nothing in particular)', '(he rolls over in his bubble, belly up)',
             '(the skull on his flank seems to wink)', '(he bumps your hand with his snout, hard)', '(a happy blub)',
             '(he circles you, twice, protectively)', '(he snaps at a passing fly and misses, and pretends he didn\'t)']
    HELLO = ('(a fin cuts the air - then a whole grinning shark in a ball of water)', '(his bubble wobbles in from nowhere, him inside it, grinning)', '(he flips his tail and swims off home)')
    SIT = ('(he perks up, all teeth)', '(he settles to the bottom of his bubble, one eye open)')
    FAINT = '(a sad, small blub)'
    NOT_YOURS = '(he shows you every single one of his teeth)'
    POWERS = [('Ride', 'from his menu: in water he goes where you look - up, down, fast; on land he floats along in his bubble. The whistle from his back: CHOMP. Sneak to get off'),
              ('Bite', 'a bite every 0.8 s (8; 11 in water)'),
              ('Thrash', 'every 5 s: he grabs the nearest foe and shakes it - three tears, 4 each, and it\'s slowed'),
              ('Torpedo', 'every 8 s, a foe within 5-14: he rams through it and everything in his way (10, flung back)'),
              ('Feeding Frenzy', 'charged, every minute: a bite every 0.4 s on foe after foe within 10, 8 each - every bite heals him and you'),
              ('Guardian of the Kingdom', 'near him you have Dolphin\'s Grace in water (and Water Breathing as you ride); Emma beside him - he hits 2 harder')]
    INTRO = [T('Bones', BJ_C, bold=True), T(' - Emma\'s shark, a guardian of the Underwater Kingdom. ', 'gray'), T('All grin. All teeth. All yours.', 'white')]
    BUTTONS = ((6, 'Ride', 'Climb on his back (sneak to get off). In water he goes where you look.', 'p196/ride_ask'),)
    BURST = ['particle minecraft:bubble_pop ~ ~1 ~ 0.6 0.6 0.6 0.05 30', 'particle minecraft:splash ~ ~1 ~ 0.6 0.4 0.6 0.1 30',
             'particle minecraft:dust{color:[0.55,0.7,0.8],scale:1.4} ~ ~1 ~ 0.5 0.5 0.5 0 16']
    FADE_SOUND = 'playsound minecraft:entity.player.splash neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'
    SUMMON_EXTRA = ['playsound minecraft:entity.dolphin.splash neutral @a[distance=..24] ~ ~ ~ 1 0.7']
    ENC_POSES = [(0, 'swim_0'), (20, 'swim_2'), (40, 'swim_4'), (60, 'swim_6')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:bubble ~ ~0.5 ~ 0.6 0.2 0.6 0.02 4'
    ADV = ('A Bigger Boat', 'Meet Bones out on the open ocean - and win over Emma\'s shark with a fish')
    ADMIN_HINT = 'He turns up rarely out on the ocean, beside a player swimming or in a boat.'
    MEET_HINT = 'Right-click him holding a raw fish.'


RP.register(C)
item('bn_whistle', TOTEM, "Bones's Whistle", BJ_C,
     ['A whistle carved from a shark\'s tooth, on a cord of kelp.', 'Emma has one just like it.', ('Use: call Bones (again: call him over).', 'blue'),
      ('Sneak + use: his menu - Ride.', 'blue'), ('Riding him: CHOMP!', 'blue'), ('Near him: Dolphin\'s Grace in water.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray'), ('"Who\'s my big scary boy?" - Emma', 'dark_gray')],
     model='bm:bn_whistle', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_bones', TOTEM, 'Bones Doll', BJ_C, ['A doll of Bones - a soft shark with felt teeth.', ('Right-click a block: set it down.', 'blue'),
                                              ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_bones', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_bones'] = 'bm:p141/doll_bones/use'
P141.DOLLS.append(('doll_bones', 'Bones', BJ_C, 'A doll of Bones - a soft shark with felt teeth.', 'minecraft:bubble_pop',
                   'minecraft:entity.dolphin.ambient', 'minecraft:splash'))
P141.DOLL_FROM['doll_bones'] = ('bn_whistle', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['bn_whistle'] = (0.0, 1.9, -0.9, 0.9, -1.6, 1.6)
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((2, 2, 5, 6, 4, 9), fill=hexc('#3a7a5a'))                                              # the kelp cord
    d.polygon([(5, 8), (12, 6), (14, 9), (8, 14)], fill=hexc('#f0ece0'), outline=hexc('#8a8478'))   # the tooth whistle
    d.line((7, 10, 12, 8), fill=hexc('#c8c0b0')); d.point((11, 9), fill=hexc('#2a2a2a')); d.point((9, 11), fill=hexc('#2a2a2a'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col=BJ_LINE: title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    pet = 'bm.bjpet'

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        host = f'@e[type=minecraft:wolf,tag={X.me},limit=1]'
        lines = ['scoreboard players set #rid bm.rng 0', 'execute if function bm:p196/has_rider run scoreboard players set #rid bm.rng 1',
                 'execute if score #rid bm.rng matches 1 run function bm:p196/ride',
                 'execute if score #rid bm.rng matches 0 if entity @s[tag=bm.bjrd] run function bm:p196/unride',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..10] run function bm:{pfx}/frenzy_go',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. unless entity @e[{foe},distance=..4] if entity @e[{foe},distance=..14] run function bm:{pfx}/torpedo_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/thrash_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/bite_go',
                 # (he hunts: anything hostile within 14, and he closes in - fast in water)
                 f'execute unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}} if predicate bm:swim if entity @e[{foe},distance=2.5..14] facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes run function bm:{pfx}/chase']
        fn(f'{pfx}/chase', ['execute if block ^ ^ ^0.6 #bm:swim_pass if block ^ ^1 ^0.6 #bm:swim_pass run tp @s ^ ^ ^0.3 ~ ~'])
        fn(f'{pfx}/bite_go', go(7, 5, 'mc', 16, ['playsound minecraft:entity.dolphin.attack neutral @a[distance=..16] ~ ~ ~ 0.8 0.6']))
        fn(f'{pfx}/thrash_go', go(8, 14, 'rc', 100, face('surprised', 14) + ['playsound minecraft:entity.guardian.attack neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/torpedo_go', go(9, 12, 'bc', 160, face('surprised', 12) + ['playsound minecraft:entity.dolphin.jump neutral @a[distance=..16] ~ ~ ~ 1 0.6']))
        fn(f'{pfx}/frenzy_go', go(12, 100, 'gc', 1200, face('surprised', 100) + ['playsound minecraft:entity.elder_guardian.curse neutral @a[distance=..24] ~ ~ ~ 0.4 1.6',
                                                                                 'playsound minecraft:entity.dolphin.attack neutral @a[distance=..24] ~ ~ ~ 1 0.5']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 2 run function bm:{pfx}/bite',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 10 run function bm:{pfx}/thrash',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/thrash',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 2 run function bm:{pfx}/thrash',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 6 run function bm:{pfx}/torpedo',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 2..96 run function bm:{pfx}/frenzy_tick'])
        # his teeth: base + water + Emma
        def dmg(base):
            return hit(base) + ['execute if predicate bm:swim run scoreboard players add #pd bm.rng 3',
                                'execute if block ~ ~ ~ minecraft:water run scoreboard players add #pd bm.rng 3',
                                f'execute if function bm:{pfx}/emma_near run scoreboard players add #pd bm.rng 2']
        fn(f'{pfx}/emma_near', ['scoreboard players operation #me2 bm.pid = @s bm.pid',
                                'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..16] if score @s bm.pid = #me2 bm.pid run return 1', 'return 0'])
        fn(f'{pfx}/bite', dmg(8) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/bitten'] + end)
        fn(f'{pfx}/bitten', [f'function bm:{pfx}/hurt', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 4', 'particle minecraft:bubble_pop ~ ~1 ~ 0.3 0.3 0.3 0.05 8',
                             'playsound minecraft:entity.player.attack.crit neutral @a[distance=..16] ~ ~ ~ 0.6 0.6'])
        fn(f'{pfx}/thrash', hit(4) + [f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] at @s run function bm:{pfx}/shaken'] + end)
        fn(f'{pfx}/shaken', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 2', 'particle minecraft:splash ~ ~1 ~ 0.4 0.4 0.4 0.1 16',
                             'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.5 0.6'])
        # TORPEDO: a dash along his facing - through his foe and anything else in the way
        fn(f'{pfx}/torpedo', hit(10) + [f'tag @s add {X.me}',
                                        f'execute facing entity @e[{foe},distance=..14,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/dash'] + end)
        fn(f'{pfx}/dash', [f'execute positioned ^ ^ ^{d} if block ~ ~0.5 ~ #bm:swim_pass run function bm:{pfx}/wake' for d in range(1, 13)] +
           [f'execute positioned ^ ^ ^{d} if block ~ ~0.5 ~ #bm:swim_pass if block ~ ~1 ~ #bm:swim_pass run tp {host} ~ ~ ~ ~ ~' for d in (4, 8, 12)] +
           ['playsound minecraft:entity.dolphin.swim neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
        fn(f'{pfx}/wake', ['particle minecraft:bubble ~ ~0.6 ~ 0.3 0.3 0.3 0.02 4', 'particle minecraft:cloud ~ ~0.4 ~ 0.2 0.1 0.2 0.01 1',
                           f'execute as @e[{foe},distance=..1.8,tag=!bm.bjtp] at @s run function bm:{pfx}/rammed'])
        fn(f'{pfx}/rammed', ['tag @s add bm.bjtp', f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.5d',
                             'particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.player.attack.knockback neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                             'schedule function bm:p196/untag 10t replace'])
        fn('p196/untag', ['tag @e[tag=bm.bjtp] remove bm.bjtp'])
        # FEEDING FRENZY: every 8 ticks, beside a random foe within 10 - a bite that heals him and his person
        fn(f'{pfx}/frenzy_tick', [f'scoreboard players operation #h bm.rng = @s {S("x")}', 'scoreboard players operation #h bm.rng %= #8 bm.rng',
                                  f'execute if score #h bm.rng matches 0 if entity @e[{foe},distance=..10] run function bm:{pfx}/frenzy_hit'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #8 bm.rng 8']
        # (foe after foe: each bite goes to one he hasn't bitten yet this frenzy - round again once they all have)
        fn(f'{pfx}/frenzy_hit', [f'execute unless entity @e[{foe},distance=..10,tag=!bm.bjfz] run tag @e[tag=bm.bjfz] remove bm.bjfz',
                                 f'tag @e[{foe},distance=..10,tag=!bm.bjfz,sort=random,limit=1] add bm.bjfzn'] + dmg(8) +
                                [f'execute as @e[tag=bm.bjfzn,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.4 if block ~ ~ ~ #bm:swim_pass run tp {host} ~ ~ ~ facing entity @s feet',
                                 f'execute as @e[tag=bm.bjfzn,limit=1] unless entity @s[distance=..3] at @s run tp {host} ~ ~ ~ facing entity @s feet',
                                 'tag @e[tag=bm.bjfzn] add bm.bjfz', 'tag @e[tag=bm.bjfzn] remove bm.bjfzn',
                                          f'execute at @s as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/bitten',
                                          'effect give @s minecraft:instant_health 1 0 true',
                                          'execute on owner if entity @s[distance=..24] run effect give @s minecraft:regeneration 2 1 true'] + end)
        # -- every second: the Guardian of the Kingdom (Dolphin's Grace in water near him), he breathes anywhere
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        fn(f'{pfx}/sec', ['effect give @s minecraft:water_breathing 3 0 true',
                          'execute on owner if entity @s[distance=..24] if predicate bm:swim run effect give @s minecraft:dolphins_grace 3 0 true',
                          'execute on owner if entity @s[distance=..24] if block ~ ~ ~ minecraft:water run effect give @s minecraft:dolphins_grace 3 0 true',
                          'execute store result score #r bm.rng run random value 1..5',
                          'execute if score #r bm.rng matches 1 unless predicate bm:swim run particle minecraft:dripping_water ~ ~1.6 ~ 0.6 0.3 0.6 0 2'])
        return lines

    def encounter(G, X):
        # out on the ocean (swimming or in a boat), rarely: a fin beside you
        X.second.append('execute as @a[tag=!bm.bjmet,gamemode=!spectator] at @s if dimension minecraft:overworld if biome ~ ~ ~ #minecraft:is_ocean run function bm:p196/enc/roll')
        fn('p196/enc/roll', ['execute store result score #r bm.rng run random value 1..900', 'execute unless score #r bm.rng matches 1 run return 0',
                             'scoreboard players set #ok bm.rng 0', 'execute if block ~ ~ ~ minecraft:water run scoreboard players set #ok bm.rng 1',
                             'execute if predicate bm:p21/riding run scoreboard players set #ok bm.rng 1',
                             'execute if score #ok bm.rng matches 0 run return 0',
                             'execute if entity @e[type=minecraft:interaction,tag=bm.bjenc,distance=..64] run return 0',
                             'execute positioned ^ ^ ^5 if block ~ ~ ~ minecraft:water run return run function bm:p196/enc/fin',
                             'execute positioned ^3 ^ ^2 if block ~ ~ ~ minecraft:water run return run function bm:p196/enc/fin',
                             'execute positioned ^-3 ^ ^2 if block ~ ~ ~ minecraft:water run function bm:p196/enc/fin'])
        fn('p196/enc/fin', ['function bm:p196/enc/spawn', 'particle minecraft:splash ~ ~1 ~ 1 0.4 1 0.2 60', 'particle minecraft:bubble_column_up ~ ~ ~ 0.6 0.3 0.6 0.05 20',
                            'playsound minecraft:entity.dolphin.splash neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                            X.tellraw('@s', [T('A fin cuts the water beside you. ', BJ_LINE, italic=True),
                                             T('Then a whole grey shark rolls up out of the sea - a scar and stitches over one eye, a skull on his flank - and grins at you with every tooth he has.', 'gray', italic=True)])])
        fn('p196/enc/talk', ['scoreboard players operation #me2 bm.pid = @s bm.pid', 'scoreboard players set #em bm.rng 0',
                             'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..24] if score @s bm.pid = #me2 bm.pid run scoreboard players set #em bm.rng 1',
                             f'execute if items entity @s container.* {holds("bn_whistle")} run return run ' + X.csay('(he nudges the whistle in your pocket with his snout)'),
                             'execute if items entity @s weapon.mainhand minecraft:cod run return run function bm:p196/enc/recruit',
                             'execute if items entity @s weapon.mainhand minecraft:salmon run return run function bm:p196/enc/recruit',
                             'execute if items entity @s weapon.mainhand minecraft:tropical_fish run return run function bm:p196/enc/recruit',
                             'execute if items entity @s weapon.mainhand minecraft:pufferfish run return run ' + X.csay('(he looks at the pufferfish. He looks at you. He is not falling for that.)'),
                             'execute if score #em bm.rng matches 1 run return run ' +
                             tellraw('@s', [T('Emma: ', '#ff9ad8', bold=True), T('"BONES! It\'s you! Oh, you big scary baby! ...He\'d love a fish, if you have one."', '#ffd8f0')]),
                             X.csay('(he circles you, grinning. He is very interested in your hands. Do they have fish in them?)')])
        fn('p196/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:splash ~ ~1 ~ 0.8 0.5 0.8 0.2 40',
                                f'execute as {X.here} at @s run playsound minecraft:entity.dolphin.eat neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                                X.tellraw('@s', [T('CHOMP. ', BJ_LINE, italic=True, bold=True),
                                                 T('The fish is gone, and so - very nearly - are your fingers. He spits a tooth-carved whistle into your hand and grins. You have a shark now.', 'gray', italic=True)]),
                                'execute if score #em bm.rng matches 1 run ' +
                                tellraw('@s', [T('Emma: ', '#ff9ad8', bold=True), T('"He likes you! Bones, this is my friend. Look after them, okay? ...He says okay."', '#ffd8f0')]),
                                'function bm:p196/enc/joined'])

    RP.build(C, G, abilities, encounter)
    sel2 = '@e[type=minecraft:wolf,tag=bm.bjsel2,limit=1]'
    # ---- the whistle's use: riding him - CHOMP
    use = G.FUNCS['p196/use']
    use.insert(0, 'execute if predicate bm:p21/riding if function bm:p196/on_him run return run function bm:p196/chomp')
    fn('p196/on_him', [f'execute on vehicle if entity @s[type=minecraft:wolf,tag={pet}] run return 1', 'return 0'])
    fn('p196/has_rider', ['execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0'])
    fn('p196/ride_ask', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add bm.bjsel2',
                         f'execute unless entity {sel2} run return run ' + say('He isn\'t out - call him first.'),
                         'dialog clear @s', f'tp {sel2} @s', 'function bm:p196/mount', 'tag @e[tag=bm.bjsel2] remove bm.bjsel2'])
    fn('p196/mount', ['execute if predicate bm:p21/riding run return run ' + say('Get off your mount first.'),
                      f'data modify entity {sel2} Sitting set value 0b', f'ride @s mount {sel2}',
                      'playsound minecraft:entity.dolphin.play neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                      title('@s', 'actionbar', [T('On his back. ', BJ_C, bold=True), T('In water he goes where you look - up and down too. The whistle: CHOMP. ', 'gray'),
                                                T('Sneak to get off.', 'dark_gray')])])
    # ---- riding: his rider's facing is his. In water: where you look (pitch too), fast. On land: a float along in his bubble.
    fn('p196/ride', ['tag @s add bm.bjrd', 'data modify entity @s Sitting set value 1b', 'scoreboard players set #fw bm.rng 0',
                     'execute on passengers if predicate bm:p39/forward run scoreboard players set #fw bm.rng 1',
                     'scoreboard players set #jp bm.rng 0', 'execute on passengers if predicate bm:p26/jump_key run scoreboard players set #jp bm.rng 1',
                     'execute on passengers if entity @s[type=minecraft:player] run function bm:p196/rider',
                     'execute on passengers if entity @s[type=minecraft:player] store result score #yaw bm.rng run data get entity @s Rotation[0] 100',
                     'execute on passengers if entity @s[type=minecraft:player] store result score #pitch bm.rng run data get entity @s Rotation[1]',
                     'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bm.rng',
                     'scoreboard players set #wet bm.rng 0', 'execute if block ~ ~0.4 ~ minecraft:water run scoreboard players set #wet bm.rng 1',
                     'execute if score #fw bm.rng matches 1 if score #wet bm.rng matches 1 run function bm:p196/swim',
                     'execute if score #fw bm.rng matches 1 if score #wet bm.rng matches 0 run function bm:p196/drive',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[0] set value 0.0d',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[2] set value 0.0d',
                     'execute if score #fw bm.rng matches 0 if score #wet bm.rng matches 1 unless score #jp bm.rng matches 1 run data modify entity @s Motion[1] set value 0.0d',
                     'execute if score #jp bm.rng matches 1 if score #wet bm.rng matches 1 run data modify entity @s Motion[1] set value 0.3d',
                     'execute if score #jp bm.rng matches 1 if score #wet bm.rng matches 0 if predicate bm:p39/on_ground run data modify entity @s Motion[1] set value 0.45d'])
    fn('p196/swim', ['data modify storage bm:tmp kxd.s set value 0.62d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                     'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                     'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                     'scoreboard players operation #vy bm.rng = #pitch bm.rng', 'scoreboard players operation #vy bm.rng *= #-7 bm.rng',
                     'execute store result entity @s Motion[1] double 0.001 run scoreboard players get #vy bm.rng',
                     'particle minecraft:bubble ~ ~0.4 ~ 0.4 0.2 0.4 0.02 3'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #-7 bm.rng -7']
    fn('p196/drive', ['data modify storage bm:tmp kxd.s set value 0.3d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                      'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                      'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    fn('p196/rider', ['tag @s add bm.bjrider', 'effect give @s minecraft:water_breathing 3 0 true', 'effect give @s minecraft:dolphins_grace 3 0 true',
                      'execute unless entity @s[tag=bm.bjfall] run attribute @s minecraft:fall_damage_multiplier modifier add bm:bj_ride -1 add_multiplied_total',
                      'tag @s add bm.bjfall'])
    fn('p196/unride', ['tag @s remove bm.bjrd', 'data modify entity @s Sitting set value 0b', 'scoreboard players set @s bm.bzs -1'])
    G.FUNCS['loop/second'][-1:-1] = ['execute as @a[tag=bm.bjrider] unless function bm:p196/on_him run function bm:p196/rider_off']
    fn('p196/rider_off', ['tag @s remove bm.bjrider', 'tag @s remove bm.bjfall', 'attribute @s minecraft:fall_damage_multiplier modifier remove bm:bj_ride'])
    G.FUNCS['p196/state'].insert(0, 'execute if entity @s[tag=bm.bjrd] run return run function bm:p196/ride_state')
    fn('p196/ride_state', ['execute if block ~ ~0.4 ~ minecraft:water run return run scoreboard players set #st bm.rng 10',
                           'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                           'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                           'scoreboard players operation #vx bm.rng += #vz bm.rng',
                           'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                           'scoreboard players set #st bm.rng 0'])
    # ---- CHOMP (from his back): he lunges at what's ahead - every 1.5 s
    fn('p196/chomp', ['execute if score @s bm.bjch matches 1.. run return run ' + say('(he\'s still chewing)'),
                      'scoreboard players set @s bm.bjch 30', 'tag @s add bm.bjchr',
                      'playsound minecraft:entity.dolphin.attack neutral @a[distance=..24] ~ ~ ~ 1 0.5', 'playsound minecraft:entity.evoker_fangs.attack neutral @a[distance=..24] ~ ~ ~ 0.8 1.2',
                      'execute rotated ~ 0 positioned ^ ^ ^2.4 run particle minecraft:sweep_attack ~ ~0.8 ~ 0.4 0.2 0.4 0 3',
                      'execute rotated ~ 0 positioned ^ ^ ^2.4 as @e[type=#bm:hostile,tag=!bm.npc,distance=..2.2] at @s run function bm:p196/chomped',
                      'tag @s remove bm.bjchr'])
    fn('p196/chomped', ['damage @s 12 minecraft:mob_attack by @a[tag=bm.bjchr,limit=1]', 'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.3 0.3 0.1 6'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.bjch dummy']
    G.OBJECTIVES += ['bm.bjch']
    G.FUNCS['tick'].append('scoreboard players remove @a[scores={bm.bjch=1..}] bm.bjch 1')
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.bjrider] run function bm:p196/rider_off']
    # (the water he swims through, and the air he swims in on land: a tag of what doesn't stop him)
    G.wjson('bm/tags/block/swim_pass.json', {'values': ['#bm:grap_pass', 'minecraft:water', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp',
                                                        'minecraft:kelp_plant', 'minecraft:bubble_column']})
