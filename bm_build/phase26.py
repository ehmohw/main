"""Phase 1.16: playtest fixes and alien gear.

- ROCKET BOOTS (Zorp, 12 green + 8 violet): jump again in mid-air for a rocket burst. ROCKET BOOTS MK II (trade the
  Mk I boots + 12 cyan): two extra jumps. Read from the jump key (26.2 player input predicate); not while flying,
  gliding or in water.
- The TRACTOR BEAM now runs on Violet Xenite, 5 pulls per shard (like the Ray Gun's green ammo).
- The XENITE DOWSER outlines the ores it finds with a glowing block that shows THROUGH stone, for 10 seconds.
- NAMEPLATES: every trader carries a small nameplate (their own name, in their colour) that only renders within about
  13 blocks and never through walls.
- MARKET FIXES for markets already generated (1.13 layout): Chef Fromage and Lucky Whiskers step out in front of their
  counters (they were hidden behind them); crowd rats sitting on stairs are lifted onto the seat. New markets are built
  that way (market2.py).
Importing registers the items; generate(G) runs after phase25.generate."""
from nbt import snbt, B, F, Int
from items import item, attr, T

item('rocket_boots', 'minecraft:iron_boots', 'Rocket Boots', '#ff9a3c',
     ['Jump again in mid-air for a rocket burst.', ('1 extra jump, +3 Safe Fall', 'blue')],
     model='bm:rocket_boots', stack=1, cat='alien',
     comps={'minecraft:attribute_modifiers': [attr('armor', 2, 'feet'), attr('safe_fall_distance', 3, 'feet')]})
item('rocket_boots_2', 'minecraft:diamond_boots', 'Rocket Boots Mk II', '#ff6a1a',
     ['Jump twice more in mid-air.', ('2 extra jumps, +5 Safe Fall', 'blue')],
     model='bm:rocket_boots_2', stack=1, cat='alien',
     comps={'minecraft:attribute_modifiers': [attr('armor', 3, 'feet'), attr('armor_toughness', 2, 'feet'), attr('safe_fall_distance', 5, 'feet')]})

# Zorp (and the mothership quartermaster) sell them - added before phase 1.14 builds his offers, so only he re-syncs
import phase24 as _R24
_k = next(i for i, o in enumerate(_R24.OFFERS) if o[2][0] == 'gravity_boots') + 1
_R24.OFFERS[_k:_k] = [(('xenite_green', 12), ('xenite_violet', 8), ('rocket_boots', 1)),
                      (('rocket_boots', 1), ('xenite_cyan', 12), ('rocket_boots_2', 1))]

TRACTOR_PULLS = 5
PLATE_RANGE = 0.2            # text display view_range: about 13 blocks at default entity distance


def generate(G):
    fn, wjson, title = G.fn, G.wjson, G.title
    tick, fast, second = [], [], []
    ident = [F(0), F(0), F(0), F(1)]
    objs = ['bm.rj', 'bm.rjp', 'bm.rjt', 'bm.tammo', 'bm.rair']
    G.FUNCS['load'][0:0] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================ rocket boots
    wjson('bm/predicate/p26/jump_key.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                              'predicate': {'minecraft:type_specific/player': {'input': {'jump': True}}}})
    wjson('bm/predicate/p26/no_rocket.json', {'condition': 'minecraft:any_of', 'terms': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {f: True}}}
        for f in ('is_flying', 'is_fall_flying', 'is_in_water', 'is_swimming')]})
    tick += ['execute as @a[gamemode=!spectator] if items entity @s armor.feet *[minecraft:custom_data~{bm:"rocket_boots"}] at @s run function bm:p26/rocket/one',
             'execute as @a[gamemode=!spectator] if items entity @s armor.feet *[minecraft:custom_data~{bm:"rocket_boots_2"}] at @s run function bm:p26/rocket/two',
             'execute as @a[scores={bm.rjt=1..}] at @s run function bm:p26/rocket/burn']
    fn('p26/rocket/one', ['scoreboard players set #rmax bm.rng 1', 'function bm:p26/rocket/check'])
    fn('p26/rocket/two', ['scoreboard players set #rmax bm.rng 2', 'function bm:p26/rocket/check'])
    # a fresh press of jump (not held over from the take-off) while airborne fires the next burst; landing reloads
    # 1.17: and only after a few ticks in the air - the server often sees the take-off and the key press in the same
    # tick, which fired a burst on the first jump
    fn('p26/rocket/check', ['execute unless score @s bm.rj matches 0.. run scoreboard players set @s bm.rj 0',
                            'scoreboard players set #j bm.rng 0',
                            'execute if predicate bm:p26/jump_key run scoreboard players set #j bm.rng 1',
                            'execute unless predicate bm:p21/airborne run scoreboard players set @s bm.rj 0',
                            'execute unless predicate bm:p21/airborne run scoreboard players set @s bm.rair 0',
                            'execute if predicate bm:p21/airborne run scoreboard players add @s bm.rair 1',
                            'execute if predicate bm:p21/airborne if score @s bm.rair matches 4.. if score #j bm.rng matches 1 unless score @s bm.rjp matches 1 unless predicate bm:p26/no_rocket if score @s bm.rj < #rmax bm.rng run function bm:p26/rocket/boost',
                            'scoreboard players operation @s bm.rjp = #j bm.rng'])
    # 1.19: 5 ticks of Levitation 27 = a real rocket kick of about 7 blocks (was 3 ticks of 25, about 3) (Levitation also clears fall distance)
    fn('p26/rocket/boost', ['scoreboard players add @s bm.rj 1', 'effect give @s minecraft:levitation 1 26 true', 'scoreboard players set @s bm.rjt 5',
                            'particle minecraft:flame ~ ~ ~ 0.2 0.05 0.2 0.03 14', 'particle minecraft:cloud ~ ~ ~ 0.25 0.05 0.25 0.02 8',
                            'playsound minecraft:entity.firework_rocket.launch player @a[distance=..16] ~ ~ ~ 0.9 1.2'])
    fn('p26/rocket/burn', ['scoreboard players remove @s bm.rjt 1', 'particle minecraft:flame ~ ~ ~ 0.08 0 0.08 0.01 3',
                           'execute if score @s bm.rjt matches 0 run effect clear @s minecraft:levitation'])

    # ================================================================ the levitation wand only lifts off from the ground
    # (1.12-1.15: re-using it in mid-air every 2 s stacked hops into an endless climb)
    wd = G.FUNCS['p22/wand']
    assert wd[0].startswith('execute if score @s bm.wcd matches 1..')
    wd.insert(1, 'execute if predicate bm:p21/airborne run return run ' + title('@s', 'actionbar', T('The wand needs solid ground under your feet.', 'gray')))

    # ================================================================ the tractor beam runs on violet xenite
    violet = '*[minecraft:custom_data~{bm:"xenite_violet"}]'
    tu = G.FUNCS['p24/tractor/use']
    assert tu[0].startswith('execute if score @s bm.tcd matches 1..')
    tu[1:1] = ['execute unless score @s bm.tammo matches 1.. store result score #s bm.rng run clear @s ' + violet + ' 0',
               'execute unless score @s bm.tammo matches 1.. if score #s bm.rng matches 0 run return run function bm:p26/tractor_empty',
               f'execute unless score @s bm.tammo matches 1.. run clear @s {violet} 1',
               f'execute unless score @s bm.tammo matches 1.. run scoreboard players set @s bm.tammo {TRACTOR_PULLS}',
               'scoreboard players remove @s bm.tammo 1']
    tu.append(title('@s', 'actionbar', [T('Tractor Beam: ', '#c27dff'), {'score': {'name': '@s', 'objective': 'bm.tammo'}, 'color': 'white'},
                                        T(' pulls left in this crystal', 'gray')]))
    fn('p26/tractor_empty', ['scoreboard players set @s bm.tcd 10', 'playsound minecraft:block.dispenser.fail player @s ~ ~ ~ 1 1.4',
                             title('@s', 'actionbar', T('Out of power - carry Violet Xenite shards.', 'red'))])

    # ================================================================ the dowser outlines ores through stone
    ORES = {'diamond': (['minecraft:diamond_ore', 'minecraft:deepslate_diamond_ore'], 0x55FFFF, 'minecraft:diamond_ore'),
            'emerald': (['minecraft:emerald_ore', 'minecraft:deepslate_emerald_ore'], 0x55FF55, 'minecraft:emerald_ore'),
            'debris': (['minecraft:ancient_debris'], 0xFFAA00, 'minecraft:ancient_debris')}
    hit = ['scoreboard players add #dn bm.rng 1', 'execute if score #dn bm.rng matches 25.. run return 0']
    for k, (blocks, col, shown) in ORES.items():
        wjson(f'bm/tags/block/dowse_{k}.json', {'values': blocks})
        d = {'Tags': ['bm.dglow'], 'Glowing': B(1), 'glow_color_override': Int(col), 'block_state': shown,
             'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(0.5),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(-0.01), F(-0.01), F(-0.01)], 'scale': [F(1.02)] * 3}}
        hit.append(f'execute if block ~ ~ ~ #bm:dowse_{k} align xyz run summon minecraft:block_display ~ ~ ~ {snbt(d)}')
    G.FUNCS['p24/dowse/hit'] = hit
    second += ['scoreboard players add @e[type=minecraft:block_display,tag=bm.dglow] bm.dage 1',
               'kill @e[type=minecraft:block_display,tag=bm.dglow,scores={bm.dage=10..}]']
    du = G.FUNCS['p24/dowse/use']
    du[:] = [l.replace(' (marked with light)', ' (outlined for 10 seconds)') if isinstance(l, str) else l for l in du]

    # ================================================================ trader nameplates (short range, not through walls)
    # Static plates (traders never move), not riders: a passenger could get in the way of trading.
    import phase22
    void_oy = next(v[5] for k2, v in phase22.RATS.items() if k2 == 'void') or 0
    plate = {'Tags': ['bm.plate', 'bm.pnew'], 'billboard': 'center', 'view_range': F(PLATE_RANGE), 'shadow': B(1),
             'background': Int(0x50000000), 'line_width': Int(200), 'brightness': {'block': Int(15), 'sky': Int(15)},
             'text': T('', 'white'),
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(2.25), F(0)], 'scale': [F(0.7)] * 3}}
    new = '@e[type=minecraft:text_display,tag=bm.pnew,limit=1,sort=nearest]'
    def height(h): return f'data merge entity {new} {{transformation:{{translation:[0f,{h}f,0f]}}}}'
    fn('p26/plate/add', ['tag @s add bm.plated', f'summon minecraft:text_display ~ ~ ~ {snbt(plate)}',
                         f'data modify entity {new} text set from entity @s CustomName',
                         'execute store result score #sc bm.rng run attribute @s minecraft:scale get 100',
                         'execute if score #sc bm.rng matches ..60 run ' + height(1.05),                      # the rats (half-size traders)
                         'execute if entity @s[tag=bm.npc_alien] run ' + height(1.95),                         # Zorp and the quartermaster
                         'execute if entity @s[tag=bm.frat_void] run ' + height(round(1.05 + float(void_oy), 2)),  # the floating Void Rat
                         'tag @e[type=minecraft:text_display,tag=bm.pnew] remove bm.pnew'])
    plates = ['execute as @e[type=minecraft:villager,tag=bm.npc,tag=!bm.plated] at @s run function bm:p26/plate/add',
              'execute as @e[type=minecraft:wandering_trader,tag=bm.npc,tag=!bm.plated] at @s run function bm:p26/plate/add',
              'execute as @e[type=minecraft:wandering_trader,tag=bm.field_rat,tag=!bm.plated] at @s run function bm:p26/plate/add',
              'execute as @e[type=minecraft:text_display,tag=bm.plate] at @s unless entity @e[type=minecraft:villager,distance=..0.3] unless entity @e[type=minecraft:wandering_trader,distance=..0.3] run kill @s']

    # ================================================================ market fixes for 1.13-layout markets already in worlds
    # Rotation-proof: look for the counter on each side, with the back shelf (barrels/smokers, gold) on the opposite side -
    # so a trader already standing in front of the counter (new markets) is never moved.
    wjson('bm/tags/block/p26_chef_back.json', {'values': ['minecraft:barrel', 'minecraft:smoker']})
    def step_out(k, counter, top, back):
        lines = ['tag @s add bm.mv16']
        for i, (dx, dz) in enumerate(((-1, 0), (1, 0), (0, -1), (0, 1))):
            o = lambda n: f'{n:g}' if n else ''
            lines.append(f'execute if block ~{o(dx)} ~ ~{o(dz)} {counter} if block ~{o(dx)} ~1 ~{o(dz)} {top} if block ~{o(-dx)} ~ ~{o(-dz)} {back} '
                         f'run return run function bm:p26/move_{k}_{i}')
            fn(f'p26/move_{k}_{i}', [f'execute as @e[type=minecraft:item_display,tag=bm.rat_sprite,distance=..0.6] run tp @s ~{o(2 * dx)} ~ ~{o(2 * dz)}',
                                     f'tp @s ~{o(2 * dx)} ~ ~{o(2 * dz)}'])
        fn(f'p26/check_{k}', lines)
    step_out('chef', 'minecraft:stripped_spruce_log', 'minecraft:spruce_slab', '#bm:p26_chef_back')
    step_out('lucky', 'minecraft:stripped_dark_oak_log', 'minecraft:gold_block', 'minecraft:gold_block')
    fixes = ['execute as @e[type=minecraft:villager,tag=bm.npc_chef,tag=!bm.mv16] at @s run function bm:p26/check_chef',
             'execute as @e[type=minecraft:villager,tag=bm.npc_lucky,tag=!bm.mv16] at @s run function bm:p26/check_lucky',
             # a crowd rat whose feet are at the bottom of a stair block sits half a block too low (new markets already sit on the seat)
             'execute as @e[type=minecraft:item_display,tag=bm.crowd,tag=!bm.seat16] at @s if block ~ ~0.5 ~ #minecraft:stairs[half=bottom] run tp @s ~ ~0.5 ~',
             'tag @e[type=minecraft:item_display,tag=bm.crowd,tag=!bm.seat16] add bm.seat16']
    second += fixes + plates

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    k = f.index('scoreboard players reset @a bm.sneak')
    f[k:k] = fast
    s = G.FUNCS['loop/second']
    s[-1:-1] = second


def icons(grid):
    I = {}
    I['rocket_boots'] = grid([
        '................', '................', '....SSS..SSS....', '....SOS..SOS....', '....SOS..SOS....', '....SOS..SOS....',
        '....SOS..SOS....', '....SOSS.SOSS...', '...SOOOS.SOOOS..', '..SOOOOSSOOOOS..', '..SSSSSSSSSSSS..', '...YY..YY.YY....',
        '..YRRY..YRRY....', '...R......R.....', '................', '................'], dict(S='#c8ccd2', O='#ff9a3c', Y='#ffe066', R='#ff4a1a'))
    I['rocket_boots_2'] = grid([
        '................', '................', '....DDD..DDD....', '....DOD..DOD....', '....DOD..DOD....', '....DOD..DOD....',
        '....DOD..DOD....', '....DODD.DODD...', '...DOOOD.DOOOD..', '..DOOOODDOOOOD..', '..DDDDDDDDDDDD..', '..YYYY..YYYY....',
        '..YRRY..YRRY....', '..RRRR..RRRR....', '...R......R.....', '................'], dict(D='#5fd8d0', O='#ff6a1a', Y='#ffe066', R='#ff3a1a'))
    return I
