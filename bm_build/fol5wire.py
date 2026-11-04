"""3.1: THE NEW FOLLOWERS' WIRING - what every one of the seven shares on top of rigpet (the Rat King's machinery):

  register(C, A, doll)  rigpet's registration, the faces (rigface), its doll (Cecil's, baked from its real model at the default
                        chibi warp, with its own groups when its head isn't named like one), its display-case fit, its pairs with
                        Bender and Mr. Capshun (Henry's and Nia's are cat_bonds')
  rp(C, R, icon)        its models (the art's sets but the shiny - a look), the textures, the summon item's icon, an item
                        definition for the face part in every set it wears, each picking the mood's face
  build(C, G, ...)      rigpet's build, then the two ways to sit (a right-click: sit_a and its idle cycle; SNEAK + right-click:
                        sit_b and its own), the frame trick (the summon item in an item frame: its model changes on a timer, a
                        right-click on the frame gives a flourish - on top of the follower climbing out, as every follower's does)
  hit(A)                its click box, fitted to its size (the art's idle extent)"""
import fol5
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
import rigpet as RP
import rigface as RF2
import rigfol as RF
import phase141 as P141
import phase134 as P134


def hit(A, pad=0.1, lo=0.5):
    """(width, height) of the click box: the art's resting extent, a little proud"""
    y0, h, x0, x1, z0, z1 = A.FIT
    return (round(max(lo, max(x1 - x0, z1 - z0) * 0.85 + pad), 2), round(max(lo, h + y0 + pad), 2))


def cycle(A, idle, sit, happy, acts, wp=8, rp_=6):
    """rigpet's state cycles (phase235.cycle) from the poses this art has: its walk keys (walk_0.., or two), its run (run_0.., or
    run_0 and a walk key), a jump (its own, or its run's first), swimming (its own, or its walk)"""
    P = A.POSES
    wk = [f'walk_{i}' for i in range(4) if f'walk_{i}' in P]
    rn = [f'run_{i}' for i in range(4) if f'run_{i}' in P] or wk[:1]
    if len(rn) == 1 and len(wk) > 1:
        rn = [rn[0], wk[1]]
    sw = [f'swim_{i}' for i in range(8) if f'swim_{i}' in P]
    spread = lambda per, ks: (per, [(i * per // len(ks), k) for i, k in enumerate(ks)])
    c = {1: spread(wp, wk), 2: spread(rp_, rn), 3: (None, [(0, 'jump' if 'jump' in P else rn[0])]), 10: spread(16, sw) if sw else spread(wp * 2, wk)}
    c.update({0: idle, 4: sit, 6: happy})
    c.update(acts)
    return c


def register(C, A, doll_desc, doll_fx=('minecraft:end_rod', 'minecraft:entity.allay.item_given', 'minecraft:poof'), pairs=None, vname=None):
    RP.register(C)
    RF2.setup(C, A.FACE_PART)
    w = C.W
    d = f'doll_{w}'
    item(d, TOTEM, f'{C.NAME[4:] if C.NAME.startswith("The ") else C.NAME} Doll', C.COL,
         [doll_desc, ('Right-click a block: set it down.', 'blue'), ('Right-click it: it twirls.', 'blue'), ('Sneak + punch: pick it up.', 'gray')],
         model=f'bm:{d}', stack=16, cat='fun', comps=hold('none'))
    HOLD[d] = f'bm:p141/{d}/use'
    P141.DOLLS.append((d, C.NAME, C.COL, doll_desc) + tuple(doll_fx))
    idle = A.POSES['idle_a']
    groups = {f'bm:{C.A.model_name(p, idle)}': g for p, g in A.GROUPS.items() if p in A.PARTS and not A.HIDDEN(p, idle)}
    P141.DOLL_FROM[d] = (C.ITEM, dict(A.DOLL, **({'groups': groups} if groups else {})))
    P134.FIT[C.ITEM] = A.FIT
    if pairs:
        import phase188 as P188
        P188.VNAME[w] = vname or C.NAME[0].lower() + C.NAME[1:]
        P188.PAIRS.update(pairs)
        P188.ICON.update({k: f'bm:{C.ITEM}' for k in pairs})


def pair_fx(*es):
    import phase188 as P188
    return [f'effect give {P188.O} minecraft:{e} 3 {a} true' for e, a in es]


def rp(C, R, icon, art):
    """the resource pack: RP.rp, and the face part's item definitions in every set (a mood's face each)"""
    R.TEXTURE_MODS.append(art)
    RP.rp(C, R, icon)
    names = set(art.models())
    fp = art.FACE_PART

    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for sfx in art.SKINS:
            base = f'{art.PREFIX}{fp}{sfx}'
            if base not in names:
                continue
            cases = [{'when': e, 'model': mdl(f'{art.PREFIX}{fp}_x{C.FACE[e]}{sfx}')} for e in C.EXPR
                     if C.FACE.get(e) and f'{art.PREFIX}{fp}_x{C.FACE[e]}{sfx}' in names]
            R2.wj(f'assets/bm/items/{base}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': cases, 'fallback': mdl(base)}})
    R.POST.append(post)


def poses_for(C, G, names, dur=None):
    """pose functions for poses no cycle names (rigpet writes only its cycles' own)"""
    pfx, A = C.pfx, C.A
    SP = A.RIG_SCALE
    psel = lambda p=None: f'@e[type=minecraft:item_display,tag=bm.{C.ab}sel' + (f',tag=bm.{C.ab}p_{p}]' if p else ']')
    for n in names:
        if f'{pfx}/pose/{n}' not in G.FUNCS:
            G.fn(f'{pfx}/pose/{n}', RF.pose(A, A.POSES[n], SP, (dur or C.DUR).get(n, 6) if isinstance(dur or C.DUR, dict) else dur, psel, swap=C.SWAP, keep=True) +
                 C.POSE_EXTRA(n, psel))


def cycle_fn(G, C, name, period, frames):
    """an animation cycle of its own: {pfx}/anim/<name> (as the host), its poses written if they aren't"""
    pfx, S = C.pfx, (lambda s: f'bm.{C.q}{s}')
    poses_for(C, G, [p for _t, p in frames])
    lines = [f'scoreboard players operation #f bm.rng = @s {S("fr")}']
    if period:
        lines.append(f'scoreboard players operation #f bm.rng %= #{period} bm.rng')
        G.FUNCS['load'][-1:-1] = [f'scoreboard players set #{period} bm.rng {period}']
    lines += [f'execute if score #f bm.rng matches {t} run function bm:{pfx}/pose/{p}' for t, p in frames]
    G.fn(f'{pfx}/anim/{name}', lines)


def build(C, G, abilities, encounter, sitb=None, frame=None):
    """rigpet's build - then the sneak-sit, and the frame trick"""
    RP.build(C, G, abilities, encounter)
    fn, pfx, ab = G.fn, C.pfx, C.ab
    sb = f'bm.{ab}sb'
    # ---- SNEAK + right-click: sit_b and its own cycle (a plain right-click, or the menu: sit_a's)
    if sitb:
        W_ = G.FUNCS[f'{pfx}/who']
        cw = f'@e[type=minecraft:wolf,tag=bm.{ab}clk,limit=1]'
        k = next(i for i, l in enumerate(W_) if 'bm.pid = #me bm.pid run return run' in l)
        W_[k + 1:k + 1] = [f'execute if predicate bm:p20/sneaking run tag {cw} add {sb}', f'execute unless predicate bm:p20/sneaking run tag {cw} remove {sb}']
        G.FUNCS[f'{pfx}/sit'].insert(0, f'tag @e[type=minecraft:wolf,tag=bm.{ab}sel2] remove {sb}')
        period, frames = sitb
        cycle_fn(G, C, '4b', period, frames)
        G.FUNCS[f'{pfx}/anim/4'].insert(0, f'execute if entity @s[tag={sb}] run return run function bm:{pfx}/anim/4b')
    # ---- the frame trick (phase68's anchor, each second, holds the frame as bm.ffsel; its p68/rot, a right-click on the frame)
    if frame:
        import phase68 as P68
        n = P68.KINDS[C.W][0]
        models, every, click = frame['models'], frame.get('every', 2), frame.get('click', [])
        FR = '@e[type=#bm:p49_frames,tag=bm.ffsel,limit=1]'
        A_ = G.FUNCS['p68/anchor']
        k = A_.index('tag @e[tag=bm.ffsel] remove bm.ffsel')
        A_.insert(k, f'execute if score @s bm.ffk matches {n} as {FR} at @s run function bm:{pfx}/frame/tick')
        ft = f'bm.{C.q}ft'
        G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {ft} dummy']
        G.OBJECTIVES.append(ft)
        L = len(models) * every
        fn(f'{pfx}/frame/tick', [f'scoreboard players add @s {ft} 1', f'execute if score @s {ft} matches {L}.. run scoreboard players set @s {ft} 0'] +
           [f'execute if score @s {ft} matches {i * every} run data modify entity @s Item.components."minecraft:item_model" set value "bm:{m}"' for i, m in enumerate(models)] +
           list(frame.get('tick', [])))
        R_ = G.FUNCS['p68/rot']
        k = R_.index('tag @a[tag=bm.ffsn] remove bm.ffsn')
        R_.insert(k, f'execute if score @e[type=minecraft:armor_stand,tag=bm.ffas,limit=1] bm.ffk matches {n} run function bm:{pfx}/frame/click')
        fn(f'{pfx}/frame/click', list(click))
        # (punched out: its own icon again, not a frame of the trick)
        G.FUNCS['p68/gone'].insert(0, f'execute if score @s bm.ffk matches {n} as @e[type=minecraft:item,distance=..3] if items entity @s contents *[minecraft:custom_data~{{bm:"{C.ITEM}"}}] run data modify entity @s Item.components."minecraft:item_model" set value "bm:{C.ITEM}"')
