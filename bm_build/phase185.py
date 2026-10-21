"""2.86: ASHUR, THE FIRE FOLLOWER - ASHUR'S CINDER (won from her in a hot biome: desert, badlands, savanna).

FINDING HER (2.87: HARD MODE ONLY - she only turns up once the world has woken to hard mode): in a desert, badlands or savanna, under the open sky, she may turn up (about once in 25 minutes there), flame
  in her palm, bored and spoiling for a fight. Right-click her holding COAL or CHARCOAL ("Got anything to burn?"): she takes
  it, likes you for it, and gives you her Cinder.
ASHUR'S CINDER  use: call her (again: call her over); sneak + use: her menu.
A DAMAGE DEALER - her HEAT: every blow she lands builds it (up to 10); each two points add 1 to every blow. It cools when
  there's nothing to fight. In water she's doused - no fire until she's out.
  FLAME SLAP      up close: 7, and the foe set alight.
  FIREBALL        further off (to 20): 6, set alight.
  FLAMETHROWER    two or more foes near (or one close): both hands thrust out - a cone of fire for 1.5 s, 3 a burst, every
                  burst setting them alight (every 12 s).
  ERUPTION        (charged, every 45 s) crouched, then up with both arms flung wide: 14 to every foe within 6, set alight and
                  thrown up; you're warded against fire.
  HEARTHWARMTH    you burn no longer than a moment while she's near (Fire Resistance whenever you catch fire).
Right-click her: sit / stand. A frame keeps her, a display case shows her as a figurine, Cecil sells her doll, the Tailor her
looks (Blue Flame, Verdant Ember, Obsidian Rose; gilded, diamond, netherite) and her aura (the Ashfall Crown), the Recruiter
her Raid Contract.
PAIR   ASHUR + CELI, "Fire and Ice": they bicker - Strength for you, both tougher and healing. (Her other pairs and trios:
       phase188, the bonds.)"""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import ashur_art as A
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

AS_C, AS_LINE, EMBER = '#ff7a2a', '#ffd8b0', '#ffb21a'
NAME, W, K = 'Ashur', 'ashur', 'as'
MENU = 2440                          # her menu (bm.menu) and its buttons 2441..2449
PET_HP, PET_CD, MAX_HEAT = 40, 120, 10
SP = A.RIG_SCALE
UP = SP / 16
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')     # (phase95's moods...)
FACE = {'happy': 'grin', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'fierce', 'serious': 'fierce'}   # (...on her faces)
ENC_ODDS = 25                        # per minute, per player in a hot biome under the sky
HOT = ['minecraft:desert', 'minecraft:badlands', 'minecraft:eroded_badlands', 'minecraft:wooded_badlands', 'minecraft:savanna',
       'minecraft:savanna_plateau', 'minecraft:windswept_savanna']

# ------------------------------------------------------------------------------------------------ items
item('ashur_cinder', TOTEM, "Ashur's Cinder", AS_C,
     ['A coal that never goes out, warm in the hand -', 'Ashur gives one only to people she likes.', ('Use: call Ashur (again: call her over).', 'blue'),
      ('Sneak + use: her menu.', 'blue'), ('Her Heat: every blow she lands burns hotter.', 'blue'), ('Flame Slap, Fireball, Flamethrower - and the Eruption.', 'blue'),
      ('If she faints: 2 minutes before she can return.', 'gray'), ('"Don\'t you DARE drop it in water."', 'dark_gray')],
     model='bm:ashur_cinder', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['ashur_cinder'] = 'bm:p185/use'
item('fcontract_ashur', TOTEM, 'Raid Contract: Ashur', AS_C, [('Use once: from then on Ashur', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_ashur'] = 'bm:p185/sign'
item('doll_ashur', TOTEM, 'Ashur Doll', AS_C, ['A doll of Ashur - magma dress, flame tiara and bare feet.', ('Right-click a block: set it down.', 'blue'),
                                               ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_ashur', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_ashur'] = 'bm:p141/doll_ashur/use'
P141.DOLLS.append(('doll_ashur', 'Ashur', AS_C, 'A doll of Ashur - magma dress, flame tiara and bare feet.', 'minecraft:flame',
                   'minecraft:item.firecharge.use', 'minecraft:lava'))
P141.DOLL_FROM['doll_ashur'] = ('ashur_cinder', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.aspet'
allies.ALLIES += ['bm.aspet']
P89.BIT[W] = 2 ** len(P89.BIT)
P68.KINDS[W] = (max(v[0] for v in P68.KINDS.values()) + 1, 'ashur_cinder', 'wolf', 'bm.aspet', 'p185/summon', 'p185/dismiss', 'bm.assel2', NAME, AS_C)
P98.CALLED.append((W, NAME, AS_C, 'wolf', 'bm.aspet', 'bm.assel2', 'bm.ascd', 'p185/try_summon', 'p185/dismiss', 'p185/recall', 'p185/go'))
P100.WHO[W] = ('wolf', 'bm.aspet')
P100.VOICE[NAME] = (AS_C, AS_LINE)
FX.FOLK[W] = ('minecraft:wolf', 'bm.aspet', 'type=minecraft:item_display,tag=bm.asp,tag=bm.asp_head,tag=bm.asp_pet,tag=!bm.asfade', EXPR,
              (50, 120), [('happy', 30, 4), ('squint', 40, 3)], ('happy', 40), 'hurt', 'serious')
_figures0 = P134.figures


def _figures():
    F2 = _figures0()
    F2['ashur_cinder'] = (NAME, P134._rigkit(A, A.POSES['idle'], SP))
    return F2


P134.figures = _figures
P134.FIT['ashur_cinder'] = (0.0, 1.87, -0.5, 0.5, -0.32, 0.36)     # (her flaring skirt and flame crown; re-measured by phase134.measure)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(4, 13), (2, 9), (4, 5), (8, 3), (12, 5), (14, 9), (12, 13)], fill=hexc('#2a0804'), outline=hexc('#120302'))
    for pts, c in (([(5, 11), (7, 8), (9, 9), (11, 6)], '#ff7a14'), ([(4, 8), (7, 6)], '#ffb21a'), ([(8, 12), (10, 10), (12, 10)], '#ff3a10')):
        d.line(pts, fill=hexc(c), width=1)
    d.point((7, 8), fill=hexc('#ffe060')); d.point((10, 10), fill=hexc('#ffe060'))
    d.polygon([(7, 3), (8, 0), (9, 3)], fill=hexc('#ff9a3a'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)
    R.ICONS['ashur_cinder'] = _icon()
    R.HATS['doll_ashur'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                    'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/as_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(f'as_head_x{FACE[e]}')} for e in EXPR], 'fallback': mdl('as_head')}})
    R.POST.insert(0, post)                      # (first: phase138 copies these item definitions for the recoloured looks)


def textures():
    return A.textures()


# ================================================================================================= the datapack
def generate_early(G):
    """(before phase137 reads the Recruiter's stock) her Raid Contract on the Recruiter's books"""
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
    fn('p185/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed +
       [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{NAME} is already under contract.", 'gray'),
        f'scoreboard players add @s bm.fcon {bit}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_ashur"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:item.firecharge.use player @s ~ ~ ~ 0.4 1.6',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(NAME, AS_C, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p185/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T(NAME, AS_C), T(' needs her ', 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
        'return 0'])
    o = offer(('gutter_trophy', 1), ('fcontract_ashur', 1), ('gutter_medallion', 3))
    Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


POSES = A.POSES
CYCLE = {0: (80, [(0, 'idle'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
         2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
         6: (None, [(0, 'wave')]), 7: (None, [(0, 'cast_back'), (4, 'cast')]), 8: (None, [(0, 'cast_back'), (6, 'cast')]), 9: (None, [(0, 'blast')]),
         12: (None, [(0, 'crouch'), (14, 'erupt')]), 10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
DUR = {'idle': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 5, 'sit_a': 20, 'sit_b': 20,
       'wave': 8, 'cast_back': 4, 'cast': 2, 'blast': 4, 'crouch': 8, 'erupt': 3, 'hurt': 4}
QUIPS = ['BURN!', 'Is that all? I\'m barely warm.', 'Stand back - unless you like your eyebrows crispy.', 'Ha! Toast.',
         'Next! ...No? Nobody? Cowards.', 'Ugh, you smell like a wet dog. Hold still.', 'That one was for the badlands.']


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    tick, fast, second = [], [], []
    S = lambda s: f'bm.az{s}'
    objs = [S(s) for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'bc', 'gc', 'sl', 'z', 'qp', 'hc', 'l', 'fg', 'h', 'ef', 'el')] + ['bm.ascd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet, me, sel, sel2, new, fade, own = 'bm.aspet', 'bm.aspme', 'bm.assel', 'bm.assel2', 'bm.aspnew', 'bm.asfade', 'bm.asown'
    pfx = 'p185'
    assay = lambda txt, who='@s': title(who, 'actionbar', [T(f'{NAME}: ', AS_C, bold=True), T(txt, AS_LINE)])
    aschat = lambda txt, who='@s': tellraw(who, [T(f'{NAME}: ', AS_C, bold=True), T(f'"{txt}"', AS_LINE)])

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.asp_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    disp = lambda tags: [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.asp", f"bm.asp_{p}"] + tags, SP, scale0=True, extra=dict(view_range=F(1.6), brightness={"block": Int(13), "sky": Int(13)}, shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5)))}'
                         for p in A.PARTS]
    rig = disp(['bm.asp_pet', new])
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = ['particle minecraft:flame ~ ~1 ~ 0.5 0.9 0.5 0.04 50', 'particle minecraft:lava ~ ~1 ~ 0.4 0.6 0.4 0 10',
             'particle minecraft:flash{color:[1.0,0.55,0.15,1.0]} ~ ~1 ~ 0 0 0 0 1']
    fn(f'{pfx}/burst', burst)
    RF.cycles(fn, pfx, CYCLE, S('fr'), S('s'), lambda p: f'{pfx}/pose/{p}')
    for name in {p for _per, frames in CYCLE.values() for _t, p in frames}:
        fn(f'{pfx}/pose/{name}', RF.pose(A, POSES[name], SP, DUR.get(name, 6), psel))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(CYCLE)]
    fn(f'{pfx}/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP:.4f}f,{SP:.4f}f,{SP:.4f}f]}}}}'
                       for p in A.PARTS] + [f'function bm:{pfx}/pose/idle'])
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
    # (doused: in water she has no fire to throw - she just paddles, furious)
    idle_fight = f'unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}} unless block ~ ~ ~ minecraft:water unless block ~ ~1 ~ minecraft:water'
    fn(f'{pfx}/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.asp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel("head")} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'bc', 'gc', 'sl')] +
       [f'execute {idle_fight} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..6] run function bm:{pfx}/great_go',
        f'execute {idle_fight} unless score @s {S("bc")} matches 1.. if entity @e[{foe},distance=..3.5] run function bm:{pfx}/blast_go',
        f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
        f'execute {idle_fight} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/blast_go',
        f'execute {idle_fight} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3.5] run function bm:{pfx}/melee_go',
        f'execute {idle_fight} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3.5] if entity @e[{foe},distance=..20] run function bm:{pfx}/range_go',
        f'function bm:{pfx}/state',
        f'execute if score #st bm.rng = @s {S("s")} run scoreboard players add @s {S("fr")} 1',
        f'execute unless score #st bm.rng = @s {S("s")} run scoreboard players set @s {S("fr")} 0',
        f'scoreboard players operation @s {S("s")} = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute on owner run tag @s add {own}',
        f'execute if score @s {S("s")} matches 7..12 if entity @e[{foe},distance=..20] facing entity @e[{foe},distance=..20,sort=nearest,limit=1] feet rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 7..12 unless entity @e[{foe},distance=..20] rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 0 run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 4 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 6 run function bm:{pfx}/face_you',
        f'execute if score @s {S("s")} matches 1..3 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'execute if score @s {S("s")} matches 10 rotated as @s rotated ~ 0 run function bm:{pfx}/place',
        f'function bm:{pfx}/box',
        f'tag @a[tag={own}] remove {own}', f'tag @e[tag={sel}] remove {sel}'])
    fn(f'{pfx}/face_you', [f'execute if entity @a[tag={own},distance=2.5..14] facing entity @a[tag={own},limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                           f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])

    # ---- her blows - each one's damage plus her Heat (a point per two)
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/hurt', ['execute store result storage bm:tmp p185.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp p185',
                       'data merge entity @s {Fire:80s}'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}', f'scoreboard players operation #h2 bm.rng = @s {S("h")}',
                     'scoreboard players operation #h2 bm.rng /= #2 bm.rng', 'scoreboard players operation #pd bm.rng += #h2 bm.rng']
    end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    fn(f'{pfx}/melee_go', go(7, 10, 'mc', 20, ['playsound minecraft:item.firecharge.use neutral @a[distance=..16] ~ ~ ~ 0.5 1.4']))
    fn(f'{pfx}/range_go', go(8, 12, 'rc', 40, ['playsound minecraft:entity.blaze.ambient neutral @a[distance=..16] ~ ~ ~ 0.4 1.6']))
    fn(f'{pfx}/blast_go', go(9, 30, 'bc', 240, face('surprised', 30) + ['playsound minecraft:entity.blaze.shoot neutral @a[distance=..20] ~ ~ ~ 0.8 0.6']))
    fn(f'{pfx}/great_go', go(12, 30, 'gc', 900, face('serious', 30) + ['playsound minecraft:block.respawn_anchor.charge neutral @a[distance=..24] ~ ~ ~ 1 1.2']))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 5 run function bm:{pfx}/melee_hit',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 5 run function bm:{pfx}/range_hit',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 2..26 run function bm:{pfx}/blast_tick',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 17..29 run particle minecraft:flame ~ ~0.3 ~ 1.2 0.1 1.2 0.02 6',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 16 run function bm:{pfx}/great_hit'])
    fn(f'{pfx}/melee_hit', hit(7) + ['playsound minecraft:entity.player.attack.sweep neutral @a[distance=..16] ~ ~ ~ 0.7 1.2',
                                     f'execute facing entity @e[{foe},distance=..3.5,sort=nearest,limit=1] feet run particle minecraft:flame ^ ^1 ^1.5 0.3 0.3 0.3 0.04 14',
                                     f'execute as @e[{foe},distance=..3.5,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt'] + end)
    fn(f'{pfx}/range_hit', hit(6) + ['playsound minecraft:entity.blaze.shoot neutral @a[distance=..16] ~ ~ ~ 0.6 1.2',
                                     f'execute positioned ~ ~1.3 ~ facing entity @e[{foe},distance=..20,sort=nearest,limit=1] eyes run function bm:{pfx}/bolt',
                                     f'execute as @e[{foe},distance=..20,sort=nearest,limit=1] at @s run function bm:{pfx}/scorched'] + end)
    fn(f'{pfx}/bolt', [f'particle minecraft:flame ^ ^ ^{d / 2:.1f} 0.08 0.08 0.08 0.01 2' for d in range(2, 40)] +
       [f'particle minecraft:small_flame ^ ^ ^{d / 2:.1f} 0.04 0.04 0.04 0.0 1' for d in range(2, 40, 3)])
    fn(f'{pfx}/scorched', [f'function bm:{pfx}/hurt', 'particle minecraft:lava ~ ~1 ~ 0.3 0.4 0.3 0 6', 'particle minecraft:flame ~ ~1 ~ 0.3 0.5 0.3 0.03 12'])
    # the flamethrower: every 5 ticks a burst down the cone at the nearest foe (3 + Heat), and every one set alight
    fn(f'{pfx}/blast_tick', ['scoreboard players operation #bt bm.rng = @s ' + S('x'), 'scoreboard players operation #bt bm.rng %= #5 bm.rng',
                             f'execute if entity @e[{foe},distance=..10] facing entity @e[{foe},distance=..10,sort=nearest,limit=1] feet rotated ~ 0 positioned ~ ~1.1 ~ run function bm:{pfx}/cone',
                             f'execute unless entity @e[{foe},distance=..10] rotated as @s rotated ~ 0 positioned ~ ~1.1 ~ run function bm:{pfx}/cone'])
    fn(f'{pfx}/cone', [f'particle minecraft:flame ^ ^ ^{d * 0.6 + 0.6:.1f} {0.06 * d:.2f} {0.05 * d:.2f} {0.06 * d:.2f} 0.02 3' for d in range(1, 11)] +
       ['execute if score #bt bm.rng matches 0 run playsound minecraft:block.fire.ambient neutral @a[distance=..16] ~ ~ ~ 1 0.6',
        f'execute if score #bt bm.rng matches 0 positioned ^ ^ ^2 as @e[{foe},distance=..2] at @s run function bm:{pfx}/blast_hurt',
        f'execute if score #bt bm.rng matches 0 positioned ^ ^ ^4.5 as @e[{foe},distance=..2.6,tag=!{me}] at @s run function bm:{pfx}/blast_hurt',
        f'execute if score #bt bm.rng matches 0 run tag @e[tag=bm.asburnt] remove bm.asburnt'])
    fn(f'{pfx}/blast_hurt', ['execute if entity @s[tag=bm.asburnt] run return 0', 'tag @s add bm.asburnt',
                             'execute as @e[type=minecraft:wolf,tag=bm.ashere,limit=1] run tag @s add ' + me] + [])
    # (the cone runs as the wolf: blast_tick tags her for the burst)
    G.FUNCS[f'{pfx}/blast_tick'][0:0] = [f'tag @s add {me}', 'tag @s add bm.ashere']
    G.FUNCS[f'{pfx}/blast_tick'] += ['tag @s remove bm.ashere', f'tag @s remove {me}',
                                     f'execute if score @s {S("x")} matches 2 run function bm:{pfx}/blow']
    G.FUNCS[f'{pfx}/blast_hurt'] += [f'scoreboard players operation #h2 bm.rng = @e[type=minecraft:wolf,tag=bm.ashere,limit=1] {S("h")}',
                                     'scoreboard players set #pd bm.rng 3', 'scoreboard players operation #h2 bm.rng /= #2 bm.rng',
                                     'scoreboard players operation #pd bm.rng += #h2 bm.rng', f'function bm:{pfx}/hurt']
    fn(f'{pfx}/great_hit', hit(14) + ['particle minecraft:flash{color:[1.0,0.55,0.15,1.0]} ~ ~1 ~ 0 0 0 0 1', 'particle minecraft:flame ~ ~0.5 ~ 3.5 0.6 3.5 0.12 180',
                                      'particle minecraft:lava ~ ~0.5 ~ 3 0.4 3 0 40', 'particle minecraft:large_smoke ~ ~1 ~ 3 1 3 0.02 40',
                                      'playsound minecraft:entity.generic.explode neutral @a[distance=..32] ~ ~ ~ 0.8 1.1',
                                      'playsound minecraft:item.firecharge.use neutral @a[distance=..32] ~ ~ ~ 1 0.5',
                                      f'execute as @e[{foe},distance=..6] at @s run function bm:{pfx}/erupted',
                                      'execute on owner if entity @s[distance=..24] run effect give @s minecraft:fire_resistance 10 0 true',
                                      'execute on owner if entity @s[distance=..24] run ' + assay('ERUPTION! Everybody DOWN!')] + end)
    fn(f'{pfx}/erupted', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:140s}', 'effect give @s minecraft:levitation 1 3 true',
                          'particle minecraft:flame ~ ~0.5 ~ 0.3 0.2 0.3 0.06 10'])
    fn(f'{pfx}/blow', [f'execute if score @s {S("h")} matches ..{MAX_HEAT - 1} run scoreboard players add @s {S("h")} 1',
                       f'execute if score @s {S("h")} matches {MAX_HEAT} run particle minecraft:flame ~ ~2 ~ 0.3 0.2 0.3 0.02 4',
                       f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 7.. run function bm:{pfx}/quip'])
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + assay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))
    # ---- (a second) her Heat cools with nothing to fight; Hearthwarmth for you; embers at her feet when she's hot
    second += [f'execute as @e[type=minecraft:wolf,tag={pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec']
    fn(f'{pfx}/sec', [f'execute unless entity @e[{foe},distance=..20] if score @s {S("h")} matches 1.. run scoreboard players remove @s {S("h")} 1',
                      f'execute if score @s {S("h")} matches 5.. run particle minecraft:small_flame ~ ~0.2 ~ 0.3 0.05 0.3 0.01 3',
                      'execute on owner if entity @s[distance=..16,predicate=bm:p34/burning] run effect give @s minecraft:fire_resistance 4 0 true',
                      'effect give @s minecraft:fire_resistance 3 0 true'])

    # ---- her cinder: call, call over, sneak for her menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
                'CustomName': T(NAME, AS_C, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(max_health=PET_HP, armor=6, attack_damage=4, movement_speed=0.36,
                                                                                       follow_range=32, step_height=1.0, water_movement_efficiency=0.4).items()],
                'active_effects': [{'id': 'minecraft:invisibility', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)},
                                   {'id': 'minecraft:fire_resistance', 'amplifier': B(0), 'duration': Int(-1), 'show_particles': B(0), 'show_icon': B(0), 'ambient': B(0)}]}
    in_heist = 'execute if entity @s[tag=bm.gvp] if dimension bm:gutter'
    fn(f'{pfx}/use', [f'{in_heist} run return run ' + say("In the vault your crew answers the Fixer's Ledger - Raid Crew.", '#9ad0ff'),
                      'execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                      'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'{sel_pet} run tag @s add {sel2}', 'scoreboard players set #am bm.rng 0',
                      'execute if predicate bm:p20/sneaking run scoreboard players set #am bm.rng 2',
                      f'execute if score #am bm.rng matches 0 if entity @e[type=minecraft:wolf,tag={sel2}] run scoreboard players set #am bm.rng 4',
                      f'execute if score #am bm.rng matches 2 run function bm:{pfx}/menu', f'execute if score #am bm.rng matches 4 run function bm:{pfx}/recall',
                      f'execute if score #am bm.rng matches 0 run function bm:{pfx}/try_summon', f'tag @e[tag={sel2}] remove {sel2}'])
    hello = ('Coming! Don\'t start the fun without me.', 'Ashur, reporting for property damage.', 'Fine, FINE. Call me when something needs burning.')
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', assay(hello[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s bm.ascd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.ascd',
                             'execute if score @s bm.ascd matches 1.. run scoreboard players add #m bm.rng 59',
                             'execute if score @s bm.ascd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             'execute if score @s bm.ascd matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{NAME} is still rekindling: about ', 'gray'),
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
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("h")} 0',
                              f'execute rotated ~180 0 run function bm:{pfx}/rig_here',
                              f'scoreboard players operation @e[tag={new},distance=..4] bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag={new},distance=..4] run tag @s add {sel}', f'function bm:{pfx}/dress', f'function bm:{pfx}/grow',
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.asp_body,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}',
                              'playsound minecraft:item.firecharge.use neutral @a[distance=..20] ~ ~ ~ 0.8 0.9', assay(hello[1])])
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {PET_HP}', f'data modify entity @s Health set value {PET_HP}f', 'attribute @s minecraft:armor base set 6'])
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'function bm:{pfx}/grow', f'scoreboard players set @s {S("s")} -1'])
    fn(f'{pfx}/dress', ['scoreboard players set #wk bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s bm.cosas',
                        f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{NAME} isn't with you - she'll wear it next time.", AS_C)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.asp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:flame ~ ~1 ~ 0.4 0.8 0.4 0.02 20'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', assay(hello[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # her menu (sneak + use the cinder)
    powers = [('Heat', f'every blow she lands builds it (up to {MAX_HEAT}); each two points add 1 to every blow - it cools when there\'s nothing to fight'),
              ('Flame Slap / Fireball', 'up close a burning slap (7); further off, to 20 blocks, a fireball (6) - both set the foe alight'),
              ('Flamethrower', 'two or more foes near, or one close: a cone of fire for 1.5 s, 3 a burst (every 12 s)'),
              ('Eruption (charged)', 'every 45 s: 14 to every foe within 6, set alight and thrown up - and you, warded against fire'),
              ('Hearthwarmth', 'you burn no longer than a moment while she\'s near'),
              ('Doused', 'in water she has no fire to throw')]
    pdlg = P28.multi([T("ASHUR'S WAYS", AS_C, bold=True)], [P28.body([T(n, AS_C, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in powers],
                     [P28.btn([T('« Back', 'gray')], MENU + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(pdlg)}'])
    intro = [T('Ashur', AS_C, bold=True), T(' - a fire-mage from the hot country, at your side. ', 'gray'), T('Every blow she lands burns hotter than the last.', 'white')]
    dlg = lambda out: P28.multi([T(ITEMS['ashur_cinder']['name'], AS_C, bold=True)],
                                [P28.body(intro, 300)] + ([P28.body([T('Her Heat: ', EMBER, bold=True), T('$(heat)', 'white'), T(f' of {MAX_HEAT}.', 'gray')], 300)] if out else []),
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send her home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {NAME}', AS_C, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T("Ashur's ways", AS_C, bold=True), MENU + 4, width=150, tooltip=T('How she fights.', 'gray')),
                                 P28.btn(T('Wardrobe', AS_C, bold=True), MENU + 2, width=150, tooltip=T('Her looks - and her aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {MENU}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] store result storage bm:tmp p185m.heat int 1 run scoreboard players get @e[type=minecraft:wolf,tag={sel2},limit=1] {S("h")}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run return run function bm:{pfx}/menu_out with storage bm:tmp p185m',
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
    sit_lines = ('Finally! Let\'s go find something to burn.', 'Fine, I\'ll sit. Wake me when it gets interesting.')
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + assay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + assay(sit_lines[1])])
    # ---- her click box: right-click her - sit / stand
    hit_tag, clk = 'bm.ashit', 'bm.asclk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.ashnew"],width:0.9f,height:1.9f,response:1b}}',
                      'ride @e[type=minecraft:interaction,tag=bm.ashnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.ashnew] remove bm.ashnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + assay('Hands off. I\'m spoken for - and I bite. With fire.'),
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + assay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + assay(sit_lines[1])])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.asp_pet,tag=bm.asp_body,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s bm.ascd {PET_CD}',
                           tellraw('@s', PREFIX + [T(f'{NAME} faints! ', AS_C, bold=True), T('"Ugh... I\'m... just... out of... fuel..." ', AS_LINE),
                                                   T(f"Ashur's Cinder needs {PET_CD // 60} minutes before she can come back.", 'gray')])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.asp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       ['playsound minecraft:block.fire.extinguish neutral @a[distance=..20] ~ ~ ~ 0.8 1.2'])
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:16742954}'])
    second.append('scoreboard players remove @a[scores={bm.ascd=1..}] bm.ascd 1')
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, 'ashur_cinder', f'{pfx}/go', NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{NAME} waits outside the vault', AS_C), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T("(Back with you when you're home.)", 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')

    # ================================================================== finding her: the hot country
    G.wjson('bm/predicate/p185/hot.json', {'condition': 'minecraft:location_check', 'predicate': {'biomes': HOT}})
    G.wjson('bm/tags/block/p185_ground.json', {'values': ['minecraft:sand', 'minecraft:red_sand', '#minecraft:terracotta', '#minecraft:dirt', '#minecraft:grass_blocks',
                                                          'minecraft:sandstone', 'minecraft:red_sandstone', 'minecraft:stone', 'minecraft:coarse_dirt', 'minecraft:gravel']})
    second += ['scoreboard players add #aset bm.bm 1', 'execute if score #aset bm.bm matches 60.. run function bm:p185/enc/check']
    fn('p185/enc/check', ['scoreboard players set #aset bm.bm 0',
                          'execute in minecraft:overworld as @a[distance=0..,gamemode=!spectator,predicate=bm:p185/hot] at @s run function bm:p185/enc/roll'])
    fn('p185/enc/roll', ['execute unless score #hard bm.cfg matches 1 run return 0',               # (2.87: a hard-mode exclusive)
                         f'execute if items entity @s container.* {holds("ashur_cinder")} run return 0', f'execute if items entity @s weapon.offhand {holds("ashur_cinder")} run return 0',
                         'execute if entity @e[type=minecraft:interaction,tag=bm.asenc,distance=..128] run return 0',
                         'execute positioned ~ ~1.6 ~ unless predicate bm:sees_sky run return 0',
                         f'execute store result score #r bm.rng run random value 1..{ENC_ODDS}', 'execute unless score #r bm.rng matches 1 run return 0',
                         'execute store result storage bm:tmp asenc.a int 1 run random value 0..359', 'function bm:p185/enc/at with storage bm:tmp asenc'])
    fn('p185/enc/at', ['$execute rotated $(a) 0 positioned ^ ^ ^14 positioned over motion_blocking_no_leaves run function bm:p185/enc/place'])
    fn('p185/enc/place', ['execute unless block ~ ~-1 ~ #bm:p185_ground run return 0', 'execute unless block ~ ~ ~ #bm:grap_pass run return 0',
                          'execute unless block ~ ~1 ~ #bm:grap_pass run return 0', 'function bm:p185/enc/spawn',
                          'execute as @a[distance=..40] run ' + title('@s', 'actionbar', T('Something crackles nearby... "Ugh, it\'s SO boring out here."', AS_LINE))])
    enc_hit = snbt({'Tags': ['bm.asenc', 'bm.asenew'], 'width': F(0.9), 'height': F(1.9), 'response': B(1)})
    fn('p185/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + disp(['bm.asencp', 'bm.asenew']) +
       ['execute as @e[type=minecraft:item_display,tag=bm.asenew,distance=..1] run tag @s add bm.assel',
        'execute store result storage bm:tmp asenc.a int 1 run random value 0..359', 'function bm:p185/enc/turn with storage bm:tmp asenc',
        'function bm:p185/grow', 'tag @e[tag=bm.assel] remove bm.assel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.asenew,distance=..1] ' + S('el') + ' 0',
        'tag @e[tag=bm.asenew,distance=..1] remove bm.asenew'])
    fn('p185/enc/turn', ['$execute rotated $(a) 0 run function bm:p185/place'])
    # she shifts her weight, the flame in her palm flickering; turns to watch anyone who comes close
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.asenc] at @s run function bm:p185/enc/tick')
    fn('p185/enc/tick', [f'scoreboard players add @s {S("ef")} 1', f'scoreboard players operation #f bm.rng = @s {S("ef")}', 'scoreboard players operation #f bm.rng %= #80 bm.rng',
                         'execute as @e[type=minecraft:item_display,tag=bm.asencp,distance=..2] run tag @s add bm.assel'] +
       [f'execute if score #f bm.rng matches {t} run function bm:p185/pose/{p}' for t, p in CYCLE[0][1]] +
       ['execute if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p185/place',
        'execute if score #f bm.rng matches 40 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p185/place',
        'execute if score #f bm.rng matches 20 run particle minecraft:flame ~ ~1 ~ 0.3 0.4 0.3 0.01 4',
        'execute if score #f bm.rng matches 60 run particle minecraft:small_flame ~ ~0.1 ~ 0.3 0.05 0.3 0.0 4',
        'tag @e[tag=bm.assel] remove bm.assel'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.asenc] at @s run function bm:p185/enc/sec')
    fn('p185/enc/sec', [f'scoreboard players add @s {S("el")} 1', 'execute unless entity @a[distance=..80] run return run function bm:p185/enc/gone',
                        f'execute if score @s {S("el")} matches 600.. run return run function bm:p185/enc/gone'])
    fn('p185/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.asencp,distance=..2]', 'particle minecraft:flame ~ ~1 ~ 0.4 0.9 0.4 0.03 40',
                         'particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.01 12', 'kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.asenc] if data entity @s interaction at @s run function bm:p185/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.asenc] if data entity @s attack at @s run function bm:p185/enc/poke']
    fn('p185/enc/click', ['tag @s add bm.ashere2', 'execute on target run function bm:p185/enc/talk', 'tag @s remove bm.ashere2', 'data remove entity @s interaction'])
    fn('p185/enc/poke', ['execute on attacker run ' + assay('OW. Do that again and I\'ll set your hair on fire. Literally.'),
                         'execute on attacker run playsound minecraft:item.firecharge.use neutral @s ~ ~ ~ 0.5 1.4', 'data remove entity @s attack'])
    fn('p185/enc/talk', ['execute if items entity @s weapon.mainhand minecraft:coal run return run function bm:p185/enc/recruit',
                         'execute if items entity @s weapon.mainhand minecraft:charcoal run return run function bm:p185/enc/recruit',
                         f'execute if items entity @s container.* {holds("ashur_cinder")} run return run ' + assay('You have my Cinder, silly. USE it.'),
                         assay("Hm? What do you want? ...Unless you've got something to burn. Coal, charcoal - I'm STARVING."),
                         'playsound minecraft:block.fire.ambient neutral @s ~ ~ ~ 0.8 1.4'])
    fn('p185/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                            'execute as @e[type=minecraft:interaction,tag=bm.ashere2,limit=1] at @s run particle minecraft:flame ~ ~1.2 ~ 0.2 0.3 0.2 0.08 30',
                            'execute as @e[type=minecraft:interaction,tag=bm.ashere2,limit=1] at @s run playsound minecraft:item.firecharge.use neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                            aschat('Ooh! Mm. Smoky. You know, you\'re not as boring as you look.'),
                            aschat('Okay, I\'ve decided: I\'m coming with you. Point me at anything that needs burning.'),
                            tellraw('@s', PREFIX + [T('Ashur joins you! ', AS_C, bold=True), T('She presses a warm Cinder into your hand. Use it to call her; sneak + use for her menu.', 'gray')]),
                            give('ashur_cinder'), 'advancement grant @s only bm:story/ashur_friend',
                            'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.2',
                            'execute as @e[type=minecraft:interaction,tag=bm.ashere2,limit=1] at @s run function bm:p185/enc/gone',
                            'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'{sel_pet} run tag @s add {sel2}', f'execute unless entity @e[type=minecraft:wolf,tag={sel2}] unless function bm:p58/full run function bm:{pfx}/summon',
                            f'tag @e[tag={sel2}] remove {sel2}'])
    G.wjson('bm/advancement/story/ashur_friend.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:ashur_cinder'}},
                        'title': T('Feed the Fire', 'yellow'), 'description': T('Win over Ashur with something to burn', 'gray'),
                        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': False}})
    fn(f'admin/{W}', [give('ashur_cinder'), say("Ashur's Cinder. (She turns up in deserts, badlands and savannas: bring her coal.)", AS_C)])
    fn(f'admin/{W}_meet', ['execute rotated ~ 0 positioned ^ ^ ^4 positioned over motion_blocking_no_leaves run function bm:p185/enc/spawn',
                           tellraw('@s', PREFIX + [T('Ashur is standing in front of you. Right-click her holding coal or charcoal.', 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T("  Ashur's Cinder (won from her in a hot biome);", 'gray'),
                                                T(f' /function bm:admin/{W}_meet', 'yellow'), T(' meet her here', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.asp]', 'kill @e[type=minecraft:interaction,tag=bm.asenc]']
    pairs(G, fn, tellraw, title, PREFIX, second)
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second


def pairs(G, fn, tellraw, title, PREFIX, second):
    """Fire and Ice (Ashur + Celi)"""
    VO = {'Celi': ('#9ad8ff', '#e0f6ff'), NAME: (AS_C, AS_LINE)}
    say2 = lambda who, txt: tellraw('@a[tag=bm.p185o]', [T(f'{who}: ', VO[who][0], bold=True), T(f'"{txt}"', VO[who][1])])
    intro = [('Celi', 'Oh, great. The walking campfire.'), (NAME, 'Oh, great. The walking ice cube. Try not to melt, princess.')]
    banter = [(NAME, 'Is it me, or did it just get COLD in here?', 'Celi', 'It\'s you. You\'re the only thing in the world that thinks warm is normal.'),
              ('Celi', 'Stop standing so close. My spear\'s dripping.', NAME, 'Then stop standing in my heat. Simple.'),
              (NAME, 'Bet I can burn more of them than you can freeze.', 'Celi', 'You\'re on. Loser carries the other one\'s stuff.')]
    G.FUNCS['load'][-1:-1] = ['scoreboard objectives add bm.p185 dummy']
    G.OBJECTIVES += ['bm.p185']
    fn('p185/fi_first', ['advancement grant @s only bm:story/pair_fireice', tellraw('@s', PREFIX + [T('Fire and Ice! ', AS_C, bold=True), T('A new pair - see the README for what it gives.', 'gray')])] +
       [tellraw('@s', [T(f'{w}: ', VO[w][0], bold=True), T(f'"{t}"', VO[w][1])]) for w, t in intro])
    G.wjson('bm/advancement/story/pair_fireice.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:ashur_cinder'}}, 'title': T('Fire and Ice', 'yellow'),
                        'description': T('Ashur and Celi, side by side - and bickering', 'gray'), 'frame': 'task', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    for j, (a, ta, b, tb) in enumerate(banter):
        fn(f'p185/fi_say{j}', [say2(a, ta), say2(b, tb)])
    fn('p185/fi_banter', ['scoreboard players set @s bm.p185 0', f'execute store result score #r bm.rng run random value 0..{len(banter) - 1}'] +
       [f'execute if score #r bm.rng matches {j} run function bm:p185/fi_say{j}' for j in range(len(banter))])
    ce = 'execute as @e[type=minecraft:wolf,tag=bm.celipet,distance=..16] if score @s bm.pid = #me bm.pid'
    second.append('execute as @e[type=minecraft:wolf,tag=bm.aspet,tag=!bm.ffpet] at @s run function bm:p185/pairs')
    fn('p185/pairs', ['scoreboard players operation #me bm.pid = @s bm.pid', 'execute on owner if entity @s[distance=..24] run tag @s add bm.p185o',
                      'execute unless entity @a[tag=bm.p185o] run return 0', 'scoreboard players set #pa2 bm.rng 0', f'{ce} run scoreboard players set #pa2 bm.rng 1',
                      'execute if score #pa2 bm.rng matches 1 run function bm:p185/fireice', 'tag @a remove bm.p185o'])
    regen = 'execute unless predicate bm:p100/regen run effect give @s minecraft:regeneration 5 0 true'
    fn('p185/fireice', ['effect give @a[tag=bm.p185o] minecraft:strength 3 0 true',
                        'effect give @s minecraft:resistance 3 0 true', regen, f'{ce} run effect give @s minecraft:resistance 3 0 true', f'{ce} run {regen}',
                        'execute as @a[tag=bm.p185o] unless entity @s[advancements={bm:story/pair_fireice=true}] run function bm:p185/fi_first',
                        'scoreboard players add @s bm.p185 1', 'execute if score @s bm.p185 matches 150.. run function bm:p185/fi_banter'])
