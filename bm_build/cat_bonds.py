"""2.97: HENRY AND NIA'S BONDS - like Bender and Mr. Capshun, the two cats have a pair with everyone (phase188 runs the pairs, and
phase100 the trios; the owner's list of trios is below). Cats don't talk: their side of every exchange is what they do.

Each character: (Henry's pair: name, the buffs, the other's line, Henry's answer; Nia's pair: the same). The buffs are (effect,
amplifier) for you, three seconds at a time while the two are together. NIA AND EMMA and NIA AND QUEEN AVA are her special pairs
(the owner's own): they do more - see SPECIAL."""

HENRY_C, HENRY_LINE = '#9a9ab8', '#d8d8ec'
NIA_C, NIA_LINE = '#e0a050', '#f6dcb8'

B = {
    'emma': (('Midnight Tea Party', (('regeneration', 0), ('luck', 0)), '"A black cat! Is that good luck or bad luck?"', '(Henry sits on her foot. Good luck, then.)'),
             ("The Princess's Kitty", (('regeneration', 1), ('absorption', 0)), '"NIA! Come here, come here, come HERE - oh, she came."', '(Nia climbs into her lap and starts to purr like a little engine)')),
    'celi': (('Cold Paws', (('fire_resistance', 0), ('speed', 0)), '"Your paws are freezing. Come here, then."', '(Henry tucks in under her cloak)'),
             ('Snow Angel', (('regeneration', 0), ('resistance', 0)), '"A tortoiseshell. All the colours of autumn - in winter."', '(Nia bats a snowflake out of the air)')),
    'zib': (('Unidentified Feline Object', (('night_vision', 0), ('speed', 0)), '"Small black creature! Specimen! May I scan you?"', '(Henry swats the scanner)'),
            ('Close Encounter', (('luck', 0), ('jump_boost', 0)), '"Your colours are not in my databanks. Beautiful."', '(Nia sniffs his antenna and sneezes)')),
    'cecil': (("The Wizard's Familiar", (('night_vision', 0), ('haste', 0)), '"Every wizard needs a black cat. It\'s in the rules."', '(Henry settles on his shoulder like he\'s always been there)'),
              ('Spellbound', (('regeneration', 0), ('haste', 0)), '"Careful, little one - that\'s a spellbook, not a bed."', '(Nia lies down on the spellbook)')),
    'kw': (('Static Cling', (('speed', 1),), '"Ha! Your fur stands right up when I\'m near!"', '(Henry, puffed up to twice his size, is not amused)'),
           ('Shocking Cuteness', (('speed', 0), ('regeneration', 0)), '"I\'ll keep the sparks down for you, kitty."', '(Nia rubs against his leg anyway - zap - and keeps purring)')),
    'leo': (("The Knight's Mouser", (('strength', 0), ('resistance', 0)), '"A guard cat. Very well - stand watch with me."', '(Henry stands watch. With his eyes shut.)'),
            ("Sir Leo's Shadow", (('resistance', 0), ('regeneration', 0)), '"She follows me everywhere. I do not mind."', '(Nia walks exactly in his footsteps)')),
    'demo': (('Omen', (('strength', 0), ('night_vision', 0)), '"A black cat crossing my path. How fitting."', '(Henry crosses it again, just to be sure)'),
             ('Soft Spot', (('regeneration', 0), ('strength', 0)), '"...Do not tell anyone the Reaper pets cats."', '(Nia headbutts his scythe hand until he does)')),
    'apo': (('Serpent and Shadow', (('strength', 0), ('night_vision', 0)), '"A creature of the dark. I approve."', '(Henry watches his tail swish, very, very closely)'),
            ('Coiled Up', (('resistance', 0), ('regeneration', 0)), '"She sleeps in my coils. Nothing else dares."', '(Nia, curled up in a loop of serpent, is fast asleep)')),
    'tul': (("Ship's Cat", (('water_breathing', 0), ('dolphins_grace', 0)), '"Every good ship has a black cat aboard. For luck."', '(Henry eyes the sea, then Tullius, with deep suspicion)'),
            ('Calm Waters', (('water_breathing', 0), ('regeneration', 0)), '"Hm. She doesn\'t mind the cold. Good sailor."', '(Nia sits on his coat and refuses to move)')),
    'frog': (('Croak and Whisker', (('jump_boost', 1),), '"Ribbit."', '(Henry\'s tail twitches. He is thinking about it.)'),
             ('Pond Friends', (('jump_boost', 0), ('regeneration', 0)), '"Ribbit?"', '(Nia pats the Frog gently on the head with one paw)')),
    'don': (('Space Cat', (('speed', 0), ('luck', 0)), '"A cat! On Earth, you are the true rulers, yes?"', '(Henry does not deny it)'),
            ('Collar Tags', (('luck', 0), ('regeneration', 0)), '"We both have tags! We are a matching set."', '(Nia\'s bell jingles; Donado\'s tag clinks. She seems pleased.)')),
    'pearl': (('Black Market Cat', (('luck', 1),), '"Ah, a black cat! Very good for business. Very, very good."', '(Henry inspects the merchandise)'),
              ('Window Shopping', (('luck', 0), ('hero_of_the_village', 0)), '"For you, little miss - first pick of the ribbons, free."', '(Nia picks a ribbon and lies on it)')),
    'wil': (('Gentle Giants', (('regeneration', 0), ('resistance', 0)), '"A small friend. I will carry you, if you like."', '(Henry rides on his shield, very regally)'),
            ('Bone Warmer', (('regeneration', 1),), '"She is warm. I have not been warm in a very long time."', '(Nia curls up against his ribs and purrs)')),
    'fishy': (('Natural Enemies', (('water_breathing', 0), ('luck', 0)), '"I say, keep that BEAST away from my bowl!"', '(Henry stares at the bowl. Unblinking.)'),
              ('An Unlikely Truce', (('water_breathing', 0), ('regeneration', 0)), '"She... she is only looking, yes? Only looking?"', '(Nia boops the bowl with her nose and walks away. Truce.)')),
    'dennis': (('Mine Cat', (('haste', 0), ('night_vision', 0)), '"Cats in the mine keep the rats down. No offence to the market."', '(Henry vanishes down a tunnel and comes back very dusty)'),
               ('Lantern Light', (('haste', 0), ('regeneration', 0)), '"She likes the lantern. Sits right by it, every time."', '(Nia warms herself by the lantern, eyes half shut)')),
    'pistachio': (('Ghost Cat', (('night_vision', 0), ('speed', 0)), '"Shall I fetch the gentleman a saucer of cream, sir?"', '(Henry accepts the saucer. Henry accepts everything.)'),
                  ('Afternoon Cream', (('regeneration', 0), ('luck', 0)), '"Milk for the little lady. Warmed, of course."', '(Nia laps it up, then washes her whiskers)')),
    'omega': (("The King's Shadow", (('resistance', 0), ('night_vision', 0)), '"Even a king of ghosts keeps a cat."', '(Henry walks straight through his ghostly hand. Unbothered.)'),
              ('Royal Lap', (('resistance', 0), ('regeneration', 0)), '"She sits on my throne when I rise from it. I allow this."', '(Nia is, at this moment, sitting on his throne)')),
    'ashur': (('Warm Spot', (('fire_resistance', 0), ('strength', 0)), '"Careful, kitty - I\'m hot stuff."', '(Henry sits exactly as close to her as is warm, and no closer)'),
              ('Hearthside', (('fire_resistance', 0), ('regeneration', 0)), '"Aww, she likes the warmth! Come here, toasty."', '(Nia stretches out in front of her like she\'s a fireplace)')),
    'chef': (('Kitchen Cat', (('saturation', 0), ('strength', 0)), '"OUT of my kitchen, you - oh, fine. One fish."', '(Henry takes two)'),
             ('Taste Tester', (('saturation', 0), ('regeneration', 0)), '"For the little lady - a morsel of salmon, en croute!"', '(Nia eats the salmon and leaves the croute)')),
    'neighbor': (('Night Music', (('speed', 0), ('night_vision', 0)), '"A black cat and a moonlit melody. Perfect."', '(Henry yowls along. Off key.)'),
                 ('Lullaby', (('regeneration', 1),), '"Shh - she\'s falling asleep. Something soft, then."', '(Nia dozes off to the music, paws twitching)')),
    'ava': (('Royal Mouser', (('water_breathing', 0), ('resistance', 0)), '"A guardian for the palace halls. Welcome, dark one."', '(Henry bows. Sort of. He stretches.)'),
            ("The Queen's Companion", (('water_breathing', 0), ('dolphins_grace', 0), ('regeneration', 1)), '"Nia. Come, sweet one - sit with me a while."',
             '(Nia settles beside the Queen, and the water round them glows softly)')),
    'pearlq': (('Spoiled Cat', (('luck', 0), ('regeneration', 0)), '"A kitty! I\'ll have cake brought for him at once!"', '(Henry does not want cake. Henry eats the cake.)'),
               ('Palace Pets', (('luck', 0), ('regeneration', 0)), '"Look at her colours - she\'s like a little autumn!"', '(Nia accepts a velvet cushion as her due)')),
    'bloo': (('Prowlers', (('strength', 0), ('speed', 0)), '(Bloo sniffs Henry. Henry sniffs Bloo. Mutual respect.)', '(Henry flicks his tail once: approved)'),
             ('Big and Small', (('strength', 0), ('regeneration', 0)), '(Bloo lies down very carefully so as not to squash her)', '(Nia curls up in his fur)')),
    'stalker': (('Things in the Dark', (('night_vision', 0), ('strength', 0)), '(The Stalker unfolds from the dark. Henry does not blink.)', '(Henry yawns at it. Nothing scares Henry.)'),
                ('Unafraid', (('night_vision', 0), ('regeneration', 0)), '(The Stalker crouches, very still, as she sniffs it)', '(Nia decides it is a friend, and rubs against it)')),
    'lantern': (('Jack and the Cat', (('fire_resistance', 0), ('night_vision', 0)), '(The Arachno-Lantern\'s glow flickers down at him)', '(Henry sits in the pool of its light like a moth that\'s also a cat)'),
                ('Warm Glow', (('fire_resistance', 0), ('regeneration', 0)), '(It lowers its glowing face to look at her)', '(Nia bats gently at one of its legs)')),
    'bender': (('Cats and Dogs', (('speed', 1),), '(Bender bows, tail going, butt in the air - PLAY?)', '(Henry bops him on the nose. Game on.)'),
               ('Best Friends', (('speed', 0), ('regeneration', 0)), '(Bender lies down so Nia can climb on him)', '(Nia climbs on, turns round three times, and settles)')),
    'bones': (('Shark Bait', (('water_breathing', 0), ('strength', 0)), '(Bones grins at Henry with every one of his teeth)', '(Henry grins back with every one of his)'),
              ('Gentle Jaws', (('water_breathing', 0), ('regeneration', 0)), '(Bones nudges her very, very gently with his nose)', '(Nia rubs her cheek on his fin)')),
    'capshun': (('The Black Cat', (('luck', 0), ('night_vision', 0)), '[Mr. Capshun narrates: "Enter: a black cat. Ominous music plays."]', '(Henry sits on the script)'),
                ('A Happy Ending', (('regeneration', 0), ('luck', 0)), '"[Mr. Capshun narrates: \'And the little tortoiseshell was loved, always.\']"', '(Nia purrs at him, and he has to stop narrating for a moment)')),
    'pxcecil': (('8-Bit Familiar', (('night_vision', 0), ('haste', 0)), '"A PIXEL CAT! ...Oh, you\'re a real one. Still counts!"', '(Henry walks across his screen)'),
                ('Save Point', (('regeneration', 0), ('haste', 0)), '"She\'s like a save point. Everything\'s okay when she\'s here."', '(Nia sits down. The game is saved.)')),
    'pxleo': (('Pixel Pounce', (('strength', 0), ('speed', 0)), '"A boss? No - a cat! An even bigger challenge!"', '(Henry pounces on his sword)'),
              ('Extra Life', (('regeneration', 0), ('resistance', 0)), '"With her around, I swear I have a 1-UP."', '(Nia\'s bell jingles like a coin)')),
    'pxemma': (('Player Cat', (('speed', 0), ('jump_boost', 0)), '"KITTY! He\'s my player two now!"', '(Henry is player one, actually)'),
               ('Pixel Purrs', (('regeneration', 0), ('jump_boost', 0)), '"NIA!!! She\'s the cutest sprite in the whole game!"', '(Nia blinks slowly at her: a cat kiss)')),
    'sky': (('Cloud Chaser', (('slow_falling', 0), ('speed', 0)), 'Sunny: "Black cat, sunny day - perfect!" Nimbus: ":3"', '(Henry swipes at a cloud. Nimbus makes it rain on him.)'),
            ('Starlight Nap', (('slow_falling', 0), ('regeneration', 0)), 'Twinkle: "We\'ll keep the stars out for you, Nia." Nimbus: ":3"', '(Nia watches the stars, and purrs)')),
    'kettle': (('Hide and Seek', (('speed', 0), ('jump_boost', 0)), '"Kitty! Wanna play hide and seek? You\'re it!"', '(Henry is very good at hiding. Kettle never finds him.)'),
               ('Yarn Ball', (('speed', 0), ('regeneration', 0)), '"I made you a yarn ball out of my rope! ...Mostly my rope."', '(Nia chases the yarn ball, and Kettle chases Nia)')),
    'rufus': (('Cat and Mouse', (('luck', 0), ('strength', 0)), '"Easy, big fella. We\'re on the same side. Same side!"', '(Henry stares at him. Licks his lips. Looks away.)'),
              ('Truce', (('luck', 0), ('regeneration', 0)), '"...She\'s not going to eat me, is she, boss?"', '(Nia lies down next to him and purrs. He relaxes. A little.)')),
    'gem': (('Shiny Thing', (('luck', 1),), '(the Gem hovers just out of reach: :3)', '(Henry bats at it. And bats at it. And bats at it.)'),
            ('Twinkle', (('regeneration', 0), ('luck', 0)), '(the Gem floats down to her level: c:)', '(Nia boops it with her nose; it giggles in colours)')),
    'batty': (('Night Hunters', (('night_vision', 0), ('strength', 0)), '"A cat. Great. Just don\'t get ideas, furball."', '(Henry has ideas.)'),
              ('Upside Down', (('slow_falling', 0), ('regeneration', 0)), '"...Hey there, little one. I don\'t bite. Not cats, anyway."', '(Nia sniffs his wing and decides he\'s fine)')),
    'eggbert': (('Nest Egg', (('resistance', 0), ('strength', 0)), '"Easy, kitty. I\'m NOT a toy."', '(Henry rolls him over anyway)'),
                ('Warm Spot', (('resistance', 0), ('regeneration', 0)), '"She\'s... sitting on me. Like a hen. I don\'t hate it."', '(Nia is keeping Eggbert warm)')),
    'count': (('The Count\'s Cat', (('strength', 0), ('luck', 0)), '"A black cat! How dreadfully gothic. I approve."', '(Henry sits in the Count\'s hat)'),
              ('Afternoon Tea', (('regeneration', 0), ('resistance', 0)), '"Would the lady care for a saucer of milk?"', '(the lady would)')),
    # (2.97) the Doodles, the Lightbringer, the Pale Dryad
    'dragon': (('Dragon and Cat', (('fire_resistance', 0), ('strength', 0)), '"RAWR! ...why isn\'t he scared? Everybody\'s scared of dragons."', '(Henry yawns. He is a black cat. He fears nothing.)'),
               ('Tail Warmer', (('regeneration', 0), ('fire_resistance', 0)), '"She\'s sleeping on my tail! It\'s warm! Don\'t move!"', '(Nia curls up on the dragon\'s warm tail and purrs)')),
    'eraser': (('Cat and Mouse', (('speed', 0), ('luck', 0)), '"P-please don\'t bat me around. I\'m not a mouse. I\'m an eraser."', '(Henry bats it around, very gently)'),
               ('Soft Paws', (('regeneration', 0), ('resistance', 0)), '"She\'s not scared of me? Nobody\'s not scared of me."', '(Nia sniffs the Eraser, and licks off a pink crumb)')),
    'cursor': (('The Red Dot', (('speed', 1),), '"Want to chase the pointer, Henry?"', '(Henry crouches. His tail twitches. He POUNCES. He misses. He pretends he didn\'t.)'),
               ('Gentle Click', (('regeneration', 0), ('haste', 0)), '"*click* ...she purred! She purrs when I click!"', '(Nia head-bumps the pointer, purring)')),
    'inkblot': (('Black on Black', (('night_vision', 0), ('strength', 0)), '(the Ink Blot turns into a little black cat, too)', '(Henry stares at it. It stares back. Two black cats.)'),
                ('Inky Paws', (('regeneration', 0), ('luck', 0)), '(it shapes itself into a ball of yarn)', '(Nia bats it, delighted, and gets ink on her paw)')),
    'speech': (('MEOW!', (('strength', 0), ('speed', 0)), '"MEOW! ...that\'s what he SHOULD say. He just looks at me."', '(Henry just looks at it)'),
               ('Purr Caption', (('regeneration', 0), ('absorption', 0)), '"*purr purr purr* - I\'m captioning her! She\'s very happy!"', '(Nia purrs louder, as if on cue)')),
    'lightbringer': (('Blessed Shadow', (('night_vision', 0), ('resistance', 0)), '"Even a black cat is welcome in the light, little one."', '(Henry sits in her light and, slowly, blinks)'),
                     ('Angel Kitty', (('regeneration', 1),), '"Oh, sweet one. The Divine One made you very well."', '(Nia winds round her robe, purring, in a halo of gold)')),
    'dryad': (('Mushroom Prowl', (('night_vision', 0), ('speed', 0)), '"Shh, Henry - the mushrooms are sleeping!"', '(Henry sniffs a glowing mushroom. It glows brighter. He is suspicious of it.)'),
              ('Moss Nap', (('regeneration', 1),), '"She can nap in my moss! It\'s the softest moss."', '(Nia kneads the moss, and falls asleep in a ring of glowing mushrooms)')),
    'sovereign': (('Two Shadows', (('night_vision', 0), ('strength', 0)), '"...a small dark thing that does not fear me. Sit, then."', '(Henry sits on its sabaton. It does not move for an hour.)'),
                  ('Warm Iron', (('regeneration', 1),), '"She is... purring. At me. Why?"', '(Nia curls up in the crook of its gauntlet, and it holds very, very still)')),
    'vexis': (('Two Hunters', (('night_vision', 0), ('speed', 0)), '"He hunts the small things, as I hunted worlds. His is the better hunt."', '(Henry bats at its gravity ring. The ring, very gently, bats back.)'),
              ('Orbit', (('regeneration', 1),), '"She is orbiting me. I have never been orbited."', '(Nia curls up inside its gravity ring, and it floats her an inch off the ground, purring)')),
    'mireling': (('Puddle Prowl', (('night_vision', 0), ('speed', 0)), '(its eye peeks out of the puddle at him, very wide)', '(Henry pats the puddle. The puddle pats back. Henry is not sure about this.)'),
                 ('Warm Puddle', (('regeneration', 1),), '(it sinks low and still, so she can curl up on the warm mound of it)', '(Nia kneads it, and falls asleep on the Mireling, purring)')),
    'keeper': (('Loose Thread', (('luck', 0), ('speed', 0)), '"Ah - you have found my loose thread. Yes, you may have it."', '(Henry bats the thread. The thread, very gently, bats back.)'),
               ('Warm Lap', (('regeneration', 1),), '(it kneels, and spreads its robe for her like a blanket)', '(Nia curls up in the rainbow folds of it, purring, among the motes)')),
}
# (2.96c) Nia is the gentle one - a support follower: her side of every pair looks after you. Each keeps Regeneration, and
# nothing of hers makes you hit harder (Strength becomes Resistance; Haste, Absorption)
_SOFT = {'strength': 'resistance', 'haste': 'absorption'}
for _w, (_h, (_nn, _fx, _nl, _na)) in list(B.items()):
    _fx = tuple((_SOFT.get(e, e), a) for e, a in _fx)
    if not any(e == 'regeneration' for e, _a in _fx):
        _fx = (('regeneration', 0),) + _fx
    _seen = []
    _fx = tuple(x for x in _fx if not (x[0] in _seen or _seen.append(x[0])))
    B[_w] = (_h, (_nn, _fx, _nl, _na))
# (the two of them, together - and the special ones)
TOGETHER = ('Together Again', (('regeneration', 1), ('luck', 0), ('speed', 0)), '(Henry trots up to Nia and touches his nose to hers)', '(Nia purrs, and curls her tail round his)')
SPECIAL = {'emma': 'p230/sp/emma', 'ava': 'p230/sp/ava'}

# the owner's trios
TRIOS = {
    'cat_pack': ('Two Cats and a Dog', '#b8a8ff', ('henry', 'bender', 'nia'), (('speed', 0), ('regeneration', 0), ('luck', 0))),
    'night_court': ('The Night Court', '#9a9ab8', ('emma', 'cecil', 'henry'), (('night_vision', 0), ('regeneration', 0), ('haste', 0))),
    'autumn_court': ('The Autumn Court', '#e0a050', ('emma', 'cecil', 'nia'), (('regeneration', 0), ('haste', 0), ('luck', 0))),
    'wild_pride': ('The Wild Pride', '#5a9ae8', ('bloo', 'henry', 'nia'), (('strength', 0), ('regeneration', 0), ('resistance', 0))),
    'gentle_giant': ('The Gentle Giant', '#7aa8e8', ('bloo', 'nia', 'bender'), (('regeneration', 1), ('resistance', 0), ('absorption', 0))),
    'night_hunt': ('The Night Hunt', '#4a5a9a', ('bloo', 'bender', 'henry'), (('strength', 0), ('speed', 0), ('night_vision', 0))),
    'queens_garden': ("The Queen's Garden", '#6ad8e8', ('emma', 'ava', 'nia'), (('regeneration', 1), ('water_breathing', 0), ('absorption', 0))),
    'playdate': ('Playdate', '#ff8ad8', ('emma', 'bender', 'nia'), (('speed', 0), ('regeneration', 0), ('jump_boost', 0))),
    'midnight_romp': ('The Midnight Romp', '#c890e0', ('emma', 'bender', 'henry'), (('speed', 0), ('jump_boost', 0), ('night_vision', 0))),
    'family_cats': ("Emma's Cats", '#ffb0d8', ('emma', 'henry', 'nia'), (('regeneration', 1), ('luck', 0), ('absorption', 0))),
    'fishbowl': ('The Fishbowl Standoff', '#ffa040', ('fishy', 'henry', 'nia'), (('water_breathing', 0), ('luck', 0), ('regeneration', 0))),
}
BANTER = {
    'cat_pack': [('Henry', '(and Nia take turns batting at Bender\'s wagging tail)', 'Bender', '(wags harder. This is the best day of his life.)')],
    'night_court': [('Emma', 'The wizard, the princess, and the cat who owns them both.', 'Cecil', 'He does own us, doesn\'t he.')],
    'autumn_court': [('Emma', 'Nia\'s colours match the leaves, Cecil! Look!', 'Cecil', 'All of autumn in one small cat.')],
    'wild_pride': [('Bloo', '(lies down; both cats climb on top of him)', 'Henry', '(this is his throne now)')],
    'gentle_giant': [('Bender', '(carries Nia on his back like a little queen)', 'Bloo', '(walks very slowly beside them, so she won\'t fall)')],
    'night_hunt': [('Henry', '(leads the way through the dark, tail high)', 'Bender', '(follows, very proud to be in the pack)')],
    'queens_garden': [('Queen Ava', 'In my garden, the little ones are always safe.', 'Emma', 'Nia loves it here, Mother. Look at her.')],
    'playdate': [('Emma', 'Bender, gentle! She\'s little!', 'Bender', '(lies down, VERY gently, next to Nia)')],
    'midnight_romp': [('Emma', 'Race you both to the tree! ...Henry, that\'s cheating, you can climb!', 'Bender', '(barks at the tree)')],
    'family_cats': [('Emma', 'My two favourite cats in the WHOLE world!', 'Henry', '(and Nia purr in stereo)')],
    'fishbowl': [('Fishy', 'TWO of them! Gentlemen, ladies - I implore you!', 'Henry', '(and Nia sit side by side, watching the bowl. Unblinking.)')],
}
