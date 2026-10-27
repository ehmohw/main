"""2.82: KING OMEGA, THE FOLLOWER - OMEGA'S MONOCLE (given to everyone present when he makes his peace, phase169).

OMEGA'S MONOCLE  use: call him (again: call him over); sneak + use: his menu. Full size, like his brother; a ghost - he hovers.
THE KING OF THE DEAD - his SOUL COURT: every hostile thing that dies near him (his kill or yours) gives him a soul (up to
  twelve; they circle him). He spends them:
  CLAW / SOUL FLAME     up close a raking claw (9); further off a bolt of soul fire (7) - no souls needed.
  RAISE THE FALLEN (3)  two spectral copies of the last kind of foe that died rise and fight for you (30 s).
  SOUL SERPENT SQUAD (5) three soul serpents dart out, each biting a foe (8, withering) - then they cackle and fade.
  KING'S PARDON (all, 6+) once a day, when you fall to 3 hearts or less, he spends every soul to pull you back: healed,
                        shielded, and everything near you thrown back.
  SOUL FLAME (charged, every 45 s) his tail's flame thrown wide - 14 to every foe within 7, set alight; you, warded.
  ROYAL SUBJECTS        the undead near him falter (Weakness, Slowness) - they know their king.
Right-click him: sit / stand. A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the Tailor his
looks (Spectral, Blood Moon, Verdant Wraith; gilded, diamond, netherite) and his aura (the Court of Souls), the Recruiter
his Raid Contract.
PAIRS  APOPHISS + OMEGA, "The Serpent Kings": Strength and Resistance for you; both brothers tougher and healing.
TRIO   APOPHISS, PISTACHIO AND CECIL, "The Palace Household": the serpent, the butler and the boy - Regeneration, Speed and
       a supper now and then for you; the three tougher and healing."""
import math
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import omega_art as OA
import rigfol as RF
import phase169 as P169
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase98 as P98
import phase100 as P100
import phase134 as P134
import phase141 as P141
import allies

OM_C, OM_LINE, SOUL = P169.OM_C, P169.OM_LINE, P169.SOUL
NAME, W, K = 'Omega', 'omega', 'om'
MENU = 2280                          # his menu (bm.menu) and its buttons 2281..2289
PET_HP, PET_CD, MAX_SOULS = 80, 300, 12
SP = OA.PET_SCALE
UP = SP / 16
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
A = P169.OArt
RAISE = ['zombie', 'husk', 'drowned', 'skeleton', 'stray', 'bogged', 'wither_skeleton', 'spider', 'cave_spider', 'creeper', 'enderman', 'pillager',
         'vindicator', 'witch', 'piglin', 'zombified_piglin', 'blaze', 'zombie_villager']

# ------------------------------------------------------------------------------------------------ items
item('om_monocle', TOTEM, "Omega's Monocle", OM_C,
     ['A gold monocle on a little chain - a joke', 'gift from his brother, worn for three centuries.', ('Use: call King Omega (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('His Soul Court: souls from the fallen, spent', 'blue'), ('on the dead raised, serpents, and your pardon.', 'blue'),
      ('If he faints: 5 minutes before he can return.', 'gray'), ('"Do keep it polished. I shall check."', 'dark_gray')],
     model='bm:om_monocle', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['om_monocle'] = 'bm:p170/use'
item('fcontract_omega', TOTEM, 'Raid Contract: Omega', OM_C, [('Use once: from then on Omega', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_omega'] = 'bm:p170/sign'
item('doll_omega', TOTEM, 'Omega Doll', OM_C, ['A doll of King Omega - crown, monocle, soul flame and all.', ('Right-click a block: set it down.', 'blue'),
                                               ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_omega', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_omega'] = 'bm:p141/doll_omega/use'
P141.DOLLS.append(('doll_omega', 'Omega', OM_C, 'A doll of King Omega - crown, monocle, soul flame and all.', 'minecraft:soul',
                   'minecraft:entity.allay.ambient_without_item', 'minecraft:soul_fire_flame'))
P141.DOLL_FROM['doll_omega'] = ('om_monocle', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62, 'groups': {'bm:om_jaw': 'head'}})

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.ompet'
allies.ALLIES += ['bm.ompet', 'bm.omraised']
P89.BIT[W] = 2 ** len(P89.BIT)
P68.KINDS[W] = (max(v[0] for v in P68.KINDS.values()) + 1, 'om_monocle', 'wolf', 'bm.ompet', 'p170/summon', 'p170/dismiss', 'bm.omsel2', NAME, OM_C)
P68.HE.add(W)
P98.CALLED.append((W, NAME, OM_C, 'wolf', 'bm.ompet', 'bm.omsel2', 'bm.omcd', 'p170/try_summon', 'p170/dismiss', 'p170/recall', 'p170/go'))
P100.WHO[W] = ('wolf', 'bm.ompet')
P100.VOICE[NAME] = (OM_C, OM_LINE)
FX.FOLK[W] = ('minecraft:wolf', 'bm.ompet', 'type=minecraft:item_display,tag=bm.omp,tag=bm.omp_head,tag=bm.omp_pet,tag=!bm.omfade', EXPR,
              (60, 140), [('happy', 40, 3), ('squint', 26, 6)], ('happy', 40), 'hurt', 'serious')
P100.TRIOS['household'] = ('The Palace Household', '#b48cff', ('apo', 'pistachio', 'cecil'), 'The Palace Household', 'Walk with Apophiss, Pistachio and Cecil at once')
P100.BANTER['household'] = [
    ('Pistachio', 'Master Apophiss. You have tracked mud across three centuries of carpet.', 'Apophiss', 'I have no feet, ghost.'),
    ('Cecil', 'So this is what the palace was like with everyone in it. Loud.', 'Pistachio', 'Lively, Master Cecil. The word is lively.'),
    ('Apophiss', 'The boy lives in my brother\'s west wing? Rent-free?', 'Cecil', 'You tried to conquer the world. I can live where I want.')]

_figures0 = P134.figures


def _figures():
    F2 = _figures0()
    F2['om_monocle'] = (NAME, P134._rigkit(A, OA.POSES['idle_a'], OA.PET_SCALE))
    return F2


P134.figures = _figures
P134.FIT['om_monocle'] = P134.FIT.get('apo_oath', (0.0, 1.9, -0.5, 0.5, -0.25, 0.4))      # (Omega is his brother's build: his fit)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2, 2, 11, 11), outline=hexc('#d8a838'), width=2)
    d.ellipse((4, 4, 9, 9), fill=(242, 240, 216, 110))
    d.point((5, 5), fill=hexc('#ffffff')); d.point((6, 4), fill=hexc('#ffffff'))
    for i, (x, y) in enumerate(((10, 11), (11, 12), (12, 13), (12, 14), (13, 15))):
        d.point((x, y), fill=hexc('#d8a838' if i % 2 else '#9a7420'))
    d.arc((2, 2, 11, 11), 200, 260, fill=hexc('#fff0a0'))
    return im


def rp(R):
    R.ICONS['om_monocle'] = _icon()
    R.HATS['doll_omega'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                    'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])


# ================================================================================================= the datapack
def generate_early(G):
    """(before phase137 reads the Recruiter's stock) his Raid Contract on the Recruiter's books"""
    from gen_dp import offer
    import phase103 as P103
    fn, title, tellraw = G.fn, G.title, G.tellraw
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    Lr = G.FUNCS['p70/r/lobby/init']
    k_ = next(i for i, l in enumerate(Lr) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    bit = P89.BIT[W]
    signed = ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {bit}',
              'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    fn('p170/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed +
       [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{NAME} is already under contract.", 'gray'),
        f'scoreboard players add @s bm.fcon {bit}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_omega"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(NAME, OM_C, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p170/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T(NAME, OM_C), T(' needs his ', 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
        'return 0'])
    o = offer(('gutter_trophy', 1), ('fcontract_omega', 1), ('gutter_medallion', 3))
    Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


POSES = P169.POSES
CYCLE = {0: (60, [(0, 'idle_a'), (30, 'idle_b')]), 1: (24, [(0, 'glide_a'), (6, 'glide_m'), (12, 'glide_b'), (18, 'glide_m')]),
         2: (16, [(0, 'glide_a'), (4, 'glide_m'), (8, 'glide_b'), (12, 'glide_m')]), 3: (None, [(0, 'glide_a')]), 4: (80, [(0, 'sit'), (40, 'sit_b')]),
         6: (None, [(0, 'bow')]), 7: (None, [(0, 'claw_up'), (5, 'claw')]), 8: (None, [(0, 'flame_up'), (6, 'flame_throw')]), 9: (None, [(0, 'summon')]),
         11: (None, [(0, 'summon'), (10, 'rally')]), 12: (None, [(0, 'flame_up'), (8, 'flame_swing'), (10, 'flame_throw'), (20, 'rally')]),
         10: (24, [(0, 'glide_a'), (6, 'glide_m'), (12, 'glide_b'), (18, 'glide_m')])}
DUR = {'idle_a': 30, 'idle_b': 30, 'glide_a': 6, 'glide_m': 6, 'glide_b': 6, 'sit': 20, 'sit_b': 20, 'bow': 10, 'claw_up': 5, 'claw': 3, 'flame_up': 6,
       'flame_swing': 2, 'flame_throw': 3, 'summon': 10, 'rally': 8}
QUIPS = ['Kneel. Or don\'t - you\'ll be lying down soon enough.', 'Another subject for the Court!', 'Three hundred years, and still the best seat in the house.',
         'Do mind my monocle.', 'Off you go, then. To my brother\'s keeping - he owes me.', 'I was a king, you know. I still am. Ask anyone dead.']


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    tick, fast, second = [], [], []
    S = lambda s: f'bm.oq{s}'
    objs = [S(s) for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'uc', 'cc', 'gc', 'sl', 'z', 'qp', 'hc', 'l', 'fg', 'so', 'lk', 'pd', 'rt')] + ['bm.omcd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet, me, sel, sel2, new, fade, own = 'bm.ompet', 'bm.ompme', 'bm.omsel', 'bm.omsel2', 'bm.ompnew', 'bm.omfade', 'bm.omown'
    pfx = 'p170'
    fysay = lambda txt, who='@s': title(who, 'actionbar', [T(f'{NAME}: ', OM_C, bold=True), T(txt, OM_LINE)])
    fychat = lambda txt, who='@s': tellraw(who, [T(f'{NAME}: ', OM_C, bold=True), T(f'"{txt}"', OM_LINE)])

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.omp_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    rig = [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.omp", f"bm.omp_{p}", "bm.omp_pet", new], SP, scale0=True, extra=dict(view_range=F(2.5), shadow_radius=F(0.9 if p == "coil" else 0.0), shadow_strength=F(0.5)))}'
           for p in A.PARTS]
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = ['particle minecraft:soul ~ ~3 ~ 1.4 2.4 1.4 0.04 90', 'particle minecraft:soul_fire_flame ~ ~3 ~ 1.2 2 1.2 0.05 50',
             'particle minecraft:flash{color:[0.5,0.8,1.0,1.0]} ~ ~3 ~ 0 0 0 0 1']
    fn(f'{pfx}/burst', burst)
    RF.cycles(fn, pfx, CYCLE, S('fr'), S('s'), lambda p: f'{pfx}/pose/{p}', tw=dict(G=G, A=A, P=POSES, S=SP, sel=psel))   # (2.94k: sitting down / getting up in steps)
    for name in {p for _per, frames in CYCLE.values() for _t, p in frames}:
        fn(f'{pfx}/pose/{name}', RF.pose(A, POSES[name], SP, DUR.get(name, 6), psel))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn(f'{pfx}/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP:.4f}f,{SP:.4f}f,{SP:.4f}f]}}}}'
                       for p in A.PARTS])
    fn(f'{pfx}/state', [f'execute if score @s {S("sl")} matches 1.. run return run scoreboard players set #st bm.rng 6',
                        f'execute if score @s {S("x")} matches 1.. run return run scoreboard players operation #st bm.rng = @s {S("a")}',
                        'execute if data entity @s {Sitting:1b} run return run scoreboard players set #st bm.rng 4',
                        'execute store result score #og bm.rng run data get entity @s OnGround',
                        'execute if score #og bm.rng matches 0 if predicate bm:swim run return run scoreboard players set #st bm.rng 10',
                        f'execute if score #og bm.rng matches 0 run scoreboard players add @s {S("z")} 1', f'execute if score #og bm.rng matches 1 run scoreboard players set @s {S("z")} 0',
                        f'execute if score @s {S("z")} matches 4.. unless block ~ ~ ~ minecraft:water run return run scoreboard players set #st bm.rng 3',
                        'execute store result score #vx bm.rng run data get entity @s Motion[0] 1000', 'execute store result score #vz bm.rng run data get entity @s Motion[2] 1000',
                        'scoreboard players operation #vx bm.rng *= #vx bm.rng', 'scoreboard players operation #vz bm.rng *= #vz bm.rng',
                        'scoreboard players operation #vx bm.rng += #vz bm.rng',
                        'execute if score #vx bm.rng matches 30000.. run return run scoreboard players set #st bm.rng 2',
                        'execute if score #vx bm.rng matches 500.. run return run scoreboard players set #st bm.rng 1',
                        'scoreboard players set #st bm.rng 0'])
    tick.append(f'execute as @e[type=minecraft:wolf,tag={pet}] at @s run function bm:{pfx}/tick')
    idle_fight = f'unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}}'
    fn(f'{pfx}/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.omp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel("head")} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'uc', 'cc', 'gc', 'sl')] +
       [f'execute {idle_fight} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..7] run function bm:{pfx}/great_go',
        f'execute {idle_fight} unless score @s {S("uc")} matches 1.. if score @s {S("so")} matches 5.. if entity @e[{foe},distance=..14] run function bm:{pfx}/squad_go',
        f'execute {idle_fight} unless score @s {S("cc")} matches 1.. if score @s {S("so")} matches 3.. if entity @e[{foe},distance=..12] run function bm:{pfx}/raise_go',
        f'execute {idle_fight} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..5.5] run function bm:{pfx}/melee_go',
        f'execute {idle_fight} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..5.5] if entity @e[{foe},distance=..18] run function bm:{pfx}/range_go',
        f'function bm:{pfx}/state',
        f'execute if score #st bm.rng = @s {S("s")} run scoreboard players add @s {S("fr")} 1',
        f'execute unless score #st bm.rng = @s {S("s")} run scoreboard players set @s {S("fr")} 0',
        f'scoreboard players operation @s {S("s")} = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute on owner run tag @s add {own}',
        f'execute if score @s {S("s")} matches 7..12 if entity @e[{foe},distance=..18] facing entity @e[{foe},distance=..18,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 7..12 unless entity @e[{foe},distance=..18] rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 0 run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 4 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 6 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 1..3 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 10 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'function bm:{pfx}/box',
        f'tag @a[tag={own}] remove {own}', f'tag @e[tag={sel}] remove {sel}'])
    fn(f'{pfx}/face_you', [f'execute if entity @a[tag={own},distance=2.5..14] facing entity @a[tag={own},limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                           f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])

    # ---- his blows, and the Soul Court
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    # (his kills are his owner's in the game's eyes - a tame wolf's blow credits the player - so p170/kill gives the soul and
    # p170/kind the kind, once, for his blows and yours alike)
    fn(f'{pfx}/hurt', ['execute store result storage bm:tmp p170.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp p170'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    fn(f'{pfx}/soul', [f'execute if score @s {S("so")} matches {MAX_SOULS}.. run return 0', f'scoreboard players add @s {S("so")} 1',
                       'particle minecraft:sculk_soul ~ ~4 ~ 0.6 1 0.6 0.04 6', 'playsound minecraft:particle.soul_escape neutral @a[distance=..16] ~ ~ ~ 1 0.8'])
    go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}']
    end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    fn(f'{pfx}/melee_go', go(7, 10, 'mc', 22, ['playsound minecraft:entity.ravager.attack neutral @a[distance=..16] ~ ~ ~ 0.6 0.7']))
    fn(f'{pfx}/range_go', go(8, 12, 'rc', 50, ['playsound minecraft:item.firecharge.use neutral @a[distance=..16] ~ ~ ~ 0.6 0.6']))
    fn(f'{pfx}/raise_go', go(9, 16, 'cc', 600, face('serious', 16) + [f'scoreboard players remove @s {S("so")} 3']))
    fn(f'{pfx}/squad_go', go(11, 22, 'uc', 900, face('happy', 22) + [f'scoreboard players remove @s {S("so")} 5']))
    fn(f'{pfx}/great_go', go(12, 30, 'gc', 900, face('serious', 30) + ['playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..24] ~ ~ ~ 1 0.6']))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 4 run function bm:{pfx}/melee_hit',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/range_hit',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 8 run function bm:{pfx}/raise_hit',
                           f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 12 run function bm:{pfx}/squad_hit',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 20..29 run particle minecraft:soul_fire_flame ~ ~5 ~ 1 1 1 0.02 6',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18 run function bm:{pfx}/great_hit'])
    fn(f'{pfx}/melee_hit', hit(9) + ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.8 0.6', 'particle minecraft:soul ^ ^3 ^3 1.2 0.6 0.6 0.02 10',
                                     f'execute as @e[{foe},distance=..5.5,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt'] + end)
    fn(f'{pfx}/range_hit', hit(7) + ['playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.6 0.8',
                                     f'execute positioned ~ ~4 ~ facing entity @e[{foe},distance=..18,sort=nearest,limit=1] eyes run function bm:{pfx}/bolt',
                                     f'execute as @e[{foe},distance=..18,sort=nearest,limit=1] at @s run function bm:{pfx}/scorched'] + end)
    fn(f'{pfx}/bolt', [f'particle minecraft:soul_fire_flame ^ ^ ^{d / 2:.1f} 0.06 0.06 0.06 0.005 1' for d in range(2, 34)])
    fn(f'{pfx}/scorched', [f'function bm:{pfx}/hurt', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.03 10'])
    fn(f'{pfx}/great_hit', hit(14) + ['particle minecraft:flash{color:[0.4,0.85,1.0,1.0]} ~ ~3 ~ 0 0 0 0 1', 'particle minecraft:soul_fire_flame ~ ~1 ~ 4 1 4 0.1 160',
                                      'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 0.8 0.8',
                                      'playsound minecraft:entity.blaze.shoot neutral @a[distance=..32] ~ ~ ~ 1 0.5',
                                      f'execute as @e[{foe},distance=..7] at @s run function bm:{pfx}/aflame',
                                      'execute on owner if entity @s[distance=..24] run effect give @s minecraft:resistance 8 1 true',
                                      'execute on owner if entity @s[distance=..24] run ' + fysay('SOUL FLAME! Burn bright, little lights!')] + end)
    fn(f'{pfx}/aflame', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:100s}', 'particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.6 0.3 0.02 8'])
    fn(f'{pfx}/blow', [f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 8.. run function bm:{pfx}/quip'])
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + fysay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))

    # ---- RAISE THE FALLEN: two of the last kind that fell rise, spectral, for 30 s - they glide (the dead don't walk) and strike
    fn(f'{pfx}/raise_hit', ['playsound minecraft:entity.evoker.prepare_summon neutral @a[distance=..24] ~ ~ ~ 1 0.6', 'particle minecraft:soul ~ ~1 ~ 3 0.4 3 0.03 50',
                            f'execute rotated as @s rotated ~ 0 positioned ^2.5 ^ ^2 run function bm:{pfx}/rise', f'execute rotated as @s rotated ~ 0 positioned ^-2.5 ^ ^2 run function bm:{pfx}/rise',
                            'execute on owner if entity @s[distance=..24] run ' + fysay('RISE! Your king has need of you.')])
    rnbt = lambda t: snbt({'Tags': ['bm.omraised', 'bm.omrnew', 'bm.npc', 'bm.seen'], 'NoAI': B(1), 'Silent': B(1), 'PersistenceRequired': B(1),
                           'CustomName': T('Risen', SOUL), 'DeathLootTable': 'minecraft:empty', 'Health': F(24),
                           'attributes': [{'id': 'minecraft:max_health', 'base': D(24)}],
                           'active_effects': [{'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}],
                           'drop_chances': {s: F(0.0) for s in ('mainhand', 'offhand', 'head', 'chest', 'legs', 'feet')}})
    fn(f'{pfx}/rise', ['execute unless block ~ ~ ~ #bm:grap_pass positioned ~ ~1 ~ run return run function bm:p170/rise2', f'function bm:{pfx}/rise2'])
    fn(f'{pfx}/rise2', [f'execute if score @s {S("lk")} matches {i} run summon minecraft:{t} ~ ~ ~ {rnbt(t)}' for i, t in enumerate(RAISE)] +
       [f'execute unless score @s {S("lk")} matches 0..{len(RAISE) - 1} run summon minecraft:zombie ~ ~ ~ {rnbt("zombie")}',
        'scoreboard players operation @e[tag=bm.omrnew,distance=..2] bm.pid = @s bm.pid', f'scoreboard players set @e[tag=bm.omrnew,distance=..2] {S("rt")} 600',
        'tag @e[tag=bm.omrnew,distance=..2] remove bm.omrnew', 'particle minecraft:sculk_soul ~ ~0.5 ~ 0.4 0.6 0.4 0.03 20'])
    tick.append('execute as @e[tag=bm.omraised] at @s run function bm:p170/risen')
    fn(f'{pfx}/risen', [f'scoreboard players remove @s {S("rt")} 1', f'execute unless score @s {S("rt")} matches 1.. run return run function bm:{pfx}/unrise',
                        'execute if block ~ ~-0.1 ~ #bm:grap_pass run tp @s ~ ~-0.25 ~',
                        f'execute if entity @e[{foe},distance=1.6..16] facing entity @e[{foe},distance=..16,sort=nearest,limit=1] feet positioned ^ ^ ^0.2 if block ~ ~0.2 ~ #bm:grap_pass if block ~ ~1.2 ~ #bm:grap_pass run tp @s ~ ~ ~ facing entity @e[{foe},distance=..17,sort=nearest,limit=1] feet',
                        f'scoreboard players operation #rt bm.rng = @s {S("rt")}', 'scoreboard players operation #rt bm.rng %= #20 bm.rng',
                        f'execute if score #rt bm.rng matches 0 as @e[{foe},distance=..2.2,sort=nearest,limit=1] run damage @s 6 minecraft:mob_attack by @e[tag=bm.omraised,limit=1,sort=nearest]',
                        'execute if score #rt bm.rng matches 0 run particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.01 3'])
    fn(f'{pfx}/unrise', ['particle minecraft:soul ~ ~1 ~ 0.3 0.6 0.3 0.04 16', 'tp @s ~ -400 ~', 'kill @s'])
    second.append('execute as @e[tag=bm.omraised] run function bm:p170/risen_owner')
    fn(f'{pfx}/risen_owner', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                              f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
                              f'execute if score #has bm.rng matches 0 at @s run function bm:{pfx}/unrise'])

    # ---- SOUL SERPENT SQUAD: three serpents dart out, each biting a foe
    fn(f'{pfx}/squad_hit', ['playsound minecraft:entity.vex.charge neutral @a[distance=..24] ~ ~ ~ 1 1.4', 'particle minecraft:soul ~ ~3 ~ 1.5 1 1.5 0.05 40',
                            'execute on owner if entity @s[distance=..24] run ' + fysay('Off you go, little ones - play nicely. Or not!')] +
       [f'execute rotated as @s rotated ~{yaw} 0 positioned ^ ^3 ^2 run function bm:{pfx}/squad_one' for yaw in (-50, 0, 50)])
    fn(f'{pfx}/squad_one', ['summon minecraft:marker ~ ~ ~ {Tags:["bm.sshost","bm.ssq","bm.ssnew"]}',
                            'execute as @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] run tp @s ~ ~ ~ ~ 0',
                            'scoreboard players operation @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] bm.pid = @s bm.pid',
                            'scoreboard players set @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] bm.sst 100',
                            'execute as @e[type=minecraft:marker,tag=bm.ssnew,distance=..1] at @s run function bm:p169/ss/born'])
    tick.append('execute as @e[type=minecraft:marker,tag=bm.ssq] at @s run function bm:p170/squad')
    fn(f'{pfx}/squad', ['scoreboard players remove @s bm.sst 1', 'execute unless score @s bm.sst matches 1.. at @s run return run function bm:p169/ss/go',
                        f'execute unless entity @e[{foe},distance=..20] run scoreboard players set #sst bm.rng 3',
                        f'execute if entity @e[{foe},distance=..20] run scoreboard players set #sst bm.rng 0',
                        f'execute if entity @e[{foe},distance=..1.8] run scoreboard players set #sst bm.rng 5',
                        'function bm:p169/ss/state',
                        f'execute if entity @e[{foe},distance=1.5..20] facing entity @e[{foe},distance=..20,sort=nearest,limit=1] eyes positioned ^ ^ ^0.55 run tp @s ~ ~-0.2 ~ ~ 0',
                        f'execute if score @s bm.sst matches 21.. if entity @e[{foe},distance=..1.8] as @e[{foe},distance=..1.8,sort=nearest,limit=1] at @s run function bm:{pfx}/squad_bite',
                        f'execute if score @s bm.sst matches 21.. if entity @e[{foe},distance=..1.8] run scoreboard players set @s bm.sst 20',
                        'execute rotated as @s run function bm:p169/ss/at'])
    fn(f'{pfx}/squad_bite', ['damage @s 8 minecraft:magic', 'effect give @s minecraft:wither 3 0', 'particle minecraft:soul ~ ~1 ~ 0.3 0.5 0.3 0.04 12',
                             'playsound minecraft:entity.allay.ambient_with_item neutral @a[distance=..16] ~ ~ ~ 0.8 1.8'])

    # ---- the KING'S PARDON (you at 3 hearts or less, 6+ souls, once a day); ROYAL SUBJECTS; the court circling him
    ring = [(math.cos(2 * math.pi * k / MAX_SOULS) * 2.6, 4.2 + 0.5 * math.sin(4 * math.pi * k / MAX_SOULS), math.sin(2 * math.pi * k / MAX_SOULS) * 2.6) for k in range(MAX_SOULS)]
    second += [f'execute as @e[type=minecraft:wolf,tag={pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec']
    fn(f'{pfx}/sec', [f'execute if score @s {S("so")} matches {k + 1}.. rotated as @s run particle minecraft:soul ^{x:.2f} ^{y:.2f} ^{z:.2f} 0.05 0.05 0.05 0.005 1' for k, (x, y, z) in enumerate(ring)] +
       ['effect give @e[type=#minecraft:undead,distance=..10,tag=!bm.omraised,tag=!bm.npc,tag=!bm.omboss] minecraft:weakness 2 0',
        'effect give @e[type=#minecraft:undead,distance=..10,tag=!bm.omraised,tag=!bm.npc,tag=!bm.omboss] minecraft:slowness 2 0',
        f'execute if score @s {S("so")} matches 6.. on owner if entity @s[distance=..24,scores={{bm.hp=1..6}}] unless score @s {S("pd")} = #day bm.bm run function bm:{pfx}/pardon'])
    fn(f'{pfx}/pardon', [f'scoreboard players operation @s {S("pd")} = #day bm.bm', 'scoreboard players operation #me bm.pid = @s bm.pid',
                         f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run scoreboard players set @s {S("so")} 0',
                         'effect give @s minecraft:instant_health 1 1 true', 'effect give @s minecraft:regeneration 6 2 true', 'effect give @s minecraft:resistance 4 2 true',
                         'effect give @s minecraft:absorption 30 1 true', f'effect give @e[{foe},distance=..6] minecraft:levitation 1 4',
                         'particle minecraft:soul ~ ~1 ~ 1 1.2 1 0.2 120', 'particle minecraft:flash{color:[0.5,0.85,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1',
                         'playsound minecraft:item.totem.use player @a[distance=..16] ~ ~ ~ 0.8 0.8',
                         title('@s', 'actionbar', [T("THE KING'S PARDON - ", SOUL, bold=True), T('"Not yet, my friend. The Court pays your debt."', OM_LINE)])])
    # (your kills: a soul for his court - while he's out and near; the kind, for Raise the Fallen)
    G.wjson('bm/advancement/p170/kill.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
        {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': '#bm:hostile'}}]}}}, 'rewards': {'function': 'bm:p170/kill'}})
    fn(f'{pfx}/kill', ['advancement revoke @s only bm:p170/kill', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:wolf,tag={pet},distance=..24] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/soul'])
    for i, t in enumerate(RAISE):
        G.wjson(f'bm/advancement/p170/kind_{t}.json', {'criteria': {'k': {'trigger': 'minecraft:player_killed_entity', 'conditions': {'entity': [
            {'condition': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {'minecraft:entity_type': f'minecraft:{t}'}}]}}}, 'rewards': {'function': f'bm:p170/kind/{t}'}})
        fn(f'{pfx}/kind/{t}', [f'advancement revoke @s only bm:p170/kind_{t}', 'scoreboard players operation #me bm.pid = @s bm.pid',
                               f'execute as @e[type=minecraft:wolf,tag={pet},distance=..24] if score @s bm.pid = #me bm.pid run scoreboard players set @s {S("lk")} {i}'])
    # (at court: the souls tithed for favour)
    fn('p170/tithe_souls', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #n bm.rng 0',
                            f'execute as @e[type=minecraft:wolf,tag={pet},distance=..48] if score @s bm.pid = #me bm.pid run scoreboard players operation #n bm.rng = @s {S("so")}',
                            'execute if score #n bm.rng matches 0 run return run ' + P169._C(G).omsay('Your Omega must be here - with souls in his Court - to tithe them.'),
                            f'execute as @e[type=minecraft:wolf,tag={pet},distance=..48] if score @s bm.pid = #me bm.pid run scoreboard players set @s {S("so")} 0',
                            'scoreboard players operation #n bm.rng *= #2 bm.rng', 'scoreboard players operation @s bm.omfav += #n bm.rng',
                            'playsound minecraft:particle.soul_escape player @s ~ ~ ~ 1 0.6', 'particle minecraft:soul ~ ~1 ~ 0.6 1 0.6 0.04 30',
                            P169._C(G).omsay('The souls of the fallen, returned to their king. Well done.'), 'function bm:p169/court/peer'])

    # ---- his monocle: call, call over, sneak for his menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
                'CustomName': T(NAME, OM_C, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(max_health=PET_HP, armor=12, armor_toughness=4, attack_damage=4, knockback_resistance=0.8,
                                                                                       movement_speed=0.34, follow_range=32, step_height=1.5, scale=SP,
                                                                                       water_movement_efficiency=0.6, oxygen_bonus=1000).items()],
                'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn(f'{pfx}/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                      'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                      'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet} run tag @s add {sel2}', 'scoreboard players set #am bm.rng 0',
                      'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                      f'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag={sel2}] run scoreboard players set #am bm.rng 4',
                      f'execute if score #am bm.rng matches 2 run function bm:{pfx}/menu', f'execute if score #am bm.rng matches 4 run function bm:{pfx}/recall',
                      f'execute if score #am bm.rng matches 0 run function bm:{pfx}/try_summon', f'tag @e[tag={sel2}] remove {sel2}'])
    hello = ('Coming, coming - a king never hurries. He merely arrives.', 'King Omega, at your service. Well - at your side. Service is Pistachio\'s department.',
             'Back to the palace, then. Do visit; the dead get so few callers.')
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', fysay(hello[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s bm.omcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.omcd',
                             'execute if score @s bm.omcd matches 1.. run scoreboard players add #m bm.rng 59',
                             'execute if score @s bm.omcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             'execute if score @s bm.omcd matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{NAME} is still gathering himself: about ', 'gray'),
                                                                                                                  {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'execute unless function bm:{pfx}/ok run return run ' + say(f"{NAME} won't come here."),
                             'execute if function bm:p58/full run return 0', f'function bm:{pfx}/summon'])
    fn(f'{pfx}/summon', [f'execute positioned ^ ^ ^2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass if block ~ ~2 ~ #bm:grap_pass run return run function bm:{pfx}/summon_here',
                         f'function bm:{pfx}/summon_here'])
    fn(f'{pfx}/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet_nbt())}',
                              f'data modify entity @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] Owner set from entity @s UUID',
                              f'execute as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] run function bm:{pfx}/tough',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("s")} -1',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("sl")} 24',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("so")} 0',
                              f'execute rotated ~180 0 run function bm:{pfx}/rig_here',
                              f'scoreboard players operation @e[tag={new},distance=..4] bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag={new},distance=..4] run tag @s add {sel}', f'function bm:{pfx}/dress', f'function bm:{pfx}/grow',
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.omp_coil,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}',
                              'playsound minecraft:block.bell.resonate neutral @a[distance=..20] ~ ~ ~ 0.6 0.6', fysay(hello[1])])
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {PET_HP}', f'data modify entity @s Health set value {PET_HP}f', 'attribute @s minecraft:armor base set 12',
                        f'attribute @s minecraft:scale base set {SP}'])
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'function bm:{pfx}/grow', f'scoreboard players set @s {S("s")} -1'])
    fn(f'{pfx}/dress', ['scoreboard players set #wk bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s bm.cosom',
                        f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{NAME} isn't with you - he'll wear it next time.", OM_C)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.omp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:soul ~ ~3 ~ 1 2 1 0.02 20'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', fysay(hello[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # his menu (sneak + use the monocle)
    powers = [('Claw / Soul Flame', 'up close a raking claw (9); further off a bolt of soul fire (7)'),
              ('The Soul Court', f'each hostile thing that dies near him - his kill or yours - gives him a soul (up to {MAX_SOULS}; they circle him)'),
              ('Raise the Fallen (3 souls)', 'two spectral copies of the last kind of foe that fell rise and fight for you, 30 s'),
              ('Soul Serpent Squad (5 souls)', 'three soul serpents dart out, each biting a foe (8, withering)'),
              ("The King's Pardon (all souls, 6+)", 'once a day, you at 3 hearts or less: healed, shielded, everything near you thrown back'),
              ('Soul Flame (charged)', 'every 45 s: 14 to every foe within 7, set alight - and you, warded'),
              ('Royal Subjects', 'the undead near him falter (Weakness, Slowness)')]
    pdlg = P28.multi([T("KING OMEGA'S WAYS", OM_C, bold=True)], [P28.body([T(n, OM_C, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in powers],
                     [P28.btn([T('« Back', 'gray')], MENU + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(pdlg)}'])
    intro = [T('King Omega', OM_C, bold=True), T(' - the King of the Dead, at your side. ', 'gray'), T('Souls from the fallen fill his court; he spends them on the dead raised, on serpents, and on you.', 'white')]
    dlg = lambda out: P28.multi([T(ITEMS['om_monocle']['name'], OM_C, bold=True)],
                                [P28.body(intro, 300)] + ([P28.body([T('His Soul Court: ', SOUL, bold=True), T('$(souls)', 'white'), T(f' of {MAX_SOULS} souls.', 'gray')], 300)] if out else []),
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {NAME}', OM_C, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T("King Omega's ways", OM_C, bold=True), MENU + 4, width=150, tooltip=T('How he fights - and what his souls buy.', 'gray')),
                                 P28.btn(T('Wardrobe', OM_C, bold=True), MENU + 2, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {MENU}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] store result storage bm:tmp p170m.souls int 1 run scoreboard players get @e[type=minecraft:wolf,tag={sel2},limit=1] {S("so")}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run return run function bm:{pfx}/menu_out with storage bm:tmp p170m',
                       f'dialog show @s {snbt(dlg(False))}'])
    fn(f'{pfx}/menu_out', [f'$dialog show @s {snbt(dlg(True))}'])
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {MENU + n} run return run function bm:{pfx}/act' for n in (1, 2, 4, 5, 8, 9)]
    fn(f'{pfx}/act', [f'execute unless score @s bm.menu matches {MENU} run return run function bm:p28/stale',
                      f'execute if score #act bm.pay matches {MENU + 2} run return run function bm:p119/plain/{W}',
                      f'execute if score #act bm.pay matches {MENU + 4} run return run function bm:{pfx}/powers',
                      'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add {sel2}',
                      f'execute if score #act bm.pay matches {MENU + 5} run function bm:{pfx}/menu',
                      f'execute if score #act bm.pay matches {MENU + 8} unless entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/try_summon',
                      f'execute if score #act bm.pay matches {MENU + 8} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/recall',
                      f'execute if score #act bm.pay matches {MENU + 1} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/sit',
                      f'execute if score #act bm.pay matches {MENU + 9} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/dismiss',
                      f'tag @e[tag={sel2}] remove {sel2}'])
    sit_lines = ('Onward! The dead wait for no one - except me.', 'I shall rest a moment. Three hundred years of lying down, and still I enjoy a sit.')
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + fysay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + fysay(sit_lines[1])])
    # ---- his click box: right-click him - sit / stand
    hit_tag, clk = 'bm.omhit', 'bm.omclk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.omhnew"],width:2.4f,height:5.0f,response:1b}}',
                      'ride @e[type=minecraft:interaction,tag=bm.omhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.omhnew] remove bm.omhnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + fysay('Charmed, I\'m sure - but I am engaged elsewhere today.'),
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + fysay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + fysay(sit_lines[1])])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.omp_pet,tag=bm.omp_coil,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s bm.omcd {PET_CD}',
                           tellraw('@s', PREFIX + [T(f'{NAME} faints! ', OM_C, bold=True), T('"Dying twice in one lifetime... how very careless of me..." ', OM_LINE),
                                                   T(f"Omega's Monocle needs {PET_CD // 60} minutes before he can come back.", 'gray')])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.omp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       ['playsound minecraft:particle.soul_escape neutral @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:10471679}'])
    second.append('scoreboard players remove @a[scores={bm.omcd=1..}] bm.omcd 1')
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, 'om_monocle', f'{pfx}/go', NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{NAME} waits outside the vault', OM_C), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T("(Back with you when you're home.)", 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')
    # ---- the monocle, given at his peace (phase169) - or again, if lost
    has = lambda iid: [f'execute if items entity @s container.* {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s weapon.offhand {holds(iid)} run scoreboard players set #has bm.rng 1',
                       f'execute if items entity @s enderchest.* {holds(iid)} run scoreboard players set #has bm.rng 1']
    fn(f'{pfx}/reissue', ['tag @s add bm.ommet', 'scoreboard players set #has bm.rng 0'] + has('om_monocle') +
       ['scoreboard players operation #me bm.pid = @s bm.pid', f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run scoreboard players set #has bm.rng 1',
        'execute if score #has bm.rng matches 1 run return 0', give('om_monocle'),
        tellraw('@s', [T("Omega's Monocle", OM_C, bold=True), T(' is yours: use it to call King Omega; sneak + use: his menu. (His Raid Contract is at the Recruiter in the den.)', 'gray', italic=True)])])
    fn(f'admin/{W}', [give('om_monocle'), 'tag @s add bm.ommet', 'scoreboard players set #omfree bm.omwin 1',
                      say("Omega's Monocle. (King Omega holds court in every Omega Palace now.)", OM_C)])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T("  Omega's Monocle (won by making peace with him in the Omega Palace)", 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.omp]', 'execute as @e[tag=bm.omraised] at @s run function bm:p170/unrise',
                                       'kill @e[type=minecraft:marker,tag=bm.ssq]']
    pairs(G, fn, tellraw, title, PREFIX, second)
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second


def pairs(G, fn, tellraw, title, PREFIX, second):
    """The Serpent Kings (Apophiss + Omega); the Palace Household trio (Apophiss, Pistachio, Cecil)"""
    VO = {'Apophiss': ('#3ad06a', '#c8f0b0'), NAME: (OM_C, OM_LINE)}
    say2 = lambda who, txt: tellraw('@a[tag=bm.p170o]', [T(f'{who}: ', VO[who][0], bold=True), T(f'"{txt}"', VO[who][1])])
    intro = [('Apophiss', 'Hss. Do not walk so close, brother. People will think we get along.'), (NAME, 'We do get along, little brother. You simply have not noticed yet.')]
    banter = [(NAME, 'Remember the orchard? You ate every golden apple and blamed the gulls.', 'Apophiss', 'The gulls were very suspicious birds.'),
              ('Apophiss', 'Must you wear that ridiculous monocle?', NAME, 'You GAVE me this ridiculous monocle.'),
              (NAME, 'I have been dead three hundred years and I am STILL the taller one.', 'Apophiss', 'You float. It does not count.')]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p170 dummy']
    G.OBJECTIVES += ['bm.p170']
    fn('p170/kings_first', ['advancement grant @s only bm:story/pair_kings', tellraw('@s', PREFIX + [T('The Serpent Kings! ', '#9fb4ff', bold=True), T('A new pair - see the README for what it gives.', 'gray')])] +
       [tellraw('@s', [T(f'{w}: ', VO[w][0], bold=True), T(f'"{t}"', VO[w][1])]) for w, t in intro])
    G.wjson('bm/advancement/story/pair_kings.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:om_monocle'}}, 'title': T('The Serpent Kings', 'yellow'),
                        'description': T('Apophiss and Omega, brothers again, side by side', 'gray'), 'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    for j, (a, ta, b, tb) in enumerate(banter):
        fn(f'p170/kings_say{j}', [say2(a, ta), say2(b, tb)])
    fn('p170/kings_banter', ['scoreboard players set @s bm.p170 0', f'execute store result score #r bm.rng run random value 0..{len(banter) - 1}'] +
       [f'execute if score #r bm.rng matches {j} run function bm:p170/kings_say{j}' for j in range(len(banter))])
    ap = 'execute as @e[type=minecraft:wolf,tag=bm.appet,distance=..16] if score @s bm.pid = #me bm.pid'
    second.append('execute as @e[type=minecraft:wolf,tag=bm.ompet,tag=!bm.ffpet] at @s run function bm:p170/pairs')
    fn('p170/pairs', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p170o',
                      'execute unless entity @a[tag=bm.p170o] run return 0', 'scoreboard players set #pa2 bm.rng 0', f'{ap} run scoreboard players set #pa2 bm.rng 1',
                      'execute if score #pa2 bm.rng matches 1 run function bm:p170/kings', 'tag @a remove bm.p170o'])
    regen = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    fn('p170/kings', ['effect give @a[tag=bm.p170o] minecraft:strength 3 0 true', 'effect give @a[tag=bm.p170o] minecraft:resistance 3 0 true',
                      'effect give @s minecraft:resistance 3 1 true', regen, f'{ap} run effect give @s minecraft:resistance 3 1 true', f'{ap} run {regen}',
                      'execute as @a[tag=bm.p170o] unless entity @s[advancements={bm:story/pair_kings=true}] run function bm:p170/kings_first',
                      'scoreboard players add @s bm.p170 1', 'execute if score @s bm.p170 matches 150.. run function bm:p170/kings_banter'])
    # the trio (phase100 tags who's there and calls p100/<key> as the player)
    import phase100 as P100_
    each = lambda mem, cmd: [f'execute as @e[type=minecraft:{P100_.WHO[m][0]},tag={P100_.WHO[m][1]},distance=..24] if function bm:p100/is_mine run {cmd}' for m in mem]
    mem = ('apo', 'pistachio', 'cecil')
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p170h dummy']
    G.OBJECTIVES += ['bm.p170h']
    fn('p100/household', [regen, 'effect give @s minecraft:speed 3 0 true', 'scoreboard players add @s bm.p170h 1',
                          'execute if score @s bm.p170h matches 40.. run function bm:p170/supper'] +
       each(mem, 'effect give @s minecraft:resistance 3 0 true') + each(mem, regen) + ['function bm:p100/banter_tick'])
    fn('p170/supper', ['scoreboard players set @s bm.p170h 0', 'effect give @s minecraft:saturation 1 1 true', 'playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.6 1.2',
                       title('@s', 'actionbar', [T('Pistachio: ', '#7ae890', bold=True), T('Supper from the palace kitchen - Master Cecil helped. Do not ask what with.', '#d8ffe0')])])
    G.wjson('bm/advancement/story/trio_household.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:pi_cloche'}}, 'title': T('The Palace Household', 'yellow'),
                        'description': T('Walk with Apophiss, Pistachio and Cecil at once', 'gray'), 'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
