"""2.70: THRONE ROOMS and PRIME FIGHTS.

THRONE ROOMS (any tier, rare)   once a heist the Fixer's crew may stumble on a king's hoard: a throne on a dais, piles of
                                treasure, and the Royal Coffer in front of it. Open the coffer and every raider's haul
                                takes a king's share; coins go into the pot, and the way on opens.
                                  THE GOLD THRONE       1 heist in 50    gold, golden apples (a rare enchanted one)
                                  THE DIAMOND THRONE    1 in 100         diamonds, emeralds, a diamond block now and then
                                  THE NETHERITE THRONE  1 in 150         a netherite ingot, scrap, an upgrade template, diamonds
PRIME FIGHTS (uncommon)         about one fight room in eight is PRIME: a red banner over the door, and every guard in it is
                                stronger (more health, harder hits, quicker, armoured, its name marked Prime). Beat it and
                                the pot takes extra coins and every raider's haul a better find.
"""
from items import T
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase75 as P75
import phase76_rooms as R6
import phase110 as P110
import phase112 as P112

GOLD = '#ffcf40'
PRIME = '#ff4a4a'
rel, relf = RM.rel, P110.relf
FY = RM.FY

# ===================================================================== THE THRONE ROOM
# (the hoard is built of stand-in blocks no tier theme touches; the room's setup swaps them for gold, diamond or netherite)
HOARD, HOARD2, RUG = 'minecraft:sponge', 'minecraft:wet_sponge', 'minecraft:moss_carpet'
THRONES = {   # var: (name, colour, hoard block, raw pile, rug, the coffer's coins, the item on the piles)
    1: ('THE GOLD THRONE', '#ffcf40', 'minecraft:gold_block', 'minecraft:raw_gold_block', 'minecraft:red_carpet', 20, 'minecraft:gold_ingot'),
    2: ('THE DIAMOND THRONE', '#6af0ff', 'minecraft:diamond_block', 'minecraft:deepslate_diamond_ore', 'minecraft:light_blue_carpet', 35, 'minecraft:diamond'),
    3: ('THE NETHERITE THRONE', '#b48cff', 'minecraft:netherite_block', 'minecraft:ancient_debris', 'minecraft:black_carpet', 50, 'minecraft:netherite_ingot')}
ODDS = {3: (1, 2), 2: (3, 5), 1: (6, 11)}       # out of 300: netherite 2 (1 in 150), diamond 3 (1 in 100), gold 6 (1 in 50)
COFFER = (12, 4, 7)
PILES = [(3, 2), (19, 2), (3, 19), (19, 19)]     # 3x3 piles (south-west corner of each)


def throne():
    b = R6.shell()
    for x in range(8, 17):                          # the dais (one step up) and its step
        for z in range(1, 4): b.set(x, 4, z, 'minecraft:smooth_quartz')
        b.set(x, 4, 4, 'minecraft:smooth_quartz_slab[type=bottom]')
    b.set(12, 5, 2, 'minecraft:quartz_stairs[facing=north]')         # the seat, its back and arms of the hoard's metal
    for y in range(5, 9): b.set(12, y, 1, HOARD)
    for x in (11, 13):
        b.set(x, 5, 2, HOARD); b.set(x, 6, 1, HOARD)
    b.set(12, 9, 1, 'minecraft:end_rod[facing=up]')
    for x in (9, 15):                               # braziers on the dais
        b.set(x, 5, 2, 'minecraft:soul_campfire[lit=true,signal_fire=false,waterlogged=false,facing=south]')
    for x in range(1, 24): b.set(x, 4, 12, RUG)     # the runner, door to door, and up to the throne
    for z in range(5, 12): b.set(12, 4, z, RUG)
    for (x0, z0) in PILES:                          # the hoard piles
        for dx in range(3):
            for dz in range(3):
                b.set(x0 + dx, 4, z0 + dz, HOARD2 if (dx + dz) % 2 else HOARD)
        b.set(x0 + 1, 5, z0 + 1, HOARD)
        for (dx, dz) in ((0, 1), (2, 1), (1, 0), (1, 2)): b.set(x0 + dx, 5, z0 + dz, RUG)
    b.set(*COFFER, 'minecraft:vault[facing=south]')
    R6.ctrl(b, 'throne')
    return P112.wall_glow(b)


P75.EXTRA_ROOMS['throne'] = throne
R6.NAMES['throne'] = 'The Throne Room'
PRIME_KINDS = ['guards', 'ambush', 'pit', 'isles']
PRIME_IN = 8                                        # one fight room in 8


def generate(G):
    fn, title, tellraw, wjson = G.fn, G.title, G.tellraw, G.wjson
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    from gen_dp import loot_entry, uni
    from items import ITEMS
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..30]'
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    def big(t_, sub, col, who=crew):
        return [f'title {who} times 5 50 15', title(who, 'title', T(t_, col, bold=True)), title(who, 'subtitle', T(sub, 'gray'))]
    my_crew = '@a[tag=bm.gvp,distance=..40]'

    # ================================================================== THRONE ROOMS: the draw (once a heist), the place (room 2-4)
    G.FUNCS['p75/lay/rooms'][0:0] = ['function bm:p113/throne/roll']
    fn('p113/throne/roll', ['scoreboard players set #thr bm.rng 0',
                            'execute if score #fth bm.gvv matches 1..3 run scoreboard players operation #thr bm.rng = #fth bm.gvv',
                            'execute if score #fth bm.gvv matches 1..3 run scoreboard players set #fth bm.gvv 0',
                            'execute if score #thr bm.rng matches 0 if score #frk bm.gvv matches 1.. run return 0',
                            'execute if score #thr bm.rng matches 0 store result score #r bm.rng run random value 1..300'] +
       [f'execute if score #thr bm.rng matches 0 if score #r bm.rng matches {a}..{b_} run scoreboard players set #thr bm.rng {v}' for v, (a, b_) in ODDS.items()] +
       ['execute store result score #thq bm.rng run random value 2..4',
        'execute if score #thq bm.rng > #gk bm.rng run scoreboard players operation #thq bm.rng = #gk bm.rng'])
    k = next(i for i, l in enumerate(G.FUNCS['p75/lay/room']) if l == 'scoreboard players add #q bm.rng 1')
    G.FUNCS['p75/lay/room'].insert(k + 1, 'execute if score #thr bm.rng matches 1.. if score #q bm.rng = #thq bm.rng run return run function bm:p113/throne/lay')
    fn('p113/throne/lay', ['function bm:p75/pc/throne',
                           'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvnew,tag=bm.gvr_throne] bm.gvvar = #thr bm.rng',
                           'execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim', 'scoreboard players set #thr bm.rng 0'])
    for v, (nm, *_r) in THRONES.items():
        key = nm.split()[1].lower()
        fn(f'admin/throne_{key}', [f'scoreboard players set #fth bm.gvv {v}', tellraw('@s', P + [T(f'The next heist laid has {nm.title()} in it (once).', 'gray')])])

    # ================================================================== THRONE ROOMS: setup, the coffer, the hoard
    G.FUNCS['p70/r/init'] += ['execute if entity @s[tag=bm.gvr_throne] run return run function bm:p113/throne/init']
    G.FUNCS['p70/r/tick'] += ['execute if entity @s[tag=bm.gvr_throne] run return run function bm:p113/throne/tick']
    k = next(i for i, l in enumerate(G.FUNCS['p76/first_visit']) if 'bm.gvr_rest' in l)
    G.FUNCS['p76/first_visit'].insert(k + 1, 'execute if entity @s[tag=bm.gvr_throne] run return 0')
    box = f'{rel(0, 4, 0)} {rel(24, 10, 24)}'
    init = ['scoreboard players set @s bm.gvs 0', 'execute unless score @s bm.gvvar matches 1..3 run scoreboard players set @s bm.gvvar 1']
    for v, (nm, col, hb, raw, rug, coins, it) in THRONES.items():
        c = f'execute if score @s bm.gvvar matches {v} run '
        init += [c + f'fill {box} {hb} replace {HOARD}', c + f'fill {box} {raw} replace {HOARD2}', c + f'fill {box} {rug} replace {RUG}',
                 c + sign(relf(12.5, 6.6, 6.2), nm, 'Open the Royal Coffer: a king\'s share for every raider\'s haul.', 0.6, col=col)]
        for (x0, z0) in PILES:
            for (dx, dz, ry) in ((0.5, 0.6, 20), (2.4, 2.3, 110), (2.5, 0.4, 250)):
                init.append(c + f'summon minecraft:item_display {relf(x0 + dx, 5.03, z0 + dz)} ' +
                            snbt({'Tags': ['bm.gvprop'], 'item': {'id': it, 'count': Int(1)}, 'item_display': 'fixed', 'brightness': {'block': 15, 'sky': 15},
                                  'Rotation': [F(ry), F(0)],
                                  'transformation': {'left_rotation': [F(-0.7071), F(0), F(0), F(0.7071)], 'right_rotation': P110.IDENT,
                                                     'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}}))
    init += [f'summon minecraft:interaction {relf(COFFER[0] + 0.5, COFFER[1], COFFER[2] + 0.5)} {{Tags:["bm.gvprop","bm.gvthc"],width:1.1f,height:1.1f,response:1b}}']
    fn('p113/throne/init', init)
    fn('p113/throne/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                            'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..13] run function bm:p113/throne/enter',
                            f'execute positioned {relf(COFFER[0] + 0.5, COFFER[1], COFFER[2] + 0.5)} as @e[type=minecraft:interaction,tag=bm.gvthc,distance=..1] if data entity @s interaction at @s run function bm:p113/throne/click',
                            f'execute if score @s bm.gvs matches 1 run particle minecraft:wax_on {relf(12.5, 6, 2.5)} 0.6 0.8 0.3 0 1'])
    enter = ['scoreboard players set @s bm.gvs 1']
    for v, (nm, col, *_r) in THRONES.items():
        enter += [f'execute if score @s bm.gvvar matches {v} run {l}' for l in big(nm, 'A king\'s hoard, and no king to guard it...', col)]
    enter += [f'execute as {crew} at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.8']
    fn('p113/throne/enter', enter)
    fn('p113/throne/click', ['data remove entity @s interaction',
                             'execute as @e[type=minecraft:marker,tag=bm.gvr_throne,distance=..12,sort=nearest,limit=1] if score @s bm.gvs matches ..2 at @s run function bm:p113/throne/claim'])
    claim = ['kill @e[type=minecraft:interaction,tag=bm.gvthc,distance=..12]']
    for v, (nm, col, hb, raw, rug, coins, it) in THRONES.items():
        c = f'execute if score @s bm.gvvar matches {v} run '
        key = nm.split()[1].lower()
        claim += [c + f'scoreboard players set #c bm.rng {coins}',
                  c + f'execute as {my_crew} if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/find {{t:"bm:p113/throne_{key}"}}',
                  c + f'particle minecraft:block{{block_state:"{hb}"}} {relf(COFFER[0] + 0.5, 5, COFFER[2] + 0.5)} 0.6 0.6 0.6 0 60']
        claim += [c + l for l in big(nm.replace('THE ', '').replace(' THRONE', '') + ' FOR EVERYONE', 'A king\'s share in every haul - and coins in the pot', col)]
    claim += [inst('bm:p75/pot_add'),
              f'execute as {crew} at @s run playsound minecraft:block.vault.open_shutter block @s ~ ~ ~ 1 0.8',
              f'execute as {crew} at @s run playsound minecraft:entity.player.levelup player @s ~ ~ ~ 1 0.9',
              f'setblock {rel(*COFFER)} minecraft:vault[facing=south,vault_state=ejecting]',
              'function bm:p70/solved']
    fn('p113/throne/claim', claim)

    def pool(*entries, rolls=1):
        return {'rolls': rolls, 'entries': [dict(loot_entry(i, c), weight=w) if i in ITEMS else
                                            {'type': 'minecraft:item', 'name': f'minecraft:{i}', 'weight': w,
                                             'functions': [{'function': 'minecraft:set_count', 'count': c}] if c else []} for i, w, c in entries]}
    def maybe(i, chance, c=None):
        p = pool((i, 1, c)); p['conditions'] = [{'condition': 'minecraft:random_chance', 'chance': chance}]; return p
    wjson('bm/loot_table/p113/throne_gold.json', {'pools': [pool(('gold_ingot', 1, uni(8, 16))), pool(('gold_block', 1, uni(1, 3))),
                                                            pool(('golden_apple', 1, uni(1, 2))), maybe('enchanted_golden_apple', 0.1)]})
    wjson('bm/loot_table/p113/throne_diamond.json', {'pools': [pool(('diamond', 1, uni(4, 10))), pool(('emerald', 1, uni(4, 8))),
                                                               maybe('diamond_block', 0.35), pool(('golden_apple', 1, uni(1, 2)))]})
    wjson('bm/loot_table/p113/throne_netherite.json', {'pools': [pool(('netherite_ingot', 1, None)), pool(('netherite_scrap', 1, uni(2, 4))),
                                                                 maybe('netherite_upgrade_smithing_template', 0.5), pool(('diamond', 1, uni(4, 8)))]})

    # ================================================================== PRIME FIGHTS
    G.FUNCS['p70/r/init'][0:0] = [f'execute if entity @s[tag=bm.gvr_{k}] run function bm:p113/prime/roll' for k in PRIME_KINDS]
    fn('p113/prime/roll', ['execute if score #fpr bm.gvv matches 2 run return 0',
                           'execute store result score #r bm.rng run random value 1..' + str(PRIME_IN),
                           'execute if score #fpr bm.gvv matches 1 run scoreboard players set #r bm.rng 1',
                           'execute unless score #r bm.rng matches 1 run return 0',
                           'tag @s add bm.gvprime',
                           label(relf(1.2, 8.6, 12.5), [T('⚔ PRIME ⚔\n', PRIME, bold=True), T('Tougher guards - richer pickings', 'gray')], 0.75)])
    G.FUNCS['p70/r/tick'].insert(1, 'execute if entity @s[tag=bm.gvprime] run function bm:p113/prime/tick')
    fn('p113/prime/tick', [f'execute positioned {rel(0, 3, 0)} as @e[tag=bm.gvg,tag=!bm.gvprm,dx=24,dy=24,dz=24] run function bm:p113/prime/buff',
                           f'execute if score @s bm.gvs matches 1..2 positioned {rel(0, 3, 0)} as @e[tag=bm.gvprm,dx=24,dy=24,dz=24] at @s run particle minecraft:crimson_spore ~ ~1 ~ 0.3 0.5 0.3 0 1'])
    fn('p113/prime/buff', ['tag @s add bm.gvprm',
                           'attribute @s minecraft:max_health modifier add bm:prime_hp 0.6 add_multiplied_base',
                           'attribute @s minecraft:attack_damage modifier add bm:prime_dmg 0.5 add_multiplied_base',
                           'attribute @s minecraft:movement_speed modifier add bm:prime_spd 0.12 add_multiplied_base',
                           'attribute @s minecraft:armor modifier add bm:prime_arm 4 add_value',
                           'attribute @s minecraft:knockback_resistance modifier add bm:prime_kb 0.25 add_value',
                           'data modify entity @s Health set value 1024f',
                           'execute if data entity @s CustomName run function bm:p113/prime/name'])
    fn('p113/prime/name', ['data modify storage bm:gv prn set value {text:"",extra:[{text:"Prime ",color:"' + PRIME + '",bold:true},""]}',
                           'data modify storage bm:gv prn.extra[1] set from entity @s CustomName',
                           'data modify entity @s CustomName set from storage bm:gv prn'])
    k = next(i for i, l in enumerate(G.FUNCS['p76/first_visit']) if l == 'tag @s add bm.gvseen')
    G.FUNCS['p76/first_visit'].insert(k + 1, 'execute if entity @s[tag=bm.gvprime] run function bm:p113/prime/warn')
    fn('p113/prime/warn', big('PRIME FIGHT', 'Tougher guards - richer pickings', PRIME) +
       [f'execute as {crew} at @s run playsound minecraft:event.raid.horn player @s ~ ~ ~ 0.6 1.2'])
    G.FUNCS['p70/solved'] += ['execute if entity @s[tag=bm.gvprime] run function bm:p113/prime/won']
    fn('p113/prime/won', ['scoreboard players operation #c bm.rng = #gt bm.rng', 'scoreboard players operation #c bm.rng *= #4 bm.rng',
                          'scoreboard players add #c bm.rng 8', inst('bm:p75/pot_add'),
                          f'execute as {my_crew} if score @s bm.gvi = #gi bm.rng at @s run function bm:p76/find {{t:"bm:p113/prime"}}'] +
       big('PRIME FIGHT WON', 'Extra coins in the pot - and a better find in every haul', PRIME))
    from phase76 import PHANTOM
    wjson('bm/loot_table/p113/prime.json', {'pools': [pool(('gutter_coin', 6, uni(12, 24)), ('second_wind', 4, None), ('lucky_purse', 4, None),
                                                           ('healing_draught', 3, uni(2, 3)), ('master_key', 2, None), ('lost_lantern', 2, None),
                                                           ('rats_foot', 2, None), *[(iid, 1, None) for iid, *_r in PHANTOM])]})
    for nm_, v, txt in (('always', 1, 'every fight room is PRIME'), ('never', 2, 'no fight room is PRIME'), ('chance', 0, f'one fight room in {PRIME_IN} is PRIME')):
        fn(f'admin/prime_{nm_}', [f'scoreboard players set #fpr bm.gvv {v}', tellraw('@s', P + [T(f'From the next heist, {txt}.', 'gray')])])
