"""2.76: PEARLMAN'S GOLDEN STATUE - and Pearlman himself, off the clock.

THE COLLECTION: every gem you buy from Pearlman out in the world counts toward his nine (the vault's gems never do - not
  the Recruiter's, nor any bought in the heist lobby). Each new one is ticked off in chat with the ones still to find.
ALL NINE: Pearlman tips his top hat - GOLD STANDARD (a hidden challenge) - and hands you PEARLMAN'S GOLDEN STATUE and his
  BUSINESS CARD.
THE STATUE: sneak + use on the top of a block to set it up (sneak + punch it to take it back). Within 32 blocks of it,
  villagers trade at about half price - you're their Hero of the Village (IV) while you're near it - and now and then toss
  you a gift. The Black Market's own traders (and Pearlman) don't play along: near them the discount is lifted.
PEARLMAN, THE FOLLOWER (his Business Card: use it to call him; again to call him over; sneak + use for his card's menu):
  not a fighter - he can't be hurt and never faints - but a salesman. While he's close:
    GIFT OF THE GAB   villagers trade cheaper and toss you gifts (Hero of the Village I; the statue's IV wins near it)
    A LUCKY FLIPPER   Luck: better fishing, better chests
    PENGUIN STROKE    in water you swim like he does (Dolphin's Grace)
    APPRAISAL         every trade with a villager near him: a 1 in 5 chance he haggles you an emerald back
  He waddles after you, sits when told (right-click him, or from his menu), and chats now and then (the Ledger's chatter
  switch hushes him). He goes home like the others when you go too far, put his card away or fall. Not in the vault.
LOST THEM? Pearlman never forgets a customer: trade with him once and a lost statue or card is replaced.
"""
import copy
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, D, Int
import phase60 as P60
import phase73 as P73

PEARL = '#5ac8ff'
GOLD = '#ffcf40'
KEYS = P60.KEYS
MENU = 970
STATUE_R = 32                       # villagers within this of the statue: half price
NPC_R = 16                          # ...but never near the Black Market's own traders
PS = 0.55                           # the follower's size

item('pearl_statue', TOTEM, "Pearlman's Golden Statue", GOLD,
     ['Solid gold. Very handsome. Tipping his hat.', ('Sneak + use on a block: set it up.', 'blue'),
      (f'Villagers within {STATUE_R} blocks trade at about', 'blue'), ('half price (not the Black Market\'s traders).', 'blue'),
      ('Sneak + punch it: take it back.', 'gray'), ('"For my finest customer." - P.', 'dark_gray')],
     model='bm:pearl_statue', glint=True, stack=1, cat='relic', comps=hold('none'), bold=True)
HOLD['pearl_statue'] = 'bm:p128/statue/use'
item('pearl_card', TOTEM, "Pearlman's Business Card", PEARL,
     ['PEARLMAN - Gems, Fine Goods, Appraisals.', 'Embossed. Smells faintly of fish.', ('Use: call Pearlman (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('Not a fighter - a salesman: cheaper villagers,', 'gray'), ('Luck, and he swims you along.', 'gray')],
     model='bm:pearl_card', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['pearl_card'] = 'bm:p128/pm/use'


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    pmsay = lambda txt, who='@s': title(who, 'actionbar', [T('Pearlman: ', PEARL, bold=True), T(txt, 'white')])
    tick, fast, second = [], [], []
    objs = ['bm.pmw', 'bm.pmq', 'bm.fgp']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    import phase28 as P28
    ident = [F(0), F(0), F(0), F(1)]
    GEMS = P60.GEMS

    # ================================================================== THE COLLECTION: Pearlman's own gems, out in the world
    for k in KEYS:
        wjson(f'bm/advancement/p128/buy_{k}.json', {'criteria': {'t': {'trigger': 'minecraft:villager_trade', 'conditions': {
            'player': [{'condition': 'minecraft:location_check', 'predicate': {'dimension': 'minecraft:overworld'}}],
            'villager': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.pearl"]}'}}],
            'item': {'items': TOTEM, 'predicates': {'minecraft:custom_data': f'{{bm:"gem_{k}"}}'}}}}}, 'rewards': {'function': f'bm:p128/buy/{k}'}})
        fn(f'p128/buy/{k}', [f'advancement revoke @s only bm:p128/buy_{k}', f'execute if entity @s[tag=bm.pmg_{k}] run return 0',
                             f'tag @s add bm.pmg_{k}', 'function bm:p128/tally'])
    fn('p128/tally', ['scoreboard players set #n bm.rng 0'] + [f'execute if entity @s[tag=bm.pmg_{k}] run scoreboard players add #n bm.rng 1' for k in KEYS] +
       ['execute if score #n bm.rng matches 9 unless entity @s[tag=bm.pmstat] run return run function bm:p128/earn',
        'data modify storage bm:tmp pmc set value []'] +
       [f'execute unless entity @s[tag=bm.pmg_{k}] run data modify storage bm:tmp pmc append value {snbt(T(" " + k.capitalize(), GEMS[k][1]))}' for k in KEYS] +
       [tellraw('@s', PREFIX + [T('Pearlman\'s collection: ', PEARL, bold=True), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                T(' of 9. Still to find:', 'gray'), {'nbt': 'pmc[]', 'storage': 'bm:tmp', 'interpret': True, 'separator': ','}]),
        'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.4'])
    fn('p128/earn', ['tag @s add bm.pmstat', 'advancement grant @s only bm:story/gold_standard', give('pearl_statue'), give('pearl_card'),
                     tellraw('@s', [T('Pearlman: ', PEARL, bold=True), T('"All nine! My dear, dear connoisseur. Pearlman is touched - truly."', 'white')]),
                     tellraw('@s', [T('Pearlman ', PEARL, bold=True), T('tips his top hat and presses two things into your hands: a little golden statue of himself, '
                                                                         'and his business card.', 'gray', italic=True)]),
                     tellraw('@s', [T('Pearlman: ', PEARL, bold=True), T('"Set the statue in a village - folk there will practically give their wares away. And should you '
                                                                         'ever want a business partner... you have my card."', 'white')]),
                     'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.4 60',
                     'particle minecraft:wax_on ~ ~1.2 ~ 0.6 0.8 0.6 0 30'])
    wjson('bm/advancement/story/gold_standard.json', {'parent': 'bm:story/pearlman', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:pearl_statue'}},
                      'title': T('Gold Standard', 'gold'), 'description': T('Buy every one of Pearlman\'s nine gems from him', 'gray'),
                      'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    # lost the statue or the card? any trade with him puts it right
    has = lambda iid: [f'execute if items entity @s container.* *[minecraft:custom_data~{{bm:"{iid}"}}] run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"{iid}"}}] run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s enderchest.* *[minecraft:custom_data~{{bm:"{iid}"}}] run scoreboard players set #has bm.rng 1']
    G.FUNCS['p60/pm/traded'].append('execute if entity @s[tag=bm.pmstat] run function bm:p128/reissue')
    fn('p128/reissue', ['scoreboard players set #has bm.rng 0'] + has('pearl_statue') +
       ['execute as @e[type=minecraft:interaction,tag=bm.pmst] if score @s bm.pid = @a[tag=bm.pmrq,limit=1] bm.pid run scoreboard players set #has bm.rng 1'] +
       ['execute if score #has bm.rng matches 0 run ' + give('pearl_statue'),
        'execute if score #has bm.rng matches 0 run ' + tellraw('@s', [T('Pearlman: ', PEARL, bold=True), T('"Misplaced your statue? Pearlman never forgets a customer. Here."', 'white')]),
        'scoreboard players set #has bm.rng 0'] + has('pearl_card') +
       ['execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = @a[tag=bm.pmrq,limit=1] bm.pid run scoreboard players set #has bm.rng 1',
        'execute if score #has bm.rng matches 0 run ' + give('pearl_card'),
        'execute if score #has bm.rng matches 0 run ' + tellraw('@s', [T('Pearlman: ', PEARL, bold=True), T('"And another card - do try not to lose this one."', 'white')])])
    rq = G.FUNCS['p128/reissue']
    rq[0:0] = ['tag @s add bm.pmrq']
    rq.append('tag @s remove bm.pmrq')

    # ================================================================== THE STATUE: set it up; villagers near it trade at half price
    fn('p128/statue/use', ['execute unless predicate bm:p20/sneaking run return run ' + say(f'Sneak + use on a block: set the statue up. (Villagers within {STATUE_R} blocks: half price.)', GOLD),
                           'execute if dimension bm:gutter run return run ' + say('Not in the vault - set it up out in the world.'),
                           'execute if dimension bm:hollow_throne run return run ' + say('Not here - set it up out in the world.'),
                           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                           'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                           'execute anchored eyes positioned ^ ^ ^ run function bm:p128/statue/ray', 'tag @s remove bm.placer',
                           'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.'),
                           'execute unless entity @s[gamemode=creative] if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"pearl_statue"}] run return run item replace entity @s weapon.mainhand with minecraft:air',
                           'execute unless entity @s[gamemode=creative] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"pearl_statue"}] run item replace entity @s weapon.offhand with minecraft:air'])
    fn('p128/statue/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p128/statue/hit',
                           'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p128/statue/ray'])
    fn('p128/statue/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                           'execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~1 ~ #minecraft:replaceable run return 0',
                           'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.gvdeco,distance=..0.8] run return 0',
                           'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p128/statue/place', 'scoreboard players set #placed bm.rng 1'])
    disp = {'Tags': ['bm.pmstd', 'bm.pmnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:pearlman_gold'}},
            'item_display': 'fixed', 'brightness': {'sky': Int(14), 'block': Int(14)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.6), F(0)], 'scale': [F(1.2)] * 3}}
    fn('p128/statue/place', ['summon minecraft:item_display ~ ~ ~ ' + snbt(disp),
                             'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.pmst', 'bm.gvdeco', 'bm.pmnew'], 'width': F(0.9), 'height': F(2.3), 'response': B(1)}),
                             'scoreboard players operation @e[type=minecraft:interaction,tag=bm.pmnew,distance=..0.5] bm.pid = @s bm.pid',
                             'execute as @e[type=minecraft:item_display,tag=bm.pmnew,distance=..0.5] at @s facing entity @a[tag=bm.placer,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                             'tag @e[tag=bm.pmnew,distance=..0.5] remove bm.pmnew',
                             'particle minecraft:wax_on ~ ~1 ~ 0.4 0.8 0.4 0 30', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.6 0.3 0.2 20',
                             'playsound minecraft:block.amethyst_block.resonate block @a[distance=..16] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.villager.celebrate neutral @a[distance=..16] ~ ~ ~ 0.8 1.2',
                             title('@a[tag=bm.placer]', 'actionbar', [T('Pearlman\'s Golden Statue gleams. ', GOLD, bold=True), T(f'Villagers within {STATUE_R} blocks: about half price.', 'gray')])])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.pmst] at @s run function bm:p128/statue/sec')
    fn('p128/statue/sec', [f'execute as @a[distance=..{STATUE_R},gamemode=!spectator] at @s unless entity @e[type=minecraft:villager,tag=bm.npc,distance=..{NPC_R}] '
                           'unless dimension bm:gutter run function bm:p128/hero4',
                           'execute store result score #r bm.rng run random value 0..5',
                           'execute if score #r bm.rng matches 0 run particle minecraft:wax_on ~ ~1.6 ~ 0.3 0.6 0.3 0 3',
                           f'execute if score #r bm.rng matches 1 as @e[type=minecraft:villager,tag=!bm.npc,distance=..{STATUE_R},sort=random,limit=1] at @s run particle minecraft:happy_villager ~ ~2 ~ 0.3 0.2 0.3 0 3'])
    fn('p128/hero4', ['effect give @s minecraft:hero_of_the_village 4 3 true', 'tag @s add bm.pmhero'])
    # (the Black Market's traders - Pearlman too - never see the discount: it's lifted near them, at once)
    tick.append(f'execute as @a[tag=bm.pmhero] at @s if entity @e[type=minecraft:villager,tag=bm.npc,distance=..{NPC_R}] run function bm:p128/unhero')
    fn('p128/unhero', ['effect clear @s minecraft:hero_of_the_village', 'tag @s remove bm.pmhero'])
    second.append(f'execute as @a[tag=bm.pmhero] at @s unless entity @e[type=minecraft:interaction,tag=bm.pmst,distance=..{STATUE_R + 2}] '
                  'unless entity @e[type=minecraft:cat,tag=bm.pmpet,distance=..18] run tag @s remove bm.pmhero')
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.pmst] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'run function bm:p128/statue/take']
    fn('p128/statue/take', [give('pearl_statue'), 'kill @e[type=minecraft:item_display,tag=bm.pmstd,distance=..0.6]',
                            'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 0.8 1.2', 'particle minecraft:wax_off ~ ~1 ~ 0.4 0.8 0.4 0 20'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.pmstd]', 'kill @e[type=minecraft:interaction,tag=bm.pmst]',
                                       'execute as @e[type=minecraft:cat,tag=bm.pmpet] run tp @s ~ -400 ~', 'kill @e[type=minecraft:item_display,tag=bm.pmd]']
    fn('admin/pearlman_statue', [give('pearl_statue'), give('pearl_card'), 'tag @s add bm.pmstat'] + [f'tag @s add bm.pmg_{k}' for k in KEYS])

    # ================================================================== PEARLMAN, THE FOLLOWER (an invisible tamed cat that can't be hurt, his model on it)
    host = {'Tags': ['bm.pmpet', 'bm.pmnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Invulnerable': B(1), 'Health': F(20),
            'CustomName': T('Pearlman', PEARL, bold=True), 'CustomNameVisible': B(0),
            'attributes': [{'id': 'minecraft:movement_speed', 'base': D(0.32)}, {'id': 'minecraft:follow_range', 'base': D(32)},
                           {'id': 'minecraft:step_height', 'base': D(1.0)}, {'id': 'minecraft:scale', 'base': D(0.8)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    pdisp = {'Tags': ['bm.pmd', 'bm.pmnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:pearlman'}},
             'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(5),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(PS / 2), F(0)], 'scale': [F(PS)] * 3}}
    sel_pet = 'execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid'
    fn('p128/pm/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'{sel_pet} run tag @s add bm.pmsel2',
                       'execute if entity @e[type=minecraft:cat,tag=bm.pmsel2] if predicate bm:p20/sneaking run function bm:p128/pm/menu',
                       'execute if entity @e[type=minecraft:cat,tag=bm.pmsel2] unless predicate bm:p20/sneaking run function bm:p128/pm/recall',
                       'execute unless entity @e[type=minecraft:cat,tag=bm.pmsel2] unless predicate bm:p20/sneaking run function bm:p128/pm/try',
                       'execute unless entity @e[type=minecraft:cat,tag=bm.pmsel2] if predicate bm:p20/sneaking run ' + say("Pearlman isn't with you. (Use his card to call him.)"),
                       'tag @e[tag=bm.pmsel2] remove bm.pmsel2'])
    # (2.77c: he counts toward the three like anyone else - three out already, and he waits his turn)
    fn('p128/pm/try', ['execute unless function bm:p74/fol_ok run return run ' + pmsay('"In there? Oh no, no. Pearlman does not do heists."'),
                       'execute if function bm:p58/full run return 0',
                       'function bm:p128/pm/summon'])
    G.FUNCS['p58/count'][-1:-1] = ['execute as @e[type=minecraft:cat,tag=bm.pmpet] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    fn('p128/pm/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p128/pm/summon_here',
                          'function bm:p128/pm/summon_here'])
    fn('p128/pm/summon_here', [f'summon minecraft:cat ~ ~ ~ {snbt(host)}', f'summon minecraft:item_display ~ ~ ~ {snbt(pdisp)}',
                               'data modify entity @e[type=minecraft:cat,tag=bm.pmnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                               'scoreboard players operation @e[tag=bm.pmnew,distance=..4] bm.pid = @s bm.pid',
                               'tag @e[tag=bm.pmnew,distance=..4] remove bm.pmnew',
                               'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.02 30', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.4 0.3 0.02 10',
                               'playsound minecraft:block.note_block.bell neutral @a[distance=..20] ~ ~ ~ 1 1.6', 'playsound minecraft:entity.parrot.ambient neutral @a[distance=..20] ~ ~ ~ 0.7 0.7',
                               pmsay('"Pearlman, off the clock and at your service! Shall we go bargain-hunting?"')])
    fn('p128/pm/recall', ['tp @e[type=minecraft:cat,tag=bm.pmsel2,limit=1] @s', 'data modify entity @e[type=minecraft:cat,tag=bm.pmsel2,limit=1] Sitting set value 0b',
                          'particle minecraft:snowflake ~ ~1 ~ 0.4 0.6 0.4 0.02 16', 'playsound minecraft:entity.parrot.ambient neutral @a[distance=..16] ~ ~ ~ 0.7 0.8',
                          pmsay('"Coming, coming! These flippers were not made for sprinting."')])
    # his card's menu
    dlg = P28.multi([T("Pearlman's Business Card", PEARL, bold=True)],
                    [P28.body([T('Off duty, on your side. ', 'white'), T('Not a fighter - he can\'t be hurt - but a salesman. While he\'s close:', 'gray')]),
                     P28.body([T('Gift of the Gab', GOLD, bold=True), T(' villagers trade cheaper and toss you gifts.  ', 'gray'),
                               T('A Lucky Flipper', '#7ad06a', bold=True), T(' Luck.  ', 'gray'), T('Penguin Stroke', PEARL, bold=True),
                               T(' you swim like him.  ', 'gray'), T('Appraisal', '#e8b04a', bold=True), T(' 1 trade in 5 with a villager near him: an emerald back.', 'gray')], 300)],
                    [P28.btn(T('Wait here / follow me', 'white', bold=True), 8301, tooltip=T('He waits on the spot - or waddles after you again.', 'gray'), width=150),
                     P28.btn(T('Send him home', 'gray'), 8309, width=150), P28.btn(T('Wardrobe', PEARL, bold=True), 8302, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray')),
                     P28.btn(T('Seasons', '#d8803a', bold=True), 8303, width=150, tooltip=T('His earth gem takes on the season of the land - pick how he wears it.', 'gray'))], columns=2, exit_label='Close')
    fn('p128/pm/menu', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 8301..8309 run return run function bm:p128/pm/act')
    fn('p128/pm/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                       'execute if score #act bm.pay matches 8302 run return run function bm:p119/plain/pearl',      # (2.78: his wardrobe)
                       'execute if score #act bm.pay matches 8303 run return run function bm:p209/menu',             # (2.93d: his seasons)
                       'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.pmsel2',
                       'execute unless entity @e[type=minecraft:cat,tag=bm.pmsel2] run return run function bm:p28/stale',
                       'execute if score #act bm.pay matches 8301 run function bm:p128/pm/sit',
                       'execute if score #act bm.pay matches 8309 run function bm:p128/pm/dismiss',
                       'tag @e[tag=bm.pmsel2] remove bm.pmsel2'])
    fn('p128/pm/sit', ['execute as @e[type=minecraft:cat,tag=bm.pmsel2] store success score #s bm.rng if data entity @s {Sitting:1b}',
                       'execute if score #s bm.rng matches 1 run data modify entity @e[type=minecraft:cat,tag=bm.pmsel2,limit=1] Sitting set value 0b',
                       'execute if score #s bm.rng matches 0 run data modify entity @e[type=minecraft:cat,tag=bm.pmsel2,limit=1] Sitting set value 1b',
                       'execute if score #s bm.rng matches 1 run ' + pmsay('"Onward! Lead the way."'),
                       'execute if score #s bm.rng matches 0 run ' + pmsay('"Pearlman shall mind the shop. Right here. Don\'t be long."')])
    fn('p128/pm/dismiss', ['execute as @e[type=minecraft:cat,tag=bm.pmsel2] at @s run function bm:p128/pm/go', pmsay('"Toodle-oo! Call if you need an appraisal."')])
    # going home (as the cat, at it): a puff of snow, his model with him
    fn('p128/pm/go', ['scoreboard players add #gone bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      'execute as @e[type=minecraft:item_display,tag=bm.pmd] if score @s bm.pid = #me bm.pid run kill @s',
                      'particle minecraft:snowflake ~ ~0.8 ~ 0.4 0.6 0.4 0.02 30', 'particle minecraft:poof ~ ~0.6 ~ 0.3 0.4 0.3 0.02 12',
                      'playsound minecraft:block.note_block.bell neutral @a[distance=..16] ~ ~ ~ 0.8 1.2',
                      'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:cat,tag=bm.pmpet] if score @s bm.pid = #me bm.pid at @s run function bm:p128/pm/go')
    P73.follow_rules(G, ('pearl', 'cat', 'bm.pmpet', 'pearl_card', 'p128/pm/go', 'Pearlman', 'bm.fgp', 'p128/pm/summon_here'), second)
    # every tick: his model where his cat is (or a new one, if it was lost)
    tick.append('execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/tick')
    fn('p128/pm/tick', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #ok bm.rng 0',
                        'execute rotated as @s rotated ~ 0 as @e[type=minecraft:item_display,tag=bm.pmd] if score @s bm.pid = #me bm.pid store success score #ok bm.rng run tp @s ~ ~ ~ ~ 0',
                        f'execute if score #ok bm.rng matches 0 run summon minecraft:item_display ~ ~ ~ {snbt(pdisp)}',
                        'execute if score #ok bm.rng matches 0 run scoreboard players operation @e[type=minecraft:item_display,tag=bm.pmnew,distance=..1] bm.pid = #me bm.pid',
                        'execute if score #ok bm.rng matches 0 run tag @e[type=minecraft:item_display,tag=bm.pmnew,distance=..1] remove bm.pmnew'])
    # (a model whose cat is gone goes too)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.pmd] at @s run function bm:p128/pm/orphan')
    fn('p128/pm/orphan', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run return 0', 'kill @s'])
    # every 5 ticks: a waddle when he walks, a little sway at rest, settled down when he sits
    fast.append('execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/anim')
    q = lambda ax, s: {'x': f'[{s:.3f}f,0f,0f,{(1 - s * s) ** 0.5:.4f}f]', 'z': f'[0f,0f,{s:.3f}f,{(1 - s * s) ** 0.5:.4f}f]'}[ax]
    pose = lambda rot, ty, d=5: f'data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{left_rotation:{rot},translation:[0f,{ty:.3f}f,0f]}}}}'
    fn('p128/pm/anim', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players add @s bm.pmw 1',
                        'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                        'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng', 'scoreboard players operation #vx bm.rng += #vz bm.rng',
                        'scoreboard players operation #w bm.rng = @s bm.pmw', 'scoreboard players operation #w bm.rng %= #2 bm.rng',
                        'scoreboard players set #pm bm.rng 0', 'execute if score #vx bm.rng matches 300.. run scoreboard players set #pm bm.rng 1',
                        'execute if data entity @s {Sitting:1b} run scoreboard players set #pm bm.rng 2',
                        'execute as @e[type=minecraft:item_display,tag=bm.pmd,distance=..8] if score @s bm.pid = #me bm.pid run function bm:p128/pm/pose'])
    fn('p128/pm/pose', [f'execute if score #pm bm.rng matches 1 if score #w bm.rng matches 0 run {pose(q("z", 0.07), PS / 2 + 0.04)}',
                        f'execute if score #pm bm.rng matches 1 if score #w bm.rng matches 1 run {pose(q("z", -0.07), PS / 2)}',
                        f'execute if score #pm bm.rng matches 0 if score #w bm.rng matches 0 run {pose(q("z", 0.015), PS / 2, 10)}',
                        f'execute if score #pm bm.rng matches 0 if score #w bm.rng matches 1 run {pose(q("z", -0.015), PS / 2, 10)}',
                        f'execute if score #pm bm.rng matches 2 run {pose(q("x", -0.09), PS / 2 - 0.1, 8)}'])
    # every second, near his owner: the perks - and now and then, a word
    second.append('execute as @e[type=minecraft:cat,tag=bm.pmpet] at @s run function bm:p128/pm/sec')
    fn('p128/pm/sec', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @a[distance=..16,gamemode=!spectator] if score @s bm.pid = #me bm.pid at @s run function bm:p128/pm/perks',
                       'scoreboard players add @s bm.pmq 1', 'execute if score @s bm.pmq matches 120.. run function bm:p128/pm/quip'])
    fn('p128/pm/perks', ['effect give @s minecraft:luck 4 0 true',
                         f'execute unless dimension bm:gutter unless entity @e[type=minecraft:villager,tag=bm.npc,distance=..{NPC_R}] '
                         f'unless entity @e[type=minecraft:interaction,tag=bm.pmst,distance=..{STATUE_R}] run function bm:p128/hero1',
                         'execute if block ~ ~ ~ minecraft:water run effect give @s minecraft:dolphins_grace 4 0 true'])
    fn('p128/hero1', ['effect give @s minecraft:hero_of_the_village 4 0 true', 'tag @s add bm.pmhero'])
    LINES = ['"A tip, friend: villagers adore a firm flipper-shake."', '"That emerald price? Robbery. Haggle!"', '"Ah, the open road. Pearlman\'s office."',
             '"Did I ever tell you about the iceberg? ...Another time."', '"Business is booming. My feet, less so."', '"Nine gems, one heart of gold. That\'s you, that is."',
             '"Mind the briefcase - it bites. Metaphorically."', '"Swim with me! It\'s all in the hips."']
    fn('p128/pm/quip', ['scoreboard players set @s bm.pmq 0', 'execute store result score #r bm.rng run random value 0..%d' % (len(LINES) - 1)] +
       [f'execute if score #r bm.rng matches {i} as @a[distance=..16,tag=!bm.hush] if score @s bm.pid = #me bm.pid run ' + pmsay(ln) for i, ln in enumerate(LINES)] +
       ['playsound minecraft:entity.parrot.ambient neutral @a[distance=..12] ~ ~ ~ 0.5 0.7'])
    # APPRAISAL: a trade with a villager near him - 1 in 5, an emerald back
    wjson('bm/advancement/p128/vtrade.json', {'criteria': {'t': {'trigger': 'minecraft:villager_trade', 'conditions': {
        'villager': [{'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                  'predicate': {'minecraft:nbt': '{Tags:["bm.npc"]}'}}}]}}},
        'rewards': {'function': 'bm:p128/pm/appraise'}})
    fn('p128/pm/appraise', ['advancement revoke @s only bm:p128/vtrade', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute unless entity @e[type=minecraft:cat,tag=bm.pmpet,distance=..12] run return 0',
                            'scoreboard players set #ok bm.rng 0', f'{sel_pet.replace("tag=bm.pmpet]", "tag=bm.pmpet,distance=..12]")} run scoreboard players set #ok bm.rng 1',
                            'execute if score #ok bm.rng matches 0 run return 0',
                            'execute store result score #r bm.rng run random value 1..5', 'execute unless score #r bm.rng matches 1 run return 0',
                            'give @s minecraft:emerald 1', 'playsound minecraft:entity.villager.yes player @s ~ ~ ~ 0.8 1.2',
                            pmsay('"Ahem - I believe you overcharged my friend." (An emerald comes back.)')])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the statue (Pearlman in gold), the icons
def textures():
    from PIL import Image
    from gen_rp import hexc
    import random
    rnd = random.Random(128)
    def gold(base, var=10, glint=None):
        im = Image.new('RGBA', (16, 16)); b = hexc(base)[:3]
        for y in range(16):
            for x in range(16):
                d = rnd.randint(-var, var) + (18 if (x + y) % 9 == 0 else 0)
                im.putpixel((x, y), tuple(max(0, min(255, v + d)) for v in b) + (255,))
        if glint:
            for i in range(4):
                im.putpixel((2 + i, 2 + i), hexc(glint)[:3] + (255,))
        return im
    return {'pmg_dark': gold('#9a6e14', 8), 'pmg_mid': gold('#d8a42a', 10), 'pmg_light': gold('#ffe070', 10, '#fff8d0'), 'pmg_eye': gold('#5a400c', 4),
            'pmg_gem': gold('#c8203a', 12, '#ff9aa8'), 'pmg_base': gold('#2a2a30', 6)}


def rp(R):
    R.TEXTURE_MODS.append(__import__('sys').modules[__name__])
    R.ICONS['pearl_statue'] = R.grid(['................', '......kkkk......', '......kyyk......', '.....kkkkkk.....', '......kyyk......', '.....kyWWyk.....',
                                      '.....kyWWyk..k..', '....kyyyyyykyk..', '....kyyyyyyk.k..', '....kyyyyyyk....', '.....kyyyyk.....', '.....kkkkkk.....',
                                      '....kddddddk....', '...kddddddddk...', '...kkkkkkkkkk...', '................'],
                                     dict(k='#5a400c', y='#e8b830', W='#fff4c0', d='#3a3a40'))
    R.ICONS['pearl_card'] = R.grid(['................', '................', '.kkkkkkkkkkkkkk.', '.kwwwwwwwwwwwwk.', '.kwggggggggggwk.', '.kwgbbwwwwwwgwk.',
                                    '.kwgbBbwkkkkgwk.', '.kwgbbwwwwwwgwk.', '.kwgwwwwkkkwgwk.', '.kwgwwwwwwwwgwk.', '.kwggggggggggwk.', '.kwwwwwwwwwwwwk.',
                                    '.kkkkkkkkkkkkkk.', '................', '................', '................'],
                                   dict(k='#2a3a4a', w='#f4f4f0', g='#e0c060', b='#1a1a24', B='#5ac8ff'))
    import json, os
    def post(R2):
        src = R2.p('assets', 'bm', 'models', 'item', 'pearlman.json')
        m = json.load(open(src))
        TEX = {'k': 'pmg_dark', 'w': 'pmg_light', 'o': 'pmg_mid', 'y': 'pmg_mid', 'b': 'pmg_mid', 'd': 'pmg_dark', 'g': 'pmg_light', 'e': 'pmg_eye',
               't': 'pmg_light', 'c': 'pmg_mid', 'r': 'pmg_gem', 'H': 'pmg_dark'}
        tex = {k: f'bm:block/{v}' for k, v in TEX.items() if k in m['textures']}
        tex['base'] = 'bm:block/pmg_base'; tex['rim'] = 'bm:block/pmg_light'; tex['particle'] = 'bm:block/pmg_light'
        S, LIFT = 0.88, 3.0                               # Pearlman shrunk a touch, stood on a plinth
        els = []
        for e in copy.deepcopy(m['elements']):
            sc = lambda p: [round((p[0] - 8) * S + 8, 4), round(p[1] * S + LIFT, 4), round((p[2] - 8) * S + 8, 4)]
            e['from'], e['to'] = sc(e['from']), sc(e['to'])
            if 'rotation' in e: e['rotation']['origin'] = sc(e['rotation']['origin'])
            els.append(e)
        cube = lambda fr, to, t: {'from': list(fr), 'to': list(to), 'faces': {f: {'uv': [0, 0, 16, 16], 'texture': f'#{t}'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}
        els = [cube((0.5, 0, 0.5), (15.5, 2.2, 15.5), 'base'), cube((1.5, 2.2, 1.5), (14.5, 3, 14.5), 'rim')] + els
        R2.wj('assets/bm/models/item/pearlman_gold.json', {'textures': tex, 'elements': els, 'display': m.get('display', {})})
        R2.wj('assets/bm/items/pearlman_gold.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/pearlman_gold'}})
    R.POST.append(post)
