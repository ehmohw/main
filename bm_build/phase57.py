"""Phase 2.37: Emma - a hidden, recruitable support companion.

- FINDING HER: on a sunny day in a cherry grove, flower forest, meadow or sunflower plains, you may hear someone humming.
  Emma sits in the flowers nearby. Bring her a flower (any flower, in your hand) and she joins you - she gives you
  EMMA'S RIBBON. (Cecil drops a hint the first time he's summoned.) She stays 10 minutes or until you wander off.
- EMMA'S RIBBON: use it to call her (and call her back). Sneak + use: her menu - pick her buff, see her charge, send her home.
- SUPPORT: every 3 seconds she buffs you, other players within 10 blocks and Cecil: SPEED (Speed + Jump Boost),
  OFFENSE (Strength), DEFENSE (Resistance) or HEALING (Regeneration, and a quick heal for anyone below 4 hearts).
  She never fights in this form - monsters don't bother her.
- CHARGE: while monsters are near she charges (2% a second). At 100% she takes her ETHEREAL FORM for 30 seconds:
  steel armour, white wings and a crescent axe. She flies, strikes the nearest monster every second (8 damage, 4 to
  anything beside it) and her buffs grow a level stronger.
- WITH CECIL - HARMONY: summoned together (within 12 blocks) they help each other: Cecil casts every second instead of
  every 2 and his bolts hit for 7; Emma charges twice as fast and her buffs get a bonus. Now and then they stop to chat.
- She animates: arms folded politely when idle, a bouncy walk, a skipping run, a cheer when she jumps, swinging her
  feet when she sits (right-click her empty-handed to sit or stand, like any pet), and flies in her ethereal form.
- If she falls: 10 minutes before the ribbon can call her again."""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import phase57_art as ART

PET_CD = 600
ENC_ODDS = 20                   # per minute, per player in flowery biomes by day
FLOWERY = ['minecraft:cherry_grove', 'minecraft:flower_forest', 'minecraft:meadow', 'minecraft:sunflower_plains']
MODES = {1: ('Speed', '#5ad8f0'), 2: ('Offense', '#ff5a5a'), 3: ('Defense', '#9ab4ff'), 4: ('Healing', '#ff8ad0')}
PINK = '#ff7ad0'

item('emma_ribbon', TOTEM, "Emma's Ribbon", PINK,
     ['A pink ribbon, still smelling faintly of the sea.', ('Once worn by the princess of the drowned kingdom.', 'dark_gray'), ('Use: call Emma to your side (or back to you).', 'blue'),
      ('Sneak + use: her menu - buffs, charge, send her home.', 'blue'),
      ('She buffs you and your friends; charged up,', 'blue'), ('she takes her Ethereal Form and fights.', 'blue'),
      ('If she falls: 10 minutes before she can return.', 'gray')],
     model='bm:emma_ribbon', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['emma_ribbon'] = 'bm:p57/use'


def extend_offers(O, offer):
    pass                         # (hidden: never sold)


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import phase28 as P28
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    emsay = lambda txt: title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(txt, '#ffd0ec')])
    tick, fast, second = [], [], []
    objs = ['bm.emm', 'bm.emc', 'bm.eme', 'bm.ems', 'bm.emf', 'bm.emk', 'bm.emcd', 'bm.emh', 'bm.emz', 'bm.emi', 'bm.emq', 'bm.emw', 'bm.emt', 'bm.emph', 'bm.emfi']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard players set #{n} bm.rng {n}' for n in (12, 16, 60, 80, 240)]
    G.OBJECTIVES += objs
    holds = '*[minecraft:custom_data~{bm:"emma_ribbon"}]'
    S = ART.RIG_SCALE
    U = S / 16                                                       # blocks per design unit
    foe = 'type=#bm:hostile,tag=!bm.npc'
    sel_pet = 'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid'
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]

    # ================================================================== the rig: eight display parts at their joints
    def part_nbt(p, extra_tags=()):
        model = f'bm:ee_{p}' if p.startswith('wing') else f'bm:em_{p}'
        return snbt({'Tags': ['bm.emp', f'bm.ep_{p}', 'bm.emnew'] + list(extra_tags),
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                     'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(10), 'start_interpolation': Int(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    rig = [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS]
    JOINT = {p: ART.PIVOT[p] for p in ART.PARTS}
    def place_lines(lift=0.0):
        out = []
        for p in ART.PARTS:
            x, y, z = JOINT[p]
            # design +x is her right = ^-x; design -z is her front = ^+z
            out.append(f'execute positioned ^{-x * U:.4f} ^{y * U + lift:.4f} ^{-z * U:.4f} run tp @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{p}] ~ ~ ~ ~ 0')
        return out
    fn('p57/place', place_lines())
    fn('p57/place_fly', place_lines(1.0))
    # (2.49) she appears whole in a burst of petals (wings stay folded away until she ascends)
    fn('p57/grow', [f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=!bm.ep_wingr,tag=!bm.ep_wingl,tag=!bm.ep_wingro,tag=!bm.ep_winglo] run data merge entity @s '
                    f'{{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}',
                    'execute at @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_body,limit=1] run function bm:p57/burst'])
    fn('p57/burst', ['particle minecraft:cherry_leaves ~ ~0.8 ~ 0.4 0.7 0.4 0.02 40', 'particle minecraft:end_rod ~ ~0.8 ~ 0.1 0.3 0.1 0.12 25',
                     'particle minecraft:dust{color:[1.0,0.55,0.85],scale:1.4} ~ ~0.8 ~ 0.4 0.7 0.4 0 20'])

    # ---- poses (left_rotation + a shared lift) - see phase57_art.POSES
    DUR = {'idle_a': 20, 'idle_b': 20, 'idle_hop': 4, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 3,
           'sit_a': 15, 'sit_b': 15, 'cast': 4, 'wave_a': 6, 'wave_b': 6, 'strike_up': 3, 'strike_dn': 3}
    DUR.update({f'fly_{i}': 3 for i in range(ART.FLY_FRAMES)})
    DUR.update({f'hover_{i}': 3 for i in range(ART.HOVER_FRAMES)})
    DUR.update({f'loco_{b}_{f}': ART.LOCO_STEP[b][1] for b in ART.LOCO_STEP for f in range(4)})
    def xf_nbt(pose, p):
        rot, tr = ART.part_xf(pose, p)
        return f'left_rotation:{snbt(qf(rot))},translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f]'
    for name, pose in ART.POSES.items():
        d = DUR[name]
        fn(f'p57/pose/{name}', [f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{p}] run data merge entity @s '
                                f'{{start_interpolation:0,interpolation_duration:{d},transformation:{{{xf_nbt(pose, p)}}}}}'
                                for p in ART.PARTS])

    # ---- the animation driver: state 0 idle, 1 walk, 2 run, 3 air, 4 sit, 5 fly, 6 cast, 7 strike, 8 wave
    CYCLE = {0: (240, [(0, 'idle_a'), (40, 'idle_b'), (80, 'idle_a'), (120, 'idle_hop'), (124, 'idle_b'), (160, 'idle_a'), (200, 'idle_b')]),
             3: (None, [(0, 'jump')]), 4: (60, [(0, 'sit_a'), (30, 'sit_b')]),
             5: (3 * ART.FLY_FRAMES, [(3 * i, f'fly_{i}') for i in range(ART.FLY_FRAMES)]),
             6: (None, [(0, 'cast')]), 7: (None, [(0, 'strike_up'), (3, 'strike_dn')]), 8: (12, [(0, 'wave_a'), (6, 'wave_b')]),
             9: (3 * ART.HOVER_FRAMES, [(3 * i, f'hover_{i}') for i in range(ART.HOVER_FRAMES)])}
    anim = []
    for st, (period, frames) in CYCLE.items():
        lines = []
        if period: lines += ['scoreboard players operation #f bm.rng = @s bm.emf', f'scoreboard players operation #f bm.rng %= #{period} bm.rng']
        else: lines += ['scoreboard players operation #f bm.rng = @s bm.emf']
        lines += [f'execute if score #f bm.rng matches {t} run function bm:p57/pose/{p}' for t, p in frames]
        fn(f'p57/anim/{st}', lines)
        anim.append(f'execute if score @s bm.ems matches {st} run return run function bm:p57/anim/{st}')
    # 1 = on the move: one walk/run cycle whose pose blends with her speed, stepping as fast as she actually moves
    loco = ['scoreboard players set #b bm.rng 8']
    for b in range(7, 0, -1):
        loco.append(f'execute if score #vx bm.rng matches ..{ART.LOCO[b - 1][0] - 1} run scoreboard players set #b bm.rng {b}')
    loco += ['execute if score @s bm.emf matches 0 run scoreboard players set @s bm.emph 1000']
    loco += [f'execute if score #b bm.rng matches {b} run scoreboard players add @s bm.emph {ART.LOCO_STEP[b][0]}' for b in ART.LOCO_STEP]
    loco += ['execute if score @s bm.emph matches 1000.. run function bm:p57/loco_step']
    fn('p57/anim/1', loco)
    fn('p57/loco_step', ['scoreboard players remove @s bm.emph 1000', 'scoreboard players add @s bm.emfi 1', 'scoreboard players operation @s bm.emfi %= #4 bm.rng'] +
       [f'execute if score #b bm.rng matches {b} if score @s bm.emfi matches {f} run return run function bm:p57/pose/loco_{b}_{f}' for b in ART.LOCO_STEP for f in range(4)])
    anim.insert(0, 'execute if score @s bm.ems matches 1 run return run function bm:p57/anim/1')
    fn('p57/anim', anim)
    # (as the host) what she's doing now -> #st
    fn('p57/state', ['execute if score @s bm.eme matches 1.. if score @s bm.emk matches 1.. run return run scoreboard players set #st bm.rng 7',
                     'execute if score @s bm.eme matches 1.. run return run function bm:p57/state_eth',
                     'execute if score @s bm.emw matches 1.. run return run scoreboard players set #st bm.rng 8',
                     'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                     'execute store result score #og bm.rng run data get entity @s OnGround',
                     'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.emz 1',
                     'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.emz 0',
                     'execute if score @s bm.emz matches 3.. run return run scoreboard players set #st bm.rng 3',
                     'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000',
                     'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                     'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                     'scoreboard players operation #vx bm.rng += #vz bm.rng',
                     'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                     'execute if score @s bm.emk matches 1.. run return run scoreboard players set #st bm.rng 6',
                     'scoreboard players set #st bm.rng 0'])
    fn('p57/state_eth', ['scoreboard players set #st bm.rng 9',
                         'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                         'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                         'scoreboard players operation #vx bm.rng += #vz bm.rng',
                         'execute if score #vx bm.rng matches 900.. run scoreboard players set #st bm.rng 5'])
    # every tick, for each Emma: find her parts, pick the state, play its frames, stand the parts at the joints
    tick.append('execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p57/tick')
    fn('p57/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel',
                    'execute if score @s bm.emk matches 1.. run scoreboard players remove @s bm.emk 1',
                    'execute if score @s bm.emw matches 1.. run scoreboard players remove @s bm.emw 1',
                    'execute unless entity @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_wingro] run function bm:p57/rerig',
                    'function bm:p57/state',
                    'execute if score #st bm.rng = @s bm.ems run scoreboard players add @s bm.emf 1',
                    'execute unless score #st bm.rng = @s bm.ems run scoreboard players set @s bm.emf 0',
                    'scoreboard players operation @s bm.ems = #st bm.rng',
                    'function bm:p57/anim',
                    'execute on owner run tag @s add bm.emown',
                    # idle / sitting / cheering: she turns to face you; waving: she faces Cecil; flying: she turns with her host
                    'execute if score @s bm.ems matches 8 as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..12] if score @s bm.pid = #me bm.pid run tag @s add bm.emcec',
                    'execute if score @s bm.ems matches 8 if entity @e[type=minecraft:wolf,tag=bm.emcec] facing entity @e[type=minecraft:wolf,tag=bm.emcec,limit=1] feet rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 8 unless entity @e[type=minecraft:wolf,tag=bm.emcec] rotated as @s rotated ~ 0 run function bm:p57/place',
                    'tag @e[type=minecraft:wolf,tag=bm.emcec] remove bm.emcec',
                    'execute if score @s bm.ems matches 0 if entity @a[tag=bm.emown,distance=1.5..10] facing entity @a[tag=bm.emown,limit=1] feet rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 4 if entity @a[tag=bm.emown,distance=1.5..10] facing entity @a[tag=bm.emown,limit=1] feet rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 6 if entity @a[tag=bm.emown,distance=1.5..10] facing entity @a[tag=bm.emown,limit=1] feet rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 0 unless entity @a[tag=bm.emown,distance=1.5..10] rotated as @s rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 4 unless entity @a[tag=bm.emown,distance=1.5..10] rotated as @s rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 6 unless entity @a[tag=bm.emown,distance=1.5..10] rotated as @s rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 1..3 rotated as @s rotated ~ 0 run function bm:p57/place',
                    'execute if score @s bm.ems matches 5 rotated as @s rotated ~ 0 run function bm:p57/place_fly',
                    'execute if score @s bm.ems matches 9 if entity @a[tag=bm.emown,distance=1.5..12] facing entity @a[tag=bm.emown,limit=1] feet rotated ~ 0 run function bm:p57/place_fly',
                    'execute if score @s bm.ems matches 9 unless entity @a[tag=bm.emown,distance=1.5..12] rotated as @s rotated ~ 0 run function bm:p57/place_fly',
                    'execute if score @s bm.ems matches 7 if entity @e[type=minecraft:marker,tag=bm.emaim,distance=..20] facing entity @e[type=minecraft:marker,tag=bm.emaim,distance=..20,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p57/place_fly',
                    'execute if score @s bm.ems matches 7 unless entity @e[type=minecraft:marker,tag=bm.emaim,distance=..20] rotated as @s rotated ~ 0 run function bm:p57/place_fly',
                    'execute if score @s bm.eme matches 1.. run particle minecraft:end_rod ~ ~2.2 ~ 0.4 0.4 0.4 0.01 1',
                    'tag @a[tag=bm.emown] remove bm.emown', 'tag @e[tag=bm.emsel] remove bm.emsel'])

    # ================================================================== the ribbon: summon, recall, menu
    pet = {'Tags': ['bm.emmapet', 'bm.emnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(60),
           'CustomName': T('Emma', PINK, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(60)}, {'id': 'minecraft:armor', 'base': D(20)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.34)}, {'id': 'minecraft:follow_range', 'base': D(32)},
                          {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p57/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                   f'{sel_pet} run tag @s add bm.emsel2',
                   'execute if entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking run function bm:p57/menu',
                   'execute if entity @e[type=minecraft:cat,tag=bm.emsel2] unless predicate bm:p20/sneaking run function bm:p57/recall',
                   'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] unless predicate bm:p20/sneaking run function bm:p57/try_summon',
                   'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] if predicate bm:p20/sneaking run ' + say("Emma isn't with you. (Use the ribbon to call her.)"),
                   'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    fn('p57/recall', ['tp @e[type=minecraft:cat,tag=bm.emsel2,limit=1] @s', 'data modify entity @e[type=minecraft:cat,tag=bm.emsel2,limit=1] Sitting set value 0b',
                      'particle minecraft:cherry_leaves ~ ~1 ~ 0.4 0.8 0.4 0 20', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 1.6',
                      emsay('Coming! Wait for me~!')])
    fn('p57/try_summon', ['execute if score @s bm.emcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.emcd',
                          'execute if score @s bm.emcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                          'execute if score @s bm.emcd matches 1.. run scoreboard players add #m bm.rng 1',
                          'execute if score @s bm.emcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Emma is still resting: about ', 'gray'),
                                                                                                             {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                          'execute unless function bm:p37/allowed run return run ' + say("Emma won't come here - it's too scary."),
                          'function bm:p57/summon'])
    fn('p57/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p57/summon_here',
                      'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p57/summon_here',
                      'function bm:p57/summon_here'])
    fn('p57/summon_here', [f'summon minecraft:cat ~ ~ ~ {snbt(pet)}',
                           'data modify entity @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                           'attribute @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] minecraft:max_health base set 60',
                           'data modify entity @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] Health set value 60f',
                           'scoreboard players set @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.emm 4',
                           'scoreboard players set @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.emc 0',
                           'scoreboard players set @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.eme 0',
                           'scoreboard players set @e[type=minecraft:cat,tag=bm.emnew,limit=1,sort=nearest] bm.ems -1',
                           'execute rotated ~180 0 run function bm:p57/rig_here',
                           'scoreboard players operation @e[tag=bm.emnew,distance=..4] bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:item_display,tag=bm.emnew,distance=..4] run tag @s add bm.emsel', 'function bm:p57/grow',
                           'tag @e[tag=bm.emsel] remove bm.emsel', 'tag @e[tag=bm.emnew,distance=..4] remove bm.emnew',
                           'particle minecraft:cherry_leaves ~ ~1 ~ 0.5 1 0.5 0 40', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.8 0.4 0.05 16',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 1 1.4',
                           'playsound minecraft:entity.allay.ambient_without_item neutral @a[distance=..20] ~ ~ ~ 1 1.2',
                           emsay("I'm here! Let's do our best today!")])
    fn('p57/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.emnew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p57/rerig', ['kill @e[type=minecraft:item_display,tag=bm.emsel]', 'execute rotated as @s rotated ~ 0 run function bm:p57/rig_here',
                     'scoreboard players operation @e[type=minecraft:item_display,tag=bm.emnew,distance=..2] bm.pid = #me bm.pid',
                     'tag @e[type=minecraft:item_display,tag=bm.emnew,distance=..2] add bm.emsel', 'tag @e[type=minecraft:item_display,tag=bm.emnew,distance=..2] remove bm.emnew',
                     'function bm:p57/grow', 'scoreboard players set @s bm.ems -1', 'execute if score @s bm.eme matches 1.. run function bm:p57/ethereal_look'])

    # ---- the menu (sneak + use): a dialog with her charge and mode
    MENU = 960
    P28.MENU['emma'] = MENU
    btn = lambda m: P28.btn(T(MODES[m][0], MODES[m][1], bold=True), 7300 + m, tooltip=T({1: 'Speed + Jump Boost', 2: 'Strength', 3: 'Resistance',
                                                                                         4: 'Regeneration + quick heals'}[m], 'gray'), width=120)
    dlg = P28.multi([T("Emma's Ribbon", PINK, bold=True)],
                    [P28.body([T('Buff: ', 'gray'), T('$(mode)', 'white', bold=True), T('     Charge: ', 'gray'), T('$(c)%', '#e0b0ff', bold=True)]),
                     P28.body([T('Pick what she focuses on. Charged to 100% with monsters near, she takes her Ethereal Form.', 'gray')])],
                    [btn(1), btn(2), btn(3), btn(4), P28.btn(T('Send her home', 'gray'), 7305, width=120)], columns=2, exit_label='Close')
    fn('p57/menu', ['execute store result storage bm:tmp em.c int 1 run scoreboard players get @e[type=minecraft:cat,tag=bm.emsel2,limit=1] bm.emc'] +
       [f'execute if score @e[type=minecraft:cat,tag=bm.emsel2,limit=1] bm.emm matches {m} run data modify storage bm:tmp em.mode set value "{MODES[m][0]}"' for m in MODES] +
       [f'scoreboard players set @s bm.menu {MENU}', 'function bm:p57/menu_show with storage bm:tmp em'])
    fn('p57/menu_show', [f'$dialog show @s {snbt(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7301..7305 run return run function bm:p57/act')
    fn('p57/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                   f'execute unless items entity @s container.* {holds} unless items entity @s weapon.offhand {holds} run return run function bm:p28/stale',
                   'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.emsel2',
                   'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] run return run function bm:p28/stale',
                   'execute if score #act bm.pay matches 7305 run function bm:p57/dismiss',
                   'execute if score #act bm.pay matches 7301..7304 run function bm:p57/set_mode',
                   'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    LINES = {1: 'Speed it is! Let\'s go-go-go!', 2: 'Offense! You can do it - smash them!', 3: 'Defense! I\'ll keep you safe!', 4: 'Healing! Tell me if it hurts, okay?'}
    fn('p57/set_mode', ['scoreboard players operation @e[type=minecraft:cat,tag=bm.emsel2] bm.emm = #act bm.pay',
                        'scoreboard players remove @e[type=minecraft:cat,tag=bm.emsel2] bm.emm 7300',
                        'scoreboard players set @e[type=minecraft:cat,tag=bm.emsel2] bm.emk 8'] +
       [f'execute if score #act bm.pay matches {7300 + m} run ' + emsay(LINES[m]) for m in MODES] +
       ['playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.8 1.6'])
    fn('p57/dismiss', ['execute as @e[type=minecraft:cat,tag=bm.emsel2] at @s run function bm:p57/fade',
                       'execute as @e[type=minecraft:cat,tag=bm.emsel2] run data remove entity @s Owner',
                       'execute as @e[type=minecraft:cat,tag=bm.emsel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:cat,tag=bm.emsel2]',
                       emsay('Bye-bye! Call me if you need me~')])

    # ---- falling: the rig without its host (4 ticks running) fades; the ribbon rests
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.ep_body,tag=!bm.emfade,tag=!bm.emencp] at @s run function bm:p57/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.emfade] bm.emt 1',
             'kill @e[type=minecraft:item_display,tag=bm.emfade,scores={bm.emt=..0}]']
    fn('p57/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{sel_pet.replace("tag=bm.emmapet]", "tag=bm.emmapet,distance=..16]")} run return run scoreboard players set @s bm.emz 0',
                     'scoreboard players add @s bm.emz 1', 'execute if score @s bm.emz matches 4.. run function bm:p57/fell'])
    fn('p57/fell', ['function bm:p57/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p57/cooldown'])
    fn('p57/cooldown', [f'scoreboard players set @s bm.emcd {PET_CD}',
                        tellraw('@s', PREFIX + [T('Emma has fallen. ', PINK, bold=True),
                                                T(f'She fades into petals; the ribbon needs {PET_CD // 60} minutes before she can come back.', 'gray')])])
    fn('p57/fade', ['kill @e[type=minecraft:marker,tag=bm.emaim,distance=..24]', 'execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run function bm:p57/fade1',
                    'particle minecraft:cherry_leaves ~ ~1 ~ 0.5 1 0.5 0.02 70', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.3 0.1 0.18 45',
                    'particle minecraft:flash{color:[1.0,0.8,0.95,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:dust{color:[1.0,0.55,0.85],scale:1.6} ~ ~1 ~ 0.5 0.9 0.5 0 30',
                    'particle minecraft:totem_of_undying ~ ~1 ~ 0.2 0.4 0.2 0.4 25',
                    'playsound minecraft:block.amethyst_block.break neutral @a[distance=..20] ~ ~ ~ 1 1.4', 'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 0.8 1.6'])
    # (2.49: no more shrinking - she flares bright for a moment and is gone in a burst of petals and light)
    fn('p57/fade1', ['tag @s add bm.emfade', 'scoreboard players set @s bm.emt 3',
                     'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:16767221}'])
    second.append('scoreboard players remove @a[scores={bm.emcd=1..}] bm.emcd 1')

    # ================================================================== every second: harmony, charge, buffs, the ethereal form
    second += ['tag @e[type=minecraft:wolf,tag=bm.harmony] remove bm.harmony',
               'execute as @e[type=minecraft:cat,tag=bm.emmapet] at @s run function bm:p57/sec']
    fn('p57/sec', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s remove bm.harmony',
                   'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..12] if score @s bm.pid = #me bm.pid run tag @s add bm.emmine',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.emmine] run tag @s add bm.harmony',
                   'tag @e[type=minecraft:wolf,tag=bm.emmine] add bm.harmony',
                   'execute if entity @s[tag=bm.harmony] run function bm:p57/harmony',
                   'tag @e[type=minecraft:wolf,tag=bm.emmine] remove bm.emmine',
                   # charge while monsters are about
                   f'execute if score @s bm.eme matches 0 if entity @e[{foe},distance=..16] run scoreboard players add @s bm.emc 2',
                   f'execute if score @s bm.eme matches 0 if entity @s[tag=bm.harmony] if entity @e[{foe},distance=..16] run scoreboard players add @s bm.emc 2',
                   'execute if score @s bm.emc matches 101.. run scoreboard players set @s bm.emc 100',
                   'execute if score @s bm.emc matches 50..99 run particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.5 0.3 0.01 1',
                   'execute if score @s bm.emc matches 100 run particle minecraft:end_rod ~ ~1.4 ~ 0.4 0.6 0.4 0.02 3',
                   f'execute if score @s bm.eme matches 0 if score @s bm.emc matches 100 if entity @e[{foe},distance=..14] run function bm:p57/ascend',
                   'execute if score @s bm.eme matches 1.. run function bm:p57/ethereal',
                   'scoreboard players add @s bm.emq 1', 'execute if score @s bm.emq matches 3.. run function bm:p57/pulse'])

    # ---- buffs: every 3 seconds, to players within 10 and Cecil. level: +1 harmony, +2 ethereal
    def effects(m, lvl):
        h, e = lvl & 1, lvl >> 1
        if m == 1: return [('speed', h + e), ('jump_boost', e)]
        if m == 2: return [('strength', e)] + ([('haste', 1)] if h else [])
        if m == 3: return [('resistance', min(1, h + e))] + ([('absorption', 0)] if e else [])
        return [('regeneration', min(1, h + e))]
    COL = {1: '[0.35,0.85,0.95]', 2: '[1.0,0.35,0.35]', 3: '[0.6,0.7,1.0]', 4: '[1.0,0.55,0.85]'}
    for m in MODES:
        for lvl in range(4):
            fn(f'p57/buff/{m}_{lvl}', [f'effect give @s minecraft:{e} 5 {a} true' for e, a in effects(m, lvl)] +
               [f'particle minecraft:dust{{color:{COL[m]},scale:1.1}} ~ ~1 ~ 0.35 0.5 0.35 0 6'])
    pulse = ['scoreboard players set @s bm.emq 0', 'scoreboard players set #lvl bm.rng 0',
             'execute if entity @s[tag=bm.harmony] run scoreboard players add #lvl bm.rng 1', 'execute if score @s bm.eme matches 1.. run scoreboard players add #lvl bm.rng 2',
             'scoreboard players operation #mode bm.rng = @s bm.emm', 'tag @s add bm.emme']
    for m in MODES:
        for lvl in range(4):
            pulse.append(f'execute if score #mode bm.rng matches {m} if score #lvl bm.rng matches {lvl} as @a[distance=..10,gamemode=!spectator] at @s run function bm:p57/buff/{m}_{lvl}')
            pulse.append(f'execute if score #mode bm.rng matches {m} if score #lvl bm.rng matches {lvl} as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..10] at @s run function bm:p57/buff/{m}_{lvl}')
    pulse += ['execute if score #mode bm.rng matches 4 run scoreboard players remove @s bm.emh 3',
              'execute if score #mode bm.rng matches 4 if score @s bm.emh matches ..0 as @a[distance=..10,gamemode=!spectator] at @s run function bm:p57/quickheal',
              'tag @s remove bm.emme',
              'execute unless score @s bm.ems matches 1..3 unless score @s bm.eme matches 1.. run scoreboard players set @s bm.emk 6',
              'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..12] ~ ~ ~ 0.4 1.8']
    fn('p57/pulse', pulse)
    fn('p57/quickheal', ['execute store result score #h bm.rng run data get entity @s Health', 'execute unless score #h bm.rng matches ..7 run return 0',
                         'effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 5',
                         'playsound minecraft:entity.allay.item_given player @s ~ ~ ~ 1 1.4',
                         'scoreboard players set @e[type=minecraft:cat,tag=bm.emme,limit=1] bm.emh 6'])

    # ---- the ethereal form
    def swap(form):
        return [f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{p}] run data modify entity @s item.components."minecraft:item_model" set value "bm:{form}_{p}"'
                for p in ('body', 'head', 'armr', 'arml', 'legr', 'legl')]
    fn('p57/ascend', ['scoreboard players set @s bm.eme 30', 'scoreboard players set @s bm.emc 0',
                      'execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel'] + swap('ee') +
       ['execute as @e[type=minecraft:item_display,tag=bm.emsel] run data merge entity @s {brightness:{block:15,sky:15},interpolation_duration:10}',
        *[f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{w}] run data merge entity @s {{start_interpolation:0,interpolation_duration:12,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}'
          for w in ('wingr', 'wingl', 'wingro', 'winglo')],
        'tag @e[tag=bm.emsel] remove bm.emsel',
        'effect give @s minecraft:resistance 31 3 true', 'data modify entity @s Sitting set value 0b',
        'particle minecraft:flash{color:[1.0,0.85,1.0,1.0]} ~ ~1.5 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~1.5 ~ 0.6 1 0.6 0.15 60',
        'particle minecraft:cherry_leaves ~ ~1.5 ~ 1 1 1 0 60',
        'playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1 1.4', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..32] ~ ~ ~ 1 0.8',
        'execute on owner run function bm:p57/ascend_owner'])
    fn('p57/ethereal_look', swap('ee') + ['execute as @e[type=minecraft:item_display,tag=bm.emsel] run data merge entity @s {brightness:{block:15,sky:15},interpolation_duration:10}'] +
       [f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{w}] run data merge entity @s {{start_interpolation:0,interpolation_duration:12,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}'
        for w in ('wingr', 'wingl', 'wingro', 'winglo')])
    fn('p57/ascend_owner', ['title @s times 5 40 10', title('@s', 'actionbar', [T('✦ ', PINK), T("Emma's Ethereal Form", '#e0b0ff', bold=True), T(' ✦', PINK)]),
                            'advancement grant @s only bm:story/emma_ethereal'])
    fn('p57/ethereal', ['scoreboard players remove @s bm.eme 1', 'execute if score @s bm.eme matches 0 run return run function bm:p57/descend',
                        f'execute if entity @e[{foe},distance=..14] run function bm:p57/strike'])
    fn('p57/descend', ['execute as @e[type=minecraft:item_display,tag=bm.emp,tag=!bm.emfade] if score @s bm.pid = #me bm.pid run tag @s add bm.emsel'] + swap('em') +
       ['execute as @e[type=minecraft:item_display,tag=bm.emsel] run data remove entity @s brightness',
        *[f'execute as @e[type=minecraft:item_display,tag=bm.emsel,tag=bm.ep_{w}] run data merge entity @s {{start_interpolation:0,interpolation_duration:12,transformation:{{scale:[0f,0f,0f]}}}}'
          for w in ('wingr', 'wingl', 'wingro', 'winglo')],
        'tag @e[tag=bm.emsel] remove bm.emsel', 'scoreboard players set @s bm.emc 0', 'kill @e[type=minecraft:marker,tag=bm.emaim,distance=..24]',
        'particle minecraft:cherry_leaves ~ ~1.5 ~ 0.6 1 0.6 0 40', 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..24] ~ ~ ~ 0.8 1.4',
        'execute on owner run ' + emsay('Phew... that was a lot! I need to recharge~')])
    # a crescent strike at the nearest monster: 8 to it, 4 to anything beside it
    fn('p57/strike', ['scoreboard players set @s bm.emk 6', 'tag @s add bm.emme', 'kill @e[type=minecraft:marker,tag=bm.emaim,distance=..24]',
                      f'execute as @e[{foe},distance=..14,sort=nearest,limit=1] at @s run function bm:p57/strike_at',
                      'tag @s remove bm.emme', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 1.3',
                      'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..20] ~ ~ ~ 1 0.7'])
    fn('p57/strike_at', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.emaim"]}', 'tag @s add bm.emtgt',
                         'damage @s 8 minecraft:magic by @e[type=minecraft:cat,tag=bm.emme,limit=1]',
                         f'execute as @e[{foe},distance=..3,tag=!bm.emtgt] run damage @s 4 minecraft:magic by @e[type=minecraft:cat,tag=bm.emme,limit=1]',
                         'tag @s remove bm.emtgt',
                         'particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.3 0.6 0 3', 'particle minecraft:dust{color:[0.7,0.9,1.0],scale:1.6} ~ ~1 ~ 1.2 0.4 1.2 0 24',
                         'particle minecraft:cherry_leaves ~ ~1 ~ 1 0.5 1 0 12',
                         'execute facing entity @e[type=minecraft:cat,tag=bm.emme,limit=1] feet run function bm:p57/crescent'])
    fn('p57/crescent', [f'particle minecraft:dust{{color:[0.85,0.95,1.0],scale:1.2}} ^ ^{1.0 + 0.06 * i:.2f} ^{0.6 * i:.1f} 0 0 0 0 1' for i in range(1, 24)])

    # ================================================================== Emma + Cecil: harmony
    def bolt_patch():
        b = G.FUNCS['p46/pet/bolt']
        k = next(i for i, l in enumerate(b) if l.startswith('damage @s 5 minecraft:magic'))
        b[k:k + 1] = ['execute if entity @e[type=minecraft:wolf,tag=bm.cpme,tag=bm.harmony] run damage @s 7 minecraft:magic by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]',
                      'execute unless entity @e[type=minecraft:wolf,tag=bm.cpme,tag=bm.harmony] run damage @s 5 minecraft:magic by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]']
        a = G.FUNCS['p46/pet/act']
        k = next(i for i, l in enumerate(a) if 'bm.cpa matches 2..' in l)
        a.insert(k, a[k].replace('if score @s bm.cpa matches 2..', 'if entity @s[tag=bm.harmony] if score @s bm.cpa matches 1'))
    bolt_patch()
    CHATS = [('Hi Cecil! *waves*', 'Hehehe... hello, little one.'),
             ('This flower is for you!', '...Thank you. Tell no one.'),
             ("I'll keep you safe too, Cecil!", 'Hehe. Of course you will.'),
             ('Ooh, can you make the sparkly purple ones again?', 'A little hex, just for you.'),
             ('Cecil, do you ever sleep?', 'Wizards rest their eyes. Hehehe.')]
    fn('p57/harmony', ['execute on owner unless entity @s[tag=bm.emharm] run function bm:p57/harmony_first',
                       'execute if score @s bm.ems matches 1..3 run return 0', 'execute if score @s bm.ems matches 5.. unless score @s bm.ems matches 6 run return 0',
                       'scoreboard players add @s bm.emi 1', 'execute unless score @s bm.emi matches 45.. run return 0',
                       'execute unless entity @e[type=minecraft:wolf,tag=bm.emmine,distance=..6] run return 0',
                       'scoreboard players set @s bm.emi 0', 'scoreboard players set @s bm.emw 30',
                       'execute as @e[type=minecraft:wolf,tag=bm.emmine,distance=..6] run function bm:p57/cecil_wave',
                       'execute store result score #r bm.rng run random value 1..5'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner run ' + title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(f'"{e}"  ', '#ffd0ec'),
                                                                                              T('Cecil: ', '#b48cff', bold=True), T(f'"{c}"', '#d8c8ff')])
        for i, (e, c) in enumerate(CHATS)] +
       ['execute positioned ~ ~1.8 ~ run particle minecraft:heart ~ ~ ~ 0.3 0.2 0.3 0 2',
        'execute at @e[type=minecraft:wolf,tag=bm.emmine,distance=..6,limit=1] run particle minecraft:witch ~ ~2 ~ 0.3 0.3 0.3 0 10',
        'playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..16] ~ ~ ~ 0.8 1.3'])
    fn('p57/cecil_wave', ['scoreboard players operation #me bm.pid = @s bm.pid', 'function bm:p46/pet/arm_cast', 'scoreboard players set @s bm.cpa 0'])
    fn('p57/harmony_first', ['tag @s add bm.emharm', 'advancement grant @s only bm:story/emma_cecil',
                             tellraw('@s', PREFIX + [T('Harmony! ', PINK, bold=True), T('Emma and Cecil fight better together: ', 'gray'),
                                                     T('Cecil casts every second and hits harder; Emma charges twice as fast and her buffs grow stronger.', 'white')])])

    # ================================================================== finding her: humming in the flowers
    wjson('bm/predicate/p57/flowery.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': FLOWERY}})
    second += ['scoreboard players add #emt bm.bm 1', 'execute if score #emt bm.bm matches 60.. run function bm:p57/enc/check']
    fn('p57/enc/check', ['scoreboard players set #emt bm.bm 0', 'execute unless score #tod bm.bm matches 0..11500 run return 0',
                         f'execute in minecraft:overworld as @a[distance=0..,gamemode=!spectator,predicate=bm:p57/flowery] at @s run function bm:p57/enc/roll'])
    fn('p57/enc/roll', [f'execute if items entity @s container.* {holds} run return 0', f'execute if items entity @s weapon.offhand {holds} run return 0',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.emenc,distance=..128] run return 0',
                        'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                        f'execute store result score #r bm.rng run random value 1..{ENC_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                        'execute store result storage bm:tmp emenc.a int 1 run random value 0..359', 'function bm:p57/enc/at with storage bm:tmp emenc'])
    fn('p57/enc/at', ['$execute rotated $(a) 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p57/enc/place'])
    wjson('bm/tags/block/p57_ground.json', {'values': ['#minecraft:dirt', '#minecraft:grass_blocks', 'minecraft:moss_block']})
    fn('p57/enc/place', ['execute unless block ~ ~-1 ~ #bm:p57_ground run return 0', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                         'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'function bm:p57/enc/spawn',
                         'execute as @a[distance=..40] run ' + title('@s', 'actionbar', T('You hear someone humming a little tune nearby...', '#ffd0ec'))])
    enc_hit = snbt({'Tags': ['bm.emenc', 'bm.emnew'], 'width': F(0.9), 'height': F(1.2), 'response': B(1)})
    fn('p57/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] +
       rig +
       ['tag @e[type=minecraft:item_display,tag=bm.emnew,distance=..1] add bm.emencp',
        'execute as @e[type=minecraft:item_display,tag=bm.emnew,distance=..1] run tag @s add bm.emsel',
        'execute store result storage bm:tmp emenc.a int 1 run random value 0..359', 'function bm:p57/enc/turn with storage bm:tmp emenc',
        'function bm:p57/grow', 'function bm:p57/pose/sit_a', 'tag @e[tag=bm.emsel] remove bm.emsel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.emnew,distance=..1] bm.emt 0',
        'tag @e[tag=bm.emnew,distance=..1] remove bm.emnew',
        'particle minecraft:cherry_leaves ~ ~1 ~ 2 1 2 0 30', 'playsound minecraft:block.note_block.flute neutral @a[distance=..24] ~ ~ ~ 0.8 1.2'])
    fn('p57/enc/turn', ['$execute rotated $(a) 0 run function bm:p57/place'])
    # each second: hum, swing her feet, turn to a player who comes close; gone after 10 minutes or with nobody within 80
    second.append('execute as @e[type=minecraft:interaction,tag=bm.emenc] at @s run function bm:p57/enc/sec')
    fn('p57/enc/sec', ['scoreboard players add @s bm.emt 1',
                       'execute unless entity @a[distance=..80] run return run function bm:p57/enc/gone',
                       'execute if score @s bm.emt matches 600.. run return run function bm:p57/enc/gone',
                       'execute as @e[type=minecraft:item_display,tag=bm.emencp,distance=..2] run tag @s add bm.emsel',
                       'scoreboard players operation #f bm.rng = @s bm.emt', 'scoreboard players operation #f bm.rng %= #4 bm.rng',
                       'execute if score #f bm.rng matches 0 run function bm:p57/pose/sit_a', 'execute if score #f bm.rng matches 2 run function bm:p57/pose/sit_b',
                       'execute if score #f bm.rng matches 1 run particle minecraft:note ~ ~1.5 ~ 0.3 0.2 0.3 1 1',
                       'execute if score #f bm.rng matches 1 run playsound minecraft:block.note_block.flute neutral @a[distance=..20] ~ ~ ~ 0.5 1.5',
                       'execute if score #f bm.rng matches 3 run playsound minecraft:block.note_block.flute neutral @a[distance=..20] ~ ~ ~ 0.5 1.2',
                       'execute if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p57/place',
                       'tag @e[tag=bm.emsel] remove bm.emsel'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4']
    fn('p57/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.emencp,distance=..2]', 'particle minecraft:cherry_leaves ~ ~1 ~ 0.5 1 0.5 0 30', 'kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.emenc] if data entity @s interaction at @s run function bm:p57/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.emenc] if data entity @s attack at @s run function bm:p57/enc/poke']
    fn('p57/enc/click', ['tag @s add bm.emhere', 'execute on target run function bm:p57/enc/talk', 'tag @s remove bm.emhere', 'data remove entity @s interaction'])
    fn('p57/enc/poke', ['execute on attacker run ' + emsay('Eep! Wh-what was that for?!'), 'data remove entity @s attack'])
    fn('p57/enc/talk', ['execute if items entity @s weapon.mainhand #minecraft:flowers run return run function bm:p57/enc/recruit',
                        f'execute if items entity @s container.* {holds} run return run ' + emsay('Oh, hi again! Shouldn\'t you be calling me with the ribbon? Hehe.'),
                        emsay("Oh! H-hi! I'm Emma. I was just looking at the flowers... they're my favourite thing in the whole world!"),
                        'playsound minecraft:entity.allay.ambient_without_item neutral @s ~ ~ ~ 1 1.3'])
    fn('p57/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                           tellraw('@s', [T('Emma: ', PINK, bold=True), T('"For me?! It\'s so pretty... thank you!"', '#ffd0ec')]),
                           tellraw('@s', [T('Emma: ', PINK, bold=True), T('"Um... can I come with you? I\'m not very good at fighting... but I can help! I promise!"', '#ffd0ec')]),
                           tellraw('@s', PREFIX + [T('Emma joins you! ', PINK, bold=True), T("She gives you her ribbon. Use it to call her; sneak + use for her menu.", 'gray')]),
                           give('emma_ribbon'), 'advancement grant @s only bm:story/emma_friend',
                           'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.4',
                           'execute as @e[type=minecraft:interaction,tag=bm.emhere,limit=1] at @s run function bm:p57/enc/gone',
                           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                           f'{sel_pet} run tag @s add bm.emsel2', 'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] run function bm:p57/summon',
                           'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    # Cecil's hint, once, the first time he's summoned
    G.FUNCS['p46/pet/summon_here' if 'p46/pet/summon_here' in G.FUNCS else 'p56/cecil_here'].append('execute unless entity @s[tag=bm.emhint] run function bm:p57/hint')
    fn('p57/hint', ['tag @s add bm.emhint', f'execute if items entity @s container.* {holds} run return 0',
                    tellraw('@s', [T('Cecil: ', '#b48cff', bold=True),
                                   T('"Hehehe... if you ever stroll through a cherry grove or a meadow on a sunny day, listen for humming. '
                                     'A little friend of mine adores flowers."', '#d8c8ff')])])

    # ================================================================== achievements, admin
    granted = {'done': {'trigger': 'minecraft:impossible'}}
    def adv(key, ico, ttl, desc, frame='task'):
        wjson(f'bm/advancement/story/{key}.json', {'parent': 'bm:story/root', 'criteria': granted,
              'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': f'bm:{ico}'}} if ':' not in ico else {'id': ico},
                          'title': T(ttl, 'gold' if frame == 'challenge' else 'yellow'), 'description': T(desc, 'gray'),
                          'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    adv('emma_friend', 'emma_ribbon', 'A Friend Among the Flowers', 'Find Emma humming in the flowers and win her over', 'goal')
    adv('emma_ethereal', 'minecraft:feather', 'Ethereal', "See Emma take her Ethereal Form", 'challenge')
    adv('emma_cecil', 'minecraft:poppy', 'Best of Friends', 'Have Emma and Cecil by your side together', 'goal')
    fn('admin/emma', ['execute rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves run function bm:p57/enc/spawn',
                      tellraw('@s', PREFIX + [T('Emma is sitting in front of you. Right-click her holding a flower.', 'gray')])])
    fn('admin/emma_ribbon', [give('emma_ribbon')])
    fn('admin/emma_charge', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run scoreboard players set @s bm.emc 100',
                             tellraw('@s', PREFIX + [T("Your Emma is fully charged - she ascends when a monster is within 14 blocks.", 'gray')])])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.emp]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.emenc]')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
