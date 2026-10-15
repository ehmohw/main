"""Phase 140 (2.78): the top of the vault bites back. A crew in rank-VI kits walked through Tier V - a Hoard guard had 58
health, three blows from a Bloodlust Offense kit, and the Gutter King fell before his second shell. Now, on top of the crew
and Lucky Raid scaling:

  TIER IV   guards: +35% health, +20% damage, +3 armour.
  TIER V    guards: +90% health, +45% damage, +6 armour, a third less knockback, a step quicker; one in four is
            Hardened (Resistance I). The guardian: +60% health, +6 damage, Resistance I below half health.

Importing does nothing; generate(G) runs after phase101 and phase87 (it slips in ahead of their health line)."""

PCT = {4: 135, 5: 190}                     # guards' health, % by tier
DMG = {4: 0.20, 5: 0.45}                   # guards' damage, + by tier (add_multiplied_base)
ARM = {4: 3, 5: 6}
BOSS_PCT, BOSS_DMG = 160, 6                # Tier V's guardian


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
    bs[k:k] = [f'execute if score #gt bm.rng matches 5 run scoreboard players operation #h bm.rng *= #k{BOSS_PCT} bm.rng',
               'execute if score #gt bm.rng matches 5 run scoreboard players operation #h bm.rng /= #k100 bm.rng']
    dl = next(i for i, l in enumerate(bs) if l == 'execute store result storage bm:gv d double 1 run scoreboard players get #d bm.rng')
    bs[dl:dl] = [f'execute if score #gt bm.rng matches 5 run scoreboard players add #d bm.rng {BOSS_DMG}', 'execute if score #gt bm.rng matches 5 run tag @s add bm.gvt5']
    # (the guardian under half: Resistance I, Tier V only - once, when the shell would come)
    sh = G.FUNCS['p70/boss/shell']
    sh += ['execute if entity @s[tag=bm.gvt5] run effect give @s minecraft:resistance infinite 0 true']
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #k{p} bm.rng {p}' for p in sorted(set(PCT.values()) | {BOSS_PCT})] + ['scoreboard players set #k100 bm.rng 100']
