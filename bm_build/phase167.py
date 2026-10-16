"""2.80i: TOUGH MOBS, NOT HEALTH SPONGES - and not faster than a sprinting player.

GEAR  Elites, Champions, Blood Moon horrors (and the Lucky Night's jackpot mobs) wore Protection on every piece: IV on an
      Elite's diamond, V (and Thorns II) on a Champion's netherite - 20 points, the game's 80% cap - IV on a horror's
      netherite, III on a jackpot mob's gold. On top of two to five times the health, they soaked up a fight. Now each piece
      rolls its own enchantment as the mob arrives - most of it light, some of it bare:
                 bare   Prot I  Prot II  Prot III  other (projectile, fire or blast protection II)
        Elite     40%    30%     20%       -        10%
        Champion  25%    35%     30%      10%        -      (no more Thorns II on everything)
        Blood     30%    40%     30%       -         -
        Jackpot   50%    35%     15%       -         -
      An unarmored Champion (a spider, a creeper...) wears Resistance I, not II.
SPEED  a Blood Moon horror had Speed I AND +20% (about x1.44), a Champion +15% (and Speed II on the unarmored kinds), an
      unarmored Elite Speed I: they ran down a sprinting player. Now: horrors and Champions +10%, unarmored Elites +10%,
      jackpot mobs +10% - and CREEPERS no boost at all, at any tier: a Blood Moon creeper (charged, a charged creeper's
      blast) ran at about 1.44 times a creeper's pace, a Champion's at 1.6, so you couldn't get clear. The quick kinds were the danger - a spider is fast to begin with, and a Champion spider with Speed II
      on top of +15% ran at about 1.6 times that. (Measured: a Blood Moon horror zombie now chases at 2.8 blocks a second, a
      vanilla zombie 2.3, a sprinting player 5.6. A monster on a steed is slower still - a monster-ridden horse moves at well
      under a sprint - so the steeds keep their speed, for whoever claims one.)
"""
import re

TIERS = {   # tier: [(weight, enchantments)]
    'elite': [(40, {}), (30, {'protection': 1}), (20, {'protection': 2}), (10, 'alt')],
    'champion': [(25, {}), (35, {'protection': 1}), (30, {'protection': 2}), (10, {'protection': 3})],
    'blood': [(30, {}), (40, {'protection': 1}), (30, {'protection': 2})],
    'jackpot': [(50, {}), (35, {'protection': 1}), (15, {'protection': 2})],
}
ALT = {'head': 'projectile_protection', 'chest': 'blast_protection', 'legs': 'fire_protection', 'feet': 'projectile_protection'}
SPEED = 0.1
ARM = re.compile(r'^item replace entity @s armor\.(head|chest|legs|feet) with (minecraft:[a-z_]+)\[enchantments=\{[^{}]*\}(,.*)?\]$')


def generate(G):
    fn = G.fn
    n_arm = 0
    made = set()
    for name in sorted(G.FUNCS):
        m = re.fullmatch(r'mobs/(elite|champion|blood|jackpot)/[a-z_]+', name)
        if not m: continue
        tier = m.group(1)
        L = G.FUNCS[name]
        for i, l in enumerate(L):
            a = ARM.match(l)
            if not a: continue
            slot, base, rest = a.group(1), a.group(2), a.group(3) or ''
            key = f'p167/arm/{tier}_{slot}_{base.split(":")[1]}' + ('_t' if 'trim=' in rest else '')
            if key not in made:
                made.add(key)
                lines, lo = ['execute store result score #r bm.rng run random value 1..100'], 1
                for w, en in TIERS[tier]:
                    if en == 'alt': en = {ALT[slot]: 2}
                    ench = ','.join(f'"minecraft:{k}":{v}' for k, v in en.items())
                    comps = (f'enchantments={{{ench}}}' if ench else '') + rest
                    comps = comps.lstrip(',')
                    item = f'{base}[{comps}]' if comps else base
                    lines.append(f'execute if score #r bm.rng matches {lo}..{lo + w - 1} run return run item replace entity @s armor.{slot} with {item}')
                    lo += w
                assert lo == 101, (tier, lo)
                fn(key, lines)
            L[i] = f'function bm:{key}'
            n_arm += 1
        # ---- speed: one modest boost, no Speed effect on top
        G.FUNCS[name] = L = [l for l in L if l != 'effect give @s minecraft:speed infinite 0 true' and l != 'effect give @s minecraft:speed infinite 1 true']
        for i, l in enumerate(L):
            L[i] = re.sub(r'(movement_speed modifier add bm:(?:blood|champion|jackpot_speed)) [0-9.]+ add_multiplied_base', rf'\1 {SPEED} add_multiplied_base', l)
            if tier == 'champion' and l == 'effect give @s minecraft:resistance infinite 1 true':
                L[i] = 'effect give @s minecraft:resistance infinite 0 true'
        if tier == 'elite' and 'attribute @s minecraft:scale base set 1.15' in L:            # (the unarmored kinds: Speed I was their boost)
            L.append(f'attribute @s minecraft:movement_speed modifier add bm:elite {SPEED} add_multiplied_base')
        # (creepers: no speed boost at any tier - one you can't outrun is a blast you can't escape)
        if name.endswith('/creeper'):
            G.FUNCS[name] = [l for l in G.FUNCS[name] if 'minecraft:movement_speed modifier add' not in l]
    assert n_arm >= 4 * 4 * 10, n_arm
    # (nothing should still wear a full Protection set, or run with Speed on top)
    for name, L in G.FUNCS.items():
        if re.fullmatch(r'mobs/(elite|champion|blood|jackpot)/[a-z_]+', name):
            assert not any('"minecraft:protection":4' in l or '"minecraft:protection":5' in l or 'minecraft:speed infinite' in l for l in L), name
