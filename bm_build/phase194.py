"""2.87: THE ARACHNO-LANTERN - THE KINDLED GOURD. A hidden mount (lantern_art.py, the Scorching Arachno-Lantern's own kind;
the machinery is rigpet's).

FINDING IT (hidden; HARD MODE ONLY): when the Scorching Arachno-Lantern falls in hard mode, everyone near who hasn't one finds a
  KINDLED GOURD in the embers - a little carved gourd still burning inside. Use it: it cracks, and something unfolds out of it
  on long black legs and sits there smouldering. Right-click it with the gourd in your hand and it's yours.
THE KINDLED GOURD   use: call it (again: call it over); sneak + use: its menu - sit / send home, RIDE, its ways, the
  wardrobe. On the Partner Wheel like any follower.
RIDING        walk to stride (fast), jump to LEAP (far), walk into a wall and it climbs it. Fire can't touch you up there and you
              take no fall damage. Use the gourd while riding: THE GLARE - a beam of fire from its carved eyes, 18 blocks ahead
              (7 to everything in it, set alight; every 3 s). Sneak to get off.
ON FOOT (it fights beside you):
  EMBER BITE    a foe within 3: 5, and it burns.
  TONGUE LASH   every 5 s, a foe 5-12 away: the tongue shoots out and drags it in (4).
  STOMP         every 8 s, foes within 4: the front pair rears and comes down - a burning shockwave that throws them (8).
  EMBER RAIN    (charged, every 45 s) it throws its head back and burning embers fall on every foe within 12 - three waves,
                6 each, and they burn.
  HALLOWFIRE    fire can't hurt you while it's near; on a Blood Moon it hits 3 harder.
Right-click it: sit / stand. A frame keeps it, a display case shows it as a figurine, Cecil sells its doll, the Ember Rat a
golden one, the Tailor its looks (and its aura, Hallowfire), the Recruiter its Raid Contract."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import lantern_art as A
import rigpet as RP
import phase141 as P141
import phase134 as P134
import phase28 as P28

LN_C, LN_LINE = '#ff8a2a', '#ffd8a0'
W = 'lantern'


class C(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = W, 'The Arachno-Lantern', LN_C, LN_LINE, 'p194', 'ln', 'lj'
    A = A
    MENU = 2740
    PET_HP, PET_CD = 80, 120
    ITEM = 'ln_gourd'
    pron, they = 'it', 'it'
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FACE = {'happy': None, 'surprised': 'glare', 'hurt': 'glare', 'sleepy': 'shut', 'blink': None, 'squint': 'glare', 'serious': None}
    ATTRS = dict(armor=10, attack_damage=5, movement_speed=0.36, follow_range=32, step_height=1.6)
    SCALE = 2.4
    HIT = (1.6, 2.3)
    CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(4 * k, f'walk_{k}') for k in range(4)]),
             2: (12, [(3 * k, f'run_{k}') for k in range(4)]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
             6: (None, [(0, 'flare')]), 7: (None, [(0, 'lash_a'), (3, 'idle_a')]), 8: (None, [(0, 'lash_a'), (5, 'lash_b'), (10, 'idle_a')]),
             11: (None, [(0, 'rear'), (10, 'stomp'), (16, 'idle_a')]),
             12: (None, [(0, 'flare'), (20, 'idle_b'), (26, 'flare'), (46, 'idle_b'), (52, 'flare')]),
             14: (None, [(0, 'flare')]),
             10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
    DUR = {'idle_a': 30, 'idle_b': 30, **{f'walk_{k}': 4 for k in range(4)}, **{f'run_{k}': 3 for k in range(4)}, 'jump': 4, 'sit_a': 20, 'sit_b': 20,
           'lash_a': 3, 'lash_b': 2, 'rear': 10, 'stomp': 3, 'flare': 10}
    QUIPS = ['(it clacks its legs together, pleased)', '(a puff of embers from its grin)', '(its fires gutter, then roar up again)',
             '(its tongue lolls out and steams)', '(it settles lower, purring like a hearth)', '(it scuttles a tight circle round you)',
             '(the carved eyes follow a moth)', '(it crunches something. Probably a skeleton.)']
    HELLO = ('(it scuttles over, legs clicking)', '(it unfolds out of a burst of embers)', '(it folds its legs in and sinks into the embers)')
    SIT = ('(it unfolds its legs and stands)', '(it folds its legs and settles, glowing low)')
    FAINT = '(its fires go out)'
    NOT_YOURS = '(it hisses steam at you)'
    POWERS = [('Riding', 'walk to stride, jump to leap, walk into a wall to climb it; fire and falls can\'t touch you up there; sneak to get off'),
              ('The Glare', 'use the gourd while riding: a beam of fire from its eyes, 18 blocks ahead - 7 to everything in it, set alight (every 3 s)'),
              ('Ember Bite', 'a foe within 3: 5, and it burns'),
              ('Tongue Lash', 'every 5 s, a foe 5-12 away: dragged in by the tongue (4)'),
              ('Stomp', 'every 8 s, foes within 4: it rears and comes down - a burning shockwave that throws them (8)'),
              ('Ember Rain', 'charged, every 45 s: burning embers fall on every foe within 12 - three waves, 6 each'),
              ('Hallowfire', 'fire can\'t hurt you while it\'s near; on a Blood Moon it hits 3 harder')]
    INTRO = [T('The Arachno-Lantern', LN_C, bold=True), T(' - a young one, from the embers of the great one. ', 'gray'), T('It likes you. Climb on.', 'white')]
    BUTTONS = ((6, 'Ride', 'Climb on its back (sneak to get off).', 'p194/ride_ask'),)
    BURST = ['particle minecraft:flame ~ ~1.4 ~ 0.8 0.8 0.8 0.05 40', 'particle minecraft:large_smoke ~ ~1 ~ 0.8 0.6 0.8 0.03 20',
             'particle minecraft:lava ~ ~1.6 ~ 0.6 0.4 0.6 0 8']
    FADE_SOUND = 'playsound minecraft:block.fire.extinguish neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.blaze.ambient neutral @a[distance=..24] ~ ~ ~ 0.8 0.7', 'playsound minecraft:entity.spider.ambient neutral @a[distance=..24] ~ ~ ~ 0.8 0.6']
    ENC_POSES = [(0, 'sit_b'), (40, 'sit_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:flame ~ ~1.6 ~ 0.4 0.3 0.4 0.01 4'
    ADV = ('Kindled', 'Find a Kindled Gourd in the embers of the Scorching Arachno-Lantern - and take what hatches out of it home')
    ADMIN_HINT = 'In hard mode, the Scorching Arachno-Lantern leaves one in its embers for everyone near who has none.'
    MEET_HINT = 'Right-click it holding the Kindled Gourd.'


RP.register(C)
item('ln_gourd', TOTEM, 'Kindled Gourd', LN_C,
     ['A little carved gourd, still burning inside.', 'Something in it ticks like eight small legs.', ('Use: call the Arachno-Lantern (again: over).', 'blue'),
      ('Sneak + use: its menu - Ride.', 'blue'), ('Riding, use: THE GLARE - fire from its eyes.', 'blue'),
      ('If it falls: 2 minutes before it can return.', 'gray'), ('From the embers of the great one.', 'dark_gray')],
     model='bm:ln_gourd', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('doll_lantern', TOTEM, 'Arachno-Lantern Doll', LN_C, ['A doll of the Arachno-Lantern. Its legs wobble.', ('Right-click a block: set it down.', 'blue'),
                                                         ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_lantern', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_lantern'] = 'bm:p141/doll_lantern/use'
P141.DOLLS.append(('doll_lantern', 'The Arachno-Lantern', LN_C, 'A doll of the Arachno-Lantern. Its legs wobble.', 'minecraft:flame',
                   'minecraft:entity.spider.ambient', 'minecraft:small_flame'))
P141.DOLL_FROM['doll_lantern'] = ('ln_gourd', {'kh': 1.4, 'kb': 0.82, 'kl': 0.62, 'groups': {'bm:ln_tongue': 'head'}})
P134.FIT['ln_gourd'] = (0.0, 2.6, -1.4, 1.4, -1.4, 1.4)
POSES = A.POSES


def extend_offers(O, offer):
    pass


def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((3, 5, 12, 14), fill=hexc('#e8761c'), outline=hexc('#a8460c'))                 # the gourd
    d.line((5, 6, 5, 13), fill=hexc('#a8460c')); d.line((10, 6, 10, 13), fill=hexc('#a8460c'))
    d.rectangle((7, 2, 8, 5), fill=hexc('#5e7a2c'))                                            # its stem
    d.polygon([(4, 9), (6, 7), (6, 9)], fill=hexc('#ffc030')); d.polygon([(11, 9), (9, 7), (9, 9)], fill=hexc('#ffc030'))   # the carved eyes, lit
    d.line((5, 11, 10, 11), fill=hexc('#ffc030')); d.point((7, 12), fill=hexc('#ffc030'))
    d.point((2, 12), fill=hexc('#16111b')); d.point((13, 12), fill=hexc('#16111b')); d.point((1, 14), fill=hexc('#16111b')); d.point((14, 14), fill=hexc('#16111b'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(C, R, _icon())
    R.HATS['doll_lantern'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                   'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])


def textures():
    return A.textures()


def generate_early(G):
    RP.contract(C, G)


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.lngl dummy', 'scoreboard objectives add bm.lnlp dummy']
    G.OBJECTIVES += ['bm.lngl', 'bm.lnlp']

    def abilities(G, X):
        S, go, hit, end, face, foe, pfx = X.S, X.go, X.hit, X.end, X.face, X.foe, X.pfx
        idle = X.idle_fight
        lines = [# (ridden: its rider drives; it doesn't fight on its own)
                 'scoreboard players set #rid bm.rng 0', 'execute if function bm:p194/has_rider run scoreboard players set #rid bm.rng 1',
                 'execute if score #rid bm.rng matches 1 run function bm:p194/ride',
                 'execute if score #rid bm.rng matches 0 if entity @s[tag=bm.lnrd] run function bm:p194/unride',
                 f'execute {idle} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..12] run function bm:{pfx}/rain_go',
                 f'execute {idle} unless score @s {S("bc")} matches 1.. if entity @e[{foe},distance=..4] run function bm:{pfx}/stomp_go',
                 f'execute {idle} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..5] if entity @e[{foe},distance=..12] run function bm:{pfx}/lash_go',
                 f'execute {idle} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/bite_go']
        fn(f'{pfx}/bite_go', go(7, 5, 'mc', 18, ['playsound minecraft:entity.spider.hurt neutral @a[distance=..16] ~ ~ ~ 0.4 1.4']))
        fn(f'{pfx}/lash_go', go(8, 12, 'rc', 100, face('surprised', 12) + ['playsound minecraft:entity.frog.tongue neutral @a[distance=..16] ~ ~ ~ 1 0.6']))
        fn(f'{pfx}/stomp_go', go(11, 18, 'bc', 160, face('surprised', 18) + ['playsound minecraft:entity.ravager.roar neutral @a[distance=..20] ~ ~ ~ 0.5 1.4']))
        fn(f'{pfx}/rain_go', go(12, 60, 'gc', 900, face('surprised', 60) + ['playsound minecraft:entity.blaze.shoot neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                                                                             'playsound minecraft:item.firecharge.use neutral @a[distance=..24] ~ ~ ~ 1 0.5']))
        fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                               f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 2 run function bm:{pfx}/bite',
                               f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 7 run function bm:{pfx}/lash',
                               f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 8 run function bm:{pfx}/stomp',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 50 run function bm:{pfx}/rain',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 30 run function bm:{pfx}/rain',
                               f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 10 run function bm:{pfx}/rain'])
        moon = ['execute if score #active bm.bm matches 1 run scoreboard players add #pd bm.rng 3']
        fn(f'{pfx}/bite', hit(5) + moon + [f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/burnt'] + end)
        fn(f'{pfx}/burnt', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:80s}', 'particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.02 8',
                            'playsound minecraft:entity.blaze.hurt neutral @a[distance=..16] ~ ~ ~ 0.5 1.2'])
        fn(f'{pfx}/lash', hit(4) + moon + [f'execute as @e[{foe},distance=..12,sort=nearest,limit=1] run tag @s add bm.lntg',
                                           f'execute rotated as @s rotated ~ 0 positioned ^ ^1 ^2 run tp @e[tag=bm.lntg,limit=1] ~ ~ ~',
                                           f'execute as @e[tag=bm.lntg] at @s run function bm:{pfx}/hurt',
                                           'execute at @e[tag=bm.lntg,limit=1] run particle minecraft:dust{color:[0.55,0.15,0.8],scale:1.4} ~ ~1 ~ 0.3 0.3 0.3 0 10',
                                           'tag @e[tag=bm.lntg] remove bm.lntg', 'playsound minecraft:entity.frog.eat neutral @a[distance=..16] ~ ~ ~ 1 0.6'] + end)
        fn(f'{pfx}/stomp', hit(8) + moon + ['particle minecraft:flame ~ ~0.3 ~ 2.5 0.1 2.5 0.1 80', 'particle minecraft:explosion ~ ~0.5 ~ 1.5 0.2 1.5 0 4',
                                            'playsound minecraft:entity.generic.explode neutral @a[distance=..24] ~ ~ ~ 0.8 0.8',
                                            f'execute as @e[{foe},distance=..4.5] at @s run function bm:{pfx}/thrown'] + end)
        fn(f'{pfx}/thrown', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:60s}', 'data modify entity @s Motion[1] set value 0.7d'])
        fn(f'{pfx}/rain', hit(6) + moon + [f'execute as @e[{foe},distance=..12] at @s run function bm:{pfx}/ember'] + end)
        fn(f'{pfx}/ember', ['particle minecraft:lava ~ ~3 ~ 0.4 0.2 0.4 0 6', 'particle minecraft:flame ~ ~1 ~ 0.4 0.8 0.4 0.03 10',
                            f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:80s}'])
        # -- every second: Hallowfire (no fire for its owner nearby), its embers
        X.second.append(f'execute as @e[type=minecraft:wolf,tag={X.pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec')
        fn(f'{pfx}/sec', ['effect give @s minecraft:fire_resistance 3 0 true', 'execute on owner if entity @s[distance=..16] run effect give @s minecraft:fire_resistance 4 0 true',
                          'execute store result score #r bm.rng run random value 1..6',
                          'execute if score #r bm.rng matches 1 run particle minecraft:small_flame ~ ~2.2 ~ 0.6 0.2 0.6 0.01 3'])
        return lines

    def encounter(G, X):
        # the gourd, used before it's hatched: it cracks, and the little one unfolds out of it (enc/spawn), sitting in the embers
        fn('p194/enc/hatch', ['execute unless score #hard bm.cfg matches 1 run return run ' + say('The gourd stays cold. (Hard mode only.)', '#c8a0a0'),
                              'execute if entity @e[type=minecraft:interaction,tag=bm.lnenc,distance=..24] run return run ' + say('It\'s already out - right-click it with the gourd.', LN_LINE),
                              'execute positioned ^ ^ ^3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:p194/enc/crack',
                              'execute positioned ^ ^ ^1.5 run function bm:p194/enc/crack'])
        fn('p194/enc/crack', ['function bm:p194/enc/spawn', 'particle minecraft:flame ~ ~1 ~ 0.8 0.6 0.8 0.05 60', 'particle minecraft:lava ~ ~1 ~ 0.6 0.4 0.6 0 10',
                              'playsound minecraft:block.fire.ambient neutral @a[distance=..24] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.spider.ambient neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                              X.tellraw('@s', [T('The gourd cracks. ', LN_LINE, italic=True),
                                               T('Long black legs unfold out of the embers, one after another, and a little carved pumpkin settles on them, smouldering, and looks up at you.', 'gray', italic=True)])])
        fn('p194/enc/talk', [f'execute if entity @s[tag=bm.lnmet] run return run ' + X.csay('(it nuzzles your hand, warm as a hearth)'),
                             f'execute if items entity @s weapon.mainhand {holds("ln_gourd")} run return run function bm:p194/enc/recruit',
                             X.csay('(it looks at your empty hand, then at the gourd you brought it in)')])
        fn('p194/enc/recruit', [f'clear @s {holds("ln_gourd")} 1',
                                f'execute as {X.here} at @s run particle minecraft:flame ~ ~1.6 ~ 0.6 0.5 0.6 0.04 30',
                                f'execute as {X.here} at @s run playsound minecraft:entity.blaze.ambient neutral @a[distance=..16] ~ ~ ~ 1 1.4',
                                X.tellraw('@s', [T('It climbs into the cracked gourd\'s light like a cat into a sunbeam, ', LN_LINE, italic=True),
                                                 T('then unfolds again beside you - bigger, somehow - and crouches low, the way a horse would for a rider.', 'gray', italic=True)]),
                                'function bm:p194/enc/joined'])

    RP.build(C, G, abilities, encounter)
    pet = 'bm.lnpet'
    sel2 = '@e[type=minecraft:wolf,tag=bm.lnsel2,limit=1]'
    # ---- the gourd's use: not yet hatched - it hatches; riding - the Glare; the menu - Ride
    use = G.FUNCS['p194/use']
    use.insert(0, 'execute unless entity @s[tag=bm.lnmet] unless entity @s[tag=bm.gvp] run return run function bm:p194/enc/hatch')
    use.insert(1, 'execute if predicate bm:p21/riding if function bm:p194/on_it run return run function bm:p194/glare')
    fn('p194/on_it', [f'execute on vehicle if entity @s[type=minecraft:wolf,tag={pet}] run return 1', 'return 0'])
    fn('p194/has_rider', ['execute on passengers if entity @s[type=minecraft:player] run return 1', 'return 0'])
    fn('p194/ride_ask', ['scoreboard players operation #me bm.pid = @s bm.pid',
                         f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add bm.lnsel2',
                         f'execute unless entity {sel2} run return run ' + say('It isn\'t out - call it first.', LN_LINE),
                         'dialog clear @s', f'tp {sel2} @s', 'function bm:p194/mount', 'tag @e[tag=bm.lnsel2] remove bm.lnsel2'])
    fn('p194/mount', ['execute if predicate bm:p21/riding run return run ' + say('Get off your mount first.'),
                      f'data modify entity {sel2} Sitting set value 0b', f'ride @s mount {sel2}',
                      'playsound minecraft:entity.spider.ambient neutral @a[distance=..16] ~ ~ ~ 0.8 0.8',
                      title('@s', 'actionbar', [T('On its back. ', LN_C, bold=True), T('Walk to stride; jump to leap; walls - it climbs them. The gourd: THE GLARE. ', 'gray'),
                                                T('Sneak to get off.', 'dark_gray')])])
    # ---- riding: its rider's facing is its; walk to stride, jump to leap, into a wall - up it goes
    fn('p194/ride', ['tag @s add bm.lnrd', 'data modify entity @s Sitting set value 1b', 'scoreboard players set #fw bm.rng 0',
                     'execute on passengers if predicate bm:p39/forward run scoreboard players set #fw bm.rng 1',
                     'scoreboard players set #jp bm.rng 0', 'execute on passengers if predicate bm:p26/jump_key run scoreboard players set #jp bm.rng 1',
                     'execute on passengers if entity @s[type=minecraft:player] run function bm:p194/rider',
                     'execute on passengers if entity @s[type=minecraft:player] store result score #yaw bm.rng run data get entity @s Rotation[0] 100',
                     'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #yaw bm.rng',
                     'execute if score #fw bm.rng matches 1 run function bm:p194/drive',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[0] set value 0.0d',
                     'execute if score #fw bm.rng matches 0 run data modify entity @s Motion[2] set value 0.0d',
                     'execute if score #fw bm.rng matches 1 rotated as @s rotated ~ 0 positioned ^ ^ ^1.6 unless block ~ ~0.6 ~ #bm:grap_pass run function bm:p194/climb',
                     'execute if score #fw bm.rng matches 1 rotated as @s rotated ~ 0 positioned ^ ^ ^1.6 unless block ~ ~1.6 ~ #bm:grap_pass run function bm:p194/climb',
                     'execute if score #jp bm.rng matches 1 if predicate bm:p39/on_ground unless score @s bm.lnlp matches 1.. run function bm:p194/leap',
                     'execute if score @s bm.lnlp matches 1.. run scoreboard players remove @s bm.lnlp 1'])
    fn('p194/drive', ['data modify storage bm:tmp kxd.s set value 0.42d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                      'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                      'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng'])
    fn('p194/climb', ['data modify entity @s Motion[1] set value 0.34d', 'particle minecraft:block_crumble{block_state:"minecraft:stone"} ~ ~0.6 ~ 0.4 0.4 0.4 0 2'])
    fn('p194/leap', ['scoreboard players set @s bm.lnlp 14', 'data modify storage bm:tmp kxd.s set value 1.3d', 'function bm:p79/pet/dir with storage bm:tmp kxd',
                     'execute store result entity @s Motion[0] double 0.001 run scoreboard players get #mx bm.rng',
                     'execute store result entity @s Motion[2] double 0.001 run scoreboard players get #mz bm.rng',
                     'data modify entity @s Motion[1] set value 0.62d', 'particle minecraft:flame ~ ~0.2 ~ 0.8 0.1 0.8 0.05 20',
                     'playsound minecraft:entity.spider.step neutral @a[distance=..16] ~ ~ ~ 1 0.6'])
    fn('p194/rider', ['tag @s add bm.lnrider', 'effect give @s minecraft:fire_resistance 3 0 true',
                      'execute unless entity @s[tag=bm.lnfall] run attribute @s minecraft:fall_damage_multiplier modifier add bm:ln_ride -1 add_multiplied_total',
                      'tag @s add bm.lnfall'])
    fn('p194/unride', ['tag @s remove bm.lnrd', 'data modify entity @s Sitting set value 0b', 'scoreboard players set @s bm.ljs -1'])
    G.FUNCS['loop/second'][-1:-1] = ['execute as @a[tag=bm.lnrider] unless function bm:p194/on_it run function bm:p194/rider_off']
    fn('p194/rider_off', ['tag @s remove bm.lnrider', 'tag @s remove bm.lnfall', 'attribute @s minecraft:fall_damage_multiplier modifier remove bm:ln_ride'])
    # (its state while ridden: its own motion picks walk / run / leap - never the sit cycle, though it's "sitting" to keep its AI still)
    G.FUNCS['p194/state'].insert(0, 'execute if entity @s[tag=bm.lnrd] run return run function bm:p194/ride_state')
    fn('p194/ride_state', ['execute store result score #og bm.rng run data get entity @s OnGround',
                           'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                           'execute if score #og bm.rng matches 0 if score @s bm.lnlp matches 1.. run return run scoreboard players set #st bm.rng 3',
                           'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                           'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                           'scoreboard players operation #vx bm.rng += #vz bm.rng',
                           'execute if score #vx bm.rng matches 60000.. run return run scoreboard players set #st bm.rng 2',
                           'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                           'scoreboard players set #st bm.rng 0'])
    # ---- THE GLARE (from the saddle): a beam of fire from its eyes, 18 blocks along the rider's look - every 3 s
    fn('p194/glare', ['execute if score @s bm.lngl matches 1.. run return run ' + say('Its eyes are still gathering fire...', LN_LINE),
                      'scoreboard players set @s bm.lngl 60', 'tag @s add bm.lnglr',
                      'playsound minecraft:entity.blaze.shoot neutral @a[distance=..32] ~ ~ ~ 1 0.6', 'playsound minecraft:item.firecharge.use neutral @a[distance=..32] ~ ~ ~ 1 0.8',
                      'execute anchored eyes positioned ^ ^ ^1.5 run function bm:p194/beam', 'tag @s remove bm.lnglr'] +
       [f'execute anchored eyes positioned ^ ^ ^{1.5 + 1.5 * i:.1f} run particle minecraft:flame ~ ~ ~ 0.15 0.15 0.15 0.02 6' for i in range(12)])
    fn('p194/beam', ['execute as @e[type=#bm:hostile,tag=!bm.npc,distance=..1.6,tag=!bm.lngld] at @s run function bm:p194/glared',
                     'execute positioned ~ ~-1.4 ~ as @e[type=#bm:hostile,tag=!bm.npc,distance=..1.6,tag=!bm.lngld] at @s run function bm:p194/glared',   # (anything under the beam, too: it's high up on the Lantern)
                     'scoreboard players add #gb bm.rng 1', 'execute unless block ~ ~ ~ #bm:grap_pass run return run function bm:p194/beam_end',
                     'execute if score #gb bm.rng matches 12.. run return run function bm:p194/beam_end',
                     'execute positioned ^ ^ ^1.5 run function bm:p194/beam'])
    fn('p194/beam_end', ['scoreboard players set #gb bm.rng 0', 'tag @e[tag=bm.lngld] remove bm.lngld'])
    fn('p194/glared', ['tag @s add bm.lngld', 'damage @s 7 minecraft:in_fire by @a[tag=bm.lnglr,limit=1]', 'data merge entity @s {Fire:100s}',
                       'particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 4'])
    G.FUNCS['tick'].append('scoreboard players remove @a[scores={bm.lngl=1..}] bm.lngl 1')
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.lnrider] run function bm:p194/rider_off']

    # ---- THE KINDLED GOURD: the great one, fallen in hard mode, leaves one in its embers for everyone near who has none
    G.FUNCS['p82/reward'].append(f'execute if score #hard bm.cfg matches 1 unless entity @s[tag=bm.lnmet] unless items entity @s container.* {holds("ln_gourd")} run function bm:p194/found')
    fn('p194/found', [G.give('ln_gourd'), 'playsound minecraft:block.fire.ambient player @s ~ ~ ~ 1 1.4',
                      tellraw('@s', G.PREFIX + [T('A Kindled Gourd! ', LN_C, bold=True), T('In the embers, a little carved gourd is still burning - and something inside it ticks like eight small legs.', 'gray')])])
