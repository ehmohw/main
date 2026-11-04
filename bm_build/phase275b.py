"""3.1: THE GOLDEN DOODLE'S FIGHT, and THE CLOVER POND - the Lucky Nights' own boss (phase275 is the follower she becomes).

THE CLOVER POND   a room off the Gilded Roost's Counting House (p2/dungeons/lucky.py): a still golden pond in a ring of clover,
                  a gilded stone - a great golden egg - on its island (the marker bm.gdpond). Three hollows are carved round the
                  stone: a SUN, a THREAD and a CROWN. Right-click the stone: it tells you which hollow is still dark (never who).
                  On a LUCKY NIGHT it shimmers, and it WAKES when one player stands in the ring with their own Lightbringer,
                  Keeper of Bonds and Bound Sovereign out within 12 of it. It rests a full day (24000 ticks) after a win.
PHASE 1, THE JOKE "The Golden Doodle (she is very proud of herself)": an invisible husk host (scale 0.9) wearing the goose's rig;
                  520 health over a hidden FLOOR, under the hit cap. Every 40-60 ticks an attack, never the same twice running:
                  HONK (a cone: 2, slowed), the WADDLE CHARGE (straight at you: 4; into a wall she BONKS and is stunned), the
                  EGG DROP (three golden eggs round you that POP: 2, a coin, 1 in 4 a Lucky Token), the NECK-WHIP SLAP (5), the
                  LUCKY COIN (heads: she's quick and tough for 5 s; tails: everyone near gets Luck II, and she sulks).
THE TURN          pool 1 empty: a 6-second cinematic (the camera as phase238's: held, a 3-tick lease, no Darkness) - she sits,
                  dazed; gets up; waddles to the Bound Sovereign and BITES ITS CROWN. A sliver of the Dread sticks: the morph.
PHASE 2           "THE GILDED ELDRITCH": the host at scale 3.0 wearing the Eldritch rig, 900 health (+300 a fighter after the
                  first), Resistance II, DREAD blows (bm:dread). Every 50-70 ticks: the DREAD BEAM (a sweeping beam from the
                  brow - get behind something, or hold a Lucky Token: it reflects the beam once, used up), the SHRIEK (three
                  rings out to 10: jump them), the WING SLAM (a floor shockwave: jump it), the LUNGE (a 7-block strike), THE
                  UNLUCKY (a black clover sigil under everyone: Unluck - and it heals while you stand on it). ALL IN at a quarter:
                  the coin lands on its EDGE - 12 s untouchable, sigils every second - then it TIRES (7 s): strike it.
THE CURE          pool 2 empty: an 8-second cinematic - the Lightbringer steps in ("Hush, little one. That isn't yours to
                  carry."), her light washes over it, the shard burns away, and the goose is back: HONK. Everyone who fought:
                  the first time, Lucky and Dread Tokens and a Gilded Feather (the off hand: Luck and Slow Falling) - and she
                  joins whoever hasn't met her (the Doodle Egg; out at once if there's room); later wins, tokens and three
                  Scratch Cards.
MUSIC             the Doodle theme (phase152's THEMES 33 / 34 / 35): the kazoo loop, the turn's record-scratch, the minor loop.
                  phase260 keeps it off for anyone who turned the music off (bm.nomus)."""
from items import item, T, TOTEM
from useitem import hold
from nbt import snbt, B, F, Int, D
import rigfol as RF
import goldendoodle_pet_art as QA
import goldendoodle_boss_art as KA
import phase152 as P152

COL, RED, GOLD = '#ffd040', '#d0182e', '#fff0b0'
S1, S2 = 0.9, KA.BOSS_SCALE                 # (her rig's size: the goose phase, the Eldritch)
HOST1, HOST2 = 0.9, 3.0
FLOOR, P1, P2, P2_EXTRA, P2_CAP = 60, 520, 900, 300, 960
CAP = 25
REST = 24000
R1, R2 = QA.R, KA.R
FIGHT = '@a[distance=..32,gamemode=!spectator,gamemode=!creative]'
TGT = '@p[distance=..24,gamemode=!spectator,gamemode=!creative]'
ME = '@e[type=minecraft:husk,tag=bm.gdb,sort=nearest,limit=1]'
HOST = '@e[type=minecraft:husk,tag=bm.gdb]'

P152.THEMES.update({33: ('gdoodle1', 64), 34: ('gdoodle_turn', 6), 35: ('gdoodle2', 64)})
P152.WHO_LATE += [(33, 'type=minecraft:husk,tag=bm.gdb,tag=bm.gdp1'), (35, 'type=minecraft:husk,tag=bm.gdb,tag=bm.gdp2'),
                  (34, 'type=minecraft:husk,tag=bm.gdb,tag=bm.gdturn')]

item('gilded_feather', TOTEM, 'Gilded Feather', COL,
     ['A gold-leaf feather from the Golden Doodle.', ('In your off hand: Luck and Slow Falling.', 'blue'), ('On a Lucky Night: Luck II.', 'blue'),
      ('Taken from the Gilded Eldritch itself.', 'dark_gray')],
     model='minecraft:feather', stack=1, cat='relic', glint=True, comps=hold('none'))


def rp(R):
    pass


def build(G, X, C):
    fn, title, tellraw, give = G.fn, G.title, G.tellraw, G.give
    tick, fast, second = G.FUNCS['tick'], G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = G.PREFIX
    import hitcap
    hitcap.install(G)
    objs = ['bm.gda', 'bm.gdx', 'bm.gdk', 'bm.gdl', 'bm.gdt', 'bm.gdf', 'bm.gdi', 'bm.gdst', 'bm.gdr', 'bm.gdpl']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        f'bossbar add bm:gdoodle {snbt(T("The Golden Doodle", COL, bold=True))}', 'bossbar set bm:gdoodle style notched_10',
        'scoreboard players set #5 bm.rng 5', 'scoreboard players set #10 bm.rng 10', 'scoreboard players set #24 bm.rng 24', 'scoreboard players set #40 bm.rng 40',
        'scoreboard players set #6 bm.rng 6']
    G.OBJECTIVES += objs
    snd = lambda s, v=1.0, p=1.0: f'playsound minecraft:{s} hostile @a[distance=..32] ~ ~ ~ {v} {p}'
    honk = snd('entity.goat.screaming.ambient', 1.4, 1.6)
    sayb = lambda txt, col=COL: tellraw('@a[distance=..32]', [T(txt, col, italic=True)])
    hurt = lambda d, dread=False: f'damage @s {d} {"bm:dread" if dread else "minecraft:mob_attack"} by {ME}'
    G.wjson('bm/predicate/p275/ground.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}})

    # ================================================================== her two rigs (the goose, the Eldritch): summoned, placed, posed
    sel = '@e[type=minecraft:item_display,tag=bm.gdsel]'
    psel = lambda p: f'@e[type=minecraft:item_display,tag=bm.gdsel,tag=bm.gdr_{p}]'
    RIGS = {'q': (R1, S1), 'k': (R2, S2)}
    for f, (R, S) in RIGS.items():
        fn(f'p275g/{f}/rig', [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(R, p, ["bm.gdr", f"bm.gdr{f}", f"bm.gdr_{p}", "bm.gdsel"], S, model=R.model_name(p, R.POSES["idle_a"]), extra=dict(view_range=F(3.0)))}'
                              for p in R.PARTS] + [f'execute rotated as @s rotated ~ 0 run function bm:p275g/{f}/place', f'function bm:p275g/{f}/pose/idle_a'])
        fn(f'p275g/{f}/place', RF.place(R, S / 16, psel))
    used = set()

    def pose(f, name):
        """the line that puts the rig in that pose (its function written once)"""
        R, S = RIGS[f]
        if (f, name) not in used:
            used.add((f, name))
            fn(f'p275g/{f}/pose/{name}', RF.pose(R, R.POSES[name], S, 4 if 'walk' in name else 6, psel, swap=tuple(R.PARTS)))
        return f'function bm:p275g/{f}/pose/{name}'
    for f in RIGS:
        pose(f, 'idle_a')
    # (its body, each tick it isn't striking: walking when it moves, else at rest)
    for f, walk in (('q', ['walk_0', 'walk_1', 'walk_2', 'walk_3']), ('k', ['walk_0', 'walk_1', 'walk_2', 'walk_3'])):
        fn(f'p275g/{f}/anim', ['scoreboard players add @s bm.gdf 1', 'scoreboard players operation #w bm.rng = @s bm.gdf',
                               'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                               'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                               'scoreboard players operation #vx bm.rng += #vz bm.rng',
                               'execute if score #vx bm.rng matches ..300 run scoreboard players operation #w bm.rng %= #40 bm.rng',
                               'execute if score #vx bm.rng matches ..300 if score #w bm.rng matches 0 run ' + pose(f, 'idle_a'),
                               'execute if score #vx bm.rng matches ..300 if score #w bm.rng matches 20 run ' + pose(f, 'idle_b'),
                               'execute if score #vx bm.rng matches ..300 run return 0', 'scoreboard players operation #w bm.rng %= #24 bm.rng'] +
           [f'execute if score #w bm.rng matches {i * 6} run ' + pose(f, w) for i, w in enumerate(walk)])

    # ================================================================== THE CLOVER POND: the stone, its hints, the wake
    pond = '@e[type=minecraft:marker,tag=bm.gdpond]'
    second.append(f'execute as {pond} at @s run function bm:p275g/pond/sec')
    stone = snbt({'Tags': ['bm.gdstone'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:gq_egg'}},
                  'item_display': 'fixed', 'brightness': {'block': Int(12), 'sky': Int(12)},
                  'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.2), F(0)], 'scale': [F(3.0)] * 3}})
    stone_hit = snbt({'Tags': ['bm.gdstoneh'], 'width': F(1.2), 'height': F(1.4), 'response': B(1)})
    fn('p275g/pond/sec', ['execute if entity @e[type=minecraft:husk,tag=bm.gdb,distance=..48] run return 0',
                          'execute unless entity @e[type=minecraft:item_display,tag=bm.gdstone,distance=..1] run function bm:p275g/pond/stone',
                          'execute unless score #lnight bm.bm matches 1 run return 0',
                          'particle minecraft:wax_on ~ ~0.5 ~ 4 0.3 4 0 6', 'particle minecraft:end_rod ~ ~0.2 ~ 4 0.1 4 0.005 3',
                          'execute store result score #gt bm.rng run time query gametime', 'execute if score #gt bm.rng < @s bm.gdr run return 0',
                          'execute as @a[distance=..6,gamemode=!spectator,gamemode=!creative] run function bm:p275g/pond/try'])
    fn('p275g/pond/stone', [f'summon minecraft:item_display ~ ~-0.5 ~ {stone}', f'summon minecraft:interaction ~ ~-0.5 ~ {stone_hit}'])
    trio = lambda: ['scoreboard players operation #o bm.rng = @s bm.pid', 'scoreboard players set #ta bm.rng 0', 'scoreboard players set #tb bm.rng 0', 'scoreboard players set #tc bm.rng 0'] + \
        [f'execute as @e[type=minecraft:wolf,tag={t},distance=..12] if score @s bm.pid = #o bm.rng run scoreboard players set {s} bm.rng 1'
         for t, s in (('bm.lhpet', '#ta'), ('bm.tkpet', '#tb'), ('bm.xvpet', '#tc'))]
    fn('p275g/pond/try', ['execute if entity @e[type=minecraft:husk,tag=bm.gdb,distance=..48] run return 0'] + trio() +
       ['execute if score #ta bm.rng matches 1 if score #tb bm.rng matches 1 if score #tc bm.rng matches 1 run function bm:p275g/wake'])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.gdstoneh] if data entity @s interaction at @s run function bm:p275g/pond/click')
    fn('p275g/pond/click', ['execute on target run function bm:p275g/pond/hint', 'data remove entity @s interaction'])
    hint = lambda txt: title('@s', 'actionbar', T(txt, GOLD, italic=True))
    fn('p275g/pond/hint', ['execute unless score #lnight bm.bm matches 1 run return run ' + hint('The gilded stone is cold. Three hollows round it: a sun, a thread, a crown. It only stirs on a Lucky Night.'),
                           'execute store result score #gt bm.rng run time query gametime',
                           'execute if score #gt bm.rng < @e[type=minecraft:marker,tag=bm.gdpond,distance=..3,limit=1] bm.gdr run return run ' + hint('The stone sleeps. It was woken not long ago - it will stir again tomorrow.'),
                           'execute unless score @s bm.pid matches 1.. run function bm:p21/pid'] + trio() +
       ['execute if score #ta bm.rng matches 1 if score #tb bm.rng matches 1 if score #tc bm.rng matches 1 run return run ' + hint('The stone is warm under your hand. All three hollows glow. Stand in the clover ring...'),
        'execute if score #ta bm.rng matches 0 run tellraw @s ' + snbt([T('The SUN hollow is dark.', GOLD, italic=True)]),
        'execute if score #tb bm.rng matches 0 run tellraw @s ' + snbt([T('The THREAD hollow is empty.', GOLD, italic=True)]),
        'execute if score #tc bm.rng matches 0 run tellraw @s ' + snbt([T('The CROWN hollow is cold.', GOLD, italic=True)]),
        'playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 0.6 0.8'])
    # ---- the wake (as the player who brought them, at the stone)
    host = {'Tags': ['bm.gdb', 'bm.boss', 'bm.seen', 'bm.gdp1', 'bm.gdnew'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(P1 + FLOOR),
            'DeathLootTable': 'minecraft:empty', 'CustomName': T('The Golden Doodle', COL, bold=True), 'CustomNameVisible': B(0),
            'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in (('max_health', P1 + FLOOR), ('armor', 6), ('attack_damage', 2), ('movement_speed', 0.32),
                                                                                ('follow_range', 32), ('knockback_resistance', 0.5), ('scale', HOST1))],
            'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)},
                               {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    fn('p275g/wake', ['kill @e[type=minecraft:item_display,tag=bm.gdstone,distance=..3]', 'kill @e[type=minecraft:interaction,tag=bm.gdstoneh,distance=..3]',
                      f'summon minecraft:husk ~ ~ ~ {snbt(host)}',
                      'execute as @e[type=minecraft:husk,tag=bm.gdnew,distance=..2] at @s run function bm:p275g/born',
                      'particle minecraft:wax_on ~ ~1 ~ 1 1 1 0 60', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.6 0.8 0.6 0.4 40', honk,
                      title('@a[distance=..32]', 'title', T('HONK.', COL, bold=True)),
                      title('@a[distance=..32]', 'subtitle', T('The Golden Doodle (she is very proud of herself)', GOLD, italic=True)),
                      tellraw('@a[distance=..32]', P + [T('The gilded stone wobbles, cracks - and out waddles a ', 'gray'), T('golden goose', COL, bold=True),
                                                       T('. She looks at the three of them, and at you. She is very, very proud of herself.', 'gray')])])
    fn('p275g/born', ['tag @s remove bm.gdnew', 'scoreboard players operation @s bm.pid = #o bm.rng', 'scoreboard players set @s bm.gdk 40', 'scoreboard players set @s bm.gdx 0',
                      'scoreboard players set @s bm.gdl 0', 'scoreboard players set @s bm.gdi 0', 'scoreboard players set @s bm.gdpl 1', 'function bm:p275g/q/rig'] + hitcap.arm(CAP) +
       [f'bossbar set bm:gdoodle name {snbt(T("The Golden Doodle (she is very proud of herself)", COL, bold=True))}', 'bossbar set bm:gdoodle color yellow', f'bossbar set bm:gdoodle max {P1}'])

    # ================================================================== every tick: its body, its mind, its turn and its cure
    tick.append(f'execute as {HOST} at @s run function bm:p275g/tick')
    fn('p275g/tick', [f'tag @e[type=minecraft:item_display,tag=bm.gdr,distance=..12] add bm.gdsel',
                      'execute if entity @s[tag=bm.gdturn] run function bm:p275g/turn/tick',
                      'execute if entity @s[tag=bm.gdcure] run function bm:p275g/cure/tick',
                      'execute if entity @s[tag=bm.gdallin] run function bm:p275g/allin/tick',
                      'execute if entity @s[tag=bm.gdtired] run function bm:p275g/tired/tick',
                      'execute store result score #hp bm.rng run data get entity @s Health',
                      f'execute if entity @s[tag=bm.gdp1,tag=!bm.gdcine] if score #hp bm.rng matches ..{FLOOR} run function bm:p275g/turn/start',
                      f'execute if entity @s[tag=bm.gdp2,tag=!bm.gdcine] if score #hp bm.rng matches ..{FLOOR} run function bm:p275g/cure/start',
                      f'execute if entity @s[tag=bm.gdp2,tag=!bm.gdcine,tag=!bm.gdan] if score #hp bm.rng <= #gdq bm.rng run function bm:p275g/allin/start',
                      'execute unless entity @s[tag=bm.gdcine] unless entity @s[tag=bm.gdallin] unless entity @s[tag=bm.gdtired] run function bm:p275g/mind',
                      'execute if entity @s[tag=bm.gdp1,tag=!bm.gdcine] unless score @s bm.gdx matches 1.. unless score @s bm.gdst matches 1.. run function bm:p275g/q/anim',
                      'execute if entity @s[tag=bm.gdp2,tag=!bm.gdcine,tag=!bm.gdallin,tag=!bm.gdtired] unless score @s bm.gdx matches 1.. run function bm:p275g/k/anim',
                      'execute if score @s bm.gdpl matches 1 rotated as @s rotated ~ 0 run function bm:p275g/q/place',
                      'execute if score @s bm.gdpl matches 2 rotated as @s rotated ~ 0 run function bm:p275g/k/place',
                      f'tag {sel} remove bm.gdsel'])
    # ---- its mind: an attack it's ready for (never the same twice running), else the husk's own walk at you
    fn('p275g/mind', ['execute if score @s bm.gdst matches 1.. run return run function bm:p275g/stun',
                      'execute if score @s bm.gdx matches 1.. run return run function bm:p275g/act',
                      'execute if score @s bm.gdk matches 1.. run return run scoreboard players remove @s bm.gdk 1',
                      f'execute unless entity {TGT[:-1].replace("..24", "..16")}] run return 0',
                      'execute if entity @s[tag=bm.gdp1] run function bm:p275g/pick1', 'execute if entity @s[tag=bm.gdp2] run function bm:p275g/pick2'])
    fn('p275g/stun', ['scoreboard players remove @s bm.gdst 1', 'particle minecraft:crit ~ ~1.6 ~ 0.3 0.1 0.3 0.1 2',
                      'execute if score @s bm.gdst matches 0 run data modify entity @s NoAI set value 0b'])
    A1 = {1: 'honk', 2: 'charge', 3: 'eggs', 4: 'slap', 5: 'coin'}
    A2 = {11: 'beam', 12: 'shriek', 13: 'slam', 14: 'lunge', 15: 'curse'}
    DUR = {1: 18, 2: 40, 3: 24, 4: 14, 5: 26, 11: 60, 12: 34, 13: 30, 14: 24, 15: 116}
    for n, (lo, hi), CD in ((1, (1, 5), (40, 60)), (2, (11, 15), (50, 70))):
        fn(f'p275g/pick{n}', [f'execute store result score #r bm.rng run random value {lo}..{hi}',
                              'execute if score #r bm.rng = @s bm.gdl run scoreboard players add #r bm.rng 1',
                              f'execute if score #r bm.rng matches {hi + 1} run scoreboard players set #r bm.rng {lo}',
                              'scoreboard players operation @s bm.gda = #r bm.rng', 'scoreboard players operation @s bm.gdl = #r bm.rng',
                              f'execute store result score @s bm.gdk run random value {CD[0]}..{CD[1]}', 'data modify entity @s NoAI set value 1b',
                              f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~'] +
           [f'execute if score #r bm.rng matches {a} run scoreboard players set @s bm.gdx {DUR[a] + 1}' for a in range(lo, hi + 1)])
    fn('p275g/act', ['scoreboard players remove @s bm.gdx 1'] +
       [f'execute if score @s bm.gda matches {a} run function bm:p275g/a/{nm}' for a, nm in list(A1.items()) + list(A2.items())] +
       ['execute if score @s bm.gdx matches 0 unless score @s bm.gdst matches 1.. run data modify entity @s NoAI set value 0b',
        'execute if score @s bm.gdx matches 0 run tag @a remove bm.gdhit', 'execute if score @s bm.gdx matches 0 run tag @a remove bm.gdref'])

    def atk(nm, tl):
        """an attack's timeline: {ticks left: [lines]} (as the host, each tick it runs)"""
        lines = []
        for x, L in sorted(tl.items(), reverse=True):
            if isinstance(x, tuple):
                lines.append(f'execute if score @s bm.gdx matches {x[0]}..{x[1]} run function bm:p275g/a/{nm}/{x[0]}_{x[1]}')
                fn(f'p275g/a/{nm}/{x[0]}_{x[1]}', L)
            elif len(L) == 1:
                lines.append(f'execute if score @s bm.gdx matches {x} run {L[0]}')
            else:
                lines.append(f'execute if score @s bm.gdx matches {x} run function bm:p275g/a/{nm}/{x}')
                fn(f'p275g/a/{nm}/{x}', L)
        fn(f'p275g/a/{nm}', lines)
    foe = lambda r: f'@a[distance=..{r},gamemode=!spectator,gamemode=!creative]'
    ring = lambda r, col='1.0,0.82,0.25', n=16: [f'particle minecraft:dust{{color:[{col}],scale:1.6}} ^{r * __import__("math").sin(6.2832 * i / n):.2f} ^0.3 ^{r * __import__("math").cos(6.2832 * i / n):.2f} 0.1 0.05 0.1 0 2' for i in range(n)]
    # ---- PHASE 1
    atk('honk', {18: [pose('q', 'honk_up')], 12: [pose('q', 'honk'), honk, 'particle minecraft:note ^ ^1 ^1.5 0.6 0.4 0.6 1 10',
                                                  f'execute positioned ^ ^ ^2 as {foe(2.6)} at @s run function bm:p275g/h/honk']})
    fn('p275g/h/honk', [hurt(2), 'effect give @s minecraft:slowness 2 0'])
    atk('charge', {40: [pose('q', 'charge'), snd('entity.cat.hiss', 1.2, 0.8)], 31: [f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~'],
                   (1, 30): ['function bm:p275g/a/charge_step']})
    fn('p275g/a/charge_step', ['execute rotated as @s rotated ~ 0 positioned ^ ^ ^0.42 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p275g/a/charge_go',
                               'scoreboard players set @s bm.gdx 0', 'scoreboard players set @s bm.gdst 20', pose('q', 'dazed'),
                               'particle minecraft:crit ~ ~1.6 ~ 0.4 0.2 0.4 0.3 20', snd('entity.player.attack.knockback', 1.2, 0.6),
                               sayb('(BONK. She waddled straight into the wall. Stars.)')])
    fn('p275g/a/charge_go', ['tp @s ~ ~ ~', 'particle minecraft:wax_on ~ ~0.3 ~ 0.2 0.1 0.2 0 2', f'execute as {foe(1.4)}[tag=!bm.gdhit] run function bm:p275g/h/charge'.replace('][', ',')])
    fn('p275g/h/charge', ['tag @s add bm.gdhit', hurt(4)])
    atk('eggs', {24: [pose('q', 'lay')], 16: [pose('q', 'eggs')], 14: [f'execute at {TGT} run function bm:p275g/a/eggs3', snd('entity.chicken.egg', 1.4, 0.6)]})
    egg = snbt({'Tags': ['bm.gdegg'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:gq_egg'}},
                'item_display': 'fixed', 'teleport_duration': Int(2),
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.3), F(0)], 'scale': [F(1.6)] * 3}})
    fn('p275g/a/eggs3', [f'summon minecraft:item_display ~2 ~ ~ {egg}', f'summon minecraft:item_display ~-1.5 ~ ~1.5 {egg}', f'summon minecraft:item_display ~ ~ ~-2 {egg}',
                         'scoreboard players set @e[type=minecraft:item_display,tag=bm.gdegg,distance=..4] bm.gdx 30'])
    tick.append('execute as @e[type=minecraft:item_display,tag=bm.gdegg] at @s run function bm:p275g/egg')
    fn('p275g/egg', ['scoreboard players remove @s bm.gdx 1', 'scoreboard players operation #w bm.rng = @s bm.gdx', 'scoreboard players operation #w bm.rng %= #6 bm.rng',
                     'execute if score #w bm.rng matches 0 run tp @s ~ ~ ~ ~25 0', 'execute if score #w bm.rng matches 3 run tp @s ~ ~ ~ ~-25 0',
                     'execute if score @s bm.gdx matches ..0 run function bm:p275g/egg_pop'])
    fn('p275g/egg_pop', ['particle minecraft:wax_on ~ ~0.4 ~ 0.5 0.4 0.5 0 20', 'particle minecraft:totem_of_undying ~ ~0.4 ~ 0.3 0.3 0.3 0.3 16',
                         'playsound minecraft:entity.firework_rocket.blast hostile @a[distance=..16] ~ ~ ~ 0.8 1.6',
                         f'execute as {foe(1.5)} run damage @s 2 minecraft:mob_attack', 'summon minecraft:item ~ ~0.3 ~ {Item:{id:"minecraft:gold_nugget",count:1}}',
                         'execute store result score #r bm.rng run random value 1..4', 'execute if score #r bm.rng matches 1 run loot spawn ~ ~0.3 ~ loot bm:items/lucky_token', 'kill @s'])
    atk('slap', {14: [pose('q', 'slap_up')], 10: [pose('q', 'slap'), snd('entity.player.attack.sweep', 1.2, 0.7), f'execute positioned ^ ^ ^1.2 as {foe(2)} run {hurt(5)}']})
    atk('coin', {26: [pose('q', 'coin'), snd('entity.experience_orb.pickup', 1.2, 1.4)],
                 6: ['execute store result score #r bm.rng run random value 1..2', 'execute if score #r bm.rng matches 1 run function bm:p275g/a/heads',
                     'execute if score #r bm.rng matches 2 run function bm:p275g/a/tails']})
    fn('p275g/a/heads', ['effect give @s minecraft:speed 5 1 true', 'effect give @s minecraft:resistance 5 0 true', pose('q', 'proud'), honk,
                         title('@a[distance=..32]', 'actionbar', T('HEADS! She is very pleased with herself.', COL, bold=True))])
    fn('p275g/a/tails', [f'effect give {foe(16)} minecraft:luck 10 1', 'effect give @s minecraft:slowness 3 3 true', 'scoreboard players set @s bm.gdst 60', pose('q', 'dazed'),
                         title('@a[distance=..32]', 'actionbar', T('TAILS. Luck for you - and she SULKS.', COL, bold=True))])
    # ---- PHASE 2 (DREAD blows)
    beam = lambda yaw, hit: f'execute positioned ~ ~4.6 ~ facing entity {TGT} eyes rotated ~{yaw} ~ run function bm:p275g/ray{"_h" if hit else ""}'
    atk('beam', {60: [pose('k', 'beam_up'), snd('entity.guardian.attack', 1.6, 0.5), 'particle minecraft:dust{color:[0.95,0.15,0.2],scale:2} ~ ~4.6 ~ 0.3 0.3 0.3 0 20'],
                 40: [pose('k', 'beam'), beam(-30, True)],
                 **{x: [beam(round((20 - x) * 1.5), x % 10 == 0)] for x in range(35, 0, -5)}})
    fn('p275g/ray', ['scoreboard players set #ray bm.rng 0', 'execute positioned ^ ^ ^1.5 run function bm:p275g/ray_s'])
    fn('p275g/ray_h', ['scoreboard players set #ray bm.rng 0', 'execute positioned ^ ^ ^1.5 run function bm:p275g/ray_hs'])
    fn('p275g/ray_s', ['particle minecraft:dust{color:[0.95,0.15,0.2],scale:1.8} ~ ~ ~ 0.08 0.08 0.08 0 2', 'scoreboard players add #ray bm.rng 1',
                       'execute if score #ray bm.rng matches ..20 if block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^1 run function bm:p275g/ray_s'])
    fn('p275g/ray_hs', ['particle minecraft:dust{color:[0.95,0.15,0.2],scale:2.2} ~ ~ ~ 0.1 0.1 0.1 0 3', 'scoreboard players add #ray bm.rng 1',
                        f'execute as {foe(1.4)}[tag=!bm.gdref] run function bm:p275g/h/beam'.replace('][', ','),
                        'execute if score #ray bm.rng matches ..20 if block ~ ~ ~ #bm:grap_pass positioned ^ ^ ^1 run function bm:p275g/ray_hs'])
    fn('p275g/h/beam', ['execute if items entity @s weapon.* *[minecraft:custom_data~{bm:"lucky_token"}] run return run function bm:p275g/h/reflect', hurt(6, True)])
    fn('p275g/h/reflect', ['tag @s add bm.gdref', 'clear @s *[minecraft:custom_data~{bm:"lucky_token"}] 1', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.4 20',
                           'playsound minecraft:block.amethyst_block.resonate player @s ~ ~ ~ 1 1.6',
                           title('@s', 'actionbar', T('Your Lucky Token flares - the beam glances off! (It\'s used up.)', COL, bold=True))])
    atk('shriek', {34: [pose('k', 'shriek'), snd('entity.warden.roar', 1.6, 1.4)],
                   **{x: ring(r, '0.95,0.15,0.2') + [f'execute as {foe(r)} unless entity @s[distance=..{r - 2.2:.1f}] if predicate bm:p275/ground run function bm:p275g/h/shriek']
                      for x, r in ((24, 3.5), (22, 7), (20, 10))}})
    fn('p275g/h/shriek', [hurt(8, True), 'effect give @s minecraft:weakness 5 0'])
    atk('slam', {30: [pose('k', 'slam_up'), snd('entity.phantom.flap', 1.6, 0.5)], 18: [pose('k', 'slam'), snd('entity.generic.explode', 1.4, 0.6), 'particle minecraft:explosion ~ ~0.3 ~ 1.5 0 1.5 0 6'],
                 **{x: ring(r, '0.85,0.6,0.15') + [f'execute as {foe(r)} unless entity @s[distance=..{r - 1.6:.1f}] if predicate bm:p275/ground run function bm:p275g/h/slam']
                    for x, r in ((17, 2.0), (15, 3.5), (13, 5.0), (11, 6.5))}})
    fn('p275g/h/slam', ['execute if entity @s[tag=bm.gdhit] run return 0', 'tag @s add bm.gdhit', hurt(10, True)])
    atk('lunge', {24: [pose('k', 'bite_up'), f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~', snd('entity.ravager.roar', 1.0, 1.6)],
                  15: [pose('k', 'bite'), snd('entity.evoker_fangs.attack', 1.4, 0.6)],
                  14: [f'execute rotated as @s rotated ~ 0 positioned ^ ^1 ^{i} as {foe(1.4)} run function bm:p275g/h/lunge' for i in range(2, 9)] +
                      [f'particle minecraft:dust{{color:[0.95,0.15,0.2],scale:1.6}} ^ ^1.4 ^{i} 0.2 0.2 0.2 0 4' for i in range(2, 9)]})
    fn('p275g/h/lunge', ['execute if entity @s[tag=bm.gdhit] run return 0', 'tag @s add bm.gdhit', hurt(12, True)])
    atk('curse', {116: [pose('k', 'curse'), snd('entity.wither.ambient', 1.0, 0.6), sayb('(THE UNLUCKY: the clover burns black and red under you - step off it!)', RED)],
                  100: ['function bm:p275g/a/sigils']})
    sig = snbt({'Tags': ['bm.gdsig']})
    fn('p275g/a/sigils', [f'execute as {foe(16)} at @s run summon minecraft:marker ~ ~ ~ {sig}', 'scoreboard players set @e[type=minecraft:marker,tag=bm.gdsig,distance=..20] bm.gdx 100'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.gdsig] at @s run function bm:p275g/sigil')
    fn('p275g/sigil', ['scoreboard players remove @s bm.gdx 1', 'scoreboard players operation #w bm.rng = @s bm.gdx', 'scoreboard players operation #w bm.rng %= #5 bm.rng',
                       'execute if score #w bm.rng matches 0 run function bm:p275g/sigil_fx',
                       f'execute as {foe(2.5)} run effect give @s minecraft:unluck 2 0',
                       'scoreboard players operation #w bm.rng = @s bm.gdx', 'scoreboard players operation #w bm.rng %= #20 bm.rng',
                       f'execute if score #w bm.rng matches 0 as {foe(2.5)} as {ME} run function bm:p275g/heal4',
                       'execute if score @s bm.gdx matches ..0 run kill @s'])
    fn('p275g/sigil_fx', ring(2.5, '0.1,0.02,0.02', 12) + ring(1.2, '0.95,0.15,0.2', 8))
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #20 bm.rng 20']
    fn('p275g/heal4', ['execute store result score #h bm.rng run data get entity @s Health', 'scoreboard players add #h bm.rng 4',
                       'execute store result entity @s Health float 1 run scoreboard players get #h bm.rng', 'particle minecraft:dust{color:[0.95,0.15,0.2],scale:1.4} ~ ~3 ~ 0.6 0.6 0.6 0 6'])

    # ================================================================== THE CAMERA (as phase238's: held, turned to the look marker, a 3-tick lease - p238/cam/lease
    # gives the body back - never a gamemode change, never Darkness)
    look = 'bm.gqlook'
    fn('p275g/cam/hold', ['tag @s add bm.svcam', 'scoreboard players set @s bm.svcm 3', 'function bm:p176/nodark',
                          f'execute at @s if entity @e[type=minecraft:marker,tag={look},distance=..48] run tp @s ~ ~ ~ facing entity @e[type=minecraft:marker,tag={look},distance=..48,sort=nearest,limit=1] feet',
                          'effect give @s minecraft:slowness 2 255 true', 'effect give @s minecraft:resistance 2 255 true', 'effect give @s minecraft:jump_boost 2 200 true'])
    fn('p275g/cam/follow', [f'execute if score @s bm.gdpl matches 1 positioned ~ ~1.2 ~ as @e[type=minecraft:marker,tag={look},distance=..32] run tp @s ~ ~ ~',
                            f'execute if score @s bm.gdpl matches 2 positioned ~ ~4.5 ~ as @e[type=minecraft:marker,tag={look},distance=..32] run tp @s ~ ~ ~'])
    cine = lambda h: ['tag @s add bm.gdcine', 'data modify entity @s Invulnerable set value 1b', 'data modify entity @s NoAI set value 1b', 'scoreboard players set @s bm.gdt 0',
                      'scoreboard players set @s bm.gdx 0', 'scoreboard players set @s bm.gdst 0', 'kill @e[type=minecraft:item_display,tag=bm.gdegg,distance=..32]',
                      'kill @e[type=minecraft:marker,tag=bm.gdsig,distance=..32]', f'kill @e[type=minecraft:marker,tag={look},distance=..32]',
                      f'summon minecraft:marker ~ ~{h} ~ {{Tags:["{look}"]}}', 'tag @a remove bm.gdhit']
    at = lambda t, cmd: f'execute if score @s bm.gdt matches {t} run {cmd}'
    sov = '@e[type=minecraft:wolf,tag=bm.gdsov,limit=1]'
    lb = '@e[type=minecraft:wolf,tag=bm.gdlb,limit=1]'
    mark_trio = ['scoreboard players operation #o bm.rng = @s bm.pid', 'tag @e[type=minecraft:wolf] remove bm.gdsov', 'tag @e[type=minecraft:wolf] remove bm.gdlb',
                 'execute as @e[type=minecraft:wolf,tag=bm.xvpet,distance=..48] if score @s bm.pid = #o bm.rng run tag @s add bm.gdsov',
                 'execute as @e[type=minecraft:wolf,tag=bm.lhpet,distance=..48] if score @s bm.pid = #o bm.rng run tag @s add bm.gdlb']
    rig_off = lambda f: f'kill @e[type=minecraft:item_display,tag=bm.gdr{f},distance=..16]'
    # ---- THE TURN (120 ticks)
    fn('p275g/turn/start', ['tag @s remove bm.gdp1', 'tag @s add bm.gdturn'] + cine(1.2) + mark_trio +
       [pose('q', 'dazed'), sayb('(She sits down, hard - X-eyed, dazed. She looks beaten.)'), 'bossbar set bm:gdoodle name "..."'])
    fn('p275g/turn/tick', ['scoreboard players add @s bm.gdt 1', f'execute as {FIGHT} at @s run function bm:p275g/cam/hold',
                           'function bm:p275g/cam/follow',
                           at(20, pose('q', 'idle_a')), at(20, sayb('(...then she gets up. And waddles, very deliberately, toward the Bound Sovereign.)')),
                           'execute if score @s bm.gdt matches 24..64 run function bm:p275g/turn/waddle',
                           at(66, pose('q', 'steal')), at(66, honk),
                           at(68, title('@a[distance=..32]', 'title', T('She bit the wrong crown.', RED, bold=True))),
                           at(68, f'execute at {sov} run particle minecraft:dust{{color:[0.95,0.15,0.2],scale:2}} ~ ~2 ~ 0.4 0.4 0.4 0 30'),
                           at(74, tellraw('@a[distance=..32]', [T('The Bound Sovereign: ', RED, bold=True), T('"...that was MINE."', '#e8a0a0', italic=True)])),
                           at(78, sayb('(A sliver of the Dread breaks off its crown - and sticks. Her gold cracks. Something red glows in the cracks.)', RED)),
                           at(80, 'function bm:p275g/turn/morph'),
                           at(100, pose('k', 'roar')), at(100, snd('entity.warden.roar', 2.0, 0.8)),
                           at(100, title('@a[distance=..32]', 'title', T('THE GILDED ELDRITCH', RED, bold=True))),
                           at(120, 'function bm:p275g/turn/end')])
    fn('p275g/turn/waddle', [f'execute if entity {sov} unless entity @e[type=minecraft:wolf,tag=bm.gdsov,distance=..2.5] facing entity {sov} feet rotated ~ 0 positioned ^ ^ ^0.14 '
                             'if block ~ ~ ~ #bm:grap_pass run tp @s ~ ~ ~ ~ ~',
                             'scoreboard players operation #w bm.rng = @s bm.gdt', 'scoreboard players operation #w bm.rng %= #24 bm.rng'] +
       [f'execute if score #w bm.rng matches {i * 6} run ' + pose('q', w) for i, w in enumerate(['walk_0', 'walk_1', 'walk_2', 'walk_3'])])
    fn('p275g/turn/morph', [rig_off('q'), 'scoreboard players set @s bm.gdpl 2', f'attribute @s minecraft:scale base set {HOST2}', 'function bm:p275g/k/rig', pose('k', 'menace'),
                            'particle minecraft:dust{color:[0.95,0.15,0.2],scale:2.5} ~ ~2 ~ 1.5 2 1.5 0 120', 'particle minecraft:wax_on ~ ~2 ~ 1.5 2 1.5 0 60',
                            snd('entity.warden.emerge', 1.6, 0.8)])
    fn('p275g/turn/end', ['tag @s remove bm.gdturn', 'tag @s remove bm.gdcine', 'tag @s add bm.gdp2', 'data modify entity @s Invulnerable set value 0b', 'data modify entity @s NoAI set value 0b',
                          f'kill @e[type=minecraft:marker,tag={look},distance=..32]', 'tag @e[type=minecraft:wolf] remove bm.gdsov', 'tag @e[type=minecraft:wolf] remove bm.gdlb',
                          f'execute store result score #n bm.rng if entity {FIGHT}', 'scoreboard players remove #n bm.rng 1', f'scoreboard players set #pl bm.rng {P2_EXTRA}',
                          'scoreboard players operation #n bm.rng *= #pl bm.rng', f'scoreboard players add #n bm.rng {P2}',
                          f'execute if score #n bm.rng matches {P2_CAP + 1}.. run scoreboard players set #n bm.rng {P2_CAP}',
                          'execute store result bossbar bm:gdoodle max run scoreboard players get #n bm.rng',
                          # (ALL IN: at a quarter of the pool)
                          'scoreboard players operation #gdq bm.rng = #n bm.rng', 'scoreboard players operation #gdq bm.rng /= #4 bm.rng', f'scoreboard players add #gdq bm.rng {FLOOR}',
                          f'scoreboard players add #n bm.rng {FLOOR}',
                          'execute store result storage bm:tmp gd.hp int 1 run scoreboard players get #n bm.rng', 'function bm:p275g/turn/hp with storage bm:tmp gd',
                          'attribute @s minecraft:movement_speed base set 0.18', 'attribute @s minecraft:armor base set 14', 'attribute @s minecraft:attack_damage base set 8',
                          'attribute @s minecraft:knockback_resistance base set 1.0', 'effect give @s minecraft:resistance infinite 1 true', 'scoreboard players set @s bm.gdk 40',
                          'function bm:hitcap/sync', f'bossbar set bm:gdoodle name {snbt(T("THE GILDED ELDRITCH", RED, bold=True))}', 'bossbar set bm:gdoodle color red'])
    fn('p275g/turn/hp', ['$attribute @s minecraft:max_health base set $(hp)', '$data modify entity @s Health set value $(hp)f'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #4 bm.rng 4']
    # ---- ALL IN (a quarter of pool 2): the coin on its EDGE - 12 s untouchable, the sigils every second; then it TIRES (7 s)
    fn('p275g/allin/start', ['tag @s add bm.gdan', 'tag @s add bm.gdallin', 'scoreboard players set @s bm.gdt 0', 'scoreboard players set @s bm.gdx 0',
                             'data modify entity @s Invulnerable set value 1b', 'data modify entity @s NoAI set value 1b', pose('k', 'curse'),
                             title('@a[distance=..32]', 'title', T('ALL IN', RED, bold=True)),
                             sayb('(It flips the lucky coin one last time - and it lands on its EDGE.)', RED), snd('entity.experience_orb.pickup', 1.6, 0.5)])
    fn('p275g/allin/tick', ['scoreboard players add @s bm.gdt 1', 'scoreboard players operation #w bm.rng = @s bm.gdt', 'scoreboard players operation #w bm.rng %= #20 bm.rng',
                            'execute if score #w bm.rng matches 0 run function bm:p275g/a/sigils', 'execute if score @s bm.gdt matches 240.. run function bm:p275g/allin/end'])
    fn('p275g/allin/end', ['tag @s remove bm.gdallin', 'tag @s add bm.gdtired', 'scoreboard players set @s bm.gdt 0', 'data modify entity @s Invulnerable set value 0b',
                           pose('k', 'tired'), sayb('(It TIRES - down on its breast, eyes dim. Strike it!)', COL)])
    fn('p275g/tired/tick', ['scoreboard players add @s bm.gdt 1', 'execute if score @s bm.gdt matches 140.. run function bm:p275g/tired/end'])
    fn('p275g/tired/end', ['tag @s remove bm.gdtired', 'data modify entity @s NoAI set value 0b', 'scoreboard players set @s bm.gdk 30'])
    # ---- THE CURE (160 ticks): the Lightbringer's light; the shard burns away; the goose again - and she joins you
    sun = snbt({'Tags': ['bm.gdsun'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:gh_cure'}}, 'item_display': 'fixed',
                'brightness': {'block': Int(15), 'sky': Int(15)},
                'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.05), F(0)], 'scale': [F(1.6)] * 3}})
    lbsay = lambda txt: tellraw('@a[distance=..32]', [T('The Lightbringer: ', '#ffe08a', bold=True), T(txt, '#fff4d0', italic=True)])
    fn('p275g/cure/start', ['tag @s add bm.gdcure', 'tag @s remove bm.gdallin', 'tag @s remove bm.gdtired'] + cine(4.0) + mark_trio +
       [pose('k', 'tired'), 'bossbar set bm:gdoodle players'])
    fn('p275g/cure/tick', ['scoreboard players add @s bm.gdt 1', 'function bm:p275g/cam/follow', f'execute as {FIGHT} at @s run function bm:p275g/cam/hold',
                           at(2, lbsay('"Hush, little one. That isn\'t yours to carry."')),
                           at(2, f'execute at {lb} run particle minecraft:end_rod ~ ~1.5 ~ 0.4 0.8 0.4 0.02 20'),
                           at(20, f'summon minecraft:item_display ~ ~ ~ {sun}'), at(20, 'particle minecraft:end_rod ~ ~3 ~ 2 2 2 0.05 120'),
                           at(20, 'particle minecraft:wax_on ~ ~3 ~ 2 2 2 0 60'), at(20, snd('block.beacon.activate', 1.6, 1.4)),
                           at(40, pose('k', 'defeat')), at(40, 'particle minecraft:dust{color:[0.95,0.15,0.2],scale:2} ~ ~4 ~ 0.6 0.6 0.6 0 30'),
                           at(44, 'particle minecraft:end_rod ~ ~4 ~ 0.8 0.8 0.8 0.08 40'), at(44, snd('block.glass.break', 1.4, 0.6)),
                           at(50, tellraw('@a[distance=..32]', [T('The Bound Sovereign: ', RED, bold=True), T('"...good riddance."', '#e8a0a0', italic=True)])),
                           at(60, 'function bm:p275g/cure/shrink'),
                           at(80, sayb('(A small goose again - dizzy. The Lightbringer kneels beside her.)', GOLD)),
                           at(100, pose('q', 'happy')), at(100, honk), at(100, title('@a[distance=..32]', 'title', T('HONK.', COL, bold=True))),
                           at(140, 'function bm:p275g/cure/end')])
    fn('p275g/cure/shrink', [rig_off('k'), 'scoreboard players set @s bm.gdpl 1', f'attribute @s minecraft:scale base set {HOST1}', 'function bm:p275g/q/rig', pose('q', 'dazed'),
                             'particle minecraft:poof ~ ~1 ~ 1 1 1 0.05 40', 'particle minecraft:end_rod ~ ~1 ~ 1 1 1 0.05 40'])
    fn('p275g/cure/end', [title('@a[distance=..32]', 'title', T('The Golden Doodle', COL, bold=True)),
                          title('@a[distance=..32]', 'subtitle', T('her Lightbringer form is yours', '#fff4d0', italic=True)),
                          'execute store result score #gt bm.rng run time query gametime', f'scoreboard players add #gt bm.rng {REST}',
                          f'execute as {pond} at @s if entity @e[type=minecraft:husk,tag=bm.gdb,distance=..48] run scoreboard players operation @s bm.gdr = #gt bm.rng',
                          'playsound minecraft:ui.toast.challenge_complete player @a[distance=..48] ~ ~ ~ 1 1.2',
                          'execute as @a[distance=..48,tag=bm.gdfight] at @s run function bm:p275g/reward', 'function bm:p275g/gone'])
    fn('p275g/gone', [rig_off('q'), rig_off('k'), 'kill @e[type=minecraft:item_display,tag=bm.gdsun,distance=..16]', f'kill @e[type=minecraft:marker,tag={look},distance=..32]',
                      'kill @e[type=minecraft:item_display,tag=bm.gdegg,distance=..32]', 'kill @e[type=minecraft:marker,tag=bm.gdsig,distance=..32]',
                      'tag @e[type=minecraft:wolf] remove bm.gdsov', 'tag @e[type=minecraft:wolf] remove bm.gdlb', 'tag @a remove bm.gdfight', 'tag @a remove bm.gdhit',
                      'bossbar set bm:gdoodle players', 'tp @s ~ -300 ~', 'kill @s'])
    # ---- the spoils (as each who fought): the first time, the tokens, the feather - and she joins; later, tokens and scratch cards
    fn('p275g/reward', ['tag @s add bm.gdwin', 'execute unless entity @s[tag=bm.gdbeat] run function bm:p275g/first', 'execute if entity @s[tag=bm.gdbeat] run function bm:p275g/again',
                        'tag @s add bm.gdbeat', 'execute unless entity @s[tag=bm.gqmet] run function bm:p275/enc/joined'])
    fn('p275g/first', [give('lucky_token', 8), give('dread_token', 3), give('gilded_feather'),
                       tellraw('@s', P + [T('The Golden Doodle is cured. ', COL, bold=True), T('8 Lucky Tokens, 3 Dread Tokens and a ', 'gray'), T('Gilded Feather', COL, bold=True), T(' are yours.', 'gray')])])
    fn('p275g/again', [give('lucky_token', 4), give('dread_token', 1), give('scratch_card', 3),
                       tellraw('@s', P + [T('The Golden Doodle is cured again. ', COL, bold=True), T('4 Lucky Tokens, a Dread Token and 3 Lucky Scratch Cards.', 'gray')])])
    # ---- the fight's bar, its fighters, and its leaving (nobody near for a minute: back into the egg - the pond doesn't rest)
    second.append(f'execute as {HOST} at @s run function bm:p275g/sec')
    second.append(f'execute unless entity {HOST} run bossbar set bm:gdoodle players')
    second.append('execute as @e[type=minecraft:item_display,tag=bm.gdr] at @s unless entity @e[type=minecraft:husk,tag=bm.gdb,distance=..16] run kill @s')
    fn('p275g/sec', ['execute store result score #b bm.rng run data get entity @s Health', f'scoreboard players remove #b bm.rng {FLOOR}',
                     'execute if score #b bm.rng matches ..-1 run scoreboard players set #b bm.rng 0',
                     'execute unless entity @s[tag=bm.gdcure] store result bossbar bm:gdoodle value run scoreboard players get #b bm.rng',
                     'execute unless entity @s[tag=bm.gdcure] run bossbar set bm:gdoodle players @a[distance=..48]',
                     f'tag {FIGHT} add bm.gdfight',
                     'execute if entity @a[distance=..48,gamemode=!spectator] run return run scoreboard players set @s bm.gdi 0',
                     'scoreboard players add @s bm.gdi 1', 'execute if score @s bm.gdi matches 60.. run function bm:p275g/leave'])
    fn('p275g/leave', ['particle minecraft:wax_on ~ ~1 ~ 1 1 1 0 40', 'function bm:p275g/gone'])
    # ---- the Gilded Feather: in the off hand, Luck (II on a Lucky Night) and Slow Falling
    second.append('execute as @a if items entity @s weapon.offhand *[minecraft:custom_data~{bm:"gilded_feather"}] run function bm:p275g/feather')
    fn('p275g/feather', ['execute unless score #lnight bm.bm matches 1 run effect give @s minecraft:luck 3 0 true', 'execute if score #lnight bm.bm matches 1 run effect give @s minecraft:luck 3 1 true',
                         'effect give @s minecraft:slow_falling 3 0 true'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.gdr]', 'kill @e[type=minecraft:item_display,tag=bm.gdegg]', 'kill @e[type=minecraft:item_display,tag=bm.gdsun]',
                                       'kill @e[type=minecraft:item_display,tag=bm.gdstone]', 'kill @e[type=minecraft:interaction,tag=bm.gdstoneh]',
                                       'kill @e[type=minecraft:marker,tag=bm.gdsig]', f'kill @e[type=minecraft:marker,tag={look}]', f'tp {HOST} ~ -300 ~', 'bossbar remove bm:gdoodle']
    fn('admin/gdoodle_boss', ['scoreboard players operation #o bm.rng = @s bm.pid', 'execute positioned ^ ^ ^6 run function bm:p275g/wake'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/gdoodle_boss', 'yellow'), T('  the Golden Doodle\'s fight, here (the Clover Pond: the Gilded Roost, on a Lucky Night, with the trio)', 'gray')]))
