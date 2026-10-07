"""Phase 2.28: Prof. Whiskerton's tinkering goods - redstone helpers that replace laggy contraptions.

Every machine is a real vanilla block (so redstone, hoppers and pistons treat it normally) with a marker that remembers what
it is. Place one by right-clicking a block face with it; break it like any block and you get the machine back.

- FILTER HOPPER: a hopper that only takes the items shown in item frames on its sides. No frames: an ordinary hopper.
  It looks at the item at the front of the line above (a hopper or chest) or the loose items above, and waits while
  that item isn't on its list - the items it does want flow through with vanilla hopper speed.
- VACUUM HOPPER: pulls loose items within 8 blocks onto itself once a second (off while the hopper is locked by redstone).
- ITEM COMPACTOR: every 5 seconds, gathers loose items and XP within 12 blocks onto itself, where they merge into full
  stacks - far fewer item entities for the server to tick.
- WIRELESS TRANSMITTER / RECEIVER: a redstone lamp and a copper block. While any transmitter is powered, every receiver on
  the same channel becomes a redstone block. The channel is the item's name: rename both in an anvil to the same name.
- REDSTONE CLOCK: pulses (a 1-tick redstone block) every 1-60 seconds; the Tinker's Wrench sets the period.
- BLOCK BREAKER: a dispenser that, when powered, breaks the block in front of it (it drops as if mined).
- BLOCK PLACER: a dropper that, when powered, places the block it drops instead of throwing it.
- SORTING CHEST: tidies itself whenever it's opened - stacks merged, items sorted A to Z.
- LAG LENS: right-click for the entity, item and mob counts in the 3x3 chunks around you.
- TINKER'S WRENCH: right-click a machine to read it (and set a clock: right-click +1 s, sneak -1 s)."""
import json
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt

FN = ['down', 'up', 'north', 'south', 'west', 'east']
OFF_RX, OFF_CLK = 'minecraft:waxed_chiseled_copper', 'minecraft:waxed_oxidized_chiseled_copper'
# kind: (name, colour, icon model, facing rule, the blocks it may be (break check), token price, lore)
KINDS = {
    'filter_hopper': ('Filter Hopper', '#5ad8e6', 'bm:filter_hopper', 'hop', 'minecraft:hopper', 3,
                      ['Only takes the items shown in item frames', 'on its sides. No frames: a normal hopper.']),
    'vacuum_hopper': ('Vacuum Hopper', '#b07cff', 'bm:vacuum_hopper', 'hop', 'minecraft:hopper', 4,
                      ['Pulls loose items within 8 blocks onto', 'itself every second. Redstone switches it off.']),
    'item_compactor': ('Item Compactor', '#e0a050', 'minecraft:waxed_copper_grate', None, 'minecraft:waxed_copper_grate', 4,
                       ['Every 5 s, gathers loose items and XP within', '12 blocks onto itself to merge into full stacks.']),
    'wireless_transmitter': ('Wireless Transmitter', '#ff5a4a', 'minecraft:redstone_lamp', None, 'minecraft:redstone_lamp', 2,
                             ['Power it: every Receiver on its channel', 'turns on. Channel = the item\'s name (anvil).']),
    'wireless_receiver': ('Wireless Receiver', '#ff5a4a', OFF_RX, None, '#bm:p49_rx', 2,
                          ['Becomes a redstone block while a Transmitter', 'on its channel is powered. Rename to pick a channel.']),
    'redstone_clock': ('Redstone Clock', '#ff5a4a', 'minecraft:clock', None, '#bm:p49_clk', 2,
                       ['A redstone pulse every 1-60 seconds', '(1 s to start). Set it with the Tinker\'s Wrench.']),
    'block_breaker': ('Block Breaker', '#c8c8d0', 'minecraft:dispenser', 'look', 'minecraft:dispenser', 4,
                      ['When powered, breaks the block in front', 'of it - it drops as if mined.']),
    'block_placer': ('Block Placer', '#c8c8d0', 'minecraft:dropper', 'look', 'minecraft:dropper', 4,
                     ['A dropper that places the blocks it', 'drops (when the space in front is free).']),
    'scrap_bin': ('Scrap Bin', '#c89060', 'minecraft:barrel', None, 'minecraft:barrel', 3,
                  ['Black Market goods put inside are scrapped', 'for half what they cost (1-Token buys: the Token back).']),
    'sorting_chest': ('Sorting Chest', '#e8c060', 'minecraft:chest', 'horiz', 'minecraft:chest', 3,
                      ['Tidies itself every time it\'s opened:', 'stacks merged, sorted A to Z.']),
}
for k, (name, col, model, _, _, _, lore) in KINDS.items():
    item(k, TOTEM, name, col, lore + [('Right-click a block face to place it.', 'blue'), ('Break it to pick it back up.', 'gray')],
         model=model, stack=16, cat='tinker', glint=model.startswith('minecraft:') or None, comps=hold('none'))
    HOLD[k] = f'bm:p49/place/{k}'
item('lag_lens', TOTEM, 'Lag Lens', '#7dff6a', ['Right-click: entities, items and mobs in', 'the 3x3 chunks around you, and where the crowd is.'],
     model='bm:lag_lens', stack=1, cat='tinker', comps=hold('none'))
HOLD['lag_lens'] = 'bm:p49/lens'
item('tinker_wrench', TOTEM, "Tinker's Wrench", '#c8c8d0', ['Right-click a tinkering block to read it.', ('Redstone Clock: right-click +1 s, sneak -1 s.', 'blue'),
                                                            ('Sorting Chest: sorts it now.', 'blue')],
     model='bm:tinker_wrench', stack=1, cat='tinker', comps=hold('none'))
HOLD['tinker_wrench'] = 'bm:p49/wrench'
PRICES = {k: v[5] for k, v in KINDS.items()} | {'lag_lens': 2, 'tinker_wrench': 1}


def extend_offers(O, offer):
    O['professor'] += [offer(('token', p), (k, 1)) for k, p in PRICES.items() if k != 'scrap_bin']     # (Old Barnaby sells the Scrap Bin)


def _stack_ids():
    d = json.load(open('/home/claude/mc263/item_components.json'))
    by = {}
    for iid, comps in d.items():
        by.setdefault(comps.get('minecraft:max_stack_size', 64), []).append('minecraft:' + iid)
    return by


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    tick, fast, second = [], [], []
    objs = ['bm.rsc dummy', 'bm.rsp dummy', 'bm.rst dummy', 'bm.wl dummy', 'bm.wlw dummy', 'bm.chop minecraft.custom:minecraft.open_chest']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o}' for o in objs]
    G.OBJECTIVES += [o.split()[0] for o in objs]
    wjson('bm/tags/block/p49_open.json', {'values': ['#minecraft:replaceable']})
    wjson('bm/tags/block/p49_rx.json', {'values': [OFF_RX, 'minecraft:redstone_block']})
    wjson('bm/tags/block/p49_clk.json', {'values': [OFF_CLK, 'minecraft:redstone_block']})
    wjson('bm/tags/block/p49_nobreak.json', {'values': ['minecraft:bedrock', 'minecraft:barrier', 'minecraft:command_block', 'minecraft:chain_command_block',
                                                        'minecraft:repeating_command_block', 'minecraft:structure_block', 'minecraft:structure_void', 'minecraft:jigsaw',
                                                        'minecraft:end_portal_frame', 'minecraft:end_portal', 'minecraft:end_gateway', 'minecraft:nether_portal',
                                                        'minecraft:reinforced_deepslate', 'minecraft:light', 'minecraft:spawner', 'minecraft:trial_spawner',
                                                        'minecraft:vault', 'minecraft:moving_piston', 'minecraft:piston_head']})
    wjson('bm/tags/entity_type/p49_frames.json', {'values': ['minecraft:item_frame', 'minecraft:glow_item_frame']})
    wjson('bm/tags/entity_type/p49_loose.json', {'values': ['minecraft:item', 'minecraft:experience_orb']})

    # ================================================================ placing: a ray from the eyes to the first solid block;
    # the machine goes in the open cell in front of it (a hopper points into the block you clicked, like vanilla)
    fn('p49/ray', ['execute positioned ^ ^ ^0.08 unless block ~ ~ ~ #bm:p49_open align xyz positioned ~0.5 ~0.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.p49hit"]}',
                   'execute if entity @e[type=minecraft:marker,tag=bm.p49hit] align xyz positioned ~0.5 ~0.5 ~0.5 run return run function bm:p49/at_cell',
                   'scoreboard players remove #rs bm.rng 1',
                   'execute if score #rs bm.rng matches 1.. positioned ^ ^ ^0.08 run function bm:p49/ray'])
    fn('p49/aim', ['kill @e[type=minecraft:marker,tag=bm.p49hit]', 'scoreboard players set #rs bm.rng 62', 'scoreboard players set #placed bm.rng 0',
                   'execute anchored eyes positioned ^ ^ ^ run function bm:p49/ray', 'kill @e[type=minecraft:marker,tag=bm.p49hit]'])
    fn('p49/at_cell', ['execute positioned ~-0.5 ~-0.5 ~-0.5 if entity @e[type=!#bm:p45_nonmob,dx=0,dy=0,dz=0] run return run ' + say('Something is in the way.'),
                       'execute unless function bm:p35/safe_dig run return run ' + say('The Market\'s wards won\'t let you build here.', 'red'),
                       # facing for hoppers (into the clicked block; never up)
                       'scoreboard players set #hf bm.rng 0'] +
       [f'execute positioned {o} if entity @e[type=minecraft:marker,tag=bm.p49hit,distance=..0.1] run scoreboard players set #hf bm.rng {i}'
        for o, i in (('~ ~ ~-1', 2), ('~ ~ ~1', 3), ('~-1 ~ ~', 4), ('~1 ~ ~', 5))] +
       # facing toward the player (dispensers, droppers: all six; chests: horizontal)
       ['scoreboard players set #lf bm.rng 2', 'execute if entity @s[y_rotation=45..135] run scoreboard players set #lf bm.rng 5',
        'execute if entity @s[y_rotation=135..225] run scoreboard players set #lf bm.rng 3', 'execute if entity @s[y_rotation=-135..-45] run scoreboard players set #lf bm.rng 4',
        'execute if entity @s[y_rotation=-225..-135] run scoreboard players set #lf bm.rng 3',
        'scoreboard players operation #hz bm.rng = #lf bm.rng',
        'execute if entity @s[x_rotation=45..90] run scoreboard players set #lf bm.rng 1', 'execute if entity @s[x_rotation=-90..-45] run scoreboard players set #lf bm.rng 0',
        'function bm:p49/put', 'scoreboard players set #placed bm.rng 1',
        'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
        'playsound minecraft:block.metal.place block @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p49/put', [f'execute if data storage bm:tmp {{rs:{{k:"{k}"}}}} run function bm:p49/put/{k}' for k in KINDS])
    fac = lambda score, blk, extra='': [f'execute if score {score} bm.rng matches {i} run setblock ~ ~ ~ {blk}[facing={f}{extra}]' for i, f in enumerate(FN)
                                        if not (blk == 'minecraft:hopper' and f == 'up') and not (blk == 'minecraft:chest' and f in ('up', 'down'))]
    def marker(k, more=''):
        return [f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.rs","bm.rs_{k}","bm.rsnew"]{more}}}']
    for k, (name, col, _, rule, blk, _, _) in KINDS.items():
        base = {'filter_hopper': 'minecraft:hopper', 'vacuum_hopper': 'minecraft:hopper', 'block_breaker': 'minecraft:dispenser',
                'block_placer': 'minecraft:dropper', 'sorting_chest': 'minecraft:chest', 'scrap_bin': 'minecraft:barrel'}.get(k)
        if rule == 'hop': put = fac('#hf', base)
        elif rule == 'look': put = fac('#lf', base)
        elif rule == 'horiz': put = fac('#hz', base, ',type=single')
        elif k == 'scrap_bin': put = ['setblock ~ ~ ~ minecraft:barrel[facing=up]']
        else: put = [f'setblock ~ ~ ~ {blk if not blk.startswith("#") else (OFF_RX if k == "wireless_receiver" else OFF_CLK)}']
        if base: put.append('data merge block ~ ~ ~ {CustomName:' + snbt(T(name, col)) + '}')
        if k == 'block_breaker':
            put.append('data merge block ~ ~ ~ {lock:{items:"minecraft:barrier",predicates:{"minecraft:custom_data":{bm_lock:1b}}}}')
        put += marker(k)
        if k.startswith('wireless'):
            # the channel is the item's name (unnamed items share the blank channel)
            put += ['data modify entity @e[type=minecraft:marker,tag=bm.rsnew,limit=1] data.ch set value ""',
                    'data modify entity @e[type=minecraft:marker,tag=bm.rsnew,limit=1] data.ch set from entity @s SelectedItem.components."minecraft:custom_name"',
                    'scoreboard players set #wlchg bm.rng 1']
        if k == 'redstone_clock':
            put += ['scoreboard players set @e[type=minecraft:marker,tag=bm.rsnew] bm.rsp 1', 'scoreboard players set @e[type=minecraft:marker,tag=bm.rsnew] bm.rsc 20']
        put.append('tag @e[type=minecraft:marker,tag=bm.rsnew] remove bm.rsnew')
        fn(f'p49/put/{k}', put)
        fn(f'p49/place/{k}', [f'data modify storage bm:tmp rs.k set value "{k}"', 'function bm:p49/aim',
                              'execute if score #placed bm.rng matches 0 run ' + say('Aim at a block face within reach to place it.')])
        # broken (by hand, explosion, piston...): the machine comes back as its item, not as the vanilla block
        vanilla = {'#bm:p49_rx': [OFF_RX, 'minecraft:redstone_block'], '#bm:p49_clk': [OFF_CLK, 'minecraft:redstone_block']}.get(blk, [blk])
        fast.append(f'execute as @e[type=minecraft:marker,tag=bm.rs_{k}] at @s unless block ~ ~ ~ {blk} run function bm:p49/broken/{k}')
        fn(f'p49/broken/{k}', [f'loot spawn ~ ~ ~ loot bm:items/{k}'] +
           [f'execute as @e[type=minecraft:item,distance=..1.6] if items entity @s contents {v} unless items entity @s contents *[minecraft:custom_data] run kill @s' for v in vanilla] +
           ['kill @s'])

    # ================================================================ FILTER HOPPER
    # every second: read the frames on its sides into data.f (item ids)
    second.append('execute as @e[type=minecraft:marker,tag=bm.rs_filter_hopper] at @s run function bm:p49/filter/frames')
    fn('p49/filter/frames', ['data modify entity @s data.f set value []', 'tag @s add bm.fme',
                             'execute as @e[type=#bm:p49_frames,distance=..0.75] if data entity @s Item.id run data modify entity @e[type=minecraft:marker,tag=bm.fme,limit=1] data.f append from entity @s Item.id',
                             'tag @s remove bm.fme'])
    # every tick: if what it would take next isn't on its list, hold its transfer timer (vanilla does the moving)
    tick.append('execute as @e[type=minecraft:marker,tag=bm.rs_filter_hopper] at @s if data entity @s data.f[0] run function bm:p49/filter/tick')
    fn('p49/filter/tick', ['data modify storage bm:tmp flt.f set from entity @s data.f', 'scoreboard players set #bad bm.rng 0',
                           # (a non-container above makes 'data block' fail, so read it into a score instead of testing it)
                           'execute store success score #box bm.rng run data get block ~ ~1 ~ Items[0]',
                           'execute if score #box bm.rng matches 1 run function bm:p49/filter/box',
                           'execute if score #box bm.rng matches 0 positioned ~-0.5 ~0.2 ~-0.5 as @e[type=minecraft:item,dx=0,dy=0.9,dz=0] run function bm:p49/filter/loose',
                           'execute if score #bad bm.rng matches 1 run data modify block ~ ~ ~ TransferCooldown set value 2'])
    fn('p49/filter/box', ['data modify storage bm:tmp flt.id set from block ~ ~1 ~ Items[0].id', 'function bm:p49/filter/test with storage bm:tmp flt'])
    fn('p49/filter/loose', ['data modify storage bm:tmp flt.id set from entity @s Item.id', 'function bm:p49/filter/test with storage bm:tmp flt'])
    fn('p49/filter/test', ['$execute unless data storage bm:tmp {flt:{f:["$(id)"]}} run scoreboard players set #bad bm.rng 1'])

    # ================================================================ VACUUM HOPPER (1 s) and ITEM COMPACTOR (5 s)
    second.append('execute as @e[type=minecraft:marker,tag=bm.rs_vacuum_hopper] at @s if block ~ ~ ~ minecraft:hopper[enabled=true] run function bm:p49/vacuum')
    fn('p49/vacuum', ['execute if entity @e[type=minecraft:item,distance=1.2..8] run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.2 0.3 0.02 6',
                      'tp @e[type=minecraft:item,distance=1.2..8,nbt=!{PickupDelay:32767s}] ~ ~0.9 ~'])
    second += ['scoreboard players add #cmp bm.rng 1', 'execute if score #cmp bm.rng matches 5.. run function bm:p49/compact_all']
    fn('p49/compact_all', ['scoreboard players set #cmp bm.rng 0', 'execute as @e[type=minecraft:marker,tag=bm.rs_item_compactor] at @s run function bm:p49/compact'])
    fn('p49/compact', ['execute if entity @e[type=#bm:p49_loose,distance=1.5..12] run particle minecraft:cloud ~ ~1.1 ~ 0.2 0.1 0.2 0.02 4',
                       'tp @e[type=minecraft:item,distance=1.5..12,nbt=!{PickupDelay:32767s}] ~ ~1.05 ~', 'tp @e[type=minecraft:experience_orb,distance=..12] ~ ~1.05 ~'])

    # ================================================================ WIRELESS: transmitters are watched every tick; receivers are recomputed on a change
    tick += ['execute as @e[type=minecraft:marker,tag=bm.rs_wireless_transmitter] at @s run function bm:p49/wl/tx',
             'execute if score #wlchg bm.rng matches 1 run function bm:p49/wl/all']
    second.append('scoreboard players set #wlchg bm.rng 1')                 # (receivers that load in later catch up within a second)
    fn('p49/wl/tx', ['execute store result score #on bm.rng if block ~ ~ ~ minecraft:redstone_lamp[lit=true]',
                     'execute unless score @s bm.wl = #on bm.rng run scoreboard players set #wlchg bm.rng 1', 'scoreboard players operation @s bm.wl = #on bm.rng'])
    fn('p49/wl/all', ['scoreboard players set #wlchg bm.rng 0', 'scoreboard players set @e[type=minecraft:marker,tag=bm.rs_wireless_receiver] bm.wlw 0',
                      'execute as @e[type=minecraft:marker,tag=bm.rs_wireless_transmitter,scores={bm.wl=1}] run function bm:p49/wl/send',
                      'execute as @e[type=minecraft:marker,tag=bm.rs_wireless_receiver] at @s run function bm:p49/wl/apply'])
    fn('p49/wl/send', ['data modify storage bm:tmp wl.ch set from entity @s data.ch',
                       'execute as @e[type=minecraft:marker,tag=bm.rs_wireless_receiver] run function bm:p49/wl/match'])
    fn('p49/wl/match', ['data modify storage bm:tmp wl.c2 set from storage bm:tmp wl.ch',
                        'execute store success score #d bm.rng run data modify storage bm:tmp wl.c2 set from entity @s data.ch',
                        'execute if score #d bm.rng matches 0 run scoreboard players set @s bm.wlw 1'])
    fn('p49/wl/apply', [f'execute if score @s bm.wlw matches 1 if block ~ ~ ~ {OFF_RX} run setblock ~ ~ ~ minecraft:redstone_block',
                        f'execute if score @s bm.wlw matches 0 if block ~ ~ ~ minecraft:redstone_block run setblock ~ ~ ~ {OFF_RX}'])

    # ================================================================ REDSTONE CLOCK: a 2-tick redstone block every period
    tick += ['scoreboard players remove @e[type=minecraft:marker,tag=bm.rs_redstone_clock] bm.rsc 1',
             'execute as @e[type=minecraft:marker,tag=bm.rs_redstone_clock,scores={bm.rsc=..0}] at @s run function bm:p49/clock/fire']
    fn('p49/clock/fire', ['execute if block ~ ~ ~ minecraft:redstone_block run return run function bm:p49/clock/off',
                          'setblock ~ ~ ~ minecraft:redstone_block', 'scoreboard players set @s bm.rsc 2'])
    fn('p49/clock/off', [f'setblock ~ ~ ~ {OFF_CLK}', 'scoreboard players operation @s bm.rsc = @s bm.rsp', 'scoreboard players operation @s bm.rsc *= #20 bm.rng',
                         'scoreboard players remove @s bm.rsc 2'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #20 bm.rng 20']

    # ================================================================ BLOCK BREAKER / PLACER: on the rising edge of 'triggered'
    for k, b in (('block_breaker', 'dispenser'), ('block_placer', 'dropper')):
        tick.append(f'execute as @e[type=minecraft:marker,tag=bm.rs_{k}] at @s run function bm:p49/{k}/tick')
        fn(f'p49/{k}/tick', [f'execute store result score #t bm.rng if block ~ ~ ~ minecraft:{b}[triggered=true]',
                             f'execute if score #t bm.rng matches 1 unless score @s bm.rst matches 1 run function bm:p49/{k}/fire',
                             'scoreboard players operation @s bm.rst = #t bm.rng'])
    off = {'north': '~ ~ ~-1', 'south': '~ ~ ~1', 'west': '~-1 ~ ~', 'east': '~1 ~ ~', 'up': '~ ~1 ~', 'down': '~ ~-1 ~'}
    fn('p49/block_breaker/fire', [f'execute if block ~ ~ ~ minecraft:dispenser[facing={f}] positioned {o} run function bm:p49/block_breaker/hit' for f, o in off.items()])
    fn('p49/block_breaker/hit', ['execute if block ~ ~ ~ #bm:p49_open run return 0', 'execute if block ~ ~ ~ #bm:p49_nobreak run return 0',
                                 'execute if entity @e[type=minecraft:marker,tag=bm.rs,distance=..0.5] run return 0',
                                 'execute unless function bm:p35/safe_dig run return 0',
                                 'setblock ~ ~ ~ minecraft:air destroy'])
    # the placer lets the dropper drop as usual, then turns the dropped block (one tick later) into a placed one
    fn('p49/block_placer/fire', ['scoreboard players set @s bm.rsc 5'])
    tick += ['scoreboard players remove @e[type=minecraft:marker,tag=bm.rs_block_placer,scores={bm.rsc=1..}] bm.rsc 1',
             'execute as @e[type=minecraft:marker,tag=bm.rs_block_placer,scores={bm.rsc=0}] at @s run function bm:p49/block_placer/catch']
    fn('p49/block_placer/catch', ['scoreboard players set @s bm.rsc -1'] +
       [f'execute if block ~ ~ ~ minecraft:dropper[facing={f}] positioned {o} run function bm:p49/block_placer/front' for f, o in off.items()])
    fn('p49/block_placer/front', ['execute unless block ~ ~ ~ #bm:p49_open run return 0', 'execute unless function bm:p35/safe_dig run return 0',
                                  'execute align xyz positioned ~0.5 ~0.5 ~0.5 as @e[type=minecraft:item,distance=..1.3,sort=nearest,limit=1] run function bm:p49/block_placer/item'])
    fn('p49/block_placer/item', ['execute store result score #age bm.rng run data get entity @s Age', 'execute if score #age bm.rng matches 8.. run return 0',
                                 'data modify storage bm:tmp pl.blk set from entity @s Item.id', 'scoreboard players set #ok bm.rng 0',
                                 'execute at @s align xyz run function bm:p49/block_placer/set with storage bm:tmp pl',
                                 'execute if score #ok bm.rng matches 1 run function bm:p49/block_placer/used'])
    fn('p49/block_placer/set', ['$execute if block ~ ~ ~ #bm:p49_open store success score #ok bm.rng run setblock ~ ~ ~ $(blk)'])
    fn('p49/block_placer/used', ['execute store result score #c bm.rng run data get entity @s Item.count', 'execute if score #c bm.rng matches ..1 run return run kill @s',
                                 'item modify entity @s contents {function:"minecraft:set_count",count:-1,add:true}'])

    # ================================================================ SORTING CHEST: tidies itself when opened
    tick.append('execute as @a[scores={bm.chop=1..}] at @s run function bm:p49/sort/opened')
    fn('p49/sort/opened', ['scoreboard players reset @s bm.chop', 'scoreboard players set #rs bm.rng 70',
                           'execute anchored eyes positioned ^ ^ ^ run function bm:p49/sort/ray'])
    fn('p49/sort/ray', ['execute if block ~ ~ ~ minecraft:chest align xyz positioned ~0.5 ~0.5 ~0.5 run return run execute as @e[type=minecraft:marker,tag=bm.rs_sorting_chest,distance=..0.3,limit=1] at @s run function bm:p49/sort/go',
                        'execute unless block ~ ~ ~ #bm:p49_open run return 0', 'scoreboard players remove #rs bm.rng 1',
                        'execute if score #rs bm.rng matches 1.. positioned ^ ^ ^0.08 run function bm:p49/sort/ray'])
    S = 'storage bm:sort'
    # (load) the item ids that stack to 16 and to 1, and an A-Z rank for every item id
    by = _stack_ids()
    rank = {iid: i for i, iid in enumerate(sorted(v for vs in by.values() for v in vs))}
    G.FUNCS['load'][-1:-1] = [f'data modify {S} s16 set value {json.dumps(by.get(16, []))}', f'data modify {S} s1 set value {json.dumps(by.get(1, []))}',
                              f'data modify {S} rank set value {snbt({k: rank[k] for k in rank})}']
    fn('p49/sort/go', [f'data modify {S} src set from block ~ ~ ~ Items', f'data modify {S} groups set value []',
                       'function bm:p49/sort/group', f'data modify {S} out set value []', 'scoreboard players set #slot bm.rng 0',
                       'function bm:p49/sort/pick', f'data modify block ~ ~ ~ Items set from {S} out',
                       'playsound minecraft:block.chiseled_bookshelf.insert block @a[distance=..8] ~ ~ ~ 0.6 1.4'])
    # 1) group identical items (everything but slot and count), adding up the counts
    fn('p49/sort/group', [f'execute unless data {S} src[0] run return 0', f'data modify {S} key set from {S} src[0]', f'data remove {S} key.Slot',
                          f'data remove {S} key.count', 'scoreboard players set #tot bm.rng 0', f'data modify {S} rest set value []', 'function bm:p49/sort/scan',
                          f'data modify {S} src set from {S} rest', f'data modify {S} g set value {{}}', f'data modify {S} g.key set from {S} key',
                          f'execute store result {S} g.n int 1 run scoreboard players get #tot bm.rng',
                          'scoreboard players set #r bm.rng 99999', f'function bm:p49/sort/rank with {S} key',
                          f'execute store result {S} g.r int 1 run scoreboard players get #r bm.rng',
                          f'data modify {S} groups append from {S} g', 'function bm:p49/sort/group'])
    fn('p49/sort/scan', [f'execute unless data {S} src[0] run return 0', f'data modify {S} cur set from {S} src[0]', f'data remove {S} src[0]',
                         f'data modify {S} ck set from {S} cur', f'data remove {S} ck.Slot', f'data remove {S} ck.count',
                         f'execute store success score #d bm.rng run data modify {S} ck set from {S} key',
                         f'execute if score #d bm.rng matches 0 store result score #c bm.rng run data get {S} cur.count',
                         'execute if score #d bm.rng matches 0 run scoreboard players operation #tot bm.rng += #c bm.rng',
                         f'execute if score #d bm.rng matches 1 run data modify {S} rest append from {S} cur', 'function bm:p49/sort/scan'])
    fn('p49/sort/rank', [f'$execute if data {S} rank."$(id)" store result score #r bm.rng run data get {S} rank."$(id)"'])
    # 2) emit the groups lowest rank first, as full stacks
    fn('p49/sort/pick', [f'execute unless data {S} groups[0] run return 0', 'scoreboard players set #best bm.rng 2147483647', f'data remove {S} best',
                         f'data modify {S} left set value []', f'data modify {S} scan set from {S} groups', 'function bm:p49/sort/find',
                         f'data modify {S} groups set from {S} left', 'function bm:p49/sort/emit', 'function bm:p49/sort/pick'])
    fn('p49/sort/find', [f'execute unless data {S} scan[0] run return 0', f'execute store result score #r bm.rng run data get {S} scan[0].r',
                         'execute store success score #lt bm.rng if score #r bm.rng < #best bm.rng',
                         f'execute if score #lt bm.rng matches 1 if data {S} best.key run data modify {S} left append from {S} best',
                         f'execute if score #lt bm.rng matches 1 run data modify {S} best set from {S} scan[0]',
                         'execute if score #lt bm.rng matches 1 run scoreboard players operation #best bm.rng = #r bm.rng',
                         f'execute if score #lt bm.rng matches 0 run data modify {S} left append from {S} scan[0]',
                         f'data remove {S} scan[0]', 'function bm:p49/sort/find'])
    fn('p49/sort/emit', [f'execute store result score #tot bm.rng run data get {S} best.n', 'scoreboard players set #max bm.rng 64',
                         f'function bm:p49/sort/max with {S} best.key',
                         f'execute if data {S} best.key.components."minecraft:max_stack_size" store result score #max bm.rng run data get {S} best.key.components."minecraft:max_stack_size"',
                         'function bm:p49/sort/stacks', f'data remove {S} best'])
    fn('p49/sort/max', [f'$execute if data {S} {{s16:["$(id)"]}} run scoreboard players set #max bm.rng 16',
                        f'$execute if data {S} {{s1:["$(id)"]}} run scoreboard players set #max bm.rng 1'])
    fn('p49/sort/stacks', ['execute if score #tot bm.rng matches ..0 run return 0', 'scoreboard players operation #n bm.rng = #tot bm.rng',
                           'scoreboard players operation #n bm.rng < #max bm.rng', 'scoreboard players operation #tot bm.rng -= #n bm.rng',
                           f'data modify {S} el set from {S} best.key', f'execute store result {S} el.count int 1 run scoreboard players get #n bm.rng',
                           f'execute store result {S} el.Slot byte 1 run scoreboard players get #slot bm.rng',
                           f'execute if score #slot bm.rng matches ..26 run data modify {S} out append from {S} el',
                           'execute if score #slot bm.rng matches 27.. run function bm:p49/sort/spill', 'scoreboard players add #slot bm.rng 1',
                           'function bm:p49/sort/stacks'])
    fn('p49/sort/spill', ['summon minecraft:item ~ ~1 ~ {Item:{id:"minecraft:stone",count:1},Tags:["bm.spill"]}', f'data remove {S} el.Slot',
                          f'data modify entity @e[type=minecraft:item,tag=bm.spill,limit=1,sort=nearest] Item set from {S} el', 'tag @e[tag=bm.spill] remove bm.spill'])

    # ================================================================ TINKER'S WRENCH (reads a machine; sets clocks; sorts a chest)
    fn('p49/wrench', ['kill @e[type=minecraft:marker,tag=bm.p49hit]', 'scoreboard players set #rs bm.rng 62', 'scoreboard players set #wr bm.rng 0',
                      'execute anchored eyes positioned ^ ^ ^ run function bm:p49/wray', 'kill @e[type=minecraft:marker,tag=bm.p49hit]',
                      'execute if score #wr bm.rng matches 0 run ' + say('That isn\'t a tinkering block.')])
    fn('p49/wray', ['execute unless block ~ ~ ~ #bm:p49_open align xyz positioned ~0.5 ~0.5 ~0.5 run return run function bm:p49/wfound',
                    'scoreboard players remove #rs bm.rng 1', 'execute if score #rs bm.rng matches 1.. positioned ^ ^ ^0.08 run function bm:p49/wray'])
    fn('p49/wfound', ['tag @s add bm.wrme', 'execute as @e[type=minecraft:marker,tag=bm.rs,distance=..0.3,limit=1] at @s run function bm:p49/wread', 'tag @s remove bm.wrme'])
    me = '@a[tag=bm.wrme,limit=1]'
    sw = lambda parts: title(me, 'actionbar', parts)
    fn('p49/wread', ['scoreboard players set #wr bm.rng 1',
                     'execute if entity @s[tag=bm.rs_redstone_clock] run return run function bm:p49/wclock',
                     'execute if entity @s[tag=bm.rs_sorting_chest] run function bm:p49/sort/go',
                     'execute if entity @s[tag=bm.rs_sorting_chest] run return run ' + sw(T('Sorted.', '#e8c060')),
                     'execute if entity @s[tag=bm.rs_filter_hopper] unless data entity @s data.f[0] run return run ' + sw(T('Filter Hopper: no item frames - takes anything.', '#5ad8e6')),
                     'execute if entity @s[tag=bm.rs_filter_hopper] run return run ' + sw([T('Filter Hopper takes only: ', '#5ad8e6'), {'entity': '@s', 'nbt': 'data.f[]', 'separator': ', ', 'color': 'white'}]),
                     'execute if entity @s[tag=bm.rs_wireless_transmitter] run return run ' + sw([T('Transmitter - channel: ', '#ff5a4a'), {'entity': '@s', 'nbt': 'data.ch', 'interpret': True, 'color': 'white'},
                                                                                                   T('  (powered: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.wl'}, 'color': 'white'}, T(')', 'gray')]),
                     'execute if entity @s[tag=bm.rs_wireless_receiver] run return run ' + sw([T('Receiver - channel: ', '#ff5a4a'), {'entity': '@s', 'nbt': 'data.ch', 'interpret': True, 'color': 'white'},
                                                                                                T('  (on: ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.wlw'}, 'color': 'white'}, T(')', 'gray')]),
                     'execute if entity @s[tag=bm.rs_vacuum_hopper] run return run ' + sw(T('Vacuum Hopper: pulls loose items within 8 blocks (off while locked by redstone).', '#b07cff')),
                     'execute if entity @s[tag=bm.rs_item_compactor] run return run ' + sw(T('Item Compactor: gathers loose items and XP within 12 blocks every 5 s.', '#e0a050')),
                     'execute if entity @s[tag=bm.rs_block_breaker] run return run ' + sw(T('Block Breaker: breaks the block in front when powered.', '#c8c8d0')),
                     'execute if entity @s[tag=bm.rs_block_placer] run return run ' + sw(T('Block Placer: places the blocks it drops when powered.', '#c8c8d0'))])
    fn('p49/wclock', ['execute if entity @a[tag=bm.wrme,predicate=bm:p20/sneaking] run scoreboard players remove @s bm.rsp 1',
                      'execute unless entity @a[tag=bm.wrme,predicate=bm:p20/sneaking] run scoreboard players add @s bm.rsp 1',
                      'execute if score @s bm.rsp matches 61.. run scoreboard players set @s bm.rsp 1', 'execute if score @s bm.rsp matches ..0 run scoreboard players set @s bm.rsp 60',
                      'playsound minecraft:block.lever.click block @a[distance=..8] ~ ~ ~ 0.6 1.6',
                      sw([T('Redstone Clock: a pulse every ', '#ff5a4a'), {'score': {'name': '@s', 'objective': 'bm.rsp'}, 'color': 'white', 'bold': True}, T(' s', '#ff5a4a')])])

    # ================================================================ LAG LENS: counts in the 3x3 chunks around you
    fn('p49/lens', ['execute store result score #cx bm.rng run data get entity @s Pos[0]', 'execute store result score #cz bm.rng run data get entity @s Pos[2]',
                    'scoreboard players set #16 bm.rng 16', 'scoreboard players operation #cx bm.rng /= #16 bm.rng', 'scoreboard players operation #cz bm.rng /= #16 bm.rng',
                    'scoreboard players operation #cx bm.rng *= #16 bm.rng', 'scoreboard players operation #cz bm.rng *= #16 bm.rng',
                    tellraw('@s', [T('— Lag Lens —', '#7dff6a', bold=True), T('  entities (items) per chunk, north at the top; yours in the middle', 'gray')])] +
       [f'function bm:p49/lens_row {{dz:{dz}}}' for dz in (-16, 0, 16)] +
       ['execute store result score #all bm.rng if entity @e', 'execute store result score #ai bm.rng if entity @e[type=minecraft:item]',
        tellraw('@s', [T('Loaded in this dimension: ', 'gray'), {'score': {'name': '#all', 'objective': 'bm.rng'}, 'color': 'white'}, T(' entities, ', 'gray'),
                       {'score': {'name': '#ai', 'objective': 'bm.rng'}, 'color': 'white'}, T(' of them dropped items.', 'gray')]),
        'playsound minecraft:item.spyglass.use player @s ~ ~ ~ 1 1.4'])
    fn('p49/lens_row', ['$scoreboard players set #dz bm.rng $(dz)'] +
       [f'function bm:p49/lens_cell {{dx:{dx},i:{i}}}' for i, dx in enumerate((-16, 0, 16))] +
       [tellraw('@s', sum(([T('  [', 'dark_gray'), {'score': {'name': f'#e{i}', 'objective': 'bm.rng'}, 'color': 'white', 'bold': i == 1},
                            T(' (', 'gray'), {'score': {'name': f'#i{i}', 'objective': 'bm.rng'}, 'color': 'yellow'}, T(')', 'gray'), T(']', 'dark_gray')]
                           for i in range(3)), []))])
    fn('p49/lens_cell', ['$scoreboard players set #dx bm.rng $(dx)', 'scoreboard players operation #x bm.rng = #cx bm.rng', 'scoreboard players operation #x bm.rng += #dx bm.rng',
                         'scoreboard players operation #z bm.rng = #cz bm.rng', 'scoreboard players operation #z bm.rng += #dz bm.rng',
                         'execute store result storage bm:tmp lens.x int 1 run scoreboard players get #x bm.rng',
                         'execute store result storage bm:tmp lens.z int 1 run scoreboard players get #z bm.rng',
                         '$data modify storage bm:tmp lens.i set value $(i)', 'function bm:p49/lens_count with storage bm:tmp lens'])
    fn('p49/lens_count', ['$execute positioned $(x) -64 $(z) store result score #e$(i) bm.rng if entity @e[dx=15,dy=383,dz=15]',
                          '$execute positioned $(x) -64 $(z) store result score #i$(i) bm.rng if entity @e[type=minecraft:item,dx=15,dy=383,dz=15]'])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


# ===================================================================== resource pack (2D icons for the hoppers, the lens and the wrench)
def icons():
    import vanilla as v
    from PIL import Image
    hx = v._hex

    def hopper(tint):
        im = v._load(v.V + 'hopper.png')
        r = v.ramp(tint, 5, 2)
        px = im.load()
        for y in range(16):
            for x in range(16):
                c = px[x, y]
                if c[3] and 4 <= y <= 6: px[x, y] = r[min(4, max(0, round(v._lum(c) / 255 * 4)))]   # a coloured band round the bowl
        return im

    def lens():
        im = Image.new('RGBA', (16, 16)); rim = v.ramp('#5a8a40', 4, 1); gl = v.ramp('#9af07a', 4, 2); h = v.ramp('#6a4a2a', 3, 1)
        for y in range(16):
            for x in range(16):
                d = ((x - 9.5) ** 2 + (y - 6.5) ** 2) ** 0.5
                if d <= 5.2: im.putpixel((x, y), rim[1] if d > 4.1 else gl[min(3, max(0, round(2 - ((x - 9.5) + (y - 6.5)) / 4)))])
                elif d <= 5.9: im.putpixel((x, y), rim[0])
        for i, (x, y) in enumerate(((5, 10), (4, 11), (3, 12), (2, 13), (1, 14))):
            im.putpixel((x, y), h[2] if i % 2 else h[1]); im.putpixel((x + 1, y), h[0])
        for (x, y) in ((8, 4), (9, 3), (7, 5)): im.putpixel((x, y), (240, 255, 235, 255))
        return im

    def wrench():
        im = Image.new('RGBA', (16, 16)); s = v.ramp('#b8bcc4', 5, 2); k = hx('#2a2c30')
        rows = ['..........KKK...', '.........KsssK..', '........KssKsK..', '........KsK.KK..', '........KssK....', '.......KssK.....',
                '......KssK......', '.....KssK.......', '....KssK........', '...KssK.........', '..KKssK.........', '.KssKK..........',
                '.KsK............', '.KK.............', '................', '................']
        for y, r in enumerate(rows):
            for x, ch in enumerate(r):
                if ch == 'K': im.putpixel((x, y), k)
                elif ch == 's': im.putpixel((x, y), s[3] if (x + y) % 3 else s[4])
        return im
    return {'filter_hopper': lambda: hopper('#3ab8c8'), 'vacuum_hopper': lambda: hopper('#8a5ad8'), 'lag_lens': lens, 'tinker_wrench': wrench}


def rp(R):
    import vanilla
    from PIL import Image
    for k, f in icons().items():
        R.ICONS[k] = Image.new('RGBA', (16, 16))
        vanilla.OVERRIDES[k] = f
    R.HANDHELD_EXTRA.add('tinker_wrench')
