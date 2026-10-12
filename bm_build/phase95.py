"""2.67: the followers' faces move.

Every follower with a face (Emma, Celi, Cecil, Leo) now blinks, and changes expression by temperament and by what's
happening around them:
- HURT: a hit shows on the face for a moment (> < for Emma and Cecil, Celi's angry squint, Leo's gritted teeth).
- FIGHTING (a monster within 10 blocks): serious - Emma's lids lowered and brows set, Celi's fangs bared, Cecil's slits
  narrowed, Leo's jaw set.
- LOW ON HEALTH (a third or less): Emma looks sad (a tear), Celi furious, Cecil and Leo grim.
- CALM, each in their own way: Emma blinks often and beams or winks at you now and then; Celi blinks quickly, cuts her
  eyes away (tsk) and huffs; Cecil spends a lot of time half-lidded and deadpan, rolls his eyes, gives a sly look; Leo
  blinks slowly, smiles when you're close - and looks worried when YOU are hurt.
- ARRIVING: Emma beams, Celi tsks, Cecil rolls his eyes, Leo smiles.
- (2.67) STARTLED: the moment a monster first comes within 10 blocks, a wide-eyed "o" before the fighting face.
- (2.67) SLEEPY: told to sit at night, with nothing the matter, their lids grow heavy.
How: the head (Cecil: his glowing eyes) keeps its model; its item definition picks a face from the item's
custom_model_data string, and one controller per follower sets that string only when the face changes."""
from nbt import snbt
import phase95_art as ART

# follower: (host type, host tag, head selector, expressions, blink ticks, calm moods [(expr, ticks, 1-in-N)], greet, low, fight)
FOLK = {
    'emma': ('minecraft:cat', 'bm.emmapet', 'type=minecraft:item_display,tag=bm.emp,tag=bm.ep_head,tag=!bm.emfade', ART.EMMA_EXPR,
             (50, 110), [('happy', 34, 5), ('wink', 14, 11)], ('happy', 34), 'sad', 'serious'),
    'celi': ('minecraft:wolf', 'bm.celipet', 'type=minecraft:item_display,tag=bm.cep,tag=bm.cp6_head,tag=!bm.cefade', ART.CELI_EXPR,
             (36, 80), [('tsk', 26, 4), ('huff', 22, 6)], ('tsk', 30), 'hurt', 'serious'),
    'cecil': ('minecraft:wolf', 'bm.cecilpet', 'type=minecraft:item_display,tag=bm.cpet,tag=bm.cp_eyes,tag=!bm.cpfade', ART.CECIL_EXPR,
              (80, 160), [('deadpan', 90, 3), ('roll', 22, 7), ('sly', 32, 9)], ('roll', 26), 'serious', 'serious'),
    'leo': ('minecraft:wolf', 'bm.leopet', 'type=minecraft:item_display,tag=bm.lep,tag=bm.lp_head,tag=!bm.lefade', None,
            (70, 140), [('smile', 36, 4)], ('smile', 40), 'serious', 'serious'),
}
OBJS = ['bm.fxe', 'bm.fxt', 'bm.fxh', 'bm.fxb', 'bm.fxc', 'bm.fxl', 'bm.fxa', 'bm.fxo', 'bm.fxp']


def exprs(k):
    if k == 'leo':
        import phase96_art
        return phase96_art.LEO_EXPR
    return FOLK[k][3]


def eid(k, name):
    return exprs(k).index(name) + 1


def face_cmd(k, name, ticks, who='@s'):
    """(for other phases) show an expression on a follower host for a while"""
    return [f'scoreboard players set {who} bm.fxe {eid(k, name)}', f'scoreboard players set {who} bm.fxt {ticks}']


# ===================================================================== resource pack: the faces, a head model per face, the item definitions
def textures():
    T = {}
    for e in ART.EMMA_EXPR:
        T[f'em2_face_{e}'] = ART.emma_face(e, *ART.EMMA_EYES)
        T[f'ee_face_{e}'] = ART.emma_face(e, *ART.EMMA_EYES_ETH)
    for e in ART.CELI_EXPR:
        T[f'ce_face_{e}'] = ART.celi_face(e)
    return T


FACE_KEYS = (('em_head', 'em2_face', ART.EMMA_EXPR), ('ee_head', 'ee_face', ART.EMMA_EXPR), ('ce_head', 'ce_face', ART.CELI_EXPR))


def rp(R):
    import sys
    import phase96_art
    R.TEXTURE_MODS.append(sys.modules[__name__])
    heads = {}                                          # item: [(case, model)]
    for base, key, ex in FACE_KEYS + (('le_head', 'le_face', phase96_art.LEO_EXPR),):
        for name in [n for n in list(R.HATS) if n == base or (n.startswith(base + '_') and '_x' not in n[len(base):])]:
            tex, els = R.HATS[name]
            assert key in tex, (name, key)
            heads[name] = []
            for e in ex:
                R.HATS[f'{name}_x{e}'] = (dict(tex, **{key: f'bm:block/{key}_{e}'}), els)
                heads[name].append((e, f'{name}_x{e}'))
    for name in ('cec2_eyes', 'cec2_eyes_ethereal'):
        tex, els = R.HATS[name]
        heads[name] = []
        for e in ART.CECIL_EXPR:
            R.HATS[f'{name}_x{e}'] = (tex, ART.cecil_eyes(els, e))
            heads[name].append((e, f'{name}_x{e}'))
    def post(R2):
        mdl = lambda n: {'type': 'minecraft:model', 'model': f'bm:item/{n}'}
        for name, cases in heads.items():
            R2.wj(f'assets/bm/items/{name}.json', {'model': {'type': 'minecraft:select', 'property': 'minecraft:custom_model_data', 'index': 0,
                                                             'cases': [{'when': e, 'model': mdl(m)} for e, m in cases], 'fallback': mdl(name)}})
    R.POST.append(post)


def extend_offers(O, offer):
    pass


# ===================================================================== the controllers
def generate(G):
    fn = G.fn
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in OBJS]
    G.OBJECTIVES += OBJS
    tick = ['scoreboard players add #fxk bm.fxt 1', 'execute if score #fxk bm.fxt matches 20.. run scoreboard players set #fxk bm.fxt 0']
    foe = 'type=#bm:hostile,tag=!bm.npc'
    for k, (host, tag, head, _, (b0, b1), moods, (gname, gt), low, fight) in FOLK.items():
        ex = exprs(k)
        tick.append(f'execute as @e[type={host},tag={tag}] at @s run function bm:p95/{k}/tick')
        fn(f'p95/{k}/tick', ['execute store result score #h bm.rng run data get entity @s Health 10',
                             f'execute unless score @s bm.fxh matches -2147483648.. run function bm:p95/{k}/greet',
                             f'execute if score #h bm.rng < @s bm.fxh run function bm:p95/{k}/ouch',
                             'scoreboard players operation @s bm.fxh = #h bm.rng',
                             # (every half second: a fight nearby? and for Leo: is his summoner hurt?)
                             f'execute if score #fxk bm.fxt matches 0 store success score @s bm.fxc if entity @e[{foe},distance=..10]',
                             f'execute if score #fxk bm.fxt matches 10 store success score @s bm.fxc if entity @e[{foe},distance=..10]',
                             # (2.67) the moment a monster first shows: startled
                             f'execute if score @s bm.fxc matches 1 unless score @s bm.fxp matches 1 run function bm:p95/{k}/startle',
                             'scoreboard players operation @s bm.fxp = @s bm.fxc'] +
           (['execute if score #fxk bm.fxt matches 5 run function bm:p95/leo/owner'] if k == 'leo' else []) +
           ['execute if score @s bm.fxt matches 1.. run scoreboard players remove @s bm.fxt 1',
            f'execute unless score @s bm.fxt matches 1.. run function bm:p95/{k}/calm',
            f'execute unless score @s bm.fxe = @s bm.fxl run return run function bm:p95/{k}/apply',
            f'execute if score #fxk bm.fxt matches 0 run function bm:p95/{k}/apply'])
        fn(f'p95/{k}/greet', ['scoreboard players set @s bm.fxl -1', 'scoreboard players set @s bm.fxc 0', 'scoreboard players set @s bm.fxo 0',
                              f'scoreboard players set @s bm.fxb {b0}'] + face_cmd(k, gname, gt))
        fn(f'p95/{k}/ouch', face_cmd(k, 'hurt', 14))
        fn(f'p95/{k}/startle', [f'execute if score @s bm.fxt matches 1.. if score @s bm.fxe matches {eid(k, "hurt")} run return 0'] + face_cmd(k, 'surprised', 14))
        # calm: the base face for the moment (fighting / low / the owner hurt / plain), and the blink clock
        low_at = ['execute store result score #mx bm.rng run attribute @s minecraft:max_health get 3.334']
        calm = ['scoreboard players remove @s bm.fxb 1', f'execute if score @s bm.fxb matches ..0 run return run function bm:p95/{k}/blink',
                'scoreboard players set @s bm.fxe 0'] + low_at + \
               [f'execute if score #h bm.rng <= #mx bm.rng run scoreboard players set @s bm.fxe {eid(k, low)}',
                f'execute if score @s bm.fxc matches 1 run scoreboard players set @s bm.fxe {eid(k, fight)}',
                # (2.67) sitting, at night, nothing the matter: drowsy
                f'execute if score @s bm.fxe matches 0 if score #tod bm.bm matches 13000..23000 if data entity @s {{Sitting:1b}} run scoreboard players set @s bm.fxe {eid(k, "sleepy")}']
        if k == 'leo':
            calm.append(f'execute if score @s bm.fxo matches 1 run scoreboard players set @s bm.fxe {eid(k, "worried")}')
        if k == 'cecil':
            calm.append(f'execute if score @s bm.fxe matches 0 if data entity @s {{Sitting:1b}} run scoreboard players set @s bm.fxe {eid(k, "deadpan")}')
        fn(f'p95/{k}/calm', calm)
        # a blink - or, calm and unhurried, one of their moods
        top = sum(1 for _ in moods) and max(n for *_, n in moods) * 2
        blink = [f'execute store result score @s bm.fxb run random value {b0}..{b1}']
        if moods:
            blink += [f'execute store result score #r bm.rng run random value 1..{top}']
            lo = 1
            for name, t, n in moods:
                w = max(1, top // n)
                cond = 'if score @s bm.fxc matches 0 ' + ('if score @s bm.fxo matches 0 ' if k == 'leo' else '')
                if k == 'leo' and name == 'smile':
                    cond += 'if entity @a[distance=..6,gamemode=!spectator] '
                blink.append(f'execute {cond}if score #r bm.rng matches {lo}..{lo + w - 1} run return run function bm:p95/{k}/mood_{name}')
                fn(f'p95/{k}/mood_{name}', face_cmd(k, name, t))
                lo += w
        blink += face_cmd(k, 'blink', 3)
        fn(f'p95/{k}/blink', blink)
        # show it: only the head of THIS follower, only when its face is different
        fn(f'p95/{k}/apply', ['scoreboard players operation @s bm.fxl = @s bm.fxe', 'scoreboard players operation #fx bm.rng = @s bm.fxe',
                              'scoreboard players operation #me bm.pid = @s bm.pid',
                              f'execute as @e[{head}] if score @s bm.pid = #me bm.pid unless score @s bm.fxa = #fx bm.rng run function bm:p95/{k}/set'])
        fn(f'p95/{k}/set', ['execute if score #fx bm.rng matches 0 run data remove entity @s item.components."minecraft:custom_model_data"'] +
           [f'execute if score #fx bm.rng matches {i + 1} run data modify entity @s item.components."minecraft:custom_model_data" set value {{strings:["{e}"]}}'
            for i, e in enumerate(ex)] + ['scoreboard players operation @s bm.fxa = #fx bm.rng'])
    # (Leo) his summoner at a third of their health or less
    fn('p95/leo/owner', ['scoreboard players set @s bm.fxo 0', 'execute on owner store result score #oh bm.rng run data get entity @s Health',
                         'execute on owner if score #oh bm.rng matches ..7 run scoreboard players set #oh bm.rng -1',
                         'execute if score #oh bm.rng matches -1 run scoreboard players set @s bm.fxo 1'])

    # ---- context: Emma beams when her heal lands; Celi tsks after a kill quip; Cecil's sly look when he casts
    if 'p57/quickheal' in G.FUNCS:
        G.FUNCS['p57/quickheal'] += ['execute as @e[type=minecraft:cat,tag=bm.emme,limit=1] run function bm:p95/emma/beam']
        fn('p95/emma/beam', face_cmd('emma', 'happy', 30))
    if 'p66/quip' in G.FUNCS:
        G.FUNCS['p66/quip'] += face_cmd('celi', 'tsk', 30)
    G.FUNCS['tick'] += tick
    G.FUNCS['admin/help'] += [G.tellraw('@s', [{'text': '/function bm:admin/faces', 'color': 'yellow'}, {'text': '  every follower nearby pulls each face in turn', 'color': 'gray'}])]
    # (admin) a parade of faces: each follower nearby runs through its expressions, a second each
    fn('admin/faces', ['scoreboard players set #fxp bm.fxt 0', 'schedule function bm:p95/parade 1t replace'])
    lines = ['scoreboard players add #fxp bm.fxt 1']
    for k, (host, tag, *_rest) in FOLK.items():
        for i, e in enumerate(exprs(k)):
            lines.append(f'execute if score #fxp bm.fxt matches {(i + 1) * 20} as @e[type={host},tag={tag}] run function bm:p95/{k}/mood_x{e}')
            fn(f'p95/{k}/mood_x{e}', face_cmd(k, e, 20))
    n = max(len(exprs(k)) for k in FOLK)
    lines.append(f'execute if score #fxp bm.fxt matches ..{(n + 1) * 20} run schedule function bm:p95/parade 1t replace')
    fn('p95/parade', lines)
