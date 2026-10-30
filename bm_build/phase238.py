"""2.98: THE DREAD SOVEREIGN - the final boss, on its throne at the bottom of the Undercrown (phase237; dread_sovereign_art.py;
undercrown_lore.py). One in the world at a time: a husk host (invisible, scaled to its body), its rig of item displays.

DORMANT      it kneels on its throne, bound by six chains to the six pillars, until someone crosses the hall.
THE COMING   (20 s; fighters held, facing it) the battle door slams, the dark falls, a heartbeat quickens; the six chains burn red
             one after another; the six Wellsprings kindle; it lifts its head and speaks; the chains SNAP one by one (the hall
             shakes); a hand on the throne, it rises; it drags the greatsword up off the floor, raises it high - and ROARS, the wings
             flung open, a shockwave through the hall: THE DREAD SOVEREIGN. Its own music (vendor/boss_sovereign_intro.ogg).
THE FIGHT    three pools of health (each phase its own - no burst skips one), PH_HP for one fighter and more for each other one;
             Resistance II always, but not while it's grounded or tired.
  I  ARMORED  SLAM (a shockwave rolls out along the floor - jump it), SWEEP (a wide arc in front - get behind a pillar),
             STAB (it lunges), CHAINS (one far away is dragged in), DREAD KNIGHTS. The six WELLSPRINGS mend it while they burn:
             hit or shoot each crystal to shatter it; they kindle again in time.
  turn       on one knee, its plate cracking off; a roar that throws everyone back; the six wings unfurl, every eye in them open.
  II BROKEN   it hovers. WING-EYE BOLTS (homing), the HEART PULSE (rings of withering - stand between them), WING GUST (pushed
             back), SWEEP, and what it taught its three: the Snowbeast's ICE VOLLEY, the Witch's CURSE CIRCLES, the Sawshark's
             WHIRLPOOL. Its six wing-eyes can be shot out: all six, and it CRASHES DOWN, its heart open (no Resistance) for 8 s.
  turn       the helm shatters - a vast red eye in the void - and the hall's outer floor cracks (5 s) and falls into the lava sea.
  III TRUE    the EYE BEAM (it charges, then sweeps: get something solid between you - or hold the Dawnshard up), the ROOTS (step
             off them), the DARKNESS (and knights), SLAM and SWEEP. Every 40 s another island cracks and falls (four at most).
             At a quarter of its last pool it FRENZIES (12 s it can't be hurt, sigils burst under everyone) - then it TIRES, the
             eye shut: strike it.
THE FALL     it unravels (3 s). Everyone in the hall: bm.dfin (the reckoning - the Lightbringer is no longer to be found), its
             spoils, a Victor's Key, the first time the Dread Ember, the Sovereign's Eye (the follower, phase239) and its record
             (the second time Aurel's elegy). The Dread Nights end (p237/nights_end), and the Undercrown begins to come apart
             (p237/collapse: 3.0a: once its victors have claimed their spoils in the Victor's Vault, three minutes, then it is rebuilt).
THE CAMERA   (3.0a) one hold for every cinematic (p238/cam/*): turned to a look marker each tick, held (the Slowness is the
             zoom), glided back from what is shown if too near it; a 3-tick lease gives control back the moment it stops (over,
             dead, gone, relogged) - never a gamemode change, never a spectated camera entity.
ABANDONED    nobody in the hall for 30 s: it goes back to its throne, the floor is put back (p237/floor) and the Wellsprings with it."""
import math
from items import T, item, TOTEM, gear, attr
from nbt import snbt, B, F, Int, D as Dd
import rigfol as RF
import rigkit as RK
import dread_sovereign_art as A
import p2.undercfg as U
import undercrown_lore as L
import phase152 as P152

COL, VCOL = L.SOV_COL, L.VOICE_COL
OX, OY, OZ = U.ORIGIN
W = lambda x, y, z: (OX + x, OY + y, OZ + z)
AR = U.ARENA
CX, CY, CZ = W(*AR['c'])                     # the floor's top layer centre (walk y = CY + 1)
HALL = f'@a[x={CX - 40},y={CY - 12},z={CZ - 40},dx=80,dy=70,dz=80,gamemode=!spectator,gamemode=!creative]'
FIGHT = f'@a[x={CX - 40},y={CY - 12},z={CZ - 40},dx=80,dy=70,dz=80,gamemode=!spectator,gamemode=!creative]'
AUD = f'@a[x={CX - 48},y={CY - 16},z={CZ - 48},dx=96,dy=80,dz=96]'
ME = '@e[type=minecraft:husk,tag=bm.usov,limit=1]'
TGT = '@a[tag=bm.svtgt,limit=1]'
HOST_SCALE = 5.6                             # (a husk 1.95 tall: ~11 blocks - its body)
PH_HP, PH_ADD, PH_MAX = 640, 160, 900        # each phase's pool: one fighter, each other one, the most
FLOOR = 100
RESIST = 1
INTRO = 400                                  # ticks: the coming (20 s)
TURN = 160                                    # (2.98c: the old turn; each form now has its own entrance)
ENT = {1: 240, 2: 300}                        # ticks: the entrance of the Broken form (12 s), of the True form (15 s)
FORM = {1: 'armored', 2: 'broken', 3: 'true'}
SCALE = {f: A.BOSS_SCALE * A.FORM_SCALE[f] for f in FORM.values()}
SWAP = tuple(A.PARTS)
sel = lambda p: f'@e[type=minecraft:item_display,tag=bm.svr_{p}]'
# ---- the theme: its intro, its three phases, its turn (tools/sovereign_music.py)
P152.THEMES.update({18: ('sovereign1', 120), 19: ('sovereign2', 120), 20: ('sovereign3', 120), 21: ('sovereign_turn', 8), 22: ('sovereign_intro', 20),
                    23: ('sovereign_enter2', 13), 24: ('sovereign_enter3', 16), 25: ('divine', 30)})      # (2.98c: each form's own entrance)
_H = 'type=minecraft:husk,tag=bm.usov'
P152.WHO_LATE += [(18, f'{_H},tag=bm.svlive,scores={{bm.svph=1}}'), (19, f'{_H},tag=bm.svlive,scores={{bm.svph=2}}'),
                  (20, f'{_H},tag=bm.svlive,scores={{bm.svph=3}}'), (23, f'{_H},tag=bm.svturn,tag=bm.svt1'), (24, f'{_H},tag=bm.svturn,tag=bm.svt2'), (22, f'{_H},tag=bm.svintro')]

# ---- what it leaves (phase237's items hold the rest)
item('sov_eye', TOTEM, L.ITEMS['eye'][0], COL, list(L.ITEMS['eye'][1]) + [('Hard mode. From the Dread Sovereign, the first time it falls.', 'dark_gray')],
     model='bm:sov_eye', glint=True, stack=1, cat='follower', bold=True)
# (2.99) ITS WINGS - the Wings of the Damned's powers (p2/hollowtools: unbreakable, wall-proof, the sneak drive, the crouch-and-jump
# launch), in the Sovereign's own: the Last Night's six black wings full of eyes, and the First Light's - Aurel's, as they were.
# Both from its fall, every fighter (seraph_wings shows them in 3D on your back - 3.0c: when switched on, bm.w3d).
_WL = ['+6 Armour. Unbreakable. Flying into a wall', 'never hurts you.', 'Hold sneak while gliding: the wings drive you on.',
       'On the ground, crouch a moment, then jump:', 'they throw you skyward - jump again to glide.']
for _iid, _nm, _col, _first, _x in (('sov_wings', 'Wings of the Last Night', COL, 'The Dread Sovereign\'s own six wings, every eye in them open.', {}),
                                     ('sov_wings_holy', 'Wings of the First Light', L.HOLY, 'Aurel\'s wings, as they were before the dark: white fire and gold.',
                                      {'bm_angel': B(1)})):
    gear(_iid, 'elytra', _nm, _col, [_first] + [(l, 'blue') for l in _WL] + [('3D wings, for screenshots: /trigger bm.wings3d', 'dark_gray'),
                                                                          ('From the Dread Sovereign\'s fall.', 'dark_gray')],
         {'bm:damned_wings': 1}, 3, attrs=[attr('armor', 6, 'chest', ident='minecraft:armor.chestplate'), attr('armor_toughness', 2, 'chest', ident='minecraft:armor.chestplate_toughness')],
         extra={'minecraft:unbreakable': {}, 'minecraft:item_model': f'bm:{_iid}',
                'minecraft:equippable': {'slot': 'chest', 'asset_id': f'bm:{_iid}', 'equip_sound': 'minecraft:item.armor.equip_elytra', 'damage_on_hurt': False}},
         bold=True, custom_extra=dict({'bm_dwings': B(1)}, **_x))

# ---- the states and their frames: (period or None, [(tick, pose)]) per form
def _cyc(f):
    P = A.BOSS_POSES[f]
    has = lambda *n: all(x in P for x in n)
    c = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (24, [(0, 'walk_0'), (6, 'walk_1'), (12, 'walk_2'), (18, 'walk_3')]),
         7: (None, [(0, 'slam_up'), (14, 'slam')]), 8: (None, [(0, 'sweep_up'), (14, 'sweep')]), 9: (None, [(0, 'stab')]),
         11: (None, [(0, 'roar')]), 12: (None, [(0, 'summon')]), 15: (None, [(0, 'heart_pulse')]),
         16: (None, [(0, 'summon')])}            # (2.99a: calling its Mires)
    if has('wing_gust'): c[13] = (None, [(0, 'wing_gust')])
    if has('eye_beam_up', 'eye_beam'): c[14] = (None, [(0, 'eye_beam_up'), (30, 'eye_beam')])
    if has('stagger'): c[22] = (None, [(0, 'stagger')])
    if has('dormant'):
        wake = [(0, 'dormant')] + [(t, p) for t, p in ((140, 'wake_0'), (230, 'wake_1'), (250, 'rise'), (280, 'wake_2'), (320, 'wake_3')) if p in P] + [(340, 'roar')]
        c[20] = (None, [(0, 'dormant')])
        c[21] = (None, wake)
    if has('death_0', 'death_1', 'death_2'): c[31] = (None, [(0, 'death_0'), (20, 'death_1'), (40, 'death_2')])
    else: c[22] = c.get(22, (None, [(0, 'roar')]))
    return c


CYC = {f: _cyc(f) for f in FORM.values()}
DUR = {'idle_a': 30, 'idle_b': 30, 'dormant': 10, 'wake_0': 30, 'wake_1': 20, 'rise': 30, 'wake_2': 30, 'wake_3': 16, 'roar': 10, 'slam_up': 12,
       'slam': 3, 'sweep_up': 10, 'sweep': 3, 'stab': 5, 'summon': 12, 'heart_pulse': 10, 'wing_gust': 8, 'eye_beam_up': 14, 'eye_beam': 6,
       'stagger': 14, 'death_0': 12, 'death_1': 16, 'death_2': 20, **{f'walk_{i}': 6 for i in range(4)}}
# ---- the attacks: per form, (state, duration, cooldown, condition on the target, {timer value: function})
CLOSE = lambda r: f'if entity {TGT[:-1]},distance=..{r}]'
FAR = lambda a, b: f'if entity {TGT[:-1]},distance={a}..{b}]'
ATK = {'armored': [(12, 30, 500, '', {15: 'knights'}),
                   (11, 30, 200, FAR(9, 34), {20: 'chain'}),
                   (7, 34, 140, CLOSE(16), {20: 'slam'}),
                   (8, 28, 100, CLOSE(11), {14: 'sweep'}),
                   (9, 22, 120, FAR(5, 20), {**{x: 'lunge' for x in range(18, 11, -1)}, 11: 'stab'})],
       'broken': [(12, 30, 600, '', {15: 'knights'}),
                  (16, 30, 900, '', {15: 'mires'}),
                  (15, 60, 260, '', {50: 'pulse_warn', 30: 'pulse'}),
                  (11, 40, 220, '', {30: 'dread'}),
                  (13, 40, 220, CLOSE(24), {**{x: 'gust' for x in range(30, 9, -1)}}),
                  (8, 28, 90, CLOSE(12), {14: 'sweep'}),
                  (7, 30, 110, '', {20: 'bolts', 14: 'bolts', 8: 'bolts'})],
       'true': [(12, 30, 600, '', {15: 'knights'}),
                (16, 30, 900, '', {15: 'mires'}),
                (14, 75, 260, '', {45: 'beam_start', **{x: 'beam' for x in range(44, 4, -1)}}),
                (11, 30, 300, '', {15: 'dark'}),
                (15, 30, 160, '', {28: 'roots', 8: 'roots_snap'}),
                (7, 34, 140, CLOSE(16), {20: 'slam'}),
                (8, 28, 100, CLOSE(12), {14: 'sweep'})]}
STATES = sorted({a[0] for v in ATK.values() for a in v})


def ring_pts(r, n):
    return [(round(r * math.cos(2 * math.pi * k / n), 2), round(r * math.sin(2 * math.pi * k / n), 2)) for k in range(n)]


def _floor_fall():
    """the cells of the floor that fall at the second turn (fill commands, world), and each island's ring (for phase III)"""
    acx, _ay, acz = AR['c']; y0, y1 = AR['floor']
    pil = [(acx + AR['pil_r'] * math.cos(math.radians(a)), acz + AR['pil_r'] * math.sin(math.radians(a))) for a in range(0, 360, 360 // AR['pil_n'])]
    tx, _ty, tz = AR['throne']

    import phase237
    dais = {(c[0], c[1]) for c in phase237.build().meta['under'].get('dais', ())}

    def falls(x, z):
        if (x, z) in dais: return False
        r = math.hypot(x - acx, z - acz)
        if r <= AR['inner'] + 0.5 or r > AR['r'] + 0.5: return False
        if any(math.hypot(x - px, z - pz) <= AR['isl_r'] + 0.5 for px, pz in pil): return False
        return math.hypot(x - tx, z - tz) > 8.5

    def runs(test):
        out = []
        for z in range(acz - AR['r'], acz + AR['r'] + 1):
            x = acx - AR['r']
            while x <= acx + AR['r']:
                if test(x, z):
                    x0 = x
                    while x + 1 <= acx + AR['r'] and test(x + 1, z): x += 1
                    a, b = W(x0, y0, z), W(x, y1, z)
                    out.append(f'fill {a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]} minecraft:air')
                x += 1
        return out
    isl = []
    for px, pz in pil:
        isl.append(runs(lambda x, z, px=px, pz=pz: AR['pil_w'] + 0.6 < math.hypot(x - px, z - pz) <= AR['isl_r'] + 0.5 and math.hypot(x - acx, z - acz) > AR['inner'] + 0.5))
    return runs(falls), isl, pil


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
    objs = ['bm.svph', 'bm.sva', 'bm.svx', 'bm.svf', 'bm.svs', 'bm.svt', 'bm.svg', 'bm.svw', 'bm.svi', 'bm.svz', 'bm.svwin', 'bm.svhp', 'bm.svhc', 'bm.svcm'] + \
           [f'bm.svk{s}' for s in STATES]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs] + [
        f'bossbar add bm:usov {snbt(T(L.SOV, COL, bold=True))}', 'bossbar set bm:usov color red', 'bossbar set bm:usov style notched_10']
    G.OBJECTIVES += objs
    say = lambda line, who=AUD: tellraw(who, [T(L.SOV + ': ', COL, bold=True), T(line, VCOL, italic=True)])
    snd = lambda s, v, p, who=AUD: f'execute as {who} at @s run playsound minecraft:{s} hostile @s ~ ~ ~ {v} {p}'
    at = lambda t, cmd: f'execute if score @s bm.svt matches {t} run {cmd}'

    # ================================================================== the rig: summoned once, posed by form
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.svr", f"bm.svr_{p}", "bm.usov_part"], SCALE["armored"], model=A.model_name(p, A.BOSS_POSES["armored"]["dormant"]), extra=dict(view_range=F(4.0), brightness={"block": Int(12), "sky": Int(12)}))}'
           for p in A.PARTS]
    for f in FORM.values():
        fn(f'p238/place/{f}', RF.place(A, SCALE[f] / 16, sel))
        for name, pz in A.BOSS_POSES[f].items():
            fn(f'p238/pose/{f}/{name}', RF.pose(A, pz, SCALE[f], DUR.get(name, 6), sel, swap=SWAP))
        RF.cycles(fn, f'p238/{f}', CYC[f], 'bm.svf', 'bm.svs', lambda p, f=f: f'p238/pose/{f}/{p}')
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for f in FORM.values() for n in RF.periods(CYC[f])]
    # (its face: the slit's mood rides each pose; for the frenzy and the tire, forced)
    host = {'Tags': ['bm.usov', 'bm.boss', 'bm.seen', 'bm.svnew'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
            'CustomName': T(L.SOV, COL), 'Invulnerable': B(1), 'DeathLootTable': 'minecraft:empty',
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(PH_HP + FLOOR)}, {'id': 'minecraft:scale', 'base': Dd(HOST_SCALE)},
                           {'id': 'minecraft:armor', 'base': Dd(20)}, {'id': 'minecraft:armor_toughness', 'base': Dd(12)},
                           {'id': 'minecraft:knockback_resistance', 'base': Dd(1.0)}, {'id': 'minecraft:follow_range', 'base': Dd(64)}],
            'Health': F(PH_HP + FLOOR),
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    tx, ty, tz = W(*AR['throne'])
    fn('p238/spawn', [f'execute positioned {tx + 0.5} {ty} {tz + 0.5} rotated 0 0 run summon minecraft:husk ~ ~ ~ {snbt(host)}',
                      f'execute positioned {tx + 0.5} {ty} {tz + 0.5} run function bm:p238/rig',
                      f'execute as {ME} at @s run function bm:p238/dormant'])
    fn('p238/rig', rig + ['tag @e[tag=bm.svnew] remove bm.svnew'])
    fn('p238/dormant', ['scoreboard players set @s bm.svph 1', 'scoreboard players set @s bm.sva 20', 'scoreboard players set @s bm.svx 0',
                        'scoreboard players set @s bm.svs -1', 'scoreboard players set @s bm.svf 0', 'scoreboard players set @s bm.svg 0',
                        'tag @s add bm.svdorm', 'tag @s remove bm.svlive', 'data modify entity @s Invulnerable set value 1b',
                        'execute rotated 0 0 run tp @s ~ ~ ~ 0 0', 'execute rotated 0 0 run function bm:p238/place/armored',
                        'function bm:p238/pose/armored/dormant'])
    # (one Sovereign, on its throne, whenever the hall is loaded and it isn't fallen; nobody can see it till the stair is passed)
    second.append(f'execute if score #ufell bm.p2 matches 0 if entity @e[type=minecraft:marker,tag=bm.uthrone] unless entity {ME} '
                  f'as @e[type=minecraft:marker,tag=bm.uthrone,limit=1] at @s run function bm:p238/spawn')

    # ================================================================== every tick: its mind, its body
    tick.append(f'execute as {ME} at @s run function bm:p238/tick')
    form_of = lambda f: [f'execute if score @s bm.svph matches {i} run function bm:p238/{FORM[i]}/{f}' for i in FORM]
    fn('p238/tick', ['tag @a[tag=bm.svtgt] remove bm.svtgt',
                     f'tag {FIGHT[:-1]},sort=nearest,limit=1] add bm.svtgt',
                     'execute if entity @s[tag=bm.svdorm] run return run function bm:p238/asleep',
                     'execute if entity @s[tag=bm.svintro] run function bm:p238/intro',
                     'execute store result score #hp bm.rng run data get entity @s Health',
                     f'execute if entity @s[tag=bm.svlive] if score #hp bm.rng matches ..{FLOOR} run function bm:p238/floor_hit',
                     'execute if score @s bm.svx matches 1.. run scoreboard players remove @s bm.svx 1'] +
       [f'execute if score @s bm.svk{s} matches 1.. run scoreboard players remove @s bm.svk{s} 1' for s in STATES] +
       ['execute if entity @s[tag=bm.svlive] if entity @a[tag=bm.svtgt] run function bm:p238/mind'] + form_of('beats') +
       ['execute if entity @s[tag=bm.svturn] run function bm:p238/turn_tick',
        'execute if entity @s[tag=bm.svfall] run function bm:p238/falling',
        'function bm:p238/state',
        'execute if score #st bm.rng = @s bm.svs run scoreboard players add @s bm.svf 1',
        'execute unless score #st bm.rng = @s bm.svs run scoreboard players set @s bm.svf 0',
        'scoreboard players operation @s bm.svs = #st bm.rng'] + form_of('body'))
    for i, f in FORM.items():
        fn(f'p238/{f}/body', [f'function bm:p238/{f}/anim', f'execute rotated as @s rotated ~ 0 run function bm:p238/place/{f}'])
    fn('p238/asleep', ['execute rotated 0 0 run function bm:p238/place/armored',
                       f'execute positioned {CX} {CY + 1} {CZ} if entity @a[distance=..24,gamemode=!spectator,gamemode=!creative,tag=!bm.svdone] run function bm:p238/wake',   # (someone crosses the hall)
                       # (2.98c) one who has felled it: it does not stir for them - until they kindle its Ember
                       f'execute positioned {CX} {CY + 1} {CZ} as @a[distance=..24,gamemode=!spectator,tag=bm.svdone] run function bm:p238/stirless'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #60 bm.rng 60']
    fn('p238/stirless', ['execute store result score #g bm.rng run time query gametime', 'scoreboard players operation #g bm.rng %= #60 bm.rng',
                         'execute unless score #g bm.rng matches 0..2 run return 0',
                         title('@s', 'actionbar', [T('It does not stir for you. ', COL, italic=True), T('You felled it once; kindle its Dread Ember, and it will rise for you again.', 'gray')])])
    fn('p238/state', ['execute if score @s bm.svx matches 1.. run return run scoreboard players operation #st bm.rng = @s bm.sva',
                      'execute if entity @s[tag=bm.svmove] run return run scoreboard players set #st bm.rng 1', 'scoreboard players set #st bm.rng 0'])

    # ---- its mind: an attack it's ready for, else it closes on its quarry (keeping to its hall)
    for f, atks in ATK.items():
        choose = [' '.join(x for x in [f'execute unless score @s bm.svx matches 1.. unless score @s bm.svk{st} matches 1..', cond, f'run function bm:p238/go{st}'] if x)
                  for st, _d, _cd, cond, _b in atks]
        fn(f'p238/{f}/mind', choose + [f'execute unless score @s bm.svx matches 1.. run function bm:p238/move'])
        beats = []
        for st, _d, _cd, _c, bt in atks:
            for x, f_ in bt.items():
                beats.append(f'execute if score @s bm.sva matches {st} if score @s bm.svx matches {x} run function bm:p238/a/{f_}')
        fn(f'p238/{f}/beats', beats)
    for st in STATES:
        dur, cd = next((a[1], a[2]) for v in ATK.values() for a in v if a[0] == st)
        fn(f'p238/go{st}', [f'scoreboard players set @s bm.sva {st}', f'function bm:p238/dur{st}', f'scoreboard players set @s bm.svk{st} {cd}',
                            f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~'])
        fn(f'p238/dur{st}', [f'execute if score @s bm.svph matches {i} run scoreboard players set @s bm.svx {a[1]}' for i, f in FORM.items() for a in ATK[f] if a[0] == st] or
           ['scoreboard players set @s bm.svx 30'])
    fn('p238/mind', form_of('mind'))
    fn('p238/move', [f'execute facing entity {TGT} feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~', 'tag @s remove bm.svmove',
                     # (it keeps to its hall: beyond 24 of the centre, back it comes)
                     f'execute unless entity @s[x={CX - 24},y={CY - 10},z={CZ - 24},dx=48,dy=50,dz=48] facing {CX} {CY + 1} {CZ} rotated ~ 0 run return run function bm:p238/step',
                     f'execute if entity {TGT[:-1]},distance=6..] rotated as @s rotated ~ 0 if block ^ ^1 ^2.5 #bm:grap_pass if block ^ ^2 ^2.5 #bm:grap_pass run function bm:p238/step'])
    fn('p238/step', ['tag @s add bm.svmove', 'execute if score @s bm.svph matches 1 rotated as @s rotated ~ 0 run tp @s ^ ^ ^0.14',
                     'execute if score @s bm.svph matches 2.. rotated as @s rotated ~ 0 run tp @s ^ ^ ^0.12',
                     'execute if score @s bm.svph matches 1 if score @s bm.svf matches 0 run function bm:p238/a/stomp',
                     'execute if score @s bm.svph matches 1 if score @s bm.svf matches 12 run function bm:p238/a/stomp'])

    # ================================================================== THE COMING (20 s)
    falls, islands, pil = _floor_fall()
    pil_w = [W(px, AR['well_y'], pz) for px, pz in pil]
    hx, hy, hz = tx + 0.5, ty + 9.5, tz + 0.5                 # (its head, kneeling, roughly)
    chain_line = lambda i, col='0.82,0.08,0.16', n=24: [f'particle minecraft:dust{{color:[{col}],scale:1.8}} {tx + 0.5 + (pil_w[i][0] + 0.5 - tx - 0.5) * k / n:.2f} '
                                                        f'{ty + 3 + (pil_w[i][1] - ty - 3) * k / n:.2f} {tz + 0.5 + (pil_w[i][2] + 0.5 - tz - 0.5) * k / n:.2f} 0.1 0.1 0.1 0 2 force {AUD}'
                                                        for k in range(n + 1)]
    for i in range(len(pil)):
        fn(f'p238/c/glow{i}', chain_line(i) + [snd('block.chain.place', 1.5, 0.5), snd('block.respawn_anchor.charge', 1, 0.5 + 0.08 * i)])
        fn(f'p238/c/snap{i}', chain_line(i, '0.2,0.2,0.22', 12) +
           [f'particle minecraft:explosion {pil_w[i][0] + 0.5} {pil_w[i][1]} {pil_w[i][2] + 0.5} 0.5 0.5 0.5 0 3 force {AUD}',
            f'particle minecraft:block{{block_state:"minecraft:iron_chain"}} {pil_w[i][0] + 0.5} {pil_w[i][1]} {pil_w[i][2] + 0.5} 1 1 1 0 40 force {AUD}',
            snd('block.anvil.land', 1.5, 0.5), snd('block.chain.break', 2, 0.4), snd('entity.generic.explode', 0.8, 0.6), 'function bm:p238/c/shake'])
    import random
    rs = random.Random(238)
    shk = []
    for k in range(4):
        a = 1.6 * (1 - k / 4)
        dx, dy = a * rs.choice((-1, 1)), a * 0.6 * rs.choice((-1, 1))
        shk.append((dx, dy))
    fn('p238/c/shake', [f'execute as {FIGHT} at @s run rotate @s ~{dx:.2f} ~{dy:.2f}' for dx, dy in shk[:2]])
    # ---- (3.0a) THE CAMERA, one hold for every cinematic (the coming, each form's entrance, the Last Light): each tick, each
    # fighter is turned to the look marker (bm.svlook), held still (the slowness is also the forced zoom), unhurt; anyone too
    # close to what is being shown (a keep-out marker: bm.svko 14, bm.svkos 9) glides back from it over the floor (never off
    # it) - so every entrance is framed as the first is, from across the hall, not from under its chin. A held player is
    # tagged bm.svcam with a 3-tick lease (bm.svcm); the lease runs out the moment the holding stops - the cinematic over,
    # its fighter dead, gone from the hall, logged out and back - and cam/release gives them their body back at once (the
    # lock's own slowness / jump / resistance cleared, nothing else). No gamemode is ever changed, no camera entity spectated.
    fn('p238/cam/all', [f'execute as {FIGHT} at @s run function bm:p238/cam/hold'])
    fn('p238/cam/hold', ['tag @s add bm.svcam', 'scoreboard players set @s bm.svcm 3',
                         'execute if entity @e[type=minecraft:marker,tag=bm.svko,distance=..14] facing entity @e[type=minecraft:marker,tag=bm.svko,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p238/cam/back',
                         'execute if entity @e[type=minecraft:marker,tag=bm.svkos,distance=..9] facing entity @e[type=minecraft:marker,tag=bm.svkos,sort=nearest,limit=1] feet rotated ~ 0 run function bm:p238/cam/back',
                         'execute at @s if entity @e[type=minecraft:marker,tag=bm.svlook] run tp @s ~ ~ ~ facing entity @e[type=minecraft:marker,tag=bm.svlook,limit=1] feet',
                         'effect give @s minecraft:slowness 2 255 true', 'effect give @s minecraft:resistance 2 255 true', 'effect give @s minecraft:jump_boost 2 200 true'])
    # (a carpet - the throne's red runner - is walked over, not into: bm:cam_pass is grap_pass and the carpets, at the feet)
    wjson('bm/tags/block/cam_pass.json', {'values': ['#bm:grap_pass', '#minecraft:wool_carpets', 'minecraft:moss_carpet', 'minecraft:pale_moss_carpet']})
    fn('p238/cam/back', ['execute if block ^ ^ ^-0.7 #bm:cam_pass if block ^ ^1 ^-0.7 #bm:grap_pass unless block ^ ^-0.6 ^-0.7 #bm:grap_pass run tp @s ^ ^ ^-0.7'])
    fn('p238/cam/release', ['tag @s remove bm.svcam', 'scoreboard players reset @s bm.svcm',
                            'execute if predicate bm:p238/cam_slow run effect clear @s minecraft:slowness',
                            'execute if predicate bm:p238/cam_jump run effect clear @s minecraft:jump_boost',
                            'execute if predicate bm:p238/cam_res run effect clear @s minecraft:resistance'])
    for nm_, eff, amp in (('slow', 'slowness', 200), ('jump', 'jump_boost', 128), ('res', 'resistance', 200)):
        wjson(f'bm/predicate/p238/cam_{nm_}.json', {'condition': 'minecraft:entity_properties', 'entity': 'this',
                                                    'predicate': {'minecraft:effects': {f'minecraft:{eff}': {'amplifier': {'min': amp}}}}})
    fn('p238/cam/lease', ['scoreboard players remove @s bm.svcm 1', 'execute unless score @s bm.svcm matches 1.. run function bm:p238/cam/release'])
    tick.append('execute as @a[tag=bm.svcam] at @s run function bm:p238/cam/lease')
    G.FUNCS['admin/uninstall'][0:0] = ['execute as @a[tag=bm.svcam] at @s run function bm:p238/cam/release']
    CAMM = 'kill @e[type=minecraft:marker,tag=bm.svcamm]'
    fn('p238/c/hold', ['function bm:p238/cam/all'])
    heart = (1, 30, 56, 80, 102, 122, 140, 156, 170, 182, 194, 204, 214, 222, 230, 238, 246, 252, 258, 264, 270, 276, 282, 288, 294, 300)
    shock = lambda r_: [f'particle minecraft:dust{{color:[0.85,0.1,0.16],scale:3.0}} {tx + 0.5 + x:.2f} {ty + 0.3} {tz + 0.5 + z:.2f} 0.2 0.05 0.2 0 2 force {AUD}'
                        for x, z in ring_pts(r_, int(6 * r_))]
    for r_ in (4, 10, 18, 28):
        fn(f'p238/c/wave{r_}', shock(r_))
    seq = ([at(1, 'function bm:p238/c/door'), at(1, f'effect give {FIGHT} minecraft:darkness 20 0 true'), at(1, snd('block.beacon.deactivate', 2, 0.4)),
            at(1, snd('block.iron_door.close', 2, 0.4)), at(1, title(AUD, 'actionbar', T('The Undercrown holds its breath.', 'gray', italic=True)))] +
           [at(t, snd('entity.warden.heartbeat', 0.8 + j * 0.05, 0.5 + j * 0.02)) for j, t in enumerate(heart)] +
           [at(t, f'particle minecraft:falling_dust{{block_state:"minecraft:blackstone"}} {CX} {CY + 40} {CZ} 20 2 20 0 40 force {AUD}') for t in range(20, 140, 10)] +
           [at(20, snd('block.chain.step', 2, 0.4)), at(36, snd('block.chain.step', 2, 0.35)),
            at(40, say(L.FIGHT['wake'][0]))] +
           [at(60 + 10 * i, f'function bm:p238/c/glow{i}') for i in range(len(pil))] +
           [at(t, f'function bm:p238/c/glow{i}') for i in range(len(pil)) for t in range(60 + 10 * i + 10, 180, 20)] +
           [at(120 + 10 * i, f'function bm:p238/w/light{i + 1}') for i in range(len(pil))] +
           [at(140, 'data merge entity @e[type=minecraft:item_display,tag=bm.svr_head,limit=1] {brightness:{block:15,sky:15}}'),
            at(140, f'particle minecraft:flash{{color:[1.0,0.1,0.15,1.0]}} {hx} {hy} {hz} 0 0 0 0 1 force {AUD}'),
            at(140, snd('entity.warden.emerge', 2, 0.5)), at(150, say('"I have waited an age under your feet."'))] +
           [at(180 + 10 * i, f'function bm:p238/c/snap{i}') for i in range(len(pil))] +
           [at(184, say('"These chains were forged for me. Watch."')),
            at(232, snd('entity.ravager.stunned', 2, 0.4)), at(232, snd('block.deepslate.break', 2, 0.4)),
            at(250, 'function bm:p238/c/shake'), at(254, 'function bm:p238/c/shake'), at(258, 'function bm:p238/c/shake'),
            at(250, f'particle minecraft:block{{block_state:"minecraft:blackstone"}} {tx + 0.5} {ty} {tz + 2} 4 0.5 4 0 200 force {AUD}'),
            at(250, snd('entity.iron_golem.damage', 2, 0.3)),
            at('280..318', f'particle minecraft:lava {tx + 0.5} {ty + 0.2} {tz + 4} 1.5 0.1 2 0 3 force {AUD}'),
            at(280, snd('block.grindstone.use', 2, 0.4)), at(296, snd('block.grindstone.use', 2, 0.35)),
            at(320, f'particle minecraft:flash{{color:[1.0,0.2,0.2,1.0]}} {hx} {hy + 6} {hz} 0 0 0 0 1 force {AUD}'),
            at(320, snd('item.trident.thunder', 2, 0.5)), at(320, snd('entity.warden.sonic_charge', 2, 0.4)),
            # (THE ROAR)
            at(340, snd('entity.ender_dragon.growl', 3, 0.5)), at(340, snd('entity.warden.roar', 3, 0.5)), at(340, snd('entity.ravager.roar', 3, 0.4)),
            at(340, snd('entity.warden.sonic_boom', 2, 0.5)), at(340, snd('entity.generic.explode', 2, 0.5)),
            at(340, f'particle minecraft:explosion_emitter {hx} {ty + 4} {hz} 2 2 2 0 3 force {AUD}'),
            at(340, f'particle minecraft:sculk_soul {hx} {ty + 6} {hz} 6 5 6 0.1 300 force {AUD}'),
            at(340, 'function bm:p238/c/wave4'), at(343, 'function bm:p238/c/wave10'), at(346, 'function bm:p238/c/wave18'), at(349, 'function bm:p238/c/wave28')] +
           [at(t, 'function bm:p238/c/shake') for t in range(340, 372, 4)] +
           [at(341, f'effect clear {FIGHT} minecraft:darkness'),
            at(342, f'title {AUD} times 4 70 20'), at(342, title(AUD, 'title', T('THE DREAD SOVEREIGN', COL, bold=True))),
            at(342, title(AUD, 'subtitle', T('the first light, gone out', '#c8a0a0', italic=True))),
            at(372, say(L.VOICE['ante'])),
            at(INTRO, 'function bm:p238/begin')] +
           [at(f'1..{INTRO - 2}', 'function bm:p238/c/hold')])
    fn('p238/intro', ['scoreboard players add @s bm.svt 1'] + seq)
    fn('p238/c/door', ['execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_under] at @s run function bm:p2/under/adoor_close'])
    fn('p238/c/door_open', ['execute as @e[type=minecraft:marker,tag=bm.adoor,tag=bm.d_under] at @s run function bm:p2/under/adoor_open'])
    fn('p238/wake', ['tag @s remove bm.svdorm', 'tag @s add bm.svintro', 'scoreboard players set @s bm.svt 0', 'scoreboard players set @s bm.sva 21',
                     CAMM, f'summon minecraft:marker {hx} {hy} {hz} {{Tags:["bm.svlook","bm.svcamm"]}}', f'summon minecraft:marker {tx + 0.5} {ty} {tz + 0.5} {{Tags:["bm.svko","bm.svcamm"]}}',
                     f'scoreboard players set @s bm.svx {INTRO + 4}',
                     # (each phase's pool, for as many as are in the hall)
                     f'execute store result score #n bm.rng if entity {FIGHT}', 'scoreboard players remove #n bm.rng 1',
                     f'scoreboard players set #ph bm.rng {PH_ADD}', 'scoreboard players operation #n bm.rng *= #ph bm.rng',
                     f'scoreboard players add #n bm.rng {PH_HP}', f'execute if score #n bm.rng matches {PH_MAX}.. run scoreboard players set #n bm.rng {PH_MAX}',
                     'scoreboard players operation @s bm.svhp = #n bm.rng',
                     f'execute as {AUD} at @s run function bm:p152/tick'])
    fn('p238/begin', ['tag @s remove bm.svintro', 'tag @s add bm.svlive', CAMM, 'data modify entity @s Invulnerable set value 0b', 'scoreboard players set @s bm.sva 0',
                      'scoreboard players set @s bm.svx 20', 'function bm:p238/fill', 'bossbar set bm:usov visible true',
                      f'bossbar set bm:usov name {snbt([T(L.SOV, COL, bold=True), T("  -  " + L.FIGHT["p1"], "#c8a0a0")])}', 'bossbar set bm:usov color red',
                      'scoreboard players set @s bm.svk12 300', 'scoreboard players set @s bm.svk11 80', f'execute as {AUD} at @s run function bm:p152/tick'])
    # (a phase's pool: max health to it, health to the top)
    fn('p238/sethp', [f'$attribute @s minecraft:max_health base set $(m)', '$data modify entity @s Health set value $(m).0f'])
    fn('p238/fill', ['scoreboard players operation #m bm.rng = @s bm.svhp', f'scoreboard players add #m bm.rng {FLOOR}',
                     'execute store result storage bm:p238 hp.m int 1 run scoreboard players get #m bm.rng',
                     'function bm:p238/sethp with storage bm:p238 hp',
                     f'effect give @s minecraft:resistance infinite {RESIST} true', 'execute store result bossbar bm:usov max run scoreboard players get @s bm.svhp'])
    # ---- every second: the bar; nobody left in the hall for 30 s -> back to its throne
    second.append(f'execute as {ME} at @s run function bm:p238/sec')
    fn('p238/sec', ['execute if entity @s[tag=bm.svdorm] run return 0',
                    'execute store result score #hp bm.rng run data get entity @s Health', f'scoreboard players remove #hp bm.rng {FLOOR}',
                    'execute if score #hp bm.rng matches ..-1 run scoreboard players set #hp bm.rng 0',
                    'execute store result bossbar bm:usov value run scoreboard players get #hp bm.rng', f'bossbar set bm:usov players {AUD}',
                    f'execute if entity {FIGHT} run scoreboard players set @s bm.svg 0', f'execute unless entity {FIGHT} run scoreboard players add @s bm.svg 1',
                    'execute if score @s bm.svg matches 30.. run function bm:p238/abandon',
                    'execute if score @s bm.svph matches 1 if entity @s[tag=bm.svlive] run function bm:p238/w/sec',
                    'execute if score @s bm.svph matches 3 if entity @s[tag=bm.svlive] run function bm:p238/isle/sec',
                    'execute if score @s bm.svz matches 1.. run function bm:p238/frenzy_sec',
                    f'execute unless entity @s[tag=bm.svground] unless score @s bm.svz matches -99..-1 run effect give @s minecraft:resistance infinite {RESIST} true'])
    fn('p238/abandon', [say(L.FIGHT['abandon']), 'function bm:p238/clear', 'function bm:p237/floor', 'function bm:p238/c/door_open',
                        'bossbar set bm:usov visible false', 'kill @e[type=minecraft:item_display,tag=bm.svr]', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p238/clear', ['execute as @e[type=minecraft:husk,tag=bm.svm] at @s run function bm:p246/melt', 'kill @e[tag=bm.svk]', 'kill @e[type=minecraft:husk,tag=bm.sveye]', 'kill @e[type=minecraft:marker,tag=bm.svfx]',
                      'execute as @e[type=minecraft:marker,tag=bm.uwell] at @s run function bm:p238/w/out', 'scoreboard players reset * bm.svi',
                      # (3.0a: nothing of one phase drags anyone through the next one's entrance - the chain, the whirlpool - and no old camera marker)
                      'scoreboard players set #chn bm.rng 0', 'tag @a[tag=bm.svchained] remove bm.svchained', 'scoreboard players set #whl bm.rng 0', CAMM])
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.usov]', 'kill @e[tag=bm.svr]', 'kill @e[tag=bm.svfx]', 'kill @e[tag=bm.sveye]', 'bossbar remove bm:usov']

    # ================================================================== THE WELLSPRINGS (phase I)
    gem = {'Tags': ['bm.svwg'], 'item': {'id': 'minecraft:paper', 'count': Int(1), 'components': {'minecraft:item_model': 'bm:sov_heart'}},
           'billboard': 'vertical', 'brightness': {'block': Int(15), 'sky': Int(15)},
           'transformation': {'left_rotation': [F(0), F(0), F(0), F(1)], 'right_rotation': [F(0), F(0), F(0), F(1)], 'translation': [F(0), F(0.5), F(0)], 'scale': [F(1.3)] * 3}}
    for i in range(1, U.WELLS + 1):
        fn(f'p238/w/light{i}', [f'execute as @e[type=minecraft:marker,tag=bm.uw{i}] at @s run function bm:p238/w/on'])
    fn('p238/w/on', ['execute if entity @s[tag=bm.svlit] run return 0', 'tag @s add bm.svlit', 'scoreboard players set @s bm.svw 0',
                     f'summon minecraft:item_display ~ ~-0.5 ~ {snbt(gem)}',
                     'summon minecraft:interaction ~ ~-0.5 ~ {Tags:["bm.svwi"],width:1.4f,height:1.6f,response:1b}',
                     'particle minecraft:flame ~ ~ ~ 0.4 0.4 0.4 0.08 40 force', 'playsound minecraft:block.respawn_anchor.charge hostile @a[distance=..48] ~ ~ ~ 1.5 0.6'])
    fn('p238/w/out', ['tag @s remove bm.svlit', 'kill @e[type=minecraft:item_display,tag=bm.svwg,distance=..1.5]', 'kill @e[type=minecraft:interaction,tag=bm.svwi,distance=..1.5]'])
    fn('p238/w/break', ['function bm:p238/w/out', 'scoreboard players set @s bm.svw 45',
                        'particle minecraft:block{block_state:"minecraft:redstone_block"} ~ ~ ~ 0.5 0.5 0.5 0 60 force', 'particle minecraft:explosion ~ ~ ~ 0 0 0 0 1 force',
                        'playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 2 0.5', 'playsound minecraft:block.respawn_anchor.deplete hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                        title(AUD, 'actionbar', T(L.FIGHT['wellspring'], '#ff8a8a')),
                        'execute unless entity @e[type=minecraft:marker,tag=bm.uwell,tag=bm.svlit] run ' + title(AUD, 'actionbar', T(L.FIGHT['wells_all'], 'gold', bold=True))])
    # (a crystal shatters to a blow or an arrow)
    fast.append('execute as @e[type=minecraft:interaction,tag=bm.svwi] if data entity @s attack at @s positioned ~ ~0.5 ~ as @e[type=minecraft:marker,tag=bm.uwell,tag=bm.svlit,distance=..1.5,limit=1] at @s run function bm:p238/w/break')
    fast.append('execute as @e[type=minecraft:marker,tag=bm.uwell,tag=bm.svlit] at @s if entity @e[type=#minecraft:arrows,distance=..1.6] run function bm:p238/w/break')
    fn('p238/w/sec', [f'execute as @e[type=minecraft:marker,tag=bm.uwell,tag=bm.svlit] at @s run function bm:p238/w/feed',
                      'execute as @e[type=minecraft:marker,tag=bm.uwell,tag=!bm.svlit,scores={bm.svw=1..}] run scoreboard players remove @s bm.svw 1',
                      'execute as @e[type=minecraft:marker,tag=bm.uwell,tag=!bm.svlit,scores={bm.svw=1}] at @s run function bm:p238/w/on'])
    fn('p238/w/feed', [f'execute as {ME} run function bm:p238/w/mend', f'execute facing entity {ME} eyes run particle minecraft:dust{{color:[0.9,0.1,0.15],scale:1.5}} ^ ^ ^2 0.1 0.1 0.1 0 4 force',
                       'particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.02 3'])
    fn('p238/w/mend', ['execute store result score #mh bm.rng run data get entity @s Health', 'scoreboard players add #mh bm.rng 3',
                       'execute store result storage bm:p238 hp.h int 1 run scoreboard players get #mh bm.rng', 'function bm:p238/heal with storage bm:p238 hp'])
    fn('p238/heal', ['$data modify entity @s Health set value $(h).0f'])

    # ================================================================== THE TURNS
    fn('p238/floor_hit', ['execute if score @s bm.svph matches 3 run return run function bm:p238/fall',
                          'tag @s remove bm.svlive', 'tag @s add bm.svturn', 'data modify entity @s Invulnerable set value 1b', 'scoreboard players set @s bm.svt 0',
                          'scoreboard players set @s bm.sva 22', 'function bm:p238/clear',
                          f'execute if score @s bm.svph matches 1 run scoreboard players set @s bm.svx {ENT[1] + 4}', f'execute if score @s bm.svph matches 2 run scoreboard players set @s bm.svx {ENT[2] + 4}',
                          'execute if score @s bm.svph matches 1 run tag @s add bm.svt1', 'execute if score @s bm.svph matches 2 run tag @s add bm.svt2',
                          # (3.0a: crashed down when its turn came? up again now - and the scheduled rise can't make the wing-eyes mid-entrance)
                          'tag @s remove bm.svground', 'schedule clear bm:p238/unground',
                          'execute at @s run summon minecraft:marker ~ ~9.5 ~ {Tags:["bm.svlook","bm.svcamm"]}', 'execute at @s run summon minecraft:marker ~ ~ ~ {Tags:["bm.svko","bm.svcamm"]}',
                          'bossbar set bm:usov color purple', f'execute as {AUD} at @s run function bm:p152/tick'])
    # (2.98c) EACH FORM'S ENTRANCE - everyone's eyes held on it (the look marker rides its head), the hall dark, the change slow
    look = '@e[type=minecraft:marker,tag=bm.svlook,limit=1]'
    fn('p238/c/look', ['function bm:p238/cam/all'])
    rs2 = random.Random(2381)
    crack = lambda k: [f'particle minecraft:block{{block_state:"minecraft:blackstone"}} ~{rs2.uniform(-2, 2):.1f} ~{rs2.uniform(3, 9):.1f} ~{rs2.uniform(-2, 2):.1f} 0.6 0.6 0.6 0 40 force {AUD}',
                       f'particle minecraft:dust{{color:[1.0,0.15,0.2],scale:2.5}} ~{rs2.uniform(-2, 2):.1f} ~{rs2.uniform(3, 9):.1f} ~{rs2.uniform(-2, 2):.1f} 0.3 0.3 0.3 0 20 force {AUD}',
                       snd('block.anvil.land', 1.2, 0.4 + 0.05 * k), snd('entity.iron_golem.damage', 1.5, 0.3 + 0.04 * k)]
    for k in range(6):
        fn(f'p238/c/crack{k}', crack(k))
    eye_ping = lambda k: [f'particle minecraft:flash{{color:[1.0,0.1,0.15,1.0]}} ~{(-1) ** k * rs2.uniform(3, 7):.1f} ~{rs2.uniform(6, 11):.1f} ~{rs2.uniform(1, 3):.1f} 0 0 0 0 1 force {AUD}',
                          snd('block.amethyst_block.chime', 2, 0.5 + 0.06 * k), snd('entity.warden.listening', 1, 0.6 + 0.05 * k)]
    for k in range(18):
        fn(f'p238/c/eye{k}', eye_ping(k))
    beat = lambda t0, t1, step: [at(t, snd('entity.warden.heartbeat', 1.6, 0.5)) for t in range(t0, t1, step)]
    turn1 = ([at(1, say(L.FIGHT['turn1'])), at(1, snd('entity.iron_golem.death', 2, 0.4)), at(1, snd('block.anvil.destroy', 2, 0.5)),
              at(1, 'function bm:p238/pose/armored/stagger'), at(1, f'effect give {FIGHT} minecraft:darkness 7 0 true'),
              at(1, title(AUD, 'actionbar', T('It falls to one knee. Its plate is splitting.', '#c8a0a0', italic=True)))] +
             beat(10, 80, 14) + [at(10 + 12 * k, f'function bm:p238/c/crack{k}') for k in range(6)] +
             [at(80, f'particle minecraft:explosion_emitter ~ ~6 ~ 2 3 2 0 3 force {AUD}'), at(80, snd('entity.generic.explode', 3, 0.5)), at(80, snd('block.glass.break', 3, 0.4)),
              at(80, f'particle minecraft:block{{block_state:"minecraft:blackstone"}} ~ ~6 ~ 3 4 3 0 400 force {AUD}'), at(80, 'function bm:p238/c/shake'),
              at(80, 'scoreboard players set @s bm.svph 2'), at(80, 'function bm:p238/pose/broken/stagger'),
              at(96, 'function bm:p238/pose/broken/roar'), at(96, snd('entity.phantom.flap', 3, 0.3)), at(96, snd('entity.ender_dragon.flap', 3, 0.4)),
              at(96, f'particle minecraft:sculk_soul ~ ~8 ~ 8 4 8 0.05 200 force {AUD}')] +
             [at(110 + 3 * k, f'function bm:p238/c/eye{k}') for k in range(18)] +
             [at(170, 'function bm:p238/a/knockback'), at(170, snd('entity.ender_dragon.growl', 3, 0.6)), at(170, snd('entity.warden.roar', 3, 0.5))] +
             [at(t, 'function bm:p238/c/shake') for t in range(170, 190, 4)] +
             [at(172, f'title {AUD} times 4 50 16'), at(172, title(AUD, 'title', T(L.FIGHT['p2'], COL, bold=True))),
              at(172, title(AUD, 'subtitle', T('six wings - and every eye in them open', '#c8a0a0', italic=True))),
              at('1..168', f'execute as @e[type=minecraft:marker,tag=bm.svlook] at @s positioned as {ME} run tp @s ~ ~9.5 ~'), at('1..168', 'function bm:p238/c/look'),
              at(ENT[1] - 1, 'function bm:p238/turned')])
    turn2 = ([at(1, say(L.FIGHT['turn2'])), at(1, snd('entity.wither.break_block', 2, 0.4)), at(1, 'function bm:p238/pose/broken/stagger'),
              at(1, f'effect give {FIGHT} minecraft:darkness 9 0 true'),
              at(1, title(AUD, 'actionbar', T('Its helm is cracking. Something behind it is looking out.', '#c8a0a0', italic=True)))] +
             beat(10, 100, 12) + [at(12 + 14 * k, f'function bm:p238/c/crack{k}') for k in range(6)] +
             [at(t, snd('block.glass.hit', 2, 0.5 + 0.1 * j)) for j, t in enumerate(range(20, 100, 16))] +
             [at(100, f'particle minecraft:flash{{color:[1.0,0.1,0.15,1.0]}} ~ ~10 ~ 0 0 0 0 1 force {AUD}'), at(100, snd('block.glass.break', 3, 0.3)),
              at(100, snd('entity.warden.sonic_boom', 3, 0.5)), at(100, f'particle minecraft:explosion_emitter ~ ~10 ~ 1 1 1 0 2 force {AUD}'),
              at(100, f'particle minecraft:block{{block_state:"minecraft:black_stained_glass"}} ~ ~10 ~ 2 2 2 0 300 force {AUD}'),
              at(100, 'scoreboard players set @s bm.svph 3'), at(100, 'function bm:p238/pose/true/stagger' if 'stagger' in A.BOSS_POSES['true'] else 'function bm:p238/pose/true/roar'),
              at(100, 'execute as @e[type=minecraft:marker,tag=bm.svlook] at @s run tp @s ~ ~2 ~'), at(100, 'function bm:p238/c/shake'),
              at(120, 'function bm:p238/pose/true/eye_beam_up'), at(120, snd('entity.warden.sonic_charge', 3, 0.4))] +
             [at(120 + 6 * k, f'particle minecraft:dust{{color:[1.0,0.05,0.1],scale:{1.5 + 0.25 * k:.2f}}} ~ ~11.5 ~ {0.2 + 0.1 * k:.1f} {0.2 + 0.1 * k:.1f} {0.2 + 0.1 * k:.1f} 0 30 force {AUD}') for k in range(10)] +
             [at(176, 'function bm:p238/pose/true/roar'), at(176, snd('entity.ender_dragon.growl', 3, 0.4)), at(176, snd('entity.warden.roar', 3, 0.4)),
              at(176, f'particle minecraft:flash{{color:[1.0,0.05,0.1,1.0]}} ~ ~11.5 ~ 0 0 0 0 1 force {AUD}')] +
             [at(t, 'function bm:p238/c/shake') for t in range(176, 196, 4)] +
             [at(178, f'title {AUD} times 4 50 16'), at(178, title(AUD, 'title', T(L.FIGHT['p3'], COL, bold=True))),
              at(178, title(AUD, 'subtitle', T('the great eye opens', '#c8a0a0', italic=True))),
              at(206, title(AUD, 'subtitle', T('THE FLOOR IS GIVING WAY - GET TO THE CENTRE OR AN ISLAND', '#ff8a8a', bold=True))), at(206, title(AUD, 'title', T(' ', COL))),
              at('2..99', f'execute as @e[type=minecraft:marker,tag=bm.svlook] at @s positioned as {ME} run tp @s ~ ~9.5 ~'),
              at('1..200', 'function bm:p238/c/look'),
              at('206..279', 'function bm:p238/a/crack'), at(220, snd('block.deepslate.break', 2, 0.4)), at(250, snd('block.deepslate.break', 2, 0.4)),
              at(280, 'function bm:p238/a/collapse'), at(ENT[2] - 1, 'function bm:p238/turned')])
    fn('p238/turn_tick', ['scoreboard players add @s bm.svt 1',
                          # (by the entrance's own tag: each sets the next form part-way through - by the form, the rest of the
                          #  Broken's entrance ran the True's, floor and all)
                          'execute if entity @s[tag=bm.svt1] run return run function bm:p238/turn1', 'execute if entity @s[tag=bm.svt2] run function bm:p238/turn2'])
    fn('p238/turn1', turn1); fn('p238/turn2', turn2)
    fn('p238/turned', ['tag @s remove bm.svturn', 'tag @s remove bm.svt1', 'tag @s remove bm.svt2', CAMM, 'tag @s add bm.svlive', 'data modify entity @s Invulnerable set value 0b', 'scoreboard players set @s bm.sva 0',
                       'scoreboard players set @s bm.svx 10', 'function bm:p238/fill', 'bossbar set bm:usov color red',
                       f'execute if score @s bm.svph matches 2 run bossbar set bm:usov name {snbt([T(L.SOV, COL, bold=True), T("  -  " + L.FIGHT["p2"], "#c8a0a0")])}',
                       f'execute if score @s bm.svph matches 3 run bossbar set bm:usov name {snbt([T(L.SOV, COL, bold=True), T("  -  " + L.FIGHT["p3"], "#c8a0a0")])}',
                       'execute if score @s bm.svph matches 2 run function bm:p238/eyes/make', 'execute if score @s bm.svph matches 3 run scoreboard players set @s bm.svi 40',
                       'execute if score @s bm.svph matches 3 run data modify entity @s NoGravity set value 1b',
                       f'execute as {AUD} at @s run function bm:p152/tick'])
    fn('p238/a/crack', ['execute if predicate bm:p238/third run ' + f'particle minecraft:dust{{color:[1.0,0.3,0.1],scale:2.0}} {CX} {CY + 1.1} {CZ} 26 0 26 0 60 force {AUD}',
                        f'execute if predicate bm:p238/third run particle minecraft:lava {CX} {CY + 1} {CZ} 24 0 24 0 6 force {AUD}'])
    wjson('bm/predicate/p238/third.json', {'condition': 'minecraft:random_chance', 'chance': 0.34})
    fn('p238/a/collapse', ['execute in minecraft:the_nether run ' + l for l in falls] + [snd('entity.generic.explode', 3, 0.4), snd('block.basalt.break', 3, 0.4),
                                                                                       'function bm:p238/c/shake', f'particle minecraft:large_smoke {CX} {CY} {CZ} 24 1 24 0.05 400 force {AUD}'])
    # (phase III: every 40 s another island falls - at most four)
    for i, cmds in enumerate(islands):
        px, pz = pil[i]
        wx, wy, wz = W(px, AR['floor'][1], pz)
        fn(f'p238/isle/warn{i}', [f'particle minecraft:dust{{color:[1.0,0.3,0.1],scale:2.0}} {wx} {wy + 1.1} {wz} 4 0 4 0 60 force {AUD}',
                                  f'particle minecraft:lava {wx} {wy + 1} {wz} 3 0 3 0 6 force {AUD}', snd('block.deepslate.break', 1.5, 0.5)])
        fn(f'p238/isle/drop{i}', ['execute in minecraft:the_nether run ' + l for l in cmds] + [snd('entity.generic.explode', 2, 0.5), f'scoreboard players set #isf{i} bm.svi 1'])
    fn('p238/isle/sec', ['scoreboard players remove @s bm.svi 1',
                         'execute if score @s bm.svi matches 1..5 run function bm:p238/isle/warn', 'execute if score @s bm.svi matches 0 run function bm:p238/isle/drop',
                         'execute if score @s bm.svi matches 0 run scoreboard players set @s bm.svi 40'])
    fn('p238/isle/pick', ['scoreboard players set #isn bm.svi 0'] + [f'execute if score #isf{i} bm.svi matches 1 run scoreboard players add #isn bm.svi 1' for i in range(len(pil))] +
       ['execute if score #isn bm.svi matches 4.. run return run scoreboard players set #isp bm.svi -1',
        f'execute store result score #isp bm.svi run random value 0..{len(pil) - 1}'] +
       [f'execute if score #isp bm.svi matches {i} if score #isf{i} bm.svi matches 1 run scoreboard players set #isp bm.svi {(i + 1) % len(pil)}' for i in range(len(pil))] +
       [f'execute if score #isp bm.svi matches {i} if score #isf{i} bm.svi matches 1 run scoreboard players set #isp bm.svi -1' for i in range(len(pil))])
    fn('p238/isle/warn', ['execute if score @s bm.svi matches 5 run function bm:p238/isle/pick'] +
       [f'execute if score #isp bm.svi matches {i} run function bm:p238/isle/warn{i}' for i in range(len(pil))] +
       ['execute if score #isp bm.svi matches 0.. run ' + title(AUD, 'actionbar', T('An island is cracking!', '#ff8a8a', bold=True))])
    fn('p238/isle/drop', [f'execute if score #isp bm.svi matches {i} run function bm:p238/isle/drop{i}' for i in range(len(pil))])
    G.FUNCS['p237/floor'] += [f'scoreboard players reset #isf{i} bm.svi' for i in range(len(pil))]

    # ================================================================== THE ATTACKS
    S, M = '@s', ME
    fn('p238/a/stomp', ['playsound minecraft:entity.iron_golem.step hostile @a[distance=..40] ~ ~ ~ 2 0.4',
                        'particle minecraft:block{block_state:"minecraft:blackstone"} ~ ~0.2 ~ 1.5 0.1 1.5 0 20 force'])
    fn('p238/a/knights', ['execute store result score #kn bm.rng if entity @e[tag=bm.svk]', 'execute if score #kn bm.rng matches 7.. run return 0',
                          'playsound minecraft:entity.evoker.prepare_summon hostile @a[distance=..64] ~ ~ ~ 2 0.5',
                          'execute at @e[type=minecraft:marker,tag=bm.mspawn,tag=bm.d_under,distance=..48,sort=random,limit=3] run function bm:p238/a/knight'])
    # (2.99a) the Mires: two at most at a time, risen at once from the hall's spawn points (phase246's spawn and rise)
    fn('p238/a/mires', [f'execute as {TGT} if items entity @s armor.* *[minecraft:custom_data~{{bm_angel:1b}}] at @s run return run function bm:p238/a/mires_fail',
                        'execute store result score #kn bm.rng if entity @e[type=minecraft:husk,tag=bm.svm]', 'execute if score #kn bm.rng matches 2.. run return 0',
                        'playsound minecraft:entity.warden.emerge hostile @a[distance=..64] ~ ~ ~ 2 0.6',
                        'execute at @e[type=minecraft:marker,tag=bm.mspawn,tag=bm.d_under,distance=..48,sort=random,limit=1] run function bm:p238/a/mire'])
    fn('p238/a/mires_fail', ['particle minecraft:end_rod ~ ~1 ~ 0.6 1 0.6 0.08 30', 'playsound minecraft:block.beacon.deactivate hostile @a[distance=..48] ~ ~ ~ 1.5 0.6',
                             'execute at @e[type=minecraft:marker,tag=bm.mspawn,tag=bm.d_under,distance=..48,sort=random,limit=2] run particle minecraft:squid_ink ~ ~0.3 ~ 0.8 0.1 0.8 0.05 20',
                             title('@s', 'actionbar', T('The Mires try to rise - and shrink from your holy armour.', '#ffe08a', bold=True))])
    fn('p238/a/mire', ['function bm:p246/spawn', 'execute as @e[type=minecraft:husk,tag=bm.mire,distance=..1,limit=1] at @s run function bm:p238/a/mire_up'])
    fn('p238/a/mire_up', ['tag @s add bm.svm', 'tag @s add bm.muc', 'function bm:p246/rise0'])
    fn('p238/a/knight', ['particle minecraft:large_smoke ~ ~1 ~ 0.4 0.8 0.4 0.03 20 force', 'particle minecraft:sculk_soul ~ ~1 ~ 0.4 0.8 0.4 0.03 10 force',
                         f'summon minecraft:wither_skeleton ~ ~ ~ {{Tags:["bm.seen","bm.dgmob","bm.svk","bm.udread","bm.udk_wither_skeleton"],PersistenceRequired:1b,'
                         f'CustomName:{snbt(T("Dread Knight", COL))},equipment:{{mainhand:{{id:"minecraft:netherite_sword",count:1}}}},drop_chances:{{mainhand:0.0f}}}}'])
    # -- the slam: a shockwave rolls out along the floor (jump it)
    fn('p238/a/slam', ['summon minecraft:marker ~ ~0.2 ~ {Tags:["bm.svfx","bm.svring"]}', 'playsound minecraft:entity.generic.explode hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                       'particle minecraft:explosion_emitter ^ ^ ^5 0 0 0 0 1 force', 'function bm:p238/c/shake'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.svring] at @s run function bm:p238/ring/tick')
    fn('p238/ring/tick', ['scoreboard players add @s bm.svt 1'] + [f'execute if score @s bm.svt matches {k} run function bm:p238/ring/r{k}' for k in range(1, 41)] +
       ['execute if score @s bm.svt matches 41.. run kill @s'])
    wjson('bm/predicate/p238/ground.json', {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:flags': {'is_on_ground': True}}})
    for k in range(1, 41):
        r_ = k * 0.55
        fn(f'p238/ring/r{k}', [f'particle minecraft:dust{{color:[0.85,0.12,0.18],scale:2.4}} ~{x} ~ ~{z} 0.1 0.05 0.1 0 1 force' for x, z in ring_pts(r_, max(8, int(4 * r_)))] +
           [f'execute as @a[distance={max(0, r_ - 0.8):.2f}..{r_ + 0.8:.2f},gamemode=!spectator,gamemode=!creative] if predicate bm:p238/ground at @s run function bm:p238/a/ring_hit'])
    fn('p238/a/ring_hit', [f'damage @s 10 minecraft:mob_attack by {M}', 'effect give @s minecraft:slowness 2 2', 'tp @s ~ ~0.4 ~'])
    # -- the sweep: a wide arc in front (a pillar between you and it is the only cover)
    fn('p238/a/sweep', ['playsound minecraft:entity.player.attack.sweep hostile @a[distance=..40] ~ ~ ~ 2 0.4', 'playsound minecraft:entity.wither.shoot hostile @a[distance=..40] ~ ~ ~ 1 0.5',
                        'execute rotated ~ 0 positioned ^ ^1.5 ^6 run particle minecraft:sweep_attack ~ ~ ~ 5 0.5 3 0 30 force',
                        f'execute rotated ~ 0 positioned ^ ^ ^6 as @a[distance=..7.5,gamemode=!spectator,gamemode=!creative] at @s run function bm:p238/a/sweep_one'])
    fn('p238/a/sweep_one', ['scoreboard players set #cov bm.rng 0', f'execute at {M} positioned ~ ~3 ~ facing entity @s eyes run function bm:p238/cov/start',
                            f'execute if score #cov bm.rng matches 0 run damage @s 14 minecraft:mob_attack by {M}'])
    # (cover: a ray from it to you - anything solid on the way and you're safe)
    fn('p238/cov/start', ['scoreboard players set #cr bm.rng 48', 'function bm:p238/cov/ray'])
    fn('p238/cov/ray', ['execute unless block ~ ~ ~ #bm:grap_pass run return run scoreboard players set #cov bm.rng 1',
                        'execute if entity @s[distance=..1.2] run return 0', 'scoreboard players remove #cr bm.rng 1',
                        'execute if score #cr bm.rng matches 1.. positioned ^ ^ ^0.8 run function bm:p238/cov/ray'])
    # -- the lunge and the stab
    fn('p238/a/lunge', ['execute rotated ~ 0 if block ^ ^1 ^2 #bm:grap_pass if block ^ ^2 ^2 #bm:grap_pass run tp @s ^ ^ ^0.8',
                        'particle minecraft:large_smoke ~ ~1 ~ 0.6 0.4 0.6 0.01 4 force'])
    fn('p238/a/stab', ['playsound minecraft:item.trident.throw hostile @a[distance=..40] ~ ~ ~ 2 0.4', 'execute rotated ~ 0 positioned ^ ^2 ^5 run particle minecraft:crit ~ ~ ~ 1 1 3 0.3 40 force',
                       f'execute rotated ~ 0 positioned ^ ^ ^4 as @a[distance=..4,gamemode=!spectator,gamemode=!creative] run damage @s 16 minecraft:mob_attack by {M}'])
    # -- the chain: someone far is dragged in
    fn('p238/a/chain', [f'execute as {FIGHT[:-1]},distance=9..34,sort=random,limit=1] run tag @s add bm.svchained',
                        'playsound minecraft:block.chain.break hostile @a[distance=..48] ~ ~ ~ 2 0.5', 'scoreboard players set #chn bm.rng 16'])
    tick.append('execute if score #chn bm.rng matches 1.. run function bm:p238/a/chain_tick')
    fn('p238/a/chain_tick', ['scoreboard players remove #chn bm.rng 1',
                             f'execute as @a[tag=bm.svchained] at @s if entity @e[type=minecraft:husk,tag=bm.usov,distance=6..,limit=1] facing entity {M} feet rotated ~ 0 if block ^ ^ ^0.8 #bm:grap_pass if block ^ ^1 ^0.8 #bm:grap_pass run tp @s ^ ^ ^0.8',
                             f'execute as @a[tag=bm.svchained] at @s facing entity {M} feet run particle minecraft:block{{block_state:"minecraft:iron_chain"}} ^ ^1 ^1 0.1 0.1 0.1 0 4 force',
                             f'execute if score #chn bm.rng matches 0 as @a[tag=bm.svchained] run damage @s 6 minecraft:mob_attack by {M}',
                             'execute if score #chn bm.rng matches 0 run tag @a remove bm.svchained'])
    # -- the knockback roar (the first turn)
    fn('p238/a/knockback', [f'execute as {FIGHT[:-1]},distance=..24] run damage @s 4 minecraft:mob_attack by {M}'])
    # -- the heart pulse: rings of withering - stand between them
    bands = (6, 12, 18, 24)
    for b_ in bands:
        fn(f'p238/a/band_warn{b_}', [f'particle minecraft:dust{{color:[0.35,0.05,0.4],scale:2.0}} ~{x} ~0.2 ~{z} 0.3 0 0.3 0 1 force' for x, z in ring_pts(b_, int(5 * b_))])
        fn(f'p238/a/band{b_}', [f'particle minecraft:dust{{color:[0.1,0.0,0.1],scale:3.0}} ~{x} ~0.5 ~{z} 0.4 0.4 0.4 0 2 force' for x, z in ring_pts(b_, int(5 * b_))] +
           [f'execute as @a[distance={b_ - 1.6}..{b_ + 1.6},gamemode=!spectator,gamemode=!creative] run function bm:p238/a/band_hit'])
    fn('p238/a/band_hit', [f'damage @s 9 minecraft:magic by {M}', 'effect give @s minecraft:wither 4 1'])
    fn('p238/a/pulse_warn', [f'execute at @s run function bm:p238/a/band_warn{b_}' for b_ in bands] + ['playsound minecraft:entity.warden.heartbeat hostile @a[distance=..48] ~ ~ ~ 3 0.5',
                                                                                                    title(AUD, 'actionbar', T('Its heart beats - stand BETWEEN the rings!', '#c080ff', bold=True))])
    fn('p238/a/pulse', [f'execute at @s run function bm:p238/a/band{b_}' for b_ in bands] + ['playsound minecraft:entity.warden.sonic_boom hostile @a[distance=..48] ~ ~ ~ 2 0.5'])
    # -- the wing gust: everyone in front pushed back
    fn('p238/a/gust', ['execute if score @s bm.svx matches 30 run playsound minecraft:entity.ender_dragon.flap hostile @a[distance=..48] ~ ~ ~ 3 0.4',
                       'execute rotated ~ 0 positioned ^ ^2 ^8 run particle minecraft:cloud ~ ~ ~ 4 2 4 0.2 20 force',
                       f'execute rotated ~ 0 positioned ^ ^ ^10 as @a[distance=..14,gamemode=!spectator,gamemode=!creative] at @s facing entity {M} feet rotated ~ 0 '
                       'if block ^ ^ ^-0.45 #bm:grap_pass if block ^ ^1 ^-0.45 #bm:grap_pass run tp @s ^ ^ ^-0.45'])
    # -- its three's moves
    fn('p238/a/dread', ['execute store result score #dm bm.rng run random value 1..3', 'execute if score #dm bm.rng matches 1 run function bm:p238/a/ice',
                        'execute if score #dm bm.rng matches 2 run function bm:p238/a/curse', 'execute if score #dm bm.rng matches 3 run function bm:p238/a/whirl'])
    fn('p238/a/ice', [say(L.FIGHT['echo_snow']), 'playsound minecraft:block.glass.break hostile @a[distance=..48] ~ ~ ~ 2 0.5',
                      f'execute as {FIGHT} at @s run function bm:p238/a/ice_one'])
    fn('p238/a/ice_one', ['scoreboard players set #cov bm.rng 0', f'execute at {M} positioned ~ ~6 ~ facing entity @s eyes run function bm:p238/cov/start',
                          f'execute at {M} positioned ~ ~6 ~ facing entity @s eyes run particle minecraft:snowflake ^ ^ ^4 0.5 0.5 0.5 0.3 30 force',
                          f'execute if score #cov bm.rng matches 0 run damage @s 6 minecraft:freeze by {M}', 'execute if score #cov bm.rng matches 0 run effect give @s minecraft:slowness 4 1',
                          'execute if score #cov bm.rng matches 0 run data modify entity @s TicksFrozen set value 200'])
    fn('p238/a/curse', [say(L.FIGHT['echo_witch']), f'execute as {FIGHT} at @s run summon minecraft:marker ~ ~0.1 ~ {{Tags:["bm.svfx","bm.svcurse"]}}'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.svcurse] at @s run function bm:p238/a/curse_tick')
    fn('p238/a/curse_tick', ['scoreboard players add @s bm.svt 1'] +
       [f'execute if score @s bm.svt matches ..27 run particle minecraft:dust{{color:[0.48,1.0,0.35],scale:1.4}} ~{x} ~ ~{z} 0 0 0 0 1 force' for x, z in ring_pts(2.4, 10)] +
       ['execute if score @s bm.svt matches 28.. run function bm:p238/a/curse_burst'])
    fn('p238/a/curse_burst', ['particle minecraft:witch ~ ~0.6 ~ 1.4 0.6 1.4 0.2 60 force', 'playsound minecraft:entity.evoker_fangs.attack hostile @a[distance=..24] ~ ~ ~ 1 0.6',
                              f'execute as @a[distance=..2.5,gamemode=!spectator,gamemode=!creative] run damage @s 12 minecraft:magic by {M}', 'kill @s'])
    fn('p238/a/whirl', [say(L.FIGHT['echo_shark']), 'scoreboard players set #whl bm.rng 60', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..48] ~ ~ ~ 2 0.5'])
    tick.append(f'execute if score #whl bm.rng matches 1.. as {ME} at @s run function bm:p238/a/whirl_tick')
    fn('p238/a/whirl_tick', ['scoreboard players remove #whl bm.rng 1', 'particle minecraft:soul ~ ~0.5 ~ 6 0.2 6 0.05 20 force',
                             f'execute as {FIGHT[:-1]},distance=4..20] at @s facing entity {M} feet rotated ~ 0 if block ^0.2 ^ ^0.22 #bm:grap_pass if block ^0.2 ^1 ^0.22 #bm:grap_pass run tp @s ^0.2 ^ ^0.22',
                             f'execute if score #whl bm.rng matches 0 as {FIGHT[:-1]},distance=..5] run damage @s 12 minecraft:mob_attack by {M}'])
    # -- the wing-eye bolts (homing)
    fn('p238/a/bolts', ['playsound minecraft:entity.blaze.shoot hostile @a[distance=..48] ~ ~ ~ 2 0.5'] +
       [f'execute rotated ~ 0 positioned ^{x} ^{y} ^-1 run summon minecraft:marker ~ ~ ~ {{Tags:["bm.svfx","bm.svbolt"]}}' for x, y in ((5, 9), (-5, 9), (7, 6), (-7, 6))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.svbolt] at @s run function bm:p238/a/bolt')
    fn('p238/a/bolt', ['scoreboard players add @s bm.svt 1', 'execute if score @s bm.svt matches 70.. run return run kill @s',
                       f'execute facing entity {FIGHT[:-1]},sort=nearest,limit=1] eyes run tp @s ^ ^ ^0.55 ~ ~',
                       'particle minecraft:dust{color:[0.95,0.12,0.2],scale:1.6} ~ ~ ~ 0.05 0.05 0.05 0 3 force', 'particle minecraft:sculk_soul ~ ~ ~ 0 0 0 0 1 force',
                       'execute unless block ~ ~ ~ #bm:grap_pass run return run kill @s',
                       f'execute positioned ~ ~-1 ~ as @a[distance=..1.1,gamemode=!spectator,gamemode=!creative] at @s run function bm:p238/a/bolt_hit',
                       f'execute as @a[distance=..1.1,gamemode=!spectator,gamemode=!creative] at @s run function bm:p238/a/bolt_hit'])
    fn('p238/a/bolt_hit', [f'damage @s 6 minecraft:magic by {M}', 'effect give @s minecraft:wither 3 0',
                           'execute as @e[type=minecraft:marker,tag=bm.svbolt,distance=..2.5,limit=1,sort=nearest] run kill @s'])
    # -- phase III: the eye beam (cover - or the Dawnshard - is all that stops it)
    fn('p238/a/beam_start', ['kill @e[type=minecraft:marker,tag=bm.svbeam]', f'execute positioned ~ ~11 ~ facing entity {TGT} feet rotated ~-50 ~ run summon minecraft:marker ~ ~ ~ {{Tags:["bm.svfx","bm.svbeam"]}}',
                             'playsound minecraft:entity.warden.sonic_charge hostile @a[distance=..64] ~ ~ ~ 3 0.4', 'playsound minecraft:entity.guardian.attack hostile @a[distance=..64] ~ ~ ~ 3 0.5',
                             title(AUD, 'actionbar', T('THE EYE OPENS - get something solid between you and it!', COL, bold=True))])
    fn('p238/a/beam', ['execute as @e[type=minecraft:marker,tag=bm.svbeam] at @s run function bm:p238/beam/step', 'execute if score @s bm.svx matches 5 run kill @e[type=minecraft:marker,tag=bm.svbeam]'])
    fn('p238/beam/step', ['tp @s ~ ~ ~ ~2.5 ~', 'scoreboard players set #br bm.rng 56', 'execute rotated as @s run function bm:p238/beam/ray'])
    fn('p238/beam/ray', ['particle minecraft:dust{color:[1.0,0.1,0.12],scale:2.2} ~ ~ ~ 0.05 0.05 0.05 0 1 force',
                         'execute unless block ~ ~ ~ #bm:grap_pass run return run particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0 2 force',
                         'execute as @a[distance=..1.5,gamemode=!spectator,gamemode=!creative] at @s run function bm:p238/beam/hit',
                         'scoreboard players remove #br bm.rng 1', 'execute if score #br bm.rng matches 1.. positioned ^ ^ ^0.8 run function bm:p238/beam/ray'])
    fn('p238/beam/hit', ['execute if items entity @s weapon.* *[minecraft:custom_data~{bm:"dawnshard"}] run return run function bm:p238/beam/shield',
                         f'damage @s 9 minecraft:magic by {M}', 'data modify entity @s Fire set value 60s'])
    fn('p238/beam/shield', ['particle minecraft:end_rod ~ ~1.2 ~ 0.6 0.6 0.6 0.05 12 force', 'playsound minecraft:block.beacon.power_select player @a[distance=..16] ~ ~ ~ 0.8 1.6',
                            title('@s', 'actionbar', T('The Dawnshard turns the beam. Light holds.', L.HOLY, bold=True))])
    fn('p238/a/roots', [f'execute as {FIGHT} at @s run summon minecraft:marker ~ ~0.1 ~ {{Tags:["bm.svfx","bm.svroot"]}}', 'playsound minecraft:block.sculk_vein.place hostile @a[distance=..48] ~ ~ ~ 2 0.4',
                        title(AUD, 'actionbar', T('The void reaches up - step OFF the roots!', '#c080ff', bold=True))])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.svroot] at @s run particle minecraft:sculk_soul ~ ~0.2 ~ 0.6 0 0.6 0 2 force')
    fn('p238/a/roots_snap', ['execute as @e[type=minecraft:marker,tag=bm.svroot] at @s run function bm:p238/a/root_snap'])
    fn('p238/a/root_snap', ['particle minecraft:squid_ink ~ ~0.6 ~ 0.6 0.6 0.6 0.1 30 force', 'playsound minecraft:entity.warden.attack_impact hostile @a[distance=..24] ~ ~ ~ 1 0.5',
                            f'execute as @a[distance=..1.7,gamemode=!spectator,gamemode=!creative] run function bm:p238/a/rooted', 'kill @s'])
    fn('p238/a/rooted', [f'damage @s 7 minecraft:magic by {M}', 'effect give @s minecraft:slowness 3 6', 'effect give @s minecraft:jump_boost 3 200 true'])
    fn('p238/a/dark', [f'effect give {FIGHT} minecraft:darkness 6 0', 'playsound minecraft:entity.warden.nearby_closest hostile @a[distance=..64] ~ ~ ~ 3 0.5', 'function bm:p238/a/knights'])

    # ---- phase II's wing-eyes: six hitboxes that ride its wings; all six shot out and it crashes down
    eyeh = {'Tags': ['bm.sveye', 'bm.boss_part'], 'NoAI': B(1), 'Silent': B(1), 'NoGravity': B(1), 'PersistenceRequired': B(1), 'DeathLootTable': 'minecraft:empty',
            'attributes': [{'id': 'minecraft:max_health', 'base': Dd(24)}, {'id': 'minecraft:scale', 'base': Dd(0.7)}], 'Health': F(24),
            'active_effects': [{'id': 'minecraft:invisibility', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)},
                               {'id': 'minecraft:fire_resistance', 'duration': Int(-1), 'amplifier': B(0), 'show_particles': B(0)}]}
    EYES = [(5.5, 9.5), (-5.5, 9.5), (8, 7), (-8, 7), (6.5, 4.5), (-6.5, 4.5)]
    fn('p238/eyes/make', ['kill @e[type=minecraft:husk,tag=bm.sveye]'] +
       [f'execute rotated ~ 0 positioned ^{x} ^{y} ^-1.5 run summon minecraft:husk ~ ~ ~ {snbt(dict(eyeh, Tags=eyeh["Tags"] + [f"bm.sve{i}"]))}' for i, (x, y) in enumerate(EYES)])
    fn('p238/eyes/ride', [f'execute rotated ~ 0 positioned ^{x} ^{y} ^-1.5 run tp @e[type=minecraft:husk,tag=bm.sve{i}] ~ ~ ~' for i, (x, y) in enumerate(EYES)] +
       [f'execute rotated ~ 0 positioned ^{x} ^{y + 0.5} ^-1.5 if entity @e[type=minecraft:husk,tag=bm.sve{i}] run particle minecraft:dust{{color:[1.0,0.15,0.2],scale:1.4}} ~ ~ ~ 0.2 0.2 0.2 0 2 force'
        for i, (x, y) in enumerate(EYES)] +
       ['execute unless entity @e[type=minecraft:husk,tag=bm.sveye] unless entity @s[tag=bm.svground] run function bm:p238/ground'])
    tick.append(f'execute as {ME} if score @s bm.svph matches 2 if entity @s[tag=bm.svlive] at @s run function bm:p238/eyes/ride')
    fn('p238/ground', ['tag @s add bm.svground', 'effect clear @s minecraft:resistance', 'scoreboard players set @s bm.sva 22', 'scoreboard players set @s bm.svx 160',
                       'playsound minecraft:entity.ender_dragon.hurt hostile @a[distance=..64] ~ ~ ~ 3 0.5', 'playsound minecraft:entity.generic.explode hostile @a[distance=..64] ~ ~ ~ 2 0.5',
                       'function bm:p238/c/shake', title(AUD, 'actionbar', T(L.FIGHT['grounded'], 'gold', bold=True)), 'schedule function bm:p238/unground 160t'])
    fn('p238/unground', [f'execute as {ME} at @s run function bm:p238/unground_me'])
    fn('p238/unground_me', ['tag @s remove bm.svground', f'effect give @s minecraft:resistance infinite {RESIST} true', 'execute if score @s bm.svph matches 2 if entity @s[tag=bm.svlive] run function bm:p238/eyes/make'])
    # ---- phase III's frenzy (a quarter of its last pool left) and its tiring
    fn('p238/frenzy_chk', ['execute unless score @s bm.svph matches 3 run return 0', 'execute if entity @s[tag=bm.svfrz] run return 0', 'execute if score @s bm.svz matches -99..-1 run return 0',
                           'execute if score @s bm.svz matches 1.. run return 0',
                           'scoreboard players operation #q bm.rng = @s bm.svhp', 'scoreboard players set #4 bm.rng 4', 'scoreboard players operation #q bm.rng /= #4 bm.rng',
                           f'scoreboard players add #q bm.rng {FLOOR}', 'execute if score #hp bm.rng <= #q bm.rng run function bm:p238/frenzy'])
    G.FUNCS['p238/tick'].insert(6, 'execute if entity @s[tag=bm.svlive] run function bm:p238/frenzy_chk')
    fn('p238/frenzy', ['tag @s add bm.svfrz', 'scoreboard players set @s bm.svz 12', 'data modify entity @s Invulnerable set value 1b', say(L.FIGHT['frenzy']),
                       'playsound minecraft:entity.warden.roar hostile @a[distance=..64] ~ ~ ~ 3 0.4', 'bossbar set bm:usov color purple'])
    fn('p238/frenzy_sec', ['scoreboard players remove @s bm.svz 1',
                           f'execute if score @s bm.svz matches 1..10 as {FIGHT} at @s run summon minecraft:marker ~ ~0.1 ~ {{Tags:["bm.svfx","bm.svcurse"]}}',
                           title(AUD, 'actionbar', [T('It can\'t be hurt - ', '#ff5a7a', bold=True), T('keep moving!', 'gray')]),
                           'execute if score @s bm.svz matches 0 run function bm:p238/tire'])
    fn('p238/tire', ['scoreboard players set @s bm.svz -8', 'data modify entity @s Invulnerable set value 0b', 'effect clear @s minecraft:resistance',
                     'scoreboard players set @s bm.sva 0', 'scoreboard players set @s bm.svx 160', 'bossbar set bm:usov color red',
                     f'execute as {sel("head")} run data modify entity @s item.components."minecraft:item_model" set value "bm:{A.model_name("head", dict(A.BOSS_POSES["true"]["idle_a"], _face="blink"))}"',
                     'playsound minecraft:entity.ravager.stunned hostile @a[distance=..64] ~ ~ ~ 2 0.6',
                     title(AUD, 'actionbar', [T('The eye shuts - ', 'gold', bold=True), T('strike it now!', 'gray')])])
    second.append(f'execute as {ME} if score @s bm.svz matches -99..-1 run scoreboard players add @s bm.svz 1')
    second.append('execute as @a[scores={bm.svwin=1..},tag=!bm.svmig] run tag @s add bm.svdone')        # (2.98c: who felled it in 2.98 has felled it)
    second.append('tag @a[tag=!bm.svmig] add bm.svmig')

    # ================================================================== THE FALL
    fn('p238/fall', ['tag @s remove bm.svlive', 'tag @s add bm.svfall', 'data modify entity @s Invulnerable set value 1b', 'scoreboard players set @s bm.sva 11',
                     'scoreboard players set @s bm.svx 9999', 'scoreboard players set @s bm.svt 0', 'function bm:p238/clear', 'bossbar set bm:usov value 0',
                     say(L.FIGHT['fall']), 'playsound minecraft:entity.wither.death hostile @a[distance=..96] ~ ~ ~ 1 0.5', f'execute as {AUD} at @s run function bm:p152/tick',
                     'execute at @s run summon minecraft:marker ~ ~12 ~ {Tags:["bm.svlook","bm.svcamm"]}',
                     # (3.0a: nobody stands where it is dragged to, or under where He comes down)
                     f'summon minecraft:marker {CX + 0.5} {CY + 1} {CZ - 5.5} {{Tags:["bm.svkos","bm.svcamm"]}}', f'summon minecraft:marker {CX + 0.5} {CY + 1} {CZ + 13.5} {{Tags:["bm.svkos","bm.svcamm"]}}'])
    # ================================================================== (2.98c) THE LAST LIGHT - the Divine One comes down and ends it
    # 28 s, everyone's eyes held where the story is: the Sovereign dragged into a beam through the dome; HE comes down through
    # it (divine_art: about 26 blocks to His hood), opens His wings, looks down on it, names it - Aurel - raises His hand, and
    # smites; it comes apart into light, the eye last. "Rest now." He rises, and fades. Then the spoils (p238/won).
    import divine_art as DV
    DSC = DV.BOSS_SCALE
    dsel = lambda p: f'@e[type=minecraft:item_display,tag=bm.dvn_{p}]'
    NX, NZ = CX + 0.5, CZ - 5.5                  # (the Sovereign, dragged here)
    DX, DZ = CX + 0.5, CZ + 13.5                 # (He comes down here, facing it - north)
    DY0, DH = CY + 1 + 24, 22                     # (His root starts 24 up; His face is some 22 above His root)
    drig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(DV, p, ["bm.dvn", f"bm.dvn_{p}"], DSC, model=DV.model_name(p, DV.BOSS_POSES["descend"]), extra=dict(view_range=F(12.0), brightness={"block": Int(15), "sky": Int(15)}, teleport_duration=Int(3)))}'
            for p in DV.PARTS]
    fn('p238/dv/place', RF.place(DV, DSC / 16, dsel))
    DVDUR = {'descend': 10, 'reveal': 40, 'gaze': 40, 'raise': 30, 'smite': 6, 'rest': 50, 'ascend': 60}
    for name, pz in DV.BOSS_POSES.items():
        fn(f'p238/dv/pose/{name}', RF.pose(DV, pz, DSC, DVDUR.get(name, 20), dsel, swap=tuple(DV.PARTS)))
    fn('p238/dv/raise', drig + ['execute rotated 180 0 run function bm:p238/dv/place'])
    root = '@e[type=minecraft:marker,tag=bm.dvroot,limit=1]'
    look = '@e[type=minecraft:marker,tag=bm.svlook,limit=1]'
    divine = lambda txt: tellraw(AUD, [T(L.DIVINE_NAME + ': ', L.HOLY, bold=True), T(txt, '#fff8e0')])
    lerp = lambda a, b, u: tuple(a[k] + (b[k] - a[k]) * u for k in range(3))
    SOVH, DVH = (NX, CY + 13, NZ), (DX, CY + 1 + DH, DZ)

    ease = lambda u: u * u * (3 - 2 * u)
    # (3.0a: every camera move a tick at a time, eased in and out - at two ticks a step, the eye moved at 10 fps and jerked)
    def pan(t0, t1, A_, B_, step=1):
        return [at(t, f'tp {look} {x:.2f} {y:.2f} {z:.2f}') for t in range(t0, t1 + 1, step) for (x, y, z) in [lerp(A_, B_, ease((t - t0) / max(1, t1 - t0)))]]
    beam = [f'particle minecraft:end_rod {DX} {CY + 1 + y} {DZ} 0.6 0.4 0.6 0.02 6 force {AUD}' for y in range(2, 50, 3)]
    fn('p238/dv/beam', beam + [f'particle minecraft:end_rod {NX} {CY + 1 + y} {NZ} 0.3 0.4 0.3 0.01 2 force {AUD}' for y in range(2, 50, 4)])
    fn('p238/dv/glow', [f'particle minecraft:end_rod ~ ~ ~ 4 6 4 0.02 12 force {AUD}', f'particle minecraft:dust{{color:[1.0,0.95,0.75],scale:2.5}} ~ ~ ~ 4 6 4 0 10 force {AUD}'])
    fn('p238/dv/unmake', [f'particle minecraft:end_rod {NX} {CY + 7} {NZ} 3 5 3 0.08 30 force {AUD}', f'particle minecraft:white_ash {NX} {CY + 7} {NZ} 3 5 3 0 60 force {AUD}',
                          f'particle minecraft:dust{{color:[1.0,1.0,0.9],scale:3.0}} {NX} {CY + 7} {NZ} 3 5 3 0 20 force {AUD}'])
    # ---- (3.0d) THE BURNING: timed to the smiting (t320) and the old unmaking's window (t330-410, its music's swell and fall)
    import phase257 as DFX
    import rigkit as RK
    DPZ = A.BOSS_POSES['true']['death_2']                            # (its pose from t240 on: the fall's frames, state 31)
    SCT = SCALE['true']; UT = SCT / 16
    CEN = DFX.part_centres(A, DPZ, SCT)
    XF = RK.solve(A.PIVOT, A.PARENT, DPZ)
    BURN = [(('shinr', 'shinl'), 322, 338, 346), (('legr', 'legl'), 326, 342, 350), (('weapon',), 328, 344, 350), (('forer', 'forel'), 330, 348, 356),
            (('w3r', 'w3l'), 332, 350, 358), (('armr', 'arml'), 334, 354, 362), (('w2r', 'w2l'), 336, 356, 364), (('body',), 338, 360, 368),
            (('w1r', 'w1l'), 340, 362, 370), (('chest',), 344, 366, 376), (('head', 'fx'), 348, 380, 392)]
    BRS = {'shin': 1.6, 'leg': 1.9, 'weapon': 1.8, 'fore': 1.6, 'arm': 1.8, 'w': 2.2, 'body': 2.6, 'chest': 2.8, 'head': 2.4, 'fx': 1.2}
    bsz = lambda p: next(v for k, v in BRS.items() if p.startswith(k))
    psel = lambda p: f'@e[type=minecraft:item_display,tag=bm.svr_{p}]'
    burn = []
    for parts, t_on, t_char, t_fall in BURN:
        for p in parts:
            if p not in CEN: continue
            c = CEN[p]; z = bsz(p)
            burn += [at(t_on, f'execute as {psel(p)} run data merge entity @s {{brightness:{{block:15,sky:15}}}}'),
                     at(t_on, DFX.at_part(c, DFX.spr('hflame', z * 1.3, z * 0.4))), at(t_on, DFX.at_part(c, DFX.spr('hflame', z, z * 0.5))),
                     at(t_on, DFX.at_part(c, f'particle minecraft:flash{{color:[1.0,0.95,0.7,1.0]}} ~ ~ ~ 0 0 0 0 1 force {AUD}'))]
            burn += [at(t, DFX.at_part(c, DFX.spr('hflame', z, z * 0.5))) for t in range(t_on + 4, t_fall + 4, 4)]
            burn += [at(t, DFX.at_part(c, DFX.spr('ember', z * 0.8, z * 0.4))) for t in range(t_on + 6, t_fall, 8)]
            burn += [at(t_char, f'execute as {psel(p)} run data merge entity @s {{brightness:{{block:1,sky:1}}}}'),
                     at(t_char, DFX.at_part(c, f'particle minecraft:large_smoke ~ ~ ~ 0.6 0.6 0.6 0.04 10 force {AUD}'))]
            q, t = XF[p]; k = getattr(A, 'PART_K', {}).get(p, 1.0)
            tr = f'[{t[0] * UT:.3f}f,{t[1] * UT - 1.6:.3f}f,{t[2] * UT:.3f}f]'
            burn += [at(t_fall, f'execute as {psel(p)} run data merge entity @s {{start_interpolation:0,interpolation_duration:14,transformation:{{translation:{tr},scale:[0f,0f,0f]}}}}'),
                     at(t_fall, DFX.at_part(c, DFX.spr('ash', z * 0.9, z * 0.6))), at(t_fall, DFX.at_part(c, DFX.spr('ash', z * 0.7, z * 0.6))),
                     at(t_fall, DFX.at_part(c, DFX.spr('ash', z * 0.8, z * 0.6))),
                     at(t_fall, DFX.at_part(c, f'particle minecraft:white_ash ~ ~ ~ 0.8 0.8 0.8 0.02 40 force {AUD}')),
                     at(t_fall, DFX.at_part(c, f'particle minecraft:end_rod ~ ~ ~ 0.4 0.4 0.4 0.08 6 force {AUD}'))]
        burn += [at(t_on, snd('item.firecharge.use', 2.5, 0.6)), at(t_on, snd('block.fire.ambient', 3, 0.7)),
                 at(t_char, snd('block.fire.extinguish', 1.2, 0.5)), at(t_fall, snd('block.basalt.break', 2.5, 0.5)), at(t_fall, snd('entity.blaze.death', 0.8, 0.5))]
    burn += [at(322, snd('entity.blaze.shoot', 3, 0.5)), at(322, snd('block.beacon.power_select', 3, 1.2)),
             at(322, title(AUD, 'actionbar', T(L.DIVINE.get('burn', 'His light takes it - and it burns, white and gold.'), L.HOLY, italic=True))),
             at('324..390', f'particle minecraft:dust{{color:[1.0,0.9,0.55],scale:2.2}} {NX} {CY + 6} {NZ} 2.5 4 2.5 0 6 force {AUD}'),
             at('324..390', f'particle minecraft:flame {NX} {CY + 3} {NZ} 2 3 2 0.02 3 force {AUD}'),
             at(381, snd('entity.warden.sonic_charge', 2.5, 1.6)),
             # (the eye, last: a last white flash, and nothing left)
             at(394, f'particle minecraft:flash{{color:[1.0,1.0,0.92,1.0]}} {NX} {CY + 12} {NZ} 0 0 0 0 1 force {AUD}'),
             at(394, f'particle minecraft:end_rod {NX} {CY + 10} {NZ} 1.5 2 1.5 0.25 80 force {AUD}'),
             at(394, f'execute positioned {NX} {CY + 11} {NZ} run ' + DFX.ring('nova', 1.6, 16)),
             at(394, snd('block.bell.resonate', 3, 0.7)), at(394, snd('block.beacon.deactivate', 3, 0.7)), at(394, snd('entity.generic.explode', 1.5, 0.7))]
    burn += [at(t, f'execute positioned {NX} {CY + 9} {NZ} run ' + DFX.spr('feather', 1.6, 3.5)) for t in range(396, 470, 3)]
    burn += [at(t, f'execute positioned {NX} {CY + 3} {NZ} run ' + DFX.spr('ash', 1.4, 3.0)) for t in range(396, 460, 5)]
    burn += [at(t, snd('block.amethyst_block.chime', 1.5, 0.9 + 0.1 * (k % 4))) for k, t in enumerate(range(400, 470, 14))]
    seq = ([at(1, f'execute as {AUD} at @s run stopsound @s record'), at(2, f'execute as {AUD} at @s run playsound bm:music.boss_divine record @s ~ ~ ~ 1000 1 1'),
            at(1, f'effect give {FIGHT} minecraft:darkness 3 0 true')] +
           # (the light takes it: dragged into the beam, turned to face where He will stand)
           [at('20..69', f'execute unless entity @s[x={NX - 0.8},y={CY - 4},z={NZ - 0.8},dx=1.6,dy=30,dz=1.6] facing {NX} ~ {NZ} run tp @s ^ ^ ^0.45'),
            at(20, title(AUD, 'actionbar', T(L.DIVINE['pulled'], L.HOLY, italic=True))), at(70, f'tp @s {NX} ~ {NZ} facing {DX} ~ {DZ}'),
            at('1..69', f'execute as {look} positioned as @e[type=minecraft:husk,tag=bm.usov,limit=1] run tp @s ~ ~12 ~')] +
           [at(40, f'particle minecraft:flash{{color:[1.0,0.97,0.85,1.0]}} {DX} {CY + 30} {DZ} 0 0 0 0 1 force {AUD}'), at(40, snd('block.beacon.activate', 3, 0.6)),
            at(40, snd('block.bell.resonate', 3, 0.5)), at('40..470', 'function bm:p238/dv/beam')] +
           # (HE comes down)
           [at(58, f'summon minecraft:marker {DX} {DY0} {DZ} {{Tags:["bm.dvroot"]}}'), at(60, f'execute positioned {DX} {DY0} {DZ} run function bm:p238/dv/raise'), at(61, 'function bm:p238/dv/pose/descend'),
            at(60, f'particle minecraft:flash{{color:[1.0,0.97,0.85,1.0]}} {DX} {DY0 + 10} {DZ} 0 0 0 0 1 force {AUD}'), at(60, snd('entity.player.levelup', 2, 0.5))] +
           [at(t, f'tp {root} {DX} {DY0 - 24 * ease((t - 60) / 100):.2f} {DZ}') for t in range(60, 161)] +
           [at('60..548', f'execute as {root} at @s rotated 180 0 run function bm:p238/dv/place'), at('60..520', f'execute at {root} positioned ~ ~12 ~ run function bm:p238/dv/glow')] +
           pan(70, 101, SOVH, (DX, DY0 - 24 * ease(41 / 100) + DH, DZ)) +
           [at(t, f'tp {look} {DX} {DY0 - 24 * ease((t - 60) / 100) + DH:.2f} {DZ}') for t in range(102, 161)] +
           [at(160, 'function bm:p238/dv/pose/reveal'), at(160, f'particle minecraft:flash{{color:[1.0,0.97,0.85,1.0]}} {DX} {CY + 20} {DZ} 0 0 0 0 1 force {AUD}'),
            at(160, snd('block.beacon.power_select', 3, 0.5)), at(160, snd('entity.ender_dragon.flap', 3, 0.5)),
            at(162, f'title {AUD} times 10 80 20'), at(162, title(AUD, 'title', T(L.DIVINE['title'], L.HOLY, bold=True))),
            at(162, title(AUD, 'subtitle', T(L.DIVINE['sub'], '#fff8e0', italic=True)))] +
           # (He looks down on it; it speaks; He names it)
           [at(200, 'function bm:p238/dv/pose/gaze'), at(200, 'scoreboard players set @s bm.sva 31'), at(204, say(L.DIVINE['sov1']))] +
           pan(206, 222, DVH, SOVH) + pan(244, 252, SOVH, DVH) +
           [at(250, divine(L.DIVINE['name'])), at(250, snd('block.bell.use', 3, 0.5)), at(270, say(L.DIVINE['sov2']))] +
           # (His hand rises; the light gathers; THE SMITING)
           [at(290, 'function bm:p238/dv/pose/raise'), at(290, title(AUD, 'actionbar', T(L.DIVINE['raise'], L.HOLY, italic=True))),
            at(290, snd('block.beacon.ambient', 3, 0.5)), at(300, snd('entity.warden.sonic_charge', 2, 1.4))] +
           pan(290, 300, DVH, (DX, DVH[1] + 6, DZ)) +
           [at(320, 'function bm:p238/dv/pose/smite'), at(320, f'particle minecraft:flash{{color:[1.0,1.0,0.95,1.0]}} {NX} {CY + 8} {NZ} 0 0 0 0 1 force {AUD}'),
            at(320, snd('item.trident.thunder', 3, 0.6)), at(320, snd('entity.generic.explode', 2, 0.5)), at(320, snd('block.beacon.deactivate', 3, 0.5)),
            at(320, f'particle minecraft:explosion_emitter {NX} {CY + 6} {NZ} 2 3 2 0 4 force {AUD}'), at(320, 'function bm:p238/c/shake'), at(326, 'function bm:p238/c/shake')] +
           pan(316, 324, (DX, DVH[1] + 6, DZ), (NX, CY + 7, NZ)) +
           # (it comes apart into light; the eye last)
           # (3.0d: IT BURNS UP IN HOLY FIRE - p238/burn: white-gold flames climb it from its feet, each part white-hot, then charred
           #  black, then crumbling away into ash; the eye last; a last flash, and only ash and feathers of light drifting)
           burn +
           [at('330..410', 'function bm:p238/dv/unmake'), at(340, snd('entity.warden.death', 2, 0.6)), at(372, snd('block.amethyst_block.break', 3, 0.5)),
            at(400, title(AUD, 'actionbar', T(L.DIVINE['end'], L.HOLY, italic=True))), at(412, 'function bm:p238/dv/pose/rest')] +
           pan(414, 430, (NX, CY + 7, NZ), DVH) +
           [at(430, divine(L.DIVINE['rest'])), at(460, divine(L.DIVINE['you']))] +
           # (He rises, and fades)
           [at(480, 'function bm:p238/dv/pose/ascend')] +
           [at(t, f'tp {root} {DX} {CY + 1 + 26 * ease((t - 480) / 68):.2f} {DZ}') for t in range(481, 549)] +
           [at(t, f'tp {look} {DX} {CY + 1 + 26 * ease((t - 480) / 68) + DH:.2f} {DZ}') for t in range(481, 549)] +
           [at(520, 'execute as @e[type=minecraft:item_display,tag=bm.dvn] run data merge entity @s {start_interpolation:0,interpolation_duration:28,transformation:{scale:[0f,0f,0f]}}'),
            at(520, f'particle minecraft:end_rod {DX} {CY + 30} {DZ} 4 8 4 0.05 200 force {AUD}'), at(548, f'particle minecraft:flash{{color:[1.0,0.97,0.85,1.0]}} {DX} {CY + 40} {DZ} 0 0 0 0 1 force {AUD}'),
            at(549, 'kill @e[type=minecraft:item_display,tag=bm.dvn]'), at(549, f'kill {root}'), at(549, CAMM),
            at('1..548', 'function bm:p238/c/look'), at(550, 'function bm:p238/won')])
    fn('p238/falling', ['scoreboard players add @s bm.svt 1'] + seq)
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[tag=bm.dvn]', 'kill @e[tag=bm.dvroot]']
    G.wjson('bm/advancement/story/sovereign.json', {'parent': 'bm:story/root', 'criteria': {'won': {'trigger': 'minecraft:impossible'}},
                                                    'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': 'bm:sov_eye'}},
                                                                'title': T('The Last Light', 'yellow'), 'description': T('Fell the Dread Sovereign at the bottom of the Undercrown', 'gray'),
                                                                'frame': 'challenge'}})
    lt, uni = G.loot_entry, G.uni
    G.wjson('bm/loot_table/p238/spoils.json', {'type': 'minecraft:chest', 'pools': [
        {'rolls': 1, 'entries': [lt('dread_token', uni(12, 20))]},
        {'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:netherite_ingot', 'functions': [{'function': 'minecraft:set_count', 'count': uni(2, 4)}]}]},
        {'rolls': 1, 'entries': [lt(i) for i in ('sov_edge', 'black_crown', 'sov_heart')]},
        {'rolls': 1, 'entries': [lt('dread_essence', uni(4, 8))]}]})
    fn('p238/won', [tellraw('@a', [T('☠ ', COL), {'selector': FIGHT}, T(' felled ', 'gray'), T(L.SOV, COL, bold=True), T(' at the bottom of the Undercrown.', 'gray')]),
                    'scoreboard players set #uowed bm.p2 0', f'execute as {FIGHT} at @s run function bm:p238/reward', CAMM,
                    'particle minecraft:explosion_emitter ~ ~6 ~ 2 3 2 0 4 force', 'function bm:p238/c/door_open',
                    'function bm:p237/nights_end', 'function bm:p237/collapse', 'function bm:p237/floor',
                    f'particle minecraft:reverse_portal {CX} {CY + 1} {CZ} 24 0.5 24 0.1 400 force {AUD}',
                    title(AUD, 'actionbar', T('The floor knits itself back together over the lava.', '#c8a0a0', italic=True)), 'bossbar set bm:usov visible false',
                    'kill @e[type=minecraft:item_display,tag=bm.svr]', 'tp @s ~ -400 ~', 'kill @s'])
    fn('p238/reward', ['tag @s add bm.dfin', 'tag @s add bm.svdone', 'advancement grant @s only bm:story/sovereign', 'scoreboard players add @s bm.svwin 1',
                       give('ukey_victor'), 'loot give @s loot bm:p238/spoils',
                       # (3.0a: the Undercrown holds until this key has opened the Victor's Vault - phase237's claim)
                       'scoreboard players operation @s bm.uclm = #urun bm.p2', 'scoreboard players set @s bm.uclk 0', 'scoreboard players add #uowed bm.p2 1',
                       tellraw('@s', P + [T(L.SOV, COL, bold=True), T(' has fallen. ', 'gray'), T(L.FIGHT['fall2'], '#c8a0a0', italic=True)]),
                       'execute unless entity @s[tag=bm.svfirst] run function bm:p238/first',
                       'execute unless entity @s[tag=bm.svwings] run function bm:p238/wings',
                       'execute if score @s bm.svwin matches 2 run function bm:p238/second',
                       'execute if score @s bm.svwin matches 2.. unless entity @s[tag=bm.xvunb] run function bm:p238/unbound'])
    # (2.98c) felled a second time: the Bound Sovereign remembers what it was - its Unbound form, at the size it fought you
    fn('p238/unbound', ['tag @s add bm.xvunb', 'advancement grant @s only bm:story/sovereign_unbound',
                        tellraw('@s', [T('  ', 'gray'), T('The Bound Sovereign', COL, bold=True), T(' remembers what it was: ', 'gray'), T('its Unbound form', COL, bold=True),
                                       T(' - as vast as it stood against you. (Its menu: Unbound / Bound.)', 'gray')])])
    G.wjson('bm/advancement/story/sovereign_unbound.json', {'parent': 'bm:story/sovereign', 'criteria': {'won': {'trigger': 'minecraft:impossible'}},
                                                           'display': {'icon': {'id': 'minecraft:paper', 'components': {'minecraft:item_model': 'bm:sov_eye'}},
                                                                       'title': T('Unbound', 'dark_red'), 'description': T('Fell the Dread Sovereign a second time, its Ember kindled again', 'gray'),
                                                                       'frame': 'challenge'}})
    fn('p238/first', ['tag @s add bm.svfirst', give('dread_ember'), give('music_disc_sovereign'),
                      'execute if score #hard bm.cfg matches 1 run function bm:p239/enc/joined',      # (its Eye - and what's left of it, bound to you)
                      tellraw('@s', [T('  In its ashes: ', 'gray'), T('the Dread Ember', COL, bold=True), T(' (the Nights, if ever you miss them), ', 'gray'),
                                     T('its record', COL), T(' - and ', 'gray'), T('the Sovereign\'s Eye', COL, bold=True), T('. Something in it is listening.', 'gray', italic=True)])])
    # (2.99) its wings, both: to every fighter the first time (and to whoever felled it before there were any)
    fn('p238/wings', ['tag @s add bm.svwings', give('sov_wings'), give('sov_wings_holy'),
                      tellraw('@s', [T('  And its wings - ', 'gray'), T('the Last Night', COL, bold=True), T(' and ', 'gray'), T('the First Light', L.HOLY, bold=True),
                                     T(': the dark it became, and the light it was.', 'gray', italic=True)])])
    second.append('execute as @a[scores={bm.svwin=1..},tag=!bm.svwings] run function bm:p238/wings')
    # (they are the Wings of the Damned in every power: p2/ht/wings runs for them too; the First Light's trail is the holy one)
    tick.append('execute as @a[gamemode=!spectator] if items entity @s armor.chest *[minecraft:custom_data~{bm_dwings:1b}] at @s run function bm:p2/ht/wings')
    fn('p238/second', [give('music_disc_aurel'), tellraw('@s', [T('  Something else in the ashes: a pale record. ', 'gray'), T('Aurel', L.HOLY, bold=True), T('.', 'gray')])])

    # ================================================================== ITS SPOILS AT WORK
    G.wjson('bm/advancement/p238/hit.json', {'criteria': {'hit': {'trigger': 'minecraft:player_hurt_entity'}}, 'rewards': {'function': 'bm:p238/hit'}})
    vic = '@e[type=!minecraft:player,distance=..9,nbt={HurtTime:10s},sort=nearest,limit=1]'
    fn('p238/hit', ['advancement revoke @s only bm:p238/hit', 'execute if entity @s[tag=bm.svme] run return 0', 'tag @s add bm.svme',
                    'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{bm:"sov_edge"}] run function bm:p238/edge',
                    f'execute if items entity @s weapon.mainhand *[minecraft:custom_data~{{bm:"chainwhip"}}] as {vic} at @s facing entity @p feet rotated ~ 0 if block ^ ^ ^1 #bm:grap_pass if block ^ ^1 ^1 #bm:grap_pass run tp @s ^ ^ ^1',
                    'tag @s remove bm.svme'])
    fn('p238/edge', ['execute if score @s bm.svt matches 1.. run return 0', 'scoreboard players set @s bm.svt 20',
                     'execute rotated ~ 0 positioned ^ ^1 ^2.5 run particle minecraft:sweep_attack ~ ~ ~ 1.5 0.3 1.5 0 6',
                     'execute rotated ~ 0 positioned ^ ^1 ^2.5 run particle minecraft:dust{color:[0.6,0.0,0.1],scale:1.6} ~ ~ ~ 1.6 0.3 1.6 0 30',
                     'execute rotated ~ 0 positioned ^ ^ ^2.5 as @e[type=#bm:hostile,distance=..3.5] run damage @s 8 minecraft:magic by @p',
                     'effect give @s minecraft:instant_health 1 0 true', 'playsound minecraft:entity.wither.shoot player @a[distance=..16] ~ ~ ~ 0.5 1.4'])
    tick.append('scoreboard players remove @a[scores={bm.svt=1..}] bm.svt 1')
    second.append('execute as @a if items entity @s armor.head *[minecraft:custom_data~{bm:"black_crown"}] at @s run function bm:p238/crown')
    fn('p238/crown', ['effect give @s minecraft:night_vision 15 0 true', 'effect give @e[tag=bm.dread,distance=..8] minecraft:weakness 2 1 true',
                      'particle minecraft:dust{color:[0.82,0.1,0.18],scale:0.8} ~ ~2.2 ~ 0.25 0.05 0.25 0 2'])
    fast.append('execute as @a[gamemode=!spectator,gamemode=!creative] unless score @s bm.svhc matches 1.. if items entity @s container.* *[minecraft:custom_data~{bm:"sov_heart"}] '
                'if predicate bm:p238/low at @s run function bm:p238/heart')
    G.wjson('bm/predicate/p238/low.json', {'condition': 'minecraft:entity_scores', 'entity': 'this', 'scores': {'bm.hp': {'max': 5}}})
    fn('p238/heart', ['scoreboard players set @s bm.svhc 1200', 'effect give @s minecraft:instant_health 1 3', 'effect give @s minecraft:absorption 10 3',
                      'effect give @s minecraft:resistance 3 3', 'particle minecraft:dust{color:[0.7,0.0,0.1],scale:2} ~ ~1 ~ 0.5 0.8 0.5 0 40',
                      'playsound minecraft:entity.warden.heartbeat player @a[distance=..16] ~ ~ ~ 2 0.6',
                      title('@s', 'actionbar', T('The Heart of the Dread beats for you. It does not want you to die. Not yet.', COL, italic=True))])
    second.append('scoreboard players remove @a[scores={bm.svhc=1..}] bm.svhc 1')

    # ================================================================== ADMIN
    fn('admin/under/boss', ['execute unless entity @e[type=minecraft:marker,tag=bm.uthrone] run return run ' + tellraw('@s', P + [T('The throne room isn\'t loaded (or placed).', 'gray')]),
                            f'kill {ME}', 'kill @e[type=minecraft:item_display,tag=bm.svr]', 'scoreboard players set #ufell bm.p2 0',
                            'execute as @e[type=minecraft:marker,tag=bm.uthrone,limit=1] at @s run function bm:p238/spawn',
                            f'tp @s {CX} {CY + 1} {CZ + 22} 180 0'])
    G.FUNCS['admin/help'].append(tellraw('@s', [T('/function bm:admin/under/boss', 'yellow'), T('  the Dread Sovereign, dormant on its throne again (and you in its hall)', 'gray')]))
