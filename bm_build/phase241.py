"""Phase 241 (2.99): THE VORN ARMADA - the Vorn's hard-mode dungeon: their hive-fleet, circling the Hive-Star far out in the End
(p2/armadacfg.py: the layout contract; p2/dungeons/armada.py: the builder; armada_lore.py: its words; phase242: Admiral Vexis;
phase243: Vexis, the Unlinked; phase244: its music).

FINDING IT  Hard mode: sabotage a Dreadnought's reactor (phase52) and among its spoils are THE HIVE-STAR COORDINATES. In the
            End (past the main island) use them: the signal goes out, a tractor beam answers - you are lifted into the dark for
            seven seconds, the fleet blooms round its star, THE VORN ARMADA - and set down on the Dock. The Dock's beam-out pad
            (and the rifts) take you back to where you signalled from.
THE FLEET   placed once per world in the End's void at armadacfg.ORIGIN (the volume cleared of outer islands first). Seven ships
            round the Hive-Star, joined by HARD-LIGHT BRIDGES that switch on as their trials are solved. Fall into the void and
            the fleet's tractor beam sets you back where you last stood (a hard hit). Too near the star, it scorches you.
            Inside, Adventure mode. It is a Phase 2 dungeon: p2/logic runs its eighteen trials, gates, waves, secret doors,
            vaults and the 20-minute idle reset - with four kinds of trial of its own (logic.EXTRA): a GUARDIAN rises (vboss:
            the Abductor, the Warlord and the Overseer, renamed and bigger - each falls with a Command Cipher), SOCKETS
            (xsock: Xenite in the Star-Forge's furnaces, the three Ciphers in the Command Lock), REACTORS (four conduits to
            smash under fire, reinforcements beaming in) and THE GAUNTLET (a corridor swept by sentry lasers).
HIDDEN      four rooms opened by followers nobody is promised (Zib, Donado, the Cursor, the Sky Buddies) and two secret ones:
            each a relic (once a player, ever) and a Hive Sigil (once a player each rebuild); six Sigils open the Hive Vault
            behind the helm, after the fall.
THE FALL    (phase242) the invasion nights END (#vfell bm.cfg): none is rolled, the Fleet Beacon gets no answer. The Armada
            comes apart and re-forms three minutes later. ATTACK A DREADNOUGHT AGAIN - one over your world (kill a guardian,
            start its reactor's sabotage) or one of the Armada's twins (sabotage its reactor) - and the hive remembers your
            world: the invasions are back, and Vexis will rise for whoever did it.
THE STARFORGE  a bench aboard the Dock: hold a Warplate piece and right-click it with 2 Star-Cores and 8 red Xenite in your
            pack, and it comes back Starforged (p2/armadaitems)."""
import json
from items import T, ITEMS
from nbt import snbt, B, F, Int
from structures import Build  # noqa: F401
import p2.armadacfg as A
import armada_lore as L

d = A.d
COL, RED, STAR = L.VX_COL, L.RED, L.STAR
OX, OY, OZ = A.ORIGIN
SX, SY, SZ = A.SIZE
END = 'minecraft:the_end'
BOX = f'x={OX},y={OY},z={OZ},dx={SX - 1},dy={SY - 1},dz={SZ - 1}'
AVER = 2                                  # bump to re-place the Armada in every world (a rebuild: everyone aboard is carried out)
COLLAPSE = 180                            # seconds between the Admiral's fall and the rebuild
GUARD_HP = {'brood': 520, 'forge': 640, 'nav': 900}
GUARD_SPAWN = {'brood': ('abductor', 'execute positioned ~ ~6 ~ run function bm:p32/boss/abductor'), 'forge': ('warlord', 'function bm:p32/boss/warlord'),
               'nav': ('overseer', 'execute positioned ~ ~7 ~ run function bm:p32/boss/overseer')}
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
W = lambda x, y, z: (OX + x, OY + y, OZ + z)          # local -> world
BUILT = {}
CLEAR = [f'type=minecraft:marker,tag=bm.d_{d}', 'tag=bm.kr', 'type=minecraft:husk,tag=bm.khost', 'tag=bm.asgt', 'tag=bm.ashow', 'tag=bm.arelic_d', 'tag=bm.arelic_i', 'tag=bm.arcond', 'tag=bm.arhit',
         'tag=bm.abench_i', 'tag=bm.amapd', 'tag=bm.dgmob', 'tag=bm.avorn', 'tag=bm.aguard', 'tag=bm.avx', 'type=minecraft:item',
         'type=minecraft:experience_orb', 'type=minecraft:arrow', 'type=minecraft:spectral_arrow']
RELIC_NAME = {'squad_jetpack': "Zib's Squad Jetpack", 'hover_collar': "Specimen 117's Collar", 'hive_override': 'the Hive Override Chip',
              'stardust_kite': 'the Stardust Kite'}


def build():
    if 'B' not in BUILT:
        from p2.dungeons import armada
        BUILT['B'] = armada.build()
    return BUILT['B']


def who(k):
    import phase125 as P125
    return P125.WHO[k]


def host(k, r):
    return f'@e[tag={who(k)[4]},distance=..{r}]'


# ================================================================== the trials' own kinds (p2/logic.EXTRA)
def _vboss(G, d_, n, c):
    """a Cipher guardian rises when someone comes within r; it falls (killed by a player: p241/guard/killed) -> solved"""
    fn, title = G.fn, G.title
    k = c['p']['data']['k']; r = int(c['p']['data']['r'])
    nm, col, sub = L.GUARD[k]
    from p2.logic import el_sel
    fn(f'p2/{d}/pz{n}_rise', ['scoreboard players set @s bm.wv 1',
                              f'execute as {el_sel(d, n, "vboss", c["R"] + 4)} at @s run function bm:p241/guard/rise_{k}',
                              f'title @a[distance=..{r + 24}] times 10 60 20', title(f'@a[distance=..{r + 24}]', 'subtitle', T(sub, 'gray', italic=True)),
                              title(f'@a[distance=..{r + 24}]', 'title', T(nm.upper(), col, bold=True))])
    body = ['execute if score #act bm.rng matches 0 run return 0',
            # (it went - everyone left, or died: it rises again for the next to walk in)
            f'execute if score @s bm.wv matches 1.. unless entity @e[tag=bm.ag_{k},distance=..128] run scoreboard players set @s bm.wv 0',
            f'execute unless score @s bm.wv matches 1.. if entity @a[distance=..{r},gamemode=!spectator,gamemode=!creative] run function bm:p2/{d}/pz{n}_rise']
    reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.wv 0', f'execute as @e[tag=bm.ag_{k},distance=..128] at @s run function bm:p241/guard/gone']
    return body, reset


def _xsock(G, d_, n, c):
    """items dropped (Q) on their slots: XSOCK[n] {key: item}; all set -> solved"""
    from p2.logic import el_sel
    fn, title = G.fn, G.title
    R = c['R']
    want = A.XSOCK[n]
    body = ['execute if score #act bm.rng matches 0 run return 0',
            f'execute as {el_sel(d, n, "sock", R, ",tag=!bm.got")} at @s run function bm:p2/{d}/pz{n}_offer']
    off = []
    for key, iid in want.items():
        off.append(f'execute if entity @s[tag=bm.sk_{key}] as @e[type=minecraft:item,distance=..1.6] if items entity @s contents {holds(iid)} at @s run function bm:p2/{d}/pz{n}_take_{key}')
        fn(f'p2/{d}/pz{n}_take_{key}', ['item modify entity @s contents bm:p241/take_one',
                                        'execute if items entity @s contents minecraft:air run kill @s',
                                        f'execute as {el_sel(d, n, "sock", 3, f",tag=bm.sk_{key},sort=nearest,limit=1")} at @s run function bm:p241/sock/set_{iid}',
                                        f'execute as {c["ctrl"]} at @s run function bm:p2/{d}/pz{n}_tally'])
    fn(f'p2/{d}/pz{n}_offer', off)
    G.wjson('bm/item_modifier/p241/take_one.json', {'function': 'minecraft:set_count', 'count': -1, 'add': True})
    what = 'Cipher' if n == 17 else 'Xenite'
    where = 'The Command Lock takes the Cipher: ' if n == 17 else 'The furnace takes the Xenite: '
    fn(f'p2/{d}/pz{n}_tally', [f'execute store result score #h bm.rng if entity {el_sel(d, n, "sock", R, ",tag=bm.got")}',
                               f'execute if score #h bm.rng matches {len(want)}.. run return run function bm:p241/sock/all{n}',
                               title('@a[distance=..20]', 'actionbar', [T(where, COL), {'score': {'name': '#h', 'objective': 'bm.rng'}, 'color': 'white'}, T(f' / {len(want)}', COL)])])
    fn(f'p241/sock/all{n}', [f'execute as {c["ctrl"]} at @s run function bm:p2/{d}/pz{n}_solve'] +
       (['execute as @a[distance=..24,gamemode=!spectator] at @s run function bm:p241/key'] if n == 17 else []))
    reset = ['scoreboard players set @s bm.done 0', f'tag {el_sel(d, n, "sock", R)} remove bm.got',
             f'execute as {el_sel(d, n, "sock", R)} at @s run kill @e[type=minecraft:item_display,tag=bm.ashow,distance=..2]']
    _ = what
    return body, reset


def _reactor(G, d_, n, c):
    """a Dreadnought's reactor: walk in and four conduits blaze up round its core; strike each 8 times while troopers beam in
    every 15 s; all four broken -> solved (and, after the Admiral's fall, the hive remembers your world)"""
    from p2.logic import el_sel
    fn, title = G.fn, G.title
    R = c['R']
    body = ['execute if score #act bm.rng matches 0 run return 0',
            f'execute unless score @s bm.wv matches 1.. if entity @a[distance=..{min(R, 14)},gamemode=!spectator,gamemode=!creative] run function bm:p2/{d}/pz{n}_ignite',
            'execute unless score @s bm.wv matches 1.. run return 0',
            f'execute unless entity @a[distance=..{R + 16},gamemode=!spectator] run return run function bm:p2/{d}/pz{n}_douse',
            f'execute unless entity @e[type=minecraft:interaction,tag=bm.arhit,distance=..{R + 4}] run return run function bm:p2/{d}/pz{n}_broken',
            'scoreboard players add @s bm.wt 1', 'execute if score @s bm.wt matches 15.. run function bm:p241/rx/reinforce',
            'particle minecraft:dust{color:[1.0,0.1,0.1],scale:2.0} ~ ~1 ~ 0.6 1.2 0.6 0 16 force @a[distance=..40]']
    fn(f'p2/{d}/pz{n}_ignite', ['scoreboard players set @s bm.wv 1', 'scoreboard players set @s bm.wt 0',
                                f'execute as {el_sel(d, n, "conduit", R)} at @s run function bm:p241/rx/conduit',
                                f'title @a[distance=..{R + 16}] times 10 50 20', title(f'@a[distance=..{R + 16}]', 'subtitle', T('Smash the four power conduits round the core!', RED)),
                                title(f'@a[distance=..{R + 16}]', 'title', T('REACTOR UNDER ATTACK', RED, bold=True)),
                                f'playsound minecraft:block.beacon.activate hostile @a[distance=..{R + 16}] ~ ~ ~ 1 0.5',
                                f'playsound minecraft:event.raid.horn hostile @a[distance=..{R + 16}] ~ ~ ~ 1.5 1.4'])
    fn(f'p2/{d}/pz{n}_douse', ['scoreboard players set @s bm.wv 0', f'kill @e[type=minecraft:item_display,tag=bm.arcond,distance=..{R + 4}]',
                               f'kill @e[type=minecraft:interaction,tag=bm.arhit,distance=..{R + 4}]'])
    fn(f'p2/{d}/pz{n}_broken', ['scoreboard players set @s bm.wv 0', f'function bm:p2/{d}/pz{n}_solve',
                                f'title @a[distance=..{R + 16}] title ' + snbt(T('REACTOR OFFLINE', COL, bold=True)),
                                f'playsound minecraft:block.beacon.deactivate hostile @a[distance=..{R + 16}] ~ ~ ~ 1 0.5', 'particle minecraft:end_rod ~ ~1 ~ 2 2 2 0.1 50',
                                # (after the fall: you attacked a Dreadnought - the hive remembers your world)
                                f'execute if score #vfell bm.cfg matches 1 as @a[distance=..{R + 24},gamemode=!spectator,limit=1,sort=nearest] at @s run function bm:p241/rekindle',
                                f'execute as @a[distance=..{R + 24},gamemode=!spectator] at @s run function bm:p241/rx/spoils'])
    reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.wv 0', f'function bm:p2/{d}/pz{n}_douse']
    return body, reset


def _gauntlet(G, d_, n, c):
    """the boarding corridor: the reach goal at its end; its sentries sweep it (p241/gauntlet - run as the trial's controller)"""
    from p2.logic import el_sel
    body = [f'execute as @e[type=minecraft:ender_pearl,distance=..{c["R"] + 8}] at @s run function bm:p2/util/pearl_zap',
            'execute if score #act bm.rng matches 0 run return 0',
            f'execute if entity @a[distance=..{c["R"] + 6},gamemode=!spectator] run function bm:p241/gauntlet/tick',
            f'execute as {el_sel(d, n, "goal", c["R"])} at @s if entity @a[distance=..1.6,gamemode=!spectator] as {c["ctrl"]} at @s run function bm:p2/{d}/pz{n}_solve']
    reset = ['scoreboard players set @s bm.done 0', 'scoreboard players set @s bm.pt 0']
    return body, reset


def setup():
    from p2 import logic
    logic.EXTRA.update(vboss=_vboss, xsock=_xsock, reactor=_reactor, gauntlet=_gauntlet)


setup()


# ================================================================== generate
def generate(G):
    fn, title, tellraw, give, wjson = G.fn, G.title, G.tellraw, G.give, G.wjson
    tick, fast, second = G.FUNCS['tick'], G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = G.PREFIX
    A.register()
    Ab = build()
    M = Ab.meta['armada']
    Ab.export(G.path('data', 'bm', 'structure', f'p2_{d}.nbt'))

    objs = ['bm.aox', 'bm.aoy', 'bm.aoz', 'bm.asx', 'bm.asy', 'bm.asz', 'bm.aocd', 'bm.akit', 'bm.ajet', 'bm.aaq', 'bm.abeam'] + [f'bm.ars_{k}' for k in list(A.HIDDEN) + ['secret1', 'secret2']]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        'execute unless score #aver bm.p2 matches 0.. run scoreboard players set #aver bm.p2 0',
        'execute unless score #arun bm.p2 matches 1.. run scoreboard players set #arun bm.p2 1',
        'execute unless score #vfell bm.cfg matches 0.. run scoreboard players set #vfell bm.cfg 0']
    G.OBJECTIVES += objs

    # ---- the framework runs it (only its own lines)
    from p2 import logic
    parts = logic.generate(G, {d: Ab})
    for f_ in (f'p2/{d}/rearm', f'p2/{d}/xdoor_open'):
        G.FUNCS.pop(f_, None)
    mine = lambda ls: [l for l in ls if f'd_{d}' in l]
    tick += mine(parts['tick'])
    second[-1:-1] = mine(parts['second'])
    k = fast.index('scoreboard players reset @a bm.sneak')
    fast[k:k] = mine(parts['fast'])
    pth = G.path('data', 'bm', 'tags', 'block', 'dungeon_floor.json')
    floors = set(json.load(open(pth))['values'])
    for (x, y, z), st in Ab.b.items():
        if 'air' in st and (x, y - 1, z) in Ab.b:
            below = Ab.b[(x, y - 1, z)].split('[')[0]
            if 'air' not in below and 'light' not in below and 'lava' not in below: floors.add(below)
    wjson('bm/tags/block/dungeon_floor.json', {'values': sorted(floors)})

    # ---- who is aboard (in the End, within the box): the music, Adventure mode, the void's tractor beam
    second[0:0] = ['tag @a[tag=bm.ain] remove bm.ain', f'execute in {END} run tag @a[{BOX}] add bm.ain']
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.aaq dummy']
    second += ['execute as @a[tag=bm.ain,gamemode=survival] run function bm:p241/adv/in',
               'scoreboard players set @a[tag=bm.aadv,tag=bm.ain] bm.aaq 3', 'scoreboard players remove @a[tag=bm.aadv,tag=!bm.ain] bm.aaq 1',
               'execute as @a[tag=bm.aadv,tag=!bm.ain,scores={bm.aaq=..0}] run function bm:p241/adv/out']
    fn('p241/adv/in', ['tag @s add bm.aadv', 'gamemode adventure @s', title('@s', 'actionbar', [T('The Vorn Armada', COL, bold=True), T(' - hive-hull does not break. (Adventure mode)', 'gray')])])
    fn('p241/adv/out', ['tag @s remove bm.aadv', 'execute if entity @s[gamemode=adventure] run gamemode survival @s'])
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.aadv] run function bm:p241/adv/out']

    # ---- the void: where you last stood (on the ground, aboard) - and the tractor beam that sets you back there
    second.append('execute as @a[tag=bm.ain,gamemode=!spectator] if entity @s[nbt={OnGround:1b}] run function bm:p241/void/mark')
    fn('p241/void/mark', ['execute store result score @s bm.asx run data get entity @s Pos[0]', 'execute store result score @s bm.asy run data get entity @s Pos[1]',
                          'execute store result score @s bm.asz run data get entity @s Pos[2]'])
    dk = M['dock']
    dwx, dwy, dwz = W(dk[0], dk[1], dk[2]) if dk else W(*A.SHIPS['dock'])
    fast.append(f'execute in {END} as @a[x={OX - 16},y={OY - 80},z={OZ - 16},dx={SX + 32},dy=80,dz={SZ + 32},gamemode=!spectator,gamemode=!creative] at @s run function bm:p241/void/catch')
    fn('p241/void/catch', ['execute unless score @s bm.asy matches -64.. run return run function bm:p241/void/dock',
                           'execute store result storage bm:tmp av.x int 1 run scoreboard players get @s bm.asx', 'execute store result storage bm:tmp av.y int 1 run scoreboard players get @s bm.asy',
                           'execute store result storage bm:tmp av.z int 1 run scoreboard players get @s bm.asz', 'function bm:p241/void/to with storage bm:tmp av',
                           'function bm:p241/void/hit'])
    fn('p241/void/to', ['$execute in minecraft:the_end run tp @s $(x).5 $(y) $(z).5'])
    fn('p241/void/dock', [f'execute in {END} run tp @s {dwx + 0.5} {dwy} {dwz + 0.5}', 'function bm:p241/void/hit'])
    fn('p241/void/hit', ['damage @s 6 minecraft:fall', 'effect give @s minecraft:slow_falling 3 0 true', 'effect give @s minecraft:resistance 2 2 true',
                         'particle minecraft:end_rod ~ ~1 ~ 0.4 1.2 0.4 0.05 40', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 1.4',
                         title('@s', 'actionbar', T('A tractor beam snatches you out of the void - and drops you, hard.', COL, italic=True))])

    # ---- the Hive-Star: its corona; too near it, it scorches you
    sx_, sy_, sz_ = W(*A.STAR['c'])
    second += [f'execute in {END} if entity @a[x={sx_},y={sy_},z={sz_},distance=..160] run function bm:p241/star/sec']
    fn('p241/star/sec', [f'execute in {END} run particle minecraft:flame {sx_} {sy_} {sz_} {A.STAR["r"] * 0.7:.0f} {A.STAR["r"] * 0.7:.0f} {A.STAR["r"] * 0.7:.0f} 0.15 40 force @a[distance=..200]',
                         f'execute in {END} run particle minecraft:dust{{color:[1.0,0.45,0.15],scale:4.0}} {sx_} {sy_} {sz_} {A.STAR["r"]} {A.STAR["r"]} {A.STAR["r"]} 0 30 force @a[distance=..200]',
                         f'execute in {END} run particle minecraft:lava {sx_} {sy_} {sz_} {A.STAR["r"] * 0.8:.0f} {A.STAR["r"] * 0.8:.0f} {A.STAR["r"] * 0.8:.0f} 0 8 force @a[distance=..200]',
                         f'execute in {END} as @a[x={sx_},y={sy_},z={sz_},distance=..{A.STAR["burn"]},gamemode=!spectator,gamemode=!creative] at @s run function bm:p241/star/burn'])
    fn('p241/star/burn', ['damage @s 3 minecraft:in_fire', 'data modify entity @s Fire set value 60s',
                          title('@s', 'actionbar', T('The Hive-Star scorches you - get away from it!', STAR, bold=True))])

    # ---- hidden sigils: their followers' names, lit while they stand there
    fn('p241/sigil/lit', ['scoreboard players add #hs bm.rng 1', 'execute if entity @s[tag=bm.lit] run return 0', 'tag @s add bm.lit', 'particle minecraft:end_rod ~ ~1 ~ 0.1 0.8 0.1 0.01 10',
                          'playsound minecraft:block.respawn_anchor.charge block @a[distance=..16] ~ ~ ~ 0.8 1.2'])
    for kk in sorted({w_[0] for h in M['hidden'].values() for w_ in h['sigils']}):
        nm, _pr, c = who(kk)[:3]
        txt = {'Tags': ['bm.asgt', 'bm.p2'], 'billboard': 'center', 'see_through': B(0), 'background': Int(0), 'shadow': B(1),
               'text': T(nm.upper(), c, bold=True), 'brightness': {'block': Int(10), 'sky': Int(10)},
               'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                  'translation': [F(0), F(0.15), F(0)], 'scale': [F(0.8), F(0.8), F(0.8)]}}
        fn(f'p241/sigil/name_{kk}', [f'summon minecraft:text_display ~ ~0.1 ~ {snbt(txt)}'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.ahsg,tag=bm.sw_{kk},tag=!bm.aon] at @s run function bm:p241/sigil/name_{kk}')
    second.append('tag @e[type=minecraft:marker,tag=bm.ahsg,tag=!bm.aon] add bm.aon')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.ahsg] at @s if entity @a[distance=..10] run particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.2} ~ ~0.15 ~ 0.6 0 0.6 0 2')

    # ---- doors of marker data {ax, w, h, b}: the hidden rooms, the Hive Vault
    DOORS = sorted({'minecraft:' + h['door'][6] for h in M['hidden'].values()} | ({'minecraft:' + M['vault'][6]} if M['vault'] else set()))
    bk = lambda b: b.split(':')[1].split('[')[0]
    for nm_ in ('open', 'close'):
        fn(f'p241/door/{nm_}', [f'execute if data entity @s {{data:{{b:"{b}"}}}} run return run function bm:p241/door/{nm_}_{bk(b)} with entity @s data' for b in DOORS])
        for b in DOORS:
            a_, b_ = (b, 'minecraft:air') if nm_ == 'open' else ('minecraft:air', b)
            fn(f'p241/door/{nm_}_{bk(b)}', ['$execute if entity @s[nbt={data:{ax:"x"}}] run fill ~-$(w) ~ ~ ~$(w) ~$(hh) ~ ' + f'{b_} replace {a_}',
                                             '$execute if entity @s[nbt={data:{ax:"z"}}] run fill ~ ~ ~-$(w) ~ ~$(hh) ~$(w) ' + f'{b_} replace {a_}'])
    for tg in ('bm.ahs', 'bm.avault'):
        second.append(f'execute in {END} as @e[type=minecraft:marker,tag={tg},{BOX}] unless data entity @s data.hh store result entity @s data.hh int 1 run data get entity @s data.h 0.999')

    # ---- HARD-LIGHT BRIDGES: on when their trial is solved; the reset takes them back
    BR = sorted({'minecraft:' + b_[7] for b_ in M['bridges']})
    fn('p241/bridge/make', [f'execute if data entity @s {{data:{{b:"{b}"}}}} run function bm:p241/bridge/make_{bk(b)} with entity @s data' for b in BR] +
       ['particle minecraft:end_rod ~ ~1 ~ 3 1 3 0.05 60', 'particle minecraft:dust{color:[0.5,1.0,0.35],scale:1.6} ~ ~1 ~ 3 1 3 0 60',
        'playsound minecraft:block.beacon.activate block @a[distance=..48] ~ ~ ~ 1 1.4', 'playsound minecraft:block.respawn_anchor.charge block @a[distance=..48] ~ ~ ~ 1 0.8'])
    fn('p241/bridge/clear', [f'execute if data entity @s {{data:{{b:"{b}"}}}} run function bm:p241/bridge/clear_{bk(b)} with entity @s data' for b in BR])
    for b in BR:
        fn(f'p241/bridge/make_{bk(b)}', [f'$fill ~ ~ ~ ~$(dx) ~$(dy) ~$(dz) {b} replace minecraft:air'])
        fn(f'p241/bridge/clear_{bk(b)}', [f'$fill ~ ~ ~ ~$(dx) ~$(dy) ~$(dz) minecraft:air replace {b}'])
    for n in sorted({b_[0] for b_ in M['bridges']}):
        G.FUNCS[f'p2/{d}/pz{n}_solve'].insert(2, f'execute as @e[type=minecraft:marker,tag=bm.abridge,tag=bm.g{n},tag=bm.d_{d},distance=..340] at @s run function bm:p241/bridge/make')
        G.FUNCS[f'p2/{d}/pz{n}_solve'].insert(2, title('@a[distance=..64]', 'actionbar', T('A hard-light bridge hums into being across the void.', COL, italic=True)))
    fast.append(f'execute in {END} as @e[type=minecraft:marker,tag=bm.abridge,{BOX}] at @s if entity @a[distance=..40] run particle minecraft:end_rod ~1 ~0.6 ~1 1 0.1 1 0 1')

    # ---- THE CIPHER GUARDIANS: the Vorn's own bosses, renamed and bigger, nothing of their own to give but their Cipher
    for k, (b, spawn) in GUARD_SPAWN.items():
        nm, col, sub = L.GUARD[k]
        hp = GUARD_HP[k]
        fn(f'p241/guard/rise_{k}', [spawn, f'execute as @e[tag=bm.vb_{b},tag=!bm.aguard,distance=..16,sort=nearest,limit=1] at @s run function bm:p241/guard/init_{k}'])
        fn(f'p241/guard/init_{k}', ['tag @s add bm.aguard', f'tag @s add bm.ag_{k}', 'tag @s add bm.vstay', f'attribute @s minecraft:max_health base set {hp}',
                                    f'data modify entity @s Health set value {hp}.0f', f'data modify entity @s CustomName set value {snbt(T(nm, col, bold=True))}',
                                    'data modify entity @s DeathLootTable set value "bm:p241/guardian"',
                                    f'bossbar set bm:{b} name {snbt(T(nm, col, bold=True))}', f'bossbar set bm:{b} max {hp}',
                                    'particle minecraft:end_rod ~ ~2 ~ 1 1.5 1 0.08 80'])
    G.wjson('bm/advancement/p241/guard.json', {'criteria': {'kill': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:nbt': '{Tags:["bm.aguard"]}'}}]}}}, 'rewards': {'function': 'bm:p241/guard/killed'}})
    fn('p241/guard/killed', ['advancement revoke @s only bm:p241/guard',
                             f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.pzt_vboss,tag=bm.d_{d},distance=..96,sort=nearest,limit=1] at @s run function bm:p241/guard/won'])
    fn('p241/guard/won', [f'execute if entity @s[tag=bm.pz{n}] run function bm:p241/guard/fell_{k}' for n, k in A.VBOSS.items()])
    for n, k in A.VBOSS.items():
        nm, col, _sub = L.GUARD[k]
        cid = A.CIPHER[k]
        fn(f'p241/guard/fell_{k}', ['particle minecraft:explosion_emitter ~ ~2 ~ 1 1 1 0 2', 'playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 2 0.6',
                                    tellraw('@a[distance=..64]', [T(f'{nm} falls. ', col, bold=True), T('Something of the Admiral\'s was in it.', 'gray', italic=True)]),
                                    f'execute as @a[distance=..64,gamemode=!spectator] at @s run function bm:p241/guard/spoils_{k}',
                                    f'function bm:p2/{d}/pz{n}_solve'])
        fn(f'p241/guard/spoils_{k}', [f'execute unless items entity @s container.* {holds(cid)} run ' + give(cid), 'function bm:p241/key', give('star_core'),
                                      tellraw('@s', P + [T(L.ITEMS[cid.replace('cipher_', 'cipher_')][0], COL, bold=True), T(' - for the Flagship\'s Command Lock.', 'gray')])])
    fn('p241/guard/gone', ['execute on passengers run kill @s', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p241/key', [give('akey'), 'playsound minecraft:block.vault.insert_item player @s ~ ~ ~ 0.8 1.2'])
    G.wjson('bm/loot_table/p241/guardian.json', {'type': 'minecraft:entity', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('xenite_red', G.uni(6, 12))]},
                                                                                      {'rolls': 1, 'entries': [G.loot_entry('power_cell')]}]})

    # ---- sockets: the item shown on its slot
    for iid in sorted({v for m_ in A.XSOCK.values() for v in m_.values()}):
        mdl = ITEMS[iid]['comps'].get('minecraft:item_model', f'bm:{iid}')
        disp = {'Tags': ['bm.ashow'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': mdl}},
                'billboard': 'vertical', 'brightness': {'block': Int(14), 'sky': Int(14)},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(0.7), F(0)], 'scale': [F(0.7), F(0.7), F(0.7)]}}
        fn(f'p241/sock/set_{iid}', ['tag @s add bm.got', f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.04 20',
                                    'playsound minecraft:block.end_portal_frame.fill block @a[distance=..16] ~ ~ ~ 1 0.8'])

    # ---- reactors: conduits, reinforcements, spoils
    cond = snbt({'Tags': ['bm.arcond', 'bm.rnew'], 'item': {'id': 'minecraft:beacon', 'count': Int(1)}, 'item_display': 'fixed', 'brightness': {'block': Int(15), 'sky': Int(15)},
                 'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.6), F(0)], 'scale': [F(1.1)] * 3}})
    chit = snbt({'Tags': ['bm.arhit', 'bm.rnew'], 'width': F(1.3), 'height': F(1.6), 'response': B(1)})
    fn('p241/rx/conduit', [f'summon minecraft:item_display ~ ~ ~ {cond}', f'summon minecraft:interaction ~ ~ ~ {chit}',
                           'scoreboard players set @e[type=minecraft:interaction,tag=bm.rnew,distance=..0.5] bm.chp 8', 'tag @e[tag=bm.rnew,distance=..0.5] remove bm.rnew'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.arhit] if data entity @s attack at @s run function bm:p241/rx/hit')
    fn('p241/rx/hit', ['scoreboard players remove @s bm.chp 1', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.5 0.4 0.3 20', 'playsound minecraft:block.anvil.land hostile @a[distance=..24] ~ ~ ~ 0.5 1.6',
                       title('@a[distance=..8]', 'actionbar', [T('Conduit: ', RED), {'score': {'name': '@s', 'objective': 'bm.chp'}, 'color': 'white'}, T(' hits left', RED)]),
                       'execute if score @s bm.chp matches ..0 run return run function bm:p241/rx/break', 'data remove entity @s attack'])
    fn('p241/rx/break', ['particle minecraft:explosion ~ ~1 ~ 0.4 0.4 0.4 0 3', 'playsound minecraft:entity.generic.explode hostile @a[distance=..32] ~ ~ ~ 1 1.2',
                         'kill @e[type=minecraft:item_display,tag=bm.arcond,distance=..0.5]', 'kill @s'])
    fn('p241/rx/reinforce', ['scoreboard players set @s bm.wt 0',
                             f'execute as @e[type=minecraft:marker,tag=bm.pet_wsp,tag=bm.d_{d},distance=..16,sort=random,limit=2] at @s run function bm:p32/spawn/trooper',
                             'execute unless entity @e[type=minecraft:marker,tag=bm.pet_wsp,tag=bm.d_' + d + ',distance=..16] positioned ~3 ~ ~3 run function bm:p32/spawn/trooper',
                             'tag @e[tag=bm.vtroop,tag=!bm.avorn,distance=..20] add bm.vstay',
                             title('@a[distance=..40]', 'actionbar', T('Vorn reinforcements beaming in!', RED, bold=True))])
    fn('p241/rx/spoils', [give('xenite_red', 6), give('star_core'), 'function bm:p241/key',
                          f'execute if score #hard bm.cfg matches 1 unless entity @s[tag=bm.acoord] run tag @s add bm.acoord'])

    # ---- THE GAUNTLET: sentries that sweep the corridor (every 2 s; a warning spark, then a 1 s beam across it)
    S_ = {}
    for (n, x, y, z, facing, length) in M['sentries']:
        S_.setdefault(n, []).append((x, y, z, facing, length))
    mx_len = max([s_[5] for s_ in M['sentries']] + [5])
    fn('p241/gauntlet/tick', ['scoreboard players add @s bm.pt 1', 'execute if score @s bm.pt matches 40.. run scoreboard players set @s bm.pt 0',
                              f'execute as @e[type=minecraft:marker,tag=bm.asentry,distance=..{80}] at @s run function bm:p241/gauntlet/sentry'])
    # (a sentry's phase: odd ones a second behind the even ones, so the corridor never clears at once)
    fn('p241/gauntlet/sentry', ['scoreboard players operation #gp bm.rng = @e[type=minecraft:marker,tag=bm.pz,tag=bm.pzt_gauntlet,tag=bm.d_' + d + ',sort=nearest,limit=1] bm.pt',
                                'execute if entity @s[tag=bm.aodd] run scoreboard players add #gp bm.rng 20', 'scoreboard players set #c40 bm.rng 40',
                                'scoreboard players operation #gp bm.rng %= #c40 bm.rng',
                                'execute if score #gp bm.rng matches 10..19 run particle minecraft:electric_spark ^ ^ ^0.4 0.1 0.1 0.1 0.05 4',
                                'execute if score #gp bm.rng matches 20..39 run function bm:p241/gauntlet/beam'])
    beam = []
    for i in range(1, mx_len + 1):
        beam += [f'particle minecraft:dust{{color:[1.0,0.15,0.1],scale:1.2}} ^ ^ ^{i} 0.02 0.25 0.02 0 2',
                 f'execute positioned ^ ^ ^{i} positioned ~ ~-1.2 ~ as @a[distance=..1.2,gamemode=!spectator,gamemode=!creative] at @s run function bm:p241/gauntlet/zap']
    fn('p241/gauntlet/beam', beam)
    fn('p241/gauntlet/zap', ['damage @s 5 minecraft:lightning_bolt', 'effect give @s minecraft:slowness 2 2', 'playsound minecraft:entity.guardian.attack player @s ~ ~ ~ 1 1.6',
                             title('@s', 'actionbar', T('A sentry laser burns you - move between the sweeps!', RED))])
    # (which sentries are odd: by their place in the corridor, recorded at placement)
    odd = [f'execute in {END} positioned {W(x, y, z)[0] + 0.5} {W(x, y, z)[1] + 0.5} {W(x, y, z)[2] + 0.5} run tag @e[type=minecraft:marker,tag=bm.asentry,distance=..0.6] add bm.aodd'
           for i, (n, x, y, z, f_, ln) in enumerate(M['sentries']) if i % 2]
    fn('p241/gauntlet/odd', odd or ['return 0'])

    # ---- the Vorn in its waves are Vorn: a trooper's body on every husk, a saucer on every phantom
    fn('p241/dress', ['tag @s add bm.adone', 'tag @s add bm.vorn', 'tag @s add bm.vstay', 'execute if entity @s[type=minecraft:husk] run function bm:p241/dress/trooper',
                      'data merge entity @s[type=minecraft:phantom] {size:5}'])
    fn('p241/dress/trooper', ['effect give @s minecraft:invisibility infinite 0 true', 'effect give @s minecraft:fire_resistance infinite 0 true',
                              'tag @s add bm.adressme', 'execute summon minecraft:item_display run function bm:p241/dress/body', 'tag @s remove bm.adressme'])
    import phase32 as P32
    fn('p241/dress/body', ['data merge entity @s ' + snbt({'Tags': ['bm.vdisp', 'bm.vbody'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:vorn3d'}},
                                                         'item_display': 'fixed', 'brightness': {'block': Int(13), 'sky': Int(13)}, 'teleport_duration': Int(2),
                                                         'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                                                            'translation': [F(0), F(round(-P32.HUSK_SEAT + 1.15 / 2, 3)), F(0)], 'scale': [F(1.15)] * 3}}),
                           'ride @s mount @e[tag=bm.adressme,limit=1]'])
    tick.append('execute as @e[tag=bm.avorn,tag=!bm.adone] run function bm:p241/dress')

    # ---- the hive's voice: one line to each player, the first time they come near
    for key in sorted({v[0] for v in M['voices']}):
        fn(f'p241/voice/{key}', [f'tag @s add bm.av_{key}', tellraw('@s', [T(L.VOICE[key], L.HIVE, italic=True)]),
                                 'playsound minecraft:entity.elder_guardian.ambient hostile @s ~ ~ ~ 0.6 0.6'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.av_{key}] at @s as @a[distance=..7,tag=!bm.av_{key},gamemode=!spectator] at @s run function bm:p241/voice/{key}')

    # ================================================================== FINDING IT: the coordinates, the signal, the beam
    G.consume_adv('hive_coords', 'bm:p241/coords')
    from useitem import give_back
    fn('p241/coords', ['advancement revoke @s only bm:consume/hive_coords'] + give_back(G.item_arg('hive_coords')) +
       ['execute unless score #hard bm.cfg matches 1 run return run ' + title('@s', 'actionbar', T('The chart is dark. (Hard mode.)', 'gray', italic=True)),
        f'execute unless dimension {END} run return run ' + title('@s', 'actionbar', T('Nothing answers here. The Hive-Star is far out in the End.', 'gray', italic=True)),
        'execute if entity @s[x=-400,y=-64,z=-400,dx=800,dy=400,dz=800] run return run ' + title('@s', 'actionbar', T('Too near the dragon\'s island - the signal drowns. Go out past it.', 'gray', italic=True)),
        'execute if entity @s[tag=bm.ain] run return 0',
        'scoreboard players set #awant bm.p2 1',
        f'execute unless score #aver bm.p2 matches {AVER} run return run ' + title('@s', 'actionbar', T('The signal goes out... the fleet is coming about. Try again in a minute.', COL, italic=True)),
        'execute if score @s bm.abeam matches 1.. run return 0',
        'execute store result score @s bm.aox run data get entity @s Pos[0]', 'execute store result score @s bm.aoy run data get entity @s Pos[1]',
        'execute store result score @s bm.aoz run data get entity @s Pos[2]', 'scoreboard players set @s bm.abeam 1'])
    # the beam (7 s): lifted, the dark, the star - then the Dock
    BEAM = 140
    at = lambda t, cmd: f'execute if score @s bm.abeam matches {t} run {cmd}'
    fn('p241/beam/tick', ['scoreboard players add @s bm.abeam 1'] + [
        at(2, 'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 0.6'), at(2, 'playsound minecraft:entity.elder_guardian.curse player @s ~ ~ ~ 0.6 0.5'),
        at(2, title('@s', 'actionbar', T('The signal goes out. Something vast turns toward it.', COL, italic=True))),
        at('2..100', 'effect give @s minecraft:levitation 1 3 true'), at('2..120', 'particle minecraft:end_rod ~ ~-1 ~ 0.6 3 0.6 0.05 12'),
        at('2..120', 'particle minecraft:dust{color:[0.5,1.0,0.35],scale:2.0} ~ ~ ~ 0.8 4 0.8 0 16'),
        at(40, 'playsound minecraft:block.respawn_anchor.charge player @s ~ ~ ~ 1 0.5'), at(80, 'effect give @s minecraft:darkness 3 0 true'),
        at(90, 'title @s times 10 50 20'), at(90, title('@s', 'title', T('THE VORN ARMADA', COL, bold=True))),
        at(90, title('@s', 'subtitle', T('the hive-fleet of the Hive-Star', STAR, italic=True))), at(90, 'playsound minecraft:entity.ender_dragon.growl player @s ~ ~ ~ 0.8 0.5'),
        at(100, 'effect give @s minecraft:slow_falling 6 0 true'),
        at(BEAM, f'execute in {END} rotated {[0, 90, 180, 270][["south", "west", "north", "east"].index(dk[3])] if dk else 0} 0 run tp @s {dwx + 0.5} {dwy} {dwz + 0.5} ~ 0'),
        at(BEAM, 'particle minecraft:flash{color:[0.6,1.0,0.5,1.0]} ~ ~1 ~ 0 0 0 0 1'), at(BEAM, 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 0.8'),
        at(BEAM + 1, 'scoreboard players set @s bm.abeam 0')])
    tick.append('execute as @a[scores={bm.abeam=1..}] at @s run function bm:p241/beam/tick')
    # out: the Dock's pad, the rifts - back to where you signalled from (or the End's own island)
    fn('p241/out', ['execute unless score @s bm.aoy matches -64.. run return run execute in minecraft:the_end run tp @s 100.5 50 0.5',
                    'execute store result storage bm:tmp ao.x int 1 run scoreboard players get @s bm.aox', 'execute store result storage bm:tmp ao.y int 1 run scoreboard players get @s bm.aoy',
                    'execute store result storage bm:tmp ao.z int 1 run scoreboard players get @s bm.aoz', 'function bm:p241/void/to with storage bm:tmp ao',
                    'tag @s remove bm.ain', 'effect give @s minecraft:slow_falling 4 0 true',
                    'particle minecraft:end_rod ~ ~1 ~ 0.3 0.8 0.3 0.05 30', 'playsound minecraft:block.beacon.deactivate player @s ~ ~ ~ 0.8 1.2'])
    fast.append('execute as @e[type=minecraft:marker,tag=bm.ahome] at @s as @a[distance=..1.2,gamemode=!spectator] at @s run function bm:p241/out')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.arift] at @s as @a[distance=..1.2,gamemode=!spectator] at @s run function bm:p241/out')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.ahome] at @s if entity @a[distance=..24] run particle minecraft:end_rod ~ ~0.3 ~ 0.4 0.1 0.4 0.02 3')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.arift] at @s if entity @a[distance=..24] run particle minecraft:end_rod ~ ~0.3 ~ 0.4 0.1 0.4 0.02 3')
    # the coordinates: in hard mode, the first Dreadnought reactor you sabotage (phase52) gives them up
    G.FUNCS['p52/rx/win'].append(f'execute if score #hard bm.cfg matches 1 as @a[gamemode=!spectator,distance=..40] unless items entity @s container.* {holds("hive_coords")} run function bm:p241/coords_found')
    fn('p241/coords_found', [give('hive_coords'), tellraw('@s', P + [T('In the Dreadnought\'s vault: ', 'gray'), T(L.ITEMS['coords'][0], STAR, bold=True),
                                                                   T('. In the End, use them - something vast will answer.', 'gray')])])

    # ================================================================== THE PLACING (once; and again after every fall)
    fl = f'{OX - 8} {OZ - 8} {OX + SX + 8} {OZ + SZ + 8}'
    clr = []
    for bx in range(0, SX, 32):
        for by in range(0, SY, 32):
            for bz in range(0, SZ, 32):
                clr.append(f'execute in {END} run fill {OX + bx} {OY + by} {OZ + bz} {OX + min(SX, bx + 32) - 1} {OY + min(SY, by + 32) - 1} {OZ + min(SZ, bz + 32) - 1} minecraft:air')
    bio = []
    for bx in range(0, SX, 60):
        for bz in range(0, SZ, 60):
            bio.append(f'execute in {END} run fillbiome {OX + bx} {OY} {OZ + bz} {OX + min(SX, bx + 60) - 1} {OY + SY - 1} {OZ + min(SZ, bz + 60) - 1} bm:armada')
    fn('p241/build/try', [f'execute in {END} run forceload add {fl}',
                          f'execute in {END} store success score #aload bm.p2 if loaded {OX} {OY} {OZ} if loaded {OX + SX - 1} {OY} {OZ + SZ - 1} if loaded {OX} {OY} {OZ + SZ - 1} if loaded {OX + SX - 1} {OY} {OZ}',
                          'execute unless score #aload bm.p2 matches 1 run return run scoreboard players set #await bm.p2 0',
                          'scoreboard players add #await bm.p2 1', 'execute unless score #await bm.p2 matches 4.. run return 0',
                          f'execute in {END} as @a[{BOX}] at @s run function bm:p241/out',
                          *[f'execute in {END} run kill @e[{s_},{BOX}]' for s_ in CLEAR]] + clr + [
                          'scoreboard players set #abuilt bm.p2 0',
                          f'execute in {END} store success score #abuilt bm.p2 run place template bm:p2_{d} {OX} {OY} {OZ}',
                          'execute unless score #abuilt bm.p2 matches 1 run return 0'] + bio + [
                          'function bm:p241/gauntlet/odd',
                          f'scoreboard players set #aver bm.p2 {AVER}', 'scoreboard players add #arun bm.p2 1', 'scoreboard players set #afell bm.p2 0',
                          f'execute in {END} run forceload remove {fl}'])
    second.append(f'execute if score #awant bm.p2 matches 1 unless score #aver bm.p2 matches {AVER} unless score #acol bm.p2 matches 1.. run function bm:p241/build/try')
    G.FUNCS['load'][-1:-1] = ['execute if entity @a[tag=bm.acoord] run scoreboard players set #awant bm.p2 1']

    # ---- the fall: three minutes, then everyone out and the Armada re-formed (phase242 calls this)
    fn('p241/collapse', ['scoreboard players set #afell bm.p2 1', f'scoreboard players set #acol bm.p2 {COLLAPSE}',
                         f'execute in {END} run ' + tellraw(f'@a[{BOX}]', [T('The fleet drifts, voiceless. ', COL, bold=True),
                                                                           T(f'In {COLLAPSE // 60} minutes the hive regroups it - and anyone still aboard is beamed out.', 'gray')])])
    fn('p241/collapse_sec', ['scoreboard players remove #acol bm.p2 1',
                             *[f'execute if score #acol bm.p2 matches {s_} in {END} run ' + title(f'@a[{BOX}]', 'actionbar', T(f'The Armada regroups in {s_} seconds.', COL))
                               for s_ in (120, 60, 30, 10, 5, 4, 3, 2, 1)],
                             'execute if score #acol bm.p2 matches ..0 run scoreboard players set #aver bm.p2 0'])
    second.append('execute if score #acol bm.p2 matches 1.. run function bm:p241/collapse_sec')
    G.FUNCS[f'p2/{d}/reset'] += [f'execute as @e[type=minecraft:marker,tag=bm.abridge,tag=bm.d_{d},distance=..340] at @s run function bm:p241/bridge/clear',
                                 f'execute as @e[type=minecraft:marker,tag=bm.ahs,tag=bm.open,distance=..340] at @s run function bm:p241/hidden/close',
                                 'kill @e[type=minecraft:item_display,tag=bm.ashow,distance=..340]',
                                 f'tag @e[type=minecraft:marker,tag=bm.d_{d},tag=bm.lit,distance=..340] remove bm.lit']

    # ================================================================== THE HIDDEN ROOMS
    for k, h in M['hidden'].items():
        title_, ws, relic = A.HIDDEN[k]
        req = [w_[0] for w_ in h['sigils']]
        lines = ['scoreboard players set #hs bm.rng 0']
        for w_ in req:
            lines.append(f'execute as @e[type=minecraft:marker,tag=bm.ahsg,tag=bm.ahs_{k},tag=bm.sw_{w_},distance=..40] at @s if entity {host(w_, 1.8)} run function bm:p241/sigil/lit')
        lines.append(f'execute if score #hs bm.rng matches {len(req)}.. run function bm:p241/hidden/open_{k}')
        fn(f'p241/hidden/try_{k}', lines)
        fn(f'p241/hidden/open_{k}', ['tag @s add bm.open', 'function bm:p241/door/open',
                                     'particle minecraft:end_rod ~ ~1.5 ~ 1 1.5 1 0.02 40', 'playsound minecraft:block.beacon.activate block @a[distance=..24] ~ ~ ~ 1 1.2',
                                     title('@a[distance=..16]', 'actionbar', [T(title_, '#9adf8a', bold=True), T(' opens for its friends.', 'gray', italic=True)])])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.ahs_{k},tag=bm.ahs,tag=!bm.open] at @s if entity @a[distance=..20] run function bm:p241/hidden/try_{k}')
    fn('p241/hidden/close', ['tag @s remove bm.open', 'function bm:p241/door/close'])
    # ---- relic pedestals: the room's Hive Sigil (once a player each rebuild), its relic (once a player, ever)
    REL = {k: (A.HIDDEN[k][0], A.HIDDEN[k][2]) for k in A.HIDDEN}
    REL.update({'secret1': ('a forgotten hold', None), 'secret2': ('a sealed bulkhead', None)})
    for k, (title_, relic) in REL.items():
        mdl = ITEMS[relic]['comps'].get('minecraft:item_model', f'bm:{relic}') if relic else 'bm:hive_sigil'
        disp = {'Tags': ['bm.arelic_d'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': mdl}},
                'billboard': 'vertical', 'brightness': {'block': Int(14), 'sky': Int(14)},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)],
                                   'translation': [F(0), F(0.9), F(0)], 'scale': [F(0.7), F(0.7), F(0.7)]}}
        fn(f'p241/relic/spawn_{k}', ['tag @s add bm.aon', f'summon minecraft:item_display ~ ~ ~ {snbt(disp)}',
                                     f'summon minecraft:interaction ~ ~ ~ {{Tags:["bm.arelic_i","bm.arel_{k}"],width:1.0f,height:1.6f,response:1b}}'])
        second.append(f'execute as @e[type=minecraft:marker,tag=bm.arel_{k},tag=!bm.aon] at @s run function bm:p241/relic/spawn_{k}')
        fn(f'p241/relic/take_{k}', [f'execute unless score @s bm.ars_{k} = #arun bm.p2 run function bm:p241/relic/sigil_{k}'] +
           ([f'execute unless entity @s[tag=bm.arel_{k}] run function bm:p241/relic/first_{k}'] if relic else []) +
           ['playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 0.8 1.2'])
        fn(f'p241/relic/sigil_{k}', [f'scoreboard players operation @s bm.ars_{k} = #arun bm.p2', give('hive_sigil'),
                                     tellraw('@s', [T('A Hive Sigil, ', '#9adf8a', bold=True), T(f'from {title_}. ', 'gray'), T('Six of them open the Hive Vault behind the helm.', 'dark_gray')])])
        if relic:
            fn(f'p241/relic/first_{k}', [f'tag @s add bm.arel_{k}', give(relic),
                                         tellraw('@s', P + [T(f'{title_}: ', '#9adf8a', bold=True), T('you find ', 'gray'), T(RELIC_NAME[relic] + '.', 'white')])])
    fn('p241/relic/click', ['tag @s add bm.ahere', 'execute on target run function bm:p241/relic/take', 'tag @s remove bm.ahere', 'data remove entity @s interaction'])
    fn('p241/relic/take', [f'execute if entity @e[tag=bm.ahere,tag=bm.arel_{k}] run function bm:p241/relic/take_{k}' for k in REL])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.arelic_i] if data entity @s interaction at @s run function bm:p241/relic/click')

    # ================================================================== THE HIVE VAULT (after the fall, six Hive Sigils)
    fn('p241/vault/tick', ['execute if entity @s[tag=bm.open] run return 0',
                           'execute unless score #afell bm.p2 matches 1 if entity @a[distance=..4] run return run ' + title('@a[distance=..4]', 'actionbar', T('A sealed vault behind the helm. Not while its Admiral stands there.', 'gray', italic=True)),
                           'execute as @a[distance=..4,gamemode=!spectator] if items entity @s container.* *[minecraft:custom_data~{bm:"hive_sigil"}] run function bm:p241/vault/count',
                           'execute if score #afell bm.p2 matches 1 as @a[distance=..4,tag=bm.avaultok,limit=1] at @s run function bm:p241/vault/open'])
    fn('p241/vault/count', ['tag @s remove bm.avaultok', 'execute store result score #sc bm.rng run clear @s *[minecraft:custom_data~{bm:"hive_sigil"}] 0',
                            f'execute if score #sc bm.rng matches {A.SIGILS_FOR_VAULT}.. run return run tag @s add bm.avaultok',
                            title('@s', 'actionbar', [T(f'{A.SIGILS_FOR_VAULT} sigil-slots in the vault door. You carry ', 'gray'), {'score': {'name': '#sc', 'objective': 'bm.rng'}, 'color': 'white'}, T('.', 'gray')])])
    fn('p241/vault/open', [f'clear @s *[minecraft:custom_data~{{bm:"hive_sigil"}}] {A.SIGILS_FOR_VAULT}', 'tag @s remove bm.avaultok',
                           'execute as @e[type=minecraft:marker,tag=bm.avault,distance=..6,sort=nearest,limit=1] at @s run function bm:p241/vault/door'])
    fn('p241/vault/door', ['tag @s add bm.open', 'function bm:p241/door/open', 'playsound minecraft:block.vault.open_shutter block @a[distance=..24] ~ ~ ~ 1 0.5',
                           'particle minecraft:end_rod ~ ~2 ~ 1 1.5 1 0.05 40', title('@a[distance=..16]', 'title', T('The Hive Vault', COL, bold=True))])
    second.append('execute as @e[type=minecraft:marker,tag=bm.avault] at @s if entity @a[distance=..6] run function bm:p241/vault/tick')

    # ================================================================== THE INVASION NIGHTS END (and come back when a Dreadnought is attacked)
    G.FUNCS['p32/inv/roll'].insert(1, 'execute if score #vfell bm.cfg matches 1 run return 0')
    G.FUNCS['p148/use/beacon'].insert(0, 'execute if score #vfell bm.cfg matches 1 run return run ' + tellraw('@s', P + [T('The beacon calls into silence. ', COL),
                                                                                                                   T('The fleet\'s Admiral has fallen; nobody is listening.', 'gray', italic=True)]))
    fn('p241/nights_end', ['scoreboard players set #vfell bm.cfg 1', 'execute if score #inv bm.bm matches 1 run function bm:p32/inv/end',
                           tellraw('@a', P + [T('The invasion nights are over. ', COL, bold=True), T('Without its Admiral the fleet has turned away from this world.', 'gray')])])
    # attacking a Dreadnought again: a guardian killed over your world, a reactor's sabotage begun, an Armada twin's reactor broken
    G.FUNCS['p41/vornmet'].insert(1, 'execute if score #vfell bm.cfg matches 1 run function bm:p241/rekindle')
    G.FUNCS['p52/rx/start'].append('execute if score #vfell bm.cfg matches 1 as @a[gamemode=!spectator,distance=..40,sort=nearest,limit=1] at @s run function bm:p241/rekindle')
    G.FUNCS['p32/dread/alarm'].append('execute if score #vfell bm.cfg matches 1 as @a[gamemode=!spectator,gamemode=!creative,distance=..40,sort=nearest,limit=1] at @s run function bm:p241/rekindle')
    fn('p241/rekindle', ['scoreboard players set #vfell bm.cfg 0', 'tag @s remove bm.vxdone',
                         'playsound minecraft:entity.elder_guardian.curse ambient @a ~ ~ ~ 1 0.5',
                         tellraw('@a', P + [T('The hive remembers this world. ', COL, bold=True), T('The invasion nights will come again - and its Admiral will rise for ', 'gray'),
                                            {'selector': '@s', 'color': 'white'}, T('.', 'gray')])])

    # ================================================================== THE STARFORGE (a Warplate piece -> Starforged)
    fn('p241/bench/spawn', ['tag @s add bm.aon', 'summon minecraft:interaction ~ ~-0.5 ~ {Tags:["bm.abench_i"],width:1.2f,height:1.4f,response:1b}',
                            'summon minecraft:text_display ~ ~0.9 ~ ' + snbt({'Tags': ['bm.amapd'], 'billboard': 'center', 'text': [T('THE STARFORGE\n', STAR, bold=True),
                                                                                                                                  T('hold a Warplate piece, carry 2 Star-Cores\nand 8 red Xenite - and right-click', 'gray')],
                                                                         'background': Int(0x60000000), 'brightness': {'block': Int(15), 'sky': Int(15)}})])
    second.append('execute as @e[type=minecraft:marker,tag=bm.abench,tag=!bm.aon] at @s run function bm:p241/bench/spawn')
    fn('p241/bench/click', ['tag @s add bm.ahere', 'execute on target run function bm:p241/bench/use', 'tag @s remove bm.ahere', 'data remove entity @s interaction'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.abench_i] if data entity @s interaction at @s run function bm:p241/bench/click')
    pieces = ('helmet', 'chestplate', 'leggings', 'boots')
    fn('p241/bench/use', ['execute store result score #c bm.rng run clear @s *[minecraft:custom_data~{bm:"star_core"}] 0',
                          'execute store result score #x bm.rng run clear @s *[minecraft:custom_data~{bm:"xenite_red"}] 0',
                          'execute unless score #c bm.rng matches 2.. run return run ' + title('@s', 'actionbar', T('The Starforge wants 2 Star-Cores.', STAR)),
                          'execute unless score #x bm.rng matches 8.. run return run ' + title('@s', 'actionbar', T('The Starforge wants 8 red Xenite.', STAR))] +
       [f'execute if items entity @s weapon.mainhand {holds(f"warplate_{p}")} run return run function bm:p241/bench/forge_{p}' for p in pieces] +
       [title('@s', 'actionbar', T('Hold a Vorn Warplate piece in your hand.', STAR))])
    for p in pieces:
        fn(f'p241/bench/forge_{p}', ['clear @s *[minecraft:custom_data~{bm:"star_core"}] 2', 'clear @s *[minecraft:custom_data~{bm:"xenite_red"}] 8',
                                     f'item replace entity @s weapon.mainhand with {G.item_arg(f"starforged_{p}")}',
                                     'particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.1 40', 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.6 0.4 0.08 20',
                                     'playsound minecraft:block.smithing_table.use player @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.2',
                                     tellraw('@s', P + [T('The Starforge roars. ', STAR, bold=True), T(f'Your Warplate comes back {ITEMS[f"starforged_{p}"]["name"]}.', 'gray')])])

    # ================================================================== THE RELICS AT WORK
    fast.append('execute as @a[gamemode=!spectator] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"squad_jetpack"}] at @s run function bm:p241/relic/jet')
    fn('p241/relic/jet', ['effect give @s minecraft:slow_falling 1 0 true', 'execute if score @s bm.ajet matches 1.. run scoreboard players remove @s bm.ajet 1',
                          'execute if score @s bm.ajet matches 1.. run return 0', 'execute if entity @s[nbt={OnGround:1b}] run return 0',
                          'execute unless predicate bm:p20/sneaking run return 0', 'scoreboard players set @s bm.ajet 25',
                          'effect give @s minecraft:levitation 1 6 true', 'particle minecraft:flame ~ ~ ~ 0.2 0.1 0.2 0.05 20', 'playsound minecraft:entity.firework_rocket.launch player @a[distance=..16] ~ ~ ~ 1 1.2'])
    second.append('execute as @a[gamemode=!spectator] if items entity @s container.* *[minecraft:custom_data~{bm:"hover_collar"}] at @s run function bm:p241/relic/collar')
    import phase125 as P125
    hosts = sorted({v[3] for v in P125.WHO.values()})
    fn('p241/relic/collar', ['scoreboard players operation #me bm.pid = @s bm.pid'] +
       [f'execute as @e[type=minecraft:{h},distance=..16] if score @s bm.pid = #me bm.pid run function bm:p241/relic/collared' for h in hosts])
    fn('p241/relic/collared', ['effect give @s minecraft:speed 3 0 true', 'effect give @s minecraft:resistance 3 0 true'])
    G.consume_adv('hive_override', 'bm:p241/relic/override')
    fn('p241/relic/override', ['advancement revoke @s only bm:consume/hive_override'] + give_back(G.item_arg('hive_override')) + [
                               'execute if score @s bm.aocd matches 1.. run return run ' + title('@s', 'actionbar', T('The chip is still rebooting.', 'gray')),
                               'scoreboard players set @s bm.aocd 60',
                               'execute as @e[tag=bm.vorn,distance=..12] run function bm:p241/relic/frozen',
                               'particle minecraft:electric_spark ~ ~1 ~ 6 1 6 0.2 120', 'playsound minecraft:block.beacon.deactivate player @a[distance=..16] ~ ~ ~ 1 1.6',
                               title('@s', 'actionbar', T('HIVE OVERRIDE: every Vorn near you freezes, confused.', COL, bold=True))])
    fn('p241/relic/frozen', ['effect give @s minecraft:slowness 6 255 true', 'effect give @s minecraft:weakness 6 9 true', 'effect give @s minecraft:glowing 6 0 true'])
    second.append('scoreboard players remove @a[scores={bm.aocd=1..}] bm.aocd 1')
    second.append('execute as @a[gamemode=!spectator] if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"stardust_kite"}] run function bm:p241/relic/kite')
    fn('p241/relic/kite', ['effect give @s minecraft:slow_falling 3 0 true', 'effect give @s minecraft:night_vision 15 0 true'])

    # ================================================================== LOOT
    lt, uni, chance = G.loot_entry, G.uni, G.chance
    pool = lambda entries, rolls=1, cond=None: dict({'rolls': rolls, 'entries': entries}, **({'conditions': cond} if cond else {}))
    it = lambda name, lo=1, hi=1, w=1: dict({'type': 'minecraft:item', 'name': f'minecraft:{name}', 'weight': w},
                                            **({'functions': [{'function': 'minecraft:set_count', 'count': uni(lo, hi)}]} if hi > 1 else {}))
    rare = pool([it('netherite_ingot', w=2), it('diamond', 3, 6, 6), it('enchanted_golden_apple', w=3), it('netherite_upgrade_smithing_template', w=2),
                 it('emerald_block', 2, 4, 5), it('shulker_shell', 2, 4, 3)])
    for nm_, pools in (('ward', [pool([lt('xenite_red', uni(3, 6))]), pool([lt('xenite_green', uni(6, 12))]), rare, pool([lt('power_cell')], cond=[chance(0.4)])]),
                       ('vault', [pool([lt('xenite_red', uni(6, 10))]), rare, rare, pool([lt('star_core')]), pool([lt('trophy', uni(1, 2))])]),
                       ('hidden', [pool([lt('xenite_red', uni(4, 8))]), rare, pool([lt('star_core')], cond=[chance(0.5)]), pool([lt('power_cell', uni(1, 2))])]),
                       ('hoard', [pool([lt('xenite_red', uni(12, 20))]), rare, rare, rare, pool([lt('star_core', uni(2, 4))]),
                                  pool([lt(i) for i in ('starfire_lance', 'hive_breaker', 'singularity_launcher', 'admiral_crown')], cond=[chance(0.4)])]),
                       ('victor', [pool([lt('xenite_red', uni(14, 22))]), rare, rare, pool([lt('star_core', uni(2, 3))]), pool([lt('trophy', uni(3, 5))]),
                                   pool([lt(i) for i in ('starfire_lance', 'hive_breaker', 'singularity_launcher', 'admiral_crown')])])):
        wjson(f'bm/loot_table/p2/{d}/{nm_}.json', {'type': 'minecraft:chest', 'pools': pools})

    # ================================================================== THE BIOME (no spawns; a green-black void)
    wjson('bm/worldgen/biome/armada.json', {
        'attributes': {'minecraft:audio/ambient_sounds': {'mood': {'block_search_extent': 8, 'offset': 2.0, 'sound': 'minecraft:ambient.basalt_deltas.mood', 'tick_delay': 4000}},
                       'minecraft:audio/background_music': {'default': {'sound': {'sound_id': 'bm:music.gv_silence'}, 'min_delay': 12000, 'max_delay': 24000,
                                                                        'replace_current_music': True}},
                       'minecraft:gameplay/natural_mob_spawns': {'argument': {'spawn_costs': {}, 'spawns_by_category': {}}, 'modifier': 'override'},
                       'minecraft:visual/ambient_particles': {'argument': [{'particle': {'type': 'minecraft:end_rod'}, 'probability': 0.0015}], 'modifier': 'override'},
                       'minecraft:visual/fog_color': '#0a1a0c'},
        'carvers': [], 'downfall': 0.0, 'effects': {'water_color': '#3f76e4'}, 'features': [], 'has_precipitation': False, 'temperature': 0.5})

    # ================================================================== ADMIN
    fn('admin/armada/place', ['scoreboard players set #awant bm.p2 1', 'scoreboard players set #aver bm.p2 0', 'scoreboard players set #acol bm.p2 0',
                              tellraw('@s', P + [T('The Vorn Armada will be (re)placed in the End in a few seconds (everyone aboard is beamed out first).', 'gray')])])
    fn('admin/armada/go', [f'execute unless score #aver bm.p2 matches {AVER} run return run ' + tellraw('@s', P + [T('Not placed yet: /function bm:admin/armada/place', 'gray')]),
                           f'execute in {END} run tp @s {dwx + 0.5} {dwy} {dwz + 0.5}'])
    fn('admin/armada/coords', [give('hive_coords'), 'tag @s add bm.acoord', 'scoreboard players set #awant bm.p2 1'])
    fn('admin/armada/fell', ['function bm:p241/nights_end'])
    fn('admin/armada/unfell', ['scoreboard players set #vfell bm.cfg 0', tellraw('@s', P + [T('The invasion nights can come again.', 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/armada/', 'yellow'), T('place | go | coords | fell | unfell', 'yellow'),
                                                T('  the Vorn Armada (hard-mode dungeon in the End): (re)place it, go aboard, the coordinates, end or bring back the invasion nights', 'gray')]))
