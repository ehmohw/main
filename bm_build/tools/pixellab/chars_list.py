"""2.94: every pixel character asked of PixelLab (/v2/create-character-pro from a concept image, then /characters/animations,
south only - they're billboarded). key: (concept (ref/owner/<k>.png, or a figurine render <item>.png), size, description,
{animation: (action, frames)})"""
STYLE = 'clean 16-bit retro RPG sprite, crisp dark outline, bright saturated colours, full body, front view'
BASE = {'idle': ('standing idle, breathing gently', 4), 'walk': ('walking forward toward the viewer', 8), 'sit': ('sitting down on the ground, resting', 4)}


def A(attack, extra=None):
    d = dict(BASE, attack=(attack, 8))
    d.update(extra or {})
    return d


CHARS = {
    # costumes (cosmetic pixel looks for followers)
    'celi': ('celi', 64, "Celi, a moody frost elf: pale blue skin, pointed ears, golden eyes, small fangs, orange-gold hair with a braid at the back; a puffy light-blue star-patterned coat with white fur collar and cuffs and a cloud-like white fur hem, a braided belt with a crescent-moon buckle, dark blue mittens, navy knee boots",
             A('thrusting a frost spear forward')),
    'demo': ('demo', 80, "Democratus, a hooded reaper: dark green hooded cloak, short white hair, violet eyes, a dark purple mask over his mouth, dark grey armour with a small violet gem, black belt and gloves, grey leggings, dark green boots, a huge teal-bladed scythe with a gold claw guard and a green crystal over his shoulder",
             A('swinging a huge scythe in a wide arc')),
    'kw': ('kw', 80, "KillerWatt, a towering glassy green brute: translucent green body, a spiky crested head with a jagged dark violet grin, a lime breastplate with a gold crescent emblem, clawed hands, yellow pointed feet, four huge yellow lightning-shaped tendrils fanning from his back",
           A('slamming both fists down, crackling with lightning')),
    'tul': ('tul', 72, "Tullius, a drowned ghost captain: pale blue-green ghostly skin, hollow dark eyes, ice crystals on a dark green top hat with a green band, a tattered teal frock coat, a green sash, black gloves, green breeches, dark boots, holding a harpoon",
            A('thrusting a harpoon forward')),
    'fishy': ('fishy', 64, "Fishy, a goldfish wearing a tiny top hat and monocle, swimming inside a round glass fishbowl with seaweed and a little castle; the bowl walks on grey robot arms and legs",
              A('punching forward with a robot fist')),
    'bloo': ('bloo', 72, "Bloo, a hulking blue furry demon cat: yellow eyes, white horns, grey bat wings, a toothy snarl, pink nose, white muscular chest and arms with big white claws, blue furry legs, a thin grey tail with a blue tuft",
             A('slashing with both claws')),
    'apo': ('apo', 80, "Apophiss, the serpent king: a green serpent with a pale yellow-green belly, clawed green arms, a smooth reptile snout with no moustache and no hair, solid black eyes with small white pupils, no glasses, a small black crown with a green gem and a red jewel on white fur trim, dark teal fins and spines, a long red forked tongue",
            A('lunging forward to bite')),
    'chef': ('chef_ladle', 64, "The Chef, a cheerful cook with a big ball-shaped perfectly round head (a circle, no square jaw, no corners), soft round cheeks with rosy blush, orange skin, a clean-shaven chin with no beard, big round white eyes, a black curly moustache, a small round open mouth, a tall puffy white chef's hat, a dark red bow tie, a white chef's jacket, black and white checked trousers, holding a ladle",
             A('swinging a ladle')),
    'neighbor': ('neighbor', 64, "The Neighbor, a musician: a black beret with an orange button, dark red-brown hair, a white mask with black square glasses and blue eyes, freckles, a white sailor shirt with a black sailor collar and an octopus emblem, white trousers, black shoes, holding a conductor's baton",
                 A('conducting energetically with a baton')),
    'stalker': ('stalker', 72, "The Stalker, a gaunt pale olive-green creature: a bald skull-like head with small red eyes, a huge jagged fanged gaping mouth, pointed ears, long thin limbs, long hooked claws, long clawed feet",
                A('lunging and raking with long claws')),
    'lantern': ('lantern', 96, "The Arachno-Lantern, a carved jack-o'-lantern spider: an orange pumpkin head with an evil glowing carved face, red eyes, flames at the corners of its mouth, a purple forked tongue, a stem on top, eight long black spindly legs",
                A('rearing up and spitting fire')),
    'ava': ('ava', 64, "Queen Ava, a gentle queen: brown hair in a bun, teal eyes, a gold crown with a purple gem and blue jewels, a dark blue gown with pale blue shoulder caps, a teardrop pendant with a pink gem, long white gloves, a full dark blue skirt over a pale lace underskirt",
            A('casting a wave of water magic with both hands')),
    'pistachio': ('pistachio', 64, "Pistachio, a green ghost butler: a translucent mint-green ghost body with a wispy tail instead of legs, a tall black top hat with a red band, a gold monocle, a black curly moustache, a grey suit jacket with a red tie, holding a silver cloche on a plate",
                  A('lifting the cloche lid and a spirit flies out')),
    'pearl': ('pearl', 64, "Pearlman, a dapper penguin merchant: a black body with a white belly, a black top hat with a blue band, a toothy grin and an orange beak, a blue bow tie, a gold-framed green earth gem on his belly, yellow feet, carrying a black briefcase",
              A('swinging his briefcase')),
    'pearlq': ('pearlq', 64, "Queen Pearl, a young queen: long brown hair with a sea-glass blue streak swept over one eye, blue eyes, a gold crown with a purple gem, a pearl necklace and earrings, a turquoise sleeveless dress, dark teal flat shoes",
               A('throwing a glowing pearl')),
    'omega': ('omega', 96, "King Omega, a grey ghostly sea serpent: a coiled grey serpent body, yellow glowing eyes, a gold monocle, a gold spiked crown with a purple dome, a purple fanged mouth with a purple tongue, pale translucent fins along the back, clawed grey arms, a blue spirit flame at the tail tip",
              A('lunging forward with jaws open')),
    'ashur': ('ashur', 64, "Ashur, a fiery magma woman: orange-red lava skin with glowing yellow cracks and dark rock patches, flaming red-orange hair, a gold tiara with a red gem, pink eyes, fists wreathed in fire, orange leggings with yellow stripes and a black belt, black boots",
              A('hurling a fireball')),
    'bones': ('bones', 72, "Bones, a grey shark swimming upright: a scar across his half-closed eye, a skull-and-crossbones mark on his side, big jagged teeth, pale grey belly, dark grey fins",
              A('lunging forward with a big bite')),
    'bender': ('bv_ball', 64, "Bender, a tan dog standing upright on two legs: tan fur, big upright pointed ears, a black muzzle, grey around the eyes, a white chest, a dark collar, white paws",
               A('pouncing forward with a bark')),
    'zib': ('donadian_medal', 56, "Zib, a small teal alien: two antennae with green tips, glowing red eyes, a wide toothy grin, teal skin, a dark navy and gold uniform with a belt",
            A('firing a little ray gun')),
    'frog': ('frog_signet', 64, "The Frog with Mustache: a big round green frog with huge white bulging eyes, a thick black mustache, a red bow tie, a pale belly",
             A('lashing out a long pink tongue')),
    'don': ('donado_tag', 64, "Donado, a cream golden dog standing upright: cream-tan fur, floppy ears, a black nose, wearing a grey shirt",
            A('firing a green tractor beam from a little gadget')),
    'wil': ('wilfrey_locket', 64, "Wilfrey, a tall shadowy black knight: a featureless black armoured figure holding a sword and a heraldic shield",
            A('swinging a sword')),
    'dennis': ('dw_horn', 64, "Dennis, a stout dwarf: a black horned helmet with a skull badge, a big squared black beard and moustache, a black leather jacket, blue jeans, brown boots, holding a big wrench",
               A('throwing a glowing hot gold ingot')),
    'capshun': ('capshun_pencil', 64, "Mr. Capshun, a flat stick figure: a big round pale grey head with two tall empty oval eyes and worried brows, a thin black ink line body with long thin arms and legs, holding a paintbrush and a pencil",
                A('swiping a paintbrush')),
    # the third pixel follower, and the pixel boss
    'cecil_px': ('cecil', 64, "Cecil, a small hooded wizard: a purple hooded robe with a stitched hood, a black shadowy face with glowing yellow eyes and a jagged grin, black clawed hands, holding a wooden staff topped with a gold crescent and a pink crystal",
                 dict(BASE, attack=('casting a spell, the staff crystal flashing', 8), hex=('raising the staff and summoning a purple magic circle', 8), hurt=('recoiling backward from a hit', 4))),
    'apo_boss': ('apo', 128, "Apophiss, the serpent king, a huge boss: a green serpent rearing up with a pale yellow-green belly, clawed green arms, a smooth reptile snout with no moustache and no hair, solid black eyes with small white pupils, no glasses, a small black crown with a green gem and a red jewel on white fur trim, dark teal fins and spines, a long red forked tongue, a roaring fanged mouth",
                 {'idle': ('swaying menacingly, coiled', 4), 'move': ('slithering forward', 8), 'bite': ('lunging down to bite', 8), 'breath': ('breathing a stream of black fire', 8),
                  'slam': ('slamming his tail down on the ground', 8), 'roar': ('rearing up and roaring', 6), 'hurt': ('recoiling from a hit', 4), 'death': ('collapsing and fading away', 8)}),
}
