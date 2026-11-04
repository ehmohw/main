"""3.1: THE ATOMIC REX - the 61st follower (rex_art.py; fol5flag.REX). The hidden mount (phase249) made a follower: the nuclear dinosaur,
charcoal hide and three rows of glowing blue dorsal plates - at a companion's size by default (~2.5 blocks), and the kaiju's own
(~7.5) at the press of its menu's Full Size. It still carries you: its menu's RIDE.

MEETING IT    as before (phase249): a Rex Fossil from deep deepslate, struck by lightning on a rod in a storm, the egg dropped in the
              Nether's lava - it hatches, and thinks you are its mother. The Atomic Whistle is now its summoning item: it follows you.
RIDING        its menu's Ride: it stands up to its full size (phase249's mount: the saddle, WASD, jump, sprint; the whistle while you
              ride - level / up: ATOMIC BREATH, down: STOMP, up past 60: ROAR); sneak to get off, and it's your follower again.
THE MECHA     no longer a mount of its own: a COSTUME in its wardrobe (look 1) - the war machine, every part swapped for the Mecha's.
              Earned as before, in the Armada's hidden hangar (three blueprints and the core) - but the dormant Mecha needs a pilot: a
              rex you've hatched. Ridden in the costume, it is the Mecha Rex (laser breath, rocket fist). The old Mecha Rex Remote
              calls your Rex in it.
ITS WAYS      TAIL SWIPE (a foe within 3, every 3 s: 6, knocked back); STOMP (two foes within 3, every 8 s: a shockwave, 5 to all,
              knocked up); ATOMIC BREATH (a foe 3-10 off, every 12 s: the plates light, a beam of blue fire - three blasts of 3, set
              alight); ROAR (charged, every 30 s: every monster within 8 slowed and weakened 5 s). Its Piercing Blow: the ATOMIC BEAM,
              super-charged, on screen (its spines light tail to head, the chest glows, a hum - then a thick sustained beam).
EVERYTHING ELSE is every follower's: sitting (right-click; sneak + right-click), a wardrobe (the Mecha, Ember, Glacier, the metals),
a rare aura (Meltdown), a shiny (Bone White), the Partner Wheel (no longer the Mounts page), a frame (it climbs out; a right-click:
a roar), a display case, Cecil's doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia. A KAIJU (bm.kaiju,
KAIJU): Talus and Trivyrn join it for the trio bond.
MIGRATION     a rex hatched before this - or a Mecha built - is a follower met (and the Mecha's costume earned); a rex kept on the old
              Mounts page comes back off it (its whistle or remote returned)."""
from items import T, ITEMS
from useitem import HOLD
import fol5
import fol5art
import fol5wire as W5
import rigpet as RP
import rigface as RF2
import phase235 as P235
import shiny as SH
import phase249  # noqa: F401  (its mount: the whistle, the models, the riding - this follower is built on it)

S5 = fol5.SPEC['rex']
A0 = fol5art.get('rex')
RX = A0.R
COL, LINE = S5['COL'], S5['LINE']
ITEM = S5['item']
MECHA = 1                                       # (the costume: its wardrobe's look 1 - handmade; earned in the hangar, never sold)
KAIJU = ['rex']                                 # (the kaiju: Talus and Trivyrn append themselves - their trio bond reads it)
K_UP = A0.K_UP
HIT_C = (1.4, 2.6)                              # (its click box, companion: its body and head - the tail sweeps outside it)
HIT_F = (3.6, 7.6)                              # (and at its full size)
HOST_C, HOST_F = 1.4, 3.6                       # (its host's scale: companion, full)
SH.UNSOLD.add(f'cos_rex_{MECHA}')
HOLD['mecha_remote'] = 'bm:p272/remote'          # (the old Mecha Rex Remote: your rex, called in its Mecha costume)
_L = ITEMS[ITEM]['comps'].get('minecraft:lore')
if isinstance(_L, list):
    _L[:] = [T('A whistle of fossil bone. Somewhere, something big hears it.', 'gray'), T('Use: call the Atomic Rex (again: call it over).', 'blue'),
             T('Sneak + use: its menu - Ride, Full Size, its wardrobe.', 'blue'), T('Riding it: use it to breathe atomic fire.', 'blue'),
             T('It answers to you alone.', 'dark_gray')]

P = A0.POSES
P['sit2'] = dict(P['sit'], head=RX.T(-10, 18, 0) if hasattr(RX, 'T') else P['sit'].get('head'))
P['happy'] = dict(P['roar'])


class Rex(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'rex', 'The Atomic Rex', COL, LINE, 'p272', 'ry', 'rq'
    A = A0
    MENU, PET_HP, PET_CD, ITEM = 5100, 60, 120, ITEM
    pron, they = 'it', 'it'
    SWAP = tuple(RX.PLATED)                     # (its plates: lit in the breath poses - the charged models)
    SWAP_START = False
    ATTRS = dict(armor=10, attack_damage=6, movement_speed=0.32, follow_range=32, step_height=1.6)
    SCALE, HIT = HOST_C, HIT_C
    BOX_FIT = True
    BUTTONS = ((6, 'Ride', 'It stands up to its full size and kneels for you: ride it (sneak to get off).', 'p272/ride'),
               (7, 'Full Size: on / off', 'On: the kaiju\'s own size, ~7.5 blocks (and its hitbox). Off: a companion\'s, ~2.5.', 'p272/csz/toggle'))
    CYCLE = W5.cycle(A0, (240, [(0, 'idle_a'), (120, 'idle_b')]), (120, [(0, 'sit'), (60, 'sit2')]), (None, [(0, 'happy'), (16, 'idle_a')]),
                     {7: (None, [(0, 'tailswipe'), (8, 'idle_a')]), 11: (None, [(0, 'stomp_0'), (8, 'stomp_1'), (12, 'idle_a')]),
                      8: (None, [(0, 'breath_0'), (10, 'breath_1'), (28, 'idle_a')]), 12: (None, [(0, 'roar'), (16, 'idle_a')])}, wp=16, rp_=10)
    DUR = dict(P235._DUR, sit=10, sit2=30, idle_a=20, idle_b=20, roar=6, breath_0=10, breath_1=4, stomp_0=8, stomp_1=3, tailswipe=6,
               walk_0=4, walk_1=4, walk_2=4, walk_3=4, run_0=3, run_1=3, run_2=3, run_3=3)
    QUIPS = ['(a rumble from deep in its chest - happy)', '(its dorsal plates flicker blue, one row at a time)', '(it sniffs you, very gently, with a nose the size of a door)',
             '(it tries to sit on your lap. It is too big. It tries anyway.)', '(it stomps. The ground remembers.)', '(a low hoot - its mother is near)']
    HELLO = ('(the Atomic Rex stomps back to you, plates glowing)', '(the ground shakes - and the Atomic Rex comes thundering up, and nuzzles you)',
             '(it rumbles goodbye, and lumbers off home)')
    SIT = ('"(RAWR - up it gets)"', '(it settles down on its haunches, tail curled round)')
    FAINT = '(a long, low groan - its plates go dark)'
    NOT_YOURS = '(it lowers its head and growls: you are not its mother)'
    POWERS = [('Tail Swipe', 'a foe within 3, every 3 s: its tail sweeps round - 6, and knocked back'),
              ('Stomp', 'two foes within 3, every 8 s: it rears and slams - a shockwave, 5 to all, knocked up'),
              ('Atomic Breath', 'a foe 3-10 off, every 12 s: its plates light tail to neck - three blasts of blue fire, 3 each, set alight'),
              ('Roar', 'charged, every 30 s: every monster within 8 slowed and weakened for 5 s'),
              ('Ride', 'its menu: it stands up to its full size and kneels for you - ride it (sneak to get off)'),
              ('Full Size', 'its menu: the kaiju\'s own size (~7.5 blocks) - or a companion\'s (~2.5); its hitbox with it')]
    INTRO = [T('The Atomic Rex', COL, bold=True), T(' - hatched in the Nether\'s lava from a fossil struck by lightning. It thinks you are its mother. ', 'gray'),
             T('(RAWR.)', LINE, italic=True)]
    BURST = ['particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 1.0 0.6 0.03 30', 'particle minecraft:end_rod ~ ~1.5 ~ 0.5 0.8 0.5 0.03 12']
    FADE_SOUND = 'playsound minecraft:entity.ravager.ambient neutral @a[distance=..20] ~ ~ ~ 1 0.6'
    SUMMON_EXTRA = ['playsound minecraft:entity.ravager.roar neutral @a[distance=..24] ~ ~ ~ 0.6 0.9', 'playsound minecraft:entity.warden.heartbeat neutral @a[distance=..24] ~ ~ ~ 1 0.8']
    ENC_POSES = [(0, 'idle_a'), (40, 'idle_b')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 30 run particle minecraft:soul_fire_flame ~ ~1.5 ~ 0.4 0.4 0.4 0.01 4'
    ADV = ('Its Mother', 'Hatch the Atomic Rex - and keep it')
    ADMIN_HINT = 'A Rex Fossil (deepslate), struck by lightning on a rod in a storm, the egg into the Nether\'s lava (admin/rex/kit).'
    MEET_HINT = 'Hatch it.'


_DOLL = 'A doll of the Atomic Rex - a little charcoal dinosaur, three rows of glowing blue plates down its back.'
_eff = W5.pair_fx
_PAIRS = {
    'ry_bender': ('rex', 'bender', 'Fetch, But Bigger', '#e0a860', 'The Atomic Rex and Bender - Bender brings it a stick; it brings Bender a tree',
                  _eff(('speed', 0), ('strength', 0)),
                  [('bender', '(drops a stick at its feet. Waits.)'), ('rex', '(it drops a whole tree at Bender\'s feet. Waits.)')],
                  [('rex', '(it lowers its head for Bender to sniff)', 'bender', '(licks its nose. It goes cross-eyed.)')]),
    'ry_capshun': ('rex', 'capshun', 'Monster Movie', '#f0f0f0', 'The Atomic Rex and Mr. Capshun - he narrates it like a monster movie, and it plays along',
                   _eff(('strength', 0), ('resistance', 0)),
                   [('capshun', '[Mr. Capshun narrates: "THE CITY TREMBLED."]'), ('rex', '(it roars, very dramatically, on cue)')],
                   [('rex', '(it stomps, slowly, for the camera)', 'capshun', '[Mr. Capshun narrates: "Nobody was harmed in the making of this picture."]')]),
}
W5.register(Rex, A0, _DOLL, ('minecraft:soul_fire_flame', 'minecraft:entity.ravager.roar', 'minecraft:poof'), _PAIRS, 'the Atomic Rex')
import phase138 as _P138  # noqa: E402
_P138.HANDMADE.add(('rex', MECHA))              # (phase138 makes no recolour of it: _mecha writes its item definitions - the Mecha's own models)

# ---- its Piercing Blow, on screen: THE ATOMIC BEAM, super-charged - it braces where it stands, its plates light tail to head (the
#      mount's own charge, part by part), the chest glows, a rising hum - then a thick sustained beam of blue fire into the monster
import phase226 as _P226  # noqa: E402
_beam = [f'execute facing entity @e[type=minecraft:wolf,tag=bm.rypet,sort=nearest,limit=1] eyes run particle minecraft:soul_fire_flame ^ ^1 ^{d} 0.12 0.12 0.12 0.01 3' for d in range(0, 9)]
_lit = lambda p: f'execute as @e[type=minecraft:item_display,tag=bm.rysel,tag=bm.ryp_{p}] run data modify entity @s item.components."minecraft:item_model" set value "bm:rx_atomic_{p}_charged"'
_P226.ASSAULT['rex'] = dict(pfx='p272', s_obj='bm.rqs', anim='p272/anim', busy='bm.rqx', end=40, dash=None, free=True,
                            hits={1: (2, _beam + ['particle minecraft:end_rod ~ ~1 ~ 0.3 0.3 0.3 0.05 6', 'data merge entity @s {Fire:60s}'], 'minecraft:entity.blaze.shoot', 0.5),
                                  2: (4, _beam + ['particle minecraft:flash{color:[0.45,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:explosion ~ ~1 ~ 0 0 0 0 1',
                                                  'particle minecraft:soul_fire_flame ~ ~1 ~ 0.6 0.6 0.6 0.1 40'], 'minecraft:entity.warden.sonic_boom', 1.0)},
                            tl={1: ['P breath_0', 'S minecraft:block.beacon.power_select 1 0.5'], **{2 + i: [_lit(p)] for i, p in enumerate(RX.CHARGE_ORDER)},
                                9: ['S minecraft:block.beacon.ambient 1 1.6', 'particle minecraft:soul_fire_flame ~ ~1.2 ~ 0.5 0.5 0.5 0.01 20'],
                                12: ['S minecraft:block.respawn_anchor.charge 1 0.6'], 16: ['P breath_1', 'H1'], 19: ['H1'], 22: ['H1'], 25: ['H1'], 28: ['H1'],
                                31: ['H2'], 36: ['P idle_a']})
_P226.NAMES['rex'] = ('Atomic Beam', 'braces, lights its plates tail to head and pours a thick, sustained beam of blue fire into the monster')


def extend_offers(O, offer):
    pass


def generate_early(G):
    RP.contract(Rex, G)


def _icon():
    from sprites280 import S
    s = S()
    pal = {'w': '#e8e0d0', 'g': '#a89880', 'b': '#5ac8ff', 'k': '#2a2420'}
    s.g(['....bb....', '...bwwb...', '...wggw...', '...wggw...', '...wkkw...', '...wggw...', '...wggw...', '..wwggww..', '...wwww...'], pal, 3, 3)
    return s.render()


def rp(R):
    R.TEXTURE_MODS.append(A0)                  # (its models and its whistle's icon are phase249's; its looks recolour its textures)

    def late(R2):
        R2.POST.append(_mecha)
    R.POST.append(late)


def _mecha(R2):
    """THE MECHA costume: every item definition of the Atomic Rex's models, look MECHA's, wears the Mecha Rex's model of that part"""
    import os, re, json, glob
    idir = R2.p('assets', 'bm', 'items')
    n = 0
    for f in sorted(glob.glob(os.path.join(idir, 'rx_atomic_*.json'))):
        nm = os.path.basename(f)[:-5]
        if re.search(r'_c\d+$', nm):
            continue
        R2.wj(f'assets/bm/items/{nm}_c{MECHA}.json', {'model': {'type': 'minecraft:model', 'model': 'bm:item/' + nm.replace('rx_atomic_', 'rx_mecha_', 1)}})
        n += 1
    assert n >= len(RX.PARTS), n


def textures():
    return A0.textures()


# ---------------------------------------------------------------------------------------------------- its ways
def _abilities(G, X):
    fn, pfx, foe, S = G.fn, X.pfx, X.foe, X.S
    snd = lambda s, v=0.8, p=1.0: f'playsound minecraft:{s} neutral @a[distance=..24] ~ ~ ~ {v} {p}'
    K = dict(melee=dict(st=7, x=10, at=5, cd=60, reach=3.0, go=[snd('entity.player.attack.sweep', 0.8, 0.5)]),
             crowd=dict(st=11, x=14, at=6, cd=160, r=3.0, n=2, go=[snd('entity.ravager.step', 1.0, 0.6)]),
             ranged=dict(st=8, x=30, at=[18, 13, 8], cd=240, near=3, far=10, go=[snd('block.beacon.power_select', 0.8, 0.6)]),
             charged=dict(st=12, x=20, at=12, cd=600, r=8, go=[snd('entity.ravager.roar', 1.2, 0.7)]))
    lines = P235.kit(G, X, K)
    G.FUNCS.pop(f'{pfx}/near_owner', None)
    fn(f'{pfx}/melee', X.hit(6) + [f'execute as @e[{foe},distance=..3.4,sort=nearest,limit=1] at @s run function bm:{pfx}/swiped'] + X.end)
    fn(f'{pfx}/swiped', [f'function bm:{pfx}/hurt', 'particle minecraft:sweep_attack ~ ~1 ~ 0.3 0.2 0.3 0 2', 'data modify entity @s Motion[1] set value 0.3d'])
    fn(f'{pfx}/crowd', X.hit(5) + [f'execute as @e[{foe},distance=..3.2] at @s run function bm:{pfx}/stomped', 'particle minecraft:explosion ~ ~0.2 ~ 1.2 0 1.2 0 4',
                                   'particle minecraft:block{block_state:"minecraft:dirt"} ~ ~0.1 ~ 1.5 0.1 1.5 0 40', snd('entity.generic.explode', 0.8, 0.6)] + X.end)
    fn(f'{pfx}/stomped', [f'function bm:{pfx}/hurt', 'data modify entity @s Motion[1] set value 0.5d'])
    for i in ('', '2', '3'):                       # (three blasts of blue fire, down the line at the foe)
        fn(f'{pfx}/ranged{i}', X.hit(3) + [f'execute as @e[{foe},distance=..10.5,sort=nearest,limit=1] at @s run function bm:{pfx}/breathed',
                                           f'execute facing entity @e[{foe},distance=..10.5,sort=nearest,limit=1] eyes run function bm:{pfx}/beamfx',
                                           snd('entity.blaze.shoot', 0.8, 0.5)] + X.end)
    fn(f'{pfx}/breathed', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:60s}', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.4 0.3 0.05 12'])
    fn(f'{pfx}/beamfx', [f'particle minecraft:soul_fire_flame ^ ^1.4 ^{d} 0.1 0.1 0.1 0.01 2' for d in range(1, 10)])
    fn(f'{pfx}/charged', [f'execute as @e[{foe},distance=..8] run function bm:{pfx}/roared', 'particle minecraft:sonic_boom ~ ~1.5 ~ 0 0 0 0 1'])
    fn(f'{pfx}/roared', ['effect give @s minecraft:slowness 5 1', 'effect give @s minecraft:weakness 5 0'])
    X.second.append('tag @e[type=minecraft:wolf,tag=bm.rypet] add bm.kaiju')
    return lines


def _encounter(G, X):
    """(its meeting is phase249's hatching: the encounter box is only ever an admin's)"""
    fn, tellraw = G.fn, G.tellraw
    fn('p272/enc/talk', [f'execute unless score @s bm.pid = {X.here} bm.pid run return 0', 'function bm:p272/enc/joined'])


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    say = lambda txt: title('@s', 'actionbar', [T('The Atomic Rex: ', COL, bold=True), T(txt, LINE)])
    frame = dict(models=[], click=['playsound minecraft:entity.ravager.roar block @a[distance=..12] ~ ~ ~ 0.4 1.6', 'particle minecraft:soul_fire_flame ~ ~0.2 ~ 0.15 0.15 0.15 0.01 8'])
    W5.build(Rex, G, _abilities, _encounter, sitb=(120, [(0, 'sit2'), (60, 'sit')]), frame=frame)
    pfx = Rex.pfx
    second, tick = G.FUNCS['loop/second'], G.FUNCS['tick']
    # ---- FULL SIZE (compsize, the Rat King's toggle the other way round: its own build is companion size, the twin is its full one)
    import compsize as CSZ
    CSZ.build(G, pfx, 'bm.rqcs', 'bm.rqcz', f'bm.{Rex.q}s', HOST_C, HOST_F,
              say('(it stands up, and up, and UP - Full Size: on)'), say('(it folds itself down to your size - Full Size: off)'), hit=('bm.ryhit', HIT_C, HIT_F))
    CSZ.LATE.append((pfx, K_UP, 'bm.rqcz', ()))
    T_ = G.FUNCS[f'{pfx}/tick']
    assert T_[0] == 'scoreboard players operation #me bm.pid = @s bm.pid', T_[0]
    T_[1:1] = CSZ.sync(pfx, 'bm.rqcs', 'bm.rqcz', f'bm.{Rex.q}s', HOST_C, HOST_F)
    fn(f'{pfx}/box_fit', [f'execute if entity @s[tag=bm.rqcz] run function bm:{pfx}/box/full'])
    fn(f'{pfx}/box/full', CSZ.resize('bm.ryhit', *HIT_F))
    # ---- RIDE: it goes home as a follower and comes as phase249's mount - full size, saddled (the Mecha's, in its costume) - you on it
    fn('p272/ride', ['execute if function bm:p20/frog/has_vehicle run return run ' + say('(get down first)'),
                     'execute unless function bm:p249/allowed run return run ' + say('(it won\'t carry you here - not in a dungeon, a market, the vault or a heist)'),
                     'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #on bm.rng 0',
                     'execute as @e[type=minecraft:wolf,tag=bm.rypet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run scoreboard players set #on bm.rng 1',
                     'execute if score #on bm.rng matches 0 run return run ' + say('(call it first - then ride it)'),
                     'execute as @e[type=minecraft:wolf,tag=bm.rypet,tag=!bm.ffpet] if score @s bm.pid = #me bm.pid run tag @s add bm.rysel2', f'function bm:{pfx}/dismiss',
                     'scoreboard players set #k bm.rxv 1', f'execute if score @s bm.cosry matches {MECHA} run scoreboard players set #k bm.rxv 2',
                     'function bm:p249/call',
                     'scoreboard players operation #me bm.rxid = @s bm.rxo',
                     'execute as @e[type=minecraft:horse,tag=bm.rxh] if score @s bm.rxid = #me bm.rxid run tag @s add bm.ryride',
                     'ride @s mount @e[type=minecraft:horse,tag=bm.ryride,limit=1,sort=nearest]'])
    second.append('execute as @e[type=minecraft:horse,tag=bm.ryride] at @s unless function bm:p249/has_rider run function bm:p272/ride_end')
    fn('p272/ride_end', ['scoreboard players operation #me bm.rxid = @s bm.rxid', 'function bm:p249/gone',
                         f'execute as @a if score @s bm.rxo = #me bm.rxid at @s run function bm:{pfx}/try_summon'])
    # (its whistle while you ride it: the mount's breath, as ever)
    U = G.FUNCS[f'{pfx}/use']
    U.insert(0, 'execute if function bm:p249/riding_mine run return run function bm:p249/ride_use')


def late(G):
    """(after phase249's generate: its hatching, its hangar, its remote - the mount made a follower)"""
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    say = lambda txt: title('@s', 'actionbar', [T('The Atomic Rex: ', COL, bold=True), T(txt, LINE)])
    pfx = Rex.pfx
    second = G.FUNCS['loop/second']
    # ---- the hatching: the rex is a follower met - its whistle (phase249 gives it) calls it now
    eg = G.FUNCS['p249/egg/gift']
    eg.insert(1, 'function bm:p272/hatched')
    fn('p272/hatched', [f'tag @s add bm.{Rex.ab}met', f'advancement grant @s only bm:story/{Rex.W}_friend',
                        tellraw('@s', [T('The Atomic Rex', COL, bold=True), T(' is your follower: use the whistle to call it; sneak + use for its menu - Ride, Full Size.', 'gray')])])
    # ---- THE MECHA: the hangar's dormant machine needs a pilot (a rex you've hatched) - and it's a costume, not a mount of its own
    ht = G.FUNCS['p249/hang/try']
    k = next(i for i, l in enumerate(ht) if l == 'tag @s add bm.rxwaker')
    ht.insert(k, f'execute unless entity @s[tag=bm.{Rex.ab}met] run return run ' +
              tellraw('@s', [T('The machine\'s cockpit lights flicker - and die. ', 'gray', italic=True), T('It needs a pilot. ', '#8ab4ff'),
                             T('(A heart that breathes fire - a rex of your own, hatched.)', 'dark_gray')]))
    j = next(i for i, l in enumerate(ht) if 'mecha_remote' in l and l.startswith('give'))
    ht[j] = f'function bm:p99/unlock/rex{MECHA}'
    jt = next(i for i, l in enumerate(ht) if 'Mecha Rex Remote' in l)
    ht[jt] = tellraw('@s', [T('The Mecha', '#8ab4ff', bold=True), T(' is your Atomic Rex\'s now - a costume in its wardrobe. Ride it in it: laser breath, rocket fist.', 'gray')])
    # (the old remote: your rex, called in the costume)
    fn(f'{pfx}/remote', [f'execute unless entity @s[tag=bm.{Rex.ab}met] run return run ' + say('(nothing answers - you have no rex to pilot it)'),
                         f'function bm:p99/unlock/rex{MECHA}', f'scoreboard players set @s bm.cosry {MECHA}', 'function bm:p99/rex_now', f'function bm:{pfx}/try_summon'])
    # ---- MIGRATION: hatched before - a follower met; the Mecha built - the costume (and the follower, its pilot); the old Mounts page - its item back
    second.append(f'execute as @a[tag=bm.rxhatch,tag=!bm.{Rex.ab}met] run function bm:p272/hatched')
    second.append('execute as @a[tag=bm.rxmecha,tag=!bm.rymig] at @s run function bm:p272/mig/mecha')
    fn('p272/mig/mecha', ['tag @s add bm.rymig', f'execute unless entity @s[tag=bm.{Rex.ab}met] unless items entity @s container.* *[minecraft:custom_data~{{bm:"{ITEM}"}}] run ' + give(ITEM),
                          f'execute unless entity @s[tag=bm.{Rex.ab}met] run function bm:p272/hatched', f'function bm:p99/unlock/rex{MECHA}',
                          tellraw('@s', [T('Your Mecha Rex', '#8ab4ff', bold=True), T(' is a costume now - your Atomic Rex\'s, in its wardrobe.', 'gray')])])
    second.append('execute as @a[scores={bm.pwrx=1..}] at @s run function bm:p272/mig/page')
    fn('p272/mig/page', ['function bm:p179/w/pid', 'scoreboard players set #got bm.rxv 0', 'execute store result score #got bm.rxv run function bm:p249/w/outm_rx with storage bm:tmp pw',
                         'scoreboard players reset @s bm.pwrx',
                         tellraw('@s', [T('The Atomic Rex', COL, bold=True), T(' is a follower now: its whistle is back in your hands - put it on your Partner Wheel with the others.', 'gray')])])
    fn('admin/rex_reset', [f'tag @s remove bm.{Rex.ab}met', 'tag @s remove bm.rymig', f'clear @s *[minecraft:custom_data~{{bm:"{ITEM}"}}]',
                           title('@s', 'actionbar', T('The Atomic Rex has not met you yet.', COL))])
