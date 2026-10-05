"""Phase 1.22 / 2.15: the docks get busier, the dead get restless, and the mail goes through.

- HOSTILE UFOs (Scout Saucers, the Abductor, the Overseer) have a 1-in-200 chance to drop a Vorn Skiff part.
- TRADER RATS are bigger (about 1.4x), so it's plain which rats will trade. Existing markets catch up automatically.
- THE BLUE MARLIN (Salty Sal): a sword with a marlin's bill for a blade. Sneak + right-click a wall to MOUNT it there as a
  trophy (it keeps its enchantments); punch the trophy to take it back down.
- STORM BALLS (Salty Sal): throw one and lightning strikes where it lands - clear skies or not.
- WEATHER VIALS now come from Salty Sal (they left Prof. Whiskerton's shelves).
- BLACK MARKET COFFEE (Chef Fromage): every cup stacks Speed and Jump Boost one level higher (up to V) for a minute... and
  the crash that follows stacks just as high: Slowness and Weakness.
- SKIFF PAINT & DECAL KITS (Zorp): six hull colours (Vorn Green, Crimson, Gilded, Midnight, Abyssal, Rose) and four decals
  (Clean, Racing Stripes, Rat Crest, Flames). Use one and your skiff wears it from then on.
- THE RESTLESS DEAD: on a Blood Moon night every graveyard with a living visitor wakes. Restless Spirits rise from the graves
  every few seconds (Ectoplasm), and at midnight THE BANSHEE climbs out once per moon, wailing. Ectoplasm buys Blood Crystals,
  Tokens and the Ghost Veil cosmetic from the Bloodbroker. The dead lie down again at dawn.
- MAILBOXES (Old Barnaby): set one down and you get its numbered KEY. Anyone can post the item in their hand into it
  (right-click); only the key (or its owner) opens it - and nothing falls out if someone breaks things nearby, because a
  mailbox is a ledger, not a chest. Sneak + punch your empty mailbox to pick it up.
  The COURIER WHISTLE (the Fence): hold the item to send in your OFF hand, blow the whistle, type a mailbox number - a
  courier rat delivers it anywhere, loaded or not, for 1 Token."""
import math
from nbt import snbt, B, F, Int, D, Short
from items import item, consumable, attr, ench, T, TOTEM, ITEMS, DYNAMIC, gear, weapon_attrs, hat
from useitem import hold, HOLD
import phase17 as P17

MARLIN, SEA = '#2a6aff', '#3f76e4'
ident = [F(0), F(0), F(0), F(1)]

# ===================================================================== the docks
gear('blue_marlin', 'netherite_sword', 'Blue Marlin', MARLIN,
     ['A marlin\'s bill, honed to a razor.', ('+1 Attack Damage, +0.5 Reach', 'blue'), ('Sneak + right-click a wall: mount it there', 'gray'),
      ('as a trophy. Punch the trophy to take it down.', 'gray')],
     ench(sharpness=6, looting=3, unbreaking=5, mending=1), 2,
     attrs=weapon_attrs('netherite_sword', 1, [attr('entity_interaction_range', 0.5, 'mainhand')]), model='bm:blue_marlin', extra=hold('none'))
HOLD['blue_marlin'] = 'bm:p36/marlin/use'
item('storm_ball', 'minecraft:snowball', 'Storm Ball', '#9ab8ff',
     ['A snowball with a thunderhead inside.', ('Throw it: lightning strikes where it lands,', 'blue'), ('whatever the weather.', 'blue')],
     model='bm:storm_ball', stack=16, cat='builder', glint=True)
item('coffee', TOTEM, 'Black Market Coffee', '#6b4226',
     ['Strong enough to stand a spoon in.', ('Each cup: Speed and Jump Boost one level', 'blue'), ('higher (up to V) for a minute...', 'blue'),
      ('...then a crash just as big: Slowness, Weakness.', 'red')],
     model='bm:coffee', stack=16, cat='food', comps={'minecraft:consumable': consumable(1.2, 'drink', 'minecraft:entity.generic.drink', False)})

# ===================================================================== skiff paint and decal kits
COLOURS = [('green', 'Vorn Green', '#7dff6a'), ('crimson', 'Crimson', '#ff4a4a'), ('gold', 'Gilded', '#ffd23f'), ('midnight', 'Midnight', '#7a5aff'),
           ('ocean', 'Abyssal', '#3ad8d0'), ('rose', 'Rose', '#ff7ac8')]
DECALS = [('none', 'Clean Hull'), ('stripes', 'Racing Stripes'), ('crest', 'Rat Crest'), ('flames', 'Flames')]
for i, (c, nm, col) in enumerate(COLOURS):
    item(f'skiff_paint_{c}', TOTEM, f'Skiff Paint Kit: {nm}', col, ['Right-click: your Vorn Skiff wears this colour', 'from now on (decals stay).'],
         model=f'bm:skiff_paint_{c}', stack=16, cat='alien', comps=hold('none'))
    HOLD[f'skiff_paint_{c}'] = f'bm:p36/skin/paint_{i}'
for i, (d, nm) in enumerate(DECALS):
    item(f'skiff_decal_{d}', TOTEM, f'Skiff Decal Kit: {nm}', '#c8c8e8', ['Right-click: your Vorn Skiff wears this decal', 'from now on (paint stays).'],
         model=f'bm:skiff_decal_{d}', stack=16, cat='alien', comps=hold('none'))
    HOLD[f'skiff_decal_{d}'] = f'bm:p36/skin/decal_{i}'

# ===================================================================== the restless dead
item('ectoplasm', TOTEM, 'Ectoplasm', '#c8fff0', ['Cold, faintly glowing, slightly offended.', ('The Bloodbroker trades for it.', 'gray')],
     model='bm:ectoplasm', stack=64, cat='blood')
hat('ghost_veil', 'Ghost Veil', '#e8fff8', 'bm:ghost_veil', 'minecraft:soul ~ ~1.9 ~ 0.25 0.1 0.25 0.01 1', None,
    ['A banshee\'s burial shroud.', ('Boo.', 'gray')])

# ===================================================================== mailboxes and couriers
item('mailbox', TOTEM, 'Mailbox', '#c0392b',
     ['Right-click the top of a block to set it down.', ('You get its numbered key. Anyone can post', 'blue'), ('the item in their hand into it; only the key', 'blue'),
      ('(or you) opens it. Sneak + punch it (empty)', 'gray'), ('to pick it up again.', 'gray')],
     model='bm:mailbox_icon', stack=16, cat='builder', comps=hold('none'))
HOLD['mailbox'] = 'bm:p36/mail/place'
item('mail_key', TOTEM, 'Mailbox Key', '#e8c870', ['Opens one mailbox. Give a copy of your trust,', 'not a copy of the key - there is only one.'],
     model='bm:mail_key', stack=1, cat='key')
DYNAMIC.add('mail_key')
item('courier_whistle', TOTEM, 'Courier Whistle', '#c8a050',
     ['Two short blasts and a rat comes running.', ('Hold the item to send in your OFF hand,', 'blue'), ('right-click, type a mailbox number.', 'blue'),
      ('Delivered anywhere, for 1 Token.', 'gray')], model='bm:courier_whistle', stack=1, cat='builder', comps=hold('toot_horn'))
HOLD['courier_whistle'] = 'bm:p36/mail/whistle'


def extend_offers(O, offer):
    from phase17 import VIALS
    O['dock'] += [offer(('medallion', 6), ('blue_marlin', 1)), offer(('token', 3), ('storm_ball', 4))]
    O['dock'] += [offer(('token', price), (f'vial_{k}', 1)) for k, (_, _, _, _, price) in VIALS.items()]
    O['chef'].append(offer(('token', 1), ('coffee', 3)))
    O['blood'] += [offer(('ectoplasm', 10), ('blood_crystal', 3)), offer(('ectoplasm', 4), ('token', 1)), offer(('ectoplasm', 24), ('ghost_veil', 1))]
    O['pawn'].append(offer(('token', 4), ('mailbox', 1)))
    O['fence'].append(offer(('token', 6), ('courier_whistle', 1)))


def zorp_offers():
    import phase24 as R24
    k = next(i for i, o in enumerate(R24.OFFERS) if o[2][0] == 'xenite_violet')
    R24.OFFERS[k:k] = [(('xenite_green', 6), ('xenite_violet', 2), (f'skiff_paint_{c}', 1)) for c, _, _ in COLOURS[1:]] + \
                      [(('xenite_cyan', 6), None, (f'skiff_decal_{d}', 1)) for d, _ in DECALS]


zorp_offers()


# ===================================================================== generation
def generate(G):
    import json, mig263
    from nbt import to_json
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    tick, fast, second, load = [], [], [], []
    objs = ['bm.cof dummy', 'bm.coft dummy', 'bm.sid dummy', 'bm.skc dummy', 'bm.skd dummy', 'bm.ght dummy', 'bm.bans dummy', 'bm.bwail dummy',
            'bm.mbid dummy', 'bm.mbo dummy', 'bm.post trigger', 'bm.mail dummy']
    load += [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    holds = '*[minecraft:custom_data~{bm:"%s"}]'

    def add_pools(rel, pools):
        path = G.path('data', *rel.split('/'))
        obj = json.load(open(path))
        obj['pools'] += mig263.convert(rel, to_json(mig263.custom_data_snbt({'type': obj.get('type', 'minecraft:entity'), 'pools': pools})))['pools']
        json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)

    # ------------------------------------------------------------------ hostile UFOs: 1 in 200 for a skiff part
    from phase35 import PARTS
    for t in ('saucer', 'abductor', 'overseer'):
        add_pools(f'bm/loot_table/p32/{t}.json', [{'rolls': 1, 'entries': [G.loot_entry(p) for p, _, _ in PARTS], 'conditions': [G.chance(0.005)]}])

    # ------------------------------------------------------------------ bigger trader rats (markets already in worlds catch up)
    # each sprite is looked at once (reading an entity's data every second is not free)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.rchk] at @s run function bm:p36/ratchk')
    fn('p36/ratchk', ['tag @s add bm.rchk', 'execute if data entity @s {transformation:{scale:[0.855f,0.855f,0.855f]}} run function bm:p36/ratbig'])
    fn('p36/ratbig', ['tag @s add bm.rbig', 'data merge entity @s {transformation:{scale:[1.197f,1.197f,1.197f],translation:[0f,0.5985f,0f]}}',
                      'scoreboard players set @s bm.rs 1197',          # the breathing animation's remembered size
                      'execute as @e[type=minecraft:villager,distance=..0.7] run function bm:p36/ratbig_v',
                      'execute as @e[type=minecraft:text_display,tag=bm.e18,distance=..1.2] run data merge entity @s {transformation:{translation:[0f,1.45f,0f]}}',
                      'execute as @e[type=minecraft:interaction,tag=bm.ledger,distance=..0.7] run data modify entity @s height set value 1.4f',
                      'execute as @e[type=minecraft:interaction,tag=bm.ledger,distance=..0.7] run data modify entity @s width set value 0.9f'])
    fn('p36/ratbig_v', ['execute store result score #s bm.rng run attribute @s minecraft:scale base get 100',
                        'execute if score #s bm.rng matches ..55 run attribute @s minecraft:scale base set 0.7'])

    # ------------------------------------------------------------------ the Blue Marlin: mount it on a wall, punch it down
    fn('p36/marlin/use', ['execute unless predicate bm:p20/sneaking run return 0',
                          'execute unless items entity @s weapon.mainhand ' + holds % 'blue_marlin' + ' run return 0',
                          'scoreboard players set #ray bm.rng 25', 'tag @s add bm.mounter', 'execute anchored eyes positioned ^ ^ ^ run function bm:p36/marlin/ray',
                          'tag @s remove bm.mounter'])
    fn('p36/marlin/ray', ['execute unless block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^-0.35 align xyz positioned ~0.5 ~0.5 ~0.5 run return run function bm:p36/marlin/hit',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p36/marlin/ray'])
    snap = [('-45..45', 0), ('45..135', 90), ('135..180', 180), ('-180..-135', 180), ('-135..-45', -90)]
    disp = {'Tags': ['bm.mdisp', 'bm.mnew'], 'item_display': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(12)},
            'transformation': {'left_rotation': [F(0), F(0), F(-0.3827), F(0.9239)], 'right_rotation': ident, 'translation': [F(0), F(0), F(0)], 'scale': [F(1.6)] * 3}}
    box = {'Tags': ['bm.mmount', 'bm.mnew'], 'width': F(1.0), 'height': F(1.0), 'response': B(1)}
    fn('p36/marlin/hit', ['execute unless block ~ ~ ~ #bm:grap_pass run return run ' + title('@a[tag=bm.mounter]', 'actionbar', T('No room to mount it there.', 'gray')),
                          'execute if entity @e[type=minecraft:interaction,tag=bm.mmount,distance=..0.6] run return 0'] +
       [f'execute as @a[tag=bm.mounter] if entity @s[y_rotation={r}] positioned ~ ~ ~ rotated {y} 0 positioned ^ ^ ^0.44 run summon minecraft:item_display ~ ~ ~ {snbt(dict(disp, Rotation=[F(y), F(0)]))}'
        for r, y in snap] +
       [f'summon minecraft:interaction ~ ~-0.5 ~ {snbt(box)}',
        'execute as @e[type=minecraft:item_display,tag=bm.mnew,distance=..1,limit=1] run data modify entity @s item set from entity @a[tag=bm.mounter,limit=1] SelectedItem',
        'item replace entity @a[tag=bm.mounter,limit=1] weapon.mainhand with minecraft:air', 'tag @e[tag=bm.mnew,distance=..1.5] remove bm.mnew',
        'playsound minecraft:entity.item_frame.add_item block @a[distance=..16] ~ ~ ~ 1 0.8',
        title('@a[tag=bm.mounter]', 'actionbar', T('A fine catch, mounted. (Punch it to take it down.)', MARLIN))])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.mmount] if data entity @s attack at @s run function bm:p36/marlin/take')
    fn('p36/marlin/take', ['data modify storage bm:tmp give set from entity @e[type=minecraft:item_display,tag=bm.mdisp,distance=..0.8,limit=1,sort=nearest] item',
                           'execute on attacker at @s run function bm:p33/give_back', 'data remove entity @s attack',
                           'kill @e[type=minecraft:item_display,tag=bm.mdisp,distance=..0.8,limit=1,sort=nearest]',
                           'playsound minecraft:entity.item_frame.remove_item block @a[distance=..16] ~ ~ ~ 1 0.8', 'kill @s'])

    # ------------------------------------------------------------------ storm balls: lightning where they land
    tick += ['execute as @e[type=minecraft:snowball,tag=!bm.sbck] at @s run function bm:p36/storm/check',
             'execute if score #storms bm.rng matches 1.. as @e[type=minecraft:marker,tag=bm.stormm] at @s run function bm:p36/storm/follow']
    fn('p36/storm/check', ['tag @s add bm.sbck', 'execute unless entity @s[nbt={Item:{components:{"minecraft:custom_data":{bm:"storm_ball"}}}}] run return 0',
                           'tag @s add bm.storm', 'scoreboard players add #sid bm.rng 1', 'scoreboard players operation @s bm.sid = #sid bm.rng',
                           'execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["bm.stormm","bm.snew"]}',
                           'execute at @s run scoreboard players operation @e[type=minecraft:marker,tag=bm.snew,distance=..1,limit=1] bm.sid = #sid bm.rng',
                           'execute at @s run tag @e[type=minecraft:marker,tag=bm.snew,distance=..1] remove bm.snew', 'scoreboard players add #storms bm.rng 1'])
    fn('p36/storm/follow', ['scoreboard players operation #s bm.sid = @s bm.sid',
                            'execute as @e[type=minecraft:snowball,tag=bm.storm] if score @s bm.sid = #s bm.sid run tag @s add bm.sbme',
                            'execute unless entity @e[type=minecraft:snowball,tag=bm.sbme] run return run function bm:p36/storm/strike',
                            'tp @s @e[type=minecraft:snowball,tag=bm.sbme,limit=1]', 'particle minecraft:electric_spark ~ ~ ~ 0.1 0.1 0.1 0.05 2',
                            'tag @e[type=minecraft:snowball,tag=bm.sbme] remove bm.sbme'])
    fn('p36/storm/strike', ['summon minecraft:lightning_bolt ~ ~ ~', 'scoreboard players remove #storms bm.rng 1', 'kill @s'])

    # ------------------------------------------------------------------ coffee: stacking buzz, stacking crash
    G.consume_adv('coffee', 'bm:p36/coffee')
    fn('p36/coffee', ['advancement revoke @s only bm:consume/coffee', 'scoreboard players add @s bm.cof 1',
                      'execute if score @s bm.cof matches 6.. run scoreboard players set @s bm.cof 5', 'scoreboard players set @s bm.coft 60'] +
       [f'execute if score @s bm.cof matches {n} run function bm:p36/coffee_{n}' for n in range(1, 6)])
    for n in range(1, 6):
        fn(f'p36/coffee_{n}', [f'effect give @s minecraft:speed 61 {n - 1}', f'effect give @s minecraft:jump_boost 61 {n - 1}',
                               'playsound minecraft:entity.generic.drink player @s ~ ~ ~ 1 1.4',
                               title('@s', 'actionbar', T(f'Buzzing: Speed & Jump Boost {"I II III IV V".split()[n - 1]}' + ('  (that\'s the limit!)' if n == 5 else ''), '#c08a5a'))])
        fn(f'p36/crash_{n}', [f'effect give @s minecraft:slowness {20 + 8 * n} {n - 1}', f'effect give @s minecraft:weakness {20 + 8 * n} {n - 1}',
                              'playsound minecraft:entity.player.burp player @s ~ ~ ~ 1 0.6',
                              title('@s', 'actionbar', T(f'Caffeine crash! Slowness & Weakness {"I II III IV V".split()[n - 1]}', 'red'))])
    second += ['scoreboard players remove @a[scores={bm.coft=1..}] bm.coft 1', 'execute as @a[scores={bm.coft=0,bm.cof=1..}] at @s run function bm:p36/coffee_crash']
    fn('p36/coffee_crash', [f'execute if score @s bm.cof matches {n} run function bm:p36/crash_{n}' for n in range(1, 6)] + ['scoreboard players set @s bm.cof 0'])

    # ------------------------------------------------------------------ skiff paint and decal kits
    for i, (c, nm, col) in enumerate(COLOURS):
        fn(f'p36/skin/paint_{i}', [f'scoreboard players set @s bm.skc {i}', f'clear @s {holds % f"skiff_paint_{c}"} 1', 'function bm:p36/skin/apply',
                                   'playsound minecraft:block.copper.place player @s ~ ~ ~ 1 1.2', title('@s', 'actionbar', T(f'Your skiff is now {nm}.', col))])
    for i, (d, nm) in enumerate(DECALS):
        fn(f'p36/skin/decal_{i}', [f'scoreboard players set @s bm.skd {i}', f'clear @s {holds % f"skiff_decal_{d}"} 1', 'function bm:p36/skin/apply',
                                   'playsound minecraft:item.dye.use player @s ~ ~ ~ 1 1', title('@s', 'actionbar', T(f'Decal applied: {nm}.', '#c8c8e8'))])
    pick = ['execute unless score @s bm.skc matches 0.. run scoreboard players set @s bm.skc 0', 'execute unless score @s bm.skd matches 0.. run scoreboard players set @s bm.skd 0']
    pick += [f'execute if score @s bm.skc matches {i} if score @s bm.skd matches {j} run data modify storage bm:tmp skin set value "bm:skiff_{c}_{d}"'
             for i, (c, _, _) in enumerate(COLOURS) for j, (d, _) in enumerate(DECALS)]
    fn('p36/skin/apply', pick + ['execute unless score @s bm.pid matches 1.. run return 0', 'scoreboard players operation #kp bm.pid = @s bm.pid',
                                 'execute as @e[type=minecraft:item_display,tag=bm.skdisp] if score @s bm.pid = #kp bm.pid run data modify entity @s item.components."minecraft:item_model" set from storage bm:tmp skin'])
    use = G.FUNCS['p35/skiff/use']
    k = next(i for i, l in enumerate(use) if l.startswith('tag @e[tag=bm.sknew'))
    use.insert(k + 1, 'function bm:p36/skin/apply')

    # ------------------------------------------------------------------ the restless dead (Blood Moon graveyards)
    GRAVES = [(4, 10), (7, 22), (23, 16), (26, 34), (4, 40), (26, 10), (7, 46), (23, 28)]       # grave spots (template x, z); the crypt controller is at (15.5, 2, 49.5)
    ghost_disp = {'id': 'minecraft:item_display', 'Tags': ['bm.ghostdisp'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:ghost3d'}},
                  'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'teleport_duration': Int(2),
                  'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.1), F(0)], 'scale': [F(1.1)] * 3}}
    invis = {'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}
    ghost = {'Tags': ['bm.ghost', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Restless Spirit', '#c8fff0'), 'Health': F(14),
             'attributes': [{'id': 'minecraft:max_health', 'base': D(14)}, {'id': 'minecraft:attack_damage', 'base': D(4)}],
             'active_effects': [invis], 'DeathLootTable': 'bm:p36/ghost', 'Passengers': [ghost_disp]}
    banshee = {'Tags': ['bm.ghost', 'bm.banshee', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('The Banshee', '#e8fff8', bold=True), 'Health': F(150),
               'attributes': [{'id': 'minecraft:max_health', 'base': D(150)}, {'id': 'minecraft:attack_damage', 'base': D(9)}, {'id': 'minecraft:scale', 'base': D(2.4)},
                              {'id': 'minecraft:armor', 'base': D(6)}],
               'active_effects': [invis], 'DeathLootTable': 'bm:p36/banshee',
               'Passengers': [dict(ghost_disp, item={'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:banshee3d'}},
                                   transformation={'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.3), F(0)], 'scale': [F(2.6)] * 3})]}
    second += ['execute if score #active bm.bm matches 1 as @e[type=minecraft:marker,tag=bm.crypt_ctrl] at @s rotated as @s positioned ^ ^16 ^-22 if entity @a[distance=..44,gamemode=!spectator] positioned ^ ^-16 ^22 run function bm:p36/ghost/yard',
               'execute as @e[type=minecraft:vex,tag=bm.ghost] at @s unless entity @a[distance=..96] run function bm:p36/ghost/fade',
               'execute as @e[type=minecraft:vex,tag=bm.banshee] at @s run function bm:p36/ghost/banshee']
    fn('p36/ghost/yard', ['scoreboard players add @s bm.ght 1',
                          'execute if score @s bm.ght matches 12.. run function bm:p36/ghost/wave',
                          'execute if score #tod bm.bm matches 17600..18600 unless score @s bm.bans = #bmn bm.bm run function bm:p36/ghost/banshee_rise',
                          'execute positioned ^ ^16 ^-22 run particle minecraft:soul ~ ~0.5 ~ 12 0.3 22 0.01 6',
                          'execute store result score #r bm.rng run random value 1..6',
                          'execute if score #r bm.rng matches 1 positioned ^ ^16 ^-22 run playsound minecraft:ambient.soul_sand_valley.mood ambient @a[distance=..40] ~ ~ ~ 0.8 0.7'])
    fn('p36/ghost/wave', ['scoreboard players set @s bm.ght 0',
                          'execute store result score #g bm.rng positioned ^ ^16 ^-22 if entity @e[type=minecraft:vex,tag=bm.ghost,distance=..50]',
                          'execute if score #g bm.rng matches 6.. run return 0',
                          'execute store result score #r bm.rng run random value 1..8',
                          'function bm:p36/ghost/rise', 'execute store result score #r bm.rng run random value 1..8', 'function bm:p36/ghost/rise'])
    fn('p36/ghost/rise', [f'execute if score #r bm.rng matches {i} positioned ^{x + 0.5 - 15.5} ^16 ^{z + 1.5 - 49.5} run function bm:p36/ghost/one' for i, (x, z) in enumerate(GRAVES, 1)])
    fn('p36/ghost/one', ['particle minecraft:sculk_soul ~ ~0.5 ~ 0.3 0.4 0.3 0.02 20', 'particle minecraft:block{block_state:"minecraft:podzol"} ~ ~0.1 ~ 0.4 0.1 0.4 0.1 20',
                         'playsound minecraft:particle.soul_escape hostile @a[distance=..24] ~ ~ ~ 1 0.6', f'summon minecraft:vex ~ ~1 ~ {snbt(ghost)}'])
    fn('p36/ghost/banshee_rise', ['scoreboard players operation @s bm.bans = #bmn bm.bm',
                                  f'execute positioned ^ ^17 ^-22 run summon minecraft:vex ~ ~ ~ {snbt(banshee)}',
                                  'execute positioned ^ ^16 ^-22 run particle minecraft:sculk_soul ~ ~1 ~ 3 1 3 0.05 120',
                                  'execute positioned ^ ^16 ^-22 run playsound minecraft:entity.warden.emerge hostile @a[distance=..64] ~ ~ ~ 2 0.6',
                                  'title @a[distance=..64] times 10 60 20', title('@a[distance=..64]', 'subtitle', T('Something tears free of the oldest grave...', 'gray', italic=True)),
                                  title('@a[distance=..64]', 'title', T('THE BANSHEE', '#e8fff8', bold=True))])
    fn('p36/ghost/banshee', ['scoreboard players add @s bm.bwail 1', 'execute unless score @s bm.bwail matches 6.. run return 0', 'scoreboard players set @s bm.bwail 0',
                             'playsound minecraft:entity.ghast.scream hostile @a[distance=..40] ~ ~ ~ 2 0.4', 'particle minecraft:sonic_boom ~ ~2 ~ 0 0 0 0 1',
                             'execute as @a[distance=..10,gamemode=!spectator,gamemode=!creative] run function bm:p36/ghost/wailed'])
    fn('p36/ghost/wailed', ['effect give @s minecraft:darkness 4 0', 'effect give @s minecraft:slowness 3 1', 'damage @s 3 minecraft:magic',
                            title('@s', 'actionbar', T('The Banshee\'s wail chills your blood!', '#c8fff0'))])
    fn('p36/ghost/fade', ['particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.02 15', 'execute on passengers run kill @s', 'tp @s ~ -400 ~'])
    G.FUNCS['bloodmoon/end'].append('execute as @e[type=minecraft:vex,tag=bm.ghost] at @s run function bm:p36/ghost/fade')
    second.append('execute as @e[type=minecraft:item_display,tag=bm.ghostdisp] unless function bm:p20/frog/has_vehicle run kill @s')
    pool = lambda e, p=None: dict({'rolls': 1, 'entries': e}, **({'conditions': [G.chance(p)]} if p else {}))
    wjson('bm/loot_table/p36/ghost.json', {'type': 'minecraft:entity', 'pools': [pool([G.loot_entry('ectoplasm', G.uni(1, 2))]), pool([G.loot_entry('blood_crystal')], 0.1)]})
    wjson('bm/loot_table/p36/banshee.json', {'type': 'minecraft:entity', 'pools': [pool([G.loot_entry('ectoplasm', G.uni(8, 12))]), pool([G.loot_entry('blood_crystal', G.uni(3, 5))]),
                                                                                  pool([G.loot_entry('ghost_veil')], 0.35), pool([G.loot_entry('medallion')]),
                                                                                  pool([G.loot_entry('specter_sheet', G.uni(1, 3))], 0.005)]})   # 2.16 (phase37)

    # ------------------------------------------------------------------ mailboxes and couriers
    mdisp = {'Tags': ['bm.mbdisp', 'bm.mbnew'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:mailbox3d'}},
             'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)},
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1.0)] * 3}}
    mbox = {'Tags': ['bm.mbox', 'bm.mbnew'], 'width': F(0.7), 'height': F(1.3), 'response': B(1)}
    key_arg = G.item_arg('mail_key')
    assert 'bm:"mail_key"' in key_arg
    key_arg = key_arg.replace('bm:"mail_key"', 'bm:"mail_key",bm_mail:$(n)', 1).replace(
        "minecraft:lore=[", "minecraft:lore=[{text:'Mailbox No. $(n)',color:'gold',italic:false},", 1) if "minecraft:lore=[" in key_arg else key_arg
    fn('p36/mail/place', ['scoreboard players set #ray bm.rng 25', 'tag @s add bm.poster', 'execute anchored eyes positioned ^ ^ ^ run function bm:p36/mail/ray', 'tag @s remove bm.poster'])
    fn('p36/mail/ray', ['execute unless block ~ ~ ~ #bm:grap_pass align xyz positioned ~0.5 ~1 ~0.5 run return run function bm:p36/mail/hit',
                        'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p36/mail/ray'])
    fn('p36/mail/hit', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run ' + title('@a[tag=bm.poster]', 'actionbar', T('Set it on top of a block, in the open.', 'gray')),
                        'execute unless block ~ ~1 ~ #minecraft:replaceable run return run ' + title('@a[tag=bm.poster]', 'actionbar', T('Set it on top of a block, in the open.', 'gray')),
                        'execute if entity @e[type=minecraft:interaction,tag=bm.mbox,distance=..0.8] run return 0',
                        'execute as @a[tag=bm.poster] unless score @s bm.pid matches 1.. run function bm:p21/pid',
                        'scoreboard players add #mbn bm.mail 1', f'summon minecraft:item_display ~ ~ ~ {snbt(mdisp)}', f'summon minecraft:interaction ~ ~ ~ {snbt(mbox)}',
                        'execute as @a[tag=bm.poster,limit=1] at @s rotated ~ 0 run tp @e[type=minecraft:item_display,tag=bm.mbnew,distance=..6] ~ ~ ~ ~180 0',
                        'execute as @e[tag=bm.mbnew,distance=..6] at @s run tp @s ~ ~ ~',
                        'scoreboard players operation @e[tag=bm.mbnew,distance=..1.5] bm.mbid = #mbn bm.mail',
                        'scoreboard players operation @e[tag=bm.mbnew,distance=..1.5] bm.mbo = @a[tag=bm.poster,limit=1] bm.pid',
                        'tag @e[tag=bm.mbnew,distance=..1.5] remove bm.mbnew',
                        'execute store result storage bm:tmp mb.n int 1 run scoreboard players get #mbn bm.mail',
                        'execute store result storage bm:tmp mb.pid int 1 run scoreboard players get @a[tag=bm.poster,limit=1] bm.pid',
                        'function bm:p36/mail/new with storage bm:tmp mb',
                        'clear @a[tag=bm.poster,limit=1] ' + holds % 'mailbox' + ' 1', 'playsound minecraft:block.chain.place block @a[distance=..16] ~ ~ ~ 1 1',
                        tellraw('@a[tag=bm.poster]', PREFIX + [T('Mailbox ', 'gray'), T('No. ', 'gold'), {'score': {'name': '#mbn', 'objective': 'bm.mail'}, 'color': 'gold', 'bold': True},
                                                               T(' is open for post. Here\'s its key - tell your friends the number.', 'gray')])])
    fn('p36/mail/new', ['$data modify storage bm:mail m$(n) set value {owner:$(pid),items:[]}', f'$give @a[tag=bm.poster,limit=1] {key_arg}'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.mbox] if data entity @s interaction at @s run function bm:p36/mail/click',
             'execute as @e[type=minecraft:interaction,tag=bm.mbox] if data entity @s attack at @s run function bm:p36/mail/punch']
    fn('p36/mail/click', ['scoreboard players operation #n bm.mail = @s bm.mbid', 'scoreboard players operation #o bm.mail = @s bm.mbo',
                          'execute on target at @s run function bm:p36/mail/who', 'data remove entity @s interaction'])
    fn('p36/mail/who', ['execute store result score #k bm.mail run data get entity @s SelectedItem.components."minecraft:custom_data".bm_mail',
                        'execute if score #k bm.mail = #n bm.mail run return run function bm:p36/mail/open',
                        'execute store result score #k bm.mail run data get entity @s equipment.offhand.components."minecraft:custom_data".bm_mail',
                        'execute if score #k bm.mail = #n bm.mail run return run function bm:p36/mail/open',
                        'execute if score @s bm.pid = #o bm.mail unless items entity @s weapon.mainhand * run return run function bm:p36/mail/open',
                        'execute if items entity @s weapon.mainhand * run return run function bm:p36/mail/post',
                        title('@s', 'actionbar', T('Locked. Hold an item and right-click to post it in.', 'gray'))])
    fn('p36/mail/post', ['execute store result storage bm:tmp mb.n int 1 run scoreboard players get #n bm.mail', 'function bm:p36/mail/post_m with storage bm:tmp mb'])
    fn('p36/mail/post_m', ['$execute unless data storage bm:mail m$(n) run return run ' + title('@s', 'actionbar', T('This mailbox is out of service.', 'gray')),
                           '$execute store result score #c bm.mail run data get storage bm:mail m$(n).items',
                           'execute if score #c bm.mail matches 27.. run return run ' + title('@s', 'actionbar', T('That mailbox is stuffed full.', 'red')),
                           '$data modify storage bm:mail m$(n).items append from entity @s SelectedItem',
                           'item replace entity @s weapon.mainhand with minecraft:air', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 1.2',
                           title('@s', 'actionbar', T('Posted!', '#e8c870')), 'function bm:p36/mail/notify'])
    fn('p36/mail/notify', ['execute as @a if score @s bm.pid = #o bm.mail run tellraw @s ' + snbt(PREFIX + [T('You\'ve got mail! ', '#e8c870', bold=True), T('(Mailbox No. ', 'gray'),
                                                                                                      {'score': {'name': '#n', 'objective': 'bm.mail'}, 'color': 'gold'}, T(')', 'gray')]),
                           'execute as @a if score @s bm.pid = #o bm.mail at @s run playsound minecraft:block.note_block.bell player @s ~ ~ ~ 0.7 1.6'])
    # opening: the mailbox's contents move into a crate you sit in (the satchel's trick - nothing is copied); closing moves them back
    crate = {'Tags': ['bm.crate', 'bm.cnew', 'bm.c_mail'], 'Invulnerable': B(1), 'Silent': B(1), 'CustomName': T('Mailbox', '#e8c870')}
    fn('p36/mail/open', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                         'execute store result storage bm:tmp mb.n int 1 run scoreboard players get #n bm.mail',
                         f'summon minecraft:dark_oak_chest_boat ~ ~ ~ {snbt(crate)}',
                         'scoreboard players operation @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] bm.pid = @s bm.pid',
                         'scoreboard players operation @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] bm.mbid = #n bm.mail',
                         'function bm:p36/mail/load with storage bm:tmp mb', 'scoreboard players set #k bm.mail 0', 'function bm:p36/mail/fill',
                         'ride @s mount @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1]',
                         'tag @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew] remove bm.cnew', 'playsound minecraft:block.iron_trapdoor.open player @s ~ ~ ~ 1 1.2',
                         title('@s', 'actionbar', T('Press your inventory key to read your mail. Sneak to close.', '#e8c870'))])
    fn('p36/mail/load', ['$data modify storage bm:tmp mb.src set from storage bm:mail m$(n).items', '$data modify storage bm:mail m$(n).items set value []'])
    fn('p36/mail/fill', ['execute unless data storage bm:tmp mb.src[0] run return 0',
                         # build the whole entry (with its Slot) first - an entry appended without a Slot is thrown away at once
                         'data modify storage bm:tmp mb.e set from storage bm:tmp mb.src[0]',
                         'execute store result storage bm:tmp mb.e.Slot byte 1 run scoreboard players get #k bm.mail',
                         'data modify entity @e[type=minecraft:dark_oak_chest_boat,tag=bm.cnew,distance=..1,limit=1] Items append from storage bm:tmp mb.e',
                         'scoreboard players add #k bm.mail 1', 'data remove storage bm:tmp mb.src[0]', 'function bm:p36/mail/fill'])
    fn('p36/mail/close', ['execute store result storage bm:tmp mb.n int 1 run scoreboard players get @s bm.mbid', 'data modify storage bm:tmp mb.out set value []',
                          'data modify storage bm:tmp mb.src set from entity @s Items', 'function bm:p36/mail/drain', 'function bm:p36/mail/store with storage bm:tmp mb',
                          'execute as @a[tag=bm.cown,limit=1] at @s run playsound minecraft:block.iron_trapdoor.close player @s ~ ~ ~ 1 1.2'])
    fn('p36/mail/drain', ['execute unless data storage bm:tmp mb.src[0] run return 0', 'data modify storage bm:tmp mb.out append from storage bm:tmp mb.src[0]',
                          'data remove storage bm:tmp mb.out[-1].Slot', 'data remove storage bm:tmp mb.src[0]', 'function bm:p36/mail/drain'])
    fn('p36/mail/store', ['$execute unless data storage bm:mail m$(n) run data modify storage bm:mail m$(n) set value {owner:0,items:[]}',
                          '$data modify storage bm:mail m$(n).items append from storage bm:tmp mb.out[]'])
    cc = G.FUNCS['p33/crate/close']
    k = next(i for i, l in enumerate(cc) if 'bm.c_box' in l)
    cc.insert(k + 1, 'execute if entity @s[tag=bm.c_mail] run function bm:p36/mail/close')
    # picking it up: its owner, sneaking, and only when it's empty
    fn('p36/mail/punch', ['scoreboard players operation #n bm.mail = @s bm.mbid', 'scoreboard players operation #o bm.mail = @s bm.mbo',
                          'tag @s add bm.mbme', 'execute on attacker at @s run function bm:p36/mail/punched', 'tag @s remove bm.mbme', 'data remove entity @s attack'])
    fn('p36/mail/punched', ['execute unless score @s bm.pid = #o bm.mail run return 0', 'execute unless predicate bm:p20/sneaking run return 0',
                            'execute store result storage bm:tmp mb.n int 1 run scoreboard players get #n bm.mail', 'function bm:p36/mail/pickup with storage bm:tmp mb'])
    fn('p36/mail/pickup', ['$execute if data storage bm:mail m$(n).items[0] run return run ' + title('@s', 'actionbar', T('Empty your mailbox first.', 'gray')),
                           '$data remove storage bm:mail m$(n)', give('mailbox'),
                           'execute as @e[type=minecraft:interaction,tag=bm.mbme] at @s run kill @e[type=minecraft:item_display,tag=bm.mbdisp,distance=..0.8]',
                           'kill @e[type=minecraft:interaction,tag=bm.mbme]', 'playsound minecraft:block.chain.break block @a[distance=..16] ~ ~ ~ 1 1',
                           title('@s', 'actionbar', T('Mailbox packed up. (Its old key no longer opens anything.)', 'gray'))])
    # the courier whistle: a dialog asks for the number; /trigger bm.post carries it back
    import phase28 as P28
    dlg = {'type': 'minecraft:multi_action', 'title': T('Courier Whistle', '#c8a050', bold=True),
           'body': [P28.body([T('Your courier rat will carry the item in your ', 'gray'), T('off hand', 'white'), T(' to any mailbox, for 1 Token.', 'gray')])],
           'inputs': [{'type': 'minecraft:text', 'key': 'box', 'label': T('Mailbox number', 'gold'), 'width': Int(200), 'max_length': Int(6)}],
           'actions': [{'label': T('Send it!', 'gold'), 'width': Int(200), 'action': {'type': 'minecraft:dynamic/run_command', 'template': 'trigger bm.post set $(box)'}}],
           'columns': Int(1), 'exit_action': {'label': T('Never mind')}, 'pause': False, 'after_action': 'close'}
    fn('p36/mail/whistle', ['execute unless items entity @s weapon.offhand * run return run ' + title('@s', 'actionbar', T('Hold the item to send in your OFF hand.', 'gray')),
                            'scoreboard players set @s bm.post 0', 'scoreboard players enable @s bm.post', f'dialog show @s {snbt(dlg)}'])
    tick.append('execute as @a[scores={bm.post=1..}] at @s run function bm:p36/mail/send')
    tok = holds % 'token'
    fn('p36/mail/send', ['scoreboard players operation #n bm.mail = @s bm.post', 'scoreboard players set @s bm.post 0',
                         'execute unless items entity @s container.* ' + holds % 'courier_whistle' + ' unless items entity @s weapon.offhand ' + holds % 'courier_whistle' + ' run return 0',
                         'execute unless items entity @s weapon.offhand * run return run ' + title('@s', 'actionbar', T('Your off hand is empty - nothing to send.', 'gray')),
                         'execute store result score #t bm.rng run clear @s ' + tok + ' 0',
                         'execute if score #t bm.rng matches 0 run return run ' + title('@s', 'actionbar', T('The courier wants 1 Token for the trip.', 'red')),
                         'execute store result storage bm:tmp mb.n int 1 run scoreboard players get #n bm.mail', 'function bm:p36/mail/send_m with storage bm:tmp mb'])
    fn('p36/mail/send_m', ['$execute unless data storage bm:mail m$(n) run return run ' + title('@s', 'actionbar', T('No mailbox by that number.', 'red')),
                           '$execute store result score #c bm.mail run data get storage bm:mail m$(n).items',
                           'execute if score #c bm.mail matches 27.. run return run ' + title('@s', 'actionbar', T('That mailbox is stuffed full.', 'red')),
                           '$execute store result score #o bm.mail run data get storage bm:mail m$(n).owner',
                           '$data modify storage bm:mail m$(n).items append from entity @s equipment.offhand',
                           'execute store result score #t bm.rng run clear @s ' + tok + ' 0', 'execute if score #t bm.rng matches 0 run return 0',
                           'item replace entity @s weapon.offhand with minecraft:air', 'clear @s ' + tok + ' 1',
                           'particle minecraft:poof ~ ~0.3 ~ 0.3 0.1 0.3 0.05 10', 'playsound minecraft:entity.silverfish.ambient player @a[distance=..16] ~ ~ ~ 1 1.4',
                           title('@s', 'actionbar', [T('Your courier rat scurries off to mailbox No. ', '#c8a050'), {'score': {'name': '#n', 'objective': 'bm.mail'}, 'color': 'gold'}]),
                           'function bm:p36/mail/notify'])

    G.FUNCS['load'][-1:-1] = load
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack
def rp(R):
    grid = R.grid
    I = {}
    I['blue_marlin'] = grid(['................', '..............WW', '.............WB.', '............WB..', '...........WB...', '..........BB....', '.....LLLLBBB....',
                              '....LBBBBBBL....', '...LBBDBBBBL....', '..LBBBBBBBL.....', '..LBBBBBL.......', '.LTLLLLL........', 'TT..L...........', 'T...............',
                              '................', '................'], dict(W='#e8f0ff', B='#2a6aff', D='#0a1a3a', L='#1a3a8a', T='#5a8aff'))
    I['storm_ball'] = grid(['................', '................', '.....WWWWWW.....', '....WGGGGGGW....', '...WGGWGGGGGW...', '...WGGGGYGGGW...', '...WGGGYYGGGW...',
                             '...WGGYYGGGGW...', '...WGGGGYGGGW...', '...WGGGYGGGGW...', '....WGGGGGGW....', '.....WWWWWW.....', '................', '................',
                             '................', '................'], dict(W='#dfe9f2', G='#6a7a9a', Y='#ffe85a'))
    I['coffee'] = grid(['................', '......s..s......', '.......s..s.....', '......s..s......', '....WWWWWWWW....', '....WCCCCCCWWW..', '....WCCCCCCW.W..',
                         '....WCCCCCCW.W..', '....WCCCCCCWWW..', '....WWWWWWWW....', '.....WWWWWW.....', '...PPPPPPPPPP...', '................', '................',
                         '................', '................'], dict(W='#f4f0e8', C='#4a2a14', s='#d8d8d8', P='#c8b08a'))
    I['ectoplasm'] = grid(['................', '................', '......GGGG......', '.....GgggggG....', '....GgWWgggG....', '....GgWggggG....', '....GgggggggG...',
                            '...GggggggggG...', '...GgggggggG....', '....GGgggGG.....', '......GGG.......', '................', '................', '................',
                            '................', '................'], dict(G='#7ad8b8', g='#c8fff0', W='#ffffff'))
    I['mailbox_icon'] = grid(['................', '.....RRRRRR.F...', '....RRRRRRRRF...', '....RKKKKKKRF...', '....RRRRRRRRF...', '....RRRRRRRR....', '.......WW.......',
                               '.......WW.......', '.......WW.......', '.......WW.......', '.......WW.......', '......WWWW......', '................', '................',
                               '................', '................'], dict(R='#c0392b', K='#3a1a12', F='#ffd23f', W='#6a4a2a'))
    I['mail_key'] = grid(['................', '....GGG.........', '...G...G........', '...G.R.G........', '...G...G........', '....GGGSSSSSSS..', '...........S.S..',
                           '...........S.SS.', '................', '................', '................', '................', '................', '................',
                           '................', '................'], dict(G='#e8c870', R='#c0392b', S='#c8a050'))
    I['courier_whistle'] = grid(['................', '................', '................', '.........BBBB...', '......BBBBBBBBK.', '....BBBBBBBBBBK.', '...BBBBBBBBBBBK.',
                                  '...BB......BBK..', '...B.........K..', '................', '................', '................', '................', '................',
                                  '................', '................'], dict(B='#c8a050', K='#6a4a2a'))
    for i, (c, nm, col) in enumerate(COLOURS):
        I[f'skiff_paint_{c}'] = grid(['................', '......KKKK......', '.....KCCCCK.....', '....KCCWCCCK....', '....KCCCCCCK....', '....KCCCCCCK....', '....KKKKKKKK....',
                                       '....KCCCCCCK....', '....KKKKKKKK....', '......K..K......', '................', '................', '................', '................',
                                       '................', '................'], dict(K='#3a3a48', C=col, W='#ffffff'))
    deco = {'none': '#d8d8e8', 'stripes': '#ffffff', 'crest': '#ffd23f', 'flames': '#ff7a1a'}
    for d, nm in DECALS:
        I[f'skiff_decal_{d}'] = grid(['................', '................', '...PPPPPPPPPP...', '...PDDDDDDDDP...', '...PDXDDDDXDP...', '...PDDXXXXDDP...', '...PDDXXXXDDP...',
                                       '...PDXDDDDXDP...', '...PDDDDDDDDP...', '...PPPPPPPPPP...', '................', '................', '................', '................',
                                       '................', '................'], dict(P='#a8a8b8', D='#e8e8f0', X=deco[d]))
    for k, v in I.items(): R.ICONS[k] = v
    R.HANDHELD_EXTRA.add('blue_marlin')
    cube = R.cube
    def c(fr, to, t, rot=None):
        e = cube(fr, to, t)
        if rot: e['rotation'] = rot
        return e
    # skiffs: the saucer in six paints, each with four decals
    paints = {'green': ('minecraft:block/iron_block', 'minecraft:block/light_gray_concrete', 'minecraft:block/light_blue_stained_glass', 'minecraft:block/verdant_froglight_side'),
              'crimson': ('minecraft:block/red_concrete', 'minecraft:block/red_nether_bricks', 'minecraft:block/red_stained_glass', 'minecraft:block/shroomlight'),
              'gold': ('minecraft:block/gold_block', 'minecraft:block/raw_gold_block', 'minecraft:block/yellow_stained_glass', 'minecraft:block/glowstone'),
              'midnight': ('minecraft:block/black_concrete', 'minecraft:block/purple_concrete', 'minecraft:block/purple_stained_glass', 'minecraft:block/amethyst_block'),
              'ocean': ('minecraft:block/prismarine_bricks', 'minecraft:block/dark_prismarine', 'minecraft:block/cyan_stained_glass', 'minecraft:block/sea_lantern'),
              'rose': ('minecraft:block/pink_concrete', 'minecraft:block/white_concrete', 'minecraft:block/magenta_stained_glass', 'minecraft:block/pearlescent_froglight_side')}
    for col, (h, p, g, l) in paints.items():
        tex = {'h': h, 'p': p, 'g': g, 'l': l, 'd': 'minecraft:block/gray_concrete', 'w': 'minecraft:block/white_concrete',
               'y': 'minecraft:block/gold_block', 'o': 'minecraft:block/orange_concrete', 'r': 'minecraft:block/red_concrete'}
        base = [c((3, 4, 3), (13, 6, 13), 'd'), c((0.5, 6, 3), (15.5, 7.5, 13), 'h'), c((3, 6, 0.5), (13, 7.5, 15.5), 'h'),
                c((1.5, 6, 1.5), (14.5, 7.5, 14.5), 'p', {'origin': [8, 6.75, 8], 'axis': 'y', 'angle': 45}), c((3.5, 7.5, 3.5), (12.5, 9, 12.5), 'p'),
                c((5.5, 9, 5.5), (10.5, 12, 10.5), 'g'), c((7, 3, 7), (9, 4, 9), 'l')]
        for (x, z) in ((0.2, 7.5), (15.2, 7.5), (7.5, 0.2), (7.5, 15.2)): base.append(c((x, 6.4, z), (x + 0.6, 7.1, z + 0.6), 'l'))
        decals = {'none': [], 'stripes': [c((6.6, 7.52, 0.6), (7.4, 9.05, 15.4), 'w'), c((8.6, 7.52, 0.6), (9.4, 9.05, 15.4), 'w')],
                  'crest': [c((3.4, 7.55, 6.5), (3.6, 8.95, 9.5), 'y'), c((12.4, 7.55, 6.5), (12.6, 8.95, 9.5), 'y'), c((6.5, 7.55, 3.4), (9.5, 8.95, 3.6), 'y'),
                            c((6.5, 7.55, 12.4), (9.5, 8.95, 12.6), 'y')],
                  'flames': [c((0.4, 6.2, 5), (0.6, 7.3, 11), 'o'), c((15.4, 6.2, 5), (15.6, 7.3, 11), 'o'), c((5, 6.2, 0.4), (11, 7.3, 0.6), 'r'),
                             c((5, 6.2, 15.4), (11, 7.3, 15.6), 'r'), c((0.35, 6.6, 6.5), (0.65, 7.45, 9.5), 'y'), c((15.35, 6.6, 6.5), (15.65, 7.45, 9.5), 'y')]}
        for d, extra in decals.items():
            R.HATS[f'skiff_{col}_{d}'] = (tex, base + extra)
    # the ghost (a sheet with two dark eyes), the banshee (a taller, tattered one), the mailbox, the Ghost Veil (cosmetic)
    gt = {'s': 'minecraft:block/white_stained_glass', 'e': 'minecraft:block/black_concrete', 'r': 'minecraft:block/red_stained_glass'}
    R.HATS['ghost3d'] = (gt, [c((4, 2, 4), (12, 12, 12), 's'), c((5, 12, 5), (11, 14, 11), 's'), c((5.5, 9, 3.8), (7, 10.5, 4), 'e'), c((9, 9, 3.8), (10.5, 10.5, 4), 'e'),
                              c((3, 2, 3), (5, 5, 5), 's'), c((11, 2, 11), (13, 4, 13), 's')])
    R.HATS['banshee3d'] = (gt, [c((4, 0, 4), (12, 13, 12), 's'), c((5, 13, 5), (11, 15.5, 11), 's'), c((5.2, 10, 3.8), (7, 11.5, 4), 'r'), c((9, 10, 3.8), (10.8, 11.5, 4), 'r'),
                                c((6.5, 6, 3.8), (9.5, 8.5, 4), 'e'), c((2, 3, 6), (4, 10, 8), 's'), c((12, 3, 8), (14, 10, 10), 's')])
    mt = {'r': 'minecraft:block/red_concrete', 'k': 'minecraft:block/black_concrete', 'w': 'minecraft:block/dark_oak_planks', 'f': 'minecraft:block/gold_block'}
    R.HATS['mailbox3d'] = (mt, [c((7, 0, 7), (9, 9, 9), 'w'), c((4.5, 9, 4), (11.5, 14, 12.5), 'r'), c((5, 9.5, 3.8), (11, 13.5, 4), 'k'), c((11.5, 11, 10), (12, 16, 11), 'f'),
                                c((12, 14.5, 10), (14.5, 16, 11), 'f')])
    R.HATS['ghost_veil'] = ({'s': 'minecraft:block/white_stained_glass', 'e': 'minecraft:block/black_concrete'},
                            [c((3, 7, 3), (13, 17, 13), 's'), c((5, 12, 2.8), (7, 13.5, 3), 'e'), c((9, 12, 2.8), (11, 13.5, 3), 'e')])
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + ('skiff_', 'ghost3d', 'banshee3d', 'mailbox3d')
