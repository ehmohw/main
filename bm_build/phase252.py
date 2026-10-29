"""3.00: THE MIRELING - the 50th follower: a young Dread Mire (phase246) that has bonded to you. The same creature as the wild one,
small and follower-sized - creepy, but endearing (mireling_art.py draws it; tools/preview/mireling.py previews it). HARD MODE: the
Mires only rise in hard mode. Slay three wild ones (not a Mire Heart's, not the Sovereign's own) and the NEXT one you slay leaves a
Mireling's Seed in its puddle, for you alone (it never despawns, nobody else can pick it up) - once (bm.mlseed). The killer is the
Mire's attacker if a player, else the nearest player within 24 (bm.mlk counts them).

  LASH         a foe within 2.8, every 1.5 s: a tentacle cocked high and whipped down (6).
  PUDDLE SNARE two or more foes within 4, every 12 s: it sinks, and its puddle spreads under them - 4 each, held fast.
  THE GRAB     (charged, every minute) a tentacle seizes the nearest foe within 8, drags it in to the open maw - and stabs (12).
  SHADOW VEIL  you, hurt in a fight, every 10 s: it wraps you in its shadow - Resistance and Regeneration; the monsters at your
               side slowed (they lose sight of you, a little).
  GLOWPOOL     out of a fight beside you, every minute: it lets you see as it sees - Night Vision and Water Breathing.
  LIGHT-SHY    in bright light it shivers and peeks about (only a look - light never hurts it).
  SHADOW KIN   while it's out near you (16), a Dread Night's Stalkers pass you over a third of the time - a little Shadow Musk.
It moves as a little puddle (sunk, walking and running) and rears up when it stops. Everything else is every follower's: sitting,
a wardrobe (the veins' colour, per look), a rare aura, a shiny (bone-white, gold veins), the Partner Wheel, a frame, a display
case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
import mireling_art as MA
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import phase95 as FX

COL, LINE = '#e0384a', '#ffb4a8'
SLAIN = 3                                       # (wild Mires a player slays before the next one leaves its seed)
SHY_CHANCE = 4                                  # (1 in this many seconds in bright light: a shiver)

item('mire_seed', TOTEM, "A Mireling's Seed", COL,
     ['A small black seed, wet and warm.', 'Something in it blinks at you.', ('Hard mode: left by a Dread Mire, for the one who slew it.', '#9a7aff'),
      ('Use: call the Mireling (again: call it over).', 'blue'), ('Sneak + use: its menu.', 'blue'), ('A lash, a snare, and THE GRAB.', 'blue'),
      ('If it faints: 2 minutes before it can return.', 'gray')],
     model='bm:mire_seed', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)


class Mireling(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'mireling', 'The Mireling', COL, LINE, 'p252', 'ml', 'mj'
    A = RF2.art(MA)
    MENU, PET_HP, PET_CD, ITEM = 5200, 36, 120, 'mire_seed'
    pron, they = 'it', 'it'
    FACE = dict(MA.FACE_MAP)
    ATTRS = dict(armor=6, attack_damage=5, movement_speed=0.37, follow_range=32, step_height=1.1)
    SCALE, HIT = 1.0, (1.0, 1.7)
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (80, 'idle_b'), (160, 'idle_c'), (210, 'idle_a')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy'), (6, 'happy_b'), (12, 'happy'), (18, 'happy_b'), (24, 'happy')]),
                       {7: (None, [(0, 'lash_up'), (3, 'lash')]),
                        11: (None, [(0, 'run_0'), (4, 'run_2'), (10, 'idle_a')]),
                        12: (None, [(0, 'grab_up'), (5, 'grab'), (8, 'grab_pull'), (24, 'idle_a')]),
                        13: (None, [(0, 'happy_b'), (12, 'idle_a')]),
                        14: (None, [(0, 'sit_b'), (20, 'happy'), (28, 'happy_b'), (36, 'idle_a')])})
    DUR = dict(P235._DUR, **MA.DUR)
    QUIPS = ['(it rises out of its puddle, looks at you, and sinks back down, satisfied you are still there)',
             '(its maw opens a crack. The big orange eye peeks out, blinks once, and hides again)',
             '(a tentacle reaches over and pats your boot. Wetly.)', '(it blows a slow black bubble. It pops. It looks very pleased.)',
             '(it chases its own reflection round the puddle)', '(a soft, gurgling purr - the closest thing it has to a word)']
    HELLO = ('(the Mireling slides back to your side, a puddle on the move)', '(a dark puddle spreads at your feet - and the Mireling rises out of it, swaying)',
             '(it sinks into its puddle, and the puddle sinks into the ground)')
    SIT = ('(it rears up out of its puddle, ready to go)', '(it settles into its puddle, only the eye poking up, blinking)')
    FAINT = '(it melts flat into its puddle, the eye very small)'
    NOT_YOURS = '(the Mireling sinks, its maw clamped shut - it is somebody else\'s)'
    POWERS = [('Lash', 'a foe within 2.8, every 1.5 s: a tentacle cocked high and whipped down - 6'),
              ('Puddle Snare', 'two or more foes within 4, every 12 s: it sinks, its puddle spreads under them - 4 each, held fast'),
              ('The Grab', 'charged, every minute: a tentacle seizes a foe within 8, drags it in to the open maw - and stabs, 12'),
              ('Shadow Veil', 'you, hurt in a fight, every 10 s: Resistance and Regeneration, and the monsters at your side slowed'),
              ('Glowpool', 'out of a fight beside you, every minute: Night Vision and Water Breathing - it lets you see as it sees'),
              ('Light-Shy', 'in bright light it shivers and peeks about (light never hurts it)'),
              ('Shadow Kin', 'while it is out near you, a Dread Night\'s Stalkers pass you over now and then')]
    INTRO = [T('The Mireling', COL, bold=True), T(' - a young Dread Mire, bonded to you. ', 'gray'),
             T('It is creepy. It is also, somehow, adorable.', LINE, italic=True)]
    BURST = ['particle minecraft:squid_ink ~ ~0.4 ~ 0.6 0.2 0.6 0.04 24', 'particle minecraft:dust{color:[0.88,0.2,0.26],scale:1.2} ~ ~0.6 ~ 0.6 0.4 0.6 0 16',
             'particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~1 ~ 0.4 0.6 0.4 0 10']
    FADE_SOUND = 'playsound minecraft:block.bubble_column.whirlpool_ambient neutral @a[distance=..20] ~ ~ ~ 0.8 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.bubble_column.upwards_inside neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                    'playsound minecraft:entity.slime.squish neutral @a[distance=..24] ~ ~ ~ 0.8 0.6']
    ENC_POSES = [(0, 'sit_b'), (40, 'idle_c')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:squid_ink ~ ~0.3 ~ 0.4 0.1 0.4 0.01 4'
    ADV = ('Something in the Puddle', 'Slay four wild Dread Mires - and take home what the last one left behind')
    ADMIN_HINT = 'Hard mode: slay three wild Dread Mires; the next one you slay leaves its seed for you, once.'
    MEET_HINT = 'Hard mode: slay the Dread Mires that rise in the dark.'


RP.register(Mireling)
RF2.setup(Mireling, 'head')

_DOLL = 'A doll of the Mireling - a head far too big for it, one huge orange eye, and two little tentacles that wave.'
item('doll_mireling', TOTEM, 'Mireling Doll', COL, [_DOLL, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                                   ('Sneak + punch: pick it up.', 'gray')], model='bm:doll_mireling', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_mireling'] = 'bm:p141/doll_mireling/use'
P141.DOLLS.append(('doll_mireling', Mireling.NAME, COL, _DOLL, 'minecraft:squid_ink', 'minecraft:entity.slime.squish', 'minecraft:poof'))
P141.DOLL_FROM['doll_mireling'] = ('mire_seed', dict(MA.DOLL))          # (the default chibi warp; its head is the head and the maw's petals)
P134.FIT['mire_seed'] = MA.FIT                                          # (phase134: idle_a at RIG_SCALE - MA.fit() re-measures)

# ---- its pairs with Bender and Mr. Capshun (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} {15 if e in ("night_vision", "water_breathing") else 3} {a} true' for e, a in es]
P188.VNAME.update({'mireling': 'the Mireling'})
P188.PAIRS.update({
    'ml_bender': ('mireling', 'bender', 'Puddle Splashing', '#e0a860', 'The Mireling and Bender - the goodest boy has found the best puddle in the world',
                  _eff(('speed', 0), ('jump_boost', 0)),
                  [('bender', '(pounces into its puddle, tail going, and comes out black to the ears)'), ('mireling', '(it rises, delighted, and splashes him back)')],
                  [('mireling', '(a tentacle rolls him a stick across the puddle)', 'bender', '(brings it back. Wet. Proud.)')]),
    'ml_capshun': ('mireling', 'capshun', 'Ink and Goo', '#f0f0f0', 'The Mireling and Mr. Capshun - the narrator, and something that might be ink',
                   _eff(('night_vision', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "From the dark puddle, a single eye. It was, he decided, a friendly eye."]'), ('mireling', '(its eye goes very wide, very happy)')],
                   [('capshun', '[Mr. Capshun narrates: "He dipped his pen in its puddle. The ink wrote back."]', 'mireling', '(it gurgles, very pleased with itself)')]),
})
P188.ICON.update({'ml_bender': 'bm:mire_seed', 'ml_capshun': 'bm:mire_seed'})


def extend_offers(O, offer):
    pass


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(Mireling, R, MA.icon_raw())                                   # (the raw icon - gen_rp's ICONS loop finishes it)
    RF2.faces(Mireling, 'head', R)


def textures():
    return MA.textures()                        # (its own ml_* textures - the Mire's patterns under its own names)


def generate_early(G):
    RP.contract(Mireling, G)


def _abilities(G, X):
    fn, pfx, foe, me = G.fn, X.pfx, X.foe, X.me
    snd = lambda s, v=0.6, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..16] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=8, at=5, cd=30, reach=2.8, go=[snd('entity.slime.attack', 0.5, 0.8)]),
             crowd=dict(st=11, x=14, at=8, cd=240, r=4, n=2, face='serious', go=[snd('block.bubble_column.whirlpool_ambient', 0.8, 0.8)]),
             charged=dict(st=12, x=30, at=[26, 8], cd=1200, r=8, face='serious', during=(9, 25), go=[snd('entity.warden.attack_impact', 0.6, 1.6)]),
             support=dict(st=13, x=16, at=8, cd=200, face='happy'),
             kind=dict(st=14, x=40, at=20, cd=1200, face='happy'))
    lines = P235.kit(G, X, K)
    # LASH
    P235.melee(G, X, 6, 2.8, ['particle minecraft:squid_ink ~ ~0.8 ~ 0.2 0.2 0.2 0.05 8', 'particle minecraft:dust{color:[0.88,0.2,0.26],scale:1.0} ~ ~0.9 ~ 0.3 0.3 0.3 0 6'],
               'minecraft:entity.warden.attack_impact')
    # PUDDLE SNARE
    fn(f'{pfx}/crowd', X.hit(4) + ['particle minecraft:squid_ink ~ ~0.1 ~ 2 0.05 2 0.02 60', 'particle minecraft:dust{color:[0.5,0.02,0.06],scale:1.3} ~ ~0.1 ~ 2 0.02 2 0 30',
                                   f'execute as @e[{foe},distance=..4] at @s run function bm:{pfx}/snared'] + X.end)
    fn(f'{pfx}/snared', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 3',
                         'particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~0.4 ~ 0.3 0.2 0.3 0 8'])
    # THE GRAB: seized (4 ticks in), dragged in while it hauls (9..25 ticks left), stabbed at the maw (8 left)
    fn(f'{pfx}/charged', ['tag @e[tag=bm.mlgr,distance=..24] remove bm.mlgr',
                          f'execute as @e[{foe},distance=..8,sort=nearest,limit=1] at @s run function bm:{pfx}/seized'])
    fn(f'{pfx}/seized', ['tag @s add bm.mlgr', 'effect give @s minecraft:slowness 2 4', 'particle minecraft:squid_ink ~ ~1 ~ 0.3 0.5 0.3 0.05 16',
                         'playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn(f'{pfx}/charged_tick', [f'tag @s add {me}',
                               f'execute as @e[tag=bm.mlgr,distance=1.8..12] at @s facing entity @e[type=minecraft:wolf,tag={me},limit=1] feet '
                               'if block ^ ^ ^0.45 #bm:grap_pass if block ^ ^1 ^0.45 #bm:grap_pass run tp @s ^ ^ ^0.45',
                               'execute as @e[tag=bm.mlgr,distance=..12] at @s run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~1 ~ 0.2 0.3 0.2 0 2',
                               f'tag @s remove {me}'])
    fn(f'{pfx}/charged2', X.hit(12) + [f'execute as @e[tag=bm.mlgr,distance=..12] at @s run function bm:{pfx}/stabbed'] + X.end)
    fn(f'{pfx}/stabbed', [f'function bm:{pfx}/hurt', 'tag @s remove bm.mlgr', 'particle minecraft:dust{color:[0.6,0.02,0.08],scale:1.6} ~ ~1 ~ 0.3 0.4 0.3 0 20',
                          'particle minecraft:crit ~ ~1 ~ 0.3 0.4 0.3 0.2 12'])
    # SHADOW VEIL
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p252/veil_you'])
    fn('p252/veil_you', ['effect give @s minecraft:resistance 6 0 true', 'effect give @s minecraft:regeneration 5 0 true',
                         f'effect give @e[{foe},distance=..4] minecraft:slowness 3 1', 'particle minecraft:squid_ink ~ ~1 ~ 0.5 0.8 0.5 0.02 24',
                         'particle minecraft:dust{color:[0.88,0.2,0.26],scale:1.0} ~ ~1 ~ 0.6 0.8 0.6 0 10', 'playsound minecraft:entity.warden.sniff player @s ~ ~ ~ 0.6 1.6'])
    # GLOWPOOL
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p252/glow_you'])
    fn('p252/glow_you', ['effect give @s minecraft:night_vision 60 0 true', 'effect give @s minecraft:water_breathing 60 0 true',
                         'particle minecraft:bubble_pop ~ ~1 ~ 0.4 0.4 0.4 0.02 10', 'playsound minecraft:block.bubble_column.bubble_pop player @s ~ ~ ~ 0.8 1.2',
                         'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('The Mireling: ', COL, bold=True),
                                                                                                 T('(it blows you a bubble. Inside it, the dark looks bright)', LINE, italic=True)])])
    return lines


def generate(G):
    fn = G.fn
    RP.build(Mireling, G, _abilities, lambda G_, X: G_.fn(f'{Mireling.pfx}/enc/talk', ['function bm:p252/enc/joined']))   # (no encounter: its Seed is a Mire's)
    # LIGHT-SHY: in bright light, now and then, a shiver and a wide eye (a look only)
    G.wjson('bm/predicate/p252/bright.json', {'condition': 'minecraft:location_check', 'predicate': {'light': {'light': {'min': 13}}}})
    G.wjson('bm/predicate/p252/third.json', {'condition': 'minecraft:random_chance', 'chance': 0.34})
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.mlpet,tag=!bm.ffpet] at @s unless score @s bm.mjx matches 1.. if predicate bm:p252/bright run function bm:p252/shy']
    fn('p252/shy', ['execute store result score #r bm.rng run random value 1..%d' % SHY_CHANCE, 'execute unless score #r bm.rng matches 1 run return 0'] +
       FX.face_cmd('mireling', 'surprised', 20) +
       ['particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ~ ~0.8 ~ 0.3 0.3 0.3 0 6', 'playsound minecraft:entity.slime.squish_small neutral @a[distance=..12] ~ ~ ~ 0.5 1.6',
        'execute store result score #r bm.rng run random value 1..20',
        'execute if score #r bm.rng matches 1 on owner if entity @s[distance=..12,tag=!bm.hush] run ' +
        G.title('@s', 'actionbar', [T('The Mireling: ', COL, bold=True), T('(it shivers in the light, and edges into your shadow)', LINE, italic=True)])])


def late(G):
    """(after phase181 and phase246) the Mire's death credits its slayer - and the fourth leaves the seed; the Stalkers' nod"""
    fn, tellraw = G.fn, G.tellraw
    ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'
    objs = ['bm.mlk', 'bm.mlo']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    G.FUNCS['p246/die0'].insert(0, 'execute unless entity @s[tag=bm.mtame] unless entity @s[tag=bm.svm] run function bm:p252/mire/slain')
    G.FUNCS['p246/s/die'].insert(0, 'execute if entity @s[tag=bm.mlsd] if score @s bm.mt matches 50 run function bm:p252/mire/seed')
    fn('p252/mire/slain', ['tag @a remove bm.mlkr', 'execute on attacker if entity @s[type=minecraft:player] run tag @s add bm.mlkr',
                           'execute unless entity @a[tag=bm.mlkr] run tag @p[distance=..24,gamemode=!spectator,gamemode=!creative] add bm.mlkr',
                           'execute as @a[tag=bm.mlkr,limit=1] run function bm:p252/mire/credit', 'tag @a remove bm.mlkr'])
    fn('p252/mire/credit', ['execute if entity @s[tag=bm.mlseed] run return 0', 'execute unless score @s bm.pid matches 1.. run function bm:p21/pid',
                            'scoreboard players add @s bm.mlk 1',
                            f'execute if score @s bm.mlk matches {SLAIN} run ' + tellraw('@s', [T('As the Mire melts away, something small in its puddle watches you go.', COL, italic=True)]),
                            f'execute if score @s bm.mlk matches ..{SLAIN} run return 0',
                            'tag @s add bm.mlseed', f'scoreboard players operation {ME} bm.mlo = @s bm.pid', f'tag {ME} add bm.mlsd'])
    fn('p252/mire/seed', ['scoreboard players operation #mlo bm.rng = @s bm.mlo', 'tag @a remove bm.mlkr',
                          'execute as @a if score @s bm.pid = #mlo bm.rng run tag @s add bm.mlkr',
                          'loot spawn ~ ~0.6 ~ loot bm:items/mire_seed',
                          'execute as @e[type=minecraft:item,distance=..2] if items entity @s contents *[minecraft:custom_data~{bm:"mire_seed"}] run function bm:p252/mire/own',
                          'particle minecraft:dust{color:[1.0,0.48,0.1],scale:1.4} ~ ~0.8 ~ 0.2 0.2 0.2 0 20', 'particle minecraft:bubble_pop ~ ~0.5 ~ 0.4 0.2 0.4 0.02 20',
                          'playsound minecraft:block.bubble_column.bubble_pop neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                          'execute as @a[tag=bm.mlkr] run ' + tellraw('@s', [T('In the last of the puddle: ', 'gray'), T("a Mireling's Seed", COL, bold=True),
                                                                             T(' - and it is looking at you. ', 'gray'), T('(Only you can pick it up.)', 'dark_gray')]),
                          'advancement grant @a[tag=bm.mlkr] only bm:story/mireling_friend', 'tag @a remove bm.mlkr'])
    fn('p252/mire/own', ['data merge entity @s {Age:-32768s,Invulnerable:1b,PickupDelay:10s}', 'data modify entity @s Owner set from entity @a[tag=bm.mlkr,limit=1] UUID'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/mireling_reset', 'yellow'), T('  forget your slain Mires and the Seed (bm.mlk, bm.mlseed)', 'gray')]))
    fn('admin/mireling_reset', ['scoreboard players reset @s bm.mlk', 'tag @s remove bm.mlseed',
                                G.title('@s', 'actionbar', T('Your slain Mires are forgotten - three more, and the next leaves its seed.', COL))])
    # SHADOW KIN: a Stalker of a Dread Night passes you over, a third of the time, while your Mireling's out near you
    G.FUNCS['p181/hunted'].insert(0, 'execute if function bm:p252/near_q if predicate bm:p252/third run return 0')
    fn('p252/near_q', ['scoreboard players operation #mlq bm.rng = @s bm.pid',
                       'execute as @e[type=minecraft:wolf,tag=bm.mlpet,tag=!bm.ffpet,distance=..16] if score @s bm.pid = #mlq bm.rng run return 1', 'return 0'])
