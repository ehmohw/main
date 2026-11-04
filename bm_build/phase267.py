"""3.1: THE SPAWNER - the 56th follower (spawner_pet_art.py draws it and its ghost minions; fol5flag.SPAWNER). The pilot light of a
dungeon spawner that got bored of making monsters, and now only makes FRIENDS.

THE VIGIL    light a Soul Lantern beside a dungeon's monster spawner (place it within 3 blocks of the spawner) and hold the room:
             three waves come at you (3, 4 and 5 monsters - the vigil's own, never an elite) - keep the spawner standing and stay
             within 16 of it. On the third wave its pilot light "gets bored of making monsters" and hops out. Right-click it: it
             hands you the PILOT LIGHT (its summoning item) and comes along. The real spawner block is never touched.
FEEDING      right-click it holding rotten flesh, string or a blaze rod: it looks up, the food drops in through the top bars, it
             chews - and its ember turns sickly green (ZOMBIES), violet (SPIDERS) or blaze yellow (BLAZES). Unfed, it's orange,
             and its minions are a mix. The type sticks until it's fed again (bm.nzfd on you).
ITS WAYS     it never fights itself - it CONJURES. A monster within 10: its ember flares to the top of the cage, a smoke puff, and
             a ghost minion pops out (two at a time, a third for 10 s after a minion's kill; one every 1.5 s). The minions rush in a
             loose swarm, each in its own lane:
               ZOMBIES  shamble in and GRAB - 2 and Slowness III for 1.5 s
               SPIDERS  circle, then lunge and WEB - 2 and Slowness IV for 1 s, in a burst of cobweb
               BLAZES   hover 3 off and pelt it - three little fireballs, 2 each (they set nothing alight, and touch no block)
             A minion lasts 5 s or 3 hits, then POPS into soul puffs that drift home. Minions are displays: no loot, no fire, no
             block ever touched; they go with it when it's sent home, faints or is left behind.
EVERYTHING ELSE is every follower's: sitting (right-click: feet tucked, the flame guttering; sneak + right-click: turned down to a
pilot light - no minions, and it slowly heals), a wardrobe (Oxidised and Amethyst - drawn - Soot Black, the metal bars; the fed
colours still show), a rare aura (the Ring of Souls), a shiny (the Gilded Cage), the Partner Wheel, a frame (a tiny ghost spinning
in it), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt, F, Int, B
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import rigfol as RF
import phase235 as P235

S5 = fol5.SPEC['spawner']
A0 = fol5art.get('spawner')
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
FED = {1: ('_z', 'zombie', 'minecraft:rotten_flesh', 'sickly green', '#5ac83a'), 2: ('_s', 'spider', 'minecraft:string', 'violet', '#b46aff'),
       3: ('_b', 'blaze', 'minecraft:blaze_rod', 'blaze yellow', '#ffd040')}
KINDS = ('zombie', 'spider', 'blaze')
FOE = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body,tag=!bm.nxwv'
WAVES = {1: 3, 2: 4, 3: 5}

item(ITEM, TOTEM, 'The Pilot Light', COL,
     ['A little ember in a soul lantern, smiling at you.', 'It used to make monsters. It\'s much happier now.',
      ('Use: call the Spawner (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'),
      ('Feed it rotten flesh, string or a blaze rod.', 'blue'), ('Its ghost minions do the fighting.', 'blue'),
      ('If it faints: 2 minutes before it can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Spawner(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'spawner', 'The Spawner', COL, LINE, 'p267', 'nx', 'nz'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 5850, 30, 120, ITEM
    pron, they = 'it', 'it'
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=6, attack_damage=1, movement_speed=0.32, follow_range=32, step_height=1.1)
    SCALE, HIT = 0.7, W5.hit(A0)
    CYCLE = W5.cycle(A0, (200, [(0, 'idle_a'), (70, 'idle_b'), (120, 'idle_a')]), (40, [(0, 'sit_a'), (20, 'sit_a2')]), (None, [(0, 'spawn'), (10, 'idle_a')]),
                     {11: (None, [(0, 'spawn'), (10, 'command'), (16, 'idle_a')]), 12: (None, [(0, 'feed'), (8, 'chew'), (14, 'chew2'), (20, 'idle_a')])}, wp=8, rp_=6)
    DUR = dict(P235._DUR, spawn=6, command=4, feed=6, chew=4, chew2=4, sit_a=10, sit_a2=10, sit_b=20, walk_0=4, walk_1=4)
    QUIPS = ['"I used to make zombies. All day. Every day. It was SO boring."', '(its ember flickers, pleased with itself)',
             '"Want a friend? I can make you a friend. A small, see-through one."', '"Feed me string and I\'ll make spiders! Nice ones."',
             '(it puffs a little smoke ring out of the top of its cage)', '"Nobody ever told the spawner it could just... stop."']
    HELLO = ('(the Spawner clanks back to you on its little iron feet)', '(a puff of soul smoke - and the Spawner hops out of it, ember first) "Friends? Friends!"',
             '(its ember dims to a pilot light, and it\'s gone)')
    SIT = ('"Up! Who needs a friend?"', '(it settles, feet tucked, its flame guttering left and right)')
    FAINT = '"...pilot light... going... out..."'
    NOT_YOURS = '(its ember looks you over) "You\'re not the one who sat with me through the waves."'
    POWERS = [('Conjure', 'a monster within 10: its ember flares, a puff - a ghost minion pops out (two at a time, a third after a kill; one every 1.5 s)'),
              ('Zombie minions', 'fed rotten flesh: they shamble in and GRAB - 2 and Slowness III for 1.5 s'),
              ('Spider minions', 'fed string: they circle, then lunge and WEB - 2 and Slowness IV for 1 s'),
              ('Blaze minions', 'fed a blaze rod: they hover and pelt it - three little fireballs, 2 each (nothing set alight)'),
              ('Pop', 'a minion lasts 5 s or 3 hits, then pops into soul puffs - no loot, no fire, no block touched'),
              ('Pilot Light', 'sneak + right-click: turned down low - no minions, and it slowly heals')]
    INTRO = [T('The Spawner', COL, bold=True), T(' - a dungeon spawner\'s pilot light, bored of making monsters. ', 'gray'),
             T('Now it only makes friends.', LINE, italic=True)]
    BURST = ['particle minecraft:soul ~ ~0.6 ~ 0.3 0.3 0.3 0.02 10', 'particle minecraft:large_smoke ~ ~0.6 ~ 0.3 0.3 0.3 0.02 8',
             'particle minecraft:flame ~ ~0.5 ~ 0.2 0.2 0.2 0.02 8']
    FADE_SOUND = 'playsound minecraft:block.fire.extinguish neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'
    SUMMON_EXTRA = ['playsound minecraft:block.trial_spawner.spawn_mob neutral @a[distance=..24] ~ ~ ~ 0.8 1.4']
    ENC_POSES = [(0, 'idle_a'), (30, 'idle_b'), (60, 'spawn')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:soul ~ ~0.6 ~ 0.2 0.2 0.2 0.01 4'
    ADV = ('Bored of Monsters', 'Hold a dungeon through three waves by a soul lantern - and meet the spawner\'s pilot light')
    ADMIN_HINT = 'Light a Soul Lantern beside a dungeon\'s monster spawner and hold the room through three waves.'
    MEET_HINT = 'Right-click it.'


from fol5_kit import T as _T  # noqa: E402
A0.POSES['sit_a2'] = A0.R.ground(dict(A0.POSES['sit_a'], flame=_T(0, 0, 14)))
A0.POSES['chew2'] = dict(A0.POSES['chew'], core=_T(-6, 0, -8))
_DOLL = 'A doll of the Spawner - a little iron cage with a smiling ember inside.'
_eff = W5.pair_fx
_PAIRS = {
    'nx_bender': ('spawner', 'bender', 'Herding Dog', '#e0a860', 'The Spawner and Bender - he herds its minions, very seriously',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(rounds up a ghost minion. It does not mind.)'), ('spawner', '"Good boy! Bring them back! ...he brings them back."')],
                  [('spawner', '(makes a little ghost minion just for him)', 'bender', '(play-bows at it. It play-bows back.)')]),
    'nx_capshun': ('spawner', 'capshun', 'Paint-Ghosts', '#f0f0f0', 'The Spawner and Mr. Capshun - he paints its minions, and they pop into colour',
                   _eff(('haste', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He painted a ghost. The ghost was delighted."]'), ('spawner', '"Can you paint them FASTER? I make them fast."')],
                   [('spawner', '"Another one!"', 'capshun', '[Mr. Capshun narrates: "He ran out of red."]')]),
}
W5.register(Spawner, A0, _DOLL, ('minecraft:soul', 'minecraft:block.trial_spawner.spawn_mob', 'minecraft:large_smoke'), _PAIRS, 'the Spawner')
FRAMES = [f'{ITEM}_f{i}' for i in range(3)]


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Spawner, G)


# ---------------------------------------------------------------------------------------------------- the icons, the minions' models
def _icon(ghost=None):
    """The Pilot Light: a little soul lantern, an ember with a smile in it (in a frame: a tiny ghost of a minion beside it)"""
    from sprites280 import S
    s = S()
    pal = {'k': '#2a2e38', 'i': '#464c5a', 'o': '#ff8a2a', 'y': '#ffd040', 'w': '#fff4c0', 'f': '#5a2a10', 'b': '#9ad8ff'}
    s.g(['...kkkk...', '..k....k..', '.kkkkkkkk.', '.ki....ik.', '.k.oooo.k.', '.k.oyyo.k.', '.k.ofyf.k.', '.k.oooo.k.', '.ki....ik.', '.kkkkkkkk.', '..kiiiik..'], pal, 3, 3)
    if ghost:
        col = {'zombie': '#8ae86a', 'spider': '#c0a0e0', 'blaze': '#fff0a0'}[ghost]
        s.g(['.cc.', 'cccc', 'c..c', '.cc.'], {'c': col}, 12, 1)
    return s.render()


def _merged(M):
    """a minion's whole rig as one model (its idle parts round its body's joint) - and its pop on its own"""
    root = M.PIVOT['body']
    tex, els = {}, []
    for name, (t, es) in M.models().items():
        p = name[len(M.PREFIX):]
        if p not in M.PARTS or p == 'pop' or '_x' in p:
            continue
        d = [M.PIVOT[p][i] - root[i] for i in range(3)]
        tex.update(t)
        for e in es:
            e2 = dict(e, **{'from': [round(e['from'][i] + d[i], 4) for i in range(3)], 'to': [round(e['to'][i] + d[i], 4) for i in range(3)]})
            if 'rotation' in e:
                e2['rotation'] = dict(e['rotation'], origin=[round(e['rotation']['origin'][i] + d[i], 4) for i in range(3)])
            els.append(e2)
    return (tex, els)


def rp(R):
    W5.rp(Spawner, R, _icon(), A0)
    for i, k in enumerate(KINDS):
        R.ICONS[FRAMES[i]] = _icon(k)
    for k, M in A0.MINIONS.items():
        R.HATS[f'{M.PREFIX}all'] = _merged(M)
        R.HATS[f'{M.PREFIX}pop'] = M.models()[f'{M.PREFIX}pop']
        R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (M.PREFIX,)


def textures():
    out = dict(A0.textures())
    for M in A0.MINIONS.values():
        out.update(M.textures())
    return out


# ---------------------------------------------------------------------------------------------------- its ways: the minions
def _abilities(G, X):
    fn, pfx, me, S = G.fn, X.pfx, X.me, X.S
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    objs = ['bm.nzml', 'bm.nzmh', 'bm.nzmc', 'bm.nzfd', 'bm.nzkt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    mins = '@e[type=minecraft:item_display,tag=bm.nxmin]'
    # (the host, free to act: a monster within 10, fewer than its cap out, the spawn timer run down - a minion)
    lines = [f'execute if score @s {S("sc")} matches 1.. run scoreboard players remove @s {S("sc")} 1',
             f'execute if score @s bm.nzkt matches 1.. run scoreboard players remove @s bm.nzkt 1',
             f'execute {X.idle_fight} unless score @s {S("sc")} matches 1.. if entity @e[{FOE},distance=..10] run function bm:{pfx}/conjure_q']
    fn(f'{pfx}/conjure_q', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #mn bm.rng 0',
                            f'execute as {mins} if score @s bm.pid = #me bm.pid run scoreboard players add #mn bm.rng 1',
                            'scoreboard players set #cap bm.rng 2', 'execute if score @s bm.nzkt matches 1.. run scoreboard players set #cap bm.rng 3',
                            'execute if score #mn bm.rng >= #cap bm.rng run return 0',
                            f'function bm:{pfx}/conjure'])
    fn(f'{pfx}/conjure', X.go(11, 16, 'sc', 30, X.face('surprised', 10) + [snd('block.trial_spawner.spawn_mob', 0.6, 1.6), snd('block.fire.ambient', 0.6, 1.4)]) +
       ['scoreboard players set #fd bm.rng 0', 'execute on owner run scoreboard players operation #fd bm.rng = @s bm.nzfd',
        'execute if score #fd bm.rng matches 0 store result score #fd bm.rng run random value 1..3',
        'execute store result score #ln bm.rng run random value 1..3',
        'particle minecraft:large_smoke ~ ~0.8 ~ 0.15 0.1 0.15 0.03 10', 'particle minecraft:soul ~ ~0.9 ~ 0.2 0.1 0.2 0.04 6'] +
       [f'execute if score #ln bm.rng matches {j + 1} if score #fd bm.rng matches {i} positioned ^{(-0.5, 0, 0.5)[j]} ^0.6 ^0.4 run function bm:{pfx}/min/new_{k}_{j}'
        for i, k in enumerate(KINDS, 1) for j in range(3)])
    for k in KINDS:
        M = A0.MINIONS[k]
        for j in range(3):
            nb = {'Tags': ['bm.nxmin', f'bm.nxm_{k}', f'bm.nxl{j}', 'bm.nxmn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': f'bm:{M.PREFIX}all'}},
                  'item_display': 'fixed', 'teleport_duration': Int(2), 'brightness': {'block': Int(12), 'sky': Int(12)}, 'view_range': F(1.0),
                  'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.25), F(0)], 'scale': [F(M.RIG_SCALE)] * 3}}
            fn(f'{pfx}/min/new_{k}_{j}', [f'summon minecraft:item_display ~ ~{0.8 if k == "blaze" else 0} ~ {snbt(nb)}',
                f'scoreboard players operation @e[type=minecraft:item_display,tag=bm.nxmn] bm.pid = #me bm.pid',
                'scoreboard players set @e[type=minecraft:item_display,tag=bm.nxmn] bm.nzml 100', 'scoreboard players set @e[type=minecraft:item_display,tag=bm.nxmn] bm.nzmh 0',
                'scoreboard players set @e[type=minecraft:item_display,tag=bm.nxmn] bm.nzmc 10', 'tag @e[type=minecraft:item_display,tag=bm.nxmn] remove bm.nxmn'])
    # ---- each minion, each tick: its life; its foe (the nearest monster within 14 of it) - or home to the cage
    X.tick.append(f'execute as {mins} at @s run function bm:{pfx}/min/tick')
    near = f'@e[{FOE},distance=..14,sort=nearest,limit=1]'
    fn(f'{pfx}/min/tick', ['scoreboard players remove @s bm.nzml 1', 'execute if score @s bm.nzmc matches 1.. run scoreboard players remove @s bm.nzmc 1',
                           'execute if score @s bm.nzml matches ..0 run return run function bm:p267/min/pop',
                           'execute if score @s bm.nzmh matches 3.. run return run function bm:p267/min/pop',
                           f'execute unless entity {near} run return run function bm:p267/min/home'] +
       [f'execute if entity @s[tag=bm.nxm_{k}] run return run function bm:p267/min/{k}' for k in KINDS])
    step = lambda d: [f'execute if entity @s[tag=bm.nxl0] facing entity {near} feet positioned ^0.03 ^ ^{d} run tp @s ~ ~ ~',
                      f'execute if entity @s[tag=bm.nxl1] facing entity {near} feet positioned ^ ^ ^{d + 0.02} run tp @s ~ ~ ~',
                      f'execute if entity @s[tag=bm.nxl2] facing entity {near} feet positioned ^-0.03 ^ ^{d - 0.02} run tp @s ~ ~ ~',
                      f'execute facing entity {near} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~']
    fn('p267/min/zombie', [f'execute if entity @e[{FOE},distance=..1.2] if score @s bm.nzmc matches ..0 run return run function bm:p267/min/grab',
                           f'execute if entity @e[{FOE},distance=..1.2] run return 0'] + step(0.11))
    fn('p267/min/spider', [f'execute if entity @e[{FOE},distance=..1.5] if score @s bm.nzmc matches ..0 run return run function bm:p267/min/web',
                           f'execute if entity @e[{FOE},distance=..2.6] run return run execute facing entity {near} feet positioned ^0.16 ^ ^0.08 run tp @s ~ ~ ~ ~ ~'] + step(0.2))
    fn('p267/min/blaze', [f'execute if entity @e[{FOE},distance=..4] if score @s bm.nzmc matches ..0 run return run function bm:p267/min/shoot',
                          f'execute if entity @e[{FOE},distance=..2.6] run return run execute facing entity {near} feet positioned ^ ^ ^-0.08 run tp @s ~ ~ ~ ~ ~',
                          f'execute if entity @e[{FOE},distance=..3.4] run return 0'] + step(0.12))
    host = lambda: ['scoreboard players operation #me bm.pid = @s bm.pid',
                    f'execute as @e[type=minecraft:wolf,tag=bm.nxpet,distance=..32] if score @s bm.pid = #me bm.pid run tag @s add {me}', 'scoreboard players set #pd bm.rng 2']
    unhost = [f'tag @e[type=minecraft:wolf,tag={me}] remove {me}', 'scoreboard players add @s bm.nzmh 1', 'scoreboard players set @s bm.nzmc 20']
    fn('p267/min/grab', host() + [f'execute as @e[{FOE},distance=..1.4,sort=nearest,limit=1] at @s run function bm:p267/min/grabbed'] + unhost +
       [snd('entity.zombie.attack_wooden_door', 0.3, 1.8)])
    fn('p267/min/grabbed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 2', 'particle minecraft:dust{color:[0.54,0.91,0.42],scale:0.8} ~ ~1 ~ 0.3 0.4 0.3 0 8',
                            'function bm:p267/min/killed_q'])
    fn('p267/min/web', host() + [f'execute as @e[{FOE},distance=..1.7,sort=nearest,limit=1] at @s run function bm:p267/min/webbed'] + unhost + [snd('entity.spider.ambient', 0.4, 1.8)])
    fn('p267/min/webbed', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 1 3', 'particle minecraft:block{block_state:"minecraft:cobweb"} ~ ~1 ~ 0.4 0.4 0.4 0 16',
                           'function bm:p267/min/killed_q'])
    fn('p267/min/shoot', host() + [f'execute facing entity {near} eyes positioned ^ ^0.4 ^0.3 run function bm:p267/min/ball',
                                   f'execute as {near} at @s run function bm:p267/min/scorched'] + unhost + [snd('entity.blaze.shoot', 0.3, 1.8)])
    fn('p267/min/ball', [f'particle minecraft:small_flame ^ ^ ^{d} 0.04 0.04 0.04 0 2' for d in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5)])
    fn('p267/min/scorched', [f'function bm:{pfx}/hurt', 'particle minecraft:flame ~ ~1 ~ 0.2 0.3 0.2 0.02 6', 'function bm:p267/min/killed_q'])
    # (a kill: for 10 s its host may have three out)
    fn('p267/min/killed_q', ['execute store result score #h bm.rng run data get entity @s Health', 'execute if score #h bm.rng matches 1.. run return 0',
                             f'execute as @e[type=minecraft:wolf,tag={me}] run scoreboard players set @s bm.nzkt 200'])
    fn('p267/min/home', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:wolf,tag=bm.nxpet,distance=..24] if score @s bm.pid = #me bm.pid run tag @s add bm.nxhm',
                         'execute unless entity @e[type=minecraft:wolf,tag=bm.nxhm] run return run function bm:p267/min/pop',
                         'execute if entity @e[type=minecraft:wolf,tag=bm.nxhm,distance=..1.2] run function bm:p267/min/pop',
                         'execute facing entity @e[type=minecraft:wolf,tag=bm.nxhm,limit=1] feet positioned ^ ^ ^0.15 run tp @s ~ ~ ~ ~ ~', 'tag @e[tag=bm.nxhm] remove bm.nxhm'])
    pop = {'Tags': ['bm.nxpop'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:smz_pop'}}, 'item_display': 'fixed',
           'brightness': {'block': Int(15), 'sky': Int(15)}, 'transformation': {'left_rotation': RF.IDENT, 'right_rotation': RF.IDENT, 'translation': [F(0), F(0.3), F(0)], 'scale': [F(0.6)] * 3}}
    fn('p267/min/pop', [f'execute if entity @s[tag=bm.nxm_{k}] run summon minecraft:item_display ~ ~ ~ ' + snbt(dict(pop, item={'id': 'minecraft:paper', 'count': Int(1),
                                                                                                                        'components': {'minecraft:item_model': f'bm:{A0.MINIONS[k].PREFIX}pop'}}))
                        for k in KINDS] +
       ['scoreboard players set @e[type=minecraft:item_display,tag=bm.nxpop,distance=..0.2] bm.nzml 6',
        'particle minecraft:soul ~ ~0.5 ~ 0.3 0.3 0.3 0.03 12', 'particle minecraft:poof ~ ~0.5 ~ 0.2 0.2 0.2 0.02 6', snd('entity.allay.item_thrown', 0.4, 1.8), 'kill @s'])
    X.tick += ['scoreboard players remove @e[type=minecraft:item_display,tag=bm.nxpop] bm.nzml 1', 'kill @e[type=minecraft:item_display,tag=bm.nxpop,scores={bm.nzml=..0}]']
    # (left without its host - sent home, fainted, unloaded, the host far off - a minion pops within the second)
    X.second.append(f'execute as {mins} at @s run function bm:p267/min/orphan_q')
    fn('p267/min/orphan_q', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                             'execute as @e[type=minecraft:wolf,tag=bm.nxpet,distance=..32] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                             'execute if score #al bm.rng matches 0 run kill @s'])
    # (turned down to a pilot light - sneak-sat: it heals slowly)
    X.second.append('execute as @e[type=minecraft:wolf,tag=bm.nxpet,tag=bm.nxsb] if data entity @s {Sitting:1b} run effect give @s minecraft:regeneration 2 0 true')
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.nxmin]', 'kill @e[tag=bm.nxpop]', 'kill @e[tag=bm.nxvig]']
    return lines


def _encounter(G, X):
    """THE VIGIL: a soul lantern placed beside a monster spawner - three waves held - and its pilot light hops out"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.nzvw', 'bm.nzvt', 'bm.nzva')]
    G.OBJECTIVES += ['bm.nzvw', 'bm.nzvt', 'bm.nzva']
    G.wjson('bm/advancement/p267/lantern.json', {'criteria': {'set': {'trigger': 'minecraft:placed_block', 'conditions': {'location': [
        {'condition': 'minecraft:location_check', 'predicate': {'block': {'blocks': 'minecraft:soul_lantern'}}}]}}}, 'rewards': {'function': 'bm:p267/vig/lantern'}})
    probe = [f'execute if block ~{dx} ~{dy} ~{dz} minecraft:spawner positioned ~{dx} ~{dy} ~{dz} run return run function bm:p267/vig/start'
             for dy in (0, -1, 1, -2, 2) for dx in range(-3, 4) for dz in range(-3, 4)]
    fn('p267/vig/lantern', ['advancement revoke @s only bm:p267/lantern', 'execute if entity @s[tag=bm.nxmet] run return 0',
                            'execute if entity @e[type=minecraft:marker,tag=bm.nxvig,distance=..32] run return 0',
                            'execute if entity @e[type=minecraft:interaction,tag=bm.nxenc,distance=..48] run return 0',
                            'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid'] + probe)
    fn('p267/vig/start', ['execute align xyz positioned ~0.5 ~ ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["bm.nxvig","bm.nxvn"]}',
                          'scoreboard players operation @e[type=minecraft:marker,tag=bm.nxvn] bm.pid = #me bm.pid',
                          'scoreboard players set @e[type=minecraft:marker,tag=bm.nxvn] bm.nzvw 0', 'scoreboard players set @e[type=minecraft:marker,tag=bm.nxvn] bm.nzvt 3',
                          'scoreboard players set @e[type=minecraft:marker,tag=bm.nxvn] bm.nzva 0', 'tag @e[tag=bm.nxvn] remove bm.nxvn',
                          'particle minecraft:soul_fire_flame ~0.5 ~0.5 ~0.5 0.4 0.4 0.4 0.02 20', 'playsound minecraft:block.trial_spawner.about_to_spawn_item block @a[distance=..24] ~ ~ ~ 1 0.8',
                          tellraw('@a[distance=..24]', [T('The soul lantern\'s blue light falls on the spawner\'s cage. Inside it, something small and orange stops spinning - ', LINE, italic=True),
                                                        T('and looks at you. ', 'gray', italic=True), T('Hold the room: three waves are coming.', COL, bold=True)])])
    X.second.append('execute as @e[type=minecraft:marker,tag=bm.nxvig] at @s run function bm:p267/vig/sec')
    fn('p267/vig/sec', ['scoreboard players operation #o bm.rng = @s bm.pid',
                        'execute unless block ~ ~ ~ minecraft:spawner run return run function bm:p267/vig/broken',
                        'scoreboard players set #near bm.rng 0', 'execute as @a[distance=..16,gamemode=!spectator] if score @s bm.pid = #o bm.rng run scoreboard players set #near bm.rng 1',
                        'execute if score #near bm.rng matches 0 run scoreboard players add @s bm.nzva 1', 'execute if score #near bm.rng matches 1 run scoreboard players set @s bm.nzva 0',
                        'execute if score @s bm.nzva matches 15.. run return run function bm:p267/vig/left',
                        'execute if score @s bm.nzvt matches 1.. run scoreboard players remove @s bm.nzvt 1',
                        'execute if score @s bm.nzvt matches 1.. run return 0',
                        'execute if entity @e[type=#bm:hostile,tag=bm.nxwv,distance=..32] run return 0',
                        'execute if score @s bm.nzvw matches 3.. run return run function bm:p267/vig/done',
                        'scoreboard players add @s bm.nzvw 1', 'scoreboard players set @s bm.nzvt 2'] +
       [f'execute if score @s bm.nzvw matches {w} run function bm:p267/vig/wave{w}' for w in WAVES])
    mob = lambda kind, dx, dz: f'summon minecraft:{kind} ~{dx} ~1 ~{dz} {{Tags:["bm.nxwv","bm.seen"],PersistenceRequired:1b}}'
    spots = [(3, 0), (-3, 0), (0, 3), (0, -3), (2, 2)]
    kinds = ['zombie', 'skeleton', 'spider', 'zombie', 'husk']
    for w, n in WAVES.items():
        fn(f'p267/vig/wave{w}', [f'execute positioned ~{dx} ~ ~{dz} if block ~ ~1 ~ #bm:grap_pass run {mob(kinds[(i + w) % 5], 0, 0)}' for i, (dx, dz) in enumerate(spots[:n])] +
           [f'execute unless entity @e[type=#bm:hostile,tag=bm.nxwv,distance=..8] run {mob("zombie", 0.5, 0.5)}',
            'playsound minecraft:block.trial_spawner.spawn_mob block @a[distance=..24] ~ ~ ~ 1 0.7', 'particle minecraft:soul ~ ~1 ~ 2 0.5 2 0.02 30',
            'execute as @a[distance=..24] if score @s bm.pid = #o bm.rng run ' + title('@s', 'actionbar', [T(f'Wave {w} of 3', COL, bold=True), T(' - hold the room!', 'gray')])])
    fn('p267/vig/broken', ['execute as @a[distance=..32] if score @s bm.pid = #o bm.rng run ' + say('The spawner is gone - and with it, the little light inside. (The vigil is over.)'),
                           'kill @e[type=#bm:hostile,tag=bm.nxwv,distance=..32]', 'kill @s'])
    fn('p267/vig/left', ['execute as @a if score @s bm.pid = #o bm.rng run ' + say('You left the room - the soul lantern\'s spell fades. (Place another to begin again.)'),
                         'kill @e[type=#bm:hostile,tag=bm.nxwv,distance=..48]', 'kill @s'])
    fn('p267/vig/done', ['execute positioned ~ ~1 ~ run function bm:p267/enc/spawn',
                         'scoreboard players operation @e[type=minecraft:interaction,tag=bm.nxenc,distance=..2] bm.pid = #o bm.rng',
                         'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.3 0.3 0.03 20', 'particle minecraft:flame ~ ~1 ~ 0.2 0.2 0.2 0.04 12',
                         'playsound minecraft:block.trial_spawner.open_shutter block @a[distance=..24] ~ ~ ~ 1 1.2',
                         tellraw('@a[distance=..24]', [T('The third wave falls. In the spawner\'s cage the little light yawns - ', LINE, italic=True),
                                                       T('it is SO bored of making monsters - and hops out between the bars.', 'gray', italic=True)]), 'kill @s'])
    csay = lambda txt: title('@s', 'actionbar', [T('The Spawner: ', COL, bold=True), T(txt, LINE)])
    fn('p267/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('"You\'re not the one who sat with me through the waves."'),
                         f'execute if items entity @s container.* {X.holds(ITEM)} run return run ' + csay('"You\'ve got my pilot light already!"'),
                         f'execute as {X.here} at @s run particle minecraft:soul ~ ~0.6 ~ 0.3 0.3 0.3 0.02 10', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.6',
                         tellraw('@s', [T('It looks up at you - "I don\'t want to make monsters any more. Can I make FRIENDS?" - ', LINE, italic=True),
                                        T('and drops a little lantern into your hand, its own pilot light burning in it. It\'s coming with you.', 'gray', italic=True)]),
                         'function bm:p267/enc/joined'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/spawner_vigil', 'yellow'), T('  start the Spawner\'s vigil at the spawner you stand on/next to', 'gray')]))
    fn('admin/spawner_vigil', ['tag @s remove bm.nxmet', 'scoreboard players operation #me bm.pid = @s bm.pid'] + probe)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    frame = dict(models=FRAMES, every=1, click=['particle minecraft:soul ~ ~0.2 ~ 0.2 0.2 0.2 0.02 10', 'particle minecraft:large_smoke ~ ~0.2 ~ 0.1 0.1 0.1 0.01 4',
                                                'playsound minecraft:entity.bat.ambient block @a[distance=..12] ~ ~ ~ 0.6 1.8'])
    W5.build(Spawner, G, _abilities, _encounter, sitb=(80, [(0, 'sit_b'), (40, 'sit_b2')]), frame=frame)
    C, pfx, ab = Spawner, 'p267', 'nx'
    sel = f'bm.{ab}sel'
    psel = lambda p: f'@e[type=minecraft:item_display,tag={sel},tag=bm.{ab}p_{p}]'
    mine = f'@e[type=minecraft:wolf,tag=bm.{ab}pet]'
    csay = lambda txt: title('@s', 'actionbar', [T('The Spawner: ', COL, bold=True), T(txt, LINE)])
    # ---- its dress: the ember the colour of what it was last fed (the owner's bm.nzfd), before the wardrobe's look
    D_ = G.FUNCS[f'{pfx}/dress']
    k = D_.index('scoreboard players set #wk bm.rng 0')
    D_[k:k] = ['scoreboard players set #fd bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #fd bm.rng = @s bm.nzfd'] + \
              [f'execute if score #fd bm.rng matches {i} as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:sw_{p}{sfx}"'
               for i, (sfx, *_r) in [(0, ('',))] + list(FED.items()) for p in ('core', 'flame')]
    # ---- FEEDING: right-click it holding rotten flesh, string or a blaze rod
    W_ = G.FUNCS[f'{pfx}/who']
    k = next(i for i, l in enumerate(W_) if 'bm.pid = #me bm.pid run return run' in l)
    W_[k + 1:k + 1] = [f'execute if items entity @s weapon.mainhand {food} run return run function bm:p267/feed/{i}' for i, (_s, _k, food, *_r) in FED.items()]
    for i, (sfx, kind, food, word, col) in FED.items():
        fn(f'p267/feed/{i}', ['item modify entity @s weapon.mainhand {type:"minecraft:set_count",count:-1,add:true}', f'scoreboard players set @s bm.nzfd {i}',
                              'scoreboard players operation #me bm.pid = @s bm.pid',
                              f'execute as {mine} if score @s bm.pid = #me bm.pid at @s run function bm:p267/fed',
                              tellraw('@s', [T('It looks up, mouth open - the food drops in through the top bars - and it chews. ', LINE, italic=True),
                                             T(f'Its ember turns {word}: ', 'gray', italic=True), T(f'{kind.upper()} minions.', col, bold=True)])])
    fn('p267/fed', ['scoreboard players set @s bm.nza 12', 'scoreboard players set @s bm.nzx 22', f'function bm:{pfx}/form2',
                    'particle minecraft:large_smoke ~ ~0.8 ~ 0.1 0.1 0.1 0.02 6', 'playsound minecraft:entity.generic.eat neutral @a[distance=..12] ~ ~ ~ 0.8 1.2'])
    if f'{pfx}/form2' not in G.FUNCS:
        fn(f'{pfx}/form2', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!bm.{ab}fade] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                            f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}'])
    fn('admin/spawner_reset', ['tag @s remove bm.nxmet', 'scoreboard players set @s bm.nzfd 0', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                               title('@s', 'actionbar', T('The Spawner has not met you yet: a soul lantern beside a dungeon spawner, three waves held.', COL))])
