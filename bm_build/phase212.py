"""2.94: DENNIS'S SEARING THROWS - Gold Rush no longer flings a fistful of nugget dust: he hurls the real thing, heated in his
forge until it glows - a diamond, or an ingot of iron, gold, copper or netherite (sear_art.py: the game's own items, glowing
hot). Each is a projectile: a billboarded display, full-bright, spinning as it flies, trailing fire and smoke, homing on the
monster it was thrown at; on the hit, a splash of molten metal (phase210's "dennis_sear"), the monster set alight and slowed
by the weight of it. Two at a time, fanned out.

  WHAT HITS HOW HARD   diamond 9, netherite 9, iron 7, gold 6, copper 6 (each sets them burning, 4 s; gold and netherite slow)
  (projectile() is general: a thrower, an item model, a damage, what happens on the hit - the Sky Buddies' Star Shot uses it too)"""
import math
from nbt import snbt, F, Int
import sear_art
import phase210 as FXS

KINDS = [('diamond', 9, []), ('netherite_ingot', 9, ['effect give @s minecraft:slowness 2 1']), ('iron_ingot', 7, []),
         ('gold_ingot', 6, ['effect give @s minecraft:slowness 2 0']), ('copper_ingot', 6, [])]
SPEED = 0.75                                     # (blocks a tick)
LIFE = 40                                        # (ticks before a miss falls away)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sear_art)
    for k in sear_art.THROWN:
        R.HATS[f'sear_{k}'] = ({'f': f'bm:block/sear_{k}'}, [{'from': [4, 4, 8], 'to': [12, 12, 8], 'shade': False, 'light_emission': 15,
                                                              'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#f'}, 'south': {'uv': [16, 0, 0, 16], 'texture': '#f'}}}])


def _spin(i, n=8):
    a = math.radians(360 * i / n) / 2
    return f'[0f,0f,{math.sin(a):.4f}f,{math.cos(a):.4f}f]'


def projectile(G, key, model, dmg, host_sel, on_hit=(), trail=(), scale=0.7, fxname='dennis_sear'):
    """-> the command (as the thrower, facing the target, at its hand) that launches one. The flight homes on the nearest monster
    in front of it; on the hit it hurts it (as the thrower: host_sel finds it again by bm.pid), then on_hit (as the monster)."""
    fn = G.fn
    tag = f'bm.pj_{key}'
    nbt = {'Tags': ['bm.pj', tag, 'bm.pjnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
           'item_display': 'fixed', 'billboard': 'center', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(1),
           'interpolation_duration': Int(1), 'view_range': F(1.5),
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)],
                              'scale': [F(scale)] * 3}}
    fn(f'p212/{key}/fly', ['scoreboard players add @s bm.pjt 1', f'execute if score @s bm.pjt matches {LIFE}.. run return run function bm:p212/fizzle',
                           f'execute positioned ~ ~-0.9 ~ if entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..1.4] run return run function bm:p212/{key}/hit',   # (2.94: aimed at the eyes - the hit, round its middle)
                           f'execute facing entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..20,sort=nearest,limit=1] eyes run tp @s ^ ^ ^{SPEED}',
                           f'execute unless entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..20] run tp @s ^ ^-0.08 ^{SPEED}',
                           'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p212/fizzle'] + list(trail) +
       ['scoreboard players operation #sp bm.rng = @s bm.pjt', 'scoreboard players operation #sp bm.rng %= #8 bm.rng'] +
       [f'execute if score #sp bm.rng matches {i} run data merge entity @s {{start_interpolation:0,interpolation_duration:1,transformation:{{right_rotation:{_spin(i + 1)}}}}}'
        for i in range(8)])
    fn(f'p212/{key}/hit', ['scoreboard players operation #me bm.pid = @s bm.pid', f'scoreboard players set #pd bm.rng {dmg}',
                           f'execute as {host_sel} if score @s bm.pid = #me bm.pid run tag @s add bm.pjme',
                           f'execute as @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..1.6,sort=nearest,limit=1] at @s run function bm:p212/{key}/hurt',
                           'tag @e[tag=bm.pjme] remove bm.pjme', FXS.fx(fxname, 0.9), 'kill @s'])
    fn(f'p212/{key}/hurt', ['execute store result storage bm:tmp p212.d int 1 run scoreboard players get #pd bm.rng', 'function bm:p212/dmg with storage bm:tmp p212'] +
       list(on_hit))
    G.FUNCS['tick'].append(f'execute as @e[type=minecraft:item_display,tag={tag}] at @s run function bm:p212/{key}/fly')
    return [f'summon minecraft:item_display ~ ~ ~ {snbt(nbt)}', 'scoreboard players operation @e[type=minecraft:item_display,tag=bm.pjnew,distance=..1] bm.pid = @s bm.pid',
            'execute rotated ~ ~ run tp @e[type=minecraft:item_display,tag=bm.pjnew,distance=..1] ~ ~ ~ ~ ~', 'tag @e[tag=bm.pjnew] remove bm.pjnew']


def common(G):
    fn = G.fn
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.pjt dummy', 'scoreboard players set #8 bm.rng 8']
    G.OBJECTIVES.append('bm.pjt')
    fn('p212/dmg', ['$damage @s $(d) minecraft:mob_attack by @e[tag=bm.pjme,limit=1]'])
    fn('p212/fizzle', ['particle minecraft:smoke ~ ~ ~ 0.1 0.1 0.1 0.02 6', 'playsound minecraft:block.fire.extinguish neutral @a[distance=..12] ~ ~ ~ 0.4 1.4', 'kill @s'])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:item_display,tag=bm.pj]')


def generate(G):
    """(after phase163: Dennis's Gold Rush throws searing metal)"""
    fn = G.fn
    common(G)
    trail = ['particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 2', 'particle minecraft:smoke ~ ~ ~ 0.04 0.04 0.04 0.01 1']
    launch = []
    for i, (k, dmg, extra) in enumerate(KINDS):
        cmds = projectile(G, f'dw_{k}', f'bm:sear_{k}', dmg, '@e[type=minecraft:wolf,tag=bm.dwpet]',
                          on_hit=['data merge entity @s {Fire:80s}', 'playsound minecraft:block.lava.extinguish neutral @a[distance=..16] ~ ~ ~ 0.7 1.2'] + extra,
                          trail=trail)
        fn(f'p212/dw/throw{i}', cmds)
    fn('p212/dw/throw', ['execute store result score #r bm.rng run random value 0..4'] +
       [f'execute if score #r bm.rng matches {i} run return run function bm:p212/dw/throw{i}' for i in range(len(KINDS))])
    L = G.FUNCS['p163/dw/range_hit']
    i = next(i for i, l in enumerate(L) if 'p163/dw/nuggets' in l)
    j = next(i for i, l in enumerate(L) if 'p163/dw/gilded' in l)
    L[i] = ('execute facing entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..12,sort=nearest,limit=1] eyes positioned ^0.3 ^1.1 ^0.6 rotated ~-8 ~ '
            'run function bm:p212/dw/throw')
    L[j] = ('execute facing entity @e[type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,distance=..12,sort=nearest,limit=1] eyes positioned ^-0.3 ^1.1 ^0.6 rotated ~8 ~ '
            'run function bm:p212/dw/throw')
    L.insert(0, 'playsound minecraft:item.firecharge.use neutral @a[distance=..16] ~ ~ ~ 0.6 1.2')
    G.FUNCS['p163/dw/range_hit'] = [l for l in L if not l.startswith('scoreboard players set #pd bm.rng')]
    del G.FUNCS['p163/dw/nuggets'], G.FUNCS['p163/dw/gilded']                     # (the old fistful of nugget dust)
