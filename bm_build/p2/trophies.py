"""2.1 placeable boss trophies. The item is a consumable: using it ray-casts from the eyes (up to 5 blocks) to the first
solid block and sets a 3D trophy (item_display, model bm:trophy3d_<d>) on top of it, turned to face the player.
An invisible interaction box over it takes right-clicks (turn 45 degrees) and punches (pops the item back out).
If there's nowhere to put it, the trophy is refunded."""
from nbt import snbt, B, F, Int
from items import T
from p2.config import D

SCALE = 0.8


def generate(G):
    fn, title, give = G.fn, G.title, G.give
    fast = []
    ds = list(D)
    for i, d in enumerate(ds, 1):
        G.consume_adv(f'trophy_{d}', f'bm:p2/trophy/use_{d}')
        fn(f'p2/trophy/use_{d}', [f'advancement revoke @s only bm:consume/trophy_{d}', f'scoreboard players set #tro bm.rng {i}',
                                  'function bm:p2/trophy/place'])
    fn('p2/trophy/place', ['scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                           'execute anchored eyes positioned ^ ^ ^ run function bm:p2/trophy/ray',
                           'tag @s remove bm.placer',
                           'execute if score #placed bm.rng matches 0 unless entity @s[gamemode=creative] run function bm:p2/trophy/refund',
                           'execute if score #placed bm.rng matches 0 run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks to set it down.', 'gray'))])
    fn('p2/trophy/refund', [f'execute if score #tro bm.rng matches {i} run {give(f"trophy_{d}")}' for i, d in enumerate(ds, 1)])
    fn('p2/trophy/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p2/trophy/hit',
                         'scoreboard players remove #ray bm.rng 1',
                         'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p2/trophy/ray'])
    fn('p2/trophy/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.tro_hit,distance=..0.6] run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p2/trophy/spawn'])
    spawn = []
    for i, d in enumerate(ds, 1):
        disp = {'Tags': ['bm.tro', 'bm.new'], 'teleport_duration': Int(3),
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:trophy3d_{d}'}},
                'item_display': 'fixed', 'billboard': 'fixed',
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(SCALE / 2), F(0)], 'scale': [F(SCALE), F(SCALE), F(SCALE)]}}
        box = {'Tags': ['bm.tro_hit', f'bm.tro_{d}', 'bm.new'], 'width': F(0.8), 'height': F(0.85), 'response': B(1)}
        spawn.append(f'execute if score #tro bm.rng matches {i} run summon minecraft:item_display ~ ~ ~ {snbt(disp)}')
        spawn.append(f'execute if score #tro bm.rng matches {i} run summon minecraft:interaction ~ ~ ~ {snbt(box)}')
    spawn += ['execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.new,distance=..0.5] ~ ~ ~ ~180 0',
              'tag @e[tag=bm.new,distance=..0.5] remove bm.new',
              'scoreboard players set #placed bm.rng 1',
              'playsound minecraft:block.stone.place block @a[distance=..16] ~ ~ ~ 1 0.8',
              'particle minecraft:wax_on ~ ~0.5 ~ 0.3 0.3 0.3 0 10']
    fn('p2/trophy/spawn', spawn)
    fn('p2/trophy/pickup', [f'execute if entity @s[tag=bm.tro_{d}] run loot spawn ~ ~0.3 ~ loot bm:items/trophy_{d}' for d in ds] + [
        'kill @e[type=minecraft:item_display,tag=bm.tro,distance=..0.3]',
        'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6',
        'playsound minecraft:block.stone.break block @a[distance=..16] ~ ~ ~ 1 0.9',
        'kill @s'])
    fn('p2/trophy/spin', ['data remove entity @s interaction',
                          'execute as @e[type=minecraft:item_display,tag=bm.tro,distance=..0.3] at @s run tp @s ~ ~ ~ ~45 0',
                          'playsound minecraft:block.stone_button.click_on block @a[distance=..12] ~ ~ ~ 0.6 1.4'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.tro_hit] if data entity @s attack at @s run function bm:p2/trophy/pickup',
             'execute as @e[type=minecraft:interaction,tag=bm.tro_hit] if data entity @s interaction at @s run function bm:p2/trophy/spin']
    return dict(fast=fast)
