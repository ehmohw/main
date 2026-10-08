"""Phase 2 data: loot tables, trial spawner configs, worldgen, the Hollow Throne dimension, item behaviours,
Conqueror's set effects, lucky map fragments, trader refresh and admin tools."""
from items import T, ITEMS
from nbt import snbt, B, F, Int
from p2.config import D, ORDER

HOLLOW_ORIGIN = (1000, 40, 1000)   # 2.2: the rebuilt citadel (152 x 128 x 152); 2.1 and earlier used (-48, 32, -48)
HOLLOW_VER = 23                  # 2.13: lava rim, nastier waves - rebuilt in place (old entities cleared first)
GRAVE_OFFSET = (-48, 14, 60)       # Wilfrey's Rest, relative to HOLLOW_ORIGIN (2.4)



def _eq(main=None, head=None, chest=None, extra=None):
    """Mob NBT with equipment that never drops (wave mobs, 2.2)."""
    e, dc = {}, {}
    for slot, it in (('mainhand', main), ('head', head), ('chest', chest)):
        if it: e[slot] = {'id': f'minecraft:{it}', 'count': Int(1)}; dc[slot] = F(0)
    n = {'equipment': e, 'drop_chances': dc} if e else {}
    if extra: n.update(extra)
    return n


_IMMUNE = {'IsImmuneToZombification': B(1)}
_KNIGHT = ('wither_skeleton', _eq('iron_sword', 'chainmail_helmet', extra={'CustomName': T('Hollow Knight', '#8a96a8')}))
_ARCHER = ('stray', _eq('bow', extra={'CustomName': T('Hollow Archer', '#8a96a8')}))
_CAPTAIN = ('wither_skeleton', _eq('netherite_sword', 'netherite_helmet', 'netherite_chestplate',
                                   extra={'CustomName': T('Hollow Captain', '#e5e4e2', bold=True), 'Glowing': B(1)}))
# 2.13: the Hollow's waves are nastier - phantoms are gone (they flew off and never fought); brutes, hoglins and a ravager instead
_BUFF = lambda *e: [{'id': f'minecraft:{x}', 'amplifier': B(a), 'duration': Int(-1), 'show_particles': B(0)} for x, a in e]
_BRUTE = ('piglin_brute', _eq('netherite_axe', 'netherite_helmet', extra=dict(_IMMUNE, CustomName=T('Hollow Brute', '#8a96a8'),
                                                                          active_effects=_BUFF(('resistance', 0)))))
_HOG = ('hoglin', dict(_IMMUNE, CustomName=T('Hollow Tusker', '#8a96a8'), active_effects=_BUFF(('strength', 0), ('speed', 0))))
_RAVAGER = ('ravager', {'CustomName': T('Hollow Ravager', '#e5e4e2', bold=True), 'active_effects': _BUFF(('resistance', 0))})
_KNIGHT2 = ('wither_skeleton', _eq('netherite_sword', 'netherite_helmet', extra={'CustomName': T('Hollow Knight', '#8a96a8'),
                                                                                 'active_effects': _BUFF(('speed', 0), ('strength', 0))}))
WAVE_PER = {'hex': (1, 3), 'keep': (2, 3), 'hollow': (2, 3)}        # mobs per spawn point on ordinary waves / on the last wave (everyone else: 1 / 2)
# combat trials: WAVES[d][n] = (title, [wave1 roster, wave2 roster, ...]); each spawn point picks one mob per wave
# from the roster (two on the last wave)
WAVES = {
    'tide': {1: ("The Tyrant's Tide", [
        [('drowned', _eq('trident')), ('drowned', _eq('iron_sword'))],
        [('drowned', _eq('trident')), ('drowned', _eq('iron_sword', 'turtle_helmet')), ('drowned', {})],
        [('drowned', _eq('trident', 'turtle_helmet')), ('drowned', _eq('iron_sword', 'turtle_helmet'))]])},
    'hex': {2: ('The Choir Militant', [
        [('vindicator', _eq('iron_axe')), ('pillager', _eq('crossbow'))],
        [('vindicator', _eq('iron_axe')), ('witch', {}), ('pillager', _eq('crossbow'))],
        [('evoker', {}), ('vindicator', _eq('diamond_axe')), ('pillager', _eq('crossbow'))]])},
    'keep': {2: ("Bobbery's Bonecrew", [
        [('wither_skeleton', _eq('stone_sword')), ('skeleton', _eq('bow'))],
        [('wither_skeleton', _eq('stone_sword')), ('blaze', {}), ('skeleton', _eq('bow'))],
        [('wither_skeleton', _eq('iron_sword', 'iron_helmet')), ('blaze', {}), ('wither_skeleton', _eq('stone_axe'))]])},
    'lucky': {3: ('The Gilded Guard', [
        [('husk', _eq('golden_sword', 'golden_helmet')), ('zombie', _eq('golden_axe', 'golden_helmet'))],
        [('husk', _eq('golden_sword', 'golden_helmet', 'golden_chestplate')), ('piglin', _eq('golden_sword', extra=_IMMUNE))],
        [('piglin_brute', _eq('golden_axe', extra=_IMMUNE)), ('husk', _eq('golden_sword', 'golden_helmet')), ('piglin', _eq('crossbow', extra=_IMMUNE))]])},
    'hollow': {1: ('The Siege of the Gate', [[_KNIGHT, _ARCHER, _BRUTE], [_KNIGHT, _BRUTE, _ARCHER, _HOG], [_CAPTAIN, _BRUTE, _HOG, _ARCHER],
                                             [_CAPTAIN, _RAVAGER, _BRUTE, _KNIGHT2]]),
               5: ("The Knights' Vigil", [[_KNIGHT2, _BRUTE, _HOG], [_BRUTE, _HOG, _ARCHER, _KNIGHT2], [_CAPTAIN, _BRUTE, _HOG, _KNIGHT2],
                                          [_CAPTAIN, _RAVAGER, _BRUTE, _HOG]])},
}

# vanilla tables to mix into each dungeon's loot, and the themed hidden gear found in its secret rooms
VANILLA = {'brood': ['chests/simple_dungeon'], 'frost': ['chests/igloo_chest', 'chests/ancient_city_ice_box'],
           'tide': ['chests/underwater_ruin_big', 'chests/buried_treasure'], 'hex': ['chests/woodland_mansion', 'chests/stronghold_library'],
           'keep': ['chests/bastion_treasure', 'chests/bastion_other'], 'hollow': ['chests/end_city_treasure', 'chests/ancient_city'],
           'lucky': ['chests/buried_treasure']}
HIDDEN = {'brood': ['silkstrider_boots'], 'frost': ['frostwarden_hood'], 'tide': ['abyssal_helm'], 'hex': ['hexwoven_robe', 'blink_tome'],
          'keep': ['oathblade', 'wilfrey_aegis'], 'hollow': ['hollow_crown', 'charm_wings_angel', 'charm_wings_evil'], 'lucky': ['horseshoe_charm', 'pocket_slots']}
BOSS_DROP = {'brood': ('broodfang', 0.25, 'spider'), 'frost': ('frost_longbow', 0.25, 'stray'), 'tide': ('tyrant_trident', 0.25, 'drowned'),
             'hex': ('archmage_staff', 0.25, 'evoker'), 'keep': ('bobbery_axe', 0.15, 'wither_skeleton'), 'hollow': (None, 0, 'wither'),
             'lucky': (None, 0, 'chicken')}
# trial spawner rosters: name -> list of (entity id, equipment items or None, weight)
SPAWNERS = {
    'brood': {'spiders': [('spider', None, 3), ('cave_spider', None, 1)], 'cave_spiders': [('cave_spider', None, 1)]},
    'frost': {'strays': [('stray', ['bow', 'leather_helmet'], 1)], 'frozen': [('zombie', ['iron_sword', 'leather_chestplate', 'leather_helmet'], 2), ('stray', ['bow'], 1)]},
    'tide': {'drowned': [('drowned', ['trident'], 1), ('drowned', None, 2)], 'drowned_melee': [('drowned', ['iron_sword'], 1)]},
    'hex': {'vindicators': [('vindicator', ['iron_axe'], 2), ('pillager', ['crossbow'], 1)], 'witches': [('witch', None, 1)]},
    'keep': {'wither_knights': [('wither_skeleton', ['stone_sword'], 3), ('skeleton', ['bow'], 1)], 'blazes': [('blaze', None, 1)]},
    # 'knights' are melee only: they guard the rooms with targets and keypads (stray arrows would hit puzzle inputs)
    'hollow': {'knights': [('wither_skeleton', ['iron_sword', 'chainmail_helmet'], 2), ('wither_skeleton', ['stone_axe'], 1)], 'archers': [('stray', ['bow'], 1), ('skeleton', ['bow'], 1)]},
    'lucky': {'gold_zombies': [('zombie', ['golden_sword', 'golden_helmet', 'golden_chestplate'], 2), ('husk', ['golden_axe'], 1)], 'gold_husks': [('husk', ['golden_sword'], 1)]},
}
WORLDGEN = {  # d: (biomes, step, start_height, heightmap, adaptation, spacing, separation, salt, decoration)
    'brood': (['#minecraft:is_forest', '#minecraft:is_taiga', '#minecraft:is_jungle', 'minecraft:dark_forest', 'minecraft:pale_garden',
               'minecraft:dripstone_caves', 'minecraft:lush_caves'], 'underground_structures',
              {'type': 'minecraft:uniform', 'min_inclusive': {'absolute': -12}, 'max_inclusive': {'absolute': 4}}, None, 'none', 32, 12, 61803391, 'minecraft:red_x'),
    'frost': (['minecraft:snowy_plains', 'minecraft:ice_spikes', 'minecraft:snowy_taiga', 'minecraft:grove', 'minecraft:snowy_slopes',
               'minecraft:frozen_peaks', 'minecraft:jagged_peaks'], 'surface_structures', {'absolute': -6}, 'WORLD_SURFACE_WG', 'beard_thin', 40, 14, 27182818, 'minecraft:target_x'),
    'tide': (['minecraft:deep_ocean', 'minecraft:deep_cold_ocean', 'minecraft:deep_lukewarm_ocean', 'minecraft:deep_frozen_ocean'],
             'surface_structures', {'absolute': -3}, 'OCEAN_FLOOR_WG', 'none', 36, 12, 14142135, 'minecraft:monument'),
    'hex': (['minecraft:swamp', 'minecraft:mangrove_swamp'], 'surface_structures', {'absolute': -5}, 'WORLD_SURFACE_WG', 'beard_thin', 40, 14, 17320508, 'minecraft:swamp_hut'),
    'keep': (['minecraft:pale_garden', 'minecraft:dark_forest'], 'surface_structures', {'absolute': -6}, 'WORLD_SURFACE_WG', 'beard_thin', 44, 16, 22360679, 'minecraft:mansion'),
    # 2.13: deep underground and very rare (a runtime shaft climbs from its front door to the surface)
    'lucky': (['minecraft:plains', 'minecraft:sunflower_plains', 'minecraft:meadow', 'minecraft:cherry_grove', 'minecraft:flower_forest',
               'minecraft:lush_caves', 'minecraft:dripstone_caves'], 'underground_structures',
              {'type': 'minecraft:uniform', 'min_inclusive': {'absolute': -24}, 'max_inclusive': {'absolute': 0}}, None, 'none', 150, 60, 77777777, 'minecraft:target_point'),
}
NATURAL = {'stone', 'deepslate', 'dirt', 'grass_block', 'sand', 'gravel', 'netherrack', 'water', 'snow_block', 'coarse_dirt', 'tuff',
           'andesite', 'diorite', 'granite', 'calcite', 'clay', 'mud', 'podzol', 'moss_block', 'rooted_dirt', 'red_sand', 'sandstone',
           'packed_ice', 'ice', 'snow', 'powder_snow', 'blue_ice', 'cobblestone', 'mossy_cobblestone', 'pale_moss_block', 'oak_leaves'}


def generate(G, builds, offers_fn):
    fn, wjson, give, title, tellraw, loot_entry, uni, KILLED, chance = (G.fn, G.wjson, G.give, G.title, G.tellraw, G.loot_entry,
                                                                        G.uni, G.KILLED, G.chance)
    PREFIX = G.PREFIX
    fast, second, tick, load = [], [], [], []
    vt = lambda name: {'type': 'minecraft:loot_table', 'value': f'minecraft:{name}'}
    pool = lambda entries, rolls=1, cond=None: dict({'rolls': rolls, 'entries': entries}, **({'conditions': cond} if cond else {}))
    frag = {'type': 'minecraft:loot_table', 'value': 'bm:p2/fragment_random'}

    # ---------------- shared loot
    wjson('bm/loot_table/p2/fragment_random.json', {'type': 'minecraft:command', 'pools': [pool([loot_entry(f'lucky_fragment_{k}') for k in range(1, 10)])]})
    wjson('bm/item_modifier/p2/consume_one.json', {'function': 'minecraft:set_count', 'count': -1, 'add': True})
    for d in D:
        V = VANILLA[d]
        wjson(f'bm/loot_table/p2/{d}/spawner.json', {'type': 'minecraft:chest', 'pools': [
            pool([loot_entry(D[d]['vkey'])]), pool([loot_entry('token')], cond=[chance(0.5)])]})      # 1.7 economy: was 1-2 every wave
        wjson(f'bm/loot_table/p2/{d}/vault.json', {'type': 'minecraft:chest', 'pools': [
            pool([vt(V[0])]), pool([loot_entry('token', uni(2, 4))]),
            pool([loot_entry('medallion')], cond=[chance(0.35)]), pool([frag], cond=[chance(0.15)]),
            pool([{'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': uni(1, 3)}]}])] + ([pool([loot_entry(i) for i in ('rabbit_foot', 'halo_fortune', 'midas_boots', 'pocket_slots')], cond=[chance(0.25)])] if d == 'lucky' else [])})
        # 2.13: a victor's (ominous) vault gives currency (Black Market + Vorn), this boss's own prizes, and one rare vanilla treasure
        item_ = lambda name, lo=1, hi=1, w=1: dict({'type': 'minecraft:item', 'name': f'minecraft:{name}', 'weight': w},
                                                 **({'functions': [{'function': 'minecraft:set_count', 'count': uni(lo, hi)}]} if hi > 1 else {}))
        rare = pool([item_('heavy_core', w=2), item_('emerald_block', 2, 4, 6), item_('diamond', 3, 6, 8), item_('enchanted_golden_apple', w=3),
                     item_('diamond_block', 1, 2, 2), item_('netherite_upgrade_smithing_template', w=2)])
        xen = pool([dict(loot_entry(f'xenite_{c}', uni(2, 4)), weight=1) for c in ('green', 'violet', 'cyan')])
        vic = [pool([loot_entry('token', uni(4, 6))]), pool([loot_entry('medallion', uni(1, 2))]), xen,
               pool([loot_entry('trophy')], cond=[chance(0.25)]), rare]
        drop, p, _ = BOSS_DROP[d]
        if drop: vic.append(pool([loot_entry(drop)], cond=[chance(0.25)]))
        if D[d].get('next_map'): vic.append(pool([loot_entry(D[d]['next_map'])]))
        if d not in ('hollow', 'lucky'): vic.append(pool([frag], cond=[chance(0.3)]))
        if d == 'hollow':
            vic = [pool([loot_entry(i)]) for i in ['conq_helmet', 'conq_chestplate', 'conq_leggings', 'conq_boots',
                                                     'conq_blade', 'conq_pick', 'conq_axe', 'conq_shovel', 'conq_hoe', 'conq_bow', 'hollow_wings', 'sepulchre']] + \
                  [pool([loot_entry('trophy', uni(2, 3))]), xen, rare, pool([item_('heavy_core')])]
        if d == 'lucky':
            from phase34 import LUCKY_LOOT
            vic += [pool([loot_entry('golden_donado')]), pool([dict(loot_entry(i), weight=w) for i, w in LUCKY_LOOT]),
                    pool([loot_entry('lucky_token', uni(6, 10))])]
        vic.append(pool([loot_entry(f'trophy_{d}')]))          # 2.1: every victor's vault gives that boss's placeable trophy
        wjson(f'bm/loot_table/p2/{d}/victor.json', {'type': 'minecraft:chest', 'pools': vic})
        wjson(f'bm/loot_table/p2/{d}/hidden.json', {'type': 'minecraft:chest', 'pools': [
            pool([loot_entry(i)]) for i in HIDDEN[d]] + [pool([vt(V[0])]), pool([loot_entry('token', uni(2, 3))]), pool([frag], cond=[chance(0.5)])]})
        # boss death loot (the Hollow King's first form drops nothing; his Wither form drops this)
        mob = BOSS_DROP[d][2]
        bl = [pool([{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{mob}'}])]
        if d == 'lucky':
            bl += [pool([loot_entry('lucky_trophy')]), pool([loot_entry('lucky_token', uni(12, 20))]),
                   pool([{'type': 'minecraft:item', 'name': 'minecraft:golden_apple', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 4)}]}]),
                   pool([{'type': 'minecraft:item', 'name': 'minecraft:enchanted_golden_apple'}], cond=[chance(0.25)]),
                   pool([{'type': 'minecraft:item', 'name': 'minecraft:gold_block', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 4)}]}])]
        elif d == 'hollow':
            bl += [pool([loot_entry('trophy', uni(3, 4))]), pool([loot_entry('medallion', uni(6, 9))])]
        else:
            tier = ORDER.index(d) + 1
            bl += [pool([loot_entry('token', uni(3 + tier, 5 + tier))], cond=[KILLED]),
                   pool([loot_entry('medallion', uni(1, max(1, tier)))], cond=[KILLED]),
                   pool([frag], cond=[chance(0.25)])]
            if tier >= 4: bl.append(pool([loot_entry('trophy')], cond=[KILLED, chance(0.3 if tier == 4 else 1.0)]))
            if drop: bl.append(pool([loot_entry(drop)], cond=[KILLED, chance(p)]))
        wjson(f'bm/loot_table/p2/{d}/boss.json', {'type': 'minecraft:entity', 'pools': bl})
        # trial spawners (+ an ominous version that spawns more)
        for name, roster in SPAWNERS[d].items():
            pots = []
            for k, (ent, gear, w) in enumerate(roster):
                data = {'entity': {'id': f'minecraft:{ent}', 'Tags': ['bm.seen', 'bm.dgmob']}}
                if gear:
                    eid = f'p2/equip/{d}_{name}_{k}'
                    wjson(f'bm/loot_table/{eid}.json', {'type': 'minecraft:equipment', 'pools': [
                        pool([{'type': 'minecraft:item', 'name': f'minecraft:{g}'}]) for g in gear]})
                    data['equipment'] = {'loot_table': f'bm:{eid}', 'slot_drop_chances': 0.0}
                pots.append({'data': data, 'weight': w})
            base = {'spawn_range': 4, 'total_mobs': 6.0, 'total_mobs_added_per_player': 2.0, 'simultaneous_mobs': 3.0,
                    'simultaneous_mobs_added_per_player': 1.0, 'ticks_between_spawn': 30, 'spawn_potentials': pots,
                    'loot_tables_to_eject': [{'data': f'bm:p2/{d}/spawner', 'weight': 1}]}
            wjson(f'bm/trial_spawner/{d}/{name}.json', base)
            wjson(f'bm/trial_spawner/{d}/{name}_ominous.json', dict(base, total_mobs=10.0, simultaneous_mobs=4.0, ticks_between_spawn=20))
    wjson('bm/loot_table/p2/brood/rats.json', {'type': 'minecraft:chest', 'pools': [
        pool([loot_entry('aged_cheddar')]), pool([loot_entry('token', uni(1, 2))]), pool([frag], cond=[chance(0.6)]),
        pool([{'type': 'minecraft:item', 'name': 'minecraft:string', 'functions': [{'function': 'minecraft:set_count', 'count': uni(4, 9)}]}])]})

    # ---------------- worldgen (Phase 2 structures) + dungeon floor tag for adventure zones
    floors = set()
    for d, Bd in builds.items():
        for (x, y, z), st in Bd.b.items():
            if 'air' in st and (x, y - 1, z) in Bd.b:
                below = Bd.b[(x, y - 1, z)].split('[')[0]
                if below.split(':')[1] not in NATURAL and 'air' not in below and 'light' not in below: floors.add(below)
        if d == 'hollow': continue
        biomes, step, height, hm, adapt, spacing, sep, salt, deco = WORLDGEN[d]
        wjson(f'bm/tags/worldgen/biome/has_structure/p2_{d}.json', {'values': [b if b.startswith('#') else {'id': b, 'required': False} for b in biomes]})
        wjson(f'bm/tags/worldgen/structure/p2_{d}.json', {'values': [f'bm:p2_{d}']})
        mon = {k: {'bounding_box': 'piece', 'spawns': []} for k in ('monster', 'creature', 'ambient', 'axolotls', 'misc',
                                                                     'underground_water_creature', 'water_ambient', 'water_creature')}
        st = {'type': 'minecraft:jigsaw', 'biomes': f'#bm:has_structure/p2_{d}', 'step': step, 'spawn_overrides': mon,
              'terrain_adaptation': adapt, 'start_pool': f'bm:p2_{d}/start', 'size': 1, 'start_height': height,
              'max_distance_from_center': 116, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'}
        if hm: st['project_start_to_heightmap'] = hm
        wjson(f'bm/worldgen/structure/p2_{d}.json', st)
        wjson(f'bm/worldgen/template_pool/p2_{d}/start.json', {'fallback': 'minecraft:empty', 'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': f'bm:p2_{d}',
                                      'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
        wjson(f'bm/worldgen/structure_set/p2_{d}.json', {'structures': [{'structure': f'bm:p2_{d}', 'weight': 1}],
                                                          'placement': {'type': 'minecraft:random_spread', 'spacing': spacing,
                                                                        'separation': sep, 'salt': salt}})
    wjson('bm/tags/block/dungeon_floor.json', {'values': sorted(floors)})

    # ---------------- sealed maps -> exploration maps
    maps = {d: WORLDGEN[d][8] for d in WORLDGEN}
    names = {'brood': "Broodmother's Nest", 'frost': 'Frostbound Spire', 'tide': 'Sunken Throne', 'hex': 'Hexbound Cathedral',
             'keep': "Wilfrey's Keep", 'lucky': 'The Gilded Roost'}
    for d, deco in maps.items():
        wjson(f'bm/loot_table/p2/maps/{d}.json', {'type': 'minecraft:command', 'pools': [pool([{
            'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [     # 26.3: exploration_map stamps the input item
                {'function': 'minecraft:exploration_map', 'destination': f'bm:p2_{d}', 'decoration': deco, 'zoom': 2,
                 'search_radius': 100 if d != 'lucky' else 220, 'skip_existing_chunks': False},
                {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T(f'Map to {names[d]}', D[d]['color'])}]}])]})
        if d == 'lucky': continue
        G.consume_adv(f'sealed_map_{d}', f'bm:p2/maps/open_{d}')
        fn(f'p2/maps/open_{d}', [f'advancement revoke @s only bm:consume/sealed_map_{d}', f'loot give @s loot bm:p2/maps/{d}',
                                 title('@s', 'actionbar', T(f'The seal cracks... the map reveals {names[d]}.', 'aqua')),
                                 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8'])

    def return_to_hand(iid):
        return [f'execute unless items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with {G.item_arg(iid)}',
                f'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{iid}"}}] run ' + give(iid)]

    # ---------------- lucky map: nine fragments -> one map
    for k in range(1, 10):
        G.consume_adv(f'lucky_fragment_{k}', f'bm:p2/lucky/frag{k}')
        fn(f'p2/lucky/frag{k}', [f'advancement revoke @s only bm:consume/lucky_fragment_{k}'] + return_to_hand(f'lucky_fragment_{k}') +
           ['function bm:p2/lucky/assemble'])
    fn('p2/lucky/assemble', ['scoreboard players set #n bm.rng 0'] +
       [f'execute if items entity @s container.* *[minecraft:custom_data~{{bm:"lucky_fragment_{k}"}}] run scoreboard players add #n bm.rng 1' for k in range(1, 10)] +
       ['execute if score #n bm.rng matches 9 run return run function bm:p2/lucky/make_map',
        title('@s', 'actionbar', [T('Lucky map pieces: ', 'gold'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'yellow'}, T(' / 9 (keep them in your main inventory)', 'gold')])])
    fn('p2/lucky/make_map', [f'clear @s *[minecraft:custom_data~{{bm:"lucky_fragment_{k}"}}] 1' for k in range(1, 10)] +
       ['loot give @s loot bm:p2/maps/lucky', 'title @s times 10 70 20', title('@s', 'subtitle', T('The nine pieces fit together...', 'gray', italic=True)),
        title('@s', 'title', T('THE GILDED ROOST', '#ffd700', bold=True)), 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2'])
    # fragment sources: vanilla chests (3%), Lucky mobs (6%), the Lucky Golden Goose (50%)
    for t in G.CHESTS:
        G.FUNCS[f'loot/{t}'] += ['execute store result score @s bm.rng run random value 1..100',
                                 'execute if score @s bm.rng matches 1..3 run function bm:p2/lucky/chest_frag']
    fn('p2/lucky/chest_frag', ['loot give @s loot bm:p2/fragment_random',
                               tellraw('@s', PREFIX + [T('A torn scrap of golden map is stuck to the lid!', 'gold')])])

    # ---------------- items: Shard of the Hollow Throne, Tome of Blinking
    G.consume_adv('hollow_summons', 'bm:p2/hollow/use')
    ox, oy, oz = HOLLOW_ORIGIN
    hb = builds.get('hollow')
    ex, ey, ez = (hb.meta['entrance'] if hb else (40, 10, 4))
    # 2.48: the Shard is retired - the Hollow Gate is the way in. An old shard re-forms as a gate.
    fn('p2/hollow/use', ['advancement revoke @s only bm:consume/hollow_summons', give('hollow_gate'),
                         'particle minecraft:ash ~ ~1 ~ 0.3 0.5 0.3 0 30', 'playsound minecraft:block.deepslate.place player @s ~ ~ ~ 1 0.6',
                         tellraw('@s', PREFIX + [T('The shard crumbles... and the pieces re-form as a ', 'gray'), T('Hollow Gate', '#c8c4d8', bold=True),
                                                 T('. Set it up and give it your five Emblems.', 'gray')])])
    fn('p2/hollow/enter', ['execute store result score @s bm.rx run data get entity @s Pos[0]', 'execute store result score @s bm.ry run data get entity @s Pos[1]',
                           'execute store result score @s bm.rz run data get entity @s Pos[2]', 'scoreboard players set @s bm.ret 1',
                           'scoreboard players set @s bm.rd 0', 'execute if dimension minecraft:the_nether run scoreboard players set @s bm.rd 1',
                           'execute if dimension minecraft:the_end run scoreboard players set @s bm.rd 2',
                           f'execute in bm:hollow_throne run tp @s {ox + ex + 0.5} {oy + ey} {oz + ez + 0.5}',
                           'effect give @s minecraft:darkness 4 0 true', 'title @s times 10 60 20',
                           title('@s', 'subtitle', T('Beyond the world, a throne waits.', 'gray', italic=True)),
                           title('@s', 'title', T('THE HOLLOW THRONE', '#e5e4e2', bold=True)),
                           'playsound minecraft:block.portal.travel ambient @s ~ ~ ~ 0.4 0.5'])
    fn('p2/hollow/leave', ['execute unless score @s bm.ret matches 1 in minecraft:overworld run return run spreadplayers 0 0 0 1 false @s',
                           'execute store result storage bm:tmp ret.x int 1 run scoreboard players get @s bm.rx',
                           'execute store result storage bm:tmp ret.y int 1 run scoreboard players get @s bm.ry',
                           'execute store result storage bm:tmp ret.z int 1 run scoreboard players get @s bm.rz',
                           'data modify storage bm:tmp ret.d set value "minecraft:overworld"',
                           'execute if score @s bm.rd matches 1 run data modify storage bm:tmp ret.d set value "minecraft:the_nether"',
                           'execute if score @s bm.rd matches 2 run data modify storage bm:tmp ret.d set value "minecraft:the_end"',
                           'function bm:p2/hollow/tp_back with storage bm:tmp ret',
                           'playsound minecraft:block.portal.travel ambient @s ~ ~ ~ 0.3 1.2'])
    fn('p2/hollow/tp_back', ['$execute in $(d) run tp @s $(x) $(y) $(z)'])
    # ---------------- 2.4 Warpstone (the final boss's reward): in and out of the Hollow Throne from anywhere
    G.consume_adv('hollow_warpstone', 'bm:p2/hollow/warp')
    fn('p2/hollow/warp', ['advancement revoke @s only bm:consume/hollow_warpstone'] + return_to_hand('hollow_warpstone') + [
        'execute unless score @s bm.conq matches 6.. run return run ' + title('@s', 'actionbar', T('The stone is cold. Only the Hollow King\'s conqueror may use it.', 'gray')),
        'execute if score @s bm.wpc matches 1.. run return run ' + title('@s', 'actionbar', T('The Warpstone is still humming... wait a moment.', 'gray')),
        'scoreboard players set @s bm.wpc 10',
        'execute if dimension bm:hollow_throne run return run function bm:p2/hollow/leave',
        f'execute unless score #hver bm.p2 matches {HOLLOW_VER} run return run ' + title('@s', 'actionbar', T('The Throne is still forming... try again in a moment.', 'gray')),
        'function bm:p2/hollow/enter'])
    second.append('scoreboard players remove @a[scores={bm.wpc=1..}] bm.wpc 1')
    fn('p2/hollow/warp_grant', ['tag @s add bm.got_warp', give('hollow_warpstone'),
                                tellraw('@s', G.PREFIX + [T('The Hollow King\'s Warpstone is yours: use it anywhere, any time, to cross over and back.', '#e5e4e2')])])
    second.append('execute as @a[scores={bm.conq=6..},tag=!bm.got_warp] run function bm:p2/hollow/warp_grant')
    # ---------------- 2.4 Wilfrey's Rest: placed once beside the citadel
    gx, gy, gz = ox + GRAVE_OFFSET[0], oy + GRAVE_OFFSET[1], oz + GRAVE_OFFSET[2]
    # 2.5: version 2 (somber) replaces 2.4's blossoming islet - its volume is cleared first (fill limit: three slabs)
    clear = [f'execute in bm:hollow_throne run fill {gx} {gy + y0} {gz} {gx + 40} {gy + y1} {gz + 40} minecraft:air' for y0, y1 in ((0, 13), (14, 27), (28, 39))]
    box = f'x={gx},y={gy},z={gz},dx=41,dy=40,dz=41'
    fn('p2/hollow/try_grave', [f'execute in bm:hollow_throne run forceload add {gx - 8} {gz - 8} {gx + 48} {gz + 48}',
                               f'execute in bm:hollow_throne store success score #gload bm.p2 if loaded {gx + 20} {gy} {gz + 20}',
                               'execute unless score #gload bm.p2 matches 1 run return 0',
                               f'execute if score #gver bm.p2 matches 1 in bm:hollow_throne run kill @e[type=minecraft:item_display,{box}]',
                               f'execute if score #gver bm.p2 matches 1 in bm:hollow_throne run kill @e[type=minecraft:interaction,tag=bm.wgrave_box,{box}]',
                               f'execute if score #gver bm.p2 matches 1 in bm:hollow_throne run kill @e[type=minecraft:marker,{box}]'] +
       [f'execute if score #gver bm.p2 matches 1 run {c}' for c in clear] +
       [f'execute in bm:hollow_throne store success score #gbuilt bm.p2 run place template bm:p2_wilfrey_grave {gx} {gy} {gz}',
        'execute if score #gbuilt bm.p2 matches 1 run scoreboard players set #gver bm.p2 2',
        'execute if score #gbuilt bm.p2 matches 1 in bm:hollow_throne run forceload remove all'])
    second.append(f'execute unless score #gver bm.p2 matches 2 if score #hver bm.p2 matches {HOLLOW_VER} run function bm:p2/hollow/try_grave')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.rift] at @s as @a[distance=..1.3] at @s run function bm:p2/hollow/leave')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.rift] at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.02 6')
    sx, sz = (hb.size[0], hb.size[2]) if hb else (152, 152)
    sy_ = hb.size[1] if hb else 128
    hbox = f'x={ox},y={oy},z={oz},dx={sx},dy={sy_},dz={sz}'
    fn('p2/hollow/try_build', [f'execute in bm:hollow_throne run forceload add {ox - 16} {oz - 16} {ox + sx + 16} {oz + sz + 16}',
                               f'execute in bm:hollow_throne store success score #hload bm.p2 if loaded {ox} {oy} {oz} if loaded {ox + sx - 1} {oy} {oz + sz - 1} if loaded {ox} {oy} {oz + sz - 1} if loaded {ox + sx - 1} {oy} {oz}',
                               'execute unless score #hload bm.p2 matches 1 run return run scoreboard players set #hwait bm.p2 0',
                               'scoreboard players add #hwait bm.p2 1', 'execute unless score #hwait bm.p2 matches 4.. run return 0',   # entities load a moment after blocks
                               # a rebuild (a newer Hollow): the old copy's markers, displays and mobs go first, or they'd double up
                               f'execute if score #hver bm.p2 matches 1.. in bm:hollow_throne run kill @e[type=!minecraft:player,{hbox}]',
                               'scoreboard players set #built bm.p2 0',
                               f'execute in bm:hollow_throne store success score #built bm.p2 run place template bm:p2_hollow {ox} {oy} {oz}',
                               f'execute if score #built bm.p2 matches 1 if score #gver bm.p2 matches 2 run scoreboard players set #gver bm.p2 1',
                               f'execute if score #built bm.p2 matches 1 run scoreboard players set #hver bm.p2 {HOLLOW_VER}',
                               'execute if score #built bm.p2 matches 1 in bm:hollow_throne run forceload remove all'])
    second.append(f'execute unless score #hver bm.p2 matches {HOLLOW_VER} run function bm:p2/hollow/try_build')
    # islet wayshrines (crying obsidian pads) carry you back to the arrival rock
    fn('p2/hollow/isle_home', ['particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 30',
                               'tp @s @e[type=minecraft:marker,tag=bm.isle_home,sort=nearest,limit=1]',
                               'playsound minecraft:block.respawn_anchor.deplete player @s ~ ~ ~ 0.6 1.4'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.isle_ret] at @s as @a[distance=..1.2] at @s run function bm:p2/hollow/isle_home')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.isle_ret] at @s if entity @a[distance=..24] run particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.3 0.1 0.3 0.01 2')
    # mob griefing is off while anyone is in the Hollow Throne (the Wither can't wreck the castle), restored afterwards
    fn('p2/hollow/mg_off', ['execute store result score #mgwas bm.p2 run gamerule mob_griefing', 'gamerule mob_griefing false',
                            'scoreboard players set #mgoff bm.p2 1'])
    fn('p2/hollow/mg_on', ['execute if score #mgwas bm.p2 matches 1 run gamerule mob_griefing true', 'scoreboard players set #mgoff bm.p2 0'])
    second += ['scoreboard players set #inh bm.p2 0',
               'execute as @a at @s if dimension bm:hollow_throne run scoreboard players set #inh bm.p2 1',
               'execute if score #inh bm.p2 matches 1 unless score #mgoff bm.p2 matches 1 run function bm:p2/hollow/mg_off',
               'execute if score #inh bm.p2 matches 0 if score #mgoff bm.p2 matches 1 run function bm:p2/hollow/mg_on']
    # rare loot on the islets (elytra only)
    wjson('bm/loot_table/p2/hollow/isle.json', {'type': 'minecraft:chest', 'pools': [
        pool([{'type': 'minecraft:item', 'name': 'minecraft:netherite_ingot', 'weight': 3},
              {'type': 'minecraft:item', 'name': 'minecraft:enchanted_golden_apple', 'weight': 3},
              {'type': 'minecraft:item', 'name': 'minecraft:totem_of_undying', 'weight': 2},
              {'type': 'minecraft:item', 'name': 'minecraft:netherite_upgrade_smithing_template', 'weight': 2},
              dict(loot_entry('heartstone'), weight=2), dict(loot_entry('trophy'), weight=2)]),
        pool([loot_entry('medallion', uni(1, 2))]),
        pool([{'type': 'minecraft:item', 'name': 'minecraft:diamond', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 5)}]}]),
        pool([{'type': 'minecraft:loot_table', 'value': 'bm:p2/fragment_random'}], cond=[chance(0.25)])]})
    G.consume_adv('blink_tome', 'bm:p2/items/blink')
    fn('p2/items/blink', ['advancement revoke @s only bm:consume/blink_tome'] + return_to_hand('blink_tome') + [
        'execute if entity @s[tag=bm.adv] run return run ' + title('@s', 'actionbar', T('The tome refuses to work in a place like this.', 'gray')),
        'execute rotated ~ 0 positioned ^ ^ ^7 unless block ~ ~ ~ #minecraft:air run return run ' + title('@s', 'actionbar', T('Something solid blocks the way.', 'gray')),
        'execute rotated ~ 0 positioned ^ ^ ^7 unless block ~ ~1 ~ #minecraft:air run return run ' + title('@s', 'actionbar', T('Something solid blocks the way.', 'gray')),
        'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 30', 'execute rotated ~ 0 positioned ^ ^ ^7 run tp @s ~ ~ ~',
        'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.8 0.3 0.05 30'])

    # ---------------- Conqueror's set: per-piece buffs, held buffs, full-set aura ("the dead keep their distance")
    worn = {'helmet': ['night_vision 15 0', 'water_breathing 11 0'], 'chestplate': ['strength 11 0', 'resistance 11 0'],
            'leggings': ['regeneration 11 0', 'haste 11 0'], 'boots': ['speed 11 0', 'fire_resistance 11 0']}
    slot = {'helmet': 'armor.head', 'chestplate': 'armor.chest', 'leggings': 'armor.legs', 'boots': 'armor.feet'}
    for p, effs in worn.items():
        for e in effs:
            fast.append(f'execute as @a if items entity @s {slot[p]} *[minecraft:custom_data~{{bm:"conq_{p}"}}] run effect give @s minecraft:{e.split()[0]} {e.split()[1]} {e.split()[2]} true')
    held = {'conq_pick': 'haste 3 1', 'conq_shovel': 'haste 3 1', 'conq_blade': 'strength 3 0', 'conq_axe': 'strength 3 0', 'conq_bow': 'speed 3 0'}
    for iid, e in held.items():
        fast.append(f'execute as @a if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"{iid}"}}] run effect give @s minecraft:{e.split()[0]} {e.split()[1]} {e.split()[2]} true')
    fast.append('execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"hollow_crown"}] run effect give @s minecraft:night_vision 15 0 true')
    fn('p2/sets/has/conqueror', ['return run execute ' + ' '.join(f'if items entity @s {slot[p]} *[minecraft:custom_data~{{bm_set:"conqueror"}}]' for p in slot)])
    fn('p2/fx/conqueror', ['$execute rotated $(a) 0 positioned ^ ^0.15 ^0.9 run particle minecraft:soul_fire_flame ~ ~ ~ 0 0 0 0 1',
                           '$execute rotated $(b) 0 positioned ^ ^0.15 ^0.9 run particle minecraft:soul_fire_flame ~ ~ ~ 0 0 0 0 1',
                           '$execute rotated $(a) 0 positioned ^ ^2.2 ^0.4 run particle minecraft:sculk_soul ~ ~ ~ 0 0 0 0 1'])
    fn('p2/sets/conqueror', ['function bm:p2/fx/conqueror with storage bm:fx',
                             'particle minecraft:smoke ~ ~0.1 ~ 0.2 0 0.2 0 1',
                             'effect give @e[type=#minecraft:undead,distance=..5,tag=!bm.boss] minecraft:weakness 2 0 true',
                             'execute store result score #r bm.rng run random value 1..40',
                             'execute if score #r bm.rng matches 1 run playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 0.25 0.7'])
    fast.append('execute as @a[gamemode=!spectator] if function bm:p2/sets/has/conqueror at @s run function bm:p2/sets/conqueror')

    # ---------------- trader refresh: existing traders in old markets learn the new trades (keys, maps, Lucky Trophy)
    # (2.6: handled by phase17's checksum refresh, which already includes the Phase 2 trades)

    # ---------------- the Hollow Throne dimension (void; the dungeon is placed by command once)
    wjson('bm/dimension_type/hollow_throne.json', {
        'ambient_light': 0.03, 'has_skylight': False, 'has_ceiling': False, 'has_ender_dragon_fight': False, 'coordinate_scale': 1.0,
        'logical_height': 256, 'min_y': 0, 'height': 256, 'infiniburn': '#minecraft:infiniburn_end',
        'monster_spawn_light_level': 0, 'monster_spawn_block_light_limit': 0, 'has_fixed_time': True,
        'default_clock': 'minecraft:the_end', 'timelines': '#minecraft:in_end', 'skybox': 'none',          # 2.2: no sky - a crimson void
        'attributes': {
            'minecraft:audio/ambient_sounds': {'mood': {'block_search_extent': 8, 'offset': 2.0, 'sound': 'minecraft:ambient.soul_sand_valley.mood', 'tick_delay': 3000}},
            'minecraft:audio/background_music': {'default': {'max_delay': 12000, 'min_delay': 3000, 'replace_current_music': True, 'sound': 'minecraft:music.nether.soul_sand_valley'}},
            'minecraft:gameplay/bed_rule': {'can_set_spawn': 'never', 'can_sleep': 'never', 'explodes': True},
            'minecraft:gameplay/respawn_anchor_works': False,
            'minecraft:visual/ambient_light_color': '#2a1214', 'minecraft:visual/fog_color': '#3a0609',
            'minecraft:visual/fog_start_distance': 24.0, 'minecraft:visual/fog_end_distance': 220.0,
            'minecraft:visual/ambient_particles': [{'particle': {'type': 'minecraft:white_ash'}, 'probability': 0.012},
                                                   {'particle': {'type': 'minecraft:crimson_spore'}, 'probability': 0.004}],
            'minecraft:visual/sky_light_color': '#5a1a1e', 'minecraft:visual/sky_light_factor': 0.0}})
    wjson('bm/dimension/hollow_throne.json', {'type': 'bm:hollow_throne', 'generator': {'type': 'minecraft:flat', 'settings': {
        'biome': 'minecraft:the_void', 'features': False, 'lakes': False, 'layers': [{'block': 'minecraft:air', 'height': 1}], 'structure_overrides': []}}})
    return dict(fast=fast, second=second, tick=tick, load=load)
