"""2.67: Democratus - the storm reaper.

- FINDING HIM: in a thunderstorm, very rarely, lightning flashes near someone out under the open sky - and where it fell, a
  hooded warrior kneels in vigil, both hands on the scythe stood upright before him, his eyes straight ahead. He keeps his
  vigil while the storm lasts. Right-click him: he rises, sizes you up - and walks the storm with you: DEMOCRATUS' STORM SEAL.
- THE SEAL: use it to call him (and call him back). Sneak + use: his challenge - DUEL HIM, or send him home.
- FIGHTING: slow, but every blow is devastating - a great sweep of the scythe (16 damage, 8 to anything beside it) every
  2.5 s. Every blow charges him; at five, his STORM REAP: he spins the scythe round him, the monsters about are lifted off
  their feet, lightning comes down on each - and he slams them into the ground with a thud you feel.
- HIS RIVAL CECIL ("Old Rivals"): you hit harder (Strength), Cecil is tougher (Resistance), and Democratus charges twice as
  fast, out to outdo him (they glare). HIS SUCCESSOR KILLERWATT ("The Storm's Heir"): you're quicker (Speed, Jump Boost),
  KillerWatt is tougher and charges faster, and Democratus regenerates. With both: Resistance for you as well.
- THE DUEL: ten seconds to put some distance between you - then he fights you for real (400 health: slow heavy sweeps, a
  lunging slash, lightning called down where you stand, his Storm Reap). Drop to three hearts (or fall, or run) and it's over:
  he goes home, to be called again whenever you like - and challenged again whenever you like. Bring him to his knee and you
  win: the first time, HIS SCYTHE is yours (one per player); after that, only his respect.
- HIS SCYTHE: heavy and slow (15 damage). Every blow arcs lightning to two monsters close by and charges it; at eight, a STORM
  REAP of your own.
- Like the others: an item frame, right-click him to sit, 5 minutes if he faints, his face moves (his violet eyes glow in the
  dark), Emma's pulses reach him, a raid contract at Goldtooth."""
from items import item, T, TOTEM, attr
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import phase97_art as ART
import phase95 as FX
import phase72 as P72
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase28 as P28
import allies

PET_CD = 300
HP = 80
DUEL_HP = 400
DUEL_YIELD = 60                     # (he yields at this much health - he can't be killed outright)
STORM, STORM_LT, GOLD = '#7ad06a', '#e0f8d8', '#f0cf4a'
MENU = 9700
SCY_CHARGE = 8

item('demo_seal', TOTEM, "Democratus' Storm Seal", STORM,
     ['The green crystal of his scythe, in golden claws.', ('Use: call Democratus (or call him back).', 'blue'),
      ('Sneak + use: his challenge - a duel - or send him home.', 'blue'), ('Slow, devastating sweeps; every fifth blow', 'blue'),
      ('a STORM REAP: lifted, struck, slammed down.', 'blue'), ('Old Rivals: with Cecil. The Storm\'s Heir: with KillerWatt.', 'gray'),
      ('If he faints: 5 minutes before he can return.', 'gray')],
     model='bm:demo_seal', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['demo_seal'] = 'bm:p97/use'
item('fcontract_demo', TOTEM, 'Raid Contract: Democratus', STORM,
     ['Signed in gold ink, sealed in wax.', ('Use once: from then on Democratus', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_demo'] = 'bm:p97/sign'
item('demo_scythe', TOTEM, "Democratus' Scythe", STORM,
     ['Won from the storm reaper himself, in a fair fight.', ('Heavy and slow: 15 damage, a long reach.', 'gray'),
      ('Every blow arcs lightning to two monsters', 'blue'), ('close by, and charges the blade.', 'blue'),
      (f'At {SCY_CHARGE}: a STORM REAP - lifted, struck, slammed.', 'blue')],
     model='bm:demo_scythe', stack=1, cat='relic', bold=True, glint=False,
     comps={'minecraft:attribute_modifiers': [attr('attack_damage', 14, 'mainhand', ident='minecraft:base_attack_damage'),
                                              attr('attack_speed', -3.2, 'mainhand', ident='minecraft:base_attack_speed'),
                                              attr('entity_interaction_range', 0.75, 'mainhand')],
            'minecraft:enchantments': {'bm:storm_reap': 1}})
P72.KEEP.append('demo_seal')
P46.COMPANIONS += ',tag=!bm.dmpet'               # (Cecil's spells pass him by, like the others)
allies.ALLIES.append('bm.dmpet')                 # (and so does every friendly-fire list)
BIT = 2 ** len(P89.BIT)
P89.BIT['demo'] = BIT                            # (admin/contracts_all signs him too)
P68.KINDS['demo'] = (5, 'demo_seal', 'wolf', 'bm.dmpet', 'p97/summon', 'p97/dismiss', 'bm.dmsel2', 'Democratus', STORM)
P68.HE.add('demo')
P28.MENU['demo'] = MENU
# his faces (phase95's controller): calm he smirks, or glares at nothing much; arriving, a smirk; in a fight or low, serious
FX.FOLK['demo'] = ('minecraft:wolf', 'bm.dmpet', 'type=minecraft:item_display,tag=bm.dmp,tag=bm.dp_head,tag=!bm.dmfade', ART.DEMO_EXPR,
                   (60, 130), [('smirk', 40, 4), ('glare', 26, 9)], ('smirk', 40), 'serious', 'serious')


def extend_offers(O, offer):
    pass                          # (found in the storm, never sold - only his raid contract, at Goldtooth)


def rp(R):
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('dm_',)
    R.ICONS['demo_seal'] = ART.seal_icon(R)
    R.ICONS['demo_scythe'] = ART.scythe_icon(R)
    # his faces: a head model per expression - the face and the glowing eyes swapped together
    tex, els = R.HATS['dm_head']
    cases = []
    for e in ART.DEMO_EXPR:
        R.HATS[f'dm_head_x{e}'] = (dict(tex, dm_face=f'bm:block/dm_face_{e}', dm_glow=f'bm:block/dm_glow_{e}'), els)
        cases.append((e, f'dm_head_x{e}'))
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/dm_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl('dm_head')}})
        # the scythe in the hand: the rig's own scythe model (shown at 4/3, as it's built at 3/4); in the inventory, its icon
        k = 1 / ART.SCYTHE_K
        R2.wj('assets/bm/models/item/demo_scythe_held.json', {'parent': 'bm:item/dm_scythe', 'display': {
            'thirdperson_righthand': {'rotation': [0, 90, 10], 'translation': [0, 3.5, 1], 'scale': [round(0.62 * k, 3)] * 3},
            'thirdperson_lefthand': {'rotation': [0, -90, -10], 'translation': [0, 3.5, 1], 'scale': [round(0.62 * k, 3)] * 3},
            'firstperson_righthand': {'rotation': [0, 90, 20], 'translation': [2, 2, 0], 'scale': [round(0.42 * k, 3)] * 3},
            'firstperson_lefthand': {'rotation': [0, -90, -20], 'translation': [2, 2, 0], 'scale': [round(0.42 * k, 3)] * 3},
            'head': {'rotation': [0, 0, 0], 'translation': [0, 8, 0], 'scale': [0.6] * 3}}})
        R2.wj('assets/bm/items/demo_scythe.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:display_context',
                                                             'cases': [{'when': ['gui', 'fixed', 'ground'], 'model': mdl('demo_scythe')}],
                                                             'fallback': mdl('demo_scythe_held')}})
    R.POST.append(post)


def generate(G):
    import phase73 as P73
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    dsay = lambda txt, who='@s': title(who, 'actionbar', [T('Democratus: ', STORM, bold=True), T(txt, STORM_LT)])
    dchat = lambda txt, who='@s': tellraw(who, [T('Democratus: ', STORM, bold=True), T(f'"{txt}"', STORM_LT)])
    tick, fast, second = [], [], []
    # (2.67b) the storm feeds him: his blows by the weather over his head - (0 clear, 1 rain, 2 thunder)
    WX_SWEEP, WX_BOLT, WX_SLAM = [(0, 16), (1, 20), (2, 26)], [(0, 9), (1, 12), (2, 15)], [(0, 12), (1, 15), (2, 18)]
    WX_DSWEEP, WX_DBOLT, WX_DSLAM = [(0, 14), (1, 17), (2, 21)], [(0, 10), (1, 12), (2, 15)], [(0, 12), (1, 14), (2, 17)]
    objs = ['bm.dms', 'bm.dmf', 'bm.dmcd', 'bm.dmk', 'bm.dma', 'bm.dmm', 'bm.dmz', 'bm.dml', 'bm.dmch', 'bm.dmq', 'bm.dmb', 'bm.dmcl',
            'bm.dmsl', 'bm.dmw', 'bm.dmd', 'bm.dmdb', 'bm.dmdn', 'bm.dmsc', 'bm.dmsch', 'bm.dmsrt', 'bm.dmwx', 'bm.dmwp']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard objectives add bm.dmdth deathCount',
                                                                                      'bossbar add bm:dmb {text:"Democratus",color:"#7ad06a"}',
                                                                                      'bossbar set bm:dmb color green', f'bossbar set bm:dmb max {DUEL_HP}',
                                                                                      'bossbar set bm:dmb style notched_10']
    G.OBJECTIVES += objs + ['bm.dmdth']
    holds = '*[minecraft:custom_data~{bm:"demo_seal"}]'
    scythe_held = '*[minecraft:custom_data~{bm:"demo_scythe"}]'
    S = ART.RIG_SCALE
    U = S / 16
    SK = round(S / ART.SCYTHE_K, 4)
    foe = 'type=#bm:hostile,tag=!bm.npc'
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.dmpet] if score @s bm.pid = #me bm.pid'
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]
    face = lambda e, t: FX.face_cmd('demo', e, t)
    SEL = '@e[type=minecraft:item_display,tag=bm.dmsel'
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in (5, 20, 24, 60, 120, 160)]

    # ================================================================== the rig
    def part_nbt(p, extra=()):
        sc = SK if p == 'scythe' else S
        return snbt({'Tags': ['bm.dmp', f'bm.dp_{p}', 'bm.dmnew'] + list(extra),
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:dm_{p}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(8), 'start_interpolation': Int(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    rig = [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS]
    def place_lines():
        out = []
        for p in ART.PARTS:
            x, y, z = ART.joint(p)
            out.append(f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp {SEL},tag=bm.dp_{p}] ~ ~ ~ ~ 0')
        return out
    fn('p97/place', place_lines())
    fn('p97/place_y', ['$execute rotated as @s rotated ~$(y) 0 run function bm:p97/place'])
    fn('p97/grow', [f'execute as {SEL},tag=!bm.dp_scythe] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}',
                    f'execute as {SEL},tag=bm.dp_scythe] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SK}f,{SK}f,{SK}f]}}}}',
                    f'execute at {SEL},tag=bm.dp_body,limit=1] run function bm:p97/burst'])
    fn('p97/burst', ['particle minecraft:flash{color:[0.55,1.0,0.5,1.0]} ~ ~1.2 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~1.2 ~ 0.5 1.0 0.5 0.3 60',
                     'particle minecraft:end_rod ~ ~1 ~ 0.1 0.4 0.1 0.12 20', 'particle minecraft:dust{color:[0.48,0.82,0.42],scale:1.6} ~ ~1 ~ 0.5 0.9 0.5 0 24',
                     'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..32] ~ ~ ~ 0.5 1.4'])
    fn('p97/head', ['$data modify entity @e[type=minecraft:item_display,tag=bm.dmsel,tag=bm.dp_head,limit=1] item.components."minecraft:custom_model_data" set value {strings:["$(e)"]}'])

    # ---- poses (a pose swaps a part's second model in or out: his bent arms, his bent legs)
    DUR = {'idle_a': 12, 'idle_b': 12, 'idle_look': 14, 'walk_a': 5, 'walk_up': 5, 'walk_b': 5, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 4,
           'kneel': 12, 'kneel_b': 16, 'sit_a': 12, 'sit_b': 14, 'sit_look': 14, 'plant': 4, 'swing_back': 9, 'swing': 3, 'spin': 5,
           'overhead': 6, 'slam': 2, 'yield': 10}
    def xf_nbt(pose, p):
        rot, tr = ART.part_xf(pose, p)
        return f'left_rotation:{snbt(qf(rot))},translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f]'
    DUR.update({f'swim_{i}': 3 for i in range(ART.SWIM_FRAMES)})
    for name, pose in ART.POSES.items():
        lines = [f'execute as {SEL},tag=bm.dp_{p}] run data merge entity @s {{start_interpolation:0,interpolation_duration:{DUR[name]},transformation:{{{xf_nbt(pose, p)}}}}}'
                 for p in ART.PARTS]
        lines += [f'execute as {SEL},tag=bm.dp_{p}] run data modify entity @s item.components."minecraft:item_model" set value "bm:dm_{p}'
                  + (f'_{pose["_alt"][p]}' if pose['_alt'].get(p) else '') + '"' for p in ART.ALT]
        fn(f'p97/pose/{name}', lines)
    # states: 0 idle, 1 walk, 2 run, 3 air, 4 sit, 6 arriving (the scythe slammed down), 7 the sweep, 8 the Storm Reap,
    #         9 calling lightning (the duel), 11 the lunge (the duel), 12 yielding (a duel lost), 13 the duel's countdown
    CYCLE = {0: (160, [(0, 'idle_a'), (40, 'idle_b'), (80, 'idle_a'), (104, 'idle_look'), (136, 'idle_a')]),
             1: (20, [(0, 'walk_a'), (5, 'walk_up'), (10, 'walk_b'), (15, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]),
             3: (None, [(0, 'jump')]), 6: (None, [(0, 'plant')]),
             4: (160, [(0, 'sit_a'), (40, 'sit_b'), (80, 'sit_a'), (110, 'sit_look'), (140, 'sit_a')]),
             7: (None, [(0, 'swing_back'), (12, 'swing'), (20, 'idle_a')]), 8: (None, [(0, 'spin'), (34, 'overhead'), (44, 'slam'), (54, 'idle_a')]),
             9: (None, [(0, 'overhead'), (26, 'slam'), (32, 'idle_a')]), 11: (None, [(0, 'run_a'), (8, 'swing_back'), (12, 'swing')]),
             12: (None, [(0, 'yield')]), 13: (None, [(0, 'plant')]),
             10: (3 * ART.SWIM_FRAMES, [(3 * i, f'swim_{i}') for i in range(ART.SWIM_FRAMES)])}
    anim = []
    for st, (period, frames) in CYCLE.items():
        lines = ['scoreboard players operation #f bm.rng = @s bm.dmf']
        if period: lines.append(f'scoreboard players operation #f bm.rng %= #{period} bm.rng')
        lines += [f'execute if score #f bm.rng matches {t} run function bm:p97/pose/{p}' for t, p in frames]
        fn(f'p97/anim/{st}', lines)
        anim.append(f'execute if score @s bm.dms matches {st} run return run function bm:p97/anim/{st}')
    fn('p97/anim', anim)
    # (as a host) moving how? -> #st: 1 walking, 2 running, 3 in the air (a few ticks), else 0
    fn('p97/move', ['execute store result score #og bm.rng run data get entity @s OnGround', 'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                    'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.dmz 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.dmz 0',
                    'execute if score @s bm.dmz matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                    'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                    'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                    'scoreboard players operation #vx bm.rng += #vz bm.rng',
                    'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                    'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                    'scoreboard players set #st bm.rng 0'])
    fn('p97/state', ['execute if score @s bm.dmsl matches 1.. run return run scoreboard players set #st bm.rng 6',
                     'execute if score @s bm.dmk matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.dma',
                     'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                     'function bm:p97/move'])
    fn('p97/frame', ['execute if score #st bm.rng = @s bm.dms run scoreboard players add @s bm.dmf 1',
                     'execute unless score #st bm.rng = @s bm.dms run scoreboard players set @s bm.dmf 0',
                     'scoreboard players operation @s bm.dms = #st bm.rng', 'function bm:p97/anim'])
    # (as a host) the spin: the whole rig turned about him, 24 degrees a tick
    fn('p97/spin', ['execute store result storage bm:tmp dmy.y int 24 run scoreboard players get @s bm.dmf', 'function bm:p97/place_y with storage bm:tmp dmy'])

    # ================================================================== the follower: every tick
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.dmpet] at @s run function bm:p97/tick')
    fn('p97/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:item_display,tag=bm.dmp,tag=!bm.dmfade,tag=!bm.dmencp,tag=!bm.dmbp] if score @s bm.pid = #me bm.pid run tag @s add bm.dmsel',
                    f'execute unless entity {SEL},tag=bm.dp_scythe] run function bm:p97/rerig',
                    'execute if score @s bm.dmk matches 1.. run function bm:p97/act_tick',
                    'execute if score @s bm.dmm matches 1.. run scoreboard players remove @s bm.dmm 1',
                    'execute if score @s bm.dmsl matches 1.. run scoreboard players remove @s bm.dmsl 1',
                    # his fights: the Storm Reap once he's charged and a monster's near, else the sweep at anything in reach
                    f'execute unless score @s bm.dmk matches 1.. unless score @s bm.dmm matches 1.. unless score @s bm.dmsl matches 1.. unless data entity @s {{Sitting:1b}} '
                    f'if score @s bm.dmch matches 5.. if entity @e[{foe},distance=..6] run function bm:p97/reap_go',
                    f'execute unless score @s bm.dmk matches 1.. unless score @s bm.dmm matches 1.. unless score @s bm.dmsl matches 1.. unless data entity @s {{Sitting:1b}} '
                    f'if entity @e[{foe},distance=..3.8] run function bm:p97/swing_go',
                    'function bm:p97/state', 'function bm:p97/frame',
                    'execute on owner run tag @s add bm.dmown',
                    # facing: in a fight his foe (spinning: round and round); sitting, arriving, idle: you; moving: where he's going
                    'execute if score @s bm.dms matches 8 if score @s bm.dmf matches ..30 run function bm:p97/spin',
                    f'execute if score @s bm.dms matches 7..8 unless score @s bm.dmf matches ..30 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p97/place',
                    f'execute if score @s bm.dms matches 7 if score @s bm.dmf matches ..30 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p97/place',
                    f'execute if score @s bm.dms matches 7..8 unless entity @e[{foe},distance=..17] unless score @s bm.dmf matches ..30 rotated as @s rotated ~ 0 run function bm:p97/place',
                    'execute if score @s bm.dms matches 4 run function bm:p97/face_you',
                    'execute if score @s bm.dms matches 6 run function bm:p97/face_you',
                    'execute if score @s bm.dms matches 0 run function bm:p97/face_you',
                    'execute if score @s bm.dms matches 1..3 rotated as @s rotated ~ 0 run function bm:p97/place',
                    'execute if score @s bm.dms matches 10 rotated as @s rotated ~ 0 run function bm:p97/place',
                    'tag @a[tag=bm.dmown] remove bm.dmown', 'tag @e[tag=bm.dmsel] remove bm.dmsel'])
    fn('p97/face_you', ['execute if entity @a[tag=bm.dmown,distance=1.5..10] facing entity @a[tag=bm.dmown,limit=1] feet rotated ~ 0 run return run function bm:p97/place',
                        'execute rotated as @s rotated ~ 0 run function bm:p97/place'])

    # ---- the sweep (26 ticks: hauled back, round - the blow lands on the 14th) and the Storm Reap (60 ticks)
    # (he plants his feet for a blow - no drifting out of reach mid-swing)
    fn('p97/swing_go', ['scoreboard players set @s bm.dmk 26', 'scoreboard players set @s bm.dma 7', 'scoreboard players set @s bm.dmm 50',
                        'effect give @s minecraft:slowness 1 9 true',
                        'playsound minecraft:item.trident.riptide_1 neutral @a[distance=..16] ~ ~ ~ 0.5 0.6'])
    fn('p97/act_tick', ['scoreboard players remove @s bm.dmk 1',
                        'execute if score @s bm.dma matches 7 if score @s bm.dmk matches 12 run function bm:p97/swing_hit',
                        'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 56 run function bm:p97/reap_lift',
                        'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 36 run function bm:p97/reap_bolt',
                        'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 14 run function bm:p97/reap_slam',
                        'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 34..58 run particle minecraft:electric_spark ~ ~1.4 ~ 1.6 0.3 1.6 0.1 6'])
    me = '@e[type=minecraft:wolf,tag=bm.dmme,limit=1]'
    wx = ['scoreboard players set #dmwx bm.rng 0', 'execute if score @s bm.dmwx matches 1.. run scoreboard players operation #dmwx bm.rng = @s bm.dmwx']
    fn('p97/swing_hit', wx + ['tag @s add bm.dmme', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                         'playsound minecraft:item.trident.thunder neutral @a[distance=..20] ~ ~ ~ 0.2 1.8',
                         f'execute as @e[{foe},distance=..4.2,sort=nearest,limit=1] at @s run function bm:p97/swung',
                         'tag @s remove bm.dmme',
                         'scoreboard players add @s bm.dmch 1', 'execute if entity @s[tag=bm.dmdc] run scoreboard players add @s bm.dmch 1',
                         'execute if score @s bm.dmwx matches 2 run scoreboard players add @s bm.dmch 1',
                         'scoreboard players add @s bm.dmq 1', 'execute if score @s bm.dmq matches 9.. run function bm:p97/quip'])
    fn('p97/swung', [f'execute if score #dmwx bm.rng matches {w} run damage @s {d} minecraft:mob_attack by {me}' for w, d in WX_SWEEP] +
                    [f'execute if score #dmwx bm.rng matches {w} as @e[{foe},distance=0.1..2.8] run damage @s {d // 2} minecraft:mob_attack by {me}' for w, d in WX_SWEEP] + [
                     'particle minecraft:sweep_attack ~ ~1 ~ 0.6 0.3 0.6 0 3', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.2 16'])
    fn('p97/reap_go', ['scoreboard players set @s bm.dmk 60', 'scoreboard players set @s bm.dma 8', 'scoreboard players set @s bm.dmm 80', 'scoreboard players set @s bm.dmch 0',
                       'effect give @s minecraft:slowness 3 9 true',
                       'playsound minecraft:block.beacon.power_select neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                       'playsound minecraft:item.trident.riptide_3 neutral @a[distance=..24] ~ ~ ~ 1 0.7',
                       'execute on owner if entity @s[distance=..32] run ' + title('@s', 'actionbar', [T('Democratus: ', STORM, bold=True), T('STORM REAP!', GOLD, bold=True)])] +
       face('serious', 60))
    fn('p97/reap_lift', [f'tag @e[{foe},distance=..7] add bm.dmreap', 'effect give @e[tag=bm.dmreap,distance=..8] minecraft:levitation 2 1 true',
                         'particle minecraft:sweep_attack ~ ~1 ~ 2.4 0.2 2.4 0 10', 'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p97/reap_bolt', wx + ['tag @s add bm.dmme', 'execute as @e[tag=bm.dmreap,distance=..12] at @s run function bm:p97/bolted', 'tag @s remove bm.dmme',
                         'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..48] ~ ~ ~ 1 1.1'])
    fn('p97/bolted', [f'execute if score #dmwx bm.rng matches {w} run damage @s {d} minecraft:lightning_bolt by {me}' for w, d in WX_BOLT] + [ 'particle minecraft:flash{color:[0.7,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                      'particle minecraft:electric_spark ~ ~2 ~ 0.1 2.0 0.1 0.05 40', 'particle minecraft:end_rod ~ ~3 ~ 0.05 2.5 0.05 0 20',
                      'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..32] ~ ~ ~ 0.8 1.2'])
    fn('p97/reap_slam', wx + ['tag @s add bm.dmme', 'execute as @e[tag=bm.dmreap,distance=..12] at @s run function bm:p97/slammed', 'tag @s remove bm.dmme',
                         'tag @e[tag=bm.dmreap] remove bm.dmreap', 'function bm:p97/thud'])
    fn('p97/slammed', ['effect clear @s minecraft:levitation', 'data modify entity @s Motion set value [0.0d,-2.4d,0.0d]',
                       'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 0.6 0.1 0.6 0 30'] +
       [f'execute if score #dmwx bm.rng matches {w} run damage @s {d} minecraft:mob_attack by {me}' for w, d in WX_SLAM])
    fn('p97/thud', ['particle minecraft:explosion ~ ~0.3 ~ 2.0 0.1 2.0 0 8', 'particle minecraft:electric_spark ~ ~0.3 ~ 3.0 0.1 3.0 0.3 80',
                    'particle minecraft:block{block_state:"minecraft:stone"} ~ ~0.2 ~ 2.5 0.1 2.5 0 60',
                    'playsound minecraft:block.anvil.land neutral @a[distance=..40] ~ ~ ~ 1.4 0.5', 'playsound minecraft:entity.generic.explode neutral @a[distance=..40] ~ ~ ~ 0.9 0.5',
                    'playsound minecraft:entity.warden.attack_impact neutral @a[distance=..40] ~ ~ ~ 1 0.6'])
    QUIPS = ['Kneel.', 'The storm reaps what it will.', 'Too slow.', 'Is that all?', 'Again.', 'Stand behind me, little one.', 'Hah. Weak.']
    fn('p97/quip', ['scoreboard players set @s bm.dmq 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..20] run ' + dsay(q) for i, q in enumerate(QUIPS)])

    # ================================================================== the seal: call, recall, his challenge
    pet = {'Tags': ['bm.dmpet', 'bm.dmnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(HP),
           'CustomName': T('Democratus', STORM, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(HP)}, {'id': 'minecraft:armor', 'base': D(12)}, {'id': 'minecraft:armor_toughness', 'base': D(4)},
                          {'id': 'minecraft:attack_damage', 'base': D(2)}, {'id': 'minecraft:knockback_resistance', 'base': D(0.8)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.31)}, {'id': 'minecraft:follow_range', 'base': D(32)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p97/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                   'execute if predicate bm:p20/sneaking run return run function bm:p97/menu',
                   f'{sel_pet} run tag @s add bm.dmsel2',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.dmsel2] run function bm:p97/recall',
                   'execute unless entity @e[type=minecraft:wolf,tag=bm.dmsel2] run function bm:p97/try_summon',
                   'tag @e[tag=bm.dmsel2] remove bm.dmsel2'])
    fn('p97/recall', ['tp @e[type=minecraft:wolf,tag=bm.dmsel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.dmsel2,limit=1] Sitting set value 0b',
                      'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.8 0.4 0.2 30', 'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..16] ~ ~ ~ 0.3 1.6',
                      dsay('I am here. Point me at something.')])
    fn('p97/try_summon', ['execute if entity @s[tag=bm.dmduel] run return run ' + say('You are in the middle of a duel with him.'),
                          'execute if score @s bm.dmcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.dmcd',
                          'execute if score @s bm.dmcd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.dmcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                          'execute if score @s bm.dmcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Democratus is still nursing his pride: about ', 'gray'),
                                                                                                             {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                          'execute unless function bm:p97/ok run return run ' + say("Democratus can't come here."),
                          'function bm:p97/summon'])
    fn('p97/summon', ['execute positioned ^ ^ ^1.4 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p97/summon_here',
                      'execute positioned ^ ^1 ^1.4 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p97/summon_here',
                      'function bm:p97/summon_here'])
    fn('p97/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                           'data modify entity @e[type=minecraft:wolf,tag=bm.dmnew,limit=1,sort=nearest] Owner set from entity @s UUID',
                           f'attribute @e[type=minecraft:wolf,tag=bm.dmnew,limit=1,sort=nearest] minecraft:max_health base set {HP}',
                           f'data modify entity @e[type=minecraft:wolf,tag=bm.dmnew,limit=1,sort=nearest] Health set value {HP}f',
                           'scoreboard players set @e[type=minecraft:wolf,tag=bm.dmnew,limit=1,sort=nearest] bm.dms -1',
                           'scoreboard players set @e[type=minecraft:wolf,tag=bm.dmnew,limit=1,sort=nearest] bm.dmsl 24',
                           'execute rotated ~180 0 run function bm:p97/rig_here',
                           'scoreboard players operation @e[tag=bm.dmnew,distance=..4] bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:item_display,tag=bm.dmnew,distance=..4] run tag @s add bm.dmsel', 'function bm:p97/grow',
                           'tag @e[tag=bm.dmsel] remove bm.dmsel', 'tag @e[tag=bm.dmnew,distance=..4] remove bm.dmnew',
                           'playsound minecraft:block.anvil.land neutral @a[distance=..20] ~ ~ ~ 0.5 0.6',
                           dsay('So. You called, and the storm answered. Show me something worth reaping.')])
    fn('p97/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p97/rerig', ['kill @e[type=minecraft:item_display,tag=bm.dmsel]', 'execute rotated as @s rotated ~ 0 run function bm:p97/rig_here',
                     'scoreboard players operation @e[type=minecraft:item_display,tag=bm.dmnew,distance=..2] bm.pid = #me bm.pid',
                     'tag @e[type=minecraft:item_display,tag=bm.dmnew,distance=..2] add bm.dmsel', 'tag @e[type=minecraft:item_display,tag=bm.dmnew,distance=..2] remove bm.dmnew',
                     'function bm:p97/grow', 'scoreboard players set @s bm.dms -1', 'scoreboard players set @s bm.fxl -1'])
    fn('p97/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.dmsel2] at @s run function bm:p97/fade',
                       'execute as @e[type=minecraft:wolf,tag=bm.dmsel2] on passengers run kill @s',
                       'execute as @e[type=minecraft:wolf,tag=bm.dmsel2] run data remove entity @s Owner',
                       'execute as @e[type=minecraft:wolf,tag=bm.dmsel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.dmsel2]'])
    fn('p97/send_home', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.dmsel2',
                         'execute unless entity @e[type=minecraft:wolf,tag=bm.dmsel2] run return run ' + say("Democratus isn't with you. (Use the seal to call him.)"),
                         'function bm:p97/dismiss', dsay('Until the next storm, then.'), 'tag @e[tag=bm.dmsel2] remove bm.dmsel2'])

    # ---- his challenge (sneak + use): a duel, or send him home
    def menu(prize):
        lines = [P28.body([T('"Steel answers steel. Face me - truly face me - and if you can bring me to my knee, my scythe is yours."', STORM_LT, italic=True)])
                 if prize else P28.body([T('"You have my scythe already. Again? Good. The only prize is the fight."', STORM_LT, italic=True)]),
                 P28.body([T('Ten seconds to get some distance. Fall to three hearts and the duel is lost - no harm done: call him again, challenge him again.', 'gray')])]
        return P28.multi([T("Democratus' Challenge", STORM, bold=True)], lines,
                         [P28.btn([T('Duel him', '#ff8a6a', bold=True)], MENU + 1, width=220), P28.btn([T('Wardrobe', STORM, bold=True)], MENU + 3, width=220),
                          P28.btn([T('Send him home', 'white')], MENU + 2, width=220)],
                         columns=1, exit_label='Not now')
    fn('p97/menu', [f'scoreboard players set @s bm.menu {MENU}',
                    f'execute if score @s bm.dmsc matches 1.. run return run dialog show @s {snbt(menu(False))}',
                    f'dialog show @s {snbt(menu(True))}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {MENU + 1}..{MENU + 3} run return run function bm:p97/act')
    fn('p97/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                   f'execute unless items entity @s container.* {holds} unless items entity @s weapon.offhand {holds} run return run function bm:p28/stale',
                   f'execute if score #act bm.pay matches {MENU + 1} run return run function bm:p97/duel/start',
                   f'execute if score #act bm.pay matches {MENU + 2} run return run function bm:p97/send_home',
                   f'execute if score #act bm.pay matches {MENU + 3} run return run function bm:p99/menu/demo'])

    # ---- (2.67) a click box the size of him: right-click him to sit him down / stand him up
    second.append('execute as @e[type=minecraft:wolf,tag=bm.dmpet,tag=!bm.ffpet] unless function bm:p97/has_hit at @s run function bm:p97/add_hit')
    fn('p97/has_hit', ['execute on passengers if entity @s[type=minecraft:interaction,tag=bm.dmhit] run return 1', 'return 0'])
    fn('p97/add_hit', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.dmhit","bm.dmhnew"],width:0.9f,height:1.5f,response:1b}',
                       'ride @e[type=minecraft:interaction,tag=bm.dmhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.dmhnew] remove bm.dmhnew'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.dmhit] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.dmhit] if data entity @s interaction run function bm:p97/click',
             'execute as @e[type=minecraft:interaction,tag=bm.dmhit] if data entity @s attack run data remove entity @s attack']
    dw = '@e[type=minecraft:wolf,tag=bm.dmclk,limit=1]'
    fn('p97/click', ['execute on vehicle run tag @s add bm.dmclk', 'execute on target at @s run function bm:p97/who', 'tag @e[tag=bm.dmclk] remove bm.dmclk',
                     'data remove entity @s interaction'])
    tick.append('scoreboard players remove @a[scores={bm.dmcl=1..}] bm.dmcl 1')
    fn('p97/who', ['execute if score @s bm.dmcl matches 1.. run return 0', 'scoreboard players set @s bm.dmcl 10',
                   'scoreboard players operation #me bm.pid = @s bm.pid',
                   f'execute unless score {dw} bm.pid = #me bm.pid run return run ' + dsay('I walk with another. Move along.'),
                   f'execute store success score #s0 bm.rng if data entity {dw} {{Sitting:1b}}',
                   f'execute if score #s0 bm.rng matches 1 run data modify entity {dw} Sitting set value 0b',
                   f'execute if score #s0 bm.rng matches 0 run data modify entity {dw} Sitting set value 1b',
                   'execute if score #s0 bm.rng matches 1 run ' + dsay('Enough rest. Onward.'),
                   'execute if score #s0 bm.rng matches 0 run ' + dsay('Hmph. A moment, then.'),
                   f'execute if score #s0 bm.rng matches 0 as {dw} run function bm:p97/sat'])
    fn('p97/sat', face('smirk', 30))
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.dmhit]')

    # ---- fainting: the rig without its host (4 ticks running) crackles away; the seal rests 5 minutes
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.dp_body,tag=!bm.dmfade,tag=!bm.dmencp,tag=!bm.dmbp] at @s run function bm:p97/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.dmfade] bm.dml 1',
             'kill @e[type=minecraft:item_display,tag=bm.dmfade,scores={bm.dml=..0}]']
    fn('p97/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{sel_pet.replace("tag=bm.dmpet]", "tag=bm.dmpet,distance=..16]")} run return run scoreboard players set @s bm.dmz 0',
                     'scoreboard players add @s bm.dmz 1', 'execute if score @s bm.dmz matches 4.. run function bm:p97/fell'])
    fn('p97/fell', ['function bm:p97/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p97/cooldown'])
    fn('p97/cooldown', [f'scoreboard players set @s bm.dmcd {PET_CD}',
                        tellraw('@s', PREFIX + [T('Democratus falls to one knee. ', STORM, bold=True), T('"...A scratch. The storm will have me back." ', STORM_LT),
                                                T(f'The seal needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn('p97/fade', ['execute as @e[type=minecraft:item_display,tag=bm.dmp,tag=!bm.dmfade,tag=!bm.dmencp] if score @s bm.pid = #me bm.pid run function bm:p97/fade1',
                    'particle minecraft:electric_spark ~ ~1 ~ 0.5 1 0.5 0.3 90', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.4 0.1 0.15 30',
                    'particle minecraft:flash{color:[0.55,1.0,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1',
                    'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..24] ~ ~ ~ 0.5 1.5',
                    'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 0.8 0.8'])
    fn('p97/fade1', ['tag @s add bm.dmfade', 'scoreboard players set @s bm.dml 3',
                     'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:8048746}'])
    second.append('scoreboard players remove @a[scores={bm.dmcd=1..}] bm.dmcd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.dmpet] if score @s bm.pid = #me bm.pid at @s run function bm:p97/go')
    fn('p97/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p97/fade', 'execute on passengers run kill @s', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    # (2.76: his own call ticket - sharing Leo's, calling either one sent the other home)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.fgd dummy']
    G.OBJECTIVES += ['bm.fgd']
    P73.follow_rules(G, ('demo', 'wolf', 'bm.dmpet', 'demo_seal', 'p97/go', 'Democratus', 'bm.fgd', 'p97/summon_here'), second)
    # (Emma's pulses buff him too, as they do Celi)
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', 'tag=bm.dmpet') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]

    # ================================================================== the rivals and the heir: every second, as Democratus
    second.append('execute as @e[type=minecraft:wolf,tag=bm.dmpet,tag=!bm.ffpet] at @s run function bm:p97/sec')
    wjson('bm/predicate/p97/regen.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:effects': {'minecraft:regeneration': {}}}})
    fn('p97/sec', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s remove bm.dmdc', 'tag @s remove bm.dmdk',
                   'scoreboard players set #dc bm.rng 0', 'scoreboard players set #dk bm.rng 0',
                   'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #dc bm.rng 1',
                   'execute as @e[type=minecraft:wolf,tag=bm.kxpet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #dk bm.rng 1',
                   'execute if score #dc bm.rng matches 1 run tag @s add bm.dmdc', 'execute if score #dk bm.rng matches 1 run tag @s add bm.dmdk',
                   'execute on owner if entity @s[distance=..24] run tag @s add bm.dmown',
                   'function bm:p97/wx',
                   'execute if entity @a[tag=bm.dmown] run function bm:p97/care',
                   'tag @a[tag=bm.dmown] remove bm.dmown'])
    # (2.67b) the weather over his head (open sky): rain - he hits harder and shrugs off blows; a thunderstorm - harder still,
    #  tougher still, he heals, and every blow charges him twice
    wjson('bm/predicate/p97/rain.json', {'condition': 'minecraft:weather_check', 'raining': True})
    fn('p97/wx', ['scoreboard players set @s bm.dmwx 0',
                  'execute if predicate bm:p97/rain positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set @s bm.dmwx 1',
                  'execute if predicate bm:p79/thunder positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set @s bm.dmwx 2',
                  'execute if score @s bm.dmwx matches 1 run effect give @s minecraft:resistance 3 0 true',
                  'execute if score @s bm.dmwx matches 2 run effect give @s minecraft:resistance 3 1 true',
                  'execute if score @s bm.dmwx matches 2 unless predicate bm:p97/regen run effect give @s minecraft:regeneration 5 0 true',
                  'execute if score @s bm.dmwx matches 1 run particle minecraft:electric_spark ~ ~1.6 ~ 0.4 0.8 0.4 0.05 2',
                  'execute if score @s bm.dmwx matches 2 run particle minecraft:electric_spark ~ ~1.6 ~ 0.5 0.9 0.5 0.15 10',
                  'execute unless score @s bm.dmwx = @s bm.dmwp if score @s bm.dmwx matches 1.. as @a[tag=bm.dmown] at @s run function bm:p97/wx_say',
                  'scoreboard players operation @s bm.dmwp = @s bm.dmwx'])
    fn('p97/wx_say', ['execute if score @e[type=minecraft:wolf,tag=bm.dmpet,limit=1,sort=nearest] bm.dmwx matches 1 run ' + dsay('Rain... the storm stirs in me.'),
                      'execute if score @e[type=minecraft:wolf,tag=bm.dmpet,limit=1,sort=nearest] bm.dmwx matches 2 run ' + dsay('THUNDER! Now the storm fights beside us!')])
    fn('p97/care', ['execute if entity @s[tag=bm.dmdc] run function bm:p97/duo_cecil',
                    'execute if entity @s[tag=bm.dmdk] run function bm:p97/duo_kw',
                    'execute if entity @s[tag=bm.dmdc,tag=bm.dmdk] as @a[tag=bm.dmown] run effect give @s minecraft:resistance 3 0 true',
                    'scoreboard players add @s bm.dmb 1', 'execute if score @s bm.dmb matches 100.. run function bm:p97/banter'])
    fn('p97/duo_cecil', ['execute as @a[tag=bm.dmown] run effect give @s minecraft:strength 3 0 true',
                         'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 3 0 true',
                         'execute store result score #r bm.rng run random value 1..12',
                         'execute if score #r bm.rng matches 1 run function bm:p97/glare',
                         'execute as @a[tag=bm.dmown] unless entity @s[advancements={bm:story/demo_cecil=true}] run function bm:p97/duo_cecil_first'])
    fn('p97/glare', face('glare', 30))
    fn('p97/duo_cecil_first', ['advancement grant @s only bm:story/demo_cecil',
                               tellraw('@s', PREFIX + [T('Old Rivals! ', STORM, bold=True), T('Democratus and Cecil each mean to outdo the other: you hit harder, Cecil is tougher, and Democratus charges twice as fast.', 'gray')]),
                               tellraw('@s', [T('Cecil: ', '#b48cff', bold=True), T('"Oh. It\'s you. Still swinging that oversized gardening tool, old man?"', '#e8d8ff')]),
                               tellraw('@s', [T('Democratus: ', STORM, bold=True), T('"Still playing with sparks, boy? Stay out of my way."', STORM_LT)])])
    fn('p97/duo_kw', ['execute as @a[tag=bm.dmown] run effect give @s minecraft:speed 3 0 true', 'execute as @a[tag=bm.dmown] run effect give @s minecraft:jump_boost 3 0 true',
                      'execute as @e[type=minecraft:wolf,tag=bm.kxpet,distance=..16] if score @s bm.pid = #me bm.pid run function bm:p97/heir',
                      'execute unless predicate bm:p97/regen run effect give @s minecraft:regeneration 5 0 true',
                      'execute as @a[tag=bm.dmown] unless entity @s[advancements={bm:story/demo_kw=true}] run function bm:p97/duo_kw_first'])
    fn('p97/heir', ['effect give @s minecraft:resistance 3 0 true', 'scoreboard players add @s bm.kxch 1'])
    fn('p97/duo_kw_first', ['advancement grant @s only bm:story/demo_kw',
                            tellraw('@s', PREFIX + [T("The Storm's Heir! ", STORM, bold=True), T('Democratus walks beside what came after him: his gem, his storm - and none of his conscience. You\'re quicker, KillerWatt is tougher and charges faster, and Democratus heals.', 'gray')]),
                            tellraw('@s', [T('Democratus: ', STORM, bold=True), T('"So this is my anger, with nothing left to answer to. ...Stay where I can see you."', STORM_LT)]),
                            tellraw('@s', [T('KillerWatt: ', '#74d462', bold=True), T('*the shard on his chest - cut from Democratus\'s own scythe - flares at its old master*', '#c8f0c0', italic=True)])])
    BANTER = [('cecil', [('Democratus', 'Your robe is smouldering again, boy.', 'Cecil', 'It is SUPPOSED to do that.'),
                         ('Cecil', 'I could have handled that one alone.', 'Democratus', 'Slowly. I was there first.'),
                         ('Democratus', 'When I was your age I reaped storms, not chickens.', 'Cecil', 'When you were my age storms were still being invented.')]),
              ('kw', [('Democratus', 'That shard was cut from my scythe. It was never meant to sit in something like you.', 'KillerWatt', '*he taps the gem with one claw, slowly - and grins*'),
                      ('KillerWatt', '*thunder rolls from somewhere deep in his chest - it sounds like laughter*', 'Democratus', 'Laugh. I had reasons. You only have appetite.'),
                      ('Democratus', 'I wanted the crown set right. You only want to wear the people under it.', 'KillerWatt', '*sparks lick a passing beetle until it walks like a puppet*')])]
    who = {'Democratus': (STORM, STORM_LT), 'Cecil': ('#b48cff', '#e8d8ff'), 'KillerWatt': ('#74d462', '#c8f0c0')}
    line = lambda n, txt: tellraw('@a[tag=bm.dmown]', [T(f'{n}: ', who[n][0], bold=True), T(txt if n == 'KillerWatt' else f'"{txt}"', who[n][1], italic=n == 'KillerWatt')])
    bl = ['scoreboard players set @s bm.dmb 0', 'execute store result score #r bm.rng run random value 1..6']
    n = 0
    for k, lst in BANTER:
        for a, ta, b, tb in lst:
            n += 1
            fn(f'p97/banter_{n}', [line(a, ta), line(b, tb)] + face('smirk', 40))
            bl.append(f'execute if score #r bm.rng matches {n} if entity @s[tag={"bm.dmdc" if k == "cecil" else "bm.dmdk"}] run function bm:p97/banter_{n}')
    fn('p97/banter', bl)

    # ================================================================== his raid contract (Goldtooth: 1 trophy + 6 medallions)
    def signed():
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    fn('p97/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                    'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return run ' + say('Democratus is already under contract.', 'gray'),
        f'scoreboard players add @s bm.fcon {BIT}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_demo"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T('Democratus', STORM, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p97/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T('Democratus', STORM), T(' needs a ', 'gray'), T('Raid Contract', '#ffcf40'), T(' to come into the vault. Goldtooth sells them.', 'gray')]), 'return 0'])
    import phase70 as P70
    from gen_dp import offer
    prev = P70.goldtooth
    def g97():
        d = prev()
        d['Offers']['Recipes'].append(offer(('gutter_trophy', 1), ('fcontract_demo', 1), ('gutter_medallion', 6)))
        return d
    P70.goldtooth = g97
    L = G.FUNCS['p70/r/lobby/init']
    L[:] = [l.replace(snbt(prev()), snbt(g97())) if 'bm.gvgt' in l and 'summon minecraft:villager' in l else l for l in L]
    assert any(snbt(g97()) in l for l in L), "Goldtooth's summon wasn't found to add Democratus' contract"

    # ================================================================== THE STORM VIGIL: rare, in a thunderstorm, out under the sky
    second += ['execute if score #dmec bm.dmw matches 1.. run scoreboard players remove #dmec bm.dmw 1',
               'execute if predicate bm:p79/thunder unless score #dmec bm.dmw matches 1.. as @a[gamemode=!spectator] at @s if dimension minecraft:overworld '
               'if predicate bm:sees_sky run function bm:p97/enc/roll']
    fn('p97/enc/roll', ['execute store result score #r bm.rng run random value 1..1500', 'execute unless score #r bm.rng matches 1 run return 0',
                        f'execute if items entity @s container.* {holds} run return 0',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.dmenc,distance=..160] run return 0',
                        'execute store result storage bm:tmp dme.a int 1 run random value 0..359', 'function bm:p97/enc/place with storage bm:tmp dme'])
    fn('p97/enc/place', ['$execute rotated $(a) 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves unless block ~ ~-1 ~ minecraft:water '
                         'unless block ~ ~-1 ~ minecraft:lava unless block ~ ~-1 ~ #minecraft:leaves run function bm:p97/enc/spawn'])
    enc_hit = snbt({'Tags': ['bm.dmenc', 'bm.dmnew'], 'width': F(1.3), 'height': F(1.6), 'response': B(1)})
    fn('p97/enc/spawn', ['scoreboard players set #dmec bm.dmw 1200', f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + rig +
       ['tag @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] add bm.dmencp',
        'execute as @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] run tag @s add bm.dmsel',
        'execute facing entity @p feet rotated ~ 0 run function bm:p97/place',
        'function bm:p97/grow', 'function bm:p97/pose/kneel', 'tag @e[tag=bm.dmsel] remove bm.dmsel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.dmnew,distance=..1] bm.dmf 0',
        'tag @e[tag=bm.dmnew,distance=..1] remove bm.dmnew',
        'particle minecraft:flash{color:[0.75,1.0,0.7,1.0]} ~ ~2 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~8 ~ 0.1 8 0.1 0 120',
        'particle minecraft:electric_spark ~ ~1 ~ 1 1.5 1 0.3 120',
        'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..96] ~ ~ ~ 2 0.8', 'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..48] ~ ~ ~ 1 0.7',
        tellraw('@a[distance=..48]', PREFIX + [T('Lightning strikes close by. Where it fell, a hooded figure kneels in vigil beside a great scythe...', 'gray', italic=True)])])
    fn('p97/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.dmencp,distance=..3]', 'particle minecraft:flash{color:[0.75,1.0,0.7,1.0]} ~ ~1 ~ 0 0 0 0 1',
                        'particle minecraft:electric_spark ~ ~1 ~ 0.6 1 0.6 0.3 60', 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..64] ~ ~ ~ 1 1.2', 'kill @s'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.dmenc] at @s run function bm:p97/enc/sec')
    fn('p97/enc/sec', ['execute unless predicate bm:p79/thunder run return run function bm:p97/enc/gone',
                       'execute unless entity @a[distance=..96] run return run function bm:p97/enc/gone'])
    # his vigil: still as stone, a breath now and then, sparks crawling on the crystal; his eyes find whoever comes close
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.dmenc] at @s run function bm:p97/enc/tick')
    fn('p97/enc/tick', ['scoreboard players add @s bm.dmf 1', 'scoreboard players operation #f bm.rng = @s bm.dmf', 'scoreboard players operation #f bm.rng %= #120 bm.rng',
                        'execute as @e[type=minecraft:item_display,tag=bm.dmencp,distance=..2] run tag @s add bm.dmsel',
                        'execute if score #f bm.rng matches 0 run function bm:p97/pose/kneel', 'execute if score #f bm.rng matches 60 run function bm:p97/pose/kneel_b',
                        'execute if score #f bm.rng matches 0 if entity @a[distance=..10,gamemode=!spectator] facing entity @p[distance=..10,gamemode=!spectator] feet rotated ~ 0 run function bm:p97/place',
                        'execute if score #f bm.rng matches 0 run particle minecraft:electric_spark ~0.3 ~2.6 ~0.3 0.2 0.4 0.2 0.05 6',
                        'execute if score #f bm.rng matches 30 run particle minecraft:electric_spark ~0.3 ~2.6 ~0.3 0.2 0.4 0.2 0.05 4',
                        'tag @e[tag=bm.dmsel] remove bm.dmsel'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.dmenc] if data entity @s interaction at @s run function bm:p97/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.dmenc] if data entity @s attack at @s run function bm:p97/enc/poke']
    fn('p97/enc/click', ['tag @s add bm.dmhere', 'execute on target run function bm:p97/enc/talk', 'tag @s remove bm.dmhere', 'data remove entity @s interaction'])
    fn('p97/enc/poke', ['execute on attacker run ' + dsay("You strike a kneeling man? ...Hah. You have nerve. Walk with me first - then I'll show you a real fight."),
                        'data remove entity @s attack'])
    fn('p97/enc/talk', [f'execute if items entity @s container.* {holds} run return run ' + dsay('We have an accord already. Call, and I will come.'),
                        dchat('You walk out into the storm, and you do not run from it. Good.'),
                        dchat('I am Democratus. I have reaped storms older than your kingdoms. Walk with me - and when you want to know how strong you really are, ask.'),
                        tellraw('@s', PREFIX + [T('Democratus joins you! ', STORM, bold=True),
                                                T('He gives you his Storm Seal: use it to call him; sneak + use for his challenge - a duel.', 'gray')]),
                        give('demo_seal'), 'advancement grant @s only bm:story/demo_friend', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.9',
                        'execute as @e[type=minecraft:interaction,tag=bm.dmhere,limit=1] at @s run function bm:p97/enc/gone',
                        'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                        f'{sel_pet} run tag @s add bm.dmsel2', 'execute unless entity @e[type=minecraft:wolf,tag=bm.dmsel2] run function bm:p97/summon',
                        'tag @e[tag=bm.dmsel2] remove bm.dmsel2'])

    # ================================================================== THE DUEL
    # (as the challenger) he steps out - from your side if he's with you - and squares up; 10 s to get clear, then he comes for you
    boss = {'Tags': ['bm.dmboss', 'bm.dmbnew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'NoAI': B(1), 'Invulnerable': B(1),
            'Health': F(DUEL_HP), 'CustomName': T('Democratus', STORM, bold=True), 'CustomNameVisible': B(0), 'DeathLootTable': 'minecraft:empty',
            'CanPickUpLoot': B(0), 'attributes': [{'id': 'minecraft:max_health', 'base': D(DUEL_HP)}, {'id': 'minecraft:armor', 'base': D(14)},
                                                  {'id': 'minecraft:armor_toughness', 'base': D(6)}, {'id': 'minecraft:knockback_resistance', 'base': D(0.85)},
                                                  {'id': 'minecraft:movement_speed', 'base': D(0.3)}, {'id': 'minecraft:follow_range', 'base': D(48)},
                                                  {'id': 'minecraft:attack_damage', 'base': D(3)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
            'drop_chances': {k: F(0) for k in ('head', 'chest', 'legs', 'feet', 'mainhand', 'offhand')}}
    fn('p97/duel/start', ['execute if entity @s[tag=bm.dmduel] run return run ' + say('You are already dueling him.'),
                          'execute if dimension bm:gutter run return run ' + say('Not in the vault. Find open ground.'),
                          'execute if entity @e[type=minecraft:vindicator,tag=bm.dmboss,distance=..96] run return run ' + say('Someone is already dueling Democratus here.'),
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                          f'{sel_pet} run tag @s add bm.dmsel2',
                          'execute as @e[type=minecraft:wolf,tag=bm.dmsel2,limit=1] at @s run function bm:p97/duel/spawn',
                          'execute unless entity @e[type=minecraft:wolf,tag=bm.dmsel2] rotated ~ 0 positioned ^ ^ ^5 run function bm:p97/duel/spawn',
                          'execute as @e[type=minecraft:wolf,tag=bm.dmsel2] at @s run function bm:p97/duel/stand_down',
                          'tag @e[tag=bm.dmsel2] remove bm.dmsel2',
                          'tag @s add bm.dmduel', 'scoreboard players set @s bm.dmd 200', 'scoreboard players operation @s bm.dmdn = @s bm.dmdth',
                          'bossbar set bm:dmb players @a[tag=bm.dmduel]', f'bossbar set bm:dmb value {DUEL_HP}', 'bossbar set bm:dmb visible true',
                          dchat('Ha! Good. Ten breaths - put some ground between us. Then the storm comes for you.'),
                          'playsound minecraft:event.raid.horn neutral @s ~ ~ ~ 0.7 1.4'])
    # (the follower, quietly away - no faint, no wait: he's the one across from you now)
    fn('p97/duel/stand_down', ['execute on passengers run kill @s', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s',
                               'execute as @e[type=minecraft:item_display,tag=bm.dmp,tag=!bm.dmencp,tag=!bm.dmbp] if score @s bm.pid = #me bm.pid run kill @s'])
    fn('p97/duel/spawn', [f'summon minecraft:vindicator ~ ~ ~ {snbt(boss)}',
                          'scoreboard players operation @e[type=minecraft:vindicator,tag=bm.dmbnew,limit=1,sort=nearest] bm.pid = #me bm.pid',
                          'scoreboard players set @e[type=minecraft:vindicator,tag=bm.dmbnew,limit=1,sort=nearest] bm.dms -1',
                          'scoreboard players set @e[type=minecraft:vindicator,tag=bm.dmbnew,limit=1,sort=nearest] bm.dmdb 20',
                          'scoreboard players set @e[type=minecraft:vindicator,tag=bm.dmbnew,limit=1,sort=nearest] bm.dmch 0'] + rig +
       ['tag @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] add bm.dmbp',
        'scoreboard players operation @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] bm.pid = #me bm.pid',
        'execute as @e[type=minecraft:item_display,tag=bm.dmnew,distance=..1] run tag @s add bm.dmsel',
        'execute facing entity @p feet rotated ~ 0 run function bm:p97/place', 'function bm:p97/grow', 'function bm:p97/pose/plant',
        'function bm:p97/head {e:"serious"}',
        'tag @e[tag=bm.dmsel] remove bm.dmsel', 'tag @e[tag=bm.dmnew,distance=..1] remove bm.dmnew', 'tag @e[tag=bm.dmbnew] remove bm.dmbnew'])
    # ---- the countdown and the stakes (as each challenger, every tick)
    tick.append('execute as @a[tag=bm.dmduel] at @s run function bm:p97/duel/you')
    fn('p97/duel/you', ['scoreboard players operation #me bm.pid = @s bm.pid',
                        'execute if score @s bm.dmd matches 1.. run function bm:p97/duel/count',
                        'execute unless score @s bm.dmd matches 1.. unless entity @e[type=minecraft:vindicator,tag=bm.dmboss,distance=..64] run return run function bm:p97/duel/lose',
                        'execute unless score @s bm.dmd matches 1.. unless score @s bm.dmdth = @s bm.dmdn run return run function bm:p97/duel/lose',
                        'execute store result score #ph bm.rng run data get entity @s Health',
                        'execute unless score @s bm.dmd matches 1.. if score #ph bm.rng matches ..6 run return run function bm:p97/duel/lose'])
    fn('p97/duel/count', ['scoreboard players remove @s bm.dmd 1', 'scoreboard players operation #c bm.rng = @s bm.dmd', 'scoreboard players operation #c bm.rng %= #20 bm.rng',
                          'execute if score #c bm.rng matches 0 if score @s bm.dmd matches 20.. run function bm:p97/duel/num',
                          'execute if score @s bm.dmd matches 0 run function bm:p97/duel/fight'])
    fn('p97/duel/num', ['scoreboard players operation #n bm.rng = @s bm.dmd', 'scoreboard players operation #n bm.rng /= #20 bm.rng',
                        'title @s times 0 18 4', title('@s', 'title', [{'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True}]),
                        'playsound minecraft:block.note_block.hat player @s ~ ~ ~ 1 0.8'])
    fn('p97/duel/fight', ['title @s times 0 30 10', title('@s', 'title', T('FIGHT!', '#ff5a3a', bold=True)),
                          title('@s', 'subtitle', T('Democratus comes for you', STORM)),
                          'playsound minecraft:entity.lightning_bolt.thunder player @s ~ ~ ~ 1 0.9',
                          'execute as @e[type=minecraft:vindicator,tag=bm.dmboss,distance=..96] if score @s bm.pid = #me bm.pid run data merge entity @s {NoAI:0b,Invulnerable:0b}'])
    fn('p97/duel/lose', ['tag @s remove bm.dmduel', 'scoreboard players set @s bm.dmd 0', 'effect clear @s minecraft:levitation',
                         'execute if score #ph bm.rng matches 1.. run effect give @s minecraft:regeneration 8 1 true',
                         'execute as @e[type=minecraft:vindicator,tag=bm.dmboss] if score @s bm.pid = #me bm.pid at @s run function bm:p97/duel/leave',
                         'execute unless entity @a[tag=bm.dmduel] run bossbar set bm:dmb visible false',
                         'title @s times 5 50 15', title('@s', 'title', T('Defeated', '#ff5a3a', bold=True)),
                         dchat('Enough. You fought - but the storm is not yours. Not yet. Call me when you are ready to try again.'),
                         tellraw('@s', PREFIX + [T('You lost the duel. ', 'gray'), T('Democratus went home - use the seal to call him again, and challenge him whenever you like.', 'dark_gray')])])
    fn('p97/duel/leave', ['execute as @e[type=minecraft:item_display,tag=bm.dmbp] if score @s bm.pid = #me bm.pid run kill @s',
                          'particle minecraft:flash{color:[0.75,1.0,0.7,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:electric_spark ~ ~1 ~ 0.6 1 0.6 0.3 60',
                          'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..48] ~ ~ ~ 0.8 1.3',
                          'tp @s ~ -500 ~', 'kill @s'])
    # ---- the duelist: every tick
    tick.append('execute as @e[type=minecraft:vindicator,tag=bm.dmboss] at @s run function bm:p97/duel/tick')
    fn('p97/duel/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:item_display,tag=bm.dmbp] if score @s bm.pid = #me bm.pid run tag @s add bm.dmsel',
                         'execute as @a[tag=bm.dmduel] if score @s bm.pid = #me bm.pid run tag @s add bm.dmfoe',
                         'execute unless entity @a[tag=bm.dmfoe] unless entity @s[tag=bm.dmyield] run return run function bm:p97/duel/orphan',
                         'execute if score @s bm.dmk matches 1.. run function bm:p97/duel/act_tick',
                         'execute unless entity @s[tag=bm.dmyield] store result score #h bm.rng run data get entity @s Health',
                         f'execute unless entity @s[tag=bm.dmyield] if score #h bm.rng matches ..{DUEL_YIELD} run function bm:p97/duel/win',
                         'execute if score @s bm.dmdb matches 1.. run scoreboard players remove @s bm.dmdb 1',
                         'execute unless entity @s[tag=bm.dmyield] unless score @s bm.dmk matches 1.. unless score @s bm.dmdb matches 1.. unless entity @a[tag=bm.dmfoe,scores={bm.dmd=1..}] run function bm:p97/duel/mind',
                         'function bm:p97/duel/state', 'function bm:p97/frame',
                         'execute if score @s bm.dms matches 8 if score @s bm.dmf matches ..30 run function bm:p97/spin',
                         'execute unless score @s bm.dms matches 8 if entity @a[tag=bm.dmfoe] facing entity @a[tag=bm.dmfoe,limit=1] feet rotated ~ 0 run function bm:p97/place',
                         'execute if score @s bm.dms matches 8 unless score @s bm.dmf matches ..30 facing entity @a[tag=bm.dmfoe,limit=1] feet rotated ~ 0 run function bm:p97/place',
                         'tag @a[tag=bm.dmfoe] remove bm.dmfoe', 'tag @e[tag=bm.dmsel] remove bm.dmsel'])
    fn('p97/duel/state', ['execute if entity @s[tag=bm.dmyield] run return run scoreboard players set #st bm.rng 12',
                          'execute if score @s bm.dmk matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.dma',
                          'execute if entity @a[tag=bm.dmfoe,scores={bm.dmd=1..}] run return run scoreboard players set #st bm.rng 13',
                          'function bm:p97/move'])
    fn('p97/duel/orphan', ['function bm:p97/duel/leave'])
    fn('p97/duel/wx', ['scoreboard players set @s bm.dmwx 0',
                       'execute if predicate bm:p97/rain positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set @s bm.dmwx 1',
                       'execute if predicate bm:p79/thunder positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set @s bm.dmwx 2',
                       'execute if score @s bm.dmwx matches 1 unless entity @s[tag=bm.dmyield] run effect give @s minecraft:resistance 3 0 true',
                       'execute if score @s bm.dmwx matches 2 unless entity @s[tag=bm.dmyield] run effect give @s minecraft:resistance 3 1 true',
                       'execute if score @s bm.dmwx matches 2 run particle minecraft:electric_spark ~ ~1.6 ~ 0.5 0.9 0.5 0.15 10'])
    # the mind: close - the sweep; a little way off - the lunge or the lightning; far - the lightning; every fifth (or at half
    # health, once) - the Storm Reap
    fn('p97/duel/mind', ['scoreboard players add @s bm.dmch 1',
                         'execute store result score #h bm.rng run data get entity @s Health',
                         f'execute unless entity @s[tag=bm.dmhalf] if score #h bm.rng matches ..{DUEL_HP // 2} if entity @a[tag=bm.dmfoe,distance=..9] run return run function bm:p97/duel/reap_first',
                         'execute if score @s bm.dmch matches 5.. if entity @a[tag=bm.dmfoe,distance=..9] run return run function bm:p97/duel/reap_go',
                         'execute if entity @a[tag=bm.dmfoe,distance=..4.6] run return run function bm:p97/duel/swing_go',
                         'execute store result score #r bm.rng run random value 1..10',
                         'execute if entity @a[tag=bm.dmfoe,distance=..14] if score #r bm.rng matches 1..6 run return run function bm:p97/duel/lunge_go',
                         'execute if entity @a[tag=bm.dmfoe,distance=..40] run return run function bm:p97/duel/call_go',
                         'scoreboard players set @s bm.dmdb 10'])
    fn('p97/duel/swing_go', ['scoreboard players set @s bm.dmk 24', 'scoreboard players set @s bm.dma 7', 'scoreboard players set @s bm.dmdb 26',
                             'playsound minecraft:item.trident.riptide_1 hostile @a[distance=..20] ~ ~ ~ 0.7 0.6'])
    fn('p97/duel/lunge_go', ['scoreboard players set @s bm.dmk 22', 'scoreboard players set @s bm.dma 11', 'scoreboard players set @s bm.dmdb 30',
                             'playsound minecraft:entity.breeze.jump hostile @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p97/duel/call_go', ['scoreboard players set @s bm.dmk 36', 'scoreboard players set @s bm.dma 9', 'scoreboard players set @s bm.dmdb 34',
                            'playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..48] ~ ~ ~ 0.8 0.7'])
    fn('p97/duel/reap_first', ['tag @s add bm.dmhalf', dchat('Hah! You draw blood. Then see the storm!', '@a[tag=bm.dmfoe]'), 'function bm:p97/duel/reap_go'])
    fn('p97/duel/reap_go', ['scoreboard players set @s bm.dmk 60', 'scoreboard players set @s bm.dma 8', 'scoreboard players set @s bm.dmdb 40', 'scoreboard players set @s bm.dmch 0',
                            'playsound minecraft:block.beacon.power_select hostile @a[distance=..32] ~ ~ ~ 1 0.6',
                            'playsound minecraft:item.trident.riptide_3 hostile @a[distance=..32] ~ ~ ~ 1 0.7'])
    bme = '@e[type=minecraft:vindicator,tag=bm.dmme,limit=1]'
    fn('p97/duel/act_tick', wx + ['scoreboard players remove @s bm.dmk 1', 'tag @s add bm.dmme',
                             # the sweep: the blow lands 14 ticks in
                             'execute if score @s bm.dma matches 7 if score @s bm.dmk matches 10 run function bm:p97/duel/sweep',
                             # the lunge: 8 ticks of a charge at you, then the sweep
                             'execute if score @s bm.dma matches 11 if score @s bm.dmk matches 15..22 facing entity @a[tag=bm.dmfoe,limit=1] feet rotated ~ 0 positioned ^ ^ ^0.8 '
                             'if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless entity @a[tag=bm.dmfoe,distance=..2.5] run tp @s ~ ~ ~',
                             'execute if score @s bm.dma matches 11 if score @s bm.dmk matches 15..22 run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.1 4',
                             'execute if score @s bm.dma matches 11 if score @s bm.dmk matches 8 run function bm:p97/duel/sweep',
                             # the lightning: three marks, one under you - then they're struck
                             'execute if score @s bm.dma matches 9 if score @s bm.dmk matches 34 at @a[tag=bm.dmfoe,limit=1] run function bm:p97/duel/marks',
                             'execute if score @s bm.dma matches 9 if score @s bm.dmk matches 11..33 as @e[type=minecraft:marker,tag=bm.dmmark] at @s run particle minecraft:electric_spark ~ ~0.2 ~ 0.8 0 0.8 0 3',
                             'execute if score @s bm.dma matches 9 if score @s bm.dmk matches 10 as @e[type=minecraft:marker,tag=bm.dmmark] at @s run function bm:p97/duel/strike',
                             # the Storm Reap: you're lifted, struck, slammed
                             'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 56 as @a[tag=bm.dmfoe,distance=..8] run effect give @s minecraft:levitation 1 3 true',
                             'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 56 run particle minecraft:sweep_attack ~ ~1 ~ 2.4 0.2 2.4 0 10',
                             'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 36 at @a[tag=bm.dmfoe,limit=1] run function bm:p97/duel/strike',
                             'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 14 run function bm:p97/duel/slam',
                             'execute if score @s bm.dma matches 8 if score @s bm.dmk matches 34..58 run particle minecraft:electric_spark ~ ~1.4 ~ 1.6 0.3 1.6 0.1 6',
                             # the end of a duel he lost: he's gone, the prize is yours
                             'execute if score @s bm.dma matches 12 if score @s bm.dmk matches 0 run function bm:p97/duel/reward',
                             'tag @s remove bm.dmme'])
    fn('p97/duel/sweep', ['playsound minecraft:entity.player.attack.sweep hostile @a[distance=..24] ~ ~ ~ 1 0.5', 'particle minecraft:sweep_attack ^ ^1.2 ^2 1.2 0.3 1.2 0 6',
                          *[f'execute if score #dmwx bm.rng matches {w} positioned ^ ^ ^1.8 as @a[tag=bm.dmfoe,distance=..3.4] run damage @s {d} minecraft:mob_attack by {bme}' for w, d in WX_DSWEEP],
                          'execute positioned ^ ^ ^1.8 as @a[tag=bm.dmfoe,distance=..3.4] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 20'])
    fn('p97/duel/marks', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.dmmark"]}',
                          'execute store result storage bm:tmp dmm.x int 1 run random value -4..4', 'execute store result storage bm:tmp dmm.z int 1 run random value -4..4',
                          'function bm:p97/duel/mark with storage bm:tmp dmm',
                          'execute store result storage bm:tmp dmm.x int 1 run random value -4..4', 'execute store result storage bm:tmp dmm.z int 1 run random value -4..4',
                          'function bm:p97/duel/mark with storage bm:tmp dmm'])
    fn('p97/duel/mark', ['$summon minecraft:marker ~$(x) ~ ~$(z) {Tags:["bm.dmmark"]}'])
    fn('p97/duel/strike', ['particle minecraft:flash{color:[0.75,1.0,0.7,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~6 ~ 0.05 6 0.05 0 60',
                           'particle minecraft:electric_spark ~ ~0.5 ~ 0.8 0.6 0.8 0.3 40',
                           'playsound minecraft:entity.lightning_bolt.impact hostile @a[distance=..40] ~ ~ ~ 1 1.0',
                           *[f'execute if score #dmwx bm.rng matches {w} as @a[tag=bm.dmfoe,distance=..2.2] run damage @s {d} minecraft:lightning_bolt by {bme}' for w, d in WX_DBOLT],
                           'kill @s[type=minecraft:marker]'])
    fn('p97/duel/slam', ['function bm:p97/thud',
                         'execute as @a[tag=bm.dmfoe,distance=..6] run effect clear @s minecraft:levitation',
                         *[f'execute if score #dmwx bm.rng matches {w} as @a[tag=bm.dmfoe,distance=..6] run damage @s {d} minecraft:mob_attack by {bme}' for w, d in WX_DSLAM],
                         'execute as @a[tag=bm.dmfoe,distance=..6] run effect give @s minecraft:slowness 3 1 true'])
    # ---- he yields (brought to his knee - he can't be killed outright): the prize, his respect, and he goes home
    fn('p97/duel/win', ['tag @s add bm.dmyield', 'data merge entity @s {NoAI:1b,Invulnerable:1b}', 'effect clear @a[tag=bm.dmfoe] minecraft:levitation',
                        'scoreboard players set @s bm.dmk 70', 'scoreboard players set @s bm.dma 12', 'function bm:p97/head {e:"hurt"}',
                        'kill @e[type=minecraft:marker,tag=bm.dmmark]',
                        'playsound minecraft:entity.lightning_bolt.thunder hostile @a[distance=..64] ~ ~ ~ 1 0.6',
                        dchat('...Hah. Hah! Enough - enough. The storm bends to you.', '@a[tag=bm.dmfoe]'),
                        'title @a[tag=bm.dmfoe] times 5 60 15', title('@a[tag=bm.dmfoe]', 'title', T('Victory', GOLD, bold=True)),
                        title('@a[tag=bm.dmfoe]', 'subtitle', T('Democratus yields', STORM))])
    fn('p97/duel/reward', ['execute as @a[tag=bm.dmfoe] at @s run function bm:p97/duel/prize', 'function bm:p97/duel/leave'])
    fn('p97/duel/prize', ['tag @s remove bm.dmduel', 'scoreboard players set @s bm.dmd 0', 'execute unless entity @a[tag=bm.dmduel] run bossbar set bm:dmb visible false',
                          'execute if score @s bm.dmsc matches 1.. run return run ' +
                          dchat('You have my scythe already, and now my respect twice over. Call me - the storm is ours.'),
                          'scoreboard players set @s bm.dmsc 1', give('demo_scythe'), 'advancement grant @s only bm:story/demo_duel',
                          dchat('Take it. My scythe, freely given - you earned it. Swing it like you mean it.'),
                          tellraw('@s', PREFIX + [T("Democratus' Scythe is yours! ", STORM, bold=True),
                                                  T('Every blow arcs lightning and charges it; at eight, a Storm Reap. He went home - call him with the seal.', 'gray')]),
                          'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.8'])
    # (every second) the bar
    second += ['execute as @e[type=minecraft:vindicator,tag=bm.dmboss] at @s run function bm:p97/duel/wx',
               f'execute as @e[type=minecraft:vindicator,tag=bm.dmboss,limit=1] store result bossbar bm:dmb value run data get entity @s Health',
               'execute unless entity @e[type=minecraft:vindicator,tag=bm.dmboss] run bossbar set bm:dmb visible false',
               'kill @e[type=minecraft:marker,tag=bm.dmmark,tag=bm.dmold]', 'tag @e[type=minecraft:marker,tag=bm.dmmark] add bm.dmold']

    # ================================================================== HIS SCYTHE: lightning arcs, a charge, a Storm Reap of your own
    wjson('bm/enchantment/storm_reap.json', {'anvil_cost': 8, 'description': T('Storm Reap', STORM), 'max_level': 1, 'weight': 1,
                                             'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
                                             'slots': ['mainhand'], 'supported_items': TOTEM,
                                             'effects': {'minecraft:post_attack': [{'affected': 'victim', 'enchanted': 'attacker',
                                                                                     'effect': {'type': 'minecraft:run_function', 'function': 'bm:p97/scy/hit'}}]}})
    pfoe = f'{foe},tag=!bm.frogpet'                       # (the allies pass makes this skip every follower)
    fn('p97/scy/hit', ['execute on attacker if entity @s[type=minecraft:player] run tag @s add bm.dmswing',
                       'execute unless entity @a[tag=bm.dmswing] run return 0',
                       'tag @s add bm.dmvic', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 14',
                       'playsound minecraft:entity.lightning_bolt.impact player @a[distance=..16] ~ ~ ~ 0.3 1.8',
                       f'execute as @e[{pfoe},distance=0.5..4.5,tag=!bm.dmvic,sort=nearest,limit=2] at @s run function bm:p97/scy/arc',
                       'tag @s remove bm.dmvic',
                       'execute as @a[tag=bm.dmswing] run function bm:p97/scy/charge',
                       'tag @a[tag=bm.dmswing] remove bm.dmswing'])
    fn('p97/scy/arc', ['damage @s 4 minecraft:lightning_bolt by @a[tag=bm.dmswing,limit=1]', 'particle minecraft:electric_spark ~ ~1 ~ 0.2 0.4 0.2 0.1 10',
                       'particle minecraft:end_rod ~ ~1 ~ 0.1 0.3 0.1 0.02 4'])
    fn('p97/scy/charge', ['execute if score @s bm.dmsrt matches 1.. run return 0', 'scoreboard players add @s bm.dmsch 1',
                          f'execute if score @s bm.dmsch matches {SCY_CHARGE}.. at @s run return run function bm:p97/scy/reap_go'] +
       [f'execute if score @s bm.dmsch matches {i} run ' + title('@s', 'actionbar', [T('Storm charge ', STORM), T('|' * i, GOLD, bold=True), T('|' * (SCY_CHARGE - i), 'dark_gray', bold=True)])
        for i in range(1, SCY_CHARGE)])
    fn('p97/scy/reap_go', ['scoreboard players set @s bm.dmsch 0', 'scoreboard players set @s bm.dmsrt 40', 'tag @s add bm.dmsrme',
                           f'execute as @e[{pfoe},distance=..6] run tag @s add bm.dmsreap', 'effect give @e[tag=bm.dmsreap,distance=..7] minecraft:levitation 2 1 true',
                           'particle minecraft:sweep_attack ~ ~1 ~ 2.4 0.2 2.4 0 12', 'playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1 0.6',
                           'playsound minecraft:entity.breeze.wind_burst player @a[distance=..24] ~ ~ ~ 1 0.7',
                           title('@s', 'actionbar', T('STORM REAP!', GOLD, bold=True)), 'tag @s remove bm.dmsrme'])
    tick.append('execute as @a[scores={bm.dmsrt=1..}] at @s run function bm:p97/scy/reap_tick')
    fn('p97/scy/reap_tick', ['scoreboard players remove @s bm.dmsrt 1', 'tag @s add bm.dmsrme',
                             'execute if score @s bm.dmsrt matches 22 as @e[tag=bm.dmsreap,distance=..12] at @s run function bm:p97/scy/bolt',
                             'execute if score @s bm.dmsrt matches 4 as @e[tag=bm.dmsreap,distance=..12] at @s run function bm:p97/scy/slam',
                             'execute if score @s bm.dmsrt matches 4 run function bm:p97/thud',
                             'execute if score @s bm.dmsrt matches 4 run tag @e[tag=bm.dmsreap] remove bm.dmsreap',
                             'tag @s remove bm.dmsrme'])
    fn('p97/scy/bolt', ['damage @s 8 minecraft:lightning_bolt by @a[tag=bm.dmsrme,limit=1]', 'particle minecraft:flash{color:[0.7,1.0,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1',
                        'particle minecraft:end_rod ~ ~3 ~ 0.05 2.5 0.05 0 20', 'playsound minecraft:entity.lightning_bolt.impact player @a[distance=..32] ~ ~ ~ 0.8 1.2'])
    fn('p97/scy/slam', ['effect clear @s minecraft:levitation', 'data modify entity @s Motion set value [0.0d,-2.4d,0.0d]',
                        'damage @s 10 minecraft:mob_attack by @a[tag=bm.dmsrme,limit=1]'])
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.mainhand {scythe_held} at @s run particle minecraft:electric_spark ~ ~1.2 ~ 0.4 0.5 0.4 0.02 1')

    # ================================================================== achievements, admin
    adv = lambda key, title_, desc, frame='goal', hidden=False, icon='bm:demo_seal': wjson(f'bm/advancement/story/{key}.json', {
        'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
        'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': icon}},
                    'title': T(title_, 'yellow'), 'description': T(desc, 'gray'), 'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': hidden}})
    adv('demo_friend', 'Eye of the Storm', 'Find Democratus keeping his vigil in a thunderstorm - and walk with him')
    adv('demo_cecil', 'Old Rivals', 'Have Democratus and Cecil at your side at once', 'task', True)
    adv('demo_kw', "The Storm's Heir", 'Have Democratus and KillerWatt at your side at once', 'task', True)
    adv('demo_duel', "Reaper's Due", 'Bring Democratus to his knee in a duel - and win his scythe', 'challenge', False, 'bm:demo_scythe')
    fn('admin/democratus', ['execute rotated ~ 0 positioned ^ ^ ^5 positioned over motion_blocking_no_leaves run function bm:p97/enc/spawn',
                            'scoreboard players set #dmec bm.dmw 0',
                            tellraw('@s', PREFIX + [T('Democratus kneels in front of you (he stays while it storms - /weather thunder). Right-click him.', 'gray')])])
    fn('admin/demo_seal', [give('demo_seal')])
    fn('admin/demo_scythe', [give('demo_scythe')])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/democratus', 'yellow'), T('  Democratus (storm vigil) in front of you', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/demo_seal', 'yellow'), T("  gives Democratus' Storm Seal", 'gray')]),
                              tellraw('@s', [T('/function bm:admin/demo_scythe', 'yellow'), T("  gives Democratus' Scythe", 'gray')])]
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.dmp]', 'kill @e[type=minecraft:interaction,tag=bm.dmenc]',
                                       'kill @e[type=minecraft:marker,tag=bm.dmmark]', 'execute as @e[type=minecraft:vindicator,tag=bm.dmboss] run tp @s ~ -500 ~',
                                       'bossbar remove bm:dmb']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
