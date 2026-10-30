"""3.0e: THE BROOD-MIRE - the Vorn's alien cousin of the Dread Mire (xmire_art draws it; mirekit runs it, as it runs phase246's).
The hive took a Dread Mire aboard the Brood-Carrier and "improved" it: a grotesque heap of purple sacs, green-veined, crowded with
blinking yellow eyes, four sucker-lined tentacles with eyes at their tips, a lamprey maw with three more eyes in its throat.

HARD MODE, and only while the hive has your world in mind: none comes (and those about melt away) once Admiral Vexis has fallen
(#vfell) - until a Dreadnought is attacked again and the hive remembers (phase241's rekindle). Never in the Nether (the Undercrown)
nor in the Overworld outside an Invasion Night: one found there melts.
WHERE  THE END, past the main island (over OUTER from 0,0; never within phase255's reach of the Armada): now and then a monster
       rising naturally comes up as a Brood-Mire instead - 1 in ROLL, never within APART of another, one a day for each player (the
       nearest within 48), none near a switched-on Signal Jammer. A puddle with eyes in it: it creeps, and rises for anyone within 10.
       THE VORN ARMADA: the Bio-Wave's last wave (trial 3, the Brood-Carrier) brings one down a short tractor beam - the wave holds
       till it's dead; and, rarely, one lies in wait in a quiet hall (an fx marker whose nearest trial is a puzzle or wave room of the
       Dock, Brood-Carrier, Star-Forge or Navigator - never a guardian's, a socket's, a reactor's, the Gauntlet's, the Flagship's, and
       never within 14 of a vault or a relic room), one at a time.
       INVASION NIGHTS: one of the invaders' drops (phase32's surge, 3 in 100): a saucer's tractor beam lowers it 20 blocks off, it
       splats and rises - one a night for each player, two in the world at most; none near a jammer; at dawn they melt away.
RISEN  as the Dread Mire: GRAB (6) at 3.5-8, STAB (10) within 4.5 - and at 8-14 the SPIT: it rears, maw wide, and lobs a glob
       of acid (5, Poison) that leaves a hissing pool (Slowness II, Poison) for 3 s. Worn to half, it shudders and three Broodlings
       (small slimes) burst out of its cysts; they melt with it.
REPELLED  by a switched-on SIGNAL JAMMER within 12 (phase52 - an Invasion Night's until dawn, and now in the End for 10 minutes):
       it shrieks, recoils and sinks; the puddle slips away from the jammer; none rises near it. Holding the SEVERED LINK (Vexis's),
       it will not rise for you. Light means nothing to it.
ITS DEATH  the Dread Mire's melt, in purple-green (phase257's dfx_bgoop, bbubble, bpop): 1-3 BROOD ICHOR, 2-4 green or violet Xenite.
BROOD ICHOR  (each use the Shadow Remnant's, in the hive's way)
       used beside your Mireling (within 6, out): it drinks it - and changes: THE BROOD MIRELING, its wardrobe's look 8, for good
       (and, owning its shiny too, look 9: Shiny Pearl Brood). 4 in hand, used: a vial of HIVE SCENT - drunk, for 5 minutes the
       Vorn's guns (troopers', saucers') pass you over, no Vorn drops near you and no Brood-Mire rises for you or fights you.
       16 in hand, sneak + used: a BROOD POD - sneak + use it on a block: a Brood-Mire of your own takes root there and guards it
       (mirekit.bound: it fights the monsters that come near - it spits at those out of reach; creepers keep away). Queen Ava takes
       8 Brood Ichor for the Mireling's honour in place of 8 Shadow Remnants (phase201)."""
from items import T, item, TOTEM, consumable, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D as Dd
import xmire_art as A
import armada_lore as L
import phase246 as P246

PFX = 'p258'
NAME, COL = A.NAME, '#b46aff'
GREEN = L.HIVE
HP, FLOOR = 180, 100
ROLL = 250                          # (1 in this many natural spawns in the outer End comes up a Brood-Mire)
APART = 96
OUTER = 1000                        # (the outer End: this far from 0, 0)
SCENT = 300
SPIT_REACH, SPIT_DMG = 14, 5
JAM_R = 12                          # (a jammer this near repels it)
INV_PCT = 3                         # (in 100 of the invasion surge's drops)
ROAM = 600                          # (aboard the Armada: 1 a second in this while someone's aboard and none roams)
ROAM_TRIALS = (1, 2, 3, 4, 6, 7, 10, 11, 12)      # (the puzzle and wave rooms of the Dock, Brood-Carrier, Star-Forge and Navigator)
BEAM_HI, BEAM_LO = 12, 4            # (blocks of tractor beam: under the open sky; indoors, aboard)
LOOK, SHINY_LOOK = 8, 9             # (the Mireling's wardrobe: 7 is its shiny, phase99/shiny.py)
FOES = 'gamemode=!spectator,gamemode=!creative,tag=!bm.hsc'


def snd(name, v=1.0, p=None, who='@a[distance=..32]'):
    """its voice: the Dread Mire's, higher and stranger (pitched up a third)"""
    base = P246.SND.get(name)
    pv = p if p is not None else (1.0 if base else P246.VAN[name][1])
    sid = base or 'minecraft:' + P246.VAN[name][0]
    return f'playsound {sid} hostile {who} ~ ~ ~ {v} {round(min(2.0, pv * 1.35), 2)}'


class CFG:
    """the Brood-Mire to mirekit"""
    P, NAME, COL, HP, FLOOR, ARMOR = PFX, NAME, COL, HP, FLOOR, 6
    A, SCALE = A, A.SCALE
    WAKE, LEAVE, CREEP, GRAB_DMG, STAB_DMG, EVERY, DIE_END, RISEN_SC, DORMANT_SC = 10, 20, 24, 6, 10, 50, 130, 2.4, 1.0
    DUR = dict(P246.DUR, **A.DUR)
    HOST, R, NEWP, NEWH, GRAB, GOOPT, GNEW, MELT, TAME = 'bm.bmire', 'bm.bxr', 'bm.bxnew', 'bm.bxnewh', 'bm.bxgrab', 'bm.bxgoop', 'bm.bxgnew', 'bm.bxmelt', 'bm.bxtame'
    FELL, CROSS, LIGHT_EXEMPT = '#vfell bm.cfg', f'bm:{PFX}/in_jam', None
    FLEE_FROM = '@a[tag=bm.jam,sort=nearest,limit=1]'
    FOES, WAKE_FOES = FOES, FOES + ',tag=!bm.bxlink'
    DUST, DRIP_DUST, STAB_DUST = '0.45,0.16,0.62', '0.55,0.9,0.18', '0.7,1.0,0.25'
    INK, SMOKE, RECOIL_FX, DRIP_BLOCK = 'minecraft:item_slime', 'minecraft:witch', 'minecraft:electric_spark', 'minecraft:purple_concrete'
    GOOP, BUBBLE, LOOT = 'bm:dfx_bgoop', 'bbubble', f'bm:{PFX}/ichor'
    SPIT, LIVE = {'reach': SPIT_REACH}, ('2..5', '8')
    snd = staticmethod(snd)
    # (the Overworld outside an invasion, and the Nether, are never its: one found there melts; a tame one is its owner's)
    SEC_EXTRA = [f'execute unless entity @s[tag=bm.bxtame] if dimension minecraft:the_nether run return run function bm:{PFX}/melt',
                 f'execute unless entity @s[tag=bm.bxtame] if dimension minecraft:overworld unless score #inv bm.bm matches 1 run return run function bm:{PFX}/melt']
    TICK_EXTRA = [f'execute if score @s bm.ms matches 9 run function bm:{PFX}/s/beam',
                  *[f'execute if score @s bm.ms matches {r} unless entity @s[tag=bm.bxhalf] unless entity @s[tag=bm.bxtame] if score #h bm.rng matches ..{FLOOR + HP // 2} '
                    f'run function bm:{PFX}/brood' for r in ('2..5', '8')]]
    LING = f'execute as @e[type=minecraft:slime,tag=bm.bxling] if score @s bm.mid = #me bm.mid at @s run function bm:{PFX}/ling/pop'
    MELT_EXTRA = [LING]
    DIE0_EXTRA = ['scoreboard players operation #me bm.mid = @s bm.mid', LING]


class BOUND:
    """(the Brood Pod's Bound Brood-Mire, to mirekit.bound)"""
    ITEM, TK, TAME_NAME, DAY_SINK = 'brood_pod', 'bm.bxtk', 'Bound Brood-Mire', False
    MON = 'type=#bm:hostile,tag=!bm.mire,tag=!bm.bmire,tag=!bm.khost,tag=!bm.boss,tag=!bm.stalker'
    refuse = [f'execute if predicate bm:p255/in_box run return run ' + 'title @s actionbar ' + snbt(T('Not aboard - the hive would only take it back.', 'gray'))]
    msg_use, msg_planted = 'Sneak + use on the top of a block: plant the Brood Pod.', 'Your Brood-Mire takes root. '
    FIGHT_EXTRA = [f'execute if score @s bm.ma matches 30.. if entity @e[{MON},distance=8..{SPIT_REACH}] run return run function bm:{PFX}/t/spit0']


# ---------------------------------------------------------------------------------------------------- items
_G = ('Hard mode: left by a Brood-Mire.', 'dark_gray')
item('brood_ichor', TOTEM, 'Brood Ichor', COL,
     ['What is left of a Brood-Mire. It glows,', 'and something in it is watching.',
      ('Used beside your Mireling: it drinks it.', 'blue'), ('4 in hand, used: a vial of Hive Scent.', 'blue'),
      ('16 in hand, sneak + used: a Brood Pod.', 'blue'), ('Queen Ava takes it in place of Shadow Remnants.', 'gray'), _G],
     model='bm:brood_ichor', stack=64, cat='alien', comps=hold('none'))
HOLD['brood_ichor'] = f'bm:{PFX}/ichor/use'
item('brood_pod', TOTEM, 'Brood Pod', COL,
     ['Sixteen ichors, grown together. It blinks.', ('Sneak + use on a block: a Brood-Mire of', 'blue'), ('your own takes root there and guards it -', 'blue'),
      ('it fights the monsters that come near.', 'blue'), ('Creepers keep away.', 'blue'), ('Sneak + punch it: take it back up.', 'gray')],
     model='bm:brood_pod', stack=4, cat='alien', comps=hold('none'))
HOLD['brood_pod'] = f'bm:{PFX}/heart/use'
item('hive_scent', TOTEM, 'Hive Scent', GREEN,
     ['It smells of nothing on this world.', ('Drink: for 5 minutes the Vorn take you', 'blue'), ('for one of their own - their guns pass', 'blue'),
      ('you over, nothing drops near you, and no', 'blue'), ('Brood-Mire rises for you or fights you.', 'blue')],
     model='bm:hive_scent', stack=16, cat='alien',
     comps={'minecraft:consumable': consumable(1.6, 'drink', 'minecraft:entity.generic.drink', False)})

# ---- the Mireling's costume: its wardrobe's looks 8 and 9 (7 is its shiny - phase99 put it there; a world remembers looks by number)
import phase99 as P99
import shiny as _SH
import xmireling_art as XL
_ml = P99.NEW['mireling'][3]
assert max(_ml) == LOOK - 1 and _SH.KEY.get('mireling') == LOOK - 1, ('the Mireling\'s looks moved', sorted(_ml))
_ml[LOOK] = (XL.NAME, ('#140620', '#4c1c70', '#8ad024'))
_ml[SHINY_LOOK] = (XL.SHINY_NAME, ('#605468', '#dcd0e4', '#ff8ade'))
P99.DYE.update({XL.NAME: 'purple', XL.SHINY_NAME: 'pink'})
import phase138 as _P138
for _k in (LOOK, SHINY_LOOK):
    _P138.HANDMADE.add(('mireling', _k))             # (phase138 makes no recoloured copies of them: xmireling_art draws them)
    _SH.UNSOLD.add(f'cos_mireling_{_k}')         # (never sold - found: a Brood Ichor fed to it)
    item(f'cos_mireling_{_k}', TOTEM, f'The Mireling\'s Veins: {_ml[_k][0]}', '#8ad024', [f'{_ml[_k][0]} - for the Mireling alone.',
         ('Found, never sold: feed your Mireling a Brood Ichor.', 'gray')], model='minecraft:purple_dye', stack=1, cat='cosmetic', glint=True)


# ---------------------------------------------------------------------------------------------------- generate
def generate(G):
    import mirekit as MK
    import phase241 as P241
    fn, title, give, tellraw = G.fn, G.title, G.give, G.tellraw
    tick, second = G.FUNCS['tick'], G.FUNCS['loop/second']
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    at = lambda t, cmd: f'execute if score @s bm.mt matches {t} {cmd[8:]}' if cmd.startswith('execute ') else f'execute if score @s bm.mt matches {t} run {cmd}'
    objs = ['bm.bxday', 'bm.hscent']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    P = PFX
    ME = '@e[type=minecraft:husk,tag=bm.mme,limit=1]'

    # (each second, while any is about: who holds the Severed Link - it will not rise for them)
    second.append(f'execute if entity @e[type=minecraft:husk,tag=bm.bmire,limit=1] run function bm:{P}/link')
    fn(f'{P}/link', ['tag @a[tag=bm.bxlink] remove bm.bxlink',
                     'execute as @a if items entity @s weapon.* *[minecraft:custom_data~{bm:"vexis_link"}] run tag @s add bm.bxlink'])
    fn(f'{P}/in_jam', [f'execute if entity @a[tag=bm.jam,distance=..{JAM_R}] run return 1', 'return 0'])

    MK.runtime(G, CFG)
    MK.watch(G, CFG)
    MK.fight(G, CFG)
    MK.death(G, CFG)
    G.wjson(f'bm/loot_table/{P}/ichor.json', {'pools': [{'rolls': 1, 'entries': [G.loot_entry('brood_ichor', G.uni(1, 3))]},
                                                       {'rolls': 1, 'entries': [G.loot_entry('xenite_green', G.uni(2, 4)), G.loot_entry('xenite_violet', G.uni(2, 4))]}]})

    # ================================================================== THE SPIT: it rears, and lobs a glob of acid
    fn(f'{P}/spit0', ['scoreboard players set @s bm.ms 8', 'scoreboard players set @s bm.mt 0', CFG.face, f'function bm:{P}/pose/spit_0', snd('shriek', 1.0, 1.5)])
    tgt_p = f'@p[distance=..{SPIT_REACH + 4},{FOES}]'
    fn(f'{P}/s/spit', [at(10, f'function bm:{P}/pose/spit_1'), at(11, snd('lash', 1.2, 1.4)),
                       at(11, f'execute if entity {tgt_p} positioned ^ ^4.4 ^2.2 run function bm:{P}/glob/new'),
                       at(11, f'execute as @e[type=minecraft:item_display,tag=bm.bxgn,distance=..6] at @s run tp @s ~ ~ ~ facing entity {tgt_p} feet'),
                       at(11, 'tag @e[type=minecraft:item_display,tag=bm.bxgn] remove bm.bxgn'),
                       at(30, 'scoreboard players set @s bm.ms 2'), at(30, 'scoreboard players set @s bm.ma 0'), at(30, 'scoreboard players set @s bm.mt 0')])
    glob = {'Tags': ['bm.bxglob', 'bm.bxgn'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:dfx_bbubble'}},
            'item_display': 'fixed', 'billboard': 'center', 'brightness': {'block': Int(15), 'sky': Int(15)}, 'view_range': F(2.0), 'teleport_duration': Int(1),
            'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0), F(0)], 'scale': [F(0.9)] * 3}}
    fn(f'{P}/glob/new', ['summon minecraft:item_display ~ ~ ~ ' + snbt(glob), 'scoreboard players set @e[type=minecraft:item_display,tag=bm.bxgn,distance=..1] bm.mt 0'])
    fn(f'{P}/glob/newm', ['summon minecraft:item_display ~ ~ ~ ' + snbt(dict(glob, Tags=['bm.bxglob', 'bm.bxgn', 'bm.bxgm'])),
                          'scoreboard players set @e[type=minecraft:item_display,tag=bm.bxgn,distance=..1] bm.mt 0'])
    tick.append(f'execute as @e[type=minecraft:item_display,tag=bm.bxglob] at @s run function bm:{P}/glob/tick')
    # (a lob: straight at where its target stood, an arc laid over it - up six ticks, level two, down after; 0.85 a tick, ~12 in 14)
    hit_p = f'@a[distance=..1.3,{FOES}]'
    hit_m = f'@e[{BOUND.MON},distance=..1.3]'
    fn(f'{P}/glob/tick', ['scoreboard players add @s bm.mt 1', 'tp @s ^ ^ ^0.85',
                          'execute if score @s bm.mt matches 1..6 run tp @s ~ ~0.32 ~', 'execute if score @s bm.mt matches 9.. run tp @s ~ ~-0.32 ~',
                          'particle minecraft:dust{color:[0.55,0.95,0.2],scale:1.2} ~ ~ ~ 0.1 0.1 0.1 0 2', 'particle minecraft:item_slime ~ ~ ~ 0.1 0.1 0.1 0 1',
                          f'execute unless entity @s[tag=bm.bxgm] if entity {hit_p} run return run function bm:{P}/glob/hit',
                          f'execute if entity @s[tag=bm.bxgm] if entity {hit_m} run return run function bm:{P}/glob/hit',
                          f'execute unless block ~ ~ ~ #minecraft:replaceable run return run function bm:{P}/glob/hit',
                          f'execute if score @s bm.mt matches 40.. run function bm:{P}/glob/hit'])
    cloud = {'Radius': F(1.6), 'Duration': Int(60), 'WaitTime': Int(0), 'RadiusPerTick': F(0), 'ReapplicationDelay': Int(20), 'Tags': ['bm.bxacid'],
             'potion_contents': {'custom_color': Int(0x8ad024), 'custom_effects': [{'id': 'minecraft:slowness', 'amplifier': B(1), 'duration': Int(40)},
                                                                                   {'id': 'minecraft:poison', 'amplifier': B(0), 'duration': Int(40)}]}}
    fn(f'{P}/glob/hit', [f'execute unless entity @s[tag=bm.bxgm] as @a[distance=..1.8,{FOES}] run damage @s {SPIT_DMG} minecraft:mob_attack',
                         f'execute unless entity @s[tag=bm.bxgm] run effect give @a[distance=..1.8,{FOES}] minecraft:poison 3 1',
                         f'execute if entity @s[tag=bm.bxgm] as @e[{BOUND.MON},distance=..1.8] run damage @s {SPIT_DMG + 4} minecraft:mob_attack',
                         'execute align y run summon minecraft:area_effect_cloud ~ ~ ~ ' + snbt(cloud),
                         'particle minecraft:item_slime ~ ~0.2 ~ 0.6 0.2 0.6 0.1 24', 'particle minecraft:dust{color:[0.55,0.95,0.2],scale:1.6} ~ ~0.2 ~ 0.8 0.1 0.8 0 16',
                         'playsound minecraft:entity.slime.squish hostile @a[distance=..20] ~ ~ ~ 1.2 0.6', 'playsound minecraft:block.lava.extinguish hostile @a[distance=..20] ~ ~ ~ 0.6 1.6',
                         'kill @s'])
    # ---- the bound one spits at the monsters out of its reach
    fn(f'{P}/t/spit0', ['scoreboard players set @s bm.ms 8', 'scoreboard players set @s bm.mt 0',
                        f'execute facing entity @e[{BOUND.MON},distance=..{SPIT_REACH + 2},sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0',
                        f'function bm:{P}/pose/spit_0'])
    tgt_m = f'@e[{BOUND.MON},distance=..{SPIT_REACH + 4},sort=nearest,limit=1]'
    fn(f'{P}/t/spit', [at(10, f'function bm:{P}/pose/spit_1'), at(11, snd('lash', 1.0, 1.4)),
                       at(11, f'execute if entity {tgt_m} positioned ^ ^4.4 ^2.2 run function bm:{P}/glob/newm'),
                       at(11, f'execute as @e[type=minecraft:item_display,tag=bm.bxgn,distance=..6] at @s run tp @s ~ ~ ~ facing entity {tgt_m} feet'),
                       at(11, 'tag @e[type=minecraft:item_display,tag=bm.bxgn] remove bm.bxgn'),
                       at(30, 'scoreboard players set @s bm.ms 2'), at(30, 'scoreboard players set @s bm.ma 0'), at(30, 'scoreboard players set @s bm.mt 0')])
    # (the tick's ms 8: a wild one's spit, or a bound one's)
    G.FUNCS[f'{P}/s/spit'].insert(0, f'execute if entity @s[tag=bm.bxtame] run return run function bm:{P}/t/spit')

    # ================================================================== THE BROODLINGS: worn to half, three burst out of its cysts
    ling = {'Tags': ['bm.bxling', 'bm.bxlnew', 'bm.seen', 'bm.dgmob'], 'Size': Int(0), 'CustomName': T('Broodling', GREEN), 'DeathLootTable': 'minecraft:empty',
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(6)}, {'id': 'minecraft:attack_damage', 'base': Dd(3)}, {'id': 'minecraft:movement_speed', 'base': Dd(0.45)}],
            'Health': F(6)}
    fn(f'{P}/brood', ['tag @s add bm.bxhalf', snd('shriek', 1.2, 1.7), 'particle minecraft:item_slime ~ ~2 ~ 1 1 1 0.2 40',
                      *[f'summon minecraft:slime ^{x} ^1.5 ^{z} ' + snbt(ling) for x, z in ((1.6, 1.2), (-1.6, 1.0), (0, -1.8))],
                      'scoreboard players operation @e[type=minecraft:slime,tag=bm.bxlnew,distance=..4] bm.mid = @s bm.mid',
                      'tag @e[type=minecraft:slime,tag=bm.bxlnew] remove bm.bxlnew',
                      title('@a[distance=..20]', 'actionbar', T('Its cysts burst - Broodlings!', GREEN, bold=True))])
    fn(f'{P}/ling/pop', ['particle minecraft:item_slime ~ ~0.3 ~ 0.3 0.2 0.3 0.05 10', 'tp @s ~ -400 ~', 'kill @s'])

    # ================================================================== ITS ARRIVAL down a tractor beam (ms 9): balled up, lowered, SPLAT, up
    # (made dormant where it lands, lifted BEAM blocks, lowered a third of a block a tick; at the ground the puddle bursts out, it rises)
    for nm, h in (('hi', BEAM_HI), ('lo', BEAM_LO)):
        fn(f'{P}/beam_{nm}', [f'function bm:{P}/spawn', f'execute as @e[type=minecraft:husk,tag=bm.bmire,distance=..1,limit=1,sort=nearest] at @s run function bm:{P}/beam0_{nm}'])
        fn(f'{P}/beam0_{nm}', ['scoreboard players set @s bm.ms 9', 'scoreboard players set @s bm.mt 0', f'scoreboard players set @s bm.mc {h * 3}', 'tag @s add bm.mme',
                               f'function bm:{P}/mine', f'function bm:{P}/pose/beam', 'tag @e[type=minecraft:item_display,tag=bm.msel] remove bm.msel', 'tag @s remove bm.mme',
                               f'tp @s ~ ~{h} ~', 'playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.2 1.4',
                               'playsound minecraft:block.end_portal.spawn hostile @a[distance=..48] ~ ~ ~ 0.4 1.8'])
    fn(f'{P}/s/beam', ['tp @s ~ ~-0.3333 ~',
                       'particle minecraft:dust{color:[0.55,1.0,0.3],scale:2.0} ~ ~ ~ 1.2 6 1.2 0 14 force @a[distance=..64]',
                       'particle minecraft:end_rod ~ ~ ~ 1 5 1 0.02 3 force @a[distance=..64]',
                       'execute if score @s bm.mt = @s bm.mc run function bm:p258/splat'])
    fn(f'{P}/splat', ['scoreboard players set @s bm.ms 1', 'scoreboard players set @s bm.mt 11', f'function bm:{P}/pose/rise_0',
                      snd('rise', 1.6, 0.9), 'playsound minecraft:entity.slime.squish_small hostile @a[distance=..32] ~ ~ ~ 2 0.5',
                      'playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1 1.4',
                      'particle minecraft:item_slime ~ ~0.4 ~ 2 0.2 2 0.2 60', f'particle minecraft:dust{{color:[{CFG.DUST}],scale:2.0}} ~ ~0.4 ~ 2 0.3 2 0 40',
                      CFG.face])

    # ================================================================== where it comes: the outer End (a natural spawn, now and then)
    fn(f'{P}/roll', ['execute unless score #hard bm.cfg matches 1 run return 0', 'execute if score #vfell bm.cfg matches 1 run return 0',
                     'execute unless dimension minecraft:the_end run return 0',
                     'execute store result score #r bm.rng run random value 1..' + str(ROLL), 'execute unless score #r bm.rng matches 1 run return 0',
                     f'execute positioned 0 ~ 0 if entity @s[distance=..{OUTER}] run return 0',
                     'execute if predicate bm:p255/near_armada run return 0',
                     'execute store result score #day bm.rng run time query day',
                     f'execute unless entity @p[distance=..48,{FOES}] run return 0',
                     f'execute as @p[distance=..48,{FOES}] if score @s bm.bxday = #day bm.rng run return 0',
                     f'execute if entity @e[type=minecraft:husk,tag=bm.bmire,distance=..{APART}] run return 0',
                     'execute if entity @a[tag=bm.jam,distance=..48] run return 0',
                     f'execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run function bm:{P}/spawn',
                     'execute unless entity @e[type=minecraft:husk,tag=bm.bmire,distance=..1] run return 0',
                     f'execute as @p[distance=..48,{FOES}] run scoreboard players operation @s bm.bxday = #day bm.rng',
                     'tp @s ~ -400 ~', 'kill @s', 'return 1'])
    skip = {'ghast', 'phantom', 'drowned', 'shulker', 'blaze', 'breeze', 'pillager', 'vindicator', 'piglin_brute'}
    n_init = 0
    for t in list(G.ARMORED) + list(G.UNARMORED):
        if t in skip or f'mobs/init/{t}' not in G.FUNCS: continue
        G.FUNCS[f'mobs/init/{t}'].insert(0, f'execute if dimension minecraft:the_end if score #hard bm.cfg matches 1 unless score #vfell bm.cfg matches 1 '
                                            f'if function bm:{P}/roll run return 0')
        n_init += 1

    # ================================================================== Invasion Nights: one of the invaders' drops
    surge = G.FUNCS['p32/inv/surge']
    k = next(i for i, l in enumerate(surge) if l.startswith('execute store result score #k bm.rng run random value 1..100'))
    surge.insert(k + 1, f'execute if score #k bm.rng matches 1..{INV_PCT} if score #hard bm.cfg matches 1 unless score #vfell bm.cfg matches 1 '
                        f'if function bm:{P}/inv/try run return run kill @e[type=minecraft:marker,tag=bm.vsp]')
    surge.insert(0, 'execute if entity @s[tag=bm.hsc] run return 0')
    fn(f'{P}/inv/try', ['execute store result score #day bm.rng run time query day', 'execute if score @s bm.bxday = #day bm.rng run return 0',
                        'execute store result score #n bm.rng if entity @e[type=minecraft:husk,tag=bm.bmire,tag=!bm.bxtame]', 'execute if score #n bm.rng matches 2.. run return 0',
                        'scoreboard players set #bxok bm.rng 0',
                        f'execute as @e[type=minecraft:marker,tag=bm.vsp,distance=..1,limit=1] rotated as @s positioned ^ ^ ^20 positioned over motion_blocking_no_leaves '
                        f'run function bm:{P}/inv/drop',
                        'execute unless score #bxok bm.rng matches 1 run return 0', 'scoreboard players operation @s bm.bxday = #day bm.rng', 'return 1'])
    fn(f'{P}/inv/drop', ['execute if block ~ ~-1 ~ #minecraft:replaceable run return 0', 'execute unless block ~ ~ ~ #minecraft:air run return 0',
                         'execute if predicate bm:p255/in_box run return 0', f'function bm:{P}/beam_hi',
                         'tag @e[type=minecraft:husk,tag=bm.bmire,distance=..14,sort=nearest,limit=1] add bm.bxinv', 'scoreboard players set #bxok bm.rng 1'])
    G.FUNCS['p32/inv/end'].append(f'execute as @e[type=minecraft:husk,tag=bm.bmire,tag=!bm.bxtame] at @s if dimension minecraft:overworld run function bm:{P}/melt')

    # ================================================================== the Armada: the Bio-Wave's finale, and the rare one aboard
    import p2.armadacfg as AC
    bio = next(n for n, kind in AC.PUZZLES if kind == 'waves')         # (the first wave trial: the Bio-Wave, aboard the Brood-Carrier)
    assert AC.WAVES[bio][0] == 'The Bio-Wave', AC.WAVES[bio][0]
    last = f'p2/armada/pz{bio}_w{len(AC.WAVES[bio][1])}'
    assert last in G.FUNCS, last
    G.FUNCS[last].append(f'execute unless score #vfell bm.cfg matches 1 run function bm:{P}/arm/finale')
    wm = f'bm.wm_armada{bio}'
    fn(f'{P}/arm/finale', ['scoreboard players set #bxok bm.rng 0',
                           f'execute as @e[type=minecraft:marker,tag=bm.pet_wsp,tag=bm.pz{bio},tag=bm.d_armada,distance=..48,sort=random,limit=1] at @s run function bm:{P}/arm/drop',
                           f'execute if score #bxok bm.rng matches 0 at @a[distance=..40,gamemode=!spectator,sort=random,limit=1] positioned ^ ^ ^6 run function bm:{P}/arm/drop'])
    fn(f'{P}/arm/drop', ['execute if score #bxok bm.rng matches 1 run return 0', 'scoreboard players set #dn bm.rng 8', f'function bm:{P}/arm/step'])
    fn(f'{P}/arm/step', [f'execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run return run function bm:{P}/arm/land',
                         'scoreboard players remove #dn bm.rng 1', f'execute if score #dn bm.rng matches 1.. positioned ~ ~-1 ~ run function bm:{P}/arm/step'])
    fn(f'{P}/arm/land', [f'execute align xyz positioned ~0.5 ~ ~0.5 run function bm:{P}/beam_lo', 'scoreboard players set #bxok bm.rng 1',
                         f'execute align xyz positioned ~0.5 ~ ~0.5 as @e[type=minecraft:husk,tag=bm.bmire,distance=..6,sort=nearest,limit=1] run function bm:{P}/arm/wave'])
    fn(f'{P}/arm/wave', ['tag @s add bm.dgmob', 'tag @s add bm.wm', f'tag @s add {wm}', 'data merge entity @s {PersistenceRequired:1b}'])
    second.append(f'execute if score #hard bm.cfg matches 1 unless score #vfell bm.cfg matches 1 in minecraft:the_end if entity @a[{P241.BOX},gamemode=!spectator] '
                  f'run function bm:{P}/arm/try')
    fn(f'{P}/arm/try', [f'execute store result score #r bm.rng run random value 1..{ROAM}', 'execute unless score #r bm.rng matches 1 run return 0',
                        f'execute in minecraft:the_end if entity @e[type=minecraft:husk,tag=bm.bmire,tag=bm.bxroam,{P241.BOX}] run return 0',
                        f'execute in minecraft:the_end as @e[type=minecraft:marker,tag=bm.dgfx,tag=bm.d_armada,sort=random,limit=1] at @s '
                        f'unless entity @a[distance=..20] if function bm:{P}/arm/open run function bm:{P}/arm/lurk'])
    fn(f'{P}/arm/open', ['execute if entity @e[type=minecraft:marker,tag=bm.vaultm,distance=..14] run return 0', 'execute if entity @e[tag=bm.arelic_d,distance=..14] run return 0',
                         'execute unless entity @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_armada,distance=..40] run return 0'] +
       [f'execute as @e[type=minecraft:marker,tag=bm.pz,tag=bm.d_armada,distance=..40,sort=nearest,limit=1] if entity @s[tag=bm.pz{n}] run return 1' for n in ROAM_TRIALS] +
       ['return 0'])
    fn(f'{P}/arm/lurk', ['scoreboard players set #dn bm.rng 16', f'function bm:{P}/arm/lstep'])
    fn(f'{P}/arm/lstep', [f'execute unless block ~ ~-1 ~ #minecraft:replaceable if block ~ ~ ~ #minecraft:replaceable run return run function bm:{P}/arm/lay',
                          'scoreboard players remove #dn bm.rng 1', f'execute if score #dn bm.rng matches 1.. positioned ~ ~-1 ~ run function bm:{P}/arm/lstep'])
    fn(f'{P}/arm/lay', [f'execute align xyz positioned ~0.5 ~ ~0.5 run function bm:{P}/spawn',
                        'execute align xyz positioned ~0.5 ~ ~0.5 as @e[type=minecraft:husk,tag=bm.bmire,distance=..1] run tag @s add bm.bxroam'])

    # ================================================================== a rig whose host is gone (a wave's abort, an unload): gone too
    second.append(f'execute as @e[type=minecraft:item_display,tag=bm.bxr_puddle] at @s unless function bm:{P}/has run function bm:{P}/orphan')
    fn(f'{P}/has', ['scoreboard players operation #me2 bm.mid = @s bm.mid',
                    'execute as @e[type=minecraft:husk,tag=bm.bmire,distance=..16] if score @s bm.mid = #me2 bm.mid run return 1', 'return 0'])
    fn(f'{P}/orphan', ['scoreboard players operation #me bm.mid = @s bm.mid',
                       'execute as @e[type=minecraft:item_display,tag=bm.bxr] if score @s bm.mid = #me bm.mid run kill @s', CFG.LING])

    # ================================================================== the ichor: fed to the Mireling, kneaded into scent, grown into a pod
    fn(f'{P}/ichor/use', [f'execute if predicate bm:p20/sneaking run return run function bm:{P}/ichor/pod',
                          'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                          'scoreboard players set #q bm.rng 0', f'execute if score @s bm.wumireling matches 0.. run function bm:{P}/ml/has8',
                          f'execute if score #q bm.rng matches 0 as @e[type=minecraft:wolf,tag=bm.mlpet,distance=..6] if score @s bm.pid = #me bm.pid run return run function bm:{P}/ml/feed0',
                          f'function bm:{P}/ichor/scent'])
    fn(f'{P}/ml/has8', ['scoreboard players operation #q bm.rng = @s bm.wumireling', f'scoreboard players set #bit bm.rng {2 ** LOOK}',
                        'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng'])
    fn(f'{P}/ml/feed0', [f'execute as @a[limit=1,sort=nearest,distance=..8] if score @s bm.pid = #me bm.pid run function bm:{P}/ml/feed', 'return 1'])
    fn(f'{P}/ml/feed', ['clear @s *[minecraft:custom_data~{bm:"brood_ichor"}] 1', f'function bm:p99/unlock/mireling{LOOK}', f'function bm:{P}/ml/shiny',
                        f'scoreboard players set @s {P99.COS["mireling"]} {LOOK}', 'function bm:p99/mireling_now',
                        'playsound minecraft:entity.generic.drink player @a[distance=..16] ~ ~ ~ 1 0.6', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.6 1.8',
                        'execute at @e[type=minecraft:wolf,tag=bm.mlpet,distance=..8] if score @s bm.pid = #me bm.pid run particle minecraft:item_slime ~ ~0.8 ~ 0.4 0.4 0.4 0.1 30',
                        tellraw('@s', [T('The Mireling: ', '#e0384a', bold=True), T('(it drinks the ichor in one long slurp. Its veins go green. Then, one by one, more eyes blink open.)', '#ffb4a8')]),
                        tellraw('@s', [T(XL.NAME, '#8ad024', bold=True), T(' is in the Mireling\'s wardrobe for good. (Sneak + use its seed to change any time.)', 'gray')])])
    # (Shiny Pearl Brood: the Brood look and the Mireling's own shiny both owned - given when it drinks, and whenever its wardrobe opens)
    fn(f'{P}/ml/shiny', ['scoreboard players operation #q bm.rng = @s bm.wumireling', 'scoreboard players set #bit bm.rng 128',
                         'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #4 bm.rng',
                         'execute unless score #q bm.rng matches 3 run return 0',
                         'scoreboard players operation #q bm.rng = @s bm.wumireling', f'scoreboard players set #bit bm.rng {2 ** SHINY_LOOK}',
                         'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                         'execute if score #q bm.rng matches 1 run return 0', f'function bm:p99/unlock/mireling{SHINY_LOOK}'])
    fn(f'{P}/ichor/scent', ['execute store result score #n bm.rng run clear @s *[minecraft:custom_data~{bm:"brood_ichor"}] 0',
                            'execute if score #n bm.rng matches ..3 run return run ' + say('Four Brood Ichor make a vial of Hive Scent. (Beside your Mireling, it drinks one.)'),
                            'clear @s *[minecraft:custom_data~{bm:"brood_ichor"}] 4', give('hive_scent'),
                            'playsound minecraft:entity.slime.squish player @s ~ ~ ~ 1 0.8', 'playsound minecraft:item.bottle.fill player @s ~ ~ ~ 1 0.7',
                            say('You squeeze the ichor into a vial of Hive Scent.', GREEN)])
    fn(f'{P}/ichor/pod', ['execute store result score #n bm.rng run clear @s *[minecraft:custom_data~{bm:"brood_ichor"}] 0',
                          'execute if score #n bm.rng matches ..15 run return run ' + say('Sixteen Brood Ichor, sneak + used, grow into a Brood Pod.'),
                          'clear @s *[minecraft:custom_data~{bm:"brood_ichor"}] 16', give('brood_pod'),
                          'playsound minecraft:entity.warden.heartbeat player @s ~ ~ ~ 1 1.3', 'particle minecraft:item_slime ~ ~1 ~ 0.3 0.4 0.3 0.05 20',
                          say('The ichor swells, hardens - and a yellow eye opens in it. A Brood Pod.', COL)])
    G.consume_adv('hive_scent', f'bm:{P}/scent')
    fn(f'{P}/scent', ['advancement revoke @s only bm:consume/hive_scent', f'scoreboard players set @s bm.hscent {SCENT}', 'tag @s add bm.hsc',
                      'particle minecraft:item_slime ~ ~1 ~ 0.3 0.6 0.3 0.02 12', 'playsound minecraft:block.beacon.power_select player @s ~ ~ ~ 0.8 1.8',
                      title('@s', 'actionbar', [T('You smell of the hive. ', GREEN, bold=True), T('The Vorn take you for one of their own for 5 minutes.', 'gray')])])
    second.append(f'execute as @a[scores={{bm.hscent=1..}}] run function bm:{P}/scent_sec')
    fn(f'{P}/scent_sec', ['scoreboard players remove @s bm.hscent 1',
                          'execute if score @s bm.hscent matches 30 run ' + title('@s', 'actionbar', T('The Hive Scent is wearing off...', 'gray', italic=True)),
                          'execute if score @s bm.hscent matches 0 run tag @s remove bm.hsc',
                          'execute if score @s bm.hscent matches 0 run ' + title('@s', 'actionbar', T('You smell like yourself again.', GREEN))])
    # (the Vorn's guns pass the scented over: a trooper's and a saucer's target)
    for f_ in ('p32/troop/fire', 'p32/sauc/fire'):
        L_ = G.FUNCS[f_]
        n0 = sum(1 for l in L_ if 'gamemode=!creative]' in l)
        L_[:] = [l.replace('gamemode=!spectator,gamemode=!creative]', 'gamemode=!spectator,gamemode=!creative,tag=!bm.hsc]') for l in L_]
        assert n0 >= 2, (f_, n0)

    # ================================================================== THE BOUND BROOD-MIRE (the Brood Pod)
    MK.bound(G, CFG, BOUND)

    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:interaction,tag=bm.bxtk]', 'kill @e[type=minecraft:item_display,tag=bm.bxr]',
                                       'kill @e[type=minecraft:item_display,tag=bm.bxglob]', 'kill @e[type=minecraft:slime,tag=bm.bxling]',
                                       'execute as @e[type=minecraft:husk,tag=bm.bmire] at @s run tp @s ~ -400 ~']
    fn('admin/broodmire/spawn', [f'execute positioned ^ ^ ^6 run function bm:{P}/spawn'])
    fn('admin/broodmire/beam', [f'execute positioned ^ ^ ^8 positioned over motion_blocking_no_leaves run function bm:{P}/beam_hi'])
    fn('admin/broodmire/kit', [give('brood_ichor', 16), give('hive_scent'), give('brood_pod')])
    return n_init


def late(G):
    """(after phase99, phase201 and phase252) the Mireling's honour takes Brood Ichor for Shadow Remnants; its wardrobe's Brood
    looks say how they're found; its wardrobe opening gives the shiny Brood look to whoever owns both its halves"""
    import phase201 as P201
    fn, title = G.fn, G.title
    rem, ich = P201.trib_pred('shadow_remnant'), P201.trib_pred('brood_ichor')
    patched = 0
    for r in (1, 2, 3):
        name = f'p201/pay/mireling{r}'
        L_ = G.FUNCS.get(name)
        if not L_: continue
        i = next((n for n, l in enumerate(L_) if l == f'execute store result score #c bm.rng run clear @s {rem} 0'), None)
        if i is None: continue
        tn = int(next(l for l in L_ if l.startswith(f'clear @s {rem} ')).split()[-1])
        L_[i:i + 1] = [f'execute store result score #c bm.rng run clear @s {rem} 0', f'execute store result score #mlic bm.rng run clear @s {ich} 0',
                       'scoreboard players set #mlich bm.rng 0',
                       f'execute unless score #c bm.rng matches {tn}.. if score #mlic bm.rng matches {tn}.. run scoreboard players set #mlich bm.rng 1',
                       'execute if score #mlich bm.rng matches 1 run scoreboard players operation #c bm.rng = #mlic bm.rng']
        j = next(n for n, l in enumerate(L_) if l == f'clear @s {rem} {tn}')
        L_[j:j + 1] = [f'execute if score #mlich bm.rng matches 0 run clear @s {rem} {tn}', f'execute if score #mlich bm.rng matches 1 run clear @s {ich} {tn}']
        L_[:] = [l.replace(f'{tn} Shadow Remnant', f'{tn} Shadow Remnants (or Brood Ichor)') if 'Queen Ava asks' in l else l for l in L_]
        patched += 1
    assert patched, 'the Mireling\'s honour asks no Shadow Remnants any more'
    for k, how in ((LOOK, 'feed your Mireling a Brood Ichor (hard mode: a Brood-Mire leaves them).'),
                   (SHINY_LOOK, 'own the Brood look and the Mireling\'s shiny both.')):
        L_ = G.FUNCS[f'p99/pick/mireling{k}']
        i = next(n for n, l in enumerate(L_) if 'is locked - ' in l and 'return run ' in l)        # (phase103 rewrote who sells it; neither sells these)
        L_[i] = L_[i][:L_[i].index('return run ') + len('return run ')] + title('@s', 'actionbar', T(f'{P99.NEW["mireling"][3][k][0]} is locked - {how}', '#8ad024'))
    G.FUNCS['p99/menu/mireling'].insert(0, f'function bm:{PFX}/ml/shiny')


def rp(R):
    A.rp(R)
    XL.rp(R)
