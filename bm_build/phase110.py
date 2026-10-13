"""2.69: THREE WAYS THROUGH EVERY PUZZLE (I) - each puzzle room is now one of three variants, drawn when the heist is laid
(each its own solution, not the old one in new paint), plus the vault's no-shortcut rules.

THE COMBINATION ROOM   A  the ledger's gold-and-coal frames, read in the mirror (as before)
                       B  THE WEIGHED LEDGER: each lever carries a number; pull the ones that add up to the ledger's sum
                       C  THE LOGIC LEDGER: no picture at all - three to five clues ("Levers II and IV are set differently...")
                          pin down the one setting that fits them all
THE WEIGHING ROOM      A  every golden scale at once (as before)
                       B  THE ORDER OF THE SCALES: four scales marked crown, key, coin and skull; a riddle gives the order -
                          step on them one at a time (only feet count), all four before the scales say yes or no
                       C  THE BATON RUN: carry the Relay Baton to the scale that lights up before its light runs out - five
                          to seven in a row (the next is always a neighbouring corner); one baton, so camping doesn't help
THE GAUNTLET           A  the sweeping laser planes (as before)
                       B  THE LOW AND THE HIGH: the beams never go out - red ones at your ankles (jump them), violet ones
                          at head height (sneak beneath them)
                       C  THE MIRROR GAUNTLET: a laser crosses the hall; turn the glass mirrors (right-click) until the beam
                          strikes the target. Exactly one setting does, and it bends the beam four times or more
THE TILE FLOOR         A  the hidden path and the peek button (as before)
                       B  THE COLOUR TRAIL: every tile is coloured; follow the colours in the sign's order from a tile by the
                          door - only one trail reaches the far side
                       C  THE COUNTED FLOOR: numbers along the edges say how many safe tiles lie in each row and column; the
                          path never turns back toward the door (one or two tiles may be shown to get you going)

NO SHORTCUTS: the tile floors judge the tile you're over (not just its middle), so creeping along the seams between tiles
  drops you like any other false step. In the rooms you cross on foot (the tiles, the rafters, the gauntlet, the bell tower)
  the Fixer holds your wind charges and ender pearls until you're through (they come back the moment you leave the room).
YOUR SECONDARY: the crossbow is a melee kit's way to shoot; a Ranged raider (who already carries a bow) who picks it gets
  a battle axe instead.
TESTING: admin/variant_a | _b | _c | _random forces the variant of every puzzle room laid from then on; admin/rooms_only_<kind>
  lays nothing but that kind of room (no events) until admin/rooms_any.
"""
import math
from items import T
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase72 as P72
import phase75 as P75
import phase75_rooms as R5
import phase80 as P80
import p110data as PD

GOLD = '#ffcf40'
rel = RM.rel
IDENT = [F(0), F(0), F(0), F(1)]


def relf(x, y, z):
    """a point in a room's local coordinates (not a block's centre) relative to its marker"""
    f = lambda v: '~' if abs(v) < 1e-9 else f'~{round(v, 3):g}'
    return f'{f(x - 12.5)} {f(y - 4)} {f(z - 12.5)}'


# ---------------------------------------------------------------- the crossbow secondary: not for the Ranged kit (it already shoots)
_s = P80.SECONDARY[0]
P80.SECONDARY[0] = (_s[0], 'a crossbow (Quick Charge) and 16 arrows - the Ranged kit, which already shoots, gets a battle axe', _s[2], _s[3])
AXE = ('minecraft:iron_axe', 1, {'minecraft:enchantments': {'minecraft:sharpness': 1}})

V70 = ['levers', 'plates', 'lasers', 'tiles', 'dial', 'coffers']
TRAV = ['tiles', 'rafters', 'lasers', 'climb']          # rooms crossed on foot: wind charges and pearls are held at the door


def kf(k, part):
    return f'p70/r/{k}/{part}' if k in V70 else f'p76/r/{k}/{part}'


def dispatch(G, k, b, c):
    """route a puzzle kind's init (and tick, where the variant has its own) to variants B and C; b, c = (init, tick or None)"""
    G.FUNCS[kf(k, 'init')][0:0] = ['function bm:p110/var', f'execute if score @s bm.gvvar matches 1 run return run function bm:{b[0]}',
                                   f'execute if score @s bm.gvvar matches 2 run return run function bm:{c[0]}']
    G.FUNCS[kf(k, 'tick')][0:0] = [f'execute if score @s bm.gvvar matches {i + 1} run return run function bm:{v[1]}' for i, v in enumerate((b, c)) if v[1]]


def helpers(G):
    """label/sign/button/theme helpers shared by the variant phases"""
    def label(pos, text, scale=0.55, bill='center', tags=(), yaw=None, width=220, bg=True):
        d = {'Tags': ['bm.gvprop'] + list(tags), 'billboard': bill, 'brightness': {'block': 15, 'sky': 15}, 'text': text, 'alignment': 'center',
             'line_width': Int(width), 'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}}
        if bg: d['background'] = Int(0x90000000 - 2 ** 32)
        if yaw is not None: d['Rotation'] = [F(yaw), F(0)]
        return f'summon minecraft:text_display {pos} ' + snbt(d)
    def sign(pos, title_, body, scale=0.6, yaw=None, col=GOLD, width=220):
        return label(pos, [T(title_ + '\n', col, bold=True), T(body, 'gray')], scale, 'vertical' if yaw is None else 'fixed', yaw=yaw, width=width)
    def vbutton(x, y, z, facing, text, face='wall', col=GOLD):
        return [f'setblock {rel(x, y, z)} minecraft:pale_oak_button[face={face},facing={facing},powered=false]',
                label(relf(x + 0.5, y + (0.7 if face == 'wall' else 0.55), z + 0.5), T(text, col, bold=True), 0.45)]
    def press(name, pos, then):
        return [f'execute if block {rel(*pos)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvl_{name}] run function {then}',
                f'execute if block {rel(*pos)} minecraft:pale_oak_button[powered=true] run tag @s add bm.gvl_{name}',
                f'execute unless block {rel(*pos)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvl_{name}']
    def themed(tpl, key):
        """tpl with {b} = the room's own block (its tier's theme, or the Vorn's steel in an alien heist)"""
        return [f'execute if score #gsf bm.rng matches 1 run ' + tpl.format(b=R5.THEMES[6][key])] + \
               [f'execute unless score #gsf bm.rng matches 1 if score #gt bm.rng matches {t} run ' + tpl.format(b=R5.THEMES[t][key]) for t in range(1, 6)]
    def crew_say(txt, col='gray', r=24):
        return f'execute as @a[tag=bm.gvp,distance=..{r}] run ' + G.title('@s', 'actionbar', T(txt, col) if isinstance(txt, str) else txt)
    def oops(n):
        return [f'scoreboard players set #add bm.rng {n}', 'function bm:p70/oops']
    def choose(score, n, fname):
        """a random 0..n-1 into #i, then run fname{i}"""
        return [f'execute store result score #i bm.rng run random value 0..{n - 1}'] + \
               [f'execute if score #i bm.rng matches {i} run function bm:{fname}{i}' for i in range(n)]
    return label, sign, vbutton, press, themed, crew_say, oops, choose


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    label, sign, vbutton, press, themed, crew_say, oops, choose = helpers(G)
    objs = ['bm.gvvar', 'bm.gvy1', 'bm.gvy2', 'bm.gvy3', 'bm.gvhw', 'bm.gvhe']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== the kit: a Ranged raider's crossbow is a battle axe
    ext = G.FUNCS['p80/kit/extras']
    ka = P72.kit_arg
    G.FUNCS['p80/kit/extras'] = [l.replace('execute if score @s bm.ksec matches 1 run ', 'execute if score @s bm.ksec matches 1 unless score @s bm.gvrole matches 3 run ')
                                 for l in ext] + [f'execute if score @s bm.ksec matches 1 if score @s bm.gvrole matches 3 run give @s {ka(AXE[0], extra=AXE[2])} {AXE[1]}']

    # ================================================================== the draw: which variant (and, for testing, which kind)
    fn('p110/var', ['execute store result score @s bm.gvvar run random value 0..2',
                    'execute if score #pvar bm.gvv matches 1..3 run scoreboard players operation @s bm.gvvar = #pvar bm.gvv',
                    'execute if score #pvar bm.gvv matches 1..3 run scoreboard players remove @s bm.gvvar 1'])
    for i, v in enumerate('abc'):
        fn(f'admin/variant_{v}', [f'scoreboard players set #pvar bm.gvv {i + 1}', tellraw('@s', P + [T(f'Every puzzle room laid from now on is variant {v.upper()} (admin/variant_random to stop).', 'gray')])])
    fn('admin/variant_random', ['scoreboard players set #pvar bm.gvv 0', tellraw('@s', P + [T('Puzzle variants back to chance.', 'gray')])])
    for j, k in enumerate(P75.KINDS):
        fn(f'admin/rooms_only_{k}', [f'scoreboard players set #frk bm.gvv {j + 1}', tellraw('@s', P + [T(f'Heists laid from now on are all {k} rooms (admin/rooms_any to stop).', 'gray')])])
    fn('admin/rooms_any', ['scoreboard players set #frk bm.gvv 0', tellraw('@s', P + [T('Heist rooms back to the usual draw.', 'gray')])])
    G.FUNCS['p75/lay/pick'].insert(0, 'execute if score #frk bm.gvv matches 1.. run return run function bm:p110/lay/forced')
    fn('p110/lay/forced', ['scoreboard players operation #r bm.rng = #frk bm.gvv', 'scoreboard players remove #r bm.rng 1'])
    G.FUNCS['p75/lay/can_event'].insert(0, 'execute if score #frk bm.gvv matches 1.. run return 0')

    # ================================================================== NO SHORTCUTS (1): the floor judges the tile you're over
    tt = G.FUNCS['p70/r/tiles/tick']
    k = next(i for i, l in enumerate(tt) if 'bm.gvsafe=0},tag=!bm.gvdown] at @s if entity @a[tag=bm.gvp,distance=..1.15]' in l)
    tt[k] = (f'execute positioned {relf(3.3, 3.5, 5.3)} as @a[tag=bm.gvp,dx=16.4,dy=3.5,dz=13.4] at @s as @e[type=minecraft:marker,tag=bm.gvtile,distance=..3,'
             'sort=nearest,limit=1] if score @s bm.gvsafe matches 0 unless entity @s[tag=bm.gvdown] at @s run function bm:p70/r/tiles/drop')
    tt[k] = tt[k].replace('distance=..3,sort=nearest', 'distance=..3.5,sort=nearest')
    # (and nobody crosses the floor in the air: higher than a jump over it - back to the start)
    def nofly(room, x0, z0, x1, z1, start):
        fn(f'p110/nofly/{room}', [f'execute at @e[type=minecraft:marker,tag=bm.gvr_{room},distance=..30,sort=nearest,limit=1] run tp @s {rel(*start)} -90 0',
                                  'playsound minecraft:entity.breeze.wind_burst player @a[distance=..16] ~ ~ ~ 1 0.6',
                                  title('@s', 'actionbar', [T('No flying! ', 'red', bold=True), T('Back to the start - this one is crossed on foot.', 'gray')])])
        return f'execute positioned {relf(x0, 8.1, z0)} as @a[tag=bm.gvp,dx={x1 - x0 - 1},dy=12,dz={z1 - z0 - 1}] at @s run function bm:p110/nofly/{room}'
    tt.insert(k + 1, nofly('tiles', 3, 1, 21, 24, (1, 4, 12)))
    G.FUNCS['p76/r/rafters/tick'].insert(3, nofly('rafters', 3, 1, 22, 24, (1, 4, 12)))
    G.FUNCS['p70/r/lasers/tick'].insert(2, nofly('lasers', 3, 6, 22, 19, (2, 4, 12)))
    # (a tile comes back with its colour, where it has one)
    G.FUNCS['p70/r/tiles/refill_base'] = G.FUNCS['p70/r/tiles/refill']
    fn('p70/r/tiles/refill', ['function bm:p70/r/tiles/refill_base'] +
       sum(([f'execute if score @s bm.gvy1 matches {i} run fill ~ ~-1 ~-1 ~ ~-1 ~1 minecraft:{c}_concrete',
             f'execute if score @s bm.gvy1 matches {i} run fill ~-1 ~-1 ~ ~1 ~-1 ~ minecraft:{c}_concrete'] for i, c in enumerate(PD.COLS)), []))

    # ================================================================== NO SHORTCUTS (2): wind charges and pearls held at the door of the rooms you cross on foot
    G.FUNCS['p70/r/init'][0:0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvtrav' for k in TRAV]
    G.FUNCS['tick'].append('execute in bm:gutter if entity @a[tag=bm.gvp,distance=0..,limit=1] run function bm:p110/cust/check')
    fn('p110/cust/check', ['tag @a[tag=bm.gvp] remove bm.gvin110',
                           'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvtrav,scores={bm.gvs=0..2}] at @s positioned ~-12.5 ~-4 ~-12.5 '
                           'as @a[tag=bm.gvp,dx=24,dy=30,dz=24] run function bm:p110/cust/take',
                           'execute as @a[tag=bm.gvheld,tag=!bm.gvin110] run function bm:p110/cust/back'])
    fn('p110/cust/take', ['tag @s add bm.gvin110',
                          'execute store result score #n bm.rng run clear @s minecraft:wind_charge 0',
                          'execute if score #n bm.rng matches 1.. run scoreboard players operation @s bm.gvhw += #n bm.rng',
                          'execute if score #n bm.rng matches 1.. run clear @s minecraft:wind_charge',
                          'execute store result score #m bm.rng run clear @s minecraft:ender_pearl 0',
                          'execute if score #m bm.rng matches 1.. run scoreboard players operation @s bm.gvhe += #m bm.rng',
                          'execute if score #m bm.rng matches 1.. run clear @s minecraft:ender_pearl',
                          'scoreboard players operation #n bm.rng += #m bm.rng',
                          'execute if score #n bm.rng matches 1.. run tag @s add bm.gvheld',
                          'execute if score #n bm.rng matches 1.. run ' + title('@s', 'actionbar', [T('No shortcuts: ', GOLD, bold=True),
                                                                                                   T('the Fixer holds your wind charges and pearls till you\'re through this room.', 'gray')])])
    fn('p110/cust/back', ['tag @s remove bm.gvheld',
                          'execute store result storage bm:gv cust.w int 1 run scoreboard players get @s bm.gvhw',
                          'execute store result storage bm:gv cust.e int 1 run scoreboard players get @s bm.gvhe',
                          'execute if score @s bm.gvhw matches 1.. run function bm:p110/cust/give_w with storage bm:gv cust',
                          'execute if score @s bm.gvhe matches 1.. run function bm:p110/cust/give_e with storage bm:gv cust',
                          'scoreboard players set @s bm.gvhw 0', 'scoreboard players set @s bm.gvhe 0'])
    fn('p110/cust/give_w', [f'$give @s {ka("minecraft:wind_charge")} $(w)'])
    fn('p110/cust/give_e', ['$give @s minecraft:ender_pearl $(e)'])
    # (leaving the heist from inside such a room: the loaned wind charges stay in the vault, your own pearls come home)
    G.FUNCS['p70/unraid'] += ['scoreboard players set @s bm.gvhw 0', 'execute if entity @s[tag=bm.gvheld] run function bm:p110/cust/back']

    # ================================================================== THE COMBINATION ROOM
    LV = [8, 10, 12, 14, 16]
    BTN = (12, 7, 23)
    def lever_tags():                              # (seen from the room, lever I is on the left: x 16)
        return [label(relf(x + 0.5, 6.15, 23.85), T(PD.ROMAN[(16 - x) // 2], GOLD, bold=True), 0.7, 'fixed', yaw=180, bg=False) for x in LV]
    hint = label(relf(12.5, 8, 22.9), T('Set the levers, then press the button.', 'gray'), 0.6, 'fixed', yaw=180)
    # ---- B: the weighed ledger (the numbers 1, 2, 4, 8, 16 shuffled over the levers - one way to make any sum)
    import random as _r
    rr = _r.Random(6905)
    WPERM = []
    while len(WPERM) < 6:
        p = [1, 2, 4, 8, 16]; rr.shuffle(p)
        if p not in WPERM: WPERM.append(p)
    TGT = [n for n in range(3, 32) if 2 <= bin(n).count('1') <= 4]
    fn('p110/levers/b/init', ['function bm:p70/ctx', 'execute store result score @s bm.gvx run random value 0..5',
                              f'execute store result score #i bm.rng run random value 0..{len(TGT) - 1}'] +
       [f'execute if score #i bm.rng matches {i} run scoreboard players set @s bm.gvc {n}' for i, n in enumerate(TGT)] +
       [f'execute if score @s bm.gvx matches {p} run ' + label(relf(x + 0.5, 6.1, 23.85), T(str(w), GOLD, bold=True), 0.8, 'fixed', yaw=180, bg=False)
        for p, ws in enumerate(WPERM) for x, w in zip(LV, ws)] +
       ['execute store result storage bm:gv v110.n int 1 run scoreboard players get @s bm.gvc', 'function bm:p110/levers/b/sign with storage bm:gv v110'] +
       vbutton(*BTN, 'north', 'TRY THE LEVERS') + [hint])
    fn('p110/levers/b/sign', ['$' + label(relf(12.5, 5.6, 2.05), [T('THE WEIGHED LEDGER\n', GOLD, bold=True), T('Pull the levers whose numbers add up to exactly ', 'gray'),
                                                       T('$(n)', 'white', bold=True), T('.', 'gray')], 0.7, 'fixed', width=200)])
    fn('p110/levers/b/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                              f'execute if block {rel(*BTN)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvlatch] run function bm:p110/levers/b/try',
                              f'execute unless block {rel(*BTN)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvlatch'])
    fn('p110/levers/b/try', ['tag @s add bm.gvlatch', 'scoreboard players set #sum bm.rng 0'] +
       [f'execute if score @s bm.gvx matches {p} if block {rel(x, 5, 23)} minecraft:lever[powered=true] run scoreboard players add #sum bm.rng {w}'
        for p, ws in enumerate(WPERM) for x, w in zip(LV, ws)] +
       ['execute if score #sum bm.rng = @s bm.gvc run return run function bm:p70/solved'] + oops(15) +
       [f'setblock {rel(x, 5, 23)} minecraft:lever[face=wall,facing=north,powered=false]' for x in LV] +
       ['playsound minecraft:block.anvil.land block @a[distance=..24] ~ ~ ~ 0.6 0.6',
        crew_say([T('Those come to ', 'red'), {'score': {'name': '#sum', 'objective': 'bm.rng'}, 'color': 'white'}, T(' - wrong. The levers snap back.', 'red')], r=20)])
    # ---- C: the logic ledger
    LP = PD.lever_puzzles()
    fn('p110/levers/c/init', ['function bm:p70/ctx'] + choose('#i', len(LP), 'p110/levers/c/p') + lever_tags() + vbutton(*BTN, 'north', 'TRY THE LEVERS') + [hint])
    for j, (pat, clues) in enumerate(LP):
        mask = sum(1 << i for i in range(5) if (pat >> (4 - i)) & 1)        # (phase70's try reads bit i as the lever at LV[i])
        body = '\n'.join(f'{n + 1}. {c}' for n, c in enumerate(clues))
        fn(f'p110/levers/c/p{j}', [f'scoreboard players set @s bm.gvc {mask}',
                                   label(relf(12.5, 4.9, 2.05), [T('THE LOGIC LEDGER\n', GOLD, bold=True), T(body + '\n', 'white'),
                                                                 T('(Every line is true. One setting fits.)', 'dark_gray')], 0.5, 'fixed', tags=('bm.gvboard',), width=330)])
    dispatch(G, 'levers', ('p110/levers/b/init', 'p110/levers/b/tick'), ('p110/levers/c/init', None))

    # ================================================================== THE WEIGHING ROOM
    PL = [(5, 5), (19, 5), (5, 19), (19, 19)]
    SYMI = {'crown': 'minecraft:golden_helmet', 'key': 'minecraft:trial_key', 'coin': 'minecraft:gold_nugget', 'skull': 'minecraft:wither_skeleton_skull'}
    ORD = PD.order_puzzles()
    PLACE = [list(p) for p in __import__('itertools').permutations(range(4))]
    # ---- B: the order of the scales
    fn('p110/plates/b/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvy3 0'] +
       choose('#i', len(ORD), 'p110/plates/b/o') + choose('#i', len(PLACE), 'p110/plates/b/q') +
       [f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvsym{s},distance=..14] bm.gvy1 {s}' for s in range(4)])
    for o, (order, clues) in enumerate(ORD):
        enc = sum(s * 4 ** i for i, s in enumerate(order))
        body = '\n'.join(clues)
        fn(f'p110/plates/b/o{o}', [f'scoreboard players set @s bm.gvy2 {enc}',
                                   sign(rel(12, 7, 1), 'THE ORDER OF THE SCALES', body + '\nStep on the four scales one at a time, in that order.', 0.6)])
    for q, pl in enumerate(PLACE):
        L = []
        for j, (x, z) in enumerate(PL):
            s = pl[j]; nm = PD.SYMS[s]
            L += [f'summon minecraft:marker {rel(x, 4, z)} {{Tags:["bm.gvprop","bm.gvpl","bm.gvsym{s}"]}}',
                  f'summon minecraft:item_display {relf(x + 0.5, 5.7, z + 0.5)} ' + snbt({'Tags': ['bm.gvprop'], 'billboard': 'vertical', 'item': {'id': SYMI[nm], 'count': Int(1)},
                                                                                     'item_display': 'fixed', 'brightness': {'block': 15, 'sky': 15},
                                                                                     'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.9)] * 3}}),
                  label(relf(x + 0.5, 6.5, z + 0.5), T(nm.upper(), GOLD, bold=True), 0.5)]
        fn(f'p110/plates/b/q{q}', L)
    fn('p110/plates/b/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                              'scoreboard players set #new bm.rng 0',
                              'execute as @e[type=minecraft:marker,tag=bm.gvpl,distance=..14] at @s run function bm:p110/plates/b/chk',
                              'execute if score #new bm.rng matches 2.. run function bm:p110/plates/b/wrong',
                              'execute if score #new bm.rng matches 1 run function bm:p110/plates/b/step',
                              'tag @e[type=minecraft:marker,tag=bm.gvplnew,distance=..14] remove bm.gvplnew',
                              'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #8 bm.rng',
                              'execute if score #q bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.gvplused,distance=..14] at @s run particle minecraft:wax_on ~ ~0.3 ~ 0.3 0.1 0.3 0 3'])
    fn('p110/plates/b/chk', ['execute store success score #on bm.rng if entity @a[tag=bm.gvp,distance=..0.8]',
                             'execute if score #on bm.rng matches 0 run return run tag @s remove bm.gvocc',
                             'execute if entity @s[tag=bm.gvocc] run return 0', 'tag @s add bm.gvocc',
                             'execute if entity @s[tag=bm.gvplused] run return 0',
                             'tag @s add bm.gvplnew', 'scoreboard players add #new bm.rng 1', 'scoreboard players operation #sym bm.rng = @s bm.gvy1'])
    fn('p110/plates/b/step', [f'execute if score @s bm.gvw matches {i} run scoreboard players operation #sym bm.rng *= #pw{i} bm.rng' for i in range(4)] +
       ['scoreboard players operation @s bm.gvy3 += #sym bm.rng', 'scoreboard players add @s bm.gvw 1',
        'tag @e[type=minecraft:marker,tag=bm.gvplnew,distance=..14] add bm.gvplused',
        'execute at @e[type=minecraft:marker,tag=bm.gvplnew,distance=..14] run playsound minecraft:block.note_block.chime block @a[distance=..24] ~ ~ ~ 1 1.2',
        crew_say([T('Scale ', 'gray'), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_plates,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                  T(' of 4 tips.', 'gray')], r=20),
        'execute if score @s bm.gvw matches 4.. run function bm:p110/plates/b/judge'])
    fn('p110/plates/b/judge', ['execute if score @s bm.gvy3 = @s bm.gvy2 run return run function bm:p70/solved', 'function bm:p110/plates/b/wrong'])
    fn('p110/plates/b/wrong', oops(8) + ['scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvy3 0',
                                         'tag @e[type=minecraft:marker,tag=bm.gvplused,distance=..14] remove bm.gvplused',
                                         'playsound minecraft:block.anvil.land block @a[distance=..24] ~ ~ ~ 0.5 0.6',
                                         crew_say('Wrong - the scales clatter back. Start again (one at a time).', 'red', 20)])
    # ---- C: the baton run
    BATON = 'minecraft:blaze_rod[minecraft:custom_data={bm_room:1b,bm_baton:1b},minecraft:item_name=' + snbt(T('Relay Baton', GOLD)) + \
            ',minecraft:lore=[' + snbt(T('Carry it to the scale that lights up.', 'gray')) + '],minecraft:enchantment_glint_override=true]'
    ADJ = {0: (1, 2), 1: (0, 3), 2: (0, 3), 3: (1, 2)}
    fn('p110/plates/c/init', ['function bm:p70/ctx', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvc -1',
                              'scoreboard players set @s bm.gvy2 6', 'execute if score #gt bm.rng matches ..2 run scoreboard players set @s bm.gvy2 5',
                              'execute if score #gt bm.rng matches 4.. run scoreboard players set @s bm.gvy2 7',
                              'scoreboard players set @s bm.gvy1 80', 'execute if score #gt bm.rng matches 4.. run scoreboard players set @s bm.gvy1 64',
                              sign(rel(12, 7, 1), 'THE BATON RUN', 'Carry the Relay Baton to the scale that lights up - before its light runs out. '
                                   'Five in a row (more on the higher tiers). One baton for the whole crew.', 0.6)])
    fn('p110/plates/c/tick', ['execute if score @s bm.gvs matches 3 run return 0',
                              'execute if score @s bm.gvs matches 0 if entity @a[tag=bm.gvp,distance=..10] run function bm:p110/plates/c/start',
                              'execute if score @s bm.gvs matches 0 run return 0',
                              'tag @a[tag=bm.gvp,distance=..30] remove bm.gvbat',
                              'execute as @a[tag=bm.gvp,distance=..30] if function bm:p110/plates/c/has run tag @s add bm.gvbat'] +
       [f'execute if score @s bm.gvc matches {j} positioned {rel(x, 4, z)} if entity @a[tag=bm.gvbat,distance=..0.9] positioned as @s run return run function bm:p110/plates/c/catch'
        for j, (x, z) in enumerate(PL)] +
       ['scoreboard players remove @s bm.gvx 1', 'execute if score @s bm.gvx matches ..0 run return run function bm:p110/plates/c/miss',
        'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #2 bm.rng'] +
       [f'execute if score #q bm.rng matches 0 if score @s bm.gvc matches {j} run particle minecraft:end_rod {relf(x + 0.5, 4.3, z + 0.5)} 0.25 1.5 0.25 0.02 4'
        for j, (x, z) in enumerate(PL)] +
       ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #10 bm.rng',
        'execute if score #q bm.rng matches 0 run function bm:p110/plates/c/bar',
        'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
        'execute if score #q bm.rng matches 0 unless entity @a[tag=bm.gvbat,distance=..30] run function bm:p110/plates/c/lost'])
    fn('p110/plates/c/has', ['execute if items entity @s container.* *[minecraft:custom_data~{bm_baton:1b}] run return 1',
                             'execute if items entity @s weapon.offhand *[minecraft:custom_data~{bm_baton:1b}] run return 1', 'return 0'])
    fn('p110/plates/c/bar', ['scoreboard players operation #s bm.rng = @s bm.gvx', 'scoreboard players operation #s bm.rng /= #20 bm.rng',
                             'scoreboard players operation #t bm.rng = @s bm.gvx', 'scoreboard players operation #t bm.rng %= #20 bm.rng',
                             'scoreboard players operation #t bm.rng /= #2 bm.rng',
                             crew_say([T('Baton run: ', GOLD, bold=True), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_plates,limit=1,sort=nearest]', 'objective': 'bm.gvw'}, 'color': 'white'},
                                       T(' of ', 'gray'), {'score': {'name': '@e[type=minecraft:marker,tag=bm.gvr_plates,limit=1,sort=nearest]', 'objective': 'bm.gvy2'}, 'color': 'white'},
                                       T('   ', 'gray'), {'score': {'name': '#s', 'objective': 'bm.rng'}, 'color': 'yellow'}, T('.', 'yellow'),
                                       {'score': {'name': '#t', 'objective': 'bm.rng'}, 'color': 'yellow'}, T(' s', 'yellow')], r=30)])
    fn('p110/plates/c/start', ['scoreboard players set @s bm.gvs 1', 'function bm:p110/plates/c/give',
                               'execute store result score @s bm.gvc run random value 0..3', 'scoreboard players set @s bm.gvx 100', 'function bm:p110/plates/c/ding'])
    fn('p110/plates/c/give', ['clear @a[tag=bm.gvp,distance=..60] *[minecraft:custom_data~{bm_baton:1b}]',
                              'execute as @e[type=minecraft:item,distance=..30] if items entity @s contents *[minecraft:custom_data~{bm_baton:1b}] run kill @s',
                              f'give @p[tag=bm.gvp,distance=..24] {BATON}',
                              'execute as @p[tag=bm.gvp,distance=..24] run ' + title('@s', 'actionbar', [T('You have the Relay Baton. ', GOLD, bold=True), T('Run it to the glowing scale!', 'gray')])])
    fn('p110/plates/c/lost', ['execute as @e[type=minecraft:item,distance=..30] if items entity @s contents *[minecraft:custom_data~{bm_baton:1b}] run return 0',
                              'function bm:p110/plates/c/give'])
    fn('p110/plates/c/ding', [f'execute if score @s bm.gvc matches {j} run playsound minecraft:block.note_block.bell block @a[distance=..30] {rel(x, 5, z)} 1 1.4'
                              for j, (x, z) in enumerate(PL)])
    fn('p110/plates/c/catch', ['scoreboard players add @s bm.gvw 1', 'playsound minecraft:entity.experience_orb.pickup block @a[distance=..30] ~ ~ ~ 1 1.2',
                               'execute if score @s bm.gvw >= @s bm.gvy2 run return run function bm:p110/plates/c/won',
                               'execute store result score #r bm.rng run random value 0..1'] +
       [f'execute if score @s bm.gvc matches {j} if score #r bm.rng matches {i} run return run function bm:p110/plates/c/next{n}' for j, ns in ADJ.items() for i, n in enumerate(ns)])
    for n in range(4):
        fn(f'p110/plates/c/next{n}', [f'scoreboard players set @s bm.gvc {n}', 'scoreboard players operation @s bm.gvx = @s bm.gvy1', 'function bm:p110/plates/c/ding'])
    fn('p110/plates/c/miss', oops(5) + ['scoreboard players set @s bm.gvf 1', 'scoreboard players set @s bm.gvw 0',
                                        'execute store result score @s bm.gvc run random value 0..3', 'scoreboard players set @s bm.gvx 100', 'function bm:p110/plates/c/ding',
                                        'playsound minecraft:block.note_block.didgeridoo block @a[distance=..30] ~ ~ ~ 1 0.6',
                                        crew_say('Too slow! The light went out - the run starts over.', 'red', 30)])
    fn('p110/plates/c/won', ['clear @a[tag=bm.gvp,distance=..60] *[minecraft:custom_data~{bm_baton:1b}]', 'function bm:p70/solved'])
    dispatch(G, 'plates', ('p110/plates/b/init', 'p110/plates/b/tick'), ('p110/plates/c/init', 'p110/plates/c/tick'))

    # ================================================================== THE GAUNTLET
    LZ = [5, 9, 13, 17, 21]
    # ---- B: low and high beams (two or three high)
    LPAT = [p for p in range(32) if 2 <= bin(p).count('1') <= 3]
    fn('p110/lasers/b/init', ['function bm:p70/ctx', f'execute store result score #i bm.rng run random value 0..{len(LPAT) - 1}'] +
       [f'execute if score #i bm.rng matches {i} run scoreboard players set @s bm.gvc {p}' for i, p in enumerate(LPAT)] +
       [sign(rel(2, 7, 12), 'THE LOW AND THE HIGH', 'The beams never go out. Red ones sweep the floor: jump them. Violet ones hang at head height: sneak beneath them.', 0.6)])
    def line(x, y, col):
        return [f'particle minecraft:dust{{color:{col},scale:0.8}} {relf(x + 0.5, y, z / 10)} 0 0 0 0 1' for z in range(62, 189, 9)]
    for i, x in enumerate(LZ):
        fn(f'p110/lasers/b/draw{i}', ['execute if score #hb{0} bm.rng matches 0 run function bm:p110/lasers/b/low{0}'.format(i),
                                      'execute if score #hb{0} bm.rng matches 1 run function bm:p110/lasers/b/high{0}'.format(i)])
        fn(f'p110/lasers/b/low{i}', line(x, 4.25, '[1.0,0.15,0.1]'))
        fn(f'p110/lasers/b/high{i}', line(x, 5.75, '[0.7,0.2,1.0]') + line(x, 6.3, '[0.7,0.2,1.0]'))
        fn(f'p110/lasers/b/beam{i}', ['execute store result score #fy bm.rng run data get entity @s Pos[1] 100', 'scoreboard players operation #fy bm.rng -= #my bm.rng',
                                      f'execute if score #hb{i} bm.rng matches 0 if score #fy bm.rng matches ..39 run return run function bm:p70/r/lasers/zap',
                                      f'execute if score #hb{i} bm.rng matches 1 unless predicate bm:p20/sneaking run return run function bm:p70/r/lasers/zap',
                                      f'execute if score #hb{i} bm.rng matches 1 if score #fy bm.rng matches 11.. run return run function bm:p70/r/lasers/zap'])
    fn('p110/lasers/b/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                              'execute store result score #my bm.rng run data get entity @s Pos[1] 100', 'scoreboard players operation #q bm.rng = @s bm.gvc'] +
       sum(([f'scoreboard players operation #hb{i} bm.rng = #q bm.rng', f'scoreboard players operation #hb{i} bm.rng %= #2 bm.rng', 'scoreboard players operation #q bm.rng /= #2 bm.rng']
            for i in range(5)), []) +
       ['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #4 bm.rng'] +
       [f'execute if score #q bm.rng matches 0 run function bm:p110/lasers/b/draw{i}' for i in range(5)] +
       [next(l for l in G.FUNCS['p70/r/lasers/tick'] if 'p110/nofly/lasers' in l)] +
       [f'execute positioned {relf(x, 4, 6)} as @a[tag=bm.gvp,dx=0,dy=2,dz=12,tag=!bm.gvzap] at @s run function bm:p110/lasers/b/beam{i}' for i, x in enumerate(LZ)] +
       [f'execute positioned {rel(22, 4, 12)} if entity @a[tag=bm.gvp,distance=..1.2] positioned as @s run function bm:p70/solved'])
    # ---- C: the mirror gauntlet
    MP = PD.mirror_puzzles(4, 8, 6911) + PD.mirror_puzzles(5, 8, 6912) + PD.mirror_puzzles(6, 8, 6913)
    SX = lambda c: LZ[c] + 0.5
    SZ = lambda r: 8 + 4 * r + 0.5
    BY = 5.15                                        # (the beam's height: chest high)
    def mirror_tf(m, sx=1.3, sy=1.4, sz=0.08):
        th = math.radians(45 if m == 1 else -45)
        cx, cy, cz = sx / 2, sy / 2, sz / 2
        lx, lz = cx * math.cos(th) + cz * math.sin(th), -cx * math.sin(th) + cz * math.cos(th)
        q = [F(0), F(round(math.sin(th / 2), 5)), F(0), F(round(math.cos(th / 2), 5))]
        return {'left_rotation': q, 'right_rotation': IDENT, 'translation': [F(round(-lx, 4)), F(0), F(round(-lz, 4))], 'scale': [F(sx), F(sy), F(sz)]}
    def exit_pt(e):
        side, n = e[0], int(e[1:])
        return {'S': (SX(n), 19.0), 'N': (SX(n), 6.0), 'E': (24.0, SZ(n)), 'W': (1.0, SZ(n))}[side]
    def seg(a, b, step=0.5):
        (x0, z0), (x1, z1) = a, b
        n = max(1, int(math.hypot(x1 - x0, z1 - z0) / step))
        return [f'particle minecraft:dust{{color:[1.0,0.12,0.12],scale:0.9}} {relf(x0 + (x1 - x0) * i / n, BY, z0 + (z1 - z0) * i / n)} 0 0 0 0 1 force' for i in range(n + 1)]
    RECV = PD.RECEIVERS
    fn('p110/lasers/c/trace', ['scoreboard players set #hit bm.rng 0'] + seg((SX(0), 6.0), (SX(0), SZ(0))) +
       ['function bm:p110/lasers/c/cell_0_0_s', 'execute if score #hit bm.rng matches 1 run function bm:p110/lasers/c/lit'])
    for c in range(PD.NC):
        for r in range(PD.NR):
            for d in 'NSEW':
                pc, pr = c - PD.DIRS[d][0], r - PD.DIRS[d][1]          # (only the ways a beam can come in: from a cell, or the emitter)
                if not (0 <= pc < PD.NC and 0 <= pr < PD.NR) and (c, r, d) != (0, 0, 'S'): continue
                fn(f'p110/lasers/c/cell_{c}_{r}_{d.lower()}', [f'execute store result score #m bm.rng run scoreboard players get @e[type=minecraft:marker,tag=bm.gvsk{c}{r},distance=..16,limit=1] bm.gvy1'] +
                   [f'execute if score #m bm.rng matches {m} run return run function bm:p110/lasers/c/seg_{c}_{r}_{(d if m == 0 else PD.REFLECT[m][d]).lower()}' for m in range(3)])
            for d, (dc, dr) in PD.DIRS.items():
                c2, r2 = c + dc, r + dr
                if 0 <= c2 < PD.NC and 0 <= r2 < PD.NR:
                    fn(f'p110/lasers/c/seg_{c}_{r}_{d.lower()}', seg((SX(c), SZ(r)), (SX(c2), SZ(r2)))[1:] + [f'function bm:p110/lasers/c/cell_{c2}_{r2}_{d.lower()}'])
                else:
                    e = PD.exit_of(c, r, d)
                    fn(f'p110/lasers/c/seg_{c}_{r}_{d.lower()}', seg((SX(c), SZ(r)), exit_pt(e))[1:] +
                       ([f'execute if score @s bm.gvy2 matches {RECV.index(e)} run scoreboard players set #hit bm.rng 1'] if e in RECV else []) +
                       [f'particle minecraft:flash{{color:[1.0,0.3,0.2,1.0]}} {relf(exit_pt(e)[0], BY, exit_pt(e)[1])} 0 0 0 0 1'])
    mdisp = lambda m, rot: snbt({'Tags': ['bm.gvprop', 'bm.gvmird'] if rot else ['bm.gvprop'], 'block_state': 'minecraft:light_blue_stained_glass' if rot else 'minecraft:iron_block',
                                 'brightness': {'block': 14, 'sky': 14}, 'transformation': mirror_tf(m), 'interpolation_duration': Int(4)})
    for j, pz in enumerate(MP):
        L = [f'scoreboard players set @s bm.gvy2 {RECV.index(pz["recv"])}']
        grid = dict(pz['fixed']); grid.update({x: 1 + ((pz['start'] >> i) & 1) for i, x in enumerate(pz['rot'])})
        for (c, r), m in grid.items():
            L.append(f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvsk{c}{r},distance=..16,limit=1] bm.gvy1 {m}')
            L.append(f'summon minecraft:block_display {relf(SX(c), 4.0, SZ(r))} {mdisp(m, (c, r) in pz["rot"])}')
        for (c, r) in pz['rot']:
            L.append(f'summon minecraft:interaction {relf(SX(c), 4.0, SZ(r))} {{Tags:["bm.gvprop","bm.gvmirc"],width:1.4f,height:1.7f,response:1b}}')
        side, n = pz['recv'][0], int(pz['recv'][1:])
        tx, tz = {'S': (SX(n), 18.75), 'N': (SX(n), 6.25), 'E': (23.75, SZ(n))}[side]
        L.append(f'summon minecraft:item_display {relf(tx, BY, tz)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvmtgt'], 'item': {'id': 'minecraft:target', 'count': Int(1)},
                                                                             'item_display': 'fixed', 'Glowing': B(1), 'glow_color_override': Int(0xffd040),
                                                                             'transformation': {'left_rotation': IDENT, 'right_rotation': IDENT, 'translation': [F(0)] * 3, 'scale': [F(0.55)] * 3}}))
        fn(f'p110/lasers/c/p{j}', L)
    # (the puzzles by tier: four turnable mirrors on Tiers I-II, five on III, six on IV-V)
    fn('p110/lasers/c/init', ['function bm:p70/ctx', f'setblock {rel(22, 4, 12)} minecraft:air'] +
       [f'summon minecraft:marker {relf(SX(c), 4.0, SZ(r))} {{Tags:["bm.gvprop","bm.gvsk","bm.gvsk{c}{r}"]}}' for c in range(PD.NC) for r in range(PD.NR)] +
       [f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvsk,distance=..16] bm.gvy1 0',
        'execute store result score #i bm.rng run random value 0..7', 'execute if score #gt bm.rng matches 3 run scoreboard players add #i bm.rng 8',
        'execute if score #gt bm.rng matches 4.. run scoreboard players add #i bm.rng 16'] +
       [f'execute if score #i bm.rng matches {j} run function bm:p110/lasers/c/p{j}' for j in range(len(MP))] +
       [sign(rel(2, 7, 12), 'THE MIRROR GAUNTLET', 'Turn the glass mirrors (right-click them) until the beam strikes the gold target. The steel ones don\'t turn.', 0.6)])
    fn('p110/lasers/c/tick', ['execute if score @s bm.gvs matches 3 run return 0', 'execute if score @s bm.gvs matches 0 run scoreboard players set @s bm.gvs 1',
                              'scoreboard players set #flip bm.rng 0',
                              'execute as @e[type=minecraft:interaction,tag=bm.gvmirc,distance=..16] if data entity @s interaction at @s run function bm:p110/lasers/c/click',
                              'execute as @e[type=minecraft:interaction,tag=bm.gvmirc,distance=..16] if data entity @s attack at @s run function bm:p110/lasers/c/click',
                              'execute if score #flip bm.rng matches 1 run return run function bm:p110/lasers/c/trace',
                              'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #4 bm.rng',
                              'execute if score #q bm.rng matches 0 run function bm:p110/lasers/c/trace'])
    fn('p110/lasers/c/click', ['data remove entity @s interaction', 'data remove entity @s attack', 'scoreboard players set #flip bm.rng 1',
                               'execute as @e[type=minecraft:marker,tag=bm.gvsk,distance=..0.6,limit=1] at @s run function bm:p110/lasers/c/flip',
                               'playsound minecraft:block.glass.hit block @a[distance=..16] ~ ~1 ~ 1 1.3'])
    fn('p110/lasers/c/flip', ['execute if score @s bm.gvy1 matches 1 run return run function bm:p110/lasers/c/to2', 'function bm:p110/lasers/c/to1'])
    for m in (1, 2):
        fn(f'p110/lasers/c/to{m}', [f'scoreboard players set @s bm.gvy1 {m}',
                                    'execute at @s as @e[type=minecraft:block_display,tag=bm.gvmird,distance=..0.6,limit=1] run data merge entity @s ' +
                                    snbt({'transformation': mirror_tf(m), 'start_interpolation': Int(0), 'interpolation_duration': Int(4)})])
    fn('p110/lasers/c/lit', ['execute as @e[type=minecraft:interaction,tag=bm.gvmirc,distance=..16] run kill @s',
                             'execute at @e[type=minecraft:item_display,tag=bm.gvmtgt,distance=..16] run particle minecraft:wax_on ~ ~ ~ 0.3 0.3 0.3 0 30',
                             'playsound minecraft:block.beacon.activate block @a[distance=..30] ~ ~ ~ 1 1.4', 'function bm:p70/solved'])
    dispatch(G, 'lasers', ('p110/lasers/b/init', 'p110/lasers/b/tick'), ('p110/lasers/c/init', 'p110/lasers/c/tick'))

    # ================================================================== THE TILE FLOOR
    tc = lambda c, r: (4 + 3 * c, 6 + 3 * r)              # (a tile's middle block)
    base_tick = [l for l in G.FUNCS['p70/r/tiles/tick'] if 'peek' not in l and 'bm.gvpk' not in l and 'gvlatch' not in l]
    fn('p110/tiles/tick', base_tick)
    markers = [f'summon minecraft:marker {rel(tc(c, r)[0], 4, tc(c, r)[1])} {{Tags:["bm.gvtile","bm.gvt{c}{r}","bm.gvprop"]}}' for c in range(6) for r in range(5)] + \
              ['execute as @e[type=minecraft:marker,tag=bm.gvtile,distance=..14] run scoreboard players set @s bm.gvsafe 0']
    safe = lambda c, r: f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvt{c}{r},distance=..14,limit=1] bm.gvsafe 1'
    # ---- B: the colour trail
    CP = PD.colour_puzzles()
    CC = {'red': '#ff5050', 'blue': '#5a8aff', 'lime': '#7dff6a', 'yellow': '#ffe050'}
    fn('p110/tiles/b/init', ['function bm:p70/ctx', f'setblock {rel(1, 5, 9)} minecraft:air'] + markers + choose('#i', len(CP), 'p110/tiles/b/p'))
    for j, pz in enumerate(CP):
        L = []
        for (c, r), ci in pz['col'].items():
            x, z = tc(c, r); col = PD.COLS[ci]
            L += [f'scoreboard players set @e[type=minecraft:marker,tag=bm.gvt{c}{r},distance=..14,limit=1] bm.gvy1 {ci}',
                  f'fill {rel(x, 3, z - 1)} {rel(x, 3, z + 1)} minecraft:{col}_concrete', f'fill {rel(x - 1, 3, z)} {rel(x + 1, 3, z)} minecraft:{col}_concrete']
        L += [safe(c, r) for c, r in pz['path']]
        names = [PD.COLS[i] for i in pz['cyc']]
        body = [T('Step on the colours in this order, over and over:\n', 'gray')]
        for i, nm in enumerate(names + [names[0]]):
            body += [T(nm.upper(), CC[nm], bold=True), T(' > ' if i < 4 else '...\n', 'gray')]
        body += [T(f'Start on a {names[0].upper()} tile by the door; step ahead or to the side. Only one trail reaches the far side.', 'gray')]
        L.append(label(rel(1, 7, 12), [T('THE COLOUR TRAIL\n', GOLD, bold=True)] + body, 0.6, 'vertical'))
        fn(f'p110/tiles/b/p{j}', L)
    # ---- C: the counted floor
    NP = PD.count_puzzles()
    fn('p110/tiles/c/init', ['function bm:p70/ctx', f'setblock {rel(1, 5, 9)} minecraft:air'] + markers + choose('#i', len(NP), 'p110/tiles/c/p') +
       [sign(rel(1, 7.6, 12), 'THE COUNTED FLOOR', 'One path of safe tiles crosses the floor; it never turns back toward the door. The numbers say how many '
             'safe tiles lie in each row and each column. Glowing tiles are safe.', 0.55)])
    for j, pz in enumerate(NP):
        L = [safe(c, r) for c, r in pz['path']]
        L += [label(relf(2.6, 4.7, tc(0, r)[1] + 0.5), T(str(n), GOLD, bold=True), 1.0) for r, n in enumerate(pz['rows'])]
        L += [label(relf(tc(c, 0)[0] + 0.5, 4.7, 4.4), T(str(n), GOLD, bold=True), 1.0) for c, n in enumerate(pz['cols'])]
        L += [f'setblock {rel(tc(c, r)[0], 3, tc(c, r)[1])} minecraft:sea_lantern' for c, r in pz['shown']]
        fn(f'p110/tiles/c/p{j}', L)
    dispatch(G, 'tiles', ('p110/tiles/b/init', 'p110/tiles/tick'), ('p110/tiles/c/init', 'p110/tiles/tick'))
