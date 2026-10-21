"""2.85d: HEIST WINS CALL THE RATS, THE NETHER AND END ROOMS PAY IN THEIR OWN COIN, SEVEN NEW FIGHTS.

THE RATS' CALLS (a won heist, every raider, any tier: 4% each - Pearlman's Bell is 5%)
  THE EMBER RAT'S CALL     a little brass whistle that smells of smoke. Blow it in the Nether and the Ember Rat sets up
                           shop nearby, whatever the odds. THE VOID RAT'S CALL does the same for the Void Rat out in the
                           End (beyond the dragon's island, where the Void Rat trades). Nothing is used up if the rat is
                           already out, there's no floor near you, or you're in the wrong place.
THE NETHER AND END ROOMS (won heists)  the heists' Nether room (the BLAZE FORGE) and End room (the VOID GARDEN) pay in the
                           Ember Rat's and the Void Rat's own coin: a heist won after the crew beat the Forge, each raider has a
                           60% chance of 2-4 EMBER SCALES in the haul; after the Garden, the same chance of 2-4 VOID SHARDS.
SEVEN NEW FIGHTS (the fight turns - there were four kinds; now eleven):
  THE STRONGROOM SIEGE (I-V)  safecrackers go for the Teller's strongbox while the guards hold you off. Three waves; the
                           box can take so much - cracked, and it costs a try (and the siege starts again).
  THE SINKING VAULT (II-V) the floor gives way under the fight, a square at a time; down in the hay pit and you're back at
                           the door. Two waves and a captain. The floor mends when it's over.
  THE HOG PENS (I-IV)      vault boars come charging out of their pens; then the Swineherd himself.
  THE CROSSFIRE GALLERY (II-V)  archers on the balconies, the guards below. Ladders at both ends go up.
  THE HALL OF MIRRORS (III-V)  glass everywhere. Guards first, then the Mirror Thief - an illusioner, doubling himself
                           (and, at Tier V, two shard wraiths).
  THE SPIDER LARDER (I-V)  webs and bones. Spiders drop from the ceiling, then cave spiders, then the Broodmother.
  THE FLOODED VAULT (II-V) knee-deep water slows every step; the drowned come up out of it (with tridents from Tier III),
                           then the Drowned Bailiff (and a guardian at Tier V).
  Every new fight bars its door when it starts (a crewmate left at the bars is let through), and starts over if the
  whole crew is knocked out of it.
"""
import random
from items import item, T, TOTEM
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase70_rooms as RM
import phase75 as P75
import phase76_rooms as R6
import phase110 as P110
import phase112 as P112
import phase116 as P116
from phase75_rooms import BASE, wall_glow

GOLD = '#ffcf40'
EMBER, VOID = '#ff7a1a', '#c08bff'
CALL_CHANCE = 4                         # % a won heist, every raider, any tier (each call)
CUR_CHANCE = 60                         # % a raider gets the Forge's / Garden's coin in the haul
rel, relf = RM.rel, P110.relf
FY = RM.FY
W, D = 25, 25

# ================================================================== THE CALLS
item('ember_call', TOTEM, "Ember Rat's Call", EMBER,
     ['A little brass whistle. It smells of smoke.', ('Blow it in the Nether: the Ember Rat', 'blue'), ('sets up shop nearby.', 'blue'),
      ('A heist find.', 'dark_gray')], model='bm:ember_call', stack=16, cat='relic', comps=hold())
item('void_call', TOTEM, "Void Rat's Call", VOID,
     ['A whistle of pale chorus wood. It hums.', ('Blow it in the End (past the dragon\'s isle):', 'blue'), ('the Void Rat sets up shop nearby.', 'blue'),
      ('A heist find.', 'dark_gray')], model='bm:void_call', stack=16, cat='relic', comps=hold())
HOLD['ember_call'] = 'bm:p184/call/ember'
HOLD['void_call'] = 'bm:p184/call/void'


# ================================================================== THE ROOMS (templates)
def _shell():
    return R6.shell()


def siege():
    b = _shell()
    for x in range(9, 16):                                   # the Teller's alcove, north: a gold dais behind low walls
        for z in range(2, 8): b.set(x, FY, z, 'minecraft:gold_block' if (x + z) % 2 else BASE['metal'])
    for x in (9, 15):
        for z in range(2, 8): b.set(x, 4, z, BASE['wall'])
    b.set(12, 4, 4, BASE['metal'])                           # (the strongbox: its pedestal - the Teller stands on it)
    for (x, z) in ((10, 3), (14, 3), (10, 6), (14, 6)): b.set(x, 4, z, 'minecraft:barrel[facing=up]')
    for (x, z) in ((4, 4), (20, 4), (4, 20), (20, 20)):     # the corners the safecrackers come from: grates
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1): b.set(x + dx, FY, z + dz, 'minecraft:iron_trapdoor[half=top,open=false]')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_siege', 'bm.gvnew'])
    return wall_glow(b)


SINK_CELLS = [(x, z) for x in range(2, 21, 3) for z in (1, 4, 7, 15, 18, 21)]      # 3x3 squares that give way (not the runner)


def sink():
    b = _shell()
    for (x0, z0) in SINK_CELLS:
        for x in range(x0, x0 + 3):
            for z in range(z0, z0 + 3):
                if 1 <= x <= 23 and 1 <= z <= 23:
                    b.set(x, 0, z, 'minecraft:hay_block'); b.set(x, 1, z, 'minecraft:air'); b.set(x, 2, z, 'minecraft:air')
                    b.set(x, FY, z, BASE['floor'] if (x + z) % 2 else 'minecraft:cracked_deepslate_tiles' if (x * z) % 7 == 0 else BASE['floor'])
    for x in (2, 22):                                        # props off the squares: dripstone and cracked pillars
        for y in range(4, 8): b.set(x, y, 12 + (2 if x == 2 else -2), BASE['pillar'])
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_sink', 'bm.gvnew'])
    return wall_glow(b)


def pens():
    b = _shell()
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            if not 10 <= z <= 14: b.set(x, FY, z, 'minecraft:mud' if (x + z) % 3 else 'minecraft:packed_mud')
    for (x0, z0) in ((2, 2), (9, 2), (16, 2), (2, 18), (9, 18), (16, 18)):   # six pens, open to the middle
        for x in range(x0, x0 + 6):
            b.set(x, 4, z0 + (4 if z0 < 10 else 0), 'minecraft:spruce_fence')
        for z in range(z0, z0 + 5):
            b.set(x0, 4, z, 'minecraft:spruce_fence'); b.set(x0 + 5, 4, z, 'minecraft:spruce_fence')
        gx = x0 + 2
        for dx in (0, 1): b.set(gx + dx, 4, z0 + (4 if z0 < 10 else 0), 'minecraft:air')      # (the gates, left open)
        b.set(x0 + 1, 4, z0 + (1 if z0 < 10 else 3), 'minecraft:hay_block'); b.set(x0 + 4, 4, z0 + (1 if z0 < 10 else 3), 'minecraft:composter')
    for x in range(8, 17, 4):                                # the troughs along the runner
        b.set(x, 4, 9, 'minecraft:cauldron'); b.set(x, 4, 15, 'minecraft:cauldron')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_pens', 'bm.gvnew'])
    return wall_glow(b)


GAL_Y = 8                                                    # the balconies' floor (archers stand at 9)


def crossfire():
    b = _shell()
    for x in range(2, 23):                                   # balconies down both long walls, a rail along their edge
        for z in (1, 2, 3, 21, 22, 23):
            b.set(x, GAL_Y, z, BASE['slab'] + '[type=top]')
        b.set(x, GAL_Y + 1, 4, 'minecraft:dark_oak_fence'); b.set(x, GAL_Y + 1, 20, 'minecraft:dark_oak_fence')
    for x in (3, 21):                                        # (the ladders' backs: a pier under each end) and the ladders
        for y in range(4, GAL_Y + 1):
            b.set(x, y, 3, BASE['pillar']); b.set(x, y, 21, BASE['pillar'])
            b.set(x, y, 4, 'minecraft:ladder[facing=south]'); b.set(x, y, 20, 'minecraft:ladder[facing=north]')
        b.set(x, GAL_Y + 1, 4, 'minecraft:air'); b.set(x, GAL_Y + 1, 20, 'minecraft:air')
    for x in range(5, 21, 5):                                # arrow slits and targets on the walls
        b.set(x, 11, 0, 'minecraft:target'); b.set(x, 11, D - 1, 'minecraft:target')
    for (x, z) in ((7, 8), (17, 8), (7, 16), (17, 16)):      # cover below: stacked crates
        b.set(x, 4, z, 'minecraft:barrel[facing=up]'); b.set(x, 5, z, 'minecraft:barrel[facing=up]'); b.set(x + 1, 4, z, 'minecraft:barrel[facing=up]')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_crossfire', 'bm.gvnew'])
    return wall_glow(b)


def mirror():
    b = _shell()
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            if not 10 <= z <= 14: b.set(x, FY, z, 'minecraft:polished_diorite' if (x + z) % 2 else 'minecraft:calcite')
    for y in range(4, 9):                                    # the walls: mirror panes in gold frames
        for x in range(2, 23):
            for z in (0, D - 1):
                b.set(x, y, z, 'minecraft:light_blue_stained_glass' if x % 4 else 'minecraft:gold_block')
    for (x, z) in ((6, 5), (12, 6), (18, 5), (6, 19), (12, 18), (18, 19), (9, 9), (15, 15), (9, 15), (15, 9)):   # free-standing mirrors
        for y in range(4, 7): b.set(x, y, z, 'minecraft:glass' if y < 6 else 'minecraft:tinted_glass')
        b.set(x, 7, z, 'minecraft:amethyst_cluster[facing=up]')
    for x in range(3, 22, 6):
        for z in (3, 21): b.set(x, 14, z, 'minecraft:end_rod[facing=down]')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_mirror', 'bm.gvnew'])
    return wall_glow(b)


def larder():
    b = _shell()
    rnd = random.Random(1849)
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            if 10 <= z <= 14: continue
            r = rnd.random()
            if r < 0.10: b.set(x, 4, z, 'minecraft:cobweb')
            elif r < 0.14: b.set(x, 4, z, 'minecraft:bone_block[axis=y]')
            if rnd.random() < 0.18: b.set(x, 14, z, 'minecraft:cobweb')
    for (x, z) in ((6, 6), (18, 6), (6, 18), (18, 18), (12, 4), (12, 20)):   # the holes they drop from, webbed round
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1): b.set(x + dx, 13, z + dz, 'minecraft:cobweb')
    for (x, z) in ((4, 8), (20, 16), (8, 20), (16, 4)):     # wrapped bundles: hay in webs
        b.set(x, 4, z, 'minecraft:hay_block'); b.set(x, 5, z, 'minecraft:cobweb')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_larder', 'bm.gvnew'])
    return wall_glow(b)


def flood():
    b = _shell()
    for x in range(1, W - 1):
        for z in range(1, D - 1):
            b.set(x, 2, z, 'minecraft:prismarine_bricks' if (x + z) % 2 else 'minecraft:dark_prismarine')
            b.set(x, FY, z, 'minecraft:water')
    for x in range(1, W - 1):                                # (the doors stay dry: a step down into it)
        for z in (11, 12, 13):
            for xx in (1, 23): b.set(xx, FY, z, BASE['floor'])
    rnd = random.Random(1850)
    for _ in range(30):
        x, z = rnd.randint(2, 22), rnd.randint(2, 22)
        if not 10 <= z <= 14: b.set(x, FY, z, 'minecraft:sea_pickle[pickles=3,waterlogged=true]' if rnd.random() < 0.4 else 'minecraft:seagrass')
    for (x, z) in ((6, 6), (18, 6), (6, 18), (18, 18)):     # sunken pillars, lanterns hung over the water
        for y in range(3, 9): b.set(x, y, z, 'minecraft:prismarine')
        b.set(x, 13, z, 'minecraft:sea_lantern')
    b.marker(*RM.CTRL, ['bm.gvr', 'bm.gvr_flood', 'bm.gvnew'])
    return b


ROOMS = {'siege': siege, 'sink': sink, 'pens': pens, 'crossfire': crossfire, 'mirror': mirror, 'larder': larder, 'flood': flood}
NAMES = {'siege': 'The Strongroom Siege', 'sink': 'The Sinking Vault', 'pens': 'The Hog Pens', 'crossfire': 'The Crossfire Gallery',
         'mirror': 'The Hall of Mirrors', 'larder': 'The Spider Larder', 'flood': 'The Flooded Vault'}
TIERS = {'siege': range(1, 6), 'sink': range(2, 6), 'pens': range(1, 5), 'crossfire': range(2, 6), 'mirror': range(3, 6),
         'larder': range(1, 6), 'flood': range(2, 6)}
for _k, _f in ROOMS.items():
    assert _k not in P75.EXTRA_ROOMS and _k not in P75.KINDS, _k          # (a key of its own: 'gallery' is the Shooting Gallery's)
    P75.EXTRA_ROOMS[_k] = _f
    R6.NAMES[_k] = NAMES[_k]
    for _t in TIERS[_k]:
        P75.TIER_POOL[_t].append(_k)
    P116.GROUP[_k] = 4 if _k == 'sink' else 1               # (the curses a room can carry: a fight's, or the Sky Isles' for the floor that drops)
P75.KINDS += list(ROOMS)
P112.FIGHTS += list(ROOMS)
assert len(P75.KINDS) <= 30, len(P75.KINDS)                  # (the layout's 'not twice' bits live in one score)


def generate(G):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    label, sign, vbutton, press, themed, crew_say, oops, choose = P110.helpers(G)
    P = [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    inst = lambda f: f'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng run function {f}'
    pot = lambda n: [f'scoreboard players set #c bm.rng {n}', inst('bm:p75/pot_add')]
    crew = '@a[tag=bm.gvp,distance=..30]'
    mk = P75._mob
    objs = ['bm.gvemb', 'bm.gvvsh']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + ['scoreboard players set #10 bm.rng 10']
    G.OBJECTIVES += objs

    def big(t_, sub, col):
        return [f'title {crew} times 5 40 10', title(crew, 'title', T(t_, col, bold=True)), title(crew, 'subtitle', T(sub, 'gray'))]

    # ================================================================== THE CALLS
    import phase22 as P22
    for k, iid, dim, name, col, ok in (('ember', 'ember_call', 'the Nether', 'Ember Rat', EMBER, 'execute if dimension minecraft:the_nether'),
                                       ('void', 'void_call', 'the End', 'Void Rat', VOID,
                                        f'execute if dimension minecraft:the_end unless entity @s[x=-{P22.END_SAFE},y=-64,z=-{P22.END_SAFE},dx={P22.END_SAFE * 2},dy=448,dz={P22.END_SAFE * 2}]')):
        where = 'Blow it in the Nether.' if k == 'ember' else 'Blow it out in the End, past the dragon\'s island.'
        fn(f'p184/call/{k}', [f'{ok} run return run function bm:p184/call/{k}_go', say(f'Nothing answers here. {where}', col)])
        fn(f'p184/call/{k}_go', [f'execute if entity @e[type=minecraft:wandering_trader,tag=bm.frat_{k}] run return run ' +
                                 tellraw('@s', P + [T(f'The {name} ', col, bold=True), T('is already out trading - follow the ' + ('sparks.' if k == 'ember' else 'purple motes.'), 'gray')]),
                                 'playsound minecraft:entity.breeze.whirl player @a[distance=..24] ~ ~ ~ 1 1.8',
                                 f'function bm:p22/rat/spawn_{k}',
                                 'execute if score #frok bm.rng matches 0 run return run ' + say('No answer - there\'s no floor near enough for a stall. Try somewhere more open.', col),
                                 f'execute unless entity @s[gamemode=creative] run clear @s *[minecraft:custom_data~{{bm:"{iid}"}}] 1'])
    HA, HB = '-200 64 -197', '-198 64 -197'                  # (the haul barrels - as Pearlman's Bell)
    ins = lambda table: [f'execute in bm:gutter unless data block {HA} Items[26] run loot insert {HA} loot {table}',
                         f'execute in bm:gutter if data block {HA} Items[26] run loot insert {HB} loot {table}']
    G.wjson('bm/loot_table/p184/ember_call.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('ember_call')]}]})
    G.wjson('bm/loot_table/p184/void_call.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('void_call')]}]})
    G.wjson('bm/loot_table/p184/ember_scales.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('ember_scale', G.uni(2, 4))]}]})
    G.wjson('bm/loot_table/p184/void_shards.json', {'type': 'minecraft:chest', 'pools': [{'rolls': 1, 'entries': [G.loot_entry('void_shard', G.uni(2, 4))]}]})
    tag_ = lambda what, col: tellraw('@s', [T('[', 'dark_gray'), T('Heist', GOLD, bold=True), T('] ', 'dark_gray'), T('Rare find! ', '#5ab0ff', bold=True),
                                            T(what, col, bold=True), T(' in your haul.', 'gray')])
    G.FUNCS['p105/finds'] += ['execute store result score #r bm.rng run random value 1..100',
                              f'execute if score #r bm.rng matches ..{CALL_CHANCE} run function bm:p184/find/ember_call',
                              'execute store result score #r bm.rng run random value 1..100',
                              f'execute if score #r bm.rng matches ..{CALL_CHANCE} run function bm:p184/find/void_call',
                              # (the Nether's and the End's rooms: their own coin, for a raider who saw them beaten this run)
                              'execute store result score #r bm.rng run random value 1..100',
                              f'execute if score @s bm.gvemb = @s bm.gvrun if score #r bm.rng matches ..{CUR_CHANCE} run function bm:p184/find/ember',
                              'execute store result score #r bm.rng run random value 1..100',
                              f'execute if score @s bm.gvvsh = @s bm.gvrun if score #r bm.rng matches ..{CUR_CHANCE} run function bm:p184/find/void']
    fn('p184/find/ember_call', ins('bm:p184/ember_call') + [tag_("Ember Rat's Call", EMBER), 'playsound minecraft:entity.breeze.whirl player @s ~ ~ ~ 0.8 1.8'])
    fn('p184/find/void_call', ins('bm:p184/void_call') + [tag_("Void Rat's Call", VOID), 'playsound minecraft:entity.breeze.whirl player @s ~ ~ ~ 0.8 1.4'])
    fn('p184/find/ember', ins('bm:p184/ember_scales') + [tellraw('@s', P + [T('Ember Scales ', EMBER, bold=True), T('from the Blaze Forge in your haul - the Ember Rat\'s coin, for his trades in the Nether.', 'gray')])])
    fn('p184/find/void', ins('bm:p184/void_shards') + [tellraw('@s', P + [T('Void Shards ', VOID, bold=True), T('from the Void Garden in your haul - the Void Rat\'s coin, for his trades in the End.', 'gray')])])
    for room, sc_ in (('forge', 'bm.gvemb'), ('voidg', 'bm.gvvsh')):
        G.FUNCS[f'p90/{room}/done'].insert(0, f'execute as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run scoreboard players operation @s {sc_} = @s bm.gvrun')
    fn('admin/rat_calls', [give('ember_call'), give('void_call')])

    # ================================================================== THE FIGHTS: one skeleton
    # (the marker's own scores: bm.gvs 0 waiting, 1 fighting, 2 done (3 once solved); bm.gvw the wave; bm.gvh seconds with
    #  nobody of the crew inside - ten and the fight starts over)
    G.FUNCS['p70/r/init'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p184/{k}/init' for k in ROOMS]
    G.FUNCS['p70/r/tick'] += [f'execute if entity @s[tag=bm.gvr_{k}] run return run function bm:p184/{k}/tick' for k in ROOMS]
    k0 = next(i for i, l in enumerate(G.FUNCS['p70/r/init']) if 'tag @s add bm.gvnopick' in l)
    G.FUNCS['p70/r/init'][k0:k0] = [f'execute if entity @s[tag=bm.gvr_{k}] run tag @s add bm.gvnopick' for k in ROOMS]
    G.FUNCS['p70/solved'] += [f'execute if entity @s[tag=bm.gvr_{k}] as @a[tag=bm.gvp,distance=..300] if score @s bm.gvi = #gi bm.rng run ' +
                              title('@s', 'actionbar', [T(NAMES[k], GOLD, bold=True), T(' - won. The way on is open.', 'gray')]) for k in ROOMS]
    bar_on = [f'fill {rel(0, 4, 11)} {rel(0, 7, 13)} minecraft:iron_bars',             # (as the Arcane Study: the doorway is open by build)
               f'playsound minecraft:block.iron_door.close block @a[distance=..30] {rel(0, 5, 12)} 1 0.5']
    bar_off = [f'fill {rel(0, 4, 11)} {rel(0, 7, 13)} minecraft:air replace minecraft:iron_bars']

    def guards(spots, cap=7, extra=0):
        """roster guards: one a raider and one a tier (and `extra`), up to `cap`, at the spots"""
        return ['function bm:p70/ctx', 'execute store result score #n bm.rng if entity @a[tag=bm.gvp,distance=..24]', 'scoreboard players operation #n bm.rng += #gt bm.rng',
                f'scoreboard players add #n bm.rng {extra}', f'execute if score #n bm.rng matches {cap + 1}.. run scoreboard players set #n bm.rng {cap}'] + \
               [f'execute if score #n bm.rng matches {i + 1}.. positioned {rel(spots[i % len(spots)][0], spots[i % len(spots)][1] if len(spots[i % len(spots)]) == 3 else 4, spots[i % len(spots)][-1])} run function bm:p70/guard'
                for i in range(cap)]

    def mob(ty, nbt, x, z, y=4, cond=''):
        p_ = f'positioned {rel(x, y, z)}'
        return [f'execute {cond}{p_} run summon minecraft:{ty} ~ ~ ~ {snbt(nbt)}', f'execute {cond}{p_} run function bm:p70/guard_set']

    def fight(k, title_, body, col, waves, *, spring=(), second=(), reset=(), done=(), tick=(), win_t='THE WAY IS OPEN', win_sub='', reward=8):
        fn(f'p184/{k}/init', ['function bm:p70/ctx', sign(relf(2.5, 7.5, 12.5), title_, body, col=col)])
        fn(f'p184/{k}/tick', ['execute if score @s bm.gvs matches 2.. run return 0',
                              f'execute if score @s bm.gvs matches 0 positioned {rel(3, 4, 1)} if entity @a[tag=bm.gvp,dx=19,dy=5,dz=22] at @s run function bm:p184/{k}/spring',   # (back at the marker: the spring's places are the room's)
                              'execute unless score @s bm.gvs matches 1 run return 0'] + list(tick) + [
                              'scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players operation #q bm.rng %= #20 bm.rng',
                              f'execute if score #q bm.rng matches 0 run function bm:p184/{k}/second'])
        fn(f'p184/{k}/spring', ['scoreboard players set @s bm.gvs 1', 'scoreboard players set @s bm.gvtm 0', 'scoreboard players set @s bm.gvh 0',
                                'scoreboard players set @s bm.gvw 1', 'function bm:p70/ctx'] + bar_on + big(title_, waves[0][1], col) + list(spring) +
           [f'function bm:p184/{k}/w1'])
        fn(f'p184/{k}/second', ['function bm:p70/ctx', 'execute unless entity @a[tag=bm.gvp,distance=..16] run scoreboard players add @s bm.gvh 1',
                                'execute if entity @a[tag=bm.gvp,distance=..16] run scoreboard players set @s bm.gvh 0',
                                f'execute if score @s bm.gvh matches 10.. run return run function bm:p184/{k}/rearm'] + list(second) + [
                                'execute unless score @s bm.gvs matches 1 run return 0',
                                'execute store result score #n bm.rng if entity @e[tag=bm.gvg,distance=..22]', 'execute if score #n bm.rng matches 1.. run return 0',
                                f'execute if score @s bm.gvw matches {len(waves)}.. run return run function bm:p184/{k}/done',
                                'scoreboard players add @s bm.gvw 1'] +
           [f'execute if score @s bm.gvw matches {i + 1} run function bm:p184/{k}/w{i + 1}' for i in range(1, len(waves))])
        for i, (lines, sub) in enumerate(waves):
            fn(f'p184/{k}/w{i + 1}', ['function bm:p70/ctx'] + lines + ([crew_say(sub, col, 30)] if i else []))
        fn(f'p184/{k}/rearm', ['scoreboard players set @s bm.gvs 0', 'scoreboard players set @s bm.gvw 0', 'scoreboard players set @s bm.gvh 0',
                               'tp @e[tag=bm.gvg,distance=..22] ~ -200 ~', 'kill @e[tag=bm.gvg,distance=..22]'] + bar_off + list(reset))
        fn(f'p184/{k}/done', ['scoreboard players set @s bm.gvs 2'] + bar_off + list(reset) + list(done) + pot(reward) + big(win_t, win_sub or f'{NAMES[k]} is yours.', col) +
           ['function bm:p70/solved'])

    # ---- THE STRONGROOM SIEGE
    SC = [(4, 4), (20, 4), (4, 20), (20, 20)]
    teller = {'Tags': ['bm.gvprop', 'bm.gvteller'], 'NoAI': B(1), 'Invulnerable': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
              'CustomName': T('The Teller', GOLD), 'CustomNameVisible': B(1), 'VillagerData': {'type': 'minecraft:plains', 'profession': 'minecraft:nitwit', 'level': Int(1)}}
    cracker = lambda nm: mk('vindicator', nm, '#c0a060', {'head': 'minecraft:leather_helmet', 'mainhand': 'minecraft:iron_pickaxe'},
                            {'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvsc']})
    BOX_P = (12, 5, 4)
    hp_txt = [f'execute if score #p bm.rng matches {i} run data modify entity @e[type=minecraft:text_display,tag=bm.gvsbox,distance=..16,limit=1] text set value ' +
              snbt([T('STRONGBOX\n', GOLD, bold=True), T('▮' * i, '#ffd040'), T('▯' * (10 - i), '#5a4a20')]) for i in range(11)]
    siege_waves = []
    for w in range(3):
        n_cr = 2 + w
        siege_waves.append((guards([(12, 18), (6, 12), (18, 12), (12, 20)], cap=5) +
                            sum((mob(*cracker('Safecracker'), *SC[(i + w) % 4]) for i in range(n_cr)), []) +
                            ['execute if score #gt bm.rng matches 3.. run ' + l for l in mob(*cracker('Master Safecracker'), *SC[w % 4])],
                            ('Safecrackers! Keep them off the strongbox!' if w == 0 else ('More of them at the grates!' if w == 1 else 'The last of them - hold!'))))
    fight('siege', 'THE STRONGROOM SIEGE', 'The Teller\'s strongbox is worth more than you. Keep the safecrackers off it.', '#ffd040', siege_waves,
          spring=['scoreboard players operation @s bm.gvc = #gt bm.rng', 'scoreboard players operation @s bm.gvc *= #8 bm.rng', 'scoreboard players add @s bm.gvc 20',
                  'scoreboard players operation @s bm.gvx = @s bm.gvc', 'function bm:p184/siege/bar'],
          second=[f'execute positioned {rel(*BOX_P)} store result score #n bm.rng if entity @e[tag=bm.gvsc,distance=..2.6]',
                  'scoreboard players operation @s bm.gvc -= #n bm.rng',
                  f'execute if score #n bm.rng matches 1.. run playsound minecraft:block.chain.hit block @a[distance=..30] {rel(*BOX_P)} 1 0.6',
                  f'execute if score #n bm.rng matches 1.. run particle minecraft:crit {rel(*BOX_P)} 0.4 0.4 0.4 0.2 8',
                  'function bm:p184/siege/bar', 'execute if score @s bm.gvc matches ..0 run function bm:p184/siege/cracked'],
          reset=[], done=['kill @e[type=minecraft:text_display,tag=bm.gvsbox,distance=..16]'], win_t='THE STRONGBOX HOLDS', win_sub='The Teller tips his hat.')
    G.FUNCS['p184/siege/init'] = ['function bm:p70/ctx', sign(relf(2.5, 7.5, 12.5), 'THE STRONGROOM SIEGE', 'The Teller\'s strongbox is worth more than you. Keep the safecrackers off it.', col='#ffd040'),
                                  f'summon minecraft:villager {rel(12, 5, 4)} {snbt(teller)}',
                                  label(relf(12.5, 7.4, 4.5), [T('STRONGBOX\n', GOLD, bold=True), T('▮' * 10, '#ffd040')], 0.6, 'center', ('bm.gvsbox',))]
    fn('p184/siege/bar', ['scoreboard players operation #p bm.rng = @s bm.gvc', 'scoreboard players operation #p bm.rng *= #10 bm.rng',
                          'scoreboard players operation #p bm.rng /= @s bm.gvx', 'execute if score #p bm.rng matches ..-1 run scoreboard players set #p bm.rng 0'] + hp_txt)
    fn('p184/siege/cracked', [f'particle minecraft:explosion {rel(*BOX_P)} 0.3 0.3 0.3 0 3', f'playsound minecraft:entity.zombie.break_wooden_door block @a[distance=..30] {rel(*BOX_P)} 1 0.6',
                              'execute as @e[type=minecraft:marker,tag=bm.gvinst] if score @s bm.gvi = #gi bm.rng at @s run function bm:p90/lose_try', 'function bm:p184/siege/rearm', 'scoreboard players operation @s bm.gvc = @s bm.gvx', 'function bm:p184/siege/bar'] +
       big('THE STRONGBOX IS CRACKED', 'That cost a try. They\'re coming again.', '#ff5a5a'))

    # ---- THE SINKING VAULT
    fn('p184/sink/init_cells', [f'summon minecraft:marker {rel(x0 + 1, FY, z0 + 1)} {{Tags:["bm.gvprop","bm.gvsk"]}}' for (x0, z0) in SINK_CELLS])
    fight('sink', 'THE SINKING VAULT', 'Old floor, heavy boots. It won\'t hold for long - and down there is a long way back.', '#c0a070',
          [(guards([(6, 12), (18, 12), (12, 6), (12, 18)], cap=6), 'The floor groans...'),
           (guards([(6, 12), (18, 12), (12, 6), (12, 18)], cap=6) + [f'execute positioned {rel(18, 4, 12)} run function bm:p70/captain'], 'More - and their captain!')],
          spring=['execute unless entity @e[type=minecraft:marker,tag=bm.gvsk,distance=..20] run function bm:p184/sink/init_cells'],
          second=['scoreboard players operation #q bm.rng = @s bm.gvtm', 'scoreboard players set #k bm.rng 60',
                  'execute if score #gt bm.rng matches 4.. run scoreboard players set #k bm.rng 40', 'scoreboard players operation #q bm.rng %= #k bm.rng',
                  'execute as @e[type=minecraft:marker,tag=bm.gvsk,tag=bm.gvskc,distance=..20] at @s run function bm:p184/sink/drop',
                  'execute if score #q bm.rng matches 0 as @e[type=minecraft:marker,tag=bm.gvsk,tag=!bm.gvskb,distance=..20,sort=random,limit=1] at @s run function bm:p184/sink/crack'],
          tick=[f'execute positioned {relf(1, 1, 1)} as @a[tag=bm.gvp,dx=22,dy=2.6,dz=22] at @s run function bm:p184/sink/fell',
                f'execute positioned {relf(1, 1, 1)} as @e[tag=bm.gvg,dx=22,dy=2.6,dz=22] at @s run function bm:p112/isles/gone'],
          reset=['execute as @e[type=minecraft:marker,tag=bm.gvsk,distance=..20] at @s run function bm:p184/sink/mend'], win_t='THE FLOOR HOLDS - JUST')
    fn('p184/sink/crack', ['tag @s add bm.gvskc', 'fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:cracked_deepslate_tiles',
                           'playsound minecraft:block.deepslate.break block @a[distance=..20] ~ ~1 ~ 1 0.5', 'particle minecraft:block{block_state:"minecraft:deepslate"} ~ ~1 ~ 1 0.1 1 0 20'])
    fn('p184/sink/drop', ['tag @s remove bm.gvskc', 'tag @s add bm.gvskb', 'fill ~-1 ~ ~-1 ~1 ~ ~1 minecraft:air',
                          'playsound minecraft:block.stone.fall block @a[distance=..20] ~ ~ ~ 1 0.5', 'particle minecraft:block{block_state:"minecraft:deepslate"} ~ ~ ~ 1 0.3 1 0 25'])
    fn('p184/sink/mend', ['tag @s remove bm.gvskb', 'tag @s remove bm.gvskc'] + themed('fill ~-1 ~ ~-1 ~1 ~ ~1 {b}', 'floor'))
    fn('p184/sink/fell', ['scoreboard players set #add bm.rng 4', 'execute as @e[type=minecraft:marker,tag=bm.gvr_sink,distance=..30,sort=nearest,limit=1] at @s run function bm:p70/oops',
                          'execute at @e[type=minecraft:marker,tag=bm.gvr_sink,distance=..30,sort=nearest,limit=1] run tp @s ' + rel(1, 4, 12) + ' -90 0',
                          'playsound minecraft:block.grass.fall player @a[distance=..16] ~ ~ ~ 1 0.8', say('Down into the hay! Back to the door.', 'red')])

    # ---- THE HOG PENS
    boar = lambda nm='Vault Boar': mk('hoglin', nm, '#c08060', {}, {'IsImmuneToZombification': B(1), 'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen']}, {'scale': 0.85})
    swine = mk('piglin_brute', 'The Swineherd', '#ff9a6a', {'head': 'minecraft:golden_helmet', 'mainhand': 'minecraft:golden_axe'},
               {'IsImmuneToZombification': B(1), 'CustomNameVisible': B(1), 'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvcap']}, {'scale': 1.2})
    PEN = [(4, 4), (11, 4), (18, 4), (4, 20), (11, 20), (18, 20)]
    fight('pens', 'THE HOG PENS', 'Something snorts behind every gate.', '#e09060',
          [(sum((mob(*boar(), *PEN[i]) for i in range(3)), []) + ['execute if score #gt bm.rng matches 2.. run ' + l for l in mob(*boar(), *PEN[3])], 'The gates burst open!'),
           (sum((mob(*boar(), *PEN[i]) for i in range(2, 5)), []) + guards([(12, 6), (12, 18)], cap=3), 'More boars - and their keepers!'),
           (mob(*swine, 18, 12) + sum((mob(*boar('Prize Boar'), *PEN[i]) for i in (0, 5)), []), 'The Swineherd!')],
          win_t='THE PENS FALL QUIET', reward=8)

    # ---- THE CROSSFIRE GALLERY
    archer = lambda: mk('skeleton', 'Gallery Archer', '#d0c8b0', {'head': 'minecraft:chainmail_helmet', 'mainhand': 'minecraft:bow'})
    BAL = [(6, 2), (12, 2), (18, 2), (6, 22), (12, 22), (18, 22)]
    arch = lambda idx, cond='': sum((mob(*archer(), x, z, GAL_Y + 1, cond) for (x, z) in [BAL[i] for i in idx]), [])
    fight('crossfire', 'THE CROSSFIRE GALLERY', 'Archers up on the balconies. The ladders at either end go up to them.', '#d0c8b0',
          [(arch([0, 3]) + arch([1, 4], 'if score #gt bm.rng matches 3.. ') + guards([(10, 12), (14, 12), (12, 8), (12, 16)], cap=4), 'Up on the balconies - archers!'),
           (arch([1, 2, 4, 5]) + guards([(10, 12), (14, 12), (12, 8), (12, 16)], cap=5) + [f'execute positioned {rel(18, 4, 12)} run function bm:p70/captain'], 'A fresh volley - and a captain below!')],
          win_t='THE GALLERY IS CLEARED')

    # ---- THE HALL OF MIRRORS
    thief = mk('illusioner', 'The Mirror Thief', '#9ad0ff', {'mainhand': 'minecraft:bow'},
               {'CustomNameVisible': B(1), 'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvcap']})
    wraith = mk('vex', 'Shard Wraith', '#c0e8ff', {'mainhand': 'minecraft:iron_sword'})
    fight('mirror', 'THE HALL OF MIRRORS', 'Which of you is the real one? Which of HIM is?', '#9ad0ff',
          [(guards([(6, 12), (18, 12), (12, 6), (12, 18)], cap=6), 'Something moves in every mirror...'),
           (mob(*thief, 12, 12) + ['execute if score #gt bm.rng matches 5 run ' + l for l in mob(*wraith, 8, 8, 6) + mob(*wraith, 16, 16, 6)] +
            ['execute as @a[tag=bm.gvp,distance=..20] run effect give @s minecraft:blindness 2 0 true', f'particle minecraft:end_rod {rel(12, 6, 12)} 2 2 2 0.1 60',
             f'playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..30] {rel(12, 5, 12)} 1 0.8'], 'The Mirror Thief steps out of the glass!')],
          win_t='THE MIRRORS CRACK', win_sub='Only you look back now.')

    # ---- THE SPIDER LARDER
    spider = lambda nm='Larder Spider': mk('spider', nm, '#a08070', {})
    cave = lambda: mk('cave_spider', 'Larder Biter', '#4080a0', {})
    brood = mk('spider', 'The Broodmother', '#a0ff80', {}, {'CustomNameVisible': B(1), 'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvcap']}, {'scale': 2.2})
    HOLE = [(6, 6), (18, 6), (6, 18), (18, 18), (12, 4), (12, 20)]
    drop = lambda f, idx, cond='': sum((mob(*f(), *HOLE[i], 11, cond) for i in idx), [])
    fight('larder', 'THE SPIDER LARDER', 'Don\'t look up.', '#a0ff80',
          [(drop(spider, [0, 1, 2]) + drop(spider, [3], 'if score #gt bm.rng matches 2.. '), 'They drop from the ceiling!'),
           (drop(spider, [0, 3]) + drop(cave, [1, 2]) + drop(cave, [4, 5], 'if score #gt bm.rng matches 3.. '), 'Biters - mind the poison!'),
           (mob(*brood, 12, 18) + drop(cave, [0, 1], 'if score #gt bm.rng matches 3.. '), 'The Broodmother!')],
          spring=[f'playsound minecraft:entity.spider.ambient hostile @a[distance=..30] {rel(12, 10, 12)} 1 0.6'], win_t='THE LARDER IS CLEARED')

    # ---- THE FLOODED VAULT
    drowned = lambda nm='Drowned Clerk': mk('drowned', nm, '#5ab0a0', {'mainhand': 'minecraft:iron_shovel'})
    tri = lambda nm='Drowned Harpooner': mk('drowned', nm, '#5ab0a0', {'mainhand': 'minecraft:trident'})
    bailiff = mk('drowned', 'The Drowned Bailiff', '#7ae0d0', {'head': 'minecraft:turtle_helmet', 'mainhand': 'minecraft:trident'},
                 {'CustomNameVisible': B(1), 'Tags': ['bm.gvg', 'bm.gvnew2', 'bm.tiered', 'bm.seen', 'bm.gvcap']}, {'scale': 1.25})
    guardian = mk('guardian', 'Vault Warden', '#7ae0d0', {})
    WET = [(6, 4), (18, 4), (6, 20), (18, 20), (12, 6), (12, 18)]
    wet = lambda f, idx, cond='': sum((mob(*f(), *WET[i], 3, cond) for i in idx), [])
    fight('flood', 'THE FLOODED VAULT', 'Knee-deep, and cold. Something down there is still on duty.', '#5ab0a0',
          [(wet(drowned, [0, 1, 2]) + wet(tri, [3], 'if score #gt bm.rng matches 3.. '), 'They rise out of the water!'),
           (wet(drowned, [4, 5]) + wet(tri, [0, 1], 'if score #gt bm.rng matches 3.. ') + guards([(12, 12)], cap=3), 'More of the drowned!'),
           (mob(*bailiff, 18, 12, 3) + ['execute if score #gt bm.rng matches 5 run ' + l for l in mob(*guardian, 12, 12, 3)], 'The Drowned Bailiff!')],
          win_t='THE WATER GOES STILL')

    # ================================================================== the admin's own (for tests)
    for k in ROOMS:
        fn(f'admin/fight_{k}', [f'scoreboard players set #frk bm.gvv {P75.KINDS.index(k) + 1}',
                                tellraw('@s', P + [T(f'Heists laid from now on are all {NAMES[k]} rooms (admin/rooms_any to stop).', 'gray')])])
    if 'admin/help' in G.FUNCS:
        G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/fight_<siege|sink|pens|crossfire|mirror|larder|flood>', 'yellow'), T('  heists of one new fight room; ', 'gray'),
                                                    T('/function bm:admin/rat_calls', 'yellow'), T('  both rats\' calls', 'gray')]))
    return len(ROOMS)


def rp(R):
    g = R.grid
    R.ICONS['ember_call'] = g(['................', '................', '...........ff...', '..........f..f..', '...........ff...', '.........k......', '........kYk.....',
                               '.......kYyk.....', '......kYyk......', '.....kYyk.......', '....kYyk........', '...kYyk.........', '..kooyk.........', '..kook..........',
                               '...kk...........', '................'],
                              dict(k='#2a1408', Y='#ffd070', y='#c08030', o='#ff7a1a', f='#ff5a10'))
    R.ICONS['void_call'] = g(['................', '................', '...........pp...', '..........p..p..', '...........pp...', '.........k......', '........kWk.....',
                              '.......kWwk.....', '......kWwk......', '.....kWwk.......', '....kWwk........', '...kWwk.........', '..kvvwk.........', '..kvvk..........',
                              '...kk...........', '................'],
                             dict(k='#1a0a24', W='#f0e0ff', w='#b8a0d0', v='#c08bff', p='#e070ff'))
