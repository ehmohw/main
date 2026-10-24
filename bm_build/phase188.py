"""2.86: THE BONDS - eleven new pairs and five new trios, for Ashur, the Chef, the Neighbor and their friends.

PAIRS (the two of them, the same summoner's, within 16 blocks of each other; his or her player within 24 - a hidden
achievement and their own banter each, as phase133's):
- ASHUR + LEO, "The Sunfire Oath": Strength and Fire Resistance for you; both of them tougher.
- ASHUR + EMMA, "Bonfire Friends": Regeneration and Fire Resistance for you; both of them heal.
- FISHY + ASHUR, "Steam": Fire Resistance and Water Breathing; underwater, Conduit Power too.
- APOPHISS + ASHUR, "Black Flame": Strength II for you; every five seconds the monsters round you catch fire.
- THE CHEF + EMMA, "The Royal Banquet": Regeneration, and a bite to eat every half minute; both of them heal.
- DENNIS + LEO, "Hammer and Shield": Haste II and Resistance for you; both of them hit harder.
- THE NEIGHBOR + THE CHEF, "Dinner and a Show": Speed, and a bite to eat every half minute; both of them heal.
- APOPHISS + DEMOCRATUS, "Death and Dominion": Strength for you; monsters round you wither; both of them tougher.
- FISHY + THE NEIGHBOR, "The Bubble Ballad": Luck and Water Breathing (Dolphin's Grace underwater); the Neighbor's
  healing song comes round twice as fast.
- THE NEIGHBOR + APOPHISS, "The Serpent's Serenade": monsters round you are charmed (Slowness, Weakness); Apophiss's
  Wrath builds faster.
- THE NEIGHBOR + OMEGA, "Requiem": Resistance and Regeneration for you; the undead round you burn.
(Already in the pack, as asked: Ashur + Celi "Fire and Ice" (phase185), Dennis + Pistachio (phase163), KillerWatt + Apophiss
"Venom and Volts" (phase133).)
TRIOS (three at your side at once - phase100's rules):
- ASHUR, EMMA AND LEO, "The Hearth Guard": Fire Resistance, Resistance and two more hearts; the three tougher.
- LEO, CELI AND ASHUR, "Frost, Flame and Steel": Strength and Resistance; every 20 seconds, frost and flame together
  round you (monsters slowed and set alight); the three heal.
- THE CHEF, FISHY AND THE NEIGHBOR, "The Dinner Party": Speed, Luck and a bite to eat every 20 seconds; the three heal.
- THE NEIGHBOR, OMEGA AND APOPHISS, "The Midnight Opera": Strength II and Night Vision; monsters round you weakened, the
  undead burning; the three tougher.
- EMMA, THE NEIGHBOR AND THE CHEF, "The Royal Feast": Regeneration, two more hearts, Haste and a bite to eat every 20
  seconds; the three heal.
(Already in the pack: Dennis, Leo and Emma "The Crown's Prospect" (phase163); Apophiss, Democratus and KillerWatt "The Dread
Court" (phase133).)"""
from items import T
import phase100 as P100

GOLD = '#ffcf40'
FOE = 'type=#bm:hostile,tag=!bm.npc'
O = '@a[tag=bm.p188o]'                       # (the pair's player, tagged while its pair runs)
VNAME = {'ashur': 'Ashur', 'leo': 'Leo', 'emma': 'Emma', 'fishy': 'Fishy', 'apo': 'Apophiss', 'chef': 'The Chef', 'dennis': 'Dennis',
         'neighbor': 'The Neighbor', 'demo': 'Democratus', 'omega': 'Omega', 'celi': 'Celi', 'ava': 'Queen Ava', 'capshun': 'Mr. Capshun'}
REGEN = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
SNACK = 'effect give @s minecraft:saturation 1 0 true'

# key: (follower a (whose host runs it), partner b, name, colour, achievement line, the buff [commands as a's host, with the
#       player tagged bm.p188o; '{B}' is "as the partner": an execute prefix], intro [(who, line) x2], banter [(who, line, who, line)])
PAIRS = {
    'sunfire': ('ashur', 'leo', 'The Sunfire Oath', '#ffb04a', 'Ashur and Leo, sworn to the same fight',
                [f'effect give {O} minecraft:strength 3 0 true', f'effect give {O} minecraft:fire_resistance 12 0 true',
                 'effect give @s minecraft:resistance 3 0 true', '{B} run effect give @s minecraft:resistance 3 0 true'],
                [('Leo', 'Lady Ashur. Your flame and my shield - for the realm.'), ('ashur', 'Realm, schmealm. I just like setting things on fire next to you.')],
                [('ashur', 'Hey, tin can! Bet your armour gets toasty.', 'Leo', 'It does. Please stand further away.'),
                 ('Leo', 'You fight bravely, Ashur.', 'ashur', 'I fight HOT. Brave is a bonus.')]),
    'bonfire': ('ashur', 'emma', 'Bonfire Friends', '#ff9ad0', 'Ashur and Emma - best friends by the fire',
                [f'execute as {O} run {REGEN}', f'effect give {O} minecraft:fire_resistance 12 0 true', REGEN, '{B} run ' + REGEN],
                [('Emma', 'Ashur! You\'re so warm! Can I hug you?'), ('ashur', 'Ha! Careful, Princess - but sure. Just this once.')],
                [('Emma', 'Ashur, can you make the fire sparkly?', 'ashur', 'Can I?! Watch this!'),
                 ('ashur', 'You\'re alright, Princess. For someone so... pink.', 'Emma', 'And you\'re alright for someone so ORANGE!')]),
    'steam': ('fishy', 'ashur', 'Steam', '#c8e0f0', 'Fishy and Ashur - fire and water, somehow',
              [f'effect give {O} minecraft:fire_resistance 12 0 true', f'effect give {O} minecraft:water_breathing 12 0 true',
               f'execute as {O} at @s if block ~ ~1 ~ minecraft:water run effect give @s minecraft:conduit_power 12 0 true'],
              [('fishy', 'Please - PLEASE - do not boil my bowl.'), ('ashur', 'No promises, fishface.')],
              [('ashur', 'Is your water getting warmer, or is it just me?', 'fishy', 'It is just you. It is ALWAYS just you.'),
               ('fishy', 'A gentleman must remain composed. Even while poaching.', 'ashur', 'I could poach you right now, y\'know.')]),
    'blackflame': ('apo', 'ashur', 'Black Flame', '#6a3ad0', 'Apophiss and Ashur - a flame as dark as he is',
                   [f'effect give {O} minecraft:strength 3 1 true', 'scoreboard players add @s bm.p188 1',
                    f'execute if score @s bm.p188 matches 5.. at @s as @e[{FOE},distance=..8] run data merge entity @s {{Fire:80s}}',
                    'execute if score @s bm.p188 matches 5.. at @s run particle minecraft:soul_fire_flame ~ ~1 ~ 3 0.5 3 0.02 30',
                    'execute if score @s bm.p188 matches 5.. run scoreboard players set @s bm.p188 0'],
                   [('apo', 'A little fire-witch. How... charming.'), ('ashur', 'Charming? Buddy, I\'m about to set your scales on fire.')],
                   [('apo', 'Your flame burns orange. Mine burns BLACK.', 'ashur', 'Yeah, yeah. Mine\'s prettier.'),
                    ('ashur', 'You\'re kinda cool for a giant snake.', 'apo', 'Kinda? I am MAGNIFICENT.')]),
    'banquet': ('chef', 'emma', 'The Royal Banquet', '#ffd0a0', 'The Chef and Emma - a feast fit for a princess',
                [f'execute as {O} run {REGEN}', 'scoreboard players add @s bm.p188 1', f'execute if score @s bm.p188 matches 30.. as {O} run {SNACK}',
                 'execute if score @s bm.p188 matches 30.. run scoreboard players set @s bm.p188 0', REGEN, '{B} run ' + REGEN],
                [('Emma', 'A real chef?! Can you make cake?'), ('chef', 'Cake? Princess, for you I will make a CASTLE of cake.')],
                [('chef', 'Taste this, Princess!', 'Emma', 'Mmmm! It tastes like sunshine!'),
                 ('Emma', 'Chef, you should cook at the palace!', 'chef', 'The palace could not afford me. But for you - free.')]),
    'hammer': ('dennis', 'leo', 'Hammer and Shield', '#d0a860', 'Dennis and Leo - the hammer and the shield',
               [f'effect give {O} minecraft:haste 3 1 true', f'effect give {O} minecraft:resistance 3 0 true',
                'effect give @s minecraft:strength 3 0 true', '{B} run effect give @s minecraft:strength 3 0 true'],
               [('dennis', 'A knight! Ye can hold the line while I swing, lad.'), ('Leo', 'Gladly, master dwarf. Swing away.')],
               [('dennis', 'That armour of yours - who forged it? Shoddy rivets.', 'Leo', 'It has served me well enough.'),
                ('Leo', 'Behind me, Dennis!', 'dennis', 'Behind ye? I\'m SHORT, lad, not slow!')]),
    'show': ('neighbor', 'chef', 'Dinner and a Show', '#a8d0ff', 'The Neighbor and the Chef - music with every course',
             [f'effect give {O} minecraft:speed 3 0 true', 'scoreboard players add @s bm.p188 1', f'execute if score @s bm.p188 matches 30.. as {O} run {SNACK}',
              'execute if score @s bm.p188 matches 30.. run scoreboard players set @s bm.p188 0', REGEN, '{B} run ' + REGEN],
             [('neighbor', 'A chef! Every good dinner needs a soundtrack.'), ('chef', 'And every good song needs a dinner! Magnifique.')],
             [('chef', 'Play something with butter in it!', 'neighbor', 'Butter? ...Smooth jazz it is.'),
              ('neighbor', 'This stew is a symphony, Chef.', 'chef', 'I know. Allegro con gusto!')]),
    'dominion': ('apo', 'demo', 'Death and Dominion', '#7a6ad0', 'Apophiss and Democratus - death and its dominion',
                 [f'effect give {O} minecraft:strength 3 0 true', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:wither 2 0',
                  'effect give @s minecraft:resistance 3 0 true', '{B} run effect give @s minecraft:resistance 3 0 true'],
                 [('demo', 'Serpent. The reaper walks beside you today.'), ('apo', 'Good. Bring your scythe, old man. There is plenty to harvest.')],
                 [('apo', 'Reaper, do you ever smile?', 'demo', 'Only at the end.'),
                  ('demo', 'Their souls are mine, serpent.', 'apo', 'Their souls, yes. Their LANDS are mine.')]),
    'bubble': ('fishy', 'neighbor', 'The Bubble Ballad', '#80c0ff', 'Fishy and the Neighbor - a song under the sea',
               [f'effect give {O} minecraft:luck 3 0 true', f'effect give {O} minecraft:water_breathing 12 0 true',
                f'execute as {O} at @s if block ~ ~1 ~ minecraft:water run effect give @s minecraft:dolphins_grace 4 0 true',
                '{B} if score @s bm.nqsc matches 2.. run scoreboard players remove @s bm.nqsc 20'],
               [('neighbor', 'A fish in a top hat! You must be musical.'), ('fishy', 'I am a baritone, sir. A gentleman baritone.')],
               [('fishy', 'Blub... blub-blub... BLUB.', 'neighbor', 'Bravo! A bit flat on the last blub.'),
                ('neighbor', 'Duet? You take the bubbles, I\'ll take the melody.', 'fishy', 'Splendid. Do keep up.')]),
    'serenade': ('neighbor', 'apo', 'The Serpent\'s Serenade', '#6ad0a0', 'The Neighbor and Apophiss - a song to charm a serpent',
                 [f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:slowness 3 0', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:weakness 3 0',
                  'scoreboard players add @s bm.p188 1', 'execute if score @s bm.p188 matches 4.. run scoreboard players set @s bm.p188 0',
                  'execute if score @s bm.p188 matches 0 {B2} run scoreboard players add @s bm.apch 1'],
                 [('neighbor', 'A snake! Let\'s see if the old flute trick works.'), ('apo', 'Play one note of that, minstrel, and I will eat your hat.')],
                 [('neighbor', 'Admit it - you were swaying.', 'apo', 'I was NOT swaying. I was... coiling. Rhythmically.'),
                  ('apo', 'Play the dark one again. The one in the minor key.', 'neighbor', 'You DO like it!')]),
    'requiem': ('neighbor', 'omega', 'Requiem', '#9fb4ff', 'The Neighbor and King Omega - a song for the dead',
                [f'effect give {O} minecraft:resistance 3 0 true', f'execute as {O} run {REGEN}',
                 'execute at @s as @e[type=#minecraft:undead,distance=..10] run data merge entity @s {Fire:60s}'],
                [('omega', 'Musician. The dead have not heard a song in a thousand years.'), ('neighbor', 'Then let\'s give them a good one, Your Majesty.')],
                [('neighbor', 'Any requests, King Omega?', 'omega', 'Something slow. Something... final.'),
                 ('omega', 'Your music stirs old memories.', 'neighbor', 'Good ones, I hope!')]),
    # (2.94) the owner's new pairs: the royal family and its reaper; Mr. Capshun and his favourite characters
    'reaper_rose': ('demo', 'emma', 'The Reaper and the Rose', '#c890ff', 'Democratus and Emma - the darkness keeps watch over the princess',
                    [f'execute as {O} run {REGEN}', f'execute at {O} as @e[{FOE},distance=..8] run effect give @s minecraft:slowness 2 0', REGEN, '{B} run ' + REGEN],
                    [('Emma', 'Democratus! You came back! I knew you would.'), ('demo', 'Princess. Someone has to keep the dark away from you.')],
                    [('Emma', 'Do you ever take off the hood?', 'demo', 'Not where the monsters can see.'),
                     ('demo', 'Stay behind my scythe, little one.', 'Emma', 'Only if you stay behind my smile!')]),
    'crown_scythe': ('demo', 'ava', 'Crown and Scythe', '#8ad0d8', 'Democratus and Queen Ava - the family\'s old quarrel set aside',
                     ['effect give @s minecraft:resistance 3 0 true', f'effect give {O} minecraft:resistance 3 0 true', f'effect give {O} minecraft:strength 3 0 true',
                      '{B} run effect give @s minecraft:resistance 3 0 true'],
                     [('ava', 'Democratus. It has been a long time.'), ('demo', 'Too long, Your Majesty. What the family did with the gem - I have not forgiven it. But I am here.')],
                     [('ava', 'You could come home, you know.', 'demo', 'Home is wherever the monsters are, my queen.'),
                      ('demo', 'You still wear the crown well.', 'ava', 'And you still brood beautifully.')]),
    'storybook': ('capshun', 'emma', 'Once Upon a Time', '#ffe4a0', 'Mr. Capshun and Emma - a narrator and his favourite heroine',
                  [f'effect give {O} minecraft:luck 3 0 true', f'execute as {O} run {REGEN}', REGEN, '{B} run ' + REGEN],
                  [('capshun', '[Mr. Capshun narrates: "And then the princess arrived. Finally - a protagonist."]'), ('Emma', 'Ooh, are you telling my story? Make it a good one!')],
                  [('Emma', 'What happens next, Mr. Capshun?', 'capshun', '"I\'d tell you, but that would be spoilers."'),
                   ('capshun', '[Mr. Capshun narrates: "She was brave. She was kind. She had excellent taste in narrators."]', 'Emma', 'Hee hee! I do!')]),
    'monologue': ('capshun', 'apo', "The Villain's Monologue", '#9ad06a', 'Mr. Capshun and Apophiss - every villain needs a narrator',
                  [f'effect give {O} minecraft:strength 3 0 true', f'execute at {O} as @e[{FOE},distance=..8] run effect give @s minecraft:weakness 2 0',
                   '{B} run effect give @s minecraft:resistance 3 0 true'],
                  [('apo', 'You. Scribbler. Write me something TERRIFYING.'), ('capshun', '[Mr. Capshun narrates: "The serpent king rose, and the monsters wept."]')],
                  [('capshun', '"Any last words for the audience, Your Serpentness?"', 'apo', 'Yes. KNEEL.'),
                   ('apo', 'Do I get a theme song?', 'capshun', '"Dun dun DUNNN. ...That\'s all the budget allowed."')]),
}

TRIOS = {   # key: (name, colour, members, advancement title, description)
    'hearth': ('The Hearth Guard', '#ffa860', ('ashur', 'emma', 'leo'), 'The Hearth Guard', 'Walk with Ashur, Emma and Leo at once'),
    'ffs': ('Frost, Flame and Steel', '#c0d8ff', ('leo', 'celi', 'ashur'), 'Frost, Flame and Steel', 'Walk with Leo, Celi and Ashur at once'),
    'dinner': ('The Dinner Party', '#ffd890', ('chef', 'fishy', 'neighbor'), 'The Dinner Party', 'Walk with the Chef, Fishy and the Neighbor at once'),
    'opera': ('The Midnight Opera', '#8a8aff', ('neighbor', 'omega', 'apo'), 'The Midnight Opera', 'Walk with the Neighbor, Omega and Apophiss at once'),
    'feast': ('The Royal Feast', '#ffc0e0', ('emma', 'neighbor', 'chef'), 'The Royal Feast', 'Walk with Emma, the Neighbor and the Chef at once'),
    'family': ('The Family Reunited', '#b8a8ff', ('emma', 'ava', 'demo'), 'The Family Reunited', 'Walk with Emma, Queen Ava and Democratus at once'),
    'everafter': ('Happily Ever After', '#ffe0a8', ('capshun', 'emma', 'leo'), 'Happily Ever After', 'Walk with Mr. Capshun, Emma and Leo at once'),
}
ICON = {'family': 'bm:demo_seal', 'everafter': 'bm:capshun_pencil', 'reaper_rose': 'bm:demo_seal', 'crown_scythe': 'bm:demo_seal',
        'storybook': 'bm:capshun_pencil', 'monologue': 'bm:capshun_pencil',
        'hearth': 'bm:ashur_cinder', 'ffs': 'bm:ashur_cinder', 'dinner': 'bm:chef_ladle', 'opera': 'bm:neighbor_baton', 'feast': 'bm:neighbor_baton'}
P100.TRIOS.update(TRIOS)
P100.BANTER.update({
    'hearth': [('Emma', 'Ashur keeps us warm, Leo keeps us safe!', 'Ashur', 'And you keep us... pink. Somehow.'),
               ('Leo', 'Stay behind me, Princess. Ashur - not too close.', 'Ashur', 'Relax, tin can. I only singe people I like.'),
               ('Ashur', 'Campfire tonight? I\'ll light it. With my face.', 'Emma', 'YES! Leo, can we?!')],
    'ffs': [('Celi', 'Fire on my left, a tin can on my right. Wonderful.', 'Ashur', 'You love it, ice cube.'),
            ('Leo', 'Frost, flame and steel - none shall pass.', 'Celi', 'Did you practise that in a mirror?'),
            ('Ashur', 'Race you both! Most monsters wins!', 'Leo', 'This is not a game, Ashur.')],
    'dinner': [('The Chef', 'Tonight: a seafood special!', 'Fishy', 'I beg your PARDON?'),
               ('The Neighbor', 'Music, food and a fish in a hat. Best party ever.', 'Fishy', 'A GENTLEMAN fish in a hat.'),
               ('Fishy', 'Chef, might I trouble you for a garnish of kelp?', 'The Chef', 'For you, monsieur - the finest kelp in the land!')],
    'opera': [('Omega', 'Sing, minstrel. Let the dead hear you.', 'The Neighbor', 'Act one, scene one - the monsters all lose!'),
              ('Apophiss', 'An opera of serpents and ghosts. How fitting.', 'Omega', 'A king and a serpent king. The stage is ours.'),
              ('The Neighbor', 'Encore?', 'Apophiss', '...Fine. ONE encore.')],
    'family': [('Emma', 'Mother! Democratus! All of us together!', 'Queen Ava', 'Together, my darling. As it should have been.'),
               ('Democratus', 'I never thought I would walk beside you two again.', 'Emma', 'Well, get used to it!'),
               ('Queen Ava', 'Brother... thank you for watching over her.', 'Democratus', 'Always.')],
    'everafter': [('Mr. Capshun', '[Mr. Capshun narrates: "The princess, the knight and the narrator set out. Mostly the narrator."]', 'Leo', 'I believe I did most of the fighting.'),
                  ('Emma', 'Mr. Capshun, will this story have a happy ending?', 'Mr. Capshun', '"With you two in it? Guaranteed."'),
                  ('Leo', 'Must you narrate everything I do?', 'Mr. Capshun', '[Mr. Capshun narrates: "He said, gruffly."]')],
    'feast': [('Emma', 'A royal feast! With music!', 'The Chef', 'For the Princess - only the finest!'),
              ('The Neighbor', 'A little dinner music, Your Highness?', 'Emma', 'Yes please! Something you can dance to!'),
              ('The Chef', 'Eat, eat! You are all too skinny!', 'The Neighbor', 'I\'m a musician, Chef. We live on applause.')],
})


def extend_offers(O_, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    second = []
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p188 dummy', 'scoreboard objectives add bm.p188b dummy']
    G.OBJECTIVES += ['bm.p188', 'bm.p188b']
    host = lambda k: P100.WHO[k]
    partner = lambda k: f'execute as @e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..16] if score @s bm.pid = #me bm.pid'
    voice = lambda w: VNAME.get(w, w)
    def line(who, txt, to='@s'):
        n = voice(who); c = P100.VOICE.get(n, ('#ffffff', '#e0e0e0'))
        return tellraw(to, [T(f'{n}: ', c[0], bold=True), T(f'"{txt}"', c[1])])
    # ================================================================== the pairs: every second, as each follower who leads one
    by_a = {}
    for k, (a, b, *_r) in PAIRS.items():
        by_a.setdefault(a, []).append(k)
    for a, keys in by_a.items():
        typ, tag = host(a)
        second.append(f'execute as @e[type=minecraft:{typ},tag={tag},tag=!bm.ffpet] at @s run function bm:p188/{a}')
        body = ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p188o',
                'execute unless entity @a[tag=bm.p188o] run return 0']
        for k in keys:
            b = PAIRS[k][1]
            body += [f'scoreboard players set #p_{k} bm.rng 0', f'{partner(b)} run scoreboard players set #p_{k} bm.rng 1',
                     f'execute if score #p_{k} bm.rng matches 1 run function bm:p188/pair/{k}']
        fn(f'p188/{a}', body + ['tag @a remove bm.p188o'])
    for k, (a, b, nm, col, desc, buff, intro, banter) in PAIRS.items():
        lines = [l.replace('{B2}', partner(b)[len('execute '):]).replace('{B}', partner(b)).replace('bm.p188 ', f'bm.p8{k} ') for l in buff]
        if any(f'bm.p8{k} ' in l for l in lines):
            G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add bm.p8{k} dummy']
            G.OBJECTIVES.append(f'bm.p8{k}')
        fn(f'p188/pair/{k}', lines + [f'execute as {O} unless entity @s[advancements={{bm:story/pair_{k}=true}}] run function bm:p188/first/{k}',
                                      'scoreboard players add @s bm.p188b 1', f'execute if score @s bm.p188b matches 150.. run function bm:p188/banter/{k}'])
        fn(f'p188/first/{k}', [f'advancement grant @s only bm:story/pair_{k}',
                               tellraw('@s', PREFIX + [T(f'{nm}! ', col, bold=True), T('A new pair - see the README for what it gives.', 'gray')])] +
           [line(w, t) for w, t in intro])
        wjson(f'bm/advancement/story/pair_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                      'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': ICON.get(k, 'bm:neighbor_baton' if 'neighbor' in (a, b) else 'bm:chef_ladle' if 'chef' in (a, b) else 'bm:ashur_cinder' if 'ashur' in (a, b) else 'bm:dw_horn')}},
                                                                  'title': T(nm, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'task', 'show_toast': True,
                                                                  'announce_to_chat': True, 'hidden': True}})
        for j, (w1, t1, w2, t2) in enumerate(banter):
            fn(f'p188/say/{k}{j}', [line(w1, t1, '@a[tag=bm.p188o,tag=!bm.hush]'), line(w2, t2, '@a[tag=bm.p188o,tag=!bm.hush]')])
        fn(f'p188/banter/{k}', ['scoreboard players set @s bm.p188b 0', f'execute store result score #r bm.rng run random value 0..{len(banter) - 1}'] +
           [f'execute if score #r bm.rng matches {j} run function bm:p188/say/{k}{j}' for j in range(len(banter))])

    # ================================================================== the trios (phase100 finds them and calls p100/<key> as the player)
    mine = lambda k: f'@e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..24]'
    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    hb = 'execute unless predicate bm:p100/hb run effect give @s minecraft:health_boost 15 0 true'
    tick20 = ['scoreboard players add @s bm.p188 1', 'execute if score @s bm.p188 matches 20.. run scoreboard players set @s bm.p188 0']
    fn('p100/hearth', ['effect give @s minecraft:fire_resistance 12 0 true', 'effect give @s minecraft:resistance 3 0 true', hb] +
       each(TRIOS['hearth'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    fn('p100/ffs', ['effect give @s minecraft:strength 3 0 true', 'effect give @s minecraft:resistance 3 0 true'] + tick20 +
       ['execute if score @s bm.p188 matches 0 run function bm:p188/ffs_wave'] + each(TRIOS['ffs'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p188/ffs_wave', ['particle minecraft:snowflake ~ ~0.5 ~ 4 0.3 4 0.05 60', 'particle minecraft:flame ~ ~0.5 ~ 4 0.3 4 0.02 40',
                         'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 0.8', 'playsound minecraft:block.powder_snow.place player @a[distance=..16] ~ ~ ~ 1 0.6',
                         f'effect give @e[{FOE},distance=..8] minecraft:slowness 5 2', f'execute as @e[{FOE},distance=..8] run data merge entity @s {{Fire:80s}}'])
    fn('p100/dinner', ['effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:luck 3 0 true'] + tick20 +
       [f'execute if score @s bm.p188 matches 0 run {SNACK}', 'execute if score @s bm.p188 matches 0 run particle minecraft:note ~ ~2 ~ 0.6 0.3 0.6 1 6'] +
       each(TRIOS['dinner'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p100/opera', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:night_vision 15 0 true',
                      f'effect give @e[{FOE},distance=..8] minecraft:weakness 3 0', 'execute as @e[type=#minecraft:undead,distance=..8] run data merge entity @s {Fire:60s}'] +
       each(TRIOS['opera'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    fn('p100/feast', [REGEN, hb, 'effect give @s minecraft:haste 3 0 true'] + tick20 + [f'execute if score @s bm.p188 matches 0 run {SNACK}'] +
       each(TRIOS['feast'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p100/family', [REGEN, hb, 'effect give @s minecraft:resistance 3 0 true'] + each(TRIOS['family'][2], 'effect give @s minecraft:strength 3 0 true') +
       each(TRIOS['family'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p100/everafter', [REGEN, 'effect give @s minecraft:resistance 3 0 true', 'effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:luck 3 0 true'] +
       each(TRIOS['everafter'][2], 'effect give @s minecraft:resistance 3 0 true') + ['function bm:p100/banter_tick'])
    for k, (nm, col, mem, at, desc) in TRIOS.items():
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': ICON[k]}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal', 'show_toast': True,
                                                                 'announce_to_chat': True, 'hidden': True}})
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
