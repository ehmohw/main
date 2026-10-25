"""2.94r: MORE BONDS - Bender and Mr. Capshun with everyone, and a few more that make sense (phase188's engine runs the pairs;
phase100 finds the trios and calls p100/<key>, built here). Each pair: the two of them, the same summoner's, within 16 blocks
of each other and their player within 24 - a hidden achievement, an introduction the first time, and banter now and then.

BENDER + ... (the goodest boy gets on with everyone):
- TULLIUS, "Ship's Dog": Water Breathing and Dolphin's Grace; Bender tougher.
- THE FROG, "Frog and Dog": Jump Boost II and Speed.
- WILFREY, "The Gentle One": Regeneration and Hero of the Village.
- PISTACHIO, "Ghost Dog": Night Vision and Luck; every 30 s Pistachio slips you a biscuit.
- KING OMEGA, "The King's Good Boy": Resistance; the undead round you burn.
- ASHUR, "Hot Dog": Fire Resistance and Speed; Bender tougher.
- THE CHEF, "Table Scraps": a bite to eat every 20 s; both of them heal.
- THE NEIGHBOR, "Howl Along": Speed and Jump Boost; Bender heals.
- QUEEN AVA, "A Dog for the Palace": Water Breathing and Regeneration.
- QUEEN PEARL, "Spoiled Rotten": Luck and Speed; cake every 30 s.
- BLOO, "Hackles Down": Strength and Speed.
- THE ARACHNO-LANTERN, "Chase!": Fire Resistance; every 10 s the monsters round you catch its embers.
- 8-BIT CECIL, "A Wild Dog Appeared": Haste II and Luck.
- 8-BIT LEO, "Pixel Hound": Strength and Resistance.
- 8-BIT EMMA, "Press A to Pet": Speed and Jump Boost II.
- THE SKY BUDDIES, "Chasing Clouds": Jump Boost II and Slow Falling (sneak to drop).
MR. CAPSHUN + ... (every story needs a narrator):
- CELI, "The Ice Queen's Chronicle": Resistance; the monsters round you slowed.
- ZIB, "First Contact": Speed and Night Vision; the monsters round you glow.
- CECIL, "The Wizard's Biography": Haste and Regeneration.
- KILLERWATT, "Shocking Twist": Speed II; the monsters round you glow.
- LEO, "The Hero's Journey": Strength and Resistance.
- DEMOCRATUS, "A Dark Chapter": Strength; the monsters round you wither.
- TULLIUS, "The Ballad of the Drowned Captain": Water Breathing and Dolphin's Grace.
- THE FROG, "The Frog Prince (Unauthorised)": Jump Boost and Strength.
- DONADO, "The Collar Tag Chronicles": Speed and Luck.
- PEARLMAN, "Product Placement": Luck II and Hero of the Village.
- WILFREY, "The Gentle One's Tale": Regeneration and Resistance.
- DENNIS, "Dig Deeper": Haste II.
- PISTACHIO, "The Butler Did It": Night Vision; the monsters round you weakened.
- KING OMEGA, "Epilogue": Resistance; the undead round you burn.
- ASHUR, "Plot Heat": Fire Resistance and Strength.
- THE CHEF, "A Recipe for Adventure": a bite to eat every 20 s; Regeneration.
- QUEEN AVA, "The Lost Queen": Regeneration and Water Breathing.
- QUEEN PEARL, "The Regent's Gossip": Luck and Jump Boost.
- BLOO, "The Beast of the Old Songs": Strength II; Bloo tougher.
- THE STALKER, "A Horror Story": Night Vision; the monsters round you weakened and slowed.
- THE ARACHNO-LANTERN, "A Spooky Tale": Fire Resistance; the monsters round you glow.
- BONES, "Jaws, but Nice": Water Breathing and Dolphin's Grace; underwater, Strength.
- 8-BIT CECIL, "Retcon": Haste and Luck.
- 8-BIT LEO, "Sprite Work": Resistance and Speed.
- 8-BIT EMMA, "Fan Art": Regeneration and Jump Boost.
AND:
- TULLIUS + BONES, "Shark and Sailor": Water Breathing, Dolphin's Grace and Conduit Power.
- QUEEN AVA + BONES, "The Kingdom's Guardian": Regeneration and Water Breathing; Bones tougher.
- FISHY + BONES, "Natural Predators": Water Breathing and Luck (Fishy keeps his distance).
- THE CHEF + PISTACHIO, "Below Stairs": a bite to eat every 20 s; both heal.
- DENNIS + PEARLMAN, "Weighed in Gold": Haste and Luck II.
- ZIB + DONADO, "The Away Team": Speed and Night Vision; both tougher.
- THE SKY BUDDIES + THE ARACHNO-LANTERN, "Harvest Moon": Night Vision and Fire Resistance.
TRIOS (three at your side at once - phase100's rules):
- KING OMEGA, PISTACHIO AND WILFREY, "The Haunting": Night Vision, Resistance and Regeneration; every 15 s the undead round
  you are laid to rest (12 to each, and they burn); the three heal.
- QUEEN AVA, TULLIUS AND BONES, "The Tide Court": Water Breathing, Conduit Power, Dolphin's Grace and Strength; every 20 s a
  wave round you throws the monsters back; the three tougher.
- PEARLMAN, DENNIS AND PISTACHIO, "The Market Guild": Luck II, Haste II and Hero of the Village; every minute your cut - an
  emerald; the three heal."""
from items import T
import phase100 as P100
import phase125 as P125
import phase188 as P188

FOE = 'type=#bm:hostile,tag=!bm.npc'
O = P188.O
REGEN = P188.REGEN
SNACK = P188.SNACK

# every follower the bonds can name - its host, its name, its voice
for _w, (_nm, _pr, _col, _host, _tag, _try, _home) in P125.WHO.items():
    P100.WHO.setdefault(_w, (_host, _tag))
    P188.VNAME.setdefault(_w, _nm[0].upper() + _nm[1:])
    _lt = '#' + ''.join(f'{(int(_col[i:i + 2], 16) + 255 * 2) // 3:02x}' for i in (1, 3, 5))
    for _n in (P188.VNAME[_w], _nm[0].upper() + _nm[1:]):
        P100.VOICE.setdefault(_n, (_col, _lt))
for _n, _c in (('Sunny', '#ffd04a'), ('Snooze', '#c8b8ff'), ('Nimbus', '#e8f0ff')):
    P100.VOICE.setdefault(_n, (_c, '#fff4d8'))

P = lambda e, a=0, t=3: f'effect give {O} minecraft:{e} {t} {a} true'          # (for you)
S = lambda e, a=0, t=3: f'effect give @s minecraft:{e} {t} {a} true'            # (for the one who leads the pair)
B = lambda e, a=0, t=3: '{B} run ' + S(e, a, t)                                 # (for the partner)
FOES = lambda e, a=0, t=2, r=8: f'execute at {O} as @e[{FOE},distance=..{r}] run effect give @s minecraft:{e} {t} {a}'
UNDEAD_BURN = f'execute at {O} as @e[type=#minecraft:undead,tag=!bm.npc,distance=..8] run data merge entity @s {{Fire:60s}}'
NV, WB = P('night_vision', t=15), P('water_breathing', t=15)
PREGEN = f'execute as {O} run {REGEN}'                                           # (Regeneration that ticks: only when it's run out)


def EVERY(n, f):
    """every n seconds the pair is together: bm:p219/<f>, as its leader, at it (the counter is the pair's own)"""
    return ['scoreboard players add @s bm.p188 1', f'execute if score @s bm.p188 matches {n}.. run function bm:p219/{f}',
            f'execute if score @s bm.p188 matches {n}.. run scoreboard players set @s bm.p188 0']


PAIRS = {
    # ================================================================== BENDER + everyone
    'shipdog': ('bender', 'tul', "Ship's Dog", '#7ad8ff', 'Bender and Tullius - every crew needs a dog, even a drowned one',
                [WB, P('dolphins_grace'), S('resistance')],
                [('tul', 'A dog. On my ship, you would have been the only one worth his rations.'), ('bender', '(he sniffs Tullius\'s boots. Seaweed. His tail goes faster.)')],
                [('tul', 'Sit.', 'bender', '(sits. At once. Perfectly.)'),
                 ('bender', '(barks at the sea)', 'tul', 'Aye. I miss her too, lad.')]),
    'frogdog': ('bender', 'frog', 'Frog and Dog', '#6ac850', 'Bender and the Frog - he hops, the dog chases',
                [P('jump_boost', 1), P('speed')],
                [('frog', 'Hmph. A dog. Do not even THINK about licking me.'), ('bender', '(he licks him)')],
                [('bender', '(pounces at the Frog - and lands where the Frog was a moment ago)', 'frog', 'Too slow, pup. Again.'),
                 ('frog', 'Fetch my sword, mutt.', 'bender', '(he brings back a stick, very proudly)')]),
    'gentle': ('bender', 'wil', 'The Gentle One', '#f4f4f4', 'Bender and Wilfrey - the gentle grandson and the village dog',
               [PREGEN, P('hero_of_the_village', t=15)],
               [('wil', 'Hello, little one. There was a dog like you in my village, long ago.'), ('bender', '(he leans his whole weight against Wilfrey\'s leg)')],
               [('bender', '(he drops a flower at Wilfrey\'s feet - roots, dirt and all)', 'wil', 'Thank you. I shall keep it always.'),
                ('wil', 'Grandfather never liked dogs.', 'bender', '(he growls at nothing in particular, on Wilfrey\'s behalf)')]),
    'ghostdog': ('bender', 'pistachio', 'Ghost Dog', '#7ae890', 'Bender and Pistachio - the dog who barks at the butler',
                 [NV, P('luck')] + EVERY(30, 'biscuit'),
                 [('pistachio', 'Master Bender. Do wipe your paws. ...He cannot hear me. He is barking.'), ('bender', '(barking at the ghost, tail wagging)')],
                 [('bender', '(he tries to sniff Pistachio and goes straight through him)', 'pistachio', 'That tickles, sir.'),
                  ('pistachio', 'A biscuit for the young master.', 'bender', '(the biscuit is gone. Was there ever a biscuit?)')]),
    'kingsgood': ('bender', 'omega', "The King's Good Boy", '#9fb4ff', 'Bender and King Omega - the dead do love a good dog',
                  [P('resistance'), UNDEAD_BURN],
                  [('omega', 'A hound! Splendid! The dead do so love a good dog. Sit, sit!'), ('bender', '(he sits - then rolls over too, just to be safe)')],
                  [('omega', 'Fetch, good hound! The bone of a fallen foe!', 'bender', '(he is VERY into this game)'),
                   ('bender', '(he howls along with the souls circling the King)', 'omega', 'Beautiful. A choir of one.')]),
    'hotdog': ('bender', 'ashur', 'Hot Dog', '#ff7a2a', 'Bender and Ashur - he likes her warm patch',
               [P('fire_resistance', t=12), P('speed'), S('resistance')],
               [('ashur', 'A DOGGO! Don\'t worry, fluffy, I won\'t singe you. Much.'), ('bender', '(he sneezes at the smoke. His tail doesn\'t stop.)')],
               [('ashur', 'Fetch the fireball, Bender! ...No, not THAT one!', 'bender', '(he proudly brings back a slightly smoking stick)'),
                ('bender', '(he flops down in the warm patch right beside her)', 'ashur', 'Aww. I\'m your heater now, huh?')]),
    'scraps': ('bender', 'chef', 'Table Scraps', '#ffd07a', 'Bender and the Chef - the kitchen is no place for a dog (here is a sausage)',
               [REGEN, '{B} run ' + REGEN] + EVERY(20, 'snack'),
               [('chef', 'Non, non, NON! The kitchen is no place for a dog! ...You want a sausage? Here.'), ('bender', '(the sausage vanishes)')],
               [('bender', '(he sits by the Chef. He stares. He does not blink.)', 'chef', 'Zut! FINE. One more!'),
                ('chef', 'Bender, mon ami - taste this for me.', 'bender', '(he eats the whole pot)')]),
    'howl': ('bender', 'neighbor', 'Howl Along', '#7ab8ff', 'Bender and the Neighbor - a minstrel and his backing singer',
             [P('speed'), P('jump_boost'), REGEN],
             [('neighbor', 'Hey there, pup! Wanna sing harmony?'), ('bender', '(AWOOOOOO)')],
             [('neighbor', 'A one, a two, a one-two-three -', 'bender', '(AWOO! AWOO-OO!)'),
              ('bender', '(he howls off-key, very happily)', 'neighbor', 'Perfect pitch. Never change.')]),
    'palacedog': ('bender', 'ava', 'A Dog for the Palace', '#6ad8e8', 'Bender and Queen Ava - Emma always wanted a dog',
                  [WB, PREGEN],
                  [('ava', 'Oh... Emma always wanted a dog. The palace only ever had fish.'), ('bender', '(he tries to lick a ghost. It is confusing for everyone.)')],
                  [('ava', 'You guard her well, little one.', 'bender', '(he sits up very straight. Very official.)'),
                   ('bender', '(he paws at the shimmer of her hem)', 'ava', 'I cannot pet you, sweet one. But I would, if I could.')]),
    'spoiled': ('bender', 'pearlq', 'Spoiled Rotten', '#5ae0d8', 'Bender and Queen Pearl - who gave the dog cake?',
                [P('luck'), P('speed')] + EVERY(30, 'cake'),
                [('pearlq', 'A DOG! Who\'s a good boy? YOU are! Do you want cake? Of COURSE you want cake!'), ('bender', '(he wants cake)')],
                [('pearlq', 'Bender, darling, don\'t tell Ava I gave you cake.', 'bender', '(cake on his nose; the very picture of innocence)'),
                 ('bender', '(he rolls over for a belly rub)', 'pearlq', 'Oh, I can\'t say no to that face. More cake!')]),
    'hackles_down': ('bender', 'bloo', 'Hackles Down', '#5a9ae8', 'Bender and Bloo - the beast who hates everyone, and the dog who doesn\'t care',
                     [P('strength'), P('speed')],
                     [('bloo', 'A dog. Dogs follow humans. I do not trust dogs.'), ('bender', '(he rolls onto his back at the beast\'s feet, all four paws in the air)')],
                     [('bender', '(he drops his ball at Bloo\'s feet)', 'bloo', '...Hrrn. Once. I will throw it ONCE.'),
                      ('bloo', 'Stop following me, small dog.', 'bender', '(he follows him closer)')]),
    'chase': ('bender', 'lantern', 'Chase!', '#ff8a2a', 'Bender and the Arachno-Lantern - eight legs to chase',
              [P('fire_resistance', t=12)] + EVERY(10, 'embers'),
              [('bender', '(he play-bows at the walking pumpkin)'), ('lantern', '(it play-bows back - with all eight legs)')],
              [('bender', '(he chases the Lantern round and round)', 'lantern', '(it chases him back, puffing happy embers)'),
               ('lantern', '(it curls up beside the dog to keep him warm)', 'bender', '(a long, contented sigh)')]),
    'wilddog': ('bender', 'pxcecil', 'A Wild Dog Appeared', '#b070ff', 'Bender and 8-Bit Cecil - the dog who sniffs the side of a sprite',
                [P('haste', 1), P('luck')],
                [('pxcecil', 'A WILD DOG APPEARED!'), ('bender', '(he sniffs the flat wizard from the side. There is no side.)')],
                [('pxcecil', 'BENDER used FETCH! It\'s super effective!', 'bender', '(he drops the ball, very pleased)'),
                 ('bender', '(he barks at the pixels)', 'pxcecil', 'CECIL is confused! ...Stop that.')]),
    'pixelhound': ('bender', 'pxleo', 'Pixel Hound', '#4ab0ff', 'Bender and 8-Bit Leo - every knight needs a hound, in any resolution',
                   [P('strength'), P('resistance')],
                   [('pxleo', 'A loyal hound! Will you join my quest?'), ('bender', '(he joins the quest)')],
                   [('pxleo', 'Heel, brave hound!', 'bender', '(he heels, then un-heels, then heels again)'),
                    ('bender', '(he tries to carry 8-Bit Leo\'s sword. It is one pixel wide.)', 'pxleo', 'A noble effort!')]),
    'press_a': ('bender', 'pxemma', 'Press A to Pet', '#ff6ac8', 'Bender and 8-Bit Emma - the best button',
                [P('speed'), P('jump_boost', 1)],
                [('pxemma', 'A DOGGY! Press A to pet! Press A! Press A!'), ('bender', '(he has been pressed. He is so happy.)')],
                [('pxemma', 'Bender! You\'re my player two!', 'bender', '(he wags his tail at sixty frames a second)'),
                 ('bender', '(he brings her a ball)', 'pxemma', 'ITEM GET! Thank you, Bender!')]),
    'clouds': ('bender', 'sky', 'Chasing Clouds', '#ffd04a', 'Bender and the Sky Buddies - he will catch that cloud one day',
               [P('jump_boost', 1), P('slow_falling')],
               [('sky', 'Nimbus: ":3"'), ('bender', '(he jumps for the cloud. He jumps again. He will NEVER stop jumping.)')],
               [('sky', 'Sunny: "Bender! Catch!"', 'bender', '(he catches a sunbeam - and looks very confused)'),
                ('bender', '(he curls up in the shade of the cloud)', 'sky', 'Snooze: "...finally... someone who gets it..."')]),

    # ================================================================== MR. CAPSHUN + everyone
    'icechron': ('capshun', 'celi', "The Ice Queen's Chronicle", '#9ad8ff', 'Mr. Capshun and Celi - a narrator, and someone who wants him to stop',
                 [P('resistance'), FOES('slowness')],
                 [('capshun', '[Mr. Capshun narrates: "Enter the knight of ice: cold, sharp, deeply unimpressed."]'), ('Celi', 'Is he going to do that the whole time?')],
                 [('Celi', 'Stop narrating me.', 'capshun', '"[She said, frostily.]"'),
                  ('capshun', '"Celi - tragic backstory? Secret soft side?"', 'Celi', 'Spear. Your face. Choose.')]),
    'contact': ('capshun', 'zib', 'First Contact', '#3ad8c8', 'Mr. Capshun and Zib - the alien and the stick figure',
                [P('speed'), NV, FOES('glowing', t=3, r=10)],
                [('zib', 'What ARE you? You are one pixel thick. Fascinating.'), ('capshun', '"I\'m a Buddy. You\'re an alien. Let\'s not make it weird."')],
                [('capshun', '[Mr. Capshun narrates: "The alien, clearly superior, took notes."]', 'zib', 'I am taking notes. You are very strange.'),
                 ('zib', 'On my planet, narrators are illegal.', 'capshun', '"That explains a LOT about your planet."')]),
    'biography': ('capshun', 'cecil', "The Wizard's Biography", '#b48cff', 'Mr. Capshun and Cecil - the wizard\'s life, unauthorised',
                  [P('haste'), PREGEN],
                  [('capshun', '"Cecil! The wizard who was there for everything. Mind if I write it all down?"'), ('Cecil', 'I mind very much.')],
                  [('capshun', '"Chapter Nine: Cecil Makes a Questionable Decision."', 'Cecil', 'Which one?'),
                   ('Cecil', 'Leave out the part with the island.', 'capshun', '"[He did not leave out the part with the island.]"')]),
    'twist': ('capshun', 'kw', 'Shocking Twist', '#ffe040', 'Mr. Capshun and KillerWatt - nobody saw it coming',
              [P('speed', 1), FOES('glowing', t=3, r=10)],
              [('kw', '*bzzt?*'), ('capshun', '[Mr. Capshun narrates: "And then - a SHOCKING twist!" ...Sorry. Couldn\'t help it.]')],
              [('capshun', '"KillerWatt: a monster of few words."', 'kw', '*BZZT*'),
               ('kw', '*sparks crawl up the narrator\'s pencil*', 'capshun', '"Ow. Ow! Good line, though."')]),
    'journey': ('capshun', 'leo', "The Hero's Journey", '#5ab8e0', 'Mr. Capshun and Leo - the hero, as narrated',
                [P('strength'), P('resistance')],
                [('capshun', '[Mr. Capshun narrates: "The knight stepped forward, brave and true, and slightly too serious."]'), ('Leo', 'I am exactly as serious as the situation demands.')],
                [('Leo', 'Must you announce every swing?', 'capshun', '"[He swung. It was very heroic.]"'),
                 ('capshun', '"Leo, smile for the illustration."', 'Leo', 'I am smiling.')]),
    'darkchapter': ('capshun', 'demo', 'A Dark Chapter', '#7ad06a', 'Mr. Capshun and Democratus - the narrator gets serious',
                    [P('strength'), FOES('wither', t=3)],
                    [('demo', 'You know what I did, narrator.'), ('capshun', '"I do. Every story has a dark chapter. Yours is just... longer."')],
                    [('capshun', '[Mr. Capshun narrates: "The old general said nothing. He did not need to."]', 'demo', '...Thank you.'),
                     ('demo', 'Will you write that I was a villain?', 'capshun', '"I\'ll write that you were sorry. The reader can decide."')]),
    'ballad': ('capshun', 'tul', 'The Ballad of the Drowned Captain', '#7ad8ff', 'Mr. Capshun and Tullius - a sea shanty, badly',
               [WB, P('dolphins_grace')],
               [('capshun', '"There once was a captain who drowned - "'), ('tul', 'Finish that line and you will drown too.')],
               [('tul', 'My ship was the finest in the cold seas.', 'capshun', '"[It was, at the time, mostly holes.]"'),
                ('capshun', '"Any regrets, Captain?"', 'tul', 'Letting Leo win that one race. Once.')]),
    'frogprince': ('capshun', 'frog', 'The Frog Prince (Unauthorised)', '#6ac850', 'Mr. Capshun and the Frog - he is NOT a prince',
                   [P('jump_boost'), P('strength')],
                   [('capshun', '[Mr. Capshun narrates: "Once upon a time, a frog. Kiss him, and - "]'), ('frog', 'Nobody is kissing anybody. I am a professional.')],
                   [('frog', 'Write that I am handsome.', 'capshun', '"[He had a very fine moustache.]"'),
                    ('capshun', '"What\'s your tragic origin, Frog?"', 'frog', 'Swamp. Rent. Next question.')]),
    'collar': ('capshun', 'don', 'The Collar Tag Chronicles', '#e8d29a', 'Mr. Capshun and Donado - an escape story',
               [P('speed'), P('luck')],
               [('don', 'You narrate? Narrate my escape from the mothership. It was very daring.'), ('capshun', '"[It was mostly a door someone left open.]"')],
               [('capshun', '"Donado, in your own words?"', 'don', 'I was magnificent.'),
                ('don', 'Zib says narrators are illegal on our planet.', 'capshun', '"Zib says a lot of things."')]),
    'placement': ('capshun', 'pearl', 'Product Placement', '#5ac8ff', 'Mr. Capshun and Pearlman - this chapter brought to you by Pearlman',
                  [P('luck', 1), P('hero_of_the_village', t=15)],
                  [('pearl', 'A narrator! Mention my shop! Mention my GEMS!'), ('capshun', '"This chapter is brought to you by Pearlman\'s Fine Gems. Sigh."')],
                  [('capshun', '[Mr. Capshun narrates: "The penguin was, once again, selling something."]', 'pearl', 'Everything is for sale, my friend! Even narration!'),
                   ('pearl', 'How much for a starring role?', 'capshun', '"More than you have, Pearlman."')]),
    'gentletale': ('capshun', 'wil', "The Gentle One's Tale", '#f4f4f4', 'Mr. Capshun and Wilfrey - a kind story, for once',
                   [PREGEN, P('resistance')],
                   [('capshun', '"Wilfrey. The grandson who sealed the King away. I\'ve wanted to tell your story for a long time."'), ('wil', 'Tell it kindly. That\'s all I ask.')],
                   [('wil', 'Do you know any happy endings?', 'capshun', '"I\'m working on yours."'),
                    ('capshun', '[Mr. Capshun narrates: "He liked flowers. He liked villagers. He was very, very brave."]', 'wil', '...Thank you.')]),
    'deeper': ('capshun', 'dennis', 'Dig Deeper', '#e0a040', 'Mr. Capshun and Dennis - the plot thickens, the tunnel deepens',
               [P('haste', 1)],
               [('dennis', 'Oi, stick man. You\'re standing on my vein.'), ('capshun', '"[Mr. Capshun narrates: The dwarf was right. He usually is.]"')],
               [('capshun', '"What are you looking for down there, Dennis?"', 'dennis', 'Gold. It\'s always gold.'),
                ('dennis', 'Write that I found a diamond.', 'capshun', '"[He found a lot of gravel.]"')]),
    'butler': ('capshun', 'pistachio', 'The Butler Did It', '#7ae890', 'Mr. Capshun and Pistachio - a mystery',
               [NV, FOES('weakness')],
               [('capshun', '"A ghost butler! Every mystery needs one. Where were you on the night of - "'), ('pistachio', 'Polishing the silver, sir. As I have been for three hundred years.')],
               [('capshun', '"[The butler did it.]"', 'pistachio', 'Did what, sir?'),
                ('pistachio', 'Might you narrate me dusting? It is very satisfying.', 'capshun', '"[He dusted. It was very satisfying.]"')]),
    'epilogue': ('capshun', 'omega', 'Epilogue', '#9fb4ff', 'Mr. Capshun and King Omega - every story ends somewhere',
                 [P('resistance'), UNDEAD_BURN],
                 [('omega', 'A narrator! At last, someone to record my reign. Chapter one: I was MAGNIFICENT.'), ('capshun', '"You were cursed into the dark for three hundred years."')],
                 [('capshun', '"How would you like your story to end, Your Majesty?"', 'omega', 'With a parade. And my brother apologising.'),
                  ('omega', 'Do I have a good side?', 'capshun', '"You\'re a ghost. Both sides are see-through."')]),
    'plotheat': ('capshun', 'ashur', 'Plot Heat', '#ff7a2a', 'Mr. Capshun and Ashur - a paper man and a girl on fire',
                 [P('fire_resistance', t=12), P('strength')],
                 [('ashur', 'Ooh, a paper man! You\'d burn SO well.'), ('capshun', '"Please don\'t. I\'m the only copy."')],
                 [('capshun', '[Mr. Capshun narrates, from a safe distance: "She was fierce. She was fiery."]', 'ashur', 'Come closer and narrate!'),
                  ('ashur', 'Write me a dragon to fight!', 'capshun', '"Budget says one large chicken."')]),
    'recipe': ('capshun', 'chef', 'A Recipe for Adventure', '#ffd07a', 'Mr. Capshun and the Chef - a cookbook, narrated',
               [PREGEN] + EVERY(20, 'snack'),
               [('chef', 'You! Stick man! You are too thin. Eat!'), ('capshun', '"I\'m a drawing, Chef. I\'m supposed to be thin."')],
               [('capshun', '[Mr. Capshun narrates: "Step one: the Chef shouts. Step two: the Chef shouts more."]', 'chef', 'I am not shouting! I am PASSIONATE!'),
                ('chef', 'What is your favourite food, Monsieur Capshun?', 'capshun', '"Ink."')]),
    'lostqueen': ('capshun', 'ava', 'The Lost Queen', '#6ad8e8', 'Mr. Capshun and Queen Ava - her story, told right',
                  [PREGEN, WB],
                  [('capshun', '"Queen Ava. I\'ve told your story wrong before. Let me tell it right."'), ('ava', 'Tell them I loved my daughter. The rest is just history.')],
                  [('ava', 'Do you know how it ends, narrator?', 'capshun', '"Not yet. That\'s the good part."'),
                   ('capshun', '[Mr. Capshun narrates: "The queen of the deep, still keeping watch."]', 'ava', 'Always.')]),
    'gossip': ('capshun', 'pearlq', "The Regent's Gossip", '#5ae0d8', 'Mr. Capshun and Queen Pearl - she has OPINIONS',
               [P('luck'), P('jump_boost')],
               [('pearlq', 'A narrator! Darling! I have SO much gossip.'), ('capshun', '"I\'m going to need more paper."')],
               [('pearlq', 'Put in that I\'m the PRETTY sister.', 'capshun', '"[She insisted she was the pretty sister.]"'),
                ('capshun', '"Any secrets from the council, Your Majesty?"', 'pearlq', 'They think I read the reports. I do NOT read the reports.')]),
    'oldsongs': ('capshun', 'bloo', 'The Beast of the Old Songs', '#5a9ae8', 'Mr. Capshun and Bloo - he will not be narrated',
                 [P('strength', 1), '{B} run ' + S('resistance')],
                 [('capshun', '[Mr. Capshun narrates: "The beast of the deep woods, terrible and blue - "]'), ('bloo', 'Say one more word and I will eat your pencil.')],
                 [('capshun', '"Bloo, about the war - "', 'bloo', 'No.'),
                  ('bloo', 'You draw me with too many teeth.', 'capshun', '"[He had, if anything, more teeth than that.]"')]),
    'horror': ('capshun', 'stalker', 'A Horror Story', '#a8ac70', 'Mr. Capshun and the Stalker - the narrator gets the shivers',
               [NV, FOES('weakness'), FOES('slowness')],
               [('capshun', '[Mr. Capshun narrates, quietly: "It was standing right behind him."]'), ('stalker', '(it is standing right behind him)')],
               [('capshun', '"It doesn\'t talk. It doesn\'t blink. It\'s my favourite."', 'stalker', '(it tilts its head, very slowly)'),
                ('stalker', '(it leans over the narrator\'s shoulder to read the page)', 'capshun', '"Please don\'t do that."')]),
    'spooky': ('capshun', 'lantern', 'A Spooky Tale', '#ff8a2a', 'Mr. Capshun and the Arachno-Lantern - a story for October',
               [P('fire_resistance', t=12), FOES('glowing', t=3, r=10)],
               [('capshun', '"A pumpkin! On legs! It\'s like I wrote it."'), ('lantern', '(it scuttles round him, delighted)')],
               [('capshun', '[Mr. Capshun narrates: "It lit the way with its own eyes. Spooky. Also very practical."]', 'lantern', '(proud embers)'),
                ('lantern', '(it singes the corner of his page)', 'capshun', '"Rude. Accurate, but rude."')]),
    'jaws': ('capshun', 'bones', 'Jaws, but Nice', '#8ab0c8', 'Mr. Capshun and Bones - the scariest grin in the sea',
             [WB, P('dolphins_grace'), 'execute as ' + O + ' at @s if block ~ ~1 ~ minecraft:water run ' + 'effect give @s minecraft:strength 3 0 true'],
             [('capshun', '"Bones! Dun dun. Dun dun. Dun dun dun dun - "'), ('bones', '(he grins. It is a LOT of teeth.)')],
             [('bones', '(he circles the narrator in his water ball)', 'capshun', '"I\'m going to need a bigger page."'),
              ('capshun', '"Bones: misunderstood. Also, tooth-heavy."', 'bones', '(a happy chomp at nothing)')]),
    'retcon': ('capshun', 'pxcecil', 'Retcon', '#b070ff', 'Mr. Capshun and 8-Bit Cecil - the remastered edition',
               [P('haste'), P('luck')],
               [('pxcecil', 'NARRATOR! Read my item description!'), ('capshun', '"[A wizard. Sixteen colours. Mildly grumpy.]"')],
               [('capshun', '"Are you canon?"', 'pxcecil', 'I am the DEFINITIVE edition.'),
                ('pxcecil', 'Your lines are too long for my text box.', 'capshun', '"..."')]),
    'spritework': ('capshun', 'pxleo', 'Sprite Work', '#4ab0ff', 'Mr. Capshun and 8-Bit Leo - one flat hero, and another',
                   [P('resistance'), P('speed')],
                   [('pxleo', 'A fellow flat warrior! Well met!'), ('capshun', '"Finally - someone as thin as I am."')],
                   [('pxleo', 'Narrate my sword! It is very pointy!', 'capshun', '"[It was three pixels long and VERY pointy.]"'),
                    ('capshun', '"Do you ever wish you were 3D?"', 'pxleo', 'Never. I am exactly enough.')]),
    'fanart': ('capshun', 'pxemma', 'Fan Art', '#ff6ac8', 'Mr. Capshun and 8-Bit Emma - she wants to be drawn',
               [PREGEN, P('jump_boost')],
               [('pxemma', 'Mr. Capshun! Draw me! DRAW ME!'), ('capshun', '"You\'re already drawn. Sixteen colours\' worth."')],
               [('pxemma', 'Can I have a cool cape in the sequel?', 'capshun', '"I\'ll talk to the developers."'),
                ('capshun', '[Mr. Capshun narrates: "She hopped. She bounced. She did NOT stop."]', 'pxemma', 'NEVER!')]),

    # ================================================================== and a few more that make sense
    'sharksailor': ('tul', 'bones', 'Shark and Sailor', '#7ab8d8', 'Tullius and Bones - the drowned captain and the shark who didn\'t eat him',
                    [WB, P('dolphins_grace'), P('conduit_power', t=12)],
                    [('tul', 'A shark. The last one I met ate my first mate.'), ('bones', '(he grins at the captain. Very innocently.)')],
                    [('bones', '(he swims round and round Tullius\'s boots)', 'tul', 'Yes, yes. You are terrifying. Good shark.'),
                     ('tul', 'Ever had a captain, shark?', 'bones', '(he bumps Tullius with his nose. Yes. Now.)')]),
    'guardian': ('ava', 'bones', "The Kingdom's Guardian", '#6ad8e8', 'Queen Ava and Bones - the shark who guards the kingdom',
                 [PREGEN, WB, '{B} run ' + S('resistance')],
                 [('ava', 'Bones... you kept her safe, all those years. Thank you.'), ('bones', '(he nuzzles the ghost-queen\'s hand - and goes through it, and doesn\'t mind)')],
                 [('ava', 'Is he still sleeping at the foot of her bed?', 'bones', '(an extremely guilty grin)'),
                  ('bones', '(he circles the queen, guarding)', 'ava', 'Good boy. The kingdom is lucky to have you.')]),
    'predators': ('fishy', 'bones', 'Natural Predators', '#ffa040', 'Fishy and Bones - a goldfish and a shark, keeping their distance',
                  [WB, P('luck')],
                  [('fishy', '(he backs to the far side of his bowl, very slowly)'), ('bones', '(he grins. Fishy does not like the grin.)')],
                  [('bones', '(he licks his lips)', 'fishy', '(a VERY indignant blub)'),
                   ('fishy', '(he raises his hat to the shark, politely, from a distance)', 'bones', '(he raises a fin back)')]),
    'belowstairs': ('chef', 'pistachio', 'Below Stairs', '#c8e890', 'The Chef and Pistachio - the kitchen and the pantry',
                    [REGEN, '{B} run ' + REGEN] + EVERY(20, 'snack'),
                    [('chef', 'A ghost in my pantry! Do you at least keep it tidy?'), ('pistachio', 'Spotless, Chef. For three hundred years.')],
                    [('pistachio', 'The soup, Chef. It wants salt.', 'chef', 'The soup wants NOTHING! ...Pass the salt.'),
                     ('chef', 'You cannot even taste it, ghost!', 'pistachio', 'I remember, sir. That is enough.')]),
    'goldweight': ('dennis', 'pearl', 'Weighed in Gold', '#e8c060', 'Dennis and Pearlman - the dwarf who digs it, the penguin who sells it',
                   [P('haste'), P('luck', 1)],
                   [('pearl', 'Mr Dennis! My favourite supplier!'), ('dennis', 'Your ONLY supplier. And you underpay.')],
                   [('dennis', 'That\'s real gold, that is.', 'pearl', 'And at Pearlman\'s, it\'s on SALE!'),
                    ('pearl', 'Twenty percent off, for friends!', 'dennis', 'Off MY gold?!')]),
    'awayteam': ('zib', 'don', 'The Away Team', '#3ad8c8', 'Zib and Donado - two Donadians, a long way from home',
                 [P('speed'), NV, S('resistance'), B('resistance')],
                 [('zib', 'Donado! Report!'), ('don', 'I am not a trooper, Zib. I am a... collar tag enthusiast.')],
                 [('zib', 'Do you miss the mothership?', 'don', 'Not the holding pen.'),
                  ('don', 'The humans here are kind, Zib.', 'zib', 'They are adequate. ...Fine. Kind.')]),
    'harvestmoon': ('sky', 'lantern', 'Harvest Moon', '#ffb04a', 'the Sky Buddies and the Arachno-Lantern - an autumn night',
                    [NV, P('fire_resistance', t=12)],
                    [('sky', 'Snooze: "...a pumpkin... is it bedtime?..."'), ('lantern', '(it lights a soft glow, just for her)')],
                    [('sky', 'Sunny: "Hey, Lantern! Who shines brighter?"', 'lantern', '(it flares up, very competitively)'),
                     ('lantern', '(it gazes up at the moon)', 'sky', 'Snooze: "...yes... I\'m pretty... go to sleep..."')]),
}
ICON = {k: 'bm:bv_ball' for k, v in PAIRS.items() if v[0] == 'bender'}
ICON.update({k: 'bm:capshun_pencil' for k, v in PAIRS.items() if v[0] == 'capshun'})
ICON.update({'sharksailor': 'bm:bn_whistle', 'guardian': 'bm:av_locket', 'predators': 'bm:fy_bowl', 'belowstairs': 'bm:chef_ladle',
             'goldweight': 'bm:pearl_card', 'awayteam': 'bm:donadian_medal', 'harvestmoon': 'bm:sky_mobile'})
assert not set(PAIRS) & set(P188.PAIRS), set(PAIRS) & set(P188.PAIRS)
P188.PAIRS.update(PAIRS)
P188.ICON.update(ICON)

TRIOS = {   # key: (name, colour, members, advancement title, description)
    'haunting': ('The Haunting', '#c8f0d8', ('omega', 'pistachio', 'wil'), 'The Haunting', 'Walk with King Omega, Pistachio and Wilfrey at once'),
    'tidecourt': ('The Tide Court', '#6ac8e8', ('ava', 'tul', 'bones'), 'The Tide Court', 'Walk with Queen Ava, Tullius and Bones at once'),
    'guild': ('The Market Guild', '#ffcf40', ('pearl', 'dennis', 'pistachio'), 'The Market Guild', 'Walk with Pearlman, Dennis and Pistachio at once'),
}
TICON = {'haunting': 'bm:om_monocle', 'tidecourt': 'bm:av_locket', 'guild': 'bm:pearl_card'}
P100.TRIOS.update(TRIOS)
P100.BANTER.update({
    'haunting': [('King Omega', 'Three ghosts out for a stroll! How delightfully morbid.', 'Pistachio', 'Shall I bring tea, Your Majesty?'),
                 ('Wilfrey', 'Do you ever miss being alive?', 'King Omega', 'Only on Tuesdays.'),
                 ('Pistachio', 'Master Wilfrey, you are dripping ectoplasm on the carpet.', 'Wilfrey', 'There is no carpet, Pistachio.')],
    'tidecourt': [('Queen Ava', 'My captain, and my daughter\'s shark. The court of the tide.', 'Tullius', 'At your command, Majesty.'),
                  ('Bones', '(he swims a slow, proud circle round his queen)', 'Queen Ava', 'Yes, Bones. You may lead the way.'),
                  ('Tullius', 'The shark outranks me now, doesn\'t he.', 'Queen Ava', 'He always did, Captain.')],
    'guild': [('Pearlman', 'The Black Market\'s finest - together! Business is BOOMING!', 'Dennis', 'Business is my back hurting.'),
              ('Pistachio', 'The pantry\'s accounts are balanced, gentlemen.', 'Pearlman', 'Balanced?! We want them PROFITABLE!'),
              ('Dennis', 'Penguin. Ghost. Me. Who\'s minding the shops?', 'Pistachio', 'I left a note, Mr Dennis.')],
})


def extend_offers(O_, offer):
    pass


def generate(G):
    fn, wjson, title, tellraw = G.fn, G.wjson, G.title, G.tellraw
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p219 dummy']
    G.OBJECTIVES += ['bm.p219']
    host = lambda k: P100.WHO[k]
    mine = lambda k: f'@e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..24]'

    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    tick = lambda n: ['scoreboard players add @s bm.p219 1', f'execute if score @s bm.p219 matches {n}.. run scoreboard players set @s bm.p219 0']
    say = lambda who, txt: title(O, 'actionbar', [T(f'{who}: ', P100.VOICE.get(who, ('#ffffff',))[0], bold=True), T(txt, '#f0f0f0')])
    # ---- the pairs' little extras (as the pair's leader, at it; its player tagged bm.p188o)
    fn('p219/snack', [f'execute as {O} run {SNACK}', f'execute at {O} run particle minecraft:item{{item:"minecraft:cooked_beef"}} ~ ~1.4 ~ 0.2 0.1 0.2 0.05 6',
                      f'execute as {O} at @s run playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.6 1.2'])
    fn('p219/biscuit', [f'execute as {O} run {SNACK}', f'execute at {O} run particle minecraft:item{{item:"minecraft:cookie"}} ~ ~1.4 ~ 0.2 0.1 0.2 0.05 6',
                        say('Pistachio', 'A biscuit, sir. One for you - and, discreetly, one for the dog.')])
    fn('p219/cake', [f'execute as {O} run {SNACK}', P('speed', 1, 10), f'execute at {O} run particle minecraft:item{{item:"minecraft:cake"}} ~ ~1.4 ~ 0.2 0.1 0.2 0.05 8',
                     say('Queen Pearl', 'Cake for you, darling - and a slice for the good boy!')])
    fn('p219/embers', ['particle minecraft:flame ~ ~0.6 ~ 1.2 0.3 1.2 0.04 24', 'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.4 1.6',
                       f'execute at {O} as @e[{FOE},distance=..6] run data merge entity @s {{Fire:60s}}'])
    # ---- THE HAUNTING
    fn('p100/haunting', [NV.replace(O, '@s'), 'effect give @s minecraft:resistance 3 0 true', REGEN] + tick(15) +
       ['execute if score @s bm.p219 matches 0 run function bm:p219/rest'] + each(TRIOS['haunting'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p219/rest', ['particle minecraft:soul ~ ~1 ~ 4 1 4 0.04 40', 'particle minecraft:sculk_soul ~ ~1 ~ 3 0.6 3 0.02 20',
                     'playsound minecraft:particle.soul_escape player @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:block.bell.resonate player @a[distance=..16] ~ ~ ~ 0.4 0.6',
                     'execute as @e[type=#minecraft:undead,tag=!bm.npc,distance=..10] run damage @s 12 minecraft:magic',
                     'execute as @e[type=#minecraft:undead,tag=!bm.npc,distance=..10] run data merge entity @s {Fire:60s}'])
    # ---- THE TIDE COURT
    fn('p100/tidecourt', ['effect give @s minecraft:water_breathing 15 0 true', 'effect give @s minecraft:conduit_power 12 0 true',
                          'effect give @s minecraft:dolphins_grace 3 0 true', 'effect give @s minecraft:strength 3 0 true'] + tick(20) +
       ['execute if score @s bm.p219 matches 0 run function bm:p219/wave'] + each(TRIOS['tidecourt'][2], 'effect give @s minecraft:resistance 3 0 true') +
       ['function bm:p100/banter_tick'])
    fn('p219/wave', ['particle minecraft:splash ~ ~0.5 ~ 4 0.3 4 0.3 120', 'particle minecraft:bubble_pop ~ ~0.6 ~ 3 0.4 3 0.1 40',
                     'playsound minecraft:entity.player.splash.high_speed player @a[distance=..16] ~ ~ ~ 1 0.7',
                     f'execute as @e[{FOE},distance=..7] run damage @s 4 minecraft:magic',
                     f'execute as @e[{FOE},distance=..7] at @s facing entity @p feet run tp @s ^ ^0.4 ^-3'])
    # ---- THE MARKET GUILD
    fn('p100/guild', ['effect give @s minecraft:luck 3 1 true', 'effect give @s minecraft:haste 3 1 true', 'effect give @s minecraft:hero_of_the_village 15 0 true'] + tick(60) +
       ['execute if score @s bm.p219 matches 0 run function bm:p219/dividend'] + each(TRIOS['guild'][2], REGEN) + ['function bm:p100/banter_tick'])
    fn('p219/dividend', ['give @s minecraft:emerald 1', 'particle minecraft:happy_villager ~ ~1.2 ~ 0.4 0.5 0.4 0 10',
                         'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 1.4',
                         title('@s', 'actionbar', [T('The Market Guild: ', '#ffcf40', bold=True), T('your cut - an emerald.', '#fff0c0')])])
    for k, (nm, col, mem, at, desc) in TRIOS.items():
        wjson(f'bm/advancement/story/trio_{k}.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': TICON[k]}},
                                                                 'title': T(at, 'yellow'), 'description': T(desc, 'gray'), 'frame': 'goal',
                                                                 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
