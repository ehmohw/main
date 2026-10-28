"""2.95: KETTLE - the first Buddy. (kettle_art.py, after the owner's art; the machinery is rigpet's.)
The very first thing the Gem of Creativity ever made: a tall stick figure, flat as a drawing, who is simply the embodiment of
childlike simplicity and fun. He isn't a narrator and he doesn't know he's in a game (that's Mr. Capshun) - he just wants to play.
He fights the way a child plays: tag, paper planes, kickball, cartwheels, a jump rope - and RECESS!

FINDING HIM: out in the open on a sunny day, in a meadow, a plain, a flower field or a cherry grove - now and then a stick figure
  comes skipping along, bouncing a ball. Right-click him holding a sheet of PAPER: he folds it into a paper plane for you. That's
  his. (With Mr. Capshun at your side he turns up three times as often: Capshun can't stop talking about him.)
KETTLE'S PAPER PLANE  use: call him (again: call him over); sneak + use: his menu - sit / send home, his ways, the wardrobe.
LET'S PLAY!    out of a fight, every 45 s beside you: he tags you ("you're it!") - Speed and Jump Boost for 30 s.
TAG            a foe within 3, every second: a poke (7) - "you're it!": it's slowed and weakened for 6 s, and lit up.
PAPER PLANES   every 4 s, a foe 4-16 away: three paper planes (4 each).
KICKBALL       every 7 s, a foe 3-12 away: his ball, kicked (9) - it bounces on to the next foe near it (5).
CARTWHEEL      every 10 s, a foe 3-8 away: he cartwheels into it (10) and sends it flying.
JUMP ROPE      three or more foes within 5, every 15 s: he skips - and trips them up as the rope comes round (3 a turn, slowed).
RECESS!        (charged, every minute) a great leap: every foe within 8 tossed into the air (12); you, and your followers,
               Speed II and Jump Boost for 10 s.
SKETCH & PLAY  (Kettle + Mr. Capshun - the duo, phase188) Speed, Jump Boost and Luck for you - and every 20 s, with a foe within
               12, Capshun sketches a toy over it and Kettle plays with it: a BALL bounced on its head (12, slowed), a KITE that lifts
               it off its feet (6, up it goes, lit up), a SLIDE it tumbles down and away (8, knocked back, slowed).
Right-click him: sit / stand (cross-legged, or flat on his back watching the clouds). A frame keeps him (he steps out of it
and plays round it), a display case shows him, Cecil sells his doll, the Tailor his inks and his aura (Playground Chalk)."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import kettle_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase210 as FXS
import phase212 as P212

KT_C, KT_LINE = '#8ad8ff', '#e0f4ff'
W = 'kettle'
TOYS = ('plane', 'ball', 'rope')
SK = ('sk_ball', 'sk_kite', 'sk_slide')
RAINBOW = [(1.0, 0.2, 0.2), (1.0, 0.6, 0.15), (1.0, 0.9, 0.2), (0.3, 0.85, 0.35), (0.25, 0.5, 1.0), (0.7, 0.3, 1.0)]


def dust(c, s=1.4):
    return f'minecraft:dust{{color:[{c[0]},{c[1]},{c[2]}],scale:{s}}}'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Kettle', KT_C, KT_LINE, 'p227', 'kt', 'kq'
    A = A
    MENU = 2920
    PET_HP, PET_CD = 40, 120
    ITEM = 'kettle_plane'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': 'happy', 'surprised': 'surprised', 'hurt': 'surprised', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'grin', 'serious': 'determined'}
    ATTRS = dict(armor=4, attack_damage=6, movement_speed=0.4, follow_range=32, step_height=1.1)
    SCALE = 0.9
    HIT = (0.7, 1.9)
    SWAP = ('tool',)
    CYCLE = {0: (200, [(0, 'idle_a'), (80, 'idle_c'), (112, 'idle_a'), (150, 'idle_d'), (176, 'idle_a')]),
             1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (240, [(0, 'sit_a'), (120, 'sit_b')]),
             6: (None, [(0, 'happy'), (10, 'wave_a'), (16, 'wave_b'), (22, 'wave_a')]),
             7: (None, [(0, 'tag_up'), (4, 'tag')]),
             8: (None, [(0, 'throw_up'), (6, 'throw')]),
             9: (None, [(0, 'kick_up'), (6, 'kick')]),
             11: (None, [(2 * i, f'cart_{i % 4}') for i in range(8)] + [(16, 'happy')]),
             12: (None, [(0, 'recess_a'), (14, 'recess_b'), (26, 'happy')]),
             13: (None, [(5 * i, ('rope_a', 'rope_b')[i % 2]) for i in range(8)]),
             14: (None, [(0, 'idle_b'), (6, 'tag_up'), (10, 'tag'), (16, 'happy')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 20, 'idle_b': 5, 'idle_c': 16, 'idle_d': 14, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3,
           'jump': 4, 'sit_a': 20, 'sit_b': 30, 'tag_up': 3, 'tag': 2, 'throw_up': 4, 'throw': 2, 'kick_up': 4, 'kick': 2,
           'cart_0': 2, 'cart_1': 2, 'cart_2': 2, 'cart_3': 2, 'recess_a': 10, 'recess_b': 4, 'rope_a': 3, 'rope_b': 3, 'happy': 6, 'wave_a': 5, 'wave_b': 5}
    CYCLE[16] = (None, [(0, 'ride')])                   # (2.96c: riding Bender - phase234 seats him)
    DUR['ride'] = 6
    QUIPS = ['"Tag! You\'re it!"', '"Again! Again!"', '"Ha! Missed me!"', '"Ready or not, here I come!"', '"Last one there\'s a rotten egg!"',
             '"Look! A cloud shaped like a duck!"', '"Is it recess yet? It\'s ALWAYS recess."', '"Wanna see me do a cartwheel? Watch! WATCH!"',
             '"I bet I can jump higher than you!"', '"My plane flew SO far. Did you see? Did you see?"', '"Everybody plays! That\'s the rule."',
             '"Capshun says I was the first. First at what? First at EVERYTHING!"']
    HELLO = ('"Wait for me! Wait for meee!"', '(Kettle comes skipping up, bouncing his ball off his head.) "Hi! What are we playing?"',
             '"Bye! Same time tomorrow? Same time tomorrow!"')
    SIT = ('"Okay, I\'m rested! That was a long time. It was five seconds."', '(Kettle flops down on the grass.) "Look at the clouds..."')
    FAINT = 'Time out... I need a time out...'
    NOT_YOURS = '"You\'re not my friend - I mean, you could BE my friend, but I\'m already somebody\'s."'
    POWERS = [("Let's Play!", 'out of a fight, every 45 s beside you: he tags you - Speed and Jump Boost for 30 s'),
              ('Tag', 'a foe within 3, every second: a poke (7) - "you\'re it!": slowed, weakened and lit up for 6 s'),
              ('Paper Planes', 'every 4 s, a foe 4-16 away: three paper planes (4 each)'),
              ('Kickball', 'every 7 s, a foe 3-12 away: his ball, kicked (9) - and it bounces on to the next (5)'),
              ('Cartwheel', 'every 10 s, a foe 3-8 away: he cartwheels into it (10) and knocks it flying'),
              ('Jump Rope', 'three or more foes within 5, every 15 s: he skips - and trips them up (3 a turn, slowed)'),
              ('Recess!', 'charged, every minute: every foe within 8 tossed into the air (12); you and your followers, Speed II and Jump Boost'),
              ('Sketch & Play', 'with Mr. Capshun: Speed, Jump Boost and Luck - and every 20 s Capshun sketches a toy and Kettle plays with it')]
    INTRO = [T('Kettle', KT_C, bold=True), T(' - the very first Buddy the Gem of Creativity ever made. ', 'gray'),
             T('Simple as a stick figure, and he\'d like to keep it that way: all he wants is to play.', 'white')]
    BUTTONS = ()
    BURST = [f'particle {dust(c, 1.3)} ~ ~1.2 ~ 0.4 0.7 0.4 0 5' for c in RAINBOW[::2]] + ['particle minecraft:poof ~ ~0.6 ~ 0.4 0.4 0.4 0.03 10']
    FADE_SOUND = 'playsound minecraft:entity.chicken.egg neutral @a[distance=..20] ~ ~ ~ 1 1.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.player.levelup neutral @a[distance=..24] ~ ~ ~ 0.4 1.8']
    ENC_POSES = [(0, 'idle_b'), (20, 'idle_a'), (40, 'wave_a'), (50, 'wave_b'), (60, 'idle_a')]
    ENC_PARTICLE = f'execute if score #f bm.rng matches 20 run particle {dust(RAINBOW[4], 1.0)} ~ ~1.6 ~ 0.3 0.4 0.3 0 4'
    ADV = ('Tag, You\'re It', 'Meet Kettle - and give him something to fold')
    ADMIN_HINT = 'He skips by on sunny days in meadows, plains, flower fields and cherry groves (more often with Mr. Capshun beside you).'
    MEET_HINT = 'Right-click him holding a sheet of paper.'


RP.register(C)
item('kettle_plane', TOTEM, "Kettle's Paper Plane", KT_C,
     ['A paper plane, folded with great care and a lot of tongue-sticking-out.', 'It says "KETTLE" on one wing in big wobbly letters.',
      ('Use: call Kettle (again: call him over).', 'blue'), ('Sneak + use: his menu.', 'blue'),
      ('He plays: tag, paper planes, kickball, cartwheels -', 'blue'), ('and RECESS!', 'blue'), ('If he faints: 2 minutes before he can return.', 'gray'),
      ('"Everybody plays! That\'s the rule."', 'dark_gray')],
     model='bm:kettle_plane', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_kettle', TOTEM, 'Kettle Doll', KT_C, ['A doll of Kettle - all arms and legs, and a grin.', ('Right-click a block: set it down.', 'blue'),
                                                 ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_kettle', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_kettle'] = 'bm:p141/doll_kettle/use'
P141.DOLLS.append(('doll_kettle', 'Kettle', KT_C, 'A doll of Kettle - all arms and legs, and a grin.', 'minecraft:happy_villager',
                   'minecraft:entity.chicken.egg', 'minecraft:poof'))
P141.DOLL_FROM['doll_kettle'] = ('kettle_plane', {'kh': 1.6, 'kb': 0.72, 'kl': 0.56, 'groups': {'bm:kt_shinr': 'legs', 'bm:kt_shinl': 'legs'}})
P134.FIT['kettle_plane'] = (0.0, 1.85, -0.3, 0.3, -0.55, 0.55)
POSES = A.POSES

# ---- his bonds (phase188 runs the pairs): with Mr. Capshun - SKETCH & PLAY (the toys are below); with Fishy and the Sky Buddies
import phase188 as P188
_O, _FOE = P188.O, 'type=#bm:hostile,tag=!bm.npc'
P188.VNAME['kettle'] = 'Kettle'
P188.PAIRS.update({
    'sketchplay': ('kettle', 'capshun', 'Sketch & Play', '#8ad8ff', 'Kettle and Mr. Capshun - one draws the toys, the other plays with them',
                   [f'effect give {_O} minecraft:speed 3 0 true', f'effect give {_O} minecraft:jump_boost 3 0 true', f'effect give {_O} minecraft:luck 15 0 true'],
                   [('capshun', '"Kettle! THE Kettle! The very first Buddy! I\'ve read your backstory - it\'s two lines long and it\'s perfect."'),
                    ('kettle', '"Hi! Can you draw me a ball? A big one?"')],
                   [('kettle', '"Draw a kite! No - a slide! No - BOTH!"', 'capshun', '"One at a time. I only have the one pencil. ...Fine, both."'),
                    ('capshun', '[Mr. Capshun narrates: "And the artist drew, and the child played, and for a moment everything was simple."]', 'kettle', '"What\'s a narrator?"'),
                    ('kettle', '"Tag! You\'re it!"', 'capshun', '"I am NOT - oh. Oh, I am. Right. Running."')]),
    'recess': ('kettle', 'fishy', 'Fish Out of Water', '#ffa040', 'Kettle and Fishy - a bowl, some legs, and a game of catch',
               [f'effect give {_O} minecraft:dolphins_grace 3 0 true', f'effect give {_O} minecraft:jump_boost 3 0 true'],
               [('kettle', '"Fishy! Wanna play catch? You can be the ball! ...No? Okay."'), ('fishy', '(a very firm blub)')],
               [('fishy', '(he blows a bubble. Kettle chases it.)', 'kettle', '"I\'ll get it! I\'ll get - it popped."'),
                ('kettle', '"Fishy, you were made by the gem too, right? We\'re like brothers!"', 'fishy', '(he adjusts his monocle, touched)')]),
    'cloudwatch': ('kettle', 'sky', 'Cloud Watching', '#ffd04a', 'Kettle and the Sky Buddies - he picks shapes out of the clouds, and they make them',
                   [f'effect give {_O} minecraft:slow_falling 3 0 true', f'effect give {_O} minecraft:regeneration 3 0 true'],
                   [('kettle', '"Look! That cloud looks like a duck!"'), ('sky', 'Nimbus: "...it IS a duck now. :3"')],
                   [('sky', 'Sunny: "Kettle! Tag - you\'re it!"', 'kettle', '"No fair, you can FLY!"'),
                    ('kettle', '"Twinkle, how many stars are there?"', 'sky', 'Twinkle: "One more every time you count!"')]),
})
P188.ICON.update({'sketchplay': 'bm:kettle_plane', 'recess': 'bm:kettle_plane', 'cloudwatch': 'bm:kettle_plane'})


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image
    import os
    im = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref', 'pixellab', 'kettle', 'plane.png')).convert('RGBA')
    bb = im.getbbox(); im = im.crop(bb)
    s = max(im.size); sq = Image.new('RGBA', (s, s), (0, 0, 0, 0)); sq.paste(im, ((s - im.width) // 2, (s - im.height) // 2))
    return sq.resize((32, 32), Image.LANCZOS)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    for k in TOYS + SK:                                  # (his toys flying, Capshun's sketches made real: flat pictures)
        face = {'uv': [0, 0, 16, 16], 'texture': '#f'}
        R.HATS[f'kt_pj_{k}'] = ({'f': f'bm:block/kt_pj_{k}'}, [{'from': [0, 0, 8], 'to': [16, 16, 8], 'shade': False,
                                                               'faces': {'north': face, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


def textures():
    import os
    from PIL import Image
    T_ = A.textures()
    D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ref', 'pixellab', 'kettle')
    for k in TOYS + SK:
        T_[f'kt_pj_{k}'] = Image.open(os.path.join(D, f'{k}.png')).convert('RGBA')
    return T_


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    csay = lambda txt: title('@s', 'actionbar', [T('Kettle: ', KT_C, bold=True), T(txt, KT_LINE)])
    pet = 'bm.ktpet'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.ktit dummy', 'scoreboard objectives add bm.ktsp dummy', 'scoreboard objectives add bm.ktty dummy']
    G.OBJECTIVES += ['bm.ktit', 'bm.ktsp', 'bm.ktty']

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute if score @s {S("k2")} matches 1.. run scoreboard players remove @s {S("k2")} 1',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..8] run function bm:{pfx}/recess_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..5]',
                 f'execute {idle} unless score @s {S("k2")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/rope_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/tag_go',
                 f'execute {idle} unless score @s {S("sc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..8] run function bm:{pfx}/cart_go',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..12] run function bm:{pfx}/kick_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..4] if entity @e[{foe},distance=..16] run function bm:{pfx}/throw_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..10] if function bm:{pfx}/near_owner run function bm:{pfx}/play_go']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..8] run return 1', 'return 0'])
        fn(f'{pfx}/tag_go', go(7, 8, 'mc', 20, ['playsound minecraft:entity.player.attack.weak neutral @a[distance=..16] ~ ~ ~ 0.6 1.6']))
        fn(f'{pfx}/throw_go', go(8, 12, 'rc', 80, face('serious', 12)))
        fn(f'{pfx}/kick_go', go(9, 12, 'bc', 140, face('serious', 12)))
        fn(f'{pfx}/cart_go', go(11, 18, 'sc', 200, face('squint', 18) + ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.4 1.8']))
        fn(f'{pfx}/rope_go', go(13, 40, 'k2', 300, face('happy', 40) + ['playsound minecraft:entity.fishing_bobber.throw neutral @a[distance=..16] ~ ~ ~ 1 1.4']))
        fn(f'{pfx}/recess_go', go(12, 32, 'gc', 1200, face('squint', 30) + ['execute on owner if entity @s[distance=..24] run ' + X.csay('"RECESS!!!"'),
                                                                             'playsound minecraft:block.bell.use neutral @a[distance=..32] ~ ~ ~ 1.4 1.6']))
        fn(f'{pfx}/play_go', go(14, 20, 'k', 900, face('happy', 20)))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/tag',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/throw',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 6 run function bm:{pfx}/kick',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 3..17 run function bm:{pfx}/wheel',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 2 run function bm:{pfx}/cart',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 1..40 if score @s {S("x")} matches 1..40 run function bm:{pfx}/skip',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/recess',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 10 run function bm:{pfx}/play'])
        # TAG: a poke - and the foe is "it" (slow, weak, lit up)
        fn(f'{pfx}/tag', hit(7) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/tagged'] + end)
        fn(f'{pfx}/tagged', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 6 0', 'effect give @s minecraft:weakness 6 0', 'effect give @s minecraft:glowing 6 0',
                             'particle minecraft:crit ~ ~1.2 ~ 0.3 0.4 0.3 0.2 12', f'particle {dust(RAINBOW[4], 1.2)} ~ ~2.2 ~ 0.2 0.1 0.2 0 6',
                             'playsound minecraft:entity.experience_orb.pickup neutral @a[distance=..16] ~ ~ ~ 0.6 1.8'])
        # PAPER PLANES: three, fanned out
        pjs = f'@e[type=minecraft:wolf,tag={pet}]'
        plane = P212.projectile(G, 'kt_plane', 'bm:kt_pj_plane', 4, pjs, scale=0.8, fxname='capshun_scribble',
                                trail=['particle minecraft:white_ash ~ ~ ~ 0.05 0.05 0.05 0 1'],
                                on_hit=['playsound minecraft:item.book.page_turn neutral @a[distance=..16] ~ ~ ~ 0.8 1.6'])
        fn(f'{pfx}/pl', plane)
        aim = f'facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes positioned ^-0.4 ^1.8 ^0.6'
        fn(f'{pfx}/throw', [f'execute {aim} rotated ~{d} ~-4 run function bm:{pfx}/pl' for d in (-10, 0, 10)] +
           ['playsound minecraft:entity.snowball.throw neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
        # KICKBALL: the ball - and where it lands, it bounces on to the next foe
        ball = P212.projectile(G, 'kt_ball', 'bm:kt_pj_ball', 9, pjs, scale=0.7, fxname='capshun_scribble',
                               trail=['particle minecraft:crit ~ ~ ~ 0.05 0.05 0.05 0 1'],
                               on_hit=['playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 1 1.6', 'tag @s add bm.ktbx',
                                       f'execute as @e[{foe},distance=..1.8,sort=nearest,limit=1] run tag @s add bm.ktbx',
                                       'scoreboard players set #pd bm.rng 5', 'execute store result storage bm:tmp p212.d int 1 run scoreboard players get #pd bm.rng',
                                       f'execute as @e[{foe},tag=!bm.ktbx,distance=..7,sort=nearest,limit=1] at @s run function bm:{pfx}/bounced',
                                       'tag @e[tag=bm.ktbx] remove bm.ktbx'])
        fn(f'{pfx}/kb', ball)
        fn(f'{pfx}/bounced', ['function bm:p212/dmg with storage bm:tmp p212', 'particle minecraft:crit ~ ~1.5 ~ 0.3 0.3 0.3 0.2 10',
                              'playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 1 1.9'])
        fn(f'{pfx}/kick', [f'execute facing entity @e[{foe},distance=..12,sort=nearest,limit=1] eyes positioned ^0.3 ^0.6 ^0.6 run function bm:{pfx}/kb',
                           'playsound minecraft:entity.player.attack.knockback neutral @a[distance=..16] ~ ~ ~ 0.8 1.4'])
        # CARTWHEEL: across the ground to it, a quarter-turn a step - then the landing
        fn(f'{pfx}/wheel', [f'execute if entity @e[{foe},distance=1.6..9] facing entity @e[{foe},distance=..9,sort=nearest,limit=1] feet rotated ~ 0 '
                            f'positioned ^ ^ ^0.45 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                            f'particle {dust(RAINBOW[2], 0.9)} ~ ~0.2 ~ 0.2 0.05 0.2 0 2'])
        fn(f'{pfx}/cart', hit(10) + [f'execute as @e[{foe},distance=..2.8,sort=nearest,limit=1] at @s run function bm:{pfx}/carted'] + end)
        fn(f'{pfx}/carted', [f'function bm:{pfx}/hurt', f'execute facing entity @e[type=minecraft:wolf,tag={X.me},limit=1] feet rotated ~ 0 run tp @s ^ ^0.3 ^-2.2',
                             'particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.player.attack.strong neutral @a[distance=..16] ~ ~ ~ 0.8 1.2'])
        # JUMP ROPE: every fifth tick the rope comes round - and trips up whoever's in reach
        fn(f'{pfx}/skip', [f'scoreboard players operation #q bm.rng = @s {S("x")}', 'scoreboard players operation #q bm.rng %= #5 bm.rng',
                           f'execute if score #q bm.rng matches 0 run function bm:{pfx}/rope_round'])
        fn(f'{pfx}/rope_round', hit(3) + [f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/tripped',
                                          f'particle {dust((0.85, 0.15, 0.2), 1.0)} ~ ~0.15 ~ 2 0 2 0 12',
                                          'playsound minecraft:entity.fishing_bobber.retrieve neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'] + end)
        fn(f'{pfx}/tripped', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 2'])
        # RECESS!: everything nearby up in the air; you and your followers off and running
        fn(f'{pfx}/recess', hit(12) + [f'execute as @e[{foe},distance=..8] at @s run function bm:{pfx}/recessed',
                                       FXS.fx('cg_conjure', 2.6, 1.0) if 'cg_conjure' in FXS.names() else 'particle minecraft:firework ~ ~1 ~ 1 1 1 0.1 40',
                                       'particle minecraft:firework ~ ~1 ~ 1.5 0.6 1.5 0.15 50',
                                       'playsound minecraft:entity.player.levelup neutral @a[distance=..32] ~ ~ ~ 0.8 1.6',
                                       'scoreboard players operation #me bm.pid = @s bm.pid',
                                       'execute as @a[distance=..24] if score @s bm.pid = #me bm.pid run function bm:p227/recess_you'] + end)
        fn(f'{pfx}/recessed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 3', 'particle minecraft:cloud ~ ~0.3 ~ 0.3 0.1 0.3 0.05 8'])
        fn('p227/recess_you', ['effect give @s minecraft:speed 10 1 true', 'effect give @s minecraft:jump_boost 10 1 true'])
        # LET'S PLAY!: he tags you - you're it (Speed, Jump Boost)
        fn(f'{pfx}/play', ['execute on owner if entity @s[distance=..8] run function bm:p227/play_you'])
        fn('p227/play_you', ['effect give @s minecraft:speed 30 0 true', 'effect give @s minecraft:jump_boost 30 0 true',
                             f'particle {dust(RAINBOW[4], 1.2)} ~ ~1 ~ 0.3 0.6 0.3 0 12', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 1.4',
                             'execute unless entity @s[tag=bm.hush] run ' + csay('"Tag! You\'re it! ...Now chase me!"')])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #5 bm.rng 5']
        return lines

    def encounter(G, X):
        # out in the open on a sunny day, in a meadow-ish biome: now and then a stick figure comes skipping by
        BIOMES = ('meadow', 'plains', 'sunflower_plains', 'flower_forest', 'cherry_grove')
        X.second.append('execute as @a[tag=!bm.ktmet,gamemode=!spectator] at @s if dimension minecraft:overworld run function bm:p227/enc/check')
        fn('p227/enc/check', ['execute unless predicate bm:p227/sunny run return 0'] +
           [f'execute if biome ~ ~ ~ minecraft:{b} run return run function bm:p227/enc/roll' for b in BIOMES])
        G.wjson('bm/predicate/p227/sunny.json', {'condition': 'minecraft:all_of', 'terms': [
            {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 0, 'max': 12000}, 'period': 24000},
            {'condition': 'minecraft:weather_check', 'raining': False}]})
        fn('p227/enc/roll', ['execute store result score #r bm.rng run random value 1..300',
                             'scoreboard players set #lim bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                             'execute as @e[type=minecraft:wolf,tag=bm.mzpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #lim bm.rng 3',
                             'execute if score #r bm.rng > #lim bm.rng run return 0',
                             'execute unless block ~ ~-1 ~ #minecraft:dirt run return 0',
                             'execute if entity @e[type=minecraft:interaction,tag=bm.ktenc,distance=..64] run return 0',
                             'execute positioned ^ ^ ^6 run function bm:p227/enc/place'])
        fn('p227/enc/place', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p227/enc/step',
                              'execute positioned ~ ~1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run function bm:p227/enc/step'])
        fn('p227/enc/step', ['function bm:p227/enc/spawn', 'particle minecraft:happy_villager ~ ~1 ~ 0.6 0.8 0.6 0 12',
                             'playsound minecraft:entity.slime.jump neutral @a[distance=..24] ~ ~ ~ 1 1.6',
                             X.tellraw('@a[tag=!bm.ktmet,distance=..16]', [T('A stick figure comes skipping across the grass, bouncing a red ball off his head. ', KT_LINE, italic=True),
                                                                            T('He stops, looks at you, and waves both arms. ', 'gray', italic=True),
                                                                            T('"Hi! I\'m Kettle! Do you have any paper? I can make the BEST planes."', '#ffffff', italic=True)]),
                             'execute as @a[tag=!bm.ktmet,distance=..16] at @s run function bm:p227/enc/capshun_sees'])
        fn('p227/enc/capshun_sees', ['scoreboard players operation #me bm.pid = @s bm.pid',
                                     'execute as @e[type=minecraft:wolf,tag=bm.mzpet,distance=..24] if score @s bm.pid = #me bm.pid run tag @s add bm.ktsaw',
                                     'execute if entity @e[tag=bm.ktsaw] run ' + X.tellraw('@s', [T('Mr. Capshun: ', '#f0f0f0', bold=True),
                                                                                                    T('"Is that - that\'s KETTLE! The first Buddy! The original! I\'m having a moment."', '#d8e4ff')]),
                                     'tag @e[tag=bm.ktsaw] remove bm.ktsaw'])
        fn('p227/enc/talk', [f'execute if items entity @s container.* {X.holds("kettle_plane")} run return run ' + csay('"You\'ve got my plane already! Throw it! Wait - don\'t, I\'m in it. Sort of."'),
                             'execute if items entity @s weapon.mainhand minecraft:paper run return run function bm:p227/enc/recruit',
                             csay('"Do you have any paper? Just one sheet! I\'ll fold you something amazing."'),
                             'playsound minecraft:entity.chicken.egg player @s ~ ~ ~ 1 1.8'])
        fn('p227/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:happy_villager ~ ~1.4 ~ 0.5 0.6 0.5 0 16',
                                f'execute as {X.here} at @s run playsound minecraft:item.book.page_turn neutral @a[distance=..16] ~ ~ ~ 1 1.6',
                                X.tellraw('@s', [T('He folds the paper - this way, that way, tongue sticking out - and hands you a perfect paper plane. ', KT_LINE, italic=True),
                                                 T('"There! Now you can call me whenever you want to play. Which is always. I always want to play."', 'gray', italic=True)]),
                                'function bm:p227/enc/joined'])

    RP.build(C, G, abilities, encounter)

    # ---- SKETCH & PLAY (with Mr. Capshun): every 20 s in a fight, Capshun sketches a toy over a foe - and Kettle plays with it
    X2 = RP.X
    G.FUNCS['loop/second'] += ['scoreboard players remove @e[type=minecraft:wolf,tag=bm.ktpet,scores={bm.ktty=1..}] bm.ktty 1',
                               'execute as @e[type=minecraft:wolf,tag=bm.ktpet,tag=!bm.ffpet] unless score @s bm.ktty matches 1.. at @s run function bm:p227/sp/check']
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
    fn('p227/sp/check', [f'execute unless entity @e[{foe},distance=..12] run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'scoreboard players set #cp bm.rng 0',
                         'execute as @e[type=minecraft:wolf,tag=bm.mzpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #cp bm.rng 1',
                         'execute if score #cp bm.rng matches 0 run return 0', 'scoreboard players set @s bm.ktty 20',
                         'execute store result score #toy bm.rng run random value 1..3',
                         f'execute as @e[{foe},distance=..12,sort=nearest,limit=1] at @s run function bm:p227/sp/sketch',
                         'execute on owner if entity @s[distance=..24,tag=!bm.hush] run function bm:p227/sp/say'])
    toy = lambda k: snbt({'Tags': ['bm.kttoy', 'bm.kttoynew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:kt_pj_{k}'}},
                          'item_display': 'fixed', 'billboard': 'center', 'view_range': F(1.5), 'brightness': {'block': Int(15), 'sky': Int(15)},
                          'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(1.6)] * 3}})
    fn('p227/sp/sketch', [f'execute if score #toy bm.rng matches {i + 1} run summon minecraft:item_display ~ ~3.2 ~ {toy(k)}' for i, k in enumerate(SK)] +
       ['scoreboard players set @e[type=minecraft:item_display,tag=bm.kttoynew,distance=..5] bm.pjt 30',
        'tag @e[type=minecraft:item_display,tag=bm.kttoynew] remove bm.kttoynew', FXS.fx('capshun_scribble', 2.0, 3.2),
        'playsound minecraft:ui.cartography_table.take_result neutral @a[distance=..16] ~ ~ ~ 1 1.2', 'tag @s add bm.ktplay', 'scoreboard players set @s bm.ktsp 20'])
    G.FUNCS['tick'] += ['execute as @e[type=minecraft:item_display,tag=bm.kttoy] at @s run function bm:p227/sp/toy_tick',
                        'execute as @e[tag=bm.ktplay] at @s run function bm:p227/sp/play_tick']
    fn('p227/sp/toy_tick', ['scoreboard players remove @s bm.pjt 1', 'execute if score @s bm.pjt matches ..0 run function bm:p227/sp/toy_gone'])
    fn('p227/sp/toy_gone', ['particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.02 6', 'kill @s'])
    # (as the foe: a second's sketching - then Kettle plays: the toy comes down on it)
    fn('p227/sp/play_tick', ['scoreboard players remove @s bm.ktsp 1', 'execute if score @s bm.ktsp matches 1.. run return 0', 'tag @s remove bm.ktplay',
                             'execute store result score #toy bm.rng run random value 1..3',
                             'execute if entity @e[type=minecraft:item_display,tag=bm.kttoy,distance=..5,nbt={item:{components:{"minecraft:item_model":"bm:kt_pj_sk_ball"}}}] run scoreboard players set #toy bm.rng 1',
                             'execute if entity @e[type=minecraft:item_display,tag=bm.kttoy,distance=..5,nbt={item:{components:{"minecraft:item_model":"bm:kt_pj_sk_kite"}}}] run scoreboard players set #toy bm.rng 2',
                             'execute if entity @e[type=minecraft:item_display,tag=bm.kttoy,distance=..5,nbt={item:{components:{"minecraft:item_model":"bm:kt_pj_sk_slide"}}}] run scoreboard players set #toy bm.rng 3',
                             'execute as @e[type=minecraft:wolf,tag=bm.ktpet,distance=..20,sort=nearest,limit=1] run tag @s add bm.ktme',
                             'execute if score #toy bm.rng matches 1 run function bm:p227/sp/ball',
                             'execute if score #toy bm.rng matches 2 run function bm:p227/sp/kite',
                             'execute if score #toy bm.rng matches 3 run function bm:p227/sp/slide',
                             'tag @e[tag=bm.ktme] remove bm.ktme',
                             'execute as @e[type=minecraft:item_display,tag=bm.kttoy,distance=..5] run scoreboard players set @s bm.pjt 6'])
    by = '@e[type=minecraft:wolf,tag=bm.ktme,limit=1]'
    fn('p227/sp/ball', [f'damage @s 12 minecraft:mob_attack by {by}', 'effect give @s minecraft:slowness 3 1',
                        'execute as @e[type=minecraft:item_display,tag=bm.kttoy,distance=..5] at @s run tp @s ~ ~-2.2 ~',
                        'particle minecraft:crit ~ ~1.8 ~ 0.4 0.3 0.4 0.3 16', 'playsound minecraft:entity.slime.jump neutral @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p227/sp/kite', [f'damage @s 6 minecraft:mob_attack by {by}', 'effect give @s minecraft:levitation 2 2', 'effect give @s minecraft:glowing 4 0',
                        'particle minecraft:cloud ~ ~0.5 ~ 0.3 0.2 0.3 0.05 10', 'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..16] ~ ~ ~ 0.6 1.4'])
    fn('p227/sp/slide', [f'damage @s 8 minecraft:mob_attack by {by}', 'effect give @s minecraft:slowness 3 2',
                         f'execute facing entity {by} feet rotated ~ 0 run tp @s ^ ^0.2 ^-3',
                         'particle minecraft:white_ash ~ ~0.5 ~ 0.6 0.2 0.6 0 20', 'playsound minecraft:block.copper.step neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn('p227/sp/say', ['execute store result score #r bm.rng run random value 1..3',
                       'execute if score #r bm.rng matches 1 run ' + title('@s', 'actionbar', [T('Mr. Capshun: ', '#f0f0f0', bold=True), T('"One ball, coming up."', '#d8e4ff'),
                                                                                                T('  Kettle: ', KT_C, bold=True), T('"Mine! MINE!"', KT_LINE)]),
                       'execute if score #r bm.rng matches 2 run ' + title('@s', 'actionbar', [T('Mr. Capshun: ', '#f0f0f0', bold=True), T('"A kite! Hold the string, Kettle."', '#d8e4ff'),
                                                                                                T('  Kettle: ', KT_C, bold=True), T('"Up, up, UP!"', KT_LINE)]),
                       'execute if score #r bm.rng matches 3 run ' + title('@s', 'actionbar', [T('Mr. Capshun: ', '#f0f0f0', bold=True), T('"And a slide. Wheee, et cetera."', '#d8e4ff'),
                                                                                                T('  Kettle: ', KT_C, bold=True), T('"WHEEE!"', KT_LINE)])])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.kttoy]')
