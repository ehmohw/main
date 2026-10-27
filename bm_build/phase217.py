"""2.94m: EMMA'S EASTER EGGS.

- A HUG FOR CECIL: when Emma and Cecil are both out with you, idle and close, with no monster near, Emma may - rarely - throw
  her arms round him (one in 600 a second while they're idle together, and never again for half an hour after). Both stand
  still for a moment: he turns to you, she steps in at his left, turned to him - one arm round behind his back, the other
  across his chest, her head tipped onto his hood (a side hug, as in the art). Cecil, as in the art: put out at first ("Personal
  space!"), then he gives in - his eyes glance aside and he blushes (a pink squiggle on each cheek: phase95_art's 'blush');
  hearts. His free arm tucks back out of her way. (State 20 on her rig.)
- HER KILLERWATT LOOK: call KillerWatt while Emma is with you (or Emma while he is) and he tries to take her - his current arcs
  into her, the way he takes any living thing. She throws him out (2.95b: no "zappy" giggle - he's a parasite, and that was a
  possession that failed), but he leaves a mark: she comes out of it recoloured in his green and yellow (her own dress and hair, phase89's emkw_* parts), with four lightning tendrils
  off her back, her eyes aglow. A look only. It's hers for good from then on - on or off in her wardrobe ("KillerWatt look").
- "FRIK YOU!": hit too often too fast (her hits pile up 10 each and drain 2 a second; at 40 - five quick blows) she rounds on them - an angry face,
  "Frik you!" in a spiky white bubble over her head, in chat too. Then not again for 30 seconds.
- PANIC: at a third of her health or less she may panic (one in four a second, then not for 20 seconds) - wide eyes swimming
  with tears, a wobbling wail, a line in chat.
Her lines go to her owner, unless they've hushed follower chatter. For a test, #hug1 bm.cfg 1 makes the hug certain."""
from items import T
from nbt import snbt, B, Int, F
import phase95 as P95

PINK = '#ff7ad0'
GREEN = '#7ae63a'
HUG_ODDS = 600                # (1 in this, a second, while they're idle together)
HUG_REST = 1800               # (seconds before another)
HUG_TICKS = 90
CEC_PUT_OUT = 30              # (ticks of Cecil put out before he gives in)
FRIK_AT, FRIK_REST, PANIC_REST = 40, 30, 20


def generate(G):
    fn, tellraw = G.fn, G.tellraw
    P = G.PREFIX
    objs = ['bm.emhg', 'bm.emhc', 'bm.emhn', 'bm.emfk', 'bm.empn', 'bm.emfb']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    own = lambda parts: f'execute on owner run ' + tellraw('@s[tag=!bm.hush]', parts)          # (to her owner, unless hushed)
    emline = lambda *parts: own([T('Emma: ', PINK, bold=True)] + list(parts))
    FOE = 'type=#bm:hostile,tag=!bm.npc'
    sec = []

    # ================================================================== the hug
    sec.append('execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p217/hug/sec')
    fn('p217/hug/sec', ['execute if score @s bm.emhc matches 1.. run return run scoreboard players remove @s bm.emhc 1',
                        'execute if score @s bm.emhg matches 1.. run return 0',
                        'execute unless score @s bm.ems matches 0 run return 0', 'execute if score @s bm.eme matches 1.. run return 0',
                        'execute if data entity @s {NoAI:1b} run return 0', 'execute if data entity @s {Sitting:1b} run return 0',
                        f'execute if entity @e[{FOE},distance=..12] run return 0',
                        f'execute store result score #r bm.rng run random value 1..{HUG_ODDS}',
                        'execute if score #hug1 bm.cfg matches 1 run scoreboard players set #r bm.rng 1',
                        'execute unless score #r bm.rng matches 1 run return 0',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..5,sort=nearest] if score @s bm.pid = #me bm.pid unless data entity @s {Sitting:1b} '
                        'unless data entity @s {NoAI:1b} run tag @s add bm.emhugc',
                        'execute unless entity @e[type=minecraft:wolf,tag=bm.emhugc] run return 0',
                        'function bm:p217/hug/start', 'tag @e[type=minecraft:wolf,tag=bm.emhugc] remove bm.emhugc'])
    # (both held still a moment: he turns to you; she steps in at his left, turned in to him)
    C = '@e[type=minecraft:wolf,tag=bm.emhugc,limit=1]'
    fn('p217/hug/start', [f'scoreboard players set @s bm.emhg {HUG_TICKS}', f'scoreboard players set @s bm.emhc {HUG_REST}',
                          'tag @s add bm.emhugging', f'tag {C} add bm.emhugging', 'execute on owner run tag @s add bm.emhugown',
                          f'data modify entity @s NoAI set value 1b', f'data modify entity {C} NoAI set value 1b',
                          f'execute as {C} at @s facing entity @a[tag=bm.emhugown,limit=1] feet run tp @s ~ ~ ~ ~ 0',     # (he turns to you...)
                          f'execute at {C} rotated as {C} rotated ~ 0 positioned ^0.491 ^ ^0.379 run tp @s ~ ~ ~ ~80 0',      # (...she at his left, turned in)
                          ] + [f'execute as {C} run {l}' for l in P95.face_cmd('cecil', 'deadpan', CEC_PUT_OUT)] + P95.face_cmd('emma', 'happy', HUG_TICKS) +
       ['tag @a remove bm.emhugown', 'particle minecraft:heart ~ ~1.6 ~ 0.4 0.3 0.4 0 6', 'playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1.3',
        emline(T('(she throws her arms around Cecil) ', '#ffd0ec', italic=True), T('"Cecil!! C\'mere, you! You\'re the BEST."', '#ffd0ec')),
        own([T('Cecil: ', '#b48cff', bold=True), T('"Hey- HEY. Personal space, Emma. I\'m holding a staff here."', '#d8c8ff')])])
    # (Cecil, as in the art: put out at first - then he gives in, and he blushes)
    fn('p217/hug/soften', [f'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,tag=bm.emhugging,distance=..3] run {l}' for l in P95.face_cmd('cecil', 'blush', HUG_TICKS - CEC_PUT_OUT)] +
       ['particle minecraft:heart ~ ~1.5 ~ 0.4 0.2 0.4 0 3',
        own([T('Cecil: ', '#b48cff', bold=True), T('"...Mrph. Fine. Just this once." ', '#d8c8ff'),
             T('(He doesn\'t pull away. His eyes glow a little warmer - is he blushing?)', '#d8c8ff', italic=True)])])
    from phase57_art import qa, qmul
    q = qa('x', 36.1)                                     # (his free arm tucked back, out of her way)
    hold = f'left_rotation:[{q[0]:.4f}f,{q[1]:.4f}f,{q[2]:.4f}f,{q[3]:.4f}f],translation:[0f,0f,0f]'
    fn('p217/hug/cecil', [
                          'execute as @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_larm,tag=!bm.cphug] run data merge entity @s '
                          f'{{start_interpolation:0,interpolation_duration:8,transformation:{{{hold}}}}}',
                          'tag @e[type=minecraft:item_display,tag=bm.cpsel,tag=bm.cp_larm] add bm.cphug'])
    # (as Cecil each tick, in place of his own animation while she hugs him: held still, his free arm tucked back out of her way)
    G.FUNCS['p46/pet/anim'].insert(0, 'execute if entity @s[tag=bm.emhugging] run return run function bm:p217/hug/cecil')
    # (each tick of it, as her host, from her tick: hold the pose where she stands; hearts now and then)
    fn('p217/hug/tick', ['scoreboard players remove @s bm.emhg 1',
                         'execute rotated as @s rotated ~ 0 run function bm:p57/place',
                         f'execute if score @s bm.emhg matches {HUG_TICKS - CEC_PUT_OUT} run function bm:p217/hug/soften',
                         'execute if score @s bm.emhg matches 20 run particle minecraft:heart ~ ~1.7 ~ 0.3 0.2 0.3 0 3',
                         'execute if score @s bm.emhg matches 45 run particle minecraft:heart ~ ~1.7 ~ 0.3 0.2 0.3 0 3',
                         'execute if score @s bm.emhg matches ..0 run function bm:p217/hug/end'])
    fn('p217/hug/end', ['scoreboard players set @s bm.emhg 0', 'data modify entity @s NoAI set value 0b', 'tag @s remove bm.emhugging',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,tag=bm.emhugging] if score @s bm.pid = #me bm.pid run function bm:p217/hug/free'])
    fn('p217/hug/free', ['data modify entity @s NoAI set value 0b', 'tag @s remove bm.emhugging', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:item_display,tag=bm.cphug] if score @s bm.pid = #me bm.pid run tag @s remove bm.cphug'])
    # (a hug cut short - unloaded, or Emma gone - never leaves either of them frozen)
    sec += ['execute as @e[type=minecraft:wolf,tag=bm.cecilpet,tag=bm.emhugging] at @s unless entity @e[type=minecraft:cat,tag=bm.emhugging,distance=..4] run function bm:p217/hug/free',
            'execute as @e[type=minecraft:cat,tag=bm.emmapet,tag=bm.emhugging] unless score @s bm.emhg matches 1.. run function bm:p217/hug/end']
    L = G.FUNCS['p57/state']
    L.insert(0, 'execute if score @s bm.emhg matches 1.. run return run scoreboard players set #st bm.rng 20')
    L = G.FUNCS['p57/tick']
    j = L.index('function bm:p57/anim')
    L.insert(j + 1, 'execute if score @s bm.ems matches 20 run function bm:p217/hug/tick')

    # ================================================================== her KillerWatt look
    sec.append('execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p217/kw/sec')
    fn('p217/kw/sec', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #kw bm.rng 0',
                       'execute as @e[type=minecraft:wolf,tag=bm.kxpet,distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #kw bm.rng 1',
                       'execute if score #kw bm.rng matches 0 run return 0',
                       'execute on owner unless entity @s[tag=bm.emkw_u] run function bm:p217/kw/unlock'])
    fn('p217/kw/unlock', ['tag @s add bm.emkw_u', 'tag @s add bm.emkw_o', 'function bm:p78/emma_now',
                          'scoreboard players operation #me bm.pid = @s bm.pid',
                          'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid at @s run function bm:p217/kw/jolt',
                          tellraw('@s', P + [T('KillerWatt lunges - his current arcs into Emma, reaching for her the way he takes any living thing. ', '#ffe040'), T('She throws him out - but comes out of it glassy green, eyes aglow.', GREEN)]),
                          tellraw('@s', [T('Emma: ', PINK, bold=True), T('"Get - OUT! ...Ugh. He left something behind. I can still feel it buzzing under my skin."', '#ffd0ec')]),
                          tellraw('@s', P + [T('KillerWatt look', GREEN, bold=True), T(' is in Emma\'s wardrobe for good. ', 'gray'),
                                             T('(Sneak + use her ribbon: Wardrobe - on or off.)', 'dark_gray')])])
    fn('p217/kw/jolt', ['particle minecraft:electric_spark ~ ~1 ~ 0.5 0.9 0.5 0.4 60', 'particle minecraft:flash{color:[0.6,1.0,0.4,1.0]} ~ ~1 ~ 0 0 0 0 1',
                        'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..24] ~ ~ ~ 0.5 1.8'] +
       P95.face_cmd('emma', 'angry', 40))
    # (her wardrobe's row - phase99, code TOP-2)
    fn('p217/kw/t', ['execute unless entity @s[tag=bm.emkw_u] run return run function bm:p217/kw/locked',
                     'execute if entity @s[tag=bm.emkw_o] run return run function bm:p217/kw/off',
                     'tag @s add bm.emkw_o', 'function bm:p78/emma_now', 'playsound minecraft:entity.lightning_bolt.impact player @s ~ ~ ~ 0.3 2',
                     'function bm:p99/menu/emma'])
    fn('p217/kw/off', ['tag @s remove bm.emkw_o', 'function bm:p78/emma_now', 'function bm:p99/menu/emma'])
    fn('p217/kw/locked', [tellraw('@s', P + [T('KillerWatt look', GREEN, bold=True), T(' is a secret. ', 'gray'),
                                             T('(Some sparks are catching... maybe if Emma met someone electric?)', 'dark_gray')]),
                          'function bm:p99/menu/emma'])
    # (worn: last of all in her outfit, over any dress or outfit - the parts' models swapped for his look's)
    G.FUNCS['p57/outfit'] += ['scoreboard players set #emkw bm.rng 0',
                              'execute as @a[tag=bm.emkw_o] if score @s bm.pid = #cp bm.rng run scoreboard players set #emkw bm.rng 1'] + \
        [f'execute if score #emkw bm.rng matches 1 as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{p}] run data modify entity @s item.components."minecraft:item_model" set value "bm:emkw_{p}"'
         for p in ('body', 'head', 'armr', 'arml', 'legr', 'legl')]

    # ================================================================== "Frik you!"
    L = G.FUNCS['p95/emma/ouch']
    L.append('function bm:p217/frik/hit')
    fn('p217/frik/hit', ['scoreboard players add @s bm.emhn 10', 'execute if score @s bm.emfk matches 1.. run return 0',
                         f'execute if score @s bm.emhn matches {FRIK_AT}.. run function bm:p217/frik/go'])
    bubble = snbt({'Tags': ['bm.emfrik', 'bm.emfriknew'], 'text': T('Frik you!', '#e02020', bold=True), 'billboard': 'center',
                   'background': Int(-1), 'shadow': B(0), 'line_width': Int(120), 'brightness': {'block': Int(15), 'sky': Int(15)},
                   'transformation': {'translation': [F(0), F(1.75), F(0)], 'left_rotation': [F(0), F(0), F(0.0436), F(0.999)],
                                      'scale': [F(1.1), F(1.1), F(1.1)], 'right_rotation': [F(0), F(0), F(0), F(1)]}})
    fn('p217/frik/go', ['scoreboard players set @s bm.emhn 0', f'scoreboard players set @s bm.emfk {FRIK_REST}'] +
       P95.face_cmd('emma', 'angry', 50) +
       ['kill @e[type=minecraft:text_display,tag=bm.emfrik,distance=..4]',
        f'summon minecraft:text_display ~ ~ ~ {bubble}',
        'ride @e[type=minecraft:text_display,tag=bm.emfriknew,limit=1,sort=nearest] mount @s',
        'scoreboard players set @e[type=minecraft:text_display,tag=bm.emfriknew] bm.emfb 0',
        'tag @e[type=minecraft:text_display,tag=bm.emfriknew] remove bm.emfriknew',
        'particle minecraft:angry_villager ~ ~1.9 ~ 0.3 0.2 0.3 0 4',
        'playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 1 1.5',
        emline(T('"Frik you!"', '#ff6060', bold=True))])
    sec += ['execute as @e[type=minecraft:cat,tag=bm.emmapet,scores={bm.emhn=1..}] run scoreboard players remove @s bm.emhn 2',
            'execute as @e[type=minecraft:cat,tag=bm.emmapet,scores={bm.emfk=1..}] run scoreboard players remove @s bm.emfk 1',
            'execute as @e[type=minecraft:text_display,tag=bm.emfrik] run scoreboard players add @s bm.emfb 1',
            'execute as @e[type=minecraft:text_display,tag=bm.emfrik,scores={bm.emfb=3..}] run kill @s',
            'execute as @e[type=minecraft:text_display,tag=bm.emfrik] at @s unless entity @e[type=minecraft:cat,tag=bm.emmapet,distance=..3] run kill @s']

    # ================================================================== panic at low health
    sec.append('execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p217/panic/sec')
    fn('p217/panic/sec', ['execute if score @s bm.empn matches 1.. run return run scoreboard players remove @s bm.empn 1',
                          'execute if score @s bm.eme matches 1.. run return 0',
                          'execute store result score #h bm.rng run data get entity @s Health 10',
                          'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 3.334',
                          'execute if score #h bm.rng > #mx bm.rng run return 0',
                          'execute store result score #r bm.rng run random value 1..4',
                          'execute unless score #r bm.rng matches 1 run return 0',
                          'function bm:p217/panic/go'])
    lines = ['"Nonono- I can\'t faint now! HELP!"', '"I-I\'m not okay! I\'m NOT okay!"', '"Somebody DO something!"']
    fn('p217/panic/go', [f'scoreboard players set @s bm.empn {PANIC_REST}'] + P95.face_cmd('emma', 'panic', 60) +
       ['particle minecraft:falling_water ~ ~1.6 ~ 0.25 0.1 0.25 0 8', 'particle minecraft:splash ~ ~1.7 ~ 0.2 0.1 0.2 0 6',
        'playsound minecraft:entity.cat.stray_ambient neutral @a[distance=..16] ~ ~ ~ 1 1.8',
        'execute store result score #r bm.rng run random value 1..3'] +
       [f'execute if score #r bm.rng matches {i + 1} run ' + emline(T('(panicking) ', '#ffd0ec', italic=True), T(l, '#ffd0ec')) for i, l in enumerate(lines)])

    G.FUNCS['loop/second'] += sec
