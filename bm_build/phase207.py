"""2.93b: BENDER'S BONDS - the goodest boy gets on with nearly everyone (phase188's engine runs the pairs; phase100 finds the
trios and calls p100/<key>, built here).

PAIRS (Bender and ...)
- EMMA, "Princess and Pup": Regeneration and Speed for you; both heal.
- LEO, "Knight and Hound": Strength and Resistance; both tougher.
- CELI, "Snow Dog": Speed II; the foes round you slowed.
- APOPHISS, "Hackles and Scales": Strength II; the foes round you weakened (he does NOT trust the snake).
- DEMOCRATUS, "Storm Dog": Strength and Speed; in the rain, Strength II.
- KILLERWATT, "Fetch!": Speed II and Jump Boost.
- CECIL, "The Wizard's Familiar": Night Vision, Luck and Regeneration.
- THE STALKER, "Something's Out There": Night Vision; every foe round you lit up - he can smell them.
- MR. CAPSHUN, "A Dog in Pencil": Luck II and Jump Boost.
- FISHY, "Not for Eating": Water Breathing, Dolphin's Grace and Luck.
- PEARLMAN, "Best Customer": Hero of the Village and Luck.
TRIOS
- EMMA, LEO AND BENDER, "The Royal Guard Dog": Resistance II, Strength and Regeneration; every 20 s Bender barks the foes
  round you down (weakened, slowed, lit up); Leo and Bender tougher.
- LEO, CELI AND BENDER, "The Winter Patrol": Speed II and Resistance; the foes round you slowed II; Leo and Bender tougher.
- KILLERWATT, DEMOCRATUS AND BENDER, "Storm Hounds": Strength II and Speed; every 12 s lightning finds two foes round you.
- CECIL, PISTACHIO AND BENDER, "The Wizard's Household": Regeneration, Night Vision, Luck II and four more hearts.
- APOPHISS, OMEGA AND BENDER, "The Kings' Hound": Strength II and Resistance; the foes round you wither.
- MR. CAPSHUN, FISHY AND BENDER, "Imaginary Friends": Luck II, Jump Boost II, Speed and Regeneration."""
import phase100 as P100
import phase188 as P188

FOE = 'type=#bm:hostile,tag=!bm.npc'
O = P188.O
REGEN = P188.REGEN
B = 'bender'


def _pair(k, b, name, col, desc, buff, intro, banter):
    P188.PAIRS[k] = (B, b, name, col, desc, buff, intro, banter)
    P188.ICON[k] = 'bm:bv_ball'


_pair('pup', 'emma', 'Princess and Pup', '#ff8ad8', 'Bender and Emma - a princess and the goodest boy',
      [f'execute as {O} run {REGEN}', f'effect give {O} minecraft:speed 3 0 true', REGEN, '{B} run ' + REGEN],
      [('Emma', 'A PUPPY! Who\'s a good boy? Who\'s the BEST boy?'), ('Bender', '(he flops over at her feet, belly up, tail thumping)')],
      [('Emma', 'Bender, sit! ...Bender, that\'s lying down.', 'Bender', '(it is lying down. It is a very good lie down.)'),
       ('Bender', '(he brings her a stick twice his size)', 'Emma', 'For ME? Bender, it\'s beautiful.')])
_pair('hound', 'leo', 'Knight and Hound', '#5ab8e0', 'Bender and Leo - every knight needs a hound',
      [f'effect give {O} minecraft:strength 3 0 true', f'effect give {O} minecraft:resistance 3 0 true',
       'effect give @s minecraft:resistance 3 0 true', '{B} run effect give @s minecraft:resistance 3 0 true'],
      [('Leo', 'A hound! A proper hound. Heel, lad.'), ('Bender', '(he heels. Perfectly. Then licks the knight\'s gauntlet.)')],
      [('Leo', 'He keeps watch better than half the palace guard.', 'Bender', '(ears up, staring hard at a bush)'),
       ('Bender', '(he barks at Leo\'s reflection in his own shield)', 'Leo', 'Yes, that one is also me.')])
_pair('snowdog', 'celi', 'Snow Dog', '#9ad8ff', 'Bender and Celi - zoomies in the snow',
      [f'effect give {O} minecraft:speed 3 1 true', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:slowness 3 0'],
      [('Celi', 'Ugh, a dog. Is it going to slobber on me?'), ('Bender', '(he slobbers on her)')],
      [('Celi', 'Fine. FINE. He can stay. He\'s warm.', 'Bender', '(he leans on her, happily)'),
       ('Bender', '(he eats a snowball she threw at him)', 'Celi', '...That was meant for your head, dog.')])
_pair('hackles', 'apo', 'Hackles and Scales', '#3ad06a', 'Bender and Apophiss - the dog does not trust the snake',
      [f'effect give {O} minecraft:strength 3 1 true', f'execute at @s run effect give @e[{FOE},distance=..8] minecraft:weakness 3 0'],
      [('Bender', '(a low, rumbling growl, hackles all the way up)'), ('Apophiss', 'Hsss. The small beast does not like me.')],
      [('Apophiss', 'I could swallow you whole, little dog.', 'Bender', '(he stands between the serpent and you, and does not move)'),
       ('Bender', '(he growls at the serpent\'s tail)', 'Apophiss', 'It is attached to me. Leave it.')])
_pair('stormdog', 'demo', 'Storm Dog', '#7ad06a', 'Bender and Democratus - the old general and the dog who isn\'t scared of thunder',
      [f'effect give {O} minecraft:strength 3 0 true', f'effect give {O} minecraft:speed 3 0 true',
       f'execute as {O} if predicate bm:p29/raining run effect give @s minecraft:strength 3 1 true'],
      [('Democratus', 'A dog that does not flinch at thunder. You and I will get along.'), ('Bender', '(he sits beside the scythe, very proud)')],
      [('Democratus', 'I had hounds, once. A thousand years ago.', 'Bender', '(he puts his head on the old man\'s knee)'),
       ('Bender', '(he barks at the lightning)', 'Democratus', 'Yes. It answers to me, not you. Good try.')])
_pair('fetch', 'kw', 'Fetch!', '#74d462', 'Bender and KillerWatt - the fastest, cruellest game of fetch in the world',
      [f'effect give {O} minecraft:speed 3 1 true', f'effect give {O} minecraft:jump_boost 3 0 true'],
      [('KillerWatt', '*a tendril snaps a stick a quarter of a mile into the dark - not for the dog. To watch him run.*'), ('Bender', '(he is GONE)')],
      [('Bender', '(he brings back the stick, faintly smoking)', 'KillerWatt', '*he throws it again. Further. And again, until the dog is panting.*'),
       ('KillerWatt', '*his current creeps toward the dog - Bender growls, hackles up, and it pulls back*', 'Bender', '(he does not turn his back on him. Ever.)')])
_pair('familiar', 'cecil', "The Wizard's Familiar", '#b48cff', 'Bender and Cecil - every wizard needs a familiar; this one\'s a dog',
      [f'effect give {O} minecraft:night_vision 15 0 true', f'effect give {O} minecraft:luck 3 0 true', f'execute as {O} run {REGEN}'],
      [('Cecil', 'Traditionally a familiar is a cat. Or a raven.'), ('Bender', '(he wags so hard he falls over)')],
      [('Cecil', 'He ate a page of my spellbook.', 'Bender', '(he hiccups a small purple spark)'),
       ('Bender', '(he sniffs the staff\'s gem, sneezes)', 'Cecil', 'Bless you. Please don\'t do that again.')])
_pair('outthere', 'stalker', "Something's Out There", '#a8ac70', 'Bender and the Stalker - he can smell what\'s hiding in the dark',
      [f'effect give {O} minecraft:night_vision 15 0 true', f'effect give @e[{FOE},distance=..12] minecraft:glowing 3 0'],
      [('Bender', '(he stares at the Stalker. The Stalker stares back. His tail wags, very slowly.)'), ('The Stalker', '(it pats his head, joint by joint)')],
      [('Bender', '(he growls at the dark - and the dark shows its eyes)', 'The Stalker', '(its head turns, all the way round, to look)'),
       ('The Stalker', '(it crouches low beside the dog, very still)', 'Bender', '(he crouches too. They wait together.)')])
_pair('pencil', 'capshun', 'A Dog in Pencil', '#f0f0f0', 'Bender and Mr. Capshun - the narrator meets a very good boy',
      [f'effect give {O} minecraft:luck 3 1 true', f'effect give {O} minecraft:jump_boost 3 0 true'],
      [('Mr. Capshun', '"And then, a dog appeared. A very good dog. The best dog, frankly."'), ('Bender', '(he licks the stick figure. It smudges.)')],
      [('Mr. Capshun', '"He tried to bury my pencil. I let him. It\'s character development."', 'Bender', '(proud)'),
       ('Bender', '(he barks at Mr. Capshun\'s shadow, which is also flat)', 'Mr. Capshun', '"It\'s fine. Everyone does that the first time."')])
_pair('noteating', 'fishy', 'Not for Eating', '#ffa040', 'Bender and Fishy - he has been told the fish is a friend',
      [f'effect give {O} minecraft:water_breathing 15 0 true', f'effect give {O} minecraft:dolphins_grace 3 0 true', f'effect give {O} minecraft:luck 3 0 true'],
      [('Bender', '(he presses his nose to the bowl. It fogs up.)'), ('Fishy', '(a nervous blub)')],
      [('Fishy', '(he swims a little circle; the dog\'s head follows it round)', 'Bender', '(he licks the glass. Gently. Friend.)'),
       ('Bender', '(he sits by the bowl, guarding it)', 'Fishy', '(a grateful blub)')])
_pair('customer', 'pearl', 'Best Customer', '#e8f2ff', 'Bender and Pearlman - a penguin who sells things and a dog who digs them up',
      [f'effect give {O} minecraft:hero_of_the_village 3 0 true', f'effect give {O} minecraft:luck 3 0 true'],
      [('Pearlman', 'A DOG! Does the dog have money? The dog has a BONE. Pearlman accepts bones!'), ('Bender', '(he drops a very wet bone on the counter)')],
      [('Pearlman', 'He dug up a diamond! Pearlman will buy it! For one biscuit!', 'Bender', '(he accepts. He is a very bad negotiator.)'),
       ('Bender', '(he chases the penguin\'s waddle)', 'Pearlman', 'Pearlman is NOT a ball! ...Pearlman is a little bit flattered.')])

TRIOS = {
    'guarddog': ('The Royal Guard Dog', '#ffc06a', ('emma', 'leo', B), 'The Royal Guard Dog', 'Walk with Emma, Leo and Bender at once'),
    'patrol': ('The Winter Patrol', '#9ad8ff', ('leo', 'celi', B), 'The Winter Patrol', 'Walk with Leo, Celi and Bender at once'),
    'hounds': ('Storm Hounds', '#8ae070', ('kw', 'demo', B), 'Storm Hounds', 'Walk with KillerWatt, Democratus and Bender at once'),
    'household2': ("The Wizard's Household", '#b48cff', ('cecil', 'pistachio', B), "The Wizard's Household", 'Walk with Cecil, Pistachio and Bender at once'),
    'kingshound': ("The Kings' Hound", '#5ad08a', ('apo', 'omega', B), "The Kings' Hound", 'Walk with Apophiss, King Omega and Bender at once'),
    'imaginary': ('Imaginary Friends', '#f0f0f0', ('capshun', 'fishy', B), 'Imaginary Friends', 'Walk with Mr. Capshun, Fishy and Bender at once'),
}
P100.TRIOS.update(TRIOS)
P100.BANTER.update({
    'guarddog': [('Emma', 'Leo, Bender is a knight now. I knighted him. With a carrot.', 'Leo', 'Sir Bender. ...He will outrank me by spring.'),
                 ('Leo', 'Heel, Sir Bender.', 'Bender', '(he heels beside Emma instead. Leo sighs.)'),
                 ('Bender', '(he barks once at the dark, and the knight\'s hand goes to his sword)', 'Leo', 'Good lad. I see it too.')],
    'patrol': [('Celi', 'Why is the dog faster than me in the snow? I LIVE in the snow.', 'Leo', 'Four legs, Celi.'),
               ('Bender', '(he bounds through a snowdrift and vanishes completely)', 'Celi', 'Ha! ...Leo. Leo, where did he go.'),
               ('Leo', 'Patrol formation. Bender on point.', 'Bender', '(he is already twenty blocks ahead)')],
    'hounds': [('Democratus', 'Three of us who do not fear the storm.', 'KillerWatt', '*sparks crawl toward the dog\'s fur - and the scythe comes down between them*'),
               ('Bender', '(he barks at the sky; the sky barks back)', 'Democratus', 'Ha! The storm likes him.'),
               ('KillerWatt', '*he crouches low beside Bender, watching the dark - watching the dog more*', 'Democratus', 'Eyes on the enemy, beast. Not the hound.')],
    'household2': [('Pistachio', 'Master Cecil, the dog has tracked mud across the entire palace.', 'Cecil', 'He\'s family now, Pistachio. Family tracks mud.'),
                   ('Bender', '(he chases the ghost butler\'s coat-tails, straight through him)', 'Pistachio', 'Most undignified. ...Good boy.'),
                   ('Cecil', 'Pistachio, could you conjure him a bone?', 'Pistachio', 'I could conjure him a ham, sir. He has earned a ham.')],
    'kingshound': [('Omega', 'Every king needs a hound! Apophiss, look at his little EARS.', 'Apophiss', 'I am looking. He is growling at me.'),
                   ('Bender', '(he sits between the two kings, very straight)', 'Omega', 'He thinks he is keeping the peace. Perhaps he is.'),
                   ('Apophiss', 'Fine. The small beast may stay.', 'Bender', '(he licks the serpent\'s claw once, quickly, then pretends he didn\'t)')],
    'imaginary': [('Mr. Capshun', '"A stick figure, a fish and a dog walk into a story..."', 'Fishy', '(a delighted blub)'),
                  ('Bender', '(he tries to fetch the narrator\'s pencil)', 'Mr. Capshun', '"No! That\'s how I MAKE things. ...Okay, one throw."'),
                  ('Fishy', '(he blows a bubble at the dog)', 'Bender', '(he catches it. It pops. He is astonished.)')],
})


def extend_offers(O_, offer):
    pass


def generate(G):
    fn = G.fn
    host = lambda k: P100.WHO[k]
    mine = lambda k: f'@e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..24]'

    def each(mem, cmd):
        return [f'execute as {mine(m)} if function bm:p100/is_mine run {cmd}' for m in mem]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p207 dummy']
    G.OBJECTIVES += ['bm.p207']
    tick = lambda n: ['scoreboard players add @s bm.p207 1', f'execute if score @s bm.p207 matches {n}.. run scoreboard players set @s bm.p207 0']
    hb2 = 'execute unless predicate bm:p100/hb run effect give @s minecraft:health_boost 15 1 true'
    fn('p100/guarddog', ['effect give @s minecraft:resistance 3 1 true', 'effect give @s minecraft:strength 3 0 true', REGEN] + tick(20) +
       ['execute if score @s bm.p207 matches 0 run function bm:p207/bark'] +
       each(('leo', B), 'effect give @s minecraft:resistance 3 1 true') + ['function bm:p100/banter_tick'])
    fn('p207/bark', [f'execute at {mine(B)} run particle minecraft:note ~ ~1.2 ~ 0.6 0.3 0.6 1 6',
                     f'execute at {mine(B)} run playsound minecraft:entity.wolf.ambient neutral @a[distance=..24] ~ ~ ~ 1.2 0.9',
                     f'effect give @e[{FOE},distance=..10] minecraft:weakness 5 0', f'effect give @e[{FOE},distance=..10] minecraft:slowness 5 1',
                     f'effect give @e[{FOE},distance=..10] minecraft:glowing 5 0'])
    fn('p100/patrol', ['effect give @s minecraft:speed 3 1 true', 'effect give @s minecraft:resistance 3 0 true',
                       f'effect give @e[{FOE},distance=..8] minecraft:slowness 3 1'] +
       each(('leo', B), 'effect give @s minecraft:resistance 3 1 true') + ['function bm:p100/banter_tick'])
    fn('p100/hounds', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:speed 3 0 true'] + tick(12) +
       [f'execute if score @s bm.p207 matches 0 as @e[{FOE},distance=..12,sort=random,limit=2] at @s run function bm:p192/bolt', 'function bm:p100/banter_tick'])
    fn('p100/household2', [REGEN, 'effect give @s minecraft:night_vision 15 0 true', 'effect give @s minecraft:luck 3 1 true', hb2,
                           'function bm:p100/banter_tick'])
    fn('p100/kingshound', ['effect give @s minecraft:strength 3 1 true', 'effect give @s minecraft:resistance 3 0 true',
                           f'effect give @e[{FOE},distance=..8] minecraft:wither 3 0', 'function bm:p100/banter_tick'])
    fn('p100/imaginary', ['effect give @s minecraft:luck 3 1 true', 'effect give @s minecraft:jump_boost 3 1 true', 'effect give @s minecraft:speed 3 0 true',
                          REGEN, 'function bm:p100/banter_tick'])
