"""Phase 1.24 / 2.17: charms for getting out of trouble, and rare monsters that wear their own.

- THE SURFACE CHARM (Overworld loot chests, rare): right-click it underground and you rise to the surface straight above.
  Reusable, no cooldown. It won't work under open sky, outside the Overworld, or in the pack's own structures.
- THE LAVA CHARM (Nether chests: bastions and fortresses): fall into lava with one anywhere in your inventory and it pulls
  you out to the last safe ground you stood on (or the nearest safe spot), puts the fire out and gives 10 s of Fire
  Resistance. One use. Right-clicking it while you're in lava works too.
- THE RAINBOW CHARM (Lucky Whiskers, 6 Lucky Tokens): a little rainbow arcs over your head.
- RARE MONSTERS: about 3 in 1000 of these natural spawns is a rare variant with double health, glowing with its own
  particles: the Cinder Revenant (zombie), the Starlit Skeleton, the Glimmerweave Spider, the Bloomcreeper, the Voidwalker
  (enderman) and the Ashen Blaze. Each has a 35% chance (+10% per Looting level) to drop its CHARM, which gives its
  wearer the very same particles. Charms work like the other cosmetic charms: keep one anywhere in your inventory."""
from items import item, T, TOTEM
from useitem import hold, HOLD

# key: (mob type, mob name, charm name, colour, lore, particle commands - run at the feet of the mob or the charm's owner)
RARE = {
    'cinder': ('zombie', 'Cinder Revenant', 'Cinderheart Charm', '#ff6a1a', 'Embers drift off you like a banked fire.',
               ['particle minecraft:flame ~ ~0.9 ~ 0.25 0.45 0.25 0.01 1', 'particle minecraft:small_flame ~ ~0.3 ~ 0.3 0.2 0.3 0.01 1',
                'execute store result score #r bm.rng run random value 1..8', 'execute if score #r bm.rng matches 1 run particle minecraft:lava ~ ~1 ~ 0.2 0.3 0.2 0 1']),
    'starlit': ('skeleton', 'Starlit Skeleton', 'Starfall Charm', '#b8c8ff', 'Starlight clings to you.',
                ['particle minecraft:end_rod ~ ~1.2 ~ 0.35 0.6 0.35 0.01 1', 'particle minecraft:firework ~ ~2.2 ~ 0.3 0.1 0.3 0.01 1']),
    'glimmer': ('spider', 'Glimmerweave Spider', 'Glimmer Charm', '#7affd8', 'Glowing motes hang in the air around you.',
                ['particle minecraft:glow ~ ~0.8 ~ 0.4 0.4 0.4 0 2']),
    'bloom': ('creeper', 'Bloomcreeper', 'Bloom Charm', '#9aff5a', 'Spores and green sparks: spring follows you.',
              ['particle minecraft:spore_blossom_air ~ ~1 ~ 0.4 0.5 0.4 0 2', 'particle minecraft:happy_villager ~ ~0.5 ~ 0.3 0.3 0.3 0 1']),
    'void': ('enderman', 'Voidwalker', 'Void Charm', '#9a5aff', 'The void leaks out of you, just a little.',
             ['particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.02 3', 'particle minecraft:portal ~ ~0.2 ~ 0.3 0.1 0.3 0.3 2']),
    'ashen': ('blaze', 'Ashen Blaze', 'Ashfall Charm', '#d8d0c8', 'A soft fall of ash, wherever you go.',
              ['particle minecraft:white_ash ~ ~1.4 ~ 0.5 0.6 0.5 0 6', 'particle minecraft:ash ~ ~2.1 ~ 0.4 0.2 0.4 0 4']),
}
RARE_ROLL = (69, 71)          # out of 1000, on the same roll as Lucky/Champion/Elite (1..68)
RAINBOW = ['#ff3b3b', '#ff8a1a', '#ffe14a', '#4ade5a', '#3ab4ff', '#5a5aff', '#b45aff']

item('surface_charm', TOTEM, 'Surface Charm', '#8fd16a',
     ['A pebble that remembers the sky.', ('Underground, right-click: rise to the surface', 'blue'), ('straight above you. Reusable.', 'blue'),
      ('Overworld only. Not in the pack\'s structures.', 'dark_gray')],
     model='bm:surface_charm', stack=1, cat='relic', glint=True, comps=hold('none'))
HOLD['surface_charm'] = 'bm:p38/surface/use'
item('lava_charm', TOTEM, 'Lava Charm', '#ff7a1a',
     ['Cool to the touch. Always.', ('In lava, from anywhere in your inventory: pulls you', 'blue'), ('out to safe ground and puts the fire out.', 'blue'),
      ('One use.', 'gray')],
     model='bm:lava_charm', stack=16, cat='relic', glint=True, comps=hold('none'))
HOLD['lava_charm'] = 'bm:p38/lava/use'
item('charm_rainbow', TOTEM, 'Rainbow Charm', '#ffe14a', ['A little rainbow arcs over your head.', ('Keep it anywhere in your inventory.', 'gray'),
                                                            ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
     model='bm:charm_rainbow', stack=1, cat='cosmetic')
for k, (mob, mname, cname, col, lore, _) in RARE.items():
    item(f'charm_{k}', TOTEM, cname, col, [lore, (f'Dropped by the rare {mname}.', 'light_purple'), ('Keep it anywhere in your inventory.', 'gray'),
                                           ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
         model=f'bm:charm_{k}', stack=1, cat='cosmetic', glint=True)

SURFACE_LOOT = {'simple_dungeon': 4, 'abandoned_mineshaft': 4, 'desert_pyramid': 3, 'jungle_temple': 3, 'stronghold_corridor': 3,
                'stronghold_crossing': 3, 'stronghold_library': 3, 'buried_treasure': 3, 'shipwreck_treasure': 2, 'ruined_portal': 2,
                'woodland_mansion': 4, 'pillager_outpost': 2, 'ancient_city': 4, 'igloo_chest': 3}
LAVA_LOOT = {'bastion_treasure': 15, 'bastion_other': 8, 'nether_bridge': 8}


def extend_offers(O, offer):
    O['lucky'] += [offer(('lucky_token', 6), ('charm_rainbow', 1))]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    from nbt import snbt
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    lava = holds % 'lava_charm'
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    objs = ['bm.lsx dummy', 'bm.lsy dummy', 'bm.lsz dummy', 'bm.lsd dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    fast, second = [], []

    # ------------------------------------------------------------------ the Surface Charm
    fn('p38/surface/use', ['execute unless dimension minecraft:overworld run return run ' + say('The charm can\'t find a sky to rise to here.'),
                           'execute positioned ~ ~1.6 ~ if predicate bm:sees_sky run return run ' + say('You\'re already under open sky.'),
                           'execute unless function bm:p37/allowed run return run ' + say('The walls here are warded. The charm stays cold.'),
                           'execute positioned over motion_blocking if block ~ ~-1 ~ minecraft:lava run return run ' + say('Only lava waits above. The charm refuses.'),
                           'execute positioned over motion_blocking unless function bm:p37/allowed run return run ' + say('Something warded waits above. The charm refuses.'),
                           'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 30',
                           'execute positioned over motion_blocking run tp @s ~ ~ ~',
                           'execute at @s run particle minecraft:end_rod ~ ~1 ~ 0.3 0.6 0.3 0.05 20',
                           'execute at @s run playsound minecraft:entity.player.levelup player @a[distance=..16] ~ ~ ~ 0.6 1.6',
                           say('Daylight! (or at least, sky)', '#8fd16a')])

    # ------------------------------------------------------------------ the Lava Charm
    wjson('bm/tags/block/p38_hot.json', {'values': ['minecraft:lava', 'minecraft:fire', 'minecraft:soul_fire', 'minecraft:magma_block',
                                                    'minecraft:campfire', 'minecraft:soul_campfire']})
    wjson('bm/predicate/p38/on_ground.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}})
    dims = [('minecraft:overworld', 0), ('minecraft:the_nether', 1), ('minecraft:the_end', 2)]
    # remember the last safe ground of everyone carrying one (once a second)
    second += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {lava} at @s if predicate bm:p38/on_ground run function bm:p38/lava/mark',
               f'execute as @a[gamemode=!spectator] if items entity @s weapon.offhand {lava} at @s if predicate bm:p38/on_ground run function bm:p38/lava/mark']
    fn('p38/lava/mark', ['execute if block ~ ~ ~ #bm:p38_hot run return 0', 'execute if block ~ ~-0.5 ~ #bm:p38_hot run return 0',
                         'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'execute if block ~ ~1 ~ minecraft:lava run return 0',
                         'execute store result score @s bm.lsx run data get entity @s Pos[0] 100',
                         'execute store result score @s bm.lsy run data get entity @s Pos[1] 100',
                         'execute store result score @s bm.lsz run data get entity @s Pos[2] 100', 'scoreboard players set @s bm.lsd 3'] +
       [f'execute if dimension {d} run scoreboard players set @s bm.lsd {i}' for d, i in dims])
    # in lava with a charm: saved (checked every 5 ticks; feet or eyes in lava)
    fast += [f'execute as @a[gamemode=!spectator,gamemode=!creative] at @s if block ~ ~ ~ minecraft:lava if items entity @s container.* {lava} run function bm:p38/lava/save',
             f'execute as @a[gamemode=!spectator,gamemode=!creative] at @s if block ~ ~ ~ minecraft:lava if items entity @s weapon.offhand {lava} run function bm:p38/lava/save',
             f'execute as @a[gamemode=!spectator,gamemode=!creative] at @s if block ~ ~1 ~ minecraft:lava if items entity @s container.* {lava} run function bm:p38/lava/save',
             f'execute as @a[gamemode=!spectator,gamemode=!creative] at @s if block ~ ~1 ~ minecraft:lava if items entity @s weapon.offhand {lava} run function bm:p38/lava/save']
    fn('p38/lava/use', ['execute unless block ~ ~ ~ minecraft:lava unless block ~ ~1 ~ minecraft:lava run return run ' + say('The charm only works in lava.'),
                        'function bm:p38/lava/save'])
    fn('p38/lava/save', ['scoreboard players set #here bm.rng 3'] + [f'execute if dimension {d} run scoreboard players set #here bm.rng {i}' for d, i in dims] +
       ['scoreboard players set #ok bm.rng 0',
        'execute if score @s bm.lsd = #here bm.rng run function bm:p38/lava/back',
        'execute if score #ok bm.rng matches 0 run function bm:p38/lava/search',
        'execute if score #ok bm.rng matches 0 run return run ' + say('The charm finds no safe ground nearby!', 'red'),
        f'clear @s {lava} 1', 'effect give @s minecraft:fire_resistance 10 0 true',
        'execute at @s run function bm:p38/lava/douse',
        'execute at @s run particle minecraft:cloud ~ ~1 ~ 0.4 0.6 0.4 0.05 20',
        'execute at @s run playsound minecraft:block.fire.extinguish player @a[distance=..16] ~ ~ ~ 1 0.8',
        say('The Lava Charm cracks - and you\'re out!', '#ff7a1a')])
    fn('p38/lava/back', ['execute store result storage bm:tmp lv.x double 0.01 run scoreboard players get @s bm.lsx',
                         'execute store result storage bm:tmp lv.y double 0.01 run scoreboard players get @s bm.lsy',
                         'execute store result storage bm:tmp lv.z double 0.01 run scoreboard players get @s bm.lsz',
                         'function bm:p38/lava/back_m with storage bm:tmp lv'])
    # only if that ground is still safe (lava flows) and within 64 blocks
    fn('p38/lava/back_m', ['$execute positioned $(x) $(y) $(z) unless entity @s[distance=..64] run return 0',
                           '$execute positioned $(x) $(y) $(z) if block ~ ~ ~ #bm:p38_hot run return 0',
                           '$execute positioned $(x) $(y) $(z) if block ~ ~1 ~ minecraft:lava run return 0',
                           '$execute positioned $(x) $(y) $(z) if block ~ ~-0.5 ~ minecraft:lava run return 0',
                           '$tp @s $(x) $(y) $(z)', 'scoreboard players set #ok bm.rng 1'])
    # no remembered ground: columns around you, from 8 below to 24 above, nearest first
    offs = [(0, 0), (3, 0), (-3, 0), (0, 3), (0, -3), (6, 0), (-6, 0), (0, 6), (0, -6), (6, 6), (-6, -6), (6, -6), (-6, 6),
            (12, 0), (-12, 0), (0, 12), (0, -12), (12, 12), (-12, -12), (12, -12), (-12, 12)]
    fn('p38/lava/search', [f'execute if score #ok bm.rng matches 0 align xyz positioned ~{dx}.5 ~-8 ~{dz}.5 run function bm:p38/lava/col_start' for dx, dz in offs])
    fn('p38/lava/col_start', ['scoreboard players set #cy bm.rng 32', 'function bm:p38/lava/col'])
    fn('p38/lava/col', ['execute if block ~ ~ ~ #bm:grap_pass unless block ~ ~ ~ #bm:p38_hot if block ~ ~1 ~ #bm:grap_pass unless block ~ ~1 ~ #bm:p38_hot '
                        'unless block ~ ~-1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:p38_hot run return run function bm:p38/lava/found',
                        'scoreboard players remove #cy bm.rng 1', 'execute if score #cy bm.rng matches 1.. positioned ~ ~1 ~ run function bm:p38/lava/col'])
    fn('p38/lava/found', ['tp @s ~ ~ ~', 'scoreboard players set #ok bm.rng 1'])
    # putting the fire out: a puff of water for two ticks where you land (only into air), plus the Fire Resistance
    fn('p38/lava/douse', ['execute unless block ~ ~ ~ #minecraft:air run return 0', 'setblock ~ ~ ~ minecraft:water',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.lvw"]}', 'schedule function bm:p38/lava/dry 2t append'])
    fn('p38/lava/dry', ['execute as @e[type=minecraft:marker,tag=bm.lvw] at @s run function bm:p38/lava/dry1'])
    fn('p38/lava/dry1', ['execute if block ~ ~ ~ minecraft:water run setblock ~ ~ ~ minecraft:air', 'kill @s'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.lvw] at @s run function bm:p38/lava/dry1')     # in case a reload ate the schedule

    for t, pct in SURFACE_LOOT.items():
        G.FUNCS[f'loot/{t}'] += ['execute store result score @s bm.rng run random value 1..100',
                                 f'execute if score @s bm.rng matches 1..{pct} run function bm:p38/found_surface']
    for t, pct in LAVA_LOOT.items():
        G.FUNCS[f'loot/{t}'] += ['execute store result score @s bm.rng run random value 1..100',
                                 f'execute if score @s bm.rng matches 1..{pct} run function bm:p38/found_lava']
    fn('p38/found_surface', [give('surface_charm'), tellraw('@s', PREFIX + [T('A Surface Charm was tucked among the loot!', '#8fd16a')])])
    fn('p38/found_lava', [give('lava_charm'), tellraw('@s', PREFIX + [T('A Lava Charm sits cool among the loot!', '#ff7a1a')])])

    # ------------------------------------------------------------------ cosmetic charms: the rainbow, and the rare monsters' own
    arc = []
    for i, c in enumerate(RAINBOW * 1):
        a = -70 + i * (140 / (len(RAINBOW) - 1))
        import math
        x, y = 0.55 * math.sin(math.radians(a)), 2.35 + 0.35 * math.cos(math.radians(a))
        r, g, b = (int(c[k:k + 2], 16) / 255 for k in (1, 3, 5))
        arc.append(f'particle minecraft:dust{{color:[{r:.2f},{g:.2f},{b:.2f}],scale:0.8}} ^{x:.2f} ^{y:.2f} ^ 0 0 0 0 1')
    fn('p38/charm/rainbow', ['execute rotated ~ 0 run function bm:p38/charm/rainbow_arc'])
    fn('p38/charm/rainbow_arc', arc)
    pick = G.FUNCS['p17/charm/pick']
    lines = []
    for k, (_, _, _, _, _, parts) in RARE.items():
        fn(f'p38/charm/{k}', parts)
    for k in list(RARE) + ['rainbow']:
        lines += [f'execute if items entity @s container.* {holds % ("charm_" + k)} run return run function bm:p38/charm/{k}',
                  f'execute if items entity @s weapon.offhand {holds % ("charm_" + k)} run return run function bm:p38/charm/{k}']
    pick[2:2] = lines                     # after the legendary Blood Eclipse, before the shop charms

    # ------------------------------------------------------------------ rare monsters
    pool = lambda e, conds: {'rolls': 1, 'entries': e, 'conditions': conds}
    looting = {'condition': 'minecraft:random_chance_with_enchanted_bonus', 'enchantment': 'minecraft:looting', 'unenchanted_chance': 0.35,
               'enchanted_chance': {'type': 'minecraft:linear', 'base': 0.45, 'per_level_above_first': 0.1}}
    for k, (mob, mname, cname, col, _, _) in RARE.items():
        hp = (G.ARMORED[mob][0] if mob in G.ARMORED else G.UNARMORED[mob]) * 2
        G.FUNCS[f'mobs/init/{mob}'].append(f'execute if score #r bm.rng matches {RARE_ROLL[0]}..{RARE_ROLL[1]} run return run function bm:p38/rare/{k}')
        fn(f'p38/rare/{k}', [f'data merge entity @s {snbt({"DeathLootTable": f"bm:p38/rare_{k}", "CustomName": T(mname, col, bold=True)})}',
                             'tag @s add bm.rare', 'tag @s add bm.tiered',
                             f'attribute @s minecraft:max_health base set {hp}', f'data modify entity @s Health set value {hp}.0f'])
        fast.append(f'execute as @e[type=minecraft:{mob},tag=bm.rare] at @s run function bm:p38/charm/{k}')
        wjson(f'bm/loot_table/p38/rare_{k}.json', {'type': 'minecraft:entity', 'pools': [
            {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{mob}'}]},
            pool([G.loot_entry(f'charm_{k}')], [G.KILLED, looting]),
            pool([G.loot_entry('token', G.uni(2, 4))], [G.KILLED])]})
        fn(f'admin/rare/{k}', [f'summon minecraft:{mob} ~ ~ ~ {{Tags:["bm.seen"]}}',
                               f'execute as @e[type=minecraft:{mob},tag=bm.seen,tag=!bm.rare,distance=..1,limit=1,sort=nearest] run function bm:p38/rare/{k}'])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/rare/<cinder|starlit|glimmer|bloom|void|ashen>', 'yellow'),
                                             T('  a rare monster (its charm: 35% + Looting)', 'gray')])]

    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    charm = ['................', '......KKKK......', '.....K....K.....', '.....K....K.....', '......K..K......', '.......KK.......',
             '......KggK......', '.....KgGGgK.....', '....KgGWGGgK....', '....KGGGGGGK....', '....KGGGGGdK....', '.....KGGGdK.....',
             '......KGdK......', '.......KK.......', '................', '................']
    for k, (_, _, _, col, _, _) in RARE.items():
        R.ICONS[f'charm_{k}'] = grid(charm, dict(K='#2b2b33', g='#e0e0f0', G=col, W='#ffffff', d='#3a3a44'))
    R.ICONS['charm_rainbow'] = grid(['................', '................', '.....RRRRRR.....', '...RROOOOOORR...', '..ROOYYYYYYOOR..', '.ROYYGGGGGGYYOR.',
                                     '.ROYGBBBBBBGYOR.', 'ROYGBVVVVVVBGYOR', 'ROYGBV....VBGYOR', 'ROYGBV....VBGYOR', 'ROYGBV....VBGYOR', '................',
                                     '................', '................', '................', '................'],
                                    dict(R=RAINBOW[0], O=RAINBOW[1], Y=RAINBOW[2], G=RAINBOW[3], B=RAINBOW[4], V=RAINBOW[6]))
    R.ICONS['surface_charm'] = grid(['................', '.......YY.......', '......YYYY......', '.....YYYYYY.....', '....YY.YY.YY....', '.......YY.......',
                                     '.......YY.......', '.....KKKKKK.....', '....KGGGGGGK....', '...KGGgGGGGGK...', '...KGGGGGGGGK...', '...KGGGGGgGGK...',
                                     '....KGGGGGGK....', '.....KKKKKK.....', '................', '................'],
                                    dict(Y='#ffe14a', K='#3a3a2a', G='#8fd16a', g='#c8f0a8'))
    R.ICONS['lava_charm'] = grid(['................', '.......KK.......', '......KOOK......', '......KOOK......', '.....KOOOOK.....', '.....KOYOOK.....',
                                  '....KOYYOOOK....', '....KOYOOOOK....', '...KOOOOOORK....', '...KOOOOORRK....', '...KOOOORRRK....', '....KOORRRK.....',
                                  '.....KRRRK......', '......KKK.......', '................', '................'],
                                 dict(K='#2a1a10', O='#ff7a1a', Y='#ffe14a', R='#c83a10'))
