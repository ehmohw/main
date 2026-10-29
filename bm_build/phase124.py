"""2.75: FIVE MORE RECORDS, and the Hollow's secrets for every newcomer.

THE RECORDS  (original tracks, like the Blood Moon's; each plays in any jukebox)
  The Big Score     - a rare heist find: 1 in 25 won hauls (any tier) has it in the barrel.
  Invasion          - Vorn night: the Overseer drops it half the time; any Vorn trooper, saucer or brute
                      killed by a player during an invasion, now and then.
  Lucky Night       - Lucky Nights only: Jackpot monsters (1 in 10), Lucky Primes (1 in 4), a Lucky mob now and then.
  The Black Market  - Old Barnaby, the pawnbroker, keeps a crate of them: 6 Tokens.
  The Hollow        - in the Hollow Throne: the hidden cache always has one, and the islet chests sometimes.
  Collect all six (with the Blood Moon's) for "Crate Digger".

THE HOLLOW (and every dungeon's hidden cache)
  Wilfrey's Locket was never one-per-world: anyone who has beaten the Hollow King can wake his grave (and the King is
  re-fought every time), and the victor's vaults pay out once per player. The hidden caches were the catch - one chest,
  first come first served (refilled only after a Blood Moon, or a day with nobody there). Now the first time each player
  walks up to a dungeon's hidden cache, it's full for them.
"""
import json, os
from items import item, T, ITEMS
from nbt import snbt

DISCS = {   # key: (title, lore, length s, label palette dark->light, description colour)
    'big_score': ('The Big Score', 'Found in a heist haul, once in a long while.', 100, ('#6a4a08', '#d4a020', '#ffe470'), '#ffcf40'),
    'invasion': ('Invasion', 'Pried off a Vorn on invasion night.', 96, ('#145a1a', '#3ad84a', '#a8ffb0'), '#5ad84a'),
    'lucky': ('Lucky Night', 'Dropped by something lucky on a Lucky Night.', 96, ('#1e6a2a', '#e0b020', '#fff07a'), '#7dff6a'),
    'market': ('The Black Market', "From Old Barnaby's crate of records.", 100, ('#2a1238', '#8a3ab0', '#e0a8ff'), '#c080ff'),
    'hollow': ('The Hollow', 'Hidden in the Hollow Throne.', 104, ('#26344e', '#8aa8d0', '#eef4ff'), '#b8d0f0'),
    'dread': ('The Dread', 'Torn from a Dread boss - its battle, every note of it.', 130, ('#2a0408', '#a01020', '#ff6a6a'), '#e0283a'),    # (2.94g: phase197 drops it)
    'dread2': ('The Dread - Lament', 'Torn from a Dread boss - its last stand.', 128, ('#10101e', '#5a3a7a', '#c8a8e8'), '#a888d0'),    # (2.94h)
    'pxapo': ('The 8-Bit Serpent King', 'Glitched out of an old cartridge - his battle, in sixteen colours.', 96, ('#0a2a12', '#3ad06a', '#b8ffc8'), '#3ad06a'),    # (2.94k: phase215 drops it)
    'sovereign': ('The Dread Sovereign', 'From the ashes of the Dread Sovereign - its three forms, its fall.', 184, ('#14040a', '#8a0a1e', '#ff5a64'), '#d0182e'),    # (2.98: phase238 drops it)
    'vexis': ('Admiral Vexis', 'From the bridge of the Vorn Armada - the Warframe, the Hive-Link, Starfire, and the silence after.', 196, ('#06140a', '#2a8a3a', '#b6ff3c'), '#7aff6a'),    # (2.99: phase242 gives it)
    'aurel': ('Aurel', 'A pale record from the ashes - an elegy for the first light.', 120, ('#3a3220', '#c8b070', '#fff4d0'), '#fff4d0'),    # (2.98: the second fall)
}
MARKET_PRICE = 6
BIG_SCORE = 4                    # % of won hauls
HERE = os.path.dirname(os.path.abspath(__file__))

for k, (ttl, lore, _s, _pal, _c) in DISCS.items():
    item(f'music_disc_{k}', 'minecraft:music_disc_13', 'Music Disc', 'aqua', [(lore, 'gray')],
         model=f'bm:music_disc_{k}', stack=1, cat='misc', comps={'minecraft:jukebox_playable': f'bm:{k}'})


def extend_offers(O, offer):
    O['pawn'].append(offer(('token', MARKET_PRICE), ('music_disc_market', 1)))


def generate(G):
    fn, wjson, tellraw = G.fn, G.wjson, G.tellraw
    loot_entry, chance, KILLED = G.loot_entry, G.chance, G.KILLED
    second = []
    import mig263
    from nbt import to_json

    def add_pools(rel, pools):
        path = G.path('data', *rel.split('/'))
        obj = json.load(open(path))
        obj['pools'] += mig263.convert(rel, to_json(mig263.custom_data_snbt({'type': obj.get('type', 'minecraft:chest'), 'pools': pools})))['pools']
        json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)

    def disc_pool(k, p, *cond):
        return {'rolls': 1, 'entries': [loot_entry(f'music_disc_{k}')], 'conditions': list(cond) + ([chance(p)] if p < 1 else [])}
    # (26.3 has no value_check: the night flags are copied onto every player each second, and the killer's copy is checked)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.ninv dummy', 'scoreboard objectives add bm.nlk dummy']
    G.OBJECTIVES += ['bm.ninv', 'bm.nlk']
    second += ['execute store result score @a bm.ninv run scoreboard players get #inv bm.bm', 'execute store result score @a bm.nlk run scoreboard players get #lnight bm.bm']
    night = lambda obj: {'condition': 'minecraft:entity_scores', 'entity': 'attacker', 'scores': {obj: 1}}

    # ================================================================== the songs
    for k, (ttl, _l, secs, _p, col) in DISCS.items():
        wjson(f'bm/jukebox_song/{k}.json', {'sound_event': {'sound_id': f'bm:music_disc.{k}'}, 'description': T(f'Black Market - {ttl}', 'gray'),
                                           'length_in_seconds': float(secs), 'comparator_output': 15})

    # ================================================================== where they turn up
    # The Big Score: a won heist's haul (the barrel, like phase120's Skiff parts)
    HA, HB = '-200 64 -197', '-198 64 -197'
    wjson('bm/loot_table/p124/big_score.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [loot_entry('music_disc_big_score')]}]})
    hl = G.FUNCS['p70/haul']
    kp = hl.index('function bm:p74/haul_pack')         # (into the barrel before the haul's packed)
    hl[kp:kp] = ['execute store result score #r bm.rng run random value 1..100', f'execute if score #r bm.rng matches ..{BIG_SCORE} run function bm:p124/big_score']
    fn('p124/big_score', [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:p124/big_score',
                          f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:p124/big_score',
                          tellraw('@s', [T('[', 'dark_gray'), T('Haul', '#ffcf40', bold=True), T('] ', 'dark_gray'), T('A record in the loot: ', 'gray'),
                                         T('The Big Score', '#ffcf40', bold=True), T('.', 'gray')])])
    fn('admin/disc_haul', ['function bm:p124/big_score'])
    # Invasion: the Overseer (only ever on invasion nights) half the time; the rank and file, now and then - on invasion nights
    add_pools('bm/loot_table/p32/overseer.json', [disc_pool('invasion', 0.5, KILLED)])
    for m, p in (('trooper', 0.012), ('saucer', 0.05), ('bigslime', 0.04), ('bphantom', 0.03), ('warlord', 0.15), ('abductor', 0.15)):
        add_pools(f'bm/loot_table/p32/{m}.json', [disc_pool('invasion', p, KILLED, night('bm.ninv'))])
    # Lucky Night: Jackpot monsters and Lucky Primes (Lucky Nights only), the odd Lucky mob on a Lucky Night
    for sub, p in (('jackpot', 0.10), ('lucky_prime', 0.25), ('lucky', 0.015)):
        d = G.path('data', 'bm', 'loot_table', 'entities', sub)
        for f in sorted(os.listdir(d)):
            add_pools(f'bm/loot_table/entities/{sub}/{f}', [disc_pool('lucky', p, KILLED, night('bm.nlk'))])
    # The Hollow: the hidden cache (always) and the islets' chests (sometimes)
    if G.PHASE2:
        # (the hidden table also pays out in heists' Hollow rooms - the record only comes out of the real Throne's cache)
        add_pools('bm/loot_table/p2/hollow/hidden.json', [disc_pool('hollow', 1, {'condition': 'minecraft:location_check', 'predicate': {'dimension': 'bm:hollow_throne'}})])
        add_pools('bm/loot_table/p2/hollow/isle.json', [disc_pool('hollow', 0.12)])

    # ================================================================== Crate Digger: all six records
    six = ['blood_moon'] + [k for k in DISCS if k not in ('dread', 'dread2', 'pxapo', 'sovereign', 'aurel', 'vexis')]             # (2.94g: the Dread's record is hard mode's own - not one of the six)
    def icon(iid):
        it = ITEMS[iid]
        return {'id': it['base'], 'components': {'minecraft:item_model': it['comps'].get('minecraft:item_model', it['base'])}}
    wjson('bm/advancement/story/records.json', {
        'display': {'icon': icon('music_disc_hollow'), 'title': T('Crate Digger', 'gold'), 'description': T('Own all six Black Market records', 'gray'),
                    'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': False},
        'parent': 'bm:story/disc',
        'criteria': {k: {'trigger': 'minecraft:inventory_changed', 'conditions': {'items': [{'items': ITEMS[f'music_disc_{k}']['base'],
                         'predicates': {'minecraft:custom_data': snbt({'bm': f'music_disc_{k}'})}}]}} for k in six},
        'requirements': [[k] for k in six]})

    # ================================================================== THE HOLLOW: every newcomer's hidden cache is full
    # (each dungeon's hidden chest has a reloot marker; the first time a player walks up to it, it's refilled unless their
    #  share of the hidden gear is still in it. Once per player per dungeon - after that, the old rules: a Blood Moon or a
    #  quiet day refills it.)
    if G.PHASE2:
        from p2.data import HIDDEN
        second += ['execute as @e[type=minecraft:marker,tag=bm.chestm,tag=!bm.hck] run function bm:p124/hid/tag',
                   'execute as @e[type=minecraft:marker,tag=bm.hidc] at @s if entity @a[distance=..5,gamemode=!spectator] run function bm:p124/hid/near']
        fn('p124/hid/tag', ['tag @s add bm.hck'] + [f'execute if data entity @s {{data:{{loot:"bm:p2/{d}/hidden"}}}} run tag @s add bm.hidc' for d in HIDDEN])
        near = []
        for d, gear in HIDDEN.items():
            near.append(f'execute if entity @s[tag=bm.d_{d}] if entity @a[distance=..5,gamemode=!spectator,tag=!bm.hid_{d}] run function bm:p124/hid/fill_{d}')
            fn(f'p124/hid/fill_{d}', [f'tag @a[distance=..5,gamemode=!spectator] add bm.hid_{d}',
                                      'execute unless block ~ ~ ~ minecraft:chest run return 0',
                                      'execute if data block ~ ~ ~ LootTable run return 0'] +
               [f'execute unless items block ~ ~ ~ container.* *[minecraft:custom_data~{{bm:"{g}"}}] run return run function bm:p124/hid/refill' for g in gear])
        near.append('return 0')
        fn('p124/hid/near', near)
        fn('p124/hid/refill', ['function bm:p2/util/reloot with entity @s data',
                               'particle minecraft:enchant ~ ~0.8 ~ 0.4 0.3 0.4 0.4 30', 'playsound minecraft:block.chest.locked block @a[distance=..8] ~ ~ ~ 0.5 1.6'])
        fn('admin/hidden_forget', [f'tag @s remove bm.hid_{d}' for d in HIDDEN])

    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ====================================================================== resource pack
def icons():
    import vanilla as v
    V, hx = v.V, v._hex
    out = {}
    for k, (_t, _l, _s, pal, _c) in DISCS.items():
        def disc(pal=pal):
            im = v._load(V + 'music_disc_13.png')
            return v.recolor_where(im, lambda c: v._hsv(c)[1] > 0.45, [hx(h) for h in pal])
        out[f'music_disc_{k}'] = disc
    return out


def rp(R):
    import vanilla, shutil
    from PIL import Image
    for k, f in icons().items():
        R.ICONS[k] = Image.new('RGBA', (16, 16))
        vanilla.OVERRIDES[k] = f

    def post(R2):
        sj = R2.p('assets', 'bm', 'sounds.json')
        snd = json.load(open(sj)) if os.path.exists(sj) else {}
        os.makedirs(R2.p('assets', 'bm', 'sounds', 'records'), exist_ok=True)
        for k in DISCS:
            shutil.copy(os.path.join(HERE, 'vendor', f'disc_{k}.ogg'), R2.p('assets', 'bm', 'sounds', 'records', f'{k}.ogg'))
            snd[f'music_disc.{k}'] = {'sounds': [{'name': f'bm:records/{k}', 'stream': True}]}
        R2.wj('assets/bm/sounds.json', snd)
    R.POST.append(post)
