"""2.56: Celi - a rare, fierce follower from the snow.

- FINDING HER: in snowy biomes (plains, taiga, slopes, groves, peaks, ice spikes, frozen rivers and beaches) you may
  hear someone muttering impatiently. Celi is standing about 14 blocks away, hand on her hip, tapping her boot. Right-
  click her with a snowball and she decides you've got guts: she gives you her MOON CHARM. She waits 10 minutes.
- THE MOON CHARM: use it to call her (and call her back). Sneak + use: send her home.
- FIGHTING: an ice spear. Up close she thrusts (10 damage); at range (5-16 blocks) she throws it (8 damage, and it
  flies back to her). Every hit FREEZES: the monster is held in place for 3 seconds (frosted over, no running, no
  jumping). She picks her own fights - she doesn't wait for you.
- RECKLESS: only 30 health and no armour - she gets hurt far more than the others. If she faints: 5 minutes.
- She animates: hand on her hip tapping her foot (and rolling her eyes), a brisk stride, a lance-levelled run, a leap,
  sitting back on one hand (right-click her empty-handed, like any pet), the thrust and the throw."""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import phase66_art as ART

PET_CD = 300
HP = 30
ENC_ODDS = 40                   # per minute, per player in a snowy biome
SNOWY = ['minecraft:snowy_plains', 'minecraft:ice_spikes', 'minecraft:snowy_taiga', 'minecraft:snowy_slopes', 'minecraft:grove', 'minecraft:frozen_peaks',
         'minecraft:jagged_peaks', 'minecraft:frozen_river', 'minecraft:snowy_beach']
ICE = '#8ed8ff'
ORANGE = '#f0a23a'

item('celi_charm', TOTEM, "Celi's Moon Charm", ICE,
     ['A crescent moon on a dark blue stone. Cold to the touch.', ('Use: call Celi (or call her back).', 'blue'), ('Sneak + use: send her home.', 'blue'),
      ('She thrusts and throws an ice spear;', 'blue'), ('every hit freezes a monster in place.', 'blue'),
      ('Reckless: hits hard, but hurts easily.', 'gray'), ('If she faints: 5 minutes before she can return.', 'gray')],
     model='bm:celi_charm', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['celi_charm'] = 'bm:p66/use'


def extend_offers(O, offer):
    pass                         # (found, never sold)


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    cesay = lambda txt, who='@s': title(who, 'actionbar', [T('Celi: ', ICE, bold=True), T(txt, '#d8f0ff')])
    tick, fast, second = [], [], []
    objs = ['bm.ces', 'bm.cef', 'bm.cecd', 'bm.cek', 'bm.cea', 'bm.cem', 'bm.cet', 'bm.cez', 'bm.cer', 'bm.ceq', 'bm.cel', 'bm.ceph', 'bm.cefi']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    holds = '*[minecraft:custom_data~{bm:"celi_charm"}]'
    S = ART.RIG_SCALE
    U = S / 16
    foe = 'type=#bm:hostile,tag=!bm.npc'
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.celipet] if score @s bm.pid = #me bm.pid'
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]

    # ================================================================== the rig
    def part_nbt(p):
        return snbt({'Tags': ['bm.cep', f'bm.cp6_{p}', 'bm.cenew'],
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:ce_{p}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(8), 'start_interpolation': Int(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    rig = [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS]
    def place_lines():
        out = []
        for p in ART.PARTS:
            x, y, z = ART.joint(p)
            out.append(f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_{p}] ~ ~ ~ ~ 0')
        return out
    fn('p66/place', place_lines())
    fn('p66/grow', [f'execute as @e[type=minecraft:item_display,tag=bm.cesel] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}',
                    'execute at @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_body,limit=1] run function bm:p66/burst'])
    fn('p66/burst', ['particle minecraft:snowflake ~ ~0.9 ~ 0.4 0.7 0.4 0.03 50', 'particle minecraft:end_rod ~ ~0.9 ~ 0.1 0.3 0.1 0.1 18',
                     'particle minecraft:dust{color:[0.6,0.85,1.0],scale:1.4} ~ ~0.9 ~ 0.4 0.7 0.4 0 24',
                     'particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~0.9 ~ 0.3 0.6 0.3 0 20'])
    # the spear comes and goes (thrown, back)
    fn('p66/spear_off', [f'execute as @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_spear] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[0f,0f,0f]}}}}'])
    fn('p66/spear_on', [f'execute as @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_spear] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}'])

    # ---- poses
    DUR = {'idle': 3, 'tap': 2, 'huff': 8, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 3,
           'sit_a': 4, 'sit_b': 4, 'stab_back': 3, 'stab': 2, 'throw_back': 4, 'throw': 2}
    def xf_nbt(pose, p):
        rot, tr = ART.part_xf(pose, p)
        return f'left_rotation:{snbt(qf(rot))},translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f]'
    for name, pose in ART.POSES.items():
        fn(f'p66/pose/{name}', [f'execute as @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_{p}] run data merge entity @s '
                                f'{{start_interpolation:0,interpolation_duration:{DUR[name]},transformation:{{{xf_nbt(pose, p)}}}}}' for p in ART.PARTS])
    # states: 0 idle (tap, tap... huff), 1 walk, 2 run, 3 air, 4 sit, 7 stab, 8 throw
    CYCLE = {0: (80, [(0, 'idle'), (4, 'tap'), (8, 'idle'), (12, 'tap'), (16, 'idle'), (20, 'tap'), (24, 'idle'), (40, 'tap'), (44, 'idle'), (48, 'tap'),
                      (52, 'idle'), (60, 'huff'), (72, 'idle')]),
             1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]),
             3: (None, [(0, 'jump')]), 4: (16, [(0, 'sit_a'), (4, 'sit_b')]),
             7: (None, [(0, 'stab_back'), (3, 'stab')]), 8: (None, [(0, 'throw_back'), (6, 'throw')])}
    anim = []
    for st, (period, frames) in CYCLE.items():
        lines = ['scoreboard players operation #f bm.rng = @s bm.cef']
        if period: lines.append(f'scoreboard players operation #f bm.rng %= #{period} bm.rng')
        lines += [f'execute if score #f bm.rng matches {t} run function bm:p66/pose/{p}' for t, p in frames]
        fn(f'p66/anim/{st}', lines)
        anim.append(f'execute if score @s bm.ces matches {st} run return run function bm:p66/anim/{st}')
    fn('p66/anim', anim)
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in (12, 16, 80)]
    fn('p66/state', ['execute if score @s bm.cek matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.cea',
                     'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                     'execute store result score #og bm.rng run data get entity @s OnGround',
                     'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.cez 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.cez 0',
                     'execute if score @s bm.cez matches 3.. run return run scoreboard players set #st bm.rng 3',
                     'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                     'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                     'scoreboard players operation #vx bm.rng += #vz bm.rng',
                     'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                     'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                     'scoreboard players set #st bm.rng 0'])
    # every tick, each Celi: her parts, her state and frames, where she stands and faces, her fighting
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.celipet] at @s run function bm:p66/tick')
    fn('p66/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:item_display,tag=bm.cep,tag=!bm.cefade] if score @s bm.pid = #me bm.pid run tag @s add bm.cesel',
                    'execute unless entity @e[type=minecraft:item_display,tag=bm.cesel,tag=bm.cp6_spear] run function bm:p66/rerig',
                    'execute if score @s bm.cek matches 1.. run function bm:p66/act_tick',
                    'execute if score @s bm.cem matches 1.. run scoreboard players remove @s bm.cem 1',
                    'execute if score @s bm.cet matches 1.. run scoreboard players remove @s bm.cet 1',
                    'execute if score @s bm.cer matches 1.. run scoreboard players remove @s bm.cer 1',
                    'execute if score @s bm.cer matches 1 run function bm:p66/spear_on',
                    # her own fights: a thrust at anything within reach, a throw at anything 5-16 away
                    f'execute unless score @s bm.cek matches 1.. unless score @s bm.cem matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=..3.2] run function bm:p66/stab_go',
                    f'execute unless score @s bm.cek matches 1.. unless score @s bm.cet matches 1.. unless score @s bm.cer matches 1.. unless data entity @s {{Sitting:1b}} '
                    f'unless entity @e[{foe},distance=..3.2] if entity @e[{foe},distance=5..16] run function bm:p66/throw_go',
                    'function bm:p66/state',
                    'execute if score #st bm.rng = @s bm.ces run scoreboard players add @s bm.cef 1',
                    'execute unless score #st bm.rng = @s bm.ces run scoreboard players set @s bm.cef 0',
                    'scoreboard players operation @s bm.ces = #st bm.rng',
                    'function bm:p66/anim',
                    'execute on owner run tag @s add bm.ceown',
                    # fighting: she faces her foe; idle / sitting: you (she's waiting on YOU); moving: where she's going
                    f'execute if score @s bm.ces matches 7..8 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p66/place',
                    f'execute if score @s bm.ces matches 7..8 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p66/place',
                    'execute if score @s bm.ces matches 0 if entity @a[tag=bm.ceown,distance=1.5..10] facing entity @a[tag=bm.ceown,limit=1] feet rotated ~ 0 run function bm:p66/place',
                    'execute if score @s bm.ces matches 0 unless entity @a[tag=bm.ceown,distance=1.5..10] rotated as @s rotated ~ 0 run function bm:p66/place',
                    'execute if score @s bm.ces matches 1..4 rotated as @s rotated ~ 0 run function bm:p66/place',
                    'tag @a[tag=bm.ceown] remove bm.ceown', 'tag @e[tag=bm.cesel] remove bm.cesel'])

    # ---- the thrust (8 ticks; the blow lands on the 4th) and the throw (12 ticks; the spear leaves on the 7th)
    fn('p66/stab_go', ['scoreboard players set @s bm.cek 8', 'scoreboard players set @s bm.cea 7', 'scoreboard players set @s bm.cem 22'])
    fn('p66/throw_go', ['scoreboard players set @s bm.cek 12', 'scoreboard players set @s bm.cea 8', 'scoreboard players set @s bm.cet 90',
                        'playsound minecraft:item.trident.throw neutral @a[distance=..16] ~ ~ ~ 0.4 1.6'])
    fn('p66/act_tick', ['scoreboard players remove @s bm.cek 1',
                        'execute if score @s bm.cea matches 7 if score @s bm.cek matches 4 run function bm:p66/stab_hit',
                        'execute if score @s bm.cea matches 8 if score @s bm.cek matches 5 run function bm:p66/release'])
    fn('p66/stab_hit', ['tag @s add bm.ceme', 'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                        f'execute as @e[{foe},distance=..3.6,sort=nearest,limit=1] at @s run function bm:p66/stabbed',
                        'tag @s remove bm.ceme', 'scoreboard players add @s bm.ceq 1', 'execute if score @s bm.ceq matches 9.. run function bm:p66/quip'])
    fn('p66/stabbed', ['damage @s 10 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.ceme,limit=1]', 'function bm:p66/freeze',
                       'particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 10'])
    # FROZEN: held in place for three seconds
    fn('p66/freeze', ['effect give @s minecraft:slowness 3 9 true', 'effect give @s minecraft:jump_boost 3 128 true', 'effect give @s minecraft:weakness 3 0 true',
                      'data merge entity @s {TicksFrozen:240}', 'tag @s add bm.cefrz', 'scoreboard players set @s bm.cel 60',
                      'particle minecraft:snowflake ~ ~1 ~ 0.3 0.6 0.3 0.02 24', 'particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 0.3 0.6 0.3 0 18',
                      'playsound minecraft:block.glass.break neutral @a[distance=..16] ~ ~ ~ 0.5 1.6', 'playsound minecraft:block.powder_snow.place neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    tick.append('execute as @e[tag=bm.cefrz] at @s run function bm:p66/frozen')
    fn('p66/frozen', ['scoreboard players remove @s bm.cel 1', 'particle minecraft:snowflake ~ ~1 ~ 0.25 0.5 0.25 0 1',
                      'execute if score @s bm.cel matches ..0 run tag @s remove bm.cefrz'])
    # the throw: the spear flies at the nearest monster, homing a little; it hits (8 + freeze), sticks in a wall, or runs out, and is back in her hand
    flying = snbt({'Tags': ['bm.cesp', 'bm.cespn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:ce_spear'}},
                   'item_display': 'fixed', 'teleport_duration': Int(1),
                   'transformation': {'left_rotation': qf(ART.TIP_FWD), 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(S)] * 3}})
    fn('p66/release', ['function bm:p66/spear_off', 'scoreboard players set @s bm.cer 200',
                       f'execute facing entity @e[{foe},distance=..17,sort=nearest,limit=1] eyes positioned ^-0.3 ^1.5 ^0.6 run summon minecraft:item_display ~ ~ ~ {flying}',
                       f'execute as @e[type=minecraft:item_display,tag=bm.cespn] at @s facing entity @e[{foe},distance=..18,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',
                       'scoreboard players operation @e[type=minecraft:item_display,tag=bm.cespn] bm.pid = #me bm.pid',
                       'scoreboard players set @e[type=minecraft:item_display,tag=bm.cespn] bm.cel 30',
                       'tag @e[type=minecraft:item_display,tag=bm.cespn] remove bm.cespn',
                       'playsound minecraft:item.trident.riptide_1 neutral @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.cesp] at @s run function bm:p66/fly')
    fn('p66/fly', ['scoreboard players remove @s bm.cel 1', 'particle minecraft:snowflake ~ ~ ~ 0.05 0.05 0.05 0 2',
                   f'execute positioned ~ ~-0.6 ~ if entity @e[{foe},distance=..1.3] run return run function bm:p66/spear_hit',
                   'execute if score @s bm.cel matches ..0 run return run function bm:p66/spear_done',
                   f'execute if entity @e[{foe},distance=..18] facing entity @e[{foe},distance=..18,sort=nearest,limit=1] eyes positioned ^ ^ ^0.9 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p66/spear_done',
                   f'execute unless entity @e[{foe},distance=..18] positioned ^ ^ ^0.9 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p66/spear_done',
                   f'execute if entity @e[{foe},distance=..18] facing entity @e[{foe},distance=..18,sort=nearest,limit=1] eyes run tp @s ^ ^ ^0.9 ~ ~',
                   f'execute unless entity @e[{foe},distance=..18] run tp @s ^ ^ ^0.9'])
    fn('p66/spear_hit', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_pet} run tag @s add bm.ceme',
                         f'execute positioned ~ ~-0.6 ~ as @e[{foe},distance=..1.3,sort=nearest,limit=1] at @s run function bm:p66/speared',
                         'tag @e[tag=bm.ceme] remove bm.ceme', 'function bm:p66/spear_done'])
    fn('p66/speared', ['execute if entity @e[tag=bm.ceme] run damage @s 8 minecraft:mob_projectile by @e[tag=bm.ceme,limit=1]',
                       'execute unless entity @e[tag=bm.ceme] run damage @s 8 minecraft:mob_projectile',
                       'function bm:p66/freeze', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 12'])
    fn('p66/spear_done', ['particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~ ~ 0.2 0.2 0.2 0 12', 'particle minecraft:snowflake ~ ~ ~ 0.2 0.2 0.2 0.05 10',
                          'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run scoreboard players set @s bm.cer 8', 'kill @s'])
    QUIPS = ['Too slow!', 'Stay down.', 'Is that IT?', 'Ugh, finally.', 'Next!', 'Hmph. Pathetic.', 'Try to keep up!']
    fn('p66/quip', ['scoreboard players set @s bm.ceq 0', 'execute store result score #r bm.rng run random value 1..7'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..20] run ' + cesay(q) for i, q in enumerate(QUIPS)])

    # ================================================================== the charm: call, recall, send home
    pet = {'Tags': ['bm.celipet', 'bm.cenew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(HP),
           'CustomName': T('Celi', ICE, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(HP)}, {'id': 'minecraft:armor', 'base': D(0)}, {'id': 'minecraft:attack_damage', 'base': D(3)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.36)}, {'id': 'minecraft:follow_range', 'base': D(32)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p66/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                   f'{sel_pet} run tag @s add bm.cesel2',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.cesel2] if predicate bm:p20/sneaking run function bm:p66/dismiss',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.cesel2] unless predicate bm:p20/sneaking run function bm:p66/recall',
                   'execute unless entity @e[type=minecraft:wolf,tag=bm.cesel2] unless predicate bm:p20/sneaking run function bm:p66/try_summon',
                   'execute unless entity @e[type=minecraft:wolf,tag=bm.cesel2] if predicate bm:p20/sneaking run ' + say("Celi isn't with you. (Use the charm to call her.)"),
                   'tag @e[tag=bm.cesel2] remove bm.cesel2'])
    fn('p66/recall', ['tp @e[type=minecraft:wolf,tag=bm.cesel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.cesel2,limit=1] Sitting set value 0b',
                      'particle minecraft:snowflake ~ ~1 ~ 0.4 0.8 0.4 0.02 20', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                      cesay("I'm coming, I'm coming. Don't rush me.")])
    fn('p66/try_summon', ['execute if score @s bm.cecd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.cecd',
                          'execute if score @s bm.cecd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.cecd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                          'execute if score @s bm.cecd matches 1.. run return run ' + title('@s', 'actionbar', [T('Celi is still sulking about her bruises: about ', 'gray'),
                                                                                                             {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                          'execute unless function bm:p37/allowed run return run ' + say("Celi won't come here. (Not even she's that reckless.)"),
                          'function bm:p66/summon'])
    fn('p66/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p66/summon_here',
                      'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p66/summon_here',
                      'function bm:p66/summon_here'])
    fn('p66/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                           'data modify entity @e[type=minecraft:wolf,tag=bm.cenew,limit=1,sort=nearest] Owner set from entity @s UUID',
                           f'attribute @e[type=minecraft:wolf,tag=bm.cenew,limit=1,sort=nearest] minecraft:max_health base set {HP}',
                           f'data modify entity @e[type=minecraft:wolf,tag=bm.cenew,limit=1,sort=nearest] Health set value {HP}f',
                           'scoreboard players set @e[type=minecraft:wolf,tag=bm.cenew,limit=1,sort=nearest] bm.ces -1',
                           'execute rotated ~180 0 run function bm:p66/rig_here',
                           'scoreboard players operation @e[tag=bm.cenew,distance=..4] bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:item_display,tag=bm.cenew,distance=..4] run tag @s add bm.cesel', 'function bm:p66/grow',
                           'tag @e[tag=bm.cesel] remove bm.cesel', 'tag @e[tag=bm.cenew,distance=..4] remove bm.cenew',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 1 0.9',
                           'playsound minecraft:entity.player.hurt_freeze neutral @a[distance=..20] ~ ~ ~ 0.6 1.4',
                           cesay('Ugh, FINALLY. What took you so long?')])
    fn('p66/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.cenew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p66/rerig', ['kill @e[type=minecraft:item_display,tag=bm.cesel]', 'execute rotated as @s rotated ~ 0 run function bm:p66/rig_here',
                     'scoreboard players operation @e[type=minecraft:item_display,tag=bm.cenew,distance=..2] bm.pid = #me bm.pid',
                     'tag @e[type=minecraft:item_display,tag=bm.cenew,distance=..2] add bm.cesel', 'tag @e[type=minecraft:item_display,tag=bm.cenew,distance=..2] remove bm.cenew',
                     'function bm:p66/grow', 'scoreboard players set @s bm.ces -1', 'execute if score @s bm.cer matches 2.. run function bm:p66/spear_off'])
    fn('p66/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.cesel2] at @s run function bm:p66/fade',
                       'execute as @e[type=minecraft:wolf,tag=bm.cesel2] run data remove entity @s Owner',
                       'execute as @e[type=minecraft:wolf,tag=bm.cesel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.cesel2]',
                       cesay('Fine. Call me when something actually needs stabbing.')])

    # ---- fainting: the rig without its host (4 ticks running) melts into snow; the charm rests 5 minutes
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.cp6_body,tag=!bm.cefade,tag=!bm.ceencp] at @s run function bm:p66/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.cefade] bm.cel 1',
             'kill @e[type=minecraft:item_display,tag=bm.cefade,scores={bm.cel=..0}]']
    fn('p66/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{sel_pet.replace("tag=bm.celipet]", "tag=bm.celipet,distance=..16]")} run return run scoreboard players set @s bm.cez 0',
                     'scoreboard players add @s bm.cez 1', 'execute if score @s bm.cez matches 4.. run function bm:p66/fell'])
    fn('p66/fell', ['function bm:p66/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p66/cooldown'])
    fn('p66/cooldown', [f'scoreboard players set @s bm.cecd {PET_CD}',
                        tellraw('@s', PREFIX + [T('Celi faints. ', ICE, bold=True), T('"...Tch. Don\'t look at me like that." ', '#d8f0ff'),
                                                T(f'The charm needs {PET_CD // 60} minutes before she can come back.', 'gray')])])
    fn('p66/fade', ['execute as @e[type=minecraft:item_display,tag=bm.cep,tag=!bm.cefade] if score @s bm.pid = #me bm.pid run function bm:p66/fade1',
                    'execute as @e[type=minecraft:item_display,tag=bm.cesp] if score @s bm.pid = #me bm.pid run kill @s',
                    'particle minecraft:snowflake ~ ~1 ~ 0.5 1 0.5 0.04 70', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.3 0.1 0.15 30',
                    'particle minecraft:flash{color:[0.75,0.92,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:block{block_state:"minecraft:packed_ice"} ~ ~1 ~ 0.4 0.8 0.4 0 30',
                    'playsound minecraft:block.glass.break neutral @a[distance=..20] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'])
    fn('p66/fade1', ['tag @s add bm.cefade', 'scoreboard players set @s bm.cel 3',
                     'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:9361407}'])
    second.append('scoreboard players remove @a[scores={bm.cecd=1..}] bm.cecd 1')
    # (with her summoner gone, she goes too - like the others)
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.celipet] if score @s bm.pid = #me bm.pid at @s run function bm:p66/go')
    fn('p66/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p66/fade', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])

    # ================================================================== finding her: muttering in the snow
    wjson('bm/predicate/p66/snowy.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': SNOWY}})
    second += ['scoreboard players add #cet bm.bm 1', 'execute if score #cet bm.bm matches 60.. run function bm:p66/enc/check']
    fn('p66/enc/check', ['scoreboard players set #cet bm.bm 0',
                         'execute in minecraft:overworld as @a[distance=0..,gamemode=!spectator,predicate=bm:p66/snowy] at @s run function bm:p66/enc/roll'])
    fn('p66/enc/roll', [f'execute if items entity @s container.* {holds} run return 0', f'execute if items entity @s weapon.offhand {holds} run return 0',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.ceenc,distance=..128] run return 0',
                        'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                        f'execute store result score #r bm.rng run random value 1..{ENC_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                        'execute store result storage bm:tmp ceenc.a int 1 run random value 0..359', 'function bm:p66/enc/at with storage bm:tmp ceenc'])
    fn('p66/enc/at', ['$execute rotated $(a) 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p66/enc/place'])
    wjson('bm/tags/block/p66_ground.json', {'values': ['#minecraft:dirt', '#minecraft:grass_blocks', 'minecraft:snow_block', 'minecraft:snow', 'minecraft:powder_snow',
                                                       'minecraft:packed_ice', 'minecraft:ice', 'minecraft:blue_ice', 'minecraft:stone', 'minecraft:gravel', 'minecraft:sand']})
    fn('p66/enc/place', ['execute if block ~ ~ ~ minecraft:snow positioned ~ ~1 ~ run return run function bm:p66/enc/place2',
                         'function bm:p66/enc/place2'])
    fn('p66/enc/place2', ['execute unless block ~ ~-1 ~ #bm:p66_ground run return 0', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                          'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'function bm:p66/enc/spawn',
                          'execute as @a[distance=..40] run ' + title('@s', 'actionbar', T('Someone nearby is muttering... "Ugh. Where IS everyone?"', '#d8f0ff'))])
    enc_hit = snbt({'Tags': ['bm.ceenc', 'bm.cenew'], 'width': F(0.9), 'height': F(1.9), 'response': B(1)})
    fn('p66/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + rig +
       ['tag @e[type=minecraft:item_display,tag=bm.cenew,distance=..1] add bm.ceencp',
        'execute as @e[type=minecraft:item_display,tag=bm.cenew,distance=..1] run tag @s add bm.cesel',
        'execute store result storage bm:tmp ceenc.a int 1 run random value 0..359', 'function bm:p66/enc/turn with storage bm:tmp ceenc',
        'function bm:p66/grow', 'function bm:p66/pose/idle', 'tag @e[tag=bm.cesel] remove bm.cesel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.cenew,distance=..1] bm.cel 0',
        'tag @e[tag=bm.cenew,distance=..1] remove bm.cenew'])
    fn('p66/enc/turn', ['$execute rotated $(a) 0 run function bm:p66/place'])
    # she taps her foot (every tick, there's only ever one of her about); turns to watch anyone who comes close
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.ceenc] at @s run function bm:p66/enc/tick')
    fn('p66/enc/tick', ['scoreboard players add @s bm.cef 1', 'scoreboard players operation #f bm.rng = @s bm.cef', 'scoreboard players operation #f bm.rng %= #80 bm.rng',
                        'execute as @e[type=minecraft:item_display,tag=bm.ceencp,distance=..2] run tag @s add bm.cesel'] +
       [f'execute if score #f bm.rng matches {t} run function bm:p66/pose/{p}' for t, p in CYCLE[0][1]] +
       ['execute if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p66/place',
        'execute if score #f bm.rng matches 40 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p66/place',
        'execute if score #f bm.rng matches 60 run particle minecraft:snowflake ~ ~1.8 ~ 0.2 0.1 0.2 0 4',
        'tag @e[tag=bm.cesel] remove bm.cesel'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.ceenc] at @s run function bm:p66/enc/sec')
    fn('p66/enc/sec', ['scoreboard players add @s bm.cel 1', 'execute unless entity @a[distance=..80] run return run function bm:p66/enc/gone',
                       'execute if score @s bm.cel matches 600.. run return run function bm:p66/enc/gone'])
    fn('p66/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.ceencp,distance=..2]', 'particle minecraft:snowflake ~ ~1 ~ 0.5 1 0.5 0 40', 'kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.ceenc] if data entity @s interaction at @s run function bm:p66/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.ceenc] if data entity @s attack at @s run function bm:p66/enc/poke']
    fn('p66/enc/click', ['tag @s add bm.cehere', 'execute on target run function bm:p66/enc/talk', 'tag @s remove bm.cehere', 'data remove entity @s interaction'])
    fn('p66/enc/poke', ['execute on attacker run ' + cesay('HEY. Watch it - or you\'ll be wearing this spear.'),
                        'execute on attacker run playsound minecraft:entity.player.hurt_freeze neutral @s ~ ~ ~ 0.6 1.6', 'data remove entity @s attack'])
    fn('p66/enc/talk', ['execute if items entity @s weapon.mainhand minecraft:snowball run return run function bm:p66/enc/recruit',
                        f'execute if items entity @s container.* {holds} run return run ' + cesay('You have my charm. USE it. Honestly.'),
                        cesay("What? Can't you see I'm busy being bored? ...If you want something, bring a snowball and see if you've got the nerve."),
                        'playsound minecraft:entity.player.hurt_freeze neutral @s ~ ~ ~ 0.4 1.8'])
    fn('p66/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                           'execute as @e[type=minecraft:interaction,tag=bm.cehere,limit=1] at @s run particle minecraft:item_snowball ~ ~1.5 ~ 0.2 0.2 0.2 0.1 16',
                           tellraw('@s', [T('Celi: ', ICE, bold=True), T('"...Did you just— Ha! You\'ve got guts, I\'ll give you that."', '#d8f0ff')]),
                           tellraw('@s', [T('Celi: ', ICE, bold=True), T('"Fine. I\'m coming with you. Don\'t slow me down, and DON\'T get in the way of my spear."', '#d8f0ff')]),
                           tellraw('@s', PREFIX + [T('Celi joins you! ', ICE, bold=True), T('She tosses you her Moon Charm. Use it to call her; sneak + use to send her home.', 'gray')]),
                           give('celi_charm'), 'advancement grant @s only bm:story/celi_friend',
                           'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.2',
                           'execute as @e[type=minecraft:interaction,tag=bm.cehere,limit=1] at @s run function bm:p66/enc/gone',
                           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                           f'{sel_pet} run tag @s add bm.cesel2', 'execute unless entity @e[type=minecraft:wolf,tag=bm.cesel2] run function bm:p66/summon',
                           'tag @e[tag=bm.cesel2] remove bm.cesel2'])

    # ================================================================== achievement, admin
    wjson('bm/advancement/story/celi_friend.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:celi_charm'}},
                      'title': T('Cold Shoulder', 'yellow'), 'description': T('Win over Celi with a snowball', 'gray'),
                      'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    fn('admin/celi', ['execute rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves run function bm:p66/enc/spawn',
                      tellraw('@s', PREFIX + [T('Celi is standing in front of you. Right-click her holding a snowball.', 'gray')])])
    fn('admin/celi_charm', [give('celi_charm')])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.cep]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.ceenc]')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    import sys
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('ce_',)
    R.ICONS['celi_charm'] = ART.charm_icon(R)
