"""2.85a: DREAD NIGHTS - the thing that empowered the Dread comes for those who kill them.

THE COUNT      every Dread killed in hard mode is counted (#dkn); when the count passes a threshold rolled between 30 and 70,
               the next night that isn't a Blood Moon is a DREAD NIGHT (it takes the place of a Lucky Night or an invasion).
               At dusk the world goes quiet: no birds, no wind, a warning to everyone in the Overworld. A new threshold is
               rolled when it comes.
THE NIGHT      (13000-23000, the Overworld) the night's monsters walk it as on any night (2.88: they were cleared as they
               spawned, all night long - a strain for nothing), and nobody's followers come out (any that are out go home; calling one says it won't come). A red bar counts to
               dawn; the dark breathes - a heartbeat, whispers, red motes, the light failing now and then. Nobody can sleep.
THE HUNTED     everyone in the Overworld who has beaten the Hollow King. STALKERS come for them (after the owner's drawing:
               tall, thin, sage-olive things, ribs showing, long hooked claws raised, a bald head tipped back over a gaping maw)
               that can't be killed, that rise at least 30 blocks away whatever the light, and that strike through armour,
               Protection, Resistance and shields - three blows kill anyone, whatever they wear (each takes a third of your
               health and absorption). One at first, two after midnight, three before dawn. They're quicker than you walk and
               slower than you sprint (4.8 blocks a second, measured): get far enough away (64 blocks) and they lose you - a
               new one rises 15-30 s later. Stand still and they don't need to walk: after 8 seconds in one spot (a warning
               at 5) one simply steps out of the dark behind you.
               In the dark you see only their shape - there is nothing in their faces.
THE GOLDEN CROSS (Vesper, 1 Dread Token; sneak + use on a floor or a wall)   Stalkers won't come within a 30x30 square of it
               (15 blocks every way) - they're thrown back at its edge, and never rise or step out of the dark inside it.
               Punch it to take it back.
DAWN           the Stalkers come apart. Anyone hunted for most of the night (6 minutes in the Overworld) who didn't die gets
               3 DREAD ESSENCE, and 1 more for every Stalker they outran (up to 3 more).
DREAD ESSENCE  Vesper takes it: 2 for 3 Dread Tokens; 3 for a DREAD BELL (ring it: tonight is a Dread Night); 6 for the
               STALKER'S GRIN (a hat: their face, its empty hollows). 16 tossed down with 4 Dread Tokens forge a DREAD TOTEM.
THE DREAD TOTEM   carried anywhere in your inventory: no monster spawns within 32 blocks of you, and monsters near you won't
               turn on you (nor Dread monsters' Pulse and Mark). It does nothing against Stalkers - only the cross does.
"""
import math
from items import item, hat, T, TOTEM, ITEMS, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase160 as P160
import phase172 as P172
import phase177 as P177
import rigfol as RF
import stalker_art as SA

DREAD, DREAD_D, GOLD = '#b0102a', '#5a0812', '#ffd24a'
ESS = '#d0406a'
holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
SPAWN_MIN, SPAWN_MAX = 30, 40          # (a Stalker rises this far from its quarry)
LOSE = 64                              # (and loses them past this)
CROSS_R = 15                           # (the cross: a 30x30 square, 15 blocks every way)
STILL_WARN, STILL_BLINK = 5, 8         # (seconds standing still: a warning, then one steps out behind you)
HUNTED_MIN = 360                       # (seconds hunted in the Overworld for the dawn's essence: most of the 500 s night)
KIN = set()                            # (2.87: followers' host tags that DO come out on a Dread Night - the Stalker, phase193)
DAWN = []                              # (2.87: lines run as each survivor at dawn, after their essence - phase193's encounter)
STILL = []                             # (2.87: lines run as each hunted player before the standing-still count is read)

# ================================================================== THE ITEMS
item('dread_essence', TOTEM, 'Dread Essence', ESS,
     ['What is left of a night you survived.', ('Vesper takes it.', 'blue'), ('16 tossed down with 4 Dread Tokens', 'gray'),
      ('forge a Dread Totem.', 'gray')], model='bm:dread_essence', stack=64, cat='currency')
item('golden_cross', TOTEM, 'Golden Cross', GOLD,
     ['Old gold, warm in the hand.', ('Sneak + use on a floor or a wall: set it up.', 'blue'),
      ('Stalkers will not come within 15 blocks', 'blue'), ('of it, any way. Punch it to take it back.', 'gray'), ('From Vesper.', 'dark_gray')],
     model='bm:golden_cross', stack=16, cat='builder', comps=hold('none'))
item('dread_bell', TOTEM, 'Dread Bell', DREAD,
     ['A black bell with no clapper. It rings anyway.', ('Ring it (use, 2 s): tonight is a Dread Night.', 'blue'),
      ('Only for those who have beaten the Hollow King,', 'gray'), ('and not on a Blood Moon.', 'gray')],
     model='bm:dread_bell', stack=16, cat='builder',
     comps={'minecraft:consumable': consumable(2.0, 'bow', 'minecraft:block.bell.resonate', False)})
item('dread_totem', TOTEM, 'Dread Totem', DREAD,
     ['It hums when something looks at you.', ('Carried: no monster spawns within 32 blocks,', 'blue'),
      ('and monsters near you will not turn on you.', 'blue'), ('It does nothing against a Stalker.', 'dark_red'),
      ('Forged: 16 Dread Essence and 4 Dread Tokens.', 'gray')], model='bm:dread_totem', stack=1, cat='magic')
hat('stalker_grin', "Stalker's Grin", DREAD, 'bm:stalker_grin', 'minecraft:dust{color:[0.7,0.0,0.05],scale:0.6} ~ ~1.8 ~ 0.15 0.05 0.15 0 1', None,
    ['Their face. Nothing looks out of it.', ('From Vesper, for Dread Essence.', 'dark_gray')])
HOLD['golden_cross'] = 'bm:p181/cross/use'
P160.RECIPES.append(('dtotem', 'Dread Totem', DREAD, ['0.69,0.06,0.16', '0.82,0.25,0.42', '0.2,0.0,0.03'],
                     (holds('dread_essence'), 16), [(holds('dread_token'), 4)], None, None))
P160.RESULT['dtotem'] = 'dread_totem'
P177.STOCK.append(('golden_cross', 1, 1))
P177.EXTRA += [(('dread_essence', 2), ('dread_token', 3)), (('dread_essence', 3), ('dread_bell', 1)), (('dread_essence', 6), ('stalker_grin', 1))]
P172.NOT_REGULAR = tuple(P172.NOT_REGULAR) + ('bm.stalker',)


def ring(r, n, y=0.1):
    return [(round(r * math.cos(2 * math.pi * i / n), 2), y, round(r * math.sin(2 * math.pi * i / n), 2)) for i in range(n)]


def generate(G):
    fn, wjson, title, tellraw, give = G.fn, G.wjson, G.title, G.tellraw, G.give
    import phase179 as P179
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    second, fast = G.FUNCS['loop/second'], G.FUNCS['loop/fast']
    OW = '@a[tag=bm.ow]'
    HUNT = '@a[tag=bm.dnh]'
    objs = ['bm.dnsp', 'bm.dnst', 'bm.dnx', 'bm.dny', 'bm.dnz', 'bm.dnt', 'bm.dnd0', 'bm.dnesc', 'bm.stkc', 'bm.stkr',
            'bm.stkid', 'bm.stka', 'bm.stkf', 'bm.stkx', 'bm.stkz', 'bm.stkd', 'bm.stkw', 'bm.stkp', 'bm.stkwc']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        'execute unless score #dkn bm.cfg matches 0.. run scoreboard players set #dkn bm.cfg 0',
        'execute unless score #dnt bm.cfg matches 1.. store result score #dnt bm.cfg run random value 30..70',
        'execute unless score #dnday bm.bm matches -1.. run scoreboard players set #dnday bm.bm -1',
        'bossbar add bm:dreadnight {text:"Dread Night",color:"dark_red",bold:true}',
        'bossbar set bm:dreadnight color red', 'bossbar set bm:dreadnight style notched_10', 'bossbar set bm:dreadnight max 10000',
        'team add bm.dtot', 'team modify bm.dtot friendlyFire true', 'team modify bm.dtot seeFriendlyInvisibles false',
        'scoreboard players set #k3 bm.rng 3', 'scoreboard players set #m1 bm.rng -1', 'scoreboard players set #k4 bm.rng 4']
    G.OBJECTIVES += objs

    # ================================================================== THE COUNT
    G.FUNCS['p176/dread/killed'] += ['execute if score #hard bm.cfg matches 1 run scoreboard players add #dkn bm.cfg 1',
                                     'execute if score #dkn bm.cfg = #dnt bm.cfg run function bm:p181/counted']
    fn('p181/counted', [title('@s', 'actionbar', [T('It has counted enough. ', DREAD, bold=True), T('Soon.', '#806060', italic=True)]),
                        'playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.5'])

    # ================================================================== THE NIGHT (ticked with the Blood Moon, once a second)
    G.FUNCS['bloodmoon/tick'].append('function bm:p181/tick')
    fn('p181/tick', [
        'execute if score #tod bm.bm matches 11000.. unless score #dnr bm.bm = #day bm.bm run function bm:p181/roll',
        'scoreboard players set #dnwant bm.bm 0',
        'execute if score #dnday bm.bm = #day bm.bm if score #bday bm.bm matches 0 if score #tod bm.bm matches 13000..22999 run scoreboard players set #dnwant bm.bm 1',
        'execute if score #dnwant bm.bm matches 1 unless score #dnight bm.bm matches 1 run function bm:p181/start',
        'execute if score #dnwant bm.bm matches 0 if score #dnight bm.bm matches 1 run function bm:p181/end',
        'execute if score #dnight bm.bm matches 1 run function bm:p181/during',
        'execute if score #dnday bm.bm = #day bm.bm if score #tod bm.bm matches 12000.. as @a if data entity @s sleeping_pos at @s run function bm:p181/wake'])
    fn('p181/roll', ['scoreboard players operation #dnr bm.bm = #day bm.bm',
                     'execute unless score #hard bm.cfg matches 1 run return 0', 'execute if score #bday bm.bm matches 1 run return 0',
                     'execute if score #dnday bm.bm = #day bm.bm run return run function bm:p181/warn',
                     'execute if score #dkn bm.cfg >= #dnt bm.cfg run scoreboard players operation #dnday bm.bm = #day bm.bm',
                     'execute if score #dnday bm.bm = #day bm.bm run function bm:p181/warn'])
    fn('p181/warn', [tellraw(OW, P + [T('The birds have stopped. The wind has stopped. ', '#c8a0a0', italic=True),
                                      T('Tonight is a Dread Night.', DREAD, bold=True)]),
                     tellraw('@a[tag=bm.ow,scores={bm.conq=6..}]', [T('  It is coming for you. ', DREAD), T('Keep moving - or find something holy.', 'gray')]),
                     f'execute as {OW} at @s run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 1 0.5',
                     f'execute as {OW} at @s run playsound minecraft:entity.warden.nearby_closest ambient @s ~ ~ ~ 0.5 0.6'])
    # (a Dread Night takes tonight from a Lucky Night or an invasion)
    for nm, flag in (('p22/lucky/roll', '#lucky'), ('p32/inv/roll', '#ivn')):
        G.FUNCS[nm].insert(1, f'execute if score #dnday bm.bm = #day bm.bm run return run scoreboard players set {flag} bm.bm 0')
    fn('p181/wake', ['tp @s ~ ~0.6 ~', title('@s', 'actionbar', T('You can\'t sleep. Something is watching.', DREAD))])

    # ---- the start
    fn('p181/start', ['scoreboard players set #dnight bm.bm 1', 'scoreboard players set #dkn bm.cfg 0',
                      'execute store result score #dnt bm.cfg run random value 30..70',
                      f'title {OW} times 20 90 40', title(OW, 'title', T('DREAD NIGHT', DREAD, bold=True)),
                      title(OW, 'subtitle', T('It has come for what you took from it. Keep moving.', '#c8a0a0', italic=True)),
                      f'execute as {OW} at @s run playsound minecraft:entity.warden.emerge ambient @s ~ ~-8 ~ 1 0.5',
                      f'execute as {OW} at @s run playsound minecraft:entity.lightning_bolt.thunder ambient @s ~ ~ ~ 0.6 0.4',
                      'effect give @a[tag=bm.ow] minecraft:darkness 6 0 true',
                      f'bossbar set bm:dreadnight players {OW}', 'bossbar set bm:dreadnight visible true',
                      tellraw(OW, P + [T('A Dread Night. Something worse than the dark walks tonight. ', '#c8a0a0'),
                                       T('Those who felled the Hollow King are hunted until dawn.', DREAD, bold=True)]),
                      'scoreboard players set @a bm.dnt 0', 'scoreboard players set @a bm.dnesc 0', 'tag @a remove bm.dnh', 'tag @a remove bm.dnwas'])

    # ---- during: the hunted, the bar, the dark breathing
    fn('p181/during', [
        'scoreboard players operation #prog bm.bm = #tod bm.bm', 'scoreboard players remove #prog bm.bm 13000',
        'execute store result bossbar bm:dreadnight value run scoreboard players get #prog bm.bm', f'bossbar set bm:dreadnight players {OW}',
        # who is hunted: anyone in the Overworld who has beaten the King (and hasn't been put back outside it)
        'tag @a[tag=bm.dnh,tag=!bm.ow] remove bm.dnh',
        'tag @a[tag=bm.dnh,scores={bm.conq=..5}] remove bm.dnh',
        'execute as @a[tag=bm.ow,tag=!bm.dnh,scores={bm.conq=6..},gamemode=!spectator,gamemode=!creative] run function bm:p181/hunt_in',
        f'scoreboard players add {HUNT} bm.dnt 1',
        f'execute as {HUNT} at @s run function bm:p181/hunted',
        f'execute as {OW} at @s run function bm:p181/dark',
        # followers stay in tonight
        *[f'execute as @e[type=minecraft:{e[1]},tag={e[2]},tag=!bm.ffpet] at @s if dimension minecraft:overworld run function bm:p181/fol/{e[0]}'
          for e in P179.FOLLOW.values() if e[2] not in KIN],
        'execute as @e[type=minecraft:zombie,tag=bm.stalker] at @s run function bm:p181/stk/second'])
    fn('p181/hunt_in', ['tag @s add bm.dnh',
                        'execute unless entity @s[tag=bm.dnwas] store result score @s bm.dnd0 run scoreboard players get @s bm.deaths',
                        'execute unless entity @s[tag=bm.dnwas] store result score @s bm.dnsp run random value 10..25',
                        'tag @s add bm.dnwas', 'scoreboard players set @s bm.dnst 0',
                        'execute store result score @s bm.dnx run data get entity @s Pos[0]', 'execute store result score @s bm.dny run data get entity @s Pos[1]',
                        'execute store result score @s bm.dnz run data get entity @s Pos[2]'])
    for e in P179.FOLLOW.values():
        kind, host, tag, iid, go, name, obj, summon = e
        if tag in KIN: continue
        fn(f'p181/fol/{kind}', ['scoreboard players operation #me bm.pid = @s bm.pid',
                                'execute as @a[tag=bm.ow] if score @s bm.pid = #me bm.pid run ' +
                                title('@s', 'actionbar', [T(f'{name} won\'t stay out on a Dread Night - ', '#c8a0a0'), T('home they go.', 'gray')]),
                                f'function bm:{go}'])
        G.FUNCS[summon].insert(0, 'execute if score #dnight bm.bm matches 1 if dimension minecraft:overworld run return run ' +
                               title('@s', 'actionbar', T(f'{name} won\'t come out on a Dread Night.', '#c8a0a0')))
    print(f'2.85a: {len(P179.FOLLOW)} followers kept in on a Dread Night')
    fn('p181/dark', [   # (everyone in the Overworld: red motes, now and then a whisper or the light failing)
        'particle minecraft:dust{color:[0.45,0.0,0.05],scale:1.2} ~ ~2 ~ 10 4 10 0 6 normal @s',
        'execute store result score #dd bm.rng run random value 1..40',
        'execute if score #dd bm.rng matches 1 run playsound minecraft:ambient.cave ambient @s ~ ~ ~ 0.8 0.5',
        'execute if score #dd bm.rng matches 2 run playsound minecraft:entity.warden.nearby_close ambient @s ^ ^ ^-6 0.4 0.5',
        'execute if score #dd bm.rng matches 3 run effect give @s minecraft:darkness 3 0 true',
        'execute if score #dd bm.rng matches 4 run playsound minecraft:ambient.soul_sand_valley.mood ambient @s ~ ~ ~ 1 0.6',
        'execute if score #dd bm.rng matches 5 run playsound minecraft:entity.allay.ambient_without_item ambient @s ^4 ^ ^-3 0.3 0.4'])
    fn('p181/hunted', [
        # standing still: one steps out of the dark behind you (never inside a cross's ground)
        'execute store result score #x bm.rng run data get entity @s Pos[0]', 'execute store result score #y bm.rng run data get entity @s Pos[1]',
        'execute store result score #z bm.rng run data get entity @s Pos[2]',
        'scoreboard players operation #dx bm.rng = #x bm.rng', 'scoreboard players operation #dx bm.rng -= @s bm.dnx',
        'scoreboard players operation #dy bm.rng = #y bm.rng', 'scoreboard players operation #dy bm.rng -= @s bm.dny',
        'scoreboard players operation #dz bm.rng = #z bm.rng', 'scoreboard players operation #dz bm.rng -= @s bm.dnz',
        'execute if score #dx bm.rng matches ..-1 run scoreboard players operation #dx bm.rng *= #m1 bm.rng',
        'execute if score #dy bm.rng matches ..-1 run scoreboard players operation #dy bm.rng *= #m1 bm.rng',
        'execute if score #dz bm.rng matches ..-1 run scoreboard players operation #dz bm.rng *= #m1 bm.rng',
        'scoreboard players operation #dx bm.rng += #dy bm.rng', 'scoreboard players operation #dx bm.rng += #dz bm.rng',
        'execute if score #dx bm.rng matches 2.. run scoreboard players set @s bm.dnst 0',
        'execute if score #dx bm.rng matches ..1 run scoreboard players add @s bm.dnst 1',
        'scoreboard players operation @s bm.dnx = #x bm.rng', 'scoreboard players operation @s bm.dny = #y bm.rng', 'scoreboard players operation @s bm.dnz = #z bm.rng',
        'execute if function bm:p181/in_cross run scoreboard players set @s bm.dnst 0', *STILL,
        f'execute if score @s bm.dnst matches {STILL_WARN} run function bm:p181/still_warn',
        f'execute if score @s bm.dnst matches {STILL_BLINK}.. run function bm:p181/blink',
        # how many are after you; another rises when it's time
        'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #n bm.rng 0',
        'execute as @e[type=minecraft:zombie,tag=bm.stalker] if score @s bm.pid = #me bm.pid run scoreboard players add #n bm.rng 1',
        'scoreboard players set #cap bm.rng 1', 'execute if score #tod bm.bm matches 16000.. run scoreboard players set #cap bm.rng 2',
        'execute if score #tod bm.bm matches 19500.. run scoreboard players set #cap bm.rng 3',
        'execute if score #n bm.rng < #cap bm.rng run scoreboard players remove @s bm.dnsp 1',
        'execute if score #n bm.rng < #cap bm.rng if score @s bm.dnsp matches ..0 run function bm:p181/stk/rise',
        # a heartbeat when one is close
        'execute if score #n bm.rng matches 1.. as @e[type=minecraft:zombie,tag=bm.stalker,distance=..20] if score @s bm.pid = #me bm.pid run tag @s add bm.stkn',
        'execute if entity @e[type=minecraft:zombie,tag=bm.stkn] run playsound minecraft:entity.warden.heartbeat hostile @s ~ ~ ~ 1 0.9',
        'tag @e[type=minecraft:zombie,tag=bm.stkn] remove bm.stkn'])
    fn('p181/still_warn', [title('@s', 'actionbar', T("Don't stand still.", DREAD, bold=True)),
                           'playsound minecraft:entity.warden.nearby_closer hostile @s ^ ^ ^-4 0.7 0.6'])
    fn('p181/in_cross', [f'execute positioned ~-{CROSS_R} ~-{CROSS_R} ~-{CROSS_R} if entity @e[type=minecraft:marker,tag=bm.gcm,'
                         f'dx={2 * CROSS_R},dy={2 * CROSS_R},dz={2 * CROSS_R}] run return 1', 'return 0'])

    # ================================================================== THE STALKERS
    host = {'Tags': ['bm.seen', 'bm.stalker', 'bm.stknew'], 'Silent': B(1), 'PersistenceRequired': B(1), 'CanPickUpLoot': B(0), 'IsBaby': B(0),
            'CanBreakDoors': B(1), 'DeathLootTable': 'minecraft:empty', 'Health': F(1024),
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)},
                               {'id': 'minecraft:resistance', 'amplifier': B(10), 'duration': Int(-1), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0)}],
            'attributes': [{'id': 'minecraft:max_health', 'base': 1024.0}, {'id': 'minecraft:movement_speed', 'base': 0.33},
                           {'id': 'minecraft:follow_range', 'base': 72.0}, {'id': 'minecraft:attack_damage', 'base': 0.0},
                           {'id': 'minecraft:attack_knockback', 'base': 0.0}, {'id': 'minecraft:knockback_resistance', 'base': 1.0},
                           {'id': 'minecraft:step_height', 'base': 1.1}, {'id': 'minecraft:safe_fall_distance', 'base': 64.0},
                           {'id': 'minecraft:spawn_reinforcements', 'base': 0.0}],
            'drop_chances': {'head': F(0), 'chest': F(0), 'legs': F(0), 'feet': F(0), 'mainhand': F(0), 'offhand': F(0)}}
    # (2.88) its body: the Stalker's own rig (stalker_art - the follower's, remodelled after the drawing) at Dread size, its parts
    # standing at the host's feet every tick - it crawls on all fours, sprints flat out, and draws itself up tall and still. (It
    # used to be two stiff displays riding the host, and glided over the ground.)
    SD = 1.2                                                           # (about 3.4 blocks drawn up to its full height)
    psel = lambda p=None: '@e[type=minecraft:item_display,tag=bm.stksel' + (f',tag=bm.stkp_{p}]' if p else ']')
    fn('p181/stk/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(SA, p, ["bm.stkpart", f"bm.stkp_{p}", "bm.stknp"], SD, extra={"view_range": F(2.0)})}'
                        for p in SA.PARTS] +
       ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.stknp,distance=..2] bm.stkid = @s bm.stkid',
        'tag @e[type=minecraft:item_display,tag=bm.stknp,distance=..2] add bm.stksel', 'execute rotated as @s rotated ~ 0 run function bm:p181/stk/place',
        'function bm:p181/stk/pose/stand_a', 'tag @e[tag=bm.stksel] remove bm.stksel', 'tag @e[tag=bm.stknp] remove bm.stknp'])
    fn('p181/stk/place', RF.place(SA, SD / 16, psel))
    GAIT = {'stand_a': 30, 'stand_b': 30, 'scream': 6, 'rend': 3, 'rend_up': 4, **{f'crawl_{k}': 5 for k in range(4)}, **{f'sprint_{k}': 3 for k in range(4)}}
    for nm, dur in GAIT.items():
        fn(f'p181/stk/pose/{nm}', RF.pose(SA, SA.POSES[nm], SD, dur, psel, swap=('head',)))
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #k12 bm.stkf 12', 'scoreboard players set #k20 bm.stkf 20', 'scoreboard players set #k80 bm.stkf 80']
    # every tick: its parts to it; how it moves (looked at every 4 ticks: still - drawn up tall; on the move - on all fours;
    # running you down - flat out) picks the cycle; and a charge through the walls, when it's winding up for one
    fn('p181/stk/tick', ['scoreboard players operation #sid bm.rng = @s bm.stkid',
                         'execute as @e[type=minecraft:item_display,tag=bm.stkpart] if score @s bm.stkid = #sid bm.rng run tag @s add bm.stksel',
                         'execute rotated as @s rotated ~ 0 run function bm:p181/stk/place',
                         'execute if score @s bm.stkp matches 1.. run function bm:p181/stk/phase',
                         'scoreboard players add @s bm.stkf 1',
                         'scoreboard players operation #f bm.rng = @s bm.stkf', 'scoreboard players operation #f bm.rng %= #k4 bm.rng',
                         'execute if score #f bm.rng matches 0 unless score @s bm.stka matches 3.. run function bm:p181/stk/gait',
                         'execute if score @s bm.stka matches 2 run scoreboard players operation #f bm.rng = @s bm.stkf',
                         'execute if score @s bm.stka matches 2 run scoreboard players operation #f bm.rng %= #k12 bm.stkf',
                         *[f'execute if score @s bm.stka matches 2 if score #f bm.rng matches {3 * k} run function bm:p181/stk/pose/sprint_{k}' for k in range(4)],
                         'execute if score @s bm.stka matches 1 run scoreboard players operation #f bm.rng = @s bm.stkf',
                         'execute if score @s bm.stka matches 1 run scoreboard players operation #f bm.rng %= #k20 bm.stkf',
                         *[f'execute if score @s bm.stka matches 1 if score #f bm.rng matches {5 * k} run function bm:p181/stk/pose/crawl_{k}' for k in range(4)],
                         'execute if score @s bm.stka matches 0 run scoreboard players operation #f bm.rng = @s bm.stkf',
                         'execute if score @s bm.stka matches 0 run scoreboard players operation #f bm.rng %= #k80 bm.stkf',
                         'execute if score @s bm.stka matches 0 if score #f bm.rng matches 0 run function bm:p181/stk/pose/stand_a',
                         'execute if score @s bm.stka matches 0 if score #f bm.rng matches 40 run function bm:p181/stk/pose/stand_b',
                         'execute if score @s bm.stka matches 4 run scoreboard players remove @s bm.stkc 1',
                         'execute if score @s bm.stka matches 4 if score @s bm.stkc matches 4 run function bm:p181/stk/pose/rend_up',
                         'execute if score @s bm.stka matches 4 if score @s bm.stkc matches ..0 run scoreboard players set @s bm.stka 0',
                         'tag @e[tag=bm.stksel] remove bm.stksel'])
    # how far it has come in 4 ticks: under 0.12 blocks it stands, under 0.6 it crawls, past that it sprints (a change starts the
    # new cycle from its first frame)
    fn('p181/stk/gait', ['execute store result score #x bm.rng run data get entity @s Pos[0] 100', 'execute store result score #z bm.rng run data get entity @s Pos[2] 100',
                         'scoreboard players operation #dx bm.rng = #x bm.rng', 'scoreboard players operation #dx bm.rng -= @s bm.stkx',
                         'scoreboard players operation #dz bm.rng = #z bm.rng', 'scoreboard players operation #dz bm.rng -= @s bm.stkz',
                         'execute if score #dx bm.rng matches ..-1 run scoreboard players operation #dx bm.rng *= #m1 bm.rng',
                         'execute if score #dz bm.rng matches ..-1 run scoreboard players operation #dz bm.rng *= #m1 bm.rng',
                         'scoreboard players operation #dx bm.rng += #dz bm.rng',
                         'scoreboard players operation @s bm.stkx = #x bm.rng', 'scoreboard players operation @s bm.stkz = #z bm.rng',
                         'scoreboard players set #g bm.rng 0', 'execute if score #dx bm.rng matches 12.. run scoreboard players set #g bm.rng 1',
                         'execute if score #dx bm.rng matches 60.. run scoreboard players set #g bm.rng 2',
                         'execute unless score #g bm.rng = @s bm.stka run scoreboard players set @s bm.stkf -1',
                         'scoreboard players operation @s bm.stka = #g bm.rng'])
    # rising: a spot 30-40 blocks off in a random direction that fits it (on the surface when you're under the sky, near your
    # own height when you aren't), not in a cross's ground - six tries a second
    fn('p181/stk/rise', ['scoreboard players set #rt bm.rng 6', 'tag @s add bm.stko', 'function bm:p181/stk/try', 'tag @s remove bm.stko'])
    fn('p181/stk/try', ['scoreboard players remove #rt bm.rng 1',
                        'summon minecraft:marker ~ ~ ~ {Tags:["bm.stkm"]}',
                        'execute as @e[type=minecraft:marker,tag=bm.stkm,distance=..1,limit=1] store result entity @s Rotation[0] float 1 run random value 0..359',
                        f'execute store result score #rd bm.rng run random value {SPAWN_MIN}..{SPAWN_MAX}',
                        'execute store result storage bm:tmp stk.r int 1 run scoreboard players get #rd bm.rng',
                        'execute as @e[type=minecraft:marker,tag=bm.stkm,distance=..1,limit=1] at @s run function bm:p181/stk/out with storage bm:tmp stk',
                        'scoreboard players set #ok bm.rng 0',
                        'execute as @e[type=minecraft:marker,tag=bm.stkm,limit=1] at @s if predicate bm:sees_sky positioned over motion_blocking_no_leaves '
                        'if function bm:p181/stk/fits run function bm:p181/stk/at',
                        'execute if score #ok bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.stkm,limit=1] at @s run function bm:p181/stk/near',
                        'kill @e[type=minecraft:marker,tag=bm.stkm]',
                        'execute if score #ok bm.rng matches 0 if score #rt bm.rng matches 1.. run function bm:p181/stk/try',
                        'execute if score #ok bm.rng matches 1 store result score @s bm.dnsp run random value 15..30'])
    fn('p181/stk/out', ['$tp @s ^ ^ ^$(r) ~ ~'])
    fn('p181/stk/near', [f'execute positioned ~ ~{dy} ~ if function bm:p181/stk/fits run return run function bm:p181/stk/at' for dy in (0, 1, -1, 2, -2, 3, -3, 4, -4, 6, -6)])
    fn('p181/stk/fits', ['execute if block ~ ~-1 ~ #bm:grap_pass run return 0', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                         'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'execute unless block ~ ~2 ~ #bm:grap_pass run return 0',
                         'execute if block ~ ~ ~ minecraft:water run return 0', 'execute if block ~ ~ ~ minecraft:lava run return 0',
                         f'execute if entity @a[tag=bm.dnh,distance=..{SPAWN_MIN - 1}] run return 0',
                         f'execute unless entity @a[tag=bm.stko,distance=..{LOSE - 8}] run return 0',      # (not down a cliff it would lose you from at once)
                         'execute if function bm:p181/in_cross run return 0', 'return 1'])
    fn('p181/stk/at', ['execute align xz positioned ~0.5 ~ ~0.5 run summon minecraft:zombie ~ ~ ~ ' + snbt(host),
                       'scoreboard players operation @e[type=minecraft:zombie,tag=bm.stknew] bm.pid = #me bm.pid',
                       'execute as @e[type=minecraft:zombie,tag=bm.stknew] at @s run function bm:p181/stk/born',
                       'scoreboard players set #ok bm.rng 1'])
    fn('p181/stk/born', ['tag @s remove bm.stknew', 'scoreboard players set @s bm.stkc 0', 'scoreboard players set @s bm.stkr 0',
                         'scoreboard players add #stkn bm.stkid 1', 'scoreboard players operation @s bm.stkid = #stkn bm.stkid',
                         'scoreboard players set @s bm.stka 0', 'scoreboard players set @s bm.stkf 0', 'scoreboard players set @s bm.stkd 999',
                         'scoreboard players set @s bm.stkw 0', 'scoreboard players set @s bm.stkp 0', 'scoreboard players set @s bm.stkwc 20',
                         'function bm:p181/stk/rig',
                         'damage @s 1 minecraft:player_attack by @a[tag=bm.stko,limit=1]',
                         'playsound minecraft:entity.warden.emerge hostile @a[distance=..48] ~ ~ ~ 0.5 0.6',
                         'particle minecraft:sculk_soul ~ ~1 ~ 0.4 1 0.4 0.02 20',
                         'execute as @a[tag=bm.stko] run ' + title('@s', 'actionbar', T('Something is out there.', DREAD, italic=True))])
    # once a second: it keeps its quarry; loses them if they're too far, gone, or no longer hunted
    fn('p181/stk/second', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.stko',
                           'execute as @a[tag=bm.dnh] if score @s bm.pid = #me bm.pid run tag @s add bm.stko',
                           'execute unless entity @a[tag=bm.stko] run return run function bm:p181/stk/gone',
                           f'execute unless entity @a[tag=bm.stko,distance=..{LOSE}] run return run function bm:p181/stk/lost',
                           'scoreboard players add @s bm.stkr 1',
                           'execute if score @s bm.stkr matches 3.. run damage @s 1 minecraft:player_attack by @a[tag=bm.stko,limit=1]',
                           'execute if score @s bm.stkr matches 3.. run scoreboard players set @s bm.stkr 0',
                           'execute if block ~ ~ ~ minecraft:water run data modify entity @s InWaterTime set value 0',
                           'execute if block ~ ~1 ~ minecraft:water run data modify entity @s InWaterTime set value 0',
                           'function bm:p181/stk/wall_watch', 'tag @a remove bm.stko'])
    # (2.88) THROUGH THE WALLS: a house won't save you. Six seconds without getting any closer (you've walled yourself in, or it
    # can't find the way) and it winds up - three seconds of it, rigid, screaming, the dark gathering round it - then comes
    # straight through whatever is between you, a block a tick, and out beside you. Not into a cross's ground; 30 s between.
    fn('p181/stk/wall_watch', ['scoreboard players remove @s[scores={bm.stkwc=1..}] bm.stkwc 1',
                               'execute if score @s bm.stkp matches 1.. run return 0',
                               'execute store result score #sx bm.rng run data get entity @s Pos[0]', 'execute store result score #sy bm.rng run data get entity @s Pos[1]',
                               'execute store result score #sz bm.rng run data get entity @s Pos[2]',
                               'execute as @a[tag=bm.stko,limit=1] store result score #qx bm.rng run data get entity @s Pos[0]',
                               'execute as @a[tag=bm.stko,limit=1] store result score #qy bm.rng run data get entity @s Pos[1]',
                               'execute as @a[tag=bm.stko,limit=1] store result score #qz bm.rng run data get entity @s Pos[2]',
                               *[l for a_ in ('x', 'y', 'z') for l in (f'scoreboard players operation #s{a_} bm.rng -= #q{a_} bm.rng',
                                                                       f'execute if score #s{a_} bm.rng matches ..-1 run scoreboard players operation #s{a_} bm.rng *= #m1 bm.rng')],
                               'scoreboard players operation #sx bm.rng += #sy bm.rng', 'scoreboard players operation #sx bm.rng += #sz bm.rng',
                               # (within its reach it has you - a wall between doesn't count: pressed to a hut's wall it's still 3 off)
                               'execute if entity @a[tag=bm.stko,distance=..2.2] run return run scoreboard players set @s bm.stkw 0',
                               'scoreboard players operation #best bm.rng = @s bm.stkd', 'scoreboard players remove #best bm.rng 1',
                               'execute if score #sx bm.rng < #best bm.rng run scoreboard players set @s bm.stkw -1',
                               'execute if score #sx bm.rng < #best bm.rng run scoreboard players operation @s bm.stkd = #sx bm.rng',
                               'scoreboard players add @s bm.stkw 1',
                               'execute if score @s bm.stkw matches 6.. if score @s bm.stkwc matches ..0 if score #sx bm.rng matches ..40 '
                               'unless function bm:p181/stk/quarry_crossed run function bm:p181/stk/wind_up'])
    fn('p181/stk/quarry_crossed', ['execute as @a[tag=bm.stko,limit=1] at @s if function bm:p181/in_cross run return 1', 'return 0'])
    fn('p181/stk/wind_up', ['scoreboard players set @s bm.stkp 80', 'scoreboard players set @s bm.stka 3', 'data merge entity @s {NoAI:1b}',
                            'scoreboard players operation #sid bm.rng = @s bm.stkid',
                            'execute as @e[type=minecraft:item_display,tag=bm.stkpart] if score @s bm.stkid = #sid bm.rng run tag @s add bm.stksel',
                            'function bm:p181/stk/pose/scream', 'tag @e[tag=bm.stksel] remove bm.stksel',
                            'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..48] ~ ~ ~ 1.2 0.5',
                            'playsound minecraft:entity.warden.roar hostile @a[distance=..48] ~ ~ ~ 0.8 0.6',
                            'execute as @a[tag=bm.stko] run ' + title('@s', 'actionbar', T('Walls won\'t stop it.', DREAD, bold=True))])
    # (every tick while it charges: 80..21 the wind-up, the dark drawing in; 20..1 through - a block a tick toward you, through
    # anything, till it's beside you; then out, and the chase goes on)
    fn('p181/stk/phase', ['scoreboard players remove @s bm.stkp 1',
                          'scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.stkq',
                          'execute as @a[tag=bm.dnh] if score @s bm.pid = #me bm.pid run tag @s add bm.stkq',
                          'execute unless entity @a[tag=bm.stkq] run return run function bm:p181/stk/phase_end',
                          'execute if score @s bm.stkp matches 21.. run particle minecraft:sculk_soul ~ ~1.4 ~ 0.6 1.0 0.6 0.04 3',
                          'execute if score @s bm.stkp matches 21.. run particle minecraft:large_smoke ~ ~1 ~ 1.2 0.4 1.2 0.01 4',
                          'execute if score @s bm.stkp matches 21 run playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 0.9 0.6',
                          'execute if score @s bm.stkp matches ..20 run particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.6 0.3 0.06 6',
                          'execute if score @s bm.stkp matches ..20 if entity @a[tag=bm.stkq,distance=2.5..] facing entity @a[tag=bm.stkq,limit=1] feet run tp @s ^ ^ ^1',
                          'execute if score @s bm.stkp matches ..20 unless entity @a[tag=bm.stkq,distance=2.5..] run scoreboard players set @s bm.stkp 0',
                          'execute if score @s bm.stkp matches ..0 run function bm:p181/stk/phase_end',
                          'tag @a remove bm.stkq'])
    fn('p181/stk/phase_end', ['scoreboard players set @s bm.stkp 0', 'scoreboard players set @s bm.stka 0', 'scoreboard players set @s bm.stkwc 30',
                              'scoreboard players set @s bm.stkw 0', 'scoreboard players set @s bm.stkd 999', 'data merge entity @s {NoAI:0b}',
                              'scoreboard players set #ok bm.rng 0',
                              'execute at @a[tag=bm.stkq,limit=1] rotated as @a[tag=bm.stkq,limit=1] rotated ~ 0 positioned ^ ^ ^-1.5 if function bm:p181/stk/fits_blink '
                              'run function bm:p181/stk/phase_out',
                              'execute if score #ok bm.rng matches 0 at @a[tag=bm.stkq,limit=1] run function bm:p181/stk/phase_out',
                              'particle minecraft:sculk_soul ~ ~1.3 ~ 0.4 1 0.4 0.03 25',
                              'execute as @a[tag=bm.stkq] at @s run playsound minecraft:entity.warden.emerge hostile @s ~ ~ ~ 1 0.8'])
    fn('p181/stk/phase_out', ['tp @s ~ ~ ~ facing entity @a[tag=bm.stkq,limit=1] feet', 'scoreboard players set #ok bm.rng 1'])

    fn('p181/stk/gone', ['function bm:p181/stk/vanish', 'tag @a remove bm.stko'])
    fn('p181/stk/lost', ['scoreboard players add @a[tag=bm.stko] bm.dnesc 1',
                         'execute as @a[tag=bm.stko] run ' + title('@s', 'actionbar', T('It has lost you. For now.', '#c8a0a0', italic=True)),
                         'function bm:p181/stk/vanish', 'tag @a remove bm.stko'])
    fn('p181/stk/vanish', ['particle minecraft:sculk_soul ~ ~1.3 ~ 0.4 1 0.4 0.03 25', 'particle minecraft:large_smoke ~ ~1.3 ~ 0.3 1 0.3 0.02 15',
                           'playsound minecraft:entity.warden.dig hostile @a[distance=..24] ~ ~ ~ 0.6 1.4',
                           'scoreboard players operation #sid bm.rng = @s bm.stkid',
                           'execute as @e[type=minecraft:item_display,tag=bm.stkpart] if score @s bm.stkid = #sid bm.rng run kill @s',
                           'tp @s ~ -300 ~', 'kill @s'])
    # (and a rig whose Stalker has gone some other way - killed by a command, a chunk unloaded under it - doesn't linger)
    second.append('execute as @e[type=minecraft:item_display,tag=bm.stkpart] at @s unless entity @e[type=minecraft:zombie,tag=bm.stalker,distance=..6] run kill @s')
    # every tick its rig; four times a second the cross throws it back, and it strikes
    G.FUNCS['tick'].append('execute as @e[type=minecraft:zombie,tag=bm.stalker] at @s run function bm:p181/stk/tick')
    fast += ['execute as @e[type=minecraft:zombie,tag=bm.stalker] at @s run function bm:p181/stk/fast']
    fn('p181/stk/fast', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a remove bm.stko',
                         'execute as @a[tag=bm.dnh] if score @s bm.pid = #me bm.pid run tag @s add bm.stko',
                         'execute if score @s bm.stkp matches 1.. run return run tag @a remove bm.stko',
                         'execute if function bm:p181/in_cross run return run function bm:p181/stk/repel',
                         'execute unless score @s bm.dnsp matches 1.. if entity @a[tag=bm.stko,distance=..1.9,gamemode=!creative,gamemode=!spectator] '
                         'run function bm:p181/stk/strike',
                         'execute if score @s bm.dnsp matches 1.. run scoreboard players remove @s bm.dnsp 1',
                         'tag @a remove bm.stko'])
    fn('p181/stk/repel', ['execute facing entity @e[type=minecraft:marker,tag=bm.gcm,sort=nearest,limit=1] feet rotated ~ 0 run tp @s ^ ^ ^-1.4',
                          'particle minecraft:end_rod ~ ~1.4 ~ 0.3 0.8 0.3 0.06 8', 'particle minecraft:large_smoke ~ ~1.4 ~ 0.3 0.8 0.3 0.02 6',
                          'execute store result score #tw bm.rng run random value 1..6',
                          'execute if score #tw bm.rng matches 1 run playsound minecraft:entity.warden.angry hostile @a[distance=..24] ~ ~ ~ 0.6 1.6',
                          'execute if score #tw bm.rng matches 1 as @e[type=minecraft:marker,tag=bm.gcm,sort=nearest,limit=1] at @s run '
                          'playsound minecraft:block.bell.resonate block @a[distance=..24] ~ ~ ~ 0.5 1.8',
                          'tag @a remove bm.stko'])
    # the blow: a third of what you have (health and absorption), through everything - three and you're dead
    fn('p181/stk/strike', ['scoreboard players set @s bm.dnsp 6',
                           'execute as @a[tag=bm.stko,limit=1] at @s run function bm:p181/stk/hit',
                           'playsound minecraft:entity.warden.attack_impact hostile @a[distance=..24] ~ ~ ~ 1.2 0.7',
                           'scoreboard players set @s bm.stka 4', 'scoreboard players set @s bm.stkc 8', 'function bm:p181/stk/strike_pose'])
    fn('p181/stk/strike_pose', ['scoreboard players operation #sid bm.rng = @s bm.stkid',
                                'execute as @e[type=minecraft:item_display,tag=bm.stkpart] if score @s bm.stkid = #sid bm.rng run tag @s add bm.stksel',
                                'function bm:p181/stk/pose/rend', 'tag @e[tag=bm.stksel] remove bm.stksel'])
    fn('p181/stk/hit', ['execute store result score #mh bm.rng run attribute @s minecraft:max_health get 10',
                        'execute store result score #ab bm.rng run data get entity @s AbsorptionAmount 10',
                        'scoreboard players operation #mh bm.rng += #ab bm.rng', 'scoreboard players operation #mh bm.rng /= #k3 bm.rng',
                        'scoreboard players add #mh bm.rng 5',
                        'execute store result storage bm:tmp stk.d float 0.1 run scoreboard players get #mh bm.rng',
                        'function bm:p181/stk/dmg with storage bm:tmp stk',
                        'effect give @s minecraft:blindness 1 0 true', 'effect give @s minecraft:darkness 3 0 true',
                        'particle minecraft:damage_indicator ~ ~1 ~ 0.3 0.4 0.3 0.2 8', 'particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.02 10',
                        'playsound minecraft:entity.player.hurt_sweet_berry_bush player @s ~ ~ ~ 1 0.5'])
    fn('p181/stk/dmg', ['$damage @s $(d) bm:stalker'])
    # stood still too long: the nearest of yours steps out of the dark, three blocks behind you (or where you stand)
    fn('p181/blink', ['scoreboard players set @s bm.dnst 0', 'scoreboard players operation #me bm.pid = @s bm.pid', 'tag @s add bm.stko',
                      'execute as @e[type=minecraft:zombie,tag=bm.stalker,sort=nearest] if score @s bm.pid = #me bm.pid run tag @s add bm.stkb2',
                      'execute unless entity @e[type=minecraft:zombie,tag=bm.stkb2] run return run tag @s remove bm.stko',
                      'scoreboard players set #ok bm.rng 0',
                      'execute rotated ~ 0 positioned ^ ^ ^-3 if function bm:p181/stk/fits_blink run function bm:p181/stk/blink_to',
                      'execute if score #ok bm.rng matches 0 run function bm:p181/stk/blink_to',
                      'tag @e[type=minecraft:zombie,tag=bm.stkb2] remove bm.stkb2', 'tag @s remove bm.stko'])
    fn('p181/stk/fits_blink', ['execute unless block ~ ~ ~ #bm:grap_pass run return 0', 'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'return 1'])
    fn('p181/stk/blink_to', ['tp @e[type=minecraft:zombie,tag=bm.stkb2,sort=nearest,limit=1] ~ ~ ~ facing entity @a[tag=bm.stko,limit=1] feet',
                             'particle minecraft:sculk_soul ~ ~1.3 ~ 0.4 1 0.4 0.03 25', 'particle minecraft:large_smoke ~ ~1.3 ~ 0.3 1 0.3 0.02 15',
                             'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..16] ~ ~ ~ 1 0.6',
                             'execute as @a[tag=bm.stko] run ' + title('@s', 'actionbar', T('Behind you.', DREAD, bold=True)),
                             'scoreboard players set #ok bm.rng 1'])

    # ---- dawn
    fn('p181/end', ['scoreboard players set #dnight bm.bm 0', 'scoreboard players set #dnday bm.bm -1', 'bossbar set bm:dreadnight visible false',
                    'execute as @e[type=minecraft:zombie,tag=bm.stalker] at @s run function bm:p181/stk/vanish',
                    'kill @e[type=minecraft:item_display,tag=bm.stkpart]',
                    tellraw(OW, P + [T('Dawn. The Dread Night lifts - the things in it come apart like smoke.', '#c8a0a0')]),
                    f'execute as {OW} at @s run playsound minecraft:block.beacon.deactivate ambient @s ~ ~ ~ 0.8 0.6',
                    'execute as @a[tag=bm.dnwas] at @s run function bm:p181/reward', 'tag @a remove bm.dnh', 'tag @a remove bm.dnwas'])
    fn('p181/reward', [f'execute unless score @s bm.dnt matches {HUNTED_MIN}.. run return run ' +
                       tellraw('@s', [T('  You weren\'t out in it long enough for anything to be left of it.', 'gray')]),
                       'execute unless score @s bm.deaths = @s bm.dnd0 run return run ' +
                       tellraw('@s', [T('  It took you tonight. ', DREAD), T('Nothing of the night is left for you.', 'gray')]),
                       'execute if score @s bm.dnesc matches 4.. run scoreboard players set @s bm.dnesc 3',
                       'scoreboard players add @s bm.dnesc 3',
                       'execute store result storage bm:tmp dn.n int 1 run scoreboard players get @s bm.dnesc',
                       'function bm:p181/give_ess with storage bm:tmp dn',
                       tellraw('@s', [T('  You survived the Dread Night. ', ESS, bold=True), T('Dread Essence: ', 'gray'),
                                      {'score': {'name': '@s', 'objective': 'bm.dnesc'}, 'color': ESS}]),
                       'playsound minecraft:ui.toast.challenge_complete player @s ~ ~ ~ 0.8 0.7', 'scoreboard players set @s bm.dnesc 0'] + DAWN)
    fn('p181/give_ess', ['$give @s ' + G.item_arg('dread_essence') + ' $(n)'])

    # ================================================================== NO MONSTER RISES near a Dread Totem
    # (2.88: a Dread Night no longer clears every monster as it spawns - the game only spawned more, all night, a strain for
    #  nothing; the night's own monsters walk it now, and the Stalkers hunt among them)
    n = 0
    for t in list(G.ARMORED) + list(G.UNARMORED):
        L = G.FUNCS.get(f'mobs/init/{t}')
        if not L: continue
        L[0:0] = ['execute unless data entity @s Tags if entity @a[tag=bm.dtot,distance=..32] run return run function bm:p181/nospawn']
        n += 1
    assert n >= 20, n
    fn('p181/nospawn', ['tp @s ~ -300 ~', 'kill @s'])

    # ================================================================== THE DREAD TOTEM: carried, monsters near you won't turn on you
    tot = holds('dread_totem')
    second += ['tag @a remove bm.dtot',
               f'execute as @a[gamemode=!spectator] if items entity @s container.* {tot} run tag @s add bm.dtot',
               f'execute as @a[gamemode=!spectator] if items entity @s weapon.offhand {tot} run tag @s add bm.dtot',
               'execute as @a[tag=bm.dtot,team=] run function bm:p181/tot/in',
               'execute as @a[tag=bm.dtj,tag=!bm.dtot] run function bm:p181/tot/out',
               f'execute as @a[tag=bm.dtot,team=bm.dtot] at @s as @e[type=#bm:hostile,distance=..24,team=,tag=!bm.stalker,tag=!bm.boss,tag=!bm.npc] run function bm:p181/tot/calm',
               'execute as @e[tag=bm.dtm] at @s unless entity @a[tag=bm.dtot,distance=..32] run function bm:p181/tot/stir',
               'scoreboard players add #dtc bm.rng 1', 'execute if score #dtc bm.rng matches 60.. run function bm:p181/tot/tidy']
    fn('p181/tot/in', ['team join bm.dtot @s', 'tag @s add bm.dtj'])
    fn('p181/tot/out', ['team leave @s', 'tag @s remove bm.dtj'])
    fn('p181/tot/calm', ['team join bm.dtot @s', 'tag @s add bm.dtm'])
    fn('p181/tot/stir', ['team leave @s', 'tag @s remove bm.dtm'])
    # (a minute at a time the team is emptied and refilled - so the dead don't pile up in it)
    fn('p181/tot/tidy', ['scoreboard players set #dtc bm.rng 0', 'team empty bm.dtot',
                         'execute as @a[tag=bm.dtj] run team join bm.dtot @s', 'execute as @e[tag=bm.dtm] run team join bm.dtot @s'])
    # (nor a Dread monster's Pulse or Mark)
    th = G.FUNCS['p176/dread/think']
    th[:] = [l.replace('gamemode=!creative,gamemode=!spectator]', 'gamemode=!creative,gamemode=!spectator,tag=!bm.dtot]') for l in th]

    # ================================================================== THE DREAD BELL
    G.consume_adv('dread_bell', 'bm:p181/bell')
    fn('p181/bell', ['advancement revoke @s only bm:consume/dread_bell',
                     'execute unless score #hard bm.cfg matches 1 run return run function bm:p181/bell_no',
                     'execute unless score @s bm.conq matches 6.. run return run function bm:p181/bell_no',
                     'execute if score #bday bm.bm matches 1 run return run function bm:p181/bell_no',
                     'execute if score #dnday bm.bm = #day bm.bm run return run function bm:p181/bell_no',
                     'execute if score #tod bm.bm matches 23000.. run return run function bm:p181/bell_no',
                     'scoreboard players operation #dnday bm.bm = #day bm.bm', 'scoreboard players operation #dnr bm.bm = #day bm.bm',
                     'scoreboard players set #lucky bm.bm 0', 'scoreboard players set #ivn bm.bm 0',
                     'execute if score #lnight bm.bm matches 1 run function bm:p22/lucky/end', 'execute if score #inv bm.bm matches 1 run function bm:p32/inv/end',
                     'playsound minecraft:block.bell.use player @a[distance=..48] ~ ~ ~ 1.5 0.5',
                     'playsound minecraft:entity.warden.roar ambient @a[distance=..64] ~ ~ ~ 0.4 0.5',
                     'particle minecraft:sculk_soul ~ ~1.5 ~ 0.6 0.6 0.6 0.04 30',
                     'execute unless score #tod bm.bm matches 13000.. run function bm:p181/warn',
                     tellraw('@s', P + [T('The bell rings with no clapper. ', '#c8a0a0', italic=True), T('Tonight, it hunts.', DREAD, bold=True)])])
    fn('p181/bell_no', [give('dread_bell'), say('The bell will not ring - not tonight, not for you.', DREAD),
                        'playsound minecraft:block.bell.resonate player @s ~ ~ ~ 0.6 0.4'])

    # ================================================================== THE GOLDEN CROSS (a floor or a wall)
    ident = [F(0), F(0), F(0), F(1)]
    def cross_disp(tag_extra, model, rot, t):
        return {'Tags': ['bm.gcd', 'bm.gcnew'] + tag_extra, 'item_display': 'fixed',
                'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': model}},
                'transformation': {'left_rotation': rot, 'right_rotation': ident, 'translation': [F(v) for v in t], 'scale': [F(0.9)] * 3},
                'brightness': {'block': Int(15), 'sky': Int(15)}}
    fn('p181/cross/use', ['execute unless predicate bm:p20/sneaking run return run ' + say('Sneak + use on a floor or a wall to set it up.'),
                          'scoreboard players set #placed bm.rng 0', 'scoreboard players set #ray bm.rng 25',
                          'execute anchored eyes positioned ^ ^ ^ run function bm:p181/cross/ray',
                          'execute if score #placed bm.rng matches 0 run return run ' + say('Look at a floor or a wall within 5 blocks.'),
                          'execute unless entity @s[gamemode=creative] run item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}'])
    fn('p181/cross/ray', ['execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:p181/cross/hit',
                          'scoreboard players remove #ray bm.rng 1', 'execute if score #ray bm.rng matches 1.. positioned ^ ^ ^0.2 run function bm:p181/cross/ray'])
    # (the cell the ray came from decides: above the block hit - the floor; beside it - that wall)
    fn('p181/cross/hit', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.gch"]}', 'execute as @e[type=minecraft:marker,tag=bm.gch,limit=1] at @s align xyz run tp @s ~0.5 ~0.5 ~0.5',
                          'execute positioned ^ ^ ^-0.2 align xyz positioned ~0.5 ~0.5 ~0.5 run function bm:p181/cross/from',
                          'kill @e[type=minecraft:marker,tag=bm.gch]'])
    # (a wall north of the cell faces the cross south, and so on; the display's +z is its back, against the wall)
    back = lambda off: ' '.join('~' + ('' if c == '~' else str(-int(c[1:]))) for c in off.split())
    walls = [('n', '~ ~ ~-1', 0, (0, 0.5, 0.42)), ('s', '~ ~ ~1', 180, (0, 0.5, 0.42)), ('w', '~-1 ~ ~', 270, (0, 0.5, 0.42)), ('e', '~1 ~ ~', 90, (0, 0.5, 0.42))]
    fn('p181/cross/from', ['execute unless block ~ ~ ~ #minecraft:replaceable run return 0',
                           'execute if entity @e[type=minecraft:marker,tag=bm.gcm,distance=..0.6] run return 0',
                           'execute positioned ~ ~-1 ~ if entity @e[type=minecraft:marker,tag=bm.gch,distance=..0.1] positioned ~ ~1 ~ run return run function bm:p181/cross/floor'] +
       [f'execute positioned {off} if entity @e[type=minecraft:marker,tag=bm.gch,distance=..0.1] positioned {back(off)} run return run function bm:p181/cross/wall_{d}' for d, off, _y, _t in walls])
    # (2.88: and back to the open cell before it's set up - the check's step down / into the wall used to carry on into the
    #  placing, and the cross went into the block under it, or into the wall)
    fn('p181/cross/floor', [f'summon minecraft:item_display ~ ~-0.5 ~ {snbt(cross_disp([], "bm:golden_cross", ident, (0, 0.45, 0)))}',
                            'execute positioned ~ ~-0.5 ~ run function bm:p181/cross/set'])
    for d, _off, yaw, t in walls:
        fn(f'p181/cross/wall_{d}', [f'summon minecraft:item_display ~ ~-0.5 ~ {snbt(cross_disp([], "bm:golden_cross_wall", ident, t))}',
                                    f'execute positioned ~ ~-0.5 ~ run rotate @e[type=minecraft:item_display,tag=bm.gcnew,limit=1] {yaw} 0',
                                    'execute positioned ~ ~-0.5 ~ run function bm:p181/cross/set'])
    fn('p181/cross/set', ['summon minecraft:interaction ~ ~ ~ {Tags:["bm.gci","bm.gcnew"],width:0.7f,height:1.0f,response:1b}',
                          'summon minecraft:marker ~ ~ ~ {Tags:["bm.gcm","bm.gcnew"]}', 'tag @e[tag=bm.gcnew] remove bm.gcnew',
                          'scoreboard players set #placed bm.rng 1',
                          'playsound minecraft:block.bell.resonate block @a[distance=..16] ~ ~ ~ 0.6 1.8',
                          'playsound minecraft:block.amethyst_block.place block @a[distance=..16] ~ ~ ~ 1 1.2',
                          'particle minecraft:end_rod ~ ~0.8 ~ 0.2 0.4 0.2 0.04 12'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.gci] if data entity @s attack at @s run function bm:p181/cross/pick',
             'execute as @e[type=minecraft:interaction,tag=bm.gci] if data entity @s interaction run data remove entity @s interaction']
    fn('p181/cross/pick', [f'execute on attacker run {give("golden_cross")}', 'kill @e[type=minecraft:item_display,tag=bm.gcd,distance=..0.7]',
                           'kill @e[type=minecraft:marker,tag=bm.gcm,distance=..0.6]', 'playsound minecraft:block.amethyst_block.break block @a[distance=..16] ~ ~ ~ 1 1.2',
                           'kill @s'])
    # (by night its light shows; on a Dread Night the ground it keeps glows at the edges now and then)
    second += ['execute if score #tod bm.bm matches 13000..22999 as @e[type=minecraft:marker,tag=bm.gcm] at @s if entity @a[distance=..48] run function bm:p181/cross/glow']
    fn('p181/cross/glow', ['particle minecraft:end_rod ~ ~0.9 ~ 0.15 0.3 0.15 0.01 2', 'particle minecraft:wax_on ~ ~0.8 ~ 0.3 0.3 0.3 0 2'] +
       [f'execute if score #dnight bm.bm matches 1 run particle minecraft:dust{{color:[1.0,0.85,0.3],scale:1.5}} ~{x} ~0.3 ~{z} 0.2 0.2 0.2 0 1'
        for x, z in ((-CROSS_R, -CROSS_R), (CROSS_R, -CROSS_R), (-CROSS_R, CROSS_R), (CROSS_R, CROSS_R), (0, -CROSS_R), (0, CROSS_R), (-CROSS_R, 0), (CROSS_R, 0))])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.gci]', 'kill @e[tag=bm.gcd]', 'kill @e[tag=bm.gcm]', 'kill @e[tag=bm.stalker]', 'kill @e[tag=bm.stkpart]',
                                       'team remove bm.dtot', 'bossbar remove bm:dreadnight']

    # ================================================================== the Stalker's blow, by name
    import json, os
    wjson('bm/damage_type/stalker.json', {'exhaustion': 0.0, 'message_id': 'bm.stalker', 'scaling': 'never', 'effects': 'hurt'})
    for tg in ('bypasses_armor', 'bypasses_enchantments', 'bypasses_shield', 'bypasses_effects', 'bypasses_resistance'):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:stalker'] + ['bm:stalker']})

    # ================================================================== operators
    fn('admin/dread_night', ['scoreboard players operation #dnday bm.bm = #day bm.bm', 'scoreboard players operation #dnr bm.bm = #day bm.bm',
                             'execute unless score #tod bm.bm matches 13000..22999 run time set 13000',
                             tellraw('@s', P + [T('A Dread Night falls. ', DREAD, bold=True), T('(It ends at dawn. Those who beat the Hollow King are hunted.)', 'gray')])])
    fn('admin/dread_kit', [give('golden_cross', 4), give('dread_bell', 2), give('dread_essence', 16), give('dread_totem'), give('stalker_grin')])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/dread_night', 'yellow'), T('  a Dread Night now; ', 'gray'),
                                                    T('/function bm:admin/dread_kit', 'yellow'), T('  crosses, bells, essence, totem, grin', 'gray')]))


# ================================================================== THE ART
def textures():
    """the Stalker's Grin's face, after the owner's drawing: sage-olive skin with a darker shadow side, a bald brow, two small
    black eyes red at the centre (2.88), and a maw - dark red, ringed with jagged teeth"""
    from PIL import Image, ImageDraw
    import random
    rnd = random.Random(2085)
    T_ = {}
    LIGHT, MID, DARK, LINE = (188, 190, 148), (160, 164, 112), (133, 138, 84), (34, 36, 22)

    def skin(base, edge=True):
        im = Image.new('RGBA', (16, 16)); px = im.load()
        for y in range(16):
            for x in range(16):
                v = rnd.randint(-5, 5)
                px[x, y] = tuple(max(0, min(255, c + v)) for c in base) + (255,)
        if edge:                                                   # (the drawing's ink line, faintly, round each face)
            for k in range(16):
                for (x, y) in ((k, 0), (k, 15), (0, k), (15, k)):
                    px[x, y] = tuple(int(c * 0.72) for c in px[x, y][:3]) + (255,)
        return im
    T_['stk_skin'] = skin(LIGHT)
    T_['stk_shade'] = skin(DARK)
    ribs = skin(LIGHT); d = ImageDraw.Draw(ribs)
    for y in (4, 7, 10):                                           # ribs down each side, the breastbone, a navel
        d.line((1, y, 5, y + 1), fill=DARK); d.line((14, y, 10, y + 1), fill=DARK)
    d.line((5, 2, 7, 3), fill=LINE); d.line((10, 2, 8, 3), fill=LINE)            # collarbones
    d.line((7, 3, 7, 9), fill=MID)
    ribs.putpixel((7, 13), LINE + (255,)); ribs.putpixel((8, 13), DARK + (255,))
    T_['stk_ribs'] = ribs
    face = skin(LIGHT, edge=False); px = face.load()               # a blank face: smooth, no brow, no nose - only the hollows (their own boxes)
    for y in range(16):                                            # (sunken under the cheekbones and round the sockets, paler down the middle)
        for x in range(16):
            dx = abs(x - 7.5)
            k = 1.0 + 0.05 * (1 - dx / 8) - (0.1 if 10 <= y <= 14 and 2 <= dx <= 6 else 0) - (0.12 if 3 <= y <= 11 and 2 <= dx <= 6 else 0)
            px[x, y] = tuple(max(0, min(255, int(c * k))) for c in px[x, y][:3]) + (255,)
    T_['stk_face'] = face
    teeth = skin(LIGHT); d = ImageDraw.Draw(teeth)                 # the upper jaw's front: lip above, jagged teeth hanging
    d.rectangle((0, 7, 15, 15), fill=(70, 14, 20, 255))
    for x in range(0, 16, 3):
        d.polygon([(x, 7), (x + 3, 7), (x + 1, 14)], fill=(222, 214, 176))
    d.line((0, 6, 15, 6), fill=LINE)
    T_['stk_teeth'] = teeth
    maw = Image.new('RGBA', (16, 16)); px = maw.load()
    for y in range(16):
        for x in range(16):
            v = rnd.randint(-10, 10)
            px[x, y] = (96 + v, 18 + v // 3, 26 + v // 3, 255)
    d = ImageDraw.Draw(maw)
    d.ellipse((4, 6, 11, 13), fill=(52, 6, 12, 255))               # the throat
    for x in range(0, 16, 2):                                      # lower teeth, pointing up
        d.polygon([(x, 15), (x + 2, 15), (x + 1, 11)], fill=(222, 214, 176))
    for (x, y) in ((5, 3), (9, 4), (12, 2)):                       # drool
        d.line((x, y, x, y + 4), fill=(200, 190, 200, 255))
    T_['stk_maw'] = maw
    claw = skin(DARK, edge=False); d = ImageDraw.Draw(claw)
    for x in range(16):
        claw.putpixel((x, 15), LINE + (255,))
    T_['stk_claw'] = claw
    eye = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(eye)   # (2.88, as drawn) a small round black eye, red at the centre
    d.ellipse((0, 0, 15, 15), fill=(58, 60, 36, 255)); d.ellipse((2, 2, 13, 13), fill=(8, 6, 6, 255)); d.ellipse((6, 5, 9, 8), fill=(208, 24, 24, 255))
    T_['stk_eye'] = eye
    return T_


CUBE = None                            # (gen_rp's cube, set by rp())


def _b(fr, to, tex, rot=None, light=0, full=False):
    e = CUBE(fr, to, tex)
    if full:
        e['faces'] = {s: {'uv': [0, 0, 16, 16], 'texture': '#' + tex} for s in e['faces']}
    if rot: e['rotation'] = rot
    if light: e['light_emission'] = light
    return e


def stalker_models():
    """the Stalker's Grin (its face, worn as a hat). (2.88: the Stalker itself is stalker_art's rig now, the follower's - its
    two old stiff display models are gone)"""
    # the hat: its face, worn over yours, the maw hanging open at your chin
    grin = [_b((3.4, 8.0, 2.9), (12.6, 15.6, 3.6), 'stk_skin'), _b((3.41, 8.0, 2.88), (12.59, 15.6, 2.9), 'stk_face', full=True),
            _b((3.6, 5.0, 2.4), (12.4, 8.0, 3.6), 'stk_skin'), _b((3.61, 5.0, 2.38), (12.39, 8.0, 2.4), 'stk_teeth', full=True),
            _b((3.8, 2.4, 1.6), (12.2, 3.4, 3.6), 'stk_shade'), _b((3.9, 3.4, 1.7), (12.1, 3.42, 3.4), 'stk_maw', full=True),
            _b((4.2, 10.6, 2.8), (6.2, 12.6, 2.88), 'stk_eye', full=True), _b((9.8, 10.6, 2.8), (11.8, 12.6, 2.88), 'stk_eye', full=True),
            _b((3.0, 14.4, 2.9), (13.0, 15.8, 13.0), 'stk_skin'), _b((3.0, 8.0, 12.4), (13.0, 15.8, 13.0), 'stk_shade')]
    return {'stalker_grin': grin}


def cross_models():
    g, w = 'minecraft:block/gold_block', 'minecraft:block/quartz_block_top'
    stand = [_b((5, 0, 5), (11, 1.5, 11), 'g'), _b((6, 1.5, 6), (10, 2.5, 10), 'g')]
    cross = [_b((7, 2.5, 7), (9, 15.5, 9), 'g'), _b((3.5, 10, 7), (12.5, 12, 9), 'g'),
             _b((7.4, 10.4, 6.8), (8.6, 11.6, 9.2), 'w', light=15)]
    tex = {'g': g, 'w': w, 'particle': g}
    wall = [dict(e) for e in cross]
    for e in wall:                                                 # (against a wall: flat to it, lifted to the middle of the face)
        e['from'] = [e['from'][0], e['from'][1] - 1.5, e['from'][2]]; e['to'] = [e['to'][0], e['to'][1] - 1.5, e['to'][2]]
    return {'golden_cross': (tex, stand + cross), 'golden_cross_wall': (tex, wall)}


def rp(R):
    import sys
    from PIL import Image, ImageDraw
    global CUBE
    CUBE = R.cube
    R.LANG.update({'death.attack.bm.stalker': '%1$s was taken by a Stalker', 'death.attack.bm.stalker.player': '%1$s was taken by a Stalker while fleeing %2$s'})
    R.TEXTURE_MODS.append(sys.modules[__name__])
    g = R.grid
    R.ICONS['dread_essence'] = g(['................', '......kkkk......', '......kWWk......', '.......kk.......', '.....kkkkkk.....', '....kRrrrrRk....', '...kRrppprrRk...',
                                  '...kRrpPPprRk...', '...kRrpPPprRk...', '...kRrrpprrRk...', '...kRrrrrrrRk...', '....kRrrrrRk....', '.....kkkkkk.....', '................',
                                  '................', '................'],
                                 dict(k='#1a0205', W='#c8c0b0', R='#5a0812', r='#b0102a', p='#d0406a', P='#ffc0d0'))
    R.ICONS['dread_bell'] = g(['................', '.......kk.......', '......kRRk......', '.....kRrrRk.....', '....kRrrrrRk....', '....kRrrrrRk....', '....kRrrrrRk....',
                               '...kRrrrrrrRk...', '...kRrrrrrrRk...', '..kRrrrrrrrrRk..', '..kkkkkkkkkkkk..', '.......ee.......', '................', '................',
                               '................', '................'],
                              dict(k='#0a0204', R='#2a0a10', r='#4a1018', e='#ff2a20'))
    R.ICONS['dread_totem'] = g(['................', '.....kkkkkk.....', '....kRRRRRRk....', '....kReRReRk....', '....kRRRRRRk....', '....kRkkkkRk....', '.....kRRRRk.....',
                                '..kkkkRrrRkkkk..', '..kRRkRrrRkRRk..', '...kkkRrrRkkk...', '.....kRrrRk.....', '.....kRppRk.....', '.....kRrrRk.....', '......kRRk......',
                                '.......kk.......', '................'],
                               dict(k='#0a0204', R='#3a0a14', r='#7a1424', e='#ff2a20', p='#d0406a'))

    def post(R2):
        for name, els in stalker_models().items():
            used = sorted({f['texture'][1:] for e in els for f in e['faces'].values()})
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': dict({t: f'bm:block/{t}' for t in used}, particle='bm:block/stk_skin'), 'elements': els,
                                                          **({'display': R.GUI_3D} if name == 'stalker_grin' else {})})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
        for name, (tex, els) in cross_models().items():
            R2.wj(f'assets/bm/models/item/{name}.json', {'textures': tex, 'elements': els,
                                                          'display': {'gui': {'rotation': [20, -30, 0], 'translation': [0, 0, 0], 'scale': [0.8, 0.8, 0.8]},
                                                                      'ground': {'scale': [0.4, 0.4, 0.4]},
                                                                      'thirdperson_righthand': {'rotation': [0, 90, 0], 'translation': [0, 1, 1], 'scale': [0.4, 0.4, 0.4]},
                                                                      'firstperson_righthand': {'rotation': [0, 90, 0], 'scale': [0.4, 0.4, 0.4]}}})
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'bm:item/{name}'}})
    R.POST.append(post)
