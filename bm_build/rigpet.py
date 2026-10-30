"""2.87: one builder for a rigkit follower - the Neighbor's machinery (phase187), lifted out so Queen Ava, Queen Pearl and Bloo
(phase189-191) share it: the host wolf and its rig of item displays, the state machine and its animation cycles, the summon
item (call, call over, sneak for the menu), the menu (sit / send home / call, ways, wardrobe, and the follower's own buttons),
the click box (right-click: sit / stand), fainting and its cooldown, the follow rules, the heist hooks and the Raid Contract.

A follower module gives a Cfg (below) and two hooks:
  abilities(G, X) -> lines run in the host's tick while it's free to act (X: the helpers - fn, S, go, hit, end, face, say...);
  encounter(G, X) -> builds how you meet it.
A FORM (Ava's ghost, Pearl's regal outfit): a score on the owner picks a suffix for every part's model ('_g', '_r'); the
dress function puts it on before the wardrobe's look (phase138's '_c<k>' rides on top of it)."""
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int, D
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


POS = {'her': 'her', 'him': 'his', 'it': 'its', 'them': 'their'}       # (the possessive for each pronoun; 2.94: 'them' - the Sky Buddies)


class Cfg:
    """W (the registry key), NAME, COL / LINE (name and speech colours), pfx ('p189'), ab (the tag stem: 'av' -> bm.avpet ...),
    q (the score stem: 'aq' -> bm.aqs ...), A (the art module), MENU (its bm.menu; buttons MENU+1..9), PET_HP, PET_CD (s),
    ITEM (the summon item's id), pron ('her' / 'him'), they ('she' / 'he'), CYCLE, DUR, QUIPS, HELLO (called over, summoned, sent home),
    SIT (stand line, sit line), FAINT (her last words), POWERS [(name, what)], INTRO [text parts], ATTRS (the host's attributes),
    FACE (phase95 mood -> the art's face or None), FORM (None, or (score, suffix, on-button label, off-button label, on line, off line)),
    BUTTONS [(n, label, tooltip, function)] (extra menu buttons on MENU + n), HIT (click-box size), SWIM_FACE, HEIST_WAIT_LINE,
    (2.94) BILLBOARD (None, or the parts' billboard: 'center' / 'vertical' - 2D sprites that always face you), SWAP (parts whose model
    each pose sets: A.model_name(part, pose) - a sprite's frame, a part's face), and pron 'them' / they 'they' (a plural follower)"""
    EXPR = ('happy', 'surprised', 'hurt', 'sleepy', 'blink', 'squint', 'serious')
    FORM = None
    FORM_PARTS = None            # (3.0: the parts whose model the form changes - None: every part; the rest keep theirs)
    FORM_WARDROBE = None         # (3.0: (code, colour, tooltip) - the form is a row of the follower's wardrobe (phase99.ROWS), not a menu button)
    BUTTONS = ()
    HIT = (0.9, 1.9)
    SCALE = 0.9
    ENC_FORM = False
    FORM_FX = []
    SUMMON_EXTRA = []
    ENC_PARTICLE = 'return 0'
    ENC_SHOW = None              # (3.0a: None, or f(G, X) -> (length, {tick: lines}, resume) - the encounter's entrance, build's enc/show)
    BILLBOARD = None
    SWAP = ()
    SWAP_START = False

    @staticmethod
    def POSE_EXTRA(name, psel):
        """(2.94) more lines for a pose's function - a sprite's frame"""
        return []


def register(C):
    """the module-level registries (as phase187 does them at import)"""
    W, pet = C.W, f'bm.{C.ab}pet'
    HOLD[C.ITEM] = f'bm:{C.pfx}/use'
    if C.FORM and C.FORM_WARDROBE:                                        # (3.0: the form as a row of its wardrobe - off / on)
        import phase99 as P99
        code, col, tip = C.FORM_WARDROBE
        P99.ROWS.setdefault(W, []).append((code, 'form', C.FORM[2], col, tip, [(None, 'off', 'gray'), (f'score @s {C.FORM[0]} matches 1', 'on', P99.GOLD)],
                                           f'{C.pfx}/form'))
    P46.COMPANIONS += f',tag=!{pet}'
    allies.ALLIES += [pet]
    if len(P89.BIT) < 30:
        P89.BIT[W] = 2 ** len(P89.BIT)
    else:                                                                 # (2.96: the first score is full - the second)
        P89.FCON2[W] = 2 ** len(P89.FCON2)
    P68.KINDS[W] = (max(v[0] for v in P68.KINDS.values()) + 1, C.ITEM, 'wolf', pet, f'{C.pfx}/summon', f'{C.pfx}/dismiss', f'bm.{C.ab}sel2', C.NAME, C.COL)
    if C.pron == 'him':
        P68.HE.add(W)
    elif C.pron == 'it':
        P68.IT.add(W)
    elif C.pron == 'them':
        P68.THEY.add(W)
    P98.CALLED.append((W, C.NAME, C.COL, 'wolf', pet, f'bm.{C.ab}sel2', f'bm.{C.ab}cd', f'{C.pfx}/try_summon', f'{C.pfx}/dismiss', f'{C.pfx}/recall', f'{C.pfx}/go'))
    P100.WHO[W] = ('wolf', pet)
    P100.VOICE[C.NAME] = (C.COL, C.LINE)
    FX.FOLK[W] = ('minecraft:wolf', pet, f'type=minecraft:item_display,tag=bm.{C.ab}p,tag=bm.{C.ab}p_head,tag=bm.{C.ab}p_pet,tag=!bm.{C.ab}fade', C.EXPR,
                  (60, 130), [('happy', 30, 5), ('blink', 4, 3)], ('happy', 40), 'hurt', 'surprised')
    item(f'fcontract_{W}', TOTEM, f'Raid Contract: {C.NAME}', C.COL, [(f'Use once: from then on {C.NAME}', 'blue'), ('will come into the vault with you.', 'blue')],
         model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
    HOLD[f'fcontract_{W}'] = f'bm:{C.pfx}/sign'
    figs0 = P134.figures

    def figures():
        F2 = figs0()
        F2[C.ITEM] = (C.NAME, P134._rigkit(C.A, C.A.POSES['idle_a'], C.A.RIG_SCALE))
        return F2
    P134.figures = figures


def rp(C, R, icon):
    """the resource pack: every part's model, the summon item's icon, the head's item definitions (a face per mood - and per form)"""
    import sys
    A = C.A
    for name, (tex, els) in A.models().items():
        R.HATS[name] = (tex, els)
    R.DISPLAY_3D_EXTRA = getattr(R, 'DISPLAY_3D_EXTRA', ()) + (A.PREFIX,)
    R.ICONS[C.ITEM] = icon
    forms = [''] + ([C.FORM[1]] if C.FORM else [])

    if A.PREFIX + 'head' not in A.models():                              # (2.97a: no plain head - its faces are another part's: rigface)
        return

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for sfx in forms:
            R2.wj(f'assets/bm/items/{A.PREFIX}head{sfx}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                                           'cases': [{'when': e, 'model': mdl(f'{A.PREFIX}head_x{C.FACE[e]}{sfx}' if C.FACE[e] else f'{A.PREFIX}head{sfx}')}
                                                                                     for e in C.EXPR], 'fallback': mdl(f'{A.PREFIX}head{sfx}')}})
    R.POST.insert(0, post)


def contract(C, G):
    """(generate_early) the Raid Contract on the Recruiter's books, its sign and the vault check"""
    from gen_dp import offer
    import phase103 as P103
    fn, title, tellraw = G.fn, G.title, G.tellraw
    W = C.W
    v = _verb(C)
    GP = [T('[', 'dark_gray'), T('Heist', '#ffcf40', bold=True), T('] ', 'dark_gray')]
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    Lr = G.FUNCS['p70/r/lobby/init']
    k_ = next(i for i, l in enumerate(Lr) if l.startswith('summon minecraft:villager') and 'bm.gvrec' in l and 'Recipes:[' in l)
    fo, bit = P89.fobj(W)
    signed = [f'scoreboard players operation #q bm.rng = @s {fo}', f'scoreboard players set #bit bm.rng {bit}',
              'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    fn(f'{C.pfx}/sign', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                         f'execute unless score @s {fo} matches 0.. run scoreboard players set @s {fo} 0'] + signed +
       [f'execute if score #q bm.rng matches 1 run return run ' + say(f"{C.NAME} {v('is', 'are')} already under contract.", 'gray'),
        f'scoreboard players add @s {fo} {bit}', f'clear @s *[minecraft:custom_data~{{bm:"fcontract_{W}"}}] 1',
        'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8',
        tellraw('@s', GP + [T('Signed! ', '#ffcf40', bold=True), T(C.NAME, C.COL, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
    fn(f'{C.pfx}/ok', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed +
       ['execute if score #q bm.rng matches 1 run return 1',
        tellraw('@s', GP + [T(C.NAME, C.COL), T(f" {v('needs', 'need')} {POS[C.pron]} ", 'gray'), T('Raid Contract', '#ffcf40'), T(' signed to come into the vault (the Recruiter in the den sells it).', 'gray')]),
        'return 0'])
    o = offer(('gutter_trophy', 1), (f'fcontract_{W}', 1), ('gutter_medallion', 3))
    Lr[k_] = Lr[k_].replace('Recipes:[', 'Recipes:[' + snbt(o) + ',', 1)
    P103.RECRUITER_OFFERS.append(o)


class X:
    """the helpers a follower's hooks get (filled in by build)"""


def _verb(C):
    """(2.94) a verb agreeing with the follower: v('needs', 'need')"""
    return (lambda one, many: many) if C.pron == 'them' else (lambda one, many: one)


def build(C, G, abilities, encounter):
    import phase28 as P28
    import phase73 as P73
    A, W, pfx, ab = C.A, C.W, C.pfx, C.ab
    v = _verb(C)
    fn, title, tellraw, give, PREFIX = G.fn, G.title, G.tellraw, G.give, G.PREFIX
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    holds = lambda i: f'*[minecraft:custom_data~{{bm:"{i}"}}]'
    foe = 'type=#bm:hostile,tag=!bm.npc,tag=!bm.wil_body'
    tick, fast, second = [], [], []
    S = lambda s: f'bm.{C.q}{s}'
    objs = [S(s) for s in ('s', 'fr', 'x', 'a', 'mc', 'rc', 'bc', 'gc', 'sc', 'sl', 'z', 'qp', 'hc', 'l', 'fg', 'ef', 'el', 'k', 'k2')] + [f'bm.{ab}cd']
    if C.FORM:
        objs.append(C.FORM[0])
    show = getattr(C, 'ENC_SHOW', None)                    # (3.0a: the encounter's entrance - Cfg.ENC_SHOW, below)
    if show:
        objs.append(S('sh'))
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    pet, me, sel, sel2, new, fade, own = (f'bm.{ab}{s}' for s in ('pet', 'me', 'sel', 'sel2', 'new', 'fade', 'own'))
    SP = A.RIG_SCALE
    UP = SP / 16
    csay = lambda txt, who='@s': title(who, 'actionbar', [T(f'{C.NAME}: ', C.COL, bold=True), T(txt, C.LINE)])
    cchat = lambda txt, who='@s': tellraw(who, [T(f'{C.NAME}: ', C.COL, bold=True), T(f'"{txt}"', C.LINE)])

    def psel(p=None):
        return f'@e[type=minecraft:item_display,tag={sel}' + (f',tag=bm.{ab}p_{p}]' if p else ']')
    sel_pet = f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid'
    face = lambda e, t: FX.face_cmd(W, e, t)
    bb = {'billboard': C.BILLBOARD} if C.BILLBOARD else {}
    # (2.94n) lit by the world, as Emma, Cecil and the older followers are: a fixed brightness kept them as bright in the dark
    # as at noon. Only one that shines by itself keeps it (Cfg.BRIGHT: the Arachno-Lantern's lit pumpkin); parts already out
    # lose it on their next second.
    lit = {'brightness': {'block': Int(C.BRIGHT), 'sky': Int(C.BRIGHT)}} if getattr(C, 'BRIGHT', None) else {}
    # (2.94z) ...and only the parts that shine (Cfg.BRIGHT_PARTS: the Lantern's pumpkin head, not its spider body); all, if unsaid
    lit_parts = getattr(C, 'BRIGHT_PARTS', None)
    lit_of = lambda p: lit if lit and (lit_parts is None or p in lit_parts) else {}
    xt = getattr(A, 'EXTRA_TAGS', {})
    # (2.97a: SWAP_START - a swapped part starts out as its idle model: one whose every model is a shape or a face has no plain one)
    start = (lambda p: A.model_name(p, A.POSES['idle_a']) if p in C.SWAP else None) if getattr(C, 'SWAP_START', False) else (lambda p: None)
    disp = lambda tags: [f'summon minecraft:item_display ~ ~ ~ {RF.part_nbt(A, p, [f"bm.{ab}p", f"bm.{ab}p_{p}"] + xt.get(p, []) + tags, SP, model=start(p), scale0=True, extra=dict(view_range=F(1.6), **lit_of(p), shadow_radius=F(0.5 if p == "body" else 0.0), shadow_strength=F(0.5), **bb))}'
                         for p in A.PARTS]
    rig = disp([f'bm.{ab}p_pet', new])
    fn(f'{pfx}/place', RF.place(A, UP, psel))
    burst = C.BURST
    fn(f'{pfx}/burst', burst)
    RF.cycles(fn, pfx, C.CYCLE, S('fr'), S('s'), lambda p: f'{pfx}/pose/{p}', tw=dict(G=G, A=A, S=SP, sel=psel, swap=C.SWAP) if getattr(C, 'TWEEN', True) else None)
    for name in {p for _per, frames in C.CYCLE.values() for _t, p in frames}:
        fn(f'{pfx}/pose/{name}', RF.pose(A, A.POSES[name], SP, C.DUR.get(name, 6), psel, swap=C.SWAP, keep=True) + C.POSE_EXTRA(name, psel))
    G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{n} bm.rng {n}' for n in RF.periods(C.CYCLE)]
    fn(f'{pfx}/grow', [f'execute as {psel(p)} run data merge entity @s {{start_interpolation:-1,interpolation_duration:0,transformation:{{scale:[{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f,{SP * A.PART_K.get(p, 1.0):.4f}f]}}}}'
                       for p in A.PARTS if not (hasattr(A, 'HIDDEN') and A.HIDDEN(p, A.POSES['idle_a']))] + [f'function bm:{pfx}/pose/idle_a'])
    fn(f'{pfx}/state', [f'execute if score @s {S("sl")} matches 1.. run return run scoreboard players set #st bm.rng 6',
                        f'execute if score @s {S("x")} matches 1.. run return run scoreboard players operation #st bm.rng = @s {S("a")}',
                        # (2.96c: phase234 - riding Bender (16; he seats them), curled up with him at night (17))
                        'execute if entity @s[tag=bm.rdr] run return run scoreboard players set #st bm.rng 16',
                        'execute if entity @s[tag=bm.cdl] run return run scoreboard players set #st bm.rng 17',
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
    anchor = 'head' if 'head' in A.PARTS else A.PARTS[0]                     # (2.97a: the part whose loss means the rig is gone - a head, or its body)
    idle_fight = f'unless score @s {S("x")} matches 1.. unless data entity @s {{Sitting:1b}} unless entity @s[tag=bm.rdr] unless entity @s[tag=bm.cdl]'

    # ---- the helpers for the follower's own abilities
    hurt_by = f'@e[type=minecraft:wolf,tag={me},limit=1]'
    fn(f'{pfx}/hurt', [f'execute store result storage bm:tmp {pfx}.d int 1 run scoreboard players get #pd bm.rng', f'function bm:{pfx}/dmg with storage bm:tmp {pfx}'])
    fn(f'{pfx}/dmg', [f'$damage @s $(d) minecraft:mob_attack by {hurt_by}'])
    X.fn, X.S, X.say, X.csay, X.cchat, X.face, X.foe, X.pfx, X.pet, X.me, X.own, X.sel2 = fn, S, say, csay, cchat, face, foe, pfx, pet, me, own, sel2
    X.idle_fight, X.tellraw, X.title, X.give, X.PREFIX, X.sel_pet, X.second, X.tick, X.fast = idle_fight, tellraw, title, give, PREFIX, sel_pet, second, tick, fast
    X.go = lambda a, x, cdo, cd, extra=(): [f'scoreboard players set @s {S("a")} {a}', f'scoreboard players set @s {S("x")} {x}', f'scoreboard players set @s {S(cdo)} {cd}'] + list(extra)
    X.hit = lambda d: [f'tag @s add {me}', f'scoreboard players set #pd bm.rng {d}']
    X.end = [f'tag @s remove {me}', f'function bm:{pfx}/blow']
    X.holds = holds
    ab_lines = abilities(G, X)
    fn(f'{pfx}/tick', ['scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'execute unless entity {psel(anchor)} run function bm:{pfx}/rerig',
                       f'execute if score @s {S("x")} matches 1.. run function bm:{pfx}/act_tick'] +
       [f'execute if score @s {S(o)} matches 1.. run scoreboard players remove @s {S(o)} 1' for o in ('mc', 'rc', 'bc', 'gc', 'sc', 'sl')] +
       ab_lines +
       [f'function bm:{pfx}/state',
        f'execute if score #st bm.rng = @s {S("s")} run scoreboard players add @s {S("fr")} 1',
        f'execute unless score #st bm.rng = @s {S("s")} run scoreboard players set @s {S("fr")} 0',
        f'scoreboard players operation @s {S("s")} = #st bm.rng',
        f'function bm:{pfx}/anim',
        f'execute on owner run tag @s add {own}',
        f'execute unless entity @s[tag=bm.rdr] run function bm:{pfx}/places',
        f'function bm:{pfx}/box',
        f'tag @a[tag={own}] remove {own}', f'tag @e[tag={sel}] remove {sel}'])
    # (2.96c: placed where it stands - unless it rides Bender: then he seats it, phase234)
    fn(f'{pfx}/places', [f'execute if score @s {S("s")} matches 7..13 if entity @e[{foe},distance=..18] facing entity @e[{foe},distance=..18,sort=nearest,limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                         f'execute if score @s {S("s")} matches 7..13 unless entity @e[{foe},distance=..18] rotated as @s rotated ~ 0 run return run function bm:{pfx}/place',
                         f'execute if score @s {S("s")} matches 0 run return run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 4 run return run function bm:{pfx}/face_you',
                         f'execute if score @s {S("s")} matches 6 run return run function bm:{pfx}/face_you', f'execute if score @s {S("s")} matches 14 run return run function bm:{pfx}/face_you',
                         f'execute if score @s {S("s")} matches 1..3 rotated as @s rotated ~ 0 run return run function bm:{pfx}/place',
                         f'execute if score @s {S("s")} matches 10 rotated as @s rotated ~ 0 run return run function bm:{pfx}/place',
                         f'execute if score @s {S("s")} matches 17 rotated as @s rotated ~ 0 run return run function bm:{pfx}/place'])
    fn(f'{pfx}/face_you', [f'execute if entity @a[tag={own},distance=2.5..14] facing entity @a[tag={own},limit=1] feet rotated ~ 0 run return run function bm:{pfx}/place',
                           f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place'])
    fn(f'{pfx}/blow', [f'scoreboard players add @s {S("qp")} 1', f'execute if score @s {S("qp")} matches 7.. run function bm:{pfx}/quip'])
    quips = C.QUIPS
    fn(f'{pfx}/quip', [f'scoreboard players set @s {S("qp")} 0', f'execute store result score #r bm.rng run random value 1..{len(quips)}'] +
       [f'execute if score #r bm.rng matches {n + 1} on owner if entity @s[distance=..20,tag=!bm.hush] run ' + csay(q) for n, q in enumerate(quips)] + face('happy', 30))

    # ---- the summon item: call, call over, sneak for the menu
    def pet_nbt():
        return {'Tags': [pet, new, 'bm.seen'], 'Silent': B(1), 'PersistenceRequired': B(1), 'Health': F(C.PET_HP),
                'CustomName': T(C.NAME, C.COL, bold=True), 'CustomNameVisible': B(0),
                'attributes': [{'id': f'minecraft:{a}', 'base': D(v)} for a, v in dict(C.ATTRS, max_health=C.PET_HP, scale=C.SCALE).items()],
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
    fn(f'{pfx}/recall', [f'tp @e[type=minecraft:wolf,tag={sel2},limit=1] @s', f'data modify entity @e[type=minecraft:wolf,tag={sel2},limit=1] Sitting set value 0b',
                         f'function bm:{pfx}/burst', csay(C.HELLO[0])])
    fn(f'{pfx}/try_summon', [f'execute if score @s bm.{ab}cd matches 1.. store result score #m bm.rng run scoreboard players get @s bm.{ab}cd',
                             f'execute if score @s bm.{ab}cd matches 1.. run scoreboard players add #m bm.rng 59',
                             f'execute if score @s bm.{ab}cd matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             f'execute if score @s bm.{ab}cd matches 1.. run return run ' + title('@s', 'actionbar', [T(f"{C.NAME} {v('is', 'are')} still recovering: about ", 'gray'),
                                                                                                                       {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'execute unless function bm:{pfx}/ok run return run ' + say(f"{C.NAME} won't come here."),
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
                              f'execute at @e[type=minecraft:item_display,tag={sel},tag=bm.{ab}p_body,limit=1] run function bm:{pfx}/burst',
                              f'tag @e[tag={sel}] remove {sel}', f'tag @e[tag={new},distance=..4] remove {new}', csay(C.HELLO[1])] + C.SUMMON_EXTRA)
    fn(f'{pfx}/tough', [f'attribute @s minecraft:max_health base set {C.PET_HP}', f'data modify entity @s Health set value {C.PET_HP}f',
                        f'attribute @s minecraft:armor base set {C.ATTRS.get("armor", 4)}', f'attribute @s minecraft:attack_damage base set {C.ATTRS.get("attack_damage", 3)}',
                        f'attribute @s minecraft:movement_speed base set {C.ATTRS.get("movement_speed", 0.3)}'])
    fn(f'{pfx}/rig_here', rig + [f'tp @e[type=minecraft:item_display,tag={new},distance=..1] ~ ~ ~ ~ 0'])
    fn(f'{pfx}/rerig', [f'kill @e[type=minecraft:item_display,tag={sel}]', f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/rig_here',
                        f'scoreboard players operation @e[type=minecraft:item_display,tag={new},distance=..2] bm.pid = #me bm.pid',
                        f'tag @e[type=minecraft:item_display,tag={new},distance=..2] add {sel}', f'tag @e[type=minecraft:item_display,tag={new},distance=..2] remove {new}',
                        f'function bm:{pfx}/dress', f'function bm:{pfx}/grow', f'scoreboard players set @s {S("s")} -1'])
    # dress: the form's models first (every part: its base model, or its form's), then the wardrobe's look over it
    cos = f'bm.cos{ab}'
    form_lines = []
    if C.FORM:
        fsc, fsfx = C.FORM[0], C.FORM[1]
        form_lines = ['scoreboard players set #fm bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #fm bm.rng = @s {fsc}']
        for p in (C.FORM_PARTS or A.PARTS):
            form_lines += [f'execute if score #fm bm.rng matches 0 as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{A.PREFIX}{p}"',
                           f'execute if score #fm bm.rng matches 1 as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{A.PREFIX}{p}{fsfx}"']
        if hasattr(A, 'HIDDEN'):                                                           # (a part one form hides - Pearl's cape)
            for p in A.PARTS:
                h0, h1 = A.HIDDEN(p, A.POSES['idle_a']), A.HIDDEN(p, A.POSES.get('idle_a' + fsfx, A.POSES['idle_a']))
                if h0 != h1:
                    sc = SP * A.PART_K.get(p, 1.0)
                    form_lines += [f'execute if score #fm bm.rng matches {0 if h0 else 1} as {psel(p)} run data merge entity @s {{transformation:{{scale:[0f,0f,0f]}}}}',
                                   f'execute if score #fm bm.rng matches {1 if h0 else 0} as {psel(p)} run data merge entity @s {{transformation:{{scale:[{sc:.4f}f,{sc:.4f}f,{sc:.4f}f]}}}}']
    fn(f'{pfx}/dress', form_lines + ['scoreboard players set #wk bm.rng 0', f'execute as @a if score @s bm.pid = #me bm.pid run scoreboard players operation #wk bm.rng = @s {cos}',
                                     f'execute as @e[type=minecraft:item_display,tag={sel}] run function bm:p138/sfx'])
    fn(f'p99/{W}_now', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #has bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/now2',
                        'execute if score #has bm.rng matches 0 run return run ' + say(f"{C.NAME} {v('isn', 'aren')}'t with you - {C.they}'ll wear it next time.", C.COL)])
    fn(f'{pfx}/now2', ['scoreboard players set #has bm.rng 1', 'scoreboard players operation #me bm.pid = @s bm.pid',
                       f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                       f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}', 'particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.02 20'])
    fn(f'{pfx}/dismiss', [f'execute as @e[type=minecraft:wolf,tag={sel2}] at @s run function bm:{pfx}/fade',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] on passengers run kill @s[type=!minecraft:player]',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run data remove entity @s Owner',
                          f'execute as @e[type=minecraft:wolf,tag={sel2}] run tp @s ~ -500 ~', f'kill @e[type=minecraft:wolf,tag={sel2}]', csay(C.HELLO[2])])
    fn(f'{pfx}/home', [f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid run tag @s add {sel2}',
                       f'execute if entity @e[tag={sel2}] run function bm:{pfx}/dismiss', f'tag @e[tag={sel2}] remove {sel2}'])
    # ---- the menu (sneak + use)
    M = C.MENU
    poss = C.NAME + ("'" if C.NAME.endswith('s') else "'s")              # (2.94: the Sky Buddies' ways)
    pdlg = P28.multi([T(f"{poss.upper()} WAYS", C.COL, bold=True)], [P28.body([T(n, C.COL, bold=True), T(f' - {d}.', 'gray')], 340) for n, d in C.POWERS],
                     [P28.btn([T('« Back', 'gray')], M + 5, width=150)], columns=1, exit_label='Close')
    fn(f'{pfx}/powers', [f'scoreboard players set @s bm.menu {M}', f'dialog show @s {snbt(pdlg)}'])
    extra = [P28.btn(T(lbl, C.COL, bold=True), M + n, width=150, tooltip=T(tip, 'gray')) for n, lbl, tip, _f in C.BUTTONS]
    form_btn = []
    if C.FORM and not C.FORM_WARDROBE:
        form_btn = [P28.btn(T(C.FORM[2], C.COL, bold=True), M + 3, width=150, tooltip=T(C.FORM[6], 'gray'))]
    dlg = lambda out: P28.multi([T(ITEMS[C.ITEM]['name'], C.COL, bold=True)], [P28.body(C.INTRO, 300)],
                                ([P28.btn(T('Sit / follow', 'white', bold=True), M + 1, width=150), P28.btn(T(f'Send {C.pron} home', 'gray'), M + 9, width=150)] if out else
                                 [P28.btn(T(f'Call for {C.NAME}', C.COL, bold=True), M + 8, width=150)]) + form_btn + extra +
                                [P28.btn(T(f"{poss} ways", C.COL, bold=True), M + 4, width=150, tooltip=T(f"What {C.they} {v('does', 'do')} - and how.", 'gray')),
                                 P28.btn(T('Wardrobe', C.COL, bold=True), M + 2, width=150, tooltip=T(f'{POS[C.pron].capitalize()} looks - and {POS[C.pron]} aura, if you have it.', 'gray'))],
                                columns=2, exit_label='Close')
    fn(f'{pfx}/menu', [f'scoreboard players set @s bm.menu {M}',
                       f'execute if entity @e[type=minecraft:wolf,tag={sel2}] run return run dialog show @s {snbt(dlg(True))}',
                       f'dialog show @s {snbt(dlg(False))}'])
    menu_form = bool(C.FORM) and not C.FORM_WARDROBE                       # (a wardrobe form: its row is routed by phase99)
    codes = [1, 2, 4, 5, 8, 9] + ([3] if menu_form else []) + [n for n, *_r in C.BUTTONS]
    G.FUNCS['p28/act'] += [f'execute if score #act bm.pay matches {M + n} run return run function bm:{pfx}/act' for n in codes]
    fn(f'{pfx}/act', [f'execute unless score @s bm.menu matches {M} run return run function bm:p28/stale',
                      f'execute if score #act bm.pay matches {M + 2} run return run function bm:p119/plain/{W}',
                      f'execute if score #act bm.pay matches {M + 4} run return run function bm:{pfx}/powers'] +
       ([f'execute if score #act bm.pay matches {M + 3} run return run function bm:{pfx}/form'] if menu_form else []) +
       [f'execute if score #act bm.pay matches {M + n} run return run function bm:{f_}' for n, _l, _t, f_ in C.BUTTONS] +
       ['scoreboard players operation #me bm.pid = @s bm.pid', f'{sel_pet} run tag @s add {sel2}',
        f'execute if score #act bm.pay matches {M + 5} run function bm:{pfx}/menu',
        f'execute if score #act bm.pay matches {M + 8} unless entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/try_summon',
        f'execute if score #act bm.pay matches {M + 8} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/recall',
        f'execute if score #act bm.pay matches {M + 1} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/sit',
        f'execute if score #act bm.pay matches {M + 9} if entity @e[type=minecraft:wolf,tag={sel2}] run function bm:{pfx}/dismiss',
        f'tag @e[tag={sel2}] remove {sel2}'])
    if C.FORM:
        fsc = C.FORM[0]
        fn(f'{pfx}/form', ['execute unless score @s ' + fsc + ' matches 0..1 run scoreboard players set @s ' + fsc + ' 0',
                           f'execute store success score #f0 bm.rng if score @s {fsc} matches 1',
                           f'execute if score #f0 bm.rng matches 1 run scoreboard players set @s {fsc} 0',
                           f'execute if score #f0 bm.rng matches 0 run scoreboard players set @s {fsc} 1',
                           f'execute if score @s {fsc} matches 1 run ' + csay(C.FORM[4]), f'execute if score @s {fsc} matches 0 run ' + csay(C.FORM[5]),
                           'scoreboard players operation #me bm.pid = @s bm.pid',
                           f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/form2',
                           # (3.0e: the menu shown again knows the follower is out by {sel2} - act returns into here before it
                           #  tags them, so tag them here: else the menu came back as "Call for ..." with them beside you)
                           f'{sel_pet} run tag @s add {sel2}',
                           f'function bm:p99/menu/{W}' if C.FORM_WARDROBE else f'function bm:{pfx}/menu',
                           f'tag @e[tag={sel2}] remove {sel2}'])
        fn(f'{pfx}/form2', ['scoreboard players operation #me bm.pid = @s bm.pid',
                            f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run tag @s add {sel}',
                            f'function bm:{pfx}/dress', f'tag @e[tag={sel}] remove {sel}'] + C.FORM_FX)
    tw = f'@e[type=minecraft:wolf,tag={sel2},limit=1]'
    fn(f'{pfx}/sit', [f'execute store success score #s0 bm.rng if data entity {tw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {tw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {tw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + csay(C.SIT[0]), 'execute if score #s0 bm.rng matches 0 run ' + csay(C.SIT[1])])
    # ---- the click box: right-click - sit / stand
    hit_tag, clk = f'bm.{ab}hit', f'bm.{ab}clk'
    fn(f'{pfx}/box', ['execute if entity @s[tag=bm.ffpet] run return 0', f'execute if function bm:{pfx}/has_hit run return 0',
                      f'summon minecraft:interaction ~ ~ ~ {{Tags:["{hit_tag}","bm.{ab}hnew"],width:{C.HIT[0]}f,height:{C.HIT[1]}f,response:1b}}',
                      f'ride @e[type=minecraft:interaction,tag=bm.{ab}hnew,limit=1,sort=nearest] mount @s', f'tag @e[tag=bm.{ab}hnew] remove bm.{ab}hnew'])
    fn(f'{pfx}/has_hit', [f'execute on passengers if entity @s[type=minecraft:interaction,tag={hit_tag}] run return 1', 'return 0'])
    second.append(f'execute as @e[type=minecraft:interaction,tag={hit_tag}] unless function bm:p20/frog/has_vehicle run kill @s')
    fast += [f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s interaction run function bm:{pfx}/click',
             f'execute as @e[type=minecraft:interaction,tag={hit_tag}] if data entity @s attack run data remove entity @s attack']
    fn(f'{pfx}/click', [f'execute on vehicle run tag @s add {clk}', f'execute on target at @s run function bm:{pfx}/who', f'tag @e[tag={clk}] remove {clk}',
                        'data remove entity @s interaction'])
    cw = f'@e[type=minecraft:wolf,tag={clk},limit=1]'
    fn(f'{pfx}/who', [f'execute if score @s {S("hc")} matches 1.. run return 0', f'scoreboard players set @s {S("hc")} 10', 'scoreboard players operation #me bm.pid = @s bm.pid',
                      f'execute unless score {cw} bm.pid = #me bm.pid run return run ' + csay(C.NOT_YOURS),
                      f'execute store success score #s0 bm.rng if data entity {cw} {{Sitting:1b}}',
                      f'execute if score #s0 bm.rng matches 1 run data modify entity {cw} Sitting set value 0b',
                      f'execute if score #s0 bm.rng matches 0 run data modify entity {cw} Sitting set value 1b',
                      'execute if score #s0 bm.rng matches 1 run ' + csay(C.SIT[0]), 'execute if score #s0 bm.rng matches 0 run ' + csay(C.SIT[1])])
    tick.append(f'scoreboard players remove @a[scores={{{S("hc")}=1..}}] {S("hc")} 1')
    G.FUNCS['admin/uninstall'].insert(0, f'kill @e[type=minecraft:interaction,tag={hit_tag}]')
    # ---- fainting
    tick += [f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=bm.{ab}p_body,tag=!{fade}] at @s run function bm:{pfx}/check',
             f'scoreboard players remove @e[type=minecraft:item_display,tag={fade}] {S("l")} 1',
             f'kill @e[type=minecraft:item_display,tag={fade},scores={{{S("l")}=..0}}]']
    fn(f'{pfx}/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #al bm.rng 0',
                        f'execute as @e[type=minecraft:wolf,tag={pet},distance=..16] if score @s bm.pid = #me bm.pid run scoreboard players set #al bm.rng 1',
                        f'execute if score #al bm.rng matches 1 run return run scoreboard players set @s {S("z")} 0',
                        f'scoreboard players add @s {S("z")} 1', f'execute if score @s {S("z")} matches 4.. run function bm:{pfx}/fell'])
    fn(f'{pfx}/fell', [f'function bm:{pfx}/fade', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:{pfx}/cooldown'])
    fn(f'{pfx}/cooldown', [f'scoreboard players set @s bm.{ab}cd {C.PET_CD}',
                           tellraw('@s', PREFIX + [T(f"{C.NAME} {v('faints', 'faint')}! ", C.COL, bold=True), T(f'"{C.FAINT}" ', C.LINE),
                                                   T(f"{C.they.capitalize()} {v('needs', 'need')} {C.PET_CD // 60} minutes before {C.they} can come back.", "gray")])])
    fn(f'{pfx}/fade', [f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p_pet,tag=!{fade}] if score @s bm.pid = #me bm.pid run function bm:{pfx}/fade1'] + burst +
       [C.FADE_SOUND])
    fn(f'{pfx}/fade1', [f'tag @s add {fade}', f'scoreboard players set @s {S("l")} 3',
                        f'data merge entity @s[type=minecraft:item_display] {{brightness:{{block:15,sky:15}},Glowing:1b,glow_color_override:{int(C.COL[1:], 16)}}}'])
    second.append(f'scoreboard players remove @a[scores={{bm.{ab}cd=1..}}] bm.{ab}cd 1')
    if not lit or lit_parts is not None:
        keep = ''.join(f',tag=!bm.{ab}p_{p}' for p in (lit_parts or ()))
        second.append(f'execute as @e[type=minecraft:item_display,tag=bm.{ab}p,tag=!bm.rplit,tag=!{fade}{keep}] run function bm:{pfx}/unlit')
        fn(f'{pfx}/unlit', ['data remove entity @s brightness', 'tag @s add bm.rplit'])
    G.FUNCS['p62/died'].insert(-1, f'execute as @e[type=minecraft:wolf,tag={pet}] if score @s bm.pid = #me bm.pid at @s run function bm:{pfx}/go')
    fn(f'{pfx}/go', ['scoreboard players add #gone bm.rng 1', f'function bm:{pfx}/fade', 'execute on passengers run kill @s[type=!minecraft:player]',
                     'data remove entity @s Owner', 'tp @s ~ -500 ~', 'kill @s'])
    P73.follow_rules(G, (W, 'wolf', pet, C.ITEM, f'{pfx}/go', C.NAME, S('fg'), f'{pfx}/summon_here'), second)
    L = G.FUNCS[f'p73/fol/{W}']
    j = next(i for i, l in enumerate(L) if ' if items entity ' in l)
    L.insert(j, 'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run scoreboard players set @s bm.fmis 0')
    G.FUNCS['p58/count'][-1:-1] = [f'execute as @e[type=minecraft:wolf,tag={pet}] on owner if entity @s[tag=bm.fcme] run scoreboard players add #fc bm.rng 1']
    G.FUNCS['p57/pulse'] += [l.replace('tag=bm.celipet', f'tag={pet}') for l in G.FUNCS['p57/pulse'] if 'tag=bm.celipet' in l]
    far = G.FUNCS[f'p73/fol/{W}_far']
    assert far[0] == f'function bm:{pfx}/go', far[0]
    far.insert(0, f'execute if entity @a[tag=bm.fown,tag=bm.gvp] run return run function bm:p103/fol/wait_{W}')
    fn(f'p103/fol/wait_{W}', [f'tag @a[tag=bm.fown] add bm.ow_{W}', f'function bm:{pfx}/go',
                              tellraw('@a[tag=bm.fown]', PREFIX + [T(f"{C.NAME} {v('waits', 'wait')} outside the vault", C.COL), T(' - your Raid Crew answers inside. ', 'gray'),
                                                                   T("(Back with you when you're home.)", 'dark_gray')]), 'tag @a remove bm.fown'])
    fn(f'p103/fol/back_{W}', [f'tag @s remove bm.ow_{W}', f'function bm:{pfx}/try_summon'])
    G.FUNCS['p103/fol/tick'].append(f'execute if entity @s[tag=bm.ow_{W}] run function bm:p103/fol/back_{W}')

    # ---- the encounter's shared pieces: a standing rig with a click box (enc/spawn), posed (enc/tick), gone after 10 minutes
    X.disp, X.psel = disp, psel
    enc = f'bm.{ab}enc'
    enc_hit = snbt({'Tags': [enc, f'bm.{ab}enew'], 'width': F(C.HIT[0]), 'height': F(C.HIT[1]), 'response': B(1)})
    # (3.0a) THE ENTRANCE (Cfg.ENC_SHOW(G, X) -> (length, {tick: lines}, resume)): the rig comes in at scale 0 and a few seconds'
    # show builds it (enc/show, from enc/tick: each tick's lines run as the click box, at it, turned to face you as it was placed,
    # the rig's parts tagged {sel}). Meanwhile the box won't talk (a click is dropped); at the end the rig faces you, the idle
    # cycle picks up at `resume`, and whatever props the show summoned (tag bm.<ab>shp) go. Walk off mid-show: enc/gone takes
    # them with the rest, and a prop left without its box is swept within the second.
    shw, prop = S('sh'), f'bm.{ab}shp'
    X.prop = prop
    fn(f'{pfx}/enc/spawn', [f'summon minecraft:interaction ~ ~ ~ {enc_hit}'] + disp([f'bm.{ab}encp', f'bm.{ab}enew']) +
       [f'execute as @e[type=minecraft:item_display,tag=bm.{ab}enew,distance=..1] run tag @s add {sel}',
        f'execute facing entity @p feet rotated ~ 0 run function bm:{pfx}/place', f'function bm:{pfx}/enc/look'] + ([] if show else [f'function bm:{pfx}/grow']) +
       [f'tag @e[tag={sel}] remove {sel}',
        f'scoreboard players set @e[type=minecraft:interaction,tag=bm.{ab}enew,distance=..1] {S("el")} 0'] +
       ([f'execute facing entity @p feet rotated ~ 0 run tp @e[type=minecraft:interaction,tag=bm.{ab}enew,distance=..1,limit=1] ~ ~ ~ ~ 0',
         f'scoreboard players set @e[type=minecraft:interaction,tag=bm.{ab}enew,distance=..1] {shw} 1'] if show else []) +
       [f'tag @e[tag=bm.{ab}enew,distance=..1] remove bm.{ab}enew'])
    enc_look = []
    if C.FORM and C.ENC_FORM:                                                              # (Ava's ghost rises as a ghost)
        enc_look = [f'execute as {psel(p)} run data modify entity @s item.components."minecraft:item_model" set value "bm:{A.PREFIX}{p}{C.FORM[1]}"' for p in A.PARTS]
    fn(f'{pfx}/enc/look', enc_look + ['return 0'])
    tick.append(f'execute as @e[type=minecraft:interaction,tag={enc}] at @s run function bm:{pfx}/enc/tick')
    ep = C.ENC_POSES
    fn(f'{pfx}/enc/tick', ([f'execute if score @s {shw} matches 1.. run return run function bm:{pfx}/enc/show'] if show else []) + [f'scoreboard players add @s {S("ef")} 1', f'scoreboard players operation #f bm.rng = @s {S("ef")}', 'scoreboard players operation #f bm.rng %= #80 bm.rng',
                           f'execute as @e[type=minecraft:item_display,tag=bm.{ab}encp,distance=..5] run tag @s add {sel}'] +
       [f'execute if score #f bm.rng matches {t} run function bm:{pfx}/pose/{p}' for t, p in ep] +
       [f'execute if score #f bm.rng matches 0 if entity @a[distance=..8,gamemode=!spectator] facing entity @p[distance=..8,gamemode=!spectator] feet rotated ~ 0 run function bm:{pfx}/place',
        C.ENC_PARTICLE.replace('return 0', 'scoreboard players set #np bm.rng 0'), f'tag @e[tag={sel}] remove {sel}'])
    G.FUNCS['load'][-1:-1] = ['scoreboard players set #80 bm.rng 80']
    second.append(f'execute as @e[type=minecraft:interaction,tag={enc}] at @s run function bm:{pfx}/enc/sec')
    fn(f'{pfx}/enc/sec', [f'scoreboard players add @s {S("el")} 1', f'execute unless entity @a[distance=..48] run return run function bm:{pfx}/enc/gone',
                          f'execute if score @s {S("el")} matches 600.. run return run function bm:{pfx}/enc/gone'])
    # (2.88: every part, wherever its joint is - the tall ones' heads stood more than 2 blocks up, and were left behind)
    fn(f'{pfx}/enc/gone', [f'kill @e[type=minecraft:item_display,tag=bm.{ab}encp,distance=..8]'] + ([f'kill @e[tag={prop},distance=..16]'] if show else []) +
       ['particle minecraft:poof ~ ~1 ~ 0.4 0.8 0.4 0.03 20', 'kill @s'])
    if show:
        length, keys, resume = show(G, X)
        assert all(1 <= t <= length for t in keys), (W, sorted(keys))
        fn(f'{pfx}/enc/show', [f'scoreboard players add @s {shw} 1', f'scoreboard players operation #f bm.rng = @s {shw}',
                               f'execute as @e[type=minecraft:item_display,tag=bm.{ab}encp,distance=..6] run tag @s add {sel}'] +
           [f'execute if score #f bm.rng matches {t + 1} rotated as @s run function bm:{pfx}/enc/show/{t}' for t in sorted(keys)] +
           [f'execute if score #f bm.rng matches {length + 1}.. rotated as @s run function bm:{pfx}/enc/show_end', f'tag @e[tag={sel}] remove {sel}'])
        for t, lines in keys.items():
            fn(f'{pfx}/enc/show/{t}', lines)
        fn(f'{pfx}/enc/show_end', [f'scoreboard players set @s {shw} 0', f'scoreboard players set @s {S("ef")} {resume - 1}', f'kill @e[tag={prop},distance=..16]',
                                   f'execute as @e[type=minecraft:item_display,tag={sel}] run data merge entity @s[type=minecraft:item_display] {{teleport_duration:2}}',
                                   f'execute as @e[type=minecraft:item_display,tag={sel}] run data remove entity @s item.components."minecraft:custom_model_data"',
                                   f'execute if entity @a[distance=..16,gamemode=!spectator] facing entity @p[distance=..16,gamemode=!spectator] feet rotated ~ 0 run tp @s ~ ~ ~ ~ 0',
                                   f'execute rotated as @s rotated ~ 0 run function bm:{pfx}/place', 'data remove entity @s interaction', 'data remove entity @s attack'])
        second.append(f'execute as @e[tag={prop}] at @s unless entity @e[type=minecraft:interaction,tag={enc},distance=..16] run kill @s')
        G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[tag={prop}]']
    fast += [f'execute as @e[type=minecraft:interaction,tag={enc}] if data entity @s interaction at @s run function bm:{pfx}/enc/click',
             f'execute as @e[type=minecraft:interaction,tag={enc}] if data entity @s attack at @s run data remove entity @s attack']
    fn(f'{pfx}/enc/click', ([f'execute if score @s {shw} matches 1.. run return run data remove entity @s interaction'] if show else []) + [f'tag @s add bm.{ab}here', f'execute on target run function bm:{pfx}/enc/talk', f'tag @s remove bm.{ab}here', 'data remove entity @s interaction'])
    X.here = f'@e[type=minecraft:interaction,tag=bm.{ab}here,limit=1]'
    # (the recruit's shared tail: met, the item, the advancement, he/she comes along)
    fn(f'{pfx}/enc/joined', [f'tag @s add bm.{ab}met', give(C.ITEM), f'advancement grant @s only bm:story/{W}_friend',
                             'playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.7 1.2',
                             tellraw('@s', PREFIX + [T(f"{C.NAME} {v('joins', 'join')} you! ", C.COL, bold=True), T(f'Use {ITEMS[C.ITEM]["name"]} to call {C.pron}; sneak + use for {POS[C.pron]} menu.', 'gray')]),
                             f'execute as {X.here} at @s run function bm:{pfx}/enc/gone',
                             'execute unless score @s bm.pid matches 1.. run function bm:p21/pid', 'scoreboard players operation #me bm.pid = @s bm.pid',
                             f'{sel_pet} run tag @s add {sel2}', f'execute unless entity @e[type=minecraft:wolf,tag={sel2}] unless function bm:p58/full at @s run function bm:{pfx}/summon',
                             f'tag @e[tag={sel2}] remove {sel2}'])
    G.wjson(f'bm/advancement/story/{W}_friend.json', {'parent': 'bm:story/root', 'criteria': {'done': {'trigger': 'minecraft:impossible'}},
            'display': {'icon': {'id': TOTEM, 'components': {'minecraft:item_model': f'bm:{C.ITEM}'}},
                        'title': T(C.ADV[0], 'yellow'), 'description': T(C.ADV[1], 'gray'),
                        'frame': 'goal', 'show_toast': True, 'announce_to_chat': True, 'hidden': True}})
    encounter(G, X)
    fn(f'admin/{W}', [give(C.ITEM), f'tag @s add bm.{ab}met', say(f"{ITEMS[C.ITEM]['name']}. ({C.ADMIN_HINT})", C.COL)])
    fn(f'admin/{W}_meet', [f'execute positioned ^ ^ ^3 run function bm:{pfx}/enc/spawn',
                           tellraw('@s', PREFIX + [T(f"{C.NAME} {v('is', 'are')} standing in front of you. {C.MEET_HINT}", 'gray')])])
    G.FUNCS['admin/help'].append(tellraw('@s', [T(f'/function bm:admin/{W}', 'yellow'), T(f"  {ITEMS[C.ITEM]['name']};", 'gray'),
                                                T(f' /function bm:admin/{W}_meet', 'yellow'), T(f' meet {C.pron} here', 'gray')]))
    G.FUNCS['admin/uninstall'][0:0] = [f'kill @e[type=minecraft:item_display,tag=bm.{ab}p]', f'kill @e[type=minecraft:interaction,tag={enc}]']
    G.FUNCS['tick'] += tick
    G.FUNCS['loop/fast'][-1:-1] = fast
    G.FUNCS['loop/second'][-1:-1] = second
