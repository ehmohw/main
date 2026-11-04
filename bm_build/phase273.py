"""3.1: TALUS, THE MOSSBACK TITAN - the 62nd follower (kaiju_ape_art.py; fol5flag.TALUS). The old mountain that guards the jungle: a
knuckle-walking stone ape with a moss pelt and an amethyst crystal ridge - at a companion's size by default (~2.6 blocks), the kaiju's
own (~8.1) at its menu's Full Size. It carries you: its menu's Ride (kaiju_ride - always full size).

MEETING IT    it needs your Rex's roar to wake it. THE ECHO: ride your Atomic Rex (or the Mecha) and ROAR in a jungle - the jungle answers
              with a distant chest-beat; a boulder of copies crashes down nearby and bursts; in its dust, a HEARTGEODE SEED (once).
              THE GEODE: drop the seed on budding amethyst in a Lush Cave - it roots (amethyst light creeping round it); after 60 s it's
              a HEARTGEODE. THE DRUMS: carry it up a mountain (the Jagged, Frozen or Stony Peaks, above y 160) at dawn, set it down, and
              play the call on note blocks - eight beats within 10 s. The mountain answers: Talus climbs up out of the peak (if your Rex
              is out, they roar at each other first). Right-click it: the MOSSBACK DRUM, and it comes along.
ITS WAYS      CLIMBING LEAP (a foe within 4, every 6 s: it coils and bounds onto it - a small pound, 8); GROUND POUND (two foes within
              6, every 8 s: both fists down, a ring of cracked copies of the ground heaves up - 10 to all, knocked up); BOULDER THROW
              (a foe 4-24 off, every 10 s: it tears up a boulder of copies and lobs it - 12, and a splash); WAR-DRUM (you hurt, a foe
              near, every 20 s: four beats on its chest - allies within 10 Strength and Resistance, monsters weakened). Its Piercing
              Blow: the FIST FLURRY, on screen (planted, a flurry of fists, then both brought down at once - its ridge lit throughout).
RIDING        the menu's Ride: level - BOULDER THROW, down - GROUND POUND, up - WAR-DRUM (its drum used as you ride). Sneak off.
EVERYTHING ELSE is every follower's: sitting (right-click: on its haunches; sneak: cross-legged like a cairn), a wardrobe (Autumn Moss
and Snowcap - drawn - Basalt Moss, the metal pelts), a rare aura (Geode Heart), a shiny (Living Jade), the Partner Wheel, a frame (it
climbs out; a right-click: a drum-boom), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun,
Henry and Nia. A KAIJU (bm.kaiju) - the Rex's rival, and Trivyrn's."""
from items import item, T, TOTEM
from useitem import hold
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235
import kaiju_ride as KR

S5 = fol5.SPEC['talus']
A0 = fol5art.get('talus')
M = A0.M
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
K_UP = A0.K_UP
HIT_C = (1.6, 2.7)
HIT_F = (4.6, 8.2)
HOST_C, HOST_F = 1.4, 3.8
import phase272 as _P272  # noqa: E402
_P272.KAIJU.append('talus')

item(ITEM, TOTEM, 'The Mossback Drum', COL,
     ['A small hand drum of stone and moss, an amethyst stud in it.', 'Somewhere, a mountain answers it.',
      ('Use: call Talus (again: call it over).', 'blue'), ('Sneak + use: its menu - Ride, Full Size, its wardrobe.', 'blue'),
      ('Riding it: use it to throw, pound, or drum.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
item('heartgeode_seed', TOTEM, 'Heartgeode Seed', '#b48cff', ['A violet crystal, humming.', ('Root it on budding amethyst, in a Lush Cave.', 'gray')],
     model='minecraft:amethyst_shard', stack=1, cat='magic', glint=True, comps=hold('none'))
item('heartgeode', TOTEM, 'Heartgeode', '#c8a0ff', ['A geode with a heartbeat.', ('Carry it up a mountain at dawn - and play the drums.', 'gray')],
     model='minecraft:amethyst_cluster', stack=1, cat='magic', glint=True, comps=hold('none'))


class Talus(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'talus', 'Talus', COL, LINE, 'p273', 'tl', 'tt'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 6910, 60, 120, ITEM
    pron, they = 'it', 'it'
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=12, attack_damage=6, movement_speed=0.32, follow_range=32, step_height=1.6)
    SCALE, HIT = HOST_C, HIT_C
    BOX_FIT = True
    BUTTONS = ((6, 'Ride', 'It stands up to its full size: climb on (sneak to get off).', 'p273/ride'),
               (7, 'Full Size: on / off', 'On: the mountain\'s own size, ~8 blocks (and its hitbox). Off: a companion\'s, ~2.6.', 'p273/csz/toggle'))
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (120, 'idle_b')]), (160, [(0, 'sit_a'), (80, 'sit_a')]), (None, [(0, 'happy'), (16, 'idle_a')]),
                     {7: (None, [(0, 'leap_0'), (8, 'leap_1'), (14, 'idle_a')]), 11: (None, [(0, 'pound_0'), (10, 'pound_1'), (18, 'idle_a')]),
                      8: (None, [(0, 'throw_0'), (14, 'throw_1'), (22, 'idle_a')]),
                      13: (None, [(0, 'beat_0'), (4, 'beat_1'), (8, 'beat_0'), (12, 'beat_1'), (16, 'beat_0'), (20, 'idle_a')])}, wp=24, rp_=12)
    DUR = dict(P235._DUR, leap_0=8, leap_1=4, pound_0=10, pound_1=2, throw_0=14, throw_1=3, beat_0=2, beat_1=2, sit_a=12, sit_b=20, happy=8,
               walk_0=6, walk_1=6, walk_2=6, walk_3=6, run_0=3, run_1=3, run_2=3, run_3=3)
    QUIPS = ['(a low hum from its crystal ridge)', '(it knuckle-walks beside you, very carefully, so as not to step on you)', '(it beats its chest, once, softly - hello)',
             '(it picks up a pebble, looks at it, and puts it in its pelt)', '(somewhere, a mountain hums back)', '(it sniffs the air - jungle, far off)']
    HELLO = ('(Talus knuckle-walks back to you, the ground thudding)', '(the ground shakes - and Talus climbs up out of it, and beats its chest)',
             '(it beats its chest goodbye, and sinks back into the stone)')
    SIT = ('(it rises off its haunches)', '(it settles on its haunches, knuckles resting, head up)')
    FAINT = '(a long, low rumble - its crystals go dark)'
    NOT_YOURS = '(it looks down at you, a long time, and doesn\'t move)'
    POWERS = [('Climbing Leap', 'a foe within 4, every 6 s: it coils and bounds onto it - a small pound, 8'),
              ('Ground Pound', 'two foes within 6, every 8 s: both fists down, the ground heaves - 10 to all, knocked up'),
              ('Boulder Throw', 'a foe 4-24 off, every 10 s: a boulder of copies torn up and lobbed - 12, and a splash'),
              ('War-Drum', 'you hurt, a foe near, every 20 s: four beats on its chest - allies Strength and Resistance, monsters weakened'),
              ('Ride', 'its menu: it stands up to its full size - climb on (sneak to get off)'),
              ('Full Size', 'its menu: the mountain\'s own size (~8 blocks) - or a companion\'s (~2.6); its hitbox with it')]
    INTRO = [T('Talus', COL, bold=True), T(' - the old mountain that guards the jungle, woken by your Rex\'s roar. ', 'gray'), T('(DOOM. DOOM.)', LINE, italic=True)]
    BURST = ['particle minecraft:end_rod ~ ~1 ~ 0.6 1.0 0.6 0.03 20', 'particle minecraft:block{block_state:"minecraft:moss_block"} ~ ~0.5 ~ 0.8 0.4 0.8 0 30']
    FADE_SOUND = 'playsound minecraft:entity.warden.dig neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.warden.emerge neutral @a[distance=..24] ~ ~ ~ 0.6 1.0', 'playsound minecraft:block.amethyst_block.resonate neutral @a[distance=..24] ~ ~ ~ 1 0.6']
    ENC_POSES = [(0, 'idle_a'), (30, 'beat_0'), (34, 'beat_1'), (38, 'beat_0'), (42, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:end_rod ~ ~2 ~ 0.6 0.6 0.6 0.01 6'
    ADV = ('Mountain Range', 'Wake the mountain that guards the jungle - with your Rex\'s roar, a Heartgeode and its drums')
    ADMIN_HINT = 'Ride a Rex and roar in a jungle; root the seed on budding amethyst in a Lush Cave; play the drums on a peak at dawn (admin/talus_meet_here).'
    MEET_HINT = 'Right-click it.'


_DOLL = 'A doll of Talus - a little mossy stone ape, an amethyst ridge down its back, sat with its hands in its lap.'
_eff = W5.pair_fx
_PAIRS = {
    'tl_bender': ('talus', 'bender', 'For Fossils', '#e0a860', 'Talus and Bender - Bender digs, and Talus scoops up a boulder to help',
                  _eff(('haste', 0), ('strength', 0)),
                  [('bender', '(digs a hole. "For fossils.")'), ('talus', '(scoops up a whole boulder beside him, to help)')],
                  [('talus', '(it offers Bender a crystal)', 'bender', '(buries it, very proudly)')]),
    'tl_capshun': ('talus', 'capshun', 'A Crown', '#f0f0f0', 'Talus and Mr. Capshun - he draws Talus a crown, and Talus wears it',
                   _eff(('resistance', 0), ('luck', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He drew the mountain a crown. It fit."]'), ('talus', '(it wears the tiny drawn crown, very carefully)')],
                   [('talus', '(it holds very still for the drawing)', 'capshun', '[Mr. Capshun narrates: "It was a long sitting."]')]),
}
W5.register(Talus, A0, _DOLL, ('minecraft:end_rod', 'minecraft:block.amethyst_block.resonate', 'minecraft:poof'), _PAIRS, 'Talus')

# ---- its Piercing Blow, on screen: THE FIST FLURRY - planted wide, a flurry of fists (each a 2-tick snap), both fists high and
#      the two-fisted hammer down - its ridge lit (_ch) throughout
import phase226 as _P226  # noqa: E402
_ridge = lambda on: f'execute as @e[type=minecraft:item_display,tag=bm.tlsel,tag=bm.tlp_ridge] run data modify entity @s item.components."minecraft:item_model" set value "bm:tl_ridge{"_ch" if on else ""}"'
_imp = ['particle minecraft:crit ~ ~1.2 ~ 0.3 0.3 0.3 0.3 10', 'particle minecraft:end_rod ~ ~1.2 ~ 0.2 0.2 0.2 0.1 6']
_P226.ASSAULT['talus'] = dict(pfx='p273', s_obj='bm.tts', anim='p273/anim', busy='bm.ttx', end=38, dash=dict(reach=2.4, speed=0.9, lift=0), free=True,
                              hits={1: (2, _imp, 'minecraft:block.amethyst_cluster.break', 1.0),
                                    2: (6, _imp + ['particle minecraft:explosion ~ ~0.4 ~ 0.6 0.1 0.6 0 3', 'data modify entity @s Motion[1] set value 0.5d'], 'minecraft:entity.generic.explode', 0.7)},
                              tl={1: ['P flurry_0', _ridge(True), 'S minecraft:entity.warden.sonic_charge 0.8 0.8'], 2: ['DASH'],
                                  3: ['P flurry_1', 'H1'], 5: ['P flurry_2'], 7: ['P flurry_3', 'H1'], 9: ['P flurry_0'], 11: ['P flurry_1', 'H1'],
                                  13: ['P flurry_2'], 15: ['P flurry_3', 'H1'], 16: ['P flurry_fin_0'], 24: ['P flurry_fin_1'], 25: ['H2'],
                                  34: ['P idle_a', _ridge(False)]})
_P226.NAMES['talus'] = ('Fist Flurry', 'plants itself and hammers the monster with a flurry of fists, then brings both down on it at once')


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Talus, G)


def _icon():
    from sprites280 import S
    s = S()
    pal = {'s': '#6a6a72', 'd': '#3a3a40', 'm': '#4a7a3a', 'v': '#b48cff'}
    s.g(['..mmmmmm..', '.mssssssm.', 'msddddddsm', 'msd.vv.dsm', 'msddddddsm', '.mssssssm.', '..mmmmmm..'], pal, 3, 4)
    return s.render()


def rp(R):
    W5.rp(Talus, R, _icon(), A0)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.9, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..24] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=14, at=6, cd=120, reach=4.0, face='serious', go=[snd('entity.warden.attack_impact', 0.6, 1.2)]),
             crowd=dict(st=11, x=18, at=8, cd=160, r=6, n=2, face='serious', go=[snd('entity.ravager.roar', 0.6, 1.4)]),
             ranged=dict(st=8, x=22, at=8, cd=200, near=4, far=24, face='serious', go=[snd('block.stone.break', 1.0, 0.6)]),
             support=dict(st=13, x=20, at=[16, 12, 8, 4], cd=400, face='happy', go=[snd('block.note_block.basedrum', 1.2, 0.6)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    fn(f'{pfx}/melee', X.hit(8) + [f'execute as @e[{foe},distance=..4.4,sort=nearest,limit=1] at @s run function bm:{pfx}/pounded1',
                                   'particle minecraft:block{block_state:"minecraft:stone"} ~ ~0.1 ~ 1.2 0.1 1.2 0 30'] + X.end)
    fn(f'{pfx}/pounded1', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.3d'])
    fn(f'{pfx}/crowd', X.hit(10) + [f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/pounded', 'particle minecraft:explosion ~ ~0.2 ~ 2.5 0 2.5 0 6',
                                    'particle minecraft:block{block_state:"minecraft:stone"} ~ ~0.1 ~ 3 0.1 3 0 60', snd('entity.generic.explode', 1.0, 0.5)] + X.end)
    fn(f'{pfx}/pounded', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.5d'])
    fn(f'{pfx}/ranged', X.hit(12) + [f'execute as @e[{foe},distance=..24.5,sort=nearest,limit=1] at @s run function bm:{pfx}/boulder'] + X.end)
    fn(f'{pfx}/boulder', [f'function bm:{pfx}/hurt', f'execute as @e[{foe},distance=..3] run function bm:{pfx}/hurt',
                          'particle minecraft:block{block_state:"minecraft:cobblestone"} ~ ~1 ~ 1.2 0.6 1.2 0 50', 'particle minecraft:explosion ~ ~0.5 ~ 0.5 0.2 0.5 0 2',
                          snd('block.stone.break', 1.4, 0.5)])
    for i in ('', '2', '3', '4'):
        fn(f'{pfx}/support{i}', ['particle minecraft:end_rod ~ ~2 ~ 1.5 0.3 1.5 0.05 24', snd('block.note_block.basedrum', 1.4, 0.5),
                                 'effect give @a[distance=..10,gamemode=!spectator] minecraft:strength 10 0 true', 'effect give @a[distance=..10,gamemode=!spectator] minecraft:resistance 10 0 true',
                                 f'effect give @e[{foe},distance=..10] minecraft:weakness 6 0'])
    X.second.append('tag @e[type=minecraft:wolf,tag=bm.tlpet] add bm.kaiju')
    return lines


def _encounter(G, X):
    """THE ECHO (a Rex's roar ridden in a jungle) - THE GEODE (a lush cave's budding amethyst) - THE DRUMS (a peak at dawn)"""
    fn, tellraw, title, give = G.fn, G.tellraw, G.title, G.give
    G.wjson('bm/predicate/p273/jungle.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': '#minecraft:is_jungle'}})
    G.wjson('bm/predicate/p273/lush.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': 'minecraft:lush_caves'}})
    G.wjson('bm/predicate/p273/peak.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': ['minecraft:jagged_peaks', 'minecraft:frozen_peaks', 'minecraft:stony_peaks']}})
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.ttg dummy', 'scoreboard objectives add bm.ttb dummy', 'scoreboard objectives add bm.ttbt dummy']
    G.OBJECTIVES += ['bm.ttg', 'bm.ttb', 'bm.ttbt']
    csay = lambda txt: title('@s', 'actionbar', [T('Talus: ', COL, bold=True), T(txt, LINE)])
    # (THE ECHO - phase249's ride roar, in a jungle: once a player)
    fn('p273/enc/echo', ['execute if entity @s[tag=bm.tlecho] run return 0', 'execute unless predicate bm:p273/jungle run return 0', 'tag @s add bm.tlecho',
                         'playsound minecraft:entity.warden.sonic_charge ambient @s ~ ~ ~ 1 0.5', 'playsound minecraft:block.note_block.basedrum ambient @s ~ ~ ~ 1 0.5',
                         'execute rotated ~ 0 positioned ^ ^ ^14 positioned over motion_blocking run function bm:p273/enc/crash',
                         tellraw('@s', [T('The jungle answers - a distant chest-beat. ', LINE, italic=True), T('Something crashes down not far off.', 'gray', italic=True)])])
    fn('p273/enc/crash', ['particle minecraft:block{block_state:"minecraft:mossy_cobblestone"} ~ ~1 ~ 1.4 1 1.4 0 80', 'particle minecraft:explosion ~ ~1 ~ 1 0.5 1 0 4',
                          'playsound minecraft:entity.generic.explode ambient @a[distance=..48] ~ ~ ~ 1.4 0.5',
                          'loot spawn ~ ~0.5 ~ loot bm:items/heartgeode_seed'])
    # (THE GEODE: the seed - an item on budding amethyst, in a lush cave - roots; 60 s: a Heartgeode)
    X.second.append('execute as @e[type=minecraft:item] if items entity @s contents *[minecraft:custom_data~{bm:"heartgeode_seed"}] at @s run function bm:p273/enc/root')
    fn('p273/enc/root', ['execute unless block ~ ~-0.5 ~ minecraft:budding_amethyst run return run scoreboard players set @s bm.ttg 0',
                         'execute unless predicate bm:p273/lush run return run scoreboard players set @s bm.ttg 0',
                         'scoreboard players add @s bm.ttg 1', 'data merge entity @s[type=minecraft:item] {Age:-32768s,PickupDelay:40s}',
                         'particle minecraft:end_rod ~ ~0.3 ~ 0.8 0.1 0.8 0.01 4', 'particle minecraft:dust{color:[0.7,0.5,1.0],scale:1.0} ~ ~0.1 ~ 1.2 0 1.2 0 8',
                         'execute if score @s bm.ttg matches 60.. run function bm:p273/enc/grown'])
    fn('p273/enc/grown', ['loot spawn ~ ~0.2 ~ loot bm:items/heartgeode', 'kill @s', 'playsound minecraft:block.amethyst_block.resonate ambient @a[distance=..16] ~ ~ ~ 1.2 0.6',
                          'particle minecraft:end_rod ~ ~0.5 ~ 0.4 0.4 0.4 0.05 30'])
    # (THE DRUMS: a Heartgeode set down on a peak above y 160 at dawn - and eight note-block beats within 10 s)
    G.wjson('bm/advancement/p273/drum.json', {'criteria': {'drum': {'trigger': 'minecraft:default_block_use', 'conditions': {'location': [
        {'condition': 'minecraft:location_check', 'predicate': {'block': {'blocks': 'minecraft:note_block'}}}]}}},
        'rewards': {'function': 'bm:p273/enc/beat'}})
    fn('p273/enc/beat', ['advancement revoke @s only bm:p273/drum', 'scoreboard players add @s bm.ttb 1', 'scoreboard players set @s bm.ttbt 10',
                         'execute if score @s bm.ttb matches 8.. at @s run function bm:p273/enc/drums'])
    X.second.append('execute as @a[scores={bm.ttbt=1..}] run function bm:p273/enc/beat_s')
    fn('p273/enc/beat_s', ['scoreboard players remove @s bm.ttbt 1', 'execute if score @s bm.ttbt matches 0 run scoreboard players set @s bm.ttb 0'])
    fn('p273/enc/drums', ['scoreboard players set @s bm.ttb 0', 'execute if entity @s[tag=bm.tlmet] run return 0',
                          'execute unless entity @s[y=160,dy=200] run return 0', 'execute unless predicate bm:p273/peak run return 0',
                          'execute unless score #tod bm.bm matches 22500..24000 unless score #tod bm.bm matches 0..1500 run return run ' +
                          title('@s', 'actionbar', T('(the mountain is silent - it listens for the drums at dawn)', 'gray')),
                          'execute if entity @e[type=minecraft:interaction,tag=bm.tlenc,distance=..48] run return 0',
                          'scoreboard players set #hg bm.rng 0',
                          'execute as @e[type=minecraft:item,distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"heartgeode"}] run scoreboard players set #hg bm.rng 1',
                          'execute if score #hg bm.rng matches 0 run return 0',
                          'execute as @e[type=minecraft:item,distance=..8] if items entity @s contents *[minecraft:custom_data~{bm:"heartgeode"}] run kill @s',
                          'scoreboard players operation #me bm.pid = @s bm.pid', 'function bm:p273/enc/wake'])
    fn('p273/enc/wake', ['playsound minecraft:entity.warden.emerge ambient @a[distance=..48] ~ ~ ~ 1.4 0.6', 'particle minecraft:block{block_state:"minecraft:stone"} ~ ~ ~ 3 0.3 3 0 100',
                         'execute rotated ~ 0 positioned ^ ^ ^4 run function bm:p273/enc/spawn',
                         'scoreboard players operation @e[type=minecraft:interaction,tag=bm.tlenc,distance=..8] bm.pid = #me bm.pid',
                         'execute as @e[type=minecraft:wolf,tag=bm.rypet,distance=..24] if score @s bm.pid = #me bm.pid run function bm:p273/enc/rival',
                         tellraw('@s', [T('The mountain answers. ', LINE, bold=True), T('The ground shakes; a ridge of crystals breaks the surface - and Talus climbs up out of the peak.', 'gray', italic=True)])])
    fn('p273/enc/rival', ['playsound minecraft:entity.ravager.roar ambient @a[distance=..32] ~ ~ ~ 1.4 0.7',
                          tellraw('@a[distance=..24]', [T('Talus roars at your Rex - and your Rex roars back. ', LINE, italic=True), T('(A long, long standoff. Then Talus beats its chest - and lets you near.)', 'gray', italic=True)])])
    fn('p273/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('(it looks down at you, a long time, and doesn\'t move)'),
                         tellraw('@s', [T('It beats its chest, once - and hands you a little drum of stone and moss.', LINE, italic=True)]), 'function bm:p273/enc/joined'])
    fn('admin/talus_meet_here', ['execute rotated ~ 0 positioned ^ ^ ^4 run function bm:p273/enc/spawn',
                                 'scoreboard players operation @e[type=minecraft:interaction,tag=bm.tlenc,distance=..8] bm.pid = @s bm.pid'])


def late(G):
    """(after phase249: the Echo - its ride roar, as the rider)"""
    L = G.FUNCS.get('p249/try/roar')
    if L is not None:
        L.append('function bm:p273/enc/echo')


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt: title('@s', 'actionbar', [T('Talus: ', COL, bold=True), T(txt, LINE)])
    frame = dict(models=[], click=['playsound minecraft:block.note_block.basedrum block @a[distance=..12] ~ ~ ~ 1 0.6', 'particle minecraft:end_rod ~ ~0.2 ~ 0.2 0.05 0.2 0.02 8'])
    W5.build(Talus, G, _abilities, _encounter, sitb=(160, [(0, 'sit_b'), (80, 'sit_b')]), frame=frame)
    pfx = Talus.pfx
    W5.poses_for(Talus, G, ['flurry_0', 'flurry_1', 'flurry_2', 'flurry_3', 'flurry_fin_0', 'flurry_fin_1'])    # (its Piercing Blow's: in no cycle)
    # ---- FULL SIZE (compsize, the Rex's way: built at a companion's size, the twin its own)
    import compsize as CSZ
    CSZ.build(G, pfx, 'bm.ttcs', 'bm.ttcz', f'bm.{Talus.q}s', HOST_C, HOST_F,
              say('(it rises, and rises - Full Size: on)'), say('(it settles down to your size - Full Size: off)'), hit=('bm.tlhit', HIT_C, HIT_F))
    CSZ.LATE.append((pfx, K_UP, 'bm.ttcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    T_[1:1] = CSZ.sync(pfx, 'bm.ttcs', 'bm.ttcz', f'bm.{Talus.q}s', HOST_C, HOST_F)
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag=bm.ttcz] run function bm:{pfx}/box/full'])
    fn(f'{pfx}/box/full', CSZ.resize('bm.tlhit', *HIT_F))
    # ---- RIDE (kaiju_ride: its full-size rig on a saddled host; level: the boulder, down: the pound, up: the war-drum)
    ride = KR.build(G, dict(key='tl', pfx=pfx, art=M.R, scale=M.R.RIG_SCALE, seat=(7.07, 1.56), hp=200, walk=0.3, run=0.42, name='Talus', col=COL,
                            poses=dict(sit='sit_a', idle='ride', walk=['walk_0', 'walk_1', 'walk_2', 'walk_3'], run=['run_0', 'run_1', 'run_2', 'run_3']),
                            moves=dict(level=('p273/rmv/throw', 10), down=('p273/rmv/pound', 8), up=('p273/rmv/drum', 20)), follower_back=f'{pfx}/try_summon'))
    foe = 'type=#bm:hostile,tag=!bm.npc'
    fn('p273/rmv/throw', [f'execute positioned ^ ^4 ^6 as @e[{foe},distance=..8,sort=nearest,limit=1] at @s run function bm:p273/rmv/hit {{d:12}}',
                          'particle minecraft:block{block_state:"minecraft:cobblestone"} ^ ^5 ^8 1.2 0.6 1.2 0 50', 'playsound minecraft:block.stone.break neutral @a[distance=..32] ~ ~ ~ 1.4 0.5'])
    fn('p273/rmv/pound', [f'execute as @e[{foe},distance=..7] at @s run function bm:p273/rmv/hit {{d:10}}', 'particle minecraft:explosion ~ ~0.2 ~ 3 0 3 0 8',
                          'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 1.2 0.5'])
    fn('p273/rmv/drum', ['effect give @a[distance=..10,gamemode=!spectator] minecraft:strength 10 0 true', 'effect give @a[distance=..10,gamemode=!spectator] minecraft:resistance 10 0 true',
                         f'effect give @e[{foe},distance=..10] minecraft:weakness 6 0', 'playsound minecraft:block.note_block.basedrum neutral @a[distance=..32] ~ ~ ~ 1.6 0.5',
                         'particle minecraft:end_rod ~ ~6 ~ 2 0.5 2 0.05 40'])
    fn('p273/rmv/hit', ['$damage @s $(d) minecraft:mob_attack', 'data modify entity @s Motion[1] set value 0.4d'])
    fn('p273/ride', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #on bm.rng 0',
                     f'execute as @e[type=minecraft:wolf,tag=bm.tlpet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run scoreboard players set #on bm.rng 1',
                     'execute if score #on bm.rng matches 0 run return run ' + say('(call it first - then ride it)'),
                     'execute if function bm:p20/frog/has_vehicle run return run ' + say('(get down first)'),
                     f'execute as @e[type=minecraft:wolf,tag=bm.tlpet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run tag @s add bm.tlsel2', f'function bm:{pfx}/dismiss',
                     f'function bm:{ride["ride"]}'])
    G.FUNCS[f'{pfx}/use'].insert(0, f'execute if function bm:{ride["riding"]} run return run function bm:{ride["use"]}')
    fn('admin/talus_reset', ['tag @s remove bm.tlmet', 'tag @s remove bm.tlecho', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                             title('@s', 'actionbar', T('Talus has not met you yet.', COL))])
