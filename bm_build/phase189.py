"""2.87: QUEEN AVA - EMMA'S MOTHER, THE QUEEN OF THE UNDERWATER KINGDOM - QUEEN AVA'S LOCKET. (ava_art.py, from the owner's art;
the machinery is rigpet's.) Apophiss killed her when he raided the palace for the ethereal gem's heart; she comes back as a
ghost - and she can wear her living form again for those she loves.

FINDING HER (hidden; HARD MODE ONLY): set down a Conduit - the kingdom's old light - at night, with Emma at your side. The sea gives her back:
  the ghost of a queen rises beside it. Right-click her (Emma still with you): mother and daughter meet again, and she gives
  you her locket. (Without Emma she only asks where her daughter is.)
QUEEN AVA'S LOCKET  use: call her (again: call her over); sneak + use: her menu - sit / send home, her FORM, her story, her
                    ways, the wardrobe.
HER LIVING FORM - THE TIDAL SOVEREIGN (control and shields):
  ROYAL WARD     every 15 s: an Absorption II shield on her player and every player within 8.
  TIDAL LASH     a whip of water at a foe up to 14 blocks off (5, Slowness II); a backhand of brine up close (3).
  UNDERTOW       two or more foes within 8: the tide drags them in toward her and holds them (Slowness III, 4).
  TIDE OF CROWNS (charged, every minute) a great wave round her: every foe within 10 takes 8 and is hurled up; her crew
                 gets Conduit Power, Dolphin's Grace and Resistance for 20 s.
HER GHOSTLY FORM - THE QUEEN'S LAMENT (drain and protection; she can't easily be hurt - Resistance III):
  MOTHER'S WATCH (passive) her player drops to 4 hearts or less: she throws herself between - Resistance IV for 5 s and a
                 burst of healing (once every 3 minutes). "Not again. Never again."
  SPECTRAL TOUCH she drifts through a foe within 6: 4, Wither; her player is healed a little.
  THE LAMENT     a wail at a foe up to 12 off: 3, Weakness and Slowness.
  REQUIEM        (charged, every minute) every foe within 10 withers, weakens and glows (6); the undead are torn apart (the
                 healing light burns them).
Right-click her: sit / stand. A frame keeps her, a display case shows her as a figurine, Cecil sells her doll, the Ember Rat
a golden one, the Tailor her looks (and her aura, Crown of the Deep), the Recruiter her Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import ava_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134

AV_C, AV_LINE = '#6ad8e8', '#d8f8ff'
W = 'ava'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Queen Ava', AV_C, AV_LINE, 'p189', 'av', 'aq'
    A = A
    MENU = 2580
    PET_HP, PET_CD = 50, 120
    ITEM = 'av_locket'
    pron, they = 'her', 'she'
    FACE = {'happy': 'happy', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': None}
    ATTRS = dict(armor=6, attack_damage=3, movement_speed=0.32, follow_range=32, step_height=1.0)
    SCALE = 0.9
    FORM = ('bm.avform', '_g', 'Living / ghostly form', None, 'Ghostly form. ...It is how I came back to you.', 'My living form - as I was. For a little while.',
            'Switch between her living form (shields and the tide) and her ghost (drain and protection).')
    ENC_FORM = True
    HIT = (0.9, 2.0)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'wave_a')]), 7: (None, [(0, 'cast_up'), (4, 'cast')]), 8: (None, [(0, 'cast_up'), (5, 'cast')]),
             9: (None, [(0, 'ward_a'), (6, 'ward_b')]), 11: (None, [(0, 'cast_up'), (6, 'cast'), (10, 'ward_a')]),
             12: (None, [(0, 'ward_a'), (6, 'ward_b'), (12, 'tide'), (26, 'curtsey')]), 14: (None, [(0, 'curtsey')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 5, 'sit_a': 20, 'sit_b': 20,
           'wave_a': 8, 'cast_up': 4, 'cast': 2, 'ward_a': 6, 'ward_b': 6, 'tide': 6, 'curtsey': 10}
    QUIPS = ['Stand tall. You are braver than you know.', 'The tide answers to me, little monster.', 'Emma used to hide behind my skirts, too.',
             'Mind your footing - the sea does not forgive.', 'A queen does not run. She glides.', 'Apophiss took my life. He will not take yours.',
             'Was that a scratch? Come here, let me see.', 'The deep remembers every crown.']
    HELLO = ('I am here, dear one.', 'The tide brought me back to you. Shall we?', 'I will be in the deep, watching. Call, and I will come.')
    SIT = ('Onward, then. Gently.', 'Let us rest a moment. Even queens tire.')
    FAINT = 'Forgive me... I could not... hold the door...'
    NOT_YOURS = 'You are kind - but I am watching over someone else.'
    POWERS = [('Living: Royal Ward', 'every 15 s, an Absorption II shield on you and every player within 8'),
              ('Living: Tidal Lash', 'a whip of water at a foe up to 14 off (5, Slowness II); a backhand of brine up close (3)'),
              ('Living: Undertow', 'two or more foes within 8 - the tide drags them in and holds them (Slowness III, 4)'),
              ('Living: Tide of Crowns', 'charged, every minute: every foe within 10 takes 8 and is hurled up; Conduit Power, Dolphin\'s Grace and Resistance for your crew'),
              ('Ghost: Mother\'s Watch', 'you drop to 4 hearts: she shields you - Resistance IV and healing (every 3 minutes)'),
              ('Ghost: Spectral Touch / The Lament', 'she drifts through a foe (4, Wither - you are healed a little); a wail at a foe up to 12 off (3, Weakness, Slowness)'),
              ('Ghost: Requiem', 'charged, every minute: every foe within 10 withers, weakens and glows (6); the undead are torn apart')]
    INTRO = [T('Queen Ava', AV_C, bold=True), T(' - Emma\'s mother, queen of the kingdom beneath the waves. ', 'gray'), T('The tide shields; the ghost protects.', 'white')]
    BUTTONS = ((6, 'Her story', 'The kingdom, the war, and the night she fell.', 'p189/story'),)
    BURST = ['particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.7 0.4 0.05 30', 'particle minecraft:splash ~ ~1 ~ 0.5 0.6 0.5 0.1 30',
             'particle minecraft:flash{color:[0.4,0.85,0.95,1.0]} ~ ~1 ~ 0 0 0 0 1']
    FADE_SOUND = 'playsound minecraft:block.conduit.deactivate neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:block.conduit.activate neutral @a[distance=..20] ~ ~ ~ 0.8 1.2']
    FORM_FX = ['particle minecraft:soul ~ ~1 ~ 0.4 0.8 0.4 0.03 20', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.8 0.4 0.05 20',
               'playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..16] ~ ~ ~ 0.8 0.6']
    ENC_POSES = [(0, 'idle_a'), (40, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:soul ~ ~1.2 ~ 0.4 0.6 0.4 0.01 3'
    ADV = ('The Queen Beneath the Waves', 'Set down a Conduit at night with Emma beside you - and meet her mother again')
    ADMIN_HINT = 'In hard mode, she rises for anyone who sets down a Conduit at night with Emma beside them.'
    MEET_HINT = 'Right-click her with Emma beside you.'


C.EXPR = RP.Cfg.EXPR
RP.register(C)
item('av_locket', TOTEM, "Queen Ava's Locket", AV_C,
     ['A silver locket, the kingdom\'s teardrop on its lid.', 'Inside, a tiny portrait of a girl with a bow.', ('Use: call Queen Ava (again: call her over).', 'blue'),
      ('Sneak + use: her menu (her living / ghostly form).', 'blue'), ('Living: shields and the tide. Ghost: drain and protection.', 'blue'),
      ('If she faints: 2 minutes before she can return.', 'gray'), ('"Look after her for me."', 'dark_gray')],
     model='bm:av_locket', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_ava', TOTEM, 'Ava Doll', AV_C, ['A doll of Queen Ava - crown, bun and her blue gown.', ('Right-click a block: set it down.', 'blue'),
                                         ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_ava', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_ava'] = 'bm:p141/doll_ava/use'
P141.DOLLS.append(('doll_ava', 'Queen Ava', AV_C, 'A doll of Queen Ava - crown, bun and her blue gown.', 'minecraft:bubble_pop',
                   'minecraft:block.conduit.ambient.short', 'minecraft:splash'))
P141.DOLL_FROM['doll_ava'] = ('av_locket', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['av_locket'] = (0.0, 1.75, -0.62, 0.62, -0.58, 0.58)
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((5, 1, 8, 4, 11, 1), fill=hexc('#c8ccd6'))                                              # the chain
    d.ellipse((3, 4, 12, 14), fill=hexc('#9aa4b4'), outline=hexc('#4a5262'))
    d.ellipse((4, 5, 11, 12), fill=hexc('#d8dee8'))
    d.ellipse((6, 7, 9, 11), outline=hexc('#6ad8e8')); d.point((7, 6), fill=hexc('#6ad8e8')); d.point((8, 6), fill=hexc('#6ad8e8'))
    d.point((7, 9), fill=hexc('#d0287a')); d.point((8, 9), fill=hexc('#d0287a'))
    d.point((5, 6), fill=hexc('#ffffff'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    R.HATS['doll_ava'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                               'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


STORY = [('I. Before the Water', ['Our kingdom was not always beneath the waves. A thousand years ago it stood on the shore, in the sun, and its heart was a gem - the ethereal gem.',
                                  'It could mend, and grow, and give. My ancestors would not use it, except for themselves. One of our own blood could not bear that.']),
         ('II. Democratus', ['He was a prince of our house. He begged them to use the gem for the people - the sick, the starving. They refused. So he took up the scythe.',
                             'Cecil stood with him, at the start. The war that followed broke the gem: its elements scattered over the land, and whoever found them, kept their power.']),
         ('III. The Deep', ['We lost so much that we fled to the depths with what was left of the gem, and built again where no army could march.',
                            'The bloo-furred folk of the woods fought beside my forefathers then. Democratus had slaughtered their families. They have not forgotten.']),
         ('IV. The Serpent', ['Centuries later Apophiss went to war with his brother, Omega, for a richer land - his own was dying. Cecil cursed Omega\'s island into darkness to drive him off.',
                              'And then the serpent looked to the sea. He came for the gem\'s heart, the night the palace fell. I held the door so Emma could get out. Leo carried her.']),
         ('V. Now', ['My sister Pearl wears the crown, for Emma was too young. She hates it - and she is better at it than she knows.',
                     'And Apophiss is planning again. He wants what is left of the gem. I died once keeping it from him. I would do it again.'])]


def generate(G):
    import phase28 as P28
    fn = G.fn

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.avwatch dummy']
        G.OBJECTIVES.append('bm.avwatch')
        lines = ['scoreboard players set @s ' + S('k2') + ' 0', 'execute on owner if score @s bm.avform matches 1 run scoreboard players set #avf bm.rng 1',
                 'execute on owner unless score @s bm.avform matches 1 run scoreboard players set #avf bm.rng 0',
                 f'scoreboard players operation @s {S("k2")} = #avf bm.rng',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..12] run function bm:{pfx}/great_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
                 f'execute {idle} if score @s {S("k2")} matches 0 unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/under_go',
                 f'execute {idle} if score @s {S("k2")} matches 0 unless score @s {S("sc")} matches 1.. run function bm:{pfx}/ward_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if score @s {S("k2")} matches 0 if entity @e[{foe},distance=..3] run function bm:{pfx}/melee_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if score @s {S("k2")} matches 1 if entity @e[{foe},distance=..6] run function bm:{pfx}/melee_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..14] run function bm:{pfx}/range_go']
        fn(f'{pfx}/ward_go', go(9, 14, 'sc', 300, face('happy', 14) + ['playsound minecraft:block.conduit.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.4']))
        fn(f'{pfx}/under_go', go(11, 14, 'bc', 240, face('surprised', 14) + ['playsound minecraft:entity.guardian.attack neutral @a[distance=..20] ~ ~ ~ 0.6 1.6']))
        fn(f'{pfx}/melee_go', go(7, 8, 'mc', 24, ['playsound minecraft:entity.player.splash neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']))
        fn(f'{pfx}/range_go', go(8, 10, 'rc', 30, ['playsound minecraft:item.trident.throw neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/great_go', go(12, 32, 'gc', 1200, face('surprised', 32) + ['playsound minecraft:block.conduit.activate neutral @a[distance=..24] ~ ~ ~ 1 0.7']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/melee_hit',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/range_hit',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 8 run function bm:{pfx}/ward_hit',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 7 run function bm:{pfx}/under_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 20..31 run particle minecraft:bubble_column_up ~ ~0.5 ~ 1.5 0.2 1.5 0.1 8',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/great_hit'])
        living, ghost = f'if score @s {S("k2")} matches 0', f'if score @s {S("k2")} matches 1'
        # -- living: the ward, the lash, the undertow, the Tide of Crowns
        fn(f'{pfx}/ward_hit', ['execute on owner if entity @s[distance=..12] run effect give @s minecraft:absorption 20 1 true',
                               'effect give @a[distance=..8,gamemode=!spectator] minecraft:absorption 20 1 true',
                               'particle minecraft:bubble_pop ~ ~1.2 ~ 2 0.6 2 0.05 30', 'particle minecraft:end_rod ~ ~1.2 ~ 1.5 0.6 1.5 0.02 10',
                               'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'])
        fn(f'{pfx}/melee_hit', hit(3) + [f'execute {ghost} run scoreboard players set #pd bm.rng 4',
                                         f'execute {living} as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/brine',
                                         f'execute {ghost} as @e[{foe},distance=..6,sort=nearest,limit=1] at @s run function bm:{pfx}/touch',
                                         f'execute {ghost} at @e[{foe},distance=..6,sort=nearest,limit=1] run tp @s ~ ~ ~',
                                         f'execute {ghost} on owner if entity @s[distance=..24] run effect give @s minecraft:instant_health 1 0 true'] + end)
        fn(f'{pfx}/brine', [f'function bm:{pfx}/hurt', 'particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.1 20', 'playsound minecraft:entity.player.splash.high_speed neutral @a[distance=..16] ~ ~ ~ 0.5 1.4'])
        fn(f'{pfx}/touch', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:wither 3 0', 'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 10',
                            'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
        fn(f'{pfx}/range_hit', hit(5) + [f'execute {ghost} run scoreboard players set #pd bm.rng 3',
                                         f'execute {living} positioned ~ ~1.3 ~ facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes run function bm:{pfx}/lash',
                                         f'execute {ghost} positioned ~ ~1.5 ~ facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes run function bm:{pfx}/wail',
                                         f'execute {living} as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/lashed',
                                         f'execute {ghost} as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/wailed'] + end)
        fn(f'{pfx}/lash', [f'particle minecraft:splash ^ ^ ^{d / 2:.1f} 0.05 0.05 0.05 0 2' for d in range(2, 28, 2)] +
           [f'particle minecraft:bubble ^ ^ ^{d / 2:.1f} 0 0 0 0 1' for d in range(3, 28, 4)])
        fn(f'{pfx}/lashed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', 'particle minecraft:splash ~ ~1 ~ 0.4 0.5 0.4 0.2 30',
                             'playsound minecraft:entity.generic.splash neutral @a[distance=..16] ~ ~ ~ 0.6 1.2'])
        fn(f'{pfx}/wail', [f'particle minecraft:soul ^ ^ ^{d / 2:.1f} 0.05 0.05 0.05 0 1' for d in range(2, 24, 2)] +
           ['playsound minecraft:entity.allay.death neutral @a[distance=..16] ~ ~ ~ 0.5 0.6'])
        fn(f'{pfx}/wailed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:weakness 4 0', 'effect give @s minecraft:slowness 4 0', 'particle minecraft:soul ~ ~1.4 ~ 0.3 0.5 0.3 0.02 8'])
        fn(f'{pfx}/under_hit', hit(4) + ['particle minecraft:bubble_column_up ~ ~0.3 ~ 3 0.2 3 0.1 60', 'particle minecraft:splash ~ ~0.5 ~ 3 0.3 3 0.2 60',
                                         'playsound minecraft:block.bubble_column.whirlpool_inside neutral @a[distance=..20] ~ ~ ~ 1 0.8',
                                         f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/drag'] + end)
        fn(f'{pfx}/drag', [f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet run tp @s ^ ^ ^1.5', f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 2'])
        fn(f'{pfx}/great_hit', [f'execute {living} run function bm:{pfx}/tide', f'execute {ghost} run function bm:{pfx}/requiem'])
        fn(f'{pfx}/tide', hit(8) + ['playsound minecraft:entity.elder_guardian.curse neutral @a[distance=..24] ~ ~ ~ 0.5 1.6',
                                    'playsound minecraft:ambient.underwater.exit neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                                    'particle minecraft:splash ~ ~1 ~ 5 1 5 0.4 200', 'particle minecraft:bubble_pop ~ ~1 ~ 4 1.5 4 0.1 80', 'particle minecraft:nautilus ~ ~1.5 ~ 2 1 2 1 40',
                                    'effect give @a[distance=..12,gamemode=!spectator] minecraft:conduit_power 20 0 true',
                                    'effect give @a[distance=..12,gamemode=!spectator] minecraft:dolphins_grace 20 0 true',
                                    'effect give @a[distance=..12,gamemode=!spectator] minecraft:resistance 20 0 true',
                                    f'execute as @e[{foe},distance=..10] at @s run function bm:{pfx}/hurled',
                                    'execute on owner if entity @s[distance=..24] run ' + X.csay('The tide of crowns - kneel to the sea!')] + end)
        fn(f'{pfx}/hurled', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 3', 'particle minecraft:splash ~ ~1 ~ 0.4 0.6 0.4 0.2 20'])
        fn(f'{pfx}/requiem', hit(6) + ['playsound minecraft:entity.warden.sonic_charge neutral @a[distance=..24] ~ ~ ~ 0.5 1.4',
                                       'playsound minecraft:particle.soul_escape neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                                       'particle minecraft:soul ~ ~1 ~ 5 1.5 5 0.03 120', 'particle minecraft:sculk_soul ~ ~1 ~ 4 1 4 0.02 40',
                                       f'execute as @e[{foe},distance=..10] at @s run function bm:{pfx}/mourned',
                                       'execute as @e[type=#minecraft:undead,distance=..10,tag=!bm.npc] run effect give @s minecraft:instant_health 1 1',
                                       'execute on owner if entity @s[distance=..24] run ' + X.csay('Requiem. Rest - and do not rise again.')] + end)
        fn(f'{pfx}/mourned', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:wither 6 1', 'effect give @s minecraft:weakness 6 1', 'effect give @s minecraft:glowing 6 0'])
        # -- the second loop: the ghost is hard to hurt; MOTHER'S WATCH; a soft drift of souls (bubbles while living)
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        fn(f'{pfx}/sec', [f'execute if score @s {S("k2")} matches 1 run effect give @s minecraft:resistance 3 2 true',
                          f'execute if score @s {S("k2")} matches 1 run particle minecraft:soul ~ ~1.4 ~ 0.3 0.5 0.3 0.01 2',
                          f'execute if score @s {S("k2")} matches 0 run particle minecraft:bubble_pop ~ ~1.6 ~ 0.3 0.4 0.3 0.02 2',
                          'effect give @s minecraft:regeneration 3 0 true', 'effect give @s minecraft:water_breathing 12 0 true',
                          f'execute if score @s {S("k2")} matches 1 on owner if entity @s[distance=..24] unless score @s bm.avwatch matches 1.. run function bm:{pfx}/watch'])
        fn(f'{pfx}/watch', ['execute store result score #hp bm.rng run data get entity @s Health', 'execute unless score #hp bm.rng matches ..8 run return 0',
                            'scoreboard players set @s bm.avwatch 180', 'effect give @s minecraft:resistance 5 3 true', 'effect give @s minecraft:instant_health 1 1 true',
                            'particle minecraft:soul ~ ~1 ~ 0.5 1 0.5 0.05 40', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 1 0.5 0.3 30',
                            'playsound minecraft:item.totem.use player @s ~ ~ ~ 0.5 1.6', X.csay('Not again. NEVER again.')])
        X.second.append('scoreboard players remove @a[scores={bm.avwatch=1..}] bm.avwatch 1')
        return lines

    def encounter(G, X):
        pfx = 'p189'
        G.wjson('bm/advancement/p189/conduit.json', {'criteria': {'set': {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
            {'condition': 'minecraft:location_check', 'predicate': {'block': {'blocks': 'minecraft:conduit'}}}]}}},
            'rewards': {'function': 'bm:p189/enc/conduit'}})
        emma_out = 'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..16] if score @s bm.pid = #me bm.pid'
        # (2.94: with Emma beside you, a conduit that can't bring her back yet says why - in Emma's words; without Emma it stays a secret)
        em_say = lambda txt: X.tellraw('@s', [T('Emma: ', '#ff8ad8', bold=True), T(f'"{txt}"', '#ffd0ec')])
        fn('p189/enc/conduit', ['advancement revoke @s only bm:p189/conduit', 'execute if entity @s[tag=bm.avmet] run return 0',
                                'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #em bm.rng 0', f'{emma_out} run scoreboard players set #em bm.rng 1',
                                'execute if score #em bm.rng matches 0 run return 0',
                                'execute unless score #hard bm.cfg matches 1 run return run ' + em_say("That light... it's like the palace. I thought I felt Mother for a moment. "
                                                                                                         "The sea isn't dark enough to give her back yet - not while the Hollow King still sits his throne."),
                                'execute store result score #nt bm.rng run time of minecraft:overworld query time', 'scoreboard players operation #nt bm.rng %= #24000 bm.bm',
                                'execute unless score #nt bm.rng matches 13000..22999 run return run ' + em_say("Mother always came to my window at night... "
                                                                                                                  "Can we light it again when the stars are out?"),
                                'execute at @s if entity @e[type=minecraft:interaction,tag=bm.avenc,distance=..48] run return 0',
                                'execute at @s positioned ^ ^ ^3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p189/enc/rise',
                                'execute at @s run function bm:p189/enc/rise'])
        fn('p189/enc/rise', ['function bm:p189/enc/spawn', 'particle minecraft:soul ~ ~1 ~ 0.5 1.2 0.5 0.03 40', 'particle minecraft:bubble_column_up ~ ~0.2 ~ 0.6 0.2 0.6 0.1 40',
                             'playsound minecraft:block.conduit.activate neutral @a[distance=..24] ~ ~ ~ 1 0.6', 'playsound minecraft:ambient.underwater.loop.additions.ultra_rare neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                             X.tellraw('@s', [T('The conduit flares. The water stills... ', AV_LINE, italic=True),
                                              T('and a pale queen rises out of the light, crown and all, looking straight at Emma.', 'gray', italic=True)])])
        emma = lambda txt: X.tellraw('@s', [T('Emma: ', '#ff8ad8', bold=True), T(f'"{txt}"', '#ffe0f4')])
        fn('p189/enc/talk', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #em bm.rng 0', f'{emma_out} run scoreboard players set #em bm.rng 1',
                             f'execute if items entity @s container.* {X.holds("av_locket")} run return run ' + X.csay('You have my locket, dear. Open it - I will come.'),
                             'execute if score #em bm.rng matches 1 run return run function bm:p189/enc/recruit',
                             X.csay('Where is my daughter? Where is Emma? ...Bring her to me. Please.'),
                             'playsound minecraft:entity.allay.ambient_without_item neutral @s ~ ~ ~ 0.8 0.6'])
        fn('p189/enc/recruit', [f'execute as {X.here} at @s run particle minecraft:heart ~ ~2 ~ 0.6 0.4 0.6 0 8',
                                f'execute as {X.here} at @s run playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                                X.cchat('Emma...? My little Emma. Look at you - all grown up, and so brave.'),
                                emma('...Mama?'),
                                X.cchat('I held the door that night so you could get out. I would do it a thousand times.'),
                                X.cchat('Take my locket, friend. Keep her safe - and when you call, I will come. The tide always comes back.'),
                                'function bm:p189/enc/joined'])

    RP.build(C, G, abilities, encounter)
    # her story (a menu button)
    pages = [P28.body([T(t, AV_C, bold=True), T('\n' + '\n'.join(p), 'gray')], 340) for t, p in STORY]
    sdlg = P28.multi([T("QUEEN AVA'S STORY", AV_C, bold=True)], pages, [P28.btn([T('« Back', 'gray')], C.MENU + 5, width=150)], columns=1, exit_label='Close')
    fn('p189/story', [f'scoreboard players set @s bm.menu {C.MENU}', f'dialog show @s {snbt(sdlg)}'])
