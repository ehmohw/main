"""2.77: THE NEW PAIRS AND TRIOS - Tullius and Apophiss in company, and a hidden trio.

PAIRS (the follower and a partner of the same summoner, within 16 blocks of each other):
- TULLIUS + CELI, "Frost and Brine": two cold hearts. You hit harder (Strength); monsters near you are slowed by the
  frost round the three of you; the pair shrug off blows (Resistance).
- TULLIUS + LEO, "Old Rivals": they race each other for every kill. You keep up (Speed, Haste II); both hit harder.
- APOPHISS + EMMA, "Forgiven": she forgave him; he'd never admit it matters. You regenerate, and a shield of absorption
  comes back every half minute; she heals him, and his Wrath builds faster.
- APOPHISS + KILLERWATT, "Venom and Volts": two monsters who get on rather well. You hit harder and see in the dark; both
  of their charged attacks build faster.
TRIOS (three at your side at once, within 24 - phase100's rules: one trio at a time, a hidden achievement each):
- TULLIUS, CELI AND LEO, "The Tidewatch": Strength and Resistance for you, Water Breathing and Dolphin's Grace at sea;
  the three tougher and healing; every 20 seconds a frost wave slows every monster round you.
- APOPHISS, EMMA AND LEO, "An Uneasy Truce": old enemies, side by side. Regeneration, Resistance and two more hearts;
  the three tougher.
- APOPHISS, KILLERWATT AND DEMOCRATUS, "The Dread Court": Strength II and Speed; monsters near you cower (Weakness,
  Slowness); the three charge their great attacks faster.
- (hidden) EMMA, LEO AND PEARLMAN, "The Royal Retinue": a princess, her knight and her most devoted merchant.
  Regeneration, Luck and Hero of the Village; Pearlman's appraisal pays out twice as often.
"""
from items import T
import phase100 as P100

GOLD = '#ffcf40'
P100.WHO['pearl'] = ('cat', 'bm.pmpet')
P100.VOICE['Pearlman'] = ('#e8f2ff', '#d8e8ff')
NEW_TRIOS = {
    'tide': ('The Tidewatch', '#8ad8f0', ('tul', 'celi', 'leo'), 'The Tidewatch', 'Walk with Tullius, Celi and Leo at once'),
    'truce': ('An Uneasy Truce', '#c8e070', ('apo', 'emma', 'leo'), 'An Uneasy Truce', 'Walk with Apophiss, Emma and Leo at once'),
    'dread': ('The Dread Court', '#9a6ae0', ('apo', 'kw', 'demo'), 'The Dread Court', 'Walk with Apophiss, KillerWatt and Democratus at once'),
    'retinue': ('The Royal Retinue', '#ffd8f0', ('emma', 'leo', 'pearl'), 'The Royal Retinue', 'Walk with Emma, Leo and Pearlman at once'),
}
# (the last trio that matches wins: the hidden Retinue goes first. 2.77: Pearlman didn't count toward the three, so he could walk
#  beside a whole other trio and must never take its place; 2.77c: he counts now, so there's never a fourth - the order stays)
_old = dict(P100.TRIOS)
P100.TRIOS.clear()
P100.TRIOS['retinue'] = NEW_TRIOS['retinue']
P100.TRIOS.update(_old)
P100.TRIOS.update({k: v for k, v in NEW_TRIOS.items() if k != 'retinue'})
P100.BANTER.update({
    'tide': [('Tullius', 'Leo. Celi. Try not to slow me down.', 'Celi', 'Says the man who walks like a shipwreck.'),
             ('Leo', 'For the shore, Tullius - like the old days.', 'Tullius', 'The old days drowned, Leo. I was there.'),
             ('Celi', 'Two old soldiers and me. Lucky me.', 'Tullius', 'You are the only one of us who is still warm, little wolf. Enjoy it.')],
    'truce': [('Emma', 'Apophiss! Say sorry to Leo for the time you ate his shield.', 'Apophiss', 'I did NOT eat it. I merely... kept it.'),
              ('Leo', 'One wrong move near the Princess, serpent.', 'Apophiss', 'Relax, tin knight. If I wanted her, I would have had her years ago.'),
              ('Apophiss', 'This is humiliating.', 'Emma', "It's called being FRIENDS!")],
    'dread': [('Democratus', 'A serpent, a storm and a reaper. The living should be very afraid.', 'Apophiss', 'They usually are. It is the best part.'),
              ('KillerWatt', '*thunder rumbles; he bumps his head against the serpent*', 'Apophiss', '...Fine. You may stay. You are warm, at least.'),
              ('Apophiss', 'Kneel, little mortals! Kneel to the Dread Court!', 'Democratus', 'They cannot hear you over the thunder.')],
    'retinue': [('Pearlman', 'Princess! Sir Leo! Pearlman is honoured, HONOURED! Have you seen my newest wares?', 'Emma', 'Pearlman! Do you have ribbons?!'),
                ('Leo', 'Stay close, Princess - and keep an eye on your coin purse.', 'Pearlman', 'Sir Leo! Pearlman is wounded. Only slightly. Ten percent off?'),
                ('Emma', 'Pearlman, you can be in our royal court!', 'Pearlman', 'Royal Purveyor of Fine Goods? Oh, Pearlman could weep.')],
})
ICON = {'tide': 'bm:tul_coin', 'truce': 'bm:apo_oath', 'dread': 'bm:apo_oath', 'retinue': 'bm:pearl_card'}


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    second = []
    mine = lambda k: f'@e[type=minecraft:{P100.WHO[k][0]},tag={P100.WHO[k][1]},distance=..24]'
    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    regen = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    # ================================================================== the trios (phase100 tags who's here and calls p100/<key> as the player)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p133 dummy']
    G.OBJECTIVES += ['bm.p133']
    fn('p100/tide', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:resistance 3 0 true',
                     'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:water_breathing 12 0 true',
                     'execute if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 4 0 true'] +
       each(NEW_TRIOS['tide'][2], 'effect give @s minecraft:resistance 3 0 true') + each(NEW_TRIOS['tide'][2], regen) +
       ['scoreboard players add @s bm.p133 1', 'execute if score @s bm.p133 matches 20.. run function bm:p133/frost_wave', 'function bm:p100/banter_tick'])
    fn('p133/frost_wave', ['scoreboard players set @s bm.p133 0', 'particle minecraft:snowflake ~ ~0.5 ~ 4 0.3 4 0.05 80',
                           'playsound minecraft:block.powder_snow.place player @a[distance=..16] ~ ~ ~ 1 0.6',
                           f'effect give @e[{foe},distance=..8] minecraft:slowness 5 2'])
    fn('p100/truce', ['execute unless predicate bm:p100/hb run effect give @s minecraft:health_boost 15 0 true', regen, 'effect give @s minecraft:resistance 3 0 true'] +
       each(NEW_TRIOS['truce'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    fn('p100/dread', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:speed 3 0 true',
                      f'effect give @e[{foe},distance=..8] minecraft:weakness 3 0', f'effect give @e[{foe},distance=..8] minecraft:slowness 3 0',
                      'scoreboard players add @s bm.p133 1', 'execute if score @s bm.p133 matches 4.. run scoreboard players set @s bm.p133 0'] +
       each(NEW_TRIOS['dread'][2], 'effect give @s minecraft:resistance 3 0 true') +
       ['execute if score @s bm.p133 matches 0 as ' + mine('kw') + ' if function bm:p100/is_mine run scoreboard players add @s bm.kxch 1',
        'execute if score @s bm.p133 matches 0 as ' + mine('demo') + ' if function bm:p100/is_mine run scoreboard players add @s bm.dmch 1',
        'execute if score @s bm.p133 matches 0 as ' + mine('apo') + ' if function bm:p100/is_mine run scoreboard players add @s bm.apch 1',
        'execute if score @s bm.p133 matches 0 run particle minecraft:dust{color:[0.6,0.4,0.9],scale:1.2} ~ ~1 ~ 1.4 0.8 1.4 0 14',
        'function bm:p100/banter_tick'])
    fn('p100/retinue', [regen, 'effect give @s minecraft:luck 3 0 true', 'effect give @s minecraft:hero_of_the_village 3 0 true',
                        'scoreboard players set @s bm.p133r 3', 'function bm:p100/banter_tick'])
    # (Pearlman's appraisal, twice over while the Retinue walks with you: a second 1-in-5 for an emerald back)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p133r dummy']
    G.OBJECTIVES += ['bm.p133r']
    ap = G.FUNCS['p128/pm/appraise']
    ap.insert(1, 'execute if score @s bm.p133r matches 1.. run function bm:p133/retinue_gift')
    fn('p133/retinue_gift', ['execute store result score #r bm.rng run random value 1..5', 'execute unless score #r bm.rng matches 1 run return 0',
                             'give @s minecraft:emerald 1', 'playsound minecraft:entity.villager.celebrate player @s ~ ~ ~ 0.8 1.2',
                             title('@s', 'actionbar', T('Pearlman slips you an emerald - "For the Royal Retinue!"', '#e8f2ff'))])
    second.append('scoreboard players remove @a[scores={bm.p133r=1..}] bm.p133r 1')
    # (the trios' advancement icons: their own followers' items)
    for k, (nm, col, mem, at, desc) in NEW_TRIOS.items():
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': ICON[k]}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal', 'show_toast': True,
                                                                 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== the pairs: every second, as each Tullius / Apophiss
    pet = lambda typ, tag: f'execute as @e[type=minecraft:{typ},tag={tag},distance=..16] if score @s bm.pid = #me bm.pid'
    VO = {'Celi': ('#9ad8ff', '#e0f6ff'), 'Leo': ('#5ab8e0', '#d8f0ff'), 'Emma': ('#ff8ad8', '#ffd0ec'), 'KillerWatt': ('#74d462', '#c8f0c0'),
          'Tullius': ('#8ad8f0', '#d8f4ff'), 'Apophiss': ('#3ad06a', '#c8f0b0')}
    say2 = lambda who, txt: tellraw('@a[tag=bm.p133o]', [T(f'{who}: ', VO[who][0], bold=True), T(txt if who == 'KillerWatt' else f'"{txt}"', VO[who][1], italic=who == 'KillerWatt')])
    PAIRS = {  # key: (follower host tag, partner (type, tag), name, colour, intro (a, b), banter [(who, line, who, line)])
        'frost': ('bm.tupet', ('wolf', 'bm.celipet'), 'Frost and Brine', '#8ad8f0',
                  [('Celi', 'Oh, wonderful. Another grump who smells like the sea.'), ('Tullius', 'And you smell like wet dog. We all have our burdens.')],
                  [('Celi', 'You are freezing the ground I walk on.', 'Tullius', 'Then walk faster.'),
                   ('Tullius', 'That last one - mine or yours?', 'Celi', 'Mine. Obviously. You were busy reloading.')]),
        'rivals': ('bm.tupet', ('wolf', 'bm.leopet'), 'Old Rivals', '#5ab8e0',
                   [('Leo', 'Tullius. You came back.'), ('Tullius', 'The sea spat me out, Leo. Even it could not stand me. Keep up.')],
                   [('Tullius', 'Seven to your five, knight.', 'Leo', 'Six. That one was already falling.'),
                    ('Leo', 'You still fight like you have something to prove.', 'Tullius', 'And you still fight like you already proved it.')]),
        'forgiven': ('bm.appet', ('cat', 'bm.emmapet'), 'Forgiven', '#ff8ad8',
                     [('Emma', 'Apophiss! You came to help! I KNEW you were nice really!'), ('Apophiss', '...I am here for the violence, child. Purely the violence.')],
                     [('Emma', 'Apophiss, you can have my healing. All of it!', 'Apophiss', 'Hmph. ...Thank you, princess.'),
                      ('Apophiss', 'Stop hugging my tail.', 'Emma', 'No!')]),
        'volts': ('bm.appet', ('wolf', 'bm.kxpet'), 'Venom and Volts', '#74d462',
                  [('KillerWatt', '*sparks crackle - he sniffs at the serpent, curious*'), ('Apophiss', 'Ah. Finally, someone worth talking to.')],
                  [('KillerWatt', '*thunder rolls in his chest*', 'Apophiss', 'I know. Them too. Pathetic.'),
                   ('Apophiss', 'You and I could rule this world, you know.', 'KillerWatt', '*a happy crackle*')]),
    }
    for k, (htag, (ptype, ptag), nm, col, intro, banter) in PAIRS.items():
        fn(f'p133/{k}_first', [f'advancement grant @s only bm:story/pair_{k}',
                               tellraw('@s', PREFIX + [T(f'{nm}! ', col, bold=True), T('A new pair - see the README for what it gives.', 'gray')]),
                               tellraw('@s', [T(f'{intro[0][0]}: ', VO[intro[0][0]][0], bold=True), T(intro[0][1] if intro[0][0] == 'KillerWatt' else f'"{intro[0][1]}"', VO[intro[0][0]][1])]),
                               tellraw('@s', [T(f'{intro[1][0]}: ', VO[intro[1][0]][0], bold=True), T(f'"{intro[1][1]}"', VO[intro[1][0]][1])])])
        wjson(f'bm/advancement/story/pair_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                      'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:tul_coin' if htag == 'bm.tupet' else 'bm:apo_oath'}},
                                                                  'title': T(nm, 'yellow'), 'description': T({'frost': 'Tullius and Celi, side by side', 'rivals': 'Tullius and Leo, racing for every kill',
                                                                                                              'forgiven': 'Apophiss and Emma - forgiven', 'volts': 'Apophiss and KillerWatt, two monsters together'}[k], 'gray'),
                                                                  'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
        for j, (a, ta, b, tb) in enumerate(banter):
            fn(f'p133/{k}_say{j}', [say2(a, ta), say2(b, tb)])
    bant = lambda k: ['scoreboard players add @s bm.p133 1', 'execute if score @s bm.p133 matches 150.. run function bm:p133/' + k + '_banter']
    for k, (_h, _p, _n, _c, _i, banter) in PAIRS.items():
        fn(f'p133/{k}_banter', ['scoreboard players set @s bm.p133 0', f'execute store result score #r bm.rng run random value 0..{len(banter) - 1}'] +
           [f'execute if score #r bm.rng matches {j} run function bm:p133/{k}_say{j}' for j in range(len(banter))])
    first = lambda k: f'execute as @a[tag=bm.p133o] unless entity @s[advancements={{bm:story/pair_{k}=true}}] run function bm:p133/{k}_first'
    # Tullius's pairs
    second.append('execute as @e[type=minecraft:wolf,tag=bm.tupet,tag=!bm.ffpet] at @s run function bm:p133/tul')
    fn('p133/tul', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p133o',
                    'execute unless entity @a[tag=bm.p133o] run return 0',
                    'scoreboard players set #pc bm.rng 0', 'scoreboard players set #pl bm.rng 0',
                    f'{pet("wolf", "bm.celipet")} run scoreboard players set #pc bm.rng 1', f'{pet("wolf", "bm.leopet")} run scoreboard players set #pl bm.rng 1',
                    'execute if score #pc bm.rng matches 1 run function bm:p133/frost', 'execute if score #pl bm.rng matches 1 run function bm:p133/rivals',
                    'tag @a remove bm.p133o'])
    fn('p133/frost', ['effect give @a[tag=bm.p133o] minecraft:strength 3 0 true', 'effect give @s minecraft:resistance 3 0 true',
                      f'{pet("wolf", "bm.celipet")} run effect give @s minecraft:resistance 3 0 true',
                      f'execute at @a[tag=bm.p133o] run effect give @e[{foe},distance=..6] minecraft:slowness 3 0',
                      'execute at @a[tag=bm.p133o] if entity @e[type=#bm:hostile,tag=!bm.npc,distance=..6] run particle minecraft:snowflake ~ ~0.3 ~ 2.5 0.2 2.5 0.02 6',
                      first('frost')] + bant('frost'))
    fn('p133/rivals', ['effect give @a[tag=bm.p133o] minecraft:speed 3 0 true', 'effect give @a[tag=bm.p133o] minecraft:haste 3 1 true',
                       'effect give @s minecraft:strength 3 0 true', f'{pet("wolf", "bm.leopet")} run effect give @s minecraft:strength 3 0 true',
                       first('rivals')] + bant('rivals'))
    # Apophiss's pairs
    second.append('execute as @e[type=minecraft:wolf,tag=bm.appet,tag=!bm.ffpet] at @s run function bm:p133/apo')
    fn('p133/apo', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p133o',
                    'execute unless entity @a[tag=bm.p133o] run return 0',
                    'scoreboard players set #pe bm.rng 0', 'scoreboard players set #pk bm.rng 0',
                    f'{pet("cat", "bm.emmapet")} run scoreboard players set #pe bm.rng 1', f'{pet("wolf", "bm.kxpet")} run scoreboard players set #pk bm.rng 1',
                    'execute if score #pe bm.rng matches 1 run function bm:p133/forgiven', 'execute if score #pk bm.rng matches 1 run function bm:p133/volts',
                    'tag @a remove bm.p133o'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p133s dummy']
    G.OBJECTIVES += ['bm.p133s']
    fn('p133/forgiven', ['execute as @a[tag=bm.p133o] unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true',
                         'scoreboard players add @s bm.p133s 1', 'execute if score @s bm.p133s matches 30.. as @a[tag=bm.p133o] unless predicate bm:p100/abs at @s run function bm:p133/shield',
                         'execute if score @s bm.p133s matches 30.. run scoreboard players set @s bm.p133s 0',
                         'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 4 0 true', 'scoreboard players add @s bm.apch 1',
                         first('forgiven')] + bant('forgiven'))
    fn('p133/shield', ['effect give @s minecraft:absorption 30 0 true', 'particle minecraft:heart ~ ~1.8 ~ 0.4 0.3 0.4 0 4'])
    fn('p133/volts', ['effect give @a[tag=bm.p133o] minecraft:strength 3 0 true', 'effect give @a[tag=bm.p133o] minecraft:night_vision 15 0 true',
                      'scoreboard players add @s bm.p133s 1', 'execute if score @s bm.p133s matches 4.. run scoreboard players set @s bm.p133s 0',
                      'execute if score @s bm.p133s matches 0 run scoreboard players add @s bm.apch 1',
                      f'execute if score @s bm.p133s matches 0 {pet("wolf", "bm.kxpet")[8:]} run scoreboard players add @s bm.kxch 1',
                      first('volts')] + bant('volts'))
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
