"""2.93b: SYNERGY ATTACKS - every bond (phase188's pairs, phase100's trios) charges up in a fight and unleashes a combined
attack. Not one per combination: one per ROLE, the bond's role read from what its bond already gives (strength and fire are
offense; resistance and absorption defense; speed and haste speed; regeneration healing; slowing and weakening control),
and coloured with the bond's own colour.

  CHARGE      while a bond is formed and a monster is within 12 of you, it charges a second at a time - a pair in 20 s, a trio
              in 35 s (only one of each kind charges at once). Full: the next monster within 10 sets it off.
  OFFENSE     "Combined Strike": a burst round you - every monster within 6 takes 10 (a trio's: 18, then a second wave of 10
              within 9).
  DEFENSE     "Shield Wall": Resistance III and Absorption II for you and the bond for 6 s (a trio's: Resistance IV, Absorption
              IV, 8 s), and every monster within 5 thrown back.
  SPEED       "Blitz": Speed III for you, and four lightning-quick hits on monsters within 10, 5 each (a trio's: eight).
  HEALING     "Mending Light": you and the bond healed (Instant Health II; a trio's III) and Regeneration II; poison and wither
              washed off you.
  CONTROL     "Binding": every monster within 10 slowed to a crawl, weakened, lit up and lifted off its feet for a moment (a
              trio's: 12 blocks, longer, and pulled in towards you).
The attacks are announced on your action bar: the bond's name and the attack's."""
from items import T
import phase100 as P100
import phase188 as P188

FOE = 'type=#bm:hostile,tag=!bm.npc'
DUO_CHARGE, TRIO_CHARGE = 20, 35
ROLES = ('offense', 'defense', 'speed', 'healing', 'control')
KW = {'offense': ('strength', 'damage @', 'Fire:', 'wither', 'bolt'), 'defense': ('resistance', 'absorption', 'health_boost'),
      'speed': ('speed', 'jump_boost', 'haste', 'dolphins_grace'), 'healing': ('regeneration', 'p100/regen', 'instant_health', 'saturation'),
      'control': ('slowness', 'weakness', 'glowing', 'levitation')}
OVERRIDE = {'pearls': 'healing', 'customer': 'healing', 'familiar': 'healing', 'storm': 'offense', 'royal': 'healing', 'oath': 'defense',
            # (where the reading is close, the bond's own character decides)
            'odd': 'speed', 'ffs': 'control', 'tide': 'control', 'dread': 'offense', 'household': 'control', 'longdark': 'control',
            'nightmares': 'control', 'snowdog': 'control', 'patrol': 'control', 'prospect': 'offense'}
NAMES = {'offense': 'Combined Strike', 'defense': 'Shield Wall', 'speed': 'Blitz', 'healing': 'Mending Light', 'control': 'Binding'}
ICONP = {'offense': 'minecraft:crit', 'defense': 'minecraft:totem_of_undying', 'speed': 'minecraft:cloud', 'healing': 'minecraft:heart',
         'control': 'minecraft:enchant'}


def role_of(key, text):
    if key in OVERRIDE:
        return OVERRIDE[key]
    n = {r: sum(text.count(w) for w in ws) for r, ws in KW.items()}
    best = max(ROLES, key=lambda r: (n[r], -ROLES.index(r)))
    return best if n[best] else 'healing'


def _rgb(h):
    h = h.lstrip('#')
    return ','.join(f'{int(h[i:i + 2], 16) / 255:.2f}' for i in (0, 2, 4))


def extend_offers(O_, offer):
    pass


def generate(G):
    """(after phase188's and phase100's generate: hooks every pair's and trio's per-second function)"""
    fn, title = G.fn, G.title
    objs = ['bm.syn2', 'bm.syn3']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.FUNCS['loop/second'][-1:-1] = ['tag @a[tag=bm.syn2t] remove bm.syn2t', 'tag @a[tag=bm.syn3t] remove bm.syn3t']
    host = lambda k: P100.WHO[k]
    mine = lambda k, r=24: f'@e[type=minecraft:{host(k)[0]},tag={host(k)[1]},distance=..{r}]'

    # ---- the five attacks, a pair's and a trio's (as the player, at them; the bond's followers tagged bm.synm)
    def attack(role, trio):
        L = []
        if role == 'offense':
            L += [f'particle minecraft:sweep_attack ~ ~1 ~ 2.5 0.3 2.5 0 12', 'playsound minecraft:entity.player.attack.sweep player @a[distance=..16] ~ ~ ~ 1 0.7',
                  f'execute as @e[{FOE},distance=..6] run damage @s {18 if trio else 10} minecraft:magic']
            if trio:
                L += ['particle minecraft:explosion ~ ~1 ~ 3 0.5 3 0 6', 'playsound minecraft:entity.generic.explode player @a[distance=..16] ~ ~ ~ 0.6 1.4',
                      f'execute as @e[{FOE},distance=..9] run damage @s 10 minecraft:magic']
        elif role == 'defense':
            r, a, t = (3, 3, 8) if trio else (2, 1, 6)
            L += [f'effect give @s minecraft:resistance {t} {r} true', f'effect give @s minecraft:absorption {t} {a} true',
                  f'execute as @e[tag=bm.synm,distance=..24] run effect give @s minecraft:resistance {t} {r} true',
                  f'execute as @e[{FOE},distance=..5] at @s facing entity @p feet run tp @s ^ ^0.4 ^-3',
                  'playsound minecraft:item.shield.block player @a[distance=..16] ~ ~ ~ 1 0.6', 'particle minecraft:end_rod ~ ~1 ~ 1.2 1 1.2 0.05 30']
        elif role == 'speed':
            L += [f'effect give @s minecraft:speed 6 2 true', 'playsound minecraft:entity.breeze.wind_burst player @a[distance=..16] ~ ~ ~ 1 1.3']
            L += [f'execute as @e[{FOE},distance=..10,sort=random,limit=1] at @s run function bm:p208/zip' for _ in range(8 if trio else 4)]
        elif role == 'healing':
            L += [f'effect give @s minecraft:instant_health 1 {2 if trio else 1} true', 'effect give @s minecraft:regeneration 8 1 true',
                  'effect clear @s minecraft:poison', 'effect clear @s minecraft:wither',
                  f'execute as @e[tag=bm.synm,distance=..24] run effect give @s minecraft:instant_health 1 {2 if trio else 1} true',
                  'particle minecraft:happy_villager ~ ~1 ~ 1 1 1 0 30', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.6']
        elif role == 'control':
            rr, t = (12, 6) if trio else (10, 4)
            L += [f'effect give @e[{FOE},distance=..{rr}] minecraft:slowness {t} 3', f'effect give @e[{FOE},distance=..{rr}] minecraft:weakness {t} 1',
                  f'effect give @e[{FOE},distance=..{rr}] minecraft:glowing {t} 0', f'effect give @e[{FOE},distance=..{rr}] minecraft:levitation 1 1',
                  'playsound minecraft:block.respawn_anchor.charge player @a[distance=..16] ~ ~ ~ 1 0.8']
            if trio:
                L.append(f'execute as @e[{FOE},distance=..12] at @s facing entity @p feet run tp @s ^ ^ ^2')
        return L
    for role in ROLES:
        for trio in (False, True):
            fn(f'p208/{role}_{"trio" if trio else "duo"}', attack(role, trio))
    fn('p208/zip', ['particle minecraft:cloud ~ ~1 ~ 0.3 0.4 0.3 0.1 6', 'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.3 8',
                    'damage @s 5 minecraft:magic', 'playsound minecraft:entity.player.attack.strong player @a[distance=..16] ~ ~ ~ 0.6 1.6'])

    # ---- each bond: charge while fighting; full - set it off (its colour, its role's mark, its name on your bar)
    def bond(key, name, col, mem, trio):
        role = role_of(key, ' '.join(G.FUNCS.get(f'p100/{key}' if trio else f'p188/pair/{key}', [])))
        sc, tg, full = ('bm.syn3', 'bm.syn3t', TRIO_CHARGE) if trio else ('bm.syn2', 'bm.syn2t', DUO_CHARGE)
        fn(f'p208/b/{key}', [f'execute if entity @s[tag={tg}] run return 0', f'tag @s add {tg}',
                             f'execute unless entity @e[{FOE},distance=..12] run return 0',
                             f'execute unless score @s {sc} matches {full}.. run return run scoreboard players add @s {sc} 1',
                             f'execute unless entity @e[{FOE},distance=..10] run return 0',
                             f'scoreboard players set @s {sc} 0'] +
           [f'execute as {mine(m)} if function bm:p100/is_mine run tag @s add bm.synm' if trio else             # (a pair's: its leader's #me)
            f'execute as {mine(m)} if score @s bm.pid = #me bm.pid run tag @s add bm.synm' for m in mem] +
           [f'execute at @e[tag=bm.synm,distance=..24] run particle minecraft:dust{{color:[{_rgb(col)}],scale:1.6}} ~ ~1 ~ 0.4 0.6 0.4 0 16',
            f'particle minecraft:dust{{color:[{_rgb(col)}],scale:2.0}} ~ ~1 ~ 2 0.6 2 0 40', f'particle {ICONP[role]} ~ ~1 ~ 1.5 0.6 1.5 0.1 20',
            f'function bm:p208/{role}_{"trio" if trio else "duo"}', 'tag @e[tag=bm.synm] remove bm.synm',
            title('@s', 'actionbar', [T('Synergy! ' if not trio else 'Trio Synergy! ', 'gold', bold=True), T(name, col, bold=True),
                                      T(' - ', 'gray'), T(NAMES[role], 'white')])])
        return role
    ROLE = {}
    for k, (a, b, nm, col, *_r) in P188.PAIRS.items():
        ROLE[k] = bond(k, nm, col, (a, b), False)
        G.FUNCS[f'p188/pair/{k}'].append(f'execute as {P188.O} at @s run function bm:p208/b/{k}')
    chk = G.FUNCS['p100/check']
    at = next(i for i, l in enumerate(chk) if l == 'tag @s remove bm.trme')
    for i, (k, (nm, col, mem, *_r)) in enumerate(P100.TRIOS.items(), 1):
        ROLE[k] = bond(k, nm, col, mem, True)
    chk[at:at] = [f'execute if score #tr bm.rng matches {i} run function bm:p208/b/{k}' for i, k in enumerate(P100.TRIOS, 1)]
    return ROLE
