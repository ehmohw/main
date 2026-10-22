"""Hold-to-use items (2.13): right-clicking starts "using" the item (a consumable that never finishes), and the
`using_item` advancement trigger fires on that first tick. Unlike the older consume trick, the item is never used up,
so it keeps its data (stored XP, contents, charges, enchantments, damage) and nothing has to be handed back.

    from useitem import hold, HOLD
    item(..., comps=hold())                  # the item's components
    HOLD['my_item'] = 'bm:p33/my_item/use'   # run (as and at the player) once per press

`use_effects` keeps the player at full speed while the button is held. One press = one action: the trigger fires every
tick the button is held, and the wrapper ignores ticks that follow straight on from the last one."""

HOLD = {}       # iid -> function run once per press
GB = []         # 2.78: item arguments handed back a tick after their consumable is used up (give_back)
HOLD_REPEAT = {}  # iid -> function run EVERY tick the button is held (#first bm.hnow = 1 on the first tick of a press) - 2.14


def hold(anim='none', extra=None):
    c = {'minecraft:consumable': {'consume_seconds': 100000.0, 'animation': anim, 'sound': 'minecraft:intentionally_empty',
                                  'has_consume_particles': False},
         'minecraft:use_effects': {'can_sprint': True, 'speed_multiplier': 1.0, 'interact_vibrations': False}}
    if extra: c.update(extra)
    return c


def give_back(item_arg):
    """2.78: lines for a consume-advancement function whose item is "never used up": the item comes back a tick later. (In 26.3
    the consume_item advancement fires BEFORE the used item is taken from the hand - a give-back done at once still sees it
    there, gives nothing, and then the item is gone: the Warpstone, Wilfrey's locket, the Blink Tome, the lucky map pieces and
    the raid kit's abilities all vanished after one use.) Into the main hand if it's empty, else the off hand, else the pack."""
    if item_arg not in GB: GB.append(item_arg)
    return [f'scoreboard players set @s bm.gbi {GB.index(item_arg) + 1}', 'tag @s add bm.gb']


def generate(G):
    from items import ITEMS
    fn, wjson = G.fn, G.wjson
    G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.huse dummy', 'scoreboard objectives add bm.hnow dummy']
    G.OBJECTIVES += ['bm.huse', 'bm.hnow']
    if GB:
        G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.gbi dummy']
        G.OBJECTIVES += ['bm.gbi']
        G.FUNCS['tick'].append('execute as @a[tag=bm.gb] run function bm:gb/back')
        fn('gb/back', ['tag @s remove bm.gb'] + [f'execute if score @s bm.gbi matches {n} run return run function bm:gb/{n}' for n in range(1, len(GB) + 1)])
        for n, arg in enumerate(GB, 1):
            fn(f'gb/{n}', [f'execute unless items entity @s weapon.mainhand * run return run item replace entity @s weapon.mainhand with {arg}',
                           f'execute unless items entity @s weapon.offhand * run return run item replace entity @s weapon.offhand with {arg}',
                           f'give @s {arg}'])
    # (2.89: every use runs at @s - an advancement's reward brings the player's position but not where they look, so anything
    #  aimed with ^ ^ ^ or anchored eyes went out level and due south; the Arachno-Lantern's Glare missed all it was aimed at)
    for iid, func in sorted(HOLD_REPEAT.items()):
        wjson(f'bm/advancement/hold/{iid}.json', {
            'criteria': {'use': {'trigger': 'minecraft:using_item', 'conditions': {
                'item': {'items': ITEMS[iid]['base'], 'predicates': {'minecraft:custom_data': G.snbt({'bm': iid})}}}}},
            'rewards': {'function': f'bm:hold/{iid}'}})
        fn(f'hold/{iid}', [f'advancement revoke @s only bm:hold/{iid}',
                           'execute store result score #now bm.hnow run time query gametime',
                           'scoreboard players operation #gap bm.hnow = #now bm.hnow', 'scoreboard players operation #gap bm.hnow -= @s bm.huse',
                           'scoreboard players operation @s bm.huse = #now bm.hnow',
                           'execute store success score #first bm.hnow if score #gap bm.hnow matches 3..',
                           f'execute at @s run function {func}'])
    for iid, func in sorted(HOLD.items()):
        wjson(f'bm/advancement/hold/{iid}.json', {
            'criteria': {'use': {'trigger': 'minecraft:using_item', 'conditions': {
                'item': {'items': ITEMS[iid]['base'], 'predicates': {'minecraft:custom_data': G.snbt({'bm': iid})}}}}},
            'rewards': {'function': f'bm:hold/{iid}'}})
        fn(f'hold/{iid}', [f'advancement revoke @s only bm:hold/{iid}',
                           'execute store result score #now bm.hnow run time query gametime',
                           'scoreboard players operation #gap bm.hnow = #now bm.hnow', 'scoreboard players operation #gap bm.hnow -= @s bm.huse',
                           'scoreboard players operation @s bm.huse = #now bm.hnow',
                           'execute if score #gap bm.hnow matches 0..2 run return 0',
                           f'execute at @s run function {func}'])
