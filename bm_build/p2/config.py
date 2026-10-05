"""Shared Phase 2 dungeon configuration: read by the builders, the logic generator and the verifier,
so materials, radii, puzzle order and boss order can never drift apart."""

# Boss order (no skipping): conquest index 1..6. The Gilded Roost (lucky) sits outside the chain (index 0).
ORDER = ['brood', 'frost', 'tide', 'hex', 'keep', 'hollow']

D = {
    'brood': dict(
        idx=1, title="The Broodmother's Nest", boss='The Broodmother', color='#7d8f3a',
        gate='minecraft:white_wool',            # "silk curtain" gates
        secret='minecraft:cobbled_deepslate',   # secret doors hide in rough stone
        trap='minecraft:bone_block',            # hidden 2 below a trap pressure plate
        radius=44,                               # dungeon reach from its controller marker
        arena_r=16,
        puzzles=[(1, 'levers'), (2, 'seq'), (3, 'path')],
        key='key_brood', vkey='vkey_brood', bkey='bkey_brood', next_map='sealed_map_frost',
        fx=['particle minecraft:white_ash ~ ~3 ~ 14 4 14 0 10', 'particle minecraft:mycelium ~ ~1 ~ 12 2 12 0 4'],
        amb=[('minecraft:entity.spider.ambient', 0.5, 0.6), ('minecraft:block.cobweb.step', 0.8, 0.5),
             ('minecraft:entity.silverfish.ambient', 0.4, 0.5), ('minecraft:ambient.cave', 0.6, 0.7)],
    ),
    'frost': dict(
        idx=2, title='The Frostbound Spire', boss='The Frost Marksman', color='#a8d8ff',
        gate='minecraft:blue_ice', secret='minecraft:cracked_deepslate_tiles', trap='minecraft:snow_block',
        radius=40, arena_r=15,
        puzzles=[(1, 'targets'), (2, 'keypad'), (3, 'path')],
        key='key_frost', vkey='vkey_frost', bkey='bkey_frost', next_map='sealed_map_tide',
        fx=['particle minecraft:snowflake ~ ~4 ~ 12 5 12 0.01 10', 'particle minecraft:white_ash ~ ~2 ~ 10 3 10 0 4'],
        amb=[('minecraft:block.powder_snow.step', 0.8, 0.5), ('minecraft:entity.stray.ambient', 0.5, 0.7),
             ('minecraft:item.elytra.flying', 0.15, 0.5), ('minecraft:block.glass.break', 0.25, 0.4)],
    ),
    'tide': dict(
        idx=3, title='The Sunken Throne', boss='The Drowned Tyrant', color='#2fa39b',
        gate='minecraft:waxed_oxidized_copper_grate', secret='minecraft:cracked_stone_bricks',
        trap='minecraft:wet_sponge', radius=46, arena_r=16,
        puzzles=[(1, 'waves'), (2, 'simon'), (3, 'offering')],
        key='key_tide', vkey='vkey_tide', bkey='bkey_tide', next_map='sealed_map_hex',
        fx=['particle minecraft:dripping_water ~ ~5 ~ 12 2 12 0 8', 'particle minecraft:falling_water ~ ~4 ~ 10 2 10 0 3'],
        amb=[('minecraft:ambient.underwater.loop.additions.rare', 0.8, 0.8), ('minecraft:entity.drowned.ambient_water', 0.5, 0.6),
             ('minecraft:block.conduit.ambient', 0.6, 0.5), ('minecraft:entity.guardian.ambient', 0.4, 0.6)],
    ),
    'hex': dict(
        idx=4, title='The Hexbound Cathedral', boss='The Archmage', color='#9b59d0',
        gate='minecraft:purple_stained_glass', secret='minecraft:chiseled_deepslate', trap='minecraft:crying_obsidian',
        radius=44, arena_r=15,
        puzzles=[(1, 'lights'), (2, 'waves'), (3, 'seq')],
        key='key_hex', vkey='vkey_hex', bkey='bkey_hex', next_map='sealed_map_keep',
        fx=['particle minecraft:witch ~ ~3 ~ 12 4 12 0 6', 'particle minecraft:enchant ~ ~2 ~ 10 3 10 0.4 8'],
        amb=[('minecraft:entity.evoker.ambient', 0.4, 0.6), ('minecraft:block.enchantment_table.use', 0.5, 0.5),
             ('minecraft:entity.vex.ambient', 0.3, 0.6), ('minecraft:block.bell.resonate', 0.3, 0.5)],
    ),
    'keep': dict(
        idx=5, title="Wilfrey's Keep", boss='Bobbery', color='#5b3a3a',
        gate='minecraft:iron_block', secret='minecraft:cracked_polished_blackstone_bricks', trap='minecraft:magma_block',
        radius=56, arena_r=17,
        puzzles=[(1, 'levers'), (2, 'waves'), (3, 'seq')],
        key='key_keep', vkey='vkey_keep', bkey='bkey_keep', next_map=None,
        # "sparse wither particles": the wither effect swirl colour, plus soot and souls
        fx=['particle minecraft:entity_effect{color:[0.45,0.38,0.34,1.0]} ~ ~3 ~ 16 5 16 0 6',
            'particle minecraft:ash ~ ~3 ~ 16 5 16 0 10', 'particle minecraft:soul ~ ~1 ~ 14 2 14 0.01 1'],
        amb=[('minecraft:entity.wither_skeleton.ambient', 0.5, 0.6), ('minecraft:ambient.soul_sand_valley.mood', 0.7, 0.8),
             ('minecraft:block.chain.step', 0.6, 0.5), ('minecraft:entity.creaking.ambient', 0.4, 0.6)],
    ),
    'hollow': dict(
        idx=6, title='The Hollow Throne', boss='The Hollow King', color='#3d4b5c',
        gate='minecraft:reinforced_deepslate', secret='minecraft:cracked_deepslate_bricks', trap='minecraft:crying_obsidian',
        radius=100, arena_r=20,     # gates are reinforced deepslate: the Wither (phase 2) cannot break them (#wither_immune)
        puzzles=[(1, 'waves'), (2, 'reach'), (3, 'targets'), (4, 'reach'), (5, 'waves')],
        key=None, vkey='vkey_hollow', bkey='bkey_hollow', next_map=None,
        fx=['particle minecraft:entity_effect{color:[0.3,0.25,0.25,1.0]} ~ ~3 ~ 18 6 18 0 6',
            'particle minecraft:sculk_soul ~ ~1 ~ 16 3 16 0.01 2', 'particle minecraft:ash ~ ~4 ~ 18 6 18 0 10'],
        amb=[('minecraft:ambient.nether_wastes.mood', 0.8, 0.6), ('minecraft:entity.warden.heartbeat', 0.5, 0.7),
             ('minecraft:entity.wither.ambient', 0.25, 0.4), ('minecraft:block.sculk_shrieker.shriek', 0.2, 0.4)],
    ),
    'lucky': dict(
        idx=0, title='The Gilded Roost', boss='The Golden Goose', color='#ffd700',
        gate='minecraft:raw_gold_block', secret='minecraft:chiseled_quartz_block', trap='minecraft:yellow_concrete',
        radius=44, arena_r=14,
        puzzles=[(1, 'slots'), (2, 'path'), (3, 'waves')],
        key=None, vkey='vkey_lucky', bkey='bkey_lucky', next_map=None,
        fx=['particle minecraft:wax_on ~ ~3 ~ 12 4 12 0 5', 'particle minecraft:end_rod ~ ~4 ~ 12 4 12 0.005 2'],
        amb=[('minecraft:block.amethyst_block.chime', 0.6, 0.6), ('minecraft:entity.chicken.ambient', 0.4, 0.5),
             ('minecraft:block.note_block.chime', 0.3, 0.5), ('minecraft:block.bell.resonate', 0.2, 0.7)],
    ),
}

# Keypad codes and ordered sequences live with the builds (the clues are physical), but are recorded here for
# the verifier and the README spoiler appendix.
CODES = {}       # d -> {puzzle n: code string}
SEQS = {}        # d -> {puzzle n: length}
OPEN_LIGHT = 'minecraft:light[level=3,waterlogged=false]'      # "open" placeholder inside a gate frame
ADOOR_LIGHT = 'minecraft:light[level=4,waterlogged=false]'     # "open" placeholder inside an arena battle door
GATE_H = 4          # gates: 3 wide x 4 tall, centred on the marker
BIG_W, BIG_H = 2, 5  # arena battle doors: 5 wide x 5 tall (half-width 2)
