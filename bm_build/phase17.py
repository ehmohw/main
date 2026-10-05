"""Phase 1.7: weather vials, more Blood Moon goods (Moon Ward, Warding Lantern, Crimson Compass, Blood Bounty),
cosmetic charms, and Heartstones (permanent +1 heart from loot chests, capped at 2 full rows).
Importing registers the items; generate(G) runs after phase16.generate (it patches a few Phase 1.5/1.6 functions)."""
from items import item, T, TOTEM, consumable

# ===================================================================== ITEMS
VIALS = {'clear': ('Vial of Clear Skies', 'aqua', 'clear', 'The clouds part.', 2),
         'rain': ('Vial of Rainfall', 'blue', 'rain', 'Rain begins to fall.', 2),
         'storm': ('Vial of Thunder', 'dark_purple', 'thunder', 'Thunder rolls across the sky!', 4)}
for k, (name, col, _, _, _) in VIALS.items():
    item(f'vial_{k}', TOTEM, name, col,
         ['Drink to change the weather for everyone.', ('Lasts 10 minutes. Overworld only.', 'blue'),
          ('Every player is told who did it.', 'gray'), ('Shared 5-minute cooldown.', 'dark_gray')],
         model=f'bm:vial_{k}', stack=16,
         comps={'minecraft:consumable': consumable(1.0, 'drink', 'minecraft:entity.generic.drink', False)}, cat='weather')

item('moon_ward', TOTEM, 'Moon Ward', 'gray',
     ['Use to hold back the NEXT Blood Moon', 'for one full cycle (30 days).', ('Every player is told who did it.', 'gray'),
      ("Can't stop one that's already rising.", 'dark_gray')],
     model='bm:moon_ward', glint=True, stack=4,
     comps={'minecraft:consumable': consumable(2.0, 'toot_horn', 'minecraft:block.beacon.power_select', False)}, cat='blood')
item('ward_lantern', TOTEM, 'Warding Lantern', 'dark_aqua',
     ['Light it during a Blood Moon.', ('Until dawn, no horror can rise', 'blue'), ('within 48 blocks of you.', 'blue'),
      ('(Ordinary monsters still spawn.)', 'dark_gray')],
     model='bm:ward_lantern', stack=16,
     comps={'minecraft:consumable': consumable(1.0, 'none', 'minecraft:block.soul_sand.place', False)}, cat='blood')
item('crimson_compass', TOTEM, 'Crimson Compass', 'red',
     ['Hold it under a Blood Moon.', ('Points to the nearest horror', 'blue'), ('(or the Monstrosity, if it walks).', 'blue')],
     model='bm:crimson_compass', stack=1, cat='blood')
item('blood_bounty', TOTEM, 'Blood Bounty', 'dark_red',
     ['Sign it during a Blood Moon.', ('Slay 5 horrors before dawn for', 'blue'), ('8 Crystals and a Medallion.', 'blue'),
      ('Unfinished bounties expire at dawn.', 'dark_gray')],
     model='bm:blood_bounty', stack=16,
     comps={'minecraft:consumable': consumable(1.0, 'none', 'minecraft:item.book.page_turn', False)}, cat='blood')

CHARMS = {  # id: (name, colour, lore, particle commands run at the player's feet every 5 ticks)
    'ember': ('Ember Charm', 'gold', 'Little sparks follow you.',
              ['particle minecraft:small_flame ~ ~0.2 ~ 0.3 0.1 0.3 0.01 1', 'particle minecraft:smoke ~ ~0.2 ~ 0.2 0.1 0.2 0 1']),
    'frost': ('Frost Charm', 'aqua', 'Snowflakes drift around you.', ['particle minecraft:snowflake ~ ~1.2 ~ 0.4 0.6 0.4 0.01 1']),
    'petal': ('Petal Charm', 'light_purple', 'Cherry petals fall behind you.', ['particle minecraft:cherry_leaves ~ ~1.8 ~ 0.4 0.2 0.4 0 1']),
    'soul': ('Soul Charm', 'dark_aqua', 'Pale souls trail your steps.',
             ['particle minecraft:soul_fire_flame ~ ~0.1 ~ 0.25 0 0.25 0.005 1', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.4 0.3 0.01 0']),
    'gilded': ('Gilded Charm', 'yellow', 'You shimmer like fresh gold.', ['particle minecraft:wax_on ~ ~1 ~ 0.35 0.6 0.35 0 1']),
    'heart': ('Sweetheart Charm', 'red', 'Little hearts float up now and then.', ['particle minecraft:heart ~ ~2.1 ~ 0.3 0.1 0.3 0 1']),
    'storm': ('Storm Cloud Charm', 'gray', 'A tiny raincloud follows you around.',
              ['particle minecraft:dust{color:[0.52,0.54,0.6],scale:2.4} ~ ~2.75 ~ 0.35 0.06 0.35 0 4',
               'particle minecraft:dust{color:[0.72,0.74,0.78],scale:2.0} ~ ~2.9 ~ 0.25 0.05 0.25 0 2',
               'particle minecraft:falling_water ~ ~2.55 ~ 0.28 0 0.28 0 2',
               'execute store result score #r bm.rng run random value 1..30',
               'execute if score #r bm.rng matches 1 run particle minecraft:electric_spark ~ ~2.6 ~ 0.2 0.1 0.2 0.05 6']),
}
CHARM_PRICE = {'storm': 7}          # Lucky Tokens; everything else 5
# legendary: only from the Blood Moon Monstrosity (10% per kill), never sold
item('charm_eclipse', TOTEM, 'Blood Eclipse', 'dark_red',
     ['Torn from the sky the night the Monstrosity fell.', ('A red moon hangs over you, ringed in blood.', 'red'),
      ('Keep it anywhere in your inventory.', 'gray'), ('LEGENDARY  -  cosmetic only', 'gold')],
     model='bm:charm_eclipse', glint=True, stack=1, bold=True, cat='cosmetic')
HP_CAP = 60              # hard cap on max health from every source: three full rows
for k, (name, col, lore, _) in CHARMS.items():
    item(f'charm_{k}', TOTEM, name, col, [lore, ('Keep it anywhere in your inventory.', 'gray'), ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
         model=f'bm:charm_{k}', stack=1, cat='cosmetic')

HEART_CAP = 10           # +10 hearts on top of the base 10 = two full rows
item('heartstone', TOTEM, 'Heartstone', 'red',
     ['A crystal that beats like a heart.', ('Use it to gain +1 max heart, forever.', 'blue'), ('Kept through death.', 'blue'),
      (f'Up to {HEART_CAP} (two full rows of hearts).', 'gray'), ('Max health from all sources caps at three rows.', 'dark_gray')],
     model='bm:heartstone', glint=True, stack=16,
     comps={'minecraft:consumable': consumable(1.6, 'eat', 'minecraft:entity.warden.heartbeat', False)}, cat='relic')

# loot-chest chance (%) of a Heartstone
HEART_CHANCE = {'simple_dungeon': 2, 'abandoned_mineshaft': 1, 'desert_pyramid': 2, 'jungle_temple': 2, 'stronghold_corridor': 2,
                'stronghold_crossing': 2, 'stronghold_library': 3, 'buried_treasure': 3, 'shipwreck_treasure': 2, 'ruined_portal': 1,
                'bastion_treasure': 5, 'bastion_other': 2, 'nether_bridge': 2, 'end_city_treasure': 5, 'woodland_mansion': 4,
                'pillager_outpost': 1, 'ancient_city': 4, 'igloo_chest': 2}

ARROWS = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']


def generate(G):
    fn, give, title, tellraw, PREFIX, wjson = G.fn, G.give, G.title, G.tellraw, G.PREFIX, G.wjson
    fast, second = [], []

    DENY = {}

    def deny(iid, msg, color='gray'):
        """A refund-with-message function; returns the command that calls it."""
        name = f'p17/deny/{iid}_{len(DENY.setdefault(iid, []))}'
        DENY[iid].append(name)
        fn(name, [give(iid), title('@s', 'actionbar', T(msg + ' (Refunded)', color))])
        return f'return run function bm:{name}'

    # ---------------- weather vials (overworld only, shared 5-minute cooldown, announced)
    for k, (name, col, w, msg, _) in VIALS.items():
        iid = f'vial_{k}'
        G.consume_adv(iid, f'bm:p17/{iid}')
        fn(f'p17/{iid}', [
            f'advancement revoke @s only bm:consume/{iid}',
            'execute unless dimension minecraft:overworld run ' + deny(iid, 'Weather only answers in the Overworld.'),
            'execute if score #wcd bm.bm matches 1.. run ' + deny(iid, 'The sky is still settling. Try again in a few minutes.'),
            f'weather {w} 600s',
            'scoreboard players set #wcd bm.bm 300',
            tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'yellow'}, T(f' uncorked a {name}. ', 'gray'), T(msg, col)]),
            'playsound minecraft:item.bottle.empty player @s ~ ~ ~ 1 0.8',
            'execute as @a at @s run playsound minecraft:ambient.basalt_deltas.additions ambient @s ~ ~ ~ 0.5 1.4'])
    second.append('execute if score #wcd bm.bm matches 1.. run scoreboard players remove #wcd bm.bm 1')

    # ---------------- Moon Ward: skips the next natural Blood Moon (the cycle day 29); cleared on cycle day 0
    G.consume_adv('moon_ward', 'bm:p17/moon_ward')
    fn('p17/moon_ward', [
        'advancement revoke @s only bm:consume/moon_ward',
        'execute if score #active bm.bm matches 1 run ' + deny('moon_ward', 'Too late - the Blood Moon has already risen.', 'red'),
        'execute if score #forced bm.bm matches 1 run ' + deny('moon_ward', 'An Effigy has called tonight\'s moon. A ward cannot undo that.', 'red'),
        'execute if score #skip bm.bm matches 1 run ' + deny('moon_ward', 'A Moon Ward already holds the next Blood Moon back.'),
        'execute if score #cyc bm.bm matches 29 if score #tod bm.bm matches 13000.. run ' + deny('moon_ward', "Tonight's moon has already come and gone."),
        'scoreboard players set #skip bm.bm 1',
        tellraw('@a', PREFIX + [{'selector': '@s', 'color': 'gray'}, T(' raised a ', 'gray'), T('Moon Ward', 'white', bold=True),
                                T('. The next Blood Moon will be held back one cycle.', 'gray')]),
        'execute as @a at @s run playsound minecraft:block.beacon.power_select ambient @s ~ ~ ~ 0.6 0.6'])
    tick_fn = next(n for n, ls in G.FUNCS.items() if any('#cyc bm.bm matches 29 run scoreboard players set #bday bm.bm 1' in l for l in ls))
    ls = G.FUNCS[tick_fn]
    k = next(i for i, l in enumerate(ls) if '#cyc bm.bm matches 29 run scoreboard players set #bday bm.bm 1' in l)
    ls[k + 1:k + 1] = ['execute if score #skip bm.bm matches 1 if score #cyc bm.bm matches 29 run scoreboard players set #bday bm.bm 0',
                       'execute if score #skip bm.bm matches 1 if score #cyc bm.bm matches 0 run scoreboard players set #skip bm.bm 0']
    alm = G.FUNCS['blood/almanac']
    k = next(i for i, l in enumerate(alm) if '#left bm.bm matches 0 run return' in l)
    alm[k:k] = ['execute if score #skip bm.bm matches 1 run scoreboard players add #left bm.bm 30']
    alm.append('execute if score #skip bm.bm matches 1 run ' + tellraw('@s', [T('  (A Moon Ward is holding it back.)', 'gray', italic=True)]))

    # ---------------- Warding Lantern: no horrors (or Monstrosity) rise within 48 blocks until dawn
    G.consume_adv('ward_lantern', 'bm:p17/ward_lantern')
    fn('p17/ward_lantern', [
        'advancement revoke @s only bm:consume/ward_lantern',
        'execute unless score #active bm.bm matches 1 run ' + deny('ward_lantern', 'The lantern only burns under a Blood Moon.'),
        'execute if entity @s[tag=bm.ward] run ' + deny('ward_lantern', 'Your lantern is already lit.'),
        'tag @s add bm.ward',
        title('@s', 'actionbar', T('The lantern flares blue. No horror will rise near you tonight.', 'dark_aqua')),
        'particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 0.6 0.6 0.02 30',
        'playsound minecraft:block.respawn_anchor.set_spawn player @s ~ ~ ~ 1 1.2'])
    ward = 'unless entity @a[tag=bm.ward,distance=..48] '
    for name, lines in G.FUNCS.items():
        if not name.startswith('mobs/blood_roll/'): continue
        for i, l in enumerate(lines):
            if 'run return run function bm:mobs/blood/' in l or 'run return run function bm:monst/spawn' in l:
                lines[i] = l.replace('run return run function', ward + 'run return run function', 1)
    second.append('execute as @a[tag=bm.ward] at @s run particle minecraft:soul_fire_flame ~ ~0.1 ~ 0.5 0 0.5 0 2')

    # ---------------- Crimson Compass: arrow + distance to the nearest horror (Monstrosity first) while held
    fn('p17/compass', [
        'execute unless score #active bm.bm matches 1 run return run ' + title('@s', 'actionbar', T('The needle hangs still. It only wakes under a Blood Moon.', 'gray', italic=True)),
        'tag @e[tag=bm.ctgt] remove bm.ctgt',
        'execute if entity @e[type=minecraft:ravager,tag=bm.monstrosity,distance=..256] run tag @e[type=minecraft:ravager,tag=bm.monstrosity,distance=..256,sort=nearest,limit=1] add bm.ctgt',
        'execute unless entity @e[tag=bm.ctgt] run tag @e[tag=bm.blood,tag=!bm.mount,type=!minecraft:marker,distance=..160,sort=nearest,limit=1] add bm.ctgt',
        'execute unless entity @e[tag=bm.ctgt] run return run ' + title('@s', 'actionbar', T('No horror within 160 blocks.', 'gray')),
        # yaw from the player to the target (via a throwaway marker) vs the player's own yaw
        'summon minecraft:marker ~ ~ ~ {Tags:["bm.cm"]}',
        'execute as @e[type=minecraft:marker,tag=bm.cm,limit=1,sort=nearest] at @s facing entity @e[tag=bm.ctgt,limit=1] feet run tp @s ~ ~ ~ ~ ~',
        'execute store result score #ty bm.rng run data get entity @e[type=minecraft:marker,tag=bm.cm,limit=1,sort=nearest] Rotation[0]',
        'kill @e[type=minecraft:marker,tag=bm.cm]',
        'execute store result score #py bm.rng run data get entity @s Rotation[0]',
        'scoreboard players operation #ty bm.rng %= #360 bm.fx', 'scoreboard players operation #py bm.rng %= #360 bm.fx',
        'execute if score #ty bm.rng matches ..-1 run scoreboard players add #ty bm.rng 360',
        'execute if score #py bm.rng matches ..-1 run scoreboard players add #py bm.rng 360',
        'scoreboard players operation #ty bm.rng -= #py bm.rng', 'scoreboard players add #ty bm.rng 382',
        'scoreboard players operation #ty bm.rng %= #360 bm.fx', 'scoreboard players operation #ty bm.rng /= #45 bm.rng',
        # distance (octagonal estimate: max + 3/8 min)
        'execute store result score #dx bm.rng run data get entity @s Pos[0]', 'execute store result score #dz bm.rng run data get entity @s Pos[2]',
        'execute store result score #tx bm.rng run data get entity @e[tag=bm.ctgt,limit=1] Pos[0]',
        'execute store result score #tz bm.rng run data get entity @e[tag=bm.ctgt,limit=1] Pos[2]',
        'scoreboard players operation #dx bm.rng -= #tx bm.rng', 'scoreboard players operation #dz bm.rng -= #tz bm.rng',
        'execute if score #dx bm.rng matches ..-1 run scoreboard players operation #dx bm.rng *= #-1 bm.rng',
        'execute if score #dz bm.rng matches ..-1 run scoreboard players operation #dz bm.rng *= #-1 bm.rng',
        'scoreboard players operation #big bm.rng = #dx bm.rng', 'scoreboard players operation #big bm.rng > #dz bm.rng',
        'scoreboard players operation #sml bm.rng = #dx bm.rng', 'scoreboard players operation #sml bm.rng < #dz bm.rng',
        'scoreboard players operation #sml bm.rng *= #3 bm.rng', 'scoreboard players operation #sml bm.rng /= #8 bm.rng',
        'scoreboard players operation #big bm.rng += #sml bm.rng',
        'scoreboard players set #mon bm.rng 0',
        'execute if entity @e[tag=bm.ctgt,tag=bm.monstrosity] run scoreboard players set #mon bm.rng 1'] +
        [f'execute if score #ty bm.rng matches {i} if score #mon bm.rng matches {m} run ' +
         title('@s', 'actionbar', [T(a + '  ', 'red', bold=True), T('Monstrosity' if m else 'Blood Moon horror', 'dark_red' if m else 'red'),
                                   T('  ·  ', 'gray'), {'score': {'name': '#big', 'objective': 'bm.rng'}, 'color': 'white'}, T(' blocks', 'gray')])
         for i, a in enumerate(ARROWS) for m in (0, 1)])
    second.append('execute as @a if items entity @s weapon.* *[minecraft:custom_data~{bm:"crimson_compass"}] at @s run function bm:p17/compass')

    # ---------------- Blood Bounty: 5 horror kills before dawn
    G.consume_adv('blood_bounty', 'bm:p17/bounty')
    fn('p17/bounty', [
        'advancement revoke @s only bm:consume/blood_bounty',
        'execute unless score #active bm.bm matches 1 run ' + deny('blood_bounty', 'Bounties are only posted under a Blood Moon.'),
        'execute if entity @s[tag=bm.bty] run ' + deny('blood_bounty', 'You already carry a bounty tonight.'),
        'tag @s add bm.bty', 'scoreboard players set @s bm.bty 0',
        title('@s', 'actionbar', T('Bounty signed: slay 5 horrors before dawn.', 'dark_red')),
        'playsound minecraft:item.book.put player @s ~ ~ ~ 1 0.7'])
    wjson('bm/advancement/p17/bounty_kill.json', {
        'criteria': {'slain': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.blood"]}'}}]}}},
        'rewards': {'function': 'bm:p17/bounty_kill'}})
    fn('p17/bounty_kill', [
        'advancement revoke @s only bm:p17/bounty_kill',
        'execute unless entity @s[tag=bm.bty] run return 0',
        'scoreboard players add @s bm.bty 1',
        'execute if score @s bm.bty matches 5.. run return run function bm:p17/bounty_done',
        title('@s', 'actionbar', [T('Bounty: ', 'dark_red'), {'score': {'name': '@s', 'objective': 'bm.bty'}, 'color': 'white'}, T(' / 5 horrors', 'gray')])])
    fn('p17/bounty_done', [
        'tag @s remove bm.bty', give('blood_crystal', 8), give('medallion'),
        title('@s', 'actionbar', T('Bounty complete! 8 Crystals and a Medallion are yours.', 'gold')),
        'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.8'])
    end = G.FUNCS['bloodmoon/end']
    end += ['execute as @a[tag=bm.bty] run ' + tellraw('@s', PREFIX + [T('Your Blood Bounty expired at dawn.', 'gray')]),
            'tag @a remove bm.bty', 'tag @a remove bm.ward']

    # ---------------- cosmetic charms (first one found shows; hidden while sneaking so Shadowstep stays hidden)
    pick = []
    for k, (_, _, _, parts) in CHARMS.items():
        fn(f'p17/charm/{k}', parts)
        pick.append(f'execute if items entity @s container.* *[minecraft:custom_data~{{bm:"charm_{k}"}}] run return run function bm:p17/charm/{k}')
        pick.append(f'execute if items entity @s weapon.offhand *[minecraft:custom_data~{{bm:"charm_{k}"}}] run return run function bm:p17/charm/{k}')
    fn('p17/charm/eclipse', ['function bm:p17/charm/eclipse_ring with storage bm:fx',
                             'particle minecraft:dust{color:[0.55,0.0,0.02],scale:3.2} ~ ~2.65 ~ 0 0 0 0 1',
                             'particle minecraft:dust{color:[0.08,0.0,0.0],scale:2.2} ~ ~2.65 ~ 0.05 0.05 0.05 0 1',
                             'execute store result score #r bm.rng run random value 1..6',
                             'execute if score #r bm.rng matches 1 run particle minecraft:falling_dust{block_state:"minecraft:redstone_block"} ~ ~2.4 ~ 0.25 0 0.25 0 1'])
    fn('p17/charm/eclipse_ring', ['$execute rotated $(a) 0 positioned ^ ^1.0 ^0.9 run particle minecraft:dust{color:[0.75,0.0,0.05],scale:1.3} ~ ~ ~ 0 0 0 0 1',
                                  '$execute rotated $(b) 0 positioned ^ ^1.0 ^0.9 run particle minecraft:dust{color:[0.3,0.0,0.0],scale:1.3} ~ ~ ~ 0 0 0 0 1'])
    pick[0:0] = ['execute if items entity @s container.* *[minecraft:custom_data~{bm:"charm_eclipse"}] run return run function bm:p17/charm/eclipse',
                 'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"charm_eclipse"}] run return run function bm:p17/charm/eclipse']
    fn('p17/charm/pick', pick)
    fast.append('execute as @a[gamemode=!spectator] unless score @s bm.sneak matches 1.. at @s run function bm:p17/charm/pick')

    # ---------------- Heartstones: a scoreboard count re-applied as one attribute modifier (survives death/respawn)
    G.consume_adv('heartstone', 'bm:p17/heartstone')
    fn('p17/heartstone', [
        'advancement revoke @s only bm:consume/heartstone',
        'execute unless score @s bm.hearts matches 0.. run scoreboard players set @s bm.hearts 0',
        f'execute if score @s bm.hearts matches {HEART_CAP}.. run ' + deny('heartstone', 'Your heart can grow no stronger (two full rows).'),
        'scoreboard players add @s bm.hearts 1',
        'function bm:p17/hearts_apply',
        'effect give @s minecraft:regeneration 3 1 true',
        title('@s', 'actionbar', [T('Your heart grows stronger: ', 'red'), {'score': {'name': '@s', 'objective': 'bm.hearts'}, 'color': 'white'},
                                  T(f' / {HEART_CAP} bonus hearts', 'gray')]),
        'particle minecraft:heart ~ ~2 ~ 0.4 0.3 0.4 0 6',
        'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.8'])
    fn('p17/hearts_apply', ['attribute @s minecraft:max_health modifier remove bm:hearts',
                            'execute store result storage bm:tmp h.amt int 2 run scoreboard players get @s bm.hearts',
                            'function bm:p17/hearts_set with storage bm:tmp h'])
    fn('p17/hearts_set', ['$attribute @s minecraft:max_health modifier add bm:hearts $(amt) add_value'])
    # after death (or any other loss) the modifier is put back, and the new max is filled in
    fn('p17/hearts_restore', ['function bm:p17/hearts_apply', 'effect give @s minecraft:instant_health 1 3 true'])
    second += ['execute as @a[scores={bm.hearts=1..}] store success score @s bm.hok run attribute @s minecraft:max_health modifier value get bm:hearts',
               'execute as @a[scores={bm.hearts=1..,bm.hok=0}] run function bm:p17/hearts_restore']
    # hard cap: max health from every source (base, Heartstones, gear, feasts, effects) never exceeds three rows
    fn('p17/hcap', ['attribute @s minecraft:max_health modifier remove bm:hcap',
                    'execute store result score @s bm.mh run attribute @s minecraft:max_health get 10',
                    f'execute if score @s bm.mh matches ..{HP_CAP * 10} run return 0',
                    # over-cap amount in tenths -> whole points, rounded up (positive maths only), stored as a negative int
                    'scoreboard players operation #c bm.rng = @s bm.mh', f'scoreboard players remove #c bm.rng {HP_CAP * 10 - 9}',
                    'scoreboard players operation #c bm.rng /= #10 bm.rng', 'scoreboard players operation #c bm.rng *= #-1 bm.rng',
                    'execute store result storage bm:tmp hc.amt int 1 run scoreboard players get #c bm.rng',
                    'function bm:p17/hcap_set with storage bm:tmp hc'])
    fn('p17/hcap_set', ['$attribute @s minecraft:max_health modifier add bm:hcap $(amt) add_value'])
    second.append('execute as @a run function bm:p17/hcap')
    for t, pct in HEART_CHANCE.items():
        G.FUNCS[f'loot/{t}'] += ['execute store result score @s bm.rng run random value 1..100',
                                 f'execute if score @s bm.rng matches 1..{pct} run function bm:p17/heart_found']
    fn('p17/heart_found', [give('heartstone'), title('@s', 'actionbar', T('A Heartstone pulses among the loot!', 'red')),
                           'playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 1 1.2'])

    # ---------------- trader refresh: traders in markets built before 1.7 learn the new trades
    O = G.all_offers()
    from nbt import snbt
    import zlib
    # 1.12.1: a trader is refreshed whenever its offer list changes (new trades, new prices, or a new ITEM_VERSION -
    # trade costs match custom_data exactly, so after a restamp the old offers wanted old-version currency and every
    # custom-currency trade failed). The stamp is a checksum of the offer list.
    G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.ofv dummy']
    for k in G.NPCS:
        blob = snbt(O[k])
        ver = zlib.crc32(blob.encode()) % 1000000000
        name = G.NPCS[k][1]
        fn(f'p17/npc/{k}', [f'data modify entity @s Offers.Recipes set value {blob}',
                            f'data modify entity @s CustomName set value {snbt(T(name, G.NPCS[k][2], bold=True))}',
                            'data merge entity @s {CustomNameVisible:0b}', f'scoreboard players set @s bm.ofv {ver}'])
        second.append(f'execute as @e[tag=bm.npc_{k}] unless score @s bm.ofv matches {ver} run function bm:p17/npc/{k}')

    # ---------------- 3D rats: flat rat sprites from older versions become the 3D models (once)
    for v in ('chef', 'prof', 'lucky', 'pirate', 'soldier'):
        fn(f'p17/rat3d/{v}', [f'data modify entity @s item set value {{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:rat3d_{v}"}}}}',
                              'data modify entity @s billboard set value "fixed"'])
        second.append(f'execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.r3d] if items entity @s contents '
                      f'*[minecraft:item_model="bm:rat_{v}"] run function bm:p17/rat3d/{v}')
    second.append('tag @e[type=minecraft:item_display,tag=bm.rat_sprite,tag=!bm.r3d] add bm.r3d')

    # ---------------- wire into the loops
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.hearts dummy', 'scoreboard objectives add bm.hok dummy', 'scoreboard objectives add bm.mh dummy',
                              'scoreboard objectives add bm.bty dummy', 'scoreboard players set #-1 bm.rng -1',
                              'scoreboard players set #3 bm.rng 3', 'scoreboard players set #8 bm.rng 8', 'scoreboard players set #10 bm.rng 10', 'scoreboard players set #45 bm.rng 45']
    G.OBJECTIVES += ['bm.hearts', 'bm.hok', 'bm.bty', 'bm.mh']
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def extend_offers(O, offer):
    # 2.15: the weather vials moved to Salty Sal, Dockmaster (phase36)
    O['blood'] += [offer(('blood_crystal', 6), ('moon_ward', 1)), offer(('blood_crystal', 4), ('ward_lantern', 1)),
                   offer(('blood_crystal', 6), ('crimson_compass', 1)), offer(('blood_crystal', 3), ('blood_bounty', 1))]
    O['lucky'] += [offer(('lucky_token', CHARM_PRICE.get(k, 5)), (f'charm_{k}', 1)) for k in CHARMS]


# ===================================================================== ICONS (resource pack)
def icons(grid):
    I = {}
    vial = ['................', '......KKKK......', '......KccK......', '.......KK.......', '......KWWK......', '.....KW..WK.....',
            '....KW....WK....', '....KLLLLLLK....', '...KLLsLLLLLK...', '...KLsLLLLLLK...', '...KLLLLLLsLK...', '...KLLLLLLLLK...',
            '....KLLLLLLK....', '.....KKKKKK.....', '................', '................']
    for k, (liq, spk) in {'clear': ('#7fd4ff', '#ffe066'), 'rain': ('#2f6fd6', '#a9d0ff'), 'storm': ('#4b2a7a', '#ffd700')}.items():
        I[f'vial_{k}'] = grid(vial, dict(K='#1d1b26', c='#8b5a2b', W='#dfe9f2', L=liq, s=spk))
    I['moon_ward'] = grid(['................', '......KKKK......', '....KKMMMMK.....', '...KMMMMKK......', '..KMMMMK........', '..KMMMK.........',
                           '.KMMMMK.........', '.KMMMMK.....r...', '.KMMMMK....rrr..', '.KMMMMMK....r...', '..KMMMMMK.......', '..KMMMMMMKK.....',
                           '...KMMMMMMMKK...', '....KKMMMMMMK...', '......KKKKK.....', '................'],
                          dict(K='#1c1c24', M='#d8dde6', r='#c0392b'))
    I['ward_lantern'] = grid(['................', '.......KK.......', '......K..K......', '......KKKK......', '.....KIIIIK.....', '....KIGGGGIK....',
                              '....KGBBBBGK....', '....KGBwwBGK....', '....KGBwwBGK....', '....KGBBBBGK....', '....KIGGGGIK....', '.....KIIIIK.....',
                              '......KKKK......', '................', '................', '................'],
                             dict(K='#14141c', I='#4a4f5a', G='#3d6f7a', B='#29b6d6', w='#d6fbff'))
    I['crimson_compass'] = grid(['................', '.....KKKKKK.....', '....KGGGGGGK....', '...KGDDDDDDGK...', '..KGDDDrDDDDGK..', '..KGDDDrrDDDGK..',
                                 '..KGDDDrrDDDGK..', '..KGDDDWWDDDGK..', '..KGDDDssDDDGK..', '..KGDDDssDDDGK..', '..KGDDDDsDDDGK..', '...KGDDDDDDGK...',
                                 '....KGGGGGGK....', '.....KKKKKK.....', '................', '................'],
                                dict(K='#1a0d0d', G='#8a1c1c', D='#2a1a1a', r='#ff3b3b', s='#9aa0a6', W='#ffffff'))
    I['blood_bounty'] = grid(['................', '..KKKKKKKKKK....', '..KPPPPPPPPK....', '...KPllllPPK....', '...KPPPPPPPK....', '...KPllllPPK....',
                              '...KPPPPPPPK....', '...KPlllPPPK....', '...KPPPPRRPK....', '...KPPPRRRRK....', '...KPPPPRRPK....', '..KPPPPPPPPK....',
                              '..KKKKKKKKKK....', '................', '................', '................'],
                             dict(K='#3b2a1a', P='#e8d5a8', l='#7a5a3a', R='#a3122a'))
    charm = ['................', '......KKKK......', '.....K....K.....', '.....K....K.....', '......K..K......', '.......KK.......',
             '......KggK......', '.....KgGGgK.....', '....KgGWGGgK....', '....KGGGGGGK....', '....KGGGGGdK....', '.....KGGGdK.....',
             '......KGdK......', '.......KK.......', '................', '................']
    I['charm_storm'] = grid(['................', '................', '....KKK.KKK.....', '...KCCCKCCCK....', '..KCCCCCCCCCKK..', '.KCCcCCCCCCCCCK.',
                             '.KCccCCCCCcCCCK.', '..KKKKKKKKKKKK..', '...b..b.Y..b....', '....b..YY.b..b..', '..b..b.Y..b.....', '...b...Y..b..b..',
                             '..b..b..b...b...', '................', '................', '................'],
                            dict(K='#3a3d46', C='#9aa1ad', c='#c8ced8', b='#5aa9ff', Y='#ffe04a'))
    I['charm_eclipse'] = grid(['................', '.....rrrrrr.....', '...rrRRRRRRrr...', '..rRRKKKKKKRRr..', '.rRRKKKKKKKKRRr.', '.rRKKKKKKKKKKRr.',
                               'rRRKKKKKKKKKKRRr', 'rRKKKKKKKKKKKKRr', 'rRKKKKKKKKKKKKRr', 'rRRKKKKKKKKKKRRr', '.rRKKKKKKKKKKRr.', '.rRRKKKKKKKKRRr.',
                               '..rRRKKKKKKRRr..', '...rrRRRRRRrr...', '.....rrrrrr.....', '................'],
                              dict(K='#140003', R='#b3001b', r='#ff4040'))
    for k, c in {'ember': '#ff7a1a', 'frost': '#8fe3ff', 'petal': '#ffa3d1', 'soul': '#39d5d5', 'gilded': '#ffd700', 'heart': '#ff3355'}.items():
        I[f'charm_{k}'] = grid(charm, dict(K='#2b2b33', g='#c9b26a', G=c, W='#ffffff', d='#3a3a44'))
    I['heartstone'] = grid(['................', '................', '...KK.....KK....', '..KRRK...KRRK...', '.KRrrRK.KRRRRK..', '.KRrWRRKRRRRRK..',
                            '.KRRRRRRRRRRRK..', '.KRRRRRRRRRRdK..', '..KRRRRRRRRdK...', '...KRRRRRRdK....', '....KRRRRdK.....', '.....KRRdK......',
                            '......KdK.......', '.......K........', '................', '................'],
                           dict(K='#2a0008', R='#e0233f', r='#ff7a8c', W='#ffffff', d='#8c0f22'))
    return I
