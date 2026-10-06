"""Phase 1.17: Lucky Night upgrades and playtest fixes.

- EVERY Overworld hostile can be Lucky: slimes, silverfish, endermites, evokers, vexes, ravagers and guardians join the
  roll (lucky only - they don't become Elites, Champions or Blood Moon horrors), and the 26.x parched skeleton joins
  the full tier list. When a Lucky Night begins, monsters already out get their 10% Lucky chance too, and Lucky
  monsters sparkle much more visibly.
- JACKPOT MONSTERS: only on Lucky Nights, about 1 in 250 Overworld hostile spawns. Bigger (1.35x), triple health,
  Strength II, +15% speed, a gold glow (seen through walls), and gold armour on anything that can wear it. They drop
  6-10 Tokens, 3-5 Lucky Tokens, maybe a Medallion and a JACKPOT SCRATCH CARD - five plays on one card.
- LUCKY PRIME ANIMALS: about 1 in 250 farm animals (1 in 50 on a Lucky Night): golden-glowing, bigger, and they drop
  five pieces of their Prime meat.
- Market (1.13-layout worlds): the Void Rat customer in the Blood Alcove leaves (Void Rats are End-only finds), and the
  Gilded Gutter's open south side is walled up (the new build seals it: market2.seal_room).
Importing registers the items; generate(G) runs after phase26.generate."""
from nbt import snbt, B, F, Int
from items import item, consumable, T, TOTEM

JACKPOT_N = 4                 # per 1000 Lucky-Night Overworld hostile spawns
LUCKY_ONLY = {'slime': 16, 'silverfish': 8, 'endermite': 8, 'evoker': 24, 'vex': 14, 'ravager': 100, 'guardian': 30}
ARMOUR_OK = {'zombie', 'husk', 'drowned', 'skeleton', 'stray', 'bogged', 'parched', 'zombie_villager', 'pillager', 'vindicator', 'evoker'}
OVERWORLD = ['zombie', 'husk', 'drowned', 'skeleton', 'stray', 'bogged', 'parched', 'pillager', 'vindicator', 'zombie_villager',
             'spider', 'cave_spider', 'creeper', 'enderman', 'witch', 'phantom', 'breeze']
PLAYS = 5

for n in range(PLAYS, 0, -1):
    item(f'jackpot_card_{n}', TOTEM, f'Jackpot Scratch Card ({n})', 'gold',
         [f'{n} play{"s" if n > 1 else ""} left on this card.', ('Hold right-click to scratch!', 'gray'),
          ('Dropped by Jackpot monsters on Lucky Nights.', 'yellow')],
         model='bm:scratch_card', glint=True, stack=1, cat='lucky',
         comps={'minecraft:consumable': consumable(1.0, 'brush', 'minecraft:item.brush.brushing.generic', False)})


def generate(G):
    fn, wjson, title, give, mob_name, loot_entry = G.fn, G.wjson, G.title, G.give, G.mob_name, G.loot_entry
    KILLED, chance, uni = G.KILLED, G.chance, G.uni
    fast, second = [], []
    G.FUNCS['load'][-1:-1] = ['team add bm.jackpot', 'team modify bm.jackpot color gold']
    vanilla = lambda t: {'rolls': 1, 'entries': [{'type': 'minecraft:loot_table', 'value': f'minecraft:entities/{t}'}]}

    # ================================================================ lucky-only hostiles
    for t, hp in LUCKY_ONLY.items():
        second.append(f'execute as @e[type=minecraft:{t},tag=!bm.seen] at @s run function bm:mobs/init/{t}')
        fn(f'mobs/init/{t}', ['tag @s add bm.seen',
                              f'execute if score #lnight bm.bm matches 1 if dimension minecraft:overworld run return run function bm:mobs/lucky_roll/{t}',
                              'execute store result score #r bm.rng run random value 1..1000',
                              f'execute if score #r bm.rng matches 1..6 run return run function bm:mobs/lucky/{t}'])
        fn(f'mobs/lucky_roll/{t}', ['execute store result score #r bm.rng run random value 1..1000',
                                    f'execute if score #r bm.rng matches 1..100 run return run function bm:mobs/lucky/{t}'])
        lhp = int(hp * 1.5)
        fn(f'mobs/lucky/{t}', [
            f'data merge entity @s {snbt({"DeathLootTable": f"bm:entities/lucky/{t}", "CustomName": mob_name("Lucky ", "yellow", t, True)})}',
            'tag @s add bm.lucky', 'tag @s add bm.tiered',
            f'attribute @s minecraft:max_health base set {lhp}', f'data modify entity @s Health set value {lhp}.0f'])
        wjson(f'bm/loot_table/entities/lucky/{t}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla(t),
            {'rolls': 1, 'entries': [loot_entry('lucky_token')], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('lucky_token')], 'conditions': [KILLED, chance(0.4)]}]})

    # ================================================================ jackpot monsters (Lucky Nights only)
    hps = {t: (G.ARMORED[t][0] if t in G.ARMORED else G.UNARMORED[t]) for t in OVERWORLD}
    hps.update(LUCKY_ONLY)
    for t, hp in hps.items():
        roll = G.FUNCS[f'mobs/lucky_roll/{t}']
        roll[0:0] = ['execute store result score #jr bm.rng run random value 1..1000',
                     f'execute if score #jr bm.rng matches 1..{JACKPOT_N} run return run function bm:mobs/jackpot/{t}']
        jhp = hp * 3
        body = [f'data merge entity @s {snbt({"DeathLootTable": f"bm:entities/jackpot/{t}", "CustomName": mob_name("Jackpot ", "gold", t, True)})}',
                'tag @s add bm.jackpot', 'tag @s add bm.lucky', 'tag @s add bm.tiered',
                'attribute @s minecraft:scale base set 1.35',
                f'attribute @s minecraft:max_health base set {jhp}', f'data modify entity @s Health set value {jhp}.0f',
                'attribute @s minecraft:movement_speed modifier add bm:jackpot_speed 0.15 add_multiplied_base',
                'effect give @s minecraft:strength infinite 1 true',
                'team join bm.jackpot @s']
        if t in ARMOUR_OK:
            for slot, piece in (('head', 'helmet'), ('chest', 'chestplate'), ('legs', 'leggings'), ('feet', 'boots')):
                body.append(f'item replace entity @s armor.{slot} with minecraft:golden_{piece}[enchantments={{"minecraft:protection":3}}]')
            body.append(f'data merge entity @s {snbt({"drop_chances": {s: F(0.0) for s in ("head", "chest", "legs", "feet")}})}')
        body.append('playsound minecraft:block.amethyst_block.chime hostile @a[distance=..24] ~ ~ ~ 1 0.6')
        fn(f'mobs/jackpot/{t}', body)
        wjson(f'bm/loot_table/entities/jackpot/{t}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla(t),
            {'rolls': 1, 'entries': [loot_entry('token', uni(6, 10))], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('lucky_token', uni(3, 5))], 'conditions': [KILLED]},
            {'rolls': 1, 'entries': [loot_entry('medallion')], 'conditions': [KILLED, chance(0.5)]},
            {'rolls': 1, 'entries': [loot_entry(f'jackpot_card_{PLAYS}')], 'conditions': [KILLED]}]})
    second.append('execute as @e[tag=bm.jackpot] at @s run particle minecraft:wax_on ~ ~1.3 ~ 0.4 0.7 0.4 0 6')

    # Lucky monsters sparkle 4x a second near players (the old once-a-second sparkle was easy to miss)
    fast.append('execute as @e[tag=bm.lucky] at @s if entity @a[distance=..40] run particle minecraft:wax_on ~ ~0.9 ~ 0.3 0.5 0.3 0 2')

    # a Lucky Night beginning: monsters already out get their Lucky chance too
    lucky_types = list(G.ARMORED) + list(G.UNARMORED) + list(LUCKY_ONLY)
    fn('p27/reroll', ['execute store result score #r bm.rng run random value 1..10', 'execute unless score #r bm.rng matches 1 run return 0'] +
       [f'execute if entity @s[type=minecraft:{t}] run return run function bm:mobs/lucky/{t}' for t in lucky_types])
    G.FUNCS['p22/lucky/start'].append('execute as @e[type=#bm:hostile,tag=bm.seen,tag=!bm.tiered,tag=!bm.npc,tag=!bm.revenant,tag=!bm.wil_body] '
                                      'at @s if dimension minecraft:overworld run function bm:p27/reroll')

    # ================================================================ jackpot scratch cards: five plays each
    for n in range(PLAYS, 0, -1):
        G.consume_adv(f'jackpot_card_{n}', f'bm:p27/jcard_{n}')
        back = []
        if n > 1:
            back = [f'execute unless items entity @s weapon.mainhand * run item replace entity @s weapon.mainhand with {G.item_arg(f"jackpot_card_{n - 1}")}',
                    f'execute unless items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"jackpot_card_{n - 1}"}}] run ' + give(f'jackpot_card_{n - 1}')]
        left = n - 1
        fn(f'p27/jcard_{n}', [f'advancement revoke @s only bm:consume/jackpot_card_{n}'] + back +
           ['scoreboard players set @s bm.sct 10',
            title('@s', 'actionbar', T(f'{left} play{"s" if left != 1 else ""} left on your Jackpot card.' if left else 'That was the last play on your Jackpot card.', 'gold'))])

    # ================================================================ lucky prime animals: five pieces of Prime meat
    for a, meat in G.ANIMALS.items():
        init = G.FUNCS[f'mobs/init/{a}']
        assert init[0] == 'tag @s add bm.seen'
        init[1:1] = ['execute store result score #lp bm.rng run random value 1..250',
                     f'execute if score #lnight bm.bm matches 1 if score #lp bm.rng matches ..5 run return run function bm:p27/lprime/{a}',
                     f'execute if score #lp bm.rng matches 1 run return run function bm:p27/lprime/{a}']
        hp = G.ANIMAL_HP[a] * 3
        fn(f'p27/lprime/{a}', [
            f'data merge entity @s {snbt({"DeathLootTable": f"bm:entities/lucky_prime/{a}", "PersistenceRequired": B(1), "CustomName": mob_name("Lucky Prime ", "gold", a, True)})}',
            'tag @s add bm.lprime', 'attribute @s minecraft:scale base set 1.3',
            f'attribute @s minecraft:max_health base set {hp}', f'data modify entity @s Health set value {hp}.0f',
            'team join bm.jackpot @s'])        # 2.13: it glows only while someone is within 10 blocks (below)
        wjson(f'bm/loot_table/entities/lucky_prime/{a}.json', {'type': 'minecraft:entity', 'pools': [
            vanilla(a), {'rolls': 1, 'entries': [loot_entry(meat, 5)]}]})
    second.append('execute as @e[tag=bm.lprime] at @s run particle minecraft:wax_on ~ ~0.9 ~ 0.35 0.35 0.35 0 4')
    second += ['execute as @e[tag=bm.lprime,tag=!bm.lpg] run effect clear @s minecraft:glowing', 'tag @e[tag=bm.lprime,tag=!bm.lpg] add bm.lpg',
               'execute as @e[tag=bm.lprime] at @s if entity @a[distance=..10] run effect give @s minecraft:glowing 2 0 true']

    # ================================================================ market patches for 1.13-layout markets already in worlds
    # the Void Rat customer leaves the Blood Alcove
    second.append('execute as @e[type=minecraft:item_display,tag=bm.crowd] if items entity @s contents *[minecraft:item_model="bm:rat3d_void"] run kill @s')
    # the Gilded Gutter is walled up: the same cells the new build seals, placed relative to the Forge's ambience marker
    # (markers turn with the structure, so local ^ coordinates follow any rotation)
    import market2
    MB = market2.build()
    ax, ay, az = 60, market2.W + 2, 24                              # the bm.amb_forge marker's block
    cells = sorted(c for c in market2.VIP_SHELL if not MB.b.get(c, 'minecraft:air').endswith(':air'))
    wjson('bm/tags/block/p27_open.json', {'values': ['minecraft:air', 'minecraft:cave_air', 'minecraft:light']})
    patch = [f'execute if block ^{x - ax} ^{y - ay} ^{z - az} #bm:p27_open run setblock ^{x - ax} ^{y - ay} ^{z - az} {MB.b[(x, y, z)]}'
             for (x, y, z) in cells]
    xs, zs = [c[0] - ax for c in cells], [c[2] - az for c in cells]
    fn('p27/vip_patch', ['tag @s add bm.vip17'] + patch)
    second.append(f'execute as @e[type=minecraft:marker,tag=bm.amb_forge,tag=!bm.vip17] at @s rotated as @s '
                  f'if loaded ^{min(xs)} ^ ^{min(zs)} if loaded ^{max(xs)} ^ ^{max(zs)} if loaded ^{min(xs)} ^ ^{max(zs)} if loaded ^{max(xs)} ^ ^{min(zs)} '
                  f'run function bm:p27/vip_patch')
    G.P27_PATCH_CELLS = len(cells)

    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def post_admin(G):
    G.FUNCS['admin/uninstall'][-1:-1] = ['team remove bm.jackpot', 'team remove bm.wil']
