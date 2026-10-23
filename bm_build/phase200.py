"""2.91: THE NETHER AND THE END, OVERHAULED (hellend.py builds the places).

THE NETHER
  THE EMBER RAT'S OUTPOST - a Black Market branch: a little nether-brick fort with an Ember Rat who never packs up (his field
    stock and more: Hellstars, Heartstones, the Smouldering Idol), a chest, a lava font and a charged respawn anchor. In an
    Eruption it's a shelter: nothing falls on you inside, and its walls lend Fire Resistance.
  THE COLOSSUS'S FORGE - a lava temple: blaze cages in the gate hall, a bridge over the moat, the Great Anvil in the Forge Heart.
    Sneak + right-click the anvil with a Smouldering Idol (or 32 Ember Scales) and the Magma Colossus wakes in the hall. Beat it
    there and the forge is lit for good: everyone who fought gets Hellstars, Ember Scales and a Heartstone. A lit forge TEMPERS:
    right-click it holding anything that wears out, with 2 Hellstars on you - it's unbreakable from then on. (Wake him again
    whenever you like, for the spoils.)
  THE ERUPTION - the Nether's own event (there's no night down there to call it one): every so often, for four minutes, the
    Nether boils - ash and rumbling, lava bombs crashing down round you (watch for the rings), magma cubes spilling out, and
    HELLSTARS falling ten times as often. Ride it out and you're paid in Ember Scales, a Hellstar, maybe a Heartstone.
THE END (out past the dragon's island)
  THE VOID RAT'S OUTPOST - a stall on its own floating island: a Void Rat who stays (his stock and more: Voidstars, Heartstones,
    the Starless Eye), an ender chest, a chest. Its rift anchor catches anyone who falls into the void within reach of it.
  THE VOIDWALKER'S OBSERVATORY - a shattered observatory adrift in the void. Take a Starless Eye from its pedestal (once each);
    later, sneak + right-click the pedestal with 3 Voidstars and the Voidwalker comes to it - beat him there for Voidstars, Void
    Shards and a Heartstone. Its telescope (once a day): stargazing brings a Voidstar down beside you (two in a Void Storm).
  THE VOID STORM - the End's event: gravity heaves (you're lifted, then let down slowly), rifts tear open and drag at you
    (step through one for a Void Shard, and a long fall), rift mites crawl out, and VOIDSTARS fall ten times as often.
THE STARS - the Nether's Hellstars and the End's Voidstars fall any time (no night to wait for), glowing where they land.
  Hellstar (use: Fire Resistance and Strength) / Voidstar (use: a Void Blink, 16 blocks where you look).
  Sneak + use with 9: the EMBER MANTLE (carried: Fire Resistance; hurt: a flame nova on up to 4 monsters) / the VOID MANTLE
    (carried: the void gives you back - fall out of the End and you're set down where you last stood; hurt: up to 3 monsters
    flung up into the air).
  GROUND FORGES: a Hellstar and a Heartstone, in the Nether: an EMBERHEART (use: +1 attack damage, for good, up to 3).
    A Voidstar and a Heartstone, in the End: a VOIDHEART (use: +1 reach, for good, up to 3).
    A Star Cloak, an Ember Mantle and a Void Mantle together: the MANTLE OF THREE SKIES (all three mantles' powers in one).
CHESTS: bastions, fortresses and End cities now hide Hellstars/Voidstars, Ember Scales/Void Shards, Heartstones (more often),
  Medallions, and now and then a Smouldering Idol or a Starless Eye."""
import math
from items import item, T, TOTEM, ITEMS, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import hellend as H
import phase22 as R22
import phase160 as P160

HC, VC, SKY = '#ff6a1a', '#c27dff', '#ffe8a0'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
ERU_SECS, ERU_ODDS, ERU_CD = 240, 20, 600          # an eruption: four minutes; a 1-in-20 roll each minute; ten minutes' rest after
VST_SECS, VST_ODDS, VST_CD = 240, 20, 600
STAR_ODDS, STAR_STORM = 150, 12                    # per player, per second: a star falls nearby (1 in 150; in an event 1 in 12)
HEART_CAP = 3
END_SAFE = R22.END_SAFE
NETHER_T = ['bastion_treasure', 'bastion_other', 'bastion_bridge', 'bastion_hoglin_stable', 'nether_bridge']
END_T = ['end_city_treasure']
# (extra heartstone % on top of the old odds, star chance %, currency chance %, idol/eye %, medallion %)
CHEST_PLUS = {'bastion_treasure': (10, 45, 70, 6, 20), 'bastion_other': (5, 30, 60, 3, 8), 'bastion_bridge': (6, 30, 60, 3, 8),
              'bastion_hoglin_stable': (6, 30, 60, 3, 8), 'nether_bridge': (6, 35, 60, 4, 10), 'end_city_treasure': (12, 40, 70, 6, 15)}


# ================================================================================================ items
def _use(sound, secs=0.8):
    return {'minecraft:consumable': consumable(secs, 'none', sound, False)}


item('hellstar', TOTEM, 'Hellstar', HC, ['A star that fell the wrong way - down, into the Nether.', ('Use: Fire Resistance (3 min) and Strength (1 min).', 'blue'),
                                         ('Sneak + use with 9: an Ember Mantle.', 'blue'), ('With a Heartstone, on the ground in the Nether:', 'gray'),
                                         ('an Emberheart.', 'gray')], model='bm:hellstar', stack=64, cat='relic', glint=True, comps=hold('none'))
HOLD['hellstar'] = 'bm:p200/hs/use'
item('voidstar', TOTEM, 'Voidstar', VC, ['A star that fell out of the sky altogether.', ('Use: a Void Blink - 16 blocks where you look.', 'blue'),
                                        ('Sneak + use with 9: a Void Mantle.', 'blue'), ('With a Heartstone, on the ground in the End:', 'gray'),
                                        ('a Voidheart.', 'gray')], model='bm:voidstar', stack=64, cat='relic', glint=True, comps=hold('none'))
HOLD['voidstar'] = 'bm:p200/vs/use'
item('ember_mantle', TOTEM, 'Ember Mantle', HC, ['Nine Hellstars, stitched with fire.', ('Carried: Fire Resistance.', 'blue'),
                                                ('When you\'re hurt: a flame nova burns up to', 'blue'), ('4 monsters near you (3 s cooldown).', 'blue')],
     model='bm:ember_mantle', stack=1, cat='relic', glint=True, bold=True)
item('void_mantle', TOTEM, 'Void Mantle', VC, ['Nine Voidstars, stitched with nothing.', ('Carried: fall out of the End and the void', 'blue'),
                                              ('gives you back - where you last stood.', 'blue'), ('When you\'re hurt: up to 3 monsters are', 'blue'),
                                              ('flung into the air (3 s cooldown).', 'blue')], model='bm:void_mantle', stack=1, cat='relic', glint=True, bold=True)
item('three_skies_mantle', TOTEM, 'Mantle of Three Skies', SKY, ['The Star Cloak, the Ember Mantle and the Void Mantle, forged as one.',
                                                                 ('Carried: all three mantles\' powers -', 'blue'), ('stars strike, flames burst and the void', 'blue'),
                                                                 ('flings, when you\'re hurt; Fire Resistance;', 'blue'), ('the void gives you back.', 'blue')],
     model='bm:three_skies_mantle', stack=1, cat='relic', glint=True, tier=3)
item('emberheart', TOTEM, 'Emberheart', HC, ['A Heartstone that swallowed a Hellstar.', ('Use: +1 attack damage, for good.', 'blue'),
                                            (f'Up to {HEART_CAP}. Kept through death.', 'gray')], model='bm:emberheart', stack=16, cat='relic', glint=True,
     comps={'minecraft:consumable': consumable(1.6, 'eat', 'minecraft:item.firecharge.use', False)})
item('voidheart', TOTEM, 'Voidheart', VC, ['A Heartstone that swallowed a Voidstar.', ('Use: +1 block and +0.5 entity reach, for good.', 'blue'),
                                          (f'Up to {HEART_CAP}. Kept through death.', 'gray')], model='bm:voidheart', stack=16, cat='relic', glint=True,
     comps={'minecraft:consumable': consumable(1.6, 'eat', 'minecraft:entity.enderman.teleport', False)})

# the ground forges (phase160 draws them; these run at import, before it does)
P160.RECIPES += [
    ('emberheart', 'Emberheart', HC, ['1.0,0.42,0.1', '1.0,0.2,0.2', '1.0,0.8,0.3'], (holds('hellstar'), 1), [(holds('heartstone'), 1)],
     'execute if dimension minecraft:the_nether', 'The Hellstar and the heart stir... but only the Nether\'s heat can fuse them.'),
    ('voidheart', 'Voidheart', VC, ['0.76,0.49,1.0', '1.0,0.2,0.35', '0.3,0.1,0.5'], (holds('voidstar'), 1), [(holds('heartstone'), 1)],
     'execute if dimension minecraft:the_end', 'The Voidstar and the heart stir... but only the End\'s cold can fuse them.'),
    ('skies', 'Mantle of Three Skies', SKY, ['1.0,0.95,0.6', '1.0,0.42,0.1', '0.76,0.49,1.0'], (holds('star_cloak'), 1),
     [(holds('ember_mantle'), 1), (holds('void_mantle'), 1)], None, None)]
P160.RESULT.update({'emberheart': 'emberheart', 'voidheart': 'voidheart', 'skies': 'three_skies_mantle'})

# the outposts' rats: their field stock and more
OUTPOST_EXTRA = {'ember': [(('ember_scale', 10), ('hellstar', 1)), (('ember_scale', 36), ('heartstone', 1)), (('ember_scale', 30), ('sum_colossus', 1)),
                           (('ember_scale', 4), ('blaze_rod', 3)), (('ember_scale', 4), ('magma_cream', 4))],
                 'void': [(('void_shard', 10), ('voidstar', 1)), (('void_shard', 36), ('heartstone', 1)), (('void_shard', 30), ('sum_voidwalker', 1)),
                          (('void_shard', 8), ('shulker_shell', 2)), (('void_shard', 6), ('ender_pearl', 4))]}


def extend_offers(O, offer):
    pass


# ================================================================================================ icons
def _icons():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    out = {}

    def star(fill, edge, glow):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        pts = []
        for i in range(10):
            a = math.pi / 2 + i * math.pi / 5
            r = 7 if i % 2 == 0 else 3
            pts.append((7.5 + r * math.cos(a), 7.5 - r * math.sin(a)))
        d.polygon(pts, fill=hexc(fill), outline=hexc(edge)); d.point((7, 6), fill=hexc(glow)); d.point((8, 7), fill=hexc(glow))
        return im, d
    im, d = star('#ff7a1a', '#8a2a0a', '#fff0a0'); d.point((5, 9), fill=hexc('#ffd040')); out['hellstar'] = im
    im, d = star('#9a5ad8', '#2a0a4a', '#f0d8ff'); d.point((10, 9), fill=hexc('#ff6ad8')); out['voidstar'] = im

    def mantle(body, trim, dots):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(4, 2), (11, 2), (14, 14), (1, 14)], fill=hexc(body), outline=hexc(trim))
        d.line([(4, 2), (11, 2)], fill=hexc(trim)); d.rectangle((6, 1, 9, 2), fill=hexc(trim))
        for (x, y), c in dots: d.point((x, y), fill=hexc(c))
        return im
    out['ember_mantle'] = mantle('#8a1a0a', '#ffb040', [((5, 6), '#ff7a1a'), ((9, 8), '#ffd040'), ((7, 11), '#ff7a1a'), ((11, 12), '#ffd040')])
    out['void_mantle'] = mantle('#1a0a2a', '#c27dff', [((5, 6), '#c27dff'), ((9, 8), '#ff6ad8'), ((7, 11), '#c27dff'), ((11, 12), '#ffffff')])
    out['three_skies_mantle'] = mantle('#2a2a5a', '#ffe8a0', [((5, 6), '#ffe85a'), ((9, 8), '#ff7a1a'), ((7, 11), '#c27dff'), ((11, 12), '#ffe85a'),
                                                               ((4, 12), '#ff7a1a'), ((10, 5), '#c27dff')])

    def heart(fill, edge, spark):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((2, 3, 8, 9), fill=hexc(fill)); d.ellipse((7, 3, 13, 9), fill=hexc(fill)); d.polygon([(2, 7), (13, 7), (7.5, 14)], fill=hexc(fill))
        d.line([(3, 4), (4, 3)], fill=hexc('#ffffff')); d.point((7, 8), fill=hexc(spark)); d.point((8, 9), fill=hexc(spark)); d.point((9, 7), fill=hexc(spark))
        return im
    out['emberheart'] = heart('#d02a1a', '#600a0a', '#ffb040')
    out['voidheart'] = heart('#7a2ad0', '#2a0a4a', '#ff6ad8')
    return out


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS.update(_icons())


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
    objs = ['bm.fst', 'bm.fwk', 'bm.lbt', 'bm.rft', 'bm.mtcd', 'bm.ehrt', 'bm.vhrt', 'bm.vgx', 'bm.vgy', 'bm.vgz', 'bm.gaze', 'bm.veye', 'bm.ofwk']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'bossbar add bm:eruption {snbt(T("Eruption", HC))}', 'bossbar set bm:eruption color red', f'bossbar set bm:eruption max {ERU_SECS}',
         'bossbar set bm:eruption style notched_10', f'bossbar add bm:voidstorm {snbt(T("Void Storm", VC))}', 'bossbar set bm:voidstorm color purple',
         f'bossbar set bm:voidstorm max {VST_SECS}', 'bossbar set bm:voidstorm style notched_10', 'scoreboard players set #20 bm.rng 20']
    G.OBJECTIVES += objs
    G.FUNCS['admin/uninstall'][0:0] = ['bossbar remove bm:eruption', 'bossbar remove bm:voidstorm', 'kill @e[type=minecraft:marker,tag=bm.lbomb]',
                                       'kill @e[type=minecraft:marker,tag=bm.vrift]', 'kill @e[type=minecraft:interaction,tag=bm.p200box]',
                                       'kill @e[type=minecraft:item_display,tag=bm.orat_sprite]',
                                       'execute as @e[type=minecraft:wandering_trader,tag=bm.orat] at @s run tp @s ~ -300 ~',
                                       'kill @e[type=minecraft:marker,tag=bm.p200seed]']
    from structures import Build

    # ---------------------------------------------------------------- the places: worldgen seeds, built when someone comes near
    PLACES = {  # key: (builder, dims, biomes, spacing, separation, salt, offset (x, z), dimension)
        'ember_outpost': (H.ember_outpost, H.EO, ['minecraft:nether_wastes', 'minecraft:crimson_forest', 'minecraft:warped_forest', 'minecraft:soul_sand_valley'],
                          26, 10, 91200417, (-11, -11), 'nether'),
        'colossus_forge': (H.colossus_forge, H.CF, ['minecraft:basalt_deltas', 'minecraft:nether_wastes', 'minecraft:crimson_forest'],
                           40, 16, 91200433, (-20, -23), 'nether'),
        'void_outpost': (H.void_outpost, H.VO, ['minecraft:end_highlands', 'minecraft:end_midlands', 'minecraft:end_barrens', 'minecraft:small_end_islands'],
                         22, 8, 91200451, (-12, -12), 'end'),
        'observatory': (H.observatory, H.OB, ['minecraft:end_highlands', 'minecraft:end_midlands', 'minecraft:end_barrens', 'minecraft:small_end_islands'],
                        30, 12, 91200467, (-15, -15), 'end'),
    }
    for k, (build, dims, biomes, spacing, sep, salt, (ox, oz), dim) in PLACES.items():
        wjson(f'bm/tags/worldgen/biome/has_structure/p200_{k}.json', {'values': biomes})
        wjson(f'bm/worldgen/structure/p200_{k}.json', {'type': 'minecraft:jigsaw', 'biomes': f'#bm:has_structure/p200_{k}', 'step': 'surface_structures',
                                                       'spawn_overrides': {}, 'terrain_adaptation': 'none', 'start_pool': f'bm:p200_{k}/start', 'size': 1,
                                                       'start_height': {'absolute': 64}, 'max_distance_from_center': 80, 'use_expansion_hack': False,
                                                       'liquid_settings': 'ignore_waterlogging',
                                                       **({'project_start_to_heightmap': 'WORLD_SURFACE_WG', 'start_height': {'absolute': 0}} if dim == 'end' else {})})
        wjson(f'bm/worldgen/template_pool/p200_{k}/start.json', {'fallback': 'minecraft:empty', 'elements': [
            {'weight': 1, 'element': {'element_type': 'minecraft:single_pool_element', 'location': f'bm:p200_{k}_seed', 'projection': 'rigid', 'processors': 'minecraft:empty'}}]})
        wjson(f'bm/worldgen/structure_set/p200_{k}.json', {'structures': [{'structure': f'bm:p200_{k}', 'weight': 1}],
                                                          'placement': {'type': 'minecraft:random_spread', 'spacing': spacing, 'separation': sep, 'salt': salt}})
        Bs = Build(1, 1, 1)
        Bs.marker(0.5, 0.0, 0.5, ['bm.p200seed', f'bm.p200seed_{k}'], 0)
        Bs.export(G.path('data', 'bm', 'structure', f'p200_{k}_seed.nbt'))
        build().export(G.path('data', 'bm', 'structure', f'p200_{k}.nbt'))
        x1, z1 = ox + dims['SX'] - 1, oz + dims['SZ'] - 1
        corners = ' '.join(f'if loaded ~{x} ~ ~{z}' for x in (ox, x1) for z in (oz, z1))
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.p200seed_{k}] at @s if entity @a[distance=..112] {corners} run function bm:p200/{k}/seed')
        oy = -(dims['FLOOR'] + 1)
        place = [f'place template bm:p200_{k} ~{ox} ~{oy} ~{oz}', f'execute as @e[type=minecraft:marker,distance=..40,tag=bm.onew] at @s run function bm:p200/o/init',
                 f'execute as @e[type=minecraft:marker,distance=..40,tag=bm.cfnew] at @s run function bm:p200/forge/init',
                 f'execute as @e[type=minecraft:marker,distance=..40,tag=bm.obnew] at @s run function bm:p200/obs/init']
        fn(f'p200/{k}/place', place)
        if dim == 'nether':
            # (in the Nether there's no sky to drop from: from y 100 down, the first floor with headroom; none - over the lava, at y 40)
            fn(f'p200/{k}/seed', ['scoreboard players set #fy bm.rng 0', f'execute positioned ~ 100 ~ run function bm:p200/{k}/scan',
                                  f'execute if score #fy bm.rng matches 0 positioned ~ 40 ~ run function bm:p200/{k}/place', 'kill @s'])
            fn(f'p200/{k}/scan', ['scoreboard players add #fy bm.rng 1', 'execute if score #fy bm.rng matches 70.. run return run scoreboard players set #fy bm.rng 0',
                                  'execute if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air if block ~ ~2 ~ minecraft:air '
                                  'unless block ~ ~-1 ~ #bm:grap_pass unless block ~ ~-1 ~ minecraft:lava unless block ~ ~-1 ~ minecraft:bedrock '
                                  f'run return run function bm:p200/{k}/place',
                                  f'execute positioned ~ ~-1 ~ run function bm:p200/{k}/scan'])
        else:
            # (in the End: on the island it landed on; over the void, adrift at y 64 - the template brings its own rock)
            fn(f'p200/{k}/seed', [f'execute if entity @s[y=-64,dy=103] positioned ~ 64 ~ run function bm:p200/{k}/place',
                                  f'execute unless entity @s[y=-64,dy=103] run function bm:p200/{k}/place', 'kill @s'])
        nm = {'ember_outpost': "The Ember Rat's Outpost", 'colossus_forge': "The Colossus's Forge", 'void_outpost': "The Void Rat's Outpost",
              'observatory': "The Voidwalker's Observatory"}[k]
        fn(f'admin/{k}', [f'function bm:p200/{k}/place', tellraw('@s', P + [T(f'{nm} is built here.', HC if dim == 'nether' else VC)])])
        G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{k}', 'yellow'), T(f'  build {nm} here', 'gray')]))

    # ---------------------------------------------------------------- the outposts' rats: they stay
    for k in ('ember', 'void'):
        name, color, model, cur, offers, oy, beacon = R22.RATS[k]
        recipes = []
        for buy, sell in list(offers) + OUTPOST_EXTRA[k]:
            if sell == 'TEMPLATE':
                o = G.offer(buy, ('token', 1)); o['sell'] = R22.TEMPLATE
            else:
                o = G.offer(buy, sell)
            recipes.append(o)
        trader = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'DespawnDelay': Int(0),
                  'Tags': ['bm.orat', f'bm.orat_{k}', 'bm.onewr'], 'CustomName': T(name, color, bold=True), 'CustomNameVisible': B(0),
                  'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
                  'attributes': [{'id': 'minecraft:scale', 'base': D(0.7)}], 'Offers': {'Recipes': recipes}}
        sprite = G.rat_sprite(model, ['bm.rat_sprite', 'bm.orat_sprite', 'bm.td', 'bm.r3d', 'bm.onewr'])
        if oy: sprite = sprite.replace('summon minecraft:item_display ~ ~ ~ ', f'summon minecraft:item_display ~ ~{oy} ~ ')
        fn(f'p200/o/rat_{k}', [f'summon minecraft:wandering_trader ~ ~ ~ {snbt(trader)}', sprite,
                               'execute as @e[tag=bm.onewr,distance=..1] run tp @s ~ ~ ~ ~ 0', 'tag @e[tag=bm.onewr,distance=..1] remove bm.onewr'])
        # (refresh: an outpost rat whose stock changed with a new version gets the new list)
        fn(f'p200/o/stock_{k}', [f'data modify entity @s Offers.Recipes set value {snbt(recipes)}', 'tag @s add bm.ostock291'])
        second.append(f'execute as @e[type=minecraft:wandering_trader,tag=bm.orat_{k},tag=!bm.ostock291] run function bm:p200/o/stock_{k}')
    fn('p200/o/init', ['tag @s remove bm.onew', 'tag @s add bm.outpost',
                       'execute if entity @s[tag=bm.oember] run tag @s add bm.outpost_ember', 'execute if entity @s[tag=bm.ovoid] run tag @s add bm.outpost_void',
                       'execute if entity @s[tag=bm.oember] run function bm:p200/o/rat_ember', 'execute if entity @s[tag=bm.ovoid] run function bm:p200/o/rat_void'])
    second += ['execute as @e[type=minecraft:marker,tag=bm.outpost_ember] at @s if entity @a[distance=..48] run particle minecraft:flame ~ ~3 ~ 0.1 2 0.1 0.005 4 force @a[distance=..96]',
               'execute as @e[type=minecraft:marker,tag=bm.outpost_void] at @s if entity @a[distance=..48] run particle minecraft:reverse_portal ~ ~3 ~ 0.2 2 0.2 0.01 10 force @a[distance=..96]']

    # ---------------------------------------------------------------- the dimensions' players (tags, each second) and the minute's rolls
    second[0:0] = ['tag @a remove bm.innether', 'tag @a remove bm.outerend',
                   'execute as @a[gamemode=!spectator,tag=!bm.adv] at @s if dimension minecraft:the_nether run tag @s add bm.innether',
                   f'execute as @a[gamemode=!spectator,tag=!bm.adv] at @s if dimension minecraft:the_end unless entity @s[x=-{END_SAFE},y=-64,z=-{END_SAFE},'
                   f'dx={END_SAFE * 2},dy=448,dz={END_SAFE * 2}] run tag @s add bm.outerend']
    second += ['scoreboard players add #p200m bm.bm 1', 'execute if score #p200m bm.bm matches 60.. run function bm:p200/minute']
    fn('p200/minute', ['scoreboard players set #p200m bm.bm 0',
                       'scoreboard players remove #erucd bm.bm 60', 'scoreboard players remove #vstcd bm.bm 60',
                       'execute unless score #eru bm.bm matches 1.. unless score #erucd bm.bm matches 1.. if entity @a[tag=bm.innether] run function bm:p200/eru/roll',
                       'execute unless score #vst bm.bm matches 1.. unless score #vstcd bm.bm matches 1.. if entity @a[tag=bm.outerend] run function bm:p200/vst/roll'])

    # ---------------------------------------------------------------- the stars: Hellstars in the Nether, Voidstars out in the End
    second += [f'execute as @a[tag=bm.innether] at @s run function bm:p200/hs/roll', f'execute as @a[tag=bm.outerend] at @s run function bm:p200/vs/roll']
    for s, (star, tagd, col, streak, burst, sound, event) in {
            'hs': ('hellstar', 'bm.hstar', HC, 'minecraft:flame', 'minecraft:lava', 'minecraft:entity.blaze.shoot', '#eru'),
            'vs': ('voidstar', 'bm.vstar', VC, 'minecraft:reverse_portal', 'minecraft:portal', 'minecraft:entity.enderman.teleport', '#vst')}.items():
        fn(f'p200/{s}/roll', [f'execute store result score #r bm.rng run random value 1..{STAR_ODDS}',
                              f'execute if score {event} bm.bm matches 1.. store result score #r bm.rng run random value 1..{STAR_STORM}',
                              'execute unless score #r bm.rng matches 1 run return 0',
                              f'execute if entity @e[type=minecraft:item,tag={tagd},distance=..48] run return 0',
                              f'function bm:p200/{s}/drop'])
        fn(f'p200/{s}/drop', ['execute store result storage bm:p200 s.x int 1 run random value -14..14',
                              'execute store result storage bm:p200 s.z int 1 run random value -14..14',
                              f'function bm:p200/{s}/at with storage bm:p200 s'])
        fn(f'p200/{s}/at', [f'$execute positioned ~$(x) ~6 ~$(z) align y run function bm:p200/{s}/find_start'])
        fn(f'p200/{s}/find_start', ['scoreboard players set #fy bm.rng 0', f'function bm:p200/{s}/find'])
        fn(f'p200/{s}/find', ['scoreboard players add #fy bm.rng 1', 'execute if score #fy bm.rng matches 20.. run return 0',
                              'execute if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air unless block ~ ~-1 ~ #bm:grap_pass unless block ~ ~-1 ~ minecraft:lava '
                              f'run return run function bm:p200/{s}/land', f'execute positioned ~ ~-1 ~ run function bm:p200/{s}/find'])
        fn(f'p200/{s}/land', ['execute unless function bm:p37/allowed run return 0'] +
           [f'particle {streak} ~{10 - i} ~{20 - 2 * i} ~ 0 0 0 0 2 force' for i in range(10)] +
           [f'particle {burst} ~ ~0.5 ~ 0.3 0.2 0.3 0.1 20 force', f'playsound {sound} ambient @a[distance=..48] ~ ~ ~ 1 0.6',
            'playsound minecraft:entity.firework_rocket.twinkle_far ambient @a[distance=..64] ~ ~ ~ 1 0.8',
            f'loot spawn ~ ~0.5 ~ loot bm:items/{star}',
            f'execute as @e[type=minecraft:item,distance=..2,tag=!{tagd}] if items entity @s contents {holds(star)} run data merge entity @s {{Glowing:1b,Tags:["{tagd}"]}}'])
        fast.append(f'execute as @e[type=minecraft:item,tag={tagd}] at @s run particle {streak} ~ ~0.4 ~ 0.1 0.2 0.1 0.01 1')
    # one star: its power; nine (sneaking): its mantle
    for s, star, mantle, col, word in (('hs', 'hellstar', 'ember_mantle', HC, 'Ember'), ('vs', 'voidstar', 'void_mantle', VC, 'Void')):
        fn(f'p200/{s}/use', [f'execute if predicate bm:p20/sneaking run return run function bm:p200/{s}/knot', f'function bm:p200/{s}/power'])
        fn(f'p200/{s}/knot', [f'execute store result score #n bm.rng run clear @s {holds(star)} 0',
                              'execute if score #n bm.rng matches ..8 run return run ' + title('@s', 'actionbar', [T(f'An {word} Mantle takes 9 {ITEMS[star]["name"]}s. You have ', 'gray'),
                                                                                                                {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': col}, T('.', 'gray')]),
                              f'clear @s {holds(star)} 9', give(mantle), 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.8',
                              f'particle minecraft:dust{{color:[{"1.0,0.42,0.1" if s == "hs" else "0.76,0.49,1.0"}],scale:1.5}} ~ ~1 ~ 0.4 0.6 0.4 0 40',
                              say(f'Nine stars knot into an {word} Mantle.', col)])
    fn('p200/hs/power', [f'clear @s {holds("hellstar")} 1', 'effect give @s minecraft:fire_resistance 180 0', 'effect give @s minecraft:strength 60 0',
                         'particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.05 30', 'playsound minecraft:item.firecharge.use player @s ~ ~ ~ 1 0.8',
                         say('The Hellstar burns into you: Fire Resistance and Strength.', HC)])
    fn('p200/vs/power', ['execute unless function bm:p37/allowed run return run ' + say('The walls here are warded. The Voidstar flickers and stays.', VC),
                         f'clear @s {holds("voidstar")} 1', 'scoreboard players set #ray bm.rng 32', 'tag @s add bm.blinker',
                         'execute anchored eyes positioned ^ ^ ^ run function bm:p200/vs/ray', 'tag @s remove bm.blinker'])
    fn('p200/vs/ray', ['execute unless block ^ ^ ^0.5 #bm:grap_pass run return run function bm:p200/vs/blink',
                       'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 0 run return run function bm:p200/vs/blink',
                       'execute positioned ^ ^ ^0.5 run function bm:p200/vs/ray'])
    fn('p200/vs/blink', ['particle minecraft:reverse_portal ~ ~ ~ 0.3 0.5 0.3 0.05 30',
                         'execute as @a[tag=bm.blinker] at @s run particle minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 0.5 40',
                         'tp @a[tag=bm.blinker] ~ ~-1 ~', 'effect give @a[tag=bm.blinker] minecraft:slow_falling 3 0 true',
                         'playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 1.2'])

    # ---------------------------------------------------------------- the mantles: carried, and when you're hurt
    def carried(iids, f):
        out = []
        for iid in iids:
            out += [f'execute as @a if items entity @s container.* {holds(iid)} at @s run function {f}',
                    f'execute as @a unless items entity @s container.* {holds(iid)} if items entity @s weapon.offhand {holds(iid)} at @s run function {f}']
        return out
    second += carried(['ember_mantle', 'three_skies_mantle'], 'bm:p200/m/fire')
    second += carried(['void_mantle', 'three_skies_mantle'], 'bm:p200/m/void')
    fn('p200/m/fire', ['effect give @s minecraft:fire_resistance 3 0 true'])
    # (the void gives you back: where you last stood on solid ground, out in the End)
    wjson('bm/predicate/p200/on_ground.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}})
    fn('p200/m/void', ['execute unless dimension minecraft:the_end run return 0', 'execute if entity @s[y=-400,dy=399] run return 0',
                       'execute unless predicate bm:p200/on_ground run return 0',
                       'execute store result score @s bm.vgx run data get entity @s Pos[0]', 'execute store result score @s bm.vgy run data get entity @s Pos[1]',
                       'execute store result score @s bm.vgz run data get entity @s Pos[2]'])
    fn('p200/m/rescue', ['execute unless score @s bm.vgy matches 1.. run return run function bm:p200/m/rescue_up',
                         'execute store result storage bm:p200 r.x int 1 run scoreboard players get @s bm.vgx',
                         'execute store result storage bm:p200 r.y int 1 run scoreboard players get @s bm.vgy',
                         'execute store result storage bm:p200 r.z int 1 run scoreboard players get @s bm.vgz',
                         'function bm:p200/m/rescue_tp with storage bm:p200 r'])
    fn('p200/m/rescue_tp', ['$tp @s $(x).5 $(y) $(z).5', 'effect give @s minecraft:slow_falling 4 0 true', 'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                            'playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 1 0.6', say('The void gives you back.', VC)])
    fn('p200/m/rescue_up', ['tp @s ~ 120 ~', 'effect give @s minecraft:slow_falling 40 0 true', say('The void gives you back - from on high.', VC)])
    wjson('bm/advancement/p200/hurt.json', {'criteria': {'hurt': {'trigger': 'minecraft:entity_hurt_player'}}, 'rewards': {'function': 'bm:p200/m/hurt'}})
    has = lambda iid: f'if items entity @s container.* {holds(iid)}'
    fn('p200/m/hurt', ['advancement revoke @s only bm:p200/hurt',
                       'execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g2 bm.rng = #g bm.rng',
                       'scoreboard players operation #g2 bm.rng -= @s bm.mtcd', 'execute if score @s bm.mtcd matches 1.. if score #g2 bm.rng matches ..59 run return 0',
                       'scoreboard players set #mh bm.rng 0',
                       f'execute {has("ember_mantle")} run scoreboard players set #mh bm.rng 1',
                       f'execute {has("void_mantle")} run scoreboard players add #mh bm.rng 2',
                       f'execute {has("three_skies_mantle")} run scoreboard players set #mh bm.rng 7',
                       'execute if score #mh bm.rng matches 0 run return 0',
                       'scoreboard players operation @s bm.mtcd = #g bm.rng', 'tag @s add bm.mantlec',
                       'execute if score #mh bm.rng matches 1 run function bm:p200/m/nova', 'execute if score #mh bm.rng matches 3 run function bm:p200/m/nova',
                       'execute if score #mh bm.rng matches 7 run function bm:p200/m/nova',
                       'execute if score #mh bm.rng matches 2..3 run function bm:p200/m/fling', 'execute if score #mh bm.rng matches 7 run function bm:p200/m/fling',
                       'execute if score #mh bm.rng matches 7 run function bm:p200/m/stars',
                       'tag @s remove bm.mantlec'])
    fn('p200/m/nova', ['particle minecraft:flame ~ ~1 ~ 2 0.5 2 0.08 80', 'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 1 0.7',
                       'execute as @e[type=#bm:hostile,distance=..6,sort=nearest,limit=4] at @s run function bm:p200/m/burn'])
    fn('p200/m/burn', ['damage @s 5 minecraft:player_attack by @p[tag=bm.mantlec]', 'data merge entity @s {Fire:80s}', 'particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 6'])
    fn('p200/m/fling', ['particle minecraft:reverse_portal ~ ~1 ~ 2 0.5 2 0.05 60', 'playsound minecraft:entity.shulker.shoot player @a[distance=..16] ~ ~ ~ 1 0.6',
                        'execute as @e[type=#bm:hostile,distance=..8,sort=nearest,limit=3] at @s run function bm:p200/m/flung'])
    fn('p200/m/flung', ['effect give @s minecraft:levitation 2 3', 'damage @s 4 minecraft:magic by @p[tag=bm.mantlec]', 'particle minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 0.5 20'])
    fn('p200/m/stars', ['tag @s add bm.starc', 'execute as @e[type=#bm:hostile,distance=..12,sort=nearest,limit=3] at @s run function bm:p39/star/strike', 'tag @s remove bm.starc'])

    # ---------------------------------------------------------------- Emberheart / Voidheart: for good (re-applied after death)
    for k, iid, obj, mods, col, txt in (('eh', 'emberheart', 'bm.ehrt', [('attack_damage', 1.0)], HC, 'Fire runs in your arm'),
                                         ('vh', 'voidheart', 'bm.vhrt', [('block_interaction_range', 1.0), ('entity_interaction_range', 0.5)], VC, 'Your reach stretches into the void')):
        G.consume_adv(iid, f'bm:p200/{k}/use')
        fn(f'p200/{k}/use', [f'advancement revoke @s only bm:consume/{iid}',
                             f'execute if score @s {obj} matches {HEART_CAP}.. run return run function bm:p200/{k}/full',
                             f'scoreboard players add @s {obj} 1', f'function bm:p200/{k}/apply',
                             title('@s', 'actionbar', [T(f'{txt}: ', col), {'score': {'name': '@s', 'objective': obj}, 'color': 'white'}, T(f' / {HEART_CAP}', 'gray')]),
                             'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.9', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4'])
        fn(f'p200/{k}/full', [give(iid), say(f'You already hold all you can ({HEART_CAP}). (Refunded)', col)])
        ap = []
        for a, per in mods:
            ap += [f'attribute @s minecraft:{a} modifier remove bm:{iid}_{a}',
                   f'execute store result storage bm:p200 {k}.{a} double {per} run scoreboard players get @s {obj}']
        ap.append(f'function bm:p200/{k}/set with storage bm:p200 {k}')
        fn(f'p200/{k}/apply', ap)
        fn(f'p200/{k}/set', [f'$attribute @s minecraft:{a} modifier add bm:{iid}_{a} $({a}) add_value' for a, _ in mods])
        fn(f'p200/{k}/has', [f'return run attribute @s minecraft:{mods[0][0]} modifier value get bm:{iid}_{mods[0][0]}'])
        second.append(f'execute as @a[scores={{{obj}=1..}}] unless function bm:p200/{k}/has run function bm:p200/{k}/apply')

    # ---------------------------------------------------------------- THE ERUPTION
    fn('p200/eru/roll', [f'execute store result score #r bm.rng run random value 1..{ERU_ODDS}', 'execute if score #r bm.rng matches 1 run function bm:p200/eru/start'])
    fn('admin/eruption', ['function bm:p200/eru/start', tellraw('@s', P + [T('An Eruption begins in the Nether.', HC)])])
    fn('admin/voidstorm', ['function bm:p200/vst/start', tellraw('@s', P + [T('A Void Storm begins in the End.', VC)])])
    G.FUNCS['admin/help'] += [tellraw('@s', [T('/function bm:admin/eruption', 'yellow'), T('  start an Eruption (the Nether)', 'gray')]),
                              tellraw('@s', [T('/function bm:admin/voidstorm', 'yellow'), T('  start a Void Storm (the outer End)', 'gray')])]
    fn('p200/eru/start', ['tag @a remove bm.innether', 'execute as @a[gamemode=!spectator,tag=!bm.adv] at @s if dimension minecraft:the_nether run tag @s add bm.innether',
                          f'scoreboard players set #eru bm.bm {ERU_SECS}', 'bossbar set bm:eruption visible true',
                          title('@a[tag=bm.innether]', 'title', T('ERUPTION', HC, bold=True)),
                          title('@a[tag=bm.innether]', 'subtitle', T('The Nether boils over - watch for the rings!', '#ffb070')),
                          'execute as @a[tag=bm.innether] at @s run playsound minecraft:entity.generic.explode ambient @s ~ ~ ~ 1 0.4',
                          'execute as @a[tag=bm.innether] at @s run playsound minecraft:ambient.basalt_deltas.mood ambient @s ~ ~ ~ 1 0.5'])
    second += ['execute if score #eru bm.bm matches 1.. run function bm:p200/eru/second']
    fn('p200/eru/second', ['scoreboard players remove #eru bm.bm 1', 'execute store result bossbar bm:eruption value run scoreboard players get #eru bm.bm',
                           'bossbar set bm:eruption players @a[tag=bm.innether]', 'tag @a[tag=bm.innether] add bm.erup',
                           'execute as @a[tag=bm.innether] at @s run function bm:p200/eru/player',
                           'execute if score #eru bm.bm matches 0 run function bm:p200/eru/end'])
    fn('p200/eru/player', ['particle minecraft:ash ~ ~3 ~ 10 4 10 0 40 normal @s', 'particle minecraft:lava ~ ~6 ~ 12 3 12 0 4 normal @s',
                           'execute store result score #r bm.rng run random value 1..8',
                           'execute if score #r bm.rng matches 1 run playsound minecraft:entity.generic.explode ambient @s ~ ~-8 ~ 0.5 0.4',
                           'execute if score #r bm.rng matches 2 run playsound minecraft:block.lava.extinguish ambient @s ~ ~ ~ 0.6 0.5',
                           # the shelter: an Ember Rat's outpost
                           'execute if entity @e[type=minecraft:marker,tag=bm.outpost_ember,distance=..16] run return run effect give @s minecraft:fire_resistance 3 0 true',
                           'execute store result score #r bm.rng run random value 1..3', 'execute if score #r bm.rng matches 1 run function bm:p200/eru/bomb_drop',
                           'execute store result score #r bm.rng run random value 1..15', 'execute if score #r bm.rng matches 1 run function bm:p200/eru/spill'])
    fn('p200/eru/bomb_drop', ['execute store result storage bm:p200 b.x int 1 run random value -9..9', 'execute store result storage bm:p200 b.z int 1 run random value -9..9',
                              'function bm:p200/eru/bomb_at with storage bm:p200 b'])
    fn('p200/eru/bomb_at', ['$summon minecraft:marker ~$(x) ~ ~$(z) {Tags:["bm.lbomb"]}'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.lbomb] at @s run function bm:p200/eru/bomb')
    ring = lambda r, n, p: [f'particle {p} ^{r * math.sin(2 * math.pi * i / n):.2f} ^0.1 ^{r * math.cos(2 * math.pi * i / n):.2f} 0 0 0 0 1' for i in range(n)]
    fn('p200/eru/bomb', ['scoreboard players add @s bm.lbt 1', 'execute if score @s bm.lbt matches 1 run playsound minecraft:entity.blaze.shoot hostile @a[distance=..16] ~ ~ ~ 0.8 0.5',
                         'scoreboard players operation #m bm.rng = @s bm.lbt', 'scoreboard players operation #m bm.rng %= #5 bm.rng',
                         'execute if score #m bm.rng matches 0 rotated 0 0 run function bm:p200/eru/ring',
                         'execute if score @s bm.lbt matches 20..39 run function bm:p200/eru/fall',
                         'execute if score @s bm.lbt matches 40.. run function bm:p200/eru/impact'])
    fn('p200/eru/ring', ring(2.5, 16, 'minecraft:flame'))
    fn('p200/eru/fall', ['scoreboard players set #h bm.rng 40', 'scoreboard players operation #h bm.rng -= @s bm.lbt',
                         'execute store result storage bm:p200 f.h double 0.8 run scoreboard players get #h bm.rng', 'function bm:p200/eru/fall_at with storage bm:p200 f'])
    fn('p200/eru/fall_at', ['$particle minecraft:lava ~ ~$(h) ~ 0.2 0.2 0.2 0 2 force', '$particle minecraft:large_smoke ~ ~$(h) ~ 0.2 0.2 0.2 0.01 1 force'])
    fn('p200/eru/impact', ['particle minecraft:explosion ~ ~0.5 ~ 0.5 0.3 0.5 0 3', 'particle minecraft:lava ~ ~0.5 ~ 1 0.3 1 0 20',
                           'particle minecraft:flame ~ ~0.5 ~ 1.5 0.3 1.5 0.05 40', 'playsound minecraft:entity.generic.explode hostile @a[distance=..24] ~ ~ ~ 1 0.8',
                           'execute as @a[distance=..2.5,gamemode=!spectator,gamemode=!creative] run damage @s 6 bm:magma', 'kill @s'])
    fn('p200/eru/spill', ['execute store result score #n bm.rng if entity @e[type=minecraft:magma_cube,tag=bm.erumob,distance=..24]',
                          'execute if score #n bm.rng matches 6.. run return 0',
                          'execute store result storage bm:p200 b.x int 1 run random value -10..10', 'execute store result storage bm:p200 b.z int 1 run random value -10..10',
                          'function bm:p200/eru/spill_at with storage bm:p200 b'])
    fn('p200/eru/spill_at', ['$execute positioned ~$(x) ~ ~$(z) if block ~ ~ ~ minecraft:air if block ~ ~1 ~ minecraft:air run summon minecraft:magma_cube ~ ~ ~ {Size:1,Tags:["bm.erumob"]}'])
    fn('p200/eru/end', ['bossbar set bm:eruption visible false', f'scoreboard players set #erucd bm.bm {ERU_CD}',
                        'execute as @a[tag=bm.erup,tag=bm.innether] at @s run function bm:p200/eru/survivor', 'tag @a remove bm.erup'])
    fn('p200/eru/survivor', [title('@s', 'title', T('The Eruption ends', HC, bold=True)), title('@s', 'subtitle', T('You rode it out - the Nether pays its dues', '#ffb070')),
                             'loot give @s loot bm:p200/eru_reward', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.9'])
    E = G.loot_entry
    wjson('bm/loot_table/p200/eru_reward.json', {'type': 'minecraft:command', 'pools': [
        {'rolls': 1, 'entries': [E('ember_scale', G.uni(4, 8))]}, {'rolls': 1, 'entries': [E('hellstar')]},
        {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.1)]}]})
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #5 bm.rng 5']

    # ---------------------------------------------------------------- THE VOID STORM
    fn('p200/vst/roll', [f'execute store result score #r bm.rng run random value 1..{VST_ODDS}', 'execute if score #r bm.rng matches 1 run function bm:p200/vst/start'])
    fn('p200/vst/start', ['tag @a remove bm.outerend',
                          f'execute as @a[gamemode=!spectator,tag=!bm.adv] at @s if dimension minecraft:the_end unless entity @s[x=-{END_SAFE},y=-64,z=-{END_SAFE},'
                          f'dx={END_SAFE * 2},dy=448,dz={END_SAFE * 2}] run tag @s add bm.outerend',
                          f'scoreboard players set #vst bm.bm {VST_SECS}', 'bossbar set bm:voidstorm visible true',
                          title('@a[tag=bm.outerend]', 'title', T('VOID STORM', VC, bold=True)),
                          title('@a[tag=bm.outerend]', 'subtitle', T('Gravity breaks. Rifts open. Stars fall.', '#e0c8ff')),
                          'execute as @a[tag=bm.outerend] at @s run playsound minecraft:entity.enderman.stare ambient @s ~ ~ ~ 1 0.5',
                          'execute as @a[tag=bm.outerend] at @s run playsound minecraft:block.end_portal.spawn ambient @s ~ ~ ~ 0.5 0.6'])
    second += ['execute if score #vst bm.bm matches 1.. run function bm:p200/vst/second',
               'execute as @e[type=minecraft:marker,tag=bm.vrift] at @s run function bm:p200/vst/rift_age']
    fn('p200/vst/second', ['scoreboard players remove #vst bm.bm 1', 'execute store result bossbar bm:voidstorm value run scoreboard players get #vst bm.bm',
                           'bossbar set bm:voidstorm players @a[tag=bm.outerend]', 'tag @a[tag=bm.outerend] add bm.vstp',
                           'scoreboard players operation #m bm.rng = #vst bm.bm', 'scoreboard players operation #m bm.rng %= #20 bm.rng',
                           'execute if score #m bm.rng matches 0 as @a[tag=bm.outerend] at @s run function bm:p200/vst/heave',
                           'execute as @a[tag=bm.outerend] at @s run function bm:p200/vst/player',
                           'execute if score #vst bm.bm matches 0 run function bm:p200/vst/end'])
    fn('p200/vst/heave', ['effect give @s minecraft:levitation 3 1 true', 'effect give @s minecraft:slow_falling 10 0 true',
                          say('Gravity heaves!', VC), 'playsound minecraft:entity.shulker.shoot ambient @s ~ ~ ~ 1 0.5'])
    fn('p200/vst/player', ['particle minecraft:reverse_portal ~ ~3 ~ 10 4 10 0.02 40 normal @s', 'particle minecraft:portal ~ ~2 ~ 8 3 8 0.5 30 normal @s',
                           'execute store result score #r bm.rng run random value 1..10',
                           'execute if score #r bm.rng matches 1 run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.6 0.5',
                           'execute if entity @e[type=minecraft:marker,tag=bm.outpost_void,distance=..16] run return 0',
                           'execute store result score #r bm.rng run random value 1..10', 'execute if score #r bm.rng matches 1 run function bm:p200/vst/rift_drop'])
    fn('p200/vst/rift_drop', ['execute if entity @e[type=minecraft:marker,tag=bm.vrift,distance=..16] run return 0',
                              'execute store result storage bm:p200 b.x int 1 run random value -8..8', 'execute store result storage bm:p200 b.z int 1 run random value -8..8',
                              'function bm:p200/vst/rift_at with storage bm:p200 b'])
    fn('p200/vst/rift_at', ['$summon minecraft:marker ~$(x) ~1 ~$(z) {Tags:["bm.vrift","bm.vriftnew"]}',
                            'execute as @e[type=minecraft:marker,tag=bm.vriftnew] at @s run function bm:p200/vst/rift_open'])
    mite = {'Tags': ['bm.riftmite'], 'CustomName': T('Rift Mite', VC), 'PersistenceRequired': B(0)}
    fn('p200/vst/rift_open', ['tag @s remove bm.vriftnew', 'execute if block ~ ~-2 ~ #minecraft:air if block ~ ~-3 ~ #minecraft:air run return run kill @s', 'scoreboard players set @s bm.rft 10', 'playsound minecraft:block.portal.trigger hostile @a[distance=..24] ~ ~ ~ 0.6 1.6',
                              f'summon minecraft:endermite ~ ~ ~ {snbt(mite)}'])
    fn('p200/vst/rift_age', ['scoreboard players remove @s bm.rft 1', 'execute if score @s bm.rft matches ..0 run particle minecraft:reverse_portal ~ ~ ~ 0.3 0.3 0.3 0.2 30',
                             'execute if score @s bm.rft matches ..0 run kill @s'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.vrift] at @s run function bm:p200/vst/rift')
    fn('p200/vst/rift', ['particle minecraft:reverse_portal ~ ~ ~ 0.4 0.6 0.4 0.02 10', 'particle minecraft:portal ~ ~ ~ 0.2 0.3 0.2 1.2 10',
                         'particle minecraft:dust{color:[0.1,0.0,0.2],scale:2.0} ~ ~ ~ 0.2 0.4 0.2 0 4',
                         'execute as @a[distance=..1.3,gamemode=!spectator] at @s run function bm:p200/vst/through',
                         'execute as @a[distance=1.3..5,gamemode=!spectator] at @s facing entity @e[type=minecraft:marker,tag=bm.vrift,sort=nearest,limit=1] feet run tp @s ^ ^ ^0.25'])
    fn('p200/vst/through', ['tp @s ~ ~10 ~', 'effect give @s minecraft:slow_falling 8 0 true', give('void_shard'),
                            'playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 1 0.5', say('Through the rift! (+1 Void Shard)', VC)])
    fn('p200/vst/end', ['bossbar set bm:voidstorm visible false', f'scoreboard players set #vstcd bm.bm {VST_CD}',
                        'kill @e[type=minecraft:marker,tag=bm.vrift]',
                        'execute as @a[tag=bm.vstp,tag=bm.outerend] at @s run function bm:p200/vst/survivor', 'tag @a remove bm.vstp'])
    fn('p200/vst/survivor', [title('@s', 'title', T('The Void Storm passes', VC, bold=True)), title('@s', 'subtitle', T('The End settles - and leaves you something', '#e0c8ff')),
                             'loot give @s loot bm:p200/vst_reward', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.9'])
    wjson('bm/loot_table/p200/vst_reward.json', {'type': 'minecraft:command', 'pools': [
        {'rolls': 1, 'entries': [E('void_shard', G.uni(4, 8))]}, {'rolls': 1, 'entries': [E('voidstar')]},
        {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.1)]}]})
    # the Void Rat's rift anchor: fall out of the End near an outpost and it catches you
    # (every quarter second, and from any depth: a fall into the void is quick)
    fast.append('execute as @a[tag=bm.outerend] at @s if entity @s[y=-400,dy=399] run function bm:p200/o/fall')
    mant = lambda iid: [f'execute if items entity @s container.* {holds(iid)} run return run function bm:p200/m/rescue',
                        f'execute if items entity @s weapon.offhand {holds(iid)} run return run function bm:p200/m/rescue']
    fn('p200/o/fall', mant('void_mantle') + mant('three_skies_mantle') +
       ['execute if entity @e[type=minecraft:marker,tag=bm.outpost_void,distance=..200] run function bm:p200/o/catch'])
    fn('p200/o/catch', ['tp @s @e[type=minecraft:marker,tag=bm.outpost_void,sort=nearest,limit=1]',
                        'effect give @s minecraft:slow_falling 4 0 true', 'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                        say('The Void Rat\'s rift anchor catches you. (Mind the edge!)', VC)])

    # ---------------------------------------------------------------- THE COLOSSUS'S FORGE
    box = lambda tag, w, h, where='~ ~ ~': f'summon minecraft:interaction {where} {{Tags:["bm.p200box","{tag}"],width:{w}f,height:{h}f,response:1b}}'
    fn('p200/forge/init', ['tag @s remove bm.cfnew', 'tag @s add bm.forge', 'scoreboard players set @s bm.fst 0', 'scoreboard players set @s bm.fwk 0',
                           box('bm.fanvil', 1.4, 1.4, '~ ~-0.2 ~3')])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.p200box] if data entity @s interaction at @s run function bm:p200/click')
    fn('p200/click', ['tag @s add bm.p200here', 'execute on target run function bm:p200/clicked', 'tag @s remove bm.p200here', 'data remove entity @s interaction'])
    fn('p200/clicked', ['execute if entity @e[type=minecraft:interaction,tag=bm.p200here,tag=bm.fanvil] run return run function bm:p200/forge/ask',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.p200here,tag=bm.veyebox] run return run function bm:p200/obs/eye',
                        'execute if entity @e[type=minecraft:interaction,tag=bm.p200here,tag=bm.vscopebox] run return run function bm:p200/obs/scope'])
    forge = '@e[type=minecraft:marker,tag=bm.forge,distance=..8,sort=nearest,limit=1]'
    fn('p200/forge/ask', [f'execute store result score #fw bm.rng run scoreboard players get {forge} bm.fwk',
                          f'execute store result score #fs bm.rng run scoreboard players get {forge} bm.fst',
                          'execute if score #fw bm.rng matches 1.. run return run ' + say('The Colossus is awake! The anvil can wait.', HC),
                          'execute if predicate bm:p20/sneaking run return run function bm:p200/forge/wake',
                          'execute if score #fs bm.rng matches 1 if items entity @s weapon.mainhand *[minecraft:max_damage] '
                          'unless items entity @s weapon.mainhand *[minecraft:unbreakable] run return run function bm:p200/forge/temper',
                          'execute if score #fs bm.rng matches 1 run return run ' +
                          tellraw('@s', P + [T('The Great Anvil ', HC, bold=True), T('burns. ', '#ffb070'),
                                             T('Hold anything that wears out and right-click - with 2 Hellstars on you, it\'s tempered unbreakable. ', 'gray'),
                                             T('Sneak + right-click with a Smouldering Idol (or 32 Ember Scales) to wake the Colossus again.', 'dark_gray')]),
                          tellraw('@s', P + [T('The Great Anvil ', HC, bold=True), T('is cold. ', 'gray'),
                                             T('Sneak + right-click it with a Smouldering Idol in hand (or 32 Ember Scales) to wake the Magma Colossus. ', 'gray'),
                                             T('Beat him here and the forge burns again.', '#ffb070')])])
    fn('p200/forge/wake', ['scoreboard players set #ok bm.rng 0',
                           f'execute if items entity @s weapon.mainhand {holds("sum_colossus")} run scoreboard players set #ok bm.rng 1',
                           'execute if score #ok bm.rng matches 1 run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                           f'execute if score #ok bm.rng matches 0 store result score #c bm.rng run clear @s {holds("ember_scale")} 0',
                           f'execute if score #ok bm.rng matches 0 if score #c bm.rng matches 32.. run clear @s {holds("ember_scale")} 32',
                           'execute if score #ok bm.rng matches 0 if score #c bm.rng matches 32.. run scoreboard players set #ok bm.rng 1',
                           'execute if score #ok bm.rng matches 0 run return run ' + say('The anvil wants a Smouldering Idol in your hand - or 32 Ember Scales.', HC),
                           f'execute as {forge} at @s run function bm:p200/forge/rise'])
    fn('p200/forge/rise', ['scoreboard players set @s bm.fwk 1', 'execute positioned ~ ~-2 ~10 run function bm:p54/mcol/summon',
                           'tag @a[distance=..40] add bm.ffight',
                           title('@a[distance=..40]', 'title', T('The forge stirs...', HC, bold=True)),
                           title('@a[distance=..40]', 'subtitle', T('The Magma Colossus rises from the moat!', '#ffb070')),
                           'playsound minecraft:block.anvil.land block @a[distance=..40] ~ ~ ~ 1 0.5'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.forge,scores={bm.fwk=1..}] at @s run function bm:p200/forge/watch')
    fn('p200/forge/watch', ['scoreboard players add @s bm.fwk 1', 'execute if score @s bm.fwk matches ..4 run return 0',
                            'execute if entity @e[type=minecraft:magma_cube,tag=bm.mcol,distance=..60] run return 0',
                            'scoreboard players set @s bm.fwk 0',
                            'execute unless entity @a[distance=..40,gamemode=!spectator] run return run tag @a remove bm.ffight',
                            'function bm:p200/forge/won'])
    fn('p200/forge/won', ['execute unless score @s bm.fst matches 1 run ' + title('@a[distance=..40]', 'title', T('The forge burns again', HC, bold=True)),
                          'scoreboard players set @s bm.fst 1',
                          'execute as @a[distance=..40,gamemode=!spectator] at @s run function bm:p200/forge/spoils', 'tag @a remove bm.ffight',
                          'particle minecraft:lava ~ ~2 ~ 3 2 3 0 60', 'playsound minecraft:block.anvil.use block @a[distance=..40] ~ ~ ~ 1 0.6'])
    fn('p200/forge/spoils', ['loot give @s loot bm:p200/forge_spoils', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1',
                             tellraw('@s', P + [T('The Colossus falls at its own forge: ', HC), T('Hellstars, Ember Scales and a Heartstone are yours.', '#ffb070')])])
    wjson('bm/loot_table/p200/forge_spoils.json', {'type': 'minecraft:command', 'pools': [
        {'rolls': 1, 'entries': [E('hellstar', G.uni(2, 3))]}, {'rolls': 1, 'entries': [E('ember_scale', G.uni(12, 20))]},
        {'rolls': 1, 'entries': [E('heartstone')]}]})
    wjson('bm/item_modifier/p200/temper.json', [{'function': 'minecraft:set_components', 'components': {'minecraft:unbreakable': {}}},
                                                {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T('Colossus-tempered: unbreakable', HC)]}])
    fn('p200/forge/temper', [f'execute store result score #c bm.rng run clear @s {holds("hellstar")} 0',
                             'execute unless score #c bm.rng matches 2.. run return run ' + say('Tempering takes 2 Hellstars.', HC),
                             f'clear @s {holds("hellstar")} 2',
                             'item modify entity @s weapon.mainhand bm:p200/temper',
                             'particle minecraft:lava ~ ~1.2 ~ 0.3 0.2 0.3 0 20', 'particle minecraft:flame ~ ~1.2 ~ 0.3 0.3 0.3 0.05 30',
                             'playsound minecraft:block.anvil.use block @a[distance=..16] ~ ~ ~ 1 0.8', 'playsound minecraft:block.lava.extinguish block @a[distance=..16] ~ ~ ~ 1 1',
                             say('The Great Anvil rings - it will never break now.', HC)])

    # ---------------------------------------------------------------- THE VOIDWALKER'S OBSERVATORY
    eye = {'Tags': ['bm.veyed'], 'item': G.stack('sum_voidwalker'), 'item_display': 'ground', 'billboard': 'fixed',
           'brightness': {'sky': Int(15), 'block': Int(15)}, 'teleport_duration': Int(3),
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                              'translation': [F(0), F(0.3), F(0)], 'scale': [F(1.2)] * 3}}
    fn('p200/obs/init', ['tag @s remove bm.obnew', 'tag @s add bm.observ', 'scoreboard players set @s bm.ofwk 0',
                         f'execute as @e[type=minecraft:marker,tag=bm.vspot_eye,distance=..20] at @s run summon minecraft:item_display ~ ~ ~ {snbt(eye)}',
                         'execute as @e[type=minecraft:marker,tag=bm.vspot_eye,distance=..20] at @s run ' + box('bm.veyebox', 1.0, 1.4, '~ ~-1 ~'),
                         'execute as @e[type=minecraft:marker,tag=bm.vspot_scope,distance=..20] at @s run ' + box('bm.vscopebox', 1.6, 3.0)])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.veyed]']
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.veyed] at @s if entity @a[distance=..32] run tp @s ~ ~ ~ ~5 0')
    obs = '@e[type=minecraft:marker,tag=bm.observ,distance=..30,sort=nearest,limit=1]'
    fn('p200/obs/eye', [f'execute store result score #fw bm.rng run scoreboard players get {obs} bm.ofwk',
                        'execute if score #fw bm.rng matches 1.. run return run ' + say('The Voidwalker is here!', VC),
                        'execute unless score @s bm.veye matches 1 run return run function bm:p200/obs/take',
                        'execute if predicate bm:p20/sneaking run return run function bm:p200/obs/call',
                        tellraw('@s', P + [T('The pedestal ', VC, bold=True), T('holds another Starless Eye - but that one is for the next stargazer. ', 'gray'),
                                           T('Sneak + right-click with 3 Voidstars on you to call the Voidwalker here.', 'dark_gray')])])
    fn('p200/obs/take', ['scoreboard players set @s bm.veye 1', give('sum_voidwalker'), 'playsound minecraft:block.end_portal_frame.fill block @s ~ ~ ~ 1 0.7',
                         'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.4 0.3 0.05 30',
                         tellraw('@s', P + [T('You lift the Starless Eye from its pedestal. ', VC), T('Another opens in its place, for the next stargazer.', 'gray')])])
    fn('p200/obs/call', [f'execute store result score #c bm.rng run clear @s {holds("voidstar")} 0',
                         'execute unless score #c bm.rng matches 3.. run return run ' + say('Calling him here takes 3 Voidstars.', VC),
                         f'clear @s {holds("voidstar")} 3', f'execute as {obs} at @s run function bm:p200/obs/rise'])
    fn('p200/obs/rise', ['scoreboard players set @s bm.ofwk 1', 'execute positioned ~ ~ ~-6 run function bm:p54/vwk/summon',
                         title('@a[distance=..40]', 'title', T('The lens turns...', VC, bold=True)),
                         title('@a[distance=..40]', 'subtitle', T('The Voidwalker comes to his observatory!', '#e0c8ff'))])
    second.append('execute as @e[type=minecraft:marker,tag=bm.observ,scores={bm.ofwk=1..}] at @s run function bm:p200/obs/watch')
    fn('p200/obs/watch', ['scoreboard players add @s bm.ofwk 1', 'execute if score @s bm.ofwk matches ..4 run return 0',
                          'execute if entity @e[type=minecraft:enderman,tag=bm.vwk,distance=..80] run return 0', 'scoreboard players set @s bm.ofwk 0',
                          'execute if entity @a[distance=..40,gamemode=!spectator] as @a[distance=..40,gamemode=!spectator] at @s run function bm:p200/obs/spoils'])
    fn('p200/obs/spoils', ['loot give @s loot bm:p200/obs_spoils', 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 1',
                           tellraw('@s', P + [T('The Voidwalker falls among his stars: ', VC), T('Voidstars, Void Shards and a Heartstone are yours.', '#e0c8ff')])])
    wjson('bm/loot_table/p200/obs_spoils.json', {'type': 'minecraft:command', 'pools': [
        {'rolls': 1, 'entries': [E('voidstar', G.uni(2, 3))]}, {'rolls': 1, 'entries': [E('void_shard', G.uni(12, 20))]},
        {'rolls': 1, 'entries': [E('heartstone')]}]})
    fn('p200/obs/scope', ['execute if score @s bm.gaze = #day bm.bm run return run ' + say('The stars have shown you all they will today. Come back tomorrow.', VC),
                          'scoreboard players operation @s bm.gaze = #day bm.bm', 'playsound minecraft:block.beacon.power_select block @s ~ ~ ~ 1 1.6',
                          tellraw('@s', P + [T('You put your eye to the telescope... ', VC), T('a star breaks loose and comes down beside you.', '#e0c8ff')]),
                          f'execute at @s run function bm:p200/vs/land_here', f'execute if score #vst bm.bm matches 1.. at @s run function bm:p200/vs/land_here',
                          'execute if score #vstcd bm.bm matches ..120 unless score #vst bm.bm matches 1.. run ' +
                          tellraw('@s', [T('  The sky out there is restless. A Void Storm is gathering.', 'dark_purple', italic=True)])])
    fn('p200/vs/land_here', ['execute align xyz positioned ~0.5 ~ ~0.5 run function bm:p200/vs/find_start'])

    # ---------------------------------------------------------------- chests: the new places' tables, and more in the old ones
    def tbl(name, rolls, entries, extra):
        wjson(f'bm/loot_table/chests/{name}.json', {'type': 'minecraft:chest', 'pools': [{'rolls': rolls, 'entries': entries}] + extra})
    V = lambda iid, w, a=1, b=1: {'type': 'minecraft:item', 'name': f'minecraft:{iid}', 'weight': w, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(a, b)}]}
    tbl('p200_outpost', G.uni(3, 6), [V('gold_ingot', 10, 2, 6), V('blaze_rod', 6, 1, 3), V('magma_cream', 6, 2, 4), V('quartz', 8, 4, 10),
                                      V('ancient_debris', 1), V('obsidian', 4, 2, 5), E('ember_scale', G.uni(3, 8)) | {'weight': 10}],
        [{'rolls': 1, 'entries': [E('hellstar')], 'conditions': [G.chance(0.5)]}, {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.15)]},
         {'rolls': 1, 'entries': [E('token', G.uni(1, 3))], 'conditions': [G.chance(0.6)]}])
    tbl('p200_forge', G.uni(4, 7), [V('gold_block', 3, 1, 2), V('netherite_scrap', 3), V('ancient_debris', 4, 1, 2), V('blaze_rod', 6, 2, 5),
                                    V('diamond', 4, 1, 3), V('magma_block', 6, 4, 8), E('ember_scale', G.uni(6, 14)) | {'weight': 10}],
        [{'rolls': 1, 'entries': [E('hellstar', G.uni(1, 2))]}, {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.35)]},
         {'rolls': 1, 'entries': [E('sum_colossus')], 'conditions': [G.chance(0.15)]}, {'rolls': 1, 'entries': [E('medallion')], 'conditions': [G.chance(0.3)]}])
    tbl('p200_void', G.uni(3, 6), [V('ender_pearl', 8, 2, 6), V('chorus_fruit', 6, 4, 10), V('shulker_shell', 3), V('diamond', 3, 1, 2),
                                   V('end_rod', 4, 2, 4), E('void_shard', G.uni(3, 8)) | {'weight': 10}],
        [{'rolls': 1, 'entries': [E('voidstar')], 'conditions': [G.chance(0.5)]}, {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.15)]},
         {'rolls': 1, 'entries': [E('token', G.uni(1, 3))], 'conditions': [G.chance(0.6)]}])
    tbl('p200_observatory', G.uni(4, 7), [V('ender_eye', 6, 1, 3), V('amethyst_shard', 6, 3, 8), V('shulker_shell', 4, 1, 2), V('diamond', 4, 1, 3),
                                          V('experience_bottle', 6, 3, 8), V('elytra', 1), E('void_shard', G.uni(6, 14)) | {'weight': 10}],
        [{'rolls': 1, 'entries': [E('voidstar', G.uni(1, 2))]}, {'rolls': 1, 'entries': [E('heartstone')], 'conditions': [G.chance(0.35)]},
         {'rolls': 1, 'entries': [E('medallion')], 'conditions': [G.chance(0.3)]}])
    import phase39 as R39

    def hook(t):
        if f'loot/{t}' not in G.FUNCS:
            wjson(f'bm/advancement/loot/{t}.json', {'criteria': {'opened': {'trigger': 'minecraft:player_generates_container_loot',
                                                                            'conditions': {'loot_table': f'minecraft:chests/{t}'}}},
                                                    'rewards': {'function': f'bm:loot/{t}'}})
            fn(f'loot/{t}', [f'advancement revoke @s only bm:loot/{t}'])
        return G.FUNCS[f'loot/{t}']
    roll = lambda pct, then: ['execute store result score @s bm.rng run random value 1..100', f'execute if score @s bm.rng matches 1..{pct} run {then}']
    for t, (heart, star_p, cur_p, idol_p, med_p) in CHEST_PLUS.items():
        nether = t in NETHER_T
        star, cur, idol = ('hellstar', 'ember_scale', 'sum_colossus') if nether else ('voidstar', 'void_shard', 'sum_voidwalker')
        hook(t).extend(roll(heart, 'function bm:p17/heart_found') + roll(star_p, f'function bm:p200/loot/{star}') +
                       roll(cur_p, f'function bm:p200/loot/{cur}') + roll(idol_p, f'function bm:p200/loot/{idol}') + roll(med_p, give('medallion')))
    for iid, n, col in (('hellstar', 1, HC), ('voidstar', 1, VC), ('sum_colossus', 1, HC), ('sum_voidwalker', 1, VC)):
        fn(f'p200/loot/{iid}', [give(iid, n), tellraw('@s', P + [T('Treasure! ', 'gold', bold=True), T('You found a ', 'gray'), T(ITEMS[iid]['name'], col), T(' in the chest.', 'gray')])])
    for iid in ('ember_scale', 'void_shard'):
        fn(f'p200/loot/{iid}', ['execute store result score #n bm.rng run random value 2..6'] +
           [f'execute if score #n bm.rng matches {n} run {give(iid, n)}' for n in range(2, 7)])

    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second
