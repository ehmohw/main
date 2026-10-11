"""2.67: THE ETHEREAL GEM, KEPT SECRET.

THE ETHEREAL GEM is a secret again: Goldtooth no longer sells it. It is still made from the nine elemental gems - set all
  nine on display together, as before, or now simply USE ONE OF THE GEMS WHILE CARRYING ALL NINE: they rise, circle you
  and become one (the hidden advancement, Nine Made One).
  IN THE VAULT: the Ethereal Gem passes the coat check now, but only ONE goes into each heist - the first raider through
  the door who carries one keeps it; any other (a second of yours, or a crewmate's) waits with the Fixer until you leave.
EMMA'S CLOTHES: her outfits already showed her buff's colour (the scarf on her dresses, the Flower Top's choker) - now
  the Cozy Sweater does too (a heart pin on its chest, phase89). Her ethereal form keeps its own armour and wings.
"""
import math
from items import T
from nbt import snbt, B, F, Int
import phase60 as P60
import phase72 as P72

P72.KEEP.append('ethereal_gem')
ETH = P60.ETH


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    gem = '*[minecraft:custom_data~{bm:"ethereal_gem"}]'

    # ================================================================== THE NINE IN YOUR HANDS: use one while carrying all nine
    has9 = ' '.join(f'if items entity @s container.* *[minecraft:custom_data~{{bm:"gem_{k}"}}]' for k in P60.KEYS)
    for k in P60.KEYS:
        G.FUNCS[f'p60/gem/use_{k}'].insert(1, f'execute {has9} run return run function bm:p94/fuse')
    ident = [F(0), F(0), F(0), F(1)]
    def gdisp(k):
        return snbt({'Tags': ['bm.gfuse', 'bm.gfnew'], 'teleport_duration': Int(5), 'interpolation_duration': Int(30), 'start_interpolation': Int(0),
                     'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:gem_{k}'}}, 'item_display': 'fixed',
                     'brightness': {'block': Int(15), 'sky': Int(15)},
                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.2), F(0)], 'scale': [F(0.55)] * 3}})
    fn('p94/fuse', [f'clear @s *[minecraft:custom_data~{{bm:"gem_{k}"}}] 1' for k in P60.KEYS] +
       ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gfm","bm.gfmnew"]}',                     # (round YOU: the gem drops into your hands)
        'scoreboard players set @e[type=minecraft:marker,tag=bm.gfmnew] bm.gft 0'] +
       [f'execute rotated {i * 40} 0 positioned ^ ^0.2 ^1.3 run summon minecraft:item_display ~ ~ ~ {gdisp(k)}' for i, k in enumerate(P60.KEYS)] +
       ['execute as @e[type=minecraft:item_display,tag=bm.gfnew] run data merge entity @s {start_interpolation:0,interpolation_duration:30,transformation:{translation:[0f,1.6f,0f]}}',
        'tag @e[type=minecraft:item_display,tag=bm.gfnew] remove bm.gfnew', 'tag @e[type=minecraft:marker,tag=bm.gfmnew] remove bm.gfmnew',
        'playsound minecraft:block.beacon.power_select block @a[distance=..32] ~ ~ ~ 1 1.4',
        'playsound minecraft:block.amethyst_block.resonate block @a[distance=..32] ~ ~ ~ 1 0.6',
        title('@s', 'actionbar', T('The nine gems slip from your hands and rise...', ETH, italic=True))])

    # ================================================================== ONE ETHEREAL GEM A HEIST: the first through the door keeps it
    import phase70 as P70
    for s in range(P70.SLOTS):
        for f in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            if f not in G.FUNCS: continue
            L = G.FUNCS[f]
            k = next((i for i, l in enumerate(L) if l.startswith('scoreboard players operation @s bm.gvrun = ')), None)
            if k is None: continue
            L.insert(k + 1, f'function bm:p94/eth/gate {{s:{s}}}')
    fn('p94/eth/gate', ['execute store result score #eg bm.rng run clear @s ' + gem + ' 0',
                        'execute if score #eg bm.rng matches 0 run return 0',
                        '$execute if score #eth$(s) bm.gvrun = @s bm.gvrun run return run function bm:p94/eth/hold {keep:0}',
                        '$scoreboard players operation #eth$(s) bm.gvrun = @s bm.gvrun',
                        'execute if score #eg bm.rng matches 2.. run function bm:p94/eth/hold {keep:1}'])
    # (as the raider) hand the Fixer every Ethereal Gem past the ones kept: into the coat-check bag, back when you leave
    fn('p94/eth/hold', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', '$scoreboard players set #keep bm.rng $(keep)',
                        'function bm:p94/eth/hold1 with storage bm:gv tmp',
                        'execute if score #held bm.rng matches 1.. run ' + tellraw('@s', P + [T('Only one Ethereal Gem may sing in the vault at a time - ', ETH),
                                                                                         T('the Fixer minds the other until you leave.', 'gray')])])
    fn('p94/eth/hold1', ['scoreboard players set #held bm.rng 0',
                         '$execute unless data storage bm:gv bag.p$(pid) run data modify storage bm:gv bag.p$(pid) set value {inv:[],eq:{}}',
                         'function bm:p94/eth/hold_step with storage bm:gv tmp'])
    fn('p94/eth/hold_step', ['execute store result score #eg bm.rng run clear @s ' + gem + ' 0', 'execute if score #eg bm.rng <= #keep bm.rng run return 0',
                             f'$execute if items entity @s weapon.offhand {gem} unless data storage bm:gv bag.p$(pid).eq.offhand run return run function bm:p94/eth/hold_off with storage bm:gv tmp',
                             'data modify storage bm:gv eg set value []',
                             'data modify storage bm:gv eg append from entity @s Inventory[{components:{"minecraft:custom_data":{bm:"ethereal_gem"}}}]',
                             'execute unless data storage bm:gv eg[0] run return 0',
                             '$data modify storage bm:gv bag.p$(pid).inv append from storage bm:gv eg[0]',
                             'execute store result score #slot bm.rng run data get storage bm:gv eg[0].Slot',
                             'execute store result storage bm:gv tmp.n int 1 run scoreboard players get #slot bm.rng',
                             'function bm:p94/eth/clear_slot with storage bm:gv tmp',
                             'scoreboard players add #held bm.rng 1', 'function bm:p94/eth/hold_step with storage bm:gv tmp'])
    fn('p94/eth/hold_off', ['$data modify storage bm:gv bag.p$(pid).eq.offhand set from entity @s equipment.offhand', 'item replace entity @s weapon.offhand with minecraft:air',
                            'scoreboard players add #held bm.rng 1', 'function bm:p94/eth/hold_step with storage bm:gv tmp'])
    fn('p94/eth/clear_slot', ['$execute if score #slot bm.rng matches 0..35 run item replace entity @s container.$(n) with minecraft:air'])     # (a player's container.N is inventory slot N)
