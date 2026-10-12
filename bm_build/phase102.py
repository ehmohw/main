"""2.67c: CARRYING ON - straight into the next heist, the haul unpacked there and then.

CARRY ON (the leader starts a new raid, or you opt in to one) and the Fixer unpacks your haul on the spot - the crate in
  your pack, and any you've set down:
  - BLACK MARKET TOKENS stay on you (they pay the next fee). No room in your pack: into your locker; no room there either:
    into your Gutter Bank as coins (32 a Token - buy them back at the bank any time).
  - GUTTER COINS, Gutter Medallions and Gutter Trophies go into your Gutter Bank as coins; spoils into it as spoils.
  - EVERYTHING ELSE goes into your Locker Hall bays - and into your pack once they're full (or if you keep none).
  - Your bays and your pack both full: the Fixer SCRAPS the rest for Gutter Coins, into your bank - and warns you. (Heist
    goods fetch their Scrap Box price; Black Market currency its worth in Tokens at 32 coins a Token; a few rare vanilla
    goods a fair price; anything else a coin a stack.)
  Head home instead and the haul comes home with you as a crate, as ever.
"""
from items import T, ITEMS
from nbt import snbt, Int
import phase28 as P28
import phase72 as P72
import phase80 as P80
import phase84 as P84

GOLD = '#ffcf40'
GUT = '#c8a050'
LOCK = '#c89a5a'
SLOTS = 36                                   # a pack: hotbar + inventory (container.0-35)
CUSTOM_DEFAULT = 4                           # scrap: a heist find with no Scrap Box price, a piece
VANILLA = {'diamond': 12, 'emerald': 3, 'netherite_scrap': 16, 'ancient_debris': 16, 'netherite_ingot': 64, 'golden_apple': 6,
           'enchanted_golden_apple': 12, 'totem_of_undying': 16, 'ender_pearl': 3, 'experience_bottle': 1, 'blaze_rod': 1,
           'gold_ingot': 1, 'enchanted_book': 4, 'golden_carrot': 1}            # scrap: a piece (anything else vanilla: a coin a stack)


def generate(G):
    fn, tellraw = G.fn, G.tellraw
    P = [T('[', 'dark_gray'), T('Vault', GOLD, bold=True), T('] ', 'dark_gray')]
    STAGE = P72.STAGE
    TC = P80.TOKEN_COINS
    S = 'storage bm:up'
    bank_worth = {'gutter_coin': 1, 'gutter_medallion': 16, 'gutter_trophy': 128}
    spoil_ix = {m[0]: i for i, m in enumerate(P80.MATS, 1)}
    cur = {k: v * TC for k, v in P28.VALUE.items() if k in ITEMS}
    G.FUNCS['load'][-1:-1] = [f'data modify {S} bank set value {snbt({k: Int(v) for k, v in bank_worth.items()})}',
                              f'data modify {S} sp set value {snbt({k: Int(v) for k, v in spoil_ix.items()})}',
                              f'data modify {S} cur set value {snbt({k: Int(v) for k, v in cur.items()})}',
                              f'data modify {S} mc set value {snbt({"minecraft:" + k: Int(v) for k, v in VANILLA.items()})}']
    num = lambda o: {'score': {'name': o, 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}
    one = [f'data modify {S} one set value []', f'data modify {S} one append from {S} it']
    is_tok = f'{S} one[{{components:{{"minecraft:custom_data":{{bm:"token"}}}}}}]'
    haul = '*[minecraft:custom_data~{bm_haul:1b}]'
    tok = '*[minecraft:custom_data~{bm:"token"}]'

    # ================================================================== (as a player carrying on) unpack every haul of theirs
    fn('p102/unpack', ['execute unless dimension bm:gutter run return 0', 'function bm:p80/init_me', 'scoreboard players operation #me bm.rng = @s bm.pid',
                       f'data modify {S} all set value []', f'data modify {S} rest set value []',
                       f'data modify {S} all append from entity @s Inventory[{{components:{{"minecraft:custom_data":{{bm_haul:1b}}}}}}].components."minecraft:container"[].item',
                       f'execute if items entity @s weapon.offhand {haul} run data modify {S} all append from entity @s equipment.offhand.components."minecraft:container"[].item',
                       f'clear @s {haul}',
                       'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.haulm,distance=0..] if score @s bm.pid = #me bm.rng at @s run function bm:p102/grab_set',
                       f'execute unless data {S} all[0] run return 0'] +
       [f'scoreboard players set {o} bm.rng 0' for o in ('#utk', '#ubc', '#usp', '#ulk', '#upk', '#usn', '#usc', '#uov', '#utb')] +
       ['function bm:p102/sort', 'function bm:p102/tokens', 'execute in bm:gutter run function bm:p72/bag/stage', 'function bm:p102/place',
        'function bm:p102/tell', 'playsound minecraft:block.barrel.open player @s ~ ~ ~ 0.8 1.1'])
    # (a haul set down: what's left in it comes along; the crate goes)
    fn('p102/grab_set', [f'execute if block ~ ~ ~ minecraft:barrel run data modify {S} all append from block ~ ~ ~ Items[]',
                         'execute if block ~ ~ ~ minecraft:barrel run data modify block ~ ~ ~ Items set value []',
                         'execute if block ~ ~ ~ minecraft:barrel run setblock ~ ~ ~ minecraft:air', 'particle minecraft:poof ~ ~ ~ 0.3 0.3 0.3 0.02 8', 'kill @s'])

    # ---- one pass: Tokens counted; coins and spoils banked; the rest set aside
    fn('p102/sort', [f'execute unless data {S} all[0] run return 0', f'data modify {S} it set from {S} all[0]', f'data remove {S} all[0]', f'data remove {S} it.Slot',
                     f'execute store result score #n bm.rng run data get {S} it.count', f'execute unless data {S} it.count run scoreboard players set #n bm.rng 1'] + one +
       [f'execute if data {is_tok} run scoreboard players operation #utk bm.rng += #n bm.rng', f'execute if data {is_tok} run return run function bm:p102/sort',
        f'data remove {S} k', 'scoreboard players set #w bm.rng 0', 'scoreboard players set #sp bm.rng 0',
        f'execute if data {S} it.components."minecraft:custom_data".bm run data modify {S} k.id set from {S} it.components."minecraft:custom_data".bm',
        f'execute if data {S} k.id run function bm:p102/look with {S} k',
        'execute if score #w bm.rng matches 1.. run function bm:p102/to_bank', 'execute if score #w bm.rng matches 1.. run return run function bm:p102/sort',
        'execute if score #sp bm.rng matches 1.. run function bm:p102/to_spoil', 'execute if score #sp bm.rng matches 1.. run return run function bm:p102/sort',
        f'data modify {S} rest append from {S} it', 'function bm:p102/sort'])
    fn('p102/look', [f'$execute store result score #w bm.rng run data get {S} bank."$(id)"', f'$execute store result score #sp bm.rng run data get {S} sp."$(id)"'])
    fn('p102/to_bank', ['scoreboard players operation #n bm.rng *= #w bm.rng', 'scoreboard players operation @s bm.gbc += #n bm.rng',
                        'scoreboard players operation #ubc bm.rng += #n bm.rng'])
    fn('p102/to_spoil', [f'execute if score #sp bm.rng matches {i} run scoreboard players operation @s bm.gb{i} += #n bm.rng' for i in spoil_ix.values()] +
       ['scoreboard players operation #usp bm.rng += #n bm.rng'])

    # ---- Tokens: as many as the pack holds (a stack of 64 a free slot, topping up the stacks there); the rest to the locker, else banked at 32 coins each
    cap = ['scoreboard players set #cap bm.rng 0']
    for n in range(SLOTS):
        cap += [f'execute unless items entity @s container.{n} * run scoreboard players add #cap bm.rng 64',
                f'execute if items entity @s container.{n} {tok} store result score #c bm.rng run data get entity @s Inventory[{{Slot:{n}b}}].count',
                f'execute if items entity @s container.{n} {tok} run scoreboard players add #cap bm.rng 64',
                f'execute if items entity @s container.{n} {tok} run scoreboard players operation #cap bm.rng -= #c bm.rng']
    fn('p102/cap', cap)
    fn('p102/tokens', ['execute if score #utk bm.rng matches ..0 run return 0', 'function bm:p102/cap',
                       'scoreboard players operation #ptk bm.rng = #utk bm.rng', 'scoreboard players operation #ptk bm.rng < #cap bm.rng',
                       'execute if score #ptk bm.rng matches 1.. run loot give @s loot bm:p75/prize_tokens',
                       'scoreboard players operation #uov bm.rng = #utk bm.rng', 'scoreboard players operation #uov bm.rng -= #ptk bm.rng',
                       'execute if score #uov bm.rng matches 1.. in bm:gutter run function bm:p72/bag/stage', 'execute if score #uov bm.rng matches 1.. run function bm:p102/tok_over'])
    fn('p102/tok_over', ['execute if score #uov bm.rng matches ..0 run return 0', 'scoreboard players set #ptk bm.rng 64', 'scoreboard players operation #ptk bm.rng < #uov bm.rng',
                         f'execute in bm:gutter run data modify block {STAGE} Items set value []', f'execute in bm:gutter run loot replace block {STAGE} container.0 loot bm:p75/prize_tokens',
                         'execute store result score #ok bm.rng run function bm:p102/lk/put',
                         'execute if score #ok bm.rng matches 0 run return run function bm:p102/tok_bank',
                         'scoreboard players operation #uov bm.rng -= #ptk bm.rng', 'scoreboard players operation #utk bm.rng -= #ptk bm.rng',
                         'scoreboard players add #ulk bm.rng 1', 'function bm:p102/tok_over'])
    fn('p102/tok_bank', ['scoreboard players operation #utk bm.rng -= #uov bm.rng', 'scoreboard players operation #utb bm.rng = #uov bm.rng', f'scoreboard players set #w bm.rng {TC}',
                         'scoreboard players operation #c bm.rng = #uov bm.rng', 'scoreboard players operation #c bm.rng *= #w bm.rng',
                         'scoreboard players operation @s bm.gbc += #c bm.rng', 'scoreboard players operation #ubc bm.rng += #c bm.rng'])

    # ---- the rest, a stack at a time: the locker, then the pack, then the scrap heap
    fn('p102/place', [f'execute unless data {S} rest[0] run return 0', f'data modify {S} it set from {S} rest[0]', f'data remove {S} rest[0]',
                      f'data modify {S} it.Slot set value 0b', f'execute in bm:gutter run data modify block {STAGE} Items set value []',
                      f'execute in bm:gutter run data modify block {STAGE} Items append from {S} it',
                      'execute store result score #ok bm.rng run function bm:p102/lk/put', 'execute if score #ok bm.rng matches 1 run scoreboard players add #ulk bm.rng 1',
                      'execute if score #ok bm.rng matches 0 store result score #ok bm.rng run function bm:p102/pk/put',
                      'execute if score #ok bm.rng matches 1 run scoreboard players add #upk bm.rng 1',
                      'execute if score #ok bm.rng matches 0 run function bm:p102/scrap', 'function bm:p102/place'])
    # (the pack: the first empty slot)
    fn('p102/pk/put', ['scoreboard players set #pok bm.rng 0'] +
       [f'execute if score #pok bm.rng matches 0 unless items entity @s container.{n} * in bm:gutter store success score #pok bm.rng run item replace entity @s container.{n} from block {STAGE} container.0'
        for n in range(SLOTS)] + ['return run scoreboard players get #pok bm.rng'])
    # (the locker: the first empty slot in any bay of theirs)
    B_ = P84.bays()
    fn('p102/lk/put', ['scoreboard players set #lok bm.rng 0',
                       'execute as @e[type=minecraft:interaction,tag=bm.lkb] if score #lok bm.rng matches 0 if score @s bm.lko = #me bm.rng run function bm:p102/lk/bay',
                       'return run scoreboard players get #lok bm.rng'])
    fn('p102/lk/bay', [f'execute if score @s bm.lkn matches {n} run return run function bm:p102/lk/b{n}' for n, *_r in B_])
    for n, cells, _p in B_:
        bl = []
        for j, (cx, cy, cz, st) in enumerate(cells):
            bl += [f'execute if score #lok bm.rng matches 0 in bm:gutter store result score #c bm.rng run data get block {cx} {cy} {cz} Items',
                   f'execute if score #lok bm.rng matches 0 if score #c bm.rng matches ..26 run function bm:p102/lk/c{n}_{j}']
            fn(f'p102/lk/c{n}_{j}', [f'execute if score #lok bm.rng matches 0 in bm:gutter unless items block {cx} {cy} {cz} container.{k} * '
                                     f'store success score #lok bm.rng run item replace block {cx} {cy} {cz} container.{k} from block {STAGE} container.0' for k in range(27)])
        fn(f'p102/lk/b{n}', bl)
    # (the scrap heap: its Scrap Box price, its worth in Tokens, a rare vanilla good's price - or a coin a stack - into the bank)
    fn('p102/scrap', ['scoreboard players set #v bm.rng 0', f'execute store result score #n bm.rng run data get {S} it.count',
                      f'execute unless data {S} it.count run scoreboard players set #n bm.rng 1', f'data remove {S} k',
                      f'execute if data {S} it.components."minecraft:custom_data".bm run data modify {S} k.id set from {S} it.components."minecraft:custom_data".bm',
                      f'execute if data {S} k.id run function bm:p102/sv_bm with {S} k',
                      f'execute if data {S} k.id if score #v bm.rng matches ..0 run scoreboard players set #v bm.rng {CUSTOM_DEFAULT}',
                      f'execute unless data {S} k.id run data modify {S} k.id set from {S} it.id',
                      f'execute unless data {S} it.components."minecraft:custom_data".bm run function bm:p102/sv_mc with {S} k',
                      'scoreboard players operation #v bm.rng *= #n bm.rng', 'execute if score #v bm.rng matches ..0 run scoreboard players set #v bm.rng 1',
                      'scoreboard players operation @s bm.gbc += #v bm.rng', 'scoreboard players operation #usc bm.rng += #v bm.rng', 'scoreboard players add #usn bm.rng 1'])
    fn('p102/sv_bm', ['$execute store result score #v bm.rng run data get storage bm:gsc t."$(id)"',
                      f'$execute if score #v bm.rng matches ..0 store result score #v bm.rng run data get {S} cur."$(id)"'])
    fn('p102/sv_mc', [f'$execute store result score #v bm.rng run data get {S} mc."$(id)"'])

    # ---- what happened to it all
    fn('p102/tell', [tellraw('@s', P + [T('The Fixer unpacks your haul.', GOLD)]),
                     'execute if score #utk bm.rng matches 1.. run ' + tellraw('@s', [T('  Tokens on you: ', 'gray'), num('#utk')]),
                     'execute if score #ubc bm.rng matches 1.. run ' + tellraw('@s', [T('  Into your Gutter Bank: ', 'gray'), num('#ubc'), T(' coins', GUT)]),
                     'execute if score #usp bm.rng matches 1.. run ' + tellraw('@s', [T('  ...and ', 'gray'), num('#usp'), T(' spoils', GUT)]),
                     'execute if score #ulk bm.rng matches 1.. run ' + tellraw('@s', [T('  Into your locker: ', 'gray'), num('#ulk'), T(' stack(s)', LOCK)]),
                     'execute if score #upk bm.rng matches 1.. run ' + tellraw('@s', [T('  Into your pack: ', 'gray'), num('#upk'), T(' stack(s)', 'white')]),
                     'execute if score #utb bm.rng matches 1.. run ' + tellraw('@s', [T('  No room for ', 'red'), num('#utb'),
                                                                                                                 T(' Tokens - banked as coins (32 each; buy them back at the bank).', 'red')]),
                     'execute if score #usn bm.rng matches 1.. run ' + tellraw('@s', P + [T('Your locker and your pack are full! ', 'red', bold=True), T('The Fixer scrapped ', 'red'),
                                                                                        num('#usn'), T(' stack(s) for ', 'red'), num('#usc'),
                                                                                        T(' Gutter Coins - in your bank. Make some room before the next one.', 'red')]),
                     'execute if score #usn bm.rng matches 1.. run playsound minecraft:block.grindstone.use player @s ~ ~ ~ 0.8 1.1',
                     'scoreboard players set #bays bm.rng 0',
                     'execute as @e[type=minecraft:interaction,tag=bm.lkb] if score @s bm.lko = #me bm.rng run scoreboard players add #bays bm.rng 1',
                     'execute if score #bays bm.rng matches 0 if score #upk bm.rng matches 1.. run ' + tellraw('@s', [T('  (Claim a bay in the Locker Hall - your Fixer\'s Ledger takes '
                                                                                                                       'you there - and your finds go into it.)', 'dark_gray')])])
