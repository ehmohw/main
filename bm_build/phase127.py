"""2.76: THE WRAITHFIRE HEART - the Scorching Heart, quenched in an Ethereal Gem.

THE FORGING (2.77b - Pearlman no longer fuses it): set a Scorching Heart down (its Hearthfire) within 4 blocks of an Ethereal
  Gem set down (its shrine) - either one first - and, as the nine gems do, they rise and glide together, circle closer and
  closer while the heart's flame turns from orange to soul-blue, and merge in a flash: a WRAITHFIRE HEART drops (Burning
  Blue, a hidden challenge, the first time).
CARRIED (anywhere in your pack): fire can't touch you, and monsters that come within 4 blocks catch soul fire.
SET DOWN (sneak + use on the top of a block): THE WRAITHFIRE HEARTH - a stronger Hearthfire. No monster spawns within 64
  blocks of it (the Hearthfire: 48); monsters within 16 burn blue and are worn down; Blood Moon horrors within 32 burn
  hard. Sneak + punch it to take it back.
HANDED TO CECIL OR KILLERWATT (right-click him with it): his WRAITHFIRE FORM - everything his Ethereal Form is (Cecil's bolt a
  second, KillerWatt's half-again blows and his flight), burning blue:
    Cecil      soul-fire bolts (9, 12 to the undead, and they burn); his charged spell is SOUL PYRE - blue fire bursts out of
               the ground (14 to everything within 6, burning and weakened), and a ring of it keeps burning for 5 seconds;
               you're wrapped in Fire Resistance and Absorption.
    KillerWatt every blow sets them alight; his charged attack is SOUL INFERNO - a blast of blue fire at everything within
               12, three rings rolling outward, then the souls go up in a pillar under every foe.
  The heart is never lost: a gem or the Ethereal Gem gives it back, and sneak + right-click empty-handed takes it back.
  (Like gems, it stays in the world it was given in - the heist lobby keeps its own.)
GIVEN TO EMMA (right-click her with it): she keeps it, and can STAY ETHEREAL - her Ethereal Form for as long as you like
  (toggle it in her menu: sneak + use her ribbon), her buff at its strongest the whole time, and the WRAITHFIRE BLESSING for
  everyone she watches over: Fire Resistance and Regeneration. Take the heart back from her menu. (Not in the heist
  lobby - there she's her usual self.)
"""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase69 as P69
import phase79_art as KA

SOUL = '#5ae0ff'
SOUL_RGB = (0.35, 0.85, 1.0)
CEC = '#b48cff'
KWG = '#74d462'
PINK = '#ff7ad0'
WF_C = P69.ETH_I + 1                 # 11: Cecil's wraithfire "element" (10 is the Ethereal Gem)
WF_K = len(KA.EL_KEYS) + 2           # 11: KillerWatt's
HEART = '*[minecraft:custom_data~{bm:"wraithfire_heart"}]'
FOE = 'type=#bm:hostile,tag=!bm.npc'

item('wraithfire_heart', TOTEM, 'Wraithfire Heart', SOUL,
     ['The Scorching Heart, quenched in an Ethereal', 'Gem\'s light. It burns blue - and cold.',
      ('Carried: fire can\'t touch you, and monsters', 'blue'), ('that come close catch soul fire.', 'blue'),
      ('Sneak + use on a block: the WRAITHFIRE HEARTH -', 'blue'), ('no monster spawns within 64 blocks.', 'blue'),
      ('Cecil or KillerWatt: their Wraithfire Form.', 'light_purple'), ('Emma: she can stay ethereal.', 'light_purple'),
      ('Sneak + punch the hearth: take it back.', 'gray')],
     model='bm:wraithfire_heart', glint=True, stack=1, cat='blood', comps=hold('none'), bold=True)
HOLD['wraithfire_heart'] = 'bm:p127/heart/use'

# (each part says where it leads - at import, before any trade or loot table is built from it)
for _iid, _line, _col in (('scorching_heart', 'Set down beside an Ethereal Gem, they fuse.', SOUL), ('ethereal_gem', 'Set down beside a Scorching Heart, they fuse.', SOUL),
                          ('cecil_gem', 'A Wraithfire Heart: his Wraithfire Form.', 'light_purple'),
                          ('kw_spark', 'Give him a Wraithfire Heart: his Wraithfire Form.', KWG),
                          ('emma_ribbon', 'Give her a Wraithfire Heart: she can stay ethereal.', PINK)):
    if _iid in ITEMS:                                # (the resource pack's build imports this alone)
        ITEMS[_iid]['comps']['minecraft:lore'].insert(-1, T(_line, _col))


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    emsay = lambda txt: title('@s', 'actionbar', [T('Emma: ', PINK, bold=True), T(txt, '#ffd0ec')])
    tick, second = [], []
    objs = ['bm.emwf', 'bm.emst']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    ident = [F(0), F(0), F(0), F(1)]
    dust = lambda rgb, sc=1.4: f'minecraft:dust{{color:[{rgb[0]},{rgb[1]},{rgb[2]}],scale:{sc}}}'
    ring = lambda part, r, n=24, y=0.3: [f'particle {part} ^{r * math.cos(2 * math.pi * k / n):.2f} ^{y} ^{r * math.sin(2 * math.pi * k / n):.2f} 0.05 0.1 0.05 0.01 2'
                                         for k in range(n)]
    def consume(where='@s'):           # one off whichever hand holds it (the use fires from either)
        return [f'execute if entity {where}[gamemode=!creative] if items entity {where} weapon.mainhand {HEART} run item modify entity {where} weapon.mainhand {{function:"minecraft:set_count",count:-1,add:true}}',
                f'execute if entity {where}[gamemode=!creative] unless items entity {where} weapon.mainhand {HEART} if items entity {where} weapon.offhand {HEART} run item modify entity {where} weapon.offhand {{function:"minecraft:set_count",count:-1,add:true}}']

    # ================================================================== THE FORGING: a Scorching Heart set down beside an Ethereal Gem
    #   (as the nine gems fuse, no one says so: set the two down within 4 blocks of each other - either one first - and they rise,
    #    glide together, circle closer and closer as the heart's flame turns blue, and become one)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.wft dummy', 'data remove storage bm:p60 fuse']      # (2.76's Pearlman offer, gone)
    G.OBJECTIVES += ['bm.wft']
    G.FUNCS['p82/heart/place'].append('function bm:p127/forge/near')
    G.FUNCS['p60/spawn/ethereal'].append('function bm:p127/forge/near')
    fn('p127/forge/near', ['execute if entity @e[type=minecraft:marker,tag=bm.wfm,distance=..12] run return 0',
                           'execute unless entity @e[type=minecraft:interaction,tag=bm.hearth,distance=..4.5] run return 0',
                           'execute as @e[type=minecraft:item_display,tag=bm.eshr,distance=..4.5,sort=nearest,limit=1] at @s run function bm:p127/forge/begin'])
    # (at the gem: it and the nearest Hearthfire are taken into the forging - no picking either up now)
    fn('p127/forge/begin', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.wfm","bm.wfnew"]}',
                            'scoreboard players set @e[type=minecraft:marker,tag=bm.wfnew,distance=..0.5] bm.wft 0',
                            'tag @e[type=minecraft:marker,tag=bm.wfnew,distance=..0.5] remove bm.wfnew',
                            'tag @s add bm.wfg', 'tag @s remove bm.eshr', 'kill @e[type=minecraft:interaction,tag=bm.eshr_hit,distance=..0.6]',
                            'execute as @e[type=minecraft:interaction,tag=bm.hearth,distance=..4.5,sort=nearest,limit=1] at @s run function bm:p127/forge/take',
                            'playsound minecraft:block.beacon.power_select block @a[distance=..32] ~ ~ ~ 1 0.7',
                            'playsound minecraft:block.amethyst_block.resonate block @a[distance=..32] ~ ~ ~ 1 0.6',
                            'playsound minecraft:block.fire.ambient block @a[distance=..32] ~ ~ ~ 2 0.6',
                            tellraw('@a[distance=..24]', [T('The heart\'s fire leans toward the gem\'s cold light...', SOUL, italic=True)])])
    fn('p127/forge/take', ['tag @e[type=minecraft:item_display,tag=bm.hearthd,distance=..0.6,sort=nearest,limit=1] add bm.wfh2',
                           'execute if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air', 'kill @s'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.wfm] at @s run function bm:p127/forge/tick')
    HT, GM = '@e[type=minecraft:item_display,tag=bm.wfh2,distance=..8,limit=1]', '@e[type=minecraft:item_display,tag=bm.wfg,distance=..8,limit=1]'
    at = lambda t, cmd: f'execute if score @s bm.wft matches {t} run {cmd}'
    fn('p127/forge/tick', ['scoreboard players add @s bm.wft 1',
                           # (both shrink a little and lose their pedestal height; then glide to where the circling begins)
                           at(1, f'execute as {HT} run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{translation:[0f,0f,0f],scale:[0.65f,0.65f,0.65f]}}}}'),
                           at(1, f'execute as {GM} run data merge entity @s {{start_interpolation:0,interpolation_duration:20,transformation:{{translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'),
                           at(2, f'execute as {HT} run data modify entity @s teleport_duration set value 28'),
                           at(2, f'execute as {GM} run data modify entity @s teleport_duration set value 28'),
                           at(3, f'execute positioned ^ ^1.6 ^1.2 run tp {HT} ~ ~ ~'), at(3, f'execute rotated ~180 0 positioned ^ ^1.6 ^1.2 run tp {GM} ~ ~ ~ ~ 0'),
                           at('3..30', 'function bm:p127/forge/gather'),
                           at(30, 'playsound minecraft:block.portal.trigger block @a[distance=..32] ~ ~ ~ 0.4 1.6'),
                           at(31, f'execute as {HT} run data modify entity @s teleport_duration set value 2'),
                           at(31, f'execute as {GM} run data modify entity @s teleport_duration set value 2'),
                           # (circling, ever closer, higher and faster - the heart's flame turning blue as it drinks the light)
                           at('32..92', 'function bm:p127/forge/orbit'),
                           at('32..92', 'function bm:p127/forge/glow'),
                           at('40..92', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.12 0.9 0.12 0.01 3'),
                           at(45, 'playsound minecraft:block.respawn_anchor.charge block @a[distance=..32] ~ ~ ~ 0.8 0.8'),
                           at(60, 'playsound minecraft:block.respawn_anchor.charge block @a[distance=..32] ~ ~ ~ 1 1.1'),
                           at(60, tellraw('@a[distance=..24]', [T('...and drinks it. The flame is turning blue.', SOUL, italic=True)])),
                           at(75, 'playsound minecraft:particle.soul_escape block @a[distance=..32] ~ ~ ~ 2 0.7'),
                           at(84, 'playsound minecraft:block.beacon.activate block @a[distance=..32] ~ ~ ~ 1 0.8'),
                           at(94, 'function bm:p127/forge/done')])
    fn('p127/forge/gather', [f'execute at {HT} run particle minecraft:flame ~ ~ ~ 0.08 0.08 0.08 0.01 2',
                             f'execute at {GM} run particle minecraft:end_rod ~ ~ ~ 0.08 0.08 0.08 0.01 1',
                             'particle minecraft:soul ~ ~0.2 ~ 0.6 0.05 0.6 0.01 1'])
    # (one smooth inward spiral: k ticks in, the radius is 1.2 - 0.018k, the height 1.6 + 0.01k, and the marker turns 14 + 0.5k degrees
    #  a tick; the heart rides one side of the circle, the gem - spinning with it - the other)
    fn('p127/forge/orbit', ['scoreboard players operation #k bm.rng = @s bm.wft', 'scoreboard players remove #k bm.rng 32',
                            'scoreboard players operation #d bm.rng = #k bm.rng', 'scoreboard players operation #d bm.rng *= #18 bm.rng',
                            'scoreboard players set #r bm.rng 1200', 'scoreboard players operation #r bm.rng -= #d bm.rng',
                            'execute store result storage bm:p127 orb.r double 0.001 run scoreboard players get #r bm.rng',
                            'scoreboard players operation #d bm.rng = #k bm.rng', 'scoreboard players operation #d bm.rng *= #10 bm.rng',
                            'execute store result storage bm:p127 orb.y double 0.001 run scoreboard players add #d bm.rng 1600',
                            'scoreboard players operation #d bm.rng = #k bm.rng', 'scoreboard players operation #d bm.rng *= #5 bm.rng',
                            'execute store result storage bm:p127 orb.s double 0.1 run scoreboard players add #d bm.rng 140',
                            'function bm:p127/forge/spin with storage bm:p127 orb'])
    fn('p127/forge/spin', ['$tp @s ~ ~ ~ ~$(s) 0',
                           f'$execute rotated as @s positioned ^ ^$(y) ^$(r) run tp {HT} ~ ~ ~',
                           f'$execute rotated as @s rotated ~180 0 positioned ^ ^$(y) ^$(r) run tp {GM} ~ ~ ~ ~ 0'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #18 bm.rng 18', 'scoreboard players set #10 bm.rng 10', 'scoreboard players set #5 bm.rng 5']
    fn('p127/forge/glow', ['scoreboard players operation #t bm.rng = @s bm.wft', 'scoreboard players operation #t bm.rng %= #10 bm.rng',
                           f'execute if score @s bm.wft matches ..59 at {HT} run particle minecraft:flame ~ ~ ~ 0.06 0.06 0.06 0.01 3',
                           f'execute if score @s bm.wft matches 60.. at {HT} run particle minecraft:soul_fire_flame ~ ~ ~ 0.06 0.06 0.06 0.01 3',
                           f'execute at {GM} run particle {dust((0.85, 0.75, 1.0), 1.1)} ~ ~ ~ 0.08 0.08 0.08 0 2',
                           f'execute at {GM} run particle minecraft:end_rod ~ ~ ~ 0.05 0.05 0.05 0.01 1',
                           'execute if score #t bm.rng matches 0 run playsound minecraft:block.amethyst_block.chime block @a[distance=..24] ~ ~ ~ 1 1.4',
                           'execute if score #t bm.rng matches 0 run playsound minecraft:block.fire.ambient block @a[distance=..24] ~ ~ ~ 1.5 0.8'] +
       [f'execute if score #t bm.rng matches 5 run {l}' for l in ring('minecraft:soul_fire_flame', 1.6, 20, 0.15)])
    fn('p127/forge/done', [f'kill {HT}', f'kill {GM}',
                           'loot spawn ~ ~2.2 ~ loot bm:items/wraithfire_heart',
                           'data merge entity @e[type=minecraft:item,distance=..3,sort=nearest,limit=1] {Glowing:1b,PickupDelay:20s,Motion:[0.0d,0.15d,0.0d]}',
                           'particle minecraft:flash{color:[0.35,0.85,1.0,1.0]} ~ ~2.2 ~ 0 0 0 0 1 force @a[distance=..64]',
                           'particle minecraft:soul_fire_flame ~ ~2.2 ~ 0.2 0.2 0.2 0.25 90 force @a[distance=..64]',
                           'particle minecraft:soul ~ ~2.2 ~ 0.3 0.3 0.3 0.12 40 force @a[distance=..64]',
                           'particle minecraft:end_rod ~ ~2.2 ~ 0.2 0.2 0.2 0.2 40 force @a[distance=..64]'] +
       ring('minecraft:soul_fire_flame', 2.6, 32, 0.2) +
       ['playsound minecraft:block.respawn_anchor.set_spawn block @a[distance=..48] ~ ~ ~ 1 0.8',
        'playsound minecraft:block.end_portal.spawn block @a[distance=..48] ~ ~ ~ 0.5 1.8',
        'playsound minecraft:item.trident.thunder block @a[distance=..48] ~ ~ ~ 0.4 1.6',
        tellraw('@a[distance=..24]', [T('The Scorching Heart drinks the gem\'s light dry - and burns blue. ', SOUL, italic=True), T('A Wraithfire Heart.', SOUL, bold=True)]),
        'advancement grant @a[distance=..12] only bm:story/wraithfire', 'kill @s'])
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:marker,tag=bm.wfm]')
    wjson('bm/advancement/story/wraithfire.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
          'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:wraithfire_heart'}},
                      'title': T('Burning Blue', 'gold'), 'description': T('Set a Scorching Heart down beside an Ethereal Gem', 'gray'),
                      'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== CARRIED: fire can't touch you; what comes close catches soul fire
    second += [f'execute as @a[gamemode=!spectator] if items entity @s container.* {HEART} at @s run function bm:p127/heart/carry',
               f'execute as @a[gamemode=!spectator] unless items entity @s container.* {HEART} if items entity @s weapon.offhand {HEART} at @s run function bm:p127/heart/carry']
    fn('p127/heart/carry', ['effect give @s minecraft:fire_resistance 3 0 true', f'execute as @e[{FOE},distance=..4] at @s run function bm:p127/heart/sear'])
    fn('p127/heart/sear', ['data modify entity @s Fire set value 60s', 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.25 0.4 0.25 0.02 6'])

    # ================================================================== SET DOWN: the Wraithfire Hearth
    fn('p127/heart/use', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a block: set down the Wraithfire Hearth. (Carried, fire can\'t touch you.)', SOUL),
                          'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                          'execute anchored eyes positioned ^ ^ ^ run function bm:p127/heart/ray', 'tag @s remove bm.placer',
                          'execute if score #placed bm.rng matches 0 run return run ' + say('Look at the top of a block within 5 blocks.')] + consume())
    fn('p127/heart/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p127/heart/hit',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p127/heart/ray'])
    fn('p127/heart/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.hearth,distance=..0.6] run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.wfh,distance=..0.6] run return 0',
                          'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p127/hearth/place', 'scoreboard players set #placed bm.rng 1'])
    # (the Scorching Heart: not on top of a Wraithfire Hearth either - and, used from the off hand, it's that hand it leaves)
    G.FUNCS['p82/heart/hit'].insert(2, 'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.wfh,distance=..0.6] run return 0')
    hu = G.FUNCS['p82/heart/use']
    assert hu[-1] == 'execute unless entity @s[gamemode=creative] run item replace entity @s weapon.mainhand with minecraft:air', hu[-1]
    sh = '*[minecraft:custom_data~{bm:"scorching_heart"}]'
    hu[-1:] = [f'execute unless entity @s[gamemode=creative] if items entity @s weapon.mainhand {sh} run return run item replace entity @s weapon.mainhand with minecraft:air',
               f'execute unless entity @s[gamemode=creative] if items entity @s weapon.offhand {sh} run item replace entity @s weapon.offhand with minecraft:air']
    disp = {'Tags': ['bm.wfhd', 'bm.hnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:wraithfire_heart'}},
            'item_display': 'fixed', 'billboard': 'vertical', 'brightness': {'sky': Int(15), 'block': Int(15)},
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(0.8)] * 3}}
    fn('p127/hearth/place', ['summon minecraft:item_display ~ ~ ~ ' + snbt(disp),
                             'summon minecraft:interaction ~ ~ ~ ' + snbt({'Tags': ['bm.wfh', 'bm.gvdeco', 'bm.hnew'], 'width': F(0.7), 'height': F(0.9), 'response': B(1)}),
                             'tag @e[tag=bm.hnew,distance=..0.5] remove bm.hnew', 'execute if block ~ ~ ~ minecraft:air run setblock ~ ~ ~ minecraft:light[level=15]',
                             'particle minecraft:soul_fire_flame ~ ~0.5 ~ 0.3 0.3 0.3 0.06 40', 'particle minecraft:soul ~ ~0.8 ~ 0.3 0.3 0.3 0.04 10',
                             'playsound minecraft:item.firecharge.use block @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:particle.soul_escape block @a[distance=..16] ~ ~ ~ 2 0.8',
                             title('@a[tag=bm.placer]', 'actionbar', T('The Wraithfire Hearth burns blue: no monster spawns within 64 blocks.', SOUL))])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.wfh] at @s run function bm:p127/hearth/sec')
    keep = 'tag=!bm.boss,tag=!bm.npc,tag=!bm.monstrosity,tag=!bm.salboss,tag=!bm.kxboss,tag=!bm.gvg,tag=!bm.gvboss,tag=!bm.tiered'
    fn('p127/hearth/sec', ['execute as @e[type=#bm:hostile,tag=!bm.wfseen,distance=..64] at @s run function bm:p127/hearth/check',
                           f'execute as @e[{FOE},distance=..16] at @s run function bm:p127/hearth/sear',
                           'execute as @e[type=#bm:hostile,tag=bm.blood,distance=..32] at @s run function bm:p127/hearth/burn',
                           'particle minecraft:soul_fire_flame ~ ~0.7 ~ 0.15 0.2 0.15 0.01 3', 'particle minecraft:soul ~ ~1.1 ~ 0.1 0.1 0.1 0.01 1'])
    fn('p127/hearth/check', ['tag @s add bm.wfseen', f'execute if entity @s[{keep}] if data entity @s {{PersistenceRequired:0b}} unless data entity @s CustomName run function bm:p82/hearth/snuff'])
    fn('p127/hearth/sear', ['data modify entity @s Fire set value 60s', 'damage @s 1 minecraft:magic', 'particle minecraft:soul_fire_flame ~ ~0.8 ~ 0.2 0.3 0.2 0.01 3'])
    fn('p127/hearth/burn', ['data modify entity @s Fire set value 80s', 'damage @s 5 minecraft:in_fire', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.02 8'])
    G.FUNCS['p71/deco/pick'][0:0] = ['execute if entity @e[type=minecraft:interaction,tag=bm.gvdme,tag=bm.wfh] at @e[type=minecraft:interaction,tag=bm.gvdme,limit=1] '
                                     'run function bm:p127/hearth/take']
    fn('p127/hearth/take', [give('wraithfire_heart'), 'kill @e[type=minecraft:item_display,tag=bm.wfhd,distance=..0.6]',
                            'execute if block ~ ~ ~ minecraft:light run setblock ~ ~ ~ minecraft:air', 'playsound minecraft:block.fire.extinguish block @a[distance=..16] ~ ~ ~ 0.8 0.8'])
    fn('admin/wraithfire_heart', [give('wraithfire_heart')])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.wfhd]', 'kill @e[type=minecraft:interaction,tag=bm.wfh]']

    # ================================================================== CECIL'S WRAITHFIRE FORM (bm.cpel 11): his Ethereal Form, burning blue
    import re
    widen = lambda l, pat: re.sub(pat + r' matches 10(?![.\d])', lambda m: m.group(0) + '..11', l)
    by = 'by @e[type=minecraft:wolf,tag=bm.cpme,limit=1]'
    sel_pet = 'execute as @e[type=minecraft:wolf,tag=bm.cecilpet] if score @s bm.pid = #me bm.pid'
    ci = G.FUNCS['p46/el/interact']
    k = next(i for i, l in enumerate(ci) if 'bm:p69/el_ethereal' in l)
    ci.insert(k + 1, f'execute if items entity @s weapon.mainhand {HEART} run return run function bm:p127/cec/give')
    at_cec = 'execute at @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] run '
    fn('p127/cec/give', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_pet} if entity @s[distance=..8] run tag @s add bm.cpsel',
                         'execute unless entity @e[type=minecraft:wolf,tag=bm.cpsel] run return run ' + say('Cecil only takes it from the one who summoned him.', CEC),
                         'data modify entity @e[type=minecraft:wolf,tag=bm.cpsel,limit=1] Sitting set value 0b',
                         f'execute if score @s bm.cpel matches {WF_C} run tag @e[tag=bm.cpsel] remove bm.cpsel',
                         f'execute if score @s bm.cpel matches {WF_C} run return run ' + say('Cecil already burns blue. "One heart is plenty - I\'ve only got the one chest."', CEC),
                         'function bm:p69/give_back', f'scoreboard players set @s bm.cpel {WF_C}', f'scoreboard players set #el bm.rng {WF_C}', 'function bm:p46/pet/dress'] + consume() +
       [at_cec + 'particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.4 0.8 0.4 0.08 60', at_cec + 'particle minecraft:soul ~ ~1.4 ~ 0.3 0.6 0.3 0.04 20',
        at_cec + 'particle minecraft:flash{color:[0.6,0.95,1.0,1.0]} ~ ~1.2 ~ 0 0 0 0 1',
        at_cec + 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 2 0.7',
        at_cec + 'playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..16] ~ ~ ~ 1 1.2',
        title('@s', 'actionbar', [T('Cecil swallows the Wraithfire Heart - and burns blue. ', SOUL), T('WRAITHFIRE FORM', 'white', bold=True),
                                  T(': soul-fire bolts, and they burn.', 'gray')]),
        'tag @e[tag=bm.cpsel] remove bm.cpsel'])
    gb = G.FUNCS['p69/give_back']
    gb.insert(0, f'execute if score @s bm.cpel matches {WF_C} run loot give @s loot bm:items/wraithfire_heart')
    # his looks: the wraith robe, hood, staff and eyes (and his gilded staff, if he has it)
    d = G.FUNCS['p46/pet/dress']
    d += [f'execute if score #el bm.rng matches {WF_C} as @e[type=minecraft:item_display,tag=bm.cpet,tag={part}] if score @s bm.pid = #me bm.pid run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_{nm}_wraith"'
          for part, nm in P69.PARTS + (('bm.cp_eyes', 'eyes'),)]
    assert any('#gild bm.rng matches 1' in l for l in d)
    d.append(f'execute if score #gild bm.rng matches 1 if score #el bm.rng matches {WF_C} as @e[type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_arm] if score @s bm.pid = #me bm.pid '
             'run data modify entity @s item.components."minecraft:item_model" set value "bm:cec2_arm_wraith_gild"')
    # everything the Ethereal Form does, the Wraithfire Form does: a cast a second, quicker heals, quicker charge, he cooks
    n = 0
    for name in ('p46/pet/act', 'p46/pet/attack', 'p69/gather', 'p46/el/interact', 'p73/cec/who'):
        L = G.FUNCS[name]
        for i, l in enumerate(L):
            if 'particle minecraft:end_rod' in l: continue        # (his own wisps, below)
            l2 = widen(widen(l, r'bm\.cpel'), r'#el bm\.rng')
            if l2 != l: L[i] = l2; n += 1
    assert n >= 7, n
    act = G.FUNCS['p46/pet/act']
    act.insert(-1, f'execute if score @s bm.cpel matches {WF_C} run particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.01 2')
    ga = G.FUNCS['p69/gather']
    k = next(i for i, l in enumerate(ga) if 'particle minecraft:end_rod' in l)
    ga.insert(k + 1, f'execute if score #el bm.rng matches {WF_C} rotated as @s rotated ~ 0 positioned ^-0.6 ^1.9 ^0.3 run particle minecraft:soul_fire_flame ~ ~ ~ 0.12 0.12 0.12 0.01 5')
    # the soul-fire bolt
    G.FUNCS['p46/pet/bolt'].insert(0, f'execute if score #el bm.rng matches {WF_C} run return run function bm:p127/cec/bolt')
    fn('p127/cec/bolt', [f'execute if entity @s[type=#minecraft:undead] run damage @s 12 minecraft:magic {by}', f'execute unless entity @s[type=#minecraft:undead] run damage @s 9 minecraft:magic {by}',
                         'data modify entity @s Fire set value 100s', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.04 14',
                         'particle minecraft:soul ~ ~1.2 ~ 0.2 0.3 0.2 0.02 3', 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 1.5 1.2',
                         'tag @s add bm.cptgt',
                         'execute as @e[type=minecraft:wolf,tag=bm.cpme,limit=1] at @s positioned ~ ~1.45 ~ facing entity @e[tag=bm.cptgt,limit=1] eyes positioned ^ ^ ^0.5 run function bm:p127/cbeam',
                         'tag @s remove bm.cptgt'])
    fn('p127/cbeam', ['scoreboard players set #bs bm.rng 0', 'function bm:p127/cbeam_s', 'particle minecraft:soul ~ ~ ~ 0.05 0.05 0.05 0.02 2'])
    fn('p127/cbeam_s', [f'particle {dust(SOUL_RGB, 1.1)} ~ ~ ~ 0 0 0 0 1', 'particle minecraft:soul_fire_flame ~ ~ ~ 0.02 0.02 0.02 0 1', 'scoreboard players add #bs bm.rng 1',
                        'execute if score #bs bm.rng matches ..30 unless entity @e[tag=bm.cptgt,distance=..1.6] positioned ^ ^ ^0.5 run function bm:p127/cbeam_s'])
    # SOUL PYRE: his charged spell
    ch = G.FUNCS['p69/charged']
    k = next(i for i, l in enumerate(ch) if 'bm:p69/ch/ethereal' in l)
    ch[k + 1:k + 1] = [f'execute if score #el bm.rng matches {WF_C} as @e[{FOE},distance=..14,sort=nearest,limit=1] at @s run function bm:p127/cec/pyre',
                       f'execute if score #el bm.rng matches {WF_C} on owner run ' + title('@s', 'actionbar', [T('Cecil unleashes ', 'gray'), T('SOUL PYRE!', SOUL, bold=True)])]
    owner = 'execute as @e[type=minecraft:wolf,tag=bm.cpme] on owner run '
    fn('p127/cec/pyre', [f'execute as @e[{FOE},distance=..6] run damage @s 14 minecraft:magic {by}', f'execute as @e[{FOE},distance=..6] run data modify entity @s Fire set value 160s',
                         f'effect give @e[{FOE},distance=..6] minecraft:weakness 6 1', owner + 'effect give @s minecraft:fire_resistance 15 0 true',
                         owner + 'effect give @s minecraft:absorption 10 1 true', 'particle minecraft:soul_fire_flame ~ ~0.5 ~ 2.5 0.3 2.5 0.06 160',
                         'particle minecraft:soul ~ ~1 ~ 2 1 2 0.05 40', 'particle minecraft:flash{color:[0.6,0.95,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                         'playsound minecraft:entity.blaze.shoot neutral @a[distance=..32] ~ ~ ~ 1 0.5', 'playsound minecraft:particle.soul_escape neutral @a[distance=..32] ~ ~ ~ 2 0.6',
                         'playsound minecraft:block.respawn_anchor.deplete neutral @a[distance=..32] ~ ~ ~ 1 0.8'] +
       [f'execute rotated {r * 30} 0 run particle minecraft:soul_fire_flame ^ ^{0.3 + 0.5 * h} ^{1.5 + 0.3 * h} 0.05 0.2 0.05 0.02 3' for r in range(12) for h in range(4)] +
       ['summon minecraft:marker ~ ~ ~ {Tags:["bm.cf","bm.cfnew"]}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.cft 100',
        'scoreboard players set @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.cfk 9',
        'scoreboard players operation @e[type=minecraft:marker,tag=bm.cfnew,limit=1] bm.pid = #me bm.pid', 'tag @e[type=minecraft:marker,tag=bm.cfnew] remove bm.cfnew'])
    ft = G.FUNCS['p69/f/tick']
    k = next(i for i, l in enumerate(ft) if 'bm:p69/f/k8' in l)
    ft.insert(k + 1, 'execute if score @s bm.cfk matches 9 run function bm:p127/f/pyre')
    fn('p127/f/pyre', [f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..4] run damage @s 3 minecraft:magic {by}',
                       f'execute if score #ft bm.rng matches 0 as @e[{FOE},distance=..4] run data modify entity @s Fire set value 40s',
                       'particle minecraft:soul_fire_flame ~ ~0.2 ~ 1.8 0.1 1.8 0.01 5', 'particle minecraft:soul ~ ~0.6 ~ 1.5 0.4 1.5 0.01 1'] +
       [f'execute if score #ft bm.rng matches 0 run {l[0:]}' for l in ring('minecraft:soul_fire_flame', 4, 20, 0.2)])

    # ================================================================== KILLERWATT'S WRAITHFIRE FORM (bm.kxel 11)
    ki = G.FUNCS['p79/el/interact']
    k = next(i for i, l in enumerate(ki) if 'ethereal_gem' in l)
    ki.insert(k + 1, f'execute if items entity @s weapon.mainhand {HEART} run return run function bm:p79/el/set {{i:{WF_K}}}')
    st = G.FUNCS['p79/el/set']
    assert st[-1] == 'tag @e[tag=bm.kxsel2] remove bm.kxsel2'
    st.insert(len(st) - 1, f'execute if score #el bm.rng matches {WF_K} run ' + title('@s', 'actionbar', [T('KillerWatt drinks the Wraithfire Heart - ', KWG), T('WRAITHFIRE FORM', SOUL, bold=True),
                                                                                                        T(': black steel burning blue - every blow sets them alight, and he flies.', 'gray')]))
    G.FUNCS['p79/el/give_back'].insert(0, f'execute if score @s bm.kxel matches {WF_K} run loot give @s loot bm:items/wraithfire_heart')
    ap = G.FUNCS['p79/el/apply']
    ap += [f'execute if score #el bm.rng matches {WF_K} run particle minecraft:soul_fire_flame ~ ~1.5 ~ 0.5 1 0.5 0.1 70',
           f'execute if score #el bm.rng matches {WF_K} run particle minecraft:soul ~ ~1.8 ~ 0.4 0.8 0.4 0.04 20',
           f'execute if score #el bm.rng matches {WF_K} run playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 2 0.7']
    # his parts: the wraith hide (dress, and the flexed arms)
    for name in ('p79/pet/dress_rig', 'p79/flex', 'p79/unflex'):
        L = G.FUNCS[name]
        out = []
        for l in L:
            out.append(l)
            if '#kel bm.rng matches 10 ' in l:
                assert '_eth"' in l, l
                out.append(l.replace('#kel bm.rng matches 10 ', f'#kel bm.rng matches {WF_K} ').replace('_eth"', '_wf"'))
        assert len(out) > len(L), name
        G.FUNCS[name] = out
    # his charged attack, its gathering and its name; what his blows do
    ul = G.FUNCS['p79/pet/a_ult']
    k = next(i for i, l in enumerate(ul) if 'bm:p79/pet/ultb/void' in l)
    ul[k + 1:k + 1] = [f'execute if score @s bm.kxt matches 20 run execute if score #kel bm.rng matches {WF_K} run function bm:p127/kw/ult',
                       f'execute if score @s bm.kxt matches 21..55 run execute if score #kel bm.rng matches {WF_K} run function bm:p127/kw/ultb']
    for name, part in (('p79/pet/charged_sec', f'particle {dust(SOUL_RGB, 1.6)} ~ ~1.6 ~ 0.6 0.9 0.6 0 10'),
                       ('p79/pet/ult_gather', f'particle {dust(SOUL_RGB, 2.0)} ~ ~2.2 ~ 2.5 1.5 2.5 0 14')):
        L = G.FUNCS[name]
        k = next(i for i, l in enumerate(L) if '#kel bm.rng matches 10 ' in l)
        L.insert(k + 1, f'execute if score #kel bm.rng matches {WF_K} run {part}')
    un = G.FUNCS['p79/pet/ult_name']
    k = next(i for i, l in enumerate(un) if '#kel bm.rng matches 10 ' in l)
    un.insert(k + 1, f'execute if score #kel bm.rng matches {WF_K} run ' + title('@a[distance=..32]', 'actionbar', [T('KillerWatt: ', 'gray'), T('SOUL INFERNO', SOUL, bold=True)]))
    to = G.FUNCS['p79/pet/touch']
    k = max(i for i, l in enumerate(to) if '#kel bm.rng matches 10 ' in l)
    to[k + 1:k + 1] = [f'execute if score #kel bm.rng matches {WF_K} run data modify entity @s Fire set value 100s',
                       f'execute if score #kel bm.rng matches {WF_K} run particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.05 12']
    # everything else the Ethereal Form does (his half-again blows, the flight, his speed ridden) the Wraithfire Form does too
    own = {'p79/pet/dress_rig', 'p79/flex', 'p79/unflex', 'p79/el/give_back', 'p79/pet/a_ult', 'p79/pet/charged_sec', 'p79/pet/ult_gather',
           'p79/pet/ult_name', 'p79/pet/touch', 'p79/el/set'}
    n = 0
    for name in [x for x in G.FUNCS if x.startswith(('p79/', 'p125/kw')) and x not in own]:
        L = G.FUNCS[name]
        for i, l in enumerate(L):
            l2 = widen(widen(l, r'#kel bm\.rng'), r'bm\.kxel')
            if name == 'p79/el/apply' and 'unless score #el bm.rng matches 10' in l2:
                l2 = widen(l2, r'#el bm\.rng')
            if l2 != l: L[i] = l2; n += 1
    assert n >= 30, n
    pme = '@e[type=minecraft:wolf,tag=bm.kxme,limit=1]'
    foe = lambda r, lo=None: f'@e[{FOE},distance={lo or ""}..{r}]'
    atk = lambda dmg, r, lo=None: f'execute as {foe(r, lo)} at @s run function bm:p79/pet/uhit{dmg}'
    beat = lambda t, cmd: f'execute if score @s bm.kxt matches {t} run {cmd}'
    # SOUL INFERNO: blue fire out of him at everything for twelve blocks; three rings roll outward; then the souls go up
    fn('p127/kw/ult', [atk(20, 12), f'execute as {foe(12)} run data modify entity @s Fire set value 200s', f'effect give {foe(12)} minecraft:weakness 6 1',
                       'particle minecraft:soul_fire_flame ~ ~1 ~ 6 1.5 6 0.25 500', 'particle minecraft:soul ~ ~1.5 ~ 5 1.5 5 0.1 120',
                       'particle minecraft:flash{color:[0.5,0.9,1.0,1.0]} ~ ~1.5 ~ 0 0 0 0 1',
                       'playsound minecraft:entity.blaze.shoot neutral @a[distance=..48] ~ ~ ~ 1.6 0.5', 'playsound minecraft:particle.soul_escape neutral @a[distance=..48] ~ ~ ~ 2 0.5'])
    ub = []
    for t, lo, hi in ((26, None, 4), (30, 4, 7), (34, 7, 10)):
        ub += [beat(t, atk(8, hi, lo)), beat(t, f'execute as {foe(hi, lo)} run data modify entity @s Fire set value 120s'),
               beat(t, 'playsound minecraft:item.firecharge.use neutral @a[distance=..32] ~ ~ ~ 1.4 0.5')] + \
              [beat(t, c) for c in ring('minecraft:soul_fire_flame', hi - 0.5, 28, 0.4)]
    ub += [beat(40, atk(12, 12)), beat(40, f'execute as {foe(12)} at @s run function bm:p127/kw/pillar'),
           beat(40, 'playsound minecraft:entity.warden.sonic_boom neutral @a[distance=..48] ~ ~ ~ 1 1.4'),
           beat(40, 'playsound minecraft:block.respawn_anchor.deplete neutral @a[distance=..48] ~ ~ ~ 1.5 0.6')]
    fn('p127/kw/ultb', ub)
    fn('p127/kw/pillar', [f'particle minecraft:soul_fire_flame ~ ~{y / 2} ~ 0.2 0.1 0.2 0.02 4' for y in range(0, 12)] + ['particle minecraft:soul ~ ~2 ~ 0.3 1 0.3 0.05 8'])

    # ================================================================== EMMA: she keeps the heart, and can stay ethereal
    wjson('bm/advancement/p127/emma_click.json', {'criteria': {'i': {'trigger': 'minecraft:player_interacted_with_entity', 'conditions': {
        'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this',
                    'predicate': {'minecraft:entity_type': 'minecraft:cat', 'minecraft:nbt': '{Tags:["bm.emmapet"]}'}}]}}}, 'rewards': {'function': 'bm:p127/em/click'}})
    sel_em = 'execute as @e[type=minecraft:cat,tag=bm.emmapet] if score @s bm.pid = #me bm.pid'
    at_em = 'execute at @e[type=minecraft:cat,tag=bm.emsel2,limit=1] run '
    unsit = ['execute as @e[type=minecraft:cat,tag=bm.emsel2] store success score #s bm.rng if data entity @s {Sitting:1b}',
             'execute if score #s bm.rng matches 1 run data modify entity @e[type=minecraft:cat,tag=bm.emsel2,limit=1] Sitting set value 0b',
             'execute if score #s bm.rng matches 0 run data modify entity @e[type=minecraft:cat,tag=bm.emsel2,limit=1] Sitting set value 1b']
    fn('p127/em/click', ['advancement revoke @s only bm:p127/emma_click', f'execute unless items entity @s weapon.mainhand {HEART} run return 0',
                         'execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'{sel_em} if entity @s[distance=..8] run tag @s add bm.emsel2',
                         'execute unless entity @e[type=minecraft:cat,tag=bm.emsel2] run return run ' + say('Emma only takes it from the one she follows.', PINK)] + unsit +
       ['execute if score @s bm.emwf matches 1 run tag @e[tag=bm.emsel2] remove bm.emsel2',
        'execute if score @s bm.emwf matches 1 run return run ' + emsay('I already have one, silly! It\'s warm... in a cold way.'),
        'scoreboard players set @s bm.emwf 1', 'scoreboard players set @s bm.emst 1'] + consume() +
       [at_em + 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.7 0.4 0.06 50', at_em + 'particle minecraft:cherry_leaves ~ ~1.2 ~ 0.5 0.7 0.5 0 30',
        at_em + 'particle minecraft:flash{color:[0.7,0.95,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
        at_em + 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 2 1.2', at_em + 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..16] ~ ~ ~ 1 1.4',
        emsay('It\'s so warm - and cold! I can stay like this now, as long as you want~'),
        tellraw('@s', PREFIX + [T('Emma keeps the Wraithfire Heart. ', SOUL, bold=True),
                                T('She can stay in her Ethereal Form now - turn it on or off in her menu (sneak + use her ribbon); take the heart back there too.', 'gray')]),
        'tag @e[tag=bm.emsel2] remove bm.emsel2'])
    # every second (as Emma): her owner's heart keeps her ethereal - and blesses them
    sec = G.FUNCS['p57/sec']
    k = next(i for i, l in enumerate(sec) if l == 'execute if score @s bm.eme matches 1.. run function bm:p57/ethereal')
    sec[k:k] = ['tag @s remove bm.emwfs', 'scoreboard players set #wfs bm.rng 0',
                'execute on owner if score @s bm.emwf matches 1 if score @s bm.emst matches 1 run scoreboard players set #wfs bm.rng 1',
                'execute if score #wfs bm.rng matches 1 unless dimension bm:gutter run tag @s add bm.emwfs',
                'execute if entity @s[tag=bm.emwfs] if score @s bm.eme matches 0 run function bm:p57/ascend',
                'execute if entity @s[tag=bm.emwfs] if score @s bm.eme matches 1..29 run scoreboard players set @s bm.eme 30',
                'execute if entity @s[tag=bm.emwfs] run particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.3 0.5 0.3 0.01 2']
    pu = G.FUNCS['p57/pulse']
    k = next(i for i, l in enumerate(pu) if l == 'tag @s remove bm.emme')
    pu.insert(k, 'execute if entity @s[tag=bm.emwfs] as @a[distance=..10,gamemode=!spectator] at @s run function bm:p127/em/bless')
    fn('p127/em/bless', ['effect give @s minecraft:fire_resistance 5 0 true', 'effect give @s minecraft:regeneration 5 0 true',
                         'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.01 3'])
    # her menu: with the heart, STAY ETHEREAL (on / off) and TAKE THE HEART BACK
    import phase28 as P28
    import phase57 as P57
    btn = lambda m: P28.btn(T(P57.MODES[m][0], P57.MODES[m][1], bold=True), 7300 + m, tooltip=T({1: 'Speed + Jump Boost', 2: 'Strength', 3: 'Resistance',
                                                                                                4: 'Regeneration + quick heals', 5: 'Haste: dig and chop faster'}[m], 'gray'), width=120)
    dlg = P28.multi([T("Emma's Ribbon", PINK, bold=True), T('  ·  the Wraithfire Heart', SOUL)],
                    [P28.body([T('Buff: ', 'gray'), T('$(mode)', 'white', bold=True), T('     Stay ethereal: ', 'gray'), T('$(st)', SOUL, bold=True)]),
                     P28.body([T('Pick what she focuses on. While she stays ethereal her buff is at its strongest, and everyone she watches over has ', 'gray'),
                               T('Fire Resistance and Regeneration', SOUL), T('. (In the heist lobby she\'s her usual self.)', 'dark_gray')])],
                    [btn(1), btn(2), btn(3), btn(4), btn(5), P28.btn(T('Wardrobe', '#ff8ad8', bold=True), 7306, tooltip=T('Her ribbons, dresses and outfits', 'gray'), width=120),
                     P28.btn(T('Stay ethereal: on / off', SOUL, bold=True), 7307, tooltip=T('Keep her in her Ethereal Form - or let her be.', 'gray'), width=120),
                     P28.btn(T('Take back the heart', '#9ad8ff'), 7308, tooltip=T('She gives the Wraithfire Heart back to you.', 'gray'), width=120),
                     P28.btn(T('Send her home', 'gray'), 7309, width=120)], columns=2, exit_label='Close')
    fn('p127/em/menu_show', [f'$dialog show @s {snbt(dlg)}'])
    mn = G.FUNCS['p57/menu']
    assert mn[-1] == 'function bm:p57/menu_show with storage bm:tmp em', mn[-1]
    mn[-1:-1] = ['data modify storage bm:tmp em.st set value "off"', 'execute if score @s bm.emst matches 1 run data modify storage bm:tmp em.st set value "on"',
                 'execute if score @s bm.emwf matches 1 run return run function bm:p127/em/menu_show with storage bm:tmp em']
    ea = G.FUNCS['p57/act']
    assert ea[-1] == 'tag @e[tag=bm.emsel2] remove bm.emsel2', ea[-1]
    ea[-1:-1] = ['execute if score #act bm.pay matches 7307 run function bm:p127/em/toggle', 'execute if score #act bm.pay matches 7308 run function bm:p127/em/take']
    fn('p127/em/toggle', ['execute unless score @s bm.emwf matches 1 run return run function bm:p28/stale',
                          'execute if score @s bm.emst matches 1 run return run function bm:p127/em/off', 'scoreboard players set @s bm.emst 1',
                          'execute if dimension bm:gutter run ' + emsay('Not here - the heart won\'t burn in the vault. Back home, though~!'),
                          'execute unless dimension bm:gutter run ' + emsay('Okay! I\'ll stay like this - shining, just for you~'),
                          'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.4', 'function bm:p57/menu'])
    fn('p127/em/off', ['scoreboard players set @s bm.emst 0', 'execute as @e[type=minecraft:cat,tag=bm.emsel2] if score @s bm.eme matches 2.. run scoreboard players set @s bm.eme 1',
                       emsay('Phew - okay, back to plain old me! Tell me when you want me shining again.'),
                       'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 0.9', 'function bm:p57/menu'])
    fn('p127/em/take', ['execute unless score @s bm.emwf matches 1 run return run function bm:p28/stale',
                        'scoreboard players set @s bm.emwf 0', 'scoreboard players set @s bm.emst 0', 'loot give @s loot bm:items/wraithfire_heart',
                        'execute as @e[type=minecraft:cat,tag=bm.emsel2] if score @s bm.eme matches 2.. run scoreboard players set @s bm.eme 1',
                        at_em + 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.03 20', 'playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.8 0.9',
                        emsay('Here you go! Keep it safe, okay? It gets lonely.'), 'function bm:p57/menu'])

    G.FUNCS['tick'] += tick
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack: the heart; Cecil's wraith looks
def textures():
    from PIL import Image
    from gen_rp import hexc
    import random
    rnd = random.Random(127)
    def flame(base, hot, alpha, seed_cols):
        """a robe of blue flame: the base colour, tongues of the hot one licking up a few columns"""
        im = Image.new('RGBA', (16, 16)); b, h = hexc(base)[:3], hexc(hot)[:3]
        tongues = {x: rnd.randint(7, 15) for x in seed_cols}
        for y in range(16):
            for x in range(16):
                t = 0.0
                for tx, ht in tongues.items():
                    dx = abs(x - tx)
                    if dx <= 1 and y >= 16 - ht: t = max(t, (1 - dx * 0.45) * (y - (16 - ht)) / ht)
                v = rnd.randint(-6, 6)
                c = tuple(max(0, min(255, int(b[i] + (h[i] - b[i]) * t) + v)) for i in range(3))
                im.putpixel((x, y), c + (max(0, min(255, alpha + rnd.randint(-10, 10))),))
        return im
    T_ = {'cec_hood_wraith': flame('#06141e', '#5ae8ff', 232, (1, 4, 7, 10, 13)), 'cec_hood_dark_wraith': flame('#02080c', '#1a8ab0', 238, (3, 8, 12)),
          'cec_metal_wraith': flame('#121c24', '#5a9ab8', 255, (7,))}
    cr = Image.new('RGBA', (16, 16))                     # soul fire: a white-hot core, cyan, teal at the edge
    for y in range(16):
        for x in range(16):
            r = math.hypot(x - 7.5, y - 7.5) / 10.6
            c = (230, 255, 255) if r < 0.3 else (90, 230, 255) if r < 0.65 else (24, 150, 190)
            cr.putpixel((x, y), c + (240 if r < 0.3 else 200,))
    T_['cec_crystal_wraith'] = cr
    T_['cec_eye_wraith'] = Image.new('RGBA', (16, 16), (110, 240, 255, 255))
    return T_


def rp(R):
    import sys, copy
    R.TEXTURE_MODS.append(sys.modules[__name__])
    R.ICONS['wraithfire_heart'] = R.grid(['................', '..rr.......rr...', '.rOOr.....rOOr..', 'rOYYOr...rOYYOr.', 'rOYWYOr.rOYWYOr.', 'rOYYYOOrOOYYYOr.',
                                          'rOOYYYOOOYYYOOr.', '.rOOYYYYYYYOOr..', '..rOOYYYYYOOr...', '...rOOYYYOOr....', '....rOOYOOr.....', '.....rOOOr......',
                                          '......rOr.......', '.......r........', '................', '................'],
                                         dict(r='#06303e', O='#1aa8d0', Y='#5af0ff', W='#e8ffff'))
    tex = {'r': 'bm:block/cec_hood_wraith', 'd': 'bm:block/cec_hood_dark_wraith', 'g': 'bm:block/cec_metal_wraith', 'p': 'bm:block/cec_crystal_wraith',
           'y': 'bm:block/cec_eye_wraith'}
    for nm in ('head', 'arm', 'body', 'larm', 'eyes'):
        ct, els = R.HATS[f'cec2_{nm}']
        els = copy.deepcopy(els)
        for e in els:                                    # burning: everything glows, the staff's flame and his eyes fully
            e['light_emission'] = max(e.get('light_emission', 0), 10)
        R.HATS[f'cec2_{nm}_wraith'] = (dict(ct, **{c: t for c, t in tex.items() if c in ct}), els)
    ct, els = R.HATS['cec2_arm_wraith']
    R.HATS['cec2_arm_wraith_gild'] = (dict(ct, g='bm:block/cec_gilded'), els)
