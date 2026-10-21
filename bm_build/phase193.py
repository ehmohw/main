"""2.87: THE STALKER - THE HOLLOW HOOK. (stalker_art.py, after the owner's drawing; the machinery is rigpet's.)
The thing that hunts you on a Dread Night (phase181) - one of them, anyway, that stopped. It doesn't speak. It doesn't have
eyes. It follows you now, and whatever it touches it touches through armour, through Protection, through shields.

FINDING IT (hidden; HARD MODE ONLY): survive a Dread Night to its dawn wearing the Stalker's Grin (its own face). When the
  others come apart, one doesn't: it crouches a few blocks off, head cocked, looking at the face you're wearing. Right-click it
  holding Dread Essence - it takes it, and it follows.
THE HOLLOW HOOK  use: call it (again: call it over); sneak + use: its menu - sit / send home, its ways, the wardrobe.
REND           a claw every 0.8 s at a foe within 3.5 - 6, through armour, enchantments and shields; every third blow on the
               same foe is THE THIRD BLOW: a quarter of its whole health more (up to 20).
STEP FROM THE DARK   every 6 s, a foe within 5-20: it folds into nothing - and unfolds behind it, mid-strike (9, Slowness III).
THE STARE      two or more foes within 10, every 20 s: it throws its head back and they can't look away - frozen 3 s,
               weakened, 3 through everything.
THE HARROWING  (charged, every minute) for five seconds it is everywhere: it steps out of the dark beside one foe after
               another within 16, seven times - 10 each, through everything.
NIGHT-BORN     at night or in the dark it hits 3 harder; in full daylight 2 softer. You see in the dark while it's near.
KIN            the only follower that comes out on a Dread Night. With it beside you, the hunters never step out of the dark
               behind you for standing still.
Right-click it: sit / stand. A frame keeps it, a display case shows it as a figurine, Cecil sells its doll, the Ember Rat a
golden one, the Tailor its looks (and its aura, The Long Night), the Recruiter its Raid Contract."""
import json
import os
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import stalker_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase181 as P181

SK_C, SK_LINE = '#a8ac70', '#d8dcb0'
W = 'stalker'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'The Stalker', SK_C, SK_LINE, 'p193', 'sv', 'sq'
    A = A
    MENU = 2700
    PET_HP, PET_CD = 60, 120
    ITEM = 'st_hook'
    pron, they = 'it', 'it'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': None, 'surprised': 'wide', 'hurt': 'wide', 'sleepy': 'shut', 'blink': 'shut', 'squint': 'shut', 'serious': None}
    ATTRS = dict(armor=6, attack_damage=6, movement_speed=0.38, follow_range=32, step_height=1.2)
    SCALE = 1.0
    HIT = (0.9, 2.7)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
             2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'tilt')]), 7: (None, [(0, 'rend_up'), (4, 'rend')]), 8: (None, [(0, 'fold'), (8, 'unfold'), (12, 'rend')]),
             11: (None, [(0, 'scream')]),
             12: (None, [(0, 'scream')] + [(10 + 12 * i + k, p) for i in range(7) for k, p in ((0, 'fold'), (5, 'unfold'), (8, 'rend'))]),
             14: (None, [(0, 'tilt')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 4, 'sit_a': 20, 'sit_b': 20,
           'rend_up': 4, 'rend': 2, 'fold': 5, 'unfold': 2, 'scream': 6, 'tilt': 10}
    QUIPS = ['(it clicks its claws together, slowly)', '(a long, wet breath)', '(its head turns all the way round to look at you)',
             '(it stands very still. Too still.)', '(somewhere in its throat, something laughs)', '(it tilts its head at the dark)',
             '(it wipes its claws on the grass, one by one)', '(it is closer than it was a moment ago)']
    HELLO = ('(it is already behind you)', '(it steps out of your shadow)', '(it folds into the dark and is gone)')
    SIT = ('(it unfolds, joint by joint)', '(it sinks down, watching you)')
    FAINT = '...'
    NOT_YOURS = '(it turns its empty face on you, and you take your hand back)'
    POWERS = [('Rend', 'a claw every 0.8 s (6) - through armour, Protection and shields; every third blow on one foe takes a quarter of its health more (up to 20)'),
              ('Step from the Dark', 'every 6 s, a foe within 5-20: it folds into nothing and unfolds behind it, mid-strike (9, Slowness III)'),
              ('The Stare', 'two or more foes within 10, every 20 s: they can\'t look away - frozen 3 s, weakened, 3 through everything'),
              ('The Harrowing', 'charged, every minute: for five seconds it steps out of the dark beside foe after foe within 16 - seven times, 10 each'),
              ('Night-Born', 'at night or in the dark it hits 3 harder (in full daylight, 2 softer); near it, you see in the dark'),
              ('Kin', 'the only follower that comes out on a Dread Night - and with it beside you, the hunters never step out behind you for standing still')]
    INTRO = [T('The Stalker', SK_C, bold=True), T(' - one of the things from the Dread Night. It stopped hunting you. ', 'gray'),
             T('Nothing it touches is safe in its armour.', 'white')]
    BUTTONS = ()
    BURST = ['particle minecraft:sculk_soul ~ ~1.4 ~ 0.4 0.9 0.4 0.03 24', 'particle minecraft:large_smoke ~ ~1 ~ 0.4 1.0 0.4 0.02 30',
             'particle minecraft:dust{color:[0.45,0.0,0.05],scale:1.4} ~ ~1.4 ~ 0.4 0.9 0.4 0 20']
    FADE_SOUND = 'playsound minecraft:entity.warden.death neutral @a[distance=..20] ~ ~ ~ 0.5 1.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.warden.nearby_closer neutral @a[distance=..24] ~ ~ ~ 0.6 0.7']
    ENC_POSES = [(0, 'tilt'), (40, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:sculk_soul ~ ~2.2 ~ 0.3 0.4 0.3 0.01 2'
    ADV = ('Its Own Face', 'Survive a Dread Night wearing the Stalker\'s Grin - and give the one that stays behind what is left of the night')
    ADMIN_HINT = 'In hard mode: survive a Dread Night to dawn wearing the Stalker\'s Grin - one stays behind.'
    MEET_HINT = 'Right-click it holding Dread Essence.'


RP.register(C)
item('st_hook', TOTEM, 'The Hollow Hook', SK_C,
     ['A long hooked claw, olive-dark, cold to touch.', 'Something answers when you hold it in the dark.', ('Use: call the Stalker (again: call it over).', 'blue'),
      ('Sneak + use: its menu.', 'blue'), ('Its claws go through armour, Protection and shields.', 'blue'),
      ('If it falls: 2 minutes before it can return.', 'gray'), ('(it does not speak)', 'dark_gray')],
     model='bm:st_hook', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_stalker', TOTEM, 'Stalker Doll', SK_C, ['A doll of the Stalker. Its little claws are not soft.', ('Right-click a block: set it down.', 'blue'),
                                                  ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_stalker', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_stalker'] = 'bm:p141/doll_stalker/use'
P141.DOLLS.append(('doll_stalker', 'The Stalker', SK_C, 'A doll of the Stalker. Its little claws are not soft.', 'minecraft:sculk_soul',
                   'minecraft:entity.warden.ambient', 'minecraft:large_smoke'))
P141.DOLL_FROM['doll_stalker'] = ('st_hook', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['st_hook'] = (0.0, 2.6, -0.6, 0.6, -0.5, 0.5)
P181.KIN.add('bm.svpet')
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((4, 14, 6, 9, 8, 5, 9, 2), fill=hexc('#2a2c1e'), width=2)                              # the claw, long and hooked
    d.line((9, 2, 12, 3, 13, 5), fill=hexc('#2a2c1e'), width=2)
    d.line((5, 12, 7, 7, 8, 4), fill=hexc('#7a7c5a'))
    d.rectangle((2, 12, 6, 15), fill=hexc('#a8ac70'), outline=hexc('#5a5e3a'))                    # the knuckle it grew from
    d.point((12, 4), fill=hexc('#b0102a')); d.point((13, 6), fill=hexc('#b0102a'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    R.HATS['doll_stalker'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                   'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])
    R.LANG.update({'death.attack.bm.stalker_claw': '%1$s was torn open by a Stalker', 'death.attack.bm.stalker_claw.player': '%1$s was torn open by %2$s\'s Stalker'})


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    fn, wjson = G.fn, G.wjson

    # ---- its claws, by name: through armour, enchantments (Protection) and shields - not through Resistance
    wjson('bm/damage_type/stalker_claw.json', {'exhaustion': 0.1, 'message_id': 'bm.stalker_claw', 'scaling': 'never', 'effects': 'hurt'})
    for tg in ('bypasses_armor', 'bypasses_enchantments', 'bypasses_shield'):
        f_ = G.path('data', 'minecraft', 'tags', 'damage_type', f'{tg}.json')
        vals = json.load(open(f_))['values'] if os.path.exists(f_) else []
        wjson(f'minecraft/tags/damage_type/{tg}.json', {'replace': False, 'values': [v for v in vals if v != 'bm:stalker_claw'] + ['bm:stalker_claw']})

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        host = f'@e[type=minecraft:wolf,tag={X.me},limit=1]'
        # (k: rends on its current foe; the third is the Third Blow)
        lines = [f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..14] run function bm:{pfx}/harrow_go',
                 f'execute store result score #nf bm.rng if entity @e[{foe},distance=..10]',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/stare_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..5] if entity @e[{foe},distance=..20] run function bm:{pfx}/step_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3.5] run function bm:{pfx}/rend_go',
                 # (it stalks: anything hostile within 16, and it closes in - quietly)
                 f'execute unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}} if entity @e[{foe},distance=3..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] feet run function bm:{pfx}/chase']
        fn(f'{pfx}/chase', ['execute if block ^ ^ ^0.4 #bm:grap_pass if block ^ ^1 ^0.4 #bm:grap_pass if block ^ ^2 ^0.4 #bm:grap_pass run tp @s ^ ^ ^0.2 ~ ~'])
        fn(f'{pfx}/rend_go', go(7, 6, 'mc', 16, ['playsound minecraft:entity.warden.attack_impact neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']))
        fn(f'{pfx}/step_go', go(8, 16, 'rc', 120, face('surprised', 16) + ['particle minecraft:large_smoke ~ ~1.2 ~ 0.3 0.8 0.3 0.02 20',
                                                                            'playsound minecraft:entity.warden.sonic_charge neutral @a[distance=..16] ~ ~ ~ 0.4 1.8']))
        fn(f'{pfx}/stare_go', go(11, 14, 'bc', 400, face('surprised', 14) + ['playsound minecraft:entity.warden.roar neutral @a[distance=..24] ~ ~ ~ 0.7 1.6']))
        fn(f'{pfx}/harrow_go', go(12, 96, 'gc', 1200, face('surprised', 96) + ['playsound minecraft:entity.warden.emerge neutral @a[distance=..32] ~ ~ ~ 1 1.2',
                                                                                'playsound minecraft:ambient.cave neutral @a[distance=..32] ~ ~ ~ 1 0.5',
                                                                                'effect give @s minecraft:resistance 5 1 true']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 2 run function bm:{pfx}/rend',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 8 run function bm:{pfx}/step',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 4 run function bm:{pfx}/step_hit',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 8 run function bm:{pfx}/stare_hit',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 2..86 run function bm:{pfx}/harrow_tick'])
        # its claws: base + the dark (night, or a dark spot) - or the full sun
        def dmg(base):
            return hit(base) + ['execute if score #tod bm.bm matches 13000..23000 run scoreboard players add #pd bm.rng 3',
                                'execute unless score #tod bm.bm matches 13000..23000 if predicate bm:sees_sky run scoreboard players remove #pd bm.rng 2',
                                'execute unless score #tod bm.bm matches 13000..23000 unless predicate bm:sees_sky run scoreboard players add #pd bm.rng 3']
        fn(f'{pfx}/claw', [f'execute store result storage bm:tmp {pfx}.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/claw_d with storage bm:tmp {pfx}'])
        fn(f'{pfx}/claw_d', [f'$damage @s $(d) bm:stalker_claw by {host}'])
        # REND: the third on the same foe is the Third Blow - a quarter of its whole health more (up to 20)
        fn(f'{pfx}/rend', dmg(6) + [f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] run tag @s add bm.svtgt',
                                    f'execute unless entity @e[tag=bm.svtgt,tag=bm.svmk] run scoreboard players set @s {S("k")} 0',
                                    f'tag @e[tag=bm.svmk] remove bm.svmk', 'tag @e[tag=bm.svtgt] add bm.svmk',
                                    f'scoreboard players add @s {S("k")} 1',
                                    f'execute if score @s {S("k")} matches 3.. run function bm:{pfx}/third',
                                    f'execute as @e[tag=bm.svtgt] at @s run function bm:{pfx}/rent', 'tag @e[tag=bm.svtgt] remove bm.svtgt'] + end)
        fn(f'{pfx}/third', [f'scoreboard players set @s {S("k")} 0',
                            'execute store result score #mh bm.rng run attribute @e[tag=bm.svtgt,limit=1] minecraft:max_health get',
                            'scoreboard players operation #mh bm.rng /= #4 bm.rng', 'execute if score #mh bm.rng matches 21.. run scoreboard players set #mh bm.rng 20',
                            'scoreboard players operation #pd bm.rng += #mh bm.rng',
                            'execute at @e[tag=bm.svtgt,limit=1] run particle minecraft:sculk_soul ~ ~1 ~ 0.3 0.5 0.3 0.05 12',
                            'execute at @e[tag=bm.svtgt,limit=1] run playsound minecraft:entity.warden.attack_impact neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                            'execute on owner if entity @s[distance=..24,tag=!bm.hush] run ' + X.csay('(the third blow)')])
        fn(f'{pfx}/rent', [f'function bm:{pfx}/claw', 'particle minecraft:sweep_attack ~ ~1.2 ~ 0.2 0.2 0.2 0 1',
                           'particle minecraft:damage_indicator ~ ~1.2 ~ 0.3 0.3 0.3 0.1 4', 'playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.6 0.5'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4']
        # STEP FROM THE DARK: folded to nothing, then behind its foe
        fn(f'{pfx}/step', [f'tag @s add {X.me}', f'execute as @e[{foe},distance=..20,sort=nearest,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.6 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run tag @s add bm.svbh',
                           'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 16',
                           f'execute as @e[tag=bm.svbh,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.6 run tp {host} ~ ~ ~ facing entity @s feet',
                           f'execute unless entity @e[tag=bm.svbh] at @e[{foe},distance=..20,sort=nearest,limit=1] run tp @s ~ ~ ~',
                           'tag @e[tag=bm.svbh] remove bm.svbh', f'tag @s add {X.me}',
                           'execute at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 16',
                           'execute at @s run playsound minecraft:entity.enderman.teleport neutral @a[distance=..16] ~ ~ ~ 0.6 0.5', f'tag @s remove {X.me}'])
        fn(f'{pfx}/step_hit', dmg(9) + [f'execute at @s as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/stepped'] + end)
        fn(f'{pfx}/stepped', [f'function bm:{pfx}/rent', 'effect give @s minecraft:slowness 3 2'])
        # THE STARE: they can't look away
        fn(f'{pfx}/stare_hit', hit(3) + ['particle minecraft:sculk_soul ~ ~2 ~ 3 1 3 0.02 30', 'particle minecraft:dust{color:[0.45,0.0,0.05],scale:1.6} ~ ~1.4 ~ 4 0.6 4 0 50',
                                         f'execute as @e[{foe},distance=..10] at @s run function bm:{pfx}/stared'] + end)
        fn(f'{pfx}/stared', [f'function bm:{pfx}/claw', 'effect give @s minecraft:slowness 3 6', 'effect give @s minecraft:weakness 6 1',
                             'effect give @s minecraft:glowing 3 0', 'particle minecraft:sculk_soul ~ ~1.6 ~ 0.2 0.3 0.2 0.01 4'])
        # THE HARROWING: every 12 ticks, out of the dark beside a foe within 16 (a random one) - 10
        fn(f'{pfx}/harrow_tick', [f'scoreboard players operation #h bm.rng = @s {S("x")}', 'scoreboard players operation #h bm.rng %= #12 bm.rng',
                                  f'execute if score #h bm.rng matches 0 if entity @e[{foe},distance=..16] run function bm:{pfx}/harrow_hit'])
        G.FUNCS['load'][-1:-1] = ['scoreboard players set #12 bm.rng 12']
        fn(f'{pfx}/harrow_hit', dmg(10) + ['particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 12',
                                           f'execute as @e[{foe},distance=..16,sort=random,limit=1] at @s rotated as @s rotated ~ 0 positioned ^ ^ ^-1.4 run tp {host} ~ ~ ~ facing entity @s feet',
                                           'execute at @s run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.8 0.3 0.02 12',
                                           'execute at @s run playsound minecraft:entity.warden.attack_impact neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                                           f'execute at @s as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/rent'] + end)
        # -- every second: night-born (you see in the dark near it); it never stops healing in the dark
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        fn(f'{pfx}/sec', ['execute if score #tod bm.bm matches 13000..23000 run effect give @s minecraft:regeneration 3 0 true',
                          'execute if score #tod bm.bm matches 13000..23000 on owner if entity @s[distance=..24] run effect give @s minecraft:night_vision 15 0 true',
                          'execute unless score #tod bm.bm matches 13000..23000 unless predicate bm:sees_sky on owner if entity @s[distance=..24] run effect give @s minecraft:night_vision 15 0 true',
                          'execute store result score #r bm.rng run random value 1..12',
                          'execute if score #r bm.rng matches 1 run particle minecraft:sculk_soul ~ ~2.4 ~ 0.2 0.2 0.2 0.01 1'])
        return lines

    def encounter(G, X):
        # the dawn of a Dread Night: anyone who survived it wearing the Grin - one stays behind
        P181.DAWN.append(f'execute if items entity @s armor.head {X.holds("stalker_grin")} unless entity @s[tag=bm.svmet] at @s run function bm:p193/enc/kin')
        fn('p193/enc/kin', ['execute unless score #hard bm.cfg matches 1 run return 0',
                            'execute if entity @e[type=minecraft:interaction,tag=bm.svenc,distance=..48] run return 0',
                            'execute positioned ^ ^ ^5 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p193/enc/stay',
                            'execute positioned ^ ^ ^2 run function bm:p193/enc/stay'])
        fn('p193/enc/stay', ['function bm:p193/enc/spawn', 'particle minecraft:large_smoke ~ ~1.4 ~ 0.4 1.0 0.4 0.02 40',
                             'playsound minecraft:entity.warden.nearby_closest neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                             X.tellraw('@s', [T('One of them doesn\'t come apart. ', SK_LINE, italic=True),
                                              T('It crouches a few steps off in the grey light, head cocked - looking at the face you\'re wearing. Its own face.', 'gray', italic=True)])])
        fn('p193/enc/talk', [f'execute if items entity @s container.* {X.holds("st_hook")} run return run ' + X.csay('(it looks at the hook you carry, then away)'),
                             f'execute if items entity @s weapon.mainhand {X.holds("dread_essence")} run return run function bm:p193/enc/recruit',
                             X.csay('(it leans in close. It smells the night on you. It waits.)'),
                             'playsound minecraft:entity.warden.sniff neutral @s ~ ~ ~ 1 1.2'])
        fn('p193/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                                f'execute as {X.here} at @s run particle minecraft:sculk_soul ~ ~2 ~ 0.5 0.6 0.5 0.03 30',
                                f'execute as {X.here} at @s run playsound minecraft:entity.warden.tendril_clicks neutral @a[distance=..16] ~ ~ ~ 1 0.6',
                                X.tellraw('@s', [T('It takes the Essence from your hand ', SK_LINE, italic=True), T('- what is left of the night - and swallows it. ', 'gray', italic=True),
                                                 T('Then it unfolds to its full height beside you, and turns, and waits for you to walk.', 'gray', italic=True)]),
                                'function bm:p193/enc/joined'])

    RP.build(C, G, abilities, encounter)
    for f_ in ('p193/hurt', 'p193/dmg'):                  # (its claws have their own damage, through armour: p193/claw)
        G.FUNCS.pop(f_, None)
    # (Kin: with it beside you, the hunters never step out behind you for standing still)
    fn('p193/kin_near', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute as @e[type=minecraft:wolf,tag=bm.svpet,distance=..16] if score @s bm.pid = #me bm.pid run return 1', 'return 0'])
    P181.STILL.append('execute if function bm:p193/kin_near run scoreboard players set @s bm.dnst 0')
