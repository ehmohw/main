"""Hold-to-use items (2.13): right-clicking starts "using" the item (a consumable that never finishes), and the
`using_item` advancement trigger fires on that first tick. Unlike the older consume trick, the item is never used up,
so it keeps its data (stored XP, contents, charges, enchantments, damage) and nothing has to be handed back.

    from useitem import hold, HOLD
    item(..., comps=hold())                  # the item's components
    HOLD['my_item'] = 'bm:p33/my_item/use'   # run (as and at the player) once per press

`use_effects` keeps the player at full speed while the button is held. One press = one action: the trigger fires every
tick the button is held, and the wrapper ignores ticks that follow straight on from the last one."""

HOLD = {}       # iid -> function run once per press


def hold(anim='none', extra=None):
    c = {'minecraft:consumable': {'consume_seconds': 100000.0, 'animation': anim, 'sound': 'minecraft:intentionally_empty',
                                  'has_consume_particles': False},
         'minecraft:use_effects': {'can_sprint': True, 'speed_multiplier': 1.0, 'interact_vibrations': False}}
    if extra: c.update(extra)
    return c


def generate(G):
    from items import ITEMS
    fn, wjson = G.fn, G.wjson
    G.FUNCS['load'][0:0] = ['scoreboard objectives add bm.huse dummy', 'scoreboard objectives add bm.hnow dummy']
    G.OBJECTIVES += ['bm.huse', 'bm.hnow']
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
                           f'function {func}'])
