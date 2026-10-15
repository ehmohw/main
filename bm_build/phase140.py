"""Phase 140 (2.78): the vault's tiers climb in a curve. Guards used to rise by a flat +8 health a tier with no change in their
blows (Tier II barely harder than Tier I, Tier III little more), and a crew in rank-VI kits walked through Tier V. Now, on top of
the crew and Lucky Raid scaling:

            guards' health   damage   armour    the guardian's health  damage
  TIER I    26 (as before)   -        -         as before              as before
  TIER II   x1.2 (41)        +10%     +1        x1.1                   -
  TIER III  x1.35 (57)       +20%     +2        x1.25                  +2
  TIER IV   x1.5 (75)        +30%     +3        x1.4                   +4
  TIER V    x1.9 (110)       +45%     +6        x1.6 (about 976 solo)  +6, Resistance I from his shell on
  Tier V guards also shrug off a third of their knockback, move a step quicker, and one in four is Hardened (Resistance I).

Importing does nothing; generate(G) runs after phase101 and phase87 (it slips in ahead of their health line)."""

PCT = {2: 120, 3: 135, 4: 150, 5: 190}     # guards' health, % by tier
DMG = {2: 0.10, 3: 0.20, 4: 0.30, 5: 0.45}  # guards' damage, + by tier (add_multiplied_base)
ARM = {2: 1, 3: 2, 4: 3, 5: 6}
BOSS_PCT = {2: 110, 3: 125, 4: 140, 5: 160}  # the guardian's health, % by tier
BOSS_DMG = {3: 2, 4: 4, 5: 6}


def generate(G):
    fn = G.fn
    HPLINE = 'execute store result storage bm:gv h double 1 run scoreboard players get #h bm.rng'
    gs = G.FUNCS['p70/guard_set1']
    k = gs.index(HPLINE)
    gs[k:k] = ['function bm:p140/guard_hp']
    fn('p140/guard_hp', [f'execute if score #gt bm.rng matches {t} run scoreboard players operation #h bm.rng *= #k{p} bm.rng' for t, p in PCT.items()] +
       [f'execute if score #gt bm.rng matches {min(PCT)}.. run scoreboard players operation #h bm.rng /= #k100 bm.rng'])
    gs += ['function bm:p140/guard_more']
    fn('p140/guard_more',
       [f'execute if score #gt bm.rng matches {t} run attribute @s minecraft:attack_damage modifier add bm:gv_tier {d} add_multiplied_base' for t, d in DMG.items()] +
       [f'execute if score #gt bm.rng matches {t} run attribute @s minecraft:armor modifier add bm:gv_tier {a} add_value' for t, a in ARM.items()] +
       ['execute if score #gt bm.rng matches 5 run attribute @s minecraft:knockback_resistance modifier add bm:gv_tier 0.33 add_value',
        'execute if score #gt bm.rng matches 5 run attribute @s minecraft:movement_speed modifier add bm:gv_tier 0.1 add_multiplied_base',
        'execute if score #gt bm.rng matches 5 store result score #r bm.rng run random value 1..4',
        'execute if score #gt bm.rng matches 5 if score #r bm.rng matches 1 run function bm:p140/hardened'])
    fn('p140/hardened', ['effect give @s minecraft:resistance infinite 0 true', 'tag @s add bm.gvhard',
                         'particle minecraft:wax_off ~ ~1 ~ 0.3 0.6 0.3 0 8'])
    bs = G.FUNCS['p70/boss/setup']
    k = bs.index(HPLINE)
    bs[k:k] = [f'execute if score #gt bm.rng matches {t} run scoreboard players operation #h bm.rng *= #k{p} bm.rng' for t, p in BOSS_PCT.items()] + \
              [f'execute if score #gt bm.rng matches {min(BOSS_PCT)}.. run scoreboard players operation #h bm.rng /= #k100 bm.rng']
    dl = next(i for i, l in enumerate(bs) if l == 'execute store result storage bm:gv d double 1 run scoreboard players get #d bm.rng')
    bs[dl:dl] = [f'execute if score #gt bm.rng matches {t} run scoreboard players add #d bm.rng {d}' for t, d in BOSS_DMG.items()] + \
                ['execute if score #gt bm.rng matches 5 run tag @s add bm.gvt5']
    # (the guardian under half: Resistance I, Tier V only - once, when the shell would come)
    sh = G.FUNCS['p70/boss/shell']
    sh += ['execute if entity @s[tag=bm.gvt5] run effect give @s minecraft:resistance infinite 0 true']
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #k{p} bm.rng {p}' for p in sorted(set(PCT.values()) | set(BOSS_PCT.values()))] + ['scoreboard players set #k100 bm.rng 100']
