"""Phase 1.12: Lucky Nights, an Overworld-only Blood Moon, the Bloodforge Sigil's new rules, and two wandering field
traders - the Ember Rat (the Nether) and the Void Rat (the outer End) - with their own currencies and goods.

- Lucky Night: at dusk on any day that is NOT a Blood Moon there is a 1% chance; from 13000 to 23000 every tiered
  hostile mob in the Overworld rolls on a much luckier table (Lucky 10%, was 0.6%). A forced Blood Moon cancels it.
- Blood Moon titles, sounds and bossbar only reach players in the Overworld (its mobs already were Overworld-only).
- Field rats: an invisible, frozen wandering trader carrying the offers, with a posable 3D rat display on top
  (same pattern as the market rats, so they animate and turn to face you). Each minute every player in the Nether
  (or the End, outside the main island) has a 1 in 25 chance to have one set up shop nearby - one of each at a time.
  They pack up after 20 minutes.
Importing registers the items; generate(G) runs after phase21.generate."""
from nbt import snbt, B, F, Int, D
from items import item, consumable, T, TOTEM

HANDHELD = {'fire_charge_launcher', 'levitation_wand'}
WADE_TICKS = 1200          # Lava Wader: 60 s
FIELD_LIFE = 1200          # field rats stay 20 min (seconds)
SPAWN_ODDS = 25            # per player, per minute
END_SAFE = 700             # no Void Rat inside +-700 of the End's centre (the dragon island)


def _use(sound, secs=0.8, anim='none'):
    return {'minecraft:consumable': consumable(secs, anim, sound, False)}


# ===================================================================== ITEMS
item('ember_scale', TOTEM, 'Ember Scale', '#ff7a1a',
     ['Still glowing. Shed by the Nether\'s fiercest.', ('Dropped in the Nether by blazes, wither skeletons,', 'gray'),
      ('magma cubes, ghasts, hoglins and piglin brutes.', 'gray'), ('Spend it with an Ember Rat.', 'gold')],
     model='bm:ember_scale', stack=64, cat='currency')
item('void_shard', TOTEM, 'Void Shard', '#b05cff',
     ['A splinter of nothing, cold to the touch.', ('Dropped in the End by endermen and shulkers.', 'gray'),
      ('Spend it with a Void Rat.', 'light_purple')],
     model='bm:void_shard', stack=64, cat='currency')

item('lava_wader_charm', TOTEM, 'Lava Wader Charm', '#ff7a1a',
     ['Use it: for 60 seconds, lava crusts over', 'into magma under your feet - and cools', 'back into lava after you pass.',
      ('Fire Resistance included.', 'blue'), ("Doesn't work in dungeons.", 'dark_gray')],
     model='bm:lava_wader_charm', stack=16, cat='rat_goods', comps=_use('minecraft:block.lava.extinguish'))
item('skin_fire_launcher', TOTEM, 'Fire Charge Launcher Skin', '#ff7a1a',
     ['Hold Snake Eyes in your OFF hand, then use', 'this to turn it into a Fire Charge Launcher.', 'Use it again to turn it back.',
      ('Reusable - the skin comes right back.', 'blue'), ('Cosmetic only.', 'dark_gray')],
     model='bm:skin_fire_launcher', stack=1, cat='rat_goods', comps=_use('minecraft:item.firecharge.use'))

item('pearl_of_return', TOTEM, 'Pearl of Return', '#7fffd4',
     ['Use it to return to where you last died.', ('One use. Not in dungeons or the Hollow.', 'gray')],
     model='bm:pearl_of_return', glint=True, stack=16, cat='rat_goods', comps=_use('minecraft:entity.enderman.teleport', 1.2))
item('elytra_repair_kit', TOTEM, 'Elytra Repair Kit', '#9aa6c8',
     ['Wear a damaged elytra (or hold it in your', 'OFF hand) and use this to fully mend it.', ('One use.', 'gray')],
     model='bm:elytra_repair_kit', stack=16, cat='rat_goods', comps=_use('minecraft:item.armor.equip_elytra', 1.2))
item('levitation_wand', 'minecraft:carrot_on_a_stick', 'Levitation Wand', '#c08bff',
     ['Right-click: a short, floaty hop straight up,', 'then a soft landing.', ('Only works from solid ground.', 'blue'), ('2 second recharge.', 'gray'),
      ("Doesn't work in dungeons.", 'dark_gray')],
     model='bm:levitation_wand', stack=1, cat='rat_goods')
item('chorus_compass', 'minecraft:compass', 'Chorus Compass', '#c08bff',
     ['Use it in the End to point it at the', 'nearest End City. Use it again to re-tune.', ('Only hums in the End.', 'gray')],
     stack=1, cat='rat_goods', comps=_use('minecraft:block.chorus_flower.grow', 1.0))
item('void_rat_statue', TOTEM, 'Void Rat Statue', '#b05cff',
     ['A little shrine to the rat between worlds.', ('Use it to place it. Punch it to pick it up,', 'gray'),
      ('right-click it to turn it.', 'gray')],
     model='bm:statue_void_rat', stack=16, cat='rat_goods', comps=_use('minecraft:block.stone.place', 0.4))

TEMPLATE = {'id': 'minecraft:netherite_upgrade_smithing_template', 'count': Int(1),
            'components': {'minecraft:custom_name': T('Blaze-forged Netherite Upgrade', 'gold'),
                           'minecraft:lore': [T('Hammered out by an Ember Rat.', 'gray'), T('Works like any netherite upgrade.', 'dark_gray')]}}

EMBER_OFFERS = [(('ember_scale', 6), ('lava_wader_charm', 1)), (('ember_scale', 4), ('wither_rose', 2)),
                (('ember_scale', 20), ('skin_fire_launcher', 1)), (('ember_scale', 24), 'TEMPLATE'),
                (('ember_scale', 3), ('token', 1))]
VOID_OFFERS = [(('void_shard', 10), ('pearl_of_return', 1)), (('void_shard', 6), ('shulker_shell', 2)),
               (('void_shard', 8), ('elytra_repair_kit', 1)), (('void_shard', 16), ('levitation_wand', 1)),
               (('void_shard', 12), ('chorus_compass', 1)), (('void_shard', 30), ('void_rat_statue', 1)),
               (('void_shard', 3), ('token', 1))]
DROPS = {'the_nether': ('ember_scale', 0.3, ['blaze', 'wither_skeleton', 'magma_cube', 'ghast', 'piglin_brute', 'hoglin']),
         'the_end': ('void_shard', 0.25, ['enderman', 'shulker'])}
RATS = {  # kind: (name, colour, model, currency, offers, sprite y-offset, beacon particle)
    'ember': ('Ember Rat', '#ff7a1a', 'bm:rat3d_ember', 'ember_scale', EMBER_OFFERS, 0.0, 'minecraft:flame'),
    'void': ('Void Rat', '#c08bff', 'bm:rat3d_void', 'void_shard', VOID_OFFERS, 0.3, 'minecraft:reverse_portal')}


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    tick, fast, second = [], [], []
    G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.wad dummy', 'scoreboard objectives add bm.wt dummy',
                            'scoreboard objectives add bm.wcd dummy', 'scoreboard objectives add bm.frt dummy',
                            'scoreboard objectives add bm.vb dummy',
                            'bossbar add bm:luckynight {text:"Lucky Night",color:"gold",bold:true}',
                            'bossbar set bm:luckynight color yellow', 'bossbar set bm:luckynight style notched_10',
                            'bossbar set bm:luckynight max 10000']
    G.OBJECTIVES += ['bm.wad', 'bm.wt', 'bm.wcd', 'bm.frt', 'bm.vb']

    # ================================================================ who is in the Overworld (Blood Moon / Lucky Night audience)
    bt = G.FUNCS['bloodmoon/tick']
    bt[0:0] = ['tag @a remove bm.ow', 'execute as @a at @s if dimension minecraft:overworld run tag @s add bm.ow']
    for name in ('bloodmoon/warn', 'bloodmoon/start', 'bloodmoon/during', 'bloodmoon/end'):
        G.FUNCS[name] = [l.replace('title @a ', 'title @a[tag=bm.ow] ').replace('tellraw @a ', 'tellraw @a[tag=bm.ow] ')
                         .replace('bossbar set bm:bloodmoon players @a', 'bossbar set bm:bloodmoon players @a[tag=bm.ow]')
                         .replace(' as @a at @s run playsound', ' as @a[tag=bm.ow] at @s run playsound')
                         .replace('as @a at @s if dimension minecraft:overworld', 'as @a[tag=bm.ow] at @s')
                         for l in G.FUNCS[name]]

    # ================================================================ Lucky Night (1% on non-Blood-Moon nights)
    OW = '@a[tag=bm.ow]'
    bt.append('function bm:p22/lucky/tick')
    fn('p22/lucky/tick', [
        'execute if score #tod bm.bm matches 12000.. unless score #lday bm.bm = #day bm.bm run function bm:p22/lucky/roll',
        'scoreboard players set #lwant bm.bm 0',
        'execute if score #lucky bm.bm matches 1 if score #lday bm.bm = #day bm.bm if score #bday bm.bm matches 0 '
        'if score #tod bm.bm matches 13000..22999 run scoreboard players set #lwant bm.bm 1',
        'execute if score #lwant bm.bm matches 1 unless score #lnight bm.bm matches 1 run function bm:p22/lucky/start',
        'execute if score #lwant bm.bm matches 0 if score #lnight bm.bm matches 1 run function bm:p22/lucky/end',
        'execute if score #lnight bm.bm matches 1 run function bm:p22/lucky/during'])
    fn('p22/lucky/roll', [
        'scoreboard players operation #lday bm.bm = #day bm.bm', 'scoreboard players set #lucky bm.bm 0',
        'execute if score #bday bm.bm matches 1 run return 0',
        'execute if score #lforce bm.bm matches 1 run scoreboard players set #lucky bm.bm 1',
        'scoreboard players set #lforce bm.bm 0',
        'execute store result score #r bm.rng run random value 1..100',
        'execute if score #r bm.rng matches 1 run scoreboard players set #lucky bm.bm 1',
        'execute if score #lucky bm.bm matches 1 run function bm:p22/lucky/warn'])
    fn('p22/lucky/warn', [tellraw(OW, PREFIX + [T('A warm breeze smells of clover... tonight is a ', 'yellow'), T('Lucky Night', 'gold', bold=True), T('.', 'yellow')]),
                          f'execute as {OW} at @s run playsound minecraft:block.amethyst_block.chime ambient @s ~ ~ ~ 1 1.4'])
    fn('p22/lucky/start', [
        'scoreboard players set #lnight bm.bm 1',
        f'title {OW} times 20 80 30',
        title(OW, 'subtitle', T('Lucky creatures roam the dark.', 'yellow', italic=True)),
        title(OW, 'title', T('A Lucky Night', 'gold', bold=True)),
        f'execute as {OW} at @s run playsound minecraft:ui.toast.challenge_complete ambient @s ~ ~ ~ 0.7 1.2',
        f'bossbar set bm:luckynight players {OW}', 'bossbar set bm:luckynight visible true',
        tellraw(OW, PREFIX + [T('A Lucky Night! Lucky monsters are about fifteen times as common until dawn.', 'yellow')])])
    fn('p22/lucky/during', [
        'scoreboard players operation #prog bm.bm = #tod bm.bm', 'scoreboard players remove #prog bm.bm 13000',
        'execute store result bossbar bm:luckynight value run scoreboard players get #prog bm.bm',
        f'bossbar set bm:luckynight players {OW}',
        'execute as @a[tag=bm.ow,gamemode=!spectator] at @s if predicate bm:sees_sky run particle minecraft:dust{color:[1.0,0.82,0.2],scale:1.4} ~ ~6 ~ 12 3 12 0 12 normal @s',
        'execute as @a[tag=bm.ow,gamemode=!spectator] at @s run particle minecraft:wax_on ~ ~1 ~ 6 2 6 0 3 normal @s'])
    fn('p22/lucky/end', [
        'scoreboard players set #lnight bm.bm 0', 'bossbar set bm:luckynight visible false',
        tellraw(OW, PREFIX + [T('Dawn. The Lucky Night is over.', 'gold')])])
    fn('admin/lucky_night', [
        'execute if score #bday bm.bm matches 1 run return run ' + tellraw('@s', PREFIX + [T('Not on a Blood Moon day.', 'red')]),
        'scoreboard players set #lucky bm.bm 1', 'scoreboard players operation #lday bm.bm = #day bm.bm',
        'execute if score #tod bm.bm matches 23000.. run scoreboard players set #lforce bm.bm 1',
        tellraw('@s', PREFIX + [T('Lucky Night set: tonight (or now, if it is already night).', 'yellow')])])
    # the mob roll: Lucky 1..100 (10%), Champion 101..112 (1.2%), Elite 113..162 (5%)
    for t in list(G.ARMORED) + list(G.UNARMORED):
        init = G.FUNCS[f'mobs/init/{t}']
        k = next(i for i, l in enumerate(init) if 'mobs/blood_roll/' in l)
        init.insert(k + 1, f'execute if score #lnight bm.bm matches 1 if dimension minecraft:overworld run return run function bm:mobs/lucky_roll/{t}')
        fn(f'mobs/lucky_roll/{t}', ['execute store result score #r bm.rng run random value 1..1000',
                                    f'execute if score #r bm.rng matches 1..100 run return run function bm:mobs/lucky/{t}',
                                    f'execute if score #r bm.rng matches 101..112 run return run function bm:mobs/champion/{t}',
                                    f'execute if score #r bm.rng matches 113..162 run return run function bm:mobs/elite/{t}'])

    # ================================================================ Heartstones pay back the Bloodforge first
    hs = G.FUNCS['p17/heartstone']
    hs.insert(1, 'execute if score @s bm.bdebt matches 1.. run return run function bm:p22/repay')
    fn('p22/repay', ['scoreboard players remove @s bm.bdebt 1', 'function bm:p21/debt_apply',
                     'effect give @s minecraft:regeneration 3 1 true', 'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6',
                     'playsound minecraft:block.respawn_anchor.charge player @s ~ ~ ~ 1 1.2',
                     title('@s', 'actionbar', [T('The Heartstone mends a heart the Bloodforge took. ', 'red'),
                                               {'score': {'name': '@s', 'objective': 'bm.bdebt'}, 'color': 'white'}, T(' still owed.', 'gray')])])

    # ================================================================ field-rat goods
    # Lava Wader: lava sources under you crust into magma; each one cools back after 3 s once nobody stands near it
    G.consume_adv('lava_wader_charm', 'bm:p22/wader')
    fn('p22/wader', ['advancement revoke @s only bm:consume/lava_wader_charm', f'scoreboard players set @s bm.wad {WADE_TICKS}',
                     f'effect give @s minecraft:fire_resistance {WADE_TICKS // 20 + 5} 0 true',
                     'particle minecraft:lava ~ ~0.5 ~ 0.4 0.2 0.4 0 10',
                     title('@s', 'actionbar', T('The lava will hold you for 60 seconds.', 'gold'))])
    tick += ['execute as @a[scores={bm.wad=1..}] at @s run function bm:p22/wade']
    wade = ['scoreboard players remove @s bm.wad 1',
            'execute if score @s bm.wad matches 0 run ' + title('@s', 'actionbar', T('Your Lava Wader Charm cools.', 'gray')),
            'execute if score @s bm.wad matches 200 run ' + title('@s', 'actionbar', T('Lava Wader: 10 seconds left!', 'red')),
            'execute if entity @s[tag=bm.adv] run return 0']
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            wade.append(f'execute positioned ~{dx} ~-1 ~{dz} if block ~ ~ ~ minecraft:lava[level=0] run function bm:p22/wade_set')
    fn('p22/wade', wade)
    fn('p22/wade_set', ['setblock ~ ~ ~ minecraft:magma_block',
                        'execute align xyz run summon minecraft:marker ~0.5 ~0.5 ~0.5 {Tags:["bm.wade"]}'])
    fast += ['execute as @e[type=minecraft:marker,tag=bm.wade] at @s run function bm:p22/wade_cool']
    fn('p22/wade_cool', ['scoreboard players add @s bm.wt 1',
                         'execute if score @s bm.wt matches ..12 run return 0',
                         'execute if entity @a[distance=..1.8] run return 0',
                         'execute if block ~ ~ ~ minecraft:magma_block run setblock ~ ~ ~ minecraft:lava',
                         'particle minecraft:smoke ~ ~0.6 ~ 0.3 0.1 0.3 0 3', 'kill @s'])

    # Fire Charge Launcher skin: a reusable toggle on Snake Eyes in the off hand
    G.consume_adv('skin_fire_launcher', 'bm:p22/fire_skin')
    snake = '*[minecraft:custom_data~{bm:"snake_eyes"}]'
    wjson('bm/item_modifier/p22/fire_on.json', {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': 'bm:fire_charge_launcher'}})
    wjson('bm/item_modifier/p22/fire_off.json', {'function': 'minecraft:set_components', 'components': {'minecraft:item_model': 'minecraft:iron_sword'}})
    fn('p22/fire_skin', ['advancement revoke @s only bm:consume/skin_fire_launcher', give('skin_fire_launcher'),
                         f'execute unless items entity @s weapon.offhand {snake} run return run ' +
                         title('@s', 'actionbar', T('Hold Snake Eyes in your OFF hand!', 'red')),
                         'execute if items entity @s weapon.offhand *[minecraft:item_model="bm:fire_charge_launcher"] run return run function bm:p22/fire_off',
                         'item modify entity @s weapon.offhand bm:p22/fire_on',
                         'playsound minecraft:item.firecharge.use player @s ~ ~ ~ 1 1', 'particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.02 20',
                         title('@s', 'actionbar', T('Snake Eyes is now a Fire Charge Launcher!', 'gold'))])
    fn('p22/fire_off', ['item modify entity @s weapon.offhand bm:p22/fire_off',
                        'playsound minecraft:block.fire.extinguish player @s ~ ~ ~ 1 1.2',
                        title('@s', 'actionbar', T('Snake Eyes is back to its old self.', 'gray'))])

    # Pearl of Return: to the last death point (refused for void deaths, the Hollow and dungeons)
    G.consume_adv('pearl_of_return', 'bm:p22/pearl')

    def pdeny(msg):
        return f'return run function bm:p22/pearl_no {{m:"{msg}"}}'
    fn('p22/pearl_no', [give('pearl_of_return'), '$title @s actionbar {text:"$(m) (Refunded)",color:"gray"}'])
    fn('p22/pearl', ['advancement revoke @s only bm:consume/pearl_of_return',
                     'execute if entity @s[tag=bm.adv] run ' + pdeny("The pearl won't wake in here."),
                     'execute unless data entity @s LastDeathLocation run ' + pdeny("You haven't died yet. Lucky you."),
                     'data remove storage bm:tmp pr',
                     'data modify storage bm:tmp pr.d set from entity @s LastDeathLocation.dimension',
                     'execute store result storage bm:tmp pr.x int 1 run data get entity @s LastDeathLocation.pos[0]',
                     'execute store result storage bm:tmp pr.y int 1 run data get entity @s LastDeathLocation.pos[1]',
                     'execute store result storage bm:tmp pr.z int 1 run data get entity @s LastDeathLocation.pos[2]',
                     'execute store result score #y bm.rng run data get entity @s LastDeathLocation.pos[1]',
                     'execute if data storage bm:tmp {pr:{d:"bm:hollow_throne"}} run ' + pdeny('What the Hollow takes, it keeps.'),
                     'execute if score #y bm.rng matches ..-65 run ' + pdeny('Your last death was in the void.'),
                     'execute if score #y bm.rng matches ..-1 unless data storage bm:tmp {pr:{d:"minecraft:overworld"}} run ' + pdeny('Your last death was in the void.'),
                     'particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                     'function bm:p22/pearl_go with storage bm:tmp pr',
                     'execute at @s align xz run tp @s ~0.5 ~ ~0.5',
                     'effect give @s minecraft:resistance 6 4 true', 'effect give @s minecraft:fire_resistance 15 0 true',
                     'effect give @s minecraft:slow_falling 10 0 true',
                     'execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.4 0.8 0.4 0.05 40',
                     'execute at @s run playsound minecraft:entity.enderman.teleport player @a[distance=..16] ~ ~ ~ 1 0.7',
                     title('@s', 'actionbar', T('You return to where you fell.', '#7fffd4'))])
    fn('p22/pearl_go', ['$execute in $(d) run tp @s $(x) $(y) $(z)'])

    # Elytra Repair Kit
    G.consume_adv('elytra_repair_kit', 'bm:p22/kit')
    wjson('bm/item_modifier/p22/mend.json', {'function': 'minecraft:set_damage', 'damage': 1.0})
    worn = 'minecraft:elytra[minecraft:damage~{damage:{min:1}}]'
    fn('p22/kit', ['advancement revoke @s only bm:consume/elytra_repair_kit',
                   f'execute if items entity @s armor.chest {worn} run return run function bm:p22/kit_do {{slot:"armor.chest"}}',
                   f'execute if items entity @s weapon.offhand {worn} run return run function bm:p22/kit_do {{slot:"weapon.offhand"}}',
                   give('elytra_repair_kit'), title('@s', 'actionbar', T('Wear a damaged elytra (or hold it in your OFF hand)! (Refunded)', 'red'))])
    fn('p22/kit_do', ['$item modify entity @s $(slot) bm:p22/mend', 'playsound minecraft:block.smithing_table.use player @s ~ ~ ~ 1 1.2',
                      'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.03 12',
                      title('@s', 'actionbar', T('Your elytra is good as new.', '#9aa6c8'))])

    # Levitation Wand (shares the carrot-on-a-stick click with the grappling hook)
    wand = '*[minecraft:custom_data~{bm:"levitation_wand"}]'
    gu = G.FUNCS['p21/grap/use']
    gu.insert(1, f'execute if items entity @s weapon.mainhand {wand} run return run function bm:p22/wand')
    fn('p22/wand', ['execute if score @s bm.wcd matches 1.. run return 0',
                    'execute if entity @s[tag=bm.adv] run return run ' + title('@s', 'actionbar', T("The wand won't wake in here.", 'gray')),
                    'scoreboard players set @s bm.wcd 40',
                    'effect give @s minecraft:levitation 1 4 true', 'effect give @s minecraft:slow_falling 4 0 true',
                    'particle minecraft:reverse_portal ~ ~0.2 ~ 0.3 0.1 0.3 0.05 30',
                    'playsound minecraft:entity.shulker.shoot player @a[distance=..16] ~ ~ ~ 0.8 1.6'])
    tick.append('scoreboard players remove @a[scores={bm.wcd=1..}] bm.wcd 1')

    # Chorus Compass: an exploration map is drawn into a scratch display, its target is copied onto the compass
    wjson('bm/tags/worldgen/structure/end_city.json', {'values': ['minecraft:end_city']})
    wjson('bm/loot_table/maps/end_city.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [{
        'type': 'minecraft:item', 'name': 'minecraft:filled_map', 'functions': [     # 26.3: exploration_map stamps the input item, so start from a filled map
            {'function': 'minecraft:exploration_map', 'destination': 'bm:end_city', 'decoration': 'minecraft:target_x', 'zoom': 1,
             'search_radius': 100, 'skip_existing_chunks': False}]}]}]})
    G.consume_adv('chorus_compass', 'bm:p22/compass')
    fn('p22/compass', ['advancement revoke @s only bm:consume/chorus_compass',
                       'execute unless dimension minecraft:the_end run return run function bm:p22/compass_no {m:"The compass only hums in the End."}',
                       'summon minecraft:item_display ~ ~ ~ {Tags:["bm.cc_tmp"]}',
                       'loot replace entity @e[type=minecraft:item_display,tag=bm.cc_tmp,limit=1] contents loot bm:maps/end_city',
                       'data remove storage bm:tmp cc',
                       'execute store result storage bm:tmp cc.x int 1 run data get entity @e[type=minecraft:item_display,tag=bm.cc_tmp,limit=1] item.components."minecraft:map_decorations"."+".x',
                       'execute store result storage bm:tmp cc.z int 1 run data get entity @e[type=minecraft:item_display,tag=bm.cc_tmp,limit=1] item.components."minecraft:map_decorations"."+".z',
                       'execute store success score #ok bm.rng if data entity @e[type=minecraft:item_display,tag=bm.cc_tmp,limit=1] item.components."minecraft:map_decorations"."+"',
                       'kill @e[type=minecraft:item_display,tag=bm.cc_tmp]',
                       'execute if score #ok bm.rng matches 0 run return run function bm:p22/compass_no {m:"No End City answers from here."}',
                       'function bm:p22/compass_give with storage bm:tmp cc',
                       'playsound minecraft:item.lodestone_compass.lock player @s ~ ~ ~ 1 0.8',
                       'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.5 0.3 0.05 20',
                       title('@s', 'actionbar', T('The compass turns toward the nearest End City.', '#c08bff'))])
    fn('p22/compass_no', [give('chorus_compass'), '$title @s actionbar {text:"$(m)",color:"gray"}'])
    tuned = G.item_arg('chorus_compass')[:-1] + ',minecraft:lodestone_tracker={target:{dimension:"minecraft:the_end",pos:[I;$(x),100,$(z)]},tracked:false}]'
    fn('p22/compass_give', [f'$give @s {tuned} 1'])

    # Void Rat Statue (placed like the boss trophies)
    G.consume_adv('void_rat_statue', 'bm:p22/statue/use')
    fn('p22/statue/use', ['advancement revoke @s only bm:consume/void_rat_statue', 'scoreboard players set #placed bm.rng 0',
                          'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                          'execute anchored eyes positioned ^ ^ ^ run function bm:p22/statue/ray', 'tag @s remove bm.placer',
                          'execute if score #placed bm.rng matches 0 unless entity @s[gamemode=creative] run ' + give('void_rat_statue'),
                          'execute if score #placed bm.rng matches 0 run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks to set it down.', 'gray'))])
    fn('p22/statue/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p22/statue/hit',
                          'scoreboard players remove #ray bm.rng 1',
                          'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p22/statue/ray'])
    fn('p22/statue/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.vstat_hit,distance=..0.6] run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p22/statue/spawn'])
    sc = 0.8
    disp = {'Tags': ['bm.vstat', 'bm.new'], 'teleport_duration': Int(3),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:statue_void_rat'}},
            'item_display': 'fixed', 'billboard': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(10)},
            'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                               'translation': [F(0), F(sc / 2), F(0)], 'scale': [F(sc), F(sc), F(sc)]}}
    box = {'Tags': ['bm.vstat_hit', 'bm.new'], 'width': F(0.8), 'height': F(0.9), 'response': B(1)}
    fn('p22/statue/spawn', [f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}', f'summon minecraft:interaction ~ ~ ~ {snbt(box)}',
                            'execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.new,distance=..0.5] ~ ~ ~ ~180 0',
                            'tag @e[tag=bm.new,distance=..0.5] remove bm.new', 'scoreboard players set #placed bm.rng 1',
                            'playsound minecraft:block.stone.place block @a[distance=..16] ~ ~ ~ 1 0.8',
                            'particle minecraft:reverse_portal ~ ~0.5 ~ 0.3 0.3 0.3 0.02 20'])
    fn('p22/statue/pickup', ['loot spawn ~ ~0.3 ~ loot bm:items/void_rat_statue',
                             'kill @e[type=minecraft:item_display,tag=bm.vstat,distance=..0.3]',
                             'particle minecraft:poof ~ ~0.4 ~ 0.2 0.2 0.2 0.02 6',
                             'playsound minecraft:block.stone.break block @a[distance=..16] ~ ~ ~ 1 0.9', 'kill @s'])
    fn('p22/statue/spin', ['data remove entity @s interaction',
                           'execute as @e[type=minecraft:item_display,tag=bm.vstat,distance=..0.3] at @s run tp @s ~ ~ ~ ~45 0',
                           'playsound minecraft:block.stone_button.click_on block @a[distance=..12] ~ ~ ~ 0.6 1.4'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.vstat_hit] if data entity @s attack at @s run function bm:p22/statue/pickup',
             'execute as @e[type=minecraft:interaction,tag=bm.vstat_hit] if data entity @s interaction at @s run function bm:p22/statue/spin',
             'execute as @e[type=minecraft:item_display,tag=bm.vstat] at @s if entity @a[distance=..16] run particle minecraft:reverse_portal ~ ~0.6 ~ 0.2 0.3 0.2 0.01 1']

    # ================================================================ currencies drop in their own dimension (vanilla tables + one pool)
    import json, os
    vdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor', 'loot')
    for dim, (iid, p, mobs) in DROPS.items():
        for m in mobs:
            with open(os.path.join(vdir, f'{m}.json')) as f:
                table = json.load(f)
            table.setdefault('pools', []).append({
                'rolls': 1, 'entries': [G.loot_entry(iid)],
                'conditions': [G.KILLED, G.chance(p),
                               {'condition': 'minecraft:location_check', 'predicate': {'dimension': f'minecraft:{dim}'}}]})
            wjson(f'minecraft/loot_table/entities/{m}.json', table)

    # ================================================================ the field rats
    for k, (name, color, model, cur, offers, oy, beacon) in RATS.items():
        recipes = []
        for buy, sell in offers:
            if sell == 'TEMPLATE':
                o = G.offer(buy, ('token', 1)); o['sell'] = TEMPLATE
            else:
                o = G.offer(buy, sell)
            recipes.append(o)
        trader = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'DespawnDelay': Int(0),
                  'Tags': ['bm.field_rat', f'bm.frat_{k}', 'bm.frnew'],
                  'CustomName': T(name, color, bold=True), 'CustomNameVisible': B(0),
                  'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1),
                                      'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
                  'attributes': [{'id': 'minecraft:scale', 'base': D(0.7)}],
                  'Offers': {'Recipes': recipes}}
        sprite = G.rat_sprite(model, ['bm.rat_sprite', 'bm.field_sprite', f'bm.fsp_{k}', 'bm.td', 'bm.r3d'])
        if oy: sprite = sprite.replace('summon minecraft:item_display ~ ~ ~ ', f'summon minecraft:item_display ~ ~{oy} ~ ')
        fn(f'p22/rat/spawn_{k}', ['execute store result score #y bm.rng run data get entity @s Pos[1]',
                                  'scoreboard players add #y bm.rng 6',
                                  'execute store result storage bm:tmp fr.y int 1 run scoreboard players get #y bm.rng',
                                  'scoreboard players set #frok bm.rng 0',
                                  f'function bm:p22/rat/place_{k} with storage bm:tmp fr',
                                  'execute if score #frok bm.rng matches 1 run ' + tellraw('@s', PREFIX + [
                                      T(f'An {name}' if name[0] in 'AEIOU' else f'A {name}', color, bold=True),
                                      T(' has set up shop somewhere nearby. Follow the ', 'gray'),
                                      T('sparks' if k == 'ember' else 'purple motes', color), T('!', 'gray')]),
                                  'execute if score #frok bm.rng matches 1 run playsound minecraft:entity.silverfish.ambient neutral @s ~ ~ ~ 1 0.6'])
        fn(f'p22/rat/place_{k}', [f'summon minecraft:wandering_trader ~ ~-200 ~ {snbt(trader)}',
                                  '$execute store success score #frok bm.rng run spreadplayers ~ ~ 6 24 under $(y) false @e[type=minecraft:wandering_trader,tag=bm.frnew]',
                                  'execute if score #frok bm.rng matches 0 run kill @e[type=minecraft:wandering_trader,tag=bm.frnew]',
                                  f'execute as @e[type=minecraft:wandering_trader,tag=bm.frnew] at @s run function bm:p22/rat/dress_{k}'])
        fn(f'p22/rat/dress_{k}', ['tag @s remove bm.frnew', 'scoreboard players set @s bm.frt 0', sprite,
                                  'execute as @e[type=minecraft:item_display,tag=bm.field_sprite,distance=..1] run data modify entity @s teleport_duration set value ' + ('20' if oy else '6'),
                                  f'particle {beacon} ~ ~0.5 ~ 0.3 0.4 0.3 0.05 30'])
        fn(f'p22/rat/try_{k}', [f'execute if entity @e[type=minecraft:wandering_trader,tag=bm.frat_{k}] run return 0',
                                f'execute store result score #r bm.rng run random value 1..{SPAWN_ODDS}',
                                f'execute if score #r bm.rng matches 1 run function bm:p22/rat/spawn_{k}'])
        fn(f'admin/{k}_rat', [f'kill @e[type=minecraft:item_display,tag=bm.fsp_{k}]',
                              f'execute as @e[type=minecraft:wandering_trader,tag=bm.frat_{k}] at @s run tp @s ~ -300 ~',
                              f'kill @e[type=minecraft:wandering_trader,tag=bm.frat_{k}]', f'function bm:p22/rat/spawn_{k}',
                              f'execute if score #frok bm.rng matches 0 run ' + tellraw('@s', PREFIX + [T('No safe spot nearby - try somewhere with more floor.', 'red')])])
    fn('p22/rat/try', ['execute if dimension minecraft:the_nether run return run function bm:p22/rat/try_ember',
                       f'execute if dimension minecraft:the_end unless entity @s[x=-{END_SAFE},y=-64,z=-{END_SAFE},dx={END_SAFE * 2},dy=448,dz={END_SAFE * 2}] run function bm:p22/rat/try_void'])
    fn('p22/rat/minute', ['scoreboard players set #min bm.frt 0',
                          'execute as @a[gamemode=!spectator,tag=!bm.adv] at @s run function bm:p22/rat/try'])
    fn('p22/rat/live', ['scoreboard players add @s bm.frt 1',
                        f'execute if score @s bm.frt matches {FIELD_LIFE}.. run return run function bm:p22/rat/leave',
                        'execute if entity @s[tag=bm.frat_ember] run particle minecraft:flame ~ ~1.5 ~ 0.05 1.5 0.05 0.005 6 force @a[distance=..64]',
                        'execute if entity @s[tag=bm.frat_void] run particle minecraft:reverse_portal ~ ~1.5 ~ 0.1 1.5 0.1 0.01 14 force @a[distance=..64]',
                        'execute store result score #r bm.rng run random value 1..6',
                        'execute if score #r bm.rng matches 1 run playsound minecraft:entity.silverfish.ambient neutral @a[distance=..20] ~ ~ ~ 0.5 1.7'])
    fn('p22/rat/leave', [tellraw('@a[distance=..48]', PREFIX + [{'selector': '@s'}, T(' packs up and scurries off.', 'gray')]),
                         'particle minecraft:poof ~ ~0.3 ~ 0.2 0.2 0.2 0.02 10',
                         'kill @e[type=minecraft:item_display,tag=bm.field_sprite,distance=..1.5]',
                         'tp @s ~ -300 ~', 'kill @s'])
    fn('p22/rat/void_fx', ['particle minecraft:reverse_portal ~ ~0.2 ~ 0.15 0.1 0.15 0.01 2',
                           'scoreboard players add @s bm.vb 1', 'execute if score @s bm.vb matches 8.. run scoreboard players set @s bm.vb 0',
                           'execute if score @s bm.vb matches 0 run tp @s ~ ~0.12 ~',
                           'execute if score @s bm.vb matches 4 run tp @s ~ ~-0.12 ~'])
    second += ['scoreboard players add #min bm.frt 1', 'execute if score #min bm.frt matches 60.. run function bm:p22/rat/minute',
               'execute as @e[type=minecraft:wandering_trader,tag=bm.field_rat] at @s run function bm:p22/rat/live',
               'execute as @e[type=minecraft:item_display,tag=bm.field_sprite] at @s unless entity @e[type=minecraft:wandering_trader,tag=bm.field_rat,distance=..1.5] run kill @s']
    fast += ['execute as @e[type=minecraft:item_display,tag=bm.fsp_void] at @s if entity @a[distance=..24] run function bm:p22/rat/void_fx',
             'execute as @e[type=minecraft:item_display,tag=bm.fsp_ember] at @s if entity @a[distance=..24] run particle minecraft:small_flame ~ ~0.35 ~ 0.15 0.1 0.15 0.005 1']

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def post_admin(G):
    G.FUNCS['admin/help'] += [
        G.tellraw('@s', [T('/function bm:admin/lucky_night', 'yellow'), T('  makes tonight a Lucky Night', 'gray')]),
        G.tellraw('@s', [T('/function bm:admin/ember_rat', 'yellow'), T('  summons the Ember Rat near you', 'gray')]),
        G.tellraw('@s', [T('/function bm:admin/void_rat', 'yellow'), T('  summons the Void Rat near you', 'gray')])]


# ===================================================================== ICONS
def icons(grid):
    I = {}
    I['ember_scale'] = grid([
        '................', '.......OO.......', '......OYYO......', '.....OYYYRO.....', '....OYYYRRRO....', '....OYYRRRRO....',
        '...OYYRRRRRDO...', '...ORYRRRRRDO...', '...ORRRRRRDDO...', '....ORRRRDDO....', '....ORRRDDDO....', '.....ORDDDO.....',
        '......ODDO......', '.......OO.......', '................', '................'],
        dict(O='#3a1206', Y='#ffd23f', R='#ff7a1a', D='#b8320c'))
    I['void_shard'] = grid([
        '................', '..........PP....', '.........PLLP...', '........PLLVP...', '.......PLLVVP...', '......PLLVVP....',
        '.....PLLVVP.....', '....PLVVVP......', '...PLVVVP.......', '...PVVVP........', '..PVVDP.........', '..PVDP..........',
        '..PDP...........', '...P............', '................', '................'],
        dict(P='#1e0a2e', L='#e0b0ff', V='#9b4dca', D='#4b1a6e'))
    I['lava_wader_charm'] = grid([
        '....SS....SS....', '...S..S..S..S...', '...S...SS...S...', '....S......S....', '.....S....S.....', '......SSSS......',
        '.....KMMMMK.....', '....KMOMMOMK....', '....KMMYYMMK....', '....KMOYYOMK....', '....KMMMMMMK....', '.....KMOMMK.....',
        '......KMMK......', '.......KK.......', '................', '................'],
        dict(S='#8a8a8a', K='#2a1208', M='#8b2a0e', O='#ff7a1a', Y='#ffd23f'))
    I['fire_charge_launcher'] = grid([
        '..........KKK...', '.........KOFOK..', '........KOFFFOK.', '.......KMOFFOK..', '......KMMMOOK...', '.....KMMMMKK....',
        '....KMMMMK......', '...KGMMMK.......', '..KGGMMK........', '.KWGGKK.........', 'KWWGK...........', 'KWWK............',
        '.KK.............', '................', '................', '................'],
        dict(K='#1a1a1a', O='#e05a10', F='#ffd23f', M='#4a4a52', G='#d4a017', W='#6b3e1f'))
    I['skin_fire_launcher'] = grid([
        '................', '..PPPPPPPPPPPP..', '..PWWWWWWWWWWP..', '..PWWWWOWWWWWP..', '..PWWWOFOWWWWP..', '..PWWOFYFOWWWP..',
        '..PWWOFYYFOWWP..', '..PWOFYYYFOWWP..', '..PWOFYYFOWWWP..', '..PWWOFFOWWWWP..', '..PWWWOOWWWWWP..', '..PWWWWWWWWWWP..',
        '..PWRRRRRRRRWP..', '..PPPPPPPPPPPP..', '................', '................'],
        dict(P='#5a3a1a', W='#e8dcb5', O='#e05a10', F='#ff9a2a', Y='#ffe066', R='#c0392b'))
    I['pearl_of_return'] = grid([
        '................', '.....KKKKK......', '....KTTTTTK.....', '...KTLLTTTDK....', '..KTLWLTTTTDK...', '..KTLLTTTTTDK...',
        '..KTTTTCCTTDK...', '..KTTTCKKCTDK...', '..KTTTCKKCTDK...', '..KDTTTCCTDDK...', '...KDDTTTDDK....', '....KDDDDDK.....',
        '.....KKKKK......', '................', '................', '................'],
        dict(K='#0a2a26', T='#2a9d8f', L='#9ff0e0', W='#ffffff', D='#145a52', C='#7fffd4'))
    I['elytra_repair_kit'] = grid([
        '................', '.......NN.......', '......N..N......', '.....BBBBBB.....', '....BbbbbbbB....', '...BbMMMMMMbB...',
        '...BbMmmmmMbB...', '...BbMmSSmMbB...', '...BbMmSSmMbB...', '...BbMmmmmMbB...', '...BbMMMMMMbB...', '...BbbbbbbbbB...',
        '....BBBBBBBB....', '................', '................', '................'],
        dict(B='#5a3a22', b='#8a5a32', M='#9aa6c8', m='#c4cce8', S='#f2f2f2', N='#bfbfbf'))
    I['levitation_wand'] = grid([
        '...........PPP..', '..........PLLVP.', '..........PLVVP.', '..........PVVVP.', '.........K.PPP..', '........KK......',
        '.......KK.......', '......KK........', '.....KK.........', '....KK..........', '...KK...........', '..KK............',
        '.KK.............', '.K..............', '................', '................'],
        dict(P='#2a1040', L='#f0d8ff', V='#b05cff', K='#3b2a4a'))
    return I
