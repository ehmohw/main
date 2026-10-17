"""2.82b: KING OMEGA'S TITHE - the last secret boss makes every currency easy to come by.

While King Omega walks with you (his follower, out):
  THE CUSTOM MOBS you kill - Blood Moon horrors, elites, champions, lucky and jackpot mobs, primes, the aliens (bioengineered,
    Vorn), the Blood Moon's Monstrosity and Herald, the Leprechaun - drop THREE TIMES their currency: Tokens, Medallions,
    Trophies, Blood Crystals, Lucky Tokens and Xenite. (Each currency pool in their loot tables is rolled twice more, only when
    the killer has Omega out - finalize() does it to every such table once all are written; everything else drops as before.)
  EVERY REGULAR MOB you kill (anything else, outside the heists) has a 1% chance to drop one of a Black Market Token, a Blood
    Crystal, a Lucky Token or a Green Xenite shard.
"""
import json
import os
from items import T

ACT = 'bm.omact'                  # (on a player, every second: their King Omega is out)
CURRENCY = ('token', 'medallion', 'trophy', 'blood_crystal', 'lucky_token', 'xenite_green', 'xenite_violet', 'xenite_cyan', 'xenite_red')
# the custom mobs' loot tables (data/bm/loot_table/...): whole folders, and single tables
CUSTOM_DIRS = ('entities/blood', 'entities/elite', 'entities/champion', 'entities/lucky', 'entities/jackpot', 'entities/lucky_prime',
               'entities/prime', 'p32', 'p32/bio')
CUSTOM_FILES = ('entities/monstrosity', 'entities/herald', 'entities/leprechaun', 'entities/lucky_goose')
TITHE = ('token', 'blood_crystal', 'lucky_token', 'xenite_green')
NOT_REGULAR = ('bm.tiered', 'bm.prime', 'bm.npc', 'bm.vorn', 'bm.bio', 'bm.lucky', 'bm.blood', 'bm.elite', 'bm.champion')
OM_C = '#9fb4ff'


def generate(G):
    fn, wjson = G.fn, G.wjson
    # ---- who has him out (the follower is a tamed wolf host, tagged bm.ompet, owned by the player)
    G.FUNCS['loop/second'] += [f'tag @a[tag={ACT}] remove {ACT}',
                               f'execute as @e[type=minecraft:wolf,tag=bm.ompet,tag=!bm.omfade] on owner run tag @s add {ACT}']
    # ---- a regular mob: 1% for a currency
    wjson('bm/advancement/p172/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
        'player': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % ACT}}],
        'entity': [{'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                'predicate': {'minecraft:entity_type': 'minecraft:player'}}}] +
                  [{'condition': 'minecraft:inverted', 'term': {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                                'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % t}}} for t in NOT_REGULAR]}}},
        'rewards': {'function': 'bm:p172/kill'}})
    fn('p172/kill', ['advancement revoke @s only bm:p172/kill', 'execute if dimension bm:gutter run return 0',
                     'execute store result score #om bm.rng run random value 1..100', 'execute unless score #om bm.rng matches 1 run return 0',
                     f'execute store result score #om bm.rng run random value 1..{len(TITHE)}'] +
       [f'execute if score #om bm.rng matches {i + 1} run loot give @s loot bm:items/{c}' for i, c in enumerate(TITHE)] +
       [G.title('@s', 'actionbar', [T('King Omega\'s tithe: ', OM_C, bold=True), T('the dead pay their due.', '#c8d4ff')]),
        'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.8 0.7', 'particle minecraft:soul ~ ~1 ~ 0.3 0.4 0.3 0.02 8'])


def finalize(G):
    """Once every loot table is written: each currency pool of a custom mob's table, twice more for a killer with Omega out."""
    root = G.path('data', 'bm', 'loot_table')
    files = []
    for d in CUSTOM_DIRS:
        p = os.path.join(root, *d.split('/'))
        if os.path.isdir(p): files += [os.path.join(p, f) for f in sorted(os.listdir(p)) if f.endswith('.json')]
    files += [os.path.join(root, *f.split('/')) + '.json' for f in CUSTOM_FILES if os.path.exists(os.path.join(root, *f.split('/')) + '.json')]
    import mig263 as M          # (this runs after the 26.3 migration: write the 26.3 shape - one `condition`, `type`d)
    cond = {'type': 'minecraft:entity_properties', 'entity': 'attacking_player', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % ACT}}
    n_t = n_p = 0
    for f in files:
        with open(f) as h: lt = json.load(h)
        if lt.get('type') != 'minecraft:entity': continue         # (a mob's, not a chest's)
        extra = []
        for pool in lt.get('pools', []):
            ents = pool.get('entries', [])
            if ents and all(is_currency(e) for e in ents):
                for _ in range(2):
                    p2 = json.loads(json.dumps(pool))
                    assert 'conditions' not in p2, f                # (26.2's list shape - the migration should have made it one)
                    p2['condition'] = M.conds(([p2['condition']] if 'condition' in p2 else []) + [cond]); extra.append(p2)
        if extra:
            lt['pools'] += extra; n_t += 1; n_p += len(extra) // 2
            with open(f, 'w') as h: json.dump(lt, h, indent=1, ensure_ascii=False)
    assert n_t >= 100, n_t            # (blood, elite, champion, lucky... each a table per mob type)
    return n_t, n_p


def is_currency(e):
    """an item entry for one of the currencies (its custom_data, SNBT text in the JSON: {bm:"token",...})"""
    if e.get('type') != 'minecraft:item': return False
    s = json.dumps(e)
    return any(f'bm:\\"{c}\\"' in s for c in CURRENCY)
