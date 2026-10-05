"""Phase 1.14: the Visitors, part 1 - crashed saucers, Xenite crystals, Zorp the alien trader, alien tech and the
Xenite Altar (socketing + infusions).

- CRASHED SAUCERS: a smoking crater on the surface with a tilted saucer, Xenite deposits, a built-in Xenite Altar and
  Zorp, a stationary alien trader. (Visitor Night and the mothership come in later updates.)
- XENITE DEPOSITS are "display blocks": a real amethyst block wearing a glowing crystal model. Mining one drops 2-4
  Xenite shards of its colour (the vanilla amethyst block drop is removed). Green = energy, violet = gravity,
  cyan = resonance.
- ZORP sells alien tech for shards, and swaps shard colours. He is a NEW trader with his own offer list and his own
  checksum re-sync - no existing trader's offers change (verified at build).
- ALIEN TECH: Ray Gun (4 shots per green shard), Tractor Beam (vacuums items/XP along your gaze, lifts mobs),
  Cloaking Device (45 s invisibility, 4 min recharge), Xenite Dowser (finds diamonds/emeralds/ancient debris within
  8 blocks), Gravity Boots (floaty jumps, soft landings).
- XENITE ALTAR (placeable; one stands at every crash site):
    right-click with gear in your main hand and a shard in your off hand -> SOCKET it (one socket per item):
      green +1.5 Attack Damage, violet +3 Safe Fall & +10% Knockback Resistance, cyan +1.5 Luck & +0.5 Reach
    SNEAK + right-click -> INFUSE: boots + 6 violet = gravity-infused boots, compass + 6 cyan = Dowser,
      crossbow + 8 green = Ray Gun, glass bottle + 4 cyan = Cloaking Device, ender pearl + 6 violet = Tractor Beam
  Sockets and infusions survive future item re-stamps (the restamp re-applies them).
Importing registers the items; generate(G) runs after phase23.generate."""
import math
import random
from nbt import snbt, B, F, Int, D
from items import item, consumable, attr, T, TOTEM, ITEM_VERSION

COLORS = {'green': ('#7dff6a', 'Green Xenite', 'energy'), 'violet': ('#c27dff', 'Violet Xenite', 'gravity'),
          'cyan': ('#6af2ff', 'Cyan Xenite', 'resonance')}
SOCKET = {   # colour: (lore, [(attribute, amount, operation, id suffix)])
    'green': ('+1.5 Attack Damage', [('attack_damage', 1.5, 'add_value', 'a')]),
    'violet': ('+3 Safe Fall, +10% Knockback Resistance', [('safe_fall_distance', 3.0, 'add_value', 'a'), ('knockback_resistance', 0.1, 'add_value', 'b')]),
    'cyan': ('+1.5 Luck, +0.5 Reach', [('luck', 1.5, 'add_value', 'a'), ('block_interaction_range', 0.5, 'add_value', 'b'),
                                         ('entity_interaction_range', 0.5, 'add_value', 'c')])}
GRAVITY = [('gravity', -0.3, 'add_multiplied_base', 'g'), ('jump_strength', 0.08, 'add_value', 'j'), ('safe_fall_distance', 4.0, 'add_value', 'f')]
INFUSIONS = [   # (main-hand test, shard colour, shards, result iid or 'gravity' (in place), consumes the main-hand item)
    ('#minecraft:foot_armor', 'violet', 6, 'gravity', False),
    ('minecraft:compass', 'cyan', 6, 'xenite_dowser', True),
    ('minecraft:crossbow', 'green', 8, 'ray_gun', True),
    ('minecraft:glass_bottle', 'cyan', 4, 'cloaking_device', True),
    ('minecraft:ender_pearl', 'violet', 6, 'tractor_beam', True)]
HANDHELD = {'ray_gun', 'tractor_beam'}
RAY_IGNORE = ['item', 'experience_orb', 'item_display', 'block_display', 'text_display', 'marker', 'interaction', 'armor_stand',
              'arrow', 'spectral_arrow', 'area_effect_cloud', 'villager', 'wandering_trader', 'iron_golem', 'snow_golem', 'player',
              'falling_block', 'tnt', 'firework_rocket', 'egg', 'snowball', 'ender_pearl', 'trident', 'fishing_bobber', 'lightning_bolt']


def _use(sound, secs=0.6, anim='none'):
    return {'minecraft:consumable': consumable(secs, anim, sound, False)}


# ===================================================================== ITEMS
for c, (col, name, kind) in COLORS.items():
    item(f'xenite_{c}', TOTEM, f'{name} Shard', col,
         [f'Alien crystal - it hums with {kind}.', ('Mined from Xenite deposits at crash sites.', 'gray'),
          ('Spend it with Zorp, or use it at a Xenite Altar.', 'dark_gray')],
         model=f'bm:xenite_{c}', stack=64, cat='alien', glint=False)
item('ray_gun', 'minecraft:carrot_on_a_stick', 'Ray Gun', '#7dff6a',
     ['Right-click: a beam of green light,', '7 damage to the first creature it hits.', ('4 shots per Green Xenite shard (from your bag).', 'blue')],
     model='bm:ray_gun', stack=1, cat='alien')
item('tractor_beam', 'minecraft:carrot_on_a_stick', 'Tractor Beam', '#c27dff',
     ['Right-click: pulls items and XP along', 'your gaze, and lifts creatures into the air.', ('Uses Violet Xenite: 5 pulls per shard.', 'blue'),
      ('1.5 second recharge.', 'gray')],
     model='bm:tractor_beam', stack=1, cat='alien')
item('cloaking_device', TOTEM, 'Cloaking Device', '#6af2ff',
     ['Use it: 45 seconds of invisibility', 'and a burst of speed.', ('Recharges for 4 minutes.', 'gray')],
     model='bm:cloaking_device', stack=1, cat='alien',
     comps=dict(_use('minecraft:block.beacon.deactivate'), **{'minecraft:use_cooldown': {'seconds': 240.0, 'cooldown_group': 'bm:cloak'}}))
item('xenite_dowser', TOTEM, 'Xenite Dowser', '#6af2ff',
     ['Use it: the crystal hums and outlines any', 'diamond, emerald or ancient debris', 'within 8 blocks - even through stone.', ('10 second recharge.', 'gray')],
     model='bm:xenite_dowser', stack=1, cat='alien',
     comps=dict(_use('minecraft:block.amethyst_block.resonate'), **{'minecraft:use_cooldown': {'seconds': 10.0, 'cooldown_group': 'bm:dowse'}}))
item('gravity_boots', 'minecraft:iron_boots', 'Gravity Boots', '#c27dff',
     ['Floaty jumps, soft landings.', ('Lower gravity, +jump, +4 Safe Fall', 'blue')],
     model='bm:gravity_boots', stack=1, cat='alien',
     comps={'minecraft:attribute_modifiers': [attr('armor', 2, 'feet'), attr('gravity', -0.3, 'feet', 'add_multiplied_base', 'bm:infuse_gravity_g'),
                                              attr('jump_strength', 0.08, 'feet', ident='bm:infuse_gravity_j'),
                                              attr('safe_fall_distance', 4, 'feet', ident='bm:infuse_gravity_f')]})
item('xenite_altar', TOTEM, 'Xenite Altar', '#7dff6a',
     ['Use it to set it down. Sneak + punch it to pick it up.', ('Right-click it: socket a shard into gear', 'blue'),
      ('(gear in your hand, shard in your off hand).', 'blue'), ('Sneak + right-click: infuse.', 'blue')],
     model='bm:xaltar', stack=1, cat='alien', comps=_use('minecraft:block.stone.place', 0.4))

OFFERS = [(('xenite_green', 16), None, ('ray_gun', 1)), (('xenite_violet', 12), None, ('tractor_beam', 1)),
          (('xenite_cyan', 12), None, ('cloaking_device', 1)), (('xenite_cyan', 10), None, ('xenite_dowser', 1)),
          (('xenite_violet', 16), None, ('gravity_boots', 1)), (('xenite_green', 6), ('xenite_violet', 6), ('xenite_altar', 1)),
          (('xenite_green', 2), None, ('xenite_violet', 1)), (('xenite_violet', 2), None, ('xenite_cyan', 1)),
          (('xenite_cyan', 2), None, ('xenite_green', 1)),
          (('xenite_green', 3), None, ('token', 1)), (('xenite_violet', 3), None, ('token', 1)), (('xenite_cyan', 3), None, ('token', 1))]
SAYS = ["Greetings, Earth-rat.", "Your shinies. Give.", "We come in peace. Mostly.", "The crystals sing. Do you hear them?",
        "Do not tell the cows.", "Our ship is fine. This is how it parks.", "Take me to your cheese.", "Probing is extra."]


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    PREFIX = G.PREFIX
    tick, fast, second = [], [], []
    objs = ['bm.rcd', 'bm.rammo', 'bm.tcd', 'bm.clcd', 'bm.dcd', 'bm.dage', 'bm.xsay']
    G.FUNCS['load'][0:0] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    fin = ['execute rotated as @s run tp @e[tag=bm.new,distance=..2] ~ ~ ~ ~ 0', 'tag @e[tag=bm.new,distance=..2] remove bm.new']
    ident = [F(0), F(0), F(0), F(1)]
    wjson('bm/tags/entity_type/ray_ignore.json', {'values': [f'minecraft:{t}' for t in RAY_IGNORE]})
    wjson('bm/tags/block/dowse.json', {'values': ['minecraft:diamond_ore', 'minecraft:deepslate_diamond_ore', 'minecraft:emerald_ore',
                                                  'minecraft:deepslate_emerald_ore', 'minecraft:ancient_debris']})
    spawn = G.FUNCS['npc/spawn']
    spawn[0:0] = ['execute if entity @s[tag=bm.npc.xenite] run function bm:npc/xenite',
                  'execute if entity @s[tag=bm.npc.alien] run function bm:npc/alien',
                  'execute if entity @s[tag=bm.npc.xaltar] run function bm:npc/xaltar']

    # ================================================================ Xenite deposits (display blocks on an amethyst block)
    for c in COLORS:
        wjson(f'bm/loot_table/xenite/{c}.json', {'type': 'minecraft:command', 'pools': [{'rolls': 1, 'entries': [
            G.loot_entry(f'xenite_{c}', G.uni(2, 4))]}]})
    dep = []
    for c in COLORS:
        d = {'Tags': ['bm.xdep', f'bm.xc_{c}', 'bm.new'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:xdep_{c}'}},
             'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)}, 'view_range': F(1.5),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(1), F(1), F(1)]}}
        dep.append(f'execute if entity @s[tag=bm.xc_{c}] run summon minecraft:item_display ~ ~ ~ {snbt(d)}')
    fn('npc/xenite', dep + ['tag @e[tag=bm.new,distance=..1] remove bm.new'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.xdep] at @s if entity @a[distance=..9] unless block ~ ~ ~ minecraft:amethyst_block run function bm:p24/xdep/broke')
    fn('p24/xdep/broke', ['execute as @e[type=minecraft:item,distance=..1.6] if items entity @s contents minecraft:amethyst_block run kill @s'] +
       [f'execute if entity @s[tag=bm.xc_{c}] run loot spawn ~ ~ ~ loot bm:xenite/{c}' for c in COLORS] +
       ['particle minecraft:end_rod ~ ~ ~ 0.3 0.3 0.3 0.06 16', 'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 1 0.6',
        'playsound minecraft:block.amethyst_block.chime block @a[distance=..16] ~ ~ ~ 1 1.4', 'kill @s'])
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.xdep] at @s if entity @a[distance=..16] run function bm:p24/xdep/glint')
    fn('p24/xdep/glint', ['execute store result score #g bm.rng run random value 1..6', 'execute unless score #g bm.rng matches 1 run return 0'] +
       [f'execute if entity @s[tag=bm.xc_{c}] run particle minecraft:dust{{color:[{int(COLORS[c][0][1:3], 16) / 255:.2f},{int(COLORS[c][0][3:5], 16) / 255:.2f},{int(COLORS[c][0][5:7], 16) / 255:.2f}],scale:0.8}} ~ ~0.9 ~ 0.3 0.4 0.3 0 3'
        for c in COLORS])

    # ================================================================ Zorp, the alien trader (stationary at crash sites)
    O = []
    for buy, buyB, sell in OFFERS:
        O.append(G.offer(buy, sell, buyB) if buyB else G.offer(buy, sell))
    trader = {'NoAI': B(1), 'Invulnerable': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'DespawnDelay': Int(0),
              'Tags': ['bm.npc', 'bm.npc_alien', 'bm.new'], 'CustomName': T('Zorp, Collector of Shinies', '#7dff6a', bold=True), 'CustomNameVisible': B(0),
              'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
              'attributes': [{'id': 'minecraft:scale', 'base': D(0.75)}], 'Offers': {'Recipes': O}}
    sprite = G.rat_sprite('bm:alien3d', ['bm.npc', 'bm.new', 'bm.rat_sprite', 'bm.alien_sprite', 'bm.td', 'bm.r3d'], 1.0)
    fn('npc/alien', [f'summon minecraft:wandering_trader ~ ~ ~ {snbt(trader)}', sprite] + fin)
    import zlib
    blob = snbt(O)
    ver = zlib.crc32(blob.encode()) % 1000000000
    fn('p17/npc/alien', [f'data modify entity @s Offers.Recipes set value {blob}', f'scoreboard players set @s bm.ofv {ver}'])
    second.append(f'execute as @e[tag=bm.npc_alien] unless score @s bm.ofv matches {ver} run function bm:p17/npc/alien')
    fast.append('execute as @e[type=minecraft:item_display,tag=bm.alien_sprite] at @s if entity @a[distance=..24] run particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.005 1')
    # he mutters too (same pop-in bubbles as the market)
    def bubble(text):
        d = {'Tags': ['bm.bubble', 'bm.bnew'], 'text': T(text, '#b8ffb0'), 'billboard': 'center', 'background': Int(1879048192),
             'line_width': Int(150), 'brightness': {'block': Int(15), 'sky': Int(15)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(0), F(0), F(0)]}}
        return f'summon minecraft:text_display ~ ~1.75 ~ {snbt(d)}'
    fn('p24/alien_say', ['execute store result score @s bm.xsay run random value 9..16',
                         'execute if entity @e[type=minecraft:text_display,tag=bm.bubble,distance=..2.5] run return 0',
                         f'execute store result score #l bm.rng run random value 1..{len(SAYS)}'] +
       [f'execute if score #l bm.rng matches {i} run {bubble(t)}' for i, t in enumerate(SAYS, 1)] +
       ['playsound minecraft:entity.allay.ambient_without_item neutral @a[distance=..8] ~ ~ ~ 0.4 0.6'])
    second += ['execute as @e[tag=bm.npc_alien] at @s if entity @a[distance=..5,gamemode=!spectator] unless score @s bm.xsay matches 1.. run function bm:p24/alien_say',
               'scoreboard players remove @e[tag=bm.npc_alien,scores={bm.xsay=1..}] bm.xsay 1']

    # ================================================================ alien tech (carrot-on-a-stick clicks share the grappling hook's hook)
    gu = G.FUNCS['p21/grap/use']
    gu[1:1] = ['execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"ray_gun"}] run return run function bm:p24/ray/fire',
               'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"tractor_beam"}] run return run function bm:p24/tractor/use']
    tick += ['scoreboard players remove @a[scores={bm.rcd=1..}] bm.rcd 1', 'scoreboard players remove @a[scores={bm.tcd=1..}] bm.tcd 1']
    green = '*[minecraft:custom_data~{bm:"xenite_green"}]'
    fn('p24/ray/fire', ['execute if score @s bm.rcd matches 1.. run return 0',
                        'execute unless score @s bm.rammo matches 1.. store result score #s bm.rng run clear @s ' + green + ' 0',
                        'execute unless score @s bm.rammo matches 1.. if score #s bm.rng matches 0 run return run function bm:p24/ray/empty',
                        f'execute unless score @s bm.rammo matches 1.. run clear @s {green} 1',
                        'execute unless score @s bm.rammo matches 1.. run scoreboard players set @s bm.rammo 4',
                        'scoreboard players remove @s bm.rammo 1', 'scoreboard players set @s bm.rcd 12',
                        'tag @s add bm.shooter', 'scoreboard players set #rr bm.rng 100',
                        'playsound minecraft:block.beacon.power_select player @a[distance=..20] ~ ~ ~ 0.8 2',
                        'execute anchored eyes positioned ^ ^ ^0.6 run function bm:p24/ray/step',
                        'tag @s remove bm.shooter',
                        title('@s', 'actionbar', [T('Ray Gun: ', '#7dff6a'), {'score': {'name': '@s', 'objective': 'bm.rammo'}, 'color': 'white'},
                                                  T(' shots left in this crystal', 'gray')])])
    fn('p24/ray/empty', ['scoreboard players set @s bm.rcd 10', 'playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 1 1.6',
                         title('@s', 'actionbar', T('Out of power - carry Green Xenite shards.', 'red'))])
    fn('p24/ray/step', ['particle minecraft:dust{color:[0.49,1.0,0.42],scale:0.7} ~ ~ ~ 0 0 0 0 1 force @a[distance=..48]',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.2 10',
                        'execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[dx=0,dy=0,dz=0,type=!#bm:ray_ignore,tag=!bm.npc,tag=!bm.frogpet,tag=!bm.wilfrey,tag=!bm.donado,tag=!bm.wil_body] positioned ~0.5 ~0.5 ~0.5 run return run function bm:p24/ray/hit',
                        'scoreboard players remove #rr bm.rng 1',
                        'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^0.4 run function bm:p24/ray/step'])
    fn('p24/ray/hit', ['execute positioned ~-0.5 ~-0.5 ~-0.5 as @e[dx=0,dy=0,dz=0,type=!#bm:ray_ignore,tag=!bm.npc,tag=!bm.frogpet,tag=!bm.wilfrey,tag=!bm.donado,tag=!bm.wil_body,limit=1,sort=nearest] run damage @s 7 minecraft:indirect_magic by @a[tag=bm.shooter,limit=1]',
                       'particle minecraft:dust{color:[0.49,1.0,0.42],scale:1.6} ~ ~ ~ 0.25 0.25 0.25 0 20 force @a[distance=..48]',
                       'playsound minecraft:entity.generic.hurt hostile @a[distance=..16] ~ ~ ~ 0.6 1.6'])
    fn('p24/tractor/use', ['execute if score @s bm.tcd matches 1.. run return 0', 'scoreboard players set @s bm.tcd 30',
                           'scoreboard players set #rr bm.rng 24', 'tag @s add bm.puller',
                           'playsound minecraft:block.beacon.ambient player @a[distance=..20] ~ ~ ~ 1 1.8',
                           'execute anchored eyes positioned ^ ^ ^1 run function bm:p24/tractor/step', 'tag @s remove bm.puller'])
    fn('p24/tractor/step', ['particle minecraft:reverse_portal ~ ~ ~ 0.15 0.15 0.15 0 3',
                            'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                            'tp @e[type=minecraft:item,distance=..2.2] @a[tag=bm.puller,limit=1]',
                            'tp @e[type=minecraft:experience_orb,distance=..2.2] @a[tag=bm.puller,limit=1]',
                            'effect give @e[distance=..1.6,type=!#bm:ray_ignore,tag=!bm.npc,tag=!bm.frogpet,tag=!bm.wilfrey,tag=!bm.donado,tag=!bm.wil_body] minecraft:levitation 2 1 true',
                            'scoreboard players remove #rr bm.rng 1',
                            'execute if score #rr bm.rng matches 1.. positioned ^ ^ ^1 run function bm:p24/tractor/step'])
    G.consume_adv('cloaking_device', 'bm:p24/cloak')
    second.append('scoreboard players remove @a[scores={bm.clcd=1..}] bm.clcd 1')
    fn('p24/cloak', ['advancement revoke @s only bm:consume/cloaking_device', give('cloaking_device'),
                     'execute if score @s bm.clcd matches 1.. run return run ' + title('@s', 'actionbar', [T('Still recharging: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.clcd'}, 'color': 'white'}, T(' s', 'gray')]),
                     'scoreboard players set @s bm.clcd 240',
                     'effect give @s minecraft:invisibility 45 0 true', 'effect give @s minecraft:speed 45 0 true',
                     'particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.6 0.3 0.05 40',
                     title('@s', 'actionbar', T('You fade from sight.', '#6af2ff'))])
    # the dowser: scans every block within 8 (17x17x17) once per use
    G.consume_adv('xenite_dowser', 'bm:p24/dowse/use')
    second += ['scoreboard players remove @a[scores={bm.dcd=1..}] bm.dcd 1',
               'scoreboard players add @e[type=minecraft:marker,tag=bm.dhit] bm.dage 1',
               'execute as @e[type=minecraft:marker,tag=bm.dhit] at @s run particle minecraft:end_rod ~ ~ ~ 0.25 0.25 0.25 0 6 force @a[distance=..24]',
               'kill @e[type=minecraft:marker,tag=bm.dhit,scores={bm.dage=8..}]']
    fn('p24/dowse/use', ['advancement revoke @s only bm:consume/xenite_dowser', give('xenite_dowser'),
                         'execute if score @s bm.dcd matches 1.. run return run ' + title('@s', 'actionbar', T('The crystal is still ringing...', 'gray')),
                         'scoreboard players set @s bm.dcd 10', 'scoreboard players set #dn bm.rng 0', 'scoreboard players set #dz bm.rng -8',
                         'execute positioned ~ ~ ~-8 run function bm:p24/dowse/z',
                         'execute if score #dn bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('Silence. Nothing precious within 8 blocks.', 'gray')),
                         'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.8',
                         title('@s', 'actionbar', [T('The crystal hums: ', '#6af2ff'), {'score': {'name': '#dn', 'objective': 'bm.rng'}, 'color': 'white'},
                                                   T(' rich deposit block(s) nearby! (marked with light)', '#6af2ff')])])
    fn('p24/dowse/z', ['scoreboard players set #dy bm.rng -8', 'execute positioned ~ ~-8 ~ run function bm:p24/dowse/y',
                       'scoreboard players add #dz bm.rng 1', 'execute if score #dz bm.rng matches ..8 positioned ~ ~ ~1 run function bm:p24/dowse/z'])
    fn('p24/dowse/y', ['scoreboard players set #dx bm.rng -8', 'execute positioned ~-8 ~ ~ run function bm:p24/dowse/x',
                       'scoreboard players add #dy bm.rng 1', 'execute if score #dy bm.rng matches ..8 positioned ~ ~1 ~ run function bm:p24/dowse/y'])
    fn('p24/dowse/x', ['execute if block ~ ~ ~ #bm:dowse run function bm:p24/dowse/hit',
                       'scoreboard players add #dx bm.rng 1', 'execute if score #dx bm.rng matches ..8 positioned ~1 ~ ~ run function bm:p24/dowse/x'])
    fn('p24/dowse/hit', ['scoreboard players add #dn bm.rng 1',
                         'execute if score #dn bm.rng matches ..6 align xyz run summon minecraft:marker ~0.5 ~0.5 ~0.5 {Tags:["bm.dhit"]}'])

    # ================================================================ sockets + infusions (item modifiers)
    for c, (lore, mods) in SOCKET.items():
        col = COLORS[c][0]
        wjson(f'bm/item_modifier/p24/socket_{c}.json', [
            {'function': 'minecraft:set_attributes', 'replace': False,
             'modifiers': [{'attribute': f'minecraft:{a}', 'id': f'bm:socket_{c}_{s}', 'amount': amt, 'operation': op, 'slot': 'any'} for a, amt, op, s in mods]},
            {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_sock:1b,bm_sockc:"{c}",bmv:{ITEM_VERSION}}}'},
            {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T(f'◆ {COLORS[c][1]} socket: {lore}', col)]}])
    wjson('bm/item_modifier/p24/infuse_gravity.json', [
        {'function': 'minecraft:set_attributes', 'replace': False,
         'modifiers': [{'attribute': f'minecraft:{a}', 'id': f'bm:infuse_gravity_{s}', 'amount': amt, 'operation': op, 'slot': 'feet'} for a, amt, op, s in GRAVITY]},
        {'function': 'minecraft:set_custom_data', 'tag': f'{{bm_inf:"gravity",bmv:{ITEM_VERSION}}}'},
        {'function': 'minecraft:set_lore', 'mode': 'append', 'lore': [T('✦ Gravity-infused: floaty jumps, soft landings', '#c27dff')]}])
    for n in range(1, 9):
        wjson(f'bm/item_modifier/p24/take_{n}.json', {'function': 'minecraft:set_count', 'count': -n, 'add': True})
    # restamps (phase18) rewrite a Black Market item's components: put its socket / infusion back afterwards
    rs = G.FUNCS['p18/refresh/slot']
    k = next(i for i, l in enumerate(rs) if 'rf.iid set from entity' in l)
    rs[k + 1:k + 1] = ['$data modify storage bm:tmp rf.sock set from entity @s $(path).components."minecraft:custom_data".bm_sockc',
                       '$data modify storage bm:tmp rf.inf set from entity @s $(path).components."minecraft:custom_data".bm_inf']
    rs += [f'execute if data storage bm:tmp rf.iid if data storage bm:tmp {{rf:{{sock:"{c}"}}}} run function bm:p24/resock_{c} with storage bm:tmp rf' for c in SOCKET]
    rs += ['execute if data storage bm:tmp rf.iid if data storage bm:tmp {rf:{inf:"gravity"}} run function bm:p24/reinfuse_gravity with storage bm:tmp rf']
    for c in SOCKET: fn(f'p24/resock_{c}', [f'$item modify entity @s $(slot) bm:p24/socket_{c}'])
    fn('p24/reinfuse_gravity', ['$item modify entity @s $(slot) bm:p24/infuse_gravity'])

    # ================================================================ the Xenite Altar (placed like the trophies; one built into every crash site)
    alt_disp = {'Tags': ['bm.xalt', 'bm.new'], 'teleport_duration': Int(3),
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:xaltar'}},
                'item_display': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(12)},
                'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1), F(1), F(1)]}}
    alt_box = {'Tags': ['bm.xalt_hit', 'bm.new'], 'width': F(0.9), 'height': F(1.3), 'response': B(1)}
    fn('npc/xaltar', [f'summon minecraft:item_display ~ ~ ~ {snbt(alt_disp)}', f'summon minecraft:interaction ~ ~ ~ {snbt(alt_box)}'] + fin)
    G.consume_adv('xenite_altar', 'bm:p24/altar/place')
    fn('p24/altar/place', ['advancement revoke @s only bm:consume/xenite_altar', 'scoreboard players set #placed bm.rng 0',
                           'scoreboard players set #ray bm.rng 25', 'tag @s add bm.placer',
                           'execute anchored eyes positioned ^ ^ ^ run function bm:p24/altar/ray', 'tag @s remove bm.placer',
                           'execute if score #placed bm.rng matches 0 unless entity @s[gamemode=creative] run ' + give('xenite_altar'),
                           'execute if score #placed bm.rng matches 0 run ' + title('@s', 'actionbar', T('Look at the top of a block within 5 blocks to set it down.', 'gray'))])
    fn('p24/altar/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p24/altar/hit',
                         'scoreboard players remove #ray bm.rng 1',
                         'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p24/altar/ray'])
    fn('p24/altar/hit', ['execute align xyz positioned ~0.5 ~1 ~0.5 unless block ~ ~ ~ #minecraft:replaceable run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 if entity @e[type=minecraft:interaction,tag=bm.xalt_hit,distance=..0.6] run return 0',
                         'execute align xyz positioned ~0.5 ~1 ~0.5 run function bm:p24/altar/spawn'])
    fn('p24/altar/spawn', [f'summon minecraft:item_display ~ ~ ~ {snbt(alt_disp)}', f'summon minecraft:interaction ~ ~ ~ {snbt(alt_box)}',
                           'tag @e[type=minecraft:interaction,tag=bm.new,distance=..0.5] add bm.xalt_own',
                           'execute rotated as @a[tag=bm.placer,limit=1] run tp @e[tag=bm.new,distance=..0.5] ~ ~ ~ ~180 0',
                           'tag @e[tag=bm.new,distance=..0.5] remove bm.new', 'scoreboard players set #placed bm.rng 1',
                           'playsound minecraft:block.amethyst_block.place block @a[distance=..16] ~ ~ ~ 1 0.8',
                           'particle minecraft:end_rod ~ ~0.8 ~ 0.3 0.3 0.3 0.02 12'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.xalt_hit] if data entity @s interaction at @s run function bm:p24/altar/click',
             'execute as @e[type=minecraft:interaction,tag=bm.xalt_hit] if data entity @s attack at @s run function bm:p24/altar/punch',
             'execute as @e[type=minecraft:item_display,tag=bm.xalt] at @s if entity @a[distance=..16] run particle minecraft:end_rod ~ ~1.3 ~ 0.15 0.1 0.15 0.01 1']
    # 1.17: a plain punch (some weapons' right-click lands as a punch) works the altar like a right-click; only a
    # SNEAKING punch picks a placed altar up
    fn('p24/altar/punch', ['scoreboard players set #sn bm.rng 0',
                           'execute on attacker if predicate bm:p20/sneaking run scoreboard players set #sn bm.rng 1',
                           'execute if score #sn bm.rng matches 0 on attacker at @s run function bm:p24/altar/use',
                           'data remove entity @s attack',
                           'execute if score #sn bm.rng matches 0 run return 0', 'execute unless entity @s[tag=bm.xalt_own] run return 0',
                           'loot spawn ~ ~0.4 ~ loot bm:items/xenite_altar', 'kill @e[type=minecraft:item_display,tag=bm.xalt,distance=..0.3]',
                           'particle minecraft:poof ~ ~0.5 ~ 0.2 0.2 0.2 0.02 6', 'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 1 0.9', 'kill @s'])
    # 1.16: read the clicker (on target) BEFORE clearing the interaction - clearing it first made every altar click do nothing
    fn('p24/altar/click', ['execute on target at @s run function bm:p24/altar/use', 'data remove entity @s interaction'])
    shard = lambda c: f'*[minecraft:custom_data~{{bm:"xenite_{c}"}}]'
    use = ['execute if predicate bm:p20/sneaking run return run function bm:p24/altar/infuse',
           'execute unless items entity @s weapon.mainhand *[minecraft:max_damage] run return run function bm:p24/altar/help',
           'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm_sock:1b}] run return run ' + title('@s', 'actionbar', T('That item already has a socket.', 'gray'))]
    for c in COLORS:
        use.append(f'execute if items entity @s weapon.offhand {shard(c)} run return run function bm:p24/altar/sock_{c}')
    use.append('function bm:p24/altar/help')
    fn('p24/altar/use', use)
    for c, (lore, _) in SOCKET.items():
        fn(f'p24/altar/sock_{c}', [f'item modify entity @s weapon.mainhand bm:p24/socket_{c}', 'item modify entity @s weapon.offhand bm:p24/take_1',
                                   'playsound minecraft:block.amethyst_block.resonate player @a[distance=..12] ~ ~ ~ 1 1.2',
                                   'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.3 0.3 0.05 20',
                                   title('@s', 'actionbar', T(f'Socketed! {COLORS[c][1]}: {lore}', COLORS[c][0]))])
    fn('p24/altar/help', [tellraw('@s', PREFIX + [T('Xenite Altar: ', '#7dff6a', bold=True), T('right-click with gear in your hand and a Xenite shard in your off hand to socket it (one per item). ', 'gray'),
                                                  T('Sneak + punch a placed altar to pick it up. ', 'gray'),
                                                  T('Sneak + right-click to infuse: ', 'gray'),
                                                  T('boots + 6 violet, compass + 6 cyan, crossbow + 8 green, glass bottle + 4 cyan, ender pearl + 6 violet.', '#c27dff')])])
    inf = []
    for test, c, n, res, consume in INFUSIONS:
        name = res if res != 'gravity' else 'gravity_boots_inf'
        chk = f'execute if items entity @s weapon.mainhand {test} if items entity @s weapon.offhand {shard(c)}'
        inf.append(f'{chk} run return run function bm:p24/altar/inf_{name}')
        body = [f'execute store result score #n bm.rng run data get entity @s equipment.offhand.count',
                f'execute if score #n bm.rng matches ..{n - 1} run return run ' + title('@s', 'actionbar', T(f'You need {n} {COLORS[c][1]} shards in your off hand.', 'gray')),
                f'item modify entity @s weapon.offhand bm:p24/take_{n}']
        if res == 'gravity':
            body = [f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm_inf:"gravity"}}] run return run ' + title('@s', 'actionbar', T('Those boots are already infused.', 'gray')),
                    'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"gravity_boots"}] run return run ' + title('@s', 'actionbar', T('Those boots are already infused.', 'gray'))] + body + \
                   ['item modify entity @s weapon.mainhand bm:p24/infuse_gravity']
            msg = 'The boots grow light as a feather.'
        else:
            body += ['item modify entity @s weapon.mainhand bm:p24/take_1', give(res)]
            msg = f'The altar hums - you made a {G.ITEMS[res]["name"]}!'
        body += ['playsound minecraft:block.beacon.activate player @a[distance=..12] ~ ~ ~ 1 1.4', 'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.06 30',
                 title('@s', 'actionbar', T(msg, COLORS[c][0]))]
        fn(f'p24/altar/inf_{name}', body)
    inf.append('function bm:p24/altar/help')
    fn('p24/altar/infuse', inf)

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def post_admin(G):
    G.FUNCS['admin/help'] += [
        G.tellraw('@s', [T('/function bm:admin/place_crash_site', 'yellow'), T('  builds a crashed saucer at your feet', 'gray')]),
        G.tellraw('@s', [T('/locate structure bm:crash_site', 'yellow'), T('  finds the nearest crash site', 'gray')])]
    G.fn('admin/place_crash_site', ['place template bm:crash_site ~-14 ~-5 ~-14',
                                    G.tellraw('@s', G.PREFIX + [T('Crash site placed around you.', 'gray')])])


# ===================================================================== the crash site structure
SX, SY, SZ = 29, 18, 29
GROUND = 5


def build_crash_site():
    from structures import Build
    rnd = random.Random(19470708)
    Bd = Build(SX, SY, SZ)
    S = Bd.set
    cx, cz = 14, 14
    # foundation + crater
    for x in range(SX):
        for z in range(SZ):
            d = math.hypot(x - cx, z - cz)
            for y in range(0, GROUND):
                Bd.set(x, y, z, 'dirt' if y >= GROUND - 2 else rnd.choice(['stone', 'stone', 'andesite', 'tuff']))
            if d > 13.5:
                S(x, GROUND, z, rnd.choice(['grass_block[snowy=false]', 'grass_block[snowy=false]', 'coarse_dirt']))
                continue
            depth = max(0, int(round(3.2 * (1 - (d / 11.5) ** 2)))) if d < 11.5 else 0
            top = GROUND - depth
            for y in range(top + 1, SY): S(x, y, z, 'air')
            r = rnd.random()
            S(x, top, z, 'magma_block' if (r < 0.04 and d < 9) else 'blackstone' if r < 0.22 else 'coarse_dirt' if r < 0.55 else 'gravel' if r < 0.75 else 'tuff')
            if 11.5 <= d <= 13.5 and rnd.random() < 0.5:                       # thrown-up rim
                S(x, GROUND + 1, z, rnd.choice(['coarse_dirt', 'dirt', 'gravel', 'rooted_dirt']))
    # the saucer: a disc of radius 7, tilted ~16 degrees, its low edge buried in the crater wall
    tilt = math.tan(math.radians(16))
    base_y = GROUND - 1
    hull = {}
    for x in range(cx - 8, cx + 9):
        for z in range(cz - 8, cz + 9):
            d = math.hypot(x - cx, z - cz)
            if d > 7.4: continue
            y = base_y + 2 + round((x - cx) * tilt)
            hull[(x, z)] = (y, d)
            S(x, y, z, 'light_gray_concrete' if d < 5.5 else 'iron_block')
            if d >= 6.4:                                                         # the rim, with running lights
                S(x, y + 1, z, 'sea_lantern' if (x + z) % 3 == 0 else 'iron_block')
            elif d < 3.6:                                                        # the glass dome
                for h in range(1, 4 - (1 if d > 2.5 else 0)):
                    S(x, y + h, z, 'light_blue_stained_glass' if h < 3 or d < 1.5 else 'air')
                S(x, y + (3 if d <= 2.5 else 2), z, 'light_blue_stained_glass')
            else:
                S(x, y + 1, z, 'smooth_stone_slab[type=bottom,waterlogged=false]' if (x * 7 + z) % 5 else 'end_rod[facing=up]')
            for yy in range(GROUND - 3, y):                                       # the saucer rests on the dirt it ploughed up
                S(x, yy, z, 'coarse_dirt' if (x + yy + z) % 3 else 'gravel')
    # inside the dome: a pilot's seat and a cracked console
    y0 = hull[(cx, cz)][0]
    S(cx, y0 + 1, cz, 'quartz_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]')
    S(cx - 1, y0 + 1, cz, 'cyan_stained_glass'); S(cx - 1, y0 + 2, cz, 'air')
    # broken antenna, scattered debris, a smouldering engine
    hx, hz = cx + 6, cz - 3
    for h in range(1, 4): S(hx, hull[(hx, hz)][0] + h, hz, 'lightning_rod[facing=up,powered=false,waterlogged=false]')
    S(hx + 1, hull[(hx, hz)][0] + 4, hz, 'lightning_rod[facing=east,powered=false,waterlogged=false]')
    for (x, z) in [(4, 9), (5, 20), (21, 23), (23, 6), (9, 4), (18, 25), (6, 14)]:
        y = max(yy for yy in range(SY) if (x, yy, z) in Bd.b and Bd.b[(x, yy, z)] not in ('minecraft:air',)) + 1
        S(x, y, z, rnd.choice(['iron_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]', 'iron_bars', 'heavy_core',
                               'iron_chain[axis=x,waterlogged=false]', 'light_gray_concrete', 'polished_andesite_slab[type=bottom,waterlogged=false]']))
    ex, ez = cx - 7, cz + 4                                                    # engine on the low side: smoke and soul fire
    ey = max(yy for yy in range(SY) if Bd.b.get((ex, yy, ez), 'minecraft:air') != 'minecraft:air') + 1
    S(ex, ey, ez, 'soul_campfire[facing=north,lit=true,signal_fire=true,waterlogged=false]')
    S(ex, ey - 1, ez, 'hay_block[axis=y]')
    # Xenite deposits on the crater floor (an amethyst block each; the crystal model is spawned by its marker)
    spots = [(8, 12, 'green'), (10, 18, 'violet'), (19, 20, 'cyan'), (20, 9, 'green'), (15, 22, 'violet'), (7, 16, 'cyan'), (17, 6, 'cyan')]
    for (x, z, c) in spots:
        if (x, z) in hull: continue
        top = max(yy for yy in range(SY) if Bd.b.get((x, yy, z), 'minecraft:air') != 'minecraft:air')
        S(x, top + 1, z, 'amethyst_block')
        Bd.marker(x + 0.5, top + 1.5, z + 0.5, ['bm.npc_spawn', 'bm.npc.xenite', f'bm.xc_{c}'], 0)
    # Zorp and the built-in altar beside the saucer's hatch (east side, up out of the crater)
    zx, zz = 23, 15
    zy = max(yy for yy in range(SY) if Bd.b.get((zx, yy, zz), 'minecraft:air') != 'minecraft:air') + 1
    Bd.marker(zx + 0.5, zy, zz + 0.5, ['bm.npc_spawn', 'bm.npc.alien'], 90)
    ax, az = 23, 12
    ay = max(yy for yy in range(SY) if Bd.b.get((ax, yy, az), 'minecraft:air') != 'minecraft:air') + 1
    Bd.marker(ax + 0.5, ay, az + 0.5, ['bm.npc_spawn', 'bm.npc.xaltar'], 90)
    for (x, z) in [(24, 17), (24, 10)]:
        y = max(yy for yy in range(SY) if Bd.b.get((x, yy, z), 'minecraft:air') != 'minecraft:air') + 1
        S(x, y, z, 'end_rod[facing=up]')
    Bd.sign(23, zy, 18, 'birch_sign[rotation=4,waterlogged=false]', ['ZORP', 'Collector of', 'Shinies', 'Xenite only.'], color='lime', glow=True)
    return Bd


# ===================================================================== resource pack: textures, 3D models, icons
def textures():
    """Custom 16x16 block-atlas textures (crystal facets, ore, alien skin/suit/eyes)."""
    from PIL import Image
    rnd = random.Random(7)
    out = {}
    pal = {'green': ((40, 140, 40), (125, 255, 106), (210, 255, 200)), 'violet': ((90, 40, 140), (194, 125, 255), (235, 210, 255)),
           'cyan': ((20, 110, 130), (106, 242, 255), (210, 252, 255)), 'red': ((120, 20, 20), (255, 74, 74), (255, 216, 216))}      # red: 2.13
    for c, (dk, md, lt) in pal.items():
        im = Image.new('RGBA', (16, 16))
        for x in range(16):
            for y in range(16):
                t = ((x + y) % 7) / 6.0
                base = [int(dk[i] + (md[i] - dk[i]) * t) for i in range(3)]
                if (x - y) % 5 == 0: base = list(lt)
                im.putpixel((x, y), tuple(base) + (255,))
        out[f'xen_{c}'] = im
        ore = Image.new('RGBA', (16, 16))
        for x in range(16):
            for y in range(16):
                g = 38 + rnd.randrange(22)
                ore.putpixel((x, y), (g, g, g + 6, 255))
        for _ in range(9):
            x0, y0 = rnd.randrange(1, 15), rnd.randrange(1, 15)
            for (dx, dy) in ((0, 0), (1, 0), (0, 1)):
                ore.putpixel((min(15, x0 + dx), min(15, y0 + dy)), md + (255,))
            ore.putpixel((x0, y0), lt + (255,))
        out[f'xenore_{c}'] = ore
    skin = Image.new('RGBA', (16, 16)); suit = Image.new('RGBA', (16, 16)); eye = Image.new('RGBA', (16, 16))
    for x in range(16):
        for y in range(16):
            n = rnd.randrange(10)
            skin.putpixel((x, y), (150 + n, 175 + n, 150 + n, 255))
            suit.putpixel((x, y), (190 + n, 196 + n, 205 + n, 255) if y % 4 else (120, 126, 140, 255))
            eye.putpixel((x, y), (8, 8, 14, 255))
    for (x, y) in ((3, 3), (4, 3), (3, 4)): eye.putpixel((x, y), (200, 255, 210, 255))
    out['alien_skin'], out['alien_suit'], out['alien_eye'] = skin, suit, eye
    return out


def _cube(fr, to, tex, rot=None):
    from gen_rp import cube
    e = cube(fr, to, tex)
    if rot: e['rotation'] = rot
    return e


def models():
    """3D models (name -> (textures, elements)) merged into gen_rp's HATS table."""
    M = {}
    for c in COLORS:
        t = {'o': f'bm:block/xenore_{c}', 'x': f'bm:block/xen_{c}'}
        els = [_cube((-0.1, -0.1, -0.1), (16.1, 16.1, 16.1), 'o'),
               _cube((6, 16, 6), (10, 27, 10), 'x', {'origin': [8, 16, 8], 'axis': 'x', 'angle': 22.5}),
               _cube((2.5, 16, 8.5), (5.5, 23, 11.5), 'x', {'origin': [4, 16, 10], 'axis': 'z', 'angle': -22.5}),
               _cube((10.5, 16, 3), (13.5, 22, 6), 'x', {'origin': [12, 16, 4.5], 'axis': 'z', 'angle': 22.5}),
               _cube((9, 16, 10.5), (12, 20, 13.5), 'x', {'origin': [10.5, 16, 12], 'axis': 'x', 'angle': -22.5}),
               _cube((3, 16, 2.5), (5, 19, 4.5), 'x')]
        M[f'xdep_{c}'] = (t, els)
    tex = {'s': 'bm:block/alien_skin', 'u': 'bm:block/alien_suit', 'e': 'bm:block/alien_eye'}
    M['alien3d'] = (tex, [
        _cube((6, 0, 7), (7.5, 7, 9), 's'), _cube((8.5, 0, 7), (10, 7, 9), 's'),          # legs
        _cube((5.5, 7, 6.5), (10.5, 14, 9.5), 'u'),                                        # torso (suit)
        _cube((4, 8, 7.5), (5.5, 14, 8.5), 's'), _cube((10.5, 8, 7.5), (12, 14, 8.5), 's'),  # long thin arms
        _cube((7.5, 14, 7.5), (8.5, 15.5, 8.5), 's'),                                      # neck
        _cube((4, 15.5, 4), (12, 23, 12), 's'), _cube((4.5, 23, 4.5), (11.5, 25, 11.5), 's'),  # the big head
        _cube((4.6, 18, 3.9), (7.4, 20.6, 4.0), 'e', {'origin': [6, 19, 4], 'axis': 'z', 'angle': -22.5}),   # almond eyes
        _cube((8.6, 18, 3.9), (11.4, 20.6, 4.0), 'e', {'origin': [10, 19, 4], 'axis': 'z', 'angle': 22.5}),
        _cube((7.3, 16.3, 3.95), (8.7, 16.6, 4.0), 'e')])
    t = {'b': 'minecraft:block/polished_blackstone', 'r': 'minecraft:block/polished_blackstone_bricks', 'c': 'minecraft:block/chiseled_polished_blackstone',
         'g': 'bm:block/xen_green', 'v': 'bm:block/xen_violet', 'y': 'bm:block/xen_cyan'}
    M['xaltar'] = (t, [_cube((2, 0, 2), (14, 3, 14), 'b'), _cube((5, 3, 5), (11, 11, 11), 'r'), _cube((3, 11, 3), (13, 13, 13), 'c'),
                       _cube((6.5, 14.5, 6.5), (9.5, 20, 9.5), 'g', {'origin': [8, 17, 8], 'axis': 'y', 'angle': 45}),
                       _cube((3.5, 13, 3.5), (5, 16, 5), 'v'), _cube((11, 13, 11), (12.5, 16, 12.5), 'y'),
                       _cube((11, 13, 3.5), (12.5, 15, 5), 'g'), _cube((3.5, 13, 11), (5, 15, 12.5), 'v')])
    return M


DISPLAY_3D = ('xdep_', 'alien3d', 'xaltar')


def icons(grid):
    I = {}
    for c, cols in {'green': ('#1f6b1f', '#7dff6a', '#e0ffd8'), 'violet': ('#4b1a6e', '#c27dff', '#f0dcff'), 'cyan': ('#145a66', '#6af2ff', '#e0fcff')}.items():
        I[f'xenite_{c}'] = grid([
            '................', '.......D........', '......DLD.......', '......DLMD......', '.....DLMMD......', '.....DLMMMD.....',
            '....DLMMMMD.....', '....DLMMMMMD....', '....DLMMMMMD....', '.....DLMMMD.....', '.....DLMMMD.....', '......DLMD......',
            '......DMD.......', '.......D........', '................', '................'], dict(D=cols[0], M=cols[1], L=cols[2]))
    I['ray_gun'] = grid([
        '................', '...........GG...', '..........GLLG..', '.........SSGGS..', '........SSSSS...', '.......SSDSS....',
        '......SSDSS.....', '.....SKSSS......', '....SKKSS.......', '...KKK.S........', '..KKK...........', '..KK............',
        '................', '................', '................', '................'], dict(G='#7dff6a', L='#e0ffd8', S='#b8bec8', D='#6a707c', K='#3a3f4a'))
    I['tractor_beam'] = grid([
        '..........VVV...', '.........VLLLV..', '.........VLLLV..', '..........VVV...', '.........SS.....', '........SS......',
        '.......SS.......', '......SDS.......', '.....SDS........', '....KKS.........', '...KKK..........', '..KKK...........',
        '..KK............', '................', '................', '................'], dict(V='#c27dff', L='#f0dcff', S='#b8bec8', D='#6a707c', K='#3a3f4a'))
    I['cloaking_device'] = grid([
        '................', '.....SSSSSS.....', '....SCCCCCCS....', '...SCLLCCCCCS...', '...SCLCCCCCCS...', '...SCCCCCCCCS...',
        '...SCCCCCCCCS...', '...SCCCCCCCCS...', '...SCCCCCCLCS...', '....SCCCCCCS....', '.....SSSSSS.....', '......K..K......',
        '.....KK..KK.....', '................', '................', '................'], dict(S='#b8bec8', C='#6af2ff', L='#e0fcff', K='#3a3f4a'))
    I['xenite_dowser'] = grid([
        '.......CC.......', '......CLLC......', '......CLCC......', '.......CC.......', '.......SS.......', '......SSSS......',
        '.....SS..SS.....', '....SS....SS....', '....S......S....', '....S..CC..S....', '....S......S....', '....SS....SS....',
        '.....SS..SS.....', '......SSSS......', '................', '................'], dict(C='#6af2ff', L='#e0fcff', S='#b8bec8'))
    I['gravity_boots'] = grid([
        '................', '................', '....SSS..SSS....', '....SVS..SVS....', '....SVS..SVS....', '....SVS..SVS....',
        '....SVS..SVS....', '....SVSS.SVSS...', '...SVVVS.SVVVS..', '..SVVVVSSVVVVS..', '..SSSSSSSSSSSS..', '...PP..PP.PP....',
        '..P..P....P.P...', '................', '................', '................'], dict(S='#b8bec8', V='#c27dff', P='#f0dcff'))
    return I
