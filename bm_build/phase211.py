"""2.94: THE SKY BUDDIES - Sunny, Snooze, Twinkle and Nimbus: the sun in his shades, the sleepy crescent moon in her nightcap
with her grumpy little star, and the ":3" cloud. Buddies, like Mr. Capshun - folk born of pure imagination - and the first
TRIO follower: they come as one (one heart between them, one of your three places), and they fight together.
(sky_art.py: the owner's painting, redrawn clean - and (2.94c) sculpted in voxels, blocky 3D you can walk round, floating.)

FINDING THEM - WITNESS THE SKY: under the open sky in the Overworld, each shows itself to you once, the first time you see
  its moment - Sunny at a clear noon, Snooze (and Twinkle) at a full-moon midnight, Nimbus in a rainstorm. Once you've seen all
  three, the trio drifts down to you together; right-click them and they hand you their summoning item, THE SKY MOBILE.
THE SKY MOBILE   use: call them (again: call them over); sneak + use: their menu - sit / send home, their ways, the wardrobe,
                 and Today's Forecast (what the sky's giving you).
SUNBEAM       Sunny, a monster within 14 every 4 s: a beam of sunlight (8 - 13 by day under the open sky), and it burns.
STAR SHOT     Twinkle, a monster 3-16 away every 2.5 s: she hurls herself, a shooting star (7, and it glows a moment).
ZAP           Nimbus, a monster within 12 every 5 s: a bolt from the cloud (7 - 13 in the rain).
LULLABY       Snooze, three or more monsters within 7, every 20 s: a lullaby - slowed to a crawl and weakened (at night longer,
              and they can't see).
DRIZZLE       you on fire, or hurt (6 hearts or less): Nimbus rains on you - Regeneration and Fire Resistance (the fire's out),
              and on the followers round you too (theirs is put out) - every 15 s at most.
WHAT THE SKY GIVES  every 30 s, beside you and no fight near: Haste by day, Night Vision and Speed at night, Regeneration in the
              rain.
THE FORECAST  (charged, every minute) all three at once - sunbeams on the three nearest monsters, a shower of stars, a bolt, and a
              lullaby: every monster within 9 takes 16, set alight, slowed and lit up.
Right-click them: sit / stand (they settle on Nimbus). A frame keeps them, a display case shows them as a figurine, Cecil sells their
doll, the Ember Rat a golden one, the Tailor their nightcaps (Bubblegum Pink, Mint Dream, Lavender Night; Gilded, Diamond and
Netherite) and their aura (Starry Sky), the Recruiter their Raid Contract; and they're on the Partner Wheel."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import sky_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase210 as FXS

SUN, SKY_LINE = '#ffd04a', '#cfe8ff'
W = 'sky'
MENU = 2940
FOE = 'type=#bm:hostile,tag=!bm.npc'
# each mood (phase95) on each of the four faces
FACES = {'happy': dict(head='grin', moon='happy', star='happy', body='happy'), 'surprised': dict(head='surprised', moon='surprised', star='surprised', body='surprised'),
         'hurt': dict(head='hurt', moon='hurt', star='hurt', body='hurt'), 'sleepy': dict(head='sleepy', moon=None, star='blink', body='blink'),
         'blink': dict(head='blink', moon=None, star='blink', body='blink'), 'squint': dict(head='grin', moon='awake', star='smug', body='happy'),
         'serious': dict(head='fierce', moon='awake', star='angry', body='angry')}


def dust(c, s=1.2):
    return f'minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:{s}}}'


GOLDD, MOOND, STARD, RAIND = (1.0, 0.82, 0.3), (0.85, 0.9, 1.0), (1.0, 0.95, 0.4), (0.45, 0.65, 1.0)


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'The Sky Buddies', SUN, SKY_LINE, 'p211', 'yb', 'yq'
    A = A
    MENU = MENU
    PET_HP, PET_CD = 60, 120
    ITEM = 'sky_mobile'
    pron, they = 'them', 'they'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {e: FACES[e]['head'] for e in EXPR}
    ATTRS = dict(armor=6, attack_damage=4, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE = 0.9
    HIT = (1.4, 2.6)
    BILLBOARD = None                         # (2.94c: blocky 3D now - turned as they are, never billboarded)
    SWAP = A.SWAP
    _lull = [(0, 'lull_a'), (8, 'lull_b'), (16, 'lull_a'), (24, 'lull_b')]
    CYCLE = {0: (160, [(0, 'idle_a'), (40, 'idle_1'), (80, 'idle_b'), (110, 'idle_3'), (140, 'idle_c')]),
             1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (200, [(0, 'sit_a'), (100, 'sit_b')]),
             6: (None, [(0, 'happy'), (10, 'wave_a'), (16, 'wave_b'), (22, 'wave_a')]),
             7: (None, [(0, 'beam_up'), (8, 'beam')]),
             8: (None, [(0, 'shot_up'), (5, 'shot')]),
             9: (None, [(0, 'zap_up'), (7, 'zap')]),
             11: (None, _lull),
             12: (None, [(0, 'forecast_a'), (14, 'forecast_b'), (36, 'happy')]),
             13: (None, [(0, 'drizzle'), (20, 'happy')]),
             14: (None, [(0, 'happy')]),
             10: (16, [(4 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_1': 30, 'idle_b': 24, 'idle_3': 26, 'idle_c': 24, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4,
           'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3, 'jump': 4, 'sit_a': 20, 'sit_b': 30, 'beam_up': 6, 'beam': 3, 'shot_up': 4, 'shot': 2,
           'zap_up': 5, 'zap': 2, 'lull_a': 8, 'lull_b': 8, 'forecast_a': 10, 'forecast_b': 6, 'drizzle': 8, 'happy': 6, 'wave_a': 5, 'wave_b': 5}
    QUIPS = ['Sunny: "Shades on, sun out. Classic."', 'Snooze: "...five more minutes..." (Twinkle glares at you. It\'s not her fault, apparently.)',
             'Nimbus: ":3"', 'Sunny: "Technically we\'re three Buddies. Four if you count Twinkle. Don\'t count Twinkle - she hates that."',
             'Twinkle: "..." (she is not amused. She is never amused.)', 'Nimbus: "I can rain on your enemies. Or your parade. Your choice! :3"',
             'Snooze: "Born of pure imagination, they say. Somebody imagined a nap. It was me."',
             'Sunny: "Mr. Capshun says hi. He also says we\'re in a video game. We\'ve stopped asking."',
             'Nimbus (whispering): "Sunny\'s been wearing those shades indoors again."', 'Sunny: "Forecast: one hundred percent chance of winning."',
             'Twinkle: "...hmph." (she twinkles, grudgingly)', 'Snooze: "Is it night yet? ...No? ...wake me when it\'s night."']
    HELLO = ('Sunny: "Coming through! Make way for the weather!"', 'Sunny: "Sun\'s up!" Snooze: "...moon\'s up..." Nimbus: ":3"', 'Nimbus: "Clearing up! See you soon!"')
    SIT = ('Sunny: "Break\'s over - back to shining!"', 'Snooze: "Oh thank goodness. A nap." (they settle down on Nimbus)')
    FAINT = 'Sunny: "Total... eclipse..." Snooze: "...goodnight..." Nimbus: "x3"'
    NOT_YOURS = 'Sunny: "Sorry, pal - we\'ve got someone else\'s sky to keep."'
    POWERS = [('Sunbeam', 'Sunny: a beam of sunlight on a monster within 14 (8 - 13 by day under the open sky), and it burns'),
              ('Star Shot', 'Twinkle: she hurls herself at a monster 3-16 away, a shooting star (7, and it glows)'),
              ('Zap', 'Nimbus: a bolt from the cloud, a monster within 12 (7 - 13 in the rain)'),
              ('Lullaby', 'Snooze: three or more monsters within 7 - slowed to a crawl and weakened; at night longer, and blinded'),
              ('Drizzle', 'you burning, or down to 6 hearts: Nimbus rains on you - Regeneration, Fire Resistance; the fire\'s out on your followers'),
              ('What the Sky Gives', 'every 30 s, no fight near: Haste by day, Night Vision and Speed at night, Regeneration in the rain'),
              ('The Forecast', 'charged, every minute: all three at once - 16 to every monster within 9, set alight, slowed and lit up'),
              ('Master of the Weather', 'their Honour at its height (Queen Ava, rank III): clear skies, rain or a storm from their menu (every 2 minutes)'),
              ('A Bed on Nimbus', 'their Honour at its height: a bed wherever you are in the Overworld - sleep the night through, and wake where you slept')]
    INTRO = [T('The Sky Buddies', SUN, bold=True), T(' - Sunny, Snooze (and Twinkle) and Nimbus. Buddies, born of pure imagination, like Mr. Capshun. ', 'gray'),
             T('Three of them, one heart: they come as one and fight as one.', 'white')]
    BUTTONS = ((6, "Today's forecast", 'What the sky is giving you right now.', 'p211/today'),
               (7, 'Change the weather', 'Their Honour at its height: clear skies, rain or a thunderstorm, at your word.', 'p211/wx/open'),
               (3, 'A bed on Nimbus', 'Their Honour at its height: Nimbus makes you a bed, wherever you are (in the Overworld).', 'p211/bed/try'))
    BURST = [f'particle {dust(GOLDD, 1.4)} ~ ~1.6 ~ 0.6 0.5 0.6 0 10', f'particle {dust(MOOND, 1.2)} ~ ~1.8 ~ 0.6 0.5 0.6 0 8',
             'particle minecraft:cloud ~ ~1.2 ~ 0.6 0.3 0.6 0.02 12', 'particle minecraft:end_rod ~ ~1.8 ~ 0.6 0.5 0.6 0.02 6']
    FADE_SOUND = 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..20] ~ ~ ~ 1 0.7'
    SUMMON_EXTRA = ['playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 1.3']
    ENC_POSES = [(0, 'idle_a'), (30, 'wave_a'), (40, 'wave_b'), (50, 'idle_1')]
    ENC_PARTICLE = f'execute if score #f bm.rng matches 20 run particle {dust(GOLDD, 1.0)} ~ ~2 ~ 0.6 0.4 0.6 0 4'
    ADV = ('Partly Sunny', 'Witness the whole sky - and meet the Sky Buddies')
    ADMIN_HINT = 'They show themselves under the open sky: a clear noon, a full-moon midnight, a rainstorm - then they come down to you.'
    MEET_HINT = 'Right-click them.'


RP.register(C)
import phase95 as _FX
_h = _FX.FOLK[W]
_FX.FOLK[W] = (_h[0], _h[1], f'type=minecraft:item_display,tag=bm.ybp,tag=bm.ybp_face,tag=bm.ybp_pet,tag=!bm.ybfade') + _h[3:]   # (all four faces take the mood)
item('sky_mobile', TOTEM, 'The Sky Mobile', SUN,
     ['A baby\'s mobile: a little sun in shades, a moon in a nightcap,', 'a grumpy star and a cloud, turning on their threads.',
      ('Use: call the Sky Buddies (again: call them over).', 'blue'), ('Sneak + use: their menu - the forecast, the wardrobe.', 'blue'),
      ('Sunbeams, star shots, zaps, lullabies - and the weather on your side.', 'blue'), ('If they faint: 2 minutes before they can return.', 'gray'),
      ('"Partly sunny, with a chance of :3"', 'dark_gray')],
     model='bm:sky_mobile', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_sky', TOTEM, 'Sky Buddies Doll', SUN, ['A doll of the Sky Buddies - all four, on one cloud.', ('Right-click a block: set it down.', 'blue'),
                                                 ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_sky', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_sky'] = 'bm:p141/doll_sky/use'
P141.DOLLS.append(('doll_sky', 'The Sky Buddies', SUN, 'A doll of the Sky Buddies - all four, on one cloud.', 'minecraft:end_rod',
                   'minecraft:block.amethyst_block.chime', 'minecraft:cloud'))
P141.DOLL_FROM['doll_sky'] = ('sky_mobile', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, 'groups': {'bm:yb_head': 'head', 'bm:yb_rays': 'head', 'bm:yb_moon': 'head',
                                                                                          'bm:yb_cap': 'head', 'bm:yb_star': 'head'}})
P134.FIT['sky_mobile'] = (0.9, 1.6, -0.6, 1.4, -0.1, 0.1)
POSES = A.POSES

# ---- their bonds (phase188 runs the pairs): with Mr. Capshun, a fellow Buddy; with Celi, the moon and the frost
import phase188 as P188
_O = P188.O
P188.VNAME['sky'] = 'the Sky Buddies'
P188.PAIRS.update({
    'daydream': ('sky', 'capshun', 'Daydreamers', '#ffe890', 'the Sky Buddies and Mr. Capshun - Buddies all, born of pure imagination',
                 [f'effect give {_O} minecraft:luck 15 0 true', f'effect give {_O} minecraft:haste 15 0 true', f'execute at @s as @e[{FOE},distance=..10] run effect give @s minecraft:glowing 3 0'],
                 [('sky', 'Sunny: "Mr. Capshun! Narrate us something sunny!"'), ('capshun', '"[And the sun shone. Mostly on Sunny. He insisted.]"')],
                 [('capshun', '"Three Buddies in one. That\'s efficient imagining."', 'sky', 'Nimbus: ":3"'),
                  ('sky', 'Snooze: "...is the narrator always this loud?..."', 'capshun', '"[He said, loudly.]"')]),
    'nightfrost': ('sky', 'celi', 'Moon and Frost', '#bcd8ff', 'the Sky Buddies and Celi - a cold clear night',
                   [f'effect give {_O} minecraft:night_vision 15 0 true', f'effect give {_O} minecraft:resistance 3 0 true', f'execute at @s as @e[{FOE},distance=..10] run effect give @s minecraft:slowness 2 0'],
                   [('celi', 'A moon in a nightcap. How... charming.'), ('sky', 'Snooze: "...thank you... I knitted it..."')],
                   [('sky', 'Twinkle: "..." (she and Celi glare at each other. Mutual respect.)', 'celi', 'Hm.'),
                    ('celi', 'Is that cloud always smiling?', 'sky', 'Nimbus: ":3"')]),
})
P188.ICON.update({'daydream': 'bm:sky_mobile', 'nightfrost': 'bm:sky_mobile'})


def extend_offers(O, offer):
    pass


def _icon():
    """the Sky Mobile: a little crossbar, four threads, the four of them hanging"""
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((7, 0, 7, 2), fill=hexc('#8a6a3a')); d.line((1, 2, 14, 2), fill=hexc('#a07a44'))
    for x, y in ((2, 3), (6, 3), (10, 3), (13, 3)):
        d.line((x, y, x, y + 2), fill=hexc('#dcdcdc'))
    d.ellipse((0, 6, 4, 10), fill=hexc('#ffc83a'), outline=hexc('#e08a1a')); d.point((1, 8), fill=hexc('#202020')); d.point((3, 8), fill=hexc('#202020'))
    d.arc((4, 5, 9, 11), 300, 120, fill=hexc('#f4eeb0')); d.point((6, 5), fill=hexc('#9ad0e8')); d.point((7, 4), fill=hexc('#9ad0e8'))
    d.polygon([(10, 7), (11, 9), (9, 9)], fill=hexc('#fff070')); d.point((10, 6), fill=hexc('#fff070'))
    d.ellipse((11, 7, 15, 11), fill=hexc('#d8d8dc'), outline=hexc('#8a8a90')); d.ellipse((9, 9, 13, 12), fill=hexc('#e4e4e8'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for p in A.FACED:                                                   # (each face: its mood's model, from phase95's string)
            cases = [{'when': e, 'model': mdl(f'yb_{p}_x{FACES[e][p]}')} for e in C.EXPR if FACES[e][p]]
            R2.wj(f'assets/bm/items/yb_{p}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': cases, 'fallback': mdl(f'yb_{p}')}})
    R.POST.append(post)                                                     # (after rigpet's head - before phase138 copies them for the looks)


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    import phase28 as P28
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col=SKY_LINE: title('@s', 'actionbar', T(txt, col))
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.ybsp dummy', 'scoreboard objectives add bm.ybvl dummy', 'scoreboard players set #8 bm.rng 8',
                              'scoreboard players set #24 bm.rng 24']
    G.OBJECTIVES += ['bm.ybsp', 'bm.ybvl']
    day = 'if score #tod bm.bm matches 0..12299'
    night = 'unless score #tod bm.bm matches 0..12299'

    def abilities(G, X):
        S, go, hit, end, face, pfx = X.S, X.go, X.hit, X.end, X.face, X.pfx
        idle = X.idle_fight
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{FOE},distance=..10] run function bm:{pfx}/forecast_go',
                 f'execute store result score #nf bm.rng if entity @e[{FOE},distance=..7]',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/lull_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. if function bm:{pfx}/needs_rain run function bm:{pfx}/drizzle_go',
                 f'execute {idle} unless score @s {S("sc")} matches 1.. if entity @e[{FOE},distance=..12] run function bm:{pfx}/zap_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. if entity @e[{FOE},distance=..14] run function bm:{pfx}/beam_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. unless entity @e[{FOE},distance=..3] if entity @e[{FOE},distance=..16] run function bm:{pfx}/shot_go',
                 f'execute {idle} unless score @s {S("k2")} matches 1.. unless entity @e[{FOE},distance=..8] if function bm:{pfx}/near_owner run function bm:{pfx}/gift_go']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..10] run return 1', 'return 0'])
        fn(f'{pfx}/needs_rain', ['execute on owner if entity @s[distance=..10] if predicate bm:p34/burning run return 1',
                                 'execute on owner if entity @s[distance=..10] store result score #hp bm.rng run data get entity @s Health',
                                 'execute on owner if entity @s[distance=..10] if score #hp bm.rng matches ..12 run return 1', 'return 0'])
        fn(f'{pfx}/beam_go', go(7, 14, 'rc', 80, face('serious', 14) + ['playsound minecraft:block.beacon.activate neutral @a[distance=..16] ~ ~ ~ 0.6 1.8']))
        fn(f'{pfx}/shot_go', go(8, 10, 'mc', 50, ['playsound minecraft:entity.firework_rocket.launch neutral @a[distance=..16] ~ ~ ~ 0.6 1.6']))
        fn(f'{pfx}/zap_go', go(9, 12, 'sc', 100, face('serious', 12) + ['playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..16] ~ ~ ~ 0.25 1.8']))
        fn(f'{pfx}/lull_go', go(11, 32, 'bc', 400, face('sleepy', 32) + ['playsound minecraft:block.note_block.chime neutral @a[distance=..16] ~ ~ ~ 1 0.7']))
        fn(f'{pfx}/forecast_go', go(12, 44, 'gc', 1200, face('squint', 44) + ['playsound minecraft:block.beacon.power_select neutral @a[distance=..32] ~ ~ ~ 1.2 0.8',
                                                                              'execute on owner if entity @s[distance=..24] run ' + X.csay('Sunny: "And now - the forecast!"')]))
        fn(f'{pfx}/drizzle_go', go(13, 24, 'k', 300, face('happy', 24) + ['playsound minecraft:weather.rain neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
        fn(f'{pfx}/gift_go', go(14, 12, 'k2', 600, face('happy', 12)))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 8..13 run particle {dust(GOLDD, 1.0)} ~ ~2.6 ~ 0.4 0.3 0.4 0 3',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 6 run function bm:{pfx}/beam',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/shot',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 5 run function bm:{pfx}/zap',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 4..30 run particle minecraft:note ~ ~2.2 ~ 0.8 0.4 0.8 1 1',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 16 run function bm:{pfx}/lull',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 30..43 run particle minecraft:end_rod ~ ~2.4 ~ 0.6 0.4 0.6 0.04 3',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 28 run function bm:{pfx}/forecast',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 4..20 on owner at @s run particle minecraft:falling_water ~ ~2.4 ~ 0.4 0.1 0.4 0 6',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 12 run function bm:{pfx}/drizzle',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 6 run function bm:{pfx}/gift'])
        # SUNBEAM: (stronger by day, under the open sky) - the beam's sprite on it, and fire
        fn(f'{pfx}/beam', hit(8) + [f'execute {day} positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set #pd bm.rng 13',
                                    f'execute as @e[{FOE},distance=..14,sort=nearest,limit=1] at @s run function bm:{pfx}/beamed',
                                    'playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.7 2'] + end)
        fn(f'{pfx}/beamed', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:80s}', FXS.fx('sky_sunbeam', 1.4, 0.0),
                             f'particle {dust(GOLDD, 1.6)} ~ ~1 ~ 0.3 1.2 0.3 0 20', 'particle minecraft:flame ~ ~1 ~ 0.3 0.6 0.3 0.02 10'])
        # STAR SHOT: Twinkle's shooting star (a bright line to it, the sprite there)
        fn(f'{pfx}/shot', hit(7) + [f'execute positioned ~ ~2 ~ facing entity @e[{FOE},distance=..16,sort=nearest,limit=1] eyes run function bm:{pfx}/trail',
                                    f'execute as @e[{FOE},distance=..16,sort=nearest,limit=1] at @s run function bm:{pfx}/starred'] + end)
        fn(f'{pfx}/trail', [f'particle {dust(STARD, 1.0)} ^ ^ ^{1 + 1.4 * i:.1f} 0.05 0.05 0.05 0 2' for i in range(11)] +
           ['particle minecraft:end_rod ^ ^ ^3 0.1 0.1 0.1 0.02 3'])
        fn(f'{pfx}/starred', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:glowing 3 0', FXS.fx('sky_star', 1.0, 1.0),
                              'playsound minecraft:entity.firework_rocket.twinkle neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
        # ZAP: (stronger in the rain)
        fn(f'{pfx}/zap', hit(7) + ['execute if predicate bm:p29/raining run scoreboard players set #pd bm.rng 13',
                                   f'execute as @e[{FOE},distance=..12,sort=nearest,limit=1] at @s run function bm:{pfx}/zapped'] + end)
        fn(f'{pfx}/zapped', [f'function bm:{pfx}/hurt', FXS.fx('sky_zap', 1.4, 0.0), 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.6 0.3 0.2 20',
                             'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'])
        # LULLABY: (at night, longer, and blinding)
        fn(f'{pfx}/lull', [FXS.fx('sky_lullaby', 1.6, 1.6), f'execute as @e[{FOE},distance=..7] run effect give @s minecraft:slowness 5 3',
                           f'execute as @e[{FOE},distance=..7] run effect give @s minecraft:weakness 5 1',
                           f'execute {night} as @e[{FOE},distance=..7] run effect give @s minecraft:slowness 9 3',
                           f'execute {night} as @e[{FOE},distance=..7] run effect give @s minecraft:blindness 4 0',
                           f'execute as @e[{FOE},distance=..7] at @s run particle minecraft:note ~ ~2 ~ 0.3 0.2 0.3 1 3',
                           'playsound minecraft:block.note_block.bell neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                           'execute on owner if entity @s[distance=..24] run ' + X.csay('Snooze: "...hush now..."')])
        # DRIZZLE: on you (and your followers' fires are put out)
        fn(f'{pfx}/drizzle', ['scoreboard players operation #me bm.pid = @s bm.pid',
                              f'execute on owner if entity @s[distance=..12] at @s run function bm:{pfx}/rained',
                              'execute on owner at @s as @e[type=!minecraft:player,distance=..8] if score @s bm.pid = #me bm.pid run data merge entity @s {Fire:0s}'])
        fn(f'{pfx}/rained', [FXS.fx('sky_drizzle', 1.6, 2.2), 'effect give @s minecraft:regeneration 6 1 true', 'effect give @s minecraft:fire_resistance 8 0 true',
                             'particle minecraft:falling_water ~ ~2.4 ~ 0.4 0.1 0.4 0 20', 'playsound minecraft:weather.rain.above player @s ~ ~ ~ 0.8 1.2',
                             title('@s', 'actionbar', [T('Nimbus: ', SUN, bold=True), T('"Drizzle! :3" (Regeneration - and the fire\'s out)', SKY_LINE)])])
        # WHAT THE SKY GIVES
        fn(f'{pfx}/gift', ['execute on owner if entity @s[distance=..12] at @s run function bm:p211/gift_me'])
        fn(f'{pfx}/forecast', hit(16) + [FXS.fx('sky_forecast', 2.6, 1.6), FXS.fx('sky_sunbeam', 1.6, 0.0),
                                        f'execute as @e[{FOE},distance=..9] at @s run function bm:{pfx}/forecasted',
                                        f'execute as @e[{FOE},distance=..9,sort=nearest,limit=3] at @s run {FXS.fx("sky_sunbeam", 1.2, 0.0)}',
                                        f'execute as @e[{FOE},distance=..9,sort=nearest,limit=1] at @s run {FXS.fx("sky_zap", 1.4, 0.0)}',
                                        'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.6 1.4',
                                        'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..32] ~ ~ ~ 1.4 1.2',
                                        'execute on owner if entity @s[distance=..24] run function bm:p211/gift_me'] + end)
        fn(f'{pfx}/forecasted', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:60s}', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:glowing 4 0',
                                 f'particle {dust(STARD, 1.4)} ~ ~2 ~ 0.4 0.6 0.4 0 10'])
        # the rays: turning slowly on their own clock (right_rotation, under every pose)
        X.tick.append(f'execute as @e[type=minecraft:item_display,tag=bm.ybp_rays] run function bm:{pfx}/spin')
        fn(f'{pfx}/spin', ['scoreboard players add @s bm.ybsp 1', 'scoreboard players operation #sp bm.rng = @s bm.ybsp', 'scoreboard players operation #sp bm.rng %= #4 bm.rng',
                           'execute unless score #sp bm.rng matches 0 run return 0', 'scoreboard players operation #sp bm.rng = @s bm.ybsp',
                           'scoreboard players operation #sp bm.rng /= #4 bm.rng', 'scoreboard players operation #sp bm.rng %= #24 bm.rng'] +
           [f'execute if score #sp bm.rng matches {i} run return run data merge entity @s {{start_interpolation:0,interpolation_duration:4,transformation:{{right_rotation:'
            f'[0f,0f,{math.sin(math.radians(-15 * (i + 1)) / 2):.4f}f,{math.cos(math.radians(-15 * (i + 1)) / 2):.4f}f]}}}}' for i in range(24)])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4']
        return lines

    def encounter(G, X):
        # WITNESS THE SKY: each moment once (open sky, the Overworld) - its Buddy shows itself; all three: they come down
        X.second.append('execute as @a[tag=!bm.ybmet,gamemode=!spectator] at @s if dimension minecraft:overworld positioned ~ ~1.6 ~ if predicate bm:sees_sky run function bm:p211/enc/sky')
        fn('p211/enc/sky', ['execute if entity @s[tag=!bm.ybs1] if score #tod bm.bm matches 5200..6800 if predicate bm:p39/clear run function bm:p211/enc/sunny',
                            # (the moon the sky shows - 2.94c: 26.3's moon timeline, the clock round a 192000-tick cycle, full for its first
                            #  24000; "time query day" is the day timeline's tick, not a day count, so the old day % 8 was no moon at all)
                            'execute store result score #mp bm.rng run time query moon',
                            'execute if entity @s[tag=!bm.ybs2] if score #tod bm.bm matches 17200..18800 if score #mp bm.rng matches ..23999 if predicate bm:p39/clear run function bm:p211/enc/snooze',
                            'execute if entity @s[tag=!bm.ybs3] if predicate bm:p29/raining run function bm:p211/enc/nimbus',
                            'execute if entity @s[tag=bm.ybs1,tag=bm.ybs2,tag=bm.ybs3] unless entity @e[type=minecraft:interaction,tag=bm.ybenc,distance=..64] run function bm:p211/enc/down'])
        vis = lambda parts, at, sc: [f'execute positioned {at} run summon minecraft:item_display ~ ~ ~ ' + snbt({
            'Tags': ['bm.ybvis'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:yb_{p}'}}, 'billboard': 'center',
            'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(4.0), 'interpolation_duration': Int(40),
            'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(sc)] * 3}})
            for p in parts]
        ahead = 'positioned ^ ^ ^24 positioned ~ ~16 ~'
        for nm, tag, parts, txt, snd in (('sunny', 'bm.ybs1', ('rays', 'head'), 'High in the clear noon sky, the sun lowers its shades and winks at you.', 'minecraft:block.beacon.activate'),
                                         ('snooze', 'bm.ybs2', ('moon', 'cap', 'star'), 'The full moon yawns, pulls her nightcap down - and her little star glares at you.', 'minecraft:block.amethyst_block.chime'),
                                         ('nimbus', 'bm.ybs3', ('back', 'body'), 'One cloud in the storm smiles down at you. It looks like a ":3".', 'minecraft:weather.rain.above')):
            fn(f'p211/enc/{nm}', [f'tag @s add {tag}', f'execute rotated ~ 0 {ahead} run function bm:p211/enc/{nm}_here', f'playsound {snd} player @s ~ ~ ~ 1 0.8',
                                  tellraw('@s', [T(txt, SKY_LINE, italic=True)]),
                                  'execute if entity @s[tag=bm.ybs1,tag=bm.ybs2,tag=bm.ybs3] run ' + tellraw('@s', [T('You\'ve seen the whole sky. ', SUN, italic=True),
                                                                                                                 T('Somewhere above you, three somebodies are deciding to come down.', 'gray', italic=True)])])
            fn(f'p211/enc/{nm}_here', vis(parts, '~ ~ ~', 12.0) + ['scoreboard players set @e[type=minecraft:item_display,tag=bm.ybvis,distance=..2] bm.ybvl 120'])
        X.second.append('scoreboard players remove @e[type=minecraft:item_display,tag=bm.ybvis] bm.ybvl 20')
        X.second.append('execute as @e[type=minecraft:item_display,tag=bm.ybvis,scores={bm.ybvl=..20}] run data merge entity @s {start_interpolation:0,interpolation_duration:20,transformation:{scale:[0f,0f,0f]}}')
        X.second.append('kill @e[type=minecraft:item_display,tag=bm.ybvis,scores={bm.ybvl=..0}]')
        fn('p211/enc/down', ['execute rotated ~ 0 positioned ^ ^ ^3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run function bm:p211/enc/land'])
        fn('p211/enc/land', ['function bm:p211/enc/spawn', 'particle minecraft:cloud ~ ~6 ~ 0.6 3 0.6 0.02 60', 'particle minecraft:end_rod ~ ~4 ~ 0.6 2 0.6 0.02 20',
                             f'particle {dust(GOLDD, 1.4)} ~ ~3 ~ 0.6 2 0.6 0 20', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                             tellraw('@s', [T('Down they drift - a sun in shades, a sleepy moon with her grumpy star, a smiling cloud - and stop in front of you. ', SKY_LINE, italic=True),
                                            T('"Hi!" says the sun. "We\'ve been watching you watch us."', 'white', italic=True)])])
        fn('p211/enc/talk', [f'execute if items entity @s container.* {X.holds("sky_mobile")} run return run ' +
                             title('@s', 'actionbar', [T('Sunny: ', SUN, bold=True), T('"You\'ve got our mobile already, pal. We\'re a set."', SKY_LINE)]),
                             'function bm:p211/enc/recruit'])
        fn('p211/enc/recruit', [f'execute as {X.here} at @s run particle {dust(GOLDD, 1.6)} ~ ~2 ~ 0.6 0.6 0.6 0 20',
                                f'execute as {X.here} at @s run playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                                tellraw('@s', [T('The cloud hands you a little mobile - the four of them, in miniature, turning on their threads. ', SKY_LINE, italic=True),
                                               T('"Hang that up," says the sun, "and we\'ll be your weather."', 'gray', italic=True)]),
                                'function bm:p211/enc/joined'])

    RP.build(C, G, abilities, encounter)
    # ---- what the sky gives (as you): by day, by night, in the rain
    fn('p211/gift_me', ['execute if predicate bm:p29/raining run return run function bm:p211/gift/rain',
                        f'execute {day} run return run function bm:p211/gift/day', 'function bm:p211/gift/night'])
    fn('p211/gift/day', ['effect give @s minecraft:haste 40 0 true', f'particle {dust(GOLDD, 1.4)} ~ ~1 ~ 0.4 0.7 0.4 0 16',
                         title('@s', 'actionbar', [T('Sunny: ', SUN, bold=True), T('"Sun\'s out!" (Haste)', SKY_LINE)])])
    fn('p211/gift/night', ['effect give @s minecraft:night_vision 40 0 true', 'effect give @s minecraft:speed 40 0 true', f'particle {dust(MOOND, 1.4)} ~ ~1 ~ 0.4 0.7 0.4 0 16',
                           title('@s', 'actionbar', [T('Snooze: ', SUN, bold=True), T('"...moonlight..." (Night Vision, Speed)', SKY_LINE)])])
    fn('p211/gift/rain', ['effect give @s minecraft:regeneration 10 0 true', f'particle {dust(RAIND, 1.4)} ~ ~1 ~ 0.4 0.7 0.4 0 16',
                          title('@s', 'actionbar', [T('Nimbus: ', SUN, bold=True), T('"Rain\'s the best! :3" (Regeneration)', SKY_LINE)])])
    # ---- today's forecast (their menu)
    fn('p211/today', ['dialog clear @s', 'execute if predicate bm:p29/raining run return run ' + tellraw('@s', [T('Nimbus: ', SUN, bold=True), T('"Rain! My favourite. Regeneration for you, and my zaps hit twice as hard. :3"', SKY_LINE)]),
                         f'execute {day} run return run ' + tellraw('@s', [T('Sunny: ', SUN, bold=True), T('"Clear and sunny - Haste for you, and my sunbeams burn their brightest under the open sky."', SKY_LINE)]),
                         tellraw('@s', [T('Snooze: ', SUN, bold=True), T('"...night... Night Vision and Speed for you... and my lullabies last longer... and blind them... zzz."', SKY_LINE)]),
                         'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2'])
    fn('admin/sky_seen', ['tag @s add bm.ybs1', 'tag @s add bm.ybs2', 'tag @s add bm.ybs3', say('(Every sky seen - they\'ll come down to you under the open sky.)', SUN)])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.ybvis]')
    weather_and_bed(G)


# ---------------------------------------------------------------------------------------------------- 2.94f: fully honoured
# With their Honour at its height (Queen Ava's Honours, rank III: Vitality, Bulwark and Might all V), the Sky Buddies are the
# weather's own: from their menu they turn the sky clear, to rain or to a thunderstorm (every 2 minutes), and Nimbus makes
# you a bed wherever you are in the Overworld - a real one: sleep in it and the night passes, and you wake where you slept
# (your spawn stays there, the bed gone). It goes when you're done with it, and leaves nothing behind.
WX = 2950                                           # (the weather page's buttons: 2950 clear, 2951 rain, 2952 storm, 2953 back)
BED = 'minecraft:light_gray_bed'


def weather_and_bed(G):
    import phase28 as P28
    fn, title, tellraw = G.fn, G.title, G.tellraw
    second = G.FUNCS['loop/second']
    line = lambda who, txt: title('@s', 'actionbar', [T(f'{who}: ', SUN, bold=True), T(txt, SKY_LINE)])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.ybwx dummy', 'scoreboard objectives add bm.ybbt dummy']
    G.OBJECTIVES += ['bm.ybwx', 'bm.ybbt']
    mine = '@e[type=minecraft:wolf,tag=bm.ybpet,tag=!bm.ffpet,distance=..24]'
    fn('p211/full', ['execute unless score @s bm.hn_sky matches 0.. run return 0', 'scoreboard players operation #hs bm.rng = @s bm.hn_sky',
                     'scoreboard players operation #hs bm.rng %= #1000 bm.rng', 'execute if score #hs bm.rng matches 555 run return 1', 'return 0'])
    fn('p211/near', ['scoreboard players operation #me bm.pid = @s bm.pid', f'execute as {mine} if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    not_full = line('Sunny', '"Not yet, pal - when Queen Ava\'s honoured us all the way (rank III), the sky\'s yours."')
    not_near = line('Sunny', '"Call us over first - we can\'t work the weather from home."')
    # ---- the weather
    page = P28.multi([T('THE SKY, YOURS', SUN, bold=True)],
                     [P28.body([T('"Say the word, pal." ', SKY_LINE), T('(every 2 minutes)', 'gray')], 300)],
                     [P28.btn(T('Clear skies', '#ffd04a', bold=True), WX, width=150, tooltip=T('Sunny chases the clouds off.', 'gray')),
                      P28.btn(T('Rain', '#7ab8ff', bold=True), WX + 1, width=150, tooltip=T('Nimbus lets it pour. :3', 'gray')),
                      P28.btn(T('Thunderstorm', '#b8a0ff', bold=True), WX + 2, width=150, tooltip=T('All three, dark and loud.', 'gray')),
                      P28.btn(T('\u00ab Back', 'gray'), WX + 3, width=150)], columns=2, exit_label='Close')
    fn('p211/wx/open', ['execute unless function bm:p211/full run return run function bm:p211/wx/nope',
                        'execute unless function bm:p211/near run return run function bm:p211/wx/far',
                        f'scoreboard players set @s bm.menu {C.MENU}', f'dialog show @s {snbt(page)}'])
    fn('p211/wx/nope', ['dialog clear @s', not_full, 'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.6 0.8'])
    fn('p211/wx/far', ['dialog clear @s', not_near])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {WX + k} run return run function bm:p211/wx/act' for k in range(4)]
    fn('p211/wx/act', [f'execute unless score @s bm.menu matches {C.MENU} run return run function bm:p28/stale',
                       f'execute if score #act bm.pay matches {WX + 3} run return run function bm:p211/menu',
                       'dialog clear @s',
                       'execute unless function bm:p211/full run return run ' + not_full,
                       'execute unless function bm:p211/near run return run ' + not_near,
                       'execute if score @s bm.ybwx matches 1.. run return run ' + line('Snooze', '"...the sky needs a moment... (every 2 minutes)..."'),
                       f'execute if score #act bm.pay matches {WX} run function bm:p211/wx/clear',
                       f'execute if score #act bm.pay matches {WX + 1} run function bm:p211/wx/rain',
                       f'execute if score #act bm.pay matches {WX + 2} run function bm:p211/wx/storm',
                       'scoreboard players set @s bm.ybwx 120'])
    burst = lambda c: [f'execute as {mine} if score @s bm.pid = #me bm.pid at @s run particle {dust(c, 1.6)} ~ ~2 ~ 0.8 0.6 0.8 0 30']
    fn('p211/wx/clear', ['weather clear'] + burst(GOLDD) + ['playsound minecraft:block.beacon.activate neutral @a[distance=..24] ~ ~ ~ 0.8 1.6',
                         line('Sunny', '"Clouds - beat it. ...There. Sun\'s out."')])
    fn('p211/wx/rain', ['weather rain'] + burst(RAIND) + ['playsound minecraft:weather.rain neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                        line('Nimbus', '"Rain! Rain! :3"')])
    fn('p211/wx/storm', ['weather thunder'] + burst((0.6, 0.5, 1.0)) + ['playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..24] ~ ~ ~ 0.6 1.2',
                         line('Sunny', '"Storm\'s coming. Twinkle\'s idea. Don\'t look at me."')])
    second.append('scoreboard players remove @a[scores={bm.ybwx=1..}] bm.ybwx 1')
    # ---- the bed: on the first open ground beside you, its foot by you; a marker keeps it
    fn('p211/bed/try', ['dialog clear @s',
                        'execute unless function bm:p211/full run return run ' + not_full,
                        'execute unless function bm:p211/near run return run ' + not_near,
                        'execute unless dimension minecraft:overworld run return run ' + line('Nimbus', '"Not here... beds go boom here. Back in the Overworld! :3"'),
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:marker,tag=bm.ybbed] if score @s bm.pid = #me bm.pid at @s run function bm:p211/bed/gone',
                        'scoreboard players set #bed bm.rng 0'] +
       [f'execute if score #bed bm.rng matches 0 align xyz positioned ~0.5 ~ ~0.5 if block ~{dx} ~ ~{dz} minecraft:air if block ~{2 * dx} ~ ~{2 * dz} minecraft:air '
        f'unless block ~{dx} ~-1 ~{dz} #bm:grap_pass unless block ~{2 * dx} ~-1 ~{2 * dz} #bm:grap_pass positioned ~{dx} ~ ~{dz} run function bm:p211/bed/put_{f}'
        for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north'))] +
       ['execute if score #bed bm.rng matches 0 run return run ' + line('Nimbus', '"No room for a bed here... find me some open, flat ground! :3"')])
    for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north')):
        fn(f'p211/bed/put_{f}', ['scoreboard players set #bed bm.rng 1',
                                 f'setblock ~ ~ ~ {BED}[facing={f},part=foot]', f'setblock ~{dx} ~ ~{dz} {BED}[facing={f},part=head]',
                                 f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.ybbed","bm.ybbed_{f}","bm.ybbnew"]}}',
                                 'scoreboard players operation @e[type=minecraft:marker,tag=bm.ybbnew,distance=..1] bm.pid = #me bm.pid',
                                 'scoreboard players set @e[type=minecraft:marker,tag=bm.ybbnew,distance=..1] bm.ybbt 0',
                                 'data modify entity @e[type=minecraft:marker,tag=bm.ybbnew,distance=..1,limit=1] data.sp set from entity @s respawn',   # (your own spawn, kept)
                                 'tag @e[type=minecraft:marker,tag=bm.ybbnew,distance=..1] remove bm.ybbnew',
                                 f'particle minecraft:cloud ~{dx / 2} ~0.6 ~{dz / 2} 0.8 0.2 0.8 0.02 30', f'particle {dust(MOOND, 1.2)} ~{dx / 2} ~1 ~{dz / 2} 0.8 0.3 0.8 0 16',
                                 'playsound minecraft:block.wool.place block @a[distance=..16] ~ ~ ~ 1 0.8',
                                 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
        fn(f'p211/bed/clear_{f}', [f'execute if block ~ ~ ~ {BED} run setblock ~ ~ ~ minecraft:air', f'execute if block ~{dx} ~ ~{dz} {BED} run setblock ~{dx} ~ ~{dz} minecraft:air'])
    G.FUNCS['p211/bed/try'].append(line('Nimbus', '"Hop on! A cloud bed, just for you. :3" (right-click it to sleep)'))
    # (each second: a sleeper on it wakes where they slept; when no one's on it, half a minute on - or you've gone - it goes)
    second.append('execute as @e[type=minecraft:marker,tag=bm.ybbed] at @s run function bm:p211/bed/sec')
    fn('p211/bed/sec', ['scoreboard players add @s bm.ybbt 1',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'scoreboard players set #slp bm.rng 0',
                        'execute as @a[distance=..3] if data entity @s sleeping_pos run scoreboard players set #slp bm.rng 1',
                        'execute as @a[distance=..3] if score @s bm.pid = #me bm.pid if data entity @s sleeping_pos run spawnpoint @s ~ ~ ~',      # (its owner only)
                        'execute as @a[distance=..3] if score @s bm.pid = #me bm.pid if data entity @s sleeping_pos run tag @e[type=minecraft:marker,tag=bm.ybbed,distance=..0.5] add bm.ybslept',
                        'execute if score #slp bm.rng matches 1 run return run scoreboard players set @s bm.ybbt 0',
                        f'execute unless block ~ ~ ~ {BED} run return run function bm:p211/bed/gone',
                        'execute if score @s bm.ybbt matches 30.. run return run function bm:p211/bed/gone',
                        'scoreboard players set #near bm.rng 0',
                        'execute as @a[distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #near bm.rng 1',
                        'execute if score #near bm.rng matches 0 run function bm:p211/bed/gone'])
    fn('p211/bed/gone', [f'execute if entity @s[tag=bm.ybbed_{f}] run function bm:p211/bed/clear_{f}' for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north'))] +
       [f'kill @e[type=minecraft:item,distance=..4,nbt={{Item:{{id:"{BED}"}}}},nbt=!{{PickupDelay:0s}}]', 'scoreboard players operation #me bm.pid = @s bm.pid',
        'execute unless entity @s[tag=bm.ybslept] if data entity @s data.sp.pos run function bm:p211/bed/unspawn',
        'particle minecraft:cloud ~ ~0.6 ~ 0.6 0.2 0.6 0.02 20', 'kill @s'])
    # (2.94k) a bed takes your spawn the moment you right-click it - by day, or with monsters near, before it says no. Gone
    # without your having slept in it, and your spawn still on it: your own spawn back, as it was.
    fn('p211/bed/unspawn', ['data modify storage bm:p211 sp set value {}', 'data modify storage bm:p211 sp.x set from entity @s data.sp.pos[0]',
                            'data modify storage bm:p211 sp.y set from entity @s data.sp.pos[1]', 'data modify storage bm:p211 sp.z set from entity @s data.sp.pos[2]',
                            'data modify storage bm:p211 sp.d set from entity @s data.sp.dimension', 'data modify storage bm:p211 sp.yaw set from entity @s data.sp.yaw',
                            'data modify storage bm:p211 sp.pitch set from entity @s data.sp.pitch',
                            'execute store result score #bx bm.rng run data get entity @s Pos[0]', 'execute store result score #by bm.rng run data get entity @s Pos[1]',
                            'execute store result score #bz bm.rng run data get entity @s Pos[2]',
                            'execute as @a if score @s bm.pid = #me bm.pid run function bm:p211/bed/unspawn_me'])
    fn('p211/bed/unspawn_me', ['execute unless data entity @s respawn.pos run return 0',
                               'execute store result score #rx bm.rng run data get entity @s respawn.pos[0]', 'execute store result score #ry bm.rng run data get entity @s respawn.pos[1]',
                               'execute store result score #rz bm.rng run data get entity @s respawn.pos[2]',
                               'scoreboard players operation #rx bm.rng -= #bx bm.rng', 'scoreboard players operation #ry bm.rng -= #by bm.rng', 'scoreboard players operation #rz bm.rng -= #bz bm.rng',
                               'execute unless score #rx bm.rng matches -1..1 run return 0', 'execute unless score #ry bm.rng matches -1..1 run return 0',
                               'execute unless score #rz bm.rng matches -1..1 run return 0',
                               'function bm:p211/bed/unspawn_tp with storage bm:p211 sp'])
    fn('p211/bed/unspawn_tp', ['$execute in $(d) run spawnpoint @s $(x) $(y) $(z) $(yaw) $(pitch)'])
    # (a broken Nimbus bed drops nothing to keep: the fresh drop - still on its pickup delay - is gone the tick it lands; your own beds lying near are left be)
    G.FUNCS['tick'].append(f'execute as @e[type=minecraft:marker,tag=bm.ybbed] at @s run kill @e[type=minecraft:item,distance=..4,nbt={{Item:{{id:"{BED}"}}}},nbt=!{{PickupDelay:0s}}]')
    G.FUNCS['admin/uninstall'].insert(0, 'execute as @e[type=minecraft:marker,tag=bm.ybbed] at @s run function bm:p211/bed/gone')

