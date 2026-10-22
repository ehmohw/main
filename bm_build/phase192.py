"""2.87: THE BONDS OF THE DEEP - pairs and trios for Queen Ava, Queen Pearl and Bloo (phase188's engine runs the pairs;
phase100 finds the trios and calls p100/<key>, built here).

TRIOS
- EMMA, AVA AND PEARL, "THE ROYAL FAMILY" - the kingdom's whole house, together again:
    Resistance II, Regeneration II, Strength, four more hearts, Conduit Power and Dolphin's Grace for you; the three tougher.
    THE ETHEREAL ECHO: every 15 s what's left of the gem answers its family - every foe within 12 takes 6 and glows, and
    the light heals you and the three.
    THE BLOODLINE WARD: once every 5 minutes, when you drop to 2 hearts or less, the crowns of the deep refuse to let you fall:
    you're healed in full, Resistance IV and Fire Resistance for 8 s, and every foe within 10 is thrown back (12).
- LEO, EMMA AND AVA, "THE QUEEN'S OATH" - the knight who carried the princess out the night her mother fell:
    Strength II and Resistance II for you; an Absorption IV shield every 20 s; every 8 s Leo's shield-bash throws back
    every foe within 6 (5); Leo and Emma tougher, Ava's ward on Emma.
- LEO, EMMA AND PEARL, "THE REGENT'S COURT": Strength, Speed II, Haste II and Luck II; every 30 s TWO of Pearl's whims at
    once (Speed, Jump Boost, Night Vision, Fire Resistance, Dolphin's Grace, Slow Falling); Leo tougher.
- DEMOCRATUS, CECIL AND BLOO, "THE OLD WAR" - the three who were there a thousand years ago:
    Strength II and Resistance; every 12 s lightning finds the foes round you; Bloo's Frenzy never fades.
PAIRS
- EMMA + AVA, "Mother and Daughter": Regeneration II and Resistance; both heal.
- AVA + PEARL, "Sisters of the Tide": Water Breathing, Dolphin's Grace and Conduit Power; underwater, Strength II.
- EMMA + PEARL, "The Fun Aunt": Speed, Jump Boost II and Luck.
- AVA + APOPHISS, "Unfinished Business": Strength II for you; the foes round you wither - she has not forgiven him.
- AVA + TULLIUS, "The Queen's Captain": Water Breathing and Resistance; Tullius tougher.
- PEARL + PEARLMAN, "Pearls of Great Price": Luck II and Hero of the Village.
- BLOO + DEMOCRATUS, "Old Wounds": Strength II for you; the foes round you weakened - Bloo is furious, and fights like it.
- BLOO + LEO, "The Old Alliance": Strength and Resistance; both tougher.
- BLOO + ASHUR, "Wildfire": Fire Resistance and Strength; the foes round you catch fire."""
from items import T
import phase100 as P100
import phase188 as P188

FOE = 'type=#bm:hostile,tag=!bm.npc'
O = P188.O
REGEN = P188.REGEN
P188.VNAME.update({'ava': 'Queen Ava', 'pearlq': 'Queen Pearl', 'bloo': 'Bloo', 'pearl': 'Pearlman', 'tul': 'Tullius', 'cecil': 'Cecil', 'stalker': 'The Stalker', 'lantern': 'The Arachno-Lantern', 'bender': 'Bender', 'bones': 'Bones'})
REGEN2 = 'effect give @s minecraft:regeneration 3 1 true'

P188.PAIRS.update({
    'mother': ('ava', 'emma', 'Mother and Daughter', '#6ad8e8', 'Queen Ava and Emma, together again',
               [f'effect give {O} minecraft:regeneration 3 1 true', f'effect give {O} minecraft:resistance 3 0 true', REGEN, '{B} run ' + REGEN],
               [('Emma', 'Mama! Mama, look - I have friends now!'), ('ava', 'I see them, my darling. I see all of you. I am so proud.')],
               [('Emma', 'Mama, do you remember the song about the seahorse?', 'ava', 'Every word. Shall we sing it?'),
                ('ava', 'You have your father\'s stubbornness, Emma.', 'Emma', 'Aunt Pearl says I have YOURS.')]),
    'sisters': ('ava', 'pearlq', 'Sisters of the Tide', '#5ad8e0', 'Queen Ava and Queen Pearl - two sisters, one sea',
                [f'effect give {O} minecraft:water_breathing 12 0 true', f'effect give {O} minecraft:dolphins_grace 3 0 true',
                 f'effect give {O} minecraft:conduit_power 12 0 true',
                 f'execute as {O} at @s if block ~ ~1 ~ minecraft:water run effect give @s minecraft:strength 3 1 true'],
                [('pearlq', 'Ava! You look... see-through. Very fashionable.'), ('ava', 'And you look like a queen, little sister. Finally.')],
                [('pearlq', 'Remember when we hid in the kelp and Father couldn\'t find us for a whole day?', 'ava', 'I remember being grounded for a month.'),
                 ('ava', 'You are a good queen, Pearl.', 'pearlq', 'Don\'t. You\'ll make me cry and my mascara will run. Underwater.')]),
    'aunt': ('pearlq', 'emma', 'The Fun Aunt', '#ffb0e8', 'Queen Pearl and Emma - trouble, times two',
             [f'effect give {O} minecraft:speed 3 0 true', f'effect give {O} minecraft:jump_boost 3 1 true', f'effect give {O} minecraft:luck 3 0 true'],
             [('Emma', 'Aunt Pearl! Did you bring cake?'), ('pearlq', 'Did I bring cake. DID I BRING CAKE. Darling, I AM cake.')],
             [('pearlq', 'Don\'t tell the council, but I gave the royal seahorses the day off.', 'Emma', 'Again?!'),
              ('Emma', 'When I\'m queen, can I still have fun?', 'pearlq', 'When you\'re queen you can make fun the LAW.')]),
    'unfinished': ('ava', 'apo', 'Unfinished Business', '#3ad0a0', 'Queen Ava and Apophiss - the queen and the serpent who killed her',
                   [f'effect give {O} minecraft:strength 3 1 true', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:wither 3 0'],
                   [('ava', 'You.'), ('apo', 'Hsss... the queen of the deep. I thought the sea had kept you.')],
                   [('apo', 'I did what I had to, queen. My people were starving.', 'ava', 'And mine were not people to you?'),
                    ('ava', 'If you so much as look at my daughter, serpent...', 'apo', '...I know. You would hold the door again.')]),
    'captain': ('ava', 'tul', 'The Queen\'s Captain', '#7ad8ff', 'Queen Ava and Tullius - the queen and the captain of her guard',
                [f'effect give {O} minecraft:water_breathing 12 0 true', f'effect give {O} minecraft:resistance 3 0 true', '{B} run effect give @s minecraft:resistance 3 0 true'],
                [('tul', 'Your Majesty. I... went down with the ship.'), ('ava', 'You did your duty, Tullius. Now do it again - for them.')],
                [('tul', 'Leo got the princess out. I got the cold.', 'ava', 'And I got the door. We each held something.'),
                 ('ava', 'Still sardonic, Captain?', 'tul', 'Death does not improve a man\'s manners, Majesty.')]),
    'pearls': ('pearlq', 'pearl', 'Pearls of Great Price', '#5ac8ff', 'Queen Pearl and Pearlman - a queen and her favourite merchant',
               [f'effect give {O} minecraft:luck 3 1 true', f'effect give {O} minecraft:hero_of_the_village 3 0 true'],
               [('pearl', 'Your MAJESTY! Pearlman is HONOURED! A queen named for pearls!'), ('pearlq', 'And a penguin named for them too! We should start a club.')],
               [('pearlq', 'Pearlman, darling, how much for the shiny one?', 'pearl', 'For you, Majesty? ...Still full price. Pearlman has principles.'),
                ('pearl', 'Royal Purveyor of Fine Goods to Queen Pearl!', 'pearlq', 'Fine, fine - but I want a discount on cake.')]),
    'wounds': ('bloo', 'demo', 'Old Wounds', '#5a8ae8', 'Bloo and Democratus - the beast and the man who took everything from him',
               [f'effect give {O} minecraft:strength 3 1 true', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:weakness 3 0'],
               [('bloo', 'YOU. Scythe-man. I have waited a thousand years.'), ('demo', 'I remember your woods. I remember what I did. I will not ask you to forgive it.')],
               [('bloo', 'One wrong move, scythe-man.', 'demo', 'I know, beast. I would think less of you otherwise.'),
                ('demo', 'I wanted to save the people, Bloo. I became the thing they needed saving from.', 'bloo', '...Hrrn. Fight, then. Talk less.')]),
    'alliance': ('bloo', 'leo', 'The Old Alliance', '#5ab8e0', 'Bloo and Leo - the woods and the kingdom, side by side again',
                 [f'effect give {O} minecraft:strength 3 0 true', f'effect give {O} minecraft:resistance 3 0 true',
                  'effect give @s minecraft:resistance 3 0 true', '{B} run effect give @s minecraft:resistance 3 0 true'],
                 [('Leo', 'The blue beast of the old songs... You fought beside my forefathers.'), ('bloo', 'Your forefathers were loud and smelled of tin. So do you.')],
                 [('Leo', 'Shoulder to shoulder, Bloo.', 'bloo', 'Shoulder to... elbow. You are short, knight.'),
                  ('bloo', 'You fight well. For a human.', 'Leo', 'From you, Bloo, I will take that as high praise.')]),
    'wildfire': ('bloo', 'ashur', 'Wildfire', '#ff8a4a', 'Bloo and Ashur - claws and flame, and no mercy in either',
                 [f'effect give {O} minecraft:fire_resistance 12 0 true', f'effect give {O} minecraft:strength 3 0 true',
                  f'execute at @s as @e[{FOE},distance=..8] run data merge entity @s {{Fire:60s}}'],
                 [('ashur', 'Ooh, a big angry kitty! Can I ride you?'), ('bloo', 'Touch me and I will eat your tiara.')],
                 [('ashur', 'Race you to the next monster!', 'bloo', 'Hrrn. You will lose.'),
                  ('bloo', 'Keep your fire off my fur.', 'ashur', 'No promises, fluffy.')]),
    # (2.87: the hidden hard-mode pair - the Stalker and the Arachno-Lantern - and their own)
    'longdark': ('stalker', 'omega', 'The Long Dark', '#a8ac70', 'The Stalker and King Omega - the hunter of the night and the king of the dead',
                 [f'effect give {O} minecraft:night_vision 15 0 true', f'effect give {O} minecraft:resistance 3 0 true',
                  f'execute at @s as @e[{FOE},distance=..8] run effect give @s minecraft:slowness 3 1'],
                 [('omega', 'One of the night-things! Good evening, friend. Do sit - oh. You do not sit. You loom.'), ('stalker', '(it bows - all the way down, joint by joint)')],
                 [('omega', 'In my kingdom we had a word for things like you: "Sir".', 'stalker', '(its head tilts, pleased)'),
                  ('stalker', '(it stands beside the King, very still, and the dark leans in to listen)', 'omega', 'Yes, yes. I miss the dark too.')]),
    'hearth': ('lantern', 'ashur', 'Hearth and Ember', '#ff8a2a', 'The Arachno-Lantern and Ashur - fire on eight legs, and fire in a dress',
               [f'effect give {O} minecraft:fire_resistance 15 0 true', f'effect give {O} minecraft:strength 3 0 true',
                f'execute at @s as @e[{FOE},distance=..8] run data merge entity @s {{Fire:80s}}'],
               [('ashur', 'A PUMPKIN! On LEGS! And it\'s ON FIRE! You\'re my new favourite thing!'), ('lantern', '(its fires roar up, delighted)')],
               [('ashur', 'Can I ride you? Pleeease?', 'lantern', '(it crouches low - then stands back up the moment she tries)'),
                ('lantern', '(it puffs a ring of embers at her)', 'ashur', 'Rude! ...Do it again.')]),
    'nightmares': ('stalker', 'lantern', 'Things in the Night', '#c84a2a', 'The Stalker and the Arachno-Lantern - two things that should not follow anyone',
                   [f'effect give {O} minecraft:night_vision 15 0 true', f'effect give {O} minecraft:speed 3 0 true',
                    f'execute at @s as @e[{FOE},distance=..10] run effect give @s minecraft:glowing 3 0'],
                   [('lantern', '(it scuttles behind you, away from the Stalker)'), ('stalker', '(it looks at the pumpkin for a long time. The pumpkin looks back.)')],
                   [('stalker', '(it holds a claw over the Lantern\'s fire - and draws it back, singed)', 'lantern', '(a puff of smug embers)'),
                    ('lantern', '(it lights the dark ahead of you)', 'stalker', '(it steps back into the dark it just lost)')]),
    # (2.88: Bender and Bones, and their own)
    'bigscary': ('bones', 'emma', 'Who\'s My Big Scary Boy?', '#8ab0c8', 'Bones and Emma - a princess and her shark',
                 [f'effect give {O} minecraft:dolphins_grace 15 0 true', f'effect give {O} minecraft:water_breathing 15 0 true',
                  f'execute as {O} if predicate bm:swim run effect give @s minecraft:strength 3 1 true',
                  f'execute at @s as @e[{FOE},distance=..8] run effect give @s minecraft:slowness 3 1'],
                 [('emma', 'BONES! Who\'s my big scary boy? YOU are!'), ('bones', '(he rolls belly-up in his bubble, every tooth showing)')],
                 [('emma', 'He used to sleep at the foot of my bed. In a fish tank. A very big fish tank.', 'bones', '(a proud blub)'),
                  ('bones', '(he circles her, twice, and glares at everything else)', 'emma', 'He\'s very protective. It\'s very sweet. It\'s a LOT of teeth.')]),
    'diggers': ('bender', 'dennis', 'Digging Buddies', '#e0a860', 'Bender and Dennis - two noses for what\'s under the ground',
                [f'effect give {O} minecraft:haste 15 1 true', f'effect give {O} minecraft:luck 15 1 true'],
                [('dennis', 'Now THERE\'S a lad who knows what ground\'s for! Dig, boy!'), ('bender', '(he digs. Enthusiastically. At Dennis\'s boots.)')],
                [('dennis', 'Found a bone. Gave it to him. He buried it. Then dug it up again. Respect.', 'bender', '(tail going like mad)'),
                 ('bender', '(he drops a muddy rock at the dwarf\'s feet)', 'dennis', 'Granite! Lovely bit o\' granite. Good lad.')]),
    'landsea': ('bender', 'bones', 'Land and Sea', '#a8c8a0', 'Bender and Bones - the goodest boy and the scariest one',
                [f'effect give {O} minecraft:speed 3 0 true', f'effect give {O} minecraft:dolphins_grace 15 0 true',
                 f'execute at @s as @e[{FOE},distance=..8] run effect give @s minecraft:weakness 3 0'],
                [('bender', '(he barks at the shark in the bubble. The shark grins at him. He barks again, delighted.)'), ('bones', '(a curious blub)')],
                [('bender', '(he tries to lick the bubble)', 'bones', '(he bumps it from the inside, nose to nose)'),
                 ('bones', '(he snaps at Bender\'s tail - gently - and misses on purpose)', 'bender', '(play bow!)')]),
})
P188.ICON.update({k: 'bm:av_locket' for k in ('mother', 'sisters', 'unfinished', 'captain')})
P188.ICON.update({k: 'bm:pq_pearls' for k in ('aunt', 'pearls')})
P188.ICON.update({k: 'bm:bo_claw' for k in ('wounds', 'alliance', 'wildfire')})
P188.ICON.update({'longdark': 'bm:st_hook', 'hearth': 'bm:ln_gourd', 'nightmares': 'bm:st_hook'})
P188.ICON.update({'bigscary': 'bm:bn_whistle', 'diggers': 'bm:bv_ball', 'landsea': 'bm:bv_ball'})

TRIOS = {
    'royal': ('The Royal Family', '#ffd86a', ('emma', 'ava', 'pearlq'), 'The Royal Family', 'Walk with Emma, Queen Ava and Queen Pearl at once'),
    'oath': ("The Queen's Oath", '#8ad8ff', ('leo', 'emma', 'ava'), "The Queen's Oath", 'Walk with Leo, Emma and Queen Ava at once'),
    'regency': ("The Regent's Court", '#7ae8d8', ('leo', 'emma', 'pearlq'), "The Regent's Court", 'Walk with Leo, Emma and Queen Pearl at once'),
    'oldwar': ('The Old War', '#7a9ae8', ('demo', 'cecil', 'bloo'), 'The Old War', 'Walk with Democratus, Cecil and Bloo at once'),
}
ICON = {'royal': 'bm:av_locket', 'oath': 'bm:leo_crest', 'regency': 'bm:pq_pearls', 'oldwar': 'bm:bo_claw'}
P100.TRIOS.update(TRIOS)
P100.BANTER.update({
    'royal': [('Emma', 'Mama AND Aunt Pearl! This is the best day EVER!', 'Queen Pearl', 'Group hug! Ava, you\'re see-through, it\'s fine, hug anyway!'),
              ('Queen Ava', 'Three queens of the deep. Well - two, and one to be.', 'Emma', 'And I\'ll be the best one! No offence.'),
              ('Queen Pearl', 'Should we tell the council we\'re all out adventuring?', 'Queen Ava', 'Absolutely not.')],
    'oath': [('Queen Ava', 'Sir Leo. You carried her out. I never got to thank you.', 'Leo', 'You held the door, Majesty. I only ran.'),
             ('Leo', 'I swore an oath that night, Princess. I keep it still.', 'Emma', 'I know, Leo. You\'re the best knight ever.'),
             ('Emma', 'Mama, Leo checks under my bed for serpents every night.', 'Queen Ava', 'Good. Keep doing that, Sir Leo.')],
    'regency': [('Queen Pearl', 'Leo, darling, be a dear and stab that thing for me?', 'Leo', 'With pleasure, Your Majesty.'),
                ('Emma', 'Aunt Pearl, Leo says you skipped council again.', 'Queen Pearl', 'Leo is a TATTLETALE.'),
                ('Leo', 'Majesty, perhaps the crown should not be worn sideways.', 'Queen Pearl', 'It\'s called FASHION, Leo.')],
    'oldwar': [('Bloo', 'The three of us. Like the old days. I still hate you both.', 'Cecil', 'Lovely to see you too, Bloo.'),
               ('Democratus', 'Cecil. You stood with me, at the start.', 'Cecil', 'And I walked away at the end. We both carry that.'),
               ('Cecil', 'Do you ever regret the curse on Omega\'s island?', 'Bloo', 'Hrrn. Regret is for those who did not survive.')],
})


def extend_offers(O_, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.royw dummy', 'scoreboard objectives add bm.p192 dummy']
    G.OBJECTIVES += ['bm.royw', 'bm.p192']
    G.FUNCS['loop/second'][-1:-1] = ['scoreboard players remove @a[scores={bm.royw=1..}] bm.royw 1']
    host = lambda k: P100.WHO[k]
    mine = lambda k: f'@e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..24]'

    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    hb2 = 'execute unless predicate bm:p100/hb run effect give @s minecraft:health_boost 15 1 true'
    tick = lambda n: ['scoreboard players add @s bm.p192 1', f'execute if score @s bm.p192 matches {n}.. run scoreboard players set @s bm.p192 0']
    # ---- THE ROYAL FAMILY
    fn('p100/royal', ['effect give @s minecraft:resistance 3 1 true', REGEN2, 'effect give @s minecraft:strength 3 0 true', hb2,
                      'effect give @s minecraft:conduit_power 12 0 true', 'effect give @s minecraft:dolphins_grace 3 0 true'] + tick(15) +
       ['execute if score @s bm.p192 matches 0 run function bm:p192/echo',
        'execute unless score @s bm.royw matches 1.. store result score #hp bm.rng run data get entity @s Health',
        'execute unless score @s bm.royw matches 1.. if score #hp bm.rng matches ..4 run function bm:p192/ward'] +
       each(TRIOS['royal'][2], 'effect give @s minecraft:resistance 3 1 true') + each(TRIOS['royal'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p192/echo', ['particle minecraft:end_rod ~ ~1.2 ~ 4 1 4 0.05 40', 'particle minecraft:flame ~ ~1 ~ 3 0.6 3 0.02 12',
                     'particle minecraft:snowflake ~ ~1 ~ 3 0.6 3 0.02 12', 'particle minecraft:electric_spark ~ ~1 ~ 3 0.6 3 0.2 12',
                     'particle minecraft:bubble_pop ~ ~1 ~ 3 0.6 3 0.05 16', 'particle minecraft:happy_villager ~ ~1 ~ 3 0.6 3 0 12',
                     'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.7 1.6',
                     'playsound minecraft:block.amethyst_block.resonate player @a[distance=..16] ~ ~ ~ 1 0.8',
                     f'execute as @e[{FOE},distance=..12] run damage @s 6 minecraft:magic',
                     f'effect give @e[{FOE},distance=..12] minecraft:glowing 5 0',
                     'effect give @s minecraft:instant_health 1 0 true'] + each(TRIOS['royal'][2], 'effect give @s minecraft:instant_health 1 0 true'))
    fn('p192/ward', ['scoreboard players set @s bm.royw 300', 'effect give @s minecraft:instant_health 1 4 true', 'effect give @s minecraft:resistance 8 3 true',
                     'effect give @s minecraft:fire_resistance 8 0 true',
                     'particle minecraft:totem_of_undying ~ ~1 ~ 0.6 1 0.6 0.5 80', 'particle minecraft:end_rod ~ ~1 ~ 2 1 2 0.2 60',
                     'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 1 1.2',
                     f'execute as @e[{FOE},distance=..10] run damage @s 12 minecraft:magic',
                     f'execute as @e[{FOE},distance=..10] at @s facing entity @p feet run tp @s ^ ^0.4 ^-3',
                     tellraw('@s', [T('The Bloodline Ward! ', '#ffd86a', bold=True), T('Three crowns of the deep refuse to let you fall. ', 'gray'),
                                    T('(Again in 5 minutes.)', 'dark_gray')])])
    # ---- THE QUEEN'S OATH
    fn('p100/oath', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:resistance 3 1 true'] + tick(40) +
       ['execute if score @s bm.p192 matches 0 run effect give @s minecraft:absorption 20 3 true',
        'execute if score @s bm.p192 matches 0 run particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.2 16',
        'execute if score @s bm.p192 matches 8 run function bm:p192/bash', 'execute if score @s bm.p192 matches 16 run function bm:p192/bash',
        'execute if score @s bm.p192 matches 24 run function bm:p192/bash', 'execute if score @s bm.p192 matches 32 run function bm:p192/bash'] +
       each(('leo', 'emma'), 'effect give @s minecraft:resistance 3 1 true') + each(('emma',), 'effect give @s minecraft:absorption 5 1 true') +
       ['function bm:p100/banter_tick'])
    fn('p192/bash', [f'execute at {mine("leo")} as @e[{FOE},distance=..6] run damage @s 5 minecraft:player_attack',
                     f'execute as {mine("leo")} at @s as @e[{FOE},distance=..6] at @s facing entity @p feet run tp @s ^ ^0.3 ^-2',
                     f'execute at {mine("leo")} run particle minecraft:sweep_attack ~ ~1 ~ 1.5 0.3 1.5 0 6',
                     f'execute at {mine("leo")} run playsound minecraft:item.shield.block player @a[distance=..16] ~ ~ ~ 1 0.8'])
    # ---- THE REGENT'S COURT
    whims = [('speed', 0), ('jump_boost', 1), ('night_vision', 0), ('fire_resistance', 0), ('dolphins_grace', 0), ('slow_falling', 0)]
    fn('p100/regency', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:speed 3 1 true', 'effect give @s minecraft:haste 3 1 true',
                        'effect give @s minecraft:luck 3 1 true'] + tick(30) + ['execute if score @s bm.p192 matches 0 run function bm:p192/whims'] +
       each(('leo',), 'effect give @s minecraft:resistance 3 1 true') + ['function bm:p100/banter_tick'])
    w = ['particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.04 20', 'playsound minecraft:entity.dolphin.play player @s ~ ~ ~ 0.8 1.4']
    for slot in ('a', 'b'):
        w.append(f'execute store result score #{slot} bm.rng run random value 0..{len(whims) - 1}')
        w += [f'execute if score #{slot} bm.rng matches {i} run effect give @s minecraft:{e} 30 {amp} true' for i, (e, amp) in enumerate(whims)]
    fn('p192/whims', w + [title('@s', 'actionbar', [T('Queen Pearl: ', '#5ae0d8', bold=True), T('Two whims, darling - one for each of you lovely knights!', '#d8fffa')])])
    # ---- THE OLD WAR
    fn('p100/oldwar', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:resistance 3 0 true'] + tick(12) +
       ['execute if score @s bm.p192 matches 0 run function bm:p192/storm'] +
       each(('bloo',), 'scoreboard players set @s bm.bkk2 80') + ['function bm:p100/banter_tick'])
    fn('p192/storm', [f'execute as @e[{FOE},distance=..12,sort=random,limit=3] at @s run function bm:p192/bolt'])     # (a bolt of their own - no fire, nothing else struck)
    fn('p192/bolt', ['particle minecraft:electric_spark ~ ~1 ~ 0.2 1.5 0.2 0.3 30', 'particle minecraft:flash{color:[0.7,0.8,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                     'particle minecraft:end_rod ~ ~3 ~ 0.05 2 0.05 0 20', 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..32] ~ ~ ~ 0.6 1.4',
                     'damage @s 6 minecraft:lightning_bolt'])
    for k, (nm, col, mem, at, desc) in TRIOS.items():
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': ICON[k]}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'challenge' if k == 'royal' else 'goal',
                                                                 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
