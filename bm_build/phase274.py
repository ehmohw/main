"""3.1: TRIVYRN, THE THREE-WORLD WYRM - the 63rd follower (kaiju_hydra_art.py; fol5flag.TRIVYRN). A three-headed wyrm, one head of each
world: SQUALL (storm, who thinks it's in charge), CINDER (fire, who bites first) and HUSH (the void, who stares). A companion's size by
default (~2.45 blocks), the kaiju's own (~7.6) at its menu's Full Size; its menu's Ride carries you (kaiju_ride - and it GLIDES: off a
height, its wings spread and it drifts down).

MEETING IT    its scales only shed once your Rex is hatched (or your Mecha built). THREE SCALES: a Squall Scale (a Breeze, 1 in 40), a
              Cinder Scale (Ancient Debris, 1 in 300 - or a Magma Cube in a Basalt Delta, 1 in 40), a Hush Scale (a Shulker, 1 in 30).
              THE PORTAL: all three thrown into a lit Nether portal together - drawn between the worlds, they fuse into the THREE-WORLD
              EGG (fire- and lightning-proof). THREE CRACKS: each world cracks its own seam - dropped on a peak above y 150 in a
              thunderstorm (Squall pokes out and complains); on magma in a Basalt Delta (Cinder bites its way out); on End stone out
              past 1000 blocks (Hush opens one eye). The last crack hatches it: the three heads squabble over who gives you the
              TRIUNE HORN (Cinder wins), and it comes along.
ITS WAYS      THE LASH (a foe within 7, every 6 s: three snake-strikes in turn - Cinder first, then Squall, then Hush - 8 each);
              WING GUST (two foes within 10, every 8 s: a cone of wind, knocked far back); TRI-BREATH (a foe 4-14 off, every 12 s: Squall's
              forked bolt (6, chaining to two more), Cinder's fire (6, alight), Hush's void (4, lifted and let down gently)). Its Piercing
              Blow: LIGHTNING BREATH, on screen (all three rear back, the storm crackles over its scales tail to heads - and a braided
              lightning stream from every head, swaying, into the monster).
RIDING        the menu's Ride: level - the TRI-BREATH, down - the WING GUST, up - all three at once; it glides.
EVERYTHING ELSE is every follower's: sitting (crouched low, three heads watching three ways; sneak: curled up, Hush one eye open), a
wardrobe (Dawnscale and Abyssal - drawn - Storm Grey, the metal scales), a rare aura (the Three Worlds), a shiny (Opal), the Partner
Wheel, a frame, a display case, Cecil's doll (three big heads - each grown on its own neck), the honours, a Raid Contract; pairs with
Bender, Mr. Capshun, Henry and Nia. A KAIJU - and THE KAIJU TRIO BOND: the Rex, Talus and Trivyrn all out - allies within 16 Resistance I
("Three Titans"); once a day, the TRIPLE THREAT: all three Piercing Blows on one monster, one after the other."""
from items import item, T, TOTEM
from useitem import hold
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235
import kaiju_ride as KR

S5 = fol5.SPEC['trivyrn']
A0 = fol5art.get('trivyrn')
M = A0.M
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
K_UP = A0.K_UP
HIT_C = (1.6, 2.5)
HIT_F = (4.6, 7.6)
HOST_C, HOST_F = 1.4, 3.6
import phase272 as _P272  # noqa: E402
_P272.KAIJU.append('trivyrn')
SCALES = (('squall_scale', 'Squall Scale', '#ffe040', 'storm-yellow, crackling'), ('cinder_scale', 'Cinder Scale', '#ff7a2a', 'ember-orange, warm'),
          ('hush_scale', 'Hush Scale', '#d040c0', 'void-magenta, very quiet'))
PROOF = {'minecraft:damage_resistant': {'types': '#bm:p249_proof'}}

item(ITEM, TOTEM, 'The Triune Horn', COL,
     ['A horn it shed, in three colours.', 'Three voices argue in it, very faintly.',
      ('Use: call Trivyrn (again: call it over).', 'blue'), ('Sneak + use: its menu - Ride, Full Size, its wardrobe.', 'blue'),
      ('Riding it: use it to breathe - and it glides.', 'blue'), ('If it faints: 2 minutes before it can return.', 'gray')],
     model=f'bm:{ITEM}', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
for _iid, _nm, _c, _w in SCALES:
    item(_iid, TOTEM, _nm, _c, [f'A scale, {_w}.', ('Three, from three worlds, thrown into a lit portal together...', 'gray')],
         model='minecraft:prismarine_shard', stack=1, cat='magic', glint=True, comps=dict(hold('none'), **PROOF))
item('three_world_egg', TOTEM, 'Three-World Egg', '#a03050', ['Maroon, with three glowing seams: yellow, orange, magenta.',
                                                             ('Each world must crack its own seam.', 'gray')],
     model='minecraft:sniffer_egg', stack=1, cat='magic', glint=True, comps=dict(hold('none'), **PROOF))


class Trivyrn(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'trivyrn', 'Trivyrn', COL, LINE, 'p274', 'tw', 'tv'
    A = RF2.art(A0)
    MENU, PET_HP, PET_CD, ITEM = 6960, 56, 120, ITEM
    pron, they = 'it', 'it'
    FACE = dict(A0.FACE_MAP)
    ATTRS = dict(armor=10, attack_damage=6, movement_speed=0.33, follow_range=32, step_height=1.6)
    SCALE, HIT = HOST_C, HIT_C
    BOX_FIT = True
    BUTTONS = ((6, 'Ride', 'It stands up to its full size: climb on (sneak to get off). Off a height, it glides.', 'p274/ride'),
               (7, 'Full Size: on / off', 'On: the wyrm\'s own size, ~7.6 blocks (and its hitbox). Off: a companion\'s, ~2.45.', 'p274/csz/toggle'))
    CYCLE = W5.cycle(A0, (300, [(0, 'idle_a'), (100, 'idle_b'), (200, 'idle_c')]), (160, [(0, 'sit_a'), (80, 'sit_a')]), (None, [(0, 'happy'), (16, 'idle_a')]),
                     {7: (None, [(0, 'lash_0'), (8, 'lash_1'), (11, 'lash_2'), (14, 'lash_3'), (20, 'idle_a')]), 11: (None, [(0, 'gust_0'), (10, 'gust_1'), (18, 'idle_a')]),
                      8: (None, [(0, 'breath_0'), (14, 'breath_1'), (54, 'idle_a')])}, wp=24, rp_=12)
    DUR = dict(P235._DUR, lash_0=8, lash_1=3, lash_2=3, lash_3=3, gust_0=10, gust_1=3, breath_0=14, breath_1=4, sit_a=12, sit_b=20, happy=8,
               walk_0=6, walk_1=6, walk_2=6, walk_3=6, run_0=3, run_1=3, run_2=3, run_3=3)
    QUIPS = ['(Squall: "Follow ME." Cinder: "No, me." Hush: "...")', '(Cinder snaps at Squall\'s neck. Squall rears away, outraged.)', '(Hush looks at you, and glows a little)',
             '(three heads look three ways at once)', '(Squall: "We are magnificent." Cinder: "We are HUNGRY.")', '(Hush hangs upside down, because it can)']
    HELLO = ('(Trivyrn lopes back to you, three heads bobbing out of step)', '(a crack of thunder, a puff of fire, a hush - and Trivyrn lands beside you)',
             '(the three heads argue about which way home is - and it goes)')
    SIT = ('(Squall: "Up! Up!" Cinder: "...fine.")', '(it crouches low, three heads up, watching three ways)')
    FAINT = '(Squall: "...this is... Cinder\'s fault..." Hush: "...")'
    NOT_YOURS = '(three heads look at you. Cinder snarls. Squall sniffs. Hush stares.)'
    POWERS = [('The Lash', 'a foe within 7, every 6 s: three snake-strikes in turn - Cinder first, then Squall, then Hush - 8 each'),
              ('Wing Gust', 'two foes within 10, every 8 s: a cone of wind - knocked far back'),
              ('Tri-Breath', 'a foe 4-14 off, every 12 s: Squall\'s bolt (6, chaining), Cinder\'s fire (6, alight), Hush\'s void (4, lifted and let down)'),
              ('Ride', 'its menu: it stands up to its full size - climb on (sneak to get off); off a height, it glides'),
              ('Full Size', 'its menu: the wyrm\'s own size (~7.6 blocks) - or a companion\'s (~2.45); its hitbox with it'),
              ('The Kaiju Trio', 'the Atomic Rex, Talus and Trivyrn all out: allies within 16 Resistance I - and once a day the Triple Threat')]
    INTRO = [T('Trivyrn', COL, bold=True), T(' - the wanderer between the three worlds, one head of each. It thinks it should be in charge (well, Squall does). ', 'gray'),
             T('(Cinder: "Hi.")', LINE, italic=True)]
    BURST = ['particle minecraft:electric_spark ~ ~1.5 ~ 0.6 0.8 0.6 0.05 20', 'particle minecraft:flame ~ ~1.5 ~ 0.4 0.6 0.4 0.02 12', 'particle minecraft:portal ~ ~1.5 ~ 0.4 0.6 0.4 0.5 20']
    FADE_SOUND = 'playsound minecraft:entity.ender_dragon.flap neutral @a[distance=..20] ~ ~ ~ 1 0.8'
    SUMMON_EXTRA = ['playsound minecraft:entity.ender_dragon.growl neutral @a[distance=..24] ~ ~ ~ 0.5 1.2', 'playsound minecraft:entity.lightning_bolt.thunder neutral @a[distance=..24] ~ ~ ~ 0.3 1.6']
    ENC_POSES = [(0, 'idle_a'), (30, 'idle_b'), (60, 'happy')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:electric_spark ~ ~2 ~ 0.6 0.6 0.6 0.02 6'
    ADV = ('Three Minds, One Wyrm', 'Three scales from three worlds, a lit portal - and three cracks, one in each world')
    ADMIN_HINT = 'Three scales (Breeze, Ancient Debris / Basalt magma cube, Shulker) into a lit portal; the egg cracked in each world (admin/trivyrn_meet_here).'
    MEET_HINT = 'Right-click it.'


_DOLL = 'A doll of Trivyrn - three big heads (storm, fire and void) on a little maroon wyrm, its tail curled round.'
_eff = W5.pair_fx
_PAIRS = {
    'tw_bender': ('trivyrn', 'bender', 'Bark-Off', '#e0a860', 'Trivyrn and Bender - Cinder snarls, Bender woofs, and Hush licks him',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(WOOF.)'), ('trivyrn', '(Cinder snarls back. Hush licks Bender. Squall sighs.)')],
                  [('trivyrn', '(three heads sniff Bender at once)', 'bender', '(licks all three, very fast)')]),
    'tw_capshun': ('trivyrn', 'capshun', 'Three Hats', '#f0f0f0', 'Trivyrn and Mr. Capshun - he draws three hats, and the heads fight over the best one',
                   _eff(('luck', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "He drew three hats."]'), ('trivyrn', '(Squall: "MINE." Cinder: "MINE." Hush quietly takes the best one.)')],
                   [('trivyrn', '(Hush wears the little drawn crown)', 'capshun', '[Mr. Capshun narrates: "The other two never forgave it."]')]),
}
W5.register(Trivyrn, A0, _DOLL, ('minecraft:electric_spark', 'minecraft:entity.ender_dragon.growl', 'minecraft:poof'), _PAIRS, 'Trivyrn')
# (its doll: each head grown on its own neck - dolls_bake's per-head growth)
import phase141 as _P141  # noqa: E402
_dg = {}
for _p, _g in (M.DOLL_GROUPS or {}).items():
    if _g == 'head':
        _g = 'head:' + _p[-1] if _p[-1] in 'sch' and _p not in ('ufl', 'ufr') else _g
    _dg[f'bm:{A0.R.model_name(_p, {})}'] = _g
_df = _P141.DOLL_FROM['doll_trivyrn']
_P141.DOLL_FROM['doll_trivyrn'] = (_df[0], dict(_df[1], groups=_dg))

# ---- its Piercing Blow, on screen: LIGHTNING BREATH - all three rear back, wings flung open; the storm crackles over its scales tail
#      to heads, a part a tick (the Rex's charge language); then the braided streams, swaying, into the monster - and bolts on it
import phase226 as _P226  # noqa: E402
_CH = ('tail3', 'tail2', 'tail1', 'body', 'chest', 'n1s', 'n1c', 'n1h', 'n2s', 'n2c', 'n2h', 'hs', 'hc', 'hh')
_chg = lambda p: f'execute as @e[type=minecraft:item_display,tag=bm.twsel,tag=bm.twp_{p}] run data modify entity @s item.components."minecraft:item_model" set value "bm:tw_{p}_ch"'
_bolt = ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 30', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.5 0.3 0.05 10',
         'summon minecraft:lightning_bolt ~ ~ ~ {Tags:["bm.twbolt"]}']
_P226.ASSAULT['trivyrn'] = dict(pfx='p274', s_obj='bm.tvs', anim='p274/anim', busy='bm.tvx', end=78, dash=None, free=True,
                                hits={1: (2, ['particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20', 'particle minecraft:end_rod ~ ~1 ~ 0.3 0.4 0.3 0.05 6'],
                                          'minecraft:entity.lightning_bolt.impact', 1.4),
                                      2: (2, _bolt, 'minecraft:entity.lightning_bolt.thunder', 1.0)},
                                tl={1: ['P storm_0', 'S minecraft:entity.ender_dragon.growl 1 0.8'], **{2 + i: [_chg(p)] for i, p in enumerate(_CH)},
                                    20: ['P storm_1', 'H2'], 28: ['H1'], 30: ['P storm_2'], 36: ['H1'], 40: ['P storm_1', 'H2'], 44: ['H1'], 50: ['P storm_2'],
                                    52: ['H1'], 60: ['P storm_1', 'H2'], 76: ['P idle_a']})
_P226.NAMES['trivyrn'] = ('Lightning Breath', 'all three heads rear back and pour a braided, swaying storm of lightning into the monster')


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Trivyrn, G)


def _icon():
    from sprites280 import S
    s = S()
    pal = {'y': '#ffe040', 'o': '#ff7a2a', 'm': '#d040c0', 'w': '#f0e8d8', 'k': '#3a2a20'}
    s.g(['y...o...m.', 'yy..oo..mm', '.yy.oo.mm.', '..ywoowm..', '...wwww...', '...wkkw...', '....ww....'], pal, 3, 4)
    return s.render()


def rp(R):
    W5.rp(Trivyrn, R, _icon(), A0)


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.9, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..24] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=20, at=[12, 9, 6], cd=120, reach=7.0, go=[snd('entity.ender_dragon.flap', 0.6, 1.4)]),
             crowd=dict(st=11, x=18, at=8, cd=160, r=10, n=2, go=[snd('entity.breeze.wind_burst', 1.0, 0.7)]),
             ranged=dict(st=8, x=54, at=[40, 30, 20], cd=240, near=4, far=14, go=[snd('entity.ender_dragon.growl', 0.8, 1.2)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    for i, (tagx, fx) in enumerate((('cinder', 'particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.05 12'), ('squall', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.1 12'),
                                     ('hush', 'particle minecraft:portal ~ ~1 ~ 0.3 0.4 0.3 0.5 16'))):
        fn(f'{pfx}/melee{"" if i == 0 else i + 1}', X.hit(8) + [f'execute as @e[{foe},distance=..7.4,sort=nearest,limit=1] at @s run function bm:{pfx}/lashed_{tagx}'] + X.end)
        fn(f'{pfx}/lashed_{tagx}', [f'function bm:{pfx}/hurt', fx, snd('entity.player.attack.sweep', 0.6, 1.4)])
    fn(f'{pfx}/crowd', X.hit(3) + [f'execute positioned ^ ^ ^4 as @e[{foe},distance=..6] at @s facing entity @e[type=minecraft:wolf,tag=bm.twme,limit=1] feet run function bm:{pfx}/gusted',
                                   'particle minecraft:gust ^ ^1 ^3 1 0.5 1 0 6'] + X.end)
    fn(f'{pfx}/gusted', [f'function bm:{pfx}/hurt', 'tp @s ^ ^ ^-2', 'data modify entity @s Motion[1] set value 0.5d'])
    breaths = [('', 6, ['particle minecraft:electric_spark ~ ~1 ~ 0.3 0.5 0.3 0.2 20'], f'execute as @e[{foe},distance=..4,sort=nearest,limit=2] run function bm:{pfx}/hurt'),
               ('2', 6, ['particle minecraft:flame ~ ~1 ~ 0.4 0.5 0.4 0.05 20'], 'data merge entity @s {Fire:100s}'),
               ('3', 4, ['particle minecraft:portal ~ ~1 ~ 0.4 0.5 0.4 0.5 30'], 'effect give @s minecraft:levitation 1 1')]
    for sfx, d, fx, rider in breaths:
        fn(f'{pfx}/ranged{sfx}', X.hit(d) + [f'execute as @e[{foe},distance=..14.5,sort=nearest,limit=1] at @s run function bm:{pfx}/breathed{sfx}'] + X.end)
        fn(f'{pfx}/breathed{sfx}', [f'function bm:{pfx}/hurt', rider] + fx + ([] if sfx != '3' else ['effect give @s minecraft:slow_falling 4 0']))
    X.second.append('tag @e[type=minecraft:wolf,tag=bm.twpet] add bm.kaiju')
    return lines


def _encounter(G, X):
    """THREE SCALES (once your Rex is met) - THE PORTAL - THREE CRACKS, one in each world: the last hatches it"""
    fn, tellraw, title = G.fn, G.tellraw, G.title
    csay = lambda txt: title('@s', 'actionbar', [T('Trivyrn: ', COL, bold=True), T(txt, LINE)])
    G.wjson('bm/predicate/p274/peak.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': ['minecraft:jagged_peaks', 'minecraft:frozen_peaks', 'minecraft:stony_peaks']}})
    G.wjson('bm/predicate/p274/basalt.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': 'minecraft:basalt_deltas'}})
    G.wjson('bm/predicate/p274/thunder.json', {'condition': 'minecraft:weather_check', 'thundering': True})
    # (the scales: a kill of a Breeze / a Basalt Delta magma cube / a shulker, or Ancient Debris mined - once your Rex is met)
    for kind, nm, iid, n, extra in (('breeze', 'squall', 'squall_scale', 40, {}), ('magma_cube', 'cinder', 'cinder_scale', 40, {'minecraft:location': {'biomes': 'minecraft:basalt_deltas'}}),
                                    ('shulker', 'hush', 'hush_scale', 30, {})):
        G.wjson(f'bm/advancement/p274/kill_{nm}.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {
            'entity': [{'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': dict({'minecraft:entity_type': f'minecraft:{kind}'}, **extra)}]}}},
            'rewards': {'function': f'bm:p274/enc/kill_{nm}'}})
        fn(f'p274/enc/kill_{nm}', [f'advancement revoke @s only bm:p274/kill_{nm}', 'execute unless entity @s[tag=bm.rymet] run return 0',
                                   f'execute store result score #r bm.rng run random value 1..{n}', 'execute unless score #r bm.rng matches 1 run return 0',
                                   f'loot give @s loot bm:items/{iid}', 'playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 1 0.6',
                                   title('@s', 'actionbar', T(f'(it sheds a scale - {nm} - and it hums in your hand)', COL))])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.tvad minecraft.mined:minecraft.ancient_debris', 'scoreboard objectives add bm.tvad0 dummy',
                              'scoreboard objectives add bm.tvh dummy']
    G.OBJECTIVES += ['bm.tvad', 'bm.tvad0', 'bm.tvh']
    X.second.append('execute as @a[tag=bm.rymet] unless score @s bm.tvad = @s bm.tvad0 run function bm:p274/enc/debris')
    fn('p274/enc/debris', ['scoreboard players operation @s bm.tvad0 = @s bm.tvad', 'execute store result score #r bm.rng run random value 1..300',
                           'execute if score #r bm.rng matches 1 run loot give @s loot bm:items/cinder_scale'])
    # (the portal: all three scales thrown into a lit Nether portal together - the Three-World Egg)
    # (3.0s: checked EVERY TICK. 26.3 moves a dropped item through a portal in its own tick, the moment it touches one - before the
    #  pack's tick could see it there - so a PortalCooldown set once it was IN the portal came too late (batch 5's check: the scales
    #  rode it). Now each new item is looked at once (bm.twchk); a scale or the egg (bm.twhold) keeps a PortalCooldown from then on,
    #  wherever it is, so it never rides a portal - it lies in it until all three are in and fuse)
    G.FUNCS['tick'] += ['execute as @e[type=minecraft:item,tag=!bm.twchk] run function bm:p274/enc/look',
                        'execute as @e[type=minecraft:item,tag=bm.twhold] at @s run function bm:p274/enc/hold']
    fn('p274/enc/look', ['tag @s add bm.twchk'] + [f'execute if items entity @s contents *[minecraft:custom_data~{{bm:"{k}"}}] run tag @s add bm.twhold'
                                                   for k in ('squall_scale', 'cinder_scale', 'hush_scale', 'three_world_egg')])
    fn('p274/enc/hold', ['data modify entity @s PortalCooldown set value 40',
                         'execute if items entity @s contents *[minecraft:custom_data~{bm:"squall_scale"}] run function bm:p274/enc/inportal'])
    # (a held item is nudged to the portal block's edge - so the squall scale's own block, or one a step to any side, will do)
    fn('p274/enc/inportal', [f'execute positioned ~{dx} ~ ~{dz} if block ~ ~ ~ minecraft:nether_portal run return run function bm:p274/enc/portal'
                             for dx, dz in (('', ''), ('0.4', ''), ('-0.4', ''), ('', '0.4'), ('', '-0.4'))])
    fn('p274/enc/portal', ['scoreboard players set #n bm.rng 0',
                           'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents *[minecraft:custom_data~{bm:"cinder_scale"}] run scoreboard players add #n bm.rng 1',
                           'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents *[minecraft:custom_data~{bm:"hush_scale"}] run scoreboard players add #n bm.rng 10',
                           'execute unless score #n bm.rng matches 11.. run return 0',
                           'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents *[minecraft:custom_data~{bm:"cinder_scale"}] run kill @s',
                           'execute as @e[type=minecraft:item,distance=..2.5] if items entity @s contents *[minecraft:custom_data~{bm:"hush_scale"}] run kill @s',
                           'kill @s', 'loot spawn ~ ~0.5 ~ loot bm:items/three_world_egg',
                           # (held at once: a new item in a portal rides it in its own first tick, before the next look)
                           'execute as @e[type=minecraft:item,tag=!bm.twchk,distance=..3] run function bm:p274/enc/look',
                           'execute as @e[type=minecraft:item,tag=bm.twhold,distance=..3] run data modify entity @s PortalCooldown set value 40', 'playsound minecraft:block.portal.trigger ambient @a[distance=..16] ~ ~ ~ 1 1.6',
                           'particle minecraft:portal ~ ~1 ~ 0.6 1 0.6 1 120', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 20',
                           tellraw('@a[distance=..12]', [T('The three scales are drawn between the worlds - and fuse into an egg, ', LINE, italic=True),
                                                         T('maroon, three seams glowing.', 'gray', italic=True)])])
    # (three cracks: the egg, dropped - its thrower's seams; the last one hatches it there)
    X.second.append('execute as @e[type=minecraft:item] if items entity @s contents *[minecraft:custom_data~{bm:"three_world_egg"}] at @s run function bm:p274/enc/egg')
    fn('p274/enc/egg', ['tag @a remove bm.tvthr', 'execute on origin run tag @s add bm.tvthr',
                        'execute unless entity @a[tag=bm.tvthr] run return 0',
                        'execute if dimension minecraft:overworld if entity @s[y=150,dy=300] if predicate bm:p274/peak if predicate bm:p274/thunder as @a[tag=bm.tvthr,limit=1] unless entity @s[tag=bm.tvc1] at @s run function bm:p274/enc/crack1',
                        'execute if dimension minecraft:the_nether if block ~ ~-0.5 ~ minecraft:magma_block if predicate bm:p274/basalt as @a[tag=bm.tvthr,limit=1] unless entity @s[tag=bm.tvc2] at @s run function bm:p274/enc/crack2',
                        'execute if dimension minecraft:the_end if block ~ ~-0.5 ~ minecraft:end_stone unless entity @s[x=-1000,z=-1000,dx=2000,dy=400,y=-64,dz=2000] as @a[tag=bm.tvthr,limit=1] unless entity @s[tag=bm.tvc3] at @s run function bm:p274/enc/crack3',
                        'execute as @a[tag=bm.tvthr,tag=bm.tvc1,tag=bm.tvc2,tag=bm.tvc3,tag=!bm.twmet] at @s run function bm:p274/enc/hatch', 'tag @a remove bm.tvthr'])
    for i, (who, line) in enumerate((('Squall', '(a bolt! Squall\'s head pokes out of its seam, yawns - and complains about the weather)'),
                                     ('Cinder', '(Cinder bites its way out of its seam, chewing)'), ('Hush', '(Hush opens one eye in its seam)')), 1):
        fn(f'p274/enc/crack{i}', [f'tag @s add bm.tvc{i}', 'playsound minecraft:block.sniffer_egg.crack ambient @a[distance=..24] ~ ~ ~ 1 0.6'] +
           (['execute at @s run summon minecraft:lightning_bolt ~ ~ ~ {Tags:["bm.twbolt"]}'] if i == 1 else []) +
           [tellraw('@s', [T(f'{who}: ', COL, bold=True), T(line, LINE)]),
            title('@s', 'actionbar', T('(a seam cracks)', 'gray'))])
    fn('p274/enc/hatch', ['execute as @e[type=minecraft:item,distance=..64] if items entity @s contents *[minecraft:custom_data~{bm:"three_world_egg"}] run kill @s',
                          'scoreboard players operation #me bm.pid = @s bm.pid',
                          'execute at @s rotated ~ 0 positioned ^ ^ ^4 run function bm:p274/enc/spawn',
                          'execute at @s run scoreboard players operation @e[type=minecraft:interaction,tag=bm.twenc,distance=..8] bm.pid = #me bm.pid',
                          'playsound minecraft:entity.ender_dragon.growl ambient @a[distance=..48] ~ ~ ~ 1.2 1.2',
                          tellraw('@s', [T('The egg bursts. ', LINE, bold=True), T('A hatchling unfolds - and grows, and grows - into TRIVYRN. Three heads argue about who gets to say hello.', 'gray', italic=True)])])
    fn('p274/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return run ' + csay('(three heads look at you. Cinder snarls.)'),
                         tellraw('@s', [T('The three heads fight over who gives you the horn. ', LINE, italic=True), T('Cinder wins.', 'gray', italic=True)]), 'function bm:p274/enc/joined'])
    fn('admin/trivyrn_meet_here', ['execute rotated ~ 0 positioned ^ ^ ^4 run function bm:p274/enc/spawn',
                                   'scoreboard players operation @e[type=minecraft:interaction,tag=bm.twenc,distance=..8] bm.pid = @s bm.pid'])
    fn('admin/trivyrn_kit', ['loot give @s loot bm:items/squall_scale', 'loot give @s loot bm:items/cinder_scale', 'loot give @s loot bm:items/hush_scale'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:lightning_bolt,tag=bm.twbolt]']


def generate(G):
    fn, title, tellraw = G.fn, G.title, G.tellraw
    say = lambda txt: title('@s', 'actionbar', [T('Trivyrn: ', COL, bold=True), T(txt, LINE)])
    frame = dict(models=[], click=['particle minecraft:electric_spark ~ ~0.2 ~ 0.1 0.1 0.1 0.05 4', 'particle minecraft:flame ~ ~0.2 ~ 0.1 0.1 0.1 0.01 3',
                                   'particle minecraft:portal ~ ~0.2 ~ 0.1 0.1 0.1 0.2 6', 'playsound minecraft:entity.ender_dragon.ambient block @a[distance=..12] ~ ~ ~ 0.3 1.8'])
    W5.build(Trivyrn, G, _abilities, _encounter, sitb=(160, [(0, 'sit_b'), (80, 'sit_b')]), frame=frame)
    pfx = Trivyrn.pfx
    W5.poses_for(Trivyrn, G, ['storm_0', 'storm_1', 'storm_2'])             # (its Piercing Blow's: in no cycle)
    import compsize as CSZ
    CSZ.build(G, pfx, 'bm.tvcs', 'bm.tvcz', f'bm.{Trivyrn.q}s', HOST_C, HOST_F,
              say('(Squall: "TALLER." - Full Size: on)'), say('(Cinder: "...smaller. Fine." - Full Size: off)'), hit=('bm.twhit', HIT_C, HIT_F))
    CSZ.LATE.append((pfx, K_UP, 'bm.tvcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    T_[1:1] = CSZ.sync(pfx, 'bm.tvcs', 'bm.tvcz', f'bm.{Trivyrn.q}s', HOST_C, HOST_F)
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag=bm.tvcz] run function bm:{pfx}/box/full'])
    fn(f'{pfx}/box/full', CSZ.resize('bm.twhit', *HIT_F))
    # ---- RIDE (kaiju_ride; level: the tri-breath, down: the wing gust, up: all three at once; it glides)
    ride = KR.build(G, dict(key='tw', pfx=pfx, art=M.R, scale=M.R.RIG_SCALE, seat=(4.83, 0.60), hp=180, walk=0.32, run=0.46, name='Trivyrn', col=COL, glide=True,
                            poses=dict(sit='sit_a', idle='ride', walk=['walk_0', 'walk_1', 'walk_2', 'walk_3'], run=['run_0', 'run_1', 'run_2', 'run_3']),
                            moves=dict(level=('p274/rmv/breath', 6), down=('p274/rmv/gust', 8), up=('p274/rmv/tri', 12)), follower_back=f'{pfx}/try_summon'))
    foe = 'type=#bm:hostile,tag=!bm.npc'
    fn('p274/rmv/breath', [f'execute positioned ^ ^4 ^6 as @e[{foe},distance=..9,sort=nearest,limit=1] at @s run function bm:p274/rmv/hit {{d:8}}',
                           'particle minecraft:electric_spark ^ ^5 ^6 0.6 0.6 0.6 0.2 40', 'playsound minecraft:entity.lightning_bolt.impact neutral @a[distance=..32] ~ ~ ~ 1 1.4'])
    fn('p274/rmv/gust', [f'execute as @e[{foe},distance=..8] at @s run function bm:p274/rmv/hit {{d:4}}', 'particle minecraft:gust ~ ~1 ~ 3 0.5 3 0 12',
                         'playsound minecraft:entity.breeze.wind_burst neutral @a[distance=..32] ~ ~ ~ 1.2 0.7'])
    fn('p274/rmv/tri', [f'execute positioned ^ ^4 ^6 as @e[{foe},distance=..10] at @s run function bm:p274/rmv/hit {{d:8}}', 'particle minecraft:flame ^ ^5 ^6 1 1 1 0.05 40',
                        'particle minecraft:portal ^ ^5 ^6 1 1 1 0.5 60', 'particle minecraft:electric_spark ^ ^5 ^6 1 1 1 0.2 40',
                        'playsound minecraft:entity.ender_dragon.growl neutral @a[distance=..32] ~ ~ ~ 1.2 1.0'])
    fn('p274/rmv/hit', ['$damage @s $(d) minecraft:mob_attack', 'data modify entity @s Motion[1] set value 0.3d'])
    fn('p274/ride', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #on bm.rng 0',
                     'execute as @e[type=minecraft:wolf,tag=bm.twpet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run scoreboard players set #on bm.rng 1',
                     'execute if score #on bm.rng matches 0 run return run ' + say('(call it first - then ride it)'),
                     'execute if function bm:p20/frog/has_vehicle run return run ' + say('(get down first)'),
                     'execute as @e[type=minecraft:wolf,tag=bm.twpet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run tag @s add bm.twsel2', f'function bm:{pfx}/dismiss',
                     f'function bm:{ride["ride"]}'])
    G.FUNCS[f'{pfx}/use'].insert(0, f'execute if function bm:{ride["riding"]} run return run function bm:{ride["use"]}')
    # ---- THE KAIJU TRIO (the Rex, Talus and Trivyrn all out, an owner's): allies within 16 Resistance I - "Three Titans";
    #      once a day, the TRIPLE THREAT: all three Piercing Blows on the nearest monster, one after the other
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.tvday dummy', 'scoreboard objectives add bm.tvtt dummy']
    G.OBJECTIVES += ['bm.tvday', 'bm.tvtt']
    G.wjson('bm/advancement/story/kaiju_trio.json', {'parent': 'bm:story/root', 'criteria': {'t': {'trigger': 'minecraft:impossible'}},
                                                     'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': f'bm:{ITEM}'}},
                                                                 'title': T('The Kaiju Trio', COL), 'description': T('The Atomic Rex, Talus and Trivyrn - all three, the Triple Threat', 'gray'),
                                                                 'frame': 'challenge', 'hidden': True}})
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.rymet,tag=bm.tlmet,tag=bm.twmet] at @s run function bm:p274/trio')
    mine = lambda t: f'@e[type=minecraft:wolf,tag={t},tag=!bm.ffpet,distance=..24]'
    fn('p274/trio', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #n bm.rng 0'] +
       [f'execute as {mine(t)} if score @s bm.pid = #me bm.pid run scoreboard players add #n bm.rng 1' for t in ('bm.rypet', 'bm.tlpet', 'bm.twpet')] +
       ['execute unless score #n bm.rng matches 3 run return 0',
        'effect give @a[distance=..16,gamemode=!spectator] minecraft:resistance 3 0 true',
        'execute unless entity @s[tag=bm.tvbond] run function bm:p274/trio_on',
        'execute if score @s bm.tvday = #day bm.bm run return 0',
        'execute unless entity @e[type=#bm:hostile,tag=!bm.npc,distance=..12] run return 0',
        'function bm:p274/triple'])
    fn('p274/trio_on', ['tag @s add bm.tvbond', tellraw('@s', [T('Three Titans', COL, bold=True), T(' - the Atomic Rex, Talus and Trivyrn, side by side. (Allies near them: Resistance.)', 'gray')])])
    G.FUNCS['loop/second'].append('execute as @a[tag=bm.tvbond] at @s run function bm:p274/trio_q')
    fn('p274/trio_q', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #n bm.rng 0'] +
       [f'execute as {mine(t)} if score @s bm.pid = #me bm.pid run scoreboard players add #n bm.rng 1' for t in ('bm.rypet', 'bm.tlpet', 'bm.twpet')] +
       ['execute unless score #n bm.rng matches 3 run tag @s remove bm.tvbond'])
    fn('p274/triple', ['scoreboard players operation @s bm.tvday = #day bm.bm', 'advancement grant @s only bm:story/kaiju_trio',
                       'tag @e[type=#bm:hostile,tag=!bm.npc,distance=..12,sort=nearest,limit=1] add bm.prfoe',
                       'execute as @e[type=minecraft:wolf,tag=bm.rypet,tag=!bm.ffpet,distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.prgo 1',
                       'scoreboard players set @s bm.tvtt 1',
                       title('@s', 'title', T('TRIPLE THREAT', COL, bold=True)), title('@s', 'subtitle', T('the beam - the flurry - the storm', 'gray', italic=True))])
    # (the flurry 2 s after the beam, the storm 2 s after that)
    G.FUNCS['loop/second'].append('execute as @a[scores={bm.tvtt=1..}] at @s run function bm:p274/triple_s')
    fn('p274/triple_s', ['scoreboard players add @s bm.tvtt 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         'execute if score @s bm.tvtt matches 3 unless entity @e[tag=bm.prfoe] run tag @e[type=#bm:hostile,tag=!bm.npc,distance=..14,sort=nearest,limit=1] add bm.prfoe',
                         'execute if score @s bm.tvtt matches 3 as @e[type=minecraft:wolf,tag=bm.tlpet,tag=!bm.ffpet,distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.prgo 1',
                         'execute if score @s bm.tvtt matches 5 unless entity @e[tag=bm.prfoe] run tag @e[type=#bm:hostile,tag=!bm.npc,distance=..14,sort=nearest,limit=1] add bm.prfoe',
                         'execute if score @s bm.tvtt matches 5 as @e[type=minecraft:wolf,tag=bm.twpet,tag=!bm.ffpet,distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set @s bm.prgo 1',
                         'execute if score @s bm.tvtt matches 6.. run scoreboard players reset @s bm.tvtt'])
    fn('admin/trivyrn_reset', ['tag @s remove bm.twmet', 'tag @s remove bm.tvc1', 'tag @s remove bm.tvc2', 'tag @s remove bm.tvc3', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                               title('@s', 'actionbar', T('Trivyrn has not met you yet.', COL))])
