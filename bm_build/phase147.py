"""2.79a: GILDED - every follower's gilded look, in polished gold, dear, and sparkling.

THE LOOK      each follower has one gilded outfit (gild.GILDED): Emma's Gilded Gown, Celi's Gilded outfit, Zib's Golden Ace,
              Cecil's Gilded robe, KillerWatt's Golden Thunder, Leo's Golden Champion, Democratus' Gilded Storm, Apophiss's
              Gilded Coil, Tullius's Gilded Captain, the Frog's Golden Prince, Donado's Gilded coat (new), Pearlman's Gilded bow
              tie, Wilfrey's Gilded Sun and Fishy's Gilded Topper. Their textures are polished gold (gild.metal: a gold ramp,
              burnished contrast, light along the edges, a sheen, glints) - not yellow cloth. Wilfrey, the one real mob among
              them, wears the sun shield and his armour turns to gold (only its look: the pieces keep what they are).
DEAR          20 Gutter Trophies - 2,560 coins at the Tailor (an aura is 1,280). Not at Madame Velour's, not in the vault's rare
              tables: bought, and dearly.
SPARKLES      a follower in their gilded look glitters wherever they go: gold motes and glints round them, now and then a star
              of light - so you can tell the rare look at a glance (not while a gem's element shows on Cecil or KillerWatt).
"""
from items import ITEMS, T
import gild
import phase138 as P138

GOLD = gild.GOLD
# (the gilded items say what they are: polished gold that sparkles, the Tailor's dearest)
for _iid in gild.ITEMS:
    _L = ITEMS[_iid]['comps']['minecraft:lore']
    _L[:] = [l for l in _L if not (isinstance(l, dict) and str(l.get('text', '')).startswith('Hidden'))]
    _L.append(T('Gilded: polished gold - and it sparkles.', GOLD))
    _L.append(T('The Tailor\'s dearest: 2,560 coins.', 'dark_gray'))
    ITEMS[_iid]['comps']['minecraft:enchantment_glint_override'] = True


def generate(G):
    fn = G.fn
    # ================================================================== the sparkles (every 5 ticks, as each follower's host)
    fast = G.FUNCS['loop/fast']
    lines = []
    for w, (k, iid, score) in gild.GILDED.items():
        host_t, host_tag = P138.HOST[w]
        _n, _c, h, r = P138.AURA[w][:4]
        extra = {'cecil': ' unless score @s bm.cpel matches 1..', 'kw': ' unless score @s bm.kxel matches 1..'}.get(w, '')   # (a gem's element showing: not gold)
        lines.append(f'execute as @e[type=minecraft:{host_t},tag={host_tag}] at @s on owner if score @s {score} matches {k}{extra} run function bm:p147/sp/{w}')
        fn(f'p147/sp/{w}', [f'particle minecraft:wax_on ~ ~{h:.2f} ~ {r:.2f} {h * 0.55:.2f} {r:.2f} 0 2',
                            f'particle minecraft:dust{{color:[1.0,0.84,0.3],scale:0.7}} ~ ~{h:.2f} ~ {r * 0.9:.2f} {h * 0.5:.2f} {r * 0.9:.2f} 0 2',
                            f'execute if predicate bm:p147/third run particle minecraft:end_rod ~ ~{h + 0.25:.2f} ~ {r * 0.8:.2f} {h * 0.45:.2f} {r * 0.8:.2f} 0.01 1'])
    fast[-1:-1] = lines
    G.wjson('bm/predicate/p147/third.json', {'condition': 'minecraft:random_chance', 'chance': 0.34})

    # ================================================================== Wilfrey: the sun shield, and his armour's look turned to gold
    slots = {'head': 'armor.head', 'chest': 'armor.chest', 'legs': 'armor.legs', 'feet': 'armor.feet'}
    for sl in slots:
        G.wjson(f'bm/item_modifier/p147/gold_{sl}.json', {'function': 'minecraft:set_components',
                                                          'components': {'minecraft:equippable': {'slot': sl, 'asset_id': 'minecraft:gold'},
                                                                         'minecraft:enchantment_glint_override': True}})
    bare = {'head': 'golden_helmet', 'chest': 'golden_chestplate', 'legs': 'golden_leggings', 'feet': 'golden_boots'}
    fn('p147/wil/gold', [l for sl, slot in slots.items() for l in (
        f'execute unless items entity @s {slot} * run item replace entity @s {slot} with minecraft:{bare[sl]}[minecraft:enchantment_glint_override=true]',
        f'item modify entity @s {slot} bm:p147/gold_{sl}')])
    G.FUNCS['p2/wil/dress'].append(f'execute if score #wk bm.rng matches {gild.GILDED["wil"][0]} run function bm:p147/wil/gold')
    # (a look picked while he's out: his own gear back on first, then the new look - the gold comes off with it)
    G.FUNCS['p99/wil_now'].insert(1, 'execute as @e[type=minecraft:wolf,tag=bm.wilfrey] if score @s bm.pid = #me bm.pid run function bm:p147/wil/redress')
    fn('p147/wil/redress', ['tag @s add bm.fsel', 'function bm:p2/wil/refresh', 'tag @s remove bm.fsel'])
