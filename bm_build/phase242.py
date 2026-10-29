"""Phase 242 (2.99): ADMIRAL VEXIS, VOICE OF THE HIVE - the boss of the Vorn Armada (phase241), at the helm of the Flagship's bridge
(p2/armadacfg.ARENA; vexis_art.py; armada_lore.py). One in the world at a time: a husk host (invisible, scaled to its body), its rig
of item displays. The second-hardest fight in the game: below the Dread Sovereign, above everything else.

DORMANT      its warframe kneels at the helm, powered down, the great window behind it full of the Hive-Star - until someone walks
             onto the bridge.
THE COMING   (20 s; fighters held, eyes on it) the battle door seals; the bridge goes dark; a hum rises; the warframe's systems light
             section by section (legs, reactor, arms, the cockpit and its pilot), the window floods red; the hive speaks through it;
             it stands - the cannon arm comes up - and the shoulder pods open: ADMIRAL VEXIS, Voice of the Hive.
THE FIGHT    three pools of health (no burst skips one), PH_HP for one fighter and more for each other one.
  I  THE WARFRAME   PLASMA SWEEP (the cannon arm sweeps an arc - get a pylon between you), MISSILES (a marked circle under every
             fighter - move), STOMP (a shockwave - jump it), DROP-PODS (troopers fall from the dome). FOUR SHIELD PYLONS: while any
             stands, the frame shrugs off most of every blow. Each one charges in turn - strike it WHILE IT GLOWS and it overloads
             (half a minute down). All four down: the frame is exposed.
  turn       (14 s) the frame staggers; the cockpit cracks, sparks, blows - and Vexis climbs out of the wreck and lifts into the air
             on gravity, its shell left kneeling behind it: THE HIVE-LINK.
  II THE HIVE-LINK  it hovers. GRAVITY WELLS (dragged toward a singularity - then it implodes), the IMPROVEMENT BEAM (from its eyes:
             it slows, weakens and burns - break its line of sight), CLONES (four of it, all firing - strike the real one; a clone
             struck bursts in your face), HIVE DRONES.
  turn       (15 s) it turns to the window and reaches for the star; the star's fire pours through the glass into it; its skin cracks
             with light: STARFIRE.
  III STARFIRE      STAR-FLARES (a wall of fire sweeps in from the window - shelter behind a pylon's husk or the wreck), the SOLAR
             LANCE (it aims, then fires a straight beam), GRAVITY FLIPS (circles where you're thrown up and dropped), the improvement
             beam, drones. At a quarter of its last pool it FRENZIES (10 s it can't be hurt, flares rain) - then it TIRES: strike it.
THE FALL     (30 s, eyes held on it) THE UNLINKING: the hive-link burns out; the implants spark and die; the hive's voice falls silent
             for the first time in an age; it sinks to its knees, and shrinks to what it was: "...one. I am only one." Everyone on the
             bridge: its spoils, a Victor's Key, the first time Vexis's Severed Link (the follower, phase243) and its record. The
             invasion nights END (p241/nights_end) and the Armada comes apart (p241/collapse: three minutes, then it re-forms).
             Whoever felled it, it won't rise for again - until they attack a Dreadnought (p241/rekindle).
ABANDONED    nobody on the bridge for 30 s: it goes back to the helm and powers down; the pylons are rebuilt."""
import math
from items import T
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF
import vexis_art as A
import p2.armadacfg as AC
import armada_lore as L
import phase152 as P152
import phase15 as P15

COL, VCOL, RED, STAR = L.VX_COL, L.HIVE, L.RED, L.STAR
OX, OY, OZ = AC.ORIGIN
W = lambda x, y, z: (OX + x, OY + y, OZ + z)
AR = AC.ARENA
END = 'minecraft:the_end'
CX, CY, CZ = W(*AR['c'])                       # the floor's top layer centre (walk y = CY + 1)
HX, HY, HZ = W(*AR['helm'])                    # (walk y)
WIN = AR['window']                             # bearing of the window (x=cos, z=sin)
WX, WZ = CX + 0.5 + 34 * math.cos(math.radians(WIN)), CZ + 0.5 + 34 * math.sin(math.radians(WIN))     # (a point beyond the glass)
YAW_HELM = (WIN + 90) % 360                    # (at the helm it faces away from the window: down the bridge)
_box = lambda r, up: f'x={CX - r},y={CY - 10},z={CZ - r},dx={2 * r},dy={up},dz={2 * r}'
FIGHT = f'@a[{_box(32, 40)},gamemode=!spectator,gamemode=!creative]'
AUD = f'@a[{_box(40, 50)}]'
ME = '@e[type=minecraft:husk,tag=bm.avx,limit=1]'
TGT = '@a[tag=bm.vxtgt,limit=1]'
HOST = {'warframe': 6.0, 'hivelink': 4.2, 'starfire': 4.6}      # (a husk 1.95 tall: ~12 / ~8 / ~9 blocks)
HOVER = {'warframe': 0, 'hivelink': 5, 'starfire': 4}           # (blocks above the deck)
PH_HP, PH_ADD, PH_MAX = 520, 140, 760
FLOOR = 100
RESIST = 1
SHIELD = 3                                      # (Resistance IV while a pylon stands: 80% of every blow turned)
INTRO = 400
ENT = {1: 280, 2: 300}
UNLINK = 600
FORM = {1: 'warframe', 2: 'hivelink', 3: 'starfire'}
SCALE = {f: A.BOSS_SCALE * A.FORM_SCALE[f] for f in FORM.values()}
SWAP = tuple(A.PARTS)
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.vxr_{p}]'
wsel = lambda p: f'@e[type=minecraft:item_display,tag=bm.vxw_{p}]'
csel = lambda i: (lambda p: f'@e[type=minecraft:item_display,tag=bm.vxc{i}_{p}]')
CLONES = 3
# ---- its music (tools/vexis_music.py, phase244)
P152.THEMES.update({26: ('vexis1', 120), 27: ('vexis2', 120), 28: ('vexis3', 120), 29: ('vexis_intro', 20), 30: ('vexis_enter2', 14), 31: ('vexis_enter3', 15),
                    32: ('vexis_unlink', 30)})
_H = 'type=minecraft:husk,tag=bm.avx'
P152.WHO_LATE += [(26, f'{_H},tag=bm.vxlive,scores={{bm.vxph=1}}'), (27, f'{_H},tag=bm.vxlive,scores={{bm.vxph=2}}'), (28, f'{_H},tag=bm.vxlive,scores={{bm.vxph=3}}'),
                  (30, f'{_H},tag=bm.vxturn,tag=bm.vxt1'), (31, f'{_H},tag=bm.vxturn,tag=bm.vxt2'), (29, f'{_H},tag=bm.vxintro'), (32, f'{_H},tag=bm.vxfall')]

# ---- the Starforged set (p2/armadaitems): hover-jets, a star-shield
P15.SET_FX['starforged'] = (['effect give @s minecraft:slow_falling 2 0 true', 'execute unless entity @s[nbt={OnGround:1b}] run function bm:p242/sf/jet',
                             'function bm:p242/sf/shield'],
                            'minecraft:dust{color:[1.0,0.7,0.3],scale:1.0}', 'particle minecraft:flame ~ ~0.1 ~ 0.15 0 0.15 0.01 1')


def pp(f, *names):
    """the first of these poses the form has (else its idle)"""
    P = A.BOSS_POSES[f]
    return next((n for n in names if n in P), 'idle_a')


# ---- the states and their frames: (period or None, [(tick, pose)]) per form
def _cyc(f):
    P = A.BOSS_POSES[f]
    c = {0: (80, [(0, 'idle_a'), (40, pp(f, 'idle_b'))]), 1: (24, [(0, pp(f, 'walk_0')), (6, pp(f, 'walk_1')), (12, pp(f, 'walk_2')), (18, pp(f, 'walk_3'))]),
         11: (None, [(0, pp(f, 'roar'))]), 12: (None, [(0, pp(f, 'deploy', 'summon', 'roar'))]), 22: (None, [(0, pp(f, 'stagger', 'roar'))])}
    if f == 'warframe':
        c[7] = (None, [(0, pp(f, 'cannon_up')), (16, pp(f, 'cannon'))])
        c[8] = (None, [(0, pp(f, 'missiles'))])
        c[9] = (None, [(0, pp(f, 'stomp_up')), (14, pp(f, 'stomp'))])
        c[20] = (None, [(0, pp(f, 'dormant'))])
        c[21] = (None, [(0, pp(f, 'dormant'))] + [(t, n) for t, n in ((100, 'wake_0'), (170, 'wake_1'), (240, 'wake_2'), (300, 'wake_3')) if n in P] + [(340, pp(f, 'roar'))])
    else:
        c[13] = (None, [(0, pp(f, 'gravity'))])
        c[14] = (None, [(0, pp(f, 'beam_up')), (20, pp(f, 'beam'))])
        c[15] = (None, [(0, pp(f, 'clone'))])
        c[23] = (None, [(0, pp(f, 'rise', 'roar'))])
    if f == 'starfire':
        c[16] = (None, [(0, pp(f, 'flare_up')), (30, pp(f, 'flare'))])
        c[17] = (None, [(0, pp(f, 'lance_up')), (26, pp(f, 'lance'))])
        c[18] = (None, [(0, pp(f, 'frenzy', 'roar'))])
        c[31] = (None, [(0, pp(f, 'death_0', 'stagger')), (60, pp(f, 'death_1', 'stagger')), (160, pp(f, 'death_2', 'stagger'))])
    return c


CYC = {f: _cyc(f) for f in FORM.values()}
DUR = {'idle_a': 30, 'idle_b': 30, 'dormant': 10, 'wake_0': 40, 'wake_1': 40, 'wake_2': 40, 'wake_3': 30, 'roar': 10, 'cannon_up': 14, 'cannon': 4,
       'missiles': 12, 'stomp_up': 12, 'stomp': 3, 'deploy': 12, 'summon': 12, 'gravity': 14, 'beam_up': 14, 'beam': 6, 'clone': 10, 'rise': 40,
       'flare_up': 20, 'flare': 5, 'lance_up': 18, 'lance': 4, 'frenzy': 10, 'stagger': 14, 'death_0': 20, 'death_1': 40, 'death_2': 60,
       **{f'walk_{i}': 6 for i in range(4)}}
CLOSE = lambda r: f'if entity {TGT[:-1]},distance=..{r}]'
ATK = {'warframe': [(12, 40, 520, '', {20: 'pods'}),
                    (8, 50, 240, '', {44: 'missile_mark'}),
                    (7, 46, 170, '', {30: 'cannon_start', **{x: 'cannon' for x in range(29, 5, -1)}}),
                    (9, 34, 120, CLOSE(14), {18: 'stomp'})],
       'hivelink': [(12, 30, 500, '', {15: 'drones'}),
                    (15, 200, 640, '', {196: 'clone', 150: 'cbeam', 110: 'cbeam', 70: 'cbeam', 30: 'cbeam', 2: 'clone_end'}),
                    (13, 40, 260, '', {30: 'well'}),
                    (14, 60, 200, '', {40: 'ibeam_start', **{x: 'ibeam' for x in range(39, 9, -1)}})],
       'starfire': [(12, 30, 520, '', {15: 'drones'}),
                    (16, 60, 240, '', {50: 'flare_warn', 20: 'flare'}),
                    (17, 50, 180, '', {44: 'lance_aim', **{x: 'lance_track' for x in range(43, 25, -1)}, 24: 'lance_fire'}),
                    (13, 40, 320, '', {30: 'flip'}),
                    (14, 60, 260, '', {40: 'ibeam_start', **{x: 'ibeam' for x in range(39, 9, -1)}})]}
STATES = sorted({a[0] for v in ATK.values() for a in v})


def ring_pts(r, n):
    return [(round(r * math.cos(2 * math.pi * k / n), 2), round(r * math.sin(2 * math.pi * k / n), 2)) for k in range(n)]


def textures():
    return A.textures()


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)


def generate(G):
    fn, title, tellraw, give, wjson = G.fn, G.title, G.tellraw, G.give, G.wjson
    tick, fast, second = G.FUNCS['tick'], G.FUNCS['loop/fast'], G.FUNCS['loop/second']
    P = G.PREFIX
    objs = ['bm.vxph', 'bm.vxa', 'bm.vxx', 'bm.vxf', 'bm.vxs', 'bm.vxt', 'bm.vxg', 'bm.vxz', 'bm.vxwin', 'bm.vxhp', 'bm.vxp', 'bm.vxsc', 'bm.vxjc'] + \
           [f'bm.vxk{s}' for s in STATES]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        f'bossbar add bm:vexis {snbt(T(L.VX, COL, bold=True))}', 'bossbar set bm:vexis color green', 'bossbar set bm:vexis style notched_10']
    G.OBJECTIVES += objs
    say = lambda line, who=AUD: tellraw(who, [T(L.VX + ': ', COL, bold=True), T(line, VCOL, italic=True)])
    snd = lambda s, v, p, who=AUD: f'execute as {who} at @s run playsound minecraft:{s} hostile @s ~ ~ ~ {v} {p}'
    at = lambda t, cmd: f'execute if score @s bm.vxt matches {t} run {cmd}'
    import phase241
    M = phase241.build().meta['armada']
    PYL = sorted(M['pylons'])

    # ================================================================== the rig: summoned once, posed by form
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.vxr", f"bm.vxr_{p}", "bm.avx_part"], SCALE["warframe"], model=A.model_name(p, A.BOSS_POSES["warframe"][pp("warframe", "dormant")]), extra=dict(view_range=F(5.0), brightness={"block": Int(12), "sky": Int(12)}))}'
           for p in A.PARTS]
    for f in FORM.values():
        fn(f'p242/place/{f}', RF.place(A, SCALE[f] / 16, sel))
        for name, pz in A.BOSS_POSES[f].items():
            fn(f'p242/pose/{f}/{name}', RF.pose(A, pz, SCALE[f], DUR.get(name, 6), sel, swap=SWAP))
        RF.cycles(fn, f'p242/{f}', CYC[f], 'bm.vxf', 'bm.vxs', lambda p, f=f: f'p242/pose/{f}/{p}')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for f in FORM.values() for n in RF.periods(CYC[f])]
    host = {'Tags': ['bm.avx', 'bm.boss', 'bm.seen', 'bm.vxnew'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T(L.VX, COL), 'Invulnerable': B(1), 'DeathLootTable': 'minecraft:empty',
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(PH_HP + FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(HOST['warframe'])},
                           {'id': 'minecraft:armor', 'base': Dd(20)}, {'id': 'minecraft:armor_toughness', 'base': Dd(10)},
                           {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)}, {'id': 'minecraft:follow_range', 'base': Dd(64)}],
            'Health': F(PH_HP + FLOOR),
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    fn('p242/spawn', [f'execute in {END} positioned {HX + 0.5} {HY} {HZ + 0.5} rotated {YAW_HELM:.1f} 0 run summon minecraft:husk ~ ~ ~ {snbt(host)}',
                      f'execute in {END} positioned {HX + 0.5} {HY} {HZ + 0.5} run function bm:p242/rig',
                      f'execute as {ME} at @s run function bm:p242/dormant'])
    fn('p242/rig', rig + ['tag @e[tag=bm.vxnew] remove bm.vxnew'])
    fn('p242/dormant', ['scoreboard players set @s bm.vxph 1', 'scoreboard players set @s bm.vxa 20', 'scoreboard players set @s bm.vxx 0',
                        'scoreboard players set @s bm.vxs -1', 'scoreboard players set @s bm.vxf 0', 'scoreboard players set @s bm.vxg 0',
                        'tag @s add bm.vxdorm', 'tag @s remove bm.vxlive', 'data modify entity @s Invulnerable set value 1b', 'data modify entity @s NoGravity set value 0b',
                        f'attribute @s minecraft:scale base set {HOST["warframe"]}',
                        f'execute rotated {YAW_HELM:.1f} 0 run tp @s {HX + 0.5} {HY} {HZ + 0.5} {YAW_HELM:.1f} 0', f'execute rotated {YAW_HELM:.1f} 0 run function bm:p242/place/warframe',
                        f'function bm:p242/pose/warframe/{pp("warframe", "dormant")}'])
    # (one Admiral, at its helm, whenever the bridge is loaded and the fleet hasn't fallen)
    second.append(f'execute if score #afell bm.p2 matches 0 if entity @e[type=minecraft:marker,tag=bm.ahelm] unless entity {ME} run function bm:p242/spawn')

    # ================================================================== every tick: its mind, its body
    tick.append(f'execute as {ME} at @s run function bm:p242/tick')
    form_of = lambda f: [f'execute if score @s bm.vxph matches {i} run function bm:p242/{FORM[i]}/{f}' for i in FORM]
    fn('p242/tick', ['tag @a[tag=bm.vxtgt] remove bm.vxtgt',
                     f'tag {FIGHT[:-1]},sort=nearest,limit=1] add bm.vxtgt',
                     'execute if entity @s[tag=bm.vxdorm] run return run function bm:p242/asleep',
                     'execute if entity @s[tag=bm.vxintro] run function bm:p242/intro',
                     'execute store result score #hp bm.rng run data get entity @s Health',
                     'execute if entity @s[tag=bm.vxlive] run function bm:p242/frenzy_chk',
                     f'execute if entity @s[tag=bm.vxlive] if score #hp bm.rng matches ..{FLOOR} run function bm:p242/floor_hit',
                     'execute if score @s bm.vxx matches 1.. run scoreboard players remove @s bm.vxx 1'] +
       [f'execute if score @s bm.vxk{s} matches 1.. run scoreboard players remove @s bm.vxk{s} 1' for s in STATES] +
       ['execute if entity @s[tag=bm.vxlive] if entity @a[tag=bm.vxtgt] run function bm:p242/mind'] + form_of('beats') +
       ['execute if entity @s[tag=bm.vxturn] run function bm:p242/turn_tick',
        'execute if entity @s[tag=bm.vxfall] run function bm:p242/falling',
        'function bm:p242/state',
        'execute if score #st bm.rng = @s bm.vxs run scoreboard players add @s bm.vxf 1',
        'execute unless score #st bm.rng = @s bm.vxs run scoreboard players set @s bm.vxf 0',
        'scoreboard players operation @s bm.vxs = #st bm.rng'] + form_of('body'))
    for i, f in FORM.items():
        fn(f'p242/{f}/body', [f'function bm:p242/{f}/anim', 'execute if entity @s[tag=bm.vxsmall] rotated as @s rotated ~ 0 run return run function bm:p242/place/small',
                              f'execute rotated as @s rotated ~ 0 run function bm:p242/place/{f}'])
    fn('p242/asleep', [f'execute rotated {YAW_HELM:.1f} 0 run function bm:p242/place/warframe',
                       f'execute positioned {CX} {CY + 1} {CZ} if entity @a[distance=..22,gamemode=!spectator,gamemode=!creative,tag=!bm.vxdone] run function bm:p242/wake',
                       f'execute positioned {CX} {CY + 1} {CZ} as @a[distance=..26,gamemode=!spectator,tag=bm.vxdone] run function bm:p242/stirless'])
    fn('p242/stirless', ['execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #60 bm.rng',
                         'execute unless score #g bm.rng matches 0..2 run return 0',
                         title('@s', 'actionbar', [T('The warframe stays dark for you. ', COL, italic=True), T('Attack a Dreadnought again, and the hive will remember you.', 'gray')])])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #60 bm.rng 60']
    fn('p242/state', ['execute if score @s bm.vxx matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.vxa',
                      'execute if entity @s[tag=bm.vxmove] run return run scoreboard players set #st bm.rng 1', 'scoreboard players set #st bm.rng 0'])

    # ---- its mind: an attack it's ready for, else it closes on its quarry (keeping to its bridge; aloft in the later forms)
    for f, atks in ATK.items():
        choose = [' '.join(x for x in [f'execute unless score @s bm.vxx matches 1.. unless score @s bm.vxk{st} matches 1..', cond, f'run function bm:p242/go{st}'] if x)
                  for st, _d, _cd, cond, _b in atks]
        fn(f'p242/{f}/mind', choose + [f'execute unless score @s bm.vxx matches 1.. run function bm:p242/move'])
        beats = []
        for st, _d, _cd, _c, bt in atks:
            for x, f_ in bt.items():
                beats.append(f'execute if score @s bm.vxa matches {st} if score @s bm.vxx matches {x} run function bm:p242/a/{f_}')
        fn(f'p242/{f}/beats', beats)
    for st in STATES:
        cd = next(a[2] for v in ATK.values() for a in v if a[0] == st)
        fn(f'p242/go{st}', [f'scoreboard players set @s bm.vxa {st}', f'function bm:p242/dur{st}', f'scoreboard players set @s bm.vxk{st} {cd}',
                            f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~'])
        fn(f'p242/dur{st}', [f'execute if score @s bm.vxph matches {i} run scoreboard players set @s bm.vxx {a[1]}' for i, f in FORM.items() for a in ATK[f] if a[0] == st])
    fn('p242/mind', form_of('mind'))
    fn('p242/move', [f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~', 'tag @s remove bm.vxmove',
                     f'execute unless entity @s[x={CX - 22},y={CY - 10},z={CZ - 22},dx=44,dy=40,dz=44] facing {CX} {CY + 1} {CZ} rotated ~ 0 run return run function bm:p242/step',
                     f'execute if score @s bm.vxph matches 1 if entity {TGT[:-1]},distance=7..] rotated as @s rotated ~ 0 if block ^ ^1 ^3 #bm:grap_pass if block ^ ^2 ^3 #bm:grap_pass run function bm:p242/step',
                     f'execute if score @s bm.vxph matches 2.. if entity {TGT[:-1]},distance=9..] run function bm:p242/step',
                     # (aloft: it keeps to its height over the deck)
                     *[f'execute if score @s bm.vxph matches {i} unless entity @s[y={CY + 1 + HOVER[FORM[i]] - 0.3},dy=0.6] run function bm:p242/hover{i}' for i in (2, 3)]])
    for i in (2, 3):
        hy = CY + 1 + HOVER[FORM[i]]
        fn(f'p242/hover{i}', [f'execute if entity @s[y={hy},dy=40] run tp @s ~ ~-0.08 ~', f'execute if entity @s[y={CY - 20},dy={hy - CY + 20 - 0.01}] run tp @s ~ ~0.08 ~'])
    fn('p242/step', ['tag @s add bm.vxmove', 'execute if score @s bm.vxph matches 1 rotated as @s rotated ~ 0 run tp @s ^ ^ ^0.13',
                     'execute if score @s bm.vxph matches 2.. rotated as @s rotated ~ 0 run tp @s ^ ^ ^0.16',
                     'execute if score @s bm.vxph matches 1 if score @s bm.vxf matches 0 run function bm:p242/a/footfall',
                     'execute if score @s bm.vxph matches 1 if score @s bm.vxf matches 12 run function bm:p242/a/footfall',
                     'execute if score @s bm.vxph matches 2.. run particle minecraft:reverse_portal ~ ~ ~ 1 0.2 1 0.02 6 force'])

    # ================================================================== THE COMING (20 s)
    hx, hy, hz = HX + 0.5, HY + 7.5, HZ + 0.5                 # (its cockpit, standing)
    look = '@e[type=minecraft:marker,tag=bm.vxlook,limit=1]'
    fn('p242/c/look', [f'execute as {FIGHT} at @s run tp @s ~ ~ ~ facing entity {look} feet', f'effect give {FIGHT} minecraft:slowness 2 255 true',
                       f'effect give {FIGHT} minecraft:resistance 2 255 true', f'effect give {FIGHT} minecraft:jump_boost 2 200 true'])
    import random
    rs = random.Random(242)
    shk = [(1.4 * (1 - k / 3) * rs.choice((-1, 1)), 0.8 * (1 - k / 3) * rs.choice((-1, 1))) for k in range(2)]
    fn('p242/c/shake', [f'execute as {FIGHT} at @s run rotate @s ~{dx:.2f} ~{dy:.2f}' for dx, dy in shk])
    # (the systems lighting, section by section: legs, reactor, arms, cockpit - sparks and a hum at each)
    sect = [(1.2, 'legs'), (4.0, 'reactor'), (6.5, 'arms'), (8.5, 'cockpit')]
    for k, (yy, _nm) in enumerate(sect):
        fn(f'p242/c/sys{k}', [f'particle minecraft:electric_spark {HX + 0.5} {HY + yy} {HZ + 0.5} 2.2 0.6 2.2 0.4 60 force {AUD}',
                              f'particle minecraft:dust{{color:[0.48,1.0,0.42],scale:2.4}} {HX + 0.5} {HY + yy} {HZ + 0.5} 2.4 0.5 2.4 0 40 force {AUD}',
                              f'particle minecraft:flash{{color:[0.5,1.0,0.45,1.0]}} {HX + 0.5} {HY + yy} {HZ + 0.5} 0 0 0 0 1 force {AUD}',
                              snd('block.beacon.power_select', 2, 0.5 + 0.15 * k), snd('block.respawn_anchor.charge', 1.5, 0.6 + 0.1 * k), snd('entity.iron_golem.repair', 1.5, 0.5)])
    # (the window floods red: light streams in from the star)
    stream = [f'particle minecraft:dust{{color:[1.0,0.35,0.12],scale:3.0}} {WX + (CX + 0.5 - WX) * k / 14:.2f} {CY + 12 + rs.uniform(-6, 10):.1f} {WZ + (CZ + 0.5 - WZ) * k / 14:.2f} 2 3 2 0 6 force {AUD}'
              for k in range(15)]
    fn('p242/c/flood', stream + [f'particle minecraft:flame {WX:.1f} {CY + 14} {WZ:.1f} 6 10 6 0.05 30 force {AUD}'])
    hum = (1, 30, 56, 80, 102, 122, 140, 156, 170, 184, 196, 208, 218, 228, 238, 246, 254, 262, 270, 278, 286, 294, 302, 310)
    seq = ([at(1, 'function bm:p242/c/door'), at(1, f'effect give {FIGHT} minecraft:darkness 18 0 true'), at(1, snd('block.beacon.deactivate', 2, 0.4)),
            at(1, snd('block.iron_door.close', 2, 0.4)), at(1, snd('block.piston.contract', 2, 0.4)),
            at(1, title(AUD, 'actionbar', T('The bulkhead seals behind you. The bridge goes dark.', 'gray', italic=True)))] +
           [at(t, snd('block.conduit.ambient.short', 1.6, 0.5 + j * 0.03)) for j, t in enumerate(hum)] +
           [at(t, snd('block.beacon.ambient', 1.2 + j * 0.1, 0.5 + j * 0.05)) for j, t in enumerate(range(20, 300, 40))] +
           [at(40, tellraw(AUD, [T('THE HIVE: ', VCOL, bold=True), T(L.VOICE['helm'], VCOL, italic=True)]))] +
           [at(100 + 70 * k, f'function bm:p242/c/sys{k}') for k in range(len(sect))] +
           [at(100 + 70 * k, 'function bm:p242/c/shake') for k in range(len(sect))] +
           [at('120..360', 'function bm:p242/c/flood')] +
           [at(120, snd('block.end_portal.spawn', 1.5, 0.5)), at(120, title(AUD, 'actionbar', T('Behind it, the window floods with the light of the Hive-Star.', STAR, italic=True)))] +
           [at(240, f'execute as @e[type=minecraft:item_display,tag=bm.vxr] run data merge entity @s {{brightness:{{block:15,sky:15}}}}'),
            at(250, say(L.FIGHT['wake'][0])),
            at(300, snd('entity.iron_golem.step', 3, 0.3)), at(316, snd('entity.iron_golem.step', 3, 0.3)), at(300, 'function bm:p242/c/shake'), at(316, 'function bm:p242/c/shake'),
            at(320, snd('block.piston.extend', 3, 0.4)), at(320, snd('entity.blaze.shoot', 2, 0.4)),
            at(320, f'particle minecraft:electric_spark {hx} {hy} {hz} 3 3 3 0.4 120 force {AUD}'),
            # (THE ROAR - the shoulder pods open, the cannon comes up)
            at(340, snd('entity.ender_dragon.growl', 3, 0.6)), at(340, snd('entity.warden.roar', 3, 0.7)), at(340, snd('entity.generic.explode', 2, 0.6)),
            at(340, snd('block.beacon.activate', 3, 0.5)), at(340, f'particle minecraft:explosion_emitter {hx} {HY + 4} {hz} 2 2 2 0 3 force {AUD}'),
            at(340, f'particle minecraft:end_rod {hx} {hy} {hz} 6 5 6 0.12 300 force {AUD}'), at(340, 'function bm:p242/c/wave'),
            at(341, f'effect clear {FIGHT} minecraft:darkness')] +
           [at(t, 'function bm:p242/c/shake') for t in range(340, 368, 4)] +
           [at(342, f'title {AUD} times 4 70 20'), at(342, title(AUD, 'title', T(L.VX.upper(), COL, bold=True))),
            at(342, title(AUD, 'subtitle', T('Voice of the Hive', VCOL, italic=True))),
            at(380, title(AUD, 'actionbar', T('Four shield pylons guard it. Strike each one while it glows!', '#9adf8a', bold=True))),
            at(INTRO, 'function bm:p242/begin'),
            at(f'1..{INTRO - 2}', 'function bm:p242/c/look')])
    fn('p242/c/wave', [f'particle minecraft:dust{{color:[0.48,1.0,0.42],scale:3.0}} {HX + 0.5 + x:.2f} {HY + 0.3} {HZ + 0.5 + z:.2f} 0.2 0.05 0.2 0 2 force {AUD}'
                       for r_ in (4, 10, 18) for x, z in ring_pts(r_, int(5 * r_))])
    fn('p242/intro', ['scoreboard players add @s bm.vxt 1'] + seq)
    fn('p242/c/door', [f'execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_{AC.d}] at @s run function bm:p2/{AC.d}/adoor_close'])
    fn('p242/c/door_open', [f'execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_{AC.d}] at @s run function bm:p2/{AC.d}/adoor_open'])
    fn('p242/wake', ['tag @s remove bm.vxdorm', 'tag @s add bm.vxintro', 'scoreboard players set @s bm.vxt 0', 'scoreboard players set @s bm.vxa 21',
                     f'scoreboard players set @s bm.vxx {INTRO + 4}', 'kill @e[type=minecraft:marker,tag=bm.vxlook]',
                     f'summon minecraft:marker {hx} {hy} {hz} {{Tags:["bm.vxlook"]}}',
                     f'execute store result score #n bm.rng if entity {FIGHT}', 'scoreboard players remove #n bm.rng 1',
                     f'scoreboard players set #ph bm.rng {PH_ADD}', 'scoreboard players operation #n bm.rng *= #ph bm.rng',
                     f'scoreboard players add #n bm.rng {PH_HP}', f'execute if score #n bm.rng matches {PH_MAX}.. run scoreboard players set #n bm.rng {PH_MAX}',
                     'scoreboard players operation @s bm.vxhp = #n bm.rng', 'function bm:p242/pyl/build',
                     f'execute as {AUD} at @s run function bm:p152/tick'])
    fn('p242/begin', ['tag @s remove bm.vxintro', 'tag @s add bm.vxlive', 'data modify entity @s Invulnerable set value 0b', 'scoreboard players set @s bm.vxa 0',
                      'kill @e[type=minecraft:marker,tag=bm.vxlook]',
                      'scoreboard players set @s bm.vxx 20', 'function bm:p242/fill', 'bossbar set bm:vexis visible true',
                      f'bossbar set bm:vexis name {snbt([T(L.VX, COL, bold=True), T("  -  " + L.FIGHT["p1"], "#9adf8a")])}', 'bossbar set bm:vexis color green',
                      'scoreboard players set @s bm.vxk12 240', 'function bm:p242/pyl/all_on', f'execute as {AUD} at @s run function bm:p152/tick'])
    fn('p242/sethp', ['$attribute @s minecraft:max_health base set $(m)', '$data modify entity @s Health set value $(m).0f'])
    fn('p242/fill', ['scoreboard players operation #m bm.rng = @s bm.vxhp', f'scoreboard players add #m bm.rng {FLOOR}',
                     'execute store result storage bm:p242 hp.m int 1 run scoreboard players get #m bm.rng',
                     'function bm:p242/sethp with storage bm:p242 hp',
                     f'effect give @s minecraft:resistance infinite {RESIST} true', 'execute store result bossbar bm:vexis max run scoreboard players get @s bm.vxhp'])
    # ---- every second: the bar, its shield; nobody left on the bridge for 30 s -> back to its helm
    second.append(f'execute as {ME} at @s run function bm:p242/sec')
    fn('p242/sec', ['execute if entity @s[tag=bm.vxdorm] run return 0',
                    'execute store result score #hp bm.rng run data get entity @s Health', f'scoreboard players remove #hp bm.rng {FLOOR}',
                    'execute if score #hp bm.rng matches ..-1 run scoreboard players set #hp bm.rng 0',
                    'execute store result bossbar bm:vexis value run scoreboard players get #hp bm.rng', f'bossbar set bm:vexis players {AUD}',
                    f'execute if entity {FIGHT} run scoreboard players set @s bm.vxg 0', f'execute unless entity {FIGHT} run scoreboard players add @s bm.vxg 1',
                    'execute if score @s bm.vxg matches 30.. run return run function bm:p242/abandon',
                    'execute if score @s bm.vxph matches 1 if entity @s[tag=bm.vxlive] run function bm:p242/pyl/sec',
                    'execute if score @s bm.vxz matches 1.. run function bm:p242/frenzy_sec',
                    f'execute unless score @s bm.vxph matches 1 unless score @s bm.vxz matches -99..-1 run effect give @s minecraft:resistance infinite {RESIST} true'])
    fn('p242/abandon', [say(L.FIGHT['abandon']), 'function bm:p242/clear', 'function bm:p242/c/door_open', 'function bm:p242/pyl/clear',
                        'bossbar set bm:vexis visible false', 'kill @e[type=minecraft:item_display,tag=bm.vxr]', 'kill @e[type=minecraft:item_display,tag=bm.vxw]',
                        'kill @e[type=minecraft:marker,tag=bm.vxlook]', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p242/clear', ['kill @e[tag=bm.vxk]', 'kill @e[type=minecraft:marker,tag=bm.vxfx]', 'function bm:p242/a/clone_end', 'tag @a remove bm.vximp'])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.avx]', 'kill @e[tag=bm.vxr]', 'kill @e[tag=bm.vxw]', 'kill @e[tag=bm.vxc]', 'kill @e[tag=bm.vxcl]',
                                       'kill @e[tag=bm.vxfx]', 'kill @e[tag=bm.vxpy]', 'kill @e[tag=bm.vxlook]', 'bossbar remove bm:vexis']

    # ================================================================== THE SHIELD PYLONS (phase I)
    crys = lambda lit: {'Tags': ['bm.vxpy', 'bm.vxpyd'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:vx_pylon' if lit else 'bm:vx_pylon_off'}},
                        'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)},
                        'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.6), F(0)], 'scale': [F(1.6)] * 3}}
    fn('p242/pyl/build', [f'execute as @e[type=minecraft:marker,tag=bm.apylon,tag=bm.d_{AC.d}] at @s run function bm:p242/pyl/make'])
    fn('p242/pyl/make', ['execute if entity @e[type=minecraft:interaction,tag=bm.vxpyi,distance=..1] run return 0', f'summon minecraft:item_display ~0.5 ~ ~0.5 {snbt(crys(True))}',
                         'summon minecraft:interaction ~0.5 ~ ~0.5 {Tags:["bm.vxpy","bm.vxpyi"],width:1.4f,height:1.8f,response:1b}', 'scoreboard players set @s bm.vxp 0'])
    fn('p242/pyl/clear', ['kill @e[tag=bm.vxpy]', f'tag @e[type=minecraft:marker,tag=bm.apylon] remove bm.vxpl', f'tag @e[type=minecraft:marker,tag=bm.apylon] remove bm.vxpc'])
    fn('p242/pyl/all_on', ['tag @e[type=minecraft:marker,tag=bm.apylon,tag=bm.d_armada] add bm.vxpl', f'effect give @s minecraft:resistance infinite {SHIELD} true'] +
       [f'scoreboard players set @e[type=minecraft:marker,tag=bm.ap{i}] bm.vxp {k * 2}' for k, (i, *_xyz) in enumerate(PYL)])
    # (each second: each standing pylon's charge counts round 8 - charged (glowing, open to a blow) for three of them; a fallen one
    #  counts down 30 to rise again; the shield is up while any stands)
    fn('p242/pyl/sec', ['execute as @e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl] at @s run function bm:p242/pyl/beat',
                        'execute as @e[type=minecraft:marker,tag=bm.apylon,tag=!bm.vxpl] at @s run function bm:p242/pyl/down_sec',
                        'execute if entity @e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl] run return run effect give @s minecraft:resistance infinite ' + str(SHIELD) + ' true',
                        'execute unless score @s bm.vxz matches -99..-1 run effect give @s minecraft:resistance infinite 0 true'])
    fn('p242/pyl/beat', ['scoreboard players add @s bm.vxp 1', 'execute if score @s bm.vxp matches 8.. run scoreboard players set @s bm.vxp 0',
                         'execute if score @s bm.vxp matches 5..7 run tag @s add bm.vxpc', 'execute unless score @s bm.vxp matches 5..7 run tag @s remove bm.vxpc',
                         'execute if score @s bm.vxp matches 5 run playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..40] ~ ~ ~ 1.2 1.2',
                         'execute if entity @s[tag=bm.vxpc] run particle minecraft:end_rod ~0.5 ~1 ~0.5 0.5 0.8 0.5 0.05 30 force',
                         'execute if entity @s[tag=bm.vxpc] run particle minecraft:dust{color:[0.5,1.0,0.4],scale:2.5} ~0.5 ~1 ~0.5 0.6 0.8 0.6 0 20 force',
                         # (its tether to the frame)
                         f'execute positioned ~0.5 ~1 ~0.5 facing entity {ME} eyes run function bm:p242/pyl/tether'])
    fn('p242/pyl/tether', [f'particle minecraft:dust{{color:[0.48,1.0,0.42],scale:1.2}} ^ ^ ^{k} 0.05 0.05 0.05 0 1 force' for k in range(2, 22, 2)])
    fn('p242/pyl/down_sec', ['execute if score @s bm.vxp matches 1.. run scoreboard players remove @s bm.vxp 1', 'particle minecraft:smoke ~0.5 ~1 ~0.5 0.3 0.5 0.3 0.02 4 force',
                             'execute if score @s bm.vxp matches 0 run function bm:p242/pyl/rise'])
    fn('p242/pyl/rise', ['tag @s add bm.vxpl', 'scoreboard players set @s bm.vxp 0', 'kill @e[type=minecraft:item_display,tag=bm.vxpyd,distance=..1.5]',
                         f'summon minecraft:item_display ~0.5 ~ ~0.5 {snbt(crys(True))}', 'playsound minecraft:block.beacon.activate hostile @a[distance=..48] ~ ~ ~ 1.5 1.2',
                         title(AUD, 'actionbar', T('A shield pylon hums back to life!', RED, bold=True))])
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.vxpyi] if data entity @s attack at @s run function bm:p242/pyl/struck')
    fn('p242/pyl/struck', ['data remove entity @s attack',
                           'execute positioned ~-0.5 ~ ~-0.5 as @e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl,tag=bm.vxpc,distance=..1.2,limit=1] at @s run return run function bm:p242/pyl/overload',
                           'playsound minecraft:block.anvil.land hostile @a[distance=..16] ~ ~ ~ 0.6 1.8', 'particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.2 10',
                           title('@a[distance=..6]', 'actionbar', T('The pylon shrugs it off - strike it while it GLOWS.', 'gray'))])
    fn('p242/pyl/overload', ['tag @s remove bm.vxpl', 'tag @s remove bm.vxpc', 'scoreboard players set @s bm.vxp 30',
                             'kill @e[type=minecraft:item_display,tag=bm.vxpyd,distance=..1.5]', f'summon minecraft:item_display ~0.5 ~ ~0.5 {snbt(crys(False))}',
                             'particle minecraft:explosion_emitter ~0.5 ~1 ~0.5 0 0 0 0 1 force', 'particle minecraft:electric_spark ~0.5 ~1 ~0.5 1 1 1 0.5 80 force',
                             'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 1.2', 'playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 2 0.6',
                             title(AUD, 'actionbar', T(L.FIGHT['pylon'], '#9adf8a')),
                             'execute unless entity @e[type=minecraft:marker,tag=bm.apylon,tag=bm.vxpl] run function bm:p242/pyl/exposed'])
    fn('p242/pyl/exposed', [title(AUD, 'actionbar', T(L.FIGHT['pylons_all'], 'gold', bold=True)), f'execute as {ME} run effect clear @s minecraft:resistance',
                            f'execute as {ME} at @s run particle minecraft:electric_spark ~ ~6 ~ 2 4 2 0.4 120 force', snd('entity.iron_golem.damage', 2, 0.4)])

    # ================================================================== THE TURNS
    fn('p242/floor_hit', ['execute if score @s bm.vxph matches 3 run return run function bm:p242/fall',
                          'tag @s remove bm.vxlive', 'tag @s add bm.vxturn', 'data modify entity @s Invulnerable set value 1b', 'scoreboard players set @s bm.vxt 0',
                          'scoreboard players set @s bm.vxa 22', 'function bm:p242/clear',
                          f'execute if score @s bm.vxph matches 1 run scoreboard players set @s bm.vxx {ENT[1] + 4}', f'execute if score @s bm.vxph matches 2 run scoreboard players set @s bm.vxx {ENT[2] + 4}',
                          'execute if score @s bm.vxph matches 1 run tag @s add bm.vxt1', 'execute if score @s bm.vxph matches 2 run tag @s add bm.vxt2',
                          'kill @e[type=minecraft:marker,tag=bm.vxlook]', 'execute at @s run summon minecraft:marker ~ ~7.5 ~ {Tags:["bm.vxlook"]}',
                          'bossbar set bm:vexis color purple', f'execute as {AUD} at @s run function bm:p152/tick'])
    rs2 = random.Random(2421)
    for k in range(6):
        fn(f'p242/c/spark{k}', [f'particle minecraft:electric_spark ~{rs2.uniform(-2.5, 2.5):.1f} ~{rs2.uniform(4, 10):.1f} ~{rs2.uniform(-2.5, 2.5):.1f} 0.6 0.6 0.6 0.4 50 force {AUD}',
                                f'particle minecraft:lava ~{rs2.uniform(-2, 2):.1f} ~{rs2.uniform(5, 9):.1f} ~{rs2.uniform(-2, 2):.1f} 0.3 0.3 0.3 0 6 force {AUD}',
                                snd('block.anvil.land', 1.2, 0.5 + 0.05 * k), snd('entity.iron_golem.damage', 1.5, 0.4 + 0.04 * k)])
    beat = lambda t0, t1, step: [at(t, snd('block.beacon.ambient', 2, 0.5)) for t in range(t0, t1, step)]
    # (the warframe's wreck: its shell left kneeling where it fell - cover in the later phases)
    wreck = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.vxw", f"bm.vxw_{p}"], SCALE["warframe"], model=A.model_name(p, A.BOSS_POSES["warframe"][pp("warframe", "dormant", "stagger")]), extra=dict(view_range=F(5.0), brightness={"block": Int(6), "sky": Int(6)}))}'
             for p in A.PARTS]
    fn('p242/wreck', wreck + ['execute rotated ~ 0 run function bm:p242/wreck_place', 'summon minecraft:marker ~ ~ ~ {Tags:["bm.vxfx","bm.vxwreck"]}'])
    fn('p242/wreck_place', RF.place(A, SCALE['warframe'] / 16, wsel))
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxwreck] at @s if predicate bm:p238/third run particle minecraft:smoke ~ ~6 ~ 1 2 1 0.02 2 force')
    turn1 = ([at(1, say(L.FIGHT['turn1'])), at(1, snd('entity.iron_golem.death', 2, 0.4)), at(1, snd('block.anvil.destroy', 2, 0.5)),
              at(1, 'function bm:p242/pose/warframe/' + pp('warframe', 'stagger', 'roar')), at(1, f'effect give {FIGHT} minecraft:darkness 6 0 true'),
              at(1, title(AUD, 'actionbar', T('The warframe staggers. Its cockpit is cracking.', '#9adf8a', italic=True)))] +
             beat(10, 120, 14) + [at(10 + 16 * k, f'function bm:p242/c/spark{k}') for k in range(6)] +
             [at(t, snd('block.glass.hit', 2, 0.5 + 0.1 * j)) for j, t in enumerate(range(30, 110, 16))] +
             # (the cockpit blows: the shell kneels, empty; out of it climbs Vexis)
             [at(110, f'particle minecraft:explosion_emitter ~ ~7 ~ 1 1 1 0 3 force {AUD}'), at(110, snd('entity.generic.explode', 3, 0.5)), at(110, snd('block.glass.break', 3, 0.4)),
              at(110, f'particle minecraft:block{{block_state:"minecraft:lime_stained_glass"}} ~ ~7 ~ 2 2 2 0 300 force {AUD}'), at(110, 'function bm:p242/c/shake'),
              at(110, 'execute rotated as @s run function bm:p242/wreck'),
              at(110, 'scoreboard players set @s bm.vxph 2'), at(110, f'attribute @s minecraft:scale base set {HOST["hivelink"]}'),
              at(110, 'tp @s ~ ~5 ~'), at(110, 'data modify entity @s NoGravity set value 1b'),
              at(110, 'function bm:p242/pose/hivelink/' + pp('hivelink', 'rise', 'roar')),
              at(110, 'execute as @e[type=minecraft:marker,tag=bm.vxlook] at @s run tp @s ~ ~1.5 ~')] +
             [at(t, 'tp @s ~ ~0.04 ~') for t in range(112, 200, 2)] +
             [at(t, 'execute as @e[type=minecraft:marker,tag=bm.vxlook] at @s run tp @s ~ ~0.04 ~') for t in range(112, 200, 2)] +
             [at('112..220', 'particle minecraft:reverse_portal ~ ~ ~ 2 0.5 2 0.05 20 force'), at(140, snd('entity.elder_guardian.curse', 2, 0.4)),
              at(150, f'particle minecraft:end_rod ~ ~4 ~ 2 3 2 0.05 80 force {AUD}'), at(180, snd('block.beacon.power_select', 2, 0.4)),
              at(220, 'function bm:p242/pose/hivelink/' + pp('hivelink', 'roar')), at(220, snd('entity.warden.roar', 3, 0.8)), at(220, snd('entity.elder_guardian.ambient', 3, 0.5)),
              at(220, f'particle minecraft:sonic_boom ~ ~5 ~ 0 0 0 0 1 force {AUD}'), at(220, 'function bm:p242/a/push')] +
             [at(t, 'function bm:p242/c/shake') for t in range(220, 236, 4)] +
             [at(222, f'title {AUD} times 4 50 16'), at(222, title(AUD, 'title', T(L.FIGHT['p2'], COL, bold=True))),
              at(222, title(AUD, 'subtitle', T('out of the shell - and into the air', '#9adf8a', italic=True))),
              at('1..270', 'function bm:p242/c/look'), at(ENT[1] - 1, 'function bm:p242/turned')])
    # (the second: it turns to the window, reaches for the star, and the star's fire pours into it)
    fn('p242/c/pour', [f'execute positioned ~ ~6 ~ facing {WX:.1f} {CY + 12} {WZ:.1f} run particle minecraft:dust{{color:[1.0,0.5,0.15],scale:3.0}} ^ ^ ^{k} 0.5 0.5 0.5 0 4 force {AUD}'
                       for k in range(2, 34, 2)] + [f'execute positioned ~ ~6 ~ facing {WX:.1f} {CY + 12} {WZ:.1f} run particle minecraft:flame ^ ^ ^{k} 0.4 0.4 0.4 0.02 3 force {AUD}'
                                                    for k in range(4, 34, 4)])
    turn2 = ([at(1, say(L.FIGHT['turn2'])), at(1, snd('entity.elder_guardian.curse', 2, 0.4)), at(1, 'function bm:p242/pose/hivelink/' + pp('hivelink', 'stagger', 'roar')),
              at(1, title(AUD, 'actionbar', T('It turns to the great window - and reaches for the star.', STAR, italic=True)))] +
             [at(t, f'execute facing {WX:.1f} ~ {WZ:.1f} run tp @s ~ ~ ~ ~ 0') for t in range(20, 60, 4)] +
             [at(40, 'function bm:p242/pose/hivelink/' + pp('hivelink', 'gravity', 'roar')), at(40, snd('block.end_portal.spawn', 3, 0.5))] +
             [at('60..200', 'function bm:p242/c/pour'), at('60..200', 'function bm:p242/c/flood')] +
             beat(60, 200, 10) + [at(60 + 20 * k, f'function bm:p242/c/spark{k}') for k in range(6)] +
             [at(t, snd('block.fire.ambient', 3, 0.5)) for t in range(60, 200, 12)] +
             [at(190, f'particle minecraft:flash{{color:[1.0,0.6,0.2,1.0]}} ~ ~6 ~ 0 0 0 0 1 force {AUD}'), at(190, snd('item.trident.thunder', 3, 0.5)),
              at(190, snd('entity.blaze.death', 3, 0.4)), at(190, f'particle minecraft:explosion_emitter ~ ~6 ~ 1 2 1 0 3 force {AUD}'),
              at(190, 'scoreboard players set @s bm.vxph 3'), at(190, f'attribute @s minecraft:scale base set {HOST["starfire"]}'),
              at(190, 'function bm:p242/pose/starfire/' + pp('starfire', 'stagger', 'roar')), at(190, 'function bm:p242/c/shake'),
              at(200, f'execute facing entity {FIGHT[:-1]},sort=nearest,limit=1] feet run tp @s ~ ~ ~ ~ 0'),
              at(230, 'function bm:p242/pose/starfire/' + pp('starfire', 'roar')), at(230, snd('entity.ender_dragon.growl', 3, 0.5)), at(230, snd('entity.blaze.ambient', 3, 0.4)),
              at(230, f'particle minecraft:flame ~ ~6 ~ 4 4 4 0.2 300 force {AUD}'), at(230, 'function bm:p242/a/push')] +
             [at(t, 'function bm:p242/c/shake') for t in range(230, 250, 4)] +
             [at(232, f'title {AUD} times 4 50 16'), at(232, title(AUD, 'title', T(L.FIGHT['p3'], STAR, bold=True))),
              at(232, title(AUD, 'subtitle', T('it drinks the star', '#ffc08a', italic=True))),
              at(262, title(AUD, 'actionbar', T('The bridge is a furnace now. Shelter from the flares behind the pylons and the wreck!', STAR, bold=True))),
              at('1..290', 'function bm:p242/c/look'), at(ENT[2] - 1, 'function bm:p242/turned')])
    fn('p242/turn_tick', ['scoreboard players add @s bm.vxt 1', 'execute if entity @s[tag=bm.vxt1] run return run function bm:p242/turn1', 'execute if entity @s[tag=bm.vxt2] run function bm:p242/turn2'])
    fn('p242/turn1', turn1); fn('p242/turn2', turn2)
    fn('p242/turned', ['tag @s remove bm.vxturn', 'tag @s remove bm.vxt1', 'tag @s remove bm.vxt2', 'kill @e[type=minecraft:marker,tag=bm.vxlook]', 'tag @s add bm.vxlive',
                       'data modify entity @s Invulnerable set value 0b', 'scoreboard players set @s bm.vxa 0',
                       'scoreboard players set @s bm.vxx 10', 'function bm:p242/fill', 'bossbar set bm:vexis color green', 'function bm:p242/pyl/clear',
                       f'execute if score @s bm.vxph matches 2 run bossbar set bm:vexis name {snbt([T(L.VX, COL, bold=True), T("  -  " + L.FIGHT["p2"], "#9adf8a")])}',
                       f'execute if score @s bm.vxph matches 3 run bossbar set bm:vexis name {snbt([T(L.VX, COL, bold=True), T("  -  " + L.FIGHT["p3"], "#ffc08a")])}',
                       'execute if score @s bm.vxph matches 3 run bossbar set bm:vexis color yellow',
                       f'execute as {AUD} at @s run function bm:p152/tick'])
    fn('p242/a/push', [f'execute as {FIGHT[:-1]},distance=..20] at @s facing entity {ME} feet rotated ~ 0 if block ^ ^ ^-1.5 #bm:grap_pass if block ^ ^1 ^-1.5 #bm:grap_pass run tp @s ^ ^ ^-1.5',
                       f'execute as {FIGHT[:-1]},distance=..20] run damage @s 4 minecraft:mob_attack by {ME}'])

    # ================================================================== THE ATTACKS
    S_, MM = '@s', ME
    fn('p242/a/footfall', ['playsound minecraft:entity.iron_golem.step hostile @a[distance=..40] ~ ~ ~ 2 0.4', 'playsound minecraft:block.anvil.land hostile @a[distance=..40] ~ ~ ~ 0.4 0.4',
                           'particle minecraft:electric_spark ~ ~0.2 ~ 1.5 0.1 1.5 0.1 10 force'])
    # -- cover: a ray from (here) to the player - anything solid on the way and they're safe (the pylons, the wreck's hull... the
    #    wreck is displays, so its marker counts as a 3-block-wide pillar)
    fn('p242/cov/start', ['scoreboard players set #cr bm.rng 64', 'function bm:p242/cov/ray'])
    fn('p242/cov/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run scoreboard players set #cov bm.rng 1',
                        'execute if entity @e[type=minecraft:marker,tag=bm.vxwreck,distance=..2.6] run return run scoreboard players set #cov bm.rng 1',
                        'execute if entity @s[distance=..1.2] run return 0', 'scoreboard players remove #cr bm.rng 1',
                        'execute if score #cr bm.rng matches 1.. positioned ^ ^ ^0.8 run function bm:p242/cov/ray'])
    # -- I: PLASMA SWEEP (the cannon arm, a sweeping beam; 90 degrees across)
    fn('p242/a/cannon_start', ['kill @e[type=minecraft:marker,tag=bm.vxcan]', f'execute positioned ^-3 ^7 ^1 facing entity {TGT} feet rotated ~-45 ~ run summon minecraft:marker ~ ~ ~ {{Tags:["bm.vxfx","bm.vxcan"]}}',
                               'playsound minecraft:block.beacon.activate hostile @a[distance=..64] ~ ~ ~ 3 1.6', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..64] ~ ~ ~ 3 0.6',
                               title(AUD, 'actionbar', T('PLASMA SWEEP - put a pylon between you and the cannon!', RED, bold=True))])
    fn('p242/a/cannon', ['execute as @e[type=minecraft:marker,tag=bm.vxcan] at @s run function bm:p242/can/step', 'execute if score @s bm.vxx matches 6 run kill @e[type=minecraft:marker,tag=bm.vxcan]'])
    fn('p242/can/step', ['tp @s ~ ~ ~ ~3.75 ~', 'scoreboard players set #br bm.rng 50', 'execute rotated as @s run function bm:p242/can/ray'])
    fn('p242/can/ray', ['particle minecraft:dust{color:[0.48,1.0,0.42],scale:2.4} ~ ~ ~ 0.05 0.05 0.05 0 1 force', 'particle minecraft:electric_spark ~ ~ ~ 0 0 0 0 1 force',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0 2 force',
                        'execute if entity @e[type=minecraft:marker,tag=bm.vxwreck,distance=..2.6] run return 0',
                        'execute as @a[distance=..1.7,gamemode=!spectator,gamemode=!creative,tag=!bm.vxhit] at @s run function bm:p242/can/hit',
                        'scoreboard players remove #br bm.rng 1', 'execute if score #br bm.rng matches 1.. positioned ^ ^ ^0.8 run function bm:p242/can/ray'])
    fn('p242/can/hit', [f'damage @s 11 minecraft:magic by {MM}', 'data modify entity @s Fire set value 40s', 'tag @s add bm.vxhit'])
    tick.append('tag @a[tag=bm.vxhit] remove bm.vxhit')
    # -- I: MISSILES (a marked circle under each fighter; 1.5 s, then the strike)
    fn('p242/a/missile_mark', [f'execute as {FIGHT} at @s run summon minecraft:marker ~ ~0.1 ~ {{Tags:["bm.vxfx","bm.vxmis"]}}', 'playsound minecraft:entity.firework_rocket.launch hostile @a[distance=..64] ~ ~ ~ 3 0.5',
                               'execute positioned ~ ~12 ~ run particle minecraft:firework ~ ~ ~ 2 1 2 0.1 30 force', title(AUD, 'actionbar', T('MISSILES - get out of the red circles!', RED, bold=True))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxmis] at @s run function bm:p242/mis/tick')
    fn('p242/mis/tick', ['scoreboard players add @s bm.vxt 1'] +
       [f'particle minecraft:dust{{color:[1.0,0.15,0.1],scale:1.4}} ~{x} ~ ~{z} 0 0 0 0 1 force' for x, z in ring_pts(3, 14)] +
       ['execute if score @s bm.vxt matches 20 run playsound minecraft:entity.firework_rocket.blast_far hostile @a[distance=..32] ~ ~ ~ 1 0.6',
        'execute if score @s bm.vxt matches 22..29 run particle minecraft:firework ~ ~6 ~ 0.2 2 0.2 0 4 force',
        'execute if score @s bm.vxt matches 30.. run function bm:p242/mis/hit'])
    fn('p242/mis/hit', ['particle minecraft:explosion_emitter ~ ~0.5 ~ 0 0 0 0 1 force', 'particle minecraft:flame ~ ~0.5 ~ 1.5 0.4 1.5 0.1 40 force',
                        'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 0.8',
                        f'execute as @a[distance=..3.2,gamemode=!spectator,gamemode=!creative] run damage @s 12 minecraft:explosion by {MM}', 'kill @s'])
    # -- I: STOMP (a shockwave rolls out - jump it)
    fn('p242/a/stomp', ['summon minecraft:marker ~ ~0.2 ~ {Tags:["bm.vxfx","bm.vxring"]}', 'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                        'playsound minecraft:entity.iron_golem.damage hostile @a[distance=..48] ~ ~ ~ 2 0.3', 'particle minecraft:explosion_emitter ^ ^ ^4 0 0 0 0 1 force',
                        'function bm:p242/c/shake'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxring] at @s run function bm:p242/ring/tick')
    fn('p242/ring/tick', ['scoreboard players add @s bm.vxt 1'] + [f'execute if score @s bm.vxt matches {k} run function bm:p242/ring/r{k}' for k in range(1, 41)] +
       ['execute if score @s bm.vxt matches 41.. run kill @s'])
    for k in range(1, 41):
        r_ = k * 0.6
        fn(f'p242/ring/r{k}', [f'particle minecraft:dust{{color:[0.48,1.0,0.42],scale:2.4}} ~{x} ~ ~{z} 0.1 0.05 0.1 0 1 force' for x, z in ring_pts(r_, max(8, int(4 * r_)))] +
           [f'execute as @a[distance={max(0, r_ - 0.8):.2f}..{r_ + 0.8:.2f},gamemode=!spectator,gamemode=!creative] if predicate bm:p238/ground at @s run function bm:p242/a/ring_hit'])
    fn('p242/a/ring_hit', [f'damage @s 10 minecraft:mob_attack by {MM}', 'effect give @s minecraft:slowness 2 2', 'tp @s ~ ~0.4 ~'])
    # -- I: DROP-PODS (from the dome: a streak of light, then troopers)
    fn('p242/a/pods', ['execute store result score #kn bm.rng if entity @e[tag=bm.vxk]', 'execute if score #kn bm.rng matches 6.. run return 0',
                       'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..64] ~ ~ ~ 2 0.5', title(AUD, 'actionbar', T('DROP-PODS incoming!', RED, bold=True)),
                       f'execute as {FIGHT[:-1]},sort=random,limit=3] at @s run summon minecraft:marker ^ ^ ^4 {{Tags:["bm.vxfx","bm.vxpod"]}}'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxpod] at @s run function bm:p242/pod/tick')
    fn('p242/pod/tick', ['scoreboard players add @s bm.vxt 1', 'execute if score @s bm.vxt matches ..39 run particle minecraft:end_rod ~ ~20 ~ 0.1 6 0.1 0 6 force',
                         'execute if score @s bm.vxt matches ..39 run particle minecraft:dust{color:[1.0,0.2,0.1],scale:1.5} ~ ~0.1 ~ 1 0 1 0 4 force',
                         'execute if score @s bm.vxt matches 40.. run function bm:p242/pod/land'])
    fn('p242/pod/land', ['particle minecraft:explosion_emitter ~ ~0.5 ~ 0 0 0 0 1 force', 'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 1',
                         f'execute as @a[distance=..2.5,gamemode=!spectator,gamemode=!creative] run damage @s 8 minecraft:explosion by {MM}',
                         'function bm:p32/spawn/trooper', 'tag @e[tag=bm.vtroop,tag=!bm.vxk,distance=..2] add bm.vxk', 'tag @e[tag=bm.vtroop,distance=..2] add bm.vstay', 'kill @s'])
    # -- II/III: HIVE DRONES
    drone = lambda: snbt({'Tags': ['bm.seen', 'bm.vxk', 'bm.vorn', 'bm.vstay'], 'PersistenceRequired': B(1), 'life_ticks': Int(600), 'CustomName': T('Hive Drone', COL),
                          'attributes': [{'id': 'minecraft:max_health', 'base': Dd(18)}], 'Health': F(18), 'DeathLootTable': 'minecraft:empty'})
    fn('p242/a/drones', ['execute store result score #kn bm.rng if entity @e[type=minecraft:vex,tag=bm.vxk]', 'execute if score #kn bm.rng matches 8.. run return 0',
                         'playsound minecraft:entity.vex.charge hostile @a[distance=..64] ~ ~ ~ 2 0.6', title(AUD, 'actionbar', T('Hive drones!', COL, bold=True)),
                         *[f'summon minecraft:vex ^{x} ^{4} ^1 {drone()}' for x in (-2, 0, 2)], 'particle minecraft:reverse_portal ~ ~4 ~ 2 1 2 0.1 60 force'])
    # -- II/III: GRAVITY WELL (a singularity at the target: everyone near is dragged in - then it implodes)
    fn('p242/a/well', [f'execute at {TGT} run summon minecraft:marker ~ ~0.5 ~ {{Tags:["bm.vxfx","bm.vxwell"]}}', 'playsound minecraft:block.end_portal.spawn hostile @a[distance=..64] ~ ~ ~ 2 1.6',
                       title(AUD, 'actionbar', T('A GRAVITY WELL - pull away from it!', '#c08aff', bold=True))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxwell] at @s run function bm:p242/well/tick')
    fn('p242/well/tick', ['scoreboard players add @s bm.vxt 1', 'particle minecraft:reverse_portal ~ ~ ~ 3 1 3 0.3 20 force', 'particle minecraft:portal ~ ~ ~ 0.3 0.3 0.3 1.5 10 force',
                          'particle minecraft:dust{color:[0.6,0.3,1.0],scale:2.0} ~ ~ ~ 0.3 0.3 0.3 0 4 force',
                          'execute if score @s bm.vxt matches ..69 as @a[distance=1.5..10,gamemode=!spectator,gamemode=!creative] at @s facing entity @e[type=minecraft:marker,tag=bm.vxwell,sort=nearest,limit=1] feet rotated ~ 0 if block ^ ^ ^0.2 #bm:grap_pass if block ^ ^1 ^0.2 #bm:grap_pass run tp @s ^ ^ ^0.2',
                          'execute if score @s bm.vxt matches 70.. run function bm:p242/well/burst'])
    fn('p242/well/burst', ['particle minecraft:explosion_emitter ~ ~ ~ 0 0 0 0 1 force', 'particle minecraft:reverse_portal ~ ~ ~ 1 1 1 1 200 force',
                           'playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 2 1.2',
                           f'execute as @a[distance=..3.5,gamemode=!spectator,gamemode=!creative] run damage @s 13 minecraft:magic by {MM}', 'kill @s'])
    # -- II/III: THE IMPROVEMENT BEAM (from its eyes; while it sees you, you are "improved" - break its line of sight)
    fn('p242/a/ibeam_start', [f'execute as {FIGHT} run tag @s add bm.vximp', 'playsound minecraft:entity.elder_guardian.curse hostile @a[distance=..64] ~ ~ ~ 2 1.2',
                              say(L.VOICE['dock'].replace('A SPECIMEN HAS BOARDED. HOW WONDERFUL. ', '')), title(AUD, 'actionbar', T('THE IMPROVEMENT BEAM - break its line of sight!', COL, bold=True))])
    fn('p242/a/ibeam', ['scoreboard players operation #ib bm.rng = @s bm.vxx', 'scoreboard players set #c5 bm.rng 5', 'scoreboard players operation #ib bm.rng %= #c5 bm.rng',
                        'execute if score #ib bm.rng matches 0 as @a[tag=bm.vximp] run function bm:p242/ib/one', 'execute if score @s bm.vxx matches 10 run tag @a remove bm.vximp'])
    fn('p242/ib/one', ['scoreboard players set #cov bm.rng 0', f'execute at {MM} positioned ~ ~6 ~ facing entity @s eyes run function bm:p242/cov/start',
                       'execute if score #cov bm.rng matches 1 run return 0',
                       f'execute at {MM} positioned ~ ~6 ~ facing entity @s eyes run function bm:p242/ib/line',
                       f'damage @s 3 minecraft:magic by {MM}', 'effect give @s minecraft:slowness 2 2', 'effect give @s minecraft:weakness 3 1', 'effect give @s minecraft:nausea 3 0 true',
                       title('@s', 'actionbar', T('YOU ARE BEING IMPROVED. Get behind something!', COL, bold=True))])
    fn('p242/ib/line', [f'particle minecraft:dust{{color:[0.7,1.0,0.25],scale:1.3}} ^ ^ ^{k} 0.03 0.03 0.03 0 1 force' for k in range(2, 40, 2)])
    # -- II: CLONES (four of it, all of them firing; strike the real one)
    cl_host = {'Tags': ['bm.vxcl', 'bm.vxfx2', 'bm.seen'], 'NoAI': B(1), 'Silent': B(1), 'NoGravity': B(1), 'PersistenceRequired': B(1), 'DeathLootTable': 'minecraft:empty',
               'CustomName': T(L.VX, COL),
               'attributes': [{'id': 'minecraft:max_health', 'base': Dd(1)}, {'id': 'minecraft:scale', 'base': Dd(HOST['hivelink'])}], 'Health': F(1),
               'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    spots = ring_pts(13, 4)
    for i in range(CLONES + 1):
        fn(f'p242/cl/spot{i}', [f'execute positioned {CX + 0.5 + spots[i][0]:.2f} {CY + 1 + HOVER["hivelink"]} {CZ + 0.5 + spots[i][1]:.2f} run tp @s ~ ~ ~'])
    for i in range(1, CLONES + 1):
        crig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.vxc", f"bm.vxc{i}", f"bm.vxc{i}_{p}"], SCALE["hivelink"], model=A.model_name(p, A.BOSS_POSES["hivelink"][pp("hivelink", "clone", "idle_a")]), extra=dict(view_range=F(5.0), brightness={"block": Int(12), "sky": Int(12)}))}'
                for p in A.PARTS]
        fn(f'p242/cl/make{i}', [f'summon minecraft:husk ~ ~ ~ {snbt(dict(cl_host, Tags=cl_host["Tags"] + [f"bm.vxcl{i}"]))}'] + crig +
           ['execute rotated ~ 0 run function bm:p242/cl/place' + str(i)])
        fn(f'p242/cl/place{i}', RF.place(A, SCALE['hivelink'] / 16, csel(i)))
        fn(f'p242/cl/tick{i}', [f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0', f'execute rotated as @s rotated ~ 0 run function bm:p242/cl/place{i}'])
    fn('p242/a/clone', ['function bm:p242/a/clone_end', 'playsound minecraft:entity.illusioner.mirror_move hostile @a[distance=..64] ~ ~ ~ 3 0.6',
                        f'particle minecraft:flash{{color:[0.5,1.0,0.45,1.0]}} ~ ~5 ~ 0 0 0 0 1 force {AUD}', say(L.FIGHT['clone']),
                        'execute store result score #sp bm.rng run random value 0..3'] +
       [f'execute if score #sp bm.rng matches {s} run function bm:p242/cl/spot{s}' for s in range(4)] +
       [f'execute if score #sp bm.rng matches {s} positioned {CX + 0.5 + spots[j][0]:.2f} {CY + 1 + HOVER["hivelink"]} {CZ + 0.5 + spots[j][1]:.2f} run function bm:p242/cl/make{n}'
        for s in range(4) for n, j in enumerate([j for j in range(4) if j != s], start=1)] +
       ['function bm:p242/pose/hivelink/' + pp('hivelink', 'clone', 'idle_a'), 'tag @s add bm.vxcloned'])
    tick.append(f'execute if entity {ME}[tag=bm.vxcloned] run function bm:p242/cl/tick')
    fn('p242/cl/tick', [f'execute as @e[type=minecraft:husk,tag=bm.vxcl{i}] at @s run function bm:p242/cl/tick{i}' for i in range(1, CLONES + 1)] +
       [f'execute unless entity @e[type=minecraft:husk,tag=bm.vxcl{i}] run kill @e[type=minecraft:item_display,tag=bm.vxc{i}]' for i in range(1, CLONES + 1)] +
       # (the real one is struck: the illusion breaks)
       [f'execute as {ME} if entity @s[nbt={{HurtTime:10s}}] run function bm:p242/cl/broken'])
    fn('p242/cl/broken', ['function bm:p242/a/clone_end', 'scoreboard players set @s bm.vxx 1', 'playsound minecraft:block.glass.break hostile @a[distance=..64] ~ ~ ~ 2 0.6',
                          title(AUD, 'actionbar', T('You struck the real one - the clones shatter!', '#9adf8a', bold=True))])
    fn('p242/a/clone_end', ['tag @e[tag=bm.vxcloned] remove bm.vxcloned', 'execute as @e[type=minecraft:husk,tag=bm.vxcl] at @s run particle minecraft:poof ~ ~4 ~ 1 3 1 0.05 40 force',
                            'kill @e[type=minecraft:item_display,tag=bm.vxc]', 'execute as @e[type=minecraft:husk,tag=bm.vxcl] run tp @s ~ -400 ~', 'kill @e[type=minecraft:husk,tag=bm.vxcl]'])
    G.wjson('bm/advancement/p242/clone.json', {'criteria': {'kill': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'nbt': '{Tags:["bm.vxcl"]}'}}]}}}, 'rewards': {'function': 'bm:p242/cl/wrong'}})
    fn('p242/cl/wrong', ['advancement revoke @s only bm:p242/clone', f'damage @s 7 minecraft:magic by {ME}', 'effect give @s minecraft:slowness 2 1',
                         'particle minecraft:electric_spark ~ ~1 ~ 0.6 1 0.6 0.4 40', 'playsound minecraft:entity.illusioner.cast_spell player @s ~ ~ ~ 1 0.6',
                         title('@s', 'actionbar', T('A clone - it bursts in your face!', RED, bold=True))])
    fn('p242/a/cbeam', ['execute as @a[tag=bm.vxtgt] run tag @s add bm.vximp', 'function bm:p242/a/ibeam_one_all', 'tag @a remove bm.vximp'])
    fn('p242/a/ibeam_one_all', ['execute as @a[tag=bm.vximp] run function bm:p242/ib/one'] +
       [f'execute as @e[type=minecraft:husk,tag=bm.vxcl{i}] at @s positioned ~ ~6 ~ facing entity {TGT} eyes run function bm:p242/ib/line' for i in range(1, CLONES + 1)] +
       [f'execute as @e[type=minecraft:husk,tag=bm.vxcl{i}] at @s positioned ~ ~6 ~ facing entity {TGT} eyes positioned ^ ^ ^2 run function bm:p242/cl/beam' for i in range(1, CLONES + 1)])
    fn('p242/cl/beam', [f'execute as {TGT} at @s run damage @s 2 minecraft:magic by {ME}'])
    # -- III: STAR-FLARES (a wall of fire from the window; cover from the star is all that saves you)
    fn('p242/a/flare_warn', ['playsound minecraft:block.fire.extinguish hostile @a[distance=..64] ~ ~ ~ 3 0.4', 'playsound minecraft:entity.blaze.ambient hostile @a[distance=..64] ~ ~ ~ 3 0.4',
                             'function bm:p242/c/flood', title(AUD, 'title', T(' ', STAR)),
                             title(AUD, 'subtitle', T('A STAR-FLARE - get a pylon or the wreck between you and the window!', STAR, bold=True))])
    fn('p242/a/flare', ['playsound minecraft:entity.blaze.shoot hostile @a[distance=..64] ~ ~ ~ 3 0.4', 'playsound minecraft:item.firecharge.use hostile @a[distance=..64] ~ ~ ~ 3 0.5',
                        f'particle minecraft:flame {CX + 0.5} {CY + 3} {CZ + 0.5} 22 2 22 0.2 600 force {AUD}', f'particle minecraft:lava {CX + 0.5} {CY + 2} {CZ + 0.5} 20 1 20 0 40 force {AUD}',
                        f'execute as {FIGHT} at @s run function bm:p242/flare/one'])
    fn('p242/flare/one', ['scoreboard players set #cov bm.rng 0', f'execute positioned {WX:.2f} ~1.2 {WZ:.2f} facing entity @s eyes run function bm:p242/cov/start',
                          f'execute if score #cov bm.rng matches 0 run damage @s 14 minecraft:in_fire by {ME}', 'execute if score #cov bm.rng matches 0 run data modify entity @s Fire set value 80s',
                          'execute if score #cov bm.rng matches 1 run ' + title('@s', 'actionbar', T('The flare breaks around your cover.', '#ffc08a'))])
    # -- III: THE SOLAR LANCE (it aims - a thin red line - then a straight burning beam)
    fn('p242/a/lance_aim', ['kill @e[type=minecraft:marker,tag=bm.vxlnc]', f'execute positioned ~ ~6 ~ facing entity {TGT} eyes run summon minecraft:marker ~ ~ ~ {{Tags:["bm.vxfx","bm.vxlnc"]}}',
                            'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..64] ~ ~ ~ 3 0.8', title(AUD, 'actionbar', T('THE SOLAR LANCE - move off its line!', STAR, bold=True))])
    fn('p242/a/lance_track', [f'execute as @e[type=minecraft:marker,tag=bm.vxlnc] at @s facing entity {TGT} eyes run tp @s ~ ~ ~ ~ ~',
                              'execute as @e[type=minecraft:marker,tag=bm.vxlnc] at @s run function bm:p242/lnc/aimline'])
    fn('p242/lnc/aimline', [f'particle minecraft:dust{{color:[1.0,0.2,0.1],scale:0.6}} ^ ^ ^{k} 0 0 0 0 1 force' for k in range(2, 50, 2)])
    fn('p242/a/lance_fire', ['playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..64] ~ ~ ~ 3 0.6', 'playsound minecraft:item.trident.thunder hostile @a[distance=..64] ~ ~ ~ 2 1.2',
                             'execute as @e[type=minecraft:marker,tag=bm.vxlnc] at @s run function bm:p242/lnc/fire', 'kill @e[type=minecraft:marker,tag=bm.vxlnc]'])
    fn('p242/lnc/fire', ['scoreboard players set #br bm.rng 70', 'execute rotated as @s run function bm:p242/lnc/ray'])
    fn('p242/lnc/ray', ['particle minecraft:flame ~ ~ ~ 0.15 0.15 0.15 0.02 3 force', 'particle minecraft:dust{color:[1.0,0.75,0.3],scale:2.6} ~ ~ ~ 0.1 0.1 0.1 0 2 force',
                        'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0 4 force',
                        'execute as @a[distance=..1.8,gamemode=!spectator,gamemode=!creative,tag=!bm.vxhit] at @s run function bm:p242/lnc/hit',
                        'scoreboard players remove #br bm.rng 1', 'execute if score #br bm.rng matches 1.. positioned ^ ^ ^0.7 run function bm:p242/lnc/ray'])
    fn('p242/lnc/hit', [f'damage @s 18 minecraft:in_fire by {ME}', 'data modify entity @s Fire set value 100s', 'tag @s add bm.vxhit'])
    # -- III: GRAVITY FLIPS (circles where gravity turns over: up you go, then down)
    fn('p242/a/flip', [f'execute as {FIGHT[:-1]},sort=random,limit=3] at @s run summon minecraft:marker ~ ~0.1 ~ {{Tags:["bm.vxfx","bm.vxflip"]}}',
                       f'execute positioned {CX + 0.5} {CY + 1.1} {CZ + 0.5} run summon minecraft:marker ^ ^ ^ {{Tags:["bm.vxfx","bm.vxflip"]}}',
                       'playsound minecraft:block.end_portal_frame.fill hostile @a[distance=..64] ~ ~ ~ 3 0.5', title(AUD, 'actionbar', T('GRAVITY FLIPS - step out of the violet circles!', '#c08aff', bold=True))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxflip] at @s run function bm:p242/flip/tick')
    fn('p242/flip/tick', ['scoreboard players add @s bm.vxt 1'] +
       [f'particle minecraft:dust{{color:[0.7,0.4,1.0],scale:1.4}} ~{x} ~ ~{z} 0 0 0 0 1 force' for x, z in ring_pts(3.5, 16)] +
       ['execute if score @s bm.vxt matches 30 as @a[distance=..3.5,gamemode=!spectator,gamemode=!creative] run function bm:p242/flip/up',
        'execute if score @s bm.vxt matches 30 run particle minecraft:reverse_portal ~ ~1 ~ 2 1 2 0.5 100 force',
        'execute if score @s bm.vxt matches 31.. run kill @s'])
    fn('p242/flip/up', ['effect give @s minecraft:levitation 2 12', 'playsound minecraft:entity.shulker.shoot player @s ~ ~ ~ 1 0.6',
                        title('@s', 'actionbar', T('Gravity turns over!', '#c08aff', bold=True))])

    # ---- the frenzy (a quarter of its last pool) and its tiring
    fn('p242/frenzy_chk', ['execute unless score @s bm.vxph matches 3 run return 0', 'execute if entity @s[tag=bm.vxfrz] run return 0',
                           'scoreboard players operation #q bm.rng = @s bm.vxhp', 'scoreboard players set #4 bm.rng 4', 'scoreboard players operation #q bm.rng /= #4 bm.rng',
                           f'scoreboard players add #q bm.rng {FLOOR}', 'execute if score #hp bm.rng <= #q bm.rng run function bm:p242/frenzy'])
    fn('p242/frenzy', ['tag @s add bm.vxfrz', 'scoreboard players set @s bm.vxz 10', 'data modify entity @s Invulnerable set value 1b', say(L.FIGHT['frenzy']),
                       'scoreboard players set @s bm.vxa 18', 'scoreboard players set @s bm.vxx 200',
                       'playsound minecraft:entity.warden.roar hostile @a[distance=..64] ~ ~ ~ 3 0.7', 'bossbar set bm:vexis color red'])
    fn('p242/frenzy_sec', ['scoreboard players remove @s bm.vxz 1',
                           'execute if score @s bm.vxz matches 1..9 run function bm:p242/a/missile_mark', 'execute if score @s bm.vxz matches 7 run function bm:p242/a/flare_warn',
                           'execute if score @s bm.vxz matches 5 run function bm:p242/a/flare',
                           title(AUD, 'actionbar', [T('It can\'t be hurt - ', '#ffc08a', bold=True), T('keep moving!', 'gray')]),
                           'execute if score @s bm.vxz matches 0 run function bm:p242/tire'])
    fn('p242/tire', ['scoreboard players set @s bm.vxz -8', 'data modify entity @s Invulnerable set value 0b', 'effect clear @s minecraft:resistance',
                     'scoreboard players set @s bm.vxa 22', 'scoreboard players set @s bm.vxx 160', 'bossbar set bm:vexis color yellow',
                     'tp @s ~ ~-3 ~', 'playsound minecraft:entity.ravager.stunned hostile @a[distance=..64] ~ ~ ~ 2 0.8',
                     title(AUD, 'actionbar', [T('Its fire gutters - ', 'gold', bold=True), T('strike it now!', 'gray')])])
    second.append(f'execute as {ME} if score @s bm.vxz matches -99..-1 run scoreboard players add @s bm.vxz 1')

    # ================================================================== THE FALL - THE UNLINKING (30 s, eyes held on it)
    fn('p242/fall', ['tag @s remove bm.vxlive', 'tag @s add bm.vxfall', 'data modify entity @s Invulnerable set value 1b', 'scoreboard players set @s bm.vxa 31',
                     f'scoreboard players set @s bm.vxx {UNLINK + 20}', 'scoreboard players set @s bm.vxt 0', 'function bm:p242/clear', 'bossbar set bm:vexis value 0',
                     'kill @e[type=minecraft:marker,tag=bm.vxlook]', 'execute at @s run summon minecraft:marker ~ ~6 ~ {Tags:["bm.vxlook"]}',
                     f'execute as {AUD} at @s run function bm:p152/tick'])
    hive = lambda txt: tellraw(AUD, [T('THE HIVE: ', VCOL, bold=True), T(txt, VCOL, italic=True)])
    vx = lambda txt: tellraw(AUD, [T('Vexis: ', '#c8f0c0', bold=True), T(txt, '#e8ffe0', italic=True)])
    for k in range(8):
        fn(f'p242/c/implant{k}', [f'particle minecraft:electric_spark ~{rs2.uniform(-1.5, 1.5):.1f} ~{rs2.uniform(5, 8):.1f} ~{rs2.uniform(-1.5, 1.5):.1f} 0.3 0.3 0.3 0.6 40 force {AUD}',
                                  f'particle minecraft:flash{{color:[0.7,1.0,0.3,1.0]}} ~{rs2.uniform(-1, 1):.1f} ~{rs2.uniform(6, 8):.1f} ~{rs2.uniform(-1, 1):.1f} 0 0 0 0 1 force {AUD}',
                                  snd('block.redstone_torch.burnout', 2, 0.5 + 0.08 * k), snd('entity.elder_guardian.hurt', 1.5, 0.5 + 0.05 * k)])
    # (what it was: the Unlinked, kneeling - a little over a follower's size)
    unl = A.POSES.get('tired', A.POSES['sit_a'])
    SMALL = A.FOLLOWER_SCALE * 1.6
    fn('p242/c/small', ['tag @s add bm.vxsmall'] + RF.pose(A, unl, SMALL, 60, sel, swap=SWAP))
    fn('p242/place/small', RF.place(A, SMALL / 16, sel))
    seq = ([at(1, f'execute as {AUD} at @s run stopsound @s record'), at(1, 'function bm:p242/pose/starfire/' + pp('starfire', 'death_0', 'stagger')),
            at(1, snd('entity.elder_guardian.death', 3, 0.5)), at(1, snd('entity.blaze.death', 3, 0.4)), at(1, f'effect give {FIGHT} minecraft:darkness 3 0 true'),
            at(1, tellraw(AUD, [T(L.FIGHT['fall'], '#c8f0c0', italic=True)]))] +
           # (the hive screams through it, louder and broken - and the implants burn out, one after another)
           [at(t, hive(w)) for t, w in ((20, 'VEXIS.'), (44, 'VEXIS. RESPOND.'), (70, 'VEXIS VEXIS VEXIS VEX'))] +
           [at(30 + 18 * k, f'function bm:p242/c/implant{k}') for k in range(8)] +
           [at(t, snd('block.beacon.deactivate', 2, 0.8 - 0.05 * j)) for j, t in enumerate(range(30, 180, 30))] +
           [at(60, 'function bm:p242/pose/starfire/' + pp('starfire', 'death_1', 'stagger'))] +
           [at(t, 'tp @s ~ ~-0.06 ~') for t in range(60, 180, 2)] +
           [at(t, 'execute as @e[type=minecraft:marker,tag=bm.vxlook] at @s run tp @s ~ ~-0.06 ~') for t in range(60, 180, 2)] +
           [at(t, 'function bm:p242/c/shake') for t in range(60, 180, 20)] +
           # (SILENCE)
           [at(180, f'particle minecraft:flash{{color:[0.8,1.0,0.6,1.0]}} ~ ~5 ~ 0 0 0 0 1 force {AUD}'), at(180, snd('block.conduit.deactivate', 3, 0.5)),
            at(180, f'execute as {AUD} at @s run stopsound @s hostile'), at(182, f'title {AUD} times 20 80 30'), at(182, title(AUD, 'title', T(' ', COL))),
            at(182, title(AUD, 'subtitle', T(L.UNLINK['cut'], '#c8f0c0', italic=True))),
            at(220, 'function bm:p242/pose/starfire/' + pp('starfire', 'death_2', 'stagger')), at(220, snd('entity.iron_golem.step', 1, 0.6))] +
           # (it kneels; it is only one; it shrinks to what it was)
           [at(270, vx(L.UNLINK['one'])), at(340, 'function bm:p242/c/small'), at(340, snd('block.amethyst_block.resonate', 2, 0.6)),
            at('340..400', 'particle minecraft:end_rod ~ ~2 ~ 1 1.5 1 0.02 4 force'), at(350, 'tp @s ~ ~-1 ~'),
            at(350, 'execute as @e[type=minecraft:marker,tag=bm.vxlook] at @s run tp @s ~ ~-3.5 ~'),
            at(410, vx(L.UNLINK['name'])), at(480, vx(L.UNLINK['you'])), at(480, snd('block.note_block.chime', 1, 0.8)),
            at(540, f'title {AUD} times 10 60 20'), at(540, title(AUD, 'title', T('THE HIVE-LINK IS CUT', COL, bold=True))),
            at(540, title(AUD, 'subtitle', T('the invasion nights are over', '#c8f0c0', italic=True))),
            at(f'1..{UNLINK - 2}', 'function bm:p242/c/look'), at(UNLINK, 'function bm:p242/won')])
    fn('p242/falling', ['scoreboard players add @s bm.vxt 1'] + seq)
    G.wjson('bm/advancement/story/vexis.json', {'parent': 'bm:story/root', 'criteria': {'won': {'trigger': 'minecraft:impossible'}},
                                                'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': 'bm:vexis_link'}},
                                                            'title': T('Unlinked', COL), 'description': T('Fell Admiral Vexis at the helm of the Vorn Armada', 'gray'),
                                                            'frame': 'challenge'}})
    lt, uni = G.loot_entry, G.uni
    G.wjson('bm/loot_table/p242/spoils.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [lt('xenite_red', uni(16, 28))]}, {'rolls': 1, 'entries': [lt('star_core', uni(3, 5))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:netherite_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 3)}]}]},
        {'rolls': 1, 'entries': [lt(i) for i in ('starfire_lance', 'hive_breaker', 'singularity_launcher', 'admiral_crown')]},
        {'rolls': 1, 'entries': [lt('power_cell', uni(2, 4))]}]})
    fn('p242/won', [tellraw('@a', [T('☄ ', COL), {'selector': FIGHT}, T(' cut the hive-link of ', 'gray'), T(L.VX, COL, bold=True), T(' at the helm of the Vorn Armada.', 'gray')]),
                    f'execute as {FIGHT} at @s run function bm:p242/reward',
                    'kill @e[type=minecraft:marker,tag=bm.vxlook]', 'function bm:p242/c/door_open', 'function bm:p241/nights_end', 'function bm:p241/collapse',
                    'bossbar set bm:vexis visible false', 'kill @e[type=minecraft:item_display,tag=bm.vxr]', 'kill @e[type=minecraft:item_display,tag=bm.vxw]',
                    'kill @e[type=minecraft:marker,tag=bm.vxwreck]', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p242/reward', ['tag @s add bm.vxdone', 'advancement grant @s only bm:story/vexis', 'scoreboard players add @s bm.vxwin 1',
                       give('akey_victor'), 'loot give @s loot bm:p242/spoils',
                       tellraw('@s', P + [T(L.VX, COL, bold=True), T(' has fallen. ', 'gray'), T(L.FIGHT['fall2'], '#c8f0c0', italic=True)]),
                       'execute unless entity @s[tag=bm.vxfirst] run function bm:p242/first',
                       'execute if score @s bm.vxwin matches 2.. unless entity @s[tag=bm.xbwar] run function bm:p242/warframe'])
    fn('p242/first', ['tag @s add bm.vxfirst', give('music_disc_vexis'), 'function bm:p243/enc/joined',
                      tellraw('@s', [T('  In the quiet: ', 'gray'), T('its record', COL), T(' - and ', 'gray'), T(L.ITEMS['link'][0], COL, bold=True),
                                     T('. Something on the other end is listening for you.', 'gray', italic=True)])])
    # (felled a second time: Vexis remembers its warframe - the full-size form, as it stood against you)
    fn('p242/warframe', ['tag @s add bm.xbwar', 'advancement grant @s only bm:story/vexis_warframe',
                         tellraw('@s', [T('  ', 'gray'), T('Vexis', COL, bold=True), T(' remembers its warframe: ', 'gray'), T('the full-size form', COL, bold=True),
                                        T(' - as vast as it stood against you. (Its menu: Warframe / Unlinked.)', 'gray')])])
    G.wjson('bm/advancement/story/vexis_warframe.json', {'parent': 'bm:story/vexis', 'criteria': {'won': {'trigger': 'minecraft:impossible'}},
                                                        'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': 'bm:vexis_link'}},
                                                                    'title': T('Warframe', 'dark_green'), 'description': T('Fell Admiral Vexis a second time, its hive remembering your world', 'gray'),
                                                                    'frame': 'challenge'}})

    # ================================================================== ITS SPOILS AT WORK (p2/armadaitems)
    G.wjson('bm/advancement/p242/hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity'}}, 'rewards': {'function': 'bm:p242/hit'}})
    vic = '@e[type=!minecraft:player,distance=..9,nbt={HurtTime:10s},sort=nearest,limit=1]'
    fn('p242/hit', ['advancement revoke @s only bm:p242/hit', 'execute if entity @s[tag=bm.vxme] run return 0', 'tag @s add bm.vxme',
                    'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"starfire_lance"}] run function bm:p242/lance',
                    f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"hive_breaker"}}] as {vic} if entity @s[tag=bm.vorn] run damage @s 8 minecraft:magic by @p',
                    f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"hive_breaker"}}] as {vic} if entity @s[tag=bm.vorn] at @s run particle minecraft:electric_spark ~ ~1 ~ 0.4 0.6 0.4 0.3 20',
                    'tag @s remove bm.vxme'])
    fn('p242/lance', ['execute if score @s bm.vxsc matches 1.. run return 0', 'scoreboard players set @s bm.vxsc 15',
                      'scoreboard players set #br bm.rng 24', 'execute anchored eyes positioned ^ ^ ^1 run function bm:p242/lance_ray',
                      'playsound minecraft:item.firecharge.use player @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    fn('p242/lance_ray', ['particle minecraft:flame ~ ~ ~ 0.05 0.05 0.05 0.01 1', 'particle minecraft:dust{color:[1.0,0.7,0.3],scale:1.0} ~ ~ ~ 0 0 0 0 1',
                          'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                          'execute as @e[type=#bm:hostile,distance=..1.4,limit=1] run return run function bm:p242/lance_hit',
                          'scoreboard players remove #br bm.rng 1', 'execute if score #br bm.rng matches 1.. positioned ^ ^ ^0.6 run function bm:p242/lance_ray'])
    fn('p242/lance_hit', ['damage @s 10 minecraft:in_fire by @p', 'data modify entity @s Fire set value 80s', 'particle minecraft:lava ~ ~1 ~ 0.3 0.3 0.3 0 6'])
    tick.append('scoreboard players remove @a[scores={bm.vxsc=1..}] bm.vxsc 1')
    # the Singularity Launcher: its bolt becomes a small, hungry star
    fast.append('execute as @e[type=minecraft:arrow,tag=!bm.vxsg0] at @s run function bm:p242/sing/tag')
    fn('p242/sing/tag', ['tag @s add bm.vxsg0', 'execute on origin if items entity @s weapon.* *[minecraft:custom_data~{bm:"singularity_launcher"}] run tag @e[type=minecraft:arrow,tag=bm.vxsg0,tag=!bm.vxsg,distance=..4,sort=nearest,limit=1] add bm.vxsg'])
    fast.append('execute as @e[type=minecraft:arrow,tag=bm.vxsg] at @s run function bm:p242/sing/fly')
    fn('p242/sing/fly', ['particle minecraft:reverse_portal ~ ~ ~ 0.1 0.1 0.1 0.05 4', 'execute if entity @s[nbt={inGround:1b}] run function bm:p242/sing/pop'])
    fn('p242/sing/pop', ['summon minecraft:marker ~ ~0.5 ~ {Tags:["bm.vxsgw"]}', 'playsound minecraft:block.end_portal.spawn player @a[distance=..24] ~ ~ ~ 0.6 1.8', 'kill @s'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.vxsgw] at @s run function bm:p242/sing/tick')
    fn('p242/sing/tick', ['scoreboard players add @s bm.vxt 1', 'particle minecraft:reverse_portal ~ ~ ~ 2 1 2 0.2 10', 'particle minecraft:dust{color:[0.75,0.55,1.0],scale:1.6} ~ ~ ~ 0.2 0.2 0.2 0 3',
                          'execute as @e[type=#bm:hostile,distance=0.8..6] at @s facing entity @e[type=minecraft:marker,tag=bm.vxsgw,sort=nearest,limit=1] feet run tp @s ^ ^ ^0.25',
                          'execute if score @s bm.vxt matches 40.. run function bm:p242/sing/crush'])
    fn('p242/sing/crush', ['particle minecraft:explosion ~ ~ ~ 0.5 0.5 0.5 0 3', 'playsound minecraft:entity.warden.sonic_boom player @a[distance=..24] ~ ~ ~ 0.6 1.6',
                           'execute as @e[type=#bm:hostile,distance=..2.5] run damage @s 14 minecraft:magic', 'kill @s'])
    # the Admiral's Crown: the hive hesitates near you
    second.append('execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"admiral_crown"}] at @s run function bm:p242/crown')
    fn('p242/crown', ['effect give @e[tag=bm.vorn,distance=..10] minecraft:slowness 2 1 true', 'effect give @s minecraft:night_vision 15 0 true',
                      'particle minecraft:dust{color:[0.48,1.0,0.42],scale:0.8} ~ ~2.2 ~ 0.25 0.05 0.25 0 2'])
    # the Starforged set: hover-jets (sneak in the air: a burst upward, every 3 s) and the star-shield (a minute's rest)
    fn('p242/sf/jet', ['execute if score @s bm.vxjc matches 1.. run return 0', 'execute unless score @s bm.sneak matches 1.. run return 0',
                       'scoreboard players set @s bm.vxjc 3', 'effect give @s minecraft:levitation 1 8 true',
                       'particle minecraft:flame ~ ~ ~ 0.2 0.1 0.2 0.05 16', 'playsound minecraft:entity.firework_rocket.launch player @a[distance=..16] ~ ~ ~ 0.8 1.4'])
    second.append('scoreboard players remove @a[scores={bm.vxjc=1..}] bm.vxjc 1')
    fn('p242/sf/shield', ['execute if score @s bm.vxsh matches 1.. run return 0', 'execute unless entity @s[nbt={HurtTime:10s}] run return 0',
                          'scoreboard players set @s bm.vxsh 1200', 'effect give @s minecraft:absorption 8 3', 'effect give @s minecraft:resistance 2 2',
                          'particle minecraft:end_rod ~ ~1 ~ 0.6 0.8 0.6 0.08 40', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 1 1.6',
                          title('@s', 'actionbar', T('STAR-SHIELD: the Starforged plate drinks the blow.', '#ffb14a', bold=True))])
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.vxsh dummy']
    G.OBJECTIVES.append('bm.vxsh')
    fast.append('scoreboard players remove @a[scores={bm.vxsh=1..}] bm.vxsh 1')

    # ================================================================== ADMIN
    fn('admin/armada/boss', ['execute unless entity @e[type=minecraft:marker,tag=bm.ahelm] run return run ' + tellraw('@s', P + [T('The bridge isn\'t loaded (or placed).', 'gray')]),
                             f'kill {ME}', 'kill @e[type=minecraft:item_display,tag=bm.vxr]', 'kill @e[type=minecraft:item_display,tag=bm.vxw]', 'kill @e[type=minecraft:marker,tag=bm.vxwreck]',
                             'function bm:p242/pyl/clear', 'scoreboard players set #afell bm.p2 0', 'function bm:p242/spawn', 'tag @s remove bm.vxdone',
                             f'execute in {END} run tp @s {W(*AR["door"])[0] + 0.5} {W(*AR["door"])[1]} {W(*AR["door"])[2] + 0.5} {(WIN - 90) % 360:.1f} 0'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/armada/boss', 'yellow'), T('  Admiral Vexis, dormant at its helm again (and you at the bridge door)', 'gray')]))
