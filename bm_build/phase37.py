"""Phase 1.23 / 2.16: the Banshee's shroud.

- SPECTER SHEETS: the Banshee has a 1-in-200 chance to drop 1-3 Specter Sheets. Face a wall and right-click one: you
  PHASE through it (up to 12 blocks of wall) and the sheet is used up. Sheets won't work in or near any of the pack's own
  structures (dungeons, the Black Market, graveyards, motherships, crash sites, the Hollow Throne) - nothing is lost when
  they refuse.
- THE SPECTER CHARM: sneak + right-click with 9 sheets to stitch one. Wear it in the CHEST slot.
  Always: 30 blocks of safe fall, but it takes 4 armor away, and players within 5 blocks of you are shrouded in Darkness
  (not you).
  At night or in low light (light 7 or less): Speed III, Jump Boost II, Regeneration I, Night Vision, Fire Resistance -
  and on a Blood Moon, Strength II and Resistance II on top.
  In daylight under open sky: no gifts at all, and you catch fire."""
from items import item, attr, T, TOTEM
from useitem import hold, HOLD

SPECTER = '#c8fff0'

item('specter_sheet', TOTEM, 'Specter Sheet', SPECTER,
     ['A scrap of a banshee\'s shroud. Still restless.', ('Face a wall and right-click: phase through it', 'blue'),
      ('(up to 12 blocks). Used up when it works.', 'blue'), ('Sneak + right-click with 9: a Specter Charm.', 'dark_aqua'),
      ('Useless in the pack\'s dungeons and structures.', 'dark_gray')],
     model='bm:specter_sheet', stack=16, cat='blood', glint=True, comps=hold('none'))
HOLD['specter_sheet'] = 'bm:p37/sheet/use'

item('specter_charm', TOTEM, 'Specter Charm', SPECTER,
     ['Nine shrouds, stitched into one. Wear it (chest).', ('30 blocks of safe fall. Takes 4 armor away.', 'blue'),
      ('Night or low light: Speed III, Jump Boost II,', 'dark_aqua'), ('Regeneration, Night Vision, Fire Resistance.', 'dark_aqua'),
      ('Blood Moon: also Strength II, Resistance II.', 'dark_red'), ('Players within 5 blocks are shrouded in Darkness.', 'gray'),
      ('Daylight, open sky: you burn.', 'red')],
     model='bm:specter_charm', stack=1, cat='blood', bold=True, glint=True,
     comps={'minecraft:equippable': {'slot': 'chest', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'swappable': True},
            'minecraft:attribute_modifiers': [attr('armor', -4, 'chest', ident='bm:specter_armor'),
                                              attr('safe_fall_distance', 27, 'chest', ident='bm:specter_fall')],
            'minecraft:enchantments': {'bm:sunbane': 1}})


def generate(G):
    fn, wjson, title, give = G.fn, G.wjson, G.title, G.give
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    sheet, charm = holds % 'specter_sheet', holds % 'specter_charm'
    objs = ['bm.spsun dummy', 'bm.spct dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))

    # ------------------------------------------------------------------ the sheet: phase through a wall
    # nowhere near the pack's own structures (the same places the drill and the skiff stay out of, plus motherships and crashes)
    fn('p37/allowed', ['execute if entity @s[tag=bm.adv] run return 0', 'execute if dimension bm:hollow_throne run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.zone_d,distance=..48] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.zone_c,distance=..36] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.crypt_ctrl,distance=..36] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.mkt,distance=..80] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.zone_m,distance=..60] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.tbeam,distance=..48] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.dread_core,distance=..48] run return 0',
                       'execute if entity @e[type=minecraft:marker,tag=bm.crash_seed,distance=..24] run return 0', 'return 1'])
    fn('p37/sheet/use', ['execute if predicate bm:p20/sneaking run return run function bm:p37/sheet/stitch',
                         'execute unless function bm:p37/allowed run return run ' + say('The walls here are warded. The sheet goes limp.'),
                         'execute rotated ~ 0 positioned ^ ^ ^0.8 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run ' +
                         say('Face a wall to phase through it.'),
                         'scoreboard players set #found bm.rng 0', 'scoreboard players set #ray bm.rng 24',
                         'execute rotated ~ 0 positioned ^ ^ ^1 run function bm:p37/sheet/ray',
                         'execute if score #found bm.rng matches 0 run return run ' + say('Too much wall - the sheet can\'t find the other side.'),
                         'execute if score #found bm.rng matches 2 run return run ' + say('Something warded waits on the other side. The sheet refuses.')])
    # half-block steps, 12 blocks deep: the first spot with room to stand (feet and head clear, no lava)
    fn('p37/sheet/ray', ['execute if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~ ~ minecraft:lava unless block ~ ~1 ~ minecraft:lava '
                         'align xyz positioned ~0.5 ~ ~0.5 run return run function bm:p37/sheet/land',
                         'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.5 run function bm:p37/sheet/ray'])
    fn('p37/sheet/land', ['execute unless function bm:p37/allowed run return run scoreboard players set #found bm.rng 2',
                          'scoreboard players set #found bm.rng 1', f'clear @s {sheet} 1',
                          'execute at @s run particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.02 16',
                          'execute at @s run playsound minecraft:entity.vex.charge player @a[distance=..16] ~ ~ ~ 1 0.6',
                          'tp @s ~ ~ ~', 'particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.02 16',
                          'playsound minecraft:entity.allay.item_taken player @a[distance=..16] ~ ~ ~ 1 0.5',
                          'effect give @s minecraft:nausea 3 0 true', say('You slip through the stone like a draught.', SPECTER)])
    # 9 sheets -> the charm
    fn('p37/sheet/stitch', [f'execute store result score #n bm.rng run clear @s {sheet} 0',
                            'execute if score #n bm.rng matches ..8 run return run ' +
                            title('@s', 'actionbar', [T('A Specter Charm takes 9 sheets. You have ', 'gray'), {'score': {'name': '#n', 'objective': 'bm.rng'}, 'color': SPECTER}, T('.', 'gray')]),
                            f'clear @s {sheet} 9', give('specter_charm'), 'title @s times 10 60 20',
                            title('@s', 'subtitle', T('The shrouds knot themselves together.', 'gray', italic=True)),
                            title('@s', 'title', T('SPECTER CHARM', SPECTER, bold=True)),
                            'playsound minecraft:entity.allay.death player @s ~ ~ ~ 1 0.5', 'particle minecraft:soul ~ ~1 ~ 0.5 0.6 0.5 0.03 30'])

    # ------------------------------------------------------------------ the charm (worn): once a second
    G.FUNCS['loop/second'][-1:-1] = [
        f'execute as @a[gamemode=!spectator] if items entity @s armor.chest {charm} at @s run function bm:p37/charm/tick',
        f'execute as @a[tag=bm.spcw] unless items entity @s armor.chest {charm} run function bm:p37/charm/off']
    fn('p37/charm/tick', ['tag @s add bm.spcw', 'scoreboard players set @s bm.spsun 0', 'scoreboard players set #dark bm.rng 0',
                          'execute if dimension minecraft:overworld unless score #tod bm.bm matches 0..12499 unless score #tod bm.bm matches 23500.. run scoreboard players set #dark bm.rng 1',
                          'execute if predicate bm:p37/dim run scoreboard players set #dark bm.rng 1',
                          'execute if score #dark bm.rng matches 1 run function bm:p37/charm/night',
                          'execute if score #dark bm.rng matches 0 if dimension minecraft:overworld positioned ~ ~1.6 ~ if predicate bm:sees_sky run scoreboard players set @s bm.spsun 1',
                          # the shroud: everyone near you but you
                          'tag @s add bm.spme',
                          'effect give @a[distance=..5,tag=!bm.spme,gamemode=!spectator,gamemode=!creative] minecraft:darkness 3 0 true',
                          'tag @s remove bm.spme'])
    fn('p37/charm/night', ['effect give @s minecraft:speed 3 2 true', 'effect give @s minecraft:jump_boost 3 1 true',
                           'effect give @s minecraft:fire_resistance 3 0 true', 'effect give @s minecraft:night_vision 13 0 true',
                           # Regeneration I heals every 2.5 s: a 6 s dose every 5 s keeps that pace (re-dosing each second would heal every second)
                           'scoreboard players add @s bm.spct 1',
                           'execute if score @s bm.spct matches 5.. run effect give @s minecraft:regeneration 6 0 true',
                           'execute if score @s bm.spct matches 5.. run scoreboard players set @s bm.spct 0',
                           'execute if score #active bm.bm matches 1 run effect give @s minecraft:strength 3 1 true',
                           'execute if score #active bm.bm matches 1 run effect give @s minecraft:resistance 3 1 true',
                           'particle minecraft:soul ~ ~0.8 ~ 0.3 0.5 0.3 0.01 2'])
    fn('p37/charm/off', ['tag @s remove bm.spcw', 'scoreboard players set @s bm.spsun 0', 'scoreboard players set @s bm.spct 0',
                         'effect clear @s minecraft:night_vision'])
    wjson('bm/predicate/p37/dim.json', {'condition': 'minecraft:location_check', 'offsetY': 1,
                                        'predicate': {'light': {'light': {'max': 7}}}})
    # Sunbane: the charm sets its wearer alight while the once-a-second check says "daylight, open sky"
    wjson('bm/enchantment/sunbane.json', {
        'anvil_cost': 8, 'description': T('Sunbane', 'red'), 'max_level': 1, 'weight': 1,
        'min_cost': {'base': 1, 'per_level_above_first': 0}, 'max_cost': {'base': 1, 'per_level_above_first': 0},
        'slots': ['chest'], 'supported_items': '#minecraft:enchantable/chest_armor',
        'effects': {'minecraft:tick': [{'effect': {'type': 'minecraft:ignite', 'duration': 4},
                                         'requirements': {'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.spsun': 1}}}]}})


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    R.ICONS['specter_sheet'] = grid(['................', '.....WWWWWW.....', '....WWWWWWWW....', '...WWWWWWWWWW...', '...WWKWWWKWWW...', '...WWKWWWKWWW...',
                                     '...WWWWWWWWWW...', '...WWWWWWWWWW...', '...WWWWWWWWWW...', '...WWWWWWWWWW...', '...WWWWWWWWWW...', '...W.WW.WW.WW...',
                                     '...W..W..W..W...', '................', '................', '................'], dict(W='#e8fff8', K='#2a3a3a'))
    R.ICONS['specter_charm'] = grid(['................', '......GGGG......', '.....G....G.....', '......GGGG......', '.......SS.......', '.....WWWWWW.....',
                                     '....WWWWWWWW....', '....WWKWWKWW....', '....WWKWWKWW....', '....WWWWWWWW....', '....WWWSSWWW....', '....WWWWWWWW....',
                                     '....W.WW.WW.....', '....W..W..W.....', '................', '................'], dict(W='#c8fff0', K='#1a4a40', G='#a8b8c0', S='#7ad8b8'))
