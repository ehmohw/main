"""3.1f: HARD MODE HITS BACK - the owner: "the reason they're so easy is because the OP potion effects you can carry in from
followers. The bosses ought to have ways to negate regen, strength, and resistance effects ... for 20-30 seconds at a time as a
unique move they use" - "same for the mires" - "I'd give dread mobs the same ability" (the natural ones in the Overworld and the
Undercrown, never the ones in the Dread Sovereign's fight) - "the alien mobs (ONLY THE ONES IN THE ARMADA)" - "lower the boss
cooldown to 45 seconds" - "both followers & potions" - "the nullify attack should remove *all* positive potion effects".

NULLIFIED   (a player: bm.nul, ticks left) every tick, every positive effect is stripped - a follower's, a potion's, a beacon's,
            gear's: none of them takes while it lasts (Resistance given by a cutscene's own shelter, amplifier 4 and up, is left be).
            The action bar counts it down; a dark haze hangs on them; when it ends, "your strength returns".
THE BOSSES  (hard mode) every boss of the pack (bm.boss - the dungeons', the Dread three, the Sovereign, Admiral Vexis) and every
            Statue Knight awake (bm.khost, never a friendly one at home): every 45 s of a fight (a player within 28), a warning
            (2 s: its name, "NULLIFY", a darkening ring) - then the pulse: everyone within 28 Nullified for 25 s. Never while it is
            invulnerable (its cinematics, dormant).
THE MIRES   (wild ones; the Dread Mire and the Brood-Mire - mirekit) a GRAB or a STAB that lands: 20 s.
THE MOBS    a blow from a thing of the Dread (bm.dread, bm.udread) or one of the Armada's own Vorn (bm.avorn, bm.aguard): one in
            four, 15 s - then 45 s before a mob can do it to them again. Never within 48 of the Dread Sovereign (its own pulse is
            enough).
SUNDER      (bm:sunder - past armour and Protection, not past Resistance: the Nullify takes that) Admiral Vexis's Solar Lance,
            star-flares and ring-shockwave. (The Dread's own blows - bm:dread - already go past both.)
GIFTS       (3.1f, the owner: "a way to disable the keeper's gifts as it turns into inventory bloat ... the rat king ... the same
            option") the Keeper of Bonds' and the Rat King's menus: "Gifts: on / off" (bm.nogift_kb, bm.nogift_rk) - the Keeper's
            gifts; the King's loans and the King's Cut."""
from items import T

COL = '#b04aff'
POS = ['speed', 'haste', 'strength', 'jump_boost', 'regeneration', 'resistance', 'fire_resistance', 'water_breathing', 'invisibility',
       'night_vision', 'health_boost', 'absorption', 'saturation', 'luck', 'slow_falling', 'conduit_power', 'dolphins_grace',
       'hero_of_the_village']
BOSS_T, MIRE_T, MOB_T = 25 * 20, 20 * 20, 15 * 20
EVERY, WARN, REACH = 45, 2, 28
MOB_CHANCE, MOB_CD = 4, 45
MOBS = ['bm.dread', 'bm.udread', 'bm.avorn', 'bm.aguard']
PLAYERS = 'gamemode=!creative,gamemode=!spectator'


def generate(G):
    fn, tellraw, title, wjson = G.fn, G.tellraw, G.title, G.wjson
    F = G.FUNCS
    objs = ['bm.nul', 'bm.nuc', 'bm.nulm']
    F['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    wjson('bm/predicate/p280/shield.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                            'predicate': {'effects': {'minecraft:resistance': {'amplifier': {'min': 4}}}}})

    # ---- NULLIFIED: #nd ticks (at least), as the player
    fn('p280/on', [f'execute unless entity @s[{PLAYERS}] run return 0',
                   'execute unless score @s bm.nul matches 1.. run function bm:p280/start',
                   'execute unless score @s bm.nul >= #nd bm.rng run scoreboard players operation @s bm.nul = #nd bm.rng'])
    fn('p280/start', ['title @s times 4 30 10', title('@s', 'title', T('')), title('@s', 'subtitle', T('NULLIFIED - your blessings are gone', COL, bold=True)),
                      'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 1 0.5', 'playsound minecraft:entity.wither.ambient player @s ~ ~ ~ 0.5 1.6'])
    fn('p280/tick', [f'effect clear @s minecraft:{e}' for e in POS if e != 'resistance'] +
       ['execute unless predicate bm:p280/shield run effect clear @s minecraft:resistance',
        'scoreboard players remove @s bm.nul 1',
        'scoreboard players operation #nq bm.rng = @s bm.nul', 'scoreboard players operation #nq bm.rng %= #20 bm.rng',
        'execute if score #nq bm.rng matches 0 run function bm:p280/bar',
        'execute if score #nq bm.rng matches 0 at @s run particle minecraft:dust{color:[0.35,0.1,0.5],scale:1.3} ~ ~1 ~ 0.35 0.6 0.35 0 8',
        'execute unless score @s bm.nul matches 1.. run function bm:p280/end'])
    fn('p280/bar', ['scoreboard players operation #ns bm.rng = @s bm.nul', 'scoreboard players operation #ns bm.rng /= #20 bm.rng',
                    title('@s', 'actionbar', [T('NULLIFIED ', COL, bold=True), T('- no blessing takes for ', 'gray'),
                                             {'score': {'name': '#ns', 'objective': 'bm.rng'}, 'color': 'white'}, T(' s', 'gray')])])
    fn('p280/end', ['scoreboard players reset @s bm.nul', title('@s', 'actionbar', T('Your strength returns.', '#c8a8ff', italic=True)),
                    'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 0.8 1.4'])
    F['tick'].append('execute as @a[scores={bm.nul=1..}] at @s run function bm:p280/tick')

    # ---- THE BOSSES: every 45 s of a fight, a warning, then the pulse
    second = []
    for sel in ('@e[tag=bm.boss,tag=!bm.boss_part]', '@e[type=minecraft:husk,tag=bm.khost,tag=!bm.khome,tag=!bm.npc]'):
        second.append(f'execute if score #hard bm.cfg matches 1 as {sel} at @s if entity @a[distance=..{REACH},{PLAYERS}] run function bm:p280/b/sec')
    fn('p280/b/sec', ['execute if entity @s[nbt={Invulnerable:1b}] run return 0', 'scoreboard players add @s bm.nuc 1',
                      f'execute if score @s bm.nuc matches {EVERY - WARN} run function bm:p280/b/warn',
                      f'execute if score @s bm.nuc matches {EVERY}.. run function bm:p280/b/pulse'])
    fn('p280/b/warn', [tellraw(f'@a[distance=..{REACH}]', [{'selector': '@s', 'color': 'white', 'bold': True}, T(' gathers the dark - ', 'gray'), T('NULLIFY', COL, bold=True), T(' in 2 s!', 'gray')]),
                       'playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                       'particle minecraft:portal ~ ~1 ~ 3 1 3 0.5 160 force'] +
       [f'particle minecraft:dust{{color:[0.45,0.1,0.65],scale:2.0}} ^{8 * __import__("math").sin(a * 0.3927):.2f} ^0.2 ^{8 * __import__("math").cos(a * 0.3927):.2f} 0.2 0 0.2 0 3 force' for a in range(16)])
    fn('p280/b/pulse', ['scoreboard players set @s bm.nuc 0', f'scoreboard players set #nd bm.rng {BOSS_T}',
                        f'execute as @a[distance=..{REACH},{PLAYERS}] at @s run function bm:p280/on',
                        'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..40] ~ ~ ~ 2 0.6',
                        'particle minecraft:sonic_boom ~ ~1.5 ~ 0 0 0 0 1 force', 'particle minecraft:reverse_portal ~ ~1 ~ 6 1 6 0.2 300 force'])

    # ---- THE MOBS: a blow from the Dread or the Armada's own Vorn - one in four, then 45 s spared
    for t in MOBS:
        wjson(f'bm/advancement/p280/hit_{t.split(".")[1]}.json', {'criteria': {'h': {'trigger': 'minecraft:entity_hurt_player', 'conditions': {
            'damage': {'source_entity': {'nbt': '{Tags:["%s"]}' % t}}}}}, 'rewards': {'function': f'bm:p280/mob/{t.split(".")[1]}'}})
        fn(f'p280/mob/{t.split(".")[1]}', [f'advancement revoke @s only bm:p280/hit_{t.split(".")[1]}', 'function bm:p280/mob/try'])
    fn('p280/mob/try', ['execute unless score #hard bm.cfg matches 1 run return 0',
                        'execute if score @s bm.nulm matches 1.. run return 0',
                        'execute at @s if entity @e[tag=bm.usov,distance=..48] run return 0',
                        f'execute store result score #r bm.rng run random value 1..{MOB_CHANCE}', 'execute unless score #r bm.rng matches 1 run return 0',
                        f'scoreboard players set @s bm.nulm {MOB_CD}', f'scoreboard players set #nd bm.rng {MOB_T}', 'function bm:p280/on'])
    second.append('scoreboard players remove @a[scores={bm.nulm=1..}] bm.nulm 1')

    # ---- THE MIRES: a grab or a stab that lands (mirekit calls p280/mire)
    fn('p280/mire', [f'scoreboard players set #nd bm.rng {MIRE_T}', 'function bm:p280/on'])
    F['loop/second'][-1:-1] = second

    # ---- SUNDER: past armour and Protection
    wjson('bm/damage_type/sunder.json', {'exhaustion': 0.1, 'message_id': 'bm.sunder', 'scaling': 'never'})

    # ---- GIFTS: on / off
    for k, who in (('kb', 'The Keeper of Bonds'), ('rk', 'The Rat King')):
        fn(f'p280/gift/{k}', [f'execute if entity @s[tag=bm.nogift_{k}] run return run function bm:p280/gift/{k}_on',
                              f'tag @s add bm.nogift_{k}', title('@s', 'actionbar', [T(f'{who}\'s gifts: ', 'gray'), T('off', 'red', bold=True), T(' (your pockets stay tidy)', 'dark_gray')])])
        fn(f'p280/gift/{k}_on', [f'tag @s remove bm.nogift_{k}', title('@s', 'actionbar', [T(f'{who}\'s gifts: ', 'gray'), T('on', 'green', bold=True)])])
    F['admin/uninstall'][0:0] = ['scoreboard players reset * bm.nul']


def late(G):
    """(after every module that writes the damage-type tags) Sunder goes past armour and Protection; Vexis's three moves take it"""
    import json, os
    for tg in ('bypasses_armor', 'bypasses_enchantments'):
        p = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(p))['values'] if os.path.exists(p) else []
        G.wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:sunder'] + ['bm:sunder']})
    n = 0
    for f, old in (('p242/lnc/hit', 'damage @s 18 minecraft:in_fire by'), ('p242/a/ring_hit', 'damage @s 10 minecraft:mob_attack by')):
        L = G.FUNCS[f]
        for i, l in enumerate(L):
            if l.startswith(old): L[i] = l.replace(old.split()[3], 'bm:sunder', 1); n += 1
    for f, L in G.FUNCS.items():
        if not f.startswith('p242/'): continue
        for i, l in enumerate(L):
            if isinstance(l, str) and 'damage @s 14 minecraft:in_fire by' in l: L[i] = l.replace('minecraft:in_fire', 'bm:sunder'); n += 1
    assert n >= 3, n
    return n
