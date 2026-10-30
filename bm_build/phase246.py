"""2.99a: THE DREAD MIRE - a lesser manifestation of the Dread, loose in the world in hard mode (mire_art draws it).

WHERE      THE UNDERCROWN: its own, rarely - one at a time, in an unsolved trial's room while someone's inside, never during the
           Sovereign's fight (it calls its own: phase238's 'mires', in its Broken and True forms).
           And any of the three dimensions, rarely, in the dark: now and then a hostile mob rising naturally (mobs/init) in hard mode
           comes up as a Mire instead - where the light is low (4 or less), outside a Golden Cross's ground, never near another
           Mire, never in the vault or the Hollow Throne; ONE A NIGHT for each player (the nearest within 48 when it rises); three
           times as likely on a Dread Night or a Blood Moon. None rise once the Dread Sovereign has fallen (#dfell) - until the
           Dread Ember kindles the nights again; those still about melt away.
DORMANT    a puddle of shimmering reddish-black shadow, 4 blocks across, faintly moving: it creeps towards anyone within 24
           blocks, bubbles and whispers. It can't be hurt like this. Daylight or a bright light on it and it seeps away.
RISEN      anyone (not in creative or spectator) within 10 blocks and it rises: a worm-like black mass ~5 blocks tall, a blind
           ring-mouth glowing red inside, four tentacles, dripping black goo. It is rooted where it rose. Every ~2.5 s:
  GRAB     at 3.5..8 blocks: a tentacle darts out and drags you in (Slowness, pulled towards it) and squeezes (6).
  STAB     within 4.5 blocks: two tentacles cocked back and driven down 4 blocks ahead (10 there).
  THE CROSS  a Golden Cross within 15 blocks (phase181's) and it shrieks, recoils and sinks - and the puddle slips away from
           the cross; it will not rise in the cross's ground. Nobody near for 10 s: it sinks back down to wait.
ITS DEATH  it collapses into the puddle and dissolves, leaving 1-3 SHADOW REMNANTS.
SHADOW MUSK   4 Shadow Remnants in hand, used: kneaded into a vial of Shadow Musk. Drink it: for 5 minutes the Stalkers of a
           Dread Night lose your scent - none rises for you, those hunting you lose you, standing still calls nothing.
(3.0e) Its rig, rise, fight, recoil, sink, melt and the Bound Mire are the Mires' shared runtime, mirekit (CFG, BOUND below): the
Brood-Mire (phase258) runs on it too. Its generated functions are the same, line for line, as before the split."""
from items import T, item, TOTEM, consumable
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF
import mire_art as A

PFX = 'p246'
NAME, COL = 'Dread Mire', '#b0182a'
HP, FLOOR = 400, 100                # (3.0e: 150 -> 400, armour 12, toughness 8 - the owner: it died too easily)
SCALE = getattr(A, 'SCALE', 1.0)
ROLL = 300                          # (1 in this many natural hostile spawns in hard mode comes up a Mire)
APART = 96                          # (never within this of another)
WAKE, LEAVE, CREEP = 10, 20, 24     # (rises for anyone within WAKE; sinks with nobody within LEAVE for 10 s; creeps towards within CREEP)
GRAB_DMG, STAB_DMG = 10, 10                  # (3.0e: past armour - bm:mire bypasses_armor; enchantments and Resistance still count)
EVERY = 50
MUSK = 300                          # (seconds the musk masks you)
DIE_END = 130                       # (3.0d: its melt, start to gone: 6.5 s)
RISEN_SC, DORMANT_SC = 2.4, 1.0     # (the host husk's scale: a 4.7-block hitbox risen; small, invulnerable, dormant)
DUR = {'dormant': 10, 'rise_0': 10, 'rise_1': 12, 'rise_2': 12, 'idle_a': 20, 'idle_b': 20, 'shriek': 6, 'grab_0': 3, 'grab_1': 8,
       'stab_0': 10, 'stab_1': 3, 'recoil': 5, 'sink_0': 10, 'death_0': 12, 'death_1': 20}
GLOW = tuple(getattr(A, 'GLOW', ()))
SND = getattr(A, 'SOUNDS', {})      # name -> sound id (the art's own, else vanilla below)
VAN = {'bubble': ('block.bubble_column.whirlpool_ambient', 0.35), 'rise': ('entity.warden.emerge', 0.6), 'idle': ('entity.warden.ambient', 0.5),
       'lash': ('entity.warden.attack_impact', 1.3), 'shriek': ('block.sculk_shrieker.shriek', 0.6), 'death': ('entity.warden.death', 0.7)}
ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
FOES = 'gamemode=!spectator,gamemode=!creative'
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.msel,tag=bm.mr_{p}]'

item('shadow_remnant', TOTEM, 'Shadow Remnant', COL,
     ['What is left of a Dread Mire. It moves when', 'you are not looking.', ('4 in hand, used: knead them into Shadow Musk.', 'blue'),
      ('16 in hand, sneak + used: a Mire Heart.', 'blue')],
     model='bm:shadow_remnant', stack=64, cat='magic', comps=hold('none'))
HOLD['shadow_remnant'] = f'bm:{PFX}/knead'
item('mire_heart', TOTEM, 'Mire Heart', COL,
     ['Sixteen remnants, knotted together. It beats.', ('Sneak + use on a block: a Mire of your own', 'blue'), ('takes root there and guards it - it fights', 'blue'),
      ('the monsters that come near. Creepers keep away.', 'blue'), ('Sneak + punch it: take it back up.', 'gray')],
     model='bm:mire_heart', stack=4, cat='magic', comps=hold('none'))
HOLD['mire_heart'] = f'bm:{PFX}/heart/use'
item('shadow_musk', TOTEM, 'Shadow Musk', COL,
     ['Black, cold, and it smells of nothing at all.', ('Drink: for 5 minutes the Stalkers', 'blue'), ('of a Dread Night lose your scent.', 'blue')],
     model='bm:shadow_musk', stack=16, cat='magic',
     comps={'minecraft:consumable': consumable(1.6, 'drink', 'minecraft:entity.generic.drink', False)})


def snd(name, v=1.0, p=None, who='@a[distance=..32]'):
    sid, pv = (SND[name], 1.0) if name in SND else ('minecraft:' + VAN[name][0], VAN[name][1])
    return f'playsound {sid} hostile {who} ~ ~ ~ {v} {p if p is not None else pv}'


class CFG:
    """(3.0e) the Dread Mire to the Mires' shared runtime (mirekit) - its rig, tags, numbers, colours and voice"""
    P, A, NAME, COL, HP, FLOOR, SCALE, ARMOR = PFX, A, NAME, COL, HP, FLOOR, SCALE, 12
    WAKE, LEAVE, CREEP, GRAB_DMG, STAB_DMG, EVERY, DIE_END, RISEN_SC, DORMANT_SC, DUR = WAKE, LEAVE, CREEP, GRAB_DMG, STAB_DMG, EVERY, DIE_END, RISEN_SC, DORMANT_SC, DUR
    HOST, R, NEWP, NEWH, GRAB, GOOPT, GNEW, MELT, TAME = 'bm.mire', 'bm.mr', 'bm.mnew', 'bm.mnewh', 'bm.mgrab', 'bm.mgoop', 'bm.mgnew', 'bm.mmelt', 'bm.mtame'
    FELL, CROSS, LIGHT_EXEMPT = '#dfell bm.cfg', 'bm:p181/in_cross', 'bm.muc'
    FLEE_FROM = '@e[type=minecraft:marker,tag=bm.gcm,sort=nearest,limit=1]'
    FOES = WAKE_FOES = FOES
    DUST, DRIP_DUST, STAB_DUST = '0.45,0.02,0.06', '0.5,0.02,0.06', '0.6,0.02,0.08'
    INK, SMOKE, RECOIL_FX, DRIP_BLOCK = 'minecraft:squid_ink', 'minecraft:smoke', 'minecraft:end_rod', 'minecraft:black_concrete'
    GOOP, BUBBLE, LOOT = 'bm:dfx_goop', 'bubble', 'bm:p246/remnants'
    DMG, TOUGH = 'bm:mire', 8
    CHASE, SPEED, LEASH, ROAM, LEASHED = 24, 0.22, 10, 32, ('bm.muc',)
    SPIT, LIVE = None, ('2..5',)
    snd = staticmethod(snd)


class BOUND:
    """(the Mire Heart's Bound Mire, to mirekit.bound)"""
    ITEM, TK, TAME_NAME, DAY_SINK, refuse = 'mire_heart', 'bm.mtk', 'Bound Mire', True, ()
    MON = 'type=#bm:hostile,tag=!bm.mire,tag=!bm.khost,tag=!bm.boss,tag=!bm.stalker'
    msg_use, msg_planted = 'Sneak + use on the top of a block: plant the Mire Heart.', 'Your Mire takes root. '


def generate(G):
    fn, title, give = G.fn, G.title, G.give
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    objs = ['bm.mid', 'bm.ms', 'bm.mt', 'bm.ma', 'bm.mc', 'bm.mq', 'bm.musk', 'bm.mday']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #4 bm.rng 4', 'scoreboard players set #20 bm.rng 20']
    G.OBJECTIVES += objs
    G.wjson('bm/predicate/p246/dark.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'max': 4}}}})
    G.wjson('bm/predicate/p246/day.json', {'condition': 'minecraft:time_check', 'clock': 'minecraft:overworld', 'value': {'min': 0, 'max': 12999}, 'period': 24000})
    G.wjson('bm/predicate/p246/bright.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'min': 12}}}})

    # ================================================================== the rig, the rise, the fight, the melt: the Mires' shared runtime (mirekit)
    import mirekit as MK
    MK.runtime(G, CFG)
    MK.damage_type(G, CFG)
    # (one a night for each player: the nearest within 48 must not have had one rise for them tonight - the day's number, bm.mday;
    #  three times the odds on a Dread Night or a Blood Moon)
    fn(f'{PFX}/roll', ['execute store result score #r bm.rng run random value 1..' + str(ROLL),
                       'scoreboard players set #rk bm.rng 1', 'execute if score #dnight bm.bm matches 1 run scoreboard players set #rk bm.rng 3',
                       'execute if score #active bm.bm matches 1 run scoreboard players set #rk bm.rng 3',
                       'execute if score #r bm.rng > #rk bm.rng run return 0',
                       'execute store result score #day bm.rng run time query day',
                       f'execute unless entity @p[distance=..48,{FOES}] run return 0',
                       f'execute as @p[distance=..48,{FOES}] if score @s bm.mday = #day bm.rng run return 0',
                       'execute unless predicate bm:p246/dark run return 0',
                       f'execute if entity @e[type=minecraft:husk,tag=bm.mire,distance=..{APART}] run return 0',
                       'execute if function bm:p181/in_cross run return 0',
                       'execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run function bm:p246/spawn',
                       'execute unless entity @e[type=minecraft:husk,tag=bm.mire,distance=..1] run return 0',
                       f'execute as @p[distance=..48,{FOES}] run scoreboard players operation @s bm.mday = #day bm.rng',
                       'tp @s ~ -400 ~', 'kill @s', 'return 1'])
    skip = {'ghast', 'phantom', 'drowned', 'shulker', 'blaze', 'breeze', 'pillager', 'vindicator', 'piglin_brute'}
    for t in list(G.ARMORED) + list(G.UNARMORED):
        if t in skip or f'mobs/init/{t}' not in G.FUNCS: continue
        G.FUNCS[f'mobs/init/{t}'].insert(0, 'execute if score #hard bm.cfg matches 1 unless score #dfell bm.cfg matches 1 unless dimension bm:gutter '
                                            f'unless dimension bm:hollow_throne if function bm:{PFX}/roll run return 0')

    MK.watch(G, CFG)
    MK.fight(G, CFG)
    MK.death(G, CFG)
    G.wjson('bm/loot_table/p246/remnants.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('shadow_remnant', G.uni(1, 3))]}]})

    # ================================================================== the remnants kneaded; the musk drunk; the Stalkers lose your scent
    fn(f'{PFX}/knead', ['execute store result score #n bm.rng run clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 0',
                        'execute if score #n bm.rng matches ..3 run return run ' + title('@s', 'actionbar', T('Four Shadow Remnants knead into a vial of Shadow Musk.', 'gray')),
                        'clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 4', give('shadow_musk'),
                        'playsound minecraft:block.honey_block.slide player @s ~ ~ ~ 1 0.6', 'playsound minecraft:item.bottle.fill player @s ~ ~ ~ 1 0.7',
                        title('@s', 'actionbar', T('You knead the remnants into a vial of Shadow Musk.', COL))])
    G.consume_adv('shadow_musk', f'bm:{PFX}/musk')
    fn(f'{PFX}/musk', ['advancement revoke @s only bm:consume/shadow_musk', f'scoreboard players set @s bm.musk {MUSK}',
                       'particle minecraft:squid_ink ~ ~1 ~ 0.3 0.6 0.3 0.02 12', 'playsound minecraft:entity.warden.sniff player @s ~ ~ ~ 1 0.6',
                       title('@s', 'actionbar', [T('Your scent is gone. ', COL, bold=True), T('The Stalkers will not find you for 5 minutes.', 'gray')])])
    second.append(f'execute as @a[scores={{bm.musk=1..}}] run function bm:{PFX}/musk_sec')
    fn(f'{PFX}/musk_sec', ['scoreboard players remove @s bm.musk 1',
                           'execute if score @s bm.musk matches 30 run ' + title('@s', 'actionbar', T('The Shadow Musk is wearing off...', 'gray', italic=True)),
                           'execute if score @s bm.musk matches 0 run ' + title('@s', 'actionbar', T('Your scent returns.', COL))])
    # (phase181: no Stalker rises or steps out for the masked; one hunting them loses them)
    G.FUNCS['p181/hunted'].insert(0, 'execute if score @s bm.musk matches 1.. run return run scoreboard players set @s bm.dnst 0')
    s2 = G.FUNCS['p181/stk/second']
    k = next(i for i, l in enumerate(s2) if 'unless entity @a[tag=bm.stko] run return run function bm:p181/stk/gone' in l)
    s2.insert(k + 1, 'execute if entity @a[tag=bm.stko,scores={bm.musk=1..}] run return run function bm:p181/stk/lost')

    # ================================================================== THE BOUND MIRE: remnants kneaded into a Mire Heart; set down, it guards
    # (16 Shadow Remnants in hand, sneak + used: a Mire Heart. Sneak + use the Heart on a block: a Mire of your own takes root there -
    #  stationary; by day (in the Overworld) it stays a puddle; by night it rises for any monster within 10 and fights it as a wild one fights you - never you, never anyone; it can't be
    #  hurt; daylight, the cross and the Dread's fall leave it be. Creepers will not come within 10 of it: they're shoved back, fuses
    #  out. Sneak + punch its puddle to take it back up.)
    fn(f'{PFX}/knead_heart', ['execute store result score #n bm.rng run clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 0',
                              'execute if score #n bm.rng matches ..15 run return run ' + title('@s', 'actionbar', T('Sixteen Shadow Remnants, sneak + used, knead into a Mire Heart.', 'gray')),
                              'clear @s *[minecraft:custom_data~{bm:"shadow_remnant"}] 16', give('mire_heart'),
                              'playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 1 0.7', 'particle minecraft:squid_ink ~ ~1 ~ 0.3 0.4 0.3 0.05 20',
                              title('@s', 'actionbar', T('The remnants knot together - and begin to beat. A Mire Heart.', COL, bold=True))])
    kn = G.FUNCS[f'{PFX}/knead']
    kn.insert(0, f'execute if predicate bm:p20/sneaking run return run function bm:{PFX}/knead_heart')
    MK.bound(G, CFG, BOUND)
    # ================================================================== THE UNDERCROWN'S OWN (in moderation: two at most at a time)
    # (now and then, while someone's inside and the Sovereign stands, a puddle rises in one of its rooms - at a room's fx marker,
    #  let down to its floor, at least 20 blocks from everyone; the per-night count doesn't apply in there. A rebuild clears them.)
    import phase237 as P237
    UB = P237.BOX
    second.append(f'execute if score #hard bm.cfg matches 1 unless score #dfell bm.cfg matches 1 in minecraft:the_nether '
                  f'if entity @a[{UB},gamemode=!spectator] run function bm:{PFX}/uc/try')
    # (2.99a, the owner: rarer, so a puzzle isn't swamped - one at a time, a chance in 300 a second; never in a room whose trial is
    #  solved (the room's nearest trial controller, bm.done); never while anyone is in the Sovereign's hall - its own Mires come then)
    import phase238 as P238
    fn(f'{PFX}/uc/try', ['execute store result score #r bm.rng run random value 1..300', 'execute unless score #r bm.rng matches 1 run return 0',
                         f'execute in minecraft:the_nether if entity {P238.FIGHT} run return 0',
                         # (holy armour worn by anyone inside: no Mire dares rise in the Undercrown)
                         f'execute in minecraft:the_nether as @a[{UB}] if items entity @s armor.* *[minecraft:custom_data~{{bm_angel:1b}}] run return 0',
                         f'execute in minecraft:the_nether if entity @e[type=minecraft:husk,tag=bm.mire,tag=!bm.mtame,tag=!bm.svm,{UB}] run return 0',
                         f'execute in minecraft:the_nether as @e[type=minecraft:marker,tag=bm.dgfx,tag=bm.d_under,sort=random,limit=1] at @s '
                         f'unless entity @a[distance=..20] if function bm:{PFX}/uc/open run function bm:{PFX}/uc/down'])
    fn(f'{PFX}/uc/open', ['execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_under,distance=..40,sort=nearest,limit=1] if score @s bm.done matches 1 run return 0',
                          'execute unless entity @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_under,distance=..40] run return 0', 'return 1'])
    fn(f'{PFX}/uc/down', ['scoreboard players set #dn bm.rng 16', f'function bm:{PFX}/uc/step'])
    fn(f'{PFX}/uc/step', ['execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run return run function bm:p246/uc/rise',
                          'scoreboard players remove #dn bm.rng 1', f'execute if score #dn bm.rng matches 1.. positioned ~ ~-1 ~ run function bm:{PFX}/uc/step'])
    fn(f'{PFX}/uc/rise', ['execute align xyz positioned ~0.5 ~ ~0.5 run function bm:p246/spawn',
                          'execute align xyz positioned ~0.5 ~ ~0.5 as @e[type=minecraft:husk,tag=bm.mire,distance=..1] run tag @s add bm.muc'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:interaction,tag=bm.mtk]']
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.mr]', 'execute as @e[type=minecraft:husk,tag=bm.mire] at @s run tp @s ~ -400 ~']
    fn('admin/mire/spawn', [f'execute positioned ^ ^ ^6 run function bm:{PFX}/spawn'])
    fn('admin/mire/kit', [give('shadow_remnant', 4), give('shadow_musk')])


def rp(R):
    A.rp(R)
    R.LANG.update({'death.attack.bm.mire': '%1$s was crushed by a Dread Mire', 'death.attack.bm.mire.player': '%1$s was crushed by a Dread Mire while fleeing %2$s'})
