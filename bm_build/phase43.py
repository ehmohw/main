"""2.21: cosmetics for the special nights, wings in the Hollow Throne, the Experience Charm.

- NIGHT COSMETICS: Blood Moon horrors, Lucky monsters and the Vorn (troopers, saucers, bioengineered beasts) sometimes carry
  a cosmetic charm - and SHOW it, wearing its particles, so you know which ones to hunt. Three per night, each rarer than
  the last (3% / 1% / 0.3% of those monsters carry one). Killed by a player, a carrier drops its charm half the time.
  The Vorn charms also turn up, rarely, in mothership stores and crash wrecks.
- WINGS: the Angelic Wings and the Evil Wings wait in the Hollow Throne's hidden vault.
- THE EXPERIENCE CHARM (the Captain, Rat Gang HQ, 10 Trophies): anywhere in your inventory, the monsters you kill drop
  twice the experience.
- The Hollow Throne's loot chests refill after every Blood Moon (the next time anyone is there).
Charms work like the other cosmetic charms: keep one anywhere in your inventory; one charm shows at a time."""
import math
from items import item, T, TOTEM

# key: (night, tier, name, colour, lore, particle lines run at the feet of the carrier / the charm's owner)
NIGHT = {
    'crimson_drip': ('blood', 1, 'Crimson Drip Charm', '#c81e1e', 'Blood beads on you and drips away.',
                     ['particle minecraft:dust{color:[0.6,0.0,0.02],scale:1.1} ~ ~1.2 ~ 0.25 0.45 0.25 0 2', 'particle minecraft:dripping_lava ~ ~1.6 ~ 0.2 0.2 0.2 0 1']),
    'bloodbat': ('blood', 2, 'Bloodbat Charm', '#8a0a14', 'Shadowy bat-shapes wheel around you.',
                 ['$execute rotated $(a) 0 positioned ^ ^1.9 ^0.7 run particle minecraft:dust{color:[0.15,0.0,0.02],scale:1.4} ~ ~ ~ 0.05 0.05 0.05 0 2',
                  '$execute rotated $(b) 0 positioned ^ ^1.5 ^0.8 run particle minecraft:dust{color:[0.5,0.0,0.03],scale:1.2} ~ ~ ~ 0.05 0.05 0.05 0 2',
                  'particle minecraft:crimson_spore ~ ~1 ~ 0.4 0.5 0.4 0 2']),
    'blood_halo': ('blood', 3, 'Blood Moon Halo', '#ff2a2a', 'A crown of blood light hangs over you.',
                   'RING_RED'),
    'clover': ('lucky', 1, 'Clover Charm', '#4ade5a', 'Little green sparks of luck.',
               ['particle minecraft:happy_villager ~ ~1 ~ 0.35 0.5 0.35 0 1', 'particle minecraft:dust{color:[0.2,0.85,0.3],scale:0.9} ~ ~0.6 ~ 0.3 0.3 0.3 0 1']),
    'gold_rush': ('lucky', 2, 'Gold Rush Charm', '#ffd23f', 'Gold coins rain down around you.',
                  ['particle minecraft:dust{color:[1.0,0.82,0.15],scale:1.2} ~ ~2.3 ~ 0.4 0.1 0.4 0 2', 'particle minecraft:falling_dust{block_state:"minecraft:gold_block"} ~ ~2.2 ~ 0.4 0.1 0.4 0 2',
                   'particle minecraft:wax_on ~ ~1 ~ 0.4 0.5 0.4 0 1']),
    'jackpot_crown': ('lucky', 3, 'Jackpot Crown', '#ffe14a', 'A golden crown of luck and fireworks.', 'RING_GOLD'),
    'xenite_glow': ('alien', 1, 'Xenite Glow Charm', '#5aff7a', 'You glow like a Xenite crystal.',
                    ['particle minecraft:glow ~ ~1 ~ 0.3 0.5 0.3 0 1', 'particle minecraft:dust{color:[0.35,1.0,0.45],scale:0.9} ~ ~0.8 ~ 0.3 0.4 0.3 0 1']),
    'tractor_beam': ('alien', 2, 'Tractor Beam Charm', '#7affd8', 'A thin green tractor beam lifts off you.',
                     ['particle minecraft:end_rod ~ ~2.4 ~ 0.05 0.6 0.05 0.01 1', 'particle minecraft:dust{color:[0.4,1.0,0.6],scale:1.0} ~ ~1.6 ~ 0.15 1.0 0.15 0 3']),
    'saucer_orbit': ('alien', 3, 'Saucer Orbit Charm', '#b0ff5a', 'A tiny flying saucer circles your head.',
                     ['$execute rotated $(a) 0 positioned ^ ^2.2 ^0.6 run particle minecraft:dust{color:[0.7,0.75,0.8],scale:1.3} ~ ~ ~ 0.05 0.02 0.05 0 3',
                      '$execute rotated $(a) 0 positioned ^ ^2.12 ^0.6 run particle minecraft:electric_spark ~ ~ ~ 0.1 0 0.1 0 1',
                      '$execute rotated $(a) 0 positioned ^ ^2.05 ^0.6 run particle minecraft:dust{color:[0.35,1.0,0.45],scale:0.7} ~ ~-0.1 ~ 0 0.15 0 0 1']),
}
NIGHT_TAGS = {'blood': ['bm.blood'], 'lucky': ['bm.lucky'], 'alien': ['bm.vorn', 'bm.bio']}
ROLL = {3: (1, 3), 2: (4, 13), 1: (14, 43)}          # out of 1000: 0.3% / 1% / 3%
NIGHT_NAME = {'blood': 'Blood Moon horrors', 'lucky': 'Lucky monsters', 'alien': 'the Vorn and their beasts'}
RARITY = {1: ('Uncommon', 'green'), 2: ('Rare', 'aqua'), 3: ('Very rare', 'light_purple')}

for k, (night, tier, name, col, lore, _) in NIGHT.items():
    item(f'charm_{k}', TOTEM, name, col, [lore, (f'Carried (and shown off) by {NIGHT_NAME[night]}.', 'light_purple'),
                                          (RARITY[tier][0], RARITY[tier][1]), ('Keep it anywhere in your inventory.', 'gray'),
                                          ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
         model=f'bm:charm_{k}', stack=1, cat='cosmetic', glint=tier >= 2)
item('charm_wings_angel', TOTEM, 'Angelic Wings', '#fff6d8', ['Feathers of light, folded at your back.', ('Found in the Hollow Throne.', 'light_purple'),
                                                              ('Keep it anywhere in your inventory.', 'gray'), ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
     model='bm:charm_wings_angel', stack=1, cat='cosmetic', glint=True, bold=True)
item('charm_wings_evil', TOTEM, 'Evil Wings', '#8a2a3a', ['Ragged wings of smoke and embers.', ('Found in the Hollow Throne.', 'light_purple'),
                                                           ('Keep it anywhere in your inventory.', 'gray'), ('Cosmetic only. One charm shows at a time.', 'dark_gray')],
     model='bm:charm_wings_evil', stack=1, cat='cosmetic', glint=True, bold=True)
item('xp_charm', TOTEM, 'Experience Charm', '#7cff4a', ['The Rat King\'s scholar swore by it.', ('Anywhere in your inventory: monsters you kill', 'blue'),
                                                        ('drop twice the experience.', 'blue')],
     model='bm:xp_charm', stack=1, cat='relic', glint=True)

# wing feathers (x right of the spine, y up from the feet); mirrored for the left wing
WING = [(0.25, 1.45), (0.45, 1.58), (0.65, 1.68), (0.85, 1.74), (1.05, 1.72), (1.22, 1.62), (0.35, 1.28), (0.55, 1.34), (0.75, 1.38),
        (0.95, 1.38), (1.12, 1.32), (0.45, 1.12), (0.65, 1.14), (0.85, 1.12), (1.0, 1.05), (0.55, 0.95), (0.75, 0.92)]


def extend_offers(O, offer):
    O['captain'] += [offer(('trophy', 10), ('xp_charm', 1))]


def _ring(r, n, y, part):
    return [f'particle {part} ~{r * math.cos(2 * math.pi * i / n):.2f} ~{y} ~{r * math.sin(2 * math.pi * i / n):.2f} 0 0 0 0 1' for i in range(n)]


def generate(G):
    fn, wjson, give = G.fn, G.wjson, G.give
    holds = '*[minecraft:custom_data~{bm:"%s"}]'
    fast, second, tick = [], [], []
    objs = ['bm.hbn dummy']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]

    # ---------------- the cosmetics' particles (shared by carriers and owners)
    special = {'RING_RED': _ring(0.35, 8, 2.3, 'minecraft:dust{color:[0.9,0.05,0.05],scale:0.8}') + ['particle minecraft:dripping_lava ~ ~2.25 ~ 0.2 0 0.2 0 1'],
               'RING_GOLD': _ring(0.33, 8, 2.3, 'minecraft:dust{color:[1.0,0.85,0.2],scale:0.8}') + ['particle minecraft:firework ~ ~2.4 ~ 0.2 0.05 0.2 0.02 1',
                                                                                                 'particle minecraft:happy_villager ~ ~2.35 ~ 0.25 0.05 0.25 0 1']}
    for k, (_, _, _, _, _, parts) in NIGHT.items():
        lines = special[parts] if isinstance(parts, str) else parts
        if any(l.startswith('$') for l in lines):
            fn(f'p43/fx/{k}_m', lines)
            fn(f'p43/fx/{k}', [f'function bm:p43/fx/{k}_m with storage bm:fx'])
        else:
            fn(f'p43/fx/{k}', lines)
    wing = lambda part, x, y: f'particle {part} ^{x:.2f} ^{y:.2f} ^-0.32 0 0 0 0 1'
    ang = [wing('minecraft:dust{color:[1.0,0.98,0.9],scale:0.7}', s * x, y) for x, y in WING for s in (1, -1)] + \
          [wing('minecraft:end_rod', s * x, y) for x, y in WING[3:6] for s in (1, -1)][:2]
    evil = [wing('minecraft:dust{color:[0.12,0.02,0.04],scale:0.8}', s * x, y) for x, y in WING for s in (1, -1)] + \
           [wing('minecraft:small_flame', s * 1.05, 1.72) for s in (1, -1)] + ['particle minecraft:smoke ^ ^1.4 ^-0.5 0.4 0.2 0.05 0 1']
    fn('p43/fx/wings_angel', ['execute rotated ~ 0 run function bm:p43/fx/wings_angel_d'])
    fn('p43/fx/wings_angel_d', ang)
    fn('p43/fx/wings_evil', ['execute rotated ~ 0 run function bm:p43/fx/wings_evil_d'])
    fn('p43/fx/wings_evil_d', evil)
    lines = []
    for k in ['wings_angel', 'wings_evil'] + sorted(NIGHT, key=lambda q: -NIGHT[q][1]):
        lines += [f'execute if items entity @s container.* {holds % ("charm_" + k)} run return run function bm:p43/fx/{k}',
                  f'execute if items entity @s weapon.offhand {holds % ("charm_" + k)} run return run function bm:p43/fx/{k}']
    G.FUNCS['p17/charm/pick'][0:0] = lines                    # the rarest showpieces win

    # ---------------- carriers: rolled once per special-night monster; they wear their charm
    for night, tags in NIGHT_TAGS.items():
        ks = {NIGHT[k][1]: k for k in NIGHT if NIGHT[k][0] == night}
        fn(f'p43/roll/{night}', ['tag @s add bm.ccr', 'execute store result score #r bm.rng run random value 1..1000'] +
           [f'execute if score #r bm.rng matches {ROLL[t][0]}..{ROLL[t][1]} run tag @s add bm.cc_{ks[t]}' for t in (3, 2, 1)] +
           ['execute if score #r bm.rng matches ..43 run tag @s add bm.ccar', 'execute if score #r bm.rng matches ..43 run function bm:p43/ccm'])
        for tg in tags:
            second.append(f'execute as @e[tag={tg},tag=!bm.ccr,type=!minecraft:player] at @s run function bm:p43/roll/{night}')
    for k in NIGHT:
        fast.append(f'execute as @e[tag=bm.cc_{k},type=!minecraft:player] at @s if entity @a[distance=..48] run function bm:p43/fx/{k}')
    wjson('bm/advancement/p43/carrier.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.ccar"]}'}}]}}},
        'rewards': {'function': 'bm:p43/carrier'}})
    # (26.3: a dying mob is invisible to @e, so each carrier wears a marker; the marker finds its fallen carrier)
    fn('p43/ccm', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.ccm","bm.ccmnew"]}', 'ride @e[type=minecraft:marker,tag=bm.ccmnew,limit=1] mount @s',
                   'tag @e[type=minecraft:marker,tag=bm.ccmnew] remove bm.ccmnew'])
    fn('p43/vdead', ['execute on vehicle if data entity @s {Health:0.0f} run return 1', 'return 0'])
    fn('p43/carrier', ['advancement revoke @s only bm:p43/carrier',
                       'execute as @e[type=minecraft:marker,tag=bm.ccm,distance=..96] if function bm:p43/vdead at @s run function bm:p43/mdrop'])
    fn('p43/mdrop', ['execute on vehicle run function bm:p43/drop', 'kill @s'])
    second.append('execute as @e[type=minecraft:marker,tag=bm.ccm] unless function bm:p41/has_vehicle run kill @s')
    fn('p43/drop', ['execute store result score #r bm.rng run random value 1..2', 'execute unless score #r bm.rng matches 1 run return 0'] +
       [f'execute if data entity @s {{Tags:["bm.cc_{k}"]}} run loot spawn ~ ~ ~ loot bm:items/charm_{k}' for k in NIGHT] +
       ['particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.4 0.3 0.2 20', 'playsound minecraft:entity.player.levelup hostile @a[distance=..24] ~ ~ ~ 0.7 1.6'])
    # the Vorn charms in their wrecks and stores
    import json, mig263
    from nbt import to_json
    for t, chances in (('mothership_stores', (0.06, 0.025, 0.008)), ('crash_wreck', (0.04, 0.015, 0.005))):
        path = G.path('data', 'bm', 'loot_table', 'p32', f'{t}.json')
        obj = json.load(open(path))
        pools = [{'rolls': 1, 'entries': [G.loot_entry(f'charm_{k}')], 'conditions': [G.chance(c)]} for k, c in zip(('xenite_glow', 'tractor_beam', 'saucer_orbit'), chances)]
        obj['pools'] += mig263.convert(f'bm/loot_table/p32/{t}.json', to_json(mig263.custom_data_snbt({'type': 'minecraft:chest', 'pools': pools})))['pools']
        json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)

    # ---------------- the Experience Charm: what dies near you (killed by you) drops its experience twice over
    # (26.3 drops a mob's orbs the moment it dies, right after this reward runs: next tick, fresh orbs near the killer are doubled)
    G.FUNCS['p33/kill'].append('execute if function bm:p43/xp/has run tag @s add bm.xpk')
    fn('p43/xp/has', [f'execute if items entity @s container.* {holds % "xp_charm"} run return 1',
                      f'execute if items entity @s weapon.offhand {holds % "xp_charm"} run return 1', 'return 0'])
    tick.append('execute as @a[tag=bm.xpk] at @s run function bm:p43/xp/next')
    fn('p43/xp/next', ['tag @s remove bm.xpk',
                       'execute as @e[type=minecraft:experience_orb,distance=..48,tag=!bm.xpd,nbt={Age:0s}] at @s run function bm:p43/xp/double',
                       'execute as @e[type=minecraft:experience_orb,distance=..48,tag=!bm.xpd,nbt={Age:1s}] at @s run function bm:p43/xp/double'])
    fn('p43/xp/double', ['tag @s add bm.xpd', 'execute store result entity @s Value short 2 run data get entity @s Value',
                         'particle minecraft:happy_villager ~ ~0.2 ~ 0.1 0.1 0.1 0 2'])

    # ---------------- the Hollow Throne's chests refill after each Blood Moon
    G.FUNCS['bloodmoon/start'].append('scoreboard players add #bmn bm.bm 1')
    if 'p2/hollow/dg' in G.FUNCS:
        G.FUNCS['p2/hollow/dg'].insert(1, 'execute unless score @s bm.hbn = #bmn bm.bm run function bm:p43/hollow_refill')
        fn('p43/hollow_refill', ['scoreboard players operation @s bm.hbn = #bmn bm.bm',
                                 'execute as @e[type=minecraft:marker,tag=bm.chestm,tag=bm.d_hollow,distance=..220] at @s run function bm:p2/util/reloot with entity @s data'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def rp(R):
    grid = R.grid
    charm = ['................', '......KKKK......', '.....K....K.....', '.....K....K.....', '......K..K......', '.......KK.......',
             '......KggK......', '.....KgGGgK.....', '....KgGWGGgK....', '....KGGGGGGK....', '....KGGGGGdK....', '.....KGGGdK.....',
             '......KGdK......', '.......KK.......', '................', '................']
    for k, (_, tier, _, col, _, _) in NIGHT.items():
        R.ICONS[f'charm_{k}'] = grid(charm, dict(K=['#2b2b33', '#3a3a50', '#5a2a6a'][tier - 1], g='#e0e0f0', G=col, W='#ffffff', d='#3a3a44'))
    wings = ['................', '................', '.WW..........WW.', 'WWWW........WWWW', 'WWWWW......WWWWW', '.WWWWW....WWWWW.', '.WWWWWW..WWWWWW.',
             '..WWWWWLLWWWWW..', '..WWWWLLLLWWWW..', '...WWWLLLLWWW...', '...WWW.LL.WWW...', '....WW....WW....', '....W......W....', '................',
             '................', '................']
    R.ICONS['charm_wings_angel'] = grid(wings, dict(W='#fff6e0', L='#ffd23f'))
    R.ICONS['charm_wings_evil'] = grid(wings, dict(W='#2a0a12', L='#c83a10'))
    R.ICONS['xp_charm'] = grid(charm, dict(K='#1a3a10', g='#c8ffb0', G='#7cff4a', W='#ffffff', d='#2a5a1a'))
