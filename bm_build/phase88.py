"""2.67: THE GUTTER GENTRY - a hidden boss trio, found only behind a hidden vault's secret door (Tier II and up).

BATTY    a bat the size of a man, roosting upside down from the parlour ceiling. He swoops; now and then he
                SCREECHES (darkness and slowness for all close by).
EGGBERT      a cracked egg full of black ooze, on talons, with long dripping arms. He lunges, and leaves OOZE
                behind him (slowness and wither if you stand in it).
THE COUNT  a grumpy blob in a top hat, with a cane. He bounces about, SWATS everything near him away, and tips his
                hat to call his BLOBLINGS.
They start together; each one that falls makes the others angrier. All three down: the Gentry's hoard opens - each of
you gets a share (into your haul) and one of their treasures:
  DANGLE'S ECHO BELL      ring it: every creature within 32 blocks glows for 8 seconds (20 s to ring again)
  YOLKSHELL HELM          a helmet of egg shell; whatever hurts you is splashed with ooze (slowed and blinded)
  BLOBSWORTH'S CANE       a cane that hits like a sword, knocks foes back - and bounces them into the air
  BLOBSWORTH'S TOP HAT    the very hat (worn: a little luck, and very dapper)
Their health grows with the tier and with your crew.
"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase75_rooms as R5
import phase88_art as ART

GOLD = '#ffcf40'
GENT = '#c8a0ff'
NAMES = {'bat': ('Batty', '#8a8ad8'), 'egg': ('Eggbert', '#d8d4c0'), 'blob': ('The Count', '#a8c8f0')}
HP = {'bat': (80, 30), 'egg': (140, 40), 'blob': (110, 35)}        # (base, + per tier); +50% per crewmate past the first

item('echo_bell', TOTEM, "Batty's Echo Bell", '#8a8ad8', ['A little bell on a bat\'s collar.', ('Use: every creature within 32 blocks', 'blue'),
                                                          ('glows for 8 seconds.', 'blue'), ('From the Gutter Gentry.', 'dark_purple')],
     model='bm:echo_bell', stack=1, cat='magic', comps=dict(hold('none'), **{'minecraft:use_cooldown': {'seconds': 20.0, 'cooldown_group': 'bm:echo_bell'}}))
HOLD['echo_bell'] = 'bm:p88/item/echo'
item('yolkshell_helm', 'minecraft:leather_helmet', "Eggbert's Yolkshell Helm", '#e8e4d4', ['A cap of cracked egg shell, still sticky.', ('Whatever hurts you is splashed with', 'blue'),
                                                                               ('ooze: slowed and blinded.', 'blue'), ('From the Gutter Gentry.', 'dark_purple')],
     comps={'minecraft:dyed_color': 0xe8e4d4, 'minecraft:attribute_modifiers': [
         {'type': 'minecraft:armor', 'id': 'bm:yolk', 'amount': 3.0, 'operation': 'add_value', 'slot': 'head'},
         {'type': 'minecraft:armor_toughness', 'id': 'bm:yolk_t', 'amount': 2.0, 'operation': 'add_value', 'slot': 'head'}]}, cat='armor')
item('blob_cane', 'minecraft:stick', "The Count's Cane", '#a8c8f0', ['Black lacquer and a silver tip.', ('Hits like a sword; knocks foes back', 'blue'),
                                                                     ('and bounces them into the air.', 'blue'), ('From the Gutter Gentry.', 'dark_purple')],
     model='bm:blob_cane', stack=1, cat='weapon',
     comps={'minecraft:attribute_modifiers': [{'type': 'minecraft:attack_damage', 'id': 'bm:cane', 'amount': 6.0, 'operation': 'add_value', 'slot': 'mainhand'},
                                              {'type': 'minecraft:attack_speed', 'id': 'bm:cane_s', 'amount': -2.2, 'operation': 'add_value', 'slot': 'mainhand'}],
            'minecraft:enchantments': {'minecraft:knockback': 2}})
item('blob_top_hat', TOTEM, "The Count's Top Hat", '#a8c8f0', ['Tall, black, and a red silk band.', ('Worn: a little luck - and very dapper.', 'blue'),
                                                               ('From the Gutter Gentry.', 'dark_purple')],
     model='bm:top_hat', stack=1, cat='cosmetic', comps={'minecraft:equippable': {'slot': 'head'}})
UNIQUES = ['echo_bell', 'yolkshell_helm', 'blob_cane', 'blob_top_hat']


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    rel = RM.rel
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    tick, fast, second = [], [], []
    objs = ['bm.gntid', 'bm.gntt', 'bm.gntc', 'bm.gntd', 'bm.gnty', 'bm.gnts', 'bm.gntf', 'bm.gntx', 'bm.gntz', 'bm.gnth', 'bm.gnta', 'bm.gntk', 'bm.gntv']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'bossbar add bm:gnt{s} ' + snbt(T('The Gutter Gentry', GENT, bold=True)) for s in range(P70.SLOTS)] + \
        [f'bossbar set bm:gnt{s} color purple' for s in range(P70.SLOTS)] + ['scoreboard players set #k16 bm.rng 16']
    G.OBJECTIVES += objs
    ident = [F(0), F(0), F(0), F(1)]
    def xf(t, q, s):
        sc = s if isinstance(s, tuple) else (s, s, s)
        return {'translation': [F(round(v, 4)) for v in t], 'left_rotation': [F(round(v, 5)) for v in q], 'right_rotation': ident, 'scale': [F(round(v, 4)) for v in sc]}

    # ================================================================== THE TRIO: hosts, their display parts, poses
    HOSTS = {'bat': ('minecraft:vex', {'NoGravity': B(1)}),          # (2.82: a vex, not a phantom - a phantom could stick to the ceiling)
              'egg': ('minecraft:husk', {}), 'blob': ('minecraft:husk', {})}
    HITBOX = {'bat': (2.2, 1.6, -0.3), 'egg': (1.9, 2.5, 0.0), 'blob': (2.2, 2.0, 0.0)}      # (each body's own box: width, height, drop)
    ATTR = {'bat': [('minecraft:attack_damage', 7.0), ('minecraft:knockback_resistance', 0.4)],
            'egg': [('minecraft:attack_damage', 9.0), ('minecraft:movement_speed', 0.22), ('minecraft:scale', 1.35), ('minecraft:knockback_resistance', 0.7),
                    ('minecraft:follow_range', 40.0)],
            'blob': [('minecraft:attack_damage', 6.0), ('minecraft:movement_speed', 0.2), ('minecraft:knockback_resistance', 0.5), ('minecraft:follow_range', 40.0)]}
    START = {'bat': ('roost', (12, 11, 6)), 'egg': ('idle0', (16, 4, 17)), 'blob': ('idle0', (8, 4, 16))}
    def host(k):
        ent, extra = HOSTS[k]
        d = dict({'Tags': ['bm.gnt', f'bm.gnt_{k}', 'bm.gvprop', 'bm.gntn'], 'NoAI': B(1), 'PersistenceRequired': B(1), 'DeathLootTable': 'minecraft:empty',
                  'CustomName': T(NAMES[k][0], NAMES[k][1], bold=True), 'Silent': B(1 if k != 'bat' else 0),
                  'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)},
                                     {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}],
                  'attributes': [{'id': a, 'base': D(v)} for a, v in ATTR[k]]}, **extra)
        return f'summon {ent} ~ ~ ~ {snbt(d)}'
    def parts_of(k, pose):
        out = []
        for part, (t, q, s) in ART.POSES[k][pose].items():
            d = {'Tags': ['bm.gntp', f'bm.gntp_{k}', f'bm.gntp_{k}_{part}', 'bm.gvprop', 'bm.gntn'], 'teleport_duration': Int(2), 'interpolation_duration': Int(4),
                 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{ART.PARTS[k][part]}'}}, 'item_display': 'fixed',
                 'view_range': F(2.0), 'transformation': xf(t, q, s)}
            if (k, part) in ART.LIT: d['brightness'] = {'sky': Int(15), 'block': Int(15)}
            out.append(f'summon minecraft:item_display ~ ~ ~ {snbt(d)}')
        w, h, dy = HITBOX[k]
        out.append(f'summon minecraft:interaction ~ ~{dy} ~ ' + snbt({'Tags': ['bm.bhit', 'bm.bhit_gnt', 'bm.gvprop', 'bm.gntn'], 'width': F(w), 'height': F(h)}))
        return out
    # every keyframe blends over its own length: a gait's frame over the gait's period, an act's step over the step
    DUR = {}
    for k in HOSTS:
        for st, (per, frames) in ART.ANIMS[k].items():
            for i in range(len(frames)): DUR[(k, f'{st}{i}')] = per
        for a, steps in ART.ACTS[k].items():
            for i, (t, _f) in enumerate(steps): DUR[(k, f'{a}{i}')] = t
    for k in HOSTS:
        for pose, pp in ART.POSES[k].items():
            fn(f'p88/pose/{k}_{pose}', [f'execute as @e[type=minecraft:item_display,tag=bm.gntp_{k}_{part},distance=..6] if score @s bm.gntid = #id bm.rng run data merge entity @s '
                                       + snbt({'start_interpolation': Int(0), 'interpolation_duration': Int(DUR.get((k, pose), 4)), 'transformation': xf(t, q, s)})
                                       for part, (t, q, s) in pp.items()])
    # ---- the parlour wakes: three hosts, their parts, the bar
    start = ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx', 'function bm:p87/crew']
    for j, (k, (pose, (x, y, z))) in enumerate(START.items(), 1):
        base, per = HP[k]
        start += ['scoreboard players operation #id bm.rng = #gi bm.rng', 'scoreboard players operation #id bm.rng *= #k10 bm.rng', f'scoreboard players add #id bm.rng {j}',
                  f'execute positioned {rel(x, y, z)} run {host(k)}', f'execute positioned {rel(x, y, z)} run function bm:p88/parts_{k}',
                  f'scoreboard players set #h bm.rng {base}', f'scoreboard players set #q bm.rng {per}', 'scoreboard players operation #q bm.rng *= #gt bm.rng',
                  'scoreboard players operation #h bm.rng += #q bm.rng', 'scoreboard players operation #hf bm.rng = #crew bm.rng', 'scoreboard players remove #hf bm.rng 1',
                  'scoreboard players operation #hf bm.rng *= #k50 bm.rng', 'scoreboard players add #hf bm.rng 100', 'scoreboard players operation #h bm.rng *= #hf bm.rng',
                  'scoreboard players operation #h bm.rng /= #k100 bm.rng',
                  'execute as @e[tag=bm.gntn,distance=..30] run scoreboard players operation @s bm.gntid = #id bm.rng',
                  'execute as @e[tag=bm.gntn,distance=..30] run scoreboard players operation @s bm.gvi = #gi bm.rng',
                  'execute as @e[type=minecraft:interaction,tag=bm.gntn,distance=..30] run scoreboard players operation @s bm.hbid = #id bm.rng',
                  f'execute as @e[tag=bm.gnt_{k},tag=bm.gntn,distance=..30] run function bm:p88/anim/init',
                  f'execute as @e[tag=bm.gnt_{k},tag=bm.gntn,distance=..30] run function bm:p88/sethp', 'tag @e[tag=bm.gntn,distance=..30] remove bm.gntn']
    start += ['scoreboard players set @s bm.gntt 0', 'tag @s add bm.gntlive',
              'title @a[tag=bm.gvp,distance=..24] times 10 60 20', title('@a[tag=bm.gvp,distance=..24]', 'title', T('THE GUTTER GENTRY', GENT, bold=True)),
              title('@a[tag=bm.gvp,distance=..24]', 'subtitle', [T('Batty', NAMES['bat'][1]), T('  ·  ', 'gray'), T('Eggbert', NAMES['egg'][1]),
                                                                T('  ·  ', 'gray'), T('The Count', NAMES['blob'][1])]),
              'playsound minecraft:entity.wither.spawn hostile @a[distance=..30] ~ ~ ~ 0.5 1.4', 'playsound minecraft:block.bell.use hostile @a[distance=..30] ~ ~ ~ 1 0.6']
    fn('p88/lair/start', start)
    for k in HOSTS:
        fn(f'p88/parts_{k}', parts_of(k, START[k][0]))
    fn('p88/sethp', ['execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                     'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng',
                     'execute store result score @s bm.gntd run scoreboard players get #h bm.rng'])
    # ---- the lair, every tick while it's live: a 3-second bow, then the fight; parts follow their hosts
    tick.append('execute as @e[type=minecraft:marker,tag=bm.gvhvr_lair,tag=bm.gntlive] at @s run function bm:p88/lair/tick')
    fn('p88/lair/tick', ['scoreboard players add @s bm.gntt 1',
                         'execute if score @s bm.gntt matches 60 as @e[tag=bm.gnt,distance=..24] run data modify entity @s NoAI set value 0b',
                         'execute if score @s bm.gntt matches 60 as @e[tag=bm.gnt_bat,distance=..24] at @s run function bm:p88/bat/wake',
                         'kill @e[type=minecraft:slime,tag=!bm.gnt,tag=!bm.gntl,distance=..24]',
                         'execute as @e[type=minecraft:slime,tag=bm.gnt,distance=..24] unless score @s bm.gntid matches 1.. run kill @s',     # (The Count's split - it copies his tags)
                         'execute as @e[tag=bm.gnt,distance=..30] at @s run function bm:p88/follow'])
    fn('p88/follow', ['scoreboard players operation #id bm.rng = @s bm.gntid', 'scoreboard players add @s bm.gntt 1',
                      'execute as @e[type=minecraft:item_display,tag=bm.gntp,distance=..6] if score @s bm.gntid = #id bm.rng run tp @s ~ ~ ~ ~ 0',
                      'execute if entity @s[tag=bm.gnt_bat] as @e[type=minecraft:interaction,tag=bm.bhit_gnt,distance=..8] if score @s bm.hbid = #id bm.rng run tp @s ~ ~-0.3 ~',
                      'execute if entity @s[tag=!bm.gnt_bat] as @e[type=minecraft:interaction,tag=bm.bhit_gnt,distance=..8] if score @s bm.hbid = #id bm.rng run tp @s ~ ~ ~',
                      'execute unless entity @s[nbt={NoAI:1b}] run function bm:p88/anim/go',
                      'execute if entity @s[tag=bm.gnt_bat] run function bm:p88/bat/tick', 'execute if entity @s[tag=bm.gnt_egg] run function bm:p88/egg/tick',
                      'execute if entity @s[tag=bm.gnt_blob] run function bm:p88/blob/tick'])
    # ---- Batty: wing beats; a screech every 7 s
    fn('p88/bat/wake', ['scoreboard players operation #id bm.rng = @s bm.gntid', 'scoreboard players set @s bm.gnts -1', 'execute at @s run function bm:p88/pose/bat_idle0',
                        'execute at @s run playsound minecraft:entity.bat.takeoff hostile @a[distance=..30] ~ ~ ~ 1 0.6'])
    fn('p88/bat/tick', ['execute if entity @s[nbt={NoAI:1b}] run return 0',
                        'scoreboard players add @s bm.gntc 1', 'execute if score @s bm.gntc matches 140.. run function bm:p88/bat/screech',
                        'execute if score @s bm.gnta matches 0 if entity @a[tag=bm.gvp,distance=..2.6] if predicate bm:p88/chance10 run function bm:p88/act/bat_bite/start'])
    fn('p88/bat/screech', ['scoreboard players set @s bm.gntc 0', 'function bm:p88/act/bat_screech/start', 'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1',
                           'playsound minecraft:entity.bat.death hostile @a[distance=..30] ~ ~ ~ 1.4 0.5', 'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..30] ~ ~ ~ 0.5 1.8',
                           'effect give @a[tag=bm.gvp,distance=..10] minecraft:darkness 4 0', 'effect give @a[tag=bm.gvp,distance=..10] minecraft:slowness 3 1',
                           title('@a[tag=bm.gvp,distance=..10]', 'actionbar', T('Batty SCREECHES!', NAMES['bat'][1], bold=True))])
    # ---- Eggbert: a waddle, a lunge every 4.5 s, ooze every 6 s
    fn('p88/egg/tick', ['execute if entity @s[nbt={NoAI:1b}] run return 0',
                        'execute if score @s bm.gnta matches 0 if entity @a[tag=bm.gvp,distance=..2.8] if predicate bm:p88/chance10 run function bm:p88/act/egg_swipe/start',
                        'scoreboard players add @s bm.gntc 1', 'execute if score @s bm.gntc matches 90 run function bm:p88/egg/lunge',
                        'execute if score @s bm.gntc matches 120.. run function bm:p88/egg/ooze'])
    fn('p88/egg/lunge', ['function bm:p88/act/egg_swipe/start', 'execute facing entity @p[tag=bm.gvp,distance=..16] feet run tp @s ~ ~ ~ ~ ~',
                         'execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["bm.gntmv"]}',
                         'execute store result score #x bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gntmv,limit=1] Pos[0] 100',
                         'execute store result score #z bm.rng run data get entity @e[type=minecraft:marker,tag=bm.gntmv,limit=1] Pos[2] 100',
                         'execute store result score #x0 bm.rng run data get entity @s Pos[0] 100', 'execute store result score #z0 bm.rng run data get entity @s Pos[2] 100',
                         'scoreboard players operation #x bm.rng -= #x0 bm.rng', 'scoreboard players operation #z bm.rng -= #z0 bm.rng', 'kill @e[type=minecraft:marker,tag=bm.gntmv]',
                         'execute store result entity @s Motion[0] double 0.012 run scoreboard players get #x bm.rng',
                         'execute store result entity @s Motion[2] double 0.012 run scoreboard players get #z bm.rng', 'data modify entity @s Motion[1] set value 0.42d',
                         'playsound minecraft:entity.ravager.roar hostile @a[distance=..24] ~ ~ ~ 0.6 1.6'])
    ooze = {'Tags': ['bm.gvprop'], 'Radius': F(3.0), 'Duration': Int(160), 'WaitTime': Int(0), 'ReapplicationDelay': Int(20), 'RadiusPerTick': F(0),
            'custom_particle': {'type': 'minecraft:dust', 'color': [F(0.05), F(0.05), F(0.06)], 'scale': F(1.6)},
            'potion_contents': {'custom_effects': [{'id': 'minecraft:slowness', 'amplifier': B(1), 'duration': Int(60)},
                                                   {'id': 'minecraft:wither', 'amplifier': B(0), 'duration': Int(60)}]}}
    fn('p88/egg/ooze', ['scoreboard players set @s bm.gntc 0', 'function bm:p88/act/egg_ooze/start', f'summon minecraft:area_effect_cloud ~ ~0.1 ~ {snbt(ooze)}',
                        'particle minecraft:squid_ink ~ ~1.5 ~ 1 0.5 1 0.05 40', 'playsound minecraft:block.honey_block.slide hostile @a[distance=..24] ~ ~ ~ 1 0.5'])
    # ---- The Count: a bounce; a swat every 5 s, bloblings every 8 s
    fn('p88/blob/tick', ['execute if entity @s[nbt={NoAI:1b}] run return 0',
                         'execute if score @s bm.gnta matches 0 if entity @a[tag=bm.gvp,distance=..2.6] if predicate bm:p88/chance10 run function bm:p88/act/blob_swat/start',
                         'scoreboard players add @s bm.gntc 1', 'execute if score @s bm.gntc matches 100 run function bm:p88/blob/swat',
                         'execute if score @s bm.gntc matches 160.. run function bm:p88/blob/call'])
    fn('p88/blob/swat', ['function bm:p88/act/blob_swat/start', 'execute as @a[tag=bm.gvp,distance=..4] run damage @s 5 minecraft:mob_attack by @e[tag=bm.gnt_blob,limit=1,sort=nearest]',
                         'playsound minecraft:entity.player.attack.knockback hostile @a[distance=..24] ~ ~ ~ 1 0.6', 'particle minecraft:sweep_attack ~ ~1 ~ 1.5 0.3 1.5 0 6'])
    ling = {'Tags': ['bm.gvprop', 'bm.gntl'], 'Size': Int(0), 'PersistenceRequired': B(1), 'DeathLootTable': 'minecraft:empty', 'CustomName': T('Blobling', '#a8c8f0')}
    fn('p88/blob/call', ['scoreboard players set @s bm.gntc 0', 'function bm:p88/act/blob_tip/start', f'summon minecraft:slime ~1 ~0.5 ~ {snbt(ling)}', f'summon minecraft:slime ~-1 ~0.5 ~ {snbt(ling)}',
                         'playsound minecraft:entity.slime.squish_small hostile @a[distance=..24] ~ ~ ~ 1 0.7',
                         title('@a[tag=bm.gvp,distance=..14]', 'actionbar', T('The Count tips his hat - Bloblings!', NAMES['blob'][1], bold=True))])
    # ---- THE ANIMATION: the gait follows how fast each one is really moving (a smoothed speed), and whether he's off the
    #      ground (Batty: diving); an act (an attack) plays through, then the gait picks up again
    wjson('bm/predicate/p88/chance10.json', {'condition': 'minecraft:random_chance', 'chance': 0.1})
    fn('p88/anim/init', ['execute store result score @s bm.gntx run data get entity @s Pos[0] 100', 'execute store result score @s bm.gntz run data get entity @s Pos[2] 100',
                         'execute store result score @s bm.gnth run data get entity @s Pos[1] 100', 'scoreboard players set @s bm.gntv 0',
                         'scoreboard players set @s bm.gnts -1', 'scoreboard players set @s bm.gnta 0'])
    GAIT = {'idle': 1, 'walk': 2, 'run': 3, 'jump': 4}
    fn('p88/anim/go', ['execute if score @s bm.gnta matches 1.. run return run function bm:p88/anim/act',
                       'execute store result score #x bm.rng run data get entity @s Pos[0] 100', 'execute store result score #z bm.rng run data get entity @s Pos[2] 100',
                       'execute store result score #y bm.rng run data get entity @s Pos[1] 100',
                       'scoreboard players operation #dx bm.rng = #x bm.rng', 'scoreboard players operation #dx bm.rng -= @s bm.gntx',
                       'scoreboard players operation #dz bm.rng = #z bm.rng', 'scoreboard players operation #dz bm.rng -= @s bm.gntz',
                       'scoreboard players operation #dy bm.rng = #y bm.rng', 'scoreboard players operation #dy bm.rng -= @s bm.gnth',
                       'scoreboard players operation @s bm.gntx = #x bm.rng', 'scoreboard players operation @s bm.gntz = #z bm.rng', 'scoreboard players operation @s bm.gnth = #y bm.rng',
                       'scoreboard players operation #dx bm.rng *= #dx bm.rng', 'scoreboard players operation #dz bm.rng *= #dz bm.rng',
                       'scoreboard players operation #dx bm.rng += #dz bm.rng', 'execute if score #dx bm.rng matches 2000.. run scoreboard players set #dx bm.rng 2000',
                       # (smoothed: three parts the old, one part the new - a stumble doesn't break the stride)
                       'scoreboard players operation @s bm.gntv *= #3 bm.rng', 'scoreboard players operation @s bm.gntv += #dx bm.rng', 'scoreboard players operation @s bm.gntv /= #4 bm.rng',
                       'scoreboard players set #st bm.rng 1', 'execute if score @s bm.gntv matches 6.. run scoreboard players set #st bm.rng 2',
                       'execute if score @s bm.gntv matches 230.. run scoreboard players set #st bm.rng 3',
                       'execute if entity @s[tag=!bm.gnt_bat,nbt={OnGround:0b}] run scoreboard players set #st bm.rng 4',
                       'execute if entity @s[tag=bm.gnt_bat] if score #dy bm.rng matches ..-14 run scoreboard players set #st bm.rng 4',
                       'execute unless score #st bm.rng = @s bm.gnts run scoreboard players set @s bm.gntf -1', 'scoreboard players operation @s bm.gnts = #st bm.rng'] +
       [f'execute if entity @s[tag=bm.gnt_{k}] if score #st bm.rng matches {n} run return run function bm:p88/gait/{k}_{st}' for k in HOSTS for st, n in GAIT.items()])
    for k in HOSTS:
        for st, (per, frames) in ART.ANIMS[k].items():
            n = len(frames)
            fn(f'p88/gait/{k}_{st}', ['scoreboard players add @s bm.gntf 1', f'execute if score @s bm.gntf matches {per * n}.. run scoreboard players set @s bm.gntf 0'] +
               [f'execute if score @s bm.gntf matches {i * per} run return run function bm:p88/pose/{k}_{st}{i}' for i in range(n)])
    ACT_ID = {}
    for k in HOSTS:
        for j, (a, steps) in enumerate(ART.ACTS[k].items(), 1):
            ACT_ID[(k, a)] = j
            fn(f'p88/act/{k}_{a}/start', [f'scoreboard players set @s bm.gntk {j}', 'scoreboard players set @s bm.gnta 0', 'function bm:p88/anim/act'])
    act = ['scoreboard players add @s bm.gnta 1']
    for (k, a), j in ACT_ID.items():
        t = 1
        for i, (d, _f) in enumerate(ART.ACTS[k][a]):
            act.append(f'execute if entity @s[tag=bm.gnt_{k}] if score @s bm.gntk matches {j} if score @s bm.gnta matches {t} run function bm:p88/pose/{k}_{a}{i}')
            t += d
        act.append(f'execute if entity @s[tag=bm.gnt_{k}] if score @s bm.gntk matches {j} if score @s bm.gnta matches {t}.. run function bm:p88/anim/act_end')
    fn('p88/anim/act', act)
    fn('p88/anim/act_end', ['scoreboard players set @s bm.gnta 0', 'scoreboard players set @s bm.gnts -1'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3', 'scoreboard players set #4 bm.rng 4']
    # (their hitboxes: a blow lands on the one inside, like the big bosses')
    h = G.FUNCS['p82/hb/hit']; h.insert(next(i for i, l in enumerate(h) if 'bhit_sal' in l) + 1, 'execute if entity @s[tag=bm.bhit_gnt] run scoreboard players set #hbk bm.rng 3')
    r = G.FUNCS['p82/hb/relay']; r.insert(r.index('tag @s remove bm.hbatk'),
                                          'execute if score #hbk bm.rng matches 3 as @e[tag=bm.gnt] if score @s bm.gntid = #hbid bm.rng at @s run function bm:p82/hb/dmg with storage bm:tmp hb')
    o = G.FUNCS['p82/hb/orphan']; o.insert(o.index('kill @s'), 'execute if entity @s[tag=bm.bhit_gnt] as @e[tag=bm.gnt,distance=..32] if score @s bm.gntid = #hbid bm.rng run return 0')

    # ---- every second: the bar; a fallen member's parts burst; the others grow angry; all three down - the hoard opens
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvhvr_lair,tag=bm.gntlive] at @s run function bm:p88/lair/sec')
    # (a slime splits only once its death throes are over - so its leavings are swept up every second, fight or no fight)
    second.append('execute as @e[type=minecraft:marker,tag=bm.gvhvr_lair] at @s as @e[type=minecraft:slime,tag=!bm.gntl,distance=..30] unless score @s bm.gntid matches 1.. run kill @s')
    fn('p88/lair/sec', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #hp bm.rng 0', 'scoreboard players set #hm bm.rng 0',
                        'execute as @e[tag=bm.gnt,distance=..30] run function bm:p88/hpsum'] +
       [f'execute if score #gi bm.rng matches {s + 1} run function bm:p88/bar{s}' for s in range(P70.SLOTS)] +
       ['execute as @e[type=minecraft:item_display,tag=bm.gntp,distance=..30] at @s run function bm:p88/orphan',
        'execute if score @s bm.gntt matches 80.. unless entity @e[tag=bm.gnt,distance=..30] run function bm:p88/lair/won'])
    fn('p88/hpsum', ['execute store result score #v bm.rng run data get entity @s Health', 'scoreboard players operation #hp bm.rng += #v bm.rng',
                     'scoreboard players operation #hm bm.rng += @s bm.gntd'])
    for s in range(P70.SLOTS):
        fn(f'p88/bar{s}', [f'execute store result bossbar bm:gnt{s} max run scoreboard players get #hm bm.rng',
                           f'execute store result bossbar bm:gnt{s} value run scoreboard players get #hp bm.rng',
                           f'bossbar set bm:gnt{s} players @a[tag=bm.gvp,distance=..24]'])
    fn('p88/orphan', ['scoreboard players operation #id bm.rng = @s bm.gntid', 'scoreboard players set #ok bm.rng 0',
                      'execute as @e[tag=bm.gnt,distance=..40] if score @s bm.gntid = #id bm.rng run scoreboard players set #ok bm.rng 1',
                      'execute if score #ok bm.rng matches 1 run return 0'] +
       [f'execute if entity @s[tag=bm.gntp_{k}_body] run function bm:p88/down_{k}' for k in HOSTS] + ['kill @s'])
    for k in HOSTS:
        nm, col = NAMES[k]
        fx = {'bat': ['particle minecraft:large_smoke ~ ~1.5 ~ 0.8 0.8 0.8 0.05 40', 'playsound minecraft:entity.bat.death hostile @a[distance=..30] ~ ~ ~ 1.4 0.4'],
              'egg': ['particle minecraft:squid_ink ~ ~1.5 ~ 1 1 1 0.1 80', 'particle minecraft:item{item:"minecraft:egg"} ~ ~1.5 ~ 0.8 0.8 0.8 0.15 40',
                      'playsound minecraft:entity.turtle.egg_crack hostile @a[distance=..30] ~ ~ ~ 1.5 0.5'],
              'blob': ['particle minecraft:item_slime ~ ~1 ~ 1 0.8 1 0.1 60', 'playsound minecraft:entity.slime.death hostile @a[distance=..30] ~ ~ ~ 1.5 0.5']}[k]
        fn(f'p88/down_{k}', fx + [tellraw('@a[tag=bm.gvp,distance=..30]', P + [T(nm, col, bold=True), T(' is beaten! ', 'gray'), T('The others grow angry...', 'red')]),
                                  'effect give @e[tag=bm.gnt,distance=..30] minecraft:strength 600 0 true', 'effect give @e[tag=bm.gnt,distance=..30] minecraft:speed 600 0 true'])
    fn('p88/lair/won', ['tag @s remove bm.gntlive', 'tag @s remove bm.gvhvlock',
                        'data modify entity @e[type=minecraft:text_display,tag=bm.gvhvt,distance=..4,limit=1] text set value '
                        + snbt([T("THE GENTRY'S HOARD\n", GENT, bold=True), T('right-click: your share', 'gray')]),
                        'kill @e[type=minecraft:slime,tag=bm.gntl,distance=..30]', 'kill @e[type=minecraft:slime,tag=!bm.gnt,distance=..30]',
                        'execute as @e[type=minecraft:slime,distance=..30] unless score @s bm.gntid matches 1.. run kill @s'] +
       [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gnt{s} players' for s in range(P70.SLOTS)] +
       ['title @a[tag=bm.gvp,distance=..30] times 10 60 20', title('@a[tag=bm.gvp,distance=..30]', 'title', T('THE GENTRY IS BROKEN', GENT, bold=True)),
        title('@a[tag=bm.gvp,distance=..30]', 'subtitle', T('Their hoard is yours - a share each, and a treasure', 'gray')),
        'playsound minecraft:ui.toast.challenge_complete player @a[distance=..30] ~ ~ ~ 1 0.9',
        'particle minecraft:totem_of_undying ~ ~2 ~ 1 1 1 0.4 80'])
    # the hits they take: a grunt each (they're mostly Silent)
    wjson('bm/advancement/p88/hit.json', {'criteria': {'h': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.gnt"]}'}}]}}}, 'rewards': {'function': 'bm:p88/hit'}})
    fn('p88/hit', ['advancement revoke @s only bm:p88/hit', 'execute at @s as @e[tag=bm.gnt,distance=..24,limit=1,sort=nearest] at @s run function bm:p88/ouch'])
    fn('p88/ouch', ['execute if entity @s[tag=bm.gnt_egg] run playsound minecraft:entity.turtle.egg_crack hostile @a[distance=..24] ~ ~ ~ 0.7 0.7',
                    'execute if entity @s[tag=bm.gnt_blob] run playsound minecraft:entity.slime.hurt hostile @a[distance=..24] ~ ~ ~ 0.8 0.6',
                    'particle minecraft:crit ~ ~1.5 ~ 0.5 0.5 0.5 0.2 8'])

    # ================================================================== THE HOARD (phase87 hands out shares from these)
    def ent(i, w, c=None):
        if i in ITEMS: return dict(G.loot_entry(i, G.uni(*c) if c else None), weight=w)
        e = {'type': 'minecraft:item', 'name': 'minecraft:' + i, 'weight': w}
        if c: e['functions'] = [{'function': 'minecraft:set_count', 'count': G.uni(*c)}]
        return e
    for t in R5.TIERS:
        wjson(f'bm/loot_table/p88/hoard_t{t}.json', {'pools': [
            {'rolls': 2 if t >= 4 else 1, 'entries': [ent(i, 1) for i in UNIQUES]},
            {'rolls': 2, 'entries': [ent('diamond', 10, (2, 2 + t)), ent('gold_block', 6, (1, 1 + t)), ent('emerald_block', 3, (1, 2)),
                                     ent('netherite_scrap', t - 1 if t > 1 else 1, (1, 1))]},
            {'rolls': 1, 'entries': [ent('gutter_medallion', 1, (1, 1 + t // 2))]}]})

    # ================================================================== THEIR TREASURES AT WORK
    fn('p88/item/echo', ['effect give @e[type=!minecraft:player,type=!minecraft:item_display,type=!minecraft:marker,type=!minecraft:interaction,distance=..32] minecraft:glowing 8 0 true',
                         'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:block.bell.use player @a[distance=..24] ~ ~ ~ 1 1.6',
                         'playsound minecraft:entity.bat.ambient player @a[distance=..24] ~ ~ ~ 1 0.6'])
    wjson('bm/advancement/p88/yolk.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {'player': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'head': {'predicates': {'minecraft:custom_data': '{bm:"yolkshell_helm"}'}}}}}]}}},
        'rewards': {'function': 'bm:p88/item/yolk'}})
    fn('p88/item/yolk', ['advancement revoke @s only bm:p88/yolk', 'execute if score @s bm.gnty matches 1.. run return 0', 'scoreboard players set @s bm.gnty 5',
                         'execute at @s run effect give @e[type=#bm:hostile,distance=..3.5] minecraft:slowness 3 2', 'execute at @s run effect give @e[type=#bm:hostile,distance=..3.5] minecraft:blindness 1 0',
                         'execute at @s run particle minecraft:squid_ink ~ ~1 ~ 1 0.6 1 0.05 30', 'execute at @s run playsound minecraft:block.honey_block.break player @a[distance=..12] ~ ~ ~ 1 0.6'])
    second.append('scoreboard players remove @a[scores={bm.gnty=1..}] bm.gnty 1')
    wjson('bm/advancement/p88/cane.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'equipment': {'mainhand': {'predicates': {'minecraft:custom_data': '{bm:"blob_cane"}'}}}}}]}}},
        'rewards': {'function': 'bm:p88/item/cane'}})
    fn('p88/item/cane', ['advancement revoke @s only bm:p88/cane',
                         'execute at @s as @e[type=!minecraft:player,distance=..6,nbt={HurtTime:10s}] run effect give @s minecraft:levitation 1 3 true',
                         'execute at @s run playsound minecraft:entity.slime.jump player @a[distance=..12] ~ ~ ~ 1 1.2'])
    second.append('execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"blob_top_hat"}] run effect give @s minecraft:luck 15 0 true')
    fn('admin/gentry_items', [G.give(i) for i in UNIQUES])
    fn('admin/gentry_here', ['scoreboard players set #gt bm.rng 3', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                             'summon minecraft:marker ~ ~ ~ {Tags:["bm.gvhvr","bm.gvhvr_lair","bm.gntadm"]}',
                             'scoreboard players operation @e[type=minecraft:marker,tag=bm.gntadm] bm.gvi = #gi bm.rng',
                             'execute as @e[type=minecraft:marker,tag=bm.gntadm] at @s run function bm:p88/lair/start', 'tag @e[tag=bm.gntadm] remove bm.gntadm'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']; f[-1:-1] = fast
    s = G.FUNCS['loop/second']; s[-1:-1] = second


def rp(R):
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('gnt_',)
    g = R.grid
    R.ICONS['echo_bell'] = g(['................', '.......kk.......', '......kppk......', '.....oYYYYo.....', '....oYwYYYYo....', '....oYwYYYYo....', '...oYYYYYYYYo...',
                              '...oYYYYYYYYo...', '..oYYYYYYYYYYo..', '..oooooooooooo..', '.......oo.......', '................', '................', '................',
                              '................', '................'], dict(k='#2c2c4c', p='#8a8ad8', o='#6a4a10', Y='#e8c040', w='#fff4c0'))
    R.ICONS['blob_cane'] = g(['................', '..........kkk...', '.........k...k..', '.........k...k..', '.........k......', '........k.......', '.......k........',
                              '......k.........', '.....k..........', '....k...........', '...k............', '..k.............', '.s..............', '................',
                              '................', '................'], dict(k='#141416', s='#c8ccd0'))
    # (The Count's Top Hat wears the Dapper Top Hat's model)
    def gilded_post(RR):
        RR.wj('assets/bm/items/gilded_grin.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                             'cases': [{'when': 'head', 'model': {'type': 'minecraft:model', 'model': 'bm:item/gilded_grin_worn'}}],
                                                             'fallback': {'type': 'minecraft:model', 'model': 'bm:item/gilded_grin'}}})
    R.POST.append(gilded_post)
