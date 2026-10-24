"""2.91: THE UNDERWATER KINGDOM - Emma's home: a ruined castle on the deep sea floor under a bubble dome (kingdom.py builds it).

IN THE WORLD: rare, in deep oceans. You come in through the TIDE DOOR (the shimmering pane in the dome's north side: swim into
  it), up the grey path to the gate. Inside: the yard and its fountain (the DOME HEART floats over it), the keep at the back -
  the throne room - with the TIDE FONT between the thrones, the Royal Steward (a rat in royal blue) and the Request Stand.
BRING THE ROYAL FAMILY HOME (right-click the Tide Font with them beside you):
  each one's HOMECOMING, once each - Emma: the Tidecaller Shell; Queen Ava: the Sea-Glass Locket; Queen Pearl: the Regent's Seal;
  Bones: the Shark-Tooth Charm. THE ROYAL FAMILY TOGETHER (Emma, Queen Ava and Queen Pearl - a full follower party):
  THE FULL COURT - the castle is RESTORED (the fires go out, the fallen tower and the broken walls stand again) and you're
  given the Crown of the Deep. After that, the full court at the Font holds a TIDE FESTIVAL once a day (Royal Pearls and favour
  for everyone there). Any royal at the Font (Bones counts): a daily ROYAL AUDIENCE (a pearl for each royal with you).
THE HIDDEN ONE: bring APOPHISS into the throne room. The carved stone behind the thrones knows its old master and grinds open
  on the Serpent's Alcove; at its plinth (with him beside you) is the penance he sealed there long ago - TIDE-BREAKER, and if
  Queen Ava is with you too, her pardon.
EVERY DAY: the Royal Treasury (the steward's barrels) pays a tribute of Royal Pearls; the Request Stand asks for one thing
  (it changes daily); the Steward's last trade is a daily special. Favour from requests, breaches and festivals earns ranks -
  Courtier, Knight of the Tide, Royal Champion (whose Royal Charter adds a pearl to every tribute).
DOME BREACHES: (2.93b) only when someone calls them - right-click the Dome Heart twice - then the dome rests 10 minutes. The
  dome cracks and Tide Raiders come through. Right-click each crack
  before the minute is up. A crack that bursts lets the sea in; three and the dome SHATTERS - the castle floods. The Dome Heart
  raises it again (a Heart of the Sea, or Queen Ava beside you); sneak + right-click it to mend leaks (2 Royal Pearls)."""
import math
from items import item, T, TOTEM, ITEMS, consumable, ench, attr
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import kingdom as K

KC, PEARL_C, GOLD = '#5ac8ff', '#d8f4ff', '#ffd66a'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
ROYALS = [('emma', 'Emma', 'bm.emmapet,tag=!bm.ffpet', '#ff8ad8'), ('ava', 'Queen Ava', 'bm.avpet,tag=!bm.ffpet', '#6ad8e8'),
          ('pearl', 'Queen Pearl', 'bm.pqpet,tag=!bm.ffpet', '#5ae0d8'), ('bones', 'Bones', 'bm.bjpet,tag=!bm.ffpet', '#a8b4bc')]
APO = 'bm.appet,tag=!bm.ffpet'
CORE = (35.5, K.P, K.KEEP[1] - 2.5)                 # the core marker's spot in the template (blocks are relative to (35, P, 41))
RANKS = [(5, 'Courtier', '#9ad8ff'), (12, 'Knight of the Tide', '#5ac8ff'), (25, 'Royal Champion', GOLD)]
REQUESTS = [('kelp', 32, 2, 'kelp for the royal kitchens'), ('prismarine_shard', 16, 2, 'prismarine shards to patch the walls'),
            ('cod', 16, 2, 'cod for the fishmongers'), ('ink_sac', 8, 2, 'ink for the royal scribes'), ('glass', 32, 3, 'glass to mend the dome'),
            ('sea_pickle', 8, 2, 'sea pickles for the lamps'), ('nautilus_shell', 1, 4, 'a nautilus shell for the treasury'),
            ('gold_ingot', 8, 3, 'gold to regild the thrones'), ('stone_bricks', 64, 3, 'stone bricks to rebuild the towers'),
            ('magenta_dye', 8, 2, 'magenta dye for new flags'), ('tropical_fish', 4, 3, 'tropical fish for the fountain'),
            ('light_blue_dye', 8, 2, 'blue dye for the roofs')]
SPECIALS = [(('royal_pearl', 18), ('enchanted_golden_apple', 1)), (('royal_pearl', 14), ('netherite_scrap', 2)),
            (('royal_pearl', 12), ('totem_of_undying', 1)), (('royal_pearl', 10), ('echo_shard', 3)), (('royal_pearl', 6), ('medallion', 2)),
            (('royal_pearl', 8), ('music_disc_otherside', 1)), (('royal_pearl', 16), ('heartstone', 1))]
BREACH_SECS, BREACH_REST, CRACKS, SHATTER_AT = 60, 600, 4, 3


# ================================================================================================ items
item('royal_pearl', TOTEM, 'Royal Pearl', PEARL_C,
     ['A pearl of the Underwater Kingdom\'s treasury,', 'stamped with the royal crest.', ('Spend it with the Royal Steward.', 'aqua'),
      ('Paid in tribute, for requests, festivals', 'gray'), ('and for keeping the dome whole.', 'gray')],
     model='bm:royal_pearl', stack=64, cat='currency')
item('tidecaller_shell', TOTEM, 'Tidecaller Shell', '#ff8ad8',
     ['Emma\'s - she says she\'s too old for it now.', ('Use it: three minutes of Water Breathing,', 'blue'), ("Dolphin's Grace and Conduit Power.", 'blue'),
      ('Two minutes to recharge.', 'gray'), ('Emma\'s homecoming gift.', 'dark_gray')],
     model='bm:tidecaller_shell', stack=1, cat='magic', glint=True,
     comps=dict(hold('none'), **{'minecraft:use_cooldown': {'seconds': 120.0, 'cooldown_group': 'bm:tidecaller'}}))
HOLD['tidecaller_shell'] = 'bm:p199/shell/use'
item('sea_glass_locket', TOTEM, 'Sea-Glass Locket', '#6ad8e8',
     ['A locket of sea glass from the queen\'s own window.', ('Carried: Water Breathing; in the water,', 'blue'), ('Regeneration too.', 'blue'),
      ('Queen Ava\'s homecoming gift.', 'dark_gray')], model='bm:sea_glass_locket', stack=1, cat='magic', glint=True)
item('regent_seal', TOTEM, "Regent's Seal", '#5ae0d8',
     ['The seal Queen Pearl ruled with, for her niece.', ('Carried: Hero of the Village -', 'blue'), ('traders give you their best prices.', 'blue'),
      ('Queen Pearl\'s homecoming gift.', 'dark_gray')], model='bm:regent_seal', stack=1, cat='magic', glint=True)
item('shark_tooth_charm', TOTEM, 'Shark-Tooth Charm', '#a8b4bc',
     ['One of Bones\'s baby teeth. He has plenty.', ('Carried, in the water: Strength', 'blue'), ('and Speed II.', 'blue'),
      ('Bones\'s homecoming gift.', 'dark_gray')], model='bm:shark_tooth_charm', stack=1, cat='magic', glint=True)
item('crown_of_the_deep', 'minecraft:turtle_helmet', 'Crown of the Deep', GOLD,
     ['Given by the full court of the Underwater Kingdom.', ('Breathe, see and dig under water as on land;', 'blue'),
      ('swim like the royal family.', 'blue'), ('Unbreakable.', 'blue')],
     stack=1, cat='gear', bold=True, glint=True,
     comps={'minecraft:unbreakable': {}, 'minecraft:enchantments': ench(respiration=3, aqua_affinity=1, protection=4),
            'minecraft:attribute_modifiers': [attr('armor', 4, 'head'), attr('armor_toughness', 3, 'head'), attr('oxygen_bonus', 4, 'head'),
                                              attr('submerged_mining_speed', 1.0, 'head'), attr('water_movement_efficiency', 0.6, 'head'),
                                              attr('max_health', 4, 'head')]})
item('tide_breaker', 'minecraft:trident', 'Tide-Breaker', '#3aff9a',
     ['The weapon Apophiss swore never to lift against the sea,', 'sealed in the castle\'s wall as his penance.',
      ('Loyalty III, Impaling V, Channeling; unbreakable.', 'blue'), ('+6 Attack Damage.', 'blue'), ('Found in the Serpent\'s Alcove.', 'dark_gray')],
     stack=1, cat='gear', bold=True, glint=True,
     comps={'minecraft:unbreakable': {}, 'minecraft:enchantments': ench(loyalty=3, impaling=5, channeling=1),
            'minecraft:attribute_modifiers': [attr('attack_damage', 14, 'mainhand', ident='minecraft:base_attack_damage'),
                                              attr('attack_speed', -2.9, 'mainhand', ident='minecraft:base_attack_speed')]})
item('sealed_map_kingdom', TOTEM, 'Sealed Royal Chart', KC,
     ['Hold right-click to break the seal.', 'Marks the nearest Underwater Kingdom,', 'deep under the sea.'],
     model='minecraft:map', glint=True, stack=16, comps={'minecraft:consumable': consumable(0.8, 'none', 'minecraft:item.book.page_turn', False)}, cat='map')


def extend_offers(O, offer):
    O['dock'] += [offer(('token', 6), ('sealed_map_kingdom', 1))]


import phase177 as _P177
_P177.STOCK.append(('sealed_map_kingdom', 1, 2))                    # (2.94: Vesper sells it too - and the Royal Steward no longer does)


# ================================================================================================ art: icons, the steward
def _icons():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    out = {}
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)                    # the Royal Pearl: a pearl, a crest
    d.ellipse((2, 2, 13, 13), fill=hexc('#a8c8dc')); d.ellipse((3, 3, 12, 12), fill=hexc('#e8f6ff')); d.ellipse((4, 3, 8, 7), fill=hexc('#ffffff'))
    d.polygon([(6, 9), (7, 7), (8, 9), (9, 7), (10, 9), (10, 11), (6, 11)], fill=hexc('#ffd66a'))
    out['royal_pearl'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)                    # the Tidecaller Shell: a pink conch
    d.polygon([(2, 12), (6, 3), (13, 6), (14, 12)], fill=hexc('#ff8ad8'), outline=hexc('#c0508a'))
    for i in range(4): d.line([(4 + i * 2, 12), (7 + i * 1.5, 4 + i)], fill=hexc('#ffd0e8'))
    d.point((12, 7), fill=hexc('#ffffff')); out['tidecaller_shell'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)                    # the Sea-Glass Locket
    d.line([(4, 1), (8, 5), (12, 1)], fill=hexc('#c0c8d0')); d.ellipse((4, 5, 12, 14), fill=hexc('#2a8a9a')); d.ellipse((5, 6, 11, 13), fill=hexc('#6ad8e8'))
    d.point((7, 8), fill=hexc('#ffffff')); out['sea_glass_locket'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)                    # the Regent's Seal: a wax seal with a crown
    d.ellipse((2, 3, 13, 14), fill=hexc('#6a3aa0')); d.ellipse((3, 4, 12, 13), fill=hexc('#8a5ac8'))
    d.polygon([(5, 11), (5, 7), (6, 9), (7.5, 6), (9, 9), (10, 7), (10, 11)], fill=hexc('#ffd66a')); out['regent_seal'] = im
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)                    # the Shark-Tooth Charm
    d.arc((1, -6, 15, 8), 20, 160, fill=hexc('#7a5a3a')); d.polygon([(6, 5), (10, 5), (8, 14)], fill=hexc('#f4f0e0'), outline=hexc('#9a9480'))
    out['shark_tooth_charm'] = im
    return out


def rp(R):
    import sys
    cube, RAT_BASE, RAT_TEX = R.cube, R.RAT_BASE, R.RAT_TEX
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS.update(_icons())
    # the Royal Steward: a rat in a royal-blue coat with gold buttons, a little crown
    kit = [cube((5.8, 3, 6.3), (10.2, 10, 6.4), 'u'), cube((5.0, 6.2, 6.9), (11.0, 11.0, 10.6), 'u'),
           cube((7.6, 6.6, 6.75), (8.4, 7.4, 6.9), 'y'), cube((7.6, 8.2, 6.75), (8.4, 9.0, 6.9), 'y'),
           cube((5.6, 16, 6.6), (10.4, 16.8, 9.9), 'y'), cube((5.6, 16.8, 6.6), (6.4, 17.8, 7.4), 'y'), cube((7.6, 16.8, 6.6), (8.4, 18.2, 7.4), 'y'),
           cube((9.6, 16.8, 6.6), (10.4, 17.8, 7.4), 'y'), cube((7.7, 17.4, 6.5), (8.3, 17.9, 6.6), 'c')]
    R.HATS['rat3d_steward'] = (dict(RAT_TEX, u='minecraft:block/blue_wool', c='minecraft:block/light_blue_wool'), RAT_BASE + kit)


def textures():
    return {}


def generate_early(G):
    pass


# ================================================================================================ the datapack
def generate(G):
    fn, wjson, tellraw, title, give = G.fn, G.wjson, G.tellraw, G.title, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = G.PREFIX
    tick, fast, second = [], [], []
    objs = ['bm.kbcd', 'bm.kbask', 'bm.kgst', 'bm.kdome', 'bm.kday', 'bm.kfest', 'bm.kbr', 'bm.kbn', 'bm.kburst', 'bm.ktrib', 'bm.kreq', 'bm.kaud', 'bm.kfav',
            'bm.krank', 'bm.kin', 'bm.kcd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [f'scoreboard players set #{n} bm.rng {n}' for n in (7, len(REQUESTS))]
    G.OBJECTIVES += objs
    core = '@e[type=minecraft:marker,tag=bm.kingdom,distance=..70,sort=nearest,limit=1]'
    near_core = lambda cmd: f'execute as {core} at @s run {cmd}'
    rel = lambda x, y, z: f'~{x - 35:g} ~{y - K.P:g} ~{z - 41:g}'                      # a template block, from the core marker

    # ---------------------------------------------------------------- worldgen: rare, deep oceans; built when someone comes near
    wjson('bm/tags/worldgen/biome/has_structure/p199_kingdom.json',
          {'values': ['minecraft:deep_ocean', 'minecraft:deep_cold_ocean', 'minecraft:deep_lukewarm_ocean', 'minecraft:deep_frozen_ocean']})
    wjson('bm/tags/worldgen/structure/p199_kingdom.json', {'values': ['bm:p199_kingdom']})
    wjson('bm/worldgen/structure/p199_kingdom.json', {'type': 'minecraft:jigsaw', 'biomes': '#bm:has_structure/p199_kingdom', 'step': 'surface_structures',
                                                      'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': 'bm:p199_kingdom/start', 'size': 1,
                                                      'start_height': {'absolute': 0}, 'project_start_to_heightmap': 'OCEAN_FLOOR_WG',
                                                      'max_distance_from_center': 80, 'use_expansion_hack': False, 'liquid_settings': 'ignore_waterlogging'})
    wjson('bm/worldgen/template_pool/p199_kingdom/start.json', {'fallback': 'minecraft:empty', 'elements': [
        {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': 'bm:p199_kingdom_seed', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
    wjson('bm/worldgen/structure_set/p199_kingdom.json', {'structures': [{'structure': 'bm:p199_kingdom', 'weight': 1}],
                                                          'placement': {'type': 'minecraft:random_spread', 'spacing': 64, 'separation': 24, 'salt': 91990133,
                                                                        # (2.92: never in an ocean monument's lap)
                                                                        'exclusion_zone': {'other_set': 'minecraft:ocean_monuments', 'chunk_count': 6}}})
    from structures import Build
    Bs = Build(1, 1, 1)
    Bs.marker(0.5, 0.0, 0.5, ['bm.kseed'], 0)
    Bs.export(G.path('data', 'bm', 'structure', 'p199_kingdom_seed.nbt'))
    Bk = K.build()
    errs = K.check(Bk)
    assert not errs, errs[:10]
    Bk.export(G.path('data', 'bm', 'structure', 'p199_kingdom.nbt'))
    K.restored_crop().export(G.path('data', 'bm', 'structure', 'p199_kingdom_restored.nbt'))
    OX, OY, OZ = -35, -K.FY, -35                                                      # the template's corner, from the seed's block
    corners = ' '.join(f'if loaded ~{x} ~ ~{z}' for x in (OX, OX + K.SX - 1) for z in (OZ, OZ + K.SZ - 1))
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.kseed] at @s if entity @a[distance=..112] {corners} run function bm:p199/k/seed')
    # (the sea floor's height: the dome's top must stay under the sea, so a seed up a slope is set down to y 34)
    fn('p199/k/seed', ['execute if entity @s[y=35,dy=400] run tp @s ~ 34 ~', 'execute at @s run function bm:p199/k/build', 'kill @s'])
    wjson('bm/tags/block/p199_soft.json', {'values': ['minecraft:sand', 'minecraft:gravel', 'minecraft:clay', 'minecraft:dirt', 'minecraft:stone',
                                                      'minecraft:red_sand', 'minecraft:mud', 'minecraft:andesite', 'minecraft:diorite', 'minecraft:granite',
                                                      'minecraft:deepslate', 'minecraft:tuff', 'minecraft:seagrass', 'minecraft:tall_seagrass',
                                                      'minecraft:kelp', 'minecraft:kelp_plant']})
    cx, cy, cz = CORE
    fn('p199/k/build', [f'place template bm:p199_kingdom ~{OX} ~{OY} ~{OZ}',
                        # the way to the Tide Door: the sea floor in front of it dug out to water
                        f'fill ~-2 ~1 ~{OZ + K.DOOR_Z - 4} ~2 ~4 ~{OZ + K.DOOR_Z - 1} minecraft:water replace #bm:p199_soft',
                        f'execute positioned ~{cx + OX:.1f} ~{cy + OY:.1f} ~{cz + OZ:.1f} as @e[type=minecraft:marker,tag=bm.kgnew,distance=..2] at @s run function bm:p199/k/init'])
    fn('p199/k/init', ['tag @s remove bm.kgnew', 'tag @s add bm.kingdom', 'scoreboard players set @s bm.kgst 0', 'scoreboard players set @s bm.kdome 0',
                       'scoreboard players set @s bm.kbr 0', 'scoreboard players set @s bm.kday -1', 'scoreboard players set @s bm.kfest -1',
                       'execute as @e[type=minecraft:marker,tag=bm.kspot_font,distance=..60] at @s run function bm:p199/k/make_font',
                       'execute as @e[type=minecraft:marker,tag=bm.kspot_steward,distance=..60] at @s run function bm:p199/k/make_steward',
                       'execute as @e[type=minecraft:marker,tag=bm.kspot_board,distance=..60] at @s run function bm:p199/k/make_board',
                       'execute as @e[type=minecraft:marker,tag=bm.kspot_heart,distance=..60] at @s run function bm:p199/k/make_heart',
                       'execute as @e[type=minecraft:marker,tag=bm.kspot_alcove,distance=..60] at @s run function bm:p199/k/make_alcove',
                       'function bm:p199/shop/refresh',
                       'playsound minecraft:ambient.underwater.enter ambient @a[distance=..96] ~ ~ ~ 1 0.6'])
    box = lambda tag, w, h, y=0: f'summon minecraft:interaction ~ ~{y} ~ {{Tags:["bm.kbox","{tag}"],width:{w}f,height:{h}f,response:1b}}'
    fn('p199/k/make_font', [box('bm.kfont', 1.4, 2.2)])
    fn('p199/k/make_board', [box('bm.kboard', 1.0, 1.6, 0)])
    fn('p199/k/make_alcove', [box('bm.kplinth', 1.2, 2.2)])
    heart = {'Tags': ['bm.kheartd'], 'item': {'id': 'minecraft:heart_of_the_sea', 'count': Int(1)}, 'item_display': 'ground', 'billboard': 'fixed',
             'brightness': {'sky': Int(15), 'block': Int(15)}, 'teleport_duration': Int(3),
             'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                'translation': [F(0), F(0.5), F(0)], 'scale': [F(1.4)] * 3}}
    insig = {'Tags': ['bm.kinsig'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:kingdom_insignia'}},
             'item_display': 'fixed', 'brightness': {'sky': Int(15), 'block': Int(13)},
             'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                'translation': [F(0), F(0), F(0)], 'scale': [F(2.6)] * 3}}
    relf = lambda x, y, z: f'~{x - 35.5:g} ~{y - K.P:g} ~{z - 41.5:g}'      # (entity spots: the core marker stands at 35.5, P, 41.5)
    insig['Rotation'] = [F(180), F(0)]
    # (2.92: hung by the castle's core, so kingdoms built before 2.92 get them too)
    fn('p199/k/insignia', ['tag @s add bm.kinsok', f'kill @e[type=minecraft:item_display,tag=bm.kinsig,distance=..70]'] +
       [f'summon minecraft:item_display {relf(x, y, z)} {snbt(insig)}' for (x, y, z) in K.INSIGNIA])
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom,tag=!bm.kinsok] at @s run function bm:p199/k/insignia')
    fn('p199/k/make_heart', [f'summon minecraft:item_display ~ ~1 ~ {snbt(heart)}', box('bm.kheart', 0.9, 1.2, 1)])
    # the Royal Steward: a frozen trader (the shop) under a rat in royal blue; his treasury barrels pay the tribute
    trader = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'DespawnDelay': Int(0),
              'Tags': ['bm.kstew', 'bm.kstnew'], 'CustomName': T('Royal Steward', KC, bold=True), 'CustomNameVisible': B(0),
              'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
              'attributes': [{'id': 'minecraft:scale', 'base': D(0.7)}], 'Offers': {'Recipes': []}}
    sprite = G.rat_sprite('bm:rat3d_steward', ['bm.rat_sprite', 'bm.kstew_sprite', 'bm.td', 'bm.r3d', 'bm.kstnew'])
    fn('p199/k/make_steward', [f'summon minecraft:wandering_trader ~ ~ ~ {snbt(trader)}', sprite,
                               'execute as @e[tag=bm.kstnew,distance=..1] run tp @s ~ ~ ~ ~ 0', 'tag @e[tag=bm.kstnew,distance=..1] remove bm.kstnew',
                               f'summon minecraft:interaction ~-1 ~1 ~-0.5 {{Tags:["bm.kbox","bm.ktrib"],width:1.0f,height:0.6f,response:1b}}'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.kseed]', 'kill @e[type=minecraft:interaction,tag=bm.kbox]',
                                       'kill @e[type=minecraft:item_display,tag=bm.kheartd]', 'kill @e[type=minecraft:item_display,tag=bm.kinsig]', 'kill @e[type=minecraft:item_display,tag=bm.kstew_sprite]',
                                       'execute as @e[type=minecraft:wandering_trader,tag=bm.kstew] at @s run tp @s ~ -300 ~']
    # the sealed chart (the Dockmaster's): the nearest kingdom
    G.consume_adv('sealed_map_kingdom', 'bm:maps/open_p199_kingdom')
    G.sealed_map('sealed_map_kingdom', 'p199_kingdom', '#bm:p199_kingdom', title('@s', 'actionbar', T('The seal cracks... the chart marks a castle under the sea.', KC)))
    wjson('bm/loot_table/maps/p199_kingdom.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [
            {'function': 'minecraft:exploration_map', 'destination': '#bm:p199_kingdom', 'decoration': 'minecraft:monument', 'zoom': 2,
             'search_radius': 100, 'skip_existing_chunks': False},
            {'function': 'minecraft:set_name', 'target': 'item_name', 'name': T('Royal Chart', KC)}]}]}]})
    # (admin: a kingdom here, now - stand on the sea floor)
    fn('admin/kingdom', ['execute align xyz positioned ~0.5 ~ ~0.5 run function bm:p199/k/build_here',
                         tellraw('@s', P + [T('The Underwater Kingdom rises here (its gate faces north; the Tide Door is 34 blocks north).', KC)])])
    fn('p199/k/build_here', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.kseed","bm.kadm"]}',
                             'execute as @e[type=minecraft:marker,tag=bm.kadm,distance=..0.5,limit=1] at @s run function bm:p199/k/build',
                             'kill @e[type=minecraft:marker,tag=bm.kadm]'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/kingdom', 'yellow'), T('  build an Underwater Kingdom here (on the sea floor)', 'gray')]))

    # ---------------------------------------------------------------- chest loot: the towers' left-behinds; the tribute
    E = G.loot_entry
    wjson('bm/loot_table/chests/p199_tower.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': {'type': 'minecraft:uniform', 'min': 3, 'max': 6}, 'entries': [
            {'type': 'minecraft:item', 'name': 'minecraft:prismarine_crystals', 'weight': 10, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 6)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:prismarine_shard', 'weight': 10, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(3, 9)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:gold_ingot', 'weight': 8, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 4)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:nautilus_shell', 'weight': 4},
            {'type': 'minecraft:item', 'name': 'minecraft:diamond', 'weight': 3, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(1, 2)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:emerald', 'weight': 6, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:golden_apple', 'weight': 3}]},
        {'rolls': {'type': 'minecraft:uniform', 'min': 1, 'max': 3}, 'entries': [E('royal_pearl', G.uni(1, 3))]},
        {'rolls': 1, 'entries': [E('token', G.uni(1, 3))], 'conditions': [G.chance(0.5)]},
        {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.08)]},
        {'rolls': 1, 'entries': [E('tide_scale', G.uni(1, 3))], 'conditions': [G.chance(0.6)]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea'}], 'conditions': [G.chance(0.05)]}]})
    wjson('bm/loot_table/p199/tribute.json', {'type': 'minecraft:command', 'pools': [
        {'rolls': 1, 'entries': [
            {'type': 'minecraft:item', 'name': 'minecraft:prismarine_crystals', 'weight': 8, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(3, 8)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:sea_lantern', 'weight': 6, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 4)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:nautilus_shell', 'weight': 4},
            {'type': 'minecraft:item', 'name': 'minecraft:gold_ingot', 'weight': 6, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(2, 5)}]},
            {'type': 'minecraft:item', 'name': 'minecraft:emerald', 'weight': 6, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(3, 7)}]},
            E('token', G.uni(1, 3)) | {'weight': 8}]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:heart_of_the_sea'}], 'conditions': [G.chance(0.03)]},
        {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.04)]}]})

    # ---------------------------------------------------------------- who's inside; the Tide Door
    # (the dome's middle is 6 blocks north of the core and 4 down; 33 round it is inside)
    dome = '~ ~-4 ~-6'
    second += ['tag @a[tag=bm.kin] remove bm.kin',
               f'execute as @e[type=minecraft:marker,tag=bm.kingdom] at @s positioned {dome} run tag @a[distance=..33,gamemode=!spectator] add bm.kin',
               'execute as @a[tag=bm.kin] unless score @s bm.kin matches 1 at @s run function bm:p199/enter',
               'execute as @a[tag=!bm.kin,scores={bm.kin=1}] run scoreboard players set @s bm.kin 0']
    fn('p199/enter', ['scoreboard players set @s bm.kin 1', title('@s', 'title', T('The Underwater Kingdom', KC, bold=True)),
                      title('@s', 'subtitle', T('Home of the royal family - what is left of it', '#bfe8ff')),
                      'playsound minecraft:block.conduit.activate ambient @s ~ ~ ~ 1 0.8'])
    fast += ['execute as @e[type=minecraft:marker,tag=bm.kdoor_o] at @s as @a[distance=..1.6,gamemode=!spectator] at @s run function bm:p199/door/in',
             'execute as @e[type=minecraft:marker,tag=bm.kdoor_i] at @s as @a[distance=..1.2,gamemode=!spectator] at @s run function bm:p199/door/out']
    fn('p199/door/in', ['tp @s ~ ~ ~7 0 0', 'playsound minecraft:block.bubble_column.upwards_inside ambient @s ~ ~ ~ 1 1',
                        'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.6 0.4 0.05 30'])
    fn('p199/door/out', ['tp @s ~ ~ ~-7 180 0', 'playsound minecraft:block.bubble_column.whirlpool_inside ambient @s ~ ~ ~ 1 1.2'])
    # the ambience: fires in the windows of the ruin, bubbles at the door, the heart turning
    second += ['execute as @e[type=minecraft:marker,tag=bm.kfire] at @s if entity @a[distance=..48] run function bm:p199/amb/fire',
               'execute as @e[type=minecraft:marker,tag=bm.kdoor_o] at @s if entity @a[distance=..32] run particle minecraft:bubble ~ ~1.5 ~1 0.8 0.8 0.2 0.02 6']
    fn('p199/amb/fire', ['particle minecraft:flame ~ ~0.3 ~ 0.25 0.3 0.25 0.01 3', 'particle minecraft:large_smoke ~ ~1 ~ 0.2 0.4 0.2 0.02 2',
                         'execute store result score #r bm.rng run random value 1..6',
                         'execute if score #r bm.rng matches 1 run particle minecraft:lava ~ ~0.4 ~ 0.2 0.1 0.2 0 2',
                         'execute if score #r bm.rng matches 2 run playsound minecraft:block.fire.ambient block @a[distance=..16] ~ ~ ~ 0.6 1'])
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.kheartd] at @s if entity @a[distance=..32] run tp @s ~ ~ ~ ~6 0')

    # ---------------------------------------------------------------- (2.94) what to do here: a label over the Font and the Dome Heart
    def label(tag, lines):
        from nbt import snbt as _sn, B as _B, F as _F, Int as _I
        return 'summon minecraft:text_display ~ ~2.5 ~ ' + _sn({'Tags': [tag], 'billboard': 'center', 'see_through': _B(0), 'shadow': _B(1), 'background': _I(1073741824),
                                                             'line_width': _I(200), 'view_range': _F(0.35), 'text': lines})
    LBL = {'bm.kfont': ('bm.kfontl', [{'text': 'The Tide Font\n', 'color': KC, 'bold': True}, {'text': 'right-click', 'color': 'white'},
                                       {'text': '\n(with Queen Ava beside you: her Honours)', 'color': 'gray'}]),
           'bm.kheart': ('bm.kheartl', [{'text': 'The Dome Heart\n', 'color': KC, 'bold': True}, {'text': 'right-click: call a breach', 'color': 'white'},
                                         {'text': '\nsneak + right-click: mend the dome', 'color': 'white'}, {'text': '\n(2 Royal Pearls - free with Queen Ava)', 'color': 'gray'}])}
    for t, (lt, lines) in LBL.items():
        second.append(f'execute as @e[type=minecraft:interaction,tag={t}] at @s if entity @a[distance=..24] unless entity @e[type=minecraft:text_display,tag={lt},distance=..4] run {label(lt, lines)}')
        G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:text_display,tag={lt}]')

    fast.append('execute as @e[type=minecraft:interaction,tag=bm.kbox] if data entity @s interaction at @s run function bm:p199/click')
    fn('p199/click', ['tag @s add bm.khere', 'execute on target run function bm:p199/clicked', 'tag @s remove bm.khere', 'data remove entity @s interaction'])
    fn('p199/clicked', ['execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.kfont] run return run function bm:p199/font/ask',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.ktrib] run return run function bm:p199/trib/ask',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.kboard] run return run function bm:p199/req/ask',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.kheart] run return run function bm:p199/heart/ask',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.kplinth] run return run function bm:p199/apo/plinth',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.khere,tag=bm.kcrackbox] run return run function bm:p199/breach/patch'])

    # ---------------------------------------------------------------- who's with you (royals: #r_<k> 1 if yours is within 24)
    count = ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #rn bm.rng 0']
    for k, nm, tag, col in ROYALS:
        count += [f'scoreboard players set #r_{k} bm.rng 0',
                  f'execute as @e[tag={tag},distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #r_{k} bm.rng 1',
                  f'scoreboard players operation #rn bm.rng += #r_{k} bm.rng']
    count += ['scoreboard players operation #rq bm.rng = #r_emma bm.rng', 'scoreboard players operation #rq bm.rng += #r_ava bm.rng',
              'scoreboard players operation #rq bm.rng += #r_pearl bm.rng',
              'scoreboard players set #r_apo bm.rng 0', f'execute as @e[tag={APO},distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set #r_apo bm.rng 1']
    fn('p199/who', count)
    pearls = lambda n: give('royal_pearl', n)
    line = lambda who, col, txt: tellraw('@a[distance=..24]', [T(who + ': ', col, bold=True), T(txt, 'white')])
    kingdom_says = lambda txt: tellraw('@a[distance=..24]', P + [T(txt, KC)])

    # ---------------------------------------------------------------- the Tide Font: homecomings, the full court, the festival, audiences
    font = ['function bm:p199/who']
    font += [f'execute if score #rn bm.rng matches 0 run return run function bm:p199/font/empty']
    for k, nm, tag, col in ROYALS:
        font.append(f'execute if score #r_{k} bm.rng matches 1 unless entity @s[tag=bm.kh_{k}] run function bm:p199/home/{k}')
    font += ['execute if score #rq bm.rng matches 3 unless entity @s[tag=bm.kh_court] run function bm:p199/court/first',
             f'execute if score #rq bm.rng matches 3 as {core} unless score @s bm.kfest = #day bm.bm at @s run function bm:p199/fest/go',
             'execute unless score @s bm.kaud = #day bm.bm run function bm:p199/font/audience',
             'execute if score #rq bm.rng matches ..2 run function bm:p199/font/missing']
    fn('p199/font/ask', font)
    names = []
    for j, (k, nm, tag, col) in enumerate(ROYALS):
        fn(f'p199/font/w_{k}', [f'execute if score #r_{k} bm.rng matches 1 run return run ' + tellraw('@s', [T('  ✔ ', 'green'), T(nm, col)]),
                                tellraw('@s', [T('  ✘ ', 'dark_gray'), T(nm, 'gray'), T(' (not with you)', 'dark_gray')])])
        names.append(f'function bm:p199/font/w_{k}')
    fn('p199/font/empty', ['playsound minecraft:block.conduit.ambient block @s ~ ~ ~ 1 0.7',
                           tellraw('@s', P + [T('The Tide Font ', KC, bold=True), T('lies still. It stirs for the royal family - bring them home:', 'gray')])] + names)
    fn('p199/font/missing', [tellraw('@s', [T('The Font ripples. The royal family together - Emma, Queen Ava and Queen Pearl - would wake it fully:', 'gray')])] + names[:3])
    aud = ['scoreboard players operation @s bm.kaud = #day bm.bm', 'scoreboard players operation #n bm.rng = #rn bm.rng']
    aud += [f'execute if score #rn bm.rng matches {n} run {pearls(n)}' for n in range(1, 5)]
    aud += [say('A royal audience: the crown thanks you (Royal Pearls).', KC), 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6']
    fn('p199/font/audience', aud)
    # each royal's homecoming (once each, for each player)
    HOME = {
        'emma': (['Home! It\'s... smaller than I remember. And so much more broken.',
                  'That was my window - up there, the one that\'s still burning. ...Let\'s not talk about it.',
                  'Here. I hid this under the fountain when I was little. It calls the tide. Take it - I\'m too old for it now.'], 'tidecaller_shell'),
        'ava': (['My halls. My people\'s halls.', 'I fell in this very room. ...It is strange, to stand here again.',
                 'Take this, from my window. Sea glass keeps the sea kind to whoever wears it.'], 'sea_glass_locket'),
        'pearl': (['I held this kingdom together for my niece, for years, with my bare hands.',
                   'You are a guest of the crown. Here - my seal. Anyone who sees it will give you their best price.'], 'regent_seal'),
        'bones': (['*Bones circles the fountain three times, splashing everyone, and spits something at your feet.*',
                   '*It\'s a tooth. One of his. He looks very proud.*'], 'shark_tooth_charm'),
    }
    for k, nm, tag, col in ROYALS:
        lines, reward = HOME[k]
        out = [f'tag @s add bm.kh_{k}', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1.2',
               f'particle minecraft:dust{{color:[0.5,0.85,1.0],scale:1.4}} ~ ~1.5 ~ 1.2 1.0 1.2 0 60', 'particle minecraft:bubble_pop ~ ~1 ~ 1 1 1 0.1 60',
               tellraw('@a[distance=..24]', P + [T('HOMECOMING: ', KC, bold=True), T(nm, col, bold=True), T(' is home.', KC)])]
        out += [line(nm if k != 'bones' else '', col, l) if k != 'bones' else tellraw('@a[distance=..24]', [T(l, col, italic=True)]) for l in lines]
        out += [give(reward), pearls(4), tellraw('@s', [T('  + ', 'gray'), T(ITEMS[reward]['name'], col), T(' and 4 Royal Pearls', PEARL_C)])]
        fn(f'p199/home/{k}', out)

    # the full court (once each): the castle is restored, the Crown of the Deep
    fn('p199/court/first', ['tag @s add bm.kh_court', 'scoreboard players add @s bm.kfav 3', 'function bm:p199/rank/check',
                            tellraw('@a[distance=..32]', P + [T('THE FULL COURT', GOLD, bold=True), T(' - the royal family of the Underwater Kingdom, together again.', KC)]),
                            line('Queen Ava', '#6ad8e8', 'All of us. Under one roof. I never thought I would see it.'),
                            line('Queen Pearl', '#5ae0d8', 'Then let the flags fly again. Light the lamps! Put out those fires!'),
                            line('Emma', '#ff8ad8', 'And YOU - you brought us here. Kneel. ...No, wait, that\'s the wrong way round.'),
                            'execute if score #r_bones bm.rng matches 1 run ' + tellraw('@a[distance=..24]', [T('*Bones does a lap of the throne room.*', '#a8b4bc', italic=True)]),
                            give('crown_of_the_deep'), pearls(12),
                            tellraw('@s', [T('  + ', 'gray'), T('Crown of the Deep', GOLD, bold=True), T(' and 12 Royal Pearls', PEARL_C)]),
                            'playsound minecraft:ui.toast.challenge_complete player @a[distance=..32] ~ ~ ~ 1 0.9',
                            f'execute as {core} unless score @s bm.kgst matches 1 at @s run function bm:p199/court/restore'])
    fn('p199/court/restore', ['scoreboard players set @s bm.kgst 1',
                              f'place template bm:p199_kingdom_restored ~{K.CASTLE_BOX[0] - 35} ~-2 ~{K.CASTLE_BOX[2] - 41}',
                              'kill @e[type=minecraft:marker,tag=bm.kfire,distance=..70]',
                              'execute if entity @s[tag=bm.kseal_open] run function bm:p199/apo/open_blocks',
                              'particle minecraft:end_rod ~ ~6 ~ 12 6 12 0.02 300', 'particle minecraft:bubble_pop ~ ~4 ~ 14 6 14 0.1 300',
                              'playsound minecraft:block.beacon.activate block @a[distance=..64] ~ ~ ~ 1 0.7',
                              'playsound minecraft:block.conduit.activate block @a[distance=..64] ~ ~ ~ 1 1.2',
                              title('@a[distance=..64]', 'title', T('Restored', GOLD, bold=True)),
                              title('@a[distance=..64]', 'subtitle', T('The fires are out. The towers stand. The flags fly.', KC))])
    # the Tide Festival: the full court at the Font, once a day (as the castle's core marker)
    fn('p199/fest/go', ['scoreboard players operation @s bm.kfest = #day bm.bm',
                        'execute at @s as @a[distance=..40,gamemode=!spectator] at @s run function bm:p199/fest/guest',
                        'execute at @s run particle minecraft:firework ~ ~8 ~ 10 5 10 0.15 300',
                        'execute at @s run particle minecraft:dust{color:[1.0,0.4,0.9],scale:2.0} ~ ~6 ~ 12 6 12 0 200',
                        'execute at @s run particle minecraft:dust{color:[0.35,0.78,1.0],scale:2.0} ~ ~6 ~ 12 6 12 0 200',
                        'execute at @s run particle minecraft:note ~ ~3 ~ 6 2 6 1 40'] +
       [f'execute at @s run playsound minecraft:block.note_block.{ins} record @a[distance=..48] ~ ~ ~ 1 {p}' for ins, p in
        (('harp', 1.0), ('bell', 1.26), ('chime', 1.5), ('flute', 1.19), ('harp', 2.0))] +
       [f'execute at @s run playsound minecraft:entity.firework_rocket.twinkle_far ambient @a[distance=..48] ~ ~ ~ 1 1.2'])
    fn('p199/fest/guest', [title('@s', 'title', T('The Tide Festival', '#ff8ad8', bold=True)), title('@s', 'subtitle', T('The whole court is home - the kingdom celebrates!', KC)),
                           pearls(3), 'scoreboard players add @s bm.kfav 1', 'function bm:p199/rank/check',
                           'execute store result score #r bm.rng run random value 1..10', 'execute if score #r bm.rng matches 1 run ' + give('heartstone'),
                           'execute if score #r bm.rng matches 1 run ' + tellraw('@s', [T('  + a Heartstone, from the festival\'s lucky dip!', 'red')])])

    # ---------------------------------------------------------------- Apophiss: the carved stone opens for him; the penance on the plinth
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.kingdom,tag=!bm.kseal_open] at @s if entity @e[tag={APO},distance=..18] run function bm:p199/apo/open')
    fn('p199/apo/open', ['tag @s add bm.kseal_open', 'function bm:p199/apo/open_blocks',
                         f'execute positioned {rel(35, K.P + 1, 51)} run particle minecraft:large_smoke ~ ~ ~ 1 1 0.4 0.02 60',
                         f'execute positioned {rel(35, K.P + 1, 51)} run particle minecraft:dust{{color:[0.23,1.0,0.6],scale:1.6}} ~ ~ ~ 1.2 1.2 0.6 0 60',
                         'playsound minecraft:block.grindstone.use block @a[distance=..40] ~ ~ ~ 1 0.5',
                         'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..40] ~ ~ ~ 0.8 0.6',
                         tellraw('@a[distance=..40]', P + [T('The carved serpent behind the thrones hears its old master\'s hiss... and the stone grinds open.', '#3aff9a', italic=True)])])
    fn('p199/apo/open_blocks', [f'setblock {rel(x, y, z)} minecraft:air' for (x, y, z) in K.SEAL] +
       [f'setblock {rel(x, y, K.KEEP[1] + 6)} minecraft:air' for x in (34, 35, 36) for y in (K.P, K.P + 1, K.P + 2)])
    fn('p199/apo/plinth', ['function bm:p199/who',
                           'execute if score #r_apo bm.rng matches 0 run return run ' + say('A stone serpent coils on the plinth. Its eyes are dull - it waits for someone.', '#3aff9a'),
                           'execute unless entity @s[tag=bm.kh_apo] run function bm:p199/apo/penance',
                           'execute if score #r_ava bm.rng matches 1 unless entity @s[tag=bm.kh_pardon] run function bm:p199/apo/pardon',
                           'execute if entity @s[tag=bm.kh_apo] if entity @s[tag=bm.kh_pardon] run ' + say('The stone serpent\'s eyes glow softly. Nothing more is owed here.', '#3aff9a')])
    fn('p199/apo/penance', ['tag @s add bm.kh_apo', 'particle minecraft:soul_fire_flame ~ ~1.5 ~ 0.5 0.8 0.5 0.03 60',
                            'playsound minecraft:entity.wither.ambient hostile @a[distance=..24] ~ ~ ~ 0.5 1.6',
                            line('Apophiss', '#3aff9a', '...I took their queen. Long ago. Before you.'),
                            line('Apophiss', '#3aff9a', 'I sealed this here, after. The one weapon I swore I would never lift against the sea.'),
                            line('Apophiss', '#3aff9a', 'Take it. Let it be lifted FOR the sea, for once.'),
                            give('tide_breaker'), tellraw('@s', [T('  + ', 'gray'), T('Tide-Breaker', '#3aff9a', bold=True), T(' - a hidden treasure of the kingdom.', 'gray')]),
                            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 0.7'])
    fn('p199/apo/pardon', ['tag @s add bm.kh_pardon', 'particle minecraft:end_rod ~ ~2 ~ 1 1 1 0.05 80',
                           line('Queen Ava', '#6ad8e8', 'Serpent.'),
                           line('Apophiss', '#3aff9a', '...Majesty.'),
                           line('Queen Ava', '#6ad8e8', 'I have had a long time to be angry with you. I am tired of it. I forgive you.'),
                           tellraw('@a[distance=..24]', [T('*Apophiss bows his head very low, and says nothing at all.*', '#3aff9a', italic=True)]),
                           give('heartstone', 2), pearls(16), 'scoreboard players add @s bm.kfav 5', 'function bm:p199/rank/check',
                           tellraw('@s', [T('  + ', 'gray'), T('2 Heartstones', 'red'), T(', 16 Royal Pearls and the court\'s deep favour', PEARL_C)])])

    # ---------------------------------------------------------------- the Royal Treasury: a tribute a day
    trib = ['execute if score @s bm.ktrib = #day bm.bm run return run ' + say('The treasury has paid you today. Come back tomorrow.', KC),
            'scoreboard players operation @s bm.ktrib = #day bm.bm', 'function bm:p199/who',
            'scoreboard players set #n bm.rng 2', 'scoreboard players operation #n bm.rng += #rn bm.rng',
            f'execute as {core} if score @s bm.kgst matches 1 run scoreboard players add #n bm.rng 1',
            'execute if score @s bm.krank matches 3.. run scoreboard players add #n bm.rng 1']
    trib += [f'execute if score #n bm.rng matches {n} run {pearls(n)}' for n in range(2, 9)]
    trib += ['loot give @s loot bm:p199/tribute', 'playsound minecraft:block.barrel.open block @s ~ ~ ~ 1 1',
             'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 1.2',
             tellraw('@s', P + [T('The Royal Treasury pays its tribute: ', KC), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': PEARL_C},
                                T(' Royal Pearls and a gift. ', PEARL_C), T('(+1 for each royal with you; +1 once the castle is restored.)', 'dark_gray')])]
    fn('p199/trib/ask', trib)

    # ---------------------------------------------------------------- the Request Stand: one ask a day; favour and ranks
    req = ['scoreboard players operation #q bm.rng = #day bm.bm', f'scoreboard players operation #q bm.rng %= #{len(REQUESTS)} bm.rng']
    req += [f'execute if score #q bm.rng matches {i} run return run function bm:p199/req/r{i}' for i in range(len(REQUESTS))]
    fn('p199/req/ask', req)
    for i, (iid, n, pay, what) in enumerate(REQUESTS):
        fn(f'p199/req/r{i}', ['execute if score @s bm.kreq = #day bm.bm run return run ' + say('The steward has what he needed from you today. Thank you!', KC),
                              # (plain ones only: the Tidecaller Shell is a nautilus shell too, and the pack's fish are cod)
                              f'execute store result score #c bm.rng run clear @s minecraft:{iid}[!minecraft:custom_data] 0',
                              f'execute unless score #c bm.rng matches {n}.. run return run ' +
                              tellraw('@s', P + [T('Today\'s royal request: ', KC, bold=True), T(f'{n} {iid.replace("_", " ")}', 'white'), T(f' - {what}. ', 'gray'),
                                                 T(f'Bring them here (pays {pay} Royal Pearls and favour). ', PEARL_C), T('Your favour: ', 'gray'),
                                                 {'score': {'name': '@s', 'objective': 'bm.kfav'}, 'color': GOLD}]),
                              f'clear @s minecraft:{iid}[!minecraft:custom_data] {n}', 'scoreboard players operation @s bm.kreq = #day bm.bm', pearls(pay),
                              'scoreboard players add @s bm.kfav 1', 'function bm:p199/rank/check',
                              'playsound minecraft:entity.villager.yes neutral @s ~ ~ ~ 1 1.3',
                              tellraw('@s', P + [T('Request fulfilled! ', KC, bold=True), T(f'+{pay} Royal Pearls, +1 favour.', PEARL_C)])])
    rk = []
    for j, (need, nm, col) in enumerate(RANKS, 1):
        rk.append(f'execute if score @s bm.kfav matches {need}.. unless score @s bm.krank matches {j}.. run function bm:p199/rank/r{j}')
    fn('p199/rank/check', ['execute unless score @s bm.krank matches 0.. run scoreboard players set @s bm.krank 0'] + rk)
    gifts = {1: [give('heartstone'), pearls(6)], 2: ['give @s minecraft:heart_of_the_sea 1', 'give @s minecraft:conduit 1', pearls(8)],
             3: [pearls(16)]}
    gift_txt = {1: 'a Heartstone and 6 Royal Pearls', 2: 'a Heart of the Sea, a Conduit and 8 Royal Pearls',
                3: 'the Royal Charter (+1 pearl in every tribute, for good) and 16 Royal Pearls'}
    for j, (need, nm, col) in enumerate(RANKS, 1):
        fn(f'p199/rank/r{j}', [f'scoreboard players set @s bm.krank {j}'] + gifts[j] +
           [title('@s', 'title', T(nm, col, bold=True)), title('@s', 'subtitle', T('The Underwater Kingdom honours you', KC)),
            tellraw('@s', P + [T('RANK: ', KC, bold=True), T(nm, col, bold=True), T(f' - the crown gives you {gift_txt[j]}.', 'gray')]),
            'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.3'])

    # ---------------------------------------------------------------- the Royal Steward's shop (rewritten each day: the daily special)
    base = [(('royal_pearl', 1), ('token', 2)), (('royal_pearl', 3), ('nautilus_shell', 1)), (('royal_pearl', 10), ('heart_of_the_sea', 1)),
            (('royal_pearl', 14), ('conduit', 1)), (('royal_pearl', 16), ('trident', 1)), (('royal_pearl', 2), ('sea_lantern', 8)),
            (('royal_pearl', 1), ('prismarine_shard', 16)), (('royal_pearl', 4), ('sponge', 4)), (('royal_pearl', 24), ('heartstone', 1)),
            (('royal_pearl', 12), ('tidecaller_shell', 1)), (('royal_pearl', 6), ('sealed_map_db_shark', 1))]   # (2.94: the Sealed Royal Chart moved to Vesper - redundant here, you're already in the castle)
    import phase202 as R202
    base_o = [G.offer(b, s) for b, s in base] + R202.steward_offers(G.offer)      # (2.92: the armoury - phase202)
    for d, sp in enumerate(SPECIALS):
        fn(f'p199/shop/d{d}', [f'data modify entity @s Offers.Recipes set value {snbt(base_o + [G.offer(*sp)])}'])
    fn('p199/shop/refresh', ['scoreboard players operation #d bm.rng = #day bm.bm', 'scoreboard players operation #d bm.rng %= #7 bm.rng'] +
       [f'execute if score #d bm.rng matches {d} as @e[type=minecraft:wandering_trader,tag=bm.kstew,distance=..70] run function bm:p199/shop/d{d}' for d in range(7)] +
       ['scoreboard players operation @s bm.kday = #day bm.bm'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom] unless score @s bm.kday = #day bm.bm at @s run function bm:p199/shop/refresh')

    # ---------------------------------------------------------------- dome breaches
    # (2.93b: never of their own accord - someone calls the Tide Raiders at the Dome Heart; then the dome rests 10 minutes)
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom,scores={bm.kbr=1..}] at @s run function bm:p199/breach/tick')
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom,scores={bm.kbcd=1..}] run scoreboard players remove @s bm.kbcd 1')
    second.append('execute as @a[scores={bm.kbask=1..}] run scoreboard players remove @s bm.kbask 1')
    raider = {'Tags': ['bm.kraider'], 'CustomName': T('Tide Raider', '#3a8a8a'), 'PersistenceRequired': B(0),
              'equipment': {'mainhand': {'id': 'minecraft:trident', 'count': Int(1)}}, 'drop_chances': {'mainhand': F(0.05)},
              'DeathLootTable': 'bm:p202/raider'}         # (2.92: a Tide Scale each - phase202)
    fn('p199/breach/start', [f'scoreboard players set @s bm.kbr {BREACH_SECS}', 'scoreboard players set @s bm.kburst 0', f'scoreboard players set @s bm.kbcd {BREACH_REST}',
                             f'tag @e[type=minecraft:marker,tag=bm.kcrack_spot,distance=..70,sort=random,limit={CRACKS}] add bm.kcrack',
                             'execute as @e[type=minecraft:marker,tag=bm.kcrack,distance=..70] at @s run function bm:p199/breach/crack',
                             'playsound minecraft:block.glass.break block @a[distance=..64] ~ ~ ~ 1 0.5',
                             'playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..64] ~ ~ ~ 0.6 1.2',
                             'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'title', T('DOME BREACH!', '#ff5a5a', bold=True)),
                             'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'subtitle', T(f'Seal the {CRACKS} cracks before the sea gets in! (right-click them)', KC))])
    fn('p199/breach/crack', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.kbox","bm.kcrackbox"],width:1.4f,height:2.6f,response:1b}',
                             f'summon minecraft:drowned ~ ~ ~ {snbt(raider)}', f'summon minecraft:drowned ~ ~ ~ {snbt(raider)}',
                             'particle minecraft:falling_water ~ ~2 ~ 0.4 0.6 0.4 0 30'])
    fn('p199/breach/tick', ['scoreboard players remove @s bm.kbr 1',
                            'execute as @e[type=minecraft:marker,tag=bm.kcrack,distance=..70] at @s run function bm:p199/breach/drip',
                            'execute store result score #n bm.rng if entity @e[type=minecraft:marker,tag=bm.kcrack,distance=..70]',
                            'execute if score #n bm.rng matches 0 run return run function bm:p199/breach/won',
                            'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'actionbar', [T('Dome breach: ', '#ff5a5a', bold=True),
                                                                                                      {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': 'white'},
                                                                                                      T(' cracks left - ', KC), {'score': {'name': '@s', 'objective': 'bm.kbr'}, 'color': 'white'},
                                                                                                      T(' s', KC)]),
                            'execute if score @s bm.kbr matches 0 run function bm:p199/breach/lost'])
    fn('p199/breach/drip', ['particle minecraft:falling_water ~ ~2.2 ~ 0.3 0.4 0.3 0 12', 'particle minecraft:bubble_pop ~ ~1.5 ~ 0.3 0.6 0.3 0.05 6',
                            'execute store result score #r bm.rng run random value 1..4',
                            'execute if score #r bm.rng matches 1 run playsound minecraft:block.glass.hit block @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn('p199/breach/patch', ['execute as @e[type=minecraft:interaction,tag=bm.khere] at @s run function bm:p199/breach/sealed',
                             pearls(1), say('You seal the crack with a slap of mortar and a prayer. (+1 Royal Pearl)', KC)])
    fn('p199/breach/sealed', ['tag @e[type=minecraft:marker,tag=bm.kcrack,distance=..1.5] remove bm.kcrack', 'kill @s',
                              'particle minecraft:block{block_state:"minecraft:glass"} ~ ~1.5 ~ 0.4 0.6 0.4 0 20',
                              'playsound minecraft:block.glass.place block @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn('p199/breach/won', ['scoreboard players set @s bm.kbr 0', 'kill @e[type=minecraft:drowned,tag=bm.kraider,distance=..70]',
                           'execute positioned ~ ~-4 ~-6 as @a[distance=..34,gamemode=!spectator] at @s run function bm:p199/breach/hero',
                           'playsound minecraft:block.beacon.power_select block @a[distance=..64] ~ ~ ~ 1 1.2'])
    fn('p199/breach/hero', [pearls(3), 'scoreboard players add @s bm.kfav 1', 'function bm:p199/rank/check',
                            title('@s', 'title', T('The dome holds!', KC, bold=True)), title('@s', 'subtitle', T('+3 Royal Pearls, +1 favour', PEARL_C))])
    fn('p199/breach/lost', ['execute as @e[type=minecraft:marker,tag=bm.kcrack,distance=..70] at @s run function bm:p199/breach/burst',
                            'kill @e[type=minecraft:interaction,tag=bm.kcrackbox,distance=..70]',
                            f'execute if score @s bm.kburst matches {SHATTER_AT}.. run return run function bm:p199/dome/shatter',
                            'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'title', T('The sea gets in!', '#ff5a5a', bold=True)),
                            'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'subtitle', T('Mend the leaks at the Dome Heart (sneak + right-click it)', KC))])
    fn('p199/breach/burst', ['tag @s remove bm.kcrack', 'scoreboard players add @e[type=minecraft:marker,tag=bm.kingdom,distance=..70,sort=nearest,limit=1] bm.kburst 1',
                             'fill ~-1 ~ ~-1 ~1 ~2 ~1 minecraft:water replace minecraft:glass',
                             # (2.94: and says plainly how to mend it)
                             tellraw('@a[distance=..60]', P + [T('The sea is getting in! ', '#ff5a5a', bold=True),
                                                               T('Mend the dome at the ', 'gray'), T('Dome Heart', KC, bold=True),
                                                               T(' (the floating Heart of the Sea in the keep): ', 'gray'), T('sneak + right-click it', 'white', bold=True),
                                                               T(' - 2 Royal Pearls, or free with Queen Ava beside you.', 'gray')]),
                             'particle minecraft:block{block_state:"minecraft:glass"} ~ ~1.5 ~ 0.6 0.8 0.6 0 40',
                             'playsound minecraft:block.glass.break block @a[distance=..32] ~ ~ ~ 1 0.7'])

    # ---------------------------------------------------------------- the dome: mend (glass back, water out) and shatter (the sea in)
    cols = K.shell_columns()
    mend, flood, dry = [], [], []

    def runs(ys):
        out, s = [], None
        for y in sorted(ys):
            if s is None or y != prev + 1:
                if s is not None: out.append((s, prev))
                s = y
            prev = y
        if s is not None: out.append((s, prev))
        return out
    # (columns side by side in x with the same run of y share one fill)
    for kind in ('shell', 'inside'):
        rows = {}
        for (x, z), (ys, ins) in cols.items():
            for r in runs(ys if kind == 'shell' else ins):
                rows.setdefault((z, r), []).append(x)
        for (z, (y0, y1)), xs in sorted(rows.items()):
            xs.sort()
            start = prev = xs[0]
            for x in xs[1:] + [None]:
                if x is not None and x == prev + 1:
                    prev = x; continue
                a, b = rel(start, y0, z), rel(prev, y1, z)
                if kind == 'shell':
                    mend.append(f'fill {a} {b} minecraft:glass replace #bm:p199_gap')
                    flood.append(f'fill {a} {b} minecraft:water replace #bm:p199_glass')
                else:
                    dry.append(f'fill {a} {b} minecraft:air replace #bm:p199_wet')
                    flood.append(f'fill {a} {b} minecraft:water replace minecraft:air')
                if x is not None: start = prev = x
    wjson('bm/tags/block/p199_gap.json', {'values': ['minecraft:water', 'minecraft:air', 'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass',
                                                     'minecraft:tall_seagrass', 'minecraft:bubble_column']})
    wjson('bm/tags/block/p199_glass.json', {'values': ['minecraft:glass', 'minecraft:light_blue_stained_glass']})
    fx, fz = K.FOUNT
    fountain = [f'setblock {rel(x, K.P, z)} minecraft:water' for x in range(fx - 3, fx + 4) for z in range(fz - 3, fz + 4)
                if math.hypot(x - fx, z - fz) <= 1.6 and (x, z) != (fx, fz)]
    door = [f'setblock {rel(x, y, K.DOOR_Z)} minecraft:light_blue_stained_glass' for x in (34, 35, 36) for y in range(K.FY + 1, K.FY + 4)]
    # (2.94: the drying is its own pass - kelp, seagrass and bubble columns that grew in the flood go too - run again a few
    #  seconds later for water that was still flowing; the fountain's own water put back after)
    wjson('bm/tags/block/p199_wet.json', {'values': ['minecraft:water', 'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:seagrass', 'minecraft:tall_seagrass',
                                                     'minecraft:bubble_column']})
    fn('p199/dome/dry', dry + fountain)
    fn('p199/dome/mend_blocks', mend + door + ['function bm:p199/dome/dry'])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kdry dummy', 'scoreboard objectives add bm.kleak dummy']
    G.OBJECTIVES += ['bm.kdry', 'bm.kleak']
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom,scores={bm.kdry=1..}] at @s run function bm:p199/dome/drying')
    fn('p199/dome/flood_blocks', flood)
    loaded = ' '.join(f'if loaded ~{x} ~ ~{z}' for x in (-36, 36) for z in (-42, 30))
    fn('p199/dome/mend', [f'execute unless loaded ~-36 ~ ~-42 run return run ' + say('The dome is too far to reach all of it - come closer.', KC),
                          f'execute {loaded} run function bm:p199/dome/mend_blocks', 'scoreboard players set @s bm.kdome 0', 'scoreboard players set @s bm.kburst 0',
                          'scoreboard players set @s bm.kdry 6',
                          'kill @e[type=minecraft:drowned,tag=bm.kraider,distance=..70]',
                          'playsound minecraft:block.conduit.activate block @a[distance=..64] ~ ~ ~ 1 0.8',
                          'execute positioned ~ ~-4 ~-6 run particle minecraft:bubble_pop ~ ~8 ~ 14 8 14 0.1 400',
                          'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..40]', 'title', T('The dome is whole', KC, bold=True))])
    fn('p199/dome/drying', ['execute if score @s bm.kdome matches 1 run return run scoreboard players set @s bm.kdry 0', 'scoreboard players remove @s bm.kdry 1', f'execute if score @s bm.kdry matches 3 {loaded} run function bm:p199/dome/dry',
                            f'execute if score @s bm.kdry matches 0 {loaded} run function bm:p199/dome/dry'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.kingdom,scores={bm.kburst=1..,bm.kdome=0}] at @s run function bm:p199/dome/leaking')
    fn('p199/dome/leaking', ['scoreboard players add @s bm.kleak 1', 'execute as @e[type=minecraft:item_display,tag=bm.kheartd,distance=..60] at @s run particle minecraft:dripping_water ~ ~0.6 ~ 0.3 0.3 0.3 0 6',
                             'execute unless score @s bm.kleak matches 20.. run return 0', 'scoreboard players set @s bm.kleak 0',
                             'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..34]', 'actionbar', [T('The dome is leaking - ', '#ff8a8a'), T('sneak + right-click the Dome Heart', 'white', bold=True),
                                                                                                         T(' to mend it (2 Royal Pearls).', '#ff8a8a')])])
    fn('p199/dome/shatter', ['scoreboard players set @s bm.kdome 1', 'scoreboard players set @s bm.kbr 0', 'scoreboard players set @s bm.kdry 0',
                             f'execute {loaded} run function bm:p199/dome/flood_blocks',
                             'playsound minecraft:block.glass.break block @a[distance=..64] ~ ~ ~ 2 0.4',
                             'playsound minecraft:entity.generic.explode block @a[distance=..64] ~ ~ ~ 1 0.5',
                             'execute positioned ~ ~-4 ~-6 run effect give @a[distance=..40] minecraft:water_breathing 60 0',
                             'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..40]', 'title', T('THE DOME SHATTERS', '#ff5a5a', bold=True)),
                             'execute positioned ~ ~-4 ~-6 run ' + title('@a[distance=..40]', 'subtitle', T('The Dome Heart can raise it: a Heart of the Sea, or Queen Ava', KC))])

    # the Dome Heart: raise a shattered dome (a Heart of the Sea, or Queen Ava); sneak + use: mend leaks (2 pearls; free with Ava)
    fn('p199/heart/ask', ['function bm:p199/who', f'execute store result score #ks bm.rng run scoreboard players get {core} bm.kdome',
                          'execute if score #ks bm.rng matches 1 run return run function bm:p199/heart/shattered',
                          'execute unless predicate bm:p20/sneaking run return run function bm:p199/heart/call',
                          'execute if score #r_ava bm.rng matches 1 run return run function bm:p199/heart/mend_free',
                          f'execute store result score #c bm.rng run clear @s {holds("royal_pearl")} 0',
                          'execute unless score #c bm.rng matches 2.. run return run ' + say('Mending the dome takes 2 Royal Pearls.', KC),
                          f'clear @s {holds("royal_pearl")} 2', f'execute as {core} at @s run function bm:p199/dome/mend'])
    fn('p199/heart/call', [f'execute if score {core} bm.kbr matches 1.. run return run ' + say('The dome is already breached - seal the cracks!', '#ff5a5a'),
                           f'execute store result score #s bm.rng run scoreboard players get {core} bm.kbcd',
                           'execute if score #s bm.rng matches 1.. run return run title @s actionbar [{"text":"The Tide Raiders are regrouping... ","color":"%s"},{"score":{"name":"#s","objective":"bm.rng"},"color":"white"},{"text":" s","color":"gray"}]' % KC,
                           'execute unless score @s bm.kbask matches 1.. run return run function bm:p199/heart/offer',
                           'scoreboard players reset @s bm.kbask', f'execute as {core} at @s run function bm:p199/breach/start'])
    fn('p199/heart/offer', ['scoreboard players set @s bm.kbask 5',
                            tellraw('@s', P + [T('The Dome Heart ', KC, bold=True), T('holds the sea back. ', 'gray'),
                                               T('Right-click it again to call the Tide Raiders against the dome', '#ff8a8a'),
                                               T(' - a breach to beat back (Royal Pearls, favour, Tide Scales). ', 'gray'),
                                               T('Sneak + right-click to mend leaks (2 Royal Pearls; free with Queen Ava beside you).', 'dark_gray')])])
    fn('p199/heart/mend_free', [line('Queen Ava', '#6ad8e8', 'Leave it to me.'), f'execute as {core} at @s run function bm:p199/dome/mend'])
    fn('p199/heart/shattered', ['execute if score #r_ava bm.rng matches 1 run return run function bm:p199/heart/raise_ava',
                                'execute unless items entity @s weapon.mainhand minecraft:heart_of_the_sea run return run ' +
                                say('The dome lies shattered. Hold a Heart of the Sea up to the Dome Heart - or bring Queen Ava.', KC),
                                'item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}', 'function bm:p199/heart/raise'])
    fn('p199/heart/raise_ava', [line('Queen Ava', '#6ad8e8', 'The sea has always listened to me. Watch.'), 'function bm:p199/heart/raise'])
    fn('p199/heart/raise', [f'execute as {core} at @s run function bm:p199/dome/mend',
                            tellraw('@a[distance=..40]', P + [T('The Dome Heart flares - the glass knits itself back across the sky, and the sea is pushed out.', KC)])])

    # ---------------------------------------------------------------- the charms
    fn('p199/shell/use', ['effect give @s minecraft:water_breathing 180 0', 'effect give @s minecraft:dolphins_grace 180 0', 'effect give @s minecraft:conduit_power 180 0',
                          'playsound minecraft:block.conduit.activate player @s ~ ~ ~ 1 1.4', 'particle minecraft:bubble_pop ~ ~1 ~ 0.5 0.8 0.5 0.1 30',
                          say('The shell sings - the tide answers.', '#ff8ad8')])
    carried = lambda iid: [f'execute as @a if items entity @s container.* {holds(iid)} at @s run function bm:p199/carry/{iid}',
                           f'execute as @a unless items entity @s container.* {holds(iid)} if items entity @s weapon.offhand {holds(iid)} at @s run function bm:p199/carry/{iid}']
    for iid in ('sea_glass_locket', 'regent_seal', 'shark_tooth_charm'):
        second += carried(iid)
    in_water = 'execute if block ~ ~ ~ minecraft:water'
    fn('p199/carry/sea_glass_locket', ['effect give @s minecraft:water_breathing 3 0 true', f'{in_water} run effect give @s minecraft:regeneration 3 0 true'])
    fn('p199/carry/regent_seal', ['effect give @s minecraft:hero_of_the_village 3 0 true'])
    fn('p199/carry/shark_tooth_charm', [f'{in_water} run effect give @s minecraft:strength 3 0 true', f'{in_water} run effect give @s minecraft:speed 3 1 true'])

    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second
