"""2.99: VEXIS, THE UNLINKED - what's left of Admiral Vexis (phase242) with the hive-link cut: one Vorn, alone in its own head for the
first time in an age, and curious about everything. HARD MODE: the Severed Link (p2/armadaitems) is in the quiet after its fall, the
first time (vexis_art.py, form 'unlinked'; armada_lore.py).

  HIVE-GRIP   a foe within 3, every 1.5 s: three long fingers and a shove of gravity (6).
  PLASMA BOLT a foe within 14, every 4 s: a bolt from its palm (8, burning).
  GRAVITY WELL (charged, every minute) a small singularity: every monster within 7 dragged together and crushed (12), held slowed.
  DEFLECTOR   you, hurt in a fight, every 10 s: a green deflector round you - Resistance and Absorption - and arrows near you knocked away.
  SCOUT DRONE out of a fight, every minute: it sends a little drone up - Night Vision, and monsters within 24 lit up for a moment.
  THE HIVE HESITATES  Vorn within 10 of it are slowed and weakened while it's out: they still hear their Admiral, a little.
Everything else is every follower's: sitting, a wardrobe, a rare aura, a shiny, the Partner Wheel, a frame, a display case, Cecil's
doll, the honours, a Raid Contract; pairs with Bender, Mr. Capshun, Henry and Nia - and OLD ENEMIES, with Zib.
ITS FORMS (its menu: Form): Unlinked (its own small self), THE WARFRAME, THE HIVE-LINK and STARFIRE - each of the Admiral's three
forms, at a companion's size (the warframe about 3.5 blocks), from the first. Felled a second time (phase242: bm.xbwar), its menu's
Size makes any of the three as vast as it stood against you."""
from items import T, ITEMS
from useitem import hold, HOLD
import vexis_art as VA
import rigpet as RP
import rigface as RF2
import phase141 as P141
import phase134 as P134
import phase235 as P235
import armada_lore as L
import p2.armadaitems  # noqa: F401  (the Severed Link, its summoning item)

COL = L.VX_COL


class Vexis(RP.Cfg):
    W, NAME, COL, LINE, pfx, ab, q = 'vexis', 'Vexis, the Unlinked', COL, '#c8f0c0', 'p243', 'xb', 'qx'
    A = RF2.art(VA)
    MENU, PET_HP, PET_CD, ITEM = 5150, 50, 150, 'vexis_link'
    pron, they = 'it', 'it'
    FACE = {'happy': 'soft', 'surprised': 'wide', 'hurt': 'dim', 'sleepy': 'closed', 'blink': 'closed', 'squint': 'narrowed', 'serious': 'narrowed'}
    ATTRS = dict(armor=10, attack_damage=6, movement_speed=0.36, follow_range=32, step_height=1.1)
    SCALE, HIT = 1.1, (1.0, 2.3)
    SWAP = tuple(VA.PARTS)                      # (every part: none of its models is a plain 'vx_<part>')
    SWAP_START = True
    CYCLE = P235.cycle((240, [(0, 'idle_a'), (120, 'idle_b')]), (240, [(0, 'sit_a'), (120, 'sit_b')]),
                       (None, [(0, 'happy')]),
                       {7: (None, [(0, 'slash_up'), (5, 'slash')]), 8: (None, [(0, 'bolt_up'), (8, 'bolt')]),
                        12: (None, [(0, 'well'), (16, 'happy')]), 13: (None, [(0, 'deflect'), (16, 'idle_a')]),
                        14: (None, [(0, 'sit_b'), (40, 'idle_a')])})
    DUR = dict(P235._DUR, slash_up=4, slash=2, bolt_up=6, bolt=3, well=8, deflect=6, tired=20)
    QUIPS = ['"It is so quiet in here. I keep listening for them. They do not come."', '(it holds up one long hand and stares at it, as if counting the fingers)',
             '"What is this one called? The square green thing that explodes. I would like to know everything."',
             '"I was a navigator, once. Before. I think I would like to see the stars without taking them."',
             '(its gravity ring lifts a pebble, turns it over, and sets it down again, very carefully)', '"Vexis. Vexis. It is strange to have a name that is only mine."']
    HELLO = ('(Vexis drifts back to your side, its ring humming)', '(a soft green light - and Vexis is there, hovering an inch off the ground) "I came. I wanted to."',
             '(it bows its long head, and the ring folds it away into the dark)')
    SIT = ('"Rest? Yes. I am learning to rest."', '(it settles cross-legged, its ring slowing to a lazy orbit)')
    FAINT = '"...the quiet... is very loud..."'
    NOT_YOURS = '"I am... with another. I chose them. Go."'
    POWERS = [('Hive-Grip', 'a foe within 3, every 1.5 s: three long fingers and a shove of gravity - 6'),
              ('Plasma Bolt', 'a foe within 14, every 4 s: a bolt from its palm - 8, burning'),
              ('Gravity Well', 'charged, every minute: every monster within 7 dragged together and crushed - 12, and held slowed'),
              ('Deflector', 'you, hurt in a fight, every 10 s: Resistance and Absorption - and arrows near you knocked away'),
              ('Scout Drone', 'out of a fight beside you, every minute: Night Vision, and the monsters within 24 lit up for a moment'),
              ('The Hive Hesitates', 'while it is out, the Vorn near it (10) are slowed and weakened: they still hear their Admiral, a little')]
    INTRO = [T('Vexis, the Unlinked', COL, bold=True), T(' - once Admiral Vexis, the Voice of the Hive. The link is cut. ', 'gray'),
             T('It is only one, now, and it would like to know everything.', '#c8f0c0', italic=True)]
    BUTTONS = ((6, 'Form', 'Unlinked, the Warframe, the Hive-Link, Starfire - the Admiral\'s three forms, at a companion\'s size', 'p243/form/next'),
               (7, 'Size: Companion / Full', 'Its form as vast as it stood against you (yours once you fell Admiral Vexis a second time)', 'p243/form/size'))
    BURST = ['particle minecraft:reverse_portal ~ ~1.2 ~ 0.4 0.8 0.4 0.05 30', 'particle minecraft:dust{color:[0.48,1.0,0.42],scale:1.4} ~ ~1.2 ~ 0.5 0.8 0.5 0 20',
             'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.1 10']
    FADE_SOUND = 'playsound minecraft:block.beacon.deactivate neutral @a[distance=..20] ~ ~ ~ 1 1.4'
    SUMMON_EXTRA = ['playsound minecraft:block.beacon.power_select neutral @a[distance=..24] ~ ~ ~ 1 1.4', 'playsound minecraft:block.conduit.ambient.short neutral @a[distance=..24] ~ ~ ~ 1 0.8']
    ENC_POSES = [(0, 'tired'), (40, 'idle_a')]
    ENC_PARTICLE = 'execute if score #f bm.rng matches 20 run particle minecraft:reverse_portal ~ ~1.5 ~ 0.3 0.3 0.3 0.02 8'
    ADV = ('Unlinked', 'Cut the hive-link of Admiral Vexis - and take what is left of it with you')
    ADMIN_HINT = 'Hard mode: fell Admiral Vexis at the helm of the Vorn Armada (in the End). The Severed Link is yours, the first time.'
    MEET_HINT = 'Hard mode: fell Admiral Vexis at the helm of the Vorn Armada.'


RP.register(Vexis)
RF2.setup(Vexis, 'head')

# the Severed Link calls it
_e = ITEMS['vexis_link']
_e['comps'].update(hold('none'))
HOLD['vexis_link'] = f'bm:{Vexis.pfx}/use'
_DOLL = 'A doll of Vexis - a head far too big for it, enormous eyes, and a ring that really spins.'
from items import item, TOTEM
item('doll_vexis', TOTEM, 'Vexis Doll', COL, [_DOLL, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'),
                                             ('Sneak + punch: pick it up.', 'gray')], model='bm:doll_vexis', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_vexis'] = 'bm:p141/doll_vexis/use'
P141.DOLLS.append(('doll_vexis', Vexis.NAME, COL, _DOLL, 'minecraft:reverse_portal', 'minecraft:block.beacon.power_select', 'minecraft:poof'))
P141.DOLL_FROM['doll_vexis'] = ('vexis_link', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})
P134.FIT['vexis_link'] = (0.0, 2.3, -0.9, 0.9, -0.6, 0.6)                 # (re-measured: phase134.measure)

# ---- its pairs with Bender and Mr. Capshun - and with Zib (Henry's and Nia's: cat_bonds)
import phase188 as P188
_O = P188.O
_eff = lambda *es: [f'effect give {_O} minecraft:{e} {15 if e == "night_vision" else 3} {a} true' for e, a in es]
P188.VNAME.update({'vexis': 'Vexis'})
P188.PAIRS.update({
    'xb_bender': ('vexis', 'bender', 'Fetch, in Zero-G', '#e0a860', 'Vexis and Bender - it lifts the stick with gravity; he does not care how, only that it flies',
                  _eff(('speed', 0), ('jump_boost', 1)),
                  [('bender', '(drops a stick at its feet and stares at it, tail going)'), ('vexis', '"You want... me to... improve the stick?" (it floats the stick. Bender loses his mind)')],
                  [('vexis', '"Why is he so happy? Nothing has happened."', 'bender', '(licks its three-fingered hand)')]),
    'xb_capshun': ('vexis', 'capshun', 'First Contact', '#f0f0f0', 'Vexis and Mr. Capshun - an alien learning what a story is',
                   _eff(('resistance', 0), ('haste', 0)),
                   [('capshun', '[Mr. Capshun narrates: "The invader laid down its fleet, and asked to be told a story instead."]'), ('vexis', '"Tell it again. The part where I am kind."')],
                   [('capshun', '[Mr. Capshun narrates: "He drew it a little green flag. It was the first thing it ever owned."]', 'vexis', '(it holds the drawing by the very edges)')]),
    'xb_zib': ('vexis', 'zib', 'Old Enemies', '#3ad8c8', 'Vexis and Zib - the Admiral who hunted the Donadians, and the Donadian who will not let it forget',
               _eff(('strength', 0), ('night_vision', 0)),
               [('zib', '"You took my whole squad, Admiral."'), ('vexis', '"...Yes. I remember every one. I will remember them for you, if you let me."')],
               [('vexis', '"Why do you walk with me, Zib?"', 'zib', '"So you never get to forget. And because... nobody else should have to."')]),
})
P188.ICON.update({'xb_bender': 'bm:vexis_link', 'xb_capshun': 'bm:vexis_link', 'xb_zib': 'bm:vexis_link'})


def extend_offers(O, offer):
    pass


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    RP.rp(Vexis, R, R.ICONS.get('vexis_link'))
    RF2.faces(Vexis, 'head', R)


def textures():
    return {}                                   # (the art's own textures go in with the boss, phase242)


def generate_early(G):
    RP.contract(Vexis, G)


def _abilities(G, X):
    fn, pfx, foe = G.fn, X.pfx, X.foe
    K = dict(melee=dict(st=7, x=8, at=5, cd=30, reach=3.0),
             ranged=dict(st=8, x=16, at=10, cd=80, near=3, far=14, face='serious', go=['playsound minecraft:block.beacon.power_select neutral @a[distance=..16] ~ ~ ~ 0.5 1.8']),
             charged=dict(st=12, x=24, at=10, cd=1200, r=7, face='serious', go=['playsound minecraft:block.end_portal.spawn neutral @a[distance=..16] ~ ~ ~ 0.5 1.6']),
             support=dict(st=13, x=20, at=8, cd=200, face='serious'),
             kind=dict(st=14, x=44, at=20, cd=1200, face='happy'))
    lines = P235.kit(G, X, K)
    P235.melee(G, X, 6, 3.0, ['particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.3 0.3 0.2 20', 'particle minecraft:dust{color:[0.48,1.0,0.42],scale:1.2} ~ ~1 ~ 0.4 0.4 0.4 0 10'],
               'minecraft:entity.shulker.shoot')
    tg = f'@e[{foe},distance=..14,sort=nearest,limit=1]'
    fn(f'{pfx}/ranged', X.hit(8) + [f'execute anchored eyes positioned ^ ^ ^1 facing entity {tg} eyes run function bm:{pfx}/bolt_fx', f'execute as {tg} at @s run function bm:{pfx}/bolted'] + X.end)
    fn(f'{pfx}/bolt_fx', [f'particle minecraft:dust{{color:[0.48,1.0,0.42],scale:1.4}} ^ ^ ^{d} 0.05 0.05 0.05 0 2' for d in range(1, 13)] +
       ['particle minecraft:electric_spark ^ ^ ^1 0.1 0.1 0.1 0.1 6', 'playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.5 1.6'])
    fn(f'{pfx}/bolted', [f'function bm:{pfx}/hurt', 'data modify entity @s Fire set value 60s', 'particle minecraft:electric_spark ~ ~1 ~ 0.3 0.4 0.3 0.1 12'])
    fn(f'{pfx}/charged', X.hit(12) + ['particle minecraft:reverse_portal ~ ~1 ~ 3 1 3 0.5 120', f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/welled'] + X.end)
    fn(f'{pfx}/welled', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 3',
                         f'execute facing entity @e[tag=bm.xbme,limit=1] feet if block ^ ^ ^1.5 #bm:grap_pass if block ^ ^1 ^1.5 #bm:grap_pass run tp @s ^ ^ ^1.5',
                         'particle minecraft:portal ~ ~1 ~ 0.3 0.6 0.3 1 16'])
    fn(f'{pfx}/support', ['execute on owner if entity @s[distance=..16] at @s run function bm:p243/deflect_you'])
    fn('p243/deflect_you', ['effect give @s minecraft:resistance 8 1 true', 'effect give @s minecraft:absorption 20 1 true',
                            'execute as @e[type=#minecraft:arrows,distance=..4] run data merge entity @s {Motion:[0.0d,0.6d,0.0d]}',
                            'particle minecraft:dust{color:[0.48,1.0,0.42],scale:1.2} ~ ~1 ~ 0.8 1 0.8 0 30', 'particle minecraft:end_rod ~ ~1 ~ 0.8 1 0.8 0.02 10',
                            'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 1 1.6'])
    fn(f'{pfx}/kind', ['execute on owner if entity @s[distance=..8] run function bm:p243/drone_you'])
    fn('p243/drone_you', ['effect give @s minecraft:night_vision 60 0 true', 'effect give @e[type=#bm:hostile,distance=..24] minecraft:glowing 4 0 true',
                          'particle minecraft:end_rod ~ ~3 ~ 0.3 0.3 0.3 0.05 10', 'playsound minecraft:entity.vex.ambient player @s ~ ~ ~ 0.6 1.6',
                          'execute unless entity @s[tag=bm.hush] run ' + G.title('@s', 'actionbar', [T('Vexis: ', COL, bold=True), T('"My little drone says: monsters, there. And there. You are welcome."', '#c8f0c0', italic=True)])])
    return lines


def generate(G):
    RP.build(Vexis, G, _abilities, lambda G_, X: G_.fn(f'{Vexis.pfx}/enc/talk', ['function bm:p243/enc/joined']))   # (no encounter: the Link comes from its fall)
    # THE HIVE HESITATES: the Vorn near it slowed and weakened while it's out
    G.FUNCS['loop/second'] += ['execute as @e[type=minecraft:wolf,tag=bm.xbpet,tag=!bm.ffpet] at @s run effect give @e[tag=bm.vorn,distance=..10] minecraft:slowness 2 0 true',
                               'execute as @e[type=minecraft:wolf,tag=bm.xbpet,tag=!bm.ffpet] at @s run effect give @e[tag=bm.vorn,distance=..10] minecraft:weakness 2 0 true']
    _forms(G)


# ====================================================================== ITS FORMS - the Admiral's three, at a companion's size or full
# Vexis can walk beside you in any of its three boss forms (its owner's bm.xbub: 0 Unlinked, 1 the Warframe, 2 the Hive-Link,
# 3 Starfire), at a companion's size (vexis_art.COMPANION_SCALE) or - felled a second time (bm.xbwar) - full (phase242.SCALE;
# bm.xbsz 1). One giant rig (20 displays) does all six: every pose swaps every part's model, and each form-and-size has its own
# place and poses. The follower's own small rig stays, unseen (view_range 0), so Unlinked comes back at once. The giant's poses
# follow the host's state: walking, resting (sat, asleep, its drone), its blows.
FORMS = {1: 'warframe', 2: 'hivelink', 3: 'starfire'}
FORM_NAME = {0: 'Unlinked', 1: 'the Warframe', 2: 'the Hive-Link', 3: 'Starfire'}
FORM_LINE = {0: '"Small again. I like small. Small can sit on things."', 1: '"My shell. I had missed it - is that strange? It fits like a memory."',
             2: '"The rings still answer me. Only me, now."', 3: '"A little of the star. Only a little. I will not take more than I need."'}
_cyc = lambda f: {0: (240, [(0, 'idle_a'), (120, _pp(f, 'idle_b'))]), 1: (24, [(0, _pp(f, 'walk_0')), (6, _pp(f, 'walk_1')), (12, _pp(f, 'walk_2')), (18, _pp(f, 'walk_3'))]),
                  2: (240, [(0, _pp(f, 'sit_a', 'dormant')), (120, _pp(f, 'sit_b', 'sit_a', 'dormant'))]),
                  3: (None, {'warframe': [(0, 'stomp_up'), (8, 'stomp')], 'hivelink': [(0, 'gravity')], 'starfire': [(0, 'flare_up'), (8, 'flare')]}[f]),
                  4: (None, {'warframe': [(0, 'missiles')], 'hivelink': [(0, 'beam_up'), (8, 'beam')], 'starfire': [(0, 'lance_up'), (8, 'lance')]}[f]),
                  5: (None, {'warframe': [(0, 'cannon_up'), (8, 'cannon')], 'hivelink': [(0, 'beam_up'), (8, 'beam')], 'starfire': [(0, 'lance_up'), (8, 'lance')]}[f]),
                  6: (None, [(0, _pp(f, 'happy', 'roar'))])}
WAR_OF = [(2, '4'), (6, '6'), (2, '14'), (2, '16..17'), (1, '1..3'), (1, '10'), (3, '7'), (6, '13'), (5, '8'), (4, '12')]      # (rigpet's states: 4 sat, 6 happy, 14 its kindness, 16-17 riding/curled; 1-3 and 10 on the move; 7, 8, 12, 13 its blows and its deflector)


def _pp(f, *names):
    P = VA.BOSS_POSES[f]
    return next((n for n in names if n in P), 'idle_a')


def _size(f, full):
    import phase242 as P242
    if full: return P242.SCALE[f]
    comp = getattr(VA, 'COMPANION_SCALE', {})
    return comp.get(f, P242.SCALE[f] * {'warframe': 0.29, 'hivelink': 0.35, 'starfire': 0.32}[f])


def _forms(G):
    import rigfol as RFol
    import phase242 as P242
    from nbt import F
    fn, title = G.fn, G.title
    A = VA
    usel = lambda p: f'@e[type=minecraft:item_display,tag=bm.xbusel,tag=bm.xbu_{p}]'
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in ('bm.xbub', 'bm.xbuf', 'bm.xbus', 'bm.xbsz', 'bm.xbuk')]
    G.OBJECTIVES += ['bm.xbub', 'bm.xbuf', 'bm.xbus', 'bm.xbsz', 'bm.xbuk']
    rig = [f'summon minecraft:item_display ~ ~ ~ {RFol.part_nbt(A, p, ["bm.xbu", f"bm.xbu_{p}", "bm.xbunew"], _size("warframe", False), model=A.model_name(p, A.BOSS_POSES["warframe"]["idle_a"]), extra=dict(view_range=F(4.0)))}'
           for p in A.PARTS]
    keys = []
    for i, f in FORMS.items():
        cyc = _cyc(f)
        for full in (0, 1):
            k, SC, tag = i * 2 + full, _size(f, full), f'{f}{"_full" if full else ""}'
            keys.append((k, tag))
            fn(f'p243u/{tag}/place', RFol.place(A, SC / 16, usel))
            for name in {pz for _per, frames in cyc.values() for _t, pz in frames}:
                fn(f'p243u/{tag}/pose/{name}', RFol.pose(A, A.BOSS_POSES[f][name], SC, P242.DUR.get(name, 6), usel, swap=tuple(A.PARTS)))
            RFol.cycles(fn, f'p243u/{tag}', cyc, 'bm.xbuf', 'bm.xbus', lambda p, tag=tag: f'p243u/{tag}/pose/{p}')
            G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RFol.periods(cyc)]
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #2 bm.rng 2']
    # (as the host, each tick: its owner's choice of form and size -> #ub = form * 2 + full)
    G.FUNCS['p243/tick'][-2:-2] = ['scoreboard players set #ub bm.rng 0', 'execute on owner run function bm:p243u/key',
                                   'execute if score #ub bm.rng matches 2.. run function bm:p243u/on',
                                   'execute unless score #ub bm.rng matches 2.. if entity @e[type=minecraft:item_display,tag=bm.xbu,distance=..16] run function bm:p243u/off']
    fn('p243u/key', ['scoreboard players operation #ub bm.rng = @s bm.xbub', 'scoreboard players operation #ub bm.rng *= #2 bm.rng',
                     'execute if entity @s[tag=bm.xbwar] if score @s bm.xbsz matches 1 run scoreboard players add #ub bm.rng 1'])
    fn('p243u/on', ['execute as @e[type=minecraft:item_display,tag=bm.xbu] if score @s bm.pid = #me bm.pid run tag @s add bm.xbusel',
                    'execute unless entity @e[type=minecraft:item_display,tag=bm.xbusel] run function bm:p243u/raise',
                    'execute as @e[type=minecraft:item_display,tag=bm.xbsel] run data modify entity @s view_range set value 0f',
                    # (a new form or size: the cycle starts over, so its first pose swaps every model at once)
                    'execute unless score @s bm.xbuk = #ub bm.rng run scoreboard players set @s bm.xbus -1',
                    'execute unless score @s bm.xbuk = #ub bm.rng run function bm:p243u/changed',
                    'scoreboard players operation @s bm.xbuk = #ub bm.rng',
                    'scoreboard players set #us bm.rng 0'] +
       [f'execute if score @s bm.qxs matches {r} run scoreboard players set #us bm.rng {st}' for st, r in WAR_OF] +
       ['execute if score #us bm.rng = @s bm.xbus run scoreboard players add @s bm.xbuf 1', 'execute unless score #us bm.rng = @s bm.xbus run scoreboard players set @s bm.xbuf 0',
        'scoreboard players operation @s bm.xbus = #us bm.rng'] +
       [f'execute if score #ub bm.rng matches {k} run function bm:p243u/{tag}/anim' for k, tag in keys] +
       [f'execute if score #ub bm.rng matches {k} rotated as @s rotated ~ 0 run function bm:p243u/{tag}/place' for k, tag in keys] +
       ['tag @e[tag=bm.xbusel] remove bm.xbusel'])
    fn('p243u/changed', ['particle minecraft:electric_spark ~ ~2 ~ 1 1.5 1 0.3 60', 'particle minecraft:reverse_portal ~ ~1.5 ~ 1 1 1 0.2 60',
                         'playsound minecraft:block.beacon.power_select neutral @a[distance=..24] ~ ~ ~ 1 0.8',
                         'execute if score #ub bm.rng matches 3 run playsound minecraft:block.beacon.activate neutral @a[distance=..32] ~ ~ ~ 1.5 0.5',
                         'execute if score #ub bm.rng matches 2..3 run playsound minecraft:entity.iron_golem.repair neutral @a[distance=..24] ~ ~ ~ 1 0.6'])
    fn('p243u/raise', rig + ['execute as @e[type=minecraft:item_display,tag=bm.xbunew] run scoreboard players operation @s bm.pid = #me bm.pid',
                             'tag @e[type=minecraft:item_display,tag=bm.xbunew] add bm.xbusel', 'tag @e[type=minecraft:item_display,tag=bm.xbunew] remove bm.xbunew',
                             'scoreboard players set @s bm.xbuk -1'])
    fn('p243u/off', ['execute as @e[type=minecraft:item_display,tag=bm.xbu] if score @s bm.pid = #me bm.pid run kill @s',
                     'execute as @e[type=minecraft:item_display,tag=bm.xbsel] run data modify entity @s view_range set value 1.6f',
                     'particle minecraft:reverse_portal ~ ~1.5 ~ 1 1 1 0.2 60', 'scoreboard players set @s bm.xbuk -1'])
    G.FUNCS['loop/second'].append('execute as @e[type=minecraft:item_display,tag=bm.xbu] unless function bm:p243u/has run kill @s')
    fn('p243u/has', ['scoreboard players operation #me2 bm.pid = @s bm.pid',
                     'execute as @e[type=minecraft:wolf,tag=bm.xbpet] if score @s bm.pid = #me2 bm.pid run return 1', 'return 0'])
    # (its menu: Form - the next of four; Size - companion or full, once it's been felled twice)
    say = lambda line: title('@s', 'actionbar', [T('Vexis: ', COL, bold=True), T(line, '#c8f0c0')])
    fn('p243/form/next', ['scoreboard players add @s bm.xbub 1', 'execute unless score @s bm.xbub matches 0..3 run scoreboard players set @s bm.xbub 0'] +
       [f'execute if score @s bm.xbub matches {i} run ' + say(f'{FORM_LINE[i]} ({FORM_NAME[i]})') for i in FORM_NAME])
    fn('p243/form/size', ['execute unless entity @s[tag=bm.xbwar] run return run ' + title('@s', 'actionbar', [T('It cannot grow so vast yet. ', COL, italic=True),
                                                                                                        T('(Fell Admiral Vexis a second time.)', 'gray')]),
                          'execute unless score @s bm.xbub matches 1..3 run return run ' + say('"Unlinked is the size I am. Choose a form first - then I can be vast."'),
                          'execute if score @s bm.xbsz matches 1 run return run function bm:p243/form/small',
                          'scoreboard players set @s bm.xbsz 1', say('"As I stood against you. Mind your head." (Full size)')])
    fn('p243/form/small', ['scoreboard players set @s bm.xbsz 0', say('"Companion-sized. Easier to fit through doors." (Companion size)')])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.xbu]']
