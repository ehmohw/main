"""2.88: BENDER - THE GOODEST BOY. (bender_art.py, after the owner's photos; the machinery is rigpet's.)
A lean fawn shepherd-mix with enormous upright ears and a dark little mask. He lives round the villages, and he'll follow anyone
who brings him a bone.

FINDING HIM: spend time in a village (three or more villagers about) - sooner or later a dog trots out from between the houses,
  tail going. Right-click him holding a bone (or anything meaty) and he's yours: he drops his ball at your feet.
BENDER'S BALL  use: call him (again: call him over); sneak + use: his menu - sit / send home, his ways, the wardrobe, and:
DIG!           (his menu; every 5 minutes) on dirt, grass, sand, gravel, snow or mud he digs like mad - and comes up with something:
               Tokens, emeralds, a Heartstone, a Medallion, Blood Crystals, now and then a diamond, a Lucky Token, a Trophy,
               the odd Omni Token (and in hard mode, sometimes a Dread Token). Sometimes just a bone. He's very proud of the bone.
SNIFF OUT TREASURE  (his menu; every minute) nose down, ears up: he finds the scent of the nearest buried treasure or old ruin and
               points the way - a trail of glints along the ground and how far it is.
BITE           a bite every 0.9 s at a foe within 3 - 8.
TACKLE         every 5 s, a foe within 4-12: he bounds in and bowls it over (10, Slowness II).
GUARD BARK     two or more foes within 8, every 20 s: he plants himself in front of you and barks - they falter (Weakness, Slowness,
               lit up 4 s); Resistance for you.
GOOD BOY!      (charged, every minute) four seconds of pure loyalty: he darts from foe to foe within 10, eight bites, 9 each - and
               you get Regeneration II.
RAGE!          (2.93b; charged, every 40 s) a growl - then he launches himself at a monster, lands on it and goes for the head,
               two savage bites; backflips off it onto the next one near, up to five in a chain, every one bitten harder (7, 10, 13,
               16, 19 a bite) - and off the last a backflip and a clean landing on his feet.
HAPPY TO SEE YOU  beside you: Luck, and he finds you a little more.
Right-click him: sit / stand (and lie down). A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the
Ember Rat a golden one, the Tailor his coats (and his aura, Goodest Boy), the Recruiter his Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import bender_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134

BV_C, BV_LINE = '#e0a860', '#fff0d8'
W = 'bender'
DIG_CD, SNIFF_CD = 300, 60                     # (seconds, on you - a resummon doesn't reset them)


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'Bender', BV_C, BV_LINE, 'p195', 'bv', 'dq'
    A = A
    MENU = 2780
    PET_HP, PET_CD = 50, 120
    ITEM = 'bv_ball'
    pron, they = 'him', 'he'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': 'happy', 'surprised': 'alert', 'hurt': 'blink', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': None}
    ATTRS = dict(armor=6, attack_damage=8, movement_speed=0.32, follow_range=32, step_height=1.1)
    SCALE = 0.9
    HIT = (0.8, 1.3)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_0'), (4, 'walk_1'), (8, 'walk_2'), (12, 'walk_3')]),
             2: (12, [(0, 'run_0'), (3, 'run_1'), (6, 'run_2'), (9, 'run_3')]), 3: (None, [(0, 'jump')]),
             4: (200, [(0, 'sit_a'), (40, 'sit_b'), (80, 'lie'), (160, 'sit_a')]),
             6: (None, [(0, 'happy')]), 7: (None, [(0, 'bite_up'), (3, 'bite')]), 8: (None, [(0, 'bite_up'), (4, 'run_1'), (8, 'bite')]),
             9: (None, [(10 * i, ('sniff', 'sniff_b')[i % 2]) for i in range(5)] + [(50, 'wave_a')]),
             11: (None, [(0, 'bite_up'), (4, 'idle_b'), (8, 'bite_up')]),
             12: (None, [(0, 'happy')] + [(6 + 9 * i + k, p) for i in range(8) for k, p in ((0, 'run_1'), (3, 'bite_up'), (6, 'bite'))]),
             13: (None, [(4 * i, ('dig_a', 'dig_b')[i % 2]) for i in range(12)] + [(48, 'happy')]),
             14: (None, [(0, 'happy')]),
             # 2.93b RAGE: its poses are played by the rage's own clock (p195/rg/*); the far-off frames only have them written out
             15: (None, [(0, 'bite_up')] + [(9000 + i, p) for i, p in enumerate(['maul_a', 'maul_b', 'land'] + [f'flip_{k}' for k in range(5)])]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_0': 4, 'walk_1': 4, 'walk_2': 4, 'walk_3': 4, 'run_0': 3, 'run_1': 3, 'run_2': 3, 'run_3': 3, 'jump': 4,
           'sit_a': 20, 'sit_b': 20, 'lie': 24, 'bite_up': 3, 'bite': 2, 'dig_a': 3, 'dig_b': 3, 'sniff': 8, 'sniff_b': 8, 'happy': 8, 'wave_a': 8,
           'maul_a': 3, 'maul_b': 3, 'land': 4, **{f'flip_{k}': 2 for k in range(5)}}
    QUIPS = ['Woof!', '(his tail goes so hard his whole back end wags)', 'Arf! Arf!', '(he brings you a stick. It is mostly a log.)',
             '(he leans his whole weight against your legs)', '(his ears swivel at a sound you can\'t hear)', 'Wrrrf.',
             '(he looks up at you like you hung the moon)']
    HELLO = ('(he comes skidding round the corner, ears flat with joy)', '(a bark from far off - and here he is, tail first)', '(he trots off home, looking back twice)')
    SIT = ('(he springs up, ready for anything)', '(he sits. Very good sit. Look at that sit.)')
    FAINT = '(a small, sad whine)'
    NOT_YOURS = '(he sniffs your hand politely - then trots back to his person)'
    POWERS = [('Dig!', f'from his menu, every {DIG_CD // 60} minutes, on dirt, grass, sand, gravel, snow or mud: he digs something up - Tokens, emeralds, a Heartstone, a Medallion, Blood Crystals; now and then a diamond, a Lucky Token, a Trophy, even an Omni Token'),
              ('Sniff out Treasure', 'from his menu, every minute: he finds the scent of the nearest buried treasure or old ruin - and points the way'),
              ('Bite', 'a bite every 0.9 s (8) - he\'s quicker than he looks'),
              ('Tackle', 'every 5 s, a foe within 4-12: he bounds in and bowls it over (10, Slowness II)'),
              ('Guard Bark', 'two or more foes within 8, every 20 s: they falter - weakened, slowed, lit up; Resistance for you'),
              ('Good Boy!', 'charged, every minute: he darts from foe to foe within 10 - eight bites, 9 each - and you get Regeneration II'),
              ('Rage!', 'charged, every 40 s: he leaps on a monster and goes for the head - then backflips off onto the next, up to five in a chain, each bitten harder - and lands on his feet'),
              ('Happy to See You', 'beside him, you have Luck')]
    INTRO = [T('Bender', BV_C, bold=True), T(' - the goodest boy. ', 'gray'), T('Big ears, a little mask, and a nose for buried things.', 'white')]
    BUTTONS = ((6, 'Dig!', f'He digs something up (every {DIG_CD // 60} minutes; he needs dirt, sand, gravel or snow under his paws).', 'p195/dig_ask'),
               (7, 'Sniff out treasure', 'He points the way to the nearest buried treasure or old ruin (every minute).', 'p195/sniff_ask'))
    BURST = ['particle minecraft:heart ~ ~1 ~ 0.4 0.4 0.4 0 6', 'particle minecraft:poof ~ ~0.6 ~ 0.4 0.4 0.4 0.03 16',
             'particle minecraft:dust{color:[0.88,0.66,0.38],scale:1.4} ~ ~0.8 ~ 0.4 0.4 0.4 0 16']
    FADE_SOUND = 'playsound minecraft:entity.wolf.whine neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'
    SUMMON_EXTRA = ['playsound minecraft:entity.wolf.ambient neutral @a[distance=..24] ~ ~ ~ 1 1.1']
    ENC_POSES = [(0, 'sit_b'), (40, 'happy')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:heart ~ ~1.4 ~ 0.2 0.1 0.2 0 1'
    ADV = ('Who\'s a Good Boy?', 'Find Bender round a village - and give him a bone')
    ADMIN_HINT = 'He turns up round villages (three or more villagers near) - now and then.'
    MEET_HINT = 'Right-click him holding a bone or any meat.'


RP.register(C)
item('bv_ball', TOTEM, "Bender's Ball", BV_C,
     ['A well-chewed ball, a little damp.', 'He will bring it back. He always brings it back.', ('Use: call Bender (again: call him over).', 'blue'),
      ('Sneak + use: his menu - Dig! and Sniff out treasure.', 'blue'), ('He digs things up. He sniffs things out. He bites the bad guys.', 'blue'),
      ('If he faints: 2 minutes before he can return.', 'gray'), ('"Who\'s a good boy?"', 'dark_gray')],
     model='bm:bv_ball', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_bender', TOTEM, 'Bender Doll', BV_C, ['A doll of Bender - all ears.', ('Right-click a block: set it down.', 'blue'),
                                                ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_bender', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_bender'] = 'bm:p141/doll_bender/use'
P141.DOLLS.append(('doll_bender', 'Bender', BV_C, 'A doll of Bender - all ears.', 'minecraft:heart',
                   'minecraft:entity.wolf.ambient', 'minecraft:poof'))
P141.DOLL_FROM['doll_bender'] = ('bv_ball', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['bv_ball'] = (0.0, 1.5, -0.4, 0.4, -0.75, 0.75)
POSES = A.POSES

# ---- what he digs up (weights out of 100)
DIG = [('token', 26, 1, 3), ('emerald', 18, 2, 6), ('heartstone', 10, 1, 1), ('medallion', 9, 1, 1), ('bone', 9, 1, 2),
       ('blood_crystal', 7, 1, 2), ('gold_ingot', 7, 1, 3), ('diamond', 5, 1, 1), ('lucky_token', 4, 1, 1), ('trophy', 3, 1, 1),
       ('omni_token', 1, 1, 1), ('music_disc_precipice', 1, 1, 1)]
VANILLA = {'emerald', 'bone', 'gold_ingot', 'diamond', 'music_disc_precipice'}


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 3, 13, 14), fill=hexc('#c8e04a'), outline=hexc('#6a7a1a'))                  # a tennis ball, well loved
    d.arc((-2, 1, 8, 14), 300, 60, fill=hexc('#f4f4e8')); d.arc((8, 3, 18, 16), 120, 240, fill=hexc('#f4f4e8'))
    d.point((5, 6), fill=hexc('#eaf890')); d.point((6, 5), fill=hexc('#eaf890'))
    d.line((9, 12, 10, 13), fill=hexc('#8a9a3a')); d.point((4, 11), fill=hexc('#8a9a3a'))     # (tooth marks)
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


RAGE_CD, RAGE_CHAIN = 800, 5                    # (ticks; mobs at most)


def rage(G, X):
    """2.93b RAGE!: a charged attack. He launches at a monster (rg/leap), lands on its head and mauls it (rg/maul: two bites),
    backflips off onto the next monster near that he hasn't bitten (rg/flip), up to RAGE_CHAIN of them, each bitten harder -
    and off the last, a backflip back and a soft landing (rg/land). His host is carried through the air by hand (no gravity,
    teleported a step a tick, its rig following); the monster he's on is tagged bm.bvrtg, those he's bitten bm.bvrhit.
    Phases (bm.bvrp): 1 leap, 2 maul, 3 flip to the next, 4 flip off and land; bm.bvrt counts the ticks in one, bm.bvrn the
    monsters so far."""
    fn, S, foe, pfx, me = X.fn, X.S, X.foe, X.pfx, X.me
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.bvrg', 'bm.bvrp', 'bm.bvrt', 'bm.bvrn')]
    G.OBJECTIVES += ['bm.bvrg', 'bm.bvrp', 'bm.bvrt', 'bm.bvrn']
    T_ = '@e[tag=bm.bvrtg,distance=..16,limit=1]'
    pose = lambda p: f'function bm:{pfx}/pose/{p}'
    step = lambda d: [f'execute facing entity {T_} eyes positioned ^ ^ ^{d} if block ~ ~ ~ #bm:grap_pass if block ~ ~0.6 ~ #bm:grap_pass run tp @s ~ ~ ~ ~ 0']
    RH = '@e[type=minecraft:wolf,tag=bm.bvrme,limit=1]'                # (Bender, while his rage's tick runs)
    RHn = '@e[type=minecraft:wolf,tag=bm.bvrme,distance=..1.5,limit=1]'
    fn(f'{pfx}/rg/go', [f'scoreboard players set @s {S("a")} 15', f'scoreboard players set @s {S("x")} 600', f'scoreboard players set @s bm.bvrg {RAGE_CD}',
        'tag @e[tag=bm.bvrhit,distance=..32] remove bm.bvrhit', 'tag @e[tag=bm.bvrtg,distance=..32] remove bm.bvrtg',
        f'tag @e[{foe},distance=..9,sort=nearest,limit=1] add bm.bvrtg', 'tag @e[tag=bm.bvrtg,distance=..9] add bm.bvrhit',
        'scoreboard players set @s bm.bvrn 1', 'scoreboard players set @s bm.bvrp 1', 'scoreboard players set @s bm.bvrt 0',
        'data merge entity @s {NoGravity:1b,Motion:[0d,0d,0d]}',
        'playsound minecraft:entity.wolf.growl neutral @a[distance=..24] ~ ~ ~ 1.4 0.6', 'particle minecraft:angry_villager ~ ~1 ~ 0.3 0.2 0.3 0 4'] +
       X.face('surprised', 120) +
       ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + X.csay('GRRRRR-')])
    fn(f'{pfx}/rg/tick', ['tag @s add bm.bvrme', f'function bm:{pfx}/rg/step', 'tag @s remove bm.bvrme'])
    fn(f'{pfx}/rg/step', ['scoreboard players add @s bm.bvrt 1', 'data modify entity @s Motion set value [0d,0d,0d]',
                          f'execute if score @s bm.bvrp matches 1..3 unless entity {T_} run function bm:{pfx}/rg/next',
                          f'execute if score @s bm.bvrp matches 1 run function bm:{pfx}/rg/leap',
                          f'execute if score @s bm.bvrp matches 2 run function bm:{pfx}/rg/maul',
                          f'execute if score @s bm.bvrp matches 3 run function bm:{pfx}/rg/flip',
                          f'execute if score @s bm.bvrp matches 4 run function bm:{pfx}/rg/land',
                          f'execute if entity {T_} facing entity {T_} feet rotated ~ 0 run return run function bm:{pfx}/place',
                          f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])
    # the leap: up and at it, a step a tick (straight onto it if there's a wall between)
    fn(f'{pfx}/rg/leap', [f'execute if score @s bm.bvrt matches 1 run {pose("bite_up")}', f'execute if score @s bm.bvrt matches 4 run {pose("flip_0")}',
                          # (2.94b) the launch: one burst of dust where he pushes off, so the dash reads as speed
                          'execute if score @s bm.bvrt matches 3 run particle minecraft:dust_plume ~ ~0.1 ~ 0.35 0.05 0.35 0.06 18',
                          'execute if score @s bm.bvrt matches 3 run particle minecraft:poof ~ ~0.2 ~ 0.3 0.05 0.3 0.06 10',
                          'execute if score @s bm.bvrt matches 3..5 if block ~ ~1.4 ~ #bm:grap_pass run tp @s ~ ~0.35 ~'] +
       [f'execute if score @s bm.bvrt matches 3.. run {l}' for l in step(0.95)] +
       [f'execute if score @s bm.bvrt matches 3.. as {T_} at @s anchored eyes positioned ^ ^ ^ if entity {RHn} run return run function bm:{pfx}/rg/latch_as',
        f'execute if score @s bm.bvrt matches 14.. run function bm:{pfx}/rg/latch',
        'particle minecraft:cloud ~ ~0.3 ~ 0.1 0.1 0.1 0.01 1'])
    fn(f'{pfx}/rg/latch_as', [f'execute as {RH} at @s run function bm:{pfx}/rg/latch'])
    fn(f'{pfx}/rg/latch', ['scoreboard players set @s bm.bvrp 2', 'scoreboard players set @s bm.bvrt 0', pose('maul_a'),
                           'playsound minecraft:entity.wolf.growl neutral @a[distance=..20] ~ ~ ~ 1.2 0.8'])
    # on its head: held there, shaking it; two bites, each harder down the chain (7, 10, 13, 16, 19) - then off
    fn(f'{pfx}/rg/maul', [f'execute as {T_} at @s anchored eyes positioned ^ ^ ^ rotated as @s run tp {RH} ~ ~0.15 ~ ~ 0',
                          f'execute if score @s bm.bvrt matches 3 run {pose("maul_b")}', f'execute if score @s bm.bvrt matches 6 run {pose("maul_a")}',
                          f'execute if score @s bm.bvrt matches 9 run {pose("maul_b")}', f'execute if score @s bm.bvrt matches 12 run {pose("maul_a")}',
                          f'execute if score @s bm.bvrt matches 4 run function bm:{pfx}/rg/bite', f'execute if score @s bm.bvrt matches 10 run function bm:{pfx}/rg/bite',
                          'execute if score @s bm.bvrt matches 1..12 run particle minecraft:crit ~ ~0.2 ~ 0.25 0.2 0.25 0.1 2',
                          f'execute if score @s bm.bvrt matches 14.. run function bm:{pfx}/rg/next'])
    fn(f'{pfx}/rg/bite', [f'tag @s add {me}', 'scoreboard players operation #pd bm.rng = @s bm.bvrn', 'scoreboard players operation #pd bm.rng *= #3 bm.rng',
                          'scoreboard players add #pd bm.rng 4', f'execute as {T_} at @s run function bm:{pfx}/rg/bitten', f'tag @s remove {me}',
                          'playsound minecraft:entity.wolf.growl neutral @a[distance=..20] ~ ~ ~ 1 1.4', 'playsound minecraft:entity.player.attack.crit neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #3 bm.rng 3']
    fn(f'{pfx}/rg/bitten', [f'function bm:{pfx}/hurt', 'particle minecraft:damage_indicator ~ ~1.6 ~ 0.2 0.2 0.2 0.1 4',
                            'particle minecraft:block{block_state:"minecraft:redstone_block"} ~ ~1.6 ~ 0.2 0.2 0.2 0 6'])
    # the next one: the nearest monster near he hasn't bitten - a flip onto it; or (none left, or five down) the last flip, back
    fn(f'{pfx}/rg/next', ['scoreboard players set @s bm.bvrt 0', 'tag @e[tag=bm.bvrtg,distance=..32] remove bm.bvrtg',
                          f'execute if score @s bm.bvrn matches {RAGE_CHAIN}.. run return run function bm:{pfx}/rg/last',
                          f'execute positioned ~ ~-1 ~ run tag @e[{foe},tag=!bm.bvrhit,distance=..8,sort=nearest,limit=1] add bm.bvrtg',
                          f'execute unless entity {T_} run return run function bm:{pfx}/rg/last',
                          'tag @e[tag=bm.bvrtg,distance=..9] add bm.bvrhit', 'scoreboard players add @s bm.bvrn 1', 'scoreboard players set @s bm.bvrp 3',
                          'playsound minecraft:entity.wolf.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.5'])
    fn(f'{pfx}/rg/last', ['scoreboard players set @s bm.bvrp 4', 'scoreboard players set @s bm.bvrt 0', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.bvrfrom"]}',
                          'playsound minecraft:entity.wolf.ambient neutral @a[distance=..20] ~ ~ ~ 1 1.3'])
    # the flip onto the next: over backwards as he goes - up, then down onto it
    flips = [f'execute if score @s bm.bvrt matches {1 + 2 * k} run {pose(f"flip_{k}")}' for k in range(5)]
    fn(f'{pfx}/rg/flip', flips +
       ['execute if score @s bm.bvrt matches 1..4 if block ~ ~1.4 ~ #bm:grap_pass run tp @s ~ ~0.4 ~'] + step(0.8) +
       [f'execute if score @s bm.bvrt matches 8.. as {T_} at @s anchored eyes positioned ^ ^ ^ if entity {RHn} run return run function bm:{pfx}/rg/latch_as',
        f'execute if score @s bm.bvrt matches 16.. run function bm:{pfx}/rg/latch',
        'particle minecraft:dust{color:[0.88,0.66,0.38],scale:1.0} ~ ~0.6 ~ 0.2 0.2 0.2 0 2'])
    # the last flip: back off it, over and down - feet first onto the ground, a crouch to take it, then the goodest boy again
    fr = '@e[type=minecraft:marker,tag=bm.bvrfrom,distance=..12,sort=nearest,limit=1]'
    fn(f'{pfx}/rg/land', flips +
       [f'execute if score @s bm.bvrt matches 1..10 facing entity {fr} feet rotated ~180 0 positioned ^ ^ ^0.3 if block ~ ~ ~ #bm:grap_pass if block ~ ~0.6 ~ #bm:grap_pass run tp @s ~ ~ ~',
        'execute if score @s bm.bvrt matches 1..3 if block ~ ~1.4 ~ #bm:grap_pass run tp @s ~ ~0.4 ~',
        'execute if score @s bm.bvrt matches 5..29 if block ~ ~-0.3 ~ #bm:grap_pass run tp @s ~ ~-0.3 ~',
        f'execute if score @s bm.bvrt matches 5..29 unless block ~ ~-0.3 ~ #bm:grap_pass run function bm:{pfx}/rg/down',
        f'execute if score @s bm.bvrt matches 24..29 run function bm:{pfx}/rg/down',
        f'execute if score @s bm.bvrt matches 40.. run function bm:{pfx}/rg/done'])
    X.second.append(f'execute as @e[type=minecraft:marker,tag=bm.bvrfrom] at @s unless entity @e[type=minecraft:wolf,tag={X.pet},scores={{bm.bvrp=4}},distance=..16] run kill @s')
    fn(f'{pfx}/rg/down', ['scoreboard players set @s bm.bvrt 30', 'data merge entity @s {NoGravity:0b}', pose('land'),
                          'particle minecraft:poof ~ ~0.1 ~ 0.3 0.05 0.3 0.02 8', 'playsound minecraft:entity.wolf.step neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    fn(f'{pfx}/rg/done', [f'scoreboard players set @s {S("x")} 1', 'scoreboard players set @s bm.bvrp 0', 'data merge entity @s {NoGravity:0b}',
                          f'kill {fr}', 'tag @e[tag=bm.bvrtg,distance=..32] remove bm.bvrtg', 'tag @e[tag=bm.bvrhit,distance=..32] remove bm.bvrhit', pose('happy')] +
       X.face('happy', 40) + ['execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + X.csay('(he lands, shakes himself off - and looks back at you, tail going. Did you see that?)')])


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    say = lambda txt, col=BV_LINE: title('@s', 'actionbar', T(txt, col))
    csay = lambda txt: title('@s', 'actionbar', [T('Bender: ', BV_C, bold=True), T(txt, BV_LINE)])
    pet = 'bm.bvpet'

    # ---- the ground he'll dig, and the scents he follows
    wjson('bm/tags/block/bv_dig.json', {'values': ['#minecraft:dirt', '#minecraft:sand', 'minecraft:gravel', 'minecraft:snow_block', 'minecraft:snow',
                                                   'minecraft:clay', 'minecraft:soul_sand', 'minecraft:soul_soil', 'minecraft:farmland', 'minecraft:dirt_path',
                                                   'minecraft:suspicious_sand', 'minecraft:suspicious_gravel']})
    wjson('bm/tags/worldgen/structure/bv_scent.json', {'values': ['minecraft:buried_treasure', 'bm:ruins_overworld', 'minecraft:trail_ruins']})
    entries = []
    for n, w, lo, hi in DIG:
        e = ({'type': 'minecraft:item', 'name': f'minecraft:{n}'} if n in VANILLA else {'type': 'minecraft:loot_table', 'value': f'bm:items/{n}'})
        e['weight'] = w
        if hi > 1:
            e['functions'] = [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': lo, 'max': hi}}]
        entries.append(e)
    wjson('bm/loot_table/p195/dig.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': entries}]})

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        host = f'@e[type=minecraft:wolf,tag={X.me},limit=1]'
        lines = [f'execute if score @s bm.bvrg matches 1.. run scoreboard players remove @s bm.bvrg 1',
                 f'execute {idle} unless score @s bm.bvrg matches 1.. if entity @e[{foe},distance=..9] run function bm:{pfx}/rg/go',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..10] run function bm:{pfx}/good_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/bark_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3.5] if entity @e[{foe},distance=..12] run function bm:{pfx}/tackle_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/bite_go']
        fn(f'{pfx}/bite_go', go(7, 6, 'mc', 18, ['playsound minecraft:entity.wolf.growl neutral @a[distance=..16] ~ ~ ~ 0.5 1.3']))
        fn(f'{pfx}/tackle_go', go(8, 12, 'rc', 100, face('surprised', 12) + ['playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 1.4']))
        fn(f'{pfx}/bark_go', go(11, 12, 'bc', 400, face('surprised', 12)))
        fn(f'{pfx}/good_go', go(12, 80, 'gc', 1200, face('happy', 80) + ['playsound minecraft:entity.wolf.ambient neutral @a[distance=..32] ~ ~ ~ 1.4 0.7',
                                                                          'effect give @s minecraft:speed 4 0 true',
                                                                          'execute on owner if entity @s[distance=..24] run effect give @s minecraft:regeneration 5 1 true']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 2 run function bm:{pfx}/bite',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/bound',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 4 run function bm:{pfx}/tackle',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 9 run function bm:{pfx}/bark',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 4 run function bm:{pfx}/bark',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 2..74 run function bm:{pfx}/good_tick',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 2.. run function bm:{pfx}/digging',
                               f'execute if score @s {S("a")} matches 13 if score @s {S("x")} matches 8 run function bm:{pfx}/dug',
                               f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 20 run function bm:{pfx}/sniffed',
                               f'execute if score @s {S("a")} matches 15 if score @s {S("x")} matches 2.. run function bm:{pfx}/rg/tick'])
        rage(G, X)
        # BITE
        fn(f'{pfx}/bite', hit(8) + [f'execute as @e[{foe},distance=..3.2,sort=nearest,limit=1] at @s run function bm:{pfx}/bitten'] + end)
        fn(f'{pfx}/bitten', [f'function bm:{pfx}/hurt', 'particle minecraft:crit ~ ~1 ~ 0.3 0.3 0.3 0.2 6',
                             'playsound minecraft:entity.wolf.growl neutral @a[distance=..16] ~ ~ ~ 0.4 1.6'])
        # TACKLE: he bounds in (beside it), then bowls it over
        fn(f'{pfx}/bound', [f'tag @s add {X.me}',
                            f'execute as @e[{foe},distance=..12,sort=nearest,limit=1] at @s facing entity {host} feet rotated ~ 0 positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tp {host} ~ ~ ~ facing entity @s feet',
                            'particle minecraft:cloud ~ ~0.3 ~ 0.3 0.1 0.3 0.02 8', f'tag @s remove {X.me}'])
        fn(f'{pfx}/tackle', hit(10) + [f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] at @s run function bm:{pfx}/tackled'] + end)
        fn(f'{pfx}/tackled', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 3 1', 'particle minecraft:sweep_attack ~ ~1 ~ 0.2 0.2 0.2 0 1',
                              'playsound minecraft:entity.player.attack.knockback neutral @a[distance=..16] ~ ~ ~ 0.8 1.2'])
        # GUARD BARK
        fn(f'{pfx}/bark', ['playsound minecraft:entity.wolf.ambient neutral @a[distance=..24] ~ ~ ~ 1.2 0.9', 'particle minecraft:note ~ ~1.2 ~ 0.6 0.3 0.6 1 4',
                           f'execute as @e[{foe},distance=..8] run function bm:{pfx}/cowed',
                           'execute on owner if entity @s[distance=..16] run effect give @s minecraft:resistance 6 0 true'])
        fn(f'{pfx}/cowed', ['effect give @s minecraft:weakness 4 0', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:glowing 4 0'])
        # GOOD BOY!: every 9 ticks, beside a foe within 10 - a bite
        fn(f'{pfx}/good_tick', [f'scoreboard players operation #h bm.rng = @s {S("x")}', 'scoreboard players operation #h bm.rng %= #9 bm.rng',
                                f'execute if score #h bm.rng matches 0 if entity @e[{foe},distance=..10] run function bm:{pfx}/good_hit'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #9 bm.rng 9']
        fn(f'{pfx}/good_hit', hit(9) + [f'execute as @e[{foe},distance=..10,sort=random,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1.2 if block ~ ~ ~ #bm:grap_pass run tp {host} ~ ~ ~ facing entity @s feet',
                                        'execute at @s run particle minecraft:heart ~ ~1 ~ 0.2 0.2 0.2 0 1',
                                        f'execute at @s as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/bitten'] + end)
        # DIG!: earth flying, then whatever he finds
        fn(f'{pfx}/digging', ['execute if block ~ ~-1 ~ #minecraft:sand run return run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.2 ~ 0.3 0.1 0.3 0 4',
                              'execute if block ~ ~-1 ~ minecraft:gravel run return run particle minecraft:block{block_state:"minecraft:gravel"} ~ ~0.2 ~ 0.3 0.1 0.3 0 4',
                              'execute if block ~ ~-1 ~ minecraft:snow_block run return run particle minecraft:block{block_state:"minecraft:snow_block"} ~ ~0.2 ~ 0.3 0.1 0.3 0 4',
                              'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.2 ~ 0.3 0.1 0.3 0 4',
                              f'execute if score @s {S("x")} matches 40 run playsound minecraft:block.gravel.break neutral @a[distance=..16] ~ ~ ~ 1 0.9',
                              f'execute if score @s {S("x")} matches 24 run playsound minecraft:block.rooted_dirt.break neutral @a[distance=..16] ~ ~ ~ 1 1.1'])
        fn(f'{pfx}/dug', ['loot spawn ~ ~0.4 ~ loot bm:p195/dig',
                          'execute if score #hard bm.cfg matches 1 store result score #r bm.rng run random value 1..8',
                          'execute if score #hard bm.cfg matches 1 if score #r bm.rng matches 1 run loot spawn ~ ~0.4 ~ loot bm:items/dread_token',
                          'particle minecraft:happy_villager ~ ~0.6 ~ 0.4 0.3 0.4 0 12', 'particle minecraft:totem_of_undying ~ ~0.6 ~ 0.3 0.4 0.3 0.2 10',
                          'playsound minecraft:entity.item.pickup neutral @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                          'execute on owner if entity @s[distance=..24] run ' + X.csay('(he backs out of the hole, tail going, something in his mouth - and drops it at your feet)')])
        # SNIFF: the scent from here, a little east and a little south - the way it gets stronger is the way it lies
        fn(f'{pfx}/sniffed', ['scoreboard players set #s0 bm.rng 0', 'scoreboard players set #sx bm.rng 0', 'scoreboard players set #sz bm.rng 0',
                              'execute store result score #s0 bm.rng run locate structure #bm:bv_scent',
                              'execute if score #s0 bm.rng matches 0 run return run execute on owner run ' + X.csay('(he sniffs and sniffs... and sneezes. Nothing worth digging for near here.)'),
                              'execute if score #s0 bm.rng matches ..12 run return run function bm:p195/sniff_here',
                              'execute positioned ~32 ~ ~ store result score #sx bm.rng run locate structure #bm:bv_scent',
                              'execute positioned ~ ~ ~32 store result score #sz bm.rng run locate structure #bm:bv_scent',
                              'scoreboard players operation #sx bm.rng -= #s0 bm.rng', 'scoreboard players operation #sz bm.rng -= #s0 bm.rng',
                              'scoreboard players operation #sx bm.rng *= #-1 bm.rng', 'scoreboard players operation #sz bm.rng *= #-1 bm.rng',
                              'execute if score #sx bm.rng matches 0 if score #sz bm.rng matches 0 run scoreboard players set #sz bm.rng -1',
                              'execute store result storage bm:tmp bv.x int 1 run scoreboard players get #sx bm.rng',
                              'execute store result storage bm:tmp bv.z int 1 run scoreboard players get #sz bm.rng',
                              'function bm:p195/point with storage bm:tmp bv',
                              'execute on owner run function bm:p195/sniff_say'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #-1 bm.rng -1']
        # (his cooldowns are on you, counted in seconds)
        X.second.append('scoreboard players remove @a[scores={bm.bvdg=1..}] bm.bvdg 1')
        X.second.append('scoreboard players remove @a[scores={bm.bvsn=1..}] bm.bvsn 1')
        # HAPPY TO SEE YOU: Luck beside him
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s on owner if entity @s[distance=..16] run effect give @s minecraft:luck 3 0 true')
        return lines

    def encounter(G, X):
        # round a village (three or more villagers within 32), now and then: he trots out from between the houses
        X.second.append('execute as @a[tag=!bm.bvmet,gamemode=!spectator] at @s if dimension minecraft:overworld run function bm:p195/enc/roll')
        fn('p195/enc/roll', ['execute store result score #r bm.rng run random value 1..600', 'execute unless score #r bm.rng matches 1 run return 0',
                             'execute store result score #nv bm.rng if entity @e[type=minecraft:villager,distance=..32]',
                             'execute if score #nv bm.rng matches ..2 run return 0',
                             'execute if entity @e[type=minecraft:interaction,tag=bm.bvenc,distance=..64] run return 0',
                             'execute positioned ^ ^ ^5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass unless block ~ ~-1 ~ #bm:grap_pass run return run function bm:p195/enc/trot',
                             'execute positioned ^ ^ ^2 run function bm:p195/enc/trot'])
        fn('p195/enc/trot', ['function bm:p195/enc/spawn', 'particle minecraft:heart ~ ~1.2 ~ 0.3 0.2 0.3 0 3',
                             'playsound minecraft:entity.wolf.ambient neutral @a[distance=..24] ~ ~ ~ 1 1.1',
                             X.tellraw('@s', [T('A dog trots out from between the houses ', BV_LINE, italic=True),
                                              T('- enormous ears, a dark little mask, tail going like mad - sits down in front of you, and looks hopeful.', 'gray', italic=True)])])
        fn('p195/enc/talk', [f'execute if items entity @s container.* {X.holds("bv_ball")} run return run ' + X.csay('(he noses the ball in your pocket. Then he noses it again.)'),
                             'execute if items entity @s weapon.mainhand minecraft:bone run return run function bm:p195/enc/recruit',
                             'execute if items entity @s weapon.mainhand #minecraft:meat run return run function bm:p195/enc/recruit',
                             X.csay('(he sniffs your empty hand very hopefully. A bone, maybe? Anything meaty?)'),
                             'playsound minecraft:entity.wolf.whine neutral @s ~ ~ ~ 1 1.3'])
        fn('p195/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:heart ~ ~1.2 ~ 0.5 0.4 0.5 0 10',
                                f'execute as {X.here} at @s run playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.3',
                                X.tellraw('@s', [T('He takes it ever so gently - then bounces. ', BV_LINE, italic=True),
                                                 T('He runs off, comes back with a chewed-up ball, drops it at your feet, and sits. He\'s yours now. He has decided.', 'gray', italic=True)]),
                                'function bm:p195/enc/joined'])

    RP.build(C, G, abilities, encounter)
    # (2.94b: the dust at every run is gone - the owner found it constant; only the Rage's launch kicks up a burst, see rg/leap)
    sel2 = 'bm.bvsel2'
    S = lambda s: f'bm.dq{s}'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.bvdg dummy', 'scoreboard objectives add bm.bvsn dummy']
    G.OBJECTIVES += ['bm.bvdg', 'bm.bvsn']
    find = ['scoreboard operation #me bm.pid = @s bm.pid'.replace('scoreboard operation', 'scoreboard players operation'),
            f'tag @e[tag={sel2}] remove {sel2}',
            f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
            f'execute unless entity @e[tag={sel2}] run return run ' + say('He isn\'t out - call him first.'),
            'execute if dimension bm:gutter run return run ' + say('(he sniffs the gutter\'s stones, and sneezes. Nothing to find in here.)'),
            f'execute unless entity @e[type=minecraft:wolf,tag={sel2},distance=..24] run return run ' + say('He\'s too far off - call him over first.'),
            'dialog clear @s']
    # DIG!: on his diggable ground, every five minutes
    fn('p195/dig_ask', find + [
        'execute if score @s bm.bvdg matches 1.. run return run function bm:p195/dig_wait',
        f'execute as @e[tag={sel2}] at @s unless block ~ ~-1 ~ #bm:bv_dig unless block ~ ~ ~ minecraft:snow run return run ' + say('(he paws at it and looks at you. Dirt, sand, gravel or snow, please.)'),
        f'execute as @e[tag={sel2}] if score @s {S("x")} matches 1.. run return run ' + say('(he\'s busy!)'),
        f'scoreboard players set @s bm.bvdg {DIG_CD}',
        f'execute as @e[tag={sel2}] run data modify entity @s Sitting set value 0b',
        f'execute as @e[tag={sel2}] run scoreboard players set @s {S("a")} 13', f'execute as @e[tag={sel2}] run scoreboard players set @s {S("x")} 52',
        f'execute as @e[tag={sel2}] at @s run playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.4',
        say('(his ears go up. He sniffs the ground - and DIGS.)'), f'tag @e[tag={sel2}] remove {sel2}'])
    fn('p195/dig_wait', ['scoreboard players operation #m bm.rng = @s bm.bvdg', 'scoreboard players operation #m bm.rng /= #60 bm.rng',
                         'scoreboard players operation #sec bm.rng = @s bm.bvdg', 'scoreboard players operation #sec bm.rng %= #60 bm.rng',
                         title('@s', 'actionbar', [T('(he flops down, paws all muddy - ', BV_LINE), T('Dig again in ', 'gray'), {'score': {'name': '#m', 'objective': 'bm.rng'}},
                                                   T('m ', 'gray'), {'score': {'name': '#sec', 'objective': 'bm.rng'}}, T('s)', 'gray')]),
                         f'tag @e[tag={sel2}] remove {sel2}'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #60 bm.rng 60']
    # SNIFF OUT TREASURE: every minute
    fn('p195/sniff_ask', find + [
        'execute if score @s bm.bvsn matches 1.. run return run ' + say('(he\'s still sneezing from the last one - give him a moment)'),
        f'execute as @e[tag={sel2}] if score @s {S("x")} matches 1.. run return run ' + say('(he\'s busy!)'),
        f'scoreboard players set @s bm.bvsn {SNIFF_CD}',
        f'execute as @e[tag={sel2}] run data modify entity @s Sitting set value 0b',
        f'execute as @e[tag={sel2}] run scoreboard players set @s {S("a")} 9', f'execute as @e[tag={sel2}] run scoreboard players set @s {S("x")} 60',
        f'execute as @e[tag={sel2}] at @s run playsound minecraft:entity.fox.sniff neutral @a[distance=..16] ~ ~ ~ 1 1',
        say('(nose down, ears up - he\'s got something...)'), f'tag @e[tag={sel2}] remove {sel2}'])
    fn('p195/point', ['$tp @s ~ ~ ~ facing ~$(x) ~ ~$(z)', '$execute positioned ~ ~0.25 ~ facing ~$(x) ~0.25 ~$(z) run function bm:p195/trail',
                      'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.2'])
    fn('p195/trail', [f'particle minecraft:dust{{color:[1.0,0.85,0.35],scale:1.3}} ^ ^ ^{d} 0.05 0.05 0.05 0 3' for d in range(2, 17, 2)] +
       ['particle minecraft:wax_on ^ ^0.4 ^16 0.3 0.3 0.3 0 12'])
    fn('p195/sniff_here', ['particle minecraft:wax_on ~ ~0.5 ~ 1.5 0.3 1.5 0 30', 'playsound minecraft:entity.wolf.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.5',
                           'execute on owner run ' + csay('(he spins in a circle and paws the ground - it\'s RIGHT HERE. Dig!)')])
    # the way, in words: from the scent's pull east (+x) and south (+z)
    dirs = [('east', 1, 0), ('south-east', 1, 1), ('south', 0, 1), ('south-west', -1, 1), ('west', -1, 0), ('north-west', -1, -1), ('north', 0, -1), ('north-east', 1, -1)]
    # (each axis counts if it pulls at least half as hard as the other: both - a diagonal)
    say_dir = ['scoreboard players operation #ax bm.rng = #sx bm.rng', 'execute if score #ax bm.rng matches ..-1 run scoreboard players operation #ax bm.rng *= #-1 bm.rng',
               'scoreboard players operation #az bm.rng = #sz bm.rng', 'execute if score #az bm.rng matches ..-1 run scoreboard players operation #az bm.rng *= #-1 bm.rng',
               'scoreboard players set #dx bm.rng 0', 'scoreboard players set #dz bm.rng 0',
               'scoreboard players operation #a2 bm.rng = #ax bm.rng', 'scoreboard players operation #a2 bm.rng += #ax bm.rng',
               'execute if score #a2 bm.rng >= #az bm.rng if score #sx bm.rng matches 1.. run scoreboard players set #dx bm.rng 1',
               'execute if score #a2 bm.rng >= #az bm.rng if score #sx bm.rng matches ..-1 run scoreboard players set #dx bm.rng -1',
               'scoreboard players operation #a2 bm.rng = #az bm.rng', 'scoreboard players operation #a2 bm.rng += #az bm.rng',
               'execute if score #a2 bm.rng >= #ax bm.rng if score #sz bm.rng matches 1.. run scoreboard players set #dz bm.rng 1',
               'execute if score #a2 bm.rng >= #ax bm.rng if score #sz bm.rng matches ..-1 run scoreboard players set #dz bm.rng -1']
    for name, dx, dz in dirs:
        say_dir.append(f'execute if score #dx bm.rng matches {dx} if score #dz bm.rng matches {dz} run return run ' +
                       tellraw('@s', [T('Bender: ', BV_C, bold=True), T(f'(he points his nose {name} and whines - treasure that way, about ', BV_LINE),
                                      {'score': {'name': '#s0', 'objective': 'bm.rng'}}, T(' blocks. Follow the glints!)', BV_LINE)]))
    fn('p195/sniff_say', say_dir)

