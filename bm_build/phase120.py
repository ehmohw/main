"""2.74: KNOCKED OUT, NOT KNOCKED BACK - and a few fixes.

THE CHECKPOINT  every room your crew clears moves your respawn to its exit door. Knocked out, you come to right there - a
                safe, cleared spot - and walk straight back into the action. (Before: the den, then the emerald plate back.)
                The void hauls you to the same spot.
YOUR POCKETS    a heist keeps your inventory just as you had it: the same slots, the same armour, the same XP. Nothing
                spills on the floor, and no fresh kit - what you used stays used. (A try is still lost, the alarm still rises.)
THE KIT         32 food (was 16) and 4 paperweights (was 3): phase72 / phase84 / phase104.
LIGHTS OUT      darkness only while the heist is on and you're out in it - never in the den or the Locker Hall, and not
                once the vault has paid out. (Before: from the moment you planned it until you went home.)
THE DEN         Goldtooth, the Recruiter, the Tailor (and Whiskers in the Rats' Rest) show their name once: the short-range
                trader nameplate, not the always-on tag as well.
THE DEN         no loose carpet on the floor by the office: the old loot pile there is cleared top-down, so its carpet no
                longer pops off as an item every time a den is built.
THE SANCTUARY   the shrines glow only while someone's in the room, and not through every wall from across the heist.
ALIEN HEISTS    (an Alien or Invasion heist) a win has a 5% chance of a Vorn Skiff part in your haul.
GLASS CANNON    (the modifier that halves your health - not the difficulty) now starts at BEGIN, says so when it does, and
                lifts once the vault pays out. (Before: from the moment you planned the heist, without a word.)
THE GUTTER BANK keeps Gutter Medallions and Gutter Trophies as they are: deposit them, see them in your account, take them
                back out. (Before: melted into a coin balance you couldn't see them in.) They still count as 16 and 128
                towards anything the bank pays for - spending breaks them into change only as needed.
SPEED RUN       with the alarm off, running out of time no longer brings a lockdown's guards: TIME'S UP - the haul
                shrinks, as a lockdown's would, and that's all. (It rang the alarm to 100 and sent patrols every 15 seconds -
                with the alarm switched off.) And patrols - alarm on - stop once the vault is open.
THE TEMPLE      (the push-block puzzle) its stones glow when it's solved - for 10 seconds now, not through the walls for good.
THE SKY ISLES   kinder to fall off: while the guards are out, the crew stands steadier against wind (the breezes' gusts
                push you a little over a third as far), and fewer breezes come - one from Tier III, two at Tier V (was three).
"""
from items import T
from nbt import snbt
import phase35 as P35
import phase72 as P72
import phase84 as P84
import phase28 as P28
import phase80 as P80

GOLD = '#ffcf40'
STAGE = P72.STAGE                       # (bm:gutter, kept loaded - a staging barrel, emptied after every use)
EQ = [('head', 'armor.head'), ('chest', 'armor.chest'), ('legs', 'armor.legs'), ('feet', 'armor.feet'), ('offhand', 'weapon.offhand')]
SNAP_EVERY = 5                          # ticks between snapshots (every tick at half health or less)
SKIFF_CHANCE = 5                        # % a won alien heist puts a Skiff part in the haul


def generate(G):
    fn, title, tellraw, wjson = G.fn, G.title, G.tellraw, G.wjson
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    objs = ['bm.kst']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    gutter = lambda c: f'execute in bm:gutter run {c}'
    pid = ['data modify storage bm:keep k set value {}', 'execute store result storage bm:keep k.n int 1 run scoreboard players get @s bm.pid']

    # ================================================================== THE CHECKPOINT: respawn where the crew last cleared the way
    # (every second, while a heist is on: each raider's spawn point is their crew's checkpoint - the exit door of the last room
    #  cleared, or the den before the first)
    second[-1:-1] = ['execute in bm:gutter as @e[type=minecraft:marker,tag=bm.gvcp,distance=0..] at @s run function bm:p120/cp_spawn']
    fn('p120/cp_spawn', ['scoreboard players operation #gi bm.rng = @s bm.gvi', 'scoreboard players set #st bm.rng 0',
                         'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng store result score #st bm.rng run scoreboard players get @s bm.gvst',
                         'execute unless score #st bm.rng matches 2..3 run return 0',
                         'execute as @a[tag=bm.gvp,tag=!bm.gvdead] if score @s bm.gvi = #gi bm.rng run spawnpoint @s ~ ~ ~ -90 0'])
    fn('p120/to_cp', ['scoreboard players operation #gi bm.rng = @s bm.gvi',
                      'execute as @e[type=minecraft:marker,tag=bm.gvcp] if score @s bm.gvi = #gi bm.rng run tag @s add bm.gvcpme',
                      'execute if entity @e[type=minecraft:marker,tag=bm.gvcpme] run tp @s @e[type=minecraft:marker,tag=bm.gvcpme,limit=1]',
                      'tag @e[type=minecraft:marker,tag=bm.gvcpme] remove bm.gvcpme'])
    # (the Rats' Rest no longer holds your spawn - every room after it moves it on)
    ra = G.FUNCS['p76/r/rest/arrive']
    ra[:] = [l for l in ra if 'run spawnpoint @s' not in l]
    ra[:] = [l.replace('If you\'re knocked out from here on, you wake by its fire.', 'Sit by the fire a while - it mends what the vault took.') for l in ra]
    ri = G.FUNCS['p76/r/rest/init']
    ri[:] = [l.replace('Knocked out after this? You\'ll wake here.', 'It mends what the vault took.') for l in ri]

    # ================================================================== YOUR POCKETS: a snapshot, kept a few ticks fresh
    tick.append('execute as @e[type=minecraft:player,tag=bm.gvp,tag=!bm.gvdead] run function bm:p120/snap_tick')
    fn('p120/snap_tick', ['scoreboard players add @s bm.kst 1', f'execute if score @s bm.hp matches ..10 run scoreboard players set @s bm.kst {SNAP_EVERY}',
                          f'execute if score @s bm.kst matches {SNAP_EVERY}.. run function bm:p120/snap'])
    fn('p120/snap', ['scoreboard players set @s bm.kst 0'] + pid + ['function bm:p120/snap2 with storage bm:keep k'])
    fn('p120/snap2', ['$data remove storage bm:keep p$(n)',
                      '$data modify storage bm:keep p$(n).inv set from entity @s Inventory',
                      '$data modify storage bm:keep p$(n).eq set from entity @s equipment',
                      '$execute store result storage bm:keep p$(n).xl int 1 run xp query @s levels',
                      '$execute store result storage bm:keep p$(n).xp int 1 run xp query @s points'])
    # (knocked out for real: what just spilled - the drops and the XP - is swept up; the snapshot comes back on waking)
    G.FUNCS['p70/died'].append('execute if entity @s[tag=bm.gvp] run function bm:p120/died')
    fn('p120/died', ['tag @s add bm.gvreal', 'tag @s remove bm.gvkeep'] + pid +
       ['scoreboard players set #has bm.rng 0', 'function bm:p120/has with storage bm:keep k',
        'execute if score #has bm.rng matches 0 run return 0',
        'tag @s add bm.gvkeep', 'scoreboard players operation #kdp bm.rng = @s bm.pid',
        'execute as @e[type=minecraft:item,tag=bm.kdi] if score @s bm.kdo = #kdp bm.rng run function bm:p120/spilt',
        'execute if data storage bm:gv kd.dim run function bm:p120/orbs with storage bm:gv kd'])
    fn('p120/has', ['$execute store success score #has bm.rng if data storage bm:keep p$(n).inv'])
    fn('p120/spilt', ['execute store result score #age bm.rng run data get entity @s Age', f'execute if score #age bm.rng matches ..{SNAP_EVERY + 1} run kill @s'])
    fn('p120/orbs', ['$execute in $(dim) positioned $(x).5 $(y) $(z).5 as @e[type=minecraft:experience_orb,distance=..5] run function bm:p120/spilt'])
    # (waking: every slot as it was, armour and off hand too, and the XP)
    fn('p120/restore', pid + ['function bm:p120/load with storage bm:keep k', 'function bm:p120/put'] +
       sum(([gutter(f'data modify block {STAGE} Items set value []'),
             f'execute if data storage bm:keep cur.eq.{k} in bm:gutter run data modify block {STAGE} Items append from storage bm:keep cur.eq.{k}',
             f'execute if data storage bm:keep cur.eq.{k} in bm:gutter run data modify block {STAGE} Items[0].Slot set value 0b',
             f'execute if data storage bm:keep cur.eq.{k} in bm:gutter run item replace entity @s {sl} from block {STAGE} container.0'] for k, sl in EQ), []) +
       ['execute if data storage bm:keep cur.xl run function bm:p120/xp with storage bm:keep cur',
        gutter(f'data modify block {STAGE} Items set value []'), 'data remove storage bm:keep cur',
        'tag @s remove bm.gvkeep', 'tag @s add bm.gvkept'])
    fn('p120/load', ['$data modify storage bm:keep cur set from storage bm:keep p$(n)'])
    fn('p120/put', ['execute unless data storage bm:keep cur.inv[0] run return 0',
                    'data modify storage bm:keep it set from storage bm:keep cur.inv[0]', 'data remove storage bm:keep cur.inv[0]',
                    'execute store result storage bm:keep a.s int 1 run data get storage bm:keep it.Slot', 'data modify storage bm:keep it.Slot set value 0b',
                    gutter(f'data modify block {STAGE} Items set value []'), gutter(f'data modify block {STAGE} Items append from storage bm:keep it'),
                    'function bm:p120/put2 with storage bm:keep a', 'function bm:p120/put'])
    fn('p120/put2', [f'$execute in bm:gutter run item replace entity @s container.$(s) from block {STAGE} container.0'])
    fn('p120/xp', ['$xp set @s $(xl) levels', '$xp set @s $(xp) points'])
    # (leaving the heist forgets it)
    G.FUNCS['p70/unraid'][0:0] = ['execute if entity @s[tag=bm.gvkeep] run function bm:p120/restore', 'tag @s remove bm.gvkept', 'tag @s remove bm.gvreal'] + \
                                 pid + ['function bm:p120/forget with storage bm:keep k']
    fn('p120/forget', ['$data remove storage bm:keep p$(n)'])

    # ================================================================== WAKING: at the checkpoint, at once, pockets as they were
    rw = G.FUNCS['p70/revive_wait']
    rw[:] = [l.replace('matches 30..', 'matches 1..') for l in rw]
    # (only once they're truly back: a player's health score isn't updated as they die, so it can't tell; @e never sees the dead)
    k = tick.index('execute as @a[tag=bm.gvdead,scores={bm.hp=1..}] run function bm:p70/revive_wait')
    tick[k] = 'execute as @e[type=minecraft:player,tag=bm.gvdead] run function bm:p70/revive_wait'
    rev = G.FUNCS['p70/revive']
    k = next(i for i, l in enumerate(rev) if ' in bm:gutter run tp @s 3.5 68 ' in l)
    while ' in bm:gutter run tp @s 3.5 68 ' in rev[k]:
        k += 1
    rev.insert(k, 'function bm:p120/to_cp')                  # (the den stays the fallback, should a checkpoint ever be missing)
    k = rev.index('execute if score @s bm.gvrole matches 1.. run function bm:p72/kit/reissue')
    rev[k:k + 1] = ['execute unless entity @s[tag=bm.gvkeep] if entity @s[tag=bm.gvreal] if score @s bm.gvrole matches 1.. run function bm:p72/kit/reissue',
                    'execute if entity @s[tag=bm.gvkeep] run function bm:p120/restore']
    k = rev.index('function bm:p104/ko_items')
    rev[k:k + 1] = ['execute unless entity @s[tag=bm.gvkept] if entity @s[tag=bm.gvreal] run function bm:p104/ko_items', 'tag @s remove bm.gvkept', 'tag @s remove bm.gvreal']
    k = next(i for i, l in enumerate(rev) if l.startswith('tellraw @s') and 'drags you back to the den' in l)
    rev[k] = tellraw('@s', P + [T('Knocked out! ', 'red', bold=True), T('You come to where your crew last cleared the way - everything you carried, just as it was.', 'gray')])
    vk = G.FUNCS['p112/void_ko']
    vk[:] = [l.replace('Into the void - the gang hauls you back to the den.', 'Into the void - the gang hauls you back to the last room you cleared.') for l in vk]

    # ================================================================== LIGHTS OUT: only out on the heist
    ins = G.FUNCS['p70/inst_sec']
    k = next(i for i, l in enumerate(ins) if 'if function bm:p70/mod1 run effect give @a[tag=bm.gvme] minecraft:darkness' in l)
    ins[k] = 'execute if function bm:p70/mod1 if score @s bm.gvst matches 2..3 run function bm:p120/lights_out'
    fn('p120/lights_out', ['execute as @e[type=minecraft:marker,tag=bm.gvr_lobby] if score @s bm.gvi = #gi bm.rng at @s positioned ~-12.5 ~-4 ~-12.5 run tag @a[tag=bm.gvme,dx=24,dy=24,dz=24] add bm.gvsafe',
                           f'execute in bm:gutter positioned {P84.HX} {P84.HY - 3} {P84.HZ} run tag @a[tag=bm.gvme,dx=15,dy=12,dz=15] add bm.gvsafe',
                           'effect give @a[tag=bm.gvme,tag=!bm.gvsafe] minecraft:darkness 3 0 true',
                           'tag @a[tag=bm.gvsafe] remove bm.gvsafe'])

    # ================================================================== THE DEN: one name each
    for f_, tags in (('p70/r/lobby/init', ('bm.gvgt', 'bm.gvrec', 'bm.gvtail')), ('p76/r/rest/init', ('bm.gvprop',))):
        L = G.FUNCS[f_]
        for i, l in enumerate(L):
            if l.startswith('summon minecraft:villager') and any(f'"{t}"' in l for t in tags) and '"bm.npc"' in l:
                assert 'CustomNameVisible:1b' in l, l[:80]
                L[i] = l.replace('CustomNameVisible:1b', 'CustomNameVisible:0b')
    # (the old loot pile in front of the office: cleared top-down - its carpet first - so nothing pops off as an item)
    li = G.FUNCS['p70/r/lobby/init']
    k = li.index('fill ~9 ~ ~-9 ~10 ~1 ~-9 minecraft:air')
    li[k:k + 1] = ['fill ~9 ~1 ~-9 ~10 ~1 ~-9 minecraft:air', 'fill ~9 ~ ~-9 ~10 ~ ~-9 minecraft:air',
                   'execute positioned ~9.5 ~1 ~-8.5 run kill @e[type=minecraft:item,distance=..3]']
    # (and those already standing)
    second[-1:-1] = ['execute in bm:gutter as @e[type=minecraft:villager,tag=bm.npc,tag=!bm.cnv0,distance=0..] run function bm:p120/one_name']
    fn('p120/one_name', ['data merge entity @s {CustomNameVisible:0b}', 'tag @s add bm.cnv0'])

    # ================================================================== THE SANCTUARY: the shrines glow for whoever's in the room
    si = G.FUNCS['p90/sanctum/init']
    n = 0
    for i, l in enumerate(si):
        if l.startswith('summon minecraft:item_display') and '"bm.gvshd"' in l:
            si[i] = l.replace('Glowing:1b', 'Glowing:0b,view_range:0.4f'); n += 1
    assert n == 3, n
    G.FUNCS['p90/sanctum/tick'] += [
        'execute if score #q bm.rng matches 0 store result score #near bm.rng if entity @a[tag=bm.gvp,distance=..12]',
        'execute if score #q bm.rng matches 0 if score #near bm.rng matches 1.. as @e[type=minecraft:item_display,tag=bm.gvshd,distance=..12] run data merge entity @s[type=minecraft:item_display] {Glowing:1b,view_range:0.4f}',
        'execute if score #q bm.rng matches 0 if score #near bm.rng matches 0 as @e[type=minecraft:item_display,tag=bm.gvshd,distance=..12] run data merge entity @s[type=minecraft:item_display] {Glowing:0b,view_range:0.4f}']

    # ================================================================== GLASS CANNON: from BEGIN to the payout, and it says so
    gc = G.FUNCS['p70/glass_check']
    k = next(i for i, l in enumerate(gc) if 'if function bm:p70/mod16 run scoreboard players set #glass bm.rng 1' in l)
    gc[k] = gc[k].replace('if function bm:p70/mod16 run', 'if function bm:p70/mod16 if score @s bm.gvst matches 2..3 run')
    gc += ['execute if score #glass bm.rng matches 1 unless entity @s[tag=bm.gvglass] run function bm:p120/glass_on',
           'execute if score #glass bm.rng matches 0 run tag @s remove bm.gvglass']
    fn('p120/glass_on', ['tag @s add bm.gvglass', 'title @s times 5 50 15', title('@s', 'title', T('GLASS CANNON', '#ff5a8a', bold=True)),
                         title('@s', 'subtitle', T('half your health - and you hit harder', 'gray')),
                         tellraw('@s', P + [T('Glass Cannon: ', '#ff5a8a', bold=True), T('this heist halves your health and makes you hit harder, until the vault pays out. ', 'gray'),
                                            T('(A modifier - not the difficulty.)', 'dark_gray')])])
    G.FUNCS['p70/unraid'].append('tag @s remove bm.gvglass')

    # ================================================================== THE GUTTER BANK: Medallions and Trophies, kept as they are
    # (the account's worth stays in bm.gbc, as everything that pays from the bank expects; bm.gbm / bm.gbt say how much of it is
    #  held as Medallions (16) and Trophies (128). Spending that eats into them breaks them - Medallions first - into change)
    bobjs = ['bm.gbm', 'bm.gbt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in bobjs]
    G.OBJECTIVES += bobjs
    hold = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    MC, GOLD_, GUT_M, TRO = P80.MENU_CODE, P80.GOLD, P80.GUT_M, '#ffd870'
    PAGE = MC + 70                                            # the Medallions & Trophies page; 71-74 its takes
    G.FUNCS['p80/init_me'] += [f'execute unless score @s {o} matches 0.. run scoreboard players set @s {o} 0' for o in bobjs] + ['function bm:p120/bk_norm']
    fn('p120/bk_norm', ['scoreboard players set #bkk bm.rng 128', 'scoreboard players operation #bkv bm.rng = @s bm.gbt', 'scoreboard players operation #bkv bm.rng *= #bkk bm.rng',
                        'scoreboard players set #bkk bm.rng 16', 'scoreboard players operation #bkw bm.rng = @s bm.gbm', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng',
                        'scoreboard players operation #bkv bm.rng += #bkw bm.rng', 'execute if score #bkv bm.rng > @s bm.gbc run function bm:p120/bk_break'])
    fn('p120/bk_break', ['execute if score @s bm.gbm matches 1.. run return run function bm:p120/bk_brm',
                         'execute if score @s bm.gbt matches 1.. run return run function bm:p120/bk_brt'])
    fn('p120/bk_brm', ['scoreboard players remove @s bm.gbm 1', 'scoreboard players remove #bkv bm.rng 16', 'execute if score #bkv bm.rng > @s bm.gbc run function bm:p120/bk_break'])
    fn('p120/bk_brt', ['scoreboard players remove @s bm.gbt 1', 'scoreboard players add @s bm.gbm 8', 'function bm:p120/bk_break'])
    # (#bkl = loose coins: the account less its Medallions and Trophies)
    fn('p120/bk_loose', ['function bm:p80/init_me', 'scoreboard players operation #bkl bm.rng = @s bm.gbc', 'scoreboard players operation #bkl bm.rng -= #bkv bm.rng'])
    # deposits: the pieces counted as pieces (the old lines still add their worth)
    dep = G.FUNCS['p80/bank_deposit']
    dep[1:1] = [f'execute store result score #bkd bm.rng run clear @s {hold("gutter_medallion")} 0', 'scoreboard players operation @s bm.gbm += #bkd bm.rng',
                f'execute store result score #bkd bm.rng run clear @s {hold("gutter_trophy")} 0', 'scoreboard players operation @s bm.gbt += #bkd bm.rng']
    G.FUNCS['p102/to_bank'][0:0] = ['execute if score #w bm.rng matches 16 run scoreboard players operation @s bm.gbm += #n bm.rng',
                                    'execute if score #w bm.rng matches 128 run scoreboard players operation @s bm.gbt += #n bm.rng']
    # taking coins out takes loose coins - never a Medallion or Trophy melted down
    for f_ in ('p80/bank_take16', 'p80/bank_take64'):
        L = G.FUNCS[f_]; k = L.index('scoreboard players operation #c bm.rng < @s bm.gbc')
        L[k:k + 1] = ['function bm:p120/bk_loose', 'scoreboard players operation #c bm.rng < #bkl bm.rng']
    L = G.FUNCS['p80/bank_takeall']
    k = L.index('scoreboard players operation #c bm.rng = @s bm.gbc'); L[k:k + 1] = ['function bm:p120/bk_loose', 'scoreboard players operation #c bm.rng = #bkl bm.rng']
    k = L.index('scoreboard players set @s bm.gbc 0'); L[k] = 'scoreboard players operation @s bm.gbc -= #c bm.rng'
    for f_ in ('p80/bank_take16', 'p80/bank_take64', 'p80/bank_takeall'):
        G.FUNCS[f_] = [l.replace('No coins in your account.', 'No loose coins in your account - Medallions and Trophies come out on their own page.') for l in G.FUNCS[f_]]
    # the account page shows them; the dialogs' values
    for f_ in ('p80/bank', 'p80/bank_coins', 'p80/bank_spoils', 'p80/bank_tokens'):
        L = G.FUNCS[f_]; L.insert(len(L) - 1, 'function bm:p120/bk_ui')
    fn('p120/bk_ui', ['function bm:p120/bk_loose', 'execute store result storage bm:ui bk2.c int 1 run scoreboard players get #bkl bm.rng',
                      'execute store result storage bm:ui bk2.all int 1 run scoreboard players get @s bm.gbc',
                      'execute store result storage bm:ui bk2.gm int 1 run scoreboard players get @s bm.gbm', 'execute store result storage bm:ui bk2.gt int 1 run scoreboard players get @s bm.gbt',
                      f'execute store result storage bm:ui bk2.gmi int 1 run clear @s {hold("gutter_medallion")} 0',
                      f'execute store result storage bm:ui bk2.gti int 1 run clear @s {hold("gutter_trophy")} 0'])
    btitle = lambda sub: [T('THE GUTTER BANK', GOLD_, bold=True), T('  ·  ' + sub, 'gray')]
    back = P28.btn(T('« Back', 'gray'), MC + 2, width=150)
    pieces = [T('\n◆ ', GUT_M), T('Gutter Medallions   ', 'white'), T('$(gm)', GUT_M, bold=True), T('   (on you: $(gmi))', 'dark_gray'),
              T('\n◆ ', TRO), T('Gutter Trophies   ', 'white'), T('$(gt)', TRO, bold=True), T('   (on you: $(gti))', 'dark_gray')]
    acct = [T('YOUR ACCOUNT\n', 'white', bold=True), T('◆ ', GOLD_), T('Gutter Coins   ', 'white'), T('$(c)', GOLD_, bold=True), T('   (on you: $(ci))', 'dark_gray')] + pieces + \
        sum(([T('\n◆ ', m[3]), T(m[2] + '   ', 'white'), T(f'$(m{i})', m[3], bold=True)] for i, m in enumerate(P80.MATS, 1)), []) + \
        [T('\nAll told: ', 'gray'), T('$(all)', GOLD_, bold=True), T(' coins', 'gray'), T(' (a Medallion is 16, a Trophy 128)', 'dark_gray')]
    bdlg = P28.multi(btitle('your coins and spoils'),
                     [P28.body(acct, 280),
                      P28.body([T('Deposit puts every coin, spoil, Gutter Medallion and Gutter Trophy you carry into your account - Medallions and Trophies kept as they are. ', 'gray'),
                                T('The Armory and the shops pay from here first, then from your pockets.', 'dark_gray')], 300)],
                     [P28.btn([T('⬇ ', P80.LUCKY), T('Deposit everything', 'white', bold=True)], MC + 40, tooltip=T('All the coins, spoils, Medallions and Trophies you carry.'), width=150),
                      P28.btn([T('⬆ ', GOLD_), T('Take out coins', 'white')], MC + 46, tooltip=T('16, 64, all your loose coins - or change some into a Medallion.'), width=150),
                      P28.btn([T('⬆ ', TRO), T('Medallions & Trophies', 'white')], PAGE, tooltip=T('Take out the Gutter Medallions and Trophies you keep here.'), width=150),
                      P28.btn([T('⬆ ', '#c060ff'), T('Take out spoils', 'white')], MC + 47, tooltip=T('Cogs, seals, leaves, pearls, embers, insignia.'), width=150),
                      P28.btn([T('✦ ', GOLD_), T('Buy Tokens', 'white')], MC + 48, tooltip=T(f'{P80.TOKEN_COINS} coins a Black Market Token.'), width=150),
                      P28.btn(T('« The Office', 'gray'), MC, width=150)],
                     columns=2)
    G.FUNCS['p80/bank_dlg'] = [f'$dialog show @s {P28.inline(bdlg)}']
    tdlg = P28.multi(btitle('Black Market Tokens'),
                     [P28.body([T(f'A Token costs {P80.TOKEN_COINS} coins - from your account first (a Medallion or Trophy is broken into change only if it has to be), '
                                  'then your pockets.\n', 'gray'), T('◆ ', GOLD_), T('In your account, all told   ', 'white'), T('$(all)', GOLD_, bold=True),
                                T('   (coins on you: $(ci))', 'dark_gray')], 300)],
                     [P28.btn([T('Buy 1 Token ', GOLD_), T(f'({P80.TOKEN_COINS})', 'gray')], MC + 44, width=150),
                      P28.btn([T('Buy 10 Tokens ', GOLD_), T(f'({P80.TOKEN_COINS * 10})', 'gray')], MC + 45, width=150), back],
                     columns=2)
    G.FUNCS['p80/bank_tdlg'] = [f'$dialog show @s {P28.inline(tdlg)}']
    pdlg = P28.multi(btitle('Medallions & Trophies'),
                     [P28.body([T('YOUR ACCOUNT', 'white', bold=True)] + pieces, 280),
                      P28.body([T('Kept just as you put them in. A Medallion is worth 16 coins, a Trophy 128 - Goldtooth, the Tailor and the Armory all take them.', 'gray')], 300)],
                     [P28.btn([T('Take 1 Medallion', GUT_M)], PAGE + 1, width=150), P28.btn([T('Take all Medallions', GUT_M)], PAGE + 2, width=150),
                      P28.btn([T('Take 1 Trophy', TRO)], PAGE + 3, width=150), P28.btn([T('Take all Trophies', TRO)], PAGE + 4, width=150), back],
                     columns=2)
    bank_lines = [l for l in G.FUNCS['p80/bank'][:-1]]
    fn('p120/bk_page', bank_lines + ['function bm:p120/bk_dlg with storage bm:ui bk2'])
    fn('p120/bk_dlg', [f'$dialog show @s {P28.inline(pdlg)}'])
    G.FUNCS['p80/act'].insert(2, f'execute if score #act bm.pay matches {PAGE}..{PAGE + 4} run return run function bm:p120/bk_act')
    for iid in ('gutter_medallion', 'gutter_trophy'):                     # (p80/hand: #k at a time)
        wjson(f'bm/loot_table/p80/n/{iid}.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry(iid, {'type': 'minecraft:score', 'target': {'type': 'minecraft:fixed', 'name': '#k'},
                                                                                                        'score': 'bm.rng'})]}]})
    fn('p120/bk_act', [f'execute if score #act bm.pay matches {PAGE} run return run function bm:p120/bk_page'] +
       [f'execute if score #act bm.pay matches {PAGE + j} run return run function bm:p120/bk_{a}' for j, a in ((1, 'm1'), (2, 'ma'), (3, 't1'), (4, 'ta'))])
    say = lambda txt, col='gray': tellraw('@s', [T('[', 'dark_gray'), T('Gutter Bank', GOLD_, bold=True), T('] ', 'dark_gray'), T(txt, col)])
    for k_, obj, iid, worth, nm in (('m', 'bm.gbm', 'gutter_medallion', 16, 'Gutter Medallions'), ('t', 'bm.gbt', 'gutter_trophy', 128, 'Gutter Trophies')):
        fn(f'p120/bk_{k_}1', ['function bm:p80/init_me', f'execute unless score @s {obj} matches 1.. run return run ' + say(f'No {nm} in your account.'),
                              f'scoreboard players remove @s {obj} 1', f'scoreboard players remove @s bm.gbc {worth}', f'loot give @s loot bm:items/{iid}',
                              'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.4', 'function bm:p120/bk_page'])
        fn(f'p120/bk_{k_}a', ['function bm:p80/init_me', f'execute unless score @s {obj} matches 1.. run return run ' + say(f'No {nm} in your account.'),
                              f'scoreboard players operation #c bm.rng = @s {obj}', f'scoreboard players set @s {obj} 0',
                              f'scoreboard players set #bkk bm.rng {worth}', 'scoreboard players operation #bkw bm.rng = #c bm.rng', 'scoreboard players operation #bkw bm.rng *= #bkk bm.rng',
                              'scoreboard players operation @s bm.gbc -= #bkw bm.rng', f'function bm:p80/hand {{iid:"{iid}"}}',
                              'playsound minecraft:block.chain.break player @s ~ ~ ~ 0.8 1.2', 'function bm:p120/bk_page'])

    # ================================================================== SPEED RUN, ALARM OFF: time's up - no guards
    lk = G.FUNCS['p70/lockdown']
    lk.insert(0, 'execute unless score @s bm.gval matches 1 run return run function bm:p120/timeup')
    fn('p120/timeup', ['scoreboard players set @s bm.gvlk 1', 'function bm:p70/bar',                  # (the haul shrinks, as a lockdown's would)
                       'title @a[tag=bm.gvme] times 5 50 15', title('@a[tag=bm.gvme]', 'title', T("TIME'S UP", '#7dd8ff', bold=True)),
                       title('@a[tag=bm.gvme]', 'subtitle', T('Too slow - the haul shrinks', 'gray')),
                       'execute as @a[tag=bm.gvme] at @s run playsound minecraft:block.note_block.bass player @s ~ ~ ~ 1 0.6'])
    # (patrols: only with the alarm on, and only until the vault's open)
    ins2 = G.FUNCS['p70/inst_sec']
    for i, l in enumerate(ins2):
        if l == 'execute if score @s bm.gvst matches 2..3 if score @s bm.gva matches 50.. run scoreboard players add @s bm.gvw 1':
            ins2[i] = 'execute if score @s bm.gvst matches 2 if score @s bm.gval matches 1 if score @s bm.gva matches 50.. run scoreboard players add @s bm.gvw 1'
        elif l.endswith('run function bm:p70/patrol') and l.startswith('execute if score @s bm.gvlk matches'):
            ins2[i] = l.replace('execute if score @s bm.gvlk', 'execute if score @s bm.gvst matches 2 if score @s bm.gval matches 1 if score @s bm.gvlk')
    assert sum('bm.gval matches 1' in l for l in ins2) == 3, [l for l in ins2 if 'patrol' in l or 'gvw' in l]

    # ================================================================== THE TEMPLE: the solved stones glow for 10 seconds
    tb = '@e[type=minecraft:block_display,tag=bm.gvtb,distance=..20]'
    G.FUNCS['p91/temple/done'][1:1] = [f'tag {tb} add bm.gvtbg', f'scoreboard players set {tb} bm.tbg 0']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.tbg dummy']
    G.OBJECTIVES += ['bm.tbg']
    second[-1:-1] = ['execute as @e[type=minecraft:block_display,tag=bm.gvtb,tag=!bm.tbseen] run function bm:p120/tb_seen',
                     'scoreboard players add @e[type=minecraft:block_display,tag=bm.gvtbg] bm.tbg 1',
                     'execute as @e[type=minecraft:block_display,tag=bm.gvtbg,scores={bm.tbg=10..}] run data merge entity @s {Glowing:0b}',
                     'tag @e[type=minecraft:block_display,tag=bm.gvtbg,scores={bm.tbg=10..}] remove bm.gvtbg']
    fn('p120/tb_seen', ['tag @s add bm.tbseen', 'execute unless entity @s[tag=bm.gvtbg] if data entity @s {Glowing:1b} run scoreboard players set @s bm.tbg 0',
                        'execute unless entity @s[tag=bm.gvtbg] if data entity @s {Glowing:1b} run tag @s add bm.gvtbg'])

    # ================================================================== THE SKY ISLES: steadier feet, fewer breezes
    it = G.FUNCS['p112/isles/tick']
    it.insert(1, 'execute if score @s bm.gvs matches 1..2 positioned ~-12.5 ~-4 ~-12.5 as @a[tag=bm.gvp,dx=24,dy=24,dz=24] run function bm:p120/steady')
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.isl dummy']
    G.OBJECTIVES += ['bm.isl']
    fn('p120/steady', ['execute unless score @s bm.isl matches 1.. run attribute @s minecraft:explosion_knockback_resistance modifier add bm:isles_steady 0.65 add_value',
                       'scoreboard players set @s bm.isl 3'])
    tick += ['scoreboard players remove @a[scores={bm.isl=1..}] bm.isl 1', 'execute as @a[scores={bm.isl=0}] run function bm:p120/unsteady']
    fn('p120/unsteady', ['attribute @s minecraft:explosion_knockback_resistance modifier remove bm:isles_steady', 'scoreboard players reset @s bm.isl'])
    w2 = G.FUNCS['p112/isles/wave2']
    bl = [i for i, l in enumerate(w2) if 'function bm:p112/isles/breeze' in l]
    assert len(bl) == 3, bl
    w2[bl[1]] = w2[bl[1]].replace('if score #gt bm.rng matches 4..', 'if score #gt bm.rng matches 5..')
    del w2[bl[2]]

    # ================================================================== ALIEN HEISTS: now and then, a Skiff part in the haul
    wjson('bm/loot_table/gv/skiff_part.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry(p) for p, _n, _s in P35.PARTS]}]})
    HA, HB = '-200 64 -197', '-198 64 -197'                  # (the haul barrels - phase101)
    G.FUNCS['p70/haul'] += ['scoreboard players set #r bm.rng 100',
                            'execute if score #gn bm.rng matches 3 store result score #r bm.rng run random value 1..100',
                            f'execute if score #r bm.rng matches ..{SKIFF_CHANCE} run function bm:p120/skiff']
    fn('p120/skiff', [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot bm:gv/skiff_part',
                      f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot bm:gv/skiff_part',
                      tellraw('@s', P + [T('Salvage! ', '#7dffd0', bold=True), T('A ', 'gray'), T('Vorn Skiff part', '#5ad84a', bold=True),
                                         T(' turned up in your haul.', 'gray')])])
    fn('admin/skiff_haul', ['function bm:p120/skiff'])
