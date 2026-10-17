"""2.67: THE ROGUES' GALLERY - more of the vault's guards, odd sizes and speeds, and a second guardian for every tier.

NEW GUARDS     every tier's roster doubles, drawn from the whole hostile pool: Gutter Urchins and Copper Bruisers, Vault Crawlers,
               Coin Mites and Copper Jockeys (I); Rimelings, Silver Widows, Ex-Tellers and Iron Brutes (II); Gilded Hogs,
               Gutter Gamblers, Gilt Wisps, Gilded Archers, Molten Coins and Golden Jockeys (III); Abyss Crawlers, Gem Mites, Mirror
               Thieves, Rime Archers and the little Vault Ravager (IV); Ash Imps, Reaper Giants, Ravager Riders, Gale Wardens, Hoard
               Turrets, Void Mites and Twin Embers (V).
ODD ONES       any guard may turn up TINY (small, quick, frail), HULKING (huge, slow, hits like a cart), SWIFT, or - from Tier III -
               IRONCLAD; now and then a BLUR (tiny and swift at once) or a JUGGERNAUT (hulking and ironclad).
GUARDIANS      half the heists meet a different guardian at the vault: THE MITE MOTHER (I - a silverfish the size of a cart, and
               her brood), THE WIDOW QUEEN (II - webs you down, calls her spiderlings), THE GOLDEN JOCKEY (III - a great hog with
               the Gambler King on its back), THE ABYSSAL RAVAGER (IV - ridden by the Mirror Mage), THE ASHEN COLOSSUS (V - a
               wither skeleton three men tall; the ground shakes when he stamps, and the Ash Imps come).
"""
from items import T
from nbt import snbt, B, F, Int, D
import phase75 as P75

GOLD = '#ffcf40'
mk = P75._mob
NOREIN = P75.NOREIN
TAGS = ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen']
SMALL = {'Tags': TAGS + ['bm.v93s']}          # (these get less health than a guard of their tier, the big ones more)
BIG = {'Tags': TAGS + ['bm.v93b']}


def rider(m):
    """a mob as a passenger: its own guard tags, set up by the same guard_set as its mount"""
    ty, n = m
    return dict(n, id=f'minecraft:{ty}', Tags=n['Tags'] + ['bm.v93ride'])


NEW = {
    1: [(2, mk('zombie', 'Gutter Urchin', '#e0a070', {'mainhand': 'minecraft:copper_sword'}, dict(SMALL, IsBaby=B(1), CanBreakDoors=B(0)),
               dict(NOREIN, scale=0.9, movement_speed=0.3))),
        (2, mk('zombie', 'Copper Bruiser', '#c06a30', {'head': 'minecraft:copper_helmet', 'mainhand': 'minecraft:copper_axe'}, dict(BIG, IsBaby=B(0), CanBreakDoors=B(0)),
               dict(NOREIN, scale=1.45, movement_speed=0.18, attack_damage=6.0, knockback_resistance=0.6))),
        (2, mk('spider', 'Vault Crawler', '#a07050', {}, {}, {'scale': 0.8, 'movement_speed': 0.36})),
        (1, mk('silverfish', 'Coin Mite', '#e0c060', {}, {}, {'scale': 1.8, 'movement_speed': 0.32, 'attack_damage': 3.0})),
        (1, mk('slime', 'Gutter Goo', '#80c050', {}, {'Size': Int(1)})),
        (1, ('spider', dict(mk('spider', 'Copper Jockey', '#e0884a', {})[1],
                            Passengers=[rider(mk('skeleton', 'Copper Jockey', '#e0884a', {'head': 'minecraft:copper_helmet', 'mainhand': 'minecraft:bow'}))])))],
    2: [(2, mk('stray', 'Rimeling', '#c0e8ff', {'mainhand': 'minecraft:bow'}, SMALL, {'scale': 0.6, 'movement_speed': 0.36})),
        (2, mk('cave_spider', 'Silver Widow', '#c8d0d8', {}, {}, {'scale': 1.3, 'movement_speed': 0.33})),
        (2, mk('zombie_villager', 'Ex-Teller', '#a0a8b0', {'head': 'minecraft:iron_helmet', 'mainhand': 'minecraft:iron_sword'}, {'IsBaby': B(0), 'CanBreakDoors': B(0)}, NOREIN)),
        (1, mk('vindicator', 'Iron Brute', '#8a9098', {'head': 'minecraft:iron_helmet', 'mainhand': 'minecraft:iron_axe'}, BIG,
               {'scale': 1.4, 'movement_speed': 0.28, 'knockback_resistance': 0.5}))],                          # (2.82: the Vault Bat, a phantom, is gone - phantoms stuck to the ceilings)
    3: [(2, mk('hoglin', 'Gilded Hog', GOLD, {}, {'IsImmuneToZombification': B(1), 'CannotBeHunted': B(1)}, {'scale': 0.9})),
        (2, mk('piglin', 'Gutter Gambler', GOLD, {'head': 'minecraft:golden_helmet', 'mainhand': 'minecraft:crossbow'}, {'IsImmuneToZombification': B(1), 'CannotHunt': B(1)})),
        (1, mk('vex', 'Gilt Wisp', '#fff0a0', {'mainhand': 'minecraft:golden_sword'}, SMALL, {'scale': 0.8})),
        (2, mk('skeleton', 'Gilded Archer', GOLD, {'head': 'minecraft:golden_helmet', 'chest': 'minecraft:golden_chestplate',
                                                 'mainhand': {'id': 'minecraft:bow', 'count': Int(1), 'components': {'minecraft:enchantments': {'minecraft:power': 2}}}})),
        (1, mk('magma_cube', 'Molten Coin', '#ff9a30', {}, {'Size': Int(1)})),
        (1, ('hoglin', dict(mk('hoglin', 'Golden Jockey', GOLD, {}, {'IsImmuneToZombification': B(1), 'CannotBeHunted': B(1)})[1],
                            Passengers=[rider(mk('piglin', 'Golden Jockey', GOLD, {'head': 'minecraft:golden_helmet', 'mainhand': 'minecraft:golden_sword'},
                                                 {'IsBaby': B(1), 'IsImmuneToZombification': B(1), 'CannotHunt': B(1)}))])))],
    4: [(2, mk('spider', 'Abyss Crawler', '#3a8aa0', {}, BIG, {'scale': 1.6, 'movement_speed': 0.34})),
        (2, mk('endermite', 'Gem Mite', '#7ae8ff', {}, {}, {'scale': 2.0, 'movement_speed': 0.35, 'attack_damage': 4.0})),
        (1, mk('illusioner', 'Mirror Thief', '#a080ff', {'mainhand': 'minecraft:bow'})),
        (2, mk('stray', 'Rime Archer', '#a0d8ff', {'head': 'minecraft:diamond_helmet',
                                                  'mainhand': {'id': 'minecraft:bow', 'count': Int(1), 'components': {'minecraft:enchantments': {'minecraft:power': 3}}}})),
        (1, mk('ravager', 'Vault Ravager', '#5a7a8a', {}, SMALL, {'scale': 0.7, 'attack_damage': 7.0}))],
    5: [(2, mk('wither_skeleton', 'Ash Imp', '#7a6a6a', {'mainhand': 'minecraft:stone_sword'}, SMALL, {'scale': 0.6, 'movement_speed': 0.38})),
        (2, mk('wither_skeleton', 'Reaper Giant', '#3a3a4a', {'head': 'minecraft:netherite_helmet', 'mainhand': 'minecraft:netherite_axe'}, BIG,
               {'scale': 1.6, 'movement_speed': 0.22, 'knockback_resistance': 0.7})),
        (1, ('ravager', dict(mk('ravager', 'Ravager Rider', '#8a5a3a', {})[1],
                             Passengers=[rider(mk('pillager', 'Ravager Rider', '#8a5a3a', {'head': 'minecraft:golden_helmet', 'mainhand': 'minecraft:crossbow'}))]))),
        (2, mk('breeze', 'Gale Warden', '#c0e0ff', {}, {}, {'scale': 1.4})),
        (1, mk('shulker', 'Hoard Turret', GOLD, {})),
        (1, mk('endermite', 'Void Mite', '#c080ff', {}, {}, {'scale': 2.4, 'movement_speed': 0.4, 'attack_damage': 5.0})),
        (1, mk('blaze', 'Twin Ember', '#ffb040', {}, SMALL, {'scale': 0.7}))],
}
for _t, _ents in NEW.items():
    P75.ROSTER[_t] += _ents

# odd ones: (tag, name prefix, colour, scale x, speed x, health x, damage x, extra armor, knockback resistance)
AFFIX = {'tiny': ('Tiny ', '#ff9ad8', -0.4, 0.5, 0.6, 1.0, 0, 0),
         'hulk': ('Hulking ', '#ff7a4a', 0.5, -0.2, 1.6, 1.5, 0, 0.5),
         'swift': ('Swift ', '#7ae8ff', 0, 0.6, 1.0, 1.0, 0, 0),
         'iron': ('Ironclad ', '#a0a8b8', 0, -0.1, 1.2, 1.0, 10, 0.3),
         'blur': ('Blur ', '#ffffff', -0.4, 0.9, 0.6, 1.0, 0, 0),
         'jugg': ('Juggernaut ', '#ff4a4a', 0.55, -0.25, 2.0, 1.6, 10, 1.0)}

# a second guardian for every tier: (type, name, colour, bossbar colour, equipment, extra nbt, attributes, tag)
ALT = {1: ('silverfish', 'The Mite Mother', '#e0c060', 'yellow', {}, {}, {'scale': 4.5, 'movement_speed': 0.3}, 'mite'),
       2: ('spider', 'The Widow Queen', '#c8d0d8', 'white', {}, {}, {'scale': 2.2, 'movement_speed': 0.32}, 'widow'),
       3: ('hoglin', 'The Golden Jockey', GOLD, 'yellow', {}, {'IsImmuneToZombification': B(1), 'CannotBeHunted': B(1)}, {'scale': 1.7, 'movement_speed': 0.34}, 'jockey'),
       4: ('ravager', 'The Abyssal Ravager', '#3a8aa0', 'blue', {}, {}, {'scale': 1.2}, 'ravager'),
       5: ('wither_skeleton', 'The Ashen Colossus', '#5a5a6a', 'red', {'head': 'minecraft:netherite_helmet', 'chest': 'minecraft:netherite_chestplate',
                                                                       'mainhand': {'id': 'minecraft:netherite_sword', 'count': Int(1),
                                                                                    'components': {'minecraft:enchantment_glint_override': True}}},
           {}, {'scale': 2.6, 'movement_speed': 0.2}, 'colossus')}
ALT_RIDER = {3: mk('piglin', 'The Gambler King', GOLD, {'head': {'id': 'minecraft:golden_helmet', 'count': Int(1), 'components': {'minecraft:enchantment_glint_override': True}},
                                                         'mainhand': 'minecraft:crossbow'}, {'IsImmuneToZombification': B(1), 'CannotHunt': B(1), 'CustomNameVisible': B(1)}),
             4: mk('illusioner', 'The Mirror Mage', '#a080ff', {'mainhand': 'minecraft:bow'}, {'CustomNameVisible': B(1)})}
MINION = {1: mk('silverfish', 'Mite Brood', '#e0c060', {}, {}, {'scale': 1.2, 'movement_speed': 0.3}),
          2: mk('cave_spider', 'Spiderling', '#c8d0d8', {}, {}, {'movement_speed': 0.32}),
          5: mk('wither_skeleton', 'Ash Imp', '#7a6a6a', {'mainhand': 'minecraft:stone_sword'}, SMALL, {'scale': 0.6, 'movement_speed': 0.38})}


def extend_offers(O, offer):
    pass


def generate(G):
    import phase70 as P70
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    wjson('bm/predicate/p93/half.json', {'condition': 'minecraft:random_chance', 'chance': 0.5})

    # riders sit higher than guard_set looks (a ravager's rider is two blocks up): set them up too
    G.FUNCS['p70/guard_set'][0:0] = ['function bm:p93/riders']
    fn('p93/riders', ['execute as @e[tag=bm.v93ride,tag=bm.gvnew2,distance=..5] at @s run function bm:p70/guard_set1',
                      'tag @e[tag=bm.v93ride,tag=bm.gvnew2,distance=..5] remove bm.gvnew2'])

    # ================================================================== the odd ones
    # (as a guard, just set up): smaller or bigger kinds keep their size's health; then maybe an odd one
    G.FUNCS['p70/guard_set1'] += ['function bm:p93/odd']
    fn('p93/odd', ['execute if entity @s[tag=bm.v93s] run function bm:p93/hp {m:6}', 'execute if entity @s[tag=bm.v93b] run function bm:p93/hp {m:15}',
                   'execute if entity @s[tag=bm.gvcap] run return 0', 'execute if entity @s[tag=bm.gvgrum] run return 0', 'execute if entity @s[tag=bm.gvshiny] run return 0',
                   'execute if entity @s[tag=bm.v93s] run return 0', 'execute if entity @s[tag=bm.v93b] run return 0',
                   'execute if score #gn bm.rng matches 1.. run return 0',
                   'execute if score #noodd bm.gvv matches 1 run return 0',
                   'execute store result score #r bm.rng run random value 1..100',
                   'execute if score #r bm.rng matches 1..7 run return run function bm:p93/aff/tiny',
                   'execute if score #r bm.rng matches 8..13 run return run function bm:p93/aff/hulk',
                   'execute if score #r bm.rng matches 14..18 run return run function bm:p93/aff/swift',
                   'execute if score #gt bm.rng matches 3.. if score #r bm.rng matches 19..22 run return run function bm:p93/aff/iron',
                   'execute if score #gt bm.rng matches 2.. if score #r bm.rng matches 23 run return run function bm:p93/aff/blur',
                   'execute if score #gt bm.rng matches 3.. if score #r bm.rng matches 24 run return run function bm:p93/aff/jugg'])
    fn('p93/hp', ['execute store result score #h bm.rng run attribute @s minecraft:max_health base get', '$scoreboard players set #q bm.rng $(m)',
                  'scoreboard players operation #h bm.rng *= #q bm.rng', 'scoreboard players operation #h bm.rng /= #10 bm.rng',
                  'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng', 'function bm:p70/hp with storage bm:gv',
                  'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng'])
    for k, (pre, col, sc, sp, hp, dm, ar, kb) in AFFIX.items():
        lines = [f'tag @s add bm.aff_{k}']
        if sc: lines.append(f'attribute @s minecraft:scale modifier add bm:aff {sc} add_multiplied_total')
        if sp: lines.append(f'attribute @s minecraft:movement_speed modifier add bm:aff {sp} add_multiplied_total')
        if dm != 1.0: lines.append(f'attribute @s minecraft:attack_damage modifier add bm:aff {dm - 1:.2f} add_multiplied_total')
        if ar: lines += [f'attribute @s minecraft:armor modifier add bm:aff {ar} add_value', 'attribute @s minecraft:armor_toughness modifier add bm:aff 4 add_value']
        if kb: lines.append(f'attribute @s minecraft:knockback_resistance modifier add bm:aff {kb} add_value')
        if hp != 1.0: lines.append(f'function bm:p93/hp {{m:{int(hp * 10)}}}')
        # (the prefixed name is put together in storage and set once: a name with an empty extra list won't decode)
        lines += ['data modify storage bm:gv aff.c set value ' + snbt({'text': pre, 'color': col, 'bold': True}),
                  'execute if data entity @s CustomName run data modify storage bm:gv aff.c.extra set value []',
                  'execute if data entity @s CustomName run data modify storage bm:gv aff.c.extra append from entity @s CustomName',
                  'data modify entity @s CustomName set from storage bm:gv aff.c']
        if k in ('blur', 'jugg'): lines.append('data merge entity @s {CustomNameVisible:1b}')
        fn(f'p93/aff/{k}', lines)
    G.FUNCS['loop/second'].append('execute as @e[tag=bm.aff_blur] at @s run particle minecraft:cloud ~ ~0.4 ~ 0.2 0.2 0.2 0.01 2')
    G.FUNCS['loop/second'].append('execute as @e[tag=bm.aff_swift] at @s run particle minecraft:end_rod ~ ~0.5 ~ 0.2 0.3 0.2 0.01 1')

    # ================================================================== the second guardians
    for t, (ty, nm, col, bcol, eq, extra, attrs, tg) in ALT.items():
        boss = {'Tags': ['bm.gvboss', 'bm.gvbnew', 'bm.tiered', 'bm.seen', 'bm.b93', f'bm.b93_{tg}'], 'PersistenceRequired': B(1), 'CustomName': T(nm, col, bold=True),
                'CustomNameVisible': B(1), 'DeathLootTable': 'bm:gv/boss', 'drop_chances': {k: F(0) for k in ('head', 'chest', 'legs', 'feet', 'mainhand', 'offhand')},
                'attributes': [{'id': 'minecraft:armor', 'base': D(10)}, {'id': 'minecraft:knockback_resistance', 'base': D(0.0)}, {'id': 'minecraft:follow_range', 'base': D(40)}] +
                              [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in attrs.items()],
                'equipment': {k: ({'id': v, 'count': Int(1)} if isinstance(v, str) else v) for k, v in eq.items()}}
        boss.update(extra)
        if t in ALT_RIDER:
            r = dict(ALT_RIDER[t][1], id=f'minecraft:{ALT_RIDER[t][0]}')
            r['Tags'] = TAGS + ['bm.b93rider', 'bm.v93ride']
            boss['Passengers'] = [r]
        fn(f'p93/boss_alt{t}', [f'summon minecraft:{ty} ~ ~ ~ {snbt(boss)}'] + (['function bm:p93/riders'] if t in ALT_RIDER else []) +
           [f'execute if score #gi bm.rng matches {s + 1} run tag @e[tag=bm.gvbnew,limit=1] add bm.gvboss{s}' for s in range(P70.SLOTS)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} name {snbt(T(nm, col, bold=True))}' for s in range(P70.SLOTS)] +
           [f'execute if score #gi bm.rng matches {s + 1} run bossbar set bm:gvb{s} color {bcol}' for s in range(P70.SLOTS)])
    # half the time (the admin's flag can force it either way: #fboss 1 always, -1 never)
    G.FUNCS['p75/boss_tier'][0:0] = ['execute if score #fboss bm.gvv matches -1 run return run function bm:p93/boss_std',
                                     'execute if score #fboss bm.gvv matches 1 run return run function bm:p93/boss_alt',
                                     'execute if predicate bm:p93/half run return run function bm:p93/boss_alt']
    fn('p93/boss_std', [l for l in G.FUNCS['p75/boss_tier'] if 'p93/' not in l])
    fn('p93/boss_alt', [f'execute if score #gt bm.rng matches {t} run return run function bm:p93/boss_alt{t}' for t in ALT])
    fn('admin/heist_boss_alt', ['scoreboard players set #fboss bm.gvv 1', tellraw('@s', P + [T('Every vault guardian is the second one now.', 'gray')])])
    fn('admin/heist_boss_std', ['scoreboard players set #fboss bm.gvv -1', tellraw('@s', P + [T('Every vault guardian is the usual one now.', 'gray')])])
    fn('admin/heist_boss_any', ['scoreboard players reset #fboss bm.gvv', tellraw('@s', P + [T('The vault guardian is drawn by chance again.', 'gray')])])

    # what they do, besides the usual (every second, as the guardian)
    G.FUNCS['loop/second'].append('execute as @e[tag=bm.b93,tag=bm.gvboss] at @s run function bm:p93/boss/sec')
    fn('p93/boss/sec', ['scoreboard players add @s bm.gvx 1', 'scoreboard players operation #gi bm.rng = @s bm.gvi'] +
       [f'execute if entity @s[tag=bm.b93_{tg}] run function bm:p93/boss/{tg}' for (*_x, tg) in ALT.values()])
    def brood(t, n, every):
        ty, nbt = MINION[t]
        return [f'execute store result score #ng bm.rng if entity @e[tag=bm.gvg,distance=..30]',
                f'scoreboard players operation #q bm.rng = @s bm.gvx', f'scoreboard players operation #q bm.rng %= #{every} bm.rng',
                'execute unless score #q bm.rng matches 0 run return 0', 'execute if score #ng bm.rng matches 8.. run return 0', 'function bm:p70/ctx'] + \
               sum(([f'execute positioned ^{dx} ^ ^1 run summon minecraft:{ty} ~ ~ ~ {snbt(nbt)}', f'execute positioned ^{dx} ^ ^1 run function bm:p70/guard_set']
                    for dx in (-1.5, 1.5)[:n]), [])
    fn('p93/boss/mite', brood(1, 2, 4) + ['execute if score #q bm.rng matches 0 run playsound minecraft:entity.silverfish.ambient hostile @a[distance=..24] ~ ~ ~ 1 0.5',
                                          'execute if score #q bm.rng matches 0 run particle minecraft:block{block_state:"minecraft:stone"} ~ ~0.5 ~ 1 0.3 1 0 30'])
    fn('p93/boss/widow', ['scoreboard players operation #q2 bm.rng = @s bm.gvx', 'scoreboard players operation #q2 bm.rng %= #3 bm.rng',
                          'execute if score #q2 bm.rng matches 0 as @a[tag=bm.gvp,distance=..6] run effect give @s minecraft:slowness 2 2',
                          'execute if score #q2 bm.rng matches 0 if entity @a[tag=bm.gvp,distance=..6] run particle minecraft:block{block_state:"minecraft:cobweb"} ~ ~0.5 ~ 3 0.3 3 0 40',
                          'execute if score #q2 bm.rng matches 0 if entity @a[tag=bm.gvp,distance=..6] run playsound minecraft:block.cobweb.place hostile @a[distance=..20] ~ ~ ~ 1 0.6'] +
       brood(2, 2, 6))
    fn('p93/boss/jockey', ['scoreboard players operation #q bm.rng = @s bm.gvx', 'scoreboard players operation #q bm.rng %= #6 bm.rng',
                           'execute if score #q bm.rng matches 0 run effect give @s minecraft:speed 2 2 true',
                           'execute if score #q bm.rng matches 0 run playsound minecraft:entity.hoglin.angry hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                           'execute if score #q bm.rng matches 0 run particle minecraft:wax_on ~ ~1 ~ 1 0.5 1 0 20',
                           'execute if score #q bm.rng matches 0 run ' + title('@a[tag=bm.gvp,distance=..24]', 'actionbar', T('The Golden Jockey charges!', GOLD))])
    fn('p93/boss/ravager', ['scoreboard players operation #q bm.rng = @s bm.gvx', 'scoreboard players operation #q bm.rng %= #7 bm.rng',
                            'execute unless score #q bm.rng matches 0 run return 0',
                            'playsound minecraft:entity.ravager.roar hostile @a[distance=..30] ~ ~ ~ 1 0.8', 'particle minecraft:sonic_boom ~ ~1.5 ~ 0 0 0 0 1',
                            'execute as @a[tag=bm.gvp,distance=..5] at @s run damage @s 4 minecraft:mob_attack by @e[tag=bm.b93_ravager,limit=1,sort=nearest]',
                            'execute as @a[tag=bm.gvp,distance=..5] run effect give @s minecraft:slowness 2 1'])
    fn('p93/boss/colossus', brood(5, 2, 8) + ['scoreboard players operation #q2 bm.rng = @s bm.gvx', 'scoreboard players operation #q2 bm.rng %= #5 bm.rng',
                                              'execute if score #q2 bm.rng matches 0 if entity @a[tag=bm.gvp,distance=..7] run function bm:p93/boss/stomp'])
    fn('p93/boss/stomp', ['particle minecraft:explosion ~ ~0.3 ~ 2.5 0.1 2.5 0 12', 'particle minecraft:block{block_state:"minecraft:blackstone"} ~ ~0.3 ~ 3.5 0.2 3.5 0 70',
                          'playsound minecraft:entity.generic.explode hostile @a[distance=..30] ~ ~ ~ 1 0.5', 'playsound minecraft:entity.wither_skeleton.ambient hostile @a[distance=..30] ~ ~ ~ 1 0.5',
                          'execute as @a[tag=bm.gvp,distance=..7] at @s run damage @s 6 minecraft:mob_attack by @e[tag=bm.b93_colossus,limit=1,sort=nearest]',
                          'effect give @a[tag=bm.gvp,distance=..7] minecraft:levitation 1 3 true', 'effect give @a[tag=bm.gvp,distance=..7] minecraft:wither 3 0'])
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in (3, 4, 5, 6, 7, 8, 10)]
