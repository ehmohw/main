"""2.98: THE GEM OF CREATIVITY - the follower. (gem_art.py: the emerald cut, its swirl animated; the Buddies it conjures:
gem_buddies_art.py, each a small 3D rig of its own; the machinery is rigpet's.)

The Gem made every Buddy there is. It has no face: it shows how it feels in TEXT, the way the owner imagined it - a little line
of emoticons floating over it: :) c: :o :3 o3o ^-^ ;( >:( -_- <3 and more, each for a mood (fighting, hurt, resting, playing,
happy to see you, you hurt...).

HOW IT COMES: when Mr. Capshun, Kettle and Emma walk with you at once (the trio, THE CREATIVE SPARK), the Gem notices: it comes
down to see what its first Buddy, its narrator and the princess are up to - and stays. (The Gem of Creativity: use it to call it.)
CONJURE (every 4 s, a foe within 14): one of its Buddies pops out of a sparkle at the monster - Grace's DIVE-PECK, Robo's ROCKET
  PUNCH, Zapper's ZAP, Dessa's FLASH-BURST, Bubbles' POP-SPLASH, Chase's TACKLE, Limer's BODY SLAM, Chico's SWING-WHACK, Spike's
  BUZZ-SAW DASH, Cheferoni's SLICE THROW - its own wind-up and strike (8, and each its own extra), and it pops away again.
PRISM (a foe within 3, every 1.5 s): a flash of colour off its facets (5).
INSPIRATION (out of a fight beside you, every minute): Haste and Luck for you - and a sparkle of creativity.
MASTERPIECE (charged, every minute and a half; three or more foes within 10): three Buddies at once.
THE CREATIVE FORMS: any Buddy - and five more besides - beside it takes on a creative form: a pair each (see CREATIVE)."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import gem_art as A
import gem_buddies_art as GB
import rigkit as RK
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase210 as FXS

CG_C, CG_LINE = '#5ae0a0', '#d8fff0'
W = 'gem'
ORDER = list(GB.RIGS)                    # (grace, robo, zapper, dessa, bubbles, chase, limer, chico, spike, cheferoni)
BNAME = {'grace': 'Grace', 'robo': 'Robo', 'zapper': 'Zapper', 'dessa': 'Dessa', 'bubbles': 'Bubbles', 'chase': 'Chase', 'limer': 'Limer',
         'chico': 'Chico', 'spike': 'Spike', 'cheferoni': 'Cheferoni'}
# each Buddy's strike: its own extra, at the struck foe (and the sound)
EXTRA = {'grace': (['effect give @s minecraft:levitation 1 0'], 'minecraft:entity.parrot.ambient'),
         'robo': ([f'execute facing entity @p feet rotated ~ 0 run tp @s ^ ^0.2 ^-2.5', 'particle minecraft:flame ~ ~1 ~ 0.2 0.2 0.2 0.04 12'], 'minecraft:entity.iron_golem.attack'),
         'zapper': (['effect give @s minecraft:slowness 3 2', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 30'], 'minecraft:entity.lightning_bolt.impact'),
         'dessa': (['effect give @s minecraft:blindness 3 0', 'effect give @s minecraft:glowing 5 0', 'particle minecraft:flash{color:[1.0,0.95,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1'], 'minecraft:block.glass.break'),
         'bubbles': (['effect give @s minecraft:slowness 3 1', 'particle minecraft:splash ~ ~1 ~ 0.6 0.6 0.6 0.3 40', 'particle minecraft:bubble_pop ~ ~1 ~ 0.5 0.5 0.5 0.1 20'], 'minecraft:entity.player.splash'),
         'chase': ([f'execute facing entity @p feet rotated ~ 0 run tp @s ^ ^0.3 ^-2', 'particle minecraft:item_slime ~ ~0.6 ~ 0.4 0.3 0.4 0.1 20'], 'minecraft:entity.slime.jump'),
         'limer': (['effect give @s minecraft:slowness 2 3', 'particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.2 ~ 0.8 0.1 0.8 0 30'], 'minecraft:entity.generic.big_fall'),
         'chico': (['effect give @s minecraft:nausea 4 0', 'particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.3 16'], 'minecraft:entity.player.attack.strong'),
         'spike': (['effect give @s minecraft:wither 3 0', 'particle minecraft:crit ~ ~1 ~ 0.5 0.3 0.5 0.4 24', 'particle minecraft:electric_spark ~ ~0.6 ~ 0.4 0.1 0.4 0.2 16'], 'minecraft:block.grindstone.use'),
         'cheferoni': (['effect give @s minecraft:slowness 2 0', 'particle minecraft:item{item:"minecraft:bread"} ~ ~1 ~ 0.3 0.3 0.3 0.1 16'], 'minecraft:entity.player.burp')}
# the puppet's timeline (ticks): appear, its wind-up, the strike, happy, gone
PUP = [(0, 'appear', 4), (5, 'idle_a', 4), (9, 'wind', 3), (13, 'strike', 2), (14, 'HIT', 0), (20, 'happy', 5), (27, 'vanish', 4), (32, 'GONE', 0)]
# the emoticons: (mood, the faces it picks from)
EMO = {'fight': ['>:(', '>:o', ':|'], 'hurt': [';(', 'D:', ':o'], 'rest': ['-_-', 'zZz', 'u_u'], 'conjure': ['\\o/', ':D', '*o*'],
       'love': ['<3', 'c:', '^-^'], 'idle': [':)', 'c:', ':3', 'o3o', '^-^', ':o', ';)', ':D', 'owo', 'o.o', 'O.o', 'o.O', 'o.e'], 'worry': [';(', ':c', 'T_T']}


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'The Gem of Creativity', CG_C, CG_LINE, 'p231', 'cg', 'cq'
    A = A
    MENU = 4400
    PET_HP, PET_CD = 40, 120
    ITEM = 'creativity_gem'
    pron, they = 'it', 'it'
    # (2.96a: its faces are its emoticons, on its table facet - gem_art.EMOTES; the moods everyone shares land on one of them,
    #  and m_<key> is each emoticon by name, for its own mood picks: p231/emo)
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious') + tuple(f'm_{k}' for k, _t in A.EMOTES)
    FACE = dict({'happy': 'caret', 'surprised': 'bigsmall', 'hurt': 'cry', 'sleepy': 'meh', 'blink': None, 'squint': 'angry', 'serious': 'flat'},
                **{f'm_{k}': (None if k == 'smile' else k) for k, _t in A.EMOTES})
    ATTRS = dict(armor=4, attack_damage=4, movement_speed=0.38, follow_range=32, step_height=1.1)
    SCALE = 0.7
    HIT = (0.6, 1.2)
    CYCLE = {0: (240, [(0, 'idle_a'), (60, 'idle_b'), (120, 'idle_a'), (180, 'idle_b')]),
             1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (480, [(0, 'sit_a'), (120, 'sit_b'), (160, 'sit_c'), (200, 'sit_b'), (240, 'sit_c'), (280, 'sit_a')]),
             6: (None, [(0, 'happy')]),
             7: (None, [(0, 'conjure_up'), (3, 'conjure')]),
             8: (None, [(0, 'conjure_up'), (6, 'conjure'), (14, 'idle_a')]),
             12: (None, [(0, 'conjure_up'), (8, 'conjure'), (14, 'conjure_up'), (20, 'conjure'), (30, 'happy')]),
             14: (None, [(0, 'happy'), (16, 'idle_b')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 20, 'idle_b': 20, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3,
           'jump': 4, 'sit_a': 30, 'sit_b': 40, 'sit_c': 40, 'happy': 10, 'conjure_up': 5, 'conjure': 3, 'hurt': 3, 'tired': 20}
    QUIPS = ['(the Gem twinkles: :D)', '(the Gem spins with delight: ^-^)', '(the Gem glows: c:)', '(the Gem sparkles: :3)', '(the Gem hums happily: o3o)']
    HELLO = ('(the Gem floats down to you, sparkling: :D)', '(a swirl of colour, and the Gem is there: ^-^)', '(the Gem twinkles goodbye and drifts off: c:)')
    SIT = ('(the Gem lifts and brightens: :)', '(the Gem settles low and dims: -_-)')
    FAINT = '(the Gem\'s light goes dim: ;(  )'
    NOT_YOURS = '(the Gem looks at you with a polite little :|)'
    POWERS = [('Conjure', 'every 4 s, a foe within 14: one of its Buddies pops out of a sparkle at it - its own attack (8, and its own extra)'),
              ('Prism', 'a foe within 3, every 1.5 s: a flash off its facets (5)'),
              ('Inspiration', 'out of a fight beside you, every minute: Haste and Luck for you'),
              ('Masterpiece', 'charged, every 90 s: three or more foes within 10 - three Buddies at once'),
              ('Creative Forms', 'any Buddy beside it (and Emma, Queen Ava, Democratus, KillerWatt, Queen Pearl) takes on a creative form')]
    INTRO = [T('The Gem of Creativity', CG_C, bold=True), T(' - it made every Buddy there is. ', 'gray'), T('It can\'t talk; it shows you how it feels :)', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.03 12', 'particle minecraft:dust{color:[0.4,1.0,0.7],scale:1.2} ~ ~1 ~ 0.4 0.4 0.4 0 10']
    FADE_SOUND = 'playsound minecraft:block.amethyst_block.chime neutral @a[distance=..20] ~ ~ ~ 1 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.amethyst_cluster.place neutral @a[distance=..24] ~ ~ ~ 1 1.2']
    ENC_POSES = [(0, 'idle_a'), (40, 'happy'), (60, 'idle_b')]
    ADV = ('The Creative Spark', 'The Gem of Creativity comes to you')
    ADMIN_HINT = 'Walk with Mr. Capshun, Kettle and Emma at once.'
    MEET_HINT = 'Mr. Capshun, Kettle and Emma, together.'


RP.register(C)
item('creativity_gem', TOTEM, 'The Gem of Creativity', CG_C,
     ['An emerald-cut gem, and all the colours there are swirling inside it.', 'Every Buddy began here.',
      ('Use: call the Gem (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'), ('It conjures its Buddies to fight beside you.', 'blue'),
      ('If it dims: 2 minutes before it can return.', 'gray'), ('(it says: :) )', 'dark_gray')],
     model='bm:creativity_gem', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_gem', TOTEM, 'Gem of Creativity Doll', CG_C, ['A little plush gem - it still swirls, somehow.', ('Right-click a block: set it down.', 'blue'),
                                                         ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_gem', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_gem'] = 'bm:p141/doll_gem/use'
P141.DOLLS.append(('doll_gem', 'The Gem of Creativity', CG_C, 'A little plush gem - it still swirls, somehow.', 'minecraft:end_rod',
                   'minecraft:block.amethyst_block.chime', 'minecraft:poof'))
P141.DOLL_FROM['doll_gem'] = ('creativity_gem', {'kh': 1.3, 'kb': 0.9, 'kl': 0.8, 'groups': {'bm:cg_body': 'head'}, 'height': 7.0})   # (a gem: no legs to shorten, so it stood as tall as the set - a little smaller, like a plush)
P134.FIT['creativity_gem'] = (0.0, 1.2, -0.4, 0.4, -0.4, 0.4)
POSES = A.POSES

# ---- the trio that brings it: Mr. Capshun, Kettle and Emma - THE CREATIVE SPARK
import phase100 as P100
import phase188 as P188
P188.VNAME['gem'] = 'The Gem'
P100.VOICE['The Gem'] = (CG_C, CG_LINE)
P100.TRIOS['creative_spark'] = ('The Creative Spark', CG_C, ('capshun', 'kettle', 'emma'), 'The Creative Spark', 'Walk with Mr. Capshun, Kettle and Emma at once')
P188.ICON['creative_spark'] = 'bm:creativity_gem'
P100.BANTER['creative_spark'] = [('Mr. Capshun', '[Mr. Capshun narrates: "The narrator, the first Buddy and the princess - the story is about to get creative."]', 'Kettle', '"What does creative mean? Is it a game?"'),
                                 ('Emma', 'Kettle, you were the very first Buddy? Ever?', 'Kettle', '"The FIRST! Before anyone! Before breakfast, even!"')]


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image
    T_ = A.textures()
    im = T_['cg_table'].crop((0, 0, 64, 64)) if 'cg_table' in T_ else Image.new('RGBA', (32, 32), (90, 224, 160, 255))
    return im.resize((32, 32), Image.LANCZOS)


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    for n, rig in GB.RIGS.items():                       # (the Buddies: their parts as models)
        for name, (tex, els) in rig.models().items():
            R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + tuple(f'gz_{n}_' for n in GB.RIGS)
    R.POST.append(lambda R2: A.write_mcmeta(R2))


def textures():
    T_ = dict(A.textures())
    for rig in GB.RIGS.values():
        T_.update(rig.textures())
    return T_


def generate_early(G):
    RP.contract(C, G)


def _xf(rig, pose, part, scale):
    """a Buddy part's transformation for a pose (as the figurines are posed: the solved hierarchy)"""
    U = scale / 16
    xf = RK.solve(rig.PIVOT, rig.PARENT, pose)
    x, y, z = rig.PIVOT[part]
    q, t = xf[part]
    tr = (-x * U + t[0] * U, y * U + t[1] * U, -z * U + t[2] * U)
    return (f'left_rotation:[{q[0]:.4f}f,{q[1]:.4f}f,{q[2]:.4f}f,{q[3]:.4f}f],right_rotation:[0f,0f,0f,1f],'
            f'translation:[{tr[0]:.4f}f,{tr[1]:.4f}f,{tr[2]:.4f}f],scale:[{scale:.4f}f,{scale:.4f}f,{scale:.4f}f]')


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    pet = 'bm.cgpet'
    objs = ['bm.cgbt', 'bm.cgbk', 'bm.cgbid', 'bm.cgemt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'

    # ================================================================== THE BUDDIES: a puppet each - its parts at the foe, posed by the timeline
    # (as a marker, bm.cgbd: bm.cgbk which Buddy, bm.cgbt its clock, bm.cgbid its id - its parts carry the same id; bm.pid the summoner)
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #cgbid bm.rng 0']
    for k, n in enumerate(ORDER, 1):
        rig = GB.RIGS[n]
        S = rig.RIG_SCALE * 1.0
        grow = GB.GROW
        def part_nbt(p, pose, sc):
            return {'Tags': ['bm.cgbd', 'bm.cgbdp', 'bm.cgbdnew', f'bm.cgbd_{p}'], 'item': {'id': 'minecraft:paper', 'count': Int(1),
                    'components': {'minecraft:item_model': f'bm:{rig.model_name(p, pose)}'}}, 'item_display': 'fixed', 'teleport_duration': Int(1),
                    'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(1.2), 'interpolation_duration': Int(3)}
        appear = rig.POSES['appear']
        sp = [f'summon minecraft:item_display ~ ~ ~ {snbt(part_nbt(p, appear, S))}' for p in rig.PARTS]
        sp += ['scoreboard players operation @e[type=minecraft:item_display,tag=bm.cgbdnew,distance=..1] bm.cgbid = #cgbid bm.rng',
               'execute as @e[type=minecraft:item_display,tag=bm.cgbdnew,distance=..1] run tp @s ~ ~ ~ ~ 0',
               'tag @e[type=minecraft:item_display,tag=bm.cgbdnew,distance=..1] remove bm.cgbdnew']
        fn(f'p231/bd/{n}/spawn', sp)
        for t, pose_name, dur in PUP:
            if pose_name in ('HIT', 'GONE'): continue
            pose = rig.POSES.get(pose_name) or rig.POSES['idle_a']
            g = {'appear': grow['appear'][2], 'vanish': grow['vanish'][2]}.get(pose_name, 1.0)
            L = []
            for p in rig.PARTS:
                if rig.HIDDEN(p, pose):
                    L.append(f'execute as @e[type=minecraft:item_display,tag=bm.cgbd_{p},distance=..4] if score @s bm.cgbid = #bid bm.rng run data merge entity @s '
                             f'{{start_interpolation:0,interpolation_duration:{dur},transformation:{{scale:[0f,0f,0f]}}}}')
                    continue
                L.append(f'execute as @e[type=minecraft:item_display,tag=bm.cgbd_{p},distance=..4] if score @s bm.cgbid = #bid bm.rng run data merge entity @s '
                         f'{{start_interpolation:0,interpolation_duration:{dur},item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"bm:{rig.model_name(p, pose)}"}}}},'
                         f'transformation:{{{_xf(rig, pose, p, S * max(g, 0.001))}}}}}')
            fn(f'p231/bd/{n}/pose_{pose_name}', L)
        # the strike: 8 and its own extra, as the Gem (its pid: the summoner's)
        ex, snd = EXTRA[n]
        fn(f'p231/bd/{n}/hit', ['scoreboard players operation #me bm.pid = @s bm.pid',
                                f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add bm.cgme',
                                f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:p231/bd/{n}/struck',
                                'tag @e[tag=bm.cgme] remove bm.cgme', f'playsound {snd} neutral @a[distance=..20] ~ ~ ~ 1 1.1'])
        fn(f'p231/bd/{n}/struck', ['damage @s 8 minecraft:mob_attack by @e[type=minecraft:wolf,tag=bm.cgme,limit=1]'] + ex)
        tl = []
        for t, pose_name, dur in PUP:
            if pose_name == 'HIT': tl.append(f'execute if score @s bm.cgbt matches {t} run function bm:p231/bd/{n}/hit')
            elif pose_name == 'GONE': tl.append(f'execute if score @s bm.cgbt matches {t}.. run function bm:p231/bd/gone')
            else: tl.append(f'execute if score @s bm.cgbt matches {t} run function bm:p231/bd/{n}/pose_{pose_name}')
        fn(f'p231/bd/{n}/tick', tl)
    # (at a foe, #me the summoner's pid: a random Buddy conjured there - a marker for its clock, its parts round it, facing the Gem)
    fn('p231/bd/conjure', ['execute store result score #bk bm.rng run random value 1..10', 'scoreboard players add #cgbid bm.rng 1',
                           'summon minecraft:marker ~ ~ ~ {Tags:["bm.cgbdm","bm.cgbdnew"]}',
                           'execute as @e[type=minecraft:marker,tag=bm.cgbdnew,distance=..1] run function bm:p231/bd/mark'] +
       [f'execute if score #bk bm.rng matches {k} run function bm:p231/bd/{n}/spawn' for k, n in enumerate(ORDER, 1)] +
       [FXS.fx('cg_conjure', 1.6, 0.8) if 'cg_conjure' in FXS.names() else 'particle minecraft:end_rod ~ ~0.8 ~ 0.4 0.4 0.4 0.05 16',
        'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..24] ~ ~ ~ 1 1.6'])
    fn('p231/bd/mark', ['tag @s remove bm.cgbdnew', 'scoreboard players operation @s bm.cgbk = #bk bm.rng', 'scoreboard players operation @s bm.cgbid = #cgbid bm.rng',
                        'scoreboard players operation @s bm.pid = #me bm.pid', 'scoreboard players set @s bm.cgbt 0'])
    G.FUNCS['tick'].append('execute as @e[type=minecraft:marker,tag=bm.cgbdm] at @s run function bm:p231/bd/tick')
    fn('p231/bd/tick', ['scoreboard players add @s bm.cgbt 1', 'scoreboard players operation #bid bm.rng = @s bm.cgbid'] +
       [f'execute if score @s bm.cgbk matches {k} run function bm:p231/bd/{n}/tick' for k, n in enumerate(ORDER, 1)])
    fn('p231/bd/gone', ['execute as @e[type=minecraft:item_display,tag=bm.cgbdp,distance=..4] if score @s bm.cgbid = #bid bm.rng run kill @s',
                        'particle minecraft:end_rod ~ ~0.6 ~ 0.3 0.3 0.3 0.02 8', 'kill @s'])
    G.FUNCS['loop/second'].append('execute as @e[type=minecraft:marker,tag=bm.cgbdm,scores={bm.cgbt=80..}] at @s run function bm:p231/bd/gone')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[tag=bm.cgbd]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:marker,tag=bm.cgbdm]')

    def abilities(G, X):
        S, go, hit, end, face, pfx = X.S, X.go, X.hit, X.end, X.face, X.pfx
        idle = X.idle_fight
        lines = [f'execute if score @s {S("k")} matches 1.. run scoreboard players remove @s {S("k")} 1',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..10]',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if score #nf bm.rng matches 3.. run function bm:{pfx}/master_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/prism_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. if entity @e[{foe},distance=..14] run function bm:{pfx}/conj_go',
                 f'execute {idle} unless score @s {S("k")} matches 1.. unless entity @e[{foe},distance=..12] if function bm:{pfx}/near_owner run function bm:{pfx}/insp_go']
        fn(f'{pfx}/near_owner', ['execute on owner if entity @s[distance=..8] run return 1', 'return 0'])
        fn(f'{pfx}/prism_go', go(7, 6, 'mc', 30, []))
        fn(f'{pfx}/conj_go', go(8, 16, 'rc', 80, ['scoreboard players set @s bm.cgemt 30']))
        fn(f'{pfx}/master_go', go(12, 32, 'gc', 1800, ['scoreboard players set @s bm.cgemt 40',
                                                        'execute on owner if entity @s[distance=..24] run ' + X.csay('(\\o/ - a masterpiece!)')]))
        fn(f'{pfx}/insp_go', go(14, 20, 'k', 1200, []))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 3 run function bm:{pfx}/prism',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 10 run function bm:{pfx}/conj',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 24 run function bm:{pfx}/conj',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/conj',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 12 run function bm:{pfx}/conj',
                               f'execute if score @s {S("a")} matches 14 if score @s {S("x")} matches 10 run function bm:{pfx}/insp'])
        fn(f'{pfx}/prism', hit(5) + [f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] at @s run function bm:{pfx}/prismed'] + end)
        fn(f'{pfx}/prismed', [f'function bm:{pfx}/hurt', 'particle minecraft:dust{color:[1.0,0.3,0.6],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 6',
                              'particle minecraft:dust{color:[0.3,0.7,1.0],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 6', 'particle minecraft:dust{color:[0.4,1.0,0.5],scale:1.0} ~ ~1 ~ 0.3 0.4 0.3 0 6',
                              'playsound minecraft:block.amethyst_block.hit neutral @a[distance=..16] ~ ~ ~ 1 1.4'])
        # (a Buddy at the monster - a random one near it, facing the Gem)
        fn(f'{pfx}/conj', [f'execute as @e[{foe},distance=..14,sort=random,limit=1] at @s facing entity @e[type=minecraft:wolf,tag={pet},distance=..16,sort=nearest,limit=1] feet '
                           f'rotated ~ 0 positioned ^ ^ ^1.1 run function bm:p231/bd/conjure_as',
                           f'function bm:{pfx}/blow'])
        fn('p231/bd/conjure_as', ['execute as @e[type=minecraft:wolf,tag=bm.cgpet,distance=..16,sort=nearest,limit=1] run scoreboard players operation #me bm.pid = @s bm.pid',
                                  'function bm:p231/bd/conjure'])
        fn(f'{pfx}/insp', ['execute on owner if entity @s[distance=..8] run function bm:p231/insp_you',
                           FXS.fx('cg_sparkle', 1.4, 1.0) if 'cg_sparkle' in FXS.names() else 'particle minecraft:end_rod ~ ~1 ~ 0.4 0.4 0.4 0.03 12'])
        fn('p231/insp_you', ['effect give @s minecraft:haste 60 0 true', 'effect give @s minecraft:luck 60 0 true',
                             'particle minecraft:end_rod ~ ~1.2 ~ 0.3 0.4 0.3 0.02 10', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.6'])
        return lines

    def encounter(G, X):
        # (it comes when the Creative Spark forms: Capshun, Kettle and Emma together - p100/creative_spark gives it once)
        fn('p231/enc/talk', [X.csay('(:o)')])

    RP.build(C, G, abilities, encounter)
    del G.FUNCS['p231/enc/joined']
    X = RP.X

    # ================================================================== THE CREATIVE SPARK: its buffs - and, once, the Gem comes
    REGEN = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    mine = lambda k: f'@e[type=minecraft:{P100.WHO[k][0]},tag={P100.WHO[k][1]},distance=..24]'
    fn('p100/creative_spark', ['effect give @s minecraft:haste 3 0 true', 'effect give @s minecraft:luck 3 0 true', 'effect give @s minecraft:speed 3 0 true'] +
       [f'execute as {mine(m)} if function bm:p100/is_mine run {REGEN}' for m in ('capshun', 'kettle', 'emma')] +
       ['execute unless entity @s[tag=bm.cgmet] at @s run function bm:p231/arrives', 'function bm:p100/banter_tick'])
    _cinematic(G, X)
    wjson('bm/advancement/story/trio_creative_spark.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
                                                         'display': {'icon': {'id': 'minecraft:totem_of_undying', 'components': {'minecraft:item_model': 'bm:creativity_gem'}},
                                                                     'title': T('The Creative Spark', 'yellow'), 'description': T('Walk with Mr. Capshun, Kettle and Emma at once', 'gray'),
                                                                     'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})

    # ================================================================== ITS FEELINGS: an emoticon on its face, by mood (each second)
    # (2.96a: on the gem itself - its head's faces, gem_art.EMOTES - where a line of text floated over it before)
    import phase95 as FX
    KEY = {t: k for k, t in A.EMOTES}
    assert all(t in KEY for faces in EMO.values() for t in faces), [t for faces in EMO.values() for t in faces if t not in KEY]
    G.FUNCS['loop/second'].append(f'execute as @e[type=minecraft:wolf,tag={pet}] at @s run function bm:p231/emo/sec')
    pick = lambda mood: ([f'execute store result score #e bm.rng run random value 1..{len(EMO[mood])}'] +
                         [f'execute if score #e bm.rng matches {i + 1} run return run function bm:p231/emo/x/{KEY[e]}' for i, e in enumerate(EMO[mood])])
    for mood in EMO:
        fn(f'p231/emo/{mood}', pick(mood))
    for k, _t in A.EMOTES:
        fn(f'p231/emo/x/{k}', FX.face_cmd(W, f'm_{k}', 30))
    fn('p231/emo/sec', ['execute if score @s bm.cgemt matches 1.. run scoreboard players remove @s bm.cgemt 1',
                        'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #lowhp bm.rng 0',
                        'execute on owner store result score #ph bm.rng run data get entity @s Health', 'execute if score #ph bm.rng matches ..6 run scoreboard players set #lowhp bm.rng 1',
                        'execute store result score #mh bm.rng run data get entity @s Health', 'execute store result score #mm bm.rng run attribute @s minecraft:max_health get',
                        'scoreboard players operation #mm bm.rng /= #3 bm.rng',
                        'execute if score @s bm.cgemt matches 1.. run return run function bm:p231/emo/conjure',
                        'execute if score #lowhp bm.rng matches 1 run return run function bm:p231/emo/worry',
                        'execute if score #mh bm.rng < #mm bm.rng run return run function bm:p231/emo/hurt',
                        'execute if data entity @s {Sitting:1b} run return run function bm:p231/emo/rest',
                        f'execute if entity @e[{foe},distance=..10] run return run function bm:p231/emo/fight',
                        'execute store result score #r bm.rng run random value 1..4', 'execute unless score #r bm.rng matches 1 run return 0',
                        'execute on owner if entity @s[distance=..3] run return run function bm:p231/emo/love',
                        'function bm:p231/emo/idle'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3']
    # (the line of text it wore before 2.96a: put out wherever one is left)
    G.FUNCS['loop/second'].append('kill @e[type=minecraft:text_display,tag=bm.cgemo]')
    G.FUNCS['admin/uninstall'].insert(0, 'kill @e[type=minecraft:text_display,tag=bm.cgemo]')

    # ================================================================== (3.0a) THE HALO: always circling (gem_art.HALO_TURN)
    _spin(G)


SPIN_N = 24                                     # (the halo's spin: SPIN_N steps a turn, each its own interpolated ticks)
SPIN_K = A.HALO_TURN // SPIN_N                  # (5 ticks a step: 15 deg)


def _yq(deg):
    h = math.radians(deg) / 2
    return [F(0), F(round(math.sin(h), 5)), F(0), F(round(math.cos(h), 5))]


def _spin(G):
    """(3.0a) the white squares, the halo's glints, circle the gem without stopping. Every SPIN_K ticks, each halo display's
    right_rotation steps a little further round the vertical, interpolated over those same ticks. The poses only ever set
    its left_rotation, translation and scale, so the turn rides on top of every pose. This runs after the followers' own tick,
    so a step taken in the same tick as a pose keeps its own pace. The halos: the Gem's rig (bm.cgp_halo) and the cinematic's
    (bm.cgcz_halo)."""
    fn = G.fn
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.cgsp dummy', f'scoreboard players set #k bm.cgsp {SPIN_K}']
    G.OBJECTIVES.append('bm.cgsp')
    G.FUNCS['tick'] += ['scoreboard players add #t bm.cgsp 1', f'execute if score #t bm.cgsp matches {SPIN_N * SPIN_K}.. run scoreboard players set #t bm.cgsp 0',
                        'scoreboard players operation #m bm.cgsp = #t bm.cgsp', 'scoreboard players operation #m bm.cgsp %= #k bm.cgsp',
                        'execute if score #m bm.cgsp matches 0 run function bm:p231/spin']
    fn('p231/spin', ['scoreboard players operation #s bm.cgsp = #t bm.cgsp', 'scoreboard players operation #s bm.cgsp /= #k bm.cgsp'] +
       [f'execute if score #s bm.cgsp matches {k} run return run function bm:p231/spin/{k}' for k in range(SPIN_N)])
    for k in range(SPIN_N):
        m = f'data merge entity @s {{start_interpolation:0,interpolation_duration:{SPIN_K},transformation:{{right_rotation:{snbt(_yq(360.0 * k / SPIN_N))}}}}}'
        fn(f'p231/spin/{k}', [f'execute as @e[type=minecraft:item_display,tag=bm.cgp_halo,tag=!bm.cgfade] run {m}',
                              f'execute as @e[type=minecraft:item_display,tag=bm.cgcz_halo] run {m}'])


# ---------------------------------------------------------------------------------------------------- (3.0a) THE GEM COMES DOWN
# A short scene (CIN_END ticks, 9 s), played round the player where they stand. The camera is never taken, and they can walk:
# the scene follows them. DOWN (0-100): high in the sky (26 up, 4 out) the Gem shines, then sinks slowly in a wide, tightening
# spiral, trailing sparkles, with a chime at every step down, each higher. SWIRL (101-160): twice round you at shoulder height,
# 2 out, rings of rainbow rising round you. RISE (161-180): in over your head and up. Then it DROPS: the summoning item,
# as an item entity just over your head, falls into your hands. Only you can pick it up (its Owner), it can't burn, and if it
# hasn't reached you within CIN_LATE ticks of the start (30 s after it drops), it is given to you directly. Nothing is given
# before then: the drop is the reward.
# (a marker, bm.cgcin, carries the clock (bm.cgct), the turn (bm.cgca, tenths of a degree) and the player's pid; the gem is three
#  displays (bm.cgcz: the body, the face (:D), the halo), set every tick by a macro: rotated by the turn, up by the height,
#  out by the radius. The player waits under bm.cgwait (bm.cgwt counts their ticks) until the Gem is in their inventory.)
CIN_DOWN, CIN_SWIRL, CIN_END = 100, 160, 180
CIN_LATE = CIN_END + 600
RAINBOW = ['1.0,0.3,0.35', '1.0,0.65,0.2', '1.0,0.95,0.3', '0.4,1.0,0.5', '0.35,0.75,1.0', '0.75,0.45,1.0']


def _cinematic(G, X):
    fn, tellraw, title = G.fn, G.tellraw, G.title
    objs = ['bm.cgct', 'bm.cgca', 'bm.cgwt']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + \
        [f'scoreboard players set #{n} bm.cgct {n}' for n in (6, 10, 20, 1000)]
    G.OBJECTIVES += objs
    ME = '@a[tag=bm.cgcme,limit=1]'
    DISP = '@e[type=minecraft:item_display,tag=bm.cgcsel]'
    has_gem = [f'execute if items entity @s {sl} *[minecraft:custom_data~{{bm:"creativity_gem"}}] run return 1' for sl in ('container.*', 'weapon.offhand', 'player.cursor')]

    def disp(p, model, extra=None):
        n = {'Tags': ['bm.cgcz', 'bm.cgcznew', f'bm.cgcz_{p}'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': dict({'minecraft:item_model': model}, **(extra or {}))},
             'item_display': 'fixed', 'teleport_duration': Int(2), 'interpolation_duration': Int(0), 'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(4.0),
             'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0)] * 3, 'scale': [F(0)] * 3}}
        return f'summon minecraft:item_display ~ ~ ~ {snbt(n)}'
    scale = lambda s, d: f'execute as {DISP} run data merge entity @s {{start_interpolation:0,interpolation_duration:{d},transformation:{{scale:[{s}f,{s}f,{s}f]}}}}'

    # ---- it begins (as the player, once: p100/creative_spark, the first time the trio forms)
    fn('p231/arrives', ['tag @s add bm.cgmet', 'tag @s add bm.cgwait', 'scoreboard players set @s bm.cgwt 0',
                        'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                        'function bm:p231/cin/end_mine',
                        'summon minecraft:marker ~ ~ ~ {Tags:["bm.cgcin","bm.cgcznew"]}',
                        'execute positioned ~ ~26 ~ run function bm:p231/cin/spawn',
                        'execute as @e[tag=bm.cgcznew] run scoreboard players operation @s bm.pid = #me bm.pid',
                        'scoreboard players set @e[type=minecraft:marker,tag=bm.cgcznew] bm.cgct 0',
                        'execute store result score @e[type=minecraft:marker,tag=bm.cgcznew] bm.cgca run data get entity @s Rotation[0] 10',
                        'tag @e[tag=bm.cgcznew] remove bm.cgcznew',
                        'playsound minecraft:block.beacon.activate player @s ~ ~ ~ 1 1.6', 'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 0.6',
                        tellraw('@s', [T('High above you, something shines - and a swirl of every colour comes down out of the sky: ', CG_LINE, italic=True),
                                       T('the Gem of Creativity', CG_C, bold=True), T(', come to see its first Buddy, its narrator and the princess.', CG_LINE, italic=True)]),
                        title('@s', 'actionbar', T('(look up!)', CG_LINE))])
    fn('p231/cin/spawn', [disp('body', 'bm:cg_body'), disp('head', 'bm:cg_head', {'minecraft:custom_model_data': {'strings': ['m_grin']}}), disp('halo', 'bm:cg_halo')])
    # (as anyone, #me the pid: any scene of theirs still playing, ended; any drop of theirs, gone)
    fn('p231/cin/end_mine', ['execute as @e[type=minecraft:marker,tag=bm.cgcin] if score @s bm.pid = #me bm.pid run kill @s',
                             'execute as @e[type=minecraft:item_display,tag=bm.cgcz] if score @s bm.pid = #me bm.pid run kill @s',
                             'execute as @e[type=minecraft:item,tag=bm.cgdrop] if score @s bm.pid = #me bm.pid run kill @s'])

    # ---- the scene, each tick (as its marker): follows the player; the path; the cues
    G.FUNCS['tick'] += ['execute as @e[type=minecraft:marker,tag=bm.cgcin] at @s run function bm:p231/cin/tick',
                        'execute as @a[tag=bm.cgwait] at @s run function bm:p231/cin/wait']
    fn('p231/cin/tick', ['scoreboard players add @s bm.cgct 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:item_display,tag=bm.cgcz] if score @s bm.pid = #me bm.pid run tag @s add bm.cgcsel',
                         'execute as @a[tag=bm.cgwait] if score @s bm.pid = #me bm.pid run tag @s add bm.cgcme',
                         f'execute unless entity {ME} run return run function bm:p231/cin/gone',
                         f'tp @s {ME}',
                         'function bm:p231/cin/path',
                         'execute at @s run function bm:p231/cin/put with storage bm:tmp cgc',
                         'execute at @s run function bm:p231/cin/cue',
                         f'execute if score @s bm.cgct matches {CIN_END}.. at @s run function bm:p231/cin/drop',
                         f'tag {DISP} remove bm.cgcsel', 'tag @a[tag=bm.cgcme] remove bm.cgcme'])
    fn('p231/cin/gone', [f'kill {DISP}', 'kill @s'])
    # the path: #h the height, #r the radius (thousandths of a block), the turn's step (tenths of a degree a tick)
    fn('p231/cin/path', ['scoreboard players operation #ct bm.cgct = @s bm.cgct',
                         f'execute if score #ct bm.cgct matches ..{CIN_DOWN} run function bm:p231/cin/p_down',
                         f'execute if score #ct bm.cgct matches {CIN_DOWN + 1}..{CIN_SWIRL} run function bm:p231/cin/p_swirl',
                         f'execute if score #ct bm.cgct matches {CIN_SWIRL + 1}.. run function bm:p231/cin/p_rise',
                         'scoreboard players operation @s bm.cgca += #cst bm.cgct',
                         'execute store result storage bm:tmp cgc.h double 0.001 run scoreboard players get #ch bm.cgct',
                         'execute store result storage bm:tmp cgc.r double 0.001 run scoreboard players get #cr bm.cgct',
                         'execute store result storage bm:tmp cgc.a float 0.1 run scoreboard players get @s bm.cgca'])
    # DOWN: d = 100 - t; the height 1.6 + 24.4 (d/100)^2 (slowing as it nears), out 4 -> 2, the turn 4 -> 12 deg a tick
    fn('p231/cin/p_down', [f'scoreboard players set #cd bm.cgct {CIN_DOWN}', 'scoreboard players operation #cd bm.cgct -= #ct bm.cgct',
                           'scoreboard players operation #ch bm.cgct = #cd bm.cgct', 'scoreboard players operation #ch bm.cgct *= #cd bm.cgct',
                           'scoreboard players set #ck bm.cgct 244', 'scoreboard players operation #ch bm.cgct *= #ck bm.cgct',
                           'scoreboard players operation #ch bm.cgct /= #1000 bm.cgct', 'scoreboard players add #ch bm.cgct 1600',
                           'scoreboard players operation #cr bm.cgct = #cd bm.cgct', 'scoreboard players operation #cr bm.cgct *= #20 bm.cgct', 'scoreboard players add #cr bm.cgct 2000',
                           'scoreboard players operation #cst bm.cgct = #ct bm.cgct', 'scoreboard players set #ck bm.cgct 8', 'scoreboard players operation #cst bm.cgct *= #ck bm.cgct',
                           'scoreboard players operation #cst bm.cgct /= #10 bm.cgct', 'scoreboard players add #cst bm.cgct 40'])
    # SWIRL: twice round you (60 ticks, 12 deg a tick), shoulder high, 2 out
    fn('p231/cin/p_swirl', ['scoreboard players set #ch bm.cgct 1600', 'scoreboard players set #cr bm.cgct 2000', 'scoreboard players set #cst bm.cgct 120'])
    # RISE: u = t - 160: in over your head (2 -> 0 out) and up (1.6 -> 3.0), slowing its turn
    fn('p231/cin/p_rise', ['scoreboard players operation #cu bm.cgct = #ct bm.cgct', f'scoreboard players remove #cu bm.cgct {CIN_SWIRL}',
                           f'execute if score #cu bm.cgct matches {CIN_END - CIN_SWIRL}.. run scoreboard players set #cu bm.cgct {CIN_END - CIN_SWIRL}',
                           'scoreboard players set #ck bm.cgct 100', 'scoreboard players operation #cr bm.cgct = #cu bm.cgct', 'scoreboard players operation #cr bm.cgct *= #ck bm.cgct',
                           'scoreboard players set #ck bm.cgct 2000', 'scoreboard players operation #ck bm.cgct -= #cr bm.cgct', 'scoreboard players operation #cr bm.cgct = #ck bm.cgct',
                           'scoreboard players set #ck bm.cgct 70', 'scoreboard players operation #ch bm.cgct = #cu bm.cgct', 'scoreboard players operation #ch bm.cgct *= #ck bm.cgct',
                           'scoreboard players add #ch bm.cgct 1600',
                           'scoreboard players operation #cst bm.cgct = #cu bm.cgct', 'scoreboard players set #ck bm.cgct 3', 'scoreboard players operation #cst bm.cgct *= #ck bm.cgct',
                           'scoreboard players set #ck bm.cgct 120', 'scoreboard players operation #ck bm.cgct -= #cst bm.cgct', 'scoreboard players operation #cst bm.cgct = #ck bm.cgct'])
    # (as the marker, at the player) the gem where the path puts it, facing you; its trail there
    fn('p231/cin/put', ['$execute rotated $(a) 0 positioned ^ ^$(h) ^$(r) run function bm:p231/cin/at_gem'])
    trail = [f'execute if score #cf bm.cgct matches {i} run particle minecraft:dust{{color:[{c}],scale:1.4}} ~ ~ ~ 0.12 0.12 0.12 0 2' for i, c in enumerate(RAINBOW)]
    fn('p231/cin/at_gem', [f'execute facing entity {ME} eyes run tp {DISP} ~ ~ ~ ~ ~',
                           'scoreboard players operation #cf bm.cgct = @s bm.cgct', 'scoreboard players operation #cf bm.cgct %= #6 bm.cgct'] + trail +
       ['particle minecraft:end_rod ~ ~ ~ 0.1 0.1 0.1 0.01 1',
        'scoreboard players operation #cf bm.cgct = @s bm.cgct', 'scoreboard players operation #cf bm.cgct %= #20 bm.cgct',
        f'execute if score #cf bm.cgct matches 0 if score @s bm.cgct matches ..{CIN_SWIRL} run ' + (FXS.fx('cg_sparkle', 1.6, 0.0) if 'cg_sparkle' in FXS.names() else 'particle minecraft:wax_off ~ ~ ~ 0.3 0.3 0.3 1 8')])
    # the cues: the gem growing in, chimes climbing as it comes down, rings round you as it swirls, the rise
    cue = [f'execute if score @s bm.cgct matches 1 run {scale(1.4, 30)}',
           f'execute if score @s bm.cgct matches {CIN_DOWN} run {scale(0.9, 20)}',
           f'execute if score @s bm.cgct matches {CIN_SWIRL + 5} run {scale(0.5, 15)}']
    for i, t in enumerate(range(20, CIN_DOWN + 1, 20)):
        cue.append(f'execute if score @s bm.cgct matches {t} run playsound minecraft:block.amethyst_block.chime player {ME} ~ ~ ~ 1 {0.8 + 0.2 * i:.1f}')
    for i, t in enumerate(range(CIN_DOWN + 1, CIN_SWIRL + 1, 10)):
        cue += [f'execute if score @s bm.cgct matches {t} run function bm:p231/cin/ring_{i}',
                f'execute if score @s bm.cgct matches {t} run playsound minecraft:block.note_block.chime player {ME} ~ ~ ~ 0.8 {1.0 + 0.15 * i:.2f}']
        y = 0.2 + 0.35 * i
        fn(f'p231/cin/ring_{i}', [f'execute rotated {a} 0 positioned ^ ^{y:.2f} ^1.6 run particle minecraft:dust{{color:[{RAINBOW[(k + i) % 6]}],scale:1.2}} ~ ~ ~ 0.05 0.05 0.05 0 2'
                                  for k, a in enumerate(range(0, 360, 30))] + ['particle minecraft:end_rod ~ ~1 ~ 0.6 0.6 0.6 0.02 6'])
    cue += [f'execute if score @s bm.cgct matches {CIN_DOWN + 1} run ' + tellraw(ME, [T('It swirls round you, sparkling, every colour there is. ', CG_LINE, italic=True), T(':D', '#ffffff', bold=True)]),
            f'execute if score @s bm.cgct matches {CIN_DOWN + 1} run ' + (FXS.fx('cg_doodles', 1.6, 1.0) if 'cg_doodles' in FXS.names() else 'particle minecraft:end_rod ~ ~1 ~ 0.6 0.6 0.6 0.02 12'),
            f'execute if score @s bm.cgct matches {CIN_DOWN + 20} run ' + tellraw(ME, [T('Mr. Capshun: ', '#f0f0f0', bold=True), T('"[Mr. Capshun narrates: \'And the Gem chose them. Obviously. Look at them.\']"', '#d8e4ff')]),
            f'execute if score @s bm.cgct matches {CIN_DOWN + 45} run ' + tellraw(ME, [T('Kettle: ', '#8ad8ff', bold=True), T('"It\'s the GEM! It made me! Hi, Gem! HI!"', '#e0f4ff')]),
            f'execute if score @s bm.cgct matches {CIN_SWIRL + 1} run playsound minecraft:block.beacon.power_select player {ME} ~ ~ ~ 1 1.6',
            f'execute if score @s bm.cgct matches {CIN_SWIRL + 1}.. run particle minecraft:end_rod ~ ~2.2 ~ 0.3 0.4 0.3 0.02 2']
    fn('p231/cin/cue', cue)
    # the DROP (as the marker, at the player): the summoning item just over their head (or at their chest, under a low roof)
    fn('p231/cin/drop', ['execute positioned ~ ~2.9 ~ if block ~ ~ ~ #bm:grap_pass run return run function bm:p231/cin/drop_here',
                         'execute positioned ~ ~1.2 ~ run function bm:p231/cin/drop_here'])
    fn('p231/cin/drop_here', ['summon minecraft:item ~ ~ ~ {Item:{id:"minecraft:stone",count:1},PickupDelay:12s,Invulnerable:1b,Motion:[0.0d,0.08d,0.0d],Tags:["bm.cgdrop","bm.cgdropnew"]}',
                              f'item replace entity @e[type=minecraft:item,tag=bm.cgdropnew,limit=1] contents with {G.item_arg("creativity_gem")} 1',
                              f'data modify entity @e[type=minecraft:item,tag=bm.cgdropnew,limit=1] Owner set from entity {ME} UUID',
                              'scoreboard players operation @e[type=minecraft:item,tag=bm.cgdropnew] bm.pid = #me bm.pid',
                              'tag @e[type=minecraft:item,tag=bm.cgdropnew] remove bm.cgdropnew',
                              FXS.fx('cg_conjure', 1.4, 0.0) if 'cg_conjure' in FXS.names() else 'particle minecraft:flash{color:[1.0,1.0,1.0,1.0]} ~ ~ ~ 0 0 0 0 1',
                              'particle minecraft:totem_of_undying ~ ~ ~ 0.4 0.4 0.4 0.3 30', 'particle minecraft:end_rod ~ ~ ~ 0.2 0.2 0.2 0.08 20',
                              f'playsound minecraft:block.amethyst_block.resonate player {ME} ~ ~ ~ 1 1.4', f'playsound minecraft:entity.player.levelup player {ME} ~ ~ ~ 0.6 1.6',
                              f'kill {DISP}', 'kill @s'])

    # ---- the player, each tick while it's theirs to catch: caught (in their inventory, no drop or scene left), or late (given)
    fn('p231/cin/wait', ['scoreboard players add @s bm.cgwt 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'execute if score @s bm.cgwt matches {CIN_LATE}.. run return run function bm:p231/cin/late',
                         'execute as @e[type=minecraft:marker,tag=bm.cgcin] if score @s bm.pid = #me bm.pid run return 0',
                         'execute as @e[type=minecraft:item,tag=bm.cgdrop] if score @s bm.pid = #me bm.pid run return 0',
                         'execute if function bm:p231/cin/has run return run function bm:p231/cin/caught',
                         'function bm:p231/cin/late'])
    # ((3.0a: an "execute as ... run return 0" inside a function returns from it - the scene or the drop still out: wait))
    fn('p231/cin/has', has_gem + ['return 0'])
    fn('p231/cin/late', ['function bm:p231/cin/end_mine', X.give('creativity_gem'), 'function bm:p231/cin/caught'])
    fn('p231/cin/caught', ['tag @s remove bm.cgwait', 'scoreboard players reset @s bm.cgwt', 'advancement grant @s only bm:story/gem_friend',
                           'particle minecraft:end_rod ~ ~1.2 ~ 0.4 0.6 0.4 0.03 20', 'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.8',
                           tellraw('@s', [T('The Gem drops into your hands, warm and humming. ', CG_LINE, italic=True), T(':)', '#ffffff', bold=True),
                                          T('  (use it to call the Gem)', 'gray')])])
    # (a drop or a scene whose player isn't waiting any more - given it late, or gone: put out)
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:item,tag=bm.cgdrop] run function bm:p231/cin/stale',
                               'execute as @e[type=minecraft:item_display,tag=bm.cgcz] run function bm:p231/cin/stale']
    fn('p231/cin/stale', ['scoreboard players operation #me bm.pid = @s bm.pid',
                          'execute as @a[tag=bm.cgwait] if score @s bm.pid = #me bm.pid run return 0', 'kill @s'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:marker,tag=bm.cgcin]', 'kill @e[type=minecraft:item_display,tag=bm.cgcz]',
                                       'kill @e[type=minecraft:item,tag=bm.cgdrop]', 'tag @a remove bm.cgwait']
