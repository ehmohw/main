"""2.60: Cecil's gems, all the way.

- HIS WHOLE CLOAK takes a gem's colours now (robe and both sleeves as well as the hood and the staff).
- TAKE IT BACK: sneak + right-click your Cecil with an empty hand and he coughs the gem up into your hands - he's his
  old poison self again. Handing him a different gem gives you the old one back, too (gems are never lost).
- THE ETHEREAL GEM: hand him one and he takes his ETHEREAL FORM - a pale, glowing, half-there Cecil with a prismatic
  staff. He casts twice as often (a bolt a second, 8 damage, each carrying a random element), mends you sooner, and his
  charge fills faster.
- CHARGED ATTACKS: every bolt builds his charge (7 bolts; 5 in Ethereal Form); his staff gathers light as it fills, and
  then the next cast is his element's own spell:
    poison (his own)  PLAGUE BLOOM      a choking cloud: poison and wither on everything in it for 6 seconds
    fire              METEOR            a burning rock falls from the sky: a fiery blast, everything nearby set alight
    water             TIDAL SURGE       a wave that throws monsters back from him and slows them
    earth             ROOT PRISON       roots burst up and hold every monster near the target fast
    electric          THUNDERSTORM      four bolts of lightning crash down on monsters around the target
    rock              ROCKSLIDE         boulders drop on up to three monsters
    air               CYCLONE           a whirlwind drags monsters together, then flings them into the air
    grass             OVERGROWTH        a thorn thicket that bleeds monsters and heals every player inside it
    ice               GLACIAL NOVA      a ring of frost: monsters frozen solid for 3 seconds
    ethereal          PRISMATIC CATACLYSM  nine beams of every element converge: a huge blast, every element at once
  Only monsters are touched - never players, pets or villagers."""
from items import T, ITEMS
from nbt import snbt, B, F, Int
import phase46 as P46

ETH_I = len(P46.EL_KEYS) + 1                       # 10: the ethereal "element"
ETH_COL = '#e8d8ff'
ETH_LOOK = ('#e6dcff', '#9c86d8', '#ffffff', '#ffd8ff', '#f4f4ff')   # hood, shadow, crystal, glint, metal
CHARGE = 7
CHARGE_ETH = 5
CH = {  # element: (spell name, colour, dust rgb)
    'poison': ('PLAGUE BLOOM', '#b05ae8', (0.6, 0.25, 0.85)), 'fire': ('METEOR', '#ff7a2a', (1.0, 0.45, 0.1)),
    'water': ('TIDAL SURGE', '#3a9cff', (0.2, 0.55, 1.0)), 'earth': ('ROOT PRISON', '#4aa86a', (0.3, 0.6, 0.3)),
    'electric': ('THUNDERSTORM', '#ffe23a', (1.0, 0.9, 0.2)), 'rock': ('ROCKSLIDE', '#b09070', (0.65, 0.55, 0.45)),
    'air': ('CYCLONE', '#d8f2ff', (0.88, 0.96, 1.0)), 'grass': ('OVERGROWTH', '#52d24a', (0.35, 0.85, 0.3)),
    'ice': ('GLACIAL NOVA', '#a8ecff', (0.65, 0.92, 1.0)), 'ethereal': ('PRISMATIC CATACLYSM', ETH_COL, (0.92, 0.85, 1.0)),
}
FOE = 'type=#bm:hostile,tag=!bm.npc'
import phase67 as _P67                                  # (bosses are never shoved, dragged or flung)
MOVABLE = FOE + ',tag=!bm.boss,tag=!bm.vboss,' + ','.join(f'tag=!{t}' for t, _b in _P67.BOSSES)
PARTS = (('bm.cp_head', 'head'), ('bm.cp_arm', 'arm'), ('bm.cp_body', 'body'), ('bm.cp_larm', 'larm'))


def generate(G):
    fn, title, tellraw, PREFIX = G.fn, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='#b48cff': title('@s', 'actionbar', T(txt, col))
    keys = P46.EL_KEYS
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.cpch dummy', 'scoreboard objectives add bm.cft dummy', 'scoreboard objectives add bm.cfk dummy']
    G.OBJECTIVES += ['bm.cpch', 'bm.cft', 'bm.cfk']
    tick, second = [], []
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.cecilpet] if score @s bm.pid = #me bm.pid'
    by = 'by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]'
    gem_loot = lambda i: f'loot give @s loot bm:items/{"ethereal_gem" if i == ETH_I else "gem_" + keys[i - 1]}'

    # ------------------------------------------------------------------ his looks: back to his own (#el 0), and the ethereal form
    d = G.FUNCS['p46/pet/dress']
    d += [f'execute if score #el bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.cpet,tag={part}] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_{nm}"'
          for part, nm in PARTS + (('bm.cp_eyes', 'eyes'),)]
    d += [f'execute if score #el bm.rng matches 1..{ETH_I - 1} as @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_eyes] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_eyes"']
    d += [f'execute if score #el bm.rng matches {ETH_I} as @e[type=minecraft:item_display,tag=bm.cpet,tag={part}] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_{nm}_ethereal"'
          for part, nm in PARTS + (('bm.cp_eyes', 'eyes'),)]

    # ------------------------------------------------------------------ handing him a gem gives back the one he had; the Ethereal Gem; taking it back
    for i, k in enumerate(keys):
        f = G.FUNCS[f'p46/el/{k}']
        at = next(n for n, l in enumerate(f) if l.startswith(f'scoreboard players set @s bm.cpel {i + 1}'))
        f.insert(at, 'function bm:p69/give_back')
    fn('p69/give_back', [f'execute if score @s bm.cpel matches {i} run {gem_loot(i)}' for i in range(1, ETH_I + 1)] +
       ['execute if score @s bm.cpel matches 1.. run playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 0.9'])
    G.FUNCS['p46/el/interact'][1:1] = [
        'execute if predicate bm:p20/sneaking unless items entity @s weapon.mainhand * run return run function bm:p69/take',
        'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"ethereal_gem"}] run return run function bm:p69/el_ethereal']
    eth_dust = 'particle minecraft:dust{color:[0.92,0.85,1.0],scale:1.8} ~ ~1.2 ~ 0.4 0.8 0.4 0 40'
    fn('p69/el_ethereal', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                           f'{sel_pet} if entity @s[distance=..8] run tag @s add bm.cpsel',
                           'execute unless entity @e[type=minecraft:wolf,tag=bm.cpsel] run return run ' + say('Cecil only takes gems from the one who summoned him.'),
                           'data modify entity @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] Sitting set value 0b',
                           f'execute if score @s bm.cpel matches {ETH_I} run tag @e[tag=bm.cpsel] remove bm.cpsel',
                           f'execute if score @s bm.cpel matches {ETH_I} run return run ' + say('Cecil is already ethereal. "Any more of me and I\'d be a draught."'),
                           'function bm:p69/give_back', f'scoreboard players set @s bm.cpel {ETH_I}', f'scoreboard players set #el bm.rng {ETH_I}', 'function bm:p46/pet/dress',
                           'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                           f'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run {eth_dust}',
                           'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run particle minecraft:end_rod ~ ~1.2 ~ 0.2 0.6 0.2 0.2 60',
                           'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run particle minecraft:flash{color:[1.0,0.9,1.0,1.0]} ~ ~1.2 ~ 0 0 0 0 1',
                           'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                           'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                           title('@s', 'actionbar', [T('Cecil swallows the Ethereal Gem - and fades into light. ', ETH_COL), T('ETHEREAL FORM', 'white', bold=True),
                                                     T(': faster, stronger, every element at once.', 'gray')]),
                           'tag @e[tag=bm.cpsel] remove bm.cpsel'])
    fn('p69/take', ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                    f'{sel_pet} if entity @s[distance=..8] run tag @s add bm.cpsel',
                    'execute unless entity @e[type=minecraft:wolf,tag=bm.cpsel] run return 0',
                    # (the click also told him to sit or stand - undo that)
                    'execute as @e[type=minecraft:wolf,tag=bm.cpsel] store success score #s bm.rng if data entity @s {Sitting:1b}',
                    'execute if score #s bm.rng matches 1 run data modify entity @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] Sitting set value 0b',
                    'execute if score #s bm.rng matches 0 run data modify entity @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] Sitting set value 1b',
                    'execute unless score @s bm.cpel matches 1.. run tag @e[tag=bm.cpsel] remove bm.cpsel',
                    'execute unless score @s bm.cpel matches 1.. run return run ' + say('Cecil has no gem in him to give back - poison is his own magic.', 'gray'),
                    'function bm:p69/give_back', 'scoreboard players set @s bm.cpel 0', 'scoreboard players set #el bm.rng 0', 'function bm:p46/pet/dress',
                    'execute as @e[type=minecraft:wolf,tag=bm.cpsel] run scoreboard players set @s bm.cpch 0',
                    'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run particle minecraft:dust{color:[0.6,0.25,0.85],scale:1.6} ~ ~1.2 ~ 0.4 0.8 0.4 0 30',
                    'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run playsound minecraft:entity.player.burp neutral @a[distance=..16] ~ ~ ~ 0.8 0.7',
                    say('Cecil coughs up the gem and hands it back. "Fine. Poison it is - my favourite anyway."'),
                    'tag @e[tag=bm.cpsel] remove bm.cpsel'])
    # (the item's lore says so)
    lore = ITEMS['cecil_gem']['comps']['minecraft:lore']
    lore.insert(-1, T('Sneak + right-click him empty-handed: take it back.', 'light_purple'))
    lore.insert(-1, T('An Ethereal Gem: his Ethereal Form.', 'light_purple'))

    # ------------------------------------------------------------------ the Ethereal Form: a bolt a second, 8 damage and a random element; heals sooner
    G.FUNCS['p46/pet/act'].insert(-1, f'execute if score @s bm.cpel matches {ETH_I} if score @s bm.cpa matches 1 if entity @e[{FOE},distance=..14] run function bm:p46/pet/attack')
    G.FUNCS['p46/pet/act'].insert(-1, f'execute if score @s bm.cpel matches {ETH_I} if score @s bm.cph matches 3.. on owner if entity @s[distance=..12] run function bm:p46/pet/heal_check')
    G.FUNCS['p46/pet/act'].insert(-1, f'execute if score @s bm.cpel matches {ETH_I} run particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.02 3')
    b = G.FUNCS['p46/pet/bolt']
    b.insert(0, f'execute if score #el bm.rng matches {ETH_I} run return run function bm:p69/eth_bolt')
    fn('p69/eth_bolt', [f'damage @s 8 minecraft:magic {by}', 'execute store result score #r bm.rng run random value 1..9'] +
       [f'execute if score #r bm.rng matches {i + 1} run function bm:p69/fx/{k}' for i, k in enumerate(keys)] +
       ['execute facing entity @e[type=minecraft:wolf,tag=bm.cpme,limit=1] eyes run function bm:p46/pet/beam/ethereal'])
    for k in keys:      # each element's touch, without its damage (the ethereal bolt brings its own)
        fn(f'p69/fx/{k}', [l for l in G.FUNCS[f'p46/pet/bolt/{k}'] if not l.startswith('damage ') and 'beam/' not in l])
    fn('p46/pet/beam/ethereal', [f'particle minecraft:dust{{color:[{0.6 + 0.4 * ((d // 6) % 2)},{0.85},{1.0}],scale:1.1}} ^ ^1.2 ^{d / 10} 0 0 0 0 1' for d in range(6, 133, 6)] +
       ['particle minecraft:end_rod ^ ^1.2 ^1 0.05 0.05 0.05 0.02 3'])

    # ------------------------------------------------------------------ the charge: every cast builds it; full, the next cast is his element's spell
    a = G.FUNCS['p46/pet/attack']
    k0 = next(n for n, l in enumerate(a) if l.startswith('scoreboard players set @s bm.cpa 0'))
    a[k0 + 1:k0 + 1] = ['scoreboard players add @s bm.cpch 1',
                        f'execute unless score #el bm.rng matches {ETH_I} if score @s bm.cpch matches {CHARGE + 1}.. run return run function bm:p69/charged',
                        f'execute if score #el bm.rng matches {ETH_I} if score @s bm.cpch matches {CHARGE_ETH + 1}.. run return run function bm:p69/charged']
    # his staff gathers light as the charge nears full
    G.FUNCS['p46/pet/act'].insert(-1, f'execute if score @s bm.cpch matches {CHARGE - 1}.. run function bm:p69/gather')
    fn('p69/gather', ['scoreboard players set #el bm.rng 0', 'execute if score @s bm.cpel matches 1.. run scoreboard players operation #el bm.rng = @s bm.cpel',
                      f'execute if score #el bm.rng matches {ETH_I} unless score @s bm.cpch matches {CHARGE_ETH - 1}.. run return 0'] +
       [f'execute if score #el bm.rng matches {0 if k == "poison" else i + 1} rotated as @s rotated ~ 0 positioned ^-0.6 ^1.9 ^0.3 run particle minecraft:dust{{color:[{CH[k][2][0]},{CH[k][2][1]},{CH[k][2][2]}],scale:1.2}} ~ ~ ~ 0.15 0.15 0.15 0 8'
        for i, k in enumerate(keys)] +
       [f'execute if score #el bm.rng matches {i + 1} rotated as @s rotated ~ 0 positioned ^-0.6 ^1.9 ^0.3 run particle minecraft:dust{{color:[0.6,0.25,0.85],scale:1.2}} ~ ~ ~ 0.15 0.15 0.15 0 8' for i, k in enumerate(keys) if k == 'poison'] +
       [f'execute if score #el bm.rng matches {ETH_I} rotated as @s rotated ~ 0 positioned ^-0.6 ^1.9 ^0.3 run particle minecraft:end_rod ~ ~ ~ 0.15 0.15 0.15 0.01 6',
        'execute rotated as @s rotated ~ 0 positioned ^-0.6 ^1.9 ^0.3 run particle minecraft:enchant ~ ~ ~ 0.2 0.2 0.2 0.4 6',
        'playsound minecraft:block.beacon.ambient neutral @a[distance=..12] ~ ~ ~ 0.5 1.8'])
    # (as Cecil; #el his element, #me his owner's id) the spell, on the nearest monster
    elnum = {k: (0 if k == 'poison' else i + 1) for i, k in enumerate(keys)}
    fn('p69/charged', ['scoreboard players set @s bm.cpch 0', 'tag @s add bm.cpme', 'function bm:p46/pet/arm_cast',
                       'execute if score #el bm.rng matches 3 run scoreboard players set #el bm.rng 0'] +
       [f'execute if score #el bm.rng matches {n} as @e[{FOE},distance=..14,sort=nearest,limit=1] at @s run function bm:p69/ch/{k}' for k, n in elnum.items()] +
       [f'execute if score #el bm.rng matches {ETH_I} as @e[{FOE},distance=..14,sort=nearest,limit=1] at @s run function bm:p69/ch/ethereal'] +
       [f'execute if score #el bm.rng matches {n} on owner run ' + title('@s', 'actionbar', [T('Cecil unleashes ', 'gray'), T(CH[k][0] + '!', CH[k][1], bold=True)])
        for k, n in list(elnum.items()) + [('ethereal', ETH_I)]] +
       ['playsound minecraft:entity.evoker.prepare_attack neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.illusioner.cast_spell neutral @a[distance=..24] ~ ~ ~ 1 1.2',
        'tag @s remove bm.cpme'])

    # ---- the spells (as the target monster, at it; the casting wolf tagged bm.cpme). Lasting ones leave a "field" marker.
    def dust(rgb, sc=1.4): return f'minecraft:dust{{color:[{rgb[0]},{rgb[1]},{rgb[2]}],scale:{sc}}}'
    def field(kind, ticks, extra=''):
        m = snbt({'Tags': ['bm.cf', 'bm.cfnew']})
        return [f'summon minecraft:marker ~ ~ ~ {m}', f'scoreboard players set @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.cft {ticks}',
                f'scoreboard players set @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.cfk {kind}',
                'scoreboard players operation @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.pid = #me bm.pid',
                'tag @e[type=minecraft:marker,tag=bm.cfnew] remove bm.cfnew']
    ring = lambda part, r, n=16: [f'particle {part} ^{r * __import__("math").sin(i * 6.283 / n):.2f} ^0.3 ^{r * __import__("math").cos(i * 6.283 / n):.2f} 0 0.1 0 0.02 2' for i in range(n)]
    S = {}
    S['poison'] = [f'execute as @e[{FOE},distance=..4] run damage @s 6 minecraft:magic {by}', f'effect give @e[{FOE},distance=..4] minecraft:poison 8 1',
                   f'effect give @e[{FOE},distance=..4] minecraft:wither 4 0', f'particle {dust((0.45, 0.9, 0.2), 2)} ~ ~0.8 ~ 2 0.6 2 0 80',
                   f'particle {dust((0.6, 0.25, 0.85), 2)} ~ ~0.8 ~ 2 0.6 2 0 60', 'playsound minecraft:entity.puffer_fish.blow_up neutral @a[distance=..20] ~ ~ ~ 1 0.6'] + field(1, 120)
    S['fire'] = ['summon minecraft:block_display ~ ~9 ~ {Tags:["bm.cfrock","bm.cfnew2"],block_state:"minecraft:magma_block",teleport_duration:0,'
                 'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.6f,-0.6f,-0.6f],scale:[1.2f,1.2f,1.2f]},brightness:{block:15,sky:15}}',
                 'execute as @e[type=minecraft:block_display,tag=bm.cfnew2] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{translation:[-0.6f,-9.2f,-0.6f]}}',
                 'tag @e[tag=bm.cfnew2] remove bm.cfnew2', 'playsound minecraft:entity.blaze.shoot neutral @a[distance=..24] ~ ~ ~ 1 0.5'] + field(2, 10)
    S['water'] = [f'execute as @e[{FOE},distance=..5] run damage @s 7 minecraft:magic {by}', f'effect give @e[{FOE},distance=..5] minecraft:slowness 5 1',
                  f'execute as @e[{FOE},distance=..5] run data merge entity @s {{Fire:0s}}', 'particle minecraft:splash ~ ~0.5 ~ 2.5 0.4 2.5 0.4 120',
                  'particle minecraft:bubble_pop ~ ~0.6 ~ 2 0.6 2 0.1 50', 'playsound minecraft:entity.generic.splash neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                  'playsound minecraft:ambient.underwater.exit neutral @a[distance=..20] ~ ~ ~ 1 0.8'] + field(3, 8)
    S['earth'] = [f'execute as @e[{FOE},distance=..5] run damage @s 6 minecraft:magic {by}', f'effect give @e[{FOE},distance=..5] minecraft:slowness 4 9',
                  f'effect give @e[{FOE},distance=..5] minecraft:weakness 4 1', 'particle minecraft:block{block_state:"minecraft:rooted_dirt"} ~ ~0.3 ~ 2 0.2 2 0.1 80',
                  'particle minecraft:block{block_state:"minecraft:mangrove_roots"} ~ ~0.8 ~ 1.5 0.6 1.5 0 50', 'playsound minecraft:block.rooted_dirt.break neutral @a[distance=..20] ~ ~ ~ 1 0.5',
                  'playsound minecraft:block.mangrove_roots.place neutral @a[distance=..20] ~ ~ ~ 1 0.6'] + field(4, 80)
    S['electric'] = ['tag @s add bm.cfzap'] + field(5, 40) + ['tag @s remove bm.cfzap', 'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..40] ~ ~ ~ 0.8 1.2']
    S['rock'] = [f'execute as @e[{FOE},distance=..6,sort=nearest,limit=3] at @s run function bm:p69/ch/boulder', 'playsound minecraft:block.stone.break neutral @a[distance=..20] ~ ~ ~ 1 0.5']
    fn('p69/ch/boulder', ['summon minecraft:block_display ~ ~8 ~ {Tags:["bm.cfrock","bm.cfnew2"],block_state:"minecraft:cobblestone",teleport_duration:0,'
                          'transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.7f,-0.7f,-0.7f],scale:[1.4f,1.4f,1.4f]}}',
                          'execute as @e[type=minecraft:block_display,tag=bm.cfnew2] run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[-0.7f,-8.3f,-0.7f]}}',
                          'tag @e[tag=bm.cfnew2] remove bm.cfnew2'] + field(6, 12))
    S['air'] = ['particle minecraft:gust_emitter_small ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..20] ~ ~ ~ 1 0.6'] + field(7, 80)
    S['grass'] = ['execute as @e[type=minecraft:wolf,tag=bm.cpme] on owner run effect give @s minecraft:instant_health 1 0 true', 'particle minecraft:spore_blossom_air ~ ~1 ~ 2.5 1 2.5 0 60',
                  'particle minecraft:cherry_leaves ~ ~1 ~ 2.5 1 2.5 0 40', 'playsound minecraft:block.azalea_leaves.place neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                  'playsound minecraft:block.sweet_berry_bush.place neutral @a[distance=..20] ~ ~ ~ 1 0.8'] + field(8, 120)
    S['ice'] = [f'execute as @e[{FOE},distance=..6] at @s run function bm:p69/ch/freeze'] + ring('minecraft:snowflake', 3, 24) + ring('minecraft:snowflake', 5, 32) + \
               ['particle minecraft:block{block_state:"minecraft:ice"} ~ ~1 ~ 3 0.6 3 0 60', 'playsound minecraft:block.glass.break neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                'playsound minecraft:entity.player.hurt_freeze neutral @a[distance=..20] ~ ~ ~ 1 0.6']
    fn('p69/ch/freeze', [f'damage @s 7 minecraft:freeze {by}', 'effect give @s minecraft:slowness 3 9', 'effect give @s minecraft:weakness 3 4', 'data merge entity @s {TicksFrozen:300}',
                         'summon minecraft:block_display ~ ~ ~ {Tags:["bm.cfice","bm.cfnew2"],block_state:"minecraft:ice",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[-0.55f,0f,-0.55f],scale:[1.1f,2f,1.1f]}}',
                         'scoreboard players set @e[type=minecraft:block_display,tag=bm.cfnew2,limit=1] bm.cft 60', 'tag @e[tag=bm.cfnew2] remove bm.cfnew2'])
    S['ethereal'] = [f'execute as @e[{FOE},distance=..7] run damage @s 16 minecraft:magic {by}', f'execute as @e[{FOE},distance=..7] at @s run function bm:p69/ch/every',
                     'execute as @e[type=minecraft:wolf,tag=bm.cpme] on owner run effect give @s minecraft:absorption 10 1 true',
                     'particle minecraft:flash{color:[1.0,0.95,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:end_rod ~ ~1 ~ 0.2 0.2 0.2 0.5 80',
                     'particle minecraft:totem_of_undying ~ ~1 ~ 1 1 1 0.6 60', 'playsound minecraft:block.beacon.power_select neutral @a[distance=..32] ~ ~ ~ 1 0.6',
                     'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..32] ~ ~ ~ 1 1.4'] + \
                    [f'execute rotated {i * 40} 0 run function bm:p69/ch/beam_{k}' for i, k in enumerate(keys)]
    import math
    for k in keys:
        fn(f'p69/ch/beam_{k}', [f'particle {dust(CH[k][2], 1.3)} ^ ^{0.8 + 6 * (1 - t / 10):.2f} ^{4 * (1 - t / 10):.2f} 0 0 0 0 2' for t in range(11)])
    fn('p69/ch/every', ['effect give @s minecraft:poison 4 1', 'data merge entity @s {Fire:80s,TicksFrozen:160}', 'effect give @s minecraft:slowness 3 2',
                        'effect give @s[tag=!bm.boss,tag=!bm.vboss] minecraft:levitation 1 2', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 10'])
    for k, lines in S.items():
        fn(f'p69/ch/{k}', lines)

    # ---- the fields, every tick (kind: 1 plague cloud, 2 meteor fall, 3 tidal push, 4 roots, 5 storm, 6 boulder fall, 7 cyclone, 8 thicket)
    tick += ['execute as @e[type=minecraft:marker,tag=bm.cf] at @s run function bm:p69/f/tick',
             'scoreboard players remove @e[type=minecraft:block_display,tag=bm.cfice] bm.cft 1', 'kill @e[type=minecraft:block_display,tag=bm.cfice,scores={bm.cft=..0}]']
    fn('p69/f/tick', ['scoreboard players remove @s bm.cft 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      'execute as @e[type=minecraft:wolf,tag=bm.cecilpet,distance=..40] if score @s bm.pid = #me bm.pid run tag @s add bm.cpme',
                      'scoreboard players operation #ft bm.rng = @s bm.cft', 'scoreboard players operation #ft bm.rng %= #20 bm.rng'] +
       [f'execute if score @s bm.cfk matches {n} run function bm:p69/f/k{n}' for n in range(1, 9)] +
       ['tag @e[type=minecraft:wolf,tag=bm.cpme] remove bm.cpme', 'execute if score @s bm.cft matches ..0 run kill @s'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #20 bm.rng 20', 'scoreboard players set #5 bm.rng 5']
    fn('p69/f/k1', [f'execute if score #ft bm.rng matches 0 run effect give @e[{FOE},distance=..3.5] minecraft:poison 3 1',
                    f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..3.5] run damage @s 2 minecraft:magic {by}',
                    f'particle {dust((0.45, 0.9, 0.2), 1.6)} ~ ~0.6 ~ 1.8 0.5 1.8 0 6', f'particle {dust((0.6, 0.25, 0.85), 1.6)} ~ ~0.9 ~ 1.8 0.5 1.8 0 4',
                    'particle minecraft:item_slime ~ ~0.5 ~ 1.5 0.3 1.5 0 2'])
    fn('p69/f/k2', ['execute if score @s bm.cft matches 1.. run particle minecraft:flame ~ ~1 ~ 0.3 4 0.3 0.02 6',
                    'execute if score @s bm.cft matches ..0 run function bm:p69/f/impact'])
    fn('p69/f/impact', ['kill @e[type=minecraft:block_display,tag=bm.cfrock,distance=..10,sort=nearest,limit=1]',
                        f'execute as @e[{FOE},distance=..4] run damage @s 12 minecraft:magic {by}', f'execute as @e[{FOE},distance=..4] run data merge entity @s {{Fire:160s}}',
                        'particle minecraft:explosion_emitter ~ ~0.5 ~ 0 0 0 0 1', 'particle minecraft:lava ~ ~0.5 ~ 1.5 0.3 1.5 0 30', 'particle minecraft:flame ~ ~0.5 ~ 2 0.4 2 0.1 80',
                        'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 1 0.8'])
    fn('p69/f/k3', [f'execute as @e[{MOVABLE},distance=..6] at @s facing entity @e[type=minecraft:wolf,tag=bm.cpme,limit=1] feet rotated ~180 0 run tp @s ^ ^0.08 ^0.45',
                    'particle minecraft:splash ~ ~0.4 ~ 2 0.2 2 0.3 30', 'particle minecraft:falling_water ~ ~1.5 ~ 2 0.5 2 0 10'])
    fn('p69/f/k4', [f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..5] run damage @s 1 minecraft:cactus {by}',
                    f'execute if score #ft bm.rng matches 0 run effect give @e[{FOE},distance=..5] minecraft:slowness 2 9',
                    'particle minecraft:block{block_state:"minecraft:mangrove_roots"} ~ ~0.4 ~ 2 0.3 2 0 4'])
    # (the storm: a strike every 10 ticks on a monster near the field, never twice the same in a row)
    fn('p69/f/k5', ['scoreboard players operation #f bm.rng = @s bm.cft', 'scoreboard players operation #f bm.rng %= #10 bm.rng',
                    f'execute if score #f bm.rng matches 0 as @e[{FOE},distance=..8,sort=random,limit=1] at @s run function bm:p69/f/strike',
                    'particle minecraft:electric_spark ~ ~3 ~ 3 1 3 0.1 6'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #10 bm.rng 10']
    fn('p69/f/strike', [f'damage @s 8 minecraft:lightning_bolt {by}'] + [f'particle minecraft:electric_spark ~ ~{y} ~ 0.08 0.1 0.08 0 4' for y in range(0, 14)] +
       ['particle minecraft:end_rod ~ ~6 ~ 0.05 6 0.05 0 30', 'particle minecraft:flash{color:[1.0,1.0,0.8,1.0]} ~ ~1 ~ 0 0 0 0 1',
        'playsound minecraft:entity.lightning_bolt.thunder weather @a[distance=..48] ~ ~ ~ 0.7 1.6', 'playsound minecraft:entity.lightning_bolt.impact weather @a[distance=..24] ~ ~ ~ 1 1'])
    fn('p69/f/k6', ['execute if score @s bm.cft matches ..0 run function bm:p69/f/crash'])
    fn('p69/f/crash', ['kill @e[type=minecraft:block_display,tag=bm.cfrock,distance=..10,sort=nearest,limit=1]', f'execute as @e[{FOE},distance=..2] run damage @s 11 minecraft:falling_block {by}',
                       f'effect give @e[{FOE},distance=..2] minecraft:slowness 3 2', 'particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~0.5 ~ 0.8 0.4 0.8 0 50',
                       'particle minecraft:dust_plume ~ ~0.3 ~ 0.8 0.2 0.8 0.02 20', 'playsound minecraft:block.stone.break neutral @a[distance=..24] ~ ~ ~ 1 0.5',
                       'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.5 1.4'])
    fn('p69/f/k7', [f'execute as @e[{MOVABLE},distance=1..7] at @s facing entity @e[type=minecraft:marker,tag=bm.cf,limit=1,sort=nearest] feet rotated ~ 0 run tp @s ^0.12 ^ ^0.2',
                    f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..7] run damage @s 3 minecraft:magic {by}',
                    'particle minecraft:cloud ~ ~0.5 ~ 1 0.2 1 0.05 4', 'particle minecraft:gust ~ ~1 ~ 1.2 0.6 1.2 0 1',
                    f'execute if score @s bm.cft matches 1 run effect give @e[{MOVABLE},distance=..7] minecraft:levitation 1 8',
                    'execute if score @s bm.cft matches 1 run playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..24] ~ ~ ~ 1 0.8'] +
       [f'execute if score #ft bm.rng matches {t} run particle minecraft:cloud ^{2 * math.sin(t):.2f} ^{0.3 + t * 0.12:.2f} ^{2 * math.cos(t):.2f} 0 0 0 0.02 3' for t in range(20)])
    fn('p69/f/k8', [f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..5] run damage @s 2 minecraft:cactus {by}',
                    f'execute if score #ft bm.rng matches 0 run effect give @e[{FOE},distance=..5] minecraft:slowness 2 0',
                    'execute if score #ft bm.rng matches 0 run effect give @a[distance=..6,gamemode=!spectator] minecraft:regeneration 2 1 true',
                    'particle minecraft:happy_villager ~ ~0.5 ~ 2 0.4 2 0 2', 'particle minecraft:spore_blossom_air ~ ~1 ~ 2 0.6 2 0 3'])

    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the ethereal looks
def textures():
    from PIL import Image
    from gen_rp import hexc
    import random
    rnd = random.Random(69)
    hood, shade, crys, glint, metal = ETH_LOOK
    def streaked(c, var, streak, alpha):
        im = Image.new('RGBA', (16, 16)); b = hexc(c)
        for y in range(16):
            for x in range(16):
                dd = rnd.randint(-var, var) - (var * 2 if x in streak else 0)
                a = alpha + rnd.randint(-12, 12) if alpha < 255 else 255
                im.putpixel((x, y), tuple(max(0, min(255, v + dd)) for v in b[:3]) + (max(0, min(255, a)),))
        return im
    T_ = {'cec_hood_ethereal': streaked(hood, 8, (3, 9, 13), 205), 'cec_hood_dark_ethereal': streaked(shade, 6, (5, 11), 215),
          'cec_metal_ethereal': streaked(metal, 6, (), 255)}
    cr = Image.new('RGBA', (16, 16))                 # a prism: rainbow bands, translucent
    bands = [(255, 120, 160), (255, 190, 110), (255, 245, 140), (150, 255, 170), (140, 220, 255), (190, 160, 255)]
    for y in range(16):
        for x in range(16):
            c = bands[((x + y) // 3) % len(bands)]
            cr.putpixel((x, y), c + (235 if (x + y) % 7 == 0 else 185,))
    T_['cec_crystal_ethereal'] = cr
    eye = Image.new('RGBA', (16, 16), (240, 250, 255, 255))
    T_['cec_eye_ethereal'] = eye
    return T_


def rp(R):
    import sys, copy
    R.TEXTURE_MODS.append(sys.modules[__name__])
    k = 'ethereal'
    tex = {'r': f'bm:block/cec_hood_{k}', 'd': f'bm:block/cec_hood_dark_{k}', 'g': f'bm:block/cec_metal_{k}', 'p': f'bm:block/cec_crystal_{k}', 'y': f'bm:block/cec_eye_{k}'}
    for nm in ('head', 'arm', 'body', 'larm', 'eyes'):
        ct, els = R.HATS[f'cec2_{nm}']
        els = copy.deepcopy(els)
        for e in els:                                # half-there: everything glows faintly, the crystal and eyes fully
            e['light_emission'] = max(e.get('light_emission', 0), 9)
        R.HATS[f'cec2_{nm}_ethereal'] = (dict(ct, **{c: t for c, t in tex.items() if c in ct}), els)
