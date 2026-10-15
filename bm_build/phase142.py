"""Phase 142 (2.78): every boss makes an entrance. KillerWatt and Apophiss had theirs; the Headless Horseman, the Sand Pharaoh,
the Storm Roc, the Elder Treant, the Magma Colossus, the Voidwalker and Captain Tullius simply appeared. Now each arrives with a
title card (name and epithet) for everyone within 64 blocks, a sting in its own sounds, a ring of its own colours sweeping in to
where it stands over two seconds, and - for the darker ones - the light dipping for a moment.

Importing does nothing; generate(G) runs after the bosses' phases (it puts the entrance first in each one's summon)."""
from items import T

# boss: (its summon function, title, colour, epithet, sounds [(sound, volume, pitch)], ring particle, column particle, darkness)
BOSSES = {
    'horseman': ('p42/boss/summon', 'THE HEADLESS HORSEMAN', '#ff7a1a', 'he rides for your head',
                 [('minecraft:entity.wither.spawn', 0.5, 1.4), ('minecraft:entity.horse.angry', 1.0, 0.6)], 'minecraft:soul_fire_flame', 'minecraft:large_smoke', True),
    'pharaoh': ('p53/sph/summon', 'THE SAND PHARAOH', '#e8c060', 'the tomb stirs',
                [('minecraft:entity.husk.converted_to_zombie', 1.0, 0.5), ('minecraft:block.sand.break', 1.0, 0.6)],
                'minecraft:falling_dust{block_state:"minecraft:sand"}', 'minecraft:dust{color:[0.95,0.8,0.4],scale:2.0}', False),
    'roc': ('p53/roc/summon', 'THE STORM ROC', '#9ad8ff', 'the sky screams',
            [('minecraft:entity.phantom.swoop', 1.0, 0.5), ('minecraft:item.trident.thunder', 0.6, 1.2)], 'minecraft:cloud', 'minecraft:electric_spark', False),
    'treant': ('p54/trt/summon', 'THE ELDER TREANT', '#7ac040', 'the forest remembers',
               [('minecraft:entity.ravager.roar', 0.8, 0.5), ('minecraft:block.wood.break', 1.0, 0.5)], 'minecraft:spore_blossom_air', 'minecraft:composter', False),
    'colossus': ('p54/mcol/summon', 'THE MAGMA COLOSSUS', '#ff5a1a', 'the earth bleeds fire',
                 [('minecraft:entity.ravager.roar', 1.0, 0.4), ('minecraft:block.lava.extinguish', 1.0, 0.6)], 'minecraft:flame', 'minecraft:lava', False),
    'voidwalker': ('p54/vwk/summon', 'THE VOIDWALKER', '#c070ff', 'between the stars, it waits',
                   [('minecraft:entity.warden.emerge', 0.8, 1.3), ('minecraft:entity.enderman.stare', 1.0, 0.5)], 'minecraft:reverse_portal', 'minecraft:portal', True),
    'tullius': ('p132/b/spawn', 'CAPTAIN TULLIUS', '#8ad8f0', 'the drowned captain',
                [('minecraft:entity.elder_guardian.curse', 0.7, 0.6), ('minecraft:ambient.underwater.enter', 1.0, 0.7)], 'minecraft:splash', 'minecraft:bubble_column_up', True),
}
TICKS = 40


def generate(G):
    fn, title = G.fn, G.title
    tick = []
    for b, (summon, name, col, epithet, sounds, ring, column, dark) in BOSSES.items():
        assert summon in G.FUNCS, summon
        G.FUNCS[summon][0:0] = [f'function bm:p142/{b}/start']
        fn(f'p142/{b}/start', ['title @a[distance=..64] times 10 50 20', title('@a[distance=..64]', 'subtitle', T(epithet, 'gray', italic=True)),
                                title('@a[distance=..64]', 'title', T(name, col, bold=True))] +
           [f'playsound {s} hostile @a[distance=..64] ~ ~ ~ {v} {p}' for s, v, p in sounds] +
           (['effect give @a[distance=..32] minecraft:darkness 3 0 true'] if dark else []) +
           [f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.cine","bm.cine_{b}"]}}',
            f'scoreboard players set @e[type=minecraft:marker,tag=bm.cine_{b},distance=..0.5,limit=1] bm.cint {TICKS}'])
        # (each tick: the ring turns and closes in, a column climbs at the middle)
        fn(f'p142/{b}/tick', ['scoreboard players remove @s bm.cint 1', 'tp @s ~ ~ ~ ~23 ~',
                              f'execute if score @s bm.cint matches 27.. positioned ^ ^0.2 ^3.6 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'execute if score @s bm.cint matches 27.. positioned ^ ^0.2 ^-3.6 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'execute if score @s bm.cint matches 14..26 positioned ^ ^0.6 ^2.4 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'execute if score @s bm.cint matches 14..26 positioned ^ ^0.6 ^-2.4 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'execute if score @s bm.cint matches ..13 positioned ^ ^1 ^1.2 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'execute if score @s bm.cint matches ..13 positioned ^ ^1 ^-1.2 run particle {ring} ~ ~ ~ 0.1 0.1 0.1 0 3',
                              f'particle {column} ~ ~1 ~ 0.25 1.0 0.25 0.02 3',
                              f'execute if score @s bm.cint matches 1 run particle {ring} ~ ~1 ~ 0.8 1.2 0.8 0.08 40',
                              'execute if score @s bm.cint matches ..0 run kill @s'])
        tick.append(f'execute as @e[type=minecraft:marker,tag=bm.cine_{b}] at @s run function bm:p142/{b}/tick')
    G.FUNCS['tick'] += tick
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.cint dummy']
    G.OBJECTIVES += ['bm.cint']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.cine]']
