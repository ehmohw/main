"""2.96c: TOGETHER - Bender and the friends who ride him, curl up with him, and fight from his back.

RIDING BENDER: Mr. Capshun, Kettle and the rat mercenary, out with Bender, hop up onto his back when things are calm (now and
  then - and they hop off again for a walk) and ride along: astride him, legs either side, seated by him every tick - on his
  back as it rises and falls through every pose of his (his bob: together_fit.py, from the rigs themselves), turned as he
  turns. One at a time. They hop off when he does one of his charged moves (Good Boy!, Rage!), when he sits, digs, sniffs or
  swims - and when you sit them (right-click). A rider is a real passenger (ride ... mount): no AI of its own while it rides
  (bm.rdr), its own abilities paused; Bender carries it.
THE NIGHT CUDDLE: Bender, Henry and Nia out together at night, all calm, nothing hostile near and you close by - a chance, every
  second they stay that way: Bender flops down asleep, and the cats curl up one either side of his chest, facing the way he faces
  (spots fitted against his sleeping pose with together_fit.clips: no part of one inside another). They breathe; they purr. If
  you go to bed beside them, they settle at once. They wake at morning, at a monster, when you walk off (16 blocks), or when you
  sit one of them (right-click). (bm.cdl; bm.cdlw counts the calm seconds - a few minutes' rest after.)
DOG PILE (Henry's charged move, with Bender beside him - phase229 calls it): Henry springs onto Bender's back (duo/hop) and
  rides him into the fight (duo/ride), swiping at whatever Bender charges into (6, harder by night); then leaps off onto a monster
  for the finish (duo/leap), Bender biting it at the same moment. While they do it Bender holds his own charged moves (bm.bvduo
  gates Good Boy! and Rage!). Henry: bm.hqdp the phase (1 hop, 2 ride, 3 leap and land), bm.hqdt its ticks."""
from items import T
import together_fit as TF
import phase195 as P195
import phase198 as P198
import phase227 as P227
import phase228 as P228
import phase229 as P229
import phase95 as FX
import capshun_art
import kettle_art
import rufus_art
import henry_art

FOE = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
BV = '@e[type=minecraft:wolf,tag=bm.dme,limit=1]'                    # (Bender, while his partner's tick runs)
# who rides: (their Cfg, art, pose, seat on: body (a rider astride) / feet (Henry's paws), how far forward along his back)
RIDERS = {'capshun': (P198.C, capshun_art, 'ride', 'body', 0.22), 'kettle': (P227.C, kettle_art, 'ride', 'body', 0.22),
          'rufus': (P228.C, rufus_art, 'ride', 'body', 0.22), 'henry': (P229.Henry, henry_art, 'perch', 'feet', -0.18)}
HOP_ON = {'capshun': ('[Mr. Capshun narrates: "And so our hero mounted his noble steed. The steed licked him."]', '(Bender wags so hard the narration wobbles)'),
          'kettle': ('"Giddy-up, Bender! GIDDY-UP!"', '(Bender giddies up)'),
          'rufus': ('"Easy, big fella. Just to the next town. My feet are killing me."', '(Bender trots very carefully, so as not to spill him)')}
# the cuddle: where each cat curls up beside him (left, up, forward of his middle; their turn against his)
CUDDLE = {'henry': (0.44, 0.0, 0.2, 0), 'nia': (-0.47, 0.0, 0.15, 0)}           # (2.96c: both facing his way - the owner's ask)


def generate(G):
    fn, title, tellraw, wjson = G.fn, G.title, G.tellraw, G.wjson
    objs = ['bm.bvbob', 'bm.rdc', 'bm.cdlw', 'bm.hqdp', 'bm.hqdt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    tick, second = [], []
    bv_body = '@e[type=minecraft:item_display,tag=bm.bvsel,tag=bm.bvp_body,limit=1]'
    line = lambda C, txt: title('@s', 'actionbar', [T(f'{C.NAME}: ' if C.NAME != 'Henry' else 'Henry ', C.COL, bold=True), T(txt, C.LINE)])
    bsay = lambda txt: title('@s', 'actionbar', [T('Bender ', P195.BV_C, bold=True), T(txt, P195.BV_LINE)])

    # ================================================================== RIDING: Bender seats whoever's on his back, every tick
    t = G.FUNCS['p195/tick']
    t.insert(len(t) - 1, 'execute if entity @s[tag=bm.bvseat] run function bm:p234/seats')
    assert t[-1] == 'tag @e[tag=bm.bvsel] remove bm.bvsel', t[-1]
    fn('p234/seats', ['execute unless function bm:p234/has_rider run return run tag @s remove bm.bvseat',
                      'execute if data entity @s {Sitting:1b} run return run function bm:p234/unseat',
                      'execute if score @s bm.dqs matches 4 run return run function bm:p234/unseat',
                      'execute if score @s bm.dqs matches 9..10 run return run function bm:p234/unseat',
                      'execute if score @s bm.dqs matches 12..13 run return run function bm:p234/unseat',
                      'execute if score @s bm.dqs matches 15.. run return run function bm:p234/unseat',
                      'scoreboard players operation #bob bm.rng = @s bm.bvbob',
                      f'execute rotated as {bv_body} rotated ~ 0 on passengers if entity @s[type=minecraft:wolf,tag=bm.rdr] run function bm:p234/seat'])
    fn('p234/has_rider', ['execute on passengers if entity @s[type=minecraft:wolf,tag=bm.rdr] run return 1', 'return 0'])
    fn('p234/seat', [f'execute if entity @s[tag=bm.{C.ab}pet] run return run function bm:p234/seat/{w}' for w, (C, *_r) in RIDERS.items()])
    for w, (C, A, pose, on, z) in RIDERS.items():
        y = TF.seat(A, pose, on)
        fn(f'p234/seat/{w}', ['scoreboard players operation #me bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag=bm.{C.ab}p_pet,tag=!bm.{C.ab}fade] if score @s bm.pid = #me bm.pid run tag @s add bm.{C.ab}sel'] +
           [f'execute if score #bob bm.rng matches {k} positioned ^ ^{y + dy:.3f} ^{z + dz:.3f} run function bm:{C.pfx}/place' for k, (dy, dz) in enumerate(TF.bobs())] +
           [f'tag @e[tag=bm.{C.ab}sel] remove bm.{C.ab}sel'])
    fn('p234/unseat', ['execute on passengers if entity @s[type=minecraft:wolf,tag=bm.rdr] run function bm:p234/off', 'tag @s remove bm.bvseat'])
    fn('p234/off', ['ride @s dismount', 'tag @s remove bm.rdr', 'data merge entity @s {NoAI:0b,NoGravity:0b}', 'scoreboard players set @s bm.rdc 6',
                    'execute at @s run particle minecraft:poof ~ ~0.4 ~ 0.2 0.1 0.2 0.01 4'])
    # (a rider no longer on him - called over, swept off - has its wits back at once; one you sit gets down and sits)
    tick += ['execute as @e[type=minecraft:wolf,tag=bm.rdr] unless function bm:p20/frog/has_vehicle at @s run function bm:p234/off',
             'execute as @e[type=minecraft:wolf,tag=bm.rdr] if data entity @s {Sitting:1b} at @s run function bm:p234/off']
    # he never takes one of them away with him: sent home, fainted, his charged moves - off they hop first
    G.FUNCS['p195/dismiss'].insert(0, 'execute as @e[type=minecraft:wolf,tag=bm.bvsel2] at @s run function bm:p234/unseat')
    G.FUNCS['p195/go'].insert(0, 'function bm:p234/unseat')
    for f in ('p195/rg/go', 'p195/good_go'):
        G.FUNCS[f].insert(0, 'function bm:p234/unseat')
    # up they hop: calm, beside him, now and then
    for w in ('capshun', 'kettle', 'rufus'):
        C = RIDERS[w][0]
        second.append(f'execute as @e[type=minecraft:wolf,tag=bm.{C.ab}pet,tag=!bm.rdr,tag=!bm.cdl,tag=!bm.ffpet] at @s run function bm:p234/try/{w}')
        fn(f'p234/try/{w}', ['execute if score @s bm.rdc matches 1.. run return run scoreboard players remove @s bm.rdc 1',
                             'execute if data entity @s {Sitting:1b} run return 0', f'execute if score @s bm.{C.q}x matches 1.. run return 0',
                             f'execute if entity @e[{FOE},distance=..10] run return 0',
                             'execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                             'scoreboard players operation #me bm.pid = @s bm.pid',
                             'execute as @e[type=minecraft:wolf,tag=bm.bvpet,tag=!bm.bvseat,tag=!bm.cdl,tag=!bm.bvduo,distance=..8] if score @s bm.pid = #me bm.pid if function bm:p234/calm run tag @s add bm.rdto',
                             f'execute if entity @e[type=minecraft:wolf,tag=bm.rdto,distance=..8] run function bm:p234/on/{w}',
                             'tag @e[tag=bm.rdto] remove bm.rdto'])
        hop, reply = HOP_ON[w]
        fn(f'p234/on/{w}', ['tag @s add bm.rdr', 'data merge entity @s[type=minecraft:wolf] {NoAI:1b,Sitting:0b,Motion:[0d,0d,0d]}',
                            'ride @s mount @e[type=minecraft:wolf,tag=bm.rdto,limit=1]', 'tag @e[type=minecraft:wolf,tag=bm.rdto] add bm.bvseat',
                            'particle minecraft:poof ~ ~0.5 ~ 0.3 0.2 0.3 0.02 6', 'playsound minecraft:entity.horse.saddle neutral @a[distance=..16] ~ ~ ~ 0.4 1.6',
                            'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.6 1.3',
                            'execute store result score #r bm.rng run random value 1..3',
                            f'execute if score #r bm.rng matches 1 on owner if entity @s[distance=..20,tag=!bm.hush] run function bm:p234/hop_say/{w}'])
        fn(f'p234/hop_say/{w}', [tellraw('@s', [T(f'{C.NAME}: ', C.COL, bold=True), T(hop, C.LINE)]),
                                 tellraw('@s', [T('Bender ', P195.BV_C, bold=True), T(reply, P195.BV_LINE)])])
        # (and now and then, when he stops, off again for a walk)
        second.append(f'execute as @e[type=minecraft:wolf,tag=bm.{C.ab}pet,tag=bm.rdr] at @s run function bm:p234/stroll')
    # (only when he's stopped - never off the back of a dog on the move)
    fn('p234/stroll', ['execute on vehicle unless score @s bm.dqs matches 0 run return 0',
                       'execute store result score #r bm.rng run random value 1..150', 'execute unless score #r bm.rng matches 1 run return 0',
                       'function bm:p234/off', 'scoreboard players set @s bm.rdc 30'])
    # calm (as Bender): nothing on, not sitting, not raging - standing, walking, running, happy
    fn('p234/calm', ['execute if score @s bm.dqx matches 1.. run return 0', 'execute if data entity @s {Sitting:1b} run return 0',
                     'execute if score @s bm.bvrp matches 1.. run return 0', 'execute if score @s bm.dqs matches 4..5 run return 0',
                     'execute if score @s bm.dqs matches 7.. run return 0', 'return 1'])
    # (their wits, whatever cut a ride short)
    for w in ('capshun', 'kettle', 'rufus'):
        ab = RIDERS[w][0].ab
        second.append(f'execute as @e[type=minecraft:wolf,tag=bm.{ab}pet,tag=!bm.rdr,tag=!bm.ffpet,nbt={{NoAI:1b}}] run data merge entity @s {{NoAI:0b,NoGravity:0b}}')

    # ================================================================== DOG PILE: Henry's charged move, with Bender
    tick_ = G.FUNCS['p195/tick']
    for i, l in enumerate(tick_):
        if ('function bm:p195/rg/go' in l or 'function bm:p195/good_go' in l) and l.startswith('execute '):
            tick_[i] = 'execute unless entity @s[tag=bm.bvduo] ' + l[len('execute '):]
    assert sum('tag=bm.bvduo' in l for l in tick_) == 2
    H = P229.Henry
    me_bv = ['scoreboard players operation #me bm.pid = @s bm.pid',
             'execute as @e[type=minecraft:wolf,tag=bm.bvduo,distance=..24] if score @s bm.pid = #me bm.pid run tag @s add bm.dme']
    fn('p234/duo/ok', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @e[type=minecraft:wolf,tag=bm.bvpet,tag=!bm.bvseat,tag=!bm.cdl,tag=!bm.bvduo,distance=..6] if score @s bm.pid = #me bm.pid '
                       'unless score @s bm.bvrp matches 1.. unless data entity @s {Sitting:1b} unless score @s bm.dqs matches 9..15 run return 1', 'return 0'])
    fn('p234/duo/go', ['scoreboard players set @s bm.hqa 18', 'scoreboard players set @s bm.hqx 400', 'scoreboard players set @s bm.hqgc 1200',
                       'scoreboard players set @s bm.hqdp 1', 'scoreboard players set @s bm.hqdt 0', 'data merge entity @s {NoAI:1b,NoGravity:1b,Motion:[0d,0d,0d]}',
                       'scoreboard players operation #me bm.pid = @s bm.pid',
                       'execute as @e[type=minecraft:wolf,tag=bm.bvpet,tag=!bm.bvduo,distance=..6,sort=nearest] if score @s bm.pid = #me bm.pid run tag @s add bm.bvduo',
                       'playsound minecraft:entity.cat.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.3', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.2'] +
       FX.face_cmd('henry', 'serious', 120) +
       ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + line(H, "(looks at Bender's back. Bender's ears go up. They both know what happens next.)")])
    fn('p234/duo/tick', ['scoreboard players add @s bm.hqdt 1', 'data modify entity @s Motion set value [0d,0d,0d]'] + me_bv +
       ['execute unless entity @e[type=minecraft:wolf,tag=bm.dme] run return run function bm:p234/duo/done',
        'execute if score @s bm.hqdp matches 1 run function bm:p234/duo/hop',
        'execute if score @s bm.hqdp matches 2 run function bm:p234/duo/ride',
        'execute if score @s bm.hqdp matches 3 run function bm:p234/duo/leap',
        'tag @e[tag=bm.dme] remove bm.dme'])
    pose = lambda p: f'function bm:p229/pose/{p}'
    # up: a crouch, a spring - onto his back
    fn('p234/duo/hop', [f'execute if score @s bm.hqdt matches 1 run {pose("pounce_up")}', f'execute if score @s bm.hqdt matches 4 run {pose("perch_hop")}',
                        'execute if score @s bm.hqdt matches 4..6 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~0.3 ~',
                        f'execute if score @s bm.hqdt matches 4.. facing entity {BV} eyes positioned ^ ^ ^0.6 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~ ~ 0',
                        f'execute facing entity {BV} feet rotated ~ 0 run function bm:p229/place',
                        f'execute if score @s bm.hqdt matches 5.. if entity {BV.replace("limit=1", "distance=..1.3,limit=1")} run return run function bm:p234/duo/mount',
                        'execute if score @s bm.hqdt matches 14.. run function bm:p234/duo/mount'])
    fn('p234/duo/mount', [f'ride @s mount {BV}', 'tag @s add bm.rdr', 'data merge entity @s {NoGravity:0b}', f'tag {BV} add bm.bvseat',
                          'scoreboard players set @s bm.hqdp 2', 'scoreboard players set @s bm.hqdt 0', pose('perch'),
                          'playsound minecraft:entity.cat.purreow neutral @a[distance=..20] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..20] ~ ~ ~ 1 0.9',
                          'particle minecraft:poof ~ ~1 ~ 0.3 0.2 0.3 0.02 6'])
    # up there: a swipe every 11 ticks at whatever's close (alternate paws - a monster shrugs off a second blow inside half a
    #  second), for five seconds - or till there's nothing to swipe at
    fn('p234/duo/ride', ['execute unless entity @s[tag=bm.rdr] run return run function bm:p234/duo/finale',
                         'scoreboard players operation #h bm.rng = @s bm.hqdt', 'scoreboard players operation #h bm.rng %= #11 bm.rng',
                         f'execute if score #h bm.rng matches 0 if entity @e[{FOE},distance=..3.4] run function bm:p234/duo/swipe',
                         f'execute if score #h bm.rng matches 4 run {pose("perch")}',
                         f'execute if score @s bm.hqdt matches 22.. if score #h bm.rng matches 0 unless entity @e[{FOE},distance=..12] run return run function bm:p234/duo/finale',
                         'execute if score @s bm.hqdt matches 110.. run function bm:p234/duo/finale'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #11 bm.rng 11', 'scoreboard players set #22 bm.rng 22']
    fn('p234/duo/swipe', ['scoreboard players operation #h bm.rng = @s bm.hqdt', 'scoreboard players operation #h bm.rng %= #22 bm.rng',
                          f'execute if score #h bm.rng matches 0 run {pose("perch_l")}', f'execute unless score #h bm.rng matches 0 run {pose("perch_r")}',
                          'tag @s add bm.hyme', 'scoreboard players set #pd bm.rng 6', 'execute if predicate bm:p229/night run scoreboard players add #pd bm.rng 2',
                          f'execute as @e[{FOE},distance=..3.4,sort=nearest,limit=1] at @s run function bm:p229/swiped', 'tag @s remove bm.hyme',
                          'playsound minecraft:entity.cat.hiss neutral @a[distance=..16] ~ ~ ~ 0.4 1.5'])
    # the finish: off his back and onto a monster - Bender biting it at the same moment
    fn('p234/duo/finale', ['ride @s dismount', 'tag @s remove bm.rdr', f'execute as {BV} run function bm:p234/unduo_seat',
                           'scoreboard players set @s bm.hqdp 3', 'scoreboard players set @s bm.hqdt 0', 'data merge entity @s {NoAI:1b,NoGravity:1b}',
                           'tag @e[tag=bm.hydtg,distance=..32] remove bm.hydtg', f'tag @e[{FOE},distance=..8,sort=nearest,limit=1] add bm.hydtg', pose('perch_hop')])
    fn('p234/unduo_seat', ['execute unless function bm:p234/has_rider run tag @s remove bm.bvseat'])
    TG = '@e[tag=bm.hydtg,distance=..12,limit=1]'
    fn('p234/duo/leap', [f'execute if score @s bm.hqdt matches 1..3 if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~0.35 ~',
                         f'execute if score @s bm.hqdt matches 2 run {pose("pounce")}',
                         f'execute if score @s bm.hqdt matches 2..20 if entity {TG} facing entity {TG} feet positioned ^ ^ ^0.75 if block ~ ~ ~ #bm:grap_pass if block ~ ~0.4 ~ #bm:grap_pass run tp @s ~ ~ ~ ~ 0',
                         f'execute if score @s bm.hqdt matches 2..20 unless entity {TG} rotated as @s rotated ~ 0 positioned ^ ^ ^0.3 if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~',
                         f'execute if score @s bm.hqdt matches 4..20 as {TG} at @s if entity @e[type=minecraft:wolf,tag=bm.hypet,tag=bm.hyme2,distance=..1.4] run return run function bm:p234/duo/strike_as',
                         'execute if score @s bm.hqdt matches 4..29 if block ~ ~-0.3 ~ #bm:grap_pass run tp @s ~ ~-0.25 ~',
                         'execute if score @s bm.hqdt matches 21 run function bm:p234/duo/strike',
                         f'execute if score @s bm.hqdt matches 30 run {pose("land")}', 'execute if score @s bm.hqdt matches 30 run data merge entity @s {NoGravity:0b}',
                         f'execute if score @s bm.hqdt matches 38 run {pose("strut")}', 'execute if score @s bm.hqdt matches 56.. run function bm:p234/duo/done',
                         f'execute if score @s bm.hqdt matches ..29 if entity {TG} facing entity {TG} feet rotated ~ 0 run return run function bm:p229/place',
                         'execute rotated as @s rotated ~ 0 run function bm:p229/place'])
    G.FUNCS['p234/duo/tick'][0:0] = ['tag @s add bm.hyme2']
    G.FUNCS['p234/duo/tick'].append('tag @s remove bm.hyme2')
    fn('p234/duo/strike_as', ['execute as @e[type=minecraft:wolf,tag=bm.hyme2,limit=1] at @s run function bm:p234/duo/strike'])
    fn('p234/duo/strike', ['scoreboard players set @s bm.hqdt 22', pose('bite'), 'tag @s add bm.hyme', 'scoreboard players set #pd bm.rng 10',
                           'execute if predicate bm:p229/night run scoreboard players add #pd bm.rng 2',
                           f'execute as {TG} at @s run function bm:p229/fl/hurt', 'tag @s remove bm.hyme',
                           f'execute as {BV} at @s if entity {TG.replace("distance=..12", "distance=..3.4")} run function bm:p195/bite_go',
                           'particle minecraft:squid_ink ~ ~0.5 ~ 0.3 0.2 0.3 0.02 8'])
    fn('p234/duo/done', ['ride @s dismount', 'tag @s remove bm.rdr', 'scoreboard players set @s bm.hqx 1', 'scoreboard players set @s bm.hqdp 0',
                         'data merge entity @s {NoAI:0b,NoGravity:0b}', 'tag @e[tag=bm.hydtg,distance=..32] remove bm.hydtg'] + me_bv +
                        ['execute as @e[type=minecraft:wolf,tag=bm.dme] run function bm:p234/unduo_seat', 'tag @e[tag=bm.dme] remove bm.bvduo',
                         'tag @e[tag=bm.dme] remove bm.dme'] + FX.face_cmd('henry', 'happy', 40) +
       ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + line(H, '(and Bender look at each other, very pleased. Same time next week.)')])
    # (a double act cut short any way at all: Bender's own moves back)
    second.append('execute as @e[type=minecraft:wolf,tag=bm.bvduo] at @s run function bm:p234/duo/orphan')
    fn('p234/duo/orphan', ['scoreboard players operation #me bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:wolf,tag=bm.hypet,distance=..32,scores={bm.hqdp=1..}] if score @s bm.pid = #me bm.pid run return 0',
                           'tag @s remove bm.bvduo'])

    # ================================================================== THE NIGHT CUDDLE
    second.append('execute as @e[type=minecraft:wolf,tag=bm.bvpet,tag=!bm.cdl,tag=!bm.ffpet] at @s if dimension minecraft:overworld run function bm:p234/cdl/try')
    fn('p234/cdl/try', ['execute if score @s bm.cdlw matches ..-1 run return run scoreboard players add @s bm.cdlw 1',
                        'execute unless predicate bm:p229/night unless function bm:p234/cdl/owner_asleep run return run scoreboard players set @s bm.cdlw 0',
                        'execute unless function bm:p234/calm run return run scoreboard players set @s bm.cdlw 0',
                        f'execute if entity @e[{FOE},distance=..16] run return run scoreboard players set @s bm.cdlw 0',
                        'execute unless function bm:p234/cdl/owner_near run return run scoreboard players set @s bm.cdlw 0',
                        'scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute as @e[type=minecraft:wolf,tag=bm.hypet,tag=!bm.cdl,distance=..10] if score @s bm.pid = #me bm.pid if function bm:p234/cdl/cat_ok run tag @s add bm.cdh',
                        'execute as @e[type=minecraft:wolf,tag=bm.nipet,tag=!bm.cdl,distance=..10] if score @s bm.pid = #me bm.pid if function bm:p234/cdl/cat_ok run tag @s add bm.cdn',
                        'scoreboard players set #go bm.rng 2',
                        'execute if entity @e[type=minecraft:wolf,tag=bm.cdh,distance=..10] if entity @e[type=minecraft:wolf,tag=bm.cdn,distance=..10] run function bm:p234/cdl/roll',
                        'execute if score #go bm.rng matches 2 run scoreboard players set @s bm.cdlw 0',
                        'execute if score #go bm.rng matches 1 run function bm:p234/cdl/go',
                        'tag @e[tag=bm.cdh] remove bm.cdh', 'tag @e[tag=bm.cdn] remove bm.cdn'])
    # (both cats beside him: a calm second more - and from the tenth, one chance in twelve; at once if you're asleep in bed by them)
    fn('p234/cdl/roll', ['scoreboard players set #go bm.rng 0', 'scoreboard players add @s bm.cdlw 1',
                         'execute if function bm:p234/cdl/owner_asleep run return run scoreboard players set #go bm.rng 1',
                         'execute if score @s bm.cdlw matches ..9 run return 0',
                         'execute store result score #r bm.rng run random value 1..12', 'execute if score #r bm.rng matches 1 run scoreboard players set #go bm.rng 1'])
    fn('p234/cdl/cat_ok', [f'execute if score @s bm.{P229.Henry.q}x matches 1.. if entity @s[tag=bm.hypet] run return 0',
                           f'execute if score @s bm.{P229.Nia.q}x matches 1.. if entity @s[tag=bm.nipet] run return 0',
                           'execute if entity @s[tag=bm.rdr] run return 0', 'execute if data entity @s {Sitting:1b} run return 0',
                           'execute if data entity @s {OnGround:0b} run return 0', 'return 1'])
    fn('p234/cdl/owner_near', ['execute on owner if entity @s[distance=..10] run return 1', 'return 0'])
    fn('p234/cdl/owner_asleep', ['execute on owner if entity @s[distance=..16] unless data entity @s {SleepTimer:0s} run return 1', 'return 0'])
    fn('p234/cdl/spot', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~0.5 ~ #bm:grap_pass unless block ~ ~-0.3 ~ #bm:grap_pass run return 1', 'return 0'])
    hx, hy_, hz, hyaw = CUDDLE['henry']
    nx, ny, nz, nyaw = CUDDLE['nia']
    fn('p234/cdl/go', [f'execute rotated as @s rotated ~ 0 positioned ^{hx} ^{hy_} ^{hz} unless function bm:p234/cdl/spot run return run scoreboard players set @s bm.cdlw 0',
                       f'execute rotated as @s rotated ~ 0 positioned ^{nx} ^{ny} ^{nz} unless function bm:p234/cdl/spot run return run scoreboard players set @s bm.cdlw 0',
                       'function bm:p234/unseat', 'scoreboard players set @s bm.cdlw 0',
                       'tag @s add bm.cdl', 'data merge entity @s[type=minecraft:wolf] {NoAI:1b,Sitting:0b,Motion:[0d,0d,0d]}', 'tp @s ~ ~ ~ ~ 0',
                       f'execute rotated as @s rotated ~ 0 positioned ^{hx} ^{hy_} ^{hz} as @e[type=minecraft:wolf,tag=bm.cdh,limit=1] run tp @s ~ ~ ~ ~{hyaw} 0',
                       f'execute rotated as @s rotated ~ 0 positioned ^{nx} ^{ny} ^{nz} as @e[type=minecraft:wolf,tag=bm.cdn,limit=1] run tp @s ~ ~ ~ ~{nyaw} 0',
                       'execute as @e[type=minecraft:wolf,tag=bm.cdh] run function bm:p234/cdl/down', 'execute as @e[type=minecraft:wolf,tag=bm.cdn] run function bm:p234/cdl/down',
                       'playsound minecraft:entity.wolf.whine neutral @a[distance=..16] ~ ~ ~ 0.5 0.8', 'playsound minecraft:entity.cat.purr neutral @a[distance=..16] ~ ~ ~ 1 1',
                       'particle minecraft:heart ~ ~0.8 ~ 0.6 0.2 0.6 0 4',
                       'execute on owner if entity @s[distance=..16,tag=!bm.hush] run function bm:p234/cdl/tell'])
    fn('p234/cdl/down', ['tag @s add bm.cdl', 'data merge entity @s[type=minecraft:wolf] {NoAI:1b,Sitting:0b,Motion:[0d,0d,0d]}'])
    fn('p234/cdl/tell', [tellraw('@s', [T('Bender flops down with a big sigh. ', P195.BV_LINE, italic=True),
                                        T('Henry and Nia curl up against him, one on each side - and all three of them are asleep in moments.', 'gray', italic=True)]),
                         'advancement grant @s only bm:story/cuddle_pile'])
    wjson('bm/advancement/story/cuddle_pile.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                   'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:nia_bell'}},
                                                               'title': T('A Dog and Two Cats, Asleep', 'yellow'),
                                                               'description': T('Let Bender, Henry and Nia curl up together on a quiet night', 'gray'),
                                                               'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    # while they sleep (as Bender, each second): a heart, a purr, a snore - and every reason to wake
    second.append('execute as @e[type=minecraft:wolf,tag=bm.bvpet,tag=bm.cdl] at @s run function bm:p234/cdl/sec')
    fn('p234/cdl/sec', ['scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute unless predicate bm:p229/night unless function bm:p234/cdl/owner_asleep run return run function bm:p234/cdl/wake',
                        f'execute if entity @e[{FOE},distance=..12] run return run function bm:p234/cdl/wake',
                        'execute unless function bm:p234/cdl/owner_by run return run function bm:p234/cdl/wake',
                        'execute if data entity @s {Sitting:1b} run return run function bm:p234/cdl/wake',
                        'execute store result score #n bm.rng if entity @e[type=minecraft:wolf,tag=bm.cdl,tag=!bm.bvpet,distance=..2,nbt={Sitting:0b}]',
                        'execute if score #n bm.rng matches ..1 run return run function bm:p234/cdl/wake',
                        'execute store result score #r bm.rng run random value 1..6',
                        'execute if score #r bm.rng matches 1 run particle minecraft:heart ~ ~0.9 ~ 0.4 0.1 0.4 0 1',
                        'execute if score #r bm.rng matches 2 run playsound minecraft:entity.cat.purr neutral @a[distance=..12] ~ ~ ~ 0.6 1.1',
                        'execute if score #r bm.rng matches 3 run playsound minecraft:entity.wolf.pant neutral @a[distance=..12] ~ ~ ~ 0.3 0.6'])
    fn('p234/cdl/owner_by', ['execute on owner if entity @s[distance=..16] run return 1', 'return 0'])
    fn('p234/cdl/wake', ['execute as @e[type=minecraft:wolf,tag=bm.cdl,distance=..3] if score @s bm.pid = #me bm.pid at @s run function bm:p234/cdl/up1',
                         'scoreboard players set @s bm.cdlw -180',
                         'execute on owner if entity @s[distance=..16,tag=!bm.hush] run ' + bsay('(stretches, yawns enormously - and all three of them are up, as if nothing happened)')])
    fn('p234/cdl/up1', ['tag @s remove bm.cdl', 'data merge entity @s[type=minecraft:wolf] {NoAI:0b,Sitting:0b}', 'execute at @s run particle minecraft:poof ~ ~0.3 ~ 0.2 0.1 0.2 0.01 3'])
    # (a cat whose Bender has gone - sent home, fainted - wakes up)
    second.append('execute as @e[type=minecraft:wolf,tag=bm.cdl,tag=!bm.bvpet] at @s unless entity @e[type=minecraft:wolf,tag=bm.bvpet,tag=bm.cdl,distance=..3] run function bm:p234/cdl/up1')

    G.FUNCS['tick'] += tick
    G.FUNCS['loop/second'][-1:-1] = second
    G.FUNCS['admin/uninstall'][0:0] = ['tag @e[tag=bm.rdr] remove bm.rdr', 'tag @e[tag=bm.cdl] remove bm.cdl']
