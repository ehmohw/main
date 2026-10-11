"""2.67: Leo - a rare knight of the shore, with a trident.

- FINDING HIM: a small stone fort sometimes stands on a beach (sandy, snowy or stony shore). Leo keeps watch inside -
  the drowned have been coming up out of the surf at his walls all week. Talk to him; raise a sword (right-click him
  holding one) and he knows you'll stand with him: DEFEND THE FORT - three waves of drowned (the last with their
  Tidecaller) come up the beach. Stay within 32 blocks of the fort; if you all fall back, he holds the gate alone and
  you can try again. Win and he gives you LEO'S CREST, and the fort's chest is yours.
- THE CREST: use it to call him (and call him back). Sneak + use: send him home. 5 minutes if he faints.
- FIGHTING: up close he thrusts with the trident (9 damage, the blow carries a little sweep); at range (6-14) he throws
  it - it comes back to him (Loyalty), and in a thunderstorm it calls down the lightning (Channeling), never near you.
- STRONG BUT CARING: 50 health and good armour. When you drop to 4 hearts with a monster about, he's at your side:
  on guard, the monsters around you turn on HIM, you get Resistance II and some absorption (30 s to recover). While a
  fight is on and you're close: Resistance I. In the water with him: Water Breathing and Dolphin's Grace.
- WITH CELI ("Steel and Frost"): you get Strength; he covers her (Resistance); his thrusts freeze like her spear.
- WITH EMMA ("The Knight's Vow"): you regenerate; he shields her (Resistance II); his guard is back twice as fast.
- With both: Speed as well. They bicker (Celi) and cheer (Emma) - and he smiles.
- He animates: a watchful idle (an eye on the sea), a steady stride, a levelled charge, sitting, the salute when he
  arrives, the thrust, the throw, on guard; his face blinks and changes (phase95)."""
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import phase96_art as ART
import phase95 as FX
import phase72 as P72
import phase46 as P46
import phase89 as P89

PET_CD = 300
HP = 50
SEA = '#5ab8e0'
CREAM = '#e8f4ff'
SHORE = ['minecraft:beach', 'minecraft:snowy_beach', 'minecraft:stony_shore']

item('leo_crest', TOTEM, "Leo's Crest", SEA,
     ['A blue badge: a crescent, a drop of sea, a pink gem.', ('Use: call Leo (or call him back).', 'blue'), ('Sneak + use: send him home.', 'blue'),
      ('He thrusts and throws a trident;', 'blue'), ('he comes to your side when you\'re hurt.', 'blue'),
      ('Steel and Frost: with Celi. The Knight\'s Vow: with Emma.', 'gray'), ('If he faints: 5 minutes before he can return.', 'gray')],
     model='bm:leo_crest', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['leo_crest'] = 'bm:p96/use'
item('fcontract_leo', TOTEM, 'Raid Contract: Leo', SEA,
     ['Signed in gold ink, sealed in wax.', ('Use once: from then on Leo', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_leo'] = 'bm:p96/sign'
P72.KEEP.append('leo_crest')
P46.COMPANIONS += ',tag=!bm.leopet'               # (Cecil's spells pass him by, like the others)
BIT = 2 ** len(P89.BIT)
P89.BIT['leo'] = BIT                              # (admin/contracts_all signs him too)


def extend_offers(O, offer):
    pass                          # (found, never sold - only his raid contract, at Goldtooth)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(ART)
    for name, (tex, els) in ART.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('le_',)
    R.ICONS['leo_crest'] = ART.crest_icon(R)


def generate(G):
    import phase73 as P73
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    lesay = lambda txt, who='@s': title(who, 'actionbar', [T('Leo: ', SEA, bold=True), T(txt, CREAM)])
    lechat = lambda txt, who='@s': tellraw(who, [T('Leo: ', SEA, bold=True), T(f'"{txt}"', CREAM)])
    tick, fast, second = [], [], []
    objs = ['bm.les', 'bm.lef', 'bm.lecd', 'bm.lek', 'bm.lea', 'bm.lem', 'bm.let', 'bm.lez', 'bm.ler', 'bm.leq', 'bm.lel', 'bm.leg', 'bm.lesl',
            'bm.lew', 'bm.leb', 'bm.lefx', 'bm.fgo', 'bm.leph']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    holds = '*[minecraft:custom_data~{bm:"leo_crest"}]'
    S = ART.RIG_SCALE
    U = S / 16
    foe = 'type=#bm:hostile,tag=!bm.npc'
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.leopet] if score @s bm.pid = #me bm.pid'
    ident = [F(0), F(0), F(0), F(1)]
    qf = lambda q: [F(round(v, 4)) for v in q]
    face = lambda e, t: FX.face_cmd('leo', e, t)

    # ================================================================== the rig
    def part_nbt(p):
        return snbt({'Tags': ['bm.lep', f'bm.lp_{p}', 'bm.lenew'],
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:le_{p}'}},
                     'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(8), 'start_interpolation': Int(0),
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}})
    rig = [f'summon minecraft:item_display ~ ~ ~ {part_nbt(p)}' for p in ART.PARTS]
    def place_lines():
        out = []
        for p in ART.PARTS:
            x, y, z = ART.joint(p)
            out.append(f'execute positioned ^{-x * U:.4f} ^{y * U:.4f} ^{-z * U:.4f} run tp @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_{p}] ~ ~ ~ ~ 0')
        return out
    fn('p96/place', place_lines())
    fn('p96/grow', [f'execute as @e[type=minecraft:item_display,tag=bm.lesel] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}',
                    'execute at @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_body,limit=1] run function bm:p96/burst'])
    fn('p96/burst', ['particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 60', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.8 0.4 0.05 30',
                     'particle minecraft:end_rod ~ ~0.9 ~ 0.1 0.3 0.1 0.1 18', 'particle minecraft:dust{color:[0.35,0.72,0.9],scale:1.4} ~ ~0.9 ~ 0.4 0.7 0.4 0 24'])
    fn('p96/tri_off', [f'execute as @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_trident] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[0f,0f,0f]}}}}'])
    fn('p96/tri_on', [f'execute as @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_trident] run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{S}f,{S}f,{S}f]}}}}'])

    # ---- poses
    DUR = {'idle_a': 10, 'idle_b': 10, 'idle_look': 12, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 3,
           'sit_a': 6, 'sit_b': 6, 'salute': 5, 'thrust_back': 3, 'thrust': 2, 'throw_back': 4, 'throw': 2, 'guard': 4}
    def xf_nbt(pose, p):
        rot, tr = ART.part_xf(pose, p)
        return f'left_rotation:{snbt(qf(rot))},translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f]'
    for name, pose in ART.POSES.items():
        fn(f'p96/pose/{name}', [f'execute as @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_{p}] run data merge entity @s '
                                f'{{start_interpolation:0,interpolation_duration:{DUR[name]},transformation:{{{xf_nbt(pose, p)}}}}}' for p in ART.PARTS])
    # states: 0 idle (breathing, a look out to sea), 1 walk, 2 run, 3 air, 4 sit, 6 salute, 7 thrust, 8 throw, 9 guard
    CYCLE = {0: (120, [(0, 'idle_a'), (30, 'idle_b'), (60, 'idle_a'), (78, 'idle_look'), (104, 'idle_a')]),
             1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]),
             3: (None, [(0, 'jump')]), 4: (16, [(0, 'sit_a'), (8, 'sit_b')]), 6: (None, [(0, 'salute')]),
             7: (None, [(0, 'thrust_back'), (3, 'thrust')]), 8: (None, [(0, 'throw_back'), (6, 'throw')]), 9: (None, [(0, 'guard')])}
    anim = []
    for st, (period, frames) in CYCLE.items():
        lines = ['scoreboard players operation #f bm.rng = @s bm.lef']
        if period: lines.append(f'scoreboard players operation #f bm.rng %= #{period} bm.rng')
        lines += [f'execute if score #f bm.rng matches {t} run function bm:p96/pose/{p}' for t, p in frames]
        fn(f'p96/anim/{st}', lines)
        anim.append(f'execute if score @s bm.les matches {st} run return run function bm:p96/anim/{st}')
    fn('p96/anim', anim)
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in (12, 16, 120)]
    # (as the host) what he's doing now -> #st
    fn('p96/state', ['execute if score @s bm.lesl matches 1.. run return run scoreboard players set #st bm.rng 6',
                     'execute if score @s bm.lek matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.lea',
                     'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                     'execute store result score #og bm.rng run data get entity @s OnGround',
                     'execute if score #og bm.rng matches 0 run scoreboard players add @s bm.lez 1', 'execute if score #og bm.rng matches 1 run scoreboard players set @s bm.lez 0',
                     'execute if score @s bm.lez matches 3.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                     'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                     'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                     'scoreboard players operation #vx bm.rng += #vz bm.rng',
                     'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                     'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                     'scoreboard players set #st bm.rng 0'])
    # every tick, each Leo: his parts, his state and frames, where he stands and faces, his fighting
    tick.append('execute as @e[type=minecraft:wolf,tag=bm.leopet] at @s run function bm:p96/tick')
    fn('p96/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                    'execute as @e[type=minecraft:item_display,tag=bm.lep,tag=!bm.lefade] if score @s bm.pid = #me bm.pid run tag @s add bm.lesel',
                    'execute unless entity @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_trident] run function bm:p96/rerig',
                    'execute if score @s bm.lek matches 1.. run function bm:p96/act_tick',
                    'execute if score @s bm.lem matches 1.. run scoreboard players remove @s bm.lem 1',
                    'execute if score @s bm.let matches 1.. run scoreboard players remove @s bm.let 1',
                    'execute if score @s bm.ler matches 1.. run scoreboard players remove @s bm.ler 1',
                    'execute if score @s bm.ler matches 1 run function bm:p96/tri_on',
                    'execute if score @s bm.lesl matches 1.. run scoreboard players remove @s bm.lesl 1',
                    'execute if score @s bm.lesl matches 1 run function bm:p96/salute_end',
                    # his fights: a thrust at anything within reach, a throw at anything 6-14 away (once the trident's back)
                    f'execute unless score @s bm.lek matches 1.. unless score @s bm.lem matches 1.. unless score @s bm.ler matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=..3.2] run function bm:p96/thrust_go',
                    f'execute unless score @s bm.lek matches 1.. unless score @s bm.let matches 1.. unless score @s bm.ler matches 1.. unless data entity @s {{Sitting:1b}} '
                    f'unless entity @e[{foe},distance=..3.2] if entity @e[{foe},distance=6..14] run function bm:p96/throw_go',
                    'function bm:p96/state',
                    'execute if score #st bm.rng = @s bm.les run scoreboard players add @s bm.lef 1',
                    'execute unless score #st bm.rng = @s bm.les run scoreboard players set @s bm.lef 0',
                    'scoreboard players operation @s bm.les = #st bm.rng',
                    'function bm:p96/anim',
                    'execute on owner run tag @s add bm.leown',
                    # fighting: he faces his foe; on guard: away from you, toward the trouble; idle / sitting / saluting: you; moving: where he's going
                    f'execute if score @s bm.les matches 7..9 if entity @e[{foe},distance=..17] facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p96/place',
                    f'execute if score @s bm.les matches 7..9 unless entity @e[{foe},distance=..17] rotated as @s rotated ~ 0 run function bm:p96/place',
                    'execute if score @s bm.les matches 4 run function bm:p96/face_you',
                    'execute if score @s bm.les matches 6 run function bm:p96/face_you',
                    'execute if score @s bm.les matches 0 run function bm:p96/face_you',
                    'execute if score @s bm.les matches 1..3 rotated as @s rotated ~ 0 run function bm:p96/place',
                    'tag @a[tag=bm.leown] remove bm.leown', 'tag @e[tag=bm.lesel] remove bm.lesel'])
    fn('p96/face_you', ['execute if entity @a[tag=bm.leown,distance=1.5..10] facing entity @a[tag=bm.leown,limit=1] feet rotated ~ 0 run return run function bm:p96/place',
                        'execute rotated as @s rotated ~ 0 run function bm:p96/place'])
    # the salute: his left arm folds up to the helm for a moment, then back
    fn('p96/salute', ['scoreboard players set @s bm.lesl 30',
                      'execute as @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_arml] run data modify entity @s item.components."minecraft:item_model" set value "bm:le_arml_salute"'])
    fn('p96/salute_end', ['execute as @e[type=minecraft:item_display,tag=bm.lesel,tag=bm.lp_arml] run data modify entity @s item.components."minecraft:item_model" set value "bm:le_arml"'])

    # ---- the thrust (10 ticks; the blow lands on the 5th) and the throw (12 ticks; the trident leaves on the 7th)
    fn('p96/thrust_go', ['scoreboard players set @s bm.lek 10', 'scoreboard players set @s bm.lea 7', 'scoreboard players set @s bm.lem 22'])
    fn('p96/throw_go', ['scoreboard players set @s bm.lek 12', 'scoreboard players set @s bm.lea 8', 'scoreboard players set @s bm.let 100',
                        'playsound minecraft:item.trident.throw neutral @a[distance=..16] ~ ~ ~ 0.6 1.0'])
    fn('p96/act_tick', ['scoreboard players remove @s bm.lek 1',
                        'execute if score @s bm.lea matches 7 if score @s bm.lek matches 5 run function bm:p96/thrust_hit',
                        'execute if score @s bm.lea matches 8 if score @s bm.lek matches 5 run function bm:p96/release'])
    fn('p96/thrust_hit', ['tag @s add bm.leme', 'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 0.9',
                          f'execute positioned ^ ^ ^1.6 as @e[{foe},distance=..2.6,sort=nearest,limit=1] at @s run function bm:p96/thrusted',
                          'tag @s remove bm.leme', 'scoreboard players add @s bm.leq 1', 'execute if score @s bm.leq matches 10.. run function bm:p96/quip'])
    fn('p96/thrusted', ['damage @s 9 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.leme,limit=1]',
                        f'execute as @e[{foe},distance=0.1..2.2] run damage @s 3 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.leme,limit=1]',
                        'execute if entity @e[type=minecraft:wolf,tag=bm.leme,tag=bm.ledc] run function bm:p66/freeze',
                        'particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 1', 'particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.2 16'])
    # the throw: the trident flies at the nearest monster, homing a little; it hits (7, + lightning in a storm), sticks, or runs out - and it's back
    flying = snbt({'Tags': ['bm.letr', 'bm.letrn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:le_trident'}},
                   'item_display': 'fixed', 'teleport_duration': Int(1),
                   'transformation': {'left_rotation': qf(ART.TIP_FWD), 'right_rotation': ident, 'translation': [F(0)] * 3, 'scale': [F(S)] * 3}})
    fn('p96/release', ['function bm:p96/tri_off', 'scoreboard players set @s bm.ler 200',
                       f'execute facing entity @e[{foe},distance=..15,sort=nearest,limit=1] eyes positioned ^-0.3 ^1.6 ^0.6 run summon minecraft:item_display ~ ~ ~ {flying}',
                       f'execute as @e[type=minecraft:item_display,tag=bm.letrn] at @s facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes run tp @s ~ ~ ~ ~ ~',
                       'scoreboard players operation @e[type=minecraft:item_display,tag=bm.letrn] bm.pid = #me bm.pid',
                       'scoreboard players set @e[type=minecraft:item_display,tag=bm.letrn] bm.lel 30',
                       'tag @e[type=minecraft:item_display,tag=bm.letrn] remove bm.letrn',
                       'playsound minecraft:item.trident.riptide_1 neutral @a[distance=..16] ~ ~ ~ 0.6 1.2'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.letr] at @s run function bm:p96/fly')
    fn('p96/fly', ['scoreboard players remove @s bm.lel 1', 'particle minecraft:bubble ~ ~ ~ 0.05 0.05 0.05 0 2', 'particle minecraft:splash ~ ~ ~ 0.05 0.05 0.05 0 1',
                   f'execute positioned ~ ~-0.6 ~ if entity @e[{foe},distance=..1.3] run return run function bm:p96/tri_hit',
                   'execute if score @s bm.lel matches ..0 run return run function bm:p96/tri_done',
                   f'execute if entity @e[{foe},distance=..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes positioned ^ ^ ^0.9 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p96/tri_done',
                   f'execute unless entity @e[{foe},distance=..16] positioned ^ ^ ^0.9 unless block ~ ~ ~ #bm:grap_pass run return run function bm:p96/tri_done',
                   f'execute if entity @e[{foe},distance=..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes run tp @s ^ ^ ^0.9 ~ ~',
                   f'execute unless entity @e[{foe},distance=..16] run tp @s ^ ^ ^0.9'])
    wjson('bm/predicate/p96/thunder.json', {'condition': 'minecraft:weather_check', 'thundering': True})
    fn('p96/tri_hit', ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add bm.leme',
                       f'execute positioned ~ ~-0.6 ~ as @e[{foe},distance=..1.3,sort=nearest,limit=1] at @s run function bm:p96/tri_struck',
                       'tag @e[tag=bm.leme] remove bm.leme', 'function bm:p96/tri_done'])
    fn('p96/tri_struck', ['execute if entity @e[tag=bm.leme] run damage @s 7 minecraft:mob_projectile by @e[tag=bm.leme,limit=1]',
                          'execute unless entity @e[tag=bm.leme] run damage @s 7 minecraft:mob_projectile',
                          'execute if entity @e[type=minecraft:wolf,tag=bm.leme,tag=bm.ledc] run function bm:p66/freeze',
                          # (Channeling: in a thunderstorm, under open sky, never within 6 of his summoner)
                          'execute if predicate bm:p96/thunder positioned ~ ~1.6 ~ if predicate bm:sees_sky positioned ~ ~-1.6 ~ unless entity @a[distance=..6] run summon minecraft:lightning_bolt ~ ~ ~',
                          'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 12'])
    fn('p96/tri_done', ['particle minecraft:splash ~ ~ ~ 0.2 0.2 0.2 0.1 16', 'particle minecraft:bubble_pop ~ ~ ~ 0.2 0.2 0.2 0.05 10',
                        'playsound minecraft:item.trident.return neutral @a[distance=..16] ~ ~ ~ 0.7 1.0',
                        'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run scoreboard players set @s bm.ler 8', 'kill @s'])
    QUIPS = ['Stay down.', 'Hold the line!', 'Not today.', "That's one.", 'Steady...', 'For the shore!', 'You alright back there?']
    fn('p96/quip', ['scoreboard players set @s bm.leq 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {i + 1} on owner if entity @s[distance=..20] run ' + lesay(q) for i, q in enumerate(QUIPS)])

    # ================================================================== the crest: call, recall, send home
    pet = {'Tags': ['bm.leopet', 'bm.lenew', 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(HP),
           'CustomName': T('Leo', SEA, bold=True), 'CustomNameVisible': B(0),
           'attributes': [{'id': 'minecraft:max_health', 'base': D(HP)}, {'id': 'minecraft:armor', 'base': D(14)}, {'id': 'minecraft:armor_toughness', 'base': D(4)},
                          {'id': 'minecraft:attack_damage', 'base': D(4)}, {'id': 'minecraft:knockback_resistance', 'base': D(0.6)},
                          {'id': 'minecraft:movement_speed', 'base': D(0.34)}, {'id': 'minecraft:follow_range', 'base': D(32)}, {'id': 'minecraft:step_height', 'base': D(1.0)}],
           'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p96/use', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                   f'{sel_pet} run tag @s add bm.lesel2',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.lesel2] if predicate bm:p20/sneaking run function bm:p96/dismiss',
                   'execute if entity @e[type=minecraft:wolf,tag=bm.lesel2] unless predicate bm:p20/sneaking run function bm:p96/recall',
                   'execute unless entity @e[type=minecraft:wolf,tag=bm.lesel2] unless predicate bm:p20/sneaking run function bm:p96/try_summon',
                   'execute unless entity @e[type=minecraft:wolf,tag=bm.lesel2] if predicate bm:p20/sneaking run ' + say("Leo isn't with you. (Use the crest to call him.)"),
                   'tag @e[tag=bm.lesel2] remove bm.lesel2'])
    fn('p96/recall', ['tp @e[type=minecraft:wolf,tag=bm.lesel2,limit=1] @s', 'data modify entity @e[type=minecraft:wolf,tag=bm.lesel2,limit=1] Sitting set value 0b',
                      'particle minecraft:splash ~ ~1 ~ 0.4 0.8 0.4 0.1 30', 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..16] ~ ~ ~ 1 0.9',
                      lesay('Right here. I\'ve got your back.')])
    fn('p96/try_summon', ['execute if score @s bm.lecd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.lecd',
                          'execute if score @s bm.lecd matches 1.. run scoreboard players add #m bm.rng 59', 'execute if score @s bm.lecd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                          'execute if score @s bm.lecd matches 1.. run return run ' + title('@s', 'actionbar', [T('Leo is still patching his armour: about ', 'gray'),
                                                                                                             {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                          'execute unless function bm:p96/ok run return run ' + say("Leo can't come here."),
                          'function bm:p96/summon'])
    fn('p96/summon', ['execute positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p96/summon_here',
                      'execute positioned ^ ^1 ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p96/summon_here',
                      'function bm:p96/summon_here'])
    fn('p96/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet)}',
                           'data modify entity @e[type=minecraft:wolf,tag=bm.lenew,limit=1,sort=nearest] Owner set from entity @s UUID',
                           f'attribute @e[type=minecraft:wolf,tag=bm.lenew,limit=1,sort=nearest] minecraft:max_health base set {HP}',
                           f'data modify entity @e[type=minecraft:wolf,tag=bm.lenew,limit=1,sort=nearest] Health set value {HP}f',
                           'scoreboard players set @e[type=minecraft:wolf,tag=bm.lenew,limit=1,sort=nearest] bm.les -1',
                           'execute rotated ~180 0 run function bm:p96/rig_here',
                           'scoreboard players operation @e[tag=bm.lenew,distance=..4] bm.pid = @s bm.pid',
                           'execute as @e[type=minecraft:item_display,tag=bm.lenew,distance=..4] run tag @s add bm.lesel', 'function bm:p96/grow',
                           'execute as @e[type=minecraft:wolf,tag=bm.lenew,distance=..4,limit=1] run function bm:p96/salute',
                           'tag @e[tag=bm.lesel] remove bm.lesel', 'tag @e[tag=bm.lenew,distance=..4] remove bm.lenew',
                           'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..20] ~ ~ ~ 1 0.7',
                           'playsound minecraft:ambient.underwater.exit neutral @a[distance=..20] ~ ~ ~ 0.8 1.0',
                           lesay('Leo, at your service. Lead on - I\'ll keep the wolves off your heels.')])
    fn('p96/rig_here', rig + ['tp @e[type=minecraft:item_display,tag=bm.lenew,distance=..1] ~ ~ ~ ~ 0'])
    fn('p96/rerig', ['kill @e[type=minecraft:item_display,tag=bm.lesel]', 'execute rotated as @s rotated ~ 0 run function bm:p96/rig_here',
                     'scoreboard players operation @e[type=minecraft:item_display,tag=bm.lenew,distance=..2] bm.pid = #me bm.pid',
                     'tag @e[type=minecraft:item_display,tag=bm.lenew,distance=..2] add bm.lesel', 'tag @e[type=minecraft:item_display,tag=bm.lenew,distance=..2] remove bm.lenew',
                     'function bm:p96/grow', 'scoreboard players set @s bm.les -1', 'scoreboard players set @s bm.lesl 0',
                     'execute if score @s bm.ler matches 2.. run function bm:p96/tri_off'])
    fn('p96/dismiss', ['execute as @e[type=minecraft:wolf,tag=bm.lesel2] at @s run function bm:p96/fade',
                       'execute as @e[type=minecraft:wolf,tag=bm.lesel2] run data remove entity @s Owner',
                       'execute as @e[type=minecraft:wolf,tag=bm.lesel2] run tp @s ~ -500 ~', 'kill @e[type=minecraft:wolf,tag=bm.lesel2]',
                       lesay('Back to the shore, then. Call, and I\'ll come running.')])

    # ---- fainting: the rig without its host (4 ticks running) washes away; the crest rests 5 minutes
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.lp_body,tag=!bm.lefade,tag=!bm.leencp] at @s run function bm:p96/check',
             'scoreboard players remove @e[type=minecraft:item_display,tag=bm.lefade] bm.lel 1',
             'kill @e[type=minecraft:item_display,tag=bm.lefade,scores={bm.lel=..0}]']
    fn('p96/check', ['scoreboard players operation #me bm.pid = @s bm.pid',
                     f'{sel_pet.replace("tag=bm.leopet]", "tag=bm.leopet,distance=..16]")} run return run scoreboard players set @s bm.lez 0',
                     'scoreboard players add @s bm.lez 1', 'execute if score @s bm.lez matches 4.. run function bm:p96/fell'])
    fn('p96/fell', ['function bm:p96/fade', 'execute as @a if score @s bm.pid = #me bm.pid run function bm:p96/cooldown'])
    fn('p96/cooldown', [f'scoreboard players set @s bm.lecd {PET_CD}',
                        tellraw('@s', PREFIX + [T('Leo goes down. ', SEA, bold=True), T('"...Just a scratch. Give me a minute - or five." ', CREAM),
                                                T(f'The crest needs {PET_CD // 60} minutes before he can come back.', 'gray')])])
    fn('p96/fade', ['execute as @e[type=minecraft:item_display,tag=bm.lep,tag=!bm.lefade] if score @s bm.pid = #me bm.pid run function bm:p96/fade1',
                    'execute as @e[type=minecraft:item_display,tag=bm.letr] if score @s bm.pid = #me bm.pid run kill @s',
                    'particle minecraft:splash ~ ~1 ~ 0.5 1 0.5 0.2 90', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.3 0.1 0.15 30',
                    'particle minecraft:flash{color:[0.55,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                    'playsound minecraft:ambient.underwater.enter neutral @a[distance=..20] ~ ~ ~ 1 1.2', 'playsound minecraft:entity.illusioner.mirror_move neutral @a[distance=..20] ~ ~ ~ 0.8 1.0'])
    fn('p96/fade1', ['tag @s add bm.lefade', 'scoreboard players set @s bm.lel 3',
                     'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:5945568}'])
    second.append('scoreboard players remove @a[scores={bm.lecd=1..}] bm.lecd 1')
    G.FUNCS['p62/died'].insert(-1, 'execute as @e[type=minecraft:wolf,tag=bm.leopet] if score @s bm.pid = #me bm.pid at @s run function bm:p96/go')
    fn('p96/go', ['scoreboard players add #gone bm.rng 1', 'function bm:p96/fade', 'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, ('leo', 'wolf', 'bm.leopet', 'leo_crest', 'p96/go', 'Leo', 'bm.fgo', 'p96/summon_here'), second)

    # ================================================================== strong but caring: every second, as Leo
    second.append('execute as @e[type=minecraft:wolf,tag=bm.leopet,tag=!bm.ffpet] at @s run function bm:p96/sec')
    wjson('bm/predicate/p96/regen.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:effects': {'minecraft:regeneration': {}}}})
    fn('p96/sec', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s remove bm.ledc', 'tag @s remove bm.lede',
                   'execute if score @s bm.leg matches 1.. run scoreboard players remove @s bm.leg 1',
                   'scoreboard players set #dc bm.rng 0', 'scoreboard players set #de bm.rng 0',
                   'execute as @e[type=minecraft:wolf,tag=bm.celipet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #dc bm.rng 1',
                   'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #de bm.rng 1',
                   'execute if score #dc bm.rng matches 1 run tag @s add bm.ledc', 'execute if score #de bm.rng matches 1 run tag @s add bm.lede',
                   'execute on owner if entity @s[distance=..24] run tag @s add bm.leown',
                   'execute if entity @a[tag=bm.leown] run function bm:p96/care',
                   'tag @a[tag=bm.leown] remove bm.leown'])
    fn('p96/care', [
        # the guard: you at 4 hearts or less, a monster about - he's there
        'execute store result score #oh bm.rng run data get entity @a[tag=bm.leown,limit=1] Health',
        f'execute if score #oh bm.rng matches ..8 unless score @s bm.leg matches 1.. as @a[tag=bm.leown,limit=1] at @s if entity @e[{foe},distance=..10] run tag @s add bm.leguard',
        'execute if entity @a[tag=bm.leguard] run function bm:p96/guard',
        'tag @a[tag=bm.leguard] remove bm.leguard',
        # steadfast: a fight on, you close - Resistance I
        f'execute if entity @e[{foe},distance=..10] as @a[tag=bm.leown,distance=..6] run effect give @s minecraft:resistance 3 0 true',
        # in the water with him: you breathe, you swim like he does
        'execute as @a[tag=bm.leown,distance=..10] at @s if block ~ ~1 ~ minecraft:water run function bm:p96/sea',
        # the pairs
        'execute if entity @s[tag=bm.ledc] run function bm:p96/duo_celi',
        'execute if entity @s[tag=bm.lede] run function bm:p96/duo_emma',
        'execute if entity @s[tag=bm.ledc,tag=bm.lede] as @a[tag=bm.leown] run effect give @s minecraft:speed 3 0 true',
        'scoreboard players add @s bm.leb 1', 'execute if score @s bm.leb matches 120.. run function bm:p96/banter'])
    fn('p96/sea', ['effect give @s minecraft:water_breathing 4 0 true', 'effect give @s minecraft:dolphins_grace 4 0 true'])
    fn('p96/guard', ['scoreboard players set @s bm.leg 30', 'execute if entity @s[tag=bm.lede] run scoreboard players set @s bm.leg 15',
                     'scoreboard players set @s bm.lek 40', 'scoreboard players set @s bm.lea 9', 'scoreboard players set @s bm.lem 0',
                     'execute at @a[tag=bm.leguard,limit=1] positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp @s ~ ~ ~',
                     'data modify entity @s Sitting set value 0b',
                     'effect give @a[tag=bm.leguard] minecraft:resistance 6 1 true', 'effect give @a[tag=bm.leguard] minecraft:absorption 10 0 true',
                     'effect give @s minecraft:resistance 8 0 true',
                     'tag @s add bm.leme',
                     f'execute at @a[tag=bm.leguard,limit=1] as @e[{foe},distance=..8] run damage @s 1 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.leme,limit=1]',
                     'tag @s remove bm.leme',
                     'particle minecraft:splash ~ ~1 ~ 0.6 0.8 0.6 0.2 40', 'particle minecraft:enchanted_hit ~ ~1.2 ~ 0.5 0.6 0.5 0.1 20',
                     'playsound minecraft:item.shield.block neutral @a[distance=..20] ~ ~ ~ 1 0.8', 'playsound minecraft:item.trident.thunder neutral @a[distance=..20] ~ ~ ~ 0.25 1.6',
                     'execute store result score #r bm.rng run random value 1..3',
                     'execute if score #r bm.rng matches 1 as @a[tag=bm.leguard] run ' + lesay('Behind me! I\'ve got you.'),
                     'execute if score #r bm.rng matches 2 as @a[tag=bm.leguard] run ' + lesay('Easy, easy - I\'m here. Catch your breath.'),
                     'execute if score #r bm.rng matches 3 as @a[tag=bm.leguard] run ' + lesay('Over here, you sea-rats! Leave them be!')] + face('worried', 24))
    fn('p96/duo_celi', ['execute as @a[tag=bm.leown] run effect give @s minecraft:strength 3 0 true',
                        'execute as @e[type=minecraft:wolf,tag=bm.celipet,distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 3 0 true',
                        'execute as @a[tag=bm.leown] unless entity @s[advancements={bm:story/leo_celi=true}] run function bm:p96/duo_celi_first'])
    fn('p96/duo_celi_first', ['advancement grant @s only bm:story/leo_celi',
                              tellraw('@s', PREFIX + [T('Steel and Frost! ', SEA, bold=True), T('Leo and Celi fight side by side: you hit harder, he covers her, and his thrusts freeze.', 'gray')]),
                              tellraw('@s', [T('Celi: ', '#8ed8ff', bold=True), T('"Oh, great. The tin can."', '#d8f0ff')]),
                              tellraw('@s', [T('Leo: ', SEA, bold=True), T('"Good to see you too, Celi. Try not to stab me this time."', CREAM)])])
    fn('p96/duo_emma', ['execute as @a[tag=bm.leown] unless predicate bm:p96/regen run effect give @s minecraft:regeneration 5 0 true',
                        'execute as @e[type=minecraft:cat,tag=bm.emmapet,distance=..16] if score @s bm.pid = #me bm.pid run effect give @s minecraft:resistance 3 1 true',
                        'execute as @a[tag=bm.leown] unless entity @s[advancements={bm:story/leo_emma=true}] run function bm:p96/duo_emma_first'])
    fn('p96/duo_emma_first', ['advancement grant @s only bm:story/leo_emma',
                              tellraw('@s', PREFIX + [T('The Knight\'s Vow! ', SEA, bold=True), T('Leo shields Emma: you regenerate, she\'s hard to hurt, and his guard comes back twice as fast.', 'gray')]),
                              tellraw('@s', [T('Emma: ', '#ff8ad8', bold=True), T('"Leo! You came! Did you see my new ribbon?"', '#ffd8f0')]),
                              tellraw('@s', [T('Leo: ', SEA, bold=True), T('"I did. It suits you. Stay behind me, Emma - I\'ll keep you safe."', CREAM)])])
    BANTER = {'celi': [('Celi', 'Try to keep up, sir knight.', 'Someone has to watch your back. You never do.'),
                       ('Leo', "You're overextending again, Celi.", "And you're SLOW again. Clank clank clank."),
                       ('Celi', 'I had that one.', 'You had it pinned to the wall by its own spear. Very impressive.')],
             'emma': [('Emma', 'Leo, Leo! Did you see? I healed a whole fox!', 'I saw. Well done, Emma.'),
                      ('Leo', 'Stay close, Emma. The dark has teeth out here.', "Okay! ...But I'm still cheering really loud!"),
                      ('Emma', 'Do knights ever get scared?', 'All the time. You just stand in front of the scary thing anyway.')]}
    who = {'Celi': ('#8ed8ff', '#d8f0ff'), 'Emma': ('#ff8ad8', '#ffd8f0'), 'Leo': (SEA, CREAM)}
    def pair(k, first, a, b):
        other = {'celi': 'Celi', 'emma': 'Emma'}[k]
        second_name = 'Leo' if first != 'Leo' else other
        return [tellraw('@a[tag=bm.leown]', [T(f'{first}: ', who[first][0], bold=True), T(f'"{a}"', who[first][1])]),
                tellraw('@a[tag=bm.leown]', [T(f'{second_name}: ', who[second_name][0], bold=True), T(f'"{b}"', who[second_name][1])])]
    bl = ['scoreboard players set @s bm.leb 0', 'execute store result score #r bm.rng run random value 1..6']
    for k, tagk in (('celi', 'bm.ledc'), ('emma', 'bm.lede')):
        for i, (first, a, b) in enumerate(BANTER[k]):
            n = i + 1 + (0 if k == 'celi' else 3)
            fn(f'p96/banter_{n}', pair(k, first, a, b) + face('smile', 40))
            bl.append(f'execute if score #r bm.rng matches {n} if entity @s[tag={tagk}] run function bm:p96/banter_{n}')
    fn('p96/banter', bl)
    # (Emma's pulses buff him too, as they do Celi)
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', 'tag=bm.leopet') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]

    # ================================================================== his raid contract (Goldtooth: 1 trophy + 5 medallions)
    def signed():
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    fn('p96/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                    'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return run ' + say('Leo is already under contract.', 'gray'),
        f'scoreboard players add @s bm.fcon {BIT}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_leo"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T('Leo', SEA, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p96/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed() +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T('Leo', SEA), T(' needs a ', 'gray'), T('Raid Contract', '#ffcf40'), T(' to come into the vault. Goldtooth sells them.', 'gray')]), 'return 0'])
    import phase70 as P70
    from gen_dp import offer
    prev = P70.goldtooth
    def g96():
        d = prev()
        d['Offers']['Recipes'].append(offer(('gutter_trophy', 1), ('fcontract_leo', 1), ('gutter_medallion', 5)))
        return d
    P70.goldtooth = g96
    L = G.FUNCS['p70/r/lobby/init']
    L[:] = [l.replace(snbt(prev()), snbt(g96())) if 'bm.gvgt' in l and 'summon minecraft:villager' in l else l for l in L]
    assert any(snbt(g96()) in l for l in L), "Goldtooth's summon wasn't found to add Leo's contract"

    # ================================================================== SEAWATCH FORTS: rare, on the shore
    wjson('bm/tags/worldgen/biome/has_structure/leo_fort.json', {'values': SHORE})
    wjson('bm/tags/worldgen/structure/leo_fort.json', {'values': ['bm:leo_fort']})
    wjson('bm/worldgen/structure/leo_fort.json', {'type': 'minecraft:jigsaw', 'biomes': '#bm:has_structure/leo_fort', 'step': 'surface_structures',
                                                  'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': 'bm:leo_fort/start', 'size': 1,
                                                  'start_height': {'absolute': 0}, 'project_start_to_heightmap': 'WORLD_SURFACE_WG',
                                                  'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
    wjson('bm/worldgen/template_pool/leo_fort/start.json', {'fallback': 'minecraft:empty', 'elements': [
        {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'bm:leo_fort', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
    wjson('bm/worldgen/structure_set/leo_fort.json', {'structures': [{'structure': 'bm:leo_fort', 'weight': 1}],
                                                      'placement': {'type': 'minecraft:random_spread', 'spacing': 40, 'separation': 16, 'salt': 96044817}})
    from structures import Build
    Bd = Build(1, 1, 1)
    Bd.marker(0.5, 0.0, 0.5, ['bm.lefort_seed'], 0)
    Bd.export(G.path('data', 'bm', 'structure', 'leo_fort.nbt'))
    second.append('execute as @e[type=minecraft:marker,tag=bm.lefort_seed] at @s if entity @a[distance=..96] if loaded ~-7 ~ ~-7 if loaded ~7 ~ ~7 '
                  'run function bm:p96/fort/build')
    wjson('bm/tags/block/p96_fill.json', {'values': ['#minecraft:replaceable', 'minecraft:sand', 'minecraft:red_sand', 'minecraft:gravel', 'minecraft:kelp', 'minecraft:kelp_plant',
                                                     'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:snow_block', 'minecraft:ice', 'minecraft:sandstone', 'minecraft:clay']})
    wjson('bm/tags/block/p96_clear.json', {'values': ['#minecraft:replaceable', 'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass', 'minecraft:tall_seagrass',
                                                      'minecraft:sugar_cane', 'minecraft:snow', 'minecraft:ice', 'minecraft:cactus']})
    wjson('bm/loot_table/chests/p96_fort.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': {'min': 4, 'max': 6, 'type': 'minecraft:uniform'}, 'entries': [
            {'type': 'minecraft:item', 'name': 'minecraft:bread', 'weight': 4, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 2, 'max': 5, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:cooked_cod', 'weight': 4, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 2, 'max': 6, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:iron_ingot', 'weight': 3, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 1, 'max': 5, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:arrow', 'weight': 3, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 4, 'max': 12, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:prismarine_shard', 'weight': 2, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 2, 'max': 6, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:emerald', 'weight': 2, 'functions': [{'function': 'minecraft:set_count', 'count': {'min': 1, 'max': 3, 'type': 'minecraft:uniform'}}]},
            {'type': 'minecraft:item', 'name': 'minecraft:nautilus_shell', 'weight': 1}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'bm:items/token', 'weight': 6}, {'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea', 'weight': 1},
                                 {'type': 'minecraft:item', 'name': 'minecraft:trident', 'weight': 1}, {'type': 'minecraft:empty', 'weight': 4}]}]})
    fn('p96/fort/build', ['kill @s',
                          'execute if block ~ ~-3 ~ minecraft:water if block ~ ~-1 ~ minecraft:water run return 0',                  # (out in deep water: no fort)
                          'execute if block ~ ~ ~ minecraft:water positioned ~ ~1 ~ run return run function bm:p96/fort/build2',     # (in the shallows: up on a plinth)
                          'function bm:p96/fort/build2'])
    W = lambda a, b, blk: f'fill ~{a[0]} ~{a[1]} ~{a[2]} ~{b[0]} ~{b[1]} ~{b[2]} minecraft:{blk}'
    fn('p96/fort/build2', [
        'fill ~-7 ~ ~-7 ~7 ~8 ~7 minecraft:air replace #bm:p96_clear', 'fill ~-5 ~ ~-5 ~5 ~6 ~5 minecraft:air replace minecraft:water',
        'fill ~-6 ~-7 ~-6 ~6 ~-1 ~6 minecraft:stone_bricks replace #bm:p96_fill',            # the plinth, down into the sand
        W((-4, -1, -4), (4, -1, 4), 'spruce_planks'),
        W((-4, 0, -4), (4, 2, -4), 'stone_bricks'), W((-4, 0, 4), (4, 2, 4), 'stone_bricks'),
        W((-4, 0, -4), (-4, 2, 4), 'stone_bricks'), W((4, 0, -4), (4, 2, 4), 'stone_bricks'),
        'fill ~-4 ~ ~-4 ~4 ~ ~4 minecraft:mossy_stone_bricks replace minecraft:stone_bricks',
        'setblock ~4 ~1 ~-2 minecraft:cracked_stone_bricks', 'setblock ~-4 ~2 ~1 minecraft:cracked_stone_bricks', 'setblock ~2 ~2 ~4 minecraft:cracked_stone_bricks',
        W((-4, 3, -4), (4, 3, -4), 'stone_brick_wall'), W((-4, 3, 4), (4, 3, 4), 'stone_brick_wall'),
        W((-4, 3, -4), (-4, 3, 4), 'stone_brick_wall'), W((4, 3, -4), (4, 3, 4), 'stone_brick_wall'),
        'fill ~-1 ~ ~4 ~1 ~1 ~4 minecraft:air', 'fill ~-1 ~3 ~4 ~1 ~3 ~4 minecraft:air',                    # the gate (south)
        'setblock ~-1 ~2 ~4 minecraft:stone_brick_stairs[facing=west,half=top]', 'setblock ~1 ~2 ~4 minecraft:stone_brick_stairs[facing=east,half=top]',
        'setblock ~-4 ~1 ~ minecraft:air', 'setblock ~4 ~1 ~ minecraft:air', 'setblock ~ ~1 ~-4 minecraft:air',  # arrow slits
        # the watchtower in the north-west corner: a ladder up, a signal fire and the blue banner on top
        W((-4, 0, -4), (-2, 5, -2), 'stone_bricks'), 'fill ~-4 ~ ~-4 ~-2 ~ ~-2 minecraft:mossy_stone_bricks',
        W((-4, 6, -4), (-2, 6, -2), 'stone_brick_wall'), 'setblock ~-3 ~6 ~-3 minecraft:campfire', 'setblock ~-2 ~6 ~-3 minecraft:air',
        'fill ~-1 ~ ~-3 ~-1 ~5 ~-3 minecraft:ladder[facing=east]', 'setblock ~-4 ~7 ~-4 minecraft:blue_banner',
        # inside: the chest, a barrel, the smoker, a hay bed, a lantern on a post, torches
        'setblock ~3 ~ ~-3 minecraft:chest[facing=west]{LootTable:"bm:chests/p96_fort"}', 'setblock ~3 ~ ~-2 minecraft:barrel[facing=up]',
        'setblock ~3 ~ ~2 minecraft:smoker[facing=west]', 'setblock ~-3 ~ ~3 minecraft:hay_block', 'setblock ~-3 ~ ~2 minecraft:hay_block',
        'setblock ~3 ~ ~3 minecraft:spruce_fence', 'setblock ~3 ~1 ~3 minecraft:lantern',
        'setblock ~ ~2 ~-3 minecraft:wall_torch[facing=south]', 'setblock ~-3 ~2 ~ minecraft:wall_torch[facing=east]', 'setblock ~3 ~2 ~ minecraft:wall_torch[facing=west]',
        'summon minecraft:marker ~ ~ ~ {Tags:["bm.lefort"]}'])

    # ---- the fort: Leo is home while anyone's near (until he leaves with someone)
    second.append('execute as @e[type=minecraft:marker,tag=bm.lefort,tag=!bm.ledone] at @s run function bm:p96/fort/sec')
    fn('p96/fort/sec', ['execute if entity @a[distance=..48,gamemode=!spectator] unless entity @e[type=minecraft:interaction,tag=bm.leenc,distance=..2] run function bm:p96/enc/spawn',
                        'execute unless entity @a[distance=..96] as @e[type=minecraft:interaction,tag=bm.leenc,distance=..2] unless score @s bm.lew matches 1.. at @s run function bm:p96/enc/gone'])
    enc_hit = snbt({'Tags': ['bm.leenc', 'bm.lenew'], 'width': F(0.9), 'height': F(2.0), 'response': B(1)})
    fn('p96/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + rig +
       ['tag @e[type=minecraft:item_display,tag=bm.lenew,distance=..1] add bm.leencp',
        'execute as @e[type=minecraft:item_display,tag=bm.lenew,distance=..1] run tag @s add bm.lesel',
        'execute rotated 0 0 run function bm:p96/place',
        'function bm:p96/grow', 'function bm:p96/pose/idle_a', 'tag @e[tag=bm.lesel] remove bm.lesel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.lenew,distance=..1] bm.lew 0',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.lenew,distance=..1] bm.lef 0',
        'tag @e[tag=bm.lenew,distance=..1] remove bm.lenew'])
    fn('p96/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.leencp,distance=..2]', 'kill @s'])
    # he keeps watch (and fights at his gate when the drowned come)
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.leenc] at @s run function bm:p96/enc/tick')
    fn('p96/enc/tick', ['scoreboard players add @s bm.lef 1', 'scoreboard players operation #f bm.rng = @s bm.lef', 'scoreboard players operation #f bm.rng %= #120 bm.rng',
                        'execute as @e[type=minecraft:item_display,tag=bm.leencp,distance=..2] run tag @s add bm.lesel',
                        'execute if score @s bm.lek matches 1.. run function bm:p96/enc/fight',
                        'execute unless score @s bm.lek matches 1.. if score @s bm.lew matches 1.. if entity @e[tag=bm.lefoe,distance=..3.5] run function bm:p96/enc/strike'] +
       [f'execute unless score @s bm.lek matches 1.. if score #f bm.rng matches {t} run function bm:p96/pose/{p}' for t, p in CYCLE[0][1]] +
       ['execute unless score @s bm.lek matches 1.. if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p96/place',
        'tag @e[tag=bm.lesel] remove bm.lesel'])
    fn('p96/enc/strike', ['scoreboard players set @s bm.lek 14', 'function bm:p96/pose/thrust_back',
                          'execute facing entity @e[tag=bm.lefoe,distance=..3.5,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p96/place'])
    fn('p96/enc/fight', ['scoreboard players remove @s bm.lek 1',
                         'execute if score @s bm.lek matches 11 run function bm:p96/pose/thrust',
                         'execute if score @s bm.lek matches 10 as @e[tag=bm.lefoe,distance=..3.6,sort=nearest,limit=1] at @s run function bm:p96/enc/hit',
                         'execute if score @s bm.lek matches 4 run function bm:p96/pose/idle_a'])
    fn('p96/enc/hit', ['damage @s 6 minecraft:mob_attack', 'particle minecraft:splash ~ ~1 ~ 0.3 0.4 0.3 0.2 16',
                       'playsound minecraft:item.trident.hit neutral @a[distance=..16] ~ ~ ~ 1 0.9'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.leenc] if data entity @s interaction at @s run function bm:p96/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.leenc] if data entity @s attack at @s run function bm:p96/enc/poke']
    fn('p96/enc/click', ['tag @s add bm.lehere', 'execute on target run function bm:p96/enc/talk', 'tag @s remove bm.lehere', 'data remove entity @s interaction'])
    fn('p96/enc/poke', ['execute on attacker run ' + lesay('Easy there, friend! Save it for the drowned.'), 'data remove entity @s attack'])
    fn('p96/enc/talk', ['execute if score @e[type=minecraft:interaction,tag=bm.lehere,limit=1] bm.lew matches 1.. run return run ' + lesay('Eyes on the water! Here they come!'),
                        f'execute if items entity @s container.* {holds} run return run ' + lesay("Good to see you, friend. The crest will bring me - whenever you need me."),
                        'execute if items entity @s weapon.mainhand #minecraft:swords run return run function bm:p96/def/start',
                        'execute if items entity @s weapon.mainhand minecraft:trident run return run function bm:p96/def/start',
                        lechat("Ho there, traveller. The drowned have come up out of that surf at my walls every night this week - and they're getting bolder."),
                        lechat("If you'll stand with me, raise your blade - a sword or a trident - and we'll hold the fort together."),
                        'playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~ 0.4 0.7'])
    # ---- DEFEND THE FORT: three waves up the beach, the last with their Tidecaller
    fn('p96/def/start', ['execute as @e[type=minecraft:interaction,tag=bm.lehere,limit=1] run scoreboard players set @s bm.lew 1',
                         'execute as @e[type=minecraft:interaction,tag=bm.lehere,limit=1] run scoreboard players set @s bm.lel 0',
                         'tag @s add bm.ledef',
                         'execute as @a[distance=..40] run ' + lechat("That's the spirit! Here they come - out of the surf! Keep them off the walls!"),
                         'playsound minecraft:block.bell.use neutral @a[distance=..48] ~ ~ ~ 1 0.8', 'playsound minecraft:event.raid.horn neutral @a[distance=..64] ~ ~ ~ 0.6 1.2',
                         'execute as @e[type=minecraft:interaction,tag=bm.lehere,limit=1] at @s run function bm:p96/def/wave'])
    def drowned(tags, captain=False, trident=False):
        d = {'Tags': ['bm.lefoe'] + tags, 'PersistenceRequired': B(1), 'CanPickUpLoot': B(0),
             'equipment': {'head': {'id': 'minecraft:turtle_helmet', 'count': Int(1)}},
             'drop_chances': {k: F(0) for k in ('head', 'chest', 'legs', 'feet', 'mainhand', 'offhand')}}
        if trident or captain: d['equipment']['mainhand'] = {'id': 'minecraft:trident', 'count': Int(1)}
        if captain:
            d.update({'CustomName': T('Tidecaller', '#3ab0a0', bold=True), 'CustomNameVisible': B(1), 'Health': F(50),
                      'attributes': [{'id': 'minecraft:max_health', 'base': D(50)}, {'id': 'minecraft:scale', 'base': D(1.25)}, {'id': 'minecraft:armor', 'base': D(8)}]})
            d['equipment']['chest'] = {'id': 'minecraft:chainmail_chestplate', 'count': Int(1)}
        return snbt(d)
    WAVES = {1: [('plain', 4)], 2: [('plain', 4), ('trident', 2)], 3: [('plain', 3), ('trident', 2), ('captain', 1)]}
    for w, groups in WAVES.items():
        lines = []
        for kind, n in groups:
            for i in range(n):
                lines.append('execute store result storage bm:tmp lew.a int 1 run random value 0..359')
                lines.append(f'function bm:p96/def/spawn_{kind} with storage bm:tmp lew')
        fn(f'p96/def/wave{w}', lines + ['execute as @a[distance=..40] run ' + title('@s', 'actionbar', [T(f'Wave {w} of 3', SEA, bold=True),
                                                                                                    T(' - the drowned are coming up the beach!', 'gray')])])
    for kind in ('plain', 'trident', 'captain'):
        fn(f'p96/def/spawn_{kind}', ['$execute rotated $(a) 0 positioned ^ ^ ^13 positioned over motion_blocking_no_leaves run summon minecraft:drowned ~ ~ ~ '
                                     + drowned([], captain=kind == 'captain', trident=kind == 'trident')])
    fn('p96/def/wave', ['execute if score @s bm.lew matches 1 run function bm:p96/def/wave1', 'execute if score @s bm.lew matches 2 run function bm:p96/def/wave2',
                        'execute if score @s bm.lew matches 3 run function bm:p96/def/wave3'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.leenc,scores={bm.lew=1..}] at @s run function bm:p96/def/sec')
    fn('p96/def/sec', ['execute unless entity @a[distance=..32,gamemode=!spectator] run return run function bm:p96/def/lose',
                       'scoreboard players add @s bm.lel 1',
                       'execute if score @s bm.lel matches 90.. run effect give @e[tag=bm.lefoe,distance=..64] minecraft:glowing 2 0 true',
                       'execute if entity @e[tag=bm.lefoe,distance=..64] run return 0',
                       'kill @e[tag=bm.lefoe]',
                       'execute if score @s bm.lew matches 3 run return run function bm:p96/def/win',
                       'scoreboard players add @s bm.lew 1', 'scoreboard players set @s bm.lel 0',
                       'execute as @a[distance=..40] run ' + lesay('Well fought! Breathe - the tide\'s turning... here comes the next lot!'),
                       'function bm:p96/def/wave'])
    fn('p96/def/lose', ['kill @e[tag=bm.lefoe,distance=..80]', 'scoreboard players set @s bm.lew 0', 'tag @a remove bm.ledef',
                        'execute as @a[distance=..80] run ' + lechat("Fall back, fall back! ...I'll hold the gate. Come back when you're ready, friend.")])
    fn('p96/def/win', ['scoreboard players set @s bm.lew 0', 'tag @s add bm.lehere',
                       'execute as @a[distance=..40,gamemode=!spectator] at @s run function bm:p96/def/reward',
                       'execute as @a[tag=bm.ledef,distance=..40,limit=1] at @s run function bm:p96/def/joins',
                       'tag @a remove bm.ledef', 'execute as @e[type=minecraft:marker,tag=bm.lefort,distance=..2] run tag @s add bm.ledone',
                       'particle minecraft:splash ~ ~1 ~ 0.6 1 0.6 0.2 60', 'function bm:p96/enc/gone'])
    fn('p96/def/reward', [lechat('We held! Ha - we held the fort! I knew you had it in you.'),
                          f'execute if items entity @s container.* {holds} run return 0',
                          lechat("Take my crest. Wherever you go, call - and I'll come. Someone ought to watch your back."),
                          tellraw('@s', PREFIX + [T('Leo joins you! ', SEA, bold=True), T('He gives you his crest. Use it to call him; sneak + use to send him home. The fort\'s chest is yours.', 'gray')]),
                          give('leo_crest'), 'advancement grant @s only bm:story/leo_friend', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.0'])
    fn('p96/def/joins', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_pet} run tag @s add bm.lesel2', 'execute unless entity @e[type=minecraft:wolf,tag=bm.lesel2] run function bm:p96/summon',
                         'tag @e[tag=bm.lesel2] remove bm.lesel2'])

    # ================================================================== achievements, admin
    adv = lambda key, title_, desc, frame='goal', hidden=False: wjson(f'bm/advancement/story/{key}.json', {
        'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
        'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:leo_crest'}},
                    'title': T(title_, 'yellow'), 'description': T(desc, 'gray'), 'frame': frame, 'show_toast': True, 'announce_to_chat': True, 'hidden': hidden}})
    adv('leo_friend', 'Hold the Line', 'Defend a seawatch fort with Leo')
    adv('leo_celi', 'Steel and Frost', 'Have Leo and Celi at your side at once', 'task', True)
    adv('leo_emma', "The Knight's Vow", 'Have Leo and Emma at your side at once', 'task', True)
    fn('admin/leo', ['execute rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves run function bm:p96/enc/spawn',
                     tellraw('@s', PREFIX + [T('Leo is standing in front of you. Right-click him with a sword or trident to defend the fort.', 'gray')])])
    fn('admin/leo_fort', ['function bm:p96/fort/build2', tellraw('@s', PREFIX + [T('A seawatch fort is built here; Leo arrives when you step back.', 'gray')])])
    fn('admin/leo_crest', [give('leo_crest')])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/leo', 'yellow'), T('  Leo (fort encounter) in front of you', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/leo_fort', 'yellow'), T('  builds a seawatch fort here', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/leo_crest', 'yellow'), T("  gives Leo's Crest", 'gray')])]
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.lep]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:interaction,tag=bm.leenc]')

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second
