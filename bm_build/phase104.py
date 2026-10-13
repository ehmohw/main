"""2.68: THE VAULT'S LOOSE ENDS - what happens when a crew changes, someone drops out, the hall fills up, or a plan is
made from somewhere it shouldn't be.

THE VAULT COUNTS ITS GUESTS: the crew's size is checked every second, not just when it walks in. Someone leaves (by the
  Fixer's Door, the Ledger or a dropped connection) and the guards still standing lose the health and bite they had for
  them; someone joins and they gain it. The crew is told ("3 in the crew now - the guards ease off").
LEAVE FROM ANYWHERE: on a heist, the Fixer's Ledger opens a card first - THE FIXER'S OFFICE, or LEAVE THE HEIST (home now,
  gear back, the fee and your share stay behind) - so nobody has to walk back to the den to quit.
A DROPPED CONNECTION: a crew that vanishes all at once (a crash, a lost connection) keeps its heist for three minutes, not
  twenty seconds, so a quick rejoin finds it still there. (A crew that walks out the door still frees its vault at once.)
  If the leader drops out while the crew waits on their call, the choice passes to the crew straight away, and a leader
  who comes back finds it has moved on. Rejoining also clears a half-finished Ledger trip or exit question.
KNOCKED OUT: what you dropped where you fell comes back to you when you're back on your feet in the den (your kit was
  always replaced; now your Tokens and finds come back too, unless lava took them).
SAFE PLANS: the Heist Plans start a heist only from safe ground (the same rules as the Ledger's Locker Hall trip: on the
  ground, not mounted or in water or lava, not hurt in the last 10 seconds, not in a boss dungeon) - they bring you back
  to that very spot. A crewmate who isn't on safe ground isn't pulled in (or charged); they can join with their own plans
  once they are.
A FULL CITY: when all eight vault crews are busy, whoever was turned away is told the moment one frees up.
A FULL LOCKER HALL: while fewer than five bays are free, it's one bay each - nobody claims a second or third. And when
  every bay is taken and someone without a bay needs one, the Fixer frees one up: a spare (someone's second or third bay -
  its things go into their other bays if they fit), or the bay of someone who hasn't been seen for 20 days. Whatever
  doesn't fit goes to that player's LOST & FOUND: Lost & Found crates (like The Haul) handed to them the next time they
  step into the Locker Hall.
"""
from items import T, ITEMS
from nbt import snbt, B, F, Int
import phase28 as P28
import phase70 as P70
import phase70_rooms as RM
import phase72 as P72
import phase80 as P80
import phase84 as P84

GOLD = '#ffcf40'
LOCK = '#c89a5a'
SL = P70.SLOTS
# (2.68) the Locker Key: only ever carried in the gutter - handed over on arrival, taken back on leaving; it can't be dropped,
# stored or kept through a death (Curse of Vanishing, unseen)
ITEMS['locker_key']['comps']['minecraft:lore'] = [T('Brass, and stamped with your name.', 'gray'), T('Opens your bays in the Locker Hall -', 'blue'),
                                                  T('hold it when you open one.', 'blue'),
                                                  T('The Fixer hands it over in the gutter and', 'dark_gray'), T('takes it back when you leave.', 'dark_gray')]
ITEMS['locker_key']['comps']['minecraft:enchantments'] = {'minecraft:vanishing_curse': Int(1)}
ITEMS['locker_key']['comps']['minecraft:enchantment_glint_override'] = False
ITEMS['locker_key']['comps'].setdefault('minecraft:tooltip_display', {'hidden_components': []})['hidden_components'].append('minecraft:enchantments')
C_LEAVE_NOW = 7729
C_LEAVE_ASK = 7899                       # (in the Office's range: the 'Leave the heist' button)
GRACE_DROP = 180                 # seconds a heist waits for a crew that vanished (logged out) - 20 for one that walked out
IDLE_DAYS = 20                   # a bay whose keeper hasn't been seen for this many days can be freed for a newcomer
FAIR_FREE = 5                    # a second or third bay only while at least this many are free
LF_POS = (-245, 64, -242)        # (unused spot by the hall's south wall, east of the way back)


def generate(G):
    fn, tellraw, title = G.fn, G.tellraw, G.title
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    PV = [T('[', 'dark_gray'), T('Vault', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray', pre=None: tellraw('@s', (pre or P) + [T(txt, col)])
    crew = lambda s: f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}}]'
    num = lambda n, col='white': {'score': {'name': n, 'objective': 'bm.rng'}, 'color': col, 'bold': True}
    tick, second = [], []
    objs = ['bm.gvcw', 'bm.lkday', 'bm.lkc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard objectives add bm.lgo minecraft.custom:minecraft.leave_game']
    G.OBJECTIVES += objs + ['bm.lgo']

    # ================================================================== THE VAULT COUNTS ITS GUESTS
    # (each scaled mob remembers the crew it was scaled for; a change rescales the living ones - health keeps its share)
    G.FUNCS['p87/hpscale'].append('scoreboard players operation @s bm.gvcw = #crew bm.rng')
    for s in range(SL):
        w = G.FUNCS[f'p70/s{s}/watch']
        k = next(i for i, l in enumerate(w) if l.startswith('execute store result score #n bm.rng if entity'))
        w.insert(k + 1, f'execute if score #n bm.rng matches 1.. unless score #n bm.rng = #np{s} bm.gvx run function bm:p104/s{s}/crew')
        fn(f'p104/s{s}/crew', [f'scoreboard players operation #npo bm.rng = #np{s} bm.gvx', f'scoreboard players operation #np{s} bm.gvx = #n bm.rng',
                               'scoreboard players operation #crew bm.rng = #n bm.rng', 'execute if score #crew bm.rng matches 7.. run scoreboard players set #crew bm.rng 6',
                               f'execute in bm:gutter as @e[type=!minecraft:player,scores={{bm.gvi={s + 1},bm.gvcw=1..}}] unless score @s bm.gvcw = #crew bm.rng run function bm:p104/rescale',
                               f'execute if score #n bm.rng < #npo bm.rng run ' + tellraw(crew(s), P + [num('#n'), T(' in the crew now', 'white'), T(' - the guards ease off.', 'gray')]),
                               f'execute if score #n bm.rng > #npo bm.rng run ' + tellraw(crew(s), P + [num('#n'), T(' in the crew now', 'white'), T(' - the guards toughen up.', 'gray')])])
    fn('p104/rescale', ['scoreboard players set #k bm.rng 35', 'execute if entity @s[tag=bm.gvboss] run scoreboard players set #k bm.rng 50',
                        'scoreboard players operation #fo bm.rng = @s bm.gvcw', 'scoreboard players remove #fo bm.rng 1', 'scoreboard players operation #fo bm.rng *= #k bm.rng',
                        'scoreboard players add #fo bm.rng 100',
                        'scoreboard players operation #fn bm.rng = #crew bm.rng', 'scoreboard players remove #fn bm.rng 1', 'scoreboard players operation #fn bm.rng *= #k bm.rng',
                        'scoreboard players add #fn bm.rng 100',
                        'execute store result score #m bm.rng run attribute @s minecraft:max_health base get 100',
                        'scoreboard players operation #m bm.rng *= #fn bm.rng', 'scoreboard players operation #m bm.rng /= #fo bm.rng',
                        'execute if score #m bm.rng matches ..99 run scoreboard players set #m bm.rng 100',
                        'execute store result storage bm:gv h double 0.01 run scoreboard players get #m bm.rng', 'function bm:p70/hp with storage bm:gv',
                        'execute store result score #hh bm.rng run data get entity @s Health 100',
                        'scoreboard players operation #hh bm.rng *= #fn bm.rng', 'scoreboard players operation #hh bm.rng /= #fo bm.rng',
                        'execute if score #hh bm.rng matches ..99 run scoreboard players set #hh bm.rng 100',
                        'execute store result entity @s Health float 0.01 run scoreboard players get #hh bm.rng',
                        'execute store success score #hadm bm.rng run attribute @s minecraft:attack_damage modifier value get bm:gv_crew',
                        'execute if score #hadm bm.rng matches 1 run attribute @s minecraft:attack_damage modifier remove bm:gv_crew'] +
       [f'execute if score #hadm bm.rng matches 1 if score #crew bm.rng matches {n} run attribute @s minecraft:attack_damage modifier add bm:gv_crew {0.1 * (n - 1):.1f} add_multiplied_base'
        for n in range(2, 7)] +
       [f'execute if entity @s[tag=bm.gvboss] if score @s bm.gvi matches {s + 1} store result bossbar bm:gvb{s} max run attribute @s minecraft:max_health get' for s in range(SL)] +
       ['scoreboard players operation @s bm.gvcw = #crew bm.rng'])

    # ================================================================== LEAVE FROM ANYWHERE: on a heist the Ledger's Office has 'Leave the heist' at the bottom
    import copy
    MC = P80.MENU_CODE
    hub = copy.deepcopy(P80.HUB)
    hub['actions'].append(P28.btn([T('⏏ ', '#ff9a7a'), T('Leave the heist', '#ff9a7a', bold=True)], C_LEAVE_ASK, width=150,
                                  tooltip=T('Home now, from right here: your own gear comes back; the fee and any share stay behind. (It asks first.)', 'gray')))
    off = G.FUNCS['p80/office']
    assert off[-1] == 'function bm:p80/office_dlg with storage bm:ui of', off[-1]
    off.insert(len(off) - 1, 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter run return run function bm:p104/office_dlg with storage bm:ui of')
    fn('p104/office_dlg', [f'$dialog show @s {P28.inline(hub)}'])
    ask = P28.multi([T('Leave the heist?', '#ff9a7a', bold=True)],
                    [P28.body([T('You go home as you came, and your own gear comes back. ', 'white'),
                               T('The fee - and any share of the haul - stays behind.', 'gray')], 300)],
                    [P28.btn([T('Leave now', '#ff9a7a', bold=True)], C_LEAVE_NOW, width=150),
                     P28.btn([T('Stay on the job', 'white')], MC, width=150)], columns=2, exit_label='Back')
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {C_LEAVE_ASK} run return run function bm:p104/leave_ask')
    fn('p104/leave_ask', ['execute unless entity @s[tag=bm.gvp] run return run function bm:p80/office', 'execute unless dimension bm:gutter run return run function bm:p80/office',
                          f'dialog show @s {snbt(ask)}'])
    G.FUNCS['p28/act'].append(f'execute if score #act bm.pay matches {C_LEAVE_NOW} run return run function bm:p104/leave_now')
    fn('p104/leave_now', ['execute unless entity @s[tag=bm.gvp] run return 0', 'execute unless dimension bm:gutter run return 0',
                          'tag @s add bm.exask', 'function bm:p103/leave_yes'])

    # ================================================================== (2.68) WHAT A ROOM LENDS, IT TAKES BACK
    # (the Shooting Gallery's bow and arrows, the Rat Ball game's snowballs, the Brawl's wind charges: room loans - gone from the
    #  whole crew the moment a room is beaten, so nobody walks on with them)
    for f_ in ('p91/gallery/ready', 'p91/grass/start', 'p91/grass/center2', 'p85/brawl/go'):
        L = G.FUNCS[f_]; n0 = sum('bm_kit:1b' in l for l in L)
        L[:] = [l.replace('minecraft:custom_data={bm_kit:1b}', 'minecraft:custom_data={bm_kit:1b,bm_room:1b}') for l in L]
        assert n0, f_
    G.FUNCS['p70/solved'].append('execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run clear @s *[minecraft:custom_data~{bm_room:1b}]')

    # ================================================================== (2.68) PUZZLES AND FIGHTS, TURN ABOUT
    # (the rooms alternate: a puzzle (or a climb), then a fight - the Counting House, an Ambush, the Pit - then a puzzle...; any
    #  room can still be an event room now and then. A pool that runs dry falls back to the tier's whole list)
    import phase75 as P75
    FIGHTS = ['guards', 'ambush', 'pit']
    G.FUNCS['p75/lay/pick'] = ['scoreboard players set #try bm.rng 0', 'scoreboard players operation #par bm.rng = #q bm.rng', 'scoreboard players operation #par bm.rng %= #2 bm.rng'] + \
        [f'execute if score #gt bm.rng matches {t} if score #par bm.rng matches 0 run return run function bm:p104/lay/fight{t}' for t in range(1, 6)] + \
        [f'execute if score #gt bm.rng matches {t} run return run function bm:p104/lay/puzzle{t}' for t in range(1, 6)]
    for t in range(1, 6):
        tp_ = P75.TIER_POOL[t]
        fights = ['guards'] + [k for k in FIGHTS[1:] if k in tp_]
        puzzles = [k for k in tp_ if k not in FIGHTS]
        for nm_, pool in (('fight', fights), ('puzzle', puzzles)):
            ids = [P75.KINDS.index(k) for k in pool]
            fn(f'p104/lay/{nm_}{t}', ['scoreboard players add #try bm.rng 1', f'execute if score #try bm.rng matches 25.. run return run function bm:p75/lay/pick{t}',
                                      f'execute store result score #i bm.rng run random value 0..{len(ids) - 1}'] +
               [f'execute if score #i bm.rng matches {i} run scoreboard players set #r bm.rng {j}' for i, j in enumerate(ids)] +
               [f'execute if score #r bm.rng matches {P75.KINDS.index(k)} if score #cy bm.rng matches {my + 1}.. run return run function bm:p104/lay/{nm_}{t}'
                for k, my in P75.ROOM_MAXY.items() if k in pool] +
               ['function bm:p75/lay/bit', f'execute if score #q2 bm.rng matches 1 run return run function bm:p104/lay/{nm_}{t}',
                'scoreboard players operation #pool bm.rng += #bit bm.rng'])

    # ================================================================== (2.68) ANOTHER JOB: PAPERWEIGHTS AND FOOD TOPPED BACK UP
    ka = P72.kit_arg
    fn('p104/resupply', ['clear @s *[minecraft:custom_data~{bm:"paperweight"}]', f'clear @s minecraft:cooked_beef[minecraft:custom_data~{{bm_kit:1b}}]',
                         f'give @s {ka("paperweight")} 4', f'give @s {ka(P72.KIT_FOOD[0])} {P72.KIT_FOOD[1]}'])
    for s_ in range(SL):
        for f_ in (f'p70/s{s_}/enter', f'p70/s{s_}/join'):
            G.FUNCS[f_].insert(0, 'execute if items entity @s container.* *[minecraft:custom_data~{bm_kit:1b}] run function bm:p104/resupply')

    # ================================================================== (2.68) GUARDS STAY IN THEIR ROOM
    # (each guard and guardian belongs to the room it's first seen in - the nearest room marker then; wandered out through a door
    #  into a corridor, the water or the room before: back to the middle of its own room)
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.gvrid dummy']
    G.OBJECTIVES.append('bm.gvrid')
    for tg in ('bm.gvg', 'bm.gvboss'):
        second.append(f'execute in bm:gutter as @e[tag={tg},tag=!bm.gvlsh] at @s run function bm:p104/leash/adopt')
    second.append('execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvr,scores={bm.gvrid=1..}] at @s run function bm:p104/leash/room')
    fn('p104/leash/adopt', ['scoreboard players set #rid bm.rng 0',
                            'execute as @e[type=minecraft:marker,tag=bm.gvr,distance=..40,sort=nearest,limit=1] run function bm:p104/leash/rid',
                            'execute if score #rid bm.rng matches 0 run return 0',
                            'scoreboard players operation @s bm.gvrid = #rid bm.rng', 'tag @s add bm.gvlsh'])
    fn('p104/leash/rid', ['execute unless score @s bm.gvrid matches 1.. run scoreboard players add #ridc bm.gvrid 1',
                          'execute unless score @s bm.gvrid matches 1.. run scoreboard players operation @s bm.gvrid = #ridc bm.gvrid',
                          'scoreboard players operation #rid bm.rng = @s bm.gvrid'])
    room_box = lambda length: f'positioned ~-12.5 ~-4 ~-12.5 as @e[tag=bm.gvlsh] if score @s bm.gvrid = #rid bm.rng unless entity @s[dx={length},dy=15,dz=25] at @s run function bm:p104/leash/back'
    fn('p104/leash/room', ['scoreboard players operation #rid bm.rng = @s bm.gvrid', 'tag @s add bm.gvlrm',
                           f'execute if entity @s[tag=bm.gvr_vault] {room_box(RM.VAULT_LEN)}',
                           f'execute unless entity @s[tag=bm.gvr_vault] {room_box(RM.W)}',
                           'tag @s remove bm.gvlrm'])
    fn('p104/leash/back', ['particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.02 8', 'tp @s @e[type=minecraft:marker,tag=bm.gvlrm,limit=1]',
                           'execute at @s run particle minecraft:poof ~ ~1 ~ 0.3 0.5 0.3 0.02 8'])

    # ================================================================== (2.68) THE LOCKER KEY: yours while you're in the gutter, and only there
    key = '*[minecraft:custom_data~{bm:"locker_key"}]'
    key_nbt = '{components:{"minecraft:custom_data":{bm:"locker_key"}}}'
    no_key = ' '.join(f'unless items entity @s {sl} {key}' for sl in ('container.*', 'weapon.offhand', 'player.cursor', 'player.crafting.*'))
    second += [f'execute as @a[scores={{bm.pid=1..}},gamemode=!spectator] at @s if dimension bm:gutter {no_key} run function bm:p104/key/give',
               f'execute as @a at @s unless dimension bm:gutter if items entity @s container.* {key} run clear @s {key}',
               f'execute as @a at @s unless dimension bm:gutter if items entity @s weapon.offhand {key} run item replace entity @s weapon.offhand with minecraft:air',
               f'execute as @a if items entity @s enderchest.* {key} run function bm:p104/key/ender',
               f'execute as @e[type=minecraft:item] if items entity @s contents {key} run kill @s',                  # (dropped: gone - a fresh one's in your hand)
               f'execute in bm:gutter positioned {P84.HX} 60 {P84.HZ} if entity @a[dx=15,dy=12,dz=15] run function bm:p104/key/lockers']
    fn('p104/key/give', ['execute store result storage bm:lk tmp.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p84/lk/key2 with storage bm:lk tmp'])
    fn('p104/key/ender', [f'execute if items entity @s enderchest.{n} {key} run item replace entity @s enderchest.{n} with minecraft:air' for n in range(27)])
    fn('p104/key/lockers', [f'data remove block {cx} {cy} {cz} Items[{key_nbt}]' for n_, cs, _p in P84.bays() for cx, cy, cz, _s in cs])

    # ================================================================== (2.68) THE DEN'S SHOPKEEPERS: one of each, ever
    # (a den built over a heist that was never swept up - a world closed mid-heist - got a second set; the den makes sure, and any
    #  extra copy already standing goes)
    li = G.FUNCS['p70/r/lobby/init']
    for tg in ('bm.gvgt', 'bm.gvrec', 'bm.gvtail'):
        k = next(i for i, l in enumerate(li) if l.startswith('summon minecraft:villager') and f'"{tg}"' in l)
        li.insert(k, f'kill @e[type=minecraft:villager,tag={tg},distance=..24]')
        nm_ = tg[5:]
        fn(f'p104/one_{nm_}', [f'execute unless entity @e[type=minecraft:villager,tag={tg},tag=bm.gvone,distance=..24] run tag @s add bm.gvone'])  # (one at a time)
        second += [f'execute in bm:gutter as @e[type=minecraft:villager,tag={tg},tag=!bm.gvone] at @s run function bm:p104/one_{nm_}',
                   f'execute in bm:gutter run kill @e[type=minecraft:villager,tag={tg},tag=!bm.gvone]']
    # (rig parts stranded in the void, far below anyone - the orphan sweep only looks near players: gone)
    second += ['execute as @e[type=minecraft:item_display] at @s if entity @s[y=-4096,dy=3936] run kill @s',
               'execute as @e[type=minecraft:block_display] at @s if entity @s[y=-4096,dy=3936] run kill @s']

    # ================================================================== A DROPPED CONNECTION
    # (who's left when someone goes: the last one out by a door marks the heist "walked out" - a fast cleanup; otherwise it waits)
    G.FUNCS['p70/unraid'].insert(0, 'execute if score @s bm.gvi matches 1.. run function bm:p104/left')
    fn('p104/left', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.lfme', 'scoreboard players set #n bm.rng 0',
                     'execute as @a[tag=bm.gvp,tag=!bm.lfme] if score @s bm.gvi = #gi bm.rng run scoreboard players add #n bm.rng 1', 'tag @s remove bm.lfme'] +
       [f'execute if score #n bm.rng matches 0 if score #gi bm.rng matches {s + 1} run scoreboard players set #lf{s} bm.gve 1' for s in range(SL)])
    for s in range(SL):
        w = G.FUNCS[f'p70/s{s}/watch']
        k = next(i for i, l in enumerate(w) if l.endswith(f'run function bm:p70/s{s}/clean'))
        assert w[k] == f'execute if score #e{s} bm.gve matches 20.. run function bm:p70/s{s}/clean', w[k]
        w[k:k + 1] = [f'execute if score #n bm.rng matches 1.. run scoreboard players set #lf{s} bm.gve 0',
                      f'execute if score #lf{s} bm.gve matches 1 if score #e{s} bm.gve matches 20.. run function bm:p70/s{s}/clean',
                      f'execute unless score #lf{s} bm.gve matches 1 if score #e{s} bm.gve matches {GRACE_DROP}.. run function bm:p70/s{s}/clean']
        G.FUNCS[f'p70/s{s}/clean'].append(f'scoreboard players set #lf{s} bm.gve 0')
        G.FUNCS[f'p70/s{s}/claim'].insert(0, f'scoreboard players set #lf{s} bm.gve 0')
    # (the leader drops out while the crew waits on them: the choice passes on now)
    for s in range(SL):
        dt = G.FUNCS[f'p103/s{s}/dt']
        asker = f'@a[tag=bm.gvask,scores={{bm.gvnx={s + 1}}}]'
        old = f'execute unless entity {asker} run return run scoreboard players set #dt{s} bm.gvdt 0'
        assert dt[0] == old, dt[0]
        dt[0] = f'execute unless entity {asker} run return run function bm:p104/s{s}/no_asker'
        deciding = f'@a[tag=bm.gvp,scores={{bm.gvi={s + 1}}},tag=bm.gvnext]'
        fn(f'p104/s{s}/no_asker', [f'scoreboard players set #dt{s} bm.gvdt 0', f'execute if entity {deciding} run return 0',
                                   f'execute unless entity {crew(s)} run return 0', f'function bm:p104/s{s}/lead_off'])
        second.append(f'execute if score #s{s} bm.gvon matches 1 if entity @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}},tag=bm.gvin] run function bm:p104/s{s}/lead_chk')
        fn(f'p104/s{s}/lead_chk', [f'execute if entity @a[tag=bm.gvp,scores={{bm.gvi={s + 1}}},tag=bm.gvask] run return 0',
                                   f'execute if entity {deciding} run return 0', f'function bm:p104/s{s}/lead_off'])
        fn(f'p104/s{s}/lead_off', [f'scoreboard players set #dt{s} bm.gvdt 0', f'tag {crew(s)} remove bm.gvoffer', f'tag {crew(s)} remove bm.gvin',
                                   tellraw(crew(s), P + [T('Your leader has dropped out - ', 'gray'), T('the choice passes to the crew.', GOLD)]),
                                   f'execute as {crew(s)[:-1]},limit=1] run scoreboard players operation #ld{s} bm.gvld = @s bm.pid',
                                   f'function bm:p101/s{s}/ask'])
    # (back from a dropped connection: no half-finished trips or questions; a choice that moved on stays moved on)
    tick.append('execute as @a[scores={bm.lgo=1..}] run function bm:p104/login')
    fn('p104/login', ['scoreboard players reset @s bm.lgo', 'tag @s remove bm.lkch', 'scoreboard players reset @s bm.lkch', 'tag @s remove bm.exon', 'tag @s remove bm.exask',
                      'execute if entity @s[tag=bm.gvask] run function bm:p104/login_stale', 'execute if entity @s[tag=bm.gvnext] run function bm:p104/login_stale'])
    fn('p104/login_stale', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'tag @s add bm.lgme', 'scoreboard players set #other bm.rng 0',
                            'execute as @a[tag=bm.gvp,tag=!bm.lgme,tag=bm.gvask] if score @s bm.gvi = #gi bm.rng run scoreboard players set #other bm.rng 1',
                            'execute as @a[tag=bm.gvp,tag=!bm.lgme,tag=bm.gvnext] if score @s bm.gvi = #gi bm.rng run scoreboard players set #other bm.rng 1',
                            'tag @s remove bm.lgme', 'execute if score #other bm.rng matches 0 run return 0',
                            'tag @s remove bm.gvask', 'tag @s remove bm.gvnext', 'scoreboard players reset @s bm.gvnx',
                            say('While you were away, the choice passed to your crew.', GOLD)])

    # ================================================================== KNOCKED OUT: what you dropped comes back
    # (the moment you fall, what you dropped is marked yours and nobody else can pick it up; back on your feet, it comes to you)
    G.OBJECTIVES += ['bm.kdo']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.kdo dummy']
    G.FUNCS['p70/died'].append('execute if entity @s[tag=bm.gvp] run function bm:p104/ko_mark')
    fn('p104/ko_mark', ['execute unless data entity @s LastDeathLocation run return 0', 'data modify storage bm:gv kd set value {}',
                        'data modify storage bm:gv kd.dim set from entity @s LastDeathLocation.dimension',
                        'execute store result storage bm:gv kd.x int 1 run data get entity @s LastDeathLocation.pos[0]',
                        'execute store result storage bm:gv kd.y int 1 run data get entity @s LastDeathLocation.pos[1]',
                        'execute store result storage bm:gv kd.z int 1 run data get entity @s LastDeathLocation.pos[2]',
                        'scoreboard players operation #kdp bm.rng = @s bm.pid', 'function bm:p104/ko_mark2 with storage bm:gv kd'])
    fn('p104/ko_mark2', ['$execute in $(dim) positioned $(x).5 $(y) $(z).5 as @e[type=minecraft:item,distance=..5,tag=!bm.kdi] run function bm:p104/ko_mark_chk'])
    fn('p104/ko_mark_chk', ['execute store result score #pd bm.rng run data get entity @s PickupDelay', 'execute if score #pd bm.rng matches 30.. run function bm:p104/ko_mark3'])
    fn('p104/ko_mark3', ['tag @s add bm.kdi', 'scoreboard players operation @s bm.kdo = #kdp bm.rng', 'data modify entity @s PickupDelay set value 32767s'])
    G.FUNCS['p70/revive'].append('function bm:p104/ko_items')
    fn('p104/ko_items', ['scoreboard players operation #kdp bm.rng = @s bm.pid', 'tag @s add bm.kdme', 'scoreboard players set #kdn bm.rng 0',
                         'execute as @e[type=minecraft:item,tag=bm.kdi] if score @s bm.kdo = #kdp bm.rng run function bm:p104/ko_item', 'tag @s remove bm.kdme',
                         'execute if score #kdn bm.rng matches 1.. run ' + title('@s', 'actionbar', T('What you dropped is back in your pockets.', GOLD))])
    fn('p104/ko_item', ['scoreboard players add #kdn bm.rng 1', 'tag @s remove bm.kdi', 'scoreboard players reset @s bm.kdo', 'data modify entity @s PickupDelay set value 0s',
                        'tp @s @a[tag=bm.kdme,limit=1]'])
    # (anyone who leaves the heist before getting up again: theirs still come to them - or, if they're gone, fade normally)
    G.FUNCS['p70/unraid'].append('function bm:p104/ko_items')

    # ================================================================== SAFE PLANS (the Ledger trip's rules - phase103 section 8)
    fn('admin/heist_plans_anywhere', ['scoreboard players set #plany bm.rng 1', tellraw('@s', P + [T('The Heist Plans work from anywhere now, safe ground or not (admin/heist_plans_safe to restore).', 'gray')])])
    fn('admin/heist_plans_safe', ['scoreboard players set #plany bm.rng 0', tellraw('@s', P + [T('The Heist Plans start a heist only from safe ground again.', 'gray')])])
    fn('p104/unsafe', ['execute if score #plany bm.rng matches 1 run return 0', 'execute if dimension bm:gutter run return 0',
                       'execute if dimension bm:hollow_throne run return 1', 'execute if predicate bm:p103/boss_dungeon run return 1', 'execute if entity @s[tag=bm.adv] run return 1',
                       'execute if predicate bm:p21/riding run return 2', 'execute if predicate bm:p103/wet run return 3',
                       'execute unless entity @s[nbt={OnGround:1b}] run return 4',
                       'execute if score @s bm.lkdt matches 1.. run scoreboard players set @s bm.lkht 10', 'execute if score @s bm.lkht matches 1.. run return 5', 'return 0'])
    why = {1: 'Not from inside a boss dungeon - head back out first.', 2: 'Get off your mount first.', 3: 'Get out of the water (or lava) first.',
           4: 'Find your feet first - the plans bring you back to this very spot.'}
    fn('p104/plans_no', [f'execute if score #why bm.rng matches {k} run ' + say(v, 'red') for k, v in why.items()] +
       ['execute if score #why bm.rng matches 5 run ' + tellraw('@s', P + [T('You were hurt just now - wait ', 'red'), {'score': {'name': '@s', 'objective': 'bm.lkht'}, 'color': 'white', 'bold': True},
                                                                          T(' more second(s), then plan it.', 'red')]),
        'playsound minecraft:entity.villager.no player @s ~ ~ ~ 0.8 1'])
    chk = ['scoreboard players set #why bm.rng 0', 'execute unless entity @s[tag=bm.gvnext] at @s store result score #why bm.rng run function bm:p104/unsafe',
           'execute unless score #why bm.rng matches 0 run return run function bm:p104/plans_no']
    for f_ in ('p70/pick_tier', 'p75/pick_lives'):
        L = G.FUNCS[f_]
        k = next(i for i, l in enumerate(L) if 'if dimension bm:gutter run return 0' in l)
        L[k + 1:k + 1] = chk
    # (a crewmate pulled along: only from safe ground - and only then charged)
    for s in range(SL):
        G.FUNCS[f'p70/s{s}/recruit'][0:0] = ['execute at @s unless function bm:p104/safe_q run return run function bm:p104/left_out']
    fn('p104/safe_q', ['execute store result score #why bm.rng run function bm:p104/unsafe', 'execute if score #why bm.rng matches 0 run return 1', 'return 0'])
    fn('p104/left_out', [say('Your crew went in without you - you weren\'t on safe ground. Use your own Heist Plans to join them once you are.', GOLD),
                         'playsound minecraft:block.note_block.bass player @s ~ ~ ~ 0.8 0.8'])
    jp = G.FUNCS['p70/plans']
    k = next(i for i, l in enumerate(jp) if 'run return run function bm:p74/join_party' in l)
    jp[k] = jp[k].replace('run return run function bm:p74/join_party', 'run return run function bm:p104/join_try')
    fn('p104/join_try', ['scoreboard players set #why bm.rng 0', 'execute at @s store result score #why bm.rng run function bm:p104/unsafe',
                         'execute unless score #why bm.rng matches 0 run return run function bm:p104/plans_no', 'function bm:p74/join_party'])
    oldt = "You're already in the vault. (The emerald plate in the treasury - or the gold plate in the den - takes you out.)"
    assert any(oldt in l for l in jp), 'the plans\' in-the-vault line moved'
    jp[:] = [l.replace(oldt, "You're already in the vault. (The Fixer's Door - in the den, or the treasury once it's open - takes you out; or the Ledger.)") for l in jp]

    # ================================================================== A FULL CITY: told when a vault frees up
    pl = G.FUNCS['p75/pick_lives']
    busy = 'Every vault crew in the city is busy - try again in a few minutes.'
    n_ = 0
    for i, l in enumerate(pl):
        if busy in l and ' run return run ' in l:
            pl[i] = l.split(' run return run ')[0] + ' run return run function bm:p104/busy'; n_ += 1
    assert n_ == 2, n_
    fn('p104/busy', ['tag @s add bm.gvq', title('@s', 'actionbar', T('Every vault crew in the city is busy - the Fixer will tell you when one frees up.', 'red'))])
    for s in range(SL):
        G.FUNCS[f'p70/s{s}/clean'] += ['execute as @a[tag=bm.gvq] at @s run playsound minecraft:block.note_block.bell player @s ~ ~ ~ 1 1.2',
                                       tellraw('@a[tag=bm.gvq]', P + [T('A vault crew is free now', GOLD, bold=True), T(' - unroll your Heist Plans.', 'gray')]),
                                       'tag @a remove bm.gvq']

    # ================================================================== A FULL LOCKER HALL
    B_ = P84.bays()
    lkb = '@e[type=minecraft:interaction,tag=bm.lkb]'
    # (keepers seen: once a minute, every bay of everyone online is marked with today's day)
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #lkmin bm.lkc 0']
    second += ['scoreboard players add #lkmin bm.lkc 1', 'execute if score #lkmin bm.lkc matches 60.. run function bm:p104/lk/seen_all']
    fn('p104/lk/seen_all', ['scoreboard players set #lkmin bm.lkc 0', 'execute as @a[scores={bm.pid=1..}] run function bm:p104/lk/seen'])
    fn('p104/lk/seen', ['scoreboard players operation #p bm.rng = @s bm.pid',
                        f'execute in bm:gutter as {lkb} if score @s bm.lko = #p bm.rng run scoreboard players operation @s bm.lkday = #day bm.bm'])
    G.FUNCS['p84/lk/claim'].append(f'execute in bm:gutter as {lkb} if score @s bm.lko = #me bm.rng run scoreboard players operation @s bm.lkday = #day bm.bm')
    # (one each while the hall's nearly full)
    cl = G.FUNCS['p84/lk/claim']
    k = next(i for i, l in enumerate(cl) if f'execute if score #n bm.rng matches {P84.MAXBAYS}.. run return run' in l)
    cl[k + 1:k + 1] = [f'execute store result score #taken bm.rng if entity @e[type=minecraft:interaction,tag=bm.lkb,scores={{bm.lko=1..}}]',
                       f'scoreboard players set #free bm.rng {len(B_)}', 'scoreboard players operation #free bm.rng -= #taken bm.rng',
                       f'execute if score #n bm.rng matches 1.. if score #free bm.rng matches ..{FAIR_FREE - 1} run return run ' +
                       say(f'The hall is nearly full - while fewer than {FAIR_FREE} bays are free, it\'s one bay each.', 'red', PV)]
    # (every bay taken, and you've none: the Fixer frees one)
    k = next(i for i, l in enumerate(cl) if 'Somebody already keeps their things in this one.' in l)
    cl[k] = 'execute if score #o bm.rng matches 1.. run return run function bm:p104/lk/taken'
    fn('p104/lk/taken', ['scoreboard players operation #me bm.rng = @s bm.pid', 'scoreboard players set #n bm.rng 0',
                         f'execute as {lkb} if score @s bm.lko = #me bm.rng run scoreboard players add #n bm.rng 1',
                         f'execute store result score #taken bm.rng if entity @e[type=minecraft:interaction,tag=bm.lkb,scores={{bm.lko=1..}}]',
                         f'execute if score #n bm.rng matches 1.. run return run ' + say('Somebody already keeps their things in this one.', 'red', PV),
                         f'execute if score #taken bm.rng matches ..{len(B_) - 1} run return run ' + say('Somebody already keeps their things in this one - but there are free bays.', 'red', PV),
                         'function bm:p104/lk/reclaim'])
    fn('p104/lk/reclaim', [
        # how many bays each keeper holds
        f'execute as {lkb} run scoreboard players set @s bm.lkc 0',
        f'execute as @e[type=minecraft:interaction,tag=bm.lkb,scores={{bm.lko=1..}}] run function bm:p104/lk/count',
        'scoreboard players operation #idle bm.rng = #day bm.bm', f'scoreboard players remove #idle bm.rng {IDLE_DAYS}',
        f'tag {lkb} remove bm.lkvic',
        # the clicked bay, if it's a spare or long idle; else any spare (of a keeper of three first); else any long-idle bay
        'execute as @e[type=minecraft:interaction,tag=bm.lkme,scores={bm.lkc=2..}] run tag @s add bm.lkvic',
        'execute unless entity @e[tag=bm.lkvic] as @e[type=minecraft:interaction,tag=bm.lkme] if score @s bm.lkday <= #idle bm.rng run tag @s add bm.lkvic',
        'execute unless entity @e[tag=bm.lkvic] as @e[type=minecraft:interaction,tag=bm.lkb,scores={bm.lkc=3..},limit=1,sort=random] run tag @s add bm.lkvic',
        'execute unless entity @e[tag=bm.lkvic] as @e[type=minecraft:interaction,tag=bm.lkb,scores={bm.lkc=2..},limit=1,sort=random] run tag @s add bm.lkvic',
        f'execute unless entity @e[tag=bm.lkvic] as {lkb} if score @s bm.lkday <= #idle bm.rng run tag @s add bm.lkvic',
        'execute unless entity @e[tag=bm.lkvic] run return run ' + say(f'Every bay is taken, one to a keeper, and all in use. When someone gives one up - or stays away {IDLE_DAYS} days - '
                                                                        'there\'ll be room.', 'red', PV),
        'execute as @e[tag=bm.lkvic,limit=1] run function bm:p104/lk/evict',
        # now claim it as if it had been free all along
        f'tag {lkb} remove bm.lkme', 'tag @e[tag=bm.lkvic,limit=1] add bm.lkme', 'scoreboard players operation #b bm.rng = @e[tag=bm.lkme,limit=1] bm.lkn',
        'scoreboard players set #o bm.rng 0', f'tag {lkb} remove bm.lkvic',
        say('The hall was full - the Fixer cleared out a spare for you.', LOCK, PV), 'function bm:p84/lk/claim'])
    fn('p104/lk/count', ['scoreboard players operation #o2 bm.rng = @s bm.lko', 'scoreboard players set #cc bm.rng 0',
                         f'execute as {lkb} if score @s bm.lko = #o2 bm.rng run scoreboard players add #cc bm.rng 1', 'scoreboard players operation @s bm.lkc = #cc bm.rng'])
    # (as the bay to free: its things into the keeper's other bays where they fit, the rest to their Lost & Found)
    fn('p104/lk/evict', ['scoreboard players operation #vk bm.rng = @s bm.lko', 'scoreboard players operation #vb bm.rng = @s bm.lkn',
                         'execute store result storage bm:lk ev.pid int 1 run scoreboard players get #vk bm.rng', 'data modify storage bm:lk ev.items set value []'] +
       [f'execute if score #vb bm.rng matches {n} in bm:gutter run function bm:p104/lk/take{n}' for n, *_r in B_] +
       ['scoreboard players set @s bm.lko 0', 'scoreboard players set @s bm.lkday 0'] +
       [f'execute if score #vb bm.rng matches {n} in bm:gutter run function bm:p84/lk/unlock{n}' for n, *_r in B_] +
       # (into the keeper's other bays, slot by slot where there's room - then whatever's left is lost-and-found)
       [f'execute in bm:gutter as {lkb} if score @s bm.lko = #vk bm.rng run function bm:p104/lk/refit',
        'function bm:p104/lk/lost with storage bm:lk ev',
        'execute as @a if score @s bm.pid = #vk bm.rng run ' + say('The Locker Hall was full: the Fixer freed one of your bays for a newcomer. Its things went into your other '
                                                                   'bays - and anything that didn\'t fit waits for you as Lost & Found crates in the Locker Hall.', LOCK, PV)])
    for n, cells, _p in B_:
        fn(f'p104/lk/take{n}', [f'data modify storage bm:lk ev.items append from block {cx} {cy} {cz} Items[]' for cx, cy, cz, st in cells] +
           [f'data modify block {cx} {cy} {cz} Items set value []' for cx, cy, cz, st in cells])
        fn(f'p104/lk/fit{n}', [f'execute if data storage bm:lk ev.items[0] run function bm:p104/lk/fitc {{x:{cx},y:{cy},z:{cz}}}' for cx, cy, cz, st in cells])
    fn('p104/lk/refit', ['scoreboard players operation #fb bm.rng = @s bm.lkn'] +
       [f'execute if score #fb bm.rng matches {n} run function bm:p104/lk/fit{n}' for n, *_r in B_])
    # (one chest cell: its free slots take items until it's full or nothing's left)
    fn('p104/lk/fitc', ['scoreboard players set #sl bm.rng 0', '$data modify storage bm:lk ev.x set value $(x)', '$data modify storage bm:lk ev.y set value $(y)',
                        '$data modify storage bm:lk ev.z set value $(z)', 'function bm:p104/lk/fits'])
    fn('p104/lk/fits', ['execute unless data storage bm:lk ev.items[0] run return 0', 'execute if score #sl bm.rng matches 27.. run return 0',
                        'execute store result storage bm:lk ev.sl int 1 run scoreboard players get #sl bm.rng', 'scoreboard players add #sl bm.rng 1',
                        'function bm:p104/lk/fit1 with storage bm:lk ev', 'function bm:p104/lk/fits'])
    fn('p104/lk/fit1', ['$execute if data block $(x) $(y) $(z) Items[{Slot:$(sl)b}] run return 0',
                        'data modify storage bm:lk ev.one set from storage bm:lk ev.items[0]', 'execute store result storage bm:lk ev.one.Slot byte 1 run data get storage bm:lk ev.sl',
                        '$data modify block $(x) $(y) $(z) Items append from storage bm:lk ev.one', 'data remove storage bm:lk ev.items[0]'])
    fn('p104/lk/lost', ['execute unless data storage bm:lk ev.items[0] run return 0', '$data modify storage bm:lk lost.p$(pid) append from storage bm:lk ev.items[]',
                        'data modify storage bm:lk ev.items set value []'])
    # (the Lost & Found: handed over in the Locker Hall as crates of up to 27 stacks - The Haul's kind of crate)
    crate = {'id': 'minecraft:barrel', 'count': Int(1), 'components': {
        'minecraft:custom_name': T('Lost & Found', LOCK, bold=True), 'minecraft:custom_data': {'bm_haul': B(1)},
        'minecraft:lore': [T('Your things, from a locker the Fixer had to free.', 'gray'), T('Set it down and open it.', 'blue'),
                           T('Walk away and it folds up - into your pack if', 'gray'), T('anything is left in it.', 'gray')]}}
    second.append('execute as @a[scores={bm.pid=1..}] at @s if dimension bm:gutter if function bm:p84/lk/inside run function bm:p104/lf/check')
    fn('p104/lf/check', ['execute store result storage bm:lk lf.pid int 1 run scoreboard players get @s bm.pid', 'function bm:p104/lf/check2 with storage bm:lk lf'])
    fn('p104/lf/check2', ['$execute unless data storage bm:lk lost.p$(pid)[0] run return 0', '$data modify storage bm:lk lfx set from storage bm:lk lost.p$(pid)',
                          '$data remove storage bm:lk lost.p$(pid)', 'scoreboard players set #lfn bm.rng 0', 'function bm:p104/lf/crate',
                          tellraw('@s', PV + [T('Lost & Found: ', LOCK, bold=True), num('#lfn'), T(' crate(s) of your things, from a locker the Fixer had to free.', 'gray')]),
                          'playsound minecraft:block.barrel.open player @s ~ ~ ~ 1 1'])
    fn('p104/lf/crate', ['execute unless data storage bm:lk lfx[0] run return 0', 'scoreboard players add #lfn bm.rng 1',
                         'data modify storage bm:tmp haul.out set value []', 'scoreboard players set #sl bm.rng 0', 'function bm:p104/lf/conv',
                         f'summon minecraft:item ~ ~0.3 ~ {snbt({"Item": crate, "PickupDelay": Int(0), "Age": Int(-32768), "Tags": ["bm.lfnew"]})}',
                         'data modify entity @e[type=minecraft:item,tag=bm.lfnew,distance=..2,limit=1] Item.components."minecraft:container" set from storage bm:tmp haul.out',
                         'data modify entity @e[type=minecraft:item,tag=bm.lfnew,distance=..2,limit=1] Owner set from entity @s UUID',
                         'tag @e[type=minecraft:item,tag=bm.lfnew] remove bm.lfnew', 'function bm:p104/lf/crate'])
    fn('p104/lf/conv', ['execute unless data storage bm:lk lfx[0] run return 0', 'execute if score #sl bm.rng matches 27.. run return 0',
                        'data modify storage bm:tmp haul.e set value {}', 'execute store result storage bm:tmp haul.e.slot int 1 run scoreboard players get #sl bm.rng',
                        'data modify storage bm:tmp haul.e.item set from storage bm:lk lfx[0]', 'data remove storage bm:tmp haul.e.item.Slot',
                        'data modify storage bm:tmp haul.out append from storage bm:tmp haul.e', 'data remove storage bm:lk lfx[0]', 'scoreboard players add #sl bm.rng 1',
                        'function bm:p104/lf/conv'])
    fn('admin/lost_found', [tellraw('@s', PV + [T('Lost & Found is kept in storage bm:lk lost (by player id); it\'s handed over in the Locker Hall.', 'gray')])])

    G.FUNCS['tick'] += tick
    s_ = G.FUNCS['loop/second']
    s_[-1:-1] = second
