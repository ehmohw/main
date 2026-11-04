"""3.1: RIDING A KAIJU - phase249's mount (the Atomic Rex's) for any big rig: Talus, Trivyrn (and whatever comes). A follower's
menu's Ride sends the follower home and brings this: an invisible, tamed, saddled horse host scaled so its rider sits on the rig's
seat, the rig (at its full size) placed on it every tick and turned with it, posed by its gait - sat with nobody aboard, still,
walking, running (the rider's own inputs, phase249's predicates). The owner drives; anyone else is thrown off; sneak gets off -
and the follower is back beside you. At RETREAT health it goes home hurt. The follower's item used while riding: the rider's
move by where they look - level (or up a little): `level`, down past 50: `down`, up past 60: `up` (each a function of the
follower's, with its cooldown). No real block is ever touched.

build(G, K) - K: key (a short name: its tags bm.kr<key>...), pfx (the follower's), art (its rig: PIVOT, PARENT, PARTS, PART_K,
HIDDEN, model_name, POSES), scale (the rig's full size), seat (y, z: blocks from the rig's origin to the seat, in its ride pose),
hp, walk, run (speeds), poses (sit, idle, walk [..], run [..]), moves ({level|down|up: (function, cooldown s)}), follower_back
(the follower's try_summon, run as the owner), col / name (its words). Returns the functions the follower calls: ride (as the
player, at them: call it, mount), riding (1 if the player rides their own), use (as the riding player: the move)."""
from nbt import snbt, B, F, Int, D
from items import T
import rigfol as RF

HORSE_ATTACH = 1.44375                       # (EntityTypes HORSE passengerAttachments(1.44375f), scaled with the horse - phase249)


def build(G, K):
    fn, title = G.fn, G.title
    key, pfx, A, S = K['key'], K['pfx'], K['art'], K['scale']
    seat_y, seat_z = K['seat']
    hostsc = round(seat_y / HORSE_ATTACH, 4)
    pre = f'p{pfx[1:]}/kr'                   # (its functions: p273/kr/...)
    tag, ptag, sel = f'bm.kr{key}', f'bm.kr{key}p', f'bm.kr{key}sel'
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = [f'bm.kr{key}{o}' for o in ('id', 'o', 's', 't', 'w', 'c')]
    oid, oo, os_, ot, ow, oc = objs
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    psel = lambda p=None: f'@e[type=minecraft:item_display,tag={sel}' + (f',tag={ptag}_{p}]' if p else ']')
    say = lambda txt: title('@s', 'actionbar', [T(f'{K["name"]}: ', K['col'], bold=True), T(txt, 'gray')])
    snd = lambda s, v=1.2, p=0.6: f'playsound minecraft:{s} neutral @a[distance=..32] ~ ~ ~ {v} {p}'
    # ---- the rig: its poses (at its full size), its place, its parts summoned at the host
    used = [K['poses']['sit'], K['poses']['idle']] + list(K['poses']['walk']) + list(K['poses']['run'])
    keep = tuple(p for p in A.PARTS if not A.HIDDEN(p, A.POSES[K['poses']['sit']]))      # (the parts it stands in: its fx are a follower's, not a mount's)
    for name in dict.fromkeys(used):
        fn(f'{pre}/pose/{name}', RF.pose(A, A.POSES[name], S, 6, psel, parts=keep))
    fn(f'{pre}/place', [l for l, p in zip(RF.place(A, S / 16, psel), A.PIVOT) if p in keep])
    fn(f'{pre}/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, [ptag, f"{ptag}_{p}", f"{ptag}n"], S, model=A.model_name(p, A.POSES[K["poses"]["sit"]]), extra=dict(view_range=F(4.0)))}'
                      for p in A.PARTS if not A.HIDDEN(p, A.POSES[K['poses']['sit']])])
    saddle = {'id': 'minecraft:saddle', 'count': Int(1), 'components': {
        'minecraft:equippable': {'slot': 'saddle', 'asset_id': 'bm:skiff_none', 'equip_sound': 'minecraft:entity.horse.saddle', 'allowed_entities': 'minecraft:horse'}}}
    at = lambda a, v: {'id': f'minecraft:{a}', 'base': D(v)}
    host = {'Tags': [tag, f'{tag}new', 'bm.seen'], 'Tame': B(1), 'PersistenceRequired': B(1), 'Silent': B(1), 'Age': Int(0),
            'CustomName': T(K['name'], K['col'], bold=True), 'CustomNameVisible': B(0), 'DeathLootTable': 'minecraft:empty',
            'equipment': {'saddle': saddle}, 'drop_chances': {'saddle': F(0)}, 'Health': F(K['hp']),
            'attributes': [at('max_health', K['hp']), at('scale', hostsc), at('movement_speed', 0.0), at('jump_strength', 0.8), at('step_height', 1.5),
                           at('fall_damage_multiplier', 0.0), at('safe_fall_distance', 24), at('knockback_resistance', 1.0), at('armor', 10)],
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0), 'show_icon': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0), 'show_icon': B(0)}]}
    # ---- RIDE (as the player, at them): it comes, saddled, and you're on it
    fn(f'{pre}/ride', ['execute unless function bm:p249/allowed run return run ' + say('(it won\'t carry you here - not in a dungeon, a market, the vault or a heist)'),
                       'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                       f'scoreboard players add #kr{key} {oid} 1', f'scoreboard players operation @s {oo} = #kr{key} {oid}',
                       f'execute rotated ~ 0 run summon minecraft:horse ~ ~ ~ {snbt(host)}',
                       f'execute as @e[type=minecraft:horse,tag={tag}new,distance=..2,limit=1] at @s run function bm:{pre}/born',
                       f'ride @s mount @e[type=minecraft:horse,tag={tag},distance=..3,sort=nearest,limit=1]',
                       snd('entity.ravager.roar', 1.4, 0.6)])
    fn(f'{pre}/born', ['execute rotated as @a[distance=..2,sort=nearest,limit=1] run tp @s ~ ~ ~ ~ 0',
                       f'scoreboard players operation @s {oid} = #kr{key} {oid}', 'data modify entity @s Owner set from entity @a[distance=..2,sort=nearest,limit=1] UUID',
                       'scoreboard players operation @s bm.pid = @a[distance=..2,sort=nearest,limit=1] bm.pid',
                       f'scoreboard players set @s {os_} 0', f'scoreboard players set @s {ow} 99', f'scoreboard players set @s {ot} 0',
                       f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^-{seat_z} run function bm:{pre}/rig',
                       f'scoreboard players operation @e[type=minecraft:item_display,tag={ptag}n] {oid} = @s {oid}', f'tag @e[type=minecraft:item_display,tag={ptag}n] remove {ptag}n',
                       f'tag @s remove {tag}new', 'particle minecraft:poof ~ ~1 ~ 1.5 0.6 1.5 0.05 30'])
    # ---- each tick: its rider (the owner drives - anyone else off), its gait, its pose, its rig placed
    tick.append(f'execute as @e[type=minecraft:horse,tag={tag}] at @s run function bm:{pre}/tick')
    walk, run = list(K['poses']['walk']), list(K['poses']['run'])
    fn(f'{pre}/tick', [f'scoreboard players operation #me {oid} = @s {oid}',
                       f'execute as @e[type=minecraft:item_display,tag={ptag}] if score @s {oid} = #me {oid} run tag @s add {sel}',
                       'execute store result score #h bm.rng run data get entity @s Health',
                       f'execute if score #h bm.rng matches ..{K.get("retreat", 30)} run return run function bm:{pre}/gone',
                       f'scoreboard players set #g {ow} -1', f'execute on passengers if entity @s[type=minecraft:player] run function bm:{pre}/rider',
                       f'execute if score #g {ow} matches -1 run return run function bm:{pre}/gone',            # (got off: it goes home; the follower's back)
                       f'execute unless score #g {ow} = @s {ow} run function bm:{pre}/gait', f'scoreboard players add @s {ot} 1',
                       f'scoreboard players operation #f bm.rng = @s {ot}', f'scoreboard players operation #f bm.rng %= #kr40 bm.rng'] +
       [f'execute if score @s {ow} matches 0 if score #f bm.rng matches 0 run function bm:{pre}/pose/{K["poses"]["idle"]}'] +
       [f'execute if score @s {ow} matches 1 if score #f bm.rng matches {i * 40 // len(walk)} run function bm:{pre}/pose/{p}' for i, p in enumerate(walk)] +
       [f'execute if score @s {ow} matches 2 if score #f bm.rng matches {i * 40 // len(run)} run function bm:{pre}/pose/{p}' for i, p in enumerate(run)] +
       ([f'execute unless entity @s[nbt={{OnGround:1b}}] run effect give @s minecraft:slow_falling 1 0 true'] if K.get('glide') else []) +     # (it glides: wings out, it drifts down)
       [f'execute if score @s {oc} matches 1.. run scoreboard players remove @s {oc} 1',
        f'execute rotated as @s rotated ~ 0 positioned ^ ^ ^-{seat_z} run function bm:{pre}/place', f'tag @e[type=minecraft:item_display,tag={sel}] remove {sel}'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #kr40 bm.rng 40']
    fn(f'{pre}/rider', ['execute unless score @s bm.pid = @e[type=minecraft:horse,tag=' + tag + ',distance=..8,sort=nearest,limit=1] bm.pid run return run function bm:' + pre + '/throw',
                        f'scoreboard players set #g {ow} 0', f'execute if predicate bm:p249/moving run scoreboard players set #g {ow} 1',
                        f'execute if predicate bm:p249/sprint run scoreboard players set #g {ow} 2'])
    fn(f'{pre}/throw', ['ride @s dismount', 'effect give @s minecraft:slow_falling 3 0 true', say('(it shakes you off - it answers to its owner alone)')])
    fn(f'{pre}/gait', [f'scoreboard players operation @s {ow} = #g {ow}', f'scoreboard players set @s {ot} -1',
                       f'execute if score #g {ow} matches 0..1 run attribute @s minecraft:movement_speed base set {K["walk"]}',
                       f'execute if score #g {ow} matches 2 run attribute @s minecraft:movement_speed base set {K["run"]}'])
    # (gone home: its rig away, its host out of the world - and the follower back beside its owner)
    fn(f'{pre}/gone', [f'scoreboard players operation #gid {oid} = @s {oid}', 'scoreboard players operation #gp bm.pid = @s bm.pid',
                       'execute on passengers run ride @s dismount',
                       f'execute as @e[type=minecraft:item_display,tag={ptag}] if score @s {oid} = #gid {oid} run kill @s',
                       'particle minecraft:poof ~ ~2 ~ 1.5 2 1.5 0.05 40', 'item replace entity @s saddle with minecraft:air',
                       f'execute as @a if score @s bm.pid = #gp bm.pid at @s run function bm:{K["follower_back"]}', 'tp @s ~ -400 ~', 'kill @s'])
    # ---- riding my own: and its item used (as the rider): the move by where I look
    fn(f'{pre}/riding', [f'scoreboard players operation #ko {oid} = @s {oo}',
                         f'execute on vehicle if entity @s[type=minecraft:horse,tag={tag}] if score @s {oid} = #ko {oid} run return 1', 'return 0'])
    mv = K['moves']
    fn(f'{pre}/use', [f'execute on vehicle if score @s {oc} matches 1.. run return run ' + say('(it\'s catching its breath)'),
                      f'execute if entity @s[x_rotation=60..90] run return run function bm:{pre}/mv/down',
                      f'execute if entity @s[x_rotation=-90..-60] run return run function bm:{pre}/mv/up', f'function bm:{pre}/mv/level'])
    for k_, (f_, cd) in mv.items():
        fn(f'{pre}/mv/{k_}', [f'execute on vehicle run scoreboard players set @s {oc} {cd * 20}', f'execute on vehicle at @s rotated as @a[distance=..8,sort=nearest,limit=1] run function bm:{f_}'])
    second.append(f'execute as @e[type=minecraft:item_display,tag={ptag}] at @s unless entity @e[type=minecraft:horse,tag={tag},distance=..16] run kill @s')
    G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[type=minecraft:item_display,tag={ptag}]', f'kill @e[type=minecraft:horse,tag={tag}]']
    return dict(ride=f'{pre}/ride', riding=f'{pre}/riding', use=f'{pre}/use')
