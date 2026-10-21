"""2.87: BLOO - THE RESERVED WOODLAND CREATURE - BLOO'S CLAW. (bloo_art.py, from the owner's art; the machinery is rigpet's.)
A hulking blue cat-beast of the deep woods, horned and bat-winged, who wants nothing to do with humans: Democratus slaughtered
his family in the great war a thousand years ago. He fought beside the Underwater Kingdom's ancestors then - grudgingly - and
he has not forgiven anyone since. He is vicious, and he fights like it: he never stops attacking.

FINDING HIM (hidden; HARD MODE ONLY): plant a sapling in a forest at night. Something in the trees has been watching the woods die for a long
  time - and he comes to see who is planting them back. Right-click him holding raw salmon (or cod): "...Fine. You're not
  like the others." (Come with Democratus and he'll have nothing to do with you.)
BLOO'S CLAW  use: call him (again: call him over); sneak + use: his menu - sit / send home, his story, his ways, the wardrobe.
CLAW RAKE      relentless: a rake every 0.7 s at a foe within 3.5 (6, and it bleeds - Wither); every hit builds FRENZY
               (up to 5 - each a point more damage); it fades if he goes 4 s without a hit.
POUNCE         every 5 s, a foe within 4-14: a crouch - and he's on it (8, Slowness).
FERAL ROAR     two or more foes within 8, every 20 s: they cower (Weakness II, Slowness II, 3); you get Strength.
THE WILD HUNT  (charged, every minute) a four-second rampage: he leaps from foe to foe within 16, eight times - 9 each.
WOODLAND GUARDIAN  in a forest he hits 2 harder, and you get Regeneration.
OLD WOUNDS     Democratus near him: Bloo hits harder still - and growls (their pair, phase192, says the rest).
Right-click him: sit / stand. A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the Ember Rat
a golden one, the Tailor his looks (and his aura, Feral Moon), the Recruiter his Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import bloo_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134

BL_C, BL_LINE = '#5a9ae8', '#d0e4ff'
W = 'bloo'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Bloo', BL_C, BL_LINE, 'p191', 'bo', 'bk'
    A = A
    MENU = 2620
    PET_HP, PET_CD = 70, 120
    ITEM = 'bo_claw'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious', 'scowl')
    FACE = {'happy': 'happy', 'surprised': 'roar', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'scowl', 'serious': None, 'scowl': 'scowl'}
    ATTRS = dict(armor=10, attack_damage=7, movement_speed=0.42, follow_range=32, step_height=1.2)
    SCALE = 1.1
    HIT = (1.2, 2.5)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'hmph')]), 7: (None, [(0, 'swipe_up'), (3, 'swipe')]), 8: (None, [(0, 'crouch'), (6, 'pounce'), (12, 'swipe')]),
             11: (None, [(0, 'roar')]),
             12: (None, [(0, 'roar'), (10, 'pounce'), (20, 'swipe'), (30, 'pounce'), (40, 'swipe'), (50, 'pounce'), (60, 'swipe'), (70, 'pounce'), (80, 'roar')]),
             14: (None, [(0, 'hmph')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 4, 'sit_a': 20, 'sit_b': 20,
           'swipe_up': 3, 'swipe': 2, 'crouch': 5, 'pounce': 3, 'roar': 6, 'hmph': 10}
    QUIPS = ['Hrrrnh.', 'Stay out of my way.', 'You humans are all the same. ...Mostly.', 'MORE.', 'That one was slow. Pathetic.',
             'Don\'t thank me. I wasn\'t doing it for you.', 'The woods remember. So do I.', 'Keep up, human.']
    HELLO = ('...What.', 'Hrrn. You called. I came. Don\'t make it a habit.', 'Finally. The woods are quieter without you.')
    SIT = ('Fine. Moving.', 'Hrrnh. Don\'t touch me.')
    FAINT = 'Not... done... yet...'
    NOT_YOURS = 'Touch me again and lose the hand.'
    POWERS = [('Claw Rake', 'relentless - a rake every 0.7 s (6, and it bleeds); every hit builds Frenzy, up to 5 - each a point more; it fades after 4 s without a hit'),
              ('Pounce', 'every 5 s, a foe within 4-14: a crouch - and he lands on it (8, Slowness)'),
              ('Feral Roar', 'two or more foes within 8, every 20 s: they cower (Weakness II, Slowness II, 3); Strength for you'),
              ('The Wild Hunt', 'charged, every minute: a four-second rampage - he leaps from foe to foe within 16, eight times, 9 each'),
              ('Woodland Guardian', 'in a forest he hits 2 harder, and you get Regeneration'),
              ('Old Wounds', 'Democratus near him: Bloo hits harder still - and growls')]
    INTRO = [T('Bloo', BL_C, bold=True), T(' - the beast of the deep woods. He doesn\'t like you. ', 'gray'), T('He likes your enemies even less.', 'white')]
    BUTTONS = ((6, 'His story', 'The war, the woods, and the man with the scythe.', 'p191/story'),)
    BURST = ['particle minecraft:cherry_leaves ~ ~1.2 ~ 0.6 0.8 0.6 0.05 30', 'particle minecraft:poof ~ ~1 ~ 0.5 0.8 0.5 0.04 20',
             'particle minecraft:flash{color:[0.35,0.6,0.95,1.0]} ~ ~1.2 ~ 0 0 0 0 1']
    FADE_SOUND = 'playsound minecraft:entity.ravager.hurt neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'
    SUMMON_EXTRA = ['playsound minecraft:entity.ravager.roar neutral @a[distance=..24] ~ ~ ~ 0.5 1.4']
    ENC_POSES = [(0, 'idle_a'), (40, 'hmph')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 40 run particle minecraft:falling_spore_blossom ~ ~2.4 ~ 0.6 0.2 0.6 0 3'
    ADV = ('Not Like the Others', 'Plant a sapling in a forest at night - and earn the trust of the beast of the woods')
    ADMIN_HINT = 'In hard mode, he comes to anyone who plants a sapling in a forest at night.'
    MEET_HINT = 'Right-click him holding raw salmon or cod.'


RP.register(C)
item('bo_claw', TOTEM, "Bloo's Claw", BL_C,
     ['A great white claw on a cord of braided bark.', 'It is still sharp.', ('Use: call Bloo (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('He never stops attacking. Frenzy, pounce, roar.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray'), ('"Don\'t make it a habit."', 'dark_gray')],
     model='bm:bo_claw', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_bloo', TOTEM, 'Bloo Doll', BL_C, ['A doll of Bloo - horns, wings and a very grumpy snarl.', ('Right-click a block: set it down.', 'blue'),
                                            ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_bloo', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_bloo'] = 'bm:p141/doll_bloo/use'
P141.DOLLS.append(('doll_bloo', 'Bloo', BL_C, 'A doll of Bloo - horns, wings and a very grumpy snarl.', 'minecraft:poof',
                   'minecraft:entity.cat.hiss', 'minecraft:cherry_leaves'))
P141.DOLL_FROM['doll_bloo'] = ('bo_claw', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['bo_claw'] = (0.0, 2.35, -0.95, 0.95, -0.6, 0.6)
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((3, 2, 6, 5, 9, 4), fill=hexc('#7a5a3a'))                                               # the bark cord
    d.polygon([(6, 5), (10, 5), (12, 9), (11, 13), (8, 15), (9, 11), (8, 8)], fill=hexc('#f0f0f4'), outline=hexc('#9a9aa8'))
    d.line((9, 6, 11, 10), fill=hexc('#ffffff'))
    d.point((7, 5), fill=hexc('#5a9ae8')); d.point((8, 5), fill=hexc('#5a9ae8'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    R.HATS['doll_bloo'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


STORY = [('I. The Woods', ['There were many of us once. Blue fur, horns, wings - we kept the old woods, and the woods kept us.',
                           'We wanted nothing from the humans in their shining kingdom by the sea. Only to be left alone.']),
         ('II. The Scythe', ['Then came the war. A prince of the sea kingdom turned on his own house - Democratus, with his storm and his scythe.',
                             'He came through our woods to get at them. He did not care what stood in the way. My family stood in the way.']),
         ('III. The Alliance', ['I fought beside the sea-folk\'s soldiers after that. Not for them. Against HIM.',
                                'The battle broke their precious gem into pieces. They ran into the sea. I stayed with the trees. I have been here ever since.']),
         ('IV. Humans', ['Every human I have met since wanted something - the woods, the stone, the gem\'s scattered pieces.',
                         'You planted a tree. ...That is the first thing a human has given back in a thousand years.']),
         ('V. The Serpent', ['The birds say the serpent-king Apophiss is stirring again, looking to the sea. More war.',
                             'Hrrn. Let him come through my woods. I have been waiting a long time for something worth fighting.'])]


def generate(G):
    import phase28 as P28
    fn = G.fn

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        # (k: Frenzy stacks; k2: its fade timer, in ticks)
        lines = [f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute if score @s {S("k2")} matches 0 run scoreboard players set @s {S("k")} 0',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..12] run function bm:{pfx}/great_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/roar_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..4] if entity @e[{foe},distance=..14] run function bm:{pfx}/pounce_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3.5] run function bm:{pfx}/melee_go',
                 # (he hunts: anything hostile within 16 and he's after it - he doesn't wait for you to be hit)
                 f'execute unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=3..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] feet run function bm:{pfx}/chase']
        fn(f'{pfx}/chase', ['execute if block ^ ^ ^0.4 #bm:grap_pass if block ^ ^1 ^0.4 #bm:grap_pass run tp @s ^ ^ ^0.22 ~ ~'])
        fn(f'{pfx}/melee_go', go(7, 5, 'mc', 14, ['playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.4 0.6']))
        fn(f'{pfx}/pounce_go', go(8, 14, 'rc', 100, face('surprised', 14) + ['playsound minecraft:entity.ravager.step neutral @a[distance=..16] ~ ~ ~ 1 1.2']))
        fn(f'{pfx}/roar_go', go(11, 12, 'bc', 400, face('surprised', 12) + ['playsound minecraft:entity.ravager.roar neutral @a[distance=..24] ~ ~ ~ 1 1.1']))
        fn(f'{pfx}/great_go', go(12, 84, 'gc', 1200, face('surprised', 84) + ['playsound minecraft:entity.ravager.roar neutral @a[distance=..32] ~ ~ ~ 1 0.8',
                                                                               'playsound minecraft:entity.warden.roar neutral @a[distance=..32] ~ ~ ~ 0.6 1.4',
                                                                               'execute on owner if entity @s[distance=..24] run ' + X.csay('THE HUNT IS ON.'),
                                                                               'effect give @s minecraft:regeneration 5 2 true']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 2 run function bm:{pfx}/rake',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/leap',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 8 run function bm:{pfx}/roar_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 2..74 run function bm:{pfx}/hunt_tick'])
        # damage: base + Frenzy + the forest + Democratus near
        def dmg(base):
            return hit(base) + [f'scoreboard players operation #pd bm.rng += @s {S("k")}',
                                'execute if biome ~ ~ ~ #minecraft:is_forest run scoreboard players add #pd bm.rng 2',
                                'execute if entity @e[type=minecraft:wolf,tag=bm.dmpet,distance=..16] run scoreboard players add #pd bm.rng 2']
        frenzy = [f'execute if score @s {S("k")} matches ..4 run scoreboard players add @s {S("k")} 1', f'scoreboard players set @s {S("k2")} 80',
                  f'execute if score @s {S("k")} matches 5 run particle minecraft:angry_villager ~ ~2.6 ~ 0.3 0.2 0.3 0 1']
        fn(f'{pfx}/rake', dmg(6) + [f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] at @s run function bm:{pfx}/raked'] + frenzy + end)
        fn(f'{pfx}/raked', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:wither 3 0', 'particle minecraft:sweep_attack ~ ~1.2 ~ 0.2 0.2 0.2 0 1',
                            'particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 4', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.6 0.7'])
        fn(f'{pfx}/leap', dmg(8) + [f'execute at @e[{foe},distance=..14,sort=nearest,limit=1] run tp @s ~ ~ ~',
                                    'particle minecraft:explosion ~ ~0.5 ~ 0.3 0.1 0.3 0 2', 'playsound minecraft:entity.ravager.attack neutral @a[distance=..20] ~ ~ ~ 1 1',
                                    f'execute at @s as @e[{foe},distance=..2.5,sort=nearest,limit=1] at @s run function bm:{pfx}/pounced'] + frenzy + end)
        fn(f'{pfx}/pounced', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 2', 'effect give @s minecraft:wither 3 0'])
        fn(f'{pfx}/roar_hit', hit(3) + ['particle minecraft:sonic_boom ~ ~1.4 ~ 0 0 0 0 1', 'particle minecraft:cloud ~ ~1 ~ 3 0.4 3 0.1 40',
                                        f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/cower',
                                        'execute on owner if entity @s[distance=..16] run effect give @s minecraft:strength 10 0 true'] + end)
        fn(f'{pfx}/cower', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 5 1', 'effect give @s minecraft:slowness 5 1'])
        # the Wild Hunt: every 9 ticks, a leap to a foe within 16 (a random one) - 9
        fn(f'{pfx}/hunt_tick', [f'scoreboard players operation #h bm.rng = @s {S("x")}', 'scoreboard players operation #h bm.rng %= #9 bm.rng',
                                f'execute if score #h bm.rng matches 0 if entity @e[{foe},distance=..16] run function bm:{pfx}/hunt_leap'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #9 bm.rng 9']
        fn(f'{pfx}/hunt_leap', dmg(9) + [f'execute at @e[{foe},distance=..16,sort=random,limit=1] run tp @s ~ ~ ~',
                                         'particle minecraft:sweep_attack ~ ~1.2 ~ 0.6 0.4 0.6 0 3', 'particle minecraft:crit ~ ~1 ~ 0.6 0.6 0.6 0.3 20',
                                         'playsound minecraft:entity.ravager.attack neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                                         f'execute at @s as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/raked'] + frenzy + end)
        # -- every second: the woodland guardian; old wounds (he snarls at Democratus)
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        fn(f'{pfx}/sec', ['effect give @s minecraft:regeneration 3 0 true',
                          'execute if biome ~ ~ ~ #minecraft:is_forest on owner if entity @s[distance=..16] run effect give @s minecraft:regeneration 3 0 true',
                          'execute if biome ~ ~ ~ #minecraft:is_forest run particle minecraft:falling_spore_blossom ~ ~2.6 ~ 0.4 0.2 0.4 0 1',
                          'execute if entity @e[type=minecraft:wolf,tag=bm.dmpet,distance=..16] store result score #r bm.rng run random value 1..40',
                          'execute if entity @e[type=minecraft:wolf,tag=bm.dmpet,distance=..16] if score #r bm.rng matches 1 on owner if entity @s[distance=..20,tag=!bm.hush] run ' +
                          X.csay('I smell him. The scythe-man. Keep him away from me, human, or I will not answer for it.')])
        return lines

    def encounter(G, X):
        G.wjson('bm/advancement/p191/sapling.json', {'criteria': {'set': {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
            {'condition': 'minecraft:location_check', 'predicate': {'block': {'blocks': '#minecraft:saplings'}}}]}}},
            'rewards': {'function': 'bm:p191/enc/sapling'}})
        fn('p191/enc/sapling', ['advancement revoke @s only bm:p191/sapling', 'execute unless score #hard bm.cfg matches 1 run return 0', 'execute if entity @s[tag=bm.bomet] run return 0',
                                'execute store result score #nt bm.rng run time of minecraft:overworld query time', 'scoreboard players operation #nt bm.rng %= #24000 bm.bm',
                                'execute unless score #nt bm.rng matches 13000..22999 run return 0',
                                'execute at @s unless biome ~ ~ ~ #minecraft:is_forest run return 0',
                                'execute at @s if entity @e[type=minecraft:interaction,tag=bm.boenc,distance=..48] run return 0',
                                'execute at @s positioned ^ ^ ^5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p191/enc/watch',
                                'execute at @s positioned ^ ^ ^3 run function bm:p191/enc/watch'])
        fn('p191/enc/watch', ['function bm:p191/enc/spawn', 'particle minecraft:cherry_leaves ~ ~2 ~ 1 1 1 0.05 40',
                              'playsound minecraft:entity.ravager.ambient neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:block.azalea_leaves.break neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                              X.tellraw('@s', [T('The leaves part. ', BL_LINE, italic=True),
                                               T('Something huge and blue steps out of the dark between the trees - horns, wings, teeth - and stares at your sapling. Then at you.', 'gray', italic=True)])])
        fn('p191/enc/talk', ['scoreboard players operation #me bm.pid = @s bm.pid',
                             f'execute if items entity @s container.* {X.holds("bo_claw")} run return run ' + X.csay('You have my claw. Use it. Don\'t poke me.'),
                             'scoreboard players set #dm bm.rng 0', 'execute as @e[type=minecraft:wolf,tag=bm.dmpet,distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #dm bm.rng 1',
                             'execute if score #dm bm.rng matches 1 run return run ' + X.csay('YOU. You walk with HIM. The scythe-man. Get out of my woods.'),
                             'execute if items entity @s weapon.mainhand minecraft:salmon run return run function bm:p191/enc/recruit',
                             'execute if items entity @s weapon.mainhand minecraft:cod run return run function bm:p191/enc/recruit',
                             X.csay('Hrrrnh. Another human. Go away. ...Unless you brought something worth eating.'),
                             'playsound minecraft:entity.cat.hiss neutral @s ~ ~ ~ 1 0.5'])
        fn('p191/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:cherry_leaves ~ ~2 ~ 0.8 0.6 0.8 0.05 30',
                                f'execute as {X.here} at @s run playsound minecraft:entity.cat.eat neutral @a[distance=..16] ~ ~ ~ 1 0.5',
                                X.cchat('...Fish. Hrrn. And you planted a tree.'),
                                X.cchat('Fine. You\'re not like the others. Take my claw. Call, and I\'ll come - and anything that comes at you dies. Don\'t make it a habit.'),
                                'function bm:p191/enc/joined'])

    RP.build(C, G, abilities, encounter)
    pages = [P28.body([T(t, BL_C, bold=True), T('\n' + '\n'.join(p), 'gray')], 340) for t, p in STORY]
    sdlg = P28.multi([T("BLOO'S STORY", BL_C, bold=True)], pages, [P28.btn([T('« Back', 'gray')], C.MENU + 5, width=150)], columns=1, exit_label='Close')
    fn('p191/story', [f'scoreboard players set @s bm.menu {C.MENU}', f'dialog show @s {snbt(sdlg)}'])
