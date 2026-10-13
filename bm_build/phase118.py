"""2.73: WHEN A RAID BOSS FALLS, ITS MINIONS FALL WITH IT.

THE GUARDIANS   the vault's guardian (every tier's, every night's, and the Lucky Raid's) and the Pit's champions call guards,
                imps, brood and riders to their side. The moment one goes down, every guard of that heist within 48 blocks of
                where it fell goes down with it - and whatever their own magic brought (vexes, split slimes, silverfish) too.
                They drop nothing: the boss's own hoard is the prize.
THE COUNT       (the Gutter Gentry) when he falls, his Bloblings pop with him.
"""
from items import T

GOLD = '#ffcf40'
SPAWNLINGS = ['vex', 'slime', 'magma_cube', 'silverfish', 'endermite']     # (what a minion's own magic or death can leave behind, untagged)


def generate(G):
    fn, tellraw, wjson = G.fn, G.tellraw, G.wjson
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    wjson('bm/tags/entity_type/p118_spawnlings.json', {'values': [f'minecraft:{e}' for e in SPAWNLINGS]})
    # (every second: each living raid boss keeps a marker at its side; a marker whose boss is gone marks where it fell)
    G.FUNCS['loop/second'][-1:-1] = ['execute in bm:gutter run tag @e[type=minecraft:marker,tag=bm.gvbtk] remove bm.gvbtks',
                                     'execute in bm:gutter as @e[tag=bm.gvboss] at @s run function bm:p118/track',
                                     'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvbtk,tag=!bm.gvbtks] at @s run function bm:p118/fell']
    fn('p118/track', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #bt bm.rng 0',
                      'execute as @e[type=minecraft:marker,tag=bm.gvbtk] if score @s bm.gvi = #gi bm.rng run tp @s ~ ~ ~',
                      'execute as @e[type=minecraft:marker,tag=bm.gvbtk] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvbtks',
                      'execute as @e[type=minecraft:marker,tag=bm.gvbtk,tag=bm.gvbtks] if score @s bm.gvi = #gi bm.rng run scoreboard players set #bt bm.rng 1',
                      'execute if score #bt bm.rng matches 0 run function bm:p118/new'])
    fn('p118/new', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gvbtk","bm.gvbtks","bm.gvbtn"]}',
                    'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvbtn,distance=..1] bm.gvi = #gi bm.rng',
                    'tag @e[type=minecraft:marker,tag=bm.gvbtn] remove bm.gvbtn'])
    fn('p118/fell', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #nm bm.rng 0',
                     'execute as @e[tag=bm.gvg,tag=!bm.gvboss,distance=..48] if score @s bm.gvi = #gi bm.rng at @s run function bm:p118/poof',
                     'execute as @e[type=#bm:p118_spawnlings,tag=!bm.gnt,tag=!bm.gntl,tag=!bm.npc,distance=..48] at @s run function bm:p118/poof',
                     'execute if score #nm bm.rng matches 1.. run ' + tellraw('@a[tag=bm.gvp,distance=..60]', P + [T('Their master has fallen - ', GOLD, bold=True),
                                                                                                                       T('and every minion falls with it.', 'gray')]),
                     'kill @s'])
    fn('p118/poof', ['scoreboard players add #nm bm.rng 1', 'particle minecraft:poof ~ ~0.8 ~ 0.3 0.5 0.3 0.02 12', 'particle minecraft:soul ~ ~1 ~ 0.2 0.4 0.2 0.02 4',
                     'data modify entity @s DeathLootTable set value "minecraft:empty"',
                     'execute if entity @s[type=minecraft:slime] run data modify entity @s Size set value 0',
                     'execute if entity @s[type=minecraft:magma_cube] run data modify entity @s Size set value 0',
                     'kill @s'])
    # (the Gutter Gentry: the Count's Bloblings go when he does)
    G.FUNCS['p88/down_blob'].append('execute as @e[type=minecraft:slime,tag=bm.gntl,distance=..40] at @s run function bm:p118/poof')
