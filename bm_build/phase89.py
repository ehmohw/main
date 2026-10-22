"""2.67: FOLLOWERS IN THE VAULT - raid contracts, the followers' wardrobe at Goldtooth, and two new outfits for Emma.

RAID CONTRACTS (Goldtooth, in the den - dear): one for each follower - Cecil, Emma, Celi, Zib, the Skiff Escorts and
  KillerWatt. Use it once and it's signed for good: from then on that follower comes into the vault with you - switched on
  or off in the Fixer's Ledger, Raid Crew (phase98); their summoning items stay at the coat check. A follower in the vault
  fights the guards as it does anywhere.
  THE FROG WITH MUSTACHE and DONADO: their contracts are kept. Use one in the vault and a vault hire of him joins you, in
  his own iron kit (he can't take your gear and drops none); use it again and he clocks off. He leaves when you leave the
  heist; if he faints, 5 minutes before he'll sign on again. The one you hired at home stays home, untouched.
THE FOLLOWERS' WARDROBE (Goldtooth): Emma's ribbons and dresses, Celi's outfits and Zib's uniforms for Gutter
  Medallions - the hidden ones too, for a Gutter Trophy each; Pearlman's nine gems (Cecil's robes) and the Ethereal Gem.
EMMA'S NEW OUTFITS (Goldtooth): THE FLOWER TOP (a pink long-sleeved top with a magenta flower, light grey trousers, black
  flats, a red bow in a high ponytail) and THE COZY SWEATER (a purple turtleneck with a pocket, blue jeans, purple
  sneakers, a pink flower tie in her ponytail). Use one while she's with you; sneak + use for her own dress again.
  (The Flower Top's thin choker still shows her buff's colour.)
"""
import copy
import random
from PIL import Image, ImageDraw
from items import item, T, TOTEM, ITEMS
from useitem import hold, HOLD
from nbt import snbt, B, F, Int
import phase57_art as EA
from phase57_art import _el, _cloth, hexc, PIVOT
import phase72 as P72

GOLD = '#ffcf40'
PINK = '#ff8ad0'
OUTFITS = {1: ('Flower Top', '#f4a0a4'), 2: ('Cozy Sweater', '#6a2ac8')}
FOLLOWERS = {  # key: (on the contract, in a sentence, colour, its summoning check (None: hired, not called), price (Gutter Trophies, Gutter Medallions))
    'cecil': ('Cecil', 'Cecil', '#7aa8ff', 'p46/pet/try_summon', (1, 4)), 'emma': ('Emma', 'Emma', PINK, 'p57/try_summon', (1, 4)),
    'celi': ('Celi', 'Celi', '#9ae0ff', 'p66/try_summon', (1, 6)), 'zib': ('Zib', 'Zib', '#7ad87a', 'p72/zb/try_summon', (1, 4)),
    'escort': ('Skiff Escorts', 'your Skiff Escorts', '#c8c8ff', 'p72/esk/use', (1, 0)),
    'killerwatt': ('KillerWatt', 'KillerWatt', '#ffe040', 'p79/pet/try', (2, 4)),
    'frog': ('The Frog with Mustache', 'the Frog with Mustache', '#6ac850', None, (1, 4)), 'donado': ('Donado', 'Donado', '#e8d29a', None, (1, 4))}
BIT = {k: 2 ** i for i, k in enumerate(k for k, v in FOLLOWERS.items() if v[3])}      # (a called follower's contract is signed for good: one bit each)
HIRED = {'frog': ('bm.frogpet', 'p20/frog/summon', 'p20/frog/refresh', 'bm.fvcf', 'fg'), 'donado': ('bm.donado', 'p25/don/summon', 'p25/don/refresh', 'bm.fvcn', 'dn')}
KIT = [('weapon.mainhand', 'minecraft:iron_sword'), ('armor.head', 'minecraft:iron_helmet'), ('armor.chest', 'minecraft:iron_chestplate')]
P72.KEEP += ['cecil_gem', 'emma_ribbon', 'celi_charm', 'donadian_medal', 'kw_spark'] + [f'skiff_escort_{c}' for c in P72.ART.ESCORT_COLS] + \
            [f'fcontract_{k}' for k in HIRED]

for _k, (_n, _c) in OUTFITS.items():
    item(f'cos_outfit_{_k}', TOTEM, f"Emma's Outfit: {_n}", _c, [{1: 'A pink top with a flower, grey trousers, a red bow.', 2: 'A purple turtleneck, jeans, comfy sneakers.'}[_k],
                                                              ('Use while Emma is with you: she changes.', 'blue'), ('Kept: change back and forth as you like.', 'gray'),
                                                              ('Sneak + use: back to her dress.', 'gray')],
         model={1: 'minecraft:pink_dye', 2: 'minecraft:purple_dye'}[_k], stack=1, cat='cosmetic', comps=hold('none'))
    HOLD[f'cos_outfit_{_k}'] = f'bm:p89/use/outfit{_k}'
for _k, (_t, _n, _c, _chk, _p) in FOLLOWERS.items():
    item(f'fcontract_{_k}', TOTEM, f'Raid Contract: {_t}', _c,
         ['Signed in gold ink, sealed in wax.'] +
         ([(f'Use once: from then on {_n}', 'blue'), ('will come into the vault with you.', 'blue')] if _chk else
          [(f'Use in the vault: {_n} joins you -', 'blue'), ("the vault's own hire, in his own kit.", 'blue'), ('Use again: he clocks off.', 'blue'),
           ('Kept: call him every heist.', 'gray'), ('(Yours at home stays home.)', 'dark_gray')]),
         model='minecraft:paper', glint=True, stack=1, cat='magic', comps=hold('none'))
    HOLD[f'fcontract_{_k}'] = f'bm:p89/sign/{_k}' if _chk else f'bm:p89/call/{_k}'


# ===================================================================== Emma's outfits: textures and models
TOP_A, TOP_A_DK, FLOWER, FLOWER_C = '#f7a6c6', '#e086aa', '#d838b8', '#f6f08a'
PANTS_A, SHOE_A, BOW_A, BOW_A_DK = '#cfc4c4', '#1c1c1e', '#d42424', '#a01818'
TOP_B, TOP_B_DK, JEANS, SNEAK, SNEAK_W = '#6a24c8', '#43148a', '#2c4c94', '#3c2a96', '#f2f2f2'


def textures():
    # (2.77c: her outfits in the same detail as her dress - a weave and folds, a knit, denim twill, polished shoes)
    from phase57_art import _fabric, _knit, _gloss, _sh
    def chest(base, decal, knit=False):
        im = (_knit if knit else _fabric)(base, 61); d = ImageDraw.Draw(im)
        decal(d)
        return im
    def flower(d):
        for k in range(5):
            import math
            a = k * 2 * math.pi / 5 - math.pi / 2
            x, y = 32 + 9 * math.cos(a), 26 + 9 * math.sin(a)
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=hexc(FLOWER))
            d.ellipse((x - 4, y - 5, x + 1, y - 1), fill=hexc('#f070d4'))          # (each petal lit)
        d.ellipse((25, 19, 39, 33), fill=hexc(FLOWER_C)); d.ellipse((28, 21, 33, 25), fill=hexc('#fffbd0'))
    def pocket(d):
        d.rounded_rectangle((16, 40, 48, 60), radius=6, fill=hexc(TOP_B_DK)); d.line((18, 42, 46, 42), fill=hexc('#2e0c60'), width=2)
        d.line((30, 6, 34, 28), fill=hexc('#c8a8ff'), width=1)
    def denim(c, seed):
        """denim: a diagonal twill, faded down the middle, a stitched seam"""
        im = _fabric(c, seed, folds=2, weave=False); px = im.load()
        for y in range(64):
            for x in range(64):
                if (x + y) % 3 == 0: px[x, y] = _sh(px[x, y], 0.86) + (255,)
                if 22 <= x <= 40: px[x, y] = _sh(px[x, y], 1.07) + (255,)
            if y % 3 == 0: px[1, y] = hexc('#d8a850')                            # (the seam's gold stitch)
        return im
    sneaker = _gloss(SNEAK, 63); ImageDraw.Draw(sneaker).rectangle((0, 48, 63, 63), fill=hexc(SNEAK_W))
    return {'em3_top_a': _fabric(TOP_A, 59), 'em3_chest_a': chest(TOP_A, flower), 'em3_pants_a': _fabric(PANTS_A, 67, folds=3),
            'em3_shoe_a': _gloss(SHOE_A, 71), 'em3_bow_a': _fabric(BOW_A, 73, folds=1, weave=False, top=1.12), 'em3_bow_a_dk': _fabric(BOW_A_DK, 79, folds=1, weave=False),
            'em3_top_b': _knit(TOP_B, 83), 'em3_top_b_dk': _knit(TOP_B_DK, 89),
            'em3_chest_b': chest(TOP_B, pocket, knit=True), 'em3_jeans': denim(JEANS, 97),
            'em3_sneaker': sneaker, 'em3_white': _fabric(SNEAK_W, 101, folds=1, top=1.0)}


def models():
    M = {}
    TX = {k: f'bm:block/{k}' for k in textures()}
    TX.update({k: f'bm:block/{k}' for k in EA.textures()})
    def part(name, els):
        used = sorted({e['faces'][f]['texture'][1:] for e in els for f in e['faces']})
        M[name] = ({k: TX[k] for k in used}, els)
    pv = PIVOT['body']
    for o, (top, chest_t, pants, dk) in {1: ('em3_top_a', 'em3_chest_a', 'em3_pants_a', 'em3_top_a'), 2: ('em3_top_b', 'em3_chest_b', 'em3_jeans', 'em3_top_b_dk')}.items():
        body = [_el((-3.4, 11.0, -2.3), (3.4, 16.0, 2.3), pants, pv),                                       # the hips, in trousers
                _el((-3.1, 15.6, -2.1), (3.1, 22.6, 2.1), top, pv, uv={'north': [0, 0, 16, 16]}),          # the top
                _el((-1.0, 22.6, -1.0), (1.0, 24.4, 1.0), 'em2_skin', pv)]
        body[1]['faces']['north']['texture'] = '#' + chest_t
        if o == 1:
            body.append(_el((-1.15, 23.0, -1.15), (1.15, 23.45, 1.15), 'em2_scarf', pv))                 # a thin choker (her buff's colour)
        else:
            body += [_el((-3.25, 15.3, -2.25), (3.25, 16.4, 2.25), dk, pv),                                # the hem
                     _el((-1.7, 22.3, -1.7), (1.7, 24.1, 1.7), top, pv),                                     # the turtleneck
                     _el((-1.8, 23.4, -1.8), (1.8, 24.2, 1.8), dk, pv),                                      # its fold
                     _el((-2.3, 19.9, -2.25), (-1.1, 21.1, -2.12), 'em2_scarf', pv)]                         # a heart pin (her buff's colour)
        part(f'em_body_o{o}', body)
        for sx, nm in ((1, 'armr'), (-1, 'arml')):
            p = PIVOT[nm]; cx = p[0]
            arm = [_el((cx - 1, 14.6, -1), (cx + 1, 22.8, 1), top, p), _el((cx - 0.9, 13.0, -0.9), (cx + 0.9, 14.6, 0.9), 'em2_skin', p)]
            if o == 2: arm.append(_el((cx - 1.12, 14.5, -1.12), (cx + 1.12, 15.6, 1.12), dk, p))            # ribbed cuffs
            part(f'em_{nm}_o{o}', arm)
        for sx, nm in ((1, 'legr'), (-1, 'legl')):
            p = PIVOT[nm]
            x0, x1 = (0.7, 2.7) if sx > 0 else (-2.7, -0.7)
            leg = [_el((x0 - 0.05, 1.3, -1.05), (x1 + 0.05, 12.0, 1.05), pants, p)]
            if o == 1:
                leg += [_el((x0 - 0.25, 0, -2.5), (x1 + 0.25, 1.3, 1.15), 'em3_shoe_a', p)]                 # black flats
            else:
                leg += [_el((x0 - 0.35, 0, -2.4), (x1 + 0.35, 1.9, 1.3), 'em3_sneaker', p),                 # sneakers, a white toe cap
                        _el((x0 - 0.36, 0, -2.9), (x1 + 0.36, 1.2, -2.2), 'em3_white', p)]
            part(f'em_{nm}_o{o}', leg)
        # her head with a high ponytail at the back: her own hair (minus her bun and bow), tied with a red bow (the Flower Top)
        # or a pink flower (the Cozy Sweater)
        etex, eels = EA.models()['em_head']
        hp = PIVOT['head']
        els = copy.deepcopy(eels[:EA.HEAD_BASE])
        hr = lambda fr, to, rot=None: _el(fr, to, 'em2_hair', hp, rot)
        els += [hr((-1.7, 25.4, 4.3), (1.7, 31.0, 6.3), ('x', -22.5, (0, 31.0, 5.3))),           # the tail, swinging back from the tie
                hr((-1.4, 20.6, 6.3), (1.4, 26.2, 8.1)), hr((-0.9, 19.2, 6.7), (0.9, 20.8, 7.8))]
        if o == 1:
            els += [_el((-1.0, 30.4, 4.3), (1.0, 32.4, 5.9), 'em3_bow_a_dk', hp),                                        # the knot
                    _el((-3.8, 30.2, 4.5), (-0.8, 33.0, 5.5), 'em3_bow_a', hp, ('z', 22.5, (-1.0, 31.4, 5.0))),          # the loops
                    _el((0.8, 30.2, 4.5), (3.8, 33.0, 5.5), 'em3_bow_a', hp, ('z', -22.5, (1.0, 31.4, 5.0))),
                    _el((-1.6, 28.0, 5.0), (-0.6, 30.6, 5.6), 'em3_bow_a', hp, ('z', -22.5, (-1.0, 30.4, 5.3))),         # the tails
                    _el((0.6, 28.0, 5.0), (1.6, 30.6, 5.6), 'em3_bow_a', hp, ('z', 22.5, (1.0, 30.4, 5.3)))]
        else:
            els += [_el((-1.5, 30.0, 4.3), (1.5, 33.0, 5.7), 'em2_pink', hp),                                            # the flower
                    _el((-2.4, 30.8, 4.6), (2.4, 32.2, 5.5), 'em2_pink', hp), _el((-0.7, 29.2, 4.6), (0.7, 33.8, 5.5), 'em2_pink', hp),
                    _el((-0.6, 30.9, 5.7), (0.6, 32.1, 6.0), 'ee_magenta', hp)]
        part(f'em_head_o{o}', els)
    return M


def extend_offers(O, offer):
    pass


def generate(G):
    fn, wjson, tellraw, title = G.fn, G.wjson, G.tellraw, G.title
    import phase70 as P70
    import phase78 as P78
    import gild
    import phase60 as P60
    say = lambda txt, col='gray': title('@s', 'actionbar', T(txt, col))
    P = [T('[', 'dark_gray'), T('Black Market', 'dark_purple', bold=True), T('] ', 'dark_gray')]
    objs = ['bm.coso', 'bm.fcon']
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs

    # ================================================================== EMMA'S NEW OUTFITS
    model = lambda tag, m: f'execute as @e[type=minecraft:item_display,tag=bm.emsel,{tag}] run data modify entity @s item.components."minecraft:item_model" set value "bm:{m}"'
    G.FUNCS['p78/emma_read'].append('scoreboard players operation #emoo bm.rng = @s bm.coso')
    out = G.FUNCS['p57/outfit']
    out.insert(0, 'scoreboard players set #emoo bm.rng 0')
    out += [model('tag=bm.ep_legr', 'em_legr').replace('execute as', 'execute if score #emoo bm.rng matches 0 as'),
            model('tag=bm.ep_legl', 'em_legl').replace('execute as', 'execute if score #emoo bm.rng matches 0 as')]
    for o in OUTFITS:
        out += [model(f'tag=bm.ep_{p}', f'em_{p}_o{o}').replace('execute as', f'execute if score #emoo bm.rng matches {o} as') for p in ('armr', 'arml', 'legr', 'legl', 'head')]
        out += [model('tag=bm.ep_body', f'em_body_o{o}_m{m}').replace('execute as', f'execute if score #emoo bm.rng matches {o} if score #emo bm.rng matches {m} as')
                for m in (1, 2, 3, 4, 5)]
    for o, (nm, c) in OUTFITS.items():
        fn(f'p89/use/outfit{o}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                                  'execute if predicate bm:p20/sneaking run scoreboard players set @s bm.coso 0',
                                  f'execute unless predicate bm:p20/sneaking run scoreboard players set @s bm.coso {o}', 'function bm:p78/emma_now',
                                  'execute if predicate bm:p20/sneaking run ' + say('"Back in my dress - it does twirl nicely."', PINK),
                                  'execute unless predicate bm:p20/sneaking run ' + say({1: '"The flower top! It\'s so comfy."', 2: '"Ooh, a sweater with a pocket!"'}[o], PINK)])
    for k in P78.DRESSES:           # (a dress puts the outfit away)
        G.FUNCS[f'p78/use/dress{k}'].insert(2, 'scoreboard players set @s bm.coso 0')

    # ================================================================== RAID CONTRACTS
    # (bm.fcon: one bit per follower, signed for good)
    def signed(k):
        return ['scoreboard players operation #q bm.rng = @s bm.fcon', f'scoreboard players set #bit bm.rng {BIT[k]}',
                'scoreboard players operation #q bm.rng /= #bit bm.rng', 'scoreboard players operation #q bm.rng %= #2 bm.rng']
    cap = lambda n: n[0].upper() + n[1:]
    for k, (ttl, nm, col, chk, price) in FOLLOWERS.items():
        if not chk: continue
        fn(f'p89/sign/{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                             'execute unless score @s bm.fcon matches 0.. run scoreboard players set @s bm.fcon 0'] + signed(k) +
           ['execute if score #q bm.rng matches 1 run return run ' + say(f'{cap(nm)} {"are" if k == "escort" else "is"} already under contract.', 'gray'),
            f'scoreboard players add @s bm.fcon {BIT[k]}', f'clear @s *[minecraft:custom_data~{{bm:"fcontract_{k}"}}] 1',
            'playsound minecraft:item.book.page_turn player @s ~ ~ ~ 1 0.8', 'playsound minecraft:block.anvil.use player @s ~ ~ ~ 0.4 1.6',
            tellraw('@s', P + [T('Signed! ', GOLD, bold=True), T(cap(nm), col, bold=True), T(' will answer your call in the vault from now on.', 'gray')])])
        fn(f'p89/ok/{k}', ['execute unless dimension bm:gutter run return run function bm:p74/fol_ok', 'execute unless entity @s[tag=bm.gvp] run return 0'] + signed(k) +
           ['execute if score #q bm.rng matches 1 run return 1',
            tellraw('@s', P + [T(cap(nm), col), T(' needs a ', 'gray'), T('Raid Contract', GOLD), T(' to come into the vault. Goldtooth sells them.', 'gray')]), 'return 0'])
        L = G.FUNCS[chk]
        assert any('execute unless function bm:p74/fol_ok' in l for l in L), chk
        L[:] = [l.replace('execute unless function bm:p74/fol_ok', f'execute unless function bm:p89/ok/{k}') for l in L]
    fn('admin/contracts_all', [f'scoreboard players set @s bm.fcon {sum(BIT.values())}', tellraw('@s', P + [T('Every follower is under contract.', 'gray')])])
    fn('admin/contracts_none', ['scoreboard players set @s bm.fcon 0', tellraw('@s', P + [T('Every contract torn up.', 'gray')])])

    # ---- the Frog with Mustache and Donado: their contracts call a vault hire of their own (the one at home stays home)
    objs = [v[3] for v in HIRED.values()]
    G.FUNCS['load'][-1:-1] = [f'scoreboard objectives add {o} dummy' for o in objs]
    G.OBJECTIVES += objs
    for k, (tag, summon, refresh, cd, fk) in HIRED.items():
        ttl, nm, col, chk, price = FOLLOWERS[k]
        src = G.FUNCS[summon]
        k_new = next(i for i, l in enumerate(src) if l.startswith('tag @e[tag=bm.') and l.endswith('remove ' + l.split('tag=')[1].split(',')[0]))
        new_t = src[k_new].split('tag=')[1].split(',')[0]
        body = [l for l in src[:k_new] if not l.startswith(('title ', 'tellraw '))] + \
            [f'tag @e[tag={new_t},distance=..3] add bm.fvault', f'scoreboard players operation @e[tag={new_t},distance=..3] bm.pid = @s bm.pid',
             f'execute as @e[type=minecraft:wolf,tag={new_t},distance=..3] run function bm:p89/fv/kit'] + \
            [l for l in src[k_new:] if not l.startswith(('title ', 'tellraw '))]
        fn(f'p89/fv/summon_{k}', body)
        fn(f'p89/call/{k}', ['execute if score @s bm.gvhc matches 1.. run return 0', 'scoreboard players set @s bm.gvhc 2',
                             'execute unless dimension bm:gutter run return run ' + say("This contract's only good in the vault.", 'gray'),
                             'execute unless entity @s[tag=bm.gvp] run return run ' + say("This contract's only good on a heist.", 'gray'),
                             'scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players set #had bm.rng 0',
                             f'execute as @e[type=minecraft:wolf,tag={tag},tag=bm.fvault] if score @s bm.pid = #me bm.pid at @s run function bm:p89/fv/dismiss',
                             'execute if score #had bm.rng matches 1 run return run ' + say(f'{cap(nm)} clocks off. (Use the contract to call him back.)', col),
                             f'execute if score @s {cd} matches 1.. store result score #m bm.rng run scoreboard players get @s {cd}',
                             f'execute if score @s {cd} matches 1.. run scoreboard players add #m bm.rng 59',
                             f'execute if score @s {cd} matches 1.. run scoreboard players operation #m bm.rng /= #60 bm.rng',
                             f'execute if score @s {cd} matches 1.. run return run ' + title('@s', 'actionbar', [T(f'{cap(nm)} is still recovering: about ', 'gray'),
                                                                                                                   {'score': {'name': '#m', 'objective': 'bm.rng'}, 'color': 'white'}, T(' min.', 'gray')]),
                             f'function bm:p89/fv/summon_{k}',
                             tellraw('@s', P + [T(cap(nm), col, bold=True), T(' signs on for the heist - ', 'gray'), T('in the vault\'s own kit', 'white'),
                                                T('. He fights what you fight. Use the contract again to send him off.', 'gray')])])
        # (fallen in the vault: he's out for 5 minutes - and it's the vault's hire who fainted, so no free walk home from the hut)
        G.FUNCS[f'p65/faint_{fk}'].insert(0, f'execute if entity @s[tag=bm.fvault] run return run function bm:p89/fv/faint_{k}')
        fn(f'p89/fv/faint_{k}', ['scoreboard players operation #me bm.pid = @s bm.pid', 'scoreboard players reset @s bm.pid',
                                 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.4 0.3 0.02 16', f'execute as @a if score @s bm.pid = #me bm.pid run function bm:p89/fv/fainted_{k}'])
        fn(f'p89/fv/fainted_{k}', [f'scoreboard players set @s {cd} 300',
                                   tellraw('@s', P + [T(f'{cap(nm)} is down! ', col, bold=True), T('Call him again with the contract in 5 minutes.', 'gray')])])
        G.FUNCS['loop/second'].append(f'scoreboard players remove @a[scores={{{cd}=1..}}] {cd} 1')
        # (his rig is built a moment later: those parts are the vault's too)
        G.FUNCS[f'p63/{"frog" if k == "frog" else "don"}/rig'].append('execute if entity @s[tag=bm.fvault] on passengers run tag @s add bm.fvault')
    # his own kit: iron, never dropped; your gear stays yours
    fn('p89/fv/kit', [f'item replace entity @s {sl} with {it}' for sl, it in KIT] +
       ['data merge entity @s {drop_chances:{mainhand:0f,offhand:0f,head:0f,chest:0f,legs:0f,feet:0f,body:0f}}'])
    G.FUNCS['p20/frog/route'].insert(0, 'execute if entity @e[type=minecraft:wolf,tag=bm.fsel,tag=bm.fvault] run return run ' +
                                     say("He's on the vault's payroll - he brought his own kit.", 'gray'))
    fn('p89/fv/dismiss', ['scoreboard players set #had bm.rng 1', 'particle minecraft:poof ~ ~0.5 ~ 0.3 0.4 0.3 0.02 12',
                          'playsound minecraft:entity.item.pickup neutral @a[distance=..12] ~ ~ ~ 0.6 0.6',
                          'execute on passengers run kill @s', 'data remove entity @s Owner', 'tp @s ~ -200 ~', 'kill @s'])
    # every second: a vault hire whose boss has left the heist clocks off; a new one shows his kit once he's rigged
    G.FUNCS['loop/second'].append('execute in bm:gutter as @e[type=minecraft:wolf,tag=bm.fvault,distance=0..] at @s run function bm:p89/fv/check')
    fn('p89/fv/check', ['scoreboard players operation #me bm.pid = @s bm.pid', 'tag @a[tag=bm.fvme] remove bm.fvme',
                        'execute as @a[tag=bm.gvp,distance=0..] if score @s bm.pid = #me bm.pid run tag @s add bm.fvme',
                        'execute unless entity @a[tag=bm.fvme] run return run function bm:p89/fv/dismiss', 'tag @a[tag=bm.fvme] remove bm.fvme',
                        'execute if entity @s[tag=bm.rigged,tag=!bm.fvdone] run function bm:p89/fv/dress'])
    fn('p89/fv/dress', ['tag @s add bm.fvdone', 'execute if entity @s[tag=bm.frogpet] run function bm:p20/frog/refresh',
                        'execute if entity @s[tag=bm.donado] run function bm:p25/don/refresh'])

    # ================================================================== GOLDTOOTH: the contracts, the wardrobe, Emma's outfits
    from gen_dp import offer
    prev = P70.goldtooth
    def gm(n): return ('gutter_medallion', n)
    def g89():
        d = prev()
        rec = d['Offers']['Recipes']
        for k, (ttl, nm, col, chk, (t, m)) in FOLLOWERS.items():
            rec.append(offer(('gutter_trophy', t), (f'fcontract_{k}', 1), gm(m) if m else None))
        rec += [offer(gm(8), (f'cos_outfit_{o}', 1)) for o in OUTFITS]
        for k in P78.RIBBONS:
            rec.append(offer(gild.price(f'cos_ribbon_{k}', ('gutter_trophy', 1) if f'cos_ribbon_{k}' in P78.HIDDEN else gm(3)), (f'cos_ribbon_{k}', 1)))
        for k in P78.DRESSES:
            rec.append(offer(gild.price(f'cos_dress_{k}', ('gutter_trophy', 1) if f'cos_dress_{k}' in P78.HIDDEN else gm(5)), (f'cos_dress_{k}', 1)))
        for k in P78.CELI:
            rec.append(offer(gild.price(f'cos_celi_{k}', ('gutter_trophy', 1) if f'cos_celi_{k}' in P78.HIDDEN else gm(4)), (f'cos_celi_{k}', 1)))
        for k in P78.ZIB:
            rec.append(offer(gild.price(f'cos_zib_{k}', ('gutter_trophy', 1) if f'cos_zib_{k}' in P78.HIDDEN else gm(4)), (f'cos_zib_{k}', 1)))
        for g in P60.GEMS:                 # (2.67: the vault's own - flagged, and they never leave it: phase98)
            o = offer(gm(6), (f'gem_{g}', 1))
            o['sell'] = dict(o['sell']); c = o['sell']['components'] = dict(o['sell']['components'])     # (a copy - never the item's own)
            c['minecraft:custom_data'] = dict(c['minecraft:custom_data'], bm_vault=B(1))
            c['minecraft:lore'] = list(c['minecraft:lore']) + [T('Bought in the vault - it stays in the vault.', '#e8b8ff', italic=True)]
            rec.append(o)
        # (2.67: the Ethereal Gem is a secret again - made from the nine, never sold)
        return d
    P70.goldtooth = g89
    old_s, new_s = snbt(prev()), snbt(g89())
    lob = G.FUNCS['p70/r/lobby/init']
    assert any(old_s in l for l in lob), "Goldtooth's summon wasn't found"
    G.FUNCS['p70/r/lobby/init'] = [l.replace(old_s, new_s) for l in lob]
    fn('admin/emma_outfits', [G.give(f'cos_outfit_{o}') for o in OUTFITS] + [G.give(f'fcontract_{k}') for k in FOLLOWERS])


def rp(R):
    import sys
    R.TEXTURE_MODS.append(sys.modules[__name__])
    EM = EA.models()
    for name, (tex, els) in models().items():
        if name.startswith('em_body_o'):
            for m in (1, 2, 3, 4, 5):            # (the collar band in the buff's colour, as her scarf)
                R.HATS[f'{name}_m{m}'] = ({a: (f'{v}_m{m}' if a in ('em2_scarf',) and m != 4 else v) for a, v in tex.items()}, els)
        else:
            R.HATS[name] = (tex, els)
