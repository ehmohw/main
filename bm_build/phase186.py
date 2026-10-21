"""2.86: THE CHEF, THE HIDDEN FOLLOWER - THE GOLDEN LADLE. Chef Fromage's old master: short, stocky, enormous eyes, a great
zigzag moustache, a toque taller than his temper (chef_art.py, from the owner's art; Fromage's portrait is of him).

FINDING HIM (hidden): eat each of the five Prime meats once (beef, pork, mutton, chicken, rabbit). The smell carries: the
  next time you're near Chef Fromage, his old master is there in the kitchen. Right-click him holding any Prime cut - he
  tastes it, approves, and hands you his Golden Ladle.
THE GOLDEN LADLE  use: call him (again: call him over); sneak + use: his menu.
PRIME PRESENCE    while he's out, every farm animal killed near him (cow, mooshroom, pig, sheep, chicken, rabbit) drops its
                  meat as PRIME meat - the same amount, Looting and all; its other drops as ever. (Only real kills: thrown or
                  dispensed meat stays what it is.)
LADLE WHACK       a whack on the head with his ladle (4) - he's a cook, not a fighter. Yet.
FEED HIM          right-click him holding one of Chef Fromage's feasts (any tier): he eats it, and each KIND he's tasted
                  (Health, Strength, Resistance, Haste, Speed) is yours for good as WELL FED: a full belly every few minutes
                  (5 min with one kind ... every minute with all five) - wherever you are, whether he's out or not.
THE MASTER CHEF   all five kinds tasted: he cooks for war. 80 health, and food-based attacks -
  PIE TOSS          to 18 blocks: a pie in the face (6, slowed).
  HOT SOUP          two or more foes near: a pot of scalding soup over the nearest and everything by it (5, set alight).
  MEATBALL BARRAGE  (charged, every 45 s) meatballs for up to five foes at once (8 each, knocked back).
  CREW FEAST        every minute, everyone with you near him: Regeneration and a bite to eat.
Right-click him: sit / stand. A frame keeps him, a display case shows him as a figurine, Cecil sells his doll, the Tailor his
looks (Midnight Brigade, Bistro Blue, Sommelier Wine; gilded, diamond, netherite) and his aura (Kitchen Steam), the Recruiter
his Raid Contract. His pairs and trios: phase188, the bonds."""
import copy
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
import chef_art as A
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

CF_C, CF_LINE, GOLD = '#ffd07a', '#fff0d0', '#ffcf40'
NAME, W = 'The Chef', 'chef'
MENU = 2500                          # his menu (bm.menu) and its buttons 2501..2509
PET_HP, PET_HP2, PET_CD = 40, 80, 120
SP = A.RIG_SCALE
UP = SP / 16
EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')     # (phase95's moods...)
FACE = {'happy': 'happy', 'surprised': 'shout', 'hurt': 'hurt', 'sleepy': 'blink', 'blink': 'blink', 'squint': 'happy', 'serious': None}   # (...on his faces)
BUFFS = ('health', 'strength', 'resistance', 'haste', 'speed')                    # (Chef Fromage's feast kinds - items.FEAST_DEF)
MEATS = {'cow': ('minecraft:beef', 'prime_beef'), 'mooshroom': ('minecraft:beef', 'prime_beef'), 'pig': ('minecraft:porkchop', 'prime_pork'),
         'sheep': ('minecraft:mutton', 'prime_mutton'), 'chicken': ('minecraft:chicken', 'prime_chicken'), 'rabbit': ('minecraft:rabbit', 'prime_rabbit')}
PRIMES = ('prime_beef', 'prime_pork', 'prime_mutton', 'prime_chicken', 'prime_rabbit')

# ------------------------------------------------------------------------------------------------ items
item('chef_ladle', TOTEM, 'The Golden Ladle', CF_C,
     ['A ladle of solid gold, polished till it shines -', 'the Chef never lets it out of his sight. Except to you.', ('Use: call the Chef (again: call him over).', 'blue'),
      ('Sneak + use: his menu.', 'blue'), ('Prime Presence: farm animals near him drop Prime meat.', 'blue'),
      ('Feed him Chef Fromage\'s feasts: every kind, a full belly for good.', 'blue'), ('If he faints: 2 minutes before he can return.', 'gray'),
      ('"Taste! Always taste!"', 'dark_gray')],
     model='bm:chef_ladle', stack=1, cat='magic', glint=True, comps=hold('none'), tier=3)
HOLD['chef_ladle'] = 'bm:p186/use'
item('fcontract_chef', TOTEM, 'Raid Contract: The Chef', CF_C, [('Use once: from then on the Chef', 'blue'), ('will come into the vault with you.', 'blue')],
     model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
HOLD['fcontract_chef'] = 'bm:p186/sign'
item('doll_chef', TOTEM, 'Chef Doll', CF_C, ['A doll of the Chef - toque, moustache and those enormous eyes.', ('Right-click a block: set it down.', 'blue'),
                                             ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
     model='bm:doll_chef', stack=16, cat='fun', comps=hold('none'))
HOLD['doll_chef'] = 'bm:p141/doll_chef/use'
P141.DOLLS.append(('doll_chef', 'The Chef', CF_C, 'A doll of the Chef - toque, moustache and those enormous eyes.', 'minecraft:happy_villager',
                   'minecraft:entity.generic.eat', 'minecraft:poof'))
P141.DOLL_FROM['doll_chef'] = ('chef_ladle', {'kh': 1.55, 'kb': 0.82, 'kl': 0.62})

# ------------------------------------------------------------------------------------------------ the registries
P46.COMPANIONS += ',tag=!bm.kkpet'
allies.ALLIES += ['bm.kkpet']
P89.BIT[W] = 2 ** len(P89.BIT)
P68.KINDS[W] = (max(v[0] for v in P68.KINDS.values()) + 1, 'chef_ladle', 'wolf', 'bm.kkpet', 'p186/summon', 'p186/dismiss', 'bm.kksel2', NAME, CF_C)
P68.HE.add(W)
P98.CALLED.append((W, NAME, CF_C, 'wolf', 'bm.kkpet', 'bm.kksel2', 'bm.kkcd', 'p186/try_summon', 'p186/dismiss', 'p186/recall', 'p186/go'))
P100.WHO[W] = ('wolf', 'bm.kkpet')
P100.VOICE['The Chef'] = (CF_C, CF_LINE)
FX.FOLK[W] = ('minecraft:wolf', 'bm.kkpet', 'type=minecraft:item_display,tag=bm.kkp,tag=bm.kkp_head,tag=bm.kkp_pet,tag=!bm.kkfade', EXPR,
              (60, 130), [('happy', 30, 4), ('squint', 26, 5)], ('happy', 40), 'hurt', 'surprised')

_figures0 = P134.figures


def _figures():
    F2 = _figures0()
    F2['chef_ladle'] = (NAME, P134._rigkit(A, A.POSES['idle_a'], SP))
    return F2


P134.figures = _figures
P134.FIT['chef_ladle'] = (0.0, 1.54, -0.42, 0.42, -0.36, 0.34)     # (his toque the tallest of him; re-measured by phase134.measure)


def extend_offers(O, offer):
    pass


# ================================================================================================= resource pack
def _icon():
    from PIL import Image, ImageDraw
    from phase57_art import hexc
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line((3, 2, 10, 9), fill=hexc('#8a6418'), width=2); d.line((3, 1, 10, 8), fill=hexc('#ffe08a'))
    d.ellipse((8, 7, 15, 14), fill=hexc('#d8a838'), outline=hexc('#6a4a10'))
    d.chord((9, 8, 14, 13), 180, 360, fill=hexc('#fff0a0')); d.point((10, 9), fill=hexc('#ffffff'))
    return im


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)
    R.ICONS['chef_ladle'] = _icon()
    R.HATS['doll_chef'] = ({'s': 'minecraft:block/white_wool'}, [{'from': [6, 0, 6], 'to': [10, 8, 10],
                                                                   'faces': {f: {'uv': [0, 0, 16, 16], 'texture': '#s'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}}])

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        R2.wj('assets/bm/items/cf_head.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                         'cases': [{'when': e, 'model': mdl(f'cf_head_x{FACE[e]}' if FACE[e] else 'cf_head')} for e in EXPR],
                                                         'fallback': mdl('cf_head')}})
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
    fn('p186/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                     'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed +
       [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{NAME} is already under contract.", 'gray'),
        f'scoreboard players add @s bm.fcon {bit}', 'clear @s *[minecraft:custom_data~{bm:"fcontract_chef"}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:entity.generic.eat player @s ~ ~ ~ 0.4 1.4',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(NAME, CF_C, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn('p186/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T(NAME, CF_C), T(' needs his ', 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
        'return 0'])
    o = offer(('gutter_trophy', 1), ('fcontract_chef', 1), ('gutter_medallion', 3))
    Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


def prime_tables(G):
    """each farm animal's vanilla loot table with its meat swapped for the Prime cut - same counts, Looting, everything else"""
    import json, os
    import phase162 as P162
    vd = P162._vanilla_dir()
    for mob, (raw, prime) in MEATS.items():
        t = copy.deepcopy(json.load(open(os.path.join(vd, 'entities', f'{mob}.json'))))
        hits = [0]

        def walk(entries):
            for e in entries:
                if e.get('type') == 'minecraft:item' and e.get('name') == raw:
                    mods = [m for m in P162._mods(e) if m.get('type') != 'minecraft:furnace_smelt']
                    e.clear(); e.update({'type': 'minecraft:loot_table', 'value': f'bm:items/{prime}', 'modifier': mods})
                    hits[0] += 1
                for k in ('children',):
                    if k in e: walk(e[k])
        for pool in t['pools']:
            walk(pool['entries'])
        assert hits[0] == 1, (mob, hits)
        G.wjson(f'bm/loot_table/p186/prime/{mob}.json', t)


POSES = A.POSES
CYCLE = {0: (80, [(0, 'idle_a'), (40, 'idle_b')]), 1: (16, [(0, 'walk_a'), (4, 'walk_up'), (8, 'walk_b'), (12, 'walk_up')]),
         2: (12, [(0, 'run_a'), (3, 'run_up'), (6, 'run_b'), (9, 'run_up')]), 3: (None, [(0, 'jump')]), 4: (80, [(0, 'sit_a'), (40, 'sit_b')]),
         6: (None, [(0, 'wave_a')]), 7: (None, [(0, 'whack_up'), (5, 'whack')]), 8: (None, [(0, 'throw_back'), (6, 'throw')]),
         9: (None, [(0, 'stir_a'), (6, 'stir_b'), (12, 'throw_back'), (16, 'throw')]), 13: (None, [(0, 'taste')]),
         12: (None, [(0, 'feast'), (12, 'throw_back'), (16, 'throw'), (20, 'throw_back'), (24, 'throw')]),
         10: (16, [(2 * i, f'swim_{i}') for i in range(A.SWIM_FRAMES)])}
DUR = {'idle_a': 30, 'idle_b': 30, 'walk_a': 4, 'walk_up': 4, 'walk_b': 4, 'run_a': 3, 'run_up': 3, 'run_b': 3, 'jump': 5, 'sit_a': 20, 'sit_b': 20,
       'wave_a': 8, 'whack_up': 5, 'whack': 2, 'throw_back': 4, 'throw': 2, 'stir_a': 6, 'stir_b': 6, 'taste': 8, 'feast': 8}
QUIPS = ['Magnifique!', 'Too much salt! ...On you, I mean.', 'This one is overcooked.', 'Taste! Always taste!', 'Bon appetit, monster.',
         'In my kitchen, we do not run! ...Except now. Run!', 'A pinch of this, a whack of that.']


def generate(G):
    import phase28 as P28
    import phase73 as P73
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc'
    tick, fast, second = [], [], []
    S = lambda s: f'bm.kq{s}'
    objs = [S(s) for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'bc', 'gc', 'sl', 'z', 'qp', 'hc', 'l', 'fg', 'ef', 'el', 'g', 'gl', 'wf', 'cf')] + ['bm.kkcd']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet, me, sel, sel2, new, fade, own = 'bm.kkpet', 'bm.kkme', 'bm.kksel', 'bm.kksel2', 'bm.kknew', 'bm.kkfade', 'bm.kkown'
    pfx = 'p186'
    cfsay = lambda txt, who='@s': title(who, 'actionbar', [T('The Chef: ', CF_C, bold=True), T(txt, CF_LINE)])
    cfchat = lambda txt, who='@s': tellraw(who, [T('The Chef: ', CF_C, bold=True), T(f'"{txt}"', CF_LINE)])
    prime_tables(G)

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.kkp_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    disp = lambda tags: [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, ["bm.kkp", f"bm.kkp_{p}"] + tags, SP, scale0=True, extra=dict(view_range=F(1.6), brightness={"block": Int(13), "sky": Int(13)}, shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5)))}'
                         for p in A.PARTS]
    rig = disp(['bm.kkp_pet', new])
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = ['particle minecraft:poof ~ ~0.8 ~ 0.4 0.7 0.4 0.03 30', 'particle minecraft:happy_villager ~ ~1 ~ 0.5 0.8 0.5 0 14',
             'particle minecraft:flash{color:[1.0,0.9,0.6,1.0]} ~ ~1 ~ 0 0 0 0 1']
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
    master = 'if entity @s[tag=bm.kkmaster]'
    fn(f'{pfx}/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.kkp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel("head")} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'bc', 'gc', 'sl')] +
       [f'execute {idle_fight} {master} unless score @s {S("gc")} matches 1.. if entity @e[{foe},distance=..14] run function bm:{pfx}/great_go',
        f'execute store result score #nf bm.rng if entity @e[{foe},distance=..8]',
        f'execute {idle_fight} {master} unless score @s {S("bc")} matches 1.. if score #nf bm.rng matches 2.. run function bm:{pfx}/soup_go',
        f'execute {idle_fight} unless score @s {S("mc")} matches 1.. if entity @e[{foe},distance=..3] run function bm:{pfx}/melee_go',
        f'execute {idle_fight} {master} unless score @s {S("rc")} matches 1.. unless entity @e[{foe},distance=..3] if entity @e[{foe},distance=..18] run function bm:{pfx}/range_go',
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

    # ---- his blows
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/hurt', ['execute store result storage bm:tmp p186.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp p186'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}']
    end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    fn(f'{pfx}/melee_go', go(7, 10, 'mc', 22, ['playsound minecraft:item.armor.equip_gold neutral @a[distance=..16] ~ ~ ~ 0.6 1.4']))
    fn(f'{pfx}/range_go', go(8, 12, 'rc', 30, ['playsound minecraft:entity.snowball.throw neutral @a[distance=..16] ~ ~ ~ 0.6 0.8']))
    fn(f'{pfx}/soup_go', go(9, 20, 'bc', 200, face('happy', 20) + ['playsound minecraft:block.brewing_stand.brew neutral @a[distance=..20] ~ ~ ~ 0.8 1.2']))
    fn(f'{pfx}/great_go', go(12, 30, 'gc', 900, face('happy', 30) + ['playsound minecraft:entity.villager.celebrate neutral @a[distance=..24] ~ ~ ~ 1 0.7']))
    fn(f'{pfx}/act_tick', [f'scoreboard players remove @s {S("x")} 1',
                           f'execute if score @s {S("a")} matches 7 if score @s {S("x")} matches 5 run function bm:{pfx}/melee_hit',
                           f'execute if score @s {S("a")} matches 8 if score @s {S("x")} matches 6 run function bm:{pfx}/range_hit',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 13..19 run particle minecraft:bubble_pop ~ ~1 ~ 0.3 0.2 0.3 0.02 3',
                           f'execute if score @s {S("a")} matches 9 if score @s {S("x")} matches 4 run function bm:{pfx}/soup_hit',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 18..29 run particle minecraft:item{{item:"minecraft:cooked_beef"}} ~ ~1.6 ~ 0.3 0.2 0.3 0.05 2',
                           f'execute if score @s {S("a")} matches 12 if score @s {S("x")} matches 14 run function bm:{pfx}/great_hit'])
    fn(f'{pfx}/melee_hit', hit(4) + ['playsound minecraft:block.anvil.land neutral @a[distance=..16] ~ ~ ~ 0.3 2', 'particle minecraft:crit ^ ^1 ^1.2 0.3 0.3 0.3 0.1 8',
                                     f'execute as @e[{foe},distance=..3,sort=nearest,limit=1] at @s run function bm:{pfx}/hurt'] + end)
    fn(f'{pfx}/range_hit', hit(6) + ['playsound minecraft:entity.slime.squish neutral @a[distance=..16] ~ ~ ~ 0.8 1.2',
                                     f'execute positioned ~ ~1.1 ~ facing entity @e[{foe},distance=..18,sort=nearest,limit=1] eyes run function bm:{pfx}/pie',
                                     f'execute as @e[{foe},distance=..18,sort=nearest,limit=1] at @s run function bm:{pfx}/pied'] + end)
    fn(f'{pfx}/pie', [f'particle minecraft:item{{item:"minecraft:pumpkin_pie"}} ^ ^{0.12 * d - 0.006 * d * d:.2f} ^{d / 2:.1f} 0.02 0.02 0.02 0 1' for d in range(2, 36, 2)])
    fn(f'{pfx}/pied', [f'function bm:{pfx}/hurt', 'effect give @s minecraft:slowness 2 1', 'particle minecraft:item{item:"minecraft:pumpkin_pie"} ~ ~1.6 ~ 0.3 0.3 0.3 0.1 16'])
    fn(f'{pfx}/soup_hit', hit(5) + ['playsound minecraft:entity.generic.splash neutral @a[distance=..20] ~ ~ ~ 1 0.8',
                                    f'execute as @e[{foe},distance=..12,sort=nearest,limit=1] at @s run function bm:{pfx}/soup_at'] + end)
    fn(f'{pfx}/soup_at', ['particle minecraft:item{item:"minecraft:mushroom_stew"} ~ ~1 ~ 1.4 0.4 1.4 0.1 40', 'particle minecraft:splash ~ ~0.5 ~ 1.6 0.3 1.6 0 40',
                          'particle minecraft:flame ~ ~0.3 ~ 1.2 0.1 1.2 0.02 16',
                          f'execute as @e[{foe},distance=..3] run function bm:{pfx}/scald'])
    fn(f'{pfx}/scald', [f'function bm:{pfx}/hurt', 'data merge entity @s {Fire:60s}'])
    fn(f'{pfx}/great_hit', hit(8) + ['playsound minecraft:entity.player.burp neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                                     'playsound minecraft:entity.snowball.throw neutral @a[distance=..24] ~ ~ ~ 1 0.6',
                                     f'execute as @e[{foe},distance=..14,sort=nearest,limit=5] at @s run function bm:{pfx}/meatball',
                                     'execute on owner if entity @s[distance=..24] run ' + cfsay('MEATBALL BARRAGE! Seconds, anyone?!')] + end)
    fn(f'{pfx}/meatball', [f'function bm:{pfx}/hurt', 'particle minecraft:item{item:"minecraft:cooked_beef"} ~ ~1.4 ~ 0.3 0.3 0.3 0.12 14',
                           'execute at @e[type=minecraft:wolf,tag=bm.kkme,limit=1] facing entity @s feet run tp @s ^ ^ ^0.8',
                           'effect give @s minecraft:levitation 1 0 true'])
    fn(f'{pfx}/blow', [f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 7.. run function bm:{pfx}/quip'])
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(QUIPS)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + cfsay(q) for n, q in enumerate(QUIPS)] + face('happy', 30))

    # ---- PRIME PRESENCE: the farm animals near him get the Prime tables; away from him, their own again
    G.wjson('bm/tags/entity_type/p186_meaty.json', {'values': [f'minecraft:{m}' for m in MEATS]})
    second += [f'execute as @e[type=minecraft:wolf,tag={pet},tag=!bm.ffpet] at @s run function bm:{pfx}/sec']
    fn(f'{pfx}/sec', [f'execute as @e[type=#bm:p186_meaty,distance=..16,tag=!bm.kkprime] unless data entity @s DeathLootTable run function bm:{pfx}/prime',
                      f'execute if entity @s[tag=bm.kkmaster] run scoreboard players add @s {S("cf")} 1',
                      f'execute if score @s {S("cf")} matches 60.. run function bm:{pfx}/crew_feast',
                      'effect give @s minecraft:regeneration 3 0 true'])
    fn(f'{pfx}/prime', ['tag @s add bm.kkprime'] +
       [f'execute if entity @s[type=minecraft:{m}] run data modify entity @s DeathLootTable set value "bm:p186/prime/{m}"' for m in MEATS])
    second.append(f'execute as @e[type=#bm:p186_meaty,tag=bm.kkprime] at @s unless entity @e[type=minecraft:wolf,tag={pet},distance=..24] run function bm:{pfx}/unprime')
    fn(f'{pfx}/unprime', ['tag @s remove bm.kkprime', 'data remove entity @s DeathLootTable'])
    fn(f'{pfx}/crew_feast', [f'scoreboard players set @s {S("cf")} 0', 'scoreboard players operation #me bm.pid = @s bm.pid',
                             'effect give @a[distance=..8,gamemode=!spectator] minecraft:regeneration 5 0 true',
                             'effect give @a[distance=..8,gamemode=!spectator] minecraft:saturation 1 0 true',
                             'particle minecraft:item{item:"minecraft:bread"} ~ ~1.4 ~ 1.5 0.5 1.5 0.05 20', 'playsound minecraft:entity.generic.eat neutral @a[distance=..12] ~ ~ ~ 0.8 1',
                             'execute on owner if entity @s[distance=..24] run ' + cfsay('Everybody eat! A happy crew is a strong crew!')])

    # ---- FEED HIM: Chef Fromage's feasts; each kind is a bit on his owner (bm.kqg) and its count (bm.kqgl) is WELL FED
    bit_of = {b: 2 ** i for i, b in enumerate(BUFFS)}
    feed = [f'execute if items entity @s weapon.mainhand {holds(f"feast_{b}_{t}")} run return run function bm:{pfx}/feed/{b}' for b in BUFFS for t in (1, 2)]
    for b in BUFFS:
        fn(f'{pfx}/feed/{b}', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                               'execute unless score @s ' + S('g') + ' matches 0.. run scoreboard players set @s ' + S('g') + ' 0',
                               f'scoreboard players operation #q bm.rng = @s {S("g")}', f'scoreboard players set #bit bm.rng {bit_of[b]}',
                               'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng',
                               f'execute if score #q bm.rng matches 1 run return run function bm:{pfx}/feed_again',
                               f'scoreboard players add @s {S("g")} {bit_of[b]}', f'scoreboard players add @s {S("gl")} 1',
                               f'function bm:{pfx}/fed'])
    fn(f'{pfx}/feed_again', ['playsound minecraft:entity.generic.eat neutral @a[distance=..12] ~ ~ ~ 1 1', cfsay('Mmm. I know this one. Delicious - but I know it. Bring me something new!'),
                             f'execute as @e[type=minecraft:wolf,tag={me}] at @s run function bm:{pfx}/tasting'])
    fn(f'{pfx}/fed', ['playsound minecraft:entity.generic.eat neutral @a[distance=..12] ~ ~ ~ 1 0.8', 'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4',
                      f'execute as @e[type=minecraft:wolf,tag={me}] at @s run function bm:{pfx}/tasting',
                      tellraw('@s', [T('The Chef: ', CF_C, bold=True), T('"Oh! OH! Fromage, you clever rat - he remembered my recipe!" ', CF_LINE),
                                     T('Well Fed: ', GOLD, bold=True), {'score': {'name': '@s', 'objective': S('gl')}, 'color': 'white'}, T(' of 5 kinds tasted.', 'gray')]),
                      f'execute if score @s {S("gl")} matches 5.. run function bm:{pfx}/mastered'])
    fn(f'{pfx}/tasting', [f'scoreboard players set @s {S("a")} 13', f'scoreboard players set @s {S("x")} 16'] + face('happy', 30) +
       ['particle minecraft:heart ~ ~1.8 ~ 0.3 0.2 0.3 0 4'])
    fn(f'{pfx}/mastered', ['advancement grant @s only bm:story/chef_master',
                           tellraw('@s', [T('The Chef: ', CF_C, bold=True), T('"All five! My palate is awake again. Now... I cook for WAR!"', CF_LINE)]),
                           tellraw('@s', PREFIX + [T('The Master Chef! ', CF_C, bold=True), T('He throws pies, scalding soup and a barrage of meatballs now - and feeds your crew.', 'gray')]),
                           'scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} at @s run function bm:{pfx}/master_on'])
    fn(f'{pfx}/master_on', ['tag @s add bm.kkmaster', f'attribute @s minecraft:max_health base set {PET_HP2}', f'data modify entity @s Health set value {PET_HP2}f',
                            'attribute @s minecraft:armor base set 10', 'particle minecraft:totem_of_undying ~ ~1 ~ 0.5 0.8 0.5 0.3 40'])
    G.wjson('bm/advancement/story/chef_master.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:chef_ladle'}}, 'title': T('Master Chef', 'yellow'),
                        'description': T('Feed the Chef all five kinds of Chef Fromage\'s feasts', 'gray'), 'frame': 'challenge', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    # WELL FED: a full belly every (6 - kinds) minutes, wherever you are
    second += [f'execute as @a[scores={{{S("gl")}=1..}}] run function bm:{pfx}/wellfed']
    fn(f'{pfx}/wellfed', [f'scoreboard players add @s {S("wf")} 1', 'scoreboard players set #wf bm.rng 6', f'scoreboard players operation #wf bm.rng -= @s {S("gl")}',
                          'scoreboard players operation #wf bm.rng *= #60 bm.rng', f'execute if score @s {S("wf")} < #wf bm.rng run return 0',
                          f'scoreboard players set @s {S("wf")} 0', 'effect give @s minecraft:saturation 1 0 true'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #60 bm.rng 60']

    # ---- his ladle: call, call over, sneak for his menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(PET_HP),
                'CustomName': T(NAME, CF_C, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(max_health=PET_HP, armor=6, attack_damage=3, movement_speed=0.33,
                                                                                       follow_range=32, step_height=1.0, scale=0.85).items()],
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
    hello = ('Coming, coming! Do not let the sauce burn!', 'Bonjour! The Chef is in the kitchen - wherever that may be.', 'I return to my stove. Call me when you are hungry!')
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', cfsay(hello[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s bm.kkcd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.kkcd',
                             'execute if score @s bm.kkcd matches 1.. run scoreboard players add #m bm.rng 59',
                             'execute if score @s bm.kkcd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             'execute if score @s bm.kkcd matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{NAME} is still catching his breath: about ', 'gray'),
                                                                                                                  {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'execute unless function bm:{pfx}/ok run return run ' + say(f"{NAME} won't come here."),
                             'execute if function bm:p58/full run return 0', f'function bm:{pfx}/summon'])
    fn(f'{pfx}/summon', [f'execute positioned ^ ^ ^2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:{pfx}/summon_here',
                         f'function bm:{pfx}/summon_here'])
    fn(f'{pfx}/summon_here', [f'summon minecraft:wolf ~ ~ ~ {snbt(pet_nbt())}',
                              f'data modify entity @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] Owner set from entity @s UUID',
                              f'execute as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] run function bm:{pfx}/tough',
                              f'execute if score @s {S("gl")} matches 5.. as @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] at @s run function bm:{pfx}/master_on',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("s")} -1',
                              f'scoreboard players set @e[type=minecraft:wolf,tag={new},limit=1,sort=nearest] {S("sl")} 20',
                              f'execute rotated ~180 0 run function bm:{pfx}/rig_here',
                              f'scoreboard players operation @e[tag={new},distance=..4] bm.pid = @s bm.pid',
                              f'execute as @e[type=minecraft:item_display,tag={new},distance=..4] run tag @s add {sel}', f'function bm:{pfx}/dress', f'function bm:{pfx}/grow',
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.kkp_body,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}',
                              'playsound minecraft:block.bell.use neutral @a[distance=..20] ~ ~ ~ 0.6 1.6', cfsay(hello[1])])
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {PET_HP}', f'data modify entity @s Health set value {PET_HP}f', 'attribute @s minecraft:armor base set 6'])   # (the summon's attributes don't take on a wolf)
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'function bm:{pfx}/grow', f'scoreboard players set @s {S("s")} -1'])
    fn(f'{pfx}/dress', ['scoreboard players set #wk bm.rng 0', 'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s bm.coskk',
                        f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{NAME} isn't with you - he'll wear it next time.", CF_C)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.kkp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 20'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', cfsay(hello[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # his menu (sneak + use the ladle)
    powers = [('Prime Presence', 'farm animals killed near him drop their meat as Prime meat - Looting and all'),
              ('Ladle Whack', 'a whack on the head (4) - a cook, not a fighter. Yet.'),
              ('Feed him', 'Chef Fromage\'s feasts, right-clicked onto him: each kind he tastes is yours for good as Well Fed - a full belly every few minutes, wherever you are'),
              ('The Master Chef', 'all five kinds tasted: Pie Toss (6, slowed), Hot Soup (5 to a crowd, set alight), the Meatball Barrage (charged: 8 to up to five) and a Crew Feast every minute')]
    pdlg = P28.multi([T("THE CHEF'S WAYS", CF_C, bold=True)], [P28.body([T(n, CF_C, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in powers],
                     [P28.btn([T('« Back', 'gray')], MENU + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {MENU}', f'dialog show @s {snbt(pdlg)}'])
    intro = [T('The Chef', CF_C, bold=True), T(' - Chef Fromage\'s old master, at your side. ', 'gray'), T('Where he goes, the meat is Prime.', 'white')]
    dlg = lambda out: P28.multi([T(ITEMS['chef_ladle']['name'], CF_C, bold=True)],
                                [P28.body(intro, 300), P28.body([T('Well Fed: ', GOLD, bold=True), T('$(fed)', 'white'), T(' of 5 kinds tasted', 'gray'),
                                                                 T('$(master)', CF_C, bold=True)], 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), MENU + 1, width=150), P28.btn(T('Send him home', 'gray'), MENU + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {NAME}', CF_C, bold=True), MENU + 8, width=150)]) +
                                [P28.btn(T("The Chef's ways", CF_C, bold=True), MENU + 4, width=150, tooltip=T('What he does - and what he cooks.', 'gray')),
                                 P28.btn(T('Wardrobe', CF_C, bold=True), MENU + 2, width=150, tooltip=T('His looks - and his aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {MENU}', f'execute store result storage bm:tmp p186m.fed int 1 run scoreboard players get @s {S("gl")}',
                       'data modify storage bm:tmp p186m.master set value ""',
                       f'execute if score @s {S("gl")} matches 5.. run data modify storage bm:tmp p186m.master set value " - the Master Chef!"',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run return run function bm:{pfx}/menu_out with storage bm:tmp p186m',
                       f'function bm:{pfx}/menu_in with storage bm:tmp p186m'])
    fn(f'{pfx}/menu_out', [f'$dialog show @s {snbt(dlg(True))}'])
    fn(f'{pfx}/menu_in', [f'$dialog show @s {snbt(dlg(False))}'])
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
    sit_lines = ('Allons-y! Off to find something to cook.', 'A chef must rest his feet. Wake me for dinner.')
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + cfsay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + cfsay(sit_lines[1])])
    # ---- his click box: right-click him - sit / stand (or, holding a feast, feed him)
    hit_tag, clk = 'bm.kkhit', 'bm.kkclk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.kkhnew"],width:0.9f,height:1.6f,response:1b}}',
                      'ride @e[type=minecraft:interaction,tag=bm.kkhnew,limit=1,sort=nearest] mount @s', 'tag @e[tag=bm.kkhnew] remove bm.kkhnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + cfsay('Non, non - I cook for one master at a time.'),
                      f'tag {cw} add {me}', f'execute store success score #fd bm.rng run function bm:{pfx}/feed', f'tag @e[type=minecraft:wolf,tag={me}] remove {me}',
                      'execute if score #fd bm.rng matches 1 run return 0',
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + cfsay(sit_lines[0]), 'execute if score #s0 bm.rng matches 0 run ' + cfsay(sit_lines[1])])
    fn(f'{pfx}/feed', feed + ['return fail'])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.kkp_pet,tag=bm.kkp_body,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s bm.kkcd {PET_CD}',
                           tellraw('@s', PREFIX + [T(f'{NAME} faints! ', CF_C, bold=True), T('"Mon dieu... too much... butter..." ', CF_LINE),
                                                   T(f"The Golden Ladle needs {PET_CD // 60} minutes before he can come back.", 'gray')])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.kkp_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       ['playsound minecraft:entity.chicken.egg neutral @a[distance=..20] ~ ~ ~ 1 0.6'])
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        'data merge entity @s[type=minecraft:item_display] {brightness:{block:15,sky:15},Glowing:1b,glow_color_override:16765050}'])
    second.append('scoreboard players remove @a[scores={bm.kkcd=1..}] bm.kkcd 1')
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, 'chef_ladle', f'{pfx}/go', NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f'{NAME} waits outside the vault', CF_C), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T("(Back with you when you're home.)", 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')

    # ================================================================== finding him: all five Prime meats eaten, then near Chef Fromage
    from items import ITEMS as _I
    G.wjson('bm/advancement/p186/ate_prime.json', {'criteria': {m: {'trigger': 'minecraft:consume_item', 'conditions': {'item': {
        'items': _I[m]['base'], 'predicates': {'minecraft:custom_data': snbt({'bm': m})}}}} for m in PRIMES}, 'requirements': [[m] for m in PRIMES]})
    second += ['execute as @a[tag=!bm.kkmet,advancements={bm:p186/ate_prime=true},gamemode=!spectator] at @s if entity @e[type=minecraft:villager,tag=bm.npc_chef,distance=..12] '
               'unless entity @e[type=minecraft:interaction,tag=bm.kkenc,distance=..48] run function bm:p186/enc/near']
    fn('p186/enc/near', ['execute positioned ^ ^ ^2 if block ~ ~ ~ #bm:grap_pass if block ~ ~1 ~ #bm:grap_pass run return run function bm:p186/enc/spawn_here',
                         'function bm:p186/enc/spawn_here'])
    fn('p186/enc/spawn_here', ['function bm:p186/enc/spawn', tellraw('@s', [T('A delicious smell drifts out of the kitchen... ', CF_LINE, italic=True),
                                                                            T('Someone small and round, in a very tall hat, is tasting Chef Fromage\'s sauce.', 'gray', italic=True)])])
    enc_hit = snbt({'Tags': ['bm.kkenc', 'bm.kkenew'], 'width': F(0.9), 'height': F(1.6), 'response': B(1)})
    fn('p186/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + disp(['bm.kkencp', 'bm.kkenew']) +
       ['execute as @e[type=minecraft:item_display,tag=bm.kkenew,distance=..1] run tag @s add bm.kksel',
        'execute facing entity @p feet rotated ~ 0 run function bm:p186/place', 'function bm:p186/grow', 'tag @e[tag=bm.kksel] remove bm.kksel',
        'scoreboard players set @e[type=minecraft:interaction,tag=bm.kkenew,distance=..1] ' + S('el') + ' 0',
        'tag @e[tag=bm.kkenew,distance=..1] remove bm.kkenew'])
    tick.append('execute as @e[type=minecraft:interaction,tag=bm.kkenc] at @s run function bm:p186/enc/tick')
    fn('p186/enc/tick', [f'scoreboard players add @s {S("ef")} 1', f'scoreboard players operation #f bm.rng = @s {S("ef")}', 'scoreboard players operation #f bm.rng %= #80 bm.rng',
                         'execute as @e[type=minecraft:item_display,tag=bm.kkencp,distance=..2] run tag @s add bm.kksel',
                         'execute if score #f bm.rng matches 0 run function bm:p186/pose/stir_a', 'execute if score #f bm.rng matches 20 run function bm:p186/pose/stir_b',
                         'execute if score #f bm.rng matches 40 run function bm:p186/pose/taste', 'execute if score #f bm.rng matches 60 run function bm:p186/pose/idle_a',
                         'execute if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:p186/place',
                         'execute if score #f bm.rng matches 40 run particle minecraft:poof ~ ~1.4 ~ 0.2 0.1 0.2 0.01 3',
                         'tag @e[tag=bm.kksel] remove bm.kksel'])
    second.append('execute as @e[type=minecraft:interaction,tag=bm.kkenc] at @s run function bm:p186/enc/sec')
    fn('p186/enc/sec', [f'scoreboard players add @s {S("el")} 1', 'execute unless entity @a[distance=..48] run return run function bm:p186/enc/gone',
                        f'execute if score @s {S("el")} matches 600.. run return run function bm:p186/enc/gone'])
    fn('p186/enc/gone', ['kill @e[type=minecraft:item_display,tag=bm.kkencp,distance=..2]', 'particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 30', 'kill @s'])
    fast += ['execute as @e[type=minecraft:interaction,tag=bm.kkenc] if data entity @s interaction at @s run function bm:p186/enc/click',
             'execute as @e[type=minecraft:interaction,tag=bm.kkenc] if data entity @s attack at @s run data remove entity @s attack']
    fn('p186/enc/click', ['tag @s add bm.kkhere', 'execute on target run function bm:p186/enc/talk', 'tag @s remove bm.kkhere', 'data remove entity @s interaction'])
    fn('p186/enc/talk', [f'execute if items entity @s weapon.mainhand {holds(m)} run return run function bm:p186/enc/recruit' for m in PRIMES] +
       [f'execute if items entity @s container.* {holds("chef_ladle")} run return run ' + cfsay('You have my ladle! Use it, use it - I am getting hungry.'),
        cfsay('Bonjour! Do not touch the sauce. ...You smell of Prime meat. Bring me a Prime cut and let me TASTE it.'),
        'playsound minecraft:entity.villager.ambient neutral @s ~ ~ ~ 0.8 1.6'])
    fn('p186/enc/recruit', ['item modify entity @s weapon.mainhand {function:"minecraft:set_count",count:-1,add:true}',
                            'execute as @e[type=minecraft:interaction,tag=bm.kkhere,limit=1] at @s run particle minecraft:heart ~ ~1.6 ~ 0.3 0.2 0.3 0 6',
                            'execute as @e[type=minecraft:interaction,tag=bm.kkhere,limit=1] at @s run playsound minecraft:entity.generic.eat neutral @a[distance=..16] ~ ~ ~ 1 0.8',
                            cfchat('Mmm... MMM! Prime! Properly hung, beautifully marbled. You have taste, my friend.'),
                            cfchat('Fromage runs this kitchen well - I taught him everything. Now I shall cook for you. Here: my Golden Ladle.'),
                            tellraw('@s', PREFIX + [T('The Chef joins you! ', CF_C, bold=True), T('Use the Golden Ladle to call him; sneak + use for his menu. Feed him Chef Fromage\'s feasts...', 'gray')]),
                            'tag @s add bm.kkmet', give('chef_ladle'), 'advancement grant @s only bm:story/chef_friend',
                            'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.2',
                            'execute as @e[type=minecraft:interaction,tag=bm.kkhere,limit=1] at @s run function bm:p186/enc/gone',
                            'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                            f'{sel_pet} run tag @s add {sel2}', f'execute unless entity @e[type=minecraft:wolf,tag={sel2}] unless function bm:p58/full run function bm:{pfx}/summon',
                            f'tag @e[tag={sel2}] remove {sel2}'])
    G.wjson('bm/advancement/story/chef_friend.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': 'bm:chef_ladle'}},
                        'title': T('The Chef Recommends', 'yellow'), 'description': T('Find Chef Fromage\'s old master - and win him over with Prime meat', 'gray'),
                        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    fn(f'admin/{W}', [give('chef_ladle'), 'tag @s add bm.kkmet', say("The Golden Ladle. (He turns up by Chef Fromage for anyone who's eaten all five Prime meats.)", CF_C)])
    fn(f'admin/{W}_meet', ['execute positioned ^ ^ ^3 run function bm:p186/enc/spawn',
                           tellraw('@s', PREFIX + [T('The Chef is standing in front of you. Right-click him holding a Prime cut.', 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T('  the Golden Ladle (the Chef: eat all five Prime meats, then visit Chef Fromage);', 'gray'),
                                                T(f' /function bm:admin/{W}_meet', 'yellow'), T(' meet him here', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = ['kill @e[type=minecraft:item_display,tag=bm.kkp]', 'kill @e[type=minecraft:interaction,tag=bm.kkenc]',
                                       'execute as @e[tag=bm.kkprime] run function bm:p186/unprime']
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second
