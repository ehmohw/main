"""3D block-model trophies, one per dungeon boss (2.1). Built from vanilla block textures with gen_rp.cube().
Front = model north (the trophy is turned to face whoever places it). All on a stepped plinth with a gold plaque."""

TEX = {'k': 'minecraft:block/black_wool', 'r': 'minecraft:block/red_wool', 'w': 'minecraft:block/white_wool',
       'y': 'minecraft:block/gold_block', 'o': 'minecraft:block/stripped_dark_oak_log', 's': 'minecraft:block/iron_block',
       'mc': 'minecraft:block/mossy_cobblestone', 'mo': 'minecraft:block/moss_block', 'pi': 'minecraft:block/packed_ice',
       'bi': 'minecraft:block/blue_ice', 'sn': 'minecraft:block/snow', 'bo': 'minecraft:block/bone_block_side',
       'lb': 'minecraft:block/light_blue_wool', 'sp': 'minecraft:block/spruce_planks', 'pr': 'minecraft:block/prismarine',
       'dp': 'minecraft:block/dark_prismarine', 'tc': 'minecraft:block/tube_coral_block', 'pu': 'minecraft:block/purple_wool',
       'am': 'minecraft:block/amethyst_block', 'pb': 'minecraft:block/polished_blackstone', 'bk': 'minecraft:block/black_concrete',
       'nb': 'minecraft:block/nether_bricks', 'gr': 'minecraft:block/gray_concrete', 'cy': 'minecraft:block/light_blue_concrete',
       'pd': 'minecraft:block/polished_deepslate', 'or': 'minecraft:block/orange_concrete', 'gc': 'minecraft:block/green_concrete',
       'em': 'minecraft:block/emerald_block'}


def plinth(cube, base, top):
    return [cube((2, 0, 2), (14, 1.5, 14), base), cube((3, 1.5, 3), (13, 3, 13), top),
            cube((5, 0.3, 1.9), (11, 1.2, 2), 'y')]                         # gold plaque on the front


def models(cube):
    M = {}
    # The Broodmother: a black spider, red eyes and hourglass, eight legs
    legs = []
    for z in (4.5, 6.5, 8.5, 10.5):
        legs += [cube((2.2, 6, z), (5, 6.8, z + 0.8), 'k'), cube((1.5, 3, z), (2.3, 6.8, z + 0.8), 'k'),
                 cube((11, 6, z), (13.8, 6.8, z + 0.8), 'k'), cube((13.7, 3, z), (14.5, 6.8, z + 0.8), 'k')]
    M['brood'] = plinth(cube, 'mc', 'mo') + legs + [
        cube((5, 4.5, 7.5), (11, 9.5, 13), 'k'), cube((6, 4.5, 4), (10, 8, 7.5), 'k'),
        cube((6.3, 6.3, 3.9), (7.5, 7.3, 4), 'r'), cube((8.5, 6.3, 3.9), (9.7, 7.3, 4), 'r'),
        cube((7.1, 5.2, 3.9), (7.7, 5.8, 4), 'r'), cube((8.3, 5.2, 3.9), (8.9, 5.8, 4), 'r'),
        cube((7.2, 9.5, 9), (8.8, 9.6, 11.5), 'r'), cube((6.5, 4, 3.5), (7.3, 5, 4.2), 'w'), cube((8.7, 4, 3.5), (9.5, 5, 4.2), 'w')]
    # The Frost Marksman: a stray's skull under an icy hood, longbow at its side, ice shards
    M['frost'] = plinth(cube, 'pi', 'sn') + [
        cube((5, 6, 5.5), (11, 12, 11), 'bo'), cube((6, 8.5, 5.4), (7.5, 10, 5.5), 'k'), cube((8.5, 8.5, 5.4), (10, 10, 5.5), 'k'),
        cube((7.5, 6.8, 5.4), (8.5, 7.6, 5.5), 'k'), cube((6, 3, 7), (10, 6, 10), 'bo'),
        cube((4.5, 10.5, 5), (11.5, 13, 11.5), 'lb'), cube((4.5, 5.5, 9), (11.5, 10.5, 11.8), 'lb'), cube((6, 13, 6.5), (10, 14, 10.5), 'lb'),
        cube((12.5, 3.5, 7.5), (13.3, 15, 8.3), 'sp'), cube((11.8, 3, 7.5), (12.6, 4.2, 8.3), 'sp'), cube((11.8, 14.3, 7.5), (12.6, 15.5, 8.3), 'sp'),
        cube((11.9, 4, 7.8), (12, 14.5, 8), 'w'),
        cube((3, 3, 3.5), (4.5, 6.5, 5), 'bi'), cube((3.5, 3, 10.5), (4.5, 5, 11.5), 'bi'), cube((11, 3, 3), (12.5, 4.8, 4.5), 'bi')]
    # The Drowned Tyrant: a trident through a golden crown on a coral throne-stone
    crown = [cube((5, 8, 5), (11, 10, 5.6), 'y'), cube((5, 8, 10.4), (11, 10, 11), 'y'), cube((5, 8, 5.6), (5.6, 10, 10.4), 'y'),
             cube((10.4, 8, 5.6), (11, 10, 10.4), 'y')] + \
            [cube((x, 10, 5), (x + 1, 11.3, 5.6), 'y') for x in (5, 7.5, 10)] + [cube((x, 10, 10.4), (x + 1, 11.3, 11), 'y') for x in (5, 7.5, 10)]
    M['tide'] = plinth(cube, 'dp', 'tc') + crown + [
        cube((7.5, 3, 7.5), (8.5, 13.5, 8.5), 'pr'), cube((5, 13, 7.5), (11, 14, 8.5), 'pr'),
        cube((5, 14, 7.5), (6, 16.5, 8.5), 'pr'), cube((7.5, 14, 7.5), (8.5, 17.5, 8.5), 'pr'), cube((10, 14, 7.5), (11, 16.5, 8.5), 'pr'),
        cube((7.6, 5.8, 5.4), (8.4, 6.6, 5.6), 'y')]
    # The Archmage: a tall pointed hat with a gold band, and a floating amethyst orb
    M['hex'] = plinth(cube, 'pb', 'am') + [
        cube((3, 3, 3), (13, 4, 13), 'pu'), cube((4.5, 4, 4.5), (11.5, 6.5, 11.5), 'pu'), cube((4.4, 4.2, 4.4), (11.6, 5, 11.6), 'y'),
        cube((5.5, 6.5, 5.5), (10.5, 9, 10.5), 'pu'), cube((6.5, 9, 6.5), (9.5, 11.5, 9.5), 'pu'), cube((7.2, 11.5, 7.5), (9, 13.5, 9.3), 'pu'),
        cube((7.8, 13.5, 8.2), (9.4, 14.8, 9.6), 'pu'), cube((6.6, 7.8, 5.4), (7.4, 8.6, 5.5), 'y'), cube((8.8, 9.6, 6.4), (9.4, 10.2, 6.5), 'y'),
        cube((11.3, 10, 2.8), (14, 12.7, 5.5), 'am'), cube((12, 9.2, 3.5), (13.3, 10, 4.8), 'y')]
    # Bobbery: a bandit-masked wither skull, his axe behind it, a spill of stolen gold
    M['keep'] = plinth(cube, 'nb', 'pd') + [
        cube((5, 4, 6), (11, 10, 12), 'bk'), cube((4.9, 7, 5.9), (11.1, 8.4, 6), 'r'),
        cube((6, 7.3, 5.85), (7.4, 8.1, 5.9), 'w'), cube((8.6, 7.3, 5.85), (10, 8.1, 5.9), 'w'),
        cube((6.5, 4.8, 5.9), (9.5, 5.4, 6), 'gr'), cube((10.5, 8.6, 9), (13, 9.4, 10), 'r'),
        cube((12, 3, 9.5), (13, 15, 10.5), 'o'), cube((12, 11.5, 6.5), (13, 14.5, 9.5), 's'),
        cube((3, 3, 3), (5, 3.8, 5), 'y'), cube((3.6, 3.8, 3.4), (5.2, 4.5, 5), 'y'), cube((5.5, 3, 3.2), (7, 3.7, 4.7), 'y'),
        cube((10, 3, 3), (11.5, 3.6, 4.5), 'y')]
    # The Hollow King: three wither skulls on a spine, the centre one crowned
    M['hollow'] = plinth(cube, 'pd', 'pb') + [
        cube((7, 3, 7.5), (9, 8, 9.5), 'gr'), cube((3.5, 5.5, 8), (12.5, 6.5, 9), 'gr'), cube((4.5, 4, 8), (11.5, 4.8, 9), 'gr'),
        cube((5.5, 8, 6), (10.5, 13, 11), 'bk'), cube((6.3, 10.3, 5.9), (7.7, 11.3, 6), 'cy'), cube((8.3, 10.3, 5.9), (9.7, 11.3, 6), 'cy'),
        cube((6.8, 8.6, 5.9), (9.2, 9.2, 6), 'gr'),
        cube((1.5, 6.5, 7), (5, 10, 10.5), 'bk'), cube((2.1, 8.2, 6.9), (2.9, 8.9, 7), 'cy'), cube((3.6, 8.2, 6.9), (4.4, 8.9, 7), 'cy'),
        cube((11, 6.5, 7), (14.5, 10, 10.5), 'bk'), cube((11.6, 8.2, 6.9), (12.4, 8.9, 7), 'cy'), cube((13.1, 8.2, 6.9), (13.9, 8.9, 7), 'cy'),
        cube((5.3, 13, 5.8), (10.7, 14, 11.2), 'y')] + \
        [cube((x, 14, 5.8), (x + 0.9, 15.4, 6.4), 'y') for x in (5.3, 7.55, 9.8)] + [cube((x, 14, 10.6), (x + 0.9, 15.4, 11.2), 'y') for x in (5.3, 7.55, 9.8)]
    # The Golden Goose: a gold goose with an orange beak, and its golden egg
    M['lucky'] = plinth(cube, 'gc', 'em') + [
        cube((5, 4.5, 6), (11, 8.5, 12), 'y'), cube((7, 8.5, 5), (9, 12.5, 7), 'y'), cube((6.8, 12, 4.5), (9.2, 14.2, 7), 'y'),
        cube((7.4, 12.6, 3.2), (8.6, 13.4, 4.5), 'or'), cube((6.7, 13.2, 5.2), (6.8, 13.8, 5.8), 'k'), cube((9.2, 13.2, 5.2), (9.3, 13.8, 5.8), 'k'),
        cube((4.5, 5.5, 7), (5, 8, 11.5), 'y'), cube((11, 5.5, 7), (11.5, 8, 11.5), 'y'), cube((7, 7.5, 12), (9, 9, 13.5), 'y'),
        cube((6.5, 3, 8), (7.3, 4.5, 8.8), 'or'), cube((8.7, 3, 8), (9.5, 4.5, 8.8), 'or'),
        cube((11.5, 3, 3.5), (13.5, 5.8, 5.5), 'y'), cube((11.8, 5.8, 3.8), (13.2, 6.3, 5.2), 'y')]
    return M
