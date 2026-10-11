"""2.60: THE GILDED GUTTER VAULT - a party raid (solo works too), with puzzles, guards, an alarm and five tiers.

Getting in: buy the HEIST PLANS from the Fence (reusable). Use them and pick a tier you've unlocked: you and every member
of your party within 24 blocks are led down into the vault (a world of its own, so nothing up top changes - your
standing in the market is untouched). Party members who arrive later use their own plans to join the heist in progress.

A RUN: the Fixer's Den (the lobby: Goldtooth's stall, the heist sheet, the week's records, a copper door that only a
Clockwork Key opens), then 3-7 rooms (one more per tier) drawn at random from seven, then the Vault. Each room's exit
stays barred until it's beaten:
  THE COMBINATION ROOM  set five levers to match the ledger on the far wall (it faces the other way...), then try them.
  THE WEIGHING ROOM     every golden scale must be pressed at once (2-4, by party size; a dropped item counts).
  THE GAUNTLET          run a corridor of sweeping lasers to the plate at its end.
  THE TILE FLOOR        cross the tiles - only a hidden path holds; the peek button shows it for a moment.
  THE DIAL LOCK         turn three dials (item frames) to the arrows on the blueprint.
  THE COUNTING HOUSE    two waves of guards.
  THE THREE COFFERS     a riddle names the honest coffer; the others are Mimics.
THE ALARM: mistakes ring it (wrong combinations, lasers, falling tiles, Mimics, being knocked out). At 50 guards start
patrolling; at 100 the vault goes into LOCKDOWN - guards keep coming and the haul shrinks. Finish under 50: a clean
getaway, an extra share.
THE VAULT: its guardian, the GILDED SENTINEL (it shells itself in gold twice - press the hall's four plates at once to
crack it), then the treasury: everyone stands on the strongbox ring together and it opens - every player gets their own
haul (nothing to fight over). Leave by the emerald plate.
TIERS: I-V. Clearing a tier unlocks the next for you; the first clear of each pays a Gilded armour piece (V: the
Treasurer's Scepter) and a better Raid Banner.
MODIFIERS: each run rolls some (more at higher tiers), each worth extra loot: Lights Out, Hot Floor, Speed Run, Iron
Guards, Glass Cannon, Greedy Vault (more loot, the alarm rings twice as loud), Silent Alarm (it starts at 40).
SPECIAL NIGHTS: on a Blood Moon, a Lucky Night or an Invasion Night the vault changes - BLOOD MOON HEIST (crimson guards,
the Crimson Treasurer, Blood Crystals in the haul, the Crimson Ledger), LUCKY NIGHT HEIST (golden guards, the Golden
Gambler, more coins and Lucky Tokens, the Gambler's Coin) and INVASION HEIST (the Vorn got here first: troopers, the Vorn
Vault-Breaker, Xenite and Power Cells, the Vorn Cracking Rig).
RECORDS: the fastest clear of each tier this week is posted in every lobby; whoever sets one gets the Gutter Laurel.
Dying in the vault isn't the end: the gang drags you back to the lobby (the alarm rings) - your things are where you fell."""
from items import T, ITEMS
from nbt import snbt, B, F, D, Int
import phase70_rooms as RM
import phase67 as P67

GOLD = '#ffcf40'
SLOTS = 8
ZS = 1000                                   # instances lie 1000 blocks apart (z); everything of one lies within ~300 of it
Y0 = 64
KINDS = RM.KINDS
TIER_NAME = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}
TIER_TITLE = {1: 'The Copper Strongroom', 2: 'The Silver Vaults', 3: 'The Gold Reserve', 4: 'The Diamond Deposit', 5: 'The Gutter King\'s Hoard'}
MODS = [(1, 'Lights Out', 'darkness everywhere', '#7a7a8a'), (2, 'Hot Floor', 'the guardhouse and vault floors burn', '#ff7a2a'),
        (4, 'Speed Run', 'beat the clock or the vault locks down', '#7dd8ff'), (8, 'Iron Guards', 'guards and guardian +50% health, tougher', '#c0c0c8'),
        (16, 'Glass Cannon', 'you hit harder - and have half your health', '#ff5a8a'), (32, 'Greedy Vault', '+2 shares, the alarm rings twice as loud', '#ffd23f'),
        (64, 'Silent Alarm', 'the alarm starts at 40', '#ff4a4a')]
NIGHTS = {1: ('BLOOD MOON HEIST', '#ff3030'), 2: ('LUCKY NIGHT HEIST', '#7dff6a'), 3: ('INVASION HEIST', '#b6ff3c')}
BOSS = {0: ('The Gilded Sentinel', GOLD, 'yellow'), 1: ('The Crimson Treasurer', '#ff3030', 'red'), 2: ('The Golden Gambler', '#7dff6a', 'green'),
        3: ('Vorn Vault-Breaker', '#b6ff3c', 'green')}
FIRST_CLEAR = {1: 'gilded_boots', 2: 'gilded_leggings', 3: 'gilded_chestplate', 4: 'gilded_helmet', 5: 'treasurers_scepter'}
CORE_CHANCE = {3: 5, 4: 10, 5: 25}          # per mille, per player per clear: a Shifting Core
P67.BOSSES += [(f'bm.gvboss{s}', f'bm:gvb{s}') for s in range(SLOTS)]       # (the guardian grows with the party, like every boss)
VAULT_PLATES = [(6, 6), (18, 6), (6, 18), (18, 18)]                        # the hall's shell plates


def zoff(s):
    return s * ZS


def generate(G):
    fn, wjson, title, tellraw, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Heist] ', GOLD, bold=True)]
    rel = RM.rel
    objs = ['bm.gvi', 'bm.gvt', 'bm.gva', 'bm.gvtm', 'bm.gvmod', 'bm.gvnt', 'bm.gvst', 'bm.gvk', 'bm.gvrun', 'bm.gvs', 'bm.gvc', 'bm.gvf',
            'bm.gvu', 'bm.gvcl', 'bm.gvon', 'bm.gvbt', 'bm.gve', 'bm.gvpty', 'bm.gvsafe', 'bm.gvw', 'bm.gvlk', 'bm.gvpk', 'bm.gvrec', 'bm.gvx',
            'bm.bond', 'bm.gvzt', 'bm.gvrv']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard objectives add bm.gvdth deathCount'] + \
        [f'bossbar add bm:gva{s} {{text:"Alarm",color:"red"}}' for s in range(SLOTS)] + [f'bossbar set bm:gva{s} color red' for s in range(SLOTS)] + \
        [f'bossbar set bm:gva{s} max 100' for s in range(SLOTS)] + [f'bossbar set bm:gva{s} style notched_10' for s in range(SLOTS)] + \
        [f'bossbar add bm:gvb{s} {{text:"The Gilded Sentinel",color:"gold"}}' for s in range(SLOTS)] + [f'bossbar set bm:gvb{s} color yellow' for s in range(SLOTS)] + \
        ['scoreboard players set #2 bm.rng 2', 'scoreboard players set #7 bm.rng 7', 'scoreboard players set #60 bm.rng 60', 'scoreboard players set #1200 bm.rng 1200',
         'scoreboard players set #20 bm.rng 20', 'scoreboard players set #8 bm.rng 8']
    G.OBJECTIVES += objs + ['bm.gvdth']
    tick, fast, second = [], [], []
    mob_new = 'tag=bm.gvnew2'

    # ------------------------------------------------------------------ the dimension (a void, warm and dim, gold dust in the air)
    wjson('bm/dimension_type/gutter.json', {
        'ambient_light': 0.0, 'has_skylight': False, 'has_ceiling': True, 'has_ender_dragon_fight': False, 'coordinate_scale': 1.0,
        'logical_height': 256, 'min_y': 0, 'height': 256, 'infiniburn': '#minecraft:infiniburn_overworld',
        'monster_spawn_light_level': 0, 'monster_spawn_block_light_limit': 0, 'has_fixed_time': True,
        'default_clock': 'minecraft:the_end', 'timelines': '#minecraft:in_end', 'skybox': 'none',
        'attributes': {
            'minecraft:audio/ambient_sounds': {'mood': {'block_search_extent': 8, 'offset': 2.0, 'sound': 'minecraft:ambient.cave', 'tick_delay': 4000}},
            'minecraft:gameplay/bed_rule': {'can_set_spawn': 'never', 'can_sleep': 'never', 'explodes': True},
            'minecraft:gameplay/respawn_anchor_works': False,
            'minecraft:visual/ambient_light_color': '#2a2010', 'minecraft:visual/fog_color': '#1a1408',
            'minecraft:visual/fog_start_distance': 30.0, 'minecraft:visual/fog_end_distance': 120.0,
            'minecraft:visual/ambient_particles': [{'particle': {'type': 'minecraft:wax_on'}, 'probability': 0.002}],
            'minecraft:visual/sky_light_color': '#3a2a10', 'minecraft:visual/sky_light_factor': 0.0}})
    wjson('bm/dimension/gutter.json', {'type': 'bm:gutter', 'generator': {'type': 'minecraft:flat', 'settings': {
        'biome': 'minecraft:the_void', 'features': False, 'lakes': False, 'layers': [{'block': 'minecraft:air', 'height': 1}], 'structure_overrides': []}}})
    for nm, b in RM.BUILDERS.items():
        b().export(G.path('data', 'bm', 'structure', f'gv_{nm}.nbt'))
        fn(f'p70/place/{nm}', [f'$execute in bm:gutter run place template bm:gv_{nm} $(x) {Y0} $(z)'])

    # ------------------------------------------------------------------ the Heist Plans: plan a heist, or join your party's
    import phase28 as P28
    MENU = 1100
    P28.MENU['heist'] = MENU
    holds_plans = '*[minecraft:custom_data~{bm:"heist_plans"}]'
    fn('p70/plans', ['execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                     'execute if dimension bm:gutter run return run ' + say('You\'re already in the vault. (The emerald plate in the treasury - or the gold plate in the den - takes you out.)', GOLD),
                     'execute unless score @s bm.gvu matches 1.. run scoreboard players set @s bm.gvu 1',
                     # a party heist already running? join it
                     'scoreboard players set #j bm.rng -1',
                     'execute if score @s bm.pty matches 1.. as @e[type=marker,tag=bm.gvinst] if score @s bm.gvpty = @a[limit=1,sort=nearest,tag=bm.gvasker] bm.pty run function bm:p70/joinable'
                     .replace('@a[limit=1,sort=nearest,tag=bm.gvasker]', '#asker'),
                     'execute if score #j bm.rng matches 0.. run return run function bm:p70/join',
                     'execute if score @s bm.pty matches 1.. unless score @s bm.pty = @s bm.pid run return run ' +
                     say('Your party\'s leader plans the heist (or leave the party to go it alone).', GOLD),
                     'function bm:p70/menu'])
    G.FUNCS['p70/plans'].insert(3, 'scoreboard players operation #asker bm.pty = @s bm.pty')
    fn('p70/joinable', ['execute if score @s bm.gvst matches 1..3 store result score #j bm.rng run scoreboard players get @s bm.gvi'])
    btn = lambda t: P28.btn([T(f'Tier {TIER_NAME[t]}  ', GOLD, bold=True), T(TIER_TITLE[t], 'white')], 7600 + t,
                            tooltip=T(f'{t + 2} rooms, then the Vault. ' + ('' if t == 1 else f'(Clear Tier {TIER_NAME[t - 1]} to unlock.)'), 'gray'), width=300)
    dlg = P28.multi([T('The Heist Plans', GOLD, bold=True)],
                    [P28.body([T('Pick the job. ', 'gray'), T('Unlocked: up to Tier ', 'gray'), T('$(u)', GOLD, bold=True), T('.', 'gray')]),
                     P28.body([T('Your party (within 24 blocks) comes with you. Your market standing is never affected.', 'dark_gray')])],
                    [btn(t) for t in range(1, 6)], columns=1, exit_label='Not tonight')
    fn('p70/menu', ['execute store result storage bm:gv m.u int 1 run scoreboard players get @s bm.gvu', f'scoreboard players set @s bm.menu {MENU}',
                    'function bm:p70/menu_show with storage bm:gv m'])
    fn('p70/menu_show', [f'$dialog show @s {snbt(dlg)}'.replace('"$(u)"', '"$(u)"')])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7601..7605 run return run function bm:p70/pick_tier')
    fn('p70/pick_tier', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                         f'execute unless items entity @s container.* {holds_plans} unless items entity @s weapon.offhand {holds_plans} run return run function bm:p28/stale',
                         'scoreboard players operation #t bm.rng = #act bm.pay', 'scoreboard players remove #t bm.rng 7600',
                         'execute if score #t bm.rng > @s bm.gvu run return run ' + say('That tier is still locked - clear the one below it first.', 'red'),
                         'execute if dimension bm:gutter run return 0',
                         'execute unless dimension minecraft:overworld unless dimension minecraft:the_nether unless dimension minecraft:the_end run return run ' + say('The plans don\'t work here.', 'red'),
                         'scoreboard players operation #asker bm.pty = @s bm.pty', 'scoreboard players set #slot bm.rng -1'] +
       [f'execute if score #slot bm.rng matches -1 unless score #s{s} bm.gvon matches 1 run scoreboard players set #slot bm.rng {s}' for s in range(SLOTS)] +
       ['execute if score #slot bm.rng matches -1 run return run ' + say('Every vault crew in the city is busy - try again in a few minutes.', 'red')] +
       [f'execute if score #slot bm.rng matches {s} run function bm:p70/s{s}/claim' for s in range(SLOTS)])

    # ------------------------------------------------------------------ claiming a slot: forceload, wait a second, build, bring everyone in
    for s in range(SLOTS):
        z0 = zoff(s)
        fn(f'p70/s{s}/claim', [f'scoreboard players set #s{s} bm.gvon 1', f'scoreboard players set #bt{s} bm.gvbt 20',
                               f'scoreboard players operation #t{s} bm.gvt = #t bm.rng', f'scoreboard players set #p{s} bm.gvpty 0',
                               f'execute if score @s bm.pty matches 1.. run scoreboard players operation #p{s} bm.gvpty = @s bm.pty',
                               f'scoreboard players add #runs bm.gvrun 1', f'scoreboard players operation #r{s} bm.gvrun = #runs bm.gvrun',
                               f'scoreboard players set #e{s} bm.gve 0',
                               f'execute in bm:gutter run forceload add -16 {z0 - 32} 252 {z0 + 32}',
                               # who comes: you, and your party within 24 blocks
                               f'tag @s add bm.gvwait', f'scoreboard players set @s bm.gvi {s + 1}',
                               f'execute if score @s bm.pty matches 1.. as @a[distance=..24,gamemode=!spectator,tag=!bm.gvwait] if score @s bm.pty = #asker bm.pty run function bm:p70/s{s}/recruit',
                               tellraw('@a[tag=bm.gvwait]', P + [T('The Fixer unrolls the plans... ', 'gray'), T('Tier ', GOLD), {'score': {'name': '#t', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True},
                                                                 T('. Hold on.', 'gray')])])
        fn(f'p70/s{s}/recruit', ['tag @s add bm.gvwait', f'scoreboard players set @s bm.gvi {s + 1}'])
        tick.append(f'execute if score #bt{s} bm.gvbt matches 1.. run function bm:p70/s{s}/count')
        fn(f'p70/s{s}/count', [f'scoreboard players remove #bt{s} bm.gvbt 1', f'execute if score #bt{s} bm.gvbt matches 0 run function bm:p70/s{s}/build'])
        build = [f'scoreboard players operation #gt bm.rng = #t{s} bm.gvt', f'scoreboard players set #gs bm.rng {s}', f'scoreboard players set #gi bm.rng {s + 1}',
                 f'scoreboard players operation #grun bm.rng = #r{s} bm.gvrun',
                 # the night, the modifiers
                 'scoreboard players set #gn bm.rng 0', 'execute if score #active bm.bm matches 1 run scoreboard players set #gn bm.rng 1',
                 'execute if score #gn bm.rng matches 0 if score #lnight bm.bm matches 1 run scoreboard players set #gn bm.rng 2',
                 'execute if score #gn bm.rng matches 0 if score #inv bm.bm matches 1 run scoreboard players set #gn bm.rng 3',
                 'function bm:p70/roll_mods',
                 'scoreboard players operation #gk bm.rng = #gt bm.rng', 'scoreboard players add #gk bm.rng 2',
                 f'data modify storage bm:gv pos set value {{x:0,z:{z0}}}', 'function bm:p70/place/lobby with storage bm:gv pos',
                 f'data modify storage bm:gv pos set value {{x:0,z:{z0 - 25}}}', 'function bm:p70/place/cache with storage bm:gv pos',
                 'execute in bm:gutter as @e[type=marker,tag=bm.gvnew] run function bm:p70/claim_room',
                 'scoreboard players set #pool bm.rng 0']
        for i in range(7):
            build += [f'execute if score #gk bm.rng matches {i + 1}.. run function bm:p70/pick',
                      f'execute if score #gk bm.rng matches {i + 1}.. run data modify storage bm:gv pos set value {{x:{25 * (i + 1)},z:{z0}}}'] + \
                     [f'execute if score #gk bm.rng matches {i + 1}.. if score #r bm.rng matches {j} run function bm:p70/place/{k} with storage bm:gv pos' for j, k in enumerate(KINDS)] + \
                     [f'execute if score #gk bm.rng matches {i + 1}.. in bm:gutter as @e[type=marker,tag=bm.gvnew] run function bm:p70/claim_room',
                      f'execute if score #gk bm.rng matches {i + 1}.. if score #gk bm.rng matches {i + 1} run data modify storage bm:gv pos set value {{x:{25 * (i + 2)},z:{z0}}}',
                      f'execute if score #gk bm.rng matches {i + 1} run function bm:p70/place/vault with storage bm:gv pos']
        build += ['execute in bm:gutter as @e[type=marker,tag=bm.gvnew] run function bm:p70/claim_room',
                  # everyone in: remember where they were, then down they go
                  f'execute as @a[tag=bm.gvwait,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/s{s}/enter',
                  # the den becomes the heist's heart; every room readies itself
                  f'execute in bm:gutter as @e[type=marker,tag=bm.gvr_lobby,scores={{bm.gvi={s + 1}}}] run function bm:p70/inst_init',
                  f'scoreboard players operation #gpl bm.rng = #np{s} bm.gvx',
                  f'execute in bm:gutter as @e[type=marker,tag=bm.gvr,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/r/init']
        fn(f'p70/s{s}/build', build)
        fn(f'p70/s{s}/enter', ['tag @s remove bm.gvwait', 'function bm:p70/save_ret', 'tag @s add bm.gvp', f'scoreboard players operation @s bm.gvrun = #r{s} bm.gvrun',
                               f'execute in bm:gutter run tp @s 3.5 {Y0 + 4} {z0 + 12.5} -90 0', f'bossbar set bm:gva{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]',
                               'effect give @s minecraft:resistance 3 4 true', 'effect give @s minecraft:slow_falling 3 0 true',
                               'playsound minecraft:block.iron_door.close player @s ~ ~ ~ 1 0.6'])
        G.FUNCS[f'p70/s{s}/build'].insert(-2, f'execute store result score #np{s} bm.gvx if entity @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]')
        # joining a heist in progress
        fn(f'p70/s{s}/join', ['function bm:p70/save_ret', 'tag @s add bm.gvp', f'scoreboard players set @s bm.gvi {s + 1}', f'scoreboard players operation @s bm.gvrun = #r{s} bm.gvrun',
                              f'execute in bm:gutter run tp @s 3.5 {Y0 + 4} {z0 + 12.5} -90 0', f'bossbar set bm:gva{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]',
                              'function bm:p70/glass_check', tellraw(f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]', P + [{'selector': '@s', 'color': 'white'}, T(' slips into the vault to join the heist.', 'gray')])])
        # going home - cleanup when nobody's left
        second.append(f'execute if score #s{s} bm.gvon matches 1 unless score #bt{s} bm.gvbt matches 1.. run function bm:p70/s{s}/watch')
        fn(f'p70/s{s}/watch', [f'execute store result score #n bm.rng if entity @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]',
                               f'execute if score #n bm.rng matches 1.. run scoreboard players set #e{s} bm.gve 0',
                               f'execute if score #n bm.rng matches 0 run scoreboard players add #e{s} bm.gve 1',
                               f'execute if score #e{s} bm.gve matches 20.. run function bm:p70/s{s}/clean'])
        clean = [f'execute in bm:gutter positioned -2 40 {z0 - 30} run kill @e[type=!minecraft:player,dx=300,dy=60,dz=62]']
        for x in list(range(0, 225 + 1, 25)) + [250]:
            clean.append(f'execute in bm:gutter run fill {x} {Y0} {z0} {x + 24} {Y0 + 15} {z0 + 24} minecraft:air strict')
        clean += [f'execute in bm:gutter run fill 0 {Y0} {z0 - 25} 24 {Y0 + 15} {z0 - 1} minecraft:air strict',
                  f'execute in bm:gutter positioned -2 40 {z0 - 30} run kill @e[type=minecraft:item,dx=300,dy=60,dz=62]',
                  f'execute in bm:gutter run forceload remove -16 {z0 - 32} 252 {z0 + 32}',
                  f'scoreboard players set #s{s} bm.gvon 0', f'scoreboard players set #e{s} bm.gve 0', f'bossbar set bm:gva{s} players', f'bossbar set bm:gvb{s} players']
        fn(f'p70/s{s}/clean', clean)
    fn('p70/join', [f'execute if score #j bm.rng matches {s + 1} run return run function bm:p70/s{s}/join' for s in range(SLOTS)])

    # (as a fresh room marker) whose it is
    fn('p70/claim_room', ['tag @s remove bm.gvnew', 'scoreboard players operation @s bm.gvi = #gi bm.rng', 'scoreboard players set @s bm.gvs 0', 'scoreboard players set @s bm.gvf 0',
                          'scoreboard players set @s bm.gvtm 0'])
    # (the room draw: #r = a kind not yet in this run)
    fn('p70/pick', ['execute store result score #r bm.rng run random value 0..6'] +
       [f'execute if score #r bm.rng matches {j} run scoreboard players set #bit bm.rng {2 ** j}' for j in range(7)] +
       ['scoreboard players operation #q bm.rng = #pool bm.rng', 'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
        'execute if score #q bm.rng matches 1 run return run function bm:p70/pick', 'scoreboard players operation #pool bm.rng += #bit bm.rng'])
    # (modifiers: T1 0-1, T2 1, T3 1-2, T4 2, T5 2-3)
    fn('p70/roll_mods', ['scoreboard players set #gm bm.rng 0', 'scoreboard players set #nm bm.rng 0',
                         'execute if score #gt bm.rng matches 1 store result score #nm bm.rng run random value 0..1',
                         'execute if score #gt bm.rng matches 2 run scoreboard players set #nm bm.rng 1',
                         'execute if score #gt bm.rng matches 3 store result score #nm bm.rng run random value 1..2',
                         'execute if score #gt bm.rng matches 4 run scoreboard players set #nm bm.rng 2',
                         'execute if score #gt bm.rng matches 5 store result score #nm bm.rng run random value 2..3',
                         'execute if score #nm bm.rng matches 1.. run function bm:p70/roll_mod'])
    fn('p70/roll_mod', ['execute store result score #r bm.rng run random value 0..6'] +
       [f'execute if score #r bm.rng matches {j} run scoreboard players set #bit bm.rng {2 ** j}' for j in range(7)] +
       ['scoreboard players operation #q bm.rng = #gm bm.rng', 'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
        'execute if score #q bm.rng matches 1 run return run function bm:p70/roll_mod', 'scoreboard players operation #gm bm.rng += #bit bm.rng',
        'scoreboard players remove #nm bm.rng 1', 'execute if score #nm bm.rng matches 1.. run function bm:p70/roll_mod'])
    modbit = lambda b: f'execute if function bm:p70/mod{b}'
    for b, nm, _d, _c in MODS:
        fn(f'p70/mod{b}', ['scoreboard players operation #q bm.rng = #gm bm.rng', f'scoreboard players set #bit bm.rng {b}',
                           'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                           'return run execute if score #q bm.rng matches 1'])

    # ------------------------------------------------------------------ return trips: where you came from, and back again
    fn('p70/save_ret', ['data modify storage bm:gv tmp set value {}', 'data modify storage bm:gv tmp.dim set from entity @s Dimension',
                        'execute store result storage bm:gv tmp.x int 1 run data get entity @s Pos[0]', 'execute store result storage bm:gv tmp.y int 1 run data get entity @s Pos[1]',
                        'execute store result storage bm:gv tmp.z int 1 run data get entity @s Pos[2]',
                        'execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p70/save_ret2 with storage bm:gv tmp'])
    fn('p70/save_ret2', ['$data modify storage bm:gv ret.p$(pid) set from storage bm:gv tmp'])
    fn('p70/home', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid',
                    'scoreboard players set #ok bm.rng 0', 'function bm:p70/home2 with storage bm:gv tmp',
                    'execute if score #ok bm.rng matches 0 in minecraft:overworld run tp @s 0 200 0',
                    'execute if score #ok bm.rng matches 0 run effect give @s minecraft:slow_falling 30 0 true',
                    'function bm:p70/unraid'])
    fn('p70/home2', ['$execute if data storage bm:gv ret.p$(pid) run function bm:p70/home3 with storage bm:gv ret.p$(pid)'])
    fn('p70/home3', ['scoreboard players set #ok bm.rng 1', '$execute in $(dim) run tp @s $(x).5 $(y) $(z).5', 'effect give @s minecraft:resistance 3 4 true'])
    fn('p70/unraid', ['tag @s remove bm.gvp', 'tag @s remove bm.gvwait', 'tag @s remove bm.gvdead', 'scoreboard players reset @s bm.gvi',
                      'attribute @s minecraft:max_health modifier remove bm:gv_glass', 'effect clear @s minecraft:darkness'] +
       [f'bossbar set bm:gva{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SLOTS)] +
       [f'bossbar set bm:gvb{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SLOTS)])
    fn('p70/leave', ['function bm:p70/home', 'playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.8',
                     tellraw('@s', P + [T('You slip back out of the vault.', 'gray')])])
    # players in the vault's world who don't belong to a live heist go home (a logout across a cleanup, a server restart)
    second.append('execute as @a at @s if dimension bm:gutter run function bm:p70/belong')
    fn('p70/belong', ['execute unless score @s bm.gvi matches 1.. run return run function bm:p70/home'] +
       [f'execute if score @s bm.gvi matches {s + 1} unless score #s{s} bm.gvon matches 1 run return run function bm:p70/home' for s in range(SLOTS)] +
       [f'execute if score @s bm.gvi matches {s + 1} unless score @s bm.gvrun = #r{s} bm.gvrun run return run function bm:p70/home' for s in range(SLOTS)] +
       ['tag @s add bm.gvp', 'function bm:p70/glass_check'])
    tick.append('execute as @a[tag=bm.gvp] at @s if dimension bm:gutter if entity @s[y=0,dy=50] run function bm:p70/fell_out')
    fn('p70/fell_out', [f'execute if score @s bm.gvi matches {s + 1} in bm:gutter run tp @s 3.5 {Y0 + 4} {zoff(s) + 12.5} -90 0' for s in range(SLOTS)])
    # knocked out: back you come, and the alarm rings
    tick.append('execute as @a[scores={bm.gvdth=1..}] run function bm:p70/died')
    fn('p70/died', ['scoreboard players reset @s bm.gvdth', 'execute if entity @s[tag=bm.gvp] run tag @s add bm.gvdead'])
    # (a moment after the respawn - once the player is standing in the world again)
    tick.append('execute as @a[tag=bm.gvdead,scores={bm.hp=1..}] run function bm:p70/revive_wait')
    fn('p70/revive_wait', ['scoreboard players add @s bm.gvrv 1', 'execute if score @s bm.gvrv matches 30.. at @s run function bm:p70/revive'])
    fn('p70/revive', ['tag @s remove bm.gvdead', 'scoreboard players reset @s bm.gvrv'] +
       [f'execute if score @s bm.gvi matches {s + 1} unless score #s{s} bm.gvon matches 1 run return run function bm:p70/unraid' for s in range(SLOTS)] +
       [f'execute if score @s bm.gvi matches {s + 1} in bm:gutter run tp @s 3.5 {Y0 + 4} {zoff(s) + 12.5} -90 0' for s in range(SLOTS)] +
       ['scoreboard players set #add bm.rng 10', 'scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/alarm_inst',
        'function bm:p70/glass_check',
        tellraw('@s', P + [T('Knocked out! ', 'red', bold=True), T('The gang drags you back to the den. Your things are where you fell.', 'gray')])])

    # ------------------------------------------------------------------ the heist itself: the den is its heart (the instance marker)
    fn('p70/inst_init', ['tag @s add bm.gvinst', 'scoreboard players operation @s bm.gvt = #gt bm.rng', 'scoreboard players operation @s bm.gvmod = #gm bm.rng',
                         'scoreboard players operation @s bm.gvnt = #gn bm.rng', 'scoreboard players operation @s bm.gvk = #gk bm.rng',
                         'scoreboard players operation @s bm.gvrun = #grun bm.rng', 'scoreboard players set @s bm.gvst 1', 'scoreboard players set @s bm.gvtm 0',
                         'scoreboard players set @s bm.gva 0', 'scoreboard players set @s bm.gvlk 0', 'scoreboard players set @s bm.gvw 0',
                         f'scoreboard players operation @s bm.gvpty = #p{{s}} bm.gvpty',
                         modbit(64) + ' run scoreboard players set @s bm.gva 40',
                         'function bm:p70/bar'])
    # (#p{s} by slot)
    G.FUNCS['p70/inst_init'] = [l for l in G.FUNCS['p70/inst_init'] if '#p{s}' not in l] + \
        [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players operation @s bm.gvpty = #p{s} bm.gvpty' for s in range(SLOTS)]
    fn('p70/bar', [f'execute if score @s bm.gvi matches {s + 1} store result bossbar bm:gva{s} value run scoreboard players get @s bm.gva' for s in range(SLOTS)] +
       [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SLOTS)])
    # (#gi = the instance, #add = how loud) ring the alarm
    fn('p70/alarm_inst', ['execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p70/alarm'])
    fn('p70/alarm', ['scoreboard players operation #gm bm.rng = @s bm.gvmod', modbit(32) + ' run scoreboard players operation #add bm.rng *= #2 bm.rng',
                     'scoreboard players operation #old bm.rng = @s bm.gva', 'scoreboard players operation @s bm.gva += #add bm.rng',
                     'execute if score @s bm.gva matches 101.. run scoreboard players set @s bm.gva 100', 'function bm:p70/bar',
                     'function bm:p70/tag_mine',
                     'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.bell.use player @s ~ ~ ~ 1 0.7',
                     'execute if score #old bm.rng matches ..49 if score @s bm.gva matches 50.. run ' + tellraw('@a[tag=bm.gvme]', P + [T('ALERT! ', 'gold', bold=True), T('Guards are on the prowl.', 'gray')]),
                     'execute if score #old bm.rng matches ..99 if score @s bm.gva matches 100.. run function bm:p70/lockdown',
                     'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p70/lockdown', ['scoreboard players set @s bm.gvlk 1', 'scoreboard players set @s bm.gva 100', 'function bm:p70/bar',
                        title('@a[tag=bm.gvme]', 'title', T('LOCKDOWN', 'red', bold=True)), title('@a[tag=bm.gvme]', 'subtitle', T('Guards everywhere - the haul shrinks', 'gray')),
                        'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.bell.resonate player @s ~ ~ ~ 1 0.5'])
    # (as the instance marker) tag its players bm.gvme
    fn('p70/tag_mine', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'execute as @a[tag=bm.gvp] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvme'])
    # every second, each heist: the clock, the modifiers' touch, patrols when the alarm's up, the speed-run limit
    second.append('execute as @e[type=marker,tag=bm.gvinst] at @s run function bm:p70/inst_sec')
    fn('p70/inst_sec', ['scoreboard players operation #gm bm.rng = @s bm.gvmod', 'scoreboard players operation #gi bm.rng = @s bm.gvi',
                        'scoreboard players operation #gn bm.rng = @s bm.gvnt', 'scoreboard players operation #gt bm.rng = @s bm.gvt',
                        'function bm:p70/tag_mine',
                        'execute if score @s bm.gvst matches 2..3 run scoreboard players add @s bm.gvtm 20',
                        modbit(1) + ' run effect give @a[tag=bm.gvme] minecraft:darkness 3 0 true',
                        modbit(4) + ' if score @s bm.gvst matches 2..3 if score @s bm.gvlk matches 0 run function bm:p70/speed',
                        'execute if score @s bm.gvst matches 2..3 if score @s bm.gva matches 50.. run scoreboard players add @s bm.gvw 1',
                        'execute if score @s bm.gvlk matches 0 if score @s bm.gvw matches 40.. run function bm:p70/patrol',
                        'execute if score @s bm.gvlk matches 1 if score @s bm.gvw matches 15.. run function bm:p70/patrol',
                        'execute if score #gn bm.rng matches 1 as @a[tag=bm.gvme] at @s run particle minecraft:dust{color:[0.7,0.05,0.05],scale:1.2} ~ ~1 ~ 6 3 6 0 6',
                        'execute if score #gn bm.rng matches 2 as @a[tag=bm.gvme] at @s run particle minecraft:wax_on ~ ~1.5 ~ 6 3 6 0 6',
                        'execute if score #gn bm.rng matches 3 as @a[tag=bm.gvme] at @s run particle minecraft:dust{color:[0.5,1.0,0.3],scale:1.0} ~ ~1.5 ~ 6 3 6 0 6',
                        'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p70/speed', ['scoreboard players operation #lim bm.rng = @s bm.gvk', 'scoreboard players add #lim bm.rng 2', 'scoreboard players operation #lim bm.rng *= #1200 bm.rng',
                     'execute if score @s bm.gvtm > #lim bm.rng run function bm:p70/lockdown',
                     'scoreboard players operation #left bm.rng = #lim bm.rng', 'scoreboard players operation #left bm.rng -= @s bm.gvtm',
                     'scoreboard players operation #left bm.rng /= #20 bm.rng',
                     'execute if score #left bm.rng matches 0..60 as @a[tag=bm.gvme] run ' + title('@s', 'actionbar', [T('Speed Run: ', '#7dd8ff'), {'score': {'name': '#left', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s left', '#7dd8ff')])])
    # (patrols: two guards beside a player, at most 8 about)
    fn('p70/patrol', ['scoreboard players set @s bm.gvw 0', 'execute store result score #ng bm.rng if entity @e[tag=bm.gvg,distance=..300]',
                      'execute if score #ng bm.rng matches 8.. run return 0',
                      'execute as @a[tag=bm.gvme,sort=random,limit=1] at @s positioned ^2 ^ ^-3 run function bm:p70/guard',
                      'execute as @a[tag=bm.gvme,sort=random,limit=1] at @s positioned ^-2 ^ ^-3 run function bm:p70/guard'])

    # ------------------------------------------------------------------ guards (#gt tier, #gn night, #gm modifiers, #gi instance)
    guard = {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T('Gutter Guard', GOLD),
             'DeathLootTable': 'bm:gv/guard', 'drop_chances': {'head': F(0), 'chest': F(0), 'legs': F(0), 'feet': F(0), 'mainhand': F(0), 'offhand': F(0)},
             'equipment': {'head': {'id': 'minecraft:golden_helmet', 'count': Int(1)}, 'chest': {'id': 'minecraft:chainmail_chestplate', 'count': Int(1)},
                           'mainhand': {'id': 'minecraft:iron_axe', 'count': Int(1)}}}
    captain = dict(guard, CustomName=T('Gutter Captain', GOLD, bold=True), equipment={'head': {'id': 'minecraft:golden_helmet', 'count': Int(1)},
                                                                                     'chest': {'id': 'minecraft:golden_chestplate', 'count': Int(1)},
                                                                                     'mainhand': {'id': 'minecraft:diamond_axe', 'count': Int(1)}})
    fn('p70/guard', ['execute unless block ~ ~ ~ #minecraft:replaceable positioned ~ ~1 ~ unless block ~ ~ ~ #minecraft:replaceable run return 0',
                     'execute if score #gn bm.rng matches 3 run return run function bm:p70/guard_vorn',
                     f'summon minecraft:vindicator ~ ~ ~ {snbt(guard)}', 'function bm:p70/guard_set'])
    fn('p70/captain', ['execute if score #gn bm.rng matches 3 run return run function bm:p70/guard_vorn', f'summon minecraft:vindicator ~ ~ ~ {snbt(captain)}',
                       'tag @e[tag=bm.gvnew2,distance=..1] add bm.gvcap', 'function bm:p70/guard_set'])
    fn('p70/guard_vorn', ['function bm:p32/spawn/trooper', 'tag @e[type=minecraft:husk,tag=bm.vtroop,distance=..1.5,sort=nearest,limit=1] add bm.gvg',
                          'tag @e[type=minecraft:husk,tag=bm.vtroop,distance=..1.5,sort=nearest,limit=1] add bm.gvnew2', 'function bm:p70/guard_set'])
    fn('p70/guard_set', ['execute as @e[tag=bm.gvnew2,distance=..2] at @s run function bm:p70/guard_set1', 'tag @e[tag=bm.gvnew2,distance=..2] remove bm.gvnew2',
                         'particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.02 10', 'playsound minecraft:entity.vindicator.ambient hostile @a[distance=..16] ~ ~ ~ 1 0.9'])
    fn('p70/guard_set1', ['scoreboard players operation @s bm.gvi = #gi bm.rng',
                          'scoreboard players operation #h bm.rng = #gt bm.rng', 'scoreboard players operation #h bm.rng *= #8 bm.rng', 'scoreboard players add #h bm.rng 18',
                          'execute if entity @s[tag=bm.gvcap] run scoreboard players operation #h bm.rng *= #2 bm.rng',
                          modbit(8) + ' run scoreboard players operation #h bm.rng *= #3 bm.rng', modbit(8) + ' run scoreboard players operation #h bm.rng /= #2 bm.rng',
                          modbit(8) + ' run effect give @s minecraft:resistance infinite 0 true',
                          'execute store result entity @s attributes[{id:"minecraft:max_health"}].base double 1 run scoreboard players get #h bm.rng',
                          'attribute @s minecraft:max_health base get', 'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng',
                          'execute if score #gn bm.rng matches 1 if entity @s[type=minecraft:vindicator] run function bm:mobs/blood/vindicator',
                          'execute if score #gn bm.rng matches 2 if entity @s[type=minecraft:vindicator] run function bm:mobs/lucky/vindicator',
                          'execute if score #gn bm.rng matches 1..2 run data modify entity @s PersistenceRequired set value 1b'])
    G.FUNCS['p70/guard_set1'] = [l if 'attributes[{id:"minecraft:max_health"}]' not in l else
                                 'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng' for l in G.FUNCS['p70/guard_set1']]
    G.FUNCS['p70/guard_set1'] = [l if l != 'attribute @s minecraft:max_health base get' else 'function bm:p70/hp with storage bm:gv' for l in G.FUNCS['p70/guard_set1']]
    fn('p70/hp', ['$attribute @s minecraft:max_health base set $(h)'])

    # ------------------------------------------------------------------ rooms: init and tick (as the room's marker, at it)
    fn('p70/r/init', [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p70/r/{k}/init' for k in KINDS + ['lobby', 'vault', 'cache']])
    tick.append('execute as @e[type=marker,tag=bm.gvr,scores={bm.gvs=0..3}] at @s if entity @a[tag=bm.gvp,distance=..22] run function bm:p70/r/tick')
    fn('p70/r/tick', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players add @s bm.gvtm 1'] +
       [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p70/r/{k}/tick' for k in KINDS + ['lobby', 'vault', 'cache']])
    # (a room beaten: its exit opens; a chance at a Clockwork Key fragment each; a trophy if it was done cleanly)
    NAMES = RM.NAMES
    fn('p70/solved', ['scoreboard players set @s bm.gvs 3',
                      f'fill {rel(24, 4, 11)} {rel(24, 7, 13)} minecraft:air replace minecraft:iron_bars',
                      f'particle minecraft:wax_off {rel(24, 5, 12)} 0.2 1 1 0 30', f'playsound minecraft:block.iron_door.open block @a[distance=..30] {rel(24, 5, 12)} 1 0.7',
                      f'playsound minecraft:entity.player.levelup block @a[distance=..30] ~ ~ ~ 0.6 1.4',
                      'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run function bm:p70/solved_p'] +
       [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
        title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - beaten. The way on is open.', 'gray')]) for k in KINDS] +
       [f'execute if entity @s[tag=bm.gvr_{k}] if score @s bm.gvf matches 0 as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run function bm:p70/trophy/{k}' for k in KINDS])
    fn('p70/solved_p', ['execute store result score #r bm.rng run random value 1..100', 'execute if score #r bm.rng matches 1..20 run function bm:p70/frag'])
    fn('p70/frag', ['loot give @s loot bm:items/clockwork_fragment', tellraw('@s', P + [T('A Clockwork Key Fragment ', '#d9a066'), T('ticks in the lock\'s workings - you pocket it.', 'gray')])])
    for k in KINDS:
        fn(f'p70/trophy/{k}', [f'loot give @s loot bm:items/trophy_{k}', tellraw('@s', P + [T('Flawless! ', GOLD, bold=True), T(f'{NAMES[k]}: a trophy for your shelf.', 'gray')])])
    # (as a room: a mistake - #add how loud)
    fn('p70/oops', ['scoreboard players add @s bm.gvf 1', 'function bm:p70/alarm_inst'])

    # ---- THE DEN (lobby): vendor, the heist sheet, the records; the start buttons; the leave plate; the clockwork door
    fn('p70/r/lobby/init', [f'summon minecraft:villager {rel(5, 4, 18)} {snbt(goldtooth())}', f'tp @e[type=minecraft:villager,tag=bm.gvgt,distance=..12,sort=nearest,limit=1] ~ ~ ~ 180 0'.replace('~ ~ ~', rel(5, 4, 18)),
                            f'summon minecraft:text_display {rel(12, 6, 1)} {{Tags:["bm.gvsheet","bm.gvnew3"],billboard:"fixed",line_width:220,background:1879048192,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.8f,0.8f,0.8f]}},text:""}}',
                            f'summon minecraft:text_display {rel(19, 6, 1)} {{Tags:["bm.gvboard","bm.gvnew3"],billboard:"fixed",line_width:240,background:1879048192,transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}},text:""}}',
                            f'summon minecraft:text_display {rel(2, 6, 4)} {{Tags:["bm.gvnew3"],billboard:"vertical",text:{{text:"Leave the heist",color:"gray"}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}',
                            f'summon minecraft:text_display {rel(23, 7, 12)} {{Tags:["bm.gvnew3"],billboard:"vertical",text:{{text:"Press a button to begin",color:"gold"}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}',
                            f'summon minecraft:text_display {rel(12, 7, 1)} {{Tags:["bm.gvnew3"],billboard:"vertical",text:{{text:"A Clockwork Key opens this",color:"#d9a066"}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]}}}}',
                            'execute as @e[type=minecraft:text_display,tag=bm.gvnew3,distance=..20] run function bm:p70/claim_disp',
                            'function bm:p70/sheet', 'function bm:p70/board'])
    fn('p70/claim_disp', ['tag @s remove bm.gvnew3', 'scoreboard players operation @s bm.gvi = #gi bm.rng'])
    G.FUNCS['p70/r/lobby/init'].insert(0, 'scoreboard players operation #gi bm.rng = @s bm.gvi')
    # the heist sheet: the job, the night, the modifiers
    sheet = ['data modify storage bm:gv sheet set value [{text:"THE JOB\\n",color:"gold",bold:true}]'] + \
            [f'execute if score #gt bm.rng matches {t} run data modify storage bm:gv sheet append value {{text:"Tier {TIER_NAME[t]}: {TIER_TITLE[t]}\\n",color:"white"}}' for t in range(1, 6)] + \
            ['data modify storage bm:gv sheet append value {text:"",color:"gray"}'] + \
            [f'execute if score #gn bm.rng matches {n} run data modify storage bm:gv sheet append value {{text:"{nm}!\\n",color:"{c}",bold:true}}' for n, (nm, c) in NIGHTS.items()] + \
            [f'{modbit(b)} run data modify storage bm:gv sheet append value {{text:"{nm} - {d}\\n",color:"{c}"}}' for b, nm, d, c in MODS] + \
            ['execute if score #gm bm.rng matches 0 run data modify storage bm:gv sheet append value {text:"No modifiers - a quiet job.\\n",color:"gray"}',
             'data modify storage bm:gv sheet append value {text:"\\nPress a button by the door to begin.",color:"dark_gray"}',
             'execute as @e[type=minecraft:text_display,tag=bm.gvsheet,distance=..20] run data modify entity @s text set from storage bm:gv sheet']
    fn('p70/sheet', sheet)
    fn('p70/board', ['function bm:p70/rec_week', 'data modify storage bm:gv bd set value [{text:"THIS WEEK\'S FASTEST\\n",color:"gold",bold:true}]'] +
       sum(([f'execute unless data storage bm:gv rec.t{t} run data modify storage bm:gv bd append value {{text:"Tier {TIER_NAME[t]}: no record yet\\n",color:"gray"}}',
             f'execute if data storage bm:gv rec.t{t} run data modify storage bm:gv bd append from storage bm:gv rec.t{t}',
             'data modify storage bm:gv bd append value {text:"\\n"}'] for t in range(1, 6)), []) +
       ['execute as @e[type=minecraft:text_display,tag=bm.gvboard,distance=..20] run data modify entity @s text set from storage bm:gv bd'])
    fn('p70/r/lobby/tick', ['execute if score @s bm.gvs matches 0 if block ' + rel(23, 5, 15) + ' #minecraft:buttons[powered=true] run function bm:p70/begin',
                            'execute if score @s bm.gvs matches 0 if block ' + rel(23, 5, 9) + ' #minecraft:buttons[powered=true] run function bm:p70/begin',
                            f'execute positioned {rel(2, 4, 4)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p70/leave'])
    G.FUNCS['p70/r/lobby/tick'] = [l.replace(' #minecraft:buttons[powered=true]', ' minecraft:pale_oak_button[powered=true]') for l in G.FUNCS['p70/r/lobby/tick']]
    fn('p70/begin', ['scoreboard players set @s bm.gvs 1', f'fill {rel(24, 4, 11)} {rel(24, 7, 13)} minecraft:air replace minecraft:iron_bars',
                     'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players set @s bm.gvst 2',
                     'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p70/tag_mine',
                     title('@a[tag=bm.gvme]', 'title', T('THE HEIST IS ON', GOLD, bold=True)), title('@a[tag=bm.gvme]', 'subtitle', T('Quick and quiet...', 'gray')),
                     'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.iron_door.open player @s ~ ~ ~ 1 0.6', 'tag @a[tag=bm.gvme] remove bm.gvme'])

    # ---- THE COMBINATION ROOM: five levers to match the ledger (frames on the far wall: gold = pull it)
    LV = [8, 10, 12, 14, 16]
    fn('p70/r/levers/init', ['execute store result score @s bm.gvc run random value 1..31', 'scoreboard players operation #b bm.rng = @s bm.gvc'] +
       sum(([f'scoreboard players operation #q bm.rng = #b bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng', 'scoreboard players operation #b bm.rng /= #2 bm.rng',
             f'execute if score #q bm.rng matches 1 run summon minecraft:item_frame {rel(x, 6, 1)} {{Facing:3b,Fixed:1b,Invulnerable:1b,Tags:["bm.gvprop"],Item:{{id:"minecraft:gold_ingot",count:1}}}}',
             f'execute if score #q bm.rng matches 0 run summon minecraft:item_frame {rel(x, 6, 1)} {{Facing:3b,Fixed:1b,Invulnerable:1b,Tags:["bm.gvprop"],Item:{{id:"minecraft:coal",count:1}}}}']
            for x in LV), []) +
       [f'summon minecraft:text_display {rel(12, 8, 1)} {{billboard:"fixed",Tags:["bm.gvprop"],text:[{{text:"THE LEDGER\\n",color:"gold",bold:true}},{{text:"Gold: pulled.  Coal: left alone.\\nThe ledger faces the levers - not you.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}',
        f'summon minecraft:text_display {rel(12, 8, 22)} {{billboard:"fixed",Rotation:[180f,0f],Tags:["bm.gvprop"],text:[{{text:"Set the levers, then press the button.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/levers/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                             f'execute if block {rel(12, 7, 23)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvlatch] run function bm:p70/r/levers/try',
                             f'execute unless block {rel(12, 7, 23)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvlatch'])
    fn('p70/r/levers/try', ['tag @s add bm.gvlatch', 'scoreboard players operation #b bm.rng = @s bm.gvc', 'scoreboard players set #bad bm.rng 0'] +
       sum(([f'scoreboard players operation #q bm.rng = #b bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng', 'scoreboard players operation #b bm.rng /= #2 bm.rng',
             f'execute if score #q bm.rng matches 1 unless block {rel(x, 5, 23)} minecraft:lever[powered=true] run scoreboard players set #bad bm.rng 1',
             f'execute if score #q bm.rng matches 0 if block {rel(x, 5, 23)} minecraft:lever[powered=true] run scoreboard players set #bad bm.rng 1'] for x in LV), []) +
       ['execute if score #bad bm.rng matches 0 run return run function bm:p70/solved',
        'scoreboard players set #add bm.rng 15', 'function bm:p70/oops'] +
       [f'setblock {rel(x, 5, 23)} minecraft:lever[face=wall,facing=north,powered=false]' for x in LV] +
       ['playsound minecraft:block.anvil.land block @a[distance=..24] ~ ~ ~ 0.6 0.6',
        'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('Wrong combination - the levers snap back and a bell rings somewhere.', 'red'))])

    # ---- THE WEIGHING ROOM: the first N of four golden scales at once (N: 2-4, by the heist's players)
    PL = [(5, 5), (19, 5), (5, 19), (19, 19)]
    fn('p70/r/plates/init', ['scoreboard players operation @s bm.gvc = #gpl bm.rng', 'execute if score @s bm.gvc matches ..1 run scoreboard players set @s bm.gvc 2',
                             'execute if score @s bm.gvc matches 5.. run scoreboard players set @s bm.gvc 4'] +
       [f'execute if score @s bm.gvc matches ..{i} run setblock {rel(x, 4, z)} minecraft:chiseled_polished_blackstone' for i, (x, z) in enumerate(PL) if i >= 2] +
       [f'summon minecraft:text_display {rel(12, 7, 1)} {{billboard:"vertical",Tags:["bm.gvprop"],text:[{{text:"THE WEIGHING ROOM\\n",color:"gold",bold:true}},{{text:"Every golden scale must tip at once.\\nAnything with weight will do - even a dropped item.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/plates/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                             'execute if score @s bm.gvtm matches 1200 run scoreboard players set @s bm.gvf 1',      # (a minute: no trophy)
                             'scoreboard players set #n bm.rng 0'] +
       [f'execute if score @s bm.gvc matches {i + 1}.. if block {rel(x, 4, z)} minecraft:light_weighted_pressure_plate unless block {rel(x, 4, z)} minecraft:light_weighted_pressure_plate[power=0] run scoreboard players add #n bm.rng 1'
        for i, (x, z) in enumerate(PL)] +
       ['execute if score #n bm.rng >= @s bm.gvc run function bm:p70/solved'] +
       [f'execute if score @s bm.gvc matches {i + 1}.. run particle minecraft:wax_on {rel(x, 4, z)} 0.3 0.1 0.3 0 1' for i, (x, z) in enumerate(PL)])

    # ---- THE GAUNTLET: five laser planes sweep on and off (staggered); touch one - zap, back to the start, the alarm rings
    LZ = [5, 9, 13, 17, 21]
    fn('p70/r/lasers/init', [f'summon minecraft:text_display {rel(2, 7, 12)} {{billboard:"vertical",Tags:["bm.gvprop"],text:[{{text:"THE GAUNTLET\\n",color:"gold",bold:true}},{{text:"Time your run. Red light means stop.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    lz_tick = ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
               'scoreboard players operation #lt bm.rng = @s bm.gvtm']
    for i, x in enumerate(LZ):
        lz_tick += [f'scoreboard players operation #p bm.rng = #lt bm.rng', f'scoreboard players add #p bm.rng {i * 12}', 'scoreboard players operation #p bm.rng %= #60 bm.rng',
                    f'execute if score #p bm.rng matches ..29 run function bm:p70/r/lasers/on{i}',
                    f'execute if score #p bm.rng matches 44..59 run function bm:p70/r/lasers/warn{i}']
        line = lambda y, step: [f'particle minecraft:dust{{color:[1.0,0.1,0.1],scale:0.7}} {rel(x, 0, 0).split()[0]} ~{y} ~{z / 10 - 12 + 0.5:.1f} 0 0 0 0 1' for z in range(60, 190, step)]
        fn(f'p70/r/lasers/on{i}', ['scoreboard players operation #q bm.rng = #lt bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                                   f'execute if score #q bm.rng matches 0 run function bm:p70/r/lasers/draw{i}',
                                   f'execute positioned {rel(x, 4, 6)} positioned ~-0.5 ~ ~-0.5 as @a[tag=bm.gvp,dx=0,dy=0.6,dz=12,tag=!bm.gvzap] at @s run function bm:p70/r/lasers/zap'])
        fn(f'p70/r/lasers/draw{i}', line(0.4, 9) + line(1.2, 9) + [f'playsound minecraft:block.beacon.ambient block @a[distance=..16] {rel(x, 5, 12)} 0.2 2'])
        fn(f'p70/r/lasers/warn{i}', ['scoreboard players operation #q bm.rng = #lt bm.rng', 'scoreboard players operation #q bm.rng %= #8 bm.rng',
                                     f'execute if score #q bm.rng matches 0 run particle minecraft:dust{{color:[1.0,0.5,0.1],scale:0.5}} {rel(x, 5, 12)} 0 0.6 3 0 6'])
    fn('p70/r/lasers/tick', lz_tick + [f'execute positioned {rel(22, 4, 12)} if entity @a[tag=bm.gvp,distance=..1.2] positioned as @s run function bm:p70/solved'])
    fn('p70/r/lasers/zap', ['tag @s add bm.gvzap', 'damage @s 4 minecraft:magic', 'particle minecraft:flash{color:[1.0,0.2,0.2,1.0]} ~ ~1 ~ 0 0 0 0 1',
                            'playsound minecraft:entity.guardian.attack player @a[distance=..16] ~ ~ ~ 1 1.6',
                            'execute as @e[type=marker,tag=bm.gvr_lasers,distance=..20,sort=nearest,limit=1] at @s run function bm:p70/r/lasers/zapped',
                            say('ZAP! Back to the start.', 'red'), 'scoreboard players set @s bm.gvzt 30'])
    fn('p70/r/lasers/zapped', ['scoreboard players set #add bm.rng 8', 'function bm:p70/oops', f'tp @a[tag=bm.gvzap,distance=..20] {rel(2, 4, 12)} -90 0'])
    tick.append('execute as @a[tag=bm.gvzap] run function bm:p70/r/lasers/unzap')
    fn('p70/r/lasers/unzap', ['scoreboard players remove @s bm.gvzt 1', 'execute unless score @s bm.gvzt matches 1.. run tag @s remove bm.gvzap'])

    # ---- THE TILE FLOOR: a hidden path across 6 x 5 tiles; others drop you in the coin pit (back to the start); the peek button
    def tile_center(c, r):
        return (3 + 3 * c + 1, 4, 5 + 3 * r + 1)
    fn('p70/r/tiles/init', [f'summon minecraft:marker {rel(*tile_center(c, r))} {{Tags:["bm.gvtile","bm.gvt{c}{r}","bm.gvprop"]}}' for c in range(6) for r in range(5)] +
       ['execute as @e[type=marker,tag=bm.gvtile,distance=..14] run scoreboard players set @s bm.gvsafe 0',
        'execute store result score #r bm.rng run random value 0..4'] +
       sum(([f'execute if score #r bm.rng matches {r} as @e[type=marker,tag=bm.gvt{c}{r},distance=..14] run scoreboard players set @s bm.gvsafe 1' for r in range(5)] +
            ['execute store result score #m bm.rng run random value -1..1', 'scoreboard players operation #r bm.rng += #m bm.rng',
             'execute if score #r bm.rng matches ..-1 run scoreboard players set #r bm.rng 0', 'execute if score #r bm.rng matches 5.. run scoreboard players set #r bm.rng 4'] +
            [f'execute if score #r bm.rng matches {r} as @e[type=marker,tag=bm.gvt{c}{r},distance=..14] run scoreboard players set @s bm.gvsafe 1' for r in range(5)]
            for c in range(6)), []) +
       [f'summon minecraft:text_display {rel(1, 7, 12)} {{billboard:"vertical",Tags:["bm.gvprop"],text:[{{text:"THE TILE FLOOR\\n",color:"gold",bold:true}},{{text:"Only one way holds. The button shows it - once for free.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/tiles/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                            f'execute if block {rel(1, 5, 9)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvlatch] run function bm:p70/r/tiles/peek',
                            f'execute unless block {rel(1, 5, 9)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvlatch',
                            'execute if score @s bm.gvpk matches 1.. run scoreboard players remove @s bm.gvpk 1',
                            'execute if score @s bm.gvpk matches 1.. as @e[type=marker,tag=bm.gvtile,distance=..14,scores={bm.gvsafe=1}] at @s run particle minecraft:happy_villager ~ ~0.2 ~ 0.6 0 0.6 0 1',
                            'execute as @e[type=marker,tag=bm.gvtile,distance=..14,scores={bm.gvsafe=0},tag=!bm.gvdown] at @s if entity @a[tag=bm.gvp,distance=..1.15] run function bm:p70/r/tiles/drop',
                            'execute as @e[type=marker,tag=bm.gvtile,tag=bm.gvdown,distance=..14] run function bm:p70/r/tiles/back',
                            f'execute positioned {rel(3, 0, 5)} positioned ~-0.5 ~-0.5 ~-0.5 as @a[tag=bm.gvp,dx=17,dy=2.4,dz=14] at @s run function bm:p70/r/tiles/pit',
                            f'execute positioned {rel(22, 4, 12)} if entity @a[tag=bm.gvp,distance=..2] positioned as @s run function bm:p70/solved'])
    fn('p70/r/tiles/peek', ['tag @s add bm.gvlatch', 'scoreboard players set @s bm.gvpk 60', 'scoreboard players add @s bm.gvc 1',
                            'execute if score @s bm.gvc matches 2.. run scoreboard players set #add bm.rng 5', 'execute if score @s bm.gvc matches 2.. run function bm:p70/alarm_inst',
                            'playsound minecraft:block.amethyst_block.chime block @a[distance=..24] ~ ~ ~ 1 1.2'])
    fn('p70/r/tiles/drop', ['tag @s add bm.gvdown', 'scoreboard players set @s bm.gvsafe 60', 'fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:air',
                            'particle minecraft:block{block_state:"minecraft:polished_blackstone"} ~ ~ ~ 1 0.2 1 0 30', 'playsound minecraft:block.stone.break block @a[distance=..24] ~ ~ ~ 1 0.6',
                            'execute as @e[type=marker,tag=bm.gvr_tiles,distance=..14,sort=nearest,limit=1] run tag @s add bm.gvtilef'])
    fn('p70/r/tiles/back', ['scoreboard players remove @s bm.gvsafe 1', 'execute if score @s bm.gvsafe matches 1.. run return 0', 'scoreboard players set @s bm.gvsafe 0', 'tag @s remove bm.gvdown',
                            'execute at @s run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:polished_blackstone'])
    fn('p70/r/tiles/pit', ['scoreboard players set #add bm.rng 6', 'execute as @e[type=marker,tag=bm.gvr_tiles,distance=..20,sort=nearest,limit=1] at @s run function bm:p70/oops',
                           'execute at @e[type=marker,tag=bm.gvr_tiles,distance=..20,sort=nearest,limit=1] run tp @s ' + rel(1, 4, 12) + ' -90 0',
                           'playsound minecraft:entity.player.splash player @a[distance=..16] ~ ~ ~ 1 1', say('Into the coin pit! A rope hauls you back to the start.', 'red')])
    # (the dropped tiles' blocks come back as they were - the checker squares)
    G.FUNCS['p70/r/tiles/back'][-1] = 'execute at @s run function bm:p70/r/tiles/refill'
    fn('p70/r/tiles/refill', [f'execute if entity @s[tag=bm.gvt{c}{r}] run return run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 minecraft:{"polished_blackstone" if (c + r) % 2 == 0 else "gilded_blackstone"}'
                              for c in range(6) for r in range(5)])

    # ---- THE DIAL LOCK: three dials (item frames) turned to the blueprint's arrows
    DX = [10, 12, 14]
    ARROWS = ['↑', '↗', '→', '↘', '↓', '↙', '←', '↖']
    G.FUNCS['load'][-1:-1] = ['data modify storage bm:gv arrows set value ' + snbt([ARROWS[(1 + r) % 8] for r in range(8)])]
    fn('p70/r/dial/init', [f'summon minecraft:item_frame {rel(x, 6, 22)} {{Facing:2b,Invulnerable:1b,Tags:["bm.gvprop","bm.gvdial{i}"],Item:{{id:"minecraft:arrow",count:1}}}}' for i, x in enumerate(DX)] +
       [f'execute store result score #d{i} bm.rng run random value 1..7' for i in range(3)] +
       ['scoreboard players operation @s bm.gvc = #d0 bm.rng', 'scoreboard players operation #q bm.rng = #d1 bm.rng', 'scoreboard players operation #q bm.rng *= #8 bm.rng',
        'scoreboard players operation @s bm.gvc += #q bm.rng', 'scoreboard players operation #q bm.rng = #d2 bm.rng', 'scoreboard players operation #q bm.rng *= #8 bm.rng',
        'scoreboard players operation #q bm.rng *= #8 bm.rng', 'scoreboard players operation @s bm.gvc += #q bm.rng'] +
       [f'execute store result storage bm:gv dial.i{i} int 1 run scoreboard players get #d{i} bm.rng' for i in range(3)] +
       ['function bm:p70/r/dial/arrows with storage bm:gv dial',
        f'summon minecraft:text_display {rel(12, 9, 22)} {{billboard:"fixed",Rotation:[180f,0f],Tags:["bm.gvprop","bm.gvbp"],text:"",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.9f,0.9f,0.9f]}}}}',
        'function bm:p70/r/dial/text with storage bm:gv dial'])
    fn('p70/r/dial/arrows', ['$data modify storage bm:gv dial.a set from storage bm:gv arrows[$(i0)]', '$data modify storage bm:gv dial.b set from storage bm:gv arrows[$(i1)]',
                             '$data modify storage bm:gv dial.c set from storage bm:gv arrows[$(i2)]'])
    fn('p70/r/dial/text', ['$data merge entity @e[type=minecraft:text_display,tag=bm.gvbp,distance=..14,limit=1] {text:[{text:"THE BLUEPRINT\\n",color:"gold",bold:true},{text:"Turn the dials to:  $(a)   $(b)   $(c)",color:"white"}]}'])
    fn('p70/r/dial/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                           'execute if score @s bm.gvtm matches 900 run scoreboard players set @s bm.gvf 1',
                           'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #5 bm.rng',
                           'execute unless score #q bm.rng matches 0 run return 0',
                           'scoreboard players operation #c bm.rng = @s bm.gvc'] +
       sum(([f'scoreboard players operation #want bm.rng = #c bm.rng', 'scoreboard players operation #want bm.rng %= #8 bm.rng', 'scoreboard players operation #c bm.rng /= #8 bm.rng',
             f'execute store result score #have bm.rng run data get entity @e[type=minecraft:item_frame,tag=bm.gvdial{i},distance=..14,limit=1] ItemRotation',
             'execute unless score #have bm.rng = #want bm.rng run return 0'] for i in range(3)), []) +
       ['execute as @e[type=minecraft:item_frame,tag=bm.gvprop,distance=..14] run data modify entity @s Fixed set value 1b', 'function bm:p70/solved'])

    # ---- THE COUNTING HOUSE: two waves of guards (the second with a captain)
    SP = [(4, 4, 6), (20, 4, 6), (4, 4, 18), (20, 4, 18), (12, 4, 4), (12, 4, 20)]
    fn('p70/r/guards/init', [modbit(2) + f' run fill {rel(1, 3, 1)} {rel(23, 3, 23)} minecraft:magma_block replace minecraft:polished_blackstone'])
    fn('p70/r/guards/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvtm matches 1500 run scoreboard players set @s bm.gvf 1',
                             'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p70/r/guards/wave1',
                             'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                             'execute unless score #q bm.rng matches 0 run return 0',
                             'execute store result score #n bm.rng if entity @e[tag=bm.gvg,distance=..18]',
                             'execute if score @s bm.gvs matches 1 if score #n bm.rng matches 0 run function bm:p70/r/guards/wave2',
                             'execute if score @s bm.gvs matches 2 if score #n bm.rng matches 0 run function bm:p70/solved'])
    def wave(n_extra, cap):
        return ['scoreboard players set @s bm.gvtm 0', 'function bm:p70/ctx',
                'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..300]', 'scoreboard players operation #n bm.rng += #gt bm.rng',
                f'scoreboard players add #n bm.rng {n_extra}'] + \
               [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(*SP[i % 6])} run function bm:p70/guard' for i in range(10)] + \
               ([f'execute positioned {rel(12, 4, 20)} run function bm:p70/captain'] if cap else []) + \
               ['execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('Guards!' if not cap else 'More guards - and their captain!', 'red'))]
    fn('p70/r/guards/wave1', ['scoreboard players set @s bm.gvs 1'] + wave(1, False))
    fn('p70/r/guards/wave2', ['scoreboard players set @s bm.gvs 2'] + wave(2, True))
    G.FUNCS['p70/r/guards/tick'][1] = 'execute if score @s bm.gvs matches 1..2 if score @s bm.gvtm matches 1500 run scoreboard players set @s bm.gvf 1'
    # (as a room: the heist's tier, night, modifiers)
    fn('p70/ctx', ['execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function bm:p70/ctx1'])
    fn('p70/ctx1', ['scoreboard players operation #gt bm.rng = @s bm.gvt', 'scoreboard players operation #gn bm.rng = @s bm.gvnt', 'scoreboard players operation #gm bm.rng = @s bm.gvmod'])

    # ---- THE THREE COFFERS: a riddle; the honest coffer opens the way, the others are Mimics
    import itertools
    KIND_ITEMS = {'oak chest': 'minecraft:chest', 'copper chest': 'minecraft:copper_chest', 'ender chest': 'minecraft:ender_chest', 'barrel': 'minecraft:barrel'}
    kinds = list(KIND_ITEMS)
    perms = [p for p in itertools.permutations(kinds)][::4][:6]
    CZ = [6, 10, 14, 18]
    def statements(perm, h):
        pos = {k: i for i, k in enumerate(perm)}
        S = []
        for k in perm:
            if pos[k] != h: S.append((f'It is not the {k}.', {i for i in range(4) if i != pos[k]}))
            if abs(pos[k] - h) == 1: S.append((f'It stands right beside the {k}.', {i for i in range(4) if abs(i - pos[k]) == 1}))
            if h < pos[k]: S.append((f'It sits somewhere left of the {k}.', {i for i in range(4) if i < pos[k]}))
            if h > pos[k]: S.append((f'It sits somewhere right of the {k}.', {i for i in range(4) if i > pos[k]}))
        if h in (1, 2): S.append(('It is not at either end of the row.', {1, 2}))
        else: S.append(('It sits at one end of the row.', {0, 3}))
        return S
    riddles = {}
    for pi, perm in enumerate(perms):
        for h in range(4):
            S = statements(perm, h)
            found = []
            for a, b in itertools.combinations(S, 2):
                if a[1] & b[1] == {h}: found.append((a[0], b[0]))
            for a, b, c in itertools.combinations(S, 3):
                if len(found) >= 3: break
                if a[1] & b[1] & c[1] == {h} and not (a[1] & b[1] == {h} or a[1] & c[1] == {h} or b[1] & c[1] == {h}): found.append((a[0], b[0], c[0]))
            assert found, (perm, h)
            riddles[(pi, h)] = found[:2] if len(found) >= 2 else found * 2
    fn('p70/r/coffers/init', ['execute store result score #p bm.rng run random value 0..5', 'execute store result score @s bm.gvc run random value 0..3',
                              'execute store result score #v bm.rng run random value 0..1'] +
       [f'summon minecraft:interaction {rel(19, 5, z)} {{Tags:["bm.gvprop","bm.gvcof","bm.gvcof{i}"],width:1.0f,height:1.0f,response:1b}}' for i, z in enumerate(CZ)] +
       [f'execute if score #p bm.rng matches {pi} if score @s bm.gvc matches {h} if score #v bm.rng matches {v} run function bm:p70/r/coffers/set_{pi}_{h}_{v}'
        for pi in range(6) for h in range(4) for v in range(2)])
    for pi, perm in enumerate(perms):
        for h in range(4):
            for v in range(2):
                lines = riddles[(pi, h)][v]
                txt = '\\n'.join(lines).replace('"', '\\"')
                fn(f'p70/r/coffers/set_{pi}_{h}_{v}', [f'summon minecraft:item_display {rel(19, 5, z)} {{Tags:["bm.gvprop","bm.gvcofd{i}"],item:{{id:"{KIND_ITEMS[k]}",count:1}},item_display:"fixed",Rotation:[90f,0f],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[0.9f,0.9f,0.9f]}}}}'
                                                       for i, (z, k) in enumerate(zip(CZ, perm))] +
                   [f'summon minecraft:text_display {rel(5, 7, 22)} {{billboard:"fixed",Rotation:[180f,0f],Tags:["bm.gvprop"],text:[{{text:"THE HONEST COFFER\\n",color:"gold",bold:true}},{{text:"{txt}\\n",color:"white"}},{{text:"(Facing the coffers. The rest bite.)",color:"dark_gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/coffers/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1'] +
       [f'execute as @e[type=minecraft:interaction,tag=bm.gvcof{i},distance=..14] if data entity @s interaction at @s run function bm:p70/r/coffers/open{i}' for i in range(4)])
    for i in range(4):
        fn(f'p70/r/coffers/open{i}', ['data remove entity @s interaction', 'scoreboard players set #pick bm.rng ' + str(i),
                                      'execute as @e[type=marker,tag=bm.gvr_coffers,distance=..14,sort=nearest,limit=1] at @s run function bm:p70/r/coffers/judge'])
    fn('p70/r/coffers/judge', ['execute if score #pick bm.rng = @s bm.gvc run return run function bm:p70/r/coffers/right',
                               'scoreboard players set #add bm.rng 12', 'function bm:p70/oops'] +
       [f'execute if score #pick bm.rng matches {i} positioned {rel(19, 5, z)} run function bm:p70/r/coffers/mimic{i}' for i, z in enumerate(CZ)])
    for i, z in enumerate(CZ):
        fn(f'p70/r/coffers/mimic{i}', [f'kill @e[type=minecraft:item_display,tag=bm.gvcofd{i},distance=..2]', f'kill @e[type=minecraft:interaction,tag=bm.gvcof{i},distance=..2]',
                                       'execute positioned ~ ~-0.5 ~ run function bm:p39/mimic/spawn_chest', 'tag @e[type=minecraft:rabbit,tag=bm.mnew,distance=..3] add bm.gvg',
                                       'scoreboard players operation @e[type=minecraft:rabbit,tag=bm.mnew,distance=..3] bm.gvi = #gi bm.rng', 'tag @e[type=minecraft:rabbit,tag=bm.mnew,distance=..3] remove bm.mnew',
                                       'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..16] ~ ~ ~ 1 0.8',
                                       'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('It bites! A Mimic!', 'red'))])
    fn('p70/r/coffers/right', ['particle minecraft:wax_on ~7 ~1 ~ 0.6 0.6 0.6 0 30', 'playsound minecraft:block.chest.open block @a[distance=..24] ~ ~ ~ 1 1',
                               'execute as @e[type=minecraft:interaction,tag=bm.gvcof,distance=..14] run kill @s', 'function bm:p70/solved'])

    # ---- THE CLOCKWORK CACHE: the strongbox pays each player once
    fn('p70/r/cache/init', [f'summon minecraft:item_display {rel(12, 5, 6)} {{Tags:["bm.gvprop"],item:{{id:"minecraft:copper_chest",count:1}},item_display:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[1.6f,1.6f,1.6f]}}}}',
                            f'summon minecraft:interaction {rel(12, 5, 6)} {{Tags:["bm.gvprop","bm.gvcbox"],width:1.6f,height:1.6f,response:1b}}',
                            f'summon minecraft:text_display {rel(12, 8, 6)} {{billboard:"vertical",Tags:["bm.gvprop"],text:[{{text:"THE CLOCKWORK CACHE\\n",color:"#d9a066",bold:true}},{{text:"One share each. Right-click the strongbox.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/cache/tick', ['execute as @e[type=minecraft:interaction,tag=bm.gvcbox,distance=..14] if data entity @s interaction at @s run function bm:p70/r/cache/click'])
    fn('p70/r/cache/click', ['tag @s add bm.gvme2', 'execute on target run function bm:p70/r/cache/pay', 'tag @s remove bm.gvme2', 'data remove entity @s interaction'])
    fn('p70/r/cache/pay', ['scoreboard players operation #q bm.rng = @s bm.gvrun', 'execute if entity @s[tag=bm.gvcached] if score @s bm.gvx = #q bm.rng run return run ' + say('You\'ve had your share.'),
                           'tag @s add bm.gvcached', 'scoreboard players operation @s bm.gvx = @s bm.gvrun', 'function bm:p70/ctx_p'] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/t{t}' for t in range(1, 6)] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/t{t}' for t in range(1, 6)] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/t{t}' for t in range(1, 6)] +
       ['loot give @s loot bm:gv/coins', 'playsound minecraft:block.chest.open player @s ~ ~ ~ 1 1.2', 'particle minecraft:wax_on ~ ~1 ~ 0.4 0.6 0.4 0 20',
        say('The Clockwork Cache: three shares, and a fistful of coins.', '#d9a066')])
    # (as a heist player) the heist's tier, night, modifiers
    fn('p70/ctx_p', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'function bm:p70/ctx'])

    # ---- THE VAULT: the guardian, the gold door, the strongbox ring, the way out
    fn('p70/r/vault/init', [modbit(2) + f' run fill {rel(1, 3, 1)} {rel(23, 3, 23)} minecraft:magma_block replace minecraft:polished_blackstone'] +
       [f'setblock {rel(x, 4, z)} minecraft:light_weighted_pressure_plate' for (x, z) in VAULT_PLATES] +
       [f'summon minecraft:item_display {rel(30, 5, 12)} {{Tags:["bm.gvprop","bm.gvsbox"],item:{{id:"minecraft:chest",count:1}},item_display:"fixed",transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.6f,0f],scale:[2f,2f,2f]}}}}',
        f'summon minecraft:text_display {rel(30, 8, 12)} {{billboard:"vertical",Tags:["bm.gvprop","bm.gvsboxt"],text:[{{text:"THE GRAND STRONGBOX\\n",color:"gold",bold:true}},{{text:"Everyone on the ring of gold plates - together.",color:"gray"}}],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.7f,0.7f,0.7f]}}}}',
        f'summon minecraft:text_display {rel(34, 6, 12)} {{billboard:"vertical",Tags:["bm.gvprop"],text:{{text:"The way out",color:"green"}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}'])
    fn('p70/r/vault/tick', ['execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..8] run function bm:p70/boss/spawn',
                            'execute if score @s bm.gvs matches 1 run function bm:p70/r/vault/fight',
                            'execute if score @s bm.gvs matches 2 run function bm:p70/r/vault/ring',
                            f'execute if score @s bm.gvs matches 2.. positioned {rel(34, 4, 12)} as @a[tag=bm.gvp,distance=..0.9] at @s run function bm:p70/leave'])
    fn('p70/r/vault/fight', ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                             'execute unless score #q bm.rng matches 0 run return 0',
                             'execute as @e[tag=bm.gvboss,distance=..40] if score @s bm.gvi = #gi bm.rng run return 0',
                             'execute if entity @e[tag=bm.gvboss,distance=..40] run return 0', 'function bm:p70/r/vault/open'])
    G.FUNCS['p70/r/vault/fight'] = [l for l in G.FUNCS['p70/r/vault/fight'] if 'if score @s bm.gvi = #gi bm.rng run return 0' not in l]
    fn('p70/r/vault/open', ['scoreboard players set @s bm.gvs 2', f'fill {rel(24, 4, 9)} {rel(24, 8, 15)} minecraft:air replace minecraft:gold_block',
                            f'particle minecraft:wax_on {rel(24, 6, 12)} 0.3 2 3 0 80', 'playsound minecraft:block.iron_door.open block @a[distance=..40] ~ ~ ~ 1 0.5',
                            'playsound minecraft:ui.toast.challenge_complete block @a[distance=..40] ~ ~ ~ 1 1',
                            'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players set @s bm.gvst 3',
                            'execute as @a[tag=bm.gvp,distance=..60] run ' + title('@s', 'title', T('The vault is open', GOLD, bold=True)),
                            'execute as @a[tag=bm.gvp,distance=..60] run ' + title('@s', 'subtitle', T('Everyone on the gold plates round the strongbox', 'gray'))])
    fn('p70/r/vault/ring', ['execute store result score #need bm.rng if entity @a[tag=bm.gvp,distance=..80,gamemode=!spectator]',
                            'execute if score #need bm.rng matches 7.. run scoreboard players set #need bm.rng 6', 'scoreboard players set #n bm.rng 0'] +
       [f'execute unless block {rel(x, 4, z)} minecraft:light_weighted_pressure_plate[power=0] run scoreboard players add #n bm.rng 1' for (x, z) in RM.RING] +
       [f'particle minecraft:wax_on {rel(x, 4, z)} 0.2 0.1 0.2 0 1' for (x, z) in RM.RING] +
       ['execute if score #n bm.rng >= #need bm.rng if score #need bm.rng matches 1.. run function bm:p70/payout'])
    # ---- the haul: everyone in the heist, each their own
    fn('p70/payout', ['scoreboard players set @s bm.gvs 3', 'function bm:p70/ctx',
                      'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p70/payout_inst',
                      'execute as @e[type=minecraft:item_display,tag=bm.gvsbox,distance=..30] run data modify entity @s item.id set value "minecraft:gold_block"',
                      'kill @e[type=minecraft:text_display,tag=bm.gvsboxt,distance=..30]',
                      f'particle minecraft:totem_of_undying {rel(30, 6, 12)} 1 1 1 0.5 120', f'particle minecraft:firework {rel(30, 7, 12)} 1 1 1 0.2 60',
                      'playsound minecraft:ui.toast.challenge_complete block @a[distance=..40] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.player.levelup block @a[distance=..40] ~ ~ ~ 1 0.6'])
    fn('p70/payout_inst', ['scoreboard players set @s bm.gvst 4', 'scoreboard players operation #gtime bm.rng = @s bm.gvtm', 'scoreboard players operation #glk bm.rng = @s bm.gvlk',
                           'scoreboard players operation #ga bm.rng = @s bm.gva', 'scoreboard players operation #grun bm.rng = @s bm.gvrun',
                           'function bm:p70/tag_mine', 'execute store result score #np bm.rng if entity @a[tag=bm.gvme]',
                           # shares: tier + 2, +1 per modifier (Greedy +2), +1 clean (alarm under 50), -2 lockdown; at least 2
                           'scoreboard players operation #sh bm.rng = #gt bm.rng', 'scoreboard players add #sh bm.rng 2'] +
       [modbit(b) + ' run scoreboard players add #sh bm.rng ' + ('2' if b == 32 else '1') for b, *_r in MODS] +
       ['execute if score #ga bm.rng matches ..49 run scoreboard players add #sh bm.rng 1', 'execute if score #glk bm.rng matches 1 run scoreboard players remove #sh bm.rng 2',
        'execute if score #sh bm.rng matches ..1 run scoreboard players set #sh bm.rng 2',
        'execute as @a[tag=bm.gvme] at @s run function bm:p70/haul', 'function bm:p70/record', 'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p70/haul', ['scoreboard players operation #i bm.rng = #sh bm.rng', 'function bm:p70/haul_roll', 'loot give @s loot bm:gv/coins'] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/coins' for t in range(2, 6)] +
       ['execute if score #gn bm.rng matches 1 run loot give @s loot bm:gv/night_blood', 'execute if score #gn bm.rng matches 2 run loot give @s loot bm:gv/night_lucky',
        'execute if score #gn bm.rng matches 3 run loot give @s loot bm:gv/night_inv',
        # first clears: a Gilded piece (V: the Scepter) and a better Raid Banner; the next tier unlocks
        'scoreboard players operation #c bm.rng = @s bm.gvcl'] +
       sum(([f'execute if score #gt bm.rng matches {t} run scoreboard players set #bit bm.rng {2 ** t}'] for t in range(1, 6)), []) +
       ['scoreboard players operation #q bm.rng = #c bm.rng', 'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
        'execute if score #q bm.rng matches 0 run function bm:p70/first_clear',
        'execute if score #gt bm.rng >= @s bm.gvu run scoreboard players operation @s bm.gvu = #gt bm.rng',
        'execute if score #gt bm.rng >= @s bm.gvu if score @s bm.gvu matches ..4 run scoreboard players add @s bm.gvu 1',
        # a Shifting Core, very rarely (tiers III-V)
        'execute store result score #r bm.rng run random value 1..1000'] +
       [f'execute if score #gt bm.rng matches {t} if score #r bm.rng matches ..{pm} run function bm:p70/core' for t, pm in CORE_CHANCE.items()] +
       # a Bond Sigil for each of a party of two or more, bound to this heist
       ['execute if score #np bm.rng matches 2.. run function bm:p70/bond',
        tellraw('@s', P + [T('Your haul: ', GOLD, bold=True), {'score': {'name': '#sh', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}, T(' shares', 'gray'),
                           T(' (tier, modifiers, a clean getaway).', 'dark_gray')]),
        'execute if score #glk bm.rng matches 1 run ' + tellraw('@s', P + [T('Lockdown cost you two shares.', 'red')])])
    fn('p70/haul_roll', [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:gv/t{t}' for t in range(1, 6)] +
       ['scoreboard players remove #i bm.rng 1', 'execute if score #i bm.rng matches 1.. run function bm:p70/haul_roll'])
    fn('p70/first_clear', ['scoreboard players operation @s bm.gvcl += #bit bm.rng'] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:items/{iid}' for t, iid in FIRST_CLEAR.items()] +
       [f'execute if score #gt bm.rng matches {t} run loot give @s loot bm:items/raid_banner_{t}' for t in range(1, 6)] +
       [tellraw('@s', P + [T('First clear of this tier! ', GOLD, bold=True), T('A Gilded prize and a finer Raid Banner. The next tier is open to you.', 'gray')]),
        'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2'])
    fn('p70/core', ['loot give @s loot bm:items/shift_core', tellraw('@a', P + [{'selector': '@s', 'color': 'white'}, T(' found a ', 'gray'), T('Shifting Core', '#e0c0ff', bold=True),
                                                                              T(' in the Gilded Gutter Vault!', 'gray')]),
                    'playsound minecraft:ui.toast.challenge_complete player @a ~ ~ ~ 0.6 0.6'])
    fn('p70/bond', [f'summon minecraft:item ~ ~0.5 ~ {snbt({"Item": G.stack("bond_sigil"), "PickupDelay": Int(0), "Tags": ["bm.gvbond"]})}',
                    'execute store result entity @e[type=minecraft:item,tag=bm.gvbond,distance=..2,limit=1] Item.components."minecraft:custom_data".bond int 1 run scoreboard players get #grun bm.rng',
                    'tag @e[type=minecraft:item,tag=bm.gvbond,distance=..2] remove bm.gvbond'])
    # ---- the records: this week's fastest clear of each tier
    fn('p70/rec_week', ['scoreboard players operation #wk bm.rng = #day bm.bm', 'scoreboard players operation #wk bm.rng /= #7 bm.rng'] +
       sum(([f'execute unless score #wk{t} bm.gvrec = #wk bm.rng run data remove storage bm:gv rec.t{t}',
             f'execute unless score #wk{t} bm.gvrec = #wk bm.rng run scoreboard players reset #best{t} bm.gvrec',
             f'scoreboard players operation #wk{t} bm.gvrec = #wk bm.rng'] for t in range(1, 6)), []))
    rec_disp = snbt({'Tags': ['bm.gvrecd'], 'item': {'id': 'minecraft:paper', 'count': Int(1)}})
    fn('p70/record', ['function bm:p70/rec_week'] +
       [f'execute if score #gt bm.rng matches {t} run function bm:p70/rec{t}' for t in range(1, 6)])
    for t in range(1, 6):
        fn(f'p70/rec{t}', [f'execute if score #best{t} bm.gvrec matches 1.. if score #gtime bm.rng >= #best{t} bm.gvrec run return 0',
                           f'scoreboard players operation #best{t} bm.gvrec = #gtime bm.rng',
                           'scoreboard players operation #mm bm.rng = #gtime bm.rng', 'scoreboard players operation #mm bm.rng /= #1200 bm.rng',
                           'scoreboard players operation #ss bm.rng = #gtime bm.rng', 'scoreboard players operation #ss bm.rng /= #20 bm.rng', 'scoreboard players operation #ss bm.rng %= #60 bm.rng',
                           f'summon minecraft:item_display ~ ~ ~ {rec_disp}',
                           f'execute if score #ss bm.rng matches 10.. run item modify entity @e[type=minecraft:item_display,tag=bm.gvrecd,limit=1,sort=nearest] contents {snbt(rec_name(t, False))}',
                           f'execute if score #ss bm.rng matches ..9 run item modify entity @e[type=minecraft:item_display,tag=bm.gvrecd,limit=1,sort=nearest] contents {snbt(rec_name(t, True))}',
                           f'data modify storage bm:gv rec.t{t} set from entity @e[type=minecraft:item_display,tag=bm.gvrecd,limit=1,sort=nearest] item.components."minecraft:custom_name"',
                           'kill @e[type=minecraft:item_display,tag=bm.gvrecd]',
                           'execute as @a[tag=bm.gvme] run function bm:p70/laurel',
                           'execute as @e[type=marker,tag=bm.gvr_lobby] at @s run function bm:p70/board'])
    fn('p70/laurel', ['loot give @s loot bm:items/gutter_laurel', tellraw('@s', P + [T('A new record for the week! ', GOLD, bold=True), T('The Gutter Laurel is yours.', 'gray')])])

    # ------------------------------------------------------------------ the guardian
    for n, (nm, col, bcol) in BOSS.items():
        boss = {'Tags': ['bm.gvboss', 'bm.gvbnew', 'bm.tiered', 'bm.seen'], 'PersistenceRequired': B(1), 'CustomName': T(nm, col, bold=True),
                'CustomNameVisible': B(1), 'DeathLootTable': 'bm:gv/boss',
                'attributes': [{'id': 'minecraft:scale', 'base': D(1.6)}, {'id': 'minecraft:armor', 'base': D(10)}, {'id': 'minecraft:knockback_resistance', 'base': D(0.0)},     # (2.64: it can be knocked back - 0.8 + netherite made it unmovable)
                               {'id': 'minecraft:follow_range', 'base': D(40)}],
                'drop_chances': {'head': F(0), 'chest': F(0), 'legs': F(0), 'feet': F(0), 'mainhand': F(0), 'offhand': F(0)},
                'equipment': {'head': {'id': 'minecraft:golden_helmet' if n != 1 else 'minecraft:netherite_helmet', 'count': Int(1)},
                              'chest': {'id': 'minecraft:golden_chestplate' if n != 1 else 'minecraft:netherite_chestplate', 'count': Int(1)},
                              'legs': {'id': 'minecraft:golden_leggings', 'count': Int(1)}, 'feet': {'id': 'minecraft:golden_boots', 'count': Int(1)},
                              'mainhand': {'id': 'minecraft:golden_axe', 'count': Int(1), 'components': {'minecraft:enchantment_glint_override': True}}}}
        fn(f'p70/boss/summon{n}', [f'summon minecraft:vindicator ~ ~ ~ {snbt(boss)}'] +
           [f'execute if score #gi bm.rng matches {s + 1} run tag @e[tag=bm.gvbnew,limit=1] add bm.gvboss{s}' for s in range(SLOTS)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} name {snbt(T(nm, col, bold=True))}' for s in range(SLOTS)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} color {bcol}' for s in range(SLOTS)])
    fn('p70/boss/spawn', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'function bm:p70/ctx'] +
       [f'execute if score #gn bm.rng matches {n} run function bm:p70/boss/summon{n}' for n in BOSS] +
       ['execute as @e[tag=bm.gvbnew,limit=1] run function bm:p70/boss/setup', 'tag @e[tag=bm.gvbnew] remove bm.gvbnew',
        'particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1', 'playsound minecraft:entity.ravager.roar hostile @a[distance=..40] ~ ~ ~ 1 0.7',
        'execute as @a[tag=bm.gvp,distance=..40] run ' + title('@s', 'title', T('The vault\'s guardian wakes', GOLD, bold=True))])
    fn('p70/boss/setup', ['scoreboard players operation @s bm.gvi = #gi bm.rng', 'scoreboard players operation @s bm.gvnt = #gn bm.rng',
                          'scoreboard players operation #h bm.rng = #gt bm.rng', 'scoreboard players set #q bm.rng 90', 'scoreboard players operation #h bm.rng *= #q bm.rng',
                          'scoreboard players add #h bm.rng 160',
                          modbit(8) + ' run scoreboard players operation #h bm.rng *= #3 bm.rng', modbit(8) + ' run scoreboard players operation #h bm.rng /= #2 bm.rng',
                          'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                          'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng',
                          'scoreboard players operation #d bm.rng = #gt bm.rng', 'scoreboard players operation #d bm.rng *= #2 bm.rng', 'scoreboard players add #d bm.rng 8',
                          'execute store result storage bm:gv d double 1 run scoreboard players get #d bm.rng', 'function bm:p70/dmg with storage bm:gv',
                          'scoreboard players set @s bm.gvc 0', 'scoreboard players set @s bm.gvw 0'] +
       [f'execute if score #gi bm.rng matches {s + 1} store result bossbar bm:gvb{s} max run scoreboard players get #h bm.rng' for s in range(SLOTS)] +
       [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} players @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]' for s in range(SLOTS)])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3']
    fn('p70/dmg', ['$attribute @s minecraft:attack_damage base set $(d)'])
    second.append('execute as @e[type=minecraft:vindicator,tag=bm.gvboss] at @s run function bm:p70/boss/sec')
    fn('p70/boss/sec', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players operation #gn bm.rng = @s bm.gvnt'] +
       [f'execute if score @s bm.gvi matches {s + 1} store result bossbar bm:gvb{s} value run data get entity @s Health' for s in range(SLOTS)] +
       ['execute store result score #hp bm.rng run data get entity @s Health', 'execute store result score #mx bm.rng run attribute @s minecraft:max_health get',
        'scoreboard players operation #half bm.rng = #mx bm.rng', 'scoreboard players operation #half bm.rng /= #2 bm.rng',
        'scoreboard players operation #qtr bm.rng = #mx bm.rng', 'scoreboard players operation #qtr bm.rng /= #2 bm.rng',
        'scoreboard players operation #qtr bm.rng /= #2 bm.rng',
        'execute if score @s bm.gvc matches 0 if score #hp bm.rng <= #half bm.rng run function bm:p70/boss/shell',
        'execute if score @s bm.gvc matches 2 if score #hp bm.rng <= #qtr bm.rng run function bm:p70/boss/shell',
        'execute if entity @s[tag=bm.gvshell] run function bm:p70/boss/shell_tick',
        'execute if entity @s[tag=bm.gvshell] run return 0',
        'scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw matches 5.. run function bm:p70/boss/ability',
        # night touches: the Treasurer's blood aura, the Gambler's dropped gold, the Vault-Breaker's green glow
        'execute if score #gn bm.rng matches 1 run effect give @a[tag=bm.gvp,distance=..4] minecraft:wither 2 0',
        'execute if score #gn bm.rng matches 1 if entity @a[tag=bm.gvp,distance=..4] run effect give @s minecraft:instant_damage 1 0 true',
        'execute if score #gn bm.rng matches 1 run particle minecraft:dust{color:[0.7,0.0,0.0],scale:1.6} ~ ~1.5 ~ 1.5 1 1.5 0 20',
        'execute if score #gn bm.rng matches 2 run particle minecraft:wax_on ~ ~2 ~ 0.8 1 0.8 0 10',
        'execute if score #gn bm.rng matches 3 run particle minecraft:dust{color:[0.5,1.0,0.3],scale:1.4} ~ ~1.5 ~ 1 1 1 0 16'])
    G.FUNCS['p70/boss/sec'] = [l for l in G.FUNCS['p70/boss/sec'] if 'instant_damage' not in l] + \
        ['execute if score #gn bm.rng matches 1 if entity @a[tag=bm.gvp,distance=..4] run effect give @s minecraft:regeneration 2 1 true']
    fn('p70/boss/ability', ['scoreboard players set @s bm.gvw 0', 'execute store result score #r bm.rng run random value 1..3',
                            'execute if score #r bm.rng matches 1 run function bm:p70/boss/barrage', 'execute if score #r bm.rng matches 2 run function bm:p70/boss/slam',
                            'execute if score #r bm.rng matches 3 run function bm:p70/boss/call',
                            'execute if score #gn bm.rng matches 2 run function bm:p70/boss/barrage', 'execute if score #gn bm.rng matches 3 run function bm:p70/boss/laser'])
    fn('p70/boss/barrage', ['tag @s add bm.gvbme', 'execute as @a[tag=bm.gvp,distance=..16,limit=4,sort=nearest] at @s run function bm:p70/boss/coin',
                            'tag @s remove bm.gvbme', 'playsound minecraft:entity.experience_orb.pickup hostile @a[distance=..24] ~ ~ ~ 1 0.5',
                            'execute if score #gn bm.rng matches 2 run summon minecraft:item ~ ~1 ~ {Item:{id:"minecraft:gold_nugget",count:3},Motion:[0.0,0.3,0.0]}'])
    fn('p70/boss/coin', ['damage @s 5 minecraft:magic by @e[tag=bm.gvbme,limit=1]',
                         'execute facing entity @e[tag=bm.gvbme,limit=1] eyes run function bm:p70/boss/coin_beam', 'particle minecraft:wax_on ~ ~1 ~ 0.3 0.3 0.3 0 8'])
    fn('p70/boss/coin_beam', [f'particle minecraft:dust{{color:[1.0,0.8,0.2],scale:1}} ^ ^1.2 ^{d / 2} 0 0 0 0 1' for d in range(1, 24)])
    fn('p70/boss/slam', ['particle minecraft:explosion ~ ~0.3 ~ 2 0.1 2 0 10', 'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~0.3 ~ 3 0.2 3 0 60',
                         'playsound minecraft:entity.generic.explode hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                         'execute as @a[tag=bm.gvp,distance=..5] run damage @s 7 minecraft:mob_attack by @e[tag=bm.gvboss,limit=1,sort=nearest]',
                         'effect give @a[tag=bm.gvp,distance=..5] minecraft:levitation 1 4 true', 'effect give @a[tag=bm.gvp,distance=..5] minecraft:slowness 2 1'])
    fn('p70/boss/call', ['execute store result score #ng bm.rng if entity @e[tag=bm.gvg,distance=..30]', 'execute if score #ng bm.rng matches 6.. run return run function bm:p70/boss/barrage',
                         'function bm:p70/ctx', 'execute positioned ^3 ^ ^ run function bm:p70/guard', 'execute positioned ^-3 ^ ^ run function bm:p70/guard',
                         'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..24] ~ ~ ~ 1 0.8'])
    fn('p70/boss/laser', ['tag @s add bm.gvbme', 'execute as @a[tag=bm.gvp,distance=..20,sort=random,limit=1] at @s run function bm:p70/boss/zap', 'tag @s remove bm.gvbme'])
    fn('p70/boss/zap', ['damage @s 6 minecraft:magic by @e[tag=bm.gvbme,limit=1]', 'execute facing entity @e[tag=bm.gvbme,limit=1] eyes run function bm:p70/boss/zap_beam',
                        'playsound minecraft:entity.guardian.attack hostile @a[distance=..24] ~ ~ ~ 1 1.4'])
    fn('p70/boss/zap_beam', [f'particle minecraft:dust{{color:[0.5,1.0,0.3],scale:1.2}} ^ ^1.2 ^{d / 2} 0 0 0 0 1' for d in range(1, 30)])
    # the gilded shell: invulnerable until the hall's four plates are pressed at once (or 12 seconds pass)
    fn('p70/boss/shell', ['scoreboard players add @s bm.gvc 1', 'tag @s add bm.gvshell', 'scoreboard players set @s bm.gvx 12', 'effect give @s minecraft:resistance 13 4 true',
                          'data merge entity @s {Glowing:1b}', 'playsound minecraft:block.anvil.use hostile @a[distance=..30] ~ ~ ~ 1 0.5',
                          'execute as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', [T('It shells itself in gold! ', GOLD, bold=True), T('Press the hall\'s four plates at once to crack it.', 'gray')])])
    fn('p70/boss/shell_tick', ['scoreboard players remove @s bm.gvx 1', 'particle minecraft:wax_on ~ ~1.5 ~ 0.8 1.2 0.8 0 20', 'scoreboard players set #n bm.rng 0',
                               'execute as @e[type=marker,tag=bm.gvr_vault,distance=..40,sort=nearest,limit=1] at @s run function bm:p70/boss/count_plates',
                               'execute if score #n bm.rng matches 4.. run function bm:p70/boss/crack', 'execute if score @s bm.gvx matches ..0 run function bm:p70/boss/unshell'])
    fn('p70/boss/count_plates', [f'execute unless block {rel(x, 4, z)} minecraft:light_weighted_pressure_plate[power=0] run scoreboard players add #n bm.rng 1' for (x, z) in VAULT_PLATES] +
       [f'particle minecraft:wax_on {rel(x, 4, z)} 0.3 0.1 0.3 0 3' for (x, z) in VAULT_PLATES])
    fn('p70/boss/crack', ['function bm:p70/boss/unshell', 'damage @s 20 minecraft:magic', 'effect give @s minecraft:slowness 4 3', 'effect give @s minecraft:weakness 4 2',
                          'particle minecraft:block{block_state:"minecraft:gold_block"} ~ ~1.5 ~ 1 1 1 0 80', 'playsound minecraft:block.glass.break hostile @a[distance=..30] ~ ~ ~ 1 0.5',
                          'execute as @a[tag=bm.gvp,distance=..30] run ' + title('@s', 'actionbar', T('The shell cracks! It reels!', GOLD))])
    fn('p70/boss/unshell', ['tag @s remove bm.gvshell', 'scoreboard players add @s bm.gvc 1', 'effect clear @s minecraft:resistance', 'data merge entity @s {Glowing:0b}'])
    # (the boss bar shows only to its heist; the guardian is a boss for every purpose - scaling, never pushed)

    # ------------------------------------------------------------------ Glass Cannon: half health, more bite (for the heist's players only)
    fn('p70/glass_check', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #glass bm.rng 0',
                           'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run scoreboard players operation #gm bm.rng = @s bm.gvmod',
                           'execute as @e[type=marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng if function bm:p70/mod16 run scoreboard players set #glass bm.rng 1',
                           'execute if score #glass bm.rng matches 1 run attribute @s minecraft:max_health modifier add bm:gv_glass -0.5 add_multiplied_total',
                           'execute if score #glass bm.rng matches 1 run effect give @s minecraft:strength 5 1 true',
                           'execute if score #glass bm.rng matches 0 run attribute @s minecraft:max_health modifier remove bm:gv_glass'])
    second.append('execute as @a[tag=bm.gvp] run function bm:p70/glass_check')
    second.append('execute as @a[tag=!bm.gvp] run attribute @s minecraft:max_health modifier remove bm:gv_glass')
    for s in range(SLOTS):
        G.FUNCS[f'p70/s{s}/enter'].append('function bm:p70/glass_check')

    # ------------------------------------------------------------------ loot tables
    from gen_dp import loot_entry, uni
    def L(*entries):
        return {'pools': [{'rolls': 1, 'entries': [dict(loot_entry(i, c), weight=w) if i in ITEMS else {'type': 'minecraft:item', 'name': i, 'weight': w,
                                                                                                         'functions': [{'function': 'minecraft:set_count', 'count': c}] if c else []}
                                                   for i, w, c in entries]}]}
    # (2.67) no Tokens, Medallions or BM Trophies here - they come only from the Fixer's capped prize (phase75 p75/prize)
    tiers = {
        1: [('gutter_coin', 40, uni(2, 4)), ('minecraft:gold_ingot', 34, uni(3, 8)), ('minecraft:emerald', 26, uni(2, 6)), ('clockwork_fragment', 8, None),
            ('heisters_shiv', 4, None), ('smoke_bomb', 10, uni(1, 2)), ('skeleton_lockpick', 5, None), ('smugglers_boots', 2, None)],
        2: [('gutter_coin', 40, uni(3, 6)), ('minecraft:gold_block', 22, uni(1, 3)), ('minecraft:diamond', 18, uni(1, 3)), ('clockwork_fragment', 10, None),
            ('heisters_shiv', 4, None), ('vault_breaker', 3, None), ('thiefs_cowl', 3, None), ('smugglers_boots', 3, None), ('smoke_bomb', 10, uni(1, 2)),
            ('skeleton_lockpick', 6, None), ('minecraft:emerald', 10, uni(3, 7))],
        3: [('gutter_coin', 40, uni(4, 8)), ('minecraft:diamond', 22, uni(2, 4)), ('clockwork_fragment', 10, None), ('vault_breaker', 4, None), ('coinslinger', 4, None),
            ('thiefs_cowl', 4, None), ('cipher_monocle', 3, None), ('gilded_staff_topper', 2, None), ('golden_spear', 2, None), ('frog_monocle', 2, None),
            ('skeleton_lockpick', 6, None), ('minecraft:gold_block', 12, uni(2, 4))],
        4: [('gutter_coin', 40, uni(6, 10)), ('minecraft:diamond_block', 12, uni(1, 2)), ('minecraft:gold_block', 12, uni(2, 4)), ('clockwork_fragment', 10, None),
            ('coinslinger', 5, None), ('gutter_cutlass', 5, None), ('cipher_monocle', 4, None), ('gilded_staff_topper', 3, None), ('golden_spear', 3, None),
            ('frog_monocle', 3, None), ('minecraft:diamond', 8, uni(2, 4))],
        5: [('gutter_coin', 40, uni(8, 14)), ('minecraft:netherite_ingot', 10, uni(1, 2)), ('clockwork_fragment', 8, None), ('gutter_cutlass', 6, None),
            ('treasurers_scepter', 2, None), ('vault_hound_whistle', 2, None), ('cipher_monocle', 4, None), ('gilded_staff_topper', 4, None), ('golden_spear', 4, None),
            ('frog_monocle', 4, None), ('minecraft:diamond_block', 6, None)],
    }
    for t, ents in tiers.items():
        wjson(f'bm/loot_table/gv/t{t}.json', L(*ents))
    wjson('bm/loot_table/gv/coins.json', L(('gutter_coin', 1, uni(4, 8))))
    wjson('bm/loot_table/gv/guard.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry('gutter_coin', uni(0, 2)))]},
                                                    {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_nugget', 'functions': [{'function': 'minecraft:set_count', 'count': uni(1, 4)}]}]}]})
    wjson('bm/loot_table/gv/boss.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry('gutter_coin', uni(6, 12)))]},
                                                   {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:gold_block', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 5)}]}]}]})
    wjson('bm/loot_table/gv/night_blood.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry('blood_crystal', uni(3, 8)))]},
                                                          {'rolls': 1, 'entries': [dict(loot_entry('crimson_ledger', None), weight=1), {'type': 'minecraft:empty', 'weight': 3}]}]})
    wjson('bm/loot_table/gv/night_lucky.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry('lucky_token', uni(3, 8)))]},
                                                          {'rolls': 1, 'entries': [dict(loot_entry('gutter_coin', uni(4, 10)))]},
                                                          {'rolls': 1, 'entries': [dict(loot_entry('gamblers_coin', None), weight=1), {'type': 'minecraft:empty', 'weight': 3}]}]})
    wjson('bm/loot_table/gv/night_inv.json', {'pools': [{'rolls': 1, 'entries': [dict(loot_entry('xenite_green', uni(3, 8)))]},
                                                        {'rolls': 1, 'entries': [dict(loot_entry('power_cell', uni(1, 3)))]},
                                                        {'rolls': 1, 'entries': [dict(loot_entry('vorn_cracking_rig', None), weight=1), {'type': 'minecraft:empty', 'weight': 3}]}]})

    # ------------------------------------------------------------------ Goldtooth, the den's fence (Gutter Coins only)
    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


def rec_name(t, pad):
    from items import T
    return {'function': 'minecraft:set_name', 'target': 'custom_name', 'entity': 'this',
            'name': [{'text': f'Tier {TIER_NAME[t]}: ', 'color': GOLD}, {'score': {'name': '#mm', 'objective': 'bm.rng'}, 'color': 'white'},
                     {'text': ':0' if pad else ':', 'color': 'white'}, {'score': {'name': '#ss', 'objective': 'bm.rng'}, 'color': 'white'},
                     {'text': '  ', 'color': 'gray'}, {'selector': '@a[tag=bm.gvme]', 'color': 'gray'}]}


GOLDTOOTH_STOCK = [   # (price in Gutter Coins, item, count)
    (6, 'smoke_bomb', 2), (10, 'skeleton_lockpick', 1), (14, 'clockwork_fragment', 1), (30, 'thiefs_cowl', 1), (30, 'smugglers_boots', 1),
    (45, 'cipher_monocle', 1), (55, 'gilded_staff_topper', 1), (55, 'golden_spear', 1), (40, 'frog_monocle', 1), (64, 'vault_hound_whistle', 1),
]


def goldtooth():
    from gen_dp import offer
    from items import T
    recipes = [offer(('gutter_coin', min(price, 64)), (iid, n), ('gutter_coin', 64) if iid == 'vault_hound_whistle' else None) for price, iid, n in GOLDTOOTH_STOCK]
    return {'Tags': ['bm.gvgt', 'bm.npc', 'bm.gvprop'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T('Goldtooth', GOLD, bold=True), 'CustomNameVisible': B(1),
            'VillagerData': {'type': 'minecraft:desert', 'profession': 'minecraft:cartographer', 'level': Int(5)},
            'Offers': {'Recipes': recipes}}
