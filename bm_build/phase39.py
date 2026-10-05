"""Phase 1.25 / 2.18: treasure of the wide world (with a nod to Terraria).

ACCESSORIES AND TOOLS, each a rare find in the vanilla chests that suit it (and in Mimics and fishing crates):
- CLIMBING CLAWS (jungle temples): in the air, push into a wall to climb it; let go of forward to slide down slowly.
- UMBRELLA (shipwreck supplies, outposts): held in either hand, you drift down gently instead of falling.
- ICE SKATES (igloos): boots - Speed II on any ice.
- WATER WALKING BOOTS (buried treasure, ocean ruins): stride across water; you bob up if you fall in. Sneak to sink.
- ROD OF DISCORD (ancient cities): teleport to where you look (24 blocks). Costs 2 hearts' worth... and more if you use
  it again within a few seconds.
- BOTTOMLESS WATER / LAVA BUCKET (shipwreck supplies / ruined portals): pour forever. Sneak + use: soak the fluid up (5x5x5).
- EXTENDO GRIP (outposts, mansions): +3 block reach in the off hand.
- LIFEFORM ANALYZER (strongholds): names the nearest rare monster within 64 blocks and points the way.
- METAL DETECTOR (mineshafts): held, it reports ancient debris, diamond, emerald and gold ore within 8 blocks.
- ENCHANTED SUNDIAL (desert temples): at night, skip to morning. Recharges in one full day; not on special nights.
- BAND OF REGENERATION (dungeon chests): Regeneration I after 5 seconds without taking damage.
- COBALT SHIELD (fortresses): immune to knockback while held.
- OBSIDIAN SKULL (bastions): fire blocks, campfires and magma blocks can't hurt you (lava still can).
MIMICS: 1 in 100 vanilla loot chests is a Mimic. It hops out snapping (the chest's loot is kept inside it); kill it and
  the chest comes back with its loot, plus a guaranteed accessory from the list above.
FALLEN STARS: on clear Overworld nights stars streak down near players and land glowing (they fade at dawn).
  Right-click with 9 to make a STAR CLOAK: when you're hurt, stars strike up to 3 nearby monsters (3 s cooldown).
  The Professor and Lucky Whiskers buy stars.
FISHING CRATES: any catch can bring up a Wooden (5%), Iron (1.5%) or Golden (0.4%) Crate. Right-click to open.
SWORD SHRINES: a very rare mossy shrine in grassy and wooded biomes, with a sword in stone. Pull it out: the
  ENCHANTED SWORD - at full health, right-click fires a sword beam."""
import math
from items import item, gear, attr, ench, T, TOTEM, weapon_attrs, DYNAMIC
from useitem import hold, HOLD

ACC = {  # id: (name, colour, lore lines, extra comps, chest tables {table: %})
    'climbing_claws': ('Climbing Claws', '#c8a070', [('In the air, push into a wall: climb it.', 'blue'), ('Let go of forward to slide down slowly.', 'blue'),
                                                    ('Works from your inventory.', 'gray')], {}, {'jungle_temple': 10}),
    'umbrella': ('Umbrella', '#e84a6a', [('Held in either hand: drift down gently', 'blue'), ('instead of falling.', 'blue')], {},
                 {'shipwreck_supply': 6, 'pillager_outpost': 3}),
    'rod_of_discord': ('Rod of Discord', '#d86aff', [('Right-click: teleport to where you look', 'blue'), ('(up to 24 blocks).', 'blue'),
                                                    ('Costs health - more if used again within', 'red'), ('a few seconds. It can kill you.', 'red')],
                       hold('none'), {'ancient_city': 3}),
    'bottomless_water': ('Bottomless Water Bucket', '#3a8aff', [('Right-click: pour water. It never runs dry.', 'blue'),
                                                               ('Sneak + right-click: soak water up (5x5x5).', 'blue')], hold('none'), {'shipwreck_supply': 4}),
    'bottomless_lava': ('Bottomless Lava Bucket', '#ff7a1a', [('Right-click: pour lava. It never runs dry.', 'blue'),
                                                             ('Sneak + right-click: soak lava up (5x5x5).', 'blue')], hold('none'), {'ruined_portal': 5}),
    'extendo_grip': ('Extendo Grip', '#ffd23f', [('In your off hand: +3 block reach.', 'blue')],
                     {'minecraft:attribute_modifiers': [attr('block_interaction_range', 3, 'offhand', ident='bm:extendo_grip')]},
                     {'pillager_outpost': 5, 'woodland_mansion': 6}),
    'lifeform_analyzer': ('Lifeform Analyzer', '#5aff9a', [('Names the nearest rare monster within', 'blue'), ('64 blocks and points the way.', 'blue'),
                                                          ('Works from your inventory (held: always reports).', 'gray')], {},
                          {'stronghold_corridor': 4, 'stronghold_crossing': 4, 'stronghold_library': 6}),
    'metal_detector': ('Metal Detector', '#c8c8d8', [('Held: reports ancient debris, diamond,', 'blue'), ('emerald and gold ore within 8 blocks.', 'blue')], {},
                       {'abandoned_mineshaft': 4}),
    'enchanted_sundial': ('Enchanted Sundial', '#ffd23f', [('At night, right-click: skip to morning.', 'blue'), ('Recharges in one full day.', 'gray'),
                                                          ('Not on Blood Moons or other special nights.', 'dark_gray')], hold('none'), {'desert_pyramid': 4}),
    'band_of_regeneration': ('Band of Regeneration', '#ff5a7a', [('Regeneration I after 5 seconds', 'blue'), ('without taking damage.', 'blue'),
                                                                ('Works from your inventory.', 'gray')], {}, {'simple_dungeon': 5}),
    'obsidian_skull': ('Obsidian Skull', '#6a4a9a', [('Fire, campfires and magma blocks', 'blue'), ('can\'t hurt you. (Lava still can.)', 'blue'),
                                                    ('Works from your inventory.', 'gray')], {}, {'bastion_other': 6, 'bastion_treasure': 10}),
}
for iid, (nm, col, lore, comps, _) in ACC.items():
    item(iid, TOTEM, nm, col, ['A treasure of the wide world.'] + lore, model=f'bm:{iid}', stack=1, cat='relic', comps=comps)
for iid in ('rod_of_discord', 'bottomless_water', 'bottomless_lava', 'enchanted_sundial'):
    HOLD[iid] = f'bm:p39/{iid}/use'
# boots and the shield are real gear
item('ice_skates', 'minecraft:leather_boots', 'Ice Skates', '#bfefff', ['A treasure of the wide world.', ('Speed II on any ice.', 'blue')],
     model='bm:ice_skates', stack=1, cat='relic', comps={'minecraft:dyed_color': 0xBFEFFF, 'minecraft:unbreakable': {}})
item('water_walking_boots', 'minecraft:leather_boots', 'Water Walking Boots', '#3a8aff',
     ['A treasure of the wide world.', ('Stride across water. Fall in and you', 'blue'), ('bob back up. Sneak to sink.', 'blue')],
     model='bm:water_walking_boots', stack=1, cat='relic', comps={'minecraft:dyed_color': 0x3A8AFF, 'minecraft:unbreakable': {}})
item('cobalt_shield', 'minecraft:shield', 'Cobalt Shield', '#3a5aff', ['A treasure of the wide world.', ('Held: immune to knockback.', 'blue')],
     stack=1, cat='relic', comps={'minecraft:base_color': 'blue', 'minecraft:unbreakable': {},
                                  'minecraft:attribute_modifiers': [attr('knockback_resistance', 1, 'offhand', ident='bm:cobalt_off'),
                                                                    attr('knockback_resistance', 1, 'mainhand', ident='bm:cobalt_main')]})
ACC_ALL = list(ACC) + ['ice_skates', 'water_walking_boots', 'cobalt_shield']
CHEST_ACC = dict({k: v[4] for k, v in ACC.items()}, ice_skates={'igloo_chest': 15}, water_walking_boots={'buried_treasure': 8, 'underwater_ruin_big': 5},
                 cobalt_shield={'nether_bridge': 6})

# stars, crates, the shrine sword
item('fallen_star', TOTEM, 'Fallen Star', '#ffe85a', ['Still warm from the sky.', ('Right-click with 9: a Star Cloak.', 'blue'),
                                                     ('The Professor and Lucky Whiskers buy them.', 'gray')], model='bm:fallen_star', stack=64, cat='relic',
     glint=True, comps=hold('none'))
HOLD['fallen_star'] = 'bm:p39/star/use'
item('star_cloak', TOTEM, 'Star Cloak', '#ffe85a', ['Nine stars, stitched with moonlight.', ('When you\'re hurt, stars strike up to', 'blue'),
                                                   ('3 nearby monsters (3 s cooldown).', 'blue'), ('Works from your inventory.', 'gray')],
     model='bm:star_cloak', stack=1, cat='relic', glint=True, bold=True)
CRATES = {'wooden': ('Wooden Crate', '#b8864a'), 'iron': ('Iron Crate', '#d8d8e0'), 'golden': ('Golden Crate', '#ffd23f')}
for c, (nm, col) in CRATES.items():
    item(f'crate_{c}', TOTEM, nm, col, ['Fished up, still dripping.', ('Right-click to open.', 'blue')], model=f'bm:crate_{c}', stack=16, cat='relic',
         comps=hold('none'))
    HOLD[f'crate_{c}'] = f'bm:p39/crate/{c}'
gear('enchanted_sword', 'diamond_sword', 'Enchanted Sword', '#7ab8ff',
     ['Pulled from the stone of a forgotten shrine.', ('At full health, right-click:', 'blue'), ('fire a sword beam (1 s cooldown).', 'blue')],
     ench(sharpness=4, unbreaking=3, looting=1), 2, attrs=weapon_attrs('diamond_sword', 1), model='bm:enchanted_sword', extra=hold('none'))
HOLD['enchanted_sword'] = 'bm:p39/sword/use'

SHRINE_BIOMES = ['plains', 'sunflower_plains', 'forest', 'flower_forest', 'birch_forest', 'old_growth_birch_forest', 'meadow', 'cherry_grove',
                 'taiga', 'savanna', 'dark_forest']
MIMIC_TABLES = None          # every chest table the pack hooks (filled in generate)


def extend_offers(O, offer):
    O['professor'] += [offer(('fallen_star', 3), ('token', 1))]
    O['lucky'] += [offer(('fallen_star', 5), ('lucky_token', 1))]


def generate(G):
    fn, wjson, title, give, tellraw, PREFIX = G.fn, G.wjson, G.title, G.give, G.tellraw, G.PREFIX
    from nbt import snbt, B, F, Int
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    objs = ['bm.rodr dummy', 'bm.dmgt minecraft.custom:minecraft.damage_taken', 'bm.bandt dummy', 'bm.bandc dummy', 'bm.scd dummy',
            'bm.mimid dummy', 'bm.swcd dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs] + ['scoreboard players set #24000 bm.rng 24000']
    G.OBJECTIVES += [o.split()[0] for o in objs]
    tick, fast, second = [], [], []
    inv = lambda iid: [f'container.* {holds % iid}', f'weapon.offhand {holds % iid}']     # "anywhere in your inventory"

    # ------------------------------------------------------------------ chest hooks (new tables get their own advancement)
    def hook(t):
        if f'loot/{t}' not in G.FUNCS:
            wjson(f'bm/advancement/loot/{t}.json', {'criteria': {'opened': {'trigger': 'minecraft:player_generates_container_loot',
                                                                            'conditions': {'loot_table': f'minecraft:chests/{t}'}}},
                                                    'rewards': {'function': f'bm:loot/{t}'}})
            fn(f'loot/{t}', [f'advancement revoke @s only bm:loot/{t}'])
        return G.FUNCS[f'loot/{t}']
    for iid, tables in CHEST_ACC.items():
        fn(f'p39/found/{iid}', [give(iid), tellraw('@s', PREFIX + [T('Treasure! ', 'gold', bold=True), T('You found ', 'gray'),
                                                                   T(G.ITEMS[iid]['name'], 'yellow'), T(' in the chest.', 'gray')]),
                                'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4'])
        for t, pct in tables.items():
            hook(t).extend(['execute store result score @s bm.rng run random value 1..100',
                            f'execute if score @s bm.rng matches 1..{pct} run function bm:p39/found/{iid}'])
    acc_entry = [G.loot_entry(i) for i in ACC_ALL]

    # ------------------------------------------------------------------ Climbing Claws (every tick, holders only)
    wjson('bm/predicate/p39/forward.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                            'predicate': {'minecraft:type_specific/player': {'input': {'forward': True}}}})
    wjson('bm/predicate/p39/on_ground.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}})
    for slot in inv('climbing_claws'):
        tick.append(f'execute as @a[gamemode=!spectator] if items entity @s {slot} at @s run function bm:p39/claws/tick')
    tick.append('execute as @a[tag=bm.climb] unless items entity @s container.* %s unless items entity @s weapon.offhand %s run function bm:p39/claws/off'
                % (holds % 'climbing_claws', holds % 'climbing_claws'))
    fn('p39/claws/wall', ['execute rotated ~ 0 positioned ^ ^ ^0.55 unless block ~ ~ ~ #bm:grap_pass run return 1',
                          'execute rotated ~ 0 positioned ^ ^1 ^0.55 unless block ~ ~ ~ #bm:grap_pass run return 1', 'return 0'])
    fn('p39/claws/tick', ['execute if predicate bm:p39/on_ground run return run function bm:p39/claws/off',
                          'execute unless function bm:p39/claws/wall run return run function bm:p39/claws/off',
                          'tag @s add bm.climb',
                          'execute if predicate bm:p39/forward run return run effect give @s minecraft:levitation 1 2 true',
                          'effect clear @s minecraft:levitation', 'effect give @s minecraft:slow_falling 1 0 true'])
    fn('p39/claws/off', ['execute if entity @s[tag=bm.climb] run effect clear @s minecraft:levitation', 'tag @s remove bm.climb'])

    # ------------------------------------------------------------------ Umbrella, Ice Skates, Obsidian Skull (every 5 ticks)
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.* {holds % "umbrella"} at @s unless predicate bm:p39/on_ground '
                'unless block ~ ~ ~ minecraft:water run effect give @s minecraft:slow_falling 1 0 true')
    fast.append(f'execute as @a[gamemode=!spectator] if items entity @s armor.feet {holds % "ice_skates"} at @s if block ~ ~-0.5 ~ #minecraft:ice '
                'run effect give @s minecraft:speed 1 1 true')
    wjson('bm/tags/block/p39_hot.json', {'values': ['minecraft:fire', 'minecraft:soul_fire', 'minecraft:campfire', 'minecraft:soul_campfire', 'minecraft:magma_block']})
    for slot in inv('obsidian_skull'):
        fast += [f'execute as @a[gamemode=!spectator] if items entity @s {slot} at @s if block ~ ~ ~ #bm:p39_hot run effect give @s minecraft:fire_resistance 1 0 true',
                 f'execute as @a[gamemode=!spectator] if items entity @s {slot} at @s if block ~ ~-0.5 ~ #bm:p39_hot run effect give @s minecraft:fire_resistance 1 0 true']

    # ------------------------------------------------------------------ Water Walking Boots (every tick, wearers only)
    # levitation 255 is "no vertical pull": hover just above the surface; levitation III lifts you out if you're in
    wwb = holds % 'water_walking_boots'
    tick += [f'execute as @a[gamemode=!spectator] if items entity @s armor.feet {wwb} at @s run function bm:p39/wwalk/tick',
             f'execute as @a[tag=bm.wwk] unless items entity @s armor.feet {wwb} run function bm:p39/wwalk/off']
    fn('p39/wwalk/tick', ['execute if predicate bm:p20/sneaking run return run function bm:p39/wwalk/off',
                          'execute if block ~ ~ ~ minecraft:water run return run function bm:p39/wwalk/rise',
                          'execute if block ~ ~-0.35 ~ minecraft:water run return run function bm:p39/wwalk/hover',
                          'function bm:p39/wwalk/off'])
    fn('p39/wwalk/rise', ['tag @s add bm.wwk', 'effect give @s minecraft:levitation 1 2 true'])
    fn('p39/wwalk/hover', ['tag @s add bm.wwk', 'effect give @s minecraft:levitation 1 255 true',
                           'execute store result score #r bm.rng run random value 1..6',
                           'execute if score #r bm.rng matches 1 run particle minecraft:splash ~ ~0.05 ~ 0.3 0 0.3 0 3'])
    fn('p39/wwalk/off', ['execute if entity @s[tag=bm.wwk] run effect clear @s minecraft:levitation', 'tag @s remove bm.wwk'])

    # ------------------------------------------------------------------ Rod of Discord
    fn('p39/rod_of_discord/use', ['execute unless function bm:p37/allowed run return run ' + say('The rod sputters - warded ground.'),
                                  'scoreboard players set #ok bm.rng 0', 'scoreboard players set #ray bm.rng 48',
                                  'execute anchored eyes positioned ^ ^ ^ run function bm:p39/rod_of_discord/ray',
                                  'execute if score #ok bm.rng matches 0 run return run ' + say('No room to land there.'),
                                  'scoreboard players add @s bm.rodr 1', 'scoreboard players operation #d bm.rng = @s bm.rodr',
                                  'scoreboard players operation #d bm.rng *= #4 bm.rng',
                                  'execute store result storage bm:tmp rod.d int 1 run scoreboard players get #d bm.rng',
                                  'function bm:p39/rod_of_discord/hurt with storage bm:tmp rod',
                                  title('@s', 'actionbar', [T('Chaos State ', '#d86aff'), {'score': {'name': '@s', 'objective': 'bm.rodr'}, 'color': 'white'},
                                                            T(' - wait a few seconds or it hurts more.', 'gray')])])
    fn('p39/rod_of_discord/hurt', ['$damage @s $(d) minecraft:magic'])
    # step forward half a block at a time until the next step is solid; then land where feet and head fit
    fn('p39/rod_of_discord/ray', ['execute positioned ^ ^ ^0.5 unless block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^-0.5 run return run function bm:p39/rod_of_discord/land',
                                  'scoreboard players remove #ray bm.rng 1',
                                  'execute if score #ray bm.rng matches 0 run return run function bm:p39/rod_of_discord/land',
                                  'execute positioned ^ ^ ^0.5 run function bm:p39/rod_of_discord/ray'])
    fn('p39/rod_of_discord/land', ['execute unless function bm:p37/allowed run return 0',
                                   'execute positioned ~ ~-1.5 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~ ~ minecraft:lava run return run function bm:p39/rod_of_discord/go',
                                   'execute positioned ~ ~-1 ~ if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~ ~ minecraft:lava run return run function bm:p39/rod_of_discord/go',
                                   'execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~ ~ minecraft:lava run return run function bm:p39/rod_of_discord/go'])
    fn('p39/rod_of_discord/go', ['execute at @s run particle minecraft:witch ~ ~1 ~ 0.3 0.6 0.3 0.1 20', 'tp @s ~ ~ ~',
                                 'particle minecraft:witch ~ ~1 ~ 0.3 0.6 0.3 0.1 20', 'playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 1.3',
                                 'scoreboard players set #ok bm.rng 1'])
    second.append('execute as @a[scores={bm.rodr=1..}] run function bm:p39/rod_of_discord/cool')
    fn('p39/rod_of_discord/cool', ['execute store result score #g bm.rng run time query gametime',
                                   'scoreboard players operation #g bm.rng %= #3 bm.rng', 'execute if score #g bm.rng matches 0 run scoreboard players remove @s bm.rodr 1'])

    # ------------------------------------------------------------------ Bottomless buckets
    wjson('bm/tags/block/p39_watery.json', {'values': ['minecraft:water', 'minecraft:seagrass', 'minecraft:tall_seagrass', 'minecraft:kelp',
                                                       'minecraft:kelp_plant', 'minecraft:bubble_column']})
    for fl, soak in (('water', '#bm:p39_watery'), ('lava', 'minecraft:lava')):
        b = f'bottomless_{fl}'
        fn(f'p39/{b}/use', ['execute if predicate bm:p20/sneaking run return run function bm:p39/%s/soak_start' % b,
                            *(['execute if dimension minecraft:the_nether run return run ' + say('The water would boil away here.')] if fl == 'water' else []),
                            'scoreboard players set #ray bm.rng 25', f'execute anchored eyes positioned ^ ^ ^ run function bm:p39/{b}/ray'])
        fn(f'p39/{b}/ray', [f'execute positioned ^ ^ ^0.2 unless block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^-0.2 run return run function bm:p39/{b}/pour',
                            f'execute positioned ^ ^ ^0.2 if block ~ ~ ~ minecraft:{fl} positioned ^ ^ ^-0.2 run return run function bm:p39/{b}/pour',
                            'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p39/{b}/ray'])
        fn(f'p39/{b}/pour', ['execute unless function bm:p37/allowed run return run ' + say('Warded ground - the bucket won\'t pour.'),
                             'execute unless block ~ ~ ~ #bm:grap_pass run return 0', f'setblock ~ ~ ~ minecraft:{fl}',
                             f'playsound minecraft:item.bucket.empty{"_lava" if fl == "lava" else ""} player @a[distance=..16] ~ ~ ~ 1 1'])
        fn(f'p39/{b}/soak_start', ['scoreboard players set #ray bm.rng 25', f'execute anchored eyes positioned ^ ^ ^ run function bm:p39/{b}/soak_ray'])
        fn(f'p39/{b}/soak_ray', [f'execute if block ~ ~ ~ {soak} run return run function bm:p39/{b}/soak',
                                 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                                 'scoreboard players remove #ray bm.rng 1', f'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p39/{b}/soak_ray'])
        fn(f'p39/{b}/soak', ['execute unless function bm:p37/allowed run return run ' + say('Warded ground - the bucket won\'t drink here.'),
                             f'fill ~-2 ~-2 ~-2 ~2 ~2 ~2 minecraft:air replace {soak}',
                             f'playsound minecraft:item.bucket.fill{"_lava" if fl == "lava" else ""} player @a[distance=..16] ~ ~ ~ 1 1'])

    # ------------------------------------------------------------------ Lifeform Analyzer (rare monsters, phase38)
    import phase38 as P38
    wjson('bm/tags/entity_type/p39_rare.json', {'values': sorted({f'minecraft:{v[0]}' for v in P38.RARE.values()})})
    rare_sel = '@e[type=#bm:p39_rare,tag=bm.rare,distance=..64]'
    for slot in inv('lifeform_analyzer'):
        second.append(f'execute as @a[gamemode=!spectator] if items entity @s {slot} at @s run function bm:p39/analyzer')
    comp = G.FUNCS['p17/compass']
    a = comp.index('summon minecraft:marker ~ ~ ~ {Tags:["bm.cm"]}')
    z = next(i for i, l in enumerate(comp) if l.startswith('scoreboard players set #mon bm.rng'))
    nav = comp[a:z]
    from phase17 import ARROWS
    fn('p39/analyzer', ['tag @e[tag=bm.ctgt] remove bm.ctgt',
                        f'execute unless entity {rare_sel} if items entity @s weapon.* {holds % "lifeform_analyzer"} run return run ' +
                        say('Lifeform Analyzer: no rare creatures within 64 blocks.'),
                        f'execute unless entity {rare_sel} run return 0',
                        f'tag @e[type=#bm:p39_rare,tag=bm.rare,distance=..64,sort=nearest,limit=1] add bm.ctgt'] + nav +
       [f'execute if score #ty bm.rng matches {i} run ' + title('@s', 'actionbar', [T(arw + '  ', '#5aff9a', bold=True), {'selector': '@e[tag=bm.ctgt,limit=1]'},
                                                                                    T('  ·  ', 'gray'), {'score': {'name': '#big', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                                    T(' blocks', 'gray')]) for i, arw in enumerate(ARROWS)] +
       ['tag @e[tag=bm.ctgt] remove bm.ctgt'])

    # ------------------------------------------------------------------ Metal Detector (held; every other second)
    # counting ore without changing anything for longer than one command: swap to structure void and straight back (strict: no updates)
    ORES = [('ancient_debris', 'Ancient Debris', '#a0683a', ['ancient_debris']), ('diamond', 'Diamond', '#5ae8ff', ['diamond_ore', 'deepslate_diamond_ore']),
            ('emerald', 'Emerald', '#3aff6a', ['emerald_ore', 'deepslate_emerald_ore']), ('gold', 'Gold', '#ffd23f', ['gold_ore', 'deepslate_gold_ore', 'nether_gold_ore'])]
    second.append(f'execute as @a[gamemode=!spectator] if items entity @s weapon.* {holds % "metal_detector"} at @s run function bm:p39/detector')
    det = ['execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #40 bm.rng',
           'execute unless score #g bm.rng matches 0..19 run return 0', 'execute unless function bm:p37/allowed run return 0']
    parts = []
    for k, nm, col, blocks in ORES:
        det.append(f'scoreboard players set #o_{k} bm.rng 0')
        for bl in blocks:
            det += [f'execute store result score #c bm.rng run fill ~-8 ~-8 ~-8 ~8 ~8 ~8 minecraft:structure_void replace minecraft:{bl} strict',
                    f'execute if score #c bm.rng matches 1.. run fill ~-8 ~-8 ~-8 ~8 ~8 ~8 minecraft:{bl} replace minecraft:structure_void strict',
                    f'scoreboard players operation #o_{k} bm.rng += #c bm.rng']
        parts.append((k, nm, col))
    det += ['scoreboard players set #any bm.rng 0'] + [f'execute if score #o_{k} bm.rng matches 1.. run scoreboard players set #any bm.rng 1' for k, _, _ in parts]
    det.append('execute if score #any bm.rng matches 0 run return run ' + say('Metal Detector: nothing valuable within 8 blocks.'))
    msg = [T('Metal Detector: ', 'gray')]
    for k, nm, col in parts:
        msg += [{'text': '', 'extra': [T(nm + ' ', col), {'score': {'name': f'#o_{k}', 'objective': 'bm.rng'}, 'color': 'white'}, T('  ', 'gray')]}]
    det.append(title('@s', 'actionbar', msg))
    fn('p39/detector', det)
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #40 bm.rng 40']

    # ------------------------------------------------------------------ Enchanted Sundial (world-wide; one full day to recharge)
    fn('p39/enchanted_sundial/use', ['execute unless dimension minecraft:overworld run return run ' + say('The sundial needs the Overworld\'s sun.'),
                                     'execute if score #tod bm.bm matches 0..12499 run return run ' + say('It\'s already day.'),
                                     'execute if score #tod bm.bm matches 23500.. run return run ' + say('Dawn is nearly here anyway.'),
                                     'execute if score #active bm.bm matches 1 run return run ' + say('The sundial won\'t turn under a Blood Moon.', 'red'),
                                     'execute if score #inv bm.bm matches 1 run return run ' + say('The sundial won\'t turn on an Invasion Night.', 'red'),
                                     'execute if score #lnight bm.bm matches 1 run return run ' + say('The sundial won\'t turn on a Lucky Night.', 'yellow'),
                                     'execute store result score #g bm.rng run time query gametime',
                                     'scoreboard players operation #g2 bm.rng = #g bm.rng', 'scoreboard players operation #g2 bm.rng -= #sundial bm.rng',
                                     'execute if score #sundial bm.rng matches 1.. if score #g2 bm.rng matches ..23999 run return run ' +
                                     say('The sundial is still recharging (one full day).'),
                                     'scoreboard players operation #sundial bm.rng = #g bm.rng',
                                     'scoreboard players set #skip bm.rng 24000', 'scoreboard players operation #skip bm.rng -= #tod bm.bm',
                                     'execute store result storage bm:tmp sun.t int 1 run scoreboard players get #skip bm.rng',
                                     'function bm:p39/enchanted_sundial/skip with storage bm:tmp sun',
                                     tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' turned the Enchanted Sundial. Good morning!', '#ffd23f')]),
                                     'playsound minecraft:block.bell.use master @a ~ ~ ~ 1 1.2'])
    fn('p39/enchanted_sundial/skip', ['$time add $(t)'])

    # ------------------------------------------------------------------ Band of Regeneration
    for slot in inv('band_of_regeneration'):
        second.append(f'execute as @a[gamemode=!spectator] if items entity @s {slot} run function bm:p39/band')
    fn('p39/band', ['execute if score @s bm.dmgt matches 1.. run scoreboard players set @s bm.bandt 5', 'scoreboard players set @s bm.dmgt 0',
                    'execute if score @s bm.bandt matches 1.. run return run scoreboard players remove @s bm.bandt 1',
                    'scoreboard players add @s bm.bandc 1',
                    'execute if score @s bm.bandc matches 5.. run effect give @s minecraft:regeneration 6 0 true',
                    'execute if score @s bm.bandc matches 5.. run scoreboard players set @s bm.bandc 0'])
    second.append('scoreboard players set @a[scores={bm.dmgt=1000..}] bm.dmgt 0')

    # ------------------------------------------------------------------ Mimics
    wjson('bm/tags/block/p39_chests.json', {'values': ['minecraft:chest', 'minecraft:trapped_chest', 'minecraft:barrel']})
    tables = sorted({k[5:] for k in G.FUNCS if k.startswith('loot/') and k[5:] not in ('tokens_1', 'tokens_2', 'tokens_3', 'medallion', 'lucky')
                     and f'bm/advancement/loot/{k[5:]}.json'})
    for t in tables:
        hook(t).extend(['execute store result score @s bm.rng run random value 1..100', 'execute if score @s bm.rng matches 1 run function bm:p39/mimic/try'])
    # the chest is filled right AFTER this trigger fires: mark it now, wake the mimic next tick
    fn('p39/mimic/try', ['execute unless function bm:p37/allowed run return 0', 'scoreboard players set #ray bm.rng 28',
                         'execute anchored eyes positioned ^ ^ ^ run function bm:p39/mimic/ray'])
    fn('p39/mimic/ray', ['execute if block ~ ~ ~ #bm:p39_chests align xyz positioned ~0.5 ~ ~0.5 run return run function bm:p39/mimic/mark',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.25 run function bm:p39/mimic/ray'])
    fn('p39/mimic/mark', ['execute if entity @e[type=minecraft:marker,tag=bm.mimq,distance=..0.5] run return 0',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.mimq"]}', 'schedule function bm:p39/mimic/wake_all 1t append'])
    fn('p39/mimic/wake_all', ['execute as @e[type=minecraft:marker,tag=bm.mimq] at @s run function bm:p39/mimic/wake'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.mimq] at @s run function bm:p39/mimic/wake')     # a reload ate the schedule
    disp = {'id': 'minecraft:item_display', 'Tags': ['bm.mimd'], 'item_display': 'fixed', 'teleport_duration': Int(2),
            'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                               'translation': [F(0), F(-0.55), F(0)], 'scale': [F(1.0)] * 3}}
    mimic = {'Tags': ['bm.mimic', 'bm.seen', 'bm.mnew'], 'RabbitType': Int(99), 'PersistenceRequired': B(1), 'Health': F(60),
             'CustomName': T('Mimic', '#c8864a', bold=True), 'DeathLootTable': 'bm:p39/mimic',
             'attributes': [{'id': 'minecraft:max_health', 'base': 60.0}, {'id': 'minecraft:scale', 'base': 2.0},
                            {'id': 'minecraft:attack_damage', 'base': 7.0}, {'id': 'minecraft:movement_speed', 'base': 0.38},
                            {'id': 'minecraft:follow_range', 'base': 24.0}],
             'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    for kind, block in (('chest', 'minecraft:chest'), ('barrel', 'minecraft:barrel')):
        m = dict(mimic, Passengers=[dict(disp, item={'id': block, 'count': Int(1)})])
        fn(f'p39/mimic/spawn_{kind}', [f'summon minecraft:rabbit ~ ~ ~ {snbt(m)}'])
    fn('p39/mimic/wake', ['kill @s', 'execute unless block ~ ~ ~ #bm:p39_chests run return 0',
                          'scoreboard players add #mim bm.mimid 1',
                          'execute store result storage bm:tmp mim.n int 1 run scoreboard players get #mim bm.mimid',
                          'data modify storage bm:tmp mim.items set value []', 'data modify storage bm:tmp mim.items set from block ~ ~ ~ Items',
                          'scoreboard players set #mb bm.rng 0', 'execute if block ~ ~ ~ minecraft:barrel run scoreboard players set #mb bm.rng 1',
                          'execute if block ~ ~ ~ minecraft:trapped_chest run scoreboard players set #mb bm.rng 2',
                          'execute store result storage bm:tmp mim.code int 1 run scoreboard players get #mb bm.rng',
                          'function bm:p39/mimic/store with storage bm:tmp mim',
                          # empty it first: a container broken by a command spills its contents
                          'data remove block ~ ~ ~ Items', 'setblock ~ ~ ~ minecraft:air',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.mimm","bm.mmnew"]}',
                          'scoreboard players operation @e[type=minecraft:marker,tag=bm.mmnew] bm.mimid = #mim bm.mimid',
                          'tag @e[type=minecraft:marker,tag=bm.mmnew] remove bm.mmnew',
                          'execute if score #mb bm.rng matches 1 run function bm:p39/mimic/spawn_barrel',
                          'execute unless score #mb bm.rng matches 1 run function bm:p39/mimic/spawn_chest',
                          'scoreboard players operation @e[type=minecraft:rabbit,tag=bm.mnew] bm.mimid = #mim bm.mimid',
                          'tag @e[type=minecraft:rabbit,tag=bm.mnew] remove bm.mnew',
                          'particle minecraft:poof ~ ~0.5 ~ 0.4 0.4 0.4 0.05 20', 'playsound minecraft:block.chest.close hostile @a[distance=..16] ~ ~ ~ 1 0.5',
                          'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..16] ~ ~ ~ 1 0.7',
                          tellraw('@a[distance=..12]', PREFIX + [T('It was a ', 'gray'), T('MIMIC', '#c8864a', bold=True), T('!', 'gray')])])
    fn('p39/mimic/store', ['$data modify storage bm:mim m$(n) set value {code:$(code)}', '$data modify storage bm:mim m$(n).items set from storage bm:tmp mim.items'])
    # the chest comes back once its mimic is gone
    second.append('execute as @e[type=minecraft:marker,tag=bm.mimm] at @s run function bm:p39/mimic/check')
    fn('p39/mimic/check', ['scoreboard players operation #k bm.mimid = @s bm.mimid',
                           'execute as @e[type=minecraft:rabbit,tag=bm.mimic] if score @s bm.mimid = #k bm.mimid run return run scoreboard players set #alive bm.rng 1',
                           'scoreboard players set #alive bm.rng 0',
                           'execute as @e[type=minecraft:rabbit,tag=bm.mimic] if score @s bm.mimid = #k bm.mimid run scoreboard players set #alive bm.rng 1',
                           'execute if score #alive bm.rng matches 1 run return 0',
                           'execute store result storage bm:tmp mim.n int 1 run scoreboard players get @s bm.mimid',
                           'function bm:p39/mimic/restore with storage bm:tmp mim', 'kill @s'])
    fn('p39/mimic/restore', ['$execute unless data storage bm:mim m$(n) run return 0',
                             '$execute store result score #mb bm.rng run data get storage bm:mim m$(n).code',
                             'execute if score #mb bm.rng matches 1 run setblock ~ ~ ~ minecraft:barrel',
                             'execute if score #mb bm.rng matches 2 run setblock ~ ~ ~ minecraft:trapped_chest',
                             'execute if score #mb bm.rng matches 0 run setblock ~ ~ ~ minecraft:chest',
                             '$data modify block ~ ~ ~ Items set from storage bm:mim m$(n).items', '$data remove storage bm:mim m$(n)',
                             'particle minecraft:poof ~ ~0.5 ~ 0.4 0.4 0.4 0.05 15'])
    fast.append('execute as @e[type=minecraft:rabbit,tag=bm.mimic] at @s run function bm:p39/mimic/fx')
    second.append('execute as @e[type=minecraft:item_display,tag=bm.mimd] unless function bm:p20/frog/has_vehicle run kill @s')
    fn('p39/mimic/fx', ['execute store result score #r bm.rng run random value 1..12',
                        'execute if score #r bm.rng matches 1 run playsound minecraft:block.chest.open hostile @a[distance=..16] ~ ~ ~ 0.6 0.6',
                        'execute if score #r bm.rng matches 2 run playsound minecraft:block.chest.close hostile @a[distance=..16] ~ ~ ~ 0.6 0.6'])
    wjson('bm/loot_table/p39/mimic.json', {'type': 'minecraft:entity', 'pools': [
        {'rolls': 1, 'entries': acc_entry}, {'rolls': 1, 'entries': [G.loot_entry('token', G.uni(3, 6))]},
        {'rolls': 1, 'entries': [G.loot_entry('medallion')], 'conditions': [G.chance(0.3)]}]})

    # ------------------------------------------------------------------ Fallen Stars and the Star Cloak
    wjson('bm/predicate/p39/clear.json', {'condition': 'minecraft:weather_check', 'raining': False})
    second.append('execute if score #tod bm.bm matches 13000..22800 as @a[gamemode=!spectator] at @s if dimension minecraft:overworld '
                  'if predicate bm:p39/clear run function bm:p39/star/roll')
    second.append('execute unless score #tod bm.bm matches 13000..23400 run kill @e[type=minecraft:item,tag=bm.star]')
    fn('p39/star/roll', ['execute store result score #r bm.rng run random value 1..45', 'execute unless score #r bm.rng matches 1 run return 0',
                         'execute if entity @e[type=minecraft:item,tag=bm.star,distance=..48] run return 0',
                         'summon minecraft:marker ~ ~ ~ {Tags:["bm.starm"]}',
                         'spreadplayers ~ ~ 4 36 false @e[type=minecraft:marker,tag=bm.starm]',
                         'execute as @e[type=minecraft:marker,tag=bm.starm] at @s run function bm:p39/star/fall'])
    streak = [f'particle minecraft:end_rod ~{12 - i} ~{24 - 2 * i} ~ 0 0 0 0 1 force' for i in range(12)]
    fn('p39/star/fall', ['kill @s', 'execute unless function bm:p37/allowed run return 0'] + streak +
       ['particle minecraft:firework ~ ~0.5 ~ 0.3 0.2 0.3 0.1 15 force', 'playsound minecraft:entity.firework_rocket.twinkle_far ambient @a[distance=..64] ~ ~ ~ 1 1.4',
        'loot spawn ~ ~0.5 ~ loot bm:items/fallen_star',
        'execute as @e[type=minecraft:item,distance=..2,tag=!bm.star] if items entity @s contents %s run data merge entity @s {Glowing:1b,Tags:["bm.star"]}'
        % (holds % 'fallen_star')])
    fast.append('execute as @e[type=minecraft:item,tag=bm.star] at @s run particle minecraft:end_rod ~ ~0.4 ~ 0.1 0.2 0.1 0.01 1')
    fn('p39/star/use', [f'execute store result score #n bm.rng run clear @s {holds % "fallen_star"} 0',
                        'execute if score #n bm.rng matches ..8 run return run ' + title('@s', 'actionbar', [T('A Star Cloak takes 9 Fallen Stars. You have ', 'gray'),
                                                                                                        {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': '#ffe85a'}, T('.', 'gray')]),
                        f'clear @s {holds % "fallen_star"} 9', give('star_cloak'),
                        'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.4', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.05 30',
                        say('Nine stars knot into a Star Cloak.', '#ffe85a')])
    wjson('bm/advancement/p39/hurt.json', {'criteria': {'hurt': {'trigger': 'minecraft:entity_hurt_player'}}, 'rewards': {'function': 'bm:p39/star/hurt'}})
    fn('p39/star/hurt', ['advancement revoke @s only bm:p39/hurt',
                         'execute unless items entity @s container.* %s unless items entity @s weapon.offhand %s run return 0' % (holds % 'star_cloak', holds % 'star_cloak'),
                         'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g2 bm.rng = #g bm.rng',
                         'scoreboard players operation #g2 bm.rng -= @s bm.scd', 'execute if score @s bm.scd matches 1.. if score #g2 bm.rng matches ..59 run return 0',
                         'scoreboard players operation @s bm.scd = #g bm.rng', 'tag @s add bm.starc',
                         'execute at @s as @e[type=#bm:hostile,distance=..12,sort=nearest,limit=3] at @s run function bm:p39/star/strike',
                         'tag @s remove bm.starc'])
    fn('p39/star/strike', [f'particle minecraft:end_rod ~{6 - i * 0.5} ~{12 - i} ~ 0 0 0 0 1 force' for i in range(12)] +
       ['particle minecraft:firework ~ ~1 ~ 0.3 0.4 0.3 0.1 10', 'playsound minecraft:entity.firework_rocket.blast player @a[distance=..16] ~ ~ ~ 0.8 1.6',
        'damage @s 6 minecraft:player_attack by @p[tag=bm.starc]'])

    # ------------------------------------------------------------------ Fishing crates
    wjson('bm/advancement/p39/fished.json', {'criteria': {'fish': {'trigger': 'minecraft:fishing_rod_hooked'}}, 'rewards': {'function': 'bm:p39/fish'}})
    fn('p39/fish', ['advancement revoke @s only bm:p39/fished', 'execute store result score #r bm.rng run random value 1..1000',
                    'execute if score #r bm.rng matches 1..4 run return run function bm:p39/fish_golden',
                    'execute if score #r bm.rng matches 5..19 run return run function bm:p39/fish_iron',
                    'execute if score #r bm.rng matches 20..69 run return run function bm:p39/fish_wooden'])
    for c, art in (('golden', 'a Golden Crate'), ('iron', 'an Iron Crate'), ('wooden', 'a Wooden Crate')):
        fn(f'p39/fish_{c}', [give(f'crate_{c}'), say(f'You also reeled in {art}!', CRATES[c][1]),
                             'playsound minecraft:entity.fishing_bobber.splash player @s ~ ~ ~ 1 0.6'])
    crate_pools = {
        'wooden': [({'rolls': 1, 'entries': [G.loot_entry('token', G.uni(1, 2))]}),
                   {'rolls': G.uni(2, 4), 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:iron_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:copper_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(3, 8)}]},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:gold_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:experience_bottle', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 3)}]}]},
                   {'rolls': 1, 'entries': acc_entry, 'conditions': [G.chance(0.04)]}],
        'iron': [{'rolls': 1, 'entries': [G.loot_entry('token', G.uni(2, 4))]},
                 {'rolls': G.uni(2, 4), 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]},
                                                    {'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 2)}]},
                                                    {'type': 'minecraft:item', 'name': 'minecraft:emerald', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]},
                                                    {'type': 'minecraft:item', 'name': 'minecraft:experience_bottle', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]}]},
                 {'rolls': 1, 'entries': acc_entry, 'conditions': [G.chance(0.1)]}],
        'golden': [{'rolls': 1, 'entries': [G.loot_entry('token', G.uni(4, 8))]}, {'rolls': 1, 'entries': [G.loot_entry('medallion')], 'conditions': [G.chance(0.35)]},
                   {'rolls': 1, 'entries': [G.loot_entry('lucky_token')], 'conditions': [G.chance(0.5)]},
                   {'rolls': G.uni(2, 3), 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 4)}]},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:netherite_scrap'},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:enchanted_golden_apple', 'weight': 1},
                                                      {'type': 'minecraft:item', 'name': 'minecraft:emerald_block'}]},
                   {'rolls': 1, 'entries': acc_entry, 'conditions': [G.chance(0.3)]}]}
    for c, pools in crate_pools.items():
        wjson(f'bm/loot_table/p39/crate_{c}.json', {'type': 'minecraft:chest', 'pools': pools})
        fn(f'p39/crate/{c}', [f'clear @s {holds % ("crate_" + c)} 1', f'loot give @s loot bm:p39/crate_{c}',
                              'playsound minecraft:block.barrel.open player @s ~ ~ ~ 1 1.2', 'particle minecraft:poof ~ ~1 ~ 0.3 0.3 0.3 0.02 8'])

    # ------------------------------------------------------------------ Sword shrines and the Enchanted Sword
    wjson('bm/tags/worldgen/biome/has_structure/sword_shrine.json', {'values': [f'minecraft:{b}' for b in SHRINE_BIOMES]})
    wjson('bm/tags/worldgen/structure/sword_shrine.json', {'values': ['bm:sword_shrine']})
    wjson('bm/worldgen/structure/sword_shrine.json', {'type': 'minecraft:jigsaw', 'biomes': '#bm:has_structure/sword_shrine', 'step': 'surface_structures',
                                                       'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': 'bm:sword_shrine/start', 'size': 1,
                                                       'start_height': {'absolute': 0}, 'project_start_to_heightmap': 'WORLD_SURFACE_WG',
                                                       'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
    wjson('bm/worldgen/template_pool/sword_shrine/start.json', {'fallback': 'minecraft:empty', 'elements': [
        {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'bm:sword_shrine', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
    wjson('bm/worldgen/structure_set/sword_shrine.json', {'structures': [{'structure': 'bm:sword_shrine', 'weight': 1}],
                                                           'placement': {'type': 'minecraft:random_spread', 'spacing': 48, 'separation': 20, 'salt': 77441902}})
    from structures import Build
    Bd = Build(1, 1, 1)
    Bd.marker(0.5, 0.0, 0.5, ['bm.shrine_seed'], 0)
    Bd.export(G.path('data', 'bm', 'structure', 'sword_shrine.nbt'))
    second.append('execute as @e[type=minecraft:marker,tag=bm.shrine_seed] at @s if entity @a[distance=..96] if loaded ~-3 ~ ~-3 if loaded ~3 ~ ~3 '
                  'run function bm:p39/shrine/build')
    q = math.sin(math.radians(-67.5)), math.cos(math.radians(-67.5))
    sword_disp = {'Tags': ['bm.shrine_d'], 'item': {'id': 'minecraft:diamond_sword', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:enchanted_sword'}},
                  'item_display': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(15)}, 'Glowing': B(1),
                  'transformation': {'left_rotation': [F(0), F(0), F(round(q[0], 4)), F(round(q[1], 4))], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                     'translation': [F(0), F(0.75), F(0)], 'scale': [F(1.3)] * 3}}
    fn('p39/shrine/build', ['kill @s',
                            'execute if block ~ ~-1 ~ #minecraft:replaceable run return 0',        # water, or floating: no shrine here
                            'fill ~-3 ~ ~-3 ~3 ~4 ~3 minecraft:air replace #minecraft:replaceable',
                            'fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 minecraft:mossy_stone_bricks', 'fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:stone_bricks',
                            'fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 minecraft:moss_block replace #minecraft:dirt',
                            'setblock ~ ~ ~ minecraft:chiseled_stone_bricks',
                            'setblock ~-2 ~ ~-2 minecraft:mossy_cobblestone_wall', 'setblock ~-2 ~1 ~-2 minecraft:lantern',
                            'setblock ~2 ~ ~2 minecraft:mossy_cobblestone_wall', 'setblock ~2 ~1 ~2 minecraft:lantern',
                            'setblock ~2 ~ ~-2 minecraft:mossy_cobblestone_wall', 'setblock ~-2 ~ ~2 minecraft:mossy_cobblestone_wall',
                            f'summon minecraft:item_display ~ ~1 ~ {snbt(sword_disp)}',
                            'summon minecraft:interaction ~ ~1 ~ {Tags:["bm.shrine_i"],width:0.7f,height:1.4f,response:1b}'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.shrine_i] if data entity @s interaction at @s run function bm:p39/shrine/pull')
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.shrine_d] at @s if entity @a[distance=..24] run particle minecraft:enchant ~ ~1.2 ~ 0.3 0.6 0.3 0.5 3')
    fn('p39/shrine/pull', ['execute on target run function bm:p39/shrine/give', 'kill @e[type=minecraft:item_display,tag=bm.shrine_d,distance=..1.5]',
                           'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.6 0.3 0.1 30', 'playsound minecraft:block.anvil.use player @a[distance=..16] ~ ~ ~ 0.7 1.6', 'kill @s'])
    fn('p39/shrine/give', [give('enchanted_sword'), tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' pulled the ', 'gray'),
                                                                            T('Enchanted Sword', '#7ab8ff', bold=True), T(' from the stone!', 'gray')])])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/shrine', 'yellow'), T('  builds a sword shrine here', 'gray')])]
    fn('admin/shrine', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.shrine_seed"]}'])
    # the beam: full health only, 1 s apart; hits the first monster in 20 blocks
    fn('p39/sword/use', ['execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g2 bm.rng = #g bm.rng',
                         'scoreboard players operation #g2 bm.rng -= @s bm.swcd', 'execute if score @s bm.swcd matches 1.. if score #g2 bm.rng matches ..19 run return 0',
                         'execute store result score #hp bm.rng run data get entity @s Health 10',
                         'execute store result score #mx bm.rng run attribute @s minecraft:max_health get 10',
                         'execute if score #hp bm.rng < #mx bm.rng run return run ' + say('The sword only sings at full health.'),
                         'scoreboard players operation @s bm.swcd = #g bm.rng', 'tag @s add bm.beamer', 'scoreboard players set #ray bm.rng 40',
                         'playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 1.6',
                         'execute anchored eyes positioned ^ ^ ^0.6 run function bm:p39/sword/ray', 'tag @s remove bm.beamer'])
    fn('p39/sword/ray', ['particle minecraft:dust{color:[0.48,0.72,1.0],scale:1.2} ~ ~ ~ 0 0 0 0 1 force',
                         'execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[type=#bm:hostile,dx=0,dy=0,dz=0,limit=1] at @s run return run function bm:p39/sword/hit',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p39/sword/ray'])
    fn('p39/sword/hit', ['damage @s 7 minecraft:player_attack by @p[tag=bm.beamer]', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 12'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    I = {}
    I['climbing_claws'] = grid(['................', '................', '...K..K..K......', '...KK.KK.KK.....', '....K..K..K.....', '....SSSSSSS.....', '...SLLLLLLLS....',
                                '...SLLLLLLLS....', '...SLLLLLLLS....', '....SSSSSSS.....', '................', '................', '................', '................',
                                '................', '................'], dict(K='#e8e8f0', S='#5a3a1a', L='#c8a070'))
    I['umbrella'] = grid(['................', '.......RR.......', '.....RRWWRR.....', '...RRWWRRWWRR...', '..RRRRRRRRRRRR..', '.R.R..R..R..R.R.', '.......K........',
                          '.......K........', '.......K........', '.......K........', '.......K........', '.......K........', '....K..K........', '.....KK.........',
                          '................', '................'], dict(R='#e84a6a', W='#ffffff', K='#3a2a1a'))
    I['rod_of_discord'] = grid(['................', '..........PPP...', '.........PWPPP..', '.........PPPPP..', '..........PPP...', '.........G......', '........G.......',
                                '.......G........', '......G.........', '.....G..........', '....G...........', '...G............', '..G.............', '................',
                                '................', '................'], dict(P='#d86aff', W='#ffffff', G='#c8a050'))
    for fl, col in (('water', '#3a8aff'), ('lava', '#ff7a1a')):
        I[f'bottomless_{fl}'] = grid(['................', '................', '....KKKKKKKK....', '...K........K...', '...KKKKKKKKKK...', '...KCCCCCCCCK...', '...KCCWCCCCCK...',
                                      '....KCCCCCCK....', '....KCCCCCCK....', '....KCCCCCCK....', '.....KKKKKK.....', '................', '.......YY.......', '......Y..Y......',
                                      '.......YY.......', '................'], dict(K='#8a8a9a', C=col, W='#ffffff', Y='#ffd23f'))
    I['extendo_grip'] = grid(['................', '.YY.............', 'Y..Y............', '.YYK............', '...KK...........', '....KK..........', '.....KK.........',
                              '......KK........', '.......KK.......', '........KK......', '.........KRR....', '..........RRR...', '..........RRR...', '................',
                              '................', '................'], dict(Y='#ffd23f', K='#8a8a9a', R='#c83a3a'))
    I['lifeform_analyzer'] = grid(['................', '....KKKKKKKK....', '....KGGGGGGK....', '....KGgGGGGK....', '....KGGGgGGK....', '....KGGGGGGK....', '....KKKKKKKK....',
                                   '....KRK..KBK....', '....KKKKKKKK....', '....KKKKKKKK....', '................', '................', '................', '................',
                                   '................', '................'], dict(K='#3a3a48', G='#1a5a3a', g='#5aff9a', R='#ff4a4a', B='#4a8aff'))
    I['metal_detector'] = grid(['................', '..K.............', '...K............', '....K...........', '.....K..........', '......K.........', '.......K........',
                                '........K.......', '.........K......', '.......SSSSS....', '......S.....S...', '......S..R..S...', '......S.....S...', '.......SSSSS....',
                                '................', '................'], dict(K='#3a3a48', S='#c8c8d8', R='#ff4a4a'))
    I['enchanted_sundial'] = grid(['................', '................', '.......Y........', '......YYK.......', '.....Y..K.......', '....GGGGGGGG....', '...GWWWWWWWWG...',
                                   '...GWWWWWWWWG...', '....GGGGGGGG....', '......SSSS......', '......SSSS......', '.....SSSSSS.....', '................', '................',
                                   '................', '................'], dict(Y='#ffd23f', K='#8a6a3a', G='#c8a050', W='#fff4c8', S='#9a9aa8'))
    I['band_of_regeneration'] = grid(['................', '................', '................', '......RRRR......', '.....R....R.....', '....R......R....', '....R..HH..R....',
                                      '....R.HHHH.R....', '....R..HH..R....', '.....R....R.....', '......RRRR......', '................', '................', '................',
                                      '................', '................'], dict(R='#ff5a7a', H='#ff2a4a'))
    I['obsidian_skull'] = grid(['................', '................', '.....KKKKKK.....', '....KPPPPPPK....', '...KPPPPPPPPK...', '...KPRRPPRRPK...', '...KPRRPPRRPK...',
                                '...KPPPPPPPPK...', '....KPPKKPPK....', '.....KPPPPK.....', '.....KPKPKP.....', '......KKKK......', '................', '................',
                                '................', '................'], dict(K='#140a20', P='#4a2a6a', R='#ff7a1a'))
    for b, col in (('ice_skates', '#bfefff'), ('water_walking_boots', '#3a8aff')):
        I[b] = grid(['................', '................', '....KKKK........', '....KCCK........', '....KCCK........', '....KCCK........', '....KCCKKKKK....',
                     '....KCCCCCCCK...', '....KKKKKKKKK...', '....S......S....' if b == 'ice_skates' else '...WW.....WW....', '....SSSSSSSS....' if b == 'ice_skates' else '..W..W...W..W...',
                     '................', '................', '................', '................', '................'],
                    dict(K='#3a3a48', C=col, S='#e8e8f0', W='#8ad8ff'))
    I['fallen_star'] = grid(['................', '.......Y........', '.......Y........', '......YYY.......', 'YYYYYYYWYYYYYY..', '..YYYYWWYYYY....', '....YYYYYYY.....',
                             '....YYY.YYY.....', '...YYY...YYY....', '...YY.....YY....', '..Y.........Y...', '................', '................', '................',
                             '................', '................'], dict(Y='#ffe85a', W='#ffffff'))
    I['star_cloak'] = grid(['................', '.....KKKKKK.....', '....KBBBBBBK....', '...KBBYBBBBBK...', '...KBBBBBYBBK...', '...KBYBBBBBBK...', '..KBBBBBBYBBBK..',
                            '..KBBBYBBBBBBK..', '..KBBBBBBBBYBK..', '.KBBYBBBBBBBBBK.', '.KBBBBBBYBBBBBK.', '.KKKKKKKKKKKKKK.', '................', '................',
                            '................', '................'], dict(K='#1a1a3a', B='#2a2a6a', Y='#ffe85a'))
    for c, col in (('wooden', '#b8864a'), ('iron', '#d8d8e0'), ('golden', '#ffd23f')):
        I[f'crate_{c}'] = grid(['................', '................', '..KKKKKKKKKKKK..', '..KCCCCCCCCCCK..', '..KCKCCCCCCKCK..', '..KCCKCCCCKCCK..', '..KCCCKCCKCCCK..',
                                '..KCCCCKKCCCCK..', '..KCCCKCCKCCCK..', '..KCCKCCCCKCCK..', '..KCKCCCCCCKCK..', '..KCCCCCCCCCCK..', '..KKKKKKKKKKKK..', '................',
                                '................', '................'], dict(K='#3a2a1a' if c == 'wooden' else '#5a5a68', C=col))
    I['enchanted_sword'] = grid(['................', '.............WW.', '............WBW.', '...........WBW..', '..........WBW...', '.........WBW....', '........WBW.....',
                                 '...K...WBW......', '....K.WBW.......', '.....KBW........', '.....GK.........', '....G..K........', '...G............', '..G.............',
                                 '.GG.............', '................'], dict(W='#c8e8ff', B='#7ab8ff', K='#3a5aaa', G='#ffd23f'))
    for k, v in I.items(): R.ICONS[k] = v
    R.HANDHELD_EXTRA |= {'enchanted_sword', 'umbrella', 'rod_of_discord', 'metal_detector'}
