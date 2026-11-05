"""3.1: THE GUIDE - a little non-combat companion you switch on from the Black Market Handbook (guide_art.py: four forms).

Not a follower (no fights, no buffs, never in the follower count, the Raid Crew or the wheel): like the Pixel Creeper (phase256),
a little friend that comes along. The Handbook's "Guide ›" page: Guide on / off, and its FORM - the Wisp (a ball of warm light
on four little wings), the Rainbow Butterfly, the Suitcase (it walks and hops) or the Little Handbook (the Handbook itself,
awake). The choice is yours (bm.gdon, bm.gdf - scores: kept through death, logging out and other dimensions).

  THE BODY      one item display per part (guide_art's rig, 4-5 parts: rigfol's machinery - each part teleported to its joint
                every tick, its pose interpolated), on a MARKER (the anchor: nothing to hit, nothing that collides, nothing any
                mob targets, never Glowing). A second marker is where it wants to be: behind your right shoulder, floating at
                the form's HOVER height (the suitcase on the ground beside you).
  FOLLOWING     each tick the anchor eases toward that spot - quicker the further it's fallen behind - facing where it's going,
                and turned to look at you when it's caught up. Over 8 blocks behind, it pops back to you (a puff); over 16, or
                in another dimension, it's gone and comes back beside you a second later. Gone when you're dead, a spectator or
                logged out (and back when you are). One per player.
  MOVING        idle: a slow float bob (idle_a <-> idle_b, 40 ticks), now and then a blink (the Suitcase, the Book); while it
                follows, the move cycle (a faster flutter, the Suitcase's hop, the Book's cover flapping).
  RIGHT-CLICK   a small click box (an interaction, 0.5 x 0.5, at its body): it does a happy little twirl (happy -> happy_b ->
                idle) and your Handbook opens - exactly as using the Handbook does (sneak: Your settings). A hit on it does
                nothing at all (the attack is cleared).
Codes 7000-7006 (p276/act, each line menu-checked): 7000 "Guide ›" on the Handbook (menu 5660); on its page (menu 7000) 7001
on / off, 7002-7005 the forms, 7006 "« Handbook"; on the Partner Wheel (menu 3350) 7007 "Black Market Handbook" (open it), 7008
"Guide ›", 7009 "Take the Handbook back".
THE HANDBOOK ON THE WHEEL   hold it in your off hand and use the Partner Wheel: it goes on (its own flag, bm.pwhb - never one of
                the wheel's numbered partner slots); the wheel's menu then opens it, and takes it back (the same item, once)."""
from items import T
from nbt import snbt
import rigfol as RF
import phase28 as P28
import phase260 as P260
import guide_art as A

MENU = 7000
B_GUIDE, B_TOG, B_FORM0, B_BACK = 7000, 7001, 7002, 7006
B_WHB, B_WGD, B_WOUT = 7007, 7008, 7009                      # (on the Partner Wheel, menu 3350: the Handbook, Guide ›, take it back)
COL = '#e8c070'
NEAR_POP, LOST = 8, 16
FORMS = A.FORMS                                              # (wisp, butterfly, suitcase, book: bm.gdf 0..3)
FACE_PART = {'suitcase': 'body', 'book': 'cover'}
# where it wants to be, from you (rotated with you, yaw only): ^left ^up ^forward, in blocks
SPOT = {'wisp': (-0.75, A.HOVER['wisp'], -0.5), 'butterfly': (-0.8, A.HOVER['butterfly'], -0.45),
        'suitcase': (-0.9, 0.0, -0.35), 'book': (-0.75, A.HOVER['book'], -0.5)}
MOVE_P = {'wisp': 8, 'butterfly': 6, 'suitcase': 10, 'book': 12}             # (the move cycle's period, ticks)
TIPS = {'wisp': 'A ball of warm light on four little wings.', 'butterfly': 'A rainbow butterfly, bright as a sticker.',
        'suitcase': 'A little suitcase on stubby legs. It hops to keep up.', 'book': 'Your Handbook, awake - with a ribbon tail.'}


def rp(R):
    """the resource pack: every part of every form as a 3D model at display scale (fixed: as it stands)"""
    for r in A.RIGS.values():
        R.TEXTURE_MODS.append(r)
        for name, (tex, els) in r.models().items():
            R.HATS[name] = (tex, els)
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (r.PREFIX,)


def generate(G):
    fn, F = G.fn, G.FUNCS
    tick, second = F['tick'], F['loop/second']
    objs = ['bm.gdon', 'bm.gdf', 'bm.gdst', 'bm.gdt', 'bm.gdq']
    F['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    say = lambda comp: G.title('@s', 'actionbar', comp)
    click = 'playsound minecraft:ui.button.click player @s ~ ~ ~ 0.6 1.4'
    puff = 'particle minecraft:poof ~ ~0.3 ~ 0.15 0.15 0.15 0.01 6'
    OWNER = '@e[type=minecraft:player,tag=bm.gdo,limit=1]'
    TG = '@e[type=minecraft:marker,tag=bm.gds,tag=bm.gdtg,limit=1]'
    HIT = '@e[type=minecraft:interaction,tag=bm.gds,tag=bm.gdh,limit=1]'
    sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.gds,tag=bm.gdk_{p},limit=1]'
    G.wjson('bm/predicate/p276/blink.json', {'condition': 'minecraft:random_chance', 'chance': 0.4})

    # ---------------------------------------------------------------- who has one on (each second), and theirs only
    second += ['tag @a remove bm.hasgd',
               'execute as @e[type=minecraft:player,gamemode=!spectator,scores={bm.gdon=1}] run tag @s add bm.hasgd',
               'execute as @e[type=minecraft:marker,tag=bm.gd] at @s unless function bm:p276/owner_ok run function bm:p276/vanish',
               'execute as @e[tag=bm.gdx] at @s unless function bm:p276/has_anchor run kill @s',
               'execute as @e[type=minecraft:player,tag=bm.hasgd] unless score @s bm.pid matches 1.. run function bm:p21/pid',
               'execute as @e[type=minecraft:player,tag=bm.hasgd] at @s unless function bm:p276/mine run function bm:p276/spawn']
    fn('p276/owner_ok', ['scoreboard players operation #p bm.pay = @s bm.pid', 'scoreboard players operation #pf bm.pay = @s bm.gdf',
                         f'execute as @e[type=minecraft:player,tag=bm.hasgd,distance=..{LOST}] if score @s bm.pid = #p bm.pay '
                         'if score @s bm.gdf = #pf bm.pay run return 1', 'return 0'])
    fn('p276/has_anchor', ['scoreboard players operation #p bm.pay = @s bm.pid',
                           f'execute as @e[type=minecraft:marker,tag=bm.gd,distance=..{LOST + 8}] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    fn('p276/mine', ['scoreboard players operation #p bm.pay = @s bm.pid',
                     f'execute as @e[type=minecraft:marker,tag=bm.gd,distance=..{LOST}] if score @s bm.pid = #p bm.pay run return 1', 'return 0'])
    fn('p276/vanish', [puff, 'scoreboard players operation #p bm.pay = @s bm.pid',
                       f'execute as @e[tag=bm.gdx,distance=..{LOST + 8}] if score @s bm.pid = #p bm.pay run kill @s', 'kill @s'])
    fn('p276/spawn', ['execute unless score @s bm.gdf matches 0..3 run scoreboard players set @s bm.gdf 0'] +
       [f'execute if score @s bm.gdf matches {i} run return run function bm:p276/f{i}/spawn' for i in range(len(FORMS))])
    # (yours, gone now: switched off, or another form chosen)
    fn('p276/off_now', ['scoreboard players operation #p bm.pay = @s bm.pid',
                        f'execute as @e[type=minecraft:marker,tag=bm.gd] if score @s bm.pid = #p bm.pay at @s run function bm:p276/vanish'])

    # ---------------------------------------------------------------- each tick: follow, move, place
    tick += ['execute as @e[type=minecraft:marker,tag=bm.gd] at @s run function bm:p276/tick',
             'execute as @e[type=minecraft:interaction,tag=bm.gdh] if data entity @s interaction run function bm:p276/click',
             'execute as @e[type=minecraft:interaction,tag=bm.gdh] if data entity @s attack run data remove entity @s attack']
    fn('p276/tick', ['scoreboard players operation #p bm.pay = @s bm.pid',
                     f'execute as @e[type=minecraft:player,tag=bm.hasgd,distance=..{LOST + 8}] if score @s bm.pid = #p bm.pay run tag @s add bm.gdo',
                     f'execute unless entity {OWNER} run return 0',
                     f'execute as @e[tag=bm.gdx,distance=..{LOST + 8}] if score @s bm.pid = #p bm.pay run tag @s add bm.gds'] +
       [f'execute if score @s bm.gdf matches {i} run function bm:p276/f{i}/tick' for i in range(len(FORMS))] +
       [f'tag @e[tag=bm.gds,distance=..{LOST + 8}] remove bm.gds', 'tag @a remove bm.gdo'])
    # (how far behind it is: the further, the quicker it comes - and over NEAR_POP blocks, a pop to you)
    fn('p276/move', ['scoreboard players set #mv bm.rng 1',
                     f'execute unless entity {TG.replace("limit=1", f"distance=..{NEAR_POP},limit=1")} run return run function bm:p276/pop',
                     f'execute if entity {TG.replace("limit=1", "distance=2.5..,limit=1")} facing entity {TG} feet run return run tp @s ^ ^ ^0.55',
                     f'execute if entity {TG.replace("limit=1", "distance=1.2..,limit=1")} facing entity {TG} feet run return run tp @s ^ ^ ^0.28',
                     f'execute if entity {TG.replace("limit=1", "distance=0.6..,limit=1")} facing entity {TG} feet run return run tp @s ^ ^ ^0.14',
                     f'execute if entity {TG.replace("limit=1", "distance=0.25..,limit=1")} facing entity {TG} feet run return run tp @s ^ ^ ^0.06',
                     'scoreboard players set #mv bm.rng 0'])
    fn('p276/pop', [puff, f'tp @s {TG}', 'execute at @s run ' + puff, 'scoreboard players set #mv bm.rng 0'])
    fn('p276/click', ['scoreboard players operation #p bm.pay = @s bm.pid',
                      'execute as @e[type=minecraft:marker,tag=bm.gd] if score @s bm.pid = #p bm.pay at @s run function bm:p276/happy',
                      'execute on target run function bm:p260/hb/use', 'data remove entity @s interaction'])
    fn('p276/happy', ['scoreboard players set @s bm.gdst 2', 'scoreboard players set @s bm.gdt 0',
                      'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..10] ~ ~ ~ 0.6 1.6',
                      'particle minecraft:wax_off ~ ~0.35 ~ 0.25 0.2 0.25 0.5 6'])
    fn('p276/to_move', ['scoreboard players set @s bm.gdst 1', 'scoreboard players set @s bm.gdt 0', 'scoreboard players set @s bm.gdq 0'])
    fn('p276/to_idle', ['scoreboard players set @s bm.gdst 0', 'scoreboard players set @s bm.gdt 0'])

    for i, w in enumerate(FORMS):
        R = A.RIGS[w]; S = R.RIG_SCALE; pre = f'p276/f{i}'
        fp = FACE_PART.get(w)
        swap = (fp,) if fp else ()
        x, y, z = SPOT[w]
        used = {}

        def pz(name, dur):
            key = f'{name}_{dur}'
            if key not in used:
                fn(f'{pre}/pose/{key}', RF.pose(R, R.POSES[name], S, dur, sel, swap=swap)); used[key] = 1
            return f'function bm:{pre}/pose/{key}'
        tags = lambda p: ['bm.gdx', 'bm.gdp', f'bm.gdk_{p}', 'bm.gdnew']
        fn(f'{pre}/spawn', [f'execute rotated ~ 0 positioned ^{x} ^{y} ^{z} run function bm:{pre}/spawn_at'])
        fn(f'{pre}/spawn_at', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gd","bm.gdnew"]}',
                               'summon minecraft:marker ~ ~ ~ {Tags:["bm.gdx","bm.gdtg","bm.gdnew"]}',
                               'summon minecraft:interaction ~ ~ ~ {Tags:["bm.gdx","bm.gdh","bm.gdnew"],width:0.5f,height:0.5f,response:1b}'] +
           [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(R, p, tags(p), S, model=R.model_name(p))}' for p in R.PARTS if R._els[p]] +
           ['scoreboard players operation @e[tag=bm.gdnew,distance=..0.1] bm.pid = @s bm.pid',
            f'scoreboard players set @e[type=minecraft:marker,tag=bm.gd,tag=bm.gdnew,distance=..0.1] bm.gdf {i}',
            'scoreboard players set @e[type=minecraft:marker,tag=bm.gd,tag=bm.gdnew,distance=..0.1] bm.gdst 0',
            'scoreboard players set @e[type=minecraft:marker,tag=bm.gd,tag=bm.gdnew,distance=..0.1] bm.gdt 0',
            'execute as @e[type=minecraft:marker,tag=bm.gd,tag=bm.gdnew,distance=..0.1] at @s facing entity @p[distance=..3] eyes run tp @s ~ ~ ~ ~ 0',
            'tag @e[tag=bm.gdnew,distance=..0.1] remove bm.gdnew', puff,
            'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..12] ~ ~ ~ 0.5 1.9'])
        # (as the anchor, its own tagged bm.gds and its player bm.gdo)
        fn(f'{pre}/tick', [f'execute as {OWNER} at @s rotated ~ 0 positioned ^{x} ^{y} ^{z} run tp {TG} ~ ~ ~',
                           'function bm:p276/move',
                           f'execute if score #mv bm.rng matches 1 at @s facing entity {TG} feet run tp @s ~ ~ ~ ~ 0',
                           f'execute if score #mv bm.rng matches 0 at @s facing entity {OWNER} eyes run tp @s ~ ~ ~ ~ 0',
                           f'function bm:{pre}/anim',
                           f'execute at @s rotated as @s rotated ~ 0 run function bm:{pre}/place',
                           f'execute at @s run tp {HIT} ~ ~ ~'])
        fn(f'{pre}/place', RF.place(R, S / 16, sel))
        P = MOVE_P[w]
        fn(f'{pre}/anim', ['scoreboard players add @s bm.gdt 1',
                           f'execute if score @s bm.gdst matches 2 run return run function bm:{pre}/happy',
                           'execute if score #mv bm.rng matches 1 if score @s bm.gdst matches 0 run function bm:p276/to_move',
                           'execute if score #mv bm.rng matches 1 run scoreboard players set @s bm.gdq 0',
                           'execute if score #mv bm.rng matches 0 if score @s bm.gdst matches 1 run scoreboard players add @s bm.gdq 1',
                           'execute if score @s bm.gdq matches 6.. if score @s bm.gdst matches 1 run function bm:p276/to_idle',
                           'scoreboard players operation #f bm.rng = @s bm.gdt',
                           f'execute if score @s bm.gdst matches 0 run return run function bm:{pre}/idle',
                           f'function bm:{pre}/walk'])
        idle = ['scoreboard players operation #f bm.rng %= #40 bm.rng',
                'execute if score #f bm.rng matches 1 run ' + pz('idle_a', 20),
                'execute if score #f bm.rng matches 21 run ' + pz('idle_b', 20)]
        if fp:
            base, blink = f'bm:{R.model_name(fp)}', f'bm:{R.model_name(fp, {"_face": "blink"})}'
            idle += [f'execute if score #f bm.rng matches 31 if predicate bm:p276/blink as {sel(fp)} run data modify entity @s item.components."minecraft:item_model" set value "{blink}"',
                     f'execute if score #f bm.rng matches 35 as {sel(fp)} run data modify entity @s item.components."minecraft:item_model" set value "{base}"']
        fn(f'{pre}/idle', idle)
        fn(f'{pre}/walk', [f'scoreboard players operation #f bm.rng %= #{P} bm.rng',
                           'execute if score #f bm.rng matches 1 run ' + pz('move_0', P // 2),
                           f'execute if score #f bm.rng matches {P // 2 + 1} run ' + pz('move_1', P // 2)])
        fn(f'{pre}/happy', ['execute if score @s bm.gdt matches 1 run ' + pz('happy', 4),
                            'execute if score @s bm.gdt matches 7 run ' + pz('happy_b', 6),
                            'execute if score @s bm.gdt matches 14 run ' + pz('idle_a', 8),
                            'execute if score @s bm.gdt matches 22.. run function bm:p276/to_idle'])
    for P in sorted(set(MOVE_P.values()) | {40}):
        line = f'scoreboard players set #{P} bm.rng {P}'
        if line not in F['load']: F['load'].insert(len(F['load']) - 1, line)

    # ---------------------------------------------------------------- the Handbook's Guide page
    st = lambda key, comp: f'data modify storage bm:ui gd.r_{key} set value {snbt(comp)}'
    state = ['data remove storage bm:ui gd', 'execute unless score @s bm.gdf matches 0..3 run scoreboard players set @s bm.gdf 0',
             st('on', T('off', '#ff8a8a', bold=True)), 'execute if score @s bm.gdon matches 1 run ' + st('on', T('on', 'white', bold=True))]
    for i in range(len(FORMS)):
        state += [st(f'f{i}', T('○ ', 'dark_gray')), f'execute if score @s bm.gdf matches {i} run ' + st(f'f{i}', T('● ', COL))]
    state.append(f'scoreboard players set @s bm.menu {MENU}')
    d = P28.multi([T('THE GUIDE', COL, bold=True), T('  ·  a little friend who comes along', 'gray')],
                  [P28.body([T('A little companion that floats along beside you. It doesn\'t fight, gives no buffs and isn\'t one of '
                               'your followers. ', 'gray'), T('Right-click it: your Handbook.', 'white')], 300)],
                  [P28.btn([T('Guide: ', 'gray'), '@@RAW:r_on@@'], B_TOG, width=150, tooltip=T('Have your guide come along - or not.', 'gray')),
                   P28.btn([T('« Handbook', 'gray')], B_BACK, width=150)] +
                  [P28.btn(['@@RAW:r_f' + str(i) + '@@', T(A.NAMES[w], 'white')], B_FORM0 + i, width=150, tooltip=T(TIPS[w], 'gray'))
                   for i, w in enumerate(FORMS)], columns=2, exit_label='Close')
    fn('p276/dlg', [f'$dialog show @s {P28.inline(d)}'])
    fn('p276/show', state + ['function bm:p276/dlg with storage bm:ui gd'])
    fn('p276/open', ['function bm:p276/show', 'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 0.8 1.2'])
    fn('p276/now', ['tag @s add bm.hasgd', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                    'execute if entity @s[gamemode=!spectator] at @s unless function bm:p276/mine run function bm:p276/spawn'])
    fn('p276/toggle', [click, 'execute if score @s bm.gdon matches 1 run return run function bm:p276/t_off', 'scoreboard players set @s bm.gdon 1',
                       'function bm:p276/now', say([T('Guide: ', COL, bold=True), T('on', 'green')]), 'function bm:p276/show'])
    fn('p276/t_off', ['scoreboard players set @s bm.gdon 0', 'tag @s remove bm.hasgd', 'function bm:p276/off_now',
                      say([T('Guide: ', COL, bold=True), T('off', 'red')]), 'function bm:p276/show'])
    for i, w in enumerate(FORMS):
        fn(f'p276/form{i}', [click, f'scoreboard players set @s bm.gdf {i}', 'scoreboard players set @s bm.gdon 1', 'function bm:p276/off_now',
                             'function bm:p276/now', say([T('Guide: ', COL, bold=True), T(A.NAMES[w], 'white')]), 'function bm:p276/show'])
    act = [f'execute if score #act bm.pay matches {B_GUIDE} if score @s bm.menu matches {P260.HB} run return run function bm:p276/open',
           f'execute if score #act bm.pay matches {B_TOG} if score @s bm.menu matches {MENU} run return run function bm:p276/toggle',
           f'execute if score #act bm.pay matches {B_BACK} if score @s bm.menu matches {MENU} run return run function bm:p260/hb/open'] + \
          [f'execute if score #act bm.pay matches {B_FORM0 + i} if score @s bm.menu matches {MENU} run return run function bm:p276/form{i}' for i in range(len(FORMS))]
    fn('p276/act', act + ['function bm:p28/stale'])
    F['p28/act'].append(f'execute if score #act bm.pay matches {B_GUIDE}..{B_WOUT} run return run function bm:p276/act')
    # (the Handbook's front page: a "Guide ›" button after its pages)
    gb = snbt(P28.btn([T('✦ ', COL), T('Guide', 'white'), T(' ›', 'gray')], B_GUIDE, width=150,
                      tooltip=T('A little friend who comes along: a wisp, a butterfly, a suitcase or a book.', 'gray')))
    L = F['p260/hb/main_dlg']; n = 0
    for j, l in enumerate(L):
        sp = P260.actions(l)
        if sp: L[j] = P260.set_actions(l, sp, sp[2] + [gb]); n += 1
    assert n == 1, n
    # ---------------------------------------------------------------- THE HANDBOOK ON THE PARTNER WHEEL (one less thing to carry)
    # Not a numbered slot (phase179's SLOTS save partners by position): its own flag, bm.pwhb, and the item itself kept as it was
    # (storage bm:pw p<pid>.hb) - put on from the off hand as a partner's item is, taken back from the wheel's menu (given back
    # once: the stored item, or a fresh one if the store is gone); dying keeps it with the wheel (a score). While you carry the
    # wheel with it on, you're tagged bm.pw_hb (as bm.pw_<partner> for a partner's item).
    import phase179 as P179
    PRE = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    holds = f'*[minecraft:custom_data~{{bm:"{P260.ITEM}"}}]'
    F['load'][-1:-1] = ['scoreboard objectives add bm.pwhb dummy']
    G.OBJECTIVES.append('bm.pwhb')
    second += ['tag @a remove bm.pw_hb', 'tag @a[tag=bm.pwc,scores={bm.pwhb=1}] add bm.pw_hb']
    use = F['p179/w/use']
    use.insert(1, f'execute if items entity @s weapon.offhand {holds} run return run function bm:p276/hb_add')
    fn('p276/hb_add', ['execute if score @s bm.pwhb matches 1 run return run ' + say(T('Your Handbook is on your wheel already.', 'gray')),
                       'function bm:p179/w/pid', 'function bm:p276/hb_addm with storage bm:tmp pw',
                       'item replace entity @s weapon.offhand with minecraft:air', 'scoreboard players set @s bm.pwhb 1', 'tag @s add bm.pw_hb',
                       'playsound minecraft:block.enchantment_table.use player @s ~ ~ ~ 0.6 1.6', 'particle minecraft:enchant ~ ~1.2 ~ 0.3 0.4 0.3 0.6 20',
                       G.tellraw('@s', PRE + [T('Black Market Handbook', COL, bold=True), T(' goes on your Partner Wheel. ', 'gray'),
                                              T('(Use the wheel: it has a Handbook button.)', 'dark_gray')])])
    fn('p276/hb_addm', ['$data modify storage bm:pw p$(pid).hb set from entity @s equipment.offhand'])
    fn('p276/hb_out', ['execute unless score @s bm.pwhb matches 1 run return run function bm:p28/stale',
                       'function bm:p179/w/pid', 'function bm:p276/hb_outm with storage bm:tmp pw', 'scoreboard players set @s bm.pwhb 0',
                       'tag @s remove bm.pw_hb', 'playsound minecraft:item.armor.equip_chain player @s ~ ~ ~ 0.6 1.4',
                       G.tellraw('@s', PRE + [T('Black Market Handbook', COL, bold=True), T(' comes off your Partner Wheel.', 'gray')]),
                       'function bm:p179/w/open'])
    fn('p276/hb_outm', ['$execute unless data storage bm:pw p$(pid).hb run return run ' + G.give(P260.ITEM),
                        'summon minecraft:item ~ ~0.4 ~ {Tags:["bm.pwout"],PickupDelay:0s,Item:{id:"minecraft:paper",count:1}}',
                        '$data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Item set from storage bm:pw p$(pid).hb',
                        'data modify entity @e[type=minecraft:item,tag=bm.pwout,limit=1] Owner set from entity @s UUID',
                        'tag @e[type=minecraft:item,tag=bm.pwout] remove bm.pwout', '$data remove storage bm:pw p$(pid).hb'])
    fn('p276/hb_open', ['execute unless score @s bm.pwhb matches 1 run return run function bm:p28/stale', 'dialog clear @s', 'function bm:p260/hb/open'])
    # (its row on the wheel - after the partners': the Handbook, Guide ›, take it back; without it, Guide › beside your settings)
    icon = {'type': 'object', 'object': 'atlas', 'atlas': 'minecraft:items', 'sprite': 'minecraft:item/book', 'fallback': {'text': '◆', 'color': COL}}
    b_hb = P28.btn([icon, T(' Black Market Handbook', COL, bold=True)], B_WHB, tooltip=T('Open your Handbook (it rides on your wheel)', 'gray'))
    b_gd = P28.btn([T('✦ ', COL), T('Guide', 'white'), T(' ›', 'gray')], B_WGD, tooltip=T('Your guide: on or off, and how it looks', 'gray'))
    b_out = P28.btn(T('Take the Handbook back', 'gray'), B_WOUT, tooltip=T('The Black Market Handbook comes off the wheel', 'gray'))
    op = F['p179/w/open']
    k = op.index('function bm:p179/w/top')
    op[k:k] = [f'execute if score @s bm.pwhb matches 1 run data modify storage bm:tmp pw.acts append value {snbt(b)}' for b in (b_hb, b_gd, b_out)]
    k = op.index('function bm:p179/w/show with storage bm:tmp pw')
    op.insert(k, f'execute unless score @s bm.pwhb matches 1 run data modify storage bm:tmp pw.acts append value {snbt(b_gd)}')
    wact = [f'execute if score #act bm.pay matches {B_WHB} if score @s bm.menu matches {P179.WMENU} run return run function bm:p276/hb_open',
            f'execute if score #act bm.pay matches {B_WGD} if score @s bm.menu matches {P179.WMENU} run return run function bm:p276/open',
            f'execute if score #act bm.pay matches {B_WOUT} if score @s bm.menu matches {P179.WMENU} run return run function bm:p276/hb_out']
    F['p276/act'][-1:-1] = wact
    F['admin/uninstall'][0:0] = ['kill @e[tag=bm.gdx]', 'kill @e[type=minecraft:marker,tag=bm.gd]', 'tag @a remove bm.hasgd', 'tag @a remove bm.gdo',
                                 'tag @a remove bm.pw_hb']
    return f'{len(FORMS)} forms, codes {B_GUIDE}-{B_WOUT}'
