"""2.86: THE NEIGHBOR, THE HIDDEN MUSICAL FOLLOWER - THE NEIGHBOR'S BATON. The lad from next door: a black beret, a mime's mask
and thick glasses, a sailor suit with an octopus on the chest, two great eighth notes for wings - and a conductor's baton
(neighbor_art.py, from the owner's art). A support follower: his songs heal and quicken, his notes sting.

FINDING HIM (hidden): at night, in a village (three villagers or more within 32 blocks), put a music disc in a jukebox. Somebody
  next door hears it: the Neighbor turns up to listen, conducting along. Right-click him holding a note block - "Shall we make
  music together?" - and he hands you his baton.
THE NEIGHBOR'S BATON  use: call him (again: call him over); sneak + use: his menu.
TEMPO             while you're within 12 blocks of him: Speed and Haste.
HEALING SONG      (every 10 s, when you're hurt or a fight is on) he conducts a gentle phrase: Regeneration II for everyone near him
                  (players and their followers, 10 blocks).
BATON JAB / SHARP NOTE  a jab with the baton (3) up close; a sharp note flung at a foe up to 16 blocks off (5).
DISSONANCE        two or more foes near: a sour chord - 4 to every foe within 6, slowed and weakened.
CRESCENDO         (charged, every minute) the whole orchestra at once: his crew within 12 healed, Strength and Resistance for ten
                  seconds; every foe within 10 takes 8 and is thrown up into the air.
Right-click him: sit / stand. A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the Tailor his
looks (Navy Bandmaster, Encore Crimson, Jazz Violet; gilded, diamond, netherite) and his aura (Grand Symphony), the Recruiter
his Raid Contract. His pairs and trios: phase188, the bonds."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import neighbor_art as A
import rigfol as RF
import phase95 as FX
import phase46 as P46
import phase89 as P89
import phase68 as P68
import phase98 as P98
import phase100 as P100
import phase134 as P134
import phase141 as P141
import allies

NB_C, NB_LINE, GOLD = '#7ab8ff', '#d8ecff', '#ffcf40'
NAME, W = 'The Neighbor', 'neighbor'
MENU = 2540                          # his menu (bm.menu) and its buttons 2541..2549
PET_HP, PET_CD = 40, 120
SP = A.RIG_SCALE
UP = SP / 16
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')     # (phase95's moods...)
FACE = {'happy': 'happy', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': None}   # (...on his faces)

# ------------------------------------------------------------------------------------------------ items
item('neighbor_baton', TOTEM, "The Neighbor's Baton", NB_C,
     ['A slim black baton, its tip worn pale', 'from a thousand downbeats.', ('Use: call the Neighbor (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('Tempo: Speed and Haste while you\'re near him.', 'blue'),
      ('His songs heal your crew; his notes sting.', 'blue'), ('If he faints: 2 minutes before he can return.', 'gray'),
      ('"From the top - and a one, and a two..."', 'dark_gray')],
     model='bm:neighbor_baton', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['neighbor_baton'] = 'bm:p187/use'
item('fcontract_neighbor', TOTEM, 'Raid Contract: The Neighbor', NB_C, [('Use once: from then on the Neighbor', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_neighbor'] = 'bm:p187/sign'
item('doll_neighbor', TOTEM, 'Neighbor Doll', NB_C, ['A doll of the Neighbor - beret, glasses and his eighth-note wings.', ('Right-click a block: set it down.', 'blue'),
                                                     ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_neighbor', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_neighbor'] = 'bm:p141/doll_neighbor/use'
P141.DOLLS.append(('doll_neighbor', 'The Neighbor', NB_C, 'A doll of the Neighbor - beret, glasses and his eighth-note wings.', 'minecraft:note',
                   'minecraft:block.note_block.chime', 'minecraft:poof'))
P141.DOLL_FROM['doll_neighbor'] = ('neighbor_baton', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.nbpet'
allies.ALLIES += ['bm.nbpet']
P89.BIT[W] = 2 ** len(P89.BIT)
P68.KINDS[W] = (max(v[0] for v in P68.KINDS.values()) + 1, 'neighbor_baton', 'wolf', 'bm.nbpet', 'p187/summon', 'p187/dismiss', 'bm.nbsel2', NAME, NB_C)
P68.HE.add(W)
P98.CALLED.append((W, NAME, NB_C, 'wolf', 'bm.nbpet', 'bm.nbsel2', 'bm.nbcd', 'p187/try_summon', 'p187/dismiss', 'p187/recall', 'p187/go'))
P100.WHO[W] = ('wolf', 'bm.nbpet')
P100.VOICE['The Neighbor'] = (NB_C, NB_LINE)
FX.FOLK[W] = ('minecraft:wolf', 'bm.nbpet', 'type=minecraft:item_display,tag=bm.nbp,tag=bm.nbp_head,tag=bm.nbp_pet,tag=!bm.nbfade', EXPR,
              (60, 130), [('happy', 30, 5), ('blink', 4, 3)], ('happy', 40), 'hurt', 'surprised')

_figures0 = P134.figures


def _figures():
    F2 = _figures0()
    F2['neighbor_baton'] = (NAME, P134._rigkit(A, A.POSES['idle_a'], SP))
    return F2


P134.figures = _figures
P134.FIT['neighbor_baton'] = (0.0, 1.58, -0.78, 0.78, -0.50, 0.42)     # (his wings the widest of him; re-measure with phase134.measure)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((2, 14, 12, 4), fill=hexc('#141418'), width=2); d.line((3, 14, 13, 4), fill=hexc('#4a4a54'))
    d.line((12, 4, 14, 2), fill=hexc('#e8e8ee'), width=2)
    d.rectangle((1, 12, 4, 15), fill=hexc('#2a2a30'))
    d.ellipse((8, 10, 12, 13), fill=hexc('#7ab8ff')); d.line((12, 11, 12, 6), fill=hexc('#7ab8ff')); d.line((12, 6, 14, 8), fill=hexc('#7ab8ff'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)
    R.ICONS['neighbor_baton'] = _icon()
    R.HATS['doll_neighbor'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                       'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/nb_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(f'nb_head_x{FACE[e]}' if FACE[e] else 'nb_head')} for e in EXPR],
                                                         'fallback': mdl('nb_head')}})
    R.POST.insert(0, post)                      # (first: phase138 copies these item definitions for the recoloured looks)


def textures():
    return A.textures()


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
    fn('p187/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed +
       [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{NAME} is already under contract.", 'gray'),
        f'scoreboard players add @s bm.fcon {bit}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_neighbor"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.note_block.chime player @s ~ ~ ~ 0.5 1.2',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(NAME, NB_C, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p187/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T(NAME, NB_C), T(' needs his ', 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
        'return 0'])
    o = offer(('gutter_trophy', 1), ('fcontract_neighbor', 1), ('gutter_medallion', 3))
    Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


POSES = A.POSES
CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
         2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
         6: (None, [(0, 'wave_a')]), 7: (None, [(0, 'strike_up'), (5, 'strike')]), 8: (None, [(0, 'strike_up'), (6, 'strike')]),
         9: (None, [(0, 'conduct_a'), (5, 'conduct_b'), (10, 'conduct_a'), (15, 'conduct_b')]),
         11: (None, [(0, 'crescendo'), (8, 'strike')]), 13: (None, [(0, 'bow')]),
         12: (None, [(0, 'conduct_a'), (6, 'conduct_b'), (12, 'crescendo'), (24, 'bow')]),
         10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 5, 'sit_a': 20, 'sit_b': 20,
       'wave_a': 8, 'strike_up': 5, 'strike': 2, 'conduct_a': 5, 'conduct_b': 5, 'crescendo': 6, 'bow': 8}
QUIPS = ['And a one, and a two...', 'Fortissimo!', 'You missed a beat. ...On purpose? Bold.', 'That monster is flat. Painfully flat.',
         'Encore? No? Fine.', 'Hello, neighbor!', 'Keep time, keep time!', 'Music soothes the savage beast. This one is just savage.']


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    tick, fast, second = [], [], []
    S = lambda s: f'bm.nq{s}'
    objs = [S(s) for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'bc', 'gc', 'sc', 'sl', 'z', 'qp', 'hc', 'l', 'fg', 'ef', 'el')] + ['bm.nbcd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet, me, sel, sel2, new, fade, own = 'bm.nbpet', 'bm.nbme', 'bm.nbsel', 'bm.nbsel2', 'bm.nbnew', 'bm.nbfade', 'bm.nbown'
    pfx = 'p187'
    nbsay = lambda txt, who='@s': title(who, 'actionbar', [T('The Neighbor: ', NB_C, bold=True), T(txt, NB_LINE)])
    nbchat = lambda txt, who='@s': tellraw(who, [T('The Neighbor: ', NB_C, bold=True), T(f'"{txt}"', NB_LINE)])

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.nbp_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    disp = lambda tags: [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.nbp", f"bm.nbp_{p}"] + tags, SP, scale0=True, extra=dict(view_range=F(1.6), brightness={"block": Int(13), "sky": Int(13)}, shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5)))}'
                         for p in A.PARTS]
    rig = disp(['bm.nbp_pet', new])
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = ['particle minecraft:poof ~ ~0.8 ~ 0.4 0.7 0.4 0.03 30', 'particle minecraft:note ~ ~1.4 ~ 0.6 0.6 0.6 1 12',
             'particle minecraft:flash{color:[0.6,0.8,1.0,1.0]} ~ ~1 ~ 0 0 0 0 1']
    fn(f'{pfx}/burst', burst)
    RF.cycles(fn, pfx, CYCLE, S('fr'), S('s'), lambda p: f'{pfx}/pose/{p}')
    for name in {p for _per, frames in CYCLE.values() for _t, p in frames}:
        fn(f'{pfx}/pose/{name}', RF.pose(A, POSES[name], SP, DUR.get(name, 6), psel))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn(f'{pfx}/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP:.4f}f,{SP:.4f}f,{SP:.4f}f]}}}}'
                       for p in A.PARTS] + [f'function bm:{pfx}/pose/idle_a'])
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
                       f'execute as @e[type=minecraft:item_display,tag=bm.nbp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel("head")} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'bc', 'gc', 'sc', 'sl')] +
       [f'execute {idle_fight} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..12] run function bm:{pfx}/great_go',
        f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
        f'execute {idle_fight} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/chord_go',
        f'execute {idle_fight} unless score @s {S("sc")} matches 1.. run function bm:{pfx}/song_chk',
        f'execute {idle_fight} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/melee_go',
        f'execute {idle_fight} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..16] run function bm:{pfx}/range_go',
        f'function bm:{pfx}/state',
        f'execute if score #st bm.rng = @s {S("s")} run scoreboard players add @s {S("fr")} 1',
        f'execute unless score #st bm.rng = @s {S("s")} run scoreboard players set @s {S("fr")} 0',
        f'scoreboard players operation @s {S("s")} = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute on owner run tag @s add {own}',
        f'execute if score @s {S("s")} matches 7..12 if entity @e[{foe},distance=..18] facing entity @e[{foe},distance=..18,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 7..12 unless entity @e[{foe},distance=..18] rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 0 run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 4 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 6 run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 13 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 1..3 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 10 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'function bm:{pfx}/box',
        f'tag @a[tag={own}] remove {own}', f'tag @e[tag={sel}] remove {sel}'])
    fn(f'{pfx}/face_you', [f'execute if entity @a[tag={own},distance=2.5..14] facing entity @a[tag={own},limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                           f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])

    # ---- his music
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/hurt', ['execute store result storage bm:tmp p187.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp p187'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}']
    end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    # the healing song: when his player's hurt (16 health or less) or a fight is on
    fn(f'{pfx}/song_chk', ['scoreboard players set #hp bm.rng 20', 'execute on owner if entity @s[distance=..16] store result score #hp bm.rng run data get entity @s Health',
                           f'execute if score #hp bm.rng matches ..16 run return run function bm:{pfx}/song_go',
                           f'execute if entity @e[{foe},distance=..10] run return run function bm:{pfx}/song_go'])
    fn(f'{pfx}/song_go', go(9, 20, 'sc', 200, face('happy', 20) + ['playsound minecraft:block.note_block.harp neutral @a[distance=..16] ~ ~ ~ 0.8 1.2']))
    fn(f'{pfx}/melee_go', go(7, 10, 'mc', 20, ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.4 1.8']))
    fn(f'{pfx}/range_go', go(8, 12, 'rc', 30, ['playsound minecraft:block.note_block.pling neutral @a[distance=..16] ~ ~ ~ 0.6 1.6']))
    fn(f'{pfx}/chord_go', go(11, 14, 'bc', 240, face('surprised', 14) + ['playsound minecraft:block.note_block.didgeridoo neutral @a[distance=..20] ~ ~ ~ 1 0.5']))
    fn(f'{pfx}/great_go', go(12, 32, 'gc', 1200, face('happy', 32) + ['playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 0.7']))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 5 run function bm:{pfx}/melee_hit',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/range_hit',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 2..19 run particle minecraft:note ~ ~2 ~ 0.6 0.3 0.6 1 1',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 10 run function bm:{pfx}/song_hit',
                           f'execute if score @s {S("a")} matches 11 if score @s {S("x")} matches 6 run function bm:{pfx}/chord_hit',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 20..31 run particle minecraft:note ~ ~2.2 ~ 1 0.5 1 1 3',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 14 run function bm:{pfx}/great_hit'])
    fn(f'{pfx}/song_hit', ['effect give @a[distance=..10,gamemode=!spectator] minecraft:regeneration 4 1 true',
                           'effect give @e[type=minecraft:wolf,distance=..10] minecraft:regeneration 4 1 true',
                           'effect give @e[type=minecraft:cat,distance=..10] minecraft:regeneration 4 1 true',
                           'particle minecraft:note ~ ~1.6 ~ 2.5 0.8 2.5 1 24', 'particle minecraft:heart ~ ~1.4 ~ 2 0.5 2 0 6',
                           'playsound minecraft:block.note_block.chime neutral @a[distance=..16] ~ ~ ~ 0.8 1.0',
                           'playsound minecraft:block.note_block.chime neutral @a[distance=..16] ~ ~ ~ 0.6 1.5'])
    fn(f'{pfx}/melee_hit', hit(3) + ['playsound minecraft:block.note_block.hat neutral @a[distance=..16] ~ ~ ~ 0.8 1.4', 'particle minecraft:crit ^ ^1 ^1.2 0.3 0.3 0.3 0.1 6',
                                     f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt'] + end)
    fn(f'{pfx}/range_hit', hit(5) + ['playsound minecraft:block.note_block.bit neutral @a[distance=..16] ~ ~ ~ 0.8 1.8',
                                     f'execute positioned ~ ~1.3 ~ facing entity @e[{foe},distance=..16,sort=nearest,limit=1] eyes run function bm:{pfx}/note',
                                     f'execute as @e[{foe},distance=..16,sort=nearest,limit=1] at @s run function bm:{pfx}/noted'] + end)
    fn(f'{pfx}/note', [f'particle minecraft:note ^ ^ ^{d / 2:.1f} 0 0 0 {(d % 24) / 24:.2f} 1' for d in range(2, 32, 2)])
    fn(f'{pfx}/noted', [f'function bm:{pfx}/hurt', 'particle minecraft:note ~ ~1.8 ~ 0.3 0.3 0.3 1 8'])
    fn(f'{pfx}/chord_hit', hit(4) + ['playsound minecraft:block.note_block.didgeridoo neutral @a[distance=..20] ~ ~ ~ 1 0.6',
                                     'playsound minecraft:block.note_block.basedrum neutral @a[distance=..20] ~ ~ ~ 1 0.5',
                                     'particle minecraft:sonic_boom ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:note ~ ~1 ~ 3 0.5 3 0.1 20',
                                     f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/sour'] + end)
    fn(f'{pfx}/sour', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 4 1', 'effect give @s minecraft:weakness 4 0'])
    fn(f'{pfx}/great_hit', hit(8) + ['playsound minecraft:ui.toast.challenge_complete neutral @a[distance=..24] ~ ~ ~ 0.8 1.2',
                                     'playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 1.2',
                                     'playsound minecraft:block.note_block.bell neutral @a[distance=..24] ~ ~ ~ 1 1.6',
                                     'particle minecraft:note ~ ~2 ~ 4 1.5 4 1 60', 'particle minecraft:end_rod ~ ~1 ~ 3 1 3 0.05 30',
                                     'effect give @a[distance=..12,gamemode=!spectator] minecraft:instant_health 1 0 true',
                                     'effect give @a[distance=..12,gamemode=!spectator] minecraft:strength 10 0 true',
                                     'effect give @a[distance=..12,gamemode=!spectator] minecraft:resistance 10 0 true',
                                     f'execute as @e[{foe},distance=..10] at @s run function bm:{pfx}/thrown',
                                     'execute on owner if entity @s[distance=..24] run ' + nbsay('CRESCENDO! The whole orchestra - NOW!')] + end)
    fn(f'{pfx}/thrown', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:levitation 1 2', 'particle minecraft:note ~ ~1 ~ 0.4 0.6 0.4 1 6'])
    fn(f'{pfx}/blow', [f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 7.. run function bm:{pfx}/quip'])
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + nbsay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))

    # ---- TEMPO: his player near him moves and works to his beat
    second += [f'execute as @e[type=minecraft:wolf,tag={pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec']
    fn(f'{pfx}/sec', ['execute on owner if entity @s[distance=..12] run effect give @s minecraft:speed 3 0 true',
                      'execute on owner if entity @s[distance=..12] run effect give @s minecraft:haste 3 0 true',
                      'effect give @s minecraft:regeneration 3 0 true'])

    # ---- his baton: call, call over, sneak for his menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
                'CustomName': T(NAME, NB_C, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(max_health=PET_HP, armor=6, attack_damage=3, movement_speed=0.33,
                                                                                       follow_range=32, step_height=1.0, scale=0.9).items()],
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
    hello = ('Coming! Just finishing the bar.', 'Hello, neighbor! Shall we make some noise?', 'Off home to practise my scales. Call me for the next number!')
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', nbsay(hello[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s bm.nbcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.nbcd',
                             'execute if score @s bm.nbcd matches 1.. run scoreboard players add #m bm.rng 59',
                             'execute if score @s bm.nbcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             'execute if score @s bm.nbcd matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{NAME} is still catching his breath: about ', 'gray'),
                                                                                                                  {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'execute unless function bm:{pfx}/ok run return run ' + say(f"{NAME} won't come here."),
                             'execute if function bm:p58/full run return 0', f'function bm:{pfx}/summon'])
    fn(f'{pfx}/summon', [f'execute positioned ^ ^ ^2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:{pfx}/summon_here',
                         f'function bm:{pfx}/summon_here'])
    fn(f'{pfx}/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet_nbt())}',
                              f'data modify entity @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] Owner set from entity @s UUID',
                              f'execute as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] run function bm:{pfx}/tough',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("s")} -1',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("sl")} 20',
                              f'execute rotated ~180 0 run function bm:{pfx}/rig_here',
                              f'scoreboard players operation @e[tag={new},distance=..4] bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag={new},distance=..4] run tag @s add {sel}', f'function bm:{pfx}/dress', f'function bm:{pfx}/grow',
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.nbp_body,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}',
                              'playsound minecraft:block.note_block.chime neutral @a[distance=..20] ~ ~ ~ 0.8 1.4', nbsay(hello[1])])
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {PET_HP}', f'data modify entity @s Health set value {PET_HP}f', 'attribute @s minecraft:armor base set 6'])   # (the summon's attributes don't take on a wolf)
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'function bm:{pfx}/grow', f'scoreboard players set @s {S("s")} -1'])
    fn(f'{pfx}/dress', ['scoreboard players set #wk bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s bm.cosnb',
                        f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{NAME} isn't with you - he'll wear it next time.", NB_C)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.nbp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 20'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', nbsay(hello[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # his menu (sneak + use the baton)
    powers = [('Tempo', 'Speed and Haste for you while you\'re within 12 blocks of him'),
              ('Healing Song', 'every 10 seconds, when you\'re hurt or a fight is on: Regeneration II for everyone near him - players and their followers'),
              ('Baton Jab / Sharp Note', 'a jab up close (3); a sharp note flung at a foe up to 16 blocks off (5)'),
              ('Dissonance', 'two or more foes near: a sour chord - 4 to every foe within 6, slowed and weakened'),
              ('Crescendo', 'charged, every minute: his crew healed, Strength and Resistance for ten seconds; every foe within 10 takes 8 and is thrown into the air')]
    pdlg = P28.multi([T("THE NEIGHBOR'S WAYS", NB_C, bold=True)], [P28.body([T(n, NB_C, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in powers],
                     [P28.btn([T('« Back', 'gray')], MENU + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(pdlg)}'])
    intro = [T('The Neighbor', NB_C, bold=True), T(' - the musician from next door, at your side. ', 'gray'), T('His songs heal; his notes sting.', 'white')]
    dlg = lambda out: P28.multi([T(ITEMS['neighbor_baton']['name'], NB_C, bold=True)], [P28.body(intro, 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {NAME}', NB_C, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T("The Neighbor's ways", NB_C, bold=True), MENU + 4, width=150, tooltip=T('What he plays - and what it does.', 'gray')),
                                 P28.btn(T('Wardrobe', NB_C, bold=True), MENU + 2, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {MENU}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run return run dialog show @s {snbt(dlg(True))}',
                       f'dialog show @s {snbt(dlg(False))}'])
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
    sit_lines = ('Right! Next movement - allegro!', 'A little rest. Every symphony has one.')
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + nbsay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + nbsay(sit_lines[1])])
    # ---- his click box: right-click him - sit / stand
    hit_tag, clk = 'bm.nbhit', 'bm.nbclk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.nbhnew"],width:0.9f,height:1.7f,response:1b}}',
                      'ride @e[type=minecraft:interaction,tag=bm.nbhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.nbhnew] remove bm.nbhnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + nbsay('Sorry, neighbor - I\'m booked for someone else\'s gig.'),
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + nbsay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + nbsay(sit_lines[1])])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.nbp_pet,tag=bm.nbp_body,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s bm.nbcd {PET_CD}',
                           tellraw('@s', PREFIX + [T(f'{NAME} faints! ', NB_C, bold=True), T('"That\'s... the final... curtain..." ', NB_LINE),
                                                   T(f"The baton needs {PET_CD // 60} minutes before he can come back.", 'gray')])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.nbp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       ['playsound minecraft:block.note_block.harp neutral @a[distance=..20] ~ ~ ~ 1 0.5'])
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:8042751}'])
    second.append('scoreboard players remove @a[scores={bm.nbcd=1..}] bm.nbcd 1')
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, 'neighbor_baton', f'{pfx}/go', NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{NAME} waits outside the vault', NB_C), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T("(Back with you when you're home.)", 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')

    # ================================================================== finding him: a record on, at night, in a village
    G.wjson('bm/advancement/p187/disc.json', {'criteria': {'disc': {'trigger': 'minecraft:item_used_on_block', 'conditions': {'location': {
        'type': 'minecraft:all_of', 'terms': [{'type': 'minecraft:location_check', 'predicate': {'block': {'blocks': 'minecraft:jukebox'}}},
                                              {'type': 'minecraft:match_tool', 'predicate': {'predicates': {'minecraft:jukebox_playable': {}}}}]}}}},
        'rewards': {'function': 'bm:p187/enc/disc'}})
    fn('p187/enc/disc', ['advancement revoke @s only bm:p187/disc', 'execute if entity @s[tag=bm.nbmet] run return 0',
                         'execute store result score #nt bm.rng run time of minecraft:overworld query time', 'scoreboard players operation #nt bm.rng %= #24000 bm.bm', 'execute unless score #nt bm.rng matches 13000..22999 run return 0',
                         'execute at @s store result score #nv bm.rng if entity @e[type=minecraft:villager,distance=..32]',
                         'execute if score #nv bm.rng matches ..2 run return 0',
                         'execute at @s if entity @e[type=minecraft:interaction,tag=bm.nbenc,distance=..48] run return 0',
                         'execute at @s run function bm:p187/enc/near'])
    fn('p187/enc/near', ['execute positioned ^ ^ ^3 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p187/enc/spawn_here',
                         'function bm:p187/enc/spawn_here'])
    fn('p187/enc/spawn_here', ['function bm:p187/enc/spawn', 'playsound minecraft:block.note_block.chime neutral @a[distance=..16] ~ ~ ~ 1 1.2',
                               tellraw('@s', [T('A door clicks open next door... ', NB_LINE, italic=True),
                                              T('Someone in a beret and a sailor suit wanders over, conducting along to your record.', 'gray', italic=True)])])
    enc_hit = snbt({'Tags': ['bm.nbenc', 'bm.nbenew'], 'width': F(0.9), 'height': F(1.7), 'response': B(1)})
    fn('p187/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + disp(['bm.nbencp', 'bm.nbenew']) +
       ['execute as @e[type=minecraft:item_display,tag=bm.nbenew,distance=..1] run tag @s add bm.nbsel',
        'execute facing entity @p feet rotated ~ 0 run function bm:p187/place', 'function bm:p187/grow', 'tag @e[tag=bm.nbsel] remove bm.nbsel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.nbenew,distance=..1] ' + S('el') + ' 0',
        'tag @e[tag=bm.nbenew,distance=..1] remove bm.nbenew'])
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.nbenc] at @s run function bm:p187/enc/tick')
    fn('p187/enc/tick', [f'scoreboard players add @s {S("ef")} 1', f'scoreboard players operation #f bm.rng = @s {S("ef")}', 'scoreboard players operation #f bm.rng %= #40 bm.rng',
                         'execute as @e[type=minecraft:item_display,tag=bm.nbencp,distance=..2] run tag @s add bm.nbsel',
                         'execute if score #f bm.rng matches 0 run function bm:p187/pose/conduct_a', 'execute if score #f bm.rng matches 10 run function bm:p187/pose/conduct_b',
                         'execute if score #f bm.rng matches 20 run function bm:p187/pose/conduct_a', 'execute if score #f bm.rng matches 30 run function bm:p187/pose/idle_b',
                         'execute if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p187/place',
                         'execute if score #f bm.rng matches 10 run particle minecraft:note ~ ~2.1 ~ 0.4 0.2 0.4 1 2',
                         'tag @e[tag=bm.nbsel] remove bm.nbsel'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #40 bm.rng 40']
    second.append('execute as @e[type=minecraft:interaction,tag=bm.nbenc] at @s run function bm:p187/enc/sec')
    fn('p187/enc/sec', [f'scoreboard players add @s {S("el")} 1', 'execute unless entity @a[distance=..48] run return run function bm:p187/enc/gone',
                        f'execute if score @s {S("el")} matches 600.. run return run function bm:p187/enc/gone'])
    fn('p187/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.nbencp,distance=..2]', 'particle minecraft:note ~ ~1.4 ~ 0.4 0.6 0.4 1 12',
                         'particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 20', 'kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.nbenc] if data entity @s interaction at @s run function bm:p187/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.nbenc] if data entity @s attack at @s run data remove entity @s attack']
    fn('p187/enc/click', ['tag @s add bm.nbhere', 'execute on target run function bm:p187/enc/talk', 'tag @s remove bm.nbhere', 'data remove entity @s interaction'])
    fn('p187/enc/talk', ['execute if items entity @s weapon.mainhand minecraft:note_block run return run function bm:p187/enc/recruit',
                         f'execute if items entity @s container.* {holds("neighbor_baton")} run return run ' + nbsay('You\'ve got my baton! Give it a wave - I\'ll be right there.'),
                         nbsay('Hello, neighbor! Lovely record. ...Ever fancied making music of your own? Bring me a note block!'),
                         'playsound minecraft:block.note_block.flute neutral @s ~ ~ ~ 0.8 1.2'])
    fn('p187/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                            'execute as @e[type=minecraft:interaction,tag=bm.nbhere,limit=1] at @s run particle minecraft:note ~ ~1.8 ~ 0.6 0.4 0.6 1 16',
                            'execute as @e[type=minecraft:interaction,tag=bm.nbhere,limit=1] at @s run playsound minecraft:block.note_block.bell neutral @a[distance=..16] ~ ~ ~ 1 1',
                            'execute as @e[type=minecraft:interaction,tag=bm.nbhere,limit=1] at @s run playsound minecraft:block.note_block.bell neutral @a[distance=..16] ~ ~ ~ 1 1.5',
                            nbchat('A note block! For me? Oh, we are going to get along SO well.'),
                            nbchat('Here - my baton. Wave it and I\'ll come running. My songs mend, my notes sting. Hello, neighbor!'),
                            tellraw('@s', PREFIX + [T('The Neighbor joins you! ', NB_C, bold=True), T('Use the baton to call him; sneak + use for his menu.', 'gray')]),
                            'tag @s add bm.nbmet', give('neighbor_baton'), 'advancement grant @s only bm:story/neighbor_friend',
                            'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.2',
                            'execute as @e[type=minecraft:interaction,tag=bm.nbhere,limit=1] at @s run function bm:p187/enc/gone',
                            'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'{sel_pet} run tag @s add {sel2}', f'execute unless entity @e[type=minecraft:wolf,tag={sel2}] unless function bm:p58/full at @s run function bm:{pfx}/summon',
                            f'tag @e[tag={sel2}] remove {sel2}'])
    G.wjson('bm/advancement/story/neighbor_friend.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:neighbor_baton'}},
                        'title': T('Hello, Neighbor!', 'yellow'), 'description': T('Play a record in a village at night - and win the lad next door over with a note block', 'gray'),
                        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    fn(f'admin/{W}', [give('neighbor_baton'), 'tag @s add bm.nbmet', say("The Neighbor's Baton. (He turns up for anyone who plays a record in a village at night.)", NB_C)])
    fn(f'admin/{W}_meet', ['execute positioned ^ ^ ^3 run function bm:p187/enc/spawn',
                           tellraw('@s', PREFIX + [T('The Neighbor is standing in front of you. Right-click him holding a note block.', 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T("  the Neighbor's Baton (play a record in a village at night);", 'gray'),
                                                T(f' /function bm:admin/{W}_meet', 'yellow'), T(' meet him here', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.nbp]', 'kill @e[type=minecraft:interaction,tag=bm.nbenc]']
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second
