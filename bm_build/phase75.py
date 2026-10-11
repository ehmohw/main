"""2.65: THE GILDED GUTTER VAULT, REBUILT - a dungeon-raiding minigame (phase70 is the original heist; this reworks it).

GETTING IN: the Heist Plans (the Fence). Pick a tier, then your TRIES (3, 5 or 7 - how many knock-outs your crew can take;
  each crewmate past the first adds one). The Fixer's fee is 3 Black Market Tokens a head; every fee goes into the
  LUCKY POOL. One heist in twenty (one in seven on a Lucky Night) is a LUCKY RAID: win it and the crew splits the pool.
DYING: you wake in the den (your spawn is set there for the heist - your own bed or spawn comes back the moment you
  leave). Every knock-out costs the crew a try. Out of tries: THE HEIST FAILS - everyone is pulled back to the den,
  everything gathered is lost, and the Fixer draws up a fresh plan to try again. The emerald plate in the den takes you
  back to the crew (the last door you opened).
THE POT: guards drop nothing - they pay into the crew's pot (watch the bar), and so do secrets, trophies already
  earned and rarer foes. The pot and every find are packed into The Haul at the end - only if you win.
THE HAUL: tier + 2 shares, +1 per modifier, +1 for a clean getaway, the contract, and now: +4 for picking 3 tries,
  +2 for 5; +2 for no knock-outs at all, +1 for just one.
ONCE ONLY: the Gutter Laurel, each puzzle trophy and the Bond Sigil are given once (after that: coins in the pot).
THE BOND SIGIL works with your party: near a party member carrying one, you both regenerate.
THE DEN only rests you (regeneration and a full belly) before the heist starts and after it's won.
THE WAY THROUGH is no longer a straight line: passages climb and drop, bend left and right, a ladder shaft, a plunge
  into a pool, a chasm with stepping stones. Every tier is built in its own stone (phase75_rooms)."""
import os
from items import T, ITEMS
from nbt import snbt, B, F, D, Int
import phase70 as P70
import phase70_rooms as RM
import phase75_rooms as R5

GOLD = '#ffcf40'
LUCKY = '#7dff6a'
SLOTS, ZS, Y0 = P70.SLOTS, P70.ZS, P70.Y0
DEN = (3.5, Y0 + 4, 12.5)                     # (z: + the slot's offset)
FEE = 3
POOL_SEED = 30
LIVES = {1: 3, 2: 5, 3: 7}
BONUS_PICK = {3: 4, 5: 2, 7: 0}               # shares for daring fewer tries
FL_X = (-16, 340)                              # forceload / cleanup bounds (x) and the lateral room bounds (z from the slot's z)
Z_LO, Z_HI = -16, 16
Y_LO, Y_HI = Y0 - 10, Y0 + 15
# every room kind the layout can draw, with its template size (cleanup) - more join in phase76
KINDS = list(RM.KINDS)
SIZE = {k: (25, 16, 25) for k in KINDS}
TIER_POOL = {1: ['levers', 'plates', 'tiles', 'guards', 'coffers'],
             2: ['levers', 'dial', 'lasers', 'coffers', 'guards', 'plates'],
             3: ['lasers', 'tiles', 'coffers', 'dial', 'plates', 'guards', 'levers'],
             4: ['lasers', 'dial', 'coffers', 'tiles', 'guards', 'levers', 'plates'],
             5: ['lasers', 'dial', 'coffers', 'tiles', 'guards', 'levers', 'plates']}
EVENT_POOL = {t: [] for t in range(1, 6)}      # (event rooms: phase76)
EXTRA_ROOMS = {}                               # name -> builder (phase76 adds its rooms here before generate)


def zoff(s):
    return s * ZS


def generate(G):
    fn, wjson, title, tellraw, give, PREFIX = G.fn, G.wjson, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[Heist] ', GOLD, bold=True)]
    rel = RM.rel
    tick, fast, second = [], [], []
    objs = ['bm.gvlv', 'bm.gvlc', 'bm.gvpot', 'bm.gvlu', 'bm.gvlp', 'bm.gvpt', 'bm.gvq', 'bm.gvlaur', 'bm.gvtro', 'bm.gvbs', 'bm.gvfail', 'bm.gvdc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'execute unless score #lpool bm.gvlp matches 1.. run scoreboard players set #lpool bm.gvlp {POOL_SEED}',
         'execute in minecraft:overworld summon minecraft:marker run function bm:p75/wsp']
    G.OBJECTIVES += objs
    ident = [F(0), F(0), F(0), F(1)]
    def label(x, y, z, text, scale=0.55, tags=('bm.gvprop',), bill='center'):
        return f'summon minecraft:text_display {rel(x, y, z)} ' + snbt({'Tags': list(tags), 'billboard': bill, 'brightness': {'block': 15, 'sky': 15},
                                                                       'background': Int(0x90000000 - 2 ** 32), 'text': text, 'alignment': 'center',
                                                                       'transformation': {'left_rotation': ident, 'right_rotation': ident,
                                                                                          'translation': [F(0)] * 3, 'scale': [F(scale)] * 3}})
    def vbutton(x, y, z, facing, text):
        return [f'setblock {rel(x, y, z)} minecraft:pale_oak_button[face=wall,facing={facing},powered=false]', label(x, y + 0.7, z, T(text, GOLD, bold=True))]
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'

    # ================================================================== THE ROOMS, TIER BY TIER (themed templates; the old untiered ones go)
    rooms = R5.tiered_rooms(EXTRA_ROOMS)
    for nm in list(RM.BUILDERS):
        pth = G.path('data', 'bm', 'structure', f'gv_{nm}.nbt')
        if os.path.exists(pth): os.remove(pth)
        G.FUNCS.pop(f'p70/place/{nm}', None)
    for nm, b in rooms.items():
        b().export(G.path('data', 'bm', 'structure', f'gv_{nm}.nbt'))
    # (at the piece's origin, #gt the tier, #gi the instance) place a piece, themed, and leave a cleanup marker of its size
    def size_tag(sz):
        return 'bm.gvpc_' + 'x'.join(str(v) for v in sz)
    SIZES = set()
    def piece_fn(key, size):
        SIZES.add(size)
        fn(f'p75/pc/{key}', [f'execute if score #gt bm.rng matches {t} run place template bm:gv_{key}_t{t} ~ ~ ~' for t in R5.TIERS] +
           [f'summon minecraft:marker ~ ~ ~ {{Tags:["bm.gvpc","{size_tag(size)}","bm.gvpcn"]}}',
            'scoreboard players operation @e[type=minecraft:marker,tag=bm.gvpcn,distance=..1] bm.gvi = #gi bm.rng',
            'tag @e[type=minecraft:marker,tag=bm.gvpcn,distance=..1] remove bm.gvpcn'])
    for k in KINDS + list(EXTRA_ROOMS) + ['lobby', 'cache']:
        piece_fn(k, SIZE.get(k, (25, 16, 25)))
    piece_fn('vault', (RM.VAULT_LEN, 16, 25))
    for k, (_b, size, *_r) in R5.CONN.items():
        piece_fn(f'cn_{k}', size)

    # ================================================================== THE LAYOUT: a cursor walks east; passages bend it up, down, left, right
    # (as the cursor marker: #gk rooms to lay, #gt tier, #z0 the slot's z)
    fn('p75/lay/rooms', ['scoreboard players operation #lk bm.rng = #gk bm.rng', 'scoreboard players set #q bm.rng 0', 'scoreboard players set #nev bm.rng 0',
                         'function bm:p75/lay/loop',
                         'execute at @s run function bm:p75/lay/cn', 'execute at @s run function bm:p75/pc/vault',
                         'execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim'])
    fn('p75/lay/loop', ['execute if score #lk bm.rng matches ..0 run return 0', 'execute at @s run function bm:p75/lay/cn',
                        'execute at @s run function bm:p75/lay/room', 'scoreboard players remove #lk bm.rng 1', 'function bm:p75/lay/loop'])
    conn = list(R5.CONN.items())
    weights = []
    for k, (_b, _s, _e, _x, w) in conn: weights += [k] * w
    ok = {'up': f'execute if score #cy bm.rng matches {Y_HI - 5 + 1}.. run return run function bm:p75/lay/cn_pick',
          'dn': f'execute if score #cy bm.rng matches ..{Y_LO + 5 - 1} run return run function bm:p75/lay/cn_pick',
          'sh': f'execute if score #cy bm.rng matches {Y_HI - 10 + 1}.. run return run function bm:p75/lay/cn_pick',
          'dp': f'execute if score #cy bm.rng matches ..{Y_LO + 9 - 1} run return run function bm:p75/lay/cn_pick',
          'lf': f'execute if score #cz bm.rng matches ..{Z_LO + 8 - 1} run return run function bm:p75/lay/cn_pick',
          'rt': f'execute if score #cz bm.rng matches {Z_HI - 8 + 1}.. run return run function bm:p75/lay/cn_pick'}
    fn('p75/lay/cn', ['execute store result score #cy bm.rng run data get entity @s Pos[1]', 'execute store result score #cz bm.rng run data get entity @s Pos[2]',
                      'scoreboard players operation #cz bm.rng -= #z0 bm.rng', 'function bm:p75/lay/cn_pick'])
    fn('p75/lay/cn_pick', [f'execute store result score #cn bm.rng run random value 0..{len(weights) - 1}'] +
       [f'execute if score #cn bm.rng matches {i} run return run function bm:p75/cn/{k}' for i, k in enumerate(weights)])
    for k in R5.CONN:
        (ox, oy, oz), (nx, ny, nz) = R5.conn_move(k)
        f = lambda v: '~' if v == 0 else f'~{v}'
        fn(f'p75/cn/{k}', ([ok[k]] if k in ok else []) +
           [f'execute positioned {f(ox)} {f(oy)} {f(oz)} run function bm:p75/pc/cn_{k}', f'tp @s {f(nx)} {f(ny)} {f(nz)}'])
    # rooms: from the tier's pool, none twice; now and then an event room instead (at most two a run)
    fn('p75/lay/room', ['scoreboard players add #q bm.rng 1', 'scoreboard players set #ev bm.rng 0',
                        'execute store result score #ev bm.rng run random value 1..100',
                        'execute if score #ev bm.rng matches 1..22 if function bm:p75/lay/can_event run return run function bm:p75/lay/event',
                        'function bm:p75/lay/pick'] +
       [f'execute if score #r bm.rng matches {j} run function bm:p75/pc/{k}' for j, k in enumerate(KINDS)] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim'])
    fn('p75/lay/can_event', [f'execute if score #gt bm.rng matches {t} if score #nev bm.rng matches ..{min(2, len(EVENT_POOL[t])) - 1} run return 1'
                             for t in range(1, 6) if EVENT_POOL[t]] + ['return 0'])
    fn('p75/lay/pick', [f'execute if score #gt bm.rng matches {t} run function bm:p75/lay/pick{t}' for t in range(1, 6)])
    for t in range(1, 6):
        pool = [KINDS.index(k) for k in TIER_POOL[t]]
        fn(f'p75/lay/pick{t}', [f'execute store result score #i bm.rng run random value 0..{len(pool) - 1}'] +
           [f'execute if score #i bm.rng matches {i} run scoreboard players set #r bm.rng {j}' for i, j in enumerate(pool)] +
           ['function bm:p75/lay/bit', 'execute if score #q2 bm.rng matches 1 run return run function bm:p75/lay/pick' + str(t),
            'scoreboard players operation #pool bm.rng += #bit bm.rng'])
    fn('p75/lay/bit', ['scoreboard players set #bit bm.rng 1', 'scoreboard players operation #k bm.rng = #r bm.rng', 'function bm:p75/lay/bit2',
                       'scoreboard players operation #q2 bm.rng = #pool bm.rng', 'scoreboard players operation #q2 bm.rng /= #bit bm.rng',
                       'scoreboard players operation #q2 bm.rng %= #2 bm.rng'])
    fn('p75/lay/bit2', ['execute if score #k bm.rng matches ..0 run return 0', 'scoreboard players operation #bit bm.rng *= #2 bm.rng',
                        'scoreboard players remove #k bm.rng 1', 'function bm:p75/lay/bit2'])
    fn('p75/lay/event', ['scoreboard players add #nev bm.rng 1'] +
       [f'execute if score #gt bm.rng matches {t} run function bm:p75/lay/event{t}' for t in range(1, 6)] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim'])
    for t in range(1, 6):
        evs = EVENT_POOL[t]
        if not evs:
            fn(f'p75/lay/event{t}', ['function bm:p75/lay/pick'] + [f'execute if score #r bm.rng matches {j} run function bm:p75/pc/{k}' for j, k in enumerate(KINDS)])
            continue
        # (an event kind not yet used this run: events are bits past the room kinds)
        fn(f'p75/lay/event{t}', [f'execute store result score #i bm.rng run random value 0..{len(evs) - 1}'] +
           [f'execute if score #i bm.rng matches {i} run scoreboard players set #r bm.rng {len(KINDS) + list(EXTRA_ROOMS).index(k)}' for i, k in enumerate(evs)] +
           ['function bm:p75/lay/bit', f'execute if score #q2 bm.rng matches 1 run return run function bm:p75/lay/event{t}', 'scoreboard players operation #pool bm.rng += #bit bm.rng'] +
           [f'execute if score #i bm.rng matches {i} run function bm:p75/pc/{k}' for i, k in enumerate(evs)])
    # (a fresh room marker: claimed for the instance, numbered along the way)
    fn('p75/claim', ['function bm:p70/claim_room', 'scoreboard players operation @s bm.gvq = #q bm.rng'])

    # ================================================================== BUILDING A HEIST (replaces phase70's straight row of rooms)
    for s in range(SLOTS):
        z0 = zoff(s)
        build = [f'scoreboard players operation #gt bm.rng = #t{s} bm.gvt', f'scoreboard players set #gs bm.rng {s}', f'scoreboard players set #gi bm.rng {s + 1}',
                 f'scoreboard players operation #grun bm.rng = #r{s} bm.gvrun', f'scoreboard players set #z0 bm.rng {z0}',
                 'scoreboard players set #gn bm.rng 0', 'execute if score #active bm.bm matches 1 run scoreboard players set #gn bm.rng 1',
                 'execute if score #gn bm.rng matches 0 if score #lnight bm.bm matches 1 run scoreboard players set #gn bm.rng 2',
                 'execute if score #gn bm.rng matches 0 if score #inv bm.bm matches 1 run scoreboard players set #gn bm.rng 3',
                 'function bm:p70/roll_mods',
                 'scoreboard players operation #gk bm.rng = #gt bm.rng', 'scoreboard players add #gk bm.rng 2', 'scoreboard players set #pool bm.rng 0',
                 f'execute in bm:gutter positioned 0 {Y0} {z0} run function bm:p75/pc/lobby',
                 f'execute in bm:gutter positioned 0 {Y0} {z0 - 25} run function bm:p75/pc/cache',
                 'scoreboard players set #q bm.rng 0', 'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvnew] run function bm:p75/claim',
                 f'execute in bm:gutter run summon minecraft:marker 0 {Y0} {z0} {{Tags:["bm.gvcur"]}}',
                 'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvcur,limit=1] run function bm:p75/lay/rooms',
                 'execute in bm:gutter run kill @e[type=minecraft:marker,tag=bm.gvcur]',
                 # the checkpoint (the den, until a door opens)
                 f'execute in bm:gutter run summon minecraft:marker {DEN[0]} {DEN[1]} {z0 + DEN[2]} {{Tags:["bm.gvcp","bm.gvpcn"],Rotation:[-90f,0f]}}',
                 f'execute in bm:gutter run scoreboard players set @e[type=minecraft:marker,tag=bm.gvpcn] bm.gvi {s + 1}',
                 'execute in bm:gutter run tag @e[type=minecraft:marker,tag=bm.gvpcn] remove bm.gvpcn',
                 # everyone in
                 f'execute as @a[tag=bm.gvwait,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/s{s}/enter',
                 f'execute store result score #np{s} bm.gvx if entity @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]',
                 f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr_lobby,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/inst_init',
                 f'scoreboard players operation #gpl bm.rng = #np{s} bm.gvx',
                 f'execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,scores={{bm.gvi={s + 1}}}] at @s run function bm:p70/r/init']
        G.FUNCS[f'p70/s{s}/build'] = build
        # claim: the wider forceload; the tries and the Lucky roll belong to the slot (they outlive a failed attempt's rebuild)
        cl = G.FUNCS[f'p70/s{s}/claim']
        k = next(i for i, l in enumerate(cl) if 'forceload add' in l)
        cl[k] = f'execute in bm:gutter run forceload add {FL_X[0]} {z0 - 32} {FL_X[1]} {z0 + 48}'
        cl[k:k] = [f'scoreboard players operation #lc{s} bm.gvlc = #lv bm.rng', f'scoreboard players set #lu{s} bm.gvlu 0',
                   'execute store result score #r bm.rng run random value 1..100',
                   f'execute if score #r bm.rng matches ..5 run scoreboard players set #lu{s} bm.gvlu 1',
                   f'execute if score #lnight bm.bm matches 1 if score #r bm.rng matches ..15 run scoreboard players set #lu{s} bm.gvlu 1']
        # cleanup: every piece by its marker, then the entities
        G.FUNCS[f'p70/s{s}/clean'] = [f'scoreboard players set #gi bm.rng {s + 1}', 'execute in bm:gutter run function bm:p75/clean_pieces',
                                      f'execute in bm:gutter positioned {FL_X[0] - 4} 30 {z0 - 40} run kill @e[type=!minecraft:player,dx={FL_X[1] - FL_X[0] + 8},dy=90,dz=100]',
                                      f'execute in bm:gutter run forceload remove {FL_X[0]} {z0 - 32} {FL_X[1]} {z0 + 48}',
                                      f'scoreboard players set #s{s} bm.gvon 0', f'scoreboard players set #e{s} bm.gve 0', f'scoreboard players set #fl{s} bm.gvfail 0',
                                      f'bossbar set bm:gva{s} players', f'bossbar set bm:gvb{s} players']
        # dying in it: your spawn is the den while the heist lasts
        for f_ in (f'p70/s{s}/enter', f'p70/s{s}/join'):
            G.FUNCS[f_] += ['function bm:p75/sp_save', f'execute in bm:gutter run spawnpoint @s {int(DEN[0])} {DEN[1]} {z0 + int(DEN[2])} -90 0']
        G.FUNCS[f'p70/s{s}/recruit'].insert(0, 'execute unless function bm:p75/fee run return 0')
        cl[:] = [l.replace(f'tag=!bm.gvwait] if score @s bm.pty = #asker bm.pty run function bm:p70/s{s}/recruit', f'tag=!bm.gvwait] at @s if score @s bm.pty = #asker bm.pty run function bm:p70/s{s}/recruit') for l in cl]
        # a failed attempt: the den, a fresh plan (same crew, same tries, same luck), nothing kept
        second.append(f'execute if score #fl{s} bm.gvfail matches 1.. run function bm:p75/s{s}/fail_tick')
        fn(f'p75/s{s}/fail_tick', [f'scoreboard players remove #fl{s} bm.gvfail 1', f'execute if score #fl{s} bm.gvfail matches 0 run function bm:p75/s{s}/reset'])
        fn(f'p75/s{s}/reset', [f'scoreboard players set #gi bm.rng {s + 1}',
                               f'execute as @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}] in bm:gutter run tp @s {DEN[0]} {DEN[1]} {z0 + DEN[2]} -90 0',
                               'execute in bm:gutter run function bm:p75/clean_pieces',
                               f'execute in bm:gutter positioned {FL_X[0] - 4} 30 {z0 - 40} run kill @e[type=!minecraft:player,dx={FL_X[1] - FL_X[0] + 8},dy=90,dz=100]',
                               'scoreboard players add #runs bm.gvrun 1', f'scoreboard players operation #r{s} bm.gvrun = #runs bm.gvrun',
                               f'scoreboard players operation @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}] bm.gvrun = #r{s} bm.gvrun',
                               f'bossbar set bm:gvb{s} players', f'function bm:p70/s{s}/build',
                               f'execute as @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}] run function bm:p75/after_fail'])
    fn('p75/after_fail', ['function bm:p70/glass_check', 'effect clear @s', 'effect give @s minecraft:instant_health 1 4 true',
                          tellraw('@s', P + [T('The Fixer spreads out a fresh plan. ', GOLD), T('Same crew, same tries - press ', 'gray'), T('BEGIN', GOLD, bold=True),
                                             T(' when you\'re ready.', 'gray')])])
    fn('p75/clean_pieces', [f'execute as @e[type=minecraft:marker,tag={size_tag(sz)}] if score @s bm.gvi = #gi bm.rng at @s run fill ~ ~ ~ ~{sz[0] - 1} ~{sz[1] - 1} ~{sz[2] - 1} minecraft:air strict'
                            for sz in sorted(SIZES)] +
       ['execute as @e[type=minecraft:marker,tag=bm.gvpc] if score @s bm.gvi = #gi bm.rng run kill @s'])

    # ================================================================== RESPAWNING IN THE DEN (and your own spawn back afterwards)
    fn('p75/wsp', ['data modify storage bm:gv wsp set value {dimension:"minecraft:overworld",yaw:0}',
                   'execute store result storage bm:gv wsp.x int 1 run data get entity @s Pos[0]', 'execute store result storage bm:gv wsp.y int 1 run data get entity @s Pos[1]',
                   'execute store result storage bm:gv wsp.z int 1 run data get entity @s Pos[2]', 'kill @s'])
    fn('p75/sp_save', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p75/sp_save2 with storage bm:gv tmp', 'tag @s add bm.gvsp'])
    fn('p75/sp_save2', ['$execute if data storage bm:gv sp.p$(pid) run return 0',                 # (already saved: a rejoin keeps the original)
                        '$data modify storage bm:gv sp.p$(pid) set value {none:1b}',
                        'data modify storage bm:gv spt set value "-"', 'data modify storage bm:gv spt set from entity @s respawn.dimension',
                        'execute store success score #ok bm.rng run data modify storage bm:gv spt set value "bm:gutter"',
                        '$execute if score #ok bm.rng matches 1 if data entity @s respawn run data modify storage bm:gv sp.p$(pid) set from entity @s respawn'])
    fn('p75/sp_restore', ['tag @s remove bm.gvsp', 'execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid',
                          'function bm:p75/sp_restore2 with storage bm:gv tmp'])
    fn('p75/sp_restore2', ['$execute unless data storage bm:gv sp.p$(pid) run return 0', '$data modify storage bm:gv spr set from storage bm:gv sp.p$(pid)',
                           '$data remove storage bm:gv sp.p$(pid)',
                           'execute if data storage bm:gv spr.none if data storage bm:gv wsp.x run return run function bm:p75/sp_set with storage bm:gv wsp',
                           'execute if data storage bm:gv spr.none run return 0',
                           'execute store result storage bm:gv spr.x int 1 run data get storage bm:gv spr.pos[0]', 'execute store result storage bm:gv spr.y int 1 run data get storage bm:gv spr.pos[1]',
                           'execute store result storage bm:gv spr.z int 1 run data get storage bm:gv spr.pos[2]',
                           'execute store result storage bm:gv spr.yaw int 1 run data get storage bm:gv spr.yaw',
                           'function bm:p75/sp_set with storage bm:gv spr'])
    fn('p75/sp_set', ['$execute in $(dimension) run spawnpoint @s $(x) $(y) $(z) $(yaw) 0'])
    G.FUNCS['p70/unraid'].insert(0, 'function bm:p75/sp_restore')
    second.append('execute as @a[tag=bm.gvsp,tag=!bm.gvp,tag=!bm.gvwait,tag=!bm.gvdead] unless dimension bm:gutter run function bm:p75/sp_restore')

    # ================================================================== THE DEN, PUT RIGHT
    lob = G.FUNCS['p70/r/lobby/init']
    k = next(i for i, l in enumerate(lob) if 'bm.gvsheet' in l)
    lob[k] = lob[k].replace(rel(12, 6, 1), rel(5.5, 6, 1), 1)
    lob += [label(21, 5.4, 5, [T('BACK TO THE CREW\n', LUCKY, bold=True), T('(the last door you opened)', 'gray')], 0.5),
            f'summon minecraft:text_display {rel(22, 6.4, 20)} ' + snbt({'Tags': ['bm.gvprop', 'bm.gvpoold'], 'billboard': 'center', 'brightness': {'block': 15, 'sky': 15},
                                                                     'background': Int(0x90000000 - 2 ** 32), 'text': '', 'alignment': 'center',
                                                                     'transformation': {'left_rotation': ident, 'right_rotation': ident, 'translation': [F(0)] * 3,
                                                                                        'scale': [F(0.55)] * 3}}),
            'function bm:p75/pool_show']
    fn('p75/pool_show', [f'execute as @e[type=minecraft:text_display,tag=bm.gvpoold,distance=..30] run data modify entity @s text set value '
                         + snbt([T('THE LUCKY POOL\n', LUCKY, bold=True), {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': 'white', 'bold': True},
                                 T(' Tokens\n', 'white'), T('Every fee drops in. Win a Lucky Raid\n(1 in 20) and the crew splits it.', 'gray')])])
    G.FUNCS['p70/r/lobby/tick'] += [f'execute positioned {rel(21, 4, 5)} as @a[tag=bm.gvp,distance=..0.8] at @s run function bm:p75/to_crew']
    fn('p75/to_crew', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                       'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                       'execute unless score #st bm.rng matches 2..3 run return run ' + say('Once the heist is on, this takes you back to your crew.', LUCKY),
                       'execute as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvcpme',
                       'tp @s @e[type=minecraft:marker,tag=bm.gvcpme,limit=1]', 'tag @e[type=minecraft:marker,tag=bm.gvcpme] remove bm.gvcpme',
                       'effect give @s minecraft:resistance 3 4 true', 'playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 0.6 1.4',
                       'particle minecraft:wax_on ~ ~1 ~ 0.3 0.6 0.3 0 20'])
    # the checkpoint moves to each door as it opens
    G.FUNCS['p70/solved'].append('execute as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #gi bm.rng run tp @s ' + rel(25, 4, 12) + ' -90 0')
    # rest only before the heist starts and after it's won
    sec = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(sec) if 'function bm:p74/den_rest' in l)
    sec[k] = sec[k].replace('tag=bm.gvr_lobby] at @s', 'tag=bm.gvr_lobby] unless score @s bm.gvst matches 2..3 unless score @s bm.gvst matches 5 at @s')

    # ================================================================== THE DIAL LOCK: a button to try the dials (no more guessing when it checks)
    dial = G.FUNCS['p70/r/dial/tick']
    k = next(i for i, l in enumerate(dial) if 'bm.gvtm matches 900' in l)
    check = dial[k + 1:]
    G.FUNCS['p70/r/dial/tick'] = dial[:k + 1] + [
        f'execute if block {rel(16, 5, 22)} minecraft:pale_oak_button[powered=true] unless entity @s[tag=bm.gvlatch] run function bm:p75/dial_try',
        f'execute unless block {rel(16, 5, 22)} minecraft:pale_oak_button[powered=true] run tag @s remove bm.gvlatch']
    rest = [l for l in check if not l.startswith('scoreboard players operation #q bm.rng = @s bm.gvtm') and '%= #5' not in l and 'unless score #q bm.rng matches 0 run return 0' not in l]
    fn('p75/dial_try', ['tag @s add bm.gvlatch', 'scoreboard players set #bad bm.rng 0', 'function bm:p75/dial_cmp',
                        'execute if score #bad bm.rng matches 0 run return run function bm:p75/dial_ok',
                        'scoreboard players set #add bm.rng 10', 'function bm:p70/oops', 'playsound minecraft:block.anvil.land block @a[distance=..24] ~ ~ ~ 0.5 0.7',
                        'execute as @a[tag=bm.gvp,distance=..20] run ' + title('@s', 'actionbar', T('The dials don\'t line up - somewhere, a bell rings.', 'red'))])
    fn('p75/dial_cmp', [l.replace('run return 0', 'run return run scoreboard players set #bad bm.rng 1') for l in rest if 'function bm:p70/solved' not in l and 'Fixed set value 1b' not in l])
    fn('p75/dial_ok', ['execute as @e[type=minecraft:item_frame,tag=bm.gvprop,distance=..14] run data modify entity @s Fixed set value 1b', 'function bm:p70/solved'])
    G.FUNCS['p70/r/dial/init'] += vbutton(16, 5, 22, 'north', 'TRY THE DIALS')

    # ================================================================== ONCE ONLY: the laurel, the trophies, the sigil
    G.FUNCS['p70/laurel'][0:0] = ['execute if score @s bm.gvlaur matches 1.. run return run function bm:p75/laurel_again', 'scoreboard players set @s bm.gvlaur 1']
    fn('p75/laurel_again', ['loot give @s loot bm:gv/coins', tellraw('@s', P + [T('A new record for the week! ', GOLD, bold=True),
                                                                             T('You already wear the Gutter Laurel - the Fixer pays you in coin instead.', 'gray')])])
    for j, k in enumerate(RM.KINDS):
        tro = G.FUNCS[f'p70/trophy/{k}']
        G.FUNCS[f'p70/trophy/{k}'] = ['scoreboard players operation #q bm.rng = @s bm.gvtro', f'scoreboard players set #bit bm.rng {2 ** j}',
                                      'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                                      'execute if score #q bm.rng matches 1 run return run function bm:p75/trophy_again',
                                      f'scoreboard players add @s bm.gvtro {2 ** j}'] + tro
    fn('p75/trophy_again', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #c bm.rng 4', inst('bm:p75/pot_add'),
                            say('Flawless! (You have this trophy already - 4 coins into the pot.)', GOLD)])
    G.FUNCS['p70/bond'][0:0] = ['execute if score @s bm.gvbs matches 1.. run return 0', 'scoreboard players set @s bm.gvbs 1']

    # ================================================================== THE BOND SIGIL: your party, not one old heist
    sec = G.FUNCS['loop/second']
    k = next(i for i, l in enumerate(sec) if 'function bm:p71/bond_read' in l)
    sigil = '*[minecraft:custom_data~{bm:"bond_sigil"}]'
    sec[k:k + 1] = [f'execute as @a if items entity @s container.* {sigil} run tag @s add bm.gvbonded',
                    f'execute as @a if items entity @s weapon.offhand {sigil} run tag @s add bm.gvbonded']
    G.FUNCS['p71/bond'] = ['execute unless score @s bm.pty matches 1.. run return 0', 'scoreboard players operation #b bm.rng = @s bm.pty', 'tag @s add bm.gvself',
                           'scoreboard players set #near bm.rng 0',
                           'execute as @a[tag=bm.gvbonded,tag=!bm.gvself,distance=..16] if score @s bm.pty = #b bm.rng run scoreboard players set #near bm.rng 1',
                           'tag @s remove bm.gvself', 'execute if score #near bm.rng matches 0 run return 0',
                           'effect give @s minecraft:regeneration 3 0 true', 'execute store result score #r bm.rng run random value 1..20',
                           'execute if score #r bm.rng matches 1 run effect give @s minecraft:absorption 20 0 true', 'particle minecraft:heart ~ ~2.1 ~ 0.2 0.1 0.2 0 1']
    ITEMS['bond_sigil']['comps']['minecraft:lore'] = [T('A gold sigil, warm when a friend is near.', 'gray'), T('Near a party member who carries', 'blue'),
                                                      T('one too: you both regenerate.', 'blue'), T('(Inventory or off-hand.)', 'gray')]

    # ================================================================== THE FEE AND THE LUCKY POOL
    tok = '*[minecraft:custom_data~{bm:"token"}]'
    fn('p75/fee', [f'execute store result score #tk bm.rng run clear @s {tok} 0',
                   f'execute if score #tk bm.rng matches ..{FEE - 1} run return run function bm:p75/fee_no',
                   f'clear @s {tok} {FEE}', f'scoreboard players add #lpool bm.gvlp {FEE}',
                   tellraw('@s', P + [T(f'You pay the Fixer\'s fee ({FEE} Tokens). ', 'gray'), T('Lucky pool: ', LUCKY),
                                      {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': LUCKY, 'bold': True}]), 'return 1'])
    fn('p75/fee_no', [tellraw('@s', P + [T(f'The Fixer\'s fee is {FEE} Black Market Tokens', 'red'), T(' - you don\'t have them, so you stay behind.', 'gray')]),
                      'playsound minecraft:entity.villager.no player @s ~ ~ ~ 1 1', 'return 0'])
    G.FUNCS['p70/join'].insert(0, 'execute unless function bm:p75/fee run return 0')

    # ================================================================== TRIES: the second page of the plans (3, 5 or 7), then the fee, then in
    import phase28 as P28
    MENU = P28.MENU['heist']
    pt = G.FUNCS['p70/pick_tier']
    k = next(i for i, l in enumerate(pt) if l == 'scoreboard players operation #asker bm.pty = @s bm.pty')
    G.FUNCS['p70/pick_tier'] = pt[:k] + ['scoreboard players operation @s bm.gvpt = #t bm.rng', 'function bm:p75/lives_menu']
    claim = pt[k:]
    lbtn = lambda c, n, col, txt: P28.btn([T(f'{n} TRIES  ', col, bold=True), T(txt, 'white')], 7610 + c, width=300,
                                          tooltip=T(f'Your crew can be knocked out {n} times (one more per crewmate past the first).', 'gray'))
    dlg = P28.multi([T('How many tries?', GOLD, bold=True)],
                    [P28.body([T('Every knock-out costs the crew a try. Run out and the heist fails: back to the den, everything gathered lost '
                                 '(you can try again).', 'gray')]),
                     P28.body([T('Fewer tries, bigger haul. ', GOLD), T('No knock-outs at all: +2 shares more.', 'gray')]),
                     P28.body([T(f'The Fixer\'s fee: {FEE} Tokens each, into the Lucky Pool (now ', 'dark_gray'), T('$(p)', LUCKY, bold=True),
                               T('). One heist in twenty is a Lucky Raid - win it and the pool is yours.', 'dark_gray')])],
                    [lbtn(1, 3, '#ff5a5a', '+4 shares - for the bold'), lbtn(2, 5, GOLD, '+2 shares'), lbtn(3, 7, LUCKY, 'no bonus - for a first try')],
                    columns=1, exit_label='Back')
    fn('p75/lives_menu', ['execute store result storage bm:gv m.p int 1 run scoreboard players get #lpool bm.gvlp', f'scoreboard players set @s bm.menu {MENU}',
                          'function bm:p75/lives_show with storage bm:gv m'])
    fn('p75/lives_show', [f'$dialog show @s {snbt(dlg)}'])
    G.FUNCS['p28/act'].append('execute if score #act bm.pay matches 7611..7613 run return run function bm:p75/pick_lives')
    holds_plans = '*[minecraft:custom_data~{bm:"heist_plans"}]'
    fn('p75/pick_lives', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                          f'execute unless items entity @s container.* {holds_plans} unless items entity @s weapon.offhand {holds_plans} run return run function bm:p28/stale',
                          'execute unless score @s bm.gvpt matches 1..5 run return run function bm:p28/stale',
                          'execute if dimension bm:gutter run return 0',
                          'scoreboard players operation #t bm.rng = @s bm.gvpt', 'scoreboard players reset @s bm.gvpt',
                          'scoreboard players operation #lvi bm.rng = #act bm.pay', 'scoreboard players remove #lvi bm.rng 7610'] +
       [f'execute if score #lvi bm.rng matches {c} run scoreboard players set #lv bm.rng {n}' for c, n in LIVES.items()] +
       # (a free crew first - the fee only once there's a vault to go to)
       ['scoreboard players set #free bm.rng 0'] + [f'execute unless score #s{s} bm.gvon matches 1 run scoreboard players set #free bm.rng 1' for s in range(SLOTS)] +
       ['execute if score #free bm.rng matches 0 run return run ' + say('Every vault crew in the city is busy - try again in a few minutes.', 'red'),
        'execute unless function bm:p75/fee run return 0'] + claim)

    # ================================================================== KNOCK-OUTS AND FAILING
    G.FUNCS['p70/died'].append('execute if entity @s[tag=bm.gvp] run function bm:p75/ko')
    fn('p75/ko', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.gvko1',
                  'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p75/ko_inst', 'tag @s remove bm.gvko1'])
    G.FUNCS['tick'] = [l.replace('execute as @a[scores={bm.gvdth=1..}] run function bm:p70/died', 'execute as @a[scores={bm.gvdth=1..}] at @s run function bm:p70/died') for l in G.FUNCS['tick']]
    fn('p75/ko_inst', ['execute unless score @s bm.gvst matches 2..3 run return 0', 'scoreboard players remove @s bm.gvlv 1', 'scoreboard players add @s bm.gvdc 1',
                       'function bm:p70/bar', 'function bm:p70/tag_mine',
                       'execute if score @s bm.gvlv matches 1.. run ' + tellraw('@a[tag=bm.gvme]', P + [{'selector': '@a[tag=bm.gvko1]', 'color': 'white'}, T(' is down! ', 'red', bold=True),
                                                                                                         {'score': {'name': '@s', 'objective': 'bm.gvlv'}, 'color': 'white', 'bold': True},
                                                                                                         T(' tries left.', 'gray')]),
                       'execute if score @s bm.gvlv matches 1 run ' + title('@a[tag=bm.gvme]', 'actionbar', T('LAST TRY - nobody else goes down!', 'red', bold=True)),
                       'execute if score @s bm.gvlv matches ..0 run function bm:p75/fail', 'tag @a[tag=bm.gvme] remove bm.gvme'])
    fn('p75/fail', ['scoreboard players set @s bm.gvst 5', 'scoreboard players set @s bm.gvpot 0'] +
       [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players set #fl{s} bm.gvfail 4' for s in range(SLOTS)] +
       ['execute as @a[tag=bm.gvme] run function bm:p75/pot_clear',
        'title @a[tag=bm.gvme] times 10 70 20', title('@a[tag=bm.gvme]', 'title', T('THE HEIST HAS FAILED', 'red', bold=True)),
        title('@a[tag=bm.gvme]', 'subtitle', T('Out of tries - everything gathered is lost', 'gray')),
        'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.bell.resonate player @s ~ ~ ~ 1 0.5',
        'execute as @a[tag=bm.gvme] at @s run playsound minecraft:entity.wither.death player @s ~ ~ ~ 0.4 1.6',
        'execute as @e[tag=bm.gvboss] if score @s bm.gvi = #gi bm.rng run kill @s'])
    # (the new instance marker takes the slot's tries)
    G.FUNCS['p70/inst_init'][-1:-1] = [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players operation @s bm.gvlc = #lc{s} bm.gvlc' for s in range(SLOTS)] + \
        [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players operation @s bm.gvlu = #lu{s} bm.gvlu' for s in range(SLOTS)] + \
        [f'execute if score @s bm.gvi matches {s + 1} run scoreboard players operation #n bm.rng = #np{s} bm.gvx' for s in range(SLOTS)] + \
        ['execute unless score @s bm.gvlc matches 1.. run scoreboard players set @s bm.gvlc 5',
         'scoreboard players operation @s bm.gvlv = @s bm.gvlc', 'scoreboard players remove #n bm.rng 1',
         'execute if score #n bm.rng matches 4.. run scoreboard players set #n bm.rng 3', 'execute if score #n bm.rng matches 1.. run scoreboard players operation @s bm.gvlv += #n bm.rng',
         'scoreboard players set @s bm.gvpot 0', 'scoreboard players set @s bm.gvdc 0',
         'execute if score @s bm.gvlu matches 1 run function bm:p75/lucky_announce', 'function bm:p70/bar']
    fn('p75/lucky_announce', ['function bm:p70/tag_mine', 'title @a[tag=bm.gvme] times 10 60 20', title('@a[tag=bm.gvme]', 'title', T('LUCKY RAID!', LUCKY, bold=True)),
                              title('@a[tag=bm.gvme]', 'subtitle', [T('Win it and the crew splits ', 'gray'), {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': LUCKY},
                                                                    T(' Tokens', 'gray')]),
                              'execute as @a[tag=bm.gvme] at @s run playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 1 1.6', 'tag @a[tag=bm.gvme] remove bm.gvme'])
    # the sheet: tries, a Lucky Raid
    sh = G.FUNCS['p70/sheet']
    k = next(i for i, l in enumerate(sh) if 'Press a button by the door to begin' in l)
    sh[k:k] = [inst('bm:p75/sheet_tries')]
    fn('p75/sheet_tries', ['execute store result storage bm:gv shl.n int 1 run scoreboard players get @s bm.gvlv', 'function bm:p75/sheet_tries2 with storage bm:gv shl',
                           'execute if score @s bm.gvlu matches 1 run data modify storage bm:gv sheet append value {text:"LUCKY RAID - win it for the pool!\\n",color:"' + LUCKY + '",bold:true}'])
    fn('p75/sheet_tries2', ['$data modify storage bm:gv sheet append value {text:"\\nTRIES: $(n)",color:"#ff7a7a",bold:true}',
                            'data modify storage bm:gv sheet append value {text:" (each knock-out costs one)\\n",color:"gray"}'])
    # the bar: alarm, tries, the pot
    bar = G.FUNCS['p70/bar']
    bar += [f'execute if score @s bm.gvi matches {s + 1} run bossbar set bm:gva{s} name ' +
            snbt([T('Alarm', 'red'), T('   Tries ', '#ff7a7a'), {'score': {'name': '@s', 'objective': 'bm.gvlv'}, 'color': 'white', 'bold': True},
                  T('   Pot ', GOLD), {'score': {'name': '@s', 'objective': 'bm.gvpot'}, 'color': 'white', 'bold': True}, T(' coins', GOLD)]) for s in range(SLOTS)]

    # ================================================================== THE POT
    wjson('bm/loot_table/gv/guard.json', {'pools': []})
    wjson('bm/loot_table/gv/boss.json', {'pools': []})
    killed = lambda tag: {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["%s"]}' % tag}}]}}}
    for key, tag, lo, hi in (('guard', 'bm.gvg', 1, 3), ('captain', 'bm.gvcap', 4, 6), ('boss', 'bm.gvboss', 14, 20)):
        wjson(f'bm/advancement/p75/kill_{key}.json', {'criteria': killed(tag), 'rewards': {'function': f'bm:p75/kill_{key}'}})
        fn(f'p75/kill_{key}', [f'advancement revoke @s only bm:p75/kill_{key}', 'execute unless entity @s[tag=bm.gvp] run return 0',
                               'scoreboard players operation #gi bm.rng = @s bm.gvi', f'execute store result score #c bm.rng run random value {lo}..{hi}',
                               inst('bm:p75/pot_add'),
                               title('@s', 'actionbar', [T('+', GOLD), {'score': {'name': '#c', 'objective': 'bm.rng'}, 'color': GOLD, 'bold': True}, T(' coins into the pot', GOLD)])])
    fn('p75/pot_add', ['execute unless score @s bm.gvst matches 1..3 run return 0', 'scoreboard players operation @s bm.gvpot += #c bm.rng', 'function bm:p70/bar'])
    # (finds: a loot table each, kept per player until the haul) #pt = the table, via storage bm:gv pf.t
    fn('p75/pot_item', ['execute store result storage bm:gv pf.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p75/pot_item2 with storage bm:gv pf'])
    fn('p75/pot_item2', ['$data modify storage bm:gv pot.p$(pid) append value {t:"$(t)"}'])
    fn('p75/pot_clear', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p75/pot_clear2 with storage bm:gv tmp'])
    fn('p75/pot_clear2', ['$data remove storage bm:gv pot.p$(pid)'])
    HA, HB = '-200 64 -197', '-198 64 -197'
    ins = lambda table: [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    wjson('bm/loot_table/p75/pot_coins.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('gutter_coin', {'type': 'minecraft:score', 'target': {'type': 'minecraft:fixed', 'name': '#pot'},
                                                                                                             'score': 'bm.rng'})]}]})
    wjson('bm/loot_table/p75/pool_tokens.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('token', {'type': 'minecraft:score', 'target': {'type': 'minecraft:fixed', 'name': '#lpe'},
                                                                                                         'score': 'bm.rng'})]}]})
    fn('p75/pot_pay', ['execute store result storage bm:gv tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p75/pot_pay2 with storage bm:gv tmp'])
    fn('p75/pot_pay2', ['$data modify storage bm:gv pp set from storage bm:gv pot.p$(pid)', '$data remove storage bm:gv pot.p$(pid)', 'function bm:p75/pot_pay3'])
    fn('p75/pot_pay3', ['execute unless data storage bm:gv pp[0] run return 0', 'function bm:p75/pot_pay4 with storage bm:gv pp[0]', 'data remove storage bm:gv pp[0]',
                        'function bm:p75/pot_pay3'])
    fn('p75/pot_pay4', ['$' + l for l in ins('$(t)')])
    haul = G.FUNCS['p70/haul']
    k = haul.index('function bm:p74/haul_pack')
    haul[k:k] = ([l.replace('execute in bm:gutter', 'execute if score #pot bm.rng matches 1.. in bm:gutter') for l in ins('bm:p75/pot_coins')] +
                 ['function bm:p75/pot_pay'] +
                 [l.replace('execute in bm:gutter', 'execute if score #lpe bm.rng matches 1.. in bm:gutter') for l in ins('bm:p75/pool_tokens')])
    pay = G.FUNCS['p70/payout_inst']
    k = next(i for i, l in enumerate(pay) if 'execute if score #sh bm.rng matches ..1 run scoreboard players set #sh bm.rng 2' in l)
    pay[k + 1:k + 1] = [f'execute if score @s bm.gvlc matches {n} run scoreboard players add #sh bm.rng {b}' for n, b in BONUS_PICK.items() if b] + \
                       ['execute if score @s bm.gvdc matches 0 run scoreboard players add #sh bm.rng 2', 'execute if score @s bm.gvdc matches 1 run scoreboard players add #sh bm.rng 1',
                        'scoreboard players operation #pot bm.rng = @s bm.gvpot', 'scoreboard players set #lpe bm.rng 0',
                        'execute if score @s bm.gvlu matches 1 run function bm:p75/lucky_pay']
    fn('p75/lucky_pay', ['scoreboard players operation #lpe bm.rng = #lpool bm.gvlp', 'execute if score #np bm.rng matches 1.. run scoreboard players operation #lpe bm.rng /= #np bm.rng',
                         'execute if score #lpe bm.rng matches ..0 run scoreboard players set #lpe bm.rng 1',
                         tellraw('@a[tag=bm.gvme]', P + [T('LUCKY RAID WON! ', LUCKY, bold=True), T('The crew splits the pool: ', 'gray'),
                                                        {'score': {'name': '#lpe', 'objective': 'bm.rng'}, 'color': LUCKY, 'bold': True}, T(' Tokens each, in The Haul.', 'gray')]),
                         f'scoreboard players set #lpool bm.gvlp {POOL_SEED}', 'execute as @e[type=minecraft:marker,tag=bm.gvr_lobby] at @s run function bm:p75/pool_show'])
    hmsg = next(i for i, l in enumerate(haul) if 'Your haul: ' in l)
    haul.insert(hmsg + 1, 'execute if score #pot bm.rng matches 1.. run ' + tellraw('@s', P + [T('The pot: ', GOLD), {'score': {'name': '#pot', 'objective': 'bm.rng'}, 'color': 'white', 'bold': True},
                                                                                         T(' coins, and everything you found - all in The Haul.', 'gray')]))

    # ================================================================== admin
    fn('admin/heist_pool', [tellraw('@s', P + [T('Lucky pool: ', LUCKY), {'score': {'name': '#lpool', 'objective': 'bm.gvlp'}, 'color': 'white'}])])
    fn('admin/heist_lucky', [f'scoreboard players set #lu{s} bm.gvlu 1' for s in range(SLOTS)] + [tellraw('@s', P + [T('Every running heist is a Lucky Raid now (after its next rebuild).', 'gray')])])

    G.FUNCS['tick'] += tick
    f = G.FUNCS['loop/fast']
    f[-1:-1] = fast
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second


def extend_offers(O, offer):
    pass


def rp(R):
    pass
