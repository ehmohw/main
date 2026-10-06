"""Phase 1.21 / 2.14: the Vorn Skiff, the Dawnbringer set, the Vorn Mining Drill, rat portraits, and a friendlier market.

- THE VORN SKIFF: six salvaged parts - Hull Plating, Canopy Dome and Gravitic Coil from crash-site wreckage; Navigation Core,
  Plasma Emitter and Micro-Reactor from mothership stores; the Dreadnought's armory holds any of them. With all six in your
  inventory, right-click any part to assemble the SKIFF KEY. Right-click the key to call your skiff (a saddled happy ghast in a
  saucer's hull, about four times faster) and climb in; sneak to get out - it folds itself away a few seconds later.
  While aboard: right-click fires a plasma laser; right-click while looking steeply down drops a CHARGED TNT bomb (twice the
  blast; one TNT from your inventory; 60 s recharge). It won't fly in dungeons, the Hollow Throne or a Black Market.
- THE DAWNBRINGER SET (Madame Velour): the vampire's opposite. Full set in daylight under open sky: Strength, Haste and Fire
  Resistance. SUNBURST: look straight up and hold sneak for a second to ARM it (again to disarm); while armed, hold sneak for
  1.5 s to raise a 10-second healing sun (Regeneration II for everyone and every tame creature within 8 blocks). 5 min recharge.
- THE VORN MINING DRILL (Zorp): hold right-click to drill in any direction - one block every other tick, drops fly to you.
  Runs on Red Xenite (each shard = 64 blocks, it refuels itself from your inventory; the bar is its charge). The VORN DRILL BIT
  (Zorp, the Dreadnought) upgrades it to Mk II: sneak + right-click switches 3 x 3 drilling on or off. It won't bite inside
  dungeons, crypts or a Black Market.
- RAT PORTRAITS: the five old rat sprites (chef, lucky, pirate, professor, soldier) as framed 2x2 paintings, banners and shields,
  found in dungeon chests and vaults, crash sites and motherships.
- THE MARKET: Vinny, the Fence and Old Barnaby step up to their counters (they stood two blocks back, out of reach); a lectern
  just inside the vault door, under a "Newcomers, Start Here" sign, lists every trader and what they sell.
- THE RAT GANG HQ (behind the mouse hole): Capt. Cheddarbeard now sells the WHISKER LANTERN (off hand: see in the dark, and
  every hostile creature within 20 blocks glows), and his Rat King's Crown is worth wearing: inside a Black Market the rats bow
  to their king - Hero of the Village prices from every villager trader there."""
import json, math
from nbt import snbt, B, F, Int, D, Short
import items as I
from items import item, consumable, attr, ench, T, TOTEM, ITEMS, DYNAMIC, gear, armor_attrs, ARMOR_SLOT
from useitem import hold, HOLD, HOLD_REPEAT
import mgeo, market2
import phase15 as P15

RED, GREEN, SUN = '#ff4a4a', '#7dff6a', '#ffcc33'
W, BF = market2.W, market2.BF

# ===================================================================== the Vorn Skiff
PARTS = [('skiff_hull', 'Skiff Hull Plating', 'crash'), ('skiff_dome', 'Skiff Canopy Dome', 'crash'), ('skiff_coil', 'Skiff Gravitic Coil', 'crash'),
         ('skiff_core', 'Skiff Navigation Core', 'ship'), ('skiff_emitter', 'Skiff Plasma Emitter', 'ship'), ('skiff_reactor', 'Skiff Micro-Reactor', 'ship')]
for i, (pid, name, src) in enumerate(PARTS, 1):
    item(pid, TOTEM, name, GREEN, [f'Part {i} of 6 of a Vorn Skiff.', ('Salvaged from ' + ('crash-site wreckage.' if src == 'crash' else 'mothership stores.'), 'gray'),
                                   ('With all six parts in your inventory,', 'blue'), ('right-click one to assemble the Skiff Key.', 'blue')],
         model=f'bm:{pid}', stack=16, cat='alien', comps=hold('none'))
    HOLD[pid] = 'bm:p35/skiff/assemble'
item('skiff_key', TOTEM, 'Vorn Skiff Key', GREEN,
     ['A saucer that answers to you.', ('Right-click: call your skiff and climb in.', 'blue'), ('Aboard: right-click fires a plasma laser;', 'blue'),
      ('look steeply down to drop a charged TNT bomb', 'blue'), ('(one TNT from your inventory, 60 s recharge).', 'gray'),
      ('Sneak to get out. Not in dungeons or markets.', 'dark_gray')],
     model='bm:skiff_key', stack=1, cat='alien', glint=True, bold=True, comps=hold('none'))
HOLD['skiff_key'] = 'bm:p35/skiff/use'

# ===================================================================== the Dawnbringer set (the vampire's opposite)
SOL_NAMES = {'helmet': 'Halo', 'chestplate': 'Aegis', 'leggings': 'Greaves', 'boots': 'Striders'}
for p, nm in SOL_NAMES.items():
    s = ARMOR_SLOT[p]
    gear(f'solar_{p}', f'netherite_{p}', f'Dawnbringer {nm}', SUN,
         ['Forged at first light.', ('+1 Max Health', 'blue'), ('Full set, in daylight: Strength, Haste, Fire Res.', 'dark_aqua'),
          ('Sunburst: look up + hold sneak to arm;', 'dark_aqua'), ('then hold sneak: a 10 s healing sun (5 min).', 'dark_aqua')],
         ench(protection=6, unbreaking=6, mending=1), 2, attrs=armor_attrs('netherite', p, [attr('max_health', 1, s)]),
         extra={'minecraft:trim': {'material': 'minecraft:gold', 'pattern': 'minecraft:spire'}}, custom_extra={'bm_set': 'solar'})
P15.SET_FX['solar'] = (['execute if score #tod bm.bm matches 0..12000 positioned ~ ~1.6 ~ if predicate bm:sees_sky run function bm:p35/sun/day'],
                       'minecraft:wax_on', 'particle minecraft:end_rod ~ ~2.3 ~ 0.2 0.05 0.2 0 1')

# ===================================================================== the Vorn Mining Drill
DRILL_MAX, PER_SHARD = 256, 64
item('vorn_drill', TOTEM, 'Vorn Mining Drill', RED,
     ['Bites through anything, any direction.', ('Hold right-click to drill.', 'blue'), ('Runs on Red Xenite: each shard = 64 blocks', 'blue'),
      ('(it refuels from your inventory).', 'gray'), ('A Vorn Drill Bit upgrades it to 3 x 3.', 'gray'), ('Not inside dungeons or markets.', 'dark_gray')],
     model='bm:vorn_drill', stack=1, cat='alien', glint=False, bold=True,
     comps=dict(hold('none'), **{'minecraft:max_damage': DRILL_MAX, 'minecraft:damage': 0}))
HOLD_REPEAT['vorn_drill'] = 'bm:p35/drill/use'
DYNAMIC.add('vorn_drill')
item('drill_bit', TOTEM, 'Vorn Drill Bit', RED,
     ['A spinning crown of red crystal.', ('Hold the Mining Drill in your OFF hand', 'blue'), ('and right-click this: Mk II (3 x 3).', 'blue'),
      ('Sneak + right-click a Mk II drill to switch 3 x 3.', 'gray')], model='bm:drill_bit', stack=1, cat='alien', glint=True, comps=hold('none'))
HOLD['drill_bit'] = 'bm:p35/drill/bit'

# ===================================================================== the Rat Gang HQ: the Whisker Lantern, the Crown
item('whisker_lantern', TOTEM, 'Whisker Lantern', '#c8a050',
     ['Rats see fine in the dark. Now so do you.', ('In your off hand: Night Vision, and every', 'blue'), ('hostile creature within 20 blocks glows.', 'blue')],
     model='bm:whisker_lantern', stack=1, cat='builder')
_crown = ITEMS['rat_king_crown']['comps']['minecraft:lore']
_crown[-2:-2] = [T('In a Black Market the rats bow to their king:', 'blue'), T('Hero of the Village prices from its villagers.', 'blue')]

# ===================================================================== rat portraits: paintings, banners, shields
RATS = [('chef', 'Chef Fromage', 'white', 'red'), ('lucky', 'Lucky Whiskers', 'lime', 'green'), ('pirate', 'Capt. Cheddarbeard', 'black', 'yellow'),
        ('prof', 'Prof. Whiskerton', 'brown', 'light_blue'), ('soldier', 'Sgt. Steelwhisker', 'gray', 'red')]
ART = []
for v, who, fg, bg in RATS:
    item(f'rat_portrait_{v}', 'minecraft:painting', f'Portrait of {who}', '#c8a050', ['A 2x2 painting, in a gilt frame.', ('From the Rat Gang\'s own walls.', 'gray')],
         stack=16, cat='relic', comps={'minecraft:painting/variant': f'bm:rat_{v}'})
    item(f'rat_banner_{v}', f'minecraft:{bg}_banner', f'Banner of {who}', '#c8a050', ['The Rat Gang flies its colours.'], stack=16, cat='relic',
         comps={'minecraft:banner_patterns': [{'pattern': f'bm:rat_face_{v}', 'color': fg}, {'pattern': 'minecraft:border', 'color': fg}]})
    item(f'rat_shield_{v}', 'minecraft:shield', f'Shield of {who}', '#c8a050', ['Rat Gang issue. Mostly dent-free.'], cat='gear',
         comps={'minecraft:base_color': bg, 'minecraft:banner_patterns': [{'pattern': f'bm:rat_face_{v}', 'color': fg}],
                'minecraft:enchantments': ench(unbreaking=3, mending=1)})
    ART += [f'rat_portrait_{v}', f'rat_banner_{v}', f'rat_shield_{v}']

# ===================================================================== the market: three traders step up; the newcomers' lectern
MOVES = {'arms': ((57.5, W, 21.5), (58.5, W, 21.5)), 'fence': ((44.5, W, 17.5), (44.5, W, 18.5)), 'pawn': ((29.5, W, 17.5), (29.5, W, 18.5))}
LECTERN = (34, BF + 1, 80)          # balcony, just inside the vault door, beside the way in
GUIDE = [
    [T('NEWCOMERS,\nSTART HERE\n\n', '#6a2a8a', bold=True), T('Welcome to the Black Market.\n\nWe trade in ', 'black'), T('Tokens', '#6a2a8a'),
     T(', ', 'black'), T('Medallions', '#6a2a8a'), T(' and ', 'black'), T('Trophies', '#6a2a8a'),
     T(' - monsters, Blood Moons, dungeons and Old Barnaby pay them out. Every trader below takes them.', 'black')],
    [T('PAWN ALLEY\n', '#6a2a8a', bold=True), T('(north, under the terrace)\n\n', 'dark_gray'), T('The Fence', 'black', bold=True),
     T(': keys, sealed maps, contraband, back-room deals.\n\n', 'black'), T('Old Barnaby', 'black', bold=True),
     T(': the pawnbroker - sells odd tools and buys your Black Market goods back.', 'black')],
    [T('THE PLAZA\n', '#6a2a8a', bold=True), T('(centre, by the waterfall)\n\n', 'dark_gray'), T('Madame Velour', 'black', bold=True),
     T(': armour sets, outfits, wings and cosmetics.\n\n', 'black'), T('Mike the Spikefish', 'black', bold=True), T(' lives in the pond. Be polite.\n\n', 'black'),
     T('THE STACKS ', '#6a2a8a', bold=True), T('(up on the terrace): ', 'dark_gray'), T('Prof. Whiskerton', 'black', bold=True),
     T(' - books, enchanting, lore, the Experience Flask.', 'black')],
    [T('THE FORGE PIT\n', '#6a2a8a', bold=True), T('(east)\n\n', 'dark_gray'), T("Vinny 'Two-Blades'", 'black', bold=True), T(': weapons.\n', 'black'),
     T('Sgt. Steelwhisker', 'black', bold=True), T(': armour and the armory.\n\n', 'black'), T('THE GNAWED FLAGON\n', '#6a2a8a', bold=True),
     T('Chef Fromage', 'black', bold=True), T(': feasts that buff you, Prime meats, cakes.', 'black')],
    [T('THE BLOOD ALCOVE\n', '#6a2a8a', bold=True), T('(south-east)\n', 'dark_gray'), T('The Bloodbroker', 'black', bold=True),
     T(': Blood Moon goods for Blood Crystals.\n\n', 'black'), T('THE DOCKS ', '#6a2a8a', bold=True), T('(west)\n', 'dark_gray'),
     T('Salty Sal', 'black', bold=True), T(': sea gear, the Kraken Conch, blue axolotls.\n\n', 'black'), T('THE LUCKY DEN ', '#6a2a8a', bold=True),
     T('(across the river)\n', 'dark_gray'), T('Lucky Whiskers', 'black', bold=True), T(': scratch cards, Lucky Tokens.', 'black')],
    [T('BEHIND THE NORTH WALL\n\n', '#6a2a8a', bold=True), T('The Dark Auction and the Gilded Gutter open as your ', 'black'), T('Standing', '#6a2a8a'),
     T(' grows - spend, and the market notices.\n\n', 'black'), T('And they say a pirate captain hides behind a very ', 'black'),
     T('small', 'black', italic=True), T(' door by the docks.\n\n- The Management', 'black')],
]


def extend_offers(O, offer):
    O['captain'].append(offer(('medallion', 3), ('whisker_lantern', 1)))
    O['armory'] += [offer(('trophy', n), (f'solar_{p}', 1), ('medallion', 10)) for p, n in        # 2.20: Steelwhisker, Trophies (economy.DIRECT)
                    (('helmet', 2), ('chestplate', 3), ('leggings', 3), ('boots', 2))]


def zorp_offers():
    import phase24 as R24
    k = next(i for i, o in enumerate(R24.OFFERS) if o[2][0] == 'xenite_violet')
    R24.OFFERS[k:k] = [(('power_cell', 2), ('xenite_red', 8), ('vorn_drill', 1)), (('power_cell', 3), ('xenite_red', 12), ('drill_bit', 1))]


zorp_offers()


# ===================================================================== generation
def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    import mig263
    from nbt import to_json
    tick, fast, second, load = [], [], [], []
    objs = ['bm.skl dummy', 'bm.skb dummy', 'bm.skt dummy', 'bm.solh dummy', 'bm.solt dummy', 'bm.sunc dummy', 'bm.sunt dummy']
    load += [f'scoreboard objectives add {o}' for o in objs] + ['scoreboard players set #3 bm.rng 3', 'scoreboard players set #2 bm.rng 2']
    G.OBJECTIVES += [o.split()[0] for o in objs]
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    ident = [F(0), F(0), F(0), F(1)]
    mob_ok = 'type=!#bm:ray_ignore,tag=!bm.npc,tag=!bm.frogpet,tag=!bm.wilfrey,tag=!bm.donado,tag=!bm.wil_body,tag=!bm.merc,tag=!bm.skiff,tag=!bm.skdisp'

    def add_pools(rel, pools):
        """Append pools to a loot table the earlier phases already wrote."""
        path = G.path('data', *rel.split('/'))
        obj = json.load(open(path))
        extra = mig263.convert(rel, to_json(mig263.custom_data_snbt({'type': obj.get('type', 'minecraft:chest'), 'pools': pools})))['pools']
        obj['pools'] += extra
        json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)

    # ------------------------------------------------------------------ protected places (shared by the drill, the skiff and Fortune's Favor)
    fn('p35/safe_dig', ['execute if entity @s[gamemode=adventure] run return 0', 'execute if entity @s[tag=bm.adv] run return 0',
                        'execute if dimension bm:hollow_throne run return 0',
                        'execute if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..40] run return 0',
                        'execute if entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..30] run return 0',
                        'execute if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..80] run return 0', 'return 1'])
    G.FUNCS['p34/pick/burst'][0:0] = ['execute unless function bm:p35/safe_dig run return run data remove storage bm:tmp lpp']

    # ------------------------------------------------------------------ the Vorn Skiff
    have = ' '.join(f'if items entity @s container.* {holds % p}' for p, _, _ in PARTS)
    fn('p35/skiff/assemble', [f'execute unless entity @s[type=minecraft:player] run return 0',
                              f'execute {have} run return run function bm:p35/skiff/build',
                              'scoreboard players set #n bm.rng 0'] +
       [f'execute if items entity @s container.* {holds % p} run scoreboard players add #n bm.rng 1' for p, _, _ in PARTS] +
       [title('@s', 'actionbar', [T('Skiff parts: ', 'gray'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': GREEN}, T(' of 6', 'gray')])])
    fn('p35/skiff/build', [f'clear @s {holds % p} 1' for p, _, _ in PARTS] + [give('skiff_key'), 'title @s times 10 60 20',
                           title('@s', 'subtitle', T('The parts lock together with a hum.', 'gray', italic=True)),
                           title('@s', 'title', T('VORN SKIFF', GREEN, bold=True)), 'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.4',
                           tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(' assembled a ', 'gray'), T('Vorn Skiff', GREEN, bold=True), T('!', 'gray')])])
    skiff = {'Tags': ['bm.skiff', 'bm.sknew', 'bm.seen'], 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1),
             # 2.20: the harness still makes the ghast rideable, but wears an empty equipment texture (bm:skiff_none) - no visible helmet
             'equipment': {'body': {'id': 'minecraft:lime_harness', 'count': Int(1), 'components': {'minecraft:equippable': {
                 'slot': 'body', 'asset_id': 'bm:skiff_none', 'equip_sound': 'minecraft:entity.happy_ghast.equip', 'allowed_entities': 'minecraft:happy_ghast'}}}},
             'drop_chances': {'body': F(0)},
             'attributes': [{'id': 'minecraft:flying_speed', 'base': D(0.22)}, {'id': 'minecraft:scale', 'base': D(0.6)},
                            {'id': 'minecraft:max_health', 'base': D(80)}],
             'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
             'CustomName': T('Vorn Skiff', GREEN, bold=True), 'CustomNameVisible': B(0)}
    hull = {'Tags': ['bm.skdisp', 'bm.sknew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:ufo3d'}},
            'item_display': 'fixed', 'teleport_duration': Int(2), 'brightness': {'block': Int(13), 'sky': Int(13)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(1.0), F(0)], 'scale': [F(3.0)] * 3}}
    fn('p35/skiff/riding', ['execute on vehicle if entity @s[tag=bm.skiff] run return 1', 'return 0'])
    fn('p35/skiff/use', ['execute if function bm:p35/skiff/riding if entity @s[x_rotation=55..90] run return run function bm:p35/skiff/bomb',
                         'execute if function bm:p35/skiff/riding run return run function bm:p35/skiff/laser',
                         'execute if entity @s[predicate=bm:p29/has_vehicle] run return 0',
                         'execute unless function bm:p35/skiff/allowed run return run ' + title('@s', 'actionbar', T('The skiff refuses to fly here.', 'gray')),
                         'execute unless block ~ ~1 ~ #bm:grap_pass run return run ' + title('@s', 'actionbar', T('Not enough room to call the skiff.', 'gray')),
                         'execute unless block ~ ~2 ~ #bm:grap_pass run return run ' + title('@s', 'actionbar', T('Not enough room to call the skiff.', 'gray')),
                         'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                         'execute as @e[tag=bm.skiff] if score @s bm.pid = #kp bm.pid at @s run function bm:p35/skiff/gone',
                         'execute as @e[tag=bm.skdisp] if score @s bm.pid = #kp bm.pid run kill @s',
                         f'summon minecraft:happy_ghast ~ ~0.2 ~ {snbt(skiff)}', f'summon minecraft:item_display ~ ~ ~ {snbt(hull)}',
                         'scoreboard players operation @e[tag=bm.sknew,distance=..3] bm.pid = @s bm.pid',
                         'ride @s mount @e[type=minecraft:happy_ghast,tag=bm.sknew,limit=1,sort=nearest]',
                         'tag @e[tag=bm.sknew,distance=..3] remove bm.sknew',
                         'playsound minecraft:block.beacon.power_select player @a[distance=..32] ~ ~ ~ 1 1.6', 'particle minecraft:end_rod ~ ~1 ~ 1 0.5 1 0.05 30',
                         title('@s', 'actionbar', T('Skiff online. Right-click: laser. Look down + right-click: TNT. Sneak: land.', GREEN))])
    fn('p35/skiff/allowed', ['execute if entity @s[tag=bm.adv] run return 0', 'execute if dimension bm:hollow_throne run return 0',
                             'execute if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..48] run return 0',
                             'execute if entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..30] run return 0',
                             'execute if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..80] run return 0', 'return 1'])
    fn('p35/skiff/gone', ['particle minecraft:end_rod ~ ~1 ~ 0.8 0.5 0.8 0.05 20', 'tp @s ~ -400 ~', 'kill @s'])
    tick += ['execute as @e[type=minecraft:item_display,tag=bm.skdisp] at @s run function bm:p35/skiff/follow',
             'scoreboard players remove @a[scores={bm.skl=1..}] bm.skl 1']
    fn('p35/skiff/follow', ['scoreboard players operation #kp bm.pid = @s bm.pid',
                            'execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] if score @s bm.pid = #kp bm.pid run tag @s add bm.skme',
                            'execute unless entity @e[tag=bm.skme] run return run kill @s',
                            'execute at @e[tag=bm.skme,limit=1] run tp @s ~ ~ ~ ~ 0', 'tag @e[tag=bm.skme] remove bm.skme'])
    # parked skiffs fold away; skiffs that stray near a dungeon or market land at once
    second += ['execute as @e[type=minecraft:happy_ghast,tag=bm.skiff] at @s run function bm:p35/skiff/watch',
               'scoreboard players remove @a[scores={bm.skb=1..}] bm.skb 1']
    fn('p35/skiff/watch', ['execute at @s if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..40] run return run function bm:p35/skiff/refuse',
                           'execute at @s if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..72] run return run function bm:p35/skiff/refuse',
                           'execute at @s if dimension bm:hollow_throne run return run function bm:p35/skiff/refuse',
                           'execute on passengers if entity @s[type=minecraft:player] run return run scoreboard players set @e[type=minecraft:happy_ghast,tag=bm.skiff,limit=1,sort=nearest] bm.skt 0',
                           'scoreboard players add @s bm.skt 1', 'execute if score @s bm.skt matches 4.. run function bm:p35/skiff/gone'])
    fn('p35/skiff/refuse', ['execute on passengers if entity @s[type=minecraft:player] run ' + title('@s', 'actionbar', T('Strange wards scramble the skiff - it sets you down.', 'red')),
                            'execute on passengers run ride @s dismount', 'function bm:p35/skiff/gone'])
    # plasma laser (from your eyes, 64 blocks)
    fn('p35/skiff/laser', ['execute if score @s bm.skl matches 1.. run return 0', 'scoreboard players set @s bm.skl 8', 'tag @s add bm.shooter',
                           'scoreboard players set #rr bm.rng 128', 'playsound minecraft:entity.guardian.attack player @a[distance=..32] ~ ~ ~ 1 1.8',
                           'execute anchored eyes positioned ^ ^ ^1.5 run function bm:p35/skiff/beam', 'tag @s remove bm.shooter'])
    fn('p35/skiff/beam', ['particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.2} ~ ~ ~ 0 0 0 0 1 force @a[distance=..96]',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.2 0.2 0.2 0.3 12',
                          f'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,{mob_ok},tag=!bm.shooter] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p35/skiff/zap',
                          'scoreboard players remove #rr bm.rng 1', 'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p35/skiff/beam'])
    fn('p35/skiff/zap', [f'execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,{mob_ok},tag=!bm.shooter,limit=1,sort=nearest] run damage @s 10 bm:plasma by @a[tag=bm.shooter,limit=1]',
                         'particle minecraft:dust{color:[0.5,1.0,0.35],scale:2.0} ~ ~ ~ 0.3 0.3 0.3 0 25 force @a[distance=..96]'])
    # the charged TNT bomb
    tnt = {'fuse': Short(50), 'explosion_power': F(8.0), 'Motion': [D(0), D(-0.6), D(0)], 'Tags': ['bm.skbomb']}
    fn('p35/skiff/bomb', ['execute if score @s bm.skb matches 1.. run return run ' + title('@s', 'actionbar', [T('Bomb bay recharging: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.skb'}, 'color': 'white'}, T(' s', 'gray')]),
                          'execute store result score #t bm.rng run clear @s minecraft:tnt 0',
                          'execute if score #t bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('The bomb bay is empty - carry TNT.', 'red')),
                          'clear @s minecraft:tnt 1', 'scoreboard players set @s bm.skb 60',
                          f'execute on vehicle at @s run summon minecraft:tnt ~ ~-1.5 ~ {snbt(tnt)}',
                          'playsound minecraft:entity.tnt.primed player @a[distance=..32] ~ ~ ~ 1 0.6', 'playsound minecraft:block.beacon.deactivate player @a[distance=..32] ~ ~ ~ 1 1.8',
                          title('@s', 'actionbar', T('Charged bomb away!', RED, bold=True))])

    # ------------------------------------------------------------------ the Dawnbringer set: daylight, Sunburst
    fn('p35/sun/day', ['effect give @s minecraft:strength 2 0 true', 'effect give @s minecraft:haste 2 0 true', 'effect give @s minecraft:fire_resistance 2 0 true'])
    tick += ['execute as @a[gamemode=!spectator,scores={bm.solh=1..}] unless predicate bm:p20/sneaking run scoreboard players set @s bm.solh 0',
             'execute as @a[gamemode=!spectator,scores={bm.solt=1..}] unless predicate bm:p20/sneaking run scoreboard players set @s bm.solt 0',
             'execute as @a[gamemode=!spectator] if predicate bm:p20/sneaking if function bm:sets/has/solar at @s run function bm:p35/sun/sneak']
    fn('p35/sun/sneak', ['execute if entity @s[x_rotation=-90..-70] run return run function bm:p35/sun/salute', 'scoreboard players set @s bm.solt 0',
                         'execute unless entity @s[tag=bm.sunarm] run return 0', 'scoreboard players add @s bm.solh 1',
                         'execute if score @s bm.solh matches 30 run function bm:p35/sun/try'])
    fn('p35/sun/salute', ['scoreboard players set @s bm.solh 0', 'scoreboard players add @s bm.solt 1', 'execute unless score @s bm.solt matches 20 run return 0',
                          'execute if entity @s[tag=bm.sunarm] run return run function bm:p35/sun/disarm', 'tag @s add bm.sunarm',
                          'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.8 1.6', 'particle minecraft:end_rod ~ ~2 ~ 0.4 0.4 0.4 0.05 20',
                          title('@s', 'actionbar', T('Sunburst ARMED - hold sneak to call the sun. (Look up + sneak again to disarm.)', SUN))])
    fn('p35/sun/disarm', ['tag @s remove bm.sunarm', 'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.8 1.4',
                          title('@s', 'actionbar', T('Sunburst disarmed - sneaking is just sneaking again.', 'gray'))])
    fn('p35/sun/try', ['execute if score @s bm.sunc matches 1.. run return run ' + title('@s', 'actionbar', [T('The sun is still rising: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.sunc'}, 'color': SUN}, T(' s', 'gray')]),
                       'scoreboard players set @s bm.sunc 300', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.sunburst","bm.sunnew"]}',
                       'scoreboard players set @e[tag=bm.sunnew,limit=1] bm.sunt 10', 'tag @e[tag=bm.sunnew] remove bm.sunnew',
                       'playsound minecraft:block.beacon.power_select player @a[distance=..24] ~ ~ ~ 1.2 1.8', 'playsound minecraft:item.totem.use player @a[distance=..24] ~ ~ ~ 0.5 1.6',
                       title('@s', 'actionbar', T('SUNBURST! (10 s, recharges in 5 min)', SUN, bold=True))])
    wjson('bm/tags/entity_type/p35_allies.json', {'values': ['minecraft:wolf', 'minecraft:cat', 'minecraft:parrot', 'minecraft:horse', 'minecraft:donkey', 'minecraft:mule',
                                                             'minecraft:llama', 'minecraft:camel', 'minecraft:iron_golem', 'minecraft:villager', 'minecraft:allay',
                                                             'minecraft:fox', 'minecraft:axolotl', 'minecraft:happy_ghast', 'minecraft:nautilus', 'minecraft:snow_golem']})
    second += ['execute as @e[type=minecraft:marker,tag=bm.sunburst] at @s run function bm:p35/sun/pulse',
               'scoreboard players remove @a[scores={bm.sunc=1..}] bm.sunc 1']
    ring = [f'particle minecraft:dust{{color:[1.0,0.85,0.3],scale:1.5}} ~{8 * math.cos(math.radians(a)):.2f} ~0.2 ~{8 * math.sin(math.radians(a)):.2f} 0 0.1 0 0 1 force @a[distance=..48]'
            for a in range(0, 360, 15)]
    fn('p35/sun/pulse', ['effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 3 1 true', 'effect give @e[type=#bm:p35_allies,distance=..8] minecraft:regeneration 3 1 true',
                         'particle minecraft:end_rod ~ ~3 ~ 0.3 1.5 0.3 0.02 8', 'particle minecraft:wax_on ~ ~1 ~ 4 0.8 4 0 25'] + ring +
       ['scoreboard players remove @s bm.sunt 1', 'execute if score @s bm.sunt matches ..0 run kill @s'])

    # ------------------------------------------------------------------ the Vorn Mining Drill
    drill = holds % 'vorn_drill'
    wjson('bm/tags/block/p35_nodrill.json', {'values': ['#bm:p34_nodig', 'minecraft:barrier', 'minecraft:command_block', 'minecraft:chain_command_block',
                                                        'minecraft:repeating_command_block', 'minecraft:structure_block', 'minecraft:jigsaw', 'minecraft:end_portal',
                                                        'minecraft:end_gateway', 'minecraft:nether_portal', 'minecraft:light', 'minecraft:furnace', 'minecraft:blast_furnace',
                                                        'minecraft:smoker', 'minecraft:hopper', 'minecraft:dropper', 'minecraft:dispenser', 'minecraft:brewing_stand',
                                                        'minecraft:crafter', 'minecraft:decorated_pot', 'minecraft:chiseled_bookshelf', 'minecraft:lectern',
                                                        'minecraft:jukebox', 'minecraft:beacon', 'minecraft:conduit', 'minecraft:respawn_anchor', 'minecraft:moving_piston',
                                                        'minecraft:piston_head', 'minecraft:test_block', 'minecraft:test_instance_block']})
    fn('p35/drill/use', ['execute unless items entity @s weapon.mainhand ' + drill + ' run return 0',
                         'execute if score #first bm.hnow matches 1 if predicate bm:p20/sneaking run return run function bm:p35/drill/toggle',
                         'execute if predicate bm:p20/sneaking run return 0',
                         'execute unless function bm:p35/safe_dig run return run execute if score #first bm.hnow matches 1 run ' + title('@s', 'actionbar', T('The drill won\'t bite here.', 'gray')),
                         'execute store result score #gt bm.rng run time query gametime', 'scoreboard players operation #gt bm.rng %= #2 bm.rng',
                         'execute unless score #gt bm.rng matches 0 run return 0',
                         'execute store result score #dd bm.rng run data get entity @s SelectedItem.components."minecraft:damage"',
                         f'scoreboard players set #ch bm.rng {DRILL_MAX}', 'scoreboard players operation #ch bm.rng -= #dd bm.rng',
                         'execute if score #ch bm.rng matches ..8 run function bm:p35/drill/refuel',
                         'execute if score #ch bm.rng matches ..0 run return 0',
                         'scoreboard players set #mined bm.rng 0', 'tag @s add bm.driller', 'scoreboard players set #ray bm.rng 25',
                         'execute anchored eyes positioned ^ ^ ^ run function bm:p35/drill/ray', 'tag @s remove bm.driller',
                         'execute if score #mined bm.rng matches 0 run return 0',
                         'scoreboard players operation #ch bm.rng -= #mined bm.rng', 'execute if score #ch bm.rng matches ..-1 run scoreboard players set #ch bm.rng 0',
                         f'scoreboard players set #nd bm.rng {DRILL_MAX}', 'scoreboard players operation #nd bm.rng -= #ch bm.rng',
                         'execute store result storage bm:tmp drl.d int 1 run scoreboard players get #nd bm.rng', 'function bm:p35/drill/write with storage bm:tmp drl',
                         'playsound minecraft:block.grindstone.use player @a[distance=..16] ~ ~ ~ 0.4 1.8'])
    fn('p35/drill/write', ['$item modify entity @s weapon.mainhand {function:"minecraft:set_components",components:{"minecraft:damage":$(d)}}'])
    red = holds % 'xenite_red'
    fn('p35/drill/refuel', ['execute store result score #r bm.rng run clear @s ' + red + ' 0',
                            'execute if score #r bm.rng matches 0 if score #ch bm.rng matches ..0 run return run ' + title('@s', 'actionbar', T('The drill is dry - carry Red Xenite.', 'red')),
                            'execute if score #r bm.rng matches 0 run return 0',
                            'clear @s ' + red + ' 1', f'scoreboard players add #ch bm.rng {PER_SHARD}',
                            'playsound minecraft:block.respawn_anchor.charge player @s ~ ~ ~ 0.6 1.6', title('@s', 'actionbar', T('The drill drinks a Red Xenite shard. (+64)', RED))])
    fn('p35/drill/ray', ['execute unless block ~ ~ ~ #bm:grap_pass align xyz run return run function bm:p35/drill/hit',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p35/drill/ray'])
    on3 = '*[minecraft:custom_data~{bm:"vorn_drill",bm_3x3:1b}]'
    fn('p35/drill/hit', [f'execute unless items entity @s weapon.mainhand {on3} run return run function bm:p35/drill/dig',
                         'execute if entity @s[x_rotation=50..90] run return run function bm:p35/drill/plane_h',
                         'execute if entity @s[x_rotation=-90..-50] run return run function bm:p35/drill/plane_h',
                         'execute if entity @s[y_rotation=-45..45] run return run function bm:p35/drill/plane_x',
                         'execute if entity @s[y_rotation=135..180] run return run function bm:p35/drill/plane_x',
                         'execute if entity @s[y_rotation=-180..-135] run return run function bm:p35/drill/plane_x',
                         'function bm:p35/drill/plane_z'])
    for nm, offs in (('h', [(a, 0, b) for a in (-1, 0, 1) for b in (-1, 0, 1)]), ('x', [(a, b, 0) for a in (-1, 0, 1) for b in (-1, 0, 1)]),
                     ('z', [(0, b, a) for a in (-1, 0, 1) for b in (-1, 0, 1)])):
        fn(f'p35/drill/plane_{nm}', [f'execute positioned ~{dx} ~{dy} ~{dz} run function bm:p35/drill/dig' for (dx, dy, dz) in offs])
    fn('p35/drill/dig', ['execute if block ~ ~ ~ #bm:grap_pass run return 0', 'execute if block ~ ~ ~ #bm:p35_nodrill run return 0',
                         'execute if score #mined bm.rng >= #ch bm.rng run return 0',
                         'loot spawn ~0.5 ~0.5 ~0.5 mine ~ ~ ~ minecraft:netherite_pickaxe', 'setblock ~ ~ ~ minecraft:air',
                         'particle minecraft:dust{color:[1.0,0.3,0.25],scale:1.0} ~0.5 ~0.5 ~0.5 0.3 0.3 0.3 0 4',
                         'execute positioned ~0.5 ~0.5 ~0.5 as @e[type=minecraft:item,distance=..1.2] run tp @s @a[tag=bm.driller,limit=1]',
                         'scoreboard players add #mined bm.rng 1'])
    fn('p35/drill/toggle', ['execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{bm_up:1b}] run return run ' + title('@s', 'actionbar', T('Install a Vorn Drill Bit for 3 x 3 drilling.', 'gray')),
                            f'execute if items entity @s weapon.mainhand {on3} run return run function bm:p35/drill/off',
                            'item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:"{bm_3x3:1b}"}',
                            'playsound minecraft:block.note_block.pling player @s ~ ~ ~ 1 1.6', title('@s', 'actionbar', T('Drill: 3 x 3 ON', RED))])
    fn('p35/drill/off', ['item modify entity @s weapon.mainhand {function:"minecraft:set_custom_data",tag:"{bm_3x3:0b}"}',
                         'playsound minecraft:block.note_block.pling player @s ~ ~ ~ 1 0.8', title('@s', 'actionbar', T('Drill: single block', 'gray'))])
    fn('p35/drill/bit', ['execute unless items entity @s weapon.offhand ' + drill + ' run return run ' + title('@s', 'actionbar', T('Hold the Mining Drill in your OFF hand.', 'gray')),
                         'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm_up:1b}] run return run ' + title('@s', 'actionbar', T('That drill already has a bit.', 'gray')),
                         'item modify entity @s weapon.offhand {function:"minecraft:set_custom_data",tag:"{bm_up:1b,bm_3x3:1b}"}',
                         'item modify entity @s weapon.offhand ' + snbt({'function': 'minecraft:set_lore', 'mode': 'insert', 'offset': Int(0), 'lore': [T('Mk II: 3 x 3 bit installed', RED, bold=True)]}),
                         'clear @s ' + holds % 'drill_bit' + ' 1', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.8 1.4',
                         title('@s', 'actionbar', T('Vorn Mining Drill Mk II! Sneak + right-click switches 3 x 3.', RED, bold=True))])

    # ------------------------------------------------------------------ the Whisker Lantern, the Rat King's Crown
    second += ['execute as @a[gamemode=!spectator] if items entity @s weapon.offhand ' + holds % 'whisker_lantern' + ' at @s run function bm:p35/whisker',
               'execute as @a[gamemode=!spectator] if items entity @s armor.head ' + holds % 'rat_king_crown' + ' at @s if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..90] run effect give @s minecraft:hero_of_the_village 3 0 true']
    fn('p35/whisker', ['effect give @s minecraft:night_vision 13 0 true', 'effect give @e[type=#bm:hostile,distance=..20] minecraft:glowing 2 0 true'])

    # ------------------------------------------------------------------ rat portraits (painting variants, banner patterns) and their loot
    for v, who, fg, bg in RATS:
        wjson(f'bm/painting_variant/rat_{v}.json', {'asset_id': f'bm:rat_{v}', 'width': Int(2), 'height': Int(2),
                                                    'title': T(f'Portrait of {who}', 'yellow'), 'author': T('The Rat Gang', 'gray')})
        wjson(f'bm/banner_pattern/rat_face_{v}.json', {'asset_id': f'bm:rat_face_{v}', 'translation_key': f'block.bm.banner.rat_face_{v}'})
    wjson('bm/loot_table/p35/rat_art.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry(a) for a in ART]}]})
    art = lambda p: {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': 'bm:p35/rat_art'}], 'conditions': [G.chance(p)]}
    part = lambda ids, p: {'rolls': 1, 'entries': [G.loot_entry(i) for i in ids], 'conditions': [G.chance(p)]}
    crash_parts = [p for p, _, s in PARTS if s == 'crash']
    ship_parts = [p for p, _, s in PARTS if s == 'ship']
    add_pools('bm/loot_table/p32/crash_wreck.json', [art(0.15), part(crash_parts, 0.12)])
    add_pools('bm/loot_table/p32/mothership_stores.json', [art(0.06), part(ship_parts, 0.05)])
    add_pools('bm/loot_table/p32/dread_stores.json', [art(0.1), part([p for p, _, _ in PARTS], 0.15)])
    add_pools('bm/loot_table/p32/dread_armory.json', [part([p for p, _, _ in PARTS], 1.0), part([p for p, _, _ in PARTS], 0.5),
                                                       {'rolls': 1, 'entries': [G.loot_entry('drill_bit')], 'conditions': [G.chance(0.3)]}])
    if G.PHASE2:
        from p2.config import D as PD
        for d in PD:
            add_pools(f'bm/loot_table/p2/{d}/hidden.json', [art(0.5)])
            add_pools(f'bm/loot_table/p2/{d}/vault.json', [art(0.15)])

    # ------------------------------------------------------------------ the market, second patch (every market, new or old)
    rel = mgeo.rel
    def delta(a, b):
        # ^ offsets are measured from wherever the command is already positioned - so the step from a to b, not b itself
        f = lambda v: ('%.3f' % v).rstrip('0').rstrip('.') if abs(v) > 1e-9 else ''
        return f'^{f(b[0] - a[0])} ^{f(b[1] - a[1])} ^{f(b[2] - a[2])}'
    for k, (a, b) in MOVES.items():
        for c in (a, b): mgeo.need_air(c, f'{k} stand')
    lx, ly, lz = LECTERN
    mgeo.need_floor((lx + 0.5, ly, lz + 0.5), 'public', 'the newcomers\' lectern')
    book = {'id': 'minecraft:written_book', 'count': Int(1), 'components': {'minecraft:written_book_content': {
        'title': 'Newcomers, Start Here', 'author': 'The Management', 'pages': [{'text': '', 'extra': pg} for pg in GUIDE]}}}
    lnbt = snbt({'Book': book, 'Page': Int(0)})
    sign = {'Tags': ['bm.newcomer', 'bm.npc'], 'billboard': 'center', 'see_through': B(0), 'shadow': B(1), 'background': Int(0x70000000),
            'brightness': {'block': Int(15), 'sky': Int(15)}, 'line_width': Int(200), 'alignment': 'center',
            'text': [T('Newcomers,\n', '#ffd23f', bold=True), T('Start Here', '#ffd23f', bold=True), T('\n(read the book)', 'gray')],
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0.8)] * 3}}
    lpos = rel((lx + 0.5, ly + 0.5, lz + 0.5))
    # the lectern faces template east (+x = the marker's left): which world direction that is depends on the market's turn
    face = [('-45..45', 'east'), ('45..135', 'south'), ('135..180', 'west'), ('-180..-135', 'west'), ('-135..-45', 'north')]
    patch = [
        f'execute positioned {rel(a)} as @e[tag=bm.npc_{k},distance=..1.2] positioned {delta(a, b)} run tp @s ~ ~ ~' for k, (a, b) in MOVES.items()] + [
        f'execute if entity @s[y_rotation={r}] positioned {lpos} unless block ~ ~ ~ minecraft:lectern if block ~ ~ ~ #minecraft:replaceable run setblock ~ ~ ~ minecraft:lectern[facing={f},has_book=true]{lnbt}' for r, f in face] + [
        f'execute positioned {rel((lx + 0.5, ly + 1.75, lz + 0.5))} unless entity @e[type=minecraft:text_display,tag=bm.newcomer,distance=..2] run summon minecraft:text_display ~ ~ ~ {snbt(sign)}']
    fn('p35/patch', patch)
    # idempotent, so it simply runs every 10 s near players (a trader whose entity loads late still gets moved)
    mk = 'execute if score #p35t bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.mkt] at @s rotated as @s'
    second += ['scoreboard players add #p35t bm.rng 1', 'execute if score #p35t bm.rng matches 10.. run scoreboard players set #p35t bm.rng 0',
               mk + f' if entity @a[distance=..64] if loaded {lpos} if loaded {rel((57, W, 21))} if loaded {rel((29, W, 17))} run function bm:p35/patch']

    # ------------------------------------------------------------------ Sunken Thrones already in a world: the tower ladder (2.14 layout fix)
    if G.PHASE2:
        dirs = [('-45..45', 'north'), ('45..135', 'east'), ('135..180', 'south'), ('-180..-135', 'south'), ('-135..-45', 'west')]
        tl = ['tag @s add bm.tlad2']
        for r, f in dirs:
            tl += [f'execute if entity @s[y_rotation={r}] positioned ^1 ^{y - 35} ^-2 if block ~ ~ ~ #bm:p35_open run setblock ~ ~ ~ minecraft:ladder[facing={f}]'
                   for y in range(23, 37)]
            tl += [f'execute if entity @s[y_rotation={r}] positioned ^1 ^{y - 35} ^-3 if block ~ ~ ~ #bm:p35_open run setblock ~ ~ ~ minecraft:ladder[facing={f}]'
                   for y in range(3, 23)]
        tl += [f'execute positioned {p} if block ~ ~ ~ #bm:p35_open run setblock ~ ~ ~ minecraft:{b}' for p, b in
               (('^ ^-1 ^-2', 'dark_prismarine'), ('^-1 ^-1 ^-2', 'dark_prismarine'), ('^-1 ^ ^-2', 'sea_lantern'))]
        fn('p35/tide_ladder', tl)
        wjson('bm/tags/block/p35_open.json', {'values': ['#minecraft:replaceable', 'minecraft:water', 'minecraft:seagrass', 'minecraft:tall_seagrass',
                                                          'minecraft:kelp', 'minecraft:kelp_plant', 'minecraft:bubble_column']})
        second.append('execute as @e[type=minecraft:marker,tag=bm.entr,tag=bm.d_tide,tag=!bm.tlad2] at @s rotated as @s if loaded ^1 ^-32 ^-3 run function bm:p35/tide_ladder')

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    I_ = {}
    G_, g_, D_, K = '#7dff6a', '#3a9a3a', '#2a2a32', '#6a6a78'
    I_['skiff_hull'] = grid(['................', '................', '......KKKK......', '....KKSSSSKK....', '...KSSSSSSSSK...', '..KSSGSSSSGSSK..', '..KSSSSSSSSSSK..',
                              '...KKKKKKKKKK...', '....g.g..g.g....', '................', '................', '................', '................', '................',
                              '................', '................'], dict(K=K, S='#a8a8b8', G=G_, g=g_))
    I_['skiff_dome'] = grid(['................', '................', '.....LLLLLL.....', '....LCCCCCCL....', '...LCCWCCCCCL...', '...LCWCCCCCCL...', '...LCCCCCCCCL...',
                              '...KKKKKKKKKK...', '................', '................', '................', '................', '................', '................',
                              '................', '................'], dict(L='#5a9a9a', C='#9fe8e0', W='#ffffff', K=K))
    I_['skiff_coil'] = grid(['................', '......KKKK......', '.....KGGGGK.....', '.....KgKKgK.....', '.....KGGGGK.....', '.....KgKKgK.....', '.....KGGGGK.....',
                              '.....KgKKgK.....', '.....KGGGGK.....', '.....KgKKgK.....', '.....KGGGGK.....', '......KKKK......', '................', '................',
                              '................', '................'], dict(K=K, G=G_, g=g_))
    I_['skiff_core'] = grid(['................', '................', '....KKKKKKKK....', '....KDDDDDDK....', '....KDGDDGDK....', '....KDDGGDDK....', '....KDDGGDDK....',
                              '....KDGDDGDK....', '....KDDDDDDK....', '....KKKKKKKK....', '.....g....g.....', '................', '................', '................',
                              '................', '................'], dict(K=K, D=D_, G=G_, g=g_))
    I_['skiff_emitter'] = grid(['................', '................', '..........GG....', '.........GWWG...', '........KGWWG...', '.......KKKGG....', '......KKK.......',
                                 '.....KKK........', '....KKK.........', '...KKK..........', '..KKK...........', '..KK............', '................', '................',
                                 '................', '................'], dict(K=K, G=G_, W='#e8ffe0'))
    I_['skiff_reactor'] = grid(['................', '.....KKKKKK.....', '....KRRRRRRK....', '....KRrrrrRK....', '....KRrWWrRK....', '....KRrWWrRK....', '....KRrrrrRK....',
                                 '....KRRRRRRK....', '.....KKKKKK.....', '......K..K......', '................', '................', '................', '................',
                                 '................', '................'], dict(K=K, R=RED, r='#ff9a7a', W='#fff0e0'))
    I_['skiff_key'] = grid(['................', '................', '.....SSSSSS.....', '...SSGSSSSGSS...', '..SSSSSSSSSSSS..', '...KKKKKKKKKK...', '......gKKg......',
                             '.......KK.......', '.......KK.......', '.......KKK......', '.......KK.......', '.......KKK......', '.......KK.......', '................',
                             '................', '................'], dict(S='#a8a8b8', G=G_, K=K, g=g_))
    I_['vorn_drill'] = grid(['................', '..........RR....', '.........RrrR...', '........RrrrR...', '.......RrrrR....', '......KKrrR.....', '.....KKKKR......',
                              '....KKKKK.......', '...KSSKK........', '..KSSSK.........', '..KSSK..........', '..KKK...........', '................', '................',
                              '................', '................'], dict(R=RED, r='#ff9a7a', K=K, S='#a8a8b8'))
    I_['drill_bit'] = grid(['................', '................', '.......RR.......', '......RrrR......', '.....RrWWrR.....', '.....RrWWrR.....', '......RrrR......',
                             '.......KK.......', '.......KK.......', '......KKKK......', '................', '................', '................', '................',
                             '................', '................'], dict(R=RED, r='#ff9a7a', W='#fff0e0', K=K))
    I_['whisker_lantern'] = grid(['................', '.......KK.......', '......K..K......', '.....KKKKKK.....', '.....KYYYYK.....', '....wKYOOYKw....', '...w.KYOOYK.w...',
                                   '....wKYYYYKw....', '.....KKKKKK.....', '................', '................', '................', '................', '................',
                                   '................', '................'], dict(K='#3a2a1a', Y='#ffcf5a', O='#fff3c0', w='#d8d8d8'))
    for k, v in I_.items(): R.ICONS[k] = v
    R.HANDHELD_EXTRA.add('vorn_drill')
    R.POST.append(rp_post)


def rp_post(R):
    """Rat portraits (2x2 paintings, 128 px - an HD painting - in a gilt frame), the rat-face banner and shield patterns, their names."""
    from PIL import Image
    import os
    src = lambda v: Image.open(R.p('assets', 'bm', 'textures', 'item', f'rat_{v}.png')).convert('RGBA')
    backs = {'chef': '#3a2a22', 'lucky': '#1f3a22', 'pirate': '#1a2a3a', 'prof': '#2a223a', 'soldier': '#2a2a2a'}
    for v, who, fg, bg in RATS:
        sp = src(v)
        N, FR = 128, 8
        im = Image.new('RGBA', (N, N), R.hexc('#7a5a20'))
        inner = Image.new('RGBA', (N - 2 * FR, N - 2 * FR), R.hexc(backs[v]))
        h = (N - 2 * FR) / 2
        for y in range(N - 2 * FR):                             # a soft vignette behind the sitter
            for x in range(N - 2 * FR):
                d = math.hypot(x - h, y - h * 0.9) / (h * 1.4)
                c = inner.getpixel((x, y))
                inner.putpixel((x, y), tuple(min(255, int(c[i] * (1.3 - 0.7 * d))) for i in range(3)) + (255,))
        im.paste(inner, (FR, FR))
        for i in range(N):                                      # gilt frame: bright outer edge, a bevel line, a dark lip at the canvas
            for (x, y) in ((i, 0), (i, 1), (i, N - 1), (i, N - 2), (0, i), (1, i), (N - 1, i), (N - 2, i)): im.putpixel((x, y), R.hexc('#e8c870'))
            for (x, y) in ((i, 4), (i, N - 5), (4, i), (N - 5, i)): im.putpixel((x, y), R.hexc('#c8a050'))
            for (x, y) in ((i, FR - 1), (i, N - FR), (FR - 1, i), (N - FR, i)):
                if FR - 1 <= i <= N - FR: im.putpixel((x, y), R.hexc('#3a2410'))
        big = sp.resize((96, 96), Image.NEAREST)
        im.paste(big, (16, 20), big)
        im.save(R.p('assets', 'bm', 'textures', 'painting', f'rat_{v}.png'))
        # banner/shield masks: white, shaded by the sprite's brightness (the game tints them with the pattern colour)
        def mask(w, h):
            m = sp.resize((w, h), Image.NEAREST)
            out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            for y in range(h):
                for x in range(w):
                    r, g, b, a = m.getpixel((x, y))
                    if a < 128: continue
                    l = (0.3 * r + 0.59 * g + 0.11 * b) / 255
                    out.putpixel((x, y), (255, 255, 255, int(255 * (0.35 + 0.65 * l))))
            return out
        ban = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        m = mask(20, 20)
        ban.paste(m, (1, 11), m); ban.paste(m.transpose(Image.FLIP_LEFT_RIGHT), (22, 11), m.transpose(Image.FLIP_LEFT_RIGHT))
        ban.save(R.p('assets', 'bm', 'textures', 'entity', 'banner', f'rat_face_{v}.png'))
        sh = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        m = mask(10, 10)
        sh.paste(m, (2, 7), m)
        sh.save(R.p('assets', 'bm', 'textures', 'entity', 'shield', f'rat_face_{v}.png'))
    lp = R.p('assets', 'bm', 'lang', 'en_us.json')
    lang = json.load(open(lp)) if os.path.exists(lp) else {}
    for v, who, fg, bg in RATS:
        for c in ('white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime', 'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue', 'brown',
                  'green', 'red', 'black'):
            lang[f'block.bm.banner.rat_face_{v}.{c}'] = ' '.join(w.capitalize() for w in c.split('_')) + f' {who}'
    json.dump(lang, open(lp, 'w'), indent=1)
