"""2.87: QUEEN PEARL - EMMA'S FUN AUNT, QUEEN REGENT OF THE UNDERWATER KINGDOM - QUEEN PEARL'S PEARLS. (pearl_art.py, from the
owner's art; the machinery is rigpet's.) Ava's younger sister: she took the throne when Ava fell, Emma being far too young -
and she would rather be anywhere else. Quirky, warm, a little wicked; the crown sits on her head like a party hat.

FINDING HER (hidden): she has a nose for cake. Set a cake down on a beach (or by any ocean or river) by day, having befriended
  Emma - and the queen regent pops up out of the surf to "inspect" it. Right-click her holding another cake: she's yours.
QUEEN PEARL'S PEARLS  use: call her (again: call her over); sneak + use: her menu - sit / send home, her OUTFIT, her story,
                      her ways, the wardrobe.
CASUAL (her aqua shift - a trickster who buffs on a whim):
  ROYAL WHIM     every 30 s, whatever takes her fancy: Speed II, Jump Boost II, Haste II, Luck, Dolphin's Grace, Night
                 Vision, Fire Resistance or Slow Falling for you, 30 s - and she tells you why.
  PEARL FLICK    a pearl flicked off her thumb at a foe up to 14 off (4) - one in four bursts in a flash: Glowing and
                 Blindness. A fan-slap up close (3).
  THE WINK       one foe within 10, every 20 s: smitten - it stops dead, can't hurt a thing, glows (6 s).
  ROYAL PROCLAMATION (charged, every minute) "I declare a HOLIDAY!" - every foe within 12 smitten; her crew gets Strength,
                 Regeneration II and Speed for 15 s; and a shower of coins - an emerald or two.
REGAL (the gown, the cape, the tall crown - she hates it, and says so):
  ROYAL DECREE   steady: Resistance and Strength for you within 12; every 30 s an Absorption shield (II) for her crew. No whims.
  ROYAL AUTHORITY her blows hit 2 harder.
  BY ROYAL DECREE (charged, every minute) every foe within 12 takes 10 and is struck down (Slowness IV); Absorption IV for the
                 crew - and a long-suffering sigh.
Right-click her: sit / stand. A frame keeps her, a display case shows her as a figurine, Cecil sells her doll, the Ember Rat
a golden one, the Tailor her looks (and her aura, Pearlescent Tide), the Recruiter her Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import pearl_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134

PQ_C, PQ_LINE = '#5ae0d8', '#d8fffa'
W = 'pearlq'
WHIMS = [('speed', 1, 'Speed! Let\'s go somewhere. Anywhere. Quickly.'), ('jump_boost', 1, 'Hop! Hop! Royal decree: hopping.'),
         ('haste', 1, 'Haste - dig, dig! I want to see what\'s down there.'), ('luck', 0, 'Luck! I have a good feeling about today.'),
         ('dolphins_grace', 0, 'Swim with me! The water\'s lovely - trust a mermaid-queen.'), ('night_vision', 0, 'Night vision. Darkness is SO last century.'),
         ('fire_resistance', 0, 'Fire resistance. Don\'t ask why. Just... trust me.'), ('slow_falling', 0, 'Slow falling - float like a jellyfish!')]


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Queen Pearl', PQ_C, PQ_LINE, 'p190', 'pq', 'pk'
    A = A
    MENU = 2600
    PET_HP, PET_CD = 44, 120
    ITEM = 'pq_pearls'
    pron, they = 'her', 'she'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious', 'wink', 'pout')
    FACE = {'happy': 'happy', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'wink', 'serious': None, 'wink': 'wink', 'pout': 'pout'}
    ATTRS = dict(armor=4, attack_damage=3, movement_speed=0.34, follow_range=32, step_height=1.0)
    FORM = ('bm.pqform', '_r', 'Casual / regal outfit', None, 'Ugh. Fine. The GOWN. Happy? I look like a wedding cake.', 'Oh thank goodness. I can breathe again!',
            'Switch between her casual shift (whims and charm) and her regal gown (steady royal decrees). She hates the gown.')
    HIT = (0.9, 1.95)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'wave_a')]), 7: (None, [(0, 'flick_up'), (4, 'flick')]), 8: (None, [(0, 'flick_up'), (5, 'flick')]),
             9: (None, [(0, 'twirl'), (8, 'bow')]), 11: (None, [(0, 'wink')]),
             12: (None, [(0, 'twirl'), (8, 'proclaim'), (24, 'bow')]), 14: (None, [(0, 'bow')]), 13: (None, [(0, 'pout')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 5, 'sit_a': 20, 'sit_b': 20,
           'wave_a': 8, 'flick_up': 4, 'flick': 2, 'twirl': 8, 'bow': 8, 'wink': 6, 'proclaim': 8, 'pout': 10}
    QUIPS = ['Is it lunchtime? It feels like lunchtime.', 'Don\'t tell the court I was here. They think I\'m "in council".',
             'Ava was always the sensible one. I got the fun genes.', 'Monsters! Ooh, exciting. Shall I wink at it?',
             'If anyone asks, I was NEVER here.', 'Emma gets her mischief from me. You\'re welcome.',
             'A crown is just a very heavy hat, darling.', 'I abdicate! ...No? Worth a try.']
    HELLO = ('Coming, coming! Hold your seahorses!', 'Queen Pearl, reporting for fun!', 'Back to the throne. Ugh. Call me the MOMENT something exciting happens!')
    SIT = ('Up we get! Adventure awaits!', 'Ooh, a sit. Wake me if there\'s cake.')
    FAINT = 'Tell the council... I died... doing something... FUN...'
    NOT_YOURS = 'Sorry, sweetie - I\'m out with someone else today!'
    POWERS = [('Casual: Royal Whim', 'every 30 s, whatever takes her fancy - Speed II, Jump Boost II, Haste II, Luck, Dolphin\'s Grace, Night Vision, Fire Resistance or Slow Falling, 30 s'),
              ('Casual: Pearl Flick', 'a pearl at a foe up to 14 off (4) - one in four bursts: Glowing and Blindness; a fan-slap up close (3)'),
              ('Casual: The Wink', 'every 20 s, one foe within 10 is smitten: it stops dead, harmless and glowing, for 6 s'),
              ('Casual: Royal Proclamation', 'charged, every minute: every foe within 12 smitten; Strength, Regeneration II and Speed for the crew; a shower of emeralds'),
              ('Regal: Royal Decree', 'steady Resistance and Strength for you within 12; every 30 s an Absorption II shield for the crew; her blows hit 2 harder'),
              ('Regal: By Royal Decree', 'charged, every minute: every foe within 12 takes 10 and is struck down (Slowness IV); Absorption IV for the crew')]
    INTRO = [T('Queen Pearl', PQ_C, bold=True), T(' - Emma\'s fun aunt, queen regent of the deep (under protest). ', 'gray'), T('Whims and winks; or, in the gown, decrees.', 'white')]
    BUTTONS = ((6, 'Her story', 'The regency, the deep, and what is coming.', 'p190/story'),)
    BURST = ['particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.7 0.4 0.05 30', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.7 0.4 0.05 16',
             'particle minecraft:flash{color:[0.4,0.95,0.9,1.0]} ~ ~1 ~ 0 0 0 0 1']
    FADE_SOUND = 'playsound minecraft:entity.dolphin.death neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'
    SUMMON_EXTRA = ['playsound minecraft:entity.dolphin.play neutral @a[distance=..20] ~ ~ ~ 0.8 1.2']
    FORM_FX = ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 20', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.8 0.4 0.05 20',
               'playsound minecraft:item.armor.equip_leather neutral @a[distance=..16] ~ ~ ~ 1 1.2']
    ENC_POSES = [(0, 'idle_a'), (30, 'idle_b'), (60, 'wave_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:bubble_pop ~ ~1.6 ~ 0.4 0.4 0.4 0.02 6'
    ADV = ('Let Them Eat Cake', 'Set a cake by the sea - and win over the queen regent with another')
    ADMIN_HINT = 'She pops up for anyone who befriended Emma and sets a cake down by the sea by day.'
    MEET_HINT = 'Right-click her holding a cake.'


RP.register(C)
item('pq_pearls', TOTEM, "Queen Pearl's Pearls", PQ_C,
     ['A rope of pearls, one of them suspiciously', 'chocolate-smudged.', ('Use: call Queen Pearl (again: call her over).', 'blue'),
      ('Sneak + use: her menu (casual / regal outfit).', 'blue'), ('Casual: whims and winks. Regal: royal decrees.', 'blue'),
      ('If she faints: 2 minutes before she can return.', 'gray'), ('"A crown is just a very heavy hat."', 'dark_gray')],
     model='bm:pq_pearls', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_pearlq', TOTEM, 'Pearl Doll', PQ_C, ['A doll of Queen Pearl - the mint swoop, the wink, the crown askew.', ('Right-click a block: set it down.', 'blue'),
                                               ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_pearlq', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_pearlq'] = 'bm:p141/doll_pearlq/use'
P141.DOLLS.append(('doll_pearlq', 'Queen Pearl', PQ_C, 'A doll of Queen Pearl - the mint swoop, the wink, the crown askew.', 'minecraft:bubble_pop',
                   'minecraft:entity.dolphin.play', 'minecraft:end_rod'))
P141.DOLL_FROM['doll_pearlq'] = ('pq_pearls', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['pq_pearls'] = (0.0, 1.72, -0.66, 0.66, -0.5, 0.5)
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(3, 3), (2, 6), (2, 9), (3, 12), (6, 14), (9, 14), (12, 12), (13, 9), (13, 6), (12, 3)]
    for x, y in pts:
        d.ellipse((x - 1, y - 1, x + 1, y + 1), fill=hexc('#fffef4'), outline=hexc('#c8c4b4'))
        d.point((x - 1, y - 1), fill=hexc('#ffffff'))
    d.ellipse((6, 13, 9, 15), fill=hexc('#5ae0d8'))
    d.point((10, 12), fill=hexc('#6a3a1a'))                                                # (the chocolate smudge)
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    R.HATS['doll_pearlq'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                  'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


STORY = [('I. The Spare', ['Ava was the heir. I was the spare - which is a polite way of saying I got to have fun.',
                           'She learned treaties and tides. I learned to swim with dolphins and hide in the kitchens.']),
         ('II. The Night', ['When the serpent came for the gem\'s heart, Ava held the palace door so Emma could escape. Leo carried her out. Ava never came back.',
                            'Emma was too small for the crown. So it landed on my head. It has never fitted.']),
         ('III. The Deep', ['We are a thousand years under the water, darling. We fled down here after the war against Democratus - our own blood, gone rogue.',
                            'The gem broke then, and its pieces flew everywhere. Some lucky souls up top found them and got their powers. We kept what was left.']),
         ('IV. What Is Coming', ['Apophiss wants what is left of the gem. He is planning something - the currents whisper about it.',
                                 'So I wear the crown, and I worry, and I eat a lot of cake. Somebody has to keep the kingdom smiling.']),
         ('V. Emma', ['She is braver than her mother ever was, and Ava was the bravest person I knew.',
                      'When Emma is ready, the crown is hers. Until then, I will keep it warm. And slightly sticky.'])]


def generate(G):
    import phase28 as P28
    fn = G.fn

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        casual, regal = f'if score @s {S("k2")} matches 0', f'if score @s {S("k2")} matches 1'
        lines = ['execute on owner if score @s bm.pqform matches 1 run scoreboard players set #pqf bm.rng 1',
                 'execute on owner unless score @s bm.pqform matches 1 run scoreboard players set #pqf bm.rng 0',
                 f'scoreboard players operation @s {S("k2")} = #pqf bm.rng',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..12] run function bm:{pfx}/great_go',
                 f'execute {idle} {casual} unless score @s {S("bc")} matches 1.. if entity @e[{foe},distance=..10] run function bm:{pfx}/wink_go',
                 f'execute {idle} unless score @s {S("sc")} matches 1.. run function bm:{pfx}/whim_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/melee_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..14] run function bm:{pfx}/range_go']
        fn(f'{pfx}/whim_go', go(9, 16, 'sc', 600, face('happy', 16) + ['playsound minecraft:entity.dolphin.play neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/wink_go', go(11, 10, 'bc', 400, face('wink', 10) + ['playsound minecraft:entity.allay.item_given neutral @a[distance=..16] ~ ~ ~ 0.8 1.4']))
        fn(f'{pfx}/melee_go', go(7, 8, 'mc', 20, ['playsound minecraft:entity.player.attack.weak neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/range_go', go(8, 10, 'rc', 24, ['playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..16] ~ ~ ~ 0.4 1.8']))
        fn(f'{pfx}/great_go', go(12, 32, 'gc', 1200, face('surprised', 32) + ['playsound minecraft:entity.villager.celebrate neutral @a[distance=..24] ~ ~ ~ 1 1.4']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/melee_hit',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/range_hit',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 8 run function bm:{pfx}/whim_hit',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 4 run function bm:{pfx}/wink_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/great_hit'])
        # -- her whim (casual) / her decree's shield (regal)
        whim = ['execute on owner if entity @s[distance=..16] run tag @s add bm.pqw', f'execute store result score #r bm.rng run random value 0..{len(WHIMS) - 1}']
        for i, (eff, amp, txt) in enumerate(WHIMS):
            whim += [f'execute if score #r bm.rng matches {i} run effect give @a[tag=bm.pqw] minecraft:{eff} 30 {amp} true',
                     f'execute if score #r bm.rng matches {i} run ' + X.csay(txt, '@a[tag=bm.pqw]')]
        fn(f'{pfx}/whim', whim + ['execute as @a[tag=bm.pqw] at @s run particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.03 12', 'tag @a remove bm.pqw'])
        fn(f'{pfx}/whim_hit', [f'execute {casual} run function bm:{pfx}/whim',
                               f'execute {regal} run effect give @a[distance=..12,gamemode=!spectator] minecraft:absorption 20 1 true',
                               f'execute {regal} on owner if entity @s[distance=..20] run ' + X.csay('A royal shield. Because the decree says so. *sigh*'),
                               'particle minecraft:bubble_pop ~ ~1.4 ~ 1 0.5 1 0.05 20'])
        # -- the flick, the slap
        fn(f'{pfx}/melee_hit', hit(3) + [f'execute {regal} run scoreboard players set #pd bm.rng 5',
                                         f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/slapped'] + end)
        fn(f'{pfx}/slapped', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.1 8'])
        fn(f'{pfx}/range_hit', hit(4) + [f'execute {regal} run scoreboard players set #pd bm.rng 6',
                                         f'execute positioned ~ ~1.3 ~ facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes run function bm:{pfx}/pearl',
                                         f'execute as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/pearled'] + end)
        fn(f'{pfx}/pearl', [f'particle minecraft:end_rod ^ ^ ^{d / 2:.1f} 0 0 0 0 1' for d in range(2, 28, 3)])
        fn(f'{pfx}/pearled', [f'function bm:{pfx}/hurt', 'execute store result score #r bm.rng run random value 1..4',
                              'execute if score #r bm.rng matches 1 run effect give @s minecraft:glowing 5 0',
                              'execute if score #r bm.rng matches 1 run effect give @s minecraft:blindness 3 0',
                              'execute if score #r bm.rng matches 1 run particle minecraft:flash{color:[1.0,1.0,0.95,1.0]} ~ ~1.2 ~ 0 0 0 0 1',
                              'particle minecraft:item{item:"minecraft:white_dye"} ~ ~1.2 ~ 0.2 0.2 0.2 0.1 6'])
        # -- the wink: smitten
        fn(f'{pfx}/wink_hit', ['particle minecraft:heart ~ ~2.2 ~ 0.3 0.2 0.3 0 3',
                               f'execute as @e[{foe},distance=..10,sort=nearest,limit=1] at @s run function bm:{pfx}/smitten',
                               'execute on owner if entity @s[distance=..20] run ' + X.csay('*wink* ...And down it goes. Works every time.')])
        fn(f'{pfx}/smitten', ['effect give @s minecraft:slowness 6 6', 'effect give @s minecraft:weakness 6 4', 'effect give @s minecraft:glowing 6 0',
                              'effect give @s minecraft:mining_fatigue 6 4', 'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6',
                              'playsound minecraft:entity.villager.yes neutral @a[distance=..16] ~ ~ ~ 0.4 1.8'])
        # -- the Proclamation (casual) / By Royal Decree (regal)
        fn(f'{pfx}/great_hit', [f'execute {casual} run function bm:{pfx}/holiday', f'execute {regal} run function bm:{pfx}/decree'])
        fn(f'{pfx}/holiday', ['particle minecraft:firework ~ ~2 ~ 3 1.5 3 0.1 80', 'particle minecraft:heart ~ ~2 ~ 4 1 4 0 20',
                              'playsound minecraft:entity.firework_rocket.twinkle neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                              'playsound minecraft:entity.firework_rocket.large_blast neutral @a[distance=..24] ~ ~ ~ 1 1',
                              f'execute as @e[{foe},distance=..12] at @s run function bm:{pfx}/smitten',
                              'effect give @a[distance=..12,gamemode=!spectator] minecraft:strength 15 0 true',
                              'effect give @a[distance=..12,gamemode=!spectator] minecraft:regeneration 15 1 true',
                              'effect give @a[distance=..12,gamemode=!spectator] minecraft:speed 15 0 true',
                              'execute store result score #r bm.rng run random value 1..2',
                              'summon minecraft:item ~ ~1.2 ~ {Item:{id:"minecraft:emerald",count:1},PickupDelay:10,Motion:[0.0,0.3,0.0]}',
                              'execute if score #r bm.rng matches 2 run summon minecraft:item ~ ~1.2 ~ {Item:{id:"minecraft:emerald",count:1},PickupDelay:10,Motion:[0.1,0.3,0.0]}',
                              'execute on owner if entity @s[distance=..24] run ' + X.csay('I declare a HOLIDAY! Everybody stop fighting and have FUN!')])
        fn(f'{pfx}/decree', hit(10) + ['particle minecraft:end_rod ~ ~2 ~ 4 1 4 0.05 60', 'particle minecraft:crit ~ ~1 ~ 4 0.5 4 0.2 60',
                                       'playsound minecraft:item.goat_horn.sound.0 neutral @a[distance=..32] ~ ~ ~ 1 1.2',
                                       f'execute as @e[{foe},distance=..12] at @s run function bm:{pfx}/struck',
                                       'effect give @a[distance=..12,gamemode=!spectator] minecraft:absorption 20 3 true',
                                       'execute on owner if entity @s[distance=..24] run ' + X.csay('BY ROYAL DECREE - kneel. ...There. Can I take the gown off now?')] + end)
        fn(f'{pfx}/struck', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 5 3'])
        # -- the regal decree, steady; and she grumbles about the gown now and then
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        grumble = ['This gown weighs more than a whale.', 'Who designs these sleeves? Pufferfish?', 'Is it the cape? It\'s the cape. I hate the cape.',
                   'Ava LOVED this sort of thing. I love naps.']
        fn(f'{pfx}/sec', ['effect give @s minecraft:regeneration 3 0 true', 'effect give @s minecraft:water_breathing 12 0 true',
                          f'execute {regal} on owner if entity @s[distance=..12] run effect give @s minecraft:resistance 3 0 true',
                          f'execute {regal} on owner if entity @s[distance=..12] run effect give @s minecraft:strength 3 0 true',
                          f'execute {regal} store result score #r bm.rng run random value 1..90'] +
           [f'execute {regal} if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..16,tag=!bm.hush] run ' + X.csay(g) for i, g in enumerate(grumble)])
        return lines

    def encounter(G, X):
        G.wjson('bm/advancement/p190/cake.json', {'criteria': {'set': {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
            {'condition': 'minecraft:location_check', 'predicate': {'block': {'blocks': 'minecraft:cake'}}}]}}},
            'rewards': {'function': 'bm:p190/enc/cake'}})
        fn('p190/enc/cake', ['advancement revoke @s only bm:p190/cake', 'execute if entity @s[tag=bm.pqmet] run return 0',
                             'execute unless entity @s[advancements={bm:story/emma_friend=true}] run return 0',
                             'execute store result score #nt bm.rng run time of minecraft:overworld query time', 'scoreboard players operation #nt bm.rng %= #24000 bm.bm',
                             'execute unless score #nt bm.rng matches 0..12000 run return 0',
                             'execute at @s unless biome ~ ~ ~ #minecraft:is_beach unless biome ~ ~ ~ #minecraft:is_ocean unless biome ~ ~ ~ #minecraft:is_river run return 0',
                             'execute at @s if entity @e[type=minecraft:interaction,tag=bm.pqenc,distance=..48] run return 0',
                             'execute at @s positioned ^ ^ ^3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p190/enc/pop',
                             'execute at @s run function bm:p190/enc/pop'])
        fn('p190/enc/pop', ['function bm:p190/enc/spawn', 'particle minecraft:splash ~ ~1 ~ 0.6 0.6 0.6 0.2 60', 'particle minecraft:bubble_pop ~ ~1 ~ 0.5 1 0.5 0.05 30',
                            'playsound minecraft:entity.dolphin.splash neutral @a[distance=..24] ~ ~ ~ 1 1', 'playsound minecraft:entity.dolphin.play neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                            X.tellraw('@s', [T('Splash! ', PQ_LINE, italic=True),
                                             T('A woman in an aqua dress and a crown pops up out of the surf, nose first, sniffing at your cake.', 'gray', italic=True)])])
        fn('p190/enc/talk', [f'execute if items entity @s container.* {X.holds("pq_pearls")} run return run ' + X.csay('You have my pearls, silly! Give them a jingle.'),
                             'execute if items entity @s weapon.mainhand minecraft:cake run return run function bm:p190/enc/recruit',
                             X.csay('Ooh, cake! Is there MORE cake? Bring me another and I\'ll tell you a royal secret.'),
                             'playsound minecraft:entity.dolphin.ambient neutral @s ~ ~ ~ 0.8 1.2'])
        fn('p190/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:heart ~ ~2 ~ 0.6 0.4 0.6 0 8',
                                f'execute as {X.here} at @s run particle minecraft:firework ~ ~1.5 ~ 0.6 0.6 0.6 0.1 30',
                                f'execute as {X.here} at @s run playsound minecraft:entity.villager.celebrate neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                                X.cchat('ANOTHER cake! Oh, you absolute treasure. Here\'s the royal secret: I\'m Queen Pearl. Emma\'s aunt!'),
                                X.cchat('Don\'t tell the council - I\'m supposed to be "governing". Take my pearls. Jingle them and I\'ll come running. Literally anything beats paperwork.'),
                                'function bm:p190/enc/joined'])

    RP.build(C, G, abilities, encounter)
    pages = [P28.body([T(t, PQ_C, bold=True), T('\n' + '\n'.join(p), 'gray')], 340) for t, p in STORY]
    sdlg = P28.multi([T("QUEEN PEARL'S STORY", PQ_C, bold=True)], pages, [P28.btn([T('« Back', 'gray')], C.MENU + 5, width=150)], columns=1, exit_label='Close')
    fn('p190/story', [f'scoreboard players set @s bm.menu {C.MENU}', f'dialog show @s {snbt(sdlg)}'])
