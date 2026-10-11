"""2.67: PARTY ROOMS - four new event rooms in the spirit of the Rat Rave (party-game minigames).

WHACK-A-RAT (any crew)   rats pop out of nine bins - hit them before they duck. Golden rats count three. Whack enough
                         in 45 seconds (12, +4 a crewmate) and the crew gets Strength and coins; miss and the alarm rings.
RAT SAYS (any crew)      the Rat Professor calls JUMP, SNEAK, LOOK UP, LOOK DOWN or FREEZE. Only obey when he says
                         "Rat says"! Eight calls; every right answer is a coin for the pot, every wrong one rings the alarm.
COIN SCRAMBLE (2+ only)  coins rain from the chutes for 35 seconds - grab the most (big coins count five). The winner
                         gets a prize in their haul; half of everything grabbed goes into the pot.
BUMPER BRAWL (2+ only)   a ring over a pit and sixteen wind charges each: blow your crewmates off. The ring shrinks
                         after 30 seconds. Last one standing wins a prize in their haul (still standing at a minute:
                         everyone left shares it).
The two contests never turn up in a solo heist.
"""
import math
from items import T, ITEMS
from nbt import snbt, B, F, Int
from structures import Build
import phase70_rooms as RM
import phase75 as P75
import phase76_rooms as R6
from phase75_rooms import BASE, wall_glow

GOLD = '#ffcf40'
PARTY = '#ff7ad8'
FY = RM.FY
W, H, D = RM.W, RM.H, RM.D
HOLES = [(x, z) for z in (7, 12, 17) for x in (7, 12, 17)]
RATS = ['pirate', 'soldier', 'chef', 'grey', 'lucky', 'prof', 'chef', 'pirate', 'soldier']
CHUTES = [(x, z) for x in (5, 10, 14, 19) for z in (5, 10, 14, 19)]
COMPETITIVE = ['scramble', 'brawl']
NAMES = {'whack': 'Whack-a-Rat', 'says': 'Rat Says', 'scramble': 'The Coin Scramble', 'brawl': 'The Bumper Brawl'}


# ===================================================================== the rooms
def whack():
    b = R6.shell()
    for (x, z) in HOLES:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                b.set(x + dx, FY, z + dz, 'minecraft:packed_mud')
        b.set(x, FY, z, 'minecraft:composter[level=0]')
    for x in range(2, 23):                                   # carnival awnings along the long walls
        for z in (1, 23):
            b.set(x, 9, z, 'minecraft:red_wool' if x % 2 else 'minecraft:white_wool')
    R6.ctrl(b, 'whack'); return wall_glow(b)


def says():
    b = R6.shell()
    for x in range(2, 23):
        for z in range(6, 23):
            if 11 <= z <= 13: continue
            b.set(x, FY, z, 'minecraft:white_concrete' if (x + z) % 2 else 'minecraft:light_gray_concrete')
    for x in range(9, 16):                                   # the Professor's stage
        for z in (2, 3, 4):
            b.set(x, 4, z, 'minecraft:polished_deepslate_slab[type=bottom]')
    b.set(12, 4, 3, 'minecraft:chiseled_quartz_block')
    for x in range(8, 17):
        b.set(x, 4, 1, 'minecraft:red_concrete'); b.set(x, 5, 1, 'minecraft:red_concrete')
    R6.ctrl(b, 'says'); return wall_glow(b)


def scramble():
    b = R6.shell()
    for x in range(2, 23):
        for z in range(2, 23):
            if (x + z) % 4 == 0: b.set(x, FY, z, BASE['metal'])
    for (x, z) in CHUTES:
        b.set(x, H - 2, z, 'minecraft:hopper[facing=down]')
    R6.ctrl(b, 'scramble'); return wall_glow(b)


def ring_cells():
    inner, outer = [], []
    for x in range(4, 21):
        for z in range(4, 21):
            r = math.hypot(x - 12, z - 12)
            if r <= 4.6: inner.append((x, z))
            elif r <= 7.4: outer.append((x, z))
    return inner, outer


BRIDGE_IN = [(x, z) for x in (3, 4) for z in (11, 12, 13)]
BRIDGE_OUT = [(x, z) for x in (20, 21) for z in (11, 12, 13)]


def brawl():
    b = R6.shell()
    inner, outer = ring_cells()
    for x in range(3, 22):                                   # the pit: everything between the galleries
        for z in range(1, 24):
            for y in (FY, 2): b.set(x, y, z, 'minecraft:air')
            b.set(x, 1, z, 'minecraft:water'); b.set(x, 0, z, 'minecraft:sea_lantern')
    for (x, z) in inner:
        b.set(x, FY, z, 'minecraft:yellow_concrete' if math.hypot(x - 12, z - 12) < 2.2 else 'minecraft:white_concrete')
    for (x, z) in outer:
        b.set(x, FY, z, 'minecraft:red_concrete')
    for (x, z) in BRIDGE_IN:
        b.set(x, FY, z, 'minecraft:spruce_planks')
    for z in range(1, 24):                                   # the galleries (x 1-2 and 22-23) keep their floor
        for x in (1, 2, 22, 23): b.set(x, FY, z, BASE['floor'])
    R6.ctrl(b, 'brawl'); return wall_glow(b)


BUILDERS = {'whack': whack, 'says': says, 'scramble': scramble, 'brawl': brawl}
for _k, _f in BUILDERS.items():
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
P75.EVENT_POOL[1] += ['whack', 'says', 'scramble', 'brawl']
P75.EVENT_POOL[2] += ['whack', 'says', 'scramble', 'brawl']
P75.EVENT_POOL[3] += ['whack', 'says', 'scramble', 'brawl']
P75.EVENT_POOL[4] += ['whack', 'says', 'scramble', 'brawl']
P75.EVENT_POOL[5] += ['whack', 'says', 'scramble', 'brawl']
assert len(P75.KINDS) + len(P75.EXTRA_ROOMS) <= 31, 'the layout keeps used rooms as bits of one score: 31 at most'


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase72 as P72
    rel = RM.rel
    ident = [F(0), F(0), F(0), F(1)]
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    crew = '@a[tag=bm.gvp,distance=..16]'
    def label(x, y, z, text, scale=0.6, tags=('bm.gvprop',)):
        return f'summon minecraft:text_display {rel(x, y, z)} ' + snbt({'Tags': list(tags), 'billboard': 'vertical', 'brightness': {'block': 15, 'sky': 15},
                                                                       'background': Int(0x90000000 - 2 ** 32), 'text': text, 'line_width': Int(220),
                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                          'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}})
    def sign(x, y, z, t_, body):
        return label(x, y, z, [T(t_ + '\n', PARTY, bold=True), T(body, 'gray')])
    def big(t_, sub, col=PARTY):
        return [f'title {crew} times 5 40 10', title(crew, 'title', T(t_, col, bold=True)), title(crew, 'subtitle', T(sub, 'gray'))]
    def pot(n):
        return [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    objs = ['bm.gvjmp', 'bm.gvsx', 'bm.gvsz', 'bm.gvscr', 'bm.gvscb', 'bm.gvscs']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvjmp minecraft.custom:minecraft.jump', 'scoreboard objectives add bm.gvsx dummy',
                              'scoreboard objectives add bm.gvsz dummy', 'scoreboard objectives add bm.gvscr minecraft.picked_up:minecraft.gold_nugget',
                              'scoreboard objectives add bm.gvscb minecraft.picked_up:minecraft.gold_ingot', 'scoreboard objectives add bm.gvscs dummy'] + \
        [f'scoreboard players set #k{n} bm.rng {n}' for n in (3, 4, 5, 6, 10)]
    G.OBJECTIVES += objs

    # ================================================================== dispatch, names, music, never alone for the contests
    ks = list(BUILDERS)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p85/{k}/init' for k in ks]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p85/{k}/tick' for k in ks]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in ks]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - done. The way on is open.', 'gray')]) for k in ks]
    for t in range(1, 6):
        ev = G.FUNCS[f'p75/lay/event{t}']
        j = next(i for i, l in enumerate(ev) if l.startswith('function bm:p75/lay/bit'))
        idx = {k: len(P75.KINDS) + list(P75.EXTRA_ROOMS).index(k) for k in COMPETITIVE}
        ev[j:j] = [f'execute if score #r bm.rng matches {idx[k]} if score #gpl bm.rng matches ..1 run return run function bm:p85/lay/solo' for k in COMPETITIVE]
    fn('p85/lay/solo', ['function bm:p75/lay/pick'] + [f'execute if score #r bm.rng matches {j} run function bm:p75/pc/{k}' for j, k in enumerate(P75.KINDS)])
    music = 'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvmz 7'
    # the prize for a contest's winner (into their haul)
    for t in range(1, 6):
        main = {1: [('minecraft:gold_ingot', 6, 10), ('minecraft:emerald', 5, 8)], 2: [('minecraft:gold_block', 1, 3), ('minecraft:diamond', 1, 2)],
                3: [('minecraft:diamond', 2, 4), ('minecraft:gold_block', 2, 4)], 4: [('minecraft:diamond', 3, 5), ('minecraft:emerald_block', 1, 3)],
                5: [('minecraft:diamond_block', 1, 2), ('minecraft:netherite_scrap', 1, 1)]}[t]
        wjson(f'bm/loot_table/p85/prize_t{t}.json', {'pools': [
            {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': i, 'functions': [{'function': 'minecraft:set_count', 'count': G.uni(lo, hi)}]} for i, lo, hi in main]},
            {'rolls': 1, 'entries': [dict(G.loot_entry('healing_draught', G.uni(1, 2)), weight=6), dict(G.loot_entry('second_wind'), weight=2),
                                     {'type': 'minecraft:item', 'name': 'minecraft:golden_apple', 'weight': 4},
                                     dict(G.loot_entry('lucky_purse'), weight=1)]}]})
    fn('p85/win', ['function bm:p70/ctx_p'] + [f'execute if score #gt bm.rng matches {t} run function bm:p81/defer {{t:"bm:p85/prize_t{t}"}}' for t in range(1, 6)] +
       [tellraw('@s', P + [T('A winner\'s prize goes into your haul!', PARTY, bold=True)]), 'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.2'])

    # ================================================================== WHACK-A-RAT
    def rat(i, x, z):
        d = {'Tags': ['bm.gvprop', 'bm.gvwhr'], 'Rotation': [F(0), F(0)], 'interpolation_duration': Int(2), 'teleport_duration': Int(0),
             'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:rat3d_{RATS[i]}'}}, 'item_display': 'fixed',
             'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(-1.5), F(0)], 'scale': [F(0.8)] * 3}}
        return [f'summon minecraft:item_display {rel(x, 4, z)} {snbt(d)}',
                f'summon minecraft:interaction {rel(x, 4, z)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvwh', 'bm.gvwhn'], 'width': F(1.3), 'height': F(1.4), 'response': B(1)})]
    fn('p85/whack/init', ['function bm:p70/ctx'] + sum((rat(i, x, z) for i, (x, z) in enumerate(HOLES)), []) +
       ['scoreboard players operation @e[type=minecraft:interaction,tag=bm.gvwhn,distance=..16] bm.gvi = #gi bm.rng',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.gvwhn,distance=..16] bm.gvx 0', 'tag @e[type=minecraft:interaction,tag=bm.gvwhn] remove bm.gvwhn',
        sign(2.5, 7.5, 12, 'WHACK-A-RAT', 'Rats pop out of the bins - hit them before they duck! Golden rats count three.')])
    fn('p85/whack/tick', ['execute if score @s bm.gvs matches 3 run return 0', music,
                          'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p85/whack/start',
                          'execute unless score @s bm.gvs matches 1 run return 0',
                          'scoreboard players set #up bm.rng 26', 'execute if score @s bm.gvtm matches 400.. run scoreboard players set #up bm.rng 16',
                          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #k10 bm.rng',
                          'execute if score @s bm.gvtm matches ..399 if score #q bm.rng matches 0 run function bm:p85/whack/pop1',
                          'scoreboard players operation #q bm.rng %= #k5 bm.rng',
                          'execute if score @s bm.gvtm matches 400.. if score #q bm.rng matches 0 run function bm:p85/whack/pop1',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvwhup,distance=..14] run scoreboard players remove @s bm.gvx 1',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvwhup,distance=..14,scores={bm.gvx=..0}] at @s run function bm:p85/whack/down',
                          'scoreboard players set #wh bm.rng 0',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvwh,distance=..14] if data entity @s attack at @s run function bm:p85/whack/hit',
                          'execute as @e[type=minecraft:interaction,tag=bm.gvwh,distance=..14] if data entity @s interaction at @s run function bm:p85/whack/hit',
                          'scoreboard players operation @s bm.gvw += #wh bm.rng', 'scoreboard players operation #c bm.rng = #wh bm.rng',
                          'execute if score #c bm.rng matches 1.. run ' + inst('bm:p75/pot_add'),
                          'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #k10 bm.rng',
                          'execute if score #q bm.rng matches 0 run function bm:p85/whack/hud',
                          'execute if score @s bm.gvtm matches 900.. run function bm:p85/whack/end'])
    fn('p85/whack/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvw 0',
                           'execute store result score @s bm.gvc if entity @a[tag=bm.gvp,distance=..20]', 'scoreboard players remove @s bm.gvc 1',
                           'scoreboard players operation @s bm.gvc *= #k4 bm.rng', 'scoreboard players add @s bm.gvc 12'] +
       big('WHACK-A-RAT!', 'Hit the rats before they duck back down') + ['playsound minecraft:block.note_block.bell block @a[distance=..20] ~ ~ ~ 1 1.2'])
    fn('p85/whack/pop1', ['execute as @e[type=minecraft:interaction,tag=bm.gvwh,tag=!bm.gvwhup,distance=..14,sort=random,limit=1] at @s run function bm:p85/whack/pop'])
    fn('p85/whack/pop', ['tag @s add bm.gvwhup', 'scoreboard players operation @s bm.gvx = #up bm.rng', 'execute store result score #r bm.rng run random value 1..8',
                         'execute if score #r bm.rng matches 1 run tag @s add bm.gvwhg',
                         'execute if entity @s[tag=bm.gvwhg] run data merge entity @e[type=minecraft:item_display,tag=bm.gvwhr,distance=..0.6,limit=1] {Glowing:1b,glow_color_override:16766976}',
                         'execute as @e[type=minecraft:item_display,tag=bm.gvwhr,distance=..0.6] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,0.35f,0f]}}',
                         'playsound minecraft:block.composter.fill_success block @a[distance=..16] ~ ~ ~ 0.8 1.4', 'particle minecraft:poof ~ ~0.6 ~ 0.2 0.1 0.2 0.01 4'])
    fn('p85/whack/down', ['tag @s remove bm.gvwhup', 'tag @s remove bm.gvwhg', 'scoreboard players set @s bm.gvx 0',
                          'execute as @e[type=minecraft:item_display,tag=bm.gvwhr,distance=..0.6] run data merge entity @s {Glowing:0b,start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,-1.5f,0f]}}'])
    fn('p85/whack/hit', ['data remove entity @s attack', 'data remove entity @s interaction', 'execute unless entity @s[tag=bm.gvwhup] run return 0',
                         'scoreboard players add #wh bm.rng 1', 'execute if entity @s[tag=bm.gvwhg] run scoreboard players add #wh bm.rng 2',
                         'execute if entity @s[tag=bm.gvwhg] run particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.3 0.3 0.3 20',
                         'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.25 12', 'playsound minecraft:entity.rabbit.hurt neutral @a[distance=..16] ~ ~ ~ 1 1.5',
                         'playsound minecraft:entity.player.attack.crit player @a[distance=..16] ~ ~ ~ 0.7 1.2', 'function bm:p85/whack/down'])
    fn('p85/whack/hud', ['scoreboard players operation #h1 bm.rng = @s bm.gvw', 'scoreboard players operation #h2 bm.rng = @s bm.gvc',
                         'scoreboard players set #h3 bm.rng 900', 'scoreboard players operation #h3 bm.rng -= @s bm.gvtm', 'scoreboard players operation #h3 bm.rng /= #20 bm.rng',
                         f'title {crew} actionbar ' + snbt([T('Whacked ', PARTY), {'score': {'name': '#h1', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                           T(' / ', 'gray'), {'score': {'name': '#h2', 'objective': 'bm.rng'}, 'color': 'white'},
                                                           T('    ', 'gray'), {'score': {'name': '#h3', 'objective': 'bm.rng'}, 'color': 'yellow'}, T(' s', 'yellow')])])
    fn('p85/whack/end', ['execute as @e[type=minecraft:interaction,tag=bm.gvwhup,distance=..14] at @s run function bm:p85/whack/down',
                         'execute if score @s bm.gvw >= @s bm.gvc run function bm:p85/whack/won', 'execute if score @s bm.gvw < @s bm.gvc run function bm:p85/whack/lost',
                         'function bm:p70/solved'])
    fn('p85/whack/won', big('WHACKED \'EM ALL!', 'The rats slink off - you feel strong') + pot(8) +
       [f'effect give {crew} minecraft:strength 90 0', f'particle minecraft:firework {rel(12, 7, 12)} 4 2 4 0.1 60',
        'playsound minecraft:entity.firework_rocket.twinkle block @a[distance=..20] ~ ~ ~ 1 1'])
    fn('p85/whack/lost', big('THE RATS GOT AWAY', 'They\'ll tell the guards...', 'red') + ['scoreboard players set #add bm.rng 4', 'function bm:p70/oops'])

    # ================================================================== RAT SAYS
    ORD = ['JUMP', 'SNEAK', 'LOOK UP', 'LOOK DOWN', 'FREEZE']
    prof = {'Tags': ['bm.gvprop', 'bm.gvsprof'], 'Rotation': [F(0), F(0)], 'interpolation_duration': Int(4),
            'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:rat3d_prof'}}, 'item_display': 'fixed',
            'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1.6)] * 3}}
    fn('p85/says/init', ['function bm:p70/ctx', f'summon minecraft:item_display {rel(12, 5, 3)} {snbt(prof)}',
                         label(12, 9.2, 3, [T('RAT SAYS', PARTY, bold=True)], 1.4, ('bm.gvprop', 'bm.gvsscr')),
                         sign(2.5, 7.5, 12, 'RAT SAYS', 'Do what the Professor says - but only when he says "Rat says"!')])
    fn('p85/says/tick', ['execute if score @s bm.gvs matches 3 run return 0', music,
                         'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p85/says/start',
                         'execute unless score @s bm.gvs matches 1 run return 0',
                         'scoreboard players set #len bm.rng 50', 'scoreboard players operation #q bm.rng = @s bm.gvw', 'scoreboard players operation #q bm.rng *= #k3 bm.rng',
                         'scoreboard players operation #len bm.rng -= #q bm.rng',
                         'execute if score @s bm.gvtm matches 15 if score @s bm.gvc matches 4 as @a[tag=bm.gvp,distance=..15] run function bm:p85/says/snap',
                         'execute if score @s bm.gvtm = #len bm.rng run function bm:p85/says/check',
                         'scoreboard players operation #q bm.rng = #len bm.rng', 'scoreboard players add #q bm.rng 30',
                         'execute if score @s bm.gvtm = #q bm.rng run function bm:p85/says/next'])
    fn('p85/says/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvh 0'] +
       big('RAT SAYS!', 'Only obey when he says "Rat says"') + ['function bm:p85/says/call'])
    call = ['scoreboard players set @s bm.gvtm 0', 'execute store result score @s bm.gvc run random value 0..4', 'execute store result score #r bm.rng run random value 1..10',
            'scoreboard players set @s bm.gvx 1', 'execute if score #r bm.rng matches 8.. run scoreboard players set @s bm.gvx 0',
            'execute if score @s bm.gvc matches 4 run scoreboard players set @s bm.gvx 1',
            'scoreboard players set @a[tag=bm.gvp,distance=..15] bm.gvjmp 0', f'title {crew} times 0 25 5']
    for j, o in enumerate(ORD):
        call += [f'execute if score @s bm.gvc matches {j} if score @s bm.gvx matches 1 run title {crew} title ' + snbt(T('Rat says:', PARTY, bold=True)),
                 f'execute if score @s bm.gvc matches {j} if score @s bm.gvx matches 0 run title {crew} title ' + snbt(T(' ', 'white')),
                 f'execute if score @s bm.gvc matches {j} run title {crew} subtitle ' + snbt(T(o + '!', 'white', bold=True)),
                 f'execute if score @s bm.gvc matches {j} if score @s bm.gvx matches 1 run data modify entity @e[type=minecraft:text_display,tag=bm.gvsscr,distance=..16,limit=1] text set value '
                 + snbt([T('Rat says:\n', PARTY, bold=True), T(o + '!', 'white', bold=True)]),
                 f'execute if score @s bm.gvc matches {j} if score @s bm.gvx matches 0 run data modify entity @e[type=minecraft:text_display,tag=bm.gvsscr,distance=..16,limit=1] text set value '
                 + snbt(T(o + '!', 'white', bold=True))]
    call += ['playsound minecraft:block.note_block.pling block @a[distance=..20] ~ ~ ~ 1 1.4',
             'execute as @e[type=minecraft:item_display,tag=bm.gvsprof,distance=..16] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,0.9f,0f]}}']
    fn('p85/says/call', call)
    fn('p85/says/snap', ['execute store result score @s bm.gvsx run data get entity @s Pos[0] 10', 'execute store result score @s bm.gvsz run data get entity @s Pos[2] 10'])
    fn('p85/says/check', ['scoreboard players operation #ord bm.rng = @s bm.gvc', 'scoreboard players operation #says bm.rng = @s bm.gvx',
                          'scoreboard players set #bad bm.rng 0', 'scoreboard players set #c bm.rng 0',
                          'execute as @a[tag=bm.gvp,distance=..15] at @s run function bm:p85/says/judge',
                          'execute if score #c bm.rng matches 1.. run ' + inst('bm:p75/pot_add'),
                          'execute if score #bad bm.rng matches 1.. run scoreboard players set #add bm.rng 2',
                          'execute if score #bad bm.rng matches 1.. run function bm:p70/oops',
                          'execute as @e[type=minecraft:item_display,tag=bm.gvsprof,distance=..16] run data merge entity @s {start_interpolation:0,transformation:{translation:[0f,0.5f,0f]}}'])
    fn('p85/says/judge', ['scoreboard players set #did bm.rng 0',
                          'execute if score #ord bm.rng matches 0 if score @s bm.gvjmp matches 1.. run scoreboard players set #did bm.rng 1',
                          'execute if score #ord bm.rng matches 1 if predicate bm:p20/sneaking run scoreboard players set #did bm.rng 1',
                          'execute if score #ord bm.rng matches 2 if entity @s[x_rotation=-90..-35] run scoreboard players set #did bm.rng 1',
                          'execute if score #ord bm.rng matches 3 if entity @s[x_rotation=35..90] run scoreboard players set #did bm.rng 1',
                          'execute if score #ord bm.rng matches 4 run function bm:p85/says/still',
                          'execute if score #did bm.rng = #says bm.rng run return run function bm:p85/says/right', 'function bm:p85/says/wrong'])
    fn('p85/says/still', ['execute store result score #x bm.rng run data get entity @s Pos[0] 10', 'execute store result score #z bm.rng run data get entity @s Pos[2] 10',
                          'scoreboard players operation #x bm.rng -= @s bm.gvsx', 'scoreboard players operation #z bm.rng -= @s bm.gvsz',
                          'execute if score #x bm.rng matches -3..3 if score #z bm.rng matches -3..3 if score @s bm.gvjmp matches 0 run scoreboard players set #did bm.rng 1'])
    fn('p85/says/right', ['scoreboard players add #c bm.rng 1', title('@s', 'actionbar', T('Right! +1 coin', '#7dff6a', bold=True)),
                          'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 1.3'])
    fn('p85/says/wrong', ['scoreboard players add #bad bm.rng 1', 'execute if score #says bm.rng matches 0 run ' + title('@s', 'actionbar', T('He didn\'t say "Rat says"!', 'red', bold=True)),
                          'execute if score #says bm.rng matches 1 run ' + title('@s', 'actionbar', T('Too slow - or the wrong move!', 'red', bold=True)),
                          'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 1 0.6'])
    fn('p85/says/next', ['scoreboard players add @s bm.gvw 1', 'execute if score @s bm.gvw matches 8.. run return run function bm:p85/says/end', 'function bm:p85/says/call'])
    fn('p85/says/end', big('CLASS DISMISSED', 'The Professor bows - and lets you through') + pot(5) +
       [f'effect give {crew} minecraft:regeneration 10 1', 'data modify entity @e[type=minecraft:text_display,tag=bm.gvsscr,distance=..16,limit=1] text set value '
        + snbt(T('Well listened!', PARTY, bold=True)), 'function bm:p70/solved'])

    # ================================================================== THE COIN SCRAMBLE (2+)
    coin_model = ITEMS['gutter_coin']['comps'].get('minecraft:item_model', 'minecraft:gold_nugget')
    nug = {'Item': {'id': 'minecraft:gold_nugget', 'count': Int(1), 'components': {'minecraft:custom_data': {'bm_scr': B(1)}, 'minecraft:item_model': coin_model}},
           'Age': Int(5200), 'PickupDelay': Int(0), 'Tags': ['bm.gvprop', 'bm.gvscoin']}
    ing = {'Item': {'id': 'minecraft:gold_ingot', 'count': Int(1), 'components': {'minecraft:custom_data': {'bm_scr': B(1)}, 'minecraft:item_model': coin_model,
                                                                                 'minecraft:enchantment_glint_override': True}},
           'Age': Int(5200), 'PickupDelay': Int(0), 'Tags': ['bm.gvprop', 'bm.gvscoin']}
    fn('p85/scramble/init', ['function bm:p70/ctx'] + [f'summon minecraft:marker {rel(x, H - 3, z)} {{Tags:["bm.gvprop","bm.gvchute"]}}' for (x, z) in CHUTES] +
       [sign(2.5, 7.5, 12, 'THE COIN SCRAMBLE', 'Coins rain from the chutes - grab the most! Big coins count five. The winner takes a prize.')])
    fn('p85/scramble/tick', ['execute if score @s bm.gvs matches 3 run return 0', music,
                             'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..9] run function bm:p85/scramble/start',
                             'execute unless score @s bm.gvs matches 1 run return 0',
                             'execute if score @s bm.gvtm matches 20 run ' + title(crew, 'title', T('2', PARTY, bold=True)),
                             'execute if score @s bm.gvtm matches 40 run ' + title(crew, 'title', T('1', PARTY, bold=True)),
                             'execute if score @s bm.gvtm matches 60 run ' + title(crew, 'title', T('GRAB!', GOLD, bold=True)),
                             'execute if score @s bm.gvtm matches ..59 run return 0',
                             'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #k3 bm.rng',
                             'execute if score #q bm.rng matches 0 if score @s bm.gvtm matches ..739 run function bm:p85/scramble/drop',
                             'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #60 bm.rng',
                             'execute if score #q bm.rng matches 0 if score @s bm.gvtm matches ..739 as @e[type=minecraft:marker,tag=bm.gvchute,distance=..16,sort=random,limit=1] at @s run summon minecraft:item ~ ~ ~ '
                             + snbt(ing),
                             'execute as @a[tag=bm.gvp,distance=..16] run function bm:p85/scramble/count',
                             'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #k10 bm.rng',
                             'execute if score #q bm.rng matches 0 run function bm:p85/scramble/hud',
                             'execute if score @s bm.gvtm matches 780.. run function bm:p85/scramble/end'])
    fn('p85/scramble/start', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0',
                              'scoreboard players set @a[tag=bm.gvp,distance=..20] bm.gvscr 0', 'scoreboard players set @a[tag=bm.gvp,distance=..20] bm.gvscb 0',
                              'scoreboard players set @a[tag=bm.gvp,distance=..20] bm.gvscs 0', f'title {crew} times 0 20 5',
                              title(crew, 'title', T('3', PARTY, bold=True)), title(crew, 'subtitle', T('COIN SCRAMBLE - grab the most coins!', 'gray'))])
    fn('p85/scramble/drop', ['execute as @e[type=minecraft:marker,tag=bm.gvchute,distance=..16,sort=random,limit=1] at @s run summon minecraft:item ~ ~ ~ ' + snbt(nug),
                             'execute store result score #r bm.rng run random value 1..3',
                             'execute if score #r bm.rng matches 1 as @e[type=minecraft:marker,tag=bm.gvchute,distance=..16,sort=random,limit=1] at @s run summon minecraft:item ~ ~ ~ ' + snbt(nug)])
    fn('p85/scramble/count', ['scoreboard players operation @s bm.gvscs = @s bm.gvscb', 'scoreboard players operation @s bm.gvscs *= #k5 bm.rng',
                              'scoreboard players operation @s bm.gvscs += @s bm.gvscr',
                              'clear @s *[minecraft:custom_data~{bm_scr:1b}]'])
    fn('p85/scramble/hud', ['scoreboard players set #h3 bm.rng 780', 'scoreboard players operation #h3 bm.rng -= @s bm.gvtm', 'scoreboard players operation #h3 bm.rng /= #20 bm.rng',
                            'execute as @a[tag=bm.gvp,distance=..16] run ' + title('@s', 'actionbar', [T('Your coins: ', GOLD), {'score': {'name': '@s', 'objective': 'bm.gvscs'}, 'color': 'white', 'bold': True},
                                                                                                    T('    ', 'gray'), {'score': {'name': '#h3', 'objective': 'bm.rng'}, 'color': 'yellow'},
                                                                                                    T(' s', 'yellow')])])
    fn('p85/scramble/end', ['kill @e[type=minecraft:item,tag=bm.gvscoin,distance=..24]', 'execute as @a[tag=bm.gvp,distance=..20] run function bm:p85/scramble/count',
                            'scoreboard players set #best bm.rng 0', 'scoreboard players set #c bm.rng 0',
                            'execute as @a[tag=bm.gvp,distance=..20] if score @s bm.gvscs > #best bm.rng run scoreboard players operation #best bm.rng = @s bm.gvscs',
                            'execute as @a[tag=bm.gvp,distance=..20] run scoreboard players operation #c bm.rng += @s bm.gvscs', 'scoreboard players operation #c bm.rng /= #2 bm.rng',
                            'execute if score #c bm.rng matches 1.. run ' + inst('bm:p75/pot_add'),
                            'execute as @a[tag=bm.gvp,distance=..20] run ' + tellraw('@s', P + [T('You grabbed ', 'gray'), {'score': {'name': '@s', 'objective': 'bm.gvscs'}, 'color': 'white', 'bold': True},
                                                                                             T(' coins. Half of all of it goes into the pot.', 'gray')]),
                            'execute if score #best bm.rng matches 1.. as @a[tag=bm.gvp,distance=..20] if score @s bm.gvscs = #best bm.rng at @s run function bm:p85/scramble/winner',
                            f'title {crew} times 5 40 10', title(crew, 'title', T('TIME!', GOLD, bold=True)), 'function bm:p70/solved'])
    fn('p85/scramble/winner', [tellraw('@a[tag=bm.gvp,distance=..24]', P + [{'selector': '@s', 'color': 'white', 'bold': True}, T(' wins the Coin Scramble with ', PARTY),
                                                                           {'score': {'name': '#best', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True}, T(' coins!', PARTY)]),
                               'function bm:p85/win'])

    # ================================================================== THE BUMPER BRAWL (2+)
    inner, outer = ring_cells()
    wc = P72.kit_arg('minecraft:wind_charge').replace('minecraft:custom_data={bm_kit:1b}', 'minecraft:custom_data={bm_kit:1b,bm_brawl:1b}')
    fn('p85/brawl/init', ['function bm:p70/ctx',
                          sign(2.5, 7.5, 12, 'THE BUMPER BRAWL', 'Step into the ring. Wind charges for everyone - blow your crewmates off! Last one standing wins.')])
    gallery = f'tp @s {rel(2, 4, 12)} 90 0'                      # (only ever run positioned at the room's marker)
    fn('p85/brawl/tick', ['execute if score @s bm.gvs matches 3 run return 0', music,
                          f'execute if score @s bm.gvs matches 0 positioned {rel(12, 4, 12)} if entity @a[tag=bm.gvp,distance=..4] run function bm:p85/brawl/ready',
                          'execute if score @s bm.gvs matches 1 run function bm:p85/brawl/count',
                          'execute if score @s bm.gvs matches 2 run function bm:p85/brawl/fight'])
    fn('p85/brawl/ready', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', f'title {crew} times 0 25 5',
                           title(crew, 'title', T('BUMPER BRAWL', PARTY, bold=True)), title(crew, 'subtitle', T('Into the ring - five seconds!', 'gray')),
                           'playsound minecraft:block.note_block.bell block @a[distance=..20] ~ ~ ~ 1 1'])
    fn('p85/brawl/count', ['execute if score @s bm.gvtm matches 40 run ' + title(crew, 'title', T('3', PARTY, bold=True)),
                           'execute if score @s bm.gvtm matches 60 run ' + title(crew, 'title', T('2', PARTY, bold=True)),
                           'execute if score @s bm.gvtm matches 80 run ' + title(crew, 'title', T('1', PARTY, bold=True)),
                           'execute if score @s bm.gvtm matches 100.. run function bm:p85/brawl/go'])
    fn('p85/brawl/go', ['scoreboard players set @s bm.gvs 2', 'scoreboard players set @s bm.gvtm 0',
                        f'execute positioned {rel(12, 4, 12)} run tag @a[tag=bm.gvp,distance=..7.4] add bm.gvbr'] +
       [f'setblock {rel(x, FY, z)} minecraft:air' for (x, z) in BRIDGE_IN] +
       [f'execute as @a[tag=bm.gvp,tag=!bm.gvbr,distance=..20] run {gallery}',
        f'execute as @a[tag=bm.gvbr,distance=..20] run give @s {wc} 16', f'title {crew} times 0 20 5', title(crew, 'title', T('BRAWL!', GOLD, bold=True)),
        'playsound minecraft:entity.wind_charge.wind_burst block @a[distance=..20] ~ ~ ~ 1 0.8',
        'execute store result score #n bm.rng if entity @a[tag=bm.gvbr,distance=..20]', 'execute if score #n bm.rng matches ..1 run function bm:p85/brawl/nocontest'])
    low = f'positioned {rel(12, 4, 12)} positioned ~-12 ~-6 ~-12'           # (the pit: feet below the ring's top)
    fn('p85/brawl/fight', [f'execute positioned {rel(12, 4, 12)} as @a[tag=bm.gvbr,distance=7.8..] run tag @s add bm.gvbro',
                           f'execute {low} as @a[tag=bm.gvbr,dx=24,dy=4.5,dz=24] run tag @s add bm.gvbro',
                           'execute as @a[tag=bm.gvbro] at @s run function bm:p85/brawl/out', f'tp @a[tag=bm.gvbro] {rel(2, 4, 12)} 90 0', 'tag @a remove bm.gvbro',
                           f'execute {low} as @a[tag=bm.gvp,tag=!bm.gvbr,dx=24,dy=4.5,dz=24] run tag @s add bm.gvbro',
                           f'tp @a[tag=bm.gvbro] {rel(2, 4, 12)} 90 0', 'tag @a remove bm.gvbro',
                           'execute if score @s bm.gvtm matches 500 run ' + title(crew, 'actionbar', T('The ring is crumbling!', 'red', bold=True)),
                           'execute if score @s bm.gvtm matches 600 run function bm:p85/brawl/shrink',
                           'execute store result score #n bm.rng if entity @a[tag=bm.gvbr,distance=..24]',
                           'execute if score #n bm.rng matches ..1 run return run function bm:p85/brawl/end',
                           'execute if score @s bm.gvtm matches 1200.. run function bm:p85/brawl/end'])
    fn('p85/brawl/out', ['tag @s remove bm.gvbr', 'clear @s minecraft:wind_charge[minecraft:custom_data~{bm_brawl:1b}]',
                         tellraw('@a[tag=bm.gvp,distance=..30]', P + [{'selector': '@s', 'color': 'white'}, T(' is out of the ring!', PARTY)]),
                         'playsound minecraft:entity.generic.splash player @a[distance=..20] ~ ~ ~ 1 1'])
    fn('p85/brawl/shrink', [f'setblock {rel(x, FY, z)} minecraft:air' for (x, z) in outer] +
       ['playsound minecraft:block.stone.break block @a[distance=..20] ~ ~ ~ 1 0.6', f'particle minecraft:poof {rel(12, 4, 12)} 6 0.2 6 0.02 60'])
    fn('p85/brawl/nocontest', [tellraw('@a[tag=bm.gvp,distance=..30]', P + [T('Only one in the ring - no contest. The rats wave you on.', 'gray')]), 'function bm:p85/brawl/finish'])
    fn('p85/brawl/end', ['execute as @a[tag=bm.gvbr,distance=..24] at @s run function bm:p85/brawl/winner', 'function bm:p85/brawl/finish'])
    fn('p85/brawl/winner', [tellraw('@a[tag=bm.gvp,distance=..30]', P + [{'selector': '@s', 'color': 'white', 'bold': True}, T(' wins the Bumper Brawl!', PARTY, bold=True)]),
                            'function bm:p85/win'])
    fn('p85/brawl/finish', ['tag @a remove bm.gvbr', 'clear @a[tag=bm.gvp,distance=..30] minecraft:wind_charge[minecraft:custom_data~{bm_brawl:1b}]'] +
       [f'setblock {rel(x, FY, z)} minecraft:spruce_planks' for (x, z) in BRIDGE_IN + BRIDGE_OUT] +
       [f'setblock {rel(x, FY, z)} minecraft:red_concrete' for (x, z) in outer] +
       [f'title {crew} times 5 40 10', title(crew, 'title', T('WHAT A BRAWL', PARTY, bold=True)), 'function bm:p70/solved'])


def rp(R):
    pass
