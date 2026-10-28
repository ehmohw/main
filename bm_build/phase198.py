"""2.90: MR. CAPSHUN - the narrator. (capshun_art.py, after the owner's sketch; the machinery is rigpet's.)
A stick figure, and completely flat: one of the Buddies, the strange folk born of pure imagination (Fishy, the Count, Eggbert and
Batty are Buddies too - nobody quite knows how they came to be, only that the Ethereal Gem had something to do with it). He fights
with a paintbrush and a pencil, both as flat as he is. He also narrates. Constantly. He knows a great deal about the Underwater
Kingdom's history - and, worryingly, that he's in a video game.

FINDING HIM: spend time near a painting you've hung (any painting, anywhere in the Overworld) - sooner or later a doodle peels itself
  off the canvas and steps out. Right-click him holding any dye and he's yours: he hands over his pencil.
MR. CAPSHUN'S PENCIL  use: call him (again: call him over); sneak + use: his menu - sit / send home, his ways, the wardrobe, and:
PALETTE        (his menu) the colour of the coat he paints on you: red (Strength), orange (Fire Resistance), yellow (Haste),
               green (Regeneration), blue (Speed), purple (Resistance) - or rainbow, a different one every coat.
THE STORY SO FAR  (his menu) he narrates. Lore, mostly. Some of it he shouldn't know.
FRESH COAT     every 30 s, beside you: he paints you (and anyone with you) in your palette's colour - 40 s of its buff.
(2.94: ONE TOOL AT A TIME - the pencil for what he draws, the paintbrush for what he paints; he swaps them as he goes.)
BRUSH SWIPE    a foe within 3, every second: the brush, and a splash of colour (8) - it burns, slows, lights up, poisons or lifts.
DRAWN TO LIFE  every 5 s, a foe 4-16 away: he sketches something in pencil - and it's real: a SKETCH BOMB (thrown: 9, and 6 to all
               round it), a SKETCH ANVIL (dropped on its head: 12, and dazed) or three SKETCH ARROWS (4 each).
PAINT SPLAT    every 4 s, a foe 4-14 away: a glob of paint (8) - and its colour does something: red burns, blue slows, yellow
               lights them up and weakens them, green poisons, purple lifts them off their feet.
SKETCH         every 15 s, a foe within 10: he scribbles an outline round it - it can barely move or hit for 3 s (and takes 4).
WET PAINT      three or more foes within 6, every 25 s: he slaps the brush across the ground - a puddle of paint; they're stuck in it.
THE RAINBOW STROKE  (charged, every minute) the brush raised high and swept over in a great arc: every foe within 8 takes 14, slowed
               and lit up; Strength and Regeneration for you.
NARRATION      when you're badly hurt, he says so. Helpfully. Dramatically.
Right-click him: sit / stand. A frame keeps him (he climbs out of pictures - it's what he does), a display case shows him as a
figurine, Cecil sells his doll, the Ember Rat a golden one, the Tailor his inks (and his aura, Rainbow Doodles), the Recruiter his Raid
Contract."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import capshun_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase210 as FXS
import phase212 as P212

MZ_C, MZ_LINE = '#f0f0f0', '#d8e4ff'
W = 'capshun'
PAL = [('Red', '#ff4040', 'Strength', 'strength', (1.0, 0.25, 0.25)), ('Orange', '#ff9a30', 'Fire Resistance', 'fire_resistance', (1.0, 0.6, 0.18)),
       ('Yellow', '#ffe040', 'Haste', 'haste', (1.0, 0.88, 0.2)), ('Green', '#50d060', 'Regeneration', 'regeneration', (0.3, 0.82, 0.36)),
       ('Blue', '#4a8aff', 'Speed', 'speed', (0.28, 0.52, 1.0)), ('Purple', '#b060ff', 'Resistance', 'resistance', (0.68, 0.36, 1.0))]
COAT_CD = 600                                   # (ticks between coats)
SPLATS = [('red', (1.0, 0.2, 0.2), ['data merge entity @s {Fire:80s}']), ('blue', (0.25, 0.45, 1.0), ['effect give @s minecraft:slowness 3 1']),
          ('yellow', (1.0, 0.88, 0.15), ['effect give @s minecraft:glowing 4 0', 'effect give @s minecraft:weakness 3 0']),
          ('green', (0.3, 0.85, 0.3), ['effect give @s minecraft:poison 3 0']), ('purple', (0.7, 0.3, 1.0), ['effect give @s minecraft:levitation 1 1'])]
RAINBOW = [(1.0, 0.2, 0.2), (1.0, 0.6, 0.15), (1.0, 0.9, 0.2), (0.3, 0.85, 0.35), (0.25, 0.5, 1.0), (0.35, 0.25, 0.85), (0.7, 0.3, 1.0)]


def dust(c, s=1.4):
    return f'minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:{s}}}'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Mr. Capshun', MZ_C, MZ_LINE, 'p198', 'mz', 'zq'
    A = A
    MENU = 2860
    PET_HP, PET_CD = 40, 120
    ITEM = 'capshun_pencil'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'surprised', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'grin', 'serious': 'determined'}
    ATTRS = dict(armor=4, attack_damage=6, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE = 0.9
    HIT = (0.7, 1.9)
    _sc = [(4 * i, ('scribble_a', 'scribble_b')[i % 2]) for i in range(5)]
    SWAP = ('tool',)                                # (2.94: the pencil or the brush - the pose says)
    _pt = [(4 * i, ('paint_a', 'paint_b')[i % 2]) for i in range(6)]
    CYCLE = {0: (160, [(0, 'idle_a'), (70, 'idle_b'), (96, 'idle_d'), (124, 'idle_c'), (146, 'idle_a')]),
             1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (200, [(0, 'sit_a'), (100, 'sit_b')]),
             6: (None, [(0, 'happy'), (10, 'wave_a'), (16, 'wave_b'), (22, 'wave_a')]),
             7: (None, [(0, 'swipe_up'), (4, 'swipe')]),
             8: (None, [(0, 'scribble_a'), (4, 'scribble_b'), (8, 'scribble_a'), (12, 'toss_up'), (16, 'toss')]),
             9: (None, [(0, 'fling_up'), (5, 'fling')]),
             11: (None, _sc + [(20, 'scribble_b')]),
             12: (None, [(0, 'rainbow_a'), (14, 'rainbow_b'), (22, 'rainbow_c'), (40, 'happy')]),
             13: (None, [(0, 'swipe_up'), (6, 'splash')]),
             14: (None, _pt),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 20, 'idle_d': 12, 'idle_b': 12, 'idle_c': 10, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3,
           'jump': 4, 'sit_a': 20, 'sit_b': 24, 'swipe_up': 3, 'swipe': 2, 'toss_up': 3, 'toss': 2, 'fling_up': 4, 'fling': 2, 'scribble_a': 3, 'scribble_b': 3,
           'rainbow_a': 10, 'rainbow_b': 6, 'rainbow_c': 5, 'splash': 3, 'paint_a': 3, 'paint_b': 3, 'happy': 6, 'wave_a': 5, 'wave_b': 5}
    CYCLE[16] = (None, [(0, 'ride')])                   # (2.96c: riding Bender - phase234 seats him)
    DUR['ride'] = 6
    QUIPS = ['[Mr. Capshun narrates: "And so our hero pressed on - bravely, if a little lost."]',
             '"Fun fact: the Underwater Kingdom wasn\'t always underwater. They don\'t put that on the loading screen."',
             '"I\'ve read ahead. The Ethereal Gem? Big deal. Keep an eye on it."',
             '[Mr. Capshun narrates: "The monster fell. The crowd went wild. The crowd was me."]',
             '"Technically I\'m a stack of display entities riding an invisible wolf. Please don\'t tell the others."',
             '"Democratus went rogue because his family wouldn\'t use the gem to help anyone. ...I wasn\'t supposed to say that yet. Whoops."',
             '"Is this a cutscene? Should I stand still? I never know."',
             '"Your inventory\'s getting full. Just saying. Narrators notice these things."',
             '"Don\'t turn sideways around me. I disappear. It\'s a whole thing."',
             '"Who writes this stuff? ...Oh. Hi."',
             '[Mr. Capshun narrates: "Somewhere, the serpent stirred. Probably. I\'d check the next update."]',
             '"Fishy says hello. Fishy always says hello. We\'re both Buddies - born of pure imagination. Don\'t ask me how. Ask the gem."']
    HELLO = ('[Mr. Capshun narrates: "And then he came running - in a straight line, because he\'s mostly straight lines."]',
             '[Mr. Capshun steps out of thin air, holding a caption: "ENTER: MR. CAPSHUN."]',
             '"Exit, stage left. Don\'t skip my next scene."')
    SIT = ('"Back on my feet. Well. Lines."', '[Mr. Capshun narrates: "He sat. It was the most relatable thing he\'d done all day."]')
    FAINT = 'Tell... the narrator... I mean, tell ME... ugh. Respawn me.'
    NOT_YOURS = '"Wrong protagonist, sorry. I\'m contractually someone else\'s narrator."'
    POWERS = [('Fresh Coat', 'every 30 s beside you: he paints you (and anyone with you) in your palette\'s colour - 40 s of its buff'),
              ('Palette', 'red Strength, orange Fire Resistance, yellow Haste, green Regeneration, blue Speed, purple Resistance - or rainbow, a new one every coat'),
              ('Brush Swipe', 'a foe within 3, every second: his brush, and a splash of colour (8) - it burns, slows, lights up, poisons or lifts'),
              ('Drawn to Life', 'every 5 s, a foe 4-16 away: he sketches it in pencil and it\'s real - a bomb (9, and 6 round it), an anvil (12, dazed) or three arrows (4 each)'),
              ('Paint Splat', 'every 4 s, a foe 4-14 away (8): red burns, blue slows, yellow lights up and weakens, green poisons, purple lifts it off its feet'),
              ('Sketch', 'every 15 s: he scribbles an outline round a foe within 10 - it can barely move or hit for 3 s'),
              ('Wet Paint', 'three or more foes within 6, every 25 s: a puddle of paint they\'re stuck in'),
              ('The Rainbow Stroke', 'charged, every minute: every foe within 8 takes 14, slowed and lit up; Strength and Regeneration for you'),
              ('Narration', 'when you\'re badly hurt, he narrates it. It doesn\'t help. It\'s very dramatic.')]
    INTRO = [T('Mr. Capshun', '#ffffff', bold=True), T(' - a Buddy: one of the strange folk born of pure imagination, like Fishy, the Count, Eggbert and Batty. ', 'gray'),
             T('He narrates. He knows a lot about the Underwater Kingdom. He knows he\'s in a game. He\'s very sorry about all of it.', 'white')]
    BUTTONS = ((6, 'Palette', 'Pick the colour of the coat he paints on you.', 'p198/pal'),
               (7, 'The story so far', 'He narrates. Whether you like it or not.', 'p198/story'))
    BURST = [f'particle {dust(c, 1.3)} ~ ~1 ~ 0.4 0.6 0.4 0 6' for c in RAINBOW[::2]] + ['particle minecraft:poof ~ ~0.6 ~ 0.4 0.4 0.4 0.03 10']
    FADE_SOUND = 'playsound minecraft:item.book.page_turn neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:item.book.page_turn neutral @a[distance=..24] ~ ~ ~ 1 1.3']
    ENC_POSES = [(0, 'idle_a'), (40, 'wave_a'), (50, 'wave_b'), (60, 'idle_a')]
    ENC_PARTICLE = f'execute if score #f bm.rng matches 20 run particle {dust(RAINBOW[2], 1.0)} ~ ~1.4 ~ 0.3 0.4 0.3 0 4'
    ADV = ('Previously, on Black Market...', 'Meet Mr. Capshun - and give him a little colour')
    ADMIN_HINT = 'He steps out of a hung painting now and then (stand near one in the Overworld).'
    MEET_HINT = 'Right-click him holding any dye.'


RP.register(C)
item('capshun_pencil', TOTEM, "Mr. Capshun's Pencil", MZ_C,
     ['A yellow pencil, well chewed at the eraser end.', 'Somebody has written "PROPERTY OF THE NARRATOR" down the side.',
      ('Use: call Mr. Capshun (again: call him over).', 'blue'), ('Sneak + use: his menu - his palette, and the story so far.', 'blue'),
      ('He paints you in colour, splats foes in it, and narrates.', 'blue'), ('If he faints: 2 minutes before he can return.', 'gray'),
      ('"Previously, on Black Market..."', 'dark_gray')],
     model='bm:capshun_pencil', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_capshun', TOTEM, 'Mr. Capshun Doll', MZ_C, ['A doll of Mr. Capshun - flat as a pancake.', ('Right-click a block: set it down.', 'blue'),
                                                     ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_capshun', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_capshun'] = 'bm:p141/doll_capshun/use'
P141.DOLLS.append(('doll_capshun', 'Mr. Capshun', MZ_C, 'A doll of Mr. Capshun - flat as a pancake.', 'minecraft:wax_on',
                   'minecraft:item.book.page_turn', 'minecraft:poof'))
P141.DOLL_FROM['doll_capshun'] = ('capshun_pencil', {'kh': 1.7, 'kb': 0.7, 'kl': 0.5, 'groups': {'bm:mz_shinr': 'legs', 'bm:mz_shinl': 'legs'}})   # (his shins are legs too; a little past the default warp - his head is big already, his body only lines)
P134.FIT['capshun_pencil'] = (0.0, 1.85, -0.3, 0.3, -0.55, 0.55)
POSES = A.POSES

# ---- his bonds (phase188 runs the pairs): with Fishy, a fellow Buddy; with the Neighbor, the other artist
import phase188 as P188
_O, _FOE = P188.O, 'type=#bm:hostile,tag=!bm.npc'
P188.VNAME['capshun'] = 'Mr. Capshun'
P188.PAIRS.update({
    'buddies': ('capshun', 'fishy', 'Imaginary Friends', '#ffffff', 'Mr. Capshun and Fishy - two Buddies, born of pure imagination',
                [f'effect give {_O} minecraft:luck 15 0 true', f'effect give {_O} minecraft:speed 3 0 true', f'effect give {_O} minecraft:night_vision 15 0 true',
                 f'execute at @s as @e[{_FOE},distance=..10] run effect give @s minecraft:glowing 3 0'],
                [('capshun', '"Fishy! My fellow Buddy! Say hello to the player."'), ('fishy', '(he blows a bubble at you. It says hello.)')],
                [('capshun', '"Fishy and I were imagined into being. By whom? The gem knows. The gem isn\'t talking."', 'fishy', '(a thoughtful blub)'),
                 ('fishy', '(he taps the glass of his bowl, pointing at you)', 'capshun', '"Yes, Fishy, that\'s the protagonist. Act natural."')]),
    'arts': ('capshun', 'neighbor', 'The Arts', '#d8b0ff', 'Mr. Capshun and the Neighbor - paint and music',
             [f'effect give {_O} minecraft:haste 15 0 true', f'effect give {_O} minecraft:jump_boost 3 0 true', f'effect give {_O} minecraft:regeneration 3 0 true'],
             [('neighbor', 'A painter! Finally, someone who appreciates a crescendo!'), ('capshun', '"And a musician! Finally, a soundtrack."')],
             [('capshun', '"Could you play something dramatic? I\'m narrating."', 'neighbor', '(he conducts a single, ominous note)'),
              ('neighbor', 'What are you painting?', 'capshun', '"Us. From the side. You\'ll have to squint - I\'m very thin."')]),
})
P188.ICON.update({'buddies': 'bm:capshun_pencil', 'arts': 'bm:capshun_pencil'})

STORY = ['"Previously: a kingdom under the sea. It wasn\'t always. A war, a thousand years ago - and the kingdom fled to the deep."',
         '"Previously: the Ethereal Gem was the kingdom\'s heart. It broke in the war. The nine gems you keep finding? Bits of it. Yes, really."',
         '"Previously: whoever found a shard found a power with it. Mostly they used it badly. Classic."',
         '"Previously: Democratus, a royal ancestor, wanted the gem\'s power used to help people. The family said no. He went rogue. Cecil was involved. Cecil is ALWAYS involved."',
         '"Previously: Queen Ava. Killed by Apophiss. Still around - as a ghost. Ghosts in this world are very polite about it."',
         '"Previously: Pearl rules as queen regent while Emma grows up. Emma does not know how much paperwork that is."',
         '"Previously: the Hollow King had power that wasn\'t his - it came from Apophiss. Spoilers. I mean... foreshadowing."',
         '"Previously: King Omega\'s island is cursed. He\'s lovely, once you get past the screaming."',
         '"Previously: the serpent has a new campaign. I\'ve seen the patch notes. You\'ll want better armour."',
         '"Previously: the Buddies. Fishy, the Count, Eggbert, Batty - and me. Born of pure imagination. The gem had something to do with it. I\'m still not sure whose imagination."',
         '"Previously: you hung a painting, and I walked out of it. Nobody questioned this. I love this world."',
         '"Previously: you were in a menu. You still are. Hello."']
NARRATE = ['[Mr. Capshun narrates: "Our hero was down to a handful of hearts. Dramatic music swelled."]',
           '[Mr. Capshun narrates: "Things were going badly. Very badly. Somebody should eat something."]',
           '[Mr. Capshun narrates: "And here, dear reader, is where most heroes would retreat."]',
           '[Mr. Capshun narrates: "The red bar was getting very short. The narrator was getting very nervous."]',
           '[Mr. Capshun narrates: "Little did our hero know, a potion would have been REALLY helpful right about now."]']


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(10):                                                                      # the pencil: corner to corner
        x, y = 3 + i, 12 - i
        d.point((x, y), fill=hexc('#f6c83a')); d.point((x + 1, y), fill=hexc('#c8961a'))
    d.point((2, 13), fill=hexc('#e8c49a')); d.point((1, 14), fill=hexc('#3a3a40'))
    d.point((13, 2), fill=hexc('#c0c4cc')); d.point((14, 2), fill=hexc('#c0c4cc'))
    d.point((14, 1), fill=hexc('#f08aa0')); d.point((15, 1), fill=hexc('#f08aa0')); d.point((14, 0), fill=hexc('#f08aa0'))
    for i, c in enumerate(('#ff3a3a', '#ffd02a', '#2a7aff')):                                  # a smear of the three primaries
        d.line((2 + 4 * i, 3 + i, 5 + 4 * i, 3 + i), fill=hexc(c))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    for k in SKETCHES:                                   # (2.94: what he draws - flat pencil sketches, as he is)
        face = {'uv': [0, 0, 16, 16], 'texture': '#f'}
        R.HATS[f'mz_sk_{k}'] = ({'f': f'bm:block/mz_sk_{k}'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False,
                                                                'faces': {'north': face, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


SKETCHES = ('bomb', 'anvil', 'arrow')


def textures():
    import os
    from PIL import Image
    T_ = A.textures()
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref', 'pixellab', 'capshun')
    for k in SKETCHES:
        T_[f'mz_sk_{k}'] = Image.open(os.path.join(D, f'sketch_{k}.png')).convert('RGBA')
    return T_


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    import phase28 as P28
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    say = lambda txt, col=MZ_LINE: title('@s', 'actionbar', T(txt, col))
    csay = lambda txt: title('@s', 'actionbar', [T('Mr. Capshun: ', MZ_C, bold=True), T(txt, MZ_LINE)])
    chat = lambda txt: tellraw('@s', [T('Mr. Capshun: ', MZ_C, bold=True), T(txt, MZ_LINE, italic=True)])
    pet = 'bm.mzpet'
    M = C.MENU
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.mzpal dummy', 'scoreboard objectives add bm.mzrb dummy', 'scoreboard objectives add bm.mznr dummy']
    G.OBJECTIVES += ['bm.mzpal', 'bm.mzrb', 'bm.mznr']
    wjson('bm/tags/item/mz_dyes.json', {'values': [f'minecraft:{c}_dye' for c in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray',
                                                                                  'light_gray', 'cyan', 'purple', 'blue', 'brown', 'green', 'red', 'black')]})

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..10] run function bm:{pfx}/rainbow_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..6]',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/wet_go',
                 f'execute {idle} unless score @s {S("sc")} matches 1.. if entity @e[{foe},distance=..10] run function bm:{pfx}/sketch_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/melee_go',
                 f'execute {idle} unless score @s {S("k2")} matches 1.. unless entity @e[{foe},distance=..4] if entity @e[{foe},distance=..16] run function bm:{pfx}/draw_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3.5] if entity @e[{foe},distance=..14] run function bm:{pfx}/splat_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..6] if function bm:{pfx}/near_owner run function bm:{pfx}/coat_go']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..10] run return 1', 'return 0'])
        fn(f'{pfx}/melee_go', [f'function bm:{pfx}/swipe_go'])
        fn(f'{pfx}/swipe_go', go(7, 8, 'mc', 20, ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.5 1.4']))
        fn(f'{pfx}/draw_go', go(8, 22, 'k2', 100, face('squint', 22) + ['playsound minecraft:ui.cartography_table.take_result neutral @a[distance=..16] ~ ~ ~ 0.8 1.5']))
        fn(f'{pfx}/splat_go', go(9, 10, 'rc', 80, face('happy', 12)))
        fn(f'{pfx}/sketch_go', go(11, 26, 'sc', 300, face('squint', 20) + ['playsound minecraft:ui.cartography_table.take_result neutral @a[distance=..16] ~ ~ ~ 0.8 1.2']))
        fn(f'{pfx}/wet_go', go(13, 24, 'bc', 500, face('serious', 16)))
        fn(f'{pfx}/rainbow_go', go(12, 50, 'gc', 1200, face('squint', 50) + ['playsound minecraft:block.amethyst_block.chime neutral @a[distance=..32] ~ ~ ~ 1.4 0.7',
                                                                             'execute on owner if entity @s[distance=..24] run ' + X.csay('[Mr. Capshun narrates: "And now - the big finish."]')]))
        fn(f'{pfx}/coat_go', go(14, 24, 'k', COAT_CD, face('happy', 24) + ['playsound minecraft:item.dye.use neutral @a[distance=..16] ~ ~ ~ 1 1.2']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 3 run function bm:{pfx}/swipe',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8..21 run function bm:{pfx}/scribbling',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/draw',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 4 run function bm:{pfx}/splat',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 6..25 run function bm:{pfx}/scribbling',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 6 run function bm:{pfx}/sketch',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 26..49 run function bm:{pfx}/rainbow_tick',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 26 run function bm:{pfx}/rainbow',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 16 run function bm:{pfx}/wet',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 12 run function bm:{pfx}/coat'])
        # a splash of colour (as the foe): one of five, and what it does
        fn(f'{pfx}/colour', ['execute store result score #c bm.rng run random value 1..5'] +
           [l for i, (_n, c, fx) in enumerate(SPLATS) for l in [f'execute if score #c bm.rng matches {i + 1} run particle {dust(c, 2.0)} ~ ~1 ~ 0.4 0.5 0.4 0 18'] +
            [f'execute if score #c bm.rng matches {i + 1} run {x}' for x in fx]])
        fn(f'{pfx}/smear', [f'particle {dust(c, 1.2)} ~ ~1 ~ 0.3 0.4 0.3 0 3' for c in RAINBOW[::3]])
        # BRUSH SWIPE: up close, a splash of colour (2.94: PixelLab's splash)
        fn(f'{pfx}/swipe', hit(8) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/swiped'] + end)
        fn(f'{pfx}/swiped', [f'function bm:{pfx}/hurt', FXS.fx('capshun_splash', 3.0, 1.0), f'function bm:{pfx}/colour',
                             'playsound minecraft:block.slime_block.hit neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'])
        # DRAWN TO LIFE (2.94): one of three pencil sketches, made real - black-and-white, PixelLab's
        pjs = '@e[type=minecraft:wolf,tag=bm.mzpet]'
        lead = ['particle minecraft:dust{color:[0.12,0.12,0.12],scale:0.6} ~ ~ ~ 0.05 0.05 0.05 0 1']
        bomb = P212.projectile(G, 'mz_bomb', 'bm:mz_sk_bomb', 9, pjs, scale=0.9, fxname='capshun_scribble', trail=lead,
                               on_hit=['scoreboard players set #pd bm.rng 6', 'execute store result storage bm:tmp p212.d int 1 run scoreboard players get #pd bm.rng',
                                       f'execute as @e[{foe},distance=0.1..3] run function bm:p212/dmg with storage bm:tmp p212',
                                       'playsound minecraft:entity.generic.explode neutral @a[distance=..16] ~ ~ ~ 0.6 1.6', FXS.fx('capshun_scribble', 2.4, 0.8)])
        arrow = P212.projectile(G, 'mz_arrow', 'bm:mz_sk_arrow', 4, pjs, scale=0.6, fxname='capshun_scribble', trail=lead,
                                on_hit=['playsound minecraft:entity.arrow.hit neutral @a[distance=..16] ~ ~ ~ 0.6 1.2'])
        fn(f'{pfx}/d_bomb', bomb)
        fn(f'{pfx}/d_arrow', arrow)
        aim = f'facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes positioned ^-0.4 ^1.4 ^0.6'
        fn(f'{pfx}/draw', hit(12) + ['execute store result score #r bm.rng run random value 1..3',
                                     f'execute if score #r bm.rng matches 1 {aim} run function bm:{pfx}/d_bomb',
                                     f'execute if score #r bm.rng matches 2 as @e[{foe},distance=..16,sort=nearest,limit=1] at @s run function bm:{pfx}/d_anvil'] +
           [f'execute if score #r bm.rng matches 3 {aim} rotated ~{d} ~ run function bm:{pfx}/d_arrow' for d in (-9, 0, 9)] +
           ['playsound minecraft:item.book.page_turn neutral @a[distance=..16] ~ ~ ~ 0.8 1.4',
            f'execute on owner if entity @s[distance=..24,tag=!bm.hush] if score #r bm.rng matches 2 run ' + X.csay('[Mr. Capshun narrates: "And then - an anvil. Where did it come from? Me. I drew it."]')] + end)
        anv = snbt({'Tags': ['bm.mzanv', 'bm.mzanvnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:mz_sk_anvil'}},
                    'item_display': 'fixed', 'billboard': 'center', 'teleport_duration': Int(1), 'view_range': F(1.5),
                    'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(1.4)] * 3}})
        fn(f'{pfx}/d_anvil', [f'summon minecraft:item_display ~ ~5 ~ {anv}', 'scoreboard players operation @e[type=minecraft:item_display,tag=bm.mzanvnew,distance=..6] bm.pid = #me bm.pid',
                              'scoreboard players set @e[type=minecraft:item_display,tag=bm.mzanvnew,distance=..6] bm.pjt 0',
                              'tag @e[type=minecraft:item_display,tag=bm.mzanvnew] remove bm.mzanvnew', 'playsound minecraft:ui.cartography_table.take_result neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
        X.tick.append('execute as @e[type=minecraft:item_display,tag=bm.mzanv] at @s run function bm:p198/anvil_fall')
        fn('p198/anvil_fall', ['scoreboard players add @s bm.pjt 1', 'tp @s ~ ~-0.55 ~',
                               'execute if score @s bm.pjt matches 9.. run return run function bm:p198/anvil_land',
                               'execute unless block ~ ~-0.6 ~ #bm:grap_pass run function bm:p198/anvil_land'])
        fn('p198/anvil_land', ['scoreboard players operation #me bm.pid = @s bm.pid',
                               f'execute as {pjs} if score @s bm.pid = #me bm.pid run tag @s add bm.pjme', 'scoreboard players set #pd bm.rng 12',
                               'execute store result storage bm:tmp p212.d int 1 run scoreboard players get #pd bm.rng',
                               f'execute positioned ~ ~-1 ~ as @e[{foe},distance=..1.8] run function bm:p198/anvilled', 'tag @e[tag=bm.pjme] remove bm.pjme',
                               FXS.fx('capshun_scribble', 2.0, 0.0), 'playsound minecraft:block.anvil.land neutral @a[distance=..16] ~ ~ ~ 0.8 1.0', 'kill @s'])
        fn('p198/anvilled', ['function bm:p212/dmg with storage bm:tmp p212', 'effect give @s minecraft:slowness 3 2', 'effect give @s minecraft:nausea 4 0'])
        G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.mzanv]')
        # PAINT SPLAT: a trail of paint to the foe, then the glob
        fn(f'{pfx}/splat', hit(8) + [f'execute positioned ~ ~1.2 ~ facing entity @e[{foe},distance=..14,sort=nearest,limit=1] eyes run function bm:{pfx}/trail',
                                     f'execute as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/splatted',
                                     'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 0.8 1.3'] + end)
        fn(f'{pfx}/trail', [f'particle {dust(RAINBOW[i % 7], 1.1)} ^ ^ ^{1 + 1.5 * i:.1f} 0.05 0.05 0.05 0 2' for i in range(9)])
        fn(f'{pfx}/splatted', [f'function bm:{pfx}/hurt', f'function bm:{pfx}/colour', 'playsound minecraft:block.honey_block.place neutral @a[distance=..16] ~ ~ ~ 1 1.1'])
        # SKETCH: scribbles - then the outline closes round it
        fn(f'{pfx}/scribbling', [f'particle {dust((0.08, 0.08, 0.08), 0.7)} ^ ^1.6 ^0.8 0.25 0.2 0.05 0 2'])
        fn(f'{pfx}/sketch', hit(4) + [f'execute as @e[{foe},distance=..10,sort=nearest,limit=1] at @s run function bm:{pfx}/sketched'] + end)
        ring = [f'particle {dust((0.08, 0.08, 0.08), 0.9)} ~{0.7 * math.cos(a / 8 * 6.283):.2f} ~{y} ~{0.7 * math.sin(a / 8 * 6.283):.2f} 0 0 0 0 1'
                for a in range(8) for y in (0.2, 1.0, 1.8)]
        fn(f'{pfx}/sketched', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 3', 'effect give @s minecraft:weakness 3 1', 'effect give @s minecraft:glowing 3 0'] + ring +
           ['playsound minecraft:ui.cartography_table.take_result neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
        # WET PAINT: a puddle round him
        fn(f'{pfx}/wet', [f'particle {dust(c, 1.8)} ~ ~0.1 ~ 2.2 0.05 2.2 0 20' for c in RAINBOW[::2]] +
           [f'execute as @e[{foe},distance=..6] run effect give @s minecraft:slowness 5 2', 'playsound minecraft:block.mud.place neutral @a[distance=..16] ~ ~ ~ 1.2 0.7',
            f'execute on owner if entity @s[distance=..10] run function bm:{pfx}/coat_me'])
        # THE RAINBOW STROKE: the arc drawn band by band as the brush sweeps over, then everything under it
        arc = []
        for b, c in enumerate(RAINBOW):
            r = 3.2 - 0.18 * b
            arc += [f'particle {dust(c, 1.5)} ^{r * math.cos(math.radians(a)):.2f} ^{0.6 + r * math.sin(math.radians(a)):.2f} ^2.5 0 0 0 0 1' for a in range(0, 181, 15)]
        fn(f'{pfx}/rainbow_tick', [f'particle {dust(RAINBOW[0], 1.0)} ^0.4 ^2.4 ^0.6 0.1 0.1 0.1 0 2'])
        fn(f'{pfx}/rainbow', hit(14) + arc + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/rainbowed',
                                               'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..32] ~ ~ ~ 1.6 1.2',
                                               'playsound minecraft:entity.player.levelup neutral @a[distance=..32] ~ ~ ~ 0.6 1.6',
                                               'execute on owner if entity @s[distance=..24] run effect give @s minecraft:strength 10 0 true',
                                               'execute on owner if entity @s[distance=..24] run effect give @s minecraft:regeneration 5 1 true'] + end)
        fn(f'{pfx}/rainbowed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:glowing 4 0', f'function bm:{pfx}/smear'])
        # FRESH COAT: on you (and whoever's with you)
        fn(f'{pfx}/coat', [f'execute on owner if entity @s[distance=..10] run function bm:{pfx}/coat_me'])
        coat = ['execute unless score @s bm.mzpal matches 0..6 run scoreboard players set @s bm.mzpal 6', 'scoreboard players operation #pc bm.rng = @s bm.mzpal',
                'execute if score #pc bm.rng matches 6 run scoreboard players add @s bm.mzrb 1', 'execute if score #pc bm.rng matches 6 run scoreboard players operation @s bm.mzrb %= #6 bm.rng',
                'execute if score #pc bm.rng matches 6 run scoreboard players operation #pc bm.rng = @s bm.mzrb']
        for i, (nm, col, buff, eff, c) in enumerate(PAL):
            coat += [f'execute if score #pc bm.rng matches {i} run effect give @a[distance=..6] minecraft:{eff} 40 0 true',
                     f'execute if score #pc bm.rng matches {i} as @a[distance=..6] at @s run particle {dust(c, 1.6)} ~ ~1 ~ 0.35 0.6 0.35 0 24',
                     f'execute if score #pc bm.rng matches {i} run ' + title('@s', 'actionbar', [T('Mr. Capshun: ', MZ_C, bold=True), T('(a fresh coat of ', MZ_LINE), T(nm.lower(), col, bold=True),
                                                                                                    T(' - ', MZ_LINE), T(buff, col), T(')', MZ_LINE)])]
        fn(f'{pfx}/coat_me', coat + ['playsound minecraft:item.dye.use player @s ~ ~ ~ 1 1.1'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #6 bm.rng 6']
        # NARRATION: badly hurt, he says so (every 45 s at most)
        X.second.append('scoreboard players remove @a[scores={bm.mznr=1..}] bm.mznr 1')
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s on owner if entity @s[distance=..24] unless score @s bm.mznr matches 1.. run function bm:{pfx}/narrate_check')
        fn(f'{pfx}/narrate_check', ['execute store result score #hp bm.rng run data get entity @s Health', 'execute if score #hp bm.rng matches 11.. run return 0',
                                    'scoreboard players set @s bm.mznr 45', 'execute store result score #r bm.rng run random value 1..' + str(len(NARRATE)), 'execute if entity @s[tag=bm.hush] run return 0'] +
           [f'execute if score #r bm.rng matches {i + 1} run ' + X.csay(l) for i, l in enumerate(NARRATE)])
        return lines

    def encounter(G, X):
        # near a painting, now and then: a doodle peels itself off the canvas and steps out
        X.second.append('execute as @a[tag=!bm.mzmet,gamemode=!spectator] at @s if dimension minecraft:overworld if entity @e[type=minecraft:painting,distance=..8] run function bm:p198/enc/roll')
        fn('p198/enc/roll', ['execute store result score #r bm.rng run random value 1..240', 'execute unless score #r bm.rng matches 1 run return 0',
                             'execute if entity @e[type=minecraft:interaction,tag=bm.mzenc,distance=..64] run return 0',
                             'execute as @e[type=minecraft:painting,distance=..8,sort=nearest,limit=1] at @s rotated as @s positioned ^ ^ ^1 run function bm:p198/enc/drop1',
                             'execute unless entity @e[type=minecraft:interaction,tag=bm.mzenc,distance=..12] positioned ^ ^ ^2 run function bm:p198/enc/step'])
        # (down to the floor in front of the painting - three blocks at most - then out, if there's room)
        for k in (1, 2, 3):
            fn(f'p198/enc/drop{k}', [f'execute if block ~ ~-1 ~ #bm:grap_pass positioned ~ ~-1 ~ run return run function bm:p198/enc/drop{k + 1}', 'function bm:p198/enc/drop4'])
        fn('p198/enc/drop4', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass align y run function bm:p198/enc/step'])
        fn('p198/enc/step', ['function bm:p198/enc/spawn', f'particle {dust(RAINBOW[0], 1.4)} ~ ~1 ~ 0.4 0.6 0.4 0 10', f'particle {dust(RAINBOW[4], 1.4)} ~ ~1 ~ 0.4 0.6 0.4 0 10',
                             'playsound minecraft:item.book.page_turn neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                             X.tellraw('@a[tag=!bm.mzmet,distance=..12]', [T('A doodle peels itself off the painting ', MZ_LINE, italic=True),
                                                                            T('- a stick figure, completely flat - steps down, looks at you, and holds up a little caption: ', 'gray', italic=True),
                                                                            T('"ENTER: MR. CAPSHUN. (He\'d love a bit of colour.)"', '#ffffff', italic=True)])])
        fn('p198/enc/talk', [f'execute if items entity @s container.* {X.holds("capshun_pencil")} run return run ' + csay('"You already have my pencil. Two of me would break the narrative."'),
                             'execute if items entity @s weapon.mainhand #bm:mz_dyes run return run function bm:p198/enc/recruit',
                             csay('"Ah. You\'ve no colour on you. I\'m mostly black and white, you see - a dye would do wonders. Any dye."'),
                             'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.4'])
        fn('p198/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle {dust(RAINBOW[2], 1.6)} ~ ~1.2 ~ 0.5 0.6 0.5 0 20',
                                f'execute as {X.here} at @s run playsound minecraft:item.dye.use neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                                X.tellraw('@s', [T('He dips a finger in the dye and draws himself a little smile. ', MZ_LINE, italic=True),
                                                 T('Then he hands you his pencil. "Chapter one," he says. "In which our hero gets a narrator."', 'gray', italic=True)]),
                                'function bm:p198/enc/joined'])

    RP.build(C, G, abilities, encounter)
    # ---- the palette (his menu): seven colours
    pbtns = [P28.btn(T(nm, col, bold=True), M + 10 + i, width=150, tooltip=T(f'A fresh coat of {nm.lower()}: {buff}.', 'gray')) for i, (nm, col, buff, _e, _c) in enumerate(PAL)]
    pbtns.append(P28.btn([T('R', '#ff4040', bold=True), T('a', '#ff9a30', bold=True), T('i', '#ffe040', bold=True), T('n', '#50d060', bold=True), T('b', '#4a8aff', bold=True),
                          T('o', '#b060ff', bold=True), T('w', '#ff60c0', bold=True)], M + 16, width=150, tooltip=T('A different colour every coat.', 'gray')))
    pbtns.append(P28.btn(T('« Back', 'gray'), M + 5, width=150))
    pdlg = P28.multi([T("MR. CAPSHUN'S PALETTE", '#ffffff', bold=True)],
                     [P28.body([T('"Pick a colour. Any colour. I\'ll paint you in it every thirty seconds or so - it\'s good for you. Probably."', MZ_LINE)], 320)],
                     pbtns, columns=2, exit_label='Close')
    fn('p198/pal', [f'scoreboard players set @s bm.menu {M}', f'dialog show @s {snbt(pdlg)}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {M + 10}..{M + 16} run return run function bm:p198/pal_act']
    fn('p198/pal_act', [f'execute unless score @s bm.menu matches {M} run return run function bm:p28/stale'] +
       [f'execute if score #act bm.pay matches {M + 10 + i} run scoreboard players set @s bm.mzpal {i}' for i in range(7)] +
       [f'execute if score #act bm.pay matches {M + 10 + i} run ' + title('@s', 'actionbar', [T('Mr. Capshun: ', MZ_C, bold=True), T('"', MZ_LINE), T(nm, col, bold=True),
                                                                                              T(f'. Bold choice. ({buff}, every coat.)"', MZ_LINE)]) for i, (nm, col, buff, _e, _c) in enumerate(PAL)] +
       [f'execute if score #act bm.pay matches {M + 16} run ' + csay('"Rainbow! Something new every coat. Chaos. I love it."'),
        'playsound minecraft:item.dye.use player @s ~ ~ ~ 1 1.2', 'function bm:p198/pal'])
    # ---- the story so far
    fn('p198/story', ['dialog clear @s', f'execute store result score #r bm.rng run random value 1..{len(STORY)}'] +
       [f'execute if score #r bm.rng matches {i + 1} run ' + chat(l) for i, l in enumerate(STORY)] + ['playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1'])
